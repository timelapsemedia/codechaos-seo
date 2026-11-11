# Release-Seiten /uhrwerk-aus-blut/ und /wiedergaenger-vol-1/ (+ /en/…). Erzeugt von build_pages.build_release().
# NUR Fakten, die schon im Repo stehen (llms.txt, Startseite). Nichts erfinden: kein Label, kein Cover, kein
# Pre-Save-Link für Wiedergänger, solange keiner im Repo steht (dann Newsletter-CTA /#newsletter).
# KI-Hinweis nur „Bild mit KI erstellt“ / „Artwork created with AI“, Stimmen nie erwähnen.
# Platzhalter: {faq} wird vom Generator ersetzt (str.replace, keine format()-Klammern nötig).

STREAM = "https://distrokid.com/hyperfollow/codechaos/uhrwerk-aus-blut-2"
WG_TRACKS = ["Error 666", "Antichrist", "The Human Paradox", "Abstrakte Musik", "Rotten Soil"]

_SZENEN = [  # (Nummer DE, Nummer EN, Titel DE, Titel EN, Zitat DE, Übersetzung EN)
    ("Prolog", "Prologue", "Sechzig Schläge", "Sixty beats",
     "Man sagt, das Herz schlägt sechzig Mal in der Minute. Meines schlug hundertfünf.",
     "They say the heart beats sixty times a minute. Mine beat a hundred and five."),
    ("I", "I", "Die Uhr", "The Clock",
     "Hörst du sie ticken? Das ist nicht die Uhr. Das bin ich.",
     "Can you hear it ticking? That is not the clock. That is me."),
    ("II", "II", "Der Spiegel", "The Mirror",
     "Im Spiegel steht einer, der mein Gesicht trägt. Er lächelt, wenn ich schreie.",
     "In the mirror stands someone who wears my face. He smiles when I scream."),
    ("III", "III", "Das Blut", "The Blood",
     "In der Stille zwischen zwei Schlägen hörte ich mein Blut rückwärts fließen.",
     "In the silence between two beats I heard my blood flowing backwards."),
    ("Rückkehr", "Return", "Zähl mit mir", "Count with me",
     "Zähl mit mir. Zähl mit mir, bis nichts mehr bleibt.",
     "Count with me. Count with me until nothing remains."),
]


def _szenen(lang):
    out = []
    for nde, nen, tde, ten, zde, zen in _SZENEN:
        if lang == "de":
            out.append(f'<li><span class="scene-num">{nde}</span><h3>{tde}</h3><blockquote><p>{zde}</p></blockquote></li>')
        else:
            out.append(f'<li><span class="scene-num">{nen}</span><h3>{ten} <small lang="de">({tde})</small></h3>'
                       f'<blockquote><p lang="de">{zde}</p></blockquote><p class="note">{zen}</p></li>')
    return '<ol class="scenes">' + "".join(out) + "</ol>"


def _tracks():
    return '<ol class="tracklist">' + "".join(f"<li>{t}</li>" for t in WG_TRACKS) + "</ol>"


_COVER = ('<figure class="rel-cover"><picture><source type="image/webp" srcset="/images/uhrwerk-aus-blut/cover-800.webp 800w, '
          '/images/uhrwerk-aus-blut/cover-1600.webp 1600w" sizes="(min-width:900px) 460px, calc(100vw - 40px)">'
          '<img class="framed" src="/images/uhrwerk-aus-blut/cover-800.jpg" width="800" height="800" fetchpriority="high" decoding="async" alt="{alt}"></picture>'
          '<figcaption class="note">{cap}</figcaption></figure>')

_EXT = 'target="_blank" rel="noopener noreferrer"'

