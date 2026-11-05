# Assemble Capital — Website

Static multi-page site for assemble.capital, rebuilt July 2026.

## Pages
- `index.html` — Home (hero, track-record stats, strategies, signature exits, active portfolio, CTA)
- `about.html` — Firm narrative, principals, affiliated platform, alignment & governance
- `strategies.html` — Four strategies, institutional buy box, IC process, kill criteria, risk framework
- `portfolio.html` — Current Projects (AC I–VII)
- `track-record.html` — Realized returns, refi/hold executions, benchmark, completed SF + MF galleries
- `contact.html` — Contact info, principals, inquiry form (opens pre-filled email to info@assemble.capital)
- `strategies/*.html` — 4 strategy detail pages (luxury redevelopment, boutique
  multifamily, fee-simple infill subdivisions, TIC housing). Each has underwriting
  targets, an extended investment-reasoning section, four dependency pillars, current
  projects split into In Entitlements / In Construction / Completed, strategy-specific
  risks, and a contact CTA. Linked from the strategy blocks on `strategies.html` and the
  homepage strategy cards. Edit the HTML directly (the old generator is out of date; see Site scripts).
- `properties/*.html` — 18 individual property pages (13 single family, 4 multifamily,
  1 tenancy-in-common). Each has a hero, headline stats, investment background, photo
  gallery with lightbox, project + equity return tables, an investment-cycle timeline,
  a takeaway, an invest-with-us CTA, and prev/next navigation. Linked from the track
  record cards and the homepage signature-exit cards.
  Gallery photos live in `assets/img/properties/<slug>/`.
  Edit the HTML directly (the old generator is out of date; see Site scripts).
- `terms.html`, `privacy.html`, `disclosures.html` — Legal pages (Terms of Service, Privacy
  Policy, Risks & Disclosures), linked from every footer. **DRAFTS — must be reviewed by
  qualified securities/privacy counsel before the site goes live.** Each file carries an
  HTML comment noting this.

## Brand system (from Assemble Capital Brand Kit)
- Colors: Cod Gray `#140f0f`, Alabaster `#f8f8f8`; bronze accent `#8f7351`
- Type: Cormorant Garamond (display, stand-in for the logo serif), Archivo (body/UI, stand-in for
  Roc Grotesque), Special Elite (brand typewriter accent — eyebrows, data labels, stamps)
  — loaded from Google Fonts. If you have Roc Grotesque licensed webfonts, swap them in
  `css/style.css` (`--sans`).

## Content sources
- AC — Track Record & Realized Returns (Jul 2026)
- Assemble Capital Institutional Overview (Jul 2026)
- Photography pulled from the previous assemble.capital site (assets/img/*.webp)

## Preview locally
    cd assemble-capital-site && python3 -m http.server 4173
    # open http://localhost:4173

## Deploy
Any static host (Netlify, Vercel, Cloudflare Pages, S3) — no build step. Point the
assemble.capital DNS at the host. The contact form is mailto-based; wire it to a form
service (Formspree, Basin, or the CRM) before launch if you want submissions captured
server-side.

## Site scripts

The live HTML files are the source of truth. Many pages were improved by hand after the
original generators were written, so those generators are now locked: they stop with a
message instead of running. Edit those pages directly in their HTML.

**Safe to run**
- `tools-new-blog-post.py blog/drafts/<slug>` adds a new Learning Center article. It copies a
  current live article's page shell, then updates only the new page, the Learning Center
  index, `blog/posts.json`, `sitemap.xml` and the post's share card. It builds everything in
  a temporary copy first and stops without changing anything if a check fails. Add
  `--dry-run` to see what would change. How to write a draft: `blog/README.md`.
- `tools-build-blog-index.py` rebuilds the Learning Center index from the article pages.
- `tools-add-analytics.py`, `tools-build-project-pages.py`, `tools-build-lenders-page.py`
  (no changes when run against the current site).
- `tools-generate-share-cards.py` only through `tools-new-blog-post.py` (a full run
  re-renders every share card).

**Locked (out of date; would overwrite live pages)**
- `tools-generate-blog-pages.py`: rebuilds every article from old copies in `posts.json`.
- `tools-rebuild-footer.py`: older footer design, rewrites every page.
- `tools-apply-seo-metadata.py`: older titles, descriptions and share images on ~30 pages.
- `tools-generate-strategy-pages.py`, `tools-generate-property-pages.py`: hand edits since,
  and both run `tools-apply-seo-metadata.py`.
- `tools-generate-sitemap.py`: resets every lastmod date.

They run only with `--overwrite-live-pages`. Don't use that unless the script has first
been brought up to date with the live pages; check the result with `git diff`.

- Gallery photos live in `assets/img/properties/<slug>/` named `01.jpg`, `02.jpg`, ….
