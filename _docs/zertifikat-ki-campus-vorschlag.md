# Vorschlag: KI-Campus-Zertifikat auf der Website (Stand 28.11.2026, nicht umgesetzt)

Status: **Tim hat Code Chaos am 28.11.2026 freigegeben**, umgesetzt im Branch `feature/weiterbildung-ki-campus` (PR, Merge durch Tim). Polished folgt eventuell mit Polished Auto (Januar 2027). /bio/ ist eine handgeschriebene Seite (geo.py setzt nur Kopfzeile und Autorenkasten), /en/ entsteht aus `_build/content_en_home.py`.

## 1. Was vorliegt

| | Leistungsnachweis | Teilnahmebestätigung |
|---|---|---|
| Kurs | KI für Alle 1: Einführung in die Künstliche Intelligenz | gleich |
| Anbieter | KI-Campus (Stifterverband) mit der Heinrich-Heine-Universität Düsseldorf („KI-Campus Original“) | gleich |
| Datum | 28.11.2026 (Ausstellungsort Berlin) | 28.11.2026 |
| Umfang | Lernzeit 45 Stunden laut Zertifikat (Kursseite nennt 42 h), keine ECTS | – |
| Bedingung | mindestens 60 % der Punkte; erreicht: 61,73 % | mindestens 50 % der Inhalte aufgerufen |
| Inhalte | ML-Grundlagen, Datentypen und Datenprobleme, Python-Grundbefehle, Ethik und Recht der KI | Grundlagen KI/ML, Datenaufbereitung/-analyse/-visualisierung, Python, Ethik/Recht |
| Kursseite | https://ki-campus.org/lernangebote/kurse/ki-fuer-alle-1 (deutsch, Einstieg, kostenlos, CC BY-SA 4.0) | |

Der **Leistungsnachweis** ist der stärkere Beleg und wird gezeigt. Die Teilnahmebestätigung bleibt im Archiv.

Ablage (lokal, Originale in Downloads unverändert, SHA-256 identisch):
- `D:\Job\Bewerbungsunterlagen\Tim Borchert_Leistungsnachweis KI-Campus KI fuer Alle 1_2026-11-28.pdf`
- `D:\Job\Bewerbungsunterlagen\Tim Borchert_Teilnahmebestaetigung KI-Campus KI fuer Alle 1_2026-11-28.pdf`

## 2. Entscheidung: Code Chaos, nicht Polished

**Code Chaos (codechaos-official.de), Seite /bio/.** Das Zertifikat kommt nicht auf polished.media.

