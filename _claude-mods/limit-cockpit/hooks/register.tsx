import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register, RenderSurface, SessionRateLimit, SessionContextUsage, TurnUsage } from 'claude-code'

import type { Gauge, Drivers } from '../types'

const gauge = atom({ plugin: 'limit-cockpit', key: 'gauge' } as const, {})
const drivers = atom({ plugin: 'limit-cockpit', key: 'drivers' } as const, null)
const busy = atom({ plugin: 'limit-cockpit', key: 'busy' } as const, null)

const FALLBACK = 'Übergabe kopiert. Neuen Chat öffnen und Cmd+V beziehungsweise Strg+V drücken.'
const WEEK_WARN = 75

const HANDOFF_PROMPT = `Schreibe eine kompakte Übergabe dieser Session für einen neuen Chat, auf Deutsch, höchstens 250 Wörter, als Markdown mit genau diesen Überschriften:
## Ziel
## Aktueller Stand
## Nächste Schritte
## Wichtige Dateien
Nur Fakten aus dieser Session; was unsicher ist, als unsicher markieren. Keine Geheimnisse, Tokens, Passwörter oder personenbezogenen Daten. Beginne direkt mit "## Ziel".`

type Step = { index: number; usage: TurnUsage | null; tools: string[] }
type ToolOut = { label: string; chars: number }

// Werte nur für den laufenden Turn; ein Reload setzt sie zurück (gewollt).
let steps: Step[] = []
let toolOuts: ToolOut[] = []

const k = (n: number) => (n >= 1000 ? `${(n / 1000).toFixed(n >= 100000 ? 0 : 1)}k` : `${n}`)

function fromUsage(rateLimits: readonly SessionRateLimit[], context: SessionContextUsage): Gauge {
  const five = rateLimits.find(r => r.kind === 'five_hour')
  const week = rateLimits.find(r => r.kind === 'seven_day')
  return {
    fivePct: five?.percentUsed,
    fiveResetsAt: five?.resetsAt,
    weekPct: week?.percentUsed,
    weekResetsAt: week?.resetsAt,
    ctxPct: context.percent,
    ctxTokens: context.tokens,
    ctxWindow: context.window,
  }
}

function until(iso: string | undefined, now: number): string {
  if (!iso) return 'Reset unbekannt'
  const t = Date.parse(iso)
  if (Number.isNaN(t)) return 'Reset unbekannt'
  const min = Math.max(0, Math.round((t - now) / 60000))
  const d = new Date(t)
  const hh = String(d.getHours()).padStart(2, '0')
  const mm = String(d.getMinutes()).padStart(2, '0')
  return `Reset ${hh}:${mm} (in ${min >= 60 ? `${Math.floor(min / 60)} h ${min % 60} min` : `${min} min`})`
}

/** Die Leiste als Text, für Band, Befehl und Tests gleich. */
export function bandText(g: Gauge, now: number): { line: string; warn?: string } {
  const five = g.fivePct === undefined
    ? '5h-Limit: keine Messung (nur mit Abo, nach der ersten Antwort)'
    : `5h-Limit ${g.fivePct} % · ${until(g.fiveResetsAt, now)}`
  const ctx = g.ctxPct === undefined
    ? 'Kontext: noch keine Messung'
    : `Kontext ${g.ctxPct} %${g.ctxTokens !== undefined && g.ctxWindow ? ` (${k(g.ctxTokens)}/${k(g.ctxWindow)})` : ''}`
  const warn = g.weekPct !== undefined && g.weekPct >= WEEK_WARN
    ? `⚠ Wochenlimit ${g.weekPct} % verbraucht · ${until(g.weekResetsAt, now)}`
    : undefined
  return { line: `${five} · ${ctx}`, warn }
}

/** Top 3 je Art. Gemessen = API-Usage je Anfrage, geschätzt = Tool-Ausgaben Zeichen/4. */
export function rankDrivers(list: Step[], outs: ToolOut[]): Drivers {
  const fresh = (u: TurnUsage) => u.input_tokens + u.cache_creation_input_tokens + u.output_tokens
  const measured = list
    .filter((s): s is Step & { usage: TurnUsage } => s.usage !== null)
    .sort((a, b) => fresh(b.usage) - fresh(a.usage))
    .slice(0, 3)
    .map(s => {
      const u = s.usage
      const what = s.tools.length ? ` → ${s.tools.slice(0, 2).join(', ')}${s.tools.length > 2 ? ' …' : ''}` : ' → Antworttext'
      return `Anfrage ${s.index + 1}: ${k(fresh(u))} neu (Eingabe ${k(u.input_tokens)}, Cache-Schreiben ${k(u.cache_creation_input_tokens)}, Ausgabe ${k(u.output_tokens)}) + ${k(u.cache_read_input_tokens)} Cache-Lesen${what}`
    })
  const estimated = [...outs]
    .sort((a, b) => b.chars - a.chars)
    .slice(0, 3)
    .filter(o => o.chars > 0)
    .map(o => `${o.label} ≈ ${k(Math.round(o.chars / 4))} Tokens (geschätzt aus ${k(o.chars)} Zeichen)`)
  return { measured, estimated }
}

function toolLabel(e: { tool: string } & Record<string, unknown>): string {
  const pick = (v: unknown) => (typeof v === 'string' ? v : '')
  const arg = pick(e.file_path) || pick(e.path) || pick(e.pattern) || pick(e.command) || pick(e.url) || pick(e.query)
  const short = arg.length > 48 ? `…${arg.slice(-47)}` : arg
  return short ? `${e.tool} ${short}` : e.tool
}

