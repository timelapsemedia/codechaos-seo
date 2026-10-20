---
name: motion-reels
description: 9:16 Motion-Reels im Leverage-Stil (instagram.com/leveragebiz) bauen – After-Effects-artig mit EffectCraft (headless, per Python-Plan → JSX), kinetische Blur-Captions, Riesentext hinter freigestelltem Produkt, Spin-/Zoom-Übergänge, Bewegungsunschärfe, synthetischer Phonk/Industrial-Score + SFX auf dem Beat-Raster, finaler Encode -14 LUFS. Nutzen für Produkt-/Werbe-Reels, Motion Graphics, „wie After Effects“, „wie leveragebiz“, Shop-Produktvideos aus Shopfotos.
---

# Motion-Reels (EffectCraft + Python)

Projektordner: `D:\Videos DaVinci\Motion_Reels\` – Bibliothek `motion.py` (Bild), `sound.py` (Musik/SFX),
`fertig.py` (Encode), `tonvergleich.py` (Klangbalance gegen Referenz). Beispiele: `regalia\regalia.py`, `druwids\druwids.py`.

## Werkzeug
- **EffectCraft 0.6.0** (Open-Source-AE-Klon in Rust, Apache-2.0, github.com/storytold/effectcraft), portabel in
  `C:\effectcraft\` (im PATH). MCP global registriert (`effectcraft`, headless). CLI: `effectcraft-cli script X.jsx --empty`,
  `render-frame --project P --comp C --time T`, `render --project P --comp C --out X.mov --format prores --prores hq`.
- AE-Scripting-Objektmodell (ExtendScript-artig): `app.project.items.addComp`, `importFile`, `layers.addText/addShape/addSolid`,
  `setValueAtTime`, `KeyframeEase`, Text-Animatoren, Effekte per matchName, Expressions (`wiggle`), `sourceRectAtTime`.

## Ablauf
1. Referenz analysieren: `yt-dlp` + `crv` (Keyframes/Transkript), `demucs --two-stems vocals` → Musik/SFX-Spur, Tempo/LUFS messen.
2. Assets: echte Shopfotos (`rembg i -m isnet-general-use` freistellen), Stock-B-Roll per Skill `media-apis` (Treffer ansehen!),
   echtes Logo von der Shop-Domain. Fakten NUR von der Shop-Domain, Quelle im Plan notieren.
3. Plan in Python auf dem Beat-Raster (120 BPM → Takt 2,0 s; 100 BPM → 2,4 s). Jede Szene = 1 Takt, Wortwechsel auf Schlägen.
   `TON`-Liste (Zeit, Art) parallel füllen → SFX sitzen exakt auf den Bildereignissen.
4. `python plan.py` → Kontaktbogen (Vorschau, ~30 s) prüfen; erst dann `--render` (CPU, ~2,5–3 s/Frame bei 1080×1920).
5. `--ton` → Score + SFX; mit `tonvergleich.py <ref_no_vocals.wav> ton.wav` gegen Referenz abgleichen (Ziel ±2 dB je Band).
6. `fertig.py bild.mov ton.wav ziel.mp4` → x264 crf 17, Grain per ffmpeg, -14 LUFS / -1 dBTP.
7. Echter Render ansehen (Kontaktbogen aus der MOV) – der Vorschau-Bogen zeigt kleine Details (z. B. Personen auf Bildschirmen) nicht.

## Automatik (seit 2026-10-09)
- Routine `motion-reels-nachschub` (Mo 06:30): je Marke 1 Reel/Woche (DRUWIDS Mi 13:00 über
  `E:\druwids_shorts\plan\warteschlange.json`, keinduftbaum Do 19:00 über `plan.json` + `publish_instagram.py`, Reels-fähig).
- Routine `motion-reels-musik` (Do 06:45, seit 2026-10-13): Code Chaos So 19:00 (5 Plattformen, `C:/hitech-lab/social/queue.json`)
  und Polished Sa 10:30 (IG, Bank `C:/PolishedMetalMastering/social/bank/queue`, Feld `video_url`).
- `generator.py <ordner>/brief.json [--bogen|--fertig]` baut aus einem kurzen Brief das ganze Reel (Beat-Raster, TON-Ereignisse).
  Marken: druwids, keinduftbaum, codechaos (echtes Audio über `"musik": {"bpm", "teile": [[datei, takte, von_s]]}`,
  TikTok-sicheres Layout), polished. `"marke_extra"` überschreibt Akzent/Unterzeile für ein Reel. Brief-Pfad wird absolut aufgelöst.
- EffectCraft braucht ~3 GB freien RAM; bei „memory allocation failed“ warten, keine fremden Prozesse beenden.
- **Lernschleife:** `leverage_abstand.py <reel.mp4> <marke>` misst gegen 12 Referenz-Reels (`_referenz/leveragebiz`,
  Werte in `stil/referenz.json`) und schiebt `stil/stil_<marke>.json` 35 % Richtung Referenz: Szenenlänge, Unterschnitte,
  Zoom, Produktbewegung, Bewegtbild-Anteil, Helligkeit (abdunkeln), Hintergrund-Blur, SFX-Dichte. Markengrenzen
  (DRUWIDS ruhig, kein Shake) in `MARKEN_GRENZEN`. Verlauf: `stil/verlauf.jsonl`, Rotation: `motion_log.jsonl`.
- Startabstand (Reel 1): Bewegung 3–4 vs. 16,8, Helligkeit 31–48 vs. 109, Schnitte 0,7–0,85/s vs. 2,5/s.
- Freisteller IMMER auf Spiegelung/Schatten prüfen und entfernen (Tim, 2026-10-09). Video-URL per Higgsfield
  `media_upload` + `put_upload.py` + `media_confirm` (cloudfront).
- keinduftbaum-Regeln: keine konkreten Haltbarkeitsangaben (max. „über Wochen“), kein Preis/keine URL in der Caption.

## Regie-Briefing (aus 513 viralen Opus-5.5-Code-Videos, ausgewertet 2026-10-10)
Quelle: github.com/yihui-dev/awesome-opus5-5-videos (MIT), lokal `_referenz/opus55_videos`, Suche:
`python prompt_suche.py <begriffe> [--kat motion|explainer|3d|interactive] [--tech gsap|threejs|shader|canvas] [--min 1500]`,
`--zeige <slug>`. Nur Muster übernehmen, nie fremde Inhalte oder Marken.

Die starken Produktfilm-Prompts (z. B. `daniel-haida-636937`, `brainextends-606193`, `thegrootdev-966114`, `annacher-433425`) haben dieselbe Struktur. Jede `brief.json` und jedes neue Reel daran ausrichten:

1. **Rolle und Gegenziel:** zum Beispiel „Senior Motion Designer“. Dazu klar sagen, was es NICHT sein soll (kein generisches Template, kein Feature-Walkthrough). Gewünschte Reaktion in einem Satz.
2. **Quelle der Wahrheit:** echte Marken-Assets wie Logo, Farben, Schrift und echte Produktfotos. Nichts erfinden („REAL PRODUCT ONLY“), keine erfundenen Zahlen.
3. **Raster:** BPM, Takte, Schläge. Auf jedem Schlag passiert etwas Beabsichtigtes. Wichtige Momente landen musikalisch.
4. **Kontinuität statt Schnittgewitter:** „one shape, never cut“, Match-Cuts. Formen und Produkte morphen bzw. fliegen in die nächste Szene. Das macht Motion Graphics zu echtem Bewegtbild, auch ohne Footage.
5. **Bewegungsqualität:**
   - Federn stark gedämpft, kaum Überschwingen.
   - Ein- und Austritt zeitlich getrennt, Inhalte mit kurzem Blur wechseln.
   - Kamera rahmt jede Szene neu, damit der Text groß und lesbar bleibt.
   - Keine tote Zeit.
6. **Verbotsliste:** bei Premium-Marken z. B. Partikel-Explosionen, Dauerglow, Verläufe auf UI, Zuviel-Bounce, Trailer-Boom/EDM-Riser. Für Leverage-Energie (keinduftbaum) gilt das Gegenteil, also markenspezifisch entscheiden.
7. **Ton:** synthetisch und rechtssicher, SFX auf den Bildereignissen. Effekte sind leiser als die Musik, wenn die Marke ruhig ist.
8. **Loop:** Das Ende kehrt nahtlos zum Anfangsbild zurück.
9. **Bauen, rendern, ansehen, verfeinern**, und nicht bei Storyboard oder Standbild aufhören. Mindestens eine Feedback-Runde am echten Render.

## Leverage-Signatur (gemessen 2026-10-09)
- Bild: Text ab Frame 1, Wörter mit Blur+Scale-Reveal, Akzentwort in Neonfarbe, faux-italic; Riesentext/Zahl hinter Subjekt;
  Spin-Blur-/Whip-Übergänge; Weißblitz + Zoom-Punch auf dem Drop; Schnitt alle 1–2 s.
- Ton: Bass House / Drift Phonk (Cowbell, verzerrte 808) / Industrial, 96–136 BPM; SFX 3–6 dB über Musik, auf dem Raster:
  Riser → Drop/Impact, Whoosh je Schnitt (L/R wandernd), Shutter-Klicks, Glitch, Reverse-Becken, Tape-Stop am Ende; -14 LUFS.

## EffectCraft-Fallen (0.6.0)
- Dateinamen mit Ziffer am Ende (`karte_2.png`) werden als **Bildsequenz** importiert → In-Points kaputt. `imp()` setzt
  `io.sequence=false`; trotzdem sprechende Namen ohne Endziffer verwenden.
- **Keyframes rasten auf Frames**: zwei Keys < 1 Frame auseinander kollidieren → Werte rampen über Sekunden. Mindestabstand 1/30 s.
- Transform-Effekt (`ADBE Geometry2`): Index 3 = Uniform Scale (bool), Skalierung = Index 4, Rotation 8. Radial Blur Type: 0 = Spin, 1 = Zoom.
- Exposure: `e.property(2).property(1)` (Master-Gruppe). Drop-Shadow-Opacity 0–100-artig (~60–75).
- **Noise-Effekt erzeugt Pixelmüll** → Grain im ffmpeg-Encode. Skew-Effekt dreht um Layer-Mitte → Text-Animator-Skew nutzen.
- `--gpu` war nicht schneller (identisches Bild). Parallel-Renders: ~3 GB RAM je Prozess, bei 15 GB RAM max. 1–2 gleichzeitig
  (sonst „memory allocation failed“). Teilbereiche mit `--start/--end` rendern; End-Frame ist exklusiv → fehlende Frames einzeln
  per `render-frame --frame N` nachrendern und framegenau (settb/setpts=N) einsetzen.

## Regeln
- Ohne Sprache: Pflicht-Endkontrolle entfällt (offen dazuschreiben). Mit Sprache: `videokontrolle.py` wie immer.
- DRUWIDS: Skill `druwids-social-operator` + Compliance-Gate, KI-Hinweis wenn KI-Bilder, Pflicht-Disclaimer, nur Shop-Fakten.
- Musik/SFX selbst synthetisieren (keine Lizenzfragen); ElevenLabs-Free-Tarif ist nicht kommerziell.
- Captions durch `ig-human`; Veröffentlichung nur nach Tims Freigabe.
