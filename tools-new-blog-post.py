#!/usr/bin/env python3
"""Add a new Learning Center article by copying a current live article.

The live HTML files in blog/ are the source of truth. This tool never rewrites
an existing article: it copies the page shell (header, nav, notice, disclaimer,
footer, schema) from a current article, swaps in the new post's content, and
then updates only the files a new post needs.

    python3 tools-new-blog-post.py blog/drafts/<slug>             # publish locally
    python3 tools-new-blog-post.py blog/drafts/<slug> --dry-run   # check only, write nothing

A draft is a folder with two files (see blog/README.md):
    post.json   metadata: slug, title, page_title, description, date, topic,
                hero, card_bg, related, faq, keyword
    body.html   the article body (h2/p/table/etc.), without the title or disclaimer

What it changes, and nothing else:
    blog/<slug>.html                               the new article
    blog/index.html                                Learning Center index (via tools-build-blog-index.py)
    blog/posts.json                                record of the post (topic, share-card photo)
    sitemap.xml                                    one new <url>, plus the blog index date
    assets/img/social/cards/blog/<slug>.jpg        share card (via tools-generate-share-cards.py)

Safety: everything is built in a temporary copy of the site first. The run stops
without touching the real site if the slug already exists, a link or image in the
new page points at a missing file, any old text from the copied article is left
behind, or any file outside the list above would change.
"""
import datetime, filecmp, html as H, importlib.util, json, os, re, shutil, subprocess, sys, tempfile

SITE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://assemble.capital"
TEMPLATE = "ab-1751-missing-middle-townhome-ownership-act"   # a current, fully up-to-date article
TOPICS = {  # topic -> (label in posts.json, strategy link under Related Reading)
    "sb684": ("SB 684 & SB 1123", '<a href="../strategies/infill-subdivisions.html">SB 684/1123 Fee Simple Subdivisions</a>'),
    "luxury": ("Luxury Residential", '<a href="../strategies/luxury-redevelopment.html">Luxury Residential Development</a>'),
    "tic": ("TIC & Multifamily", '<a href="../strategies/tic-housing.html">Tenancy-In-Common Housing</a>'),
    "investing": ("Investing & Syndication", '<a href="../strategies.html">All four Assemble Capital strategies</a>'),
}
REQUIRED = ["slug", "title", "description", "date", "topic", "hero", "related"]


def die(msg):
    print("STOPPED: " + msg + "\nNothing on the site was changed.")
    sys.exit(1)


def plain(x):
    return H.unescape(re.sub(r"<[^>]+>", "", x)).replace("\xa0", " ")


def attr(x):
    """Escape text for an HTML attribute, keeping existing entities like &rsquo;."""
    return re.sub(r"&(?![a-zA-Z]+;|#\d+;)", "&amp;", x).replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def load_draft(path):
    d = os.path.abspath(path)
    if not os.path.isfile(os.path.join(d, "post.json")) or not os.path.isfile(os.path.join(d, "body.html")):
        die(f"{path} needs post.json and body.html")
    p = json.load(open(os.path.join(d, "post.json")))
    missing = [k for k in REQUIRED if not p.get(k)]
    if missing: die("post.json is missing: " + ", ".join(missing))
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", p["slug"]): die("slug must be lowercase words joined by hyphens")
    if p["topic"] not in TOPICS: die("topic must be one of: " + ", ".join(TOPICS))
    try:
        p["_d"] = datetime.date.fromisoformat(p["date"])
    except ValueError:
        die("date must look like 2026-11-05")
    p["_date"] = p["_d"].strftime("%B ") + str(p["_d"].day) + p["_d"].strftime(", %Y")
    p.setdefault("page_title", plain(p["title"]))
    p.setdefault("card_bg", p["hero"])
    p.setdefault("faq", [])
    p["body"] = open(os.path.join(d, "body.html")).read().strip()
    if re.search(r"<h1|post-disclaimer|<html|<body", p["body"], re.I): die("body.html should hold only the article body (no h1, page shell or disclaimer)")
    if len(p["related"]) != 3: die("related needs exactly 3 article slugs")
    if len(p["page_title"]) > 65: print(f"note: page_title is {len(p['page_title'])} characters; Google shows about 60")
    if not 70 <= len(plain(p["description"])) <= 170: print(f"note: description is {len(plain(p['description']))} characters; aim for 120-160")
    return p


def article_info(site, slug):
    s = open(os.path.join(site, "blog", slug + ".html")).read()
    return dict(title=re.search(r'<h1 class="display">(.*?)</h1>', s, re.S).group(1).strip(),
                date=re.search(r'rel="author">Oliver Thornton</a> &middot; ([A-Za-z]+ \d+, \d{4})', s).group(1),
                hero=re.search(r"background-image:url\('\.\./assets/img/([^']+)'\)", s).group(1))


