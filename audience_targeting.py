"""
Audience Targeting Configurations for T&N IB Education — Meta Ads
=================================================================
Defines funnel-stage audiences (TOFU/MOFU/BOFU), detailed targeting
segments, and helper functions for campaign planning.

Designed for use with Meta Ads Manager. All interest keywords, behavior
categories, and custom audience descriptions follow Meta's targeting
taxonomy and paid-advertising best practices.
"""

from brand_constants import TARGET_AUDIENCE, CAMPAIGN_THEMES, IB_SUBJECTS


# =============================================================================
# FUNNEL STAGE DEFINITIONS
# =============================================================================

FUNNEL_STAGES = {
    "TOFU": {
        "label": "Top of Funnel — Awareness",
        "objective": "Reach new audiences who have never interacted with the brand",
        "meta_objectives": ["Awareness", "Traffic", "Video Views"],
        "budget_weight": 0.50,
        "description": (
            "Broad interest targeting, lookalike audiences, and video view "
            "campaigns designed to introduce T&N IB Education to cold audiences."
        ),
    },
    "MOFU": {
        "label": "Middle of Funnel — Consideration",
        "objective": "Re-engage warm audiences who have shown initial interest",
        "meta_objectives": ["Traffic", "Engagement", "Lead Generation"],
        "budget_weight": 0.30,
        "description": (
            "Retarget website visitors, social engagers, and email subscribers "
            "with content that builds trust and demonstrates expertise."
        ),
    },
    "BOFU": {
        "label": "Bottom of Funnel — Conversion",
        "objective": "Convert high-intent prospects into paying customers",
        "meta_objectives": ["Conversions", "Sales"],
        "budget_weight": 0.20,
        "description": (
            "Target users who visited pricing or booking pages, started a form, "
            "or otherwise demonstrated strong purchase intent."
        ),
    },
}


# =============================================================================
# KEY IB MARKETS — Countries with significant IB school populations
# =============================================================================

IB_CORE_MARKETS = [
    "GB",  # United Kingdom
    "AE",  # United Arab Emirates
    "SG",  # Singapore
    "HK",  # Hong Kong
    "IN",  # India
    "US",  # United States
    "CA",  # Canada
    "AU",  # Australia
    "NL",  # Netherlands
    "DE",  # Germany
    "CH",  # Switzerland
    "MY",  # Malaysia
    "TH",  # Thailand
]

IB_TIER_2_MARKETS = [
    "ES",  # Spain
    "MX",  # Mexico
    "JP",  # Japan
    "KR",  # South Korea
    "EG",  # Egypt
    "KE",  # Kenya
    "QA",  # Qatar
    "BH",  # Bahrain
]


# =============================================================================
# SHARED EXCLUSION LISTS
# =============================================================================

_STANDARD_EXCLUSIONS = [
    "Existing customers (purchase event, last 180 days)",
    "Current active subscribers",
]

_RETARGETING_EXCLUSIONS = [
    "Existing customers (purchase event, last 180 days)",
    "Users who already booked a session (last 30 days)",
]


# =============================================================================
# AUDIENCE SEGMENTS
# =============================================================================

def _build_subject_interests() -> list[str]:
    """Flatten IB_SUBJECTS into Meta-compatible interest keywords."""
    interests = []
    for group, subjects in IB_SUBJECTS.items():
        for subject in subjects:
            interests.append(f"IB {subject}")
            # Add the plain subject name for broader reach
            plain = subject.replace("AA", "").replace("AI", "").strip()
            if plain and plain not in interests:
                interests.append(plain)
    return interests


