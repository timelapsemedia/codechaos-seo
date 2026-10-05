#!/usr/bin/env python3
"""Postet fällige Einträge aus crucible-posts.json auf Instagram (Graph API, Business/Creator-Account).

Benötigte Umgebungsvariablen (niemals ins Repo committen):
  INSTAGRAM_ACCESS_TOKEN   Long-lived Token mit instagram_content_publish
  INSTAGRAM_USER_ID        ID des Instagram-Business-Accounts

Aufruf:  python3 _marketing/post_instagram.py            # postet alles, was heute fällig ist
         python3 _marketing/post_instagram.py --dry-run  # zeigt nur an
Bereits gepostete IDs landen in _marketing/posted.json.
"""
import datetime, json, os, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://graph.facebook.com/v21.0"

def call(path, **params):
    data = urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(urllib.request.Request(f"{API}/{path}", data=data), timeout=60) as r:
        return json.load(r)

def main():
    dry = "--dry-run" in sys.argv
    posts = json.load(open(os.path.join(HERE, "crucible-posts.json"), encoding="utf-8"))
    done_path = os.path.join(HERE, "posted.json")
    done = set(json.load(open(done_path))) if os.path.exists(done_path) else set()
    today = datetime.date.today().isoformat()
    due = [p for p in posts if p["date"] <= today and p["id"] not in done]
    if not due:
        print("Nichts fällig."); return
    if dry:
        for p in due: print("WÜRDE POSTEN:", p["id"], p["image"])
        return
    token, user = os.environ["INSTAGRAM_ACCESS_TOKEN"], os.environ["INSTAGRAM_USER_ID"]
    for p in due:
        container = call(f"{user}/media", image_url=p["image"], caption=p["caption"], access_token=token)["id"]
        time.sleep(5)
        media = call(f"{user}/media_publish", creation_id=container, access_token=token)["id"]
        print("Gepostet:", p["id"], "->", media)
        done.add(p["id"])
        json.dump(sorted(done), open(done_path, "w"), indent=1)

if __name__ == "__main__":
    main()
