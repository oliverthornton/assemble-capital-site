#!/usr/bin/env python3
"""Generate sitemap.xml containing only canonical, indexable URLs.

Inclusion is derived from each page's own <meta name="robots"> and
<link rel="canonical"> tags, so the sitemap can never drift out of sync
with the pages themselves.

    python3 tools-generate-sitemap.py
"""
import os, re

SITE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://assemble.capital"
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", "assets", "css", "js"}

PRIORITY = {
    "index.html": "1.0",
    "strategies.html": "0.9",
    "track-record.html": "0.9",
    "blog/index.html": "0.9",
    "about.html": "0.8",
    "portfolio.html": "0.8",
    "contact.html": "0.6",
}

def head_of(path):
    src = open(path, encoding="utf-8", errors="ignore").read()
    m = re.search(r"<head>(.*?)</head>", src, re.S | re.I)
    return m.group(1) if m else ""

urls, skipped = [], []
for root, dirs, files in os.walk(SITE):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    rel_dir = os.path.relpath(root, SITE)
    for f in sorted(files):
        if not f.endswith(".html"):
            continue
        path = os.path.join(root, f)
        rel = f if rel_dir == "." else f"{rel_dir}/{f}"
        head = head_of(path)

        robots = re.search(r'<meta\s+name="robots"\s+content="([^"]*)"', head, re.I)
        if robots and "noindex" in robots.group(1).lower():
            skipped.append((rel, "noindex"))
            continue

        canon = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', head, re.I)
        if not canon:
            skipped.append((rel, "NO CANONICAL — excluded"))
            continue
        loc = canon.group(1)

        if rel in PRIORITY:
            p = PRIORITY[rel]
        elif rel_dir in ("properties", "strategies"):
            p = "0.9"
        elif rel_dir == "blog":
            p = "0.6"
        else:
            p = "0.5"
        urls.append((loc, p))

urls.sort()
body = ['<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
body += [f"  <url><loc>{loc}</loc><priority>{p}</priority></url>" for loc, p in urls]
body.append("</urlset>")
open(os.path.join(SITE, "sitemap.xml"), "w").write("\n".join(body) + "\n")

print(f"wrote sitemap.xml with {len(urls)} canonical URLs")
for rel, why in skipped:
    print(f"  excluded: {rel}  ({why})")
