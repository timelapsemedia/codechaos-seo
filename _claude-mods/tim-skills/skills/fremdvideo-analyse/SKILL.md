---
name: fremdvideo-analyse
description: >-
  Fremdes Video/Reel/Short per Link analysieren (Hook, Tempo, Aufbau, Zahlen, Machart) und Lehren für Tims Inhalte ableiten, ohne Text zu kopieren. Bei "schau dir das Video an", "analysiere diesen Reel", Video-Link.
---

# fremdvideo-analyse

Belegt (Sessions 03.11., 08.11. „Automatisierte Geldverdienung“, 08.11. „YouTube-Videoanalyse“):
Tim schickt Links zu fremden Videos und will wissen, was daran funktioniert und was er
übernehmen kann. In der Cloud scheitert der Abruf meist (YouTube/Instagram sperren
Rechenzentren, Login nötig). Dieser Ablauf kommt trotzdem zu einer belastbaren Analyse.

**Grenzen:** Nur analysieren. Fremden Text, Bild oder Ton nicht übernehmen; Ergebnis in
eigenen Worten. Keine Behauptung über Inhalte, die nicht gesehen/gehört wurden.
Zahlen/Versprechen aus dem Video (Umsatz, „passives Einkommen“) als Behauptung kennzeichnen.

## Ablauf

1. **Quelle beschaffen** (erste Stufe, die klappt):
   a. Lokal am PC: `yt-dlp -f "bv*[height<=720]+ba/b" -o "%(id)s.%(ext)s" <link>` plus
      `--write-auto-subs --sub-langs "de,en" --skip-download` für Untertitel.
   b. Cloud: dasselbe versuchen; bei 403/Login/„Sign in to confirm“ nicht umgehen.
   c. Sonst Tim um eins bitten: Datei/Bildschirmaufnahme hochladen, Transkript (YouTube:
      „Transkript anzeigen“) oder 3–5 Screenshots. Nur Metadaten (Titel, Beschreibung) reichen
      für eine Aussage über Hook und Verpackung, nicht über den Inhalt – dann so sagen.
2. **Messen** mit `video-werkstatt`: `analysieren` (Dauer, Format, Lautheit, Schnitte →
   Schnitte pro Minute), `standbilder` (Kontaktbogen), `transkribieren` (falls kein Untertitel).
3. **Auswerten** (Tabelle, je Punkt Zeitstempel):
   - Hook 0–3 s: Bild, erster Satz, Texteinblendung; welcher Hook-Typ.
   - Aufbau: Abschnitte mit Zeiten, wo die Auflösung kommt, Call-to-Action.
   - Tempo: Schnitte/Minute, Sprechtempo (Wörter/Minute), Musik/Lautheit.
   - Behauptungen und Zahlen: belegt / unbelegt / Werbung (Affiliate, Kurs).
   - Was davon passt zu Tims Marken (Code Chaos, Polished Metal Mastering, keinduftbaum) –
     konkret, max. 3 Punkte, und was nicht (Clickbait, unbelegte Geldversprechen).
4. **Übergabe:** Für eigenes Video gleich weiter an `hook-master`, `ig-reel`/`yt-script`
   oder `code-chaos-motion`; bei Geld-Ideen an `money-diagnose`.
