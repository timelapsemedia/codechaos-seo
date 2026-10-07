import { expect, test } from 'claude-code/testing'

import { bewerte } from '../hooks/register'

const ok = (stdout: string) => ({ value: { exitCode: 0, stdout, stderr: '', isStdoutTruncated: false, isStderrTruncated: false } }) as never

function boot(on: any, messung: object, seen: string[][] = []) {
  on('session.start', (_$: unknown, e: { cwd: string }) => ({ cwd: e.cwd }) as never)
  on('tool.register', () => ({ value: { tool: 'x' } }) as never)
  on('process.run', (_$: unknown, e: any) => {
    seen.push(e.argv)
    if (e.argv.includes('--version')) return e.argv[0] === 'python3' ? { value: { exitCode: 127, stdout: '', stderr: 'nicht gefunden', isStdoutTruncated: false, isStderrTruncated: false } } : ok('Python 3.12.1')
    return ok(JSON.stringify(messung))
  })
  on('tool.call', () => ({ result: 'gesendet' }) as never)
  return seen
}

test('Bewertung nur aus Messwerten, mit Zielprofil', async () => {
  const laut = bewerte({ lufs_integriert: -5.2, true_peak_dbtp: 0.4, geclippte_samples: 120, crest_db: 5.1 }, 'streaming')
  expect(laut.join(' ')).toContain('Lauter als Ziel')
  expect(laut.join(' ')).toContain('True Peak 0.4')
  expect(laut.join(' ')).toContain('120 Samples')
  expect(bewerte({ lufs_integriert: -6.5, true_peak_dbtp: -0.5 }, 'hitech').join(' ')).toContain('im Ziel')
  expect(bewerte({ lufs_integriert: -11, true_peak_dbtp: -1.2 }, 'streaming_laut').join(' ')).toContain('im Ziel')
  expect(bewerte({ letzte_10ms_peak_dbfs: -21 }, undefined).join(' ')).toContain('Klick-Gefahr')
  expect(bewerte({ fehler: 'kaputt' }, 'metal')).toEqual(['Fehler: kaputt'])
  expect(bewerte({}, undefined)).toEqual([])
})

test('Windows: findet „python“ statt „python3“ und misst über das Skript', async ($, on) => {
  const seen = boot(on, { lufs_integriert: -14.2, true_peak_dbtp: -1.3, geclippte_samples: 0 })
  await $.session.start({ cwd: '/p' } as never)
  const r = await $.tool.call({ tool: 'mcp__audio-labor__messen', datei: 'C:\\master\\song.wav', ziel: 'streaming' } as never)
  expect(String(r.result)).toContain('im Ziel')
  const call = seen.find(a => a.some(x => x.endsWith('audio_analyse.py')))!
  expect(call[0]).toBe('python')
})

test('Vor dem Versand: Problem-Datei einmal angehalten, zweiter Versand geht durch', async ($, on) => {
  boot(on, { lufs_integriert: -8, true_peak_dbtp: 0.3, geclippte_samples: 0, letzte_10ms_peak_dbfs: -18 })
  await $.session.start({ cwd: '/p' } as never)
  const send = { tool: 'SendUserFile', files: ['/p/master.wav', '/p/cover.png'], status: 'normal' } as never
  const r1 = await $.tool.call(send)
  expect(r1.deny).toContain('True Peak 0.3')
  expect(r1.deny).toContain('Klick-Gefahr')
  const r2 = await $.tool.call(send)
  expect(r2.deny).toBeUndefined()
})
