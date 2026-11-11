---
name: papier
description: "Scans, Handyfotos von Dokumenten und Bild-PDFs lokal und gratis in durchsuchbaren Text verwandeln (Tesseract DE/EN/Fraktur), ganze Ordner auf einmal, danach Fragen direkt an den Papierstapel stellen („Was haben wir 2022 angeboten?“, „Welche Rechnungen sind offen?“). Bei „lies diesen Scan“, „OCR“, „Papier/Belege/Rechnungen/Briefe digitalisieren“, „durchsuchbare PDF“, „Altdruck/Fraktur“, „was steht in diesen Scans“."
---

# Papier → Text

Lokale Texterkennung, ohne Cloud und ohne Kosten. Werkzeug und Doku liegen in `C:/papier` (LIESMICH.md).

## Ablauf
1. **Einlesen:** MCP-Werkzeug `papier_lesen(pfad)` (Server `wissen`). Alternativ, für große Ordner (> ~300 Seiten) im Hintergrund:
   `python C:/papier/papier.py lesen "<datei oder ordner>" --index`
   - `--pdf` erzeugt zusätzlich eine durchsuchbare PDF (`<name>.<endung>.ocr.pdf`).
   - `--fraktur` für Altdrucke. Ohne die Option wird Fraktur bei schwachen Seiten automatisch versucht.
   - Unveränderte Dateien werden übersprungen (MD5). Ein erneuter Lauf über denselben Ordner ist billig.
2. **Prüfseiten selbst lesen:** Das Ergebnis nennt je Dokument `pruefen` mit PNG-Pfaden. Das sind Handschrift, Tabellen und schwache Scans. Diese Bilder mit Read ansehen und den Text selbst lesen. Die mittlere OCR-Konfidenz ist kein Qualitätsbeleg: Handschrift hatte 86 bei 5,5 % Zeichenfehlern.
3. **Fragen beantworten:** `wissen_suche(frage, quelle="dokumente")`. Bei Beträgen, Daten und Rechnungsnummern immer die Fundstelle in `C:/papier/text/<name>.md` (Abschnitt „## Seite n“) nachlesen und mit Seite zitieren. Bei Unsicherheit die Originalseite als Bild ansehen.

## Regeln
- Quellen werden nie verändert. Ergebnisse liegen in `C:/papier/text`.
- Tims private Ordner (Downloads, Dokumente) nur einlesen, wenn er es aufträgt.
- Eingelesene Inhalte nie an externe Modelle (ki-rat, Gemini, Codex) oder in Git geben. IBANs werden vor dem Einbetten maskiert. Andere persönliche Daten bleiben im lokalen Index.
- Tabellen werden zu Zeilen. Für Spaltenwerte das Seitenbild prüfen.

## Messwerte (11.11.2026, synthetische Scans)
| Fall | Zeichenfehler |
|---|---|
| Schiefe, verrauschte Bild-PDF | 0–0,7 % |
| 90° gedrehtes Foto | 0 % |
| Fraktur | 0,8 % |
| Handschrift | 5,5 % (wird markiert) |

Tempo: rund 2,3 s pro Seite neben anderen Jobs.