Begründung:
1. **Ein Kurszertifikat hilft, aber nur als Nebenbeleg.** In zwei randomisierten Experimenten zogen die Befragten Profile mit MOOC-Zertifikat Profilen ohne Nachweis vor, mit 61 Prozentpunkten Vorsprung. Gegen jeden klassischen Abschluss verlor das MOOC-Zertifikat aber. Rivas, Baker & Evans 2020, AERA Open, https://doi.org/10.1177/2332858420973577, **Stufe B**. Grenzen: MTurk-Befragte, fiktive Webentwickler, Stellenvergabe und kein Kauf. Folge: Das Zertifikat wird gezeigt, aber klein, auf der Autorenseite, nicht im Hero und nicht auf Produktseiten.
2. **Expertise der Quelle wirkt auf die Kaufabsicht.** Meta-Analyse über 20 Studien: Expertise, Vertrauenswürdigkeit und Ähnlichkeit der Quelle beeinflussen Glaubwürdigkeit, Informationsübernahme und Kaufabsicht. Ismagilova et al. 2020, J. Retailing and Consumer Services, https://doi.org/10.1016/j.jretconser.2019.01.005, **Stufe A**. Grenze: eWOM-Kontext (Bewertungen), nicht Anbieter-Bios. Folge: Der Beleg gehört dorthin, wo die Person hinter der Marke steht. Das ist /bio/ mit dem `#autor`-Kasten.
3. **Ein KI-Etikett kann kreative Arbeit abwerten.** Identische Bilder wurden mit der Aufschrift „AI-created“ schlechter bewertet als mit „Human-created“, und zwar bei Gefallen, Schönheit, Tiefe und Wert. Wahrgenommene Mühe und Geschichte moderieren den Effekt. Bellaiche et al. 2023, Cognitive Research, https://doi.org/10.1186/s41235-023-00499-6, **Stufe B**. In einem Werbe-Experiment wirkte die Offenlegung von KI-Beteiligung als Persuasionswissens-Hinweis und dämpfte die positive Bewertung. Duong et al. 2026, Int. J. Advertising, https://doi.org/10.1080/02650487.2026.2748259, **Stufe B**. Grenzen: Bilder und Werbung, keine Mastering-Dienstleistung. Folge: Polished verkauft Handwerk am Metal-Master. Ein KI-Abzeichen dort riskiert genau diesen Abwertungseffekt und bringt keinen Fachbeleg fürs Mastering. Bei Code Chaos geht es um Werkzeuge (Plugins, Analysen). Dort passen KI- und Python-Grundlagen inhaltlich, und das Abzeichen steht nicht neben einem Track, sondern in der Biografie.
4. **Google und E-E-A-T.** Google fragt, ob klar ist, wer Inhalte erstellt hat. Es empfiehlt Autorenangaben mit Link zu Hintergrundinformationen. E-E-A-T selbst ist laut Google **kein** direkter Rankingfaktor. Google Search Central, „Creating helpful, reliable, people-first content“, https://developers.google.com/search/docs/fundamentals/creating-helpful-content, **Stufe E** (Anbieterangabe). Folge: Die Bylines verlinken schon auf `/bio/#autor`. Das Zertifikat kommt also auf /bio/ und nicht in jeden Autorenkasten.
5. **Optional ab Januar 2027 für Polished Auto (KI-Mastering-Abo):** Dort ist KI ohnehin das Produkt, also entfällt Punkt 3. Höchstens eine Zeile „Wer steckt dahinter“ auf der Polished-Auto-Seite, und nur als A/B-Variante. **Stufe E**, unbelegt. Nicht auf den Seiten mit Polished-Handmastering.

## 3. Platzierung (gemessen am 28.11.2026 auf der Live-Seite)

| Variante | Ort | Desktop 1024×768 | Handy 390×844 | Bewertung |
|---|---|---|---|---|
| A | Seitenkopf /bio/ (erster Bildschirm) | < 1 Bildschirmhöhe | < 1 | verworfen: Der erste Bildschirm gehört der Kernidentität Musik. Ein Nebenbeleg vorne verdrängt sie (Rivas 2020: schwächer als Hauptnachweise). Hohe visuelle Komplexität senkt die Nutzungsabsicht (Crutzen et al. 2012, DOI 10.1075/is.13.3.07cru, Stufe B, siehe webdesign.md). |
| **B** | **/bio/, Ende des Bio-Texts, direkt vor `#autor`** | **2,40** (Kasten bei 1846 px von 3051) | **2,10** (Bio-Ende 1727 px, Kasten 1776 px von 3156) | **gewählt**: Diese Seite ist die Hintergrundseite, auf die Googles Byline-Empfehlung zielt. Der Block steht innerhalb der ersten 2–2,5 Bildschirmhöhen (Fessenden 2018, NN/g: 74 % Betrachtungszeit in den ersten zwei Höhen, Stufe D). |
| C | im `geo-autor`-Kasten (über `geo.py` auf allen Ratgeber-Seiten) | – | – | verworfen: Der KI-Kurs erschiene bei jedem Psy-Ratgeber, das ist fachfremd. Wer mehr will, folgt dem Byline-Link zu B. |

Englisch: Eine Zeile im Abschnitt `/en/#about` („Ten years at the extreme edge of psytrance“, 3,2 Bildschirmhöhen) mit Link auf den Block. /bio/ ist bisher nur deutsch, deshalb steht der Block dort zweisprachig mit Englisch zuerst.

## 4. Text (Englisch zuerst)

Vier Fassungen wurden mit ig-human gemessen (`detect.py`): A dritte Person 61,2 · B Ich-Form mit unbelegtem Motiv 71,2 (verworfen, weil das Motiv erfunden wäre) · C Ich-Form sachlich 65,6 · **D Ich-Form 69,4 (gewählt)**. Angebots-Gate `angebots_sperre.py --pruefe … --termin 2026-12-10`: **ok, Exit 0** für alle Fassungen. Kein Preis, kein Link auf Shop oder Buchung, keine Aufforderung.

