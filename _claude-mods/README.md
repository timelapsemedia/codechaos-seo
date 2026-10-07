# tim-mods – Claude-Code-Mods

Getestet mit Claude Code **2.1.292**. Mods brauchen im Terminal mindestens 2.1.287 und in der Desktop-App mindestens 2.1.286.
Die Mod-API ist „early access“ und kann sich zwischen Versionen ändern.

Grundlage ist eine Auswertung von 60 Sessions (Juli bis Oktober 2026). Die meisten davon liefen auf einem Windows-PC mit Git Bash, die übrigen in der Cloud. Die Mods sind auf beide Umgebungen ausgelegt.

## Werkzeug-Mods: geben Claude echte Messwerkzeuge

Diese Mods laufen auch in Cloud-Sessions, weil sie nichts zeichnen müssen. Sie brauchen ffmpeg/ffprobe und Python 3; die Instagram-Mod nutzt nur die Python-Standardbibliothek.

| Mod | Werkzeuge für Claude | Automatisch |
|---|---|---|
| `audio-labor` | `messen`: LUFS, LRA, True Peak, Crest, DC, Stereo-Korrelation, Frequenzanteile, Clipping, Stille, Klick am Ende, Spektrogramm. `vergleichen`: Vorher/Nachher oder gegen eine Referenz. `midi_pruefen`: Tempo, Takte, Töne außerhalb einer Skala. `lua_pruefen`: ReaScript. | Bevor Claude dir eine Audiodatei schickt, wird sie gemessen. Bei Problemen hält die Mod den Versand einmal an. |
| `video-werkstatt` | `analysieren` mit Plattform-Check und Kontaktbogen, `standbilder` mit Safe-Area-Linien, `shorts_untertitel` (ASS für Hochkant, Schlüsselwörter farbig), `einbrennen`, `transkribieren` (Whisper, falls installiert), `untertitel_pruefen` | Videos und SRT/VTT werden vor dem Versand geprüft. |
| `seo-werkstatt` | `site_pruefen`: lokaler Ordner vor dem Push – kaputte Links, `.jpg` statt `.jpeg`, Groß-/Kleinschreibung, div-Balance, hreflang. `seite_pruefen` und `sitemap_pruefen` für die Live-Seite. | – |
| `social-studio` | `text_pruefen`: Captions, Titel, Etsy-Tags; deine Vorgabe von 5 Hashtags, KI-Hinweis, Warnung bei Heil- und Wirkversprechen. `bilder_pruefen`: Feed, Story, Etsy und Thumbnails, Karussell einheitlich. | – |
| `insta-publisher` | `ig_zugang_speichern` (Token aus Umgebungsvariable oder Plugin-Speicher), `ig_status`, `ig_posten` (Bild, Karussell, Reel; ohne `bestaetigt` nur Vorschau; mit Live-Prüfung und Wiederholung bei Ratenlimit), `ig_insights`, `ig_token_verlaengern` | Regel an Claude: Tokens nie in Routinen oder Prompts schreiben. |
| `windows-helfer` | – | Unter Windows: `python3` wird zu `python`, UTF-8 wird für Python erzwungen. Überall: Fehlt ein Modul, nennt die Mod den passenden pip-Befehl; bei curl mit Umlauten warnt sie. |
| `raritaeten-jaeger` | `suchlinks` (sagt dazu, welche Seiten Bots blocken), `suche_merken`, `fund_merken`, `suchverlauf` – das Gedächtnis gilt über alle Sessions | – |

## Arbeits-Mods

| Mod | Was sie tut | Befehl |
|---|---|---|
| `limit-cockpit` | Leiste mit 5h-Limit, Reset-Zeit und Kontext; Warnung ab 75 % Wochenlimit; die größten Token-Treiber, getrennt nach gemessen und geschätzt | `/handoff`, `/cockpit` |
| `pruefer` | Hält eine Abgabe ohne Beleg höchstens 2× an. Die Messwerkzeuge oben zählen als Beleg. Seitenpanel, Learnings pro Projekt. | `/pruefer` |
| `schutzschild` | Fragt vor riskanten Schritten nach. Versteht Windows-Pfade. Mustererkennung, also kein vollständiger Schutz. | `/schutzschild` |
| `spar-modus` | **Experiment, standardmäßig aus.** Schickt leichte Schritte an Haiku und zeigt „Ersparnis unbekannt“. | `/sparmodus` |
| `studio-kompass` | Regeln je Arbeitsbereich mit deinen Vorgaben: Deutsch; vor der Abgabe selbst prüfen; 5 Hashtags und KI-Hinweis; nur echte Produkte; DaVinci-Regeln. Dazu Warnung, wenn ein Geheimnis im Chat steht. | `/studio`, `/dateien` |

