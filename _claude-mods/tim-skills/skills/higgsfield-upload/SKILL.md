---
name: higgsfield-upload
description: Lokale Dateien nach Higgsfield media_upload hochladen, ohne signierte URLs abzutippen (hf_upload.py, curl PUT); liefert media_ids für media_confirm.
---

# higgsfield-upload

Higgsfields `media_upload` liefert pro Datei eine signierte URL von ca. 1.500 Zeichen. Bisher
wurden diese URLs von Hand in `curl -X PUT …` abgetippt, bei 4 Dateien rund 5.800 Zeichen Ausgabe.
Das ist langsam, teuer und fehleranfällig. Das Skript liest die Antwort direkt aus dem Transkript
der laufenden Session und erledigt die PUTs.

**Grenzen:** Lädt nur die genannten Dateien an die signierten Higgsfield-URLs hoch, sonst kein
Netz. Es gibt keine URL und kein Token aus. Es veröffentlicht nichts: Hochgeladene Medien sind
erst einmal privat in Higgsfield. Für Posts gelten weiter die Freigaberegeln der jeweiligen Pipeline.

## Ablauf

1. **Plätze anfragen:** `media_upload` mit `files: [{filename, content_type}, …]`. Die Reihenfolge
   ist wichtig, das Skript ordnet die lokalen Dateien in derselben Reihenfolge zu.
   `content_type` passend zur Endung (`video/mp4`, `image/png`, `image/jpeg`, `audio/mpeg` …).
2. **Hochladen:** gleich danach, ohne die Antwort abzuschreiben:
   ```bash
   python "<Ordner dieses Skills>/hf_upload.py" "D:/pfad/clip1.mp4" "D:/pfad/bild2.png"
   ```
   - Das Skript findet das Transkript über `CLAUDE_CODE_SESSION_ID` (auch in Subagenten). Sonst
     nimmt es das neueste Transkript der letzten 2 Stunden. Bei mehreren parallelen Sessions
     `--transkript <pfad.jsonl>` angeben.
   - `--probe` zeigt nur die Zuordnung Datei → Platz und lädt nichts hoch.
   - Abbruch vor dem Upload, wenn Anzahl, Dateityp oder Größe nicht passen oder die URLs (24 h)
     abgelaufen sind. `--trotzdem` nur bewusst setzen.
3. **Bestätigen:** Das Skript druckt je Medienart eine Zeile
   `media_confirm: {"type": "video", "media_ids": [...]}`. Diese Werte 1:1 an `media_confirm`
   übergeben. Gemischte Arten (Bild + Video) gehen als getrennte Aufrufe oder als `type: "auto"`.
4. **Prüfen:** `media_confirm` muss für jede ID `status: uploaded` melden. Erst dann die IDs in
   `generate_*` oder Presets verwenden.

## Fallen (belegt)

- **403 mit Python-urllib:** Die signierte URL schlägt bei urllib fehl (signierter Header), mit
  curl kommt 200. Deshalb lädt das Skript nur über curl hoch.
- **413 bei großen Dateien:** 533 MB lehnte Higgsfield ab, 317 MB gingen (Zollhaus, 20.10.2026).
  Ab 500 MB warnt das Skript. Für Longform vorher eine Social-Fassung mit niedrigerer Bitrate
  rendern, nicht den Master hochladen.
- **„Media input not found“ nach Kontowechsel:** Media-IDs gehören zum Higgsfield-Konto. Nach einem
  Konnektor- oder Kontowechsel neu hochladen, alte IDs aus Konfigurationsdateien gelten nicht mehr.
- **Cloud-Session/Sandbox:** PUT dort ausführen, wo die Bytes liegen. Dateien auf Tims Rechner nur aus
  einer lokalen Session hochladen, Bytes nie zwischen Umgebungen hin- und herschieben.

## Test

`hf_upload.py` wurde gegen einen lokalen PUT-Server getestet: 2 Dateien → 200 und richtige
media_confirm-Zeilen, keine URL in der Ausgabe; vertauschte Reihenfolge (Typ passt nicht) →
Abbruch; falsche Anzahl → Abbruch; 403 → einmal wiederholt, Exit 1; `--probe` lädt nichts hoch.
Gegen ein echtes Transkript vom 10.10.: 3 Plätze erkannt, abgelaufene URLs gemeldet.
