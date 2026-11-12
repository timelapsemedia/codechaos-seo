---
name: hitech-produktionsstandard
description: Pflichtablauf für jede neue Hitech-/Psycore-Produktion, jeden Satz von Album 12 und jeden Katalog-Nachzug (Wiedergänger, Grown in Rain) nach dem Standard „Kyrie v41“. Dazu gehören Lesereihenfolge, neue Stimmen-Palette bauen und messen sowie die Gates vor jeder Ausgabe. Nutzen bei „Track bauen“, „Satz produzieren“, „mit den Kyrie-Learnings überarbeiten“, „neue Stimmen/Leads“, „ist das fertig?“.
---

# Hitech-Produktionsstandard (Kyrie v41)

Tim am 04.11.2026 zu Kyrie v41: „bisher dein bester Track bei weitem … alle Learnings/Regeln von Kyrie global mit aufnehmen“.
Dieser Skill ist der **Ablauf**. Die Zahlen, Zielfenster und Rezepte stehen nur lokal auf Tims PC und werden **vor Beginn gelesen, nicht aus dem Gedächtnis angewendet**.
In einer Cloud-Session ohne `C:/hitech-lab` wird nicht produziert. Dann sagen, dass die Quellen fehlen.

## 1. Vor dem ersten Handgriff lesen (Reihenfolge)
1. `C:/hitech-lab/knowledge/produktionsstandard_kyrie_v41.md`: Kick/Bass, Drums, FM-Leads, Genre-Wechsel, Mix/Master, Gates. Jeden Abschnitt als Prüfliste für den Track nehmen.
2. `C:/hitech-lab/knowledge/referenz_korpus.md`: Genrestandard und neueste Dossiers unter `C:/hitech-lab/korpus/`.
3. `C:/hitech-lab/knowledge/gothic_essenz.md` und `geschmack_korpus.md`: Tims Handschrift, 2–3 Familien je Track einstreuen, keine Fremd-Samples.
4. `C:/hitech-lab/knowledge/fm_leadlines_tutorials.md`: nur wenn Leads neu entstehen.
5. Bei Album 12 zusätzlich `C:/hitech-lab/album12/PLAN.md`, `GENREKARTE.md` und `OFFEN.md` des Satzes (`t0x/OFFEN.md`).

Danach im Chat in 3–5 Zeilen festhalten, welche Punkte des Standards für diesen Track gelten und welche bewusst nicht. Ein Beispiel ist der Katalog-Nachzug: Material bleibt, nur Klang wird nachgezogen.

## 2. Rahmen vor jedem Job
- Ableton-Sperre: `python C:/sperren/sperre.py nimm ableton --wer <session> --dauer 4h`, am Ende `gib`. Läuft Live nicht, über `ensure_live()` (`C:/hitech-lab/bridge/client.py`) öffnen. Set nie speichern, laufendes Live nie beenden.
- Speicher und GPU: `python C:/hitech-lab/tools/speicher.py` (freier Commit ≥ 4 GB, C/D/E). Testrender nach der Messung verwerfen, nur die beste Variante je Stimme behalten.
- Abgenommene Versionen (z. B. Kyrie v41, Wiedergänger-Master) nie überschreiben. Neue Version mit eigener Nummer, nur Genanntes ändern, A/B gegen die alte.
- Regeln teilen, Material nicht: Motive, Sequenzen, Figuren und FM-Sounds sind je Track neu. `figur_gate.py` prüft das albumweit.

## 3. Neue Stimmen-Palette bauen („palette-bauen“, Bausteine aus Album 12)
Gilt für jede neue Lead-, Sequenz- oder Themenstimme. Ziel: kein Standardpreset-Klang, jeder Anschlag klingt anders, Werte im Profi-Fenster.
1. **Entwerfen:** Synth und Patch wählen (Dexed, Chaos FM, Odin 2, Vital/Serum per Zustandsdatei). Keine Ableton-Presets. Vorlage für die Klangfarben-Sequenz je Sechzehntel ist `C:/hitech-lab/album12/t02/lab/stimmen_ky.py`.
2. **Parameter auf Wirkung messen:** `python C:/hitech-lab/album12/t01/lab/probe.py <plugin> <param> <lo> <hi>` misst je Wert Schwerpunkt und Pegel einer Einzelnote. Parameter ohne messbare Wirkung nicht sequenzieren. Offline-Synths glätten Parameter, darum Je-Noten-Render mit `reset=True` (Memory `pedalboard_parameterglaettung.md`).
3. **Mit der echten Figur rendern:** `render_voice(...)` aus `C:/hitech-lab/album12/t02/lab/klanglabor.py` (Ruf/Antwort mit den Anschlägen der Partitur).
4. **Gegen Referenz-Leads messen:**
   - `python C:/hitech-lab/album12/t02/lab/stimmprofil.py <wav>`: Helligkeit, tonale Klarheit, Varianz je Anschlag, Schärfe, Pitch-Bewegung.
   - `python C:/hitech-lab/album12/t02/lab/lebendigkeit.py <wav>`: Modulationstiefe, Fluss, Schwerpunkt-Wanderung.
   - Ziel: im Profi-Zielfenster aus dem Standard (Abschnitt 3). Abstimmung automatisch über `tune_pmlead.py`.
