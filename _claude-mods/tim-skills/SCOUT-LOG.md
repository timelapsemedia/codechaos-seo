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

## 2026-10-27 – Wochenlauf 4 (nachgeholt vom 26.10.) + Ausdünnung (Freigabe Tim)
Neu aufgenommen: keine. Kandidatensuche ohne Treffer, der alle Kriterien erfüllt und Mehrwert bringt (VoltAgent-Neuzugänge themenfremd; ComposioHQ/travisvn/anthropics unverändert; keine Hersteller-Skills für Splice/iZotope/Ableton/NI/Cockos/MetaBrainz).
Beobachten: jamcgrath/music-theory-skill (MIT, sauber, MIDI-Prüfung; 1 Stern), Akurganow/sound-to-patch (Vital/Serum-Presets, noch ohne SKILL.md), hed0rah/acidcat (weiter 8 Sterne), ZiadAbdelkarim/beat-synced-edit (14 Sterne).
Abgelehnt: RandyHaylor/audio-and-vocal-mastering (keine LICENSE), JonoGitty/claude-composer-reaper (2 Sterne, Anfängerniveau), kajisho5/audio-production-skill (doppelt mit ffmpeg), tubone24/midi-agent-skill (ungepflegt), SJY051/music-composition (2,3 MB).
Hinweis: iamzifei/show-me-the-money ist nicht mehr öffentlich erreichbar (404) – lokale geprüfte Kopie bleibt, keine Updates mehr.
Updates: zurückgestellt bis nach der Ausdünnung (nächster Lauf), betroffene Quellen u. a. coreyhaines31/marketingskills, remotion-dev/skills, lottie.

Nutzung 19.–26.10. (18 Cloud-/Remote-Control-Sessions, Stichprobe): 1 Aufruf aus tim-skills (etsy-seo). Ursache vermutlich das überlaufene Beschreibungs-Budget (147 Skills, 67.400 Zeichen > ~30.000).
Ausgedünnt: 76 Skills nach _papierkorb/tim-skills-2026-10-27/ (git mv, wiederherstellbar): 19 money-* (Kern money/-diagnose/-strategy/-product/-finance bleibt), 8 doppelte ig-* (sergebulaev), alle fb-*, threads-*, tt-*, 18 seo-* (AgriciDaniel; seo-audit, seo-google bleiben), SaaS-Marketing (churn-prevention, cold-email, customer-research, events, influencer-marketing, product-marketing), paid-ads, cro, gsap-utils/-performance/-timeline/-plugins, shorts.
Eigene Beschreibungen gekürzt: routine-waechter, routine-einrichtung, rohschnitt-davinci, sammler-kontakt. Ergebnis: 70 Skills, 29.832 Zeichen.

## 2026-10-27 – Tims Hinweise (3 aufgenommen: hook-master, design-to-motion, hallmark; copywriting/copy-editing ergänzt)

