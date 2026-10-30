#!/usr/bin/env python3
"""Build lenders.html (for construction and bridge lenders) and the lender marquee snippet.

    python3 tools-build-lenders-page.py

Shell (head, header, footer) is borrowed from investors.html. LENDERS drives both the
marquee on lenders.html and the homepage band (between <!-- LENDERS --> markers).
Logos live in assets/img/lenders/ and render in one ink tone (CSS filter) so they read as a set.
"""
import html as H
import json
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://assemble.capital/"

# (name, logo file, display height in px — tuned so each mark has similar visual weight)
LENDERS = [
    ("Anchor Loans", "anchor-loans.png", 22),
    ("Genesis Capital", "genesis.svg", 40),
    ("Lendyx", "lendyx.svg", 30),
    ("Churchill Real Estate", "churchill.svg", 21),
    ("ARIXA Capital", "arixa-capital.png", 38),
    ("Convoy Home Loans", "convoy-home-loans.png", 28),
    ("Archwest", "archwest.svg", 34),
]


def marquee(label):
    def li(n, f, h, hidden=False):
        aria = ' aria-hidden="true"' if hidden else ""
        alt = "" if hidden else H.escape(n)
        return f'<li{aria}><img src="assets/img/lenders/{f}" alt="{alt}" style="height:{h}px" decoding="async"></li>'
    items = "".join(li(*l) for l in LENDERS)
    dup = "".join(li(*l, hidden=True) for l in LENDERS)
    return (f'<div class="lender-marquee" role="region" aria-label="{label}">'
            f'<ul class="lm-track lm-logos">{items}{dup}</ul></div>')


ICON = {
    "capital": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 10l9-6 9 6M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18"/></svg>',
    "build": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 21h18M5 21V9l7-5 7 5v12M9 21v-6h6v6"/></svg>',
    "sell": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 12l-8 8-9-9V3h8l9 9z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l8 3v6c0 4.5-3.4 8.2-8 9-4.6-.8-8-4.5-8-9V6l8-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>',
    "call": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H8l-5 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 3H6v18h12V7l-4-4z"/><path d="M14 3v4h4M9 12h6M9 16h6"/></svg>',
    "plans": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18v14H3zM3 10h8v9M11 14h10"/></svg>',
    "draw": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 12a8 8 0 1 1-2.3-5.6M20 4v4h-4"/></svg>',
}

# Pipeline tracker: stage index reached (0 Acquisition … 4 Sellout); `now` is the active stage
STAGES = ["Acquisition", "Entitlement", "Permits", "Construction", "Sellout"]
PIPELINE = [
    ("The Culver VI", "properties/the-culver-vi.html", "3850 Westwood Blvd", 6, 2, "Tentative map approved"),
    ("The Harter V", "properties/the-harter-v.html", "4058 Harter Ave", 5, 1, "In entitlement"),
    ("The Helms VI", "properties/the-helms-vi.html", "3562 Helms Ave", 6, 1, "Tentative map filed"),
    ("The Sentney VI", "properties/the-sentney-vi.html", "3011 Sentney Ave", 6, 0, "In escrow"),
]


def pipeline_tracker():
    head = "".join(f"<span>{s}</span>" for s in STAGES)
    rows = []
    for name, href, addr, homes, now, status in PIPELINE:
        cells = "".join(
            f'<i class="{"done" if i < now else "now" if i == now else ""}" title="{STAGES[i]}"></i>' for i in range(5))
        rows.append(f'<a class="pt-row" href="{href}"><div class="pt-name"><b>{name}</b><span>{addr} &middot; {homes} homes</span></div>'
                    f'<div class="pt-bar" aria-label="{status}">{cells}</div><div class="pt-status">{status}</div></a>')
    total = sum(p[3] for p in PIPELINE)
    return (f'<div class="pipe-tracker reveal"><div class="pt-head"><span class="pt-total"><b>{total}</b> homes across {len(PIPELINE)} Culver City sites</span>'
            f'<div class="pt-stages">{head}</div><span></span></div>{"".join(rows)}'
            f'<div class="pt-key"><span><i class="done"></i>Complete</span><span><i class="now"></i>Current stage</span><span><i></i>Ahead</span></div></div>')


