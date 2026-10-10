#!/usr/bin/env python3
"""Legt den Wikipedia-Entwurf (im Benutzernamensraum) und die Wikidata-Einträge für Code Chaos an.

Zugang: ein Wikimedia-Bot-Passwort (Spezial:BotPasswords), nie das normale Passwort:
  WIKI_USER=Benutzername@botname  WIKI_BOTPASS=...

  python3 _build/wiki_publish.py check              # nur prüfen: Login, vorhandene Einträge, Wikidata-IDs
  python3 _build/wiki_publish.py wikidata --apply   # Wikidata: Label-Item + Artist-Item anlegen
  python3 _build/wiki_publish.py draft --apply      # Wikipedia: Entwurf unter Benutzer:<Name>/Code Chaos
  python3 _build/wiki_publish.py move --apply       # Entwurf nach „Code Chaos“ verschieben, sobald das Konto das Recht hat
  python3 _build/wiki_publish.py watch [STUNDEN]    # Artikel + Diskussion prüfen: Löschantrag, SLA, QS, fremde Bearbeitungen (Fenster, Standard 26 h)
  python3 _build/wiki_publish.py reply SEITE ABSCHNITT DATEI --apply   # einmalige signierte Antwort in einem Diskussionsabschnitt

Ohne --apply wird nichts geschrieben. Bestehende Einträge werden nie überschrieben (createonly / Dublettenprüfung).
"""
import http.cookiejar, json, os, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "CodeChaosSEO/1.0 (https://codechaos-official.de; polished.media@gmx.de)"
WD = "https://www.wikidata.org/w/api.php"
DEWP = "https://de.wikipedia.org/w/api.php"
SITE = "https://codechaos-official.de/"

# Erwartete englische Labels: das Skript bricht ab, wenn eine ID nicht (mehr) passt.
EXPECT = {
    "Q5": "human", "Q183945": "record producer", "Q639669": "musician", "Q105404852": "tech",
    "Q114107195": "psycore", "Q2452152": "dark psytrance", "Q18127": "record label", "Q183": "Germany", "Q1055": "Hamburg",
    "P31": "instance of", "P742": "pseudonym", "P106": "occupation", "P136": "genre", "P27": "country of citizenship",
    "P551": "residence", "P2031": "work period", "P1953": "Discogs artist", "P1955": "Discogs label",
    "P434": "MusicBrainz artist", "P3283": "Bandcamp", "P3040": "SoundCloud", "P2003": "Instagram", "P7085": "TikTok",
    "P2002": "username", "P856": "official website", "P264": "record label", "P571": "inception", "P17": "country",
    "P112": "found", "P854": "reference URL", "P813": "retrieved",
}

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))


def api(url, params, post=False):
    params = {**params, "format": "json", "formatversion": "2"}
    for attempt in range(5):
        data = urllib.parse.urlencode(params).encode() if post else None
        req = urllib.request.Request(url + ("" if post else "?" + urllib.parse.urlencode(params)), data=data, headers={"User-Agent": UA})
        try:
            with opener.open(req, timeout=60) as r:
                res = json.load(r)
            if res.get("error", {}).get("code") == "maxlag":
                time.sleep(30 * (attempt + 1)); continue
            return res
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                wait = e.headers.get("Retry-After", "")
                time.sleep(int(wait) if wait.isdigit() else 30 * (attempt + 1)); continue
            raise
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            time.sleep(15 * (attempt + 1)); continue
    sys.exit("API dauerhaft überlastet oder nicht erreichbar, später erneut versuchen.")


def login(url):
    u, p = os.environ.get("WIKI_USER"), os.environ.get("WIKI_BOTPASS")
    if not (u and p and "@" in u):
        sys.exit("WIKI_USER (Form Name@botname) und WIKI_BOTPASS setzen (Spezial:BotPasswords).")
    tok = api(url, {"action": "query", "meta": "tokens", "type": "login"})["query"]["tokens"]["logintoken"]
    r = api(url, {"action": "login", "lgname": u, "lgpassword": p, "lgtoken": tok}, post=True)
    if r.get("login", {}).get("result") != "Success":
        sys.exit(f"Login fehlgeschlagen bei {url}: {r.get('login', {}).get('reason', r)}")
    return api(url, {"action": "query", "meta": "tokens"})["query"]["tokens"]["csrftoken"]


