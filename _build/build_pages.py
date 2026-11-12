#!/usr/bin/env python3
"""Erzeugt die Genre-Unterseiten (DE + EN) und die englische Startseite.

Aufruf aus dem Repo-Root:  python3 _build/build_pages.py
Inhalte stehen in _build/content_genres.py und _build/content_en_home.py.
Der Ordner _build wird von GitHub Pages nicht veröffentlicht.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_genres import GENRES, RELEASES          # noqa: E402
from content_en_home import EN_HOME                   # noqa: E402
from content_en_mastering import EN_MASTERING, FORM   # noqa: E402
from content_de_mastering import DE_MASTERING, FORM_DE  # noqa: E402
from flags import UK as FLAG_UK, DE as FLAG_DE       # noqa: E402
from content_plugins import PLUGINS, GROUPS, GENRE_PLUGINS, GUMROAD  # noqa: E402
import geo                                            # noqa: E402
from geo import DATUM, autor_ld, publisher_ld        # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://codechaos-official.de"
TODAY = "2026-10-05"            # datePublished Genre-, EN- und Mastering-Seiten
PLUGIN_DATE = "2026-10-21"      # datePublished Plugin-Seiten
# dateModified und „Zuletzt aktualisiert“ kommen aus _build/seiten_datum.json (geo.py, nur echte Inhaltsänderungen)
ARTIST = BASE + "/#artist"
PERSON = BASE + "/#tim-borchert"

UI = {
    "de": dict(home="Startseite", genres="Genres", releases="Releases", mastering="Mastering", lang_label="EN",
               skip="Zum Inhalt springen", menu="Menü öffnen", faq="Häufige Fragen", rel_title="Releases von Code Chaos",
               more="Weiterlesen", legal="Rechtliches", imprint="Impressum", privacy="Datenschutz", nav="Navigation",
               follow="Code Chaos folgen", other="Weitere Genre-Guides", foot="Hitech, Psycore & Darkpsy Producer aus Hamburg. Heute ein reines Studioprojekt.",
               home_url="/", mastering_url="/mastering/", releases_url="/releases/"),
    "en": dict(home="Home", genres="Genres", releases="Releases", mastering="Mastering", lang_label="DE",
               skip="Skip to content", menu="Open menu", faq="FAQ", rel_title="Releases by Code Chaos",
               more="Read more", legal="Legal", imprint="Imprint (German)", privacy="Privacy policy (German)", nav="Navigation",
               follow="Follow Code Chaos", other="More genre guides", foot="Hitech, Psycore & Darkpsy producer from Hamburg, Germany. Studio project.",
               home_url="/en/", mastering_url="/en/mastering/", releases_url="/en/#releases"),
}

# sameAs der Künstler-Entität (wie schema_home.py)
SAME_AS = ["https://codechaos.bandcamp.com", "https://soundcloud.com/codechaos", "https://www.instagram.com/codechaos_official",
           "https://www.tiktok.com/@codechaos_abstractsound", "https://x.com/codechaos_music", "https://www.threads.net/@codechaos_official",
           "https://www.youtube.com/@codechaos_abstractsounddesign", "https://www.discogs.com/artist/18204093-Code-Chaos",
           "https://musicbrainz.org/artist/14d40d24-a91e-4600-a1b3-d14682d32e42", "https://www.wikidata.org/wiki/Q141646843",
           "https://de.wikipedia.org/wiki/Code_Chaos"]

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
<link rel="stylesheet" href="/css/geo.css">
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
              ("Plugins", "/plugins/" if lang == "de" else "/en/plugins/", "plug")]
    cur = ' aria-current="page"'
    lis = "".join(
        f'<li><a href="{h}"{cur if k == current else ""}>{esc(t)}</a></li>' for t, h, k in items)
    alt_href = (alt_url or BASE + ("/en/" if lang == "de" else "/")).replace(BASE, "")
    other = "en" if lang == "de" else "de"
    switch = (f'<a class="lang-switch" href="{alt_href}" hreflang="{other}" lang="{other}" aria-label="{"EN – English version" if lang == "de" else "DE – Deutsche Version"}">'
              f'{FLAG_UK if lang == "de" else FLAG_DE}<span>{other.upper()}</span></a>')
    return f"""<body>
