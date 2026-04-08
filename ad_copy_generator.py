"""
Ad Copy Generator for T&N IB Education — Facebook & Instagram Campaigns
========================================================================
Generates compelling ad copy using proven copywriting frameworks (AIDA, PAS,
BAB, FOMO), tailored to IB students and parents. Respects Meta's ad copy
character limits and adapts copy for different ad placements.

Inspired by agentkits-marketing copywriter agent patterns.
"""

import random

from brand_constants import (
    BRAND,
    SELLING_POINTS,
    CAMPAIGN_THEMES,
    AD_COPY_LIMITS,
    AD_FORMATS,
    IB_SUBJECTS,
    TARGET_AUDIENCE,
)


# =============================================================================
# COPY FRAMEWORKS — Templates keyed by (theme_id, framework)
# =============================================================================
# Each framework returns primary_text, headline, description strings.
# {subject} placeholders are filled when a subject is provided.
# {pain_point} placeholders are filled from the audience's pain points.

_COPY_TEMPLATES = {
    # ----- IA KICKSTART -----
    ("ia_kickstart", "aida", "primary"): {
        "primary_text": (
            "Starting your IA? Our AI tools help you find the perfect topic, "
            "build a strong structure, and refine your analysis — ethically."
        ),
        "headline": "Ace Your IA With AI-Powered Help",
        "description": "Expert IB tutors + smart AI",
    },
    ("ia_kickstart", "aida", "secondary"): {
        "primary_text": (
            "Your child's IA can make or break their IB grade. "
            "Give them expert tutoring and ethical AI support to get it right."
        ),
        "headline": "Help Your Child Ace Their IA",
        "description": "Trusted by IB families",
    },
    ("ia_kickstart", "pas", "primary"): {
        "primary_text": (
            "Staring at a blank page for your IA? You're not alone. "
            "Our AI-guided platform helps you go from stuck to structured in one session."
        ),
        "headline": "Stuck on Your IA? We Fix That",
        "description": "From blank page to top marks",
    },
    ("ia_kickstart", "pas", "secondary"): {
        "primary_text": (
            "Is your child stressed about their Internal Assessment? "
            "Our tutors and AI tools turn IA panic into a clear plan — fast."
        ),
        "headline": "End Your Child's IA Stress",
        "description": "Results parents can trust",
    },
    ("ia_kickstart", "bab", "primary"): {
        "primary_text": (
            "Before: no topic, no structure, no confidence. "
            "After: a polished IA you're proud of. "
            "Bridge: T&N's AI-powered tutoring gets you there."
        ),
        "headline": "From Lost to a 7 on Your IA",
        "description": "AI-guided, tutor-approved",
    },
    ("ia_kickstart", "bab", "secondary"): {
        "primary_text": (
            "Before: your child is overwhelmed by IB deadlines. "
            "After: they submit a confident, well-structured IA. "
            "We bridge the gap with expert tutoring and AI."
        ),
        "headline": "Transform Your Child's IA",
        "description": "Ethical AI + expert tutors",
    },
    ("ia_kickstart", "fomo", "primary"): {
        "primary_text": (
            "Hundreds of IB students already started their IAs with our AI tools. "
            "Don't wait until the deadline to get help — spots fill fast."
        ),
        "headline": "Don't Start Your IA Alone",
        "description": "Limited tutor spots left",
    },
    ("ia_kickstart", "fomo", "secondary"): {
        "primary_text": (
            "Other IB families are already giving their children an edge. "
            "Our AI-assisted IA support has limited availability — book now."
        ),
        "headline": "IB Parents Are Booking Fast",
        "description": "Secure your child's spot",
    },

    # ----- SCORE BOOST -----
    ("score_boost", "aida", "primary"): {
        "primary_text": (
            "IB students using T&N improve their IA scores by 2+ points on average. "
            "Real tutors. Real AI tools. Real results."
        ),
        "headline": "Boost Your IB Score Today",
        "description": "Average +2 point improvement",
    },
    ("score_boost", "aida", "secondary"): {
        "primary_text": (
            "Your child deserves every point. Our students improve IA scores by 2+ "
            "points on average with expert tutoring and AI-powered guidance."
        ),
        "headline": "+2 Points on Their IA Score",
        "description": "Proven results for IB kids",
    },
    ("score_boost", "pas", "primary"): {
        "primary_text": (
            "A low IA score can cost you your diploma target. "
            "Our students gain 2+ points on average — don't leave marks on the table."
        ),
        "headline": "Stop Losing IA Marks",
        "description": "Data-backed score gains",
    },
    ("score_boost", "pas", "secondary"): {
        "primary_text": (
            "Worried a weak IA will hurt your child's university chances? "
            "Our tutoring delivers a 2+ point average improvement. See the proof."
        ),
        "headline": "Protect Their Uni Prospects",
        "description": "Scores parents celebrate",
    },
    ("score_boost", "bab", "primary"): {
        "primary_text": (
            "Before T&N: scraping a 4 on your IA. After T&N: confidently hitting a 6 or 7. "
            "Our tutors and AI tools make the difference."
        ),
        "headline": "From a 4 to a 7 — For Real",
        "description": "See student success stories",
    },
    ("score_boost", "bab", "secondary"): {
        "primary_text": (
            "Before: your child dreads IA results. After: they celebrate a top score. "
            "Our expert tutors and AI make it happen — see real student stories."
        ),
        "headline": "Watch Their Scores Climb",
        "description": "Real families, real results",
    },
    ("score_boost", "fomo", "primary"): {
        "primary_text": (
            "Students who started with T&N last term already boosted their scores. "
            "The earlier you start, the bigger the gain. Don't wait."
        ),
        "headline": "Your Classmates Are Ahead",
        "description": "Start now, score higher",
    },
    ("score_boost", "fomo", "secondary"): {
        "primary_text": (
            "Families who enrolled early saw the biggest score jumps. "
            "The next IB deadline is closer than you think — act now."
        ),
        "headline": "Early Families See Best Gains",
        "description": "Limited enrolment window",
    },

    # ----- AI DONE RIGHT (ai_ethics) -----
    ("ai_ethics", "aida", "primary"): {
        "primary_text": (
            "AI can help your IA — if you use it the right way. "
            "T&N's tools guide your thinking without writing your work. 100% IB-compliant."
        ),
        "headline": "Use AI the IB-Approved Way",
        "description": "Ethical AI for IB students",
    },
    ("ai_ethics", "aida", "secondary"): {
        "primary_text": (
            "Worried about your child using AI for schoolwork? "
            "T&N's approach is fully aligned with IB academic integrity — see how it works."
        ),
        "headline": "AI Your Child Can Trust",
        "description": "IB-compliant, parent-approved",
    },
    ("ai_ethics", "pas", "primary"): {
        "primary_text": (
            "Confused about what AI use is allowed for your IA? One wrong move and "
            "your work gets flagged. T&N keeps you safe with IB-aligned AI tools."
        ),
        "headline": "Don't Risk an AI Violation",
        "description": "Stay safe, score high",
    },
    ("ai_ethics", "pas", "secondary"): {
        "primary_text": (
            "AI in education worries every parent. Will it help or get them in trouble? "
            "T&N's AI guides thinking, never writes — fully IB-approved."
        ),
        "headline": "AI Without the Worry",
        "description": "Academic integrity first",
    },
    ("ai_ethics", "bab", "primary"): {
        "primary_text": (
            "Before: confused about AI rules, afraid to use helpful tools. "
            "After: confidently using AI to sharpen your IA — the IB-approved way."
        ),
        "headline": "AI Confidence for IB Students",
        "description": "Guided, ethical, effective",
    },
    ("ai_ethics", "bab", "secondary"): {
        "primary_text": (
            "Before: anxious about AI and academic honesty. "
            "After: peace of mind knowing your child uses AI ethically. T&N makes it simple."
        ),
        "headline": "Peace of Mind for IB Parents",
        "description": "Ethical AI, real results",
    },
    ("ai_ethics", "fomo", "primary"): {
        "primary_text": (
            "Smart IB students are already using AI — the right way. "
            "Don't fall behind because you're unsure what's allowed. T&N shows you how."
        ),
        "headline": "Smart Students Use AI Right",
        "description": "Join them at T&N",
    },
    ("ai_ethics", "fomo", "secondary"): {
        "primary_text": (
            "Other IB families already found the safe way to use AI for assessments. "
            "Don't let your child miss out — learn our IB-approved approach."
        ),
        "headline": "Other Families Found the Way",
        "description": "Your child deserves this too",
    },

    # ----- SUBJECT SPOTLIGHT -----
    ("subject_spotlight", "aida", "primary"): {
        "primary_text": (
            "Your {subject} IA deserves expert eyes. Our tutors and AI tools help you "
            "nail the topic, structure, and analysis — from first draft to final."
        ),
        "headline": "Ace Your {subject} IA",
        "description": "Subject-specific IA support",
    },
    ("subject_spotlight", "aida", "secondary"): {
        "primary_text": (
            "Is your child struggling with their {subject} Internal Assessment? "
            "Our subject-specialist tutors and AI tools will guide them to a top score."
        ),
        "headline": "{subject} IA Help Is Here",
        "description": "Expert tutors for {subject}",
    },
    ("subject_spotlight", "pas", "primary"): {
        "primary_text": (
            "The {subject} IA is one of the toughest in the IB. Wrong topic? Weak analysis? "
            "That's marks lost. Our AI tools and tutors fix both — fast."
        ),
        "headline": "Don't Bomb Your {subject} IA",
        "description": "Fix it before the deadline",
    },
    ("subject_spotlight", "pas", "secondary"): {
        "primary_text": (
            "The {subject} IA has a high failure rate — don't let your child be a statistic. "
            "Our tutors specialise in {subject} and know exactly what examiners want."
        ),
        "headline": "Protect Their {subject} Score",
        "description": "{subject} experts on call",
    },
    ("subject_spotlight", "bab", "primary"): {
        "primary_text": (
            "Before: dreading your {subject} IA. After: submitting work you're proud of. "
            "Our AI-powered platform and expert tutors bridge the gap."
        ),
        "headline": "Love Your {subject} IA",
        "description": "From dread to confidence",
    },
    ("subject_spotlight", "bab", "secondary"): {
        "primary_text": (
            "Before: your child panics about {subject}. After: they submit a confident IA. "
            "T&N's {subject} specialists make the transformation happen."
        ),
        "headline": "{subject} IA Transformation",
        "description": "Specialists your child needs",
    },
    ("subject_spotlight", "fomo", "primary"): {
        "primary_text": (
            "Your classmates are already getting {subject} IA help from T&N. "
            "Tutor spots for {subject} are limited — secure yours now."
        ),
        "headline": "{subject} Spots Filling Fast",
        "description": "Don't wait, book today",
    },
    ("subject_spotlight", "fomo", "secondary"): {
        "primary_text": (
            "Other families already booked {subject} IA sessions — and our tutors are "
            "filling up. Give your child the same advantage before it's too late."
        ),
        "headline": "Book {subject} Help Now",
        "description": "Tutor spots are limited",
    },

    # ----- DEADLINE CRUNCH -----
    ("deadline_urgency", "aida", "primary"): {
        "primary_text": (
            "Your IA deadline is closer than you think. Book a session with T&N and get "
            "a clear plan, expert feedback, and AI-powered tools — today."
        ),
        "headline": "IA Deadline? Act Now",
        "description": "Same-week sessions available",
    },
    ("deadline_urgency", "aida", "secondary"): {
        "primary_text": (
            "Your child's IA deadline is approaching. Help them submit their best work "
            "with last-minute expert tutoring and AI-guided revisions."
        ),
        "headline": "Deadline Coming? We're Ready",
        "description": "Fast-track IA support",
    },
    ("deadline_urgency", "pas", "primary"): {
        "primary_text": (
            "IA due next week and you're not even close? "
            "Panicking won't help — but our crash-course tutoring and AI tools will."
        ),
        "headline": "IA Due Soon? Don't Panic",
        "description": "Rapid results, real support",
    },
    ("deadline_urgency", "pas", "secondary"): {
        "primary_text": (
            "Your child's IA is due soon and they haven't started? "
            "Don't watch them struggle. Our rapid-response tutors get IAs on track fast."
        ),
        "headline": "Last-Minute IA Rescue",
        "description": "Expert help when it counts",
    },
    ("deadline_urgency", "bab", "primary"): {
        "primary_text": (
            "Before: panicking with a deadline days away. "
            "After: submitting a strong IA on time. "
            "T&N's rapid tutoring and AI tools get you there."
        ),
        "headline": "From Panic to Polished IA",
        "description": "We work on your timeline",
    },
    ("deadline_urgency", "bab", "secondary"): {
        "primary_text": (
            "Before: your child is in tears over a looming deadline. "
            "After: they submit confidently. T&N's fast-track sessions make it possible."
        ),
        "headline": "Turn Deadline Stress Around",
        "description": "Fast-track support for IAs",
    },
    ("deadline_urgency", "fomo", "primary"): {
        "primary_text": (
            "Last-minute IA sessions are almost fully booked. "
            "Every hour you wait is an hour less to improve your score. Book now."
        ),
        "headline": "Sessions Selling Out Fast",
        "description": "Book before it's too late",
    },
    ("deadline_urgency", "fomo", "secondary"): {
        "primary_text": (
            "Deadline-week tutoring slots are nearly gone. "
            "Other parents already secured help for their children — don't miss out."
        ),
        "headline": "Almost Fully Booked",
        "description": "Grab the last slots now",
    },

    # ----- GENERAL TUITION -----
    ("general_tuition", "aida", "primary"): {
        "primary_text": (
            "Struggling with IB? Get 1-on-1 tutoring from expert IB teachers "
            "across every subject — Maths, Sciences, English, Economics, and more. "
            "Plus our AI-powered IA support to give you the edge."
        ),
        "headline": "Expert IB Tutors, All Subjects",
        "description": "1-on-1 IB tuition online",
    },
    ("general_tuition", "aida", "secondary"): {
        "primary_text": (
            "Give your child the IB support they need — expert 1-on-1 tutoring "
            "in every subject, from Maths to Languages. Plus specialised AI tools "
            "for their Internal Assessments."
        ),
        "headline": "All-Subject IB Tuition",
        "description": "Every subject, one platform",
    },
    ("general_tuition", "pas", "primary"): {
        "primary_text": (
            "IB is tough — juggling 6 subjects, IAs, and exams all at once. "
            "Our expert tutors help you master every subject, and our AI tools "
            "make your IAs stress-free."
        ),
        "headline": "IB Overwhelming? We Help",
        "description": "All subjects + IA support",
    },
    ("general_tuition", "pas", "secondary"): {
        "primary_text": (
            "Watching your child struggle with the IB workload? "
            "Our tutors cover every subject — and our AI-powered IA support "
            "tackles the hardest part of the Diploma."
        ),
        "headline": "End Their IB Struggle",
        "description": "Tutoring parents trust",
    },
    ("general_tuition", "bab", "primary"): {
        "primary_text": (
            "Before: falling behind in multiple subjects. "
            "After: confident across the board with top IA scores. "
            "T&N's expert tutors and AI tools cover everything."
        ),
        "headline": "Master Every IB Subject",
        "description": "Tuition + AI IA support",
    },
    ("general_tuition", "bab", "secondary"): {
        "primary_text": (
            "Before: your child is stressed across multiple IB subjects. "
            "After: they're thriving with personalised tutor support and "
            "AI-guided IA help. T&N makes the IB manageable."
        ),
        "headline": "Watch Them Thrive in IB",
        "description": "Full IB support, one place",
    },
    ("general_tuition", "fomo", "primary"): {
        "primary_text": (
            "Top IB students don't do it alone. They get expert tutoring "
            "across all subjects and AI-powered IA support. Spots are limited — "
            "join them now."
        ),
        "headline": "Top Students Use T&N",
        "description": "Limited tutor spots left",
    },
    ("general_tuition", "fomo", "secondary"): {
        "primary_text": (
            "Other IB families already have tutoring locked in for every subject. "
            "Our all-subject tuition with AI IA support is filling up fast."
        ),
        "headline": "Families Are Booking Fast",
        "description": "Secure all-subject support",
    },
}

