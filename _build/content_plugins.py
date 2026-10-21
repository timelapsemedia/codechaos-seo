# Inhalte der Plugin-Landingpages (/plugins/ und /plugins/<slug>/), Hauptsprache Deutsch.
# Quelle aller Fakten: codechaos-store/products/<slug>/description.html und product.json
# (Stand 21.10.2026). Nichts ergänzen, was dort nicht steht.
#
# live=False: Seite wird NICHT gebaut und steht nicht in Sitemap/llms.txt.
# Erst auf True setzen, wenn https://timberwolf688.gumroad.com/l/<slug> (und /l/<slug>-demo) HTTP 200 liefern,
# dann python3 _build/plugin_assets.py && python3 _build/build_pages.py, Sitemap + llms.txt ergänzen.

GUMROAD = "https://timberwolf688.gumroad.com/l/"

# Formate-Text für die Plugins mit Mac-Build (wortgleich zur Gumroad-Beschreibung, übersetzt)
MAC_FORMATS = ("<strong>Windows 10/11:</strong> VST3 + Standalone. <strong>macOS nur Apple Silicon</strong> (arm64, kein Intel-Build): "
               "VST3 + Standalone, <strong>nicht signiert und nicht notarisiert</strong>. macOS blockiert das Plugin beim ersten Start; "
               "du erlaubst es unter Systemeinstellungen → Datenschutz &amp; Sicherheit. <strong>Kein AU</strong>, deshalb läuft es nicht in Logic Pro.")
MAC_FAQ = ("Ja, aber nur auf Macs mit Apple Silicon (arm64), einen Intel-Build gibt es nicht. Das Plugin ist nicht signiert und nicht notarisiert: "
           "macOS blockiert es beim ersten Start, du erlaubst es unter Systemeinstellungen → Datenschutz &amp; Sicherheit. "
           "Es gibt kein AU-Format, deshalb läuft es nicht in Logic Pro.")
NOT_EVERY_DAW = ("Das VST3 wurde mit automatischen Tests geprüft, aber noch nicht in jeder DAW ausprobiert. "
                 "Wenn etwas in deiner DAW nicht funktioniert, sag Bescheid.")

