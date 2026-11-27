# Endkontrolle – Protokolle

## Fassung A (last-rave_teil-03.mp4)

# Endkontrolle LAST RAVE Teil 3 (Hauptfassung) – begründete Freigabe, 27.11.2026

videokontrolle.py (über tools/kontrolle.py), 51 Kanten, Soll-Text. Exit 1, alle Befunde geprüft:

| Befund | Prüfung | Entscheidung |
|---|---|---|
| 38 Fremdsilben an Kanten (u. a. „Untertitelung des ZDF“, „gut bis zum nächsten Mal“) | `STORY_TEIL=3 kanten_gegenprobe.py last-rave A`: alle = Fragmente der laufenden Zeile oder Sprachspur still (Whisper-Halluzination auf Bett/Sound-Moment); Zeilenprüfung 0 Zeilen mit fremden Wörtern, Exit 0. | frei |
| 11,16 s „erzählt.“ ohne Sprengung | HF-Profil 4–11 kHz von vo/b04.wav: Verschluss −70 dB, Sprengung −34 dB in den letzten 0,3 s vorhanden; Einzelzeile per faster-whisper medium vollständig „Kai hat niemandem davon erzählt.“; im Mix vom Bett überdeckt. | frei (Fehlalarm) |
| 31,49 s „hundertzwanzig.“ fehlt | Einzelzeile vo/b09.wav: „Viel schneller als 120.“ – Ziffern-Normalisierung, Wort gesprochen. | frei |
| 56,65 s „weh tut“ statt „wehtut“ | Schreibweise von Whisper, gleiches Wort. | frei |

Lautheit −13,9 LUFS integriert, LRA 10,1 LU, True Peak −1,5 dBTP, 1080×1920, 30 fps, 61,4 s. Kontaktbogen angesehen: Stil einheitlich (Graphic Novel, Tusche), Kais Kupfer-Kopfhörer ohne Zeichen (b07 lokal retuschiert), Laptopdeckel ohne Logo (b12 lokal retuschiert), b13 Taste ohne Schrift, b14 Containerhafen statt Straße, keine Signaturen.
