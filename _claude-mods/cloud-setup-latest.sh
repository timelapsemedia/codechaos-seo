#!/usr/bin/env bash
# Setup script for the cloud environment (claude.ai/code -> environment -> Edit -> Setup script).
# On every new cloud session it fetches the CURRENT version of all tim-mods + tim-skills from main
# (public package, about 2 MB) and puts them where Claude Code loads them. Changes on main arrive in the next session,
# so cloud and PC stay in step without editing this script again.
set -u
TMP="$(mktemp -d)"
if curl -fsSL --max-time 90 "https://raw.githubusercontent.com/timelapsemedia/codechaos-seo/refs/heads/main/_claude-mods/tim-mods.tar.gz" | tar -xz -C "$TMP"; then
  mkdir -p "$HOME/.claude/skills"
  for d in "$TMP"/*/; do
    n="$(basename "$d")"
    [ -f "$d/.claude-plugin/plugin.json" ] || continue
    [ "$n" = "spar-modus" ] && continue
    rm -rf "$HOME/.claude/skills/$n" && cp -R "$d" "$HOME/.claude/skills/$n"
  done
  echo "tim-mods loaded: $(ls "$HOME/.claude/skills" | tr '\n' ' ')"
else
  echo "tim-mods: download failed, session runs without mods"
fi
exit 0
