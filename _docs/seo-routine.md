# Tägliche SEO-/GEO-/Conversion-Routine codechaos-official.de

Ziel: Platz 1 bei Google und Bing für die Zielbegriffe, vor allem im DACH-Raum:
**psycore, darkpsy / dark psy, hitech psy / hitech psytrance, psytrance mastering / psycore mastering, code chaos, uhrwerk aus blut, crucible plugin.**

Beobachtet werden zusätzlich alle Begriffe in `TARGET_GROUPS` (`_build/seo_snapshot.py`, Gruppen Genre, Mastering, Crucible, Marke; ca. 39 Begriffe). Der Bericht gruppiert danach. Das Skript listet außerdem nicht verfolgte Anfragen mit ≥2 Einblendungen und Position > 3: relevante davon in `TARGET_GROUPS` aufnehmen, Rauschen (Tippfehler, fremde Begriffe) ignorieren. Mastering- und Crucible-Gruppe haben Vorrang, weil sie Umsatz bringen.

## Auftrag: Platz 1 bei allen Begriffen in `TARGET_GROUPS`, vollautomatisch

Die Routine arbeitet selbstständig und ohne Rückfrage auf dieses Ziel hin. Jeden Tag:
1. Begriffe mit dem größten Abstand zu Platz 1 und dem höchsten Geschäftswert wählen (Reihenfolge: Mastering, Crucible, Marke, Genre). Begriffe ohne Einblendungen sind Inhaltslücken: prüfen, ob es eine passende Seite gibt, die den Begriff sachlich abdeckt (Überschrift, Abschnitt, FAQ, interner Link mit Ankertext); wenn nicht, eine Seite oder einen Abschnitt für die echte Suchabsicht anlegen (keine Doorway-Seiten, nur belegbare Fakten).
2. Nicht indexierte URLs vorrangig behandeln (interne Links von indexierten Seiten, Sitemap, IndexNow, Bing/Google-Einreichung), weil ohne Indexierung kein Ranking möglich ist.
3. Pro Tag 1–2 Änderungen, 7-Tage-Sperre pro Seite, erst ab ca. 7 Tagen Messdaten Wirkung bewerten. Was belegbar hilft, ausbauen; was nicht, nach Messgrund anpassen.
4. Ein Begriff gilt als erledigt, wenn er 7 Tage lang Position 1 hat; dann nur noch beobachten.
5. Offline-Hebel, die nur der Nutzer erledigen kann (Backlinks, Discogs/MusicBrainz-Einträge, Profile), im Bericht nennen.

## Ablauf (täglich 08:52; montags mit Wochenüberblick)

1. **Messen:** `python3 _build/seo_snapshot.py`
   - schreibt `_docs/seo-history.jsonl` und vergleicht mit der Vorwoche
   - reicht dabei die Sitemap bei Google und Bing ein, meldet alle URLs bei Bing und pingt IndexNow (Bing, Yandex, Seznam, Naver, Amazon, Yep)
   - Zugang: `GSC_KEY_FILE` oder `GSC_KEY_JSON`, `BING_API_KEY` als Umgebungsvariablen. Fehlen sie, steht das im Bericht; dann den Rest trotzdem erledigen.
2. **Auswerten:**
   - Welche Seiten sind noch nicht indexiert? Mögliche Gründe: dünner Inhalt, fehlende interne Links, Duplikate.
   - Bei welchen Zielbegriffen hat sich die Position verschlechtert, wo gibt es neue Suchanfragen mit Einblendungen, aber Position > 3?
   - Welche URL rankt für welchen Begriff? Sollte bei Genre-Begriffen die Genre-Seite sein, nicht die Startseite.
3. **Verbessern (höchstens 1–2 gezielte Änderungen pro Tag; Seiten, die in den letzten 7 Tagen geändert wurden, nicht erneut umbauen):**
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
