export type Tokens = { input: number; output: number; cacheWrite: number; cacheRead: number }
export type SparStats = {
  enabled: boolean
  /** Schritte, die Haiku beantwortet hat und die übernommen wurden */
  haikuSteps: number
  /** Haiku-Antworten, die verworfen und beim großen Modell wiederholt wurden */
  retried: number
  /** gemessen (API-Usage) */
  kept: Tokens
  wasted: Tokens
  /** Listenpreis-Schätzung in USD, null wenn ein Preis fehlt */
  keptUsd: number | null
  wastedUsd: number | null
}

declare module 'claude-code' {
  interface PluginState {
    'spar-modus': { stats: SparStats }
  }
}
