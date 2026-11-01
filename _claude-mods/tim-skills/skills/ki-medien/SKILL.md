---
name: ki-medien
description: "KI-Bilder und KI-Videos über Tims Werkstatt ki-medien erzeugen (Ersatz für Higgsfield): Modellwahl, Kostendeckel, Prompt-Regeln, Prüfung, Video-Host. Vor jedem ki_bild oder ki_video laden."
---

# ki-medien

Higgsfield ist seit 28.10.2026 gekündigt. Alle KI-Bilder und -Videos für Tims eigene Projekte laufen über den MCP `ki-medien` oder gleichwertig per CLI `python C:/bildwerk/ki.py`. Dieser Skill sagt, welches Modell wann dran ist und wie das Ergebnis geprüft wird.

**Grenzen:** Jeder Bezahlaufruf läuft durch den Monatsdeckel `C:/bildwerk/deckel.json`. Den Deckel erhöht nur Tim, nie dieser Skill. Keys kommen aus `C:/Users/moonc/OneDrive/Claude-Keys/` und werden nie ausgegeben. Erzeugen heißt nicht veröffentlichen: Für Posts gelten die Pipelines mit ihren Gates.

**Nicht verwenden für:** DRUWIDS, keinduftbaum, Mitragyna und andere Heart-Warrior-Projekte. Dort bis 30.11.2026 nur echte Fotos und Stock, keine KI.

## 1. Vor dem ersten Aufruf

1. `ki_kosten` lesen. Zeigt je Anbieter Ausgaben und Deckel des laufenden Monats. Ein Deckel von 0 $ heißt: Dieser Anbieter ist gesperrt.
2. Vor Serien oder Videos den Modal-Stand prüfen und die geschätzten Kosten nennen: `modal billing summary --json`. Modal darf nur das Gratisguthaben von 30 $ im Monat verbrauchen.
3. Echtes Material zuerst prüfen. Gibt es ein passendes Foto oder eine Aufnahme, wird das verwendet oder bearbeitet, nicht neu erzeugt.

## 2. Modellwahl

Immer zuerst die Gratis-Stufe. Ein Bezahlmodell nur, wenn das Gratis-Ergebnis sichtbar nicht reicht und der Deckel es zulässt.

| Aufgabe | Zuerst | Wenn das nicht reicht | Hinweis |
|---|---|---|---|
| Bild | `qwen` (Modal, ca. 0,12 $ vom Gratisguthaben) | `muse-image`, `nanobanana2`, `nanobanana-pro` | `muse-image` sucht Web-Referenzen, gut für echte Orte und Stile |
| Bearbeiten, 1 Bild | `qwen-edit` | `nanobanana2`, `nanobanana-pro` | genau ein Eingabebild |
| Bearbeiten, mehrere Referenzen | `muse-image` oder `nanobanana2` | `nanobanana-pro` | `auto` nimmt hier `nanobanana2` und kostet |
| Video | `wan` (720p, höchstens 5 s, ohne Ton) | `veo-lite`, `veo-fast`, `veo` (4–8 s, mit Ton), `kling`, `seedance` | Formate 16:9, 9:16, 1:1 |
| Hochskalieren | `ki_hochskalieren` (Real-ESRGAN, 4×) | – | nicht für historische Belegfotos |
| Etsy-/Wand-Mockup | `python C:/bildwerk/mockup.py <kunst.png> <out.png>` | – | kein Modell fasst die Kunst an; `--liste` zeigt Szenen |

- Andere fal-Modelle laufen über `fal:<modell-id>`. Dafür gilt die vorsichtige Pauschale aus `C:/bildwerk/preise.json`.
- Die Preise in `preise.json` sind Schätzungen. Vor größerem Einsatz auf der Preisseite des Anbieters nachsehen.
- Der erste Wan-Lauf dauerte im Test 21 min, weil das Modell geladen wurde. Solche Läufe im Hintergrund starten und abwarten.

## 3. Wenn der Deckel greift

Meldung `NICHT ERZEUGT: Budget-Gate …`: Es wurde nichts erzeugt und nichts berechnet. Nicht über andere Wege umgehen.

