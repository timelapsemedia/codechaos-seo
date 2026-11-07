---
name: audio-plugin-review
description: Prüfung von Audio-Plugin- und DSP-Code (JUCE, VST3, processBlock, APVTS, Echtzeit-Sicherheit, Denormals/NaN, Filterstabilität) und Diagnose von Klicks, Knacksern, DC, Aliasing, Phasen- und Latenzfehlern, z. B. Chaos FM, Crucible, BM-Suite.
---

# Audio-Plugin-Review (Bündel aus kunitoki/sonic-skills)

Ein Einstieg für fünf Prüfstufen. Lies nur die Stufe, die zur Aufgabe passt; sie verweist selbst auf ihre Datei unter `references/`.
In den Stufen heißen die anderen Stufen noch wie die Upstream-Skills (`audio-dsp-review` …): gemeint ist jeweils die gleichnamige Datei unter `stufen/`.

| Aufgabe | Stufe(n) in dieser Reihenfolge |
|---|---|
| JUCE-Plugin prüfen (AudioProcessor, APVTS, Editor) | `stufen/audio-dsp-review.md` → `stufen/audio-numerics-review.md` → `stufen/juce-review.md` |
| VST3 ohne JUCE bzw. Host-Kompatibilität, Busse, Parameter | `stufen/audio-dsp-review.md` → `stufen/vst3-review.md` |
| beliebiger DSP-Code auf dem Audio-Thread (Echtzeit) | `stufen/audio-dsp-review.md` |
| Filter, Feedback, Oszillatoren, Zahlenfehler | `stufen/audio-numerics-review.md` |
| „Es klickt/knackt/rauscht/ist still/DC/Aliasing“ | `stufen/audio-artifacts-debug.md`, danach die dort genannte Stufe |

## Tims Hinweise (lokal ergänzt, gehen vor)

- Tims Plugins: Quellen der BM-Suite unter `C:/blackmetal-suite/plugins/*/`, fertige Builds unter `C:/VST 2026/` und `C:/hitech-lab/cc_plugins_dl/` (siehe Memory `eigene_plugins_pfade`). Code-Chaos-Audio-Plugins werden auf Gumroad verkauft: Befunde vor jedem Release-Build abarbeiten.
- Befunde mit Datei:Zeile belegen. Eine Vermutung erst als Befund melden, wenn sie im Code nachgewiesen ist; Klangfehler zusätzlich messen (Offline-Render per pedalboard, `audio-labor` messen/vergleichen, Spektrogramm), statt nur aus dem Code zu schließen.
- Fixes einzeln mit A/B-Render (pegelgleich) prüfen; abgenommene Plugin-Versionen nie überschreiben, neue Builds versionieren.
- Fallen auf Tims PC: pedalboard braucht die innere DLL des VST3-Bundles; Offline-Hosts glätten Parameter (Memory `pedalboard_parameterglaettung`); JUCE-8-Fenster lassen sich per WGC nicht aufnehmen, dann gdigrab.
- Berichte an Tim auf Deutsch; Code-Bezeichner bleiben englisch.
