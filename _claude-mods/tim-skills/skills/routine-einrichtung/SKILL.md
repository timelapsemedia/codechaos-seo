---
name: routine-einrichtung
description: >-
  Eine neue Routine (geplanter Claude-Code-Lauf, Trigger) für Tim richtig
  anlegen oder umbauen – mit Checkliste für Repos, Branch, Freigaben,
  Zugangsdaten, Kosten, Bericht und Testlauf, damit der erste echte Lauf nicht
  scheitert. Nutzen bei "richte eine Routine ein", "jeden Tag/jede Woche
  automatisch", "plane das", "Routine anlegen/ändern", "warum hat die Routine
  nicht auf main gepusht", "wo trage ich die Repos ein", "Routine ohne
  Rückfragen". Prüft den Prompt vor dem Anlegen auf Klartext-Zugangsdaten.
---

# routine-einrichtung

Belegt (Oktober 2026): Neue Routinen scheiterten im ersten Lauf immer an denselben Stellen –
Repos fehlten in der Umgebung, Pushes landeten auf Nebenzweigen statt auf `main`, eine
Sicherheitsprüfung blockte einen Upload, weil die Freigabe nicht im Prompt stand, und Tokens
standen im Klartext im Prompt. Diese Checkliste geht alles vorher durch.

**Grenzen:** Routine erst anlegen, wenn Tim den fertigen Prompt gesehen und „ja“ gesagt hat.
Zugangsdaten nie in Prompt, Dateien oder Commits schreiben und nie ausgeben.

## Checkliste (in dieser Reihenfolge)

1. **Ziel in einem Satz** und Erfolgskriterium („fertig heißt: …“).
2. **Takt:** so selten wie möglich. Beobachtungen (prüfen, ob sich etwas geändert hat)
   lieber täglich als stündlich. Uhrzeit in `CRON_TZ=Europe/Berlin`, Minute nicht auf :00.
3. **Session-Art:**
   - *Frische Session pro Lauf* (Standard): günstig, sauber, braucht alles im Prompt.
   - *Dieselbe Session* nur, wenn der Lauf den Verlauf wirklich braucht – dann nicht stündlich
     (jeder Lauf liest den ganzen Verlauf erneut, das wird teuer).
4. **Repos und Umgebung:** Welche Repos braucht der Lauf? Im Prompt `owner/repo` nennen und
   den Fallback „falls nicht im Container: per add_repo (Zugriff push) hinzufügen und klonen“.
   Tim zeigen, wo die Repos der Umgebung eingetragen werden:
   claude.ai/code → Umgebung bearbeiten → Repositories (bei Unsicherheit die Doku-Seite
   `github.access` bzw. `environment.setup_script` lesen).
5. **Branch:** ausdrücklich festlegen – entweder „direkt nach main pushen
   (`git push origin HEAD:main`, vorher `git pull --no-rebase origin main`)“ oder „Branch,
   PR gegen main, mergen“. Ohne Angabe landen Pushes auf Session-Branches.
6. **Freigaben wörtlich:** Alles mit Außenwirkung (posten, veröffentlichen, hochladen,
   verkaufen, mergen) braucht Tims Freigabe **mit Datum und Wortlaut** im Prompt, plus harte
   Grenzen (z. B. „höchstens 1 Post pro Lauf“, „keine Echtgeld-Aktionen“). Sonst stoppt die
   Sicherheitsprüfung im unbeaufsichtigten Lauf.
7. **Zugangsdaten:** nur als Secret der Cloud-Umgebung bzw. lokale Umgebungsvariable; im
   Prompt nur der Name (`INSTAGRAM_ACCESS_TOKEN`), Prüfung nur mit `test -n`. Regel in den
   Prompt: „bei 401/abgelaufenem Token: stoppen und melden, keinen neuen Token besorgen“.
   Für Instagram `@codechaos_official` `insta-publisher` nutzen (`ig_status`,
   `ig_token_verlaengern`), Ablaufdatum als Erinnerung einplanen.
8. **Regeln gegen Doppelarbeit:** idempotent (vorher prüfen, ob schon erledigt; Zustand in
   einer Datei im Repo), „nur vorwärts“, Höchstmengen pro Lauf.
9. **Bericht:** letzte Nachricht kurz auf Deutsch, Format vorgeben; Benachrichtigung
   (push/E-Mail) einschalten. Ohne Bericht fallen Ausfälle nicht auf.
10. **Prompt prüfen:** Entwurf als Datei speichern und
    `python3 ../routine-waechter/routinen_check.py --prompt <datei>` ausführen.
    PROBLEM muss weg; HINWEISE bewusst entscheiden.
11. **Tim zeigen**, nach „ja“ anlegen (`create_trigger`), dann **einen Testlauf**
    (`fire_trigger`), den Verlauf der Test-Session lesen (`list_events`, kinds
    `["result","assistant"]`) und erst nach grünem Testlauf „läuft“ melden.

## Vorlage für den Prompt

```
<Ziel in einem Satz>. Freigabe von Tim (<Datum>, wörtlich): „…“.
1. Repos: <owner/repo> (falls fehlt: add_repo push, klonen). Auf main arbeiten: git pull …
2. Lies <PLAYBOOK.md> und befolge es.
3. Harte Regeln: … (Höchstmengen, nie …, Zugangsdaten nur per test -n prüfen, nie ausgeben)
4. Bei Fehlern (401/Limit/fehlendes Werkzeug): stoppen, nichts halb veröffentlichen, melden.
5. Ergebnis: <wohin committen/pushen>.
6. Bericht auf Deutsch, 3–6 Zeilen: <Format>.
```

Danach `routine-waechter` erwähnen: Er prüft alle Routinen gesammelt auf Ausfälle.
