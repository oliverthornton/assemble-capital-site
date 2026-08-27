# Rule 506(b) — Securities-Counsel Review Checklist

**Branch:** `seo-metadata-506b` · **Prepared:** 2026-08-26
**Status:** NOT DEPLOYED — awaiting counsel sign-off.

> This is an implementation record, not legal advice. Rule 506(b) compliance is fact-specific.
> Counsel must approve the exact public wording and the investor-access workflow before deploy.

---

## Part A — Changes ALREADY APPLIED on this branch

Applied because the implementation plan prescribed the replacement wording, and because the same
change makes the site more discoverable (raising exposure if left as-is). **All are reversible:**
`git diff main..seo-metadata-506b`.

### A1. Public metadata — solicitation language removed sitewide

| Page | Before | After |
|---|---|---|
| `/` title | Assemble Capital — Los Angeles Residential Investment Manager | Los Angeles Residential Development Firm \| Assemble Capital |
| `/` description | "...vertically integrated, **open to accredited investors**." | "...luxury homes, multifamily, fee-simple subdivisions, and TIC housing." |
| `/` og:title + twitter:title | **"Generating Asymmetrical Returns Through Real Estate Syndication"** | Los Angeles Residential Development Firm \| Assemble Capital |
| 19 property pages | "...gallery, **returns**, and investment cycle." | neutral, project-specific development summaries |

### A4. Late catch — "asymmetric returns" on `/about.html`

`about.html` described the firm as "focused on **generating asymmetric returns**". An earlier sweep
searched for "asymmetric*al*" and missed the shorter stem. Replaced with "Assemble Capital is a Los
Angeles residential development firm working across single-family redevelopment, ground-up
multifamily, fee-simple subdivisions, and TIC housing." A stem-based sweep now confirms no
non-blog page carries this or any equivalent performance promise.

### A3. Social-preview alt text — misattribution corrected

An initial pass of this work described TDG projects as Assemble Capital projects in
`og:image:alt` / `twitter:image:alt` (the homepage's Hideaway HH image, the insights index's
David III image, and 12 blog posts using TDG project photos). Corrected: images of TDG projects
are now either described neutrally ("a Los Angeles residential development project") or credited
to "the Assemble Capital principals", matching the framing already used elsewhere on the site.
Only Gonzaga, Berryman, Culver VI, SAMO IV, and Kentwood images are described as Assemble Capital
projects.

**Verified:** no page's `<head>` outside `/blog/` now contains `accredited`, `asymmetrical`,
`open to`, `now raising`, `current offering`, `invest now`, `preferred return`, `equity multiple`,
`target return`, or `join the network`.

### A2. Visible page copy

| Location | Before | After |
|---|---|---|
| `/` H1 | "Generating *asymmetrical returns* through real estate syndication." | "Residential development, *assembled with discipline*." |
| `/` eyebrow | "Los Angeles · Real Estate Syndication" | "Los Angeles · Residential Development" |
| `/` subhead | "...in partnership with **accredited investors who share in the profits**." | "...luxury homes, small multifamily, fee-simple subdivisions, and tenancy-in-common housing." |
| `/` CTA ×2, `/about`, `/portfolio`, 19 property pages (**23 buttons total**) | "Join the investment network" | "Contact the firm" |
| `/contact` eyebrow | "Join the Investment Network" | "Contact the Firm" |
| `/about` Economics card | "...Class A / Class B structure with an **8% preferred return** and project-specific splits..." | "Each project is structured through its own project-specific entity, with economics and governance defined in that project's operating agreement." |
| `/about` CTA heading | "Get to know the platform **before the next offering opens**." | "Get to know the platform and the projects behind it." |
| `/portfolio` heading | "**Future acquisitions are capitalized through new project-specific offerings.**" | "Assemble Capital continues to source and develop residential projects across Los Angeles." |
| `/portfolio` body | "...**Join the network to see the next offering.**" | "...Contact the firm for general information." |
| **19 property pages** | "We **syndicate** Los Angeles residential projects with **accredited investors** — an **8% preferred return** paid first, **Class A participation in the profits**... **Join the network to see the next offering**." | "Assemble Capital develops residential projects across Los Angeles, with the principals' own capital invested in every project. Contact the firm for general information." |
| **4 strategy pages** | "Future projects...capitalized through new **project-specific offerings** — an **8% preferred return**...**what a specific offering looks like**." | "Assemble Capital continues to develop projects in this strategy across Los Angeles, with the principals' own capital invested in every project. Contact the firm for general information about this strategy and the team's work." |
| `/` alignment band | "Our **offerings** have typically paid investors an **8% preferred return** before the sponsor shares in any profit..." | "Assemble Capital invests its own capital in every project it develops. Project-specific terms are governed by that project's operating agreement." |

