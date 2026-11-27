# FROSTFALL Teil 3 – Produktionslog

Skript: Tim (08.11.2026, deutsche Fassung), Hook-Variante A.

## 27.11.2026 (Routine story-serien)
- Figur eirik_jung (1979, Schlagzeuger) neu auf Kaggle (0 $); Hemd ohne Aufdruck, Markenplakette auf der Tom lokal entfernt (Original figuren/eirik_jung_vorRetusche.png).
- Bilder: 18 auf Kaggle (Qwen-Image-Edit + Lightning 8 Schritte, 2x T4, 4896 s, 0 $), jedes geprüft. b07 hatte Fantasieschrift „AASS“ auf dem Bassdrum-Fell -> neu als blankes Fell (0 $), Name als Overlay „EIRIK“ (Schrift hand, x 190 / y 740 / w 700, Größe 190, #33434E). Kein --voll.
- Sound: Hoarfell „Raw Blast Kit“ -> Rimehall „Grim Rehearsal Tape“, 200 BPM, 4 Takte Blast (Renderer hoarfell_blast); Sound-Moment b15 auf −16,6 LUFS gemessen gezogen, Frost-Freeze + Schütteln.
- Stimme: ElevenLabs (Serienstimme aus serien.json), 18 Zeilen. Werkzeug-Fix: vo.trimmen entfernt kurze laute End-Inseln der ElevenLabs-Dateien (b02/b03 wurden an der Kante abgeschnitten), Zeilen neu getrimmt.
- Länge: erst 60,6 s -> Sound-Moment 6,8 s, Pause nach „Dann Stille.“ 1,3 s -> 61,3 s.
- Render: 61,3 s, −14,0 LUFS, LRA 6,5 LU, True Peak −1,6 dBTP, 1080×1920. Endkontrolle begründet freigegeben (endkontrolle.md).
- KI: alle Bilder KI-generiert -> Caption „Image created with AI / Bild mit KI erstellt.“ + Plattformflag.
