import type { Register } from 'claude-code'

type TextRegel = { name: string; max: number; sichtbar?: number; hashtags?: number }
// Plattform-Grenzen als Richtwerte (Stand 2025/26; Plattformen ändern sie gelegentlich).
export const TEXTE: Record<string, TextRegel> = {
  instagram: { name: 'Instagram-Caption', max: 2200, sichtbar: 125, hashtags: 30 },
  tiktok: { name: 'TikTok-Beschreibung', max: 4000, hashtags: 100 },
  youtube_titel: { name: 'YouTube-Titel', max: 100, sichtbar: 70 },
  youtube_beschreibung: { name: 'YouTube-Beschreibung', max: 5000, sichtbar: 150 },
  x: { name: 'X/Twitter-Post', max: 280 },
  pinterest: { name: 'Pinterest-Beschreibung', max: 500 },
  etsy_titel: { name: 'Etsy-Titel', max: 140 },
  facebook: { name: 'Facebook-Post', max: 63206, sichtbar: 125 },
}

type BildRegel = { name: string; ratios: [number, number][]; minKante: number; maxMb: number }
export const BILDER: Record<string, BildRegel> = {
  feed: { name: 'Instagram Feed/Karussell', ratios: [[4, 5], [1, 1], [191, 100]], minKante: 1080, maxMb: 30 },
  story: { name: 'Story/Reel-Cover/TikTok', ratios: [[9, 16]], minKante: 1080, maxMb: 30 },
  etsy: { name: 'Etsy-Listing-Foto', ratios: [[4, 3], [5, 4], [1, 1]], minKante: 2000, maxMb: 20 },
  youtube_thumb: { name: 'YouTube-Thumbnail', ratios: [[16, 9]], minKante: 720, maxMb: 2 },
}

// Formulierungen, die als Heil- oder Wirkversprechen gelten können (Plattformregeln, Heilmittelwerbegesetz).
const HEIL = /\b(heilt|heilend|heilung|wirkt\s+gegen|hilft\s+(bei|gegen)|lindert|therapie|therapeutisch|behandl\w*|medizin\w*|gegen\s+(krebs|depression|angst|schmerz\w*|entzündung\w*)|entgiftet|detox|stärkt\s+das\s+immunsystem|psychoaktiv|high\s+werden|berauschend)\b/i

