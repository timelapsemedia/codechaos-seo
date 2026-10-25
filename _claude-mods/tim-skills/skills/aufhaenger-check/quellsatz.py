#!/usr/bin/env python3
"""Zu jedem Aufhänger (Hook, Thumbnail-Text, Titel, Caption) den vollen Quellsatz finden.

Sucht das Zitat bzw. die Schlüsselwörter eines Aufhängers im Transkript (SRT, VTT,
Whisper-JSON oder Text) und gibt den ganzen Satz samt Satz davor und danach aus,
bei SRT/VTT/JSON mit Zeitmarke. So lässt sich prüfen, ob der Aufhänger ohne Kontext
dasselbe behauptet wie die Quelle.

Nur Standardbibliothek, kein Netz.
"""
import argparse
import difflib
import json
import re
import sys

STOPP = set("der die das ein eine einer eines einem einen und oder aber noch nur auch "
            "ist war sind waren hat hatte haben wird wurde hier da dort so wie was wer "
            "ich du er sie es wir ihr man nicht kein keine mit von zu im in am an auf "
            "für den dem des sich mal ja schon dann denn doch the a an of to is was".split())


def zeit(s):
    s = s.strip().replace(",", ".")
    teile = [float(x) for x in s.split(":")]
    while len(teile) < 3:
        teile.insert(0, 0.0)
    return teile[0] * 3600 + teile[1] * 60 + teile[2]


def lade(pfad):
    """Liste von (startzeit|None, text) in Reihenfolge."""
    roh = open(pfad, encoding="utf-8-sig").read()
    if pfad.lower().endswith(".json"):
        d = json.loads(roh)
        segs = d.get("segments", d) if isinstance(d, dict) else d
        return [(s.get("start"), s.get("text", "")) for s in segs]
    if pfad.lower().endswith((".srt", ".vtt")):
        stuecke = []
        for block in re.split(r"\n\s*\n", roh.replace("\r", "")):
            m = re.search(r"(\d[\d:.,]+)\s*-->", block)
            if not m:
                continue
            text = " ".join(z for z in block.split("\n")[1:] if "-->" not in z and not z.strip().isdigit())
            stuecke.append((zeit(m.group(1)), re.sub(r"<[^>]+>", "", text)))
        return stuecke
    return [(None, roh)]


def saetze(stuecke):
    """Text zu Sätzen zusammenfügen; jeder Satz bekommt die Startzeit des Stücks, in dem er beginnt."""
    text, marken = "", []
    for t0, t in stuecke:
        marken.append((len(text), t0))
        text += t.strip() + " "
    out = []
    for m in re.finditer(r"[^.!?…]+[.!?…]*[\"“”»«]*", text):
        s = m.group().strip()
        if not s:
            continue
        beginn = m.start() + len(m.group()) - len(m.group().lstrip())
        t0 = None
        for pos, tz in marken:
            if pos <= beginn:
                t0 = tz
        out.append((t0, s))
    return out


def woerter(s):
    return re.findall(r"[a-zäöüß0-9]+", s.lower())


def wertung(aufhaenger, satz):
    a = [w for w in woerter(aufhaenger) if w not in STOPP] or woerter(aufhaenger)
    s = woerter(satz)
    if not a or not s:
        return 0.0
    treffer = sum(1 for w in a if any(difflib.SequenceMatcher(None, w, x).ratio() >= 0.8 for x in s))
    folge = difflib.SequenceMatcher(None, " ".join(woerter(aufhaenger)), " ".join(s)).find_longest_match()
    return treffer / len(a) + 0.3 * folge.size / max(1, len(" ".join(woerter(aufhaenger))))


def fmt(t0):
    if t0 is None:
        return ""
    return f"[{int(t0 // 60):02d}:{t0 % 60:05.2f}] "


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("transkript", help="SRT, VTT, Whisper-JSON oder Text")
    ap.add_argument("aufhaenger", nargs="+", help="Hook-/Thumbnail-/Titeltexte")
    ap.add_argument("--treffer", type=int, default=2, help="beste Fundstellen je Aufhänger (Standard 2)")
    a = ap.parse_args()

    ss = saetze(lade(a.transkript))
    if not ss:
        sys.exit("FEHLER: Transkript leer oder Format nicht erkannt.")
    for h in a.aufhaenger:
        print(f"\n=== Aufhänger: „{h}“")
        bewertet = sorted(((wertung(h, s), i) for i, (_, s) in enumerate(ss)), reverse=True)[:a.treffer]
        if not bewertet or bewertet[0][0] < 0.4:
            print("  KEIN QUELLSATZ GEFUNDEN – Aussage ist nicht durch das Transkript gedeckt "
                  "(eigene Behauptung? dann an anderer Quelle belegen).")
            continue
        if bewertet[0][0] < 0.75:
            print("  NUR SCHWACHE ÜBEREINSTIMMUNG – Aussage wahrscheinlich nicht durch das Transkript "
                  "gedeckt. Nächstliegende Stelle:")
            bewertet = bewertet[:1]
        for w, i in bewertet:
            if w < 0.4:
                break
            print(f"  Fundstelle (Übereinstimmung {min(w, 1.3) / 1.3:.0%}):")
            for j in (i - 1, i, i + 1):
                if 0 <= j < len(ss):
                    t0, s = ss[j]
                    print(f"  {'>>' if j == i else '  '} {fmt(t0)}{s}")


if __name__ == "__main__":
    main()
