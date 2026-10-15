# Skill-Scout – Logbuch

## 2026-10-07 – Erstauswahl (30 Skills installiert, siehe README.md)

Abgelehnt:
| Skill/Repo | Grund |
|---|---|
| zubair-trabzada/geo-seo-claude | Installation per `curl … \| bash`, Skill aktualisiert sich selbst per git clone |
| ericosiu/ai-marketing-skills | Telemetrie-Skript in jedem SKILL.md-Vorspann, stille Netzwerk-Versionsprüfung |
| browser-use/video-use | lädt Audio zu ElevenLabs hoch, schreibt API-Key in .env |
| ScrapeCreators/social-media-research-skills | benötigt kostenpflichtigen API-Key |
| AgriciDaniel/claude-seo | sehr viele Skripte, eigene Hooks und Installer; Überschneidung mit marketingskills |
| adamjmurray/producer-pal: ableton-analyze-audio | durchsucht .env nach Google-Keys, lädt Audio zu Google hoch |
| Spartan-Game-Studios/reaper-mcp-mac | keine Lizenz |
| mikecfisher/ableton-lom-skill | keine Lizenz |
| heygen-com/skills | kostenpflichtige Avatar-API, Update-Check-Skript |
| typefully/agent-skills | kein Instagram/TikTok |
| nexscope-ai Shop-Stubs (außer etsy-seo) | inhaltsleere Platzhalter mit Werbelinks |
| anthropics/skills: canvas-design | ca. 5 MB Schriften (zu groß) |
| glincker/ableton-skills, Korben00/ableton-producer-skills | generisch, wenig gepflegt (ggf. erneut prüfen) |
| bitwize-music-studio/claude-ai-music-skills: mastering-engineer | an eigenen MCP-Server/Suno-Pipeline gebunden |

## 2026-10-07 – Wochenlauf 1 (3 aufgenommen: accessibility, gsap-utils, gsap-performance; keine Updates bei den 30 vorhandenen)

Zurückgestellt:
| Skill/Repo | Grund |
|---|---|
| mblode/agent-skills: typography-audit | sauber, MIT; aber 82 Dateien und englische Anführungszeichen-Regeln (falsche Funde bei deutschen Texten) – ggf. später |
| mblode/agent-skills: ui-animation | sauber, aber starke Überschneidung mit GSAP-Paket, braucht OpenCV/SciPy |
| coreyhaines31/marketingskills: influencer-marketing | Überschneidung mit druwids-outreach und social-content |

Abgelehnt:
| Skill/Repo | Grund |
|---|---|
| mvanhorn/printing-press-library: pp-discogs | ungepinnte Go-Binary per `go install @latest`, Hintergrund-Lernvorgang, Notizen fließen zurück ans Projekt |
| jmfontaine/agent-discogs, Nikolasgrizli/discogs-api-skills u. a. Discogs-Treffer | Kleinstprojekte/Sammelkopien, keine seriöse Quelle |
| timcase/agent-skills musicbrainz, chrischall/musicbrainz-mcp | 1 Stern bzw. eigener MCP-Server nötig |
| VerkCoding/ReaperSkillsForClaude, mthines/reaper-mcp, onliner10/AutoReaper, c4m3r0nn/Reaper-Agent, DDDPG/Rea-Cli | 0–3 Sterne, eigene MCP-Server/Installer |
| Mastering-Treffer (ruflo music-master, Registry-Kopien) | Kopien bereits abgelehnter Skills / anonyme Sammel-Repos |
| vercel-labs/agent-skills: web-design-guidelines | lädt Regeln bei jedem Lauf per WebFetch nach (fernsteuerbar), keine LICENSE |
| sanity-io: seo-aeo-best-practices | Überschneidung mit ai-seo, schema-markup, seo-audit |
| remotion-dev/skills: remotion-captions, remotion-multimedia | bereits in remotion-best-practices enthalten |
| coreyhaines31/marketingskills: image | Ratgeber für bezahlte Bild-KIs, wenig Mehrwert |
| addyosmani/web-quality-skills: best-practices, web-quality-audit | geringer Mehrwert, Audit ist Dach über installierte Skills |
| google-labs-code/stitch-skills | an Google Stitch gebunden bzw. doppelt mit frontend-design |

## 2026-10-12 – Wochenlauf 2 (4 aufgenommen: good-css, yt-retention, yt-package, yt-edit; 9 aktualisiert)

Aktualisiert (coreyhaines31/marketingskills @1efedbc, 2026-10-08, MIT): ad-creative, ai-seo, content-strategy, copy-editing, cro, paid-ads,
schema-markup, seo-audit, social-content – SKILL.md, References, Evals vollständig übernommen; LICENSE.upstream ergänzt. Diffs geprüft:
keine Netzaufrufe/Telemetrie, HTML-Vorlage ad-creative ohne externe Skripte.

Nicht aktualisiert:
| Skill/Repo | Grund |
|---|---|
| remotion-dev/skills: remotion-best-practices (Update 2026-10-07) | Repo hat keine LICENSE-Datei (Kriterium 1); Bestandskopie ist ebenfalls ohne Lizenz – von Tim zu entscheiden |

