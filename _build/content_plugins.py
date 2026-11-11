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
    # Crucible: Fakten aus der früheren Produktseite /crucible.html (Stand 05.11.2026, jetzt Weiterleitung) und
    # _docs/gumroad-crucible-text.md. Bilder/Audio liegen schon in der Site (assets_manual: plugin_assets.py überspringt).
    {
        "slug": "crucible", "live": True, "assets_manual": True, "group": "psy", "name": "Crucible", "price": 19, "version": "1.1.0",
        "category": "3-Band-Sättigung", "sub": "Effekt-Plugin (VST3)", "os": "Windows 10+",
        "title": "Crucible: 3-Band-Sättigung VST3 für Hitech | Code Chaos",
        "feat_title": "Funktionen der 3-Band-Sättigung",
        "desc": "Crucible: 3-Band-Sättigung (VST3 + Standalone, Windows) für Hitech & Psycore. Hard Clip, Wavefolder, Tube, Diode, Tape pro Band. 19 €, Gratis-Demo.",
        "h1": "Crucible: 3-Band-Sättigung (VST3) für Hitech & Psycore",
        "eyebrow": "Code Chaos Audio · Effekt-Plugin",
        "teaser": "3-Band-Sättigung: Hard Clip, Wavefolder, Tube, Diode oder Tape pro Band, bis 8x Oversampling.",
        "answer": "Crucible ist ein Sättigungs-Plugin mit drei Bändern: Es teilt dein Signal in Low, Mid und High und sättigt jedes Band für sich, "
                  "mit fünf Sättigungsarten (Hard Clip, Wavefolder, Tube, Diode, Tape), Drive, Mix und Gain pro Band und bis zu 8x Oversampling. "
                  "VST3 + Standalone für Windows 10+, mit kostenloser Demo. <strong>Shape. Saturate. Dominate.</strong>",
        "gui_alt": "Oberfläche von Crucible: Low Hard Clip, Mid Tube, High Tape, 4x Oversampling",
        "gui_w": 1760, "gui_h": 1120,
        "audio_mode": "ab",
        "audio": [
            {"src": "SITE:audio/crucible-demo-dry.mp3", "file": "demo-dry.mp3", "label": "A · Ohne Crucible"},
            {"src": "SITE:audio/crucible-demo-wet.mp3", "file": "demo-wet.mp3", "label": "B · Mit Crucible"},
        ],
        "audio_intro": "Derselbe Psy-Loop mit 190 BPM ohne (A) und mit Crucible (B), lautheitsangeglichen (beide −16 LUFS): Du hörst Klang und Dichte, nicht nur Lautstärke. "
                       "Während der Wiedergabe zwischen A und B umschalten.",
        "audio_note": "Einstellungen: Low Hard Clip 12 dB, Mid Tube 9 dB, High Tape 6 dB bei 70 % Mix, Crossover 120 Hz / 4 kHz, 4x Oversampling, Output −0,8 dB. "
                      "Offline gerendert mit Crucible 1.0.0; der Quell-Loop ist für diese Demo synthetisiert.",
        "specs": [
            ("Typ", "3-Band-Sättigung (Harmonic Saturation)"),
            ("Preis", "19 € auf Gumroad"),
            ("Formate", "VST3 + Standalone"),
            ("System", "Windows 10 oder neuer (kein macOS-Build)"),
            ("Bänder", "Low, Mid, High mit zwei einstellbaren Crossovern"),
            ("Sättigungsarten", "Hard Clip, Wavefolder, Tube, Diode, Tape (pro Band wählbar)"),
            ("Pro Band", "Drive, Mix, Gain, Mute, Solo"),
            ("Oversampling", "bis 8x"),
            ("Lizenz", "Einzelplatz, unbefristet; ein Key aktiviert bis zu 3 Rechner"),
            ("Demo", "vollständiges Plugin, kurzes Rauschen alle 45 Sekunden"),
        ],
        "features": [
            "<strong>3 Bänder:</strong> Low, Mid und High getrennt bearbeiten, zwei einstellbare Crossover. Den Bass hart fahren und die Höhen sauber lassen",
            "<strong>5 Sättigungsarten</strong>, pro Band wählbar: Hard Clip (aggressiv, laut, chirurgisch), Wavefolder (metallisch, synthetisch), "
            "Tube (warm, rund, musikalisch), Diode (asymmetrisch, rau), Tape (Glue, Verschmieren, Vintage-Drive)",
            "<strong>Pro Band</strong> Drive, Mix, Gain, Mute und Solo, dazu Output-Gain und Bypass",
            "<strong>Oversampling bis 8x</strong> für saubere Sättigung ohne Aliasing, auch wenn du hart reinfährst",
            "Gebaut von einem aktiven Hitech- und Psycore-Producer für echte Sessions: Mix, Master, Destroy",
        ],
        "extra_prose": "<h3>So arbeitest du mit Crucible</h3><ol>"
                       "<li><strong>Split:</strong> Die Übergänge Low/Mid und Mid/High setzen und das Signal in drei unabhängige Bänder teilen.</li>"
                       "<li><strong>Saturate:</strong> Pro Band eine Sättigungsart wählen und Drive aufdrehen: Gewicht für die Tiefen, Biss für die Mitten, Luft und Kante für die Höhen.</li>"
                       "<li><strong>Balance:</strong> Mit Mix pro Band mischen, mit Gain angleichen, mit Solo abhören und mit Oversampling sauber halten.</li></ol>"
                       "<h3>Warum Sättigung in drei Bändern?</h3>"
                       "<p>Harmonische Sättigung fügt einem Signal musikalische Obertöne hinzu. Es wirkt dadurch lauter, wärmer und präsenter. "
                       "Statt das ganze Signal auf einmal zu sättigen, bekommt bei Crucible jedes Band seinen eigenen Charakter: Hard Clip auf Sub und Kick für Druck, "
                       "eine sanfte Tube in den Mitten für die Leads, Tape in den Höhen, alles in einer Instanz. "
                       "Crucible ist für schnelle, dunkle Psytrance-Produktionen gebaut, funktioniert aber überall, wo du einen Saturator einsetzt: "
                       "Drum &amp; Bass, Techno, Dubstep, Hip-Hop, Rock und Mastering.</p>",
        "tested": "",
        "good_to_know": "Nach dem Kauf steht in deiner Gumroad-Quittung ein persönlicher Lizenz-Key. Du fügst ihn einmal in Crucible ein (Activate, dafür braucht es Internet); "
                        "ein Key aktiviert bis zu 3 deiner Rechner. Crucible prüft die Lizenz alle zwei Wochen im Hintergrund und läuft bis zu 60 Tage offline. "
                        "Bis zur Aktivierung verhält es sich wie die kostenlose Demo.",
        "formats": "<strong>Windows 10 oder neuer:</strong> VST3 + Standalone, in jedem VST3-Host, z. B. REAPER, Ableton Live 12+, Cubase 12+, Studio One 6+, FL Studio und Bitwig. "
                   "Einen macOS-Build von Crucible gibt es nicht. Die aktuellen Systemanforderungen stehen auf der Gumroad-Seite.",
        "faq": [
            ("Was ist Crucible?",
             "Crucible ist ein 3-Band-Sättigungs-Plugin von Code Chaos Audio. Es teilt dein Signal in Low, Mid und High und sättigt jedes Band für sich, "
             "mit fünf Sättigungsarten (Hard Clip, Wavefolder, Tube, Diode, Tape), Drive, Mix, Gain, Mute und Solo pro Band und Oversampling bis 8x."),
            ("Eignet sich Crucible für Psytrance, Hitech und Psycore?",
             "Ja, gebaut hat es ein aktiver Hitech-, Psycore- und Darkpsy-Producer. Im Low-Band gibst du Kick und Bassline Wärme und Gewicht, "
             "oben Leads und Percussion Biss und Präsenz, ohne dass der Mix matschig wird."),
            ("Was ist der Unterschied zwischen den Sättigungsarten?",
             "Hard Clip ist aggressiv, laut und chirurgisch, gut für Druck im Bass. Wavefolder faltet die Wellenform zurück und erzeugt metallische, synthetische Obertöne. "
             "Tube ist warm, rund und musikalisch für die Mitten. Diode bringt asymmetrischen, rauen Biss. Tape klebt zusammen, verschmiert leicht und gibt Luft. "
             "Jedes Band bekommt seine eigene Art."),
            ("Läuft Crucible auf dem Mac?",
             "Nein. Crucible gibt es als VST3 und Standalone für Windows 10 oder neuer, einen macOS-Build gibt es nicht."),
            ("Wie funktioniert die Lizenz-Aktivierung?",
             "In deiner Gumroad-Quittung steht ein persönlicher Lizenz-Key. Du fügst ihn einmal in Crucible ein (Activate, Internet nötig); ein Key aktiviert bis zu 3 Rechner. "
             "Crucible prüft die Lizenz alle zwei Wochen im Hintergrund und läuft bis zu 60 Tage offline."),
            ("Gibt es eine kostenlose Demo?",
             "Ja, die Crucible Demo auf Gumroad ist das vollständige Plugin mit einem kurzen Rauschen alle 45 Sekunden."),
        ],
        "related": ["kick-bass-scope", "shardstep", "chaos-fm"],
        # Englische Fassung /en/plugins/crucible/ (Texte aus der früheren crucible.html)
        "en": {
            "title": "Crucible: 3-Band Saturation VST3 Plugin | Code Chaos",
            "desc": "Crucible: 3-band harmonic saturation VST3 + standalone for Windows. Hard clip, wavefolder, tube, diode, tape per band, up to 8x oversampling. €19, free demo.",
            "h1": "Crucible: 3-band saturation VST3",
            "eyebrow": "Code Chaos Audio · effect plugin",
            "category": "3-band saturation",
            "os": "Windows 10+",
            "answer": "Crucible is a 3-band harmonic saturation plugin: it splits your signal into low, mid and high and saturates each band independently, "
                      "with five saturation types (hard clip, wavefolder, tube, diode, tape), per-band drive, mix and gain and up to 8x oversampling. "
                      "VST3 + standalone for Windows 10+, with a free demo. <strong>Shape. Saturate. Dominate.</strong>",
            "gui_alt": "Crucible plugin interface: Low Hard Clip, Mid Tube, High Tape, 4x oversampling",
            "audio": ["A · Dry", "B · Crucible"],
            "audio_intro": "The same 190 BPM psy loop, without and with Crucible. Loudness-matched (both −16 LUFS), so you hear tone and density, not just volume. "
                           "Switch between A and B while it plays.",
            "audio_note": "Settings: Low Hard Clip 12 dB, Mid Tube 9 dB, High Tape 6 dB at 70 % mix, crossovers 120 Hz / 4 kHz, 4x oversampling, output −0.8 dB. "
                          "Rendered offline with Crucible 1.0.0; source loop synthesized for this demo.",
            "specs": [
                ("Type", "3-band harmonic saturation plugin"),
                ("Price", "€19 on Gumroad"),
                ("Formats", "VST3 + Standalone"),
                ("System", "Windows 10 or newer (no macOS build)"),
                ("Bands", "Low, Mid, High with two adjustable crossovers"),
                ("Saturation types", "Hard Clip, Wavefolder, Tube, Diode, Tape (chosen per band)"),
                ("Per-band controls", "Drive, Mix, Gain, Mute, Solo"),
                ("Oversampling", "Up to 8x"),
                ("License", "Single-user perpetual license, one key activates up to 3 computers"),
                ("Demo", "Full plugin, short noise burst every 45 seconds"),
            ],
            "feat_title": "3-band saturation features",
            "features": [
                "<strong>3-band processing:</strong> independent low, mid and high control with two adjustable crossovers. Drive your bass hard while keeping highs clean",
                "<strong>Five saturation types</strong>, chosen per band: Hard Clip (aggressive, loud, surgical), Wavefolder (metallic, synthetic, alien), "
                "Tube (warm, rounded, musical), Diode (asymmetric, gritty bite), Tape (glue, smear, vintage drive)",
                "<strong>Per band</strong> Drive, Mix, Gain, Mute and Solo, plus output gain and bypass",
                "<strong>Oversampling up to 8x</strong> for clean, alias-free saturation even when you push hard",
                "Designed by an active hitech and psycore producer for real sessions: mix, master, destroy",
            ],
            "extra_prose": "<h3>How it works</h3><ol>"
                           "<li><strong>Split:</strong> set the low/mid and mid/high crossover points to carve your signal into three independent bands.</li>"
                           "<li><strong>Saturate:</strong> choose a saturation type per band and push drive. Add weight to lows, bite to mids, air and edge to highs.</li>"
                           "<li><strong>Balance:</strong> blend with per-band mix, trim gain, solo to audition, and use oversampling to keep it all clean.</li></ol>"
                           "<h3>Why 3-band saturation?</h3>"
                           "<p>Harmonic saturation adds musical overtones to a sound, so it feels louder, warmer and more present. Instead of saturating the whole signal at once, "
                           "Crucible gives every band its own character: a hard clip into sub and kick for low-end punch, a gentle tube on the leads in the mids, tape on the highs, "
                           "all in a single instance. Crucible was forged for the fast and the dark, but works anywhere you would reach for a saturator: "
                           "drum &amp; bass, techno, dubstep, hip-hop, rock and mastering.</p>",
            "good_to_know": "After purchase your Gumroad receipt contains a personal license key. Paste it into Crucible once (Activate button, internet needed for this step); "
                            "one key activates up to 3 of your computers. Crucible re-checks the license in the background every two weeks and keeps working offline for up to 60 days. "
                            "Until activated it behaves like the free demo.",
            "formats": "<strong>Windows 10 or newer:</strong> VST3 + standalone, in any VST3 host such as REAPER, Ableton Live 12+, Cubase 12+, Studio One 6+, FL Studio and Bitwig. "
                       "There is no macOS build of Crucible. See the Gumroad page for the latest system requirements.",
            "faq": [
                ("What is Crucible?",
                 "Crucible is a 3-band harmonic saturation plugin by Code Chaos Audio. It splits your signal into low, mid and high bands and lets you saturate each band independently "
                 "with five selectable types (Hard Clip, Wavefolder, Tube, Diode, Tape), per-band Drive, Mix, Gain, Mute and Solo, and oversampling up to 8x."),
                ("Is it good for psytrance, hitech and psycore?",
                 "Yes, it was built by an active hitech, psycore and darkpsy producer. Add warmth and weight to kicks and basslines in the low band while adding bite and presence "
                 "to leads and percussion up top, without muddying the mix."),
                ("What's the difference between the saturation types?",
                 "Hard Clip is aggressive, loud and surgical, great for pushing low-end punch. Wavefolder folds the waveform back on itself for metallic, synthetic overtones. "
                 "Tube is warm, rounded and musical for mids. Diode adds asymmetric, gritty bite. Tape adds glue, vintage smear and air. You can assign a different type to each band."),
                ("Does Crucible run on a Mac?",
                 "No. Crucible is a VST3 plugin and standalone app for Windows 10 or newer; there is no macOS build."),
                ("How does license activation work?",
                 "Your Gumroad receipt contains a personal license key. Paste it into Crucible once (Activate button, internet needed); one key activates up to 3 computers. "
                 "Crucible re-checks the license every two weeks and keeps working offline for up to 60 days."),
                ("Is there a free demo?",
                 "Yes. The Crucible demo on Gumroad is the full plugin with a short noise burst every 45 seconds."),
            ],
        },
    },
    {
        "slug": "shardstep", "live": True, "group": "psy", "name": "Shardstep", "price": 15,
        "category": "Stutter- und Glitch-Effekt", "sub": "Effekt-Plugin (VST3)", "os": "Windows 10/11, macOS (Apple Silicon)",
        "title": "Shardstep: Stutter & Tape Stop VST3 für Hitech | Code Chaos",
        "feat_title": "Funktionen: Stutter, Tape Stop, Gate und Crush",  # war von Hand in der HTML (Commit 001f1a5), jetzt im Generator
        "desc": "Shardstep: Stutter- und Glitch-Effekt für 200–300 BPM. 16-Step-Pattern, Repeats bis 1/64, Tape Stop, MIDI-Trigger. VST3 Win + Mac, 15 €, Gratis-Demo.",
        "h1": "Shardstep: Stutter-, Glitch- und Tape-Stop-Plugin für Hitech und Psycore",
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
        "slug": "psy-kick-bass", "live": True, "group": "psy", "name": "Kick+Bass Engine", "price": 24,
        "category": "Kick- und Rolling-Bass-Instrument", "sub": "Instrument (VST3)", "os": "Windows 10/11, macOS (Apple Silicon)",
        "title": "Kick+Bass Engine: Psytrance Kick & Rolling Bass VST3 | Code Chaos",
        "desc": "Kick+Bass Engine: Kick und Rolling Bass in einem Plugin für 140–300+ BPM. Kick auf den Bass gestimmt, 0 ms Overlap im Test, 8 Patterns. VST3 Win + Mac, 24 €, Gratis-Demo.",
        "h1": "Kick+Bass Engine: Psytrance-Kick und Rolling Bass in einem Plugin",
        "eyebrow": "Code Chaos Audio · Instrument",
        "teaser": "Kick und Rolling Bass in einem Plugin: Kick auf den Bass gestimmt, endet vor der ersten Bassnote.",
        "answer": "Die Kick+Bass Engine spielt den Kick und den Rolling Bass eines Psytrance-, Hitech- oder Psycore-Tracks aus einem Plugin, damit beide aufeinander abgestimmt sind. "
                  "Der Kick übernimmt die Tonhöhe der Bassnote und endet tempoabhängig vor der ersten Bassnote des Patterns. "
                  "Im Test lag die Kick-Energie nach dem Bass-Einsatz bei 145 bis 250 BPM bei 0 ms, mit festem 330-ms-Kick waren es 180 bis 244 ms.",
        "gui_alt": "Oberfläche der Kick+Bass Engine: Pattern und Timing, Kick-Scope mit Kick und Bass übereinander, Kick Designer, Bass Engine und Mix",
        "gui_w": 2280, "gui_h": 1324,
        "audio_mode": "single",
        "audio": [
            {"src": "plugins/psy-kick-bass/demo/fullon_145bpm.wav", "file": "fullon-145.mp3", "label": "Full-On Rolling · 145 BPM"},
            {"src": "plugins/psy-kick-bass/demo/hitech_200bpm.wav", "file": "hitech-200.mp3", "label": "Hitech Machine 180 · 200 BPM"},
        ],
        "audio_intro": "Zwei Ausschnitte, direkt aus dem Plugin gerendert (acht Takte, Bassline F#1 F#1 A1 F#1 F#1 F#1 B1 G#1).",
        "audio_note": "Gerendert mit dem Plugin-Code selbst, ohne Nachbearbeitung.",
        "specs": [
            ("Typ", "Kick- und Rolling-Bass-Instrument, MIDI-Eingang"),
            ("Preis", "24 € auf Gumroad"),
            ("Formate", "VST3 + Standalone"),
            ("Systeme", "Windows 10/11 · macOS nur Apple Silicon (unsigniert)"),
            ("Nicht unterstützt", "AU / Logic Pro, Intel-Macs"),
            ("Tempo", "140 bis 300+ BPM, Fallback-BPM 60 bis 320 ohne Host-Tempo"),
            ("Presets", "14 Factory-Presets"),
            ("Demo", "vollständiges Plugin, kurzes Rauschen alle 45 Sekunden"),
        ],
        "features": [
            "<strong>Kick-Designer:</strong> Click (Rauschen + Ton, 1 bis 9 kHz), Body mit Pitch-Hüllkurve, phasenstarker Sub, vier Drive-Kurven (Soft, Tube, Hard, Fold), Länge und Tune",
            "<strong>Auto-Tune:</strong> Der Kick folgt der Bassnote (Root Note oder gehaltene MIDI-Note), in den Bereich von 38 bis 76 Hz gefaltet, plus Tune von ±12 Halbtönen",
            "<strong>Tempoabhängiges Kick-Ende:</strong> Die Engine findet den nächsten Bass-Einsatz und beendet den Kick dort mit einer kurzen Überblendung, optional mit Kick/Bass Gap von 0 bis 20 ms. Abschaltbar für manuelle Länge",
            "<strong>Phasen-Ausrichtung:</strong> Der Bass-Oszillator setzt die Phase der Kick-Grundwelle an der Übergabe fort (schaltbar)",
            "<strong>8 Rolling-Patterns:</strong> KBBB 1/16, Triplet Roll, 32nd Roll, Off-Beat, Gallop, Skip Roll, Double Kick, Kick Only. Der Bass duckt im Plugin unter den Kick (Depth, Release)",
            "<strong>4 Bass-Modi:</strong> Rubber, Plock, Growl, FM, je mit Filter-Hüllkurve pro Note, Drive, Sub, Width und Notenlänge. 4-faches Oversampling und polyBLEP-Oszillatoren",
            "Mono unter 150 Hz (einstellbar von 20 bis 300 Hz), der obere Bass bleibt breit",
            "Eingebautes Scope: der letzte Beat mit Kick über Bass, Marker am ersten Basston und Overlap in ms",
            "MIDI-Noten setzen die Bass-Tonhöhe und starten das Pattern; es läuft auch vom DAW-Transport",
            "14 Factory-Presets für Full-On, Darkpsy, Forest, Hitech und Psycore plus ein Kick-Lab-Preset",
        ],
        "tested": "27 automatische Prüfungen: jedes Factory-Preset bei 145, 200 und 260 BPM ohne NaN, ohne Spitzen über −0,3 dBFS und ohne Gleichspannung. "
                  "Der Kick wurde einzeln gemessen (Schwelle −60 dBFS): Mit automatischem Kick-Ende lag die Kick-Energie nach dem ersten Bass bei 145, 175, 200 und 250 BPM in allen Bass-Patterns bei 0,000 ms; "
                  "mit festem 330-ms-Kick waren es im KBBB-Pattern 226, 244, 225 und 180 ms. Die Phase von Kick und Bass an der Übergabe lag mit Phasen-Ausrichtung bei höchstens 21°, ohne bei bis zu 176°. "
                  "Aliasing des Basses lag im Bereich 10 Hz bis 20 kHz bei −73 dB oder besser (Filter-Cutoff intern auf 12 kHz begrenzt). "
                  "Der Klang wurde bei diesen Tests nicht nach Gehör beurteilt, hör dir deshalb zuerst die Demo an. Noch nicht in jeder DAW ausprobiert: Wenn etwas in deiner nicht funktioniert, sag Bescheid.",
        "good_to_know": "Bei 250 BPM bleiben dem Kick im 1/16-Pattern nur 60 ms; im Auto-Modus kürzt die Engine dann seinen Ausklang, er bleibt ein kurzer, knackiger Schlag. "
                        "Das Plugin ist ein Instrument und bearbeitet kein Audio, das du hineinschickst. Die Standalone-App hat keinen Transport, dort spielst du es mit MIDI-Noten.",
        "formats": MAC_FORMATS + " Die Vollversion wird einmalig mit dem Lizenzschlüssel aus deiner Gumroad-Quittung aktiviert (Internet nötig, bis zu 3 Rechner, Prüfung alle 14 Tage, 60 Tage offline nutzbar). Ohne Aktivierung verhält sie sich wie die Demo.",
        "faq": [
            ("Brauche ich Sidechain für die Kick+Bass Engine?",
             "Nein. Der Bass duckt im Plugin selbst unter den Kick (Depth und Release), und der Kick endet vor der ersten Bassnote des Patterns."),
            ("Wird der Kick auf den Bass gestimmt?",
             "Ja. Mit Auto-Tune folgt das Kick-Ende der Bassnote (Root Note oder gehaltene MIDI-Note), plus Tune von ±12 Halbtönen. Die Abweichung lag im Test unter 0,3 Cent."),
            ("Läuft sie auch ohne DAW-Tempo?",
             "Ja, dann gilt der Fallback-BPM-Wert von 60 bis 320. Mit Host-Tempo hat das Tempo der DAW Vorrang."),
            ("Läuft die Kick+Bass Engine auf dem Mac?", MAC_FAQ),
            ("Wie aktiviere ich die Vollversion?",
             "Im Plugin-Kopf auf „Activate“ klicken und den Lizenzschlüssel aus der Gumroad-Quittung eintragen (einmalig, Internet nötig). Ein Schlüssel gilt für bis zu 3 Rechner, das Plugin prüft ihn alle 14 Tage im Hintergrund und läuft 60 Tage offline weiter. Ohne Aktivierung verhält es sich wie die Demo, bei Rückerstattung oder Rückbuchung endet die Lizenz. Die Demo braucht keinen Schlüssel."),
            ("Gibt es eine kostenlose Demo?",
             "Ja, die Kick+Bass Engine Demo auf Gumroad ist das vollständige Plugin mit einem kurzen Rauschen alle 45 Sekunden."),
        ],
        "related": ["kick-bass-scope", "chaos-fm", "shardstep"],
    },
    {
        "slug": "chaos-fm", "live": True, "group": "psy", "name": "Chaos FM", "price": 19,
        "category": "FM-Synthesizer", "sub": "Instrument (VST3)", "os": "Windows 10/11",
        "title": "Chaos FM: FM-Synth VST3 für Hitech & Psycore | Code Chaos",
        "desc": "Chaos FM: 3-Operator-FM-Synth für Hitech, Psycore und Darkpsy mit GENERATE-Knopf und 12 Presets. VST3 + Standalone für Windows, 19 €, Gratis-Demo.",
        "h1": "Chaos FM: FM-Synth für Hitech, Psycore und Darkpsy",
        "eyebrow": "Code Chaos Audio · Instrument",
        "teaser": "3-Operator-FM-Synth mit GENERATE-Knopf für Leads, Bässe, Acid, Stabs, Plucks und FX.",
        "answer": "Chaos FM ist der FM-Synth-VST hinter dem Code-Chaos-Sound (VST3 + Standalone für Windows, mit kostenloser Demo): drei Operatoren, drei Algorithmen und ein großer <strong>GENERATE</strong>-Knopf, "
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
        "title": "Kick/Bass Scope: Kick & Bass Phase prüfen – gratis VST3",
        "desc": "Kostenloses VST3: Kick/Bass Scope zeigt Kick und Bass übereinander im Takt deiner DAW und warnt bei Gegenphasigkeit. Peaks in dBFS, Clip-Linie. Win + Mac.",
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
        "extra_sections": [
            ("Phase Alignment: erkennen statt raten",
             "<p>Ob Kick und Bass phasenrichtig zusammenspielen, hörst du auf Kopfhörern oft nicht, auf einer großen Anlage dafür umso deutlicher: Der Druck fehlt genau dort, wo beide gleichzeitig klingen. "
             "Kick/Bass Scope macht das sichtbar. Die <strong>Kick/Bass-Korrelation</strong> (−1 bis +1) wird nur dort gemessen, wo beide tatsächlich spielen, "
             "bei Gegenphasigkeit erscheint eine klare Warnung, und die Überlappungszeit pro Fenster steht in Millisekunden daneben.</p>"
             "<p><strong>Wichtig:</strong> Das Scope ist ein Analyzer. Es verschiebt nichts, dreht keine Phase und verändert dein Audio nicht (der Ausgang ist bitgenau gleich dem Eingang). "
             "Ausrichten tust du beim Mischen in deiner DAW, das Scope zeigt dir sofort, ob die Änderung geholfen hat. "
             "Was nach dem Mix noch an Druck und Lautheit fehlt, ist Sache des Masterings: <a href=\"/mastering/\">Mastering für Psytrance, Hitech und Psycore →</a></p>"),
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
        "title": "Gravesaw: Black-Metal-Amp-Sim (VST3) | Code Chaos",
        "feat_title": "Funktionen der Black-Metal-Amp-Sim",
        "desc": "Gravesaw: Black-Metal-Amp-Sim mit eingebauter Box für Gitarre und Bass-DI. 19 Cabs, 16 Presets, VST3 + Standalone für Windows und macOS. 19 €, Gratis-Demo.",
        "h1": "Gravesaw: Black-Metal-Amp mit eingebauter Box",
        "eyebrow": "Code Chaos Audio · Black Metal Suite",
        "teaser": "Black-Metal-Amp mit eingebauter Box für Gitarre und Bass-DI, von rau und sägend bis dick.",
        "answer": "Gravesaw ist eine Black-Metal-Amp-Sim: ein Amp mit eingebauter Box (Cab). Du steckst ein Gitarren- oder Bass-DI ein und bekommst den kalten, sägenden, "
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
        "slug": "frostfret", "live": True, "group": "metal", "name": "Frostfret", "price": 29,
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
        "slug": "hoarfell", "live": True, "group": "metal", "name": "Hoarfell", "price": 17,
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

GROUPS = [
    ("psy", "Für Hitech, Psycore und Darkpsy",
     "Gebaut für schnelle, dichte Psytrance-Produktionen: Sättigung, Glitch, FM-Sounds und Kontrolle über Kick und Bass."),
    ("metal", "Für Black Metal: die Code Chaos Black Metal Suite",
     "Amp, Hall und Atmosphäre für einen kalten, rauen Black-Metal-Sound aus dem Heimstudio."),
]

# Genre-Seite (DE) → passende Plugins (nur live gebaute Seiten werden verlinkt)
GENRE_PLUGINS = {
    "psycore": ["psy-kick-bass", "shardstep", "chaos-fm", "kick-bass-scope", "crucible"],
    "hitech-psytrance": ["psy-kick-bass", "shardstep", "chaos-fm", "kick-bass-scope", "crucible"],
    "darkpsy": ["psy-kick-bass", "chaos-fm", "kick-bass-scope", "crucible", "shardstep"],
}
