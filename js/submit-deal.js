// Submit-a-Deal form → Supabase (table + private photo bucket).
// Until SUPABASE_URL and SUPABASE_KEY are set, it falls back to a pre-filled email.
// The key is the project's publishable (anon) key: row-level security only lets it
// insert submissions and upload files, never read them back.
(function () {
  const CONFIG = {
    SUPABASE_URL: '',              // e.g. https://<ref>.supabase.co
    SUPABASE_KEY: '',              // publishable / anon key
    TABLE: 'deal_submissions',
    BUCKET: 'deal-files',
    FALLBACK_EMAIL: 'info@assemble.capital',
    MAX_FILES: 10,
    MAX_BYTES: 10 * 1024 * 1024,
  };

  const form = document.querySelector('form.deal-form');
  if (!form) return;
  const status = form.querySelector('.form-status');
  const button = form.querySelector('button[type="submit"]');
  const startedAt = Date.now();
  const live = Boolean(CONFIG.SUPABASE_URL && CONFIG.SUPABASE_KEY);

  const say = (msg, isError) => {
    status.textContent = msg;
    status.classList.toggle('is-error', Boolean(isError));
  };

  const FIELDS = ['role', 'name', 'company', 'email', 'phone', 'address', 'asking_price',
                  'lot_size', 'zoning', 'property_type', 'occupancy', 'deal_status', 'notes'];

  function collect() {
    const d = new FormData(form);
    const row = {};
    FIELDS.forEach((k) => { row[k] = (d.get(k) || '').toString().trim(); });
    return row;
  }

  function validate(row, files) {
    if (!row.role) return 'Please tell us your role.';
    if (!row.name || !row.email || !row.phone || !row.address) return 'Please fill in your name, email, phone, and the property address.';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(row.email)) return 'Please check your email address.';
    if (!form.querySelector('input[name="consent"]').checked) return 'Please confirm you’re authorized to share this property.';
    if (files.length > CONFIG.MAX_FILES) return 'Please attach no more than ' + CONFIG.MAX_FILES + ' files.';
    const big = files.find((f) => f.size > CONFIG.MAX_BYTES);
    if (big) return big.name + ' is larger than 10 MB.';
    return '';
  }

  function mailtoFallback(row, files) {
    const lines = [
      'Role: ' + row.role, 'Name: ' + row.name, 'Company: ' + row.company,
      'Email: ' + row.email, 'Phone: ' + row.phone, '',
      'Property: ' + row.address, 'Asking price: ' + row.asking_price,
      'Lot size (SF): ' + row.lot_size, 'Zoning: ' + row.zoning,
      'Type: ' + row.property_type, 'Occupancy: ' + row.occupancy, 'Status: ' + row.deal_status,
      '', row.notes,
    ];
    if (files.length) lines.push('', '(Please attach the ' + files.length + ' file(s) to this email before sending.)');
    const subject = encodeURIComponent('Deal submission — ' + row.address);
    window.location.href = 'mailto:' + CONFIG.FALLBACK_EMAIL + '?subject=' + subject + '&body=' + encodeURIComponent(lines.join('\n'));
    say('Your email app should open with the details filled in. Attach any photos, then send.');
  }

  const headers = (extra) => Object.assign({
    apikey: CONFIG.SUPABASE_KEY,
    Authorization: 'Bearer ' + CONFIG.SUPABASE_KEY,
  }, extra || {});

  async function upload(id, file, i) {
    const safe = file.name.replace(/[^\w.\-]+/g, '_').slice(-80);
    const path = id + '/' + String(i + 1).padStart(2, '0') + '-' + safe;
    const res = await fetch(CONFIG.SUPABASE_URL + '/storage/v1/object/' + CONFIG.BUCKET + '/' + path, {
      method: 'POST',
      headers: headers({ 'Content-Type': file.type || 'application/octet-stream', 'x-upsert': 'false' }),
      body: file,
    });
    if (!res.ok) throw new Error('upload');
    return path;
  }

  async function submitLive(row, files) {
    const id = (crypto.randomUUID && crypto.randomUUID()) || String(Date.now()) + Math.random().toString(16).slice(2);
    const paths = [];
    for (let i = 0; i < files.length; i++) paths.push(await upload(id, files[i], i));
    const res = await fetch(CONFIG.SUPABASE_URL + '/rest/v1/' + CONFIG.TABLE, {
      method: 'POST',
      headers: headers({ 'Content-Type': 'application/json', Prefer: 'return=minimal' }),
      body: JSON.stringify(Object.assign({ id: id, file_paths: paths, page: location.pathname }, row)),
    });
    if (!res.ok) throw new Error('insert');
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const row = collect();
    const files = Array.from(form.querySelector('input[type="file"]').files || []);
    const problem = validate(row, files);
    if (problem) { say(problem, true); return; }

    // Bots fill the hidden field or submit a complete form instantly; quietly accept and drop.
    if (form.website && form.website.value) { say('Thank you. We’ll be in touch.'); return; }
    if (Date.now() - startedAt < 3000) { say('Thank you. We’ll be in touch.'); return; }

    if (!live) { mailtoFallback(row, files); return; }

    button.disabled = true;
    say(files.length ? 'Uploading ' + files.length + ' file(s)…' : 'Sending…');
    try {
      await submitLive(row, files);
      form.reset();
      say('Thank you. We received your property and will reply within two business days.');
      if (window.gtag) window.gtag('event', 'deal_submission', { role: row.role });
    } catch (err) {
      say('Something went wrong sending your submission. Please email it to ' + CONFIG.FALLBACK_EMAIL + ' or call (310) 704-1794.', true);
    } finally {
      button.disabled = false;
    }
  });
})();
