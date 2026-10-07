import { expect, mock, test } from 'claude-code/testing'

import { bandText, rankDrivers } from '../hooks/register'

const NOW = Date.parse('2026-10-07T10:00:00Z')

// Was in einer Session die Engine beantwortet, hier als Stub
function boot(on: any) {
  on('session.start', (_$: unknown, e: { cwd: string }) => ({ cwd: e.cwd }))
  on('command.register', () => ({ value: undefined }))
  on('session.usage', () => ({ value: { startedAt: NOW, context: { window: 200000 }, rateLimits: [] } }))
}

test('Leiste: ohne Messung keine erfundenen Werte', async () => {
  const b = bandText({}, NOW)
  expect(b.line).toContain('keine Messung')
  expect(b.warn).toBeUndefined()
})

test('Leiste: Wochenwarnung erst ab 75 %', async () => {
  expect(bandText({ fivePct: 42, weekPct: 74.9 }, NOW).warn).toBeUndefined()
  const b = bandText({ fivePct: 42, fiveResetsAt: '2026-10-07T12:10:00Z', weekPct: 75, ctxPct: 37, ctxTokens: 74000, ctxWindow: 200000 }, NOW)
  expect(b.line).toContain('5h-Limit 42 %')
  expect(b.line).toContain('in 2 h 10 min')
  expect(b.line).toContain('Kontext 37 % (74.0k/200k)')
  expect(b.warn).toContain('Wochenlimit 75 %')
})

test('Token-Treiber: gemessen pro Anfrage getrennt von geschätzten Tool-Ausgaben', async () => {
  const u = (i: number, c: number, o: number, r: number) => ({ input_tokens: i, cache_creation_input_tokens: c, output_tokens: o, cache_read_input_tokens: r, model: 'claude-opus-5-5' })
  const d = rankDrivers(
    [
      { index: 0, usage: u(10, 2000, 300, 0), tools: ['Read'] },
      { index: 1, usage: u(5, 40000, 200, 2000), tools: ['Bash'] },
      { index: 2, usage: null, tools: [] },
      { index: 3, usage: u(5, 100, 900, 42000), tools: [] },
      { index: 4, usage: u(1, 1, 1, 1), tools: [] },
    ],
    [
      { label: 'Read src/riesig.ts', chars: 160000 },
      { label: 'Bash npm test', chars: 8000 },
      { label: 'Grep foo', chars: 400 },
      { label: 'Glob *', chars: 10 },
    ],
  )
  expect(d.measured).toHaveLength(3)
  expect(d.measured[0]).toStartWith('Anfrage 2:')
  expect(d.estimated[0]).toBe('Read src/riesig.ts ≈ 40.0k Tokens (geschätzt aus 160k Zeichen)')
  expect(d.estimated).toHaveLength(3)
})

test('Messung aus session.measure landet in der Leiste (Terminal und Desktop)', async ($, on) => {
  mock.clock(on, { now: NOW })
  boot(on)
  on('session.measure', (_$, e) => ({ changed: [...e.changed] }))
  await $.session.start({ cwd: '/tmp/x' } as never)
  await $.session.measure({
    context: { window: 200000, tokens: 50000, percent: 25 },
    rateLimits: [
      { kind: 'five_hour', percentUsed: 61, resetsAt: '2026-10-07T11:30:00Z' },
      { kind: 'seven_day', percentUsed: 80 },
    ],
    changed: ['context', 'rateLimits'],
  })
  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({
      plugin: 'limit-cockpit',
      surface,
      component: 'AbovePrompt',
      props: { hasSurvey: false, isWorking: false, maxRows: 10, bodyColumns: 120, scroll: { bodyRows: 9, offset: 0 } } as never,
    })
    expect((await ui.find({ type: 'Text', text: /5h-Limit 61 %/ }))?.text).toContain('Kontext 25 %')
    expect((await ui.find({ type: 'Text', text: /Wochenlimit 80 %/ }))).toBeDefined()
    expect((await ui.find({ key: 'handoff' }))?.props.label).toBe('Neuer Chat mit Übergabe')
    await ui.unmount()
  }
})

test('/handoff ohne Verlauf erfindet nichts', async ($, on) => {
  on('model.fork', () => ({ value: { isAnswered: false, reason: 'nothing-to-fork' } }) as never)
  boot(on)
  await $.session.start({ cwd: '/tmp/x' } as never)
  const r = await $.command.run({ command: 'handoff', args: '' } as never)
  expect(r.text).toContain('Noch nichts zu übergeben')
})

test('/handoff: Fallback-Hinweis, wenn kein neuer Chat geöffnet werden kann', async ($, on) => {
  on('model.fork', () => ({ value: { isAnswered: true, text: '## Ziel\nX', usage: { input_tokens: 1, output_tokens: 1, cache_read_input_tokens: 0, cache_creation_input_tokens: 0 } } }) as never)
  on('ui.copy', () => ({ value: { isCopied: true } }) as never)
  mock.store(on)
  on('command.list', () => ({ value: [] }) as never)
  boot(on)
  await $.session.start({ cwd: '/tmp/x' } as never)
  const r = await $.command.run({ command: 'handoff', args: '' } as never)
  expect(r.text).toBe('Übergabe kopiert. Neuen Chat öffnen und Cmd+V beziehungsweise Strg+V drücken.')
})
