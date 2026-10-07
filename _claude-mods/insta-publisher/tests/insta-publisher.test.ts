import { expect, mock, test } from 'claude-code/testing'

import { ohneGeheimnis } from '../hooks/register'

const run = (stdout: string) => ({ value: { exitCode: 0, stdout, stderr: '', isStdoutTruncated: false, isStderrTruncated: false } }) as never

test('Geheimnisse werden aus Ausgaben entfernt', async () => {
  expect(ohneGeheimnis('Fehler mit EAAgeheimertoken123 drin', ['EAAgeheimertoken123'])).toBe('Fehler mit *** drin')
})

test('Token aus Umgebungsvariable, nie im Ergebnis; Posten nur mit Bestätigung', async ($, on) => {
  mock.store(on)
  const envs: Record<string, string>[] = []
  on('session.start', (_$: unknown, e: { cwd: string }) => ({ cwd: e.cwd }) as never)
  on('tool.register', () => ({ value: { tool: 'x' } }) as never)
  mock.env(on, { IG_TOKEN: 'EAAgeheimertoken123' })
  on('process.run', (_$: unknown, e: any) => {
    if (e.argv.includes('--version')) return run('Python 3.12')
    envs.push(e.init?.env ?? {})
    return run(JSON.stringify(e.argv.includes('posten') ? { veroeffentlicht: true, permalink: 'https://instagram.com/p/x', echo: 'EAAgeheimertoken123' } : { konto: { username: 'druwids' } }))
  })
  await $.session.start({ cwd: '/p' } as never)
  const s = await $.tool.call({ tool: 'mcp__insta-publisher__ig_zugang_speichern', token_env: 'IG_TOKEN', ig_user_id: '17841' } as never)
  expect(String(s.result)).toContain('aus Umgebungsvariable IG_TOKEN')
  const st = await $.tool.call({ tool: 'mcp__insta-publisher__ig_status' } as never)
  expect(String(st.result)).toContain('druwids')
  expect(envs[0]?.IG_TOKEN).toBe('EAAgeheimertoken123')
  expect(envs[0]?.PYTHONIOENCODING).toBe('utf-8')
  const vorschau = await $.tool.call({ tool: 'mcp__insta-publisher__ig_posten', typ: 'bild', medien: ['https://x/a.jpg'], caption: 'Räucherwerk 🌿' } as never)
  expect(String(vorschau.result)).toContain('VORSCHAU – nichts veröffentlicht')
  expect(envs).toHaveLength(1)
  const post = await $.tool.call({ tool: 'mcp__insta-publisher__ig_posten', typ: 'bild', medien: ['https://x/a.jpg'], caption: 'Räucherwerk 🌿', bestaetigt: true } as never)
  expect(String(post.result)).toContain('instagram.com/p/x')
  expect(String(post.result)).not.toContain('EAAgeheimertoken123')
})
