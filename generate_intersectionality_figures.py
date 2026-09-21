#!/usr/bin/env python3
"""
Generate 4 conceptual figures (PNG) for the chapter
"Intersectionality, Climate Vulnerability, and Community Resilience".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - Intersectional framework of climate vulnerability
  Figure 2 - Pathways of differential climate vulnerability
  Figure 3 - Community resilience ecosystem
  Figure 4 - Transformative framework for intersectional climate action

Note: the bundled 5x7 bitmap font supports letters, digits and a small set of
punctuation; ampersands and apostrophes are intentionally avoided in labels.
"""

import os

from generate_figures import (
    PNGCanvas,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE,
    RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE,
    GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY,
    BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/intersectionality_figures'


def _box_center_lines(c, x1, y1, x2, y2, outline, fill, lines, color=BLACK,
                      scale=1, line_h=13, top_pad=8):
    """Draw a rectangle and center a list of text lines within it."""
    c.rect(x1, y1, x2, y2, outline, fill)
    cx = (x1 + x2) // 2
    total = len(lines) * line_h
    start = (y1 + y2) // 2 - total // 2 + top_pad // 2
    for i, ln in enumerate(lines):
        c.text_c(cx, start + i * line_h, ln, color, scale)


def gen_fig1():
    """Figure 1: Intersectional framework of climate vulnerability."""
    c = PNGCanvas(780, 500)
    c.text_c(390, 12, "Intersectional Framework of Climate Vulnerability", BLACK, 2)

    # Central node
    cx1, cy1, cx2, cy2 = 300, 205, 480, 275
    _box_center_lines(c, cx1, cy1, cx2, cy2, DARK_GREEN, LIGHT_GREEN,
                      ["INTERSECTING POSITION", "Individual and Household"],
                      scale=1, line_h=16)
    center = (390, 240)

    # Axis boxes with their anchor points toward the center
    axes = [
        ("Gender", 40, 60, MED_BLUE, LIGHT_BLUE),
        ("Caste", 230, 55, PURPLE, LIGHT_PURPLE),
        ("Class", 420, 55, ORANGE, LIGHT_ORANGE),
        ("Ethnicity", 600, 60, RED, LIGHT_RED),
        ("Indigeneity", 30, 210, DARK_BLUE, PALE_BLUE),
        ("Age", 610, 205, GOLD, LIGHT_GOLD),
        ("Disability", 600, 275, MED_GREEN, LIGHT_GREEN),
    ]
    bw, bh = 140, 46
    for label, bx, by, col, fill in axes:
        _box_center_lines(c, bx, by, bx + bw, by + bh, col, fill, [label],
                          scale=1)
        # anchor from box edge toward center
        bcx, bcy = bx + bw // 2, by + bh // 2
        # start near the box, end near the central node edge
        if bcy < cy1:            # box above center
            sx, sy = bcx, by + bh
            ex, ey = center[0] + (bcx - center[0]) // 3, cy1 - 4
        elif bcx < cx1:          # box left of center
            sx, sy = bx + bw, bcy
            ex, ey = cx1 - 4, center[1]
        else:                    # box right of center
            sx, sy = bx, bcy
            ex, ey = cx2 + 4, center[1]
        c.arrow(sx, sy, ex, ey, GRAY, 2, 8)

    # Output box
    ox1, oy1, ox2, oy2 = 235, 370, 545, 430
    _box_center_lines(c, ox1, oy1, ox2, oy2, DARK_BLUE, PALE_BLUE,
                      ["Differential Vulnerability", "and Adaptive Capacity"],
                      scale=1, line_h=16)
    c.arrow(390, cy2 + 4, 390, oy1 - 4, DARK_GREEN, 3, 11)

    c.text_c(390, 455, "Axes interact rather than add: combined positions "
                       "produce distinct climate risk", GRAY, 1)
    c.text(30, 482, "Figure 1: Intersecting axes of social identity shaping "
                    "climate vulnerability and adaptive capacity", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Intersectional_Framework.png'))
    print("  Figure_1_Intersectional_Framework.png done")


def gen_fig2():
    """Figure 2: Pathways of differential climate vulnerability."""
    c = PNGCanvas(820, 500)
    c.text_c(410, 12, "Pathways of Differential Climate Vulnerability", BLACK, 2)

    # Hazard box (top)
    _box_center_lines(c, 250, 50, 570, 100, DARK_BLUE, PALE_BLUE,
                      ["CLIMATE HAZARD", "drought, flood, storm, heat"],
                      scale=1, line_h=16)

    # Four channel boxes
    channels = [
        (["Division", "of Labor"], MED_BLUE, LIGHT_BLUE),
        (["Resource", "Access"], ORANGE, LIGHT_ORANGE),
        (["Mobility", "and Voice"], PURPLE, LIGHT_PURPLE),
        (["Compounding", "Marginalization"], RED, LIGHT_RED),
    ]
    bw, bh = 170, 62
    gap = 30
    total_w = 4 * bw + 3 * gap
    start_x = (820 - total_w) // 2
    top = 175
    centers = []
    for i, (lines, col, fill) in enumerate(channels):
        bx = start_x + i * (bw + gap)
        _box_center_lines(c, bx, top, bx + bw, top + bh, col, fill, lines,
                          scale=1, line_h=15)
        cxi = bx + bw // 2
        centers.append(cxi)
        c.arrow(410, 100 + 2, cxi, top - 4, GRAY, 2, 8)
        c.text_c(cxi, top + bh + 12, "social channel", GRAY, 1)

    # Outcome box
    oy1, oy2 = 300, 400
    _box_center_lines(c, 230, oy1, 590, oy1 + 34, DARK_GREEN, LIGHT_GREEN,
                      ["DIFFERENTIAL OUTCOMES"], scale=1)
    # three outcome levels
    levels = [
        ("Severe", RED, LIGHT_RED, "most marginalized"),
        ("Moderate", GOLD, LIGHT_GOLD, "partial buffering"),
        ("Buffered", MED_GREEN, LIGHT_GREEN, "resource-rich"),
    ]
    lw = 150
    lgap = 25
    ltot = 3 * lw + 2 * lgap
    lstart = (820 - ltot) // 2
    for i, (lab, col, fill, sub) in enumerate(levels):
        lx = lstart + i * (lw + lgap)
        _box_center_lines(c, lx, 350, lx + lw, 350 + 44, col, fill,
                          [lab, sub], scale=1, line_h=15)
    for cxi in centers:
        c.arrow(cxi, top + bh + 20, 410, oy1 - 4, GRAY, 2, 7)

    c.text_c(410, 415, "The same hazard yields unequal outcomes depending on "
                       "intersecting social position", GRAY, 1)
    c.text(30, 482, "Figure 2: Social channels translating a common climate "
                    "hazard into differentiated outcomes", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Vulnerability_Pathways.png'))
    print("  Figure_2_Vulnerability_Pathways.png done")


def gen_fig3():
    """Figure 3: Community resilience ecosystem."""
    c = PNGCanvas(780, 500)
    c.text_c(390, 12, "The Community Resilience Ecosystem", BLACK, 2)

    # Enabling environment enclosure
    c.rect(40, 55, 740, 360, DARK_BLUE, PALE_BLUE)
    c.text_c(390, 64, "ENABLING ENVIRONMENT: rights, resources, "
                      "participatory governance", BLACK, 1)

    # Three resilience nodes (triangle layout)
    n1 = (200, 130, 380, 200)   # top-left
    n2 = (500, 130, 680, 200)   # top-right
    n3 = (300, 260, 480, 330)   # bottom-center
    _box_center_lines(c, *n1, MED_BLUE, LIGHT_BLUE,
                      ["Grassroots", "Womens Organizations"], scale=1, line_h=15)
    _box_center_lines(c, *n2, PURPLE, LIGHT_PURPLE,
                      ["Traditional Ecological", "Knowledge"], scale=1, line_h=15)
    _box_center_lines(c, *n3, ORANGE, LIGHT_ORANGE,
                      ["Community-Based", "Adaptation"], scale=1, line_h=15)

    def cen(b):
        return ((b[0] + b[2]) // 2, (b[1] + b[3]) // 2)
    c1, c2, c3 = cen(n1), cen(n2), cen(n3)
    # bidirectional links
    c.arrow(n1[2] + 2, c1[1], n2[0] - 2, c2[1], GRAY, 2, 8)
    c.arrow(n2[0] - 2, c2[1] + 6, n1[2] + 2, c1[1] + 6, GRAY, 2, 8)
    c.arrow(c1[0] + 10, n1[3] + 2, c3[0] - 20, n3[1] - 2, GRAY, 2, 8)
    c.arrow(c2[0] - 10, n2[3] + 2, c3[0] + 20, n3[1] - 2, GRAY, 2, 8)
    c.text_c(390, 168, "mutually", GRAY, 1)
    c.text_c(390, 180, "reinforcing", GRAY, 1)

    # Resilience outcome
    _box_center_lines(c, 235, 400, 545, 452, DARK_GREEN, LIGHT_GREEN,
                      ["CLIMATE RESILIENCE", "adaptive, equitable, local"],
                      scale=1, line_h=16)
    c.arrow(390, 360 + 2, 390, 400 - 4, DARK_GREEN, 3, 11)

    c.text(30, 482, "Figure 3: Three mutually reinforcing sources of community "
                    "resilience within an enabling environment", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Resilience_Ecosystem.png'))
    print("  Figure_3_Resilience_Ecosystem.png done")


def gen_fig4():
    """Figure 4: Transformative framework for intersectional climate action."""
    c = PNGCanvas(820, 500)
    c.text_c(410, 12, "Transformative Framework for Intersectional Climate Action",
             BLACK, 2)

    # Goal box (top)
    _box_center_lines(c, 250, 45, 570, 92, DARK_GREEN, LIGHT_GREEN,
                      ["GOAL: Just and Effective", "Climate Resilience"],
                      scale=1, line_h=16)

    # Four pillars
    pillars = [
        (["Gender-", "Responsive", "Finance"], MED_BLUE, LIGHT_BLUE),
        (["Traditional", "Ecological", "Knowledge"], PURPLE, LIGHT_PURPLE),
        (["Grassroots", "Leadership", "Capacity"], ORANGE, LIGHT_ORANGE),
        (["Institutional", "and Structural", "Reform"], RED, LIGHT_RED),
    ]
    pw, ph = 165, 150
    gap = 24
    total_w = 4 * pw + 3 * gap
    start_x = (820 - total_w) // 2
    ptop = 160
    for i, (lines, col, fill) in enumerate(pillars):
        px = start_x + i * (pw + gap)
        _box_center_lines(c, px, ptop, px + pw, ptop + ph, col, fill, lines,
                          scale=1, line_h=16)
        cxi = px + pw // 2
        # arrow up to goal
        c.arrow(cxi, ptop - 4, cxi, 92 + 4, GRAY, 2, 8)
        # arrow from foundation up into pillar
        c.arrow(cxi, ptop + ph + 40, cxi, ptop + ph + 4, GRAY, 2, 8)

    # Foundation box (bottom)
    fy1 = ptop + ph + 44
    _box_center_lines(c, start_x, fy1, start_x + total_w, fy1 + 52,
                      DARK_BLUE, PALE_BLUE,
                      ["FOUNDATION: Participatory, Feminist, "
                       "and Decolonial Governance"], scale=1, line_h=16)

    c.text(30, 484, "Figure 4: Four pillars of intersectional climate action "
                    "on a participatory governance foundation", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Action_Framework.png'))
    print("  Figure_4_Action_Framework.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating intersectionality chapter figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print(f"\nAll figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz / 1024:.1f} KB")


if __name__ == '__main__':
    main()
