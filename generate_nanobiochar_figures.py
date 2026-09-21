#!/usr/bin/env python3
"""
Generate 4 figure images (PNG) for Chapter 1
"Next-Generation Nanobiochar: Emerging Trends, Smart Technologies and Future
Innovations".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - Synthesis and functionalization pathways (top-down / bottom-up /
             chemical / green)
  Figure 2 - Multifunctional roles of nanobiochar in sustainable agriculture
  Figure 3 - Integration of nanobiochar with AI / IoT / biosensing (digital)
  Figure 4 - Circular-bioeconomy roadmap (closed material loop)
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/nanobiochar_figures'


def _lines(c, cx, y, lines, color, scale=1, lh=12):
    for i, ln in enumerate(lines):
        c.text_c(cx, y + i * lh, ln, color, scale)


def gen_fig1():
    """Figure 1: Synthesis and functionalization pathways."""
    c = PNGCanvas(780, 500)
    c.text_c(390, 10, "Synthesis and Functionalization of Nanobiochar", BLACK, 2)

    # Feedstock source box (top)
    c.rect(280, 45, 500, 90, DARK_GREEN, LIGHT_GREEN)
    c.text_c(390, 55, "Renewable Biomass and", BLACK, 1)
    c.text_c(390, 69, "Agricultural Residues", BLACK, 1)

    # Pyrolysis / conversion
    c.rect(280, 110, 500, 155, DARK_BLUE, PALE_BLUE)
    c.text_c(390, 120, "Thermochemical Conversion", BLACK, 1)
    c.text_c(390, 134, "(pyrolysis, HTC, gasification)", GRAY, 1)
    c.arrow(390, 90, 390, 110, GRAY, 2, 8)

    c.rect(300, 172, 480, 205, MED_BLUE, LIGHT_BLUE)
    c.text_c(390, 183, "Bulk Biochar", BLACK, 1)
    c.arrow(390, 155, 390, 172, GRAY, 2, 8)

    # Four route columns
    routes = [
        (40, "TOP-DOWN", MED_BLUE, LIGHT_BLUE,
         ["Ball milling", "Ultrasonication", "Homogenization"]),
        (230, "BOTTOM-UP", PURPLE, LIGHT_PURPLE,
         ["Hydrothermal", "Templating", "Carbon dots"]),
        (420, "CHEMICAL", ORANGE, LIGHT_ORANGE,
         ["Acid/base", "Heteroatom", "Magnetic load"]),
        (610, "GREEN NANO", DARK_GREEN, LIGHT_GREEN,
         ["Plant extract", "Microbial", "Biosynthesis"]),
    ]
    bw = 150
    top = 250
    for bx, title, col, fill, items in routes:
        c.rect(bx, top, bx + bw, top + 105, col, fill)
        c.text_c(bx + bw // 2, top + 10, title, BLACK, 1)
        for j, it in enumerate(items):
            c.text_c(bx + bw // 2, top + 32 + j * 18, it, BLACK, 1)
        c.arrow(390, 205, bx + bw // 2, top - 3, GRAY, 1, 6)

    # Converge to product
    c.rect(250, 400, 530, 450, GOLD, LIGHT_GOLD)
    c.text_c(390, 412, "Next-Generation Nanobiochar", BLACK, 1)
    c.text_c(390, 428, "high surface area, tunable chemistry,", GRAY, 1)
    c.text_c(390, 440, "multifunctional composites", GRAY, 1)
    for bx, *_ in routes:
        c.arrow(bx + bw // 2, top + 105, 390, 400, GRAY, 1, 6)

    c.text(40, 480, "Figure 1: Top-down, bottom-up, chemical and green synthesis routes to nanobiochar", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Synthesis_Pathways.png'))
    print("  Figure_1_Synthesis_Pathways.png done")


def gen_fig2():
    """Figure 2: Multifunctional roles in sustainable agriculture."""
    c = PNGCanvas(780, 500)
    c.text_c(390, 10, "Multifunctional Roles of Nanobiochar in Agriculture", BLACK, 2)

    # Central soil / plant hub
    cx, cy = 390, 250
    c.circle(cx, cy, 70, DARK_GREEN, LIGHT_GREEN)
    c.text_c(cx, cy - 14, "Nanobiochar", BLACK, 1)
    c.text_c(cx, cy, "in Soil-Plant", BLACK, 1)
    c.text_c(cx, cy + 14, "System", BLACK, 1)

    funcs = [
        (390, 60, MED_BLUE, LIGHT_BLUE,
         ["Nutrient Retention", "& Controlled Release"]),
        (650, 160, ORANGE, LIGHT_ORANGE,
         ["Soil Structure", "& Water Holding"]),
        (650, 350, PURPLE, LIGHT_PURPLE,
         ["Microbial", "Stimulation"]),
        (390, 440, RED, LIGHT_RED,
         ["Carbon Sequestration", "& GHG Mitigation"]),
        (130, 350, GOLD, LIGHT_GOLD,
         ["Contaminant", "Immobilization"]),
        (130, 160, DARK_BLUE, PALE_BLUE,
         ["Higher Yield &", "Resource Efficiency"]),
    ]
    bw, bh = 170, 46
    for bx, by, col, fill, lines in funcs:
        c.rect(bx - bw // 2, by - bh // 2, bx + bw // 2, by + bh // 2, col, fill)
        _lines(c, bx, by - 10, lines, BLACK, 1, 14)
        # connector
        c.arrow(cx, cy, bx, by, GRAY, 1, 7)

    c.text(40, 482, "Figure 2: Nutrient delivery, soil health, microbes, carbon and remediation functions", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Agriculture_Roles.png'))
    print("  Figure_2_Agriculture_Roles.png done")


def gen_fig3():
    """Figure 3: Integration with AI / IoT / biosensing."""
    c = PNGCanvas(780, 500)
    c.text_c(390, 10, "Integration of Nanobiochar with Smart Technologies", BLACK, 2)

    layers = [
        ("AI / MACHINE LEARNING", "property prediction, inverse design, active learning",
         PURPLE, LIGHT_PURPLE),
        ("IoT PRECISION FARMING", "soil/moisture/nutrient sensors, remote monitoring",
         MED_BLUE, LIGHT_BLUE),
        ("NANOBIOCHAR MATERIAL", "biosensors, bioelectrochemical systems, amendments",
         DARK_GREEN, LIGHT_GREEN),
        ("FIELD DEPLOYMENT", "controlled release, remediation, carbon storage",
         ORANGE, LIGHT_ORANGE),
    ]
    lx1, lx2 = 120, 660
    top = 60
    lh = 70
    gap = 22
    mids = []
    for i, (title, sub, col, fill) in enumerate(layers):
        y1 = top + i * (lh + gap)
        y2 = y1 + lh
        c.rect(lx1, y1, lx2, y2, col, fill)
        c.text_c((lx1 + lx2) // 2, y1 + 20, title, BLACK, 1)
        c.text_c((lx1 + lx2) // 2, y1 + 42, sub, GRAY, 1)
        mids.append((y1, y2))
        if i > 0:
            py = mids[i - 1][1]
            c.arrow((lx1 + lx2) // 2 - 40, py + gap, (lx1 + lx2) // 2 - 40, py + 2, GRAY, 2, 7)
            c.arrow((lx1 + lx2) // 2 + 40, py + 2, (lx1 + lx2) // 2 + 40, py + gap, GRAY, 2, 7)

    # Feedback loop on the right
    c.line(lx2 + 10, top + 20, lx2 + 40, top + 20, RED, 2)
    c.line(lx2 + 40, top + 20, lx2 + 40, mids[-1][0] + 30, RED, 2)
    c.line(lx2 + 40, mids[-1][0] + 30, lx2 + 10, mids[-1][0] + 30, RED, 2)
    c.arrow(lx2 + 10, mids[-1][0] + 30, lx2 + 8, mids[-1][0] + 30, RED, 2, 7)
    c.text(lx2 + 20, (top + mids[-1][0]) // 2, "data", RED, 1)
    c.text(lx2 + 20, (top + mids[-1][0]) // 2 + 14, "feedback", RED, 1)

    c.text(40, 482, "Figure 3: Data-driven feedback linking material design, sensing and deployment", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Digital_Integration.png'))
    print("  Figure_3_Digital_Integration.png done")


def gen_fig4():
    """Figure 4: Circular-bioeconomy roadmap (closed loop)."""
    c = PNGCanvas(780, 500)
    c.text_c(390, 10, "Circular-Bioeconomy Roadmap for Nanobiochar", BLACK, 2)

    cx, cy = 390, 260
    stages = [
        (390, 70, DARK_GREEN, LIGHT_GREEN, ["1. Biomass &", "Residue Supply"]),
        (630, 160, DARK_BLUE, PALE_BLUE, ["2. Low-Emission", "Production"]),
        (660, 320, PURPLE, LIGHT_PURPLE, ["3. Nanoscale", "Engineering"]),
        (470, 440, ORANGE, LIGHT_ORANGE, ["4. Multifunctional", "Deployment"]),
        (250, 440, RED, LIGHT_RED, ["5. Monitoring &", "Carbon Accounting"]),
        (120, 320, GOLD, LIGHT_GOLD, ["6. Recovery &", "Regeneration"]),
        (150, 160, MED_BLUE, LIGHT_BLUE, ["7. Nutrient & Value", "Return to Soil"]),
    ]
    bw, bh = 165, 48
    centers = []
    for bx, by, col, fill, lines in stages:
        c.rect(bx - bw // 2, by - bh // 2, bx + bw // 2, by + bh // 2, col, fill)
        _lines(c, bx, by - 10, lines, BLACK, 1, 14)
        centers.append((bx, by))

    # Circular arrows connecting stages in sequence
    n = len(centers)
    for i in range(n):
        x1, y1 = centers[i]
        x2, y2 = centers[(i + 1) % n]
        c.arrow(x1, y1, x2, y2, GRAY, 1, 7)

    # Center hub
    c.circle(cx, cy, 55, GRAY, (245, 245, 245))
    c.text_c(cx, cy - 8, "Closed", DARK_GREEN, 1)
    c.text_c(cx, cy + 8, "Material Loop", DARK_GREEN, 1)

    c.text(40, 482, "Figure 4: Closed-loop valorization, deployment, monitoring and recovery of nanobiochar", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Circular_Bioeconomy.png'))
    print("  Figure_4_Circular_Bioeconomy.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating next-generation nanobiochar chapter figures...")
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
