#!/usr/bin/env python3
"""Keyword discovery without a paid SEO API.

Pulls real query suggestions from Google and Bing autocomplete. These are
queries people actually type, which for content planning is often more useful
than a modelled volume estimate. It does NOT return search volume or keyword
difficulty — assess competition by looking at who currently ranks.

    python3 tools-keyword-research.py "sb 684" "sb 1123" --out docs/kw.md

Options:
    --deep     also expand seed + each letter a-z (slower, much wider net)
    --out FILE write a markdown report
"""
import sys, json, time, urllib.parse, urllib.request, re
from collections import OrderedDict

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
GOOGLE = "https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=us&q={}"
BING = "https://api.bing.com/osjson.aspx?query={}"

QUESTIONS = ["what is", "what are", "how does", "how to", "how long", "how many",
             "why", "when", "can you", "does", "is", "who"]
MODIFIERS = ["vs", "requirements", "eligibility", "rules", "explained", "california",
             "los angeles", "cost", "process", "checklist", "summary", "2026"]


def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8", "replace"))
    except Exception:
        return None


def suggest(term):
    """Suggestions for one term from both engines."""
    out = []
    q = urllib.parse.quote(term)
    g = fetch(GOOGLE.format(q))
    if g and len(g) > 1 and isinstance(g[1], list):
        out += [s for s in g[1] if isinstance(s, str)]
    b = fetch(BING.format(urllib.parse.quote_plus(term)))
    if b and len(b) > 1 and isinstance(b[1], list):
        out += [s for s in b[1] if isinstance(s, str)]
    time.sleep(0.35)          # be polite to both endpoints
    return out


def expand(seed, deep=False):
    seen = OrderedDict()
    def add(items):
        for s in items:
            s = re.sub(r"\s+", " ", s.strip().lower())
            if s and s not in seen:
                seen[s] = True

    add(suggest(seed))
    for q in QUESTIONS:
        add(suggest(f"{q} {seed}"))
    for m in MODIFIERS:
        add(suggest(f"{seed} {m}"))
    if deep:
        for ch in "abcdefghijklmnopqrstuvwxyz":
            add(suggest(f"{seed} {ch}"))
    return [k for k in seen if relevant(k, seed)]



STOP = {"is","are","the","a","an","of","in","to","for","and","how","what","why",
        "when","who","can","does","vs","california","los","angeles"}


def relevant(kw, seed):
    """Drop suggestions that share only a bare number with the seed.

    Short numeric seeds ("sb 684") pull unrelated arithmetic and part-number
    queries out of autocomplete. Require the seed's non-numeric signal to be
    present, not just the digits.
    """
    kw_l, seed_l = kw.lower(), seed.lower()
    if seed_l in kw_l:
        return True
    nums = re.findall(r"\d+", seed_l)
    if nums:
        # A numbered seed needs BOTH halves. The number alone lets arithmetic and
        # part numbers through ("684 divided by 2", "gb/t 684"); the prefix alone
        # lets neighbouring bills through ("sb 694", "sb 54").
        if not all(re.search(rf"\b{n}\b", kw_l) for n in nums):
            return False
        alpha = [w for w in re.findall(r"[a-z]+", seed_l) if w]
        expanded = {"sb": ["sb", "senate bill"], "ab": ["ab", "assembly bill"]}
        for w in alpha:
            forms = expanded.get(w, [w])
            if not any(f in kw_l for f in forms):
                return False
        return True
    words = [w for w in re.findall(r"[a-z]+", seed_l) if w not in STOP and len(w) > 2]
    if not words:
        words = [w for w in re.findall(r"[a-z]+", seed_l) if w]
    return all(w in kw_l for w in words) if words else True


def classify(k):
    if re.match(r"^(what|how|why|when|who|can|does|is|are)\b", k): return "question"
    if re.search(r"\bvs\b|versus|difference|compare", k):          return "comparison"
    if re.search(r"\b(cost|price|fee|hire|near me|company|firm|builder|developer|attorney|consultant)\b", k):
        return "commercial"
    return "informational"


def main():
    argv = sys.argv[1:]
    deep = "--deep" in argv
    out = None
    if "--out" in argv:
        i = argv.index("--out")
        out = argv[i + 1] if i + 1 < len(argv) else None
        del argv[i:i + 2]                       # drop the flag AND its value
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__); sys.exit(1)

    report, total = [], 0
    for seed in args:
        print(f"expanding: {seed} ...", file=sys.stderr)
        kws = expand(seed, deep)
        total += len(kws)
        groups = {}
        for k in kws:
            groups.setdefault(classify(k), []).append(k)
        report.append((seed, groups, len(kws)))
        print(f"  {len(kws)} suggestions", file=sys.stderr)

    lines = ["# Keyword discovery — Google + Bing autocomplete", "",
             "Real query suggestions, not modelled volume. No search volume or difficulty:",
             "assess competition by checking who currently ranks for the term.", ""]
    for seed, groups, n in report:
        lines += [f"## Seed: `{seed}` — {n} suggestions", ""]
        for g in ("question", "comparison", "commercial", "informational"):
            if g in groups:
                lines += [f"### {g.title()} ({len(groups[g])})", ""]
                lines += [f"- {k}" for k in sorted(groups[g])]
                lines.append("")
    text = "\n".join(lines)
    if out:
        open(out, "w").write(text + "\n")
        print(f"\nwrote {out} — {total} suggestions across {len(report)} seed(s)", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
