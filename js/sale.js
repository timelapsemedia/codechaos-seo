/* Code Chaos Audio · Black Friday 2026.
   Shows a sale bar and applies the Gumroad code BLACKFRIDAY (-40 %, set up by Tim)
   to links of paid products, only inside the code's validity window
   (valid_at 2026-11-26T23:00Z, expires_at 2026-11-30T22:59Z). Outside the window it does nothing.
   Preview: append ?sale=preview to any page URL. */
(function () {
  var START = Date.UTC(2026, 10, 26, 23, 0), END = Date.UTC(2026, 10, 30, 22, 59);
  var CODE = 'BLACKFRIDAY';
  var PAID = ['psy-kick-bass', 'black-metal-suite-complete', 'black-metal-suite', 'frostfret', 'hoarfell',
    'gravesaw', 'rimehall', 'shardstep', 'black-metal-midi-grooves-2', 'black-metal-tone-kit',
    'hitech-fm-industrial', 'black-metal-drum-kit', 'psycore-ableton-template', 'chaos-fm',
    'hitech-fm-serum2', 'hitech-fm-vital', 'hitech-arsenal-1', 'crucible'];
  var now = Date.now();
  var preview = /[?&]sale=preview\b/.test(location.search);
  if (!preview && (now < START || now > END)) return;

  function run() {
    var en = (document.documentElement.lang || '').indexOf('en') === 0;
    // 1) paid product links: /l/<slug>?... -> /l/<slug>/BLACKFRIDAY?...
    // eigene Shop-Domain seit 24.11.2026, alte Gumroad-Adresse bleibt gültig: beide erkennen
    var links = document.querySelectorAll('a[href*="shop.codechaos-official.de/l/"], a[href*="timberwolf688.gumroad.com/l/"]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i], m = a.href.match(/^(https:\/\/(?:shop\.codechaos-official\.de|timberwolf688\.gumroad\.com)\/l\/)([a-z0-9-]+)(\/[^?#]*)?([?#].*)?$/);
      if (!m || m[3] || PAID.indexOf(m[2]) < 0) continue;
      a.href = m[1] + m[2] + '/' + CODE + (m[4] || '');
    }
    // 2) sale bar
    var css = '.cc-sale{position:relative;z-index:150;display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:6px 14px;' +
      'padding:10px 16px;background:#8e1016;color:#ece2ce;font:600 15px/1.4 Georgia,serif;text-align:center}' +
      '.cc-sale b{color:#fff;letter-spacing:.04em}.cc-sale code{font:700 14px/1 ui-monospace,Menlo,monospace;background:#0b0806;color:#dcc08a;padding:4px 8px;border:1px solid #c9a86a}' +
      '.cc-sale a{color:#fff;text-decoration:underline;text-underline-offset:3px}';
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    var bar = document.createElement('div'); bar.className = 'cc-sale'; bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', en ? 'Black Friday sale' : 'Black-Friday-Angebot');
    bar.innerHTML = en
      ? '<span><b>Black Friday:</b> 40% off every paid Code Chaos Audio product until 30 Nov.</span><span>Code <code>' + CODE + '</code> · applied automatically via the links on this site</span><a href="/en/plugins/">See the plugins</a>'
      : '<span><b>Black Friday:</b> 40 % auf alle bezahlten Code-Chaos-Audio-Produkte bis 30.11.</span><span>Code <code>' + CODE + '</code> · über die Links auf dieser Seite automatisch drin</span><a href="/plugins/">Zu den Plugins</a>';
    var skip = document.querySelector('body > .skip');
    if (skip) skip.parentNode.insertBefore(bar, skip.nextSibling); else document.body.insertBefore(bar, document.body.firstChild);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
