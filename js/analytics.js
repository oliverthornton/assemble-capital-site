// Assemble Capital — GA4 loader and conversion events.
//
// Production measurement ID: G-676QQYXN22 (GA4 property 551599429).
// Production hosts: assemble.capital, www.assemble.capital.
//
// This is a static site with no build step. The browser cannot read
// VERCEL_ENV or NEXT_PUBLIC_GA_MEASUREMENT_ID, so those variables are not
// consulted. The tag is requested only after a hostname allowlist check,
// which also keeps the production *.vercel.app alias, preview deployments,
// localhost, and every other host out of the production property.
// vercel.json redirects www.assemble.capital to the apex host before HTML
// is served; both hosts stay allowlisted in case that redirect is bypassed.
(function () {
  'use strict';

  var MEASUREMENT_ID = 'G-676QQYXN22';
  var PRODUCTION_HOSTS = {
    'assemble.capital': true,
    'www.assemble.capital': true
  };

  if (window.__assembleAnalytics) return;
  window.__assembleAnalytics = true;

  function productionHost() {
    var host = String((window.location && window.location.hostname) || '');
    host = host.toLowerCase().replace(/\.$/, '');
    return PRODUCTION_HOSTS[host] === true;
  }

  var enabled = productionHost();

  // Never forward free-text or contact fields. form_name is the only
  // parameter the conversion events are supposed to carry.
  var BLOCKED_KEYS = {
    email: true,
    phone: true,
    tel: true,
    name: true,
    first: true,
    last: true,
    first_name: true,
    last_name: true,
    full_name: true,
    message: true,
    notes: true,
    accredited: true,
    range: true,
    address: true,
    company: true,
    referred: true,
    asking_price: true,
    investment: true,
    role: true
  };

  function looksSensitive(value) {
    if (typeof value !== 'string') return false;
    if (value.indexOf('@') !== -1) return true;
    if (/^(tel:|mailto:)/i.test(value)) return true;
    if (/\d{3}[^\d]?\d{3}[^\d]?\d{4}/.test(value)) return true;
    return false;
  }

  function safeParams(params) {
    var out = {};
    if (!params) return out;
    for (var key in params) {
      if (!Object.prototype.hasOwnProperty.call(params, key)) continue;
      if (BLOCKED_KEYS[String(key).toLowerCase()]) continue;
      if (looksSensitive(params[key])) continue;
      out[key] = params[key];
    }
    return out;
  }

  function track(name, params) {
    if (!enabled || typeof window.gtag !== 'function') return;
    window.gtag('event', name, safeParams(params));
  }

  window.assembleTrack = track;
  window.assembleGaEnabled = enabled;

  if (enabled) {
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', MEASUREMENT_ID);

    var src = 'https://www.googletagmanager.com/gtag/js?id=' + MEASUREMENT_ID;
    var already = document.querySelector('script[src="' + src + '"]');
    if (!already) {
      var script = document.createElement('script');
      script.async = true;
      script.src = src;
      document.head.appendChild(script);
    }
  }

  // One listener for the whole document. The href is not sent: on this site
  // the visible link text is the address or phone number.
  document.addEventListener('click', function (event) {
    var node = event.target;
    var anchor = null;
    while (node && node !== document) {
      if (node.nodeName === 'A') { anchor = node; break; }
      node = node.parentNode;
    }
    if (!anchor || !anchor.getAttribute) return;
    var href = String(anchor.getAttribute('href') || '');
    var lower = href.slice(0, 7).toLowerCase();
    if (lower.indexOf('tel:') === 0) track('click_to_call');
    else if (lower.indexOf('mailto:') === 0) track('click_to_email');
  });
})();
