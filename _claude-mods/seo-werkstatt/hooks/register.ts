import type { EngineInterface, ProcessRunResult, Register } from 'claude-code'

import { istPython3, PY_ENV, PY_KANDIDATEN } from './py'

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

async function pruefen($: EngineInterface, args: string[]): Promise<string> {
  const r = await skript($, 'seo_pruefen.py', args)
  const line = r.stdout.trim().split('\n').pop() ?? ''
  try {
    return JSON.stringify(JSON.parse(line), null, 1)
  } catch {
    return `Fehler (Exit ${r.exitCode}): ${(r.stderr || r.stdout).slice(0, 500)}`
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.tool.register({
      name: 'seite_pruefen',
      description: 'Prüft eine Webseite (URL) oder lokale HTML-Datei auf SEO-Grundlagen und meldet echte Werte: HTTP-Status, Weiterleitungskette, Antwortzeit, X-Robots-Tag, Title/Description inkl. Länge, robots-Meta, canonical, lang, hreflang, Open Graph, Twitter Card, h1/h2, Bilder ohne alt, Links intern/gesamt, Wortzahl, JSON-LD-Typen und Parse-Fehler, plus Problemliste. Vor und nach jeder SEO-Änderung nutzen.',
      inputSchema: { type: 'object', properties: { ziel: { type: 'string', description: 'https://… oder Pfad zu einer .html-Datei' } }, required: ['ziel'] },
    })
    await $.tool.register({
      name: 'sitemap_pruefen',
      description: 'Lädt eine sitemap.xml (inkl. Sitemap-Index) und prüft jede URL per HEAD auf HTTP-Status; listet alles, was nicht 200 ist (Weiterleitungen, 404, Fehler).',
      inputSchema: { type: 'object', properties: { url: { type: 'string' }, max_urls: { type: 'number' } }, required: ['url'] },
    })
    await $.tool.register({
      name: 'site_pruefen',
      description: 'Prüft einen lokalen Website-Ordner (GitHub Pages, statisch) vor dem Push: kaputte lokale Links/Bilder/Skripte, Verweise mit falscher Groß-/Kleinschreibung oder falscher Endung (.jpg statt .jpeg), unausgeglichene <div>, doppelte Titel, Bilder ohne alt, einseitige hreflang-Verweise zwischen Sprachversionen.',
      inputSchema: { type: 'object', properties: { ordner: { type: 'string' } }, required: ['ordner'] },
    })
    return next(e)
  })

  on('tool.call', { tool: 'mcp__seo-werkstatt__site_pruefen' }, async ($, e) => {
    const i = e as unknown as { ordner: string }
    return { result: await pruefen($, ['site', i.ordner]) }
  })

  on('tool.call', { tool: 'mcp__seo-werkstatt__seite_pruefen' }, async ($, e) => {
    const i = e as unknown as { ziel: string }
    return { result: await pruefen($, ['seite', i.ziel]) }
  })

  on('tool.call', { tool: 'mcp__seo-werkstatt__sitemap_pruefen' }, async ($, e) => {
    const i = e as unknown as { url: string; max_urls?: number }
    return { result: await pruefen($, ['sitemap', i.url, String(Math.min(Math.max(1, i.max_urls ?? 200), 2000))]) }
  })
}
