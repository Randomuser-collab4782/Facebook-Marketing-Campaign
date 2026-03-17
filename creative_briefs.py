"""
Creative Brief Generator for T&N IB Education — Facebook/Instagram Campaigns
=============================================================================
Generates structured creative briefs for each campaign theme, ready for
designers and copywriters to execute against.

Usage:
    python creative_briefs.py          # Generate all briefs to briefs/ directory
    python creative_briefs.py score_boost   # Generate a single brief by theme ID
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any

from brand_constants import (
    AD_FORMATS,
    BRAND,
    BUDGET_STRATEGY,
    CAMPAIGN_THEMES,
    COLOURS,
    FONTS,
    SELLING_POINTS,
    TARGET_AUDIENCE,
)

# =============================================================================
# THEME-SPECIFIC VISUAL & COPY DIRECTION
# =============================================================================
# Each entry maps a theme ID to guidance a designer can act on directly.

_VISUAL_DIRECTION: dict[str, dict[str, Any]] = {
    "ia_kickstart": {
        "mood": "Calm, empowering, fresh-start energy",
        "imagery_style": (
            "Clean workspace flat-lays — laptop, notebook, highlighters. "
            "Split-screen before/after showing a blank doc vs. structured IA outline. "
            "Soft gradient overlays transitioning from navy to teal."
        ),
        "colour_usage": {
            "dominant": COLOURS["primary"],
            "supporting": COLOURS["secondary"],
            "accent": COLOURS["accent"],
            "background": COLOURS["background"],
        },
        "layout_notes": (
            "Hero text top-third, supporting visual centre, CTA button bottom. "
            "Use the accent amber for the CTA pill. Keep whitespace generous — "
            "the message is 'simplicity'."
        ),
    },
    "score_boost": {
        "mood": "Celebratory, aspirational, proof-driven",
        "imagery_style": (
            "Testimonial-style layouts: large score numbers in Space Grotesk, "
            "student photo or avatar alongside a quote card. "
            "Use upward-trending graph motifs and the success green for "
            "score-change highlights (e.g., '4 -> 7' with an arrow)."
        ),
        "colour_usage": {
            "dominant": COLOURS["success"],
            "supporting": COLOURS["primary"],
            "accent": COLOURS["accent"],
            "background": COLOURS["background"],
        },
        "layout_notes": (
            "Carousel: each card = one student story. Card 1 = hook stat, "
            "Cards 2-4 = individual testimonials, Card 5 = CTA. "
            "For single-image: large score delta centred, quote below, CTA bottom."
        ),
    },
    "ai_ethics": {
        "mood": "Trustworthy, transparent, reassuring",
        "imagery_style": (
            "Trust-building imagery: shield/check icons, IB logo placement "
            "(if licensed), side-by-side comparison of 'AI that writes for you' "
            "(red cross) vs. 'AI that guides your thinking' (green check). "
            "Clean infographic style with generous whitespace."
        ),
        "colour_usage": {
            "dominant": COLOURS["primary"],
            "supporting": COLOURS["background"],
            "accent": COLOURS["success"],
            "contrast": COLOURS["error"],
        },
        "layout_notes": (
            "Two-column or split layout works well — myth vs. reality. "
            "Use the error red sparingly for the 'wrong way' column and "
            "success green for the 'right way'. Logo and trust badges prominent."
        ),
    },
    "subject_spotlight": {
        "mood": "Focused, subject-specific, expert",
        "imagery_style": (
            "Subject-coded colour bands on a navy base — e.g., Biology gets "
            "a green accent, Physics gets blue, Economics amber. "
            "Icon or illustration representing the subject front-and-centre. "
            "Textbook/notebook texture overlays for authenticity."
        ),
        "colour_usage": {
            "dominant": COLOURS["primary"],
            "supporting": COLOURS["secondary"],
            "accent": COLOURS["accent"],
            "background": COLOURS["background_dark"],
        },
        "layout_notes": (
            "Top banner with subject name in Poppins 700. "
            "Central icon/illustration. Pain-point text in Inter 500. "
            "CTA at bottom with amber highlight. Design as a template so "
            "subject name and icon can be swapped per variant."
        ),
    },
    "deadline_urgency": {
        "mood": "Urgent but supportive — not panicked",
        "imagery_style": (
            "Countdown-clock motifs, calendar pages, ticking elements. "
            "Use the error red as a strategic accent for deadline dates — "
            "but keep the overall tone helpful, not anxiety-inducing. "
            "Student-at-desk imagery with warm lighting."
        ),
        "colour_usage": {
            "dominant": COLOURS["error"],
            "supporting": COLOURS["primary"],
            "accent": COLOURS["accent"],
            "background": COLOURS["background"],
        },
        "layout_notes": (
            "Bold date/countdown top-centre. Empathetic hook text below. "
            "CTA button in amber with urgency phrasing. "
            "For Stories: animated countdown sticker style with swipe-up CTA."
        ),
    },
}

_COPY_DIRECTION: dict[str, dict[str, Any]] = {
    "ia_kickstart": {
        "tone": "Encouraging, low-pressure, mentor-like",
        "key_phrases": [
            "Start strong",
            "Your IA, simplified",
            "AI-guided, student-written",
            "From blank page to first draft",
        ],
        "cta": "Get Started Free",
        "headline_variants": [
            "Your IA Doesn't Have to Be Stressful",
            "Blank Page? We'll Fix That.",
            "AI-Powered IA Support — Start Free",
        ],
    },
    "score_boost": {
        "tone": "Confident, data-backed, celebratory",
        "key_phrases": [
            "Average +2 point improvement",
            "Real students, real results",
            "Join 500+ IB students",
            "Your 7 is within reach",
        ],
        "cta": "See How They Did It",
        "headline_variants": [
            "From a 4 to a 7 — Here's How",
            "+2 Points. Average. Real Students.",
            "They Boosted Their IA Score. You Can Too.",
        ],
    },
    "ai_ethics": {
        "tone": "Authoritative, transparent, reassuring",
        "key_phrases": [
            "IB-aligned AI",
            "Guides your thinking, never writes for you",
            "Academic integrity first",
            "The ethical way to use AI",
        ],
        "cta": "Learn Our Approach",
        "headline_variants": [
            "Use AI the IB-Approved Way",
            "AI That Guides — Never Writes For You",
            "Academic Integrity, Built In",
        ],
    },
    "subject_spotlight": {
        "tone": "Empathetic, subject-expert, direct",
        "key_phrases": [
            "Struggling with your {subject} IA?",
            "Expert {subject} tutors",
            "Every IB subject, covered",
            "Tailored to your syllabus",
        ],
        "cta": "Get Expert Help Now",
        "headline_variants": [
            "Struggling With Your {subject} IA?",
            "{subject} IA Help — From IB Experts",
            "Your {subject} IA, Sorted.",
        ],
    },
    "deadline_urgency": {
        "tone": "Urgent but warm, solution-focused",
        "key_phrases": [
            "Deadline approaching",
            "Still time to get it right",
            "Last-minute doesn't mean last-resort",
            "Expert help, fast turnaround",
        ],
        "cta": "Book a Session Today",
        "headline_variants": [
            "IA Deadline Approaching? We've Got You.",
            "Don't Panic — Get Expert IA Help Now",
            "Crunch Time? Let's Get Your IA Done.",
        ],
    },
}

# =============================================================================
# KEY MESSAGES PER THEME
# =============================================================================

_KEY_MESSAGES: dict[str, str] = {
    "ia_kickstart": (
        "Starting your IA is the hardest part. T&N IB Education's AI-powered "
        "platform walks you through topic selection, structure, and analysis — "
        "so you go from a blank page to a confident first draft, ethically."
    ),
    "score_boost": (
        "Students who use T&N IB Education see an average 2-point improvement "
        "on their IA scores. Real tutoring, real AI tools, real results — "
        "backed by data from hundreds of IB students worldwide."
    ),
    "ai_ethics": (
        "AI is transforming education, but not all AI tools are equal. "
        "T&N IB Education's platform guides your thinking without writing "
        "your work — fully aligned with IB academic integrity policies."
    ),
    "subject_spotlight": (
        "Every IB subject has unique IA requirements. T&N IB Education "
        "provides subject-specialist tutors and AI tools calibrated to "
        "your specific syllabus, criteria, and assessment structure."
    ),
    "deadline_urgency": (
        "Your IA deadline is closer than you think. T&N IB Education "
        "offers rapid-turnaround tutoring sessions and AI-assisted "
        "structuring to help you submit confidently — even under pressure."
    ),
}

# =============================================================================
# SUCCESS METRICS (based on paid-advertising benchmarks)
# =============================================================================

_SUCCESS_METRICS: dict[str, dict[str, Any]] = {
    "ia_kickstart": {
        "objective": "Lead Generation",
        "target_ctr": "1.5% - 3.0%",
        "target_cpc": "< $2.00",
        "target_cpl": "< $15.00",
        "target_roas": "3:1+",
        "engagement_rate": "> 3%",
        "landing_page_conversion": "> 8%",
        "kpi_notes": (
            "Optimise toward free-trial sign-ups. Track funnel from "
            "ad click -> sign-up -> first IA session started."
        ),
    },
    "score_boost": {
        "objective": "Conversions (Paid Sign-Ups)",
        "target_ctr": "2.0% - 3.5%",
        "target_cpc": "< $1.50",
        "target_cpl": "< $12.00",
        "target_roas": "4:1+",
        "engagement_rate": "> 4%",
        "landing_page_conversion": "> 10%",
        "kpi_notes": (
            "Social proof drives high intent. Carousel format typically "
            "outperforms single image — track per-card click-through."
        ),
    },
    "ai_ethics": {
        "objective": "Brand Awareness & Trust",
        "target_ctr": "1.0% - 2.0%",
        "target_cpc": "< $3.00",
        "target_cpl": "< $20.00",
        "target_roas": "3:1+",
        "engagement_rate": "> 2.5%",
        "landing_page_conversion": "> 5%",
        "kpi_notes": (
            "Top-of-funnel awareness play targeting parents. "
            "Measure brand lift and time-on-page alongside direct conversions."
        ),
    },
    "subject_spotlight": {
        "objective": "Lead Generation (Subject-Specific)",
        "target_ctr": "1.5% - 2.5%",
        "target_cpc": "< $2.50",
        "target_cpl": "< $18.00",
        "target_roas": "3:1+",
        "engagement_rate": "> 3%",
        "landing_page_conversion": "> 7%",
        "kpi_notes": (
            "Run as dynamic creative with subject-swappable elements. "
            "Compare performance across subjects to find highest-intent niches."
        ),
    },
    "deadline_urgency": {
        "objective": "Conversions (Booked Sessions)",
        "target_ctr": "2.5% - 4.0%",
        "target_cpc": "< $1.00",
        "target_cpl": "< $10.00",
        "target_roas": "5:1+",
        "engagement_rate": "> 5%",
        "landing_page_conversion": "> 12%",
        "kpi_notes": (
            "Highest-intent theme — run 2-3 weeks before known IB deadlines. "
            "Use Meta's 'conversions' objective with a booking-confirmation pixel event."
        ),
    },
}


# =============================================================================
# DATACLASS
# =============================================================================


@dataclass
class CreativeBrief:
    """A complete creative brief for one Facebook/Instagram campaign theme."""

    campaign_theme: dict
    objective: str
    target_audience: dict
    key_message: str
    visual_direction: dict
    copy_direction: dict
    deliverables: list[dict]
    brand_guidelines: dict
    budget_allocation: dict
    success_metrics: dict


# =============================================================================
# BRIEF GENERATION
# =============================================================================


def _build_deliverables(theme: dict) -> list[dict]:
    """Build the deliverables list from the theme's best_for formats."""
    today = date.today()
    deliverables = []
    for i, format_key in enumerate(theme["best_for"]):
        fmt = AD_FORMATS[format_key]
        deadline = today + timedelta(days=14 + i * 3)
        deliverables.append({
            "format_name": fmt["label"],
            "format_key": format_key,
            "dimensions": f"{fmt['width']}x{fmt['height']}",
            "aspect_ratio": fmt["aspect_ratio"],
            "platforms": fmt["platforms"],
            "owner": "TBD — Designer",
            "deadline": deadline.isoformat(),
            "notes": (
                f"Max {int(fmt.get('max_text_ratio', 0.20) * 100)}% text coverage. "
                f"Export as {', '.join(fmt['file_formats']).upper()}. "
                f"Max file size {fmt['max_file_size_mb']} MB."
            ),
        })
    return deliverables


