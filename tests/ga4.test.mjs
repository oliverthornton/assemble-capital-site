import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { dirname, join, relative } from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const analyticsSrc = readFileSync(join(root, 'js/analytics.js'), 'utf8');
const mainSrc = readFileSync(join(root, 'js/main.js'), 'utf8');
const dealSrc = readFileSync(join(root, 'js/submit-deal.js'), 'utf8');
const MEASUREMENT_ID = 'G-676QQYXN22';
const GTAG_SRC = 'https://www.googletagmanager.com/gtag/js?id=' + MEASUREMENT_ID;

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (name === '.git' || name === 'node_modules') continue;
    const path = join(dir, name);
    if (statSync(path).isDirectory()) walk(path, out);
    else out.push(path);
  }
  return out;
}

function pushed(dataLayer) {
  return Array.from(dataLayer || [], (args) => Array.prototype.slice.call(args));
}

function events(sandbox) {
  // Params are created inside the page sandbox, so compare a structured clone
  // in this realm instead of deep-equating across the two.
  return JSON.parse(JSON.stringify(
    pushed(sandbox.dataLayer).filter((row) => row[0] === 'event')
  ));
}

function createSandbox(hostname, extras = {}) {
  const scripts = [];
  const listeners = [];
  const location = {
    hostname,
    pathname: extras.pathname || '/contact.html',
    href: 'https://' + (hostname || 'local') + (extras.pathname || '/contact.html'),
  };
  const document = {
    head: {
      appendChild(el) {
        scripts.push(el);
        return el;
      },
    },
    createElement() {
      return { async: false, src: '' };
    },
    querySelector(sel) {
      if (String(sel).includes('googletagmanager.com/gtag/js')) return null;
      return extras.querySelector ? extras.querySelector(sel) : null;
    },
    querySelectorAll() {
      return [];
    },
    addEventListener(type, fn) {
      listeners.push({ type, fn });
    },
    body: {},
    documentElement: { classList: { add() {} } },
  };
  const sandbox = {
    window: null,
    document,
    location,
    console,
    Date: extras.Date || Date,
    Object,
    String,
    Array,
    Math,
    JSON,
    Error,
    Promise,
    encodeURIComponent,
    setTimeout,
    clearTimeout,
    FormData: extras.FormData,
    fetch: extras.fetch,
    crypto: extras.crypto,
    scripts,
    listeners,
  };
  sandbox.window = sandbox;
  vm.runInNewContext(analyticsSrc, sandbox, { filename: 'js/analytics.js' });
  return sandbox;
}

function click(sandbox, href, child = false) {
  const listener = sandbox.listeners.find((entry) => entry.type === 'click');
  const anchor = {
    nodeName: 'A',
    parentNode: sandbox.document,
    getAttribute(name) {
      return name === 'href' ? href : null;
    },
  };
  const target = child
    ? { nodeName: 'SPAN', parentNode: anchor }
    : anchor;
  listener.fn({ target });
}

test('public pages load the shared loader once and do not inline gtag', () => {
  const html = walk(root).filter((path) => path.endsWith('.html'));
  assert.ok(html.length > 100);
  for (const path of html) {
    const rel = relative(root, path).replaceAll('\\', '/');
    const source = readFileSync(path, 'utf8');
    const skipped = rel.startsWith('email-signatures/') || rel.startsWith('blog/drafts/');
    const loaders = source.split('src="/js/analytics.js"').length - 1;
    if (skipped) {
      assert.equal(loaders, 0, rel);
      assert.equal(source.includes('googletagmanager.com'), false, rel);
      continue;
    }
    assert.equal(loaders, 1, rel);
    assert.equal(source.includes('googletagmanager.com'), false, rel);
    assert.equal(source.includes(MEASUREMENT_ID), false, rel);
    assert.ok(source.indexOf('src="/js/analytics.js"') < source.indexOf('</head>'), rel);
  }
});

