#!/usr/bin/env python3
"""Generate sitemap.xml from every HTML page in the site.

    python3 tools-generate-sitemap.py

Output: sitemap.xml (in the site root, picked up by tools-build-preview.py)
"""
import os

SITE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://assemble.capital"

EXCLUDE_DIRS = {".git", "__pycache__", "node_modules"}
# not meant for search — private/utility pages
EXCLUDE_FILES = {"privacy.html", "terms.html"}

PRIORITY = {
    "index.html": "1.0",
    "about.html": "0.8",
    "strategies.html": "0.9",
    "portfolio.html": "0.8",
    "track-record.html": "0.9",
    "contact.html": "0.6",
    "disclosures.html": "0.3",
    "blog/index.html": "0.9",
}

urls = []
for root, dirs, files in os.walk(SITE):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    rel_dir = os.path.relpath(root, SITE)
    for f in sorted(files):
        if not f.endswith(".html") or f in EXCLUDE_FILES:
            continue
        rel = f if rel_dir == "." else f"{rel_dir}/{f}"
        loc = f"{BASE}/" if rel == "index.html" else f"{BASE}/{rel}"
        if rel in PRIORITY:
            priority = PRIORITY[rel]
        elif rel_dir in ("properties", "strategies"):
            priority = "0.9"
        elif rel_dir == "blog":
            # individual posts rank below the properties/strategies detail
            # pages (0.9) but above the site's generic default (0.5) —
            # timely content, not core deal/strategy collateral.
            priority = "0.6"
        else:
            priority = "0.5"
        urls.append((loc, priority))

urls.sort()

body = ['<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, priority in urls:
    body.append(f"  <url><loc>{loc}</loc><priority>{priority}</priority></url>")
body.append("</urlset>")

with open(os.path.join(SITE, "sitemap.xml"), "w") as fh:
    fh.write("\n".join(body) + "\n")

print(f"wrote sitemap.xml with {len(urls)} URLs")
