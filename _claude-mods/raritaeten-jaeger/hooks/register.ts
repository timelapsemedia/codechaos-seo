import type { Register } from 'claude-code'

type Quelle = { name: string; url: (q: string) => string; maschinell: boolean }
const enc = encodeURIComponent
const slug = (q: string) => q.toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')

// „maschinell“ = antwortete am 2026-10-07 auf Server-Abrufe mit 200; sonst Bot-Schutz (403) – Link nur im Browser.
export const QUELLEN: Record<string, Quelle> = {
  discogs: { name: 'Discogs (Datenbank)', url: q => `https://www.discogs.com/search/?q=${enc(q)}&type=all`, maschinell: false },
  discogs_markt: { name: 'Discogs Marktplatz', url: q => `https://www.discogs.com/sell/list?q=${enc(q)}`, maschinell: false },
  ebay: { name: 'eBay.de', url: q => `https://www.ebay.de/sch/i.html?_nkw=${enc(q)}`, maschinell: false },
  kleinanzeigen: { name: 'Kleinanzeigen', url: q => `https://www.kleinanzeigen.de/s-${slug(q)}/k0`, maschinell: true },
  musik_sammler: { name: 'musik-sammler.de', url: q => `https://www.musik-sammler.de/search/${enc(q)}/`, maschinell: true },
  archive: { name: 'archive.org', url: q => `https://archive.org/search?query=${enc(q)}`, maschinell: true },
  bandcamp: { name: 'Bandcamp', url: q => `https://bandcamp.com/search?q=${enc(q)}`, maschinell: true },
  metal_archives: { name: 'Encyclopaedia Metallum', url: q => `https://www.metal-archives.com/search?searchString=${enc(q)}&type=band_name`, maschinell: true },
  cdandlp: { name: 'CDandLP', url: q => `https://www.cdandlp.com/en/search/?q=${enc(q)}`, maschinell: false },
  rym: { name: 'RateYourMusic', url: q => `https://www.rateyourmusic.com/search?searchterm=${enc(q)}&searchtype=a`, maschinell: false },
}

export type Suche = { datum: string; begriff: string; quelle: string; ergebnis: string; link?: string }
export type Fund = { datum: string; titel: string; quelle: string; preis?: string; zustand?: string; link: string; notiz?: string }

export const norm = (s: string) => s.toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, '').replace(/\s+/g, ' ').trim()

