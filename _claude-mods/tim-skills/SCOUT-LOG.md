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

## 2026-10-18 – Wochenlauf lokal (nur Selbstverbesserung; letzter Lauf 15.10. < 6 Tage → keine Fremd-Suche)

Eigenbau:
| Skill | Anlass (Belege) | Test |
|---|---|---|
| agenten-schwarm | SKILL-KANDIDAT im Selbstverbesserungs-Log 15.10.; Freigabe der Orchestrierung (Session 15.10., Projekt C--) | Ladetest; Vorlagen gegen vorhandene Werkzeuge (videokontrolle.py, kanten_mms.py, codex-bridge) abgeglichen |
| sammler-kontakt | Sammler-Verhandlung und Provenienz-Recherche in Sessions 13.10., 14.10., 15.10. (Projekt C--); raritaeten-jaeger deckt nur Suche ab | `preisanker.py` mit 5 Beispielfällen (Leiter, Rundung, Fehler bei max < Start, Warnungen); Ladetest |

Offen (nur Vorschlag, nicht umgesetzt): 18 Skills doppelt in `~/.claude/skills` und tim-skills (gsap-*, ig-*) – Bereinigung bräuchte Löschen lokaler Ordner, das darf die Routine nicht.

## 2026-10-19 – Wochenlauf 3 (2 fremde aufgenommen: earshot, leonardo-colors; 2 Eigenbau: routine-waechter, routine-einrichtung; 12 aktualisiert)

Aktualisiert: ai-seo, copy-editing, copywriting, paid-ads, programmatic-seo, seo-audit, site-architecture, social-content, video-marketing
(coreyhaines31/marketingskills @365b412, 15.10.); remotion-best-practices (remotion-dev/skills @1441a11, 16.10.); core-web-vitals und web-seo
um References ergänzt, die bei der Erstinstallation fehlten (addyosmani/web-quality-skills @afa8da9).
Nicht aktualisiert: ad-creative – Upstream hat einen Werbeeinschub für das Produkt „Magister“ mit Affiliate-Link (?ref=marketingskills) in die
SKILL.md aufgenommen; bisherige Fassung bleibt.

Aufgenommen:
| Skill | Quelle | Lizenz | Prüfung |
|---|---|---|---|
| earshot | Leonxlnx/earshot @925ebe5 | MIT | SKILL.md gelesen; braucht pip-Paket earshot (lokal, CPU, Modelle gepinnt von Hugging Face); Gemini-Upload nur mit eigenem Key und ausdrücklicher Zustimmung, Skill verbietet eigenmächtiges --yes-upload |
| leonardo-colors | adobe/leonardo @eb6481d | Apache-2.0 | offizieller Hersteller; reine Anleitung, keine Skripte |

Eigenbau:
| Skill | Anlass (Belege) | Test |
|---|---|---|
| routine-waechter | ausgefallene Routine-Läufe unbemerkt: Etsy 13.10. (Wochenlimit), polished.media 13./14.10. (3× Limitfehler), Mitragyna 08./18.10. (fehlende Posts); Klartext-Token in einem Routine-Prompt (list_triggers 19.10.); stündliche Session-Routine mit sehr hohen Cache-Kosten (Wikipedia 18./19.10.) | `routinen_check.py` mit 5 Beispiel-Routinen (FAILED, überfällig, stündlich+Session, Token im Prompt, ok) und 2 Prompts; Token-Wert erscheint nie in der Ausgabe |
| routine-einrichtung | Session Geldverdienung 18.10. („wo genau?“ bei Repos, Push auf Nebenzweige, Upload von Sicherheitsprüfung blockiert); Myriad-Routine zuerst ohne Repo-Zugriff; Token per Chat in Prompt (Mitragyna 18.10.) | Prompt-Prüfung über `routinen_check.py --prompt` (schlechter Prompt: 1 Problem + 4 Hinweise; guter Prompt: ok) |

Zurückgestellt/abgelehnt:
| Skill/Repo | Grund |
|---|---|
| hed0rah/acidcat | inhaltlich passend (Vital/Serum-Presets, ACID-Tags, WAV-Reparatur), sauber, MIT – aber ein Maintainer mit 8 Sternen; beobachten |
| Leonxlnx/taste-skill | 2,5 MB, Bilder zur Laufzeit aus APIs, Überschneidung frontend-design |
| Leonxlnx/cinetic | 3,1 MB, Stil-Verbote (Neon/Glow) passen nicht, Überschneidung Remotion/GSAP |
| pycodebr/heditor | `curl … \| sudo bash` im setup.sh, ungepinntes npx |
| juliobsz/skills (awwwards) | lädt ungepinntes axe-core vom CDN zur Laufzeit, unbekannter Autor |
| DeepAleph/jevreel | Upload zu kostenpflichtiger Cloud-API |
| talsiach/take-one, liyupi/ai-promo-video-maker, calesthio/generative-media-skills | bezahlte APIs (ElevenLabs, Suno, Higgsfield) als Pflicht |
| alchaincyf/huashu-motion | 1 Tag alt, chinesische Doku, Überschneidung |
| sandraschi/reaper-mcp, dcc-mcp/dcc-mcp-reaper, FunwayHQ/sound-design-skill, pemeunier/Electronic_Music_Mentor, jmfontaine/discogskit | 0–1 Sterne bzw. MCP-gebunden |
| Fangx-AI/geo-doctor | auf chinesische KI-Plattformen ausgerichtet |
| FeedHive/ai-slop-detector, phuryn/work-humanizer | Überschneidung humanizer |
| publora/skills | automatisches Posten |
| ZiadAbdelkarim/beat-synced-edit | weiter beobachten, unverändert 13 Sterne |

