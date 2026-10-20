"""Product audio -> audio.json for the Reel (onset strength per band, 30 fps) + the matching audio section.

  python3 onsets.py <audio> <out_dir> [--seconds 10] [--start S]
Writes <out_dir>/audio.json and <out_dir>/section.wav. Without --start, picks the section with the most onsets.
Bands: low < 150 Hz (kick/sub), mid 1.5-6 kHz (snare/lead body), high 7-16 kHz (hats/air).
"""
import argparse, json, subprocess
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

ap = argparse.ArgumentParser()
ap.add_argument("audio"); ap.add_argument("out_dir")
ap.add_argument("--seconds", type=float, default=10.0); ap.add_argument("--start", type=float)
a = ap.parse_args()
x, sr = sf.read(a.audio); x = x if x.ndim == 1 else x.mean(1)
hop = sr // 60

def onset(sig, lo, hi):
    sos = butter(4, [lo, hi] if lo else hi, btype="band" if lo else "low", fs=sr, output="sos")
    y = np.abs(sosfilt(sos, sig)); n = len(y) // hop
    e = y[: n * hop].reshape(n, hop).max(1)
    return np.maximum(e - np.concatenate([[0], e[:-1]]), 0)

if a.start is None:
    o = sum(onset(x, *b) / (onset(x, *b).max() + 1e-9) for b in ((0, 150), (1500, 6000), (7000, 16000)))
    w = int(a.seconds * 60)
    a.start = max(range(0, max(1, len(o) - w), 30), key=lambda s: o[s:s + w].sum()) / 60
seg = x[int(a.start * sr): int((a.start + a.seconds) * sr)]

def track(lo, hi):
    o = onset(seg, lo, hi); o = o / (np.percentile(o[o > 0], 90) + 1e-9)
    o = o[: len(o) // 2 * 2].reshape(-1, 2).max(1).clip(0, 1)
    out, v = [], 0.0
    for k in o:
        v = max(float(k), v * 0.45); out.append(round(v, 3))
    return out

d = {"fps": 30, "start": a.start, "low": track(0, 150), "mid": track(1500, 6000), "high": track(7000, 16000)}
json.dump(d, open(f"{a.out_dir}/audio.json", "w"))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(a.start), "-t", str(a.seconds), "-i", a.audio, "-af",
                f"afade=t=in:d=0.05,afade=t=out:st={a.seconds - 0.6}:d=0.6", f"{a.out_dir}/section.wav"], check=True)
print(f"start {a.start:.2f}s, frames {len(d['low'])}, busy low/mid/high:",
      [round(float((np.array(d[k]) > 0.5).mean()), 2) for k in ("low", "mid", "high")])
