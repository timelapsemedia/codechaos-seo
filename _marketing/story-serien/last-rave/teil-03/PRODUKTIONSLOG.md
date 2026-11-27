# LAST RAVE Teil 3 – Produktionslog

Skript: Tim (08.11.2026, deutsche Fassung), Hook-Variante A, 210 BPM.

## 25.–27.11.2026 (Routine story-serien)
- Bilder: 18 auf Kaggle (Qwen-Image-Edit + Lightning 8 Schritte, 2x T4, 0 $), jedes in voller Größe geprüft.
  - 26.11.: b07/b12 Logo-Zeichen auf den Kopfhörern, b13 Fantasieschrift auf Tasten, b09/b14/b18 Straßenzug statt Hafen -> Szenen präzisiert, neu gerechnet.
  - 27.11.: b09, b18 ok. b07 (Zeichen auf der Kopfhörerkapsel) und b12 (Logo-Fleck auf dem Laptopdeckel) nach 2 Versuchen lokal retuschiert (OpenCV, Originale in bilder_v1/*_vorRetusche.png). b13 neu als blanke Kupfertaste ohne Tastatur, b14 neu als Containerkai mit Kränen (3. Versuch, 0 $). Kein --voll (Modal-Gate zu).
- Overlays: keine nötig (Schlüsselwörter über die Untertitel).
- Sound: Chaos FM „Psycore Growl Bass“ -> Crucible (Low 6 dB/70 %, Mid 18 dB/100 %, High 14 dB/90 %), 210 BPM, E1-Rolling (3 von 4 Sechzehnteln), Takt 4 auf G1, 5,4 s (Renderer crucible_bass); Sound-Moment b14 auf −12,4 LUFS gemessen gezogen.
- Stimme: ElevenLabs (Serienstimme aus serien.json), 17 Zeilen, 48,4 s, Tempo 0,9.
- Render: 61,4 s, −13,9 LUFS, LRA 10,1 LU, True Peak −1,5 dBTP, 1080×1920, 30 fps. Endkontrolle begründet freigegeben (endkontrolle.md).
- KI: alle Bilder KI-generiert -> Caption „Image created with AI / Bild mit KI erstellt.“ + Plattformflag.
