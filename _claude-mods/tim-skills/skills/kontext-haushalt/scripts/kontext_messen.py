#!/usr/bin/env python3
"""Kontext-Haushalt messen: Was kostet jede Anfrage, bevor die Arbeit beginnt?

Misst ohne Netz und ohne Tokens, nur aus lokalen Dateien:
  1. Fester Text je Session: CLAUDE.md samt @-Importen, MEMORY.md, ~/.claude/rules.
  2. Startkontext je Session: Kontext der ERSTEN Anfrage (System-Prompt, Werkzeuge,
     MCP-Anleitungen, Skill-Liste, CLAUDE.md, Auftrag), aus den Transkripten.
  3. Mittlerer und größter Kontext je Anfrage und je Session.
  4. Welche MCP-Server im Zeitraum wirklich aufgerufen wurden.
  5. Größe der Routine-Prompts (scheduled-tasks/*/SKILL.md).

Aufruf:
  python kontext_messen.py                     Bericht über die letzten 24 h
  python kontext_messen.py --stunden 168       letzte 7 Tage
  python kontext_messen.py --json              maschinenlesbar
  python kontext_messen.py --gate              Exit 1, wenn eine Grenze reißt
  python kontext_messen.py --projekt C--       MEMORY.md dieses Projektordners (Standard C--)

Grenzen (Quelle: code.claude.com/docs/en/memory, gelesen 24.11.2026):
  CLAUDE.md höchstens 200 Zeilen je Datei; MEMORY.md lädt nur die ersten 200 Zeilen / 25 KB.
Token-Schätzung für Dateien: Zeichen / 3,5 (deutscher Text). Transkript-Werte sind echte Zählwerte.
Nur Python-Standardbibliothek. Liest nur, schreibt nichts.
"""
import argparse
import glob
import io
import json
import os
import re
import statistics
import sys
import time

HOME = os.path.expanduser("~").replace("\\", "/")
CLAUDE = HOME + "/.claude"
MAX_CLAUDE_ZEILEN = 200
MAX_MEMORY_ZEILEN = 200
MAX_MEMORY_BYTES = 25 * 1024
WARN_SESSION_KONTEXT = 400_000
ZEICHEN_JE_TOKEN = 3.5


def lesen(pfad):
    try:
        return io.open(pfad, encoding="utf-8", errors="replace").read()
    except OSError:
        return None


def tokens(text):
    return int(len(text) / ZEICHEN_JE_TOKEN)


def importe(text, basis, tiefe=0, gesehen=None):
    """@-Importe wie Claude Code auflösen (höchstens vier Sprünge). Importe sparen keinen Kontext."""
    gesehen = gesehen if gesehen is not None else set()
    out = []
    if tiefe >= 4:
        return out
    for m in re.finditer(r"(?m)^@(\S+)\s*$", text):
        p = m.group(1).replace("\\", "/")
        if p.startswith("~"):
            p = HOME + p[1:]
        elif not re.match(r"^([A-Za-z]:)?/", p):
            p = os.path.join(basis, p).replace("\\", "/")
        if p in gesehen:
            continue
        gesehen.add(p)
        t = lesen(p)
        if t is None:
            out.append({"datei": p, "fehlt": True, "zeichen": 0, "zeilen": 0, "tokens": 0})
            continue
        out.append({"datei": p, "zeichen": len(t), "zeilen": len(t.splitlines()), "tokens": tokens(t)})
        out += importe(t, os.path.dirname(p), tiefe + 1, gesehen)
    return out