**Counsel should confirm** each replacement is acceptable and that removing the preferred-return
disclosure from public pages does not create a disclosure gap elsewhere (offering documents must
carry their own complete disclosures).

---

## Part B — DELIBERATELY NOT CHANGED (counsel decision required)

These were left intact because changing them is a business/legal judgment, not an SEO fix.

### B0. Entity map (confirmed by Oliver Thornton, 2026-08-26)

| Entity | Project | Status |
|---|---|---|
| AC I | The Gonzaga Residence — 8404 Gonzaga Ave | construction complete, **in escrow** |
| AC II | The Berryman Residence — 4432 Berryman Ave | construction complete, **on market** |
| AC III | Culver VI — 3850 Westwood | in progress |
| AC IV | The SAMO IV — 1925 19th St | in progress |
| AC V | Kentwood — 85th St | in progress |
| AC VI | Harter | in progress |
| AC VII | Helms | in progress |
| **TDG / affiliates** | **all 17 other property pages** and the entire realized track record | completed |

Assemble Capital has **seven** deals and **zero realized exits**. Every realized return figure on
the site was earned by Thornton Development Group or an affiliated predecessor.

### B1. Public performance statistics — attribution verified, prominence is the open question

**Correction to an earlier draft of this checklist:** attribution is *not* missing. It is present,
accurate, and in four places:

- `track-record.html` — a dedicated note naming Thornton Development Group explicitly and stating
  the results "show how the operators have performed, not what any Assemble Capital offering has
  returned"
- `index.html` — three separate footnotes attributing results to principals and predecessor companies
- the `class="legal"` disclosure block, present on **every** page
- **all 17 TDG property pages** carry a page-level sentence: "This project was completed by the
  principals through Thornton Development Group or an affiliated predecessor entity. It was not an
  Assemble Capital offering and did not involve Assemble Capital investors."

Independently verified: Gonzaga and Berryman correctly **omit** that sentence, and both publish
**no economics whatsoever** — no equity multiple, IRR, or projected return. No active Assemble
Capital offering economics appear anywhere on the public site.

**What remains for counsel** is therefore prominence and framing, not absence:

1. The homepage stat band (`21` · `$86.0M` · `2.13x` · `~38% IRR`) renders **above the fold**,
   while its attributing footnote sits further down the page. A visitor can see the numbers
   without the attribution.
2. `track-record.html` H1 reads "Every number, on the record" over TDG results on an Assemble
   Capital domain.
3. Whether sponsor-level, unaudited figures belong on an unrestricted public page at all.

**Decision needed:** keep as-is / move attribution adjacent to the stat band / move figures behind
the investor portal.

### B2. Predecessor / affiliate attribution — COMPLETE, no action required

Already implemented correctly across all 19 property pages and verified against the entity map in
B0. An earlier draft of this checklist listed this as outstanding; that was wrong.

### B3. Blog content — investor-acquisition oriented

Left entirely untouched. All 15 posts warrant a review pass; the 13 below are the highest exposure, targeting terms the plan lists as do-not-target:

