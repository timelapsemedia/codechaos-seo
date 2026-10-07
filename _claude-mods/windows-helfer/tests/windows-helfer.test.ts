import { expect, mock, test } from 'claude-code/testing'

import { anpassen, hinweise } from '../hooks/register'

test('python3 → python nur wenn nötig, UTF-8 nur bei Python-Aufrufen', async () => {
  expect(anpassen('python3 audit.py --x', false)).toBe('export PYTHONIOENCODING=utf-8 PYTHONUTF8=1; python audit.py --x')
  expect(anpassen('cd /c/lab && python3 -m pip list', false)).toBe('export PYTHONIOENCODING=utf-8 PYTHONUTF8=1; cd /c/lab && python -m pip list')
  expect(anpassen('python3 a.py', true)).toBe('export PYTHONIOENCODING=utf-8 PYTHONUTF8=1; python3 a.py')
  expect(anpassen('ls -la', false)).toBe('ls -la')
  expect(anpassen('echo python3ist ein wort', false)).toBe('echo python3ist ein wort')
})

test('Hinweise aus Fehlermeldungen', async () => {
  expect(hinweise('python x.py', "ModuleNotFoundError: No module named 'cv2'", true)[0]).toContain('python -m pip install opencv-python')
  expect(hinweise('python x.py', "ModuleNotFoundError: No module named 'google.auth'", false)[0]).toContain('python3 -m pip install google-auth')
  expect(hinweise('curl -X POST -d "caption=Räucherwerk 🌿" https://x', '', true)[0]).toContain('Umlaute/Emojis')
  expect(hinweise('curl -X POST -d "caption=Räucherwerk" https://x', '', false)).toEqual([])
})

test('Auf Windows wird der Bash-Befehl umgeschrieben und der Hinweis an Claude gehängt', async ($, on) => {
  mock.env(on, { OS: 'Windows_NT' })
  const seen: string[] = []
  on('process.run', () => ({ value: { exitCode: 9009, stdout: '', stderr: 'Python wurde nicht gefunden', isStdoutTruncated: false, isStderrTruncated: false } }) as never)
  on('tool.call', (_$: unknown, e: any) => { seen.push(e.command); return { result: { stdout: '' }, text: "Traceback\nModuleNotFoundError: No module named 'soundfile'" } as never })
  const r = await $.tool.call({ tool: 'Bash', command: 'python3 master.py song.wav' } as never)
  expect(seen[0]).toBe('export PYTHONIOENCODING=utf-8 PYTHONUTF8=1; python master.py song.wav')
  expect(String(r.context)).toContain('python -m pip install soundfile')
})

test('Auf Linux/Mac bleibt der Befehl unverändert', async ($, on) => {
  mock.env(on, { OS: '' })
  const seen: string[] = []
  on('tool.call', (_$: unknown, e: any) => { seen.push(e.command); return { result: { stdout: '' }, text: 'ok' } as never })
  await $.tool.call({ tool: 'Bash', command: 'python3 a.py' } as never)
  expect(seen[0]).toBe('python3 a.py')
})
