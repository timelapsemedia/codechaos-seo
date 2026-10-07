#!/usr/bin/env bash
# Erzeugt cloud-setup.sh: ein Setup-Skript für Claude-Code-Cloud-Umgebungen, das die Mods
# ohne Netzwerk-Zugriff (eingebettet) installiert. Neu erzeugen nach jeder Mod-Änderung.
set -euo pipefail
cd "$(dirname "$0")"
payload=$(tar --exclude='./cloud-setup.sh' --exclude='./build-cloud-setup.sh' --exclude='*/tests' -czf - . | base64 -w0)
cat > cloud-setup.sh <<SCRIPT
#!/usr/bin/env bash
# Claude-Code-Mods (tim-mods) für Cloud-Sessions installieren.
# In claude.ai/code → Cloud-Umgebung bearbeiten → „Setup script“ einfügen (oder von dort aus aufrufen).
# Installiert per dokumentiertem Weg: claude plugin marketplace add + claude plugin install (Scope: user).
set -euo pipefail
DEST="\${HOME}/.claude-mods/tim-mods"
mkdir -p "\$DEST"
echo '${payload}' | base64 -d | tar -xzf - -C "\$DEST"
claude plugin marketplace add "\$DEST" >/dev/null 2>&1 || claude plugin marketplace update tim-mods >/dev/null 2>&1 || true
for m in limit-cockpit pruefer schutzschild spar-modus studio-kompass; do
  claude plugin install "\$m@tim-mods" --scope user >/dev/null 2>&1 || true
done
claude plugin list 2>/dev/null | grep -E '@tim-mods|Status' || true
SCRIPT
chmod +x cloud-setup.sh
echo "cloud-setup.sh: $(wc -c < cloud-setup.sh) Bytes"
