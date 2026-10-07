import { expect, mock, test } from 'claude-code/testing'

import { assessBash, assessPath } from '../hooks/register'

test('Erkennt riskante Befehle, lässt harmlose durch', async () => {
  for (const c of [
    'rm -rf build', 'rm notes.txt', 'cd x && rm -r y', 'find . -name "*.log" -delete',
    'git push --force origin main', 'git push -f', 'git push origin +main', 'git reset --hard HEAD~1',
    'git clean -fd', 'git checkout -- .', 'git restore .', 'git branch -D feature',
    'psql -c "DROP TABLE users;"', 'mysql -e "truncate table logs"', 'sqlite3 db.sqlite "DELETE FROM users;"',
    'redis-cli FLUSHALL', 'echo KEY=1 > .env', 'cp example.env .env', 'echo x | tee config/.env.local',
  ]) expect(assessBash(c), c).toBeDefined()
  for (const c of [
    'ls -la', 'git status', 'git push origin main', 'git reset HEAD file.txt', 'npm test', 'cat .env.example',
    'psql -c "DELETE FROM users WHERE id = 3;"', 'grep -r "rm -rf" docs', 'echo hi > out.txt', 'git checkout main',
  ]) expect(assessBash(c), c).toBeUndefined()
})

test('Dateien: Geheimnisse und außerhalb des Projekts', async () => {
  expect(assessPath('/proj/.env', '/proj')?.was).toContain('.env')
  expect(assessPath('/proj/keys/server.pem', '/proj')).toBeDefined()
  expect(assessPath('/home/u/.bashrc', '/proj')?.was).toContain('außerhalb')
  expect(assessPath('/proj/../other/a.txt', '/proj')?.was).toContain('außerhalb')
  expect(assessPath('/proj/src/a.ts', '/proj')).toBeUndefined()
  expect(assessPath('src/a.ts', '/proj')).toBeUndefined()
  expect(assessPath('/tmp/scratch/a.txt', '/proj')).toBeUndefined()
})

function boot(on: any, answer: string | 'reject' | 'fail-root') {
  mock.store(on)
  mock.clock(on, { now: Date.parse('2026-10-07T10:00:00Z') })
  const ran: string[] = []
  on('session.start', (_$: unknown, e: { cwd: string }) => ({ cwd: e.cwd }))
  on('command.register', () => ({ value: undefined }))
  on('ui.status', () => ({ value: undefined }))
  on('session.root', () => {
    if (answer === 'fail-root') throw new Error('kaputt')
    return { value: '/proj/test-ordner' }
  })
  on('fs.stat', () => { throw new Error('ENOENT') })
  on('tool.call', (_$: unknown, e: any) => {
    if (e.tool === 'AskUserQuestion') {
      if (answer === 'reject') throw new Error('dismissed')
      const q = e.questions[0].question
      return { result: { questions: e.questions, answers: { [q]: answer } } }
    }
    ran.push(e.tool === 'Bash' ? e.command : `${e.tool} ${e.file_path}`)
    return { result: { ok: true }, text: 'ok' }
  })
  return ran
}

test('Harmloses läuft ohne Rückfrage; riskant + bestätigt läuft', async ($, on) => {
  const ran = boot(on, 'Ja, ausführen')
  await $.session.start({ cwd: '/proj/test-ordner' } as never)
  expect((await $.tool.call({ tool: 'Bash', command: 'ls' } as never)).deny).toBeUndefined()
  expect((await $.tool.call({ tool: 'Bash', command: 'rm dummy.txt' } as never)).deny).toBeUndefined()
  expect(ran).toEqual(['ls', 'rm dummy.txt'])
  const r = await $.command.run({ command: 'schutzschild', args: '' } as never)
  expect(r.text).toContain('2 Schritte geprüft, 1 angehalten')
})

test('Riskant + abgelehnt: blockiert', async ($, on) => {
  const ran = boot(on, 'Nein, abbrechen')
  await $.session.start({ cwd: '/proj/test-ordner' } as never)
  const r = await $.tool.call({ tool: 'Bash', command: 'git reset --hard' } as never)
  expect(r.deny).toContain('abgelehnt')
  expect(ran).toEqual([])
})

test('Keine Rückfrage möglich: blockiert', async ($, on) => {
  const ran = boot(on, 'reject')
  await $.session.start({ cwd: '/proj/test-ordner' } as never)
  const r = await $.tool.call({ tool: 'Write', file_path: '/proj/test-ordner/.env', content: 'X=1' } as never)
  expect(r.deny).toContain('nicht bestätigt')
  expect(ran).toEqual([])
})

test('Risikoprüfung fehlgeschlagen: blockiert mit Fehler', async ($, on) => {
  const ran = boot(on, 'fail-root')
  await $.session.start({ cwd: '/proj/test-ordner' } as never)
  const r = await $.tool.call({ tool: 'Edit', file_path: '/proj/test-ordner/a.txt', old_string: 'a', new_string: 'b' } as never)
  expect(r.deny).toContain('fehlgeschlagen')
  expect(ran).toEqual([])
})
