---
name: agenten-schwarm
description: >-
  Vorlagen für Multi-Agenten-Arbeit in Tims Bereichen: Track-QA über mehrere
  Tracks, Video-QA über viele Clips, breite Recherche mit unabhängiger
  Gegenprüfung (zweiter Agent oder Codex). Nutzen, wenn eine Aufgabe groß und
  teilbar ist ("prüf alle Tracks der EP", "Endkontrolle für alle Reels",
  "recherchiere breit", "Agentenschwarm", "parallel prüfen", "mit Gegenprüfung"),
  oder bevor ein Workflow geschrieben wird. Legt Agentenzahl und Aufwand vorab
  offen und übernimmt nur belegte Ergebnisse.
---

# agenten-schwarm

Große, teilbare Aufgaben laufen als Schwarm: mehrere Agenten arbeiten parallel, ein
unabhängiger Prüfer bestätigt oder verwirft jeden Befund. Ins Ergebnis kommt nur, was ein
Beleg stützt. Der Skill ist eine Arbeitsanleitung. Er startet selbst nichts.

## 1. Lohnt sich ein Schwarm?

Nur wenn **alles** zutrifft:
- Die Aufgabe zerfällt in **mindestens 3 unabhängige Teile** (Tracks, Clips, Quellen, Dateien).
- Jeder Teil lässt sich **ohne gemeinsamen Zustand** bearbeiten. Kein Teil schreibt in dieselbe
  Datei, dasselbe Ableton-Set oder dieselbe Resolve-Timeline wie ein anderer.
- Ein Fehler kostet etwas: Kundenauftrag, Veröffentlichung, Auslieferung oder Geld.

Sonst gilt: allein und nacheinander arbeiten. Kleine Aufgaben nicht aufblasen.
Abhängigkeitsketten laufen immer nacheinander, z. B. „erst Master, dann Hörprobe aus dem Master“.

## 2. Vor dem Start (Pflicht)

1. **Agentenzahl und Aufwand nennen:** „N Arbeits-Agenten + M Prüfer, grob X Minuten“.
   Richtwert: unter 10 Agenten.
2. **Werkzeug wählen:**
   - `Workflow`-Tool nur bei ausdrücklichem Opt-in des Nutzers, in eigenen Worten im Chat
     („nimm einen Workflow“, „ultracode“) oder durch eine Skill-Anweisung, die das verlangt.
     Vor dem Schreiben des Skripts den Skill `workflow-authoring` laden.
   - Ohne Opt-in: mehrere `Agent`-Aufrufe in **einer** Nachricht, damit sie parallel laufen.
   - Gegenprüfung durch ein zweites Modell: `/codex:adversarial-review` oder `/codex:review`
     (Plugin `codex@openai-codex`; das frühere MCP `codex-bridge` ist seit 20.10.2026 entfernt). **Keine Schlüssel und keine Kundendaten an Codex.**
   - Rechenlast (Transkription, Alignment, viele Renders): Modal. Vorher
     `modal billing summary --json` prüfen. Pro Monat höchstens die Free Credits verbrauchen.
3. **Modell nie selbst wechseln oder vorschlagen.** Das Modell wählt Tim.
4. **Ressourcen prüfen:** RAM, Laufwerke, GPU und laufende Jobs anderer Sessions.
   Mehr als 2 lokale Audio- oder Video-Worker parallel nur, wenn der Speicher reicht.

## 3. Grundmuster: Arbeiten → Gegenprüfen → nur Belegtes übernehmen

```
Teile ──► Arbeits-Agent je Teil ──► Befunde (Datei, Stelle, Messwert, Beleg)
                                      │
                                      ▼
                          Prüfer je Befund (unabhängig, adversarial:
                          „versuche den Befund zu widerlegen“)
                                      │
                    BESTÄTIGT ◄───────┴───────► VERWORFEN / UNKLAR
                        │                           │
                  ins Ergebnis              im Bericht als „nicht bestätigt,
                                            geprüft in <Ort>“ markieren
```

Regeln für jeden Arbeits-Agenten (in den Prompt schreiben):
- Ein Befund braucht **Ort + Messwert/Zitat + Werkzeug**, z. B. „Track 3, 1:42–1:50,
  LUFS-S −7,1 gegen Ziel −9 (ffmpeg ebur128)“. Ohne Beleg gilt er nicht als Befund.
- Nur lesen und messen. **Schreiben, Rendern oder Veröffentlichen nur im Hauptstrang**, nach
  der Gegenprüfung. Abgenommene Versionen nie anfassen.
- Strukturierte Antwort (Liste mit `datei`, `stelle`, `befund`, `beleg`, `schwere`), damit
  der Prüfer sie Punkt für Punkt angehen kann.

Regeln für den Prüfer:
- Bekommt den Befund, **nicht** die Begründung des Arbeits-Agenten. So bleibt er unbeeinflusst.
- Misst selbst nach, mit einem anderen Werkzeug oder an der Quelle.
- Gibt `BESTÄTIGT`, `VERWORFEN` oder `UNKLAR` mit eigenem Beleg zurück.
- Ein Gemini-Ohr oder ein anderes Sprachmodell als Hörer entscheidet nie allein. Es ist
  suggestibel. Ausschlaggebend sind Messung und Spektrogramm.