def feste_dateien(projekt):
    res, befunde = [], []
    cm = CLAUDE + "/CLAUDE.md"
    t = lesen(cm)
    if t is not None:
        z = len(t.splitlines())
        res.append({"datei": cm, "zeichen": len(t), "zeilen": z, "tokens": tokens(t)})
        if z > MAX_CLAUDE_ZEILEN:
            befunde.append(f"CLAUDE.md hat {z} Zeilen, Grenze {MAX_CLAUDE_ZEILEN}")
        res += importe(t, os.path.dirname(cm))
        abschnitte = []
        for teil in re.split(r"(?m)^(?=## )", t):
            if teil.strip():
                abschnitte.append({"titel": teil.splitlines()[0][:70], "zeilen": len(teil.splitlines()),
                                   "tokens": tokens(teil), "anteil": round(100 * len(teil) / max(len(t), 1), 1)})
        abschnitte.sort(key=lambda a: -a["tokens"])
    else:
        abschnitte = []
    mem = f"{CLAUDE}/projects/{projekt}/memory/MEMORY.md"
    t = lesen(mem)
    if t is not None:
        z, b = len(t.splitlines()), len(t.encode("utf-8"))
        res.append({"datei": mem, "zeichen": len(t), "zeilen": z, "tokens": tokens(t)})
        if z > MAX_MEMORY_ZEILEN or b > MAX_MEMORY_BYTES:
            befunde.append(f"MEMORY.md {z} Zeilen / {b} Bytes: nur die ersten {MAX_MEMORY_ZEILEN} Zeilen "
                           f"bzw. {MAX_MEMORY_BYTES} Bytes werden geladen, der Rest fehlt jeder Session")
    for p in sorted(glob.glob(CLAUDE + "/rules/**/*.md", recursive=True)):
        t = lesen(p) or ""
        if not re.search(r"(?m)^paths:", t.split("---")[1] if t.startswith("---") and t.count("---") >= 2 else ""):
            res.append({"datei": p.replace("\\", "/"), "zeichen": len(t), "zeilen": len(t.splitlines()), "tokens": tokens(t)})
    return res, abschnitte, befunde


def routinen(top=10):
    out = []
    for p in glob.glob(CLAUDE + "/scheduled-tasks/*/SKILL.md"):
        t = lesen(p) or ""
        out.append({"routine": os.path.basename(os.path.dirname(p)), "tokens": tokens(t), "zeilen": len(t.splitlines())})
    out.sort(key=lambda r: -r["tokens"])
    return out[:top], len(out)


