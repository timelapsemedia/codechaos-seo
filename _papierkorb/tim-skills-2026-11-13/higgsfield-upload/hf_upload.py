#!/usr/bin/env python3
"""Lokale Dateien zu Higgsfield hochladen, ohne die signierten Upload-URLs abzutippen.

Liest die letzte media_upload-Antwort aus dem Transkript der laufenden Session
(~/.claude/projects/*/<CLAUDE_CODE_SESSION_ID>.jsonl), ordnet die lokalen Dateien
in derselben Reihenfolge wie im media_upload-Aufruf zu und lädt sie per curl -X PUT
hoch (Python-urllib bekommt von der signierten URL 403). Gibt nie eine URL aus,
nur Statuscodes und die media_ids für media_confirm.

Nur Standardbibliothek + curl. Netz: ausschließlich die PUTs an die signierten URLs.
"""
import argparse
import datetime as dt
import glob
import json
import mimetypes
import os
import re
import subprocess
import sys

GRENZE_MB = 500  # 533 MB lehnte Higgsfield mit HTTP 413 ab, 317 MB gingen (Zollhaus 20.10.2026)


def kandidaten(transkript):
    if transkript:
        return [transkript]
    basis = os.path.join(os.path.expanduser("~"), ".claude", "projects")
    sid = os.environ.get("CLAUDE_CODE_SESSION_ID", "")
    pfade = []
    if sid:
        pfade += glob.glob(os.path.join(basis, "*", sid + ".jsonl"))
        pfade += glob.glob(os.path.join(basis, "*", sid, "subagents", "*.jsonl"))
    if not pfade:  # Fallback: zuletzt geänderte Transkripte der letzten 2 Stunden
        grenze = dt.datetime.now().timestamp() - 7200
        pfade = [p for p in glob.glob(os.path.join(basis, "*", "*.jsonl"))
                 if os.path.getmtime(p) > grenze]
    return pfade


def text_aus(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(b.get("text", "") for b in content if isinstance(b, dict))
    return ""


def letzte_antwort(pfad):
    """(zeitstempel, dateinamen_aus_aufruf, uploads) der letzten media_upload-Antwort oder None."""
    aufrufe, treffer = {}, None
    with open(pfad, encoding="utf-8") as f:
        for zeile in f:
            if "media_upload" not in zeile and "upload_url" not in zeile:
                continue
            try:
                r = json.loads(zeile)
            except ValueError:
                continue
            inhalt = (r.get("message") or {}).get("content")
            if not isinstance(inhalt, list):
                continue
            for b in inhalt:
                if b.get("type") == "tool_use" and re.search(r"(^|__)media_upload$", b.get("name", "")):
                    namen = [d.get("filename", "") for d in (b.get("input") or {}).get("files", [])]
                    aufrufe[b["id"]] = namen
                elif b.get("type") == "tool_result" and b.get("tool_use_id") in aufrufe:
                    t = text_aus(b.get("content"))
                    try:
                        uploads = json.loads(t).get("uploads")
                    except (ValueError, AttributeError):
                        uploads = None
                    if uploads:
                        treffer = (r.get("timestamp", ""), aufrufe[b["tool_use_id"]], uploads)
    return treffer


def finde(transkript):
    beste = None
    for p in kandidaten(transkript):
        t = letzte_antwort(p)
        if t and (beste is None or t[0] > beste[0]):
            beste = t
    return beste


def put(datei, url, ctype):
    befehl = ["curl", "-s", "-o", os.devnull, "-w", "%{http_code}", "-X", "PUT",
              "-H", "Content-Type: " + ctype, "--data-binary", "@" + datei, url]
    code = ""
    for _ in range(2):  # einmal wiederholen
        code = subprocess.run(befehl, capture_output=True, text=True).stdout.strip()
        if code == "200":
            break
    return code


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dateien", nargs="+", help="lokale Dateien, gleiche Reihenfolge wie im media_upload-Aufruf")
    ap.add_argument("--transkript", help="Pfad zum Session-Transkript (.jsonl), sonst automatisch")
    ap.add_argument("--probe", action="store_true", help="nur Zuordnung zeigen, nichts hochladen")
    ap.add_argument("--trotzdem", action="store_true", help="Warnungen (Typ, Größe) übergehen")
    a = ap.parse_args()

    t = finde(a.transkript)
    if not t:
        sys.exit("FEHLER: keine media_upload-Antwort im Transkript gefunden. Erst media_upload aufrufen "
                 "(oder --transkript angeben).")
    zeit, namen, uploads = t
    if len(a.dateien) != len(uploads):
        sys.exit(f"FEHLER: {len(a.dateien)} Dateien, aber {len(uploads)} Upload-Plätze "
                 f"(angefragt: {', '.join(namen) or '?'}).")
    if zeit:
        ab = dt.datetime.fromisoformat(zeit.replace("Z", "+00:00"))
        rest = min(u.get("expires_in_seconds", 86400) for u in uploads) - (
            dt.datetime.now(dt.timezone.utc) - ab).total_seconds()
        if rest <= 0:
            sys.exit("FEHLER: Upload-URLs sind abgelaufen – media_upload neu aufrufen.")

    probleme = []
    for i, (datei, u) in enumerate(zip(a.dateien, uploads)):
        if not os.path.isfile(datei):
            sys.exit(f"FEHLER: Datei fehlt: {datei}")
        ctype = u.get("content_type", "")
        geraten = mimetypes.guess_type(datei)[0] or "?"
        mb = os.path.getsize(datei) / 1e6
        angefragt = namen[i] if i < len(namen) else "?"
        print(f"{i + 1}. {datei} ({mb:.1f} MB) -> Platz „{angefragt}“ [{ctype}]")
        if geraten != ctype:
            probleme.append(f"{datei}: Dateityp {geraten}, Platz erwartet {ctype}")
        if mb > GRENZE_MB:
            probleme.append(f"{datei}: {mb:.0f} MB > {GRENZE_MB} MB (Higgsfield lehnte 533 MB mit 413 ab)")
    if probleme:
        print("WARNUNG:\n  " + "\n  ".join(probleme))
        if not a.trotzdem:
            sys.exit("Abbruch. Reihenfolge/Datei prüfen oder mit --trotzdem bewusst übergehen.")
    if a.probe:
        print("Probe: nichts hochgeladen.")
        return

    fehler, ids = 0, {}
    for datei, u in zip(a.dateien, uploads):
        code = put(datei, u["upload_url"], u.get("content_type", "application/octet-stream"))
        ok = code == "200"
        fehler += not ok
        print(f"{os.path.basename(datei)} -> {code or 'kein HTTP-Code'}{'' if ok else '  FEHLGESCHLAGEN'}")
        if ok:
            art = u.get("content_type", "").split("/")[0]
            ids.setdefault(art, []).append(u["media_id"])
    for art, liste in ids.items():
        print("media_confirm: " + json.dumps({"type": art, "media_ids": liste}))
    sys.exit(1 if fehler else 0)


if __name__ == "__main__":
    main()
