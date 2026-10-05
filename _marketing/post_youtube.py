#!/usr/bin/env python3
"""Lädt die Crucible-Videos als YouTube Shorts hoch und plant sie per publishAt (17:00 Berlin) ein.

Ein Lauf genügt: Zukünftige Termine werden als „geplant“ hochgeladen, YouTube veröffentlicht selbst.
Bereits hochgeladene Posts stehen in _marketing/youtube_uploaded.json.

Zugang: Hochladen braucht OAuth (ein reiner API-Key reicht dafür nicht).
  YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN   (empfohlen, erneuert sich selbst)
  oder YOUTUBE_ACCESS_TOKEN                                         (kurzlebig, ca. 1 Stunde)
Scope des Tokens: https://www.googleapis.com/auth/youtube.upload

  python3 _marketing/post_youtube.py --dry-run
  python3 _marketing/post_youtube.py
"""
import datetime, json, os, sys, urllib.error, urllib.parse, urllib.request, uuid
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TZ = ZoneInfo("Europe/Berlin")
BASE = "https://codechaos-official.de/"


def env(n):
    return os.environ.get(n) or None


def access_token():
    if env("YOUTUBE_REFRESH_TOKEN") and env("YOUTUBE_CLIENT_ID") and env("YOUTUBE_CLIENT_SECRET"):
        data = urllib.parse.urlencode({"client_id": env("YOUTUBE_CLIENT_ID"), "client_secret": env("YOUTUBE_CLIENT_SECRET"),
                                       "refresh_token": env("YOUTUBE_REFRESH_TOKEN"), "grant_type": "refresh_token"}).encode()
        with urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=data), timeout=60) as r:
            return json.load(r)["access_token"]
    return env("YOUTUBE_ACCESS_TOKEN")


def local_file(url):
    return os.path.join(ROOT, url.replace(BASE, "").lstrip("/"))


def upload(token, path, meta):
    boundary = uuid.uuid4().hex
    video = open(path, "rb").read()
    body = (f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{json.dumps(meta)}\r\n"
            f"--{boundary}\r\nContent-Type: video/mp4\r\n\r\n").encode() + video + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request("https://www.googleapis.com/upload/youtube/v3/videos?uploadType=multipart&part=snippet,status",
                                 data=body, headers={"Authorization": "Bearer " + token, "Content-Type": f"multipart/related; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.load(r)["id"]
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code} {e.read().decode(errors='replace')}") from None


def main():
    dry = "--dry-run" in sys.argv
    posts = [p for p in json.load(open(os.path.join(HERE, "crucible-posts.json"), encoding="utf-8")) if p.get("video")]
    state_path = os.path.join(HERE, "youtube_uploaded.json")
    state = json.load(open(state_path)) if os.path.exists(state_path) else {}
    todo = [p for p in posts if p["id"] not in state]
    if not todo:
        print("YouTube: nichts zu tun.")
        return 0
    now = datetime.datetime.now(datetime.timezone.utc)
    token = None if dry else access_token()
    if not dry and not token:
        print("YouTube: keine OAuth-Zugangsdaten gesetzt, übersprungen.")
        return 0
    errors = 0
    for p in todo:
        due = datetime.datetime.combine(datetime.date.fromisoformat(p["date"]), datetime.time(17, 0), TZ).astimezone(datetime.timezone.utc)
        status = {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
        if due > now:
            status = {"privacyStatus": "private", "publishAt": due.strftime("%Y-%m-%dT%H:%M:%S.000Z"), "selfDeclaredMadeForKids": False}
        meta = {"snippet": {"title": (p["video_title"] + " #Shorts")[:100],
                            "description": p["caption"] + "\n\nCrucible: https://codechaos-official.de/crucible.html",
                            "tags": ["Crucible", "saturation plugin", "psytrance", "hitech", "psycore", "darkpsy", "Code Chaos"],
                            "categoryId": "10", "defaultLanguage": "de"},
                "status": status}
        label = f'{p["id"]} ({"geplant für " + due.astimezone(TZ).strftime("%d.%m.%Y %H:%M") if "publishAt" in status else "sofort"})'
        if dry:
            print("YouTube WÜRDE HOCHLADEN:", label, local_file(p["video"]))
            continue
        try:
            vid = upload(token, local_file(p["video"]), meta)
            state[p["id"]] = vid
            json.dump(state, open(state_path, "w"), indent=1)
            print("YouTube HOCHGELADEN:", label, "-> https://youtu.be/" + vid)
        except Exception as e:  # noqa: BLE001
            errors += 1
            print("YouTube FEHLER:", label, "-", e)
    return errors


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
