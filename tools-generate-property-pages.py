#!/usr/bin/env python3
"""Generate individual property pages for the Assemble Capital site."""
import os, json

SITE = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(SITE, "assets", "img", "properties")

# ---------------------------------------------------------------- data
# cat: sf | mf | tic
P = [
 dict(slug="apex-hh", name="The Apex HH", addr="7115 Macapa Dr", sub="Hollywood Hills",
   cat="sf", hero="apex.webp", badge="Sold &middot; $8.65M", years="2019 &ndash; 2023",
   strategy="Studs-out remodel + FAR expansion", status="Sold",
   cost="$5.55M", exit="$8.65M", profit="$3.10M", poc="55.9%",
   eq=dict(inv="$1,274,516", ret="$4,093,460", prof="$2,818,944", hold="47", mom="3.21x", irr="~37%"),
   stats=[("$8.65M","Sale price &mdash; neighborhood record"),("3.21x","Equity multiple"),
          ("~37%","Deal-level IRR"),("47 mo","Hold period")],
   lede="The highest-multiple exit in the portfolio &mdash; and a lesson in what patience buys.",
   bg=["Acquired in 2019 as an under-improved hillside home on a street the principals had "
       "worked for over a decade. The thesis was floor area: the lot carried unused FAR that a "
       "buyer pool focused on existing square footage had consistently overlooked.",
       "The business plan was a studs-out rebuild paired with an expansion &mdash; the harder, "
       "slower path, but the one that repositioned the house into a different price tier entirely. "
       "Mid-hold, a $1.67M second trust deed recapitalization returned capital to the sponsor while "
       "the remaining equity stayed at risk through completion.",
       "The home sold in 2023 for $8.65M, a neighborhood record at the time of closing, returning "
       "$4.09M on $1.27M of equity over a 47-month hold."],
   cycle=[("Acquire","2019","Off-market hillside acquisition at a basis that priced the house, not the unused floor area."),
          ("Design &amp; permit","2019&ndash;2021","Expansion design and hillside permitting &mdash; the long pole, and the source of the margin."),
          ("Build","2021&ndash;2022","Studs-out rebuild executed with in-house construction management."),
          ("Recapitalize","Mid-hold","A $1.67M second trust deed returned capital early while equity stayed at risk."),
          ("Exit","2023","Sold at $8.65M &mdash; a neighborhood record at closing.")],
   lesson="Complexity premium plus patient expansion. The unused FAR was visible to anyone who pulled the zoning; converting it took four years of execution."),

 dict(slug="hideaway-hh", name="The Hideaway HH", addr="7932 Woodrow Wilson Dr", sub="Celebrity Row, Hollywood Hills",
   cat="sf", hero="hideaway.webp", badge="Sold &middot; $6.75M", years="2021 &ndash; 2023",
   strategy="Studs-out rebuild", status="Sold",
   cost="$3.60M", exit="$6.75M", profit="$3.15M", poc="87.6%",
   eq=dict(inv="$1,500,000", ret="$3,805,728", prof="$2,305,728", hold="24", mom="2.54x", irr="~57%"),
   stats=[("$6.75M","Sale price &mdash; record sale"),("2.54x","Equity multiple"),
          ("~57%","Deal-level IRR"),("87.6%","Gross profit on cost")],
   lede="The clearest demonstration in the portfolio that speed is a return driver.",
   bg=["Celebrity Row is one of the most recognizable addresses in the Hollywood Hills, and one "
       "where buyers pay for finish quality and view framing above almost anything else. The house "
       "was structurally sound and architecturally dated &mdash; the profile the team targets.",
       "Rather than pursue an expansion, the plan stayed on the remodel pathway: a full studs-out "
       "rebuild inside the existing envelope, which avoided the entitlement timeline entirely and "
       "moved the project from acquisition to a finished, market-ready home in roughly two years.",
       "The house sold for $6.75M &mdash; a record on the street &mdash; turning $1.5M of equity "
       "into $3.81M returned. At 87.6% gross profit on cost, it is the highest-margin project in "
       "the 21-project schedule."],
   cycle=[("Acquire","2021","Acquired on Celebrity Row at a basis supported by dated finishes, not location."),
          ("Design","2021","Interior-only scope defined to stay inside the existing envelope and skip entitlement."),
          ("Build","2021&ndash;2023","Studs-out rebuild &mdash; full systems, finishes, and view-framing glazing."),
          ("Market","2023","Listed into the strongest comparable set on the street."),
          ("Exit","2023","Sold at $6.75M in roughly 24 months from acquisition.")],
   lesson="Remodel-pathway speed converted directly into IRR. The same margin over four years would have been a materially worse investment."),

 dict(slug="villa-de-vistas", name="Villa De Vistas", addr="7212 Mulholland Dr", sub="Hollywood Hills",
   cat="sf", hero="villa-de-vistas.webp", badge="Sold &middot; $6.40M", years="2021 &ndash; 2022",
   strategy="Remodel + refinance", status="Sold",
   cost="$4.20M", exit="$6.40M", profit="$2.20M", poc="52.4%",
   eq=dict(inv="$700,000", ret="$1,872,710", prof="$1,172,710", hold="16", mom="2.68x", irr="~84%"),
   stats=[("~84%","Deal-level IRR &mdash; highest in portfolio"),("2.68x","Equity multiple"),
          ("16 mo","Hold period"),("$878K","Refinance proceeds mid-hold")],
   lede="The highest IRR in the portfolio, built on a short hold and an early return of capital.",
   bg=["A Mulholland property acquired with a defined, narrow scope: the house needed a "
       "comprehensive remodel, not a rebuild, and the underwriting was built around getting in and "
       "out before the carry could compound.",
       "Mid-hold, an $878K refinance returned a substantial portion of capital to the sponsor while "
       "the position remained at risk through the sale &mdash; the mechanic that drove the IRR. "
       "Refinance proceeds are not profit; they accelerate the timing of capital coming back, which "
       "is precisely what a time-weighted return measures.",
       "The property sold within roughly seven months of close of escrow at $6.40M. Total returned "
       "was $1.87M on $700K of equity across a 16-month hold &mdash; approximately 84% IRR."],
   cycle=[("Acquire","2021","Purchased with a remodel-only scope and a defined exit window."),
          ("Build","2021&ndash;2022","Comprehensive remodel executed on a compressed schedule."),
          ("Refinance","Mid-hold","$878K refinance returned capital early; remaining equity stayed at risk."),
          ("Market","2022","Listed immediately upon completion into a strong comp set."),
          ("Exit","2022","Sold at $6.40M roughly seven months after close of escrow.")],
   lesson="Refinance as a return-of-capital tool. Time-weighted returns reward getting capital back early, even when total profit is unchanged."),

 dict(slug="macapa-oasis", name="The Macapa Oasis", addr="7123 Macapa Dr", sub="Outpost Estates",
   cat="sf", hero="macapa-oasis-hd.jpg", badge="Sold &middot; $7.25M", years="2009 &ndash; 2020",
   strategy="Expand &amp; spec rebuild", status="Sold",
   cost="$2.75M", exit="$7.25M", profit="$4.50M", poc="163.6%",
   eq=dict(inv="$1,000,000", ret="$1,612,783", prof="$612,783", hold="18", mom="1.61x", irr="~37%"),
   stats=[("$7.25M","Sale price &mdash; Outpost Estates record"),("163.6%","Gross profit on cost"),
          ("1.61x","Equity multiple &mdash; spec phase"),("$4.50M","Gross project profit")],
   lede="The largest gross profit in the portfolio &mdash; and the longest story behind it.",
   bg=["7123 Macapa was RC Thornton's primary residence for over a decade before it was "
       "redeveloped. That history matters to reading the numbers: the acquisition basis dates to "
       "2009, and the gross project economics span an eleven-year ownership, not an eleven-year "
       "development.",
       "The redevelopment itself &mdash; a substantial expansion and spec-quality rebuild &mdash; "
       "was executed over an 18-month phase at the end of that hold, which is the window the equity "
       "return reflects. The house was rebuilt to a specification aimed squarely at the top of the "
       "Outpost Estates market rather than a mid-market renovation.",
       "It sold in 2020 for $7.25M &mdash; at the time, the most expensive sale ever recorded in "
       "Outpost Estates. Gross project profit was $4.50M, the largest single-project profit in the "
       "21-project schedule."],
   cycle=[("Acquire","2009","Purchased as a primary residence; held through two market cycles."),
          ("Reposition","2019","Redevelopment scope defined &mdash; expansion plus spec-level rebuild."),
          ("Build","2019&ndash;2020","18-month expansion and rebuild phase executed in-house."),
          ("Market","2020","Listed at the top of the Outpost Estates comparable set."),
          ("Exit","2020","Sold at $7.25M &mdash; the submarket's highest recorded sale at closing.")],
   lesson="Gross project profit and equity multiple answer different questions. Both are shown here because only reporting the larger number would misrepresent the return.",
   note="Equity figures reflect the 18-month spec expansion, rebuild, and sale phase. The property was RC Thornton's primary residence prior to redevelopment, and the project-level economics span the full ownership period from 2009."),

 dict(slug="treehouse-hh", name="The Treehouse HH", addr="8070 Laurelmont Dr", sub="Mount Olympus",
   cat="sf", hero="treehouse.webp", badge="Sold &middot; $7.00M", years="2021 &ndash; 2024",
   strategy="Studs-out rebuild &mdash; hillside flag lot", status="Sold",
   cost="$5.10M", exit="$7.00M", profit="$1.90M", poc="37.3%",
   eq=dict(inv="$1,000,000", ret="$733,829", prof="($266,171)", hold="48", mom="0.73x", irr="~(8%)"),
   loss=True,
   stats=[("$7.00M","Sale price"),("0.73x","Equity multiple &mdash; capital loss"),
          ("$1.90M","Gross project profit"),("48 mo","Hold period")],
   lede="Gross-profitable at the project level. A loss at the equity level. Both are true, and we publish both.",
   bg=["A hillside flag-lot rebuild in Mount Olympus that carried genuine new-construction scope "
       "under a remodel permit &mdash; new retaining walls and more than thirty caissons. The "
       "structural work materially exceeded the original pricing, and on a hillside site that "
       "overage is not recoverable through value engineering.",
       "The extended timeline is what converted a cost overrun into an equity loss. Forty-eight "
       "months of debt carry and partner-level costs compounded against a project that did generate "
       "roughly $1.9M of gross profit at the property level on a $5.1M total cost when it sold for "
       "$7.0M in 2024.",
       "At the sponsor-equity level, the deal returned $733,829 on $1,000,000 invested &mdash; a "
       "0.73x multiple. It is the only capital-impairment outcome across 21 completed projects, and "
       "it is disclosed here for the same reason it appears in the track record: an operator's "
       "record is only useful if it includes the deals that did not work."],
   cycle=[("Acquire","2021","Hillside flag lot acquired with a studs-out remodel scope underwritten."),
          ("Discover","2021&ndash;2022","Structural conditions required retaining walls and 30+ caissons &mdash; new-construction scope under a remodel permit."),
          ("Build","2022&ndash;2023","Extended schedule; debt carry and partner-level costs compounded."),
          ("Market","2024","Listed and sold into a functioning market at $7.0M."),
          ("Exit","2024","Project-level gross profit ~$1.9M; sponsor equity returned 0.73x after debt and carry.")],
   lesson="Project margin is not equity return. Underwriting must test the equity outcome, not just the spread between cost and exit price.",
   controls=["Geotechnical and structural investigation before acquisition on all hillside deals",
             "Hillside-specific contingency and interest-reserve sizing, with maximum-duration limits in underwriting",
             "A severe-downside case required at investment committee &mdash; equity outcome tested, not just project margin",
             "Preference shifted toward ministerial and flatland product (SB&nbsp;684, infill multifamily) at greater scale"]),

 dict(slug="gonzaga-residence", name="The Gonzaga Residence", addr="8404 Gonzaga Ave", sub="Westchester",
   cat="sf", hero="gonzaga.webp", badge="For Sale", years="2024 &ndash; present",
   strategy="Full remodel", status="Complete &mdash; on market",
   cost="$1.85M", exit="$2.80M", profit="$0.95M", poc="51.1%",
   ac=True, zillow="https://www.zillow.com/homedetails/8404-Gonzaga-Ave-Los-Angeles-CA-90045/20384430_zpid/",
   stats=[("5 / 5","Bedrooms / bathrooms"),("2,780","Square feet"),
          ("Westchester","Submarket"),("Complete","Construction status")],
   lede="An Assemble Capital project, complete and on the market in Westchester.",
   bg=["8404 Gonzaga is held in Assemble Capital LLC &mdash; one of the seven active projects on "
       "the current portfolio, and the first of them to reach completion.",
       "Westchester sits in the path of steady owner-user demand: proximity to the Westside and LAX "
       "employment, a deep buyer pool at the upper end of the local market, and a housing stock old "
       "enough that a well-executed full remodel stands clearly apart from its comparable set. "
       "The scope was a comprehensive remodel delivering five bedrooms and five bathrooms across "
       "2,780 square feet.",
       "The home is complete and listed on the open market. It was underwritten to today's closed "
       "comparables before acquisition rather than to future appreciation &mdash; the discipline "
       "that carries across every project. Deal-level economics for this active offering are shared "
       "privately with prospective investors."],
   cycle=[("Acquire","2024","Acquired into Assemble Capital LLC with investor participation."),
          ("Design &amp; permit","2024","Full remodel scope permitted &mdash; no entitlement pathway required."),
          ("Build","2024&ndash;2026","Comprehensive remodel executed under in-house construction management."),
          ("Market","2026","Listed on the open market into the Westchester comparable set."),
          ("Exit","Q3 2026 target","Sale targeted; proceeds distributed per the operating agreement waterfall.")],
   lesson="Underwrite to today's comparables. The Westchester exit was supported by closed sales before the property was acquired."),

 dict(slug="berryman-residence", name="The Berryman Residence", addr="4432 Berryman Ave", sub="Culver City",
   cat="sf", hero="berryman-home.jpg", badge="Completed &middot; For Sale", years="2024 &ndash; present",
   strategy="New construction", status="Complete &mdash; on market",
   cost="", exit="", profit="", poc="",
   ac=True, zillow="https://www.zillow.com/homedetails/4432-Berryman-Ave-Los-Angeles-CA-90230/20438877_zpid/",
   stats=[("6 / 6","Bedrooms / bathrooms"),("3,140","Square feet"),
          ("Culver City","Submarket"),("Complete","Construction status")],
   lede="A completed Assemble Capital project &mdash; ground-up new construction in Culver City, on the market.",
   bg=["4432 Berryman is held in AC&nbsp;II&nbsp;LLC and is one of the seven active Assemble Capital "
       "projects. It is a completed, ground-up new-construction home &mdash; delivered, not a "
       "rendering &mdash; now finished and listed on the open market.",
       "Culver City has become one of the most sought-after submarkets on the Westside: a walkable "
       "core, the Metro E Line, and a concentration of media and tech employment have deepened "
       "buyer demand for well-designed modern homes. The house delivers six bedrooms and six "
       "bathrooms across roughly 3,140 square feet, with an indoor-outdoor plan, white-oak "
       "millwork, and a private landscaped yard.",
       "The project was underwritten to today's closed comparables before acquisition rather than "
       "to future appreciation. Deal-level economics for this active offering are shared privately "
       "with prospective investors."],
   cycle=[("Acquire","2024","Acquired into AC II LLC with investor participation."),
          ("Design &amp; permit","2024","Ground-up new-construction scope designed and permitted."),
          ("Build","2024&ndash;2026","Built under in-house construction management; delivered July 2026."),
          ("Market","2026","Completed and listed on the open market in Culver City."),
          ("Exit","Target","Sale targeted; proceeds distributed per the operating agreement waterfall.")],
   lesson="Build where demand is deepest. Culver City's buyer pool for modern, move-in homes supported the exit underwriting before a shovel hit the ground."),

 dict(slug="hollywood-marvel", name="The Hollywood Marvel", addr="2827 Las Alturas St", sub="Hollywood Hills",
   cat="sf", hero="hollywood-marvel.webp", badge="Sold &middot; $3.22M", years="2016 &ndash; 2019",
   strategy="New construction", status="Sold",
   cost="$1.65M", exit="$3.22M", profit="$1.57M", poc="95.2%",
   stats=[("$3.22M","Sale price"),("95.2%","Gross profit on cost"),
          ("$1.57M","Gross project profit"),("New build","Ground-up construction")],
   lede="A ground-up hillside build that nearly doubled its cost basis.",
   bg=["Las Alturas is a Hollywood Hills street where lot geometry does most of the work &mdash; "
       "buildable envelopes are constrained, and the difference between a site that pencils and one "
       "that does not comes down to how much house the topography will actually carry.",
       "The team acquired the site and built ground-up rather than renovating, delivering a modern "
       "home designed around the view corridor. Total project cost was $1.65M inclusive of land and "
       "construction.",
       "The home sold in 2019 for $3.22M, producing $1.57M of gross project profit &mdash; a 95.2% "
       "gross profit on total cost, among the strongest margins in the schedule."],
   cycle=[("Acquire","2016","Hillside site acquired on buildable-envelope analysis."),
          ("Design &amp; permit","2016&ndash;2017","Ground-up design engineered to the topography and view corridor."),
          ("Build","2017&ndash;2019","New construction delivered under in-house management."),
          ("Market","2019","Listed into the Hollywood Hills new-construction comp set."),
          ("Exit","2019","Sold at $3.22M &mdash; 95.2% gross profit on cost.")],
   lesson="On constrained hillside lots, the yield study is the investment decision. Everything after it is execution."),

 dict(slug="hutton-marvel", name="The Hutton Marvel", addr="2731 Hutton Dr", sub="Beverly Hills",
   cat="sf", hero="hutton-marvel.webp", badge="Sold &middot; $3.90M", years="2007 &ndash; 2008",
   strategy="SFR remodel", status="Sold",
   cost="$3.02M", exit="$3.90M", profit="$0.89M", poc="29.4%",
   stats=[("9 mo","Hold period &mdash; fastest in portfolio"),("~39%","Annualized profit on cost"),
          ("$3.90M","Sale price"),("29.4%","Gross profit on cost")],
   lede="Bought in 2007. Sold in 2008. Profitable through the worst housing market in modern memory.",
   bg=["A Beverly Hills remodel acquired in 2007 &mdash; and sold in 2008, directly into the "
       "financial crisis. The margin is the thinnest of any project on this page at 29.4% gross "
       "profit on cost, and that is the point: the deal worked because it was fast, not because it "
       "was rich.",
       "The scope was a focused SFR remodel with no entitlement component and no structural "
       "expansion, which is what made a nine-month round trip possible. Total project cost was "
       "$3.02M against a $3.90M sale.",
       "Annualized, that 29.4% margin over nine months is roughly 39% profit on cost per year "
       "&mdash; the third-highest annualized figure across all 21 completed projects, achieved in "
       "the single worst year for U.S. residential real estate in living memory."],
   cycle=[("Acquire","2007","Beverly Hills property acquired with a narrow, defined remodel scope."),
          ("Build","2007&ndash;2008","Focused remodel &mdash; no expansion, no entitlement, no structural work."),
          ("Market","2008","Listed immediately on completion as the credit markets deteriorated."),
          ("Exit","2008","Sold at $3.90M in a nine-month round trip.")],
   lesson="Duration is risk. A thin margin captured in nine months outperformed richer deals that took years &mdash; and it cleared the market before conditions could turn against it."),

 dict(slug="rising-glen-mcm", name="Rising Glen MCM", addr="1420 Rising Glen Rd", sub="Sunset Strip",
   cat="sf", hero="rising-glen.webp", badge="Sold &middot; $3.80M", years="2005 &ndash; 2007",
   strategy="SFR remodel", status="Sold",
   cost="$2.55M", exit="$3.80M", profit="$1.25M", poc="49.0%",
   stats=[("2005","First project in the track record"),("$3.80M","Sale price"),
          ("49.0%","Gross profit on cost"),("$1.25M","Gross project profit")],
   lede="Where the track record starts.",
   bg=["1420 Rising Glen is the earliest project in the 21-project schedule &mdash; acquired in "
       "2005, two decades before Assemble Capital existed as a platform. The model being executed "
       "on this page is recognizably the same one running today.",
       "The property is a mid-century home above the Sunset Strip. The scope was a full remodel "
       "that respected the original architecture rather than replacing it, which in this submarket "
       "is a pricing decision as much as a design one &mdash; mid-century provenance carries a "
       "premium that a generic renovation forfeits.",
       "It sold in 2007 for $3.80M against $2.55M of total cost &mdash; $1.25M of gross profit at "
       "a 49% margin on cost, and the beginning of a twenty-year operating history with no notices "
       "of default, foreclosures, or lender workouts."],
   cycle=[("Acquire","2005","Mid-century home above the Sunset Strip acquired for renovation."),
          ("Design","2005&ndash;2006","Scope built around preserving mid-century provenance."),
          ("Build","2006&ndash;2007","Full remodel executed with period-appropriate detailing."),
          ("Exit","2007","Sold at $3.80M &mdash; 49% gross profit on cost.")],
   lesson="In submarkets where architectural provenance is priced, preservation outperforms replacement."),

 dict(slug="villa-de-edinburgh", name="Villa De Edinburgh", addr="138 N Edinburgh Ave", sub="Beverly Grove",
   cat="sf", hero="edinburgh-hd.jpg", badge="Sold &middot; $2.40M", years="2013 &ndash; 2015",
   strategy="New construction", status="Sold",
   cost="$1.73M", exit="$2.40M", profit="$0.68M", poc="39.3%",
   stats=[("$2.40M","Sale price"),("39.3%","Gross profit on cost"),
          ("$0.68M","Gross project profit"),("New build","Ground-up construction")],
   lede="Ground-up infill on a flat Beverly Grove lot &mdash; the low-drama version of the model.",
   bg=["Beverly Grove is dense, flat, and walkable, with a buyer pool that skews toward end users "
       "rather than investors. Flat-lot construction here carries none of the geotechnical risk "
       "that hillside work does, which narrows the range of outcomes in both directions.",
       "The team built ground-up on the site, delivering a new home into a submarket where most "
       "of the competing inventory is decades old. Total project cost was $1.73M.",
       "The home sold in 2015 for $2.40M &mdash; $0.68M of gross profit at a 39.3% margin on cost. "
       "It is a representative outcome rather than a headline one, which is why it sits in the "
       "schedule alongside the record sales."],
   cycle=[("Acquire","2013","Flat infill lot acquired in Beverly Grove."),
          ("Design &amp; permit","2013&ndash;2014","By-right ground-up design permitted without entitlement risk."),
          ("Build","2014&ndash;2015","New construction delivered on a flat, low-complexity site."),
          ("Exit","2015","Sold at $2.40M &mdash; 39.3% gross profit on cost.")],
   lesson="Flat-lot infill trades upside for predictability. A portfolio needs both."),

 dict(slug="modern-orange", name="The Modern Orange", addr="465 S Orange Grove", sub="Los Angeles",
   cat="sf", hero="modern-orange-hd.jpg", badge="Sold &middot; $2.77M", years="2014 &ndash; 2015",
   strategy="New construction", status="Sold",
   cost="$1.84M", exit="$2.77M", profit="$0.93M", poc="50.8%",
   stats=[("~41%","Annualized profit on cost &mdash; best in portfolio"),("15 mo","Hold period"),
          ("$2.77M","Sale price"),("50.8%","Gross profit on cost")],
   lede="The best annualized return across all 21 completed projects.",
   bg=["465 S Orange Grove produced a 50.8% gross profit on cost &mdash; strong, but not the "
       "highest margin in the schedule. What sets it apart is that the project delivered that "
       "margin in fifteen months.",
       "It was a ground-up build on an infill lot with a by-right pathway, which is the "
       "configuration that compresses timelines: no entitlement hearings, no variance risk, and a "
       "construction program that could start as soon as plans cleared.",
       "Annualized over the actual hold, the return works out to roughly 41% profit on cost per "
       "year &mdash; the highest annualized figure in the portfolio, ahead of projects that "
       "generated far larger absolute profits over far longer holds."],
   cycle=[("Acquire","2014","By-right infill lot acquired with a defined construction program."),
          ("Permit","2014","Plans cleared without entitlement hearings or variance risk."),
          ("Build","2014&ndash;2015","Ground-up construction executed on a compressed schedule."),
          ("Exit","2015","Sold at $2.77M &mdash; 50.8% on cost in 15 months, ~41% annualized.")],
   lesson="Annualized return is the honest comparison. A 50% margin in 15 months and a 50% margin in 50 months are not the same investment."),

 dict(slug="martha-mcm", name="The Martha MCM", addr="14918 Martha St", sub="Sherman Oaks",
   cat="sf", hero="martha.webp", badge="Sold &middot; $1.45M", years="&ndash; 2018",
   strategy="New construction", status="Sold",
   cost="$0.91M", exit="$1.45M", profit="$0.54M", poc="59.3%",
   stats=[("$1.45M","Sale price"),("59.3%","Gross profit on cost"),
          ("$0.54M","Gross project profit"),("New build","Ground-up construction")],
   lede="Valley ground-up construction at an entry price point &mdash; and a 59% margin.",
   bg=["Sherman Oaks carries consistent family-buyer demand at price points well below the "
       "Westside, and the arithmetic of development changes accordingly: smaller absolute profits, "
       "but margins that hold up because land basis stays proportionate to exit value.",
       "The project was a ground-up mid-century-informed build on a Valley lot, delivered at a "
       "total project cost of $0.91M &mdash; the second-lowest cost basis of any project in the "
       "schedule.",
       "It sold in 2018 for $1.45M, producing $0.54M of gross profit at a 59.3% margin on cost "
       "&mdash; a higher margin than most of the multi-million-dollar Hollywood Hills projects "
       "alongside it."],
   cycle=[("Acquire","&mdash;","Valley infill lot acquired at a low cost basis."),
          ("Design &amp; permit","&mdash;","Mid-century-informed ground-up design permitted by right."),
          ("Build","&mdash;2018","New construction delivered for a family-buyer end user."),
          ("Exit","2018","Sold at $1.45M &mdash; 59.3% gross profit on cost.")],
   lesson="Margin percentage and absolute profit tell different stories. Smaller Valley projects have repeatedly out-margined larger hillside ones."),

 dict(slug="paseo-moderna", name="Paseo Moderna", addr="3406 The Paseo", sub="Los Angeles",
   cat="sf", hero="paseo.webp", badge="Sold &middot; $1.14M", years="2013 &ndash; 2016",
   strategy="New construction", status="Sold",
   cost="$0.75M", exit="$1.14M", profit="$0.40M", poc="53.3%",
   stats=[("$1.14M","Sale price"),("53.3%","Gross profit on cost"),
          ("$0.75M","Total project cost &mdash; lowest in portfolio"),("New build","Ground-up construction")],
   lede="The smallest project in the portfolio, at a 53% margin.",
   bg=["At $0.75M of total project cost, Paseo Moderna is the smallest development in the "
       "21-project schedule &mdash; and a useful demonstration that the underwriting discipline "
       "does not change with deal size.",
       "The scope was a straightforward ground-up build with no entitlement complexity, designed "
       "for an entry-level buyer pool where finish quality and efficient layout matter more than "
       "square footage.",
       "It sold in 2016 for $1.14M &mdash; $0.40M of gross profit at a 53.3% margin on cost, in "
       "line with the portfolio's 51.1% median despite being a fraction of the size of the "
       "projects around it."],
   cycle=[("Acquire","2013","Small infill lot acquired at the portfolio's lowest cost basis."),
          ("Permit","2013&ndash;2014","Straightforward by-right permitting."),
          ("Build","2014&ndash;2016","Ground-up construction for an entry-level buyer pool."),
          ("Exit","2016","Sold at $1.14M &mdash; 53.3% gross profit on cost.")],
   lesson="The buy box has a floor, not a ceiling on discipline. Small projects get the same downside test as large ones."),

 # ------------------------------------------------------------ multifamily
 dict(slug="calvert-xiv", name="The Calvert XIV", addr="10957 Calvert St", sub="North Hollywood",
   cat="mf", hero="calvert-home.jpg", badge="Refinanced &amp; Held &middot; 14 Units", years="2023 &ndash; present",
   strategy="Ground-up multifamily", status="Refinanced &amp; held",
   cost="$6.30M", exit="$8.25M", profit="$1.95M", poc="31.0%",
   hold_eq=dict(inv="$1.15M", now="$3.30M", mom="2.9x", dscr="1.69"),
   stats=[("14","Units delivered"),("2.9x","Equity multiple to date &mdash; unrealized"),
          ("1.69","Debt service coverage ratio"),("100%","Occupancy")],
   lede="The largest ground-up project in the portfolio &mdash; built, stabilized, refinanced, and held.",
   bg=["A ground-up 14-unit apartment building in North Hollywood, and the largest development by "
       "unit count in the schedule. It received its certificate of occupancy in October 2025 at a "
       "total project cost of $5.73M in construction and acquisition.",
       "Rather than sell into the stabilized-asset market, the building was refinanced in June 2026 "
       "into a Kinecta Federal term loan at 5.93% interest-only and retained. The asset is 100% "
       "occupied at roughly $48,100 per month of scheduled rent, with a 1.69x debt service coverage "
       "ratio &mdash; the strongest coverage of the three retained buildings.",
       "Sponsor equity of approximately $1.15M carries a mark of roughly $3.30M today &mdash; about "
       "2.9x. That multiple is unrealized: it reflects appraised value less first trust deed debt, "
       "and it is not proceeds until the building is sold or further refinanced."],
   cycle=[("Acquire","2023","North Hollywood site acquired for ground-up multifamily development."),
          ("Permit","2023","14-unit program permitted."),
          ("Build","2023&ndash;2025","Construction completed; certificate of occupancy October 2025."),
          ("Stabilize","2025&ndash;2026","Leased to 100% occupancy at ~$48.1K/mo scheduled rent."),
          ("Refinance &amp; hold","June 2026","Kinecta Federal term loan at 5.93% IO; asset retained at 1.69x DSCR.")],
   lesson="Build-to-hold converts a development margin into a durable equity position &mdash; but the multiple stays unrealized until the asset trades."),

 dict(slug="case-v", name="The Case V", addr="5651 Case Ave", sub="North Hollywood",
   cat="mf", hero="case.webp", badge="Refinanced &amp; Held &middot; 5 Units", years="2023 &ndash; present",
   strategy="Ground-up multifamily", status="Refinanced &amp; held",
   cost="$2.80M", exit="$4.00M", profit="$1.20M", poc="42.9%",
   hold_eq=dict(inv="$0.50M", now="$1.21M", mom="2.4x", dscr="1.01"),
   stats=[("5","Units delivered"),("2.4x","Equity multiple to date &mdash; unrealized"),
          ("42.9%","Gross profit on cost"),("Under budget","Delivered below construction budget")],
   lede="Delivered under budget &mdash; the rarest sentence in development.",
   bg=["A ground-up five-unit building in North Hollywood, delivered for less than its construction "
       "budget. Across 21 projects and two decades, cost overruns are the norm and underruns are "
       "the exception; this project is the exception.",
       "The building was refinanced through Archwest and retained as a stabilized rental rather "
       "than sold. Total project cost was $2.80M against a current value of roughly $4.00M &mdash; "
       "$1.20M of value created at a 42.9% gross profit on cost.",
       "Sponsor equity of roughly $0.50M carries a mark of approximately $1.21M today, about 2.4x, "
       "unrealized until sale. Debt service coverage sits at 1.01x &mdash; the tightest of the "
       "three retained buildings, and the reason this asset is watched most closely on rate and "
       "vacancy movement."],
   cycle=[("Acquire","2023","North Hollywood site acquired for a five-unit program."),
          ("Permit","2023","Ground-up multifamily entitlement and permitting completed."),
          ("Build","2023&ndash;2025","Construction delivered under the approved budget."),
          ("Stabilize","2025","Units leased and building stabilized."),
          ("Refinance &amp; hold","2025&ndash;2026","Archwest refinancing; asset retained at 1.01x DSCR.")],
   lesson="Coverage ratios are a risk disclosure, not a footnote. At 1.01x DSCR this asset has minimal cushion, and we say so."),

 dict(slug="june-iv", name="The June IV", addr="1323 N June St", sub="Hollywood",
   cat="mf", hero="june.webp", badge="Refinanced &amp; Held &middot; 4 Units", years="2023 &ndash; present",
   strategy="Ground-up multifamily", status="Refinanced &amp; held",
   cost="$2.38M", exit="$3.60M", profit="$1.23M", poc="51.7%",
   hold_eq=dict(inv="$0.39M", now="$1.44M", mom="3.7x", dscr="1.19"),
   stats=[("3.7x","Equity multiple to date &mdash; highest of the retained assets"),("4","Units delivered"),
          ("51.7%","Gross profit on cost"),("1.19","Debt service coverage ratio")],
   lede="The highest equity mark of the three retained buildings, on the smallest check.",
   bg=["A ground-up four-unit building on North June Street, Hollywood-adjacent &mdash; a submarket "
       "where land basis is high but rental demand is deep and consistent.",
       "Total project cost was $2.38M against a current value of approximately $3.60M, producing "
       "$1.23M of created value at a 51.7% gross profit on cost. The building was refinanced "
       "through Acra and retained rather than sold.",
       "The equity story is the notable one: roughly $0.39M of sponsor equity &mdash; the smallest "
       "position of the three retained assets &mdash; carries a mark of about $1.44M today, "
       "approximately 3.7x. That is a function of leverage and basis, and like the other holds, it "
       "is unrealized until the asset trades."],
   cycle=[("Acquire","2023","Hollywood-adjacent site acquired for a four-unit program."),
          ("Permit","2023","Ground-up multifamily permitting completed."),
          ("Build","2023&ndash;2025","Four-unit building constructed and delivered."),
          ("Stabilize","2025","Units leased into deep Hollywood rental demand."),
          ("Refinance &amp; hold","2025&ndash;2026","Acra refinancing; asset retained at 1.19x DSCR.")],
   lesson="Equity multiples on levered holds are sensitive to basis. A small equity check against a strong valuation produces a large multiple &mdash; and a large sensitivity to value movement."),

 dict(slug="hortense-vi", name="The Hortense VI", addr="10742 Hortense St", sub="North Hollywood",
   cat="mf", hero="hortense.webp", badge="Sold &middot; $4.20M", years="2024 &ndash; 2025",
   strategy="Ground-up multifamily", status="Sold",
   cost="$3.00M", exit="$4.20M", profit="$1.20M", poc="40.0%",
   eq=dict(inv="$544,340", ret="$1,006,430", prof="$462,090", hold="21", mom="1.85x", irr="~42%"),
   stats=[("$4.20M","Sale price"),("1.85x","Equity multiple"),
          ("~42%","Deal-level IRR"),("21 mo","Hold period")],
   lede="The multifamily build that proved the sale exit &mdash; then rolled forward tax-deferred.",
   bg=["A ground-up six-unit multifamily building in North Hollywood, and the counterpoint to the "
       "three retained assets: this one was underwritten with a sale exit and executed on it.",
       "The building was completed and sold in October 2025 for $4.20M against $3.00M of total "
       "project cost. Sponsor equity of $544,340 returned $1,006,430 &mdash; a 1.85x multiple and "
       "roughly 42% XIRR over a 21-month equity hold, computed on dated cash flows.",
       "The disposition proceeds were exchanged under Section&nbsp;1031 into 1949&nbsp;17th&nbsp;St "
       "in Santa Monica, deferring the gain and rolling the capital forward into the next project "
       "rather than paying it out to tax. That exchange was a sponsor-owned transaction and should "
       "not be assumed to apply to any Assemble Capital investment."],
   cycle=[("Acquire","2024","North Hollywood site acquired for a six-unit ground-up program."),
          ("Permit","2024","Multifamily permitting completed."),
          ("Build","2024&ndash;2025","Six units constructed and delivered."),
          ("Market","2025","Marketed as a stabilized multifamily asset."),
          ("Exit","Oct 2025","Sold at $4.20M; 1.85x / ~42% XIRR over a 21-month equity hold."),
          ("Exchange","2025","Proceeds exchanged under Section 1031 into 1949 17th St, Santa Monica.")],
   lesson="Underwriting multiple exits means the sale option is real. This asset was built to be sellable, and it sold."),

 # ------------------------------------------------------------ TIC
 dict(slug="david-iii", name="The David III", addr="5832 David Ave", sub="Culver City adjacent",
   cat="tic", hero="david.webp", badge="Sold as TIC &middot; $2.91M", years="2023 &ndash; 2026",
   strategy="Ground-up triplex, sold as tenancy-in-common units", status="Sold &mdash; TIC sellout",
   cost="$2.43M", exit="$2.91M", profit="$0.49M", poc="20.2%",
   eq=dict(inv="$448,707", ret="$630,439", prof="$181,732", hold="26", mom="1.41x", irr="~17%"),
   stats=[("3","Fee-simple TIC units sold"),("$2.91M","Combined sellout"),
          ("1.41x","Equity multiple"),("26 mo","Hold period")],
   lede="The proof-of-concept for the tenancy-in-common exit &mdash; now the model at 1925 19th St.",
   bg=["Tenancy-in-common is a structure that lets a small multifamily building be sold as "
       "individual homes to individual buyers, rather than as a single income asset to an investor. "
       "The unit buyer pool pays a premium to the bulk value, because they are pricing a place to "
       "live, not a cap rate.",
       "5832 David Ave was built ground-up as a triplex and sold as three separate fee-simple TIC "
       "units across closings from November 2025 through February 2026, totaling $2.91M against "
       "$2.43M of total project cost. Sponsor equity of $448,707 returned $630,439 &mdash; a 1.41x "
       "multiple and roughly 17% XIRR over a 26-month hold.",
       "The returns here are the most modest of the realized exits, and the reason is instructive: "
       "a TIC sellout takes time. Three units close on three separate timelines, each dependent on "
       "an individual buyer securing individual financing. What the project bought was not an "
       "outsized return &mdash; it was a documented, executed template for the TIC pathway, which "
       "is now being applied at 1925&nbsp;19th&nbsp;St in Santa Monica (AC&nbsp;IV)."],
   cycle=[("Acquire","2023","Culver City&ndash;adjacent site acquired for a ground-up triplex."),
          ("Permit","2023","Triplex permitted with a TIC exit structure underwritten from the start."),
          ("Build","2023&ndash;2025","Three units constructed to for-sale finish standards, not rental spec."),
          ("Structure","2025","TIC legal structuring, partial-release terms, and buyer-financing availability arranged."),
          ("Sell out","Nov 2025 &ndash; Feb 2026","Three fee-simple units closed individually, totaling $2.91M."),
          ("Result","2026","Equity returned 1.41x / ~17% XIRR over 26 months; template proven for AC IV.")],
   lesson="A TIC sellout trades speed for price. The premium over bulk value is real, but so is the absorption timeline &mdash; and the bulk-sale fallback has to be underwritten before you start."),
]

