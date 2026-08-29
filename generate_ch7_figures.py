#!/usr/bin/env python3
"""
Generate 4 scientific figure images (PNG) for Chapter 7:
AI in Drug Toxicology and Safety.
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/ch7_figures'


def fig1_multimodal_tox():
    """Figure 7.1: Multi-modal toxicity prediction framework."""
    c = PNGCanvas(760, 480)
    c.text_c(380, 10, "Multi-Modal Toxicity Prediction Framework", BLACK, 2)

    # Input modality boxes (left)
    c.rect(25, 70, 200, 130, MED_BLUE, LIGHT_BLUE)
    c.text_c(112, 82, "Chemical Structure", BLACK, 1)
    c.text(35, 100, "- Fingerprints", GRAY, 1)
    c.text(35, 115, "- Molecular graphs", GRAY, 1)

    c.rect(25, 150, 200, 230, DARK_GREEN, LIGHT_GREEN)
    c.text_c(112, 162, "Biological Readouts", BLACK, 1)
    c.text(35, 180, "- Gene expression", GRAY, 1)
    c.text(35, 195, "- High-content imaging", GRAY, 1)
    c.text(35, 210, "- Bioassay panels", GRAY, 1)

    c.rect(25, 250, 200, 320, PURPLE, LIGHT_PURPLE)
    c.text_c(112, 262, "Physicochemical", BLACK, 1)
    c.text(35, 280, "- logP, PSA, MW", GRAY, 1)
    c.text(35, 295, "- Reactivity descriptors", GRAY, 1)

    # Fusion / model (center)
    c.rect(270, 140, 460, 260, DARK_BLUE, PALE_BLUE)
    c.text_c(365, 155, "ML MODEL", BLACK, 2)
    c.text_c(365, 185, "Feature fusion", BLACK, 1)
    c.text_c(365, 205, "Multitask learning", BLACK, 1)
    c.text_c(365, 225, "+ uncertainty", GRAY, 1)

    # arrows to model
    for y in [100, 190, 285]:
        c.arrow(200, y, 270, 200, GRAY, 2, 7)

    # Output endpoints (right)
    endpoints = [("Hepatotoxicity", 90, LIGHT_RED, RED),
                 ("Cardiotoxicity", 140, LIGHT_ORANGE, ORANGE),
                 ("Mutagenicity", 190, LIGHT_GOLD, GOLD),
                 ("Nephrotoxicity", 240, LIGHT_GREEN, DARK_GREEN),
                 ("Immunotoxicity", 290, LIGHT_PURPLE, PURPLE)]
    for label, y, fill, outline in endpoints:
        c.rect(540, y, 720, y + 40, outline, fill)
        c.text_c(630, y + 14, label, BLACK, 1)
        c.arrow(460, 200, 540, y + 20, GRAY, 1, 6)

    # Applicability domain / uncertainty note
    c.rect(270, 285, 460, 345, GOLD, LIGHT_GOLD)
    c.text_c(365, 298, "Applicability domain check", BLACK, 1)
    c.text_c(365, 318, "flag out-of-domain inputs", GRAY, 1)

    c.text(40, 455, "Figure 7.1: Multi-modal framework integrating chemical and biological data", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_7_1_Multimodal_Toxicity.png'))
    print("  Figure_7_1_Multimodal_Toxicity.png done")


def fig2_ddi_mechanisms():
    """Figure 7.2: DDI mechanistic categories and prediction strategies."""
    c = PNGCanvas(760, 480)
    c.text_c(380, 10, "Drug-Drug Interaction Mechanisms and Prediction", BLACK, 2)

    # Two drugs at top
    c.circle(180, 70, 26, DARK_BLUE, LIGHT_BLUE)
    c.text_c(180, 66, "Drug A", BLACK, 1)
    c.circle(560, 70, 26, DARK_GREEN, LIGHT_GREEN)
    c.text_c(560, 66, "Drug B", BLACK, 1)
    c.text_c(370, 65, "+", BLACK, 2)

    # PK branch (left)
    c.rect(40, 130, 360, 300, MED_BLUE, (238, 244, 252))
    c.text_c(200, 142, "Pharmacokinetic (PK)", BLACK, 1)
    c.text(55, 165, "One drug alters ADME of the other", GRAY, 1)
    c.rect(60, 185, 200, 220, GRAY, LIGHT_GRAY)
    c.text_c(130, 197, "Enzyme inhibition", BLACK, 1)
    c.rect(210, 185, 340, 220, GRAY, LIGHT_GRAY)
    c.text_c(275, 197, "Transporters", BLACK, 1)
    c.rect(60, 235, 340, 285, ORANGE, LIGHT_ORANGE)
    c.text_c(200, 248, "Predict from:", BLACK, 1)
    c.text_c(200, 265, "metabolism / enzyme profiles", GRAY, 1)

    # PD branch (right)
    c.rect(400, 130, 720, 300, DARK_GREEN, (240, 250, 240))
    c.text_c(560, 142, "Pharmacodynamic (PD)", BLACK, 1)
    c.text(415, 165, "Combined effect on shared pathway", GRAY, 1)
    c.rect(420, 185, 560, 220, GRAY, LIGHT_GRAY)
    c.text_c(490, 197, "Additive / synergy", BLACK, 1)
    c.rect(570, 185, 700, 220, GRAY, LIGHT_GRAY)
    c.text_c(635, 197, "Antagonism", BLACK, 1)
    c.rect(420, 235, 700, 285, PURPLE, LIGHT_PURPLE)
    c.text_c(560, 248, "Predict from:", BLACK, 1)
    c.text_c(560, 265, "pathway / target overlap", GRAY, 1)

    c.arrow(180, 96, 200, 130, MED_BLUE, 2, 7)
    c.arrow(560, 96, 560, 130, DARK_GREEN, 2, 7)

    # Computational methods band (bottom)
    c.rect(40, 320, 720, 420, DARK_BLUE, PALE_BLUE)
    c.text_c(380, 330, "Computational Prediction Strategies", BLACK, 1)
    methods = [("Similarity", 70, MED_BLUE),
               ("Matrix factor.", 210, ORANGE),
               ("Knowledge graph", 360, PURPLE),
               ("Graph NN", 520, DARK_GREEN),
               ("Multimodal DL", 630, RED)]
    for label, x, col in methods:
        c.rect(x, 355, x + 110, 400, col, WHITE)
        c.text_c(x + 55, 372, label, BLACK, 1)

    c.text(40, 455, "Figure 7.2: PK and PD interaction categories and their prediction strategies", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_7_2_DDI_Mechanisms.png'))
    print("  Figure_7_2_DDI_Mechanisms.png done")


def fig3_safety_continuum():
    """Figure 7.3: Preclinical-clinical safety pipeline continuum."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "ML Across the Drug Safety Pipeline", BLACK, 2)

    stages = [
        ("In Silico\nScreening", 30, DARK_BLUE, PALE_BLUE,
         ["Structure-based", "tox prediction", "Read-across"]),
        ("Preclinical", 210, DARK_GREEN, LIGHT_GREEN,
         ["High-content", "Toxicogenomics", "NAMs / 3Rs"]),
        ("Clinical\nTrials", 390, ORANGE, LIGHT_ORANGE,
         ["Risk prediction", "Patient monitoring", "Signal watch"]),
        ("Post-Market", 570, PURPLE, LIGHT_PURPLE,
         ["Pharmacovigilance", "EHR mining", "Spontaneous reports"]),
    ]
    bw, bh = 150, 60
    by = 80
    for label, bx, col, fill, items in stages:
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        for li, ln in enumerate(label.split("\n")):
            c.text_c(bx + bw // 2, by + bh // 2 - 10 + li * 14, ln, BLACK, 1)
        # detail list
        c.rect(bx, by + 90, bx + bw, by + 200, GRAY, (248, 248, 248))
        for ii, it in enumerate(items):
            c.text(bx + 8, by + 100 + ii * 22, "- " + it, GRAY, 1)
        c.arrow(bx + bw // 2, by + 60, bx + bw // 2, by + 90, col, 2, 6)

    # connecting arrows between stages
    for i in range(len(stages) - 1):
        x1 = stages[i][1] + bw
        x2 = stages[i + 1][1]
        c.arrow(x1, by + bh // 2, x2, by + bh // 2, GRAY, 2, 8)

    # time axis
    c.arrow(30, 320, 720, 320, BLACK, 2, 9)
    c.text(330, 328, "Development timeline ->", BLACK, 1)

    # feedback arrow
    c.line(645, 300, 645, 360, RED, 2)
    c.line(645, 360, 105, 360, RED, 2)
    c.arrow(105, 360, 105, 285, RED, 2, 7)
    c.text_c(380, 368, "Post-market findings refine earlier predictive models", RED, 1)

    # accumulating evidence note
    c.text_c(380, 400, "Evidence accumulates; predictions refined as compound advances", GRAY, 1)

    c.text(40, 445, "Figure 7.3: The continuum of ML applications across preclinical and clinical safety", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_7_3_Safety_Continuum.png'))
    print("  Figure_7_3_Safety_Continuum.png done")


def fig4_pharmacovigilance():
    """Figure 7.4: ML-based pharmacovigilance workflow."""
    c = PNGCanvas(760, 480)
    c.text_c(380, 10, "Machine-Learning-Based Pharmacovigilance Workflow", BLACK, 2)

    # Stage 1: multi-source data (left column)
    c.text_c(110, 45, "1. Data Sources", BLACK, 1)
    sources = [("Spontaneous reports", 60, MED_BLUE),
               ("Electronic health rec.", 105, DARK_GREEN),
               ("Claims data", 150, ORANGE),
               ("Literature", 195, PURPLE),
               ("Social media", 240, RED)]
    for label, y, col in sources:
        c.rect(25, y, 200, y + 35, col, WHITE)
        c.text_c(112, y + 12, label, BLACK, 1)

    # Stage 2: processing (center)
    c.text_c(380, 45, "2. Processing", BLACK, 1)
    c.rect(260, 70, 500, 260, DARK_BLUE, PALE_BLUE)
    c.text_c(380, 85, "NLP + Statistical Methods", BLACK, 1)
    c.text(275, 110, "- Named entity recognition", GRAY, 1)
    c.text(275, 135, "- Relation extraction", GRAY, 1)
    c.text(275, 160, "- Duplicate detection", GRAY, 1)
    c.text(275, 185, "- Disproportionality / ML", GRAY, 1)
    c.text(275, 210, "- Signal scoring", GRAY, 1)
    c.text(275, 235, "- Uncertainty estimates", GRAY, 1)
    for label, y, col in sources:
        c.arrow(200, y + 17, 260, 165, GRAY, 1, 6)

    # Stage 3: candidate signals (right)
    c.text_c(630, 45, "3. Candidate Signals", BLACK, 1)
    c.rect(540, 90, 730, 200, GOLD, LIGHT_GOLD)
    c.text_c(635, 105, "Prioritised drug-event", BLACK, 1)
    c.text_c(635, 122, "associations", BLACK, 1)
    c.text_c(635, 150, "ranked by strength", GRAY, 1)
    c.text_c(635, 167, "& plausibility", GRAY, 1)
    c.arrow(500, 160, 540, 145, BLACK, 2, 8)

    # Stage 4: expert evaluation (bottom, human)
    c.rect(200, 300, 560, 400, DARK_GREEN, LIGHT_GREEN)
    c.text_c(380, 315, "4. EXPERT EVALUATION (human)", BLACK, 1)
    c.text_c(380, 340, "Causality assessment - Regulatory judgement", BLACK, 1)
    c.text_c(380, 362, "Labelling changes - Risk communication", GRAY, 1)
    c.text_c(380, 382, "Human accountability retained", RED, 1)
    c.arrow(635, 200, 500, 300, BLACK, 2, 8)

    # feedback
    c.line(200, 350, 110, 350, GRAY, 2)
    c.line(110, 350, 110, 290, GRAY, 2)
    c.arrow(110, 290, 110, 280, GRAY, 2, 6)
    c.text(120, 355, "monitor & update", GRAY, 1)

    c.text(40, 455, "Figure 7.4: Pharmacovigilance workflow from data ingestion to expert action", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_7_4_Pharmacovigilance.png'))
    print("  Figure_7_4_Pharmacovigilance.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Chapter 7 figures...")
    fig1_multimodal_tox()
    fig2_ddi_mechanisms()
    fig3_safety_continuum()
    fig4_pharmacovigilance()
    print(f"\nAll 4 figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz/1024:.1f} KB")


if __name__ == '__main__':
    main()
