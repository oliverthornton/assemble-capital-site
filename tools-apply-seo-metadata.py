#!/usr/bin/env python3
"""
Apply 506(b)-conservative SEO metadata sitewide for assemble.capital.

Implements the ASSEMBLE_CAPITAL_SEO_METADATA_506B_IMPLEMENTATION_PLAN:
  - unique title + meta description per page
  - self-referencing absolute canonical
  - robots directive (index/noindex per page class)
  - complete OG + Twitter card set with dimensions and alt text
  - Organization / BreadcrumbList / WebPage JSON-LD

Idempotent: safe to re-run.
"""
import os, re, json, html

SITE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://assemble.capital"
OG_W, OG_H = "1200", "630"

# ---------------------------------------------------------------- core pages
# (title, description, og_image_rel, og_alt)
CORE = {
 "index.html": (
   "Los Angeles Residential Development Firm | Assemble Capital",
   "Assemble Capital is a Los Angeles residential development firm focused on luxury homes, "
   "multifamily, fee-simple subdivisions, and tenancy-in-common housing.",
   "assets/img/social/home-1200x630.jpg",
   "The Hideaway HH, a Hollywood Hills luxury residence completed by the Assemble Capital principals"),

 "about.html": (
   "About Our Los Angeles Development Firm | Assemble Capital",
   "Meet the Assemble Capital principals and the vertically integrated team behind residential "
   "development projects across Los Angeles.",
   "assets/img/social/about-1200x630.jpg",
   "The Berryman Residence, a completed Assemble Capital ground-up home near Culver City"),

 "strategies.html": (
   "Los Angeles Development Strategies | Assemble Capital",
   "Explore Assemble Capital's approach to luxury residential, multifamily, SB 684 and SB 1123 "
   "subdivisions, and tenancy-in-common housing in Los Angeles.",
   "assets/img/social/strategies-1200x630.jpg",
   "The Gonzaga Residence, a completed Assemble Capital redevelopment in Westchester, Los Angeles"),

 "strategies/luxury-redevelopment.html": (
   "Luxury Home Development Los Angeles | Assemble Capital",
   "Luxury residential redevelopment and ground-up home development across prime Los Angeles "
   "neighborhoods, led by an experienced local team.",
   "assets/img/social/luxury-redevelopment-1200x630.jpg",
   "Villa De Vistas, a completed luxury residence on Mulholland Drive in the Hollywood Hills"),

 "strategies/boutique-multifamily.html": (
   "Multifamily Development Los Angeles | Assemble Capital",
   "Ground-up and value-add multifamily development for four- to fourteen-unit residential "
   "properties across Los Angeles.",
   "assets/img/social/boutique-multifamily-1200x630.jpg",
   "The Calvert XIV, a fourteen-unit multifamily development in North Hollywood"),

 "strategies/infill-subdivisions.html": (
   "SB 684 &amp; SB 1123 Subdivisions Los Angeles | Assemble Capital",
   "Fee-simple infill housing and small-lot subdivision development under California SB 684 and "
   "SB 1123 in Los Angeles.",
   "assets/img/social/infill-subdivisions-1200x630.jpg",
   "Rendering of a fee-simple infill subdivision project in Culver City"),

 "strategies/tic-housing.html": (
   "Tenancy-in-Common Housing Los Angeles | Assemble Capital",
   "Assemble Capital develops thoughtfully designed tenancy-in-common housing in Los Angeles "
   "through adaptive infill and small multifamily projects.",
   "assets/img/social/tic-housing-1200x630.jpg",
   "Rendering of a tenancy-in-common housing development in Santa Monica"),

 "portfolio.html": (
   "Current Los Angeles Development Projects | Assemble Capital",
   "Development updates for Assemble Capital residential projects in Westchester, Culver City, "
   "Santa Monica, and Los Angeles.",
   "assets/img/social/portfolio-1200x630.jpg",
   "A current Assemble Capital residential development project in Los Angeles"),

 "track-record.html": (
   "Completed Los Angeles Development Projects | Assemble Capital",
   "Explore completed luxury residential and multifamily projects delivered by the Assemble "
   "Capital principals and affiliated development teams.",
   "assets/img/social/track-record-1200x630.jpg",
   "The Macapa Oasis, a completed luxury residence in Outpost Estates, Los Angeles"),

 "blog/index.html": (
   "Los Angeles Real Estate Development Insights | Assemble Capital",
   "Practical insights on Los Angeles development, SB 684 and SB 1123, multifamily projects, "
   "tenancy-in-common housing, construction, and entitlements.",
   "assets/img/social/insights-1200x630.jpg",
   "The David III, a residential development near Culver City completed by the Assemble Capital principals"),

 "contact.html": (
   "Contact Assemble Capital | Los Angeles Development Firm",
   "Contact Assemble Capital regarding development opportunities, firm information, media, and "
   "professional collaboration in Los Angeles.",
   "assets/img/social/contact-1200x630.jpg",
   "The June IV, a completed four-unit multifamily building in Hollywood, Los Angeles"),
}

