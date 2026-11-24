#!/usr/bin/env python3
"""Zitierbare Belege für die Genre-Seiten (Aufgabe seo-geo-zitierbar, 24.11.2026).

Grundlage: Aggarwal et al. 2024, „GEO: Generative Engine Optimization“ (KDD, DOI 10.1145/3637528.3671900):
Quellenangaben, wörtliche Zitate und Statistiken heben die Sichtbarkeit in generativen Antworten um 30–40 %.

Regeln:
  - Jedes Zitat steht wörtlich in der verlinkten Quelle (am 24.11.2026 im Volltext nachgelesen). Nichts umformulieren.
  - Rechenwerte (Millisekunden je Schlag) entstehen hier aus dem Tempo: 60000 / BPM, Sechzehntel = ein Viertel davon.
  - Lautheitswerte stammen aus _build/daten/tabellen_codechaos_*.md (eigene Messung); bei neuer Messung hier nachziehen.
  - Keine Preise, keine Kauflinks (Angebots-Sperre Dezember 2026).
"""

CHARLES = dict(
    autor="Christopher Charles", jahr=2020,
    titel="Genre in Practice: Categories, Metadata and Music-Making in Psytrance Culture",
    quelle="Dancecult: Journal of Electronic Dance Music Culture 12(1)",
    url="https://doi.org/10.12801/1947-5403.2020.12.01.09")
VITOS = dict(
    autor="Botond Vitos", jahr=2009,
    titel="The Inverted Sublimity of the Dark Psytrance Dance Floor",
    quelle="Dancecult: Journal of Electronic Dance Music Culture 1(1)",
    url="https://doi.org/10.12801/1947-5403.2009.01.01.10")
ITU = dict(
    autor="International Telecommunication Union", jahr=2023,
    titel="Recommendation ITU-R BS.1770-5: Algorithms to measure audio programme loudness and true-peak audio level",
    quelle="ITU-R", url="https://www.itu.int/rec/R-REC-BS.1770")

TEMPI = {"psycore": (180, 200, 240, 300), "hitech-psytrance": (170, 185, 200, 230), "darkpsy": (150, 160, 175, 200)}

# Wörtliche Zitate je Seite: (Text, Quelle)
ZITAT = {
    "psycore": ("hi-tech and psycore, the latter reaching tempi upwards of 190 BPM", CHARLES),
    "hitech-psytrance": ("very fast, intense genres meant for performance at night", CHARLES),
    "darkpsy": ("an underlying tempo which exceeds 150 BPM", VITOS),
}