RELEASE_PAGES = {
 "uhrwerk-aus-blut": {
  "og": "/images/uhrwerk-aus-blut/og-uhrwerk-aus-blut.jpg",
  "de": {
   "nav": "Uhrwerk aus Blut",
   "title": "Uhrwerk aus Blut · Single von Code Chaos (30.10.2026)",
   "desc": "„Uhrwerk aus Blut“, die Single von Code Chaos: erschienen am 30.10.2026 auf Abstract Sound Design, erzählt in fünf Szenen. Jetzt überall streamen.",
   "og_alt": "Uhrwerk aus Blut: ein goldenes, mechanisches Herz in einem Ziffernblatt, aus dem Blut tropft",
   "faq": [
     ("Wann ist „Uhrwerk aus Blut“ erschienen?", "Am 30. Oktober 2026 auf Abstract Sound Design. Die Single ist auf allen großen Streaming-Plattformen zu hören: <a href=\"" + STREAM + "\">jetzt streamen</a>."),
     ("Worum geht es in „Uhrwerk aus Blut“?", "Um ein Herz, das zu schnell schlägt, und ein Uhrwerk, das blutet. Die Geschichte ist in fünf Szenen erzählt: Prolog, Die Uhr, Der Spiegel, Das Blut und Rückkehr."),
     ("Was kommt nach „Uhrwerk aus Blut“?", "Das nächste Release ist <a href=\"/wiedergaenger-vol-1/\">Wiedergänger Vol. I · Was nicht ruhen will</a>, ein Remix-Release mit fünf Tracks, am 4. Dezember 2026."),
   ],
   "body": """<main id="main">
<div class="wrap crumbs"><nav aria-label="Breadcrumb"><ol><li><a href="/">Startseite</a></li><li><a href="/releases/">Releases</a></li><li aria-current="page">Uhrwerk aus Blut</li></ol></nav></div>
<section class="s-hero">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">Single · Code Chaos · erschienen am 30.10.2026</span>
      <h1>Uhrwerk aus Blut</h1>
      <div class="rule rule-left" aria-hidden="true"><i></i></div>
      <p class="lead">Ein Herz, das zu schnell schlägt. Ein Uhrwerk, das blutet.</p>
      <p class="answer">„Uhrwerk aus Blut“ ist die Single von Code Chaos, erschienen am <time datetime="2026-10-30">30. Oktober 2026</time> auf Abstract Sound Design und auf allen großen Streaming-Plattformen zu hören. Sie ist das erste Werk der Ära, die Code Chaos <strong>New Psychedelic Death Art</strong> nennt: dunkler, erzählend, mit Stimme und Bild.</p>
      <div class="btns"><a class="btn btn-blood" href=\"""" + STREAM + """\" """ + _EXT + """>Jetzt streamen</a><a class="btn btn-ghost" href="/wiedergaenger-vol-1/">Nächstes Release · 04.12.2026</a></div>
    </div>
    """ + _COVER.format(alt="Single-Cover „Uhrwerk aus Blut“ von Code Chaos: ein goldenes, mechanisches Herz in einem Ziffernblatt, aus dem Blut tropft", cap="Single-Cover · Bild mit KI erstellt") + """
  </div>
</section>
<section class="alt" aria-labelledby="fakten-t">
  <div class="wrap narrow">
    <h2 id="fakten-t">Fakten zur Single</h2>
    <div class="table-scroll"><table class="specs"><tbody>
      <tr><th scope="row">Artist</th><td>Code Chaos</td></tr>
      <tr><th scope="row">Release</th><td><time datetime="2026-10-30">30. Oktober 2026</time></td></tr>
      <tr><th scope="row">Label</th><td>Abstract Sound Design</td></tr>
      <tr><th scope="row">Format</th><td>Single · alle Streaming-Plattformen</td></tr>
      <tr><th scope="row">Genre</th><td>Darkpsy · Hitech Psytrance · Gothic</td></tr>
      <tr><th scope="row">Story</th><td>Fünf Szenen: Prolog, Die Uhr, Der Spiegel, Das Blut, Rückkehr</td></tr>
    </tbody></table></div>
  </div>
</section>
<section aria-labelledby="szenen-t">
  <div class="wrap narrow">
    <h2 id="szenen-t">Die Geschichte in fünf Szenen</h2>
    """ + _szenen("de") + """
    <div class="btns"><a class="btn btn-blood" href=\"""" + STREAM + """\" """ + _EXT + """>Jetzt streamen</a></div>
  </div>
</section>
<section class="alt" aria-labelledby="faq-t">
  <div class="wrap narrow">
    <h2 id="faq-t">Häufige Fragen zu „Uhrwerk aus Blut“</h2>
    {faq}
  </div>
</section>
<section aria-labelledby="mehr-t">
  <div class="wrap">
    <h2 id="mehr-t">Mehr von Code Chaos</h2>
    <div class="cards">
      <div class="card"><div class="bpm">Ankündigung · 04.12.2026</div><h3>Wiedergänger Vol. I</h3><p>Was nicht ruhen will: Remix-Release mit fünf Tracks.</p><a class="more" href="/wiedergaenger-vol-1/">Zum Release →</a></div>
      <div class="card"><div class="bpm">Code Chaos Audio · Gumroad</div><h3>Plugins</h3><p>Crucible, Kick+Bass Engine, Shardstep, Chaos FM und mehr. Zu jedem Bezahl-Plugin gibt es eine kostenlose Demo.</p><a class="more" href="/plugins/">Alle Plugins →</a></div>
      <div class="card"><div class="bpm">Code Chaos Mastering · ab 79 €</div><h3>Mastering</h3><p>Für Psytrance, Hitech und Psycore: Stereo 79 €, Stem 129 €, EP 349 €, Album 629 €.</p><a class="more" href="/mastering/">Zum Mastering →</a></div>
    </div>
  </div>
</section>
</main>
""",
  },
  "en": {
   "nav": "Uhrwerk aus Blut",
   "title": "Uhrwerk aus Blut · Single by Code Chaos (30 Oct 2026)",
   "desc": "\"Uhrwerk aus Blut\" (Clockwork of Blood), the single by Code Chaos: released 30 October 2026 on Abstract Sound Design, told in five scenes. Stream it now.",
   "og_alt": "Uhrwerk aus Blut: a golden mechanical heart inside a clock face, dripping blood",
   "faq": [
     ("When was \"Uhrwerk aus Blut\" released?", "On 30 October 2026 on Abstract Sound Design. The single is available on all major streaming platforms: <a href=\"" + STREAM + "\">listen now</a>."),
     ("What is \"Uhrwerk aus Blut\" about?", "A heart that beats too fast and a clockwork that bleeds. The story is told in five scenes: Prologue, The Clock, The Mirror, The Blood and Return."),
     ("What comes after \"Uhrwerk aus Blut\"?", "The next release is <a href=\"/en/wiedergaenger-vol-1/\">Wiedergänger Vol. I · Was nicht ruhen will</a>, a remix release with five tracks, out on 4 December 2026."),
   ],
   "body": """<main id="main">
<div class="wrap crumbs"><nav aria-label="Breadcrumb"><ol><li><a href="/en/">Home</a></li><li><a href="/en/#releases">Releases</a></li><li aria-current="page">Uhrwerk aus Blut</li></ol></nav></div>
<section class="s-hero">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">Single · Code Chaos · released 30 Oct 2026</span>
      <h1>Uhrwerk aus Blut</h1>
      <div class="rule rule-left" aria-hidden="true"><i></i></div>
      <p class="lead">A heart that beats too fast. A clockwork that bleeds.<br><span lang="de">„Ein Herz, das zu schnell schlägt. Ein Uhrwerk, das blutet.“</span></p>
      <p class="answer">"Uhrwerk aus Blut" (Clockwork of Blood) is the single by Code Chaos, released on <time datetime="2026-10-30">30 October 2026</time> on Abstract Sound Design and available on all major streaming platforms. It is the first release of the era Code Chaos calls <strong>New Psychedelic Death Art</strong>: darker, narrative, with voice and image.</p>
      <div class="btns"><a class="btn btn-blood" href=\"""" + STREAM + """\" """ + _EXT + """>Listen now</a><a class="btn btn-ghost" href="/en/wiedergaenger-vol-1/">Next release · 4 Dec 2026</a></div>
    </div>
    """ + _COVER.format(alt="Cover of the single Uhrwerk aus Blut by Code Chaos: a golden mechanical heart inside a clock face, dripping blood", cap="Single cover · Artwork created with AI") + """
  </div>
</section>
<section class="alt" aria-labelledby="facts-t">
  <div class="wrap narrow">
    <h2 id="facts-t">Single facts</h2>
    <div class="table-scroll"><table class="specs"><tbody>
      <tr><th scope="row">Artist</th><td>Code Chaos</td></tr>
      <tr><th scope="row">Release date</th><td><time datetime="2026-10-30">30 October 2026</time></td></tr>
      <tr><th scope="row">Label</th><td>Abstract Sound Design</td></tr>
      <tr><th scope="row">Format</th><td>Single · all streaming platforms</td></tr>
      <tr><th scope="row">Genre</th><td>Darkpsy · Hitech psytrance · Gothic</td></tr>
      <tr><th scope="row">Language</th><td>German (spoken scenes)</td></tr>
      <tr><th scope="row">Story</th><td>Five scenes: Prologue, The Clock, The Mirror, The Blood, Return</td></tr>
    </tbody></table></div>
  </div>
</section>
<section aria-labelledby="scenes-t">
  <div class="wrap narrow">
    <h2 id="scenes-t">The story in five scenes</h2>
    """ + _szenen("en") + """
    <div class="btns"><a class="btn btn-blood" href=\"""" + STREAM + """\" """ + _EXT + """>Listen now</a></div>
  </div>
</section>
<section class="alt" aria-labelledby="faq-t">
  <div class="wrap narrow">
    <h2 id="faq-t">FAQ: Uhrwerk aus Blut</h2>
    {faq}
  </div>
</section>
<section aria-labelledby="more-t">
  <div class="wrap">
    <h2 id="more-t">More from Code Chaos</h2>
    <div class="cards">
      <div class="card"><div class="bpm">Announcement · 4 Dec 2026</div><h3>Wiedergänger Vol. I</h3><p>Was nicht ruhen will: a remix release with five tracks.</p><a class="more" href="/en/wiedergaenger-vol-1/">See the release →</a></div>
      <div class="card"><div class="bpm">Code Chaos Audio · Gumroad</div><h3>Plugins</h3><p>Crucible, Kick+Bass Engine, Shardstep, Chaos FM and more. Every paid plugin has a free demo.</p><a class="more" href="/plugins/">All plugins (German) →</a></div>
      <div class="card"><div class="bpm">Code Chaos Mastering · from €79</div><h3>Mastering</h3><p>For psytrance, hitech and psycore: stereo €79, stem €129, EP €349, album €629.</p><a class="more" href="/en/mastering/">Mastering →</a></div>
    </div>
  </div>
</section>
</main>
""",
  },
 },
 "wiedergaenger-vol-1": {
  "og": "/images/wiedergaenger-vol-1/og-wiedergaenger-vol-1.jpg",
  "de": {
   "nav": "Wiedergänger Vol. I",
   "title": "Wiedergänger Vol. I · Was nicht ruhen will · Code Chaos",
   "desc": "Wiedergänger Vol. I · Was nicht ruhen will: nächstes Release von Code Chaos: Remix-Release mit fünf Tracks am 04.12.2026. Tracklist, Link zuerst per Newsletter.",
   "og_alt": "Wiedergänger Vol. I · Was nicht ruhen will · Code Chaos · 04.12.2026",
   "faq": [
     ("Wann erscheint „Wiedergänger Vol. I · Was nicht ruhen will“?", "Am 4. Dezember 2026."),
     ("Welche Tracks sind auf „Wiedergänger Vol. I“?", "Fünf Tracks: Error 666, Antichrist, The Human Paradox, Abstrakte Musik und Rotten Soil."),
     ("Wie bekomme ich den Link zum Release als Erstes?", "Über den Newsletter von Code Chaos: Der Link kommt dort zuerst. <a href=\"/#newsletter\">Zum Newsletter</a>."),
   ],
   "body": """<main id="main">
<div class="wrap crumbs"><nav aria-label="Breadcrumb"><ol><li><a href="/">Startseite</a></li><li><a href="/releases/">Releases</a></li><li aria-current="page">Wiedergänger Vol. I</li></ol></nav></div>
<section class="s-hero">
  <div class="wrap narrow">
    <span class="eyebrow">Ankündigung · Remix-Release · <time datetime="2026-12-04">04.12.2026</time></span>
    <h1>Wiedergänger Vol. I <span class="h1-sub">Was nicht ruhen will</span></h1>
    <div class="rule" aria-hidden="true"><i></i></div>
    <p class="answer">„Wiedergänger Vol. I · Was nicht ruhen will“ ist das nächste Release von Code Chaos: ein Remix-Release mit fünf Tracks, das am <time datetime="2026-12-04">4. Dezember 2026</time> erscheint.</p>
    <div class="btns"><a class="btn btn-blood" href="/#newsletter">Link zuerst per Newsletter</a><a class="btn btn-ghost" href="/uhrwerk-aus-blut/">Jetzt hören: Uhrwerk aus Blut</a></div>
  </div>
</section>
<section class="alt" aria-labelledby="tracks-t">
  <div class="wrap narrow">
    <h2 id="tracks-t">Tracklist</h2>
    """ + _tracks() + """
    <div class="table-scroll"><table class="specs"><tbody>
      <tr><th scope="row">Artist</th><td>Code Chaos</td></tr>
      <tr><th scope="row">Release</th><td><time datetime="2026-12-04">4. Dezember 2026</time></td></tr>
      <tr><th scope="row">Format</th><td>Remix-Release · 5 Tracks</td></tr>
    </tbody></table></div>
  </div>
</section>
<section aria-labelledby="faq-t">
  <div class="wrap narrow">
    <h2 id="faq-t">Häufige Fragen zu „Wiedergänger Vol. I“</h2>
    {faq}
  </div>
</section>
<section class="alt" aria-labelledby="bis-t">
  <div class="wrap">
    <h2 id="bis-t">Bis zum 4. Dezember</h2>
    <div class="cards">
      <div class="card"><div class="bpm">Erschienen · 30.10.2026</div><h3>Uhrwerk aus Blut</h3><p>Die aktuelle Single von Code Chaos auf Abstract Sound Design, erzählt in fünf Szenen.</p><a class="more" href="/uhrwerk-aus-blut/">Zur Single →</a></div>
      <div class="card"><div class="bpm">Code Chaos Audio · Gumroad</div><h3>Plugins</h3><p>Crucible, Kick+Bass Engine, Shardstep, Chaos FM und mehr. Zu jedem Bezahl-Plugin gibt es eine kostenlose Demo.</p><a class="more" href="/plugins/">Alle Plugins →</a></div>
      <div class="card"><div class="bpm">Code Chaos Mastering · ab 79 €</div><h3>Mastering</h3><p>Für Psytrance, Hitech und Psycore: Stereo 79 €, Stem 129 €, EP 349 €, Album 629 €.</p><a class="more" href="/mastering/">Zum Mastering →</a></div>
    </div>
  </div>
</section>
</main>
""",
  },
  "en": {
   "nav": "Wiedergänger Vol. I",
   "title": "Wiedergänger Vol. I · Code Chaos remix release, 4 Dec 2026",
   "desc": "Wiedergänger Vol. I · Was nicht ruhen will: the next Code Chaos release: five remix tracks, out 4 December 2026. Tracklist and link first via newsletter.",
   "og_alt": "Wiedergänger Vol. I · Was nicht ruhen will · Code Chaos · 4 December 2026",
   "faq": [
     ("When is \"Wiedergänger Vol. I · Was nicht ruhen will\" released?", "On 4 December 2026."),
     ("Which tracks are on \"Wiedergänger Vol. I\"?", "Five tracks: Error 666, Antichrist, The Human Paradox, Abstrakte Musik and Rotten Soil."),
     ("How do I get the release link first?", "Through the Code Chaos newsletter: the link goes out there first. <a href=\"/#newsletter\">Newsletter sign-up (German page)</a>."),
   ],
   "body": """<main id="main">
<div class="wrap crumbs"><nav aria-label="Breadcrumb"><ol><li><a href="/en/">Home</a></li><li><a href="/en/#releases">Releases</a></li><li aria-current="page">Wiedergänger Vol. I</li></ol></nav></div>
<section class="s-hero">
  <div class="wrap narrow">
    <span class="eyebrow">Announcement · remix release · <time datetime="2026-12-04">4 Dec 2026</time></span>
    <h1>Wiedergänger Vol. I <span class="h1-sub" lang="de">Was nicht ruhen will</span></h1>
    <div class="rule" aria-hidden="true"><i></i></div>
    <p class="answer">"Wiedergänger Vol. I · Was nicht ruhen will" is the next release by Code Chaos: a remix release with five tracks, out on <time datetime="2026-12-04">4 December 2026</time>.</p>
    <div class="btns"><a class="btn btn-blood" href="/#newsletter">Get the link first (newsletter)</a><a class="btn btn-ghost" href="/en/uhrwerk-aus-blut/">Listen now: Uhrwerk aus Blut</a></div>
  </div>
</section>
<section class="alt" aria-labelledby="tracks-t">
  <div class="wrap narrow">
    <h2 id="tracks-t">Tracklist</h2>
    """ + _tracks() + """
    <div class="table-scroll"><table class="specs"><tbody>
      <tr><th scope="row">Artist</th><td>Code Chaos</td></tr>
      <tr><th scope="row">Release date</th><td><time datetime="2026-12-04">4 December 2026</time></td></tr>
      <tr><th scope="row">Format</th><td>Remix release · 5 tracks</td></tr>
    </tbody></table></div>
  </div>
</section>
<section aria-labelledby="faq-t">
  <div class="wrap narrow">
    <h2 id="faq-t">FAQ: Wiedergänger Vol. I</h2>
    {faq}
  </div>
</section>
<section class="alt" aria-labelledby="until-t">
  <div class="wrap">
    <h2 id="until-t">Until 4 December</h2>
    <div class="cards">
      <div class="card"><div class="bpm">Out now · 30 Oct 2026</div><h3>Uhrwerk aus Blut</h3><p>The current single by Code Chaos on Abstract Sound Design, told in five scenes.</p><a class="more" href="/en/uhrwerk-aus-blut/">See the single →</a></div>
      <div class="card"><div class="bpm">Code Chaos Audio · Gumroad</div><h3>Plugins</h3><p>Crucible, Kick+Bass Engine, Shardstep, Chaos FM and more. Every paid plugin has a free demo.</p><a class="more" href="/plugins/">All plugins (German) →</a></div>
      <div class="card"><div class="bpm">Code Chaos Mastering · from €79</div><h3>Mastering</h3><p>For psytrance, hitech and psycore: stereo €79, stem €129, EP €349, album €629.</p><a class="more" href="/en/mastering/">Mastering →</a></div>
    </div>
  </div>
</section>
</main>
""",
  },
 },
}
