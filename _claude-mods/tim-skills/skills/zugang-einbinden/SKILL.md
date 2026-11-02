---
name: zugang-einbinden
description: >-
  Neuen API-Schlüssel/KI-Anbieter sicher einbinden: Region und Abo-vs-API vorab prüfen, Schlüssel nie über den Chat, Ausgabengrenze, Testaufruf. Bei "hier ist mein Key", "binde X ein".
---

# zugang-einbinden

Belegt (Okt./Nov. 2026): Schlüssel für Telefon-API, Kimi und Google landeten im Klartext im Chat;
danach stellte sich heraus, dass der Dienst in der EU nicht verfügbar war, das Abo per API keine
Pro-Modelle liefert oder die CLI für Privatkonten gesperrt ist. Diese Reihenfolge verhindert beides.

**Grenzen:** Schlüssel nie ausgeben, nie in Prompts, Routinen, Commits oder Skill-Dateien schreiben.
Nichts kaufen, keine Abos abschließen.

## Ablauf

1. **Vorab prüfen, bevor ein Schlüssel angelegt wird** (Doku des Anbieters lesen):
   - Verfügbar in Deutschland/EU? Für Privatkonten oder nur Firmen?
   - Bringt das Abo (z. B. „Pro“, „Plus“) auch API-Zugang – oder ist API extra und nach Verbrauch?
   - Welches Modell/welcher Endpunkt genau, Preis pro Einheit, gibt es eine Ausgabengrenze?
   Ergebnis Tim in 3–5 Zeilen sagen. Passt es nicht: hier stoppen und Alternative nennen.
2. **Schlüssel ohne Chat übergeben lassen:**
   - Lokal (Windows): Tim legt ihn selbst in den Schlüsselordner (`C:\Users\<name>\OneDrive\Claude-Keys\<dienst>.env`,
     Zeile `NAME=wert`) oder kopiert ihn in die Zwischenablage; Claude liest ihn per Skript in die Datei, ohne ihn anzuzeigen.
   - Cloud-Routinen: als Secret der Cloud-Umgebung (claude.ai/code → Umgebung bearbeiten → Umgebungsvariablen) bzw.
     als GitHub-Actions-Secret; im Prompt nur der Variablenname.
   - Steht ein Schlüssel schon im Chat: einbinden, aber Tim sagen, dass er im Verlauf gespeichert ist, und zum
     Erneuern beim Anbieter raten (alter Schlüssel löschen).
3. **Ausgabengrenze setzen**, wo der Anbieter es erlaubt (Monatslimit/Budget im Dashboard), sonst Tim darum bitten.
4. **Testaufruf** mit minimaler Anfrage; nur Erfolg/Fehlercode und Modellname melden, nie den Schlüssel.
   Prüfen mit `test -n "$NAME"` (Bash) bzw. ohne Ausgabe des Werts.
5. **Festhalten:** Memory/CLAUDE.md-Eintrag „<Dienst>: Variable NAME, Ort, Grenzen (Region, Modelle, Preis)“ –
   ohne Wert. Bei Routinen: `routine-einrichtung` (Konnektoren nur das Nötige).

## Typische Fallen

- „Abo“ ≠ API: Verbraucher-Abos (Chat-Apps) schalten meist keine API frei.
- Regionale Sperren (EU) zeigen sich oft erst beim ersten Aufruf → Schritt 1 nicht überspringen.
- OAuth-/Login-Flows („Angemeldet?“) kann Claude nicht selbst durchklicken: Tim einmal anmelden lassen, dann prüfen.
