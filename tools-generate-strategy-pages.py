#!/usr/bin/env python3
"""Generate the four strategy detail pages."""
import os

SITE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SITE, "strategies")

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
 '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&'
 'family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,500&family=Special+Elite&'
 'display=swap" rel="stylesheet">')
FAVICON = '<link rel="icon" href="../assets/img/logo/favicon-v2.png">'
MONO = '<img class="emblem" src="../assets/img/logo/emblem-white-v2.png" alt="" aria-hidden="true">'
LEGAL = ("Not an offer or solicitation. Any offering is made only through definitive offering documents "
 "of the applicable issuer to verified accredited and/or sophisticated investors in compliance with "
 "applicable securities laws. Past performance is not indicative of future results. Historical returns "
 "shown on this site were generated on projects completed by the principals through predecessor and "
 "affiliated entities — most were not Assemble Capital offerings and did not involve Assemble Capital "
 "investors — and are sponsor-level, unaudited, and derived from internal records. Projections are "
 "unrealized and subject to change. Investments in private real estate offerings are speculative, "
 "illiquid, and involve a high degree of risk, including possible loss of the entire investment. "
 "Assemble Capital does not provide investment, legal, or tax advice.")

def header():
    return f'''<header class="site-head">
  <div class="bar">
    <a class="lockup" href="../index.html" aria-label="Assemble Capital home">
      {MONO}
      <span class="word">Assemble<br>Capital</span>
    </a>
    <button class="menu-btn" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="site-nav" id="site-nav" aria-label="Primary">
      <a href="../about.html">About</a>
      <div class="nav-dd">
        <a href="../strategies.html" class="nav-dd-toggle active">Strategies</a>
        <div class="nav-dd-menu">
          <a href="luxury-redevelopment.html">Luxury Residential Development</a>
          <a href="boutique-multifamily.html">Opportunistic &amp; Value Add Multifamily Development</a>
          <a href="infill-subdivisions.html">SB 684/1123 Fee Simple Subdivisions</a>
          <a href="tic-housing.html">Tenancy-In-Common Housing</a>
        </div>
      </div>
      <a href="../portfolio.html">Current Projects</a>
      <a href="../track-record.html">Track Record</a>
      <a href="../contact.html">Contact</a>
      <a class="portal" href="https://assemblecapital.cashflowportal.com" target="_blank" rel="noopener">Investor Portal&nbsp;&#8599;</a>
    </nav>
  </div>
</header>'''

# footer comes from the single source of truth so it stays in sync sitewide
import importlib.util as _ilu, os as _os
_spec = _ilu.spec_from_file_location("_footer",
    _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "tools-rebuild-footer.py"))
_fm = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_fm)

def footer(base=".."):
    return _fm.build("../")

def card(img, name, sub, tag, href=None, figs=None):
    t = f'<span class="tag">{tag}</span>' if tag else ""
    f = ""
    if figs:
        f = '<div class="figures">' + "".join(
            f"<div><b>{a}</b><span>{b}</span></div>" for a, b in figs) + "</div>"
    inner = (f'<div class="frame">{t}<img src="../assets/img/{img}" alt="{name}" loading="lazy"></div>'
             f'<div class="meta"><div class="name">{name}</div><div class="sub">{sub}</div>{f}</div>')
    if href:
        return f'      <a class="photo-card" href="{href}">{inner}</a>'
    return f'      <div class="photo-card">{inner}</div>'

def stage(title, eyebrow, blurb, cards, warm=False, stamp=None):
    if not cards:
        return ""
    cls = ' class="on-warm"' if warm else ""
    st = f'<span class="stamp">{stamp}</span>' if stamp else ""
    if len(cards) == 1:
        grid = "grid-solo"
    elif len(cards) == 2:
        grid = "grid-2"
    elif len(cards) == 3:
        grid = "grid-3"
    else:
        grid = "grid-4"
    return f'''
<section{cls}>
  <div class="wrap">
    <div class="reveal" style="display:flex;flex-wrap:wrap;align-items:end;justify-content:space-between;gap:1.5rem;margin-bottom:2.4rem">
      <div>
        <p class="eyebrow">{eyebrow}</p>
        <h2 class="h-lg">{title}</h2>
      </div>
      {st}
    </div>
    {f'<p class="muted reveal" style="max-width:48rem;margin:-1.2rem 0 2rem;font-size:.94rem">{blurb}</p>' if blurb else ''}
    <div class="{grid} reveal">
{chr(10).join(cards)}
    </div>
  </div>
</section>'''