**EN**
> **Training**
> AI fundamentals · KI-Campus / Heinrich Heine University Düsseldorf
> In November 2026 I finished the online course "KI für Alle 1: Einführung in die Künstliche Intelligenz" (AI for Everyone 1: Introduction to Artificial Intelligence) and passed it with a statement of achievement. 45 hours of machine learning basics, data prep and analysis, Python, plus the ethical and legal side of AI. I learned a lot about where AI actually stands today, and where it doesn't.
> *Statement of achievement · 45 h · November 2026*

**DE**
> **Weiterbildung**
> KI-Grundlagen · KI-Campus / Heinrich-Heine-Universität Düsseldorf
> Im November 2026 habe ich den Onlinekurs „KI für Alle 1: Einführung in die Künstliche Intelligenz“ mit Leistungsnachweis abgeschlossen. 45 Stunden: Grundlagen des maschinellen Lernens, Datenaufbereitung und -analyse, Python sowie ethische und rechtliche Fragen rund um KI. Ich habe viel darüber gelernt, was KI heute wirklich kann und was nicht.
> *Leistungsnachweis · 45 Std. · November 2026*

**/en/#about, eine Zeile:** „Latest training: AI fundamentals at KI-Campus / Heinrich Heine University Düsseldorf (statement of achievement, 45 h, 2026).“ (Link auf `/bio/#weiterbildung`)

Tim bitte bestätigen: Stimmt der letzte Satz („I learned a lot …“) für dich? Er ist deine Aussage und steht in keinem Dokument. Sonst nehmen wir Fassung C (der Satz entfällt).

Bewusst **nicht** im Text: „certified“, „zertifiziert“, „KI-Experte“ (ein 45-Stunden-Einstiegskurs ist keine Zertifizierung, Irreführungsrisiko nach § 5 UWG) sowie die Punktzahl.

## 5. Abzeichen (Badge)

- **Eigenes Text-Abzeichen im Seitenstil** (darunter das Zertifikat als Bild, siehe 7), ohne die Logos von KI-Campus und HHU und ohne das Siegel „KI-Campus Original“. Den Anbieter im Text zu nennen ist beschreibend. Fremde Logos und Siegel nur mit Erlaubnis des Rechteinhabers. Rechtlich nicht weiter geprüft: **Stufe E, unbelegt.**
- Gestaltung: schmale Karte, so breit wie der `geo-autor`-Kasten, Hintergrund `var(--deep)`, 1 px Rahmen im vorhandenen Gold `rgba(201,168,106,0.35)`, Kicker in Versalien „TRAINING · WEITERBILDUNG“ wie `.section-eyebrow`, Titel in Fließtextgröße und kein großes „KI“-Icon (Punkt 3). Meta-Zeile klein und gedämpft. Kein Bild, also kein zusätzliches Laden.

```html
<aside class="cred" id="weiterbildung" aria-label="Training / Weiterbildung">
  <p class="cred-kicker">Training · Weiterbildung</p>
  <p class="cred-titel">AI fundamentals · KI-Campus / Heinrich Heine University Düsseldorf</p>
  <p lang="en">…EN-Text…</p>
  <p lang="de">…DE-Text…</p>
  <p class="cred-meta">Statement of achievement / Leistungsnachweis · 45 h · 11/2026</p>
</aside>
```

## 6. Schema.org

`Person` hat die Eigenschaft `hasCredential` (Wertebereich `Credential`, Untertyp `EducationalOccupationalCredential`; geprüft auf schema.org/hasCredential und schema.org/Credential am 28.11.2026). Ergänzung im vorhandenen Person-Knoten `#tim-borchert` in `_build/schema_home.py`, nicht als neuer Knoten. JSON ist geparst und gültig. Nach dem Bau zusätzlich mit validator.schema.org prüfen. Google zeigt dafür kein Rich Result (Stufe E), das Markup dient der Entitätsbeschreibung.

