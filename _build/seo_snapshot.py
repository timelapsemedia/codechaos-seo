#!/usr/bin/env python3
"""Wöchentlicher SEO-Messstand: Google Search Console + Bing + IndexNow.

Hängt einen Datensatz an _docs/seo-history.jsonl an und gibt einen Vergleich zum
letzten Stand aus. Läuft lokal, in der Cloud-Session und in der Routine.

Zugangsdaten (nie ins Repo):
  Google:  GSC_KEY_FILE=/pfad/key.json   oder   GSC_KEY_JSON='{...kompletter JSON-Inhalt...}'
  Bing:    BING_API_KEY=... oder BING_API_KEY_FILE=/pfad/key.txt
Aufruf:   python3 _build/seo_snapshot.py [--no-ping]
"""
import base64, datetime, json, os, re, subprocess, sys, tempfile, time, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, "_docs", "seo-history.jsonl")
SITE_GSC = "sc-domain:codechaos-official.de"
SITE_BING = "https://codechaos-official.de/"
TARGETS = ["psycore", "darkpsy", "dark psy", "hitech psy", "hitech psytrance", "hi-tech psytrance", "psytrance mastering",
           "psycore mastering", "code chaos", "uhrwerk aus blut", "crucible plugin", "psycore bpm", "darkpsy bpm"]


def gsc_key_file():
    if os.environ.get("GSC_KEY_FILE"):
        return os.environ["GSC_KEY_FILE"]
    raw = os.environ.get("GSC_KEY_JSON")
    if not raw and os.environ.get("GSC_SERVICE_ACCOUNT_JSON_B64"):
        raw = base64.b64decode(os.environ["GSC_SERVICE_ACCOUNT_JSON_B64"]).decode()
    if not raw:
        return None
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    f.write(raw); f.close()
    return f.name


def rs256(pem, msg):
    """RS256-Signatur; bevorzugt openssl (kein Python-Paket nötig), sonst cryptography."""
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".pem") as f:
            os.chmod(f.name, 0o600); f.write(pem); f.flush()
            return subprocess.run(["openssl", "dgst", "-sha256", "-sign", f.name], input=msg, capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import padding
        k = serialization.load_pem_private_key(pem.encode(), password=None)
        return k.sign(msg, padding.PKCS1v15(), hashes.SHA256())


def gsc_token(key_file):
    b64 = lambda b: base64.urlsafe_b64encode(b).rstrip(b"=")
    d = json.load(open(key_file)); now = int(time.time())
    h = b64(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    c = b64(json.dumps({"iss": d["client_email"], "scope": "https://www.googleapis.com/auth/webmasters",
                        "aud": d["token_uri"], "iat": now, "exp": now + 3600}).encode())
    sig = b64(rs256(d["private_key"], h + b"." + c))
    data = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                                   "assertion": (h + b"." + c + b"." + sig).decode()}).encode()
    return json.load(urllib.request.urlopen(urllib.request.Request(d["token_uri"], data=data), timeout=30))["access_token"]


def http(method, url, body=None, headers=None):
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            t = r.read().decode(); return r.status, (json.loads(t) if t.strip() else {})
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]


def google(snap, urls):
    kf = gsc_key_file()
    if not kf:
        snap["google"] = "keine Zugangsdaten (GSC_KEY_FILE / GSC_KEY_JSON)"; return
    auth = {"Authorization": "Bearer " + gsc_token(kf)}
    s = urllib.parse.quote(SITE_GSC, safe="")
    http("PUT", f"https://www.googleapis.com/webmasters/v3/sites/{s}/sitemaps/{urllib.parse.quote('https://codechaos-official.de/sitemap.xml', safe='')}", headers=auth)
    idx = {}
    for u in urls:
        st, b = http("POST", "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
                     {"inspectionUrl": u, "siteUrl": SITE_GSC, "languageCode": "de-DE"}, auth)
        idx[u] = b.get("inspectionResult", {}).get("indexStatusResult", {}).get("coverageState", st) if st == 200 else st
    end = datetime.date.today() - datetime.timedelta(days=2); start = end - datetime.timedelta(days=28)
    q = {}
    for dims, key in ((["query"], "queries"), (["page"], "pages")):
        st, b = http("POST", f"https://www.googleapis.com/webmasters/v3/sites/{s}/searchAnalytics/query",
                     {"startDate": str(start), "endDate": str(end), "dimensions": dims, "rowLimit": 1000}, auth)
        q[key] = {r["keys"][0]: {"impr": r["impressions"], "clicks": r["clicks"], "pos": round(r["position"], 1)}
                  for r in (b.get("rows", []) if st == 200 else [])}
    snap["google"] = {"period": [str(start), str(end)], "index": idx, **q}