def _build_brand_guidelines() -> dict:
    """Assemble brand guidelines section common to all briefs."""
    return {
        "colours": {
            "primary": f"{COLOURS['primary']} — Deep navy (trust, authority)",
            "secondary": f"{COLOURS['secondary']} — Bright teal (innovation)",
            "accent": f"{COLOURS['accent']} — Warm amber (CTAs, highlights)",
            "background": f"{COLOURS['background']} — Off-white (light mode)",
            "background_dark": f"{COLOURS['background_dark']} — Dark navy (dark mode)",
            "success": f"{COLOURS['success']} — Green (positive metrics)",
            "error": f"{COLOURS['error']} — Red (urgency only)",
        },
        "typography": {
            "headings": f"{FONTS['heading']['family']} {'/'.join(FONTS['heading']['weights'])}",
            "body": f"{FONTS['body']['family']} {'/'.join(FONTS['body']['weights'])}",
            "data_callouts": f"{FONTS['accent']['family']} {'/'.join(FONTS['accent']['weights'])}",
        },
        "logo_placement": (
            "Bottom-right corner within the safe zone. Minimum clear space "
            "equal to the height of the 'T' in the logo mark. On dark backgrounds "
            "use the white/reversed logo variant."
        ),
        "voice": BRAND["voice"],
    }


