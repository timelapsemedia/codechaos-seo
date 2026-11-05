#!/usr/bin/env python3
"""Gemeinsame GEO-Bausteine für alle Seiten (SISTRIX „Citation Worthiness“, 22.10.2026; siehe _docs/seo-routine.md).

Jede Seite bekommt hier zentral:
  - Kopfzeile „Von Tim Borchert · Zuletzt aktualisiert: TT.MM.JJJJ“ (EN „Last updated“) unter der H1,
  - Inhaltsverzeichnis „Auf dieser Seite“ / „On this page“ mit Sprunglinks auf alle H2 der Seite (H2 bekommen stabile ids),
  - Autorenbox mit echtem Foto von Tim Borchert am Seitenende (vor dem Footer),
  - das Datum für dateModified im JSON-LD (Platzhalter DATUM wird ersetzt).

Das Datum ist das echte letzte inhaltliche Änderungsdatum der Seite und wird NICHT bei jedem Build erneuert:
_build/seiten_datum.json speichert je Seite Datum + Prüfsumme des sichtbaren Hauptinhalts (<main>, ohne die
GEO-Bausteine). Ändert sich der Inhalt, setzt der Build das Datum auf heute; Layout-, Nav-, Footer- oder
Schema-Änderungen zählen nicht. Startwerte: letzter Commit, der den sichtbaren Hauptinhalt geändert hat.

Generierte Seiten rufen ausbauen() in build_pages.py / build_sounds.py auf; handgeschriebene Seiten
(index.html, crucible.html) bekommen dieselben Bausteine über handseiten() (läuft am Ende von build_pages.py).
"""
import datetime, hashlib, html as H, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://codechaos-official.de"
DATEI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seiten_datum.json")
DATUM = "@@GEO_DATUM@@"          # Platzhalter für dateModified im JSON-LD
PERSON_ID = BASE + "/#tim-borchert"
FOTO = "/images/brand/tim-borchert"   # echtes Foto (Quelle: polished.media/tim-borchert-portrait.jpg), -192/-384.webp, -192.jpg, -800.jpg

MONATE = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

TEXT = {
    "de": dict(von="Von", upd="Zuletzt aktualisiert", toc="Auf dieser Seite", about="Über den Autor", more="Mehr über Code Chaos",
               more_url="/#ueber",
               alt="Tim Borchert (Code Chaos) im Studio, Porträtfoto",
               bio="Tim Borchert produziert seit 2016 als Code Chaos Psycore, Hitech und Darkpsy in Hamburg und mastert seine Tracks selbst. "
                   "2021 hat er das Label Abstract Sound Design mitgegründet.",
               extra={"mastering": "Unter dem Namen Polished Media mastert er auch Releases anderer Artists.",
                      "plugin": "Code Chaos Audio ist seine Plugin-Reihe für Hitech, Psycore, Darkpsy und Black Metal."}),
    "en": dict(von="By", upd="Last updated", toc="On this page", about="About the author", more="More about Code Chaos",
               more_url="/en/#about",
               alt="Tim Borchert (Code Chaos) in the studio, portrait photo",
               bio="Tim Borchert has been producing psycore, hitech and darkpsy as Code Chaos in Hamburg since 2016 and masters his own tracks. "
                   "In 2021 he co-founded the label Abstract Sound Design.",
               extra={"mastering": "Under the name Polished Media he also masters releases by other artists.",
                      "plugin": "Code Chaos Audio is his plugin series for hitech, psycore, darkpsy and black metal."}),
}


def autor_ld():
    """author-Objekt für JSON-LD (Person, inline, damit es auch ohne die Startseite auflösbar ist)."""
    return {"@type": "Person", "@id": PERSON_ID, "name": "Tim Borchert", "alternateName": "Code Chaos", "url": BASE + "/",
            "image": BASE + FOTO + "-800.jpg", "jobTitle": "Producer (Hitech Psytrance, Psycore, Darkpsy) und Mastering Engineer",
            "homeLocation": {"@type": "Place", "name": "Hamburg"}}


def publisher_ld():
    return {"@type": "MusicGroup", "@id": BASE + "/#artist", "name": "Code Chaos", "url": BASE + "/",
            "logo": {"@type": "ImageObject", "url": BASE + "/images/brand/codechaos-logo-bone-480.webp"}}


# ───────────── Seitendatum (nur echte Inhaltsänderungen) ─────────────

_GEO_BLOCK = re.compile(r"<!--geo:(\w+)-->.*?<!--/geo:\1-->", re.S)


def hauptbereich(h):
    """<main>…</main>; ohne <main> (crucible.html): von </nav> bis <footer."""
    m = re.search(r"<main\b.*?</main>", h, re.S)
    if m:
        return m.group(0)
    a = h.find("</nav>")
    b = h.rfind("<footer")
    return h[a if a >= 0 else 0:b if b >= 0 else len(h)]


