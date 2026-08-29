#!/usr/bin/env python3
"""
Generate 4 figure images (PNG) for Chapter 5
"Machine Learning for Drug Design".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py
so it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - ML in the structure-based and ligand-based drug design workflow
  Figure 2 - Generative design and optimization loop for novel drug molecules
  Figure 3 - Taxonomy of ML tasks across the drug discovery pipeline
  Figure 4 - Multi-property / ADMET prediction as a filter in the design cycle
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/drug_design_figures'


def gen_fig1():
    """Figure 1: Structure-based and ligand-based drug design workflow."""
    c = PNGCanvas(780, 500)
    c.text_c(390, 10, "Machine Learning in Structure-Based and Ligand-Based Drug Design", BLACK, 2)

    # Start box
    c.rect(300, 45, 480, 90, DARK_BLUE, PALE_BLUE)
    c.text_c(390, 58, "Biological Target", BLACK, 1)
    c.text_c(390, 72, "and Known Ligands", BLACK, 1)

    # Split: structure-based (left) vs ligand-based (right)
    c.arrow(340, 90, 200, 130, GRAY, 2, 9)
    c.arrow(440, 90, 580, 130, GRAY, 2, 9)

    # ---- Structure-based branch (left) ----
    c.rect(60, 135, 340, 170, MED_BLUE, LIGHT_BLUE)
    c.text_c(200, 145, "STRUCTURE-BASED", BLACK, 1)
    c.text_c(200, 158, "3D target structure known", GRAY, 1)

    sb = [
        ("3D Target Structure", "X-ray / cryo-EM / predicted"),
        ("Molecular Docking", "pose sampling + scoring"),
        ("ML Scoring Function", "CNN / GNN affinity model"),
    ]
    y = 185
    for i, (t, s) in enumerate(sb):
        c.rect(60, y, 340, y + 48, DARK_GREEN, LIGHT_GREEN)
        c.text_c(200, y + 12, t, BLACK, 1)
        c.text_c(200, y + 30, s, GRAY, 1)
        if i < len(sb) - 1:
            c.arrow(200, y + 48, 200, y + 62, GRAY, 2, 8)
        y += 62

    # ---- Ligand-based branch (right) ----
    c.rect(440, 135, 720, 170, ORANGE, LIGHT_ORANGE)
    c.text_c(580, 145, "LIGAND-BASED", BLACK, 1)
    c.text_c(580, 158, "no target structure needed", GRAY, 1)

    lb = [
        ("Active Molecules", "measured bioactivity"),
        ("Descriptors / Fingerprints", "representation + QSAR"),
        ("ML Activity Model", "RF / SVM / GNN prediction"),
    ]
    y = 185
    for i, (t, s) in enumerate(lb):
        c.rect(440, y, 720, y + 48, PURPLE, LIGHT_PURPLE)
        c.text_c(580, y + 12, t, BLACK, 1)
        c.text_c(580, y + 30, s, GRAY, 1)
        if i < len(lb) - 1:
            c.arrow(580, y + 48, 580, y + 62, GRAY, 2, 8)
        y += 62

    # Converge into virtual screening / prioritization
    c.rect(250, 385, 530, 435, RED, LIGHT_RED)
    c.text_c(390, 398, "Virtual Screening &", BLACK, 1)
    c.text_c(390, 414, "Hit Prioritization", BLACK, 1)
    c.arrow(200, 371, 300, 385, GRAY, 2, 9)
    c.arrow(580, 371, 480, 385, GRAY, 2, 9)

    # Experimental validation
    c.rect(300, 455, 480, 490, GOLD, LIGHT_GOLD)
    c.text_c(390, 466, "Experimental Validation", BLACK, 1)
    c.arrow(390, 435, 390, 455, GRAY, 2, 8)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Drug_Design_Workflow.png'))
    print("  Figure_1_Drug_Design_Workflow.png done")


def gen_fig2():
    """Figure 2: Generative design and optimization loop."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Generative Design and Optimization Loop", BLACK, 2)

    # Circular loop of 4 stages
    stages = [
        ("Generative Model", "VAE / GAN / Transformer", 300, 60, DARK_GREEN, LIGHT_GREEN),
        ("Property Prediction", "ADMET, affinity, drug-likeness", 540, 200, MED_BLUE, LIGHT_BLUE),
        ("Multi-Objective Scoring", "reward + Pareto trade-offs", 300, 340, ORANGE, LIGHT_ORANGE),
        ("Feedback / Update", "reinforcement, fine-tuning", 60, 200, PURPLE, LIGHT_PURPLE),
    ]
    bw, bh = 200, 62
    centers = []
    for t, s, cx, cy, col, fill in stages:
        c.rect(cx, cy, cx + bw, cy + bh, col, fill)
        c.text_c(cx + bw // 2, cy + 16, t, BLACK, 1)
        c.text_c(cx + bw // 2, cy + 36, s, GRAY, 1)
        centers.append((cx + bw // 2, cy + bh // 2))

    # Clockwise arrows between stage centers (offset from box edges)
    c.arrow(510, 110, 615, 195, GRAY, 2, 9)
    c.arrow(615, 275, 510, 360, GRAY, 2, 9)
    c.arrow(250, 375, 160, 275, GRAY, 2, 9)
    c.arrow(160, 195, 250, 110, GRAY, 2, 9)

    # Central chemical space label
    c.rect(300, 200, 460, 258, GOLD, LIGHT_GOLD)
    c.text_c(380, 214, "Navigating Vast", BLACK, 1)
    c.text_c(380, 230, "Chemical Space", BLACK, 1)
    c.text_c(380, 244, "(~10^60 molecules)", GRAY, 1)

    # Output arrow
    c.rect(280, 415, 480, 455, RED, LIGHT_RED)
    c.text_c(380, 428, "Optimized Candidate Molecules", BLACK, 1)
    c.arrow(400, 402, 400, 415, GRAY, 2, 8)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Generative_Loop.png'))
    print("  Figure_2_Generative_Loop.png done")


def gen_fig3():
    """Figure 3: Taxonomy of ML tasks across the drug discovery pipeline."""
    c = PNGCanvas(820, 470)
    c.text_c(410, 10, "Taxonomy of Machine Learning Tasks Across the Drug Discovery Pipeline", BLACK, 2)

    # Horizontal pipeline stages across the top
    stages = [
        ("Target ID", DARK_BLUE, PALE_BLUE),
        ("Hit Discovery", MED_BLUE, LIGHT_BLUE),
        ("Lead Optimization", DARK_GREEN, LIGHT_GREEN),
        ("Preclinical", ORANGE, LIGHT_ORANGE),
    ]
    sw = 180
    gap = 15
    top = 55
    xs = []
    for i, (t, col, fill) in enumerate(stages):
        x = 20 + i * (sw + gap)
        xs.append(x)
        c.rect(x, top, x + sw, top + 40, col, fill)
        c.text_c(x + sw // 2, top + 15, t, BLACK, 1)
        if i < len(stages) - 1:
            c.arrow(x + sw, top + 20, x + sw + gap, top + 20, GRAY, 2, 7)

    # ML tasks listed under each stage
    tasks = [
        ["Structure", "prediction", "Druggability"],
        ["Virtual", "screening", "Affinity pred."],
        ["QSAR", "Generative", "design", "Synthesis plan"],
        ["ADMET pred.", "Toxicity pred.", "Property pred."],
    ]
    task_cols = [MED_GREEN, PURPLE, RED, GOLD]
    task_fills = [LIGHT_GREEN, LIGHT_PURPLE, LIGHT_RED, LIGHT_GOLD]
    for i, x in enumerate(xs):
        c.arrow(x + sw // 2, top + 40, x + sw // 2, top + 62, GRAY, 2, 7)
        ty = top + 65
        items = tasks[i]
        # group them into one box with lines
        box_h = 22 * len(items) + 16
        c.rect(x, ty, x + sw, ty + box_h, task_cols[i], task_fills[i])
        for j, it in enumerate(items):
            c.text_c(x + sw // 2, ty + 14 + j * 22, it, BLACK, 1)

    # Cross-cutting foundations bar at bottom
    c.rect(20, 360, 800, 405, DARK_BLUE, PALE_BLUE)
    c.text_c(410, 372, "Cross-Cutting Foundations", BLACK, 1)
    c.text_c(410, 390, "Molecular representations  |  Curated data  |  Validation & applicability domain", GRAY, 1)

    # Learning-paradigm bar
    c.rect(20, 415, 800, 458, DARK_GREEN, LIGHT_GREEN)
    c.text_c(410, 427, "Learning Paradigms", BLACK, 1)
    c.text_c(410, 445, "Supervised  |  Self-supervised pretraining  |  Reinforcement  |  Generative", GRAY, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_ML_Task_Taxonomy.png'))
    print("  Figure_3_ML_Task_Taxonomy.png done")


def gen_fig4():
    """Figure 4: Multi-property / ADMET prediction as a filter in the design cycle."""
    c = PNGCanvas(780, 470)
    c.text_c(390, 10, "Multi-Property and ADMET Prediction as a Design-Cycle Filter", BLACK, 2)

    # Left: large pool of generated candidates
    c.rect(40, 90, 210, 330, MED_BLUE, LIGHT_BLUE)
    c.text_c(125, 105, "Generated /", BLACK, 1)
    c.text_c(125, 120, "Screened Candidates", BLACK, 1)
    c.text_c(125, 145, "(thousands to millions)", GRAY, 1)
    # dots to suggest many molecules
    for r in range(6):
        for col in range(5):
            c.circle(70 + col * 25, 175 + r * 22, 6, DARK_BLUE, PALE_BLUE)

    # Middle: stacked filter of property predictors
    filters = [
        ("Drug-Likeness", GOLD, LIGHT_GOLD),
        ("Absorption / Permeability", DARK_GREEN, LIGHT_GREEN),
        ("Metabolism (P450)", ORANGE, LIGHT_ORANGE),
        ("Toxicity (hERG, hepatic)", RED, LIGHT_RED),
    ]
    fx1, fx2 = 260, 520
    y = 90
    for i, (t, col, fill) in enumerate(filters):
        c.rect(fx1, y, fx2, y + 52, col, fill)
        c.text_c((fx1 + fx2) // 2, y + 20, t, BLACK, 1)
        c.text_c((fx1 + fx2) // 2, y + 36, "ML predictor / filter", GRAY, 1)
        if i < len(filters) - 1:
            c.arrow((fx1 + fx2) // 2, y + 52, (fx1 + fx2) // 2, y + 60, GRAY, 2, 7)
        y += 60

    c.arrow(210, 210, fx1 - 4, 116, GRAY, 2, 9)
    c.text(212, 150, "predict", GRAY, 1)

    # Right: small set of prioritized molecules
    c.rect(570, 150, 740, 270, DARK_GREEN, LIGHT_GREEN)
    c.text_c(655, 165, "Prioritized", BLACK, 1)
    c.text_c(655, 180, "Candidates", BLACK, 1)
    for col in range(3):
        c.circle(615 + col * 30, 225, 8, DARK_GREEN, PALE_BLUE)
    c.arrow(fx2 + 4, 210, 570 - 4, 210, GRAY, 2, 9)
    c.text(524, 190, "pass", DARK_GREEN, 1)

    # Down to synthesis & testing
    c.rect(570, 300, 740, 350, PURPLE, LIGHT_PURPLE)
    c.text_c(655, 312, "Synthesis &", BLACK, 1)
    c.text_c(655, 328, "Experimental Testing", BLACK, 1)
    c.arrow(655, 270, 655, 300, GRAY, 2, 8)

    # Feedback loop back to candidate generation
    c.line(655, 350, 655, 400, GRAY, 1)
    c.line(655, 400, 125, 400, GRAY, 1)
    c.arrow(125, 400, 125, 330, GRAY, 2, 8)
    c.text(300, 405, "feedback: refine generation and models", GRAY, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_ADMET_Filter.png'))
    print("  Figure_4_ADMET_Filter.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating drug-design chapter figures...")
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
