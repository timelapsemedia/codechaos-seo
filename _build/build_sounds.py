#!/usr/bin/env python3
"""Erzeugt /sounds/ (Sammelseite für die Datei-Produkte: Samples, MIDI, Presets, IRs, Template).

Aufruf aus dem Repo-Root:  python3 _build/build_sounds.py
Fakten stammen aus codechaos-store/products/<slug>/description.html (Stand 29.10.2026). Nichts ergänzen, was dort nicht steht.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pages as bp  # noqa: E402

BASE, ROOT, esc = bp.BASE, bp.ROOT, bp.esc
DATE = "2026-10-29"
URL = BASE + "/sounds/"
G = "https://timberwolf688.gumroad.com/l/"

TITLE = "Samples, MIDI & Presets für Psytrance und Black Metal | Code Chaos"
DESC = ("Code Chaos Audio: Black Metal Drum Kit, MIDI Grooves, Cab-IRs, Hitech FM Presets für Vital und Serum 2, "
        "Hitech Arsenal Samples und Ableton-Template. Ab 9 €, Sofort-Download, ohne Login.")

# (slug, gruppe, name, preis, teaser, bullets, wofür)
ITEMS = [
    ("black-metal-drum-kit", "metal", "Black Metal Drum Kit", 12,
     "47 synthetisch erzeugte Drum-Samples und 30 humanisierte MIDI-Grooves für rohe Black-Metal-Drums.",
     ["6 Kicks, 21 Snares (5 Velocity-Stufen mit je 3 Round-Robins), 5 Toms, 9 Hats, 6 Becken",
      "26 MIDI-Grooves (Blasts, Gallop, Black'n'Roll, Doom, 60–230 BPM) plus 4 Fills, je als Grid- und Human-Version",
      "44,1 kHz / 24 Bit WAV, normalisiert, ohne DC-Offset; General-MIDI-Belegung"]),
    ("black-metal-midi-grooves-2", "metal", "Black Metal MIDI Grooves 2", 9,
     "74 humanisierte Drum-Grooves als MIDI für Bands und Heimproduzenten ohne Schlagzeuger.",
     ["14 Blasts, 6 Gallops, 6 D-Beats, 6 Mid-Tempo-/Double-Bass-Grooves, 6 Doom-Grooves, 12 Fills, Transitions, Intros/Outros",
      "60–240 BPM, vier Belegungen: General MIDI, Code Chaos Black Metal Drum Kit (mit SFZ), MT Power Drum Kit 2, DrumGizmo DRSKit",
      "Reine MIDI-Dateien, in jeder DAW nutzbar"]),
    ("black-metal-tone-kit", "metal", "Black Metal Tone Kit", 9,
     "19 synthetisch erzeugte Cab-IRs und 16 REAPER-FX-Chains für einen kalten, breiten Black-Metal-Gitarren- und Basssound.",
     ["19 Cab-IRs (je 48 und 44,1 kHz, 24 Bit WAV), darunter 6 entschärfte Versionen gegen Zischeln und 3 Bass-Cabs",
      "10 REAPER-Chains, die nur REAPERs eigene Effekte nutzen, plus 6 „Heavy Bus“-Chains (Update 1.1, kostenlos)",
      "Läuft mit Neural Amp Modeler (kostenlos) und jedem IR-Loader"]),
    ("hitech-arsenal-1", "psy", "Hitech Arsenal Vol. 1", 15,
     "120 Hitech- und Psycore-Samples: Kicks, rollende Bässe, FM-Leads, Glitches, FX und Loops bei 190/200 BPM.",
     ["12 Kicks, 16 Bass-One-Shots, 12 FM-Leads, 8 Stabs, 25 Glitch-Percussion, 12 Hats, 15 FX",
      "12 Bass-Loops und 8 Synth-Loops (190/200 BPM), taktgenau geschnitten",
      "44,1 kHz / 24 Bit WAV, jede Datei mit Tonart und BPM benannt"]),
    ("hitech-fm-vital", "psy", "Hitech FM für Vital", 12,
     "32 FM-Presets für Vital (die kostenlose Version genügt): Leads, rollende Bässe, Plucks und FX.",
     ["12 Leads, 8 Bässe, 6 Plucks, 6 FX auf Basis von 3-Operator-FM",
      "Vital 1.5.5 oder neuer; Windows, macOS und Linux",
      "Reine Preset-Dateien, ohne Login und Lizenzserver"]),
    ("hitech-fm-serum2", "psy", "Hitech FM für Serum 2", 12,
     "24 Serum-2-Presets: FM/AM-Leads, Plucks, FX sowie dunkle Brass- und Chor-Pads für die Breaks.",
     ["8 Leads, 6 Plucks, 4 FX, 3 Brass, 3 Pads",
      "Benötigt Xfer Serum 2 (2.0.13 oder neuer)",
      "Reine Preset-Dateien, ohne Login und Lizenzserver"]),
    ("hitech-fm-industrial", "psy", "Hitech FM Industrial / Metallic", 9,
     "Metallische FM-Sounds ohne Operator: 30 Vital- und 26 Serum-2-Presets für Hitech, Psycore und Industrial.",
     ["Stabs, Metal Hits und Bells, Industrial-Bässe, Talking- und Growl-Filter, Texturen",
      "Zu jedem Preset eine Zeile, wie er gebaut ist (FM-Ratio, Filter, Verzerrung, Modulation), plus PRESET-GUIDE",
      "Ein Download mit zwei getrennten Banks, du nimmst die für deinen Synth"]),
    ("psycore-ableton-template", "psy", "Psycore Production Template (Ableton Live 12)", 19,
     "Das Produktions-Set hinter dem Code-Chaos-Sound als Vorlage: 77 Spuren mit fertigen Sounddesign- und FX-Ketten.",
     ["Geschichteter Kick, 4 Serum-2-Bass-Layer, 13 Vital-FM-Instrumente, 5 Returns und komplette Master-Chain",
      "16-Takte-Starter-Groove in F Phrygisch bei 260 BPM, nutzbar von 180 bis 300 BPM",
      "Kostenlos für alle Käufer: Lern-Set „Dissect Me“ (11 Lektionen à 8 Takte, 128-Takte-Arrangement)"]),
]

GROUPS = [
    ("metal", "Black Metal: Drums, MIDI und Gitarrensound",
     "Für Bands und Heimproduzenten ohne Schlagzeuger oder teure Amp-Suite. Alle Sounds sind synthetisch erzeugt, ohne fremde Samples. "
     "Wer lieber ein Plugin will: die Code Chaos Black Metal Suite (Frostfret, Hoarfell, Gravesaw, Rimehall) findest du in der "),
    ("psy", "Hitech, Psycore und Darkpsy: Samples, Presets und Template",
     "Für Producer, die bei 180 bis 300 BPM arbeiten. Die Presets und Samples kommen aus dem Code-Chaos-Studio. "
     "Kick und Rolling Bass zusammen als Plugin gibt es als "),
]

FAQ = [
    ("Brauche ich einen Account oder Lizenzserver?",
     "Nein. Alle Produkte auf dieser Seite sind einfache Dateien (WAV, MIDI, Presets, IRs, ein Ableton-Set), die dir gehören. Kein Login, kein Lizenzserver, kein Abo."),
    ("Darf ich die Sounds in meinen Veröffentlichungen nutzen?",
     "Ja, für deine eigenen Releases, lizenzfrei. Weiterverkauf oder Weitergabe der Dateien selbst ist nicht erlaubt; die genauen Bedingungen stehen in der LICENSE.txt im Paket."),
    ("Woher stammen die Sounds?",
     "Von Code Chaos selbst erzeugt, synthetisiert oder gebaut. Es sind keine fremden Samples, Impulsantworten oder Presets enthalten."),
    ("In welcher DAW funktioniert das?",
     "Samples und MIDI laufen in jeder DAW oder jedem Sampler. Die Presets brauchen Vital (die kostenlose Version genügt) bzw. Serum 2. "
     "Das Template ist für Ableton Live 12 (Suite). Die REAPER-Chains im Tone Kit nutzen nur REAPERs eigene Effekte."),
    ("Gibt es etwas zum Ausprobieren?",
     "Zu allen Plugins gibt es kostenlose Demos, siehe die Plugin-Übersicht. Die Datei-Produkte kosten zwischen 9 und 19 €."),
]


def utm(slug):
    return f"{G}{slug}?utm_source=site&amp;utm_medium=landing&amp;utm_campaign=sounds"


def card(it):
    slug, _, name, price, teaser, bullets = it
    img = (f'<picture><source type="image/webp" srcset="/images/sounds/{slug}.webp"><img src="/images/sounds/{slug}.jpg" width="640" height="360" '
           f'loading="lazy" decoding="async" alt="{esc("Cover: " + name)}"></picture>')
    lis = "".join(f"<li>{esc(b)}</li>" for b in bullets)
    return (f'<article class="pcard"><div class="pcard-img">{img}</div>'
            f'<div class="pcard-body"><h3>{esc(name)}</h3><p>{esc(teaser)}</p><ul class="pbul">{lis}</ul>'
            f'<p class="pcard-meta"><span class="price-tag">{price} €</span> Sofort-Download auf Gumroad</p>'
            f'<p class="pcard-links"><a href="{utm(slug)}">Ansehen &amp; kaufen</a></p></div></article>')


def build():
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": URL + "#webpage", "url": URL, "name": TITLE, "description": DESC, "inLanguage": "de",
         "isPartOf": {"@id": BASE + "/#website"}, "datePublished": DATE, "dateModified": DATE,
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "item": {
                 "@type": "Product", "name": it[2], "description": it[4], "url": f"{G}{it[0]}",
                 "image": f"{BASE}/images/sounds/{it[0]}.jpg", "brand": {"@type": "Brand", "name": "Code Chaos Audio"},
                 "offers": {"@type": "Offer", "price": str(it[3]), "priceCurrency": "EUR", "availability": "https://schema.org/InStock",
                            "url": f"{G}{it[0]}"}}} for i, it in enumerate(ITEMS)]}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Startseite", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Samples & Presets", "item": URL}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": bp.strip(a)}} for q, a in FAQ]},
    ]}
    sections = ""
    tail = {"metal": '<a href="/plugins/">Plugin-Übersicht</a>.', "psy": '<a href="/plugins/psy-kick-bass/">Kick+Bass Engine</a>.'}
    for i, (g, h, intro) in enumerate(GROUPS):
        cards = "".join(card(it) for it in ITEMS if it[1] == g)
        sections += (f'<section{" class=alt" if i % 2 == 0 else ""} aria-labelledby="g-{g}"><div class="wrap"><h2 id="g-{g}">{esc(h)}</h2>'
                     f'<p class="prose">{esc(intro)}{tail[g]}</p><div class="pcards">{cards}</div></div></section>\n')
    rows = "".join(f'<tr><th scope="row">{esc(it[2])}</th><td>{it[3]} €</td></tr>' for it in ITEMS)
    body = f"""<main id="main">
