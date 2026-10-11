#!/usr/bin/env bash
# Baut die Wikipedia-Story/Reel (2160x3840) neu. Voraussetzungen: ffmpeg, python3 mit pillow, fonttools, brotli, numpy, scipy.
# Hintergrund: Higgsfield Topaz-Upscale, Job 59328b39-897f-43b6-b418-de2fa9c3ae3c (Quelle Seedance-Job 38ddc25b-a3a3-4738-ae3d-8cb4a47a8256)
set -euo pipefail
cd "$(dirname "$0")"
W=build; mkdir -p "$W"; cp overlays.py synth.py "$W"/; mkdir -p images; cp logo_quelle.jpg images/4.jpg
python3 - <<'PY'
from fontTools.ttLib import TTFont
for n in ["cinzel","eb-garamond","eb-garamond-italic"]:
    f=TTFont(f"../../fonts/{n}.woff2"); f.flavor=None; f.save(f"build/{n}.ttf")
PY
cd "$W"
[ -f bg4k.mp4 ] || curl -s -o bg4k.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3FMtIAsE6D0cRzFFQz1eWjr2KmC/hf_20261011_145833_59328b39-897f-43b6-b418-de2fa9c3ae3c.mp4"
sed -i 's#"../../images/4.jpg"#"../images/4.jpg"#' overlays.py
python3 overlays.py
python3 -c "
from PIL import Image
W,H=2160,3840; col=[]
for y in range(H):
    a=0
    if 1050<y<3250: a=int(150*min(1,min(y-1050,3250-y)/350))
    col.append(a)
g=Image.new('L',(1,H)); g.putdata(col); g=g.resize((W,H))
s=Image.new('RGBA',(W,H),(11,8,6,255)); s.putalpha(g); s.save('l0_scrim.png')"
python3 synth.py
ffmpeg -v error -y -i bed.wav -af loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000 bed_norm.wav
ffmpeg -v error -y -ss 0.6 -i bg4k.mp4 -i bed_norm.wav \
 -loop 1 -framerate 24 -i l0_scrim.png -loop 1 -framerate 24 -i l1_logo.png -loop 1 -framerate 24 -i l2_head.png \
 -loop 1 -framerate 24 -i l3_card.png -loop 1 -framerate 24 -i l4_claim.png -loop 1 -framerate 24 -i l5_url.png \
 -filter_complex "[0]setsar=1,setpts=PTS-STARTPTS[bg];[2]format=rgba[s];[3]format=rgba[l];\
[4]format=rgba,fade=in:st=0.6:d=0.6:alpha=1[h];[5]format=rgba,fade=in:st=1.8:d=0.6:alpha=1[c];\
[6]format=rgba,fade=in:st=3.0:d=0.6:alpha=1[k];[7]format=rgba,fade=in:st=4.1:d=0.5:alpha=1[u];\
[bg][s]overlay=shortest=1[a];[a][l]overlay=shortest=1[b];[b][h]overlay=shortest=1[c2];[c2][c]overlay=shortest=1[d];[d][k]overlay=shortest=1[e];[e][u]overlay=shortest=1,format=yuv420p[v]" \
 -map "[v]" -map 1:a -shortest -c:v libx264 -preset slow -crf 19 -profile:v high -level 5.2 -r 24 -c:a aac -b:a 192k -movflags +faststart ../codechaos_wikipedia_4k.mp4
echo "fertig: _social/wikipedia-story/codechaos_wikipedia_4k.mp4"
