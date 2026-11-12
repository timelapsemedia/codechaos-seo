"""Gemessene Lautheitsdaten (Grok #72, 12.11.2026): Markdown -> HTML für /psy-lautheit-daten/ + /en/psy-loudness-data/.

Quellen in _build/daten/ sind Kopien aus C:/traffic/seiten/ (Texte der Session Traffic P6, Tabellen von genre_index.py).
Zahlen nie hier oder in den .md-Dateien von Hand ändern: genre_index.py neu laufen lassen und die Dateien erneut kopieren.
"""
import html, os, re

DATEN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "daten")


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip().strip('"')
    return meta, text[m.end():]


def inline(s):
    s = html.escape(s, quote=False).replace("\\*", "&#42;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)


def bloecke(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [l for l in block.strip().splitlines() if l.strip()]
        if not lines:
            continue
        if lines[0].startswith("## "):
            out.append(("h2", lines[0][3:].strip()))
            lines = lines[1:]
            if not lines:
                continue
        if all(l.startswith("|") for l in lines):
            out.append(("table", [[c.strip() for c in l.strip().strip("|").split("|")]
                                  for l in lines if not re.match(r"^\|[\s|:-]+\|$", l)]))
        elif all(l.startswith("- ") for l in lines):
            out.append(("ul", [l[2:] for l in lines]))
        else:
            out.append(("p", "\n".join(lines)))
    return out


def block_html(b):
    typ, inhalt = b
    if typ == "p":
        cls = ' class="note"' if inhalt.startswith("\\*") else ""
        text = inline(inhalt).replace("\n", " ")
        return f"<p{cls}>{text}</p>"
    if typ == "ul":
        return "<ul>" + "".join(f"<li>{inline(i)}</li>" for i in inhalt) + "</ul>"
    if typ == "table":
        kopf, *rows = inhalt
        th = "".join(f'<th scope="col">{inline(c)}</th>' for c in kopf)
        tr = "".join(f'<tr><th scope="row">{inline(r[0])}</th>' + "".join(f"<td>{inline(c)}</td>" for c in r[1:]) + "</tr>" for r in rows)
        return f'<div class="table-scroll"><table class="cmp"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
    raise ValueError(typ)


def faq(bl):
    """'**Frage?**\\nAntwort' -> [(frage, antwort_html)], übrige Blöcke getrennt."""
    faqs, rest = [], []
    for b in bl:
        m = re.match(r"\*\*(.+?\?)\*\*\n(.+)", b[1], re.S) if b[0] == "p" else None
        if m:
            faqs.append((m.group(1).strip(), inline(m.group(2).strip()).replace("\n", " ")))
        else:
            rest.append(b)
    return faqs, rest


def lesen(lang):
    """(meta, intro_bloecke, [(h2, bloecke)]) mit den Tabellen an der TABELLEN-Markierung."""
    with open(os.path.join(DATEN_DIR, f"seite_codechaos_{lang}.md"), encoding="utf-8") as f:
        meta, body = frontmatter(f.read())
    with open(os.path.join(DATEN_DIR, f"tabellen_codechaos_{lang}.md"), encoding="utf-8") as f:
        tabellen = f.read()
    marke = re.search(r"<!-- TABELLEN:[^>]*-->", body)
    assert marke, f"seite_codechaos_{lang}.md: TABELLEN-Markierung fehlt"
    body = body[:marke.start()] + "\n\n" + tabellen + "\n\n" + body[marke.end():]
    intro, sections = [], []
    for b in bloecke(body):
        if b[0] == "h2":
            sections.append((b[1], []))
        elif sections:
            sections[-1][1].append(b)
        else:
            intro.append(b)
    return meta, intro, sections
