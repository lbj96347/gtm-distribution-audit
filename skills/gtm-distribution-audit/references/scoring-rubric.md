# Scoring Rubric — 12 Readiness Dimensions

Each dimension is scored **0–100** and produces:
`{ id, name, score, band, weight, is_gate, evidence[], gaps[], next_actions[], delegated_to }`

## Score bands

| Band | Range | Meaning | Heatmap color |
|---|---|---|---|
| solid | 70–100 | Real primary evidence; ready to build on | green |
| partial | 40–69 | Some work, unvalidated or thin | amber |
| missing | 0–39 | Absent or assumption-only | red |

## Weights & gates

Gates are the primary-evidence dimensions. If a **gate** dimension scores < 40, the
overall report shows the **"Not ready to build — fix primary evidence first"** banner
and all tool-driven dimensions (3, 4, 8, 9, 10) are capped/discounted in the
composite, per the playbook's "tools are secondary evidence" rule.

| # | id | Dimension | Weight | Gate? | Delegates to |
|---|---|---|---|---|---|
| 1 | pain_evidence | Pain evidence (primary) | 3.0 | ✅ | gtm-pain-evidence |
| 2 | user_language | User language & intent | 3.0 | ✅ | gtm-pain-evidence |
| 3 | keyword_opportunity | Keyword opportunity | 2.0 | — | — (opportunity formula) |
| 4 | serp_competition | SERP / competition | 1.5 | — | seo-technical |
| 5 | channel_selection | Channel selection (1–2 deep) | 2.0 | — | gtm-channel-directory |
| 6 | directory_strategy | Directory strategy | 1.0 | — | gtm-channel-directory + seo-schema |
| 7 | content_assets | Content assets & format | 1.5 | — | seo-content |
| 8 | landing_seo | Landing page / on-page SEO | 1.5 | — | seo-technical |
| 9 | aso | App Store Optimization | 1.0 | — | (inline ASO rubric below) |
| 10 | geo_ai | GEO / AI visibility | 1.5 | — | seo-geo |
| 11 | conversion_retention | Conversion / activation / retention | 2.0 | — | gtm-conversion-loop |
| 12 | measurement_loop | Measurement & learning loop | 1.5 | — | gtm-conversion-loop |

**Composite readiness** = weighted mean over the **applicable** dimensions only,
rounded 0–100:

```
readiness = Σ(wᵢ · scoreᵢ) / Σ(wᵢ)   for every dimension where band ≠ "na"
```

