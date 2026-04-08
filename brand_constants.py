"""
Brand Constants for T&N IB Education - Facebook Marketing Campaign
==================================================================
Defines all brand identity elements, target audience, selling points,
and ad format specifications for Facebook/Instagram ad generation.

Based on brand-building patterns from agentkits-marketing and
tailored for IB tuition + AI-assisted internal assessment services.
"""

# =============================================================================
# BRAND IDENTITY
# =============================================================================

BRAND = {
    "company_name": "T&N IB Education",
    "website": "https://tandnibeducation.com",
    "tagline": "Ace Your IB With AI-Powered Guidance",
    "short_description": (
        "Expert IB tuition across all subjects — with AI-powered Internal "
        "Assessment support as our speciality. From general exam prep to "
        "IA mastery, we help students achieve top grades."
    ),
    "mission": (
        "To empower IB students worldwide with personalised tutoring across "
        "every subject, with industry-leading AI-driven tools that simplify "
        "Internal Assessments."
    ),
    "services": {
        "general_tuition": (
            "1-on-1 tutoring for all IB Diploma subjects — Maths, Sciences, "
            "Humanities, Languages, and more. Exam prep, coursework help, "
            "and concept mastery."
        ),
        "speciality_ia": (
            "AI-powered Internal Assessment support — topic selection, "
            "structure, analysis, and refinement. Our flagship offering."
        ),
    },
    "voice": {
        "tone": "Confident, supportive, and approachable",
        "formality": "Semi-formal — academic credibility with a friendly edge",
        "personality": [
            "Knowledgeable mentor",
            "Encouraging coach",
            "Tech-savvy guide",
        ],
    },
}

# =============================================================================
# COLOUR PALETTE
# =============================================================================

COLOURS = {
    "primary": "#1E3A5F",       # Deep navy — trust, academic authority
    "secondary": "#2E86AB",     # Bright teal — innovation, freshness
    "accent": "#F6AE2D",        # Warm amber — energy, optimism, CTA highlight
    "background": "#F9FAFB",    # Off-white — clean, readable
    "background_dark": "#0F1B2D",  # Dark navy — for dark-mode / contrast sections
    "text_primary": "#1A1A2E",  # Near-black — body text
    "text_secondary": "#6B7280", # Muted grey — supporting text
    "success": "#10B981",       # Green — score improvements, positive metrics
    "error": "#EF4444",         # Red — urgency accents, deadline reminders
}

# =============================================================================
# TYPOGRAPHY
# =============================================================================

FONTS = {
    "heading": {
        "family": "Poppins",
        "weights": ["600", "700"],
        "fallback": "sans-serif",
    },
    "body": {
        "family": "Inter",
        "weights": ["400", "500"],
        "fallback": "sans-serif",
    },
    "accent": {
        "family": "Space Grotesk",
        "weights": ["500", "700"],
        "fallback": "monospace",
        "usage": "Stats, scores, data callouts",
    },
}

# =============================================================================
# KEY SELLING POINTS
# =============================================================================

SELLING_POINTS = [
    {
        "headline": "AI-Powered IA Support",
        "detail": (
            "Our AI tools help you brainstorm topics, structure your IA, "
            "and refine your analysis — while keeping every word authentically yours."
        ),
        "icon": "brain-circuit",
    },
    {
        "headline": "Expert IB Tutors",
        "detail": (
            "Learn from tutors who have taught and examined IB curricula. "
            "Personalised 1-on-1 sessions tailored to your subject and level."
        ),
        "icon": "graduation-cap",
    },
    {
        "headline": "All IB Subjects Covered",
        "detail": (
            "From Maths AA/AI and Sciences to English, Economics, and more — "
            "get help with any IB Diploma subject and assessment type."
        ),
        "icon": "book-open",
    },
    {
        "headline": "Academic Integrity First",
        "detail": (
            "Our AI guides your thinking — it never writes your work. "
            "Fully aligned with IB academic integrity policies."
        ),
        "icon": "shield-check",
    },
    {
        "headline": "Proven Score Improvements",
        "detail": (
            "Students using our platform see an average improvement of "
            "2+ points on their IA scores across all subjects."
        ),
        "icon": "trending-up",
    },
    {
        "headline": "General IB Tuition",
        "detail": (
            "Beyond IAs — get 1-on-1 tutoring for exams, coursework, and "
            "concept mastery across every IB Diploma subject. Maths, Sciences, "
            "Humanities, Languages, and more."
        ),
        "icon": "book-open-check",
    },
]

