#!/usr/bin/env python3
"""Render a GTM audit-data JSON file into a self-contained HTML report.

Stdlib-only. No CDN, no external assets — the output opens offline by double-click.
Charts are inline SVG; colors come from the dataviz reference palette (validated).

Usage:
    python3 render_report.py audit-data.json -o gtm-audit-report.html
"""
import argparse
import html
import json
import math
import sys

# --- palette (from dataviz references/palette.md, validated) --------------------
ACCENT_LIGHT = "#2a78d6"
ACCENT_DARK = "#3987e5"
STATUS = {  # band/maturity -> status color (fixed, never themed)
    "solid": "#0ca30c", "green": "#0ca30c",
    "partial": "#fab219", "amber": "#fab219",
    "missing": "#d03b3b", "red": "#d03b3b",
    "na": "#898781",
}
BAND_LABEL = {"solid": "Solid", "partial": "Partial", "missing": "Missing", "na": "N/A"}

RADAR_LABELS = {
    "pain_evidence": "Pain", "user_language": "Language", "keyword_opportunity": "Keywords",
    "serp_competition": "SERP", "channel_selection": "Channels", "directory_strategy": "Directory",
    "content_assets": "Content", "landing_seo": "Landing", "aso": "ASO", "geo_ai": "GEO",
    "conversion_retention": "Convert", "measurement_loop": "Measure",
}


def esc(s):
    return html.escape(str(s if s is not None else ""))


def band_color(band):
    return STATUS.get(band, "#898781")


# --- gauge ----------------------------------------------------------------------
def render_gauge(score, band):
    """Donut ring gauge with the score in the center."""
    r, cx, cy, sw = 66, 90, 90, 14
    circ = 2 * math.pi * r
    frac = max(0, min(100, score)) / 100.0
    dash = circ * frac
    color = band_color(band)
    return f'''<svg viewBox="0 0 180 180" width="180" height="180" role="img"
      aria-label="Readiness score {score} of 100">
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="var(--grid)" stroke-width="{sw}"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{sw}"
        stroke-linecap="round" stroke-dasharray="{dash:.2f} {circ:.2f}"
        transform="rotate(-90 {cx} {cy})"/>
      <text x="{cx}" y="{cy-4}" text-anchor="middle" font-size="44" font-weight="700"
        fill="var(--text-primary)">{score}</text>
      <text x="{cx}" y="{cy+22}" text-anchor="middle" font-size="14"
        fill="var(--text-secondary)">of 100</text>
    </svg>'''


# --- radar ----------------------------------------------------------------------
def render_radar(dimensions):
    dims = [d for d in dimensions if d.get("band") != "na"]
    n = len(dims)
    total = len(dimensions)
    caption = (f'<p class="muted radar-cap">{n} of {total} dimensions apply '
               f'(N/A ones excluded).</p>') if n < total else ""
    if n < 3:
        return "<p class='muted'>Not enough dimensions for a radar chart.</p>" + caption
    size, cx, cy, R = 420, 210, 210, 150
    rings = [25, 50, 75, 100]
    parts = [f'<svg viewBox="0 0 {size} {size}" width="100%" style="max-width:440px"'
             ' role="img" aria-label="Readiness by dimension (see table below for values)">']

    def pt(frac, i):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        return cx + R * frac * math.cos(ang), cy + R * frac * math.sin(ang)

    # grid rings
    for ring in rings:
        f = ring / 100.0
        poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(f, i) for i in range(n)))
        parts.append(f'<polygon points="{poly}" fill="none" stroke="var(--grid)" stroke-width="1"/>')
    # axes + labels
    for i, d in enumerate(dims):
        ex, ey = pt(1.0, i)
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="var(--grid)" stroke-width="1"/>')
        lx, ly = pt(1.14, i)
        anchor = "middle"
        if lx < cx - 6:
            anchor = "end"
        elif lx > cx + 6:
            anchor = "start"
        label = RADAR_LABELS.get(d.get("id"), d.get("name", "")[:8])
        parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" dominant-baseline="middle"'
                     f' font-size="12" fill="var(--text-secondary)">{esc(label)}</text>')
    # data polygon
    dpoly = " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(d.get("score", 0) / 100.0, i) for i, d in enumerate(dims)))
    parts.append(f'<polygon points="{dpoly}" fill="var(--accent)" fill-opacity="0.18"'
                 ' stroke="var(--accent)" stroke-width="2"/>')
    # data points with native tooltips
    for i, d in enumerate(dims):
        x, y = pt(d.get("score", 0) / 100.0, i)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="var(--accent)"'
                     f' stroke="var(--surface-1)" stroke-width="1.5">'
                     f'<title>{esc(d.get("name"))}: {d.get("score")}/100</title></circle>')
    parts.append("</svg>")
    return "".join(parts) + caption


