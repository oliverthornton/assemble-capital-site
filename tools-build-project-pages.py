#!/usr/bin/env python3
"""Build the four active SB 684 project pages (properties/the-*.html).

    python3 tools-build-project-pages.py

Shell (head, header, footer) is borrowed from properties/gonzaga-residence.html so nav,
footer and asset versions stay in sync. Edit PROJECTS below, then re-run. No returns,
projections or offering terms belong on these pages (Rule 506(b)).
"""
import html as H
import json
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://assemble.capital/"

INTERIORS = [  # (file stem, label, floor)
    ("kitchen", "Kitchen", "First floor"), ("living", "Living", "First floor"), ("powder", "Powder room", "First floor"),
    ("bedroom-1", "Bedroom 1", "Second floor"), ("bath-1", "Bath 1", "Second floor"),
    ("bedroom-2", "Bedroom 2", "Second floor"), ("bath-2", "Bath 2", "Second floor"),
    ("primary-bedroom", "Primary bedroom", "Third floor"), ("primary-bath", "Primary bath", "Third floor"),
    ("closet", "Walk-in closet", "Third floor"), ("rooftop-deck", "Rooftop deck", "Roof"),
]

PROJECTS = [
    dict(
        slug="the-culver-vi", name="The Culver VI", addr="3850 Westwood Blvd", entity="AC III LLC",
        hero="westwood-hd.jpg", hero_alt="Conceptual exterior rendering of The Culver VI, six fee-simple homes at 3850 Westwood Blvd, Culver City",
        status="Tentative map approved", homes="6",
        ledger=[("6", "Fee-simple homes"), ("3 / 3.5", "Bedrooms / baths (concept)"), ("Approved", "Tentative tract map"), ("Q4 2027", "Target sellout (est.)")],
        lede="Six new fee-simple homes on a single Culver City lot, and the first SB&nbsp;684 tentative map approval in the city.",
        body=[
            "The Culver VI turns one infill lot on Westwood Boulevard into six homes, each on its own legal parcel and each sold individually, like a single-family home, with no HOA. It is Assemble Capital&rsquo;s first SB&nbsp;684 project and, to our knowledge, the first SB&nbsp;684 tentative tract map approved in Culver City.",
            "The project has refinanced into its construction loan and is working through final map and plan check toward ready-to-issue permits. Construction is expected to begin in January 2027 (est.).",
        ],
        highlights=[
            ("First in Culver City", "To our knowledge, the first SB&nbsp;684 tentative tract map approved in the city."),
            ("Six homes, six parcels", "Fee-simple ownership: buyers own their home and the land under it, with no HOA."),
            ("Three levels plus a roof deck", "Concept plan of three bedrooms and three and a half baths, a primary-suite balcony and a private rooftop deck."),
            ("Construction financing in place", "Refinanced into the construction loan; personally guaranteed by the principals, never by investors."),
        ],
        specs=[("Address", "3850 Westwood Blvd, Culver City, CA"), ("Ownership entity", "AC III LLC"),
               ("Program", "6 fee-simple homes on individual parcels"), ("Pathway", "SB&nbsp;684 ministerial small-lot subdivision"),
               ("Home concept", "3 stories &middot; 3 bedrooms &middot; 3.5 baths &middot; balcony &middot; private roof deck"),
               ("First floor", "Kitchen, living, dining, powder room"), ("Second floor", "Two bedrooms, each with a bath"),
               ("Third floor", "Primary suite with walk-in closet and balcony"),
               ("Developer &amp; builder", "Thornton Development Group"), ("Status", "Tentative tract map approved; final map and permits in progress"),
               ("Construction start", "January 2027 (est.)"), ("Target sellout", "Q4 2027 (est.)")],
        stage=2, gallery_ext=[("westwood-hd.jpg", "Exterior concept")], interiors=True,
    ),
    dict(
        slug="the-harter-v", name="The Harter V", addr="4058 Harter Ave", entity="AC VI LLC",
        hero="harter-hd.jpg", hero_alt="Conceptual exterior rendering of The Harter V, five fee-simple homes at 4058 Harter Ave, Culver City",
        status="In entitlement", homes="5",
        ledger=[("5", "Fee-simple homes"), ("SB 684", "Ministerial pathway"), ("In entitlement", "Current stage"), ("Q1 2028", "Target sellout (est.)")],
        lede="Five fee-simple homes on a Culver City flats lot, following the playbook proven at The Culver VI.",
        body=[
            "The Harter V subdivides one Culver City lot into five homes, each on its own parcel and sold individually with no HOA. It runs the same SB&nbsp;684 sequence, with the same architect and the same development team, as The Culver VI.",
            "The project is in entitlement. Our SB&nbsp;684 projects have taken about 12 months from entitlement start to ready-to-issue permits, trending toward 9 to 10.",
        ],
        highlights=[
            ("Five homes, five parcels", "Fee-simple ownership with no HOA, priced for owner-occupant buyers."),
            ("Repeatable playbook", "Same ministerial pathway, architect and team as The Culver VI and The Helms VI."),
            ("Culver City flats", "A flat infill lot in a city with strong owner-occupant demand."),
            ("Shared design concept", "Organic-modern interiors and private rooftop decks; final plans in progress."),
        ],
        specs=[("Address", "4058 Harter Ave, Culver City, CA"), ("Ownership entity", "AC VI LLC"),
               ("Program", "5 fee-simple homes on individual parcels"), ("Pathway", "SB&nbsp;684 ministerial small-lot subdivision"),
               ("Design", "Shared organic-modern concept; final plans in progress"),
               ("Developer &amp; builder", "Thornton Development Group"), ("Status", "In entitlement"),
               ("Target sellout", "Q1 2028 (est.)")],
        stage=1, gallery_ext=[("harter-hd.jpg", "Exterior concept")], interiors=True,
    ),
    dict(
        slug="the-helms-vi", name="The Helms VI", addr="3562 Helms Ave", entity="AC VII LLC",
        hero="helms-hd.jpg", hero_alt="Conceptual exterior rendering of The Helms VI, six fee-simple homes at 3562 Helms Ave, Culver City",
        status="Tract map filed", homes="6",
        ledger=[("6", "Fee-simple homes"), ("SB 684", "Ministerial pathway"), ("Map filed", "Current stage"), ("Q1 2028", "Target sellout (est.)")],
        lede="Six fee-simple homes on a Culver City flats lot, with its tentative tract map filed.",
        body=[
            "The Helms VI subdivides one Culver City lot into six homes, each on its own parcel and sold individually with no HOA. It follows the same SB&nbsp;684 sequence, with the same architect and development team, as The Culver VI and The Harter V.",
            "The tentative tract map has been filed. Our SB&nbsp;684 projects have taken about 12 months from entitlement start to ready-to-issue permits, trending toward 9 to 10.",
        ],
        highlights=[
            ("Six homes, six parcels", "Fee-simple ownership with no HOA, priced for owner-occupant buyers."),
            ("Tract map filed", "Moving through the ministerial SB&nbsp;684 approval pathway."),
            ("Culver City flats", "A flat infill lot in a city with strong owner-occupant demand."),
            ("Shared design concept", "Organic-modern interiors and private rooftop decks; final plans in progress."),
        ],
        specs=[("Address", "3562 Helms Ave, Culver City, CA"), ("Ownership entity", "AC VII LLC"),
               ("Program", "6 fee-simple homes on individual parcels"), ("Pathway", "SB&nbsp;684 ministerial small-lot subdivision"),
               ("Design", "Shared organic-modern concept; final plans in progress"),
               ("Developer &amp; builder", "Thornton Development Group"), ("Status", "Tentative tract map filed"),
               ("Target sellout", "Q1 2028 (est.)")],
        stage=1, gallery_ext=[("helms-hd.jpg", "Exterior concept")], interiors=True,
    ),
    dict(
        slug="the-sentney-vi", name="The Sentney VI", addr="3011 Sentney Ave", entity="AC VIII LLC",
        hero="sentney-aerial.jpg", hero_pos="center 62%", hero_alt="Conceptual aerial rendering of The Sentney VI, six fee-simple homes at 3011 Sentney Ave, Culver City",
        status="In escrow", homes="6",
        ledger=[("6", "Fee-simple homes"), ("~1,300", "Square feet per home"), ("5,401", "Lot square feet"), ("In escrow", "Current stage")],
        lede="Six three-story homes on a 5,401&nbsp;square foot Culver City lot, the fourth run of our SB&nbsp;684 playbook.",
        body=[
            "The Sentney VI is planned as six new fee-simple homes of about 1,300 square feet each across three stories, every one with a private rooftop deck. Each home will sit on its own parcel and sell individually, like a single-family home, with no HOA.",
            "The property is in escrow, with closing expected in Q4 2026. It may not close. If it does, it will be the fourth time the team has run the ministerial SB&nbsp;684 playbook in Culver City, with the same architect and the same sequence as The Culver VI, The Harter V and The Helms VI.",
        ],
        highlights=[
            ("Six homes, six parcels", "Fee-simple ownership with no HOA, priced for owner-occupant buyers."),
            ("Three stories, private roof decks", "About 1,300 square feet per home, with outdoor living one floor up."),
            ("Fourth in the series", "Same ministerial pathway, architect and team as our three Culver City SB&nbsp;684 projects."),
            ("Shared design concept", "Organic-modern interiors with warm wood, natural stone and soft light."),
        ],
        specs=[("Address", "3011 Sentney Ave, Culver City, CA"), ("Ownership entity", "AC VIII LLC"),
               ("Lot size", "5,401 square feet"), ("Program", "6 fee-simple homes on individual parcels"),
               ("Home concept", "3 stories &middot; about 1,300 square feet &middot; private roof deck"),
               ("Pathway", "SB&nbsp;684 ministerial small-lot subdivision"),
               ("Developer &amp; builder", "Thornton Development Group"), ("Status", "In escrow; closing expected Q4 2026 (may not close)"),
               ("Target sellout", "2029 (est.)")],
        stage=0, gallery_ext=[("sentney-aerial.jpg", "Aerial concept"), ("sentney-rooftop.jpg", "Rooftop concept")], interiors=True,
    ),
]

