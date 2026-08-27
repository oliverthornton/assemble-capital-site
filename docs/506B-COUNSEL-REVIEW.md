# Assemble Capital — Rule 506(b) Counsel Review

**Prepared for:** securities counsel
**Site:** https://assemble.capital · **Branch:** `seo-metadata-506b` (15 commits)
**Status:** **NOT DEPLOYED.** Nothing in this document is live. Production still serves the
pre-existing site. Going live requires a deliberate deploy that has not been made.
**Date:** 2026-08-27

> Implementation record prepared by the site's engineer, not legal advice. Rule 506(b) compliance
> is fact-specific. Counsel should approve the exact public wording and the investor-access
> workflow before deployment.

---

## 1. Read this first — what is and is not changing

Almost everything in Sections 3–5 below **already exists on the live site today**. This review is
not primarily about new copy. It is about whether the *existing* public posture is right, made
newly urgent because the branch materially improves the site's search visibility.

**What actually changes on deployment:**

| Change | Scope |
|---|---|
| Technical SEO — canonical tags, robots directives, unique titles/descriptions, Open Graph and Twitter cards, structured data | 49 pages (the live site currently has **zero** canonical tags) |
| Public metadata scrubbed of offering and performance language | all pages |
| New educational article: *SB 684 and SB 1123 Explained* | 1 new page |
| Kentwood status changed from "In construction · ~20%" to "In construction" | 2 pages |
| Strategy page: adds "Senate Bill" / "Starter Home Revitalization Act" wording, links to the new article | 1 page |
| Facebook and TikTok buttons added to the footer | 49 pages |

**Body copy is otherwise byte-identical to the live site.** An earlier pass had replaced the
offering-structure copy; it was restored in full at the owner's direction (Section 2).

**The material risk change is exposure, not wording.** The site currently has no canonical tags and
thin metadata. After deployment it is substantially more indexable, and the SB 684 / SB 1123
article is designed to attract non-brand search traffic. Public statements that were low-traffic
become higher-traffic.

---

## 2. Owner decisions already taken

Recorded so counsel knows these were deliberate, and can override.

| # | Decision | Owner rationale |
|---|---|---|
| D1 | Offering-structure copy **stays public** — 8% preferred return, Class A/B splits, waterfall mechanics, the "$100,000 investment" worked example | *"As long as specific deal information on financials for an active 506(b) project isn't being provided, it's fair game to showcase this type of information."* |
| D2 | The tagline **stays** — "Generating asymmetrical returns through real estate syndication" | Established brand asset; not to be changed |
| D3 | 23 "Join the investment network" CTAs **stay** | Restored with D1 |
| D4 | Kentwood construction percentage **removed** | A percentage goes stale silently and needs constant monitoring |

**Verification performed against D1.** Every dollar figure, equity multiple and IRR on the site was
matched against the entity map. **None attaches to an active Assemble Capital deal:**

| Active deal | Financials published |
|---|---|
| Gonzaga (AC I) — in escrow | none; status only |
| Berryman (AC II) — on market | none; status only |
| Culver VI / 3850 Westwood (AC III) | none; stage only |
| SAMO IV / 1925 19th St (AC IV) | none; stage only |
| Kentwood / 6450 W 85th St (AC V) | none (the `~20%` was construction progress, now removed) |
| Harter (AC VI) · Helms (AC VII) | none; rendering and stage only |

Every `$`, multiple and IRR figure on the site belongs to a **completed Thornton Development Group
project**. The stated standard in D1 is met.

---

## 3. Items requiring counsel decision

### 3.1 Public performance statistics — *highest exposure*

Publicly displayed, and staying under D1:

- **Homepage stat band, above the fold:** `21 completed projects` · `$86.0M dispositions & carried
  value` · `2.13x blended realized equity multiple — 7 documented exits` · `~38% avg. deal-level
  IRR on realized exits`
- **`/track-record.html`:** full realized-performance tables including equity multiples and IRR
- **19 property pages:** per-deal equity invested / returned / profit, equity multiple, IRR, gross
  profit on cost

**Attribution is present and accurate** in four places: a dedicated note on the track-record page
naming Thornton Development Group explicitly; three footnotes on the homepage; the `class="legal"`
disclosure block on every page; and a page-level sentence on all 17 TDG property pages.

**The open questions are prominence and appropriateness, not absence:**

1. The homepage stat band renders **above the fold**; its attributing footnote sits further down.
   A visitor can see the numbers before learning whose they are.
2. `/track-record.html` is headed *"Every number, on the record"* over TDG results, on an Assemble
   Capital domain.
3. Whether sponsor-level, unaudited figures belong on an unrestricted public page at all.

**Decision:** keep as-is / move attribution adjacent to the stat band / move figures behind the
investor portal.

### 3.2 Investment-structure content

Public under D1, counsel to confirm:

- **`/strategies.html`, "How You Invest"** — a section walking a visitor through investing as a
  Class A member, stating a preferred return "historically 8%", describing the Class A / Class B
  waterfall, and giving a worked **"A $100,000 Investment"** example.
- **19 property pages and 4 strategy pages** — "We syndicate Los Angeles residential projects with
  accredited investors — an 8% preferred return paid first, Class A participation in the profits...
  Join the network to see the next offering."
- **`/about.html`** — Class A / Class B structure with an 8% preferred return and project-specific
  splits.
- **23 CTA buttons** reading "Join the investment network".

These publish preferred return, waterfall mechanics, ownership-class structure and an
investment-size example on an unrestricted page. The site carries disclaimers; counsel should
confirm the disclaimers are sufficient and that none of this constitutes general solicitation.

### 3.3 The tagline

