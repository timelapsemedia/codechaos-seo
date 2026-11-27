# Endkontrolle – Protokolle

## Fassung A (frostfall_teil-03.mp4)

# Endkontrolle FROSTFALL Teil 3 (Hauptfassung) – begründete Freigabe, 27.11.2026

videokontrolle.py (über tools/kontrolle.py), 54 Kanten, Soll-Text. Exit 1, alle Befunde geprüft:

| Befund | Prüfung | Entscheidung |
|---|---|---|
| (1. Render) 6,58 s „Zeit.“ / 9,19 s „hingeht.“ Friktion bis an die Kante | Echter Fehler: ElevenLabs-Zeilen b02/b03 endeten nach 0,4 s Rauschen mit einem kurzen lauten Ansatz (bis −2 dB), der an der Kante abgeschnitten wurde. Behoben in vo.trimmen (End-Inseln werden entfernt, Ausklang holt sie nicht zurück), FF3-Zeilen neu getrimmt, neu gebaut. Im 3. Render kein Wortende-Befund mehr. | behoben |
| 30 Fremdsilben an Kanten (u. a. „Untertitelung des ZDF“, „musik musik“, „snippet“) | `STORY_TEIL=3 kanten_gegenprobe.py frostfall A`: alle = Fragmente der laufenden Zeile oder Sprachspur still (−52 … −105 dBFS) → Whisper-Halluzination auf Bett/Blast. | frei |
| 60,07 s „Untertitelung“ angeschnitten / 59,65 s nicht im Soll | Sprachspur still (−58 dBFS), Halluzination auf dem Ausklang nach der letzten Zeile. | frei |
| Zeile b11 im Mix als „Let's begin.“ gehört | Einzelzeile vo/b11.wav und b11.mp3 (faster-whisper medium): beide „Liv will gehen.“ – Mix-Fehlhörer durch das Bett. | frei |
| „drei“/„zwölf“/„neunzehnhundertneunundsiebzig“ fehlen | Einzelzeilen b04/b19: „Seit 1979 …“, „Morgen um 3 Uhr 12 …“ – Ziffern-Normalisierung. „Bassdrum“/„Bass Drum“ Schreibweise. | frei |

Lautheit −14,0 LUFS integriert, LRA 6,5 LU, True Peak −1,6 dBTP, 1080×1920, 30 fps, 61,3 s. Kontaktbogen angesehen: Ölmalerei einheitlich, Livs rostroter Schal + halb rasiertes Haar, Rabe mit Kupferauge, b07 blankes Fell (Fantasieschrift „AASS“ ersetzt) mit Overlay EIRIK, keine Signaturen/Logos.