def paydown_svg():
    # Illustrative stepped loan balance: one release payment per home sale (6 homes). No values shown.
    x0, x1, y0, y1 = 40, 520, 30, 210
    steps = 6
    w = (x1 - x0 - 90) / steps
    d = f"M{x0},{y0} H{x0 + 90}"
    for i in range(steps):
        x = x0 + 90 + w * i
        y = y0 + (y1 - y0) * (i + 1) / steps
        d += f" V{y:.1f}" + (f" H{x + w:.1f}" if i < steps - 1 else "")
    area = d + f" V{y1} H{x0} Z"
    homes = "".join(
        f'<g transform="translate({x0 + 90 + w * i - 9:.1f},{y1 + 12})"><path d="M2 9 9 3l7 6v8H2z"/></g>' for i in range(steps))
    return f'''<svg class="paydown" viewBox="0 0 560 250" role="img" aria-label="Illustration: the loan balance steps down each time one of six homes closes escrow, reaching zero at the last sale.">
  <line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" class="pd-axis"/>
  <line x1="{x0}" y1="{y0 - 10}" x2="{x0}" y2="{y1}" class="pd-axis"/>
  <text x="{x0 - 12}" y="{(y0 + y1) / 2}" class="pd-lbl" text-anchor="middle" transform="rotate(-90 {x0 - 12} {(y0 + y1) / 2})">Loan balance</text>
  <path d="{area}" class="pd-area"/>
  <path d="{d}" class="pd-line"/>
  <text x="{x0 + 45}" y="{y0 - 10}" class="pd-lbl" text-anchor="middle">Construction</text>
  <text x="{x0 + 90 + w * 3:.1f}" y="{y0 + 40}" class="pd-lbl" text-anchor="middle">Release payment at each closing</text>
  <g class="pd-home">{homes}</g>
</svg>'''


def lifecycle():
    phases = ["Acquire", "Entitle", "Permit", "Build", "Sell"]
    bars = [
        ("1 / 3", "Acquisition &amp; bridge", "Lots and homes bought at land value, on short closing timelines."),
        ("3 / 4", "Entitlement refinance", "Entitled land refinanced with interest reserves through permit issuance."),
        ("4 / 5", "Ground-up construction", "SB&nbsp;684 and SB&nbsp;1123 homes, funded through monthly draws."),
        ("5 / 6", "Unit-release paydowns", "Each home that closes pays down the loan."),
    ]
    head = "".join(f'<span style="grid-column:{i + 1}"><em>0{i + 1}</em>{p}</span>' for i, p in enumerate(phases))
    rows = "".join(
        f'<div class="lcy-bar{" lc-draws" if "construction" in t else ""}" style="grid-column:{c};grid-row:{i + 1}"><b>{t}</b><span>{s}</span></div>'
        for i, (c, t, s) in enumerate(bars))
    return f'<div class="lifecycle reveal"><div class="lc-phases">{head}</div><div class="lc-gantt">{rows}</div></div>'


FAQ = [
    ("Who guarantees the loans?", "The principals personally guarantee the construction and bridge loans on our projects. Our investors never sign personal guarantees."),
    ("Who builds the projects?", "Construction is managed in-house through Thornton Development Group, led by RC Thornton, a licensed general contractor. Budgets, draw schedules and inspections run through one accountable team."),
    ("What do you typically finance?", "Acquisition and bridge loans on infill lots and homes, entitlement-stage refinances, and ground-up or remodel construction loans with interest reserves, for SB&nbsp;684 small-lot homes and luxury single-family projects."),
    ("Where are your projects?", "Primarily the Westside of Los&nbsp;Angeles and Culver City, plus the Hollywood Hills and select South Bay, Orange County, San Diego and Santa Barbara markets."),
    ("How are the homes sold?", "SB&nbsp;684 homes sit on individual fee-simple parcels and sell one at a time with conventional buyer financing, so loans can be paid down through unit releases. Sales are handled through the principals&rsquo; affiliated brokerage."),
    ("What does a loan package include?", "Sponsor materials (track record, schedule of real estate owned, personal financial statements) plus a per-project package: purchase contract, plans and entitlement status, construction budget and schedule, and comparable sales."),
]


