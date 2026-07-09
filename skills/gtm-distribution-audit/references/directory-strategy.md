# Niche Directory Strategy

In niche markets, curated directory websites (owned or third-party) are **essential
infrastructure** for comparison-intent traffic — not just a backlink tactic. Users
searching "best X for Y", "alternatives to Z", "tools for [workflow]" land on curated
lists before individual product pages, and AI search tools cite brands in trusted lists.

## Two-track model

| Track | When to use | Primary value | Main risk |
|---|---|---|---|
| **A: Build an owned niche directory** | SERP shows weak/stale lists; you have 3+ products in a niche; long-tail "best tools" queries have opportunity | Long-term discovery + category authority + portfolio cross-sell | Build & maintenance cost |
| **B: Strategic third-party listings** | Established directories already rank & users trust them | Credibility + referral traffic | Low-quality directory farms waste time |

## Directory opportunity score

`directory_opportunity = comparison_intent × serp_gap × portfolio_fit`

- **comparison_intent** — share of target queries that are comparison/alternatives.
- **serp_gap** — how weak/stale the currently-ranking directory & listicle pages are.
- **portfolio_fit** — do you have ≥3 products in the niche to justify an owned directory?

High score + portfolio breadth → **Track A (build owned)**. High score but single
product → **Track B (strategic listings)**. Low comparison intent → directories are
not a priority; score dim 6 neutral.

## Owned directory quality checklist (for scoring)

- Categories structured around **user problems** ("hide menu bar icons") not feature taxonomy.
- Listing template: problem fit, use case, pricing, screenshots, honest pros/cons.
- Editorial standards: quality over quantity; spam rejected.
- SEO: category pages with schema.org **ItemList + SoftwareApplication** markup, internal links to product landing pages (delegate schema check to `seo-schema`).
- UTM: `?utm_source=directory&utm_medium={owned|third_party}&utm_campaign={category}`.

## Directory red flags

- Mass-submitting to low-quality directory farms.
- Building a directory before validating search demand in SERP.
- Feature-first listings instead of problem-first copy.
- Treating all directories as equal — curated niche lists ≠ spam farms.