# Frameworks list for iteration
FRAMEWORKS = ["aida", "pas", "bab", "fomo"]

FRAMEWORK_LABELS = {
    "aida": "AIDA (Attention, Interest, Desire, Action)",
    "pas": "PAS (Problem, Agitate, Solution)",
    "bab": "BAB (Before, After, Bridge)",
    "fomo": "FOMO (Fear of Missing Out)",
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _get_theme(theme_id: str) -> dict:
    """Look up a campaign theme by id."""
    for theme in CAMPAIGN_THEMES:
        if theme["id"] == theme_id:
            return theme
    raise ValueError(f"Unknown theme_id: {theme_id!r}")


def _pick_cta(theme: dict) -> str:
    """Return a CTA from the allowed options, preferring the theme's own CTA."""
    allowed = AD_COPY_LIMITS["cta_options"]
    theme_cta = theme.get("cta", "")
    # Map theme CTAs to the closest allowed option
    cta_map = {
        "Get Started Free": "Get Started",
        "See How They Did It": "Learn More",
        "Learn Our Approach": "Learn More",
        "Get Expert Help Now": "Get Started",
        "Book a Session Today": "Book Now",
    }
    mapped = cta_map.get(theme_cta, theme_cta)
    if mapped in allowed:
        return mapped
    return "Learn More"


def _pick_subject(subject: str | None = None) -> str:
    """Return a subject string — use the given one or pick a popular default."""
    if subject:
        return subject
    popular = ["Mathematics AA", "Physics", "Economics", "Chemistry", "Biology",
               "English A: Language & Literature", "Psychology"]
    return random.choice(popular)


def _truncate(text: str, max_chars: int) -> str:
    """Truncate text to max_chars, ending cleanly at a word boundary."""
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars - 1]
    # Cut at the last space to avoid breaking a word
    last_space = truncated.rfind(" ")
    if last_space > max_chars // 2:
        truncated = truncated[:last_space]
    return truncated.rstrip(" .,") + "\u2026"


