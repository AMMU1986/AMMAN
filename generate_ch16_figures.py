#!/usr/bin/env python3
"""
Generate the four figures for Chapter 16, "Digital Twins and Intelligent
Automation for Industry 5.0", as baseline JPEG files (per the publisher's
requirement that figures be supplied in JPEG format).

Drawing primitives are reused from the repository's proven pure-Python
PNGCanvas (generate_figures.py); the pixel buffer is then encoded to JPEG by
the standalone ch16_jpeg module. No third-party libraries are used.
"""

import os

from generate_figures import (
    PNGCanvas,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE, RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)
from ch16_jpeg import encode_rgb_to_jpeg

OUTPUT_DIR = '/projects/sandbox/AMMAN/ch16_figures'
QUALITY = 92


def save_jpeg(canvas, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    encode_rgb_to_jpeg(canvas.w, canvas.h, canvas.data, path, quality=QUALITY)
    size_kb = os.path.getsize(path) / 1024
    print(f"  {filename}: {canvas.w}x{canvas.h}, {size_kb:.1f} KB")


def box(c, x1, y1, x2, y2, outline, fill, lines, tcol=BLACK, scale=2):
    """Draw a filled, outlined box with centred multi-line text."""
    c.rect(x1, y1, x2, y2, outline, fill)
    cx = (x1 + x2) // 2
    total_h = len(lines) * (8 * scale)
    ty = (y1 + y2) // 2 - total_h // 2
    for ln in lines:
        c.text_c(cx, ty, ln, tcol, scale)
        ty += 8 * scale


def gen_fig1():
    """Fig. 16-1: Five-layer reference architecture of a digital twin."""
    c = PNGCanvas(1000, 780)
    c.text_c(500, 18, "Digital Twin Reference Architecture", BLACK, 3)

    layers = [
        ("Application Layer",
         ["APPLICATION LAYER", "Monitoring  Prediction  Optimisation  Control"],
         DARK_BLUE, PALE_BLUE),
        ("Digital-Modelling Layer",
         ["DIGITAL-MODELLING LAYER", "Virtual Model  Simulation  ML Analytics"],
         PURPLE, LIGHT_PURPLE),
        ("Communication Layer",
         ["COMMUNICATION LAYER", "Secure Transport  Edge-Cloud  Protocols"],
         MED_GREEN, LIGHT_GREEN),
        ("Data-Acquisition Layer",
         ["DATA-ACQUISITION LAYER", "Sensors  Signal Conditioning  Streaming"],
         ORANGE, LIGHT_ORANGE),
        ("Physical Layer",
         ["PHYSICAL LAYER", "Assets  Machines  Processes  Actuators"],
         RED, LIGHT_RED),
    ]

    x1, x2 = 250, 760
    top = 70
    bh, gap = 108, 18
    centers = []
    for i, (_, lines, outline, fill) in enumerate(layers):
        y1 = top + i * (bh + gap)
        y2 = y1 + bh
        box(c, x1, y1, x2, y2, outline, fill, lines, scale=2)
        centers.append((y1, y2))

    stack_top = centers[0][0]
    stack_bot = centers[-1][1]

    # Left upward arrow: data / sensing flow (physical -> application)
    lx = 165
    c.arrow(lx, stack_bot, lx, stack_top, MED_BLUE, 3, 14)
    c.text(70, (stack_top + stack_bot) // 2 - 40, "Data", MED_BLUE, 2)
    c.text(60, (stack_top + stack_bot) // 2 - 16, "flow", MED_BLUE, 2)
    c.text(40, (stack_top + stack_bot) // 2 + 8, "(sensing)", MED_BLUE, 2)

    # Right downward arrow: control / actuation flow (application -> physical)
    rx = 845
    c.arrow(rx, stack_top, rx, stack_bot, RED, 3, 14)
    c.text(880, (stack_top + stack_bot) // 2 - 40, "Control", RED, 2)
    c.text(890, (stack_top + stack_bot) // 2 - 16, "flow", RED, 2)
    c.text(865, (stack_top + stack_bot) // 2 + 8, "(actuation)", RED, 2)

    # Physical / virtual annotations
    c.text_c(500, stack_bot + 30, "Physical entity and virtual model synchronised via bidirectional flow", GRAY, 2)
    save_jpeg(c, 'Fig_16_1_DT_Architecture.jpg')


def gen_fig2():
    """Fig. 16-2: Transition from Industry 4.0 to Industry 5.0."""
    c = PNGCanvas(1000, 640)
    c.text_c(500, 18, "From Industry 4.0 to Industry 5.0", BLACK, 3)

    # Foundation bar (Industry 4.0)
    box(c, 120, 470, 880, 560, DARK_BLUE, PALE_BLUE,
        ["INDUSTRY 4.0 TECHNOLOGICAL FOUNDATION",
         "Automation  Connectivity  IoT  Big Data  Cyber-Physical Systems"],
        scale=2)

    # Three pillars
    pillars = [
        (["HUMAN-", "CENTRICITY", "", "People-first", "collaboration"], MED_GREEN, LIGHT_GREEN),
        (["RESILIENCE", "", "Robust and", "adaptive", "operation"], ORANGE, LIGHT_ORANGE),
        (["SUSTAIN-", "ABILITY", "", "Planet-", "positive", "production"], PURPLE, LIGHT_PURPLE),
    ]
    pw = 190
    xs = [175, 405, 635]
    ptop, pbot = 170, 450
    for (lines, outline, fill), px in zip(pillars, xs):
        box(c, px, ptop, px + pw, pbot, outline, fill, lines, scale=2)
        # arrow up from foundation into pillar
        c.arrow(px + pw // 2, 470, px + pw // 2, pbot + 2, GRAY, 2, 10)

    # Industry 5.0 crown
    box(c, 150, 70, 850, 150, RED, LIGHT_RED,
        ["INDUSTRY 5.0",
         "Human-centric   Resilient   Sustainable"],
        scale=2)
    for px in xs:
        c.arrow(px + pw // 2, 168, px + pw // 2, 152, RED, 2, 10)

    c.text_c(500, 590, "Industry 5.0 augments the Industry 4.0 base with human values", GRAY, 2)
    save_jpeg(c, 'Fig_16_2_Industry_4_to_5.jpg')


def gen_fig3():
    """Fig. 16-3: Perception-cognition-action integration loop."""
    c = PNGCanvas(1000, 720)
    c.text_c(500, 18, "Digital Twin and Intelligent Automation Loop", BLACK, 3)

    # Human oversight (top)
    box(c, 300, 70, 700, 140, DARK_BLUE, PALE_BLUE,
        ["HUMAN OVERSIGHT", "Sets goals and constraints; can intervene"], scale=2)

    # Physical asset (bottom-left) and Digital twin (bottom-right)
    box(c, 90, 520, 380, 630, RED, LIGHT_RED,
        ["PHYSICAL ASSET", "Machine / Process", "Sensors + Actuators"], scale=2)
    box(c, 620, 520, 910, 630, PURPLE, LIGHT_PURPLE,
        ["DIGITAL TWIN", "Synchronised", "Virtual Model"], scale=2)

    # Loop nodes (circle-ish boxes) in the middle
    box(c, 130, 250, 360, 340, MED_GREEN, LIGHT_GREEN,
        ["PERCEPTION", "Acquire and", "interpret state"], scale=2)
    box(c, 385, 200, 615, 290, ORANGE, LIGHT_ORANGE,
        ["COGNITION", "Predict, simulate,", "decide"], scale=2)
    box(c, 640, 250, 870, 340, GOLD, LIGHT_GOLD,
        ["ACTION", "Select and", "enact response"], scale=2)

    # Loop arrows: Perception -> Cognition -> Action -> (down to physical) -> up
    c.arrow(360, 285, 385, 258, GRAY, 3, 12)          # perception -> cognition
    c.arrow(615, 258, 640, 285, GRAY, 3, 12)          # cognition -> action
    # Action -> Digital twin -> Physical (control)
    c.arrow(760, 340, 760, 518, RED, 3, 12)           # action -> digital twin/physical
    c.text(770, 420, "actuate", RED, 2)
    # Physical -> Perception (sensing up)
    c.arrow(235, 518, 235, 342, MED_BLUE, 3, 12)      # physical -> perception
    c.text(120, 420, "sense", MED_BLUE, 2)
    # Physical <-> Digital twin synchronisation
    c.arrow(385, 560, 615, 560, MED_GREEN, 3, 12)
    c.arrow(615, 600, 385, 600, MED_GREEN, 3, 12)
    c.text_c(500, 570, "sync", DARK_GREEN, 2)

    # oversight links
    c.arrow(400, 140, 250, 248, GRAY, 2, 10)
    c.arrow(600, 140, 740, 248, GRAY, 2, 10)

    c.text_c(500, 665, "Continuous closed-loop synchronisation under human supervision", GRAY, 2)
    save_jpeg(c, 'Fig_16_3_Integration_Loop.jpg')


def gen_fig4():
    """Fig. 16-4: Indicative benefits across performance dimensions."""
    c = PNGCanvas(1000, 640)
    c.text_c(500, 18, "Indicative Benefits of Integration", BLACK, 3)

    # Axes
    ax_x = 120      # y-axis position
    ax_y = 520      # x-axis baseline
    top_y = 90
    c.vline(ax_x, top_y, ax_y, BLACK)
    c.hline(ax_x, 940, ax_y, BLACK)
    c.text(20, top_y - 20, "Indicative improvement (%)", BLACK, 2)

    # gridlines + scale (0..50%)
    for pct in range(0, 51, 10):
        gy = ax_y - int(pct / 50.0 * (ax_y - top_y))
        c.hline(ax_x, 940, gy, LIGHT_GRAY)
        c.text(ax_x - 55, gy - 6, f"{pct}", BLACK, 2)

    bars = [
        (["Down-", "time"], 40, RED),
        (["Maint.", "cost"], 30, ORANGE),
        (["Quality"], 25, MED_GREEN),
        (["Through-", "put"], 22, MED_BLUE),
        (["Energy", "eff."], 18, PURPLE),
        (["Time to", "market"], 30, GOLD),
    ]
    n = len(bars)
    span = 940 - ax_x - 30
    slot = span // n
    bw = int(slot * 0.55)
    for i, (labels, pct, col) in enumerate(bars):
        bx = ax_x + 30 + i * slot
        bh = int(pct / 50.0 * (ax_y - top_y))
        c.rect(bx, ax_y - bh, bx + bw, ax_y, BLACK, col)
        c.text_c(bx + bw // 2, ax_y - bh - 22, f"~{pct}%", BLACK, 2)
        ly = ax_y + 12
        for ln in labels:
            c.text_c(bx + bw // 2, ly, ln, BLACK, 2)
            ly += 18

    c.text_c(500, 600, "Illustrative gains reported across representative application domains", GRAY, 2)
    save_jpeg(c, 'Fig_16_4_Benefits.jpg')


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Chapter 16 figures (JPEG)...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print(f"All figures saved to {OUTPUT_DIR}/")


if __name__ == '__main__':
    main()
