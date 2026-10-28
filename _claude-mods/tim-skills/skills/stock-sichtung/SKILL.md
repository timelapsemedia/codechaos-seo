---
name: stock-sichtung
description: Stock-, B-Roll- und Fremdmaterial vor dem Schnitt in voller Größe sichten (Rauch, Glut, Konsum-Motive, Fremdmarken, Texttafeln) und per Prüfsumme freigeben; Gate vor dem Bau.
---

# stock-sichtung

Kontaktbögen mit 150–180 px pro Bild übersehen feine Details. Belege vom 27.10.2026:

- Pexels-Clip „sunlight wooden table“ mit glimmendem Salbeibündel und Rauchfäden war erst im 100-%-Ausschnitt des fertigen DRUWIDS-Reels zu sehen. Das Reel wurde verworfen.
- Story-B-Roll mit Fremdmarke auf dem Shirt, eine Einblendung über einem Gast und eine Abspanntafel.
- Beim ARTE-Reel: eingebrannte Texttafeln und Rauch im Fremdmaterial.

Dieser Skill macht die Sichtung zur Pflicht und hält sie fest: Jeder Clip wird in voller Größe angesehen, der Befund wird mit der Prüfsumme der Datei gespeichert, und vor dem Bau prüft ein Gate, ob alle verwendeten Clips freigegeben sind.

**Wann:** bei jedem Stock-Clip (Pexels, Pixabay, Higgsfield-Ergebnis), jeder B-Roll aus Langvideos und jedem Fremdmaterial (Doku, TV), bevor er in einen Schnitt geht. Das gilt für alle Projekte. Für DRUWIDS und Mitragyna ist es Pflicht.

**Grenzen:** Das Skript arbeitet lokal mit ffmpeg/ffprobe, ohne Netz, und löscht nichts. Die Sichtung ersetzt weder das Konsum-Gate (`E:/druwids_shorts/konsum_gate.py`, gesprochener Text) noch Tims Endkontrolle (`tim_freigabe.py`) noch die Pflicht-Endkontrolle für Videos. Sie kommt davor dazu.

## Ablauf

1. **Bilder ziehen** (Standard: 5 Bilder je Clip, gleichmäßig verteilt, lange Seite bis 1920 px):
   ```bash
   python "<Ordner dieses Skills>/sichtung.py" bilder "D:/projekt/stock/clip1.mp4" "D:/projekt/stock/clip2.mp4"
   ```
   - Bei 4K-Quellen, kleinen Motiven im Bild oder DRUWIDS immer `--lupe` dazunehmen. Das liefert je Bild zusätzlich 4 Viertel-Ausschnitte in Quellauflösung, in denen Rauchfäden, Glut und Kleingedrucktes sichtbar werden.
   - Bei langen B-Roll-Strecken `--n 10` oder mehr; mindestens ein Bild alle 3 s des verwendeten Bereichs.
2. **Jedes ausgegebene PNG mit Read ansehen.** Nicht nur einen Kontaktbogen und nicht stichprobenartig. Dabei gegen die Prüfliste unten gehen.
3. **Befund festhalten:**
   ```bash
   python "<Ordner>/sichtung.py" freigabe "D:/projekt/stock/clip1.mp4" --ok --grund "Holztisch, Pilzmodell, kein Rauch/Text"
   python "<Ordner>/sichtung.py" freigabe "D:/projekt/stock/clip2.mp4" --sperre --grund "Räucherbündel glimmt ab 4 s, Rauchfäden"
   ```
   Eine Freigabe geht nur nach `bilder`, solange die Bilder noch existieren und der Clip unverändert ist (Prüfsumme). Wer einen Clip neu schneidet oder ersetzt, muss neu sichten.
4. **Gate vor dem Bau** (in Pipelines vor dem Render aufrufen, Exit 1 = abbrechen):
   ```bash
   python "<Ordner>/sichtung.py" pruefe D:/projekt/stock/*.mp4
   ```
   Ist ein Clip gesperrt, wird er ersetzt und nicht „nur kurz“ verwendet. Ein Zuschnitt um die Stelle herum gilt erst als neuer Clip (eigene Datei, eigene Sichtung).

Das Register `stock_sichtung.json` liegt im Clipordner (oder unter `--register`) und behält den Verlauf jeder Entscheidung.

## Prüfliste

**Sperre in allen Projekten:**
- eingebrannte Texte, Untertitel, Wasserzeichen, Senderlogos, Abspann- oder Werbetafeln
- Fremdmarken und Logos auf Kleidung, Verpackungen, Bildschirmen, Fahrzeugen
- erkennbare Personen, für die keine Freigabe vorliegt; Kinder
- Schnitte innerhalb des Clips (Szenenwechsel, Schwarzbild), die im Schnitt als Fehler wirken
- KI-Artefakte wie verformte Hände, schmelzende Schrift, springende Objekte

**Zusätzlich für DRUWIDS und Mitragyna** (Rechtssicherheit geht vor; im Zweifel sperren und Tim fragen):
- Rauch, Dampf, Glut, Flammen, Kerzen, Räucherbündel, Räucherschalen
- Essen, Trinken, Tassen, Teekannen, Löffel, Mörser, Sieb, Pulver, Kapseln, Waagen, Dosierungsszenen
- Pilze in Küche, Pfanne, Topf oder auf dem Teller; Hände, die etwas zum Mund führen
- medizinische Motive wie Spritze, Tabletten, Arzt oder Krankenhaus
- Superlativ- oder Vergleichs-Texte im Bild

**Hinweis statt Sperre** (im Grund vermerken): starke Farbstiche oder Belichtung, die das Shot-Matching übernehmen muss; Hochkant-Crop, der das Motiv anschneidet; Safe-Zone-Konflikte bei 9:16.

## Bei Fremdmaterial (Doku, TV, Langvideos)

- Vor der Schnittliste ein Rohbild-Raster über den ganzen verwendeten Bereich ziehen (`--n` so wählen, dass ein Bild höchstens alle 3 s fällt). Darin Texttafeln, Rauch und Filmschnitte markieren.
- Den Grade des Urhebers nicht ändern. Bekannte Fallen eines Langvideos (Zeitbereiche mit Fremdmarke, Werbetafel, Abspann) im Projekt-Memory notieren, damit spätere Läufe sie meiden.
