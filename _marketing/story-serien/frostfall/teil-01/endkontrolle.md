# Endkontrolle – Protokolle

## Fassung A (frostfall_teil-01.mp4)

# Endkontrolle FROSTFALL Teil 1 (Hauptfassung) – begründete Freigabe, 08.11.2026

videokontrolle.py (über vk_sicher.py), 57 Kanten (Shot-Grenzen + Anfang/Ende jeder Sprechzeile), Soll-Text. Exit 1, alle Befunde geprüft:

| Befund | Prüfung | Entscheidung |
|---|---|---|
| 0,00 s „beginnt vermutlich mitten im Satz mit ‚Die‘“ (Lauf nach Neurender) | Die erste Sprecherzeile ist der vollständige Satz „Die Maschine startet von selbst.“ als eigene Datei ab 0,40 s; davor nur Bandmaschinen-SFX, keine Sprache (Sprachspur 0–0,4 s still). | frei (Fehlalarm) |
| 2,28 s „selbst.“ Wortende angeschnitten | Rohdatei (ElevenLabs) vs. getrimmte Zeile: nach dem Trimmpunkt nur noch HF −79,6 dB; HF-Profil zeigt s-Friktion mit weichem Ausklang, keine eigene t-Sprengung → Aussprache der Stimme, kein Schnitt. Die Zeile liegt frei im Mix (danach 0,47 s Pause). | frei |
| 12,10 s „schläft.“ Wortende angeschnitten | HF-Profil der Zeile: f-Friktion → Verschluss (−61…−88 dB) → t-Sprengung (−70 → −39 dB) vollständig in der Datei; nach Trimmpunkt −83 dB. | frei (Fehlalarm) |
| Fremdsilben an Tonkanten (39,12 / 43,11 / 43,46 / 43,58 / 50,03 / 52,56 / 53,71 / 59,61 / 59,73 / 64,89–66,90) | Die „Kanten“ sind Anfang/Ende einzeln gesetzter Sprechzeilen über Musikbett, keine Tonschnitte. Reine Sprachspur transkribiert: 53,6–59,4 s −180 dBFS (Sound-Moment, „amen“ = Chor), 49,6–50,4 −54 dBFS und 52,2–52,9 −64 dBFS (nur Ausklang von „Play“ / „nichts“), 42,7–43,9 nur „verboten.“ + „Er hat …“. Übrige = Wörter des laufenden Satzes („merkt“, „dass“, „Teil zwei morgen“). | frei |
| „Leaves“ statt „Livs“, „Frostwick“ statt „Frostvik“ | Eigennamen, Whisper-Schreibung; Aussprache korrekt. | frei |
| „Teil zwei morgen.“ fehlt gegenüber Soll | Bekanntes Ziffern-Artefakt (Whisper „Teil 2“, Normalisierung löscht Ziffern); Wörter in den Kanten-Befunden 64,9–66,9 s gehört. | frei |

Lautheit −14,2 LUFS, True Peak −1,4 dBTP, 1080×1920, 30 fps, 68,6 s.


## Fassung B (frostfall_teil-01_hook-B.mp4)

# Endkontrolle FROSTFALL Teil 1 – Hook B (Etikett) – begründete Freigabe, 08.11.2026

videokontrolle.py (vk_sicher.py), Kanten = Shot-Grenzen + Anfang/Ende jeder Sprechzeile, Soll-Text. Exit 1, 32 Befunde, geprüft:

| Befund | Prüfung | Entscheidung |
|---|---|---|
| 70,08 s „letztes Wort ‚Morgen‘ ohne Satzende“ | Letzte Zeile „Teil zwei morgen.“ vollständig, danach 1,9 s Endkarte ohne Sprache; Whisper setzt keinen Punkt. | frei (Fehlalarm) |
| 26 Fremdsilben an Tonkanten | `kanten_gegenprobe.py`: Fenster = Fragmente der überlappenden Sprechzeile oder still; Zeilenprüfung aller Sprecherzeilen: 0 fremde Wörter. Alle SFX per VAD sprachfrei. | frei |
| „Leaves“/„Frostwick“, „zwei“ fehlt | Eigennamen-Schreibung bzw. Ziffern-Artefakt (Whisper „Teil 2“). | frei |

Hook B: Etikett „NIEMALS ABSPIELEN.“ ab Frame 0 + Satz „Mein Großvater hat mir ein Band hinterlassen. Und ein Verbot.“ (Text-Ebene = Etikett, keine Untertitel im Hook-Bild).
Lautheit −14,1 LUFS, True Peak −1,4 dBTP, 70,1 s.


## Fassung C (frostfall_teil-01_hook-C.mp4)

# Endkontrolle FROSTFALL Teil 1 – Hook C (Frost + Chor vorn) – begründete Freigabe, 08.11.2026

Erster Lauf: Rimehall-Chor im Hook lag zu dicht an der Stimme. Behoben: Produktsound vorn unter der Stimme um 10 dB abgesenkt (Ducking in build.py), Ton neu kodiert (aac_mf, Limiter 4× überabgetastet).
Zweiter Lauf (Ton neu): Exit 1, 21 Befunde, geprüft:

| Befund | Prüfung | Entscheidung |
|---|---|---|
| Hook-Satz | „Wer dieses Band abspielt, verliert seine Stimme.“ ohne Anschnitt-Befund erkannt. | behoben |
| 63,10 s „ist“: Wortende angeschnitten (keine Sprengung) | HF-Profil (4–11 kHz/LF) der Mischung: s-Friktion 62,66–62,72 s (−18 dB), Verschluss 62,74–62,76 s (−50/−64 dB), t-Sprengung 62,78–62,82 s (−29 dB), Ausklang bis −75 dB bei 62,88 s. Gleiches Muster in der Zeilendatei f18 (Sprengung 1,69–1,71 s, danach −71…−95 dB). Whisper-Wortzeit liegt ~0,3 s zu spät in der Stille. Zeile f18 ist in A/B identisch und dort ohne Befund. | frei (Fehlalarm) |
| 15 Fremdsilben an Tonkanten | `kanten_gegenprobe.py` (Lauf Ton neu, Exit 0): alle 27 geprüften Kantenfenster = Fragmente der laufenden Sprechzeile bzw. still; Zeilenprüfung aller Sprecherzeilen 0 fremde Wörter. | frei |
| „Leaves“/„Frostwick“, „zwei“ fehlt | Eigennamen-Schreibung (Liv, Frostvik) bzw. Ziffern-Artefakt (Whisper „Teil 2“). | frei |

Lautheit −14,2 LUFS, True Peak −1,5 dBTP, 70,0 s.