def _fill_subject(text: str, subject: str) -> str:
    """Replace {subject} placeholders with the actual subject name."""
    return text.replace("{subject}", subject)


# =============================================================================
# CORE GENERATION FUNCTIONS
# =============================================================================

def generate_ad_copy(
    theme_id: str,
    framework: str = "aida",
    subject: str | None = None,
    audience: str = "primary",
) -> dict:
    """
    Generate a single ad copy dict for the given theme and framework.

    Parameters
    ----------
    theme_id : str
        One of the campaign theme ids (e.g. "ia_kickstart", "score_boost").
    framework : str
        Copywriting framework: "aida", "pas", "bab", or "fomo".
    subject : str | None
        IB subject name — required for "subject_spotlight", optional otherwise.
    audience : str
        Target audience key: "primary" (students) or "secondary" (parents).

    Returns
    -------
    dict with keys: primary_text, headline, description, cta, and metadata.
    """
    framework = framework.lower()
    if framework not in FRAMEWORKS:
        raise ValueError(f"Unknown framework: {framework!r}. Choose from {FRAMEWORKS}")

    theme = _get_theme(theme_id)
    audience_key = audience if audience in ("primary", "secondary") else "primary"

    # Look up the template
    key = (theme_id, framework, audience_key)
    if key not in _COPY_TEMPLATES:
        raise ValueError(
            f"No copy template for theme={theme_id!r}, "
            f"framework={framework!r}, audience={audience_key!r}"
        )

    template = _COPY_TEMPLATES[key]

    # Resolve subject for subject_spotlight (or any template with placeholders)
    subj = _pick_subject(subject) if theme_id == "subject_spotlight" else (subject or "")
    primary_text = _fill_subject(template["primary_text"], subj)
    headline = _fill_subject(template["headline"], subj)
    description = _fill_subject(template["description"], subj)

    # Enforce character limits
    primary_text = _truncate(primary_text, AD_COPY_LIMITS["primary_text"]["max_chars"])
    headline = _truncate(headline, AD_COPY_LIMITS["headline"]["max_chars"])
    description = _truncate(description, AD_COPY_LIMITS["description"]["max_chars"])

    cta = _pick_cta(theme)

    return {
        "primary_text": primary_text,
        "headline": headline,
        "description": description,
        "cta": cta,
        "metadata": {
            "theme_id": theme_id,
            "theme_name": theme["name"],
            "framework": framework,
            "framework_label": FRAMEWORK_LABELS[framework],
            "target_audience": audience_key,
            "audience_label": TARGET_AUDIENCE[audience_key]["label"],
            "subject": subj if subj else None,
        },
    }


