import { expect, test } from 'claude-code/testing'

import { bilderPruefen, tagsPruefen, textPruefen } from '../hooks/register'

test('Texte: Grenzen, sichtbarer Anfang, Hashtags, Heilversprechen', async () => {
  const lang = 'x'.repeat(2300)
  expect(textPruefen(lang, 'instagram').join(' ')).toContain('ZU LANG um 100')
  const t = textPruefen('Fliegenpilz-Räucherwerk – hilft gegen Stress #räuchern #ritual #räuchern', 'instagram').join(' ')
  expect(t).toContain('3 Hashtags')
  expect(t).toContain('Doppelte Hashtags: #räuchern')
  expect(t).toContain('hilft gegen')
  expect(textPruefen('Neues Video', 'youtube_titel').join(' ')).toContain('11/100')
  expect(tagsPruefen(['räucherwerk', 'a'.repeat(21), 'räucherwerk']).join(' ')).toMatch(/zu lang.*doppelt/)
})

test('Bilder: Formate und Karussell', async () => {
  const b = (d: string, w: number, h: number) => ({ datei: d, breite: w, hoehe: h, mb: 1, format: 'JPEG', farbraum: 'sRGB' })
  expect(bilderPruefen([b('a.jpg', 1080, 1350)], 'feed')[0]).toContain('ok')
  const k = bilderPruefen([b('a.jpg', 1080, 1350), b('b.jpg', 1080, 1080)], 'feed').join(' ')
  expect(k).toContain('unterschiedliche Seitenverhältnisse')
  expect(bilderPruefen([b('c.jpg', 1920, 1080)], 'story')[0]).toContain('passt nicht')
  expect(bilderPruefen([{ ...b('d.jpg', 1080, 1920), farbraum: 'CMYK' }], 'story')[0]).toContain('CMYK')
})

test('Vorgaben des Nutzers: 5 Hashtags und KI-Hinweis', async () => {
  const t = textPruefen('Neues Motiv aus dem Herbstwald #pilze #wald', 'instagram', true, 5).join(' ')
  expect(t).toContain('Vorgabe des Nutzers: 5 Hashtags (jetzt 2)')
  expect(t).toContain('ohne KI-Hinweis')
  expect(textPruefen('Mit KI erstellt #a #b #c #d #e', 'instagram', true, 5).join(' ')).not.toMatch(/Vorgabe|KI-Hinweis/)
})

test('Bilder über ffprobe messen (geht auch ohne ImageMagick)', async ($, on) => {
  on('session.start', (_$: unknown, e: { cwd: string }) => ({ cwd: e.cwd }) as never)
  on('tool.register', () => ({ value: { tool: 'x' } }) as never)
  on('process.run', (_$: unknown, e: any) => (e.argv[0] === 'ffprobe' ? { value: { exitCode: 0, stdout: '{"programs":[],"streams":[{"codec_name":"mjpeg","width":1080,"height":1350,"pix_fmt":"yuvj420p"}]}', stderr: '', isStdoutTruncated: false, isStderrTruncated: false } } : { value: { exitCode: 127, stdout: '', stderr: 'nicht gefunden', isStdoutTruncated: false, isStderrTruncated: false } }) as never)
  on('fs.stat', () => ({ value: { size: 512000 } }) as never)
  await $.session.start({ cwd: '/p' } as never)
  const r = await $.tool.call({ tool: 'mcp__social-studio__bilder_pruefen', dateien: ['C:\\posts\\a.jpg'], plattform: 'feed' } as never)
  expect(String(r.result)).toContain('1080×1350, mjpeg, 0.51 MB – ok')
})
