"""
Campaign Calendar for T&N IB Education - Facebook Marketing Campaign
====================================================================
Maps campaign phases to the IB academic calendar for the 2026-2027 cycle.
Aligns ad spend, themes, and audience targeting with key IB assessment
deadlines so that ads reach students when urgency is highest.

Covers April 2026 through March 2027.
"""

from __future__ import annotations

import datetime
from typing import Optional

from brand_constants import BUDGET_STRATEGY, CAMPAIGN_THEMES, TARGET_AUDIENCE

# =============================================================================
# IB ACADEMIC CALENDAR — 2026 CYCLE
# =============================================================================
# Dates reflect typical IB school timelines. Individual schools vary, but
# these windows capture the bulk of the global IB cohort.

IB_ACADEMIC_CALENDAR = {
    # --- Internal Assessment milestones ---
    "ia_draft_deadline_early": {
        "label": "IA Draft Deadline (early schools)",
        "date": datetime.date(2026, 10, 15),
        "note": "Some schools require first drafts as early as mid-October of Year 2.",
    },
    "ia_draft_deadline_mid": {
        "label": "IA Draft Deadline (majority of schools)",
        "date": datetime.date(2026, 12, 1),
        "note": "Most schools set draft deadlines in November-December.",
    },
    "ia_draft_deadline_late": {
        "label": "IA Draft Deadline (late schools)",
        "date": datetime.date(2027, 1, 15),
        "note": "A minority of schools allow drafts into January.",
    },
    "ia_final_submission_early": {
        "label": "IA Final Submission (early schools)",
        "date": datetime.date(2027, 1, 20),
        "note": "Early-submitting schools close IAs in late January.",
    },
    "ia_final_submission_mid": {
        "label": "IA Final Submission (majority of schools)",
        "date": datetime.date(2027, 2, 15),
        "note": "The largest cluster of final IA deadlines falls in February.",
    },
    "ia_final_submission_late": {
        "label": "IA Final Submission (IB upload deadline)",
        "date": datetime.date(2027, 3, 15),
        "note": "Absolute IB upload deadline for May-session coursework.",
    },
    # --- Extended Essay ---
    "extended_essay_draft": {
        "label": "Extended Essay Draft Deadline (typical)",
        "date": datetime.date(2026, 11, 15),
        "note": "Many schools require a near-final EE draft by mid-November.",
    },
    "extended_essay_final": {
        "label": "Extended Essay Final Submission",
        "date": datetime.date(2027, 3, 1),
        "note": "Final EE submission to the IB, usually early March.",
    },
    # --- Exam sessions ---
    "may_exam_session_start": {
        "label": "May Examination Session Begins",
        "date": datetime.date(2026, 4, 28),
        "note": "Written exams run late April through late May.",
    },
    "may_exam_session_end": {
        "label": "May Examination Session Ends",
        "date": datetime.date(2026, 5, 22),
        "note": "Final papers typically wrap up in the third week of May.",
    },
    "november_exam_session_start": {
        "label": "November Examination Session Begins",
        "date": datetime.date(2026, 10, 26),
        "note": "November session (southern hemisphere schools).",
    },
    "november_exam_session_end": {
        "label": "November Examination Session Ends",
        "date": datetime.date(2026, 11, 20),
        "note": "November session concludes mid-to-late November.",
    },
    # --- Results ---
    "may_results_day": {
        "label": "May Session Results Day",
        "date": datetime.date(2026, 7, 6),
        "note": "Results released to schools and students on July 6.",
    },
    "november_results_day": {
        "label": "November Session Results Day",
        "date": datetime.date(2027, 1, 5),
        "note": "November session results typically released early January.",
    },
    # --- School calendar ---
    "back_to_school_northern": {
        "label": "Back to School — Northern Hemisphere",
        "date": datetime.date(2026, 8, 24),
        "note": "Year 2 IB students return and begin serious IA work.",
    },
    "back_to_school_southern": {
        "label": "Back to School — Southern Hemisphere",
        "date": datetime.date(2027, 2, 1),
        "note": "Southern hemisphere IB schools start in late Jan / early Feb.",
    },
}


# =============================================================================
# THEME LOOKUP HELPER
# =============================================================================

_THEME_INDEX: dict[str, dict] = {t["id"]: t for t in CAMPAIGN_THEMES}


def _theme_ids(*ids: str) -> list[str]:
    """Validate theme IDs exist and return them as a list."""
    for tid in ids:
        if tid not in _THEME_INDEX:
            raise ValueError(f"Unknown theme ID: {tid!r}")
    return list(ids)


# =============================================================================
# CAMPAIGN PHASES — April 2026 through March 2027
# =============================================================================