# --- 20-stage funnel heatmap ----------------------------------------------------
def render_heatmap(stages):
    cells = []
    for s in sorted(stages, key=lambda x: x.get("n", 0)):
        maturity = s.get("maturity")
        color = STATUS.get(maturity, "#898781")
        is_na = maturity == "na"
        tip = s.get("na_reason", "") if is_na else s.get("note", "")
        cls = "cell na" if is_na else "cell"
        cells.append(
            f'<div class="{cls}" style="--c:{color}" title="{esc(tip)}">'
            f'<span class="cell-n">{s.get("n")}</span>'
            f'<span class="cell-name">{esc(s.get("name"))}</span>'
            f'{"<span class=cell-na>N/A</span>" if is_na else ""}'
            f'</div>'
        )
    return f'<div class="heatmap">{"".join(cells)}</div>'


# --- top actions ----------------------------------------------------------------
def render_actions(actions):
    if not actions:
        return "<p class='muted'>No actions recorded.</p>"
    rows = []
    for a in sorted(actions, key=lambda x: -x.get("priority", 0)):
        rows.append(
            f'<tr><td>{esc(a.get("summary"))}</td>'
            f'<td class="mono">{esc(a.get("dimension"))}</td>'
            f'<td class="num">{esc(a.get("impact"))}</td>'
            f'<td class="num">{esc(a.get("effort"))}</td>'
            f'<td class="num strong">{a.get("priority", 0):.1f}</td></tr>'
        )
    return (
        '<table class="grid"><thead><tr><th>Next action</th><th>Dimension</th>'
        '<th class="num">Impact</th><th class="num">Effort</th><th class="num">Priority</th>'
        f'</tr></thead><tbody>{"".join(rows)}</tbody></table>'
    )


# --- dimension detail -----------------------------------------------------------
def render_dimensions(dimensions):
    rows = []
    for d in dimensions:
        band = d.get("band", "na")
        color = band_color(band)
        gate = ' <span class="pill gate">GATE</span>' if d.get("is_gate") else ""
        deleg = d.get("delegated_to")
        deleg_html = f' <span class="pill deleg">→ {esc(deleg)}</span>' if deleg else ""
        if band == "na":
            # N/A dimensions are excluded from the score — suppress the bar and score,
            # show why instead of gaps/actions.
            reason = d.get("na_reason") or "Not applicable to this product."
            rows.append(f'''<tr class="na">
          <td>
            <div class="dim-name">{esc(d.get("name"))}{gate}{deleg_html}</div>
            <ul class="mini"><li>{esc(reason)}</li></ul>
          </td>
          <td class="num strong" style="color:{color}">—</td>
          <td><span class="pill" style="background:{color}1f;color:{color};border-color:{color}">{BAND_LABEL.get(band, band)}</span></td>
        </tr>''')
            continue
        gaps = "".join(f"<li>{esc(g.get('summary'))}</li>" for g in d.get("gaps", []))
        acts = "".join(f"<li>{esc(a)}</li>" for a in d.get("next_actions", []))
        bar_w = max(2, min(100, d.get("score", 0)))
        rows.append(f'''<tr>
          <td>
            <div class="dim-name">{esc(d.get("name"))}{gate}{deleg_html}</div>
            <div class="bar"><span style="width:{bar_w}%;background:{color}"></span></div>
            {f'<ul class="mini">{gaps}</ul>' if gaps else ''}
            {f'<ul class="mini act">{acts}</ul>' if acts else ''}
          </td>
          <td class="num strong" style="color:{color}">{d.get("score")}</td>
          <td><span class="pill" style="background:{color}1f;color:{color};border-color:{color}">{BAND_LABEL.get(band, band)}</span></td>
        </tr>''')
    return (
        '<table class="grid dims"><thead><tr><th>Dimension &amp; gaps</th>'
        '<th class="num">Score</th><th>Band</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table>'
    )


