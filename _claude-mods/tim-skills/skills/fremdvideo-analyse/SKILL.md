---
name: fremdvideo-analyse
description: >-
  Fremdes Video/Reel/Short per Link oder Datei analysieren (Hook, Tempo, Aufbau, Zahlen, Machart gefilmt/KI/Code, Untertitel, Musik/BPM, Stimme) und Lehren für Tims Inhalte ableiten, so nah wie rechtlich möglich (Format ja, Material/Wortlaut/Marke nie); tiefe Zerlegung mit rea-video, Blick-Review der Machart-Rezepte. Bei "schau dir das Video an", "analysiere diesen Reel", "wie wurde das gemacht", Video-Link, offene Rezept-Reviews.
---

# fremdvideo-analyse

Belegt (Sessions 03.11., 08.11. „Automatisierte Geldverdienung“, 08.11. „YouTube-Videoanalyse“):
Tim schickt Links zu fremden Videos und will wissen, was daran funktioniert und was er
übernehmen kann. In der Cloud scheitert der Abruf meist (YouTube/Instagram sperren
Rechenzentren, Login nötig). Dieser Ablauf kommt trotzdem zu einer belastbaren Analyse.
Seit 14.11.2026 gibt es dazu die Schuss-für-Schuss-Zerlegung mit **rea-video** (lokal) und
die wöchentlichen **Machart-Rezepte** aus dem Gewinner-Radar.

**Regel (Tim 14.11., ersetzt die enge Lesart „nur Machart lernen“): so nah am Vorbild wie rechtlich möglich,
„quasi 1:1, aber auf seine Marken zugeschnitten“** (passt zu „legal, aber voll ausreizen“). Format und Idee sind nicht geschützt:
- **Übernehmen (voll nutzen):** Aufbau Schuss für Schuss mit gleicher Länge je Einstellung, gleichem Schnittrhythmus und gleichen
  Beats/Timecodes; Hook-Mechanik und Satzbau des Hooks mit eigenen Worten; Kameraperspektiven, Bewegungen, Übergänge, Effekte;
  Untertitel-Stil (Position, Größe, Animation, Wortzahl je Einblendung); Dramaturgie, Länge, CTA-Muster; Musik-Rolle (Tempo,
  Drop-Position) mit eigener Musik.
- **Nie übernehmen (Werk/Marke, UWG-Herkunftstäuschung):** fremdes Bild- und Tonmaterial, Musik, Samples; wörtliche Texte,
  Skripte, Captions über kurze übliche Wendungen hinaus; erkennbare Figuren, Gesichter, Logos, Namen, Markenzeichen;
  unverwechselbare Grafiken/Illustrationen; alles, was wie vom Original-Kanal wirkt.
- **Prüfschritt je Rezept:** Spalten „übernommen (Format)“ und „ersetzt durch Tim-eigen (Inhalt)“; Grauzonen markieren und
  nicht ausliefern, bevor sie geklärt sind (nie selbst freigeben, an Tim/Leitstelle melden).
Analysen in eigenen Worten. Keine Behauptung über Inhalte, die nicht gesehen/gehört wurden.
Zahlen/Versprechen aus dem Video (Umsatz, „passives Einkommen“) als Behauptung kennzeichnen.
DRUWIDS, keinduftbaum und Mitragyna: keine Rezepte, keine Experimente (Projektende 30.11.2026).
rea-video-Befehle `remake-run`, `capsule-draft`, `assemble` nicht benutzen (bezahlte Erzeugung bzw. Nachbau).

## Ablauf

1. **Quelle beschaffen** (erste Stufe, die klappt):
   a. Lokal am PC: `yt-dlp -f "bv*[height<=720]+ba/b" -o "%(id)s.%(ext)s" <link>` plus
      `--write-auto-subs --sub-langs "de,en" --skip-download` für Untertitel.
   b. Cloud: dasselbe versuchen; bei 403/Login/„Sign in to confirm“ nicht umgehen.
   c. Sonst Tim um eins bitten: Datei/Bildschirmaufnahme hochladen, Transkript (YouTube:
      „Transkript anzeigen“) oder 3–5 Screenshots. Nur Metadaten (Titel, Beschreibung) reichen
      für eine Aussage über Hook und Verpackung, nicht über den Inhalt – dann so sagen.