Nur die vier von Tim genannten Kandidaten geprüft, keine allgemeine Fremd-Suche. Alle Dateien gelesen, Skripte auf Netzaufrufe/Hooks/Schlüssel durchsucht, unsichtbare Zeichen geprüft.
Lief parallel zur Ausdünnung desselben Tages (PR #61, 70 Skills). Damit das Beschreibungs-Budget (~30.000 Zeichen) hält, sind die Beschreibungen der drei neuen Skills kurz gehalten und die von copywriting/copy-editing gekürzt: Summe danach ca. 28.800 Zeichen (73 Skills), also weniger als vorher. tt-hook-scripter, ig-hook-extractor und shorts sind seit #61 im Papierkorb; hook-master deckt die Hook-Arbeit für Shorts damit allein ab.

Aufgenommen:
| Skill | Quelle | Lizenz | Prüfung / lokale Anpassung |
|---|---|---|---|
| hook-master | Liamrjohnston/hook-master-skill @287053a (v1.1.0) | MIT | reines Markdown, keine Netzaufrufe; neu (25.10., 6 Sterne), aber Inhalt sauber und ehrlichkeitsorientiert (keine erfundenen Zahlen/Trends/View-Versprechen). Überschneidung: tt-hook-scripter (schreibt Hooks neu), ig-hook-extractor (analysiert fremde Hooks), yt-retention (Retention-CSV), ig-viral/shorts – hook-master ist der einzige, der ein vorhandenes Video-Opening diagnostiziert und gegen das Material repariert. Die 9 Upstream-Skills zu EINEM Skill gebündelt (Router + `stages/*.md`), damit nur eine Beschreibung dauerhaft im Kontext steht; Abschnitt „Tims Regeln“ (Social Media Rules 2026, 1,5-s-Hook dreischichtig, DRUWIDS-/Mitragyna-Gate inkl. konsum_gate.py, keine Zitatfragmente, Endkontrolle, A/B über social-insights). install.sh nicht übernommen |
| design-to-motion | elayadesign/ai-design-skills @5e57840 | MIT | reines Markdown; Figma-Token nur aus Umgebung/Schlüsselbund. Neu gegenüber hyperframes/brag/motion-design/gsap-*: pixelgenaue Rekonstruktion aus Figma/Screenshot, deterministische Bildaufnahme, PSNR-, Überlauf- und Nahtprüfung, Export MP4/GIF – passt zu Plugin-GUI-/Dashboard-Showcases. Beschreibung gekürzt (Kontextkosten), „Tims Hinweise“ (9:16, Social-Regeln, DRUWIDS) ergänzt |
| hallmark | Nutlope/hallmark @7ec8682 (v2.0.0, Together AI, ~37 000 Sterne) | MIT | Das Posting von @rammcodes zeigt dieses Repo (v2.0.0 im plugin.json). Klar neu gegenüber frontend-design/genjutsu: `sloplint` (mechanische Prüfung auf KI-Muster, statisch + optional gerendert), 48 Themes, Seitenaufbau nach Zweck, Wikimedia-Fotobibliothek mit Nachweisen. Getestet: `sloplint.mjs` auf Beispiel `slopped.html` (24 FAIL erkannt), `theme.mjs deal` ohne Bilder ok, `refcheck.mjs` sauber. NICHT übernommen: `references/themes/*.jpg` (~5 MB, Theme-Bilder optional, würden cloud-setup.sh verdreifachen), `install.mjs` (kopiert in ~/.claude/skills usw. → Dublette), `install-hook.mjs`/`lint-hook.mjs` (schreibt PostToolUse-Hook in settings.json – Hooks nie über Skills), `agents/` (Codex). `imagegen.mjs` (Together AI) bleibt: nur mit gesetztem TOGETHER_API_KEY und ausdrücklichem Wunsch; Hinweise in `references/tim-hinweise.md` |

Abgelehnt:
| Skill/Repo | Grund |
|---|---|
| elayadesign/ai-design-skills: landing-page-design | Überschneidung copywriting/cro/frontend-design/hallmark; zu breite Auslöser („ANY … web UI, component … even when the user does not mention design“) würden jede Webarbeit übernehmen; starre Hausregeln passen nicht (verbietet Inter, Pflicht-Tagline-Sektion, „no hyphens in text“ – falsch für deutsche Komposita); „Content realism“ verlangt erfundene Testimonials mit vollen Namen und erfundene Kundenlogos (UWG-Risiko, widerspricht Tims Belegregel) |

Ergänzt (eigene Worte, keine Zitate):
| Skill | Was |
|---|---|
| copywriting | `references/klassiker.md`: Schwartz-Bewusstseinsstufen + Marktreife, Headline nach Nutzen/Neuigkeit/Neugier (Caples/Ogilvy), Rutschbahn (Sugarman), Reason why (Hopkins), Cialdini-Hebel fair/tabu, Markt vor Formulierung (Halbert), Prüfliste, Grenzen für DRUWIDS (keine Superlative/Wettbewerbsvergleiche/Konsumaussagen), Mitragyna, Gesundheits-Kundenreels. Vorher nur Bewusstseinsstufen in ad-creative abgedeckt, Rest fehlte. Je ein Verweis in copywriting/copy-editing SKILL.md |

## 2026-10-28 – Wochenlauf lokal (nur Selbstverbesserung; letzter Lauf 27.10. < 6 Tage → keine Fremd-Suche)

Eigenbau:
| Skill | Anlass (Belege) | Test |
|---|---|---|
| stock-sichtung | SKILL-KANDIDAT „Rauch-/Glut-Gate für DRUWIDS-Stock“ im Selbstverbesserungs-Log 27.10. (Routine motion-reels-nachschub: Rauchfäden eines Pexels-Clips erst im 100-%-Ausschnitt sichtbar, Reel verworfen); Routine druwids-shorts-nachschub 27.10. (Fremdmarke, Einblendung, Abspanntafel in B-Roll); ARTE-Reel (Texttafeln/Rauch im Fremdmaterial, Memory arte_reel_druwids) | `sichtung.py` mit zwei Testclips (3840×2160 und 1080×1920, Name mit Leerzeichen): 4K → 1920×1080 + 4 Lupen in Quellauflösung, Hochkant unskaliert; Gate: ungesichtet → Exit 1, Freigabe ohne Sichtung abgelehnt, gesperrt → Exit 1, freigegeben → Exit 0, Datei danach geändert → „GEÄNDERT“, Exit 1; Ladetest |

Bewusst ohne CLIP/Bildmodell: Erkennung über Claudes Sichtung der Vollbilder (Read), damit keine Modelle/Pakete nötig sind; Beschreibung kurz gehalten (Budget ~30.000 Zeichen).
Nicht als Skill (Vorschläge an Tim, Pipeline-Code): globale Render-Sperre in motion.py rendern() (Log 27./28.10.), Lock-Datei in bauen_r3.py, Polished-Sitemap-Strukturtest.

## 2026-11-01 – Wochenlauf lokal (nur Selbstverbesserung; letzter Lauf 28.10. < 6 Tage → keine Fremd-Suche)

Zwei Kandidaten aus dem Selbstverbesserungs-Log (grok-dirigent 01.11.) gezielt geprüft, beide abgelehnt:
| Repo | Grund |
|---|---|
| kajisho5/ffmpeg-skill (MIT, 4.224 Sterne, v3.1.1) | Kein belegter Mehrwert gegenüber ffmpeg, auto-editor, video-werkstatt und Tims Pipelines. Auslöser greift bei jeder Video-/Audiodatei und verbietet rohes ffmpeg, das konkurriert mit Tims Schnitt-Pipelines. Gelesen: SKILL.md, plugin.json, bin/install.js; die 58 Dateien unter scripts/ nicht auditiert |
| jordanrendric/claude-video-vision (MIT, 1.444 Sterne) | Kein Skill, sondern MCP über `npx -y claude-video-vision@latest` (zieht bei jedem Start die neueste Version). Doppelt mit claude-real-video und video-werkstatt |

Eigenbau:
| Skill | Anlass (Belege) | Test |
|---|---|---|
| ki-medien | SKILL-KANDIDAT im Selbstverbesserungs-Log 28.10. (Higgsfield gekündigt, Routing stand nur in CLAUDE.md und MCP-Texten); Tims Korrektur 28.10. zu Gratis-Ersatz | `ki.py kosten`, `mockup.py --liste`, Bezahlaufrufe nanobanana2 und veo-lite gegen Deckel 0 $ (Budget-Gate, Exit 1, keine Datei, keine Kosten); Ladetest |

Verbessert: higgsfield-upload als überholt markiert (Beschreibung gekürzt), stock-sichtung und motion-reels ohne Higgsfield-Bezug.
Nicht als Skill (Vorschlag an Tim): higgsfield-upload nach _papierkorb verschieben.

## 2026-11-02 – Wochenlauf 5 (Cloud): keine neuen fremden Skills, 11 Updates, 2 Eigenbau

Neu aufgenommen: keine. Kein Kandidat seit 27.10. erfüllt alle Kriterien mit echtem Mehrwert (VoltAgent-Neuzugänge themenfremd/Auto-Posting; ComposioHQ/travisvn unverändert; anthropics nur mcp-builder).
Abgelehnt: mthines/jsfx-agent-skills (keine LICENSE-Datei, 4 Sterne, JSFX statt ReaScript), sb-dev/music-production-skills (Pflicht-Replicate-Key), crunkkid411/midi-agent-skill (Fork, 0 Sterne, eigene settings.json), m4bwav/musicwright (0 Sterne, Selbst-Refresh, Überschneidung audio-labor/earshot), hodgemann/mondo-music-video (33 MB Web-App), ClawHub-/claudskills-Registry-Kopien.
Beobachten (Grund nicht erledigt): Akurganow/sound-to-patch (SKILL.md jetzt vorhanden, aber 0 Sterne, nur Vital, eigenes Rust-Binary), jamcgrath/music-theory-skill, hed0rah/acidcat, ZiadAbdelkarim/beat-synced-edit.

Aktualisiert: ai-seo, content-strategy, copy-editing, programmatic-seo, seo-audit, social-content, video-marketing (marketingskills @88c79f6), earshot (@591fa3e), producer-pal (@8a9cfff), seo-google (claude-seo @6be93f4), remotion-best-practices (@30d4553). Gekürzte Budget-Beschreibungen bei copy-editing und earshot behalten.
Nicht aktualisiert: ad-creative (Upstream weiter mit Affiliate-Werbung „Magister“), copywriting und hallmark (lokale Ergänzungen/Abwandlungen), show-me-the-money (Upstream 404).

Nutzung 27.10.–02.11. (17 Remote-Sessions): 0 Aufrufe aus tim-skills (Vorwoche 1). Die Ausdünnung allein bringt keine messbare Nutzung.

Eigenbau:
| Skill | Anlass (Belege) | Test |
|---|---|---|
| zugang-einbinden | API-Schlüssel im Chat + lange Umwege beim Einbinden (Setup-Inventur 27.10., Meta Muse 29.10., Grok Bot 01.11.) | Ladetest; Ablauf gegen die drei Fälle geprüft (EU-Sperre, Abo≠API, CLI-Sperre) |
| bewerbung-zuschnitt | Lebenslauf/Anschreiben mit bis zu 6 Korrekturrunden (Kündigungsprozess 28.10., 30.10.), Jobsuche ab 03.11. | Ladetest; Regeln aus Tims Korrekturen übernommen |
Verbessert: routine-einrichtung (Konnektoren beim Anlegen ausdrücklich begrenzen; belegt 29.10.).

Vorschläge an Tim (nicht umgesetzt): higgsfield-upload in den Papierkorb (überholt, lief 28.10. noch als Skript); DRUWIDS-Endkontrolle (Konsum-/Etikett-Gate + Telegram-Freigabe) von lokalen Skripten als Skill für Cloud-Sessions verfügbar machen (braucht Zugangsdaten/Posten → Tims Entscheidung); Windows-Bash-Wrapper-Fehler „line 85 unexpected EOF“ bei verketteten Befehlen/Temp-Pfaden (15× am 27.10.) im Mod windows-helfer abfangen.

## 2026-11-07 – Sonderlauf lokal: skills.sh (Vercel, „The Agent Skills Directory“) auf Tims Hinweis

Auftrag Tim (07.11.): „Installiere global für alle sessions alles was davon sinnvoll für meine projekte und arbeit ist und wende selbst vollautonom an wenn sinnvoll“. Durchsucht über die öffentliche Suche von skills.sh (rund 110 Suchbegriffe aus allen Arbeitsfeldern, Bestenliste, Liste „Official“). Ergebnis: Die meistinstallierten passenden Skills sind schon da (remotion, gsap, lottie, threejs, marketingskills, hyperframes, auto-editor, firecrawl, earshot, manim, frontend-design, pdf/docx/pptx …). Zwei echte Lücken geschlossen. DRUWIDS/keinduftbaum/Mitragyna bewusst ausgenommen (Projektende 30.11.).

Aufgenommen:
| Skill | Quelle | Lizenz | Prüfung / lokale Anpassung |
|---|---|---|---|
| gemini-api-dev | google-gemini/gemini-skills @7cfc690 (05.11.2026), offiziell | Apache-2.0 | reines Markdown (SKILL.md + references/migration.md), nur Links auf aistudio.google.com/github.com, keine unsichtbaren Zeichen. Mehrwert: aktuelle Modellnamen und Interactions-API für ki.py, ki-rat, hitech-listen (bisher nur Wissen aus Memory). Beschreibung deutsch gekürzt, „Tims Hinweise“: Gratisstufe (Pro/Omni/Deep Research 429, gemessen 01.11.), Schlüssel nur aus Claude-Keys, Deckel für Bezahlmodelle, `store=False` für Kunden-/unveröffentlichtes Audio, 429 laut behandeln. gemini-interactions-api und gemini-live-api-dev nicht übernommen (gemini-api-dev deckt den Bedarf, Budget) |
| audio-plugin-review | kunitoki/sonic-skills @8b6dcfe (23 Sterne, Autor von popsicle/YUP) | Unlicense | 5 Skills (juce-review, audio-dsp-review, vst3-review, audio-numerics-review, audio-artifacts-debug) unverändert als `stufen/*.md` + references/ zu EINEM Skill gebündelt (Muster hook-master); reines Markdown ohne Netzaufrufe. Mehrwert: es gab keine Prüfung für Tims JUCE-Plugins (BM-Suite, Chaos FM, Crucible; Code Chaos Audio auf Gumroad). Deutscher Einstieg mit Tims Pfaden und Messpflicht (pedalboard/audio-labor) |

Budget: 3 überlange Upstream-Beschreibungen deutsch gekürzt (ad-creative, social-content, ai-seo, je ~1.000 → ~260 Zeichen). Summe 30.237 → 28.457 Zeichen bei 81 statt 79 Skills.

Abgelehnt:
| Skill/Repo | Grund |
|---|---|
| shortwavlabs/agent-skills (juce-plugin, dsp, faust-dsp …) | keine LICENSE-Datei |
| maystudios/claude-skills audio-to-midi | `transcribe.py` installiert fehlende Pakete per pip und lädt ein Modell von zenodo ohne Rückfrage; MIDI-Export hat Tim schon in korpus/dossier.py |
| bitwize-music-studio mastering-engineer/mix-engineer | Anfängerniveau („-14 LUFS überall“) gegen Polished-Engines; hängt am eigenen MCP-System, 7 MB |
| calesthio/generative-media-skills audio-mixing-mastering | gut belegt, aber doppelt mit audio-labor, ffmpeg-normalize und Tims Lautheitsregeln |
| emilkowalski/skills review-animations | nur Web-UI-Animation, `disable-model-invocation` (nie autonom), Überschneidung motion-design-critique |
| philtzjp/skills m4l-project | japanisch, Max for Live nutzt Tim nicht |
| higgsfield-ai/skills higgsfield-youtube-thumbnail | Higgsfield gekündigt (28.10.) |
| recoupable/release-management | keine Lizenz, 1 Stern |
| mikecfisher/ableton-lom-skill | keine Lizenz; ableton-lom ist schon installiert |
| glincker/ableton-skills, korben00/ableton-producer-skills | Anfänger-Rezepte, doppelt mit producer-pal und Tims Hitech-Wissen |
| mattpocock/skills (diagnosing-bugs, tdd, research), pbakaus/impeccable, leonxlnx/taste-skill, resciencelab seo-geo, theclaymethod/unslop | doppelt mit systematic-debugging/verification-before-completion, hallmark/frontend-design, ai-seo, ig-human/humanizer-de |
| mvanhorn/last30days-skill | 3,7 MB, gebündelter X-Scraper; Trendrecherche läuft über Grok |
| digitalsamba/claude-code-video-toolkit | 25 MB, doppelt mit ffmpeg/remotion/ki-medien |

Hinweis: Die API `skills.sh/api/v1/*` braucht ein Vercel-OIDC-Token; die öffentliche Suche `skills.sh/api/search?q=` geht ohne, drosselt aber (429 nach ~25 Anfragen, Abstand ≥ 4 s). Künftige Scout-Läufe können skills.sh als Quelle in Schritt 2 nutzen. Tim hat das am 07.11. freigegeben („Ja, aufnehmen“): skills.sh steht jetzt fest in SCOUT.md Schritt 2.

## 2026-11-08 – Wochenlauf lokal (nur Selbstverbesserung; letzter Lauf 07.11. < 6 Tage → keine Fremd-Suche)

Neu aufgenommen (fremd): keine (Suche übersprungen, Sonderlauf skills.sh am 07.11.).

Eigenbau:
| Skill | Anlass (Belege) | Test |
|---|---|---|
| hitech-produktionsstandard | SKILL-KANDIDAT „hitech-produktionsstandard“ (Selbstverbesserungs-Log 04.11., Tim: „alle Learnings von Kyrie global“) und „palette-bauen“ (Log 03.11.); Katalog-Nachzug Wiedergänger/Grown in Rain mit den neuen Learnings (Session 08.11.). Beide Kandidaten zu einem Ablauf-Skill gebündelt. Weil das Repo öffentlich ist, stehen nur Ablauf und Pfade drin; Zahlen und Rezepte bleiben in C:/hitech-lab/knowledge/ | alle genannten Dateien/Werkzeuge lokal vorhanden (ls), keine Steuerzeichen, Ladetest 82 Skills |

Verbessert: code-chaos-toolkit verweist für Ablauf und Gates auf hitech-produktionsstandard.
Offen gelassen: SKILL-KANDIDAT „Ohr-Fallback lokal (CLAP/MERT)“ (04.11.) – braucht Modell-Download und ist ein Werkzeug, kein Skill → Vorschlag an Tim.

## 2026-11-09 – Wochenlauf 6 (Cloud-Routine)

Fremd-Suche: übersprungen – Sonderlauf skills.sh am 07.11. (< 6 Tage).

Upstream-Updates: earshot, remotion-best-practices, social-content (lokal gekürzte Beschreibungen behalten).
Nicht aktualisiert: ad-creative (Upstream enthält Magister-Affiliate-Werbung), copywriting, hallmark, gemini-api-dev (lokale Änderungen), design-to-motion (Upstream-Ordner fehlt), show-me-the-money (404).

Nutzung tim-skills 02.–09.11. (Cloud-Sessions): 2 Aufrufe, beide ki-medien.

Eigenbau:
| Skill | Anlass (Belege) | Test |
|---|---|---|
| fremdvideo-analyse | Video-Links zur Analyse: Sessions „Automatisierte Geldverdienung“ 03.11. und 08.11., „YouTube-Videoanalyse“ 08.11.; Abruf in der Cloud scheiterte, Vorgehen jedes Mal neu | verweist nur auf vorhandene Werkzeuge (video-werkstatt analysieren/standbilder/transkribieren, hook-master, ig-reel, yt-script) |
| session-suche | 06.11.: Fragen nach Inhalten anderer Sessions in „Automatisierte Geldverdienung“ und „Kündigungsprozess“ | list_sessions/list_events in dieser Session benutzt; Grep-Befehle lokal geprüft |

Verbessert: routine-waechter – `routinen_check.py --verlauf laeufe.json` meldet ROT bei ≥ 3× gleichem Fehler in Folge, GELB bei ≥ 5× „nichts Neues“ im Stundentakt (Anlass: Etsy-Routine 6/6 Läufe Token ungültig/0 Listings trotz SUCCEEDED; Wikipedia 28× „nichts Neues“). Getestet mit Beispieldaten (ROT/GELB/OK, Exit 2).

Vorschläge an Tim (nicht umgesetzt, SCOUT.md D):
- higgsfield-upload (überholt seit 28.10.) in `_papierkorb/` verschieben – liegt noch in skills/.
- Etsy-Routine: Token erneuern oder Routine pausieren (6/6 Läufe ohne Daten).
- Wikipedia-Beobachtung: täglich statt stündlich.
- Skill „Gründungs-/Behörden-Korrespondenz“ – erst bei zweitem Beleg bauen.
- Autonomie-Regel als Hook/CLAUDE.md-Eintrag; Render-Warteschlange für lange Videojobs.

## 2026-11-10 – Sonderlauf Trend-Liste (lokal, Setup-Inventur-Session)

Anlass: Tim schickte die Grafik „Fastest Trending GitHub Repos“ (Charlie Hills, 06.11.2026, 23 KI-Repos) und zwei Social-Posts (Content-Pipeline mit Apify/vidIQ/Whisper/ffmpeg/Remotion; „Claude als Ads-Maschine“ mit Meta Ad Library). Auftrag: „Implementiere was sinnvoll ist“ und Dauerfreigabe „Installiere immer neue mods, skills, skills.sh github usw alles was dich verbessert“ (steht jetzt in SCOUT.md). Sternzahlen per GitHub-API geprüft, alle echt.

Aufgenommen:
| Skill | Quelle | Lizenz | Prüfung |
|---|---|---|---|
| security-audit | cloudflare/security-audit-skill @c1c8a8c (14.09.2026), 68 k Sterne | MIT | 15 Markdown-Dateien + report-schema.json + 2 Validatoren (.cjs, nur `fs`/`path`/`util`, kein Netz, kein `child_process`); keine unsichtbaren Zeichen; 260 KB. Mehrwert: gründlicher als `/security-review` (Gegenprüfung je Fund), passend für Tims Python-Routinen mit Tokens und die Webseiten. Beschreibung deutsch, Testdateien weggelassen. Viele Subagenten → nur auf Zuruf voll laufen lassen. |

Abgelehnt:
| Repo | Grund |
|---|---|
| morluto/rea | Reverse Engineering von Binaries, kein Arbeitsfeld |
| obra/superpowers | 14 Skills überwiegend doppelt (systematic-debugging, verification-before-completion, writing-plans ≈ planning-and-task-breakdown); SessionStart-Hook lädt bei jedem Start Text nach |
| affaan-m/ECC (everything-claude-code) | 71 Agents, 314 Skills, Hook-Katalog – Gegenteil von „Setup schlank“; nützlicher Teil ist mit ecc-security-checklist schon da |
| deepseek-ai/deepseek-harness, anomalyco/opencode, stablyai/orca, pingdotgg/t3code | eigene Agenten/Oberflächen, keine Skills |
| multica-ai/andrej-karpathy-skills | keine Lizenz; die vier Regeln (Annahmen nennen, einfach, chirurgisch, zielgetrieben) stehen inhaltlich schon in CLAUDE.md/incremental-implementation |
| DietrichGebert/ponytail | doppelt mit Karpathy-Regeln/simplify |
| Graphify-Labs/graphify | 50-KB-Skill, Dokument-Durchlauf über LLM, Nutzen nur für große Code-Repos |
| thedotmack/claude-mem | Hooks auf jedem Tool-Aufruf, Telemetrie standardmäßig an, Bun-Worker + Chroma; eigenes Memory-System vorhanden |
| Panniantong/Agent-Reach | liest Social-Plattformen über die eingeloggte Chrome-Sitzung (Kopie der Login-Daten), Autor rät selbst zum Zweitkonto → Sperrgefahr; Apify/Firecrawl vorhanden |
| debpalash/VoiceStudio | App (AGPL), große Modell-Downloads; ElevenLabs/Kokoro vorhanden – bei Bedarf separat prüfen |
| tt-a1i/archify, cathrynlavery/diagram-design | Diagramme: Wunsch statt Lücke, artifact-diagramming/Figma-Diagramme vorhanden; 19–31 KB Skill |
| bilawalsidhu/gods-eye-view, HKUDS/DeepTutor | Apps ohne Bezug |
| Matt Pocock Skills, Taste Skill, Impeccable | schon am 07.11. abgelehnt; HyperFrames, Hallmark installiert |

Aus dem Content-Pipeline-Post selbst gebaut (lokal, kein Skill): Gewinner-Radar `C:/social-insights/si/gewinner.py` – findet Ausreißer-Shorts (Aufrufe ≥ 3× Kanal-Median) in den Nischen von Code Chaos, Polished und ZeitSprung, misst sie mit derselben Machart-Messung wie die eigenen Posts und transkribiert den Hook (yt-dlp + Whisper, 0 €). „Ads-Maschine“: nicht umgesetzt – Tim schaltet keine bezahlten Anzeigen; ad-creative ist vorhanden.

## 2026-11-10 – Eigenbau ads-maschine (Nachtrag zum Trend-Lauf)

| Skill | Anlass (Belege) | Test |
|---|---|---|
| ads-maschine | Tim 10.11.: „Ads-maschine super für organische videos“ (Grafik „Make Claude an ads machine“: /ads → Ad Library → Creator → Bilder). Gebaut mit Tims vorhandenen Werkzeugen statt fremdem Skill: Werbe-Radar `C:/social-insights/si/werbung.py` (Apify jmlp/meta-ad-library-scraper, 0,00015 $/Anzeige; offizielle Ad-Library-API braucht Tims Ausweisbestätigung bei Meta, kein passender Token vorhanden), Gewinner-Radar `si/gewinner.py`, Creator über ad-creative/hook-master/copywriting, Bilder über ki-medien | Werbe-Radar-Testlauf 10.11.: Polished/Code Chaos liefern echte Langläufer (z. B. Mastering.com 248 Tage × 5 Varianten, Hook „How to use a compressor in 60 seconds?“); ZeitSprung nur Fachfremdes → dort abgeschaltet, lernt über den YouTube-Gewinner-Radar. Filter: mind. 2 Fachbegriffe, Dubletten raus. Ladetest 87 Skills |
