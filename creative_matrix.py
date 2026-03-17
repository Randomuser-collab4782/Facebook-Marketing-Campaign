"""
Creative Matrix System for T&N IB Education — Facebook Marketing
================================================================
Generates every combination of Topic × Persona × Visual Style,
producing image descriptions and ad copy for each variant.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field

from brand_constants import (
    AD_COPY_LIMITS,
    BRAND,
    COLOURS,
    FONTS,
)

# =============================================================================
# TOPICS — Key messages to promote
# =============================================================================

TOPICS = [
    {
        "id": "ai_ia_support",
        "name": "AI-Powered IA Support",
        "core_message": (
            "Our AI helps you brainstorm, structure, and refine your Internal "
            "Assessment — every word stays authentically yours."
        ),
        "hook": "Your IA, powered by AI.",
        "emotional_driver": "confidence",
        "keywords": ["AI", "Internal Assessment", "IA help", "structure"],
    },
    {
        "id": "expert_tutors",
        "name": "Expert IB Tutors",
        "core_message": (
            "1-on-1 sessions with tutors who've taught and examined IB curricula, "
            "personalised to your subject and level."
        ),
        "hook": "Learn from tutors who've been IB examiners.",
        "emotional_driver": "trust",
        "keywords": ["tutor", "examiner", "1-on-1", "personalised"],
    },
    {
        "id": "score_improvement",
        "name": "Proven Score Improvements",
        "core_message": (
            "Students using T&N IB Education see an average 2+ point improvement "
            "on their IA scores across all subjects."
        ),
        "hook": "From a 4 to a 7 — real results.",
        "emotional_driver": "aspiration",
        "keywords": ["score", "improvement", "results", "grade 7"],
    },
    {
        "id": "academic_integrity",
        "name": "AI Done Right",
        "core_message": (
            "Our AI guides your thinking without writing your work. Fully aligned "
            "with IB academic integrity policies."
        ),
        "hook": "Use AI the IB-approved way.",
        "emotional_driver": "safety",
        "keywords": ["integrity", "ethical", "IB-approved", "your own work"],
    },
    {
        "id": "deadline_support",
        "name": "Deadline Crunch Support",
        "core_message": (
            "IA deadline approaching? Get expert guidance fast — structured "
            "sessions to help you submit with confidence."
        ),
        "hook": "Deadline close? We've got you.",
        "emotional_driver": "urgency",
        "keywords": ["deadline", "fast", "submit", "last minute"],
    },
    {
        "id": "all_subjects",
        "name": "All IB Subjects Covered",
        "core_message": (
            "From Maths AA to English Lit, Economics to Physics — get IA help "
            "in any IB Diploma subject."
        ),
        "hook": "Every IB subject. One platform.",
        "emotional_driver": "convenience",
        "keywords": ["all subjects", "Maths", "Sciences", "Humanities"],
    },
]

# =============================================================================
# PERSONAS — Audience types we're targeting
# =============================================================================

PERSONAS = [
    {
        "id": "stressed_student",
        "name": "The Stressed Student",
        "age_range": "16-18",
        "description": (
            "A Year 1 or Year 2 IB student juggling multiple IAs, EE, CAS, "
            "and exams. Feeling overwhelmed and unsure where to start."
        ),
        "pain_points": [
            "Too many IAs at once",
            "Don't know how to pick a topic",
            "Worried about failing",
        ],
        "language_style": "Casual, empathetic, peer-like",
        "motivators": ["Quick wins", "Clear structure", "Stress relief"],
        "platforms": ["Instagram Stories", "Instagram Feed", "Reels"],
    },
    {
        "id": "ambitious_achiever",
        "name": "The Ambitious Achiever",
        "age_range": "16-18",
        "description": (
            "A high-performing IB student aiming for 40+ points and top "
            "university offers. Wants to maximise every IA score."
        ),
        "pain_points": [
            "Already scoring 5-6 but wants a 7",
            "Needs that competitive edge",
            "Perfectionism causing paralysis",
        ],
        "language_style": "Aspirational, data-driven, achievement-focused",
        "motivators": ["Top scores", "University admission", "Excellence"],
        "platforms": ["Instagram Feed", "Facebook Feed"],
    },
    {
        "id": "concerned_parent",
        "name": "The Concerned Parent",
        "age_range": "38-55",
        "description": (
            "A parent who sees their child struggling with IB workload. "
            "Wants to help but doesn't understand the IB system well enough."
        ),
        "pain_points": [
            "Child is stressed and shutting down",
            "Worried about university prospects",
            "Unsure if AI tools are safe to use",
        ],
        "language_style": "Reassuring, professional, solution-oriented",
        "motivators": ["Child's wellbeing", "Academic results", "Trust"],
        "platforms": ["Facebook Feed", "Facebook Stories"],
    },
    {
        "id": "proactive_parent",
        "name": "The Proactive Parent",
        "age_range": "35-50",
        "description": (
            "A parent who plans ahead and invests in education early. "
            "Looking for the best resources before problems arise."
        ),
        "pain_points": [
            "Wants to prevent academic struggles",
            "Comparing tutoring options",
            "Needs proof of ROI on tutoring spend",
        ],
        "language_style": "Confident, value-focused, evidence-based",
        "motivators": ["Proven results", "Value for money", "Early advantage"],
        "platforms": ["Facebook Feed", "Instagram Feed"],
    },
    {
        "id": "last_minute_student",
        "name": "The Last-Minute Student",
        "age_range": "16-19",
        "description": (
            "A student with an IA deadline in days or weeks. Needs immediate, "
            "practical help — not a long-term programme."
        ),
        "pain_points": [
            "Deadline is imminent",
            "Haven't started or barely started",
            "Panicking about failing",
        ],
        "language_style": "Urgent, direct, action-oriented",
        "motivators": ["Speed", "Immediate help", "Passing grade"],
        "platforms": ["Instagram Stories", "Reels"],
    },
]

# =============================================================================
# VISUAL STYLES — Art direction for ad creatives
# =============================================================================

VISUAL_STYLES = [
    {
        "id": "clean_modern",
        "name": "Clean & Modern",
        "description": (
            "Minimalist design with generous white space, bold typography, "
            "and subtle gradient accents. Professional and trustworthy."
        ),
        "background": COLOURS["background"],
        "text_colour": COLOURS["text_primary"],
        "accent_colour": COLOURS["secondary"],
        "imagery": "Abstract geometric shapes, clean icons, subtle gradients",
        "font_mood": f"{FONTS['heading']['family']} bold headings, {FONTS['body']['family']} body",
        "photo_style": None,
        "overlay": "None — text on solid/gradient background",
    },
    {
        "id": "student_lifestyle",
        "name": "Student Lifestyle",
        "description": (
            "Warm, relatable photography of diverse students studying, "
            "collaborating, or celebrating. Overlay text on a semi-transparent band."
        ),
        "background": "Photo-based",
        "text_colour": "#FFFFFF",
        "accent_colour": COLOURS["accent"],
        "imagery": (
            "Diverse students aged 16-18 at desks, in libraries, or with laptops. "
            "Natural lighting, candid feel, school/study environment."
        ),
        "font_mood": f"{FONTS['heading']['family']} white bold on dark overlay",
        "photo_style": "Candid, warm-toned, natural light",
        "overlay": f"Semi-transparent {COLOURS['primary']} band (70% opacity) behind text",
    },
    {
        "id": "dark_premium",
        "name": "Dark & Premium",
        "description": (
            "Dark navy background with glowing accent elements. Conveys "
            "exclusivity, tech-forward innovation, and seriousness."
        ),
        "background": COLOURS["background_dark"],
        "text_colour": "#FFFFFF",
        "accent_colour": COLOURS["accent"],
        "imagery": (
            "Dark background with subtle glowing lines, circuit-like patterns, "
            "or soft light particles. AI/tech aesthetic."
        ),
        "font_mood": f"{FONTS['heading']['family']} white on dark, {FONTS['accent']['family']} for stats",
        "photo_style": None,
        "overlay": "Subtle glow effects around key text or numbers",
    },
    {
        "id": "results_showcase",
        "name": "Results Showcase",
        "description": (
            "Data-driven design centred on score numbers, before/after comparisons, "
            "or progress charts. Green success accents."
        ),
        "background": COLOURS["background"],
        "text_colour": COLOURS["text_primary"],
        "accent_colour": COLOURS["success"],
        "imagery": (
            "Large score numbers (e.g., '4 → 7'), progress bars, upward arrows, "
            "checkmarks. Clean data visualisation style."
        ),
        "font_mood": f"{FONTS['accent']['family']} for big numbers, {FONTS['heading']['family']} for headlines",
        "photo_style": None,
        "overlay": "Score highlight with green glow or underline accent",
    },
    {
        "id": "urgent_bold",
        "name": "Urgent & Bold",
        "description": (
            "High-contrast design with red/amber urgency accents, countdown "
            "elements, and bold sans-serif text. Drives immediate action."
        ),
        "background": COLOURS["primary"],
        "text_colour": "#FFFFFF",
        "accent_colour": COLOURS["error"],
        "imagery": (
            "Clock icons, countdown numbers, calendar with circled dates, "
            "exclamation elements. Bold, high-contrast layout."
        ),
        "font_mood": f"{FONTS['heading']['family']} extra-bold white, {FONTS['accent']['family']} for countdown",
        "photo_style": None,
        "overlay": "Red/amber banner or badge for deadline emphasis",
    },
]


# =============================================================================
# CREATIVE MATRIX GENERATION
# =============================================================================


@dataclass
class CreativeVariant:
    """A single Topic × Persona × Style combination with generated assets."""

    variant_id: str
    topic: dict
    persona: dict
    style: dict
    image_description: str
    primary_text: str
    headline: str
    description: str
    cta: str
    recommended_formats: list[str] = field(default_factory=list)


def _build_image_description(topic: dict, persona: dict, style: dict) -> str:
    """Generate a detailed image prompt for this combination."""
    elements = [
        f"Visual style: {style['name']} — {style['description']}",
        f"Background: {style['background']}",
        f"Imagery elements: {style['imagery']}",
    ]

    if style["photo_style"]:
        elements.append(f"Photography direction: {style['photo_style']}")

    if style["overlay"]:
        elements.append(f"Text overlay treatment: {style['overlay']}")

    # Topic-specific visual elements
    topic_visuals = {
        "ai_ia_support": (
            "Show an AI interface or chat-like element alongside a student's "
            "notebook/laptop. Convey human + AI collaboration."
        ),
        "expert_tutors": (
            "Feature a tutor-student interaction — screen share, whiteboard, "
            "or video call. Convey expertise and personal attention."
        ),
        "score_improvement": (
            "Prominently display score numbers with an upward trajectory. "
            "Before/after comparison (e.g., '4 → 7' or 'C → A')."
        ),
        "academic_integrity": (
            "Show a shield or checkmark icon alongside the IB logo area. "
            "Convey trust, safety, and official alignment."
        ),
        "deadline_support": (
            "Include a calendar, clock, or countdown element. "
            "Convey urgency without panic — structured, fast help."
        ),
        "all_subjects": (
            "Show icons or text for multiple IB subjects (Maths, Physics, "
            "English, Economics). Convey breadth and coverage."
        ),
    }
    elements.append(f"Topic visual: {topic_visuals.get(topic['id'], '')}")

    # Persona-specific adjustments
    if persona["id"] in ("stressed_student", "last_minute_student"):
        elements.append(
            "Mood: empathetic and reassuring — avoid imagery that increases anxiety."
        )
    elif persona["id"] == "ambitious_achiever":
        elements.append(
            "Mood: aspirational and polished — convey excellence and top performance."
        )
    elif persona["id"] in ("concerned_parent", "proactive_parent"):
        elements.append(
            "Mood: professional and trustworthy — appeal to adults making investment decisions."
        )

    elements.append(
        f"Text on image: Headline in {style['font_mood']}. "
        f"Include T&N IB Education logo. Accent colour: {style['accent_colour']}."
    )

    return "\n".join(f"- {e}" for e in elements)


def _build_primary_text(topic: dict, persona: dict) -> str:
    """Generate ad primary text tailored to persona and topic."""
    max_chars = AD_COPY_LIMITS["primary_text"]["max_chars"]

    templates = {
        ("ai_ia_support", "stressed_student"): (
            "Stuck on your IA? Our AI helps you find a topic, build your "
            "structure, and sharpen your analysis. Your words, your grade."
        ),
        ("ai_ia_support", "ambitious_achiever"): (
            "Already good — want to be great? Our AI tools help you refine "
            "your IA analysis to examiner-level precision."
        ),
        ("ai_ia_support", "concerned_parent"): (
            "Your child's IA work stays 100% their own. Our AI guides their "
            "thinking — it never writes for them."
        ),
        ("ai_ia_support", "proactive_parent"): (
            "Give your child the smartest study tool available. AI-guided IA "
            "support that builds skills, not dependency."
        ),
        ("ai_ia_support", "last_minute_student"): (
            "IA due soon? Our AI can help you structure your work fast. "
            "Get a clear plan in your first session."
        ),
        ("expert_tutors", "stressed_student"): (
            "You don't have to figure it out alone. Our IB examiner-tutors "
            "break down exactly what your IA needs."
        ),
        ("expert_tutors", "ambitious_achiever"): (
            "Learn what IB examiners actually look for. Our tutors have "
            "marked hundreds of IAs — now they'll help perfect yours."
        ),
        ("expert_tutors", "concerned_parent"): (
            "Expert IB tutors with real examining experience. Personalised "
            "1-on-1 sessions that get your child back on track."
        ),
        ("expert_tutors", "proactive_parent"): (
            "Invest in tutoring that works. Our IB examiner-tutors deliver "
            "measurable score improvements across all subjects."
        ),
        ("expert_tutors", "last_minute_student"): (
            "Need an expert — fast? Book a session with an IB examiner-tutor "
            "and get your IA on track today."
        ),
        ("score_improvement", "stressed_student"): (
            "Students like you improved from 4s to 7s on their IAs. "
            "Real results, real people — you can do this too."
        ),
        ("score_improvement", "ambitious_achiever"): (
            "Our students average 2+ points higher on their IAs. "
            "When every point counts for uni, this is your edge."
        ),
        ("score_improvement", "concerned_parent"): (
            "Parents trust us because we deliver. Average 2+ point IA score "
            "improvement across all IB subjects."
        ),
        ("score_improvement", "proactive_parent"): (
            "The data speaks: 2+ point average IA improvement. "
            "See why parents choose T&N IB Education."
        ),
        ("score_improvement", "last_minute_student"): (
            "Even starting late, our students see real improvements. "
            "One focused session can change your IA score."
        ),
        ("academic_integrity", "stressed_student"): (
            "Worried about using AI for your IA? We show you exactly how to "
            "use it the IB-approved way. No risk, just better work."
        ),
        ("academic_integrity", "ambitious_achiever"): (
            "Smart students use AI smartly. Learn the IB-compliant way to "
            "leverage AI tools and stay ahead — ethically."
        ),
        ("academic_integrity", "concerned_parent"): (
            "Concerned about AI and your child's IB work? Our approach is "
            "fully aligned with IB integrity policies. 100% safe."
        ),
        ("academic_integrity", "proactive_parent"): (
            "AI in education is here to stay. We teach students to use it "
            "ethically — building skills the IB rewards."
        ),
        ("academic_integrity", "last_minute_student"): (
            "Need AI help but scared of integrity issues? We keep it safe. "
            "Get IB-approved guidance — no risks."
        ),
        ("deadline_support", "stressed_student"): (
            "Deadline breathing down your neck? Deep breath. Book a session "
            "and we'll build your IA plan together — today."
        ),
        ("deadline_support", "ambitious_achiever"): (
            "Running out of time doesn't mean settling for less. Our tutors "
            "help you submit a high-scoring IA, even under pressure."
        ),
        ("deadline_support", "concerned_parent"): (
            "Your child's IA deadline is close and they're struggling? "
            "We offer fast, focused sessions to help them submit on time."
        ),
        ("deadline_support", "proactive_parent"): (
            "Don't wait until the last week. Book IA support now so your "
            "child submits with confidence, not panic."
        ),
        ("deadline_support", "last_minute_student"): (
            "IA due this week? We specialise in fast turnarounds. "
            "Book now — let's get it done."
        ),
        ("all_subjects", "stressed_student"): (
            "Maths, Physics, English, Economics — whatever your IA subject, "
            "we've got a specialist tutor ready for you."
        ),
        ("all_subjects", "ambitious_achiever"): (
            "Top scores across every subject. Our tutors cover all IB "
            "subjects at HL and SL — find your specialist."
        ),
        ("all_subjects", "concerned_parent"): (
            "One platform for every IB subject. No need to find separate "
            "tutors — we cover Maths, Sciences, Humanities, and more."
        ),
        ("all_subjects", "proactive_parent"): (
            "Why juggle multiple tutors? T&N covers every IB subject "
            "under one roof — consistent quality, proven results."
        ),
        ("all_subjects", "last_minute_student"): (
            "Whatever subject your IA is in, we have a tutor ready now. "
            "Maths, Sciences, English — all covered."
        ),
    }

    key = (topic["id"], persona["id"])
    text = templates.get(key, topic["core_message"])
    return text[:max_chars]


def _build_headline(topic: dict, persona: dict) -> str:
    """Generate a short headline for the ad."""
    max_chars = AD_COPY_LIMITS["headline"]["max_chars"]

    headlines = {
        ("ai_ia_support", "stressed_student"): "AI-Powered IA Help Is Here",
        ("ai_ia_support", "ambitious_achiever"): "Refine Your IA With AI",
        ("ai_ia_support", "concerned_parent"): "Safe AI for IB Students",
        ("ai_ia_support", "proactive_parent"): "Smarter IA Prep With AI",
        ("ai_ia_support", "last_minute_student"): "AI IA Help — Start Now",
        ("expert_tutors", "stressed_student"): "IB Examiners On Your Side",
        ("expert_tutors", "ambitious_achiever"): "Learn From IB Examiners",
        ("expert_tutors", "concerned_parent"): "Trusted IB Examiner Tutors",
        ("expert_tutors", "proactive_parent"): "Expert IB Tutors, Proven",
        ("expert_tutors", "last_minute_student"): "Expert Help — Book Today",
        ("score_improvement", "stressed_student"): "From 4 to 7. You Can Too.",
        ("score_improvement", "ambitious_achiever"): "Average +2 Points on IAs",
        ("score_improvement", "concerned_parent"): "Proven IA Score Boosts",
        ("score_improvement", "proactive_parent"): "Results That Speak",
        ("score_improvement", "last_minute_student"): "Boost Your IA Score Fast",
        ("academic_integrity", "stressed_student"): "AI Help, Zero Risk",
        ("academic_integrity", "ambitious_achiever"): "Use AI the Smart Way",
        ("academic_integrity", "concerned_parent"): "IB-Approved AI Approach",
        ("academic_integrity", "proactive_parent"): "Ethical AI for IB",
        ("academic_integrity", "last_minute_student"): "Safe AI — Fast Results",
        ("deadline_support", "stressed_student"): "Deadline Close? We Help.",
        ("deadline_support", "ambitious_achiever"): "Submit Strong, On Time",
        ("deadline_support", "concerned_parent"): "IA Deadline Support",
        ("deadline_support", "proactive_parent"): "Plan Ahead, Score High",
        ("deadline_support", "last_minute_student"): "Due This Week? Book Now.",
        ("all_subjects", "stressed_student"): "Every IB Subject Covered",
        ("all_subjects", "ambitious_achiever"): "Specialists in Every Subject",
        ("all_subjects", "concerned_parent"): "One Platform, All Subjects",
        ("all_subjects", "proactive_parent"): "All IB Subjects, One Place",
        ("all_subjects", "last_minute_student"): "Any Subject. Right Now.",
    }

    key = (topic["id"], persona["id"])
    return headlines.get(key, topic["hook"])[:max_chars]


def _build_description(topic: dict, persona: dict) -> str:
    """Generate the short description line."""
    max_chars = AD_COPY_LIMITS["description"]["max_chars"]

    if persona["id"] in ("stressed_student", "last_minute_student"):
        return BRAND["tagline"][:max_chars]
    elif persona["id"] == "ambitious_achiever":
        return "Maximise your IB score."[:max_chars]
    elif persona["id"] == "concerned_parent":
        return "Trusted by IB families."[:max_chars]
    else:
        return "Expert IB IA support."[:max_chars]


def _pick_cta(topic: dict, persona: dict) -> str:
    """Select the best CTA for this combination."""
    if persona["id"] == "last_minute_student":
        return "Book Now"
    if topic["id"] == "score_improvement":
        return "Learn More"
    if topic["id"] == "academic_integrity":
        return "Learn More"
    if persona["id"] in ("concerned_parent", "proactive_parent"):
        return "Learn More"
    return "Get Started"


def _pick_formats(persona: dict, style: dict) -> list[str]:
    """Recommend ad formats based on persona platforms and style."""
    platform_to_format = {
        "Instagram Stories": "portrait_story",
        "Instagram Feed": "square_feed",
        "Facebook Feed": "landscape_feed",
        "Facebook Stories": "portrait_story",
        "Reels": "portrait_story",
    }
    formats = set()
    for platform in persona.get("platforms", []):
        fmt = platform_to_format.get(platform)
        if fmt:
            formats.add(fmt)
    return sorted(formats) if formats else ["square_feed"]


def generate_variant(
    topic: dict, persona: dict, style: dict
) -> CreativeVariant:
    """Generate a single creative variant for one Topic × Persona × Style."""
    variant_id = f"{topic['id']}__{persona['id']}__{style['id']}"

    return CreativeVariant(
        variant_id=variant_id,
        topic=topic,
        persona=persona,
        style=style,
        image_description=_build_image_description(topic, persona, style),
        primary_text=_build_primary_text(topic, persona),
        headline=_build_headline(topic, persona),
        description=_build_description(topic, persona),
        cta=_pick_cta(topic, persona),
        recommended_formats=_pick_formats(persona, style),
    )


def generate_full_matrix(
    topics: list[dict] | None = None,
    personas: list[dict] | None = None,
    styles: list[dict] | None = None,
) -> list[CreativeVariant]:
    """Generate every combination of Topic × Persona × Style."""
    topics = topics or TOPICS
    personas = personas or PERSONAS
    styles = styles or VISUAL_STYLES

    variants = []
    for topic, persona, style in itertools.product(topics, personas, styles):
        variants.append(generate_variant(topic, persona, style))
    return variants


def filter_matrix(
    variants: list[CreativeVariant],
    topic_id: str | None = None,
    persona_id: str | None = None,
    style_id: str | None = None,
) -> list[CreativeVariant]:
    """Filter the matrix by any axis."""
    result = variants
    if topic_id:
        result = [v for v in result if v.topic["id"] == topic_id]
    if persona_id:
        result = [v for v in result if v.persona["id"] == persona_id]
    if style_id:
        result = [v for v in result if v.style["id"] == style_id]
    return result


def get_best_variants(
    variants: list[CreativeVariant],
) -> list[CreativeVariant]:
    """Return variants where visual style best matches the topic's emotional driver."""
    style_affinity = {
        "confidence": ["clean_modern", "dark_premium"],
        "trust": ["student_lifestyle", "clean_modern"],
        "aspiration": ["results_showcase", "dark_premium"],
        "safety": ["clean_modern", "student_lifestyle"],
        "urgency": ["urgent_bold", "dark_premium"],
        "convenience": ["clean_modern", "student_lifestyle"],
    }
    best = []
    for v in variants:
        driver = v.topic.get("emotional_driver", "")
        good_styles = style_affinity.get(driver, [])
        if v.style["id"] in good_styles:
            best.append(v)
    return best


