#!/usr/bin/env bash
# Erzeugt cloud-setup.sh: ein Setup-Skript für Claude-Code-Cloud-Umgebungen, das alle Mods aus
# .claude-plugin/marketplace.json ohne Netzwerk (eingebettet) installiert. Nach jeder Mod-Änderung neu erzeugen.
set -euo pipefail
cd "$(dirname "$0")"
names=$(python3 -c "import json;print(' '.join(p['name'] for p in json.load(open('.claude-plugin/marketplace.json'))['plugins']))")
payload=$(tar --exclude='./cloud-setup.sh' --exclude='./build-cloud-setup.sh' --exclude='./tim-mods.tar.gz' --exclude='*/tests' --exclude='*/__pycache__' -czf - . | base64 -w0)
{
  printf '%s\n' '#!/usr/bin/env bash' \
    '# Claude-Code-Mods (tim-mods) für Cloud-Sessions installieren.' \
    '# claude.ai/code → Cloud-Umgebung bearbeiten → „Setup script“: diesen Inhalt einfügen.' \
    '# Installiert per dokumentiertem Weg: claude plugin marketplace add + claude plugin install (Scope: user).' \
    'set -euo pipefail' \
    'DEST="${HOME}/.claude-mods/tim-mods"' \
    'mkdir -p "$DEST"'
  printf "echo '%s' | base64 -d | tar -xzf - -C \"\$DEST\"\n" "$payload"
  printf '%s\n' 'claude plugin marketplace add "$DEST" >/dev/null 2>&1 || claude plugin marketplace update tim-mods >/dev/null 2>&1 || true' \
    "for m in ${names}; do" \
    '  claude plugin install "$m@tim-mods" --scope user >/dev/null 2>&1 || true' \
    'done' \
    "claude plugin list 2>/dev/null | grep -E '@tim-mods|Status' || true"
} > cloud-setup.sh
chmod +x cloud-setup.sh
# Kleines Paket für den SessionStart-Hook der Repos (ohne Tests, ohne spar-modus-Sonderbehandlung: das macht der Hook)
tar --exclude='*/tests' --exclude='*/__pycache__' -czf tim-mods.tar.gz $(for n in ${names}; do printf '%s ' "$n"; done)
echo "cloud-setup.sh: $(wc -c < cloud-setup.sh) Bytes, tim-mods.tar.gz: $(wc -c < tim-mods.tar.gz) Bytes, Mods: ${names}"
