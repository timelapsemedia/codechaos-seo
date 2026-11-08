# LAST RAVE – Teil 1 „220 BPM“ · Produktionslog

Stand: 08.11.2026 · Skript: `_marketing/serie-last-rave.md` · Pipeline: `_marketing/konzept-story-serie.md` („Produktionspipeline ohne Higgsfield“)
Kanal laut Plan: Code-Chaos-Konten. **Nicht gepostet.**

## Dateien in diesem Ordner
| Datei | Inhalt |
|---|---|
| `last-rave_teil-01.mp4` | Hauptfassung (Hook A: „Um 2:20 leuchten alle Fenster im Block auf.“) |
| `last-rave_teil-01_hook-B.mp4` | Trial Reel B: Plakat „MAX. 120 BPM. FÜR IHRE RUHE.“ + „In meiner Stadt ist schnelle Musik seit 2041 verboten.“ |
| `last-rave_teil-01_hook-C.mp4` | Trial Reel C: FM-Lead + BPM-Strobe in der ersten Sekunde + „Diese Frequenz bringt alle zum Tanzen. Bis zum Sonnenaufgang.“ |
| `kontaktbogen.png` | Kontaktbogen der Hauptfassung |
| `endkontrolle.md` | Protokolle der Pflicht-Endkontrolle aller drei Fassungen mit begründeten Freigaben |
| `caption.txt` | Caption-Vorschlag (aus dem Skript, mit Strobe-Hinweis) |

Technik: 1080×1920, 30 fps, H.264 High (CRF 18, max. 9 Mbit/s), AAC 256 kb/s, integriert −14 LUFS, True Peak ≤ −1 dBTP.
In Hook C liegt der Produktsound vorn unter der Stimme und wird dort um 10 dB abgesenkt, damit der erste Satz klar verständlich bleibt (erste Kontrolle hatte die Stimme als angeschnitten erkannt).

## Sound der Folge (echt aus dem Produkt gerendert)
- **Quelle:** **Chaos FM** (Code Chaos Audio), installierte Windows-VST3 (`Chaos FM.vst3`, Stand 20.10.2026).
- **Programme (Werkspresets, unverändert):** Ruf in Takt 1+3 **„Hitech Scream Lead“**, Antwort in Takt 2+4 **„Laser Lead“**, darunter leise **„Rolling Psy Bass“** (Rolling-Sechzehntel auf E1, 9 dB unter dem Lead).
- **Musik:** 220 BPM, E-Phrygisch, 4 Takte Sechzehntel, Gate 80 %, Anschlag 100. Takt 4 steigt bis E5 („das Tempo steigt“). Noten im Skript `tools/sound_lastrave_t01.py`.
- **Render:** pedalboard 0.9.26, 48 kHz, 24 bit, getrennte Instanzen je Programm (keine Programmwechsel-Glättung), Summe auf −1 dBFS Spitze, 5,56 s.
- **Im Video:** Sound-Moment mit Strobe im BPM-Raster (halbe Zeit, ca. 1,8 Blitze/s, Deckkraft ≤ 30 %), Einblendung „Dieser Sound → Link in Bio“ (Chaos FM ist auf Gumroad live).
- **Bett:** derselbe Puls aus Chaos FM („Sub Thump Bass“ auf den Vierteln + „Rolling Psy Bass“), 8-Takt-Loop, Tiefpass 260 Hz („durch die Wände“). Er steigt ab „Heute Nacht knistern seine Kopfhörer“ an und bricht bei „Um 6 Uhr ist es vorbei“ schlagartig ab, nur der Regen bleibt.

## Stimme
- ElevenLabs, Modell `eleven_multilingual_v2`, feste Erzählerstimme **„Manuel – Profound, Deep“** (Voice-ID `JH302OKVzGGJc47f08ex`), Stabilität 0,6, Ähnlichkeit 0,8, Stil 0,15, Tempo 1,0, Seed 4242.
- Zeilen einzeln mit Kontext, Ränder im Pegelprofil getrimmt. Deutsche Fassung der Skriptzeilen, Zahlen ausgeschrieben („zwei Uhr zwanzig“, „hundertzwanzig BPM“).

## Bild
- **Figurenblätter:** Kai, Mira, Ruhe-Patrouille (qwen, 9:16). Korrigiert: Apple-Logo, Converse-/Nike-Zeichen und Kratzer bei Kai, Dienstmarke, Ärmelabzeichen und Fantasietext bei der Patrouille.
- **Standbilder:** qwen-edit gegen die Figurenblätter (Kai, Patrouille), Bilder ohne Figur gegen eine leere Stilreferenz (einheitlicher Graphic-Novel-Look mit Tuschekonturen).
- **Geprüft und neu erzeugt:** Ölmalerei statt Graphic Novel (r01, r02, …), Funken im Gesicht statt an den Kopfhörern (r06), Karateanzüge und Lächeln statt Schlafanzug und Leerblick (r10), Schreie bzw. Maskengesichter statt Leerblick (r11), Fantasieschrift auf Plakat und Display (r03, r07), eingestecktes Kabel trotz „kein Kabel steckt“ (r07), noch beleuchtete Fenster (r17).
- **Text im Bild** nur als Overlay: „220.0“ (Radio), Plakat „MAX. 120 BPM. FÜR IHRE RUHE.“, „BPM 200“, „IN 220.0“, „REC“, „LAST_RAVE.wav · 220 BPM“.
- **Hochskalieren:** Real-ESRGAN x4plus (lokal), danach Shot-Matching im Lab-Raum, gemessen vorher/nachher.
- **Bewegung:** 2.5D-Parallax aus Depth-Anything-V2-**Small**-Tiefenkarten (Apache-2.0), dazu Fenster-Puls im BPM-Raster (Szene 1), Funken-Flackern (Kopfhörer) und Strobe (Sound-Moment). Die drei geplanten wan-Clips (Fenster, Funken, Tanz) sind in dieser Fassung Parallax plus Effekt, weil das monatliche Gratis-Rechenguthaben erreicht war.
- **Schnitt:** Remotion (code-chaos-motion), Untertitel 2–3 Wörter (Schlüsselwörter kupfer), Teilzähler „TEIL 1“ ab dem zweiten Bild, Endkarte „Teil 2 →“.

## Hinweise fürs Posten
- **Strobe:** Erste Caption-Zeile oder Ende der Caption: „⚠️ Enthält Lichtblitze.“ (Skript-Checkliste).
- **KI-Kennzeichnung:** Bilder sind KI-erzeugt, Plattform-Kennzeichnung setzen; Code-Chaos-Texthinweis nur „Bild mit KI erstellt“. Keine Aussage dazu, wie Plugins entstehen.
