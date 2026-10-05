# Wöchentliche SEO-Routine codechaos-official.de

Ziel: Platz 1 bei Google und Bing für die Zielbegriffe, vor allem im DACH-Raum:
**psycore, darkpsy / dark psy, hitech psy / hitech psytrance, psytrance mastering / psycore mastering, code chaos, uhrwerk aus blut, crucible plugin.**

## Ablauf (jede Woche)

1. **Messen:** `python3 _build/seo_snapshot.py`
   - schreibt `_docs/seo-history.jsonl` und vergleicht mit der Vorwoche
   - reicht dabei die Sitemap bei Google und Bing ein, meldet alle URLs bei Bing und pingt IndexNow (Bing, Yandex, Seznam, Naver, Amazon, Yep)
   - Zugang: `GSC_KEY_FILE` oder `GSC_KEY_JSON`, `BING_API_KEY` als Umgebungsvariablen. Fehlen sie, steht das im Bericht; dann den Rest trotzdem erledigen.
2. **Auswerten:**
   - Welche Seiten sind noch nicht indexiert? Mögliche Gründe: dünner Inhalt, fehlende interne Links, Duplikate.
   - Bei welchen Zielbegriffen hat sich die Position verschlechtert, wo gibt es neue Suchanfragen mit Einblendungen, aber Position > 3?
   - Welche URL rankt für welchen Begriff? Sollte bei Genre-Begriffen die Genre-Seite sein, nicht die Startseite.
3. **Verbessern (1–3 gezielte Änderungen pro Woche, nicht mehr):**
   - Titel und Description der rankenden Seite auf den Suchbegriff schärfen
   - Inhalte ergänzen, die zur Suchabsicht passen (z. B. neue FAQ aus echten Suchanfragen)
   - interne Links mit passendem Ankertext setzen
   - Performance und Technik prüfen (Playwright: keine Fehler, kein horizontales Scrollen, keine kaputten Bilder/Links)
4. **Bauen und prüfen:**
   - `python3 _build/build_pages.py` (Genre-, Mastering-, EN- und 404-Seiten)
   - `python3 _build/schema_home.py` (JSON-LD der Startseite, wenn die FAQ geändert wurde)
   - `sitemap.xml` `lastmod` aktualisieren, bei neuen Seiten auch `llms.txt`
5. **Veröffentlichen:** Branch → Pull Request → Merge in `main` (GitHub Pages deployt), danach `python3 _build/indexnow_ping.py`.
6. **Bericht:** kurze Zusammenfassung auf Deutsch: Positionen (vorher/nachher), Indexstatus, was geändert wurde, was der Nutzer selbst tun kann (z. B. Backlinks).

## Regeln

- **Keine erfundenen Fakten.** Artists, Festivals, Daten, Zitate oder Kundenstimmen nur, wenn belegt oder vom Nutzer geliefert. Unsichere Aussagen weglassen.
- **Kein Keyword-Stuffing**, keine versteckten Texte, keine Doorway-Seiten. Inhalte für Menschen schreiben.
- **Fakten konsistent halten:** Hamburg, aktiv seit 2016, Abstract Sound Design gegründet 2021, heute reines Studioprojekt ohne Bookings (früher Live-Sets: Abstract Ritual Hamburg 07/2023, Lost Signal Festival 08/2026, Live-Mitschnitt Arnsteinhöhle 04/2026), Mastering: Single 79 €, Stem 129 €, EP 349 €, Album 629 € inkl. MwSt., Zahlung per Vorkasse oder Rechnung; Crucible 1.0.0: VST3 + Standalone für Windows, 49 €, 5 Sättigungstypen.
- **Schlüssel nie committen** (`.gitignore` schützt `*service-account*.json` und `codechaos-*.json`).
- Startseite: Single „Uhrwerk aus Blut“ vorn, Mastering direkt dahinter (Entscheidung 10/2026; nach dem Release prüfen, ob Mastering nach vorn soll).
