# Hinweise für Claude-Sessions in diesem Repo

## Abschluss jedes Laufs (Routinen und Cloud-Sessions)

Die Cloud-Umgebung prüft beim Beenden (Stop-Hook), ob der aktuelle Branch ungepushte Commits,
ungetrackte oder geänderte Dateien hat, und verlangt dann einen Push. Ohne Regel landet das als
Extra-Push auf einem Zufallsbranch (belegt: polished.media 19.11.2026, SEO-Routine 22.11.2026).
Tim, 25.11.2026: „ja“ – so entschärfen:

1. Hilfs-, Mess- und Zwischendateien ins Scratchpad, nicht ins Repo. Was ins Repo gehört, committen.
2. Nach dem Push auf main (`git push origin HEAD:main`, vorher `git pull --no-rebase origin main`)
   bzw. nach dem Mergen eines PRs lokal auf main zurückkehren:
   `git fetch origin main && git checkout -B main origin/main`.
   Dann ist der aktuelle Branch sauber und der Hook schweigt.
3. Meldet der Hook trotzdem etwas: **nicht** auf einen neuen Branch pushen. Ungewollte Dateien ins
   Scratchpad verschieben, fehlende Commits wie in Schritt 2 nach main bringen, Schritt 2 wiederholen.
