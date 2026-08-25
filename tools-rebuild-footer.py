#!/usr/bin/env python3
"""Rebuild the site footer on every page.

Footer columns: brand + social · Navigate (mirrors header) · Strategies · Insights,
followed by a principals strip, legal text, and legal links.
"""
import os, re, glob, json
from datetime import datetime

SITE = os.path.dirname(os.path.abspath(__file__))

# --- social ----------------------------------------------------------------
# Only LinkedIn + Instagram are live (confirmed w/ Oliver, Aug 2026). No
# Twitter/X or YouTube profiles exist. Facebook page is not live — the button
# stays commented out below; paste the URL into FACEBOOK and uncomment to
# switch it on once/if the page goes live.
LINKEDIN = "https://www.linkedin.com/company/assemble-capital-real-estate"
INSTAGRAM = "https://www.instagram.com/assemble.capital"
FACEBOOK = ""   # e.g. https://www.facebook.com/assemblecapital

ICON = {
 "linkedin": '<path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.42v1.56h.05a3.75 3.75 0 0 1 3.37-1.85c3.6 0 4.27 2.37 4.27 5.46zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13M7.12 20.45H3.55V9h3.57zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0"/>',
 "instagram": '<path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9-.42-.42-.68-.82-.9-1.38-.16-.42-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41 1.27-.06 1.65-.07 4.85-.07M12 0C8.74 0 8.33.01 7.05.07 5.78.13 4.9.33 4.14.63a5.9 5.9 0 0 0-2.13 1.38A5.9 5.9 0 0 0 .63 4.14c-.3.76-.5 1.64-.56 2.91C.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.06 1.27.26 2.15.56 2.91a5.9 5.9 0 0 0 1.38 2.13 5.9 5.9 0 0 0 2.13 1.38c.76.3 1.64.5 2.91.56C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.27-.06 2.15-.26 2.91-.56a5.9 5.9 0 0 0 2.13-1.38 5.9 5.9 0 0 0 1.38-2.13c.3-.76.5-1.64.56-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.27-.26-2.15-.56-2.91a5.9 5.9 0 0 0-1.38-2.13A5.9 5.9 0 0 0 19.86.63c-.76-.3-1.64-.5-2.91-.56C15.67.01 15.26 0 12 0m0 5.84a6.16 6.16 0 1 0 0 12.32 6.16 6.16 0 0 0 0-12.32M12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8m7.85-10.4a1.44 1.44 0 1 1-2.88 0 1.44 1.44 0 0 1 2.88 0"/>',
 "facebook": '<path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.69.24 2.69.24v2.97h-1.52c-1.49 0-1.96.93-1.96 1.89v2.25h3.33l-.53 3.49h-2.8V24C19.61 23.1 24 18.1 24 12.07"/>',
}

def social(base):
    def btn(name, url, label):
        return (f'          <a href="{url}" target="_blank" rel="noopener" aria-label="Assemble Capital on {label}">'
                f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICON[name]}</svg></a>')
    out = [btn("linkedin", LINKEDIN, "LinkedIn"), btn("instagram", INSTAGRAM, "Instagram")]
    if FACEBOOK:
        out.append(btn("facebook", FACEBOOK, "Facebook"))
    else:
        out.append('          <!-- Facebook: add the page URL to FACEBOOK in tools-rebuild-footer.py and re-run to enable.\n'
                   '          ' + btn("facebook", "FACEBOOK_URL", "Facebook").strip() + ' -->')
    return "\n".join(out)

# --- blog -------------------------------------------------------------------
# The blog now lives in-repo (see blog/README.md) rather than on the old,
# now-dead Squarespace domain. BLOG_BASE is an internal path, matching the
# leading-slash-free convention every other internal link in this footer
# already uses (e.g. "{b}strategies.html").
BLOG_BASE = "blog"
POSTS_PER_FOOTER = 4  # how many latest published posts to surface here

def latest_posts(limit=POSTS_PER_FOOTER):
    """Read blog/posts.json, filter to status == 'published', sort by date
    descending, and return up to `limit` as (title, slug) tuples. Returns []
    if the file is missing, malformed, or has no published posts yet — the
    Insights column just renders empty rather than crashing the footer build."""
    path = os.path.join(SITE, "blog", "posts.json")
    try:
        with open(path) as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return []
    published = [p for p in data if p.get("status") == "published"]
    def _key(p):
        try:
            return datetime.strptime(p["date"], "%B %d, %Y")
        except (KeyError, TypeError, ValueError):
            return datetime.min
    published.sort(key=_key, reverse=True)
    return [(p["title"], p["slug"]) for p in published[:limit]]

MONO = ('<svg viewBox="0 0 64 64" fill="none" aria-hidden="true">\n'
 '            <circle cx="32" cy="32" r="30" stroke="currentColor" stroke-width="1.5"/>\n'
 '            <text x="26" y="42.5" font-family="Cormorant Garamond, Georgia, serif" font-size="31" text-anchor="middle" fill="currentColor">C</text>\n'
 '            <text x="37.5" y="46" font-family="Cormorant Garamond, Georgia, serif" font-size="25" text-anchor="middle" fill="currentColor">A</text>\n'
 '          </svg>')