def export_matrix_markdown(variants: list[CreativeVariant]) -> str:
    """Export the full matrix as a markdown document."""
    lines = [
        f"# Creative Matrix — {BRAND['company_name']}",
        f"**Total variants:** {len(variants)}",
        "",
    ]

    # Group by topic
    topics_seen: dict[str, list[CreativeVariant]] = {}
    for v in variants:
        topics_seen.setdefault(v.topic["id"], []).append(v)

    for topic_id, topic_variants in topics_seen.items():
        topic_name = topic_variants[0].topic["name"]
        lines.append(f"## Topic: {topic_name}")
        lines.append("")

        for v in topic_variants:
            lines.append(
                f"### {v.persona['name']} × {v.style['name']}"
            )
            lines.append(f"**ID:** `{v.variant_id}`")
            lines.append(f"**Formats:** {', '.join(v.recommended_formats)}")
            lines.append("")
            lines.append(f"**Headline:** {v.headline}")
            lines.append(f"**Primary Text:** {v.primary_text}")
            lines.append(f"**Description:** {v.description}")
            lines.append(f"**CTA:** {v.cta}")
            lines.append("")
            lines.append("**Image Description:**")
            lines.append(v.image_description)
            lines.append("")
            lines.append("---")
            lines.append("")

    return "\n".join(lines)


