import { expect, mock, test } from 'claude-code/testing'

import { QUELLEN, schonGesucht } from '../hooks/register'

test('Links und Normalisierung', async () => {
  expect(QUELLEN.kleinanzeigen!.url('Stillste Stund – Demo')).toBe('https://www.kleinanzeigen.de/s-stillste-stund-demo/k0')
  expect(schonGesucht([{ datum: 'd', begriff: 'Janus  Liebeslieder', quelle: 'ebay', ergebnis: 'nichts' }], 'janus liebeslieder', 'ebay')).toHaveLength(1)
})

test('Suchgedächtnis über Aufrufe hinweg, keine doppelten Funde', async ($, on) => {
  mock.store(on)
  mock.clock(on, { now: Date.parse('2026-10-07T10:00:00Z') })
  on('session.start', (_$: unknown, e: { cwd: string }) => ({ cwd: e.cwd }) as never)
  on('tool.register', () => ({ value: { tool: 'x' } }) as never)
  await $.session.start({ cwd: '/p' } as never)
  await $.tool.call({ tool: 'mcp__raritaeten-jaeger__suche_merken', begriff: 'Stillste Stund Demo', quelle: 'kleinanzeigen', ergebnis: '0 Treffer' } as never)
  const l = await $.tool.call({ tool: 'mcp__raritaeten-jaeger__suchlinks', begriff: 'stillste stund demo', quellen: ['kleinanzeigen', 'ebay'] } as never)
  expect(String(l.result)).toContain('schon gesucht am 2026-10-07: 0 Treffer')
  expect(String(l.result)).toContain('nur im Browser')
  const f = { tool: 'mcp__raritaeten-jaeger__fund_merken', titel: 'Demo-Tape 1994', quelle: 'musik_sammler', preis: '25 €', link: 'https://x/1' } as never
  await $.tool.call(f)
  expect(String((await $.tool.call(f)).result)).toContain('schon gespeichert')
  expect(String((await $.tool.call({ tool: 'mcp__raritaeten-jaeger__suchverlauf', filter: 'demo' } as never)).result)).toMatch(/Suchen \(1\)[\s\S]*Funde \(1\)/)
})