<a class="skip" href="#main">{u['skip']}</a>
<header>
<nav class="s-nav" aria-label="{u['nav']}">
  <a class="logo" href="{u['home_url']}"><img src="/images/brand/codechaos-logo-bone-136.webp" srcset="/images/brand/codechaos-logo-bone-68.webp 1x, /images/brand/codechaos-logo-bone-136.webp 2x, /images/brand/codechaos-logo-bone-204.webp 3x" width="68" height="40" alt="Code Chaos Logo"></a>
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
      <div><h2>{u['genres']}</h2><ul>{genre_links}<li><a href="{'/plugins/crucible/' if lang == 'de' else '/en/plugins/crucible/'}">Crucible Plugin</a></li>{'<li><a href="/plugins/">Alle Plugins</a></li>' if lang == "de" else ""}</ul></div>
      <div><h2>{u['follow']}</h2><ul>{social}</ul></div>
      <div><h2>{u['legal']}</h2><ul><li><a href="/impressum/">{u['imprint']}</a></li><li><a href="/datenschutz/">{u['privacy']}</a></li><li><a href="#cookies" class="cookie-settings-link">{'Cookie-Einstellungen' if lang == 'de' else 'Cookie settings'}</a></li><li><a href="{'/en/' if lang == 'de' else '/'}" hreflang="{'en' if lang == 'de' else 'de'}">{'English version' if lang == 'de' else 'Deutsche Version'}</a></li></ul></div>
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
        href = r.get("url_" + lang, r["url"])
        ext = ' target="_blank" rel="noopener noreferrer"' if href.startswith("http") else ""
        out.append(f'<a href="{href}"{ext}>'
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
         "url": url, "mainEntityOfPage": url, "datePublished": TODAY, "dateModified": DATUM,
         "author": autor_ld(), "publisher": publisher_ld(), "image": BASE + g["og"],
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
    <div class="btns"><a class="btn btn-blood" href="{u['mastering_url']}">{c['cta_btn1']}</a><a class="btn btn-ghost" href="{pre}/plugins/crucible/">Crucible Plugin</a></div>
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
    html, _ = geo.ausbauen(html, f"{pre}/{g['slug']}/", lang)
    path = os.path.join(ROOT, pre.strip("/"), g["slug"], "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8", newline="\n").write(html)
    return path


def build_en_home():
    h = EN_HOME
    url, alt = BASE + "/en/", BASE + "/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": h["title"], "description": h["desc"], "inLanguage": "en",
         "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": ARTIST}, "mainEntity": {"@id": ARTIST},
         "primaryImageOfPage": {"@type": "ImageObject", "url": BASE + "/images/uhrwerk-aus-blut/og-uhrwerk-aus-blut.jpg"},
         "datePublished": TODAY, "dateModified": DATUM, "author": autor_ld()},
        {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": "en", "mainEntity": [
            {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in h["faq"]]},
        {"@type": "MusicGroup", "@id": ARTIST, "name": "Code Chaos", "alternateName": ["Code-Chaos", "CodeChaos"],
         "description": "Code Chaos is a hitech psytrance, psycore and darkpsy producer from Hamburg, Germany, and the studio project of Tim Borchert. "
                        "Self-described style: New Psychedelic Death Art. Active since 2016 with 24+ releases on labels including Abstract Sound Design "
                        "(co-founded in 2021), TATEWARI Records (Mexico) and Soma Ritual Records (India). Today a studio-only project without bookings.",
         "genre": ["Hitech Psytrance", "Psycore", "Darkpsy", "Dark Psytrance", "Psytrance"], "foundingDate": "2016",
         "foundingLocation": {"@type": "Place", "name": "Hamburg", "address": {"@type": "PostalAddress", "addressLocality": "Hamburg", "addressCountry": "DE"}},
         "slogan": "New Psychedelic Death Art", "url": BASE + "/", "logo": BASE + "/images/brand/codechaos-logo-bone-480.webp",
         "image": BASE + "/images/brand/portrait-press-1200.jpg", "sameAs": SAME_AS, "member": {"@id": PERSON}},
        {"@type": "Service", "@id": url + "#mastering", "name": "Code Chaos Mastering: mastering for psycore, hitech psytrance and darkpsy",
         "serviceType": "Audio Mastering", "brand": {"@type": "Brand", "name": "Code Chaos Mastering"},
         "description": "Genre-specific audio mastering for psycore, hitech psytrance and darkpsy by an active producer. Single (stereo) €79, Stem Pro €129, "
                        "EP up to 5 tracks €349, album up to 10 tracks €629, incl. 19% German VAT, audio audit and unlimited revisions.",
         "provider": {"@id": PERSON}, "areaServed": "Worldwide", "availableLanguage": ["de", "en"], "url": BASE + "/en/mastering/",
         "offers": [{"@type": "Offer", "name": n, "price": pr, "priceCurrency": "EUR", "url": BASE + "/en/mastering/#request",
                     "priceSpecification": {"@type": "PriceSpecification", "price": pr, "priceCurrency": "EUR", "valueAddedTaxIncluded": True}}
                    for n, pr in [("Single: stereo mastering (1 track)", "79"), ("Stem Pro: stem mastering (1 track, up to 6 stems)", "129"),
                                  ("EP mastering (up to 5 tracks)", "349"), ("Album mastering (up to 10 tracks)", "629"),
                                  ("Cover art", "99"), ("Lyric video", "179"), ("Promo video (60 s)", "299")]]},
        {"@type": "ItemList", "@id": url + "#plugins", "name": "Plugins by Code Chaos Audio", "numberOfItems": len(LIVE),
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {
             "@type": "SoftwareApplication", "name": p["name"], "url": BASE + (f"/en/plugins/{p['slug']}/" if p.get("en") else plugin_url(p)),
             "applicationCategory": "MultimediaApplication", "operatingSystem": p["os"], "brand": {"@type": "Brand", "name": "Code Chaos Audio"},
             "offers": {"@type": "Offer", "price": f"{p['price']:.2f}", "priceCurrency": "EUR", "url": GUMROAD + p["slug"],
                        "availability": "https://schema.org/InStock"}}} for i, p in enumerate(LIVE)]},
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
    html, _ = geo.ausbauen(html, "/en/", "en", toc_offen=False)
    path = os.path.join(ROOT, "en", "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8", newline="\n").write(html)
    return path


def build_mastering(lang):
    m, form = (DE_MASTERING, FORM_DE) if lang == "de" else (EN_MASTERING, FORM)
    pre = "" if lang == "de" else "/en"
    url = f"{BASE}{pre}/mastering/"
    alt = f"{BASE}{'/en' if lang == 'de' else ''}/mastering/"
    if lang == "de":
        offers = [("Single: Stereo Mastering (1 Track)", "79"), ("Stem Pro: Stem Mastering (1 Track, bis 6 Stems)", "129"), ("EP Mastering (bis 5 Tracks)", "349"),
                  ("Album Mastering (bis 10 Tracks)", "629"), ("Cover Art", "99"), ("Lyric Video", "179"), ("Promo Video (60 Sekunden)", "299")]
        sname, home = "Code Chaos Mastering: Psytrance Mastering für Psycore, Hitech und Darkpsy", "Startseite"
    else:
        offers = [("Single: stereo mastering (1 track)", "79"), ("Stem Pro: stem mastering (1 track, up to 6 stems)", "129"), ("EP mastering (up to 5 tracks)", "349"),
                  ("Album mastering (up to 10 tracks)", "629"), ("Cover art", "99"), ("Lyric video", "179"), ("Promo video (60 s)", "299")]
        sname, home = "Code Chaos Mastering: psytrance mastering for psycore, hitech and darkpsy", "Home"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": m["title"], "description": m["desc"], "inLanguage": lang,
         "isPartOf": {"@id": BASE + "/#website"}, "mainEntity": {"@id": url + "#service"}, "datePublished": TODAY, "dateModified": DATUM,
         "author": autor_ld()},
        {"@type": "Article", "@id": url + "#article", "headline": strip(re.search(r"<h1>(.*?)</h1>", m["body"], re.S).group(1)),
         "description": m["desc"], "inLanguage": lang, "url": url, "mainEntityOfPage": url, "datePublished": TODAY, "dateModified": DATUM,
         "author": autor_ld(), "publisher": publisher_ld(), "image": BASE + "/images/og/mastering.jpg", "about": {"@id": url + "#service"},
         "isPartOf": {"@id": BASE + "/#website"}},
        {"@type": "Service", "@id": url + "#service", "name": sname, "serviceType": "Audio Mastering",
         "description": m["desc"], "brand": {"@type": "Brand", "name": "Code Chaos Mastering"}, "provider": {"@id": PERSON}, "areaServed": "Worldwide", "availableLanguage": ["de", "en"], "url": url,
         "offers": [{"@type": "Offer", "name": n, "price": p, "priceCurrency": "EUR", "url": url + "#request", "priceSpecification": {"@type": "PriceSpecification", "price": p, "priceCurrency": "EUR", "valueAddedTaxIncluded": True}} for n, p in offers]},
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
    html, _ = geo.ausbauen(html, f"{pre}/mastering/", lang, art="mastering")
    path = os.path.join(ROOT, pre.strip("/"), "mastering", "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8", newline="\n").write(html)
    return path

RELEASE_DATE = "2026-11-10"     # datePublished der Release-Seiten