export function schonGesucht(verlauf: Suche[], begriff: string, quelle?: string): Suche[] {
  return verlauf.filter(s => norm(s.begriff) === norm(begriff) && (!quelle || s.quelle === quelle))
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.tool.register({
      name: 'suchlinks',
      description: `Erzeugt direkte Suchlinks für einen Begriff auf ${Object.values(QUELLEN).map(q => q.name).join(', ')} und sagt je Quelle, ob sie maschinell abrufbar ist (WebFetch) oder nur im Browser (Bot-Schutz). Zeigt außerdem, was zu diesem Begriff schon gesucht wurde.`,
      inputSchema: { type: 'object', properties: { begriff: { type: 'string' }, quellen: { type: 'array', items: { type: 'string', enum: Object.keys(QUELLEN) } } }, required: ['begriff'] },
    })
    await $.tool.register({
      name: 'suche_merken',
      description: 'Merkt sich eine durchgeführte Suche (Begriff, Quelle, Ergebnis kurz) dauerhaft – auch für spätere Sessions und Routinen, damit nicht doppelt gesucht wird.',
      inputSchema: { type: 'object', properties: { begriff: { type: 'string' }, quelle: { type: 'string' }, ergebnis: { type: 'string' }, link: { type: 'string' } }, required: ['begriff', 'quelle', 'ergebnis'] },
    })
    await $.tool.register({
      name: 'fund_merken',
      description: 'Speichert einen Fund (Titel, Quelle, Preis, Zustand, Link, Notiz) in der dauerhaften Fundliste.',
      inputSchema: { type: 'object', properties: { titel: { type: 'string' }, quelle: { type: 'string' }, preis: { type: 'string' }, zustand: { type: 'string' }, link: { type: 'string' }, notiz: { type: 'string' } }, required: ['titel', 'quelle', 'link'] },
    })
    await $.tool.register({
      name: 'suchverlauf',
      description: 'Zeigt bisherige Suchen und Funde (optional gefiltert nach Begriff).',
      inputSchema: { type: 'object', properties: { filter: { type: 'string' } } },
    })
    return next(e)
  })

  on('tool.call', { tool: 'mcp__raritaeten-jaeger__suchlinks' }, async ($, e) => {
    const i = e as unknown as { begriff: string; quellen?: string[] }
    const verlauf = ((await $.store.get('suchen')) as Suche[] | undefined) ?? []
    const ids = i.quellen?.length ? i.quellen : Object.keys(QUELLEN)
    const zeilen = ids.filter(id => QUELLEN[id]).map(id => {
      const q = QUELLEN[id]!
      const vorher = schonGesucht(verlauf, i.begriff, id).at(-1)
      return `- ${q.name}: ${q.url(i.begriff)} ${q.maschinell ? '(maschinell abrufbar)' : '(nur im Browser – Bot-Schutz)'}${vorher ? ` · schon gesucht am ${vorher.datum}: ${vorher.ergebnis}` : ''}`
    })
    return { result: `Suchlinks für „${i.begriff}“:\n${zeilen.join('\n')}` }
  })

  on('tool.call', { tool: 'mcp__raritaeten-jaeger__suche_merken' }, async ($, e) => {
    const i = e as unknown as Omit<Suche, 'datum'>
    const verlauf = ((await $.store.get('suchen')) as Suche[] | undefined) ?? []
    const datum = new Date(await $.clock.now()).toISOString().slice(0, 10)
    await $.store.set('suchen', [...verlauf, { datum, begriff: i.begriff, quelle: i.quelle, ergebnis: i.ergebnis.slice(0, 300), ...(i.link ? { link: i.link } : {}) }].slice(-2000))
    return { result: `Gemerkt (${verlauf.length + 1} Suchen gespeichert).` }
  })

  on('tool.call', { tool: 'mcp__raritaeten-jaeger__fund_merken' }, async ($, e) => {
    const i = e as unknown as Omit<Fund, 'datum'>
    const funde = ((await $.store.get('funde')) as Fund[] | undefined) ?? []
    if (funde.some(f => f.link === i.link)) return { result: 'Dieser Fund (gleicher Link) ist schon gespeichert.' }
    const datum = new Date(await $.clock.now()).toISOString().slice(0, 10)
    await $.store.set('funde', [...funde, { ...i, datum }].slice(-1000))
    return { result: `Fund gespeichert (${funde.length + 1} insgesamt).` }
  })

  on('tool.call', { tool: 'mcp__raritaeten-jaeger__suchverlauf' }, async ($, e) => {
    const i = e as unknown as { filter?: string }
    const f = i.filter ? norm(i.filter) : ''
    const suchen = (((await $.store.get('suchen')) as Suche[] | undefined) ?? []).filter(s => !f || norm(s.begriff).includes(f))
    const funde = (((await $.store.get('funde')) as Fund[] | undefined) ?? []).filter(x => !f || norm(x.titel).includes(f))
    return {
      result: `Suchen (${suchen.length}):\n${suchen.slice(-60).map(s => `- ${s.datum} · ${s.begriff} · ${s.quelle}: ${s.ergebnis}`).join('\n') || '- keine'}\n\nFunde (${funde.length}):\n${funde.slice(-60).map(x => `- ${x.datum} · ${x.titel} · ${x.quelle}${x.preis ? ` · ${x.preis}` : ''}${x.zustand ? ` · ${x.zustand}` : ''} · ${x.link}`).join('\n') || '- keine'}`,
    }
  })
}
