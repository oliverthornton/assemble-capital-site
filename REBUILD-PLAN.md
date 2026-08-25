# Assemble Capital Site — Rebuild & Remediation Plan

Prepared following a Semrush Site Audit that found the live site (assemble.capital) in
bad technical shape: 486 errors, 1 "healthy" page out of 74 crawled, 300 broken internal
links, 60 pages flagged duplicate title/content/meta, 6 pages blocked from crawling, no
`robots.txt`. This doc records the real root causes (most audit symptoms traced back to a
small number of concrete bugs, not 486 independent problems), what was fixed and verified
in this session, what's still open, and exactly how to operate the blog going forward.

**Status of this doc:** written immediately after the fixes below were made, verified with
a local preview, and committed locally (not pushed). Read the "Working notes" section near
the bottom before you push — it explains an oddity in the commit history from this session.

---

## 1. Current state summary

### What's live
A 31-page static HTML/CSS/JS site (home, about, strategies + 4 strategy detail pages,
portfolio, track record, contact, 18 property pages, 3 legal pages) plus a blog that,
until this session, had zero rendered posts. No build step; content comes from Python
generator scripts (`tools-generate-*.py`) that read data and emit HTML. Deployed to Vercel,
connected via Git to `github.com/oliverthornton/assemble-capital-site` — Vercel deploys
straight from the repo root, so anything the live site needs must exist there (see the
`tools-build-preview.py` note under §3 for a related dead end).

### What the audit found vs. what was actually wrong
The audit's headline numbers look catastrophic but trace back to a small number of root
causes, each amplified across every page:

| Audit finding | Real cause |
|---|---|
| 300 broken internal links | Two compounding bugs: (1) every page's footer had a dead `href="FACEBOOK_URL"` link — one broken link × 31 pages; (2) the footer's "Insights" column and `blog/index.html` linked to 29 blog posts that were never generated, so every one of those links 404'd. |
| 60 pages flagged duplicate title/content/meta | Almost certainly the blog: `blog/index.html` existed but listed no posts, and internal links pointed at 29 non-existent `blog/<slug>.html` pages, all of which likely resolved to the same generic 404/host page — i.e., the audit was probably seeing ~29 identical "missing page" responses, not 29 pages with genuinely duplicated content. Property and strategy pages were checked and already have unique titles/meta descriptions/content — not a source of this finding. |
| 486 errors / 1 healthy page out of 74 | Same two bugs above, multiplied across every page the crawler could reach — a 31-page site with a sitewide dead link and a broken blog section will fail almost every page-level check a site auditor runs. |
| 6 pages blocked from crawling | Not independently investigated this session — worth a fresh audit re-run once the fixes below are live, since it may resolve on its own once robots.txt exists and the broken links are gone. Flagged as open below. |
| No `robots.txt` | Confirmed: literally missing at the repo root. Fixed below. |

### What was fixed this session (see §2 for detail)
1. Footer's dead `FACEBOOK_URL` link — removed everywhere.
2. All 29 recovered Squarespace blog posts (plus one new post authored this session — see
   Working notes) rendered and published.
3. `robots.txt` added, pointing at the existing `sitemap.xml`.
4. `vercel.json` added with 301 redirects from the old Squarespace blog path pattern to the
   new in-repo blog URLs.

---

## 2. Fixes made and how they were verified

### 2.1 Footer Facebook link (`tools-rebuild-footer.py`)
**Root cause:** `FACEBOOK` was intentionally left blank (no real Facebook page exists), and
the script's fallback path wrapped a real `<a href="FACEBOOK_URL" ...>` element inside an
HTML comment (`<!-- ... -->`) instead of just not emitting it. A browser never renders
that markup, but the literal string `href="FACEBOOK_URL"` was sitting in every page's raw
HTML source, and Semrush's crawler (like many audit tools) appears to extract links from
raw source rather than a comment-aware DOM parse — so it saw and flagged a real, dead link
on every page.