```json
"hasCredential": {
  "@type": "EducationalOccupationalCredential",
  "@id": "https://codechaos-official.de/bio/#ki-campus-kfa1",
  "name": "KI für Alle 1: Einführung in die Künstliche Intelligenz (Leistungsnachweis)",
  "alternateName": "AI for Everyone 1: Introduction to Artificial Intelligence (statement of achievement)",
  "credentialCategory": "Leistungsnachweis Onlinekurs / statement of achievement (online course)",
  "educationalLevel": "Einstieg / beginner",
  "inLanguage": "de",
  "dateCreated": "2026-11-28",
  "timeRequired": "PT45H",
  "url": "https://ki-campus.org/lernangebote/kurse/ki-fuer-alle-1",
  "recognizedBy": [
    {"@type": "Organization", "name": "KI-Campus (Stifterverband)", "url": "https://ki-campus.org/"},
    {"@type": "CollegeOrUniversity", "name": "Heinrich-Heine-Universität Düsseldorf", "url": "https://www.hhu.de/"}
  ],
  "competencyRequired": [
    "Grundlagen der Künstlichen Intelligenz und des maschinellen Lernens",
    "Datenaufbereitung, -analyse und -visualisierung",
    "Grundlagen der Programmierung mit Python",
    "Ethische und rechtliche Aspekte der Künstlichen Intelligenz"
  ]
}
```

Dazu `knowsAbout` um `"Maschinelles Lernen (Grundlagen)"` ergänzen.

## 7. Zertifikat selbst zeigen: ja, als Bild (Tim, 28.11.2026)

Tim: „zertifikat selbst nicht hochladen? Das sieht doch gut aus...“ Deshalb wird der Leistungsnachweis als Bild gezeigt.

Datenschutz: **keine Privatanschrift, kein Geburtsdatum.** Sichtbar sind Name, Ausstellungsort Berlin (Sitz des Anbieters), Verifizierungscode/QR und die Unterschrift des KI-Campus. Diese Angaben sind dafür gemacht, vorgezeigt und überprüft zu werden. Tim, 28.11.2026: „kannst du so machen dass man die 61 prozent nicht sieht aber den rest des dokuments?“ Die Zeile „Gesamtergebnis: 61,73 % aller möglichen Punkte“ ist im Bild entfernt: Position per PDF-Textsuche ermittelt und die Fläche mit dem Hintergrundton gefüllt (#EFF5F5, Streuung des Umfelds 0, danach dunkelstes Pixel im Zeilenband = 243, also nichts übrig). Das PDF selbst wird nicht veröffentlicht. Der Satz „mindestens 60 %“ (Bestehensbedingung) bleibt sichtbar. Hinweis: Wer den Verifizierungscode auf moodle.ki-campus.org eingibt, sieht dort das Original mit Punktzahl.

Umsetzung ohne das 14-MB-PDF:
- Vorschau 240 px breit im Block: `images/weiterbildung/ki-campus-kfa1-480.webp` (38 KB) bzw. `-960.webp` für Retina (102 KB), JPG-Fallback 50 KB, `loading="lazy"`. Dadurch bleibt der erste Seitenaufbau unberührt.
- Klick öffnet `ki-campus-kfa1-1600.webp` (200 KB), voll lesbar. Gerendert mit 300 dpi aus dem PDF.
- Bildunterschrift „View certificate / Zertifikat ansehen · verifiable via KI-Campus / über KI-Campus überprüfbar“.
- Schema: `image` am Credential.
- Die Teilnahmebestätigung bleibt im Archiv. Der Leistungsnachweis ist der stärkere Beleg.

## 8. Regeln geprüft

- Angebots-Sperre Dezember: Der Block enthält kein Angebot. Gate ok (Exit 0). Er kann auch im Dezember live gehen, ohne `angebots_sperre.py` zu berühren.
- Privatanschrift: nicht betroffen (keine Anschrift im Block oder im PDF).
- Heart Warrior UG: kommt nicht vor.
- Code Chaos zweisprachig mit Englisch zuerst: erfüllt.
- Messung danach: Die Zugriffe auf /bio/ sind zu gering für ein aussagekräftiges A/B. Beobachtet werden die GSC-Impressionen für „Tim Borchert“ / „Code Chaos“ und die Klicks auf den Byline-Link (`#autor`) ab Januar. **Stufe E.**

## 9. Nächster Schritt (nach Tims OK)

Branch von main, Block in den Generator für /bio/ und die Zeile in `/en/#about`, `hasCredential` in `_build/schema_home.py`, Bau, Prüfung (validator.schema.org, Handy-Ansicht, Angebots-Gate), dann PR. Merge durch Tim.