def release_ld(slug, lang, url):
    """Schema der Release-Seiten. @ids der Uhrwerk-Knoten = dieselben wie im Startseiten-Graph (schema_home.py)."""
    asd = {"@type": "Organization", "@id": BASE + "/#label-asd", "name": "Abstract Sound Design", "url": "https://www.abstract-sound-design.de/"}
    artist = {"@type": "MusicGroup", "@id": ARTIST, "name": "Code Chaos", "url": BASE + "/"}
    if slug == "uhrwerk-aus-blut":
        desc = ("Ein Herz, das zu schnell schlägt. Ein Uhrwerk, das blutet. Single von Code Chaos in fünf Szenen (Prolog, Die Uhr, Der Spiegel, Das Blut, Rückkehr), erschienen am 30.10.2026 auf Abstract Sound Design. Bild mit KI erstellt."
                if lang == "de" else
                "A heart that beats too fast. A clockwork that bleeds. Single by Code Chaos in five scenes (Prologue, The Clock, The Mirror, The Blood, Return), released 30 October 2026 on Abstract Sound Design. Artwork created with AI.")
        rec = {"@type": "MusicRecording", "@id": BASE + "/#uhrwerk-aus-blut", "name": "Uhrwerk aus Blut", "byArtist": artist,
               "datePublished": "2026-10-30", "genre": ["Darkpsy", "Hitech Psytrance", "Gothic"], "inLanguage": "de",
               "image": BASE + "/images/uhrwerk-aus-blut/cover-1600.jpg", "url": url, "description": desc,
               "recordingOf": {"@type": "MusicComposition", "name": "Uhrwerk aus Blut", "composer": {"@id": PERSON}},
               "inAlbum": {"@id": BASE + "/#uhrwerk-aus-blut-single"},
               "potentialAction": {"@type": "ListenAction", "name": "Jetzt streamen" if lang == "de" else "Listen now",
                                   "target": "https://distrokid.com/hyperfollow/codechaos/uhrwerk-aus-blut-2"}}
        alb = {"@type": "MusicAlbum", "@id": BASE + "/#uhrwerk-aus-blut-single", "name": "Uhrwerk aus Blut",
               "albumReleaseType": "https://schema.org/SingleRelease", "albumProductionType": "https://schema.org/StudioAlbum",
               "datePublished": "2026-10-30", "byArtist": artist, "recordLabel": asd, "url": url,
               "image": BASE + "/images/uhrwerk-aus-blut/cover-1600.jpg", "numTracks": 1, "track": {"@id": BASE + "/#uhrwerk-aus-blut"}}
        return [rec, alb], BASE + "/#uhrwerk-aus-blut"
    from content_releases import WG_TRACKS
    alb = {"@type": "MusicAlbum", "@id": BASE + "/wiedergaenger-vol-1/#album", "name": "Wiedergänger Vol. I · Was nicht ruhen will",
           "alternateName": "Wiedergänger Vol. I", "albumProductionType": "https://schema.org/RemixAlbum",
           "datePublished": "2026-12-04", "byArtist": artist, "url": url, "numTracks": len(WG_TRACKS),
           "description": ("Remix-Release von Code Chaos mit fünf Tracks, erscheint am 04.12.2026." if lang == "de"
                           else "Remix release by Code Chaos with five tracks, out 4 December 2026."),
           "track": {"@type": "ItemList", "numberOfItems": len(WG_TRACKS), "itemListElement": [
               {"@type": "ListItem", "position": i + 1, "item": {"@type": "MusicRecording", "name": t, "byArtist": {"@id": ARTIST}}}
               for i, t in enumerate(WG_TRACKS)]}}
    return [alb], alb["@id"]