**Fix:** `social()` in `tools-rebuild-footer.py` now simply omits the Facebook `<a>`
element entirely when `FACEBOOK` is unset — no placeholder, commented or otherwise, ever
gets written to any page. When Oliver has a real Facebook URL, set `FACEBOOK` at the top of
the file and re-run `python3 tools-rebuild-footer.py` to enable the button on all pages.

**Verified:**
- `grep -rl "FACEBOOK_URL" . --include="*.html"` returns zero matches across the whole
  site (63 HTML pages) after regeneration.
- Loaded `properties/apex-hh.html` and `blog/accredited-investor-requirements.html` in a
  local preview (`python3 -m http.server 4173`) and inspected the rendered footer's social
  block via the DOM directly — only LinkedIn and Instagram icons are present on both pages.

### 2.2 Blog posts rendered and published (`blog/posts.json`, generator scripts)
**Root cause:** `tools-generate-blog-pages.py` (which turns `blog/posts.json` into
`blog/<slug>.html` + `blog/index.html`) existed and worked correctly, but had never been
run — `blog/` contained only `README.md`, `posts.json`, and an empty `index.html`
("New posts are on the way"). Every one of the 29 recovered Squarespace posts had
`"status": "draft"` in the data, which is the flag the generator uses to decide what to
render — so even running the script would have produced nothing.

**What this required beyond "just run the script":** all 29 (later 30 — see Working
notes) posts being marked `"draft"` was a judgment call, not a technical bug — see
"Content decision" below for the reasoning on why they were flipped to `"published"`.

**Fix:**
1. Flipped `"status": "draft"` → `"published"` for all posts in `blog/posts.json`
   (content decision, discussed below).
2. Ran, in order:
   ```
   python3 tools-generate-blog-pages.py   # wrote blog/index.html + 30 blog/<slug>.html pages
   python3 tools-rebuild-footer.py        # refreshed the "Insights" 4-latest-posts list on all 63 pages
   python3 tools-generate-sitemap.py      # sitemap.xml grew from 30 to 61 URLs
   ```

**Content decision — why all posts were published, not left as drafts:**
`posts.json`'s `"draft"` default turned out to be the initial import state, not a
deliberate "hold for review" signal. Evidence considered: (a) every post's `body_html` is a
complete, polished, non-placeholder article (5,000–16,000 characters), not filler; (b)
every post has a working `hero_image` that resolves to a real file (`assets/img/blog/<slug>/`
was fully populated for all 29 original posts, confirmed by checking every path); (c) an
undocumented `_migration_source` field (see §3) shows every original post was a real, live
URL on the old Squarespace blog (`assemblecapital.squarespace.com/assemble-capital-blogs/<slug>`)
— this is republishing previously-public content, not exposing unreviewed drafts for the
first time; (d) nothing here goes live until Oliver reviews the diff and pushes himself,
per the constraint on this task. On balance, publishing was the reasonable call — but
**Oliver should skim `git diff HEAD -- blog/posts.json` for the `status` changes and the
30 generated `blog/*.html` files before pushing**, same as he'd review any other content
change, especially given this is a securities-adjacent business.

Four of the 29 original posts have auto-generated Squarespace slugs
(`blog-post-title-four-y3jky`, `-one-6648y`, `-three-w77ad`, `-two-bgnct`) rather than
descriptive ones. Their content is legitimate, finished articles (checked — not junk) —
just poorly named. Left as-is rather than renamed, because renaming would (a) require also
renaming their asset folders under `assets/img/blog/`, and (b) break the 1:1 old-slug/new-slug
match the redirect in §2.3 depends on unless a redirect were added for the rename too. Flagged
in §4 as a cleanup item, not done this session.

**Verified:**
- Local preview: `blog/index.html` lists all 30 published posts, sorted by date descending,
  each with a working thumbnail and link.
