---
name: aufhaenger-check
description: Faktencheck für Hook, Cold Open, Thumbnail-Text, Titel und Caption-Einstieg; holt den vollen Quellsatz zum Zitat (quellsatz.py) und prüft, ob die Aussage ohne Kontext dasselbe behauptet.
---

# aufhaenger-check

Ein viraler Aufhänger darf zuspitzen, aber nichts Falsches behaupten. Beim Zollhaus (ZeitSprung,
19.10.2026) hieß der Hook „Hier brannte noch Licht“. Im vollen Satz ging es um die Zeit, als der
Wirt dort noch wohnte. Ohne Kontext klang es nach Licht im verlassenen Haus. Tim: „da brannte nicht
noch licht … das stimmt nicht“. Danach mussten Hook, Thumbnail, Cold Open und Captions neu gemacht
werden. Die Prüfung gehört deshalb vor die Freigabe, nicht danach.

## Ablauf

1. **Aufhänger sammeln:** alle Texte, die ohne Video-Kontext wirken: Hook (gesprochen und als
   Text), Thumbnail-Text, Titel, erste Caption-Zeile, Short-Titel, Teaser, Kapitelnamen.
2. **Quellsatz holen:** mit dem Transkript der Quelle (SRT, VTT, Whisper-JSON oder Text):
   ```bash
   python "<Ordner dieses Skills>/quellsatz.py" quelle.srt "Hook 1" "Thumbnail-Text" "Titel"
   ```
   Das Skript zeigt je Aufhänger den ganzen Satz mit Zeitmarke, dazu den Satz davor und danach.
   Meldet es „KEIN QUELLSATZ“ oder „NUR SCHWACHE ÜBEREINSTIMMUNG“, ist die Aussage eine eigene
   Behauptung. Dann braucht sie einen anderen Beleg, z. B. Shopseite, Archiv oder Recherche.
   Wortlaut-Zweifel immer auf der Rohquelle klären (mehrere Whisper-Fenster), nicht auf einem
   geschnittenen Stem.
3. **Drei Fragen je Aufhänger, schriftlich beantworten:**
   - **Was glaubt der Zuschauer ohne Kontext?** Einen Satz formulieren, als hätte man nur das
     Thumbnail gesehen.
   - **Was sagt die Quelle im vollen Satz?** Wer, wann, worauf bezogen. Achte auf Zeitform
     („noch“, „damals“), Bezug („sein“, „hier“) und Einschränkungen („manchmal“, „angeblich“).
   - **Stimmt beides überein?** Zuspitzen ist erlaubt, etwa Kürzen, Neugierlücke oder starkes Bild.
     Nicht erlaubt: ein Ereignis erfinden (Spuk, Licht, Leiche), Zeitebenen vertauschen, eine
     Vermutung als Tatsache darstellen oder ein Zitat jemand anderem zuschreiben.
4. **Ergebnis:** je Aufhänger `ok`, `umformulieren` (mit neuem Vorschlag, der genauso klickstark
   ist) oder `streichen`. Neugier lieber aus echten Details bauen: „Die Zeit blieb stehen“ statt
   „Hier brannte noch Licht“.

## Grenzen und Zusammenspiel

- Ersetzt keine Pflichtprüfungen. DRUWIDS: Konsum-Gate und Compliance aus `druwids-social-operator`.
  Mitragyna: Compliance-Gate der Routine. Videos: Endkontrolle. Diese laufen zusätzlich.
- Historische Bilder, die als Beleg gezeigt werden (Postkarten, Fotos), nicht per KI „verbessern“.
  Ein Thumbnail aus solchen Bildern darf nichts zeigen, was im Original fehlt.
- Das Skript liest nur lokale Dateien und hat kein Netz. Es entscheidet nichts allein: Die drei
  Fragen beantwortet der Mensch bzw. Claude anhand des gefundenen Satzes.

## Test

`quellsatz.py` mit Beispiel-SRT (Satz über zwei Untertitel verteilt, Zeitmarken 00:04,6 und 01:02)
und Whisper-JSON geprüft. Ergebnisse: „Hier brannte noch Licht“ findet den vollen Satz „Als der
Wirt noch hier wohnte, hier brannte noch Licht bis spät in die Nacht …“ mit richtiger Startzeit.
„Hier spukt es nachts“ wird als „nur schwache Übereinstimmung“ gemeldet. Der JSON-Pfad liefert
die Segmentzeit.
