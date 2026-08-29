#!/usr/bin/env python3
"""
Generate 4 figure images (PNG) for Chapter 9
"Engineering Principles of Modern Drug Delivery".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 9.1 - Compartmental PK model + concentration-time profiles vs window
  Figure 9.2 - Controlled-release device geometries + release profiles
  Figure 9.3 - Release-model curves (zero/first-order/Higuchi/Korsmeyer-Peppas)
  Figure 9.4 - Integrated modelling workflow (material -> release -> PK -> profile)
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/dd_figures'


def gen_fig1():
    """Figure 9.1: Compartmental PK model and concentration-time profiles."""
    c = PNGCanvas(780, 470)
    c.text_c(390, 10, "Compartmental Pharmacokinetics and Concentration Profiles", BLACK, 2)

    # (a) One/two-compartment schematic (left)
    c.text(30, 42, "(a) Compartmental model", BLACK, 1)
    # Dose input
    c.rect(30, 70, 120, 105, GRAY, LIGHT_GRAY)
    c.text_c(75, 82, "Dose", BLACK, 1)
    c.text_c(75, 94, "input", GRAY, 1)
    # Central compartment
    c.rect(150, 95, 270, 175, MED_BLUE, LIGHT_BLUE)
    c.text_c(210, 112, "CENTRAL", BLACK, 1)
    c.text_c(210, 130, "(blood +", BLACK, 1)
    c.text_c(210, 146, "rapid tissues)", BLACK, 1)
    c.text_c(210, 162, "V, C(t)", GRAY, 1)
    c.arrow(120, 88, 155, 110, DARK_GREEN, 2, 8)
    c.text(120, 70, "ka (absorption)", DARK_GREEN, 1)
    # Peripheral compartment
    c.rect(150, 210, 270, 285, PURPLE, LIGHT_PURPLE)
    c.text_c(210, 228, "PERIPHERAL", BLACK, 1)
    c.text_c(210, 246, "(slow", BLACK, 1)
    c.text_c(210, 262, "tissues)", BLACK, 1)
    c.arrow(200, 178, 200, 208, GRAY, 2, 7)
    c.arrow(225, 208, 225, 178, GRAY, 2, 7)
    c.text(275, 190, "k12 / k21", GRAY, 1)
    # Elimination
    c.arrow(210, 175, 210, 178, RED, 1, 5)
    c.arrow(150, 135, 100, 135, RED, 2, 8)
    c.text(30, 118, "CL (elimination)", RED, 1)

    # (b) Concentration-time profiles (right)
    ox, oy = 360, 300     # origin of axes
    axw, axh = 380, 220
    c.text(360, 42, "(b) Plasma concentration vs time", BLACK, 1)
    c.vline(ox, oy - axh, oy, BLACK)
    c.hline(ox, ox + axw, oy, BLACK)
    c.text(360, oy - axh - 12, "Concentration", BLACK, 1)
    c.text(ox + axw - 40, oy + 8, "Time", BLACK, 1)

    # therapeutic window band
    y_mtc = oy - 165   # min toxic conc
    y_mec = oy - 55    # min effective conc
    for x in range(ox + 1, ox + axw, 3):
        c.pixel(x, y_mtc, RED)
        c.pixel(x, y_mec, DARK_GREEN)
    c.text(ox + axw - 70, y_mtc - 12, "MTC", RED, 1)
    c.text(ox + axw - 70, y_mec + 4, "MEC", DARK_GREEN, 1)

    # immediate-release: oscillating peaks (blue) - repeated doses
    prev = None
    for i in range(0, axw):
        t = i / axw * 4.0  # 4 dosing intervals
        frac = t - math.floor(t)
        # sharp rise then expo decay each interval
        amp = 150
        y = oy - int(amp * (1 - math.exp(-8 * frac)) * math.exp(-1.5 * frac))
        x = ox + i
        if prev:
            c.line(prev[0], prev[1], x, y, MED_BLUE, 1)
        prev = (x, y)

    # sustained-release: broadened lower humps (orange)
    prev = None
    for i in range(0, axw):
        t = i / axw * 4.0
        frac = t - math.floor(t)
        amp = 95
        y = oy - int(amp * (1 - math.exp(-3 * frac)) * math.exp(-0.6 * frac)) - 35
        x = ox + i
        if prev:
            c.line(prev[0], prev[1], x, y, ORANGE, 1)
        prev = (x, y)

    # zero-order constant input (green) - rises to plateau within window
    prev = None
    for i in range(0, axw):
        t = i / axw
        y = oy - int(110 * (1 - math.exp(-5 * t)))
        x = ox + i
        if prev:
            c.line(prev[0], prev[1], x, y, DARK_GREEN, 2)
        prev = (x, y)

    # legend
    c.hline(ox + 10, ox + 40, oy - axh + 12, MED_BLUE); c.text(ox + 45, oy - axh + 8, "Immediate release", BLACK, 1)
    c.hline(ox + 10, ox + 40, oy - axh + 28, ORANGE); c.text(ox + 45, oy - axh + 24, "Sustained release", BLACK, 1)
    c.hline(ox + 10, ox + 40, oy - axh + 44, DARK_GREEN); c.text(ox + 45, oy - axh + 40, "Zero-order input", BLACK, 1)

    c.text(30, 452, "Figure 9.1: Compartmental PK model and concentration-time profiles relative to the therapeutic window", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_9_1_Compartmental_PK.png'))
    print("  Figure_9_1_Compartmental_PK.png done")


def gen_fig2():
    """Figure 9.2: Controlled-release device geometries and release profiles."""
    c = PNGCanvas(780, 480)
    c.text_c(390, 10, "Controlled-Release Device Geometries and Release Profiles", BLACK, 2)

    devices = [
        ("Reservoir", "drug core + rate-\ncontrolling membrane", MED_BLUE, LIGHT_BLUE, "zero-order"),
        ("Matrix", "drug dispersed\nthroughout carrier", DARK_GREEN, LIGHT_GREEN, "sqrt(t) Higuchi"),
        ("Osmotic pump", "semipermeable shell\n+ delivery orifice", ORANGE, LIGHT_ORANGE, "zero-order"),
        ("Eroding depot", "surface-eroding\nbiodegradable polymer", PURPLE, LIGHT_PURPLE, "near zero-order"),
    ]

    col_w = 185
    for i, (name, desc, col, fill, kin) in enumerate(devices):
        cx = 30 + i * col_w + col_w // 2 - 25
        top = 55
        # device schematic
        if name == "Reservoir":
            c.circle(cx, top + 45, 40, col, LIGHT_GRAY)
            c.circle(cx, top + 45, 26, col, fill)
            c.text_c(cx, top + 42, "drug", BLACK, 1)
        elif name == "Matrix":
            c.rect(cx - 38, top + 8, cx + 38, top + 82, col, fill)
            import random
            random.seed(3)
            for _ in range(30):
                px = random.randint(cx - 34, cx + 34)
                py = random.randint(top + 12, top + 78)
                c.pixel(px, py, DARK_BLUE)
                c.pixel(px + 1, py, DARK_BLUE)
        elif name == "Osmotic pump":
            c.circle(cx, top + 45, 40, col, LIGHT_GRAY)
            c.circle(cx, top + 45, 27, col, fill)
            c.line(cx, top + 5, cx, top + 18, BLACK, 2)  # orifice
            c.text_c(cx, top - 6, "orifice", GRAY, 1)
        else:  # eroding depot
            c.rect(cx - 38, top + 8, cx + 38, top + 82, col, fill)
            # dashed eroding surface
            for y in range(top + 8, top + 82, 6):
                c.pixel(cx - 38, y, GRAY); c.pixel(cx + 38, y, GRAY)
        c.text_c(cx, top + 95, name, BLACK, 1)
        parts = desc.split("\n")
        c.text_c(cx, top + 110, parts[0], GRAY, 1)
        c.text_c(cx, top + 122, parts[1], GRAY, 1)

        # mini release profile below
        ax = 30 + i * col_w + 20
        ay = 340
        aw, ah = 130, 95
        c.vline(ax, ay - ah, ay, BLACK)
        c.hline(ax, ax + aw, ay, BLACK)
        c.text_c(ax + aw // 2, ay - ah - 12, kin, col, 1)
        prev = None
        for j in range(aw):
            t = j / aw
            if "zero" in kin:
                y = ay - int(ah * min(1.0, t * 1.05))
            elif "sqrt" in kin:
                y = ay - int(ah * math.sqrt(t))
            else:
                y = ay - int(ah * min(1.0, t * 1.02))
            x = ax + j
            if prev:
                c.line(prev[0], prev[1], x, y, col, 2)
            prev = (x, y)
        c.text(ax - 2, ay + 6, "t", BLACK, 1)
        c.text(ax - 14, ay - ah, "%", BLACK, 1)

    c.text(30, 462, "Figure 9.2: Archetypal device geometries (reservoir, matrix, osmotic, eroding) and their release profiles", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_9_2_Device_Geometries.png'))
    print("  Figure_9_2_Device_Geometries.png done")


def gen_fig3():
    """Figure 9.3: Comparison of release-model curves."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Characteristic Drug-Release Model Curves", BLACK, 2)

    ox, oy = 90, 385
    axw, axh = 560, 285
    c.vline(ox, oy - axh, oy, BLACK)
    c.hline(ox, ox + axw, oy, BLACK)
    c.text(28, oy - axh - 22, "Cumulative", BLACK, 1)
    c.text(28, oy - axh - 8, "release (%)", BLACK, 1)
    c.text(ox + axw - 60, oy + 10, "Time", BLACK, 1)
    # y gridlines
    for pct, lbl in [(0, "0"), (0.5, "50"), (1.0, "100")]:
        y = oy - int(axh * pct)
        c.text(ox - 30, y - 3, lbl, GRAY, 1)
        for x in range(ox, ox + axw, 6):
            c.pixel(x, y, LIGHT_GRAY)

    # zero-order: straight line
    prev = None
    for j in range(axw):
        t = j / axw
        y = oy - int(axh * min(1.0, t))
        x = ox + j
        if prev: c.line(prev[0], prev[1], x, y, MED_BLUE, 2)
        prev = (x, y)

    # first-order: 1 - exp(-k t)
    prev = None
    for j in range(axw):
        t = j / axw
        y = oy - int(axh * (1 - math.exp(-3.2 * t)))
        x = ox + j
        if prev: c.line(prev[0], prev[1], x, y, RED, 2)
        prev = (x, y)

    # Higuchi: sqrt(t)
    prev = None
    for j in range(axw):
        t = j / axw
        y = oy - int(axh * math.sqrt(t))
        x = ox + j
        if prev: c.line(prev[0], prev[1], x, y, DARK_GREEN, 2)
        prev = (x, y)

    # Korsmeyer-Peppas anomalous: n = 0.75
    prev = None
    for j in range(axw):
        t = j / axw
        y = oy - int(axh * min(1.0, (t ** 0.75)))
        x = ox + j
        if prev: c.line(prev[0], prev[1], x, y, PURPLE, 2)
        prev = (x, y)

    # legend (in lower-right open area, below the curves)
    lx = ox + 40
    ly = oy - axh + 8
    for k, (col, lbl) in enumerate([
        (MED_BLUE, "Zero-order (n=1)"),
        (RED, "First-order"),
        (DARK_GREEN, "Higuchi (n=0.5)"),
        (PURPLE, "Korsmeyer-Peppas (n=0.75)"),
    ]):
        c.hline(lx, lx + 28, ly + k * 16, col)
        c.text(lx + 34, ly + k * 16 - 4, lbl, BLACK, 1)

    c.text(30, 452, "Figure 9.3: Zero-order, first-order, Higuchi and power-law release curves; the exponent n diagnoses mechanism", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_9_3_Release_Models.png'))
    print("  Figure_9_3_Release_Models.png done")


def gen_fig4():
    """Figure 9.4: Integrated modelling workflow."""
    c = PNGCanvas(800, 440)
    c.text_c(400, 10, "Integrated Drug-Delivery Modelling Workflow", BLACK, 2)

    stages = [
        ("Material &\nFormulation", ["Diffusivity", "Solubility", "Geometry, loading"], MED_BLUE, LIGHT_BLUE),
        ("Release\nModel", ["Fickian diffusion", "Erosion/swelling", "In-vitro fit"], DARK_GREEN, LIGHT_GREEN),
        ("Transport /\nPK Model", ["Compartmental", "PBPK", "Absorption"], ORANGE, LIGHT_ORANGE),
        ("Predicted\nProfile", ["C(t) at target", "Therapeutic window", "Optimise design"], PURPLE, LIGHT_PURPLE),
    ]
    bw = 165
    gap = 22
    top = 80
    bh = 130
    xs = []
    for i, (title, bullets, col, fill) in enumerate(stages):
        bx = 25 + i * (bw + gap)
        xs.append((bx, bx + bw))
        c.rect(bx, top, bx + bw, top + bh, col, fill)
        parts = title.split("\n")
        c.text_c(bx + bw // 2, top + 12, parts[0], BLACK, 1)
        c.text_c(bx + bw // 2, top + 28, parts[1], BLACK, 1)
        for j, b in enumerate(bullets):
            c.text_c(bx + bw // 2, top + 52 + j * 18, b, BLACK, 1)
        if i > 0:
            c.arrow(xs[i - 1][1] + 2, top + bh // 2, bx - 4, top + bh // 2, GRAY, 3, 10)

    # Validation & uncertainty layer spanning workflow
    vy1 = top + bh + 45
    vy2 = vy1 + 60
    c.rect(25, vy1, xs[3][1], vy2, GOLD, LIGHT_GOLD)
    c.text_c(400, vy1 + 14, "VALIDATION & UNCERTAINTY ANALYSIS", BLACK, 1)
    c.text_c(400, vy1 + 34, "In-vitro-in-vivo correlation  |  Sensitivity analysis  |  Parameter uncertainty", GRAY, 1)
    for (bx1, bx2) in xs:
        midx = (bx1 + bx2) // 2
        c.line(midx, top + bh, midx, vy1, LIGHT_GRAY)

    # feedback arrow from validation back to material stage
    fy = vy2 + 22
    c.line(xs[3][0] + 80, vy2, xs[3][0] + 80, fy, GRAY, 2)
    c.line(xs[3][0] + 80, fy, xs[0][0] + 80, fy, GRAY, 2)
    c.arrow(xs[0][0] + 80, fy, xs[0][0] + 80, vy2 + 2, GRAY, 2, 8)
    c.text_c(400, fy - 12, "iterative refinement of parameters and design", GRAY, 1)

    c.text(25, 425, "Figure 9.4: Workflow linking material/formulation parameters through release and PK models to a predicted profile", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_9_4_Modelling_Workflow.png'))
    print("  Figure_9_4_Modelling_Workflow.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating drug-delivery chapter figures...")
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
