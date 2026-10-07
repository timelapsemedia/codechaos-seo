import { expect, test } from 'claude-code/testing'

import { pruefePlattform, pruefeUntertitel } from '../hooks/register'

test('Plattform-Check aus Messwerten', async () => {
  const quer = pruefePlattform({ breite: 1920, hoehe: 1080, seitenverhaeltnis: '16:9', dauer_s: 30, fps: 25, audio_lufs: -14 }, 'reels')
  expect(quer.join(' ')).toContain('passt nicht zu Instagram Reels')
  const ok = pruefePlattform({ breite: 1080, hoehe: 1920, seitenverhaeltnis: '9:16', dauer_s: 30, fps: 30, audio_lufs: -14, audio_true_peak_dbtp: -1.5, schwarzbilder: [] }, 'reels')
  expect(ok).toEqual([])
  expect(pruefePlattform({ breite: 1080, hoehe: 1920, schwarzbilder: [{ von_s: 0, bis_s: 1 }], audio: 'keine Tonspur' }, 'tiktok').join(' ')).toMatch(/Schwarzbild.*Keine Tonspur/)
})

test('Untertitel inkl. Videolänge', async () => {
  const srt = '1\n00:00:01,000 --> 00:00:03,000\nHallo\n\n2\n00:00:09,000 --> 00:00:11,000\nzu spät\n'
  const r = pruefeUntertitel(srt, 10)
  expect(r.cues).toBe(2)
  expect(r.probleme.join(' ')).toContain('nach Videoende')
  expect(pruefeUntertitel('1\n00:00:01,000 --> 00:00:03,000\nok\n').probleme).toEqual([])
})

test('Werkzeug ruft das Analyse-Skript auf', async ($, on) => {
  on('session.start', (_$: unknown, e: { cwd: string }) => ({ cwd: e.cwd }) as never)
  on('tool.register', () => ({ value: { tool: 'x' } }) as never)
  on('process.run', () => ({ value: { exitCode: 0, stdout: 'Python 3.12\n' + JSON.stringify({ breite: 1920, hoehe: 1080, seitenverhaeltnis: '16:9', dauer_s: 20 }), stderr: '', isStdoutTruncated: false, isStderrTruncated: false } }) as never)
  await $.session.start({ cwd: '/p' } as never)
  const r = await $.tool.call({ tool: 'mcp__video-werkstatt__analysieren', datei: '/p/a.mp4', plattform: 'shorts' } as never)
  expect(String(r.result)).toContain('passt nicht zu YouTube Shorts')
})

test('Vor dem Versand: Hochkant-Video mit Schwarzbild und kaputte SRT werden einmal angehalten', async ($, on) => {
  on('session.start', (_$: unknown, e: { cwd: string }) => ({ cwd: e.cwd }) as never)
  on('tool.register', () => ({ value: { tool: 'x' } }) as never)
  on('process.run', () => ({ value: { exitCode: 0, stdout: 'Python 3.12\n' + JSON.stringify({ breite: 1080, hoehe: 1920, seitenverhaeltnis: '9:16', dauer_s: 20, fps: 30, schwarzbilder: [{ von_s: 0, bis_s: 0.8 }], audio_lufs: -14, audio_true_peak_dbtp: -1.5 }), stderr: '', isStdoutTruncated: false, isStderrTruncated: false } }) as never)
  on('fs.read', () => ({ value: '1\n00:00:02,000 --> 00:00:01,000\nfalsch\n' }) as never)
  on('tool.call', () => ({ result: 'gesendet' }) as never)
  await $.session.start({ cwd: '/p' } as never)
  const send = { tool: 'SendUserFile', files: ['/p/short.mp4', '/p/short.srt'], status: 'normal' } as never
  const r1 = await $.tool.call(send)
  expect(r1.deny).toContain('Schwarzbild am Anfang')
  expect(r1.deny).toContain('Ende vor Anfang')
  expect((await $.tool.call(send)).deny).toBeUndefined()
})