def verify_ids():
    ids = list(EXPECT)
    labels = {}
    for i in range(0, len(ids), 40):
        ent = api(WD, {"action": "wbgetentities", "ids": "|".join(ids[i:i + 40]), "props": "labels", "languages": "en"})["entities"]
        labels.update({k: v.get("labels", {}).get("en", {}).get("value", "") for k, v in ent.items()})
    bad = [f"{k}: erwartet '{v}', ist '{labels.get(k)}'" for k, v in EXPECT.items() if v.lower() not in (labels.get(k) or "").lower()]
    if bad:
        sys.exit("Wikidata-IDs passen nicht:\n  " + "\n  ".join(bad))
    print(f"Wikidata-IDs geprüft ({len(EXPECT)}).")


def search(term):
    return api(WD, {"action": "wbsearchentities", "search": term, "language": "en", "limit": 10, "type": "item"}).get("search", [])


def by_identifier(prop, value):
    q = f'haswbstatement:{prop}="{value}"'
    return [h["title"] for h in api(WD, {"action": "query", "list": "search", "srsearch": q, "srnamespace": 0})["query"]["search"]]


# --- Wikidata-Bausteine ---
def ref():
    return [{"snaks": {"P854": [snak("P854", "url", SITE)], "P813": [snak("P813", "time", today())]}}]


def today():
    return {"time": time.strftime("+%Y-%m-%dT00:00:00Z"), "timezone": 0, "before": 0, "after": 0, "precision": 11,
            "calendarmodel": "http://www.wikidata.org/entity/Q1985727"}


def year(y):
    return {"time": f"+{y}-00-00T00:00:00Z", "timezone": 0, "before": 0, "after": 0, "precision": 9,
            "calendarmodel": "http://www.wikidata.org/entity/Q1985727"}


def snak(p, kind, v):
    if kind == "item":
        dv = {"type": "wikibase-entityid", "value": {"entity-type": "item", "id": v}}
    elif kind == "time":
        dv = {"type": "time", "value": v}
    elif kind == "mono":
        dv = {"type": "monolingualtext", "value": {"text": v, "language": "de"}}
    else:
        dv = {"type": "string", "value": v}
    return {"snaktype": "value", "property": p, "datavalue": dv}


def claim(p, kind, v, with_ref=True):
    c = {"mainsnak": snak(p, kind, v), "type": "statement", "rank": "normal"}
    if with_ref:
        c["references"] = ref()
    return c


def label_entity():
    return {
        "labels": {"de": {"language": "de", "value": "Abstract Sound Design"}, "en": {"language": "en", "value": "Abstract Sound Design"}},
        "descriptions": {"de": {"language": "de", "value": "deutsches Independent-Label für Psycore, Hi-Tech und Darkpsy"},
                         "en": {"language": "en", "value": "German independent record label for psycore, hi-tech and dark psytrance"}},
        "claims": [claim("P31", "item", "Q18127"), claim("P17", "item", "Q183"), claim("P571", "time", year(2021)),
                   claim("P856", "url", "https://www.abstract-sound-design.de/", False),
                   claim("P1955", "string", "4052777", False), claim("P3283", "string", "abstract-sound-design", False)],
    }


def artist_entity(label_q):
    c = [claim("P31", "item", "Q5"), claim("P742", "string", "Code Chaos"), claim("P27", "item", "Q183"),
         claim("P551", "item", "Q1055"), claim("P106", "item", "Q183945"), claim("P106", "item", "Q639669"),
         claim("P136", "item", "Q105404852"), claim("P136", "item", "Q114107195"), claim("P136", "item", "Q2452152"),
         claim("P2031", "time", year(2016)), claim("P856", "url", SITE, False),
         claim("P1953", "string", "18204093", False), claim("P434", "string", "14d40d24-a91e-4600-a1b3-d14682d32e42", False),
         claim("P3283", "string", "codechaos", False), claim("P3040", "string", "codechaos", False),
         claim("P2003", "string", "codechaos_official", False), claim("P7085", "string", "codechaos_abstractsound", False),
         claim("P2002", "string", "codechaos_music", False)]
    if label_q:
        c.append(claim("P264", "item", label_q))
    return {
        "labels": {"de": {"language": "de", "value": "Code Chaos"}, "en": {"language": "en", "value": "Code Chaos"}},
        "aliases": {"de": [{"language": "de", "value": "Tim Borchert"}], "en": [{"language": "en", "value": "Tim Borchert"}]},
        "descriptions": {"de": {"language": "de", "value": "deutscher Psytrance-Produzent (Hi-Tech, Psycore, Darkpsy) aus Hamburg"},
                         "en": {"language": "en", "value": "German psytrance producer (hi-tech, psycore, dark psy) from Hamburg"}},
        "claims": c,
    }


