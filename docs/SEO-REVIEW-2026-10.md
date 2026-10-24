# Assemble Capital — SEO Review (October 2026)

**Checked:** 2026-10-23 · **Source:** Semrush `us` database (330 API units), live-site crawl, search-index snapshot
**Baseline:** `SEO-KEYWORD-MAP.md` (2026-08-26). It recorded keyword volumes, not rankings, so this is the first ranking snapshot.

---

## 1. Where the site stands

| Metric | Value |
|---|---|
| Ranking keywords (top 100) | **14** |
| In top 3 / top 10 / top 20 / top 30 | 0 / 1 / 1 / 1 |
| Estimated organic traffic | **~0 visits/month** |
| Semrush Authority Score | **2** (out of 100) |
| Backlinks / referring domains | 347 / 213 (219 follow, 128 nofollow) |
| Pages indexed (search-index snapshot) | ~40 of 53 found, including legacy Squarespace URLs |

### Every keyword the site ranks for

| Keyword | Pos. | Vol. | KD | Page |
|---|---|---|---|---|
| assemble management | 8 | 40 | 22 | portfolio |
| assemble group | 20 | 70 | 10 | portfolio |
| tenant in common california | 21 | 50 | 13 | TIC blog post |
| tenancy in common california | 34 | 170 | 12 | TIC blog post |
| tenants in common california | 45 | 320 | 5 | TIC blog post |
| tenants in common california definition | 46 | 50 | 16 | TIC blog post |
| **sb 1123** | **58** | **590** | 19 | SB 684 blog post |
| sb1123 ca | 59 | 50 | 16 | SB 684 blog post |
| assemblage real estate (definition) | 83–87 | 90–210 | 2–4 | homepage / glossary |

**What this says:**
- **Brand-confusion terms** ("assemble management", "assemble group") bring no relevant visitors.
- **The two pages with real potential:**
  - The **TIC post**, which sits on pages 3–5 for a cluster of about 600 searches a month at very low difficulty (KD 5–13).
  - The **SB 684 post**, which sits on page 6 for "sb 1123" (590 a month).
- **What doesn't rank at all:**
  - **"sb 684"** (480 a month, KD 18).
  - The SB 684 strategy page.
  - Submit a Deal.
  - Any investor-intent term.

---

## 2. Issues found

### A. Blog posts have no real subheadings (technical, high impact)
Every blog post jumps from the `<h1>` straight to `<h4>` section headings. The only `<h2>`s on each post are the footer CTAs ("Keep Going.", "Want to invest in the next one?").

So Google sees no topical structure. That hurts the two posts most: the SB 684 post (2,300 words) and the TIC post (4,400 words), whose sections ("What are SB 684 and SB 1123?", "Who qualifies?") are exactly the questions people search.

**Fix:** promote the article `<h4>`s to `<h2>`/`<h3>`, and demote the footer CTAs to non-heading elements. It's a styling-neutral change.

### B. The search index still shows old return figures (506(b) risk)
The live pages are clean, but the search-index snapshot still carries the old descriptions:
- **Apex HH:** "returning $4.09M on $1.27M of equity over a 47-month hold"
- **Hollywood Marvel:** "$1.57M of gross project profit — a 95.2% gross profit on total cost"
- **Villa De Vistas:** "Total returned was $1.87M on $700K of equity"
- **Treehouse HH:** "…returns, and investment cycle"
- **Legacy Squarespace URLs** (`/completed-single-family-projects`, `/completed-multi-family-projects-1`) are still listed. They already 308-redirect correctly.

**Fix (your action):** verify `assemble.capital` in Google Search Console, submit the sitemap, and use *URL Inspection → Request indexing* on the four property pages above plus the track-record page. Adding `<lastmod>` dates to the sitemap (fix C) also prompts a recrawl.

### C. Sitemap has no `<lastmod>` dates
Without them, Google has no signal that the pages changed in October. Add the git last-commit date per page.

### D. Titles and descriptions
- **SB 684 post title:** "SB 684 and SB 1123 Explained". It doesn't say *California*, *lot split* or *2026*, which are the words in the ranking queries.
  - **Suggested:** "SB 684 & SB 1123 Explained: California's Lot-Split Laws (2026 Guide)".
- **TIC post title:** "Tenancy in Common in Los Angeles". The ranking queries all say *California*.
  - **Suggested:** "Tenancy in Common in California & Los Angeles, Explained".
- **Descriptions over 160 characters** (Google truncates them):
  - 15 of 18 blog posts
  - homepage (218)
  - strategies (180)
  - Submit a Deal (171)
  - glossary (166)

### E. Authority is the ceiling
An Authority Score of 2 with 213 referring domains means the links are almost all low-value: directories, scrapers and Squarespace-era spam. On-page fixes will move the TIC and SB 684 posts onto pages 1–2. Ranking for anything competitive takes a handful of real links.

---

## 3. Recommendations, in priority order

| # | Action | Who | Effort | Expected effect |
|---|---|---|---|---|
| 1 | Search Console: verify, submit sitemap, request reindex of the 5 pages in 2B | Oliver | 20 min | Clears old return figures from search results (compliance) |
| 2 | Fix blog heading structure (h4 → h2/h3) on all 18 posts | Claude | small | Clear structure for the TIC and SB 684 posts |
| 3 | Retitle the SB 684 and TIC posts and trim the 19 over-length descriptions | Claude | small | Better match to the queries already ranking |
| 4 | Add `<lastmod>` to the sitemap | Claude | small | Faster recrawl |
| 5 | Expand the SB 684 post with an LA-specific section: City of LA / Culver City implementation, a real timeline (entitlement start to RTI in about 12 months), fee-simple vs condo, SB 684 vs SB 9. Link it to the strategy page and Submit a Deal. | Claude draft, Oliver review | medium | Targets "sb 684" (480/mo), "sb 684 los angeles" and "sb 684 vs sb 9" |
| 6 | New informational posts in the SB 684 cluster (volumes from the Aug map): "SB 1123 lot split requirements", "SB 684 vs SB 9", "How to sell your lot to an SB 684 developer" (also feeds Submit a Deal) | Claude draft | medium per post | Low-KD informational traffic, 506(b)-safe |
| 7 | Earn 5–10 real links. Concrete sources below. | Oliver | ongoing | Moves the Authority Score off 2 |

**Concrete link sources for #7:**
- Local press and Culver City / Westside outlets on 17th St as an early SB 684 project.
- Partner sites (architect, lender, GC) linking to project pages.
- Guest spots on podcasts and real estate shows.
- BiggerPockets or industry write-ups on SB 684 financing.
- Your own YouTube, podcast and speaking pages linking back.

**Not worth doing:** chasing "real estate syndication los angeles" or other firm-descriptor terms (10–30 searches a month, per the August map), or the brand-confusion "assemble" terms.

**Re-check:** pull `domain_rank` and `resource_organic` (about 150 units) in 30 and 60 days, after fixes 1–4 land.