T = {
 "en": {
  "h2": {"psycore": "Psycore BPM in numbers", "hitech-psytrance": "Hitech BPM in numbers", "darkpsy": "Darkpsy BPM in numbers"},
  "satz": {
   "psycore": "<strong>Psycore runs at 180 to 300+ BPM, typically 190–240 BPM.</strong> One beat then lasts between 333 and 200 milliseconds and a sixteenth note between 83 and 50 ms, which is why kick and bass have to be extremely short.",
   "hitech-psytrance": "<strong>Hitech psytrance runs at 170 to 230+ BPM, typically 180–200 BPM.</strong> One beat then lasts between 353 and 261 milliseconds and a sixteenth note between 88 and 65 ms, so every bass note has to fit into well under a tenth of a second.",
   "darkpsy": "<strong>Darkpsy runs at 150 to 200 BPM, typically 155–175 BPM.</strong> One beat then lasts between 400 and 300 milliseconds and a sixteenth note between 100 and 75 ms, which leaves more room for long, heavy bass notes than hitech or psycore.",
  },
  "kopf": ("Tempo", "One beat", "Sixteenth note"),
  "spektrum_h3": "Where it sits in the psytrance tempo range",
  "spektrum_kopf": ("Style", "Tempo", "Source"),
  "spektrum": [
   ("Full-on and progressive psytrance", "135–145 BPM", "Charles 2020"),
   ("Forest psytrance", "148–150 BPM", "Charles 2020"),
   ("Darkpsy", "150–200 BPM", "Vitos 2015, quoted in Charles 2020"),
   ("Hitech psytrance", "170–230+ BPM", "Code Chaos, studio practice since 2016"),
   ("Psycore", "from about 190 BPM (Charles 2020); 180–300+ BPM in current releases", "Charles 2020; Code Chaos"),
  ],
  "zitat_vor": {
   "psycore": "Research on psytrance culture puts psycore at the fast end of the scale. In his study of genre terms in psytrance, Christopher Charles (University of Bristol) names the fastest night-time styles:",
   "hitech-psytrance": "Research on psytrance culture places hitech at the fast end of the scale. In his study of genre terms in psytrance, Christopher Charles (University of Bristol) groups dark psytrance, forest, hi-tech and psycore as",
   "darkpsy": "One of the first academic descriptions of the genre comes from Botond Vitos, who describes quality darkpsy as layered, distorted sound with",
  },
  "zitat_nach": {
   "darkpsy": " Christopher Charles later described the production aesthetic of darkpsy as \"murky and aggressive\" and notes that the all-night sets of DJ Goa Gil helped to establish the style in the late 1990s and early 2000s.",
  },
  "laut_h3": "Measured loudness",
  "laut": {
   "psycore": "In our own measurement of <strong>553 hitech and psycore tracks</strong> the median integrated loudness is <strong>−8.3 LUFS</strong> (middle half −9.7 to −6.9 LUFS, measured after ITU-R BS.1770). A subset of 16 releases shows a median DR of 6.8 and a loudness range of 4.2 LU. Method and full tables: <a href=\"/en/psy-loudness-data/\">psytrance and hitech loudness data</a>.",
   "hitech-psytrance": "In our own measurement of <strong>553 hitech and psycore tracks</strong> the median integrated loudness is <strong>−8.3 LUFS</strong> (middle half −9.7 to −6.9 LUFS, measured after ITU-R BS.1770). Full-on and dark psytrance sit at −7.9 LUFS, so hitech is not mastered louder despite the higher tempo. Method and full tables: <a href=\"/en/psy-loudness-data/\">psytrance and hitech loudness data</a>.",
   "darkpsy": "In our own measurement, 16 full-on and dark psytrance releases have a median integrated loudness of <strong>−7.9 LUFS</strong> (middle half −8.9 to −7.6 LUFS, measured after ITU-R BS.1770), with a loudness range of 7.0 LU. For comparison: 553 hitech and psycore tracks sit at −8.3 LUFS. Method and full tables: <a href=\"/en/psy-loudness-data/\">psytrance and hitech loudness data</a>.",
  },
  "quellen_h2": "Sources",
  "quellen_intro": "Tempo ranges, descriptions and measurements on this page are based on:",
  "eigen": "Code Chaos: <a href=\"/en/psy-loudness-data/\">Psytrance and hitech loudness data</a>, own measurement of 553 hitech and psycore tracks plus 16 releases per comparison genre.",
  "praxis": "Tempo ranges without a source note come from Code Chaos studio practice since 2016.",
 },
 "de": {
  "h2": {"psycore": "Psycore-BPM in Zahlen", "hitech-psytrance": "Hitech-BPM in Zahlen", "darkpsy": "Darkpsy-BPM in Zahlen"},
  "satz": {
   "psycore": "<strong>Psycore läuft mit 180 bis über 300 BPM, meist 190–240 BPM.</strong> Ein Schlag dauert dann zwischen 333 und 200 Millisekunden, eine Sechzehntelnote zwischen 83 und 50 ms. Deshalb müssen Kick und Bass extrem kurz sein.",
   "hitech-psytrance": "<strong>Hitech Psytrance läuft mit 170 bis über 230 BPM, meist 180–200 BPM.</strong> Ein Schlag dauert dann zwischen 353 und 261 Millisekunden, eine Sechzehntelnote zwischen 88 und 65 ms. Jede Bassnote muss also in deutlich weniger als eine Zehntelsekunde passen.",
   "darkpsy": "<strong>Darkpsy läuft mit 150 bis 200 BPM, meist 155–175 BPM.</strong> Ein Schlag dauert dann zwischen 400 und 300 Millisekunden, eine Sechzehntelnote zwischen 100 und 75 ms. Das lässt mehr Platz für lange, schwere Bassnoten als bei Hitech oder Psycore.",
  },
  "kopf": ("Tempo", "Ein Schlag", "Sechzehntelnote"),
  "spektrum_h3": "Einordnung im Tempo-Spektrum des Psytrance",
  "spektrum_kopf": ("Stil", "Tempo", "Quelle"),
  "spektrum": [
   ("Full-on und Progressive Psytrance", "135–145 BPM", "Charles 2020"),
   ("Forest Psytrance", "148–150 BPM", "Charles 2020"),
   ("Darkpsy", "150–200 BPM", "Vitos 2015, zitiert in Charles 2020"),
   ("Hitech Psytrance", "170–230+ BPM", "Code Chaos, Studiopraxis seit 2016"),
   ("Psycore", "ab etwa 190 BPM (Charles 2020); 180–300+ BPM in aktuellen Releases", "Charles 2020; Code Chaos"),
  ],
  "zitat_vor": {
   "psycore": "Die Forschung zur Psytrance-Kultur ordnet Psycore am schnellen Ende der Skala ein. Christopher Charles (University of Bristol) nennt in seiner Studie über Genre-Begriffe im Psytrance die schnellsten Stile für die Nacht (englisches Original):",
   "hitech-psytrance": "Die Forschung zur Psytrance-Kultur ordnet Hitech am schnellen Ende der Skala ein. Christopher Charles (University of Bristol) fasst in seiner Studie über Genre-Begriffe im Psytrance Dark Psytrance, Forest, Hi-Tech und Psycore so zusammen (englisches Original):",
   "darkpsy": "Eine der ersten wissenschaftlichen Beschreibungen des Genres stammt von Botond Vitos. Er beschreibt guten Darkpsy als geschichteten, verzerrten Klang mit (englisches Original):",
  },
  "zitat_nach": {
   "psycore": " Sinngemäß: Hi-Tech und Psycore, wobei Psycore Tempi ab 190 BPM aufwärts erreicht.",
   "hitech-psytrance": " Sinngemäß: sehr schnelle, intensive Genres, die für die Nacht gedacht sind.",
   "darkpsy": " Sinngemäß: ein Grundtempo von über 150 BPM. Christopher Charles beschreibt die Produktionsästhetik von Darkpsy später als „murky and aggressive“ (düster und aggressiv) und hält fest, dass die nächtelangen Sets von DJ Goa Gil den Stil Ende der 1990er und Anfang der 2000er mitgeprägt haben.",
  },
  "laut_h3": "Gemessene Lautheit",
  "laut": {
   "psycore": "In unserer eigenen Messung von <strong>553 Hitech- und Psycore-Tracks</strong> liegt die integrierte Lautheit im Median bei <strong>−8,3 LUFS</strong> (mittlere Hälfte −9,7 bis −6,9 LUFS, gemessen nach ITU-R BS.1770). Eine Teilmenge von 16 Releases zeigt im Median DR 6,8 und einen Lautheitsumfang von 4,2 LU. Methode und alle Tabellen: <a href=\"/psy-lautheit-daten/\">Lautheitsdaten für Psytrance und Hitech</a>.",
   "hitech-psytrance": "In unserer eigenen Messung von <strong>553 Hitech- und Psycore-Tracks</strong> liegt die integrierte Lautheit im Median bei <strong>−8,3 LUFS</strong> (mittlere Hälfte −9,7 bis −6,9 LUFS, gemessen nach ITU-R BS.1770). Full-on und Dark Psytrance liegen bei −7,9 LUFS. Hitech wird also trotz des höheren Tempos nicht lauter gemastert. Methode und alle Tabellen: <a href=\"/psy-lautheit-daten/\">Lautheitsdaten für Psytrance und Hitech</a>.",
   "darkpsy": "In unserer eigenen Messung liegen 16 Full-on- und Dark-Psytrance-Releases im Median bei <strong>−7,9 LUFS</strong> integrierter Lautheit (mittlere Hälfte −8,9 bis −7,6 LUFS, gemessen nach ITU-R BS.1770), bei einem Lautheitsumfang von 7,0 LU. Zum Vergleich: 553 Hitech- und Psycore-Tracks liegen bei −8,3 LUFS. Methode und alle Tabellen: <a href=\"/psy-lautheit-daten/\">Lautheitsdaten für Psytrance und Hitech</a>.",
  },
  "quellen_h2": "Quellen",
  "quellen_intro": "Tempo-Angaben, Beschreibungen und Messwerte auf dieser Seite stützen sich auf:",
  "eigen": "Code Chaos: <a href=\"/psy-lautheit-daten/\">Lautheitsdaten für Psytrance und Hitech</a>, eigene Messung von 553 Hitech- und Psycore-Tracks sowie 16 Releases je Vergleichsgenre.",
  "praxis": "Tempo-Angaben ohne Quellenhinweis stammen aus der Studiopraxis von Code Chaos seit 2016.",
 },
}


