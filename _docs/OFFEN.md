# OFFEN – codechaos-official.de

Liegt bewusst in `_docs/` (wird von GitHub Pages nicht veröffentlicht; im Repo-Root würde Jekyll die Datei ausliefern).

## Aus Grok #66 (Website-Agentur, 11.11.2026)

- [ ] Shardstep: H2 „Tape Stop in Ableton Live, FL Studio & Co.“ – braucht Tim: In welchen Hosts wurde Shardstep tatsächlich getestet? Bisher steht nur „noch nicht in jeder DAW ausprobiert“, deshalb keine Host-Namen gesetzt.
- [ ] /mastering/: Abschnitt „Die Psytrance-Mastering-Kette: was bei 145–200 BPM zählt“ – braucht Tims echte Kette (keine erfundenen Settings).
- [x] /mastering/ + Startseite: Vorher/Nachher aus „Uhrwerk aus Blut“ (echter Pre-Master `premaster_abgenommen_3009.wav` gegen veröffentlichtes Master, Korrelation 0,99, je 16 Takte, pegelgleich −13 LUFS, Opus + AAC). Erledigt 11.11.2026 (Grok #67).
- [ ] Weitere Vorher/Nachher-Beispiele aus Runtime Terror – braucht Tim: Pre-Master-Dateien von Runtime Terror (lokal nicht gefunden; nur Uhrwerk hat einen abgenommenen Pre-Master). Wiedergänger-Pre-Master liegen vor, erscheinen aber erst am 04.12.2026, deshalb nicht verwendet.
- [x] DE-Startseite entschlackt (Grok #67, Tim-Freigabe 11.11.): Archiv → /releases/, Genre-Guide/BPM/Glossar/Sound/Netzwerk → /genre-lexikon/, FAQ → /faq/, Bio → /bio/, Impressum/Datenschutz → /impressum/ /datenschutz/; alte Anker leiten per Skript weiter.
- [ ] Produktidee Phase-Align-Plugin (Nachfolger von Kick/Bass Scope, das nur anzeigt) – Marktgröße ungemessen, Entscheidung Tim.
- [ ] Gravesaw: H2 „Black-Metal-Amp-Sim: Einstellungen für kalte Gitarren“ mit echten Preset-Werten – Werte nur aus dem Plugin (Presets auslesen), nicht erfinden.
- [x] /en/plugins/ angelegt (11.11.2026, Grok #67), hreflang DE↔EN, Sitemap.
- [ ] EN-Pendants der übrigen Plugin-Seiten (bisher nur Crucible); die EN-Übersicht verlinkt die anderen auf die DE-Seiten („page in German“).
  - Priorität laut Grok T18 (14.11., GEO-Test): zuerst Gravesaw und Frostfret auf Englisch, mit hreflang-Paar. Bei „best black metal guitar VST plugin 2026“ wird Code Chaos nicht genannt; zitiert werden SVARTRUNA, FATHOM II und Gjalla, alle mit englischen Seiten. `/en/plugins/gravesaw/` liefert 404 (Claude hat das am 14.11. geprüft).
  - [x] /en/plugins/gravesaw/ live seit 15.11.2026 (Übersetzung der DE-Fakten, hreflang-Paar, Sitemap, llms.txt). Offen: Frostfret EN.
- [ ] EN-Sammelseite „Free psytrance plugins (VST3)“: Shardgate und die Demos bündeln, mit Link auf die Kick+Bass Engine. Bei „free psytrance kick bass plugin VST3“ steht /plugins/psy-kick-bass/ nur auf Platz 4 der Linkliste, „free“ fehlt im Title (Grok T18, 14.11.).
- [x] Doppelter Title DE/EN bei /hitech-psytrance/ behoben (EN: „Hi-Tech Psytrance Explained: BPM, Sound & Guide“).
- [x] polished.media 9a: Rechtstexte auf /impressum/ /datenschutz/ /agb/ verlagert (Wortlaut 1:1), DE-Formular verlinkt /datenschutz/ (Grok #67).
- [ ] Rechtstexte beider Seiten zum 01.12.2026 auf Tims Kleingewerbe umstellen (Heart Warrior UG darf dann nicht mehr vorkommen) – braucht Tim: Name und Anschrift des Kleingewerbes.

## Aus Grok #88 (Website-Agentur, 18.11.2026)
- [x] GA4-Conversion-Events (cta_click Gumroad/Mail, form_submit, generate_lead) in js/analytics-consent.js, nur nach Einwilligung (1bf9080, im DOM der Live-Seite getestet). Auswertung BF 26.–30.11. damit möglich.
- [ ] Angebot gegen Interzone (Hamburg, 39 €/69 €, Gratis-Testmaster; selbst abgerufen 18.11.): Testmaster gratis/bezahlt oder Begründungsblock „Warum 79 €“ – Entscheidung Tim (Preis/Angebot).
- [ ] Abschnitt „Psytrance mastering service / chain“ (Autocomplete) – nur mit Tims echten Kettenangaben (#66).
- [x] Meta-Descriptions aller 6 Genre-Seiten: BPM-Spanne zuerst, ≤ 160 Zeichen (24.11.2026, Aufgabe `seo-cc-titel`). Titel auf 48–60 Zeichen gekürzt (Psycore, Darkpsy DE/EN, Hitech DE); Titel /en/hitech-psytrance/ unverändert. Ausgangswert 23.10.–20.11.: 562 Impr., 2 Klicks, Pos. ~7. Prüftag 22.12.2026. Mengen klein = Hypothese.

## Zitierbar für KI-Antworten (24.11.2026, Aufgabe `seo-geo-zitierbar`)
- [x] Genre-Seiten DE/EN: Abschnitt „BPM in Zahlen“ (Antwortsatz, Millisekunden je Schlag, Tempo-Spektrum mit Quelle, wörtliches Zitat, eigene Lautheitswerte) und Quellenliste; `citation` im Article-Schema. Quelle der Texte: `_build/genre_belege.py`. Grundlage: Aggarwal et al. 2024 (DOI 10.1145/3637528.3671900, Stufe B). Zitate am 24.11. im Volltext nachgelesen (Charles 2020, Vitos 2009, Dancecult).
- [ ] Deutsche Genre-Seiten /psycore/, /hitech-psytrance/, /darkpsy/ sind bei Google „nicht bekannt“ bzw. „gefunden, nicht indexiert“ (24.11., Sitemap ohne Fehler, 28 interne Links). Braucht Tim: in der Search Console je URL „Indexierung beantragen“. Prüftag 22.12.2026.
- [ ] AES TD1008 (Streaming-Lautheit) als weitere Quelle: Primärdokument war am 24.11. nicht abrufbar (403), deshalb nicht zitiert.

## Plattformgrenzen GitHub Pages (Grok #67)

- Cache-Control ist fest `max-age=600`, eigene Header gehen nicht; Lighthouse „cache-insight“ bleibt deshalb gelb. Abhilfe nur per Cloudflare-Proxy vor der Domain (gratis, braucht Tims DNS-Login).
- Kein echter HTTP-301 für /crucible.html; es bleibt bei meta-refresh + canonical + JS.

## Pflege

- `css/start.css` ist Quelle der Wahrheit für das CSS der Startseite; `_build/inline_css.py` (läuft am Ende von `build_pages.py`) kopiert es inline in `index.html`.
- Lighthouse sauber messen: Workflow `lighthouse` (Actions, manuell) statt auf Tims ausgelastetem PC.
