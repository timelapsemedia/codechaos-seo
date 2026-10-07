import type { ProcessRunResult } from 'claude-code'

// Windows (Git Bash) kennt oft nur „python“ oder „py -3“; UTF-8 erzwingen, sonst zerbrechen Umlaute/Emojis.
export const PY_KANDIDATEN: string[][] = [['python3'], ['python'], ['py', '-3']]
export const PY_ENV = { PYTHONIOENCODING: 'utf-8', PYTHONUTF8: '1' }

export function istPython3(r: ProcessRunResult): boolean {
  return r.exitCode === 0 && /Python 3/.test(r.stdout + r.stderr)
}

export function letztesJson<T extends object = Record<string, unknown>>(r: ProcessRunResult): T & { fehler?: string } {
  try {
    return JSON.parse(r.stdout.trim().split('\n').pop() ?? '{}') as T & { fehler?: string }
  } catch {
    return { fehler: (r.stderr || r.stdout).slice(-500) || `Exit ${r.exitCode}` } as T & { fehler?: string }
  }
}