def _ms(wert, lang):
    """Millisekunden: ganze Zahl, nur bei genau ,5 mit einer Nachkommastelle (62,5 ms)."""
    s = f"{wert:.1f}" if abs(wert % 1 - 0.5) < 1e-9 else f"{round(wert)}"
    return (s.replace(".", ",") if lang == "de" else s) + " ms"


def quellen(slug):
    """Quellen der Seite in fester Reihenfolge (für Liste und JSON-LD)."""
    return [CHARLES, VITOS, ITU]


def _zitat(slug, lang):
    t = T[lang]
    text, q = ZITAT[slug]
    auf, zu = ("„", "“") if lang == "de" else ("“", "”")
    return (f'<p>{t["zitat_vor"][slug]}</p>\n'
            f'<blockquote cite="{q["url"]}"><p lang="en">{auf}{text}{zu}</p>'
            f'<footer>{q["autor"]}, <cite><a href="{q["url"]}" rel="noopener">{q["titel"]}</a></cite>, {q["quelle"]}, {q["jahr"]}</footer></blockquote>\n'
            + (f'<p>{t["zitat_nach"][slug].strip()}</p>\n' if t["zitat_nach"].get(slug) else ""))


def zahlen_html(slug, lang):
    """Abschnitt direkt unter der Steckbrief-Tabelle: Antwortsatz mit Zahl, Rechentabelle, Tempo-Spektrum mit Quellen, Zitat, Messwerte."""
    t = T[lang]
    zeilen = "".join(f'<tr><th scope="row">{b} BPM</th><td>{_ms(60000 / b, lang)}</td><td>{_ms(15000 / b, lang)}</td></tr>' for b in TEMPI[slug])
    spektrum = "".join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in t["spektrum"])
    k, sk = t["kopf"], t["spektrum_kopf"]
    return f"""<section aria-labelledby="zahlen-t">
  <div class="wrap narrow prose">
    <h2 id="zahlen-t">{t['h2'][slug]}</h2>
    <p>{t['satz'][slug]}</p>
    <div class="table-scroll"><table class="cmp"><thead><tr><th>{k[0]}</th><th>{k[1]}</th><th>{k[2]}</th></tr></thead><tbody>{zeilen}</tbody></table></div>
    <h3>{t['spektrum_h3']}</h3>
    <div class="table-scroll"><table class="cmp"><thead><tr><th>{sk[0]}</th><th>{sk[1]}</th><th>{sk[2]}</th></tr></thead><tbody>{spektrum}</tbody></table></div>
    {_zitat(slug, lang)}    <h3>{t['laut_h3']}</h3>
    <p>{t['laut'][slug]}</p>
  </div>
</section>
"""


def quellen_html(slug, lang):
    """Quellenliste am Ende des Fließtexts (innerhalb .prose)."""
    t = T[lang]
    lis = "".join(f'<li>{q["autor"]} ({q["jahr"]}): <a href="{q["url"]}" rel="noopener">{q["titel"]}</a>. {q["quelle"]}.</li>' for q in quellen(slug))
    return (f'<h2>{t["quellen_h2"]}</h2>\n<p>{t["quellen_intro"]}</p>\n<ol>{lis}<li>{t["eigen"]}</li></ol>\n<p>{t["praxis"]}</p>')


def quellen_ld(slug):
    """schema.org citation für das Article-Objekt."""
    out = []
    for q in quellen(slug):
        art = "ScholarlyArticle" if q is not ITU else "CreativeWork"
        out.append({"@type": art, "name": q["titel"], "author": {"@type": "Organization" if q is ITU else "Person", "name": q["autor"]},
                    "datePublished": str(q["jahr"]), "url": q["url"]})
    return out
