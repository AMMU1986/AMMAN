#!/usr/bin/env python3
"""
Generate the 4 figures for the chapter:
"Techno-Economic and Sustainability Assessment of Hybrid Renewable Energy Systems".

Reuses the pure-standard-library PNGCanvas renderer defined in generate_figures.py
(no matplotlib / Pillow required in this sandbox).
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/techno_economic_figures'


def gen_fig1():
    """Figure 1: HRES layered architecture and classification."""
    c = PNGCanvas(760, 500)
    c.text_c(380, 10, "Hybrid Renewable Energy System: Architecture and Classification", BLACK, 1)

    # --- Generation layer ---
    c.text(20, 40, "Generation Layer", DARK_GREEN, 1)
    gens = [("Solar PV", DARK_GREEN, LIGHT_GREEN),
            ("Wind", MED_BLUE, LIGHT_BLUE),
            ("Biomass", GOLD, LIGHT_GOLD),
            ("Micro-hydro", DARK_BLUE, PALE_BLUE),
            ("Backup Gen", GRAY, LIGHT_GRAY)]
    gx = 20
    gen_centers = []
    for label, col, fill in gens:
        c.rect(gx, 58, gx+128, 98, col, fill)
        c.text_c(gx+64, 72, label, BLACK, 1)
        gen_centers.append(gx+64)
        gx += 140

    # --- Common bus ---
    c.fill_rect(40, 150, 720, 170, DARK_BLUE)
    c.text_c(380, 155, "Common AC / DC Bus", WHITE, 1)
    # arrows generation -> bus
    for cx in gen_centers:
        c.arrow(cx, 98, cx, 150, GRAY, 2, 6)

    # --- Power conditioning layer (label on bus) ---
    c.text(560, 128, "Power Conditioning", PURPLE, 1)

    # --- Storage layer ---
    c.text(20, 195, "Storage Layer", RED, 1)
    stores = [("Battery", RED, LIGHT_RED),
              ("Pumped Hydro", MED_BLUE, LIGHT_BLUE),
              ("Hydrogen", PURPLE, LIGHT_PURPLE),
              ("Thermal", ORANGE, LIGHT_ORANGE)]
    sx = 60
    for label, col, fill in stores:
        c.rect(sx, 212, sx+150, 250, col, fill)
        c.text_c(sx+75, 226, label, BLACK, 1)
        c.arrow(sx+75, 212, sx+75, 170, GRAY, 2, 6)
        sx += 165

    # --- EMS layer ---
    c.rect(230, 285, 530, 335, DARK_GREEN, LIGHT_GREEN)
    c.text_c(380, 298, "Energy Management System (EMS)", BLACK, 1)
    c.text_c(380, 314, "forecast - dispatch - control", GRAY, 1)
    c.arrow(380, 170, 380, 285, MED_GREEN, 2, 7)
    # loads/grid
    c.rect(60, 285, 180, 335, DARK_BLUE, PALE_BLUE)
    c.text_c(120, 303, "Loads", BLACK, 1)
    c.rect(580, 285, 700, 335, GOLD, LIGHT_GOLD)
    c.text_c(640, 303, "Grid / Export", BLACK, 1)
    c.arrow(230, 310, 180, 310, GRAY, 2, 6)
    c.arrow(530, 310, 580, 310, GRAY, 2, 6)

    # --- Classification axes box ---
    c.rect(40, 365, 720, 475, GRAY, (248, 248, 248))
    c.text_c(380, 374, "Classification Axes", BLACK, 1)
    c.text(60, 398, "Coupling topology:", DARK_BLUE, 1)
    c.text(230, 398, "DC-coupled / AC-coupled / Hybrid", BLACK, 1)
    c.text(60, 420, "Grid relationship:", RED, 1)
    c.text(230, 420, "Grid-connected / Off-grid / Grid-interactive", BLACK, 1)
    c.text(60, 442, "System scale:", DARK_GREEN, 1)
    c.text(230, 442, "Household / Community / Utility-scale", BLACK, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_HRES_Architecture.png'))
    print("  Figure_1_HRES_Architecture.png done")


def gen_fig2():
    """Figure 2: Techno-economic modeling and optimization workflow."""
    c = PNGCanvas(760, 460)
    c.text_c(380, 10, "Techno-Economic Modeling and Optimization Workflow", BLACK, 1)

    # Stage boxes left-to-right
    boxes = [
        ("Resource &\nLoad Data", 30, 70, DARK_BLUE, PALE_BLUE),
        ("Component\nModels", 220, 70, DARK_GREEN, LIGHT_GREEN),
        ("Sizing &\nDispatch\nOptimizer", 410, 60, PURPLE, LIGHT_PURPLE),
        ("Reliability &\nEconomic\nIndicators", 600, 60, ORANGE, LIGHT_ORANGE),
    ]
    centers = []
    for label, bx, by, col, fill in boxes:
        bh = 90
        c.rect(bx, by, bx+130, by+bh, col, fill)
        lines = label.split("\n")
        for li, ln in enumerate(lines):
            c.text_c(bx+65, by+20+li*16, ln, BLACK, 1)
        centers.append((bx+65, by, bx+130, by+bh))

    # arrows between stages
    for i in range(len(centers)-1):
        _, _, rx, _ = centers[i]
        nx, ny, _, nbh = centers[i+1]
        c.arrow(rx, 110, nx-65, 110, GRAY, 2, 7)

    # Inputs under data
    c.text(30, 185, "- irradiance, wind", GRAY, 1)
    c.text(30, 202, "- demand profile", GRAY, 1)
    c.text(30, 219, "- cost / price data", GRAY, 1)
    # under component models
    c.text(220, 185, "- PV / wind power", GRAY, 1)
    c.text(220, 202, "- battery / fade", GRAY, 1)
    c.text(220, 219, "- biomass / genset", GRAY, 1)
    # under optimizer
    c.text(410, 185, "- MILP / metaheur.", GRAY, 1)
    c.text(410, 202, "- MPC / RL dispatch", GRAY, 1)
    c.text(410, 219, "- co-optimization", GRAY, 1)
    # under indicators
    c.text(600, 185, "- LCOE / NPC", GRAY, 1)
    c.text(600, 202, "- IRR / payback", GRAY, 1)
    c.text(600, 219, "- LPSP / emissions", GRAY, 1)

    # Pareto trade-off output
    c.rect(410, 270, 730, 440, DARK_BLUE, (248, 250, 255))
    c.text_c(570, 280, "Output: Cost-Reliability-Emission Trade-off", BLACK, 1)
    c.vline(440, 305, 420, BLACK)
    c.hline(440, 710, 420, BLACK)
    c.text(445, 300, "Cost", BLACK, 1)
    c.text(640, 425, "Reliability", BLACK, 1)
    pts = [(460, 320), (490, 335), (530, 352), (585, 372), (650, 395), (700, 410)]
    for i in range(len(pts)-1):
        c.line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], RED, 2)
    for px, py in pts:
        c.circle(px, py, 4, RED, RED)
    c.text(470, 400, "Pareto front", RED, 1)

    # Feedback loop (routed above the stage boxes to avoid overlap)
    c.text_c(380, 44, "Iterative feedback loop", RED, 1)
    c.line(475, 60, 475, 36, RED, 1)       # up from optimizer
    c.line(475, 36, 95, 36, RED, 1)         # across the top
    c.arrow(95, 36, 95, 60, RED, 1, 7)      # down into data stage

    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Modeling_Workflow.png'))
    print("  Figure_2_Modeling_Workflow.png done")


def gen_fig3():
    """Figure 3: Cost trajectories (left) and LCOE sensitivity tornado (right)."""
    c = PNGCanvas(760, 460)
    c.text_c(380, 10, "Economic Uncertainty: Cost Trajectories and LCOE Sensitivity", BLACK, 1)

    # ---- (a) Cost trajectories ----
    c.text(30, 36, "(a) Indexed Cost Trajectory (2015 = 100)", BLACK, 1)
    ox, oy = 60, 230          # origin
    ax_w, ax_h = 300, 170
    c.vline(ox, oy-ax_h, oy, BLACK)
    c.hline(ox, ox+ax_w, oy, BLACK)
    # y labels
    for frac, lbl in [(0.0, "0"), (0.5, "50"), (1.0, "100")]:
        y = int(oy - frac*ax_h)
        c.text(ox-30, y-3, lbl, BLACK, 1)
        c.hline(ox-3, ox, y, BLACK)
    # x labels (2015..2035)
    years = [2015, 2020, 2025, 2030, 2035]
    for i, yr in enumerate(years):
        x = ox + int(i/(len(years)-1)*ax_w)
        c.text_c(x, oy+8, str(yr), BLACK, 1)
        c.vline(x, oy, oy+3, BLACK)
    # three declining curves (indexed, start 100)
    series = [
        ("PV", MED_BLUE, [100, 62, 45, 36, 30]),
        ("Wind", DARK_GREEN, [100, 72, 58, 50, 44]),
        ("Battery", RED, [100, 55, 38, 28, 22]),
    ]
    for name, col, vals in series:
        prev = None
        for i, v in enumerate(vals):
            x = ox + int(i/(len(vals)-1)*ax_w)
            y = int(oy - v/100.0*ax_h)
            if prev:
                c.line(prev[0], prev[1], x, y, col, 2)
            c.circle(x, y, 3, col, col)
            prev = (x, y)
    # legend
    ly = 60
    for name, col, _ in series:
        c.hline(300, 325, ly, col)
        c.circle(312, ly, 3, col, col)
        c.text(330, ly-3, name, BLACK, 1)
        ly += 16

    # ---- (b) Tornado sensitivity ----
    c.text(420, 36, "(b) LCOE Sensitivity (Tornado)", BLACK, 1)
    tx = 560       # center axis
    ty0 = 60
    bar_h = 20
    gap = 10
    c.vline(tx, ty0-5, ty0 + 6*(bar_h+gap), BLACK)
    c.text_c(tx, ty0 + 6*(bar_h+gap)+8, "- LCOE  |  + LCOE", BLACK, 1)
    params = [
        ("Discount rate", 120, 125, RED, LIGHT_RED),
        ("Capacity factor", 100, 95, MED_BLUE, LIGHT_BLUE),
        ("Storage cost", 80, 85, PURPLE, LIGHT_PURPLE),
        ("CapEx", 70, 65, DARK_GREEN, LIGHT_GREEN),
        ("O&M cost", 45, 40, ORANGE, LIGHT_ORANGE),
        ("Fuel price", 30, 28, GOLD, LIGHT_GOLD),
    ]
    yy = ty0
    for name, lft, rgt, col, fill in params:
        # left (negative) and right (positive) bars
        c.rect(tx-lft, yy, tx, yy+bar_h, col, fill)
        c.rect(tx, yy, tx+rgt, yy+bar_h, col, fill)
        c.text(420, yy+5, name, BLACK, 1)
        yy += bar_h + gap

    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Cost_Sensitivity.png'))
    print("  Figure_3_Cost_Sensitivity.png done")


def gen_fig4():
    """Figure 4: Intelligent closed-loop assessment framework."""
    c = PNGCanvas(760, 480)
    c.text_c(380, 10, "Intelligent Closed-Loop Assessment Framework for HRES", BLACK, 1)

    # Physical asset
    c.rect(300, 50, 460, 100, DARK_BLUE, PALE_BLUE)
    c.text_c(380, 65, "Physical HRES Asset", BLACK, 1)
    c.text_c(380, 81, "sensors - SCADA", GRAY, 1)

    # Four intelligence modules around the loop
    mods = [
        ("AI/ML Forecasting\n& Surrogate Models", 40, 150, MED_BLUE, LIGHT_BLUE),
        ("Multi-Objective\nOptimization", 540, 150, PURPLE, LIGHT_PURPLE),
        ("Digital Twin", 540, 300, DARK_GREEN, LIGHT_GREEN),
        ("Predictive Analytics\n& Monitoring", 40, 300, ORANGE, LIGHT_ORANGE),
    ]
    for label, bx, by, col, fill in mods:
        c.rect(bx, by, bx+180, by+70, col, fill)
        for li, ln in enumerate(label.split("\n")):
            c.text_c(bx+90, by+22+li*16, ln, BLACK, 1)

    # Decision core
    c.circle(380, 240, 55, GOLD, LIGHT_GOLD)
    c.text_c(380, 228, "Techno-Economic", BLACK, 1)
    c.text_c(380, 244, "& Sustainability", BLACK, 1)
    c.text_c(380, 260, "Decision", BLACK, 1)

    # Connect asset -> forecasting -> optimization -> twin -> analytics -> asset (loop)
    c.arrow(300, 80, 130, 150, GRAY, 2, 7)       # asset -> forecasting
    c.arrow(220, 175, 325, 215, GRAY, 2, 7)      # forecasting -> core
    c.arrow(435, 215, 560, 175, GRAY, 2, 7)      # core -> optimization
    c.arrow(630, 220, 630, 300, GRAY, 2, 7)      # optimization -> twin
    c.arrow(560, 335, 435, 255, GRAY, 2, 7)      # twin -> core
    c.arrow(325, 265, 220, 320, GRAY, 2, 7)      # core -> analytics
    c.arrow(130, 300, 320, 100, RED, 2, 7)       # analytics -> asset (feedback)

    # labels on flows
    c.text(150, 120, "live data", MED_BLUE, 1)
    c.text(455, 120, "designs", PURPLE, 1)
    c.text(640, 265, "simulate", DARK_GREEN, 1)
    c.text(150, 285, "health / RUL", ORANGE, 1)

    # bottom note
    c.rect(40, 400, 720, 465, GRAY, (248, 248, 248))
    c.text_c(380, 412, "Continuously refined estimates of LCOE, NPC, emissions,", BLACK, 1)
    c.text_c(380, 430, "reliability and remaining useful life over the asset lifetime", BLACK, 1)
    c.text_c(380, 448, "replace static, one-time design calculations", GRAY, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Intelligent_Framework.png'))
    print("  Figure_4_Intelligent_Framework.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating techno-economic chapter figures...")
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
