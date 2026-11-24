#!/usr/bin/env python3
"""Gate vor allen drei Zielen der Crucible-Pipeline (Instagram, YouTube, Buffer). Fail-closed.

Anlass (Tim, 21.11.2026): Die Pipeline hat "Black Metal MIDI Grooves 2" mit deutscher Caption auf TikTok
@codechaos_abstractsound gepostet. Regeln:
  1. Marke: Gothic/Black/Death Metal gehören zu Polished, Psy/Hitech/Psycore/Elektronik zu Code Chaos.
     Ausnahme nur für store-weite Aktionen (Feld "store_weit": true UND Aktionswort wie Black Friday im Text).
  2. Sprache: Englisch zuerst (Tim 17.11.2026). Caption/Beschreibung: erster Absatz englisch;
     Titel und X-Text überwiegend englisch. Logik übernommen aus C:/hitech-lab/social/sprach_gate.py.
  3. Höchstens 5 Hashtags pro Text.
  4. KI-Hinweis (Post mit "ki": true): genau "Image created with AI / Bild mit KI erstellt", nie Stimmen erwähnen.

Jeder Fehler im Gate hält ALLES zurück (lade_posts() liefert dann eine leere Liste).

    python3 _marketing/crucible_gate.py --test     Selbsttest (Exit 0 = grün)
    python3 _marketing/crucible_gate.py            Bericht über alle offenen Posts
"""
import datetime
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TZ = ZoneInfo("Europe/Berlin")

# ---------------------------------------------------------------- Sprache (aus sprach_gate.py, Stand 17.11.2026)
EN = set("a the and with your you this that is are was for of now it its not into from what who when where our out "
         "here there just every all one two before after first then only still never more than his her they them "
         "we my me be been have has had can will would at by on in an to "
         "it's they're you're we're i'm don't can't won't isn't there's that's what's doesn't "
         "today tonight everywhere new free get got make made how many much did does do sleep awake night day "
         "track tracks song every each again back down up off over through without inside outside nothing "
         "something someone everyone always ever world sound mix master voice dead death life blood heart time "
         "listen hear play plays playing played made making while because which these those very most other".split())
DE = set("und der die das nicht mit ist ein eine einen dem den des für auf du dein deine jetzt hier wird sind war "
         "noch nur auch wie wenn dann aber oder ich mir mich wir uns sie ihr zum zur vom beim über unter nach vor "
         "zwischen bei aus dass schon erst "
         "heute überall wach neu neue neuen jeder jede jedes immer wieder nichts etwas alles nacht tag stunden "
         "schläft schlafen hört hören spielt stimme leben tod herz zeit welt klang ohne durch gegen ganz sehr "
         "kostenlos kostenlose kostenloses gratis".split())
GEMEINSAM = {"in", "an", "so", "man", "will", "was", "die"}
EN -= GEMEINSAM
DE -= GEMEINSAM


def _woerter(text):
    text = re.sub(r"https?://\S+|#\w+|@\w+", " ", text)
    return re.findall(r"[A-Za-zÄÖÜäöüß']+", text.lower())


def zaehle(text):
    w = _woerter(text)
    return sum(x in EN for x in w), sum(x in DE for x in w)


def sprache(abschnitt):
    e, d = zaehle(abschnitt)
    if e != d:
        return "en" if e > d else "de"
    sauber = " ".join(_woerter(abschnitt))
    if len(sauber.split()) < 2:
        return "?"
    try:
        from langdetect import DetectorFactory, detect_langs
        DetectorFactory.seed = 0
        beste = {x.lang: x.prob for x in detect_langs(sauber)}
        return "en" if beste.get("en", 0) >= beste.get("de", 0) else "de"
    except Exception:  # noqa: BLE001  ohne langdetect gilt Gleichstand nicht als Englisch (fail-closed)
        return "?"


def englisch_ok(text, kurz=None):
    """(ok, grund). kurz=None: unter 80 Zeichen gilt die Regel für kurze Texte."""
    if not isinstance(text, str) or not text.strip():
        return True, "leer"
    kurz = len(text) < 80 if kurz is None else kurz
    en, de = zaehle(text)
    if kurz:
        if de > en:
            return False, f"kurzer Text überwiegend deutsch (en {en}, de {de})"
        return True, "ok"
    if len(text) > 400 and en < 4:
        return False, f"kein englischer Block (en {en}, de {de})"
    if len(text) > 400:
        erster = next((a for a in re.split(r"\n\s*\n", text) if _woerter(a)), "")
    else:
        absaetze = [a for a in re.split(r"\n\s*\n", text) if len(_woerter(a)) >= 3]
        erster = (absaetze[0] if absaetze else text.strip())[:120]
    if sprache(erster) != "en":
        e1, d1 = zaehle(erster)
        return False, f"Anfang nicht englisch (en {e1}, de {d1}); Englisch gehört nach vorn"
    return True, "ok"


