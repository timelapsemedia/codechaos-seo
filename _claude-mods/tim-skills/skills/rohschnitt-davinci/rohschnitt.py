#!/usr/bin/env python3
"""rohschnitt.py - Rohschnitt aus einem Transkript als EDL für DaVinci Resolve (und Premiere).

    python3 rohschnitt.py transkript.srt --clip interview.mp4
    python3 rohschnitt.py transkript.json --clip A001.mov --fps 25 --pause 0.6 --rand 0.15 -o rohschnitt.edl
    python3 rohschnitt.py transkript.srt --clip x.mp4 --nur-liste      # nur anzeigen, keine EDL

Erkennt (deutsch und englisch):
  PAUSE    Stille zwischen gesprochenen Abschnitten länger als --pause Sekunden
  FUELL    Abschnitte, die nur aus Füllwörtern bestehen ("äh", "ähm", "also", "halt", "um", "uh" …)
  NEU      neu angesetzter Satz – der ERSTE Versuch fliegt raus, der zweite bleibt

Schreibt eine CMX3600-EDL mit den Teilen, die BLEIBEN, hintereinander auf einer Spur.
DaVinci: Datei > Importieren > Timeline > „AAF, EDL, XML importieren…“, Clip vorher im Media Pool.
Ändert keine Mediendateien. Nur Python-Standardbibliothek, kein Netz.
"""
import argparse
import json
import re
import sys

FUELL = re.compile(
    r"^[\s,.!?…-]*((äh+m*|ähm+|öh+m*|hm+|mh+|em+|eh+|also|halt|quasi|sozusagen|irgendwie|genau|ja|ne|naja|"
    r"okay|ok|so|gut|na ja|wie gesagt|keine ahnung|weißt du|ich mein|"
    r"um+|uh+|er+|ah+|like|anyway|basically|actually|you know|i mean|right|yeah)[\s,.!?…-]*)+$",
    re.I)


def parse_ts(s):
    s = s.strip().replace(",", ".")
    p = s.split(":")
    return int(p[0]) * 3600 + int(p[1]) * 60 + float(p[2]) if len(p) == 3 else int(p[0]) * 60 + float(p[1])


def lade(pfad):
    roh = open(pfad, encoding="utf-8", errors="replace").read()
    if pfad.lower().endswith(".json"):
        d = json.loads(roh)
        segs = d.get("segments", d if isinstance(d, list) else [])
        return [(float(s["start"]), float(s["end"]), (s.get("text") or "").strip()) for s in segs]
    cues, cur = [], None
    for zeile in roh.splitlines():
        m = re.match(r"\s*(\d[\d:.,]+)\s*-->\s*(\d[\d:.,]+)", zeile)
        if m:
            cur = [parse_ts(m.group(1)), parse_ts(m.group(2)), []]
            cues.append(cur)
        elif cur is not None and zeile.strip() and not zeile.strip().isdigit() and not zeile.startswith("WEBVTT"):
            cur[2].append(zeile.strip())
    return [(a, b, " ".join(t)) for a, b, t in cues if t]


def woerter(t):
    return re.sub(r"[^\wäöüß ]", "", t.lower()).split()


def finde_schnitte(cues, pause, rand):
    schnitte = []
    for i, (s, e, t) in enumerate(cues):
        if FUELL.match(t):
            schnitte.append(("FUELL", s, e, t.strip()[:40]))
        if i:
            luecke = s - cues[i - 1][1]
            if luecke > pause:
                schnitte.append(("PAUSE", cues[i - 1][1] + rand, s - rand, f"{luecke:.2f}s Stille"))
        if t.strip() and not FUELL.match(t):
            j = i - 1
            while j >= 0 and (FUELL.match(cues[j][2]) or not cues[j][2].strip()):
                j -= 1
            if j >= 0:
                a, b = woerter(cues[j][2])[:4], woerter(t)[:4]
                if len(a) >= 3 and a == b:
                    schnitte.append(("NEU", cues[j][0], cues[j][1], f'neu angesetzt: "{" ".join(a)}"'))
    return sorted([c for c in schnitte if c[2] - c[1] > 0.05], key=lambda c: c[1])


