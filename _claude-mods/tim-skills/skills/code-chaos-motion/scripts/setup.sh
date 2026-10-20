#!/usr/bin/env bash
# Usage: setup.sh <workdir>   -> claude-motion at a pinned commit, deps installed, Reel template registered
set -euo pipefail
SKILL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIR="${1:-$HOME/claude-motion}"
COMMIT=e627941543d9988b155dc610bb9cc0115a5e365e
[ -d "$DIR/.git" ] || git clone -q https://github.com/whaleyxbt/claude-motion "$DIR"
cd "$DIR" && git fetch -q --depth 50 origin && git checkout -q "$COMMIT"
npm ci --ignore-scripts --no-audit --no-fund >/dev/null
grep -q "Reel" src/Root.tsx || python3 - <<'PY'
p='src/Root.tsx'; s=open(p).read()
s=s.replace("import {FPS, H, TL, W} from './lib';","import {FPS, H, TL, W} from './lib';\nimport {Reel, REEL_FPS, REEL_H, REEL_W} from './reel/Reel';\nimport REELTL from './reel/timeline.json';")
s=s.replace("    <Still id=","    <Composition id=\"Reel\" component={Reel} durationInFrames={REELTL.duration * REEL_FPS} fps={REEL_FPS} width={REEL_W} height={REEL_H} />\n    <Still id=",1)
open(p,'w').write(s)
PY
mkdir -p src/reel && for f in Reel.tsx timeline.json config.json; do [ -f src/reel/$f ] || cp "$SKILL/templates/reel/$f" src/reel/; done
echo "ready: $DIR (composition id: Reel)"
# Browser: in the cloud set REMOTION_BROWSER to the preinstalled headless shell; on Windows/Mac Remotion downloads its own on first render.
for b in /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell /usr/bin/chromium; do [ -x "$b" ] && { echo "export REMOTION_BROWSER=$b"; break; }; done
