#!/usr/bin/env python3
"""
Generate 4 scientific figures (PNG) for Chapter 3:
"Biomedical and Pharmacological Data Science".

Reuses the pure-stdlib PNGCanvas class from generate_figures.py so it works in a
sandbox without matplotlib/PIL/numpy.
"""

import os
import math

# Reuse the canvas + color palette + font from the existing figure generator.
from generate_figures import (
    PNGCanvas,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE, RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/biomed_figures'


def gen_fig1():
    """Figure 1: Taxonomy of biomedical & pharmacological data sources feeding
    a unified analytics layer."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Sources and Types of Biomedical and", BLACK, 2)
    c.text_c(380, 30, "Pharmacological Data", BLACK, 2)

    # Left column: five source categories
    sources = [
        ("Genomics / Omics", DARK_BLUE, PALE_BLUE),
        ("Clinical / EHR", MED_BLUE, LIGHT_BLUE),
        ("Medical Imaging", PURPLE, LIGHT_PURPLE),
        ("Chemical / HTS", ORANGE, LIGHT_ORANGE),
        ("Real-World / Wearable", DARK_GREEN, LIGHT_GREEN),
    ]
    bx, bw, bh = 30, 190, 46
    src_centers = []
    for i, (label, col, fill) in enumerate(sources):
        by = 70 + i * 74
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        c.text_c(bx + bw // 2, by + bh // 2 - 4, label, BLACK, 1)
        src_centers.append((bx + bw, by + bh // 2))

    # Center hub: integration / data lake
    hub_x1, hub_y1, hub_x2, hub_y2 = 330, 150, 480, 320
    c.rect(hub_x1, hub_y1, hub_x2, hub_y2, GOLD, LIGHT_GOLD)
    c.text_c((hub_x1 + hub_x2) // 2, 200, "Integrated", BLACK, 1)
    c.text_c((hub_x1 + hub_x2) // 2, 218, "Data Layer", BLACK, 1)
    c.text_c((hub_x1 + hub_x2) // 2, 245, "(FAIR,", BLACK, 1)
    c.text_c((hub_x1 + hub_x2) // 2, 263, "harmonized)", BLACK, 1)

    for (sx, sy) in src_centers:
        c.arrow(sx + 2, sy, hub_x1 - 2, (hub_y1 + hub_y2) // 2, GRAY, 2, 7)

    # Right column: data modalities / downstream use
    outputs = [
        ("Structured tables", MED_BLUE, LIGHT_BLUE),
        ("Sequences / text", DARK_GREEN, LIGHT_GREEN),
        ("Images / signals", PURPLE, LIGHT_PURPLE),
        ("Graphs / networks", ORANGE, LIGHT_ORANGE),
    ]
    ox, ow, oh = 560, 180, 46
    for i, (label, col, fill) in enumerate(outputs):
        oy = 90 + i * 74
        c.rect(ox, oy, ox + ow, oy + oh, col, fill)
        c.text_c(ox + ow // 2, oy + oh // 2 - 4, label, BLACK, 1)
        c.arrow(hub_x2 + 2, (hub_y1 + hub_y2) // 2, ox - 2, oy + oh // 2, GRAY, 2, 7)

    c.text(30, 452, "Figure 1: Heterogeneous data sources harmonized into a unified analytics layer.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Data_Sources.png'))
    print("  Figure_1_Data_Sources.png done")


def gen_fig2():
    """Figure 2: End-to-end preprocessing / feature engineering / modeling
    pipeline."""
    c = PNGCanvas(780, 430)
    c.text_c(390, 12, "Preprocessing, Feature Engineering and Model Development", BLACK, 2)

    stages = [
        ("Raw\nData", GRAY, LIGHT_GRAY),
        ("Cleaning\n& QC", MED_BLUE, LIGHT_BLUE),
        ("Normalize\n/ Impute", DARK_BLUE, PALE_BLUE),
        ("Feature\nEng.", ORANGE, LIGHT_ORANGE),
        ("Selection\n/ Reduce", PURPLE, LIGHT_PURPLE),
        ("Model\nTraining", DARK_GREEN, LIGHT_GREEN),
        ("Tuned\nModel", GOLD, LIGHT_GOLD),
    ]
    bw, bh = 86, 60
    gap = 14
    total = len(stages) * bw + (len(stages) - 1) * gap
    start_x = (780 - total) // 2
    y = 90
    centers = []
    for i, (label, col, fill) in enumerate(stages):
        x = start_x + i * (bw + gap)
        c.rect(x, y, x + bw, y + bh, col, fill)
        parts = label.split("\n")
        for li, part in enumerate(parts):
            c.text_c(x + bw // 2, y + bh // 2 - 8 + li * 14, part, BLACK, 1)
        centers.append((x + bw // 2, y + bh // 2, x, x + bw))
        if i > 0:
            prev = centers[i - 1]
            c.arrow(prev[3] + 1, y + bh // 2, x - 1, y + bh // 2, BLACK, 2, 6)

    # Cross-validation feedback loop from Training back to Feature Eng.
    fe = centers[3]
    tr = centers[5]
    loop_y = y + bh + 55
    c.line(tr[0], y + bh, tr[0], loop_y, RED, 2)
    c.line(tr[0], loop_y, fe[0], loop_y, RED, 2)
    c.arrow(fe[0], loop_y, fe[0], y + bh + 1, RED, 2, 6)
    c.text_c((fe[0] + tr[0]) // 2, loop_y + 6, "cross-validation / iterative refinement", RED, 1)

    # Lower panel: example engineered features by modality
    c.text(30, 250, "Representative engineered features by modality:", BLACK, 1)
    rows = [
        ("Omics", "expression ratios, pathway scores, variant burden", DARK_BLUE),
        ("Chemical", "Morgan fingerprints, descriptors, graph embeddings", ORANGE),
        ("Clinical", "aggregates, trends, comorbidity indices", MED_BLUE),
        ("Imaging", "radiomics, CNN embeddings, texture features", PURPLE),
    ]
    ry = 275
    for name, desc, col in rows:
        c.fill_rect(30, ry + 3, 44, ry + 13, col)
        c.text(52, ry, name + ":", BLACK, 1)
        c.text(150, ry, desc, GRAY, 1)
        ry += 26

    c.text(30, 412, "Figure 2: Modeling pipeline from raw data to a validated, tuned model.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Pipeline.png'))
    print("  Figure_2_Pipeline.png done")


def gen_fig3():
    """Figure 3: Model performance comparison (bar chart of AUROC across models
    and tasks)."""
    c = PNGCanvas(760, 450)
    c.text_c(380, 12, "Comparative Model Performance (AUROC)", BLACK, 2)

    # Axes
    ax_x, ax_y0, ax_y1, ax_x1 = 70, 380, 60, 720
    c.vline(ax_x, ax_y1, ax_y0, BLACK)
    c.hline(ax_x, ax_x1, ax_y0, BLACK)
    # Y gridlines / labels 0.5 - 1.0
    for v in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        yy = int(ax_y0 - (v - 0.5) / 0.5 * (ax_y0 - ax_y1))
        c.hline(ax_x, ax_x1, yy, LIGHT_GRAY)
        c.text(34, yy - 4, f"{v:.1f}", BLACK, 1)
    c.vline(ax_x, ax_y1, ax_y0, BLACK)

    # Grouped bars: 4 tasks x 3 models
    tasks = ["Diagnosis", "Toxicity", "DDI", "Readmission"]
    models = [("LogReg", MED_BLUE), ("Grad. Boost", ORANGE), ("Deep NN", DARK_GREEN)]
    data = [
        [0.78, 0.86, 0.90],
        [0.74, 0.83, 0.85],
        [0.71, 0.80, 0.88],
        [0.69, 0.76, 0.79],
    ]
    group_w = (ax_x1 - ax_x - 30) // len(tasks)
    bar_w = group_w // (len(models) + 1)
    for ti, task in enumerate(tasks):
        gx = ax_x + 20 + ti * group_w
        for mi, (mname, col) in enumerate(models):
            val = data[ti][mi]
            bh = int((val - 0.5) / 0.5 * (ax_y0 - ax_y1))
            bx = gx + mi * bar_w
            c.rect(bx, ax_y0 - bh, bx + bar_w - 4, ax_y0, BLACK, col)
            c.text_c(bx + (bar_w - 4) // 2, ax_y0 - bh - 11, f"{val:.2f}", BLACK, 1)
        c.text_c(gx + group_w // 2 - 10, ax_y0 + 8, task, BLACK, 1)

    # Legend
    lx, ly = 520, 70
    for mi, (mname, col) in enumerate(models):
        c.fill_rect(lx, ly + mi * 18, lx + 16, ly + mi * 18 + 12, col)
        c.text(lx + 22, ly + mi * 18, mname, BLACK, 1)

    c.text(30, 432, "Figure 3: AUROC of three model families across four biomedical prediction tasks.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Performance.png'))
    print("  Figure_3_Performance.png done")


def gen_fig4():
    """Figure 4: Validation, explainability and reproducibility framework."""
    c = PNGCanvas(760, 460)
    c.text_c(380, 12, "Validation, Explainability and Reproducibility", BLACK, 2)

    # Three pillars
    pillars = [
        ("VALIDATION", DARK_BLUE, PALE_BLUE,
         ["Internal CV", "External cohort", "Temporal split", "Calibration", "Decision curves"]),
        ("EXPLAINABILITY", ORANGE, LIGHT_ORANGE,
         ["SHAP / LIME", "Attention maps", "Feature import.", "Counterfactuals", "Saliency"]),
        ("REPRODUCIBILITY", DARK_GREEN, LIGHT_GREEN,
         ["Version control", "Seeds / configs", "Data lineage", "Containers", "Reporting stds"]),
    ]
    pw = 220
    gap = 18
    start_x = (760 - (pw * 3 + gap * 2)) // 2
    top = 70
    head_h = 40
    for pi, (title, col, fill, items) in enumerate(pillars):
        x = start_x + pi * (pw + gap)
        c.rect(x, top, x + pw, top + head_h, col, col)
        c.text_c(x + pw // 2, top + head_h // 2 - 4, title, WHITE, 1)
        box_bottom = top + head_h + len(items) * 34 + 12
        c.rect(x, top + head_h, x + pw, box_bottom, col, fill)
        for ii, item in enumerate(items):
            iy = top + head_h + 12 + ii * 34
            c.rect(x + 14, iy, x + pw - 14, iy + 24, col, WHITE)
            c.text_c(x + pw // 2, iy + 8, item, BLACK, 1)

    # Trust banner beneath
    banner_y = 380
    c.rect(start_x, banner_y, start_x + pw * 3 + gap * 2, banner_y + 46, GOLD, LIGHT_GOLD)
    c.text_c(380, banner_y + 12, "Trustworthy, Deployable Clinical / Pharmacological Model", BLACK, 1)
    c.text_c(380, banner_y + 28, "(regulatory-grade evidence + transparency + auditability)", BLACK, 1)

    # arrows from pillars down to banner
    for pi in range(3):
        x = start_x + pi * (pw + gap) + pw // 2
        c.arrow(x, 366, x, banner_y - 1, GRAY, 2, 6)

    c.text(30, 445, "Figure 4: Three pillars underpinning trustworthy biomedical models.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Trust_Framework.png'))
    print("  Figure_4_Trust_Framework.png done")


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating biomedical figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print("All figures generated in", OUTPUT_DIR)
