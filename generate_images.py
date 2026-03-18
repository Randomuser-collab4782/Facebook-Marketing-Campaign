"""
Image Generation Script for T&N IB Education — Facebook Marketing
=================================================================
Pulls creative variants from the creative matrix, builds detailed image
prompts enriched with brand constants, and sends them to the Google
Gemini API (Imagen) to generate PNG ad images.

Usage
-----
    # Generate images for ALL best-fit variants (style matches topic emotion)
    python generate_images.py

    # Limit to N images
    python generate_images.py --limit 10

    # Filter by topic / persona / style
    python generate_images.py --topic ai_ia_support --persona stressed_student

    # Use a specific Gemini model
    python generate_images.py --model gemini-2.0-flash-exp

    # Custom output directory
    python generate_images.py --output ./campaign_images

Environment
-----------
Set your API key before running:

    export GEMINI_API_KEY="your-api-key-here"
"""

from __future__ import annotations

import argparse
import base64
import os
import re
import sys
import time
from pathlib import Path

import requests

# Load .env file if present (keeps API keys out of shell history)
_env_path = Path(__file__).resolve().parent / ".env"
if _env_path.exists():
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _key, _, _val = _line.partition("=")
                _val = _val.strip().strip("\"'")
                os.environ.setdefault(_key.strip(), _val)

from brand_constants import BRAND, COLOURS, FONTS, AD_FORMATS
from creative_matrix import (
    CreativeVariant,
    generate_full_matrix,
    filter_matrix,
    get_best_variants,
)

# =============================================================================
# CONFIGURATION
# =============================================================================

DEFAULT_OUTPUT_DIR = Path("generated_images")
DEFAULT_MODEL = "gemini-2.0-flash-exp"
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

# Rate-limit: pause between API calls to stay within quotas
REQUEST_DELAY_SECONDS = 2.0


# =============================================================================
# PROMPT BUILDER
# =============================================================================


def _colour_name(hex_code: str) -> str:
    """Return a human-readable colour description for the prompt."""
    colour_names = {
        COLOURS["primary"]: "deep navy blue (#1E3A5F)",
        COLOURS["secondary"]: "bright teal (#2E86AB)",
        COLOURS["accent"]: "warm amber/gold (#F6AE2D)",
        COLOURS["background"]: "clean off-white (#F9FAFB)",
        COLOURS["background_dark"]: "dark navy (#0F1B2D)",
        COLOURS["success"]: "vibrant green (#10B981)",
        COLOURS["error"]: "bold red (#EF4444)",
    }
    return colour_names.get(hex_code, hex_code)


def build_image_prompt(variant: CreativeVariant) -> str:
    """Convert a creative variant into a detailed Gemini image-generation prompt.

    Incorporates brand colours, visual style direction, topic visuals,
    persona mood, and enforces the "no text" / "brand colours prominent" rules.
    """
    topic = variant.topic
    persona = variant.persona
    style = variant.style

    # --- Core visual direction ---
    sections = [
        f"Create a high-quality advertising image for {BRAND['company_name']}.",
        "",
        "=== VISUAL STYLE ===",
        f"Style: {style['name']} — {style['description']}",
        f"Imagery elements: {style['imagery']}",
    ]

    if style.get("photo_style"):
        sections.append(f"Photography direction: {style['photo_style']}")

    # --- Brand colours (prominent) ---
    bg_colour = _colour_name(style["background"]) if style["background"] != "Photo-based" else "photo-based background"
    accent = _colour_name(style["accent_colour"])
    sections += [
        "",
        "=== BRAND COLOURS (must be prominently featured) ===",
        f"Primary background tone: {bg_colour}",
        f"Accent colour used for highlights and focal elements: {accent}",
        f"The T&N brand palette must dominate: deep navy ({COLOURS['primary']}), "
        f"bright teal ({COLOURS['secondary']}), and warm amber ({COLOURS['accent']}).",
        "These colours should be clearly visible in the composition — in backgrounds, "
        "gradients, accent shapes, lighting tints, or decorative elements.",
    ]

    # --- Topic-specific visual cues ---
    topic_cues = {
        "ai_ia_support": (
            "Show a futuristic AI interface element alongside a student workspace — "
            "a laptop with glowing holographic outlines or a notebook with luminous "
            "margin annotations. Convey human + AI collaboration."
        ),
        "expert_tutors": (
            "Depict a warm one-on-one tutoring moment — a mentor and student at a "
            "desk with a whiteboard or screen-share visible. Convey expertise and "
            "personal attention."
        ),
        "score_improvement": (
            "Feature an upward-trending graph or large score numbers with a visual "
            "progression (e.g. rising bars, ascending steps). Use success green "
            f"({COLOURS['success']}) for the upward elements."
        ),
        "academic_integrity": (
            "Include a prominent shield or verification badge icon, conveying trust "
            "and safety. Clean, authoritative composition."
        ),
        "deadline_support": (
            "Include a clock, calendar page, or countdown element. Convey structured "
            "urgency — help is available, not panic."
        ),
        "all_subjects": (
            "Show a mosaic or arrangement of subject icons — a flask for science, "
            "sigma for maths, a book for literature, a globe for geography. "
            "Convey breadth and variety."
        ),
    }
    sections += [
        "",
        "=== SUBJECT / TOPIC ===",
        f"Ad topic: {topic['name']} — {topic['core_message']}",
        topic_cues.get(topic["id"], ""),
    ]

    # --- Persona mood ---
    persona_moods = {
        "stressed_student": "Mood: empathetic, calming, and reassuring. Warm lighting, soft focus.",
        "ambitious_achiever": "Mood: aspirational, polished, and confident. Sharp focus, premium feel.",
        "concerned_parent": "Mood: trustworthy, professional, and reassuring. Clean, authoritative.",
        "proactive_parent": "Mood: confident, forward-thinking, and investment-minded. Modern, clean.",
        "last_minute_student": "Mood: urgent but supportive. Dynamic composition, warm but energetic lighting.",
    }
    sections += [
        "",
        "=== MOOD & AUDIENCE ===",
        f"Target: {persona['name']} ({persona['age_range']})",
        persona_moods.get(persona["id"], ""),
    ]

    # --- Hard rules ---
    sections += [
        "",
        "=== CRITICAL RULES ===",
        "1. ABSOLUTELY NO TEXT, WORDS, LETTERS, NUMBERS, OR TYPOGRAPHY in the image. "
        "The image must be purely visual — no headlines, labels, watermarks, or captions.",
        "2. The brand colours (deep navy, bright teal, warm amber) MUST be prominently "
        "visible in the image through backgrounds, objects, lighting, or accents.",
        "3. No logos or brand marks.",
        "4. The image should work as a compelling ad visual at 1080x1080 pixels.",
        "5. Professional, high-production-quality look suitable for Facebook/Instagram ads.",
    ]

    return "\n".join(sections)


