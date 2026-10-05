#!/usr/bin/env python3
"""Bing Webmaster Tools API: Site anlegen, verifizieren, Sitemap + URLs einreichen, Suchanfragen abrufen.

API-Key (Bing Webmaster Tools > Einstellungen > API-Zugriff) NIE ins Repo. Aufruf:
  BING_API_KEY_FILE=/pfad/key.txt python3 _build/bing_webmaster.py status
  BING_API_KEY_FILE=... python3 _build/bing_webmaster.py add      # Site anlegen + Meta-Code ausgeben
  BING_API_KEY_FILE=... python3 _build/bing_webmaster.py verify   # nach Deploy des msvalidate.01-Tags
  BING_API_KEY_FILE=... python3 _build/bing_webmaster.py submit   # Sitemap + alle Sitemap-URLs
  BING_API_KEY_FILE=... python3 _build/bing_webmaster.py queries  # Suchanfragen (Bing, Copilot, ChatGPT-Suche)
Optional SITE=https://polished.media/ für eine andere Property.
"""
import json, os, re, sys, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://ssl.bing.com/webmaster/api.svc/json/"
SITE = os.environ.get("SITE", "https://codechaos-official.de/")


def key():
    f = os.environ.get("BING_API_KEY_FILE")
    k = open(f).read().strip() if f else os.environ.get("BING_API_KEY")
    return k or sys.exit("BING_API_KEY_FILE oder BING_API_KEY setzen.")


def call(method, http="GET", body=None, **params):
    q = urllib.parse.urlencode({**params, "apikey": key()})
    req = urllib.request.Request(f"{API}{method}?{q}", method=http,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            t = r.read().decode()
            return json.loads(t).get("d") if t.strip() else None
    except urllib.error.HTTPError as e:
        sys.exit(f"{method}: HTTP {e.code} {e.read().decode()[:300]}")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "status":
        for s in call("GetUserSites") or []:
            print(f'{s.get("Url"):40} verifiziert: {s.get("IsVerified")}  Meta-Code: {s.get("AuthenticationCode")}')
    elif cmd == "add":
        call("AddSite", "POST", {"siteUrl": SITE})
        for s in call("GetUserSites") or []:
            if s.get("Url", "").rstrip("/") == SITE.rstrip("/"):
                print("In <head> einfügen:", f'<meta name="msvalidate.01" content="{s.get("AuthenticationCode")}">')
    elif cmd == "verify":
        print("Verifiziert:", call("VerifySite", "POST", {"siteUrl": SITE}))
    elif cmd == "submit":
        sitemap = SITE.rstrip("/") + "/sitemap.xml"
        call("SubmitFeed", "POST", {"siteUrl": SITE, "feedUrl": sitemap}); print("Sitemap eingereicht:", sitemap)
        urls = re.findall(r"<loc>(.*?)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read())
        if SITE.startswith("https://codechaos-official.de"):
            call("SubmitUrlBatch", "POST", {"siteUrl": SITE, "urlList": urls}); print(len(urls), "URLs eingereicht")
    elif cmd == "queries":
        rows = call("GetQueryStats", siteUrl=SITE) or []
        agg = {}
        for r in rows:
            a = agg.setdefault(r["Query"], [0, 0, 0.0])
            a[0] += r.get("Impressions", 0); a[1] += r.get("Clicks", 0); a[2] += r.get("AvgImpressionPosition", 0) * r.get("Impressions", 0)
        for q, (i, c, p) in sorted(agg.items(), key=lambda x: -x[1][0])[:40]:
            print(f"{q[:45]:45} Impr {i:5}  Klicks {c:4}  Pos {p / i if i else 0:.1f}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
