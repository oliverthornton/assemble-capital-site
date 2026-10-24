#!/usr/bin/env python3
"""Branded 1200x630 link-preview cards for every page, plus their og/twitter tags.

    python3 tools-generate-share-cards.py            # render cards + update tags
    python3 tools-generate-share-cards.py --tags     # only rewrite tags

Cards land in assets/img/social/cards/<name>.jpg. Rendering uses headless Chrome
(fonts load from Google Fonts, so it needs a network connection).
"""
import html as H
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
IMG = os.path.join(ROOT, "assets/img")
OUT = "assets/img/social/cards"
SITE = "https://assemble.capital/"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

TDG = "Principals&rsquo; Track Record"
AC = "Assemble Capital Project"

# page -> (card name, background, eyebrow, headline, sub)
PAGES = {
    "index.html": ("home", "sb684-hero.jpg", "Los Angeles Infill Development",
                   "Real Estate Syndication &amp; <em>Development</em>",
                   "SB&nbsp;684 / SB&nbsp;1123 Small-Lot Homes &nbsp;&middot;&nbsp; Luxury Residential"),
    "about.html": ("about", "social/about-1200x630.jpg", "About Assemble Capital",
                   "The Firm &amp; Its <em>Principals</em>",
                   "A Los Angeles real estate syndication and development firm"),
    "strategies.html": ("strategies", "social/strategies-1200x630.jpg", "Investment Strategies",
                        "Value-Add &amp; <em>Opportunistic</em>",
                        "SB&nbsp;684 / SB&nbsp;1123 &nbsp;&middot;&nbsp; Luxury Residential &nbsp;&middot;&nbsp; Multifamily &nbsp;&middot;&nbsp; TIC"),
    "strategies/infill-subdivisions.html": ("infill-subdivisions", "samo-ix-render.jpg", "Core Strategy",
                                            "SB&nbsp;684 &amp; SB&nbsp;1123 <em>Small-Lot Homes</em>",
                                            "Fee-simple homes on individual lots &nbsp;&middot;&nbsp; Westside infill"),
    "strategies/luxury-redevelopment.html": ("luxury-redevelopment", "social/luxury-redevelopment-1200x630.jpg", "Core Strategy",
                                             "Luxury Residential <em>Development</em>",
                                             "Hollywood Hills &nbsp;&middot;&nbsp; Westside &nbsp;&middot;&nbsp; Beverly Hills"),
    "strategies/boutique-multifamily.html": ("boutique-multifamily", "social/boutique-multifamily-1200x630.jpg", "Additional Strategy",
                                             "Boutique <em>Multifamily</em>",
                                             "Value-add small multifamily in Los Angeles"),
    "strategies/tic-housing.html": ("tic-housing", "social/tic-housing-1200x630.jpg", "Additional Strategy",
                                    "Tenancy-in-Common <em>Housing</em>",
                                    "Entry-level ownership on Los Angeles infill lots"),
    "portfolio.html": ("portfolio", "social/portfolio-1200x630.jpg", "Current Projects",
                       "Current Assemble Capital <em>Projects</em>",
                       "SB&nbsp;684 subdivisions &amp; residential development in Los Angeles"),
    "track-record.html": ("track-record", "social/track-record-1200x630.jpg", TDG,
                          "Completed Los Angeles <em>Projects</em>",
                          "Developed by the principals through Thornton Development Group"),
    "investors.html": ("investors", "social/about-1200x630.jpg", "For Investors",
                       "How We Work With <em>Investors</em>",
                       "Relationship first &nbsp;&middot;&nbsp; Passive ownership &nbsp;&middot;&nbsp; Loans guaranteed by the principals"),
    "contact.html": ("contact", "social/contact-1200x630.jpg", "Investor Relations",
                     "Start a <em>Conversation</em>",
                     "Talk with the principals about upcoming projects"),
    "submit-a-deal.html": ("submit-a-deal", "helms-render.jpg", "For Agents &amp; Wholesalers",
                           "Submit a <em>Deal</em>",
                           "SB&nbsp;684 infill lots &nbsp;&middot;&nbsp; Single-family remodels &nbsp;&middot;&nbsp; Reply within 48 hours"),
    "blog/index.html": ("insights", "social/insights-1200x630.jpg", "Insights",
                        "Notes on Syndication &amp; <em>Development</em>",
                        "Guides for investors from the Assemble Capital principals"),
    "glossary.html": ("glossary", "social/strategies-1200x630.jpg", "Investor Resources",
                      "Real Estate Investment <em>Glossary</em>",
                      "Plain definitions of syndication and development terms"),
    "disclosures.html": ("disclosures", "social/home-1200x630.jpg", "Legal",
                         "Risks &amp; <em>Disclosures</em>", "Read before considering any investment"),
    "privacy.html": ("privacy", "social/home-1200x630.jpg", "Legal",
                     "Privacy <em>Policy</em>", "How we handle the information you share with us"),
    "terms.html": ("terms", "social/home-1200x630.jpg", "Legal",
                   "Terms of <em>Service</em>", "Terms for using assemble.capital"),
}

