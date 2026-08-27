#!/usr/bin/env python3
"""Generate the blog: an index page plus one page per published post.

Post data lives in blog/posts.json (NOT an inline Python list, unlike the
sibling generators) so a future content-writing agent can add a post by
editing JSON rather than editing Python source. See blog/README.md for the
field schema.

Only posts with status == "published" get a page; drafts are skipped
entirely. Pages are written flat as blog/<slug>.html (not year-nested) so
tools-add-analytics.py's one-directory-deep glob still reaches them.

    python3 tools-generate-blog-pages.py

Output: blog/index.html, blog/<slug>.html for each published post.
"""
import os, json
from datetime import datetime

SITE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SITE, "blog")
BASE_URL = "https://assemble.capital"

# ---------------------------------------------------------------- template bits
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
 '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&'
 'family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,500&family=Special+Elite&'
 'display=swap" rel="stylesheet">')
FAVICON = '<link rel="icon" href="../assets/img/logo/favicon-v2.png">'
MONO = '<img class="emblem" src="../assets/img/logo/emblem-white-v2.png" alt="" aria-hidden="true">'
LOGO_PATH = "assets/img/logo/lockup-codgray-v2.png"  # used as the JSON-LD publisher logo

# GA4 tag — built via plain string concatenation, NOT as one f-string with the
# literal `{dataLayer.push(arguments);}` inline. That exact mistake (a JS
# snippet's literal braces breaking an f-string parser) already happened once
# on a sibling repo. Keeping this as its own pre-rendered string means the
# braces below are just characters in a value, not f-string template syntax,
# so it's always safe to drop {GA4} into a later f-string.
MEASUREMENT_ID = "G-676QQYXN22"
GA4 = ('<!-- Google tag (gtag.js) -->\n'
 f'<script async src="https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}"></script>\n'
 '<script>\n'
 '  window.dataLayer = window.dataLayer || [];\n'
 '  function gtag(){dataLayer.push(arguments);}\n'
 "  gtag('js', new Date());\n"
 f"  gtag('config', '{MEASUREMENT_ID}');\n"
 '</script>')

def header(base=".."):
    return f'''<header class="site-head">
  <div class="bar">
    <a class="lockup" href="/" aria-label="Assemble Capital home">
      {MONO}
      <span class="word">Assemble<br>Capital</span>
    </a>
    <button class="menu-btn" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="site-nav" id="site-nav" aria-label="Primary">
      <a href="{base}/about.html">About</a>
      <div class="nav-dd">
        <a href="{base}/strategies.html" class="nav-dd-toggle">Strategies</a>
        <div class="nav-dd-menu">
          <a href="{base}/strategies/luxury-redevelopment.html">Luxury Residential Development</a>
          <a href="{base}/strategies/boutique-multifamily.html">Opportunistic &amp; Value Add Multifamily Development</a>
          <a href="{base}/strategies/infill-subdivisions.html">SB 684/1123 Fee Simple Subdivisions</a>
          <a href="{base}/strategies/tic-housing.html">Tenancy-In-Common Housing</a>
        </div>
      </div>
      <a href="{base}/portfolio.html">Current Projects</a>
      <a href="{base}/track-record.html">Track Record</a>
      <a href="{base}/contact.html">Contact</a>
      <a class="portal" href="https://assemblecapital.cashflowportal.com" target="_blank" rel="noopener">Investor Portal&nbsp;&#8599;</a>
    </nav>
  </div>
</header>'''

# footer comes from the single source of truth so it stays in sync sitewide
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("_footer", os.path.join(SITE, "tools-rebuild-footer.py"))
_fm = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_fm)

def footer():
    return _fm.build("../")

# ---------------------------------------------------------------- data
def load_posts():
    with open(os.path.join(OUT, "posts.json")) as fh:
        data = json.load(fh)
    return data

def parse_date(date_str):
    """'November 28, 2025' -> datetime. Raises on malformed input — a bad
    date in posts.json should fail loudly rather than silently mis-sort."""
    return datetime.strptime(date_str, "%B %d, %Y")