def wikidata(apply):
    verify_ids()
    have_artist = by_identifier("P1953", "18204093") or by_identifier("P434", "14d40d24-a91e-4600-a1b3-d14682d32e42")
    have_label = by_identifier("P1955", "4052777")
    print("Vorhanden: Artist", have_artist or "-", "| Label", have_label or "-")
    if not apply:
        print("Probelauf: nichts geschrieben. Mit --apply anlegen.")
        return
    tok = login(WD)
    label_q = have_label[0] if have_label else None
    if not label_q:
        r = api(WD, {"action": "wbeditentity", "new": "item", "data": json.dumps(label_entity()), "token": tok,
                     "summary": "Neues Item: Abstract Sound Design (Label), Angaben laut offizieller Website"}, post=True)
        label_q = r.get("entity", {}).get("id") or sys.exit(f"Label anlegen fehlgeschlagen: {r}")
        print("Label angelegt:", label_q)
    if have_artist:
        print("Artist existiert bereits, nichts angelegt:", have_artist)
        return
    r = api(WD, {"action": "wbeditentity", "new": "item", "data": json.dumps(artist_entity(label_q)), "token": tok,
                 "summary": "Neues Item: Code Chaos (Musikproduzent), Angaben laut offizieller Website; Bearbeiter ist der Künstler selbst"}, post=True)
    artist_q = r.get("entity", {}).get("id") or sys.exit(f"Artist anlegen fehlgeschlagen: {r}")
    print("Artist angelegt:", artist_q)
    api(WD, {"action": "wbcreateclaim", "entity": label_q, "property": "P112", "snaktype": "value",
             "value": json.dumps({"entity-type": "item", "numeric-id": int(artist_q[1:])}), "token": tok,
             "summary": "Gründer ergänzt"}, post=True)
    print(f"Fertig: https://www.wikidata.org/wiki/{artist_q} · https://www.wikidata.org/wiki/{label_q}")


def draft(apply):
    user = os.environ.get("WIKI_USER", "Name@bot").split("@")[0]
    title = f"Benutzer:{user}/Code Chaos"
    text = open(os.path.join(ROOT, "_docs", "wikipedia", "code-chaos.wiki"), encoding="utf-8").read()
    exists = api(DEWP, {"action": "query", "titles": title})["query"]["pages"][0].get("missing") is None
    print(f"Ziel: https://de.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))} ({'existiert schon' if exists else 'neu'})")
    if not apply:
        print("Probelauf: nichts geschrieben. Mit --apply anlegen.")
        return
    if exists:
        sys.exit("Seite existiert bereits, wird nicht überschrieben.")
    tok = login(DEWP)
    r = api(DEWP, {"action": "edit", "title": title, "text": text, "createonly": 1, "token": tok,
                   "summary": "Artikelentwurf Code Chaos. Interessenkonflikt: Ich bin der Künstler selbst."}, post=True)
    if r.get("edit", {}).get("result") != "Success":
        sys.exit(f"Fehlgeschlagen: {r}")
    up = f"Benutzer:{user}"
    note = ("Ich bin Tim Borchert (Code Chaos). Ich schreibe hier über mein eigenes Musikprojekt "
            "und lege damit einen [[Wikipedia:Interessenkonflikt|Interessenkonflikt]] offen.")
    r = api(DEWP, {"action": "edit", "title": up, "appendtext": "\n\n" + note, "token": tok,
                   "summary": "Offenlegung Interessenkonflikt"}, post=True)
    if r.get("edit", {}).get("result") != "Success":
        sys.exit(f"Entwurf angelegt, aber Offenlegung auf {up} fehlgeschlagen, bitte nachtragen: {r}")
    print("Entwurf angelegt, Interessenkonflikt auf der Benutzerseite offengelegt.")


