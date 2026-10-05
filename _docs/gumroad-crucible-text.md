# Crucible: Prüfung des Plugins und Vorschlag für die Gumroad-Seite

Stand: 05.10.2026. Geprüft wurde `Crucible.vst3` (6,3 MB) und die Gumroad-Seite https://timberwolf688.gumroad.com/l/crucible.

## Was die Datei enthält

| Punkt | Befund |
|---|---|
| Format | VST3, Windows x64 (PE32+ DLL), gebaut mit JUCE, Build vom 11.06.2026 |
| Version / Hersteller | 1.0.0 · „Tim Borchert“ · VST3-Kategorie `Fx|Distortion` |
| Sättigungstypen | **5:** Hard Clip, Wavefolder, Tube, Diode, Tape |
| Pro Band (Low/Mid/High) | Type, Drive, Mix, Gain, Mute, Solo |
| Global | Crossover Low/Mid, Crossover Mid/High, Output Gain, Oversampling, Bypass |
| Oversampling | JUCE-2x-FIR-Stufen vorhanden; „bis 8x“ ist plausibel, die genauen Stufen ließen sich aus der Datei nicht auslesen |
| macOS / AU | Diese Datei ist **nur Windows**. Ein AU-Build wird nirgends angeboten |

## Abweichungen, die ich auf der Website korrigiert habe

- **Preis:** Die Website zeigte „$56.76“, auf Gumroad kostet Crucible **49 €**. Die 56,76 $ waren nur die US-Umrechnung inkl. Steuer. Jetzt steht überall 49 €.
- **Formate:** Die Website versprach „VST3 / AU, Windows & macOS“ und nannte Logic, das nur AU kann. Jetzt steht dort „VST3 + Standalone · Windows 10+“, passend zu den Systemanforderungen auf Gumroad.
- **Sättigungstypen:** Statt „Hard Clip, Tube, Tape and more“ stehen jetzt alle fünf Typen da.

## Was du auf Gumroad ändern solltest (kann ich nicht für dich tun)

1. **Wavefolder und Diode fehlen** in Text und Attributen. Das sind zwei der fünf Typen, also verschenktes Verkaufsargument.
2. **macOS widerspricht sich:** „INCLUDES: VST3 Plugin (Windows/macOS)“, aber die Systemanforderungen nennen nur Windows 10+. Wenn es keinen Mac-Build gibt: „(Windows/macOS)“ löschen, sonst gibt es Rückerstattungen. Wenn es ihn gibt, sag mir Bescheid, dann ergänze ich macOS wieder auf der Website.
3. **Titelbild:** Das Cover zeigt eine Mockup-Oberfläche mit dem sichtbaren Wort „Mockup“ und Reglern („Band 1/2/3 · Saturation 20 %“), die es im Plugin nicht gibt. Ein echter Screenshot der Oberfläche wirkt deutlich vertrauenswürdiger.
4. **Optik:** Das Cover ist orange/cyan, die Website gold/blutrot. Ein Cover im Website-Look (wie `images/crucible-og.jpg`) macht die Marke wiedererkennbar.
5. **Hörbeispiele / Video:** Auf Gumroad gibt es keine Audio-Demo. Ein 30–60-Sekunden-Video mit Vorher/Nachher ist der wichtigste Verkaufshebel.

## Vorschlag Gumroad-Text (Englisch, zum Einfügen)

```
SHAPE. SATURATE. DOMINATE.

Crucible is a 3-band harmonic saturation plugin built by Code Chaos for hitech psytrance, psycore and darkpsy, and it works on anything that needs weight, bite or air.

FIVE SATURATION TYPES, PER BAND
Hard Clip · Wavefolder · Tube · Diode · Tape
Pick a different character for Low, Mid and High and stack them: hard-clip the sub, fold the mids into metallic overtones, add tape air on top.

3-BAND CONTROL
Two adjustable crossovers (Low/Mid, Mid/High). Per band: Drive, Mix, Gain, Mute, Solo. Global Output Gain and Bypass.

CLEAN WHEN PUSHED
Oversampling up to 8x keeps aliasing in check even at extreme drive.

INCLUDES
- VST3 plugin (Windows 10+, 64-bit)
- Standalone application (Windows)

WORKS IN
REAPER, Ableton Live 12+, Cubase 12+, Studio One 6+, FL Studio, Bitwig and any other VST3 host.

LICENSE
Single user, perpetual. Free 1.x updates.

Built by Code Chaos Audio · https://codechaos-official.de/crucible.html
```

(„Free 1.x updates“ nur stehen lassen, wenn du das so anbieten willst.)