AC_PROJECTS = {"gonzaga-residence", "berryman-residence"}

# Blog post -> background photo (the pages' og:image now points at the card itself).
BLOG_BG = {
    "10-red-flags-in-real-estate-offering-documents": "properties/paseo-moderna/01.jpg",
    "accredited-investor-requirements": "properties/hortense-vi/01.jpg",
    "exit-strategies-sell-lease-or-reinvest": "properties/martha-mcm/01.jpg",
    "general-partner-vs-limited-partner-in-a-syndication": "properties/modern-orange/01.jpg",
    "how-to-read-a-real-estate-offering-memorandum": "properties/hutton-marvel/01.jpg",
    "multifamily-vs-single-family-which-offers-better-returns": "properties/rising-glen-mcm/01.jpg",
    "passive-real-estate-investing-explained": "apex.webp",
    "real-estate-syndication-for-accredited-investors-los-angeles": "properties/hideaway-hh/01.jpg",
    "risk-vs-return-questions-to-ask-before-you-invest": "properties/hollywood-marvel/01.jpg",
    "sb-684-sb-1123-california-lot-split-guide": "samo-ix-render.jpg",
    "sb-684-vs-sb-9": "sb684-hero.jpg",
    "sb-1123-lot-split-requirements": "samo-ix-render.jpg",
    "selling-your-lot-to-an-sb-684-developer": "helms-render.jpg",
    "sb-684-vs-sb-1123-what-changed": "samo.webp",
    "tic-vs-condo-california": "properties/david-iii/02.jpg",
    "los-angeles-residential-entitlement-process": "westwood.jpg",
    "measure-ula-explained": "properties/apex-hh/01.jpg",
    "remodel-vs-new-construction-los-angeles": "berryman-home.jpg",
    "how-sb-684-construction-financing-works": "helms-render.jpg",
    "tenancy-in-common-los-angeles-explained": "david.webp",
    "timing-vs-time-in-market-for-private-real-estate": "properties/calvert-xiv/01.jpg",
    "understanding-downside-protection-in-private-deals": "properties/treehouse-hh/01.jpg",
    "what-makes-a-sponsor-worth-trusting": "properties/berryman-residence/01.jpg",
    "what-to-know-before-investing-in-a-private-placement": "properties/villa-de-edinburgh/01.jpg",
    "why-experience-matters-more-than-project-size": "properties/macapa-oasis/01.jpg",
    "why-projected-returns-matter-less-than-structure": "properties/villa-de-vistas/01.jpg",
    "why-vertical-integration-matters-in-development": "properties/june-iv/01.jpg",
}
DEFAULT_BLOG_BG = "social/insights-1200x630.jpg"

# Photos with a listing watermark in the bottom-right corner: zoom from the top-left to crop it out.
ZOOM = ("properties/hideaway-hh/",)


def attr(s, name):
    m = re.search(r'<meta (?:property|name)="%s" content="([^"]*)"' % re.escape(name), s)
    return m.group(1) if m else ""


def property_card(path, s):
    slug = os.path.basename(path)[:-5]
    name = re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S).group(1)).strip()
    words = name.split(" ", 1)
    head = f"{words[0]} <em>{words[1]}</em>" if words[0] == "The" and len(words) > 1 else f"<em>{name}</em>"
    kind = re.search(r'class="eyebrow">([^<]*)', s).group(1).strip()
    sub = re.search(r'<p class="sub">([^<]*)', s).group(1)
    parts = [p.strip() for p in sub.split("&middot;")]
    status = [p for p in parts[1:] if not re.search(r"\$|\d{4}|Units", p)]
    kind = kind.replace("adjacent", "Adjacent")
    line = " &nbsp;&middot;&nbsp; ".join([kind.replace(" &middot; ", " &nbsp;&middot;&nbsp; ")] + status)
    eyebrow = AC if slug in AC_PROJECTS else TDG
    return (f"properties/{slug}", f"properties/{slug}/01.jpg", eyebrow, head, line)


def blog_card(path, s):
    slug = os.path.basename(path)[:-5]
    title = re.sub(r"\s*&mdash;\s*Assemble Capital$", "", attr(s, "og:title"))
    bg = BLOG_BG.get(slug, DEFAULT_BLOG_BG)
    return (f"blog/{slug}", bg, "Insights", title, "Oliver Thornton &nbsp;&middot;&nbsp; Assemble Capital")


def cards():
    out = {}
    for page, card in PAGES.items():
        out[page] = card
    for f in sorted(os.listdir("properties")):
        if f.endswith(".html"):
            p = f"properties/{f}"
            out[p] = property_card(p, open(p).read())
    for f in sorted(os.listdir("blog")):
        if f.endswith(".html") and f != "index.html":
            p = f"blog/{f}"
            out[p] = blog_card(p, open(p).read())
    return out


