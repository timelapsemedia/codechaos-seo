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
