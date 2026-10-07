import { expect, mock, test } from 'claude-code/testing'

import { judge } from '../hooks/register'

const PROPS = { bodyColumns: 60 } as never

function boot(on: any, surfaces: string[] = ['terminal']) {
  mock.store(on)
  mock.clock(on, { now: Date.parse('2026-10-07T10:00:00Z') })
  on('session.start', (_$: unknown, e: { cwd: string }) => ({ cwd: e.cwd }))
  on('command.register', () => ({ value: undefined }))
  on('ui.open', () => ({ value: { isOpen: true } }))
  on('session.repo', () => ({ value: null }))
  on('session.root', () => ({ value: '/proj/demo' }))
  on('session.surfaces', () => ({ value: surfaces }))
  on('session.model', () => ({ value: 'claude-opus-5-5' }))
  on('turn.start', (_$: unknown, e: { turnId: string }) => ({ turnId: e.turnId }))
  on('classic.Stop', () => ({}))
  on('prompt.compose', () => ({ sections: [{ id: 'intro', text: 'x', scope: 'shared' }] }))
  on('tool.call', (_$: unknown, e: { tool: string; command?: string }) =>
    e.tool === 'Bash' && e.command?.includes('FAIL') ? { result: { stdout: '', stderr: 'x' }, isError: true, text: 'x' } : { result: { ok: true }, text: 'ok' },
  )
}

const stop = (msg: string, extra: object = {}) => ({ stop_hook_active: false, last_assistant_message: msg, background_tasks: [], ...extra }) as never

test('Urteil nur nach Belegen', async () => {
  expect(judge({ files: [], checks: [], message: 'funktioniert', lastEditSeq: -1 }).block).toBeUndefined()
  expect(judge({ files: ['a.ts'], checks: [], message: 'Fertig, funktioniert.', lastEditSeq: 1 }).block).toContain('behauptet Erfolg')
  expect(judge({ files: ['a.ts'], checks: [{ cmd: 'npm test', ok: true, seq: 1, afterEdit: true }], message: 'ok', lastEditSeq: 2 }).block).toContain('kein Test')
  expect(judge({ files: ['a.ts'], checks: [{ cmd: 'npm test', ok: false, seq: 3, afterEdit: true }], message: 'ok', lastEditSeq: 2 }).block).toContain('noch rot')
  expect(judge({ files: ['a.ts'], checks: [{ cmd: 'npm test', ok: false, seq: 3, afterEdit: true }, { cmd: 'npm test', ok: true, seq: 4, afterEdit: true }], message: 'ok', lastEditSeq: 2 }).block).toBeUndefined()
  expect(judge({ files: ['a.ts'], checks: [{ cmd: 'pytest -k x', ok: false, seq: 3, afterEdit: true }, { cmd: 'pytest', ok: true, seq: 4, afterEdit: true }], message: 'ok', lastEditSeq: 2 }).block).toBeUndefined()
  expect(judge({ files: ['a.ts'], checks: [{ cmd: 'npx tsc --noEmit', ok: false, seq: 3, afterEdit: true }, { cmd: 'npm test', ok: true, seq: 4, afterEdit: true }], message: 'ok', lastEditSeq: 2 }).block).toContain('tsc')
  expect(judge({ files: ['a.ts'], checks: [], message: 'Nicht getestet, weil keine Testumgebung da ist.', lastEditSeq: 1 }).block).toBeUndefined()
})

test('Sperrt ohne Test höchstens zweimal, dann durch; Learning gespeichert und mitgegeben', async ($, on) => {
  boot(on)
  await $.session.start({ cwd: '/proj/demo' } as never)
  await $.turn.start({ text: 'Bau Feature X', turnId: 't1' })
  await $.tool.call({ tool: 'Edit', file_path: '/proj/demo/a.ts', old_string: 'a', new_string: 'b' } as never)
  const r1 = await $.classic.Stop(stop('Fertig, funktioniert.'))
  expect(r1.block).toContain('a.ts')
  const r2 = await $.classic.Stop(stop('Jetzt aber fertig.', { stop_hook_active: true }))
  expect(r2.block).toBeDefined()
  const r3 = await $.classic.Stop(stop('Fertig.', { stop_hook_active: true }))
  expect(r3.block).toBeUndefined()
  // Neue Learnings wirken ab der nächsten Session (stabiler System-Prompt); Sessionstart simulieren:
  await $.session.start({ cwd: '/proj/demo' } as never)
  const composed = await $.prompt.compose({ model: 'm', promptModel: 'm', surfaces: ['terminal'], tools: [], outputStyle: null, traits: [] } as never)
  const learned = composed.sections.find(s => s.id === 'pruefer:learnings')?.text ?? ''
  expect(learned).toContain('a.ts')
  expect(learned.split('\n- ').length - 1).toBe(2)
})

