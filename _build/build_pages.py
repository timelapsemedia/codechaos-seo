#!/usr/bin/env python3
"""Erzeugt die Genre-Unterseiten (DE + EN) und die englische Startseite.

Aufruf aus dem Repo-Root:  python3 _build/build_pages.py
Inhalte stehen in _build/content_genres.py und _build/content_en_home.py.
Der Ordner _build wird von GitHub Pages nicht veröffentlicht.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_genres import GENRES, RELEASES          # noqa: E402
from content_en_home import EN_HOME                   # noqa: E402
from content_en_mastering import EN_MASTERING, FORM   # noqa: E402
from content_de_mastering import DE_MASTERING, FORM_DE  # noqa: E402
from flags import UK as FLAG_UK, DE as FLAG_DE       # noqa: E402
from content_plugins import PLUGINS, CRUCIBLE, GROUPS, GENRE_PLUGINS, GUMROAD  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://codechaos-official.de"
TODAY = "2026-10-05"
PLUGIN_DATE = "2026-10-21"      # Plugin-Seiten erstellt/geändert
GENRE_DE_MODIFIED = "2026-10-21"  # DE-Genre-Seiten: Plugin-Block ergänzt
ARTIST = BASE + "/#artist"
PERSON = BASE + "/#tim-borchert"

UI = {
    "de": dict(home="Startseite", genres="Genres", releases="Releases", mastering="Mastering", lang_label="EN",
               skip="Zum Inhalt springen", menu="Menü öffnen", faq="Häufige Fragen", rel_title="Releases von Code Chaos",
               more="Weiterlesen", legal="Rechtliches", imprint="Impressum", privacy="Datenschutz", nav="Navigation",
               follow="Code Chaos folgen", other="Weitere Genre-Guides", foot="Hitech, Psycore & Darkpsy Producer aus Hamburg. Heute ein reines Studioprojekt.",
               home_url="/", mastering_url="/mastering/", releases_url="/#releases",
               author="Von Code Chaos (Tim Borchert), Producer aus Hamburg · aktualisiert am 21.10.2026"),
    "en": dict(home="Home", genres="Genres", releases="Releases", mastering="Mastering", lang_label="DE",
               skip="Skip to content", menu="Open menu", faq="FAQ", rel_title="Releases by Code Chaos",
               more="Read more", legal="Legal", imprint="Imprint (German)", privacy="Privacy policy (German)", nav="Navigation",
               follow="Follow Code Chaos", other="More genre guides", foot="Hitech, Psycore & Darkpsy producer from Hamburg, Germany. Studio project.",
               home_url="/en/", mastering_url="/en/mastering/", releases_url="/en/#releases",
               author="By Code Chaos (Tim Borchert), producer from Hamburg · updated 5 Oct 2026"),
}

SOCIAL = [("Bandcamp", "https://codechaos.bandcamp.com"), ("SoundCloud", "https://soundcloud.com/codechaos"),
          ("Instagram", "https://www.instagram.com/codechaos_official"), ("TikTok", "https://www.tiktok.com/@codechaos_abstractsound"),
          ("YouTube", "https://www.youtube.com/@codechaos_abstractsounddesign"), ("X", "https://x.com/codechaos_music"),
          ("Threads", "https://www.threads.net/@codechaos_official")]


def esc(t):
    return t.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def head(lang, url, alt_url, title, desc, og_image, og_alt, ld, og_type="article"):
    de_url, en_url = (url, alt_url) if lang == "de" else (alt_url, url)
    if alt_url is None:  # Seite ohne Gegenstück in der anderen Sprache
        alternates = f'<link rel="alternate" hreflang="{lang}" href="{url}">'
    else:
        alternates = (f'<link rel="alternate" hreflang="de" href="{de_url}">\n<link rel="alternate" hreflang="en" href="{en_url}">\n'
                      f'<link rel="alternate" hreflang="x-default" href="{de_url}">')
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Code Chaos">
<meta name="theme-color" content="#0b0806">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="{url}">
{alternates}
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Code Chaos">
<meta property="og:locale" content="{'de_DE' if lang == 'de' else 'en_US'}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@codechaos_music">
<meta name="twitter:image" content="{og_image}">
<link rel="preload" as="font" type="font/woff2" href="/fonts/cinzel.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/fonts/eb-garamond.woff2" crossorigin>
<link rel="stylesheet" href="/css/fonts.css">
<link rel="stylesheet" href="/css/sub.css">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
"""


