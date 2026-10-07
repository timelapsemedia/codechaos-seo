import { atom, read, update } from 'claude-code'
import type { ModelUsage, Register, TurnStepChunk, TurnStepResult } from 'claude-code'

import type { SparStats, Tokens } from '../types'

export const HAIKU = 'claude-haiku-4-5'
/** Haiku 4.5 hat 200K Kontext; mit Reserve nur darunter umleiten. */
const MAX_CONTEXT_FOR_HAIKU = 150_000
/** Werkzeuge, die nur lesen. Ein Haiku-Schritt, der etwas anderes will, wird verworfen. */
const READ_TOOLS = new Set(['Read', 'Grep', 'Glob', 'LS', 'WebFetch', 'WebSearch', 'ToolSearch'])

/** USD je 1 Mio. Tokens, Listenpreise (Stand der claude-api-Referenz 2026-09-25). Cache-Schreiben = 1,25 × Eingabe (5-Min-Cache). */
const PRICES: Record<string, { in: number; out: number; cr: number }> = {
  'claude-haiku-4-5': { in: 1, out: 5, cr: 0.1 },
  'claude-sonnet-5-5': { in: 2, out: 10, cr: 0.2 },
  'claude-opus-5-5': { in: 4, out: 20, cr: 0.2 },
  'claude-fable-5-1': { in: 10, out: 50, cr: 0.25 },
}

const ZERO: Tokens = { input: 0, output: 0, cacheWrite: 0, cacheRead: 0 }
const INITIAL: SparStats = { enabled: false, haikuSteps: 0, retried: 0, kept: ZERO, wasted: ZERO, keptUsd: 0, wastedUsd: 0 }
const stats = atom({ plugin: 'spar-modus', key: 'stats' } as const, INITIAL)

export function priceOf(model: string, u: ModelUsage): number | null {
  const key = Object.keys(PRICES).find(k => model.startsWith(k))
  const p = key ? PRICES[key] : undefined
  if (!p) return null
  return (u.input_tokens * p.in + u.output_tokens * p.out + u.cache_creation_input_tokens * p.in * 1.25 + u.cache_read_input_tokens * p.cr) / 1e6
}

const add = (t: Tokens, u: ModelUsage): Tokens => ({
  input: t.input + u.input_tokens,
  output: t.output + u.output_tokens,
  cacheWrite: t.cacheWrite + u.cache_creation_input_tokens,
  cacheRead: t.cacheRead + u.cache_read_input_tokens,
})
const sum = (t: Tokens) => t.input + t.output + t.cacheWrite + t.cacheRead
const addUsd = (a: number | null, b: number | null) => (a === null || b === null ? null : a + b)

/** Leicht nur, wenn der vorige Schritt ausschließlich gelesen hat und der Kontext in Haiku passt. Im Zweifel: groß. */
export function isLight(prev: { tools: string[]; allReadOnly: boolean; context: number } | undefined): boolean {
  if (!prev || prev.tools.length === 0) return false
  if (!prev.allReadOnly) return false
  if (prev.context <= 0 || prev.context > MAX_CONTEXT_FOR_HAIKU) return false
  return true
}

/** Haiku-Ergebnis übernehmen nur, wenn es selbst nur weiterliest – kein Plan-Text, kein Code, keine finale Antwort. */
export function acceptHaiku(r: TurnStepResult): boolean {
  return r.stopReason === 'tool_use' && r.answer.trim() === '' && r.toolUses.length > 0 && r.toolUses.every(t => READ_TOOLS.has(t.name))
}

export function counterText(s: SparStats): string {
  const k = (n: number) => (n >= 1000 ? `${(n / 1000).toFixed(1)}k` : `${n}`)
  const usd = (n: number | null) => (n === null ? 'Preis unbekannt' : `≈$${n.toFixed(4)}`)
  const extra = s.retried ? ` · Mehrkosten ${s.retried}× wiederholt: ${k(sum(s.wasted))} Tok ${usd(s.wastedUsd)}` : ''
  return `Spar-Modus (Experiment): ${s.haikuSteps}× Haiku · ${k(sum(s.kept))} Tok ${usd(s.keptUsd)}${extra} · Ersparnis unbekannt`
}

