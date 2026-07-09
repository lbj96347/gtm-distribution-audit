# GTM Distribution Readiness Audit — Claude Code plugin

Audit a project or idea against the **Distribution Channel Playbook** *before* you
invest effort building distribution channels. The plugin scores go-to-market readiness
across 12 dimensions for digital marketing (SEO, ASO, GEO, content), enforces
evidence-first gates, and renders a **self-contained visual HTML report**.

> **Prime directive:** user pain first, tools second. Real pain evidence and
> user-language mapping *gate* keyword/SERP/landing/GEO work. Strong tool work on top
> of no primary evidence is "not ready to build."

## What you get

- **`/gtm-audit`** slash command — the entry point.
- A **readiness score (0–100)** with an evidence-gate verdict ("ready" / "not ready — fix primary evidence first").
- A visual report: readiness gauge, 12-dimension radar, **20-stage funnel heatmap**, prioritized action table, channel recommendation, and a red-flags card — one offline HTML file, light/dark aware.
- Reuse of the installed `seo-*` capabilities: SEO/ASO/GEO deep-checks are delegated to `seo-technical`, `seo-content`, `seo-geo`, and `seo-schema` rather than reimplemented.

## Usage

```
/gtm-audit                      # guided interview (best for pre-launch ideas)
/gtm-audit ./my-brief.md        # audit a filled-in GTM brief
/gtm-audit https://myapp.com    # audit live SEO/ASO/GEO signals + short interview for the gates
```

Fill `skills/gtm-distribution-audit/templates/gtm-brief.template.md` for brief mode.

## The 12 dimensions

| # | Dimension | Gate? | Delegates to |
|---|---|---|---|
| 1 | Pain evidence (primary) | ✅ | `gtm-pain-evidence` |
| 2 | User language & intent | ✅ | `gtm-pain-evidence` |
| 3 | Keyword opportunity | | inline (opportunity formula) |
| 4 | SERP / competition | | `seo-technical` |
| 5 | Channel selection (1–2 deep) | | `gtm-channel-directory` |
| 6 | Directory strategy | | `gtm-channel-directory` + `seo-schema` |
| 7 | Content assets & format | | `seo-content` |
| 8 | Landing page / on-page SEO | | `seo-technical` |
| 9 | App Store Optimization | | inline ASO rubric |
| 10 | GEO / AI visibility | | `seo-geo` |
| 11 | Conversion / activation / retention | | `gtm-conversion-loop` |
| 12 | Measurement & learning loop | | `gtm-conversion-loop` |

## Layout

```
.claude-plugin/{plugin.json, marketplace.json}
commands/gtm-audit.md
skills/gtm-distribution-audit/
  SKILL.md                    # the orchestration method
  references/*.md             # playbook, rubric, channel matrix, directory, interview, red flags
  templates/                  # brief template, audit-data schema + example
  scripts/                    # render_report.py, validate_audit.py (stdlib only)
agents/gtm-*.md               # 3 GTM-specific auditors
```

## Install (local directory marketplace)

```
/plugin marketplace add /Users/CashMacbook/Documents/project/gtm-audit/gtm-distribution-audit
/plugin install gtm-distribution-audit@gtm-audit-local
```

Then `/gtm-audit` is available. (The `seo-*` skills/agents are expected to be present
for the delegated SEO/ASO/GEO checks; without them, those dimensions degrade gracefully
and the report notes it.)

## Regenerate a report from data

```
python3 skills/gtm-distribution-audit/scripts/validate_audit.py audit-data.json
python3 skills/gtm-distribution-audit/scripts/render_report.py audit-data.json -o gtm-audit-report.html
```

Source framework: *Distribution Channel Playbook: From User Pain to Product Adoption*
and *AI-Agent GTM Platform: Technical Approaches by Playbook Stage*.

## License

Released under the [MIT License](LICENSE). © 2026 libingjun1024.

## Contact

Questions, ideas, or feedback? Reach out on X: [@lbjhkg](https://x.com/lbjhkg).