# =============================================================================
# FILENAME BUILDER
# =============================================================================


def build_filename(variant: CreativeVariant) -> str:
    """Create a descriptive filename from the variant axes."""
    parts = [
        variant.topic["id"],
        variant.persona["id"],
        variant.style["id"],
    ]
    name = "__".join(parts)
    # Sanitise for filesystem safety
    name = re.sub(r"[^a-zA-Z0-9_\-]", "_", name)
    return f"{name}.png"


# =============================================================================
# GEMINI API CALLER
# =============================================================================


def generate_image_gemini(
    prompt: str,
    api_key: str,
    model: str = DEFAULT_MODEL,
) -> bytes | None:
    """Call the Gemini API to generate an image and return raw PNG bytes.

    Uses the generateContent endpoint with responseModalities=["image"].
    Returns None on failure (logged to stderr).
    """
    url = f"{GEMINI_API_BASE}/{model}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["image"],
            "responseMimeType": "image/png",
        },
    }

    try:
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
    except requests.exceptions.RequestException as exc:
        print(f"  [ERROR] API request failed: {exc}", file=sys.stderr)
        return None

    data = resp.json()

    # Navigate Gemini response structure to extract image bytes
    try:
        candidates = data["candidates"]
        parts = candidates[0]["content"]["parts"]
        for part in parts:
            if "inlineData" in part:
                b64 = part["inlineData"]["data"]
                return base64.b64decode(b64)
        print("  [ERROR] No image data found in API response.", file=sys.stderr)
        return None
    except (KeyError, IndexError) as exc:
        print(f"  [ERROR] Unexpected response structure: {exc}", file=sys.stderr)
        # Dump a snippet for debugging
        import json
        print(f"  Response snippet: {json.dumps(data, indent=2)[:500]}", file=sys.stderr)
        return None


# =============================================================================
# PROGRESS DISPLAY
# =============================================================================


class ProgressDisplay:
    """Simple terminal progress tracker with per-item status."""

    def __init__(self, total: int) -> None:
        self.total = total
        self.current = 0
        self.successes = 0
        self.failures = 0
        self._start_time = time.time()

    def _elapsed(self) -> str:
        secs = int(time.time() - self._start_time)
        mins, secs = divmod(secs, 60)
        return f"{mins:02d}:{secs:02d}"

    def _bar(self, width: int = 30) -> str:
        filled = int(width * self.current / self.total) if self.total else 0
        return f"[{'#' * filled}{'.' * (width - filled)}]"

    def start(self) -> None:
        print()
        print(f"  T&N IB Education — Image Generation")
        print(f"  {'=' * 50}")
        print(f"  Variants to generate: {self.total}")
        print(f"  Output directory:     (see below)")
        print()

    def update(self, variant: CreativeVariant, success: bool) -> None:
        self.current += 1
        if success:
            self.successes += 1
        else:
            self.failures += 1

        status = "OK" if success else "FAIL"
        pct = int(100 * self.current / self.total) if self.total else 0

        topic_short = variant.topic["name"][:25]
        persona_short = variant.persona["name"][:22]
        style_short = variant.style["name"][:18]

        print(
            f"  {self._bar()} {pct:3d}%  "
            f"[{self.current}/{self.total}]  "
            f"{status:4s}  "
            f"{topic_short} | {persona_short} | {style_short}  "
            f"({self._elapsed()})"
        )

    def finish(self, output_dir: Path) -> None:
        print()
        print(f"  {'=' * 50}")
        print(f"  DONE  {self.successes} succeeded, {self.failures} failed  "
              f"({self._elapsed()} elapsed)")
        print(f"  Images saved to: {output_dir.resolve()}")
        print()