ARTIST_Q = "Q141646843"


def move(apply):
    """Exit 0 = verschoben (oder schon erledigt), 3 = Recht fehlt noch (später erneut), sonst Fehler."""
    user = os.environ.get("WIKI_USER", "Name@bot").split("@")[0]
    src, dst = f"Benutzer:{user}/Code Chaos", "Code Chaos"
    pages = {p["title"]: p for p in api(DEWP, {"action": "query", "titles": f"{src}|{dst}", "prop": "revisions|info",
                                                "rvprop": "user|timestamp"})["query"]["pages"]}
    if pages[dst].get("missing") is None:
        if pages[src].get("missing") is not None or pages[src].get("redirect"):
            print(f"Schon verschoben: https://de.wikipedia.org/wiki/{urllib.parse.quote(dst.replace(' ', '_'))}")
            sys.exit(0)
        sys.exit(f"Ziel „{dst}“ existiert bereits (fremde Seite), nichts verschoben.")
    if pages[src].get("missing") is not None:
        sys.exit("Entwurf fehlt, nichts verschoben.")
    if pages[src]["revisions"][0]["user"] != user:
        sys.exit(f"Letzte Bearbeitung des Entwurfs von {pages[src]['revisions'][0]['user']}, bitte erst ansehen.")
    tok = login(DEWP)
    rights = api(DEWP, {"action": "query", "meta": "userinfo", "uiprop": "rights|groups|editcount"})["query"]["userinfo"]
    if "move" not in rights["rights"]:
        print(f"Verschieberecht fehlt noch (Gruppen {rights['groups']}, {rights['editcount']} Bearbeitungen).")
        sys.exit(3)
    if not apply:
        print("Recht vorhanden. Probelauf: nichts verschoben. Mit --apply verschieben.")
        return
    r = api(DEWP, {"action": "move", "from": src, "to": dst, "token": tok, "movetalk": 1,
                   "reason": "Entwurf in den Artikelnamensraum. Interessenkonflikt: Ich bin der Künstler selbst (offengelegt auf meiner Benutzerseite)."},
            post=True)
    if "move" not in r:
        sys.exit(f"Verschieben fehlgeschlagen: {r.get('error', r)}")
    print(f"Verschoben: https://de.wikipedia.org/wiki/{urllib.parse.quote(dst.replace(' ', '_'))}")
    wtok = login(WD)
    r = api(WD, {"action": "wbsetsitelink", "id": ARTIST_Q, "linksite": "dewiki", "linktitle": dst, "token": wtok,
                 "summary": "Sitelink zum de.wikipedia-Artikel"}, post=True)
    print("Wikidata-Sitelink:", "ok" if r.get("success") else r.get("error", r))


ARTICLE = "Code Chaos"
MARKERS = {"Löschantrag": ("{{Löschantragstext", "{{Löschantrag"), "Schnelllöschantrag": ("{{Löschen", "{{SLA"),
           "Qualitätssicherung": ("{{QS-", "{{QS|"), "Relevanzfrage": ("{{Relevanzcheck", "{{Relevanz")}


def ld_page(text):
    """Löschdiskussionsseite aus {{Löschantragstext|tag=..|monat=..|jahr=..}} ableiten."""
    import re
    m = re.search(r"\{\{Löschantragstext([^}]*)\}\}", text)
    if not m:
        return None
    kv = dict(re.findall(r"\|\s*(tag|monat|jahr)\s*=\s*([^|}]+)", m.group(1)))
    if len(kv) < 3:
        return None
    return f"Wikipedia:Löschkandidaten/{kv['tag'].strip()}. {kv['monat'].strip()} {kv['jahr'].strip()}"


