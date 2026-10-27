---
name: rohschnitt-davinci
description: >-
  Rohschnitt aus dem Transkript als EDL für DaVinci Resolve/Premiere: Stille, Füllwörter (äh, ähm, also, um) und verpatzte Takes raus. Bei "Rohschnitt", "Pausen rausschneiden", "Podcast schneiden", "Silence Remover".
---

# rohschnitt-davinci

DaVinci-Gegenstück zu Premiere-Plugins wie „AutoEdit“: Das Transkript bestimmt den Schnitt,
das Ergebnis ist eine **EDL-Timeline**, die in Resolve als bearbeitbarer Rohschnitt landet.
Ergänzt `yt-edit` (nur Liste, nur englische Füllwörter) um deutsche Füllwörter und den Import.

**Grenzen:** Erzeugt nur eine Textdatei (EDL). Originalclips bleiben unangetastet. Kein Netz.
Was gut klingt, entscheidet am Ende das Ohr: der Rohschnitt ist ein Vorschlag, kein Endschnitt.

## Ablauf

1. **Transkript mit Zeitmarken** besorgen (Wortebene ist nicht nötig, Satzebene reicht):
   - Mod `video-werkstatt` → `transkribieren` (Whisper) liefert .srt/.json, oder
   - DaVinci: Clip in Timeline → *Untertitel aus Audio erstellen* → als .srt exportieren.
2. **Probelauf ansehen:** `python3 rohschnitt.py transkript.srt --clip <Clipname> --nur-liste`
   Die Liste Tim zeigen (PAUSE / FUELL / NEU mit Zeiten). Bei Musik-, Performance- oder
   Szenen mit gewollter Stille die Pausen-Schwelle hoch (`--pause 1.5`) oder den Abschnitt ausnehmen.
3. **EDL schreiben:** `python3 rohschnitt.py transkript.srt --clip <Clipname> --fps <fps>`
   - `--clip` exakt wie der Clip im Media Pool heißt (mit Endung).
   - `--fps` wie das Projekt (25 bei PAL-Material, sonst 30/50/60; nur ganze Zahlen).
   - `--quell-tc` setzen, wenn der Clip nicht bei 00:00:00:00 beginnt (Kamera-Timecode,
     in Resolve unter Clip-Attribute/Metadaten „Start TC“).
   - `--rand 0.15` lässt an jeder Kante 0,15 s Luft – kleiner = straffer, größer = natürlicher.
4. **In DaVinci importieren:** Clip in den Media Pool legen →
   *Datei > Importieren > Timeline > AAF, EDL, XML importieren…* → EDL wählen →
   Haken bei „Automatically import source clips into media pool“ entfernen (Clip ist schon da).
   Ergebnis: neue Timeline „Rohschnitt <Clip>“ mit allen behaltenen Stücken hintereinander.
5. **Nachkontrolle:** Schnittstellen anhören (oder `earshot`), Sprünge im Bild mit
   Zooms/B-Roll kaschieren. Für Shorts danach `shorts` oder `yt-edit`/`ig-repurpose`.

## Grenzen der Erkennung

- „NEU“ erkennt Neuansätze, wenn die ersten 4 Wörter gleich sind. Umformulierte Wiederholungen
  findet es nicht – die Liste aus Schritt 2 lesen und bei Bedarf von Hand ergänzen.
- Füllwörter werden nur geschnitten, wenn ein Untertitel-Abschnitt **nur** aus Füllwörtern besteht.
  Ein „äh“ mitten im Satz bleibt (sonst klingt es zerhackt).
- Mehrkamera: EDL gilt für einen Clip. Bei synchronisierten Spuren erst in Resolve einen
  Multicam-/Compound-Clip bauen und dessen Namen als `--clip` nehmen.
- Fps mit Nachkomma (23,976/29,97) werden auf ganze Zahlen gerundet – bei solchem Material
  die Timeline vor dem Import auf 24/30 non-drop stellen oder das Ergebnis prüfen.
