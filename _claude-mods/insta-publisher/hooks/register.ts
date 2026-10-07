import type { EngineInterface, ProcessRunResult, Register } from 'claude-code'

import { istPython3, letztesJson, PY_ENV, PY_KANDIDATEN } from './py'

// Python-Interpreter einmal pro Laden ermitteln (python3 / python / py -3).
let interpreter: string[] | undefined

async function python($: EngineInterface): Promise<string[]> {
  if (interpreter) return interpreter
  for (const c of PY_KANDIDATEN) {
    try {
      if (istPython3(await $.process.run([...c, '--version'], { timeoutMs: 15_000 }))) return (interpreter = c)
    } catch {
      // nächster Kandidat
    }
  }
  return (interpreter = ['python3'])
}

async function skript($: EngineInterface, name: string, args: string[], timeoutMs = 600_000): Promise<ProcessRunResult> {
  return $.process.run([...(await python($)), `${$.plugin.root}/tools/${name}`, ...args], { timeoutMs, env: PY_ENV })
}

export type Zugang = { token?: string; tokenEnv?: string; userId: string; api: 'facebook' | 'instagram'; version: string; appId?: string; appSecretEnv?: string }

export function ohneGeheimnis(text: string, geheim: (string | undefined)[]): string {
  return geheim.filter((g): g is string => !!g && g.length > 8).reduce((t, g) => t.split(g).join('***'), text)
}

export const TOKEN_VARS = ['IG_TOKEN', 'INSTAGRAM_ACCESS_TOKEN', 'META_ACCESS_TOKEN'] as const
export const SECRET_VARS = ['IG_APP_SECRET', 'META_APP_SECRET'] as const

// $.env.get braucht feste Namen: so ist sichtbar, welche Variablen diese Mod liest.
async function leseVar($: EngineInterface, name: string | undefined): Promise<string | undefined> {
  switch (name) {
    case 'IG_TOKEN': return $.env.get('IG_TOKEN')
    case 'INSTAGRAM_ACCESS_TOKEN': return $.env.get('INSTAGRAM_ACCESS_TOKEN')
    case 'META_ACCESS_TOKEN': return $.env.get('META_ACCESS_TOKEN')
    case 'IG_APP_SECRET': return $.env.get('IG_APP_SECRET')
    case 'META_APP_SECRET': return $.env.get('META_APP_SECRET')
    default: return undefined
  }
}

async function zugang($: EngineInterface): Promise<{ z?: Zugang; token?: string; secret?: string }> {
  const z = (await $.store.get('zugang')) as Zugang | undefined
  if (!z) return {}
  const token = z.tokenEnv ? await leseVar($, z.tokenEnv) : z.token
  const secret = z.appSecretEnv ? await leseVar($, z.appSecretEnv) : undefined
  return { z, token, secret }
}

