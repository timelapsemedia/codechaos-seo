---
name: code-chaos-toolkit
description: Tims eigene Code-Chaos-Audio-Werkzeuge in jeder Hitech-/Psycore-/Darkpsy-Produktion, jedem Remix und jeder Produktionsassistenz aktiv einsetzen. Dazu gehören die Plugins Hoarfell, das Gitarren-Instrument, Gravesaw, Rimehall, Shardstep, Chaos FM, Crucible und Kick/Bass Scope, die Vital-/Serum-Bänke, die Kits, MIDI und das Ableton-Template. Außerdem Black-Metal-Parts in Hitech-Tracks bauen, z. B. Tremolo-Gitarren, Blast-Breaks oder kalte Chöre. Nutzen bei "Hitech Remix", "Hitech produzieren", "Produktionsassistent", "Track bauen", "Arrangement", "Sounddesign", "mach Black-Metal-Parts dazu", "Gitarre rein", "mit unseren Plugins".
---

# Code Chaos Toolkit in Produktionen

Tims Wunsch vom 20.10.2026: Alles, was im Store gebaut wird, soll auch in seinen eigenen Hitech-Remix- und Produktionsassistenz-Sessions zum Einsatz kommen. Black-Metal-Parts sind ausdrücklich erwünscht. Der Clean/Crunch- und der Akustik-Klang von Hoarfell gefallen ihm.

## Wo das gilt
Gemeint sind Tims lokale Claude-Code-Sessions auf dem PC (Desktop-App, Ableton): „Ableton Hitech Psytrance Production“ und „Ableton Hitech Psytrance Remix-Session“. Dort entstanden „Uhrwerk aus Blut“ sowie „Wiedergänger“ Vol. 1 und Vol. 2.
- **Erst ab dem 20.10.2026 und nur für neue Tracks und Remixe.** „Uhrwerk aus Blut“ und „Wiedergänger“ Vol. 1/2 sind fertig und liegen beim Vertrieb. Diese Tracks nicht anfassen und ihnen keine Parts nachträglich vorschlagen, außer Tim fragt ausdrücklich danach.
- Bei neuen Tracks Black-Metal-Parts anbieten. Tempo und Tonart aus dem Ableton-Set lesen, nicht raten.
- Ablauf, Messungen und Gates jeder Produktion regelt der Skill `hitech-produktionsstandard` (Kyrie v41). Dieser Skill hier sagt nur, welche eigenen Werkzeuge hineingehören.

## Welche Werkzeuge es gibt (vor dem Einsatz prüfen)
Was live ist, steht in `timelapsemedia/codechaos-store` → `research/state.json` (`history`). Produktseiten liegen in `products/<slug>/`, Plugin-Quellen in `plugins/<slug>/`. Stand Oktober 2026:

| Werkzeug | Einsatz im Hitech-Track |
|---|---|
| **Gitarren-Instrument** (eigener Name, siehe state.json) und **Hoarfell** (Drums/Bass/Atmos) | Gitarre (E, Steel, Nylon, eingebauter Amp), Bass, Drums, Chor/Orgel/Pad/Glocke |
| **Gravesaw** | Amp + Box für Gitarren- und Bass-DI; auch als Verzerrer für Synth-Leads |
| **Rimehall** | kalter Hall, Shimmer, Tape für Breaks, Intros, Pads |
| **Shardstep** | Stutter/Glitch, 16-Step-Pattern, für 200+ BPM gebaut: Fills auf Takt 4/8, Leads und Loops |
| **Chaos FM** (Repo chaos-fm) | 3-OP-FM für Hitech-Leads, Zaps, Bässe |
| **Crucible** (Repo crucible) | 3-Band-Sättigung für Bass- und Leadbus |
| **Kick/Bass Scope** | Phasenlage von Kick und Bass prüfen |
| **Shardgate** (gratis, seit 12.11.2026) | 16-Step-Trance-Gate + Kick-Duck ohne Sidechain, Auto Gain: Kick-Lücke im Rolling Bass (Preset „Psy Bass Gap (KBBB)“), Pads/Leads zerhacken, Pump |
| Hitech FM (Vital/Serum), Hitech Arsenal Vol. 1, Psycore-Ableton-Template | Presets, Samples, Template mit „Dissect Me" |
| Black Metal Tone Kit (IRs, REAPER-Ketten inkl. Heavy Bus), Drum Kit, MIDI Grooves 2 | Box-IRs, Gitarren im lauten Psy-Mix, Blast-MIDI |

