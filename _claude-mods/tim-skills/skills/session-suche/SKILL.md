---
name: session-suche
description: >-
  Über frühere Claude-Sessions hinweg suchen (Cloud: list_sessions/list_events, lokal: ~/.claude/projects) und Fundstelle mit Session, Datum, Zitat melden. Bei "wo hatten wir…", "in welcher Session", "such im Verlauf".
---

# session-suche

Belegt (06.11., Sessions „Automatisierte Geldverdienung“ und „Kündigungsprozess“): Tim fragte
nach etwas aus einer anderen Session; jedes Mal wurde von vorn gesucht oder geraten.

**Grenzen:** Nur lesen. Verläufe enthalten teils Zugangsdaten im Klartext: nie Rohverläufe
speichern oder ausgeben, Treffer nur als kurzes Zitat (≤ 2 Sätze), Geheimnisse durch
`[entfernt]` ersetzen. Keine Nachrichten an andere Sessions senden.

## Ablauf

1. **Suchbegriffe** aus Tims Frage: 2–4 Wörter plus Synonyme (de/en), Zeitraum, falls genannt.
2. **Cloud** (claude-code-remote):
   - `list_sessions` (`mine: true`, limit 100, ggf. mit `after_id` weiter); erst nach **Titel** filtern.
   - Für die 5–10 passendsten: `list_events` mit `kinds ["user","assistant"]`, limit 100,
     rückwärts mit `before_id` blättern, bis Treffer oder Session-Anfang.
   - Viele Sessions: an einen Agenten delegieren, der nur Fundstellen zurückgibt
     (Session-Titel, ID, Datum, kurzes Zitat) – keine Rohdaten in Dateien.
3. **Lokal** (Windows/Mac, Claude Code): Verläufe liegen als JSONL unter
   `~/.claude/projects/<projekt>/*.jsonl`.
   `grep -il "<begriff>" ~/.claude/projects/*/*.jsonl` → Dateien; dann
   `grep -o ".\{0,120\}<begriff>.\{0,120\}" <datei> | head` für den Kontext.
   Datum aus dem Feld `timestamp` derselben Zeile.
4. **Melden:** je Treffer `Session-Titel – Datum – Zitat – Link/Pfad`
   (Cloud-Link: `https://claude.ai/code/<session_id>`). Nichts gefunden: sagen, wo gesucht wurde.
5. Ist das Gefundene eine Entscheidung oder Regel, die wieder gebraucht wird: vorschlagen,
   sie in CLAUDE.md/Memory festzuhalten.