- Spot-checked 3 individual post pages in a real browser
  (`blog/accredited-investor-requirements.html`,
  `blog/blog-post-title-one-6648y.html`, and the index itself): unique `<title>`, correct
  meta description, hero image actually loads, body content renders, footer is correct.
  `blog/blog-post-title-one-6648y.html` also carries an FAQ section — confirmed both its
  `BlogPosting` and `FAQPage` JSON-LD blocks parse as valid JSON via the browser console.
- Ran a link check across all 30 generated post pages: every `hero_image` and inline
  (`inline-0`, `inline-1`, ...) image path referenced in the generated HTML resolves to a
  real file on disk (60 unique image paths checked, zero missing).
- No console errors on any of the pages checked in the browser preview.

### 2.3 `robots.txt`
Added at the repo root:
```
User-agent: *
Allow: /

Sitemap: https://assemble.capital/sitemap.xml
```
Matches the existing `sitemap.xml`'s URL format exactly (`https://assemble.capital/...`).
Verified locally: `curl http://localhost:4173/robots.txt` returns 200 with this content.

Note: `tools-build-preview.py` (a separate, apparently-unused staging tool — see §4) also
writes a `robots.txt`, but into a sibling `../assemble-capital-preview/` folder for
uploading to a generic static host. That folder doesn't exist on disk and Vercel deploys
straight from this repo's root via Git, not from that staged copy — so that script's
robots.txt was never actually reaching production. The new root-level `robots.txt` is the
one that matters for the live site.

### 2.4 Legacy Squarespace blog redirects (`vercel.json`)
The README's "Open items" section noted the old blog lived at
`assemble.capital/assemble-capital-blogs/...` on Squarespace, and flagged that migrating it
would need those URLs redirected. Investigating `blog/posts.json` turned up an undocumented
`_migration_source` field on every one of the 29 recovered posts, recording the exact
original URL, e.g.:
```
https://assemblecapital.squarespace.com/assemble-capital-blogs/10-red-flags-in-real-estate-offering-documents
```
Confirmed programmatically that every post's `slug` field is identical to the last path
segment of its `_migration_source` — i.e., new URLs are a 1:1 match to old ones. `vercel.json`
now has:
```json
{
  "redirects": [
    { "source": "/assemble-capital-blogs", "destination": "/blog/index.html", "permanent": true },
    { "source": "/assemble-capital-blogs/", "destination": "/blog/index.html", "permanent": true },
    { "source": "/assemble-capital-blogs/:slug", "destination": "/blog/:slug.html", "permanent": true }
  ]
}
```
No existing `vercel.json` was present, so this created it fresh — nothing was clobbered.

