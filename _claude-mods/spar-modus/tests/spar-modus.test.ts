import { expect, mock, test } from 'claude-code/testing'

import { acceptHaiku, counterText, HAIKU, isLight, priceOf } from '../hooks/register'

const U = (i: number, o: number, cw = 0, cr = 0, model = HAIKU) => ({ input_tokens: i, output_tokens: o, cache_creation_input_tokens: cw, cache_read_input_tokens: cr, model })
const res = (answer: string, tools: string[], stop: 'tool_use' | 'end_turn', usage: any) =>
  ({ turnId: 't', index: 0, answer, toolUses: tools.map(name => ({ name, input: {} })), stopReason: stop, usage }) as any

test('Im Zweifel groß: nur nach reinen Lese-Schritten und kleinem Kontext', async () => {
  expect(isLight(undefined)).toBe(false)
  expect(isLight({ tools: [], allReadOnly: true, context: 1000 })).toBe(false)
  expect(isLight({ tools: ['Edit'], allReadOnly: false, context: 1000 })).toBe(false)
  expect(isLight({ tools: ['Read'], allReadOnly: true, context: 190_000 })).toBe(false)
  expect(isLight({ tools: ['Read'], allReadOnly: true, context: 20_000 })).toBe(true)
})

test('Haiku-Antwort nur übernehmen, wenn sie selbst nur weiterliest', async () => {
  expect(acceptHaiku(res('', ['Grep'], 'tool_use', U(1, 1)))).toBe(true)
  expect(acceptHaiku(res('Hier ist die Lösung', [], 'end_turn', U(1, 1)))).toBe(false)
  expect(acceptHaiku(res('', ['Edit'], 'tool_use', U(1, 1)))).toBe(false)
  expect(acceptHaiku(res('Plan: erst A dann B', ['Read'], 'tool_use', U(1, 1)))).toBe(false)
  expect(acceptHaiku(res('', ['Bash'], 'tool_use', U(1, 1)))).toBe(false)
})

test('Kosten: Listenpreise inkl. Cache-Schreiben/-Lesen; unbekanntes Modell = null', async () => {
  expect(priceOf(HAIKU, U(1_000_000, 0))).toBe(1)
  expect(priceOf(HAIKU, U(0, 0, 1_000_000, 1_000_000))).toBe(1.35)
  expect(priceOf('claude-opus-5-5', U(0, 1_000_000))).toBe(20)
  expect(priceOf('irgendwas', U(1, 1))).toBeNull()
  expect(counterText({ enabled: true, haikuSteps: 0, retried: 0, kept: { input: 0, output: 0, cacheWrite: 0, cacheRead: 0 }, wasted: { input: 0, output: 0, cacheWrite: 0, cacheRead: 0 }, keptUsd: 0, wastedUsd: 0 })).toContain('Ersparnis unbekannt')
})

async function drain(stream: any) {
  let r
  while (!(r = await stream.next()).done) {}
  return r.value
}

test('Standardmäßig aus; an: Lese-Auswertung an Haiku, Finale beim großen Modell mit sichtbaren Mehrkosten', async ($, on) => {
  mock.store(on)
  const calls: string[] = []
  const script: Record<string, any> = {
    'big:0': res('', ['Read'], 'tool_use', U(100, 50, 0, 5000, 'claude-opus-5-5')),
    'haiku:1': res('', ['Grep'], 'tool_use', U(3000, 40, 0, 0)),
    'haiku:2': res('Fertig: so geht es.', [], 'end_turn', U(3500, 200, 0, 0)),
    'big:2': res('Fertig: so geht es.', [], 'end_turn', U(10, 300, 200, 6000, 'claude-opus-5-5')),
    'big:1': res('', ['Grep'], 'tool_use', U(10, 30, 0, 5000, 'claude-opus-5-5')),
  }
  on('session.start', (_$: unknown, e: { cwd: string }) => ({ cwd: e.cwd }) as never)
  on('command.register', () => ({ value: undefined }) as never)
  on('ui.invalidate', () => ({ value: undefined }) as never)
  on('tool.call', () => ({ result: { ok: true }, text: 'ok', isReadOnly: true }) as never)
  on('turn.step', async function* (_$: unknown, e: any) {
    const who = e.model === HAIKU ? 'haiku' : 'big'
    calls.push(`${who}:${e.index}`)
    yield { kind: 'text', index: 0, text: 'x' } as any
    return { ...script[`${who}:${e.index}`], index: e.index, turnId: e.turnId }
  })
  await $.session.start({ cwd: '/p' } as never)

  // aus: alles beim großen Modell
  await drain($.turn.step({ turnId: 't0', index: 0, model: 'claude-opus-5-5', messageCount: 1 }))
  await $.tool.call({ tool: 'Read', file_path: '/p/a' } as never)
  await drain($.turn.step({ turnId: 't0', index: 1, model: 'claude-opus-5-5', messageCount: 3 }))
  expect(calls).toEqual(['big:0', 'big:1'])

  const on1 = await $.command.run({ command: 'sparmodus', args: '' } as never)
  expect(on1.text).toContain('AN')
  calls.length = 0
  await drain($.turn.step({ turnId: 't1', index: 0, model: 'claude-opus-5-5', messageCount: 1 }))
  await $.tool.call({ tool: 'Read', file_path: '/p/a' } as never)
  const s1 = await drain($.turn.step({ turnId: 't1', index: 1, model: 'claude-opus-5-5', messageCount: 3 }))
  expect(s1.usage.model).toBe(HAIKU)
  await $.tool.call({ tool: 'Grep', pattern: 'x' } as never)
  const s2 = await drain($.turn.step({ turnId: 't1', index: 2, model: 'claude-opus-5-5', messageCount: 5 }))
  expect(s2.usage.model).toBe('claude-opus-5-5')
  expect(calls).toEqual(['big:0', 'haiku:1', 'haiku:2', 'big:2'])

  const report = await $.command.run({ command: 'sparmodus', args: '' } as never)
  expect(report.text).toContain('1× Haiku')
  expect(report.text).toContain('Mehrkosten 1× wiederholt')
  expect(report.text).toContain('Ersparnis unbekannt')
  expect(report.text).toContain('keine Messung deines Abo-Limits')
})
