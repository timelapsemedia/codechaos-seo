"""Render stills of a composition and tile them into one contact sheet you can look at.

  python3 sheet.py <claude-motion dir> <CompositionId> <out.png> 0 45 100 140 250 299
"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw

d, comp, out, frames = sys.argv[1], sys.argv[2], sys.argv[3], [int(f) for f in sys.argv[4:]]
ims = []
with tempfile.TemporaryDirectory() as tmp:
    for f in frames:
        p = os.path.join(tmp, f"{f}.png")
        subprocess.run(["npx", "remotion", "still", comp, p, f"--frame={f}", "--scale=0.5"], cwd=d, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        im = Image.open(p).convert("RGB"); ImageDraw.Draw(im).text((8, 8), f"f{f}", fill=(255, 255, 0)); ims.append(im)
w, h = ims[0].size
sheet = Image.new("RGB", (len(ims) * (w + 10), h), "white")
for i, im in enumerate(ims):
    sheet.paste(im, (i * (w + 10), 0))
sheet.save(out); print(out)
