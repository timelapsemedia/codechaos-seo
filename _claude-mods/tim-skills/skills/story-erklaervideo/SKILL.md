---
name: story-erklaervideo
description: Story-geführtes Erklär-/Lernvideo (Motion Graphics) – ein schwieriges Thema über eine Geschichte statt über lose Fakten erklären, mit Hook-Frage, Mechanismus, Aha und Auflösung; Szenenformat, Übergänge, die Beziehungen erklären, Sprecher-/Sound-Regeln, Qualitätscheck. Nutzen für Erklärvideos, Wissens-Reels, „erklär mal …“, Botanik/Kultur/Geschichte-Content (z. B. DRUWIDS-Säule 1), Explainer, Lernanimationen.
---

# Story-Erklärvideo (Vorlage „paper-explainer“, Opus 5.5)

Quelle: Prompt-Vorlage „Story-led educational animation“ (paper-explainer.prompt), von Tim am 2026-10-10 als globales Wissen übernommen. Ich habe sie auf Deutsch, auf Tims Werkzeuge und auf seine Regeln übertragen. Bauen mit hyperframes (GSAP/Canvas) oder EffectCraft (Skill `motion-reels`). Siehe dort auch „Regie-Briefing“.

## Auftrag (Platzhalter füllen)
- **Rolle:** Senior Motion Director und Lern-Storyteller.
- **Ziel:** [THEMA] für [PUBLIKUM] als vollständige visuelle Lektion. Bei Reels sind das 45–90 s in 9:16, sonst 75–90 s in 16:9.
- **Lernziel:** Am Ende versteht man [KERNIDEE], ihre Ursache, ihre Folge und einen verbreiteten Irrtum. Nur so viel Fachsprache wie dafür nötig.

## Visuelles System (Beispiel-Stil, je Marke anpassen)
- **Look:** gerissenes Papier, trockene Gouache, Kreide und Bleistift-Textur.
- **Palette:** Beispielsweise Koralle, Senf, Petrol, Creme, Anthrazit. Bei Marken gilt deren Farbwelt.
- **Formen:** dünne cremefarbene Outlines, weiche Kartonschatten, einfache Silhouetten.
- **Stop-Motion-Boil:** Formen verschieben sich alle paar Frames um 1–2 px.
- **Vermeiden:** Fotorealismus, glänzendes 3D, generische KI-Verläufe.

## Figur
- **Führer:** eine Leitfigur bzw. ein Maskottchen als Erzähler. Sie entdeckt das Konzept mit dem Publikum, statt zu dozieren.
- **Konsistenz:** Silhouette, Augen, Farben und Größe bleiben über alle Szenen gleich.
- **Markeneigen:** keine fremden Maskottchen oder Marken. DRUWIDS: kein Konsum, keine Pilzhut-Szenen mit Anwendungsbezug.

## Story-Bogen (7 Schritte)
1. **Hook:** die überraschende Frage.
2. **Vertraute Welt:** an bekannte Erfahrung anknüpfen.
3. **Bruch:** das Problem oder Paradox zeigen.
4. **Mechanismus:** zeigen, was im Inneren passiert.
5. **Entdeckung:** das Prinzip benennen, ERST nachdem es gezeigt wurde.
6. **Konsequenz:** warum die Idee zählt.
7. **Recap:** die Eingangsfrage auflösen (das Schlussbild beantwortet das erste Bild, Loop).

## Lerndesign
- **Reihenfolge:** erst konkrete Erfahrung, dann abstrakter Begriff.
- **Visueller Vergleich**, wo Größe, Zeit oder Kausalität eine Rolle spielen.
- **Fragen:** vor jeder großen Enthüllung eine Frage stellen, dann visuell beantworten.
- **Labels** nur, wo das Objekt sich nicht selbst durch Bewegung erklärt.
- **Recap:** das mentale Modell in neuem Kontext wiederholen.
- **Kognitive Last:** eine neue Beziehung pro Szene.