def main_html():
    faq = "\n".join(f'      <details><summary>{q}</summary><div class="ans"><p>{a}</p></div></details>' for q, a in FAQ)
    return f'''<main id="main">

<section class="on-dark tight" style="padding-top:9rem">
  <div class="wrap">
    <p class="eyebrow">For Lenders</p>
    <h1 class="h-lg" style="max-width:52rem">Lend Alongside a Team That Builds, Guarantees and Sells.</h1>
    <p class="muted" style="max-width:40rem;margin:1.2rem 0 0">Assemble Capital and Thornton Development Group develop new small-lot homes and luxury residences across Los&nbsp;Angeles. We work with a short list of construction and bridge lenders on repeat programs, and we&rsquo;re always glad to meet new lending partners.</p>
    <div class="actions" style="margin-top:2rem">
      <a class="btn solid" href="mailto:oliver@assemble.capital?subject=Lender%20inquiry">Start a lender conversation</a>
      <a class="btn" href="portfolio.html">See current projects</a>
    </div>
  </div>
</section>

<!-- LENDER MARQUEE -->
<section class="tight lender-band">
  <div class="wrap">
    <p class="eyebrow" style="margin-bottom:1.2rem">Lenders we&rsquo;ve worked with</p>
  </div>
  {marquee("Lenders we have worked with")}
  <div class="wrap"><p class="footnote" style="margin-top:1.2rem">Lenders that have financed projects of the principals and their affiliated entities. Names and logos are trademarks of their owners, shown for identification only, and do not imply endorsement.</p></div>
</section>

<!-- THE BORROWER -->
<section>
  <div class="wrap">
    <div class="split reveal" style="align-items:end;margin-bottom:2.4rem">
      <div>
        <p class="eyebrow">The Borrower</p>
        <h2 class="h-lg">Why Lenders Repeat With Us.</h2>
      </div>
      <p class="muted" style="max-width:34rem;margin:0">Two decades of building in Los&nbsp;Angeles, one team from acquisition to sale, and principals who stand behind every loan.</p>
    </div>
    <div class="ledger reveal">
      <div class="cell"><div class="num">22<sup>*</sup></div><div class="lbl">Completed projects since 2005</div></div>
      <div class="cell"><div class="num">50+<sup>*</sup></div><div class="lbl">Homes delivered by the principals</div></div>
      <div class="cell"><div class="num">20+<sup>*</sup></div><div class="lbl">Years developing in Los Angeles</div></div>
      <div class="cell"><div class="num">0<sup>*</sup></div><div class="lbl">Notices of default or foreclosures in ~20 years</div></div>
    </div>
    <p class="footnote reveal" style="margin-top:1.4rem">* Figures reflect projects completed by the principals since 2005, through Thornton Development Group and affiliated entities and one Assemble Capital project, based on internal records. See <a href="disclosures.html">Risks &amp; Disclosures</a>.</p>
  </div>
</section>

<!-- ONE TEAM -->
<section class="on-warm">
  <div class="wrap">
    <div class="split reveal" style="align-items:end;margin-bottom:2.4rem">
      <div>
        <p class="eyebrow">One Team, Acquisition to Payoff</p>
        <h2 class="h-lg">Who Stands Behind the Loan.</h2>
      </div>
      <p class="muted" style="max-width:34rem;margin:0">The same principals buy the site, build the homes and sell them, and they personally guarantee the loan the whole way through.</p>
    </div>
    <div class="team-chain reveal">
      <div class="tc-node">{ICON["capital"]}<em>Sponsor</em><b>Assemble Capital</b><span>Sources and acquires sites, raises the equity and manages the loan relationship.</span></div>
      <div class="tc-node">{ICON["build"]}<em>Builder</em><b>Thornton Development Group</b><span>In-house construction led by a licensed general contractor, with clean draw requests.</span></div>
      <div class="tc-node">{ICON["sell"]}<em>Exit</em><b>Affiliated brokerage</b><span>Lists and sells every home, one fee-simple parcel at a time.</span></div>
      <div class="tc-guarantee">{ICON["shield"]}<b>Personal guarantee from the principals</b><span>Covers every construction and bridge loan, from close to final payoff.</span></div>
    </div>
  </div>
</section>

<!-- WHAT WE FINANCE -->
<section>
  <div class="wrap">
    <div class="split reveal" style="align-items:end;margin-bottom:2.4rem">
      <div>
        <p class="eyebrow">What We Finance</p>
        <h2 class="h-lg">Loans Across the Life of a Project.</h2>
      </div>
      <p class="muted" style="max-width:34rem;margin:0">An SB&nbsp;684 site typically uses four loans in sequence, from purchase to the last home sale. We also finance luxury remodels and hillside new builds across Los&nbsp;Angeles.</p>
    </div>
    {lifecycle()}
    <div class="split paydown-wrap reveal">
      <div>
        <p class="eyebrow">The Built-In Exit</p>
        <h3 class="h-md" style="margin:0 0 1rem">Paid Down Home by Home.</h3>
        <p class="muted" style="margin:0 0 1rem">Every SB&nbsp;684 home sits on its own fee-simple parcel and sells with conventional buyer financing. Each closing sends a release payment to the lender, so exposure falls with every sale instead of waiting on a single bulk exit.</p>
        <p class="footnote" style="margin:0">Illustration only. Not to scale and not a projection for any project.</p>
      </div>
      {paydown_svg()}
    </div>
  </div>
</section>

<!-- PIPELINE -->
<section class="on-warm">
  <div class="wrap">
    <div class="split reveal" style="align-items:end;margin-bottom:2.4rem">
      <div>
        <p class="eyebrow">Current Pipeline</p>
        <h2 class="h-lg">Projects in Motion.</h2>
      </div>
      <p class="muted" style="max-width:34rem;margin:0">Four Culver City SB&nbsp;684 projects on the same plans, architect and sequence, so each loan is easier to underwrite than the last. <a href="portfolio.html" class="text-link-inline">All current projects &rarr;</a></p>
    </div>
    {pipeline_tracker()}
    <div class="grid-4 reveal" style="margin-top:2.4rem">
      <a class="photo-card" href="properties/the-culver-vi.html"><div class="frame"><span class="tag">Map Approved</span><img src="assets/img/westwood-hd.jpg" alt="The Culver VI conceptual rendering" loading="lazy"></div><div class="meta"><div class="name">The Culver VI</div><div class="sub">3850 Westwood Blvd &middot; 6 homes</div></div></a>
      <a class="photo-card" href="properties/the-harter-v.html"><div class="frame"><span class="tag">In Entitlement</span><img src="assets/img/harter-hd.jpg" alt="The Harter V conceptual rendering" loading="lazy"></div><div class="meta"><div class="name">The Harter V</div><div class="sub">4058 Harter Ave &middot; 5 homes</div></div></a>
      <a class="photo-card" href="properties/the-helms-vi.html"><div class="frame"><span class="tag">Map Filed</span><img src="assets/img/helms-hd.jpg" alt="The Helms VI conceptual rendering" loading="lazy"></div><div class="meta"><div class="name">The Helms VI</div><div class="sub">3562 Helms Ave &middot; 6 homes</div></div></a>
      <a class="photo-card" href="properties/the-sentney-vi.html"><div class="frame"><span class="tag">In Escrow</span><img src="assets/img/sentney-wide.jpg" alt="The Sentney VI conceptual aerial rendering" loading="lazy"></div><div class="meta"><div class="name">The Sentney VI</div><div class="sub">3011 Sentney Ave &middot; 6 homes</div></div></a>
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section>
  <div class="wrap">
    <div class="reveal" style="margin-bottom:2.4rem">
      <p class="eyebrow">Working Together</p>
      <h2 class="h-lg">From Intro to Final Draw.</h2>
    </div>
    <ol class="flow-steps reveal">
      <li><i>{ICON["call"]}</i><em>01</em><b>Intro call</b><p>We walk through your programs, leverage, pricing and the markets you lend in.</p></li>
      <li><i>{ICON["doc"]}</i><em>02</em><b>Sponsor package</b><p>Track record, schedule of real estate owned and personal financial statements for the guarantors.</p></li>
      <li><i>{ICON["plans"]}</i><em>03</em><b>Deal package</b><p>Contract, plans and entitlement status, budget, schedule and comparable sales for each loan.</p></li>
      <li><i>{ICON["draw"]}</i><em>04</em><b>Close &amp; draw</b><p>Monthly draw requests, site inspections and straightforward reporting through payoff.</p></li>
    </ol>
  </div>
</section>

<!-- FAQ -->
<section>
  <div class="wrap">
    <div class="split reveal" style="align-items:end;margin-bottom:2.2rem">
      <div>
        <p class="eyebrow">Questions</p>
        <h2 class="h-lg">Lender FAQ.</h2>
      </div>
    </div>
    <div class="faq2 faq-short reveal">
{faq}
    </div>
  </div>
</section>

<!-- CTA -->
<section class="cta-band on-warm">
  <div class="wrap reveal">
    <p class="eyebrow">Lending Partners</p>
    <h2 class="h-lg">Let&rsquo;s Talk Programs.</h2>
    <p class="muted" style="max-width:40rem;margin:1.4rem auto 0">Oliver Thornton leads financing for Assemble Capital. Send your term sheet, program guide or a note about what you&rsquo;re lending on.</p>
    <div class="actions">
      <a class="btn" style="border-color:var(--line-strong)" href="mailto:oliver@assemble.capital?subject=Lender%20inquiry">oliver@assemble.capital</a>
      <a class="btn" style="border-color:var(--line-strong)" href="tel:+13107041794">(310) 704-1794</a>
    </div>
  </div>
</section>

</main>'''