def build_page(site, p):
    s = open(os.path.join(site, "blog", TEMPLATE + ".html")).read()
    old = article_info(site, TEMPLATE)
    old_url = f"{BASE}/blog/{TEMPLATE}.html"
    url = f"{BASE}/blog/{p['slug']}.html"
    title_attr, desc_attr = attr(p["title"]), attr(p["description"])

    def sub1(pattern, repl, s, flags=0):
        out, n = re.subn(pattern, lambda m: repl, s, count=1, flags=flags)
        if n != 1: die(f"template layout changed; could not find {pattern[:60]!r} in blog/{TEMPLATE}.html")
        return out

    s = sub1(r"<title>.*?</title>", f"<title>{H.escape(p['page_title'], quote=False)}</title>", s)
    for tag in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = sub1(rf'<meta {tag} content="[^"]*">', f'<meta {tag} content="{desc_attr}">', s)
    for tag in ('property="og:title"', 'name="twitter:title"'):
        s = sub1(rf'<meta {tag} content="[^"]*">', f'<meta {tag} content="{title_attr} &mdash; Assemble Capital">', s)
    s = s.replace(old_url, url).replace(f"social/cards/blog/{TEMPLATE}.jpg", f"social/cards/blog/{p['slug']}.jpg")
    card_alt = attr(f"Learning Center: {plain(p['title'])}. Oliver Thornton  ·  Assemble Capital")
    for tag in ('property="og:image:alt"', 'name="twitter:image:alt"'):
        s = sub1(rf'<meta {tag} content="[^"]*">', f'<meta {tag} content="{card_alt}">', s)

    # structured data: edit the parsed JSON rather than the text
    def fix(m):
        d = json.loads(m.group(2))
        t = d.get("@type")
        if t == "BlogPosting":
            d.update(headline=plain(p["title"]), description=plain(p["description"]), image=f"{BASE}/assets/img/{p['hero']}",
                     datePublished=p["date"], dateModified=p["date"])
            d["mainEntityOfPage"]["@id"] = url
        elif t == "FAQPage":
            if not p["faq"]: return ""
            d["mainEntity"] = [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in p["faq"]]
        elif t == "BreadcrumbList":
            d["itemListElement"][-1].update(name=plain(p["title"]), item=url)
        return m.group(1) + "\n" + json.dumps(d, indent=2, ensure_ascii=False) + "\n</script>"
    s = re.sub(r'(<script type="application/ld\+json"[^>]*>)\s*(.*?)\s*</script>', fix, s, flags=re.S)
    s = re.sub(r"\n\n+(<script type=\"application/ld\+json\")", r"\n\1", s)

    s = sub1(r'<h1 class="display">.*?</h1>', f'<h1 class="display">{p["title"]}</h1>', s, re.S)
    s = sub1(r'rel="author">Oliver Thornton</a> &middot; [A-Za-z]+ \d+, \d{4}', 'rel="author">Oliver Thornton</a> &middot; ' + p["_date"], s)
    s = sub1(r"background-image:url\('\.\./assets/img/[^']+'\)", f"background-image:url('../assets/img/{p['hero']}')", s)

    # body: everything between the "general information" notice and the full disclaimer
    a = s.index("</p>\n", s.index('<p class="post-notice">')) + 5
    b = s.index('    <div class="post-disclaimer"')
    s = s[:a] + p["body"] + "\n\n" + s[b:]

    cards = []
    for r in p["related"]:
        if not os.path.exists(os.path.join(site, "blog", r + ".html")): die(f"related article blog/{r}.html does not exist")
        if r == p["slug"]: die("an article can't list itself as related")
        i = article_info(site, r)
        cards.append(f'''        <a class="photo-card" href="{r}.html">
          <div class="frame"><img src="../assets/img/{i['hero']}" alt="{attr(plain(i['title']))}" loading="lazy"></div>
          <div class="meta">
            <div class="name">{i['title']}</div>
            <div class="sub">{i['date']}</div>
          </div>
        </a>''')
    m = re.search(r'(<!-- related-reading -->.*?<div class="grid-3 reveal" style="margin-top:2.4rem">\n).*?(\n    </div>\n    <p class="muted" style="margin-top:2rem">Or see how this plays out in practice: )<a [^>]*>.*?</a>(\.</p>)', s, re.S)
    if not m: die(f"template layout changed; Related Reading not found in blog/{TEMPLATE}.html")
    s = s[:m.start()] + m.group(1) + "\n".join(cards) + m.group(2) + TOPICS[p["topic"]][1] + m.group(3) + s[m.end():]

    # leftovers from the copied article
    head = s.split("<!-- related-reading -->")[0]
    for leftover in (TEMPLATE, old["title"], old["date"], old["hero"]):
        if leftover in head and leftover not in p["body"] and leftover != p["hero"] and leftover != p["_date"]:
            die(f"text from the copied article was left behind: {leftover!r}")
    return s


