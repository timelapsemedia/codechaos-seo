#!/usr/bin/env python3
"""Meldet alle URLs aus sitemap.xml per IndexNow an Bing, Yandex, Seznam & Co.
(Bing-Index ist Grundlage für ChatGPT-Suche und Copilot.)
Aufruf nach einem Deploy:  python3 _build/indexnow_ping.py
"""
import json, os, re, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = open(os.path.join(ROOT, "_build", "indexnow_key.txt")).read().strip()
urls = re.findall(r"<loc>(.*?)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read())
body = json.dumps({"host": "codechaos-official.de", "key": KEY,
                   "keyLocation": f"https://codechaos-official.de/{KEY}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("IndexNow:", r.status, f"({len(urls)} URLs)")
