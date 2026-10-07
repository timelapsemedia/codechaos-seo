import type { Register } from 'claude-code'

// Import-Name → pip-Paket, wo sie sich unterscheiden (die häufigen Stolpersteine).
export const PIP: Record<string, string> = {
  cv2: 'opencv-python', PIL: 'pillow', yaml: 'pyyaml', sklearn: 'scikit-learn', bs4: 'beautifulsoup4', fitz: 'pymupdf',
  google: 'google-auth google-api-python-client', googleapiclient: 'google-api-python-client', dotenv: 'python-dotenv',
  docx: 'python-docx', pptx: 'python-pptx', soundfile: 'soundfile', pyloudnorm: 'pyloudnorm', audioread: 'audioread',
  faster_whisper: 'faster-whisper', whisper: 'openai-whisper', mido: 'mido', magic: 'python-magic', serial: 'pyserial',
  Crypto: 'pycryptodome', jwt: 'pyjwt', telegram: 'python-telegram-bot', pypdfium2: 'pypdfium2', moviepy: 'moviepy',
}

const RUFT_PYTHON = /(^|[;&|(]\s*|\s)(python3?|py)(\.exe)?\s/

/** Befehl für Windows anpassen: python3 → python (falls python3 fehlt), UTF-8 erzwingen. */
export function anpassen(cmd: string, hatPython3: boolean): string {
  let c = cmd
  if (!hatPython3) c = c.replace(/(^|[;&|(]\s*|\s)python3(\.exe)?(?=\s)/g, '$1python')
  if (RUFT_PYTHON.test(c + ' ') && !/PYTHONIOENCODING=/.test(c)) c = `export PYTHONIOENCODING=utf-8 PYTHONUTF8=1; ${c}`
  return c
}

/** Hinweise aus der Ausgabe eines Befehls. */
export function hinweise(cmd: string, ausgabe: string, windows: boolean): string[] {
  const out: string[] = []
  for (const m of ausgabe.matchAll(/ModuleNotFoundError: No module named '([\w.]+)'/g)) {
    const top = m[1]!.split('.')[0]!
    out.push(`Python-Modul „${m[1]}“ fehlt: ${windows ? 'python' : 'python3'} -m pip install ${PIP[top] ?? top}`)
  }
  if (/UnicodeEncodeError: 'charmap'|UnicodeDecodeError: 'charmap'/.test(ausgabe)) out.push('Windows-Zeichensatzfehler: PYTHONIOENCODING=utf-8 und PYTHONUTF8=1 setzen, Dateien mit encoding="utf-8" öffnen.')
  if (/Python wurde nicht gefunden|Python was not found/.test(ausgabe)) out.push('Unter Windows heißt der Befehl meist „python“ oder „py -3“, nicht „python3“ (App-Ausführungsalias ggf. deaktivieren).')
  if (windows && /\bcurl\b[^\n]*\s(-d|--data(-raw|-urlencode)?|-F)\s/.test(cmd) && /[^\x00-\x7F]/.test(cmd)) {
    out.push('curl unter Windows kann Umlaute/Emojis in Formularfeldern zerstören: Text aus einer UTF-8-Datei senden (--data-urlencode "caption@datei.txt") oder Python (urllib/requests) verwenden.')
  }
  return [...new Set(out)]
}

let hatPython3: boolean | undefined

export const register: Register = on => {
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const windows = (await $.env.get('OS')) === 'Windows_NT'
    let command = e.command
    if (windows) {
      if (hatPython3 === undefined) {
        hatPython3 = await $.process.run(['python3', '--version'], { timeoutMs: 15_000 }).then(r => r.exitCode === 0 && /Python 3/.test(r.stdout + r.stderr), () => false)
      }
      command = anpassen(command, hatPython3)
    }
    const r = await next(command === e.command ? e : { ...e, command })
    if (r.deny !== undefined) return r
    const h = hinweise(command, r.text ?? '', windows)
    return h.length ? { ...r, context: [...(r.context ?? []), `windows-helfer: ${h.join(' ')}`] } : r
  })

  on('prompt.compose', async ($, e, next) => {
    const r = await next(e)
    if ((await $.env.get('OS')) !== 'Windows_NT') return r
    const text = 'Umgebung: Windows mit Git Bash (windows-helfer). Pfade mit Leerzeichen immer in Anführungszeichen; Python als „python“ (nicht python3) mit UTF-8; Dateien immer mit encoding="utf-8" lesen/schreiben; für HTTP-Anfragen mit Umlauten/Emojis Python statt curl; keine sleep-Warteschleifen, sondern Hintergrundaufgaben/Statusabfragen.'
    return { sections: [...r.sections, { id: 'windows-helfer:umgebung', text, scope: 'session' as const }] }
  })
}
