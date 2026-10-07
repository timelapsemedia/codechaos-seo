#!/usr/bin/env python3
"""Misst ein Video mit ffprobe/ffmpeg und gibt JSON aus: Format, Bild, Ton-Lautheit, Schwarzbilder, Schnitte, Kontaktbogen.

Aufruf: video_analyse.py <datei> [--bogen <png>] [--schnitte]
"""
import json, re, subprocess, sys
from fractions import Fraction

def run(args):
    return subprocess.run(args, capture_output=True, text=True)

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"fehler": "Datei fehlt"})); return
    path = sys.argv[1]
    r = run(["ffprobe", "-v", "error", "-show_entries",
             "stream=index,codec_type,codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels,bit_rate,display_aspect_ratio:stream_side_data=rotation:format=duration,bit_rate,size,format_name",
             "-of", "json", path])
    if r.returncode != 0:
        print(json.dumps({"fehler": "ffprobe: " + r.stderr.strip()[:300]})); return
    d = json.loads(r.stdout)
    fmt = d.get("format", {})
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), None)
    a = next((s for s in d.get("streams", []) if s.get("codec_type") == "audio"), None)
    dur = float(fmt["duration"]) if fmt.get("duration") else None
    res = {"datei": path, "container": fmt.get("format_name"), "dauer_s": round(dur, 3) if dur else None,
           "groesse_mb": round(int(fmt["size"]) / 1e6, 2) if fmt.get("size") else None,
           "bitrate_mbps": round(int(fmt["bit_rate"]) / 1e6, 2) if fmt.get("bit_rate") else None}
    if v:
        w, h = v.get("width"), v.get("height")
        rot = 0
        for sd in v.get("side_data_list", []) or []:
            if "rotation" in sd:
                rot = int(sd["rotation"])
        if abs(rot) in (90, 270) and w and h:
            w, h = h, w
        fps = float(Fraction(v["r_frame_rate"])) if v.get("r_frame_rate") and v["r_frame_rate"] != "0/0" else None
        ratio = Fraction(w, h).limit_denominator(30) if w and h else None
        res.update({"video_codec": v.get("codec_name"), "breite": w, "hoehe": h, "rotation": rot,
                    "seitenverhaeltnis": f"{ratio.numerator}:{ratio.denominator}" if ratio else None,
                    "fps": round(fps, 3) if fps else None, "pix_fmt": v.get("pix_fmt")})
    if a:
        res.update({"audio_codec": a.get("codec_name"), "audio_hz": int(a["sample_rate"]) if a.get("sample_rate") else None, "audio_kanaele": a.get("channels")})
        t = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn", "-af", "ebur128=peak=true:framelog=quiet", "-f", "null", "-"]).stderr
        def num(p):
            m = re.findall(p, t)
            return float(m[-1]) if m else None
        res.update({"audio_lufs": num(r"I:\s+(-?[\d.]+) LUFS"), "audio_true_peak_dbtp": num(r"Peak:\s+(-?[\d.]+) dBFS")})
    else:
        res["audio"] = "keine Tonspur"
    if v:
        t = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-an", "-vf", "blackdetect=d=0.2:pix_th=0.10", "-f", "null", "-"]).stderr
        blacks = [(float(s), float(e)) for s, e in re.findall(r"black_start:(-?[\d.]+) black_end:(-?[\d.]+)", t)]
        res["schwarzbilder"] = [{"von_s": round(s, 2), "bis_s": round(e, 2)} for s, e in blacks][:20]
        if "--schnitte" in sys.argv:
            t = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-an", "-vf", "select='gt(scene,0.35)',showinfo", "-f", "null", "-"]).stderr
            cuts = [round(float(x), 2) for x in re.findall(r"pts_time:([\d.]+)", t)]
            res["schnitte_s"] = cuts[:200]
            res["schnitte_anzahl"] = len(cuts)
        if "--bogen" in sys.argv and dur:
            png = sys.argv[sys.argv.index("--bogen") + 1]
            n = 12
            vf = f"fps={n}/{max(dur, 0.1):.3f},scale=480:-2,tile=4x3:padding=4:margin=4"
            ok = run(["ffmpeg", "-v", "error", "-y", "-i", path, "-vf", vf, "-frames:v", "1", png]).returncode == 0
            res["kontaktbogen_png"] = png if ok else None
    print(json.dumps(res, ensure_ascii=False))

main()
