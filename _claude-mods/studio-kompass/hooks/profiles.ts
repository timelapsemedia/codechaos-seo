export type Profile = { id: string; name: string; detect: RegExp; rules: string }

// Kurze, stabile Regeln je Bereich. Zahlen sind gängige Plattform-Richtwerte; Claude soll aktuelle Grenzen bei Bedarf prüfen.
export const PROFILES: Profile[] = [
  {
    id: 'musik',
    name: 'Musikproduktion (Hitech/Psytrance/Darkpsy, Ableton/REAPER)',
    detect: /\b(hitech|psytrance|psycore|darkpsy|ableton|reaper|reascript|vst3?|daw|bpm|midi|arrangement|kick|bassline|vital|serum|supercollider|remix|track\s?\d)/i,
    rules: '- Nenne BPM, Tonart/Skala und Taktzahlen explizit; Arrangement in Takten.\n- Nur Plugins/Instrumente verwenden, die nachweislich installiert sind (scannen statt annehmen).\n- Skripte (Lua/ReaScript, Python) vor Abgabe mindestens syntaktisch prüfen (z. B. luac -p, python -m py_compile).',
  },
  {
    id: 'mastering',
    name: 'Mastering (Death/Black Metal u. a.)',
    detect: /\b(master(ing)?|lufs|true\s?peak|dbtp|limiter|loudness|death\s?metal|black\s?metal|deathmetal|blackmetal)\b/i,
    rules: '- Lautheit immer gemessen angeben (Integrated LUFS, True Peak dBTP, LRA) – nie schätzen.\n- Streaming normalisiert (Spotify/YouTube ca. −14 LUFS integriert); True Peak ≤ −1 dBTP als Richtwert gegen Clipping nach Encoding.\n- Vorher/Nachher-Messwerte gegenüberstellen; Originaldateien nie überschreiben.',
  },
  {
    id: 'video',
    name: 'Videoschnitt & Untertitel (DaVinci Resolve, Vimeo, Shorts)',
    detect: /\b(davinci|resolve|schnitt|video|vimeo|untertitel|subtitle|\.srt|\.vtt|shorts?|reel|timeline|ffmpeg|render)\b/i,
    rules: '- Untertitel: max. 2 Zeilen, ca. 42 Zeichen/Zeile, Standzeit ca. 1–7 s, Lesegeschwindigkeit ≤ ca. 20 Zeichen/s, Zeiten aufsteigend ohne Überlappung.\n- ffmpeg-Ausgaben nie über Quellen schreiben; Format, Auflösung, fps und Dauer des Ergebnisses mit ffprobe belegen.',
  },
  {
    id: 'motion',
    name: 'Motion Graphics / Animation (wie After Effects, Higgsfield, Runway, LTX)',
    detect: /\b(motion\s?graphics?|after\s?effects|animation|keyframe|higgsfield|runway|ltx|kling|lottie|remotion|visualizer)\b/i,
    rules: '- Seitenverhältnis, Auflösung, fps und Dauer vorab festlegen und am Ergebnis prüfen.\n- Bei kostenpflichtigen Generierungen (Credits) vorher Kosten nennen und bestätigen lassen.',
  },
  {
    id: 'social',
    name: 'Social-Media-Management (Instagram, TikTok, YouTube, Druwids)',
    detect: /\b(instagram|insta|tiktok|reel|caption|hashtag|post|karussell|carousel|druwids|meta\s?ads?|werbekonto|youtube|story)\b/i,
    rules: '- Richtwerte: Instagram-Caption max. 2.200 Zeichen und max. 30 Hashtags; YouTube-Titel max. 100, Beschreibung max. 5.000 Zeichen.\n- Vor dem Posten: Entwurf zeigen; automatisches Veröffentlichen nur nach ausdrücklicher Freigabe.\n- Gesundheits-/Wirkversprechen bei Pflanzen/Substanzen vermeiden (Plattformregeln, Heilmittelwerberecht).',
  },
  {
    id: 'seo',
    name: 'SEO & Marketing (GSC, Bing, Wikipedia/Wikidata, GEO)',
    detect: /\b(seo|geo|gsc|search\s?console|bing|ranking|meta\s?description|sitemap|schema\.org|wikidata|wikipedia|backlink|conversion|keyword)\b/i,
    rules: '- <title> ca. ≤ 60 Zeichen, Meta-Description ca. ≤ 160 Zeichen, genau eine <h1>, Bilder mit alt, canonical gesetzt.\n- Zahlen (Klicks, Positionen) nur aus echten GSC/Bing-Abfragen, mit Zeitraum; nie schätzen.\n- Wikipedia: keine Selbstdarstellung/Interessenkonflikt verschweigen; Bot-Edits brauchen Genehmigung.',
  },
  {
    id: 'etsy',
    name: 'Etsy & E-Commerce',
    detect: /\b(etsy|listing|shop|print\s?on\s?demand|e-?commerce|produkt(titel|beschreibung))\b/i,
    rules: '- Etsy-Richtwerte: Titel max. 140 Zeichen, max. 13 Tags à max. 20 Zeichen.\n- OAuth-/API-Zugänge: Schritte für den Nutzer einmal klar und vollständig auflisten, statt mehrfach nachzufragen.',
  },
  {
    id: 'recherche',
    name: 'Recherche (Diskographien, seltene CDs/Tapes, Fakten)',
    detect: /\b(recherche|diskograph|discogs|lineup|besetzung|release|tape|kassette|demo|vinyl|quelle|research)\b/i,
    rules: '- Fakten zu Bands, Besetzungen, Veröffentlichungen nur mit Quelle (Link) nennen; Unsicheres als unsicher markieren.\n- Fundstellen als Liste mit Preis, Zustand, Link und Abrufdatum.',
  },
]

export const ALWAYS = `Arbeitsregeln vom Plugin „studio-kompass“:
- Nenne jede erstellte oder geänderte Datei mit vollem Pfad und sag dazu, ob sie in einer Cloud-Session (Container, nicht auf dem Rechner des Nutzers) oder lokal liegt.
- Gib Geheimnisse (API-Keys, Tokens, Passwörter, OAuth-Codes) nie im Klartext aus und schreibe sie nie in Repository-Dateien; empfiehl Umgebungsvariablen bzw. API-Credentials der Umgebung.
- Was eine Plattform nicht erlaubt (z. B. fehlende API, Login nur im Browser, Bot-Genehmigung), einmal klar sagen und die kürzeste machbare Alternative anbieten.`

export function detect(text: string): string[] {
  return PROFILES.filter(p => p.detect.test(text)).map(p => p.id)
}
