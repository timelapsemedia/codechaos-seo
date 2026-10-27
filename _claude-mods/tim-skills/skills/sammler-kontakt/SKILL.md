---
name: sammler-kontakt
description: >-
  Seltene Tonträger von privaten Sammlern bekommen und Herkunft klären: Anfrage, Preisverhandlung, sichere Bezahlung, Rip-Bitte, Zeitzeugen. Bei "was antworte ich dem Sammler", "Demotape kaufen", "in der Mitte treffen". Entwirft nur.
---

# sammler-kontakt

Ergänzt den Mod `raritaeten-jaeger` (Suche, Suchgedächtnis, Fundliste) um den menschlichen
Teil: Besitzer gefunden, was jetzt? Ziel ist **immer das physische Exemplar**. Ein
verlustfreier Rip mit Scans ist ein Zwischenziel, keine Endstation.

**Grenzen:** Der Skill entwirft Texte und schlägt nächste Schritte vor. Er sendet nichts,
loggt sich nirgends ein und bezahlt nichts. Senden und Bezahlen erledigt der Nutzer selbst.
Höchstens wird ein Entwurf auf Zuruf über den Browser eingefügt, und zwar jede Nachricht
einzeln freigegeben. Private Namen, Preise und Chatverläufe bleiben in der lokalen
Lead-Liste des Projekts und kommen nie in Repos, Skills oder öffentliche Texte.

## 1. Lage klären (vor jedem Entwurf)

Aus Lead-Liste, Chatverlauf und Memory zusammentragen:
- **Wer:** Sammler, Händler, Zeitzeuge oder Bandumfeld? Verkauft die Person aktiv, löst sie
  eine Sammlung auf, oder ist sie nur „vielleicht später“ bereit?
- **Was genau:** Titel, Format, Auflage, Zustand, Fotos vorhanden? Ist es wirklich das
  gesuchte Stück? Varianten wie Advance, Vorab, andere Tracklist oder Nachpressung prüfen.
- **Stand:** letzte Nachricht von wem, wann, und welche Frage noch offen ist.
- **Was der Nutzer schon besitzt** (digital oder physisch): Das verändert den Hebel.
- **Wen der Nutzer bewusst nicht fragen will,** z. B. weil ein Fund eine Überraschung sein
  soll. Das im Lead-Status vermerken und respektieren, ohne daraus ein Geheimnis zu machen.

## 2. Wie Sammler ticken (Hebel)

- Sammler geben ungern an Händler ab, **lieber an jemanden, der das Stück schätzt.** Den
  eigenen Bezug kurz und echt erzählen: seit wann man die Band hört, was einem gerade dieses
  Stück bedeutet. Keine Rührstücke.
- **Gegenleistung statt Druck:** die Suchliste des Sammlers mitüberwachen, Tausch,
  Rip-Kopie, Infos aus der eigenen Recherche teilen, Paket- und Versandfragen abnehmen.
- **Seltenheit ehrlich anerkennen.** Den Preis drückt man mit Belegen, nicht indem man das
  Stück kleinredet.
- **Vorkaufsrecht statt Kauf**, wenn die Person (noch) nicht verkaufen will: „Falls du je
  verkaufst, wäre ich gern der Erste.“ Dazu einen Termin zum Nachfassen setzen.
- **Geduld:** Nachfassen frühestens nach 10–14 Tagen, höchstens zweimal ohne Antwort. Danach
  ruht der Lead mit einem Datum zum Wiedervorlegen (z. B. „Auflösung 2027“) und wird nicht
  totgeschrieben.

## 3. Preis verhandeln

1. **Referenzpreise belegen:** Discogs-Verkaufshistorie (nicht die Angebotspreise),
   have/want, gleiche Aufnahmen auf anderer Auflage, Zustand. Quelle und Datum notieren.
2. **Ziel und Obergrenze festlegen**, bevor man schreibt. Die Obergrenze bleibt intern.
3. **Gebotsleiter rechnen:**
   ```
   python preisanker.py --ziel <Wunsch> --max <Obergrenze> [--gebot <bisher>] --referenz <Preise …> [--inkl-versand]
   ```
   Die Zugeständnisse werden kleiner (50 % / 30 % / 20 % der Lücke). Das signalisiert, dass
   die Grenze naht.