def transkripte(stunden):
    """Je Session: Kontext jeder Anfrage = input + cache_read + cache_creation (echte Zählwerte)."""
    grenze = time.time() - stunden * 3600
    sessions, mcp = {}, {}
    for f in glob.glob(CLAUDE + "/projects/*/*.jsonl"):
        try:
            if os.path.getmtime(f) < grenze:
                continue
        except OSError:
            continue
        sid = os.path.basename(f)[:-6]
        anfragen = {}  # message.id -> (zeit, kontext, modell); Streaming schreibt dieselbe id mehrfach
        try:
            fh = io.open(f, encoding="utf-8", errors="replace")
        except OSError:
            continue
        with fh:
            for zeile in fh:
                if '"usage"' not in zeile and '"tool_use"' not in zeile:
                    continue
                try:
                    o = json.loads(zeile)
                except ValueError:
                    continue
                m = o.get("message")
                if o.get("type") != "assistant" or not isinstance(m, dict):
                    continue
                ts = o.get("timestamp") or ""
                try:
                    sek = time.mktime(time.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S")) - time.timezone
                except ValueError:
                    sek = 0
                u = m.get("usage") or {}
                ktx = sum(int(u.get(k) or 0) for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
                mid = m.get("id") or ts
                neu = mid not in anfragen
                if ktx:
                    anfragen[mid] = (sek, ktx, m.get("model") or "?")
                if sek >= grenze and neu:
                    for c in m.get("content") or []:
                        if isinstance(c, dict) and c.get("type") == "tool_use":
                            n = c.get("name") or ""
                            if n.startswith("mcp__"):
                                srv = n.split("__")[1]
                                mcp[srv] = mcp.get(srv, 0) + 1
        if not anfragen:
            continue
        reihe = sorted(anfragen.values())
        im_fenster = [k for s, k, _ in reihe if s >= grenze]
        if not im_fenster:
            continue
        sessions[sid] = {"session": sid, "projekt": os.path.basename(os.path.dirname(f)), "modell": reihe[-1][2],
                         "anfragen": len(im_fenster), "start": reihe[0][1], "start_im_fenster": reihe[0][0] >= grenze,
                         "mittel": int(statistics.mean(im_fenster)), "max": max(im_fenster), "zuletzt": reihe[-1][1],
                         "summe": sum(im_fenster)}
    return sessions, mcp


def bericht(stunden, projekt):
    dateien, abschnitte, befunde = feste_dateien(projekt)
    rout, rout_n = routinen()
    sess, mcp = transkripte(stunden)
    alle = list(sess.values())
    anfragen = sum(s["anfragen"] for s in alle)
    summe = sum(s["summe"] for s in alle)
    starts = [s["start"] for s in alle if s["start_im_fenster"]]
    fest = sum(d["tokens"] for d in dateien)
    start_median = int(statistics.median(starts)) if starts else None
    kennzahlen = {
        "zeitraum_stunden": stunden,
        "sessions": len(alle),
        "anfragen": anfragen,
        "kontext_tokens_summe": summe,
        "kontext_je_anfrage_mittel": int(summe / anfragen) if anfragen else None,
        "startkontext_median": start_median,
        "startkontext_sessions": len(starts),
        "fester_text_tokens": fest,
        "anteil_startkontext_prozent": round(100 * start_median * anfragen / summe, 1) if start_median and summe else None,
        "anteil_fester_text_prozent": round(100 * fest * anfragen / summe, 1) if summe else None,
        "sessions_ueber_400k": sum(1 for s in alle if s["zuletzt"] > WARN_SESSION_KONTEXT),
    }
    for s in alle:
        if s["zuletzt"] > WARN_SESSION_KONTEXT:
            befunde.append(f"Session {s['session'][:8]} steht bei {s['zuletzt'] // 1000}k Kontext: neue Arbeit in frische Session")
    alle.sort(key=lambda s: -s["summe"])
    return {"kennzahlen": kennzahlen, "dateien": dateien, "claude_md_abschnitte": abschnitte[:8],
            "routinen_top": rout, "routinen_anzahl": rout_n, "sessions_top": alle[:10],
            "mcp_aufrufe": dict(sorted(mcp.items(), key=lambda kv: -kv[1])), "befunde": befunde}


def drucken(b):
    k = b["kennzahlen"]
    p = print
    p(f"# Kontext-Haushalt, letzte {k['zeitraum_stunden']} h\n")
    p(f"- Sessions {k['sessions']}, Anfragen {k['anfragen']}, gelesener Kontext {k['kontext_tokens_summe'] / 1e6:.0f} Mio. Tokens")
    if k["kontext_je_anfrage_mittel"]:
        p(f"- Kontext je Anfrage im Mittel: {k['kontext_je_anfrage_mittel'] // 1000}k Tokens")
    if k["startkontext_median"]:
        p(f"- Startkontext (erste Anfrage, Median aus {k['startkontext_sessions']} neuen Sessions): "
          f"{k['startkontext_median'] // 1000}k Tokens = {k['anteil_startkontext_prozent']} % des gelesenen Kontexts")
    p(f"- Fester Text (CLAUDE.md, Importe, MEMORY.md): {k['fester_text_tokens'] / 1000:.1f}k Tokens "
      f"= {k['anteil_fester_text_prozent']} % des gelesenen Kontexts")
    p(f"- Sessions über 400k Kontext: {k['sessions_ueber_400k']}\n")
    p("## Feste Dateien\n| Datei | Zeilen | Tokens |\n|---|---|---|")
    for d in b["dateien"]:
        p(f"| {d['datei']} | {d['zeilen']} | {d['tokens']}{' FEHLT' if d.get('fehlt') else ''} |")
    p("\n## CLAUDE.md nach Abschnitt\n| Abschnitt | Zeilen | Tokens | Anteil |\n|---|---|---|---|")
    for a in b["claude_md_abschnitte"]:
        p(f"| {a['titel']} | {a['zeilen']} | {a['tokens']} | {a['anteil']} % |")
    p("\n## Sessions mit dem meisten gelesenen Kontext\n| Session | Modell | Anfragen | Start | Mittel | Zuletzt |\n|---|---|---|---|---|---|")
    for s in b["sessions_top"]:
        p(f"| {s['session'][:8]} ({s['projekt'][:18]}) | {s['modell'].replace('claude-', '')} | {s['anfragen']} | "
          f"{s['start'] // 1000}k | {s['mittel'] // 1000}k | {s['zuletzt'] // 1000}k |")
    p(f"\n## Routine-Prompts (größte von {b['routinen_anzahl']})\n| Routine | Zeilen | Tokens |\n|---|---|---|")
    for r in b["routinen_top"]:
        p(f"| {r['routine']} | {r['zeilen']} | {r['tokens']} |")
    p("\n## MCP-Server mit Aufrufen im Zeitraum")
    p(", ".join(f"{n} {c}" for n, c in b["mcp_aufrufe"].items()) or "keine")
    p("\n## Befunde")
    for f in b["befunde"] or ["keine"]:
        p(f"- {f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--stunden", type=float, default=24)
    ap.add_argument("--projekt", default="C--")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--gate", action="store_true")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    b = bericht(a.stunden, a.projekt)
    if a.json:
        print(json.dumps(b, ensure_ascii=False, indent=1))
    else:
        drucken(b)
    sys.exit(1 if a.gate and b["befunde"] else 0)