## Szenenformat (pro Szene festlegen)
- `SZENE [N] – [START–ENDE]`
- **Lernzweck:** genau eine Idee.
- **Bild:** Komposition, Figur, Requisiten, Labels, Kamera.
- **Bewegung:** Auftritt, Hauptaktion, Reaktion, Abgang.
- **Sprecher:** finaler gesprochener Satz.
- **Ton:** Musik-Cue, Atmosphäre, haptische Effekte.
- **Übergang:** was physisch zur nächsten Szene WIRD.

## Übergänge
- Keine harten Schnitte. Linien werden zu Pfaden, Strahlen zu Diagrammen, Partikel formen Objekte, Paneele falten sich zu Papierbühnen.
- Jeder Übergang erklärt eine Beziehung, er dekoriert nicht.

## Sprecher und Ton
- **Tempo:** warm und präzise, 125–145 Wörter pro Minute.
- **Satzbau:** konkrete Sprache vor Fachbegriffen, eine Idee pro Satz.
- **Bildschirmtext:** wiederholt die Sprecherzeile nicht vollständig.
- **Klangwelt:** Papierrascheln, Bleistiftstriche, sanfte Taps, zurückhaltendes tonales Bett. Die Musik duckt unter der Sprache.
- **Export:** ein Sprecher-Clip pro Szene. Stimme z. B. per Kokoro-TTS oder ElevenLabs (nur mit kommerzieller Lizenz). KI-Stimme in der Caption kennzeichnen, außer bei Code Chaos (dort Stimmen nie erwähnen).

## Technik
- **Format:** 1080×1920 bei 9:16 (Safe Zones: oben 250, unten 320, seitlich 120 px) oder 1920×1080, 24–30 fps.
- **Sync:** Sprecher, Bewegung, Untertitel, Musik und SFX laufen synchron.
- **Doppelte Abnahme:** einmal ohne Ton ansehen, einmal nur hören.
- **Pflicht-Endkontrolle:** Wegen der Sprache gilt immer `python C:/video-kontrolle/videokontrolle.py "<video>" --sprache de --schnitte <…>`. Jeden Befund isoliert abhören.

## Barrierefreiheit
- Starker Kontrast und lesbare Schrift in Handy-Größe.
- Bedeutung nie nur über Farbe.
- Jede Sprecherzeile untertiteln, wichtige Nicht-Sprach-Geräusche beschreiben.

## Lieferung
1. Erst Konzept, Stil, Figurenblatt, Storyboard, Sprechertext, Übergangskarte und Audioplan.
2. Dann die komplette funktionierende Animation. NICHT bei Mockup, Styleframe oder stummem Prototyp aufhören.

## Qualitätscheck (vor Abgabe abhaken)
- [ ] Jede Szene hat einen eigenen Lernzweck.
- [ ] Die Eingangsfrage wird vom Schlussbild aufgelöst.
- [ ] Bilder ergänzen den Sprechertext, statt ihn zu doppeln.
- [ ] Übergänge entstehen aus Objekten, die schon im Bild sind.
- [ ] Labels stehen lange genug zum Lesen.
- [ ] Das Maskottchen bleibt über alle Szenen konsistent.
- [ ] Endkontrolle bestanden. Bei DRUWIDS: Compliance-Gate der Skill `druwids-social-operator`, Fakten nur von den Shop-Domains, Pflicht-Disclaimer.

## Autonomie
- Vernünftige Produktionsentscheidungen selbst treffen. Nicht zwischen Storyboard und Animation um Freigabe bitten.
- Nur anhalten, wenn fehlende Infos das Lernziel ändern würden. Annahmen kurz berichten und mit der stärksten Lösung weitermachen.
- Fertig erst, wenn die Animation komplett, synchron und exportfertig ist.
- Veröffentlichen weiter nur nach Tims Freigabe bzw. über die freigegebenen Pipelines.