# =============================================================================
# MAIN PIPELINE
# =============================================================================


def select_variants(
    topic_id: str | None = None,
    persona_id: str | None = None,
    style_id: str | None = None,
    best_fit_only: bool = True,
    limit: int | None = None,
) -> list[CreativeVariant]:
    """Build the matrix and return the filtered/sorted variant list."""
    matrix = generate_full_matrix()

    if best_fit_only:
        variants = get_best_variants(matrix)
    else:
        variants = matrix

    variants = filter_matrix(
        variants,
        topic_id=topic_id,
        persona_id=persona_id,
        style_id=style_id,
    )

    if limit and limit < len(variants):
        variants = variants[:limit]

    return variants


def run(
    variants: list[CreativeVariant],
    api_key: str,
    output_dir: Path,
    model: str = DEFAULT_MODEL,
    delay: float = REQUEST_DELAY_SECONDS,
) -> dict:
    """Generate images for all provided variants.

    Returns a summary dict with counts and file paths.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    progress = ProgressDisplay(total=len(variants))
    progress.start()
    print(f"  Output directory:     {output_dir.resolve()}")
    print()

    results = {"generated": [], "failed": []}

    for i, variant in enumerate(variants):
        prompt = build_image_prompt(variant)
        filename = build_filename(variant)
        filepath = output_dir / filename

        # Call Gemini
        img_bytes = generate_image_gemini(prompt, api_key=api_key, model=model)

        if img_bytes:
            filepath.write_bytes(img_bytes)
            results["generated"].append(str(filepath))
            progress.update(variant, success=True)
        else:
            results["failed"].append(variant.variant_id)
            progress.update(variant, success=False)

        # Rate-limit pause (skip after last item)
        if i < len(variants) - 1:
            time.sleep(delay)

    progress.finish(output_dir)
    return results


# =============================================================================
# CLI
# =============================================================================


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate ad images for T&N IB Education using the Gemini API.",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default=None,
        help="Filter to a single topic ID (e.g. ai_ia_support)",
    )
    parser.add_argument(
        "--persona",
        type=str,
        default=None,
        help="Filter to a single persona ID (e.g. stressed_student)",
    )
    parser.add_argument(
        "--style",
        type=str,
        default=None,
        help="Filter to a single style ID (e.g. dark_premium)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        default=False,
        dest="all_variants",
        help="Generate ALL 150 variants (default: best-fit only ~60)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of images to generate",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Gemini model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"Output directory for PNGs (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=REQUEST_DELAY_SECONDS,
        help=f"Seconds to pause between API calls (default: {REQUEST_DELAY_SECONDS})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Print prompts without calling the API",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    # --- API key ---
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key and not args.dry_run:
        print("ERROR: Set the GEMINI_API_KEY environment variable.", file=sys.stderr)
        print("  export GEMINI_API_KEY='your-api-key-here'", file=sys.stderr)
        sys.exit(1)

    # --- Select variants ---
    variants = select_variants(
        topic_id=args.topic,
        persona_id=args.persona,
        style_id=args.style,
        best_fit_only=not args.all_variants,
        limit=args.limit,
    )

    if not variants:
        print("No variants matched your filters. Try broadening your criteria.")
        sys.exit(0)

    # --- Dry-run mode: just print prompts ---
    if args.dry_run:
        print(f"\n  DRY RUN — {len(variants)} variants selected\n")
        for v in variants:
            print(f"  {'=' * 60}")
            print(f"  File: {build_filename(v)}")
            print(f"  Topic:   {v.topic['name']}")
            print(f"  Persona: {v.persona['name']}")
            print(f"  Style:   {v.style['name']}")
            print()
            print(build_image_prompt(v))
            print()
        return

    # --- Generate ---
    output_dir = Path(args.output)
    results = run(
        variants=variants,
        api_key=api_key,
        output_dir=output_dir,
        model=args.model,
        delay=args.delay,
    )

    # --- Final summary ---
    if results["failed"]:
        print(f"  Failed variant IDs:")
        for vid in results["failed"]:
            print(f"    - {vid}")


if __name__ == "__main__":
    main()