CATS = {"sf": "Single Family", "mf": "Multifamily", "tic": "Tenancy-In-Common"}

# ---------------------------------------------------------------- template
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
 '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&'
 'family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,500&family=Special+Elite&'
 'display=swap" rel="stylesheet">')
FAVICON = '<link rel="icon" href="../assets/img/logo/favicon-v2.png">'
MONO = '<img class="emblem" src="../assets/img/logo/emblem-white-v2.png" alt="" aria-hidden="true">'

def header(base=".."):
    return f'''<header class="site-head">
  <div class="bar">
    <a class="lockup" href="/" aria-label="Assemble Capital home">
      {MONO}
      <span class="word">Assemble<br>Capital</span>
    </a>
    <button class="menu-btn" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="site-nav" id="site-nav" aria-label="Primary">
      <a href="{base}/about.html">About</a>
      <div class="nav-dd">
        <a href="{base}/strategies.html" class="nav-dd-toggle">Strategies</a>
        <div class="nav-dd-menu">
          <a href="{base}/strategies/luxury-redevelopment.html">Luxury Residential Development</a>
          <a href="{base}/strategies/boutique-multifamily.html">Opportunistic &amp; Value Add Multifamily Development</a>
          <a href="{base}/strategies/infill-subdivisions.html">SB 684/1123 Fee Simple Subdivisions</a>
          <a href="{base}/strategies/tic-housing.html">Tenancy-In-Common Housing</a>
        </div>
      </div>
      <a href="{base}/portfolio.html">Current Projects</a>
      <a href="{base}/track-record.html" class="active">Track Record</a>
      <a href="{base}/contact.html">Contact</a>
      <a class="portal" href="https://assemblecapital.cashflowportal.com" target="_blank" rel="noopener">Investor Portal&nbsp;&#8599;</a>
    </nav>
  </div>
</header>'''