# ---------------------------------------------------------------- Marke
# Metal-Begriffe und die Produkte der Black Metal Suite (Memory marken_trennung_metal_psy, Tim 21.11.2026)
METAL = re.compile(r"\b(black|death|gothic|doom|thrash|melodic death|post)[\s-]?metal\w*|#?\bmetal\w*\b|\bblast ?beats?\b|"
                   r"\bblasts?\b|\btremolo\b|\bd-beat\b|\bblackgaze\b|\bdungeon ?synth\b|"
                   r"\b(rimehall|gravesaw|frostfret|hoarfell|black metal suite|midi grooves|tone kit)\b", re.I)
AKTION = re.compile(r"black ?friday|cyber ?monday|store-?wide|storeweit|\bsale\b|summer sale|winter sale", re.I)

KI_HINWEIS = "Image created with AI / Bild mit KI erstellt"
STIMME = re.compile(r"\b(ai|ki)[\s-]?(voice|stimme|vocals?|gesang)\b|\bstimme mit ki\b|\bvoice (made|created) with ai\b", re.I)


# ---------------------------------------------------------------- Angebots-Sperre Dezember 2026
# Roadmap-Schritt 12 (24.11.2026): Tims Gewerbe beginnt erst am 01.01.2027, im Dezember keine Aufträge. Im Fenster
# geht kein Post mit Preis, Rabatt, Code, Kauf-/Buchungsaufruf oder Shop-Link raus (Black Friday bis 30.11. bleibt).
# Logik = C:/kunden-kreislauf/angebots_sperre.py (hier als Kopie, weil die Pipeline auch in GitHub Actions läuft).
SPERRE_VON = os.environ.get("ANGEBOTS_SPERRE_VON", "2026-12-01")
SPERRE_BIS = os.environ.get("ANGEBOTS_SPERRE_BIS", "2026-12-31")
SHOP = ("gumroad", "shop.codechaos-official.de", "etsy",   # shop.codechaos-official.de = Gumroad-Domain seit 24.11. "payhip", "ko-fi.com/s", "polished.media", "codechaos-official.de/store",
        "codechaos-official.de/shop", "codechaos-official.de/plugins", "buymeacoffee", "patreon.com",
        "codechaos-official.de/en/mastering", "codechaos-official.de/mastering", "codechaos-official.de/#mastering",
        "codechaos-official.de/de/mastering")
ANGEBOT = [
    ("Preis", re.compile(r"[€$£]\s?\d+(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?\s?(?:€|EUR\b|euro\b|USD\b|\$)|"
                         r"\b(?:price[sd]?|pricing|preis|preise|kostet|costs? (?:just |only )?\d|pay what you want|"
                         r"name your price|zahl,? was du willst)\b", re.I)),
    ("Rabatt", re.compile(r"\b\d{1,2}\s?%\s?(?:off|rabatt|discount|günstiger|reduziert|sparen)\b|[−–-]\s?\d{1,2}\s?%|"
                          r"\b(?:rabatt\w*|discount\w*|sale|on sale|sonderangebot\w*|angebot|angebote|special offer|"
                          r"limited offer|launch offer|intro(?:ductory)? (?:offer|price)|early[- ]?bird|frühbucher\w*|"
                          r"black ?friday|cyber ?monday|gutschein\w*|coupon\w*|voucher\w*|save \d+|spar(?:e|st) \d+)\b",
                          re.I)),
    ("Code", re.compile(r"(?i:\b(?:promo|rabatt|discount|coupon|gutschein|voucher)[- ]?codes?\b)|"
                        r"\b(?:code|Code|CODE)\s*[:=]?\s*[\"'“„]?(?!CHAOS\b)[A-Z0-9]{4,}\b")),
    ("Kauf/Buchung", re.compile(
        r"\b(?:buy|buying|kaufen|kauf|kaufe|jetzt kaufen|pre-?order|order\s+(?:now|here|today|yours|it|via|at|on|from|"
        r"through|your)|bestell\w*|book\s+(?:now|here|today|your|a|an|it|via|at|in)|booking|bookings|booked|"
        r"buchen|buchung\w*|buchbar|gebucht|checkout|purchase|add to cart|warenkorb|shop now|get yours|grab yours|"
        r"send (?:me )?your (?:mix|track|song|stems)|schick (?:mir )?deinen (?:mix|track|song)|"
        r"request a (?:quote|master)|mastering-?anfrage|anfrage|slots?|free (?:mix )?audit|"
        r"kostenlose[nrs]? (?:mix-?)?audit|mastering[^.\n]{0,25}(?:link in (?:bio|profile)|link im profil|dm me))\b",
        re.I)),
]


