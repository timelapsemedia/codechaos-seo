# SEO- & GEO-Audit codechaos-official.de (Oktober 2026)

Stand: 05.10.2026 · Geprüft: `index.html`, `crucible.html`, `sitemap.xml`, `robots.txt`, `llms.txt`, Live-Seite.
Hinweis: Die Skills `/claude-seo:seo` und `/claude-seo:seo-geo` waren in der Session nicht installiert. Das Audit wurde manuell nach denselben Kriterien durchgeführt (Technik, On-Page, Content/E-E-A-T, Schema, GEO/KI-Sichtbarkeit, Performance, Recht). Suchvolumen-Tools standen nicht zur Verfügung, die Nachfrage-Einschätzung unten ist daher qualitativ.

---

## 1. Kurzfazit

Die Seite hatte eine sehr gute Grundlage (viel Genre-Content, FAQ, llms.txt, KI-Crawler erlaubt), aber mehrere Fehler, die Vertrauen und Ranking kosten:

- **Sichtbarer Code-Müll:** Ein kaputter HTML-Kommentar zeigte „ALBUM ANNOUNCEMENT, Runtime Terror ═══ -->“ als Text auf der Seite.
- **Widersprüche zur Entität:** „Studioprojekt ohne Liveshows“, gleichzeitig „produziert und **performed**“, „DJ-Performance“, „Hitech Psytrance Sets“.
- **Falsche Fakten im FAQ-Schema:** Hellfish, Broken Note, The Mover, DJ Freak, Shitmat und Nystagmus als „bekannte Psycore-Künstler“. Das sind Breakcore- und Hardcore-Acts, kein Psytrance. KI-Suchmaschinen übernehmen so etwas 1:1.
- **Entitäts-Vermischung im Schema:** YouTube und TikTok von Polished Media standen im `sameAs` des Artists, das Label hatte „gegründet“ vs. „mitgegründet“, und es gab ein erfundenes Album „Code Chaos Discography“.
- **9 einzelne, teils doppelte JSON-LD-Blöcke** plus widersprüchliche Microdata (z. B. zwei FAQPage-Definitionen mit unterschiedlichen Fragen, eine Breadcrumb aus Sprungmarken, eine SearchAction ohne Suchfunktion).
- **Performance:** 25 Release-Cover mit 1200 px (zusammen ca. 13 MB) wurden auf 300 px angezeigt, ein Label-Bild hatte 3000 px.
- **Sprachmix:** Die Seite ist `lang="de"`, aber Bio, Mastering-Texte, Label-Texte und Newsletter waren auf Englisch.
- **Crucible-OG-Bild:** Beim Teilen der Plugin-Seite erschien ein Porträtfoto statt des Plugins, mit falschen Bildmaßen.
- **Recht:** Impressum noch nach „§ 5 TMG“ (seit 05/2024 DDG). Google Fonts wurden extern geladen (DSGVO-Abmahnrisiko). Die Datenschutzerklärung nannte keinen der eingesetzten Dienste.

Alle Punkte oben sind behoben (Details in Abschnitt 2).

---

## 2. Umgesetzte Änderungen

