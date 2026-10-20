---
name: code-chaos-motion
description: Animated promo videos and reels coded with Remotion (claude-motion toolkit). The video reacts to the product's real audio and is checked frame by frame before it ships. Use whenever Tim, Code Chaos, Code Chaos Audio, Polished Metal Mastering or a routine needs a promo video, reel, short, launch clip, animated post, motion graphic, explainer or simulation video. That includes plugin, sample-pack or preset-bank launches and social posts with video. Trigger phrases include "Reel", "Promo-Video", "animiertes Video", "Motion", "Short", "Launch-Video" and "mach ein Video für den Post". Prefer this over static image-plus-zoom videos.
---

# Code Chaos Motion

Videos are written as code (React/Remotion) and rendered frame by frame. The motion reacts to the product's **real** audio.
Toolkit: [whaleyxbt/claude-motion](https://github.com/whaleyxbt/claude-motion) (MIT, pinned in `scripts/setup.sh`). Remotion is free for individuals and small teams.

## Files
- `scripts/setup.sh <dir>`: clones claude-motion at the pinned commit, runs `npm ci`, registers the `Reel` composition and prints the browser path.
- `scripts/onsets.py <audio> <dir>`: writes `audio.json` (onsets per band at 30 fps) and `section.wav` (the matching 10 s of audio).
- `scripts/sheet.py`: renders stills and tiles them into one contact sheet. You **must** look at it before calling a video done.
- `templates/reel/`: `Reel.tsx`, `timeline.json` and `config.json`. A 10 s 1080×1920 reel: title, an audio-driven step grid, 3 rolling numbers, then price and CTA. Tested with the Black Metal Drum Kit.
- `references/`: the toolkit's taste rules. Read `motion-design.md` and `review-loop.md` before your first video in a session. Read `sound-design.md` when there is no product audio, and `web-sims.md` for simulations and 3D.

## Workflow
1. **Message and storyboard.** One message, one hero moment. Formats:
   - reel/short 1080×1920
   - feed 1080×1350
   - square 1080×1080
   - 30 fps is enough for social.
2. **Setup.** Run `bash scripts/setup.sh ~/claude-motion`, then `export REMOTION_BROWSER=…` (the script prints the path).
   - Cloud: the preinstalled headless shell under `/opt/pw-browsers`.
   - Windows/Mac: Remotion downloads its own browser on the first render.
3. **Audio.** Run `python3 scripts/onsets.py <demo.wav|mp3> ~/claude-motion/src/reel`.
   - Use real product audio: a plugin render, a pack demo or a preset demo. Never use third-party music.
   - With no audio, use the toolkit's own `sfx` engine (see `references/sound-design.md`).
4. **Content.** Edit `src/reel/config.json`:
   - text fields: `kicker`, `title1`, `title2`, `subtitle`, `rows` (labels for high/mid/low), `stats` (exactly 3), `price`, `formats`, `cta`;
   - `palette` overrides tokens (`bg`, `cream`, `creamDim`, `muted`, `copper`, `hot`, `cell`, `line`).

   Put beats in `timeline.json` only, never as times inside a component. For a different layout (GUI screenshot, preset names, before/after), copy the template into a new folder, register it as its own composition, and keep the rules.
5. **Review loop.**
   - Run `python3 scripts/sheet.py ~/claude-motion Reel /tmp/sheet.png 0 45 100 140 250 299` and look at the image. Check:
     - frame 0 shows the title (it is the thumbnail);
     - no text or numbers visible before their entrance (the bug was "0 0 0");
     - no overlaps;
     - readable at phone width;
     - the audio visual shows rhythm (if the grid is always full, use onsets instead of loudness);
     - nothing important in the bottom ~350 px or top ~200 px (Instagram/TikTok UI).
   - Fix and repeat until a pass is clean.
6. **Render.** Run `npx remotion render Reel out/silent.mp4` (about 70 s for 10 s of video). Then mux:
   ```
   ffmpeg -y -i out/silent.mp4 -i src/reel/section.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest out/reel.mp4
   ```
   Check the result with `ffprobe` (1080×1920, h264 + aac, duration).
7. **Hand-off.**
   - Send the video to Tim, or use it in the post pipeline.
   - Code Chaos: `codechaos-seo/images/social/<slug>.mp4` plus the `video` field in `_marketing/crucible-posts.json`.

## Brands
- **Code Chaos / Code Chaos Audio:** bg `#0C0A09`, accent copper `#D67834`, hot `#FFAA50`, cream `#F5ECE4`. Fonts Instrument Serif, Inter and JetBrains Mono (from the toolkit). Kicker "CODE CHAOS AUDIO".
- **Polished Metal Mastering:** take the colours and fonts from the existing pages on polished.media or the repo `timelapsemedia/polished`. Do not guess them.

## Rules
- Animation is a pure function of the frame. No CSS animations, no `Math.random()`, no `Date`.
- One accent colour per frame, one focal point, readable holds of at least 1 s and at least 2 s on the final hook. Exits are faster than entrances.
- Claims in the video must match the product description: numbers, formats, price.
- Never use third-party audio, logos or footage.
