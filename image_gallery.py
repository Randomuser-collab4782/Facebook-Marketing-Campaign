"""
Local Image Gallery for T&N IB Education — Facebook Marketing
=============================================================
Serves a browser-based gallery of all generated ad images, grouped by
topic and persona.  Each image has a delete button so you can quickly
cull unwanted variants.

Usage
-----
    python image_gallery.py                     # default: ./generated_images on port 8899
    python image_gallery.py --port 9000         # custom port
    python image_gallery.py --images ./my_imgs  # custom image directory
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from brand_constants import COLOURS, BRAND, FONTS
from creative_matrix import TOPICS, PERSONAS, VISUAL_STYLES

# =============================================================================
# LOOKUPS — human-readable labels keyed by ID
# =============================================================================

TOPIC_LABELS = {t["id"]: t["name"] for t in TOPICS}
PERSONA_LABELS = {p["id"]: p["name"] for p in PERSONAS}
STYLE_LABELS = {s["id"]: s["name"] for s in VISUAL_STYLES}

DEFAULT_IMAGE_DIR = Path("generated_images")
DEFAULT_PORT = 8899


# =============================================================================
# IMAGE SCANNER
# =============================================================================


def scan_images(image_dir: Path) -> dict[str, dict[str, list[dict]]]:
    """Scan the image directory and return images grouped by topic > persona.

    Returns:
        {topic_id: {persona_id: [{filename, style_id, style_label, path}, ...]}}
    """
    grouped: dict[str, dict[str, list[dict]]] = {}

    if not image_dir.is_dir():
        return grouped

    for png in sorted(image_dir.glob("*.png")):
        parts = png.stem.split("__")
        if len(parts) != 3:
            continue

        topic_id, persona_id, style_id = parts

        entry = {
            "filename": png.name,
            "topic_id": topic_id,
            "persona_id": persona_id,
            "style_id": style_id,
            "topic_label": TOPIC_LABELS.get(topic_id, topic_id),
            "persona_label": PERSONA_LABELS.get(persona_id, persona_id),
            "style_label": STYLE_LABELS.get(style_id, style_id),
        }

        grouped.setdefault(topic_id, {}).setdefault(persona_id, []).append(entry)

    return grouped


def count_images(grouped: dict) -> int:
    return sum(
        len(imgs)
        for personas in grouped.values()
        for imgs in personas.values()
    )


# =============================================================================
# HTML BUILDER
# =============================================================================


def build_html(image_dir: Path) -> str:
    """Build the full gallery HTML page."""
    grouped = scan_images(image_dir)
    total = count_images(grouped)

    # CSS colours from brand constants
    c = COLOURS
    heading_font = FONTS["heading"]["family"]
    body_font = FONTS["body"]["family"]

    cards_html = []

    if not grouped:
        cards_html.append(
            '<div class="empty-state">'
            "<h2>No images found</h2>"
            f"<p>Generate images first with <code>python generate_images.py</code>, "
            f"then refresh this page.</p>"
            f"<p>Looking in: <code>{image_dir.resolve()}</code></p>"
            "</div>"
        )
    else:
        # Maintain the order from TOPICS / PERSONAS
        topic_order = [t["id"] for t in TOPICS]
        persona_order = [p["id"] for p in PERSONAS]

        for topic_id in topic_order:
            if topic_id not in grouped:
                continue

            topic_label = TOPIC_LABELS.get(topic_id, topic_id)
            persona_groups = grouped[topic_id]
            topic_count = sum(len(v) for v in persona_groups.values())

            cards_html.append(
                f'<div class="topic-section" id="topic-{topic_id}">'
                f'<div class="topic-header">'
                f"<h2>{topic_label}</h2>"
                f'<span class="badge">{topic_count} images</span>'
                f"</div>"
            )

            for persona_id in persona_order:
                if persona_id not in persona_groups:
                    continue

                images = persona_groups[persona_id]
                persona_label = PERSONA_LABELS.get(persona_id, persona_id)

                cards_html.append(
                    f'<div class="persona-group">'
                    f'<h3>{persona_label} <span class="persona-count">({len(images)})</span></h3>'
                    f'<div class="image-grid">'
                )

                for img in images:
                    fname = img["filename"]
                    style_label = img["style_label"]
                    cards_html.append(
                        f'<div class="card" id="card-{fname}" data-filename="{fname}">'
                        f'<div class="card-img-wrap">'
                        f'<img src="/images/{fname}" alt="{fname}" loading="lazy" />'
                        f"</div>"
                        f'<div class="card-info">'
                        f'<span class="style-tag">{style_label}</span>'
                        f'<button class="delete-btn" onclick="deleteImage(\'{fname}\')" '
                        f'title="Delete this image">Delete</button>'
                        f"</div>"
                        f"</div>"
                    )

                cards_html.append("</div></div>")  # close grid + persona-group

            cards_html.append("</div>")  # close topic-section

    body = "\n".join(cards_html)

    # --- Topic nav pills ---
    nav_pills = []
    for t in TOPICS:
        if t["id"] in grouped:
            nav_pills.append(
                f'<a class="nav-pill" href="#topic-{t["id"]}">{TOPIC_LABELS[t["id"]]}</a>'
            )
    nav_html = "\n".join(nav_pills)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Ad Gallery — {BRAND["company_name"]}</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family={heading_font}:wght@600;700&family={body_font}:wght@400;500&display=swap" rel="stylesheet" />
<style>
  :root {{
    --primary:    {c["primary"]};
    --secondary:  {c["secondary"]};
    --accent:     {c["accent"]};
    --bg:         {c["background"]};
    --bg-dark:    {c["background_dark"]};
    --text:       {c["text_primary"]};
    --text-muted: {c["text_secondary"]};
    --success:    {c["success"]};
    --error:      {c["error"]};
  }}

  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: '{body_font}', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.5;
  }}

  /* ---- Top bar ---- */
  .top-bar {{
    background: var(--primary);
    color: #fff;
    padding: 1.25rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 8px rgba(0,0,0,.25);
  }}
  .top-bar h1 {{
    font-family: '{heading_font}', sans-serif;
    font-weight: 700;
    font-size: 1.35rem;
    letter-spacing: -0.02em;
  }}
  .top-bar .stats {{
    font-size: 0.9rem;
    opacity: 0.85;
  }}
  .top-bar .stats strong {{ color: var(--accent); }}

  /* ---- Nav pills ---- */
  .nav-bar {{
    background: var(--bg-dark);
    padding: 0.75rem 2rem;
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    position: sticky;
    top: 60px;
    z-index: 99;
  }}
  .nav-pill {{
    display: inline-block;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    color: #ccc;
    text-decoration: none;
    font-size: 0.82rem;
    font-weight: 500;
    transition: background 0.2s, color 0.2s;
  }}
  .nav-pill:hover {{
    background: var(--secondary);
    color: #fff;
  }}

  /* ---- Main content ---- */
  .container {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
  }}

  /* ---- Topic sections ---- */
  .topic-section {{
    margin-bottom: 3rem;
  }}
  .topic-header {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.25rem;
    padding-bottom: 0.6rem;
    border-bottom: 3px solid var(--secondary);
  }}
  .topic-header h2 {{
    font-family: '{heading_font}', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: var(--primary);
  }}
  .badge {{
    background: var(--secondary);
    color: #fff;
    padding: 0.2rem 0.65rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
  }}

  /* ---- Persona groups ---- */
  .persona-group {{
    margin-bottom: 2rem;
  }}
  .persona-group h3 {{
    font-family: '{heading_font}', sans-serif;
    font-weight: 600;
    font-size: 1.05rem;
    color: var(--text);
    margin-bottom: 0.75rem;
  }}
  .persona-count {{
    color: var(--text-muted);
    font-weight: 400;
  }}

  /* ---- Image grid ---- */
  .image-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 1rem;
  }}

  /* ---- Card ---- */
  .card {{
    background: #fff;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,.1);
    transition: transform 0.15s, box-shadow 0.15s, opacity 0.3s;
  }}
  .card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(0,0,0,.15);
  }}
  .card.removing {{
    opacity: 0;
    transform: scale(0.9);
    transition: opacity 0.3s, transform 0.3s;
  }}
  .card-img-wrap {{
    aspect-ratio: 1 / 1;
    overflow: hidden;
    background: #e5e7eb;
    cursor: pointer;
  }}
  .card-img-wrap img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}
  .card-info {{
    padding: 0.55rem 0.7rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .style-tag {{
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--text-muted);
  }}

  /* ---- Delete button ---- */
  .delete-btn {{
    background: none;
    border: 1.5px solid var(--error);
    color: var(--error);
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
  }}
  .delete-btn:hover {{
    background: var(--error);
    color: #fff;
  }}

  /* ---- Lightbox overlay ---- */
  .lightbox {{
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,.85);
    z-index: 200;
    align-items: center;
    justify-content: center;
    cursor: zoom-out;
  }}
  .lightbox.active {{
    display: flex;
  }}
  .lightbox img {{
    max-width: 90vw;
    max-height: 90vh;
    border-radius: 8px;
    box-shadow: 0 8px 32px rgba(0,0,0,.5);
  }}

  /* ---- Empty state ---- */
  .empty-state {{
    text-align: center;
    padding: 4rem 2rem;
    color: var(--text-muted);
  }}
  .empty-state h2 {{
    font-family: '{heading_font}', sans-serif;
    color: var(--primary);
    margin-bottom: 0.75rem;
  }}
  .empty-state code {{
    background: #e5e7eb;
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
    font-size: 0.9rem;
  }}

  /* ---- Toast notification ---- */
  .toast {{
    position: fixed;
    bottom: 1.5rem;
    right: 1.5rem;
    background: var(--primary);
    color: #fff;
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    font-size: 0.88rem;
    font-weight: 500;
    box-shadow: 0 4px 12px rgba(0,0,0,.3);
    opacity: 0;
    transform: translateY(10px);
    transition: opacity 0.25s, transform 0.25s;
    z-index: 300;
    pointer-events: none;
  }}
  .toast.show {{
    opacity: 1;
    transform: translateY(0);
  }}
</style>
</head>
<body>

<div class="top-bar">
  <h1>{BRAND["company_name"]} — Ad Image Gallery</h1>
  <div class="stats" id="stats"><strong id="total-count">{total}</strong> images</div>
</div>

<nav class="nav-bar">
  {nav_html}
</nav>

<div class="container">
  {body}
</div>

<!-- Lightbox -->
<div class="lightbox" id="lightbox" onclick="closeLightbox()">
  <img id="lightbox-img" src="" alt="" />
</div>

<!-- Toast -->
<div class="toast" id="toast"></div>

<script>
// ---------- Lightbox ----------
document.querySelectorAll('.card-img-wrap').forEach(wrap => {{
  wrap.addEventListener('click', () => {{
    const src = wrap.querySelector('img').src;
    document.getElementById('lightbox-img').src = src;
    document.getElementById('lightbox').classList.add('active');
  }});
}});
function closeLightbox() {{
  document.getElementById('lightbox').classList.remove('active');
}}
document.addEventListener('keydown', e => {{
  if (e.key === 'Escape') closeLightbox();
}});

// ---------- Toast ----------
let toastTimer = null;
function showToast(msg) {{
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 2500);
}}

// ---------- Delete ----------
function deleteImage(filename) {{
  if (!confirm('Delete ' + filename + '?')) return;

  const card = document.getElementById('card-' + filename);
  if (card) card.classList.add('removing');

  fetch('/delete?file=' + encodeURIComponent(filename), {{ method: 'DELETE' }})
    .then(r => r.json())
    .then(data => {{
      if (data.ok) {{
        setTimeout(() => {{
          if (card) card.remove();
          updateCounts();
          showToast('Deleted ' + filename);
        }}, 300);
      }} else {{
        if (card) card.classList.remove('removing');
        alert('Delete failed: ' + (data.error || 'unknown error'));
      }}
    }})
    .catch(err => {{
      if (card) card.classList.remove('removing');
      alert('Network error: ' + err);
    }});
}}

// ---------- Live count updates ----------
function updateCounts() {{
  const total = document.querySelectorAll('.card:not(.removing)').length;
  document.getElementById('total-count').textContent = total;

  // Update per-topic badges
  document.querySelectorAll('.topic-section').forEach(sec => {{
    const n = sec.querySelectorAll('.card:not(.removing)').length;
    const badge = sec.querySelector('.badge');
    if (badge) badge.textContent = n + ' images';
    if (n === 0) sec.style.display = 'none';
  }});

  // Update per-persona counts
  document.querySelectorAll('.persona-group').forEach(grp => {{
    const n = grp.querySelectorAll('.card:not(.removing)').length;
    const counter = grp.querySelector('.persona-count');
    if (counter) counter.textContent = '(' + n + ')';
    if (n === 0) grp.style.display = 'none';
  }});
}}
</script>
</body>
</html>"""