CAMPAIGN_PHASES: list[dict] = [
    # ---- Always-on baseline ------------------------------------------------
    {
        "phase_name": "Year-Round Always-On",
        "start_date": datetime.date(2026, 4, 1),
        "end_date": datetime.date(2027, 3, 31),
        "campaign_themes": _theme_ids("ai_ethics", "score_boost"),
        "target_audiences": ["primary", "secondary"],
        "budget_multiplier": 0.5,
        "objective": "awareness",
        "notes": (
            "Continuous low-budget brand awareness layer. Runs beneath every "
            "seasonal phase so T&N stays visible even outside peak periods. "
            "Uses the AI Done Right and Score Boost themes for evergreen relevance."
        ),
    },
    # ---- Pre-Exam Revision (Apr 2026) --------------------------------------
    {
        "phase_name": "Pre-Exam Revision",
        "start_date": datetime.date(2026, 4, 1),
        "end_date": datetime.date(2026, 4, 27),
        "campaign_themes": _theme_ids("score_boost"),
        "target_audiences": ["primary"],
        "budget_multiplier": 1.3,
        "objective": "conversion",
        "notes": (
            "Final push before May exams begin. Focus on exam-prep tutoring "
            "packages and last-minute IA revision for late-submitting students. "
            "Score Boost theme with urgency messaging."
        ),
    },
    # ---- May Exam Season (May 2026) ----------------------------------------
    {
        "phase_name": "May Exam Season",
        "start_date": datetime.date(2026, 4, 28),
        "end_date": datetime.date(2026, 5, 31),
        "campaign_themes": _theme_ids("ai_ethics"),
        "target_audiences": ["secondary", "tertiary"],
        "budget_multiplier": 0.6,
        "objective": "awareness",
        "notes": (
            "Students are sitting exams — lower direct-response spend. "
            "Shift to parent-focused brand building with the AI Done Right "
            "angle, positioning T&N for the next cohort. Light retargeting "
            "of Year 1 IB students who will need IA help next year."
        ),
    },
    # ---- Summer Nurture (Jun-Jul 2026) -------------------------------------
    {
        "phase_name": "Summer Nurture",
        "start_date": datetime.date(2026, 6, 1),
        "end_date": datetime.date(2026, 7, 5),
        "campaign_themes": _theme_ids("ai_ethics", "subject_spotlight"),
        "target_audiences": ["primary", "secondary"],
        "budget_multiplier": 0.5,
        "objective": "awareness",
        "notes": (
            "Low-spend content and brand-building phase. Share blog posts, "
            "subject guides, and 'how to prepare for Year 2' content. "
            "Warm up audiences ahead of results day and back-to-school."
        ),
    },
    # ---- Results & Testimonials (Jul 2026) ---------------------------------
    {
        "phase_name": "Results & Testimonials",
        "start_date": datetime.date(2026, 7, 6),
        "end_date": datetime.date(2026, 7, 31),
        "campaign_themes": _theme_ids("score_boost"),
        "target_audiences": ["primary", "secondary"],
        "budget_multiplier": 1.0,
        "objective": "awareness",
        "notes": (
            "Leverage results day excitement. Feature real student "
            "testimonials and score improvements from the May session. "
            "Carousel ads showing before/after scores. Build social proof "
            "for the incoming Year 2 cohort."
        ),
    },
    # ---- Back to School (Aug-Sep 2026) -------------------------------------
    {
        "phase_name": "Back to School",
        "start_date": datetime.date(2026, 8, 1),
        "end_date": datetime.date(2026, 9, 30),
        "campaign_themes": _theme_ids("ia_kickstart"),
        "target_audiences": ["primary", "secondary"],
        "budget_multiplier": 1.2,
        "objective": "awareness",
        "notes": (
            "Year 2 IB students return and face the reality of IAs. "
            "Awareness-focused IA Kickstart campaign positions T&N as the "
            "go-to platform before students have committed elsewhere. "
            "Strong parent targeting as they look for academic support."
        ),
    },
    # ---- IA Topic Selection (Sep-Oct 2026) ---------------------------------
    {
        "phase_name": "IA Topic Selection",
        "start_date": datetime.date(2026, 9, 15),
        "end_date": datetime.date(2026, 10, 31),
        "campaign_themes": _theme_ids("subject_spotlight", "ia_kickstart"),
        "target_audiences": ["primary"],
        "budget_multiplier": 1.3,
        "objective": "consideration",
        "notes": (
            "Students are choosing IA topics and starting research. "
            "Subject Spotlight ads target by subject interest (Maths, "
            "Sciences, Economics, etc.) while IA Kickstart shows the "
            "AI-assisted workflow. Drive sign-ups for free consultations."
        ),
    },
    # ---- IA Draft Support (Nov-Dec 2026) -----------------------------------
    {
        "phase_name": "IA Draft Support",
        "start_date": datetime.date(2026, 11, 1),
        "end_date": datetime.date(2026, 12, 31),
        "campaign_themes": _theme_ids("ia_kickstart", "score_boost"),
        "target_audiences": ["primary", "secondary"],
        "budget_multiplier": 1.5,
        "objective": "conversion",
        "notes": (
            "Peak conversion phase. Most schools have draft deadlines in "
            "Nov-Dec, driving high urgency. IA Kickstart for students still "
            "writing, Score Boost for those refining drafts. Ramp budget to "
            "capture the highest-intent traffic of the year. Combine with "
            "deadline countdown creatives and Extended Essay support."
        ),
    },
    # ---- IA Final Push (Jan-Feb 2027) --------------------------------------
    {
        "phase_name": "IA Final Push",
        "start_date": datetime.date(2027, 1, 1),
        "end_date": datetime.date(2027, 2, 28),
        "campaign_themes": _theme_ids("deadline_urgency", "score_boost"),
        "target_audiences": ["primary", "secondary"],
        "budget_multiplier": 1.8,
        "objective": "conversion",
        "notes": (
            "Highest budget multiplier of the year. Final IA submission "
            "deadlines cluster in Jan-Feb. Deadline Crunch theme drives "
            "urgency; Score Boost reinforces the outcome. Heavy retargeting "
            "of warm audiences from earlier phases. Extended Essay final "
            "submissions also fall in this window."
        ),
    },
    # ---- Pre-Exam Revision (Mar 2027) --------------------------------------
    {
        "phase_name": "Pre-Exam Revision (2027)",
        "start_date": datetime.date(2027, 3, 1),
        "end_date": datetime.date(2027, 3, 31),
        "campaign_themes": _theme_ids("score_boost"),
        "target_audiences": ["primary"],
        "budget_multiplier": 1.2,
        "objective": "conversion",
        "notes": (
            "IAs are submitted; students pivot to exam revision. "
            "Promote tutoring sessions and revision packages. "
            "Score Boost testimonials anchor the messaging."
        ),
    },
]


