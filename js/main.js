// Assemble Capital — shared behaviors

// Header: transparent over hero, solid after scroll
const head = document.querySelector('.site-head');
if (head && !head.classList.contains('always-solid')) {
  const onScroll = () => head.classList.toggle('solid', window.scrollY > 40);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

// Primary navigation: full-screen menu on small screens, grouped dropdowns everywhere
const menuBtn = document.querySelector('.menu-btn');
const nav = document.querySelector('.site-nav');
if (menuBtn && nav) {
  const groups = Array.from(nav.querySelectorAll('.nav-dd'));
  const closeGroups = (except) => groups.forEach((g) => {
    if (g === except) return;
    g.classList.remove('open');
    const t = g.querySelector('.nav-dd-toggle'); if (t) t.setAttribute('aria-expanded', 'false');
  });
  const setOpen = (open) => {
    nav.classList.toggle('open', open);
    document.body.classList.toggle('nav-locked', open);
    menuBtn.textContent = open ? 'Close' : 'Menu';
    menuBtn.setAttribute('aria-expanded', open);
    if (!open) closeGroups();
  };
  menuBtn.addEventListener('click', () => setOpen(!nav.classList.contains('open')));
  groups.forEach((g) => {
    const t = g.querySelector('.nav-dd-toggle');
    if (!t) return;
    t.addEventListener('click', () => {
      const open = !g.classList.contains('open');
      closeGroups(g);
      g.classList.toggle('open', open);
      t.setAttribute('aria-expanded', open);
    });
  });
  // Following a link (including in-page anchors) closes the menu
  nav.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => setOpen(false)));
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    if (nav.classList.contains('open')) setOpen(false); else closeGroups();
  });
  document.addEventListener('click', (e) => { if (!nav.contains(e.target) && !nav.classList.contains('open')) closeGroups(); });
}

// Scroll reveals — with fallbacks so content can never stay hidden
const reveals = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  reveals.forEach((el) => io.observe(el));
  // Safety net: reveal anything already on screen shortly after load
  setTimeout(() => {
    reveals.forEach((el) => {
      if (!el.classList.contains('in') && el.getBoundingClientRect().top < window.innerHeight) {
        el.classList.add('in');
      }
    });
  }, 900);
} else {
  reveals.forEach((el) => el.classList.add('in'));
}

// Project carousel
document.querySelectorAll('[data-carousel]').forEach((carousel) => {
  const slides = carousel.querySelectorAll('.slide');
  const count = carousel.querySelector('.c-count');
  const prev = carousel.querySelector('.c-prev');
  const next = carousel.querySelector('.c-next');
  if (!slides.length) return;
  let i = 0;
  let timer = null;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const show = (n) => {
    i = (n + slides.length) % slides.length;
    slides.forEach((s, k) => s.classList.toggle('is-active', k === i));
    if (count) count.textContent = String(i + 1).padStart(2, '0') + ' / ' + String(slides.length).padStart(2, '0');
  };
  const stop = () => { if (timer) { clearInterval(timer); timer = null; } };
  const start = () => { if (!reduced && !timer) timer = setInterval(() => show(i + 1), 6000); };

  prev?.addEventListener('click', () => { stop(); show(i - 1); start(); });
  next?.addEventListener('click', () => { stop(); show(i + 1); start(); });
  carousel.addEventListener('mouseenter', stop);
  carousel.addEventListener('mouseleave', start);
  carousel.addEventListener('focusin', stop);
  carousel.addEventListener('focusout', start);

  // basic swipe support
  let x0 = null;
  carousel.addEventListener('pointerdown', (e) => { x0 = e.clientX; }, { passive: true });
  carousel.addEventListener('pointerup', (e) => {
    if (x0 === null) return;
    const dx = e.clientX - x0;
    if (Math.abs(dx) > 45) { stop(); show(i + (dx < 0 ? 1 : -1)); start(); }
    x0 = null;
  }, { passive: true });

  show(0);
  start();
});

