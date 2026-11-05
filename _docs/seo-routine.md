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
   - fehlende GEO-Merkmale aus dem Abschnitt „GEO-Merkmale“ (Prüfwerkzeug `_build/geo_merkmale.py`) zentral im Generator ergänzen
   - Performance und Technik prüfen (Playwright: keine Fehler, kein horizontales Scrollen, keine kaputten Bilder/Links)
4. **Bauen und prüfen:**
   - `python3 _build/build_pages.py` (Genre-, Mastering-, EN- und 404-Seiten)
   - `python3 _build/schema_home.py` (JSON-LD der Startseite, wenn die FAQ geändert wurde)
   - `sitemap.xml` `lastmod` aktualisieren, bei neuen Seiten auch `llms.txt`
5. **Veröffentlichen:** Branch → Pull Request → Merge in `main` (GitHub Pages deployt), danach `python3 _build/indexnow_ping.py`.
6. **Bericht:** kurze Zusammenfassung auf Deutsch: Positionen (vorher/nachher), Indexstatus, was geändert wurde, was der Nutzer selbst tun kann (z. B. Backlinks).

## GEO-Merkmale (fester Arbeitsvorrat, seit 05.11.2026)

Grundlage: SISTRIX-Studie „Citation Worthiness“ vom 22.10.2026. Ausgewertet wurden 96.418 URLs aus ChatGPT, Google AI Mode und AI Overviews, jeweils zitierte gegen nicht zitierte Seiten derselben Domain. Es entscheidet also die einzelne Seite, nicht die Marke. Quelle: https://www.sistrix.de/news/geo-mythen-im-datencheck/. Die Werte sind Korrelationen, keine Kausalität.

Der Faktor gibt an, wie viel öfter eine Seite mit dem Merkmal zitiert wird. Seiten mit vielen der elf Merkmale werden etwa 2,1× so oft zitiert wie kaum optimierte.

| Prio | Merkmal | Faktor | Umsetzung |
|---|---|---|---|
| 1 | Sichtbares Inhaltsverzeichnis mit Sprungmarken | 1,7 | Kasten „Auf dieser Seite / On this page“ unter der H1, Links auf die H2-IDs |
| 2 | Article-Schema | 1,6 | Ratgeber- und Genre-Seiten bekommen `Article` mit `author`, `datePublished`, `dateModified`; Produktseiten behalten `Product`/`SoftwareApplication` (AI Overviews zitieren Produktseiten seltener, dort kein Article erzwingen) |
| 2 | Mindestens 5 klare H2 | 1,6 | Jede H2 beantwortet eine Frage |
| 3 | FAQ mit echten Fragen (FAQPage) | 1,4–1,5 | Fragen aus GSC/Bing-Suchanfragen, keine erfundenen |
| 3 | Tabelle mit Kopfzeile (`<th>`) | 1,4–1,5 | Vergleiche, Preise, technische Werte als echte Tabelle |
| 3 | Autorenbox mit Foto | 1,4 | „Tim Borchert“ mit echtem Foto, 1–2 Sätze, Link auf die Über-mich-Seite; `author` im Schema |
| 4 | Sichtbares Datum „Zuletzt aktualisiert“ | 1,3 | Aus dem Build-Datum der Seite, nur bei echter inhaltlicher Änderung erhöhen |
| 4 | Mindestens 1.000 Wörter | 1,5 | Nur mit echtem Inhalt für die Suchabsicht, nie Füllstoff |

**Kaum Wirkung:** llms.txt, eine Ziel-Wortzahl als Selbstzweck, Lesbarkeitswerte sowie Breadcrumb-, HowTo- und QAPage-Schema. Diese nicht als GEO-Hebel verkaufen.

**Ablauf:**
1. Jede Routine misst live mit dem Prüfwerkzeug, welche Seiten welche Merkmale nicht haben:
   - codechaos-official.de: `python3 _build/geo_merkmale.py https://codechaos-official.de`
   - polished.media: `python3 _tools/geo_merkmale.py https://polished.media`
2. Die fehlenden Merkmale kommen **zentral in den Generator**, nicht als Handarbeit pro Seite:
   - codechaos: `_build/build_pages.py`
   - polished: `_tools/gen*.py`
3. Reihenfolge nach Prio: zuerst Inhaltsverzeichnis, dann Article-Schema mit Autor und Datum plus Autorenbox, dann Tabellen.
4. Pro Lauf eine Merkmal-Gruppe umsetzen, bauen, live prüfen (seo-werkstatt `seite_pruefen`) und IndexNow anstoßen.
5. Wirkung frühestens nach 4–8 Wochen bewerten: KI-Zitate über den SISTRIX-AI-Index, falls verfügbar, sonst über die Grok-Aufgabe T18 (KI-Sichtbarkeit) und GSC.
6. Messstand 05.11.2026 (Prüfwerkzeug, Anzahl Seiten ohne das Merkmal):
   - **codechaos-official.de, 21 Seiten:** AUTOR 21, DATUM 18, TOC 11, ART 7, WORTE 7, TAB 1, FAQ 1.
   - **polished.media, 36 Seiten:** AUTOR 36, DATUM 35, TOC 33, ART 28, WORTE 12, TAB 10, H2 3.

## Regeln

- **Keine erfundenen Fakten.** Artists, Festivals, Daten, Zitate oder Kundenstimmen nur, wenn belegt oder vom Nutzer geliefert. Unsichere Aussagen weglassen.
- **Kein Keyword-Stuffing**, keine versteckten Texte, keine Doorway-Seiten. Inhalte für Menschen schreiben.
- **Fakten konsistent halten:** Hamburg, aktiv seit 2016, Abstract Sound Design gegründet 2021, heute reines Studioprojekt ohne Bookings (früher Live-Sets: Abstract Ritual Hamburg 07/2023, Lost Signal Festival 08/2026, Live-Mitschnitt Arnsteinhöhle 04/2026), Mastering: Single 79 €, Stem 129 €, EP 349 €, Album 629 € inkl. MwSt., Zahlung per Banküberweisung (Vorkasse oder Rechnung, kein PayPal); Crucible 1.0.0: VST3 + Standalone für Windows, 19 € (seit 10/2026, vorher 49 €), 5 Sättigungstypen.
- **Schlüssel nie committen** (`.gitignore` schützt `*service-account*.json` und `codechaos-*.json`).
- Startseite: Single „Uhrwerk aus Blut“ vorn, Mastering direkt dahinter (Entscheidung 10/2026; nach dem Release prüfen, ob Mastering nach vorn soll).