A dimension marked `band: "na"` (not applicable to the product's surfaces — see below)
contributes **neither its score nor its weight** — it is dropped from both sums, so a
web-only product is never penalized for lacking an app. When a gate is < 40, multiply
each tool-driven dimension's contribution by 0.5 before the mean (evidence discount)
and set `gate_status = "blocked"`.

## Surface applicability (which dimensions/stages apply)

Read `project.surfaces` (the surfaces the product actually ships: `web`, `ios`,
`android`, `mac_app_store`, `desktop`, `browser_extension`, `api_cli`, `marketplace`, …).
A dimension or funnel stage that depends on a surface the product does **not** ship is
marked N/A (dimension `band: "na"`, stage `maturity: "na"`) with a short `na_reason`, and
excluded from the composite. An **app-store surface** = `ios`, `android`, or
`mac_app_store` (any store with a listing to optimize). Default: every dimension/stage
applies to all surfaces **except**:

| Item | Applies only when surfaces include | N/A otherwise |
|---|---|---|
| Dim 9 — ASO | an app-store surface (`ios`/`android`/`mac_app_store`) | `band: "na"`, e.g. "No app-store surface — ASO not applicable" |
| Stage 15 — App Store optimization | an app-store surface | `maturity: "na"`, same reason |

This table is the extension point: add rows here as new surface-specific rules emerge.
Everything else (pain, language, keywords, SERP, channels, content, landing, GEO,
conversion, measurement) applies regardless of surface.

## Per-dimension scoring anchors

Score by the strongest anchor that is fully true; interpolate between.

### 1. Pain evidence (GATE)
- 0–39: Only the founder's belief / feature list. No user quotes.
- 40–69: A handful of anecdotal signals, not clustered or counted.
- 70–100: ≥5 interviews **or** 20+ reviews/comments clustered into named problem
  hypotheses, each with cited raw sources (source_type + excerpt).

### 2. User language & intent (GATE)
- 0–39: Product described only in developer/feature language.
- 40–69: A rough list of user phrases, no dev↔user mapping, no intent classes.
- 70–100: A dev-term ↔ user-term glossary with frequency, plus each query tagged
  informational / comparison / solution / buying.

### 3. Keyword opportunity
- 0–39: No keywords, or popularity-only list.
- 40–69: Keyword list exists but scored by volume alone.
- 70–100: Keywords scored by the opportunity formula (intent × relevance ×
  1/competition × product_fit), long-tail included, popular-vs-opportunity split.
- **Gate rule:** cannot exceed 50 if dim 2 (user_language) < 40.

### 4. SERP / competition  → seo-technical
- Weak/undifferentiated SERP that's actually beatable = opportunity (higher score);
  authority-dominated SERP with no gap = low score. Score reflects *whether a
  realistic content gap was identified*, not just that SERPs were viewed.

### 5. Channel selection
- 0–39: "Post everywhere" or no channel chosen.
- 40–69: Channels named but >2, or chosen by hype not user-intent fit.
- 70–100: **1–2 channels** chosen with rationale tied to where users show intent
  and matching content format + conversion path (see channel-matrix.md).

### 6. Directory strategy  → seo-channel + seo-schema
- Score the owned-vs-third-party decision quality vs SERP directory dominance and
  portfolio breadth (see directory-strategy.md). N/A → score 50 (neutral) and note.

### 7. Content assets & format  → seo-content
- Reflects content depth, E-E-A-T, format-fit to chosen channel, and pain-first
  (not feature-first) angles.

### 8. Landing page / on-page SEO  → seo-technical
- Reflects intent-match of the page to the target keyword, promise alignment with
  upstream content, on-page SEO, and schema.

### 9. ASO (inline rubric — no delegated skill)
Score the App Store package **only when `project.surfaces` includes an app-store surface
(`ios`, `android`, or `mac_app_store`)**. Otherwise mark `band: "na"` with a `na_reason`
and omit from the composite (and set stage 15 to `maturity: "na"` to match). When it does
apply, score by:
- Title: contains primary user-language keyword (not just brand). +
- Subtitle: secondary keywords + clear value. +
- Keyword field: filled with user-language long-tail, no wasted spaces. +
- Screenshots: problem/benefit-first captions, not feature tour. +
- Popularity read via Apple's **1–5 relative** score with validation caveat. +

### 10. GEO / AI visibility  → seo-geo
- Reflects AI-crawler accessibility (GPTBot/ClaudeBot/PerplexityBot), llms.txt,
  passage-level citability, brand-mention signals, presence in curated lists AI cites.

### 11. Conversion / activation / retention  → gtm-conversion-loop
- Reflects CTA/onboarding, time-to-first-value, and the extended funnel
  (install → first action → repeat → review → referral). Install-only tracking = low.

### 12. Measurement & learning loop  → gtm-conversion-loop
- 0–39: No analytics, or vanity metrics only.
- 40–69: Installs/traffic tracked but not attributed to keyword/channel/content.
- 70–100: Event pipeline attributes activation to upstream keyword→content→channel→
  pain, with a stated repeat/adjust/drop iteration cadence.

## Gap prioritization

Each gap carries `impact` (1–5) and `effort` (1–5). Rank the report's "Top next
actions" by `priority = impact / effort`, descending. Gate-dimension gaps get a
+1 impact bonus (never above 5).