- **Auf Tims PC:** Den VST3-Ordner scannen (`C:\Program Files\Common Files\VST3`) und nur einsetzen, was dort installiert ist. Fehlt etwas, bietet man die Gumroad-Zips aus `products/<slug>/product.json` an bzw. die CI-Artefakte der Plugin-Pipeline.
- **In der Cloud:** Plugins aus dem Repo bauen und headless rendern.
  1. `bash plugins/setup.sh`
  2. `cmake -S plugins/<slug> -B plugins/<slug>/build -DCMAKE_BUILD_TYPE=Release`
  3. `cmake --build ... --target <Target>_All`
  4. MIDI per `pedalboard` rendern (`p.load_plugin(...VST3/<Name>.vst3)`, Instrument mit MIDI-Nachrichten). Effekte in Reihe schalten, z. B. Gitarre → Gravesaw → Rimehall.
- **Für Ableton:** über producer-pal bzw. die Ableton-Bridge Spuren anlegen und die Plugins laden (Windows: `PYTHONIOENCODING=utf-8`).

## Loop-Baukasten (Methode der Shardgate-Demo, Tim 12.11.2026: „Sound und Track an sich super“)
Eigene Synthese, keine Samples. Werkzeug: `codechaos-store/tools/psy_loop.py` (Python, numpy + soundfile, kein JUCE nötig; identisch mit `plugins/*/tools/TestSignal.cpp` bis auf das Hat-Rauschen, Korrelation < 1 kHz 0,9999).
- Bausteine: Kick als Sinus mit Pitch-Sweep 190 → 48 Hz (τ 18 ms) + tanh-Drive; Rolling Bass KBBB als Saw durch Tiefpass mit Cutoff-Hüllkurve pro Note (180 + 1600 Hz, τ 20 ms, „Plock“); Offbeat-Open-Hat + 1/16-Ticks; 2-OP-FM-Stab (Ratio 2, Index 3,5 → 0, τ 30 ms) als Motiv in der Skala; 20-Hz-DC-Blocker je Stem.
- Aufruf: `python3 tools/psy_loop.py --bpm 145 --bars 8 --root E --mode phrygian --out build/loops/psy145` → `_mix.wav` + Stems `_kick/_bass/_hats/_stab.wav` (24 bit) + JSON mit Kick-Länge und 1/16-Dauer. `--short-kick` bzw. ab 200 BPM endet die Kick vor dem ersten Bass.
- Einsatz in der Ableton-Session: als Skizzen-/Testbett (Stems in Ableton, Warp aus, Tempo = BPM), als Referenz für Kick/Bass-Abstimmung, als Material für Lernvideos. **Nicht** als fertiger Track-Kern ohne den Standard (`hitech-produktionsstandard`): Motive und Sounds je Track neu.
- Plugins drüber (offline, mit Host-Transport): `<Plugin>Render --process <in.wav> <out.wav> <bpm> "<presets>" <takte je preset>`; `-1` = trockener Takt (Shardgate). So entsteht ein A/B mit Preset-Wechsel je N Takte. Vorher Eingang auf ca. −9 dBFS Peak bringen (Auto Gain hebt bis +6 dB).
- A/B immer pegelgleich nachweisen (LUFS mit `ffmpeg -af ebur128` oder `mcp__audio-labor__messen`), z. B. Demo 12.11.: trocken −17,5 / Shardgate −17,4 LUFS.

## Forschung als Leitplanken (12.11.2026)
Volltext mit Quellen: `codechaos-store/research/wissen/psytrance-forschung-uebertragung-2026-11-12.md`. Kurz (belegt → für 200+ BPM abgeleitet, nicht getestet):
- 1/16 = 15000/BPM ms (75 ms @200, 60 @250, 50 @300). Ab ~150 BPM sind 1/16 Textur; ab ~220 BPM vermutlich Half-time-Puls → Akzente auf Viertel/Halbe.
- Kick-Körper vor dem ersten Bass enden lassen (< 75/60/50 ms @200/250/300), Vorwärtsmaskierung.
- Bass-Tonhöhe kommt bei kurzen Noten aus 80–300 Hz-Obertönen, nicht aus dem Sub → Filterhüllkurve/Drive pro Note; Sub-Energie in der Kick lassen (Groove ↔ Flux < 100 Hz).
- Kurze Noten nach LUFS beurteilen, nicht nach Peak (Lautheitsintegration 100–200 ms).
- Arrangement in Sekunden planen: 25-s-Build-up = ~32 Takte bei 250 BPM; Variation darf dichter kommen.
- FM-Leads: Wirkung über Helligkeit und Index-Hüllkurve pro Note; Ratio nicht-ganzzahlig = unharmonisch/metallisch (Chowning).