def render_channel(ch):
    if not ch:
        return ""
    chans = "".join(f'<span class="chip">{esc(c)}</span>' for c in ch.get("primary_channels", []))
    return f'''<div class="card">
      <h3>Recommended channels</h3>
      <div class="chips">{chans}</div>
      <p><strong>Directory:</strong> {esc(ch.get("directory_call"))}</p>
      <p class="muted">{esc(ch.get("rationale"))}</p>
    </div>'''


def render_redflags(flags):
    if not flags:
        return ""
    items = "".join(
        f'<li><span class="mono">#{f.get("n")}</span> {esc(f.get("assumption"))}'
        f'<span class="muted"> — {esc(f.get("dimension"))}</span></li>'
        for f in flags
    )
    return f'<div class="card"><h3>Red flags (wrong assumptions detected)</h3><ul class="flags">{items}</ul></div>'


def _na_note(data):
    """Auto-derive a one-line explanation when any dimension/stage is N/A."""
    na_dims = [d for d in data.get("dimensions", []) if d.get("band") == "na"]
    na_stages = [s for s in data.get("stages", []) if s.get("maturity") == "na"]
    if not na_dims and not na_stages:
        return ""
    names = [d.get("name", "") for d in na_dims]
    surfaces = data.get("project", {}).get("surfaces") or []
    surf_txt = ", ".join(surfaces) if surfaces else "the declared surfaces"
    listed = "; ".join(n for n in names if n) or f"{len(na_stages)} funnel stage(s)"
    return (f'<p class="na-note"><span class="k" style="background:{STATUS["na"]}"></span>'
            f'Marked <strong>N/A</strong> and excluded from the score: {esc(listed)} — '
            f'not applicable to a product shipping {esc(surf_txt)}.</p>')


def build_html(data):
    p = data.get("project", {})
    score = data.get("readiness_score", 0)
    overall_band = "solid" if score >= 70 else "partial" if score >= 40 else "missing"
    blocked = data.get("gate_status") == "blocked"
    banner_color = STATUS["missing"] if blocked else STATUS["solid"]
    banner_icon = "⚠" if blocked else "✓"
    banner_title = "Not ready to build — fix primary evidence first" if blocked else "Evidence gates cleared — ready to build"
    banner_reason = data.get("gate_reason", "") if blocked else "Primary pain evidence and user-language mapping are in place; downstream channel work rests on real evidence."

    title = f"GTM Readiness Audit — {p.get('name', 'Project')}"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>
:root {{
  --surface-1:#fcfcfb; --page:#f9f9f7; --text-primary:#0b0b0b; --text-secondary:#52514e;
  --muted:#898781; --grid:#e1e0d9; --baseline:#c3c2b7; --border:rgba(11,11,11,.10);
  --accent:{ACCENT_LIGHT};
  color-scheme: light dark;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --surface-1:#1a1a19; --page:#0d0d0d; --text-primary:#fff; --text-secondary:#c3c2b7;
    --muted:#898781; --grid:#2c2c2a; --baseline:#383835; --border:rgba(255,255,255,.10);
    --accent:{ACCENT_DARK};
  }}
}}
:root[data-theme="dark"] {{
  --surface-1:#1a1a19; --page:#0d0d0d; --text-primary:#fff; --text-secondary:#c3c2b7;
  --muted:#898781; --grid:#2c2c2a; --baseline:#383835; --border:rgba(255,255,255,.10);
  --accent:{ACCENT_DARK};
}}
:root[data-theme="light"] {{
  --surface-1:#fcfcfb; --page:#f9f9f7; --text-primary:#0b0b0b; --text-secondary:#52514e;
  --muted:#898781; --grid:#e1e0d9; --baseline:#c3c2b7; --border:rgba(11,11,11,.10);
  --accent:{ACCENT_LIGHT};
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--page); color:var(--text-primary);
  font-family:system-ui,-apple-system,"Segoe UI",sans-serif; line-height:1.5; }}
