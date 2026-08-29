#!/usr/bin/env python3
"""
Generate 4 scientific figure images (PNG) for Chapter 6:
AI in Pharmacokinetics and Pharmacodynamics.
Reuses the stdlib-only PNGCanvas class from generate_figures.py.
"""

import os
from generate_figures import (
    PNGCanvas, math, random,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE, RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/ch6_figures'


def fig1_adme_workflow():
    """Figure 6.1: End-to-end ML workflow for ADME prediction."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "End-to-End ML Workflow for ADME Prediction", BLACK, 2)

    stages = [
        ("Molecular\nInput", 30, DARK_BLUE, PALE_BLUE),
        ("Representation", 180, MED_BLUE, LIGHT_BLUE),
        ("Model\nTraining", 330, DARK_GREEN, LIGHT_GREEN),
        ("Validation", 480, ORANGE, LIGHT_ORANGE),
        ("Deployment", 630, PURPLE, LIGHT_PURPLE),
    ]
    bw, bh = 120, 60
    by = 90
    centers = []
    for label, bx, col, fill in stages:
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        lines = label.split("\n")
        for li, ln in enumerate(lines):
            c.text_c(bx + bw // 2, by + bh // 2 - 8 + li * 12, ln, BLACK, 1)
        centers.append((bx + bw, by + bh // 2, bx))
    for i in range(len(stages) - 1):
        x_end = centers[i][0]
        x_next = centers[i + 1][2]
        c.arrow(x_end, by + bh // 2, x_next, by + bh // 2, GRAY, 2, 7)

    # Representation detail box
    c.rect(150, 185, 300, 300, MED_BLUE, (240, 246, 252))
    c.text_c(225, 193, "Representations", BLACK, 1)
    c.text(160, 213, "- Descriptors (logP)", GRAY, 1)
    c.text(160, 233, "- Fingerprints", GRAY, 1)
    c.text(160, 253, "- Molecular graphs", GRAY, 1)
    c.text(160, 273, "- SMILES strings", GRAY, 1)
    c.arrow(210, 185, 240, 155, MED_BLUE, 2, 6)

    # Model detail box
    c.rect(320, 185, 470, 300, DARK_GREEN, (240, 250, 240))
    c.text_c(395, 193, "Models", BLACK, 1)
    c.text(330, 213, "- Random forest", GRAY, 1)
    c.text(330, 233, "- Gradient boosting", GRAY, 1)
    c.text(330, 253, "- Graph neural nets", GRAY, 1)
    c.text(330, 273, "- Multitask deep nets", GRAY, 1)
    c.arrow(390, 185, 390, 155, DARK_GREEN, 2, 6)

    # Validation detail box
    c.rect(490, 185, 655, 300, ORANGE, (255, 248, 240))
    c.text_c(572, 193, "Validation", BLACK, 1)
    c.text(500, 213, "- Scaffold splits", GRAY, 1)
    c.text(500, 233, "- Temporal splits", GRAY, 1)
    c.text(500, 253, "- Applicability domain", GRAY, 1)
    c.text(500, 273, "- Uncertainty", GRAY, 1)
    c.arrow(540, 185, 540, 155, ORANGE, 2, 6)

    # Feedback loop
    c.line(690, 120, 690, 340, RED, 2)
    c.line(690, 340, 90, 340, RED, 2)
    c.arrow(90, 340, 90, 152, RED, 2, 7)
    c.text_c(380, 350, "Active learning feedback: prioritise informative compounds", RED, 1)

    # Endpoints label
    c.text_c(380, 385, "Endpoints: solubility, permeability, clearance, protein binding, BBB", BLACK, 1)

    c.text(40, 445, "Figure 6.1: End-to-end machine learning workflow for ADME property prediction", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_6_1_ADME_Workflow.png'))
    print("  Figure_6_1_ADME_Workflow.png done")


def fig2_exposure_response():
    """Figure 6.2: Sigmoidal exposure-response with ML surface."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Exposure-Response: Classical vs Machine-Learned", BLACK, 2)

    # Axes
    ox, oy = 90, 380
    ax_r = 640
    ax_t = 60
    c.vline(ox, ax_t, oy, BLACK)
    c.hline(ox, ax_r, oy, BLACK)
    c.arrow(ox, ax_t, ox, ax_t - 2, BLACK, 2, 6)
    c.arrow(ax_r, oy, ax_r + 2, oy, BLACK, 2, 6)
    c.text(ox - 60, 210, "Effect", BLACK, 1)
    c.text(ax_r - 120, oy + 20, "Concentration (log)", BLACK, 1)

    # y gridlines
    for frac, lbl in [(0.0, "0"), (0.5, "Emax/2"), (1.0, "Emax")]:
        y = int(oy - frac * (oy - ax_t))
        for x in range(ox, ax_r, 6):
            c.pixel(x, y, LIGHT_GRAY)
        c.text(ox - 70, y - 4, lbl, GRAY, 1)

    # Classical sigmoidal Emax curve (blue)
    prev = None
    for px in range(ox, ax_r):
        t = (px - ox) / (ax_r - ox)
        # sigmoidal in log-conc space
        val = 1.0 / (1.0 + math.exp(-9 * (t - 0.5)))
        y = int(oy - val * (oy - ax_t))
        if prev:
            c.line(prev[0], prev[1], px, y, MED_BLUE, 2)
        prev = (px, y)

    # ML surface with deviations (green) - wiggly departures + plateau dip
    prev = None
    random.seed(11)
    for px in range(ox, ax_r):
        t = (px - ox) / (ax_r - ox)
        base = 1.0 / (1.0 + math.exp(-9 * (t - 0.5)))
        wiggle = 0.06 * math.sin(t * 14) + (0.10 if 0.72 < t < 0.9 else 0.0) - (0.07 if 0.85 < t < 0.95 else 0.0)
        val = max(0, min(1.05, base + wiggle))
        y = int(oy - val * (oy - ax_t))
        if prev:
            c.line(prev[0], prev[1], px, y, MED_GREEN, 2)
        prev = (px, y)

    # scattered observed data points
    random.seed(5)
    for _ in range(38):
        t = random.random()
        base = 1.0 / (1.0 + math.exp(-9 * (t - 0.5)))
        noise = random.uniform(-0.08, 0.08)
        val = max(0, min(1.05, base + noise + (0.09 if 0.72 < t < 0.9 else 0.0)))
        px = int(ox + t * (ax_r - ox))
        py = int(oy - val * (oy - ax_t))
        c.circle(px, py, 3, GRAY, LIGHT_GRAY)

    # Legend
    c.hline(480, 520, 90, MED_BLUE); c.text(525, 84, "Sigmoidal Emax", BLACK, 1)
    c.hline(480, 520, 110, MED_GREEN); c.text(525, 104, "ML surface", BLACK, 1)
    c.circle(500, 130, 3, GRAY, LIGHT_GRAY); c.text(525, 125, "Observed data", BLACK, 1)

    c.text(40, 445, "Figure 6.2: Classical sigmoidal curve and a flexible machine-learned response surface", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_6_2_Exposure_Response.png'))
    print("  Figure_6_2_Exposure_Response.png done")


def fig3_hybrid_pbpk():
    """Figure 6.3: Hybrid PBPK-ML architecture."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Hybrid PBPK - Machine Learning Framework", BLACK, 2)

    # ML parameter predictor (left)
    c.rect(30, 70, 210, 180, DARK_GREEN, LIGHT_GREEN)
    c.text_c(120, 80, "ML Parameter Models", BLACK, 1)
    c.text(40, 100, "Input: structure", GRAY, 1)
    c.text(40, 120, "- Partition coeff (Kp)", BLACK, 1)
    c.text(40, 140, "- Intrinsic clearance", BLACK, 1)
    c.text(40, 160, "- Transport kinetics", BLACK, 1)

    # Arrow to PBPK
    c.arrow(210, 125, 275, 200, MED_GREEN, 2, 8)
    c.text(215, 150, "drug-specific", MED_GREEN, 1)
    c.text(215, 165, "parameters", MED_GREEN, 1)

    # PBPK model - organ compartments (center)
    c.rect(280, 90, 540, 360, DARK_BLUE, (238, 244, 252))
    c.text_c(410, 98, "PBPK Model (organ compartments)", BLACK, 1)
    organs = [("Lung", 300, 120, LIGHT_RED),
              ("Brain", 300, 165, LIGHT_PURPLE),
              ("Liver", 430, 120, LIGHT_ORANGE),
              ("Kidney", 430, 165, LIGHT_GREEN),
              ("Gut", 300, 210, LIGHT_GOLD),
              ("Muscle", 430, 210, LIGHT_BLUE)]
    for name, bx, by, fill in organs:
        c.rect(bx, by, bx + 95, by + 32, GRAY, fill)
        c.text_c(bx + 47, by + 10, name, BLACK, 1)
    # central blood pool
    c.rect(340, 260, 490, 300, RED, LIGHT_RED)
    c.text_c(415, 273, "Systemic Blood", BLACK, 1)
    # connect organs to blood
    for name, bx, by, fill in organs:
        c.line(bx + 47, by + 32, 415, 270, MED_BLUE, 1)
    c.text_c(410, 320, "coupled differential equations", GRAY, 1)
    c.text_c(410, 340, "mass balance across organs", GRAY, 1)

    # Output: concentration-time (right)
    c.rect(560, 90, 730, 260, ORANGE, (255, 248, 240))
    c.text_c(645, 98, "C-t Prediction", BLACK, 1)
    # small conc-time curve
    ox2, oy2 = 575, 240
    c.vline(ox2, 120, oy2, BLACK)
    c.hline(ox2, 720, oy2, BLACK)
    prev = None
    for px in range(ox2, 720):
        t = (px - ox2) / (720 - ox2)
        val = 100 * (math.exp(-3.2 * t) - math.exp(-9 * t))
        y = int(oy2 - val * 1.1)
        if prev:
            c.line(prev[0], prev[1], px, y, MED_BLUE, 2)
        prev = (px, y)
    c.text(ox2 + 5, 118, "Conc", GRAY, 1)
    c.text(660, oy2 + 6, "Time", GRAY, 1)
    c.arrow(540, 175, 560, 175, BLACK, 2, 7)

    # Validation feedback
    c.rect(560, 290, 730, 360, PURPLE, LIGHT_PURPLE)
    c.text_c(645, 300, "Validate & calibrate", BLACK, 1)
    c.text(570, 320, "- vs clinical data", GRAY, 1)
    c.text(570, 340, "- residual correction", GRAY, 1)
    c.line(645, 290, 645, 268, PURPLE, 2)
    c.arrow(645, 268, 645, 262, PURPLE, 2, 6)

    c.text(40, 445, "Figure 6.3: Hybrid PBPK-ML framework; learned models supply drug-specific parameters", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_6_3_Hybrid_PBPK.png'))
    print("  Figure_6_3_Hybrid_PBPK.png done")


def fig4_precision_dosing():
    """Figure 6.4: Closed-loop model-informed precision dosing."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Closed-Loop Model-Informed Precision Dosing", BLACK, 2)

    # 4 nodes arranged in a loop
    nodes = [
        ("Patient\nMeasurements", 120, 110, MED_BLUE, LIGHT_BLUE),
        ("Predictive\nModel", 560, 110, DARK_GREEN, LIGHT_GREEN),
        ("Dose\nRecommendation", 560, 320, ORANGE, LIGHT_ORANGE),
        ("Administer &\nMonitor", 120, 320, PURPLE, LIGHT_PURPLE),
    ]
    bw, bh = 170, 80
    ctrs = []
    for label, cx, cy, col, fill in nodes:
        c.rect(cx - bw // 2, cy - bh // 2, cx + bw // 2, cy + bh // 2, col, fill)
        for li, ln in enumerate(label.split("\n")):
            c.text_c(cx, cy - 8 + li * 14, ln, BLACK, 1)
        ctrs.append((cx, cy))

    # Arrows around the loop (clockwise)
    c.arrow(ctrs[0][0] + bw // 2, ctrs[0][1], ctrs[1][0] - bw // 2, ctrs[1][1], GRAY, 2, 9)
    c.text_c(340, 95, "covariates, biomarkers, drug levels", GRAY, 1)
    c.arrow(ctrs[1][0], ctrs[1][1] + bh // 2, ctrs[2][0], ctrs[2][1] - bh // 2, GRAY, 2, 9)
    c.text(600, 210, "target", GRAY, 1)
    c.text(600, 225, "exposure", GRAY, 1)
    c.arrow(ctrs[2][0] - bw // 2, ctrs[2][1], ctrs[3][0] + bw // 2, ctrs[3][1], GRAY, 2, 9)
    c.text_c(340, 305, "individualised dose", GRAY, 1)
    c.arrow(ctrs[3][0], ctrs[3][1] - bh // 2, ctrs[0][0], ctrs[0][1] + bh // 2, GRAY, 2, 9)
    c.text(70, 210, "new", GRAY, 1)
    c.text(70, 225, "data", GRAY, 1)

    # Center annotation
    c.rect(300, 190, 460, 245, GOLD, LIGHT_GOLD)
    c.text_c(380, 200, "Bayesian update", BLACK, 1)
    c.text_c(380, 218, "refine per patient", BLACK, 1)
    c.text_c(380, 232, "each iteration", GRAY, 1)

    # Bottom note
    c.text_c(380, 390, "Especially valuable for narrow-therapeutic-window drugs", RED, 1)
    c.text_c(380, 408, "(immunosuppressants, anticoagulants, aminoglycosides, oncology agents)", GRAY, 1)

    c.text(40, 448, "Figure 6.4: Closed-loop model-informed precision dosing with feedback refinement", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_6_4_Precision_Dosing.png'))
    print("  Figure_6_4_Precision_Dosing.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Chapter 6 figures...")
    fig1_adme_workflow()
    fig2_exposure_response()
    fig3_hybrid_pbpk()
    fig4_precision_dosing()
    print(f"\nAll 4 figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz/1024:.1f} KB")


if __name__ == '__main__':
    main()