| Post | Issue |
|---|---|
| `real-estate-syndication-for-accredited-investors-los-angeles` | body promises "**asymmetrical returns**" ×2; "why it's one of the most powerful wealth-building strategies for accredited investors"; names Assemble Capital as the sponsor to align with |
| `accredited-investor-requirements` | targets `accredited investor` directly |
| `what-to-know-before-investing-in-a-private-placement` | private-placement investor intent |
| `multifamily-vs-single-family-which-offers-better-returns` | "better returns" framing |
| `10-red-flags-in-real-estate-offering-documents` | offering-document intent |
| `how-to-read-a-real-estate-offering-memorandum` | offering-document intent |
| `why-projected-returns-matter-less-than-structure` | projected-returns framing |
| `understanding-downside-protection-in-private-deals` | private-deal investor intent |
| `general-partner-vs-limited-partner-in-a-syndication` | syndication framing |
| `risk-vs-return-questions-to-ask-before-you-invest` | direct investor CTA framing |
| `timing-vs-time-in-market-for-private-real-estate` | private-investment framing |
| `what-makes-a-sponsor-worth-trusting` | "best real estate syndication companies" |
| `exit-strategies-sell-lease-or-reinvest` | investor-decision framing |

**Options per post:** (a) leave as-is with counsel approval, (b) rewrite toward the
development-education angle, or (c) set `noindex, follow` pending rewrite.

Note: these posts also have the site's only **technical** metadata defects — titles 70–110 chars
and descriptions 187–267 chars, both of which truncate in search results. Fixing those means
rewriting the same sensitive copy, so it was **deliberately deferred to this review** rather than
done unilaterally. All core, strategy, and property pages are within limits.

### B5. `strategies.html` — "How You Invest" section (**recommend moving behind the portal**)

Lines 186–227 are a 41-line public module titled **"How You Invest / The investment model, step
by step"**, containing:

- Steps 1–4 walking a visitor through investing as a **Class A member**
- "investors receive a **preferred return (historically 8%)** and their capital back before the
  sponsor takes a dollar of profit"
- "split between Class A (investors) and Class B (sponsor) **through the waterfall**"
- a worked example: **"A $100,000 Investment"** → `You invest (Class A) $100,000` ·
  `Preferred return paid first 8% — $8,000` · `Your capital returned $100,000`

This is the **most solicitation-like artifact remaining on the public site**. It publishes
preferred return, waterfall mechanics, Class A/B structure, and an investment-size example — four
items on the plan's do-not-publish list — and the plan states a disclaimer does not cure language
that may itself be viewed as solicitation.

**Left in place deliberately.** Unlike the one-line CTAs and sentences already replaced, this is an
entire named page section; removing it changes what the page is, and relocating it behind the
investor portal is a migration decision, not an edit. **Recommendation: move it to the portal.**

### B6. Related-party construction (Harter, Helms, and current AC projects)

Confirmed by Oliver: **Harter (AC VI) and Helms (AC VII) are owned by Assemble Capital but built
by Thornton Development Group.** Ownership attribution on the site is unaffected and correct.

The disclosure question is different: `index.html` markets the firm as **"Vertically integrated —
acquisition, entitlement, architecture coordination, construction management, and disposition
handled in-house"**, and `about.html` says "Every aspect of the development process is coordinated
in-house." In substance that is accurate (common principals), but the builder is an **affiliated
entity under common control**, which makes it a **related-party arrangement** — an affiliate earning
construction fees on AC-owned projects.

Counsel should confirm (a) the arrangement is disclosed in the offering documents as a conflict of
interest and related-party transaction, and (b) whether "in-house" is the right public
characterisation of an affiliate relationship. `disclosures.html` already contemplates sponsor
compensation and conflicts generally; this specific relationship is not named publicly.

### B4. Investor Portal link

`https://assemblecapital.cashflowportal.com` is linked from the public header on every page.
Counsel should confirm the portal's own gating establishes a pre-existing substantive relationship
and that a self-attested accreditation checkbox is not the sole qualification basis.

---

## Part C — Deployment gate

Do not publish until counsel has approved:

- [ ] Part A replacement wording
- [ ] Part B1 — prominence of public performance statistics (attribution already correct)
- [x] Part B2 — predecessor/affiliate attribution COMPLETE and verified (no action)
- [ ] Part B3 — disposition of the blog (13 highest-exposure posts listed; all 15 warrant a pass)
- [ ] Part B4 — investor-portal qualification workflow
- [ ] Part B5 — `strategies.html` "How You Invest" module (**recommend moving behind the portal**)
- [ ] Part B6 — related-party construction disclosure (TDG builds AC-owned Harter/Helms)
