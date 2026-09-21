#!/usr/bin/env python3
"""
Generate 4 original figure images (PNG) for the chapter
"Artificial Intelligence-Assisted Phytochemical Profiling and Antidiabetic
Potential of Gymnema sylvestre".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - AI-assisted phytochemical profiling workflow
  Figure 2 - Multi-target antidiabetic mechanisms of G. sylvestre
  Figure 3 - Integrative pipeline: traditional knowledge -> precision therapy
  Figure 4 - Indicative ML model performance comparison (schematic)
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/gymnema_figures'


def gen_fig1():
    """Figure 1: AI-assisted phytochemical profiling workflow."""
    c = PNGCanvas(780, 440)
    c.text_c(390, 10, "AI-Assisted Phytochemical Profiling Workflow", BLACK, 2)

    # Row of pipeline stages
    stages = [
        ("Plant Material", "G. sylvestre", "leaves", DARK_GREEN, LIGHT_GREEN),
        ("Extraction &", "Sample Prep", "fractionation", MED_GREEN, LIGHT_GREEN),
        ("LC-MS/MS", "& NMR", "spectra", MED_BLUE, LIGHT_BLUE),
        ("ML Annotation", "in silico MS", "SIRIUS", PURPLE, LIGHT_PURPLE),
        ("Database", "Matching", "COCONUT", ORANGE, LIGHT_ORANGE),
    ]
    bw, bh = 130, 78
    top = 90
    gap = 26
    centers = []
    for i, (l1, l2, l3, col, fill) in enumerate(stages):
        bx = 20 + i * (bw + gap)
        c.rect(bx, top, bx + bw, top + bh, col, fill)
        c.text_c(bx + bw // 2, top + 14, l1, BLACK, 1)
        c.text_c(bx + bw // 2, top + 30, l2, BLACK, 1)
        c.text_c(bx + bw // 2, top + 50, l3, GRAY, 1)
        centers.append((bx + bw // 2, bx, bx + bw))
        if i > 0:
            prev_right = centers[i - 1][2]
            c.arrow(prev_right + 3, top + bh // 2, bx - 3, top + bh // 2, GRAY, 3, 9)

    # Output box (annotated phytochemicals) below the last two stages
    oy1, oy2 = 240, 320
    ox1, ox2 = 430, 760
    c.rect(ox1, oy1, ox2, oy2, DARK_BLUE, PALE_BLUE)
    c.text_c((ox1 + ox2) // 2, oy1 + 14, "Annotated Phytochemical Profile", BLACK, 1)
    c.text_c((ox1 + ox2) // 2, oy1 + 34, "Gymnemic acids, saponins,", GRAY, 1)
    c.text_c((ox1 + ox2) // 2, oy1 + 48, "flavonoids, phenolics", GRAY, 1)
    # arrow from database matching down into output
    last_cx = centers[4][0]
    c.arrow(last_cx, top + bh + 3, last_cx, oy1 - 3, ORANGE, 3, 9)

    # Feedback loop: NMR confirmation improves ML models
    conf_x1, conf_y1, conf_x2, conf_y2 = 40, 240, 360, 320
    c.rect(conf_x1, conf_y1, conf_x2, conf_y2, GOLD, LIGHT_GOLD)
    c.text_c((conf_x1 + conf_x2) // 2, conf_y1 + 16, "NMR Confirmation &", BLACK, 1)
    c.text_c((conf_x1 + conf_x2) // 2, conf_y1 + 34, "Structure Verification", BLACK, 1)
    c.text_c((conf_x1 + conf_x2) // 2, conf_y1 + 54, "confirmed structures retrain models", GRAY, 1)
    # ML annotation stage center x
    ml_cx = centers[3][0]
    c.arrow(ml_cx, top + bh + 3, (conf_x1 + conf_x2) // 2, conf_y1 - 3, PURPLE, 2, 8)
    # feedback arrow back up (dashed-style via short segments)
    fbx = conf_x2
    c.line(fbx, conf_y1 + bh // 2, fbx + 20, conf_y1 + bh // 2, DARK_GREEN, 2)
    c.line(fbx + 20, conf_y1 + bh // 2, fbx + 20, 70, DARK_GREEN, 2)
    c.line(fbx + 20, 70, ml_cx, 70, DARK_GREEN, 2)
    c.arrow(ml_cx, 70, ml_cx, top - 3, DARK_GREEN, 2, 8)
    c.text(fbx + 26, 150, "iterative", DARK_GREEN, 1)
    c.text(fbx + 26, 164, "feedback", DARK_GREEN, 1)

    c.text(20, 420, "Figure 1: AI-assisted phytochemical profiling workflow, from extraction to annotation.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Profiling_Workflow.png'))
    print("  Figure_1_Profiling_Workflow.png done")


def gen_fig2():
    """Figure 2: Multi-target antidiabetic mechanisms."""
    c = PNGCanvas(780, 470)
    c.text_c(390, 10, "Multi-Target Antidiabetic Mechanisms of Gymnema sylvestre", BLACK, 2)

    # Central node
    cx, cy = 390, 240
    c.circle(cx, cy, 74, DARK_GREEN, LIGHT_GREEN)
    c.text_c(cx, cy - 18, "Blood", BLACK, 1)
    c.text_c(cx, cy - 4, "Glucose", BLACK, 1)
    c.text_c(cx, cy + 10, "Homeostasis", BLACK, 1)

    # Radial mechanism boxes
    mechs = [
        ("Sweet-Taste", "Suppression", "gurmarin, gymnemic acids", 130, 70, PURPLE, LIGHT_PURPLE),
        ("alpha-Glucosidase /", "alpha-Amylase Inhib.", "carbohydrate digestion", 470, 70, MED_BLUE, LIGHT_BLUE),
        ("Reduced Intestinal", "Glucose Uptake", "SGLT1", 560, 210, ORANGE, LIGHT_ORANGE),
        ("Insulin Secretion", "beta-cell K-ATP", "GLUT2", 470, 350, RED, LIGHT_RED),
        ("Peripheral Glucose", "Uptake", "AMPK, GLUT4", 130, 350, GOLD, LIGHT_GOLD),
        ("beta-Cell Protection", "& Regeneration", "Nrf2, PPAR-gamma", 40, 210, MED_GREEN, LIGHT_GREEN),
    ]
    bw, bh = 175, 66
    for l1, l2, l3, bx, by, col, fill in mechs:
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        c.text_c(bx + bw // 2, by + 12, l1, BLACK, 1)
        c.text_c(bx + bw // 2, by + 26, l2, BLACK, 1)
        c.text_c(bx + bw // 2, by + 46, l3, GRAY, 1)
        # arrow from box toward center
        bcx, bcy = bx + bw // 2, by + bh // 2
        dx, dy = cx - bcx, cy - bcy
        d = math.sqrt(dx * dx + dy * dy)
        sx = int(bcx + dx / d * (bh // 2 + 6))
        sy = int(bcy + dy / d * (bh // 2 + 6))
        ex = int(cx - dx / d * 78)
        ey = int(cy - dy / d * 78)
        c.arrow(sx, sy, ex, ey, GRAY, 2, 8)

    c.text(20, 452, "Figure 2: Complementary antidiabetic mechanisms and their principal molecular targets.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Antidiabetic_Mechanisms.png'))
    print("  Figure_2_Antidiabetic_Mechanisms.png done")


def gen_fig3():
    """Figure 3: Integrative pipeline from traditional knowledge to precision therapy."""
    c = PNGCanvas(780, 450)
    c.text_c(390, 10, "From Traditional Knowledge to Precision Therapeutics", BLACK, 2)

    steps = [
        ("Traditional", "Knowledge", "ethnobotany, gurmar", DARK_GREEN, LIGHT_GREEN),
        ("Phytochemical", "Profiling", "AI-assisted (Fig. 1)", MED_GREEN, LIGHT_GREEN),
        ("AI Prediction", "bioactivity /", "target inference", MED_BLUE, LIGHT_BLUE),
        ("Network Pharm.", "& Docking", "mechanisms (Fig. 2)", PURPLE, LIGHT_PURPLE),
        ("Experimental &", "Clinical", "validation", ORANGE, LIGHT_ORANGE),
        ("Precision", "Therapeutics", "personalized use", RED, LIGHT_RED),
    ]
    bw, bh = 116, 92
    top = 120
    gap = 15
    centers = []
    for i, (l1, l2, l3, col, fill) in enumerate(steps):
        bx = 15 + i * (bw + gap)
        c.rect(bx, top, bx + bw, top + bh, col, fill)
        c.text_c(bx + bw // 2, top + 16, l1, BLACK, 1)
        c.text_c(bx + bw // 2, top + 32, l2, BLACK, 1)
        c.text_c(bx + bw // 2, top + 56, l3, GRAY, 1)
        centers.append((bx, bx + bw))
        if i > 0:
            c.arrow(centers[i - 1][1] + 2, top + bh // 2, bx - 2, top + bh // 2, GRAY, 3, 8)

    # Data layer beneath
    dy1, dy2 = 270, 320
    c.rect(15, dy1, 765, dy2, DARK_BLUE, PALE_BLUE)
    c.text_c(390, dy1 + 12, "Shared Data & Knowledge Layer: curated databases, ML models, standardized chemistry", BLACK, 1)
    c.text_c(390, dy1 + 30, "(quality control links data-driven phytochemistry with sustainable cultivation)", GRAY, 1)
    for i in range(6):
        bx = 15 + i * (bw + gap) + bw // 2
        c.line(bx, top + bh, bx, dy1, LIGHT_GRAY, 1)

    # Global feedback loop arrow
    c.line(720, top - 8, 720, 90, MED_BLUE, 2)
    c.line(720, 90, 75, 90, MED_BLUE, 2)
    c.arrow(75, 90, 75, top - 3, MED_BLUE, 2, 8)
    c.text(300, 78, "insight refines targeted profiling (closed loop)", MED_BLUE, 1)

    c.text(20, 432, "Figure 3: Integrative AI-assisted pipeline translating tradition into precision therapeutics.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Integrative_Pipeline.png'))
    print("  Figure_3_Integrative_Pipeline.png done")


def gen_fig4():
    """Figure 4: Indicative ML model performance comparison (schematic)."""
    c = PNGCanvas(780, 450)
    c.text_c(390, 10, "Indicative ML Model Performance (Schematic)", BLACK, 2)

    # Grouped bars: models vs two metrics (ROC-AUC classification, R2 regression)
    models = ["Descriptor", "Fingerprint", "Graph NN", "Deep DTA"]
    model_sub = ["+ RF", "+ GBM", "(GNN)", "(seq+struct)"]
    auc = [0.78, 0.82, 0.89, 0.87]
    r2 = [0.66, 0.71, 0.83, 0.80]
    colors_a = [LIGHT_BLUE, MED_BLUE, DARK_GREEN, PURPLE]

    # Axes
    ax_x0, ax_y0 = 90, 360
    ax_top = 70
    c.vline(ax_x0, ax_top, ax_y0, BLACK)
    c.hline(ax_x0, 720, ax_y0, BLACK)
    c.text_c(46, 200, "Score", BLACK, 1)
    # y gridlines / labels 0.0 - 1.0
    for v in range(0, 11, 2):
        yy = int(ax_y0 - (v / 10.0) * (ax_y0 - ax_top))
        c.hline(ax_x0 - 4, ax_x0, yy, BLACK)
        c.text(ax_x0 - 40, yy - 3, f"{v/10:.1f}", GRAY, 1)
        if v > 0:
            for gx in range(ax_x0 + 2, 720, 6):
                c.pixel(gx, yy, LIGHT_GRAY)

    group_w = 150
    bar_w = 40
    for i, m in enumerate(models):
        gx = ax_x0 + 20 + i * group_w
        # AUC bar
        h1 = int(auc[i] * (ax_y0 - ax_top))
        c.rect(gx, ax_y0 - h1, gx + bar_w, ax_y0, BLACK, colors_a[i])
        c.text_c(gx + bar_w // 2, ax_y0 - h1 - 12, f"{auc[i]:.2f}", BLACK, 1)
        # R2 bar (hatched look via lighter fill)
        h2 = int(r2[i] * (ax_y0 - ax_top))
        c.rect(gx + bar_w + 6, ax_y0 - h2, gx + 2 * bar_w + 6, ax_y0, BLACK, LIGHT_ORANGE)
        c.text_c(gx + bar_w + 6 + bar_w // 2, ax_y0 - h2 - 12, f"{r2[i]:.2f}", BLACK, 1)
        # labels
        c.text_c(gx + bar_w + 3, ax_y0 + 12, m, BLACK, 1)
        c.text_c(gx + bar_w + 3, ax_y0 + 26, model_sub[i], GRAY, 1)

    # Legend (placed under the title, above the plot area, to avoid bar labels)
    c.rect(150, 44, 168, 56, BLACK, MED_BLUE)
    c.text(174, 45, "ROC-AUC (classification)", BLACK, 1)
    c.rect(430, 44, 448, 56, BLACK, LIGHT_ORANGE)
    c.text(454, 45, "R-squared (regression)", BLACK, 1)

    c.text(20, 400, "Figure 4: Indicative comparison across model families; values are illustrative,", BLACK, 1)
    c.text(20, 416, "drawn from typical ranges in the cited benchmarks, and require experimental confirmation.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Model_Performance.png'))
    print("  Figure_4_Model_Performance.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Gymnema sylvestre chapter figures...")
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
