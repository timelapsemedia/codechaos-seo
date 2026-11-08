# FROSTFALL – Teil 1 „Das Band“ · Produktionslog

Stand: 08.11.2026 · Skript: `_marketing/serie-frostfall.md` · Pipeline: `_marketing/konzept-story-serie.md` („Produktionspipeline ohne Higgsfield“)
Kanal laut Plan: Polished-Konten. **Nicht gepostet.**

## Dateien in diesem Ordner
| Datei | Inhalt |
|---|---|
| `frostfall_teil-01.mp4` | Hauptfassung (Hook A: „Die Maschine startet von selbst.“) |
| `frostfall_teil-01_hook-B.mp4` | Trial Reel B: Etikett „NIEMALS ABSPIELEN.“ + „Mein Großvater hat mir ein Band hinterlassen. Und ein Verbot.“ |
| `frostfall_teil-01_hook-C.mp4` | Trial Reel C: Frost + Chor in der ersten Sekunde + „Wer dieses Band abspielt, verliert seine Stimme.“ |
| `kontaktbogen.png` | Kontaktbogen der Hauptfassung |
| `endkontrolle.md` | Protokolle der Pflicht-Endkontrolle aller drei Fassungen mit begründeten Freigaben |
| `caption.txt` | Caption-Vorschlag (aus dem Skript) |

Technik: 1080×1920, 30 fps, H.264 High (CRF 18, max. 9 Mbit/s), AAC 256 kb/s, integriert −14 LUFS, True Peak ≤ −1 dBTP.
In Hook C liegt der Produktsound vorn unter der Stimme und wird dort um 10 dB abgesenkt, damit der erste Satz klar verständlich bleibt (erste Kontrolle hatte die Stimme als angeschnitten erkannt).

## Sound der Folge (echt aus dem Produkt gerendert)
- **Quelle:** Hoarfell (Code Chaos Audio, Black Metal Suite), Windows-VST3 aus dem Release-Build der Plugin-CI, Programm **„Choir Ah – Frozen Hall“**.
- **Effekt:** **Rimehall 1.0.0** (Code Chaos Audio, Black Metal Suite, Teil 2), Windows-VST3 aus dem Release-Build der Plugin-CI, Programm **„Ice Shimmer Choir“** (Werkspreset, unverändert).
- **Noten:** D-Moll mit None, gestaffelter Einsatz: D3 (0,00 s) · A3 (0,25 s) · F4 (0,55 s) · E5 (1,10 s), Anschlag 92, gehalten 4,2 s, Hallfahne bis 8 s.
- **Render:** pedalboard 0.9.26, 48 kHz, 24 bit, 1 s Vorlauf gegen Parameterglättung, danach weggeschnitten. Trocken: Spitze −8,1 dBFS. Gefroren: Spitze −10,9 dBFS.
- **Im Video:** gefrorene Fassung ab dem Freeze-Bild (Liv neben der Maschine), Frost wächst über das Bild, Einblendung „Dieser Sound → Link in Bio“ (Rimehall ist auf Gumroad live).
- **Bett unter der Erzählung:** Hoarfell „Choir Uh – Low Drone“ (Dm – B♭ – Gm – A, je 9 s) durch Rimehall „Northern Void“, leise und unter der Stimme abgesenkt. Vor dem Sound-Moment ist es bewusst still.
- Skripte: `tools/sound_frostfall_t01.py`, `tools/betten.py` (Produktionsordner).

## Stimme
- ElevenLabs, Modell `eleven_multilingual_v2`, feste Erzählerstimme **„Tom – Gloomy“** (Voice-ID `xouqnknI7nCiPaJ9gwt8`), Stabilität 0,6, Ähnlichkeit 0,8, Stil 0,15, Tempo 0,92, Seed 4242.
- Jede Zeile einzeln mit vorheriger/nächster Zeile als Kontext, Ränder im Pegelprofil getrimmt (Einzelzeilen, keine Schnitte im Wort).
- Text: deutsche Fassung der Skriptzeilen (Skript liegt auf Englisch vor), Zahlen für die Aussprache ausgeschrieben.

## Bild
- **Figurenblätter:** Liv, Eirik, Rabe (qwen, 9:16), Fehler korrigiert (Eiriks leuchtende Augen).
- **Standbilder:** qwen-edit gegen die Figurenblätter (Liv/Eirik/Rabe), Bandmaschinen-Shots gegen f01 als Maschinenreferenz, Bilder ohne Figur gegen eine leere Stilreferenz (einheitlicher Ölmalerei-Look).
- **Geprüft und neu erzeugt:** Stilbrüche (Comic/Foto statt Malerei: f01, f02, f06, f09), Plattenspieler statt Bandmaschine (f14), andere Maschine (f10, f16), Fantasieschrift (f15), falsches Zählwerk (f20), überzeichnetes Gesicht (f18), Stahl- statt Kupferspule (f11).
- **Text im Bild** wird nie vom Modell gemalt: Etikett „NIEMALS ABSPIELEN.“ und Bandzählwerk 000→001 sind Overlays.
- **Bekannte Abweichung:** Livs Undercut ist nicht in jedem Bild gleich deutlich, Schal, Gesicht und Mantel tragen die Wiedererkennung.
- **Hochskalieren:** Real-ESRGAN x4plus (lokal), danach Shot-Matching im Lab-Raum (Belichtung, Kontrast, Farbstich), gemessen vorher/nachher. Ausnahme: Rückblende f13 bleibt bewusst warm.
- **Bewegung:** 2.5D-Parallax aus Depth-Anything-V2-**Small**-Tiefenkarten (Apache-2.0) für alle Standbilder. Schlüsselmoment „Die Maschine startet von selbst“ als wan-Clip (5 s, Startbild = Standbild). Die zwei weiteren geplanten wan-Clips (Spule startet, Rabe dreht den Kopf) sind in dieser Fassung Parallax, weil das monatliche Gratis-Rechenguthaben erreicht war.
- **Schnitt:** Remotion (code-chaos-motion), Untertitel 2–3 Wörter (Schlüsselwörter eisblau), Teilzähler „TEIL 1“ ab dem zweiten Bild, Frost-Freeze im Sound-Moment, Endkarte „Teil 2 →“.

## KI-Kennzeichnung beim Posten
Bilder und Bewegtbilder sind KI-erzeugt: TikTok „AI-generated content“, Meta „KI-Info“, YouTube „veränderte oder synthetische Inhalte“ setzen. Die Kennzeichnung betrifft nur die Bilder, nicht die Produkte. Im Video gibt es keine Aussage dazu, wie Plugins oder Master entstehen.
