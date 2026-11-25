# Endkontrolle – Protokolle

## Fassung A (last-rave_teil-02.mp4)

# Endkontrolle LAST RAVE Teil 2 (Hauptfassung) – begründete Freigabe, 25.11.2026

videokontrolle.py (über tools/kontrolle.py), 54 Kanten, Soll-Text. Exit 1, alle Befunde geprüft:

| Befund | Prüfung | Entscheidung |
|---|---|---|
| 14 Fremdsilben an Tonkanten | `kanten_gegenprobe.py last-rave A` (STORY_TEIL=2): 39 Fenster = Fragmente der laufenden Zeile oder Sprachspur still (Halluzination auf Bett/Puls); Zeilenprüfung 0 Zeilen mit fremden Wörtern, Exit 0. | frei |
| 44,09 s „Papierkorb.“ ohne Sprengung | HF-Profil 4–11 kHz der Zeile vo/a14.wav gegen die ElevenLabs-Rohdatei a14.mp3: Verschluss −82 dB bei 1,92 s, Sprengung −51,9 dB bei 1,96 s, Ausklang −88 … −102 dB – in beiden Dateien identisch, nichts abgeschnitten; im Mix vom Bett überdeckt. | frei (Fehlalarm) |
| 21,19 s „hundertvierzig.“ fehlt | Einzelzeile vo/a06.wav (faster-whisper medium): „Kai's Herz schlägt mit 140.“ – Ziffern-Artefakt der Normalisierung, Wort vollständig gesprochen. | frei |
| (erster Render) 63,08 s Videoende „Drohne.“ Friktion bis an die Kante | Ursache: Bett lief mit −47 dBFS bis zur letzten Probe. Behoben: Ausklang in folge_build.py; Befund im zweiten Lauf weg, letzte 100 ms −80,7 dB. „Drohne.“ endet bei 62,42 s. | behoben |

Lautheit −14,1 LUFS, LRA 5,3 LU, True Peak −1,3 dBTP, 1080×1920, 30 fps, 63,1 s. Strobe nur im Sound-Moment a16, 210 BPM, jeder 2. Schlag = 1,75 Blitze/s (≤ 2). Kontaktbogen angesehen (Kais Kupfer-Kopfhörer, Tuschekonturen, keine Schrift/Logos/Signaturen; Overlays 200+, 140→143, LAST_RAVE.wav, 53.54 / 9.97).