# =============================================================================
# FUNCTIONS
# =============================================================================


def get_active_campaigns(
    date: Optional[datetime.date] = None,
) -> list[dict]:
    """Return all campaign phases that are active on the given date.

    Parameters
    ----------
    date : datetime.date or None
        The date to check. Defaults to today.

    Returns
    -------
    list[dict]
        A list of phase dicts whose date range includes *date*.
    """
    if date is None:
        date = datetime.date.today()
    return [
        phase
        for phase in CAMPAIGN_PHASES
        if phase["start_date"] <= date <= phase["end_date"]
    ]


def get_monthly_budget_plan(
    monthly_budget: float = 1500.0,
) -> list[dict]:
    """Build a month-by-month budget allocation for the full campaign year.

    The base *monthly_budget* is scaled by the highest ``budget_multiplier``
    among all phases active during that month. Where multiple seasonal phases
    overlap, the highest multiplier wins (the always-on layer is already
    accounted for in creative scheduling, not in the multiplier stack).

    The 70-20-10 split from :pydata:`BUDGET_STRATEGY` is applied within
    each month.

    Parameters
    ----------
    monthly_budget : float
        Base monthly ad spend before multipliers are applied. Default $1 500.

    Returns
    -------
    list[dict]
        One entry per month from April 2026 to March 2027.
    """
    plan: list[dict] = []
    start = datetime.date(2026, 4, 1)

    for month_offset in range(12):
        year = start.year + (start.month + month_offset - 1) // 12
        month = (start.month + month_offset - 1) % 12 + 1
        first_of_month = datetime.date(year, month, 1)

        # Find the last day of the month.
        if month == 12:
            last_of_month = datetime.date(year, 12, 31)
        else:
            last_of_month = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

        mid_month = datetime.date(year, month, 15)

        # Collect active phases for this month (check first, mid, and last day).
        active_phases: list[dict] = []
        seen_names: set[str] = set()
        for check_date in (first_of_month, mid_month, last_of_month):
            for phase in get_active_campaigns(check_date):
                if phase["phase_name"] not in seen_names:
                    seen_names.add(phase["phase_name"])
                    active_phases.append(phase)

        # Use the highest seasonal multiplier (exclude always-on for the
        # multiplier calc — it runs at its own low baseline).
        seasonal = [
            p for p in active_phases if p["phase_name"] != "Year-Round Always-On"
        ]
        if seasonal:
            effective_multiplier = max(p["budget_multiplier"] for p in seasonal)
        else:
            # Only always-on is running.
            effective_multiplier = 0.5

        total = round(monthly_budget * effective_multiplier, 2)

        plan.append(
            {
                "month": first_of_month.strftime("%B %Y"),
                "month_date": first_of_month,
                "active_phases": [p["phase_name"] for p in active_phases],
                "effective_multiplier": effective_multiplier,
                "total_budget": total,
                "proven_budget": round(
                    total * BUDGET_STRATEGY["proven"]["allocation"], 2
                ),
                "testing_budget": round(
                    total * BUDGET_STRATEGY["testing"]["allocation"], 2
                ),
                "experimental_budget": round(
                    total * BUDGET_STRATEGY["experimental"]["allocation"], 2
                ),
            }
        )

    return plan