def published_sorted(posts):
    pub = [p for p in posts if p.get("status") == "published"]
    pub.sort(key=lambda p: parse_date(p["date"]), reverse=True)
    return pub

# ---------------------------------------------------------------- JSON-LD


# Posts that cite project-level results carry the same adjacent attribution the
# property pages use. The global legal footer alone leaves a reader to connect
# figures on an Assemble Capital domain to Assemble Capital offerings.
PROJECT_ATTRIBUTION = (
    '<p class="footnote" style="margin-top:2rem">Project results referenced in this article were '
    'achieved by the principals through Thornton Development Group and affiliated entities. '
    'Thornton Development Group is a separate company; Assemble Capital contracts with it for '
    'development execution. These projects were not Assemble Capital offerings and did not involve '
    'Assemble Capital investors. Figures are sponsor-level, unaudited, and drawn from internal '
    'records. Past performance is not indicative of future results.</p>'
)


def attribution_for(p):
    return PROJECT_ATTRIBUTION if p.get("project_attribution") else ""


def faq_jsonld(p):
    """FAQPage markup from the post's `faq` list, or "" when it has none."""
    items = p.get("faq") or []
    if not items:
        return ""
    obj = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": it["q"],
             "acceptedAnswer": {"@type": "Answer", "text": it["a"]}}
            for it in items
        ],
    }
    return ('\n<script type="application/ld+json">\n'
            + json.dumps(obj, indent=2) + "\n</script>")


def jsonld_for(p, canonical_url, abs_image_url, abs_logo_url, iso_date):
    data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": p["title"],
        "description": p["meta_description"],
        "image": abs_image_url,
        "datePublished": iso_date,
        "dateModified": iso_date,
        "author": {"@type": "Organization", "name": "Assemble Capital"},
        "publisher": {
            "@type": "Organization",
            "name": "Assemble Capital",
            "logo": {"@type": "ImageObject", "url": abs_logo_url},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical_url},
    }
    # json.dumps() into its own string FIRST, then only the resulting
    # variable name is interpolated into the page f-string below — never
    # literal JSON-looking braces typed directly into an f-string body.
    return json.dumps(data, indent=2)

