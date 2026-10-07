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

export type VideoInfo = Record<string, unknown> & {
  breite?: number; hoehe?: number; seitenverhaeltnis?: string; fps?: number; dauer_s?: number
  audio_lufs?: number | null; audio_true_peak_dbtp?: number | null; audio?: string
  schwarzbilder?: { von_s: number; bis_s: number }[]; fehler?: string
}

type Plattform = { name: string; ratio: [number, number]; minBreite: number; maxDauer?: number; hinweis: string }

// Richtwerte der Plattformen (Stand 2025/26 – Grenzen ändern sich, im Zweifel in der Plattform-Hilfe prüfen).
export const PLATTFORMEN: Record<string, Plattform> = {
  reels: { name: 'Instagram Reels', ratio: [9, 16], minBreite: 1080, maxDauer: 180, hinweis: '1080×1920, bis ca. 3 min' },
  tiktok: { name: 'TikTok', ratio: [9, 16], minBreite: 1080, maxDauer: 600, hinweis: '1080×1920, Upload bis 10 min' },
  shorts: { name: 'YouTube Shorts', ratio: [9, 16], minBreite: 1080, maxDauer: 180, hinweis: '9:16 oder 1:1, bis 3 min' },
  youtube: { name: 'YouTube', ratio: [16, 9], minBreite: 1920, hinweis: '16:9, ≥1080p' },
  feed: { name: 'Instagram Feed-Video', ratio: [4, 5], minBreite: 1080, hinweis: '1080×1350 (4:5)' },
  vimeo: { name: 'Vimeo', ratio: [16, 9], minBreite: 1920, hinweis: '16:9, ≥1080p' },
}

export function pruefePlattform(v: VideoInfo, id: string | undefined): string[] {
  const out: string[] = []
  if (v.fehler) return [`Fehler: ${v.fehler}`]
  const p = id ? PLATTFORMEN[id] : undefined
  if (p && v.breite && v.hoehe) {
    const soll = p.ratio[0] / p.ratio[1]
    const ist = v.breite / v.hoehe
    if (Math.abs(ist - soll) > 0.02) out.push(`Seitenverhältnis ${v.seitenverhaeltnis} passt nicht zu ${p.name} (${p.ratio.join(':')}, ${p.hinweis}).`)
    if (Math.min(v.breite, v.hoehe) < Math.min(p.minBreite, 1080)) out.push(`Auflösung ${v.breite}×${v.hoehe} unter ${p.name}-Richtwert (${p.hinweis}).`)
    if (p.maxDauer && typeof v.dauer_s === 'number' && v.dauer_s > p.maxDauer) out.push(`Dauer ${v.dauer_s} s länger als ${p.maxDauer} s (${p.name}).`)
  }
  const erstes = v.schwarzbilder?.[0]
  if (erstes && erstes.von_s < 0.1) out.push(`Schwarzbild am Anfang bis ${erstes.bis_s} s – kostet den Hook in den ersten Sekunden.`)
  if (v.audio === 'keine Tonspur') out.push('Keine Tonspur.')
  if (typeof v.audio_lufs === 'number' && (v.audio_lufs < -20 || v.audio_lufs > -9)) out.push(`Ton ${v.audio_lufs} LUFS – Plattformen normalisieren auf ca. −14 LUFS.`)
  if (typeof v.audio_true_peak_dbtp === 'number' && v.audio_true_peak_dbtp > -1) out.push(`Ton True Peak ${v.audio_true_peak_dbtp} dBTP > −1.`)
  if (typeof v.fps === 'number' && v.fps > 0 && v.fps < 23.9) out.push(`Nur ${v.fps} fps.`)
  return out
}

const ts = (s: string) => {
  const m = s.trim().match(/^(?:(\d+):)?(\d{1,2}):(\d{2})[,.](\d{1,3})$/)
  if (!m) return NaN
  return (Number(m[1] ?? 0) * 3600 + Number(m[2]) * 60 + Number(m[3])) * 1000 + Number((m[4] ?? '0').padEnd(3, '0'))
}

