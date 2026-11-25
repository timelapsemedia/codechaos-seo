# Endkontrolle – Protokolle

## Fassung A (frostfall_teil-02.mp4)

# Endkontrolle FROSTFALL Teil 2 (Hauptfassung) – begründete Freigabe, 25.11.2026

videokontrolle.py (über tools/kontrolle.py), 54 Kanten (Shot-Grenzen + Anfang/Ende jeder Sprechzeile), Soll-Text. Exit 1, alle Befunde geprüft:

| Befund | Prüfung | Entscheidung |
|---|---|---|
| 27 Fremdsilben an Tonkanten (u. a. „untertitelung des zdf“, „gears of war“, „musik“) | `kanten_gegenprobe.py frostfall A` (STORY_TEIL=2): reine Sprachspur an jeder Stelle ±0,35 s; 12× Sprachspur still (−58 … −109 dBFS) = Whisper-Halluzination auf Musik/Atmo, 15× Fragment der laufenden Zeile; Zeilenprüfung 0 Zeilen mit fremden Wörtern, Exit 0. Die Kanten sind Anfang/Ende einzeln gesetzter Sprechzeilen, keine Tonschnitte. | frei |
| 0,86 s „Leaves“ statt „Livs“ | Einzelzeile vo/a01.wav mit faster-whisper medium: „Das Wasser in Lief's Glas gefriert, von innen.“ – Eigenname, Whisper-Schreibung, alle Wörter vollständig (wie Teil 1). | frei |
| 59,40 s „Er hat“ nicht im Soll | Einzelzeile vo/a19.wav: „Etwas hat gelernt zu spielen.“ vollständig (0,00–1,56 s); im Mix Fehlhörer über dem Musikbett. | frei |

Lautheit −13,9 LUFS, LRA 6,7 LU, True Peak −1,5 dBTP, 1080×1920, 30 fps, 62,1 s. Kontaktbogen angesehen (Kontinuität Schal, Rabe mit einem Kupferauge, Bandmaschine mit Kupferspulen; keine Schrift/Signaturen).
