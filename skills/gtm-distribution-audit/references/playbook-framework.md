# Distribution Playbook — Framework Reference

Distilled from *Distribution Channel Playbook: From User Pain to Product Adoption*
and *AI-Agent GTM Platform: Technical Approaches*. This is the canonical map the
audit scores against.

## Core principle (the whole reason this audit exists)

> **User pain first, tools second.** Keyword planners, Search Console, and App Store
> data are *secondary evidence*. Primary evidence comes from conversations, reviews,
> comments, and observed workflows. An audit that finds strong keyword work but no
> primary pain evidence is a **red flag**, not a green light.

Distribution is a **feedback loop**, not a straight line:
`Users/Prospects → Search & Discovery → Developer Content → Product Adoption → (evidence) → repeat`.

## The 11-Step Loop

| Step | Action | Output |
|---|---|---|
| 1 | Observe real user pain (interviews, reviews, Reddit, comments, support) | Problem hypothesis |
| 2 | Convert pain into **user language**, not developer language | Problem statement in user words |
| 3 | Map user intent: informational / comparison / solution-seeking / buying | Intent map |
| 4 | Use keyword tools **only after** understanding user language | Keyword list |
| 5 | Check real search results & App Store results (SERP) | SERP analysis |
| 6 | Choose keywords by **opportunity**, not popularity | Keyword map |
| 7 | Pick **1–2 channels** where users already show intent | Channel map |
| 8 | Create content that answers the exact question / shows the exact pain | Content assets |
| 9 | Build landing / App Store page matching the same promise | Conversion path |
| 10 | Measure install, activation, retention, feedback | Analytics baseline |
| 11 | Repeat based on evidence, not assumptions | Learning loop |

## The 20-Stage Deep Dive (used for the funnel heatmap)

Each stage has a maturity level the audit colors (green = solid evidence / done,
amber = partial / unvalidated, red = missing / blocking).

| # | Stage | Goal | Hardest part |
|---|---|---|---|
| 1 | Hidden problem | Discover a real problem | Users describe symptoms, not the problem |
| 2 | Problem awareness | Convert vague pain into a clear problem | Developer defines problem from own view |
| 3 | Search intent appears | Understand how users express demand | Users use different words than product language |
| 4 | Keyword discovery | Find keywords worth targeting | Popular = competitive; long-tail = low volume |
| 5 | Real SERP inspection | Find content gaps & positioning | Keyword tools alone are not enough |
| 6 | Channel mapping | Choose right channels | Different channels = different intent |
| 7 | Content format research | Know what content users consume | Good explanation fails if format is boring |
| 8 | Emotional hook | Capture attention | Developers explain features too early |
| 9 | Landing page creation | Convert attention into interest | Page must match search intent |
| 10 | Social content creation | Build awareness & trust | Consistency is hard; one post rarely works |
| 11 | Community placement | Build credibility | Communities dislike obvious promotion |
| 12 | SEO accumulation | Create long-term discovery | SEO takes time & requires quality |
| 13 | Short-term acquisition | Get fast traffic & test messaging | Short-term traffic disappears quickly |
| 14 | Product positioning | Make product memorable | Generic products are not remembered |
| 15 | App Store optimization | Improve discovery & conversion | ASO changes affect ranking unpredictably |
| 16 | Trust building | Reduce hesitation | New products lack reviews & authority |
| 17 | Conversion | Turn traffic into users | Traffic useless with weak conversion |
| 18 | Activation | Help user experience value | Users drop off without value in first minute |
| 19 | Retention | Convert install into habit | Product experience keeps users, not distribution |
| 20 | Feedback loop | Improve product & distribution | Developers stop after publishing — iteration is hard |

**Surface-dependent stages.** A stage that depends on a surface the product doesn't ship
is marked `maturity: "na"` (with a `na_reason`) and excluded from scoring — not counted
as a failure. In particular **Stage 15 (App Store optimization) is N/A unless
`project.surfaces` includes an app-store surface (`ios`/`android`/`mac_app_store`)**; the
other 19 stages apply regardless.

## Opportunity formula (Step 6)

`opportunity = search_volume + user_intent + competition + product_fit + content_format`

The correct target is the keyword where **user has pain + product fits + competition
is beatable + conversion is likely** — not the most popular keyword. Popularity is
competitive and expensive.

Apple Search Ads caveat: popularity is a **1–5 relative score**, not exact volume.
Validate with impressions, tap-through, conversion, and organic ranking changes.

## Extended funnel (do not stop at install)

`Install → first successful action → repeated use → review → referral → content proof`

If users install but do not activate, the distribution signal is misleading — you
may credit a keyword/channel that actually failed after the click.

## Evidence-first gates (enforced by the audit)

- Keyword work (dim 3) is **blocked / discounted** until user-language map (dim 2) exists.
- Stage N maturity cannot read "green" if Stage N-1's evidence is missing.
- Low-confidence dimensions are flagged for human review, never treated as done.