def generate_variations(
    theme_id: str,
    num_variations: int = 3,
    subject: str | None = None,
) -> list[dict]:
    """
    Generate multiple copy variations for A/B testing.

    Uses different frameworks and alternates between primary/secondary audiences
    to produce diverse variations. Best practice: test 3-5 variations per campaign.

    Parameters
    ----------
    theme_id : str
        Campaign theme id.
    num_variations : int
        Number of variations to generate (1-8). Defaults to 3.
    subject : str | None
        IB subject name for subject_spotlight theme.

    Returns
    -------
    list of ad copy dicts (same structure as generate_ad_copy output).
    """
    num_variations = max(1, min(num_variations, len(FRAMEWORKS) * 2))
    variations = []

    # Build a list of (framework, audience) combos to cycle through
    combos = []
    for fw in FRAMEWORKS:
        for aud in ("primary", "secondary"):
            combos.append((fw, aud))

    # Shuffle to get variety across runs, but seed for reproducibility within a call
    random.shuffle(combos)

    for fw, aud in combos[:num_variations]:
        copy = generate_ad_copy(
            theme_id=theme_id,
            framework=fw,
            subject=subject,
            audience=aud,
        )
        copy["variation_index"] = len(variations) + 1
        variations.append(copy)

    return variations


def generate_campaign_copy_set(theme_id: str, subject: str | None = None) -> dict:
    """
    Generate ad copy adapted for every ad format.

    Stories/reels get shorter, punchier copy. Feed posts get more detail.
    Carousel cards get concise per-card copy.

    Parameters
    ----------
    theme_id : str
        Campaign theme id.
    subject : str | None
        IB subject name for subject_spotlight theme.

    Returns
    -------
    dict keyed by ad format name, each containing an ad copy dict.
    """
    # Format-specific character budgets (tighter for stories, fuller for feed)
    format_limits = {
        "portrait_story": {"primary_text": 80, "headline": 25, "description": 20},
        "square_feed": {"primary_text": 125, "headline": 40, "description": 30},
        "landscape_feed": {"primary_text": 125, "headline": 40, "description": 30},
        "vertical_feed": {"primary_text": 110, "headline": 35, "description": 30},
        "carousel_card": {"primary_text": 90, "headline": 30, "description": 25},
    }

    # Pick a framework that suits each format's feel
    format_frameworks = {
        "portrait_story": "fomo",     # short, urgent — perfect for stories
        "square_feed": "aida",        # balanced attention-grabber
        "landscape_feed": "pas",      # more room for problem/solution narrative
        "vertical_feed": "bab",       # visual before/after suits vertical
        "carousel_card": "aida",      # clear and scannable per card
    }

    result = {}
    for fmt_key, fmt_info in AD_FORMATS.items():
        fw = format_frameworks.get(fmt_key, "aida")
        limits = format_limits.get(fmt_key, {})

        copy = generate_ad_copy(
            theme_id=theme_id,
            framework=fw,
            subject=subject,
            audience="primary",
        )

        # Re-truncate to format-specific limits
        if limits:
            copy["primary_text"] = _truncate(
                copy["primary_text"], limits["primary_text"]
            )
            copy["headline"] = _truncate(copy["headline"], limits["headline"])
            copy["description"] = _truncate(
                copy["description"], limits["description"]
            )

        copy["ad_format"] = fmt_key
        copy["ad_format_label"] = fmt_info["label"]
        copy["platforms"] = fmt_info.get("platforms", [])
        result[fmt_key] = copy

    return result


