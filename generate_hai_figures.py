#!/usr/bin/env python3
"""
Generate 4 figures (PNG) for the book chapter
"Explainable and Federated Artificial Intelligence for Secure Clinical
Decision Support in Next-Generation Healthcare Systems".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py
so it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - Conceptual convergence framework: Secure + Explainable +
             Federated AI for clinical decision support (CDS).
  Figure 2 - Federated learning workflow across multiple hospitals with
             privacy-preserving aggregation.
  Figure 3 - Taxonomy of explainability methods for clinical decision support.
  Figure 4 - Comparative assessment of privacy-preserving techniques across
             privacy strength, model utility and system overhead.
"""

import os

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

OUTPUT_DIR = '/projects/sandbox/AMMAN/healthcare_figures'


# ---------------------------------------------------------------------------
# Figure 1 - Conceptual convergence framework
# ---------------------------------------------------------------------------
def gen_fig1():
    c = PNGCanvas(920, 620)
    c.text_c(460, 14, "Secure Explainable and Federated AI for Clinical Decision Support",
             BLACK, 2)

    # Data layer: distributed hospital sites
    c.text(30, 60, "Distributed Clinical Data Sources", DARK_BLUE, 1)
    sites = ["Hospital A", "Hospital B", "Clinic C", "Lab D"]
    for i, s in enumerate(sites):
        bx = 30 + i * 150
        c.rect(bx, 80, bx + 130, 130, DARK_BLUE, PALE_BLUE)
        c.text_c(bx + 65, 92, s, BLACK, 1)
        c.text_c(bx + 65, 108, "EHR / Imaging", GRAY, 1)
        c.arrow(bx + 65, 132, bx + 65, 168, GRAY, 2, 8)

    # Three technology pillars
    pillars = [
        ("Federated Learning", MED_BLUE, LIGHT_BLUE,
         ["Local training", "No raw data", "sharing", "Model updates"]),
        ("Explainable AI", MED_GREEN, LIGHT_GREEN,
         ["Feature attribution", "Saliency maps", "Interpretable", "surrogates"]),
        ("Security and Privacy", ORANGE, LIGHT_ORANGE,
         ["Differential privacy", "Secure aggregation", "Encryption", "Access control"]),
    ]
    pw, ph = 250, 130
    top = 175
    for i, (title, col, fill, items) in enumerate(pillars):
        bx = 40 + i * 280
        c.rect(bx, top, bx + pw, top + ph, col, fill)
        c.text_c(bx + pw // 2, top + 12, title, BLACK, 1)
        for j, it in enumerate(items):
            c.text_c(bx + pw // 2, top + 40 + j * 18, it, BLACK, 1)
        # arrows down to fusion bar
        c.arrow(bx + pw // 2, top + ph + 2, bx + pw // 2, top + ph + 38, GRAY, 2, 8)

    # Trust and governance fusion bar
    fy = top + ph + 40
    c.rect(60, fy, 860, fy + 46, PURPLE, LIGHT_PURPLE)
    c.text_c(460, fy + 10, "Trustworthy AI Orchestration Layer", BLACK, 1)
    c.text_c(460, fy + 27, "Privacy preserving training  plus  transparent reasoning  plus  auditability",
             BLACK, 1)
    c.arrow(460, fy + 48, 460, fy + 82, GRAY, 3, 10)

    # Clinical decision support output
    cy = fy + 84
    c.rect(250, cy, 670, cy + 70, DARK_GREEN, LIGHT_GREEN)
    c.text_c(460, cy + 14, "Secure Clinical Decision Support", BLACK, 2)
    c.text_c(460, cy + 40, "Diagnosis  -  Risk prediction  -  Treatment guidance", BLACK, 1)
    c.text_c(460, cy + 54, "with human interpretable evidence", BLACK, 1)

    # Clinician
    c.arrow(670, cy + 35, 770, cy + 35, GRAY, 2, 8)
    c.rect(772, cy + 8, 892, cy + 62, MED_BLUE, PALE_BLUE)
    c.text_c(832, cy + 26, "Clinician", BLACK, 1)
    c.text_c(832, cy + 42, "in the loop", BLACK, 1)

    c.text(30, 600, "Figure 1: Convergence of federated learning, explainable AI and "
                    "privacy technologies for clinical decision support.", GRAY, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure-1-Convergence-Framework.png'))
    print("  Figure_1 done")


# ---------------------------------------------------------------------------
# Figure 2 - Federated learning workflow across hospitals
# ---------------------------------------------------------------------------
def gen_fig2():
    c = PNGCanvas(900, 640)
    c.text_c(450, 14, "Privacy Preserving Federated Learning Across Hospitals", BLACK, 2)

    # Central aggregation server
    sx, sy = 450, 300
    c.circle(sx, sy, 74, DARK_BLUE, PALE_BLUE)
    c.text_c(sx, sy - 26, "Global", BLACK, 1)
    c.text_c(sx, sy - 12, "Aggregation", BLACK, 1)
    c.text_c(sx, sy + 4, "Server", BLACK, 1)
    c.text_c(sx, sy + 22, "Secure", GRAY, 1)
    c.text_c(sx, sy + 36, "aggregation", GRAY, 1)

    # Hospital clients around the server
    clients = [
        ("Hospital 1", 160, 150),
        ("Hospital 2", 740, 150),
        ("Hospital 3", 160, 470),
        ("Hospital 4", 740, 470),
    ]
    for name, cx, cy in clients:
        c.rect(cx - 85, cy - 45, cx + 85, cy + 45, MED_GREEN, LIGHT_GREEN)
        c.text_c(cx, cy - 30, name, BLACK, 1)
        c.text_c(cx, cy - 12, "Local model", BLACK, 1)
        c.text_c(cx, cy + 4, "training on", GRAY, 1)
        c.text_c(cx, cy + 18, "private data", GRAY, 1)
        # upload encrypted updates
        c.arrow(cx + (60 if cx < sx else -60), cy + (30 if cy < sy else -30),
                sx + (-60 if cx < sx else 60), sy + (-40 if cy < sy else 40),
                ORANGE, 2, 9)
        # download global model
        c.arrow(sx + (-70 if cx < sx else 70), sy + (-30 if cy < sy else 30),
                cx + (50 if cx < sx else -50), cy + (40 if cy < sy else -40),
                MED_BLUE, 2, 9)

    # Legend
    c.rect(360, 560, 540, 585, ORANGE, LIGHT_ORANGE)
    c.text(368, 568, "Encrypted model updates up", BLACK, 1)
    c.rect(360, 590, 540, 615, MED_BLUE, PALE_BLUE)
    c.text(368, 598, "Global model download down", BLACK, 1)

    # Privacy mechanisms box
    c.rect(690, 545, 890, 632, PURPLE, LIGHT_PURPLE)
    c.text_c(790, 552, "Privacy Mechanisms", BLACK, 1)
    for j, it in enumerate(["Differential privacy", "Secure aggregation",
                            "Homomorphic encryption", "Secure multiparty comp."]):
        c.text_c(790, 570 + j * 14, it, BLACK, 1)

    # Round annotation
    c.rect(10, 545, 340, 632, GRAY, (245, 245, 245))
    c.text(18, 552, "Communication round:", BLACK, 1)
    c.text(18, 570, "1 broadcast global model", GRAY, 1)
    c.text(18, 584, "2 train locally on site data", GRAY, 1)
    c.text(18, 598, "3 send protected updates", GRAY, 1)
    c.text(18, 612, "4 aggregate into new model", GRAY, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure-2-Federated-Workflow.png'))
    print("  Figure_2 done")


# ---------------------------------------------------------------------------
# Figure 3 - Taxonomy of explainability methods
# ---------------------------------------------------------------------------
def gen_fig3():
    c = PNGCanvas(920, 560)
    c.text_c(460, 14, "Taxonomy of Explainability Methods for Clinical Decision Support",
             BLACK, 2)

    # Root
    c.rect(360, 50, 560, 90, DARK_BLUE, PALE_BLUE)
    c.text_c(460, 62, "Explainable AI", BLACK, 1)
    c.text_c(460, 76, "for Healthcare", BLACK, 1)

    # Two main branches
    c.arrow(460, 92, 230, 138, GRAY, 2, 8)
    c.arrow(460, 92, 690, 138, GRAY, 2, 8)

    c.rect(90, 140, 370, 190, MED_GREEN, LIGHT_GREEN)
    c.text_c(230, 152, "Ante-hoc / Intrinsic", BLACK, 1)
    c.text_c(230, 170, "Transparent by design", GRAY, 1)

    c.rect(550, 140, 830, 190, ORANGE, LIGHT_ORANGE)
    c.text_c(690, 152, "Post-hoc", BLACK, 1)
    c.text_c(690, 170, "Explain trained black box", GRAY, 1)

    # Ante-hoc leaves
    ante = ["Decision trees", "Rule based models", "Linear / logistic", "Attention models",
            "Generalized additive"]
    for i, a in enumerate(ante):
        by = 210 + i * 46
        c.rect(120, by, 340, by + 36, MED_GREEN, WHITE)
        c.text_c(230, by + 12, a, BLACK, 1)
        c.arrow(230, (192 if i == 0 else by - 10), 230, by - 2, LIGHT_GRAY, 1, 6)

    # Post-hoc split into model-agnostic and model-specific
    c.arrow(690, 192, 560, 232, GRAY, 2, 8)
    c.arrow(690, 192, 820, 232, GRAY, 2, 8)

    c.rect(440, 234, 660, 274, MED_BLUE, LIGHT_BLUE)
    c.text_c(550, 246, "Model agnostic", BLACK, 1)
    c.text_c(550, 262, "LIME  -  SHAP", BLACK, 1)

    c.rect(710, 234, 900, 274, PURPLE, LIGHT_PURPLE)
    c.text_c(805, 246, "Model specific", BLACK, 1)
    c.text_c(805, 262, "Grad-CAM  -  Saliency", BLACK, 1)

    # scope leaves under each
    ag = ["Local: single patient", "Global: cohort level", "Counterfactuals"]
    for i, a in enumerate(ag):
        by = 292 + i * 44
        c.rect(450, by, 660, by + 34, MED_BLUE, WHITE)
        c.text_c(555, by + 11, a, BLACK, 1)
    sp = ["Saliency maps", "Feature maps", "Layer relevance"]
    for i, a in enumerate(sp):
        by = 292 + i * 44
        c.rect(705, by, 900, by + 34, PURPLE, WHITE)
        c.text_c(802, by + 11, a, BLACK, 1)

    # Evaluation footer
    c.rect(90, 470, 830, 520, GOLD, LIGHT_GOLD)
    c.text_c(460, 482, "Clinical evaluation of explanations", BLACK, 1)
    c.text_c(460, 500, "Fidelity  -  Stability  -  Comprehensibility  -  Clinician trust", BLACK, 1)

    c.text(30, 540, "Figure 3: Ante-hoc and post-hoc explainability techniques and their "
                    "clinical evaluation criteria.", GRAY, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure-3-XAI-Taxonomy.png'))
    print("  Figure_3 done")


# ---------------------------------------------------------------------------
# Figure 4 - Comparative assessment of privacy-preserving techniques
# ---------------------------------------------------------------------------
def gen_fig4():
    c = PNGCanvas(900, 560)
    c.text_c(450, 14, "Comparative Assessment of Privacy Preserving Techniques", BLACK, 2)

    # Grouped bar chart: 4 techniques x 3 metrics (scores 0-10)
    techniques = ["Diff.\nPrivacy", "Secure\nAggreg.", "Homomorph.\nEncrypt.", "Secure\nMPC"]
    # metric scores: [privacy strength, model utility, low overhead]
    scores = {
        "Privacy strength": [8, 6, 9, 9],
        "Model utility":    [6, 9, 8, 7],
        "Low overhead":     [9, 7, 3, 4],
    }
    metric_colors = [MED_BLUE, MED_GREEN, ORANGE]
    metric_names = list(scores.keys())

    # Axes
    ax0x, ax0y = 90, 430
    axtop = 80
    c.vline(ax0x, axtop, ax0y, BLACK)
    c.hline(ax0x, 830, ax0y, BLACK)
    # y ticks 0..10
    for v in range(0, 11, 2):
        yy = ax0y - int(v / 10 * (ax0y - axtop))
        c.hline(ax0x - 5, ax0x, yy, BLACK)
        c.text(ax0x - 30, yy - 3, str(v), BLACK, 1)
    c.text(30, axtop - 20, "Score (0 to 10, higher is better)", GRAY, 1)

    group_w = 170
    bar_w = 44
    for gi, tech in enumerate(techniques):
        gx = ax0x + 30 + gi * group_w
        for mi, m in enumerate(metric_names):
            val = scores[m][gi]
            bh = int(val / 10 * (ax0y - axtop))
            bx = gx + mi * (bar_w + 4)
            c.rect(bx, ax0y - bh, bx + bar_w, ax0y, BLACK, metric_colors[mi])
            c.text_c(bx + bar_w // 2, ax0y - bh - 12, str(val), BLACK, 1)
        # technique label (two lines split on \n)
        for li, part in enumerate(tech.split("\n")):
            c.text_c(gx + group_w // 2 - 25, ax0y + 12 + li * 13, part, BLACK, 1)

    # Legend
    lx, ly = 560, 90
    for mi, m in enumerate(metric_names):
        c.rect(lx, ly + mi * 22, lx + 18, ly + mi * 22 + 14, BLACK, metric_colors[mi])
        c.text(lx + 26, ly + mi * 22 + 2, m, BLACK, 1)

    c.text(30, 540, "Figure 4: Qualitative trade-offs among privacy preserving mechanisms "
                    "for federated clinical models.", GRAY, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure-4-Privacy-Tradeoffs.png'))
    print("  Figure_4 done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating healthcare AI chapter figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print("All figures written to", OUTPUT_DIR)


if __name__ == '__main__':
    main()
