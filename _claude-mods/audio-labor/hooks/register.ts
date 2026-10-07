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

export type Messung = Record<string, unknown> & {
  lufs_integriert?: number | null
  true_peak_dbtp?: number | null
  lra_lu?: number | null
  crest_db?: number
  stereo_korrelation?: number | null
  geclippte_samples?: number | null
  stille_am_anfang_s?: number
  letztes_sample_dbfs?: number
  letzte_10ms_peak_dbfs?: number
  fehler?: string
}

export type Ziel = { name: string; lufs: [number, number]; tpMax: number; quelle: string }

// Plattform-Normalisierung ist dokumentiert; Genre-Lautheiten sind gängige Praxis, keine Norm.
export const ZIELE: Record<string, Ziel> = {
  streaming_laut: { name: 'Lautes Streaming-Master (ca. −11 LUFS)', lufs: [-12, -10], tpMax: -1, quelle: 'Praxis-Richtwert, keine Norm' },
  streaming: { name: 'Streaming (Spotify/YouTube normalisieren auf ca. −14 LUFS)', lufs: [-15, -13], tpMax: -1, quelle: 'Plattform-Normalisierung' },
  apple: { name: 'Apple Music (ca. −16 LUFS)', lufs: [-17, -15], tpMax: -1, quelle: 'Plattform-Normalisierung' },
  hitech: { name: 'Hitech/Psytrance/Psycore Club-Master', lufs: [-8, -5], tpMax: -0.3, quelle: 'Praxis-Richtwert, keine Norm' },
  metal: { name: 'Death/Thrash Metal laut', lufs: [-10, -6], tpMax: -0.5, quelle: 'Praxis-Richtwert, keine Norm' },
  blackmetal: { name: 'Atmospheric Black Metal (mehr Dynamik)', lufs: [-12, -8], tpMax: -1, quelle: 'Praxis-Richtwert, keine Norm' },
  podcast: { name: 'Sprache/Podcast', lufs: [-17, -15], tpMax: -1, quelle: 'gängige Empfehlung' },
}

export function bewerte(m: Messung, zielId: string | undefined): string[] {
  const out: string[] = []
  const z = zielId ? ZIELE[zielId] : undefined
  if (m.fehler) return [`Fehler: ${m.fehler}`]
  if (z && typeof m.lufs_integriert === 'number') {
    const [lo, hi] = z.lufs
    if (m.lufs_integriert < lo) out.push(`Leiser als Ziel „${z.name}“: ${m.lufs_integriert} LUFS < ${lo} (${z.quelle}).`)
    else if (m.lufs_integriert > hi) out.push(`Lauter als Ziel „${z.name}“: ${m.lufs_integriert} LUFS > ${hi} (${z.quelle}).`)
    else out.push(`Lautheit im Ziel „${z.name}“ (${lo} bis ${hi} LUFS).`)
  }
  const tpMax = z?.tpMax ?? -1
  if (typeof m.true_peak_dbtp === 'number' && m.true_peak_dbtp > tpMax) out.push(`True Peak ${m.true_peak_dbtp} dBTP über ${tpMax} dBTP – Gefahr von Verzerrung nach MP3/AAC-Encoding.`)
  if (typeof m.geclippte_samples === 'number' && m.geclippte_samples > 0) out.push(`${m.geclippte_samples} Samples am Vollausschlag (Clipping).`)
  if (typeof m.stereo_korrelation === 'number' && m.stereo_korrelation < 0.2) out.push(`Stereo-Korrelation ${m.stereo_korrelation}: Phasenprobleme/Mono-Inkompatibilität prüfen.`)
  if (typeof m.crest_db === 'number' && m.crest_db < 6) out.push(`Crest-Faktor ${m.crest_db} dB: sehr stark verdichtet.`)
  if (typeof m.stille_am_anfang_s === 'number' && m.stille_am_anfang_s > 0.5) out.push(`${m.stille_am_anfang_s} s Stille am Anfang.`)
  if (typeof m.letzte_10ms_peak_dbfs === 'number' && m.letzte_10ms_peak_dbfs > -40) out.push(`Ende ohne Ausklang (letzte 10 ms bei ${m.letzte_10ms_peak_dbfs} dBFS) – Klick-Gefahr, Fade-out setzen.`)
  else if (typeof m.letztes_sample_dbfs === 'number' && m.letztes_sample_dbfs > -60) out.push(`Letztes Sample bei ${m.letztes_sample_dbfs} dBFS – nicht bei null, Klick möglich.`)
  return out
}