def build_release(slug, lang):
    from content_releases import RELEASE_PAGES
    r = RELEASE_PAGES[slug]
    c = r[lang]
    u = UI[lang]
    pre = "" if lang == "de" else "/en"
    url = f"{BASE}{pre}/{slug}/"
    alt = f"{BASE}{'/en' if lang == 'de' else ''}/{slug}/"
    nodes, main_id = release_ld(slug, lang, url)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": c["title"], "description": c["desc"], "inLanguage": lang,
         "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": main_id}, "mainEntity": {"@id": main_id},
         "primaryImageOfPage": {"@type": "ImageObject", "url": BASE + r["og"], "width": 1200, "height": 630},
         "datePublished": RELEASE_DATE, "dateModified": DATUM, "author": autor_ld(), "publisher": publisher_ld()},
        *nodes,
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": u["home"], "item": BASE + u["home_url"]},
            {"@type": "ListItem", "position": 2, "name": u["releases"], "item": BASE + u["releases_url"]},
            {"@type": "ListItem", "position": 3, "name": c["nav"], "item": url}]},
        {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": lang, "mainEntity": [
            {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in c["faq"]]},
    ]}
    body = c["body"].replace("{faq}", faq_html(c["faq"]))
    og_type = "music.song" if slug == "uhrwerk-aus-blut" else "music.album"
    html = head(lang, url, alt, c["title"], c["desc"], BASE + r["og"], c["og_alt"], ld, og_type=og_type) \
        + nav(lang, alt, "rel") + body + footer(lang)
    html, _ = geo.ausbauen(html, f"{pre}/{slug}/", lang)
    path = os.path.join(ROOT, pre.strip("/"), slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8", newline="\n").write(html)
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
      <div class="card"><h3>Uhrwerk aus Blut</h3><p>Die Single, erschienen am 30.10.2026.</p><a class="more" href="/uhrwerk-aus-blut/">Zur Single →</a></div>
      <div class="card"><h3>Mastering</h3><p>Psycore, Hitech &amp; Darkpsy: Single 79 €, EP 349 €, Album 629 €.</p><a class="more" href="/mastering/">Preise &amp; Ablauf →</a></div>
      <div class="card"><h3>Genre Guides</h3><p><a href="/psycore/">Psycore</a> · <a href="/hitech-psytrance/">Hitech</a> · <a href="/darkpsy/">Darkpsy</a></p></div>
      <div class="card"><h3>Crucible</h3><p>3-Band Harmonic Saturation Plugin von Code Chaos Audio.</p><a class="more" href="/plugins/crucible/">Zum Plugin →</a></div>
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
    open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8", newline="\n").write(html)
    return os.path.join(ROOT, "404.html")



# ───────────────────────── Plugin-Seiten (/plugins/, /plugins/<slug>/) ─────────────────────────
# Inhalte: _build/content_plugins.py · Bilder/Audio: python3 _build/plugin_assets.py
# Nur Einträge mit live=True werden gebaut (Gumroad-Seite muss erreichbar sein).

LIVE = [p for p in PLUGINS if p["live"]]
BY_SLUG = {p["slug"]: p for p in LIVE}


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
    # plugin_assets.py legt die 1600er nur an, wenn die Quelle so breit ist (Frostfret/Hoarfell: nein) -> nie ins Leere verlinken
    has_1600 = has_1600 and os.path.exists(os.path.join(ROOT, "images", "plugins", slug, f"{name}-1600.webp"))
    srcset = f"{base}-880.webp 880w" + (f", {base}-1600.webp 1600w" if has_1600 else "")
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    return (f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
            f'<img src="{base}-880.jpg" width="880" height="{round(h * 880 / w)}" {load} alt="{esc(alt)}"></picture>')


PL = {
    "de": dict(free_dl="Kostenlos herunterladen", buy="Kaufen", demo="Kostenlose Demo", home="Startseite", home_url="/",
               play="▶ Abspielen", pause="❚❚ Pause", listen_t="{name} anhören", listen_id="hoeren", listen_link="▶ Hörprobe anhören",
               real_gui="Die echte Oberfläche von {name}.", glance="{name} auf einen Blick", features="Funktionen",
               tested="Was getestet wurde", good="Gut zu wissen", formats="Formate und Systeme", det_tested="Tests, Formate und Systeme",
               faq="Häufige Fragen zu {name}", get="{name} holen", sticky_buy="{name} kaufen · {price}", by="von Code Chaos Audio"),
    "en": dict(free_dl="Free download", buy="Buy", demo="Free demo", home="Home", home_url="/en/",
               play="▶ Play", pause="❚❚ Pause", listen_t="Listen to {name}", listen_id="listen", listen_link="▶ Listen to the A/B demo",
               real_gui="The real {name} interface.", glance="{name} at a glance", features="Features",
               tested="What was tested", good="Good to know", formats="Formats and systems", det_tested="Tests, formats and systems",
               faq="{name} FAQ", get="Get {name}", sticky_buy="Get {name} · {price}", by="by Code Chaos Audio"),
}


def price_l(price, lang):
    if lang == "de":
        return euro(price)
    return "free" if price == 0 else f"€{price}"


def cta_buttons(p, campaign, big=True, lang="de"):
    """Kauf- und Demo-Buttons. Gratis-Plugin: nur ein Download-Button."""
    L = PL[lang]
    if p["price"] == 0:
        return f'<a class="btn btn-blood" href="{utm(p["slug"], campaign)}">{L["free_dl"]}</a>'
    return (f'<a class="btn btn-blood" href="{utm(p["slug"], campaign)}">{L["buy"]} · {price_l(p["price"], lang)}</a>'
            f'<a class="btn btn-ghost" href="{utm(p["slug"] + "-demo", campaign)}">{L["demo"]}</a>')


def plugin_card(p, campaign):
    """Karte für Übersicht und Querverweise (DE): Bild, 1 Satz, Preis, Links."""
    img = picture(p["slug"], "gui", p["gui_w"], p["gui_h"], p["gui_alt"], sizes="(max-width: 700px) 100vw, 340px")
    os_line = p["os"]
    links = (f'<a href="{utm(p["slug"], campaign)}">Kostenlos laden</a>' if p["price"] == 0 else
             f'<a href="{utm(p["slug"] + "-demo", campaign)}">Kostenlose Demo</a><a href="{utm(p["slug"], campaign)}">Kaufen</a>')
    return (f'<article class="pcard"><a class="pcard-img" href="{plugin_url(p)}" tabindex="-1" aria-hidden="true">{img}</a>'
            f'<div class="pcard-body"><h3><a href="{plugin_url(p)}">{esc(p["name"])}</a></h3><p>{p["teaser"]}</p>'
            f'<p class="pcard-meta"><span class="price-tag">{euro(p["price"])}</span> {esc(os_line)}</p>'
            f'<p class="pcard-links"><a href="{plugin_url(p)}">Details &amp; Hörprobe</a>{links}</p></div></article>')


def audio_html(p, lang="de", t=None):
    """t = sprachspezifische Texte (bei EN aus p['en']); Dateien immer aus p."""
    t = t or p
    L = PL[lang]
    if not p.get("audio"):
        return ""
    base = f"/audio/plugins/{p['slug']}/"
    labels = t["audio"] if lang != "de" else [a["label"] for a in p["audio"]]
    if p["audio_mode"] == "ab":
        a, b = p["audio"]
        player = f"""<div class="ab">
      <audio id="ab-a" src="{base}{a['file']}" preload="metadata" loop></audio>
      <audio id="ab-b" src="{base}{b['file']}" preload="metadata" loop></audio>
      <div class="ab-row">
        <button type="button" class="ab-play" id="ab-play">{L['play']}</button>
        <button type="button" id="ab-dry" aria-pressed="true">{esc(labels[0])}</button>
        <button type="button" id="ab-wet" aria-pressed="false">{esc(labels[1])}</button>
      </div>
    </div>
<script>
(function(){{var a=document.getElementById('ab-a'),b=document.getElementById('ab-b'),p=document.getElementById('ab-play'),d=document.getElementById('ab-dry'),w=document.getElementById('ab-wet');if(!a||!b)return;
var wet=false,playing=false;function mix(){{a.muted=wet;b.muted=!wet;d.setAttribute('aria-pressed',wet?'false':'true');w.setAttribute('aria-pressed',wet?'true':'false');}}
p.addEventListener('click',function(){{if(playing){{a.pause();b.pause();playing=false;p.textContent='{L['play']}';return;}}
b.currentTime=a.currentTime;mix();Promise.all([a.play(),b.play()]).then(function(){{playing=true;p.textContent='{L['pause']}';}}).catch(function(){{}});}});
d.addEventListener('click',function(){{wet=false;mix();}});w.addEventListener('click',function(){{wet=true;if(playing&&Math.abs(a.currentTime-b.currentTime)>0.05)b.currentTime=a.currentTime;mix();}});mix();}})();
</script>"""
    else:
        parts = []
        for a, lab in zip(p["audio"], labels):
            ch = ""
            if a.get("chapters"):
                ch = '<ol class="chapters">' + "".join(f"<li><span>{tt}</span> {esc(l)}</li>" for tt, l in a["chapters"]) + "</ol>"
            parts.append(f'<figure class="track"><figcaption>{esc(lab)}</figcaption>'
                         f'<audio controls preload="metadata" src="{base}{a["file"]}"></audio>{ch}</figure>')
        player = "".join(parts)
    note = f'<p class="note">{esc(t["audio_note"])}</p>' if t.get("audio_note") else ""
    return f"""<section class="alt" id="{L['listen_id']}" aria-labelledby="hoeren-t">
  <div class="wrap narrow">
    <h2 id="hoeren-t">{esc(L['listen_t'].format(name=p['name']))}</h2>
    <p class="prose">{esc(t['audio_intro'])}</p>
    {player}
    {note}
  </div>
</section>
"""


def build_plugin(p, lang="de"):
    """Plugin-Landingpage. lang="en" nur für Plugins mit p["en"] (Texte dort, Fakten/Dateien aus p)."""
    L = PL[lang]
    t = p if lang == "de" else {**p, **p["en"]}
    slug, name = p["slug"], p["name"]
    pre = "" if lang == "de" else "/en"
    url = f"{BASE}{pre}/plugins/{slug}/"
    alt_url = (f"{BASE}/en/plugins/{slug}/" if lang == "de" else f"{BASE}/plugins/{slug}/") if p.get("en") else None
    og = f"{BASE}/images/plugins/{slug}/og.jpg"
    buy, demo = GUMROAD + slug, GUMROAD + slug + "-demo"
    price = f"{p['price']:.2f}"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": t["title"], "description": t["desc"], "inLanguage": lang,
         "isPartOf": {"@id": BASE + "/#website"}, "mainEntity": {"@id": url + "#product"}, "primaryImageOfPage": {"@type": "ImageObject", "url": og, "width": 1200, "height": 630},
         "datePublished": PLUGIN_DATE, "dateModified": DATUM, "author": autor_ld()},
        {"@type": ["Product", "SoftwareApplication"], "@id": url + "#product", "name": name, "description": strip(t["answer"]),
         "author": autor_ld(), "dateModified": DATUM,
         "applicationCategory": "MultimediaApplication", "applicationSubCategory": p["sub"] if lang == "de" else "Audio plugin (VST3)", "operatingSystem": t["os"],
         "brand": {"@type": "Brand", "name": "Code Chaos Audio"}, "category": "Audio Plugin",
         "image": og, "screenshot": f"{BASE}/images/plugins/{slug}/gui-880.jpg", "url": url,
         "downloadUrl": buy, "featureList": [strip(f) for f in t["features"]],
         "offers": {"@type": "Offer", "url": buy, "price": price, "priceCurrency": "EUR", "availability": "https://schema.org/InStock",
                    "seller": {"@type": "Organization", "name": "Code Chaos Audio", "url": BASE + "/plugins/"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": L["home"], "item": BASE + L["home_url"]},
            {"@type": "ListItem", "position": 2, "name": "Plugins", "item": BASE + "/plugins/"},
            {"@type": "ListItem", "position": 3, "name": name, "item": url}]},
        {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": lang, "mainEntity": [
            {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in t["faq"]]},
    ]}
    if p.get("version"):
        ld["@graph"][1]["softwareVersion"] = p["version"]
    if p["price"] > 0:
        ld["@graph"][1]["isRelatedTo"] = {"@type": "SoftwareApplication", "name": f"{name} Demo", "url": demo,
                                          "applicationCategory": "MultimediaApplication", "operatingSystem": t["os"],
                                          "offers": {"@type": "Offer", "price": "0.00", "priceCurrency": "EUR", "url": demo}}
    specs = "".join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in t["specs"])
    feats = "".join(f"<li>{f}</li>" for f in t["features"])
    fmt_line = "VST3 + Standalone · " + t["os"]
    extra_imgs = "".join(
        f'<figure class="shot">{picture(slug, i["name"], i["w"], i["h"], i["alt"], sizes="(max-width: 800px) 100vw, 740px")}<figcaption>{esc(i["caption"])}</figcaption></figure>'
        for i in p.get("extra_images", []))
    more = []
    if t.get("extra_prose"):
        more.append(t["extra_prose"])
    if t.get("routing"):
        more.append(f"<h3>Routing</h3><p>{t['routing']}</p>")
    if t.get("pairs"):
        more.append(f"<p>{t['pairs']}</p>")
    extra_secs = "".join(f"""<section aria-labelledby="x{i}-t">
  <div class="wrap narrow prose">
    <h2 id="x{i}-t">{esc(h)}</h2>
    {inhalt}
  </div>
</section>
""" for i, (h, inhalt) in enumerate(t.get("extra_sections", []), 1))
    details = []
    if t.get("tested"):
        details.append(f"<h3>{L['tested']}</h3><p>{t['tested']}</p>")
    if t.get("good_to_know"):
        details.append(f"<h3>{L['good']}</h3><p>{t['good_to_know']}</p>")
    details.append((f"<h3>{L['formats']}</h3>" if details else "") + f"<p>{t['formats']}</p>")
    det_title = L["det_tested"] if t.get("tested") else L["formats"]
    if lang == "de":
        demo_hint = ("" if p["price"] == 0 else
                     f'<p>Nicht sicher? Die <a href="{utm(slug + "-demo", slug)}">kostenlose Demo</a> ist das vollständige Plugin mit einem kurzen Rauschen alle 45 Sekunden.</p>')
        preis_text = "kostenlos (Pay what you want)" if p["price"] == 0 else "für " + euro(p["price"])
        get_line = f"{esc(name)} gibt es auf Gumroad, {preis_text}, als Sofort-Download."
        rel = [BY_SLUG[s] for s in p["related"] if s in BY_SLUG]
        rel += [o for o in LIVE if o is not p and o not in rel and o["group"] == p["group"]]
        more_sec = f"""<section class="alt" aria-labelledby="more-t">
  <div class="wrap">
    <h2 id="more-t">Weitere Plugins von Code Chaos Audio</h2>
    <div class="pcards">{"".join(plugin_card(o, slug) for o in rel)}</div>
    <p class="prose" style="margin-top:22px"><a href="/plugins/">Alle Plugins im Überblick →</a></p>
  </div>
</section>"""
        crumbs = '<li><a href="/">Startseite</a></li><li><a href="/plugins/">Plugins</a></li>'
    else:
        demo_hint = ("" if p["price"] == 0 else
                     f'<p>Not sure yet? The <a href="{utm(slug + "-demo", slug)}">free demo</a> is the full plugin with a short noise burst every 45 seconds.</p>')
        get_line = (f'{esc(name)} is available on Gumroad for {price_l(p["price"], "en")} as an instant download. '
                    'Gumroad may show your local currency.')
        others = "".join(f'<li><a href="{plugin_url(o)}" hreflang="de">{esc(o["name"])}</a> · {price_l(o["price"], "en")}</li>'
                         for o in LIVE if o is not p and o["group"] == p["group"])
        more_sec = f"""<section class="alt" aria-labelledby="more-t">
  <div class="wrap narrow prose">
    <h2 id="more-t">More plugins by Code Chaos Audio</h2>
    <p>The other plugin pages are in German for now; specs, prices and audio demos are easy to follow.</p>
    <ul>{others}</ul>
    <p><a href="/plugins/" hreflang="de">All plugins (German) →</a> · <a href="/en/mastering/">Mastering for psytrance, hitech &amp; psycore →</a></p>
  </div>
</section>"""
        crumbs = '<li><a href="/en/">Home</a></li><li><a href="/plugins/" hreflang="de">Plugins</a></li>'
    sticky = L["free_dl"] if p["price"] == 0 else L["sticky_buy"].format(name=name, price=price_l(p["price"], lang))
    listen_note = f'<p class="note"><a href="#{L["listen_id"]}">{L["listen_link"]}</a></p>' if p.get("audio") else ""
    body = f"""<main id="main">
<div class="wrap crumbs"><nav aria-label="Breadcrumb"><ol>{crumbs}<li aria-current="page">{esc(name)}</li></ol></nav></div>
<section class="s-hero">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">{esc(t['eyebrow'])}</span>
      <h1>{esc(t['h1'])}</h1>
      <div class="rule" aria-hidden="true"><i></i></div>
      <p class="answer">{t['answer']}</p>
      <p class="price-line"><span class="price-tag">{price_l(p['price'], lang)}</span> {esc(fmt_line)}</p>
      <div class="btns">{cta_buttons(p, slug, lang=lang)}</div>
      {listen_note}
    </div>
    <figure class="shot">{picture(slug, "gui", p["gui_w"], p["gui_h"], t["gui_alt"], lazy=False)}<figcaption>{esc(L['real_gui'].format(name=name))}</figcaption></figure>
  </div>
</section>
{audio_html(p, lang, t)}<section aria-labelledby="specs-t">
  <div class="wrap narrow">
    <h2 id="specs-t">{esc(L['glance'].format(name=name))}</h2>
    <div class="table-scroll"><table class="specs"><tbody>{specs}</tbody></table></div>
  </div>
</section>
<section class="alt" aria-labelledby="feat-t">
  <div class="wrap narrow prose">
    <h2 id="feat-t">{esc(t.get("feat_title", L["features"]))}</h2>
    <ul>{feats}</ul>
    {extra_imgs}
    {"".join(more)}
  </div>
</section>
{extra_secs}<section aria-labelledby="det-t">
  <div class="wrap narrow prose">
    <h2 id="det-t">{det_title}</h2>
    {"".join(details)}
  </div>
</section>
<section class="alt" aria-labelledby="faq-t">
  <div class="wrap narrow">
    <h2 id="faq-t">{esc(L['faq'].format(name=name))}</h2>
    {faq_html(t['faq'])}
  </div>
</section>
<section aria-labelledby="cta-t">
  <div class="wrap narrow prose">
    <h2 id="cta-t">{esc(L['get'].format(name=name))}</h2>
    <p>{get_line}</p>
    {demo_hint}
    <div class="btns">{cta_buttons(p, slug, lang=lang)}</div>
  </div>
</section>
{more_sec}
</main>
<a class="sticky-cta" href="{utm(slug, slug)}">{esc(sticky)}</a>
"""
    html = head(lang, url, alt_url, t["title"], t["desc"], og, f"{name} {L['by']}: {t['category']}", ld, og_type="product") \
        + nav(lang, alt_url, "plug") + body + footer(lang)
    html, _ = geo.ausbauen(html, f"{pre}/plugins/{slug}/", lang, art="plugin")
    path = os.path.join(ROOT, pre.strip("/"), "plugins", slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8", newline="\n").write(html)
    return path


def build_crucible_redirect():
    """/crucible.html → /plugins/crucible/ (GitHub Pages kann kein 301: meta refresh + canonical + JS, Grok #66).
    Alte Sprunganker (#listen, #faq …) werden auf die neue Seite übertragen."""
    ziel = "/plugins/crucible/"
    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>Crucible: 3-Band-Sättigung VST3 | Code Chaos Audio</title>
<link rel="canonical" href="{BASE}{ziel}">
<meta http-equiv="refresh" content="0; url={ziel}">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script>(function(){{var m={{"#listen":"#hoeren","#faq":"#faq-t","#crucible-faq":"#faq-t"}},h=location.hash;location.replace("{ziel}"+(m[h]||""));}})();</script>
</head>
<body>
<p>Crucible ist umgezogen: <a href="{ziel}">codechaos-official.de/plugins/crucible/</a> · English: <a href="/en/plugins/crucible/" hreflang="en">codechaos-official.de/en/plugins/crucible/</a></p>
</body>
</html>
"""
    path = os.path.join(ROOT, "crucible.html")
    open(path, "w", encoding="utf-8", newline="\n").write(html)
    return path


PLUGINS_INDEX = dict(
    title="Plugins: VST3 für Psytrance & Black Metal | Code Chaos",
    desc="Audio-Plugins von Code Chaos Audio: Crucible, Shardstep, Chaos FM, Gravesaw, Rimehall und das kostenlose Kick/Bass Scope. VST3, Gratis-Demos.",
    h1="Audio-Plugins von Code Chaos Audio",
    answer="Code Chaos Audio ist die Plugin-Reihe von Code Chaos (Tim Borchert, Hamburg): VST3-Plugins für Hitech, Psycore und Darkpsy und die Code Chaos Black Metal Suite. "
           "Alle Plugins gibt es auf Gumroad als Sofort-Download, zu jedem Bezahl-Plugin eine kostenlose Demo (vollständiges Plugin mit einem kurzen Rauschen alle 45 Sekunden).",
)


def plugins_faq(allp, mac):
    """FAQ der Übersicht: nur Fragen, die auf den Plugin-Seiten schon stehen (Mac, Demo, kostenlos), Antworten aus den Plugin-Daten."""
    def liste(namen):
        return namen[0] if len(namen) == 1 else ", ".join(namen[:-1]) + " und " + namen[-1]
    mac_ja = [p["name"] for p in allp if mac(p) != "nein"]
    mac_nein = [p["name"] for p in allp if mac(p) == "nein"]
    gratis = [p for p in allp if p["price"] == 0]
    preise = sorted(p["price"] for p in allp if p["price"] > 0)
    return [
        ("Laufen die Plugins auf dem Mac?",
         f"{liste(mac_ja)} gibt es auch für macOS, aber nur für Macs mit Apple Silicon (arm64), einen Intel-Build gibt es nicht. "
         "Die macOS-Builds sind nicht signiert und nicht notarisiert: macOS blockiert sie beim ersten Start, du erlaubst sie unter "
         f"Systemeinstellungen → Datenschutz &amp; Sicherheit. {liste(mac_nein)} laufen nur unter Windows 10/11."),
        ("Laufen die Plugins in Logic Pro?",
         "Nein. Alle Plugins gibt es als VST3 und Standalone, ein AU-Format gibt es nicht, deshalb laufen sie nicht in Logic Pro."),
        ("Gibt es kostenlose Demos?",
         "Ja. Zu jedem Bezahl-Plugin gibt es auf Gumroad eine kostenlose Demo: das vollständige Plugin mit einem kurzen Rauschen alle 45 Sekunden."),
        ("Welches Plugin ist kostenlos?",
         f"{liste([p['name'] for p in gratis])}. Auf Gumroad gilt Pay what you want: Du kannst 0 € eingeben oder etwas zahlen, wenn dir das Plugin hilft."),
        ("Wo kann ich die Plugins kaufen?",
         f"Auf Gumroad, als Sofort-Download. Die Bezahl-Plugins kosten zwischen {preise[0]} und {preise[-1]} €, die Preise stehen in der Tabelle oben."),
    ]


def build_plugins_index():
    url = BASE + "/plugins/"
    order = {g: [p for p in LIVE if p["group"] == g] for g, _, _ in GROUPS}
    allp = [p for g, _, _ in GROUPS for p in order[g]]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": PLUGINS_INDEX["title"], "description": PLUGINS_INDEX["desc"],
         "inLanguage": "de", "isPartOf": {"@id": BASE + "/#website"}, "datePublished": PLUGIN_DATE, "dateModified": DATUM, "author": autor_ld(),
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
    faq = plugins_faq(allp, mac)
    ld["@graph"].append({"@type": "FAQPage", "@id": url + "#faq", "inLanguage": "de", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faq]})
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
<section class="alt" aria-labelledby="faq-t">
  <div class="wrap narrow">
    <h2 id="faq-t">Häufige Fragen zu den Plugins</h2>
    {faq_html(faq)}
  </div>
</section>
</main>
"""
    html = head("de", url, BASE + "/en/plugins/", PLUGINS_INDEX["title"], PLUGINS_INDEX["desc"], BASE + "/images/plugins/shardstep/og.jpg",
                "Audio-Plugins von Code Chaos Audio", ld, og_type="website") + nav("de", BASE + "/en/plugins/", "plug") + body + footer("de")
    html, _ = geo.ausbauen(html, "/plugins/", "de", art="plugin")
    path = os.path.join(ROOT, "plugins", "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8", newline="\n").write(html)
    return path


EN_PLUG = {   # Übersetzung der DE-Teaser/Kategorien aus content_plugins.py (Grok #67, 11.11.2026)
    "crucible": ("3-band saturation", "3-band saturation: hard clip, wavefolder, tube, diode or tape per band, up to 8x oversampling."),
    "shardstep": ("Stutter and glitch effect", "Stutter, repeats, tape stop and reverse synced to your DAW, built for 200 to 300 BPM."),
    "psy-kick-bass": ("Kick and rolling bass instrument", "Kick and rolling bass in one plugin: the kick is tuned to the bass and ends before the first bass note."),
    "chaos-fm": ("FM synthesizer", "3-operator FM synth with a GENERATE button for leads, basses, acid, stabs, plucks and FX."),
    "kick-bass-scope": ("Oscilloscope / analyzer for kick and bass", "Free: kick and bass overlaid in time with your DAW, with phase warning and clip line."),
    "gravesaw": ("Amp + cab for guitar and bass", "Black metal amp with built-in cab for guitar and bass DI, from raw and sawing to thick."),
    "rimehall": ("Reverb, shimmer and tape (atmosphere bus)", "Cold reverb up to 30 s, octave shimmer and tape lo-fi with ducking, so the riff stays in front."),
    "frostfret": ("Physically modelled guitar and bass", "Electric guitar, steel and nylon acoustic and electric bass via MIDI, physically modelled, no samples."),
    "hoarfell": ("Modelled drums, bass and atmosphere", "Modelled drum kit for blast beats, electric bass and choir/organ/strings, no samples."),
}
EN_GROUPS = {
    "psy": ("For hitech, psycore and darkpsy", "Built for fast, dense psytrance productions: saturation, glitch, FM sounds and control over kick and bass."),
    "metal": ("For black metal: the Code Chaos Black Metal Suite", "Amp, reverb and atmosphere for a cold, raw black metal sound from the home studio."),
}


def build_plugins_index_en():
    url = BASE + "/en/plugins/"
    order = {g: [p for p in LIVE if p["group"] == g] for g, _, _ in GROUPS}
    allp = [p for g, _, _ in GROUPS for p in order[g]]
    title = "Audio Plugins for Psytrance & Black Metal (VST3) | Code Chaos"
    desc = ("VST3 plugins by Code Chaos Audio for hitech, psycore, darkpsy and black metal: saturation, glitch, FM synth, "
            "kick and bass, amp and reverb. Free demo for every paid plugin.")

    def en_url(p):
        return f"/en/plugins/{p['slug']}/" if p.get("en") else plugin_url(p)

    def euro_en(price):
        return "Free" if price == 0 else f"€{price}"

    def card(p):
        cat, teaser = EN_PLUG[p["slug"]]
        alt = p["en"]["gui_alt"] if p.get("en") else f"{p['name']} plugin interface"
        img = picture(p["slug"], "gui", p["gui_w"], p["gui_h"], alt, sizes="(max-width: 700px) 100vw, 340px")
        de_note = "" if p.get("en") else ' <span class="note">(page in German)</span>'
        hl = "" if p.get("en") else ' hreflang="de"'
        links = (f'<a href="{utm(p["slug"], "plugins-en")}">Free download</a>' if p["price"] == 0 else
                 f'<a href="{utm(p["slug"] + "-demo", "plugins-en")}">Free demo</a><a href="{utm(p["slug"], "plugins-en")}">Buy</a>')
        return (f'<article class="pcard"><a class="pcard-img" href="{en_url(p)}"{hl} tabindex="-1" aria-hidden="true">{img}</a>'
                f'<div class="pcard-body"><h3><a href="{en_url(p)}"{hl}>{esc(p["name"])}</a></h3><p>{esc(teaser)}</p>'
                f'<p class="pcard-meta"><span class="price-tag">{euro_en(p["price"])}</span> {esc(cat)}</p>'
                f'<p class="pcard-links"><a href="{en_url(p)}"{hl}>Details &amp; audio{de_note}</a>{links}</p></div></article>')

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
         "inLanguage": "en", "isPartOf": {"@id": BASE + "/#website"}, "datePublished": "2026-11-11", "dateModified": DATUM, "author": autor_ld(),
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": p["name"], "url": BASE + en_url(p)} for i, p in enumerate(allp)]}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/en/"},
            {"@type": "ListItem", "position": 2, "name": "Plugins", "item": url}]},
    ]}
    groups = ""
    for i, (g, _, _) in enumerate(GROUPS):
        h, intro = EN_GROUPS[g]
        cards = "".join(card(p) for p in order[g])
        groups += f"""<section{' class="alt"' if i % 2 == 0 else ''} aria-labelledby="g-{g}">
  <div class="wrap">
    <h2 id="g-{g}">{esc(h)}</h2>
    <p class="prose">{esc(intro)}</p>
    <div class="pcards">{cards}</div>
  </div>
</section>
"""

    def mac(p):
        return "no" if p["slug"] in ("crucible", "chaos-fm") else "Apple Silicon (unsigned)"
    rows = "".join(f'<tr><th scope="row"><a href="{en_url(p)}">{esc(p["name"])}</a></th><td>{esc(EN_PLUG[p["slug"]][0])}</td>'
                   f'<td>{euro_en(p["price"])}</td><td>yes</td><td>{mac(p)}</td></tr>' for p in allp)
    body = f"""<main id="main">
<div class="wrap crumbs"><nav aria-label="Breadcrumb"><ol><li><a href="/en/">Home</a></li><li aria-current="page">Plugins</li></ol></nav></div>
<section class="s-hero">
  <div class="wrap narrow">
    <span class="eyebrow">Code Chaos Audio</span>
    <h1>Audio plugins for psytrance and black metal</h1>
    <div class="rule" aria-hidden="true"><i></i></div>
    <p class="answer">VST3 + standalone plugins by Code Chaos Audio for hitech, psycore, darkpsy and black metal, sold on Gumroad. Every paid plugin comes with a free demo, Kick/Bass Scope is free.</p>
  </div>
</section>
{groups}<section aria-labelledby="cmp-t">
  <div class="wrap narrow">
    <h2 id="cmp-t">Formats and systems compared</h2>
    <div class="table-scroll"><table class="cmp"><thead><tr><th>Plugin</th><th>Type</th><th>Price</th><th>Windows 10/11</th><th>macOS</th></tr></thead><tbody>{rows}</tbody></table></div>
    <p class="note" style="margin-top:14px">All plugins as VST3 + standalone. No AU format, so they do not run in Logic Pro. The macOS builds are Apple Silicon (arm64) only, unsigned and not notarized: macOS blocks them on first launch, allow them under System Settings → Privacy &amp; Security.</p>
  </div>
</section>
</main>
"""
    html = head("en", url, BASE + "/plugins/", title, desc, BASE + "/images/plugins/shardstep/og.jpg",
                "Audio plugins by Code Chaos Audio", ld, og_type="website") + nav("en", BASE + "/plugins/", "plug") + body + footer("en")
    html, _ = geo.ausbauen(html, "/en/plugins/", "en", art="plugin")
    path = os.path.join(ROOT, "en", "plugins", "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8", newline="\n").write(html)
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

