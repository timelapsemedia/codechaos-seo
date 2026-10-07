#!/usr/bin/env python3
"""Misst eine Audiodatei mit ffmpeg (+ numpy) und gibt JSON aus. Keine Schätzwerte: was nicht messbar ist, fehlt.

Aufruf: audio_analyse.py <datei> [--spektrum <png>]
"""
import json, re, subprocess, sys

def run(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)

def probe(path):
    r = run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
             "stream=codec_name,sample_rate,channels,bits_per_raw_sample,bits_per_sample,sample_fmt:format=duration,bit_rate,format_name",
             "-of", "json", path])
    if r.returncode != 0:
        raise SystemExit(json.dumps({"fehler": "ffprobe: " + r.stderr.strip()[:300]}))
    d = json.loads(r.stdout)
    s = (d.get("streams") or [{}])[0]
    f = d.get("format", {})
    bits = s.get("bits_per_raw_sample") or s.get("bits_per_sample")
    return {
        "format": f.get("format_name"), "codec": s.get("codec_name"),
        "samplerate_hz": int(s["sample_rate"]) if s.get("sample_rate") else None,
        "kanaele": s.get("channels"), "bittiefe": int(bits) if bits and str(bits) != "0" else None,
        "dauer_s": round(float(f["duration"]), 3) if f.get("duration") else None,
        "bitrate_kbps": round(int(f["bit_rate"]) / 1000) if f.get("bit_rate") else None,
    }

def loudness(path):
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af",
             "ebur128=peak=true:framelog=quiet,astats=metadata=0:measure_perchannel=none:measure_overall=Peak_level+RMS_level+DC_offset",
             "-f", "null", "-"])
    t = r.stderr
    def num(pat):
        m = re.findall(pat, t)
        return float(m[-1]) if m else None
    out = {
        "lufs_integriert": num(r"I:\s+(-?[\d.]+) LUFS"),
        "lra_lu": num(r"LRA:\s+(-?[\d.]+) LU"),
        "true_peak_dbtp": num(r"Peak:\s+(-?[\d.]+|-inf) dBFS"),
        "sample_peak_dbfs": num(r"Peak level dB:\s+(-?[\d.]+)"),
        "rms_dbfs": num(r"RMS level dB:\s+(-?[\d.]+)"),
        "dc_offset": num(r"DC offset:\s+(-?[\d.]+)"),
    }
    if out["sample_peak_dbfs"] is not None and out["rms_dbfs"] is not None:
        out["crest_db"] = round(out["sample_peak_dbfs"] - out["rms_dbfs"], 2)
    return out

def pcm_stats(path, sr=22050):
    try:
        import numpy as np
    except ImportError:
        return {"hinweis": "numpy fehlt: Korrelation/Clipping/Bänder nicht gemessen"}
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(sr), "-"], capture_output=True)
    if r.returncode != 0 or not r.stdout:
        return {"hinweis": "Dekodieren fehlgeschlagen"}
    x = np.frombuffer(r.stdout, dtype=np.float32).reshape(-1, 2)
    l, rr = x[:, 0].astype(np.float64), x[:, 1].astype(np.float64)
    den = np.sqrt((l * l).sum() * (rr * rr).sum())
    corr = float((l * rr).sum() / den) if den > 0 else None
    side, mid = (l - rr) / 2, (l + rr) / 2
    sm = float(10 * np.log10(((side ** 2).mean() + 1e-20) / ((mid ** 2).mean() + 1e-20)))
    # Clipping: Samples am Vollausschlag (nach Resampling nur Näherung -> separat aus Original gezählt wäre exakter)
    mono = mid
    n = len(mono)
    bands = {"sub_20_60": (20, 60), "bass_60_250": (60, 250), "lowmid_250_2k": (250, 2000), "highmid_2k_6k": (2000, 6000), "hoehen_6k_11k": (6000, 11000)}
    energy = {k: 0.0 for k in bands}
    win = 8192
    if n >= win:
        hann = np.hanning(win)
        freqs = np.fft.rfftfreq(win, 1 / sr)
        for start in range(0, n - win, win * 4):
            spec = np.abs(np.fft.rfft(mono[start:start + win] * hann)) ** 2
            for k, (lo, hi) in bands.items():
                energy[k] += float(spec[(freqs >= lo) & (freqs < hi)].sum())
    total = sum(energy.values()) or 1.0
    return {
        "stereo_korrelation": round(corr, 3) if corr is not None else None,
        "side_zu_mid_db": round(sm, 1),
        "spektrale_anteile_prozent": {k: round(100 * v / total, 1) for k, v in energy.items()},
    }

def raender(path, sr):
    """Clipping und Anfang/Ende in Originalrate: Klick-Gefahr, wenn das letzte Sample nicht nahe 0 ist bzw. kein Fade da ist."""
    try:
        import numpy as np
    except ImportError:
        return {}
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-"], capture_output=True)
    if r.returncode != 0 or not r.stdout:
        return {}
    x = np.abs(np.frombuffer(r.stdout, dtype=np.float32).reshape(-1, 2)).max(axis=1)
    db = lambda v: round(float(20 * np.log10(max(float(v), 1e-10))), 1)
    n = max(1, int((sr or 44100) * 0.01))
    return {
        "geclippte_samples": int((x >= 0.9999).sum()),
        "erstes_sample_dbfs": db(x[0]), "letztes_sample_dbfs": db(x[-1]),
        "letzte_10ms_peak_dbfs": db(x[-n:].max()), "letzte_500ms_peak_dbfs": db(x[-50 * n:].max()),
    }

def silence(path):
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "silencedetect=n=-60dB:d=0.3", "-f", "null", "-"])
    starts = [float(v) for v in re.findall(r"silence_start: (-?[\d.]+)", r.stderr)]
    ends = [float(v) for v in re.findall(r"silence_end: (-?[\d.]+)", r.stderr)]
    return {"stille_abschnitte": len(starts), "stille_am_anfang_s": round(ends[0], 2) if starts and starts[0] <= 0.01 and ends else 0.0}

def spectrum(path, png):
    r = run(["ffmpeg", "-v", "error", "-y", "-i", path, "-lavfi", "showspectrumpic=s=1600x600:legend=1:scale=log:fscale=log", png])
    return png if r.returncode == 0 else None

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"fehler": "Datei fehlt"})); return
    path = sys.argv[1]
    res = {"datei": path, **probe(path), **loudness(path), **pcm_stats(path), **silence(path)}
    res.update(raender(path, res.get("samplerate_hz")))
    if "--spektrum" in sys.argv:
        res["spektrogramm_png"] = spectrum(path, sys.argv[sys.argv.index("--spektrum") + 1])
    print(json.dumps(res, ensure_ascii=False))

main()