def nav(lang, alt_url, current):
    u = UI[lang]
    pre = "" if lang == "de" else "/en"
    items = [(u["home"], u["home_url"], "home")]
    for g in GENRES:
        items.append((g[lang]["nav"], f"{pre}/{g['slug']}/", g["slug"]))
    items += [(u["releases"], u["releases_url"], "rel"), (u["mastering"], u["mastering_url"], "mast"),
              ("Plugins", "/plugins/", "plug") if lang == "de" else ("Crucible", "/crucible.html", "cru")]
    cur = ' aria-current="page"'
    lis = "".join(
        f'<li><a href="{h}"{cur if k == current else ""}>{esc(t)}</a></li>' for t, h, k in items)
    alt_href = (alt_url or BASE + ("/en/" if lang == "de" else "/")).replace(BASE, "")
    other = "en" if lang == "de" else "de"
    switch = (f'<a class="lang-switch" href="{alt_href}" hreflang="{other}" lang="{other}" aria-label="{"English version" if lang == "de" else "Deutsche Version"}">'
              f'{FLAG_UK if lang == "de" else FLAG_DE}<span>{other.upper()}</span></a>')
    return f"""<body>
<a class="skip" href="#main">{u['skip']}</a>
<header>
<nav class="s-nav" aria-label="{u['nav']}">
  <a class="logo" href="{u['home_url']}"><img src="/images/brand/codechaos-logo-bone-240.webp" srcset="/images/brand/codechaos-logo-bone-240.webp 1x, /images/brand/codechaos-logo-bone-480.webp 2x" width="68" height="40" alt="Code Chaos Logo"></a>
  <button class="s-toggle" aria-label="{u['menu']}" aria-expanded="false" aria-controls="s-menu"><span></span><span></span><span></span></button>
  <ul id="s-menu">{lis}</ul>
  {switch}
</nav>
</header>
"""


def footer(lang):
    u = UI[lang]
    pre = "" if lang == "de" else "/en"
    genre_links = "".join(f'<li><a href="{pre}/{g["slug"]}/">{esc(g[lang]["nav"])}</a></li>' for g in GENRES)
    social = "".join(f'<li><a href="{h}" target="_blank" rel="noopener noreferrer me">{n}</a></li>' for n, h in SOCIAL)
    return f"""<footer class="s-foot">
  <div class="wrap">
    <div class="cols">
      <div><img src="/images/brand/codechaos-logo-bone-240.webp" width="120" height="70" loading="lazy" alt="Code Chaos Logo" style="height:70px;width:auto;margin-bottom:10px"><p>{esc(u['foot'])}</p></div>
      <div><h2>{u['genres']}</h2><ul>{genre_links}<li><a href="/crucible.html">Crucible Plugin</a></li>{'<li><a href="/plugins/">Alle Plugins</a></li>' if lang == "de" else ""}</ul></div>
      <div><h2>{u['follow']}</h2><ul>{social}</ul></div>
      <div><h2>{u['legal']}</h2><ul><li><a href="/#impressum">{u['imprint']}</a></li><li><a href="/#datenschutz">{u['privacy']}</a></li><li><a href="#cookies" class="cookie-settings-link">{'Cookie-Einstellungen' if lang == 'de' else 'Cookie settings'}</a></li><li><a href="{'/en/' if lang == 'de' else '/'}" hreflang="{'en' if lang == 'de' else 'de'}">{'English version' if lang == 'de' else 'Deutsche Version'}</a></li></ul></div>
    </div>
    <p class="copy">© 2016–2026 CODE CHAOS · ABSTRACT SOUND DESIGN · HAMBURG</p>
  </div>
</footer>
<script>
(function(){{var b=document.querySelector('.s-toggle'),m=document.getElementById('s-menu');if(!b||!m)return;
b.addEventListener('click',function(){{var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');}});}})();
document.addEventListener('click',function(e){{var a=e.target.closest&&e.target.closest('[data-pick]');if(!a)return;var s=document.querySelector('select[name=service]');if(!s)return;
for(var i=0;i<s.options.length;i++){{if(s.options[i].text===a.getAttribute('data-pick')){{s.selectedIndex=i;break;}}}}}});
</script>
<script src="/js/analytics-consent.js" defer></script>
</body>
</html>
"""


def release_grid(keys, lang):
    out = []
    for k in keys:
        r = RELEASES[k]
        ext = ' target="_blank" rel="noopener noreferrer"' if r["url"].startswith("http") else ""
        out.append(f'<a href="{r["url"]}"{ext}>'
                   f'<img src="{r["img"]}" width="300" height="300" loading="lazy" decoding="async" alt="{esc("Code Chaos " + r["title"] + " Cover")}">'
                   f'<span>{esc(r["title"])}<small>{esc(r[lang])}</small></span></a>')
    return '<div class="rel">' + "".join(out) + "</div>"


def faq_html(items):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>"


def strip(t):
    import re, html
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", t))).strip()