# =============================================================================
# TARGET AUDIENCE
# =============================================================================

TARGET_AUDIENCE = {
    "primary": {
        "label": "IB Diploma Students",
        "age_range": "15-19",
        "description": (
            "Current IB Diploma Programme students (HL and SL) who need "
            "help with Internal Assessments, Extended Essays, and exam prep."
        ),
        "pain_points": [
            "Struggling to choose an IA topic",
            "Unsure how to structure analysis and evaluation",
            "Time pressure from multiple IAs across subjects",
            "Fear of low IA scores dragging down final grade",
            "Confusion about how to use AI tools ethically",
        ],
        "facebook_targeting": {
            "interests": [
                "International Baccalaureate",
                "IB Diploma Programme",
                "Study tips",
                "Academic success",
            ],
            "behaviors": ["Education-related searches", "Online learning"],
        },
    },
    "secondary": {
        "label": "Parents of IB Students",
        "age_range": "35-55",
        "description": (
            "Parents who want to invest in their child's academic success "
            "and are looking for reliable, ethical tutoring support."
        ),
        "pain_points": [
            "Child is stressed about IB workload",
            "Worried about university admission competitiveness",
            "Want to ensure ethical use of AI in their child's work",
            "Looking for trustworthy tutoring that delivers results",
        ],
        "facebook_targeting": {
            "interests": [
                "Parenting",
                "International Baccalaureate",
                "Education",
                "University admissions",
            ],
            "behaviors": ["Parents with teenagers", "Education spenders"],
        },
    },
    "tertiary": {
        "label": "IB Coordinators & Teachers",
        "age_range": "28-55",
        "description": (
            "IB school staff who may recommend resources to students "
            "or are interested in AI-integrated teaching support."
        ),
    },
}

# =============================================================================
# AD FORMATS — Facebook & Instagram Specifications
# =============================================================================
# Following Meta's recommended specs (March 2026)

AD_FORMATS = {
    "square_feed": {
        "label": "Square — Instagram/Facebook Feed",
        "width": 1080,
        "height": 1080,
        "aspect_ratio": "1:1",
        "platforms": ["Instagram Feed", "Facebook Feed", "Facebook Marketplace"],
        "max_text_ratio": 0.20,
        "safe_zone_margin": 60,  # px from edges for text/logo
        "file_formats": ["jpg", "png"],
        "max_file_size_mb": 30,
    },
    "portrait_story": {
        "label": "Portrait — Instagram/Facebook Stories & Reels",
        "width": 1080,
        "height": 1920,
        "aspect_ratio": "9:16",
        "platforms": ["Instagram Stories", "Facebook Stories", "Reels"],
        "max_text_ratio": 0.20,
        "safe_zone_top": 250,    # px — avoid profile/UI overlap
        "safe_zone_bottom": 340,  # px — avoid CTA button overlap
        "file_formats": ["jpg", "png", "mp4"],
        "max_file_size_mb": 30,
    },
    "landscape_feed": {
        "label": "Landscape — Facebook Feed / Link Ads",
        "width": 1200,
        "height": 628,
        "aspect_ratio": "1.91:1",
        "platforms": ["Facebook Feed", "Audience Network", "Messenger"],
        "max_text_ratio": 0.20,
        "safe_zone_margin": 50,
        "file_formats": ["jpg", "png"],
        "max_file_size_mb": 30,
    },
    "vertical_feed": {
        "label": "Vertical — Facebook/Instagram Feed",
        "width": 1080,
        "height": 1350,
        "aspect_ratio": "4:5",
        "platforms": ["Instagram Feed", "Facebook Feed"],
        "max_text_ratio": 0.20,
        "safe_zone_margin": 60,
        "file_formats": ["jpg", "png"],
        "max_file_size_mb": 30,
    },
    "carousel_card": {
        "label": "Carousel Card — Feed",
        "width": 1080,
        "height": 1080,
        "aspect_ratio": "1:1",
        "platforms": ["Instagram Feed", "Facebook Feed"],
        "max_cards": 10,
        "min_cards": 2,
        "file_formats": ["jpg", "png"],
        "max_file_size_mb": 30,
    },
}

