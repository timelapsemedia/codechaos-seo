#!/usr/bin/env bash
# Lädt die tim-mods in jede Session dieses Repos: kopiert sie nach ~/.claude/skills/<mod>
# (Claude Code übernimmt Plugins dort automatisch als <mod>@skills-dir) und fordert ein Neuladen an.
# Quelle: dieses Repo (_claude-mods/) oder, falls nicht vorhanden, das öffentliche Repo auf GitHub.
set -u
ZIEL="${HOME}/.claude/skills"
QUELLE="${CLAUDE_PROJECT_DIR:-$PWD}/_claude-mods"
if [ ! -f "$QUELLE/.claude-plugin/marketplace.json" ]; then
  TMP="$(mktemp -d)"
  if curl -fsSL --max-time 60 "https://codeload.github.com/timelapsemedia/codechaos-seo/tar.gz/refs/heads/main" | tar -xz -C "$TMP" 2>/dev/null; then
    QUELLE="$(ls -d "$TMP"/*/_claude-mods 2>/dev/null | head -1)"
  fi
fi
[ -n "${QUELLE:-}" ] && [ -d "$QUELLE" ] || { echo '{}'; exit 0; }
mkdir -p "$ZIEL"
for d in "$QUELLE"/*/; do
  n="$(basename "$d")"
  [ -f "$d/.claude-plugin/plugin.json" ] || continue
  [ "$n" = "spar-modus" ] && continue   # Experiment: nur auf ausdrücklichen Wunsch
  mkdir -p "$ZIEL/$n" && cp -R "$d". "$ZIEL/$n/"
done
echo '{"hookSpecificOutput":{"hookEventName":"SessionStart","reloadSkills":true}}'
