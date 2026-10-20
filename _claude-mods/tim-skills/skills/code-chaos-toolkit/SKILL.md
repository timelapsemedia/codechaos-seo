---
name: code-chaos-toolkit
description: Tims eigene Code-Chaos-Audio-Werkzeuge in jeder Hitech-/Psycore-/Darkpsy-Produktion, jedem Remix und jeder Produktionsassistenz aktiv einsetzen. Dazu gehören die Plugins Hoarfell, das Gitarren-Instrument, Gravesaw, Rimehall, Shardstep, Chaos FM, Crucible und Kick/Bass Scope, die Vital-/Serum-Bänke, die Kits, MIDI und das Ableton-Template. Außerdem Black-Metal-Parts in Hitech-Tracks bauen, z. B. Tremolo-Gitarren, Blast-Breaks oder kalte Chöre. Nutzen bei "Hitech Remix", "Hitech produzieren", "Produktionsassistent", "Track bauen", "Arrangement", "Sounddesign", "mach Black-Metal-Parts dazu", "Gitarre rein", "mit unseren Plugins".
---

# Code Chaos Toolkit in Produktionen

Tims Wunsch vom 20.10.2026: Alles, was im Store gebaut wird, soll auch in seinen eigenen Hitech-Remix- und Produktionsassistenz-Sessions zum Einsatz kommen. Black-Metal-Parts sind ausdrücklich erwünscht. Der Clean/Crunch- und der Akustik-Klang von Hoarfell gefallen ihm.

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
| Hitech FM (Vital/Serum), Hitech Arsenal Vol. 1, Psycore-Ableton-Template | Presets, Samples, Template mit „Dissect Me" |
| Black Metal Tone Kit (IRs, REAPER-Ketten inkl. Heavy Bus), Drum Kit, MIDI Grooves 2 | Box-IRs, Gitarren im lauten Psy-Mix, Blast-MIDI |

- **Auf Tims PC:** Den VST3-Ordner scannen (`C:\Program Files\Common Files\VST3`) und nur einsetzen, was dort installiert ist. Fehlt etwas, bietet man die Gumroad-Zips aus `products/<slug>/product.json` an bzw. die CI-Artefakte der Plugin-Pipeline.
- **In der Cloud:** Plugins aus dem Repo bauen und headless rendern.
  1. `bash plugins/setup.sh`
  2. `cmake -S plugins/<slug> -B plugins/<slug>/build -DCMAKE_BUILD_TYPE=Release`
  3. `cmake --build ... --target <Target>_All`
  4. MIDI per `pedalboard` rendern (`p.load_plugin(...VST3/<Name>.vst3)`, Instrument mit MIDI-Nachrichten). Effekte in Reihe schalten, z. B. Gitarre → Gravesaw → Rimehall.
- **Für Ableton:** über producer-pal bzw. die Ableton-Bridge Spuren anlegen und die Plugins laden (Windows: `PYTHONIOENCODING=utf-8`).

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

## Regeln
- Nur echte, geprüfte Werkzeuge einsetzen; nichts behaupten, was nicht gerendert oder gemessen ist.
- Keine Fremd-Samples in Produkten. In Tims eigenen Tracks gelten seine Lizenzen.
- Schwächen ehrlich nennen, z. B. dass Clean und Akustik modelliert klingen, wenn das noch zutrifft.
- Neue Store-Produkte kommen in diese Tabelle (Skill-Sync bzw. die Store-Routine aktualisiert sie).
