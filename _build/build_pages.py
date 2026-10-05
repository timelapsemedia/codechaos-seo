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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://codechaos-official.de"
TODAY = "2026-10-05"
ARTIST = BASE + "/#artist"
PERSON = BASE + "/#tim-borchert"

UI = {
    "de": dict(home="Startseite", genres="Genres", releases="Releases", mastering="Mastering", lang_label="EN",
               skip="Zum Inhalt springen", menu="Menü öffnen", faq="Häufige Fragen", rel_title="Releases von Code Chaos",
               more="Weiterlesen", legal="Rechtliches", imprint="Impressum", privacy="Datenschutz", nav="Navigation",
               follow="Code Chaos folgen", other="Weitere Genre-Guides", foot="Hitech, Psycore & Darkpsy Producer aus Hamburg. Reines Studioprojekt.",
               home_url="/", mastering_url="/mastering/", releases_url="/#releases",
               author="Von Code Chaos (Tim Borchert), Producer aus Hamburg · aktualisiert am 05.10.2026"),
    "en": dict(home="Home", genres="Genres", releases="Releases", mastering="Mastering", lang_label="DE",
               skip="Skip to content", menu="Open menu", faq="FAQ", rel_title="Releases by Code Chaos",
               more="Read more", legal="Legal", imprint="Imprint (German)", privacy="Privacy policy (German)", nav="Navigation",
               follow="Follow Code Chaos", other="More genre guides", foot="Hitech, Psycore & Darkpsy producer from Hamburg, Germany. Studio project only.",
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
    items += [(u["releases"], u["releases_url"], "rel"), (u["mastering"], u["mastering_url"], "mast"), ("Crucible", "/crucible.html", "cru")]
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
      <div><h2>{u['genres']}</h2><ul>{genre_links}<li><a href="/crucible.html">Crucible Plugin</a></li></ul></div>
      <div><h2>{u['follow']}</h2><ul>{social}</ul></div>
      <div><h2>{u['legal']}</h2><ul><li><a href="/#impressum">{u['imprint']}</a></li><li><a href="/#datenschutz">{u['privacy']}</a></li><li><a href="{'/en/' if lang == 'de' else '/'}" hreflang="{'en' if lang == 'de' else 'de'}">{'English version' if lang == 'de' else 'Deutsche Version'}</a></li></ul></div>
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
         "url": url, "mainEntityOfPage": url, "datePublished": TODAY, "dateModified": TODAY,
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
<section aria-labelledby="other-t">
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


if __name__ == "__main__":
    for g in GENRES:
        for lang in ("de", "en"):
            print(build_genre(g, lang))
    print(build_en_home())
    print(build_mastering("de"))
    print(build_mastering("en"))
    print(build_404())
