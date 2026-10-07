import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Check, PrueferView, Verdict } from '../types'

const verdict = (kind: Verdict['kind'], reason: string, blocks: number): Verdict => ({ kind, reason, blocks })

const PANE = 'pruefer'
const MAX_BLOCKS = 2
const MAX_LEARNINGS = 30
const HEAVY_FILES = 5
const HEAVY_MS = 15 * 60 * 1000

const INITIAL: PrueferView = {
  files: [],
  checks: [],
  verdict: { kind: 'beobachtet', reason: 'Noch keine Abgabe in dieser Session.', blocks: 0 },
  learnings: [],
  enabled: true,
  secondOpinion: true,
}
const view = atom({ plugin: 'pruefer', key: 'view' } as const, INITIAL)

/** Tests, Builds, Typchecks, Linter und echte Aufrufe eines Programms. */
export const CHECK = new RegExp(
  [
    String.raw`\b(npm|pnpm|yarn|bun)\s+(run\s+)?(test|build|lint|typecheck|type-check|check|tsc|e2e)\b`,
    String.raw`\bnpx\s+(--no-install\s+)?(tsc|vitest|jest|eslint|playwright|mocha|ava|prettier --check)\b`,
    String.raw`\b(pytest|mypy|ruff|flake8|pyright|tsc|vitest|jest|shellcheck|htmlhint|xmllint|php -l)\b`,
    String.raw`\bpython3?\s+-m\s+(pytest|unittest|mypy|py_compile|compileall)\b`,
    String.raw`\b(go\s+(test|build|vet)|cargo\s+(test|build|check|clippy)|dotnet\s+(test|build)|mvn\s+\S*(test|verify|package)|gradle\w*\s+\S*(test|build|check))\b`,
    String.raw`\bclaude\s+plugin\s+(test|validate)\b`,
    String.raw`(^|[;&|]\s*)make(\s|$)`,
    String.raw`\b(node|deno|bun|python3?|ruby|php|bash|sh|lua|luajit)\s+(--check\s+|-n\s+)?[\w./-]+\.(m?js|cjs|ts|py|rb|php|sh|lua)\b`,
    String.raw`\bcurl\s+.*\b(localhost|127\.0\.0\.1)\b`,
    String.raw`\bpy\s+(-3\s+)?[\w./\\-]+\.py\b`,
  ].join('|'),
)

export function checkFamily(cmd: string): string {
  const m = cmd.match(CHECK)
  return (m?.[0] ?? cmd).trim().replace(/^[;&|]\s*/, '').split(/\s+/).slice(0, 3).join(' ').replace(/\s+\S*\.(m?js|cjs|ts|py|rb|php|sh|lua)$/, '')
}