LEGAL = ("Not an offer or solicitation. Any offering is made only through definitive offering documents "
 "of the applicable issuer to verified accredited and/or sophisticated investors in compliance with "
 "applicable securities laws. Past performance is not indicative of future results. Historical returns "
 "shown on this site were generated on projects completed by the principals through predecessor and "
 "affiliated entities — most were not Assemble Capital offerings and did not involve Assemble Capital "
 "investors — and are sponsor-level, unaudited, and derived from internal records. Projections are "
 "unrealized and subject to change. Investments in private real estate offerings are speculative, "
 "illiquid, and involve a high degree of risk, including possible loss of the entire investment. "
 "Assemble Capital does not provide investment, legal, or tax advice.")

def build(base):
    """base is '' for root pages, '../' for pages one directory deep."""
    b = base
    posts = "\n".join(
        f'          <a href="{b}{BLOG_BASE}/{slug}.html">{title}</a>'
        for title, slug in latest_posts())
    return f'''<footer class="site-foot">
  <img class="watermark" src="{b}assets/img/logo/emblem-white-v2.png" alt="" aria-hidden="true">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="lockup" href="{b}index.html" style="color:var(--paper);margin-bottom:1.2rem">
          <img class="emblem" src="{b}assets/img/logo/emblem-white-v2.png" alt="" aria-hidden="true">
          <span class="word">Assemble<br>Capital</span>
        </a>
        <p style="font-size:.85rem;color:rgba(248,248,248,.7);max-width:22rem;margin-top:1.2rem">A Los Angeles residential investment manager.<br>9000 Sunset Blvd #3, Los Angeles, CA 90069</p>
        <p style="font-size:.85rem"><a href="mailto:info@assemble.capital" style="text-decoration:none">info@assemble.capital</a><br><a href="tel:+13107041794" style="text-decoration:none">(310) 704-1794</a></p>
        <div style="display:flex;align-items:center;gap:.7rem;font-family:var(--type);font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:rgba(248,248,248,.5);margin:1.7rem 0 .7rem">
          <span style="width:1.6rem;height:1px;background:var(--bronze)"></span>Follow
        </div>
        <div class="social">
{social(b)}
        </div>
      </div>
      <div>
        <h4>Navigate</h4>
        <div class="foot-nav">
          <a href="{b}index.html">Home</a>
          <a href="{b}about.html">About</a>
          <a href="{b}strategies.html">Strategies</a>
          <a href="{b}portfolio.html">Current Projects</a>
          <a href="{b}track-record.html">Track Record</a>
          <a href="{b}{BLOG_BASE}/index.html">Blogs</a>
          <a href="{b}contact.html">Contact</a>
          <a href="https://assemblecapital.cashflowportal.com" target="_blank" rel="noopener">Investor Portal &#8599;</a>
        </div>
      </div>
      <div>
        <h4>Strategies</h4>
        <div class="foot-nav">
          <a href="{b}strategies/luxury-redevelopment.html">Luxury Residential Development</a>
          <a href="{b}strategies/boutique-multifamily.html">Opportunistic &amp; Value Add Multifamily Development</a>
          <a href="{b}strategies/infill-subdivisions.html">SB 684/1123 Fee Simple Subdivisions</a>
          <a href="{b}strategies/tic-housing.html">Tenancy-In-Common Housing</a>
        </div>
      </div>
      <div>
        <h4>Insights</h4>
        <div class="foot-posts">
{posts}
        </div>
        <p class="foot-more"><a href="{b}{BLOG_BASE}/index.html">All insights</a></p>
      </div>
    </div>
    <div class="foot-principals">
      <div><b>RC Thornton</b><span>Partner &middot; Construction &amp; Development<br><a href="mailto:rc@assemble.capital">rc@assemble.capital</a> &middot; (310) 210-5315</span></div>
      <div><b>Oliver Thornton</b><span>Partner &middot; Syndications, Investor Relations, Financing &amp; Strategy<br><a href="mailto:oliver@assemble.capital">oliver@assemble.capital</a> &middot; (310) 704-1794</span></div>
      <div><b>Erik Lim</b><span>Partner &middot; Syndications, Investor Relations &amp; Operations<br><a href="mailto:erik@assemble.capital">erik@assemble.capital</a> &middot; (310) 989-9166</span></div>
    </div>
    <p class="legal">{LEGAL}</p>
    <p class="legal-links"><a href="{b}terms.html">Terms of Service</a> &nbsp;&middot;&nbsp; <a href="{b}privacy.html">Privacy Policy</a> &nbsp;&middot;&nbsp; <a href="{b}disclosures.html">Risks &amp; Disclosures</a></p>
    <div class="colophon">
      <span>&copy; 2026 Assemble Capital &middot; Los Angeles, CA</span>
      <span>Prepared for accredited &amp; sophisticated investors</span>
    </div>
  </div>
</footer>'''

if __name__ == "__main__":
    pat = re.compile(r'<footer class="site-foot">.*?</footer>', re.S)
    n = 0
    for f in glob.glob(os.path.join(SITE, "*.html")) + glob.glob(os.path.join(SITE, "*", "*.html")):
        rel = os.path.relpath(f, SITE)
        base = "" if os.sep not in rel else "../"
        s = open(f).read()
        if not pat.search(s):
            print("  no footer:", rel); continue
        open(f, "w").write(pat.sub(lambda _: build(base), s, count=1))
        n += 1
    print(f"footer rebuilt on {n} pages")