5. **Themen und Leitmotive:** Tonhöhen-Gate (pyin ≥ 90 % der Töne erhalten). Sonst den alten tonalen Klang behalten.
6. **Im Kontext entscheiden:** alt gegen neu per `ab_stimme.py`, je 2 Aufnahmen, pegelgleich. Die Streuung von aes ist ±0,2. Der Profi-Abstand allein entscheidet nicht.
7. **Mono-fest:** Breite je Band mit `C:/hitech-lab/album12/ms_fix.py` begrenzen, kein Haas.

## 3a. Skizzen-Bett und Forschung (seit 12.11.2026)
- Für Kick/Bass-Abstimmung, schnelle Skizzen und Plugin-A/B gibt es den synthetischen Loop-Baukasten `codechaos-store/tools/psy_loop.py` (Stems, eigene Synthese, Methode der Shardgate-Demo). Details im Skill `code-chaos-toolkit`, Abschnitt „Loop-Baukasten“. Er ersetzt keine Stimmen-Palette.
- Leitplanken aus der Wahrnehmungsforschung (Tempo-Tabelle, Kick-Länge, Bass-Tonhöhe, Arrangement in Sekunden, FM-Wirkung): `codechaos-store/research/wissen/psytrance-forschung-uebertragung-2026-11-12.md`. Was dort „abgeleitet“ heißt, ist für 200+ BPM nicht getestet: messen, nicht übernehmen. Bei Widerspruch gilt der lokale Standard.

## 4. Messen statt glauben
- Kick/Bass immer K-gewichtet (LU) und **im Vollmix je Abschnitt** (`t03/fenster.py <block> <takt>`), nicht nur solo.
- Jedes Geräte-A/B (Roar, Sättigung, Master-EQ) erst auf gleiche LUFS normieren.
- Gemini-Ohr nur mit Rollentausch und nur für A/B-Kontraste. Messwerte gehen vor Gehörtem. Das Tageskontingent setzt um 09:00 zurück.
- Vor jeder Aufnahme `gates.vor_aufnahme`: Warp-Prüfung, Sätze nicht gemischt, Live spielt nicht schon.
- Messungen, die still auf einen Default fallen (Wert 0, immer gleiche Konstante), sind Ausfälle, keine Befunde. Laut abbrechen.

## 5. Vor jeder Ausgabe an Tim (Sperre)
1. Jede Verbesserungsidee sofort in `OFFEN.md` des Tracks. Ausgabe nur, wenn dort kein „- [ ]“ mehr steht.
2. `python C:/hitech-lab/album12/abgabe_gate.py <premaster.wav> <bpm> <takt0:takt1> …` muss grün sein (Exit 0). Rot heißt weiterarbeiten, nicht ausgeben.
3. Gibt es einen Release-Bau (`release_t0x.py`), dann nur bei Grün.
4. Im Bericht jede Pflichtprüfung mit Befehl und Ergebnis nennen. Übersprungenes ausdrücklich nennen und in `OFFEN.md` eintragen.
5. Zwischenstände nur als kurzer Text, nie als Mediendatei oder „Version“.

## Grenzen
- Nichts veröffentlichen oder hochladen. Release-Planung läuft über die bestehenden Pipelines und Tims Freigabe.
- Keine Fremd-Samples, keine KI-Musik im Hitech-Kern (ACE-Step höchstens für Fremdgenre-Parts, Memory `ki_musik_nur_fremdgenres.md`).
- Dieser Skill ersetzt den lokalen Standard nicht. Widerspricht er ihm, gilt die Datei unter `C:/hitech-lab/knowledge/`.
