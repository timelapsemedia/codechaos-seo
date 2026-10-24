/* Google Analytics 4 nur mit Einwilligung (24.10.2026, Muster wie polished.media).
   Banner wird von diesem Skript erzeugt; Auswahl in localStorage. "Cookie-Einstellungen" (Links mit
   class="cookie-settings-link") öffnet den Banner erneut, damit der Widerruf so einfach ist wie die Einwilligung. */
(function () {
  var GA_ID = 'G-TQPP6RXX77';
  var KEY = 'codechaos_analytics_consent';
  var en = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0;
  var T = en ? {
    text: 'We use Google Analytics to understand how this site is used, but only with your consent. You can change your choice at any time via “Cookie settings”. Details in the ',
    policy: 'privacy policy (German)', no: 'Necessary only', yes: 'Accept'
  } : {
    text: 'Wir nutzen Google Analytics, um zu verstehen, wie diese Seite genutzt wird, aber nur mit deiner Einwilligung. Du kannst deine Wahl jederzeit über „Cookie-Einstellungen“ ändern. Details in der ',
    policy: 'Datenschutzerklärung', no: 'Nur notwendige', yes: 'Akzeptieren'
  };

  function loadGA() {
    if (window.gtag) return;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID, { cookie_flags: 'SameSite=None;Secure', cookie_expires: 60 * 60 * 24 * 180 });
  }

  function disableGA() {
    window['ga-disable-' + GA_ID] = true;
    document.cookie.split(';').map(function (c) { return c.trim().split('=')[0]; })
      .filter(function (n) { return n.indexOf('_ga') === 0; })
      .forEach(function (n) {
        document.cookie = n + '=; Max-Age=0; path=/';
        document.cookie = n + '=; Max-Age=0; path=/; domain=.' + location.hostname.replace(/^www\./, '');
      });
  }

  var css = '#cc-consent{position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;max-width:720px;margin:0 auto;' +
    'background:#0b0806;color:#ece2ce;border:1px solid rgba(201,168,106,.35);border-radius:6px;padding:16px 18px;' +
    'font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;box-shadow:0 8px 30px rgba(0,0,0,.6);display:none}' +
    '#cc-consent.show{display:block}#cc-consent p{margin:0 0 12px}#cc-consent a{color:#c9a86a;text-decoration:underline}' +
    '#cc-consent .cc-row{display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end}' +
    '#cc-consent button{font:600 13px/1 system-ui,sans-serif;letter-spacing:.5px;padding:11px 18px;border-radius:4px;cursor:pointer;' +
    'border:1px solid #c9a86a;background:transparent;color:#ece2ce;min-width:150px}' +
    '#cc-consent button:focus-visible{outline:2px solid #c9a86a;outline-offset:2px}';

  function banner() {
    var b = document.getElementById('cc-consent');
    if (b) return b;
    var st = document.createElement('style');
    st.textContent = css;
    document.head.appendChild(st);
    b = document.createElement('div');
    b.id = 'cc-consent';
    b.setAttribute('role', 'dialog');
    b.setAttribute('aria-label', en ? 'Cookie settings' : 'Cookie-Einstellungen');
    b.innerHTML = '<p>' + T.text + '<a href="/#datenschutz">' + T.policy + '</a>.</p>' +
      '<div class="cc-row"><button type="button" id="cc-no">' + T.no + '</button>' +
      '<button type="button" id="cc-yes">' + T.yes + '</button></div>';
    document.body.appendChild(b);
    b.querySelector('#cc-yes').addEventListener('click', function () {
      try { localStorage.setItem(KEY, 'granted'); } catch (e) {}
      loadGA();
      b.classList.remove('show');
    });
    b.querySelector('#cc-no').addEventListener('click', function () {
      try { localStorage.setItem(KEY, 'denied'); } catch (e) {}
      disableGA();
      b.classList.remove('show');
    });
    return b;
  }

  window.ccCookieSettings = function (e) {
    if (e && e.preventDefault) e.preventDefault();
    banner().classList.add('show');
  };

  function start() {
    document.querySelectorAll('.cookie-settings-link').forEach(function (a) {
      a.addEventListener('click', window.ccCookieSettings);
    });
    var stored = null;
    try { stored = localStorage.getItem(KEY); } catch (e) {}
    if (stored === 'granted') loadGA();
    else if (stored !== 'denied') setTimeout(function () { banner().classList.add('show'); }, 1200);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
