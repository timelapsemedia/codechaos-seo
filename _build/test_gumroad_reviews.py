#!/usr/bin/env python
"""Selbsttest für gumroad_reviews.render(): python _build/test_gumroad_reviews.py (Exit 0 = ok)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gumroad_reviews as g

def b(i, s, text, name="Max", ant="", prod="crucible", datum="2026-11-20"):
    return {"id": f"id{i}", "produkt": prod, "sterne": s, "text": text, "name": name, "datum": datum, "antwort": ant}

bew = [b(1, 5, "Super Plugin, klingt sehr gut und ich nutze es für Psytrance."),
       b(2, 1, '<script>alert(1)</script> <a href="http://x">bad</a> https://spam.example'),
       b(3, 4, "", name="X"), b(4, 3, "Fine. This is okay for the price and it works.", prod="crucible-demo", ant="Thanks! https://x.de"),
       b(5, 5, "L" * 3000)] + [b(10 + i, 5, f"Text {i}") for i in range(8)]
daten = {"stand": "2026-11-24", "seiten": {"crucible": {"produkte": [{"permalink": "crucible"}, {"permalink": "crucible-demo"}], "bewertungen": bew}}}
h = g.render("crucible", "de", daten)
fehler = []
def pruefe(cond, msg):
    if not cond: fehler.append(msg)
pruefe("<script>" not in h and "&lt;script&gt;" in h, "HTML nicht escaped")
pruefe("<a href=\"http://x" not in h, "Fremdlink im Text")
pruefe(h.count('<blockquote class="rev"') == 12, "nicht alle Textbewertungen sichtbar: %d" % h.count('<blockquote class="rev"'))
pruefe("<details" in h and "Weitere 4 Bewertungen" in h, "Details fehlt")
pruefe("1× 4 Sterne" in h, "Zähler ohne Text fehlt")
pruefe(h.count('lang="de"') == 1 or 'lang="en"' in h, "lang")
pruefe("Gekürzt, vollständig auf Gumroad" in h, "Kürzungshinweis")
pruefe("Antwort von Code Chaos Audio" in h and "https://x.de" not in h, "Antwort/Link")
pruefe("AggregateRating" not in h, "Schema")
pruefe(", Demo<" in h, "Demo-Kennzeichnung")
pruefe("4,0 von 5" not in h and "von 5 Sternen bei 13 Bewertungen" in h, "Durchschnitt/Anzahl: " + h[h.find('rev-sum'):h.find('rev-sum') + 200])
pruefe(g.render("shardstep", "de", daten) == "", "leere Seite muss leer sein")
pruefe("out of 5 stars from 13 ratings" in g.render("crucible", "en", daten), "EN")
print("\n".join(fehler) or "ok")
sys.exit(1 if fehler else 0)