test('the measurement ID is documented in the loader and nowhere else in HTML', () => {
  assert.match(analyticsSrc, /Production measurement ID: G-676QQYXN22/);
  assert.match(analyticsSrc, /assemble\.capital/);
  assert.match(analyticsSrc, /www\.assemble\.capital/);
  assert.doesNotMatch(mainSrc, /gtag\s*\(/);
  assert.doesNotMatch(dealSrc, /gtag\s*\(/);
  assert.doesNotMatch(dealSrc, /['"]deal_submission['"]/);
});

test('gtag.js is not requested off the production hosts', () => {
  const blocked = [
    'localhost',
    '127.0.0.1',
    '',
    'assemble-capital.vercel.app',
    'assemble-capital-git-ga4-oliver.vercel.app',
    'assemble.capital.evil.com',
    'preview.assemble.capital',
    'www.assemble.capital.cdn.cloudflare.net',
  ];
  for (const host of blocked) {
    const sandbox = createSandbox(host);
    assert.equal(sandbox.scripts.length, 0, host);
    assert.equal(sandbox.gtag, undefined, host);
    assert.equal(sandbox.assembleGaEnabled, false, host);
    sandbox.assembleTrack('generate_lead', { form_name: 'investor_network', email: 'a@b.co' });
    click(sandbox, 'tel:+13107041794');
    click(sandbox, 'mailto:info@assemble.capital');
    assert.equal(sandbox.dataLayer, undefined, host);
  }
});

test('production hosts load gtag.js exactly once', () => {
  for (const host of ['assemble.capital', 'www.assemble.capital', 'ASSEMBLE.CAPITAL', 'assemble.capital.']) {
    const sandbox = createSandbox(host);
    assert.equal(sandbox.assembleGaEnabled, true, host);
    assert.equal(sandbox.scripts.length, 1, host);
    assert.equal(sandbox.scripts[0].src, GTAG_SRC, host);
    assert.equal(sandbox.scripts[0].async, true, host);
    const configs = pushed(sandbox.dataLayer).filter((row) => row[0] === 'config');
    assert.deepEqual(configs, [['config', MEASUREMENT_ID]], host);
    vm.runInNewContext(analyticsSrc, sandbox, { filename: 'js/analytics.js' });
    assert.equal(sandbox.scripts.length, 1, host + ' second init');
    assert.equal(pushed(sandbox.dataLayer).filter((row) => row[0] === 'config').length, 1, host);
  }
});

test('click events fire once per activation and carry no phone or email', () => {
  const sandbox = createSandbox('assemble.capital');
  click(sandbox, 'tel:+13107041794', true);
  click(sandbox, 'mailto:oliver@assemble.capital');
  click(sandbox, 'mailto:oliver@assemble.capital');
  click(sandbox, '/contact.html');
  const names = events(sandbox).map((row) => row[1]);
  assert.deepEqual(names, ['click_to_call', 'click_to_email', 'click_to_email']);
  const encoded = JSON.stringify(events(sandbox));
  assert.equal(encoded.includes('310'), false);
  assert.equal(encoded.includes('oliver@'), false);
  assert.equal(encoded.includes('mailto:'), false);
  assert.equal(encoded.includes('tel:'), false);
});

test('assembleTrack drops contact fields and sensitive values', () => {
  const sandbox = createSandbox('www.assemble.capital');
  sandbox.assembleTrack('generate_lead', {
    form_name: 'investor_network',
    email: 'investor@example.com',
    phone: '3105550100',
    name: 'Pat Example',
    message: 'I want to invest $250,000',
    accredited: 'Yes',
    range: '$250,000 – $500,000',
    role: 'Owner',
    note: 'call 310-704-1794',
  });
  assert.deepEqual(events(sandbox), [[
    'event',
    'generate_lead',
    { form_name: 'investor_network' },
  ]]);
});

function investorForm(valid) {
  const form = {
    dataset: {},
    valid,
    values: {
      first: 'Pat',
      last: 'Example',
      email: 'investor@example.com',
      phone: '(310) 555-0100',
      accredited: 'Yes',
      range: '$250,000 – $500,000',
      message: 'Looking at the Culver City offering',
    },
    multi: { interest: ['SB 684 / SB 1123'] },
    checkValidity() { return this.valid; },
    addEventListener(type, fn) { this.handlers = this.handlers || {}; this.handlers[type] = fn; },
  };
  return form;
}

function loadInvestor(form) {
  const sandbox = createSandbox('assemble.capital', {
    querySelector(sel) {
      return sel === 'form.inquiry:not(.deal-form)' ? form : null;
    },
    FormData: function FormData(target) {
      this.get = (key) => {
        const value = target.values[key];
        return value == null || value === '' ? null : value;
      };
      this.getAll = (key) => target.multi[key] || [];
    },
  });
  vm.runInNewContext(mainSrc, sandbox, { filename: 'js/main.js' });
  return sandbox;
}

test('investor generate_lead fires once, only after the form is valid', () => {
  const form = investorForm(false);
  const sandbox = loadInvestor(form);
  assert.equal(events(sandbox).length, 0);

  form.handlers.submit({ preventDefault() {} });
  assert.equal(events(sandbox).length, 0);
  assert.match(sandbox.location.href, /^mailto:info@assemble\.capital/);

  form.valid = true;
  form.handlers.submit({ preventDefault() {} });
  form.handlers.submit({ preventDefault() {} });
  assert.deepEqual(events(sandbox), [[
    'event',
    'generate_lead',
    { form_name: 'investor_network' },
  ]]);
  const encoded = JSON.stringify(sandbox.dataLayer);
  assert.equal(encoded.includes('investor@example.com'), false);
  assert.equal(encoded.includes('555-0100'), false);
  assert.equal(encoded.includes('Culver'), false);
  assert.equal(encoded.includes('250,000'), false);
  assert.equal(encoded.includes('Yes'), false);
});

function dealForm(overrides = {}) {
  const status = { textContent: '', classList: { toggle() {} } };
  const button = { disabled: false };
  const consent = { checked: overrides.consent !== false };
  const fileInput = { files: overrides.files || [] };
  const form = {
    dataset: {},
    website: { value: overrides.website || '' },
    values: {
      role: 'Owner',
      name: 'Pat Example',
      company: 'Example Co',
      email: 'pat@example.com',
      phone: '3105550100',
      address: '1 Main St, Los Angeles',
      asking_price: '$2,980,000',
      lot_size: '6000',
      zoning: 'R2',
      property_type: 'Single-family home',
      occupancy: 'Vacant',
      deal_status: 'Off-market',
      notes: 'Tenant lease ends in June',
      ...overrides.values,
    },
    status,
    button,
    resetCalled: false,
    querySelector(sel) {
      if (sel === '.form-status') return status;
      if (sel === 'button[type="submit"]') return button;
      if (sel === 'input[name="consent"]') return consent;
      if (sel === 'input[type="file"]') return fileInput;
      return null;
    },
    addEventListener(type, fn) { this.handlers = this.handlers || {}; this.handlers[type] = fn; },
    reset() { this.resetCalled = true; },
  };
  return form;
}

function loadDeal(form, extras = {}) {
  let extra = 0;
  const NativeDate = Date;
  class Clock extends NativeDate {
    static now() { return NativeDate.now() + extra; }
  }
  const sandbox = createSandbox('assemble.capital', {
    Date: Clock,
    querySelector(sel) {
      return sel === 'form.deal-form' ? form : null;
    },
    FormData: function FormData(target) {
      this.get = (key) => target.values[key] ?? '';
    },
    fetch: extras.fetch,
    crypto: extras.crypto || { randomUUID: () => 'deal-id' },
  });
  sandbox.advance = (ms) => { extra = ms; };
  const source = extras.source || dealSrc;
  vm.runInNewContext(source, sandbox, { filename: 'js/submit-deal.js' });
  return sandbox;
}

test('deal generate_lead fires once on the mailto success path and not on failure', () => {
  const form = dealForm();
  const sandbox = loadDeal(form);
  const before = sandbox.location.href;

  form.values.name = '';
  sandbox.advance(5000);
  form.handlers.submit({ preventDefault() {} });
  assert.equal(events(sandbox).length, 0);
  assert.equal(sandbox.location.href, before);
  assert.match(form.status.textContent, /name, email, phone/);

  form.values.name = 'Pat Example';
  form.website.value = 'https://spam.test';
  form.handlers.submit({ preventDefault() {} });
  assert.equal(events(sandbox).length, 0);
  assert.equal(sandbox.location.href, before);

  form.website.value = '';
  sandbox.advance(0);
  form.handlers.submit({ preventDefault() {} });
  assert.equal(events(sandbox).length, 0, 'instant submit is dropped');

  sandbox.advance(5000);
  form.handlers.submit({ preventDefault() {} });
  form.handlers.submit({ preventDefault() {} });
  assert.deepEqual(events(sandbox), [[
    'event',
    'generate_lead',
    { form_name: 'submit_a_deal' },
  ]]);
  assert.match(sandbox.location.href, /^mailto:info@assemble\.capital/);
  const encoded = JSON.stringify(pushed(sandbox.dataLayer));
  for (const secret of ['pat@example.com', '3105550100', '1 Main St', '2,980,000', 'Tenant lease', 'Owner', 'Example Co']) {
    assert.equal(encoded.includes(secret), false, secret);
  }
});

test('deal generate_lead fires once after a live insert and not when the insert fails', async () => {
  const liveSrc = dealSrc
    .replace("SUPABASE_URL: '',", "SUPABASE_URL: 'https://example.test',")
    .replace("SUPABASE_KEY: '',", "SUPABASE_KEY: 'anon-test-key',");
  let fetchCalls = 0;
  let release;
  const pending = new Promise((resolve) => { release = resolve; });
  const form = dealForm();
  const sandbox = loadDeal(form, {
    source: liveSrc,
    fetch() {
      fetchCalls += 1;
      return pending;
    },
  });
  sandbox.advance(5000);
  const first = form.handlers.submit({ preventDefault() {} });
  const second = form.handlers.submit({ preventDefault() {} });
  assert.equal(fetchCalls, 1);
  assert.equal(form.button.disabled, true);
  release({ ok: true });
  await first;
  await second;
  assert.equal(form.resetCalled, true);
  assert.deepEqual(events(sandbox), [[
    'event',
    'generate_lead',
    { form_name: 'submit_a_deal' },
  ]]);
  assert.equal(JSON.stringify(pushed(sandbox.dataLayer)).includes('pat@example.com'), false);

  const failed = dealForm();
  const failure = loadDeal(failed, {
    source: liveSrc,
    fetch() { return Promise.resolve({ ok: false }); },
  });
  failure.advance(5000);
  await failed.handlers.submit({ preventDefault() {} });
  assert.equal(events(failure).length, 0);
  assert.equal(failed.resetCalled, false);
  assert.equal(failed.button.disabled, false);
  assert.match(failed.status.textContent, /Something went wrong/);
});