| Bereich | Änderung |
|---|---|
| Technik | Kaputten HTML-Kommentar repariert (sichtbarer Text entfernt) |
| Technik | Doppelte ID `legal-backdrop` entfernt, Skip-Link zeigt jetzt auf `#main` |
| Technik | BPM-Ticker-Bug behoben (Label „Tempo Range“ wurde dauerhaft durch „300“ ersetzt) |
| Technik | `http://polished.media` → `https://` |
| Performance | 25 Release-Cover als 600-px-WebP mit sprechenden Dateinamen (`images/releases/code-chaos-*.webp`), ca. 13 MB → 1,9 MB |
| Performance | Label-Bild 800 KB → 247 KB, Sound-Bild 528 KB → 117 KB |
| Performance + DSGVO | Google Fonts selbst gehostet (`/fonts`, `/css/fonts.css`), keine Verbindung mehr zu Google |
| Performance | Inline-`onmouseover`-Handler der Cover durch CSS ersetzt |
| Meta | Title gekürzt (≈65 Zeichen), Meta-Description auf 159 Zeichen |
| Schema | Ein konsolidierter `@graph`: WebSite, WebPage, MusicGroup, Person (Tim Borchert), Label, MusicRecording + Single-Release „Uhrwerk aus Blut“, MusicAlbum „Runtime Terror“, Organization Polished Media, Service (alle 9 Preise), Product Crucible, FAQPage |
| Schema | FAQPage wird jetzt automatisch aus den sichtbaren FAQ erzeugt (14 Fragen, 1:1 synchron), Microdata-Duplikate entfernt |
| Schema | Entfernt: falsche Psycore-Künstler, fake Discography-Album, Polished-Media-Profile im Artist-`sameAs`, Breadcrumb aus Sprungmarken, SearchAction, unvollständige Playlist |
| Content | Widersprüche „performed“, „DJ-Performance“, „Sets“ entfernt (reines Studioprojekt) |
| Content | Englische Fließtexte ins Deutsche übersetzt: Bio, Mastering, Label-Netzwerk, Sound, Releases, Newsletter, Footer |
| Content | SEO-Jargon aus sichtbaren Labels und Quelltext entfernt („E-E-A-T“, „FEATURED SNIPPET TARGET“, „ENTITY CLUSTER“, „Knowledge Graph fodder“ usw.) |
| Content | Versteckte, keyword-gestopfte H3s entfernt; Section-`aria-label`s auf natürliche Namen umgestellt (Screenreader) |
| Content | Neue Sektion **„Fakten zur Single“** mit Cover und Fakten-Tabelle (Artist, Release, Label, Genre, Story), ideal für KI-Antworten und die Google-Bildersuche |
| Content | 4 neue FAQ: Release-Datum der Single, „Wer steckt hinter Code Chaos?“, „Live/DJ buchbar?“ (Nein), „Was ist Crucible?“; die Mastering-Frage ist neutral statt „der beste“ formuliert |
| Crucible | Neues OG-Bild 1200×630 mit Plugin-Darstellung (`images/crucible-og.jpg`), FAQ-Schema mit sichtbarer FAQ synchronisiert, Organization mit Artist/Person verknüpft |
| GEO | `llms.txt` erweitert: Runtime Terror inkl. Tracklist und BPM, Preise, Polished-Media-Domain, „Booking: nicht verfügbar“, Genre-Typical-BPM |
| Sitemap | `lastmod` aktualisiert, Crucible-Bild ergänzt, Porträt-Eintrag „herofull“ entfernt |
| Recht | Impressum § 5 DDG; Datenschutz: neuer Abschnitt „Eingesetzte Dienste“ (GitHub Pages, lokale Fonts, cdnjs, Formspree, Brevo, Gumroad); Newsletter-Hinweis mit Double-Opt-in und Link zur Datenschutzerklärung |

---

## 3. Keyword-Analyse

Einschätzung der Nachfrage: ●●● hoch für die Nische · ●● mittel · ● klein. Wettbewerb: Musik-Nischen-Keywords haben kaum kommerzielle Konkurrenz, dafür ranken Bandcamp, SoundCloud, YouTube, Beatport und Wikipedia.

### Cluster A: Marke & Releases (höchste Conversion, sicher gewinnbar)
| Keyword | Intent | Nachfrage | Zielseite | Status |
|---|---|---|---|---|
| code chaos, code chaos psytrance, code chaos bandcamp | navigational | ●● | `/` | stark, Entität jetzt sauber |
| uhrwerk aus blut, code chaos uhrwerk aus blut | navigational | ● (ab 30.10. steigend) | `/#single`, `/#single-info` | neu mit Faktenbox |
| runtime terror code chaos | navigational | ● | `/#album-runtime-terror` | ok |
| abstract sound design label | navigational | ● | `/#network` + Label-Website | ok |

### Cluster B: Genre-Informational (Reichweite + GEO-Zitate)
| Keyword (DE / EN) | Intent | Nachfrage | Zielseite |
|---|---|---|---|
| was ist psycore / what is psycore | informational | ●● | `/#was-ist-psycore` |
| hitech psytrance / hi-tech psytrance | informational | ●●● (vor allem EN, BR, MX) | `/#was-ist-hitech`, `/#hitech-psytrance-ultimate` |
| darkpsy / dark psytrance | informational | ●●● (EN) | `/#was-ist-darkpsy` |
| psycore bpm, hitech bpm, darkpsy bpm | informational | ● | `/#bpm-guide` |
| psycore vs hitech, unterschied psycore hitech | informational | ● | `/#genre-vergleich` |

