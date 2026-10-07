#!/usr/bin/env python3
"""Instagram Graph API ohne Zusatzbibliotheken (urllib, UTF-8-sicher). Token kommt aus der Umgebung (IG_TOKEN), nie aus argv.

ig.py status
ig.py posten <json-auftrag>          {"typ":"bild|karussell|reel","medien":[url,...],"caption":"...","cover_url":opt}
ig.py insights <anzahl>
ig.py token_verlaengern
Umgebung: IG_TOKEN, IG_USER_ID, IG_API (facebook|instagram), IG_VERSION, IG_APP_ID, IG_APP_SECRET, IG_BASE (nur Tests)
"""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request

API = os.environ.get("IG_API", "facebook")
VERSION = os.environ.get("IG_VERSION", "v21.0")
BASE = os.environ.get("IG_BASE") or (f"https://graph.instagram.com/{VERSION}" if API == "instagram" else f"https://graph.facebook.com/{VERSION}")
TOKEN = os.environ.get("IG_TOKEN", "")
USER = os.environ.get("IG_USER_ID", "")

def out(d):
    print(json.dumps(d, ensure_ascii=False))

def call(method, path, params=None, versuche=3):
    params = dict(params or {}); params["access_token"] = TOKEN
    data = urllib.parse.urlencode(params).encode("utf-8")
    url = f"{BASE}/{path.lstrip('/')}"
    if method == "GET":
        req = urllib.request.Request(url + "?" + data.decode("utf-8"))
    else:
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"})
    for n in range(versuche):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            try:
                err = json.loads(body).get("error", {})
            except Exception:
                err = {"message": body[:300]}
            # Ratenlimit / vorübergehend: warten und erneut (code 4, 17, 32, 613, HTTP 429/5xx)
            if (e.code in (429, 500, 502, 503) or err.get("code") in (4, 17, 32, 613) or err.get("is_transient")) and n < versuche - 1:
                time.sleep(10 * (n + 1)); continue
            msg = str(err.get("message", "")).replace(TOKEN, "***") if TOKEN else err.get("message")
            raise RuntimeError(f"Graph API {e.code}: {msg} (code {err.get('code')}, subcode {err.get('error_subcode')})")
        except urllib.error.URLError as e:
            if n < versuche - 1:
                time.sleep(5); continue
            raise RuntimeError(f"Netzwerk: {e.reason}")

def warten(container, max_s=300):
    t = time.time()
    while time.time() - t < max_s:
        st = call("GET", container, {"fields": "status_code,status"})
        code = st.get("status_code")
        if code == "FINISHED": return
        if code in ("ERROR", "EXPIRED"): raise RuntimeError(f"Container {container}: {code} {st.get('status', '')}")
        time.sleep(5)
    raise RuntimeError(f"Container {container}: nach {max_s} s nicht fertig")

def posten(auftrag):
    typ, medien, caption = auftrag["typ"], auftrag["medien"], auftrag.get("caption", "")
    if typ == "bild":
        c = call("POST", f"{USER}/media", {"image_url": medien[0], "caption": caption})["id"]
    elif typ == "reel":
        p = {"media_type": "REELS", "video_url": medien[0], "caption": caption}
        if auftrag.get("cover_url"): p["cover_url"] = auftrag["cover_url"]
        c = call("POST", f"{USER}/media", p)["id"]
    elif typ == "karussell":
        if not 2 <= len(medien) <= 10: raise RuntimeError("Karussell braucht 2–10 Medien")
        kinder = []
        for m in medien:
            ist_video = m.lower().split("?")[0].endswith((".mp4", ".mov"))
            k = call("POST", f"{USER}/media", {("video_url" if ist_video else "image_url"): m, "is_carousel_item": "true", **({"media_type": "VIDEO"} if ist_video else {})})["id"]
            warten(k); kinder.append(k)
        c = call("POST", f"{USER}/media", {"media_type": "CAROUSEL", "children": ",".join(kinder), "caption": caption})["id"]
    else:
        raise RuntimeError(f"unbekannter Typ {typ}")
    warten(c)
    pub = call("POST", f"{USER}/media_publish", {"creation_id": c})
    mid = pub["id"]
    # Prüfen, ob der Beitrag wirklich live ist
    info = call("GET", mid, {"fields": "id,permalink,timestamp,media_type,caption"})
    return {"veroeffentlicht": True, "media_id": mid, "permalink": info.get("permalink"), "zeit": info.get("timestamp"),
            "caption_unveraendert": info.get("caption", "") == caption}

def insights(anzahl):
    media = call("GET", f"{USER}/media", {"fields": "id,caption,media_type,timestamp,permalink,like_count,comments_count", "limit": str(anzahl)}).get("data", [])
    for m in media:
        werte = {}
        for metrik in ("reach", "views", "saved", "shares", "total_interactions"):
            try:
                d = call("GET", f"{m['id']}/insights", {"metric": metrik}, versuche=1).get("data", [])
                if d: werte[metrik] = d[0].get("values", [{}])[0].get("value")
            except RuntimeError:
                pass  # Metrik für diesen Medientyp nicht verfügbar
        m["insights"] = werte
        m["caption"] = (m.get("caption") or "")[:120]
    return {"anzahl": len(media), "beitraege": media, "hinweis": "Werte direkt aus der Graph API; fehlende Metriken gibt die API für diesen Medientyp nicht her."}

def status():
    feld = "id,username,followers_count,media_count" if API == "facebook" else "user_id,username,followers_count,media_count"
    return {"konto": call("GET", USER or "me", {"fields": feld}), "api": API, "version": VERSION}

def token_verlaengern():
    if API == "instagram":
        d = call("GET", "refresh_access_token", {"grant_type": "ig_refresh_token"})
    else:
        app, secret = os.environ.get("IG_APP_ID"), os.environ.get("IG_APP_SECRET")
        if not app or not secret: raise RuntimeError("Für Facebook-Login-Tokens braucht die Verlängerung App-ID und App-Secret")
        d = call("GET", "oauth/access_token", {"grant_type": "fb_exchange_token", "client_id": app, "client_secret": secret, "fb_exchange_token": TOKEN})
    return {"neuer_token": d.get("access_token"), "laeuft_ab_in_s": d.get("expires_in")}

try:
    if not TOKEN: raise RuntimeError("Kein Token gespeichert – zuerst ig_zugang_speichern")
    a = sys.argv[1:]
    if a[0] == "status": out(status())
    elif a[0] == "posten": out(posten(json.loads(a[1])))
    elif a[0] == "insights": out(insights(int(a[1]) if len(a) > 1 else 12))
    elif a[0] == "token_verlaengern": out(token_verlaengern())
    else: out({"fehler": f"unbekannt: {a[0]}"})
except Exception as ex:
    out({"fehler": str(ex).replace(TOKEN, "***") if TOKEN else str(ex)})
