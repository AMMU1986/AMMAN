#!/usr/bin/env python3
"""
Generate the 4 figures for Chapter 3: Smart Hybrid Renewable Energy Systems.

Reuses the pure-standard-library PNGCanvas and 5x7 font from generate_figures.py
(matplotlib/PIL are unavailable in this sandbox). Produces:

  chapter3_figures/Figure_1_Smart_HRES_Architecture.png
  chapter3_figures/Figure_2_LCOE_Comparison.png
  chapter3_figures/Figure_3_Digitalization_Stack.png
  chapter3_figures/Figure_4_Resilience_Framework.png
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/chapter3_figures'


def box(c, x, y, w, h, outline, fill, lines, scale=1, text_color=BLACK):
    """Draw a filled, outlined box with centered multi-line text."""
    c.rect(x, y, x + w, y + h, outline, fill)
    n = len(lines)
    line_h = 11 * scale
    start_y = y + h // 2 - (n * line_h) // 2 + 1
    for i, ln in enumerate(lines):
        c.text_c(x + w // 2, start_y + i * line_h, ln, text_color, scale)


# ---------------------------------------------------------------------------
# Figure 1: Layered architecture of a smart HRES
# ---------------------------------------------------------------------------
def fig1():
    c = PNGCanvas(900, 560)
    c.text_c(450, 14, "Smart Hybrid Renewable Energy System Architecture", BLACK, 2)

    # Generation / storage sources (top row)
    sources = [
        ("Solar PV", GOLD, LIGHT_GOLD),
        ("Wind", MED_BLUE, LIGHT_BLUE),
        ("Hydropower", DARK_BLUE, PALE_BLUE),
        ("Storage", DARK_GREEN, LIGHT_GREEN),
    ]
    sw, sh = 150, 55
    gap = 40
    total = len(sources) * sw + (len(sources) - 1) * gap
    x0 = (900 - total) // 2
    src_centers = []
    for i, (label, oc, fc) in enumerate(sources):
        bx = x0 + i * (sw + gap)
        box(c, bx, 55, sw, sh, oc, fc, [label])
        src_centers.append((bx + sw // 2, 55 + sh))

    # Power-electronic converter layer
    conv_y = 160
    c.rect(x0, conv_y, x0 + total, conv_y + 36, GRAY, LIGHT_GRAY)
    c.text_c(450, conv_y + 13, "Power-Electronic Converters (DC/DC, DC/AC)", BLACK, 1)
    for cx, cy in src_centers:
        c.arrow(cx, cy, cx, conv_y, GRAY, 2, 7)

    # Common AC/DC bus
    bus_y = 235
    c.fill_rect(x0 - 10, bus_y, x0 + total + 10, bus_y + 14, DARK_BLUE)
    c.text_c(450, bus_y + 3, "Common AC / DC Bus", WHITE, 1)
    c.arrow(450, conv_y + 36, 450, bus_y, GRAY, 2, 7)

    # EMS core
    ems_y = 300
    box(c, 330, ems_y, 240, 58, PURPLE, LIGHT_PURPLE,
        ["Intelligent Energy", "Management System (EMS)"])
    c.arrow(450, bus_y + 14, 450, ems_y, GRAY, 2, 7)

    # Bottom row: smart grid, markets, loads
    bottoms = [
        ("Smart Grid", MED_BLUE, LIGHT_BLUE, 120),
        ("Energy Markets", ORANGE, LIGHT_ORANGE, 420),
        ("Local Loads", DARK_GREEN, LIGHT_GREEN, 700),
    ]
    bw, bh = 170, 52
    for label, oc, fc, bx in bottoms:
        box(c, bx, 440, bw, bh, oc, fc, [label])
        # bidirectional arrows to EMS
        c.arrow(450, ems_y + 58, bx + bw // 2, 440, GRAY, 2, 7)

    # Cyber layer annotation
    c.rect(20, 300, 300, 360, DARK_GREEN, (240, 248, 240))
    c.text(30, 308, "Cyber layer:", BLACK, 1)
    c.text(30, 322, "- Sensing / metering", GRAY, 1)
    c.text(30, 336, "- Communication", GRAY, 1)
    c.text(30, 350, "- Optimization/control", GRAY, 1)

    c.rect(600, 300, 880, 360, ORANGE, (252, 245, 235))
    c.text(610, 308, "Objectives:", BLACK, 1)
    c.text(610, 322, "- Min cost / max RE use", GRAY, 1)
    c.text(610, 336, "- Reliability / stability", GRAY, 1)
    c.text(610, 350, "- Market revenue", GRAY, 1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Smart_HRES_Architecture.png'))


# ---------------------------------------------------------------------------
# Figure 2: LCOE comparison across HRES configurations
# ---------------------------------------------------------------------------
def fig2():
    c = PNGCanvas(900, 540)
    c.text_c(450, 14, "LCOE Comparison Across HRES Configurations (USD/MWh)", BLACK, 2)

    # Plot area
    px0, py0 = 90, 70       # top-left of plot
    px1, py1 = 850, 440     # bottom-right (y axis baseline at py1)
    c.vline(px0, py0, py1, BLACK)
    c.hline(px0, px1, py1, BLACK)

    ymax = 120
    # y gridlines and labels
    for val in range(0, ymax + 1, 20):
        yy = py1 - int((val / ymax) * (py1 - py0))
        c.hline(px0, px1, yy, LIGHT_GRAY)
        c.vline(px0, py0, py1, BLACK)
        c.text(px0 - 40, yy - 3, str(val), BLACK, 1)
    c.text(px0, py0 - 14, "USD/MWh", GRAY, 1)

    # (label, low, optimal_high) : solid bar = optimal (low..opt), light = range to max
    configs = [
        ("PV/Wind", 30, 55, MED_BLUE, LIGHT_BLUE),
        ("PV/Wind/Battery", 55, 85, PURPLE, LIGHT_PURPLE),
        ("PV/Wind/Hydro", 38, 60, DARK_GREEN, LIGHT_GREEN),
        ("PV/Wind/Hydrogen", 70, 110, ORANGE, LIGHT_ORANGE),
    ]
    n = len(configs)
    slot = (px1 - px0) // n
    bw = 70

    def ytop(val):
        return py1 - int((val / ymax) * (py1 - py0))

    for i, (label, low, high, oc, fc) in enumerate(configs):
        cx = px0 + slot * i + slot // 2
        bx1 = cx - bw // 2
        bx2 = cx + bw // 2
        # light bar = full range up to high
        c.fill_rect(bx1, ytop(high), bx2, py1 - 1, fc)
        # solid bar = optimal (floor) value
        c.fill_rect(bx1, ytop(low), bx2, py1 - 1, oc)
        c.rect(bx1, ytop(high), bx2, py1 - 1, BLACK)
        # value labels
        c.text_c(cx, ytop(high) - 14, str(low) + "-" + str(high), BLACK, 1)
        # x label (wrap long names)
        parts = label.split("/")
        for k, p in enumerate(parts):
            c.text_c(cx, py1 + 8 + k * 11, p, BLACK, 1)

    # Legend (placed in empty upper-left region)
    lx, ly = 130, 95
    c.fill_rect(lx, ly, lx + 18, ly + 12, MED_BLUE)
    c.text(lx + 24, ly + 2, "Optimal (floor) LCOE", BLACK, 1)
    c.fill_rect(lx, ly + 20, lx + 18, ly + 32, LIGHT_BLUE)
    c.text(lx + 24, ly + 22, "Upper range (resource/sizing)", BLACK, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_LCOE_Comparison.png'))


# ---------------------------------------------------------------------------
# Figure 3: Digitalization and intelligent-management stack
# ---------------------------------------------------------------------------
def fig3():
    c = PNGCanvas(900, 560)
    c.text_c(450, 14, "Digitalization and Intelligent Management Stack", BLACK, 2)

    layers = [
        ("Cloud Layer: Digital Twin + AI/ML Analytics (forecasting, optimization)",
         DARK_BLUE, PALE_BLUE),
        ("Edge Layer: Real-Time Control, Protection, Local Decision-Making",
         DARK_GREEN, LIGHT_GREEN),
        ("Communication Layer: Secure Bidirectional Data Exchange",
         GRAY, LIGHT_GRAY),
        ("Field Layer: IoT Sensors, Smart Meters, Converters, Storage, Loads",
         ORANGE, LIGHT_ORANGE),
    ]
    lw = 700
    lh = 70
    lx = (900 - lw) // 2
    y = 60
    gap = 30
    centers = []
    for label, oc, fc in layers:
        box(c, lx, y, lw, lh, oc, fc, [label])
        centers.append((lx, y, lw, lh))
        y += lh + gap

    # Upward data-flow arrows (field -> cloud) on left
    for i in range(len(layers) - 1, 0, -1):
        x = lx + 60
        y_from = centers[i][1]
        y_to = centers[i - 1][1] + lh
        c.arrow(x, y_from, x, y_to, DARK_GREEN, 2, 7)
    c.text(lx + 70, 240, "Data up", DARK_GREEN, 1)

    # Downward control arrows (cloud -> field) on right
    for i in range(len(layers) - 1):
        x = lx + lw - 60
        y_from = centers[i][1] + lh
        y_to = centers[i + 1][1]
        c.arrow(x, y_from, x, y_to, RED, 2, 7)
    c.text(lx + lw - 150, 240, "Control down", RED, 1)

    # Cross-cutting cybersecurity bar
    c.fill_rect(lx, y + 4, lx + lw, y + 34, PURPLE)
    c.text_c(lx + lw // 2, y + 11, "Cross-Cutting: Cybersecurity and Predictive Maintenance",
             WHITE, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Digitalization_Stack.png'))


# ---------------------------------------------------------------------------
# Figure 4: Integrated resilience & sustainability framework (4 pillars)
# ---------------------------------------------------------------------------
def fig4():
    c = PNGCanvas(900, 560)
    c.text_c(450, 14, "Integrated Resilience and Sustainability Framework", BLACK, 2)

    # Central hub
    hub_cx, hub_cy = 450, 285
    c.circle(hub_cx, hub_cy, 78, DARK_BLUE, fill=PALE_BLUE)
    c.text_c(hub_cx, hub_cy - 14, "Adaptive", BLACK, 1)
    c.text_c(hub_cx, hub_cy - 2, "Energy", BLACK, 1)
    c.text_c(hub_cx, hub_cy + 10, "Management", BLACK, 1)

    pillars = [
        ("Technical", "Performance", 180, 110, MED_BLUE, LIGHT_BLUE),
        ("Economic", "Feasibility", 720, 110, DARK_GREEN, LIGHT_GREEN),
        ("Market", "Participation", 180, 460, ORANGE, LIGHT_ORANGE),
        ("Digital", "Intelligence", 720, 460, PURPLE, LIGHT_PURPLE),
    ]
    pw, ph = 180, 70
    for t1, t2, cx, cy, oc, fc in pillars:
        box(c, cx - pw // 2, cy - ph // 2, pw, ph, oc, fc, [t1, t2])
        # connect to hub
        dx, dy = hub_cx - cx, hub_cy - cy
        d = math.sqrt(dx * dx + dy * dy)
        c.arrow(int(cx + dx / d * 40), int(cy + dy / d * 28),
                int(hub_cx - dx / d * 82), int(hub_cy - dy / d * 82), GRAY, 2, 8)

    # Outcome banner
    c.fill_rect(300, 520, 600, 548, DARK_GREEN)
    c.text_c(450, 527, "Resilient and Sustainable Operation", WHITE, 1)
    c.arrow(hub_cx, hub_cy + 78, 450, 520, DARK_GREEN, 2, 8)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Resilience_Framework.png'))


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Chapter 3 figures...")
    fig1()
    fig2()
    fig3()
    fig4()
    print(f"\nFigures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz/1024:.1f} KB")


if __name__ == '__main__':
    main()