**Wichtig:** Das meiste Suchvolumen für diese Genres ist englisch-, portugiesisch- und spanischsprachig. Auf Deutsch ist die Nachfrage klein. Größter Hebel: eine englische Version (siehe Abschnitt 7).

### Cluster C: Kommerziell (Umsatz)
| Keyword | Intent | Nachfrage | Zielseite |
|---|---|---|---|
| psytrance mastering, psycore mastering, hitech mastering, darkpsy mastering | transactional | ● (aber hoher Wert pro Anfrage) | `/#psycore-mastering`, polished.media |
| mastering service psytrance günstig / online mastering psytrance | transactional | ● | dito |
| multiband saturation plugin, 3 band saturation vst | commercial | ●● (EN) | `/crucible.html` |
| saturation plugin psytrance, best saturation plugin for bass | commercial | ●● (EN) | `/crucible.html` (+ Blog/Tutorial empfohlen) |
| cover art psytrance, lyric video psytrance | transactional | ● | `/#mastering` |

### Cluster D: Long-Tail-Chancen (noch nicht abgedeckt)
- „psytrance bass saturation tutorial“, „how to make psycore kick“, „hitech lead sound design“: Tutorial-Content mit Crucible als Lösung.
- „gothic psytrance“, „deutschsprachiger darkpsy“, „psytrance mit deutschen texten“: passt exakt zur neuen Ära von „Uhrwerk aus Blut“, kaum Konkurrenz.
- „psycore labels“, „hitech psytrance labels deutschland“.

---

## 4. Zielgruppen-Avatare

### Avatar 1: „Mateo, der Hitech-Head“ (Hörer/Fan)
- 22–34, Brasilien, Mexiko, Kolumbien oder Osteuropa; Festival- und Forest-Party-Gänger.
- Hört auf SoundCloud und YouTube, kauft vereinzelt auf Bandcamp (Bandcamp Friday).
- Sucht: neue schnelle, dunkle Tracks, Labels, Tracklists mit BPM.
- Spricht an: Kompromisslosigkeit, BPM-Zahlen, Label-Zugehörigkeit, internationale Releases.
- Kanal: Instagram Reels, TikTok, YouTube, Telegram-Gruppen. **Sprache: Englisch/Spanisch.**
- Ziel auf der Seite: Bandcamp-Kauf, Follow, Newsletter.

### Avatar 2: „Lena, die Gothic-Crossover-Hörerin“ (neu durch „Uhrwerk aus Blut“)
- 25–40, DACH; hört Dark Electro, Darkwave, Industrial, ein bisschen Psytrance.
- Kommt über Story, Ästhetik, deutsche Texte und Artwork, nicht über BPM.
- Sucht: Atmosphäre, Geschichte, Bedeutung hinter dem Track.
- Spricht an: die fünf Szenen, Zitate, Cover, Video-Loop, deutsche Sprache.
- Kanal: Instagram, Spotify-Playlists, YouTube (Visualizer). **Sprache: Deutsch.**
- Ziel: Pre-Save, Spotify-Follow, Newsletter.

### Avatar 3: „Jonas, der Bedroom-Producer“ (Käufer Crucible + Mastering)
- 18–32, weltweit, produziert Hitech, Psycore oder Darkpsy in FL Studio, Ableton oder Bitwig.
- Problem: Tracks klingen leise, matschig, Kick und Bass kämpfen; kein Budget für große Studios.
- Sucht: Tutorials, Presets, Plugins, günstiges Mastering von jemandem aus der Szene.
- Einwände: „Lohnt sich ein weiteres Saturation-Plugin? Ich habe doch schon Saturn/Decapitator.“ und „Wie klingt das konkret?“
- Spricht an: Vorher/Nachher-Audio, kurze Tutorials, Credibility als aktiver Producer, Demo-Version.
- Kanal: YouTube-Tutorials, Reddit (r/psytrance, r/edmproduction), Instagram/TikTok Reels, Discord. **Sprache: Englisch.**
- Ziel: Crucible-Kauf, Mastering-Anfrage.

