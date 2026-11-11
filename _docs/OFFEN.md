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
- [x] Doppelter Title DE/EN bei /hitech-psytrance/ behoben (EN: „Hi-Tech Psytrance Explained: BPM, Sound & Guide“).
- [x] polished.media 9a: Rechtstexte auf /impressum/ /datenschutz/ /agb/ verlagert (Wortlaut 1:1), DE-Formular verlinkt /datenschutz/ (Grok #67).
- [ ] Rechtstexte beider Seiten zum 01.12.2026 auf Tims Kleingewerbe umstellen (Heart Warrior UG darf dann nicht mehr vorkommen) – braucht Tim: Name und Anschrift des Kleingewerbes.

## Plattformgrenzen GitHub Pages (Grok #67)

- Cache-Control ist fest `max-age=600`, eigene Header gehen nicht; Lighthouse „cache-insight“ bleibt deshalb gelb. Abhilfe nur per Cloudflare-Proxy vor der Domain (gratis, braucht Tims DNS-Login).
- Kein echter HTTP-301 für /crucible.html; es bleibt bei meta-refresh + canonical + JS.

## Pflege

- `css/start.css` ist Quelle der Wahrheit für das CSS der Startseite; `_build/inline_css.py` (läuft am Ende von `build_pages.py`) kopiert es inline in `index.html`.
- Lighthouse sauber messen: Workflow `lighthouse` (Actions, manuell) statt auf Tims ausgelastetem PC.