AUDIENCE_SEGMENTS = [
    # ------------------------------------------------------------------
    # TOFU — Broad IB Student Interest
    # ------------------------------------------------------------------
    {
        "id": "ib_students_broad",
        "name": "IB Students — Broad Interest",
        "funnel_stage": "TOFU",
        "description": (
            "Cold audience of users aged 15-19 with interests in the "
            "International Baccalaureate, study tips, and academic success. "
            "Sourced from Meta interest targeting."
        ),
        "age_min": 15,
        "age_max": 19,
        "genders": ["All"],
        "interests": [
            "International Baccalaureate",
            "IB Diploma Programme",
            "Study tips",
            "Academic success",
            "IB exams",
            "IB revision",
            "Internal Assessment",
            "Extended Essay",
            "Online tutoring",
            "Exam preparation",
        ],
        "behaviors": [
            "Digital activities: Education-related searches",
            "Digital activities: Online learning platforms",
            "Technology early adopters",
        ],
        "exclusions": _STANDARD_EXCLUSIONS + [
            "Website visitors (last 30 days)",
        ],
        "locations": IB_CORE_MARKETS,
        "languages": ["English (All)"],
        "custom_audiences": [],
        "lookalike_source": None,
        "lookalike_percentage": None,
        "estimated_reach": "500K-1.5M",
        "recommended_daily_budget_usd": 15.0,
    },

    # ------------------------------------------------------------------
    # TOFU — Subject-Specific Targeting
    # ------------------------------------------------------------------
    {
        "id": "ib_students_subject",
        "name": "IB Students — Subject-Specific",
        "funnel_stage": "TOFU",
        "description": (
            "Cold audience segmented by individual IB subjects. Best used "
            "with the 'subject_spotlight' campaign theme and dynamic creative "
            "that swaps subject names in headlines."
        ),
        "age_min": 15,
        "age_max": 19,
        "genders": ["All"],
        "interests": _build_subject_interests(),
        "behaviors": [
            "Digital activities: Education-related searches",
            "Digital activities: Online learning platforms",
        ],
        "exclusions": _STANDARD_EXCLUSIONS + [
            "Website visitors (last 30 days)",
        ],
        "locations": IB_CORE_MARKETS,
        "languages": ["English (All)"],
        "custom_audiences": [],
        "lookalike_source": None,
        "lookalike_percentage": None,
        "estimated_reach": "200K-800K per subject group",
        "recommended_daily_budget_usd": 12.0,
        "notes": (
            "Create separate ad sets per IB subject group (1-6 + core) "
            "for granular performance reporting. Use dynamic creative "
            "to insert subject name into ad copy."
        ),
    },

    # ------------------------------------------------------------------
    # TOFU — Parents of IB Students
    # ------------------------------------------------------------------
    {
        "id": "ib_parents_broad",
        "name": "Parents of IB Students — Broad",
        "funnel_stage": "TOFU",
        "description": (
            "Parents aged 35-55 interested in education, international "
            "schools, and academic support. Higher disposable income "
            "segment likely to make purchasing decisions."
        ),
        "age_min": 35,
        "age_max": 55,
        "genders": ["All"],
        "interests": [
            "International Baccalaureate",
            "International schools",
            "Education",
            "Parenting teenagers",
            "University admissions",
            "College preparation",
            "Private tutoring",
            "Academic tutoring",
            "Gifted education",
            "UCAS",
            "Common Application",
        ],
        "behaviors": [
            "Parents with teenagers (13-18)",
            "Engaged shoppers",
            "Frequent travellers (international schools correlation)",
            "Digital activities: Education spenders",
        ],
        "exclusions": _STANDARD_EXCLUSIONS,
        "locations": IB_CORE_MARKETS,
        "languages": ["English (All)"],
        "custom_audiences": [],
        "lookalike_source": None,
        "lookalike_percentage": None,
        "estimated_reach": "1M-3M",
        "recommended_daily_budget_usd": 15.0,
    },

    # ------------------------------------------------------------------
    # TOFU — Lookalike of Past Converters
    # ------------------------------------------------------------------
    {
        "id": "lookalike_converters",
        "name": "Lookalike — Past Converters (1-3%)",
        "funnel_stage": "TOFU",
        "description": (
            "Lookalike audience built from the seed of all users who "
            "completed a purchase or booking in the last 180 days. "
            "Meta finds statistically similar users in the target countries."
        ),
        "age_min": 15,
        "age_max": 55,
        "genders": ["All"],
        "interests": [],
        "behaviors": [],
        "exclusions": _STANDARD_EXCLUSIONS + [
            "Website visitors (last 30 days)",
            "Source seed audience (past converters)",
        ],
        "locations": IB_CORE_MARKETS,
        "languages": ["English (All)"],
        "custom_audiences": [
            "Seed: All users with Purchase or CompleteRegistration event (180 days)",
        ],
        "lookalike_source": "purchase_and_registration_180d",
        "lookalike_percentage": 3,
        "estimated_reach": "2M-6M (varies by country)",
        "recommended_daily_budget_usd": 12.0,
        "notes": (
            "Start with 1% lookalike for best quality. Scale to 2-3% "
            "once 1% audience is saturated (frequency > 2.5). "
            "Requires minimum 100 seed events for reliable modelling."
        ),
    },

    # ------------------------------------------------------------------
    # TOFU — Exam Season Surge
    # ------------------------------------------------------------------
    {
        "id": "exam_season_surge",
        "name": "Exam Season Surge — Broad Reach",
        "funnel_stage": "TOFU",
        "description": (
            "Broader targeting activated during IB assessment deadlines "
            "(IA submission windows in Jan-Mar, final exams in May). "
            "Relaxed interest constraints to maximise reach during "
            "peak-intent periods."
        ),
        "age_min": 14,
        "age_max": 20,
        "genders": ["All"],
        "interests": [
            "International Baccalaureate",
            "IB exams",
            "Exam preparation",
            "Study motivation",
            "Tutoring",
            "Student life",
            "Academic stress",
            "Revision techniques",
            "Online tutoring",
            "Study planner",
        ],
        "behaviors": [
            "Digital activities: Education-related searches",
            "Digital activities: Increased mobile usage",
        ],
        "exclusions": [
            "Existing customers (purchase event, last 180 days)",
        ],
        "locations": IB_CORE_MARKETS + IB_TIER_2_MARKETS,
        "languages": ["English (All)"],
        "custom_audiences": [],
        "lookalike_source": None,
        "lookalike_percentage": None,
        "estimated_reach": "1M-4M",
        "recommended_daily_budget_usd": 20.0,
        "activation_windows": [
            {"label": "IA Submission Window", "months": [1, 2, 3]},
            {"label": "Final Exam Prep", "months": [4, 5]},
            {"label": "Results & Re-enrolment", "months": [7, 8]},
        ],
        "notes": (
            "Only activate during defined windows. Increase daily budget "
            "by 50-100% during peak weeks. Use urgency-driven creative "
            "(deadline_urgency theme)."
        ),
    },

    # ------------------------------------------------------------------
    # MOFU — Website Visitors (Pixel Retargeting)
    # ------------------------------------------------------------------
    {
        "id": "website_visitors",
        "name": "Website Visitors — Retargeting",
        "funnel_stage": "MOFU",
        "description": (
            "Retarget all users who visited tandnibeducation.com in the "
            "last 7-30 days but did not convert. Requires Meta Pixel "
            "installed and firing PageView events."
        ),
        "age_min": 14,
        "age_max": 55,
        "genders": ["All"],
        "interests": [],
        "behaviors": [],
        "exclusions": _RETARGETING_EXCLUSIONS,
        "locations": IB_CORE_MARKETS,
        "languages": ["English (All)"],
        "custom_audiences": [
            "Website visitors — All pages (7-30 days)",
            "Exclude: Purchase event (last 30 days)",
            "Exclude: CompleteRegistration event (last 30 days)",
        ],
        "lookalike_source": None,
        "lookalike_percentage": None,
        "estimated_reach": "Depends on site traffic (typically 2K-20K)",
        "recommended_daily_budget_usd": 8.0,
        "retargeting_windows": [
            {"label": "Hot visitors", "days": 7, "priority": "high"},
            {"label": "Warm visitors", "days": 14, "priority": "medium"},
            {"label": "Cool visitors", "days": 30, "priority": "low"},
        ],
        "notes": (
            "Segment into 0-7d, 8-14d, and 15-30d windows for frequency "
            "control. Show different creatives at each interval — social "
            "proof for warm, urgency for cool."
        ),
    },

    # ------------------------------------------------------------------
    # MOFU — Content Engagers
    # ------------------------------------------------------------------
    {
        "id": "content_engagers",
        "name": "Content Engagers — Social Retargeting",
        "funnel_stage": "MOFU",
        "description": (
            "Users who engaged with T&N IB Education content on Facebook "
            "or Instagram in the last 30-90 days. Includes video viewers "
            "(25%+), post reactions, comments, shares, and profile visitors."
        ),
        "age_min": 14,
        "age_max": 55,
        "genders": ["All"],
        "interests": [],
        "behaviors": [],
        "exclusions": _RETARGETING_EXCLUSIONS,
        "locations": IB_CORE_MARKETS,
        "languages": ["English (All)"],
        "custom_audiences": [
            "Facebook Page engagers (90 days)",
            "Instagram business profile engagers (90 days)",
            "Video viewers — watched 25% or more (90 days)",
            "People who sent a message to the Page (90 days)",
            "People who saved any post or ad (90 days)",
            "Exclude: Website visitors (to avoid overlap with website_visitors segment)",
        ],
        "lookalike_source": None,
        "lookalike_percentage": None,
        "estimated_reach": "Depends on content volume (typically 5K-50K)",
        "recommended_daily_budget_usd": 7.0,
        "notes": (
            "Layer with website visitor exclusion to avoid audience overlap. "
            "Best creative: testimonials, detailed subject breakdowns, "
            "and free resource offers to drive site visits."
        ),
    },

    # ------------------------------------------------------------------
    # BOFU — High-Intent Visitors
    # ------------------------------------------------------------------
    {
        "id": "high_intent_visitors",
        "name": "High-Intent Visitors — Pricing & Booking Pages",
        "funnel_stage": "BOFU",
        "description": (
            "Users who visited high-intent pages (pricing, booking, checkout, "
            "or free trial signup) in the last 14 days but did not convert. "
            "These users are closest to purchasing."
        ),
        "age_min": 14,
        "age_max": 55,
        "genders": ["All"],
        "interests": [],
        "behaviors": [],
        "exclusions": [
            "Existing customers (purchase event, last 180 days)",
            "Users who completed booking (last 14 days)",
        ],
        "locations": IB_CORE_MARKETS,
        "languages": ["English (All)"],
        "custom_audiences": [
            "Website visitors — /pricing page (14 days)",
            "Website visitors — /booking page (14 days)",
            "Website visitors — /checkout page (14 days)",
            "Website visitors — /free-trial page (14 days)",
            "InitiateCheckout event without Purchase (14 days)",
            "AddToCart event without Purchase (14 days)",
        ],
        "lookalike_source": None,
        "lookalike_percentage": None,
        "estimated_reach": "Depends on site traffic (typically 500-5K)",
        "recommended_daily_budget_usd": 10.0,
        "notes": (
            "Highest-value retargeting segment. Use direct-response creative "
            "with strong CTAs: limited-time discount, free first session, "
            "or social proof from recent students. Cap frequency at 1x/day "
            "to avoid ad fatigue."
        ),
    },
]


