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

### B1. Public performance statistics — **highest residual exposure**

Still displayed publicly:

- **Homepage stat band:** `21 completed projects` · `$86.0M dispositions & carried value` ·
  `2.13x blended realized equity multiple — 7 documented exits` · `~38% avg. deal-level IRR on realized exits`
- **`/track-record.html`:** full realized-performance tables, including `equity multiple`
- **19 property pages:** per-deal `Equity invested / returned / profit`, `equity multiple`, `IRR`,
  `gross profit on cost`

These are *realized* results, not projections — a materially different risk posture than target
returns. The plan still requires counsel to approve **attribution, calculation methodology, and
whether they appear publicly at all**, including in search and social previews.

**Decision needed:** keep public / move behind the investor portal / keep with added methodology
and attribution disclosure.

### B2. Predecessor / affiliate attribution

The plan requires a visible attribution wherever a project was **not** an Assemble Capital
offering:

> Completed by the principals through a predecessor or affiliated entity. This project was not an
> Assemble Capital offering and did not involve Assemble Capital investors.

**Not yet added** — Assemble cannot determine from the codebase which of the 19 projects this
applies to. **Oliver must supply the per-project ownership history**, then this can be applied.

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

### B4. Investor Portal link

`https://assemblecapital.cashflowportal.com` is linked from the public header on every page.
Counsel should confirm the portal's own gating establishes a pre-existing substantive relationship
and that a self-attested accreditation checkbox is not the sole qualification basis.

---

## Part C — Deployment gate

Do not publish until counsel has approved:

- [ ] Part A replacement wording
- [ ] Part B1 — public performance statistics (highest exposure)
- [ ] Part B2 — predecessor/affiliate attribution supplied and applied
- [ ] Part B3 — disposition of the blog (13 highest-exposure posts listed; all 15 warrant a pass)
- [ ] Part B4 — investor-portal qualification workflow