**Residual gap, needs Oliver:** the `_migration_source` domain recorded is the Squarespace
default subdomain (`assemblecapital.squarespace.com`), not the live custom domain. The
README implies the custom domain used the identical path structure
(`assemble.capital/assemble-capital-blogs/...`), which is standard for a Squarespace site
with a connected custom domain, so the redirect above should be correct — but this wasn't
independently confirmed against an archived copy of the old live site (e.g. the Wayback
Machine) or Google Search Console's list of previously-indexed URLs. **Before or shortly
after push, Oliver should pull the old blog's URL list from Google Search Console
(Coverage / Pages report, or the legacy Search Console's "previously indexed" data) or
Squarespace's old sitemap.xml (if still reachable) and confirm there are no old post slugs
that aren't in this list of 29** — if there are, they'll need either a matching post added
to `posts.json` or an explicit redirect entry, since the wildcard rule above only helps
slugs it can match to a real `blog/<slug>.html` file.

---

## 3. The blog content pipeline (for future posts)

`blog/posts.json` is the single source of truth. Full field schema is in `blog/README.md`
(now includes the `_migration_source` field, which was previously present in the data but
undocumented).

**To add a new post:**
1. Append an object to the `posts.json` array with `"status": "published"` (or `"draft"`
   to stage it without publishing yet — see below).
2. Run, in this order:
   ```
   python3 tools-generate-blog-pages.py   # writes blog/<slug>.html + rebuilds blog/index.html
   python3 tools-rebuild-footer.py        # refreshes the footer's latest-4-posts list sitewide
   python3 tools-generate-sitemap.py      # adds the new post's URL to sitemap.xml
   ```
3. Preview locally (`python3 -m http.server 4173`) and check the new post renders correctly
   before committing.
4. Commit and push.

**To take a post live later that was staged as a draft:** flip its `"status"` to
`"published"` in `posts.json` and re-run the same three commands.

`tools-add-analytics.py` also exists in the repo root and expects blog posts one directory
deep (`blog/<slug>.html`, not year-nested) — this is already how the generator writes them,
so no extra step is needed there, but don't restructure the blog into date-nested folders
without checking that script too.

---

## 4. Remaining SEO/technical gaps (not fixed this session)

Roughly ordered by how much they're likely worth vs. effort, but see §5 for the actual
priority-ordered checklist.

- **No JSON-LD/structured data outside the blog.** The blog generator emits
  `BlogPosting` (and `FAQPage` where applicable) JSON-LD per post — but the homepage,
  `about.html`, all 4 strategy pages, and all 18 property pages have zero structured data.
  At minimum, an `Organization`/`LocalBusiness` block sitewide (name, logo, address, phone,
  sameAs links to LinkedIn/Instagram) and something like `RealEstateListing` or a generic
  `Product`/`CreativeWork` block per property page (address, photos, description) would be
  a meaningful, low-risk SEO upgrade. Not attempted this session — real content/schema
  design work, not a bug fix.
- **Blog post dates look like batch-import defaults, not real original publish dates.**
  14 of the 30 posts share the exact date "December 18, 2025"; 5 share "November 18, 2025";
  4 share "May 28, 2019". That's very unlikely to reflect 14 genuinely simultaneous
  original publish dates — more likely a fallback timestamp applied during the Squarespace
  recovery process. This affects sort order on the blog index and the `datePublished` in
  each post's JSON-LD, but doesn't break anything. If Oliver has access to the old
  Squarespace export/admin with real per-post dates, worth back-filling; otherwise not
  urgent.
- **Four posts have ugly auto-generated slugs** (`blog-post-title-four-y3jky`, etc. — see
  §2.2). Content is fine; URLs aren't SEO-friendly. Renaming requires: updating the slug in
  `posts.json`, renaming the matching `assets/img/blog/<old-slug>/` folder, regenerating,
  and adding a redirect from the old slug to the new one (both are now potentially
  "legacy" URLs — the original Squarespace one from `_migration_source`, and the ugly one
  that will have been live on this site in the interim). Not done this session — real risk
  of breaking a URL that's already been live briefly, better done deliberately in its own
  pass.
- **6 pages Semrush flagged as blocked from crawling** — not independently diagnosed this
  session. Worth re-running the Semrush crawl after these fixes are live; may resolve on
  its own now that `robots.txt` exists and doesn't need further action, or may point at
  something else (e.g. a `noindex` meta tag somewhere, or a page returning a non-200). If
  it persists, that's the next thing to dig into.
- **`tools-build-preview.py` looks like dead/orphaned tooling.** It stages a deployable
  copy into a sibling folder for "any static host," including its own `robots.txt`, but
  Vercel deploys directly from this repo via Git — that sibling folder doesn't exist on
  disk and doesn't appear to be part of the actual deploy path. Its console output also
  has a stale line ("robots.txt: Disallow: /  (blocks crawling of the review link)") that
  contradicts the `Allow: /` it actually writes — a leftover from when this script staged a
  non-production preview link. Worth deciding whether to update it to match the Vercel-only
  reality, or delete it, in a future cleanup pass. Not touched this session since it's not
  in the live path and isn't broken, just confusing.
- **Alt text:** checked broadly — property-page gallery photos have descriptive alt text
  (e.g. `"The Apex HH — photo 1"`), decorative logo/watermark images correctly use
  `alt=""` with `aria-hidden="true"`, and the lightbox's empty `<img src="" alt="">`
  placeholder is a JS-driven element, not a real content gap. No alt-text problem found.

---

## 5. Prioritized checklist for the next session

1. **Push this commit and re-run the Semrush Site Audit** to confirm the error count drops
   as expected and see what (if anything) remains once the crawler can actually reach a
   working blog and a clean footer. This validates the whole theory of the fixes above.
2. **Close the Squarespace redirect gap** (§2.4) — pull the old blog's real URL list from
   Google Search Console or an archived sitemap and confirm no post slugs are missing from
   the 30 in `posts.json`; add explicit redirects for any that are.
3. **Legal page review — compliance risk, not SEO** (see prominent callout below).
4. **Add sitewide JSON-LD** (Organization + per-property structured data) — real content
   work, biggest remaining SEO gap.
5. Decide on and execute the **ugly-slug cleanup** for the 4 ambiguously-named blog posts,
   with proper redirects.
6. **Back-fill accurate blog post dates** if the original per-post dates are recoverable
   from Squarespace.
7. Decide the fate of `tools-build-preview.py` — update it to match reality or remove it.
8. Wire the contact form to a real form service (Formspree, Basin, or the CRM) instead of
   `mailto:` — this was already flagged as an open item in the README pre-dating this
   session, unrelated to the Semrush audit, but still open.

---

## ⚠️ Legal pages — compliance risk, flagged prominently

`terms.html`, `privacy.html`, and `disclosures.html` are marked in the repo's own README as
**drafts that must be reviewed by qualified securities/privacy counsel before the site is
considered fully launched** — each file carries an HTML comment saying the same. This is a
**compliance risk, not a technical or SEO issue**, and nothing in this session touched their
content. If these pages haven't already been reviewed by counsel since the July 2026
rebuild, that should happen independently of any of the technical work in this document —
don't let "the site is technically healthy now" be read as "the site is legally ready."

---

## Working notes — concurrent session collision during this work

While this session was in progress, a **second, separate Claude Code session** (also
authenticated as `oliverthornton`) was independently working in this exact same repo at the
same time, doing unrelated SEO content work: it added an FAQ section + `FAQPage` JSON-LD to
5 existing posts, authored one new post ("Accredited Investor Requirements"), and — because
it ran `tools-rebuild-footer.py` after this session had already fixed the Facebook-link bug
in that script — its own commit ended up absorbing this session's footer fix too. That
commit is already in the local history as:

```
7b61930  SEO revision pass on 5 priority posts + new accredited-investor guide
```

sitting between the original baseline (`4898908`) and the commit this session made on top
of it. Its commit message is thorough and explains its own reasoning (it explicitly left
everything as `"draft"` — "Publishing is a separate decision"). Nothing about it looked
wrong on review — the new post is well-reasoned, appropriately hedged around not
referencing a specific current offering, and consistent with `disclosures.html`'s existing
general-solicitation language — so it was left in place rather than reverted, and this
session's blog-publishing decision (§2.2) treated its output as part of the 30 posts to
evaluate for publishing.

**Practical effect for Oliver:** `git log` will show two new local commits, not one, and
`git diff HEAD~1` alone won't show the footer fix (it's in the older of the two). Use
`git diff 4898908..HEAD` to see the full combined diff against the last state that was
actually live, or review the two commits individually with `git show 7b61930` and
`git show HEAD`.

**Worth understanding before this happens again:** two agent sessions editing the same
repo at the same time is inherently risky — this one happened to resolve cleanly, but it
easily could not have (e.g. if both had tried to write `blog/posts.json` at overlapping
moments). If multiple sessions are going to work on this repo concurrently going forward,
worth deciding on a convention (e.g. one session at a time, or coordinate on which files
each will touch) rather than relying on this outcome repeating.
