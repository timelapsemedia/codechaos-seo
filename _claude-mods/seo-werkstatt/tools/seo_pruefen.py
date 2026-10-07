#!/usr/bin/env python3
"""SEO-Prüfung einer Seite (URL oder lokale HTML-Datei) oder einer Sitemap. Gibt JSON aus; misst, schätzt nicht.

seo_pruefen.py seite <url|datei>
seo_pruefen.py sitemap <url> [max_urls]
"""
import json, re, sys, time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

UA = {"User-Agent": "Mozilla/5.0 (compatible; seo-werkstatt/0.1; +https://claude.ai/code)"}

def laden(ziel):
    if re.match(r"^https?://", ziel):
        t = time.time()
        r = requests.get(ziel, headers=UA, timeout=30, allow_redirects=True)
        kette = [{"url": h.url, "status": h.status_code} for h in r.history]
        return r.text, {"status": r.status_code, "end_url": r.url, "weiterleitungen": kette, "antwortzeit_s": round(time.time() - t, 2),
                        "x_robots_tag": r.headers.get("X-Robots-Tag"), "content_type": r.headers.get("Content-Type")}, r.url
    with open(ziel, encoding="utf-8", errors="replace") as f:
        return f.read(), {"datei": ziel}, None

def seite(ziel):
    html, meta, basis = laden(ziel)
    s = BeautifulSoup(html, "lxml")
    def m(attr, val):
        t = s.find("meta", attrs={attr: re.compile(f"^{re.escape(val)}$", re.I)})
        return t.get("content") if t else None
    title = s.title.get_text(strip=True) if s.title else None
    canon = s.find("link", rel=lambda v: v and "canonical" in v)
    hreflang = [{"lang": l.get("hreflang"), "href": l.get("href")} for l in s.find_all("link", hreflang=True)]
    jsonld, fehler_ld = [], []
    for sc in s.find_all("script", type="application/ld+json"):
        try:
            d = json.loads(sc.string or "")
            items = d if isinstance(d, list) else d.get("@graph", [d]) if isinstance(d, dict) else []
            jsonld += [str(i.get("@type")) for i in items if isinstance(i, dict)]
        except Exception as ex:
            fehler_ld.append(str(ex)[:120])
    imgs = s.find_all("img")
    ohne_alt = [i.get("src") for i in imgs if not i.get("alt")]
    links = [a.get("href") for a in s.find_all("a", href=True)]
    host = urlparse(basis).netloc if basis else None
    intern = [l for l in links if basis and urlparse(urljoin(basis, l)).netloc == host]
    text = s.get_text(" ", strip=True)
    res = {**meta,
           "title": title, "title_laenge": len(title) if title else 0,
           "meta_description": m("name", "description"), "meta_description_laenge": len(m("name", "description") or ""),
           "robots_meta": m("name", "robots"), "canonical": canon.get("href") if canon else None,
           "lang": (s.html.get("lang") if s.html else None), "hreflang": hreflang,
           "og": {k: m("property", f"og:{k}") for k in ["title", "description", "image", "url", "type"]},
           "twitter_card": m("name", "twitter:card"),
           "h1": [h.get_text(" ", strip=True)[:120] for h in s.find_all("h1")], "h2_anzahl": len(s.find_all("h2")),
           "bilder": len(imgs), "bilder_ohne_alt": len(ohne_alt), "beispiele_ohne_alt": ohne_alt[:5],
           "links_gesamt": len(links), "links_intern": len(intern),
           "woerter": len(text.split()), "jsonld_typen": jsonld, "jsonld_fehler": fehler_ld}
    p = []
    if not title: p.append("kein <title>")
    elif len(title) > 60: p.append(f"<title> {len(title)} Zeichen (Richtwert ≤ 60)")
    if not res["meta_description"]: p.append("keine Meta-Description")
    elif res["meta_description_laenge"] > 160: p.append(f"Meta-Description {res['meta_description_laenge']} Zeichen (Richtwert ≤ 160)")
    if len(res["h1"]) != 1: p.append(f"{len(res['h1'])} × h1 (genau eine empfohlen)")
    if not res["canonical"]: p.append("kein canonical")
    if res["robots_meta"] and "noindex" in res["robots_meta"].lower(): p.append("robots-Meta: noindex")
    if res.get("x_robots_tag") and "noindex" in res["x_robots_tag"].lower(): p.append("X-Robots-Tag: noindex")
    if res["bilder_ohne_alt"]: p.append(f"{res['bilder_ohne_alt']} Bilder ohne alt")
    if fehler_ld: p.append("JSON-LD nicht parsebar")
    if not res["og"]["image"]: p.append("kein og:image (Vorschaubild beim Teilen)")
    if not res["lang"]: p.append("kein lang-Attribut")
    if res.get("status") and res["status"] >= 400: p.append(f"HTTP {res['status']}")
    if len(res.get("weiterleitungen", [])) > 1: p.append(f"{len(res['weiterleitungen'])} Weiterleitungen in Folge")
    res["probleme"] = p
    return res

def sitemap(url, max_urls=200):
    r = requests.get(url, headers=UA, timeout=30)
    s = BeautifulSoup(r.text, "xml")
    subs = [l.get_text(strip=True) for l in s.select("sitemap > loc")]
    urls = [l.get_text(strip=True) for l in s.select("url > loc")]
    for sub in subs[:20]:
        try:
            urls += [l.get_text(strip=True) for l in BeautifulSoup(requests.get(sub, headers=UA, timeout=30).text, "xml").select("url > loc")]
        except Exception:
            pass
    status = {}
    for u in urls[:max_urls]:
        try:
            h = requests.head(u, headers=UA, timeout=15, allow_redirects=False)
            status[u] = h.status_code
        except Exception as ex:
            status[u] = f"Fehler: {type(ex).__name__}"
    nicht200 = {u: c for u, c in status.items() if c != 200}
    return {"sitemap": url, "http": r.status_code, "unter_sitemaps": len(subs), "urls_gesamt": len(urls), "geprueft": len(status), "nicht_200": nicht200}

