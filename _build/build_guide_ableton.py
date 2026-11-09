#!/usr/bin/env python3
"""Erzeugt /ratgeber/gitarrensound-ableton/ (Ratgeber: Heavy-Gitarrensound in Ableton Live mit Cab-IRs).

Aufruf aus dem Repo-Root:  python3 _build/build_guide_ableton.py
Quelle der Fragen: Reddit-Scan 2026-11-08 (codechaos-store/research/reddit/). Produktfakten aus products/black-metal-tone-kit/.
Keine Messwerte erfunden: die Anleitung beschreibt Vorgehen, Zahlen sind als Richtwerte der Community gekennzeichnet.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pages as bp  # noqa: E402
import geo  # noqa: E402

BASE, ROOT, esc = bp.BASE, bp.ROOT, bp.esc
DATE = "2026-11-09"
URL = BASE + "/ratgeber/gitarrensound-ableton/"
G = "https://timberwolf688.gumroad.com/l/black-metal-tone-kit?utm_source=site&amp;utm_medium=guide&amp;utm_campaign=ableton-guitar"

TITLE = "Heavy-Gitarrensound in Ableton Live: Amp-Sim, IR und Doubles | Code Chaos"
DESC = ("Warum Amp-Sims zu Hause klein klingen und wie du das in Ableton Live löst: Pegel vor der Sim, Cab-IR in Hybrid Reverb, "
        "Low-Cut und Doubles ohne Kammfilter im Mono.")

STEPS = [
    ("Pegel vor der Amp-Sim prüfen",
     "Viele Amp-Sims klingen dünn oder „plinky“, weil das DI-Signal zu heiß oder zu leise ankommt. In den Reddit-Threads, aus denen diese Anleitung stammt, "
     "lautet der Rat meist: Spitzen etwa zwischen −12 und −6 dBFS in die Sim schicken, den Rest regelt der Gain-Regler der Sim. "
     "Das ist ein Richtwert aus der Community, kein Messwert von uns. Prüfe ihn mit einem Utility oder Spectrum vor der Sim."),
    ("Vor der Verzerrung filtern",
     "Setze vor die Sim einen EQ Eight: Hochpass bei etwa 80 bis 100 Hz und eine leichte Senke im Low-Mid. So verzerrt die Sim keine Bassenergie, "
     "die später den Mix zuschmiert. Die Werte sind Startpunkte; passe sie an deine Gitarre und Stimmung an."),
    ("Cab-Impulsantwort statt Standard-Cab laden",
     "Schalte das Cab der Sim ab (oder nutze eine Sim ohne Cab) und lade eine Impulsantwort. In Live Suite geht das über Hybrid Reverb: "
     "WAV-Datei aus dem Browser auf das Gerät ziehen und den Convolution-Teil nutzen, Mix auf 100 %. Hybrid Reverb gehört zu Live Suite. "
     "Ohne Suite funktioniert jeder IR-Loader als Plugin genauso. Hinweis: Diesen Schritt beschreiben wir nach dem Ableton-Handbuch; die Anleitung ersetzt keinen eigenen Hörtest."),
    ("Zischeln im Cab lösen, nicht im Master",
     "Black-Metal-Gitarren zischeln meist über 6 kHz. Eine entschärfte IR löst das ohne EQ. Das Code Chaos Black Metal Tone Kit enthält dafür "
     "6 entschärfte Versionen seiner 19 synthetisch erzeugten IRs (je 48 und 44,1 kHz, 24 Bit WAV)."),
    ("Doubles ohne Kammfilter im Mono",
     "Zwei Aufnahmen derselben Gitarre, hart links und rechts, klingen im Mono phasig, wenn beide dieselbe Cab-IR und dieselbe Spielweise teilen. "
     "Nimm für die zweite Spur eine andere IR (zum Beispiel eine andere Mikrofonposition), spiele sie wirklich neu ein statt zu kopieren, "
     "und höre im Mono gegen: Verschwindet die Gitarre, hast du ein Phasenproblem."),
]

FAQ = [
    ("Welche Pegel sollen in die Amp-Sim?",
     "Als Richtwert nennen viele Heimproduzenten Spitzen zwischen −12 und −6 dBFS. Prüfe es an deiner Sim: Wenn sie bei normalem Spielen ständig übersteuert oder kaum anspricht, passe den Eingangspegel an."),
    ("Kann ich eine IR in Ableton Live laden?",
     "In Live Suite über Hybrid Reverb (Convolution-Teil). In anderen Versionen mit einem IR-Loader als VST3, zum Beispiel einem Neural-Amp-Modeler-Plugin mit IR-Slot."),
    ("Brauche ich dafür das Tone Kit?",
     "Nein, der Weg funktioniert mit jeder IR. Das Tone Kit (9 €) liefert dafür 19 selbst erzeugte, lizenzfreie IRs für Black Metal. Es sind keine fremden IRs enthalten."),
    ("Enthält das Tone Kit Ableton-Dateien?",
     "Noch nicht. Die 10 + 6 FX-Chains sind für REAPER. Die IR-WAV-Dateien laufen in jeder DAW, die Ableton-Racks fehlen bisher."),
]


def build():
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "HowTo", "@id": URL + "#howto", "name": "Heavy-Gitarrensound in Ableton Live mit Amp-Sim und Cab-IR", "description": DESC,
         "inLanguage": "de", "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t} for i, (n, t) in enumerate(STEPS)]},
        {"@type": "Article", "@id": URL + "#webpage", "url": URL, "headline": TITLE, "description": DESC, "inLanguage": "de",
         "isPartOf": {"@id": BASE + "/#website"}, "datePublished": DATE, "dateModified": geo.DATUM, "author": geo.autor_ld()},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Startseite", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Gitarrensound in Ableton", "item": URL}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": bp.strip(a)}} for q, a in FAQ]},
    ]}
    steps = "".join(f'<li><h3>{esc(n)}</h3><p class="prose">{esc(t)}</p></li>' for n, t in STEPS)
    body = f"""<main id="main">