## 4. Vorlagen

### A. Track-QA (EP, Album, Remix-Serie)
- **Teile:** ein Agent je Track.
- **Auftrag je Track:** Integrated LUFS, True Peak, LRA, Spektralbalance gegen die
  Genre-Referenz, Kick-/Bass-Phase und Grundton, Clipping, DC sowie Stille am Anfang und Ende.
  Vorhandene Werkzeuge des Projekts nutzen (z. B. Referenzvergleich, Fenster-A/B), nichts
  nachbauen.
- **Gegenprüfung:** Ein Prüfer nimmt sich jeden Befund mit Schwere „hoch“ vor und misst
  ihn an der Stelle selbst nach.
- **Abschluss:** Eine Tabelle über alle Tracks. Hörproben stehen an der Stelle mit dem
  **größten gemessenen Unterschied**.

### B. Video-QA (viele Reels, Clips, Shorts)
- **Teile:** ein Agent je Clip.
- **Auftrag je Clip:** Endkontrolle (`videokontrolle.py`) und Kanten-Gate (`kanten_mms.py`)
  auf alle Schnittzeiten. Dazu Social-Media-Regeln (Hook ≤ 1,5 s, Re-Hooks, CTA, Safe Zones,
  Captions 4–7 Wörter, < 60 s) und Bildwerte je Einstellung (Belichtung, Kontrast,
  Sättigung, Weißabgleich).
- **Gegenprüfung:** Ein Prüfer hört jeden Befund isoliert ab und prüft am Wortende das
  Bandprofil. Ein wiederholter Whisper-Befund an derselben Kante gilt als ernst.
- **Abschluss:** Pro Clip „frei“ oder „korrigieren: …“. Ohne bestandene Endkontrolle wird
  nichts ausgeliefert.

### C. Recherche mit Gegenprüfung (Provenienz, Markt, Fakten)
- **Teile:** ein Agent je Quelle oder Suchrichtung (z. B. Discogs, Archive und Fanzines,
  Foren, Händler, Presse). Bei einfacher Recherche 2–3 Agenten, bei breiter Recherche bis 6.
- **Auftrag:** Jede Aussage mit URL, Datum und wörtlichem Kurzzitat (≤ 15 Wörter).
  Vermutungen als solche kennzeichnen.
- **Gegenprüfung:** Ein Prüfer (oder Codex) prüft jede Kernaussage an der Originalquelle.
  Bei DRUWIDS gelten als Quellen nur druwids.com und fliegenpilz-onlineshop.de.
- **Abschluss:** Belegte Aussagen getrennt von offenen Fragen. Nichts automatisch in
  Watchlists oder Pläne übernehmen. Tim entscheidet.

### D. Code-Änderung mit Zweitmeinung
- **Teile:** ein Agent setzt um, ein zweiter schreibt Tests, Codex macht ein Review.
- Nur Unabhängiges parallel. Sonst nacheinander in dünnen Scheiben.

## 5. Skelett für ein Workflow-Skript (nur nach Opt-in)

Die genaue API steht im Skill `workflow-authoring`. Vorher laden. Die Form:

```js
export const meta = {
  name: 'track-qa',
  description: 'Alle Tracks messen, jeden Befund unabhängig gegenprüfen',
  phases: [{ title: 'Messen' }, { title: 'Gegenprüfen' }],
}
const tracks = args            // Liste absoluter Pfade, als JSON-Array übergeben
const ergebnisse = await pipeline(
  tracks,
  t => agent(`Miss ${t} … gib Befunde mit Ort+Messwert+Werkzeug zurück`,
             { label: `messen:${t}`, phase: 'Messen', schema: BEFUNDE }),
  r => parallel(r.befunde.map(b => () =>
         agent(`Versuche zu widerlegen: ${b.befund} (${b.datei}, ${b.stelle})`,
               { label: `pruefen:${b.datei}`, phase: 'Gegenprüfen', schema: URTEIL })
           .then(u => ({ ...b, urteil: u })))),
)
return { bestaetigt: ergebnisse.flat().filter(b => b?.urteil?.status === 'BESTÄTIGT') }
```

## 6. Bericht

Lange Läufe enden mit drei Punkten:
- **Brauche dich:** Entscheidungen, Freigaben, alles mit Außenwirkung.
- **Geändert:** was im Hauptstrang wirklich geschrieben, gerendert oder umgestellt wurde.
- **Gefunden:** bestätigte Befunde mit Beleg. Danach die nicht bestätigten mit dem Ort, an
  dem geprüft wurde.

Außerdem: Agentenzahl tatsächlich gegenüber geplant, und was die Gegenprüfung verworfen hat.
Wenn die Prüfer viel verworfen haben, ist der Arbeits-Prompt zu ungenau. Dann diese Vorlage
nachschärfen.