# ───────────── Lautheits-Datenseite (Grok #72, 12.11.2026; Texte/Tabellen aus _build/daten/, siehe md_daten.py) ─────────────
DATEN_PFAD = {"de": "/psy-lautheit-daten/", "en": "/en/psy-loudness-data/"}
# Titel auf <= 60 Zeichen gekürzt (Tims SEO-Regel), das Frontmatter der Quellen hatte 76-81 Zeichen
DATEN_TITEL = {"de": "Psytrance & Hitech Lautheit: LUFS von 553 Releases",
               "en": "Psytrance & Hitech Loudness Data: LUFS of 553 Releases"}
# Descriptions auf <= 160 Zeichen gekürzt (Quelle 161/172), Zahlen unverändert aus genre_index.json
DATEN_DESC = {"de": "Gemessen: Hitech und Psycore liegen im Median bei etwa −8,3 LUFS (553 Tracks), Full-on und Dark Psy bei −7,9, Hardcore bei −6. Mediane, Spannen, Methode.",
              "en": "Measured: hitech and psycore releases sit at about -8.3 LUFS (553 tracks), full-on and dark psytrance near -7.9, hardcore at -6. Medians, ranges, method."}
DATEN_TECHNIK = "ITU-R BS.1770 integrated loudness, DR database method, third-octave spectrum"
DATEN_VARIABLEN = {
    "de": [("Integrierte Lautheit", "LUFS", "integrierte Lautheit nach ITU-R BS.1770 je Track; Median und 25. bis 75. Perzentil je Genre"),
           ("Dynamikwert (DR)", "dB", "Methode der DR-Datenbank: zweithöchster Spitzenwert gegen die lautesten 20 % der RMS-Blöcke"),
           ("Lautheitsumfang (LRA)", "LU", "Loudness Range nach EBU R 128"),
           ("Peak-to-Loudness-Ratio (PLR)", "dB", "True Peak minus integrierte Lautheit"),
           ("Side/Mid-Verhältnis", "dB", "Energie des Seitensignals gegen das Mittensignal"),
           ("Korrelation unter 150 Hz", None, "Phasenkorrelation im Low End, 1,00 = mono"),
           ("Tonale Balance relativ zu 1 kHz", "dB", "Terzspektrum, in fünf Bänder gruppiert, relativ zum 1-kHz-Band")],
    "en": [("Integrated loudness", "LUFS", "ITU-R BS.1770 integrated loudness per track; median and 25th to 75th percentile per genre"),
           ("Dynamic range (DR)", "dB", "DR database method: second-highest peak against the loudest 20 % of RMS blocks"),
           ("Loudness range (LRA)", "LU", "EBU R 128 loudness range"),
           ("Peak-to-loudness ratio (PLR)", "dB", "true peak minus integrated loudness"),
           ("Side/mid ratio", "dB", "energy of the side signal against the mid signal"),
           ("Correlation below 150 Hz", None, "phase correlation of the low end, 1.00 = mono"),
           ("Tonal balance relative to 1 kHz", "dB", "third-octave spectrum, grouped into five bands, relative to the 1 kHz band")],
}