// Was der vorige Hauptschritt dieses Turns getan hat (pro Reload neu).
let prev: { turnId: string; tools: string[]; allReadOnly: boolean; context: number } | undefined
// Lese-Status der Tool-Aufrufe seit dem letzten Hauptschritt (isReadOnly setzt die Engine).
let sinceStep: boolean[] = []

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'sparmodus', description: 'Spar-Modus (Experiment) an/aus und Zahlen anzeigen' })
    const enabled = (await $.store.get('enabled')) === true
    await update($, stats, s => ({ ...s, enabled }))
    return next(e)
  })

  on('tool.call', async ($, e, next) => {
    const r = await next(e)
    if (!e.agentId) sinceStep.push(r.deny === undefined && (r.isReadOnly === true || READ_TOOLS.has(String(e.tool))))
    return r
  })

  on('turn.step', async function* ($, e, next) {
    const s = await read($, stats)
    const before = prev && prev.turnId === e.turnId ? prev : undefined
    let result: TurnStepResult

    // Die Tool-Aufrufe seit dem vorigen Schritt entscheiden, ob er nur gelesen hat.
    if (before && !e.agentId) before.allReadOnly = sinceStep.length > 0 && sinceStep.every(Boolean)
    if (!e.agentId) sinceStep = []

    if (!s.enabled || e.agentId || !isLight(before)) {
      result = yield* next(e)
    } else {
      // Leichter Schritt: Haiku zuerst, Antwort zurückhalten, bis klar ist, ob sie passt.
      const held: TurnStepChunk[] = []
      const stream = next({ ...e, model: HAIKU, effort: undefined })
      let r: IteratorResult<TurnStepChunk, TurnStepResult>
      while (!(r = await stream.next()).done) held.push(r.value)
      const haiku = r.value
      if (haiku.usage && acceptHaiku(haiku)) {
        for (const c of held) yield c
        const u = haiku.usage
        await update($, stats, x => ({ ...x, haikuSteps: x.haikuSteps + 1, kept: add(x.kept, u), keptUsd: addUsd(x.keptUsd, priceOf(u.model, u)) }))
        result = haiku
      } else {
        // Verworfen: beim großen Modell wiederholen; Haikus Verbrauch zählt als Mehrkosten.
        const u = haiku.usage
        if (u) await update($, stats, x => ({ ...x, retried: x.retried + 1, wasted: add(x.wasted, u), wastedUsd: addUsd(x.wastedUsd, priceOf(u.model, u)) }))
        result = yield* next(e)
      }
      $.ui.invalidate('ui.render')
    }

    if (!e.agentId) {
      const u = result.usage
      prev = {
        turnId: e.turnId,
        tools: result.toolUses.map(t => t.name),
        allReadOnly: false,
        context: u ? u.input_tokens + u.cache_creation_input_tokens + u.cache_read_input_tokens + u.output_tokens : 0,
      }
    }
    return result
  })

  on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
    const s = await read($, stats)
    if (!s.enabled) return next(e)
    return next({ ...e, props: { ...e.props, suffix: `${e.props.suffix ?? ''} · ${counterText(s)}` } })
  })

  on('command.run', { command: 'sparmodus' }, async $ => {
    const isOn = !(await read($, stats)).enabled
    await $.store.set('enabled', isOn)
    const s = await update($, stats, x => ({ ...x, enabled: isOn }))
    return {
      text: [
        `Spar-Modus (Experiment) ist jetzt ${isOn ? 'AN' : 'AUS'}.`,
        counterText(s),
        'Gemessen: Tokens aus der API-Usage. Kosten: Schätzung zu API-Listenpreisen inkl. Cache-Schreiben (1,25×), Cache-Lesen und wiederholter Anfragen – keine Messung deines Abo-Limits.',
        'Ersparnis unbekannt: Was das große Modell für dieselben Schritte gekostet hätte, wird nicht gemessen. Achtung: Haiku liest den Gesprächsverlauf ohne den warmen Cache des großen Modells; Opus-5.5-Cache-Lesen (0,20 $/Mio.) ist billiger als ungecachte Haiku-Eingabe (1 $/Mio.). Es kann also teurer werden.',
      ].join('\n'),
    }
  })
}