async function ig($: EngineInterface, args: string[]): Promise<Record<string, unknown>> {
  const { z, token, secret } = await zugang($)
  if (!z || !token) return { fehler: 'Kein Instagram-Zugang hinterlegt (ig_zugang_speichern) oder die Umgebungsvariable ist leer.' }
  const env: Record<string, string> = { ...PY_ENV, IG_TOKEN: token, IG_USER_ID: z.userId, IG_API: z.api, IG_VERSION: z.version }
  if (z.appId) env.IG_APP_ID = z.appId
  if (secret) env.IG_APP_SECRET = secret
  const r = await $.process.run([...(await python($)), `${$.plugin.root}/tools/ig.py`, ...args], { timeoutMs: 600_000, env })
  return JSON.parse(ohneGeheimnis(JSON.stringify(letztesJson(r)), [token, secret])) as Record<string, unknown>
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.tool.register({
      name: 'ig_zugang_speichern',
      description: 'Hinterlegt den Instagram-Zugang einmalig für alle Sessions: am besten token_env (Umgebungsvariable IG_TOKEN, INSTAGRAM_ACCESS_TOKEN oder META_ACCESS_TOKEN, z. B. in der Cloud-Umgebung gesetzt), sonst token direkt (wird lokal im Plugin-Speicher abgelegt, nie wieder ausgegeben). Danach NIE den Token in Routinen/Prompts schreiben – nur noch die ig_*-Werkzeuge nutzen.',
      inputSchema: { type: 'object', properties: { token: { type: 'string' }, token_env: { type: 'string', enum: [...TOKEN_VARS] }, ig_user_id: { type: 'string' }, api: { type: 'string', enum: ['facebook', 'instagram'], description: 'facebook = Facebook-Login/Business (graph.facebook.com), instagram = Instagram-Login (graph.instagram.com)' }, version: { type: 'string' }, app_id: { type: 'string' }, app_secret_env: { type: 'string', enum: [...SECRET_VARS] } }, required: ['ig_user_id'] },
    })
    await $.tool.register({ name: 'ig_status', description: 'Prüft den hinterlegten Instagram-Zugang: Konto, Follower, Beitragszahl (ohne den Token zu zeigen).', inputSchema: { type: 'object', properties: {} } })
    await $.tool.register({
      name: 'ig_posten',
      description: 'Veröffentlicht auf Instagram (bild, karussell 2–10, reel) über öffentlich erreichbare Medien-URLs, UTF-8-sicher, wartet auf die Verarbeitung, wiederholt bei Ratenlimit und prüft danach, ob der Beitrag live ist (Permalink). Nur mit bestaetigt=true nach ausdrücklicher Freigabe des Nutzers oder in einer vom Nutzer eingerichteten Routine; ohne bestaetigt gibt es nur eine Vorschau.',
      inputSchema: { type: 'object', properties: { typ: { type: 'string', enum: ['bild', 'karussell', 'reel'] }, medien: { type: 'array', items: { type: 'string' } }, caption: { type: 'string' }, cover_url: { type: 'string' }, bestaetigt: { type: 'boolean' } }, required: ['typ', 'medien', 'caption'] },
    })
    await $.tool.register({ name: 'ig_insights', description: 'Holt die letzten Beiträge mit Likes, Kommentaren und Insights (Reichweite, Views, Saves, Shares – soweit die API sie je Medientyp liefert) als JSON für Analysen/Berichte.', inputSchema: { type: 'object', properties: { anzahl: { type: 'number' } } } })
    await $.tool.register({ name: 'ig_token_verlaengern', description: 'Verlängert den langlebigen Token (Instagram-Login: ig_refresh_token; Facebook-Login: fb_exchange_token mit App-ID/Secret) und speichert den neuen automatisch. Gibt nur die neue Laufzeit aus.', inputSchema: { type: 'object', properties: {} } })
    return next(e)
  })

  on('prompt.compose', async ($, e, next) => {
    const r = await next(e)
    const text = 'Instagram (Plugin „insta-publisher“): Tokens niemals in Routinen, Prompts, Dateien oder Commits schreiben; zum Posten, für Insights und Token-Verlängerung die Werkzeuge mcp__insta-publisher__ig_* nutzen. Vor dem Posten Caption mit social-studio prüfen, falls vorhanden.'
    return { sections: [...r.sections, { id: 'insta-publisher:regel', text, scope: 'session' as const }] }
  })

  on('tool.call', { tool: 'mcp__insta-publisher__ig_zugang_speichern' }, async ($, e) => {
    const i = e as unknown as { token?: string; token_env?: string; ig_user_id: string; api?: 'facebook' | 'instagram'; version?: string; app_id?: string; app_secret_env?: string }
    if (!i.token && !i.token_env) return { result: 'Bitte token_env (empfohlen) oder token angeben.' }
    const z: Zugang = { userId: i.ig_user_id, api: i.api ?? 'facebook', version: i.version ?? 'v21.0', ...(i.token_env ? { tokenEnv: i.token_env } : { token: i.token }), ...(i.app_id ? { appId: i.app_id } : {}), ...(i.app_secret_env ? { appSecretEnv: i.app_secret_env } : {}) }
    await $.store.set('zugang', z)
    return { result: `Zugang gespeichert (Konto ${z.userId}, API ${z.api} ${z.version}, Token ${z.tokenEnv ? `aus Umgebungsvariable ${z.tokenEnv}` : 'im Plugin-Speicher'}). Prüfe jetzt mit ig_status.` }
  })

  on('tool.call', { tool: 'mcp__insta-publisher__ig_status' }, async $ => ({ result: JSON.stringify(await ig($, ['status']), null, 1) }))

  on('tool.call', { tool: 'mcp__insta-publisher__ig_posten' }, async ($, e) => {
    const i = e as unknown as { typ: string; medien: string[]; caption: string; cover_url?: string; bestaetigt?: boolean }
    if (i.bestaetigt !== true) {
      return { result: `VORSCHAU – nichts veröffentlicht.\nTyp: ${i.typ}, ${i.medien.length} Medien\nCaption (${[...i.caption].length} Zeichen):\n${i.caption}\n\nZum Veröffentlichen nach Freigabe des Nutzers erneut mit bestaetigt=true aufrufen.` }
    }
    const auftrag = JSON.stringify({ typ: i.typ, medien: i.medien, caption: i.caption, ...(i.cover_url ? { cover_url: i.cover_url } : {}) })
    return { result: JSON.stringify(await ig($, ['posten', auftrag]), null, 1) }
  })

  on('tool.call', { tool: 'mcp__insta-publisher__ig_insights' }, async ($, e) => {
    const i = e as unknown as { anzahl?: number }
    return { result: JSON.stringify(await ig($, ['insights', String(Math.min(Math.max(1, i.anzahl ?? 12), 50))]), null, 1) }
  })

  on('tool.call', { tool: 'mcp__insta-publisher__ig_token_verlaengern' }, async $ => {
    const { z } = await zugang($)
    const r = (await ig($, ['token_verlaengern'])) as { neuer_token?: string; laeuft_ab_in_s?: number; fehler?: string }
    if (r.fehler || !r.neuer_token || !z) return { result: `Nicht verlängert: ${r.fehler ?? 'keine Antwort'}` }
    if (z.tokenEnv) return { result: `Neuer Token erhalten (läuft in ${Math.round((r.laeuft_ab_in_s ?? 0) / 86400)} Tagen ab), aber der Zugang liest aus der Umgebungsvariable ${z.tokenEnv}: dort muss der Nutzer ihn ersetzen. Token wird hier bewusst nicht angezeigt.` }
    await $.store.set('zugang', { ...z, token: r.neuer_token })
    return { result: `Token verlängert und gespeichert (läuft in ${Math.round((r.laeuft_ab_in_s ?? 0) / 86400)} Tagen ab).` }
  })
}