def inhalt(h):
    """Sichtbarer Text des Hauptbereichs, ohne Skripte, Styles und GEO-Bausteine, Leerraum normalisiert."""
    t = _GEO_BLOCK.sub(" ", hauptbereich(h))
    t = re.sub(r"<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->", " ", t, flags=re.S)
    t = H.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t).strip()


def pruefsumme(h):
    return hashlib.sha1(inhalt(h).encode("utf-8")).hexdigest()[:16]


class Register:
    def __init__(self):
        self.d = json.load(open(DATEI, encoding="utf-8")) if os.path.exists(DATEI) else {}
        self.heute = datetime.date.today().isoformat()

    def datum(self, key, h):
        s = pruefsumme(h)
        e = self.d.get(key)
        if e and e.get("hash") in (None, s):      # unverändert (oder Startwert ohne Prüfsumme)
            e["hash"] = s
            return e["datum"]
        self.d[key] = {"datum": self.heute, "hash": s}
        return self.heute

    def speichern(self):
        with open(DATEI, "w", encoding="utf-8") as f:
            json.dump(dict(sorted(self.d.items())), f, ensure_ascii=False, indent=1)
            f.write("\n")


REG = Register()


def anzeige(iso, lang):
    j, m, t = (int(x) for x in iso.split("-"))
    return f"{t:02d}.{m:02d}.{j}" if lang == "de" else f"{t} {MONATE[m - 1]} {j}"


# ───────────── Inhaltsverzeichnis ─────────────

def slug(t):
    t = t.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"), ("&", " ")):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:60].strip("-") or "abschnitt"


def label(inner):
    t = re.sub(r'<span class="visually-hidden">.*?</span>', "", inner, flags=re.S)
    t = re.sub(r"<br\s*/?>", " ", t)
    t = H.unescape(re.sub(r"<[^>]+>", "", t))
    return re.sub(r"\s+", " ", t).strip()


def h2_ids(h):
    """Gibt jeder H2 im Hauptbereich eine stabile id (bestehende bleiben) und liefert [(id, Text)]."""
    teil = hauptbereich(h)
    start = h.find(teil)
    ids = set(re.findall(r'\bid="([^"]+)"', h))
    liste = []

    def ersetze(m):
        attrs, inner = m.group(1) or "", m.group(2)
        im = re.search(r'\bid="([^"]+)"', attrs)
        if im:
            hid = im.group(1)
        else:
            basis = hid = slug(label(inner))
            n = 2
            while hid in ids:
                hid, n = f"{basis}-{n}", n + 1
            ids.add(hid)
            attrs = f' id="{hid}"' + attrs
        liste.append((hid, label(inner)))
        return f"<h2{attrs}>{inner}</h2>"

    # H2 in Dialogen (Impressum/Datenschutz-Modal der Startseite) sind nicht sichtbar → nicht ins Inhaltsverzeichnis
    dialoge = []
    for m in re.finditer(r'<div\b[^>]*role="dialog"[^>]*>', teil):
        tiefe, k = 0, m.end()
        for t in re.finditer(r"<(/?)div\b[^>]*>", teil[k:]):
            if t.group(1):
                if tiefe == 0:
                    dialoge.append((m.start(), k + t.end()))
                    break
                tiefe -= 1
            else:
                tiefe += 1

    def ersetze_sichtbar(m):
        if any(a <= m.start() < b for a, b in dialoge):
            return m.group(0)
        return ersetze(m)

    neu = re.sub(r"<h2(\s[^>]*)?>(.*?)</h2>", ersetze_sichtbar, teil, flags=re.S)
    return h[:start] + neu + h[start + len(teil):], liste


def h1_container_ende(h, tags="div|section|header|article", nach=False):
    """Index direkt vor dem schließenden Tag des Elements (aus tags), das die H1 enthält; nach=True: direkt dahinter."""
    i = h.find("</h1>", h.find("<h1"))
    if i < 0:
        raise SystemExit("GEO: keine H1 gefunden")
    i += 5
    tiefe = 0
    for m in re.finditer(rf"<(/?)({tags})\b[^>]*>", h[i:]):
        if m.group(1):
            if tiefe == 0:
                return i + (m.end() if nach else m.start())
            tiefe -= 1
        elif not m.group(0).endswith("/>"):
            tiefe += 1
    raise SystemExit("GEO: Container der H1 nicht gefunden")