LEGAL = ("Not an offer or solicitation. Any offering is made only through definitive offering documents "
 "of the applicable issuer to verified accredited and/or sophisticated investors in compliance with "
 "applicable securities laws. Past performance is not indicative of future results. Historical returns "
 "shown on this site were generated on projects completed by the principals through predecessor and "
 "affiliated entities — most were not Assemble Capital offerings and did not involve Assemble Capital "
 "investors — and are sponsor-level, unaudited, and derived from internal records. Projections are "
 "unrealized and subject to change. Investments in private real estate offerings are speculative, "
 "illiquid, and involve a high degree of risk, including possible loss of the entire investment. "
 "Assemble Capital does not provide investment, legal, or tax advice.")

# footer comes from the single source of truth so it stays in sync sitewide
import importlib.util as _ilu, os as _os
_spec = _ilu.spec_from_file_location("_footer",
    _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "tools-rebuild-footer.py"))
_fm = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_fm)

def footer(base=".."):
    return _fm.build("../")

def gallery_html(slug, name):
    d = os.path.join(IMGDIR, slug)
    if not os.path.isdir(d):
        return ""
    shots = sorted(f for f in os.listdir(d) if f.endswith(".jpg"))
    if not shots:
        return ""
    btns = "\n".join(
        f'        <button type="button" data-full="../assets/img/properties/{slug}/{s}" '
        f'aria-label="View photo {i+1} of {len(shots)}">'
        f'<img src="../assets/img/properties/{slug}/thumbs/{s}" alt="{name} &mdash; photo {i+1}" loading="lazy"></button>'
        for i, s in enumerate(shots))
    return f'''
<!-- GALLERY -->
<section class="on-warm">
  <div class="wrap">
    <div class="reveal" style="display:flex;flex-wrap:wrap;align-items:end;justify-content:space-between;gap:1.5rem;margin-bottom:2.2rem">
      <div>
        <p class="eyebrow">Gallery</p>
        <h2 class="h-lg">The property.</h2>
      </div>
      <span class="stamp">{len(shots)} photographs</span>
    </div>
    <div class="gallery reveal">
{btns}
    </div>
  </div>
</section>

<div class="lightbox" role="dialog" aria-modal="true" aria-label="Property photo viewer">
  <button class="lb-close" type="button" aria-label="Close viewer">&#10005;</button>
  <button class="lb-prev" type="button" aria-label="Previous photo">&larr;</button>
  <img src="" alt="">
  <button class="lb-next" type="button" aria-label="Next photo">&rarr;</button>
  <span class="lb-count"></span>
</div>
'''

