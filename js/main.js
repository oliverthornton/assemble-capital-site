// Assemble Capital — shared behaviors

// Header: transparent over hero, solid after scroll
const head = document.querySelector('.site-head');
if (head && !head.classList.contains('always-solid')) {
  const onScroll = () => head.classList.toggle('solid', window.scrollY > 40);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

// Mobile menu
const menuBtn = document.querySelector('.menu-btn');
const nav = document.querySelector('.site-nav');
if (menuBtn && nav) {
  menuBtn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuBtn.textContent = open ? 'Close' : 'Menu';
    menuBtn.setAttribute('aria-expanded', open);
  });
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

// Contact form → composes an email to the firm
const form = document.querySelector('form.inquiry');
if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const d = new FormData(form);
    const subject = encodeURIComponent('Investment network inquiry — ' + d.get('first') + ' ' + d.get('last'));
    const body = encodeURIComponent(
      'Name: ' + d.get('first') + ' ' + d.get('last') +
      '\nEmail: ' + d.get('email') +
      '\nPhone: ' + d.get('phone') +
      '\nAccredited investor: ' + d.get('accredited') +
      '\n\n' + (d.get('message') || '')
    );
    window.location.href = 'mailto:info@assemble.capital?subject=' + subject + '&body=' + body;
  });
}
