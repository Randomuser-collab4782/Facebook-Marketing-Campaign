"""
Quickstart — T&N IB Education Marketing Campaign
=================================================
Walks through each step of the campaign pipeline:
  1. Verify Gemini API connection
  2. Generate ad copy samples
  3. Export creative briefs
  4. Generate ad images via Gemini
  5. Launch the image review gallery

Usage
-----
    # Set your API key first (or put it in .env)
    export GEMINI_API_KEY="your-key"

    # Run the quickstart
    python quickstart.py

    # Skip image generation (briefs + copy only)
    python quickstart.py --skip-images

    # Generate only a few test images
    python quickstart.py --image-limit 3
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# .env loader (same as generate_images.py)
# ---------------------------------------------------------------------------
_env_path = Path(__file__).resolve().parent / ".env"
if _env_path.exists():
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _key, _, _val = _line.partition("=")
                _val = _val.strip().strip("\"'")
                os.environ.setdefault(_key.strip(), _val)

# ---------------------------------------------------------------------------
# Imports from the campaign modules
# ---------------------------------------------------------------------------
from brand_constants import BRAND, COLOURS, CAMPAIGN_THEMES, TARGET_AUDIENCE
from ad_copy_generator import generate_ad_copy, generate_variations
from audience_targeting import AUDIENCE_SEGMENTS, estimate_daily_budget
from campaign_calendar import get_active_campaigns, export_calendar_markdown
from creative_briefs import generate_all_briefs, export_brief_markdown
from creative_matrix import get_best_variants, generate_full_matrix
from generate_images import select_variants, run as run_image_generation


# ---------------------------------------------------------------------------
# Step helpers
# ---------------------------------------------------------------------------

def _header(step: int, title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  STEP {step}: {title}")
    print(f"{'=' * 60}\n")


def step_1_verify_api() -> str:
    """Check the Gemini API key is present and test a lightweight call."""
    _header(1, "VERIFY GEMINI API CONNECTION")

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("  [ERROR] GEMINI_API_KEY is not set.")
        print("  Set it via environment variable or create a .env file:")
        print('    echo \'GEMINI_API_KEY=your-key\' > .env')
        print("  See .env.example for the format.")
        sys.exit(1)

    # Quick health-check: list models endpoint
    import requests
    url = "https://generativelanguage.googleapis.com/v1beta/models?key=" + api_key
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            models = resp.json().get("models", [])
            gemini_models = [m["name"] for m in models if "gemini" in m.get("name", "").lower()]
            print(f"  [OK] API key is valid. Found {len(gemini_models)} Gemini models.")
            for m in gemini_models[:5]:
                print(f"       - {m}")
            if len(gemini_models) > 5:
                print(f"       ... and {len(gemini_models) - 5} more")
        elif resp.status_code in (400, 403):
            print(f"  [WARN] API key rejected (HTTP {resp.status_code}).")
            print("  Check your key at: https://aistudio.google.com/apikey")
            print("  Continuing with non-API steps (ad copy, briefs, calendar)...")
        else:
            print(f"  [WARN] Unexpected status {resp.status_code}. Continuing anyway...")
    except requests.exceptions.RequestException as exc:
        print(f"  [WARN] Could not reach Gemini API: {exc}")
        print("  Continuing — image generation may fail if the network is unavailable.")

    return api_key


def step_2_ad_copy() -> None:
    """Generate sample ad copy across themes and frameworks."""
    _header(2, "GENERATE AD COPY SAMPLES")

    for theme in CAMPAIGN_THEMES:
        theme_id = theme["id"]
        variations = generate_variations(theme_id=theme_id, num_variations=2)
        print(f"  Theme: {theme['name']}")
        for v in variations:
            fw = v['metadata']['framework'].upper()
            print(f"    [{fw}] {v['primary_text'][:80]}...")
        print()

    print(f"  [OK] Generated copy samples for {len(CAMPAIGN_THEMES)} campaign themes.")


def step_3_briefs() -> None:
    """Generate and export creative briefs."""
    _header(3, "EXPORT CREATIVE BRIEFS")

    briefs_dir = Path("briefs")
    briefs_dir.mkdir(exist_ok=True)

    briefs = generate_all_briefs()
    for brief in briefs:
        md = export_brief_markdown(brief)
        filepath = briefs_dir / f"brief_{brief.campaign_theme['id']}.md"
        filepath.write_text(md)
        print(f"  [OK] {filepath}")

    print(f"\n  {len(briefs)} briefs exported to {briefs_dir.resolve()}/")


def step_4_images(api_key: str, limit: int | None = None) -> Path:
    """Generate ad images via Gemini."""
    _header(4, "GENERATE AD IMAGES VIA GEMINI")

    output_dir = Path("generated_images")
    effective_limit = limit or 5  # Default to 5 for quickstart

    variants = select_variants(best_fit_only=True, limit=effective_limit)
    print(f"  Generating {len(variants)} images (limit={effective_limit})...")
    print(f"  Output: {output_dir.resolve()}/")
    print()

    results = run_image_generation(
        variants=variants,
        api_key=api_key,
        output_dir=output_dir,
    )

    print(f"\n  [OK] {len(results['generated'])} images generated, "
          f"{len(results['failed'])} failed.")
    return output_dir


def step_5_gallery(image_dir: Path) -> None:
    """Launch the image review gallery."""
    _header(5, "LAUNCH IMAGE GALLERY")

    images = list(image_dir.glob("*.png")) if image_dir.exists() else []
    if not images:
        print("  No images found. Skipping gallery.")
        return

    print(f"  {len(images)} images ready for review.")
    print(f"  To launch the gallery, run:")
    print(f"    python image_gallery.py --images {image_dir}")
    print(f"  Then open http://localhost:8899 in your browser.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Quickstart guide for the T&N IB Education marketing pipeline.",
    )
    parser.add_argument(
        "--skip-images",
        action="store_true",
        default=False,
        help="Skip image generation (steps 1-3 only)",
    )
    parser.add_argument(
        "--image-limit",
        type=int,
        default=5,
        help="Max images to generate in quickstart (default: 5)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    print()
    print(f"  T&N IB Education — Marketing Campaign Quickstart")
    print(f"  {'~' * 50}")
    print(f"  Brand:   {BRAND['company_name']}")
    print(f"  Tagline: {BRAND['tagline']}")
    print()

    # Step 1: Verify API
    api_key = step_1_verify_api()

    # Step 2: Ad copy
    step_2_ad_copy()

    # Step 3: Briefs
    step_3_briefs()

    # Step 4: Images
    if args.skip_images:
        print(f"\n  [SKIP] Image generation skipped (--skip-images).")
        image_dir = Path("generated_images")
    else:
        image_dir = step_4_images(api_key, limit=args.image_limit)

    # Step 5: Gallery instructions
    step_5_gallery(image_dir)

    print(f"\n{'=' * 60}")
    print(f"  QUICKSTART COMPLETE")
    print(f"{'=' * 60}")
    print()
    print("  Next steps:")
    print("    1. Review generated images in the gallery")
    print("    2. Upload winning creatives to Meta Ads Manager")
    print("    3. Use audience_targeting.py segments for ad set setup")
    print("    4. Follow campaign_calendar.py for scheduling")
    print()


if __name__ == "__main__":
    main()
