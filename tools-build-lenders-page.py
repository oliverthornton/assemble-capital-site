#!/usr/bin/env python3
"""Build lenders.html (for construction and bridge lenders) and the lender marquee snippet.

    python3 tools-build-lenders-page.py

Shell (head, header, footer) is borrowed from investors.html. LENDERS drives both the
marquee on lenders.html and the homepage band (between <!-- LENDERS --> markers).
Names are text wordmarks; swap in logos only with each lender's permission.
"""
import html as H
import json
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://assemble.capital/"

LENDERS = ["Anchor Loans", "Genesis Capital", "Lendyx", "Churchill", "ARIXA Capital", "Convoy Home Loans", "Archwest"]


def marquee(label):
    items = "".join(f"<li>{H.escape(n)}</li>" for n in LENDERS)
    dup = "".join(f'<li aria-hidden="true">{H.escape(n)}</li>' for n in LENDERS)
    return (f'<div class="lender-marquee" role="region" aria-label="{label}">'
            f'<ul class="lm-track">{items}{dup}</ul></div>')


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
  <div class="wrap"><p class="footnote" style="margin-top:1.2rem">Lenders that have financed projects of the principals and their affiliated entities. Names are shown for identification only and do not imply endorsement.</p></div>
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
    <div class="hl-grid reveal" style="margin-top:2.4rem">
      <div class="hl"><h3>Personal guarantees</h3><p>The principals guarantee our construction and bridge loans personally, so the people running the project are on the hook for it.</p></div>
      <div class="hl"><h3>In-house construction</h3><p>Thornton Development Group manages the build, led by a licensed general contractor, with clean draw requests and on-site accountability.</p></div>
      <div class="hl"><h3>Built-in exit</h3><p>Fee-simple SB&nbsp;684 homes sell one at a time with conventional buyer financing; the principals&rsquo; brokerage handles every sale.</p></div>
      <div class="hl"><h3>Repeatable programs</h3><p>Four Culver City SB&nbsp;684 projects run the same plans, architect and sequence, so underwriting gets easier with every loan.</p></div>
    </div>
    <p class="footnote reveal" style="margin-top:1.4rem">* Figures reflect projects completed by the principals since 2005, through Thornton Development Group and affiliated entities and one Assemble Capital project, based on internal records. See <a href="disclosures.html">Risks &amp; Disclosures</a>.</p>
  </div>
</section>

<!-- WHAT WE FINANCE -->
<section class="on-warm">
  <div class="wrap">
    <div class="split reveal" style="align-items:end;margin-bottom:2.4rem">
      <div>
        <p class="eyebrow">What We Finance</p>
        <h2 class="h-lg">The Loans We Place.</h2>
      </div>
      <p class="muted" style="max-width:34rem;margin:0">Residential projects in Los&nbsp;Angeles and select Southern California markets.</p>
    </div>
    <div class="finish-grid reveal">
      <div><b>Acquisition &amp; bridge</b><span>Infill lots and homes bought at land value, closing on short timelines.</span></div>
      <div><b>Entitlement refinance</b><span>Refinancing entitled land with interest reserves through permit issuance.</span></div>
      <div><b>Ground-up construction</b><span>SB&nbsp;684 and SB&nbsp;1123 small-lot homes, five to ten fee-simple units per site.</span></div>
      <div><b>Luxury remodels</b><span>Value-add single-family projects in Class&nbsp;A, A&minus; and B+ neighborhoods.</span></div>
      <div><b>Hillside &amp; new builds</b><span>Selective single-family construction in the Hills and on the Westside.</span></div>
      <div><b>Unit-release structures</b><span>Paydowns as individual homes sell, instead of a single bulk exit.</span></div>
    </div>
  </div>
</section>

<!-- PIPELINE -->
<section>
  <div class="wrap">
    <div class="split reveal" style="align-items:end;margin-bottom:2.4rem">
      <div>
        <p class="eyebrow">Current Pipeline</p>
        <h2 class="h-lg">Projects in Motion.</h2>
      </div>
      <p class="muted" style="max-width:34rem;margin:0">Our active SB&nbsp;684 projects in Culver City. <a href="portfolio.html" class="text-link-inline">All current projects &rarr;</a></p>
    </div>
    <div class="grid-4 reveal">
      <a class="photo-card" href="properties/the-culver-vi.html"><div class="frame"><span class="tag">Map Approved</span><img src="assets/img/westwood-hd.jpg" alt="The Culver VI conceptual rendering" loading="lazy"></div><div class="meta"><div class="name">The Culver VI</div><div class="sub">3850 Westwood Blvd &middot; 6 homes</div></div></a>
      <a class="photo-card" href="properties/the-harter-v.html"><div class="frame"><span class="tag">In Entitlement</span><img src="assets/img/harter-hd.jpg" alt="The Harter V conceptual rendering" loading="lazy"></div><div class="meta"><div class="name">The Harter V</div><div class="sub">4058 Harter Ave &middot; 5 homes</div></div></a>
      <a class="photo-card" href="properties/the-helms-vi.html"><div class="frame"><span class="tag">Map Filed</span><img src="assets/img/helms-hd.jpg" alt="The Helms VI conceptual rendering" loading="lazy"></div><div class="meta"><div class="name">The Helms VI</div><div class="sub">3562 Helms Ave &middot; 6 homes</div></div></a>
      <a class="photo-card" href="properties/the-sentney-vi.html"><div class="frame"><span class="tag">In Escrow</span><img src="assets/img/sentney-wide.jpg" alt="The Sentney VI conceptual aerial rendering" loading="lazy"></div><div class="meta"><div class="name">The Sentney VI</div><div class="sub">3011 Sentney Ave &middot; 6 homes</div></div></a>
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section class="on-warm">
  <div class="wrap">
    <div class="reveal" style="margin-bottom:2.4rem">
      <p class="eyebrow">Working Together</p>
      <h2 class="h-lg">From Intro to Final Draw.</h2>
    </div>
    <div class="steps4 reveal">
      <div><span>01</span><b>Intro call</b><p>We walk through your programs, leverage, pricing and the markets you lend in.</p></div>
      <div><span>02</span><b>Sponsor package</b><p>Track record, schedule of real estate owned and personal financial statements for the guarantors.</p></div>
      <div><span>03</span><b>Deal package</b><p>Contract, plans and entitlement status, budget, schedule and comparable sales for each loan.</p></div>
      <div><span>04</span><b>Close &amp; draw</b><p>Monthly draw requests, site inspections and straightforward reporting through payoff.</p></div>
    </div>
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