.wrap {{ max-width:960px; margin:0 auto; padding:32px 20px 80px; }}
header.top {{ display:flex; justify-content:space-between; align-items:flex-start; gap:16px; flex-wrap:wrap; }}
h1 {{ font-size:24px; margin:0 0 4px; }}
h2 {{ font-size:16px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted);
  margin:40px 0 12px; font-weight:600; }}
h3 {{ font-size:15px; margin:0 0 10px; }}
.sub {{ color:var(--text-secondary); margin:0; }}
.meta {{ color:var(--muted); font-size:13px; margin-top:6px; }}
.theme-btn {{ background:var(--surface-1); color:var(--text-secondary); border:1px solid var(--border);
  border-radius:8px; padding:6px 12px; font-size:13px; cursor:pointer; }}
.hero {{ display:flex; gap:28px; align-items:center; margin-top:24px; flex-wrap:wrap; }}
.banner {{ border-radius:12px; padding:16px 18px; margin-top:20px; display:flex; gap:12px;
  align-items:flex-start; border:1px solid; }}
.banner .ico {{ font-size:20px; line-height:1; }}
.banner .bt {{ font-weight:700; margin:0 0 2px; }}
.banner .br {{ margin:0; color:var(--text-secondary); font-size:14px; }}
.na-note {{ margin:10px 0 0; font-size:13px; color:var(--text-secondary); }}
.na-note .k {{ display:inline-block; width:10px; height:10px; border-radius:2px; margin-right:6px; vertical-align:middle; }}
.radar-cap {{ text-align:center; font-size:12px; margin:8px 0 0; }}
tr.na td {{ opacity:.6; }}
.card {{ background:var(--surface-1); border:1px solid var(--border); border-radius:12px;
  padding:18px; margin-top:16px; }}
.cols {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
@media (max-width:720px) {{ .cols {{ grid-template-columns:1fr; }} }}
.radar-wrap {{ display:flex; justify-content:center; }}
.heatmap {{ display:grid; grid-template-columns:repeat(5,1fr); gap:6px; }}
@media (max-width:720px) {{ .heatmap {{ grid-template-columns:repeat(2,1fr); }} }}
.cell {{ border-left:5px solid var(--c); background:var(--surface-1); border:1px solid var(--border);
  border-left:5px solid var(--c); border-radius:8px; padding:8px 10px; min-height:56px; }}
.cell.na {{ border-style:dashed; border-left-style:dashed; opacity:.55; }}
.cell.na .cell-name {{ color:var(--muted); }}
.cell-na {{ display:inline-block; font-size:10px; font-weight:700; letter-spacing:.04em;
  color:var(--muted); border:1px solid var(--border); border-radius:4px; padding:0 4px; margin-top:4px; }}
.cell-n {{ display:inline-block; font-size:11px; color:var(--muted); font-weight:700; }}
.cell-name {{ display:block; font-size:12px; color:var(--text-primary); }}
.tablewrap {{ overflow-x:auto; }}
table.grid {{ width:100%; border-collapse:collapse; font-size:14px; }}
table.grid th {{ text-align:left; color:var(--muted); font-weight:600; font-size:12px;
  text-transform:uppercase; letter-spacing:.03em; padding:8px 10px; border-bottom:1px solid var(--border); }}
table.grid td {{ padding:10px; border-bottom:1px solid var(--border); vertical-align:top; }}
.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
.strong {{ font-weight:700; }}
.mono {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:12px; color:var(--text-secondary); }}
.muted {{ color:var(--muted); }}
.dim-name {{ font-weight:600; margin-bottom:6px; }}
.bar {{ height:6px; background:var(--grid); border-radius:4px; overflow:hidden; max-width:280px; }}
.bar span {{ display:block; height:100%; border-radius:4px; }}
ul.mini {{ margin:8px 0 0; padding-left:18px; font-size:13px; color:var(--text-secondary); }}
ul.mini.act {{ color:var(--text-primary); }}
ul.mini.act li::marker {{ color:var(--accent); }}
.pill {{ display:inline-block; font-size:11px; padding:1px 8px; border-radius:999px;
  border:1px solid var(--border); }}
