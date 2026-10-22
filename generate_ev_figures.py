#!/usr/bin/env python3
"""
Generate 4 high-resolution figures (PNG) for Chapter 3:
"Battery Technologies, Charging Fundamentals, Psychological Barriers, User
Trust, AI-based Second-Life Battery Health and AI in Material Discovery".

Reuses the pure-stdlib PNGCanvas drawing engine already present in the repo
(generate_figures.py), so no third-party libraries are required.
"""

import os
import math

# Reuse the existing canvas + colour palette from the repo.
from generate_figures import (
    PNGCanvas,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE, RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/ev_figures'

# High-resolution canvas dimensions
W, H = 1600, 1000


def _box(c, x1, y1, x2, y2, outline, fill, lines, tcolor=BLACK, scale=2):
    """Draw a filled, outlined rectangle with centred, wrapped text lines."""
    c.rect(x1, y1, x2, y2, outline, fill)
    cx = (x1 + x2) // 2
    total = len(lines) * (8 * scale + 4)
    y = (y1 + y2) // 2 - total // 2 + 4
    for ln in lines:
        c.text_c(cx, y, ln, tcolor, scale)
        y += 8 * scale + 4


def gen_fig1():
    """Figure 1: Psychological barriers and user trust in EV adoption."""
    c = PNGCanvas(W, H)
    c.text_c(W // 2, 24, "Psychological Barriers, User Trust and EV Adoption", BLACK, 3)

    # Left column: five barrier boxes
    barriers = [
        ("Range", "Anxiety", DARK_BLUE, PALE_BLUE),
        ("Charging", "Uncertainty", MED_BLUE, LIGHT_BLUE),
        ("Perceived", "Reliability", PURPLE, LIGHT_PURPLE),
        ("Cost", "Perception", ORANGE, LIGHT_ORANGE),
        ("Safety", "Concern", RED, LIGHT_RED),
    ]
    bx1, bx2 = 60, 360
    top, gap, bh = 110, 22, 100
    centers = []
    for i, (l1, l2, outline, fill) in enumerate(barriers):
        y1 = top + i * (bh + gap)
        y2 = y1 + bh
        _box(c, bx1, y1, bx2, y2, outline, fill, [l1, l2], scale=2)
        centers.append((bx2, (y1 + y2) // 2))

    # Centre hub: user trust
    hx1, hy1, hx2, hy2 = 560, 300, 1000, 640
    c.rect(hx1, hy1, hx2, hy2, DARK_GREEN, LIGHT_GREEN)
    c.text_c((hx1 + hx2) // 2, hy1 + 30, "USER TRUST", BLACK, 3)
    c.text_c((hx1 + hx2) // 2, hy1 + 90, "Transparency and Safety", BLACK, 2)
    c.text_c((hx1 + hx2) // 2, hy1 + 140, "Ease of Charging", BLACK, 2)
    c.text_c((hx1 + hx2) // 2, hy1 + 190, "Digital Connectivity", BLACK, 2)
    c.text_c((hx1 + hx2) // 2, hy1 + 255, "mediates barriers", GRAY, 2)

    hub_left = ((hx1 + hx2) // 2, hy1)
    # Arrows from each barrier to the trust hub
    for (sx, sy) in centers:
        c.arrow(sx + 6, sy, hx1 - 6, (hy1 + hy2) // 2 + (sy - 500) // 6, GRAY, 3, 14)

    # Right: EV adoption outcome
    ax1, ay1, ax2, ay2 = 1180, 360, 1540, 580
    c.rect(ax1, ay1, ax2, ay2, GOLD, LIGHT_GOLD)
    c.text_c((ax1 + ax2) // 2, ay1 + 50, "WIDESPREAD", BLACK, 3)
    c.text_c((ax1 + ax2) // 2, ay1 + 100, "EV ADOPTION", BLACK, 3)
    c.text_c((ax1 + ax2) // 2, ay1 + 155, "sustainable mobility", GRAY, 2)
    c.arrow(hx2 + 6, (hy1 + hy2) // 2, ax1 - 6, (ay1 + ay2) // 2, DARK_GREEN, 4, 16)

    # Bottom band: mitigation levers
    c.rect(60, 760, 1540, 930, LIGHT_GRAY, (248, 248, 248))
    c.text(80, 775, "Mitigation levers:", BLACK, 2)
    levers = [
        "- Longer range and accurate range prediction",
        "- Interoperable, reliable charging networks",
        "- Warranties and transparent battery health data",
        "- Incentives and total-cost-of-ownership framing",
        "- Safety standards and transparent engineering",
        "- Direct experience and familiarity with EVs",
    ]
    for i, lv in enumerate(levers):
        col = i % 2
        row = i // 2
        c.text(100 + col * 740, 820 + row * 36, lv, BLACK, 2)

    c.text_c(W // 2, 965,
             "Figure 1. Psychological barriers to EV adoption and their influencing factors.",
             BLACK, 2)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Psychological_Barriers.png'))
    print("  Figure_1 done")


def gen_fig2():
    """Figure 2: AI-driven second-life battery assessment workflow."""
    c = PNGCanvas(W, H)
    c.text_c(W // 2, 24, "AI-Driven Second-Life Battery Assessment Workflow", BLACK, 3)

    stages = [
        (["Retired EV", "Battery Pack", "(70-80% SOH)"], DARK_BLUE, PALE_BLUE),
        (["Data", "Acquisition", "V, I, T, cycles"], MED_BLUE, LIGHT_BLUE),
        (["AI Health", "Assessment", "SOH / RUL"], DARK_GREEN, LIGHT_GREEN),
        (["Grading and", "Sorting", "reuse vs recycle"], ORANGE, LIGHT_ORANGE),
        (["Second-Life", "Applications", "grid / solar"], PURPLE, LIGHT_PURPLE),
    ]
    n = len(stages)
    bw, bh = 250, 170
    gapx = (W - 120 - n * bw) // (n - 1)
    y1 = 220
    centers = []
    for i, (lines, outline, fill) in enumerate(stages):
        x1 = 60 + i * (bw + gapx)
        x2 = x1 + bw
        _box(c, x1, y1, x2, y1 + bh, outline, fill, lines, scale=2)
        centers.append((x1, x2, y1 + bh // 2))

    for i in range(n - 1):
        c.arrow(centers[i][1] + 6, centers[i][2],
                centers[i + 1][0] - 6, centers[i + 1][2], GRAY, 4, 16)

    # Digital-twin band feeding the AI block
    c.rect(60, 500, W - 60, 620, GOLD, LIGHT_GOLD)
    c.text_c(W // 2, 520, "DIGITAL TWIN: physics-informed ML + live telemetry", BLACK, 2)
    c.text_c(W // 2, 560, "condition monitoring - fault detection - RUL prediction - charging optimization",
             BLACK, 2)
    ai_cx = (centers[2][0] + centers[2][1]) // 2
    c.arrow(ai_cx, 500 - 6, ai_cx, y1 + bh + 6, DARK_GREEN, 3, 14)

    # ML techniques used
    c.rect(60, 680, 780, 900, LIGHT_GRAY, (248, 248, 248))
    c.text(80, 695, "Machine-learning techniques:", BLACK, 2)
    for i, t in enumerate([
            "- Neural networks (RNN / CNN)",
            "- Gaussian-process regression",
            "- Random forests / SVM",
            "- Physics + data hybrid models"]):
        c.text(100, 740 + i * 36, t, BLACK, 2)

    # Circular-economy outcome
    c.rect(820, 680, W - 60, 900, DARK_GREEN, (235, 250, 235))
    c.text_c((820 + W - 60) // 2, 700, "Circular-Economy Outcome", BLACK, 2)
    for i, t in enumerate([
            "- Extended battery service life",
            "- Deferred recycling, less waste",
            "- Lower-cost stationary storage",
            "- Sustainable resource use"]):
        c.text(850, 745 + i * 36, t, DARK_GREEN, 2)

    c.text_c(W // 2, 965,
             "Figure 2. AI-driven workflow for second-life battery health assessment and repurposing.",
             BLACK, 2)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_SecondLife_Workflow.png'))
    print("  Figure_2 done")


def gen_fig3():
    """Figure 3: AI closed-loop battery material-discovery pipeline."""
    c = PNGCanvas(W, H)
    c.text_c(W // 2, 24, "AI Closed-Loop Battery Material Discovery Pipeline", BLACK, 3)

    cx, cy = W // 2, 460
    rx, ry = 600, 250
    nodes = [
        (["Materials", "Databases"], DARK_BLUE, PALE_BLUE),
        (["Feature /", "Graph", "Representation"], MED_BLUE, LIGHT_BLUE),
        (["ML Property", "Prediction"], DARK_GREEN, LIGHT_GREEN),
        (["Generative", "Design and", "Screening"], PURPLE, LIGHT_PURPLE),
        (["Candidate", "Materials"], ORANGE, LIGHT_ORANGE),
        (["Autonomous", "Synthesis and", "Characterization"], RED, LIGHT_RED),
    ]
    nnodes = len(nodes)
    bw, bh = 250, 150
    centers = []
    for i, (lines, outline, fill) in enumerate(nodes):
        ang = -math.pi / 2 + i * 2 * math.pi / nnodes
        nx = int(cx + rx * math.cos(ang))
        ny = int(cy + ry * math.sin(ang))
        _box(c, nx - bw // 2, ny - bh // 2, nx + bw // 2, ny + bh // 2,
             outline, fill, lines, scale=2)
        centers.append((nx, ny))

    for i in range(nnodes):
        x1, y1 = centers[i]
        x2, y2 = centers[(i + 1) % nnodes]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        off = max(90, min(155, d * 0.3))  # clear the boxes, adapt to edge length
        c.arrow(int(x1 + dx / d * off), int(y1 + dy / d * off),
                int(x2 - dx / d * off), int(y2 - dy / d * off), GRAY, 3, 14)

    # Centre: active learning
    c.rect(cx - 200, cy - 75, cx + 200, cy + 75, GOLD, LIGHT_GOLD)
    c.text_c(cx, cy - 38, "ACTIVE LEARNING", BLACK, 2)
    c.text_c(cx, cy + 2, "sample-efficient", BLACK, 2)
    c.text_c(cx, cy + 42, "feedback loop", BLACK, 2)

    # Target properties
    c.rect(60, 835, W - 60, 925, LIGHT_GRAY, (248, 248, 248))
    c.text_c(W // 2, 853, "Design targets: higher energy density  -  improved safety  -  longer lifespan",
             BLACK, 2)
    c.text_c(W // 2, 893, "Applied to electrodes, electrolytes and solid-state ionic conductors",
             GRAY, 2)

    c.text_c(W // 2, 965,
             "Figure 3. AI-driven closed-loop pipeline for battery material discovery and optimization.",
             BLACK, 2)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Material_Discovery.png'))
    print("  Figure_3 done")


def gen_fig4():
    """Figure 4: AI capabilities across the EV battery value chain."""
    c = PNGCanvas(W, H)
    c.text_c(W // 2, 24, "AI Across the Electric-Vehicle Battery Value Chain", BLACK, 3)

    stages = [
        ("Material", "Discovery", DARK_BLUE, PALE_BLUE,
         ["Property prediction", "Generative design", "Autonomous labs"]),
        ("Cell and Pack", "Design", MED_BLUE, LIGHT_BLUE,
         ["Design optimization", "Thermal modeling", "Digital twins"]),
        ("Manufacturing", "and Quality", DARK_GREEN, LIGHT_GREEN,
         ["Defect detection", "Process control", "Yield forecasting"]),
        ("BMS and", "Charging", ORANGE, LIGHT_ORANGE,
         ["SOC / SOH est.", "Fast-charge control", "Smart / V2G charge"]),
        ("First-Life", "Operation", PURPLE, LIGHT_PURPLE,
         ["Range prediction", "Fault detection", "Predictive upkeep"]),
        ("Second-Life", "and Recycling", RED, LIGHT_RED,
         ["RUL grading", "Reuse decisions", "Material recovery"]),
    ]
    n = len(stages)
    bw = 230
    gapx = (W - 100 - n * bw) // (n - 1)
    y1, bh = 150, 120
    centers = []
    for i, (l1, l2, outline, fill, caps) in enumerate(stages):
        x1 = 50 + i * (bw + gapx)
        x2 = x1 + bw
        _box(c, x1, y1, x2, y1 + bh, outline, fill, [l1, l2], scale=2)
        centers.append((x1, x2))
        # capability list below each stage
        cardy1 = y1 + bh + 50
        c.rect(x1, cardy1, x2, cardy1 + 230, outline, WHITE)
        c.text_c((x1 + x2) // 2, cardy1 + 16, "AI roles", GRAY, 2)
        for j, cap in enumerate(caps):
            c.text(x1 + 14, cardy1 + 60 + j * 46, cap, BLACK, 2)
        # connector from stage to its card
        c.arrow((x1 + x2) // 2, y1 + bh + 6, (x1 + x2) // 2, cardy1 - 6, GRAY, 3, 12)

    # horizontal flow arrows between stages
    for i in range(n - 1):
        c.arrow(centers[i][1] + 6, y1 + bh // 2,
                centers[i + 1][0] - 6, y1 + bh // 2, DARK_BLUE, 3, 14)

    # loop-back arrow (recycling -> material discovery) along the bottom
    by = 720
    c.line((centers[-1][0] + centers[-1][1]) // 2, 580,
           (centers[-1][0] + centers[-1][1]) // 2, by, DARK_GREEN, 3)
    c.line((centers[-1][0] + centers[-1][1]) // 2, by,
           (centers[0][0] + centers[0][1]) // 2, by, DARK_GREEN, 3)
    c.arrow((centers[0][0] + centers[0][1]) // 2, by,
            (centers[0][0] + centers[0][1]) // 2, 580, DARK_GREEN, 3, 14)
    c.text_c(W // 2, by + 20, "Closed-loop circular economy: recovered materials re-enter discovery",
             DARK_GREEN, 2)

    c.rect(60, 790, W - 60, 905, GOLD, LIGHT_GOLD)
    c.text_c(W // 2, 812,
             "Cross-cutting enablers: data integration  -  machine learning  -  digital twins  -  predictive analytics",
             BLACK, 2)
    c.text_c(W // 2, 858,
             "Outcome: safer, higher-energy, longer-lived batteries and trusted, sustainable electric mobility",
             GRAY, 2)

    c.text_c(W // 2, 965,
             "Figure 4. Artificial-intelligence capabilities mapped across the EV battery value chain.",
             BLACK, 2)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_AI_Value_Chain.png'))
    print("  Figure_4 done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating EV chapter figures (high resolution)...")
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