def build():
    s = open("investors.html").read()
    top, bottom = s[: s.index('<main id="main">')], s[s.index("</main>") + len("</main>"):]
    title = "For Lenders | Construction &amp; Bridge Lending Partners | Assemble Capital"
    desc = ("Construction and bridge lenders: how to work with Assemble Capital and Thornton Development Group on "
            "Los Angeles SB 684 small-lot homes and luxury residential projects, with loans personally guaranteed by the principals.")
    url = SITE + "lenders.html"
    t = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", top)
    for k in ("description", "og:description", "twitter:description"):
        t = re.sub(rf'(<meta (?:name|property)="{k}" content=")[^"]*"', rf'\g<1>{desc}"', t)
    for k in ("og:title", "twitter:title"):
        t = re.sub(rf'(<meta (?:name|property)="{k}" content=")[^"]*"', rf'\g<1>{title}"', t)
    t = re.sub(r'(<link rel="canonical" href=")[^"]*"', rf'\g<1>{url}"', t)
    t = re.sub(r'(<meta property="og:url" content=")[^"]*"', rf'\g<1>{url}"', t)
    t = re.sub(r'<link rel="preload" as="image"[^>]*>\n', "", t)
    # replace all JSON-LD with WebPage + FAQPage + Breadcrumb
    t = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>\n?', "", t, flags=re.S)
    plain = lambda x: H.unescape(re.sub(r"<[^>]+>", "", x))
    lds = [
        {"@context": "https://schema.org", "@type": "WebPage", "name": "For Lenders", "description": desc, "url": url,
         "isPartOf": {"@type": "WebSite", "name": "Assemble Capital", "url": SITE}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in FAQ]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "For Lenders", "item": url}]},
    ]
    t = t.replace("</head>", "".join('<script type="application/ld+json">\n' + json.dumps(d, indent=2, ensure_ascii=False) + "\n</script>\n" for d in lds) + "</head>")
    open("lenders.html", "w").write(t + main_html() + bottom)

    # homepage band
    s = open("index.html").read()
    band = f'''<!-- LENDERS -->
<section class="tight lender-band">
  <div class="wrap" style="display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:1rem;margin-bottom:1.2rem">
    <p class="eyebrow" style="margin:0">Construction &amp; bridge lenders we&rsquo;ve worked with</p>
    <a href="lenders.html" class="text-link-inline" style="font-size:.82rem">For lenders &rarr;</a>
  </div>
  {marquee("Lenders we have worked with")}
</section>
<!-- /LENDERS -->

'''
    if "<!-- LENDERS -->" in s:
        s = re.sub(r"<!-- LENDERS -->.*?<!-- /LENDERS -->\n\n", band, s, flags=re.S)
    else:
        s = s.replace("<!-- INSIGHTS -->", band + "<!-- INSIGHTS -->", 1)
    open("index.html", "w").write(s)
    print("built lenders.html + homepage band")


if __name__ == "__main__":
    build()
