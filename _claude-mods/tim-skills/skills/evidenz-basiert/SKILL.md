---
name: evidenz-basiert
description: "Jede Entscheidung in Marketing, Social, Video, Audio/Mastering, Musikproduktion, Webdesign und Verkaufspsychologie wissenschaftlich begründen: Studien suchen (PubMed, Scholar-Ersatz, Springer, KatalogPlus), Evidenzstufe bewerten, mit Tims eigenen A/B-Daten abgleichen, Befund ablegen. Bei Hook, Länge, Schnitt, Mix/Master, Preis, Angebot, Landingpage, Thumbnail, CTA und „warum wirkt das?“."
---

# Evidenz-basiert arbeiten

Tim, 10.11.2026: „Alles global marketing, audio, video, webdesign, mastering, verkaufspsych usw alles an wissensch ausrichten in allen sessions global“.
Ziel: Entscheidungen auf Forschung und Messung stützen, nicht auf Guru-Regeln. Ausnahmen gibt es keine; Tims ausdrückliche Regeln und die Compliance-Gates gehen trotzdem immer vor.

## Ablauf je Entscheidung (kurz halten, nicht jede Kleinigkeit)
1. **Frage präzisieren:** Was genau soll wirken (Klickrate, Watchtime, Kauf, Lautheitsempfinden, Groove …), bei welchem Publikum?
2. **Vorhandenes zuerst:** `wissen_suche` (MCP `wissen`, Quelle `wissenschaft`) und `C:/wissenschaft/<bereich>.md` lesen. Gibt es dort einen geprüften Befund, den nutzen.
3. **Literatur suchen** (MCP `literatur`): `pubmed_suche` (Wahrnehmung, Psychoakustik, Aufmerksamkeit, Emotion), `scholar_suche`/`openalex_suche` (Marketing, Konsumentenpsychologie, HCI, Medien), `springer_suche`, `katalogplus_suche`/`sub_bestand` (Bücher, Handbücher der SUB Hamburg). Englische Suchbegriffe, Meta-Analyse/Review bevorzugen („meta-analysis“, „systematic review“).
4. **Lesen, nicht nur Titel:** Abstract (oder freien Volltext) lesen. Effektrichtung, Größe, Stichprobe, Kontext notieren. Titel allein ist kein Beleg.
5. **Evidenzstufe nennen:**
   - **A** Meta-Analyse / systematisches Review
   - **B** kontrolliertes Experiment / RCT / Feldexperiment
   - **C** Beobachtung, Korrelation, große Plattformdaten
   - **D** Fachpraxis, Lehrbuch, Experten (z. B. AES-Praxis, Mastering-Standards wie ITU-R BS.1770)
   - **E** Plattform-, Anbieter- oder Guru-Angabe (Algorithmus-Tipps, Blogposts) – nur als Hypothese
6. **Übertragbarkeit prüfen:** Gilt der Befund für Tims Nische (Hitech/Psycore, Metal-Mastering, Urbex, deutsch/englisch, Shorts)? Laborbefunde sind Richtung, keine Garantie.
7. **Mit eigenen Daten abgleichen:** `C:/social-insights` (Register, A/B-Experimente, `berichte/wachstum_*.md`, `gewinner_*.md`, `werbung_*.md`). **Belastbare eigene A/B-Daten schlagen Fremdstudien** für Tims Publikum. Widerspricht beides: als A/B-Experiment anlegen (`si.experimente`).
8. **Ablegen:** Geprüften Befund in `C:/wissenschaft/<bereich>.md` unter „Geprüfte Befunde“ eintragen:
   `- Aussage · Stufe X · Quelle (Autor Jahr, DOI) · Grenzen · Anwendung bei Tim · eigener Beleg (falls vorhanden)`.
   Bereiche: mastering-audio, musik-produktion, video, social-marketing, verkaufspsychologie, webdesign (neue Datei anlegen, wenn nötig).
9. **Im Ergebnis zeigen:** Entscheidung + Beleg in einem Satz („Hook als Frage, weil … (Stufe B, DOI …) und unser A/B cc-hook …“).

## Grenzen
- Nie Quellen, Zahlen, Effektstärken oder DOIs erfinden. Nur was ein Werkzeug zurückgegeben hat und gelesen wurde.
- Keine Ethik-Grauzonen aus der Verkaufspsychologie: keine falsche Verknappung, keine erfundenen Bewertungen oder Kundenzahlen, keine Dark Patterns (UWG, DSA, Tims Glaubwürdigkeit).
- Uni-Arbeiten zusätzlich nach den Uni-Regeln (neutral, nicht gendern, keine eigenen Projekte).
- Google Scholar nicht automatisch abfragen (keine API, CAPTCHA); `scholar_suche` gibt einen Link für Tims eigene Suche mit.
- Bezahlte Volltexte: Tim meldet sich über UHH-VPN bzw. „Institutional login“ an; Claude gibt keine Zugangsdaten ein.

## Startliteratur
`C:/wissenschaft/*.md` enthält je Bereich automatisch gezogene, meistzitierte Einstiegsliteratur (OpenAlex, ungeprüft). Bei Gebrauch lesen und als geprüften Befund hochziehen. Neu ziehen: `python C:/wissenschaft/seed.py` (eigene Befunde bleiben erhalten).
