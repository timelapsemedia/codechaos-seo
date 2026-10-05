# Code Chaos & Abstract Sound Design: Wikidata, Discogs, MusicBrainz

Stand: 05.10.2026, geprüft über die öffentlichen APIs. Diese Einträge kann nur jemand mit eigenem Account anlegen, sie laufen unter deinem Namen. Unten steht alles zum Kopieren, sodass jeder Eintrag in wenigen Minuten erledigt ist.

**Ist-Zustand**

| Plattform | Code Chaos | Abstract Sound Design |
|---|---|---|
| Discogs | existiert: [artist/18204093](https://www.discogs.com/artist/18204093-Code-Chaos), Profil **leer**, keine Links | existiert: [label/4052777](https://www.discogs.com/label/4052777-Abstract-Sound-Design), Profil **leer** |
| MusicBrainz | existiert: [14d40d24-…](https://musicbrainz.org/artist/14d40d24-a91e-4600-a1b3-d14682d32e42), Beginn **falsch (2023-08-11)**, kein Ort, keine Links | existiert **nicht** |
| Wikidata | existiert **nicht** | existiert **nicht** |

Reihenfolge: 1. Discogs, 2. MusicBrainz, 3. Wikidata (Wikidata nutzt die IDs der beiden anderen als Belege).

---

## 1. Discogs (eingeloggt → Seite öffnen → „Edit Artist“ bzw. „Edit Label“)

### Artist: Code Chaos (18204093)
- **Real Name:** Tim Borchert
- **Profile:**
  ```
  German producer of [g=Hi Tech], [g=Psy-Trance] and dark psytrance from Hamburg, active since 2016. Self-described style: "New Psychedelic Death Art". Co-founder of the label [l=Abstract Sound Design] (2021). Studio project only, no live shows or DJ sets. Also runs the mastering service Polished Media and the plugin brand Code Chaos Audio.
  ```
  (Falls `[g=…]`-Tags nicht akzeptiert werden, einfach als Klartext lassen.)
- **Sites** (eine URL pro Zeile):
  ```
  https://codechaos-official.de/
  https://codechaos.bandcamp.com/
  https://soundcloud.com/codechaos
  https://www.instagram.com/codechaos_official
  https://www.youtube.com/@codechaos_abstractsounddesign
  https://www.tiktok.com/@codechaos_abstractsound
  https://x.com/codechaos_music
  ```
- **Aliases / Name Variations:** Moonchild (nur eintragen, wenn die frühen Releases auf moonchildproject.bandcamp.com tatsächlich unter diesem Alias liefen)

### Label: Abstract Sound Design (4052777)
- **Profile:**
  ```
  German independent label for psycore, hitech psytrance and darkpsy, founded in 2021 and co-founded by [a=Code Chaos].
  ```
- **Sites:** `https://www.abstract-sound-design.de/` und `https://abstract-sound-design.bandcamp.com/`

---

## 2. MusicBrainz (eingeloggt)

### Artist bearbeiten: https://musicbrainz.org/artist/14d40d24-a91e-4600-a1b3-d14682d32e42/edit
- **Type:** Person (Solo-Projekt). Alternativ „Group“, falls du es als Projekt führen willst. Für ein Ein-Personen-Projekt ist „Person“ üblich.
- **Area:** Hamburg
- **Begin date:** 2016 (das aktuelle 2023-08-11 ist falsch)
- **Disambiguation:** `German psytrance producer`
- **Alias:** `Tim Borchert` (Typ: Legal name), sofern du das öffentlich haben willst. Auf der Website steht der Name bereits.
- **External links:** dieselben URLs wie bei Discogs, plus `https://www.discogs.com/artist/18204093-Code-Chaos`
- **Edit note** (Pflichtfeld für gute Edits): `Information from the artist's official website https://codechaos-official.de/ (I am the artist).`

### Label neu anlegen: https://musicbrainz.org/label/create
- **Name:** Abstract Sound Design
- **Type:** Original Production
- **Area:** Germany
- **Begin date:** 2021
- **External links:** `https://www.abstract-sound-design.de/`, `https://abstract-sound-design.bandcamp.com/`, `https://www.discogs.com/label/4052777-Abstract-Sound-Design`

Danach kann der Artist mit dem Label verknüpft werden (Relationship „founder“).

---

## 3. Wikidata per QuickStatements (am einfachsten)

1. Mit Wikidata-Account einloggen und https://quickstatements.toolforge.org/ öffnen („Log in“ oben rechts).
2. „New batch“ → Block unten einfügen → „Import V1 commands“ → „Run“.
3. Danach die neue Label-Q-Nummer in den letzten Block (P264) eintragen und diesen extra ausführen.

**Hinweis:** Wikidata verlangt, dass ein Eintrag belegbar ist. Die Discogs- und MusicBrainz-IDs dienen als Belege, deshalb erst die Schritte 1 und 2 erledigen. Sehr kleine Einträge ohne externe Quellen können von Admins gelöscht werden.

### Batch A: Artist Code Chaos
```
CREATE
LAST	Len	"Code Chaos"
LAST	Lde	"Code Chaos"
LAST	Den	"German psytrance producer (hitech, psycore, darkpsy) from Hamburg"
LAST	Dde	"deutscher Psytrance-Produzent (Hitech, Psycore, Darkpsy) aus Hamburg"
LAST	P31	Q215380
LAST	P495	Q183
LAST	P740	Q1055
LAST	P571	+2016-00-00T00:00:00Z/9
LAST	P136	Q105404852
LAST	P136	Q114107195
LAST	P136	Q2452152
LAST	P856	"https://codechaos-official.de/"
LAST	P1953	"18204093"
LAST	P434	"14d40d24-a91e-4600-a1b3-d14682d32e42"
LAST	P3283	"codechaos"
LAST	P3040	"codechaos"
LAST	P2003	"codechaos_official"
LAST	P7085	"codechaos_abstractsound"
LAST	P2002	"codechaos_music"
LAST	P11892	"codechaos_official"
```

### Batch B: Label Abstract Sound Design
```
CREATE
LAST	Len	"Abstract Sound Design"
LAST	Lde	"Abstract Sound Design"
LAST	Den	"German record label for psycore, hitech psytrance and darkpsy"
LAST	Dde	"deutsches Plattenlabel für Psycore, Hitech Psytrance und Darkpsy"
LAST	P31	Q18127
LAST	P17	Q183
LAST	P571	+2021-00-00T00:00:00Z/9
LAST	P136	Q114107195
LAST	P136	Q105404852
LAST	P136	Q2452152
LAST	P856	"https://www.abstract-sound-design.de/"
LAST	P1955	"4052777"
LAST	P3283	"abstract-sound-design"
```

### Batch C: Verknüpfung (Q-Nummern aus A und B einsetzen)
```
Q_ARTIST	P264	Q_LABEL
Q_LABEL	P112	Q_ARTIST
```
Dazu, sobald vorhanden: die MusicBrainz-Label-ID beim Label als `P966` ergänzen.

Verwendete IDs (geprüft): Q215380 musical group · Q183 Deutschland · Q1055 Hamburg · Q18127 record label · Q105404852 hi-tech psytrance · Q114107195 psycore · Q2452152 dark psytrance · P1953 Discogs artist · P1955 Discogs label · P434 MusicBrainz artist · P3283 Bandcamp · P3040 SoundCloud · P2003 Instagram · P7085 TikTok · P2002 X · P11892 Threads.

---

## 4. Danach auf der Website ergänzen

Sobald die Wikidata-Q-Nummer existiert, kommt sie ins `sameAs` des Artists (in `index.html`, Block `MusicGroup`), zusammen mit den Discogs- und MusicBrainz-Links. Sag mir einfach die Q-Nummer.