def watch(hours=26):
    """Exit 0 = nichts Neues, 10 = Handlungsbedarf (LA/SLA/QS/fremde Edits/Diskussion), 20 = Artikel weg."""
    user = os.environ.get("WIKI_USER", "Name@bot").split("@")[0]
    since = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - hours * 3600))
    pages = {p["title"]: p for p in api(DEWP, {"action": "query", "titles": f"{ARTICLE}|Diskussion:{ARTICLE}",
                                                "prop": "revisions|info", "rvprop": "user|timestamp|comment|content",
                                                "rvslots": "main"})["query"]["pages"]}
    art = pages[ARTICLE]
    if art.get("missing") is not None or art.get("redirect"):
        log = api(DEWP, {"action": "query", "list": "logevents", "letitle": ARTICLE, "lelimit": 3})["query"]["logevents"]
        print("ARTIKEL FEHLT oder ist Weiterleitung. Letzte Logbuch-Einträge:",
              [(l["type"], l["action"], l["user"], l["timestamp"], l.get("comment", "")) for l in log])
        sys.exit(20)
    text = art["revisions"][0]["slots"]["main"]["content"]
    found = [name for name, keys in MARKERS.items() if any(k in text for k in keys)]
    action = bool(found)
    print("Bausteine im Artikel:", found or "keine")
    if "Löschantrag" in found:
        print("Löschdiskussion:", ld_page(text) or "(Seite aus Baustein nicht ermittelbar)")
    for title in (ARTICLE, f"Diskussion:{ARTICLE}"):
        if pages[title].get("missing") is not None:
            print(f"{title}: existiert nicht")
            continue
        revs = api(DEWP, {"action": "query", "prop": "revisions", "titles": title, "rvlimit": 20, "rvend": since,
                          "rvprop": "user|timestamp|comment"})["query"]["pages"][0].get("revisions", [])
        foreign = [r for r in revs if r["user"] != user]
        print(f"{title}: {len(revs)} Bearbeitungen in {hours} h, davon fremd:",
              [(r["user"], r["timestamp"], r.get("comment", "")[:80]) for r in foreign] or "keine")
        action = action or bool(foreign)
    sys.exit(10 if action else 0)


def reply(page, section_hint, path, apply):
    """Hängt einmalig eine signierte Antwort an den Abschnitt an, dessen Überschrift section_hint enthält."""
    user = os.environ.get("WIKI_USER", "Name@bot").split("@")[0]
    secs = api(DEWP, {"action": "parse", "page": page, "prop": "sections"})["parse"]["sections"]
    hits = [x for x in secs if section_hint.lower() in x["line"].lower()]
    if len(hits) != 1:
        sys.exit(f"Abschnitt „{section_hint}“ auf {page} nicht eindeutig gefunden: {[x['line'] for x in hits]}")
    idx = hits[0]["index"]
    cur = api(DEWP, {"action": "parse", "page": page, "section": idx, "prop": "wikitext"})["parse"]["wikitext"]
    if f"[[Benutzer:{user}" in cur or f"[[User:{user}" in cur:
        sys.exit(f"Im Abschnitt steht schon ein Beitrag von {user}; keine zweite automatische Antwort.")
    body = open(path, encoding="utf-8").read().strip()
    if "~~~~" not in body:
        body += " ~~~~"
    print(f"Ziel: {page} § {hits[0]['line']}\n---\n{body}\n---")
    if not apply:
        print("Probelauf: nichts gespeichert. Mit --apply speichern.")
        return
    tok = login(DEWP)
    r = api(DEWP, {"action": "edit", "title": page, "section": idx, "appendtext": "\n:" + body.replace("\n", "\n:"),
                   "token": tok, "summary": "/* " + hits[0]["line"] + " */ Antwort (Interessenkonflikt: ich bin der Künstler)"},
            post=True)
    if r.get("edit", {}).get("result") != "Success":
        sys.exit(f"Speichern fehlgeschlagen: {r}")
    print("Antwort gespeichert, Revision", r["edit"].get("newrevid"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    apply = "--apply" in sys.argv
    if cmd == "check":
        verify_ids(); wikidata(False); draft(False)
    elif cmd == "wikidata":
        wikidata(apply)
    elif cmd == "draft":
        draft(apply)
    elif cmd == "move":
        move(apply)
    elif cmd == "watch":
        watch(int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 26)
    elif cmd == "reply" and len(sys.argv) >= 5:
        reply(sys.argv[2], sys.argv[3], sys.argv[4], apply)
    else:
        sys.exit(__doc__)
