#!/usr/bin/env python3
"""Meldet alle URLs aus sitemap.xml per IndexNow an Bing, Yandex, Seznam, Naver, Amazon, Yep (+ api.indexnow.org).
(Bing-Index ist Grundlage für ChatGPT-Suche und Copilot.)
Aufruf nach einem Deploy:  python3 _build/indexnow_ping.py
"""
import json, os, re, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = open(os.path.join(ROOT, "_build", "indexnow_key.txt")).read().strip()
urls = re.findall(r"<loc>(.*?)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read())
body = json.dumps({"host": "codechaos-official.de", "key": KEY,
                   "keyLocation": f"https://codechaos-official.de/{KEY}.txt", "urlList": urls}).encode()
ENDPOINTS = ["https://api.indexnow.org/indexnow", "https://www.bing.com/indexnow", "https://yandex.com/indexnow",
             "https://search.seznam.cz/indexnow", "https://searchadvisor.naver.com/indexnow",
             "https://indexnow.amazonbot.amazon/indexnow", "https://indexnow.yep.com/indexnow"]
for ep in ENDPOINTS:
    try:
        req = urllib.request.Request(ep, data=body, headers={"Content-Type": "application/json; charset=utf-8"})
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"{ep}: {r.status} ({len(urls)} URLs)")
    except Exception as e:  # noqa: BLE001
        print(f"{ep}: {e}")