def export_calendar_markdown() -> str:
    """Generate a readable Markdown overview of the full campaign calendar.

    Returns
    -------
    str
        Markdown-formatted text with IB dates, phases, and budget plan.
    """
    lines: list[str] = []

    # --- Header ---
    lines.append("# T&N IB Education — Facebook Campaign Calendar 2026-2027")
    lines.append("")
    lines.append(
        "Campaign plan aligned to IB assessment deadlines for "
        "[tandnibeducation.com](https://tandnibeducation.com)."
    )
    lines.append("")

    # --- IB Academic Calendar ---
    lines.append("## IB Academic Calendar — Key Dates")
    lines.append("")
    lines.append("| Milestone | Date | Notes |")
    lines.append("|---|---|---|")
    for key, entry in IB_ACADEMIC_CALENDAR.items():
        lines.append(
            f"| {entry['label']} | {entry['date'].strftime('%d %b %Y')} | {entry['note']} |"
        )
    lines.append("")

    # --- Campaign Phases ---
    lines.append("## Campaign Phases")
    lines.append("")
    for phase in CAMPAIGN_PHASES:
        lines.append(f"### {phase['phase_name']}")
        lines.append("")
        lines.append(
            f"**Dates:** {phase['start_date'].strftime('%d %b %Y')} "
            f"— {phase['end_date'].strftime('%d %b %Y')}"
        )
        lines.append(f"  ")
        lines.append(f"**Objective:** {phase['objective'].title()}")
        lines.append(f"  ")
        lines.append(f"**Budget multiplier:** {phase['budget_multiplier']}x")
        lines.append(f"  ")
        theme_names = [
            _THEME_INDEX[tid]["name"] for tid in phase["campaign_themes"]
        ]
        lines.append(f"**Themes:** {', '.join(theme_names)}")
        lines.append(f"  ")
        audience_labels = [
            TARGET_AUDIENCE[seg]["label"]
            for seg in phase["target_audiences"]
            if seg in TARGET_AUDIENCE and "label" in TARGET_AUDIENCE[seg]
        ]
        lines.append(f"**Audiences:** {', '.join(audience_labels)}")
        lines.append("")
        lines.append(f"> {phase['notes']}")
        lines.append("")

    # --- Monthly Budget Plan ---
    lines.append("## Monthly Budget Plan")
    lines.append("")
    lines.append(
        "Based on a $1,500/month baseline, split using the "
        "70-20-10 rule (proven / testing / experimental)."
    )
    lines.append("")
    lines.append(
        "| Month | Multiplier | Total | Proven (70%) | Testing (20%) "
        "| Experimental (10%) | Active Phases |"
    )
    lines.append("|---|---|---|---|---|---|---|")

    budget_plan = get_monthly_budget_plan(1500.0)
    annual_total = 0.0
    for entry in budget_plan:
        annual_total += entry["total_budget"]
        phases_str = ", ".join(
            p for p in entry["active_phases"] if p != "Year-Round Always-On"
        ) or "Always-On only"
        lines.append(
            f"| {entry['month']} | {entry['effective_multiplier']}x "
            f"| ${entry['total_budget']:,.2f} "
            f"| ${entry['proven_budget']:,.2f} "
            f"| ${entry['testing_budget']:,.2f} "
            f"| ${entry['experimental_budget']:,.2f} "
            f"| {phases_str} |"
        )

    lines.append("")
    lines.append(f"**Annual total:** ${annual_total:,.2f}")
    lines.append("")

    return "\n".join(lines)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    today = datetime.date.today()
    print(f"Today: {today.strftime('%A, %d %B %Y')}")
    print()

    # Active campaigns
    active = get_active_campaigns(today)
    if active:
        print(f"=== Active Campaigns ({len(active)}) ===")
        for phase in active:
            theme_names = [
                _THEME_INDEX[tid]["name"] for tid in phase["campaign_themes"]
            ]
            print(f"  - {phase['phase_name']}")
            print(f"    Dates: {phase['start_date']} to {phase['end_date']}")
            print(f"    Objective: {phase['objective']}")
            print(f"    Themes: {', '.join(theme_names)}")
            print(f"    Budget multiplier: {phase['budget_multiplier']}x")
            print()
    else:
        print("No seasonal campaigns active today (always-on may still run).")
        print()

    # Full calendar
    print("=== Full Campaign Calendar (Markdown) ===")
    print()
    print(export_calendar_markdown())
