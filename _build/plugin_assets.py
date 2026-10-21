#!/usr/bin/env python3
"""Kopiert Bilder und Demo-Audio der Plugin-Seiten aus dem Store-Repo in die Website.

Aufruf aus dem Repo-Root:  python3 _build/plugin_assets.py [/pfad/zu/codechaos-store]
Erzeugt je Plugin (nur Einträge mit live=True aus content_plugins.py):
  images/plugins/<slug>/gui-880.webp, gui-1600.webp, gui-880.jpg (Fallback), og.jpg (1200x630 aus cover.png)
  audio/plugins/<slug>/*.mp3 (160 kbit/s CBR, aus der WAV-Quelle, wenn vorhanden)
Braucht Pillow und ffmpeg. Der Ordner _build wird von GitHub Pages nicht veröffentlicht.
"""
import os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_plugins import PLUGINS  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(ROOT), "codechaos-store")


def resize(im, w):
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def images(p):
    src = os.path.join(STORE, "products", p["slug"])
    out = os.path.join(ROOT, "images", "plugins", p["slug"])
    os.makedirs(out, exist_ok=True)
    for name, extra in [("gui", p.get("gui_src", "gui.png"))] + [(i["name"], i["src"]) for i in p.get("extra_images", [])]:
        path = extra if os.path.isabs(extra) else os.path.join(src, extra)
        im = Image.open(path).convert("RGB")
        resize(im, 880).save(os.path.join(out, f"{name}-880.webp"), "WEBP", quality=82, method=6)
        resize(im, 880).save(os.path.join(out, f"{name}-880.jpg"), "JPEG", quality=82, optimize=True, progressive=True)
        if im.width >= 1600:
            resize(im, 1600).save(os.path.join(out, f"{name}-1600.webp"), "WEBP", quality=80, method=6)
    cov = Image.open(os.path.join(src, "cover.png")).convert("RGB")
    # 1280x720 -> 1200x675 -> mittig auf 1200x630 beschneiden (OG-Standardformat der Site)
    cov = resize(cov, 1200)
    top = (cov.height - 630) // 2
    cov.crop((0, top, 1200, top + 630)).save(os.path.join(out, "og.jpg"), "JPEG", quality=84, optimize=True, progressive=True)


def audio(p):
    out = os.path.join(ROOT, "audio", "plugins", p["slug"])
    for a in p.get("audio", []):
        os.makedirs(out, exist_ok=True)
        # "SITE:pfad" = Datei liegt bereits in diesem Repo (z. B. Social-Clip), sonst relativ zum Store-Repo
        src = os.path.join(ROOT, a["src"][5:]) if a["src"].startswith("SITE:") else os.path.join(STORE, a["src"])
        dst = os.path.join(out, a["file"])
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "2", "-ar", "44100",
                        "-codec:a", "libmp3lame", "-b:a", "160k", "-map_metadata", "-1", dst], check=True)


if __name__ == "__main__":
    for p in PLUGINS:
        if not p["live"]:
            print("übersprungen (nicht live):", p["slug"])
            continue
        images(p)
        audio(p)
        print("ok:", p["slug"])
