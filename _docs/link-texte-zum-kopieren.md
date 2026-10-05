# Link-Texte zum Kopieren (ca. 20–30 Minuten Handarbeit)

Bandcamp, SoundCloud, Gumroad, Discogs und MusicBrainz bieten keine Schnittstelle, über die sich diese Texte automatisch eintragen lassen. YouTube geht automatisch, siehe unten.

## Bandcamp (codechaos.bandcamp.com → Release öffnen → „edit“ → About this album/track, ans Ende)

**Psycore-Releases:** Roadside Butchery · The Slaughterhouse · Filaments & Voids · Abstrakte Musik · Code Pandorum – Rotten Soil (Code Chaos Remix)
```
Was ist Psycore? → https://codechaos-official.de/psycore/
```

**Hitech-Releases:** The Grudge · Interstellar · Ruins Of Humanity · Heart & Mind · Parallax Prison – Schism of Self · A Tiny Piece Of Paper · TANZALARM · Chaos Kidz
```
Was ist Hitech Psytrance? → https://codechaos-official.de/hitech-psytrance/
```

**Darkpsy-Releases:** Oblivion · The Twilight Zone · Amanita Muscaria
```
Was ist Darkpsy? → https://codechaos-official.de/darkpsy/
```

**Releases mit mehreren Genres:** Runtime Terror · Insomnia · Paradigma
```
Genre-Guides: https://codechaos-official.de/psycore/ · https://codechaos-official.de/hitech-psytrance/ · https://codechaos-official.de/darkpsy/
```

**Unter jeden Release zusätzlich:**
```
Mastering für Psycore, Hitech & Darkpsy: https://codechaos-official.de/mastering/
```

## SoundCloud (Track → „Edit“ → Description)
Dieselben Zeilen wie bei Bandcamp, passend zum Genre des Tracks. In die Profil-Bio:
```
Psycore · Hitech · Darkpsy aus Hamburg · https://codechaos-official.de/
Mastering: https://codechaos-official.de/mastering/
```

## Gumroad (Crucible → Edit → Description, ans Ende)
```
Features, saturation types & FAQ: https://codechaos-official.de/crucible.html
Built by Code Chaos: https://codechaos-official.de/
```
Komplett überarbeiteter Produkttext: `_docs/gumroad-crucible-text.md`.

## YouTube (automatisch möglich)
Das Skript `_marketing/youtube_descriptions.py` ergänzt Kanal-Info und alle Videobeschreibungen passend zum Genre. Es braucht OAuth-Zugangsdaten mit dem Scope `youtube` (`YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`). Erst Probelauf, dann `--apply`.

## Discogs, MusicBrainz, Wikidata
Fertige Eingaben in `_docs/entitaeten-wikidata-discogs-musicbrainz.md`. Bei Wikidata reicht ein Einfügen in QuickStatements und ein Klick auf „Run“.

## Reddit und Foren: Antwortvorlagen
Nur auf echte Fragen antworten, nicht dieselbe Antwort mehrfach posten und nicht in jeden Thread einen Link setzen. Sonst wertet Reddit das als Spam und sperrt das Konto.

**„Was ist Psycore?“**
```
Psycore ist die schnellste, extremste Ecke vom Psytrance: 180 bis über 300 BPM, meist 190–240. Statt Drops und Breaks gibt's einen fast statischen Puls mit Sinus-Kick und rollender Neurotrance-Bassline, darüber dichte, dunkle Soundscapes. Eher Trance-Zustand als Song. Ich produziere das selbst und hab hier einen ausführlichen Guide mit BPM, Geschichte und Produktionstipps geschrieben: https://codechaos-official.de/psycore/
```

**„Hitech vs. Psycore?“**
```
Beide schnell, aber anderes Feeling: Hitech (170–230+ BPM) ist komplex, glitchy, voller Wechsel und kann sogar euphorisch sein. Psycore (180–300+ BPM) ist minimal, statisch, hypnotisch und durchgehend dunkel. Vergleichstabelle und Beispiele: https://codechaos-official.de/hitech-psytrance/
```

**„Darkpsy BPM?“**
```
Darkpsy liegt meist bei 155–175 BPM, insgesamt 150–200. Darüber geht's Richtung Hitech (170–230+) und Psycore (180–300+). Übersicht mit allen drei: https://codechaos-official.de/darkpsy/
```