STAGES = ["Acquisition", "Entitlement", "Permits (RTI)", "Construction", "Sellout"]

CULVER = [
    ("A city of its own", "About five square miles and roughly 40,000 residents, surrounded by Los&nbsp;Angeles&rsquo; Westside, with its own city hall, police, fire and planning department."),
    ("Studios and offices", "Home to Sony Pictures Studios and Amazon MGM Studios, with media and tech offices across downtown and the Hayden Tract."),
    ("Schools", "Served by Culver City Unified School District, a draw for the owner-occupant buyers these homes are designed for."),
    ("Getting around", "Metro&rsquo;s E Line stops in Culver City, the Ballona Creek bike path runs to the coast, and Santa Monica, Downtown and LAX are all close."),
    ("Downtown Culver City", "A walkable core of restaurants, theaters and the Culver Steps, with the Baldwin Hills Scenic Overlook nearby."),
    ("No Measure ULA", "Culver City is outside the City of Los&nbsp;Angeles, so LA&rsquo;s Measure ULA transfer tax does not apply. Culver City has its own transfer tax."),
]


def shell():
    s = open("properties/gonzaga-residence.html").read()
    a = s.index('<main id="main">')
    b = s.index("</main>") + len("</main>")
    return s[:a], s[b:]


def head(top, p):
    title = f"{p['name']} | {p['addr']}, Culver City | Assemble Capital"
    desc = (f"{p['name']} at {p['addr']}, Culver City: {p['homes']} new fee-simple homes under SB 684 by Assemble Capital. "
            f"Highlights, specs, design concepts and the Culver City market.")
    url = f"{SITE}properties/{p['slug']}.html"
    img = f"{SITE}assets/img/{p['hero']}"
    alt = H.escape(p["hero_alt"], quote=True)
    t = top
    t = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", t)
    for k in ("description", "og:description", "twitter:description"):
        t = re.sub(rf'(<meta (?:name|property)="{k}" content=")[^"]*"', rf'\g<1>{desc}"', t)
    for k in ("og:title", "twitter:title"):
        t = re.sub(rf'(<meta (?:name|property)="{k}" content=")[^"]*"', rf'\g<1>{title}"', t)
    for k in ("og:image", "twitter:image"):
        t = re.sub(rf'(<meta (?:name|property)="{k}" content=")[^"]*"', rf'\g<1>{img}"', t)
    for k in ("og:image:alt", "twitter:image:alt"):
        t = re.sub(rf'(<meta (?:name|property)="{k}" content=")[^"]*"', rf'\g<1>{alt}"', t)
    t = re.sub(r'<meta property="og:image:(width|height)" content="\d+">\n', "", t)
    t = re.sub(r'(<link rel="canonical" href=")[^"]*"', rf'\g<1>{url}"', t)
    t = re.sub(r'(<meta property="og:url" content=")[^"]*"', rf'\g<1>{url}"', t)
    t = re.sub(r'(<link rel="preload" as="image" href=")[^"]*"', rf'\g<1>../assets/img/{p["hero"]}"', t)
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": f"{p['name']} | {p['addr']}, Culver City",
          "description": desc, "url": url,
          "primaryImageOfPage": {"@type": "ImageObject", "url": img, "caption": p["hero_alt"]},
          "about": {"@type": "Residence", "name": p["name"],
                    "address": {"@type": "PostalAddress", "streetAddress": p["addr"], "addressLocality": "Culver City",
                                "addressRegion": "CA", "addressCountry": "US"}},
          "isPartOf": {"@type": "WebSite", "name": "Assemble Capital", "url": SITE},
          "publisher": {"@type": "Organization", "name": "Assemble Capital", "url": SITE}}
    t = re.sub(r'<script type="application/ld\+json" data-seo="auto">\s*\{\s*"@context": "https://schema.org",\s*"@type": "WebPage".*?</script>',
               lambda m: '<script type="application/ld+json" data-seo="auto">\n' + json.dumps(ld, indent=2, ensure_ascii=False) + "\n</script>", t, count=1, flags=re.S)
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": "Current Projects", "item": SITE + "portfolio.html"},
        {"@type": "ListItem", "position": 3, "name": p["name"], "item": url}]}
    t = re.sub(r'<script type="application/ld\+json" data-seo="auto">\s*\{\s*"@context": "https://schema.org",\s*"@type": "BreadcrumbList".*?</script>',
               lambda m: '<script type="application/ld+json" data-seo="auto">\n' + json.dumps(bc, indent=2, ensure_ascii=False) + "\n</script>", t, count=1, flags=re.S)
    return t


