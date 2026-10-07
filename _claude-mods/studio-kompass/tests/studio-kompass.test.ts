import { expect, mock, test } from 'claude-code/testing'

import { checkCaption, checkHtmlSeo, checkSubtitles, findSecrets } from '../hooks/checks'
import { detect } from '../hooks/profiles'

test('Bereiche werden aus Text erkannt', async () => {
  expect(detect('Mach mir einen Hitech Track mit 200 BPM in Ableton')).toContain('musik')
  expect(detect('Master das Black Metal Album auf -14 LUFS')).toContain('mastering')
  expect(detect('Untertitel für das Vimeo Video')).toContain('video')
  expect(detect('Druwids Instagram Post mit Hashtags')).toContain('social')
  expect(detect('GSC Report und Meta Description')).toContain('seo')
  expect(detect('Etsy Listing Titel')).toContain('etsy')
  expect(detect('Hallo')).toEqual([])
})

test('Untertitel-Prüfung', async () => {
  const ok = '1\n00:00:01,000 --> 00:00:03,000\nHallo Welt\n\n2\n00:00:03,500 --> 00:00:05,000\nZweite Zeile\n'
  expect(checkSubtitles(ok)).toEqual([])
  const bad = '1\n00:00:01,000 --> 00:00:04,000\nDiese Zeile ist eindeutig viel zu lang für einen Untertitel hier\n\n2\n00:00:03,000 --> 00:00:03,300\na\nb\nc\n'
  const issues = checkSubtitles(bad)
  expect(issues.join(' ')).toContain('Zeile mit')
  expect(issues.join(' ')).toContain('überlappt')
  expect(issues.join(' ')).toContain('3 Zeilen')
  expect(checkSubtitles('WEBVTT\n\n00:01.000 --> 00:02.000\nok\n')).toEqual([])
})

test('HTML-SEO-Prüfung', async () => {
  const good = '<html><head><title>Hitech Psytrance – Code Chaos</title><meta name="description" content="Kurz und gut."><link rel="canonical" href="https://x"></head><body><h1>A</h1><img src="a" alt="b"></body></html>'
  expect(checkHtmlSeo(good)).toEqual([])
  const bad = `<html><head><title>${'x'.repeat(70)}</title></head><body><h1>a</h1><h1>b</h1><img src="a"></body></html>`
  expect(checkHtmlSeo(bad).join(' ')).toMatch(/70 Zeichen.*Meta-Description.*2 × <h1>.*ohne alt.*canonical/)
  expect(checkHtmlSeo('<div>Fragment</div>')).toEqual([])
})

test('Caption- und Geheimnis-Prüfung', async () => {
  expect(checkCaption('Text ' + Array.from({ length: 31 }, (_, i) => `#tag${i}`).join(' '))[0]).toContain('31 Hashtags')
  expect(checkCaption('kurz #a #b')).toEqual([])
  expect(findSecrets('mein key ist sk-ant-api03-abcdefghijklmnopqrstuvwxyz0123')).toContain('Anthropic-API-Key')
  expect(findSecrets('ghp_' + 'a'.repeat(36))).toContain('GitHub-Token')
  expect(findSecrets('ganz normale Nachricht über Kicks')).toEqual([])
})

function boot(on: any, files: Record<string, string>) {
  mock.store(on)
  on('session.start', (_$: unknown, e: { cwd: string }) => ({ cwd: e.cwd }))
  on('command.register', () => ({ value: undefined }))
  on('env.get', () => ({ value: 'true' }))
  on('session.id', () => ({ value: 's1' }))
  on('session.repo', () => ({ value: null }))
  on('session.root', () => ({ value: '/home/user/codechaos-seo' }))
  on('ui.toast', () => ({ value: undefined }))
  on('fs.read', (_$: unknown, e: any) => ({ value: files[e.path ?? e] ?? '' }))
  on('prompt.submit', (_$: unknown, e: any) => ({ text: e.text, context: e.context }))
  on('prompt.compose', () => ({ sections: [{ id: 'intro', text: 'x', scope: 'shared' }] }))
  on('tool.call', () => ({ result: { ok: true }, text: 'ok' }))
}

test('In einer Cloud-Session: Regeln, Bereich, Prüfhinweis an Claude, Geheimnis-Warnung, /dateien', async ($, on) => {
  boot(on, { '/home/user/codechaos-seo/sub.srt': '1\n00:00:01,000 --> 00:00:00,500\nfalsch\n' })
  await $.session.start({ cwd: '/home/user/codechaos-seo' } as never)
  const sub = await $.prompt.submit({ text: 'Untertitel fürs Video, mein Token ghp_' + 'b'.repeat(36), wait: false, origin: { kind: 'composer' } } as never)
  expect(String(sub.context)).toContain('GitHub-Token')
  expect(String(sub.context)).not.toContain('ghp_')
  const c = await $.prompt.compose({ model: 'm', promptModel: 'm', surfaces: [], tools: [], outputStyle: null, traits: [] } as never)
  const rules = c.sections.find(s => s.id === 'studio-kompass:regeln')?.text ?? ''
  expect(rules).toContain('Cloud-Session')
  expect(rules).toContain('Untertitel')
  expect(rules).toContain('vollem Pfad')
  const r = await $.tool.call({ tool: 'Write', file_path: '/home/user/codechaos-seo/sub.srt', content: 'x' } as never)
  expect(String(r.context)).toContain('Ende vor Anfang')
  const files = await $.command.run({ command: 'dateien', args: '' } as never)
  expect(files.text).toContain('/home/user/codechaos-seo/sub.srt')
})
