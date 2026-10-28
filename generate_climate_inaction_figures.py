#!/usr/bin/env python3
"""
Generate 4 conceptual figure images (PNG) for the chapter
"Economic Consequences of Climate Inaction".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - Causal framework linking climate inaction to macroeconomic,
             health, and distributional consequences
  Figure 2 - Projected trajectories of cumulative economic loss under
             climate inaction versus early climate action
  Figure 3 - Transmission pathway from climatic exposure to health impacts
             and healthcare expenditure
  Figure 4 - An integrated framework for climate-ready economies
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/climate_inaction_figures'


def gen_fig1():
    """Figure 1: Causal framework linking inaction to compounding consequences."""
    c = PNGCanvas(940, 560)
    c.text_c(470, 10, "Causal Framework: From Climate Inaction to Economic Loss", BLACK, 2)

    # Top node: Climate Inaction
    c.rect(330, 44, 530, 92, DARK_BLUE, PALE_BLUE)
    c.text_c(430, 54, "CLIMATE INACTION", BLACK, 1)
    c.text_c(430, 72, "delayed mitigation & adaptation", GRAY, 1)

    # Three pathway columns
    cols = [
        (160, "MACROECONOMIC", MED_BLUE, LIGHT_BLUE,
         ["Lower GDP growth", "Infrastructure &", "supply-chain damage",
          "Agricultural &", "industrial losses"]),
        (430, "PUBLIC HEALTH", RED, LIGHT_RED,
         ["Heat & disease burden", "Rising treatment cost",
          "Productivity loss", "Strained health", "systems"]),
        (700, "SOCIAL INEQUITY", PURPLE, LIGHT_PURPLE,
         ["Burden on the poor", "Informal / outdoor", "workers exposed",
          "Displacement &", "lost livelihoods"]),
    ]

    # arrows from top node to each column header
    for cx, title, col, fill, items in cols:
        c.rect(cx - 105, 130, cx + 105, 168, col, fill)
        c.text_c(cx, 142, title, BLACK, 1)
        c.arrow(430, 94, cx, 128, GRAY, 2, 9)
        # item boxes
        y = 188
        for it in items:
            c.text_c(cx, y, it, BLACK, 1)
            y += 22
        # arrow down to the convergence bar
        c.arrow(cx, y + 2, cx, 352, GRAY, 2, 9)

    # Convergence: compounding economic loss
    c.rect(55, 360, 805, 408, ORANGE, LIGHT_ORANGE)
    c.text_c(430, 370, "COMPOUNDING, NONLINEAR ECONOMIC LOSS", BLACK, 1)
    c.text_c(430, 388, "transferred to the future and to the most vulnerable", GRAY, 1)

    # Feedback loop (far right, clear of columns): loss erodes adaptive capacity
    c.line(805, 384, 880, 384, MED_GREEN, 2)
    c.line(880, 384, 880, 68, MED_GREEN, 2)
    c.arrow(880, 68, 530, 68, MED_GREEN, 2, 9)
    c.text(846, 206, "erodes", MED_GREEN, 1)
    c.text(846, 222, "fiscal &", MED_GREEN, 1)
    c.text(846, 238, "adaptive", MED_GREEN, 1)
    c.text(846, 254, "capacity", MED_GREEN, 1)

    # Interpretive note
    c.rect(60, 448, 880, 500, GRAY, (250, 250, 250))
    c.text_c(470, 460, "Short-term savings from delay are offset by larger, compounding future costs", BLACK, 1)
    c.text_c(470, 478, "across macroeconomic, health, and distributional channels acting together", GRAY, 1)

    c.text(60, 536, "Figure 1: Inaction propagates through three interacting channels to magnified, inequitable economic loss", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Causal_Framework.png'))
    print("  Figure_1_Causal_Framework.png done")


def gen_fig2():
    """Figure 2: Cumulative economic loss trajectories, inaction vs action."""
    c = PNGCanvas(820, 520)
    c.text_c(410, 10, "Cumulative Economic Loss: Inaction versus Early Action", BLACK, 2)

    # Axes
    ox, oy = 110, 430          # origin
    ax_w, ax_h = 620, 360
    c.line(ox, oy, ox + ax_w, oy, BLACK, 2)          # x-axis
    c.line(ox, oy, ox, oy - ax_h, BLACK, 2)          # y-axis
    c.text_c(ox + ax_w // 2, 470, "Time (decades ahead)", BLACK, 1)
    # y label (vertical-ish, stacked)
    c.text(20, 150, "Cumulative", BLACK, 1)
    c.text(20, 166, "economic", BLACK, 1)
    c.text(20, 182, "loss", BLACK, 1)

    # x gridlines
    for i in range(0, 6):
        gx = ox + int(i / 5 * ax_w)
        c.vline(gx, oy - ax_h, oy, LIGHT_GRAY)
        c.text_c(gx, oy + 8, str(2030 + i * 15), GRAY, 1)

    # y gridlines
    for j in range(0, 6):
        gy = oy - int(j / 5 * ax_h)
        c.hline(ox, ox + ax_w, gy, LIGHT_GRAY)
        c.text(ox - 40, gy - 4, f"{j*4}%", GRAY, 1)

    def curve_points(fn):
        pts = []
        n = 60
        for k in range(n + 1):
            t = k / n
            gx = ox + int(t * ax_w)
            v = fn(t)                       # fraction 0..1 of ax_h
            gy = oy - int(v * ax_h)
            pts.append((gx, gy))
        return pts

    # Inaction: accelerating, convex (nonlinear) loss -> ~ 20% (full scale)
    inaction = curve_points(lambda t: 0.98 * (t ** 1.9))
    # Action: early cost then flattening -> ~ 6%
    action = curve_points(lambda t: 0.30 * (1 - math.exp(-2.4 * t)))

    # Shade the avoidable-loss gap between the two curves
    for (xa, ya), (xb, yb) in zip(action, inaction):
        c.vline(xa, yb, ya, (252, 236, 224))

    # Draw curves
    for pts, col in [(inaction, RED), (action, DARK_GREEN)]:
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            c.line(x1, y1, x2, y2, col, 3)

    # End labels
    ex, ey = inaction[-1]
    c.text(ex - 150, ey - 6, "Inaction", RED, 1)
    ex2, ey2 = action[-1]
    c.text(ex2 - 60, ey2 - 20, "Early action", DARK_GREEN, 1)

    # Gap annotation
    mid = len(inaction) * 3 // 4
    gx = inaction[mid][0]
    c.line(gx, inaction[mid][1], gx, action[mid][1], GRAY, 1)
    c.text(gx + 6, (inaction[mid][1] + action[mid][1]) // 2 - 8, "avoidable", ORANGE, 1)
    c.text(gx + 6, (inaction[mid][1] + action[mid][1]) // 2 + 8, "loss", ORANGE, 1)

    # Legend
    c.rect(ox + 20, oy - ax_h + 6, ox + 250, oy - ax_h + 54, GRAY, WHITE)
    c.line(ox + 32, oy - ax_h + 20, ox + 60, oy - ax_h + 20, RED, 3)
    c.text(ox + 66, oy - ax_h + 15, "Climate inaction", BLACK, 1)
    c.line(ox + 32, oy - ax_h + 40, ox + 60, oy - ax_h + 40, DARK_GREEN, 3)
    c.text(ox + 66, oy - ax_h + 35, "Early climate action", BLACK, 1)

    c.text(40, 500, "Figure 2: Nonlinear damages widen the gap between inaction and action over time (illustrative)", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Loss_Trajectories.png'))
    print("  Figure_2_Loss_Trajectories.png done")


def gen_fig3():
    """Figure 3: Transmission from climatic exposure to healthcare expenditure."""
    c = PNGCanvas(900, 500)
    c.text_c(450, 10, "Transmission: Climatic Exposure to Health & Economic Cost", BLACK, 2)

    # Four-stage horizontal chain
    stages = [
        ("CLIMATIC", "EXPOSURE", "Heat, extreme events,", "altered disease range", DARK_BLUE, PALE_BLUE),
        ("PHYSIOLOGICAL", "& CLINICAL IMPACT", "Illness, injury,", "reduced work capacity", ORANGE, LIGHT_ORANGE),
        ("DEMAND ON", "HEALTH SERVICES", "Admissions, emergency", "care, medication", RED, LIGHT_RED),
        ("ECONOMIC", "EXPENDITURE", "Treatment cost,", "lost productivity", PURPLE, LIGHT_PURPLE),
    ]
    bw, bh = 180, 90
    gap = 50
    x0 = 40
    y0 = 90
    centers = []
    for i, (t1, t2, s1, s2, col, fill) in enumerate(stages):
        x1 = x0 + i * (bw + gap)
        c.rect(x1, y0, x1 + bw, y0 + bh, col, fill)
        c.text_c(x1 + bw // 2, y0 + 14, t1, BLACK, 1)
        c.text_c(x1 + bw // 2, y0 + 30, t2, BLACK, 1)
        c.text_c(x1 + bw // 2, y0 + 54, s1, GRAY, 1)
        c.text_c(x1 + bw // 2, y0 + 68, s2, GRAY, 1)
        centers.append((x1 + bw // 2, y0 + bh // 2))
        if i < len(stages) - 1:
            c.arrow(x1 + bw + 4, y0 + bh // 2, x1 + bw + gap - 4, y0 + bh // 2, GRAY, 3, 11)

    # Parallel lower branch: labour-productivity pathway from stage 2
    px, py = centers[1][0], 260
    c.rect(px - 90, py, px + 90, py + 70, DARK_GREEN, LIGHT_GREEN)
    c.text_c(px, py + 14, "LABOUR", BLACK, 1)
    c.text_c(px, py + 30, "PRODUCTIVITY LOSS", BLACK, 1)
    c.text_c(px, py + 50, "absenteeism, slower work", GRAY, 1)
    c.arrow(centers[1][0], y0 + bh + 4, px, py - 4, GRAY, 2, 9)
    # productivity loss also feeds economic expenditure box
    c.arrow(px + 90, py + 20, centers[3][0], y0 + bh + 6, GRAY, 2, 9)

    # Intervention markers (early action cheaper)
    c.rect(40, 360, 860, 412, DARK_GREEN, (240, 250, 240))
    c.text_c(450, 372, "Early intervention is cheapest upstream", DARK_GREEN, 1)
    c.text_c(450, 392, "Prevention & heat-health action plans --->  avoided emergency care & lost output", GRAY, 1)
    # upstream arrow
    c.arrow(760, 345, 120, 345, MED_GREEN, 2, 10)
    c.text(560, 328, "lower cost of action", MED_GREEN, 1)

    c.text(40, 470, "Figure 3: Acting early in the chain averts the far larger downstream costs of treatment and lost output", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Transmission_Pathway.png'))
    print("  Figure_3_Transmission_Pathway.png done")


def gen_fig4():
    """Figure 4: Integrated framework for climate-ready economies."""
    c = PNGCanvas(940, 500)
    c.text_c(470, 10, "Integrated Framework for Climate-Ready Economies", BLACK, 2)

    layers = [
        ("ANALYSIS",
         "Integrated health-economic modelling; AI & geospatial vulnerability mapping",
         DARK_BLUE, PALE_BLUE),
        ("POLICY INSTRUMENTS",
         "Carbon pricing - clean energy - resilient infrastructure - heat-health plans",
         MED_BLUE, LIGHT_BLUE),
        ("FINANCE & INSTITUTIONS",
         "Climate-informed health budgeting; public, private & international finance",
         DARK_GREEN, LIGHT_GREEN),
        ("CLIMATE-READY ECONOMY",
         "Anticipatory resilience, protected health coverage, equitable outcomes",
         ORANGE, LIGHT_ORANGE),
    ]
    lx1, lx2 = 180, 760
    top = 60
    lh = 62
    gap = 24
    for i, (title, sub, col, fill) in enumerate(layers):
        y1 = top + i * (lh + gap)
        y2 = y1 + lh
        c.rect(lx1, y1, lx2, y2, col, fill)
        c.text_c((lx1 + lx2) // 2, y1 + 14, title, BLACK, 1)
        c.text_c((lx1 + lx2) // 2, y1 + 36, sub, GRAY, 1)
        if i < len(layers) - 1:
            midx = (lx1 + lx2) // 2
            c.arrow(midx, y2 + 2, midx, y2 + gap - 2, GRAY, 3, 10)

    # Right-hand indicator feedback loop (outcomes -> analysis)
    y_bottom = top + 3 * (lh + gap) + lh // 2
    y_top = top + lh // 2
    c.line(lx2 + 10, y_bottom, 850, y_bottom, PURPLE, 2)
    c.line(850, y_bottom, 850, y_top, PURPLE, 2)
    c.arrow(850, y_top, lx2 + 10, y_top, PURPLE, 2, 9)
    c.text(858, top + 2 * (lh + gap) - 6, "measurable", PURPLE, 1)
    c.text(858, top + 2 * (lh + gap) + 10, "indicators", PURPLE, 1)

    # Left-hand equity anchor
    c.line(lx1 - 10, y_top, 100, y_top, RED, 2)
    c.line(100, y_top, 100, y_bottom, RED, 2)
    c.arrow(100, y_bottom, lx1 - 10, y_bottom, RED, 2, 9)
    c.text(44, top + 2 * (lh + gap) - 6, "equity &", RED, 1)
    c.text(44, top + 2 * (lh + gap) + 10, "co-benefits", RED, 1)

    c.text(40, 474, "Figure 4: Linking analysis to instruments, finance, and measurable, equitable resilience outcomes", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Integrated_Framework.png'))
    print("  Figure_4_Integrated_Framework.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating climate-inaction chapter figures...")
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
