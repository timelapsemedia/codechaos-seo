#!/usr/bin/env python3
"""Kopiert CSS-Dateien inline in die Startseite (Grok #67: kein render-blockierendes CSS auf index.html).

<style data-src="/css/start.css">…</style> wird mit dem aktuellen Inhalt von css/start.css gefüllt.
Quelle der Wahrheit sind die CSS-Dateien; Aufruf aus dem Repo-Root: python _build/inline_css.py
(läuft automatisch am Ende von build_pages.py)."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEITEN = ["index.html"]


def css_min(t):
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    t = re.sub(r"\s*\n\s*", "\n", t)
    return t.strip()


def lauf():
    for datei in SEITEN:
        p = os.path.join(ROOT, datei)
        h = open(p, encoding="utf-8").read()
        def rep(m):
            src = m.group(1)
            css = open(os.path.join(ROOT, src.lstrip("/")), encoding="utf-8").read()
            return f'<style data-src="{src}">\n{css_min(css)}\n</style>'
        h2, n = re.subn(r'<style data-src="([^"]+)">.*?</style>', rep, h, flags=re.S)
        open(p, "w", encoding="utf-8", newline="\n").write(h2)
        print(datei, n, "CSS-Dateien inline")


if __name__ == "__main__":
    lauf()