def build_daten(lang):
    import md_daten
    meta, intro, sections = md_daten.lesen(lang)
    pfad = DATEN_PFAD[lang]
    assert meta["url"] == pfad, meta["url"]
    url = BASE + pfad
    alt = BASE + DATEN_PFAD["en" if lang == "de" else "de"]
    u = UI[lang]
    assert len(intro) == 2 and intro[1][1].startswith("**"), "Intro = Einleitung + Kurzantwort erwartet"
    kurz = re.sub(r"^<strong>[^<]*</strong>\s*", "", md_daten.inline(intro[1][1]))
    crumb = "Lautheit: Messdaten" if lang == "de" else "Loudness data"
    secs, faqs = [], []
    for i, (titel, bl) in enumerate(sections):
        cls = ' class="alt"' if i % 2 == 0 else ""
        if "FAQ" in titel or "Häufige Fragen" in titel:
            faqs, rest = md_daten.faq(bl)
            assert len(faqs) >= 4, "FAQ nicht gefunden"
            weiter = "".join(md_daten.block_html(b) for b in rest)
            secs.append(f'<section{cls}>\n  <div class="wrap narrow">\n    <h2>{md_daten.inline(titel)}</h2>\n    {faq_html(faqs)}{weiter}\n  </div>\n</section>')
        else:
            inner = "\n".join(md_daten.block_html(b) for b in bl)
            secs.append(f'<section{cls}>\n  <div class="wrap narrow prose">\n    <h2>{md_daten.inline(titel)}</h2>\n{inner}\n  </div>\n</section>')
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url + "#article", "headline": meta["h1"], "description": meta["description"], "inLanguage": lang,
         "url": url, "mainEntityOfPage": url, "datePublished": "2026-11-12", "dateModified": DATUM,
         "author": autor_ld(), "publisher": publisher_ld(), "image": BASE + "/images/og/mastering.jpg",
         "about": {"@id": url + "#dataset"}, "isPartOf": {"@id": BASE + "/#website"}},
        {"@type": "Dataset", "@id": url + "#dataset", "name": meta["h1"], "description": meta["description"], "url": url,
         "inLanguage": lang, "creator": {"@type": "Person", "@id": PERSON, "name": "Tim Borchert"}, "publisher": publisher_ld(),
         "isAccessibleForFree": True, "measurementTechnique": DATEN_TECHNIK, "temporalCoverage": "2026", "dateModified": DATUM,
         "keywords": ["hitech", "psycore", "psytrance", "LUFS", "loudness", "mastering", "dynamic range", "hardcore", "dubstep", "drum and bass"],
         "variableMeasured": [dict({"@type": "PropertyValue", "name": n, "description": d}, **({"unitText": e} if e else {}))
                              for n, e, d in DATEN_VARIABLEN[lang]]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": u["home"], "item": BASE + u["home_url"]},
            {"@type": "ListItem", "position": 2, "name": "Mastering", "item": BASE + u["mastering_url"]},
            {"@type": "ListItem", "position": 3, "name": crumb, "item": url}]},
        {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": lang, "mainEntity": [
            {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]},
    ]}
    body = f"""<main id="main">
<div class="wrap crumbs"><nav aria-label="Breadcrumb"><ol><li><a href="{u['home_url']}">{u['home']}</a></li><li><a href="{u['mastering_url']}">Mastering</a></li><li aria-current="page">{crumb}</li></ol></nav></div>
<section class="s-hero">
  <div class="wrap narrow">
    <span class="eyebrow">{"Daten · Lautheit" if lang == "de" else "Data · Loudness"}</span>
    <h1>{esc(meta['h1'])}</h1>
    <div class="rule" aria-hidden="true"><i></i></div>
    <p>{md_daten.inline(intro[0][1])}</p>
    <p class="answer">{kurz[:1].upper() + kurz[1:]}</p>
  </div>
</section>
{chr(10).join(secs)}
</main>
"""
    h = head(lang, url, alt, DATEN_TITEL[lang], DATEN_DESC[lang], BASE + "/images/og/mastering.jpg",
             "Lautheit von Hitech-, Psytrance- und Hardcore-Releases, gemessen von Code Chaos" if lang == "de"
             else "Loudness of hitech, psytrance and hardcore releases, measured by Code Chaos", ld) \
        + nav(lang, alt, "mast") + body + footer(lang)
    h, _ = geo.ausbauen(h, pfad, lang, art="mastering")
    path = os.path.join(ROOT, pfad.strip("/"), "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8", newline="\n").write(h)
    return path


if __name__ == "__main__":
    for lang in ("de", "en"):
        print(build_daten(lang))
    for g in GENRES:
        for lang in ("de", "en"):
            print(build_genre(g, lang))
    print(build_en_home())
    print(build_mastering("de"))
    print(build_mastering("en"))
    for slug in ("uhrwerk-aus-blut", "wiedergaenger-vol-1"):
        for lang in ("de", "en"):
            print(build_release(slug, lang))
    print(build_404())
    print(build_plugins_index())
    print(build_plugins_index_en())
    for p in LIVE:
        print(build_plugin(p))
        if p.get("en"):
            print(build_plugin(p, "en"))
    print(build_crucible_redirect())
    # handgeschriebene Seiten: dieselben GEO-Bausteine (TOC, Datum, Autorenbox), danach JSON-LD der Startseite
    for p in geo.handseiten():
        print(p)
    geo.REG.speichern()
    import runpy
    runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema_home.py"), run_name="__main__")
    # Startseite: CSS inline aus den Dateien (Grok #67)
    import inline_css
    inline_css.lauf()
