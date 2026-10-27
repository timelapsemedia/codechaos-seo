#!/usr/bin/env bash
# Erzeugt cloud-setup.sh: ein Setup-Skript für Claude-Code-Cloud-Umgebungen, das alle Mods aus
# .claude-plugin/marketplace.json ohne Netzwerk (eingebettet) installiert. Nach jeder Mod-Änderung neu erzeugen.
set -euo pipefail
cd "$(dirname "$0")"
# Windows: „python3“ ist dort oft nur der Store-Platzhalter, dann „python“ nehmen.
PY=python3; "$PY" -c "" 2>/dev/null || PY=python
# Gate: jede SKILL.md braucht gültiges YAML-Frontmatter mit name + description (lostplace-hdr hatte
# „Tim, 2026-10-20: …“ unquotiert, Claude Code meldete „Failed to parse YAML frontmatter“).
"$PY" - <<'PYEOF'
import glob, sys
try:
    import yaml
except ImportError:
    print("Hinweis: PyYAML fehlt, Frontmatter-Prüfung übersprungen", file=sys.stderr); sys.exit(0)
bad = []
for p in sorted(glob.glob("*/skills/*/SKILL.md")):
    t = open(p, encoding="utf-8").read()
    try:
        y = yaml.safe_load(t.split("---")[1]) if t.startswith("---") else None
        assert isinstance(y, dict) and y.get("name") and y.get("description")
    except Exception as e:
        bad.append(f"{p}: {str(e).splitlines()[0] if str(e) else 'name/description fehlt'}")
if bad:
    sys.exit("Ungültiges SKILL.md-Frontmatter:\n  " + "\n  ".join(bad))
PYEOF
names=$("$PY" -c "import json;print(' '.join(p['name'] for p in json.load(open('.claude-plugin/marketplace.json'))['plugins']))")
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