TEMPLATE = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600&family=Cormorant+Garamond:ital,wght@0,500;1,500&display=swap" rel="stylesheet">
<style>
*{margin:0;box-sizing:border-box}
html,body{width:1200px;height:630px;overflow:hidden;background:#140f0f}
.bg{position:absolute;inset:0;background:url('%(bg)s') center/cover;transform-origin:0 0;%(zoom)s}
.fade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(20,15,15,.95) 0%%,rgba(20,15,15,.84) 44%%,rgba(20,15,15,.2) 76%%,rgba(20,15,15,0) 100%%)}
.col{position:absolute;left:64px;top:56px;bottom:56px;width:660px;display:flex;flex-direction:column}
.logo{width:250px;margin-left:-14px}
.text{margin-top:auto}
.eb{font:600 15px/1.2 Archivo;letter-spacing:.22em;text-transform:uppercase;color:#c9a97f}
h1{font:500 64px/1.04 "Cormorant Garamond";color:#f8f8f8;margin-top:18px;visibility:hidden}
h1 em{color:#d4b48a}
.sub{font:500 19px/1.4 Archivo;color:#e6e1da;margin-top:20px}
.url{font:600 16px/1 Archivo;letter-spacing:.14em;color:#c9a97f;text-transform:uppercase;margin-top:30px}
</style></head><body>
<div class="bg"></div><div class="fade"></div>
<div class="col"><img class="logo" src="%(logo)s">
<div class="text"><p class="eb">%(eb)s</p><h1 id="h">%(h)s</h1><p class="sub">%(sub)s</p><p class="url">assemble.capital</p></div></div>
<script>
document.fonts.ready.then(()=>{const h=document.getElementById('h');let s=64;
while(h.offsetHeight>200&&s>40){s-=2;h.style.fontSize=s+'px';}h.style.visibility='visible';});
</script></body></html>"""


def nowrap(head):
    # keep hyphenated words (Small-Lot, Time-in-Market) on one line
    return re.sub(r"(?<![<\w&])(\w+(?:-\w+)+)(?![^<]*>)", r'<span style="white-space:nowrap">\1</span>', head)


def render(name, bg, eb, head, sub, tmp):
    zoom = "transform:scale(1.12)" if bg.startswith(ZOOM) else ""
    src = os.path.join(IMG, bg)
    if src.endswith(".webp"):  # Chrome reads webp fine, but crop to a jpg for consistency
        jpg = os.path.join(tmp, os.path.basename(src) + ".jpg")
        Image.open(src).convert("RGB").save(jpg, quality=92)
        src = jpg
    page = os.path.join(tmp, name.replace("/", "_") + ".html")
    png = page[:-5] + ".png"
    open(page, "w").write(TEMPLATE % {"bg": "file://" + src, "logo": "file://" + os.path.join(IMG, "logo/lockup-white-v2.png"),
                                      "eb": eb, "h": nowrap(head), "sub": sub, "zoom": zoom})
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--virtual-time-budget=6000", "--window-size=1200,630", "--screenshot=" + png, "file://" + page],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    dest = os.path.join(OUT, name + ".jpg")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    Image.open(png).convert("RGB").save(dest, quality=86, optimize=True, progressive=True)
    return dest


def plain(x):
    return H.unescape(re.sub(r"<[^>]+>", "", x)).replace("\xa0", " ")


def set_tags(page, name, eb, head, sub):
    s = open(page).read()
    url = f"{SITE}{OUT}/{name}.jpg"
    alt = H.escape(f"{plain(eb)}: {plain(head)}. {plain(sub)}", quote=True).replace("&#x27;", "&rsquo;")
    for prop in ("og:image", "twitter:image"):
        kind = "property" if prop.startswith("og") else "name"
        tag = f'<meta {kind}="{prop}" content="{url}">'
        s, n = re.subn(rf'<meta {kind}="{prop}" content="[^"]*">', tag, s)
        assert n == 1, (page, prop)
        alt_tag = f'<meta {kind}="{prop}:alt" content="{alt}">'
        s, n = re.subn(rf'<meta {kind}="{prop}:alt" content="[^"]*">', alt_tag, s)
        if not n:
            s = s.replace(tag, tag + "\n" + alt_tag, 1)
    if 'og:image:width' not in s:
        tag = f'<meta property="og:image" content="{url}">'
        s = s.replace(tag, tag + '\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">', 1)
    open(page, "w").write(s)


if __name__ == "__main__":
    only_tags = "--tags" in sys.argv
    with tempfile.TemporaryDirectory() as tmp:
        for page, (name, bg, eb, head, sub) in cards().items():
            if not only_tags:
                render(name, bg, eb, head, sub, tmp)
            set_tags(page, name, eb, head, sub)
            print(f"{page:60s} -> {name}")