<div class="wrap crumbs"><nav aria-label="Breadcrumb"><ol><li><a href="/">Startseite</a></li><li aria-current="page">Gitarrensound in Ableton</li></ol></nav></div>
<section class="s-hero">
  <div class="wrap narrow">
    <span class="eyebrow">Ratgeber</span>
    <h1>Heavy-Gitarrensound in Ableton Live: Amp-Sim, IR und Doubles</h1>
    <div class="rule" aria-hidden="true"><i></i></div>
    <p class="answer">Gitarren aus Amp-Sims klingen zu Hause oft klein, zischelnd oder im Mono phasig. In fünf Schritten behebst du das in Ableton Live: Pegel vor der Sim prüfen, vor der Verzerrung filtern, eine Cab-Impulsantwort laden, Zischeln im Cab lösen und Doubles im Mono gegenhören.</p>
  </div>
</section>
<section aria-labelledby="s-t"><div class="wrap narrow"><h2 id="s-t">Die fünf Schritte</h2><ol class="steps">{steps}</ol></div></section>
<section class="alt" aria-labelledby="k-t"><div class="wrap narrow"><h2 id="k-t">Passende IRs</h2>
<p class="prose">Das <a href="{G}">Black Metal Tone Kit</a> von Code Chaos Audio kostet 9 €: 19 selbst erzeugte Cab-IRs (darunter 6 entschärfte und 3 Bass-Cabs) und REAPER-Chains. Sofort-Download, ohne Login und ohne Lizenzserver. Mehr dazu auf der Seite <a href="/sounds/">Samples, MIDI und Presets</a>. Wer ein komplettes Gitarren-Plugin sucht: <a href="/plugins/gravesaw/">Gravesaw</a> (Amp + Cab) hat eine kostenlose Demo.</p></div></section>
<section aria-labelledby="faq-t"><div class="wrap narrow"><h2 id="faq-t">Häufige Fragen</h2>{bp.faq_html(FAQ)}</div></section>
</main>
"""
    html = (bp.head("de", URL, None, TITLE, DESC, BASE + "/images/sounds/og.jpg", "Code Chaos Audio Black Metal Tone Kit", ld, og_type="article")
            + bp.nav("de", None, "sounds") + body + bp.footer("de"))
    html, _ = geo.ausbauen(html, "/ratgeber/gitarrensound-ableton/", "de", art="sounds")
    path = os.path.join(ROOT, "ratgeber", "gitarrensound-ableton", "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8", newline="\n").write(html)
    geo.REG.speichern()
    return path


if __name__ == "__main__":
    print(build())