def check_links(site, page_path, s):
    bad = []
    for ref in re.findall(r'(?:href|src)="([^"#?]+)', s) + re.findall(r"url\('([^']+)'\)", s):
        if re.match(r"(https?:|mailto:|tel:|data:|//)", ref): continue
        target = os.path.normpath(os.path.join(site, ref.lstrip("/")) if ref.startswith("/") else os.path.join(os.path.dirname(page_path), ref))
        if not os.path.exists(target): bad.append(ref)
    if bad: die("the new page links to files that don't exist: " + ", ".join(sorted(set(bad))))


def load_module(site, name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), os.path.join(site, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    cwd = os.getcwd(); os.chdir(site)
    try:
        spec.loader.exec_module(mod)
    finally:
        os.chdir(cwd)
    return mod


def publish(site, p):
    slug = p["slug"]
    page = os.path.join(site, "blog", slug + ".html")
    s = build_page(site, p)
    open(page, "w").write(s)
    check_links(site, page, s)

    # posts.json: the record of the post; the index builder and share cards read topic and card_bg from it
    pj_path = os.path.join(site, "blog", "posts.json")
    pj = json.load(open(pj_path))
    pj.append(dict(slug=slug, title=plain(p["title"]), meta_description=plain(p["description"]), author="Oliver Thornton",
                   date=p["_date"], category=TOPICS[p["topic"]][0], topic=p["topic"], tags=[], hero_image=f"assets/img/{p['hero']}",
                   card_bg=p["card_bg"], body_html=p["body"], status="published", source_keyword=p.get("keyword"),
                   _migration_source=None, faq=[{"q": q, "a": a} for q, a in p["faq"]], project_attribution=False))
    json.dump(pj, open(pj_path, "w"), indent=2, ensure_ascii=False)

    subprocess.run([sys.executable, os.path.join(site, "tools-build-blog-index.py")], check=True, cwd=site, stdout=subprocess.DEVNULL)

    # sitemap: add one <url> in alphabetical place and bump the blog index date
    sm_path = os.path.join(site, "sitemap.xml")
    sm = open(sm_path).read()
    line = f"  <url><loc>{BASE}/blog/{slug}.html</loc><lastmod>{p['date']}</lastmod><priority>0.6</priority></url>\n"
    lines = sm.splitlines(keepends=True)
    blog = [i for i, l in enumerate(lines) if f"<loc>{BASE}/blog/" in l]
    at = next((i for i in blog if re.search(r"<loc>([^<]+)</loc>", lines[i]).group(1) > f"{BASE}/blog/{slug}.html"), blog[-1] + 1)
    lines.insert(at, line)
    sm = "".join(lines)
    sm, n = re.subn(rf"(<loc>{re.escape(BASE)}/blog/index\.html</loc><lastmod>)[^<]+", lambda m: m.group(1) + p["date"], sm)
    if n != 1: die("couldn't find the blog index in sitemap.xml")
    open(sm_path, "w").write(sm)

    # share card
    sc = load_module(site, "tools-generate-share-cards")
    cwd = os.getcwd(); os.chdir(site)
    try:
        name, bg, eb, head, sub = sc.blog_card(f"blog/{slug}.html", s)
        with tempfile.TemporaryDirectory() as tmp:
            sc.render(name, bg, eb, head, sub, tmp)
        sc.set_tags(f"blog/{slug}.html", name, eb, head, sub)
    finally:
        os.chdir(cwd)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if len(args) != 1: print(__doc__); sys.exit(2)
    p = load_draft(args[0])
    slug = p["slug"]
    if os.path.exists(os.path.join(SITE, "blog", slug + ".html")):
        die(f"blog/{slug}.html already exists. This tool only adds new articles; edit existing ones directly.")

    expected = {f"blog/{slug}.html", "blog/index.html", "blog/posts.json", "sitemap.xml", f"assets/img/social/cards/blog/{slug}.jpg"}
    with tempfile.TemporaryDirectory() as tmp:
        copy = os.path.join(tmp, "site")
        shutil.copytree(SITE, copy, ignore=shutil.ignore_patterns(".git", ".stfolder", ".vercel", "node_modules"))
        publish(copy, p)
        changed = set()
        for root, _, files in os.walk(copy):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), copy)
                if "__pycache__" in rel: continue
                orig = os.path.join(SITE, rel)
                if not os.path.exists(orig) or not filecmp.cmp(orig, os.path.join(copy, rel), shallow=False):
                    changed.add(rel)
        extra = changed - expected
        if extra: die("this would also change files it shouldn't: " + ", ".join(sorted(extra)))
        if expected - changed: die("expected changes didn't happen: " + ", ".join(sorted(expected - changed)))
        print(("Dry run OK. These files would change:" if dry else "Published locally. Changed files:"))
        for rel in sorted(changed): print("  " + rel)
        if dry: return
        for rel in sorted(changed):
            os.makedirs(os.path.dirname(os.path.join(SITE, rel)), exist_ok=True)
            shutil.copy2(os.path.join(copy, rel), os.path.join(SITE, rel))
    print(f"\nPreview it at /blog/{slug}.html, then commit and push to make it live.")


if __name__ == "__main__":
    main()
