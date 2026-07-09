---
name: gtm-distribution-audit
description: >
  Audit a project or idea against the Distribution Channel Playbook BEFORE investing
  effort in building distribution channels. Scores go-to-market readiness across 12
  dimensions for digital marketing (SEO, ASO, GEO, content), enforces evidence-first
  gates (real user pain and user-language before keyword/SERP tools), and renders a
  self-contained visual HTML report (readiness gauge, radar, 20-stage funnel heatmap,
  prioritized gaps, channel recommendation). Use when the user wants a "GTM audit",
  "distribution readiness" check, "go-to-market audit", "distribution channel audit",
  asks "should I build this channel / is my idea ready to market", or runs /gtm-audit.
  Triggers on: "GTM audit", "distribution readiness", "go-to-market audit",
  "distribution channel audit", "audit my marketing", "is my idea ready to launch".
---

# GTM Distribution Readiness Audit

You audit a project/idea against the Distribution Channel Playbook and produce a
**readiness scorecard + gap analysis + prioritized next actions**, visualized as a
self-contained HTML report. The point is to tell the user **whether they should
invest more in building distribution channels yet, and what the weakest link is** —
not to build the channels.

## Prime directive: evidence before tools

> **User pain first, tools second.** Primary evidence = conversations, reviews,
> comments, observed workflows. Secondary evidence = keyword planners, SERP data,
> App Store stats. A project with polished keyword work but no primary pain evidence
> is **NOT ready** — the report must say so.

Dimensions 1 (pain evidence) and 2 (user language) are **gates**. If either scores
below 40, keyword/SERP/landing/GEO dimensions are discounted and the report shows the
**"Not ready to build — fix primary evidence first"** banner. Never let strong
tool-driven scores paper over missing primary evidence.

## Read these first

- `references/playbook-framework.md` — the 11-step loop, 20-stage map, opportunity formula, gates.
- `references/scoring-rubric.md` — the 12 dimensions, weights, gates, 0–100 anchors, composite math, gap prioritization.
- `references/channel-matrix.md` — channel intent/format/risk table for dim 5.
- `references/directory-strategy.md` — owned-vs-third-party two-track for dim 6.
- `references/interview-questions.md` — the question bank for interview mode.
- `references/wrong-assumptions.md` — the 10 red-flags checklist.

## Workflow

### 1. Pick the input mode

