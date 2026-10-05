#!/usr/bin/env python3
"""Plant alle Posts aus crucible-posts.json in Buffer ein, auf allen verbundenen Kanälen.

Ein Lauf genügt: Buffer veröffentlicht dann selbst zum jeweiligen Datum (17:00 Uhr Berlin).

API-Key (Buffer > Settings > API) als Umgebungsvariable, einer dieser Namen:
  BUFFER_API_KEY, BUFFER_ACCESS_TOKEN, BUFFER_TOKEN

  python3 _marketing/buffer_schedule.py --dry-run   # zeigt Kanäle und Plan, postet nichts
  python3 _marketing/buffer_schedule.py             # plant ein

Bereits eingeplante Kombinationen (Post + Kanal) stehen in _marketing/buffer_scheduled.json
und werden beim nächsten Lauf übersprungen.

Instagram und YouTube werden NICHT über Buffer gepostet (dafür gibt es post_instagram.py und
post_youtube.py). Mit --all-channels werden sie trotzdem einbezogen.

Kanal-Logik:
  instagram            Bild als Feed-Post, volle Caption
  youtube              Video als Short (nur Posts mit Video), Titel + Caption, Kategorie Musik
  tiktok               Video (nur Posts mit Video), volle Caption
  twitter/threads/bluesky/mastodon   Bild + Kurztext (<= 280 Zeichen)
  facebook/linkedin    Bild + volle Caption
"""
import datetime, json, os, sys, urllib.request
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://api.buffer.com"
POST_TIME = datetime.time(17, 0)
TZ = ZoneInfo("Europe/Berlin")


def key():
    for n in ("BUFFER_API_KEY", "BUFFER_ACCESS_TOKEN", "BUFFER_TOKEN"):
        if os.environ.get(n):
            return os.environ[n]
    return None


def gql(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=body, headers={"Authorization": "Bearer " + key(), "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], ensure_ascii=False))
    return data["data"]


def channels():
    orgs = gql("query { account { organizations { id name } } }")["account"]["organizations"]
    out = []
    for o in orgs:
        q = "query($id: OrganizationId!) { channels(input: { organizationId: $id }) { id name service } }"
        try:
            out += gql(q, {"id": o["id"]})["channels"]
        except RuntimeError:  # ältere Schemas typisieren die ID als String
            q = q.replace("OrganizationId!", "String!")
            out += gql(q, {"id": o["id"]})["channels"]
    return out


def plan_for(post, ch):
    s = ch["service"].lower()
    img = [{"image": {"url": post["image"]}}]
    vid = [{"video": {"url": post["video"], "metadata": {"thumbnailOffset": 1000}}}] if post.get("video") else None
    if s == "instagram":
        return dict(text=post["caption"], assets=img, metadata={"instagram": {"type": "post", "shouldShareToFeed": True}})
    if s == "youtube":
        if not vid:
            return None
        return dict(text=post["caption"], assets=vid,
                    metadata={"youtube": {"title": post["video_title"][:100], "categoryId": "10", "privacy": "public", "madeForKids": False}})
    if s == "tiktok":
        return dict(text=post["caption"], assets=vid) if vid else None
    if s in ("twitter", "threads", "bluesky", "mastodon"):
        return dict(text=post["short"], assets=img)
    if s in ("facebook", "linkedin"):
        return dict(text=post["caption"], assets=img)
    return None


MUTATION = """mutation($input: CreatePostInput!) {
  createPost(input: $input) {
    ... on PostActionSuccess { post { id dueAt } }
    ... on MutationError { message }
  }
}"""


def main():
    dry = "--dry-run" in sys.argv
    if not key():
        print("Buffer: kein API-Key gesetzt, übersprungen.")
        return 0
    skip = set() if "--all-channels" in sys.argv else {"instagram", "youtube"}
    posts = json.load(open(os.path.join(HERE, "crucible-posts.json"), encoding="utf-8"))
    state_path = os.path.join(HERE, "buffer_scheduled.json")
    state = json.load(open(state_path)) if os.path.exists(state_path) else {}
    chans = [c for c in channels() if c["service"].lower() not in skip]
    print("Buffer-Kanäle:", ", ".join(f'{c["service"]} ({c["name"]})' for c in chans) or "keine")
    now = datetime.datetime.now(datetime.timezone.utc)
    errors = 0
    for post in posts:
        due = datetime.datetime.combine(datetime.date.fromisoformat(post["date"]), POST_TIME, TZ).astimezone(datetime.timezone.utc)
        if due <= now:
            print(f'- {post["id"]}: Termin {post["date"]} liegt in der Vergangenheit, übersprungen')
            continue
        for ch in chans:
            k = f'{post["id"]}::{ch["id"]}'
            if k in state:
                continue
            p = plan_for(post, ch)
            if not p:
                print(f'- {post["id"]} → {ch["service"]}: kein passendes Format, übersprungen')
                continue
            label = f'{post["id"]} → {ch["service"]} ({ch["name"]}) am {due.astimezone(TZ):%d.%m.%Y %H:%M}'
            if dry:
                print("WÜRDE EINPLANEN:", label)
                continue
            inp = {"channelId": ch["id"], "schedulingType": "automatic", "mode": "customScheduled",
                   "dueAt": due.strftime("%Y-%m-%dT%H:%M:%S.000Z"), **p}
            try:
                res = gql(MUTATION, {"input": inp})["createPost"]
            except Exception as e:  # noqa: BLE001
                res = {"message": str(e)}
            if res.get("post"):
                state[k] = res["post"]["id"]
                json.dump(state, open(state_path, "w"), indent=1)
                print("EINGEPLANT:", label)
            else:
                errors += 1
                print("FEHLER:", label, "-", res.get("message"))
    return errors


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
