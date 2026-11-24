#!/usr/bin/env python3
"""Ein Befehl für alles:  python3 _marketing/run_social.py [--dry-run]

- Gate:      Sprach- und Markenprüfung (crucible_gate.py) vor allen Zielen, fail-closed
- Instagram: postet fällige Posts direkt per Zugriffstoken (täglich ausführen)
- YouTube:   lädt die Shorts hoch und plant sie per publishAt ein (einmal reicht)
- Buffer:    plant alle übrigen verbundenen Kanäle (z. B. TikTok) ein (einmal reicht)
Fehlende Zugangsdaten werden übersprungen, nichts wird doppelt gepostet.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
import crucible_gate  # noqa: E402

# Gate zuerst (Tim 21.11.2026: deutsche Black-Metal-Caption auf TikTok). Schlägt der Selbsttest fehl,
# geht in diesem Lauf nichts raus, auf keinem Ziel.
print("=== Gate (Sprache + Marke)")
try:
    selbsttest = crucible_gate._test()
except Exception as e:  # noqa: BLE001
    print("Gate FEHLER:", type(e).__name__, e)
    selbsttest = 1
if selbsttest:
    print("Gate-Selbsttest rot: nichts gepostet, nichts eingeplant.")
    sys.exit(1)
crucible_gate.bericht()

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