test('Grüner Test nach der Änderung: Abgabe geht durch; roter Test: Sperre', async ($, on) => {
  boot(on)
  await $.session.start({ cwd: '/proj/demo' } as never)
  await $.turn.start({ text: 'Fix', turnId: 't1' })
  await $.tool.call({ tool: 'Write', file_path: '/proj/demo/b.py', content: 'x' } as never)
  await $.tool.call({ tool: 'Bash', command: 'pytest -q FAIL' } as never)
  expect((await $.classic.Stop(stop('Erledigt.'))).block).toContain('noch rot')
  await $.tool.call({ tool: 'Bash', command: 'pytest -q' } as never)
  expect((await $.classic.Stop(stop('Erledigt.', { stop_hook_active: true }))).block).toBeUndefined()
})

test('Nie sperren: Rückfrage, Hintergrundjob, Headless', async ($, on) => {
  boot(on)
  await $.session.start({ cwd: '/proj/demo' } as never)
  await $.turn.start({ text: 'Fix', turnId: 't1' })
  await $.tool.call({ tool: 'Edit', file_path: '/proj/demo/a.ts', old_string: 'a', new_string: 'b' } as never)
  expect((await $.classic.Stop(stop('Soll ich A oder B nehmen?'))).block).toBeUndefined()
  expect((await $.classic.Stop(stop('Fertig.', { background_tasks: [{ id: 'b1' }] }))).block).toBeUndefined()
})

test('Headless-Lauf wird nie gesperrt', async ($, on) => {
  boot(on, [])
  await $.session.start({ cwd: '/proj/demo' } as never)
  await $.turn.start({ text: 'Fix', turnId: 't1' })
  await $.tool.call({ tool: 'Edit', file_path: '/proj/demo/a.ts', old_string: 'a', new_string: 'b' } as never)
  expect((await $.classic.Stop(stop('Fertig.'))).block).toBeUndefined()
})

test('Seitenpanel zeigt Dateien, Checks, Status (Terminal und Desktop); /pruefer schaltet aus', async ($, on) => {
  boot(on)
  on('ui.close', () => ({ value: undefined }))
  await $.session.start({ cwd: '/proj/demo' } as never)
  await $.turn.start({ text: 'Fix', turnId: 't1' })
  await $.tool.call({ tool: 'Edit', file_path: '/proj/demo/a.ts', old_string: 'a', new_string: 'b' } as never)
  await $.tool.call({ tool: 'Bash', command: 'npm test' } as never)
  await $.classic.Stop(stop('Fertig.'))
  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ plugin: 'pruefer', surface, component: 'Pane', requestId: 'pruefer', props: PROPS })
    expect(await ui.find({ type: 'Text', text: /durchgelassen/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /a\.ts/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /npm test/ })).toBeDefined()
    await ui.unmount()
  }
  const off = await $.command.run({ command: 'pruefer', args: '' } as never)
  expect(off.text).toContain('AUS')
  await $.tool.call({ tool: 'Edit', file_path: '/proj/demo/c.ts', old_string: 'a', new_string: 'b' } as never)
  expect((await $.classic.Stop(stop('Fertig.'))).block).toBeUndefined()
})

test('Schwierige Antwort (≥5 Dateien): Zweitprüfung läuft sichtbar und kann sperren; abschaltbar', async ($, on) => {
  boot(on)
  let asked = 0
  on('model.complete', () => { asked += 1; return { value: { isAnswered: true, text: '{"ok": false, "grund": "Für e.ts gibt es keinen Test."}', usage: { input_tokens: 1, output_tokens: 1, cache_read_input_tokens: 0, cache_creation_input_tokens: 0 } } } as never })
  on('process.run', () => ({ value: { stdout: ' 5 files changed', stderr: '', exitCode: 0 } }) as never)
  on('ui.toast', () => ({ value: undefined }) as never)
  await $.session.start({ cwd: '/proj/demo' } as never)
  await $.turn.start({ text: 'Großer Umbau', turnId: 't1' })
  for (const f of ['a', 'b', 'c', 'd', 'e']) await $.tool.call({ tool: 'Edit', file_path: `/proj/demo/${f}.ts`, old_string: 'a', new_string: 'b' } as never)
  await $.tool.call({ tool: 'Bash', command: 'npm test' } as never)
  const r = await $.classic.Stop(stop('Fertig.'))
  expect(asked).toBe(1)
  expect(r.block).toContain('Zweitprüfung')
  await $.command.run({ command: 'pruefer', args: 'zweit aus' } as never)
  expect((await $.classic.Stop(stop('Fertig.', { stop_hook_active: true }))).block).toBeUndefined()
  expect(asked).toBe(1)
})

test('Mess-Werkzeuge anderer Mods zählen als Beleg', async ($, on) => {
  boot(on)
  await $.session.start({ cwd: '/proj/demo' } as never)
  await $.turn.start({ text: 'Master fertig machen', turnId: 't1' })
  await $.tool.call({ tool: 'Write', file_path: '/proj/demo/master.py', content: 'x' } as never)
  expect((await $.classic.Stop(stop('Fertig.'))).block).toBeDefined()
  await $.tool.call({ tool: 'mcp__audio-labor__messen', datei: '/proj/demo/out.wav' } as never)
  expect((await $.classic.Stop(stop('Fertig.', { stop_hook_active: true }))).block).toBeUndefined()
})