4. **Regeln:**
   - Nie eine Spanne nennen („zwischen 150 und 250“). Der Gegenüber hört nur die obere Zahl.
   - Jede Stufe nur gegen etwas: neue Info, Gegenleistung, Versand inklusive, schnelle Zahlung.
   - „In der Mitte treffen“ nur anbieten, wenn die Mitte unter der Obergrenze liegt.
     Sonst konkret eine eigene Zahl nennen.
   - Nach dem letzten Wort nicht weiter erhöhen. Freundlich offenlassen, Vorkaufsrecht erbitten.
   - Schweigt der Verkäufer nach einem Gebot, nicht gegen sich selbst nachbieten. Erst
     nachfragen, dann die nächste Stufe mit Gegenleistung verknüpfen.

## 4. Sicher bezahlen und versenden

- Bei Personen, die man nicht kennt: **PayPal „Waren und Dienstleistungen“** (Käuferschutz)
  oder die Bezahlfunktion der Plattform (z. B. „Sicher bezahlen“ bei Kleinanzeigen).
  **Nie „Freunde und Familie“ und keine Vorab-Überweisung** an Unbekannte, auch nicht bei
  gutem Gefühl.
- Überweisung nur bei bekannten Personen mit Vorgeschichte (Discogs-Bewertungen, frühere
  Käufe) oder bei Abholung bzw. Übergabe.
- Versand versichert und mit Sendungsnummer. Bei Kassetten: Hülle polstern, J-Card nicht
  knicken. Lieber Paket als Warensendung.
- Vor dem Bezahlen Fotos vom echten Exemplar erbitten: Cover, Inlay innen, Tapeschale bzw.
  CD-Ring, Matrix.

## 5. Rip und Scans erbitten (Zwischenziel oder Provenienz-Beleg)

Will jemand nicht verkaufen, aber teilen, freundlich um genau das bitten:
- **CD:** EAC (Windows) oder XLD (Mac) im sicheren Modus, FLAC, mit Log- und Cue-Datei.
- **Tape:** WAV 24 bit / 96 kHz, ohne Rauschunterdrückung und ohne Nachbearbeitung.
  Beide Seiten komplett, inklusive Pausen.
- **Scans:** 600 dpi, unbearbeitet (PNG oder TIFF): Vorder- und Rückseite, Inlay innen,
  Schale bzw. CD-Label.
- Anbieten, die Kosten zu übernehmen (Porto für Hin- und Rückversand an ein Studio). Nicht
  drängeln: Qualität geht vor Tempo.

## 6. Provenienz über Zeitzeugen

Kette von außen nach innen: Musik- und Szene-Lexika, Clubs und Veranstalter der Zeit, Labels
und Vertriebe, Studios, Fanzines, Radiomacher, Fotografen, frühere Mitmusiker.
- **Jede Anfrage:** was man schon weiß (1–2 Sätze), **eine** konkrete Frage, ein Angebot
  (z. B. die eigenen Funde teilen). Keine Fragebögen.
- **Tipps von Kontakten** sofort als neuer Lead mit Quelle erfassen („Hinweis von X am
  <Datum>“) und dem Tippgeber kurz danken. Kommt etwas dabei heraus, ihm berichten. Das
  hält die Kette warm.
- Fakten nur mit Beleg in die Lead-Liste. Gerüchte als „ungeprüft, Quelle X“ markieren.

## 7. Texte schreiben

- In der Stimme des Nutzers, kurz, ohne Floskeln. Die Anrede (Du/Sie) folgt dem
  Gegenüber; mit `du-sie-check` prüfen.
- Vor der Ausgabe durch `humanizer-de` (bzw. `ig-human`).
- **Bei Überarbeitungen nur den genannten Teil ändern.** Alles andere bleibt wortgleich.
- Ausgabe: der Entwurf, darunter ein Satz zur Absicht („hält den Lead warm, nennt keine
  Zahl“) und der nächste Schritt mit Datum.

## 8. Lead-Liste pflegen

Pro Lead eine Zeile: Person (Plattform/Kanal), Objekt, Status (angefragt / verhandelt /
ruht bis <Datum> / gekauft / Sackgasse), letzter Kontakt, nächster Schritt mit Datum, Notiz
zu Hebel bzw. Gegenleistung. Gekauftes erst als Besitz markieren, wenn das Stück da ist.
Bis dahin weitersuchen.