def build(p, prev, nxt):
    slug, name = p["slug"], p["name"]
    stats = "".join(
        f'      <div class="cell"><div class="num">{v}</div><div class="lbl">{l}</div></div>\n'
        for v, l in p["stats"])
    bg = "\n".join(f"      <p>{x}</p>" for x in p["bg"])
    cycle = "\n".join(
        f'      <div class="step"><span class="ph">{ph}</span><h3>{t}</h3><p>{d}</p></div>'
        for t, ph, d in p["cycle"])

    # equity block
    eqrows = ""
    if p.get("eq"):
        e = p["eq"]
        eqrows = f'''
    <div class="reveal" style="margin-top:3rem">
      <p class="eyebrow">Equity Performance &mdash; Realized</p>
      <div class="table-scroll">
        <table class="data">
          <thead><tr><th>Equity invested</th><th class="num">Total returned</th><th class="num">Net profit</th><th class="num">Hold</th><th class="num">Multiple</th><th class="num">IRR</th></tr></thead>
          <tbody><tr>
            <td class="addr">{e["inv"]}</td>
            <td class="num">{e["ret"]}</td>
            <td class="num{' neg' if p.get('loss') else ''}">{e["prof"]}</td>
            <td class="num">{e["hold"]} mo</td>
            <td class="num">{e["mom"]}</td>
            <td class="num{' neg' if p.get('loss') else ''}">{e["irr"]}</td>
          </tr></tbody>
        </table>
      </div>
    </div>'''
    elif p.get("hold_eq"):
        h = p["hold_eq"]
        eqrows = f'''
    <div class="reveal" style="margin-top:3rem">
      <p class="eyebrow">Equity Position &mdash; Unrealized</p>
      <div class="table-scroll">
        <table class="data">
          <thead><tr><th>Equity invested</th><th class="num">Equity value today</th><th class="num">Multiple to date</th><th class="num">DSCR</th><th class="num">Status</th></tr></thead>
          <tbody><tr>
            <td class="addr">{h["inv"]}</td><td class="num">{h["now"]}</td>
            <td class="num">{h["mom"]}</td><td class="num">{h["dscr"]}</td>
            <td class="num">Held &mdash; unrealized</td>
          </tr></tbody>
        </table>
      </div>
      <p class="footnote" style="margin-top:1rem">Equity value = appraised value less first trust deed debt, per SREO dated 7/14/26. Multiples to date are unrealized and are not proceeds. Junior portfolio debt also encumbers this asset.</p>
    </div>'''

    # loss controls block
    controls = ""
    if p.get("controls"):
        items = "\n".join(f"        <li>{c}</li>" for c in p["controls"])
        controls = f'''
<!-- CONTROLS -->
<section class="on-dark">
  <div class="wrap split reveal" style="align-items:start">
    <div>
      <p class="eyebrow">Accountability</p>
      <h2 class="h-lg">What changed afterward.</h2>
      <p class="muted" style="max-width:30rem">A loss is only useful if it changes the underwriting. These controls were implemented across the platform following this project.</p>
    </div>
    <div>
      <ul style="list-style:none;padding:0;margin:0;border-top:1px solid var(--line)">
{items}
      </ul>
    </div>
  </div>
</section>'''.replace("<li>", '<li style="padding:1rem 0;border-bottom:1px solid var(--line);font-size:.94rem">')

    # disclosure
    if p.get("ac"):
        disc = ("This is an active Assemble Capital project held in a project-specific LLC &mdash; a "
                "private offering. Nothing here is an offer to sell or a solicitation to buy any "
                "security. Any offering is made only through definitive offering documents to eligible "
                "investors, and investor-level returns are governed by the applicable operating "
                "agreement. Past performance is not indicative of future results.")
    else:
        disc = ("This project was completed by the principals through Thornton Development Group or an "
                "affiliated predecessor entity. It was not an Assemble Capital offering and did not "
                "involve Assemble Capital investors. Figures are sponsor-level, pre-tax, unaudited, and "
                "derived from internal records, closing statements, and lender documentation. "
                "Past performance is not indicative of future results.")
    if p.get("note"):
        disc = p["note"] + " " + disc

    zbtn = (f'<a class="btn" style="border-color:var(--line-strong)" href="{p["zillow"]}" '
            f'target="_blank" rel="noopener">View the listing &#8599;</a>' if p.get("zillow") else "")

    gal = gallery_html(slug, name)

    # Returns section. Active AC projects are private 506(b) offerings — no public deal
    # financials; show a "shared privately" callout instead of the economics table.
    if p.get("ac"):
        returns_section = f'''
<!-- FINANCIALS — PRIVATE -->
<section>
  <div class="wrap">
    <div class="reveal" style="display:flex;flex-wrap:wrap;align-items:end;justify-content:space-between;gap:1.5rem;margin-bottom:2.2rem">
      <div>
        <p class="eyebrow">The Investment</p>
        <h2 class="h-lg">Financials, privately.</h2>
      </div>
      <span class="stamp">{p["status"]}</span>
    </div>
    <div class="reveal" style="border:1px solid var(--line);border-left:3px solid var(--bronze);padding:1.6rem 1.9rem;max-width:54rem">
      <p style="margin:0 0 .8rem;font-size:.95rem">This is an active Assemble Capital project, held in a project-specific LLC as a private offering. We don't publish projected returns, capitalization, or deal-level economics for active projects.</p>
      <p style="margin:0;font-size:.95rem">Prospective investors who qualify can review the full underwriting, business plan, and offering documents privately, one-on-one. <a href="../contact.html" style="border-bottom:1px solid var(--line-strong);text-decoration:none">Request the details &rarr;</a></p>
    </div>
    <p class="footnote reveal" style="margin-top:1.6rem">{disc}</p>
  </div>
</section>'''
    else:
        returns_section = f'''
<!-- RETURNS -->
<section>
  <div class="wrap">
    <div class="reveal" style="display:flex;flex-wrap:wrap;align-items:end;justify-content:space-between;gap:1.5rem;margin-bottom:2.2rem">
      <div>
        <p class="eyebrow">Return On Investment</p>
        <h2 class="h-lg">The numbers.</h2>
      </div>
      <span class="stamp">{p["status"]}</span>
    </div>
    <div class="table-scroll reveal">
      <table class="data">
        <thead><tr><th>Strategy</th><th class="num">Total project cost</th><th class="num">Disposition / value</th><th class="num">Gross profit</th><th class="num">Profit on cost</th></tr></thead>
        <tbody><tr>
          <td class="addr">{p["strategy"]}</td>
          <td class="num">{p["cost"]}</td>
          <td class="num">{p["exit"]}</td>
          <td class="num">{p["profit"]}</td>
          <td class="num">{p["poc"]}</td>
        </tr></tbody>
      </table>
    </div>{eqrows}
    <p class="footnote reveal" style="margin-top:1.6rem">{disc}</p>
  </div>
</section>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} &mdash; {p["addr"]} | Assemble Capital</title>
<meta name="description" content="{name} at {p['addr']}, {p['sub']} — investment background, gallery, returns, and investment cycle.">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Assemble Capital">
<meta property="og:url" content="https://assemble.capital/properties/{p['slug']}.html">
<meta property="og:title" content="{name} &mdash; {p["addr"]} | Assemble Capital">
<meta property="og:description" content="{name} at {p['addr']}, {p['sub']} — investment background, gallery, returns, and investment cycle.">
<meta property="og:image" content="https://assemble.capital/assets/img/{p['hero']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{name} &mdash; {p["addr"]} | Assemble Capital">
<meta name="twitter:description" content="{name} at {p['addr']}, {p['sub']} — investment background, gallery, returns, and investment cycle.">
<meta name="twitter:image" content="https://assemble.capital/assets/img/{p['hero']}">
{FONTS}
<link rel="stylesheet" href="../css/style.css?v=3">
{FAVICON}
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>

{header()}

<main id="main">

<section class="hero short" style="padding:0">
  <div class="bg" style="background-image:url('../assets/img/{p["hero"]}')"></div>
  <div class="wrap">
    <p class="eyebrow">{CATS[p["cat"]]} &middot; {p["sub"]}</p>
    <h1 class="display">{name}</h1>
    <p class="sub">{p["addr"]} &middot; {p["badge"]} &middot; {p["years"]}</p>
  </div>
</section>

<!-- HEADLINE STATS -->
<section>
  <div class="wrap">
    <div class="ledger reveal">
{stats}    </div>
  </div>
</section>

<!-- BACKGROUND -->
<section class="on-warm">
  <div class="wrap split reveal">
    <div>
      <p class="eyebrow">The Investment</p>
      <p class="lede">{p["lede"]}</p>
    </div>
    <div>
{bg}
    </div>
  </div>
</section>
{gal}{returns_section}

<!-- INVESTMENT CYCLE -->
<section class="on-dark">
  <div class="wrap">
    <div class="split reveal" style="align-items:end;margin-bottom:2.6rem">
      <div>
        <p class="eyebrow">Investment Cycle</p>
        <h2 class="h-lg">How the deal ran.</h2>
      </div>
      <p class="muted" style="max-width:34rem;margin:0">Every project follows the same arc &mdash; acquire, design and permit, build, market, exit. What changes is where the time and the risk concentrate.</p>
    </div>
    <div class="cycle reveal">
{cycle}
    </div>
    <div class="split reveal" style="margin-top:3rem;align-items:start">
      <p class="eyebrow" style="margin:0">The Takeaway</p>
      <p class="lede" style="margin:0">{p["lesson"]}</p>
    </div>
  </div>
</section>
{controls}
<!-- CTA -->
<section class="cta-band on-warm">
  <div class="wrap reveal">
    <p class="eyebrow">Invest With Us</p>
    <h2 class="h-lg">Interested in projects like this one?</h2>
    <p class="muted" style="max-width:40rem;margin:1.4rem auto 0">We syndicate Los Angeles residential projects with accredited investors &mdash; an 8% preferred return paid first, Class&nbsp;A participation in the profits, and our own capital in every deal. Join the network to see the next offering.</p>
    <div class="actions">
      <a class="btn" style="border-color:var(--line-strong)" href="../contact.html">Join the investment network</a>
      <a class="btn" style="border-color:var(--line-strong)" href="../strategies.html">See how the model works</a>
      {zbtn}
    </div>
  </div>
</section>

<!-- PREV / NEXT -->
<nav class="pn-nav" aria-label="Property navigation">
  <a class="prev" href="{prev["slug"]}.html"><span class="k">&larr; Previous</span><span class="n">{prev["name"]}</span></a>
  <a class="next" href="{nxt["slug"]}.html"><span class="k">Next &rarr;</span><span class="n">{nxt["name"]}</span></a>
</nav>

</main>

{footer()}

<script src="../js/main.js"></script>
</body>
</html>
'''

# ---------------------------------------------------------------- write
out = os.path.join(SITE, "properties")
os.makedirs(out, exist_ok=True)
for i, p in enumerate(P):
    prev = P[(i - 1) % len(P)]
    nxt = P[(i + 1) % len(P)]
    with open(os.path.join(out, p["slug"] + ".html"), "w") as f:
        f.write(build(p, prev, nxt))
    print("wrote", p["slug"] + ".html")

# emit slug map for track-record linking
with open("/tmp/slugmap.json", "w") as f:
    json.dump({p["addr"]: p["slug"] for p in P}, f, indent=1)
print("TOTAL", len(P))


# --- keep SEO/506(b) metadata authoritative -------------------------------
# This generator emits a baseline <head>. tools-apply-seo-metadata.py owns the
# canonical/robots/OG/Twitter/JSON-LD block, so re-apply it after every build.
import subprocess as _sp
_sp.run(["python3", os.path.join(SITE, "tools-apply-seo-metadata.py")], check=True)
