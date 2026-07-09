---
description: "Audit a project/idea against the Distribution Channel Playbook and render a visual GTM readiness report"
argument-hint: "[<url> | <brief.md> | interview]  (empty = guided interview)"
---

# GTM Distribution Readiness Audit

Load and follow the skill at
`${CLAUDE_PLUGIN_ROOT}/skills/gtm-distribution-audit/SKILL.md`, then run the audit
end to end.

**Input mode** is chosen from the argument below:

- `$ARGUMENTS` looks like a URL (starts with `http`, or is an App Store link) → **URL mode**: audit live SEO/ASO/GEO signals, then ask a short interview to fill the gate dimensions (pain, user language) and the conversion/retention/measurement dimensions that a page can't reveal.
- `$ARGUMENTS` is a path ending in `.md` → **Brief mode**: read that GTM brief and audit each section.
- `$ARGUMENTS` is empty or the word `interview` → **Interview mode**: walk `references/interview-questions.md`, 1–3 questions at a time, probing for primary evidence.

Argument received: `$ARGUMENTS`

Follow the SKILL.md workflow: gather evidence (delegating SEO/ASO/GEO checks to the
installed `seo-technical`, `seo-content`, `seo-geo`, `seo-schema` capabilities and the
bundled `gtm-*` agents), enforce the evidence-first gates, write a validated
`gtm-audit-report/audit-data.json`, render `gtm-audit-report/gtm-audit-report.html`
(both artifacts go inside the `gtm-audit-report/` output folder — never loose in the
project root), then give the user the headline (score, ready-to-build or not, weakest
link, top actions) and the report folder path.

Distribution channels are **surface-aware**: establish `project.surfaces` (web / iOS /
Android / desktop / …) first, and mark surface-inapplicable dimensions and stages N/A
(excluded from the score) — most notably, **App Store / Google Play (ASO, Stage 15) is
N/A unless the product ships through an app store (iOS / Android / Mac App Store).** Never
score or recommend app-store channels for a website-only product.

Remember the prime directive: **primary user-pain evidence before keyword/SERP tools.**
If pain evidence or user-language mapping is missing, the verdict is "not ready to
build — fix primary evidence first," regardless of how good the tool-driven work looks.