# legal pages -> noindex, follow
LEGAL = {
 "terms.html": ("Terms of Service | Assemble Capital",
   "Review the terms governing use of the Assemble Capital website."),
 "privacy.html": ("Privacy Policy | Assemble Capital",
   "Review how Assemble Capital collects, uses, and protects information submitted through its website."),
 "disclosures.html": ("Risks &amp; Disclosures | Assemble Capital",
   "Review important disclosures regarding Assemble Capital, project information, historical "
   "results, and private real estate investments."),
}

# ------------------------------------------------------------ property pages
# slug: (title, description, og_alt)
PROPS = {
 "apex-hh": ("7115 Macapa Dr Development Case Study | Assemble Capital",
   "Explore The Apex HH, a completed luxury residential development at 7115 Macapa Drive in "
   "Outpost Estates, Los Angeles.",
   "The Apex HH, a completed luxury residence at 7115 Macapa Drive, Los Angeles"),
 "berryman-residence": ("4432 Berryman Ave Development | Assemble Capital",
   "Explore The Berryman Residence, a completed ground-up home at 4432 Berryman Avenue near "
   "Culver City, with project details and gallery.",
   "The Berryman Residence, a completed ground-up home at 4432 Berryman Avenue"),
 "calvert-xiv": ("10957 Calvert St Multifamily Development | Assemble Capital",
   "Explore The Calvert XIV, a 14-unit multifamily development at 10957 Calvert Street in North "
   "Hollywood, Los Angeles.",
   "The Calvert XIV, a fourteen-unit multifamily building at 10957 Calvert Street"),
 "case-v": ("5651 Case Ave Multifamily Development | Assemble Capital",
   "Explore The Case V, a completed five-unit multifamily development at 5651 Case Avenue in "
   "North Hollywood, Los Angeles.",
   "The Case V, a completed five-unit multifamily building at 5651 Case Avenue"),
 "david-iii": ("5832 David Ave Residential Development | Assemble Capital",
   "Explore The David III, a completed residential development at 5832 David Avenue near Culver "
   "City, with project details and gallery.",
   "The David III, a completed residential development at 5832 David Avenue"),
 "gonzaga-residence": ("8404 Gonzaga Ave Development | Assemble Capital",
   "Explore The Gonzaga Residence, a completed residential redevelopment at 8404 Gonzaga Avenue "
   "in Westchester, Los Angeles.",
   "The Gonzaga Residence, a completed redevelopment at 8404 Gonzaga Avenue, Westchester"),
 "hideaway-hh": ("7932 Woodrow Wilson Dr Case Study | Assemble Capital",
   "Explore The Hideaway HH, a completed luxury residential development at 7932 Woodrow Wilson "
   "Drive in the Hollywood Hills.",
   "The Hideaway HH, a completed luxury residence on Woodrow Wilson Drive"),
 "hollywood-marvel": ("2827 Las Alturas St Case Study | Assemble Capital",
   "Explore The Hollywood Marvel, a completed residential development at 2827 Las Alturas Street "
   "in the Hollywood Hills, Los Angeles.",
   "The Hollywood Marvel, a completed residence at 2827 Las Alturas Street"),
 "hortense-vi": ("10742 Hortense St Multifamily Development | Assemble Capital",
   "Explore The Hortense VI, a completed six-unit multifamily development at 10742 Hortense "
   "Street in North Hollywood, Los Angeles.",
   "The Hortense VI, a completed six-unit multifamily building at 10742 Hortense Street"),
 "hutton-marvel": ("2731 Hutton Dr Development Case Study | Assemble Capital",
   "Explore The Hutton Marvel, a completed luxury residential development at 2731 Hutton Drive "
   "in the Beverly Hills area of Los Angeles.",
   "The Hutton Marvel, a completed luxury residence at 2731 Hutton Drive"),
 "june-iv": ("1323 N June St Multifamily Development | Assemble Capital",
   "Explore The June IV, a completed four-unit multifamily development at 1323 North June Street "
   "in Hollywood, Los Angeles.",
   "The June IV, a completed four-unit multifamily building at 1323 North June Street"),
 "macapa-oasis": ("7123 Macapa Dr Development Case Study | Assemble Capital",
   "Explore The Macapa Oasis, a completed luxury residential development at 7123 Macapa Drive in "
   "Outpost Estates, Los Angeles.",
   "The Macapa Oasis, a completed luxury residence at 7123 Macapa Drive, Outpost Estates"),
 "martha-mcm": ("14918 Martha St Development Case Study | Assemble Capital",
   "Explore The Martha MCM, a completed mid-century modern residential project at 14918 Martha "
   "Street in Sherman Oaks, Los Angeles.",
   "The Martha MCM, a completed mid-century modern residence at 14918 Martha Street"),
 "modern-orange": ("465 S Orange Grove Development Case Study | Assemble Capital",
   "Explore The Modern Orange, a completed residential redevelopment at 465 South Orange Grove "
   "Avenue in Los Angeles.",
   "The Modern Orange, a completed redevelopment at 465 South Orange Grove Avenue"),
 "paseo-moderna": ("3406 The Paseo Development Case Study | Assemble Capital",
   "Explore Paseo Moderna, a completed residential development at 3406 The Paseo in Los Angeles, "
   "with project details and gallery.",
   "Paseo Moderna, a completed residential development at 3406 The Paseo"),
 "rising-glen-mcm": ("1420 Rising Glen Rd Case Study | Assemble Capital",
   "Explore Rising Glen MCM, a completed residential development at 1420 Rising Glen Road near "
   "the Sunset Strip in Los Angeles.",
   "Rising Glen MCM, a completed residence at 1420 Rising Glen Road"),
 "treehouse-hh": ("8070 Laurelmont Dr Case Study | Assemble Capital",
   "Explore The Treehouse HH, a completed luxury residential development at 8070 Laurelmont "
   "Drive in Mount Olympus, Los Angeles.",
   "The Treehouse HH, a completed luxury residence at 8070 Laurelmont Drive"),
 "villa-de-edinburgh": ("138 N Edinburgh Ave Case Study | Assemble Capital",
   "Explore Villa De Edinburgh, a completed residential development at 138 North Edinburgh "
   "Avenue in Beverly Grove, Los Angeles.",
   "Villa De Edinburgh, a completed residence at 138 North Edinburgh Avenue"),
 "villa-de-vistas": ("7212 Mulholland Dr Case Study | Assemble Capital",
   "Explore Villa De Vistas, a completed luxury residential development at 7212 Mulholland Drive "
   "in the Hollywood Hills, Los Angeles.",
   "Villa De Vistas, a completed luxury residence at 7212 Mulholland Drive"),
}