2. **Messen** – schnell mit `video-werkstatt`: `analysieren` (Dauer, Format, Lautheit, Schnitte →
   Schnitte pro Minute), `standbilder` (Kontaktbogen), `transkribieren` (falls kein Untertitel).
   **Tief (lokal, ~10–25 min CPU je Kurzvideo, OCR ist der Engpass) mit rea-video**, wenn es um „wie wurde das gemacht“
   geht (gefilmt/KI/Code je Einstellung, Untertitel-Stil, Übergänge, Musik/Stimme):
   ```bash
   C:/rea-video/.venv/Scripts/rea-video.exe decompose <video> -o E:/rea-video-cache/<name> --lang en --no-stems --no-asr --no-speakers
   C:/rea-video/.venv/Scripts/rea-video.exe summary E:/rea-video-cache/<name>/breakdown.json
   ```
   Umgebung: `PYTHONUTF8=1 REA_VIDEO_MODELS=E:/rea-video-models REA_VIDEO_HOME=C:/rea-video/.home
   OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=6`; ohne Stem-Trenner keine render-Sperre nötig, vorher freien Commit prüfen (≥ 4 GB).
   Nie mit niedriger Prozesspriorität (BELOW_NORMAL) starten: auf dem ausgelasteten PC bekam rea-video damit 0 s CPU (14.11.).
   Lesen: zuerst `VIDEO.md` (≈2k Token), Details nur über die Karte darin; nie `breakdown.json` oder `report.md` ganz einlesen.
   Danach Video und jeden fremden Ton (`stems/`, `sfx/`, *.wav) löschen.
3. **Messwerte prüfen, bevor sie zählen** (Testlauf 14.11., eigenes Reel mit bekannter Wahrheit):
   - Schnitte: gut (5 von 5 echten Kanten, +1 Zusatzkante in einem Spin-Übergang); gegen `scenedetect` oder `si.messen` gegenprüfen.
   - Texte/Untertitel (OCR, Farbe, Position, Einblendart): gut.
   - Stimme ja/nein: gut.
   - **BPM: unzuverlässig** (79,5 statt 100; librosa auf dem Mix 136, auf der Musikspur 49,7 = Oktave). Nur „bestätigt“ nennen, wenn zwei Verfahren (rea-video + librosa auf dem Ton) bis auf Oktave übereinstimmen.
   - **Machart gefilmt/KI/3D/Code ohne Blick: unzuverlässig** (Stock-Realfilm als 3D/KI erkannt, Konfidenz 0,41). Immer den Blick-Review machen (Schritt 4) oder als „ungeprüft“ kennzeichnen.
4. **Blick-Review** (du bist das Bildmodell; kein externes VLM nötig, kostet nichts außer Token):
   `rea-video review <ordner>` → `review_tasks.json` lesen (nur `instructions` und je Einstellung `images.sheet`),
   die Kontaktbögen `shots/shot_XXX.jpg` ansehen (zuerst `storyboard.jpg`), in `review_answers.json` je Einstellung
   `label_probs` (z. B. live_action / ai_video / code_render / screen_capture / still_motion …), `evidence`, `description`
   und `narrative` {role: hook|context|info|proof|turn|payoff|cta|mood, point} eintragen, dann
   `rea-video apply-review <ordner> --by claude --lang en`. Unsicheres als verteilte Wahrscheinlichkeit, nicht raten.