def kopf_html(liste, iso, lang, offen):
    t = TEXT[lang]
    lis = "".join(f'<li><a href="#{i}">{H.escape(x, quote=False)}</a></li>' for i, x in liste)
    return (f'<!--geo:kopf--><p class="geo-meta">{t["von"]} <a href="#autor">Tim Borchert</a> (Code Chaos) · '
            f'{t["upd"]}: <time datetime="{iso}">{anzeige(iso, lang)}</time></p>'
            f'<div class="geo-toc" role="navigation" aria-label="{t["toc"]}"><details{" open" if offen else ""}><summary>{t["toc"]}</summary>'
            f'<ol>{lis}</ol></details></div><!--/geo:kopf-->')   # div statt <nav>: Startseite/Crucible stylen nav global


def autor_html(lang, art):
    t = TEXT[lang]
    extra = t["extra"].get(art, "")
    return (f'<!--geo:autor--><div class="geo-autor-wrap"><aside class="geo-autor" id="autor" aria-label="{t["about"]}">'
            f'<picture><source type="image/webp" srcset="{FOTO}-192.webp 1x, {FOTO}-384.webp 2x">'
            f'<img src="{FOTO}-192.jpg" width="96" height="96" loading="lazy" decoding="async" alt="{t["alt"]}"></picture>'
            f'<div><p class="geo-autor-kicker">{t["about"]}</p><p class="geo-autor-name">Tim Borchert</p>'
            f'<p>{t["bio"]}{" " + extra if extra else ""}</p>'
            f'<p><a href="{t["more_url"]}">{t["more"]} →</a></p></div></aside></div><!--/geo:autor-->')


def ausbauen(h, key, lang, art="ratgeber", toc_offen=True, nach_hero=False):
    """Fügt Kopfzeile + Inhaltsverzeichnis, Autorenbox und CSS ein und ersetzt den Datums-Platzhalter. Idempotent.
    nach_hero=True (Startseiten mit Vollbild-Hero): Kopfzeile + eingeklapptes Inhaltsverzeichnis als schmales Band
    direkt hinter der Hero-Section der H1, damit das Hero-Layout unberührt bleibt."""
    h = re.sub(r"<!--geo:(\w+)-->.*?<!--/geo:\1-->\n?", "", h, flags=re.S)   # alte Bausteine entfernen (handgeschriebene Seiten)
    iso = REG.datum(key, h)
    h, liste = h2_ids(h)
    if len(liste) < 2:
        raise SystemExit(f"GEO: {key} hat nur {len(liste)} H2 – Inhaltsverzeichnis lohnt nicht, bitte prüfen")
    def zeilenanfang(k):   # vor die Einrückung des schließenden Tags einfügen, damit das Entfernen die Datei exakt wiederherstellt
        z = h.rfind("\n", 0, k) + 1
        return z if not h[z:k].strip() else k
    if nach_hero:
        i = h1_container_ende(h, "section", nach=True)
        if h[i:i + 1] == "\n":
            i += 1
        kopf = kopf_html(liste, iso, lang, toc_offen).replace("<!--geo:kopf-->", '<!--geo:kopf--><div class="geo-band"><div class="geo-band-in">', 1) \
            .replace("<!--/geo:kopf-->", "</div></div><!--/geo:kopf-->")
    else:
        i = zeilenanfang(h1_container_ende(h))
        kopf = kopf_html(liste, iso, lang, toc_offen)
    h = h[:i] + kopf + "\n" + h[i:]
    j = h.rfind("</main>")
    if j < 0:
        j = h.rfind("<footer")
    j = zeilenanfang(j)
    h = h[:j] + autor_html(lang, art) + "\n" + h[j:]
    if 'href="/css/geo.css"' not in h:
        h = h.replace("</head>", '<link rel="stylesheet" href="/css/geo.css">\n</head>', 1)
    return h.replace(DATUM, iso), iso


# ───────────── handgeschriebene Seiten ─────────────

def _crucible_ld(h, iso):
    """crucible.html: author + dateModified ins Product/SoftwareApplication-Schema (kein Article auf Produktseiten)."""
    m = re.search(r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)', h, re.S)
    ld = json.loads(m.group(2))
    for n in ld["@graph"]:
        if n.get("@id", "").endswith("#product"):
            n["author"] = autor_ld()
            n["dateModified"] = iso
    return h[:m.start(2)] + json.dumps(ld, ensure_ascii=False, indent=2) + h[m.end(2):]


def handseiten():
    """index.html (DE-Startseite) und crucible.html. Das JSON-LD der Startseite schreibt danach schema_home.py."""
    out = []
    for datei, key, lang, art, offen in (("index.html", "/", "de", "ratgeber", False),
                                          ("crucible.html", "/crucible.html", "en", "plugin", True)):
        p = os.path.join(ROOT, datei)
        h = open(p, encoding="utf-8").read()
        h, iso = ausbauen(h, key, lang, art, toc_offen=offen, nach_hero=(datei == "index.html"))
        if datei == "crucible.html":
            h = _crucible_ld(h, iso)
        open(p, "w", encoding="utf-8", newline="\n").write(h)
        out.append(p)
    return out