def angebot_treffer(text):
    out = [f"{n}: {m.group(0).strip()}" for n, rx in ANGEBOT for m in rx.finditer(text or "")]
    out += [f"Shop-Link: {d}" for d in SHOP if d in (text or "").lower()]
    return list(dict.fromkeys(out))


def texte(p):
    """(feld, text, kurz) aller Texte, die eine Plattform sieht."""
    out = [("caption", p.get("caption", ""), None), ("short", p.get("short", ""), None)]
    if p.get("video"):
        out.append(("video_title", p.get("video_title", ""), True))
    if p.get("youtube_description"):
        out.append(("youtube_description", p["youtube_description"], None))
    return out


def pruefe(p):
    """Liste der Befunde; leer = darf raus."""
    befunde = []
    for feld, text, kurz in texte(p):
        if feld in ("caption", "short") and not (text or "").strip():
            befunde.append(f"{feld}: fehlt")
            continue
        ok, grund = englisch_ok(text, kurz)
        if not ok:
            befunde.append(f"sprache {feld}: {grund}")
        tags = re.findall(r"#\w+", text or "")
        if len(tags) > 5:
            befunde.append(f"{feld}: {len(tags)} Hashtags (max. 5)")
        if STIMME.search(text or ""):
            befunde.append(f"{feld}: erwähnt KI-Stimme (KI-Hinweis nur fürs Bild)")
    alles = "\n".join(t or "" for _, t, _ in texte(p)) + "\n" + " ".join(p.get("youtube_tags") or [])
    treffer = sorted({m.group(0).strip().lower() for m in METAL.finditer(alles)})
    if treffer:
        if not (p.get("store_weit") is True and AKTION.search(alles)):
            befunde.append("marke: Metal-Inhalt gehört zu Polished (" + ", ".join(treffer[:6]) + ")")
    if p.get("ki") and KI_HINWEIS not in (p.get("caption") or ""):
        befunde.append(f'ki: Caption ohne "{KI_HINWEIS}"')
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(p.get("date", ""))):
        befunde.append("date: fehlt/ungültig")
    elif SPERRE_VON <= str(p["date"]) <= SPERRE_BIS:
        t = angebot_treffer(alles)
        if t:
            befunde.append(f"angebots-sperre {SPERRE_VON}–{SPERRE_BIS} (Gewerbe ab 01.01.2027): " + "; ".join(t[:5]))
    return befunde


def lade_posts(log=print, pfad=None):
    """Für post_instagram/post_youtube/buffer_schedule: nur Posts, die das Gate bestehen. Fail-closed."""
    try:
        posts = json.load(open(pfad or os.path.join(HERE, "crucible-posts.json"), encoding="utf-8"))
        heute = datetime.datetime.now(TZ).date().isoformat()
        ok, alt = [], 0
        for p in posts:
            b = pruefe(p)
            if not b:
                ok.append(p)
            elif str(p.get("date", "")) >= heute:
                log(f"[gate] GEHALTEN {p.get('id')}: {'; '.join(b)[:400]}")
            else:
                alt += 1   # Altbestand (vor dem Gate gepostet): bleibt ebenfalls draußen, nur nicht einzeln geloggt
        if alt:
            log(f"[gate] {alt} ältere Einträge ohne EN/Marken-Freigabe ausgeblendet")
        return ok
    except Exception as e:  # noqa: BLE001
        log(f"[gate] FEHLER ({type(e).__name__}: {str(e)[:200]}) - in diesem Lauf geht nichts raus")
        return []


def bericht():
    posts = json.load(open(os.path.join(HERE, "crucible-posts.json"), encoding="utf-8"))
    heute = datetime.datetime.now(TZ).date().isoformat()
    n = 0
    for p in posts:
        if p["date"] < heute:
            continue
        b = pruefe(p)
        n += bool(b)
        print(("ROT  " if b else "ok   ") + p["date"] + " " + p["id"] + ("  " + "; ".join(b)[:300] if b else ""))
    print(f"{n} offene Posts gehalten")
    return 1 if n else 0


