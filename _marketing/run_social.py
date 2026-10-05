#!/usr/bin/env python3
"""Ein Befehl für alles:  python3 _marketing/run_social.py [--dry-run]

- Instagram: postet fällige Posts direkt per Zugriffstoken (täglich ausführen)
- YouTube:   lädt die Shorts hoch und plant sie per publishAt ein (einmal reicht)
- Buffer:    plant alle übrigen verbundenen Kanäle (z. B. TikTok) ein (einmal reicht)
Fehlende Zugangsdaten werden übersprungen, nichts wird doppelt gepostet.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_instagram, post_youtube, buffer_schedule  # noqa: E402

errors = 0
for name, mod in (("Instagram", post_instagram), ("YouTube", post_youtube), ("Buffer", buffer_schedule)):
    print(f"=== {name}")
    try:
        errors += mod.main() or 0
    except Exception as e:  # noqa: BLE001
        errors += 1
        print(f"{name} FEHLER:", e)
sys.exit(1 if errors else 0)
