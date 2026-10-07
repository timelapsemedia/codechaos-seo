// Deterministische Prüfungen; das Ergebnis geht als Hinweis an Claude (funktioniert auch ohne Oberfläche).

const ts = (s: string) => {
  const m = s.trim().match(/^(?:(\d+):)?(\d{1,2}):(\d{2})[,.](\d{1,3})$/)
  if (!m) return NaN
  return (Number(m[1] ?? 0) * 3600 + Number(m[2]) * 60 + Number(m[3])) * 1000 + Number((m[4] ?? '0').padEnd(3, '0'))
}

export function checkSubtitles(text: string): string[] {
  const issues: string[] = []
  const blocks = text.replace(/\r/g, '').replace(/^WEBVTT[^\n]*\n/, '').split(/\n{2,}/).filter(b => b.includes('-->'))
  let lastEnd = -1
  blocks.forEach((b, i) => {
    const lines = b.split('\n')
    const timeIdx = lines.findIndex(l => l.includes('-->'))
    const [a, z] = (lines[timeIdx] ?? '').split('-->')
    const start = ts(a ?? ''), end = ts((z ?? '').trim().split(/\s+/)[0] ?? '')
    const textLines = lines.slice(timeIdx + 1).filter(l => l.trim())
    const n = i + 1
    if (Number.isNaN(start) || Number.isNaN(end)) { issues.push(`Cue ${n}: Zeitstempel unlesbar`); return }
    if (end <= start) issues.push(`Cue ${n}: Ende vor Anfang`)
    if (start < lastEnd) issues.push(`Cue ${n}: überlappt mit vorherigem`)
    const dur = (end - start) / 1000
    if (dur > 0 && dur < 0.8) issues.push(`Cue ${n}: nur ${dur.toFixed(2)} s sichtbar`)
    if (dur > 7.5) issues.push(`Cue ${n}: ${dur.toFixed(1)} s sichtbar (lang)`)
    if (textLines.length > 2) issues.push(`Cue ${n}: ${textLines.length} Zeilen`)
    const long = textLines.find(l => l.replace(/<[^>]+>/g, '').length > 42)
    if (long) issues.push(`Cue ${n}: Zeile mit ${long.replace(/<[^>]+>/g, '').length} Zeichen`)
    const chars = textLines.join(' ').replace(/<[^>]+>/g, '').length
    if (dur > 0 && chars / dur > 21) issues.push(`Cue ${n}: ${(chars / dur).toFixed(0)} Zeichen/s`)
    lastEnd = Math.max(lastEnd, end)
  })
  if (blocks.length === 0) issues.push('keine Cues gefunden')
  return issues
}

export function checkHtmlSeo(html: string): string[] {
  const issues: string[] = []
  if (!/<html[\s>]/i.test(html)) return issues // Fragment/Template: nicht prüfen
  const title = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1]?.trim()
  if (!title) issues.push('kein <title>')
  else if (title.length > 60) issues.push(`<title> hat ${title.length} Zeichen (Richtwert ≤ 60)`)
  const desc = html.match(/<meta[^>]+name=["']description["'][^>]*>/i)?.[0]?.match(/content=["']([^"']*)["']/i)?.[1]
  if (desc === undefined) issues.push('keine Meta-Description')
  else if (desc.length > 160) issues.push(`Meta-Description hat ${desc.length} Zeichen (Richtwert ≤ 160)`)
  const h1 = (html.match(/<h1[\s>]/gi) ?? []).length
  if (h1 !== 1) issues.push(`${h1} × <h1> (genau eine empfohlen)`)
  const noAlt = (html.match(/<img\b(?![^>]*\balt=)[^>]*>/gi) ?? []).length
  if (noAlt) issues.push(`${noAlt} Bild(er) ohne alt`)
  if (!/<link[^>]+rel=["']canonical["']/i.test(html)) issues.push('kein canonical')
  return issues
}

export function checkCaption(text: string): string[] {
  const issues: string[] = []
  if (text.length > 2200) issues.push(`${text.length} Zeichen (Instagram max. 2.200)`)
  const tags = text.match(/(^|\s)#[\p{L}\p{N}_]+/gu) ?? []
  if (tags.length > 30) issues.push(`${tags.length} Hashtags (Instagram max. 30)`)
  return issues
}

export function checkFile(path: string, content: string): { kind: string; issues: string[] } | undefined {
  if (/\.(srt|vtt)$/i.test(path)) return { kind: 'Untertitel', issues: checkSubtitles(content) }
  if (/\.html?$/i.test(path)) return { kind: 'HTML-SEO', issues: checkHtmlSeo(content) }
  if (/(caption|post|instagram|reel|tiktok)[^/]*\.(txt|md)$/i.test(path)) return { kind: 'Caption', issues: checkCaption(content) }
  return undefined
}

const SECRETS: [string, RegExp][] = [
  ['Anthropic-API-Key', /\bsk-ant-[\w-]{20,}/],
  ['OpenAI-ähnlicher Key', /\bsk-(proj-)?[A-Za-z0-9]{32,}/],
  ['GitHub-Token', /\b(ghp|gho|ghs|ghu)_[A-Za-z0-9]{30,}|\bgithub_pat_[\w]{40,}/],
  ['AWS-Zugangsschlüssel', /\bAKIA[0-9A-Z]{16}\b/],
  ['Google-API-Key', /\bAIza[0-9A-Za-z_-]{35}\b/],
  ['Google-OAuth-Token', /\bya29\.[\w-]{20,}/],
  ['Meta/Instagram-Token', /\bEAA[A-Za-z0-9]{60,}/],
  ['Slack-Token', /\bxox[abprs]-[\w-]{10,}/],
  ['Privater Schlüssel', /-----BEGIN [A-Z ]*PRIVATE KEY-----/],
  ['OAuth-Code/Refresh-Token', /\b(code|refresh_token|access_token)=[\w.%-]{20,}/],
]

export function findSecrets(text: string): string[] {
  return SECRETS.filter(([, re]) => re.test(text)).map(([name]) => name)
}
