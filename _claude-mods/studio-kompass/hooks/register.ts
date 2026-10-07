import type { EngineInterface, Register } from 'claude-code'

import { checkFile, findSecrets } from './checks'
import { ALWAYS, detect, PROFILES } from './profiles'

// Aktive Bereiche dieser Session (sticky, damit der System-Prompt stabil bleibt) und geänderte Dateien.
let active: string[] = []
let changed: string[] = []
let where = 'unbekannt'

const EDIT_TOOLS = new Set(['Edit', 'Write', 'MultiEdit', 'NotebookEdit'])

async function addProfiles($: EngineInterface, ids: string[]) {
  const fresh = ids.filter(id => !active.includes(id))
  if (fresh.length === 0) return
  active = [...active, ...fresh]
  await $.store.set(`active:${await $.session.id()}`, active)
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'studio', description: 'Aktive Arbeitsbereiche zeigen oder einen hinzufügen', argumentHint: '[musik|mastering|video|motion|social|seo|etsy|recherche]' })
    await $.command.register({ name: 'dateien', description: 'Alle in dieser Session geänderten Dateien mit vollem Pfad' })
    where = (await $.env.get('CLAUDE_CODE_REMOTE')) === 'true' ? 'Cloud-Session (Container in der Cloud, nicht dein Rechner)' : 'lokal auf deinem Rechner'
    active = ((await $.store.get(`active:${await $.session.id()}`)) as string[] | undefined) ?? []
    const repo = await $.session.repo()
    await addProfiles($, detect(`${JSON.stringify(repo ?? '')} ${await $.session.root()}`))
    return next(e)
  })

  on('prompt.submit', async ($, e, next) => {
    await addProfiles($, detect(e.text))
    const secrets = findSecrets(e.text)
    if (secrets.length === 0) return next(e)
    $.ui.toast(`studio-kompass: Deine Nachricht enthält vermutlich ein Geheimnis (${secrets.join(', ')}). Besser als Umgebungsvariable/API-Credential hinterlegen und den Schlüssel rotieren.`, { timeoutMs: 10000 })
    return next({
      ...e,
      context: [
        ...(e.context ?? []),
        `studio-kompass: Die Nachricht des Nutzers enthält vermutlich ${secrets.join(', ')}. Gib den Wert nie wieder aus, schreibe ihn in keine Repository-Datei und keinen Commit; empfiehl, ihn als Umgebungsvariable bzw. API-Credential der Umgebung zu hinterlegen und zu rotieren.`,
      ],
    })
  })

  on('prompt.compose', async ($, e, next) => {
    const r = await next(e)
    const parts = PROFILES.filter(p => active.includes(p.id)).map(p => `### ${p.name}\n${p.rules}`)
    const text = `${ALWAYS}\n- Diese Session läuft: ${where}.${parts.length ? `\n\nAktive Arbeitsbereiche:\n${parts.join('\n')}` : ''}`
    return { sections: [...r.sections, { id: 'studio-kompass:regeln', text, scope: 'session' as const }] }
  })

  on('tool.call', async ($, e, next) => {
    const r = await next(e)
    if (r.deny !== undefined || r.isError || !EDIT_TOOLS.has(String(e.tool))) return r
    const path = String((e as { file_path?: unknown }).file_path ?? (e as { notebook_path?: unknown }).notebook_path ?? '')
    if (path && !changed.includes(path)) changed = [...changed, path]
    const check = checkFile(path, '')
    if (!check) return r
    let content = ''
    try {
      content = String(await $.fs.read(path))
    } catch {
      return r
    }
    const result = checkFile(path, content)
    if (!result || result.issues.length === 0) return r
    const note = `studio-kompass ${result.kind}-Check für ${path}: ${result.issues.slice(0, 12).join('; ')}${result.issues.length > 12 ? ` (+${result.issues.length - 12} weitere)` : ''}. Prüfe, ob das beabsichtigt ist, und korrigiere sonst.`
    return { ...r, context: [...(r.context ?? []), note] }
  })

  on('command.run', { command: 'studio' }, async ($, e) => {
    const want = e.args.trim().toLowerCase()
    if (want) {
      const p = PROFILES.find(x => x.id === want)
      if (!p) return { text: `Unbekannt. Bereiche: ${PROFILES.map(x => x.id).join(', ')}` }
      await addProfiles($, [p.id])
      return { text: `Bereich „${p.name}“ aktiv (wirkt ab der nächsten Anfrage).` }
    }
    const list = PROFILES.filter(p => active.includes(p.id)).map(p => `• ${p.name}`)
    return { text: `Session läuft: ${where}\nAktive Bereiche:\n${list.length ? list.join('\n') : '• keine erkannt (mit /studio <bereich> hinzufügen)'}\nAutomatische Prüfungen: Untertitel (.srt/.vtt), HTML-SEO (.html), Captions (*caption*/post*.txt|md), Geheimnisse in Nachrichten.` }
  })

  on('command.run', { command: 'dateien' }, async () => ({
    text: changed.length ? `Geänderte Dateien (${where}):\n${changed.map(p => `• ${p}`).join('\n')}` : `Noch keine Datei geändert (${where}).`,
  }))
}
