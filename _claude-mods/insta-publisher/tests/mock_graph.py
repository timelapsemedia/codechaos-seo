#!/usr/bin/env python3
"""Kleiner Fake der Graph API für einen lokalen Funktionstest (kein echtes Instagram)."""
import json, sys, urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
state = {"n": 0, "posts": {}}
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, d, code=200):
        b = json.dumps(d, ensure_ascii=False).encode("utf-8"); self.send_response(code); self.send_header("Content-Type", "application/json; charset=utf-8"); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        u = urllib.parse.urlparse(self.path); q = dict(urllib.parse.parse_qsl(u.query)); p = u.path.strip("/").split("/")
        if q.get("access_token") != "geheim": return self.send({"error": {"message": "Invalid OAuth access token", "code": 190}}, 400)
        if p[-1] == "insights": return self.send({"data": [{"values": [{"value": 42}]}]} if q["metric"] in ("reach", "saved") else {"error": {"message": "nope", "code": 100}}, 200 if q["metric"] in ("reach", "saved") else 400)
        if p[-1] == "media": return self.send({"data": [{"id": k, "caption": v, "media_type": "IMAGE"} for k, v in state["posts"].items()]})
        if p[-1].startswith("c"): return self.send({"status_code": "FINISHED"})
        if p[-1].startswith("m"): return self.send({"id": p[-1], "permalink": f"https://instagram.example/p/{p[-1]}", "timestamp": "2026-10-07T10:00:00+0000", "caption": state["posts"][p[-1]]})
        return self.send({"id": "17841", "username": "test_konto", "followers_count": 10, "media_count": len(state["posts"])})
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0)); q = dict(urllib.parse.parse_qsl(self.rfile.read(n).decode("utf-8"))); p = urllib.parse.urlparse(self.path).path.strip("/").split("/")
        if q.get("access_token") != "geheim": return self.send({"error": {"message": "Invalid OAuth access token", "code": 190}}, 400)
        state["n"] += 1
        if p[-1] == "media": state["c" + str(state["n"])] = q.get("caption", ""); return self.send({"id": "c" + str(state["n"])})
        if p[-1] == "media_publish": mid = "m" + str(state["n"]); state["posts"][mid] = state.get(q["creation_id"], ""); return self.send({"id": mid})
HTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