5. **Auswerten** (Tabelle, je Punkt Zeitstempel):
   - Hook 0–1,5 s: Bild, erster Satz, Texteinblendung; Hook-Typ; wie viele der drei Schichten (Bild + Text + Ton).
   - Aufbau: Abschnitte mit Zeiten (Erzählrollen aus dem Review), wo die Auflösung kommt, Call-to-Action.
   - Tempo: Schnitte/Minute, mittlere Einstellung, Übergänge, Schnitte auf dem Beat, Sprechtempo.
   - Untertitel: Wörter je Zeile, Position, Farbe/Akzent, Einblendart.
   - Behauptungen und Zahlen: belegt / unbelegt / Werbung (Affiliate, Kurs).
   - Bauplan für Tims Marke (Code Chaos, Polished Mastering, ZeitSprung): Tabelle je Einstellung
     „übernommen (Format)“ | „ersetzt durch Tim-eigen (Inhalt)“, so konkret, dass man das Vorbild Schuss für Schuss
     nachbauen kann; Grauzonen getrennt auflisten. Nicht übernehmen: Clickbait, unbelegte Geldversprechen.
   - Evidenzstufe nennen (Skill `evidenz-basiert`): ein fremder Ausreißer ist Stufe D (Beobachtung);
     Beleg für Tims Publikum liefert erst ein A/B (`si.experimente`).
6. **Übergabe:** Für eigenes Video gleich weiter an `hook-master`, `ig-reel`/`yt-script`
   oder `code-chaos-motion`; bei Geld-Ideen an `money-diagnose`.

## Machart-Rezepte (wöchentlich, C:/social-insights)

Der Gewinner-Radar (`si/gewinner.py`, im Wochenlauf `wachstum.py`) findet Ausreißer-Shorts (≥ 3× Kanal-Median);
`si/rezepte.py` zerlegt die Top 3 je Marke mit rea-video als eigener Windows-Prozess und schreibt
`C:/social-insights/rezepte/<marke>/<id>.json|.md` (Hook, Schnitt, Struktur, Untertitel, Musik/BPM mit Gegenprüfung,
Stimme, Machart-Mix) plus den Abschnitt „Machart-Rezepte“ im Gewinner-Bericht und je Marke ein Experiment `rz-<marke>`
(status „geplant“, eine Variable mit dem größten Abstand Gewinner gegen eigene Shorts) in `experimente.json`.

Claude arbeitet nur, wenn die Python-Vorgate etwas meldet (Verbrauch schonen):
```bash
python -m si.rezepte --vorgate        # im Ordner C:/social-insights; JSON {neu, offen_review, grauzonen_offen}
```
- `offen_review` leer → nichts tun.
- Sonst je Eintrag Schritt 4 (Blick-Review) im angegebenen `ordner`, höchstens 9 Videos je Lauf, nur `storyboard.jpg`
  und die Kontaktbögen der Einstellungen mit `priority: high`. Danach einmal `python -m si.rezepte --nach-review`
  (leitet Rezepte, Experimente und Bericht neu ab).
- Jedes Rezept (`rezepte/<marke>/<id>.md`) hat den Bauplan Schuss für Schuss und ein Feld **Freigabe**. Automatisch
  erkannte Grauzonen (markante Grafik ≥ 25 %, Kanalname/Logo im Bild, Song-Verdacht, Liedtext-Hook) sperren es. Was der
  Blick zusätzlich findet (z. B. Figuren wie bekannte Filmfiguren), mit `python -m si.rezepte --grauzone <id> "<text>"`
  eintragen. Klären nur Tim bzw. die Leitstelle: `python -m si.rezepte --klaeren <id> <nr> "<Begründung>"`. Die Vorgate
  meldet `grauzonen_offen` – unter **Brauche dich** melden, gesperrte Rezepte nie an die Produktion geben.
- Ein `rz-<marke>`-Experiment nie selbst auf „aktiv“ setzen: erst, wenn die Pipeline der Marke die Variable liest
  und kein anderer Test der Marke läuft (laufend z. B. `pm-hook-w1`, `cc-hook-w1`); das ist ein Vorschlag an Tim.
