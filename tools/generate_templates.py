#!/usr/bin/env python3
"""Generate layered SVG design templates for each side of each pedal enclosure.

Each SVG is sized exactly to Tayda's UV-print artboard for that side, in
millimetres, and holds one named group per design layer. Open a template in
Affinity and save it as .afdesign / .aftemplate to get the layered starting point.

Artboard sizes are transcribed from `tayda-uv sides <enclosure>`, which in turn
comes from Tayda's UV printing guide:
https://www.taydaelectronics.com/uv-printing-service-guide-v1

Usage: python3 tools/generate_templates.py [output_dir]   (default: templates/)
"""

import sys
from pathlib import Path

# (width, height) in mm for side A (face), B (end) and C (side).
# Tayda's sides pair up: Lid = A, D = B, E = C.
ENCLOSURES = {
    "125B":    {"A": (62, 117),    "B": (57, 33),  "C": (33, 111)},
    "1590A":   {"A": (35, 89),     "B": (30, 25),  "C": (25, 83)},
    "1590B":   {"A": (56, 108.5),  "B": (52, 24),  "C": (24, 103)},
    "1590BB":  {"A": (90, 115.5),  "B": (84, 29),  "C": (29, 110)},
    "1590BB2": {"A": (90, 115.5),  "B": (84, 32),  "C": (32, 110)},
    "1590D":   {"A": (113, 182),   "B": (105, 48), "C": (48, 172)},
    "1590DD":  {"A": (117, 185),   "B": (110, 29), "C": (29, 179)},
    "1590XX":  {"A": (117, 141),   "B": (112, 32), "C": (32, 135)},
}

# Tayda side letter -> (size key, descriptive suffix for the filename).
SIDES = {
    "A":   ("A", "face"),
    "B":   ("B", "end"),
    "C":   ("C", "side"),
    "D":   ("B", "end"),
    "E":   ("C", "side"),
    "Lid": ("A", "back"),
}

# Bottom to top. SVG paints in document order, so this is also the stacking order.
LAYERS = [
    "Base Artwork",
    "Accent Artwork",
    "Logos",
    "Labels",
    "Holes",
    "Knobs & Switches",
]

SAFE_MARGIN_MM = 3.0
GUIDE_COLOUR = "#00B4FF"
GUIDE_STROKE_MM = 0.2


def fmt(n):
    """Format a number without a trailing .0 so sizes read like the Tayda guide."""
    return f"{n:g}"


def layer_id(name):
    return name.replace(" & ", "-and-").replace(" ", "-")


def layer_group(name, body="", hidden=False):
    style = ' style="display:none"' if hidden else ""
    return (
        f'  <g id="{layer_id(name)}" serif:id="{xml_escape(name)}" '
        f'inkscape:label="{xml_escape(name)}" inkscape:groupmode="layer"{style}>\n'
        f"{body}"
        f"  </g>\n"
    )


def xml_escape(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def guides(w, h):
    m = SAFE_MARGIN_MM
    stroke = (
        f'fill="none" stroke="{GUIDE_COLOUR}" stroke-width="{fmt(GUIDE_STROKE_MM)}"'
    )
    dashed = f'{stroke} stroke-dasharray="1 1"'
    return (
        f'    <rect id="Artboard-Edge" x="0" y="0" width="{fmt(w)}" height="{fmt(h)}" {stroke}/>\n'
        f'    <rect id="Safe-Area" x="{fmt(m)}" y="{fmt(m)}" '
        f'width="{fmt(w - 2 * m)}" height="{fmt(h - 2 * m)}" {dashed}/>\n'
        f'    <line id="Vertical-Centre" x1="{fmt(w / 2)}" y1="0" x2="{fmt(w / 2)}" y2="{fmt(h)}" {dashed}/>\n'
        f'    <line id="Horizontal-Centre" x1="0" y1="{fmt(h / 2)}" x2="{fmt(w)}" y2="{fmt(h / 2)}" {dashed}/>\n'
    )


def placeholder(w, h):
    # Affinity drops empty groups on SVG import, so each layer carries a hidden
    # outline to keep it alive. Hidden objects are not exported; delete it once
    # the layer has real content.
    return (
        f'    <rect id="Placeholder" serif:id="Placeholder (delete me)" x="0" y="0" '
        f'width="{fmt(w)}" height="{fmt(h)}" fill="none" stroke="{GUIDE_COLOUR}" '
        f'stroke-width="{fmt(GUIDE_STROKE_MM)}" style="display:none"/>\n'
    )


def template(enclosure, side, w, h):
    layers = "".join(layer_group(name, placeholder(w, h)) for name in LAYERS)
    layers += layer_group("Guides", guides(w, h), hidden=True)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:serif="http://www.serif.com/" '
        f'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
        f'width="{fmt(w)}mm" height="{fmt(h)}mm" viewBox="0 0 {fmt(w)} {fmt(h)}">\n'
        f"  <title>{enclosure} side {side} ({fmt(w)} x {fmt(h)} mm)</title>\n"
        f"{layers}"
        "</svg>\n"
    )


def main():
    out_root = Path(sys.argv[1] if len(sys.argv) > 1 else "templates")
    count = 0
    for enclosure, sizes in ENCLOSURES.items():
        out_dir = out_root / enclosure
        out_dir.mkdir(parents=True, exist_ok=True)
        for side, (size_key, suffix) in SIDES.items():
            w, h = sizes[size_key]
            path = out_dir / f"{enclosure}-{side}-{suffix}.svg"
            path.write_text(template(enclosure, side, w, h))
            count += 1
    print(f"wrote {count} templates to {out_root}/")


if __name__ == "__main__":
    main()
