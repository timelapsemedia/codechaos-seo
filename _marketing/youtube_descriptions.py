#!/usr/bin/env python3
"""Ergänzt YouTube-Videobeschreibungen und die Kanal-Info um Links zu den Genre-Guides.

Zugang: OAuth mit Scope https://www.googleapis.com/auth/youtube (nicht nur youtube.upload):
  YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN
Ein reiner API-Key reicht zum Schreiben NICHT.

  python3 _marketing/youtube_descriptions.py           # Probelauf: zeigt nur, was geändert würde
  python3 _marketing/youtube_descriptions.py --apply   # schreibt die Änderungen

Jedes Video bekommt höchstens einen Block (erkennbar an „codechaos-official.de/“), doppelte Läufe ändern nichts.
"""
import json, os, re, sys, urllib.error, urllib.parse, urllib.request

API = "https://www.googleapis.com/youtube/v3/"
SITE = "https://codechaos-official.de"
GENRES = [  # (Muster im Titel/Beschreibung, Zeile)
    (r"psycore|psy-core|slaughterhouse|roadside butchery|filaments|abstrakte musik|rotten soil",
     f"Was ist Psycore? → {SITE}/psycore/"),
    (r"hi-?tech|grudge|interstellar|ruins of humanity|heart ?& ?mind|parallax|tiny piece|tanzalarm|alternate future",
     f"Was ist Hitech Psytrance? → {SITE}/hitech-psytrance/"),
    (r"dark ?psy|oblivion|twilight zone|amanita",
     f"Was ist Darkpsy? → {SITE}/darkpsy/"),
]
FOOTER = f"\n\n—\nCode Chaos · Psycore, Hitech & Darkpsy aus Hamburg: {SITE}/\nMastering für Psycore, Hitech & Darkpsy: {SITE}/mastering/"
CHANNEL = (f"\n\nOffizielle Website: {SITE}/\nGenre-Guides: {SITE}/psycore/ · {SITE}/hitech-psytrance/ · {SITE}/darkpsy/\n"
           f"Mastering: {SITE}/mastering/ · Plugin Crucible: {SITE}/crucible.html")


def token():
    e = os.environ
    if not all(e.get(k) for k in ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN")):
        sys.exit("YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET und YOUTUBE_REFRESH_TOKEN setzen (OAuth, Scope youtube).")
    data = urllib.parse.urlencode({"client_id": e["YOUTUBE_CLIENT_ID"], "client_secret": e["YOUTUBE_CLIENT_SECRET"],
                                   "refresh_token": e["YOUTUBE_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    return json.load(urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=data), timeout=30))["access_token"]


TOK = None


def call(method, path, body=None, **params):
    url = API + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": "Bearer " + TOK, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path}: HTTP {e.code} {e.read().decode()[:300]}")


def main():
    global TOK
    apply = "--apply" in sys.argv
    TOK = token()
    ch = call("GET", "channels", part="snippet,contentDetails,brandingSettings", mine="true")["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    desc = ch["brandingSettings"]["channel"].get("description", "")
    if f"{SITE}/psycore/" not in desc:
        print("Kanal-Info: Website- und Guide-Links ergänzen")
        if apply:
            ch["brandingSettings"]["channel"]["description"] = (desc.rstrip() + CHANNEL)[:1000]
            call("PUT", "channels", {"id": ch["id"], "brandingSettings": ch["brandingSettings"]}, part="brandingSettings")
    ids, page = [], None
    while True:
        r = call("GET", "playlistItems", part="contentDetails", playlistId=uploads, maxResults=50, **({"pageToken": page} if page else {}))
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        page = r.get("nextPageToken")
        if not page:
            break
    changed = 0
    for i in range(0, len(ids), 50):
        for v in call("GET", "videos", part="snippet", id=",".join(ids[i:i + 50]))["items"]:
            sn = v["snippet"]; d = sn.get("description", "")
            if "codechaos-official.de/" in d:
                continue
            text = (sn["title"] + " " + d).lower()
            lines = [line for pat, line in GENRES if re.search(pat, text)]
            add = ("\n\n" + "\n".join(lines) if lines else "") + FOOTER
            print(f"{'ÄNDERN' if apply else 'WÜRDE ÄNDERN'}: {sn['title'][:70]}  (+{len(lines)} Genre-Zeile(n))")
            if apply:
                sn["description"] = (d.rstrip() + add)[:5000]
                body = {"id": v["id"], "snippet": {k: sn[k] for k in ("title", "description", "categoryId", "tags", "defaultLanguage") if k in sn}}
                call("PUT", "videos", body, part="snippet")
            changed += 1
    print(f"{changed} Video(s) {'geändert' if apply else 'betroffen (Probelauf)'} von {len(ids)}")


if __name__ == "__main__":
    main()