def generate_brief(theme_id: str, audience: str = "primary") -> CreativeBrief:
    """
    Generate a complete creative brief for a given campaign theme.

    Args:
        theme_id: One of the theme IDs defined in CAMPAIGN_THEMES
                  (e.g., "ia_kickstart", "score_boost").
        audience: Target audience segment key — "primary", "secondary",
                  or "tertiary".

    Returns:
        A fully populated CreativeBrief dataclass instance.

    Raises:
        ValueError: If theme_id is not found in CAMPAIGN_THEMES.
    """
    # Look up the theme dict
    theme = None
    for t in CAMPAIGN_THEMES:
        if t["id"] == theme_id:
            theme = t
            break
    if theme is None:
        valid = [t["id"] for t in CAMPAIGN_THEMES]
        raise ValueError(
            f"Unknown theme_id '{theme_id}'. Valid IDs: {valid}"
        )

    audience_data = TARGET_AUDIENCE.get(audience, TARGET_AUDIENCE["primary"])
    metrics = _SUCCESS_METRICS.get(theme_id, _SUCCESS_METRICS["ia_kickstart"])

    return CreativeBrief(
        campaign_theme=theme,
        objective=metrics["objective"],
        target_audience=audience_data,
        key_message=_KEY_MESSAGES[theme_id],
        visual_direction=_VISUAL_DIRECTION[theme_id],
        copy_direction=_COPY_DIRECTION[theme_id],
        deliverables=_build_deliverables(theme),
        brand_guidelines=_build_brand_guidelines(),
        budget_allocation={
            "proven": BUDGET_STRATEGY["proven"],
            "testing": BUDGET_STRATEGY["testing"],
            "experimental": BUDGET_STRATEGY["experimental"],
            "target_roas": BUDGET_STRATEGY["target_roas"],
            "optimisation_cadence": BUDGET_STRATEGY["optimisation_cadence"],
            "creative_variations": BUDGET_STRATEGY["creative_variations_per_campaign"],
        },
        success_metrics=metrics,
    )