def site(ordner, max_dateien=3000):
    """Statische Website lokal prüfen (vor dem Push): kaputte lokale Links/Bilder (inkl. Groß/Klein und .jpg/.jpeg),
    unausgeglichene <div>, doppelte Titel, fehlende alt, hreflang-Gegenseitigkeit."""
    import os
    from collections import Counter, defaultdict
    root = os.path.abspath(ordner)
    alle = {}
    for d, _, fs in os.walk(root):
        if "/." in d.replace("\\", "/") or "node_modules" in d: continue
        for f in fs:
            rel = os.path.relpath(os.path.join(d, f), root).replace("\\", "/")
            alle[rel] = True
    lower = {k.lower(): k for k in alle}
    html = [k for k in alle if k.lower().endswith((".html", ".htm"))][:max_dateien]
    kaputt, fast, divs, ohne_alt, titel, hreflang = [], [], [], 0, defaultdict(list), {}
    for rel in html:
        src = open(os.path.join(root, rel), encoding="utf-8", errors="replace").read()
        soup = BeautifulSoup(src, "lxml")
        oeffnend = len(re.findall(r"<div\b", src, re.I)); schliessend = len(re.findall(r"</div\s*>", src, re.I))
        if oeffnend != schliessend: divs.append({"datei": rel, "auf": oeffnend, "zu": schliessend})
        t = soup.title.get_text(strip=True) if soup.title else ""
        if t: titel[t].append(rel)
        ohne_alt += sum(1 for i in soup.find_all("img") if not i.get("alt"))
        hl = {l.get("hreflang"): l.get("href") for l in soup.find_all("link", hreflang=True)}
        if hl: hreflang[rel] = hl
        for tag, attr in (("a", "href"), ("img", "src"), ("link", "href"), ("script", "src"), ("source", "src"), ("source", "srcset")):
            for el in soup.find_all(tag):
                v = (el.get(attr) or "").split(",")[0].strip().split(" ")[0]
                if not v or re.match(r"^(https?:|//|mailto:|tel:|#|data:|javascript:)", v): continue
                ziel = v.split("#")[0].split("?")[0]
                if not ziel: continue
                if ziel.startswith("/"): kand = ziel.lstrip("/")
                else: kand = os.path.normpath(os.path.join(os.path.dirname(rel), ziel)).replace("\\", "/")
                kand = "" if kand in (".", "./") else kand.strip("/")
                cands = [kand, (kand + "/index.html").lstrip("/"), kand + ".html"]
                if any(c in alle for c in cands): continue
                treffer = next((lower[c.lower()] for c in cands if c.lower() in lower), None)
                if treffer:
                    fast.append({"datei": rel, "verweis": v, "existiert_als": treffer, "grund": "Groß-/Kleinschreibung (GitHub Pages unterscheidet)"}); continue
                stamm = re.sub(r"\.(jpe?g|png|webp|gif|avif)$", "", kand, flags=re.I)
                alt = next((k for k in alle if re.sub(r"\.(jpe?g|png|webp|gif|avif)$", "", k, flags=re.I) == stamm and k != kand), None)
                if alt:
                    fast.append({"datei": rel, "verweis": v, "existiert_als": alt, "grund": "andere Dateiendung"}); continue
                kaputt.append({"datei": rel, "verweis": v})
    # hreflang gegenseitig? Seite A verweist auf B (andere Sprache) -> B sollte auf A zurückverweisen.
    einseitig = []
    norm = lambda h: re.sub(r"^https?://[^/]+/", "", h or "").split("#")[0].strip("/")
    def datei_zu(pfad):
        for c in [pfad, (pfad + "/index.html").lstrip("/"), pfad + ".html"]:
            if c in alle: return c
    for rel, hl in hreflang.items():
        eigen = {rel.strip("/"), rel.replace("index.html", "").strip("/")}
        for lang, href in hl.items():
            if not href or lang == "x-default": continue
            ziel = datei_zu(norm(href))
            if not ziel or ziel == rel: continue
            zurueck = any(norm(h) in eigen for h in hreflang.get(ziel, {}).values())
            if not zurueck: einseitig.append({"von": rel, "nach": ziel, "lang": lang})
    doppelt = {t: fs for t, fs in titel.items() if len(fs) > 1}
    return {"ordner": root, "html_dateien": len(html), "kaputte_verweise": kaputt[:200], "kaputte_verweise_anzahl": len(kaputt),
            "fast_richtig": fast[:100], "div_unausgeglichen": divs[:100], "doppelte_titel": dict(list(doppelt.items())[:50]),
            "bilder_ohne_alt": ohne_alt, "hreflang_einseitig": einseitig[:100]}

if __name__ == "__main__":
    try:
        if sys.argv[1] == "site":
            print(json.dumps(site(sys.argv[2]), ensure_ascii=False))
        elif sys.argv[1] == "seite":
            print(json.dumps(seite(sys.argv[2]), ensure_ascii=False))
        else:
            print(json.dumps(sitemap(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 200), ensure_ascii=False))
    except Exception as ex:
        print(json.dumps({"fehler": f"{type(ex).__name__}: {str(ex)[:300]}"}))