Abgelehnt/zurückgestellt:
| Skill/Repo | Grund |
|---|---|
| diffusionstudio/lottie: text-to-lottie | sauber, MIT; setzt aber Player per `npx degit` (ungepinnt, jeweils neuester Stand) + `npm install` voraus – zurückgestellt |
| dreamrec/LivePilot | Business Source License 1.1 |
| adrianeyre/soundcheck | an eigene DAW-App gebunden, keine LICENSE-Datei |
| JefroB/Electronic-Music-Genre-Skills | keine Lizenz („personal and educational use“) |
| whi-rik/claude-skills | keine LICENSE, HISE-/interne Skills |
| countrymanprime/narration-utils: reaper-api-facts | repo-intern, nicht eigenständig |
| ZiadAbdelkarim/beat-synced-edit | passend, aber Ein-Personen-Repo (13 Sterne), Skripte außerhalb des Skill-Ordners, Chart.js ungepinnt vom CDN – beobachten |
| nolangz/pixel2motion | geringer Mehrwert, Werbe-/Verifizierungsdateien im Ordner |
| EGSECDA/vocaloid-style-mv-pipeline | Nische, lädt ~260 MB Fonts und Fremd-Repo nach |
| kaankiziltug/logo-design-skill | 14 MB, fremde Marken-SVGs nicht unter MIT |
| howseen-ai/claude-motion-design | Firmen-Pipeline mit Client für externen Dienst |
| Barty-Bart/motion-graphics | SaaS-Explainer-spezifisch, braucht SAM 2 |
| iart-ai/kinetic-typography-skills | kleiner Anbieter, ungepflegt, Überschneidung mit gsap-plugins |
| greensock: gsap-react, gsap-frameworks | nur für React/Vue-Projekte – bei Bedarf |
| VoltAgent-Neuzugänge (cutaway, upload-post, atomicmail, unbrowse …) | themenfremd, Auto-Posting oder gehostete API |

## 2026-10-13 – Tims Hinweise aus Facebook (7 aufgenommen: yt-audit, yt-chapters, yt-comment, yt-plan, yt-script, yt-seo, yt-viral)

Quelle der Hinweise: vier Facebook-Posts/Reels, die Tim geschickt hat. Aufgenommen aus Jakeschincariol/youtube-agent-skill @a2feb21 (MIT),
gleiche Quelle wie yt-retention/yt-package/yt-edit; alle Dateien gelesen, nur Markdown bzw. Python-Standardbibliothek, nichts wird veröffentlicht.

Abgelehnt:
| Skill/Repo | Grund |
|---|---|
| tejashmakwana/motionmaxxing | voice.py/providers.sh durchsuchen `./.env`, `~/.elevenlabs` und `~/.claude.json` nach Schlüsseln (auch beliebige `api_key=`-Zeilen), schicken sie an ElevenLabs; Bildgenerierung über `codex exec`; Logos per `simple-icons@latest`; 26 MB (ohne Medien ca. 5 MB) |
| Jakeschincariol/youtube-agent-skill: yt-shorts | doppelt mit installiertem `shorts` (der zusätzlich rendert) |
| REA „Reverse Engineer Anything“ (MCP) | kein Skill für Tims Arbeitsfelder; beworbener Zweck ist das Nachbauen kostenpflichtiger Software (TradingView-Premium) |
| aicertified.free / „Google-Zertifikate per Codex“ | kein Skill, sondern Anleitung, Online-Prüfungen von einer KI ablegen zu lassen; fremde Anmeldung über Drittseite |

## 2026-10-15 – Tims Hinweise (12 aufgenommen: ig-audit, ig-caption, ig-carousel, ig-comment, ig-dm, ig-plan, ig-profile, ig-reel, ig-reply, ig-repurpose, ig-story, ig-viral)

Quelle: Google-Doc „Claude Instagram Agent Skill“ (von Tim geschickt) → Jakeschincariol/instagram-agent-skill @d03c56b (MIT), gleicher Autor wie die yt-Skills.
Alle Dateien gelesen: Markdown bzw. Python-Standardbibliothek, keine Netzaufrufe, postet/sendet nichts, verbietet Scraping und Logins im Namen des Nutzers.
Skripte (caption.py, swipe.py) mit Beispieldaten ausgeführt. Die Vosu-AI-Werbung im Dokument ist nicht Teil des Skills.

Abgelehnt:
| Skill/Repo | Grund |
|---|---|
| instagram-agent-skill: ig-human | doppelt mit `humanizer`; wandelt typografische Anführungszeichen („…“) in gerade um – falsch für Deutsch |
| albertshiney/websitegenerator | keine LICENSE; füllt automatisch Kontaktformulare fremder Firmen mit Werbenachricht (submit_by_default), Firecrawl-Key aus .env |
| „Claude-Autopilot, 50 Accounts“ (jayantcreates) | kein Projekt, nur Kommentar-Köder; Mehrfach-Accounts mit Auto-Posting verstoßen gegen Instagram-Regeln |
| Higgsfield Katana | kein Skill nötig – Higgsfield ist als Connector bereits verbunden (kostenpflichtige Credits) |
| browser-use/video-use (erneut gesehen) | bleibt abgelehnt (ElevenLabs-Upload, Schlüssel in .env) |
