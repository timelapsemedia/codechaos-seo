#!/usr/bin/env python3
"""Google Search Console: Sitemap einreichen, Indexierungsstatus aller Sitemap-URLs prüfen,
Suchanfragen der letzten 90 Tage ausgeben.

Service-Account-Schlüssel (JSON) NIE ins Repo legen. Pfad per Umgebungsvariable:
  GSC_KEY_FILE=/pfad/zum/key.json python3 _build/gsc_report.py
Der Service-Account muss in der Search Console als Inhaber/Nutzer der Property
sc-domain:codechaos-official.de eingetragen sein (ist er seit 10/2026).
"""
import base64, datetime, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "sc-domain:codechaos-official.de"
SITEMAP = "https://codechaos-official.de/sitemap.xml"


def b64(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=")


def token(key_file):
    d = json.load(open(key_file)); now = int(time.time())
    h = b64(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    c = b64(json.dumps({"iss": d["client_email"], "scope": "https://www.googleapis.com/auth/webmasters",
                        "aud": d["token_uri"], "iat": now, "exp": now + 3600}).encode())
    k = serialization.load_pem_private_key(d["private_key"].encode(), password=None)
    sig = b64(k.sign(h + b"." + c, padding.PKCS1v15(), hashes.SHA256()))
    data = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                                   "assertion": (h + b"." + c + b"." + sig).decode()}).encode()
    return json.load(urllib.request.urlopen(urllib.request.Request(d["token_uri"], data=data), timeout=30))["access_token"]


def main():
    key_file = os.environ.get("GSC_KEY_FILE") or sys.exit("GSC_KEY_FILE setzen (Pfad zum Service-Account-JSON).")
    tok = token(key_file)

    def api(method, url, body=None):
        req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None,
                                     headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                t = r.read().decode(); return r.status, (json.loads(t) if t.strip() else {})
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode()[:300]

    s = urllib.parse.quote(SITE, safe="")
    print("Sitemap einreichen:", api("PUT", f"https://www.googleapis.com/webmasters/v3/sites/{s}/sitemaps/{urllib.parse.quote(SITEMAP, safe='')}")[0])
    urls = re.findall(r"<loc>(.*?)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read())
    print("\nIndexierungsstatus:")
    for u in urls:
        st, b = api("POST", "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
                    {"inspectionUrl": u, "siteUrl": SITE, "languageCode": "de-DE"})
        r = b.get("inspectionResult", {}).get("indexStatusResult", {}) if st == 200 else {}
        print(f"  {u:55} {r.get('coverageState', st)}  {r.get('lastCrawlTime', '')[:10]}")
    end = datetime.date.today() - datetime.timedelta(days=2); start = end - datetime.timedelta(days=90)
    st, b = api("POST", f"https://www.googleapis.com/webmasters/v3/sites/{s}/searchAnalytics/query",
                {"startDate": str(start), "endDate": str(end), "dimensions": ["query"], "rowLimit": 1000})
    rows = sorted(b.get("rows", []), key=lambda r: -r["impressions"]) if st == 200 else []
    print(f"\nSuchanfragen {start} bis {end} (nach Impressionen):")
    for r in rows[:40]:
        print(f"  {r['keys'][0][:45]:45} Impr {r['impressions']:5}  Klicks {r['clicks']:4}  Pos {r['position']:.1f}")


if __name__ == "__main__":
    main()
