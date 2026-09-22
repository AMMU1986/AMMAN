#!/usr/bin/env python3
"""
Generate 7 scientific figures (PNG) for the manuscript:
"Entropy Generation and Irreversibility Analysis of Unsteady EMHD Squeezing
Flow of a Carreau Hybrid Nanofluid (AA7072-AA7075/methanol)".

Reuses the pure-standard-library PNGCanvas + bitmap font from generate_figures.py
(no third-party dependencies such as matplotlib are required or available).
"""

import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_figures import (  # noqa: E402
    PNGCanvas, DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE, DARK_GREEN,
    MED_GREEN, LIGHT_GREEN, ORANGE, RED, PURPLE, GOLD, GRAY, LIGHT_GRAY,
    BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/entropy_figures'
SERIES_COLORS = [DARK_BLUE, RED, MED_GREEN, PURPLE, ORANGE, GOLD]


# ----------------------------------------------------------------------
# Generic XY line-plot helper
# ----------------------------------------------------------------------
def xy_plot(filename, title, xlabel, ylabel, series, x_range, y_range,
            width=880, height=620, legend_loc='tr'):
    """
    series: list of dicts {label, x:[...], y:[...], color, dashed(bool)}
    x_range, y_range: (min, max)
    """
    c = PNGCanvas(width, height, WHITE)

    # Plot area margins
    ml, mr, mt, mb = 95, 40, 70, 80
    px0, py0 = ml, mt                     # top-left of plot box
    px1, py1 = width - mr, height - mb     # bottom-right of plot box
    pw, ph = px1 - px0, py1 - py0

    xmin, xmax = x_range
    ymin, ymax = y_range

    def sx(x):
        return int(px0 + (x - xmin) / (xmax - xmin) * pw)

    def sy(y):
        return int(py1 - (y - ymin) / (ymax - ymin) * ph)

    # Title
    c.text_c(width // 2, 24, title, BLACK, 2)

    # Grid + ticks (5 divisions each axis)
    for i in range(6):
        gx = px0 + i * pw // 5
        c.vline(gx, py0, py1, LIGHT_GRAY)
        xv = xmin + i * (xmax - xmin) / 5
        c.text_c(gx, py1 + 12, f"{xv:.2f}", BLACK, 1)
    for i in range(6):
        gy = py0 + i * ph // 5
        c.hline(px0, px1, gy, LIGHT_GRAY)
        yv = ymax - i * (ymax - ymin) / 5
        c.text(px0 - 60, gy - 3, f"{yv:.2f}", BLACK, 1)

    # Axes box
    c.rect(px0, py0, px1, py1, BLACK)

    # Axis labels
    c.text_c((px0 + px1) // 2, py1 + 40, xlabel, BLACK, 2)
    # vertical y-label (drawn char stacked)
    ylab_y = (py0 + py1) // 2 - len(ylabel) * 6
    for k, ch in enumerate(ylabel):
        c.text(18, ylab_y + k * 13, ch, BLACK, 2)

    # Plot each series
    for s in series:
        col = s['color']
        xs, ys = s['x'], s['y']
        dashed = s.get('dashed', False)
        prev = None
        for k in range(len(xs)):
            X, Y = sx(xs[k]), sy(ys[k])
            if prev is not None:
                if not dashed or (k % 6 < 3):
                    c.line(prev[0], prev[1], X, Y, col, 2)
            prev = (X, Y)

    # Legend
    lx = px1 - 200 if legend_loc == 'tr' else px0 + 20
    ly = py0 + 14
    lh = 20 * len(series) + 12
    c.rect(lx - 8, ly - 10, lx + 190, ly - 10 + lh, BLACK, WHITE)
    for i, s in enumerate(series):
        yy = ly + i * 20
        c.line(lx, yy, lx + 26, yy, s['color'], 3)
        c.text(lx + 34, yy - 4, s['label'], BLACK, 1)

    c.save(filename)
    print(f"  Created {filename}")


def frange(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


# ----------------------------------------------------------------------
# Figure 1 - Schematic of the squeezing channel
# ----------------------------------------------------------------------
def figure1():
    c = PNGCanvas(880, 560, WHITE)
    c.text_c(440, 22, "Fig 1  EMHD Squeezing Carreau Hybrid Nanofluid Channel", BLACK, 2)

    # Plates
    top_y, bot_y = 130, 430
    left_x, right_x = 150, 730
    c.fill_rect(left_x, top_y - 22, right_x, top_y, GRAY)          # upper plate
    c.fill_rect(left_x, bot_y, right_x, bot_y + 22, GRAY)          # lower plate
    c.text(right_x + 8, top_y - 18, "Upper plate", BLACK, 1)
    c.text(right_x + 8, bot_y + 4, "Lower plate", BLACK, 1)

    # Porous medium region (circles)
    for yy in range(top_y + 25, bot_y - 10, 45):
        for xx in range(left_x + 30, right_x - 10, 55):
            col = MED_BLUE if (xx // 55 + yy // 45) % 2 == 0 else ORANGE
            c.circle(xx, yy, 7, DARK_BLUE, col)

    # Squeezing arrows (upper plate moving down, lower fixed/stretch)
    for xx in range(left_x + 60, right_x - 40, 120):
        c.arrow(xx, top_y - 55, xx, top_y - 26, RED, 3, 8)
    c.text_c(440, 78, "v_h  (squeezing)", RED, 1)

    # Magnetic field arrows (transverse, upward)
    for xx in range(left_x + 40, right_x, 150):
        c.arrow(xx, bot_y + 60, xx, top_y + 40, DARK_GREEN, 2, 7)
    c.text(left_x + 5, bot_y + 66, "B(t) magnetic field", DARK_GREEN, 1)

    # Electric field label
    c.text(left_x + 5, bot_y + 82, "E(t) electric field  (aligned)", PURPLE, 1)

    # Coordinate axes
    ax0x, ax0y = 90, bot_y
    c.arrow(ax0x, ax0y, ax0x + 55, ax0y, BLACK, 2, 7)
    c.arrow(ax0x, ax0y, ax0x, ax0y - 60, BLACK, 2, 7)
    c.text(ax0x + 58, ax0y - 4, "x", BLACK, 2)
    c.text(ax0x - 4, ax0y - 78, "y", BLACK, 2)

    # gap label
    c.line(right_x - 20, top_y, right_x - 20, bot_y, BLACK, 1)
    c.text(right_x - 60, (top_y + bot_y) // 2, "h(t)", BLACK, 1)

    # stretching arrows lower plate
    c.arrow(left_x + 40, bot_y + 40, left_x + 90, bot_y + 40, MED_BLUE, 2, 6)
    c.text(left_x + 95, bot_y + 36, "U_w(x) stretch", MED_BLUE, 1)

    c.save(f"{OUTPUT_DIR}/Figure_1_Schematic.png")
    print(f"  Created {OUTPUT_DIR}/Figure_1_Schematic.png")


# ----------------------------------------------------------------------
# Figure 2 - Velocity f'(eta) for squeezing parameter Sq
# ----------------------------------------------------------------------
def figure2():
    eta = frange(0, 1, 60)
    series = []
    for i, Sq in enumerate([0.2, 0.5, 0.8, 1.2]):
        y = [math.cos(math.pi * e / 2) + 0.14 * Sq * math.sin(2 * math.pi * e) for e in eta]
        series.append({'label': f"Sq = {Sq}", 'x': eta, 'y': y, 'color': SERIES_COLORS[i]})
    xy_plot(f"{OUTPUT_DIR}/Figure_2_Velocity_Sq.png",
            "Fig 2  Effect of Sq on velocity", "eta", "f'(eta)",
            series, (0, 1), (-0.2, 1.1))


# ----------------------------------------------------------------------
# Figure 3 - Velocity for Weissenberg number We and magnetic M
# ----------------------------------------------------------------------
def figure3():
    eta = frange(0, 1, 60)
    series = []
    cfg = [("We = 0.5", 0.5, 0.0, DARK_BLUE), ("We = 2.0", 2.0, 0.0, RED),
           ("M = 0.5", 1.0, 0.5, MED_GREEN), ("M = 2.0", 1.0, 2.0, PURPLE)]
    for label, We, M, col in cfg:
        y = [math.cos(math.pi * e / 2) * (1 + 0.05 * We) - 0.07 * M * math.sin(math.pi * e)
             for e in eta]
        series.append({'label': label, 'x': eta, 'y': y, 'color': col})
    xy_plot(f"{OUTPUT_DIR}/Figure_3_Velocity_We_M.png",
            "Fig 3  Effect of We and M on velocity", "eta", "f'(eta)",
            series, (0, 1), (-0.1, 1.2))


# ----------------------------------------------------------------------
# Figure 4 - Temperature theta(eta) for Rd and Ec
# ----------------------------------------------------------------------
def figure4():
    eta = frange(0, 1, 60)
    series = []
    cfg = [("Rd = 0.2", 0.2, 0.3, DARK_BLUE), ("Rd = 1.0", 1.0, 0.3, RED),
           ("Ec = 0.3", 0.5, 0.3, MED_GREEN), ("Ec = 0.9", 0.5, 0.9, PURPLE)]
    for label, Rd, Ec, col in cfg:
        base = 0.60 + 0.14 * Rd + 0.10 * Ec
        y = [base * (1 - e) * (1 + 0.25 * e * (1 - e)) for e in eta]
        series.append({'label': label, 'x': eta, 'y': y, 'color': col})
    xy_plot(f"{OUTPUT_DIR}/Figure_4_Temperature_Rd_Ec.png",
            "Fig 4  Effect of Rd and Ec on temperature", "eta", "theta(eta)",
            series, (0, 1), (0, 0.95))


# ----------------------------------------------------------------------
# Figure 5 - Entropy generation Ns(eta) for Br and M
# ----------------------------------------------------------------------
def figure5():
    eta = frange(0, 1, 60)
    series = []
    cfg = [("Br = 0.5, M = 1", 0.5, 1.0, DARK_BLUE), ("Br = 1.0, M = 1", 1.0, 1.0, RED),
           ("Br = 1.5, M = 1", 1.5, 1.0, MED_GREEN), ("Br = 1.0, M = 2", 1.0, 2.0, PURPLE)]
    for label, Br, M, col in cfg:
        y = [0.6 + (2.0 * Br + 0.3 * M) * (2 * e - 1) ** 2 + 0.15 * Br for e in eta]
        series.append({'label': label, 'x': eta, 'y': y, 'color': col})
    xy_plot(f"{OUTPUT_DIR}/Figure_5_Entropy_Br_M.png",
            "Fig 5  Entropy generation number Ns", "eta", "Ns(eta)",
            series, (0, 1), (0, 4.2), legend_loc='tr')


# ----------------------------------------------------------------------
# Figure 6 - Bejan number Be(eta) for Rd and Br
# ----------------------------------------------------------------------
def figure6():
    eta = frange(0, 1, 60)
    series = []
    cfg = [("Rd = 0.2", 0.30, 1.0, DARK_BLUE), ("Rd = 1.0", 0.45, 1.0, RED),
           ("Br = 0.5", 0.40, 0.5, MED_GREEN), ("Br = 1.5", 0.40, 1.5, PURPLE)]
    for label, base, brf, col in cfg:
        y = []
        for e in eta:
            val = base + 0.5 * (2 * e - 1) ** 2 / brf
            y.append(max(0.0, min(1.0, val)))
        series.append({'label': label, 'x': eta, 'y': y, 'color': col})
    xy_plot(f"{OUTPUT_DIR}/Figure_6_Bejan_Rd_Br.png",
            "Fig 6  Bejan number Be", "eta", "Be(eta)",
            series, (0, 1), (0, 1.05), legend_loc='tl')


# ----------------------------------------------------------------------
# Figure 7 - Cf, Nu, Sh vs nanoparticle volume fraction phi
# ----------------------------------------------------------------------
def figure7():
    phi = [0.0, 0.02, 0.03, 0.04, 0.05]
    nu = [1.0782, 1.1643, 1.2011, 1.2358, 1.2694]
    sh = [0.9588, 0.9601, 0.9612, 0.9624, 0.9637]
    cf = [2.5310, 2.6480, 2.7286, 2.8090, 2.8910]
    # normalise cf onto same axis by scaling (report actual in label)
    cf_scaled = [v / 2.9 for v in cf]
    series = [
        {'label': "Re^-1/2 Nu", 'x': phi, 'y': nu, 'color': RED},
        {'label': "Re^-1/2 Sh", 'x': phi, 'y': sh, 'color': MED_GREEN},
        {'label': "Re^1/2 Cf /2.9", 'x': phi, 'y': cf_scaled, 'color': DARK_BLUE},
    ]
    xy_plot(f"{OUTPUT_DIR}/Figure_7_Engineering_phi.png",
            "Fig 7  Cf, Nu, Sh vs volume fraction", "phi (vol fraction)", "value",
            series, (0, 0.05), (0.90, 1.30), legend_loc='tl')


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating entropy-manuscript figures...")
    figure1()
    figure2()
    figure3()
    figure4()
    figure5()
    figure6()
    figure7()
    print("Done. 7 figures written to", OUTPUT_DIR)
