# Endkontrolle – Protokolle

## Fassung A (last-rave_teil-01.mp4)

# Endkontrolle LAST RAVE Teil 1 (Hauptfassung) – begründete Freigabe, 08.11.2026

videokontrolle.py (über vk_sicher.py), 57 Kanten (Shot-Grenzen + Anfang/Ende jeder Sprechzeile), Soll-Text. Exit 1, alle Befunde geprüft:

| Befund | Prüfung | Entscheidung |
|---|---|---|
| 0,00 / 0,30 / 60,47 / 60,59 s „Füllwort ‚Um‘“ | „Um“ ist hier Präposition und Satzanfang („Um zwei Uhr zwanzig …“, „Um sechs Uhr ist es vorbei.“), kein Füllwort. | frei (Fehlalarm) |
| 31 Fremdsilben-Befunde an Tonkanten | Kanten = Anfang/Ende einzeln gesetzter Sprechzeilen über Regen + Puls, keine Tonschnitte. Alle SFX (Regen, Radio, Knistern, Messgerät) per VAD sprachfrei; Betten/Produktsound reine Synthesizer. Reine Sprachspur: Fenster still oder Fragment der laufenden Zeile (`kanten_gegenprobe.py`). Zeilenprüfung: jede der 19 Sprecherzeilen vollständig transkribiert = Soll-Text, 0 fremde Wörter. | frei |
| „fehlt gegenüber Soll“: zwei, zwanzig, hundertzwanzig, zwanzig einundvierzig, zweihundert, siebenundachtzig, sechs | Ziffern-Artefakt (Whisper schreibt 2.20, 120, 2041, 200, 87, 6); Zeilenprüfung bestätigt die Wörter. | frei |
| „Neo Hamburg“ statt „Neo-Hamburg“ | Bindestrich-Schreibung. | frei |

Lautheit −14,0 LUFS, True Peak −1,2 dBTP, 1080×1920, 30 fps, 72,3 s. Strobe nur im BPM-Raster (halbe Zeit, ≤ 2 Blitze/s); Caption mit „⚠️ Enthält Lichtblitze.“.


## Fassung B (last-rave_teil-01_hook-B.mp4)

# Endkontrolle LAST RAVE Teil 1 – Hook B (Plakat) – begründete Freigabe, 08.11.2026

videokontrolle.py (vk_sicher.py), Kanten = Shot-Grenzen + Anfang/Ende jeder Sprechzeile, Soll-Text. Exit 1, 40 Befunde, geprüft:

| Befund | Prüfung | Entscheidung |
|---|---|---|
| 60,05 / 60,17 s „Füllwort ‚Um‘“ | Satzanfang „Um sechs Uhr ist es vorbei.“ (Präposition). | frei (Fehlalarm) |
| 30 Fremdsilben an Tonkanten | `kanten_gegenprobe.py`: Fragmente der laufenden Sprechzeile oder still; Zeilenprüfung: 0 fremde Wörter; SFX per VAD sprachfrei. | frei |
| Zahlwörter „fehlen“ (zwanzig einundvierzig, hundertzwanzig, zweihundert, siebenundachtzig, sechs), „Neo -Hamburg“ | Ziffern-Artefakt / Bindestrich-Schreibung; Zeilenprüfung bestätigt den Wortlaut. | frei |

Hook B: Plakat „MAX. 120 BPM. FÜR IHRE RUHE.“ ab Frame 0 + „In meiner Stadt ist schnelle Musik seit 2041 verboten.“
Lautheit −14,0 LUFS, True Peak −1,2 dBTP, 71,9 s. Strobe nur im BPM-Raster (≤ 2 Blitze/s).


## Fassung C (last-rave_teil-01_hook-C.mp4)

# Endkontrolle LAST RAVE Teil 1 – Hook C (FM-Lead + Strobe vorn) – begründete Freigabe, 08.11.2026

Erster Lauf: echter Befund – der FM-Lead im Hook überdeckte die Stimme („Diese“ angeschnitten, Score 0,17; „Kassel“ statt „Tanzen“).
Behoben: Produktsound vorn unter der Stimme um 10 dB abgesenkt (Ducking in build.py); Ton neu kodiert (aac_mf, Limiter 4× überabgetastet).
Zweiter Lauf (Ton neu): Exit 1, 43 Befunde, geprüft:

| Befund | Prüfung | Entscheidung |
|---|---|---|
| Hook-Satz | „Diese Frequenz bringt alle zum Tanzen. Bis zum Sonnenaufgang.“ wird jetzt korrekt erkannt, kein Anschnitt-Befund mehr. | behoben |
| 22,60 s „gehört.“ Wortende angeschnitten | Zeilendatei r05 enthält die komplette Rohaufnahme (getrimmt 2,378 s ≥ roh 2,368 s); HF-Profil: Verschluss (−53…−73 dB) → t-Sprengung (bis −21 dB) → Ausklang −82 dB. | frei (Fehlalarm) |
| 42,91 s „Niemand“ Wortende angeschnitten | Liegt mitten in der durchgehend gespielten Zeile r11 (42,50–45,66 s), kein Tonschnitt; automatisch erkannter Bildwechsel (Strobe/Puls) als „Schnitt“ gewertet. | frei (Fehlalarm) |
| 60,38 / 60,50 s „Füllwort ‚Um‘“ | Satzanfang „Um sechs Uhr ist es vorbei.“ | frei |
| 32 Fremdsilben an Tonkanten | `kanten_gegenprobe.py` (Lauf auf Ton neu, siehe rest.log) – Fragmente bzw. still; Zeilenprüfung 0 fremde Wörter. | frei |
| Zahlwörter „fehlen“, „Neo Hamburg“ | Ziffern-Artefakt / Bindestrich. | frei |

Lautheit −13,9 LUFS, True Peak −1,1 dBTP, 72,2 s. Strobe nur im BPM-Raster (≤ 2 Blitze/s); Caption mit Lichtblitz-Hinweis.