def bing(snap, urls):
    f = os.environ.get("BING_API_KEY_FILE")
    k = open(f).read().strip() if f else os.environ.get("BING_API_KEY")
    if not k:
        snap["bing"] = "kein BING_API_KEY / BING_API_KEY_FILE"; return
    api = "https://ssl.bing.com/webmaster/api.svc/json/"
    http("POST", f"{api}SubmitFeed?apikey={k}", {"siteUrl": SITE_BING, "feedUrl": SITE_BING + "sitemap.xml"})
    http("POST", f"{api}SubmitUrlBatch?apikey={k}", {"siteUrl": SITE_BING, "urlList": urls})
    st, b = http("GET", f"{api}GetQueryStats?siteUrl={urllib.parse.quote(SITE_BING, safe='')}&apikey={k}")
    agg = {}
    for r in (b.get("d") or [] if st == 200 else []):
        a = agg.setdefault(r["Query"], {"impr": 0, "clicks": 0, "pw": 0.0})
        a["impr"] += r.get("Impressions", 0); a["clicks"] += r.get("Clicks", 0); a["pw"] += r.get("AvgImpressionPosition", 0) * r.get("Impressions", 0)
    snap["bing"] = {q: {"impr": a["impr"], "clicks": a["clicks"], "pos": round(a["pw"] / a["impr"], 1) if a["impr"] else None} for q, a in agg.items()}


def main():
    urls = re.findall(r"<loc>(.*?)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read())
    snap = {"date": str(datetime.date.today())}
    google(snap, urls)
    bing(snap, urls)
    if "--no-ping" not in sys.argv:
        out = subprocess.run([sys.executable, os.path.join(ROOT, "_build", "indexnow_ping.py")], capture_output=True, text=True).stdout
        snap["indexnow"] = [l for l in out.splitlines() if l.strip()]
    prev = None
    if os.path.exists(HIST):
        lines = [l for l in open(HIST, encoding="utf-8") if l.strip()]
        prev = json.loads(lines[-1]) if lines else None
    with open(HIST, "a", encoding="utf-8") as f:
        f.write(json.dumps(snap, ensure_ascii=False) + "\n")

    print(f"SEO-Messstand {snap['date']}" + (f" (Vergleich: {prev['date']})" if prev else ""))
    g = snap.get("google")
    if isinstance(g, dict):
        print("\nGoogle-Index:")
        for u, st in g["index"].items():
            print(f"  {u.replace('https://codechaos-official.de', '') or '/':28} {st}")
        pg = (prev or {}).get("google", {}); pg = pg if isinstance(pg, dict) else {}
        print("\nGoogle-Zielbegriffe (28 Tage, Ø Position | Vorwoche):")
        for t in TARGETS:
            r = g["queries"].get(t); p = pg.get("queries", {}).get(t)
            if r or p:
                print(f"  {t:22} Pos {r['pos'] if r else '–':>5} | {p['pos'] if p else '–':>5}   Impr {r['impr'] if r else 0}  Klicks {r['clicks'] if r else 0}")
        print("\nTop-Suchanfragen nach Impressionen:")
        for q, r in sorted(g["queries"].items(), key=lambda x: -x[1]["impr"])[:15]:
            print(f"  {q[:35]:35} Pos {r['pos']:>5}  Impr {r['impr']}  Klicks {r['clicks']}")
    else:
        print("Google:", g)
    b = snap.get("bing")
    print("\nBing:", f"{len(b)} Suchanfragen" if isinstance(b, dict) else b)
    if isinstance(b, dict):
        for q, r in sorted(b.items(), key=lambda x: -x[1]["impr"])[:10]:
            print(f"  {q[:35]:35} Pos {r['pos']}  Impr {r['impr']}  Klicks {r['clicks']}")
    for l in snap.get("indexnow", []):
        print("IndexNow:", l)


if __name__ == "__main__":
    main()