# =============================================================================
# PRETTY PRINTING
# =============================================================================

def _print_divider(char: str = "=", width: int = 72):
    print(char * width)


def _print_copy(copy: dict, indent: str = "  "):
    """Print a single ad copy dict in a readable format."""
    meta = copy.get("metadata", {})
    print(f"{indent}Framework : {meta.get('framework_label', 'N/A')}")
    print(f"{indent}Audience  : {meta.get('audience_label', 'N/A')}")
    if meta.get("subject"):
        print(f"{indent}Subject   : {meta['subject']}")
    print()
    print(f"{indent}Primary   : {copy['primary_text']}")
    print(f"{indent}            ({len(copy['primary_text'])} chars)")
    print(f"{indent}Headline  : {copy['headline']}")
    print(f"{indent}            ({len(copy['headline'])} chars)")
    print(f"{indent}Description: {copy['description']}")
    print(f"{indent}            ({len(copy['description'])} chars)")
    print(f"{indent}CTA       : [{copy['cta']}]")


# =============================================================================
# MAIN — Demonstration
# =============================================================================

if __name__ == "__main__":
    print()
    _print_divider()
    print(f"  {BRAND['company_name']} — Ad Copy Generator")
    print(f"  {BRAND['tagline']}")
    _print_divider()

    # --- 1. Generate copy for each campaign theme ---
    print("\n\n>>> SINGLE COPY PER THEME (AIDA framework, student audience)\n")

    for theme in CAMPAIGN_THEMES:
        tid = theme["id"]
        subj = "Physics" if tid == "subject_spotlight" else None
        copy = generate_ad_copy(tid, framework="aida", subject=subj)

        _print_divider("-", 60)
        print(f"  Theme: {theme['name']}  |  Hook: \"{theme['hook']}\"")
        _print_divider("-", 60)
        _print_copy(copy)
        print()

    # --- 2. A/B test variations for one theme ---
    print()
    _print_divider()
    print("  A/B TEST VARIATIONS — 'IA Kickstart' theme (4 variations)")
    _print_divider()

    variations = generate_variations("ia_kickstart", num_variations=4)
    for v in variations:
        print(f"\n  --- Variation {v['variation_index']} ---")
        _print_copy(v)
    print()

    # --- 3. Format-adapted copy set for one theme ---
    print()
    _print_divider()
    print("  FORMAT-ADAPTED COPY SET — 'Score Boost' theme")
    _print_divider()

    copy_set = generate_campaign_copy_set("score_boost")
    for fmt_key, copy in copy_set.items():
        print(f"\n  [{copy['ad_format_label']}]")
        print(f"  Platforms: {', '.join(copy.get('platforms', []))}")
        _print_copy(copy, indent="    ")
    print()

    # --- 4. Subject spotlight with a specific subject ---
    print()
    _print_divider()
    print("  SUBJECT SPOTLIGHT — Multiple IB subjects")
    _print_divider()

    spotlight_subjects = ["Economics", "Mathematics AA", "Chemistry",
                          "English A: Literature", "Psychology"]
    for subj in spotlight_subjects:
        copy = generate_ad_copy("subject_spotlight", framework="pas", subject=subj)
        print(f"\n  --- {subj} ---")
        _print_copy(copy)
    print()

    _print_divider()
    print(f"  Generated by {BRAND['company_name']} Ad Copy Engine")
    print(f"  Visit {BRAND['website']}")
    _print_divider()
    print()
