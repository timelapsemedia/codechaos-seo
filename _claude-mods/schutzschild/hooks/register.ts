import type { EngineInterface, Register } from 'claude-code'

export type Risk = { was: string; verlust: string; rueckgaengig: string }
type Rule = { re: RegExp; risk: Risk }

// Erkennung nach Mustern: hilft, garantiert aber keinen vollständigen Schutz.
const BASH: Rule[] = [
  { re: /\bgit\s+push\b[^\n;|&]*(\s--force\b|\s-f\b|\s--force-with-lease\b|\s\+\S+)/, risk: { was: 'Git-Verlauf auf dem Server mit „git push --force“ überschreiben', verlust: 'Commits auf dem Server, die lokal fehlen (auch die anderer Leute)', rueckgaengig: 'nur, wenn jemand die alten Commits noch hat (Reflog/anderer Klon)' } },
  { re: /\bgit\s+reset\b[^\n;|&]*--hard\b/, risk: { was: 'Alle nicht committeten Änderungen mit „git reset --hard“ verwerfen', verlust: 'ungespeicherte Änderungen an Dateien im Repository', rueckgaengig: 'nicht committete Änderungen: nein; Commits: über git reflog' } },
  { re: /\bgit\s+clean\b[^\n;|&]*\s-[a-zA-Z]*f/, risk: { was: 'Nicht versionierte Dateien mit „git clean -f“ löschen', verlust: 'alle Dateien, die nicht in Git sind (z. B. neue Dateien, .env, Builds)', rueckgaengig: 'nein' } },
  { re: /\bgit\s+(checkout|restore)\b[^\n;|&]*\s(--\s+)?\.(\s|$)/, risk: { was: 'Alle lokalen Änderungen mit „git checkout/restore .“ verwerfen', verlust: 'ungespeicherte Änderungen an versionierten Dateien', rueckgaengig: 'nein' } },
  { re: /\bgit\s+(stash\s+(drop|clear)|branch\s+-D|filter-branch|filter-repo)\b/, risk: { was: 'Git-Stash, Branch oder Verlauf endgültig entfernen/umschreiben', verlust: 'gestashte Änderungen, ungemergte Branches oder Verlauf', rueckgaengig: 'meist nur über git reflog, solange noch vorhanden' } },
  { re: /(^|[\s;&|(])(sudo\s+)?(rm|rmdir|unlink|shred)\s/, risk: { was: 'Dateien oder Ordner löschen', verlust: 'die genannten Dateien/Ordner (rm hat keinen Papierkorb)', rueckgaengig: 'nur aus Git oder einem Backup' } },
  { re: /\bfind\b[^\n]*\s(-delete\b|-exec\s+rm\b)/, risk: { was: 'Dateien per „find … -delete“ massenhaft löschen', verlust: 'alle Treffer der Suche', rueckgaengig: 'nur aus Git oder einem Backup' } },
  { re: /\b(drop\s+(table|database|schema|collection)|truncate\s+(table\s+)?\w)/i, risk: { was: 'Datenbank-Tabelle oder ganze Datenbank löschen/leeren', verlust: 'alle Datensätze darin', rueckgaengig: 'nur aus einem Datenbank-Backup' } },
  { re: /\bdelete\s+from\s+[\w."`]+\s*(;|$|"|')/i, risk: { was: 'Alle Zeilen einer Tabelle löschen (DELETE ohne WHERE)', verlust: 'alle Datensätze der Tabelle', rueckgaengig: 'nur aus einem Datenbank-Backup' } },
  { re: /\b(flushall|flushdb|dropDatabase\(\)|dropdb\s|db:drop|db:reset|migrate\s+reset|prisma\s+db\s+push\s+--force-reset)\b/i, risk: { was: 'Datenbank leeren oder zurücksetzen', verlust: 'alle gespeicherten Daten', rueckgaengig: 'nur aus einem Backup' } },
  { re: /(>|\btee\b(\s+-a)?|\bcp\b[^\n;|&]*|\bmv\b[^\n;|&]*)\s*\S*(^|\/|\s)\.env(\.[\w.-]+)?(\s|$|;)/, risk: { was: 'Eine .env-Datei überschreiben', verlust: 'Passwörter, API-Schlüssel und Einstellungen darin', rueckgaengig: 'nein, .env ist meist nicht in Git' } },
  { re: /\b(mkfs(\.\w+)?|dd\s+[^\n]*\bof=\/dev\/|diskutil\s+erase\w*|chmod\s+-R\s+0*0{3}\b|chown\s+-R\s+\S+\s+\/(\s|$))/, risk: { was: 'Datenträger oder Rechte im großen Stil verändern', verlust: 'Daten auf dem Datenträger oder Zugriff auf Dateien', rueckgaengig: 'kaum' } },
]

const SECRET_FILE = /(^|[\/\\])(\.env(\.[\w.-]+)?|\.npmrc|\.netrc|\.pypirc|credentials(\.json)?|secrets?\.(json|ya?ml|toml)|id_(rsa|ed25519|ecdsa)|[\w.-]+\.(pem|key|p12|pfx|keystore))$/i
const TEMP = /^(\/tmp\/|\/private\/tmp\/|\/var\/folders\/|\/private\/var\/folders\/|[a-z]:\/users\/[^/]+\/appdata\/local\/temp\/|[a-z]:\/windows\/temp\/)/i

const EDIT_TOOLS = new Set(['Edit', 'Write', 'MultiEdit', 'NotebookEdit'])

export function assessBash(command: string): Risk | undefined {
  return BASH.find(r => r.re.test(command))?.risk
}

const isWin = (p: string) => /^[a-zA-Z]:[\\/]/.test(p) || p.includes('\\')

/** Vereinheitlicht /unix/pfade und C:\\windows\\pfade (Laufwerk klein, Schrägstriche vorwärts). */
function normalize(p: string): string {
  const win = isWin(p)
  let rest = p.replace(/\\/g, '/')
  let prefix = ''
  const drive = rest.match(/^([a-zA-Z]):\//)
  if (drive) { prefix = drive[1]!.toLowerCase() + ':'; rest = rest.slice(2) }
  const out: string[] = []
  for (const part of rest.split('/')) {
    if (part === '' || part === '.') continue
    if (part === '..') out.pop()
    else out.push(win ? part.toLowerCase() : part)
  }
  return prefix + '/' + out.join('/')
}

const isAbs = (p: string) => p.startsWith('/') || /^[a-zA-Z]:[\\/]/.test(p) || p.startsWith('\\\\')

export function assessPath(path: string, root: string): Risk | undefined {
  if (SECRET_FILE.test(path)) {
    return { was: `Die Geheimnis-Datei „${path.split('/').pop()}“ ändern oder überschreiben`, verlust: 'Passwörter/Schlüssel darin, falls sie ersetzt werden', rueckgaengig: 'nein, solche Dateien sind meist nicht in Git' }
  }
  const abs = normalize(isAbs(path) ? path : `${root}/${path}`)
  const base = normalize(root)
  if (abs !== base && !abs.startsWith(base + '/') && !TEMP.test(abs)) {
    return { was: `Eine Datei außerhalb des Projekts ändern: ${abs}`, verlust: 'der bisherige Inhalt dieser Datei', rueckgaengig: 'nur, wenn die Datei woanders gesichert ist' }
  }
  return undefined
}

async function realRoot($: EngineInterface): Promise<string> {
  const root = await $.session.root()
  try {
    return (await $.fs.stat(root, { resolve: true })).realPath ?? root
  } catch {
    return root
  }
}

async function realTarget($: EngineInterface, path: string): Promise<string> {
  // Symlinks auflösen; existiert die Datei noch nicht, den Ordner darüber.
  try {
    return (await $.fs.stat(path, { resolve: true })).realPath ?? path
  } catch {
    const cut = path.lastIndexOf('/')
    if (cut <= 0) return path
    try {
      const dir = (await $.fs.stat(path.slice(0, cut), { resolve: true })).realPath
      return dir ? `${dir}/${path.slice(cut + 1)}` : path
    } catch {
      return path
    }
  }
}

async function bump($: EngineInterface, field: 'checked' | 'halted') {
  const day = new Date(await $.clock.now()).toISOString().slice(0, 10)
  const key = `stats:${day}`
  const s = ((await $.store.get(key)) as { checked: number; halted: number } | undefined) ?? { checked: 0, halted: 0 }
  s[field] += 1
  await $.store.set(key, s)
  $.ui.status(`🛡 heute ${s.checked} geprüft · ${s.halted} angehalten`)
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'schutzschild', description: 'Schutzschild an/aus und heutige Zahlen zeigen' })
    const day = new Date(await $.clock.now()).toISOString().slice(0, 10)
    const s = ((await $.store.get(`stats:${day}`)) as { checked: number; halted: number } | undefined) ?? { checked: 0, halted: 0 }
    const isOn = (await $.store.get('enabled')) !== false
    $.ui.status(isOn ? `🛡 heute ${s.checked} geprüft · ${s.halted} angehalten` : '🛡 Schutzschild aus')
    return next(e)
  })

  on('tool.call', async ($, e, next) => {
    if ((await $.store.get('enabled')) === false) return next(e)
    if (e.tool !== 'Bash' && !EDIT_TOOLS.has(String(e.tool))) return next(e)

    let risk: Risk | undefined
    try {
      if (e.tool === 'Bash') {
        risk = assessBash(e.command)
      } else {
        const raw = String((e as { file_path?: unknown }).file_path ?? (e as { notebook_path?: unknown }).notebook_path ?? '')
        risk = assessPath(await realTarget($, raw), await realRoot($))
      }
    } catch (err) {
      return { deny: `schutzschild: Risikoprüfung fehlgeschlagen (${String(err).slice(0, 200)}) – Schritt vorsichtshalber blockiert.` }
    }
    await bump($, 'checked')
    if (!risk) return next(e)

    await bump($, 'halted')
    const detail = e.tool === 'Bash' ? `\nBefehl: ${e.command.slice(0, 300)}` : ''
    let answer: string
    try {
      answer = await $.ui.ask(
        `🛡 Claude möchte: ${risk.was}.${detail}\nDabei kann verloren gehen: ${risk.verlust}.\nRückgängig machen: ${risk.rueckgaengig}.\nSoll Claude das ausführen?`,
        { header: 'Schutzschild', options: ['Nein, abbrechen', 'Ja, ausführen'] },
      )
    } catch {
      return { deny: `schutzschild: „${risk.was}“ wurde nicht bestätigt (keine Rückfrage möglich oder abgelehnt). Frag den Nutzer oder nimm einen sichereren Weg.` }
    }
    if (answer !== 'Ja, ausführen') {
      return { deny: `schutzschild: Der Nutzer hat „${risk.was}“ abgelehnt. Nicht erneut versuchen, ohne nachzufragen.` }
    }
    // Bestätigt: weiter durch die normalen Berechtigungsregeln (nichts wird pauschal erlaubt).
    return next(e)
  }).catch(($, e, next) => (next.called ? next(e) : { deny: `schutzschild: Risikoprüfung fehlgeschlagen (${next.error?.kind ?? 'Fehler'}) – Schritt blockiert.` }))

  on('command.run', { command: 'schutzschild' }, async $ => {
    const isOn = (await $.store.get('enabled')) === false
    await $.store.set('enabled', isOn)
    const day = new Date(await $.clock.now()).toISOString().slice(0, 10)
    const s = ((await $.store.get(`stats:${day}`)) as { checked: number; halted: number } | undefined) ?? { checked: 0, halted: 0 }
    $.ui.status(isOn ? `🛡 heute ${s.checked} geprüft · ${s.halted} angehalten` : '🛡 Schutzschild aus')
    return { text: `Schutzschild ist jetzt ${isOn ? 'AN' : 'AUS'}. Heute: ${s.checked} Schritte geprüft, ${s.halted} angehalten. Hinweis: Die Erkennung arbeitet mit Mustern und garantiert keinen vollständigen Schutz.` }
  })
}
