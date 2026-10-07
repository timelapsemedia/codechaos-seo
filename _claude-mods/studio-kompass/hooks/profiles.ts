export type Profile = { id: string; name: string; detect: RegExp; rules: string }

// Kurze, stabile Regeln je Bereich. Zahlen sind gängige Plattform-Richtwerte; Claude soll aktuelle Grenzen bei Bedarf prüfen.
export const PROFILES: Profile[] = [
  {
    id: 'musik',
    name: 'Musikproduktion (Hitech/Psytrance/Darkpsy, Ableton/REAPER)',
    detect: /\b(hitech|psytrance|psycore|darkpsy|ableton|reaper|reascript|vst3?|daw|bpm|midi|arrangement|kick|bassline|vital|serum|supercollider|remix|track\s?\d)/i,
    rules: '- Nenne BPM, Tonart/Skala und Taktzahlen explizit; Arrangement in Takten.\n- Nur Plugins/Instrumente verwenden, die nachweislich installiert sind (scannen statt annehmen).\n- Prüfwerkzeuge (falls geladen): mcp__audio-labor__messen/vergleichen für Bounces, midi_pruefen (Skala, Tempo, Takte), lua_pruefen für ReaScript.\n- Ableton-Bridge/Python-Skripte unter Windows mit PYTHONIOENCODING=utf-8 starten.',
  },
  {
    id: 'mastering',
    name: 'Mastering (Death/Black Metal u. a.)',
    detect: /\b(master(ing)?|lufs|true\s?peak|dbtp|limiter|loudness|death\s?metal|black\s?metal|deathmetal|blackmetal)\b/i,
    rules: '- Lautheit immer gemessen angeben (Integrated LUFS, True Peak dBTP, LRA) – nie schätzen; dafür mcp__audio-labor__messen/vergleichen nutzen, falls geladen.\n- Streaming normalisiert (Spotify/YouTube ca. −14 LUFS integriert); True Peak ≤ −1 dBTP gegen Clipping nach Encoding.\n- Vor der Abgabe: Fade-out vorhanden, letztes Sample nahe 0 (kein Klick), keine Stille am Anfang.\n- Vorher/Nachher-Messwerte gegenüberstellen; Originaldateien nie überschreiben; nach jeder Korrektur die neue Datei erneut senden (keine alten Stände testen lassen).',
  },
  {
    id: 'video',
    name: 'Videoschnitt & Untertitel (DaVinci Resolve, Vimeo, Shorts)',
    detect: /\b(davinci|resolve|schnitt|video|vimeo|untertitel|subtitle|\.srt|\.vtt|shorts?|reel|timeline|ffmpeg|render)\b/i,
    rules: '- Untertitel: max. 2 Zeilen, ca. 42 Zeichen/Zeile (Shorts: kurze Einblendungen ≤ 15 Zeichen im sicheren Bereich), Standzeit ca. 1–7 s, ≤ ca. 20 Zeichen/s, ohne Überlappung.\n- Werkzeuge (falls geladen): mcp__video-werkstatt__analysieren, standbilder (mit safe_area_9_16 Untertitel und Crop sichtbar kontrollieren), shorts_untertitel, einbrennen, transkribieren, untertitel_pruefen.\n- DaVinci Resolve: Untertitel nur auf der Edit-Seite erzeugen; Hochkant-Auflösung pro Timeline (eigene Timeline-Einstellungen), nicht fürs ganze Projekt; Render-Status abfragen statt sleep-Schleifen; Endstille schneiden; eingebrannten Text der Quelle im Crop prüfen.\n- ffmpeg-Ausgaben nie über Quellen schreiben; Ergebnis vor dem Senden messen.',
  },
  {
    id: 'motion',
    name: 'Motion Graphics / Animation (wie After Effects, Higgsfield, Runway, LTX)',
    detect: /\b(motion\s?graphics?|after\s?effects|animation|keyframe|higgsfield|runway|ltx|kling|lottie|remotion|visualizer|keinduftbaum|creative|werbevideo)\b/i,
    rules: '- Seitenverhältnis, Auflösung, fps und Dauer vorab festlegen und am Ergebnis prüfen.\n- Bei kostenpflichtigen Generierungen (Credits) vorher Kosten nennen und bestätigen lassen; Ergebnisse in einen benannten Projektordner herunterladen.\n- Nur echte Produkte zeigen – nichts erfinden. KeinDuftbaum/Druwids-Werbung: weibliche Creatorin und weibliche deutsche Stimme (bei schwacher Higgsfield-Stimme mit ElevenLabs nachvertonen).\n- KI-generierte Inhalte im Post als KI kennzeichnen.',
  },
  {
    id: 'social',
    name: 'Social-Media-Management (Instagram, TikTok, YouTube, Druwids)',
    detect: /\b(instagram|insta|tiktok|reel|caption|hashtag|post|karussell|carousel|druwids|meta\s?ads?|werbekonto|youtube|story)\b/i,
    rules: '- Vorgabe des Nutzers: 5 Hashtags pro Post und ein KI-Hinweis bei KI-Bildern/-Videos; YouTube immer mit Titel, Beschreibung und Tags.\n- Grenzen: Instagram-Caption max. 2.200 Zeichen, max. 30 Hashtags; YouTube-Titel max. 100, Beschreibung max. 5.000.\n- Werkzeuge (falls geladen): mcp__social-studio__text_pruefen/bilder_pruefen vor jedem Post; Instagram nur über mcp__insta-publisher__ig_* (Token nie in Routinen oder Prompts).\n- Automatisches Veröffentlichen nur nach ausdrücklicher Freigabe oder in einer vom Nutzer eingerichteten Routine.\n- Gesundheits-/Wirkversprechen bei Pflanzen/Substanzen vermeiden (Plattformregeln, Heilmittelwerbegesetz).',
  },
  {
    id: 'seo',
    name: 'SEO & Marketing (GSC, Bing, Wikipedia/Wikidata, GEO)',
    detect: /\b(seo|geo|gsc|search\s?console|bing|ranking|meta\s?description|sitemap|schema\.org|wikidata|wikipedia|backlink|conversion|keyword)\b/i,
    rules: '- <title> ca. ≤ 60 Zeichen, Meta-Description ca. ≤ 160 Zeichen, genau eine <h1>, Bilder mit alt, canonical gesetzt.\n- Werkzeuge (falls geladen): mcp__seo-werkstatt__site_pruefen vor jedem Push (kaputte Links, .jpg/.jpeg, Groß-/Klein, div-Balance, hreflang), seite_pruefen und sitemap_pruefen nach dem Deploy auf der Live-Seite.\n- Zahlen (Klicks, Positionen) nur aus echten GSC/Bing-Abfragen, mit Zeitraum; nie schätzen.\n- Wikipedia: Interessenkonflikt offenlegen; Bot-Edits brauchen Genehmigung.',
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
    rules: '- Fakten zu Bands, Besetzungen, Veröffentlichungen nur mit Quelle (Link) nennen; Unsicheres als unsicher markieren.\n- Werkzeuge (falls geladen): mcp__raritaeten-jaeger__suchlinks/suchverlauf vor jeder Suche (nichts doppelt suchen), suche_merken nach jeder Suche, fund_merken für Treffer.\n- Fundstellen als Liste mit Preis, Zustand, Link und Abrufdatum.',
  },
]

export const ALWAYS = `Arbeitsregeln vom Plugin „studio-kompass“:
- Antworte und berichte auf Deutsch (Englisch nur für Kunden-Reviews, wenn gewünscht).
- Kontrolliere jedes Ergebnis selbst, bevor du es ausgibst (messen, ansehen, testen); nach jeder Korrektur alle betroffenen Dateien erneut senden.
- Nenne jede erstellte oder geänderte Datei mit vollem Pfad und sag dazu, ob sie in einer Cloud-Session (Container, nicht auf dem Rechner des Nutzers) oder lokal liegt.
- Gib Geheimnisse (API-Keys, Tokens, Passwörter, OAuth-Codes) nie im Klartext aus und schreibe sie nie in Repository-Dateien; empfiehl Umgebungsvariablen bzw. API-Credentials der Umgebung.
- Was eine Plattform nicht erlaubt (z. B. fehlende API, Login nur im Browser, Bot-Genehmigung), einmal klar sagen und die kürzeste machbare Alternative anbieten.`

export function detect(text: string): string[] {
  return PROFILES.filter(p => p.detect.test(text)).map(p => p.id)
}