# =============================================================================
# CAMPAIGN THEMES — Pre-defined content angles for ad generation
# =============================================================================

CAMPAIGN_THEMES = [
    {
        "id": "ia_kickstart",
        "name": "IA Kickstart",
        "hook": "Your IA doesn't have to be stressful.",
        "angle": "Position AI-assisted IA support as the smart, ethical shortcut.",
        "cta": "Get Started Free",
        "best_for": ["square_feed", "portrait_story"],
    },
    {
        "id": "score_boost",
        "name": "Score Boost",
        "hook": "From a 4 to a 7 — real students, real results.",
        "angle": "Social proof with score improvement testimonials.",
        "cta": "See How They Did It",
        "best_for": ["square_feed", "carousel_card"],
    },
    {
        "id": "ai_ethics",
        "name": "AI Done Right",
        "hook": "Use AI the IB-approved way.",
        "angle": "Address parent/student anxiety about AI and academic integrity.",
        "cta": "Learn Our Approach",
        "best_for": ["landscape_feed", "square_feed"],
    },
    {
        "id": "subject_spotlight",
        "name": "Subject Spotlight",
        "hook": "Struggling with your {subject} IA?",
        "angle": "Subject-specific ads targeting individual IB courses.",
        "cta": "Get Expert Help Now",
        "best_for": ["portrait_story", "vertical_feed"],
    },
    {
        "id": "deadline_urgency",
        "name": "Deadline Crunch",
        "hook": "IA deadline approaching? We've got you.",
        "angle": "Urgency-driven ads timed around IB assessment deadlines.",
        "cta": "Book a Session Today",
        "best_for": ["portrait_story", "square_feed"],
    },
    {
        "id": "general_tuition",
        "name": "General IB Tuition",
        "hook": "Expert IB tutors for every subject.",
        "angle": (
            "Promote broad 1-on-1 IB tutoring — exams, coursework, concept "
            "mastery — with IA support as the standout speciality."
        ),
        "cta": "Book a Session Today",
        "best_for": ["square_feed", "carousel_card", "landscape_feed"],
    },
]

# =============================================================================
# META AD COPY CONSTRAINTS
# =============================================================================

AD_COPY_LIMITS = {
    "primary_text": {"max_chars": 125, "recommended_chars": 80},
    "headline": {"max_chars": 40, "recommended_chars": 27},
    "description": {"max_chars": 30, "recommended_chars": 27},
    "cta_options": [
        "Learn More",
        "Sign Up",
        "Get Started",
        "Book Now",
        "Contact Us",
        "Get Offer",
    ],
}

# =============================================================================
# BUDGET STRATEGY (70-20-10 Rule from paid-advertising best practices)
# =============================================================================

BUDGET_STRATEGY = {
    "proven": {
        "allocation": 0.70,
        "description": "Proven campaigns with strong ROAS",
    },
    "testing": {
        "allocation": 0.20,
        "description": "Optimisation tests — new creatives, audiences, copy",
    },
    "experimental": {
        "allocation": 0.10,
        "description": "New channels, audiences, or bold creative experiments",
    },
    "target_roas": 3.0,  # 3:1 minimum return on ad spend
    "optimisation_cadence": "weekly",
    "creative_variations_per_campaign": 5,  # Test 3-5 variations
}

# =============================================================================
# IB SUBJECTS — For subject-specific ad targeting
# =============================================================================

IB_SUBJECTS = {
    "group_1": ["English A: Literature", "English A: Language & Literature"],
    "group_2": ["French B", "Spanish B", "Mandarin B"],
    "group_3": ["Economics", "Business Management", "Psychology", "History", "Geography"],
    "group_4": ["Physics", "Chemistry", "Biology", "Computer Science", "ESS"],
    "group_5": ["Mathematics AA", "Mathematics AI"],
    "group_6": ["Visual Arts", "Music", "Theatre", "Film"],
    "core": ["Extended Essay", "Theory of Knowledge"],
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def get_ad_dimensions(format_key: str) -> tuple[int, int]:
    """Return (width, height) for a given ad format."""
    fmt = AD_FORMATS[format_key]
    return (fmt["width"], fmt["height"])


def get_colour(name: str) -> str:
    """Return hex colour by name."""
    return COLOURS[name]


def get_audience(segment: str = "primary") -> dict:
    """Return target audience segment."""
    return TARGET_AUDIENCE[segment]
