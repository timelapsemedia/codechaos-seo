import { expect, test } from 'claude-code/testing'

test('Werkzeuge rufen das Prüfskript mit den richtigen Argumenten auf', async ($, on) => {
  on('session.start', (_$: unknown, e: { cwd: string }) => ({ cwd: e.cwd }) as never)
  on('tool.register', () => ({ value: { tool: 'x' } }) as never)
  const seen: string[][] = []
  on('process.run', (_$: unknown, e: any) => {
    seen.push(e.argv)
    return { value: { exitCode: 0, stdout: e.argv.includes('--version') ? 'Python 3.12' : JSON.stringify({ status: 200, probleme: ['kein canonical'] }), stderr: '', isStdoutTruncated: false, isStderrTruncated: false } } as never
  })
  await $.session.start({ cwd: '/p' } as never)
  const r = await $.tool.call({ tool: 'mcp__seo-werkstatt__seite_pruefen', ziel: 'https://example.org/' } as never)
  expect(String(r.result)).toContain('kein canonical')
  await $.tool.call({ tool: 'mcp__seo-werkstatt__sitemap_pruefen', url: 'https://example.org/sitemap.xml', max_urls: 99999 } as never)
  const calls = seen.filter(a => !a.includes('--version'))
  expect(calls[0]?.slice(2)).toEqual(['seite', 'https://example.org/'])
  expect(calls[1]?.slice(2)).toEqual(['sitemap', 'https://example.org/sitemap.xml', '2000'])
})

test('Kaputte Skriptausgabe wird als Fehler gemeldet, nicht erfunden', async ($, on) => {
  on('session.start', (_$: unknown, e: { cwd: string }) => ({ cwd: e.cwd }) as never)
  on('tool.register', () => ({ value: { tool: 'x' } }) as never)
  on('process.run', () => ({ value: { exitCode: 1, stdout: '', stderr: 'Traceback …', isStdoutTruncated: false, isStderrTruncated: false } }) as never)
  await $.session.start({ cwd: '/p' } as never)
  const r = await $.tool.call({ tool: 'mcp__seo-werkstatt__seite_pruefen', ziel: 'x.html' } as never)
  expect(String(r.result)).toContain('Fehler (Exit 1)')
})
