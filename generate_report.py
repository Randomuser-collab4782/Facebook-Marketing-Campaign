"""
Generate a single combined campaign report in Markdown.

Usage:
    python generate_report.py

Output:
    campaign_report.md
"""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path

# .env loader
_env_path = Path(__file__).resolve().parent / ".env"
if _env_path.exists():
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _key, _, _val = _line.partition("=")
                _val = _val.strip().strip("\"'")
                os.environ.setdefault(_key.strip(), _val)

from brand_constants import (
    BRAND, COLOURS, SELLING_POINTS, TARGET_AUDIENCE,
    CAMPAIGN_THEMES, AD_FORMATS, BUDGET_STRATEGY, IB_SUBJECTS,
    AD_COPY_LIMITS,
)
from ad_copy_generator import generate_variations
from audience_targeting import AUDIENCE_SEGMENTS
from campaign_calendar import export_calendar_markdown, get_active_campaigns
from creative_briefs import generate_all_briefs, export_brief_markdown


def main() -> None:
    lines: list[str] = []

    # ── Title ──
    lines.append(f"# {BRAND['company_name']} — Full Campaign Report")
    lines.append(f"")
    lines.append(f"**Generated:** {date.today().strftime('%d %B %Y')}  ")
    lines.append(f"**Website:** {BRAND['website']}  ")
    lines.append(f"**Tagline:** {BRAND['tagline']}")
    lines.append(f"")
    lines.append(f"> {BRAND['short_description']}")
    lines.append(f"")

    # ── 1. Brand Overview ──
    lines.append("---")
    lines.append("## 1. Brand Overview")
    lines.append("")
    lines.append(f"**Mission:** {BRAND['mission']}")
    lines.append("")
    lines.append(f"**Voice:** {BRAND['voice']['tone']} — {BRAND['voice']['formality']}")
    lines.append("")
    lines.append("### Colour Palette")
    lines.append("")
    lines.append("| Colour | Hex | Usage |")
    lines.append("|--------|-----|-------|")
    colour_usage = {
        "primary": "Trust, academic authority",
        "secondary": "Innovation, freshness",
        "accent": "Energy, optimism, CTA highlight",
        "background": "Clean, readable",
        "background_dark": "Dark-mode / contrast",
        "text_primary": "Body text",
        "text_secondary": "Supporting text",
        "success": "Score improvements",
        "error": "Urgency accents",
    }
    for name, hex_val in COLOURS.items():
        usage = colour_usage.get(name, "")
        lines.append(f"| {name} | `{hex_val}` | {usage} |")
    lines.append("")

    lines.append("### Key Selling Points")
    lines.append("")
    for sp in SELLING_POINTS:
        lines.append(f"- **{sp['headline']}** — {sp['detail']}")
    lines.append("")

    # ── 2. Target Audiences ──
    lines.append("---")
    lines.append("## 2. Target Audiences")
    lines.append("")
    for key in ("primary", "secondary", "tertiary"):
        aud = TARGET_AUDIENCE[key]
        lines.append(f"### {aud['label']} ({key.title()})")
        lines.append(f"**Age range:** {aud['age_range']}  ")
        lines.append(f"{aud['description']}")
        if "pain_points" in aud:
            lines.append("")
            lines.append("**Pain points:**")
            for pp in aud["pain_points"]:
                lines.append(f"- {pp}")
        lines.append("")

    # ── 3. Facebook Audience Segments ──
    lines.append("---")
    lines.append("## 3. Facebook Audience Segments")
    lines.append("")
    lines.append("| # | Segment | Funnel | Age | Est. Reach | Daily Budget |")
    lines.append("|---|---------|--------|-----|------------|--------------|")
    for i, seg in enumerate(AUDIENCE_SEGMENTS, 1):
        lines.append(
            f"| {i} | {seg['name']} | {seg['funnel_stage']} | "
            f"{seg['age_min']}-{seg['age_max']} | {seg.get('estimated_reach', 'N/A')} | "
            f"${seg.get('recommended_daily_budget_usd', 'N/A')} |"
        )
    lines.append("")

    # ── 4. Campaign Themes & Ad Copy ──
    lines.append("---")
    lines.append("## 4. Campaign Themes & Ad Copy")
    lines.append("")
    for theme in CAMPAIGN_THEMES:
        lines.append(f"### Theme: {theme['name']}")
        lines.append(f"**Hook:** {theme['hook']}  ")
        lines.append(f"**Angle:** {theme['angle']}  ")
        lines.append(f"**CTA:** {theme['cta']}  ")
        lines.append(f"**Best formats:** {', '.join(theme['best_for'])}")
        lines.append("")

        variations = generate_variations(theme_id=theme["id"], num_variations=3)
        for v in variations:
            fw = v["metadata"]["framework_label"]
            lines.append(f"**{fw}:**")
            lines.append(f"- **Headline:** {v['headline']}")
            lines.append(f"- **Primary text:** {v['primary_text']}")
            lines.append(f"- **Description:** {v['description']}")
            lines.append(f"- **CTA:** {v['cta']}")
            lines.append("")

    # ── 5. Ad Formats ──
    lines.append("---")
    lines.append("## 5. Ad Formats")
    lines.append("")
    lines.append("| Format | Dimensions | Aspect Ratio | Platforms |")
    lines.append("|--------|-----------|--------------|-----------|")
    for key, fmt in AD_FORMATS.items():
        platforms = ", ".join(fmt["platforms"])
        lines.append(f"| {fmt['label']} | {fmt['width']}x{fmt['height']} | {fmt['aspect_ratio']} | {platforms} |")
    lines.append("")

    # ── 6. Budget Strategy ──
    lines.append("---")
    lines.append("## 6. Budget Strategy (70-20-10 Rule)")
    lines.append("")
    lines.append("| Category | Allocation | Description |")
    lines.append("|----------|-----------|-------------|")
    for cat in ("proven", "testing", "experimental"):
        b = BUDGET_STRATEGY[cat]
        lines.append(f"| {cat.title()} | {int(b['allocation']*100)}% | {b['description']} |")
    lines.append("")
    lines.append(f"**Target ROAS:** {BUDGET_STRATEGY['target_roas']}:1  ")
    lines.append(f"**Optimisation cadence:** {BUDGET_STRATEGY['optimisation_cadence']}  ")
    lines.append(f"**Variations per campaign:** {BUDGET_STRATEGY['creative_variations_per_campaign']}")
    lines.append("")

    # ── 7. Campaign Calendar ──
    lines.append("---")
    lines.append("## 7. Campaign Calendar")
    lines.append("")
    calendar_md = export_calendar_markdown()
    # Strip the top-level heading from calendar since we have our own
    for line in calendar_md.splitlines():
        if line.startswith("# "):
            continue
        lines.append(line)
    lines.append("")

    # ── 8. Active Campaigns (Today) ──
    lines.append("---")
    lines.append("## 8. Active Campaigns Right Now")
    lines.append("")
    active = get_active_campaigns()
    if active:
        for phase in active:
            lines.append(f"- **{phase['phase_name']}** ({phase['start_date']} to {phase['end_date']})")
    else:
        lines.append("No campaigns active today.")
    lines.append("")

    # ── 9. Creative Briefs ──
    lines.append("---")
    lines.append("## 9. Creative Briefs")
    lines.append("")
    briefs = generate_all_briefs()
    for brief in briefs:
        md = export_brief_markdown(brief)
        # Indent brief headings to be sub-sections
        for line in md.splitlines():
            if line.startswith("# "):
                lines.append(f"### {line[2:]}")
            elif line.startswith("## "):
                lines.append(f"#### {line[3:]}")
            else:
                lines.append(line)
        lines.append("")
        lines.append("---")
        lines.append("")

    # ── 10. IB Subjects Covered ──
    lines.append("## 10. IB Subjects Covered")
    lines.append("")
    for group, subjects in IB_SUBJECTS.items():
        lines.append(f"**{group.replace('_', ' ').title()}:** {', '.join(subjects)}")
    lines.append("")

    # ── Footer ──
    lines.append("---")
    lines.append(f"*Report generated by T&N IB Education Campaign Pipeline on {date.today().strftime('%d %B %Y')}.*")

    report = "\n".join(lines)
    output_path = Path(__file__).resolve().parent / "campaign_report.md"
    output_path.write_text(report)
    print(f"Campaign report saved to: {output_path}")
    print(f"Size: {len(report):,} characters")


if __name__ == "__main__":
    main()