def build_genre(g, lang):
    c = g[lang]
    u = UI[lang]
    pre = "" if lang == "de" else "/en"
    url = f"{BASE}{pre}/{g['slug']}/"
    alt = f"{BASE}{'/en' if lang == 'de' else ''}/{g['slug']}/"
    others = [o for o in GENRES if o is not g]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url + "#article", "headline": c["h1"], "description": c["desc"], "inLanguage": lang,
         "url": url, "mainEntityOfPage": url, "datePublished": TODAY, "dateModified": GENRE_DE_MODIFIED if lang == "de" else TODAY,
         "author": {"@id": PERSON}, "publisher": {"@id": ARTIST}, "image": BASE + g["og"],
         "about": {"@type": "DefinedTerm", "name": g["term"], "description": strip(c["answer"]),
                   "inDefinedTermSet": {"@type": "DefinedTermSet", "name": "Psytrance-Subgenres" if lang == "de" else "Psytrance subgenres"}},
         "isPartOf": {"@id": BASE + ("/#website")}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": u["home"], "item": BASE + u["home_url"]},
            {"@type": "ListItem", "position": 2, "name": c["nav"], "item": url}]},
        {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": lang, "mainEntity": [
            {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in c["faq"]]},
    ]}
    specs = "".join(f"<tr><th scope=\"row\">{k}</th><td>{v}</td></tr>" for k, v in c["specs"])
    other_cards = "".join(
        f'<div class="card"><div class="bpm">{o[lang]["bpm"]}</div><h3>{esc(o[lang]["nav"])}</h3><p>{o[lang]["teaser"]}</p>'
        f'<a class="more" href="{pre}/{o["slug"]}/">{u["more"]} →</a></div>' for o in others)
    body = f"""<main id="main">
<div class="wrap crumbs"><nav aria-label="Breadcrumb"><ol><li><a href="{u['home_url']}">{u['home']}</a></li><li aria-current="page">{esc(c['nav'])}</li></ol></nav></div>
<section class="s-hero">
  <div class="wrap narrow">
    <span class="eyebrow">{c['eyebrow']}</span>
    <h1>{c['h1']}</h1>
    <div class="rule" aria-hidden="true"><i></i></div>
    <p class="answer">{c['answer']}</p>
    <p class="note">{u['author']}</p>
  </div>
</section>
<section class="alt" aria-labelledby="specs-t">
  <div class="wrap narrow">
    <h2 id="specs-t">{c['specs_title']}</h2>
    <div class="table-scroll"><table class="specs"><tbody>{specs}</tbody></table></div>
  </div>
</section>
<section>
  <div class="wrap narrow prose">
{c['body']}
  </div>
</section>
<section class="alt" aria-labelledby="rel-t">
  <div class="wrap">
    <h2 id="rel-t">{c['rel_title']}</h2>
    <p class="prose">{c['rel_intro']}</p>
    {release_grid(g['releases'], lang)}
  </div>
</section>
<section aria-labelledby="faq-t">
  <div class="wrap narrow">
    <h2 id="faq-t">{u['faq']}: {esc(c['nav'])}</h2>
    {faq_html(c['faq'])}
  </div>
</section>
<section class="alt" aria-labelledby="cta-t">
  <div class="wrap narrow prose">
    <h2 id="cta-t">{c['cta_title']}</h2>
    <p>{c['cta']}</p>
    <div class="btns"><a class="btn btn-blood" href="{u['mastering_url']}">{c['cta_btn1']}</a><a class="btn btn-ghost" href="/crucible.html">Crucible Plugin</a></div>
  </div>
</section>
{genre_plugins_html(g, lang)}<section aria-labelledby="other-t">
  <div class="wrap">
    <h2 id="other-t">{u['other']}</h2>
    <div class="cards">{other_cards}</div>
  </div>
</section>
</main>
"""
    html = head(lang, url, alt, c["title"], c["desc"], BASE + g["og"], c["og_alt"], ld) + nav(lang, alt, g["slug"]) + body + footer(lang)
    path = os.path.join(ROOT, pre.strip("/"), g["slug"], "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html)
    return path


def build_en_home():
    h = EN_HOME
    url, alt = BASE + "/en/", BASE + "/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": h["title"], "description": h["desc"], "inLanguage": "en",
         "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": ARTIST}, "mainEntity": {"@id": ARTIST},
         "primaryImageOfPage": {"@type": "ImageObject", "url": BASE + "/images/uhrwerk-aus-blut/og-uhrwerk-aus-blut.jpg"},
         "datePublished": TODAY, "dateModified": TODAY},
        {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": "en", "mainEntity": [
            {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in h["faq"]]},
    ]}
    genre_cards = "".join(
        f'<div class="card"><div class="bpm">{g["en"]["bpm"]}</div><h3>{esc(g["en"]["nav"])}</h3><p>{g["en"]["teaser"]}</p>'
        f'<a class="more" href="/en/{g["slug"]}/">Read the guide →</a></div>' for g in GENRES)
    body = h["body"].format(
        releases=release_grid(list(RELEASES.keys()), "en"),
        genre_cards=genre_cards,
        faq=faq_html(h["faq"]),
        social="".join(f'<li><a href="{hh}" target="_blank" rel="noopener noreferrer me">{n}</a></li>' for n, hh in SOCIAL),
    )
    html = head("en", url, alt, h["title"], h["desc"], BASE + "/images/uhrwerk-aus-blut/og-uhrwerk-aus-blut.jpg",
                "Uhrwerk aus Blut: a golden mechanical heart inside a clock face, dripping blood", ld, og_type="website") \
        + nav("en", alt, "home") + body + footer("en")
    path = os.path.join(ROOT, "en", "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html)
    return path


def build_mastering(lang):
    m, form = (DE_MASTERING, FORM_DE) if lang == "de" else (EN_MASTERING, FORM)
    pre = "" if lang == "de" else "/en"
    url = f"{BASE}{pre}/mastering/"
    alt = f"{BASE}{'/en' if lang == 'de' else ''}/mastering/"
    if lang == "de":
        offers = [("Single: Stereo Mastering (1 Track)", "79"), ("Stem Pro: Stem Mastering (1 Track, bis 6 Stems)", "129"), ("EP Mastering (bis 5 Tracks)", "349"),
                  ("Album Mastering (bis 10 Tracks)", "629"), ("Cover Art", "99"), ("Lyric Video", "179"), ("Promo Video (60 Sekunden)", "299")]
        sname, home = "Psytrance Mastering für Psycore, Hitech und Darkpsy", "Startseite"
    else:
        offers = [("Single: stereo mastering (1 track)", "79"), ("Stem Pro: stem mastering (1 track, up to 6 stems)", "129"), ("EP mastering (up to 5 tracks)", "349"),
                  ("Album mastering (up to 10 tracks)", "629"), ("Cover art", "99"), ("Lyric video", "179"), ("Promo video (60 s)", "299")]
        sname, home = "Psytrance mastering for psycore, hitech and darkpsy", "Home"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": m["title"], "description": m["desc"], "inLanguage": lang,
         "isPartOf": {"@id": BASE + "/#website"}, "mainEntity": {"@id": url + "#service"}, "datePublished": TODAY, "dateModified": TODAY},
        {"@type": "Service", "@id": url + "#service", "name": sname, "serviceType": "Audio Mastering",
         "description": m["desc"], "provider": {"@id": "https://polished.media/#org"}, "areaServed": "Worldwide", "availableLanguage": ["de", "en"], "url": url,
         "offers": [{"@type": "Offer", "name": n, "price": p, "priceCurrency": "EUR", "url": url + "#request", "priceSpecification": {"@type": "PriceSpecification", "price": p, "priceCurrency": "EUR", "valueAddedTaxIncluded": True}} for n, p in offers]},
        {"@type": "Organization", "@id": "https://polished.media/#org", "name": "Polished Media", "url": "https://polished.media", "email": "polished.media@gmx.de", "founder": {"@id": PERSON}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": home, "item": BASE + UI[lang]["home_url"]},
            {"@type": "ListItem", "position": 2, "name": "Mastering", "item": url}]},
        {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": lang, "mainEntity": [
            {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in m["faq"]]},
    ]}
    cta = "Mastering anfragen · ab 79 €" if lang == "de" else "Request mastering · from €79"
    body = m["body"].replace("{faq}", faq_html(m["faq"])).replace("{form}", form) \
        + f'<a class="sticky-cta" href="#request">{cta}</a>\n'
    html = head(lang, url, alt, m["title"], m["desc"], BASE + "/images/og/mastering.jpg",
                "Psytrance Mastering für Psycore, Hitech und Darkpsy von Code Chaos" if lang == "de" else "Psytrance mastering for psycore, hitech and darkpsy by Code Chaos", ld, og_type="website") \
        + nav(lang, alt, "mast") + body + footer(lang)
    path = os.path.join(ROOT, pre.strip("/"), "mastering", "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html)
    return path

def build_404():
    body = """<main id="main">
<section class="s-hero">
  <div class="wrap narrow">
    <span class="eyebrow">Fehler 404 · Error 404</span>
    <h1>Diese Seite ist im Uhrwerk verschwunden.</h1>
    <div class="rule" aria-hidden="true"><i></i></div>
    <p class="lead">Die Adresse gibt es nicht (mehr). This page does not exist.</p>
    <div class="btns"><a class="btn btn-blood" href="/">Zur Startseite</a><a class="btn btn-ghost" href="/mastering/">Mastering ab 79 €</a><a class="btn btn-ghost" href="/en/" hreflang="en" lang="en">English</a></div>
  </div>
</section>
<section class="alt">
  <div class="wrap">
    <h2>Beliebte Seiten</h2>
    <div class="cards">
      <div class="card"><h3>Uhrwerk aus Blut</h3><p>Die neue Single, erscheint am 30.10.2026.</p><a class="more" href="/#single">Zur Single →</a></div>
      <div class="card"><h3>Mastering</h3><p>Psycore, Hitech &amp; Darkpsy: Single 79 €, EP 349 €, Album 629 €.</p><a class="more" href="/mastering/">Preise &amp; Ablauf →</a></div>
      <div class="card"><h3>Genre Guides</h3><p><a href="/psycore/">Psycore</a> · <a href="/hitech-psytrance/">Hitech</a> · <a href="/darkpsy/">Darkpsy</a></p></div>
      <div class="card"><h3>Crucible</h3><p>3-Band Harmonic Saturation Plugin von Code Chaos Audio.</p><a class="more" href="/crucible.html">Zum Plugin →</a></div>
    </div>
  </div>
</section>
</main>
"""
    html = head("de", BASE + "/404.html", None, "Seite nicht gefunden | Code Chaos", "Diese Seite existiert nicht. Zur Startseite von Code Chaos.",
                BASE + "/images/uhrwerk-aus-blut/og-uhrwerk-aus-blut.jpg", "Code Chaos", {"@context": "https://schema.org", "@type": "WebPage", "name": "404"}, og_type="website")
    html = html.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex, follow">')
    html = "\n".join(l for l in html.split("\n") if not l.startswith('<link rel="canonical"') and not l.startswith('<link rel="alternate"'))
    html += nav("de", BASE + "/en/", "") + body + footer("de")
    open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(html)
    return os.path.join(ROOT, "404.html")



# ───────────────────────── Plugin-Seiten (/plugins/, /plugins/<slug>/) ─────────────────────────
# Inhalte: _build/content_plugins.py · Bilder/Audio: python3 _build/plugin_assets.py
# Nur Einträge mit live=True werden gebaut (Gumroad-Seite muss erreichbar sein).

LIVE = [p for p in PLUGINS if p["live"]]
BY_SLUG = {p["slug"]: p for p in LIVE}
BY_SLUG["crucible"] = CRUCIBLE


def utm(slug, campaign):
    return f"{GUMROAD}{slug}?utm_source=site&amp;utm_medium=landing&amp;utm_campaign={campaign}"


def euro(price):
    return "kostenlos" if price == 0 else f"{price} €"


def plugin_url(p):
    return p.get("url") or f"/plugins/{p['slug']}/"


def gui_h(p, w=880):
    return round(p["gui_h"] * w / p["gui_w"])


def picture(slug, name, w, h, alt, lazy=True, has_1600=True, sizes="(max-width: 900px) 100vw, 520px"):
    base = f"/images/plugins/{slug}/{name}"
    srcset = f"{base}-880.webp 880w" + (f", {base}-1600.webp 1600w" if has_1600 else "")
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    return (f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
            f'<img src="{base}-880.jpg" width="880" height="{round(h * 880 / w)}" {load} alt="{esc(alt)}"></picture>')


def cta_buttons(p, campaign, big=True):
    """Kauf- und Demo-Buttons. Gratis-Plugin: nur ein Download-Button."""
    if p["price"] == 0:
        return f'<a class="btn btn-blood" href="{utm(p["slug"], campaign)}">Kostenlos herunterladen</a>'
    return (f'<a class="btn btn-blood" href="{utm(p["slug"], campaign)}">Kaufen · {euro(p["price"])}</a>'
            f'<a class="btn btn-ghost" href="{utm(p["slug"] + "-demo", campaign)}">Kostenlose Demo</a>')


def plugin_card(p, campaign):
    """Karte für Übersicht und Querverweise: Bild, 1 Satz, Preis, Links."""
    if p["slug"] == "crucible":
        img = (f'<picture><source type="image/webp" srcset="{p["img_webp"]}"><img src="{p["img_jpg"]}" width="{p["w"]}" height="{p["h"]}" '
               f'loading="lazy" decoding="async" alt="{esc(p["alt"])}"></picture>')
        os_line = p["os"]
    else:
        img = picture(p["slug"], "gui", p["gui_w"], p["gui_h"], p["gui_alt"], sizes="(max-width: 700px) 100vw, 340px")
        os_line = p["os"]
    links = (f'<a href="{utm(p["slug"], campaign)}">Kostenlos laden</a>' if p["price"] == 0 else
             f'<a href="{utm(p["slug"] + "-demo", campaign)}">Kostenlose Demo</a><a href="{utm(p["slug"], campaign)}">Kaufen</a>')
    return (f'<article class="pcard"><a class="pcard-img" href="{plugin_url(p)}" tabindex="-1" aria-hidden="true">{img}</a>'
            f'<div class="pcard-body"><h3><a href="{plugin_url(p)}">{esc(p["name"])}</a></h3><p>{p["teaser"]}</p>'
            f'<p class="pcard-meta"><span class="price-tag">{euro(p["price"])}</span> {esc(os_line)}</p>'
            f'<p class="pcard-links"><a href="{plugin_url(p)}">Details &amp; Hörprobe</a>{links}</p></div></article>')


def audio_html(p):
    if not p.get("audio"):
        return ""
    base = f"/audio/plugins/{p['slug']}/"
    if p["audio_mode"] == "ab":
        a, b = p["audio"]
        player = f"""<div class="ab">
      <audio id="ab-a" src="{base}{a['file']}" preload="metadata" loop></audio>
      <audio id="ab-b" src="{base}{b['file']}" preload="metadata" loop></audio>
      <div class="ab-row">
        <button type="button" class="ab-play" id="ab-play">▶ Abspielen</button>
        <button type="button" id="ab-dry" aria-pressed="true">{esc(a['label'])}</button>
        <button type="button" id="ab-wet" aria-pressed="false">{esc(b['label'])}</button>
      </div>
    </div>
<script>
(function(){{var a=document.getElementById('ab-a'),b=document.getElementById('ab-b'),p=document.getElementById('ab-play'),d=document.getElementById('ab-dry'),w=document.getElementById('ab-wet');if(!a||!b)return;
var wet=false,playing=false;function mix(){{a.muted=wet;b.muted=!wet;d.setAttribute('aria-pressed',wet?'false':'true');w.setAttribute('aria-pressed',wet?'true':'false');}}
p.addEventListener('click',function(){{if(playing){{a.pause();b.pause();playing=false;p.textContent='▶ Abspielen';return;}}
b.currentTime=a.currentTime;mix();Promise.all([a.play(),b.play()]).then(function(){{playing=true;p.textContent='❚❚ Pause';}}).catch(function(){{}});}});
d.addEventListener('click',function(){{wet=false;mix();}});w.addEventListener('click',function(){{wet=true;if(playing&&Math.abs(a.currentTime-b.currentTime)>0.05)b.currentTime=a.currentTime;mix();}});mix();}})();
</script>"""
    else:
        parts = []
        for a in p["audio"]:
            ch = ""
            if a.get("chapters"):
                ch = '<ol class="chapters">' + "".join(f"<li><span>{t}</span> {esc(l)}</li>" for t, l in a["chapters"]) + "</ol>"
            parts.append(f'<figure class="track"><figcaption>{esc(a["label"])}</figcaption>'
                         f'<audio controls preload="metadata" src="{base}{a["file"]}"></audio>{ch}</figure>')
        player = "".join(parts)
    note = f'<p class="note">{esc(p["audio_note"])}</p>' if p.get("audio_note") else ""
    return f"""<section class="alt" id="hoeren" aria-labelledby="hoeren-t">
  <div class="wrap narrow">
    <h2 id="hoeren-t">{esc(p['name'])} anhören</h2>
    <p class="prose">{esc(p['audio_intro'])}</p>
    {player}
    {note}
  </div>
</section>
"""


def build_plugin(p):
    slug, name = p["slug"], p["name"]
    url = f"{BASE}/plugins/{slug}/"
    og = f"{BASE}/images/plugins/{slug}/og.jpg"
    buy, demo = GUMROAD + slug, GUMROAD + slug + "-demo"
    price = f"{p['price']:.2f}"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p["title"], "description": p["desc"], "inLanguage": "de",
         "isPartOf": {"@id": BASE + "/#website"}, "mainEntity": {"@id": url + "#product"}, "primaryImageOfPage": {"@type": "ImageObject", "url": og, "width": 1200, "height": 630},
         "datePublished": PLUGIN_DATE, "dateModified": PLUGIN_DATE},
        {"@type": ["Product", "SoftwareApplication"], "@id": url + "#product", "name": name, "description": strip(p["answer"]),
         "applicationCategory": "MultimediaApplication", "applicationSubCategory": p["sub"], "operatingSystem": p["os"],
         "brand": {"@type": "Brand", "name": "Code Chaos Audio"}, "category": "Audio Plugin",
         "image": og, "screenshot": f"{BASE}/images/plugins/{slug}/gui-880.jpg", "url": url,
         "downloadUrl": buy, "featureList": [strip(f) for f in p["features"]],
         "offers": {"@type": "Offer", "url": buy, "price": price, "priceCurrency": "EUR", "availability": "https://schema.org/InStock",
                    "seller": {"@type": "Organization", "name": "Code Chaos Audio", "url": BASE + "/plugins/"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Startseite", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Plugins", "item": BASE + "/plugins/"},
            {"@type": "ListItem", "position": 3, "name": name, "item": url}]},
        {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": "de", "mainEntity": [
            {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in p["faq"]]},
    ]}
    if p["price"] > 0:
        ld["@graph"][1]["isRelatedTo"] = {"@type": "SoftwareApplication", "name": f"{name} Demo", "url": demo,
                                          "applicationCategory": "MultimediaApplication", "operatingSystem": p["os"],
                                          "offers": {"@type": "Offer", "price": "0.00", "priceCurrency": "EUR", "url": demo}}
    specs = "".join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in p["specs"])
    feats = "".join(f"<li>{f}</li>" for f in p["features"])
    fmt_line = "VST3 + Standalone · " + p["os"]
    extra_imgs = "".join(
        f'<figure class="shot">{picture(slug, i["name"], i["w"], i["h"], i["alt"], sizes="(max-width: 800px) 100vw, 740px")}<figcaption>{esc(i["caption"])}</figcaption></figure>'
        for i in p.get("extra_images", []))
    more = []
    if p.get("extra_prose"):
        more.append(p["extra_prose"])
    if p.get("routing"):
        more.append(f"<h3>Routing</h3><p>{p['routing']}</p>")
    if p.get("pairs"):
        more.append(f"<p>{p['pairs']}</p>")
    details = []
    if p.get("tested"):
        details.append(f"<h3>Was getestet wurde</h3><p>{p['tested']}</p>")
    if p.get("good_to_know"):
        details.append(f"<h3>Gut zu wissen</h3><p>{p['good_to_know']}</p>")
    details.append((f"<h3>Formate und Systeme</h3>" if details else "") + f"<p>{p['formats']}</p>")
    det_title = "Tests, Formate und Systeme" if p.get("tested") else "Formate und Systeme"
    demo_hint = ("" if p["price"] == 0 else
                 f'<p>Nicht sicher? Die <a href="{utm(slug + "-demo", slug)}">kostenlose Demo</a> ist das vollständige Plugin mit einem kurzen Rauschen alle 45 Sekunden.</p>')
    rel = [BY_SLUG[s] for s in p["related"] if s in BY_SLUG]
    rel += [o for o in LIVE if o is not p and o not in rel and o["group"] == p["group"]]
    rel_cards = "".join(plugin_card(o, slug) for o in rel)
    sticky = "Kostenlos herunterladen" if p["price"] == 0 else f"{name} kaufen · {euro(p['price'])}"
    body = f"""<main id="main">
<div class="wrap crumbs"><nav aria-label="Breadcrumb"><ol><li><a href="/">Startseite</a></li><li><a href="/plugins/">Plugins</a></li><li aria-current="page">{esc(name)}</li></ol></nav></div>
<section class="s-hero">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">{esc(p['eyebrow'])}</span>
      <h1>{esc(p['h1'])}</h1>
      <div class="rule" aria-hidden="true"><i></i></div>
      <p class="answer">{p['answer']}</p>
      <p class="price-line"><span class="price-tag">{euro(p['price'])}</span> {esc(fmt_line)}</p>
      <div class="btns">{cta_buttons(p, slug)}</div>
      {'<p class="note"><a href="#hoeren">▶ Hörprobe anhören</a></p>' if p.get('audio') else ''}
    </div>
    <figure class="shot">{picture(slug, "gui", p["gui_w"], p["gui_h"], p["gui_alt"], lazy=False)}<figcaption>Die echte Oberfläche von {esc(name)}.</figcaption></figure>
  </div>
</section>
{audio_html(p)}<section aria-labelledby="specs-t">
  <div class="wrap narrow">
    <h2 id="specs-t">{esc(name)} auf einen Blick</h2>
    <div class="table-scroll"><table class="specs"><tbody>{specs}</tbody></table></div>
  </div>
</section>
<section class="alt" aria-labelledby="feat-t">
  <div class="wrap narrow prose">
    <h2 id="feat-t">Funktionen</h2>
    <ul>{feats}</ul>
    {extra_imgs}
    {"".join(more)}
  </div>
</section>
<section aria-labelledby="det-t">
  <div class="wrap narrow prose">
    <h2 id="det-t">{det_title}</h2>
    {"".join(details)}
  </div>
</section>
<section class="alt" aria-labelledby="faq-t">
  <div class="wrap narrow">
    <h2 id="faq-t">Häufige Fragen zu {esc(name)}</h2>
    {faq_html(p['faq'])}
  </div>
</section>
<section aria-labelledby="cta-t">
  <div class="wrap narrow prose">
    <h2 id="cta-t">{esc(name)} holen</h2>
    <p>{esc(name)} gibt es auf Gumroad, {"kostenlos (Pay what you want)" if p['price'] == 0 else f"für {euro(p['price'])}"}, als Sofort-Download.</p>
    {demo_hint}
    <div class="btns">{cta_buttons(p, slug)}</div>
  </div>
</section>
<section class="alt" aria-labelledby="more-t">
  <div class="wrap">
    <h2 id="more-t">Weitere Plugins von Code Chaos Audio</h2>
    <div class="pcards">{rel_cards}</div>
    <p class="prose" style="margin-top:22px"><a href="/plugins/">Alle Plugins im Überblick →</a></p>
  </div>
</section>
</main>
<a class="sticky-cta" href="{utm(slug, slug)}">{esc(sticky)}</a>
"""
    html = head("de", url, None, p["title"], p["desc"], og, f"{name} von Code Chaos Audio: {p['category']}", ld, og_type="product") \
        + nav("de", None, "plug") + body + footer("de")
    path = os.path.join(ROOT, "plugins", slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html)
    return path