PROP_BREADCRUMB_PARENT = ("Track Record", "/track-record.html")

ORG_JSONLD = {
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Assemble Capital",
  "url": BASE + "/",
  "logo": BASE + "/assets/img/logo/lockup-codgray-v2.png",
  "description": "Assemble Capital is a Los Angeles residential development firm focused on "
                 "luxury homes, multifamily, fee-simple subdivisions, and tenancy-in-common housing.",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "9000 Sunset Blvd #3",
    "addressLocality": "Los Angeles",
    "addressRegion": "CA",
    "postalCode": "90069",
    "addressCountry": "US"
  },
  "telephone": "+1-310-704-1794",
  "email": "info@assemble.capital",
  "areaServed": {"@type": "City", "name": "Los Angeles"},
  "sameAs": [
    "https://www.linkedin.com/company/assemble-capital-real-estate/",
    "https://www.instagram.com/assemble.capital/"
  ]
}

# ---------------------------------------------------------------- helpers
def rel_to_canonical(relpath):
    if relpath == "index.html":
        return BASE + "/"
    return BASE + "/" + relpath.replace(os.sep, "/")

def strip_tag(head, pattern, dotall=False):
    return re.sub(pattern, "", head, flags=re.I | (re.S if dotall else 0))

def build_meta_block(canonical, title, desc, og_image_abs, og_alt, og_type, robots):
    return f'''<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Assemble Capital">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image_abs}">
<meta property="og:image:width" content="{OG_W}">
<meta property="og:image:height" content="{OG_H}">
<meta property="og:image:alt" content="{og_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image_abs}">
<meta name="twitter:image:alt" content="{og_alt}">'''


# ---------------------------------------------------------------- LCP preload
def hero_preload(relpath, head):
    """Preload the hero background image.

    Heroes are CSS background-image, so the browser cannot discover them until
    the stylesheet has parsed - which pushes out Largest Contentful Paint. An
    explicit preload lets the fetch start with the HTML.
    """
    src = open(os.path.join(SITE, relpath), encoding="utf-8").read()
    body = src.split("</head>", 1)[-1]
    m = re.search(r"background-image:\s*url\(['\"]?([^)'\"]+)", body)
    head = re.sub(r'[ \t]*<link rel="preload"[^>]*data-seo="auto"[^>]*>\s*\n?', "", head, flags=re.I)
    if not m:
        return head
    href = m.group(1)
    tag = (f'<link rel="preload" as="image" href="{href}" '
           f'fetchpriority="high" data-seo="auto">')
    css = re.search(r'(<link rel="stylesheet"[^>]*>)', head, re.I)
    if css:
        return head[:css.start()] + tag + "\n" + head[css.start():]
    return head.rstrip() + "\n" + tag + "\n"