def behalten(dauer, schnitte, min_teil):
    teile, pos = [], 0.0
    for _, s, e, _ in schnitte:
        if s > pos:
            teile.append((pos, s))
        pos = max(pos, e)
    if dauer > pos:
        teile.append((pos, dauer))
    return [(a, b) for a, b in teile if b - a >= min_teil]


def tc(sek, fps):
    f = int(round(sek * fps))
    return f"{f // (3600 * fps):02d}:{f // (60 * fps) % 60:02d}:{f // fps % 60:02d}:{f % fps:02d}"


def edl(teile, clip, fps, titel, quell_start, rec_start):
    zeilen = [f"TITLE: {titel}", "FCM: NON-DROP FRAME", ""]
    rec = rec_start
    for n, (a, b) in enumerate(teile, 1):
        fa, fb = int(round(a * fps)), int(round(b * fps))
        if fb <= fa:
            continue
        laenge = (fb - fa) / fps
        zeilen.append(f"{n:03d}  AX       AA/V  C        {tc(quell_start + fa / fps, fps)} "
                      f"{tc(quell_start + fb / fps, fps)} {tc(rec, fps)} {tc(rec + laenge, fps)}")
        zeilen.append(f"* FROM CLIP NAME: {clip}")
        zeilen.append("")
        rec += laenge
    return "\n".join(zeilen) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Rohschnitt-EDL aus Transkript (DaVinci Resolve)")
    ap.add_argument("transkript")
    ap.add_argument("--clip", required=True, help="Dateiname des Quellclips, genau wie im Media Pool")
    ap.add_argument("--fps", type=int, default=25)
    ap.add_argument("--pause", type=float, default=0.6, help="Stille ab dieser Länge kürzen (s)")
    ap.add_argument("--rand", type=float, default=0.15, help="so viel Stille an jeder Schnittkante stehen lassen (s)")
    ap.add_argument("--min-teil", type=float, default=0.4, help="kürzere Reststücke weglassen (s)")
    ap.add_argument("--dauer", type=float, help="Clipdauer in s (sonst Ende des letzten Abschnitts)")
    ap.add_argument("--quell-tc", default="00:00:00:00", help="Start-Timecode des Quellclips")
    ap.add_argument("-o", "--ausgabe", help="EDL-Datei (Standard: <transkript>.rohschnitt.edl)")
    ap.add_argument("--nur-liste", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    cues = lade(a.transkript)
    if not cues:
        sys.exit("Keine Abschnitte gefunden – ist das eine .srt, .vtt oder Whisper-.json?")
    dauer = a.dauer or cues[-1][1]
    schnitte = finde_schnitte(cues, a.pause, a.rand)
    teile = behalten(dauer, schnitte, a.min_teil)
    raus = dauer - sum(b - x for x, b in teile)
    h, m, s, f = (int(x) for x in a.quell_tc.split(":"))
    quell_start = h * 3600 + m * 60 + s + f / a.fps

    if a.json:
        print(json.dumps({"clip": a.clip, "dauer": dauer, "schnitte": [
            {"art": k, "start": round(s, 3), "ende": round(e, 3), "grund": g} for k, s, e, g in schnitte],
            "behalten": [[round(x, 3), round(b, 3)] for x, b in teile], "entfernt_s": round(raus, 2)},
            ensure_ascii=False, indent=1))
    else:
        print(f"\n  {a.transkript}: {dauer:.1f}s, {len(cues)} Abschnitte, Pause ab {a.pause}s\n")
        for k, s, e, g in schnitte:
            print(f"    {k:<6} {s:8.2f} → {e:8.2f}  {e - s:5.2f}s  {g}")
        print(f"\n  {len(schnitte)} Schnitte, {raus:.1f}s raus → {dauer - raus:.1f}s "
              f"({raus / dauer * 100:.0f} % kürzer), {len(teile)} Teile in der Timeline\n")
    if a.nur_liste:
        return
    ziel = a.ausgabe or re.sub(r"\.[^.]+$", "", a.transkript) + ".rohschnitt.edl"
    with open(ziel, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(edl(teile, a.clip, a.fps, "Rohschnitt " + a.clip, quell_start, 3600.0))
    if not a.json:
        print(f"  EDL geschrieben: {ziel}\n  DaVinci: Datei > Importieren > Timeline > AAF, EDL, XML … "
              f"(Clip „{a.clip}“ muss im Media Pool liegen)\n")


if __name__ == "__main__":
    main()