PLUGINS_INDEX = dict(
    title="Plugins: VST3 für Psytrance & Black Metal | Code Chaos",
    desc="Audio-Plugins von Code Chaos Audio: Crucible, Shardstep, Chaos FM, Gravesaw, Rimehall und das kostenlose Kick/Bass Scope. VST3, Gratis-Demos.",
    h1="Audio-Plugins von Code Chaos Audio",
    answer="Code Chaos Audio ist die Plugin-Reihe von Code Chaos (Tim Borchert, Hamburg): VST3-Plugins für Hitech, Psycore und Darkpsy und die Code Chaos Black Metal Suite. "
           "Alle Plugins gibt es auf Gumroad als Sofort-Download, zu jedem Bezahl-Plugin eine kostenlose Demo (vollständiges Plugin mit einem kurzen Rauschen alle 45 Sekunden).",
)


def build_plugins_index():
    url = BASE + "/plugins/"
    order = {g: [p for p in [CRUCIBLE] + LIVE if p["group"] == g] for g, _, _ in GROUPS}
    allp = [p for g, _, _ in GROUPS for p in order[g]]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": PLUGINS_INDEX["title"], "description": PLUGINS_INDEX["desc"],
         "inLanguage": "de", "isPartOf": {"@id": BASE + "/#website"}, "datePublished": PLUGIN_DATE, "dateModified": PLUGIN_DATE,
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": p["name"], "url": BASE + plugin_url(p)} for i, p in enumerate(allp)]}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Startseite", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Plugins", "item": url}]},
    ]}
    groups = ""
    for i, (g, h, intro) in enumerate(GROUPS):
        cards = "".join(plugin_card(p, "plugins") for p in order[g])
        groups += f"""<section{' class="alt"' if i % 2 == 0 else ''} aria-labelledby="g-{g}">
  <div class="wrap">
    <h2 id="g-{g}">{esc(h)}</h2>
    <p class="prose">{esc(intro)}</p>
    <div class="pcards">{cards}</div>
  </div>
</section>
"""
    def mac(p):
        return "nein" if p["slug"] in ("crucible", "chaos-fm") else "Apple Silicon (unsigniert)"
    rows = "".join(f'<tr><th scope="row"><a href="{plugin_url(p)}">{esc(p["name"])}</a></th><td>{esc(p.get("category", "3-Band-Sättigung"))}</td>'
                   f'<td>{euro(p["price"])}</td><td>ja</td><td>{mac(p)}</td></tr>' for p in allp)
    body = f"""<main id="main">
<div class="wrap crumbs"><nav aria-label="Breadcrumb"><ol><li><a href="/">Startseite</a></li><li aria-current="page">Plugins</li></ol></nav></div>
<section class="s-hero">
  <div class="wrap narrow">
    <span class="eyebrow">Code Chaos Audio</span>
    <h1>{PLUGINS_INDEX['h1']}</h1>
    <div class="rule" aria-hidden="true"><i></i></div>
    <p class="answer">{PLUGINS_INDEX['answer']}</p>
  </div>
</section>
{groups}<section aria-labelledby="cmp-t">
  <div class="wrap narrow">
    <h2 id="cmp-t">Formate und Systeme im Vergleich</h2>
    <div class="table-scroll"><table class="cmp"><thead><tr><th>Plugin</th><th>Typ</th><th>Preis</th><th>Windows 10/11</th><th>macOS</th></tr></thead><tbody>{rows}</tbody></table></div>
    <p class="note" style="margin-top:14px">Alle Plugins als VST3 + Standalone. Kein AU-Format, deshalb laufen sie nicht in Logic Pro. Die macOS-Builds sind nur für Apple Silicon (arm64), nicht signiert und nicht notarisiert: macOS blockiert sie beim ersten Start, du erlaubst sie unter Systemeinstellungen → Datenschutz &amp; Sicherheit.</p>
    <p class="prose" style="margin-top:14px">Du suchst keine Plugins, sondern Sounds? <a href="/sounds/">Samples, MIDI und Presets für Psytrance und Black Metal →</a></p>
  </div>
</section>
</main>
"""
    html = head("de", url, None, PLUGINS_INDEX["title"], PLUGINS_INDEX["desc"], BASE + "/images/plugins/shardstep/og.jpg",
                "Audio-Plugins von Code Chaos Audio", ld, og_type="website") + nav("de", None, "plug") + body + footer("de")
    path = os.path.join(ROOT, "plugins", "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html)
    return path


def genre_plugins_html(g, lang):
    """DE-Genre-Seiten: Block mit passenden Plugins (nur live gebaute)."""
    if lang != "de":
        return ""
    ps = [BY_SLUG[s] for s in GENRE_PLUGINS.get(g["slug"], []) if s in BY_SLUG]
    if not ps:
        return ""
    cards = "".join(f'<div class="card"><div class="bpm">{euro(p["price"])}</div><h3>{esc(p["name"])}</h3><p>{p["teaser"]}</p>'
                    f'<a class="more" href="{plugin_url(p)}">Zum Plugin →</a></div>' for p in ps)
    return f"""<section class="alt" aria-labelledby="plug-t">
  <div class="wrap">
    <h2 id="plug-t">Plugins für {esc(g['de']['nav'])}-Producer</h2>
    <p class="prose">Von Code Chaos Audio, gebaut für schnelle, dichte Psytrance-Produktionen. Zu jedem Bezahl-Plugin gibt es eine kostenlose Demo. <a href="/plugins/">Alle Plugins →</a></p>
    <div class="cards">{cards}</div>
  </div>
</section>
"""

if __name__ == "__main__":
    for g in GENRES:
        for lang in ("de", "en"):
            print(build_genre(g, lang))
    print(build_en_home())
    print(build_mastering("de"))
    print(build_mastering("en"))
    print(build_404())
    print(build_plugins_index())
    for p in LIVE:
        print(build_plugin(p))