# =============================================================================
# THEME-TO-AUDIENCE MAPPING
# =============================================================================

_THEME_AUDIENCE_MAP = {
    "ia_kickstart": [
        "ib_students_broad",
        "ib_students_subject",
        "website_visitors",
        "content_engagers",
        "lookalike_converters",
    ],
    "score_boost": [
        "ib_parents_broad",
        "website_visitors",
        "content_engagers",
        "high_intent_visitors",
    ],
    "ai_ethics": [
        "ib_parents_broad",
        "ib_students_broad",
        "content_engagers",
    ],
    "subject_spotlight": [
        "ib_students_subject",
        "website_visitors",
        "lookalike_converters",
    ],
    "deadline_urgency": [
        "exam_season_surge",
        "website_visitors",
        "high_intent_visitors",
        "ib_students_broad",
    ],
}

# Build a lookup dict for fast access by segment ID
_SEGMENT_BY_ID = {seg["id"]: seg for seg in AUDIENCE_SEGMENTS}


# =============================================================================
# PUBLIC FUNCTIONS
# =============================================================================

def get_audiences_for_theme(theme_id: str) -> list[dict]:
    """Return the recommended audience segments for a given campaign theme.

    Args:
        theme_id: One of the theme IDs defined in CAMPAIGN_THEMES
                  (e.g. "ia_kickstart", "score_boost").

    Returns:
        List of audience segment dicts suitable for the theme.

    Raises:
        ValueError: If theme_id is not recognised.
    """
    if theme_id not in _THEME_AUDIENCE_MAP:
        valid = ", ".join(sorted(_THEME_AUDIENCE_MAP.keys()))
        raise ValueError(
            f"Unknown theme_id '{theme_id}'. Valid themes: {valid}"
        )

    segment_ids = _THEME_AUDIENCE_MAP[theme_id]
    return [_SEGMENT_BY_ID[sid] for sid in segment_ids if sid in _SEGMENT_BY_ID]