### Avatar 4: „Kai, der kleine Label-Betreiber“ (B2B, hoher Warenkorb)
- 28–45, betreibt ein Netlabel oder ein kleines Psytrance-Label, 1–4 Releases pro Monat.
- Problem: konsistenter Sound über Releases, Cover und Promo-Videos aus einer Hand.
- Spricht an: Pakete (Pro Release EP €399, Full Release €999), Turnaround, Referenzen.
- Kanal: E-Mail, LinkedIn/Facebook-Gruppen, persönliche Empfehlung. **Sprache: Englisch/Deutsch.**
- Ziel: Paket-Anfrage über das Formular.

### Avatar 5: „Die KI-Suche“ (GEO-Zielgruppe)
- ChatGPT, Perplexity, Gemini, Claude und Google AI Overviews beantworten „Was ist Psycore?“, „Hitech BPM?“, „Mastering für Psytrance?“.
- Braucht: kurze, eindeutige, faktisch korrekte Aussagen; konsistente Entität; strukturierte Daten; `llms.txt`.
- Umgesetzt: Faktenbox, synchronisiertes FAQ-Schema, korrigierte Fakten, `llms.txt`. **Wichtig:** Fakten müssen überall gleich sein (Bandcamp, Socials, Label-Seite), siehe offene Punkte.

---

## 5. GEO (Generative Engine Optimization)

**Stärken:** `robots.txt` erlaubt GPTBot, ClaudeBot, PerplexityBot, Google-Extended usw.; es gibt `llms.txt`, Definitionen, Vergleichstabelle, BPM-Tabellen und FAQ.

**Behoben:** falsche Künstlernamen, widersprüchliche Aussagen (live/Studio), unsaubere Entitäten, keine Fakten-Sektion zur Single.

**Weitere Empfehlungen:**
1. **Zitierfähige Primärquelle sein:** Pro Genre eine eigene URL (`/psycore`, `/hitech-psytrance`, `/darkpsy`) mit Autor, Datum und Quellenangaben. KI-Systeme zitieren eher eigene Seiten als Sprungmarken.
2. **Externe Bestätigung:** Wikidata-Eintrag für „Code Chaos“ (Musiker) und „Abstract Sound Design“ (Label) mit Verweis auf die Website; Discogs- und MusicBrainz-Profile vervollständigen. Das ist der größte Hebel für KI-Entitätserkennung.
3. **Genre-Fakten mit Quellen belegen:** Einige historische Aussagen im Genre Guide (z. B. dass „Osom“ = Kindzadza & Psykovsky den Begriff Hitech geprägt habe, Noise Poison Records als früher Hub, „Slambient“ durch The Endless Knot) sollten mit Quellen geprüft werden. Unsichere Aussagen lieber weicher formulieren.

---

## 6. Crucible: Warum (noch) keine Sales, und was jetzt hilft

### Diagnose
1. **Kein Hörbeispiel.** Für ein Saturation-Plugin ist Audio das wichtigste Verkaufsargument. Es gibt keine Vorher/Nachher-Clips und kein Video.
2. **Kein echtes Produktbild.** Die Seite zeigt ein CSS-Mockup, keinen Screenshot der echten Oberfläche. Das wirkt auf Producer unsicher („gibt es das wirklich?“).
3. **Keine Demo/Trial.** Bei unbekannten Plugin-Marken ist eine Testversion Standard.
4. **Preis:** US$56.76 ist eine ungewöhnliche Zahl (wirkt umgerechnet) und liegt im Bereich etablierter Marken. Ohne Bekanntheit konvertiert ein Einführungspreis (z. B. $29 Launch, später $49) oder Pay-what-you-want-mit-Minimum deutlich besser.
5. **Keine Social Proof:** keine Zitate von anderen Producern, keine Track-Beispiele „mit Crucible gemastert“.
6. **Reichweite:** Auf der Startseite steht Crucible erst nach Mastering. Die Fans der Musik (Avatar 1 & 2) kaufen keine Plugins; Käufer sind Producer (Avatar 3), die anders angesprochen werden müssen (Tutorials).