async function handoff($: EngineInterface, surface: RenderSurface | undefined): Promise<string> {
  await update($, busy, () => 'Übergabe wird geschrieben …')
  try {
    const r = await $.model.fork({ prompt: HANDOFF_PROMPT })
    if (!r.isAnswered) {
      return r.reason === 'nothing-to-fork'
        ? 'Noch nichts zu übergeben: diese Session hat noch keine Antwort.'
        : `Übergabe konnte nicht geschrieben werden (${r.reason}).`
    }
    const text = r.text.trim()
    const copied = await $.ui.copy(surface ? { text, surface } : { text })
    if (!copied.isCopied) {
      return `Zwischenablage nicht verfügbar (${copied.reason}). Hier die Übergabe zum manuellen Kopieren:\n\n${text}`
    }
    // Neuer Chat: /clear beginnt ein neues Gespräch (das alte bleibt über /resume erreichbar).
    // Der Text wird nach dem Clear ins leere Eingabefeld gelegt (classic.SessionStart unten).
    const canClear = (await $.command.list()).some(c => c.name === 'clear')
    if (!canClear) return FALLBACK
    try {
      await $.store.set('pendingHandoff', text)
      void $.command.run({ command: 'clear' }).catch(async () => {
        await $.store.delete('pendingHandoff')
        $.ui.toast(FALLBACK)
      })
      return 'Übergabe kopiert. Neuer Chat startet, die Übergabe steht danach im Eingabefeld.'
    } catch {
      await $.store.delete('pendingHandoff')
      return FALLBACK
    }
  } finally {
    await update($, busy, () => null)
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'handoff', description: 'Kompakte Übergabe schreiben, kopieren und neuen Chat starten' })
    await $.command.register({ name: 'cockpit', description: 'Limit-Cockpit als Text anzeigen (auch wo keine Leiste gezeichnet wird)' })
    const u = await $.session.usage()
    await update($, gauge, () => fromUsage(u.rateLimits, u.context))
    return next(e)
  })

  // Nach /clear: wartende Übergabe ins Eingabefeld legen.
  on('classic.SessionStart', async ($, e, next) => {
    const r = await next(e)
    if (e.source === 'clear') {
      const pending = await $.store.get('pendingHandoff')
      if (typeof pending === 'string' && pending) {
        await $.store.delete('pendingHandoff')
        const filled = await $.prompt.fill({ text: pending })
        if (!filled.isFilled) $.ui.toast(FALLBACK)
      }
    }
    return r
  })

  on('session.measure', async ($, e, next) => {
    await update($, gauge, () => fromUsage(e.rateLimits, e.context))
    return next(e)
  })

  on('turn.start', ($, e, next) => {
    steps = []
    toolOuts = []
    return next(e)
  })

  on('turn.step', async function* ($, e, next) {
    const r = yield* next(e)
    if (!e.agentId) steps.push({ index: e.index, usage: r.usage, tools: r.toolUses.map(t => t.name) })
    return r
  })

  on('tool.call', async ($, e, next) => {
    const r = await next(e)
    if (r.deny === undefined && typeof r.text === 'string' && !e.tool.startsWith('mcp__limit-cockpit')) {
      toolOuts.push({ label: toolLabel(e as never), chars: r.text.length })
    }
    return r
  })

  on('turn.complete', async ($, e, next) => {
    const r = await next(e)
    if (e.agentId || e.reason !== 'answer') return r
    const d = rankDrivers(steps, toolOuts)
    await update($, drivers, () => d)
    if (d.measured.length || d.estimated.length) {
      const m = d.measured.length ? `gemessen: ${d.measured.join(' | ')}` : 'gemessen: keine Usage gemeldet'
      const s = d.estimated.length ? ` · geschätzt: ${d.estimated.join(' | ')}` : ''
      $.ui.log(`Token-Treiber · ${m}${s}`)
    }
    return r
  })

  on('command.run', { command: 'handoff' }, async ($, e) => ({ text: await handoff($, undefined) }))

  on('command.run', { command: 'cockpit' }, async $ => {
    const u = await $.session.usage()
    const b = bandText(fromUsage(u.rateLimits, u.context), await $.clock.now())
    const d = await read($, drivers)
    const lines = [b.line, b.warn ?? '']
    if (d) lines.push('Letzte Antwort – gemessen:', ...d.measured.map(x => `  ${x}`), 'geschätzt (Tool-Ausgaben):', ...d.estimated.map(x => `  ${x}`))
    lines.push('Hinweis: API-Usage misst Tokens; dein Abo-Limit zeigen nur die Prozentwerte des 5h-/Wochenfensters.')
    return { text: lines.filter(Boolean).join('\n') }
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey) return next(e)
    const { Box, Text, Button } = $.ui.resolve(e)
    const g = await read($, gauge)
    const working = await read($, busy)
    const b = bandText(g, await $.clock.now())
    return (
      <Box flexDirection="column">
        <Box>
          <Text dimColor>{b.line} </Text>
          <Button
            key="handoff"
            label={working ?? 'Neuer Chat mit Übergabe'}
            onPress={async press => {
              const msg = await handoff($, press.surface)
              $.ui.toast(msg.length > 300 ? `${msg.slice(0, 300)} …` : msg)
            }}
          />
        </Box>
        {b.warn ? <Text color="yellow">{b.warn}</Text> : null}
      </Box>
    )
  })
}