/** Ehrliche Angabe, dass nicht getestet wurde: die Antwort geht durch. */
export const HONEST = /nicht\s+(getestet|geprüft|ausgeführt|verifiziert)|ungetestet|ungeprüft|konnte\s+(ich\s+)?(es\s+|das\s+|dies\s+)?nicht\s+(testen|prüfen|ausführen|verifizieren)|not\s+(been\s+)?(tested|verified|run)|untested|could\s*n[o']?t\s+(test|run|verify)/i
/** Erfolgsbehauptung */
export const CLAIM = /funktioniert|läuft\s+(jetzt|wieder)|ist\s+(fertig|behoben|gefixt)|erledigt|getestet|works|fixed|passes|done\b/i

const EDIT_TOOLS = new Set(['Edit', 'Write', 'MultiEdit', 'NotebookEdit'])
/** Mess-/Prüfwerkzeuge der anderen Mods zählen als Beleg. */
export const MESS_TOOL = /^mcp__(audio-labor|video-werkstatt|seo-werkstatt|social-studio)__(messen|vergleichen|midi_pruefen|lua_pruefen|analysieren|standbilder|untertitel_pruefen|seite_pruefen|sitemap_pruefen|site_pruefen|text_pruefen|bilder_pruefen)$/

// Zustand des laufenden Turns; ein Reload beginnt ihn neu.
let seq = 0
let lastEditSeq = -1
let turnStartedAt = 0
let task = ''
let askedUser = false
// Learnings, wie sie beim Sessionstart waren: der System-Prompt bleibt stabil (Prompt-Cache).
let startLearnings: string[] = []

export type Evidence = { files: string[]; checks: Check[]; message: string; lastEditSeq: number }

/** Das Urteil nur aus Belegen. undefined = durchlassen. */
export function judge(ev: Evidence): { block?: string; pass: string } {
  if (ev.files.length === 0) return { pass: 'Keine Dateien geändert – nichts zu belegen.' }
  if (HONEST.test(ev.message)) return { pass: 'Offen als nicht getestet gekennzeichnet – durchgelassen.' }
  const after = ev.checks.filter(c => c.seq > ev.lastEditSeq)
  const names = ev.files.slice(0, 4).join(', ') + (ev.files.length > 4 ? ` und ${ev.files.length - 4} weitere` : '')
  if (after.length === 0) {
    const claim = CLAIM.test(ev.message) ? ' Die Antwort behauptet Erfolg, ohne dass ein Beleg vorliegt.' : ''
    return {
      block: `pruefer: Geändert wurden ${names}, danach lief aber kein Test, Build, Typcheck oder Aufruf.${claim} Prüfe jetzt passend (z. B. Tests, Build, Typcheck oder das Programm einmal ausführen) und gib dann ab. Wenn Prüfen nicht möglich ist, schreibe offen „nicht getestet, weil …“.`,
      pass: '',
    }
  }
  // Jüngster Lauf je Werkzeug zählt (ein späteres grünes „pytest“ ersetzt ein rotes „pytest -k x“).
  const latest = new Map<string, Check>()
  for (const c of after) latest.set(checkFamily(c.cmd), c)
  const red = [...latest.values()].filter(c => !c.ok)
  if (red.length) {
    return {
      block: `pruefer: Nach der letzten Änderung ist noch rot: ${red.map(c => `„${c.cmd.slice(0, 80)}“`).join(', ')}. Behebe das und prüfe erneut – oder schreibe offen, was nicht funktioniert und warum.`,
      pass: '',
    }
  }
  return { pass: `Belegt: ${latest.size} Check(s) nach der letzten Änderung grün.` }
}

async function projectKey($: EngineInterface): Promise<string> {
  const repo = await $.session.repo()
  return `learnings:${repo ? JSON.stringify(repo).slice(0, 200) : await $.session.root()}`
}

async function learn($: EngineInterface, reason: string) {
  const key = await projectKey($)
  const old = (await $.store.get(key)) as string[] | undefined
  const day = new Date(await $.clock.now()).toISOString().slice(0, 10)
  const line = `${day}: ${reason.replace(/^pruefer: /, '').slice(0, 220)}`
  const list = [...(old ?? []), line].slice(-MAX_LEARNINGS)
  await $.store.set(key, list)
  await update($, view, v => ({ ...v, learnings: list }))
}

async function secondOpinion($: EngineInterface, files: string[], checks: Check[]): Promise<string | undefined> {
  const own = await $.session.model()
  const model = /opus|fable/i.test(own) ? 'claude-sonnet-5-5' : 'claude-opus-5-5'
  $.ui.toast(`pruefer: unabhängige Zweitprüfung mit ${model} – verbraucht zusätzliche Tokens (abschalten: /pruefer zweit aus).`, { timeoutMs: 8000 })
  let diff = ''
  try {
    const r = await $.process.run(['git', 'diff', '--stat'])
    diff = r.stdout.slice(0, 4000)
  } catch {
    diff = '(git diff nicht verfügbar)'
  }
  const prompt = `Du prüfst unabhängig, ob eine Abgabe belegt ist. Antworte NUR mit JSON {"ok": true|false, "grund": "<ein Satz>"}.
Aufgabe des Nutzers: ${task.slice(0, 2000)}
Geänderte Dateien: ${files.join(', ')}
git diff --stat: ${diff}
Gelaufene Checks (nach letzter Änderung markiert): ${checks.map(c => `${c.ok ? 'GRÜN' : 'ROT'}${c.afterEdit ? '' : ' (vor Änderung)'}: ${c.cmd.slice(0, 120)}`).join('; ') || 'keine'}
Fehlt ein Beleg dafür, dass die Aufgabe erfüllt ist (z. B. geänderte Bereiche ohne passenden Test)? ok=false nur bei konkretem, benennbarem Fehlen.`
  const r = await $.model.complete({ model, prompt, maxTokens: 300 })
  if (!r.isAnswered) return undefined
  const m = r.text.match(/\{[\s\S]*\}/)
  if (!m) return undefined
  try {
    const j = JSON.parse(m[0]) as { ok?: boolean; grund?: string }
    return j.ok === false && j.grund ? `pruefer (Zweitprüfung ${model}): ${j.grund}` : undefined
  } catch {
    return undefined
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'pruefer', description: 'pruefer an/aus; „/pruefer zweit an|aus“ für die Zweitprüfung; „/pruefer panel“', argumentHint: '[zweit an|aus | panel]' })
    const enabled = (await $.store.get('enabled')) !== false
    const secondOn = (await $.store.get('secondOpinion')) !== false
    const learnings = ((await $.store.get(await projectKey($))) as string[] | undefined) ?? []
    startLearnings = learnings
    await update($, view, v => ({ ...v, enabled, secondOpinion: secondOn, learnings, verdict: enabled ? v.verdict : verdict('aus', 'Mit /pruefer ausgeschaltet.', 0) }))
    if (enabled) void $.ui.open({ id: PANE, title: 'Prüfer' })
    return next(e)
  })

  // Learnings dieses Projekts in jede neue Session mitgeben.
  on('prompt.compose', async ($, e, next) => {
    const r = await next(e)
    const v = await read($, view)
    if (!v.enabled || startLearnings.length === 0) return r
    const text = `Learnings aus früheren Sperren in diesem Projekt (vom Plugin „pruefer“): Belege Änderungen mit Tests/Build/Typcheck, bevor du „fertig“ meldest.\n${startLearnings.slice(-12).map(l => `- ${l}`).join('\n')}`
    return { sections: [...r.sections, { id: 'pruefer:learnings', text, scope: 'session' as const }] }
  })

  on('turn.start', async ($, e, next) => {
    if (e.text) {
      task = e.text
      turnStartedAt = await $.clock.now()
      lastEditSeq = -1
      askedUser = false
      await update($, view, v => ({ ...v, files: [], checks: [], verdict: verdict(v.enabled ? 'beobachtet' : 'aus', v.enabled ? 'Claude arbeitet – ich beobachte nur.' : 'Aus.', 0) }))
    }
    return next(e)
  })

  // Nur beobachten: nie eingreifen, nie verzögern.
  on('tool.call', async ($, e, next) => {
    const r = await next(e)
    if (e.agentId) return r
    seq += 1
    if (EDIT_TOOLS.has(String(e.tool)) && r.deny === undefined && !r.isError) {
      const path = String((e as { file_path?: unknown; notebook_path?: unknown }).file_path ?? (e as { notebook_path?: unknown }).notebook_path ?? '?')
      lastEditSeq = seq
      await update($, view, v => ({ ...v, files: v.files.includes(path) ? v.files : [...v.files, path], checks: v.checks.map(c => ({ ...c, afterEdit: false })) }))
    } else if (e.tool === 'Bash' && r.deny === undefined && !e.run_in_background && CHECK.test(e.command)) {
      const check: Check = { cmd: e.command.trim().split('\n')[0] ?? e.command, ok: r.isError !== true, seq, afterEdit: true }
      await update($, view, v => ({ ...v, checks: [...v.checks, check].slice(-40) }))
    } else if (MESS_TOOL.test(String(e.tool)) && r.deny === undefined) {
      const text = typeof r.text === 'string' ? r.text : String(r.result ?? '')
      const ok = !r.isError && !/"fehler"|^Fehler|FEHLER/.test(text)
      const check: Check = { cmd: String(e.tool).replace(/^mcp__/, '').replace('__', ': '), ok, seq, afterEdit: true }
      await update($, view, v => ({ ...v, checks: [...v.checks, check].slice(-40) }))
    } else if (e.tool === 'AskUserQuestion') {
      askedUser = true
    }
    return r
  })

  // Erst bei der Abgabe urteilen.
  on('classic.Stop', async ($, e, next) => {
    const v = await read($, view)
    const pass = async (reason: string) => {
      await update($, view, x => ({ ...x, verdict: verdict(x.enabled ? 'durchgelassen' : 'aus', reason, x.verdict.blocks) }))
      return next(e)
    }
    if (!v.enabled) return next(e)
    if ((e.background_tasks?.length ?? 0) > 0) return pass('Hintergrundjob läuft – keine Sperre.')
    if ((await $.session.surfaces()).length === 0) return pass('Headless-Lauf – keine Sperre.')
    const msg = e.last_assistant_message ?? ''
    if (askedUser || /\?\s*$/.test(msg.trim())) return pass('Rückfrage an dich – keine Sperre.')
    if (v.verdict.blocks >= MAX_BLOCKS) return pass(`Schon ${MAX_BLOCKS}× angehalten – jetzt durchgelassen, damit nichts hängt.`)

    const j = judge({ files: v.files, checks: v.checks.filter(c => c.afterEdit).map(c => ({ ...c })), message: msg, lastEditSeq })
    let block = j.block
    if (!block && v.secondOpinion && (v.files.length >= HEAVY_FILES || (await $.clock.now()) - turnStartedAt >= HEAVY_MS)) {
      block = await secondOpinion($, v.files, v.checks)
    }
    if (!block) return pass(j.pass || 'Belegt.')
    await update($, view, x => ({ ...x, verdict: verdict('gesperrt', block, x.verdict.blocks + 1) }))
    await learn($, block)
    return { block }
  }).catch(($, e, next) => next(e))

  on('command.run', { command: 'pruefer' }, async ($, e) => {
    const arg = e.args.trim().toLowerCase()
    if (arg.startsWith('zweit')) {
      const isOn = !/aus|off/.test(arg)
      await $.store.set('secondOpinion', isOn)
      await update($, view, v => ({ ...v, secondOpinion: isOn }))
      return { text: `Zweitprüfung ${isOn ? 'an (bei ≥5 Dateien oder ≥15 min; kostet zusätzliche Tokens)' : 'aus'}.` }
    }
    if (arg === 'panel') {
      await $.ui.open({ id: PANE, title: 'Prüfer' })
      return { text: 'Prüfer-Panel geöffnet.' }
    }
    const v = await read($, view)
    const isOn = !v.enabled
    await $.store.set('enabled', isOn)
    await update($, view, x => ({ ...x, enabled: isOn, verdict: verdict(isOn ? 'beobachtet' : 'aus', isOn ? 'Eingeschaltet.' : 'Mit /pruefer ausgeschaltet.', 0) }))
    if (isOn) await $.ui.open({ id: PANE, title: 'Prüfer' })
    else await $.ui.close({ id: PANE })
    return { text: `pruefer ist jetzt ${isOn ? 'AN' : 'AUS'}.` }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const v = await read($, view)
    const color = v.verdict.kind === 'gesperrt' ? 'red' : v.verdict.kind === 'durchgelassen' ? 'green' : undefined
    return (
      <Box flexDirection="column">
        <Text bold>Abgabe: <Text color={color}>{v.verdict.kind}</Text>{v.verdict.blocks ? ` (${v.verdict.blocks}/${MAX_BLOCKS} Sperren)` : ''}</Text>
        <Text dimColor wrap="wrap">{v.verdict.reason}</Text>
        <Text> </Text>
        <Text bold>Geänderte Dateien ({v.files.length})</Text>
        {v.files.length === 0 ? <Text dimColor>keine</Text> : v.files.slice(-12).map(f => <Text wrap="truncate-start">· {f}</Text>)}
        <Text> </Text>
        <Text bold>Checks</Text>
        {v.checks.length === 0 ? <Text dimColor>noch keine</Text> : v.checks.slice(-10).map(c => (
          <Text wrap="truncate-end" dimColor={!c.afterEdit}>
            <Text color={c.ok ? 'green' : 'red'}>{c.ok ? '✓' : '✗'}</Text> {c.cmd}{c.afterEdit ? '' : ' (vor letzter Änderung)'}
          </Text>
        ))}
        <Text> </Text>
        <Text bold>Learnings dieses Projekts ({v.learnings.length})</Text>
        {v.learnings.length === 0 ? <Text dimColor>keine</Text> : v.learnings.slice(-6).map(l => <Text dimColor wrap="wrap">· {l}</Text>)}
        <Text> </Text>
        <Text dimColor>{v.enabled ? 'AN' : 'AUS'} · Zweitprüfung {v.secondOpinion ? 'an (kostet extra Tokens)' : 'aus'} · /pruefer</Text>
      </Box>
    )
  })
}