## Installieren – Windows-PC, Mac oder Linux (Terminal und Desktop-App)

In Git Bash (Windows) oder im Terminal (Mac/Linux) ausführen. Die Desktop-App lädt Plugins, die im Terminal im Benutzer-Scope installiert wurden.

```bash
git clone -b claude/epic-dirac-w38jzi https://github.com/timelapsemedia/codechaos-seo.git ~/codechaos-seo
claude plugin marketplace add ~/codechaos-seo/_claude-mods
for m in limit-cockpit pruefer schutzschild studio-kompass audio-labor video-werkstatt seo-werkstatt social-studio insta-publisher windows-helfer raritaeten-jaeger; do claude plugin install "$m@tim-mods"; done
claude plugin install spar-modus@tim-mods   # optional, Experiment, startet ausgeschaltet
```

Danach in einer laufenden Sitzung `/reload-plugins` eingeben. `/plugin` zeigt, welche Mods aktiv sind.
Auf dem PC werden zusätzlich gebraucht: ffmpeg und ffprobe im PATH, Python 3 und für `lua_pruefen` node. Für `transkribieren`: `python -m pip install faster-whisper`.

## Installieren – für alle Cloud-Sessions, egal welches Repo

Cloud-Sessions übernehmen weder lokale Plugins noch `enabledPlugins` aus Repo-Einstellungen. Nur das **Setup-Skript der Cloud-Umgebung** kommt an:

1. Auf claude.ai/code die Cloud-Umgebung bearbeiten und **Setup script** öffnen.
2. Den Inhalt von [`cloud-setup.sh`](cloud-setup.sh) einfügen. Er enthält alle Mods eingebettet und braucht kein Netzwerk.
3. Eine neue Session starten.

Nach Änderungen an den Mods `./build-cloud-setup.sh` ausführen und das neue Skript erneut einfügen.
Für Instagram in der Cloud: In der Umgebung die Variable `IG_TOKEN` setzen und einmal `ig_zugang_speichern` mit `token_env=IG_TOKEN` aufrufen.

## Abschalten

- **Eine Mod:** `/plugin` → Tab **Installed** → deaktivieren, oder `claude plugin disable <mod>@tim-mods`.
- **Nur die Funktion:** `/pruefer`, `/schutzschild` und `/sparmodus` schalten an und aus.
- **Alle Mods:** `"disableAllHooks": true` in `~/.claude/settings.json` (stoppt auch Settings-Hooks und Statuszeile), oder einmalig `claude --safe-mode`.
- **Cloud:** das Setup-Skript entfernen.

## Ehrliche Grenzen

- **Zeichnen:** In Cloud-Sessions zeichnen Mods nichts, also keine Leisten, Panels oder Zähler. Werkzeuge, Hooks und Befehle laufen.
- **Abo-Limit:** Die 5h- und Wochenprozente zeigt `limit-cockpit` nur, wenn die API sie meldet. Tokens einzelnen Schritten zuzuordnen liefert die API nicht; Werte pro Tool-Schritt sind Schätzungen.
- **Instagram:** `insta-publisher` ist gegen einen lokalen Nachbau der Graph API getestet, **nicht gegen echtes Instagram**. Metriknamen der Insights ändert Meta gelegentlich; fehlende Werte werden weggelassen, nicht geschätzt.
- **Richtwerte:** Genre-Lautheiten (Hitech, Metal) und Plattformgrenzen sind Praxis- bzw. Richtwerte, keine Normen.
- **Windows:** `windows-helfer` schreibt Bash-Befehle um (Präfix `export PYTHONIOENCODING=…`). Das kann Erlaubnisregeln betreffen, die genau auf `python …` lauten.
- **DaVinci Resolve:** Ein Render-und-Warten-Makro ist innerhalb einer Mod nicht zuverlässig baubar, weil Wartezeit das Zeitbudget eines Hooks verbraucht. Stattdessen gibt `studio-kompass` die Resolve-Regeln vor.

## Prüfen

```bash
claude plugin validate _claude-mods            # Marketplace, Manifeste und Hooks
cd _claude-mods/<mod> && claude plugin test    # Tests je Mod (insgesamt 51)
```