.pill.gate {{ background:#d03b3b1f; color:#d03b3b; border-color:#d03b3b; font-weight:700; }}
.pill.deleg {{ color:var(--text-secondary); }}
.chips {{ display:flex; gap:8px; flex-wrap:wrap; margin-bottom:10px; }}
.chip {{ background:var(--accent); color:#fff; border-radius:999px; padding:4px 12px; font-size:13px; font-weight:600; }}
ul.flags {{ margin:0; padding-left:18px; }}
ul.flags li {{ margin-bottom:6px; font-size:14px; }}
.legend {{ display:flex; gap:16px; flex-wrap:wrap; font-size:12px; color:var(--text-secondary); margin-top:10px; }}
.legend .k {{ display:inline-block; width:10px; height:10px; border-radius:2px; margin-right:5px; vertical-align:middle; }}
footer {{ margin-top:48px; color:var(--muted); font-size:12px; border-top:1px solid var(--border); padding-top:16px; }}
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div>
      <h1>{esc(p.get("name"))} — GTM Readiness Audit</h1>
      <p class="sub">{esc(p.get("one_liner"))}</p>
      <p class="meta">{esc(p.get("type"))}{f' · surfaces: {esc(", ".join(p.get("surfaces")))}' if p.get("surfaces") else ""} · input: {esc(p.get("input_mode"))} · {esc(p.get("audited_at"))}</p>
    </div>
    <button class="theme-btn" onclick="tgl()">◐ Theme</button>
  </header>

  <div class="hero">
    {render_gauge(score, overall_band)}
    <div style="flex:1; min-width:240px">
      <div class="banner" style="border-color:{banner_color}; background:{banner_color}14">
        <span class="ico" style="color:{banner_color}">{banner_icon}</span>
        <div>
          <p class="bt" style="color:{banner_color}">{esc(banner_title)}</p>
          <p class="br">{esc(banner_reason)}</p>
        </div>
      </div>
      {_na_note(data)}
    </div>
  </div>

  <div class="cols">
    <div>
      <h2>Readiness by dimension</h2>
      <div class="card radar-wrap">{render_radar(data.get("dimensions", []))}</div>
    </div>
    <div>
      <h2>Top next actions</h2>
      <div class="card"><div class="tablewrap">{render_actions(data.get("top_actions", []))}</div></div>
    </div>
  </div>

  <h2>Distribution funnel — 20-stage maturity</h2>
  {render_heatmap(data.get("stages", []))}
  <div class="legend">
    <span><span class="k" style="background:{STATUS['green']}"></span>Solid / done</span>
    <span><span class="k" style="background:{STATUS['amber']}"></span>Partial / unvalidated</span>
    <span><span class="k" style="background:{STATUS['red']}"></span>Missing / blocking</span>
    <span><span class="k" style="background:{STATUS['na']}"></span>N/A — not applicable to this product</span>
  </div>

  <div class="cols" style="margin-top:8px">
    {render_channel(data.get("channel_recommendation"))}
    {render_redflags(data.get("red_flags"))}
  </div>

  <h2>Dimension detail</h2>
  <div class="tablewrap">{render_dimensions(data.get("dimensions", []))}</div>

  <footer>
    Generated by the <strong>gtm-distribution-audit</strong> plugin. Scores follow the
    Distribution Channel Playbook — primary evidence (pain, user language) gates downstream
    tool-driven work. This is a readiness snapshot, not a guarantee; re-audit as evidence changes.
  </footer>
</div>
<script>
function tgl(){{
  var r=document.documentElement;
  var cur=r.getAttribute('data-theme');
  if(!cur){{ cur = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark':'light'; }}
  r.setAttribute('data-theme', cur==='dark'?'light':'dark');
}}
</script>
</body>
</html>'''


def main():
    ap = argparse.ArgumentParser(description="Render GTM audit-data JSON to a self-contained HTML report.")
    ap.add_argument("data", help="Path to audit-data.json")
    ap.add_argument("-o", "--out", default="gtm-audit-report.html", help="Output HTML path")
    args = ap.parse_args()

    try:
        with open(args.data, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR reading data: {e}", file=sys.stderr)
        return 2

    html_out = build_html(data)
    try:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(html_out)
    except OSError as e:
        print(f"ERROR writing output: {e}", file=sys.stderr)
        return 2

    print(f"Wrote {args.out} ({len(html_out)} bytes) — open it in a browser.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
