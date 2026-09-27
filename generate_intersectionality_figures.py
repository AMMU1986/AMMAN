#!/usr/bin/env python3
"""
Generate 4 conceptual figure images (PNG) for the chapter
"Intersectionality, Climate Vulnerability, and Community Resilience".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - The intersectional matrix of compounded climate vulnerability
  Figure 2 - Comparative vulnerability profiles of differently positioned women
  Figure 3 - Pillars of community resilience and the community-based
             adaptation cycle
  Figure 4 - An integrated framework for intersectional, community-centered
             climate action
"""

import os
import math

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


def gen_fig1():
    """Figure 1: Intersectional matrix of compounded climate vulnerability."""
    c = PNGCanvas(760, 500)
    c.text_c(380, 10, "The Intersectional Matrix of Compounded Climate Vulnerability", BLACK, 2)

    # Central individual/household node
    cx, cy = 380, 240
    c.circle(cx, cy, 46, DARK_BLUE, PALE_BLUE)
    c.text_c(cx, cy - 12, "Individual", BLACK, 1)
    c.text_c(cx, cy + 2, "/ Household", BLACK, 1)
    c.text_c(cx, cy + 16, "at risk", GRAY, 1)

    # Overlapping identity axes arranged radially, converging on the center
    axes = [
        ("Gender", MED_BLUE, LIGHT_BLUE),
        ("Caste /", DARK_GREEN, LIGHT_GREEN),
        ("Class /", ORANGE, LIGHT_ORANGE),
        ("Indigeneity", PURPLE, LIGHT_PURPLE),
        ("Age /", RED, LIGHT_RED),
        ("Displacement", GOLD, LIGHT_GOLD),
    ]
    sublabels = ["norms, labor", "Ethnicity", "Income", "land, rights", "Disability", "status"]
    n = len(axes)
    R = 150
    for i, ((label, col, fill), sub) in enumerate(zip(axes, sublabels)):
        ang = -math.pi / 2 + i * (2 * math.pi / n)
        bx = int(cx + R * math.cos(ang))
        by = int(cy + R * math.sin(ang))
        c.rect(bx - 70, by - 26, bx + 70, by + 26, col, fill)
        c.text_c(bx, by - 10, label, BLACK, 1)
        c.text_c(bx, by + 6, sub, GRAY, 1)
        # arrow converging toward the center node
        dx, dy = cx - bx, cy - by
        d = math.sqrt(dx * dx + dy * dy)
        sx = int(bx + dx / d * 74)
        sy = int(by + dy / d * 28)
        ex = int(cx - dx / d * 50)
        ey = int(cy - dy / d * 50)
        c.arrow(sx, sy, ex, ey, GRAY, 2, 9)

    # Legend / interpretive note
    c.rect(30, 430, 730, 482, GRAY, (250, 250, 250))
    c.text_c(380, 442, "Overlapping systems of power interact (not merely add) to intensify risk", BLACK, 1)
    c.text_c(380, 460, "and constrain adaptive pathways; densest intersections are least visible to planners", GRAY, 1)

    c.text(30, 492, "Figure 1: Multiple axes of identity converge to produce compounded, relational vulnerability", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Intersectional_Matrix.png'))
    print("  Figure_1_Intersectional_Matrix.png done")


def gen_fig2():
    """Figure 2: Comparative vulnerability profiles of differently positioned women."""
    c = PNGCanvas(820, 470)
    c.text_c(410, 10, "Comparative Vulnerability Profiles of Differently Positioned Women", BLACK, 2)

    # Grouped horizontal bars across three dimensions for four profiles.
    # Higher bar => higher exposure/sensitivity OR lower adaptive capacity (risk).
    dims = ["Exposure", "Sensitivity", "Low Adaptive Capacity"]
    profiles = [
        ("Landowning, dominant group", [30, 30, 25], MED_GREEN),
        ("Landless, marginalized caste", [70, 72, 78], ORANGE),
        ("Indigenous, dispossessed", [78, 70, 82], PURPLE),
        ("Widowed / displaced, poor", [85, 88, 90], RED),
    ]

    left = 260
    axis_x = left
    top = 60
    group_h = 96
    bar_h = 20
    max_w = 420

    # gridlines / scale
    for frac, lab in [(0.0, "low"), (0.5, "med"), (1.0, "high")]:
        gx = int(axis_x + frac * max_w)
        c.vline(gx, top - 8, top + len(profiles) * group_h - 30, LIGHT_GRAY)
        c.text_c(gx, top - 20, lab, GRAY, 1)
    c.text_c(axis_x + max_w // 2, 40, "Relative level of climate risk", GRAY, 1)

    for pi, (name, vals, col) in enumerate(profiles):
        gy = top + pi * group_h
        c.text(20, gy + group_h // 2 - 24, name[:22], BLACK, 1)
        if len(name) > 22:
            c.text(20, gy + group_h // 2 - 10, name[22:], BLACK, 1)
        for di, (dim, v) in enumerate(zip(dims, vals)):
            by = gy + di * (bar_h + 4)
            bw = int(v / 100.0 * max_w)
            shade = [LIGHT_GREEN, LIGHT_ORANGE, LIGHT_PURPLE, LIGHT_RED][pi]
            c.rect(axis_x, by, axis_x + bw, by + bar_h, col, shade)
            c.text(axis_x + bw + 4, by + 4, dim, GRAY, 1)

    c.text(20, 452, "Figure 2: Internal heterogeneity among women; aggregate gender analysis conceals the most vulnerable", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Vulnerability_Profiles.png'))
    print("  Figure_2_Vulnerability_Profiles.png done")


def gen_fig3():
    """Figure 3: Pillars of community resilience + community-based adaptation cycle."""
    c = PNGCanvas(760, 490)
    c.text_c(380, 10, "Pillars of Community Resilience and the Adaptation Cycle", BLACK, 2)

    # (a) Five pillars supporting a "resilience" lintel
    c.text(30, 40, "(a) Pillars of Community Resilience", BLACK, 1)
    pillars = [
        ("Diversified", "livelihoods", MED_BLUE, LIGHT_BLUE),
        ("Collective", "institutions", DARK_GREEN, LIGHT_GREEN),
        ("Resource", "access", ORANGE, LIGHT_ORANGE),
        ("Social", "cohesion", PURPLE, LIGHT_PURPLE),
        ("Voice &", "influence", RED, LIGHT_RED),
    ]
    px0 = 30
    pw = 68
    gap = 12
    ptop = 95
    pbot = 210
    lintel_x2 = px0 + len(pillars) * (pw + gap) - gap
    # lintel (roof)
    c.rect(px0, 70, lintel_x2, 92, GOLD, LIGHT_GOLD)
    c.text_c((px0 + lintel_x2) // 2, 76, "COMMUNITY RESILIENCE", BLACK, 1)
    # base
    c.rect(px0, pbot, lintel_x2, pbot + 16, GRAY, LIGHT_GRAY)
    for i, (l1, l2, col, fill) in enumerate(pillars):
        bx = px0 + i * (pw + gap)
        c.rect(bx, ptop, bx + pw, pbot, col, fill)
        c.text_c(bx + pw // 2, ptop + 40, l1, BLACK, 1)
        c.text_c(bx + pw // 2, ptop + 56, l2, BLACK, 1)

    # (b) Community-based adaptation cycle (4 stages in a loop)
    c.text(430, 40, "(b) Community-Based Adaptation Cycle", BLACK, 1)
    ccx, ccy = 580, 165
    r = 95
    stages = [
        ("Assess", MED_BLUE, LIGHT_BLUE),
        ("Plan", DARK_GREEN, LIGHT_GREEN),
        ("Act", ORANGE, LIGHT_ORANGE),
        ("Learn", PURPLE, LIGHT_PURPLE),
    ]
    pts = []
    for i, (label, col, fill) in enumerate(stages):
        ang = -math.pi / 2 + i * (math.pi / 2)
        sx = int(ccx + r * math.cos(ang))
        sy = int(ccy + r * math.sin(ang))
        pts.append((sx, sy))
        c.circle(sx, sy, 34, col, fill)
        c.text_c(sx, sy - 4, label, BLACK, 1)
    # curved-ish arrows around the loop
    for i in range(4):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % 4]
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        c.arrow(x1 + (x2 - x1) // 4, y1 + (y2 - y1) // 4,
                x2 - (x2 - x1) // 4, y2 - (y2 - y1) // 4, GRAY, 2, 9)
    c.text_c(ccx, ccy - 4, "Local", GRAY, 1)
    c.text_c(ccx, ccy + 10, "ownership", GRAY, 1)

    # Interpretive note
    c.rect(30, 300, 730, 352, GRAY, (250, 250, 250))
    c.text_c(380, 312, "Resilience is transformative only when each pillar and each stage of the cycle", BLACK, 1)
    c.text_c(380, 330, "is made inclusive of marginalized members' knowledge and priorities", GRAY, 1)

    c.text(30, 468, "Figure 3: Interdependent pillars and an iterative, locally owned adaptation cycle", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Resilience_Pillars_Cycle.png'))
    print("  Figure_3_Resilience_Pillars_Cycle.png done")


def gen_fig4():
    """Figure 4: Integrated framework for intersectional, community-centered climate action."""
    c = PNGCanvas(940, 470)
    c.text_c(470, 10, "Integrated Framework for Intersectional, Community-Centered Climate Action", BLACK, 2)

    # Vertical flow of four layers linked by arrows
    layers = [
        ("Intersectional Analysis",
         "Map compounded vulnerability across gender, caste, class, indigeneity, age",
         DARK_BLUE, PALE_BLUE),
        ("Feminist & Decolonial Lenses",
         "Center power, care, rights, self-determination, and local knowledge",
         PURPLE, LIGHT_PURPLE),
        ("Participatory & Community-Led Governance",
         "Genuine decision power; gender-responsive finance; TEK integration",
         DARK_GREEN, LIGHT_GREEN),
        ("Transformative Outcomes",
         "Equitable, durable resilience that reshapes structures of vulnerability",
         ORANGE, LIGHT_ORANGE),
    ]
    lx1, lx2 = 180, 760
    top = 60
    lh = 66
    gap = 22
    for i, (title, sub, col, fill) in enumerate(layers):
        y1 = top + i * (lh + gap)
        y2 = y1 + lh
        c.rect(lx1, y1, lx2, y2, col, fill)
        c.text_c((lx1 + lx2) // 2, y1 + 16, title, BLACK, 1)
        c.text_c((lx1 + lx2) // 2, y1 + 38, sub, GRAY, 1)
        if i < len(layers) - 1:
            midx = (lx1 + lx2) // 2
            c.arrow(midx, y2 + 2, midx, y2 + gap - 2, GRAY, 3, 10)

    # Feedback / learning loop on the right side, bottom back to top
    c.line(lx2 + 10, top + 3 * (lh + gap) + lh // 2, 850, top + 3 * (lh + gap) + lh // 2, MED_BLUE, 2)
    c.line(850, top + 3 * (lh + gap) + lh // 2, 850, top + lh // 2, MED_BLUE, 2)
    c.arrow(850, top + lh // 2, lx2 + 10, top + lh // 2, MED_BLUE, 2, 9)
    c.text(860, top + 2 * (lh + gap), "learning", MED_BLUE, 1)
    c.text(860, top + 2 * (lh + gap) + 14, "& feedback", MED_BLUE, 1)

    # Justice anchor on the left
    c.line(lx1 - 10, top + lh // 2, 100, top + lh // 2, RED, 2)
    c.line(100, top + lh // 2, 100, top + 3 * (lh + gap) + lh // 2, RED, 2)
    c.arrow(100, top + 3 * (lh + gap) + lh // 2, lx1 - 10, top + 3 * (lh + gap) + lh // 2, RED, 2, 9)
    c.text(55, top + 2 * (lh + gap) - 10, "climate", RED, 1)
    c.text(55, top + 2 * (lh + gap) + 4, "justice", RED, 1)

    c.text(30, 458, "Figure 4: Linking analysis of compounded vulnerability to inclusive governance and transformative outcomes", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Integrated_Framework.png'))
    print("  Figure_4_Integrated_Framework.png done")


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
