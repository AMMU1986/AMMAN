#!/usr/bin/env python3
"""
Generate 4 scientific figure images (PNG) for the chapter
"Next-Generation Nanobiochar: Emerging Trends, Smart Technologies and
Future Innovations".

Reuses the pure-standard-library PNGCanvas rendering engine and colour
palette from generate_figures.py (no third-party dependencies).
"""

import os
import math

from generate_figures import (
    PNGCanvas,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE, RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/nanobiochar_figures'


def gen_fig1():
    """Figure 1: From biomass to next-generation nanobiochar pipeline."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "From Renewable Biomass to Next-Generation Nanobiochar", BLACK, 2)

    stages = [
        ("1. FEEDSTOCK", 30, DARK_GREEN, LIGHT_GREEN,
         ["Crop straw / husks", "Nut & rice shells", "Manure / sludge", "Forestry residue"]),
        ("2. CONVERSION", 210, ORANGE, LIGHT_ORANGE,
         ["Slow pyrolysis", "Hydrothermal", "Gasification", "Carbonization"]),
        ("3. NANO-ENGINEER", 390, MED_BLUE, LIGHT_BLUE,
         ["Ball milling", "Ultrasonication", "Activation", "Functionalize"]),
        ("4. NANOBIOCHAR", 570, PURPLE, LIGHT_PURPLE,
         ["High surface area", "Tunable chemistry", "Nano-porosity", "Multifunctional"]),
    ]
    bx_w, top, box_h = 165, 60, 150
    centers = []
    for label, bx, col, fill, items in stages:
        c.rect(bx, top, bx + bx_w, top + box_h, col, fill)
        c.fill_rect(bx, top, bx + bx_w, top + 24, col)
        c.text_c(bx + bx_w // 2, top + 8, label, WHITE, 1)
        for k, it in enumerate(items):
            c.text(bx + 8, top + 34 + k * 26, "- " + it, BLACK, 1)
        centers.append((bx + bx_w, top + box_h // 2))
        if bx < 560:
            c.arrow(bx + bx_w + 2, top + box_h // 2, bx + bx_w + 13, top + box_h // 2,
                    GRAY, 3, 9)

    # Applications band
    c.rect(30, 250, 735, 335, DARK_BLUE, PALE_BLUE)
    c.fill_rect(30, 250, 735, 274, DARK_BLUE)
    c.text_c(382, 258, "MULTIFUNCTIONAL APPLICATIONS", WHITE, 1)
    apps = ["Precision Ag", "Smart Nutrients", "Soil Health", "Carbon Storage",
            "Water Purify", "Metal Immobil.", "GHG Mitigation"]
    for i, a in enumerate(apps):
        ax = 45 + i * 99
        c.rect(ax, 285, ax + 90, 320, MED_GREEN, LIGHT_GREEN)
        c.text_c(ax + 45, 297, a, BLACK, 1)
    # Arrow from nanobiochar box down to applications
    c.arrow(652, 210, 652, 248, PURPLE, 3, 9)

    # Circular-economy return arrow
    c.rect(250, 360, 510, 405, GOLD, LIGHT_GOLD)
    c.text_c(380, 370, "Circular Bioeconomy Loop", BLACK, 1)
    c.text_c(380, 385, "waste to value to soil", BLACK, 1)
    c.arrow(250, 382, 112, 382, GOLD, 2, 8)
    c.line(112, 382, 112, 215, GOLD, 2)
    c.arrow(112, 215, 112, 210, GOLD, 2, 7)

    c.text(30, 440, "Figure 1. Feedstocks, conversion routes, nanoscale engineering, and multifunctional applications of nanobiochar.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Biomass_to_Nanobiochar.png'))
    print("  Figure_1 done")


def gen_fig2():
    """Figure 2: Multifunctional roles across the agriculture-environment nexus."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Multifunctional Roles Across the Agriculture-Environment Nexus", BLACK, 2)

    cx, cy = 380, 235
    # Central node
    c.circle(cx, cy, 62, DARK_BLUE, MED_BLUE)
    c.text_c(cx, cy - 12, "NANO-", WHITE, 1)
    c.text_c(cx, cy, "BIOCHAR", WHITE, 1)
    c.text_c(cx, cy + 12, "core", WHITE, 1)

    nodes = [
        ("Nutrient Delivery", 380, 70, DARK_GREEN, LIGHT_GREEN),
        ("Soil Health", 620, 130, MED_GREEN, LIGHT_GREEN),
        ("Carbon Sequestration", 660, 300, GOLD, LIGHT_GOLD),
        ("GHG Mitigation", 560, 400, ORANGE, LIGHT_ORANGE),
        ("Pesticide Remediation", 200, 400, RED, LIGHT_RED),
        ("Metal Immobilization", 100, 300, PURPLE, LIGHT_PURPLE),
        ("Water Purification", 140, 130, MED_BLUE, LIGHT_BLUE),
    ]
    nw, nh = 150, 46
    for label, nx, ny, col, fill in nodes:
        dx, dy = nx - cx, ny - cy
        d = math.sqrt(dx * dx + dy * dy)
        sx = int(cx + dx / d * 64)
        sy = int(cy + dy / d * 64)
        ex = int(nx - dx / d * (nw // 2 - 8))
        ey = int(ny - dy / d * (nh // 2))
        c.line(sx, sy, ex, ey, GRAY, 2)
        c.rect(nx - nw // 2, ny - nh // 2, nx + nw // 2, ny + nh // 2, col, fill)
        c.text_c(nx, ny - 4, label, BLACK, 1)

    # Domain legend (radial hub spans both domains)
    c.fill_rect(40, 40, 55, 52, DARK_GREEN)
    c.text(62, 42, "Agriculture functions", BLACK, 1)
    c.fill_rect(560, 40, 575, 52, MED_BLUE)
    c.text(582, 42, "Environmental functions", BLACK, 1)

    c.text(30, 445, "Figure 2. Nanobiochar as a hub linking agricultural productivity and environmental remediation functions.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Multifunctional_Roles.png'))
    print("  Figure_2 done")


def gen_fig3():
    """Figure 3: Integration with AI, IoT sensing, and digital-agriculture platforms."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Nanobiochar Integration with AI, IoT and Digital Agriculture", BLACK, 2)

    layers = [
        ("MATERIAL LAYER", 45, PURPLE, LIGHT_PURPLE,
         "Nanobiochar amendments, controlled-release fertilizers, biosensors"),
        ("SENSING LAYER (IoT)", 130, MED_GREEN, LIGHT_GREEN,
         "Soil moisture / pH / nutrient sensors, UAV & satellite imagery"),
        ("INTELLIGENCE LAYER (AI)", 215, MED_BLUE, LIGHT_BLUE,
         "Property prediction, inverse design, decision-support models"),
        ("PLATFORM LAYER", 300, ORANGE, LIGHT_ORANGE,
         "Digital-agriculture dashboards, site-specific recommendations"),
    ]
    lx, lw, lh = 60, 560, 62
    centers = []
    for label, ly, col, fill, desc in layers:
        c.rect(lx, ly, lx + lw, ly + lh, col, fill)
        c.fill_rect(lx, ly, lx + lw, ly + 22, col)
        c.text(lx + 10, ly + 7, label, WHITE, 1)
        c.text(lx + 10, ly + 34, desc, BLACK, 1)
        centers.append((lx + lw, ly + lh // 2))
        if ly < 290:
            c.arrow(lx + lw // 2, ly + lh, lx + lw // 2, ly + lh + 21, GRAY, 2, 8)

    # Field / outcome box
    c.rect(60, 385, 620, 430, DARK_GREEN, LIGHT_GREEN)
    c.text_c(340, 393, "OPTIMIZED FIELD OUTCOMES", BLACK, 1)
    c.text_c(340, 410, "higher yield  -  resource efficiency  -  lower emissions", BLACK, 1)
    c.arrow(340, 362, 340, 383, GRAY, 2, 8)

    # Closed feedback loop on the right
    c.line(620, 407, 700, 407, RED, 2)
    c.line(700, 407, 700, 76, RED, 2)
    c.arrow(700, 76, 622, 76, RED, 2, 8)
    c.text(648, 235, "feedback", RED, 1)
    c.text(648, 250, "loop", RED, 1)

    c.text(30, 448, "Figure 3. Layered coupling of nanobiochar, IoT sensing, AI models, and digital platforms in a closed feedback loop.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Smart_Integration.png'))
    print("  Figure_3 done")


def gen_fig4():
    """Figure 4: Circular-bioeconomy and responsible-innovation framework."""
    c = PNGCanvas(760, 480)
    c.text_c(380, 10, "Nanobiochar in a Circular-Bioeconomy and Responsible-Innovation Framework", BLACK, 1)

    cx, cy, r = 300, 250, 150
    cycle = [
        ("Residue\nValorization", DARK_GREEN, LIGHT_GREEN),
        ("Synthesis &\nEngineering", ORANGE, LIGHT_ORANGE),
        ("Field\nApplication", MED_GREEN, LIGHT_GREEN),
        ("Recovery &\nReuse", MED_BLUE, LIGHT_BLUE),
    ]
    positions = []
    for i, (label, col, fill) in enumerate(cycle):
        ang = -math.pi / 2 + i * (math.pi / 2)
        nx = int(cx + r * math.cos(ang))
        ny = int(cy + r * math.sin(ang))
        positions.append((nx, ny))
        c.circle(nx, ny, 58, col, fill)
        lines = label.split("\n")
        for li, ln in enumerate(lines):
            c.text_c(nx, ny - 8 + li * 13, ln, BLACK, 1)

    # Curved (approx) arrows around the loop
    for i in range(4):
        x1, y1 = positions[i]
        x2, y2 = positions[(i + 1) % 4]
        dx, dy = x2 - x1, y2 - y1
        d = math.sqrt(dx * dx + dy * dy)
        sx = int(x1 + dx / d * 60); sy = int(y1 + dy / d * 60)
        ex = int(x2 - dx / d * 60); ey = int(y2 - dy / d * 60)
        c.arrow(sx, sy, ex, ey, GRAY, 3, 10)
    c.text_c(cx, cy - 6, "CIRCULAR", GOLD, 1)
    c.text_c(cx, cy + 8, "LOOP", GOLD, 1)

    # Responsible-innovation pillars panel
    c.rect(490, 70, 735, 360, DARK_BLUE, PALE_BLUE)
    c.fill_rect(490, 70, 735, 94, DARK_BLUE)
    c.text_c(612, 78, "RESPONSIBLE INNOVATION", WHITE, 1)
    pillars = [
        ("Environmental safety", RED),
        ("Ecotoxicity screening", ORANGE),
        ("Life-cycle assessment", MED_GREEN),
        ("Regulatory frameworks", PURPLE),
        ("Economic feasibility", GOLD),
        ("Social acceptance", MED_BLUE),
    ]
    for i, (p, col) in enumerate(pillars):
        py = 108 + i * 40
        c.fill_rect(505, py, 520, py + 15, col)
        c.text(530, py + 3, p, BLACK, 1)

    c.text(30, 455, "Figure 4. Closed material loop of nanobiochar coupled with the pillars of responsible innovation.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Circular_Framework.png'))
    print("  Figure_4 done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating nanobiochar figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print(f"\nAll 4 figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz/1024:.1f} KB")


if __name__ == '__main__':
    main()