### Maßnahmen (Priorität)
1. **3 Audio-Demos** (Kick+Bass, Lead, Master-Bus) als Vorher/Nachher, jeweils 10–15 s, auf crucible.html und als Reels.
2. **Echte Screenshots + 60-Sekunden-Walkthrough** (YouTube + Reel), auf crucible.html einbetten.
3. **Launch-Aktion:** zeitlich begrenzter Rabattcode auf Gumroad (z. B. `CHAOS30`), kommuniziert über Newsletter, Instagram und Bandcamp-Community.
4. **Demo-Version** (z. B. mit periodischem Rauschen oder ohne Speichern).
5. **Seeding:** 10–20 Producer aus der Hitech-/Psycore-Szene (Abstract Sound Design, TATEWARI, Soma Ritual) bekommen eine Lizenz gegen ehrliches Feedback bzw. einen Post.
6. **Listings:** KVR Audio Product Database, Plugin Boutique Marketplace, r/AudioProductionDeals, Gearspace (Product Alerts), Bedroom Producers Blog (Pressemitteilung).
7. **Content:** Tutorials „Psytrance Bass Saturation“, „Psycore Kick Processing“ mit Crucible, englisch, YouTube + Blog.

### Social-Automatisierung (vorbereitet)
- Grafiken (1080×1350): `images/social/crucible-out-now.jpg`, `crucible-three-bands.jpg`, `crucible-psycore.jpg`
- Posting-Plan mit Captions und Hashtags: `_marketing/crucible-posts.json` (4 Posts, 07.10.–21.10.2026)
- Posting-Skript Instagram Graph API: `_marketing/post_instagram.py` (liest `INSTAGRAM_ACCESS_TOKEN` und `INSTAGRAM_USER_ID` aus der Umgebung, merkt sich gepostete IDs). TikTok und YouTube über Buffer folgen, sobald die Zugangsdaten in der Umgebung hinterlegt sind.
- Ordner mit `_` werden von GitHub Pages nicht veröffentlicht.

---

## 7. Offene Punkte (brauchen deine Entscheidung oder Info)

1. **Standort:** Bandcamp sagt „from Hamburg“, die Website nur „Deutschland“. Wenn Hamburg stimmt, sollte es überall stehen (Bio, Schema, llms.txt). Das hilft Entität und lokale Suche („Psytrance Producer Hamburg“).
2. **Booking-Widerspruch:** Bandcamp nennt `code.chaos@gmx.de` für Booking, die Website sagt „keine Bookings“. Bitte auf Bandcamp anpassen.
3. **Label-Gründungsjahr:** Die Timeline sagt „2021 Abstract Sound Design Founded“, aber die Releases 2017–2019 sind mit dem Label „Abstract Sound Design“ gekennzeichnet und liegen auf `moonchildproject.bandcamp.com`. Bitte korrekt angeben.
4. **Englische Version** (`/en/`) mit `hreflang`: größter Reichweiten-Hebel, da Avatar 1, 3 und 4 überwiegend englisch suchen.
5. **Eigene Unterseiten** für Genre-Guides und Mastering statt alles auf einer 240-KB-Seite (bessere Rankings je Keyword, bessere KI-Zitierbarkeit).
6. **Font Awesome** (ca. 100 KB CSS + Webfont von cdnjs) für 8 Icons: durch Inline-SVG ersetzen. Dadurch entfällt auch die Cloudflare-Verbindung im Datenschutz.
7. **Repo aufräumen:** ca. 33 MB ungenutzte Bilder (u. a. `runtime-terror-cover.png` 12,6 MB, `runtime-terror-tracklist.png` 10,6 MB, `ASD.png` 5,8 MB, `hero*.png`). Bewusst nicht gelöscht, weil eventuell für Discogs genutzt.
8. **Impressum:** Prüfen lassen, ob ein Verantwortlicher nach § 18 Abs. 2 MStV angegeben werden muss (redaktionelle Inhalte wie der Genre Guide). Das Impressum nennt außerdem Facebook, es gibt aber keinen verlinkten Facebook-Auftritt.
9. **Datenschutz:** Der neue Abschnitt beschreibt die tatsächlich eingebundenen Dienste, ersetzt aber keine Rechtsberatung.

---

## 8. Monitoring nach dem Deploy
- Google Search Console: Sitemap neu einreichen, URL-Prüfung für `/` und `/crucible.html` (Live-Test für strukturierte Daten).
- Rich Results Test / Schema Validator für beide Seiten.
- Bing Webmaster Tools anmelden (Grundlage für ChatGPT-Suche und Copilot).
- Nach 4 Wochen: Brand-Queries, „uhrwerk aus blut“, Crucible-Klicks und Gumroad-Conversion vergleichen.
