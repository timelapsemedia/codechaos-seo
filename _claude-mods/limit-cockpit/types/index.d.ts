export type Gauge = {
  /** 5-Stunden-Fenster, 0-100, nur wenn die API eine Messung lieferte */
  fivePct?: number
  fiveResetsAt?: string
  weekPct?: number
  weekResetsAt?: string
  ctxPct?: number
  ctxTokens?: number
  ctxWindow?: number
}

export type Drivers = {
  /** gemessen: eine Zeile je API-Anfrage (Usage aus der API) */
  measured: string[]
  /** geschätzt: Tool-Ausgaben nach Zeichenzahl / 4 */
  estimated: string[]
}

declare module 'claude-code' {
  interface PluginState {
    'limit-cockpit': { gauge: Gauge; drivers: Drivers | null; busy: string | null }
  }
}