"Generating **asymmetrical returns** through real estate syndication" appears as the homepage H1,
in the homepage eyebrow ("Los Angeles · Real Estate Syndication"), and on `/about.html`
("focused on generating asymmetric returns"). Retained under D2.

This is a statement about **outcomes** rather than a description of deal structure, which is a
different category from 3.2. Counsel should confirm it is acceptable on an unrestricted page.

**Related, outside this repository:** the **Assemble Capital Facebook page bio** reads *"Generating
Asymmetrical Returns Through Multi Family Real Estate Syndication."* That is public on a Meta
property, indexed, and will be linked from `sameAs` structured data on all 49 pages after
deployment. It cannot be changed from the website.

### 3.4 Blog content — 13 investor-acquisition posts

Unchanged from the live site. Highest exposure first:

| Post | Issue |
|---|---|
| `real-estate-syndication-for-accredited-investors-los-angeles` | body promises "asymmetrical returns" twice; "one of the most powerful wealth-building strategies for accredited investors"; names Assemble Capital as the sponsor to align with |
| `accredited-investor-requirements` | targets "accredited investor" directly |
| `multifamily-vs-single-family-which-offers-better-returns` | "asymmetric returns — where the upside far exceeds the downside"; "protecting investor capital while amplifying returns" |
| `what-to-know-before-investing-in-a-private-placement` | private-placement investor intent |
| `10-red-flags-in-real-estate-offering-documents` | offering-document intent |
| `how-to-read-a-real-estate-offering-memorandum` | offering-document intent |
| `why-projected-returns-matter-less-than-structure` | projected-returns framing |
| `understanding-downside-protection-in-private-deals` | private-deal investor intent |
| `general-partner-vs-limited-partner-in-a-syndication` | syndication framing |
| `risk-vs-return-questions-to-ask-before-you-invest` | direct investor-decision framing |
| `timing-vs-time-in-market-for-private-real-estate` | private-investment framing |
| `what-makes-a-sponsor-worth-trusting` | "best real estate syndication companies" |
| `exit-strategies-sell-lease-or-reinvest` | investor-decision framing |

All 15 posts warrant a pass; these 13 are the highest exposure. Note these posts become **more
discoverable** after deployment.

**Options per post:** leave as-is with approval / rewrite toward development education / set
`noindex, follow` pending rewrite.

### 3.5 Investor portal and qualification workflow

`https://assemblecapital.cashflowportal.com` is linked from the public header on every page.
Counsel should confirm the portal's gating establishes a pre-existing substantive relationship, and
that a self-attested accreditation checkbox is not the sole basis for qualification before
offering-specific materials are shared.

### 3.6 Related-party construction

**Harter (AC VI) and Helms (AC VII) are owned by Assemble Capital but built by Thornton Development
Group.** Ownership attribution on the site is correct and unaffected.

The disclosure question is different: the homepage markets the firm as *"Vertically integrated —
acquisition, entitlement, architecture coordination, construction management, and disposition
handled **in-house**"*, and `/about.html` says *"Every aspect of the development process is
coordinated in-house."* In substance that is accurate — common principals — but the builder is an
**affiliated entity under common control** earning construction fees on AC-owned projects.

Counsel should confirm (a) the arrangement is disclosed in the offering documents as a
related-party transaction and conflict of interest, and (b) whether "in-house" is the right public
characterisation of an affiliate relationship. `/disclosures.html` addresses sponsor compensation
and conflicts generally; this specific relationship is not named publicly.

### 3.7 Realized results associated with an active offering

`/properties/david-iii.html` presents David III's realized `1.41x` and `~17% IRR` — a completed TDG
project — then states it is *"the proof-of-concept for the tenancy-in-common exit — **now the model
at 1925 19th St**."* 1925 19th St is SAMO IV, an active Assemble Capital offering.

No SAMO IV financials are stated. The issue is the inferential association between a completed
deal's realized results and an active offering.

---

## 4. Verified — no action required

Recorded so counsel does not need to re-check.

- **Predecessor / affiliate attribution is complete and correct.** All 17 TDG property pages carry:
  *"This project was completed by the principals through Thornton Development Group or an affiliated
  predecessor entity. It was not an Assemble Capital offering and did not involve Assemble Capital
  investors."* Gonzaga and Berryman — actual Assemble Capital deals — correctly omit it.
- **No active-offering economics are published anywhere.** See the table in Section 2.
- **Public metadata is clean.** No `<title>`, `<meta description>`, Open Graph or Twitter tag on any
  non-blog page contains `accredited`, `asymmetric`, `8% preferred`, `next offering`, `now raising`,
  `invest now`, or `join the network`. Search results and social previews stay neutral even where
  the page body carries the full structural detail.
- **Legal pages** — `/terms.html`, `/privacy.html`, `/disclosures.html` — remain `noindex, follow`,
  linked in the footer, and excluded from the sitemap.
- **The new SB 684 / SB 1123 article** contains no offering, availability, or performance language.
  It is educational content citing primary California Government Code sections, carries a
  last-reviewed date, and states it is not legal advice.

---

## 5. Deployment gate

Do not publish until counsel has approved:

- [ ] **3.1** Public performance statistics — prominence and appropriateness
- [ ] **3.2** Investment-structure content — preferred return, waterfall, worked example, CTAs
- [ ] **3.3** The tagline, on-site and in the Facebook page bio
- [ ] **3.4** Disposition of the 13 investor-acquisition blog posts
- [ ] **3.5** Investor-portal qualification workflow
- [ ] **3.6** Related-party construction disclosure
- [ ] **3.7** David III / SAMO IV association
- [x] Predecessor attribution — verified complete, no action
- [x] No active-offering economics published — verified
- [x] Public metadata free of offering language — verified