# =============================================================================
# MAIN — Demonstration
# =============================================================================

if __name__ == "__main__":
    matrix = generate_full_matrix()
    print(f"Total creative variants: {len(matrix)}")
    print(f"  ({len(TOPICS)} topics × {len(PERSONAS)} personas × {len(VISUAL_STYLES)} styles)")
    print()

    # Show the best-fit variants
    best = get_best_variants(matrix)
    print(f"Best-fit variants (style matches topic emotion): {len(best)}")
    print()

    # Print a sample of 5 best-fit variants
    for v in best[:5]:
        print(f"{'=' * 70}")
        print(f"ID:       {v.variant_id}")
        print(f"Topic:    {v.topic['name']}")
        print(f"Persona:  {v.persona['name']}")
        print(f"Style:    {v.style['name']}")
        print(f"Formats:  {', '.join(v.recommended_formats)}")
        print(f"Headline: {v.headline}")
        print(f"CTA:      {v.cta}")
        print(f"Primary:  {v.primary_text}")
        print()
        print("Image Description:")
        print(v.image_description)
        print()

    # Summary by axis
    print(f"{'=' * 70}")
    print("MATRIX SUMMARY")
    print(f"{'=' * 70}")
    print(f"\nTopics ({len(TOPICS)}):")
    for t in TOPICS:
        count = len(filter_matrix(matrix, topic_id=t["id"]))
        print(f"  - {t['name']}: {count} variants")

    print(f"\nPersonas ({len(PERSONAS)}):")
    for p in PERSONAS:
        count = len(filter_matrix(matrix, persona_id=p["id"]))
        print(f"  - {p['name']}: {count} variants")

    print(f"\nVisual Styles ({len(VISUAL_STYLES)}):")
    for s in VISUAL_STYLES:
        count = len(filter_matrix(matrix, style_id=s["id"]))
        print(f"  - {s['name']}: {count} variants")