PLUGINS = [
    # ─────────────────────────────── PSY ───────────────────────────────
    {
        "slug": "shardstep", "live": True, "group": "psy", "name": "Shardstep", "price": 15,
        "category": "Stutter- und Glitch-Effekt", "sub": "Effekt-Plugin (VST3)", "os": "Windows 10/11, macOS (Apple Silicon)",
        "title": "Shardstep: Stutter & Glitch VST3 für Hitech | Code Chaos",
        "desc": "Shardstep: Stutter- und Glitch-Effekt für 200–300 BPM. 16-Step-Pattern, Repeats bis 1/64, Tape Stop, MIDI-Trigger. VST3 Win + Mac, 15 €, Gratis-Demo.",
        "h1": "Shardstep: Stutter- und Glitch-Effekt für Hitech und Psycore",
        "eyebrow": "Code Chaos Audio · Effekt-Plugin",
        "teaser": "Stutter, Repeats, Tape Stop und Reverse im Takt deiner DAW, gebaut für 200 bis 300 BPM.",
        "answer": "Shardstep zerhackt, wiederholt und stoppt dein Audio im Takt deiner DAW, gebaut für Hitech und Psycore mit 200 bis 300 BPM. "
                  "Bei diesen Tempi dauert ein 1/32-Repeat nur wenige Millisekunden, deshalb braucht jede Slice-Kante eine kurze Überblendung, sonst klickt es. "
                  "Shardstep blendet jede Kante über, und Triolen-Repeats und Tape Stops folgen dem Beat deines Hosts.",
        "gui_alt": "Oberfläche von Shardstep: 16-Step-Pattern mit Repeat 1/32, Tie, Reverse, Gate und Tape Stop, darunter Mix, Repeat Pitch, Slice Fade, Crush und die MIDI-Trigger-Belegung",
        "gui_w": 2000, "gui_h": 1200,
        "audio_mode": "ab",
        "audio": [
            {"src": "build/shardstep/demo-dry.wav", "file": "demo-dry.mp3", "label": "A · Ohne Shardstep"},
            {"src": "build/shardstep/demo.wav", "file": "demo-wet.mp3", "label": "B · Mit Shardstep"},
        ],
        "audio_intro": "Dieselbe Passage ohne (A) und mit Shardstep (B). Während der Wiedergabe zwischen A und B umschalten.",
        "audio_note": "Gerendert mit dem Plugin-Code selbst (Demo-Datei aus dem Gumroad-Paket).",
        "specs": [
            ("Typ", "Stutter-/Glitch-Effekt, tempo-synchron"),
            ("Preis", "15 € auf Gumroad"),
            ("Formate", "VST3 + Standalone"),
            ("Systeme", "Windows 10/11 · macOS nur Apple Silicon (unsigniert)"),
            ("Nicht unterstützt", "AU / Logic Pro, Intel-Macs"),
            ("Pattern", "16 Steps (ein Takt in Sechzehnteln), 15 Factory-Patterns"),
            ("Latenz", "keine (Zero Latency)"),
            ("Demo", "vollständiges Plugin, kurzes Rauschen alle 45 Sekunden"),
        ],
        "features": [
            "<strong>16-Step-Pattern</strong>, ein Takt in Sechzehnteln, synchron zu Tempo und Taktposition des Hosts. Jeder Step wählt einen Effekt: Repeat 1/8, 1/16, 1/32, 1/64, 1/8T, 1/16T, 1/32T, Reverse, Tape Stop, Gate, Crush oder Tie (hält den vorigen Effekt länger)",
            "Pattern in jedem Takt abspielen oder nur im letzten Takt von 2, 4 oder 8, für <strong>Fills</strong>",
            "<strong>MIDI-Trigger:</strong> eine Note halten feuert einen Effekt (C = 1/8 bis A# = Crush, jede Oktave). Eine gehaltene Note überstimmt das Pattern und funktioniert auch bei gestopptem Transport",
            "<strong>Repeat Pitch</strong> von −24 bis +12 Halbtönen: Repeats tauchen ab oder steigen über die Länge des Events",
            "Tape Stop von 1/16 bis zu einem Takt, Gate in 1/16, 1/32 oder 1/64, Bitcrush 3 bis 16 Bit mit 1- bis 32-fachem Downsampling",
            "<strong>Slice Fade</strong> von 0,5 bis 8 ms: eine Raised-Cosine-Überblendung an jeder Slice-Kante und jedem Repeat-Neustart",
            "Wet/Dry-Mix. <strong>Null Latenz:</strong> Repeats spielen Audio ab, das schon angekommen ist; Reverse spielt das Audio direkt vor dem Step rückwärts",
            "Wenn nichts passiert (Transport gestoppt, leeres Pattern, Mix auf 0 % oder ein ausgelassener Takt), geht das Audio Bit für Bit unverändert durch",
            "15 Factory-Patterns, darunter Hitech Stutter 32, Psycore Tape Drop, Triplet Glitch Fill, Pitch Dive Roll, Rolling 1/64 Buzz und Bar 8 Breakdown Drop",
        ],
        "tested": "Die automatischen Prüfungen spielen jedes Factory-Pattern bei 150, 200 und 260 BPM auf einem synthetischen Psy-Loop und auf einem Sinuston. "
                  "Geprüft wird auf NaN, auf Spitzen über −0,3 dBFS, auf Gleichspannung (DC) und auf Sprünge an jeder Slice-Kante. Dazu kommen eine Tempo-Rampe "
                  "von 200 auf 300 BPM, ein Loop-Sprung und ein Transport-Stopp mitten im Effekt, und die bitgenaue Durchleitung wird bestätigt. "
                  "Noch nicht in jeder DAW ausprobiert: Wenn etwas in deiner nicht funktioniert, sag Bescheid.",
        "good_to_know": "Das Pattern folgt dem Transport der DAW. Die Standalone-App hat keinen Transport, dort spielst du die Effekte mit MIDI-Noten. "
                        "Sehr kurze Repeats (1/64) einer Kick sind kürzer als eine Schwingung der Kick und können während des Effekts leicht aus der Mitte rutschen. "
                        "So funktioniert Beat Repeat; sobald der Effekt endet, ist wieder dein unverändertes Audio da.",
        "formats": MAC_FORMATS + " Kein Login und kein Lizenzserver.",
        "faq": [
            ("Funktioniert Shardstep auch in der Standalone-App?",
             "Ja, aber die Standalone-App hat keinen Transport, dem das Pattern folgen könnte. Dort löst du die Effekte mit MIDI-Noten aus (C = 1/8 bis A# = Crush, in jeder Oktave)."),
            ("Klicken die Repeats bei 1/64 und hohem Tempo?",
             "Jede Slice-Kante und jeder Repeat-Neustart bekommt eine Raised-Cosine-Überblendung von 0,5 bis 8 ms (Slice Fade). Die automatischen Tests prüfen jedes Pattern bei 150, 200 und 260 BPM auf Sprünge an den Slice-Kanten."),
            ("Hat Shardstep Latenz?",
             "Nein. Repeats spielen Audio ab, das schon angekommen ist, und Reverse spielt das Audio direkt vor dem Step rückwärts. Wenn kein Effekt läuft, geht das Signal bitgenau durch."),
            ("Kann ich Shardstep nur für Fills nutzen?",
             "Ja. Das Pattern läuft wahlweise in jedem Takt oder nur im letzten Takt von 2, 4 oder 8. Die Takte davor bleiben unberührt."),
            ("Läuft Shardstep auf dem Mac?", MAC_FAQ),
            ("Gibt es eine kostenlose Demo?",
             "Ja, die Shardstep Demo auf Gumroad ist das vollständige Plugin mit einem kurzen Rauschen alle 45 Sekunden."),
        ],
        "related": ["chaos-fm", "kick-bass-scope", "crucible"],
    },
    {
        "slug": "chaos-fm", "live": True, "group": "psy", "name": "Chaos FM", "price": 19,
        "category": "FM-Synthesizer", "sub": "Instrument (VST3)", "os": "Windows 10/11",
        "title": "Chaos FM: FM-Synth VST3 für Hitech & Psycore | Code Chaos",
        "desc": "Chaos FM: 3-Operator-FM-Synth für Hitech, Psycore und Darkpsy mit GENERATE-Knopf und 12 Presets. VST3 + Standalone für Windows, 19 €, Gratis-Demo.",
        "h1": "Chaos FM: FM-Synth für Hitech, Psycore und Darkpsy",
        "eyebrow": "Code Chaos Audio · Instrument",
        "teaser": "3-Operator-FM-Synth mit GENERATE-Knopf für Leads, Bässe, Acid, Stabs, Plucks und FX.",
        "answer": "Chaos FM ist der FM-Synth hinter dem Code-Chaos-Sound: drei Operatoren, drei Algorithmen und ein großer <strong>GENERATE</strong>-Knopf, "
                  "der für die gewählte Kategorie einen neuen, musikalisch brauchbaren Patch würfelt: Lead, Bass, Acid, Stab, Pluck oder FX.",
        "gui_alt": "Oberfläche von Chaos FM: drei Operatoren A, B und C mit Ratio, Fine, Level und ADSR, darunter Algorithmus, Filter, Unison und Glide, oben Preset Hitech Scream Lead und der GENERATE-Knopf",
        "gui_w": 1880, "gui_h": 1240,
        "audio_mode": "single",
        "audio": [
            {"src": "SITE:images/social/chaos-fm.mp4", "file": "demo.mp3", "label": "Chaos FM · Werks-Presets"},
        ],
        "audio_intro": "Werks-Presets von Chaos FM, so wie sie aus dem Plugin kommen (Ton aus dem 10-Sekunden-Launch-Clip).",
        "audio_note": "",
        "specs": [
            ("Typ", "FM-Synthesizer, 3 Operatoren"),
            ("Preis", "19 € auf Gumroad"),
            ("Formate", "VST3 + Standalone"),
            ("Systeme", "Windows 10/11 (kein macOS-Build)"),
            ("Presets", "12 Factory-Presets"),
            ("Demo", "vollständiger Synth, kurzes Rauschen alle 45 Sekunden"),
        ],
        "features": [
            "3 Operatoren (Carrier + 2 Modulatoren) mit Ratio, Fine, Level und vollständiger ADSR-Hüllkurve je Operator",
            "3 Algorithmen, Feedback auf Operator C",
            "Zero-Delay-Tiefpassfilter mit Hüllkurven-Anteil und Drive",
            "Bis zu 4 Stimmen Unison mit Stereo-Spread, Mono/Legato mit Glide",
            "<strong>GENERATE</strong> würfelt einen neuen Patch für Lead, Bass, Acid, Stab, Pluck oder FX",
            "12 Factory-Presets: Hitech Scream Lead, Rolling Psy Bass, Psycore Growl Bass, Acid FM Squelch, Phrygian Bell Stab und mehr",
        ],
        "tested": "",
        "good_to_know": "",
        "formats": "<strong>Windows 10/11:</strong> VST3 + Standalone. Einen macOS-Build von Chaos FM gibt es nicht.",
        "faq": [
            ("Was macht der GENERATE-Knopf?",
             "Er würfelt einen neuen, musikalisch brauchbaren Patch für die Kategorie, die du auswählst: Lead, Bass, Acid, Stab, Pluck oder FX."),
            ("Läuft Chaos FM auf dem Mac?",
             "Nein. Chaos FM gibt es als VST3 und Standalone für Windows 10/11, einen macOS-Build gibt es nicht."),
            ("Welche Presets sind dabei?",
             "12 Factory-Presets, darunter Hitech Scream Lead, Rolling Psy Bass, Psycore Growl Bass, Acid FM Squelch und Phrygian Bell Stab."),
            ("Gibt es eine kostenlose Demo?",
             "Ja, die Chaos FM Demo auf Gumroad ist der vollständige Synth mit einem kurzen Rauschen alle 45 Sekunden."),
        ],
        "related": ["shardstep", "kick-bass-scope", "crucible"],
    },
    {
        "slug": "kick-bass-scope", "live": True, "group": "psy", "name": "Kick/Bass Scope", "price": 0,
        "category": "Oszilloskop / Analyzer für Kick und Bass", "sub": "Analyzer-Plugin (VST3)", "os": "Windows 10/11, macOS (Apple Silicon)",
        "title": "Kick/Bass Scope: Gratis Kick-Bass-Oszilloskop | Code Chaos",
        "desc": "Kostenloses VST3: Kick/Bass Scope zeigt Kick und Bass übereinander im Takt deiner DAW, mit Peaks in dBFS, Clip-Linie und Phasen-Warnung. Win + Mac.",
        "h1": "Kick/Bass Scope: kostenloses Oszilloskop für Kick und Bass",
        "eyebrow": "Code Chaos Audio · Gratis-Plugin",
        "teaser": "Gratis: Kick und Bass übereinander im Takt der DAW, mit Phasen-Warnung und Clip-Linie.",
        "answer": "Kick/Bass Scope zeigt deine Kick und deinen Bass übereinander, synchron zum Beat deiner DAW. Wenn eine rollende Bassline mit dem Kick-Ausklang kämpft, "
                  "siehst du es: wo sich die beiden Wellen überlappen, ob sie sich addieren oder auslöschen und wie nah die Summe am Clipping ist. "
                  "Das Plugin ist kostenlos; wenn es dir hilft, zahl, was du willst.",
        "gui_alt": "Oberfläche von Kick/Bass Scope: Kick in Orange und Bass in Türkis übereinander über eine halbe Taktlänge bei 145 BPM, rechts Peak-Anzeigen und die Kick/Bass-Korrelation",
        "gui_w": 2000, "gui_h": 1280,
        "extra_images": [
            {"name": "phase", "src": "../../build/kick-bass-scope/social/gui-out-of-phase.png", "w": 2000, "h": 1280,
             "alt": "Kick/Bass Scope warnt bei gegenphasiger Kick und Bass: negative Korrelation und Hinweis auf Auslöschung",
             "caption": "Gegenphasig: Die Korrelation wird negativ und das Plugin zeigt eine Warnung."},
        ],
        "audio_mode": None, "audio": [],
        "specs": [
            ("Typ", "Oszilloskop / Analyzer für Kick und Bass"),
            ("Preis", "kostenlos (Pay what you want)"),
            ("Formate", "VST3 + Standalone"),
            ("Systeme", "Windows 10/11 · macOS nur Apple Silicon (unsigniert)"),
            ("Nicht unterstützt", "AU / Logic Pro, Intel-Macs"),
            ("Fenster", "1/4, 1/2, 1 oder 2 Takte, synchron zum Host"),
            ("Presets", "13 Factory-Presets"),
            ("Audio", "geht bitgenau unverändert durch"),
        ],
        "features": [
            "Kick und Bass in zwei Farben, optional die Summenkurve (Kick + Bass)",
            "Synchron zu Tempo und Taktposition des Hosts: Fenster von 1/4, 1/2, 1 oder 2 Takten. Bei gestopptem Transport läuft die Anzeige frei weiter",
            "Peak-Anzeige pro Fenster in dBFS für Kick, Bass und Summe",
            "Einstellbare <strong>Clip-Linie</strong> (−12 bis 0 dBFS, Standard −0,3 dBFS), im Scope und auf den Metern eingezeichnet",
            "<strong>Kick/Bass-Korrelation</strong> von −1 bis +1, gemessen dort, wo beide tatsächlich spielen, mit einer klaren Warnung bei Gegenphasigkeit",
            "Überlappungszeit pro Fenster in ms, Zoom bis +24 dB für Kick-Ausklänge, Ghost des vorigen Fensters",
            "13 Factory-Presets: Psy Rolling 1/4, Hitech 1 Bar, Psycore 2 Bars, Darkpsy Tail Check 1/4, Club Headroom −6 dBFS und mehr",
            "Das Audio geht unberührt durch: Der Ausgang ist bitgenau identisch mit dem Eingang (in den automatischen Tests geprüft)",
        ],
        "routing": "Setz das Scope auf die Bass-Spur und schick die Kick in den Sidechain-Eingang. Sidechain-Routing für VST3 funktioniert in jeder DAW anders. "
                   "Wenn deine DAW keinen Sidechain in einen Effekt führen kann, stell Input auf <em>Single input</em>: Kick hart links und Bass hart rechts "
                   "auf einen gemeinsamen Bus routen und das Scope dort einsetzen.",
        "tested": "",
        "good_to_know": "",
        "formats": MAC_FORMATS + " " + NOT_EVERY_DAW,
        "faq": [
            ("Ist Kick/Bass Scope wirklich kostenlos?",
             "Ja. Auf Gumroad gilt Pay what you want: Du kannst 0 € eingeben oder etwas zahlen, wenn dir das Plugin hilft."),
            ("Wie bekomme ich Kick und Bass gleichzeitig in das Plugin?",
             "Setz das Scope auf die Bass-Spur und schick die Kick in den Sidechain-Eingang. Wenn deine DAW keinen Sidechain in einen Effekt führen kann, stell Input auf Single input und route Kick hart links und Bass hart rechts auf einen gemeinsamen Bus mit dem Scope."),
            ("Verändert das Plugin meinen Sound?",
             "Nein. Der Ausgang ist bitgenau identisch mit dem Eingang, das wurde in den automatischen Tests geprüft."),
            ("Was sagt mir die Kick/Bass-Korrelation?",
             "Sie läuft von −1 bis +1 und wird nur dort gemessen, wo Kick und Bass beide spielen. Bei Gegenphasigkeit, also wenn sich die beiden auslöschen, zeigt das Plugin eine klare Warnung."),
            ("Läuft Kick/Bass Scope auf dem Mac?", MAC_FAQ),
        ],
        "related": ["shardstep", "chaos-fm", "crucible"],
    },
    # ─────────────────────────── BLACK METAL ───────────────────────────
    {
        "slug": "gravesaw", "live": True, "group": "metal", "name": "Gravesaw", "price": 19,
        "category": "Amp + Cab für Gitarre und Bass", "sub": "Effekt-Plugin (VST3)", "os": "Windows 10/11, macOS (Apple Silicon)",
        "title": "Gravesaw: Black-Metal-Amp-Plugin (VST3) | Code Chaos",
        "desc": "Gravesaw: Black-Metal-Amp mit eingebauter Box für Gitarre und Bass-DI. 19 Cabs, 16 Presets, VST3 + Standalone für Windows und macOS. 19 €, Gratis-Demo.",
        "h1": "Gravesaw: Black-Metal-Amp mit eingebauter Box",
        "eyebrow": "Code Chaos Audio · Black Metal Suite",
        "teaser": "Black-Metal-Amp mit eingebauter Box für Gitarre und Bass-DI, von rau und sägend bis dick.",
        "answer": "Gravesaw ist ein Black-Metal-Amp mit eingebauter Box (Cab). Du steckst ein Gitarren- oder Bass-DI ein und bekommst den kalten, sägenden, "
                  "gesättigten Ton der Second-Wave-Platten: Tremolo-Picking, das auch bei 170+ BPM klar bleibt, Höhen, die schneiden statt zu zischen, "
                  "und keinerlei Clean-Headroom. Gravesaw ist der Amp der Code Chaos Black Metal Suite.",
        "gui_alt": "Oberfläche von Gravesaw: Gate, Tight, Gain und Raw/Thick, Tone Stack mit Bass, Mid, Treble, Fizz und Presence, Cab-Auswahl 4x12 Cold Bright und Pegelanzeigen, Preset Carpathian Buzz",
        "gui_w": 1960, "gui_h": 1020,
        "audio_mode": "single",
        "audio": [
            {"src": "build/gravesaw/demo.wav", "file": "demo.mp3", "label": "Gravesaw · Demo",
             "chapters": [("0:00", "DI-Gitarre (trocken, wie aufgenommen)"), ("0:03", "Gravesaw: Cold Tremolo Lead"), ("0:06", "Gravesaw: Carpathian Buzz"),
                          ("0:08", "Gravesaw: Frozen Wall Thick"), ("0:11", "Gravesaw: Raw Rehearsal Room"), ("0:14", "Gravesaw: Tamed Fizz"),
                          ("0:17", "Gravesaw: Four-Track Demo"), ("0:20", "Voller Mix: Wall Rhythm L/R doppelt + Cold Tremolo Lead + Bass Grind + Black Metal Drum Kit")]},
        ],
        "audio_intro": "Erst das trockene DI-Riff, dann dasselbe Riff durch sechs Presets, am Ende ein voller Mix (170 BPM, 26 Sekunden).",
        "audio_note": "",
        "specs": [
            ("Typ", "Amp-Simulation mit eingebauter Box (Cab) für Gitarre und Bass"),
            ("Preis", "19 € auf Gumroad"),
            ("Formate", "VST3 + Standalone"),
            ("Systeme", "Windows 10/11 · macOS nur Apple Silicon (unsigniert)"),
            ("Nicht unterstützt", "AU / Logic Pro, Intel-Macs"),
            ("Cabs", "19 eingebaut (10 Gitarre, 6 entschärft, 3 Bass) oder Cab aus für eigene IRs"),
            ("Presets", "16 Factory-Presets"),
            ("Latenz", "61 Samples (1,4 ms bei 44,1 kHz), wird an die DAW gemeldet"),
            ("Demo", "vollständiges Plugin, kurzes Rauschen alle 45 Sekunden"),
        ],
        "features": [
            "<strong>Noise Gate</strong> vor dem Amp (Threshold von −90 dBFS = aus bis −30 dBFS, mit Hold und Hysterese), damit die Lücken zwischen den Tremolo-Salven still bleiben",
            "<strong>Tight:</strong> Hochpass vor der Verzerrung, 20 bis 400 Hz, für straffe Bässe oder ein volles Doom-Fundament",
            "<strong>Gain-Stufen mit 4x Oversampling</strong> und Anti-Aliasing-Clipping. <strong>Raw / Thick</strong> verschiebt die Stimmung von rau und sägend (härteres Clipping, mehr Höhen in die Verzerrung) zu dick (weicheres Clipping, Schub in den unteren Mitten)",
            "<strong>Tone Stack</strong> nach der Verzerrung: Bass, Mid, Treble (je ±12 dB), <strong>Fizz</strong> (der Bereich über etwa 4 kHz, von gezähmt bis voller Fizz) und <strong>Presence</strong>",
            "<strong>19 eingebaute Cabs:</strong> 10 Gitarren-Boxen (4x12, 2x12 Open Back, 1x12 Lo-Fi-Combo, ein breites L/R-Paar für gedoppelte Rhythmusgitarren), 6 entschärfte Versionen und 3 Bass-Boxen. Der Wechsel überblendet ohne Klicks. Mit <strong>Cab aus</strong> lädst du nach Gravesaw deine eigene IR",
            "<strong>Low Blend</strong> mischt den cleanen Bassbereich des DI unter die Verzerrung, für Bass",
            "<strong>16 Factory-Presets:</strong> Cold Tremolo Lead, Carpathian Buzz, Wall Rhythm L / R (+ Tamed), Tamed Fizz, Four-Track Demo, Frozen Wall Thick, Depressive Haze, Low Gain Crunch, Bass Grind, Bass Clank, Doom Bass Deep und Amp Only (eigene IR)",
            "Ein- und Ausgangsmeter in dBFS, Gate-Anzeige. Mono- oder Stereo-Eingang",
        ],
        "extra_prose": "<p><strong>Die Boxen sind synthetisiert, nicht abgenommen.</strong> Es sind die Impulsantworten aus dem "
                       "<a href=\"" + GUMROAD + "black-metal-tone-kit?utm_source=site&amp;utm_medium=landing&amp;utm_campaign=gravesaw\">Black Metal Tone Kit</a>, "
                       "im Code entworfen aus einem Modell von Lautsprecher, Membran-Aufbruch, Mikrofonposition und Gehäuse. Sie sind keine Kopien kommerzieller Boxen oder IR-Bibliotheken. "
                       "Jede Box ist pegelangeglichen, ein Wechsel ändert also den Klang, nicht die Lautstärke.</p>",
        "tested": "Jedes Preset wird in den automatischen Tests mit einem synthetischen DI-Riff gerendert: kein Clipping (alle Spitzen bei etwa −4,5 dBFS; eine Sicherheitsstufe am Ausgang "
                  "hält die Spitzen auch bei einem 12 dB heißeren DI unter −0,3 dBFS), kein DC, keine Stille. Die Latenz beträgt 61 Samples (1,4 ms bei 44,1 kHz) und wird an die DAW gemeldet; "
                  "die Cab-Faltung fügt keine hinzu. Das Aliasing liegt im schlimmsten getesteten Fall (2,8-kHz-Sinus bei vollem Gain, roheste Einstellung, Cab aus) 54 dB unter den Obertönen.",
        "good_to_know": "",
        "formats": MAC_FORMATS + " " + NOT_EVERY_DAW + " Kein Lizenzserver, kein Login, keine Online-Prüfung.",
        "pairs": "Passt zum <a href=\"" + GUMROAD + "black-metal-drum-kit?utm_source=site&amp;utm_medium=landing&amp;utm_campaign=gravesaw\">Black Metal Drum Kit</a> "
                 "und zum Atmosphären-Bus <a href=\"/plugins/rimehall/\">Rimehall</a>.",
        "faq": [
            ("Funktioniert Gravesaw auch für Bass?",
             "Ja. Low Blend mischt den cleanen Bassbereich des DI unter die Verzerrung, es gibt 3 Bass-Boxen und die Presets Bass Grind, Bass Clank und Doom Bass Deep."),
            ("Kann ich meine eigenen Impulsantworten verwenden?",
             "Ja. Mit Cab aus (Preset Amp Only) läuft nur der Amp, und du lädst deine eigene IR nach Gravesaw."),
            ("Sind die Boxen Kopien bekannter Cabinets?",
             "Nein. Die Boxen sind synthetisiert: Impulsantworten aus dem Black Metal Tone Kit, im Code aus einem Modell von Lautsprecher, Membran, Mikrofonposition und Gehäuse entworfen. Sie sind keine Kopien kommerzieller Boxen oder IR-Bibliotheken."),
            ("Läuft Gravesaw auf dem Mac?", MAC_FAQ),
            ("Brauche ich einen Account oder eine Online-Aktivierung?",
             "Nein. Es gibt keinen Lizenzserver, keinen Login und keine Online-Prüfung."),
            ("Gibt es eine kostenlose Demo?",
             "Ja, die Gravesaw Demo auf Gumroad ist das vollständige Plugin mit einem kurzen Rauschen alle 45 Sekunden."),
        ],
        "related": ["rimehall", "crucible", "shardstep"],
    },
    {
        "slug": "rimehall", "live": True, "group": "metal", "name": "Rimehall", "price": 19,
        "category": "Hall, Shimmer und Tape (Atmosphären-Bus)", "sub": "Effekt-Plugin (VST3)", "os": "Windows 10/11, macOS (Apple Silicon)",
        "title": "Rimehall: Shimmer- & Tape-Reverb VST3 | Code Chaos",
        "desc": "Rimehall: kalter Hall bis 30 s, Oktav-Shimmer, Tape-Wow/Flutter und Ducking für Black Metal und Dark Ambient. VST3 Win + Mac, 19 €, Gratis-Demo.",
        "h1": "Rimehall: kalter Hall, Shimmer und Tape für Black Metal",
        "eyebrow": "Code Chaos Audio · Black Metal Suite, Teil 2",
        "teaser": "Kalter Hall bis 30 s, Oktav-Shimmer und Tape-Lo-Fi mit Ducking, damit das Riff vorne bleibt.",
        "answer": "Rimehall ist ein Atmosphären-Bus für Black Metal und Dark Ambient: ein kalter, dunkler Hall, ein Oktav-Shimmer und eine Tape-/Lo-Fi-Stufe in einem Plugin. "
                  "Leg ihn auf Tremolo-Gitarren, Keys oder Vocals und schieb sie in die Ferne, mit den gefrorenen Hallräumen und dem rauen Tape-Grit der Black-Metal-Platten der frühen 90er. "
                  "Rimehall ist Teil 2 der Code Chaos Black Metal Suite.",
        "gui_alt": "Oberfläche von Rimehall: Nachhall-Anzeige für Tiefen, Mitten und Höhen, Regler für Cold Hall, Shimmer und Space, Tape/Lo-Fi und Output, Preset Frozen Forest",
        "gui_w": 2000, "gui_h": 1224,
        "audio_mode": "single",
        "audio": [
            {"src": "build/rimehall/demo.wav", "file": "demo.mp3", "label": "Rimehall · Demo",
             "chapters": [("0:00", "Trocken: synthetisches Tremolo-Riff (DI, Amp und Cab-IRs aus dem Black Metal Tone Kit)"), ("0:08", "Rimehall: Frozen Forest"),
                          ("0:16", "Rimehall: Moonlit Tremolo Bus"), ("0:24", "Rimehall: Cassette Cathedral"), ("0:31", "Rimehall: Ice Shimmer Choir"),
                          ("0:39", "Rimehall: Grim Rehearsal Tape"), ("0:47", "Rimehall: Northern Void"),
                          ("0:55", "Voller Mix: Gitarren durch Moonlit Tremolo Bus, Bass und Black Metal Drum Kit trocken")]},
        ],
        "audio_intro": "Erst das trockene Riff, dann sechs Presets, am Ende ein voller Mix (170 BPM, 69 Sekunden).",
        "audio_note": "Das Demo-Audio wurde mit dem Plugin-Code selbst gerendert; das Riff ist synthetisiert, ohne fremde Samples.",
        "specs": [
            ("Typ", "Hall + Shimmer + Tape/Lo-Fi (Atmosphären-Bus)"),
            ("Preis", "19 € auf Gumroad"),
            ("Formate", "VST3 + Standalone"),
            ("Systeme", "Windows 10/11 · macOS nur Apple Silicon (unsigniert)"),
            ("Nicht unterstützt", "AU / Logic Pro, Intel-Macs"),
            ("Nachhallzeit", "0,3 bis 30 Sekunden"),
            ("Presets", "14 Factory-Presets"),
            ("Latenz", "konstant 4 ms, wird an den Host gemeldet"),
            ("Demo", "vollständiges Plugin, kurzes leises Rauschen alle 45 Sekunden"),
        ],
        "features": [
            "<strong>Cold Hall:</strong> Feedback-Delay-Netzwerk mit 8 Leitungen, Pre-Delay bis 250 ms, Size, Decay von 0,3 bis 30 s, Damping (1 bis 18 kHz) und langsame Delay-Modulation gegen metallisches Klingeln",
            "<strong>Frost:</strong> ein Regler für den Charakter des Halls. Hoch = dünnere, kältere Tiefen und etwas mehr Luft oben; runter = dunkler und voller",
            "<strong>Shimmer:</strong> eine Oktave höher in der Rückkopplungsschleife, 0 bis 100 %. Der Shimmer-Pfad wird vor dem Pitch-Shift bandbegrenzt, damit kein Aliasing-Rauschen zurückfaltet (getestet: das Alias-Produkt eines 14-kHz-Tons bleibt mehr als 100 dB darunter)",
            "<strong>Tape / Lo-Fi:</strong> Wow, Flutter, asymmetrische Sättigung, Tape-Ton (2 bis 20 kHz) und optionales Rauschen. Wählbar, ob das Tape nur den Hall oder den ganzen Bus färbt",
            "<strong>Ducking:</strong> der Hall tritt um bis zu 18 dB zurück, solange das trockene Signal spielt, und blüht in den Lücken auf, damit schnelle Riffs klar bleiben",
            "Width, Mix (Equal Power), Output-Gain und ein optionaler Safety-Soft-Clip, der Spitzen unter −0,3 dBFS hält",
            "Geschätzte Nachhallzeit-Anzeige für Tiefen, Mitten und Höhen, Meter für Eingang, Hall, Ausgang und Ducking",
            "<strong>14 Factory-Presets:</strong> Frozen Forest, Cassette Cathedral, Winter Hall Vocals, Ice Shimmer Choir, Grim Rehearsal Tape, Northern Void, Moonlit Tremolo Bus, Glacier Pad Swell, Frostbitten Room, Pale Ritual Hall, Blizzard Wash, Init Cold Hall und mehr",
        ],
        "tested": "Jedes Preset wird automatisch mit einem Impuls, einem Rauschstoß und einem synthetischen Tremolo-Riff gerendert: kein NaN oder Inf, kein DC, Spitzen bei oder unter −0,3 dBFS "
                  "bei unserem Standard-Eingangspegel (−6 dBFS Spitze), und jeder Ausklang fällt bis zur Stille ab (oder bis zum Rauschteppich, wenn Hiss an ist). Extreme Einstellungen "
                  "(30 s Decay, 100 % Shimmer und Modulation, +6 dBFS Eingang) klingen ohne außer Kontrolle geratene Rückkopplung aus. Die Latenz beträgt konstant 4 ms und wird an den Host gemeldet.",
        "good_to_know": "",
        "formats": MAC_FORMATS + " " + NOT_EVERY_DAW,
        "pairs": "Mehr aus der Black Metal Suite: der Amp <a href=\"/plugins/gravesaw/\">Gravesaw</a>, das "
                 "<a href=\"" + GUMROAD + "black-metal-tone-kit?utm_source=site&amp;utm_medium=landing&amp;utm_campaign=rimehall\">Black Metal Tone Kit</a> "
                 "(synthetisierte Cab-IRs und REAPER-Ketten, das Demo-Riff nutzt dessen Amp- und Cab-Modelle) und das "
                 "<a href=\"" + GUMROAD + "black-metal-drum-kit?utm_source=site&amp;utm_medium=landing&amp;utm_campaign=rimehall\">Black Metal Drum Kit</a> (synthetisierte Blast-Beat-Drums).",
        "faq": [
            ("Wird der Mix bei schnellen Riffs nicht matschig?",
             "Dafür gibt es Ducking: Der Hall tritt um bis zu 18 dB zurück, solange das trockene Signal spielt, und blüht in den Lücken auf. So bleiben schnelle Riffs klar."),
            ("Färbt das Tape nur den Hall oder das ganze Signal?",
             "Beides ist möglich. Du wählst, ob die Tape-Stufe (Wow, Flutter, Sättigung, Tape-Ton, Rauschen) nur den Hall oder den ganzen Bus färbt."),
            ("Erzeugt der Shimmer Aliasing?",
             "Der Shimmer-Pfad wird vor dem Pitch-Shift bandbegrenzt. In den Tests bleibt das Alias-Produkt eines 14-kHz-Tons mehr als 100 dB darunter."),
            ("Läuft Rimehall auf dem Mac?", MAC_FAQ),
            ("Gibt es eine kostenlose Demo?",
             "Ja, die Rimehall Demo auf Gumroad ist das vollständige Plugin mit einem kurzen, leisen Rauschen alle 45 Sekunden."),
        ],
        "related": ["gravesaw", "crucible", "shardstep"],
    },
    # Vorbereitet, noch NICHT live (Gumroad /l/frostfret und /l/hoarfell: 404 am 21.10.2026)
    {
        "slug": "frostfret", "live": False, "group": "metal", "name": "Frostfret", "price": 29,
        "category": "Physikalisch modellierte Gitarre und Bass", "sub": "Instrument (VST3)", "os": "Windows 10/11, macOS (Apple Silicon)",
        "title": "Frostfret: modellierte Gitarre als VST3 | Code Chaos",
        "desc": "Frostfret: E-Gitarre, Akustik und Bass per MIDI, physikalisch modelliert ohne Samples. Tremolo-Picking, Amp eingebaut, 30 Presets. VST3 Win + Mac, 29 €.",
        "h1": "Frostfret: Gitarre aus Physik statt Samples",
        "eyebrow": "Code Chaos Audio · Black Metal Suite",
        "teaser": "E-Gitarre, Steel- und Nylon-Akustik und E-Bass per MIDI, physikalisch modelliert, ohne Samples.",
        "answer": "Frostfret ist eine Gitarre, die du per MIDI spielst, gebaut aus Physik statt aus Samples. Jede Note ist eine modellierte Saite: Sie wird angeschlagen, klingt, schwebt, "
                  "wird mit dem Handballen abgedämpft und rutscht. E-Gitarre, Steelstring- und Nylon-Akustik und ein E-Bass in einem Instrument. Frostfret ist Teil der Code Chaos Black Metal Suite.",
        "gui_alt": "Oberfläche von Frostfret, dem physikalisch modellierten Gitarren-Instrument von Code Chaos Audio",
        "gui_w": 1240, "gui_h": 860,
        "audio_mode": "single",
        "audio": [
            {"src": "build/frostfret/demo-blackmetal.wav", "file": "demo-blackmetal.mp3", "label": "Black Metal (170 BPM, E-Phrygisch)"},
            {"src": "build/frostfret/demo-acoustic.wav", "file": "demo-acoustic.mp3", "label": "Akustik: Strumming und Fingerpicking (100 BPM)"},
            {"src": "build/frostfret/demo-clean-crunch.wav", "file": "demo-clean-crunch.mp3", "label": "Clean Neck Arpeggio v1 + Cold Crunch Rhythm v1 (110 BPM)"},
        ],
        "audio_intro": "Drei Demo-Clips aus dem Gumroad-Paket.",
        "audio_note": "",
        "specs": [
            ("Typ", "Physikalisch modelliertes Instrument (Gitarre + Bass)"),
            ("Preis", "29 € auf Gumroad"),
            ("Formate", "VST3-Instrument + Standalone"),
            ("Systeme", "Windows 10/11 · macOS nur Apple Silicon (unsigniert)"),
            ("Nicht unterstützt", "AU / Logic Pro, Intel-Macs"),
            ("Presets", "30 (24 Gitarre, 6 Bass)"),
            ("Latenz", "61 Samples (1,4 ms bei 44,1 kHz), wird an die DAW gemeldet"),
            ("Demo", "vollständiges Instrument, kurzes Rauschen alle 45 Sekunden"),
        ],
        "features": [
            "<strong>Modellierte Saiten:</strong> digitale Waveguides mit Saitensteifigkeit, zwei Schwingungsebenen, Anschlagposition und Plektrumhärte; Noten liegen auf echten Saiten und Bünden",
            "<strong>Drei Gitarren:</strong> E-Gitarre mit Tonabnehmer-Modellen, Steelstring- und Nylon-Akustik mit modellierten Korpussen und Mikrofonpositionen, Piezo oder Mikro + Piezo",
            "<strong>Voicing</strong> Natural oder Classic (v1), dazu ein <strong>Air</strong>-Regler für hellere oder weichere Saiten",
            "<strong>Amp eingebaut:</strong> die DSP von Gravesaw (Gate, 4x Oversampling, Tone Stack, 19 synthetisierte Boxen) in Clean, Crunch, Overdrive und High-Gain, oder DI Out",
            "<strong>Spielweisen:</strong> Tremolo-Picking (1/16, 1/16-Triole, 1/32, tempo-synchron), Powerchords von einer Taste, Palm Mute, Legato, Slides, Bends, Vibrato, Flageoletts, Dead Notes, Strumming",
            "<strong>Humanize</strong> und <strong>Double Track</strong>: zwei unabhängige Takes hart links und rechts aus einer MIDI-Spur",
            "<strong>Bass</strong> mit Finger, Plektrum und leichtem Slap, Palm Mute, Tremolo, eingebautem Amp mit drei Bass-Boxen oder DI Out",
            "<strong>30 Factory-Presets:</strong> 10 E-Gitarre, 6 Akustik, 4 hellere Varianten, 4 Sounds aus Version 1, 6 Bass",
        ],
        "tested": "Jedes Preset läuft in den automatischen Tests bei 44,1, 48 und 96 kHz mit MIDI-Testspuren: kein NaN, keine Stille, Spitzen nie über −0,3 dBFS, kein DC, jeder Ausklang endet in Stille, "
                  "keine Klicks bei Neuanschlägen, Voice-Steals und Note-Offs, identische Ausgabe bei jeder Puffergröße, alles unter 160 Hz mono. Saiten sind auf 1,5 Cent genau gestimmt.",
        "good_to_know": "<strong>Ehrlich zum Klang:</strong> Keine synthetisierte Gitarre klingt genau wie eine aufgenommene, Frostfret auch nicht. Akustik, Crunch, High-Gain und Bass kommen am nächsten heran; "
                        "die cleane E-Gitarre klingt noch am deutlichsten synthetisch. Hör dir die Demo-Clips an oder probier die kostenlose Demo, bevor du kaufst.",
        "formats": MAC_FORMATS + " " + NOT_EVERY_DAW + " Keine Samples, kein Lizenzserver, kein Login.",
        "faq": [
            ("Klingt Frostfret wie eine echte Gitarre?",
             "Nicht genau. Keine synthetisierte Gitarre klingt wie eine aufgenommene. Akustik, Crunch, High-Gain und Bass kommen am nächsten heran, die cleane E-Gitarre klingt am deutlichsten synthetisch. Hör dir die Demo-Clips an oder probier die Demo."),
            ("Brauche ich zusätzlich einen Amp?",
             "Nein, die DSP des Gravesaw-Amps ist eingebaut. Mit DI Out kannst du aber auch Gravesaw oder einen anderen Amp danach einsetzen."),
            ("Läuft Frostfret auf dem Mac?", MAC_FAQ),
            ("Gibt es eine kostenlose Demo?",
             "Ja, die Frostfret Demo ist das vollständige Instrument mit einem kurzen Rauschen alle 45 Sekunden."),
        ],
        "related": ["hoarfell", "gravesaw", "rimehall"],
    },
    {
        "slug": "hoarfell", "live": False, "group": "metal", "name": "Hoarfell", "price": 17,
        "category": "Modellierte Drums, Bass und Atmosphäre", "sub": "Instrument (VST3)", "os": "Windows 10/11, macOS (Apple Silicon)",
        "title": "Hoarfell: Black-Metal-Drums & Atmos VST3 | Code Chaos",
        "desc": "Hoarfell: modellierte Drums für 250-BPM-Blasts, E-Bass und Chor, Orgel, Strings im Hall, ohne Samples. 20 Presets, VST3 Win + Mac, 17 €, Gratis-Demo.",
        "h1": "Hoarfell: Drums, Bass und Atmosphäre für Black Metal",
        "eyebrow": "Code Chaos Audio · Black Metal Suite",
        "teaser": "Modelliertes Drumkit für Blast Beats, E-Bass und Chor/Orgel/Strings, ohne Samples.",
        "answer": "Hoarfell spielt Drums, Bass und Atmosphäre eines Black-Metal-Songs, gebaut aus Modellen statt aus Samples. Ein Plugin, drei Engines: ein Drumkit für Blast Beats, "
                  "ein modellierter E-Bass und Chor, Orgel, Strings, Glocken und Keys in einer kalten Halle. Die Gitarren stecken im Schwester-Plugin Frostfret.",
        "gui_alt": "Oberfläche von Hoarfell, dem modellierten Drum-, Bass- und Atmosphären-Instrument von Code Chaos Audio",
        "gui_w": 1240, "gui_h": 860,
        "audio_mode": "single",
        "audio": [
            {"src": "build/hoarfell/demo-blackmetal.wav", "file": "demo-blackmetal.mp3", "label": "Black Metal (180 BPM): Raw Blast Kit, Bass Pick Grind, Choir Ah, Frostfret-Gitarren"},
            {"src": "build/hoarfell/demo-suite.wav", "file": "demo-suite.mp3", "label": "Suite (150 BPM): Chor, Glocke, Studio Kit, Bass, Strings"},
        ],
        "audio_intro": "Zwei Demo-Clips aus dem Gumroad-Paket.",
        "audio_note": "",
        "specs": [
            ("Typ", "Modelliertes Instrument: Drums, Bass, Atmos/Keys"),
            ("Preis", "17 € auf Gumroad"),
            ("Formate", "VST3-Instrument + Standalone"),
            ("Systeme", "Windows 10/11 · macOS nur Apple Silicon (unsigniert)"),
            ("Nicht unterstützt", "AU / Logic Pro, Intel-Macs"),
            ("Presets", "20 (6 Kits, 6 Bass, 8 Atmos/Keys)"),
            ("Latenz", "61 Samples (1,4 ms bei 44,1 kHz), wird an die DAW gemeldet"),
            ("Demo", "vollständiges Instrument, kurzes Rauschen alle 45 Sekunden"),
        ],
        "features": [
            "<strong>Modelliertes Drumkit auf der General-MIDI-Belegung:</strong> Kick, zwei Snares, Rim, sechs Toms, Hi-Hats mit Choke, zwei Crashes, zwei Rides, Bell, China",
            "Jeder Schlag aus 24 Frequenzbändern mit eigenem Pegel und zweistufigem Ausklang, nach Messungen echter Drums geformt (gemittelte Kurven, kein aufgenommenes Audio)",
            "Kein Schlag gleicht dem anderen (Round Robin); Snare-Teppich schnarrt mit Kick und Toms",
            "<strong>Close-Mikros, Overhead-Paar und Raum</strong>, dazu ein Lo-Fi-Regler für Proberaum-Tape-Grit. 6 Kits von Studio bis Lo-Fi",
            "Für Blast Beats gebaut: 250-BPM-Sechzehntel bleiben in den Tests klickfrei",
            "<strong>Bass:</strong> modellierte Saite mit Finger, Plektrum oder leichtem Slap, Palm Mute, Tremolo, eingebauter Gravesaw-Amp mit drei Bass-Boxen oder DI Out. 6 Presets",
            "<strong>Atmos / Keys:</strong> modellierter Chor (bis zu acht Sänger pro Note, Vokale Ah / Oh / Uh), Zugriegelorgel, Strings-Pad, kalte Glocke, Celesta und Lo-Fi-Keys mit langem Hall. 8 Presets",
        ],
        "tested": "Jedes Preset läuft in den automatischen Tests bei 44,1, 48 und 96 kHz mit MIDI-Testspuren (250-BPM-Blast, Grooves, Pad-Akkorde, Sustain-Pedal): kein NaN, keine Stille, "
                  "Spitzen nie über −0,3 dBFS, kein DC, jeder Ausklang endet in Stille, keine Klicks, identische Ausgabe bei jeder Puffergröße, alles unter 160 Hz mono.",
        "good_to_know": "<strong>Ehrlich zum Klang:</strong> Die Drums kommen nah an ein mikrofoniertes Kit heran, im Groove und bei Blast-Beat-Tempo; der Bass nah an einen aufgenommenen Bass. "
                        "Der Chor singt nur Vokale, keine Wörter, und funktioniert als Chor-Pad hinter dem Mix, nicht als Lead-Chor.",
        "formats": MAC_FORMATS + " " + NOT_EVERY_DAW + " Keine Samples, kein Lizenzserver, kein Login.",
        "faq": [
            ("Schafft das Drumkit schnelle Blast Beats?",
             "Ja, es ist dafür gebaut: 250-BPM-Sechzehntel bleiben in den automatischen Tests klickfrei."),
            ("Kann der Chor Text singen?",
             "Nein. Der Chor singt die Vokale Ah, Oh und Uh, keine Wörter. Er funktioniert als Chor-Pad hinter dem Mix."),
            ("Läuft Hoarfell auf dem Mac?", MAC_FAQ),
            ("Gibt es eine kostenlose Demo?",
             "Ja, die Hoarfell Demo ist das vollständige Instrument mit einem kurzen Rauschen alle 45 Sekunden."),
        ],
        "related": ["frostfret", "gravesaw", "rimehall"],
    },
]

