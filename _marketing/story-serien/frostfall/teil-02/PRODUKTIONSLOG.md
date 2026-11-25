# FROSTFALL Teil 2 – Produktionslog (laufend)

## 11.11.2026 (Routine story-serien)
- Figuren: mutter.png, pfarrer.png neu (qwen-schnell, je 0,04 $). Beide hatten Künstlersignaturen unten rechts -> lokal per OpenCV-Inpaint entfernt (Originale: C:/story-serien/figuren/v1/*_sig.png).
- Bilder: 18 Bilder im Schnellmodus (0,72 $). Geprüft in voller Größe.
  - OK: a03, a04, a08, a09, a10, a11, a13, a14, a15, a16, a18, a19.
  - Neu nötig (Originale in bilder_v1/): a01, a06, a07 (Stil warm/sepia bzw. fotografisch statt kalter Ölmalerei), a02 (Schal liegt auf dem Teller, Wollknäuel), a05 (draußen statt Küche, passt nicht zur Handlung), a12 (Tür offen mit Hand, Text sagt „abgeschlossen“; jetzt runde Eisentür passend zu a14, Vorhängeschloss).
  - Szenen a02, a05, a06, a07, a12 in skript.json präzisiert; folge.py hängt jetzt auch bei figurlosen Bildern den Serien-Stiltext an.
- Neu-Erzeugung durch Budget-Gate gesperrt (Modal 23,78 $, Rest 6,22 $ < Reserve 6 $ + 0,8 $) -> nächster Lauf ab 01.12. (`python folge.py frostfall 2 bilder` erzeugt nur die fehlenden 6).
- Noch offen: 6 Bilder, Overlays, stimme, bauen, render, kontrolle, Ablage.

## 25.11.2026 (Routine story-serien, Lauf 1)
- 6 Kaggle-Bilder vom 24.11. in voller Größe geprüft: a01, a02, a05, a06, a07, a12 ok (keine Schrift, keine Signatur, Schal rostrot, Stil kalte Ölmalerei).
- Stimme 18 Zeilen (47,0 s), spec, bauen, render: 62,1 s, 1080×1920, −13,9 LUFS, True Peak −1,5 dBTP.
- Fehler behoben: Rohmix +2,5 LUFS, loudnorm brach ab. Ursache: sound.wav (Frostfret → Gravesaw → Rimehall, spitzen-normalisiert) liegt bei −2,4 LUFS, spec setzte fest +6 dB. `tools/folge.py` misst jetzt den Sound-Moment und pegelt auf das Niveau von Teil 1 (FROSTFALL −16,6 LUFS, hier −14,2 dB).
- Endkontrolle (vk_sicher.py über kontrolle.py): Exit 1, geprüft: 27 Fremdsilben an Tonkanten → `kanten_gegenprobe.py` Exit 0 (Sprachspur still bzw. Fragment der Zeile, 0 Zeilen mit fremden Wörtern); „Leaves“/„Livs“ = Namensschreibung; 59,40 s „Er hat“ → Ausschnitt 56,3–62,1 s isoliert transkribiert (large-v3): „Die Saiten schwingen noch. Etwas hat gelernt zu spielen.“; 0,00 s „Das“ = echter Satzbeginn („Das Wasser …“).
- Kontaktbogen: a04 zeigt Liv mit vollem kurzen Haar statt halb rasiert (Kontinuität), a13 Hand warm-orange (Stilbruch). Beide neu nötig, danach bauen/render/kontrolle erneut. a04 hat der Parallel-Lauf (Session „Story-Serien …“, e010cb8f) um 08:39 nach bilder_v1 verschoben und den Prompt geändert; die Bilder liegen bei ihm.
- Caption Englisch zuerst, titel_en „The Cold“. Skript-Gate 0 Befunde, Angebots-Sperre ok (Termin 03.12.).
- NICHT produziert gesetzt: Status bleibt „frei“, bis a04/a13 ersetzt und neu gebaut sind.

## 24.11.2026 (Session Kaggle-Backend)
- a01 a02 a05 a06 a07 a12 neu auf Kaggle (Qwen-Image-Edit + Lightning 8 Schritte, 0 $).

## 25.11.2026 (Routine story-serien, Lauf 07:38 brach um 08:16 am Limit ab; Lauf 2 übernahm)
- Stimme (vo/), Bau, Render und erste Endkontrolle aus Lauf 1.
- Lauf 2: a04 in voller Größe geprüft -> Kontinuitätsfehler (Liv mit kurzen Jungenhaaren, anderes Gesicht). Szene neu: Nahaufnahme der Mutter, von Liv nur Unterarm + Schalende. Neu auf Kaggle (Schnellmodus, 203 s, 0 $), Original in bilder_v1/a04.png. Rest: Ärmelbündchen leicht unlogisch, bei 2 s Standzeit mit Push vertretbar.
- tools/folge_build.py: Cache (hoch, _m, tiefe, Parallax-Clip) prüft jetzt Zeitstempel statt nur Existenz – sonst wäre das neue a04 still durch das alte ersetzt worden.
- Sound: Frostfret -> Gravesaw -> Rimehall (Renderer frostfret_tremolo, 08.11.), Sound-Moment a17, −2,4 LUFS gemessen, auf −16,6 LUFS gesetzt.
- Render: 62,1 s, 1080×1920, −13,9 LUFS, True Peak −1,5 dBTP. Endkontrolle Exit 1, alle Befunde begründet freigegeben (E:/story-serien/frostfall/final/frostfall_teil-02_A.freigabe.md). Keine Bilder im --voll-Modus, keine Modal-Kosten.