def _test():
    """Echte Fälle: der TikTok-Post vom 21.11. (muss gehalten werden) und ein EN-Psy-Post (muss durchgehen)."""
    arch = json.load(open(os.path.join(HERE, "crucible-ausgelagert.json"), encoding="utf-8"))["posts"]
    echt = {p["id"]: p for p in arch}
    posts = {p["id"]: p for p in json.load(open(os.path.join(HERE, "crucible-posts.json"), encoding="utf-8"))}
    faelle = [
        ("Black Metal MIDI Grooves 2 (echter Fall 21.11., DE + Metal)", echt["store-14-black-metal-midi-grooves-2"], False),
        ("Black Metal MIDI Grooves 2 auf Englisch (Metal bleibt Metal)",
         dict(echt["store-14-black-metal-midi-grooves-2"],
              caption="No drummer in the band? Then the blast has to come from the computer.\n\n74 new drum grooves as MIDI, "
                      "from blasts and gallops to d-beat and doom.\n\n9 € · link in bio\n\n#blackmetal #drummidi",
              short="Black Metal MIDI Grooves 2: 74 humanised drum grooves for your next record, 9 €",
              video_title="Black Metal MIDI Grooves 2: 74 humanised drum grooves"), False),
        ("Shardgate EN-Psy-Post (neu)", posts["store-32-shardgate-launch"], True),
        ("Shardgate in alter DE-Fassung", echt["store-32-shardgate-launch__de_alt"], False),
        ("Black Friday DE (−40 %, alt)", echt["bf-01-black-friday-2026"], False),
        ("Black Friday EN store-weit mit Metal-Produkten",
         {"id": "t-bf", "date": "2026-11-27", "store_weit": True,
          "caption": "Black Friday at Code Chaos Audio: code BLACKFRIDAY takes 40 % off every product, the Black Metal "
                     "Suite included, until Monday.\n\nBlack Friday bei Code Chaos Audio: 40 % auf alles.\n\n#blackfriday",
          "short": "Black Friday: 40 % off every Code Chaos Audio product until Mon 30 Nov, code BLACKFRIDAY"}, True),
        ("Metal-Produkt mit store_weit-Flag, aber ohne Aktion",
         {"id": "t-flag", "date": "2026-12-01", "store_weit": True,
          "caption": "Gravesaw is out: a black metal amp for your guitar and bass.\n\n#ampsim",
          "short": "Gravesaw: the black metal amp, 19 €"}, False),
        ("Psy-Post mit 6 Hashtags",
         dict(posts["store-32-shardgate-launch"],
              caption=posts["store-32-shardgate-launch"]["caption"].rstrip() + " " +
              " ".join(f"#extra{i}" for i in range(6 - len(re.findall(r"#\w+", posts["store-32-shardgate-launch"]["caption"]))))),
         False),
        ("KI-Post ohne Hinweis", dict(posts["store-32-shardgate-launch"], ki=True), False),
        # Angebots-Sperre Dezember 2026 (Roadmap-Schritt 12): echte Fälle aus crucible-posts.json
        ("Shardstep-Launch 01.12. (echter Fall, €15 + Gumroad)", dict(posts["store-19-shardstep-launch"], date="2026-12-01"), False),
        ("Shardstep-Launch auf 05.01.2027 verschoben", dict(posts["store-19-shardstep-launch"], date="2027-01-05"), True),
        ("Kick+Bass-Engine-Overlap 19.12. (echter Fall)", dict(posts["store-31-kick-bass-engine-overlap"], date="2026-12-19"), False),
        ("Lernpost im Dezember mit Shop-Link (Gratis-Tool, trotzdem Shop)",
         dict(posts["learn-04-kick-laenge"], date="2026-12-10"), False),
        ("derselbe Lernpost ohne Shop-Link",
         {k: (re.sub(r"\S*(?:gumroad|shop\.codechaos-official\.de)\S*", "", v, flags=re.I) if isinstance(v, str) else v)
          for k, v in dict(posts["learn-04-kick-laenge"], date="2026-12-10").items()}, True),
        ("Black Friday EN 30.11. (letzter Aktionstag, vor der Sperre)",
         {"id": "t-bf30", "date": "2026-11-30", "store_weit": True,
          "caption": "Last day of Black Friday at Code Chaos Audio: code BLACKFRIDAY takes 40 % off.\n\n#blackfriday",
          "short": "Black Friday: last day, 40 % off with code BLACKFRIDAY"}, True),
    ]
    fehler = 0
    for name, post, soll in faelle:
        b = pruefe(post)
        ist = not b
        mark = "ok " if ist == soll else "FALSCH"
        fehler += ist != soll
        print(f"{mark} {name}: {'durch' if ist else 'gehalten'} (soll {'durch' if soll else 'gehalten'})"
              + ("" if ist else "  <- " + "; ".join(b)[:220]))
    # Fail-closed: kaputte Datei -> leere Liste
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:     # echte Datei bleibt unberührt
        kaputt = os.path.join(tmp, "crucible-posts.json")
        open(kaputt, "w", encoding="utf-8").write("{kaputt")
        leer = lade_posts(log=lambda *_: None, pfad=kaputt) == []
    print(("ok " if leer else "FALSCH") + " kaputte crucible-posts.json: nichts geht raus")
    fehler += not leer
    print(f"crucible_gate: {len(faelle) + 1 - fehler}/{len(faelle) + 1} Fälle richtig")
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(_test() if "--test" in sys.argv else bericht())