- Reicht die Gratis-Qualität: damit weiterarbeiten.
- Reicht sie nicht: Tim den besten Weg nennen, mit Modell und Kosten, und seine Entscheidung abwarten. Blockiert das eine Routine, per Telegram fragen (`python C:/telefon/telefon.py frage`). Ein sichtbar schlechteres Ersatzmodell nicht still als gleichwertig ausliefern.

## 4. Prompt-Regeln

**Bild (qwen, nanobanana, muse-image)**
- Motiv, Licht, Kamera und Stil konkret nennen. Objekte eindeutig benennen („volles Bierglas mit Schaum“).
- Soll das Bild randlos sein, das ausdrücklich in den Prompt schreiben.
- Text im Bild exakt in Anführungszeichen und kurz halten.
- Echte Produkte, Etiketten und Logos nie neu zeichnen lassen. Aus dem echten Foto freistellen und compositen.
- Bei Bildern mit Tims Gesicht ein echtes Foto als Referenz nehmen.
- Kommerziell genutzte KI-Inhalte im Text kennzeichnen. Code Chaos: nur „Bild mit KI erstellt“.

**Video (wan, veo, kling)**
- Pro Clip eine Kamerabewegung und eine Handlung. Für Standbild-Szenen ausdrücklich „feste Kamera“ schreiben.
- Aus echtem Material: Startbild per `startbild` übergeben. Statische Bereiche danach aus dem Original zurücksetzen (`python -m zs.kifix` in `C:/zeitsprung-pipeline`, bei Personen immer `matte`).
- Wan liefert keinen Ton. Ton kommt aus Musik, SFX oder ElevenLabs, nicht aus dem Modell. Veo liefert Ton, der genauso geprüft werden muss.

## 5. Prüfen vor der Weitergabe

Jedes Ergebnis selbst ansehen, nicht nur die Erfolgsmeldung lesen.

1. **Bild:** in voller Größe mit Read öffnen. Hände, Kanten, Spiegelungen und Fremdmarken prüfen.
2. **Schrift:** Buchstabe für Buchstabe gegen den Soll-Text lesen. Bildmodelle schreiben auch bei gutem Gesamteindruck falsch.
3. **Video:** Bilder in kurzen Abständen ziehen und ansehen (`ffmpeg`, Skill `stock-sichtung`). Auf Verformung, Flackern und sich verändernde Objekte achten.
4. **Verwendung:** Clips mit Sprache im Schnitt durchlaufen die Pflicht-Endkontrolle (`C:/video-kontrolle/videokontrolle.py`). Thumbnails gehen durch den 64/150-px-Test.
5. **Belegbilder:** Historische Fotos oder Postkarten nie per KI hochrechnen. Upscaler erfinden Details.
6. **Lizenz:** Die offenen Modelle (qwen, wan, Real-ESRGAN) sind laut `ki.py` kommerziell nutzbar. Bei Veo, Kling und anderen Anbietern gelten deren Bedingungen, vor kommerzieller Nutzung nachlesen.

Fehlerhafte Ergebnisse gezielt neu erzeugen, nicht die ganze Serie. Bevorzugt mit neuem `seed` oder präziserem Prompt.

## 6. Video hosten

Instagram und Buffer holen Videos per URL.

- Polished: `tools/bank_reel.py hosten`
- Code Chaos: hostet selbst auf GitHub
- Alle anderen:
  ```bash
  python C:/bildwerk/videohost.py hochladen "<datei.mp4>" --name <marke>_<slug>.mp4 --bis <JJJJ-MM-TT>
  ```
  `--bis` ist das Ablaufdatum, Standard ist Posttermin plus 3 Tage.

## Häufige Fehler

| Fehler | Stattdessen |
|---|---|
| Gleich ein Bezahlmodell nehmen | Erst `qwen`/`wan`, Ergebnis ansehen |
| Deckel selbst erhöhen oder auf anderen Anbieter ausweichen, um ihn zu umgehen | Tim fragen |
| Produktfoto mit Etikett per KI neu erzeugen | Echtes Foto compositen |
| Open-Higgsfield-AI als Gratis-Ersatz einplanen | Ist nur eine Oberfläche für den Bezahldienst Muapi.ai; nur nach Tims OK |
| Erfolgsmeldung als Prüfung werten | Bild öffnen, Video Bild für Bild ansehen |
