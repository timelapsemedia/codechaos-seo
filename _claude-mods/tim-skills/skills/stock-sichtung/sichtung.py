#!/usr/bin/env python3
"""Stock-Sichtung: Standbilder in voller Größe ziehen, Befund mit Prüfsumme festhalten, vor dem Bau prüfen.

  python sichtung.py bilder  <clip> [<clip> …] [--n 5] [--lupe] [--out ORDNER] [--register DATEI]
  python sichtung.py freigabe <clip> (--ok | --sperre) --grund "…" [--register DATEI]
  python sichtung.py pruefe  <clip> [<clip> …] [--register DATEI]

Nur Python-Standardbibliothek plus ffmpeg/ffprobe. Kein Netz, löscht nichts.
Register: standardmäßig stock_sichtung.json im Ordner des (ersten) Clips.
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys

LANGE_SEITE = 1920  # Obergrenze je Standbild; kleiner wird nie skaliert


def sha256(pfad):
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def probe(pfad):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height:format=duration", "-of", "json", pfad],
        capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        raise SystemExit(f"ffprobe scheitert an {pfad}: {out.stderr.strip()}")
    d = json.loads(out.stdout)
    s = (d.get("streams") or [{}])[0]
    dauer = float(d.get("format", {}).get("duration") or 0)
    if not s.get("width"):
        raise SystemExit(f"Keine Videospur in {pfad}")
    return int(s["width"]), int(s["height"]), dauer


def register_pfad(args, clip):
    return os.path.abspath(args.register or os.path.join(os.path.dirname(os.path.abspath(clip)), "stock_sichtung.json"))


def lade(reg):
    if os.path.exists(reg):
        with open(reg, encoding="utf-8") as f:
            return json.load(f)
    return {}


def speichere(reg, daten):
    tmp = f"{reg}.{os.getpid()}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)
    os.replace(tmp, reg)


def schluessel(clip):
    return os.path.abspath(clip).replace("\\", "/")


def bilder(args):
    for clip in args.clips:
        b, h, dauer = probe(clip)
        if dauer <= 0:
            raise SystemExit(f"Dauer unbekannt: {clip}")
        ziel = os.path.abspath(args.out or os.path.join(os.path.dirname(os.path.abspath(clip)), "_sichtung"))
        os.makedirs(ziel, exist_ok=True)
        stamm = os.path.splitext(os.path.basename(clip))[0]
        faktor = min(1.0, LANGE_SEITE / max(b, h))
        skala = [] if faktor >= 1.0 else ["-vf", f"scale=-2:{int(h * faktor) // 2 * 2}" if h >= b else f"scale={int(b * faktor) // 2 * 2}:-2"]
        dateien = []
        for i in range(args.n):
            t = (i + 0.5) / args.n * dauer
            png = os.path.join(ziel, f"{stamm}_{i + 1:02d}_{t:07.2f}s.png")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", clip,
                            "-frames:v", "1", *skala, png], check=True)
            dateien.append(png)
            if args.lupe:
                # 2×2-Ausschnitte in Quellauflösung: feine Rauchfäden, Glut, Kleingedrucktes
                for n, (x, y) in enumerate([(0, 0), (1, 0), (0, 1), (1, 1)], 1):
                    lupe = png[:-4] + f"_lupe{n}.png"
                    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", clip, "-frames:v", "1",
                                    "-vf", f"crop=iw/2:ih/2:{x}*iw/2:{y}*ih/2", lupe], check=True)
                    dateien.append(lupe)
        reg = register_pfad(args, clip)
        daten = lade(reg)
        alt = daten.get(schluessel(clip), {})
        daten[schluessel(clip)] = {
            "sha256": sha256(clip), "quelle_px": f"{b}x{h}", "dauer_s": round(dauer, 2),
            "bilder": dateien, "status": "ungeprueft",
            "verlauf": alt.get("verlauf", []),
        }
        speichere(reg, daten)
        print(f"{clip}: {b}x{h}, {dauer:.1f} s -> {len(dateien)} Bilder (jedes mit Read ansehen):")
        for d in dateien:
            print("  " + d)
    print("Danach je Clip: freigabe --ok oder --sperre mit Grund.")


def freigabe(args):
    clip = args.clips[0]
    reg = register_pfad(args, clip)
    daten = lade(reg)
    e = daten.get(schluessel(clip))
    if not e or not e.get("bilder"):
        raise SystemExit(f"Erst sichten: python sichtung.py bilder \"{clip}\"")
    if e["sha256"] != sha256(clip):
        raise SystemExit("Clip hat sich seit der Sichtung geändert, neu sichten.")
    fehlend = [p for p in e["bilder"] if not os.path.exists(p)]
    if fehlend:
        raise SystemExit(f"Sichtungsbilder fehlen ({len(fehlend)}), neu sichten.")
    if not args.grund.strip():
        raise SystemExit("--grund darf nicht leer sein (was wurde gesehen?).")
    e["status"] = "ok" if args.ok else "gesperrt"
    e["grund"] = args.grund.strip()
    e["datum"] = datetime.datetime.now().isoformat(timespec="seconds")
    e["verlauf"].append({"status": e["status"], "grund": e["grund"], "datum": e["datum"]})
    speichere(reg, daten)
    print(f"{e['status'].upper()}: {clip} ({e['grund']})")


def pruefe(args):
    fehler = 0
    for clip in args.clips:
        e = lade(register_pfad(args, clip)).get(schluessel(clip))
        if not e:
            print(f"UNGESICHTET  {clip}")
            fehler += 1
        elif e["sha256"] != sha256(clip):
            print(f"GEÄNDERT     {clip} (Prüfsumme passt nicht mehr zur Sichtung)")
            fehler += 1
        elif e["status"] != "ok":
            print(f"{e['status'].upper():<12} {clip}" + (f" – {e.get('grund')}" if e.get("grund") else ""))
            fehler += 1
        else:
            print(f"OK           {clip} – {e.get('grund', '')}")
    if fehler:
        print(f"SPERRE: {fehler} von {len(args.clips)} Clips nicht freigegeben. Nicht bauen.")
        sys.exit(1)
    print("Alle Clips freigegeben.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("befehl", choices=["bilder", "freigabe", "pruefe"])
    ap.add_argument("clips", nargs="+")
    ap.add_argument("--n", type=int, default=5, help="Standbilder je Clip (bilder)")
    ap.add_argument("--lupe", action="store_true", help="zusätzlich 2×2-Ausschnitte in Quellauflösung")
    ap.add_argument("--out", help="Zielordner der Standbilder (Standard: <Clipordner>/_sichtung)")
    ap.add_argument("--register", help="Register-JSON (Standard: <Clipordner>/stock_sichtung.json)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--ok", action="store_true")
    g.add_argument("--sperre", action="store_true")
    ap.add_argument("--grund", default="")
    args = ap.parse_args()
    if args.befehl == "freigabe":
        if len(args.clips) != 1 or not (args.ok or args.sperre):
            ap.error("freigabe braucht genau einen Clip und --ok oder --sperre")
    if args.n < 1:
        ap.error("--n muss ≥ 1 sein")
    {"bilder": bilder, "freigabe": freigabe, "pruefe": pruefe}[args.befehl](args)


if __name__ == "__main__":
    main()
