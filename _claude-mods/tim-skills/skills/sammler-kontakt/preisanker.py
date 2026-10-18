# -*- coding: utf-8 -*-
"""Gebotsleiter für Ankäufe von Sammlern: abnehmende Zugeständnisse vom Erstgebot bis zum letzten Wort.

Aufruf:
  python preisanker.py --ziel 100 --max 250 [--gebot 150] [--referenz 149 180 220] [--inkl-versand]

  --ziel      Wunschpreis (wird Erstgebot, wenn noch nichts geboten wurde)
  --max       Obergrenze = letztes Wort (wird nie vorab genannt)
  --gebot     bereits gebotener Betrag (die Leiter startet dort)
  --referenz  belegte Vergleichspreise (z. B. Discogs-Verkäufe, gleiche Aufnahmen/Auflage)

Nur Python-Standardbibliothek, keine Netzzugriffe. Gibt eine Leiter aus, keine Empfehlung zum Kauf.
"""
import argparse
import statistics
import sys

ANTEILE = (0.5, 0.3, 0.2)  # Anteil der Lücke je Schritt: Zugeständnisse werden kleiner


def glatt(betrag):
    """Auf glatte Beträge runden: unter 100 auf 5, sonst auf 10 (abrunden, nie über das Ziel hinaus)."""
    schritt = 5 if betrag < 100 else 10
    return int(betrag // schritt * schritt)


def leiter(start, maximum):
    """Stufen von start bis maximum mit abnehmenden Zugeständnissen; die letzte Stufe ist exakt maximum."""
    if maximum < start:
        raise ValueError(f"--max ({maximum}) liegt unter dem Startbetrag ({start})")
    luecke = maximum - start
    stufen, summe = [], start
    for anteil in ANTEILE[:-1]:
        summe += anteil * luecke
        wert = glatt(summe)
        if stufen and wert <= stufen[-1] or wert <= start or wert >= maximum:
            continue
        stufen.append(wert)
    stufen.append(maximum)
    return stufen


def warnungen(ziel, maximum, referenz):
    if not referenz:
        return ["Keine Referenzpreise angegeben: erst belegte Vergleichspreise sammeln (gleiche Aufnahme, Auflage, Zustand)."]
    hinweise = []
    med, tief = statistics.median(referenz), min(referenz)
    if maximum > med * 1.3:
        hinweise.append(f"Max {maximum:g} liegt mehr als 30 % über dem Referenz-Median {med:g}: nur bei echter Seltenheit (have/want, Auflage) vertretbar.")
    if ziel < tief * 0.5:
        hinweise.append(f"Erstgebot {ziel:g} liegt unter der Hälfte des niedrigsten Referenzpreises {tief:g}: kann als respektlos ankommen, Begründung mitliefern.")
    return hinweise


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--ziel", type=float, required=True)
    p.add_argument("--max", type=float, required=True, dest="maximum")
    p.add_argument("--gebot", type=float)
    p.add_argument("--referenz", type=float, nargs="*", default=[])
    p.add_argument("--inkl-versand", action="store_true")
    a = p.parse_args(argv)
    if a.ziel <= 0 or a.maximum <= 0 or (a.gebot is not None and a.gebot <= 0):
        p.error("Beträge müssen positiv sein")

    zusatz = " inkl. Versand" if a.inkl_versand else ""
    start = a.gebot if a.gebot is not None else a.ziel
    try:
        stufen = leiter(start, a.maximum)
    except ValueError as e:
        p.error(str(e))

    sys.stdout.reconfigure(encoding="utf-8")
    if a.gebot is None:
        print(f"Erstgebot: {glatt(a.ziel)} €{zusatz} (mit Begründung aus den Referenzpreisen)")
    else:
        print(f"Bisher geboten: {a.gebot:g} €{zusatz}")
    for i, s in enumerate(stufen, 1):
        rolle = "letztes Wort" if s == stufen[-1] else "Zugeständnis"
        print(f"  Stufe {i}: {s:g} €{zusatz}  ({rolle})")
    print("Regeln: nie eine Spanne nennen; jede Stufe nur gegen eine Gegenleistung oder neue Info;"
          " nach dem letzten Wort nicht weiter erhöhen.")
    for w in warnungen(a.ziel, a.maximum, a.referenz):
        print("WARNUNG: " + w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