def get_audiences_by_funnel(stage: str) -> list[dict]:
    """Return all audience segments for a given funnel stage.

    Args:
        stage: One of "TOFU", "MOFU", or "BOFU".

    Returns:
        List of audience segment dicts matching the funnel stage.

    Raises:
        ValueError: If stage is not a valid funnel stage.
    """
    stage_upper = stage.upper()
    if stage_upper not in FUNNEL_STAGES:
        valid = ", ".join(sorted(FUNNEL_STAGES.keys()))
        raise ValueError(
            f"Unknown funnel stage '{stage}'. Valid stages: {valid}"
        )

    return [seg for seg in AUDIENCE_SEGMENTS if seg["funnel_stage"] == stage_upper]


def estimate_daily_budget(audience: dict, total_daily_budget: float = 50.0) -> float:
    """Estimate the daily budget allocation for a single audience segment.

    Budget is distributed across all audiences weighted by funnel stage:
      - BOFU audiences receive the highest per-audience allocation (they
        are smaller but highest-intent).
      - TOFU audiences share a larger total pool but individually receive
        less because there are more of them.

    The allocation follows the funnel weights defined in FUNNEL_STAGES
    and divides evenly among audiences within each stage.

    Args:
        audience: An audience segment dict (must have "funnel_stage" key).
        total_daily_budget: Total daily ad spend in USD across all audiences.

    Returns:
        Estimated daily budget in USD for this audience, rounded to 2 decimals.
    """
    stage = audience["funnel_stage"]
    stage_weight = FUNNEL_STAGES[stage]["budget_weight"]
    stage_pool = total_daily_budget * stage_weight

    # Count how many audiences share this stage's pool
    peers_in_stage = sum(
        1 for seg in AUDIENCE_SEGMENTS if seg["funnel_stage"] == stage
    )

    if peers_in_stage == 0:
        return 0.0

    return round(stage_pool / peers_in_stage, 2)