# ------------------------------------------------------------------ data
S = [
dict(slug="luxury-redevelopment", eyebrow="Strategy 01 &middot; SFR&ndash;Redev",
  name="Luxury Residential<br>Development",
  hero="villa-de-vistas.webp",
  sub="Studs-out rebuilds and heavy remodels of under-improved homes in prime Los Angeles submarkets.",
  specs=[("$2M &ndash; $6M","Acquisition basis"),("$3M &ndash; $9M","Exit range"),
         ("12 &ndash; 30 mo","Business plan"),("~30 &ndash; 60%","Target gross margin on cost")],
  lede="The largest pricing gap in Los Angeles residential is between a dated house in a great location and a finished one.",
  why=["A dated home in a prime submarket prices to a narrow buyer pool &mdash; the small "
       "fraction of purchasers willing and able to manage a construction project. A finished home "
       "on the same street prices to the entire market. That spread is the strategy.",
       "It persists because the work in between is genuinely hard. Most buyers will not take on a "
       "studs-out rebuild. Most small operators cannot finance one or carry it through permitting. "
       "And institutional capital will not underwrite a single $4M house. The deals sit in a gap "
       "that stays open because of who is structurally unable to compete for them.",
       "Our edge inside that gap is vertical integration. Construction management sits in-house, "
       "which means cost control and &mdash; more importantly &mdash; schedule control. Schedule "
       "is the dominant variable in these returns: the same margin captured in sixteen months "
       "rather than forty is a fundamentally different investment. 7212&nbsp;Mulholland produced "
       "roughly 84% IRR on a 52% margin because it moved fast; 2731&nbsp;Hutton cleared a thinner "
       "29% margin in nine months and still annualized near 39%.",
       "The submarkets are chosen for exit depth rather than headline prestige. Hollywood Hills, "
       "Beverly Hills, the Sunset Strip, and the Westside carry buyer pools that are largely "
       "equity-driven and therefore less rate-sensitive than the entry-level market &mdash; when "
       "financing tightens, this segment slows but does not stop."],
  pillars=[("Basis","Buy the location, not the house","Acquisition is underwritten against the dated-condition comp set, with the finished value supported by closed sales before we commit."),
           ("Speed","Schedule is the return driver","In-house construction management compresses the build, and every month removed from the hold compounds into IRR."),
           ("Scope","Match the work to the ceiling","Some houses justify an expansion and a four-year hold; most justify a fast, disciplined remodel. The site decides."),
           ("Exit","More than one way out","Sell finished, sell partially completed to a builder, or lease and hold &mdash; each underwritten before acquisition.")],
  risks=["Hillside and geotechnical conditions can carry new-construction scope under a remodel "
         "permit. 8070&nbsp;Laurelmont is the disclosed example: retaining walls and 30+ caissons "
         "materially exceeded pricing, and forty-eight months of carry converted a project-level "
         "profit into a 0.73x equity outcome. Pre-acquisition geotechnical investigation is now "
         "required on every hillside deal.",
         "The upper-end buyer pool is deep but not infinite; in a sharp downturn, absorption at "
         "$5M+ slows before it slows at $1.5M.",
         "Long holds compound debt carry. Maximum-duration limits are set in underwriting, and a "
         "severe-downside case testing the equity outcome &mdash; not just the project margin "
         "&mdash; is required at investment committee."],
  ent=[],
  con=[card("85th.jpg","&ldquo;The Kentwood Farmhouse&rdquo;","6450 W 85th St &middot; Westchester &middot; AC V LLC","In Construction", "../portfolio.html",
            [("Q1 2027","Target sale"),("Dual","Product")])],
  done=[card("gonzaga.webp","&ldquo;The Gonzaga Residence&rdquo;","8404 Gonzaga Ave &middot; Assemble Capital LLC","Completed","../properties/gonzaga-residence.html"),
        card("berryman-home.jpg","&ldquo;The Berryman Residence&rdquo;","4432 Berryman Ave &middot; AC II LLC","Completed","../properties/berryman-residence.html"),
        card("apex.webp","&ldquo;The Apex HH&rdquo;","7115 Macapa Dr &middot; Sold $8.65M &middot; 3.21x","Completed","../properties/apex-hh.html"),
        card("hideaway.webp","&ldquo;The Hideaway HH&rdquo;","7932 Woodrow Wilson Dr &middot; Sold $6.75M &middot; 2.54x","Completed","../properties/hideaway-hh.html"),
        card("villa-de-vistas.webp","&ldquo;Villa De Vistas&rdquo;","7212 Mulholland Dr &middot; Sold $6.40M &middot; 2.68x","Completed","../properties/villa-de-vistas.html"),
        card("macapa-oasis-hd.jpg","&ldquo;The Macapa Oasis&rdquo;","7123 Macapa Dr &middot; Sold $7.25M","Completed","../properties/macapa-oasis.html"),
        card("treehouse.webp","&ldquo;The Treehouse HH&rdquo;","8070 Laurelmont Dr &middot; Sold $7.00M &middot; 0.73x","Completed","../properties/treehouse-hh.html"),
        card("hutton-marvel.webp","&ldquo;The Hutton Marvel&rdquo;","2731 Hutton Dr &middot; Sold $3.90M &middot; 9-month turn","Completed","../properties/hutton-marvel.html")],
  more=("Five additional completed single-family projects &mdash; Rising Glen MCM, The Hollywood Marvel, "
        "Villa De Edinburgh, The Modern Orange, The Martha MCM, and Paseo Moderna &mdash; are documented on the "
        '<a href="../track-record.html">track record</a>.'),
  ),

dict(slug="boutique-multifamily", eyebrow="Strategy 02 &middot; MF&ndash;Dev",
  name="Opportunistic &amp; Value Add<br>Multifamily Development",
  hero="calvert-home.jpg",
  sub="Ground-up four to fourteen unit buildings &mdash; sold stabilized, or refinanced into term debt and held.",
  specs=[("4 &ndash; 20","Units per project"),("12 &ndash; 30 mo","Build duration"),
         ("&ge; ~1.20 &ndash; 1.25x","Refinance DSCR discipline"),("2","Exit pathways underwritten")],
  lede="Los Angeles is structurally short of housing, and the law has recently made small buildings far easier to build.",
  why=["The supply case is not a forecast &mdash; it is arithmetic. Los Angeles has permitted "
       "housing well below household formation for years, and the constraint has been regulatory "
       "as much as economic. A sequence of state legislation has shifted meaningful categories of "
       "small multifamily from discretionary approval into ministerial pathways, which removes the "
       "political risk that historically made these projects unfinanceable.",
       "Four to fourteen units is a deliberate band. Below four, the economics do not carry the "
       "fixed costs of development. Above roughly fifteen, projects begin crossing thresholds "
       "&mdash; financing complexity, prevailing-wage exposure, and the size at which institutional "
       "developers compete &mdash; that erase the advantage of being small and fast.",
       "The structural benefit of this strategy is optionality at the end. A stabilized building "
       "can be sold to an investor at a cap rate, or refinanced into term debt and held. That "
       "choice is made at completion, with real market information, rather than committed to at "
       "acquisition. It means we are never forced to sell into a bad cap-rate environment to "
       "return capital.",
       "Three of our four delivered buildings were refinanced and retained. 10957&nbsp;Calvert "
       "&mdash; fourteen units &mdash; carries an equity mark of roughly $3.30M against $1.15M "
       "invested. Those marks are unrealized: they are appraised value less first trust deed debt, "
       "not proceeds, and they will not become proceeds until the buildings trade."],
  pillars=[("Supply","Build where the shortage is","Concentrated in North Hollywood and Hollywood-adjacent submarkets with deep, consistent rental demand."),
           ("Scale","Deliberately boutique","Large enough to carry development cost, small enough to stay below the thresholds that attract institutional competition."),
           ("Optionality","Decide the exit at the end","Sell stabilized or refinance and hold &mdash; the choice is made with market information, not assumed at acquisition."),
           ("Coverage","Underwrite to debt service","Refinance discipline targets DSCR at or above roughly 1.20&ndash;1.25x, with coverage disclosed per asset.")],
  risks=["Debt service coverage is the live risk on held assets. 5651&nbsp;Case sits at 1.01x DSCR "
         "&mdash; minimal cushion against vacancy or rate movement, and the reason that asset is "
         "monitored most closely. Coverage is disclosed per building rather than blended away.",
         "Equity marks on retained buildings are unrealized and levered. A modest decline in "
         "appraised value produces a disproportionate decline in the equity mark.",
         "Construction cost, lease-up timing, and rent regulation each affect outcomes, and "
         "refinancing depends on credit markets that are outside our control."],
  ent=[],
  con=[],
  done=[card("calvert-home.jpg","&ldquo;The Calvert XIV&rdquo;","10957 Calvert St &middot; 14 units &middot; Refinanced &amp; held","Held &middot; 2.9x to date","../properties/calvert-xiv.html"),
        card("case.webp","&ldquo;The Case V&rdquo;","5651 Case Ave &middot; 5 units &middot; Refinanced &amp; held","Held &middot; 2.4x to date","../properties/case-v.html"),
        card("june.webp","&ldquo;The June IV&rdquo;","1323 N June St &middot; 4 units &middot; Refinanced &amp; held","Held &middot; 3.7x to date","../properties/june-iv.html"),
        card("hortense.webp","&ldquo;The Hortense VI&rdquo;","10742 Hortense St &middot; 6 units &middot; Sold $4.20M","Sold &middot; 1.85x","../properties/hortense-vi.html")],
  more=("The three retained buildings carry $15.85M of combined stabilized value, roughly $938K of annual "
        "net operating income, and a 1.33x blended DSCR at 100% occupancy. Those figures are unrealized "
        "equity marks per the SREO dated 7/14/26, not proceeds."),
  pipeline_note=("No boutique multifamily project is currently in entitlement or construction. The "
        "platform's active development capacity is presently committed to fee-simple subdivisions and "
        "the tenancy-in-common project, and new multifamily acquisitions would be capitalized through "
        "future project-specific offerings."),
  ),

dict(slug="infill-subdivisions", eyebrow="Strategy 03 &middot; SB&ndash;684",
  name="SB 684/1123 Fee Simple<br>Subdivisions",
  hero="harter-render.jpg",
  sub="Ministerial small-lot subdivisions under SB&nbsp;684 and SB&nbsp;1123 &mdash; fee-simple homes on individual APNs.",
  specs=[("4 &ndash; 10","Homes per project"),("$1M &ndash; $1.5M","End-user pricing"),
         ("Months, not years","Entitlement timeline"),("Bulk sale","Fallback underwritten")],
  lede="A change in state law turned a multi-year political process into an administrative one. That is the whole opportunity.",
  why=["SB&nbsp;684, expanded by SB&nbsp;1123, created a ministerial approval pathway for small-lot subdivisions on "
       "multifamily-zoned land. Ministerial matters enormously: it means approval is administrative "
       "rather than discretionary &mdash; no public hearing, no discretionary environmental review, "
       "no neighbor appeal that can add three years and kill a project outright. Entitlement stops "
       "being a political risk and becomes a schedule item.",
       "The arbitrage this opens is a valuation mismatch. Multifamily-zoned land is priced on the "
       "income approach &mdash; what a rental building on that site would earn. SB&nbsp;684 lets "
       "the same site deliver individual homes sold to individual buyers at for-sale pricing, which "
       "on a per-square-foot basis is materially higher than income-based value. We are buying "
       "land at one valuation basis and exiting it at another.",
       "The fee-simple structure is what makes the exit work. Each home sits on its own legal lot "
       "with its own APN, so buyers use conventional mortgage financing rather than the specialized "
       "loans a TIC or condo-alternative structure requires. That widens the buyer pool to "
       "essentially every qualified homebuyer in the price band &mdash; a decisive advantage over "
       "structures that ask buyers to accept unfamiliar financing.",
       "Being early is a real and temporary edge. Few operators in the region have executed this "
       "pathway; The Culver&nbsp;VI at 3850&nbsp;Westwood was the first ministerial approval in Culver City. While the field is "
       "thin, sites can still be acquired at bases set by the old rental-value assumption. That "
       "window narrows as the statute becomes better understood."],
  pillars=[("Regulatory","Ministerial, not discretionary","No hearing, no discretionary review, no appeal &mdash; entitlement becomes a timeline rather than a political outcome."),
           ("Arbitrage","Buy on income value, sell on for-sale value","Land priced as rental product, exited as individual homes at for-sale pricing."),
           ("Financing","Fee-simple widens the buyer pool","Individual APNs mean conventional mortgages, not specialized fractional lending."),
           ("Absorption","Release units, don't dump them","Homes are sold on a unit-release schedule as the market absorbs, with a bulk-sale fallback underwritten from acquisition.")],
  risks=["SB&nbsp;684 is a recent statute and jurisdictions interpret and administer it "
         "differently. Processing timelines, plan-check standards, and local implementation vary, "
         "and the law itself could be amended.",
         "Affordable-housing obligations apply on these projects and are disclosed per deal.",
         "Sellout is absorption-dependent: each home waits on its own buyer and financing. The "
         "bulk-sale fallback value is underwritten before acquisition precisely because the "
         "unit-by-unit path may take longer than modeled.",
         "Three of the active projects carry construction cost above current loan commitments; "
         "each requires a construction refinancing, and investor-level return projections are "
         "intentionally withheld until that capitalization is reconciled."],
  ent=[card("westwood.jpg","&ldquo;The Culver VI&rdquo;","3850 Westwood &middot; Culver City &middot; AC III LLC","In Entitlements","../portfolio.html",[("Q4 2027","Target sellout"),("Fee-simple","Exit")]),
       card("harter-render.jpg","&ldquo;The Harter V&rdquo;","4058 Harter &middot; Culver City &middot; AC VI LLC","In Entitlements","../portfolio.html",[("Q1 2028","Target sellout"),("Fee-simple","Exit")]),
       card("helms-render.jpg","&ldquo;The Helms VI&rdquo;","3562 Helms &middot; Culver City &middot; AC VII LLC","In Entitlements","../portfolio.html",[("Q1 2028","Target sellout"),("Fee-simple","Exit")])],
  con=[],
  done=[],
  more=("The pathway was proven at 1949&nbsp;17th&nbsp;St, a principal-owned project: ministerial "
        "approval, fee-simple homes on individual APNs, conventional buyer financing, and a "
        "unit-release sellout. No Assemble Capital SB&nbsp;684 project has completed a sellout yet "
        "&mdash; all three active projects are in entitlement, with construction refinancings "
        "planned from Q4&nbsp;2026."),
  pipeline_note=None,
  ),

dict(slug="tic-housing", eyebrow="Strategy 04 &middot; TIC",
  name="Tenancy-In-Common<br>Housing",
  hero="david.webp",
  sub="Small multifamily sold as individual tenancy-in-common homes at a premium to bulk value.",
  specs=[("3 &ndash; 4","Units per project"),("18 &ndash; 30 mo","Sellout window"),
         ("Premium to bulk","Pricing objective"),("Bulk sale","Fallback underwritten")],
  lede="An investor buys a cap rate. A homeowner buys a home. The gap between those two prices is the strategy.",
  why=["Tenancy-in-common allows a small apartment building to be sold as individual homes to "
       "individual buyers, each taking an undivided fractional interest with exclusive right to "
       "occupy a specific unit. It exists because condominium conversion in Los Angeles is heavily "
       "restricted &mdash; TIC is the structure that reaches the for-sale buyer in buildings that "
       "cannot legally be condo-mapped.",
       "The economics come from who is bidding. An investor purchasing a three-unit building "
       "prices it on income &mdash; rents, expenses, a cap rate. Three separate homebuyers price "
       "the same square footage as places to live. On a small building that spread between "
       "aggregate unit value and bulk value is meaningful, and capturing it is the entire thesis.",
       "The structural constraint used to be financing: TIC buyers historically needed to pay cash "
       "or take a shared blanket loan. Fractional TIC lending has matured, with multiple lenders "
       "now writing individual loans against individual interests, which is what makes the "
       "strategy executable at scale rather than a curiosity.",
       "The tradeoff is honest and it is absorption. Each unit waits on its own buyer securing "
       "their own financing, and a sellout takes time. 5832&nbsp;David returned 1.41x and roughly "
       "17% IRR over 26 months &mdash; the most modest of our realized exits. What that project "
       "bought was a documented, executed template, which is now being applied at "
       "1925&nbsp;19th&nbsp;St."],
  pillars=[("Pricing","Sell to homeowners, not cap rates","Unit buyers pay for a home; the spread over bulk investor value is the return driver."),
           ("Structure","TIC where condo mapping is closed","The legal structure that reaches for-sale buyers in buildings that cannot be condo-mapped."),
           ("Financing","Fractional lending has matured","Individual TIC loans are now available from multiple lenders &mdash; the constraint that historically limited this strategy."),
           ("Discipline","Underwrite the fallback first","Bulk-sale value, partial-release terms, and absorption assumptions are set before acquisition, not after.")],
  risks=["Absorption is the dominant risk. Three or four units each require their own buyer and "
         "their own loan, and a slow sellout extends carry against the whole project.",
         "TIC buyer financing depends on a small set of lenders. If fractional lending tightens, "
         "the buyer pool narrows quickly.",
         "TIC ownership is less familiar than fee-simple, which requires buyer education and can "
         "lengthen marketing timelines relative to conventional for-sale product.",
         "Partial-release requirements with the construction lender govern how and when individual "
         "units can close, and those terms materially affect the sellout schedule."],
  ent=[card("samo.webp","&ldquo;The SAMO IV&rdquo;","1925 19th St &middot; Santa Monica &middot; AC IV LLC","In Entitlements &middot; TIC","../portfolio.html",[("4 units","Program"),("Q4 2027","Target sellout")])],
  con=[],
  done=[card("david.webp","&ldquo;The David III&rdquo;","5832 David Ave &middot; Ground-up triplex &middot; 3 fee-simple TIC units","Sold as TIC &middot; $2.91M","../properties/david-iii.html",[("1.41x","Multiple"),("~17%","IRR"),("26 mo","Hold")])],
  more=("5832&nbsp;David was sold as three separate TIC units across closings from November&nbsp;2025 "
        "through February&nbsp;2026. It is the executed proof of the pathway now being applied at "
        "1925&nbsp;19th&nbsp;St in Santa Monica."),
  pipeline_note=None,
  ),
]