const KI_HINWEIS = /(\bKI\b|\bAI\b|künstliche[rn]? intelligenz|mit KI|ki-generiert|ai-generated|#ki\b|#ai\b|#aiart|#kiart)/i

export function textPruefen(text: string, plattform: string, kiInhalt = false, wunschHashtags?: number): string[] {
  const r = TEXTE[plattform]
  const out: string[] = []
  if (!r) return [`Unbekannte Plattform ${plattform}`]
  const len = [...text].length
  out.push(`${r.name}: ${len}/${r.max} Zeichen`)
  if (len > r.max) out.push(`ZU LANG um ${len - r.max} Zeichen`)
  if (r.sichtbar && len > r.sichtbar) out.push(`Nur die ersten ca. ${r.sichtbar} Zeichen sind ohne „mehr“ sichtbar: „${[...text].slice(0, r.sichtbar).join('')}…“`)
  const tags = text.match(/(^|\s)#[\p{L}\p{N}_]+/gu) ?? []
  if (r.hashtags !== undefined) out.push(`${tags.length} Hashtags${tags.length > r.hashtags ? ` – mehr als erlaubt (${r.hashtags})` : ''}`)
  if (wunschHashtags !== undefined && tags.length !== wunschHashtags) out.push(`Vorgabe des Nutzers: ${wunschHashtags} Hashtags (jetzt ${tags.length}).`)
  if (kiInhalt && !KI_HINWEIS.test(text)) out.push('KI-Inhalt ohne KI-Hinweis im Text – Hinweis ergänzen (z. B. „mit KI erstellt“) und auf der Plattform das KI-Label setzen.')
  const doppelt = tags.map(t => t.trim().toLowerCase()).filter((t, i, a) => a.indexOf(t) !== i)
  if (doppelt.length) out.push(`Doppelte Hashtags: ${[...new Set(doppelt)].join(' ')}`)
  const heil = text.match(new RegExp(HEIL.source, 'gi'))
  if (heil) out.push(`Mögliche Heil-/Wirkversprechen: ${[...new Set(heil.map(h => h.toLowerCase()))].join(', ')} – riskant für Plattformregeln und Heilmittelwerbegesetz.`)
  return out
}

export function tagsPruefen(tags: string[]): string[] {
  const out = [`${tags.length}/13 Tags`]
  if (tags.length > 13) out.push('mehr als 13 Tags')
  for (const t of tags) if ([...t].length > 20) out.push(`Tag zu lang (${[...t].length}/20): ${t}`)
  const d = tags.map(t => t.toLowerCase()).filter((t, i, a) => a.indexOf(t) !== i)
  if (d.length) out.push(`doppelt: ${[...new Set(d)].join(', ')}`)
  return out
}

export type Bild = { datei: string; breite: number; hoehe: number; mb: number; format: string; farbraum: string }

export function bilderPruefen(bilder: Bild[], plattform: string): string[] {
  const r = BILDER[plattform]
  if (!r) return [`Unbekannte Plattform ${plattform}`]
  const out: string[] = []
  const ratio = (b: Bild) => b.breite / b.hoehe
  for (const b of bilder) {
    const passt = r.ratios.some(([w, h]) => Math.abs(ratio(b) - w / h) < 0.02)
    const p: string[] = []
    if (!passt) p.push(`Seitenverhältnis ${(ratio(b)).toFixed(3)} passt nicht (${r.ratios.map(x => x.join(':')).join(', ')})`)
    if (Math.min(b.breite, b.hoehe) < r.minKante && Math.max(b.breite, b.hoehe) < r.minKante) p.push(`zu klein (${b.breite}×${b.hoehe}, Richtwert ≥ ${r.minKante} px)`)
    if (b.mb > r.maxMb) p.push(`${b.mb} MB > ${r.maxMb} MB`)
    if (/cmyk/i.test(b.farbraum)) p.push('CMYK – für Web in sRGB umwandeln')
    out.push(`${b.datei}: ${b.breite}×${b.hoehe}, ${b.format}, ${b.mb} MB${p.length ? ' – ' + p.join('; ') : ' – ok'}`)
  }
  if (plattform === 'feed' && bilder.length > 1) {
    const rs = new Set(bilder.map(b => ratio(b).toFixed(2)))
    if (rs.size > 1) out.push('Karussell: Bilder haben unterschiedliche Seitenverhältnisse – Instagram schneidet alle auf das Format des ersten zu.')
    if (bilder.length > 20) out.push('Karussell: mehr als 20 Bilder')
  }
  return out
}

export function leseStream(json: string): { width?: number; height?: number; codec_name?: string; pix_fmt?: string } {
  try {
    return ((JSON.parse(json) as { streams?: Record<string, unknown>[] }).streams?.[0] ?? {}) as { width?: number; height?: number; codec_name?: string; pix_fmt?: string }
  } catch {
    return {}
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.tool.register({
      name: 'text_pruefen',
      description: `Prüft einen Post-/Caption-/Titeltext gegen Plattformgrenzen (${Object.keys(TEXTE).join(', ')}): Zeichen, sichtbarer Anfang vor „mehr“, Hashtags (Anzahl, doppelte) und mögliche Heil-/Wirkversprechen. Optional Etsy-Tags (13 × max. 20 Zeichen). Vor jedem Posting nutzen.`,
      inputSchema: { type: 'object', properties: { text: { type: 'string' }, plattform: { type: 'string', enum: Object.keys(TEXTE) }, ki_inhalt: { type: 'boolean', description: 'Bild/Video mit KI erstellt (z. B. Higgsfield)' }, hashtags_soll: { type: 'number', description: 'gewünschte Hashtag-Anzahl, Standard des Nutzers: 5' }, etsy_tags: { type: 'array', items: { type: 'string' } } }, required: ['text', 'plattform'] },
    })
    await $.tool.register({
      name: 'bilder_pruefen',
      description: `Misst Bilder wirklich (ImageMagick identify) und prüft sie gegen ${Object.keys(BILDER).join(', ')}: Seitenverhältnis, Mindestgröße, Dateigröße, Farbraum, Karussell-Einheitlichkeit.`,
      inputSchema: { type: 'object', properties: { dateien: { type: 'array', items: { type: 'string' } }, plattform: { type: 'string', enum: Object.keys(BILDER) } }, required: ['dateien', 'plattform'] },
    })
    return next(e)
  })

  on('tool.call', { tool: 'mcp__social-studio__text_pruefen' }, async ($, e) => {
    const i = e as unknown as { text: string; plattform: string; ki_inhalt?: boolean; hashtags_soll?: number; etsy_tags?: string[] }
    const out = textPruefen(i.text, i.plattform, i.ki_inhalt === true, i.hashtags_soll ?? (i.plattform === 'instagram' || i.plattform === 'tiktok' ? 5 : undefined))
    if (i.etsy_tags) out.push(...tagsPruefen(i.etsy_tags))
    return { result: out.map(l => `- ${l}`).join('\n') }
  })

  on('tool.call', { tool: 'mcp__social-studio__bilder_pruefen' }, async ($, e) => {
    const i = e as unknown as { dateien: string[]; plattform: string }
    const bilder: Bild[] = []
    const fehler: string[] = []
    for (const datei of i.dateien.slice(0, 40)) {
      // ffprobe gibt es überall, wo ffmpeg installiert ist (auch Windows); ImageMagick nur für den Farbraum, falls vorhanden.
      // JSON statt CSV: ffprobe ordnet die Felder selbst (nicht in der angefragten Reihenfolge).
      const r = await $.process.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,codec_name,pix_fmt', '-of', 'json', datei], { timeoutMs: 60_000 }).catch(() => undefined)
      const st = leseStream(r?.stdout ?? '')
      const [w, h, codec, pix] = [st.width, st.height, st.codec_name, st.pix_fmt]
      if (!r || r.exitCode !== 0 || !w || !h) { fehler.push(`${datei}: nicht lesbar${r ? ` (${r.stderr.slice(0, 120)})` : ' (ffprobe fehlt)'}`); continue }
      const groesse = await $.fs.stat(datei).then(s => s.size).catch(() => 0)
      const cs = await $.process.run(['identify', '-format', '%[colorspace]', datei], { timeoutMs: 30_000 }).then(x => (x.exitCode === 0 ? x.stdout.trim() : ''), () => '')
      bilder.push({ datei, breite: Number(w), hoehe: Number(h), mb: Math.round(groesse / 1e4) / 100, format: codec ?? '?', farbraum: cs || (pix?.includes('cmyk') ? 'CMYK' : pix ?? '?') })
    }
    return { result: [...bilderPruefen(bilder, i.plattform), ...fehler].map(l => `- ${l}`).join('\n') }
  })
}