<div class="wrap crumbs"><nav aria-label="Breadcrumb"><ol><li><a href="/">Startseite</a></li><li aria-current="page">Samples &amp; Presets</li></ol></nav></div>
<section class="s-hero">
  <div class="wrap narrow">
    <span class="eyebrow">Code Chaos Audio</span>
    <h1>Samples, MIDI und Presets für Psytrance und Black Metal</h1>
    <div class="rule" aria-hidden="true"><i></i></div>
    <p class="answer">Code Chaos Audio verkauft neben den Plugins auch einfache Datei-Produkte für Hitech, Psycore und Black Metal: Drum-Samples, MIDI-Grooves, Cab-Impulsantworten, Vital- und Serum-2-Presets und ein Ableton-Template. Alles von Code Chaos (Tim Borchert, Hamburg) selbst erzeugt, lizenzfrei für deine eigenen Releases, ab 9 € als Sofort-Download auf Gumroad, ohne Login und ohne Lizenzserver.</p>
  </div>
</section>
{sections}<section aria-labelledby="p-t">
  <div class="wrap narrow">
    <h2 id="p-t">Preise im Überblick</h2>
    <div class="table-scroll"><table class="cmp"><thead><tr><th>Produkt</th><th>Preis</th></tr></thead><tbody>{rows}</tbody></table></div>
  </div>
</section>
<section class="alt" aria-labelledby="faq-t">
  <div class="wrap narrow">
    <h2 id="faq-t">Häufige Fragen</h2>
    {bp.faq_html(FAQ)}
    <p class="prose" style="margin-top:22px"><a href="/plugins/">Alle Plugins ansehen →</a> · <a href="/mastering/">Mastering für deinen Track →</a></p>
  </div>
</section>
</main>
"""
    html = (bp.head("de", URL, None, TITLE, DESC, BASE + "/images/sounds/og.jpg", "Black Metal Drum Kit von Code Chaos Audio", ld, og_type="website")
            + bp.nav("de", None, "sounds") + body + bp.footer("de"))
    path = os.path.join(ROOT, "sounds", "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html)
    return path


if __name__ == "__main__":
    print(build())