# ------------------------------------------------------------------ build
def build(s):
    specs = "".join(f'      <div class="cell"><div class="num">{v}</div><div class="lbl">{l}</div></div>\n'
                    for v, l in s["specs"])
    why = "\n".join(f"      <p>{p}</p>" for p in s["why"])
    pillars = "\n".join(
        f'      <div class="pillar"><div><div class="k">{k}</div><h3>{t}</h3></div><p>{d}</p></div>'
        for k, t, d in s["pillars"])
    risks = "\n".join(f'        <li style="padding:1rem 0;border-bottom:1px solid var(--line);font-size:.94rem">{r}</li>'
                      for r in s["risks"])

    sections = ""
    sections += stage("In entitlements.", "Current Projects",
                      None, s["ent"], warm=True, stamp="Approval pipeline")
    sections += stage("In construction.", "Current Projects",
                      None, s["con"], warm=not s["ent"], stamp="Underway")
    warm_done = not (bool(s["ent"]) ^ bool(s["con"]))
    sections += stage("Completed." if s["done"] else "", "Track Record",
                      s.get("more"), s["done"], warm=warm_done, stamp="Delivered")

    pipeline = ""
    if s.get("pipeline_note"):
        pipeline = f'''
<section class="tight">
  <div class="wrap">
    <p class="footnote reveal" style="max-width:52rem">{s["pipeline_note"]}</p>
  </div>
</section>'''
    elif not s["done"] and s.get("more"):
        pipeline = f'''
<section class="tight">
  <div class="wrap">
    <p class="footnote reveal" style="max-width:52rem">{s["more"]}</p>
  </div>
</section>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{s["name"].replace("<br>", " ")} &mdash; Assemble Capital</title>
<meta name="description" content="{s['sub']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Assemble Capital">
<meta property="og:url" content="https://assemble.capital/strategies/{s['slug']}.html">
<meta property="og:title" content="{s["name"].replace("<br>", " ")} &mdash; Assemble Capital">
<meta property="og:description" content="{s['sub']}">
<meta property="og:image" content="https://assemble.capital/assets/img/{s['hero']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{s["name"].replace("<br>", " ")} &mdash; Assemble Capital">
<meta name="twitter:description" content="{s['sub']}">
<meta name="twitter:image" content="https://assemble.capital/assets/img/{s['hero']}">
{FONTS}
<link rel="stylesheet" href="../css/style.css?v=3">
{FAVICON}
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>

{header()}

<main id="main">

<section class="hero short" style="padding:0">
  <div class="bg" style="background-image:url('../assets/img/{s["hero"]}')"></div>
  <div class="wrap">
    <p class="eyebrow">{s["eyebrow"]}</p>
    <h1 class="display">{s["name"]}</h1>
    <p class="sub">{s["sub"]}</p>
  </div>
</section>

<!-- UNDERWRITING TARGETS -->
<section>
  <div class="wrap">
    <div class="ledger reveal">
{specs}    </div>
    <p class="footnote reveal" style="margin-top:1.2rem">Underwriting targets, not promises or guarantees. Individual investments may vary; final parameters are governed by each investment's definitive documents.</p>
  </div>
</section>

<!-- WHY THIS STRATEGY -->
<section class="on-dark">
  <div class="wrap split reveal">
    <div>
      <p class="eyebrow">The Reasoning</p>
      <p class="lede">{s["lede"]}</p>
    </div>
    <div>
{why}
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section>
  <div class="wrap">
    <div class="reveal" style="max-width:46rem;margin-bottom:2.6rem">
      <p class="eyebrow">How It Works</p>
      <h2 class="h-lg">Four things this strategy depends on.</h2>
    </div>
    <div class="pillars reveal">
{pillars}
    </div>
  </div>
</section>
{sections}{pipeline}
<!-- RISKS -->
<section class="on-dark">
  <div class="wrap split reveal" style="align-items:start">
    <div>
      <p class="eyebrow">What Can Go Wrong</p>
      <h2 class="h-lg">The risks we underwrite against.</h2>
      <p class="muted" style="max-width:30rem">Every strategy has a failure mode. These are the ones specific to this one &mdash; the complete risk disclosure for any investment lives in its offering documents.</p>
    </div>
    <div>
      <ul style="list-style:none;padding:0;margin:0;border-top:1px solid var(--line)">
{risks}
      </ul>
    </div>
  </div>
</section>

<!-- CTA -->
<section class="cta-band on-warm">
  <div class="wrap reveal">
    <p class="eyebrow">Future Opportunities</p>
    <h2 class="h-lg">Want to invest in the next one?</h2>
    <p class="muted" style="max-width:42rem;margin:1.4rem auto 0">Future projects in this strategy are capitalized through new project-specific offerings &mdash; an 8% preferred return paid before the sponsor participates, Class&nbsp;A participation in the profits, and our own capital in every deal. Get in touch and we'll walk you through the model, the pipeline, and what a specific offering looks like.</p>
    <div class="actions">
      <a class="btn" style="border-color:var(--line-strong)" href="../contact.html">Contact us about investing</a>
      <a class="btn" style="border-color:var(--line-strong)" href="../strategies.html#model">See how the structure works</a>
    </div>
    <p class="footnote" style="margin-top:1.8rem;max-width:44rem;margin-left:auto;margin-right:auto">Contacting us is not an offer, commitment, or investment. Any offering is made only through definitive offering documents to eligible investors.</p>
  </div>
</section>

<!-- OTHER STRATEGIES -->
<section>
  <div class="wrap">
    <p class="eyebrow reveal">Other Strategies</p>
    <div class="grid-3 reveal">
{other_links(s["slug"])}
    </div>
  </div>
</section>

</main>

{footer()}

<script src="../js/main.js"></script>
</body>
</html>
'''

