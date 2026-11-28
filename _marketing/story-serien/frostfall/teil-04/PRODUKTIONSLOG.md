# FROSTFALL Teil 4 – Produktionslog

Skript: Claude (27.11.2026) nach Staffelplan (Teil 4 „Die Glocke“), Hook-Variante B (Verbot/Warnung). Vorschau an die Leitstelle, ohne Einwand nach 24 h frei.

## 28.11.2026 (Routine story-serien)
- Higgsfield-Schlüsselbilder (geprüft, 0 $): b04, b06, b08, b16; b16 nutzt den Higgsfield-Clip folge_04 (Rabe am Glockenseil) als Schlüsselmoment statt wan.
- Bilder: 12 auf Kaggle (Qwen-Image-Edit + Lightning 8 Schritte, 2x T4, 3286 s, 0 $), jedes geprüft (Hände, Schrift, Signaturen in den Ecken, Kontinuität: Livs rostroter Schal + halb rasiertes Haar, Eirik jung, Ölmalerei). b09 zeigte zwei Kupferringe statt einer Glocke -> Szene präzisiert („one single large bronze church bell“), neu auf Kaggle (1. Stapel hing in der Kaggle-Warteschlange, 2. Stapel 637 s, 0 $). Altes Bild in bilder_v1/. Kein --voll.
- Overlays: b01 Schild „EIS BETRETEN / VERBOTEN“ (hand, 42/50 px, x 360, w 270; erste Fassung ragte über das Brett, verkleinert), b10 „1979“ auf dem Glockenrand (hand, 96 px, #2A2116), Untertitel b10 auf cap_y 1330.
- Sound: Rimehall (Renderer rimehall_glocke): Chaos FM „Phrygian Bell Stab“ -> Rimehall „Northern Void“ (Frost 70 %, Mix 55 %), D2 D2 A1 D2, je ein Schlag alle 1,5 s; Sound-Moment b14 auf −16,6 LUFS gemessen gezogen (−6,8 dB), Frost-Freeze + Schütteln.
- Stimme: ElevenLabs (Serienstimme aus serien.json), 16 Zeilen, 47,7 s.
- Werkzeug-Fix: folge.py spec übernahm das Feld „wan“ nicht (KeyError im Bau) -> „wan“ in die Feldliste aufgenommen.
- Render: 61,7 s, −14,0 LUFS, True Peak −1,5 dBTP, 1080×1920, 30 fps.
- KI: alle Bilder/der Clip KI-generiert -> Caption „Image created with AI / Bild mit KI erstellt.“ + Plattformflag.
