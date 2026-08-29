#!/usr/bin/env python3
"""Generate 4 figures (PNG) for the Migration, Governance and Regional Politics chapter."""

import os
import math
from migration_pngcanvas import (PNGCanvas, DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
                                  DARK_GREEN, MED_GREEN, LIGHT_GREEN, ORANGE, LIGHT_ORANGE,
                                  RED, LIGHT_RED, PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
                                  GRAY, LIGHT_GRAY, BLACK, WHITE, TEAL, LIGHT_TEAL)

OUTPUT_DIR = '/projects/sandbox/AMMAN/migration_figures'


def fig1():
    """Figure 1: Conceptual framework linking migration governance, identity and political economy."""
    c = PNGCanvas(760, 500)
    c.text_c(380, 12, "Framework of Migration Governance (ME and Africa)", BLACK, 2)

    # Three driver boxes (top)
    drivers = [("Structural Drivers", 40, DARK_BLUE, PALE_BLUE,
                ["Conflict & fragility", "Labour demand", "Climate stress"]),
               ("Governance Layer", 300, DARK_GREEN, LIGHT_GREEN,
                ["Policies & borders", "Institutions", "Regional frameworks"]),
               ("Political Economy", 555, ORANGE, LIGHT_ORANGE,
                ["Remittances", "Inequality", "Diaspora capital"])]
    for label, bx, oc, fc, items in drivers:
        c.rect(bx, 55, bx+165, 175, oc, fc)
        c.text_c(bx+82, 63, label, BLACK, 1)
        for k, it in enumerate(items):
            c.text(bx+12, 90+k*22, "- "+it, BLACK, 1)

    # Arrows down to central process
    for bx in (122, 382, 637):
        c.arrow(bx, 175, 380, 215, GRAY, 2, 8)

    # Central process box
    c.rect(230, 220, 530, 300, PURPLE, LIGHT_PURPLE)
    c.text_c(380, 232, "MIGRATION PROCESS", BLACK, 2)
    c.text_c(380, 258, "Corridors, displacement,", BLACK, 1)
    c.text_c(380, 274, "mixed & labour migration", BLACK, 1)

    # Outcomes (bottom)
    outcomes = [("Identity & Belonging", 40, MED_BLUE, LIGHT_BLUE),
                ("Political Stability", 300, RED, LIGHT_RED),
                ("Regional Development", 555, TEAL, LIGHT_TEAL)]
    for label, bx, oc, fc in outcomes:
        c.rect(bx, 355, bx+165, 415, oc, fc)
        c.text_c(bx+82, 378, label, BLACK, 1)
        c.arrow(380, 300, bx+82, 355, GRAY, 2, 8)

    # Feedback loop
    c.line(122, 415, 30, 415, RED, 2)
    c.line(30, 415, 30, 115, RED, 2)
    c.arrow(30, 115, 40, 115, RED, 2, 7)
    c.text(35, 440, "Feedback: governance outcomes reshape drivers and policy (Section 4)", RED, 1)

    c.text(40, 470, "Figure 1: Analytical framework linking drivers, governance and outcomes.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1.png'))
    print("Figure_1 done")


def fig2():
    """Figure 2: Major migration corridors (stylized flow map ME & Africa)."""
    c = PNGCanvas(760, 500)
    c.text_c(380, 12, "Major Migration Corridors within and between the Regions", BLACK, 2)

    # Stylized landmass panels
    c.rect(60, 60, 360, 440, DARK_GREEN, (235, 245, 232))
    c.text_c(210, 68, "AFRICA", DARK_GREEN, 2)
    c.rect(400, 60, 700, 440, DARK_BLUE, (233, 240, 250))
    c.text_c(550, 68, "MIDDLE EAST", DARK_BLUE, 2)

    # Nodes (hubs): name, x, y
    nodes = {
        "Horn": (300, 300), "W.Africa": (110, 210), "N.Africa": (200, 110),
        "Sahel": (170, 260), "Gulf": (600, 180), "Levant": (470, 130),
        "Egypt": (360, 150), "Yemen": (560, 320),
    }
    for name, (x, y) in nodes.items():
        c.circle(x, y, 8, BLACK, GOLD)
        c.text(x+11, y-4, name, BLACK, 1)

    # Corridors: (from, to, color, label)
    corridors = [
        ("Horn", "Gulf", MED_BLUE, "Eastern"),
        ("Horn", "Yemen", ORANGE, "Yemen route"),
        ("W.Africa", "N.Africa", MED_GREEN, "Western"),
        ("Sahel", "N.Africa", PURPLE, "Central"),
        ("N.Africa", "Levant", RED, "Trans-Med"),
        ("Egypt", "Gulf", TEAL, "Labour"),
        ("Levant", "Gulf", GRAY, "Intra-ME"),
    ]
    for f, t, col, lbl in corridors:
        x1, y1 = nodes[f]; x2, y2 = nodes[t]
        c.arrow(x1, y1, x2, y2, col, 2, 9)
        mx, my = (x1+x2)//2, (y1+y2)//2
        c.text(mx-14, my-14, lbl, col, 1)

    # Legend
    c.rect(60, 455, 700, 490, LIGHT_GRAY, (250, 250, 250))
    c.text(70, 465, "Arrows indicate dominant direction of labour, forced and mixed migration flows.", BLACK, 1)
    c.text(70, 478, "Figure 2: Principal migration corridors (schematic, not to scale).", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2.png'))
    print("Figure_2 done")


def fig3():
    """Figure 3: Remittance and displacement trends (dual chart)."""
    c = PNGCanvas(760, 500)
    c.text_c(380, 12, "Remittances and Forced Displacement Trends (Illustrative)", BLACK, 2)

    # (a) Remittance bar chart
    c.text(50, 45, "(a) Remittance inflows (USD bn, selected years)", BLACK, 1)
    years = ["2010", "2014", "2018", "2022", "2024"]
    vals = [58, 74, 88, 102, 110]
    c.vline(70, 70, 230, BLACK)
    c.hline(70, 380, 230, BLACK)
    maxv = 120
    for i, (yr, v) in enumerate(zip(years, vals)):
        bx = 90 + i*58
        bh = int(v/maxv * 150)
        c.rect(bx, 230-bh, bx+38, 230, BLACK, MED_GREEN)
        c.text_c(bx+19, 235, yr, BLACK, 1)
        c.text_c(bx+19, 230-bh-12, str(v), BLACK, 1)
    c.text(40, 80, "120", BLACK, 1)
    c.text(46, 150, "60", BLACK, 1)
    c.text(52, 222, "0", BLACK, 1)

    # (b) Displacement line chart
    c.text(430, 45, "(b) Forced displacement (millions)", BLACK, 1)
    c.vline(450, 70, 230, BLACK)
    c.hline(450, 730, 230, BLACK)
    disp = [(0, 18), (1, 22), (2, 28), (3, 33), (4, 38)]
    maxd = 40
    pts = []
    for i, d in disp:
        x = 470 + i*62
        y = int(230 - d/maxd * 150)
        pts.append((x, y))
    for i in range(len(pts)-1):
        c.line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], RED, 2)
    for (x, y), (_, d) in zip(pts, disp):
        c.circle(x, y, 4, RED, RED)
        c.text_c(x, y-14, str(d), BLACK, 1)
    for i, yr in enumerate(years):
        c.text_c(470+i*62, 235, yr, BLACK, 1)
    c.text(418, 80, "40", BLACK, 1)
    c.text(424, 150, "20", BLACK, 1)
    c.text(430, 222, "0", BLACK, 1)

    # (c) Composition stacked bar
    c.text(50, 275, "(c) Composition of migration flows (share, %)", BLACK, 1)
    c.vline(70, 300, 450, BLACK)
    c.hline(70, 710, 450, BLACK)
    cats = [("Labour", 42, MED_BLUE), ("Forced", 31, RED),
            ("Family", 15, ORANGE), ("Other/mixed", 12, PURPLE)]
    bx = 120
    for name, share, col in cats:
        bh = int(share/50 * 130)
        c.rect(bx, 450-bh, bx+90, 450, BLACK, col)
        c.text_c(bx+45, 455, name, BLACK, 1)
        c.text_c(bx+45, 450-bh-12, str(share)+"%", BLACK, 1)
        bx += 150
    c.text(50, 475, "Figure 3: Remittances, displacement and flow composition (illustrative).", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3.png'))
    print("Figure_3 done")


def fig4():
    """Figure 4: Multi-level governance and future scenarios."""
    c = PNGCanvas(760, 520)
    c.text_c(380, 12, "Multi-Level Governance and Future Migration Scenarios", BLACK, 2)

    # (a) Governance pyramid
    c.text(50, 45, "(a) Multi-level governance architecture", BLACK, 1)
    layers = [("Global (GCM, UN, SDGs)", 320, GOLD, LIGHT_GOLD),
              ("Regional (AU, LAS, RECs)", 250, PURPLE, LIGHT_PURPLE),
              ("Bilateral agreements", 185, MED_BLUE, LIGHT_BLUE),
              ("National policy & institutions", 120, DARK_GREEN, LIGHT_GREEN),
              ("Local / host communities", 60, ORANGE, LIGHT_ORANGE)]
    cy = 70
    cx = 210
    for label, w, oc, fc in layers:
        c.rect(cx-w//2, cy, cx+w//2, cy+40, oc, fc)
        c.text_c(cx, cy+15, label, BLACK, 1)
        cy += 48
    c.arrow(cx, 320, cx, 300, GRAY, 2, 7)
    c.text(30, 320, "coordination & shared responsibility", GRAY, 1)

    # (b) Scenario quadrants
    c.text(430, 45, "(b) Future scenario space", BLACK, 1)
    ox, oy = 470, 90
    c.rect(ox, oy, ox+250, oy+250, BLACK, WHITE)
    c.vline(ox+125, oy, oy+250, GRAY)
    c.hline(ox, ox+250, oy+125, GRAY)
    c.text(ox+30, oy-2, "Restrictive", BLACK, 1)
    c.text(ox+150, oy-2, "Open", BLACK, 1)
    c.text(ox-40, oy+55, "High", BLACK, 1)
    c.text(ox-52, oy+62, "coop.", BLACK, 1)
    c.text(ox-40, oy+185, "Low", BLACK, 1)
    c.text(ox-52, oy+192, "coop.", BLACK, 1)
    quads = [("Fortress\nregion", ox+30, oy+40, RED),
             ("Inclusive\nmobility", ox+160, oy+40, MED_GREEN),
             ("Fragmented\ncrisis", ox+30, oy+165, GRAY),
             ("Ad-hoc\nbilateral", ox+160, oy+165, ORANGE)]
    for lbl, qx, qy, col in quads:
        parts = lbl.split("\n")
        c.circle(qx+30, qy+15, 6, col, col)
        for k, p in enumerate(parts):
            c.text(qx, qy+30+k*14, p, BLACK, 1)

    # Bottom summary bar
    c.rect(50, 400, 710, 480, DARK_BLUE, PALE_BLUE)
    c.text_c(380, 410, "Toward inclusive, adaptive, rights-based governance", BLACK, 2)
    c.text(70, 435, "- Rights-based & people-centred policies", MED_BLUE, 1)
    c.text(70, 452, "- Strengthened regional coordination", DARK_GREEN, 1)
    c.text(400, 435, "- Climate-mobility preparedness", ORANGE, 1)
    c.text(400, 452, "- Data systems & shared responsibility", PURPLE, 1)

    c.text(50, 500, "Figure 4: Governance architecture and scenario space for the two regions.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4.png'))
    print("Figure_4 done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fig1(); fig2(); fig3(); fig4()
    print("\nAll figures saved to", OUTPUT_DIR)
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz/1024:.1f} KB")


if __name__ == '__main__':
    main()