async function messen($: EngineInterface, datei: string, spektrum: boolean): Promise<Messung> {
  const args = [datei]
  if (spektrum) args.push('--spektrum', `${datei.replace(/\.[^./\\]+$/, '')}.spektrum.png`)
  return letztesJson<Messung>(await skript($, 'audio_analyse.py', args))
}

export const AUDIO = /\.(wav|flac|aiff?|mp3|m4a|aac|ogg|opus)$/i
// Bereits gewarnte Dateien: ein zweiter Versand derselben Datei geht durch (bewusste Entscheidung).
const gewarnt = new Set<string>()

const ZIEL_SCHEMA = { type: 'string', enum: Object.keys(ZIELE), description: 'Zielprofil für die Bewertung' }

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.tool.register({
      name: 'messen',
      description: 'Misst eine Audiodatei (WAV/FLAC/MP3/…) wirklich mit ffmpeg: Integrated LUFS, LRA, True Peak, Sample Peak, RMS, Crest, DC-Offset, Stereo-Korrelation, Side/Mid, Frequenzanteile (Sub/Bass/LowMid/HighMid/Höhen), geclippte Samples, Stille am Anfang; optional Spektrogramm-PNG (danach mit Read ansehen). Nutze das statt Werte zu schätzen, vor und nach jedem Mastering-/Mixschritt.',
      inputSchema: { type: 'object', properties: { datei: { type: 'string' }, ziel: ZIEL_SCHEMA, spektrum: { type: 'boolean' } }, required: ['datei'] },
    })
    await $.tool.register({
      name: 'vergleichen',
      description: 'Misst zwei Audiodateien (z. B. vorher/nachher Master oder eigener Track vs. Referenz) und zeigt die Unterschiede in LUFS, True Peak, LRA, Crest, Stereo und Frequenzanteilen.',
      inputSchema: { type: 'object', properties: { vorher: { type: 'string' }, nachher: { type: 'string' }, ziel: ZIEL_SCHEMA }, required: ['vorher', 'nachher'] },
    })
    await $.tool.register({
      name: 'midi_pruefen',
      description: 'Liest eine MIDI-Datei (ohne Zusatzbibliotheken): Tempo, Taktart, Länge in Takten, Spuren, Notenzahl, Tonumfang, Tonklassen; mit skala (z. B. „A phrygisch“, „F# moll“, „E phrygisch_dominant“) die Töne außerhalb der Skala.',
      inputSchema: { type: 'object', properties: { datei: { type: 'string' }, skala: { type: 'string' } }, required: ['datei'] },
    })
    await $.tool.register({
      name: 'lua_pruefen',
      description: 'Syntaxprüfung für Lua/ReaScript (REAPER) per luaparse: Fehler mit Zeile, verwendete reaper.*-Funktionen, unbekannte Globale (Tippfehler-Verdacht). Braucht node.',
      inputSchema: { type: 'object', properties: { datei: { type: 'string' } }, required: ['datei'] },
    })
    return next(e)
  })

  on('tool.call', { tool: 'mcp__audio-labor__midi_pruefen' }, async ($, e) => {
    const i = e as unknown as { datei: string; skala?: string }
    const r = await skript($, 'midi_pruefen.py', i.skala ? [i.datei, i.skala] : [i.datei], 120_000)
    return { result: JSON.stringify(letztesJson(r), null, 1) }
  })

  on('tool.call', { tool: 'mcp__audio-labor__lua_pruefen' }, async ($, e) => {
    const i = e as unknown as { datei: string }
    try {
      const r = await $.process.run(['node', `${$.plugin.root}/tools/lua_pruefen.cjs`, i.datei], { timeoutMs: 60_000 })
      return { result: r.exitCode === 0 ? r.stdout.trim() : `Fehler: ${(r.stderr || r.stdout).slice(0, 400)}` }
    } catch (err) {
      return { result: `node nicht verfügbar – Lua-Prüfung nicht möglich (${String(err).slice(0, 120)}).` }
    }
  })

  // Vor dem Versand an den Nutzer: Audiodateien wirklich messen; bei Problemen einmal anhalten.
  on('tool.call', { tool: 'SendUserFile' }, async ($, e, next) => {
    const files = ((e as unknown as { files?: string[] }).files ?? []).filter(f => AUDIO.test(f) && !gewarnt.has(f))
    const funde: string[] = []
    for (const f of files.slice(0, 8)) {
      const m = await messen($, f, false)
      if (m.fehler) continue
      const probleme = bewerte(m, undefined).filter(x => !x.startsWith('Lautheit im Ziel'))
      if (probleme.length) {
        gewarnt.add(f)
        funde.push(`${f} (${m.lufs_integriert} LUFS, TP ${m.true_peak_dbtp} dBTP): ${probleme.join(' ')}`)
      }
    }
    if (funde.length === 0) return next(e)
    return { deny: `audio-labor hat vor dem Versand gemessen und Probleme gefunden:\n${funde.map(f => `- ${f}`).join('\n')}\nBehebe sie und sende die neue Datei – oder sende dieselbe Datei erneut und nenne dem Nutzer die Abweichung ausdrücklich.` }
  }).catch(($, e, next) => next(e))

  on('tool.call', { tool: 'mcp__audio-labor__messen' }, async ($, e) => {
    const i = e as unknown as { datei: string; ziel?: string; spektrum?: boolean }
    const m = await messen($, i.datei, i.spektrum === true)
    const notes = bewerte(m, i.ziel)
    return { result: `${JSON.stringify(m, null, 1)}\n\nBewertung:\n${notes.length ? notes.map(n => `- ${n}`).join('\n') : '- keine Auffälligkeiten'}` }
  })

  on('tool.call', { tool: 'mcp__audio-labor__vergleichen' }, async ($, e) => {
    const i = e as unknown as { vorher: string; nachher: string; ziel?: string }
    const [a, b] = [await messen($, i.vorher, false), await messen($, i.nachher, false)]
    const keys = ['lufs_integriert', 'true_peak_dbtp', 'lra_lu', 'rms_dbfs', 'crest_db', 'stereo_korrelation', 'geclippte_samples'] as const
    const rows = keys.map(k => {
      const x = a[k], y = b[k]
      const d = typeof x === 'number' && typeof y === 'number' ? ` (Δ ${(y - x >= 0 ? '+' : '')}${(y - x).toFixed(2)})` : ''
      return `${k}: ${x ?? '–'} → ${y ?? '–'}${d}`
    })
    const sa = (a.spektrale_anteile_prozent ?? {}) as Record<string, number>
    const sb = (b.spektrale_anteile_prozent ?? {}) as Record<string, number>
    const spec = Object.keys(sa).map(k => `${k}: ${sa[k]}% → ${sb[k] ?? '–'}%`)
    const notes = bewerte(b, i.ziel)
    return { result: `Vorher: ${i.vorher}\nNachher: ${i.nachher}\n${rows.join('\n')}\nFrequenzanteile: ${spec.join(', ')}\n\nBewertung nachher:\n${notes.map(n => `- ${n}`).join('\n') || '- keine Auffälligkeiten'}` }
  })
}
