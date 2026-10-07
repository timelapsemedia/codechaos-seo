export type Check = { cmd: string; ok: boolean; seq: number; afterEdit: boolean }
export type Verdict = {
  kind: 'beobachtet' | 'gesperrt' | 'durchgelassen' | 'aus'
  reason: string
  blocks: number
}
export type PrueferView = {
  files: string[]
  checks: Check[]
  verdict: Verdict
  learnings: string[]
  enabled: boolean
  secondOpinion: boolean
}

declare module 'claude-code' {
  interface PluginState {
    pruefer: { view: PrueferView }
  }
}
