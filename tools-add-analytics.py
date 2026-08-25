#!/usr/bin/env python3
"""Insert the GA4 Google tag into every page's <head>, right before </head>.

Idempotent: re-running is safe, it skips pages that already have the tag.
"""
import glob, os, re

SITE = os.path.dirname(os.path.abspath(__file__))
MEASUREMENT_ID = "G-676QQYXN22"

TAG = f'''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{MEASUREMENT_ID}');
</script>
</head>'''

if __name__ == "__main__":
    n = 0
    for f in glob.glob(os.path.join(SITE, "*.html")) + glob.glob(os.path.join(SITE, "*", "*.html")):
        rel = os.path.relpath(f, SITE)
        s = open(f).read()
        if MEASUREMENT_ID in s:
            print("  already tagged:", rel); continue
        if "</head>" not in s:
            print("  no </head>:", rel); continue
        open(f, "w").write(s.replace("</head>", TAG, 1))
        n += 1
    print(f"GA tag added to {n} pages")