Vorschläge an Tim (nicht umgesetzt, Abschnitt D):
- Routine „DRUWIDS Instagram Shorts Auto-Poster“ (abgeschaltet) enthält einen Instagram-Zugangstoken im Klartext im Prompt → Token bei Meta erneuern (alter gilt als offen), Prompt bereinigen.
- Stündliche Wikipedia-Beobachtung in derselben großen Session ist sehr teuer → frische Session pro Lauf oder seltener.
- Lokal: 18 Skills doppelt in ~/.claude/skills und tim-skills (aus Lauf 18.10.) – Bereinigung braucht Löschen, nur durch Tim.

## 2026-10-19 – Tims Hinweise (Reels/Doc, zweite Runde) – nichts Neues aufgenommen
| Skill/Repo | Ergebnis |
|---|---|
| iamzifei/show-me-the-money (25 money-*-Skills, „AI whose only job is to make money“) | abgelehnt: Lizenz CC BY-NC 4.0 (keine kommerzielle Nutzung; Tim verkauft über Gumroad/Mastering – kommerzielle Lizenz kostenpflichtig) und `money-upgrade` aktualisiert sich selbst per npm |
| Jakeschincariol/instagram-agent-skill (Google-Doc) | bereits am 15.10. aufgenommen (12 ig-*-Skills) |
| albertshiney/websitegenerator, „Autopilot 50 Accounts“, video-use | bereits abgelehnt (13./15.10.), unverändert |
| Higgsfield Katana | kein Skill nötig – Connector ist verbunden |

## 2026-10-19 – Korrektur: show-me-the-money aufgenommen (24 Skills, ohne money-upgrade)
Tim: „trotzdem nutzen … geht darum, ob die Skills gut sind und mich finanziell nach vorne bringen.“
Die Ablehnung von heute früh war falsch begründet: Laut `COMMERCIAL-LICENSE.md` des Autors ist die Nutzung für das **eigene** Geschäft und
eigenes Einkommen unter CC BY-NC 4.0 kostenlos abgedeckt. Kostenpflichtig wird es erst bei Weiterverkauf, Einbau in ein Produkt für Dritte
oder Entfernen der Namensnennung. Bedingungen: Namensnennung behalten (LICENSE.upstream, QUELLE.txt, README), das Paket nicht weiterverkaufen.
Quelle iamzifei/show-me-the-money @b1e2f9e. Geprüft: kein Upload (Zustand nur lokal unter `~/.smtm/`), Update-Check nur als Hinweis,
unsichtbare Zeichen nur Emoji-Verbinder (U+200D), Ads/Ops mit Budgetgrenze und Bestätigungspflicht für kritische Aktionen.
Nicht übernommen: `money-upgrade` (aktualisiert die Suite selbst per npm; Updates laufen über den Skill-Scout).

## 2026-10-19 – Tims Hinweise: AutoEdit (Premiere) und Claude-Code-Prompt-Bibliothek
| Hinweis | Ergebnis |
|---|---|
| AutoEdit „Content Creator Mode“ (Premiere-Plugin, nur per „Kommentiere CLAUDE“) | nicht installiert: kein öffentlicher Code/keine Lizenz, Kommentar-Köder, nur Premiere. Stattdessen Eigenbau `rohschnitt-davinci` (Rohschnitt-EDL für DaVinci aus Transkript; getestet mit deutschem Beispiel: Füllwörter, Neuansatz, 3-s-Pause erkannt, EDL-Zeitcodes lückenlos, CRLF) |
| code.claude.com/docs/en/prompt-library | keine Installation (Kopiervorlagen, überwiegend Softwareentwicklung); passende Prompts Tim direkt genannt |

## Bereinigung 2026-10-20 (Setup-Inventur, Freigabe Tim)
Entfernt, weil inhaltsgleiche Kopien von Plugins, die als Werkzeug-Plugin aktiv bleiben, oder ungenutzt (0 Aufrufe in 30 Tagen) mit besserem Ersatz:
hyperframes-audio, hyperframes-core, hyperframes-keyframes, hyperframes-studio, figma, remotion-to-hyperframes, slideshow (→ Plugin hyperframes),
bunshin, cast (→ Plugin genjutsu), codex-cli-runtime, codex-result-handling (→ Plugin codex), brag-slim (→ Plugin brag), claude-real-video (→ Plugin claude-real-video),
agent-development, skill-development, claude-automation-recommender, claude-md-improver, math-olympiad, playground (ungenutzt; skill-creator/plugin-authoring vorhanden),
humanizer (ungenutzt; ig-human und humanizer-de decken das ab). Nicht erneut aufnehmen. Beleg: C:/selbstverbesserung/setup-inventur-2026-10.md
