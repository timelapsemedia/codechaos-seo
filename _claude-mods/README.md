# tim-mods – Claude-Code-Mods

Getestet mit Claude Code **2.1.292** (Mods brauchen im Terminal ≥ 2.1.287, in der Desktop-App ≥ 2.1.286).
Die Mod-API ist „early access“ und kann sich zwischen Versionen ändern.

| Mod | Was sie tut | Befehl | Terminal / Desktop | Cloud-Session |
|---|---|---|---|---|
| `limit-cockpit` | Leiste über dem Prompt: 5h-Limit in %, Reset, Kontext in %, Warnung ab 75 % Wochenlimit, Knopf „Neuer Chat mit Übergabe“. Nach jeder Antwort: Top-3-Token-Treiber, **gemessen** (API-Usage pro Anfrage) getrennt von **geschätzt** (Tool-Ausgaben, Zeichen ÷ 4). | `/handoff`, `/cockpit` | Leiste + Zeile | keine Leiste; `/cockpit` und `/handoff` als Text |
| `pruefer` | Beobachtet nur. Bei der Abgabe: Dateien geändert, aber danach kein grüner Test/Build/Typcheck/Aufruf → schickt Claude zurück (max. 2× pro Antwort). „nicht getestet, weil …“ geht durch. Nie bei Rückfragen, Hintergrundjobs, Headless. Optional Zweitprüfung durch ein zweites Modell (kostet extra Tokens, sichtbarer Hinweis). Learnings pro Projekt → neue Sessions. | `/pruefer`, `/pruefer zweit aus`, `/pruefer panel` | Seitenpanel | wirkt nur, wenn die Session eine Oberfläche meldet |
| `schutzschild` | Hält riskante Schritte an (löschen, `git push --force`, `git reset --hard`, DB leeren, `.env`/Schlüssel, Dateien außerhalb des Projekts) und fragt in einfachen Worten. Ohne Bestätigung oder bei Prüffehler: blockiert. Erlaubt nie pauschal; deine Berechtigungsregeln bleiben. **Mustererkennung – kein vollständiger Schutz.** | `/schutzschild` | Statuszeile „heute X geprüft · Y angehalten“ | Rückfrage über den Fragedialog, sonst Block |
| `spar-modus` | **Experiment, standardmäßig aus.** Nach reinen Lese-Schritten probiert Haiku den nächsten Schritt; übernommen wird er nur, wenn Haiku selbst nur weiterliest – sonst verworfen und beim großen Modell wiederholt (als Mehrkosten gezählt). Zähler: Haiku-Schritte, gemessene Tokens, geschätzte API-Kosten, „Ersparnis unbekannt“. | `/sparmodus` | Zähler am Ladesymbol | nur Text über `/sparmodus` |
| `studio-kompass` | Regeln je Arbeitsbereich (Musik, Mastering, Video/Untertitel, Motion, Social, SEO, Etsy, Recherche), automatische Prüfungen (SRT/VTT, HTML-SEO, Captions) als Hinweis an Claude, Warnung bei Geheimnissen in Nachrichten, volle Dateipfade, Cloud/Lokal-Hinweis. | `/studio`, `/dateien` | ja | ja (braucht keine Oberfläche) |

## Installieren – lokal (Terminal und Desktop-App auf deinem Rechner)

Im Terminal (die Desktop-App lädt Plugins mit, die du im Terminal im Benutzer-Scope installierst):

```bash
git clone -b claude/epic-dirac-w38jzi https://github.com/timelapsemedia/codechaos-seo.git ~/codechaos-seo
claude plugin marketplace add ~/codechaos-seo/_claude-mods
claude plugin install limit-cockpit@tim-mods
claude plugin install pruefer@tim-mods
claude plugin install schutzschild@tim-mods
claude plugin install studio-kompass@tim-mods
claude plugin install spar-modus@tim-mods   # optional, Experiment, startet ausgeschaltet
```

In einer laufenden Sitzung danach `/reload-plugins`. `/plugin` zeigt „N mods active · …“.

## Installieren – für alle Cloud-Sessions (egal welches Repo)

Cloud-Sessions übernehmen keine Plugins aus deinen lokalen Einstellungen und keine `enabledPlugins` aus Repo-Einstellungen.
Was ankommt, ist das **Setup-Skript der Cloud-Umgebung**. Deshalb:

1. claude.ai/code → Cloud-Umgebung bearbeiten → **Setup script**.
2. Den Inhalt von [`cloud-setup.sh`](cloud-setup.sh) einfügen (enthält die Mods eingebettet, braucht kein Netzwerk).
3. Neue Session starten. Die Umgebung wird neu gecacht; danach haben alle Sessions dieser Umgebung die Mods.

Nach Änderungen an den Mods: `./build-cloud-setup.sh` ausführen und das neue `cloud-setup.sh` erneut einfügen.

## Abschalten

- Eine Mod: `/plugin` → Tab **Installed** → Mod deaktivieren, oder `claude plugin disable <mod>@tim-mods`.
- Nur die Funktion: `/pruefer`, `/schutzschild`, `/sparmodus` schalten an/aus.
- Alle Mods: `"disableAllHooks": true` in `~/.claude/settings.json` (stoppt auch Settings-Hooks und Statuszeile) oder einmalig `claude --safe-mode`.
- Cloud: Zeilen aus dem Setup-Skript entfernen.

## Ehrliche Grenzen

- In Cloud-Sessions zeichnen Mods nichts (keine Leisten, Panels, Zähler) – Hooks und Befehle laufen.
- 5h-/Wochenprozente zeigt `limit-cockpit` nur, wenn die API sie meldet (Abo, nach der ersten Antwort); sonst „keine Messung“.
- Tokens einzelnen Tool-Schritten zuzuordnen liefert die API nicht – nur pro Anfrage. Tool-Ausgaben sind deshalb als Schätzung markiert.
- „Neuer Chat“: `/handoff` startet über `/clear` ein neues Gespräch (das alte bleibt über `/resume` erreichbar) und legt die Übergabe ins Eingabefeld; geht das nicht, kommt der Hinweis „Übergabe kopiert. Neuen Chat öffnen und Cmd+V beziehungsweise Strg+V drücken.“
- `spar-modus`: Haiku hat nur 200K Kontext und keinen warmen Cache des großen Modells; Opus-5.5-Cache-Lesen (0,20 $/Mio.) ist billiger als ungecachte Haiku-Eingabe (1 $/Mio.). Es kann teurer werden – deshalb Experiment und „Ersparnis unbekannt“.

## Prüfen

```bash
claude plugin validate _claude-mods            # Marketplace + Manifeste + Hooks
cd _claude-mods/<mod> && claude plugin test    # Tests je Mod
```
