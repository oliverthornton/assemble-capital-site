#!/usr/bin/env python3
"""Point every public page at /js/analytics.js, once, inside <head>.

The loader — not an inline gtag snippet — decides whether to fetch GA4.
Replacing the old inline snippet is idempotent. Email-signature pages and
blog drafts are left alone: they are not public site pages.
"""
import glob
import os

SITE = os.path.dirname(os.path.abspath(__file__))
LOADER = '<script src="/js/analytics.js"></script>'
SKIP_PREFIXES = ("email-signatures/", "blog/drafts/")
OLD = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-676QQYXN22"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-676QQYXN22');
</script>"""


def skip(rel):
    rel = rel.replace("\\", "/")
    return rel.startswith(SKIP_PREFIXES)


def main():
    changed = 0
    for path in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True):
        rel = os.path.relpath(path, SITE)
        if skip(rel):
            continue
        with open(path, encoding="utf-8") as handle:
            source = handle.read()
        if OLD in source:
            updated = source.replace(OLD, LOADER, 1)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(updated)
            changed += 1
            print("  replaced inline tag:", rel)
            continue
        if source.count('src="/js/analytics.js"') == 1:
            print("  already set:", rel)
            continue
        if "googletagmanager.com/gtag/js" in source:
            print("  unexpected gtag snippet:", rel)
            continue
        if "</head>" not in source:
            print("  no </head>:", rel)
            continue
        updated = source.replace("</head>", LOADER + "\n</head>", 1)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(updated)
        changed += 1
        print("  added loader:", rel)
    print(f"updated {changed} pages")


if __name__ == "__main__":
    main()