// Property gallery lightbox
(() => {
  const gallery = document.querySelector('.gallery');
  const box = document.querySelector('.lightbox');
  if (!gallery || !box) return;
  // grid shows thumbnails; the lightbox loads the full-size image
  const shots = [...gallery.querySelectorAll('button')].map((b) => {
    const img = b.querySelector('img');
    return { src: b.dataset.full || img.src, alt: img.alt };
  });
  const view = box.querySelector('img');
  const count = box.querySelector('.lb-count');
  let i = 0;
  let lastFocus = null;

  const render = () => {
    view.src = shots[i].src;
    view.alt = shots[i].alt;
    if (count) count.textContent = String(i + 1).padStart(2, '0') + ' / ' + String(shots.length).padStart(2, '0');
  };
  const open = (n) => {
    lastFocus = document.activeElement;
    i = n; render();
    box.classList.add('open');
    document.body.style.overflow = 'hidden';
    box.querySelector('.lb-close').focus();
  };
  const close = () => {
    box.classList.remove('open');
    document.body.style.overflow = '';
    lastFocus?.focus();
  };
  const step = (d) => { i = (i + d + shots.length) % shots.length; render(); };

  gallery.querySelectorAll('button').forEach((b, n) => b.addEventListener('click', () => open(n)));
  box.querySelector('.lb-close').addEventListener('click', close);
  box.querySelector('.lb-prev').addEventListener('click', () => step(-1));
  box.querySelector('.lb-next').addEventListener('click', () => step(1));
  box.addEventListener('click', (e) => { if (e.target === box) close(); });
  document.addEventListener('keydown', (e) => {
    if (!box.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') step(-1);
    if (e.key === 'ArrowRight') step(1);
  });
})();

// Investor intake: scheduling link + Cash Flow Portal form.
// Fill these in once the scheduler and the CFP lead-capture form exist; until then
// "Schedule an intro call" links fall back to the contact form and the email form stays.
const INTAKE = {
  SCHEDULER_URL: '',   // e.g. a Calendly or Cash Flow Portal booking link
  CFP_FORM_URL: '',    // Cash Flow Portal lead-capture form (embedded in an iframe)
  CFP_FORM_HEIGHT: 980,
};

(function () {
  const track = (name, params) => { if (window.gtag) window.gtag('event', name, params || {}); };

  document.querySelectorAll('[data-schedule]').forEach((a) => {
    if (INTAKE.SCHEDULER_URL) {
      a.href = INTAKE.SCHEDULER_URL;
      a.target = '_blank';
      a.rel = 'noopener';
    }
    a.addEventListener('click', () => track('schedule_call_click', { page: location.pathname }));
  });
  if (INTAKE.SCHEDULER_URL) document.querySelectorAll('[data-schedule-only]').forEach((el) => { el.style.display = ''; });

  if (INTAKE.CFP_FORM_URL) {
    document.querySelectorAll('[data-cfp-embed]').forEach((box) => {
      const f = document.createElement('iframe');
      f.src = INTAKE.CFP_FORM_URL;
      f.title = 'Join the Assemble Capital investor network';
      f.loading = 'lazy';
      f.style.cssText = 'width:100%;border:0;min-height:' + INTAKE.CFP_FORM_HEIGHT + 'px;background:transparent';
      box.replaceChildren(f);
    });
  }

  // Fallback: the inquiry form composes an email to the firm
  const form = document.querySelector('form.inquiry:not(.deal-form)');
  if (!form) return;
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const d = new FormData(form);
    const v = (k) => d.get(k) || 'Not specified';
    const subject = encodeURIComponent('Investor network — ' + d.get('first') + ' ' + d.get('last'));
    const body = encodeURIComponent(
      'Name: ' + d.get('first') + ' ' + d.get('last') +
      '\nEmail: ' + d.get('email') +
      '\nPhone: ' + d.get('phone') +
      '\nAccredited investor: ' + v('accredited') +
      '\nStrategies of interest: ' + (d.getAll('interest').join(', ') || 'Not specified') +
      '\nTypical investment size: ' + v('range') +
      '\nPrivate real estate experience: ' + v('experience') +
      '\nHow they heard about us: ' + v('heard') +
      (d.get('referred') ? '\nReferred by: ' + d.get('referred') : '') +
      '\n\n' + (d.get('message') || '')
    );
    track('generate_lead', { form: 'investor_network' });
    window.location.href = 'mailto:info@assemble.capital?subject=' + subject + '&body=' + body;
  });
})();

// FAQ topic nav — highlight the topic in view
(function () {
  var nav = document.querySelector('.faq2-nav'); if (!nav || !('IntersectionObserver' in window)) return;
  var links = Array.prototype.slice.call(nav.querySelectorAll('a'));
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) links.forEach(function (l) { l.classList.toggle('on', l.getAttribute('href') === '#' + e.target.id); });
    });
  }, { rootMargin: '-30% 0px -60% 0px' });
  document.querySelectorAll('.faq2-group').forEach(function (g) { io.observe(g); });
})();

// Blog index: collapse long topic sections behind "Show all"
(function () {
  const btns = document.querySelectorAll('[data-more]');
  if (!btns.length) return;
  document.documentElement.classList.add('js-topics');
  btns.forEach((b) => {
    const grid = b.previousElementSibling;
    const label = b.textContent;
    b.addEventListener('click', () => {
      const open = grid.classList.toggle('expanded');
      b.textContent = open ? 'Show fewer' : label;
      if (!open) grid.closest('section').scrollIntoView({ behavior: 'smooth' });
    });
  });
})();
