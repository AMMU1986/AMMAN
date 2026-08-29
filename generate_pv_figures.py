#!/usr/bin/env python3
"""
Generate 4 figure images (PNG) for Chapter 8
"Artificial Intelligence in Pharmacovigilance".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 8.1 - End-to-end NLP pipeline for ADR extraction, normalisation, coding
  Figure 8.2 - Signal detection architecture over a distributed RWD network
  Figure 8.3 - Predictive risk-modelling framework (molecular + patient + DDI)
  Figure 8.4 - AI-augmented pharmacovigilance lifecycle with governance layer
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/pv_figures'


def gen_fig1():
    """Figure 8.1: End-to-end NLP pipeline for automated ADR detection."""
    c = PNGCanvas(780, 460)
    c.text_c(390, 10, "Automated ADR Detection Pipeline from Text Sources", BLACK, 2)

    # Input sources (left column)
    c.text(30, 45, "Heterogeneous Text Sources", BLACK, 1)
    sources = [
        ("Clinical narratives", MED_BLUE, LIGHT_BLUE),
        ("Literature abstracts", DARK_GREEN, LIGHT_GREEN),
        ("Spontaneous reports", ORANGE, LIGHT_ORANGE),
        ("Social media / forums", PURPLE, LIGHT_PURPLE),
    ]
    sx1, sx2 = 30, 190
    for i, (label, col, fill) in enumerate(sources):
        y1 = 65 + i * 48
        c.rect(sx1, y1, sx2, y1 + 36, col, fill)
        c.text_c((sx1 + sx2) // 2, y1 + 13, label, BLACK, 1)

    # Processing stages (center pipeline)
    stages = [
        ("Text\nPreprocessing", "Tokenise, normalise", MED_BLUE, LIGHT_BLUE),
        ("Named Entity\nRecognition", "Drugs & events", DARK_GREEN, LIGHT_GREEN),
        ("Relation &\nCausality", "Link drug-event", ORANGE, LIGHT_ORANGE),
        ("Terminology\nNormalisation", "MedDRA coding", PURPLE, LIGHT_PURPLE),
    ]
    px1, px2 = 250, 470
    for i, (title, sub, col, fill) in enumerate(stages):
        y1 = 65 + i * 78
        y2 = y1 + 58
        c.rect(px1, y1, px2, y2, col, fill)
        parts = title.split("\n")
        c.text_c((px1 + px2) // 2, y1 + 10, parts[0], BLACK, 1)
        c.text_c((px1 + px2) // 2, y1 + 24, parts[1], BLACK, 1)
        c.text_c((px1 + px2) // 2, y1 + 42, sub, GRAY, 1)
        if i < len(stages) - 1:
            midx = (px1 + px2) // 2
            c.arrow(midx, y2, midx, y2 + 20, GRAY, 3, 9)

    # Arrows from all sources into first stage
    for i in range(len(sources)):
        y = 83 + i * 48
        c.arrow(sx2 + 2, y, px1 - 4, 94, GRAY, 2, 8)

    # Human-in-the-loop review + output (right)
    c.rect(540, 90, 750, 190, GOLD, LIGHT_GOLD)
    c.text_c(645, 108, "HUMAN-IN-THE-LOOP", BLACK, 1)
    c.text_c(645, 128, "Expert verification", BLACK, 1)
    c.text_c(645, 146, "Causality & seriousness", BLACK, 1)
    c.text_c(645, 166, "Final adjudication", GRAY, 1)
    c.arrow(470, 250, 645, 192, MED_GREEN, 3, 10)
    c.text(500, 210, "candidate", MED_GREEN, 1)
    c.text(500, 224, "signals", MED_GREEN, 1)

    c.rect(540, 250, 750, 350, DARK_BLUE, PALE_BLUE)
    c.text_c(645, 268, "STRUCTURED OUTPUT", BLACK, 1)
    c.text_c(645, 288, "Coded ICSRs", BLACK, 1)
    c.text_c(645, 306, "Aggregated counts", BLACK, 1)
    c.text_c(645, 324, "Safety database", GRAY, 1)
    c.arrow(645, 190, 645, 250, GRAY, 3, 9)

    # Feedback loop (verified corrections retrain models)
    c.line(540, 300, 360, 300, RED, 1)
    c.line(360, 300, 360, 400, RED, 1)
    c.line(360, 400, 360, 400, RED, 1)
    c.arrow(360, 400, 360, 402, RED, 1, 6)
    c.text(370, 385, "verified data retrains models (feedback)", RED, 1)

    c.text(30, 440, "Figure 8.1: End-to-end NLP pipeline for extraction, normalisation and coding of ADRs with human oversight", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_8_1_ADR_Detection_Pipeline.png'))
    print("  Figure_8_1_ADR_Detection_Pipeline.png done")


def gen_fig2():
    """Figure 8.2: Signal detection over a distributed real-world data network."""
    c = PNGCanvas(780, 470)
    c.text_c(390, 10, "Signal Detection over a Distributed Real-World Data Network", BLACK, 2)

    # Institutional data sources (top row)
    c.text(30, 40, "Heterogeneous Institutional Data", BLACK, 1)
    insts = [
        ("Hospital\nEHR", MED_BLUE, LIGHT_BLUE),
        ("Insurance\nClaims", DARK_GREEN, LIGHT_GREEN),
        ("Disease\nRegistry", ORANGE, LIGHT_ORANGE),
        ("Pharmacy\nDispensing", PURPLE, LIGHT_PURPLE),
    ]
    bw = 150
    gap = 30
    for i, (label, col, fill) in enumerate(insts):
        bx = 40 + i * (bw + gap)
        c.rect(bx, 60, bx + bw, 120, col, fill)
        parts = label.split("\n")
        c.text_c(bx + bw // 2, 78, parts[0], BLACK, 1)
        c.text_c(bx + bw // 2, 96, parts[1], BLACK, 1)

    # Common data model layer (full-width connective band)
    c.rect(40, 155, 740, 205, GOLD, LIGHT_GOLD)
    c.text_c(390, 168, "COMMON DATA MODEL (e.g., OMOP)", BLACK, 1)
    c.text_c(390, 188, "Standardised structure + shared vocabulary; privacy preserved locally", GRAY, 1)
    for i in range(len(insts)):
        bx = 40 + i * (bw + gap) + bw // 2
        c.arrow(bx, 122, bx, 153, GRAY, 2, 8)

    # Analytic layer
    c.rect(40, 245, 740, 385, DARK_BLUE, PALE_BLUE)
    c.text_c(390, 258, "MACHINE LEARNING ANALYTIC LAYER", BLACK, 1)
    c.arrow(390, 207, 390, 243, GRAY, 3, 9)

    analytics = [
        ("Self-controlled\ndesigns", MED_BLUE, LIGHT_BLUE),
        ("Propensity /\nconfounding adj.", DARK_GREEN, LIGHT_GREEN),
        ("Representation\nlearning", ORANGE, LIGHT_ORANGE),
        ("Graph-based\nmodels", PURPLE, LIGHT_PURPLE),
    ]
    aw = 150
    for i, (label, col, fill) in enumerate(analytics):
        bx = 55 + i * (aw + 12)
        c.rect(bx, 285, bx + aw, 345, col, fill)
        parts = label.split("\n")
        c.text_c(bx + aw // 2, 300, parts[0], BLACK, 1)
        c.text_c(bx + aw // 2, 318, parts[1], BLACK, 1)
    c.text_c(390, 362, "Empirical calibration with negative controls", GRAY, 1)

    # Output
    c.rect(250, 410, 530, 445, RED, LIGHT_RED)
    c.text_c(390, 422, "Validated safety signals -> evaluation", BLACK, 1)
    c.arrow(390, 387, 390, 408, GRAY, 3, 9)

    c.text(30, 458, "Figure 8.2: Distributed RWD network standardised by a common data model feeding an ML analytic layer", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_8_2_Signal_Detection_Architecture.png'))
    print("  Figure_8_2_Signal_Detection_Architecture.png done")


def gen_fig3():
    """Figure 8.3: Predictive risk-modelling framework."""
    c = PNGCanvas(780, 460)
    c.text_c(390, 10, "Predictive Risk-Modelling Framework for Drug Safety", BLACK, 2)

    # Three input feature blocks (left)
    c.text(30, 45, "Feature Inputs", BLACK, 1)
    inputs = [
        ("Molecular", ["Structure", "Target binding", "QSAR liabilities"], MED_BLUE, LIGHT_BLUE),
        ("Patient-level", ["Demographics", "Comorbidities", "Genetics, labs"], DARK_GREEN, LIGHT_GREEN),
        ("Interaction", ["Co-medications", "Shared pathways", "Interaction graph"], PURPLE, LIGHT_PURPLE),
    ]
    ix1, ix2 = 30, 220
    for i, (title, bullets, col, fill) in enumerate(inputs):
        y1 = 65 + i * 105
        y2 = y1 + 88
        c.rect(ix1, y1, ix2, y2, col, fill)
        c.text_c((ix1 + ix2) // 2, y1 + 10, title, BLACK, 1)
        for j, b in enumerate(bullets):
            c.text_c((ix1 + ix2) // 2, y1 + 30 + j * 16, b, BLACK, 1)

    # Model core (center)
    c.rect(300, 130, 490, 280, ORANGE, LIGHT_ORANGE)
    c.text_c(395, 150, "PREDICTIVE MODEL", BLACK, 1)
    c.text_c(395, 172, "Gradient boosting /", BLACK, 1)
    c.text_c(395, 188, "deep nets /", BLACK, 1)
    c.text_c(395, 204, "graph neural nets", BLACK, 1)
    c.text_c(395, 228, "+ probability", GRAY, 1)
    c.text_c(395, 244, "calibration", GRAY, 1)
    for i in range(3):
        y = 109 + i * 105
        c.arrow(ix2 + 2, y, 300 - 4, 205, GRAY, 2, 8)

    # Outputs (right)
    c.rect(560, 120, 755, 185, RED, LIGHT_RED)
    c.text_c(657, 136, "Calibrated risk", BLACK, 1)
    c.text_c(657, 154, "estimate per", BLACK, 1)
    c.text_c(657, 170, "patient / drug pair", BLACK, 1)
    c.arrow(490, 175, 560 - 4, 152, MED_GREEN, 3, 9)

    c.rect(560, 215, 755, 285, GOLD, LIGHT_GOLD)
    c.text_c(657, 231, "Signal priority", BLACK, 1)
    c.text_c(657, 249, "score (triage of", BLACK, 1)
    c.text_c(657, 267, "expert review)", BLACK, 1)
    c.arrow(490, 235, 560 - 4, 250, MED_GREEN, 3, 9)

    # Decision layer (bottom)
    c.rect(300, 330, 755, 400, DARK_BLUE, PALE_BLUE)
    c.text_c(527, 348, "RISK-MANAGEMENT DECISION LAYER", BLACK, 1)
    c.text_c(527, 370, "Intensified monitoring - dose adjustment - alerts - prioritised evaluation", GRAY, 1)
    c.arrow(657, 285, 657, 330, GRAY, 3, 9)
    c.arrow(657, 185, 657, 215, GRAY, 2, 8)

    c.text(30, 435, "Figure 8.3: Predictive framework combining molecular, patient and interaction features into calibrated risk", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_8_3_Predictive_Risk_Framework.png'))
    print("  Figure_8_3_Predictive_Risk_Framework.png done")


def gen_fig4():
    """Figure 8.4: AI-augmented pharmacovigilance lifecycle with governance layer."""
    c = PNGCanvas(800, 440)
    c.text_c(400, 10, "The AI-Augmented Pharmacovigilance Lifecycle", BLACK, 2)

    # Horizontal lifecycle stages
    stages = [
        ("Data\nAcquisition", MED_BLUE, LIGHT_BLUE),
        ("Detection", DARK_GREEN, LIGHT_GREEN),
        ("Prediction", ORANGE, LIGHT_ORANGE),
        ("Prioritisation", PURPLE, LIGHT_PURPLE),
        ("Risk\nManagement", RED, LIGHT_RED),
    ]
    bw = 130
    gap = 15
    top = 90
    bh = 90
    xs = []
    for i, (label, col, fill) in enumerate(stages):
        bx = 30 + i * (bw + gap)
        xs.append((bx, bx + bw))
        c.rect(bx, top, bx + bw, top + bh, col, fill)
        parts = label.split("\n")
        if len(parts) == 1:
            c.text_c(bx + bw // 2, top + bh // 2 - 4, parts[0], BLACK, 1)
        else:
            c.text_c(bx + bw // 2, top + bh // 2 - 12, parts[0], BLACK, 1)
            c.text_c(bx + bw // 2, top + bh // 2 + 4, parts[1], BLACK, 1)
        if i > 0:
            c.arrow(xs[i - 1][1] + 2, top + bh // 2, bx - 4, top + bh // 2, GRAY, 3, 9)

    # Sub-labels under each stage
    subs = ["EHR, claims,\nreports, social", "NLP,\nmultimodal ML", "Molecular +\npatient risk", "Composite\nscoring", "Labelling,\nRMM, reporting"]
    for i, s in enumerate(subs):
        bx = 30 + i * (bw + gap)
        parts = s.split("\n")
        c.text_c(bx + bw // 2, top + bh + 12, parts[0], GRAY, 1)
        c.text_c(bx + bw // 2, top + bh + 26, parts[1], GRAY, 1)

    # Feedback arc back from Risk Management to Data Acquisition
    fy = top + bh + 55
    c.line(xs[4][0] + bw // 2, top + bh + 35, xs[4][0] + bw // 2, fy, GRAY, 2)
    c.line(xs[4][0] + bw // 2, fy, xs[0][0] + bw // 2, fy, GRAY, 2)
    c.arrow(xs[0][0] + bw // 2, fy, xs[0][0] + bw // 2, top + bh + 42, GRAY, 2, 8)
    c.text_c(400, fy - 12, "continuous lifecycle feedback", GRAY, 1)

    # Governance / oversight horizontal layer spanning the whole lifecycle
    gy1 = fy + 30
    gy2 = gy1 + 70
    c.rect(30, gy1, xs[4][1], gy2, GOLD, LIGHT_GOLD)
    c.text_c(400, gy1 + 14, "CROSS-CUTTING GOVERNANCE & OVERSIGHT", BLACK, 1)
    gov = "Interpretability  |  Bias & equity audits  |  Privacy (federated)  |  Validation & monitoring  |  Accountability"
    c.text_c(400, gy1 + 36, gov, GRAY, 1)
    c.text_c(400, gy1 + 54, "Human experts retain final judgement at every stage", GRAY, 1)
    # connectors from each stage down to governance layer
    for (bx1, bx2) in xs:
        midx = (bx1 + bx2) // 2
        c.line(midx, top + bh + 40, midx, gy1, LIGHT_GRAY)

    c.text(30, 425, "Figure 8.4: Lifecycle map from data acquisition to risk management, with a cross-cutting governance layer", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_8_4_PV_Lifecycle.png'))
    print("  Figure_8_4_PV_Lifecycle.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating pharmacovigilance chapter figures...")
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