# =============================================================================
# HTTP SERVER
# =============================================================================


class GalleryHandler(BaseHTTPRequestHandler):
    """Handles GET / (gallery), GET /images/<file> (serve PNG), DELETE /delete (remove)."""

    image_dir: Path = DEFAULT_IMAGE_DIR

    def log_message(self, fmt, *args):
        # Quieter logging — single line per request
        sys.stderr.write(f"  {self.address_string()} {fmt % args}\n")

    # ---------- Routing ----------

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/" or parsed.path == "":
            self._serve_gallery()
        elif parsed.path.startswith("/images/"):
            self._serve_image(parsed.path[len("/images/"):])
        else:
            self._send(404, "text/plain", b"Not found")

    def do_DELETE(self):
        parsed = urlparse(self.path)
        if parsed.path == "/delete":
            qs = parse_qs(parsed.query)
            filenames = qs.get("file", [])
            if filenames:
                self._handle_delete(filenames[0])
            else:
                self._send_json(400, {"ok": False, "error": "Missing ?file= parameter"})
        else:
            self._send(404, "text/plain", b"Not found")

    # ---------- Handlers ----------

    def _serve_gallery(self):
        html = build_html(self.image_dir)
        self._send(200, "text/html; charset=utf-8", html.encode())

    def _serve_image(self, filename: str):
        # Prevent path traversal
        safe_name = Path(filename).name
        filepath = self.image_dir / safe_name

        if not filepath.is_file() or filepath.suffix.lower() != ".png":
            self._send(404, "text/plain", b"Image not found")
            return

        data = filepath.read_bytes()
        self._send(200, "image/png", data)

    def _handle_delete(self, filename: str):
        safe_name = Path(filename).name
        filepath = self.image_dir / safe_name

        if not filepath.is_file():
            self._send_json(404, {"ok": False, "error": "File not found"})
            return

        try:
            filepath.unlink()
            self._send_json(200, {"ok": True, "deleted": safe_name})
        except OSError as exc:
            self._send_json(500, {"ok": False, "error": str(exc)})

    # ---------- Response helpers ----------

    def _send(self, status: int, content_type: str, body: bytes):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, obj: dict):
        body = json.dumps(obj).encode()
        self._send(status, "application/json", body)


# =============================================================================
# CLI
# =============================================================================


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Local gallery server for generated ad images.",
    )
    parser.add_argument(
        "--images",
        type=str,
        default=str(DEFAULT_IMAGE_DIR),
        help=f"Directory containing generated PNGs (default: {DEFAULT_IMAGE_DIR})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port to serve on (default: {DEFAULT_PORT})",
    )
    args = parser.parse_args(argv)

    image_dir = Path(args.images)
    GalleryHandler.image_dir = image_dir

    grouped = scan_images(image_dir)
    total = count_images(grouped)

    server = HTTPServer(("0.0.0.0", args.port), GalleryHandler)

    print()
    print(f"  T&N IB Education — Ad Image Gallery")
    print(f"  {'=' * 46}")
    print(f"  Images:  {image_dir.resolve()}  ({total} found)")
    print(f"  Server:  http://localhost:{args.port}")
    print()
    print(f"  Open the URL above in your browser.")
    print(f"  Press Ctrl+C to stop.")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
