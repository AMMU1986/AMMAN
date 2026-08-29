#!/usr/bin/env python3
"""
Generate 4 figures (PNG) for Chapter 8: Sustainable Manufacturing in Industry 5.0.
Reuses the pure-stdlib PNGCanvas drawing toolkit from generate_figures.py
(no matplotlib/PIL/numpy available in this sandbox).
"""

import os
import sys

# Reuse the PNGCanvas + font from the existing module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_figures import (
    PNGCanvas, BLACK, WHITE, GRAY, LIGHT_GRAY,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE, RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
)

OUT = '/projects/sandbox/AMMAN/chapter8_figures'
os.makedirs(OUT, exist_ok=True)


def box(c, x, y, w, h, outline, fill, label_lines, txt_scale=1, txt_color=BLACK):
    c.rect(x, y, x + w, y + h, outline, fill)
    n = len(label_lines)
    line_h = 12 * txt_scale
    start_y = y + h // 2 - (n * line_h) // 2
    for i, ln in enumerate(label_lines):
        c.text_c(x + w // 2, start_y + i * line_h, ln, txt_color, txt_scale)


# ---------------------------------------------------------------------------
def fig1():
    """Figure 1: Layered technology architecture for sustainable manufacturing."""
    W, H = 820, 560
    c = PNGCanvas(W, H)
    c.text_c(W // 2, 14, "Layered Technology Architecture for Sustainable Manufacturing", BLACK, 2)

    layers = [
        ("Decision and Optimisation Layer", "AI / Machine Learning  -  Digital Twins  -  Industrial Analytics",
         DARK_GREEN, LIGHT_GREEN),
        ("Data and Computation Layer", "Cloud Computing  -  Edge Computing  -  Data Platforms",
         MED_BLUE, LIGHT_BLUE),
        ("Connectivity and Sensing Layer", "Internet of Things  -  Networked Sensors  -  Monitoring",
         PURPLE, LIGHT_PURPLE),
        ("Physical Production Layer", "Machines  -  Robotics / Cobots  -  Materials and Processes",
         ORANGE, LIGHT_ORANGE),
    ]

    lx, lw = 120, 560
    ly = 70
    lh = 78
    gap = 26
    centers = []
    for i, (title, sub, oc, fc) in enumerate(layers):
        y = ly + i * (lh + gap)
        c.rect(lx, y, lx + lw, y + lh, oc, fc)
        c.text_c(lx + lw // 2, y + 20, title, BLACK, 2)
        c.text_c(lx + lw // 2, y + 48, sub, BLACK, 1)
        centers.append((y, y + lh))

    # Upward arrow (data ascends) on the left
    top_y = centers[0][0]
    bot_y = centers[-1][1]
    c.arrow(lx - 45, bot_y, lx - 45, top_y, DARK_BLUE, 3, 12)
    c.text(lx - 112, (top_y + bot_y) // 2 - 18, "Data", DARK_BLUE, 1)
    c.text(lx - 116, (top_y + bot_y) // 2 - 4, "ascends", DARK_BLUE, 1)

    # Downward arrow (decisions descend) on the right
    rx = lx + lw + 45
    c.arrow(rx, top_y, rx, bot_y, RED, 3, 12)
    c.text(rx + 12, (top_y + bot_y) // 2 - 18, "Decisions", RED, 1)
    c.text(rx + 12, (top_y + bot_y) // 2 - 4, "descend", RED, 1)

    # Outcome banner
    by = bot_y + 22
    c.rect(lx, by, lx + lw, by + 40, GOLD, LIGHT_GOLD)
    c.text_c(lx + lw // 2, by + 8, "Outcome: Real-time visibility of energy, emissions and material flows",
             BLACK, 1)
    c.text_c(lx + lw // 2, by + 22, "enabling closed-loop, self-optimising sustainable operation", BLACK, 1)

    c.text(20, H - 20, "Figure 1: Integrated, interdependent technology stack underpinning Industry 5.0 sustainable manufacturing.",
           BLACK, 1)
    c.save(os.path.join(OUT, 'Figure_1.png'))
    print("Figure_1.png done")


# ---------------------------------------------------------------------------
def fig2():
    """Figure 2: Digital enablers mapped to the narrow-slow-close circular framework."""
    W, H = 820, 540
    c = PNGCanvas(W, H)
    c.text_c(W // 2, 14, "Digital Enablers across the Narrow - Slow - Close Circular Framework", BLACK, 2)

    cols = [
        ("NARROW", "Reduce resources per product", MED_BLUE, LIGHT_BLUE,
         ["AI resource", "optimisation", "Generative", "design"]),
        ("SLOW", "Extend product lifetime", DARK_GREEN, LIGHT_GREEN,
         ["IoT condition", "monitoring", "Predictive", "maintenance"]),
        ("CLOSE", "Return materials to production", PURPLE, LIGHT_PURPLE,
         ["Digital twins", "for LCA", "Blockchain /", "product passports"]),
    ]
    cw = 230
    gap = 30
    total = len(cols) * cw + (len(cols) - 1) * gap
    x0 = (W - total) // 2
    top = 70
    head_h = 64
    body_h = 300

    for i, (name, desc, oc, fc, tools) in enumerate(cols):
        x = x0 + i * (cw + gap)
        # header
        c.rect(x, top, x + cw, top + head_h, oc, fc)
        c.text_c(x + cw // 2, top + 14, name, BLACK, 2)
        c.text_c(x + cw // 2, top + 40, desc, BLACK, 1)
        # body of enabler tools
        by = top + head_h + 14
        c.rect(x, by, x + cw, by + body_h, GRAY, WHITE)
        c.text_c(x + cw // 2, by + 12, "Key Digital Enablers", BLACK, 1)
        yy = by + 42
        # draw the tool chips (pairs of lines)
        pairs = [(tools[0], tools[1]), (tools[2], tools[3])]
        for (l1, l2) in pairs:
            c.rect(x + 20, yy, x + cw - 20, yy + 70, oc, fc)
            c.text_c(x + cw // 2, yy + 22, l1, BLACK, 1)
            c.text_c(x + cw // 2, yy + 40, l2, BLACK, 1)
            yy += 92
        # arrow to next
        if i < len(cols) - 1:
            ax = x + cw + 4
            c.arrow(ax, top + head_h // 2, ax + gap - 8, top + head_h // 2, BLACK, 3, 10)

    # bottom banner
    yb = top + head_h + 14 + body_h + 22
    c.rect(x0, yb, x0 + total, yb + 40, GOLD, LIGHT_GOLD)
    c.text_c(W // 2, yb + 8, "Integration into a shared circular information system", BLACK, 1)
    c.text_c(W // 2, yb + 22, "unlocks circular value across organisational boundaries", BLACK, 1)

    c.text(20, H - 18, "Figure 2: Mapping of digital technologies onto circular economy resource-loop strategies.",
           BLACK, 1)
    c.save(os.path.join(OUT, 'Figure_2.png'))
    print("Figure_2.png done")


# ---------------------------------------------------------------------------
def fig3():
    """Figure 3: Industrial symbiosis network - energy and material exchanges."""
    W, H = 820, 560
    c = PNGCanvas(W, H)
    c.text_c(W // 2, 14, "Industrial Symbiosis Network: Energy and Material Exchanges", BLACK, 2)

    import math
    # nodes: (label lines, cx, cy, outline, fill)
    nodes = [
        (["Power", "Plant"], 410, 105, DARK_BLUE, PALE_BLUE),      # 0 top-centre
        (["Refinery"], 170, 240, ORANGE, LIGHT_ORANGE),            # 1 left
        (["Chemical", "Plant"], 650, 240, PURPLE, LIGHT_PURPLE),   # 2 right
        (["Cement /", "Gypsum"], 210, 410, GRAY, LIGHT_GRAY),      # 3 bottom-left
        (["Fish Farm /", "Greenhouse"], 610, 410, DARK_GREEN, LIGHT_GREEN),  # 4 bottom-right
        (["Water", "Recycling"], 410, 320, MED_BLUE, LIGHT_BLUE),  # 5 centre
    ]
    bw, bh = 130, 60
    centers = []
    for lines, cx, cy, oc, fc in nodes:
        box(c, cx - bw // 2, cy - bh // 2, bw, bh, oc, fc, lines, 1)
        centers.append((cx, cy))

    # exchanges: (from, to, label, label_position_fraction along edge)
    exch = [
        (0, 5, "steam", 0.30),
        (0, 4, "waste heat", 0.68),
        (0, 3, "fly ash", 0.28),
        (1, 0, "fuel gas", 0.5),
        (1, 2, "sulphur", 0.42),
        (2, 3, "gypsum", 0.72),
        (5, 4, "water", 0.55),
        (2, 5, "process water", 0.40),
    ]
    for a, b, lbl, frac in exch:
        x1, y1 = centers[a]
        x2, y2 = centers[b]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        off = 42
        sx = int(x1 + dx / d * off)
        sy = int(y1 + dy / d * off)
        ex = int(x2 - dx / d * off)
        ey = int(y2 - dy / d * off)
        c.arrow(sx, sy, ex, ey, MED_GREEN, 2, 9)
        mx = int(sx + (ex - sx) * frac)
        my = int(sy + (ey - sy) * frac)
        c.text_c(mx, my - 8, lbl, RED, 1)

    # legend
    c.rect(30, 470, 300, 540, GRAY, WHITE)
    c.text(40, 480, "Green arrows: by-product and", DARK_GREEN, 1)
    c.text(40, 496, "energy exchanges between firms", DARK_GREEN, 1)
    c.text(40, 514, "Waste of one firm = input of another", BLACK, 1)

    c.text(20, H - 12, "Figure 3: Schematic of a symbiotic industrial ecosystem exchanging energy, water and by-products.",
           BLACK, 1)
    c.save(os.path.join(OUT, 'Figure_3.png'))
    print("Figure_3.png done")


# ---------------------------------------------------------------------------
def fig4():
    """Figure 4: Barriers vs enabling strategies across four transformation dimensions."""
    W, H = 820, 540
    c = PNGCanvas(W, H)
    c.text_c(W // 2, 14, "Barriers and Enabling Strategies for Industry 5.0 Transformation", BLACK, 2)

    rows = [
        ("Technological", ["Legacy integration", "Immature recovery tech"],
         ["Modular platforms", "Standards, interoperability"], MED_BLUE, LIGHT_BLUE),
        ("Financial", ["High capital cost", "Short payback horizons"],
         ["Incentives, green finance", "Product-as-a-service"], ORANGE, LIGHT_ORANGE),
        ("Organisational", ["Inertia, linear models", "Misaligned incentives"],
         ["Cross-functional teams", "New performance metrics"], PURPLE, LIGHT_PURPLE),
        ("Human", ["Skills gaps", "Change resistance"],
         ["Training, reskilling", "Human-centred change mgmt"], DARK_GREEN, LIGHT_GREEN),
    ]

    x_dim = 40
    w_dim = 150
    x_bar = x_dim + w_dim + 20
    w_bar = 270
    x_str = x_bar + w_bar + 20
    w_str = 270
    top = 66
    rh = 96
    gap = 12

    # column headers
    c.rect(x_dim, top - 34, x_dim + w_dim, top - 6, GRAY, LIGHT_GRAY)
    c.text_c(x_dim + w_dim // 2, top - 26, "Dimension", BLACK, 1)
    c.rect(x_bar, top - 34, x_bar + w_bar, top - 6, RED, LIGHT_RED)
    c.text_c(x_bar + w_bar // 2, top - 26, "Barriers", BLACK, 1)
    c.rect(x_str, top - 34, x_str + w_str, top - 6, DARK_GREEN, LIGHT_GREEN)
    c.text_c(x_str + w_str // 2, top - 26, "Enabling Strategies", BLACK, 1)

    for i, (dim, bars, strs, oc, fc) in enumerate(rows):
        y = top + i * (rh + gap)
        # dimension cell
        box(c, x_dim, y, w_dim, rh, oc, fc, [dim], 2)
        # barriers cell
        c.rect(x_bar, y, x_bar + w_bar, y + rh, RED, LIGHT_RED)
        for j, b in enumerate(bars):
            c.text(x_bar + 14, y + 24 + j * 26, "- " + b, BLACK, 1)
        # arrow
        c.arrow(x_bar + w_bar + 2, y + rh // 2, x_str - 2, y + rh // 2, BLACK, 3, 10)
        # strategies cell
        c.rect(x_str, y, x_str + w_str, y + rh, DARK_GREEN, LIGHT_GREEN)
        for j, s in enumerate(strs):
            c.text(x_str + 14, y + 24 + j * 26, "+ " + s, BLACK, 1)

    c.text(20, H - 14, "Figure 4: Structured mapping of transformation barriers to coordinated enabling responses.",
           BLACK, 1)
    c.save(os.path.join(OUT, 'Figure_4.png'))
    print("Figure_4.png done")


if __name__ == '__main__':
    fig1()
    fig2()
    fig3()
    fig4()
    print("All figures generated in", OUT)
