#!/usr/bin/env python3
"""GEO-Merkmale je Seite prüfen (SISTRIX-Studie „Citation Worthiness“, 22.10.2026, 96.418 URLs).

Misst live jede Sitemap-URL auf die Merkmale, die KI-Zitate (ChatGPT, AI Mode, AI Overviews) am stärksten
mit sich bringen (Faktor = so viel öfter zitiert als eine Seite derselben Domain ohne das Merkmal):
  TOC    sichtbares Inhaltsverzeichnis mit Sprungmarken           1,7
  ART    Article-/BlogPosting-Schema (nicht auf Produktseiten)     1,6
  H2     mindestens 5 H2-Überschriften                             1,6
  FAQ    FAQPage-Schema mit echten Fragen                          1,4–1,5
  TAB    Tabelle mit Kopfzeile (<th>)                              1,4–1,5
  AUTOR  Autorenbox mit Foto                                       1,4–1,5
  DATUM  sichtbares „Zuletzt aktualisiert“                         1,3
  WORTE  mindestens 1.000 Wörter                                   1,5
Ohne messbaren Effekt: llms.txt, Breadcrumb-, HowTo-, QAPage-Schema, Lesbarkeitswerte. Korrelation, keine Kausalität.

  python3 geo_merkmale.py https://polished.media [--json]
"""
import html, json, re, sys, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (geo-merkmale)"}


def holen(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read().decode("utf-8", "replace")


def pruefe(u):
    h = holen(u)
    ld = " ".join(re.findall(r'<script[^>]+ld\+json[^>]*>(.*?)</script>', h, re.S))
    typen = set(re.findall(r'"@type"\s*:\s*"([^"]+)"', ld))
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", h, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    produkt = bool(typen & {"Product", "SoftwareApplication"})
    return {
        "TOC": bool(re.search(r'(inhalt|contents|toc|auf dieser seite|on this page)', body, re.I))
               and len(re.findall(r'href="#[^"]+"', body)) >= 3,
        "ART": bool(typen & {"Article", "BlogPosting", "TechArticle", "NewsArticle"}) or produkt,  # Produktseiten: eigenes Schema
        "H2": len(re.findall(r"<h2[\s>]", body, re.I)) >= 5,
        "FAQ": "FAQPage" in typen,
        "TAB": bool(re.search(r"<table.*?<th[\s>]", body, re.S | re.I)),
        "AUTOR": bool(re.search(r'class="[^"]*(autor|author)[^"]*"', body, re.I))
                 and bool(re.search(r'<img[^>]+', body)),
        "DATUM": bool(re.search(r'(zuletzt aktualisiert|aktualisiert am|last updated|updated on)', text, re.I)),
        "WORTE": len(text.split()) >= 1000,
    }


def main():
    site = sys.argv[1].rstrip("/")
    urls = re.findall(r"<loc>(.*?)</loc>", holen(site + "/sitemap.xml"))
    erg = {}
    for u in urls:
        try:
            erg[u] = pruefe(u)
        except Exception as e:  # nie still auf „ok“ fallen
            erg[u] = {"FEHLER": str(e)[:120]}
    if "--json" in sys.argv:
        print(json.dumps(erg, ensure_ascii=False, indent=1))
        return
    zaehl = {}
    for u, r in erg.items():
        fehlt = [k for k, v in r.items() if v is False]
        for k in fehlt:
            zaehl[k] = zaehl.get(k, 0) + 1
        print(f"{len(fehlt)} fehlen  {u.replace(site, '') or '/'}: {', '.join(fehlt) or '–'}")
    print(f"\n{len(urls)} Seiten · fehlend: " + ", ".join(f"{k} {v}" for k, v in sorted(zaehl.items(), key=lambda x: -x[1])))


if __name__ == "__main__":
    main()
