#!/usr/bin/env python3
"""Gumroad-Bewertungen zu den Plugin-Seiten von codechaos-official.de.

Aufruf aus dem Repo-Root:
    python _build/gumroad_reviews.py            # holt alle öffentlichen Bewertungen, schreibt die Datendatei
    python _build/gumroad_reviews.py --trocken  # nur anzeigen, nichts schreiben

Quelle: die öffentlichen Produktseiten auf timberwolf688.gumroad.com (kein Login, kein Schlüssel):
  1. /l/<slug> liefert im Inertia-JSON (data-page) die Produkt-ID und Anzahl/Durchschnitt der Bewertungen,
  2. /product_reviews?product_id=<ID>&page=<n> liefert die Bewertungen selbst (JSON, derselbe Aufruf wie die Seite).
Kauf- und Demo-Produkt (<slug> und <slug>-demo) werden zu einer Plugin-Seite zusammengeführt.

Datendatei: _build/daten/gumroad_bewertungen.json (nur Bewertungsdaten und das Datum der letzten Änderung, damit
ein unveränderter Lauf keine Änderung erzeugt). Sicherheitsnetz: weicht die Zahl der geholten Bewertungen von der Zahl
auf der Produktseite ab oder scheitert ein Abruf, bleibt der alte Stand dieses Produkts erhalten (Exit-Code 2).

Darstellung: render() am Ende, wird von build_pages.build_plugin() aufgerufen. Alle öffentlichen Bewertungen werden
gezeigt (keine Auswahl; EU-Omnibus / § 5b UWG), Texte HTML-escaped, keine Links aus Fremdtext, kein
AggregateRating/Review-Schema.
"""
import html as _html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

HIER = os.path.dirname(os.path.abspath(__file__))
DATEI = os.path.join(HIER, "daten", "gumroad_bewertungen.json")
SHOP = "https://timberwolf688.gumroad.com"
UA = "CodeChaosBewertungsSync/1.0 (+https://codechaos-official.de)"
PAUSE = 2.5            # Sekunden zwischen Abrufen (Rate-Limit schonen)
MAX_SEITEN = 20        # Sicherung gegen Endlosschleife (10 Bewertungen/Seite)
MAX_TEXT = 1500        # Zeichen je Bewertung auf der Seite
MAX_NAME = 40
SICHTBAR = 8           # so viele Bewertungen direkt, der Rest in <details> (alle bleiben auf der Seite)


# ---------------------------------------------------------------- Abruf

