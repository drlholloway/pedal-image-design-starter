# Pedal Image Design Starter
### Starter images for UV artwork

## Introduction

Creating graphics for pedals is a daunting task, and this library / wiki is here to help. It has tutorials and ready-made templates for designing pedal artwork that you can either:

- convert to PDF for UV printing with the Tayda UV Converter Tool, or
- print on an inkjet or laser printer, apply to a pre-drilled enclosure, and protect with lacquer or another clear coat.

It contains correctly sized templates for the face, sides, ends and back of each standard pedal enclosure. We assume you are using [Affinity](https://www.affinity.studio), a free graphic design tool available for multiple platforms, but the templates are plain SVG and open in any vector editor (Inkscape, Illustrator, ...).

## Templates

Every template is sized exactly to Tayda's UV-print artboard for that side, in millimetres. They live in `templates/<enclosure>/`, one file per side:

| File | Tayda side | What it is |
|---|---|---|
| `<enclosure>-A-face.svg` | A | Front face, where the knobs and footswitch go |
| `<enclosure>-B-end.svg`, `-D-end.svg` | B, D | The two short ends (jacks, DC) |
| `<enclosure>-C-side.svg`, `-E-side.svg` | C, E | The two long sides |
| `<enclosure>-Lid-back.svg` | Lid | The back plate |

### Artboard sizes (mm, width × height)

| Enclosure | Face / Lid | Ends (B, D) | Sides (C, E) |
|---|---|---|---|
| 125B | 62 × 117 | 57 × 33 | 33 × 111 |
| 1590A | 35 × 89 | 30 × 25 | 25 × 83 |
| 1590B | 56 × 108.5 | 52 × 24 | 24 × 103 |
| 1590BB | 90 × 115.5 | 84 × 29 | 29 × 110 |
| 1590BB2 | 90 × 115.5 | 84 × 32 | 32 × 110 |
| 1590D | 113 × 182 | 105 × 48 | 48 × 172 |
| 1590DD | 117 × 185 | 110 × 29 | 29 × 179 |
| 1590XX | 117 × 141 | 112 × 32 | 32 × 135 |

Sizes come from Tayda's [UV printing service guide](https://www.taydaelectronics.com/uv-printing-service-guide-v1). If Tayda changes them, update `tools/generate_templates.py` and regenerate.

### Layers

Each template has these layers, bottom to top:

| Layer | Use it for | Printed? |
|---|---|---|
| **Base Artwork** | Background, main illustration | Yes |
| **Accent Artwork** | Borders, frames, flourishes | Yes |
| **Logos** | Pedal name, brand mark | Yes |
| **Labels** | Knob and switch labels, jack markings | Yes |
| **Holes** | Drill positions, so artwork doesn't land under a pot or jack | **No** |
| **Knobs & Switches** | Knob and footswitch images for a rough preview of the finished pedal | **No** |
| **Guides** (hidden) | Artboard edge, 3 mm safe area, centre lines | **No** |

Each layer starts with a hidden `Placeholder (delete me)` outline. It's there because Affinity drops empty layers when it imports an SVG. Hidden objects aren't exported, so it's harmless, but you can delete it once the layer has real content.

## Using a template in Affinity

1. Open the SVG for the side you're designing (for example `templates/1590B/1590B-A-face.svg`).
2. Save it as an Affinity document (`.afdesign`), or as a template so it appears when you start a new document.
3. Design, keeping important details inside the safe area. Turn on **Guides** to see it.

## Before you print

- **Hide or delete the Holes, Knobs & Switches and Guides layers.** Anything visible gets printed on the enclosure.
- **Export at 300 DPI or more** at the artboard size. PNG with a transparent background lets Tayda's white undercoat follow your artwork, so bare enclosure shows through the gaps.
- **Convert text to curves/outlines** if you are exporting SVG.
- **Check the file in Tayda's PDF Analyzer** before ordering, and order a single enclosure before a batch.

## Regenerating the templates

```sh
python3 tools/generate_templates.py
```

This rewrites everything in `templates/`. Change the layer list, safe margin or sizes in the script, not in the SVGs.
