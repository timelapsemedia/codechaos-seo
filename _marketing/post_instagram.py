#!/usr/bin/env python3
"""Postet fällige Einträge aus crucible-posts.json direkt auf Instagram (Graph API, Business/Creator-Account).

Instagram kann über die API nicht vorplanen. Deshalb postet das Skript nur, was heute oder
früher fällig und noch nicht gepostet ist. Täglich ausführen (GitHub Action oder lokal).

Zugang (Umgebungsvariablen, einer der Namen reicht):
  Token:    INSTAGRAM_ACCESS_TOKEN | IG_ACCESS_TOKEN | INSTAGRAM_TOKEN
  User-ID:  INSTAGRAM_USER_ID | IG_USER_ID   (optional, wird sonst über /me ermittelt)
Tokens mit "IGAA…" laufen über graph.instagram.com (Instagram Login),
alle anderen über graph.facebook.com (Facebook Login).

  python3 _marketing/post_instagram.py --dry-run
  python3 _marketing/post_instagram.py
"""
import datetime, json, os, sys, time, urllib.error, urllib.parse, urllib.request
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = "v21.0"


def env(*names):
    for n in names:
        if os.environ.get(n):
            return os.environ[n]
    return None


def call(host, path, method="GET", **params):
    url = f"https://{host}/{VERSION}/{path}"
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url + ("?" + data.decode() if method == "GET" else ""), data=None if method == "GET" else data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code} {e.read().decode(errors='replace')}") from None


def main():
    dry = "--dry-run" in sys.argv
    posts = json.load(open(os.path.join(HERE, "crucible-posts.json"), encoding="utf-8"))
    done_path = os.path.join(HERE, "posted.json")
    done = set(json.load(open(done_path))) if os.path.exists(done_path) else set()
    today = datetime.datetime.now(ZoneInfo("Europe/Berlin")).date().isoformat()
    due = [p for p in posts if p["date"] <= today and p["id"] not in done]
    if not due:
        print("Instagram: nichts fällig.")
        return 0
    if dry:
        for p in due:
            print("Instagram WÜRDE POSTEN:", p["id"], p["image"])
        return 0
    token = env("INSTAGRAM_ACCESS_TOKEN", "IG_ACCESS_TOKEN", "INSTAGRAM_TOKEN")
    if not token:
        print("Instagram: kein Token gesetzt, übersprungen.")
        return 0
    host = "graph.instagram.com" if token.startswith("IG") else "graph.facebook.com"
    user = env("INSTAGRAM_USER_ID", "IG_USER_ID")
    if not user:
        me = call(host, "me", fields="user_id,id,username", access_token=token)
        user = me.get("user_id") or me["id"]
    errors = 0
    for p in due:
        try:
            cid = call(host, f"{user}/media", "POST", image_url=p["image"], caption=p["caption"], access_token=token)["id"]
            for _ in range(30):  # warten, bis Instagram das Bild verarbeitet hat
                st = call(host, cid, fields="status_code", access_token=token).get("status_code")
                if st in ("FINISHED", None):
                    break
                if st == "ERROR":
                    raise RuntimeError("Container-Status ERROR")
                time.sleep(5)
            media = call(host, f"{user}/media_publish", "POST", creation_id=cid, access_token=token)["id"]
            print("Instagram GEPOSTET:", p["id"], "->", media)
            done.add(p["id"])
            json.dump(sorted(done), open(done_path, "w"), indent=1)
        except Exception as e:  # noqa: BLE001
            errors += 1
            print("Instagram FEHLER:", p["id"], "-", e)
    return errors


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