NAMES = {"luxury-redevelopment": ("Luxury Residential Development", "Studs-out rebuilds and heavy remodels in prime submarkets."),
         "boutique-multifamily": ("Opportunistic &amp; Value Add Multifamily Development", "Ground-up 4&ndash;20-unit multifamily projects, sold or held."),
         "infill-subdivisions": ("SB 684/1123 Fee Simple Subdivisions", "Ministerial SB&nbsp;684/1123 small-lot subdivisions."),
         "tic-housing": ("Tenancy-In-Common Housing", "Small multifamily sold as individual TIC homes.")}

def other_links(slug):
    out = []
    for k, (n, d) in NAMES.items():
        if k == slug: continue
        out.append(f'''      <a href="{k}.html" style="border:1px solid var(--line);padding:1.8rem;text-decoration:none;display:block">
        <h3 class="h-md" style="font-size:1.35rem">{n}</h3>
        <p class="muted" style="font-size:.9rem;margin:.5rem 0 0">{d}</p>
      </a>''')
    return "\n".join(out)

os.makedirs(OUT, exist_ok=True)
for s in S:
    with open(os.path.join(OUT, s["slug"] + ".html"), "w") as f:
        f.write(build(s))
    print("wrote strategies/" + s["slug"] + ".html")
print("TOTAL", len(S))


# --- keep SEO/506(b) metadata authoritative -------------------------------
# This generator emits a baseline <head>. tools-apply-seo-metadata.py owns the
# canonical/robots/OG/Twitter/JSON-LD block, so re-apply it after every build.
import subprocess as _sp
_sp.run(["python3", os.path.join(SITE, "tools-apply-seo-metadata.py")], check=True)
