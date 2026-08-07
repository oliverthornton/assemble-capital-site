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
  homepage strategy cards. Regenerate with `python3 tools-generate-strategy-pages.py`.
- `properties/*.html` — 18 individual property pages (13 single family, 4 multifamily,
  1 tenancy-in-common). Each has a hero, headline stats, investment background, photo
  gallery with lightbox, project + equity return tables, an investment-cycle timeline,
  a takeaway, an invest-with-us CTA, and prev/next navigation. Linked from the track
  record cards and the homepage signature-exit cards.
  Gallery photos live in `assets/img/properties/<slug>/`.
  To regenerate: edit the data block in the generator and re-run it (see Notes below).
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

## Notes
- Property pages are generated from `tools-generate-property-pages.py` — all copy and
  financials live in the `P` list at the top. Edit there, then run:
  `python3 tools-generate-property-pages.py`. It rewrites every file in `properties/`.
- Gallery images are built separately; drop new photos into
  `assets/img/properties/<slug>/` named `01.jpg`, `02.jpg`, … and re-run the generator
  (it reads whatever is in the folder).
- The footer is generated for every page by `tools-rebuild-footer.py` — edit it there and
  re-run to update all 31 pages at once. The property and strategy generators import from
  it, so footers stay in sync.

## Open items
- **Facebook link**: no Facebook page was found on the current site. The footer button is
  written but commented out — set `FACEBOOK` in `tools-rebuild-footer.py` and re-run to
  enable it.
- **Blog**: footer "Insights" links point at the live Squarespace blog
  (assemble.capital/assemble-capital-blogs). If this site replaces that domain, the blog
  needs to move too — either onto a subdomain or rebuilt into this site — and those links
  updated in `tools-rebuild-footer.py`.