# Crucible hat eine eigene (englische) Seite /crucible.html; hier nur die Karte für /plugins/ und die Querverweise.
CRUCIBLE = {
    "slug": "crucible", "live": True, "group": "psy", "name": "Crucible", "price": 19, "url": "/crucible.html",
    "teaser": "3-Band-Sättigung: Hard Clip, Wavefolder, Tube, Diode oder Tape pro Band, bis 8x Oversampling.",
    "img_webp": "/images/crucible-ui-880.webp", "img_jpg": "/images/crucible-ui.jpg", "w": 880, "h": 560,
    "alt": "Oberfläche von Crucible: Low Hard Clip, Mid Tube, High Tape, 4x Oversampling",
    "os": "Windows 10+ · VST3 + Standalone",
}

GROUPS = [
    ("psy", "Für Hitech, Psycore und Darkpsy",
     "Gebaut für schnelle, dichte Psytrance-Produktionen: Sättigung, Glitch, FM-Sounds und Kontrolle über Kick und Bass."),
    ("metal", "Für Black Metal: die Code Chaos Black Metal Suite",
     "Amp, Hall und Atmosphäre für einen kalten, rauen Black-Metal-Sound aus dem Heimstudio."),
]

# Genre-Seite (DE) → passende Plugins (nur live gebaute Seiten werden verlinkt)
GENRE_PLUGINS = {
    "psycore": ["shardstep", "chaos-fm", "kick-bass-scope", "crucible"],
    "hitech-psytrance": ["shardstep", "chaos-fm", "kick-bass-scope", "crucible"],
    "darkpsy": ["chaos-fm", "kick-bass-scope", "crucible", "shardstep"],
}