def apply(relpath, title, desc, og_image_abs, og_alt, og_type="website",
          robots="index, follow, max-image-preview:large", extra_jsonld=None):
    path = os.path.join(SITE, relpath)
    if not os.path.exists(path):
        print(f"  !! missing {relpath}")
        return False
    src = open(path, encoding="utf-8").read()
    m = re.search(r"(<head>)(.*?)(</head>)", src, re.S | re.I)
    if not m:
        print(f"  !! no <head> in {relpath}")
        return False
    head = m.group(2)

    # remove every tag we are about to re-emit (idempotent)
    head = strip_tag(head, r"[ \t]*<title>.*?</title>\s*\n?")
    head = strip_tag(head, r'[ \t]*<meta\s+name="description"[^>]*>\s*\n?')
    head = strip_tag(head, r'[ \t]*<link\s+rel="canonical"[^>]*>\s*\n?')
    head = strip_tag(head, r'[ \t]*<meta\s+name="robots"[^>]*>\s*\n?')
    head = strip_tag(head, r'[ \t]*<meta\s+property="og:[^"]*"[^>]*>\s*\n?')
    head = strip_tag(head, r'[ \t]*<meta\s+name="twitter:[^"]*"[^>]*>\s*\n?')
    head = strip_tag(head, r'[ \t]*<meta\s+name="keywords"[^>]*>\s*\n?')
    # drop any previously injected block from this script
    head = strip_tag(head, r'<script type="application/ld\+json" data-seo="auto">.*?</script>\s*\n?', dotall=True)

    block = build_meta_block(rel_to_canonical(relpath), title, desc,
                             og_image_abs, og_alt, og_type, robots)

    # insert after viewport (keeps charset/viewport first)
    vp = re.search(r'(<meta\s+name="viewport"[^>]*>)', head, re.I)
    if vp:
        head = head[:vp.end()] + "\n" + block + head[vp.end():]
    else:
        head = "\n" + block + head

    if extra_jsonld:
        payload = "\n".join(
            '<script type="application/ld+json" data-seo="auto">\n'
            + json.dumps(o, indent=2) + "\n</script>" for o in extra_jsonld)
        head = head.rstrip() + "\n" + payload + "\n"

    head = hero_preload(relpath, head)
    out = src[:m.start(2)] + head + src[m.end(2):]
    if out != src:
        open(path, "w", encoding="utf-8").write(out)
    return True

def breadcrumb(items):
    return {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n,
         "item": BASE + u} for i, (n, u) in enumerate(items)
      ]
    }

# ---------------------------------------------------------------- run
def main():
    n = 0
    # --- core pages
    for rel, (title, desc, img, alt) in CORE.items():
        crumbs = None
        if rel != "index.html":
            trail = [("Home", "/")]
            if rel.startswith("strategies/"):
                trail.append(("Strategies", "/strategies.html"))
            elif rel.startswith("blog/"):
                pass
            label = title.split(" | ")[0]
            trail.append((label, "/" + rel if rel != "index.html" else "/"))
            crumbs = [breadcrumb(trail)]
        else:
            crumbs = [ORG_JSONLD]
        if apply(rel, title, desc, BASE + "/" + img, alt, extra_jsonld=crumbs):
            n += 1

    # --- legal pages (noindex, follow) keep their existing social image
    for rel, (title, desc) in LEGAL.items():
        if apply(rel, title, desc, BASE + "/assets/img/social/home-1200x630.jpg",
                 "Assemble Capital", robots="noindex, follow"):
            n += 1

    # --- property pages
    for slug, (title, desc, alt) in PROPS.items():
        rel = f"properties/{slug}.html"
        img = f"{BASE}/assets/img/social/properties/{slug}-1200x630.jpg"
        page = {
          "@context": "https://schema.org",
          "@type": "WebPage",
          "name": title.split(" | ")[0],
          "description": html.unescape(desc),
          "url": rel_to_canonical(rel),
          "primaryImageOfPage": {"@type": "ImageObject", "url": img,
                                 "width": int(OG_W), "height": int(OG_H),
                                 "caption": html.unescape(alt)},
          "isPartOf": {"@type": "WebSite", "name": "Assemble Capital", "url": BASE + "/"},
          "publisher": {"@type": "Organization", "name": "Assemble Capital",
                        "url": BASE + "/"}
        }
        crumbs = breadcrumb([("Home", "/"),
                             (PROP_BREADCRUMB_PARENT[0], PROP_BREADCRUMB_PARENT[1]),
                             (title.split(" | ")[0], "/" + rel)])
        if apply(rel, title, desc, img, alt, extra_jsonld=[page, crumbs]):
            n += 1

    print(f"metadata applied to {n} pages")

if __name__ == "__main__":
    main()