def get_segment_by_id(segment_id: str) -> dict | None:
    """Look up a single audience segment by its ID.

    Args:
        segment_id: The unique segment identifier (e.g. "ib_students_broad").

    Returns:
        The audience segment dict, or None if not found.
    """
    return _SEGMENT_BY_ID.get(segment_id)


def get_all_locations() -> list[str]:
    """Return a deduplicated, sorted list of all targeted country codes."""
    codes = set()
    for seg in AUDIENCE_SEGMENTS:
        codes.update(seg.get("locations", []))
    return sorted(codes)


# =============================================================================
# CLI SUMMARY
# =============================================================================

def _print_summary() -> None:
    """Print a formatted summary of all audience segments."""
    divider = "=" * 72

    print(divider)
    print("T&N IB EDUCATION — Meta Ads Audience Targeting Summary")
    print(f"Total segments: {len(AUDIENCE_SEGMENTS)}")
    print(divider)

    # Funnel stage overview
    print("\nFUNNEL STAGE OVERVIEW")
    print("-" * 40)
    for stage_key, stage_info in FUNNEL_STAGES.items():
        count = len(get_audiences_by_funnel(stage_key))
        print(f"  {stage_key:5s}  |  {stage_info['label']}")
        print(f"         |  Budget weight: {stage_info['budget_weight']:.0%}")
        print(f"         |  Segments: {count}")
        print(f"         |  Objectives: {', '.join(stage_info['meta_objectives'])}")
        print()

    # Per-segment detail
    total_budget = 50.0
    print(f"\nAUDIENCE SEGMENTS  (budget based on ${total_budget:.0f}/day total)")
    print(divider)

    for seg in AUDIENCE_SEGMENTS:
        budget = estimate_daily_budget(seg, total_budget)
        print(f"\n  [{seg['funnel_stage']}] {seg['name']}")
        print(f"  ID: {seg['id']}")
        print(f"  {seg['description']}")
        print(f"  Age: {seg['age_min']}-{seg['age_max']}")
        print(f"  Locations: {', '.join(seg['locations'][:8])}", end="")
        if len(seg["locations"]) > 8:
            print(f" +{len(seg['locations']) - 8} more", end="")
        print()

        if seg["interests"]:
            shown = seg["interests"][:6]
            print(f"  Interests: {', '.join(shown)}", end="")
            if len(seg["interests"]) > 6:
                print(f" +{len(seg['interests']) - 6} more", end="")
            print()

        if seg["behaviors"]:
            print(f"  Behaviors: {', '.join(seg['behaviors'][:4])}")

        if seg["custom_audiences"]:
            print(f"  Custom audiences:")
            for ca in seg["custom_audiences"]:
                print(f"    - {ca}")

        if seg.get("lookalike_source"):
            print(f"  Lookalike source: {seg['lookalike_source']}")
            print(f"  Lookalike %: {seg['lookalike_percentage']}%")

        if seg["exclusions"]:
            print(f"  Exclusions:")
            for ex in seg["exclusions"]:
                print(f"    - {ex}")

        print(f"  Est. reach: {seg.get('estimated_reach', 'N/A')}")
        print(f"  Allocated daily budget: ${budget:.2f}")

        if seg.get("notes"):
            print(f"  Notes: {seg['notes']}")

    # Theme mapping
    print(f"\n{divider}")
    print("THEME -> AUDIENCE MAPPING")
    print(divider)
    for theme in CAMPAIGN_THEMES:
        tid = theme["id"]
        audiences = get_audiences_for_theme(tid)
        audience_names = [a["name"] for a in audiences]
        print(f"\n  {theme['name']} ({tid})")
        print(f"  Hook: \"{theme['hook']}\"")
        for aname in audience_names:
            print(f"    -> {aname}")

    # Budget summary
    print(f"\n{divider}")
    print(f"BUDGET ALLOCATION SUMMARY (${total_budget:.0f}/day)")
    print(divider)
    for stage_key in FUNNEL_STAGES:
        stage_audiences = get_audiences_by_funnel(stage_key)
        stage_total = sum(
            estimate_daily_budget(a, total_budget) for a in stage_audiences
        )
        print(f"  {stage_key}: ${stage_total:.2f}/day across {len(stage_audiences)} audiences")

    total_allocated = sum(
        estimate_daily_budget(a, total_budget) for a in AUDIENCE_SEGMENTS
    )
    print(f"  Total allocated: ${total_allocated:.2f}/day")
    print(divider)


if __name__ == "__main__":
    _print_summary()
