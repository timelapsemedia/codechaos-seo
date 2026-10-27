---
name: routine-waechter
description: >-
  Alle Routinen (geplante Claude-Läufe) auf Ausfälle prüfen: fehlgeschlagen, überfällig, Limit, abgelaufene Tokens, Klartext-Zugangsdaten, teure Dauer-Sessions. Bei "laufen meine Routinen?", "Routine-Check", "warum kam kein Bericht". Nur lesen.
---

# routine-waechter

Tims Routinen (SEO, Etsy, Social, Myriad, Audio-Produkte, Wikipedia, Skill-Scout …) laufen
ohne ihn. Fällt einer aus (Wochenlimit, abgelaufener Token, Fehler im Skript), merkt er es
oft erst Tage später. Dieser Skill macht daraus **eine** kurze Meldung.

**Grenzen:** Nur lesen. Routinen nicht ändern, nicht löschen, nicht abschalten und nicht
auslösen, solange Tim das nicht in dieser Session ausdrücklich sagt. Zugangsdaten nie
ausgeben, auch nicht gekürzt.

## Ablauf

1. **Routinen holen:** `list_triggers` (limit 100; bei `has_more` mit `next_cursor` weiter).
   Jede Seite als Datei im Scratchpad speichern (`routinen-1.json`, `routinen-2.json` …).
   Ist die Ausgabe zu groß, landet sie automatisch in einer Datei – die nehmen.
2. **Prüfen:** `python3 routinen_check.py routinen-*.json`
   (Skript liegt neben dieser Datei; nur Standardbibliothek, kein Netz.) Es meldet je Routine:
   - **ROT:** letzter Lauf nicht `SUCCEEDED`, endgültig beendet, überfällig (> 3 h nach
     `next_run_at`), **Zugangsdaten im Klartext im Prompt** (nur Art und Zeile, nie der Wert).
   - **GELB:** pausiert, stündlich in derselben Session (teuer), Session-Routinen, deren
     `SUCCEEDED` nur „zugestellt“ bedeutet.
3. **Ergebnis der Läufe nachsehen** – das Skript sieht nur den Zustellstatus. Für jede aktive
   Routine mit Lauf in den letzten 2 Tagen: `list_events` der `session_id` aus `last_run`
   mit `kinds ["result"]` (bei Session-Routinen zusätzlich `["assistant"]`, letzte Seite).
   Achten auf: „limit“, „rate limit“, „Wochenlimit“, „401“, „403“, „token“, „expired“,
   „abgelaufen“, „BLOCKER“, „fehlgeschlagen“, „konnte nicht“, leere Berichte.
4. **Meldung schreiben** (Deutsch, kurz):
   ```
   Routinen-Check <Datum>: <n> ok, <n> mit Problem
   ROT  <Name> – <was> – <was Tim tun muss / was ich nachholen könnte>
   GELB <Name> – <Hinweis>
   ```
   Bei Klartext-Geheimnissen immer dazuschreiben: Zugang beim Anbieter erneuern (der alte
   Wert gilt als offen), neuen Wert als Secret der Cloud-Umgebung bzw. lokal als
   Umgebungsvariable hinterlegen, im Prompt nur den Variablennamen nennen.
5. **Nachholen anbieten, nicht selbst tun:** Ist ein Lauf wegen Limit ausgefallen und das
   Limit wieder frei, „Soll ich <Routine> jetzt nachholen?“ fragen. Erst nach Tims „ja“
   `fire_trigger` aufrufen.

## Bekannte Fallen

- **Session-Routinen** (`persist_session: true`): `last_run` sagt nur, dass die Nachricht
  ankam. Ob der Lauf geklappt hat, steht nur im Verlauf der Session.
- **Stündlich in einer großen Session** liest jeder Lauf den ganzen Verlauf erneut (belegt:
  Wikipedia-Beobachtung, Oktober 2026, sehr hohe Cache-Kosten für „nichts geändert“).
  Vorschlag an Tim: Beobachtungs-Routinen mit frischer Session pro Lauf oder seltener.
- **Instagram/Meta-Tokens** laufen ab oder werden von Meta ungültig gemacht. Für
  `@codechaos_official` gibt es `insta-publisher` (`ig_status`, `ig_token_verlaengern`) –
  zuerst diesen nutzen, statt Tokens im Chat auszutauschen.
- **Wochenlimit:** mit dem Mod `limit-cockpit` gegenprüfen, ob das Limit der Grund war.

## Neue Routinen

Für das Anlegen oder Umbauen einer Routine den Skill `routine-einrichtung` nutzen; dessen
Prompt-Prüfung (`routinen_check.py --prompt`) verhindert die Fälle, die dieser Skill meldet.
