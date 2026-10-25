#!/usr/bin/env python3
"""Rebuild blog/index.html topic sections, the Blog JSON-LD and categories in blog/posts.json
from the post pages themselves.

    python3 tools-build-blog-index.py

New posts are picked up automatically. Assign a post to a topic in LUXURY / TIC / SB684 below;
anything starting with sb-684 or sb-1123 is SB 684, and everything else falls under Investing.
"""
import datetime, glob, html as H, json, os, re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

LUXURY = {
    "remodel-vs-new-construction-los-angeles", "hillside-development-costs-los-angeles", "measure-ula-explained",
    "adding-square-footage-luxury-remodel", "designing-a-remodel-for-westside-buyers", "how-we-underwrite-a-luxury-remodel",
    "what-makes-a-neighborhood-class-a", "selling-your-home-to-a-luxury-developer", "luxury-remodel-timeline-los-angeles",
    "hidden-costs-luxury-remodel-los-angeles", "how-luxury-flips-sell-los-angeles", "luxury-markets-outside-measure-ula",
    "hollywood-hills-vs-westside-luxury",
}
TIC = {"tenancy-in-common-los-angeles-explained", "tic-vs-condo-california", "multifamily-vs-single-family-which-offers-better-returns"}
SB684 = {
    "what-is-the-starter-home-revitalization-act", "selling-your-lot-to-an-sb-684-developer", "how-to-spot-an-sb-684-lot",
    "what-happens-at-a-final-map", "how-fee-simple-small-lot-homes-are-priced", "ellis-act-tenant-history-sb-684",
    "sell-or-develop-sb-684-owners-guide", "how-sb-684-construction-financing-works", "los-angeles-residential-entitlement-process",
}
CATS = [
    ("sb684", "SB 684 &amp; SB 1123", "Small-Lot Homes", "How California&rsquo;s small-lot laws work, which sites qualify, and what owners, agents and investors should know.", "sb-684-sb-1123-california-lot-split-guide"),
    ("luxury", "Luxury Residential", "Remodels &amp; Fix-and-Flips", "Underwriting, design, timelines, hidden costs and Measure ULA for luxury remodels in Los&nbsp;Angeles.", "how-we-underwrite-a-luxury-remodel"),
    ("tic", "TIC &amp; Multifamily", "Shared Ownership", "Tenancy in common, condos and small multifamily in California.", None),
    ("investing", "Investing &amp; Syndication", "For Investors", "How private real estate syndications work, what to ask, and how to evaluate a sponsor.", None),
]
SHOW = 6


def category(slug):
    if slug in LUXURY: return "luxury"
    if slug in TIC: return "tic"
    if slug in SB684 or slug.startswith(("sb-684", "sb-1123")): return "sb684"
    return "investing"