/** Netflix-nahe Richtwerte: ≤2 Zeilen, ≤42 Zeichen/Zeile, 0,83–7 s, ≤20 Zeichen/s, keine Überlappung. */
export function pruefeUntertitel(text: string, videoDauerS?: number): { cues: number; probleme: string[] } {
  const probleme: string[] = []
  const blocks = text.replace(/\r/g, '').replace(/^﻿/, '').replace(/^WEBVTT[^\n]*\n/, '').split(/\n{2,}/).filter(b => b.includes('-->'))
  let lastEnd = -1
  blocks.forEach((b, i) => {
    const lines = b.split('\n')
    const ti = lines.findIndex(l => l.includes('-->'))
    const [a, z] = (lines[ti] ?? '').split('-->')
    const start = ts(a ?? ''), end = ts((z ?? '').trim().split(/\s+/)[0] ?? '')
    const txt = lines.slice(ti + 1).filter(l => l.trim()).map(l => l.replace(/<[^>]+>/g, ''))
    const n = i + 1
    if (Number.isNaN(start) || Number.isNaN(end)) { probleme.push(`Cue ${n}: Zeitstempel unlesbar`); return }
    if (end <= start) probleme.push(`Cue ${n}: Ende vor Anfang`)
    if (start < lastEnd) probleme.push(`Cue ${n}: überlappt`)
    const dur = (end - start) / 1000
    if (dur > 0 && dur < 0.83) probleme.push(`Cue ${n}: nur ${dur.toFixed(2)} s`)
    if (dur > 7) probleme.push(`Cue ${n}: ${dur.toFixed(1)} s`)
    if (txt.length > 2) probleme.push(`Cue ${n}: ${txt.length} Zeilen`)
    const lang = txt.find(l => l.length > 42)
    if (lang) probleme.push(`Cue ${n}: Zeile mit ${lang.length} Zeichen`)
    if (txt.length === 0) probleme.push(`Cue ${n}: leer`)
    const cps = txt.join(' ').length / Math.max(dur, 0.001)
    if (dur > 0 && cps > 20) probleme.push(`Cue ${n}: ${cps.toFixed(0)} Zeichen/s`)
    if (videoDauerS !== undefined && end / 1000 > videoDauerS + 0.05) probleme.push(`Cue ${n}: endet nach Videoende (${(end / 1000).toFixed(2)} s > ${videoDauerS} s)`)
    lastEnd = Math.max(lastEnd, end)
  })
  if (blocks.length === 0) probleme.push('keine Cues gefunden')
  return { cues: blocks.length, probleme }
}

async function analysieren($: EngineInterface, datei: string, bogen: boolean, schnitte: boolean): Promise<VideoInfo> {
  const args = [datei]
  if (bogen) args.push('--bogen', `${datei.replace(/\.[^./\\]+$/, '')}.kontaktbogen.png`)
  if (schnitte) args.push('--schnitte')
  return letztesJson<VideoInfo>(await skript($, 'video_analyse.py', args))
}