## Suno und andere KI-Musik (12.11.2026)
Volltext: `codechaos-store/research/wissen/suno-2026-11-12.md`. Regel: nur Ideen, Referenzen und Vorlagen für Fremdgenre-Parts (Gothic-Chöre, Black-Metal-Arrangements, Vocal-Hooks), danach mit eigenen Werkzeugen nachbauen. Kein Suno-Audio im Hitech-Kern, in Store-Produkten, Demos oder Samplepacks; nichts aus dem Free-Plan kommerziell. Suno hält > 180 BPM laut Berichten kein sauberes Tempo.

## Black-Metal-Parts in Hitech-Tracks
- **Tempo und Tonart:** Tempo und Tonart des Tracks übernehmen. Hitech läuft meist mit 180–220+ BPM und ist oft phrygisch oder moll mit b2. BPM, Skala und Takte immer nennen.
- **Tremolo-Gitarre:**
  - Hoarfell/Gitarre mit Tremolo 1/16 (bei sehr hohem Tempo 1/16T oder halbe Zeit), Double-Track L/R, danach Gravesaw High-Gain.
  - Hochpass bei 100–150 Hz, damit Kick und Rolling Bass frei bleiben.
  - Sidechain bzw. Ducking auf die Kick.
- **Blast-Break:** Hoarfell-Drums oder Drum-Kit-MIDI (Blast 1/16) über 4–8 Takte als Break oder Fill, danach zurück in den Psy-Groove. Shardstep auf dem Übergang.
- **Atmosphäre:** Choir oder Pad aus Hoarfell durch Rimehall (Frost hoch, Shimmer) in Intro, Breakdown und Outro.
- **Akustik/Clean:** Nylon-Fingerpicking oder Clean-Arpeggio als ruhiges Intro bzw. Breakdown-Kontrast.
- **Mixen:**
  - Gitarren im lauten Psy-Mix über die Heavy-Bus-Ketten aus dem Tone Kit.
  - Lautheit und True Peak mit `mcp__audio-labor__messen` messen.
  - Härte und Fizz mit dem Skill comsar (TimbreTrack) vorher/nachher prüfen.
- **Arrangement:** in Takten angeben, z. B. „Break T. 97–112: Blast + Tremolo, T. 113 Drop“.

## Lernvideos mit eigenen Plugins
Tim, 21.10.2026: Lernvideos zur Musikproduktion kommen sehr gut an. Deshalb sollen eigene Plugins dort oft vorkommen, gleichzeitig als Werbung.
- Gilt für jedes Lern- oder Erklärvideo zur Musikproduktion: Reels, Shorts, YouTube, Karussells.
  - Wo es passt, macht ein eigenes Werkzeug den gezeigten Schritt hörbar. Beispiele: Kick/Bass Scope für die Phase, Crucible für Bass-Sättigung, Shardstep für Fills, Frostfret/Gravesaw/Rimehall für Gitarre und Raum, Hoarfell für Drums, Chaos FM/Hitech FM für Leads.
  - Das Plugin wird im Schritt genannt, nicht als Werbeblock. Am Ende kommt ein weicher CTA („Gratis-Demo · Link in Bio“).
- Zusätzlich eigene Lernvideos zu allgemeinen Produktionsthemen, umgesetzt mit den eigenen Plugins. Themen sind z. B.:
  - Mixing, Mastering und Lautheit
  - Sounddesign
  - Arrangement bei 180–300 BPM
  - Black-Metal-Gitarren und Mono-Kompatibilität
- Echtes Vorher/Nachher-Audio aus dem Plugin. Zahlen werden nur genannt, wenn sie gemessen sind (audio-labor, comsar). Nichts behaupten, was das Plugin nicht kann.
- Für die Store-Posts steht das Format in ROUTINE-AUDIO.md (codechaos-store), Abschnitt „Learning videos“.

## Regeln
- Nur echte, geprüfte Werkzeuge einsetzen; nichts behaupten, was nicht gerendert oder gemessen ist.
- Keine Fremd-Samples in Produkten. In Tims eigenen Tracks gelten seine Lizenzen.
- Schwächen ehrlich nennen, z. B. dass Clean und Akustik modelliert klingen, wenn das noch zutrifft.
- Neue Store-Produkte kommen in diese Tabelle (Skill-Sync bzw. die Store-Routine aktualisiert sie).
