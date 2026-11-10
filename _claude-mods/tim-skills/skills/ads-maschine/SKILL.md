---
name: ads-maschine
description: "Gewinner der Nische finden (Meta-Anzeigen, die seit Wochen laufen, und Ausreißer-Shorts fremder Kanäle) und daraus organische Shorts, Captions und später eigene Anzeigen bauen. Bei /ads, „Ads-Maschine“, „was läuft bei der Konkurrenz“, „Ad Library“, „Gewinner-Hooks“, neues Format oder Angebot für Polished, Code Chaos, ZeitSprung."
---

# Ads-Maschine

Eine Website oder Marke rein, Gewinnermuster der Nische raus, daraus fertige Varianten für Shorts, Posts und Anzeigen.
Drei Werkzeuge: **Scraper** (Werbe-Radar + Gewinner-Radar), **Creator** (Texte, Hooks, Skripte), **Bilder** (ki-medien).
Tim, 10.11.2026: „Ads-maschine super für organische videos“. Bezahlte Anzeigen schaltet Tim noch nicht; das Kleingewerbe kann das ändern.

Nicht für DRUWIDS, keinduftbaum, Mitragyna (Projektende 30.11.2026, beide Radare sperren sie im Code).

## 1. Marke und Angebot lesen
- Website mit Firecrawl lesen (`firecrawl scrape <url>`): Angebot, Preis, Nutzenversprechen, Belege, Zielgruppe, vorhandene CTAs.
- Eigene Zahlen: neuester `C:/social-insights/berichte/wachstum_*.md` und `C:/social-insights/empfehlungen.md`.
- Grok-Briefing der Marke (`grok_briefing`) als Zusatz, Befunde gelten als ungeprüft.

## 2. Scraper: Gewinner holen
- **Werbe-Radar (Meta Ad Library):** `python -m si.werbung --marke <marke> [--max N]` in `C:/social-insights`.
  Aktive Anzeigen, die ≥ 30 Tage laufen; Rang = min(Tage, 180) × (1 + ln Varianten). Video-Gewinner werden gemessen und ihr Hook transkribiert.
  Kosten: Apify-Gratisguthaben (0,00015 $ je Anzeige, Deckel 0,05 $ je Lauf, Reserve 1,5 $ für den Polished-Outreach). Konfiguration `werbung.json`.
- **Gewinner-Radar (YouTube-Shorts):** `python -m si.gewinner --marke <marke>`. Ausreißer ≥ 3× Median des eigenen Kanals, 0 €. Konfiguration `gewinner.json`.
- Neue Marke oder Nische: Eintrag in beiden JSON-Dateien anlegen (Suchbegriffe, `text_filter`/`titel_filter`, feste Konkurrenten), dann laufen lassen.
- Beide laufen sonntags in `wachstum.py` mit. Berichte: `berichte/werbung_<datum>.md`, `berichte/gewinner_<datum>.md`.
- Einzelnes fremdes Video genauer ansehen: Skill `fremdvideo-analyse`.

## 3. Muster ableiten (Pflicht vor jedem Text)
Tabelle je Muster, nur mit mindestens 3 Belegen (sonst als „Einzelfall“ markieren):
| Muster | Hook-Art (Frage, Zahl, Vorher/Nachher, Fehler, Demo) | Winkel (Schmerz, Ergebnis, Beweis, Neugier) | Format | Länge/Tempo | CTA | Belege (Links) |
Gegen die eigenen Messwerte stellen (Länge, Schnitte/min, erster Schnitt aus dem Bericht): Was machen Gewinner anders?

## 4. Creator: Varianten bauen
- Je Muster 3 Varianten: **organischer Short** (Hook ≤ 1,5 s dreischichtig: gesprochen + Bild + Text, Re-Hook, Payoff, CTA/Loop nach `Social Media Rules 2026.md`), **Caption**, **Anzeige** (Primärtext ≤ 125 Zeichen, Überschrift ≤ 40, CTA-Knopf).
- Skills dazu laden: `ad-creative` (Anzeigenformate, Creative-Tests), `hook-master` (Einstieg), `copywriting`, danach `ig-human` bzw. `humanizer-de`.
- Captions vor dem Einplanen mit `social-studio`/`post-gate` prüfen. Tims Regeln je Marke gelten (z. B. Code Chaos: KI-Hinweis nur „Bild mit KI erstellt“; Polished-Fachkommentare selbstbewusst in Fachsprache).
- Machart jeder neuen Variante melden (`si.machart.melde`) und als A/B-Arm führen (`si.experimente.arm`), damit der Wochenbericht zeigt, welches Muster bei Tims Publikum trägt.

## 5. Bilder und Video-Bausteine
- Skill `ki-medien` (Gratisstufe zuerst, Deckel `C:/bildwerk/deckel.json`). Schrift nie malen lassen, immer als Overlay. Echte Produktfotos/Screenshots vor KI.
- Thumbnails/Cover nach den Thumbnail-Regeln (64/150-px-Test).

## 6. Eigenes Werbekonto (erst wenn Tim es einrichtet)
- Dann: Anzeigen-Insights nur lesen (Meta Marketing API, `ads_read`), Gewinner-Varianten aus Schritt 4 als Testvorschlag mit Budget-Rahmen vorlegen.
- **Claudes eigene Grenze:** Anzeigen schalten, Budget ändern oder Zahlungsdaten anfassen nur auf Tims ausdrückliches Wort je Kampagne (Geld + Außenwirkung). Anbieterangaben nie erfinden (`{{ANBIETER_NAME}}`, bis das Kleingewerbe einen Namen hat).

## Grenzen
- Nur Form lernen. Nie Text, Bild, Musik oder Video von Fremden übernehmen, nie Konkurrenten in eigener Werbung nennen (Urheberrecht, UWG).
- Keine erfundenen Zahlen oder Kundenstimmen; jede Aussage muss Tims Angebot wirklich halten.
- Laufzeit ≠ Erfolg in jedem Einzelfall (vergessene Daueranzeigen) – darum Varianten-Gewicht, Deckel bei 180 Tagen und Musterbildung über mehrere Belege.