const VIDEO = /\.(mp4|mov|m4v|mkv|webm)$/i
const UNTERTITEL = /\.(srt|vtt)$/i
const gewarnt = new Set<string>()
const ohneEndung = (p: string) => p.replace(/\.[^./\\]+$/, '')

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.tool.register({
      name: 'analysieren',
      description: 'Misst ein Video wirklich (ffprobe/ffmpeg): Container, Codec, Breite×Höhe, Seitenverhältnis, fps, Dauer, Bitrate, Ton-LUFS/True Peak, Schwarzbilder; optional Schnitt-Zeitpunkte und ein Kontaktbogen-PNG mit 12 Standbildern (danach mit Read ansehen). Mit plattform prüft es gegen Reels/TikTok/Shorts/YouTube/Feed/Vimeo. Nutze es vor und nach jedem Export.',
      inputSchema: { type: 'object', properties: { datei: { type: 'string' }, plattform: { type: 'string', enum: Object.keys(PLATTFORMEN) }, kontaktbogen: { type: 'boolean' }, schnitte: { type: 'boolean' } }, required: ['datei'] },
    })
    await $.tool.register({
      name: 'untertitel_pruefen',
      description: 'Prüft eine SRT/VTT-Datei: Zeitstempel, Reihenfolge, Überlappung, Standzeit (0,83–7 s), Zeilen (≤2, ≤42 Zeichen), Lesegeschwindigkeit (≤20 Zeichen/s), optional gegen die Videolänge.',
      inputSchema: { type: 'object', properties: { datei: { type: 'string' }, video: { type: 'string' } }, required: ['datei'] },
    })
    await $.tool.register({
      name: 'standbilder',
      description: 'Speichert Standbilder zu bestimmten Zeitpunkten als PNG (danach mit Read ansehen), optional mit roten Hilfslinien für den sicheren Bereich von Reels/TikTok/Shorts (oben 14 %, unten 20 %, Seiten 6 %). Nutze das, um eingebrannte Untertitel, Crop und Text im Bild zu kontrollieren, bevor du ein Video abgibst.',
      inputSchema: { type: 'object', properties: { datei: { type: 'string' }, zeiten: { type: 'array', items: { type: 'number' } }, safe_area_9_16: { type: 'boolean' }, ordner: { type: 'string' } }, required: ['datei', 'zeiten'] },
    })
    await $.tool.register({
      name: 'shorts_untertitel',
      description: 'Erzeugt animationsfreie Hochkant-Untertitel als .ass aus einer SRT oder einem Whisper-JSON mit Wort-Zeitstempeln: kurze Einblendungen (max_zeichen, Standard 15), große Schrift mit Kontur, Position im sicheren Bereich, Schlüsselwörter farbig. Danach mit einbrennen ins Video rendern und mit standbilder kontrollieren.',
      inputSchema: { type: 'object', properties: { quelle: { type: 'string' }, ausgabe: { type: 'string' }, breite: { type: 'number' }, hoehe: { type: 'number' }, max_zeichen: { type: 'number' }, schrift: { type: 'string' }, groesse: { type: 'number' }, keywords: { type: 'array', items: { type: 'string' } }, position: { type: 'string', enum: ['unten', 'mitte'] } }, required: ['quelle'] },
    })
    await $.tool.register({
      name: 'einbrennen',
      description: 'Brennt eine .ass/.srt-Untertiteldatei mit ffmpeg (libass) in ein Video (H.264, CRF 18, Ton kopiert).',
      inputSchema: { type: 'object', properties: { video: { type: 'string' }, untertitel: { type: 'string' }, ausgabe: { type: 'string' } }, required: ['video', 'untertitel'] },
    })
    await $.tool.register({
      name: 'transkribieren',
      description: 'Transkribiert Audio/Video mit Wort-Zeitstempeln (faster-whisper, sonst whisper-CLI) in ein JSON für shorts_untertitel. Meldet ehrlich, wenn kein Whisper installiert ist.',
      inputSchema: { type: 'object', properties: { datei: { type: 'string' }, sprache: { type: 'string' }, modell: { type: 'string' }, ausgabe: { type: 'string' } }, required: ['datei'] },
    })
    return next(e)
  })

  on('tool.call', { tool: 'mcp__video-werkstatt__standbilder' }, async ($, e) => {
    const i = e as unknown as { datei: string; zeiten: number[]; safe_area_9_16?: boolean; ordner?: string }
    const args = [i.datei, i.ordner ?? `${ohneEndung(i.datei)}_standbilder`, i.zeiten.slice(0, 24).join(',')]
    if (i.safe_area_9_16) args.push('9:16')
    return { result: JSON.stringify(letztesJson(await skript($, 'shorts.py', ['standbilder', ...args])), null, 1) }
  })

  on('tool.call', { tool: 'mcp__video-werkstatt__shorts_untertitel' }, async ($, e) => {
    const i = e as unknown as { quelle: string; ausgabe?: string; breite?: number; hoehe?: number; max_zeichen?: number; schrift?: string; groesse?: number; keywords?: string[]; position?: string }
    const args = ['untertitel', i.quelle, i.ausgabe ?? `${ohneEndung(i.quelle)}.shorts.ass`, String(i.breite ?? 1080), String(i.hoehe ?? 1920), String(i.max_zeichen ?? 15), i.schrift ?? 'Montserrat', String(i.groesse ?? Math.round((i.breite ?? 1080) * 0.072)), (i.keywords ?? []).join(','), i.position ?? 'unten']
    return { result: JSON.stringify(letztesJson(await skript($, 'shorts.py', args)), null, 1) }
  })

  on('tool.call', { tool: 'mcp__video-werkstatt__einbrennen' }, async ($, e) => {
    const i = e as unknown as { video: string; untertitel: string; ausgabe?: string }
    const ziel = i.ausgabe ?? `${ohneEndung(i.video)}_untertitel.mp4`
    return { result: JSON.stringify(letztesJson(await skript($, 'shorts.py', ['einbrennen', i.video, i.untertitel, ziel])), null, 1) }
  })

  on('tool.call', { tool: 'mcp__video-werkstatt__transkribieren' }, async ($, e) => {
    const i = e as unknown as { datei: string; sprache?: string; modell?: string; ausgabe?: string }
    const args = ['transkribieren', i.datei, i.sprache ?? 'de', i.modell ?? 'small', i.ausgabe ?? `${ohneEndung(i.datei)}.woerter.json`]
    return { result: JSON.stringify(letztesJson(await skript($, 'shorts.py', args)), null, 1) }
  })

  // Vor dem Versand an den Nutzer: Videos und Untertitel wirklich prüfen; bei Problemen einmal anhalten.
  on('tool.call', { tool: 'SendUserFile' }, async ($, e, next) => {
    const files = ((e as unknown as { files?: string[] }).files ?? []).filter(f => (VIDEO.test(f) || UNTERTITEL.test(f)) && !gewarnt.has(f))
    const funde: string[] = []
    for (const f of files.slice(0, 6)) {
      if (UNTERTITEL.test(f)) {
        const p = pruefeUntertitel(String(await $.fs.read(f))).probleme
        if (p.length) { gewarnt.add(f); funde.push(`${f}: ${p.slice(0, 8).join('; ')}${p.length > 8 ? ` (+${p.length - 8})` : ''}`) }
        continue
      }
      const v = await analysieren($, f, false, false)
      if (v.fehler) continue
      const hoch = v.breite && v.hoehe && v.hoehe > v.breite ? 'reels' : undefined
      const p = pruefePlattform(v, hoch)
      if (p.length) { gewarnt.add(f); funde.push(`${f} (${v.breite}×${v.hoehe}, ${v.dauer_s} s): ${p.join(' ')}`) }
    }
    if (funde.length === 0) return next(e)
    return { deny: `video-werkstatt hat vor dem Versand geprüft und Probleme gefunden:\n${funde.map(f => `- ${f}`).join('\n')}\nBehebe sie und sende neu – oder sende dieselbe Datei erneut und nenne dem Nutzer die Abweichung ausdrücklich.` }
  }).catch(($, e, next) => next(e))

  on('tool.call', { tool: 'mcp__video-werkstatt__analysieren' }, async ($, e) => {
    const i = e as unknown as { datei: string; plattform?: string; kontaktbogen?: boolean; schnitte?: boolean }
    const v = await analysieren($, i.datei, i.kontaktbogen === true, i.schnitte === true)
    const notes = pruefePlattform(v, i.plattform)
    return { result: `${JSON.stringify(v, null, 1)}\n\nPrüfung${i.plattform ? ` (${PLATTFORMEN[i.plattform]?.name})` : ''}:\n${notes.length ? notes.map(n => `- ${n}`).join('\n') : '- keine Auffälligkeiten'}` }
  })

  on('tool.call', { tool: 'mcp__video-werkstatt__untertitel_pruefen' }, async ($, e) => {
    const i = e as unknown as { datei: string; video?: string }
    const text = String(await $.fs.read(i.datei))
    const dauer = i.video ? (await analysieren($, i.video, false, false)).dauer_s : undefined
    const r = pruefeUntertitel(text, typeof dauer === 'number' ? dauer : undefined)
    return { result: `${i.datei}: ${r.cues} Cues${dauer ? `, Video ${dauer} s` : ''}\n${r.probleme.length ? r.probleme.slice(0, 60).map(p => `- ${p}`).join('\n') + (r.probleme.length > 60 ? `\n- … und ${r.probleme.length - 60} weitere` : '') : '- keine Probleme'}` }
  })
}