def gallery(p):
    items = [(f"../assets/img/{f}", f"../assets/img/{f}", f"{p['name']}: {lab.lower()} (conceptual rendering)") for f, lab in p["gallery_ext"]]
    if p["interiors"]:
        items += [(f"../assets/img/concepts/sb684-{k}.jpg", f"../assets/img/concepts/thumbs/sb684-{k}.jpg",
                   f"Interior concept: {lab.lower()}, {fl.lower()}") for k, lab, fl in INTERIORS]
    n = len(items)
    btns = "\n".join(f'        <button type="button" data-full="{full}" aria-label="View image {i} of {n}"><img src="{th}" alt="{H.escape(alt, quote=True)}" loading="lazy"></button>'
                     for i, (full, th, alt) in enumerate(items, 1))
    return n, btns


def main_html(p, prev, nxt):
    ledger = "\n".join(f'      <div class="cell"><div class="num">{a}</div><div class="lbl">{b}</div></div>' for a, b in p["ledger"])
    body = "\n".join(f"      <p>{x}</p>" for x in p["body"])
    hl = "\n".join(f'      <div class="hl"><h3>{a}</h3><p>{b}</p></div>' for a, b in p["highlights"])
    specs = "\n".join(f"        <div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in p["specs"])
    steps = "".join(f'<li class="{"done" if i < p["stage"] else "now" if i == p["stage"] else ""}"><span>{s}</span></li>' for i, s in enumerate(STAGES))
    n, btns = gallery(p)
    culver = "\n".join(f'      <div><b>{a}</b><span>{b}</span></div>' for a, b in CULVER)
    return f'''<main id="main">

<section class="hero short" style="padding:0">
  <div class="bg" style="background-image:url('../assets/img/{p['hero']}');background-position:{p.get('hero_pos','center')}" role="img" aria-label="{H.escape(p['hero_alt'], quote=True)}"></div>
  <div class="wrap">
    <p class="eyebrow">SB&nbsp;684 Small-Lot Homes &middot; Culver City</p>
    <h1 class="display">{p['name']}</h1>
    <p class="sub">{p['addr']} &middot; {p['entity']} &middot; {p['status']}</p>
  </div>
</section>

<!-- HEADLINE STATS -->
<section>
  <div class="wrap">
    <div class="ledger reveal">
{ledger}
    </div>
    <ol class="stage-track reveal" aria-label="Project stage">{steps}</ol>
  </div>
</section>

<!-- OVERVIEW -->
<section class="on-warm">
  <div class="wrap split reveal">
    <div>
      <p class="eyebrow">The Project</p>
      <p class="lede">{p['lede']}</p>
    </div>
    <div>
{body}
    </div>
  </div>
</section>

<!-- HIGHLIGHTS + SPECS -->
<section>
  <div class="wrap">
    <div class="reveal" style="margin-bottom:2.2rem">
      <p class="eyebrow">Highlights</p>
      <h2 class="h-lg">Why It Works.</h2>
    </div>
    <div class="hl-grid reveal">
{hl}
    </div>
    <div class="split reveal" style="align-items:start;margin-top:4rem">
      <div>
        <p class="eyebrow">Specifications</p>
        <h2 class="h-lg">The Details.</h2>
        <p class="muted" style="max-width:26rem">Plans are conceptual and may change through entitlement, plan check and construction.</p>
      </div>
      <dl class="spec-list">
{specs}
      </dl>
    </div>
  </div>
</section>

<!-- GALLERY -->
<section class="on-warm">
  <div class="wrap">
    <div class="reveal" style="display:flex;flex-wrap:wrap;align-items:end;justify-content:space-between;gap:1.5rem;margin-bottom:2.2rem">
      <div>
        <p class="eyebrow">Design Concepts</p>
        <h2 class="h-lg">Inside the Homes.</h2>
        <p class="muted" style="max-width:38rem;margin:.8rem 0 0">Organic-modern and earthy: light oak cabinetry and floors, travertine- and limestone-toned stone, soft plaster walls, matte black fixtures and layered, warm light, with a private rooftop deck for outdoor living.</p>
      </div>
      <span class="stamp">{n} conceptual renderings</span>
    </div>
    <div class="gallery reveal">
{btns}
    </div>
    <p class="footnote reveal" style="margin-top:1.4rem">Conceptual renderings for illustration only. Interiors show a shared design concept used across our Culver City SB&nbsp;684 projects; final plans, layouts, square footage, finishes, fixtures, landscaping and amenities will vary by project and home and are subject to change. Furniture and d&eacute;cor are not included.</p>
  </div>
</section>

<div class="lightbox" role="dialog" aria-modal="true" aria-label="Rendering viewer">
  <button class="lb-close" type="button" aria-label="Close viewer">&#10005;</button>
  <button class="lb-prev" type="button" aria-label="Previous image">&larr;</button>
  <img alt="">
  <button class="lb-next" type="button" aria-label="Next image">&rarr;</button>
  <span class="lb-count"></span>
</div>

<!-- CULVER CITY -->
<section class="on-dark">
  <div class="wrap">
    <div class="split reveal" style="align-items:end;margin-bottom:2.4rem">
      <div>
        <p class="eyebrow">The Location</p>
        <h2 class="h-lg">Why Culver City.</h2>
      </div>
      <p class="muted" style="max-width:34rem;margin:0">One of the most active places in Los&nbsp;Angeles County for SB&nbsp;684: multifamily-zoned blocks in the flats, strong owner-occupant demand, and a location between the Westside and Downtown. <a href="../blog/sb-684-culver-city.html" class="text-link-inline">SB&nbsp;684 in Culver City &rarr;</a></p>
    </div>
    <div class="finish-grid city-grid reveal">
{culver}
    </div>
  </div>
</section>

<!-- CTA -->
<section class="cta-band on-warm">
  <div class="wrap reveal">
    <p class="eyebrow">Investor Relationships</p>
    <h2 class="h-lg">Interested in How We Work?</h2>
    <p class="muted" style="max-width:40rem;margin:1.4rem auto 0">We develop Los Angeles residential projects alongside investors we know well, and the principals personally guarantee the project loans, never our investors. Project financials are shared privately, through each offering&rsquo;s documents.</p>
    <div class="actions">
      <a class="btn" style="border-color:var(--line-strong)" href="../contact.html#inquiry" data-schedule>Schedule an intro call</a>
      <a class="btn" style="border-color:var(--line-strong)" href="../investors.html">How we work with investors</a>
    </div>
    <p class="footnote" style="max-width:44rem;margin:2rem auto 0">This page is for informational purposes only and is not an offer to sell or a solicitation of an offer to buy any security. Target dates are estimates, not commitments. Stages reflect the project as of October 2026. See <a href="../disclosures.html">Risks &amp; Disclosures</a>.</p>
  </div>
</section>

<!-- PREV / NEXT -->
<nav class="pn-nav" aria-label="Project navigation">
  <a class="prev" href="{prev['slug']}.html"><span class="k">&larr; Previous</span><span class="n">{prev['name']}</span></a>
  <a class="next" href="{nxt['slug']}.html"><span class="k">Next &rarr;</span><span class="n">{nxt['name']}</span></a>
</nav>

</main>'''


def build():
    top, bottom = shell()
    for i, p in enumerate(PROJECTS):
        prev, nxt = PROJECTS[i - 1], PROJECTS[(i + 1) % len(PROJECTS)]
        open(f"properties/{p['slug']}.html", "w").write(head(top, p) + main_html(p, prev, nxt) + bottom)
        print("wrote", p["slug"])


if __name__ == "__main__":
    build()
