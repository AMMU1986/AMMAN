#!/usr/bin/env python3
"""
Generate 4 scientific figures (PNG) for Chapter 14:
AI in Pharmacogenomics and Precision Medicine.

Reuses the pure-stdlib PNGCanvas from generate_figures.py so no
third-party libraries are required in the sandbox.
"""

import os
import math

# Reuse the canvas + color palette from the existing figure generator.
from generate_figures import (
    PNGCanvas,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE, RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/chapter14_figures'


def gen_fig1():
    """Figure 1: Pharmacogenomic pathway from gene to drug response."""
    c = PNGCanvas(720, 460)
    c.text_c(360, 10, "Pharmacogenomic Pathway: Gene to Drug Response", BLACK, 2)

    # Top: genetic variation source
    c.rect(260, 45, 460, 90, DARK_BLUE, PALE_BLUE)
    c.text_c(360, 55, "Genetic Variation", BLACK, 1)
    c.text_c(360, 70, "(SNPs, CNVs, indels)", GRAY, 1)

    # Two branches: PK and PD
    c.arrow(320, 90, 200, 130, GRAY, 2, 8)
    c.arrow(400, 90, 520, 130, GRAY, 2, 8)

    # PK branch
    c.rect(60, 135, 300, 175, MED_BLUE, LIGHT_BLUE)
    c.text_c(180, 145, "Pharmacokinetics (PK)", BLACK, 1)
    c.text_c(180, 160, "What body does to drug", GRAY, 1)
    pk_boxes = [
        ("Metabolizing", "Enzymes (CYP)", 60),
        ("Drug", "Transporters", 175),
    ]
    for t1, t2, bx in pk_boxes:
        c.rect(bx, 190, bx+110, 235, DARK_GREEN, LIGHT_GREEN)
        c.text_c(bx+55, 200, t1, BLACK, 1)
        c.text_c(bx+55, 215, t2, BLACK, 1)
    c.arrow(150, 175, 115, 190, GRAY, 2, 6)
    c.arrow(210, 175, 230, 190, GRAY, 2, 6)

    # PD branch
    c.rect(420, 135, 660, 175, PURPLE, LIGHT_PURPLE)
    c.text_c(540, 145, "Pharmacodynamics (PD)", BLACK, 1)
    c.text_c(540, 160, "What drug does to body", GRAY, 1)
    pd_boxes = [
        ("Receptors &", "Targets", 420),
        ("Immune", "(HLA)", 545),
    ]
    for t1, t2, bx in pd_boxes:
        c.rect(bx, 190, bx+105, 235, ORANGE, LIGHT_ORANGE)
        c.text_c(bx+52, 200, t1, BLACK, 1)
        c.text_c(bx+52, 215, t2, BLACK, 1)
    c.arrow(500, 175, 475, 190, GRAY, 2, 6)
    c.arrow(575, 175, 595, 190, GRAY, 2, 6)

    # Modifiers box (nongenetic)
    c.rect(280, 255, 440, 320, GOLD, LIGHT_GOLD)
    c.text_c(360, 263, "Nongenetic Factors", BLACK, 1)
    c.text(295, 280, "- Age / organ function", GRAY, 1)
    c.text(295, 295, "- Drug interactions", GRAY, 1)
    c.text(295, 310, "- Diet / environment", GRAY, 1)

    # Converge to drug exposure & effect
    c.arrow(180, 235, 320, 335, MED_BLUE, 2, 8)
    c.arrow(540, 235, 400, 335, PURPLE, 2, 8)
    c.arrow(360, 320, 360, 340, GOLD, 2, 8)

    # Clinical outcome
    c.rect(240, 345, 480, 400, RED, LIGHT_RED)
    c.text_c(360, 356, "Clinical Drug Response", BLACK, 2)
    c.text_c(360, 380, "Efficacy | Toxicity | Dose need", BLACK, 1)

    # Phenotype spectrum bar
    c.text(60, 355, "Phenotype", BLACK, 1)
    labels = ["Poor", "Interm", "Normal", "Rapid", "Ultra"]
    cols = [RED, ORANGE, MED_GREEN, MED_BLUE, PURPLE]
    for i, (lb, cl) in enumerate(zip(labels, cols)):
        c.fill_rect(50+i*30, 372, 78+i*30, 388, cl)
    c.text(50, 392, "PM ......... UM", GRAY, 1)

    c.text(50, 435, "Figure 1: From genetic variation to individual drug response.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Pharmacogenomic_Pathway.png'))
    print("  Figure_1_Pharmacogenomic_Pathway.png done")


def gen_fig2():
    """Figure 2: Machine learning pipeline for pharmacogenomic prediction."""
    c = PNGCanvas(760, 440)
    c.text_c(380, 10, "Machine Learning Pipeline for Pharmacogenomic Prediction", BLACK, 2)

    # Stage boxes left-to-right
    stages = [
        ("Data\nSources", 30, DARK_BLUE, PALE_BLUE),
        ("Feature\nEngineering", 175, MED_BLUE, LIGHT_BLUE),
        ("Model\nTraining", 320, DARK_GREEN, LIGHT_GREEN),
        ("Validation", 465, ORANGE, LIGHT_ORANGE),
        ("Deployment", 610, RED, LIGHT_RED),
    ]
    bw, bh = 120, 60
    by = 70
    centers = []
    for label, bx, col, fill in stages:
        c.rect(bx, by, bx+bw, by+bh, col, fill)
        lines = label.split("\n")
        for li, ln in enumerate(lines):
            c.text_c(bx+bw//2, by+bh//2-8+li*14, ln, BLACK, 1)
        centers.append((bx+bw//2, by+bh//2))
    for i in range(len(centers)-1):
        x1 = centers[i][0]+bw//2
        x2 = centers[i+1][0]-bw//2
        c.arrow(x1, by+bh//2, x2, by+bh//2, GRAY, 2, 8)

    # Detail under each stage
    details = [
        (30, ["Genome / SNPs", "Multi-omics", "EHR + labs", "Wearables"]),
        (175, ["Genotype->", " phenotype", "Polygenic scores", "Selection"]),
        (320, ["Regression", "Tree ensembles", "Deep networks", "GNN / SVM"]),
        (465, ["Cross-val", "External cohort", "Calibration", "Subgroups"]),
        (610, ["EHR alerts", "Point of care", "Monitoring", "Feedback"]),
    ]
    for bx, items in details:
        c.rect(bx, 150, bx+120, 250, LIGHT_GRAY, (248, 248, 248))
        for j, it in enumerate(items):
            c.text(bx+6, 158+j*20, it, GRAY, 1)

    # Feedback loop from deployment back to data
    c.line(670, 250, 670, 300, RED, 2)
    c.line(670, 300, 90, 300, RED, 2)
    c.arrow(90, 300, 90, 250, RED, 2, 8)
    c.text_c(380, 305, "Continuous learning feedback loop", RED, 1)

    # Metrics band
    c.rect(30, 330, 700, 400, DARK_BLUE, PALE_BLUE)
    c.text(45, 338, "Evaluation Metrics:", BLACK, 1)
    c.text(45, 358, "Classification: AUROC, sensitivity, specificity, calibration", MED_BLUE, 1)
    c.text(45, 378, "Regression: RMSE, MAE, R-squared, prediction interval coverage", DARK_GREEN, 1)

    c.text(50, 420, "Figure 2: End-to-end ML pipeline for pharmacogenomic prediction.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_ML_Pipeline.png'))
    print("  Figure_2_ML_Pipeline.png done")


def gen_fig3():
    """Figure 3: AI clinical decision support architecture."""
    c = PNGCanvas(740, 470)
    c.text_c(370, 10, "AI Clinical Decision Support for Personalized Prescribing", BLACK, 2)

    # Input data layer (left)
    c.text(20, 40, "Data Inputs", BLACK, 1)
    inputs = [
        ("Genomic Panel", DARK_BLUE, LIGHT_BLUE),
        ("EHR / History", MED_BLUE, LIGHT_BLUE),
        ("Lab Values", DARK_GREEN, LIGHT_GREEN),
        ("Concomitant Rx", PURPLE, LIGHT_PURPLE),
        ("Wearable Data", ORANGE, LIGHT_ORANGE),
    ]
    for i, (lb, col, fill) in enumerate(inputs):
        y = 60 + i*55
        c.rect(20, y, 170, y+42, col, fill)
        c.text_c(95, y+16, lb, BLACK, 1)
        c.arrow(170, y+21, 235, 190, GRAY, 1, 6)

    # AI engine (center)
    c.rect(235, 120, 470, 300, DARK_GREEN, LIGHT_GREEN)
    c.text_c(352, 132, "AI PREDICTIVE ENGINE", BLACK, 2)
    c.rect(255, 160, 450, 195, MED_BLUE, LIGHT_BLUE)
    c.text_c(352, 170, "Genotype-to-phenotype translation", BLACK, 1)
    c.rect(255, 205, 450, 240, ORANGE, LIGHT_ORANGE)
    c.text_c(352, 215, "Response + toxicity prediction", BLACK, 1)
    c.rect(255, 250, 450, 285, PURPLE, LIGHT_PURPLE)
    c.text_c(352, 260, "PK/PD dose optimization", BLACK, 1)

    # Output (right)
    c.arrow(470, 210, 540, 210, BLACK, 2, 8)
    c.rect(540, 120, 720, 300, RED, LIGHT_RED)
    c.text_c(630, 132, "RECOMMENDATION", BLACK, 1)
    c.text(555, 160, "Drug selection", BLACK, 1)
    c.text(555, 185, "Optimal dose", BLACK, 1)
    c.text(555, 210, "Monitoring plan", BLACK, 1)
    c.text(555, 235, "Alerts + rationale", BLACK, 1)
    c.text(555, 265, "Uncertainty est.", GRAY, 1)

    # Point of care / clinician
    c.rect(540, 330, 720, 385, GOLD, LIGHT_GOLD)
    c.text_c(630, 342, "Clinician at", BLACK, 1)
    c.text_c(630, 358, "Point of Care", BLACK, 1)
    c.text_c(630, 373, "(human-in-loop)", GRAY, 1)
    c.arrow(630, 300, 630, 330, RED, 2, 8)

    # Outcome + feedback loop
    c.rect(235, 330, 460, 385, DARK_BLUE, PALE_BLUE)
    c.text_c(347, 345, "Observed Outcome", BLACK, 1)
    c.text_c(347, 363, "(efficacy / safety)", GRAY, 1)
    c.arrow(540, 360, 460, 360, GRAY, 2, 8)
    c.line(235, 358, 100, 358, RED, 2)
    c.line(100, 358, 100, 300, RED, 2)
    c.arrow(100, 300, 95, 172, RED, 2, 8)
    c.text(105, 320, "Feedback", RED, 1)

    c.text(50, 440, "Figure 3: Integrated AI decision support architecture for prescribing.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Clinical_Decision_Support.png'))
    print("  Figure_3_Clinical_Decision_Support.png done")


def gen_fig4():
    """Figure 4: Barriers to and enablers of clinical adoption."""
    c = PNGCanvas(740, 470)
    c.text_c(370, 10, "Barriers and Enablers of AI Pharmacogenomics Adoption", BLACK, 2)

    dims = ["Data", "Technical", "Clinical", "Regulatory"]
    barriers = [
        ["Siloed formats", "Scarce labels", "Low diversity"],
        ["Overfitting risk", "Poor interpret.", "Compute needs"],
        ["Alert fatigue", "Workflow fit", "Clinician trust"],
        ["Liability", "Evolving rules", "Model drift"],
    ]
    enablers = [
        ["Biobanks", "Standards", "Federated data"],
        ["Explainable AI", "Transfer learn", "Ensembles"],
        ["Preemptive test", "Point-of-care", "Education"],
        ["Governance", "Monitoring", "Validation"],
    ]

    col_w = 165
    x0 = 25
    # Header labels
    c.text_c(190, 42, "BARRIERS", RED, 2)
    c.text_c(190, 62, "(challenges to overcome)", GRAY, 1)
    c.text_c(555, 42, "ENABLERS", DARK_GREEN, 2)
    c.text_c(555, 62, "(accelerators of adoption)", GRAY, 1)

    for i, dim in enumerate(dims):
        y = 85 + i*90
        # Dimension label
        c.rect(x0, y, x0+80, y+75, DARK_BLUE, PALE_BLUE)
        c.text_c(x0+40, y+32, dim, BLACK, 1)

        # Barriers block
        bx = x0 + 90
        c.rect(bx, y, bx+col_w, y+75, RED, LIGHT_RED)
        for j, item in enumerate(barriers[i]):
            c.text(bx+8, y+12+j*20, "- " + item, BLACK, 1)

        # Arrow barrier -> enabler
        c.arrow(bx+col_w+2, y+37, bx+col_w+55, y+37, GRAY, 2, 8)

        # Enablers block
        ex = bx + col_w + 60
        c.rect(ex, y, ex+col_w, y+75, DARK_GREEN, LIGHT_GREEN)
        for j, item in enumerate(enablers[i]):
            c.text(ex+8, y+12+j*20, "+ " + item, BLACK, 1)

    c.text(50, 450, "Figure 4: Barriers and enablers across data, technical, clinical, regulatory dimensions.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Barriers_Enablers.png'))
    print("  Figure_4_Barriers_Enablers.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Chapter 14 figures...")
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