def _get(url, json_antwort=False):
    """GET mit Wiederholung bei 429/5xx (Wartezeit nach Retry-After, sonst 20/60/120 s)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json" if json_antwort else "text/html"})
    for versuch in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or versuch == 3:
                raise
            ra = e.headers.get("Retry-After", "")
            time.sleep(min(int(ra), 180) if ra.isdigit() else (20, 60, 120)[versuch])


def produkt_info(permalink):
    """-> {"id", "anzahl", "schnitt"} oder None (Produkt gibt es nicht, 404)."""
    try:
        s = _get(f"{SHOP}/l/{permalink}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    m = re.search(r'data-page="([^"]+)"', s)
    if not m:
        raise RuntimeError(f"{permalink}: keine Seitendaten (Gumroad-Aufbau geändert?)")
    pr = json.loads(_html.unescape(m.group(1)))["props"]["product"]
    return {"id": pr["id"], "anzahl": int(pr["ratings"]["count"]), "schnitt": float(pr["ratings"]["average"])}


def bewertungen_holen(produkt_id):
    alle, seite = [], 1
    while seite <= MAX_SEITEN:
        time.sleep(PAUSE)
        d = json.loads(_get(f"{SHOP}/product_reviews?product_id={urllib.parse.quote(produkt_id, safe='')}&page={seite}", True))
        alle += d["reviews"]
        if seite >= int(d["pagination"]["pages"]):
            break
        seite += 1
    return alle


def _antwort(r):
    a = (r.get("response") or {}).get("message") or ""
    return a.strip()


def normal(permalink, r):
    return {"id": r["id"], "produkt": permalink, "sterne": int(r["rating"]),
            "text": (r.get("message") or "").strip(), "name": ((r.get("rater") or {}).get("name") or "").strip(),
            "datum": (r.get("created_at") or "")[:10], "antwort": _antwort(r)}


def plugin_slugs():
    sys.path.insert(0, HIER)
    from content_plugins import PLUGINS
    return [(p["slug"], p["price"] > 0) for p in PLUGINS if p.get("live")]


def laden():
    if os.path.exists(DATEI):
        return json.load(open(DATEI, encoding="utf-8"))
    return {"stand": "", "ids": {}, "seiten": {}}


def sync(trocken=False):
    """-> (neu, alt, Meldungen, Probleme). Produkt-IDs sind stabil und stehen im Cache (ids): pro Produkt und Lauf genügt ein
    Abruf der Bewertungsliste. Die Produktseite wird nur für unbekannte Produkte und zum Gegenprüfen der Anzahl geholt,
    sobald es Bewertungen gibt."""
    alt = laden()
    ids = dict(alt.get("ids", {}))
    neu = {"stand": alt.get("stand", ""), "ids": ids, "seiten": {}}
    meldungen, probleme = [], []
    for slug, mit_demo in plugin_slugs():
        produkte, bew = [], []
        alte = alt["seiten"].get(slug, {"produkte": [], "bewertungen": []})
        for permalink in [slug] + ([slug + "-demo"] if mit_demo else []):
            try:
                info = None
                if permalink not in ids:
                    info = produkt_info(permalink)
                    time.sleep(PAUSE)
                    if info is None:
                        meldungen.append(f"{permalink}: Produkt nicht gefunden (übersprungen)")
                        continue
                    ids[permalink] = info["id"]
                geholt = [normal(permalink, r) for r in bewertungen_holen(ids[permalink])]
                if not geholt:
                    continue
                if info is None:      # Gegenprobe: Anzahl laut Produktseite
                    info = produkt_info(permalink)
                    time.sleep(PAUSE)
                if info is not None and len(geholt) != info["anzahl"]:
                    raise RuntimeError(f"{len(geholt)} Bewertungen geholt, Produktseite meldet {info['anzahl']}")
                produkte.append({"permalink": permalink, "anzahl": len(geholt),
                                 "schnitt": round(sum(b["sterne"] for b in geholt) / len(geholt), 2)})
                bew += geholt
            except Exception as e:  # noqa: BLE001 - Abruffehler: alten Stand dieses Produkts behalten
                probleme.append(f"{permalink}: {e} (alter Stand bleibt)")
                produkte += [x for x in alte["produkte"] if x["permalink"] == permalink]
                bew += [x for x in alte["bewertungen"] if x["produkt"] == permalink]
        if bew:
            ids_gesehen = set()
            eindeutig = []
            for b in sorted(bew, key=lambda x: (x["datum"], x["id"]), reverse=True):
                if b["id"] not in ids_gesehen:
                    ids_gesehen.add(b["id"])
                    eindeutig.append(b)
            neu["seiten"][slug] = {"produkte": produkte, "bewertungen": eindeutig}
    if json.dumps(neu["seiten"], sort_keys=True) != json.dumps(alt["seiten"], sort_keys=True):
        neu["stand"] = date.today().isoformat()
        for slug in sorted(set(alt["seiten"]) | set(neu["seiten"])):
            a = {b["id"] for b in alt["seiten"].get(slug, {}).get("bewertungen", [])}
            n = {b["id"] for b in neu["seiten"].get(slug, {}).get("bewertungen", [])}
            if n - a:
                meldungen.append(f"{slug}: {len(n - a)} neue Bewertung(en)")
            if a - n:
                meldungen.append(f"{slug}: {len(a - n)} Bewertung(en) bei Gumroad nicht mehr vorhanden")
            if a == n and a:
                meldungen.append(f"{slug}: Inhalt einer Bewertung geändert")
    return neu, alt, meldungen, probleme


def speichern(neu):
    text = json.dumps(neu, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    with open(DATEI, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


# ---------------------------------------------------------------- Darstellung

def _esc(t):
    return _html.escape(t, quote=False)


_DE = set("der die das und ich nicht ist mit für ein eine sehr auch aber wie zu von auf den dem es sind war habe hat kann".split())
_EN = set("the and is to of for it with this that was have has very but not are you can my on in a".split())


def _sprache(text):
    w = re.findall(r"[a-zäöüß']+", text.lower())
    de, en = sum(x in _DE for x in w), sum(x in _EN for x in w)
    return "de" if de > en else "en" if en > de else ""


def _kuerzen(t, n):
    t = re.sub(r"\s+", " ", t).strip()
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + " …"


def _ohne_links(t):
    return re.sub(r"https?://\S+|www\.\S+", "", t).strip()


def _zahl(x, lang):
    s = f"{x:.1f}"
    return s.replace(".", ",") if lang == "de" else s


def _datum(iso, lang):
    try:
        y, m, d = iso.split("-")
    except ValueError:
        return iso
    return f"{d}.{m}.{y}" if lang == "de" else iso


def _sterne(n, lang):
    return ("★" * n + "☆" * (5 - n)), (f"{n} von 5 Sternen" if lang == "de" else f"{n} out of 5 stars")


T = {
    "de": dict(h="Bewertungen auf Gumroad", beides=" (Kauf- und Demo-Version zusammen)", rev="Bewertung", revs="Bewertungen", notext="ohne Text", stars="Sterne", star1="Stern",
               demo="Demo", prod="Produkt", reply="Antwort von Code Chaos Audio", more="Weitere {n} Bewertungen anzeigen",
               avg="{a} von 5 Sternen bei {n} {b}", src="Quelle: Gumroad", link="Alle Bewertungen auf Gumroad", stand="Stand",
               intro=("Hier stehen alle öffentlichen Gumroad-Bewertungen zu {name}{beides}, nicht nur die guten, "
                      "neueste zuerst. Ob die Bewertenden das Plugin tatsächlich genutzt haben, prüfen wir nicht selbst. "
                      "Neue Bewertungen übernehmen wir regelmäßig und unverändert."),
               orig="Originalwortlaut", notext_line="Außerdem {n} {b} ohne Text: {verteilung}.", cut="Gekürzt, vollständig auf Gumroad"),
    "en": dict(h="Reviews on Gumroad", beides=" (full and demo version together)", rev="rating", revs="ratings", notext="without text", stars="stars", star1="star",
               demo="demo", prod="product", reply="Reply from Code Chaos Audio", more="Show {n} more reviews",
               avg="{a} out of 5 stars from {n} {b}", src="Source: Gumroad", link="All reviews on Gumroad", stand="As of",
               intro=("This lists every public Gumroad review of {name}{beides}, not just the good ones, newest first. "
                      "We do not check ourselves whether reviewers actually used the plugin. New reviews are copied over regularly and unchanged."),
               orig="Original wording", notext_line="Plus {n} {b} without text: {verteilung}.", cut="Shortened, full text on Gumroad"),
}


def render(slug, lang="de", daten=None):
    """HTML der Bewertungs-Section für Plugin-Seite slug oder "" (keine Bewertungen). Rückgabe ist ein komplettes <section>."""
    d = (daten if daten is not None else laden())["seiten"].get(slug)
    if not d or not d["bewertungen"]:
        return ""
    t = T[lang]
    bew = d["bewertungen"]
    n = len(bew)
    schnitt = sum(b["sterne"] for b in bew) / n
    haupt = d["produkte"][0]["permalink"]
    quelle = f"{SHOP}/l/{haupt}"
    mit_text = [b for b in bew if b["text"]]
    ohne = [b for b in bew if not b["text"]]
    daten_stand = (daten if daten is not None else laden()).get("stand", "")

    def karte(b):
        gl, al = _sterne(b["sterne"], lang)
        text = _kuerzen(b["text"], MAX_TEXT)
        sl = _sprache(b["text"])
        lang_attr = f' lang="{sl}"' if sl and sl != lang else ""
        name = _esc(_kuerzen(b["name"], MAX_NAME)) or ("Anonym" if lang == "de" else "Anonymous")
        demo = f", {t['demo']}" if b["produkt"].endswith("-demo") else ""
        gekuerzt = f' <a href="{quelle}" target="_blank" rel="noopener">{t["cut"]}</a>' if len(re.sub(r"\s+", " ", b["text"]).strip()) > MAX_TEXT else ""
        ant = _ohne_links(b.get("antwort", ""))
        antwort = ""
        if ant and len(ant) <= 400:
            antwort = f'<p class="rev-reply"><strong>{t["reply"]}:</strong> {_esc(ant)}</p>'
        return (f'<blockquote class="rev"{lang_attr}><p>{_esc(text)}{gekuerzt}</p>'
                f'<footer><span class="rev-stars" role="img" aria-label="{al}">{gl}</span> {name}, {_datum(b["datum"], lang)}{demo}</footer>{antwort}</blockquote>')

    karten = [karte(b) for b in mit_text]
    sichtbar = "".join(karten[:SICHTBAR])
    rest = ""
    if len(karten) > SICHTBAR:
        rest = f'<details class="rev-more"><summary>{t["more"].format(n=len(karten) - SICHTBAR)}</summary>{"".join(karten[SICHTBAR:])}</details>'
    ohne_zeile = ""
    if ohne:
        zaehl = {}
        for b in ohne:
            zaehl[b["sterne"]] = zaehl.get(b["sterne"], 0) + 1
        ver = ", ".join(f"{c}× {s} {t['star1'] if s == 1 else t['stars']}" for s, c in sorted(zaehl.items(), reverse=True))
        ohne_zeile = f'<p>{t["notext_line"].format(n=len(ohne), b=t["rev"] if len(ohne) == 1 else t["revs"], verteilung=ver)}</p>'
    avg = t["avg"].format(a=_zahl(schnitt, lang), n=n, b=t["rev"] if n == 1 else t["revs"])
    stand = f" · {t['stand']} {_datum(daten_stand, lang)}" if daten_stand else ""
    return f"""<section aria-labelledby="bew-t">
  <div class="wrap narrow prose">
    <h2 id="bew-t">{t["h"]}</h2>
    <p class="rev-sum"><strong>{avg}</strong>{stand} · <a href="{quelle}" target="_blank" rel="noopener">{t["link"]}</a></p>
    <p>{t["intro"].format(name=_esc(slug_name(slug)), beides=t["beides"] if len(d["produkte"]) > 1 else "")}</p>
    {sichtbar}{rest}{ohne_zeile}
  </div>
</section>
"""


_NAMEN = {}


def slug_name(slug):
    if not _NAMEN:
        sys.path.insert(0, HIER)
        from content_plugins import PLUGINS
        _NAMEN.update({p["slug"]: p["name"] for p in PLUGINS})
    return _NAMEN.get(slug, slug)


# ---------------------------------------------------------------- Kommandozeile

if __name__ == "__main__":
    trocken = "--trocken" in sys.argv
    neu, alt, meldungen, probleme = sync()
    geaendert = json.dumps(neu, sort_keys=True) != json.dumps(alt, sort_keys=True)
    for m in meldungen:
        print("-", m)
    for p in probleme:
        print("! PROBLEM:", p)
    seiten = {s: len(v["bewertungen"]) for s, v in neu["seiten"].items()}
    print("Bewertungen je Seite:", seiten or "keine")
    if geaendert and not trocken:
        speichern(neu)
    print("GEAENDERT" if geaendert else "UNVERAENDERT")
    sys.exit(2 if probleme else 0)