# =============================================================================
# MARKDOWN EXPORT
# =============================================================================


def export_brief_markdown(brief: CreativeBrief) -> str:
    """
    Format a CreativeBrief as a clean, designer-ready markdown document.

    Follows the campaign brief structure:
    Campaign Overview -> Target Audience -> Messaging -> Deliverables ->
    Brand Guidelines -> Budget -> Success Metrics.
    """
    theme = brief.campaign_theme
    lines: list[str] = []

    def heading(level: int, text: str) -> None:
        lines.append(f"\n{'#' * level} {text}\n")

    def kv(label: str, value: str) -> None:
        lines.append(f"- **{label}:** {value}")

    # --- Title ---
    lines.append(f"# Creative Brief — {theme['name']}")
    lines.append("")
    lines.append(f"*{BRAND['company_name']}  ·  {BRAND['website']}*")
    lines.append(f"*Generated: {date.today().isoformat()}*")

    # --- Campaign Overview ---
    heading(2, "Campaign Overview")
    kv("Theme", theme["name"])
    kv("Theme ID", f"`{theme['id']}`")
    kv("Hook", f"*\"{theme['hook']}\"*")
    kv("Angle", theme["angle"])
    kv("Objective", brief.objective)
    kv("CTA", theme["cta"])

    heading(3, "Key Message")
    lines.append(f"> {brief.key_message}")

    # --- Target Audience ---
    heading(2, "Target Audience")
    aud = brief.target_audience
    kv("Segment", aud.get("label", "N/A"))
    kv("Age Range", aud.get("age_range", "N/A"))
    kv("Description", aud.get("description", "N/A"))

    if "pain_points" in aud:
        lines.append("")
        lines.append("**Pain Points Addressed:**")
        for pp in aud["pain_points"]:
            lines.append(f"  - {pp}")

    if "facebook_targeting" in aud:
        ft = aud["facebook_targeting"]
        lines.append("")
        lines.append("**Facebook/Instagram Targeting:**")
        lines.append(f"  - Interests: {', '.join(ft.get('interests', []))}")
        lines.append(f"  - Behaviors: {', '.join(ft.get('behaviors', []))}")

    # --- Messaging & Copy Direction ---
    heading(2, "Messaging & Copy Direction")
    copy = brief.copy_direction
    kv("Tone", copy["tone"])
    kv("Primary CTA", copy["cta"])

    lines.append("")
    lines.append("**Key Phrases:**")
    for phrase in copy["key_phrases"]:
        lines.append(f"  - {phrase}")

    lines.append("")
    lines.append("**Headline Variants (test all):**")
    for i, hl in enumerate(copy["headline_variants"], 1):
        lines.append(f"  {i}. {hl}")

    # --- Visual Direction ---
    heading(2, "Visual Direction")
    vis = brief.visual_direction
    kv("Mood", vis["mood"])
    lines.append("")
    lines.append("**Imagery Style:**")
    lines.append(f"  {vis['imagery_style']}")
    lines.append("")
    lines.append("**Colour Usage:**")
    for role, hex_val in vis["colour_usage"].items():
        lines.append(f"  - {role.replace('_', ' ').title()}: `{hex_val}`")
    lines.append("")
    lines.append("**Layout Notes:**")
    lines.append(f"  {vis['layout_notes']}")

    # --- Deliverables ---
    heading(2, "Deliverables")
    lines.append(
        "| # | Format | Dimensions | Aspect Ratio | Platforms | Owner | Deadline |"
    )
    lines.append(
        "|---|--------|------------|--------------|-----------|-------|----------|"
    )
    for i, d in enumerate(brief.deliverables, 1):
        platforms = ", ".join(d["platforms"])
        lines.append(
            f"| {i} | {d['format_name']} | {d['dimensions']} | "
            f"{d['aspect_ratio']} | {platforms} | {d['owner']} | {d['deadline']} |"
        )

    lines.append("")
    lines.append("**Production Notes:**")
    for d in brief.deliverables:
        lines.append(f"- *{d['format_name']}:* {d['notes']}")

    # --- Brand Guidelines ---
    heading(2, "Brand Guidelines")

    lines.append("**Colour Palette:**")
    for role, desc in brief.brand_guidelines["colours"].items():
        lines.append(f"  - {role.replace('_', ' ').title()}: {desc}")

    lines.append("")
    lines.append("**Typography:**")
    for role, spec in brief.brand_guidelines["typography"].items():
        lines.append(f"  - {role.replace('_', ' ').title()}: {spec}")

    lines.append("")
    lines.append("**Logo Placement:**")
    lines.append(f"  {brief.brand_guidelines['logo_placement']}")

    lines.append("")
    lines.append("**Brand Voice:**")
    voice = brief.brand_guidelines["voice"]
    lines.append(f"  - Tone: {voice['tone']}")
    lines.append(f"  - Formality: {voice['formality']}")
    lines.append(f"  - Personality: {', '.join(voice['personality'])}")

    # --- Budget Allocation ---
    heading(2, "Budget Allocation")
    ba = brief.budget_allocation
    lines.append(
        f"| Tier | Allocation | Description |"
    )
    lines.append(
        f"|------|-----------|-------------|"
    )
    for tier in ("proven", "testing", "experimental"):
        info = ba[tier]
        pct = int(info["allocation"] * 100)
        lines.append(f"| {tier.title()} | {pct}% | {info['description']} |")

    lines.append("")
    kv("Target ROAS", f"{ba['target_roas']}:1")
    kv("Optimisation Cadence", ba["optimisation_cadence"].title())
    kv("Creative Variations to Test", str(ba["creative_variations"]))

    # --- Success Metrics ---
    heading(2, "Success Metrics")
    sm = brief.success_metrics
    kv("Campaign Objective", sm["objective"])
    kv("Target CTR", sm["target_ctr"])
    kv("Target CPC", sm["target_cpc"])
    kv("Target CPL", sm["target_cpl"])
    kv("Target ROAS", sm["target_roas"])
    kv("Engagement Rate", sm["engagement_rate"])
    kv("Landing Page Conversion", sm["landing_page_conversion"])

    lines.append("")
    lines.append("**KPI Notes:**")
    lines.append(f"  {sm['kpi_notes']}")

    # --- Footer ---
    lines.append("")
    lines.append("---")
    lines.append(
        f"*Brief generated for {BRAND['company_name']} — {BRAND['tagline']}*"
    )

    return "\n".join(lines) + "\n"


# =============================================================================
# BATCH GENERATION
# =============================================================================


def generate_all_briefs() -> list[CreativeBrief]:
    """Generate creative briefs for every campaign theme in CAMPAIGN_THEMES."""
    return [generate_brief(theme["id"]) for theme in CAMPAIGN_THEMES]


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "briefs")
    os.makedirs(output_dir, exist_ok=True)

    # Allow generating a single brief by theme ID via CLI argument
    if len(sys.argv) > 1:
        theme_ids = sys.argv[1:]
    else:
        theme_ids = [t["id"] for t in CAMPAIGN_THEMES]

    briefs_generated = []
    for tid in theme_ids:
        try:
            brief = generate_brief(tid)
        except ValueError as exc:
            print(f"SKIP: {exc}")
            continue

        md = export_brief_markdown(brief)
        filename = f"brief_{tid}.md"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write(md)

        briefs_generated.append(filepath)
        print(f"  -> {filepath}")

    print(f"\nDone. {len(briefs_generated)} brief(s) saved to {output_dir}/")