def load_posts():
    posts = []
    for f in sorted(glob.glob("blog/*.html")):
        if f.endswith("index.html"): continue
        s = open(f).read()
        p = dict(slug=f[5:-5],
                 title=re.search(r'<h1 class="display">(.*?)</h1>', s, re.S).group(1).strip(),
                 date=re.search(r'rel="author">Oliver Thornton</a> &middot; ([A-Za-z]+ \d+, \d{4})', s).group(1),
                 hero=re.search(r"background-image:url\('\.\./assets/img/([^']+)'\)", s).group(1),
                 desc=re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
        p["d"] = datetime.datetime.strptime(p["date"], "%B %d, %Y")
        p["cat"] = category(p["slug"])
        posts.append(p)
    return posts


def plain(x):
    return H.unescape(re.sub(r"<[^>]+>", "", x))


def card(p, hidden):
    return f'''      <a class="photo-card post-card{' more' if hidden else ''}" href="{p['slug']}.html">
        <div class="frame"><img src="../assets/img/{p['hero']}" alt="{H.escape(plain(p['title']), quote=True)}" loading="lazy"></div>
        <div class="meta">
          <div class="name">{p['title']}</div>
          <div class="sub">{p['date']}</div>
          <p class="muted">{p['desc']}</p>
        </div>
      </a>'''


def build():
    posts = load_posts()
    chips = " ".join(f'<a href="#topic-{k}">{label}<span>{sum(1 for p in posts if p["cat"] == k)}</span></a>' for k, label, *_ in CATS)
    secs = []
    for i, (k, label, eb, blurb, lead) in enumerate(CATS):
        ps = sorted([p for p in posts if p["cat"] == k], key=lambda p: (p["slug"] != lead, -p["d"].timestamp(), p["slug"]))
        cards = "\n".join(card(p, j >= SHOW) for j, p in enumerate(ps))
        more = f'\n    <button class="topic-more" type="button" data-more>Show all {len(ps)} articles</button>' if len(ps) > SHOW else ""
        secs.append(f'''<section class="topic{' on-warm' if i % 2 else ''}" id="topic-{k}">
  <div class="wrap">
    <div class="split reveal" style="align-items:end;margin-bottom:2.2rem">
      <div>
        <p class="eyebrow">{eb} &middot; {len(ps)} articles</p>
        <h2 class="h-lg">{label}</h2>
      </div>
      <p class="muted" style="max-width:34rem;margin:0">{blurb}</p>
    </div>
    <div class="grid-3 topic-grid reveal" data-topic>
{cards}
    </div>{more}
  </div>
</section>''')

    s = open("blog/index.html").read()
    a = s.index('<main id="main">'); b = s.index("</main>")
    hero = s[a:s.index("</section>", a) + len("</section>")]
    notice = re.search(r'<p class="post-notice"[^>]*>.*?</p>', s, re.S).group(0)
    main = hero + f'''

<section class="tight topic-nav-wrap">
  <div class="wrap">
    {notice}
    <nav class="topic-nav" aria-label="Browse by topic">{chips}</nav>
  </div>
</section>

''' + "\n\n".join(secs) + "\n\n"
    s = s[:a] + main + s[b:]

    def fix(m):
        d = json.loads(m.group(2))
        if d.get("@type") == "Blog":
            d["blogPost"] = [{"@type": "BlogPosting", "headline": plain(p["title"]),
                              "url": f"https://assemble.capital/blog/{p['slug']}.html",
                              "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://assemble.capital/blog/{p['slug']}.html"},
                              "datePublished": p["d"].strftime("%Y-%m-%d")}
                             for p in sorted(posts, key=lambda p: -p["d"].timestamp())]
            return m.group(1) + "\n" + json.dumps(d, indent=2, ensure_ascii=False) + "\n</script>"
        return m.group(0)
    s = re.sub(r'(<script type="application/ld\+json"[^>]*>)(.*?)</script>', fix, s, flags=re.S)
    open("blog/index.html", "w").write(s)

    pj = json.load(open("blog/posts.json"))
    known = {x["slug"] for x in pj}
    names = {k: H.unescape(label) for k, label, *_ in CATS}
    for p in posts:
        if p["slug"] not in known:
            body = open(f"blog/{p['slug']}.html").read()
            i = body.index("</p>", body.index('<p class="post-notice">')) + 4
            j = body.index('<div class="post-disclaimer"')
            pj.insert(0, {"slug": p["slug"], "title": plain(p["title"]), "meta_description": H.unescape(p["desc"]),
                          "author": "Oliver Thornton", "date": p["date"], "category": None, "tags": [],
                          "hero_image": f"assets/img/{p['hero']}", "body_html": body[i:j].strip()})
    cmap = {p["slug"]: names[p["cat"]] for p in posts}
    for x in pj:
        if x["slug"] in cmap: x["category"] = cmap[x["slug"]]
    json.dump(pj, open("blog/posts.json", "w"), indent=2, ensure_ascii=False)
    print({k: sum(1 for p in posts if p["cat"] == k) for k, *_ in CATS}, "posts:", len(posts))


if __name__ == "__main__":
    build()
