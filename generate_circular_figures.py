#!/usr/bin/env python3
"""
Generate 4 scientific figures (PNG) for the chapter
'Circular Economy and Recyclable 3D Printed Materials'.

Reuses the pure-Python PNGCanvas class from generate_figures.py so that no
third-party libraries (matplotlib/PIL) are required.
"""

import os
import math

# Reuse the existing pure-Python PNG toolkit from the repo.
from generate_figures import (
    PNGCanvas,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE, RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/circular_figures'


def gen_fig1():
    """Figure 1: Property degradation vs recycling cycles (line chart)."""
    c = PNGCanvas(760, 480)
    c.text_c(380, 12, "Property Retention Across Recycling Cycles", BLACK, 2)

    # Plot area
    x0, y0 = 90, 400   # origin (bottom-left)
    x1, y1 = 700, 70   # top-right
    c.vline(x0, y1, y0, BLACK)
    c.hline(x0, x1, y0, BLACK)

    # Y axis gridlines and labels (0-100 %)
    for pct in range(0, 101, 20):
        gy = y0 - int((pct / 100.0) * (y0 - y1))
        c.hline(x0, x1, gy, LIGHT_GRAY)
        c.line(x0 - 5, gy, x0, gy, BLACK, 1)
        c.text(x0 - 55, gy - 4, f"{pct}%", BLACK, 1)
    # re-draw axis over gridlines
    c.vline(x0, y1, y0, BLACK)
    c.hline(x0, x1, y0, BLACK)

    # X axis labels (0..5 cycles)
    n_cyc = 5
    for i in range(n_cyc + 1):
        gx = x0 + int((i / n_cyc) * (x1 - x0))
        c.line(gx, y0, gx, y0 + 5, BLACK, 1)
        c.text_c(gx, y0 + 12, str(i), BLACK, 1)
    c.text_c((x0 + x1) // 2, y0 + 34, "Number of Recycling Cycles", BLACK, 1)

    # Axis title (y) - drawn horizontally near top
    c.text(30, y1 - 24, "Property Retention (percent of virgin)", BLACK, 1)

    def to_xy(cycle, pct):
        gx = x0 + int((cycle / n_cyc) * (x1 - x0))
        gy = y0 - int((pct / 100.0) * (y0 - y1))
        return gx, gy

    # Data series: tensile strength and elongation at break (relative %)
    tensile = [100, 96, 90, 82, 73, 63]
    elong = [100, 88, 74, 58, 44, 32]

    def plot_series(data, color, marker_fill):
        pts = [to_xy(i, v) for i, v in enumerate(data)]
        for k in range(len(pts) - 1):
            c.line(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], color, 3)
        for (px, py) in pts:
            c.circle(px, py, 5, color, fill=marker_fill)

    plot_series(tensile, DARK_BLUE, LIGHT_BLUE)
    plot_series(elong, RED, LIGHT_RED)

    # Legend
    lx, ly = 470, 100
    c.rect(lx, ly, lx + 240, ly + 62, GRAY, WHITE)
    c.line(lx + 12, ly + 18, lx + 42, ly + 18, DARK_BLUE, 3)
    c.circle(lx + 27, ly + 18, 5, DARK_BLUE, fill=LIGHT_BLUE)
    c.text(lx + 50, ly + 13, "Tensile Strength", BLACK, 1)
    c.line(lx + 12, ly + 42, lx + 42, ly + 42, RED, 3)
    c.circle(lx + 27, ly + 42, 5, RED, fill=LIGHT_RED)
    c.text(lx + 50, ly + 37, "Elongation at Break", BLACK, 1)

    c.text(90, 455, "Figure 1: Property retention of a representative thermoplastic over recycling cycles", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Recycling_Degradation.png'))
    print("  Figure_1_Recycling_Degradation.png done")


def gen_fig2():
    """Figure 2: Closed-loop material processing workflow diagram."""
    c = PNGCanvas(780, 500)
    c.text_c(390, 12, "Closed-Loop Material Processing Workflow", BLACK, 2)

    cx, cy = 390, 270
    r = 165
    bw, bh = 150, 56

    stages = [
        ("Collection", DARK_BLUE, PALE_BLUE),
        ("Sorting", MED_BLUE, LIGHT_BLUE),
        ("Shredding", ORANGE, LIGHT_ORANGE),
        ("Reprocessing", DARK_GREEN, LIGHT_GREEN),
        ("3D Printing", PURPLE, LIGHT_PURPLE),
        ("Use / End-of-Life", RED, LIGHT_RED),
    ]
    n = len(stages)
    centers = []
    for i, (label, col, fill) in enumerate(stages):
        ang = -math.pi / 2 + i * (2 * math.pi / n)
        bx = int(cx + r * math.cos(ang) - bw / 2)
        by = int(cy + r * math.sin(ang) - bh / 2)
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        c.text_c(bx + bw // 2, by + bh // 2 - 4, label, BLACK, 1)
        centers.append((bx + bw // 2, by + bh // 2))

    # Clockwise arrows between consecutive stages
    for i in range(n):
        x1, y1 = centers[i]
        x2, y2 = centers[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        d = math.sqrt(dx * dx + dy * dy)
        off = 92
        ax1 = int(x1 + dx / d * off)
        ay1 = int(y1 + dy / d * off)
        ax2 = int(x2 - dx / d * off)
        ay2 = int(y2 - dy / d * off)
        c.arrow(ax1, ay1, ax2, ay2, GRAY, 2, 9)

    # Center: quality control hub
    c.circle(cx, cy, 62, GOLD, fill=LIGHT_GOLD)
    c.text_c(cx, cy - 12, "Quality", BLACK, 1)
    c.text_c(cx, cy, "Control", BLACK, 1)
    c.text_c(cx, cy + 12, "and Traceability", BLACK, 1)

    # Spokes from hub to each stage (dashed-look via short segments)
    for (px, py) in centers:
        dx, dy = px - cx, py - cy
        d = math.sqrt(dx * dx + dy * dy)
        sx = int(cx + dx / d * 64)
        sy = int(cy + dy / d * 64)
        ex = int(px - dx / d * 30)
        ey = int(py - dy / d * 30)
        c.line(sx, sy, ex, ey, LIGHT_GRAY, 1)

    c.text(80, 478, "Figure 2: Continuous closed-loop workflow with a central quality-control gate", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Closed_Loop_Workflow.png'))
    print("  Figure_2_Closed_Loop_Workflow.png done")


def gen_fig3():
    """Figure 3: Embodied carbon of virgin vs recycled feedstock (grouped bars)."""
    c = PNGCanvas(760, 480)
    c.text_c(380, 12, "Comparative Embodied Carbon of Feedstocks", BLACK, 2)

    x0, y0 = 90, 400
    x1, y1 = 710, 70
    c.vline(x0, y1, y0, BLACK)
    c.hline(x0, x1, y0, BLACK)

    max_val = 6.0  # kg CO2e per kg (illustrative)
    for v in range(0, 7):
        gy = y0 - int((v / max_val) * (y0 - y1))
        c.hline(x0, x1, gy, LIGHT_GRAY)
        c.line(x0 - 5, gy, x0, gy, BLACK, 1)
        c.text(x0 - 40, gy - 4, f"{v}", BLACK, 1)
    c.vline(x0, y1, y0, BLACK)
    c.hline(x0, x1, y0, BLACK)
    c.text(24, y1 - 24, "Embodied Carbon (kg CO2e / kg)", BLACK, 1)

    # groups: material, [virgin, mechanical-recycled, chemical-recycled]
    groups = [
        ("PLA", [3.2, 1.6, 2.4]),
        ("ABS", [3.8, 1.9, 2.9]),
        ("PETG", [3.5, 1.7, 2.7]),
        ("rPET", [4.1, 1.5, 2.5]),
    ]
    series_colors = [MED_BLUE, MED_GREEN, ORANGE]
    series_names = ["Virgin", "Mechanical Recycled", "Chemical Recycled"]

    group_w = (x1 - x0 - 40) // len(groups)
    bar_w = group_w // 4
    for gi, (name, vals) in enumerate(groups):
        gx = x0 + 30 + gi * group_w
        for si, val in enumerate(vals):
            bx = gx + si * (bar_w + 4)
            bh = int((val / max_val) * (y0 - y1))
            c.rect(bx, y0 - bh, bx + bar_w, y0, BLACK, series_colors[si])
            c.text_c(bx + bar_w // 2, y0 - bh - 12, f"{val:.1f}", BLACK, 1)
        c.text_c(gx + (3 * (bar_w + 4)) // 2, y0 + 12, name, BLACK, 1)

    # Legend
    lx, ly = 470, 90
    c.rect(lx, ly, lx + 250, ly + 78, GRAY, WHITE)
    for si, sname in enumerate(series_names):
        yy = ly + 12 + si * 22
        c.rect(lx + 12, yy, lx + 32, yy + 14, BLACK, series_colors[si])
        c.text(lx + 40, yy + 2, sname, BLACK, 1)

    c.text(80, 455, "Figure 3: Illustrative embodied carbon for virgin and recycled feedstocks", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Embodied_Carbon.png'))
    print("  Figure_3_Embodied_Carbon.png done")


def gen_fig4():
    """Figure 4: Layered digital ecosystem for circular AM."""
    c = PNGCanvas(780, 500)
    c.text_c(390, 12, "Digital Ecosystem for Circular Additive Manufacturing", BLACK, 2)

    layers = [
        ("Artificial Intelligence: optimization and prediction", PURPLE, LIGHT_PURPLE),
        ("Digital Twins: simulation and monitoring", DARK_BLUE, LIGHT_BLUE),
        ("Material Passports: composition and provenance", DARK_GREEN, LIGHT_GREEN),
        ("Sensing and Process Data: real-time capture", ORANGE, LIGHT_ORANGE),
    ]
    lx, lw = 120, 540
    top = 70
    lh = 62
    gap = 18
    centers_y = []
    for i, (label, col, fill) in enumerate(layers):
        ly = top + i * (lh + gap)
        c.rect(lx, ly, lx + lw, ly + lh, col, fill)
        c.text_c(lx + lw // 2, ly + lh // 2 - 4, label, BLACK, 1)
        centers_y.append(ly + lh // 2)

    # Upward data-flow arrows on the left, feedback arrows on the right
    for i in range(len(layers) - 1):
        # data flows up (from lower layer to upper layer)
        y_low = top + (i + 1) * (lh + gap)
        y_high = top + i * (lh + gap) + lh
        c.arrow(lx + 60, y_low, lx + 60, y_high, DARK_GREEN, 2, 8)
        # control/feedback flows down
        c.arrow(lx + lw - 60, y_high, lx + lw - 60, y_low, RED, 2, 8)

    # side labels
    c.text(lx + 5, top - 20, "Data flow (up)", DARK_GREEN, 1)
    c.text(lx + lw - 150, top - 20, "Control / feedback (down)", RED, 1)

    # Life-cycle band at bottom
    band_y = top + len(layers) * (lh + gap) + 6
    stages = ["Design", "Production", "Use", "Recovery"]
    seg_w = lw // len(stages)
    for i, s in enumerate(stages):
        bx = lx + i * seg_w
        c.rect(bx, band_y, bx + seg_w, band_y + 34, GRAY, PALE_BLUE)
        c.text_c(bx + seg_w // 2, band_y + 12, s, BLACK, 1)
    # loop arrow from Recovery back to Design
    c.arrow(lx + lw - 6, band_y + 17, lx + lw + 30, band_y + 17, PURPLE, 2, 8)
    c.line(lx + lw + 30, band_y + 17, lx + lw + 30, band_y - 10, PURPLE, 2)
    c.line(lx - 30, band_y - 10, lx + lw + 30, band_y - 10, PURPLE, 2)
    c.arrow(lx - 30, band_y - 10, lx - 30, band_y + 17, PURPLE, 2, 8)
    c.line(lx - 30, band_y + 17, lx, band_y + 17, PURPLE, 2)

    c.text(80, 480, "Figure 4: Integrated, layered digital ecosystem enabling circular material loops", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Digital_Ecosystem.png'))
    print("  Figure_4_Digital_Ecosystem.png done")


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating circular-economy figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print("All figures generated in", OUTPUT_DIR)