# ---------------------------------------------------------------- post page
def build_post(p):
    slug = p["slug"]
    title = p["title"]
    desc = p["meta_description"]
    hero = p["hero_image"]
    date_str = p["date"]
    iso_date = parse_date(date_str).strftime("%Y-%m-%d")
    canonical_url = f"{BASE_URL}/blog/{slug}.html"
    abs_image_url = f"{BASE_URL}/{hero}"
    abs_logo_url = f"{BASE_URL}/{LOGO_PATH}"
    jsonld_str = jsonld_for(p, canonical_url, abs_image_url, abs_logo_url, iso_date)
    faq_str = faq_jsonld(p)
    attribution_str = attribution_for(p)

    category = p.get("category")
    eyebrow = category if category else "Insights"
    author = p.get("author", "Assemble Capital")

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &mdash; Assemble Capital</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical_url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Assemble Capital">
<meta property="og:url" content="{canonical_url}">
<meta property="og:title" content="{title} &mdash; Assemble Capital">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{abs_image_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Los Angeles residential development project photograph accompanying &ldquo;{title}&rdquo;">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} &mdash; Assemble Capital">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{abs_image_url}">
<meta name="twitter:image:alt" content="Los Angeles residential development project photograph accompanying &ldquo;{title}&rdquo;">
{FONTS}
<link rel="stylesheet" href="../css/style.css?v=3">
{FAVICON}
<script type="application/ld+json">
{jsonld_str}
</script>{faq_str}
{GA4}
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>

{header()}

<main id="main">

<section class="hero short" style="padding:0">
  <div class="bg" style="background-image:url('../{hero}')"></div>
  <div class="wrap">
    <p class="eyebrow">{eyebrow}</p>
    <h1 class="display">{title}</h1>
    <p class="sub">{author} &middot; {date_str}</p>
  </div>
</section>

<section>
  <div class="wrap" style="max-width:46rem">
{p["body_html"]}
{attribution_str}
    <p class="footnote" style="margin-top:2.4rem;padding-top:1.6rem;border-top:1px solid var(--line)">This article is for general informational and educational purposes only. It is not, and should not be relied upon as, investment, legal, tax, or accounting advice, and it is not a recommendation or endorsement of any strategy or investment. Consult your own financial, tax, and legal advisors before making any investment decision. See our full <a href="../disclosures.html">Risk Disclosures</a> for additional information.</p>
  </div>
</section>

<section class="cta-band on-warm">
  <div class="wrap reveal">
    <p class="eyebrow">Future Opportunities</p>
    <h2 class="h-lg">Want to invest in the next one?</h2>
    <p class="muted" style="max-width:42rem;margin:1.4rem auto 0">Get in touch and we'll walk you through the model, the pipeline, and what a specific offering looks like.</p>
    <div class="actions">
      <a class="btn" style="border-color:var(--line-strong)" href="../contact.html">Contact us about investing</a>
      <a class="btn" style="border-color:var(--line-strong)" href="../blog/index.html">More insights</a>
    </div>
    <p class="footnote" style="margin-top:1.8rem;max-width:44rem;margin-left:auto;margin-right:auto">Contacting us is not an offer, commitment, or investment. Any offering is made only through definitive offering documents to eligible investors.</p>
  </div>
</section>

</main>

{footer()}

<script src="../js/main.js"></script>
</body>
</html>
'''

# ---------------------------------------------------------------- index page
def build_index(posts):
    if posts:
        cards = "\n".join(
            f'''      <a class="photo-card" href="{p["slug"]}.html">
        <div class="frame"><img src="../{p["hero_image"]}" alt="{p["title"]}" loading="lazy"></div>
        <div class="meta">
          <div class="name">{p["title"]}</div>
          <div class="sub">{p["date"]}</div>
          <p class="muted" style="font-size:.9rem;margin-top:.5rem">{p["meta_description"]}</p>
        </div>
      </a>'''
            for p in posts)
        grid = f'<div class="grid-3 reveal">\n{cards}\n    </div>'
    else:
        grid = ('<p class="muted reveal" style="max-width:36rem">'
                'New posts are on the way &mdash; check back soon.</p>')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Insights &mdash; Assemble Capital</title>
<meta name="description" content="Notes on Los Angeles residential investment, development, and syndication from the Assemble Capital team.">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Assemble Capital">
<meta property="og:url" content="{BASE_URL}/blog/index.html">
<meta property="og:title" content="Insights &mdash; Assemble Capital">
<meta property="og:description" content="Notes on Los Angeles residential investment, development, and syndication from the Assemble Capital team.">
<meta property="og:image" content="{BASE_URL}/{LOGO_PATH}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Insights &mdash; Assemble Capital">
<meta name="twitter:description" content="Notes on Los Angeles residential investment, development, and syndication from the Assemble Capital team.">
<meta name="twitter:image" content="{BASE_URL}/{LOGO_PATH}">
{FONTS}
<link rel="stylesheet" href="../css/style.css?v=3">
{FAVICON}
{GA4}
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>

{header()}

<main id="main">

<section class="hero short" style="padding:0">
  <div class="wrap">
    <p class="eyebrow">Insights</p>
    <h1 class="display">Notes from the field.</h1>
    <p class="sub">Perspective on Los Angeles residential investment, development, and syndication from the Assemble Capital team.</p>
  </div>
</section>

<section>
  <div class="wrap">
    {grid}
  </div>
</section>

</main>

{footer()}

<script src="../js/main.js"></script>
</body>
</html>
'''

# ---------------------------------------------------------------- write
if __name__ == "__main__":
    all_posts = load_posts()
    posts = published_sorted(all_posts)

    os.makedirs(OUT, exist_ok=True)

    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(build_index(posts))
    print("wrote blog/index.html")

    for p in posts:
        with open(os.path.join(OUT, p["slug"] + ".html"), "w") as f:
            f.write(build_post(p))
        print("wrote blog/" + p["slug"] + ".html")

    skipped = len(all_posts) - len(posts)
    print(f"TOTAL {len(posts)} published post(s) generated"
          + (f", {skipped} draft(s) skipped" if skipped else ""))