The `/gtm-audit` argument (or the user's request) selects the mode:

- **Brief file** (a path ending in `.md`): read it, treat each section as the
  corresponding dimension's evidence. Blank sections are findings, not errors.
- **URL** (starts with `http` or is an App Store link): audit live signals — see
  "URL mode" below.
- **Interview** (no argument, or "interview"): walk `references/interview-questions.md`,
  1–3 questions at a time. Capture verbatim answers as evidence. Probe for primary
  evidence (real quotes, counts, sources), not opinions. Stop early on empty gates.

If mode is ambiguous, ask the user once.

### 2. Determine product surfaces, then gather evidence per dimension

First establish **`project.surfaces`** — the surfaces the product actually ships (`web`,
`ios`, `android`, `mac_app_store`, `desktop`, `browser_extension`, `api_cli`,
`marketplace`, …). Ask if unclear; infer from a URL/brief where possible. This decides
which dimensions and funnel stages apply. Anything that depends on a surface the product
doesn't ship is marked **N/A** (dimension `band: "na"`, stage `maturity: "na"`) with a
short `na_reason`, and **excluded from the composite** (see the surface-applicability
table in the rubric). Most notably, **ASO (dim 9) and Stage 15 are N/A unless surfaces
include an app-store surface (`ios`/`android`/`mac_app_store`)** — never score a
website-only product on App Store / Google Play.

Score every applicable dimension from `references/scoring-rubric.md` (mark the rest
`na`). **Delegate, don't reimplement** — invoke the installed capabilities and fold
their findings in:

| Dimensions | Delegate to |
|---|---|
| 1, 2 (pain, user language) | Task → `gtm-pain-evidence` agent |
| 5, 6 (channel, directory) | Task → `gtm-channel-directory` agent |
| 11, 12 (conversion/retention, learning loop) | Task → `gtm-conversion-loop` agent |
| 4, 8 (SERP, landing/on-page SEO) | `seo-technical` skill/agent |
| 7 (content depth, E-E-A-T) | `seo-content` skill/agent |
| 10 (GEO / AI visibility) | `seo-geo` skill/agent |
| 6 (directory schema: ItemList/SoftwareApplication) | `seo-schema` skill/agent |
| 3, 9 (keyword opportunity, ASO) | score inline via the rubric |

In **interview** or **brief** mode without a live URL, the SEO/GEO delegates have no
page to crawl — score dims 4/8/10 from what the user reports and **note the
degradation** in each dimension's evidence (e.g. "not verified against a live page").

Run independent delegations in parallel where possible. For each dimension produce
`{ score, band, evidence[], gaps[], next_actions[] }` per the rubric anchors.

### 3. Compute gates, composite, stages, red flags

- Apply the gate rule: if a gate dimension < 40, set `gate_status: "blocked"`, write a
  `gate_reason`, and multiply each tool-driven dimension's contribution by 0.5 in the composite.
- Composite `readiness_score` = weighted mean over **applicable** (non-`na`) dimensions,
  rounded 0–100 (see rubric — N/A dims drop out of both the score and weight sums).
- Map every dimension's state onto the **20 stages** (`references/playbook-framework.md`)
  as `green|amber|red` maturity with a short note — or `na` (with a `na_reason`) for a
  surface-inapplicable stage such as Stage 15 on a web-only product. A stage can't be
  green if its upstream evidence is missing.
- Run the **red-flags checklist** (`references/wrong-assumptions.md`); record each
  matched assumption with the dimension it damages.
- Build `channel_recommendation` (1–2 channels + directory call) from dims 5–6, honoring
  `project.surfaces` — never recommend App Store Search / ASO for a product with no
  `ios`/`android` surface (its conversion target is the website, not an App Store page).
- Build `top_actions`: collect all gaps, compute `priority = impact / effort` (gate gaps
  get +1 impact, capped at 5), keep the top ~5.

### 4. Write and validate the audit data

**All output goes into a single dedicated folder — never scatter files in the project
root.** Create an output folder `gtm-audit-report/` in the working directory (make a
fresh subfolder like `gtm-audit-report/<slug>/` if the user names a project, so repeat
runs don't clobber each other), and write every artifact there.

Write the result as JSON conforming to `templates/audit-data.schema.json` (use
`templates/audit-data.example.json` as the shape reference). Save it as
`gtm-audit-report/audit-data.json`, then validate:

```
mkdir -p gtm-audit-report
python3 skills/gtm-distribution-audit/scripts/validate_audit.py gtm-audit-report/audit-data.json
```

Fix any reported problems before rendering. All 12 dimensions and all 20 stages must be
present in the data — but surface-inapplicable ones carry `band: "na"` / `maturity: "na"`
(with a `na_reason`) rather than a real score, and are excluded from the composite.

### 5. Render the report

```
python3 skills/gtm-distribution-audit/scripts/render_report.py gtm-audit-report/audit-data.json -o gtm-audit-report/gtm-audit-report.html
```

The output is a single offline HTML file (inline SVG + CSS, no external assets),
theme-aware, with the readiness gauge, evidence-gate banner, 12-dimension radar,
20-stage funnel heatmap, prioritized action table, channel card, and red-flags card.
Report the `gtm-audit-report/` folder path and offer to open the HTML. To preview it
yourself in the browser tools, serve the directory with `python3 -m http.server`
(file:// URLs are blocked) — do not require this for the user.

Inside a packaged plugin the scripts live at
`${CLAUDE_PLUGIN_ROOT}/skills/gtm-distribution-audit/scripts/`; when invoked as a
loose skill, use the relative `scripts/…` paths shown above.

### 6. Summarize

In chat, give the headline: the score, whether they're ready to build, the single
weakest link, and the top 2–3 actions. Keep the detail in the report.

## URL mode specifics

For a live landing page or App Store listing: delegate crawl/analysis to
`seo-technical` (crawlability, on-page SEO, CWV → dims 4, 8), `seo-geo` (AI-crawler
access, llms.txt, citability → dim 10), and `seo-schema` (structured data → dim 6).
Browser MCP tools or the `seo` skill's bundled fetch scripts may be used for capture.
Crawled signals only cover the tool-driven dimensions — you still need interview or
brief input for the **gate** dimensions (pain, user language) and for conversion/
retention/measurement, since those aren't visible from a page. If you only have a URL,
tell the user the gate dimensions are unverified and offer a short interview to fill them.

## Principles

- Be honest, not encouraging. A low score with clear next actions is the valuable output.
- Cite primary evidence in `evidence[]` (source_type + excerpt). No evidence → say so.
- Never invent evidence to inflate a gate. Missing evidence is the finding.
- Recommend **1–2 channels**, never "post everywhere."
