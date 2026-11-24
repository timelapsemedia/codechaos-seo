---
name: kontext-haushalt
description: >-
  Kontext und Tokenverbrauch messen und senken: Startkontext je Session, Kontext je Anfrage,
  CLAUDE.md, MEMORY.md, MCP-Server, Skill-Liste, Routine-Prompts. Entscheidet, wohin eine neue
  Regel gehört (CLAUDE.md, Pfad-Regel, Skill, Hook, Memory), und liefert die Vorlage für Aufträge
  an Sessions und Subagenten. Nutzen bei "Verbrauch senken", "Limit", "Kontext zu groß",
  "CLAUDE.md kürzen", "neue Regel eintragen", "Session ist lang", "Brief für Subagent",
  "welche MCPs brauchen wir", vor jeder neuen Routine und im wöchentlichen Lern-Lauf.
---

# kontext-haushalt

Jede Anfrage liest den ganzen Kontext neu. Bezahlt wird also vor allem, was schon dasteht, bevor
die Arbeit beginnt, und was sich in langen Sessions ansammelt. Der Skill misst das und nennt den
Hebel. Quellen und Messwerte: `C:/wissenschaft/agentische_ki.md`.

## 1. Messen (immer zuerst)

```
python "${CLAUDE_SKILL_DIR}/scripts/kontext_messen.py" --stunden 24
python "${CLAUDE_SKILL_DIR}/scripts/kontext_messen.py" --stunden 168 --json
python "${CLAUDE_SKILL_DIR}/scripts/kontext_messen.py" --gate      # Exit 1 bei Befund
```

Das Skript liest nur lokale Dateien und Transkripte, verbraucht keine Tokens und schreibt nichts.
Es liefert: Startkontext (Median der ersten Anfrage), Kontext je Anfrage, Sessions über 400k,
feste Dateien, CLAUDE.md nach Abschnitt, größte Routine-Prompts, MCP-Server mit Aufrufen.

Zerlegung des Startkontexts, wenn sie gebraucht wird (drei kurze Haiku-Läufe, zusammen wenige Cent):

```
claude -p "Antworte nur: ok" --model haiku --output-format json --max-turns 1
... --strict-mcp-config --mcp-config leer.json          # ohne MCP ({"mcpServers":{}})
... --strict-mcp-config --mcp-config leer.json --disable-slash-commands   # ohne Skill-Liste
```

Kontext = `input_tokens + cache_creation_input_tokens + cache_read_input_tokens` aus `usage`.

Ausgangswerte vom 24.11.2026: Startkontext 148k, Mittel 392k je Anfrage, fester Text 19,8k,
MCP rund 25k, Skill-Liste rund 6k.

## 2. Hebel in dieser Reihenfolge

1. **Sessionlänge.** Über 400k Kontext: Stand in OFFEN.md bzw. Übergabedatei schreiben, neue
   Aufgabe in frische Session. Themenwechsel in langer Session: abgeben, nicht weiterschleppen.
2. **MCP-Server.** Server ohne Aufruf im Zeitraum (Skript, 7 Tage) kosten Werkzeugnamen und
   Anleitungen in jeder Anfrage. Liste an Tim bzw. die Leitstelle geben. Konto-Konnektoren
   schaltet nur Tim ab. Vor dem Abschalten prüfen, ob eine Routine den Server nennt
   (`grep -l "<server>" ~/.claude/scheduled-tasks/*/SKILL.md`).
3. **Fester Text.** CLAUDE.md unter 200 Zeilen je Datei. @-Importe sparen nichts. MEMORY.md lädt
   nur die ersten 200 Zeilen bzw. 25 KB, alles dahinter fehlt jeder Session.
4. **Routine-Prompts.** Über rund 3k Tokens: festen Ablauf in ein Skript, Fachwissen in einen
   Skill, im Prompt bleiben Ziel, Abnahme und Bericht.
5. **Werkzeugausgaben.** Lange Ausgaben in eine Datei leiten und nur das Nötige lesen. Breite
   Suche an einen Subagenten geben, der eine Zusammenfassung zurückgibt.

## 3. Wohin gehört eine neue Regel?

| Die Regel … | Ort | Warum |
|---|---|---|
| darf keine Ausnahme haben und ist maschinell prüfbar | Hook, Gate, Test | wird ausgeführt, nicht erbeten |
| gilt in jeder Session und in jedem Bereich | CLAUDE.md, eine Zeile | wird immer geladen |
| gilt nur für einen Ordner oder Dateityp | `~/.claude/rules/<bereich>.md` mit `paths:` | lädt nur bei passenden Dateien |
| ist ein Ablauf oder Fachwissen eines Bereichs | Skill | lädt nur Name und Beschreibung |
| ist ein Einzelfall, Projektstand oder eine Vorliebe | Memory-Datei, eine Zeile im Index | nachladbar über `wissen_suche` |

Vor dem Eintragen: Steht die Regel schon irgendwo? Eine wiederholte oder immer stärker betonte
Zeile ist das Zeichen, dass sie in einen Hook gehört. Widersprüche zwischen zwei Orten zuerst
auflösen, sonst befolgt das Modell mal die eine, mal die andere.

## 4. Auftrag an Session oder Subagent

Grundlage ist `C:/leitstelle/VERTRAG.md` (acht Felder). Für schlanken Kontext zusätzlich:

- **Kontext:** Pfade und Entscheidungen, keine kopierten Dateiinhalte. Was der Empfänger selbst
  lesen kann, wird verlinkt.
- **Rückgabe:** Format vorgeben (z. B. „Ergebnis, Beleg je Punkt, offene Punkte“) und eine
  Obergrenze von rund 1.500 Tokens. Große Funde in eine Datei, im Bericht steht der Pfad.
- **Aufwand:** Rahmen nennen. Einfache Frage: 1 Agent, 3–10 Werkzeugaufrufe. Vergleich: 2–4
  Agenten. Mehr nur bei breiter, teilbarer Arbeit mit hohem Wert (Skill `agenten-schwarm`).
- **Schon ausgeschlossen:** was geprüft und verworfen ist, damit es nicht noch einmal geschieht.

Subagenten lohnen sich für Breite, für lange Ausgaben und für einen Prüfer ohne Vorwissen. Für
Aufgaben mit gemeinsamem Zustand und für wenige Werkzeugaufrufe sind sie teurer als Selbstmachen.

## 5. Abnahme

Eine Änderung zählt erst mit Vorher/Nachher aus dem Skript: betroffene Kennzahl, Zeitraum,
Differenz. Rückweg sichern (`<datei>.vor-<änderung>-<datum>`). Kürzen an CLAUDE.md nur mit
Nachweis, wohin jeder entfernte Satz gewandert ist (`C:/selbstverbesserung/wissen/NACHWEIS.md`).
Regeln von Tim werden verschoben oder zusammengefasst, nie gestrichen.
