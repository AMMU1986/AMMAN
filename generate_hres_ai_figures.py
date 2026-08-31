#!/usr/bin/env python3
"""
Generate 4 figures (PNG) for the chapter
"Physics-Informed ML, Digital Twins, and AI-Driven Optimization for
Nanofluid Thermal Systems".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py
(no third-party dependencies).

  Figure 1 - PINN architecture for heat transfer
  Figure 2 - Predicted vs measured convective heat transfer coefficient
  Figure 3 - Reference architecture of a thermal digital twin
  Figure 4 - Pareto front for nanofluid heat exchanger optimization
"""

import os
import math
import random

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

OUTPUT_DIR = '/projects/sandbox/AMMAN/hres_ai_figures'


def gen_fig1():
    """Figure 1: PINN architecture for heat transfer."""
    c = PNGCanvas(780, 470)
    c.text_c(390, 10, "Physics-Informed Neural Network for Heat Transfer", BLACK, 2)

    # Input layer (coordinates)
    c.rect(30, 150, 140, 300, DARK_BLUE, PALE_BLUE)
    c.text_c(85, 165, "INPUTS", BLACK, 1)
    c.text_c(85, 205, "x", BLACK, 1)
    c.text_c(85, 235, "y", BLACK, 1)
    c.text_c(85, 265, "t", BLACK, 1)
    for cy in (205, 235, 265):
        c.circle(85, cy + 6, 8, MED_BLUE, LIGHT_BLUE)

    # Hidden layers
    hl_x = [200, 300, 400]
    node_ys = [170, 210, 250, 290]
    for hx in hl_x:
        for ny in node_ys:
            c.circle(hx, ny, 10, MED_GREEN, LIGHT_GREEN)
    # connections input -> first hidden
    for ny in node_ys:
        c.line(140, 235, hl_x[0], ny, LIGHT_GRAY, 1)
    # connections between hidden layers
    for a in range(len(hl_x) - 1):
        for ny1 in node_ys:
            for ny2 in node_ys:
                c.line(hl_x[a], ny1, hl_x[a + 1], ny2, LIGHT_GRAY, 1)
    c.text_c(300, 320, "Hidden layers (fully connected)", GRAY, 1)

    # Output (field prediction)
    c.rect(470, 200, 580, 270, ORANGE, LIGHT_ORANGE)
    c.text_c(525, 218, "OUTPUT", BLACK, 1)
    c.text_c(525, 240, "T(x,y,t)", BLACK, 1)
    for ny in node_ys:
        c.line(hl_x[-1], ny, 470, 235, LIGHT_GRAY, 1)

    # Automatic differentiation box
    c.rect(620, 60, 760, 150, PURPLE, LIGHT_PURPLE)
    c.text_c(690, 75, "AUTO-DIFF", BLACK, 1)
    c.text_c(690, 100, "dT/dt, grad T,", BLACK, 1)
    c.text_c(690, 120, "Laplacian T", BLACK, 1)
    c.arrow(580, 220, 690, 150, PURPLE, 2, 8)

    # Physics residual (PDE)
    c.rect(620, 180, 760, 285, DARK_GREEN, LIGHT_GREEN)
    c.text_c(690, 195, "PHYSICS LOSS", BLACK, 1)
    c.text_c(690, 220, "energy eqn", BLACK, 1)
    c.text_c(690, 240, "residual", BLACK, 1)
    c.text_c(690, 262, "= 0 target", GRAY, 1)
    c.arrow(690, 150, 690, 180, PURPLE, 2, 8)

    # Data loss
    c.rect(620, 315, 760, 410, RED, LIGHT_RED)
    c.text_c(690, 330, "DATA LOSS", BLACK, 1)
    c.text_c(690, 353, "sensors, BC,", BLACK, 1)
    c.text_c(690, 373, "initial cond.", BLACK, 1)
    c.arrow(580, 255, 620, 350, RED, 2, 8)

    # Total loss + backprop
    c.rect(300, 370, 520, 430, GOLD, LIGHT_GOLD)
    c.text_c(410, 388, "TOTAL LOSS = Physics + Data", BLACK, 1)
    c.text_c(410, 410, "backprop -> update weights", GRAY, 1)
    c.arrow(690, 285, 520, 400, DARK_GREEN, 2, 8)
    c.arrow(690, 410, 520, 410, RED, 2, 8)
    # feedback to hidden layers
    c.line(300, 400, 300, 340, GOLD, 2)
    c.arrow(300, 340, 300, 302, GOLD, 2, 8)

    c.text(30, 452, "Figure 1: PINN architecture embedding the energy equation as a soft constraint via automatic differentiation", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_PINN_Architecture.png'))
    print("  Figure_1_PINN_Architecture.png done")


def gen_fig2():
    """Figure 2: Predicted vs measured convective heat transfer coefficient."""
    c = PNGCanvas(720, 560)
    c.text_c(360, 10, "Predicted vs Measured Convective Heat Transfer Coefficient", BLACK, 2)

    # Plot area
    ox, oy = 90, 470     # origin (bottom-left)
    ax_len = 540
    top = 60
    # axes
    c.line(ox, oy, ox + ax_len, oy, BLACK, 2)   # x axis
    c.line(ox, oy, ox, top, BLACK, 2)           # y axis
    c.text_c(ox + ax_len // 2, 520, "Measured h  (W/m^2 K)", BLACK, 1)
    # y label (vertical-ish, drawn as stacked)
    c.text(15, 230, "Pred", BLACK, 1)
    c.text(15, 245, "icted", BLACK, 1)
    c.text(15, 260, "h", BLACK, 1)

    # axis ticks (0..4000 mapped)
    vmax = 4000.0
    def sx(v): return int(ox + (v / vmax) * ax_len)
    def sy(v): return int(oy - (v / vmax) * (oy - top))
    for v in range(0, 4001, 1000):
        c.text_c(sx(v), oy + 12, str(v), BLACK, 1)
        c.text(ox - 45, sy(v) - 4, str(v), BLACK, 1)
        c.line(ox, sy(v), ox + 4, sy(v), BLACK, 1)
        c.line(sx(v), oy, sx(v), oy - 4, BLACK, 1)

    # parity line y=x
    c.line(sx(0), sy(0), sx(vmax), sy(vmax), GRAY, 2)
    c.text(sx(3050), sy(3300), "y = x", GRAY, 1)
    # +/-10% band lines
    for f in (1.1, 0.9):
        c.line(sx(0), sy(0), sx(vmax), sy(vmax * f), LIGHT_BLUE, 1)
    c.text(sx(3100), sy(2500), "+/-10%", MED_BLUE, 1)

    # scatter data for three nanofluids
    random.seed(11)
    series = [
        ("Al2O3/water", MED_BLUE, LIGHT_BLUE, 900, 3600),
        ("CuO/water", ORANGE, LIGHT_ORANGE, 1100, 3400),
        ("TiO2/EG", MED_GREEN, LIGHT_GREEN, 800, 3000),
    ]
    for name, col, fill, lo, hi in series:
        for _ in range(16):
            meas = random.uniform(lo, hi)
            pred = meas * (1 + random.uniform(-0.08, 0.08))
            c.circle(sx(meas), sy(pred), 4, col, fill)

    # legend
    ly = 80
    for name, col, fill, lo, hi in series:
        c.circle(ox + 30, ly, 5, col, fill)
        c.text(ox + 45, ly - 4, name, BLACK, 1)
        ly += 22
    c.text(ox + 30, ly + 6, "Points within +/-10% band: physics-aware model", GRAY, 1)

    c.text(30, 545, "Figure 2: Parity plot of physics-aware predictions against measured convective coefficients", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Parity_Plot.png'))
    print("  Figure_2_Parity_Plot.png done")


def gen_fig3():
    """Figure 3: Reference architecture of a thermal digital twin."""
    c = PNGCanvas(780, 500)
    c.text_c(390, 10, "Reference Architecture of a Thermal Digital Twin", BLACK, 2)

    # Physical asset
    c.rect(40, 190, 190, 300, DARK_BLUE, PALE_BLUE)
    c.text_c(115, 210, "PHYSICAL", BLACK, 1)
    c.text_c(115, 228, "ASSET", BLACK, 1)
    c.text_c(115, 255, "heat exch.,", GRAY, 1)
    c.text_c(115, 273, "cooling loop", GRAY, 1)

    # Sensors
    c.rect(40, 330, 190, 400, MED_GREEN, LIGHT_GREEN)
    c.text_c(115, 348, "SENSORS", BLACK, 1)
    c.text_c(115, 370, "T, flow, dP,", GRAY, 1)
    c.text_c(115, 388, "fluid probes", GRAY, 1)
    c.arrow(115, 300, 115, 330, GRAY, 2, 8)

    # Data assimilation
    c.rect(250, 320, 420, 410, ORANGE, LIGHT_ORANGE)
    c.text_c(335, 338, "DATA ASSIMILATION", BLACK, 1)
    c.text_c(335, 362, "Kalman / particle", GRAY, 1)
    c.text_c(335, 380, "filter, sensor fusion,", GRAY, 1)
    c.text_c(335, 398, "state estimation", GRAY, 1)
    c.arrow(190, 365, 250, 365, GRAY, 2, 8)

    # Model core
    c.rect(250, 150, 420, 280, DARK_GREEN, LIGHT_GREEN)
    c.text_c(335, 168, "MODEL CORE", BLACK, 1)
    c.text_c(335, 195, "Physics (CFD/ROM)", GRAY, 1)
    c.text_c(335, 218, "+ ML surrogate", GRAY, 1)
    c.text_c(335, 245, "+ fluid-condition", GRAY, 1)
    c.text_c(335, 263, "model", GRAY, 1)
    c.arrow(335, 320, 335, 280, PURPLE, 2, 8)
    c.arrow(360, 280, 360, 320, PURPLE, 2, 8)
    c.text(425, 300, "update / estimate", PURPLE, 1)

    # Services
    services = [
        ("MONITORING", 60, MED_BLUE, LIGHT_BLUE, "virtual sensing"),
        ("PREDICTION", 150, PURPLE, LIGHT_PURPLE, "RUL, forecast"),
        ("OPTIMIZATION", 240, GOLD, LIGHT_GOLD, "setpoints"),
        ("CONTROL", 330, RED, LIGHT_RED, "actions"),
    ]
    for name, y, col, fill, sub in services:
        c.rect(500, y, 740, y + 70, col, fill)
        c.text_c(620, y + 20, name, BLACK, 1)
        c.text_c(620, y + 44, sub, GRAY, 1)
    c.arrow(420, 200, 500, 95, DARK_GREEN, 2, 8)
    c.arrow(420, 215, 500, 185, DARK_GREEN, 2, 8)
    c.arrow(420, 230, 500, 275, DARK_GREEN, 2, 8)
    c.arrow(420, 250, 500, 365, DARK_GREEN, 2, 8)

    # Closed-loop feedback control -> physical asset
    c.line(620, 400, 620, 450, RED, 2)
    c.line(620, 450, 115, 450, RED, 2)
    c.arrow(115, 450, 115, 400, RED, 2, 8)
    c.text_c(370, 465, "Closed-loop feedback (control actions to physical asset)", RED, 1)

    c.text(30, 485, "Figure 3: Thermal digital twin linking sensing, assimilation, a physics-plus-learning core, and services", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Digital_Twin_Architecture.png'))
    print("  Figure_3_Digital_Twin_Architecture.png done")


def gen_fig4():
    """Figure 4: Pareto front for nanofluid heat exchanger optimization."""
    c = PNGCanvas(720, 560)
    c.text_c(360, 10, "Pareto Front: Nanofluid Heat Exchanger Optimization", BLACK, 2)

    ox, oy = 90, 470
    top = 60
    ax_len = 560
    c.line(ox, oy, ox + ax_len, oy, BLACK, 2)
    c.line(ox, oy, ox, top, BLACK, 2)
    c.text_c(ox + ax_len // 2, 520, "Pumping power  (W)", BLACK, 1)
    c.text(15, 240, "Heat", BLACK, 1)
    c.text(15, 256, "trans.", BLACK, 1)
    c.text(15, 272, "rate", BLACK, 1)
    c.text(15, 288, "(kW)", BLACK, 1)

    pmax = 100.0   # pumping power axis max (W)
    qmax = 10.0    # heat transfer rate axis max (kW)
    def sx(v): return int(ox + (v / pmax) * ax_len)
    def sy(v): return int(oy - (v / qmax) * (oy - top))
    for v in range(0, 101, 20):
        c.text_c(sx(v), oy + 12, str(v), BLACK, 1)
        c.line(sx(v), oy, sx(v), oy - 4, BLACK, 1)
    for v in range(0, 11, 2):
        c.text(ox - 40, sy(v) - 4, str(v), BLACK, 1)
        c.line(ox, sy(v), ox + 4, sy(v), BLACK, 1)

    # Pareto fronts for three concentrations (higher conc -> higher Q but higher P)
    concs = [
        ("phi = 0.5%", MED_BLUE, LIGHT_BLUE, 6.5),
        ("phi = 1.0%", ORANGE, LIGHT_ORANGE, 7.8),
        ("phi = 2.0%", RED, LIGHT_RED, 8.9),
    ]
    for name, col, fill, qcap in concs:
        pts = []
        for i in range(9):
            p = 8 + i * 11
            # diminishing returns curve toward qcap
            q = qcap * (1 - math.exp(-p / 35.0))
            pts.append((sx(p), sy(q)))
        for i in range(len(pts) - 1):
            c.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], col, 2)
        for px, py in pts:
            c.circle(px, py, 4, col, fill)

    # Dominated cloud
    random.seed(23)
    for _ in range(40):
        p = random.uniform(10, 95)
        qmaxlocal = 8.9 * (1 - math.exp(-p / 35.0))
        q = random.uniform(1.5, qmaxlocal - 0.5)
        if q > 1:
            c.circle(sx(p), sy(q), 2, LIGHT_GRAY, LIGHT_GRAY)

    # knee annotation
    kp, kq = 40, 7.8 * (1 - math.exp(-40 / 35.0))
    c.circle(sx(kp), sy(kq), 6, DARK_GREEN, LIGHT_GREEN)
    c.text(sx(kp) + 10, sy(kq) - 10, "knee (balanced)", DARK_GREEN, 1)

    # legend
    ly = 85
    for name, col, fill, qcap in concs:
        c.circle(ox + 350, ly, 5, col, fill)
        c.text(ox + 365, ly - 4, name, BLACK, 1)
        ly += 22
    c.circle(ox + 350, ly, 2, LIGHT_GRAY, LIGHT_GRAY)
    c.text(ox + 365, ly - 4, "dominated designs", BLACK, 1)

    c.text(30, 545, "Figure 4: Pareto fronts trading heat transfer rate against pumping power for three volume fractions", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Pareto_Front.png'))
    print("  Figure_4_Pareto_Front.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating HRES AI/ML chapter figures...")
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
