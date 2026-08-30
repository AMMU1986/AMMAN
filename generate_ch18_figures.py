#!/usr/bin/env python3
"""
Generate 4 scientific figure images (PNG) for Chapter 18:
AI Applications in Disease-Specific Pharmacology.
Uses only the Python standard library (zlib + struct) via a reusable PNGCanvas.
Reuses the drawing primitives / bitmap font from generate_figures.py.
"""

import os
import math
from generate_figures import (
    PNGCanvas, DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN, ORANGE, LIGHT_ORANGE,
    RED, LIGHT_RED, PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/ch18_figures'


def gen_fig1():
    """Figure 1: Clinical decision-support pipeline for pharmacotherapy."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "AI Clinical Decision-Support Pipeline", BLACK, 2)

    # Data sources column
    c.rect(20, 60, 175, 320, DARK_BLUE, PALE_BLUE)
    c.text_c(97, 68, "Data Sources", BLACK, 1)
    srcs = ["EHR records", "Genomics", "Wearables", "Imaging / ECG",
            "Labs / vitals", "Med history"]
    for i, s in enumerate(srcs):
        c.text(30, 92 + i*32, "- " + s, MED_BLUE, 1)

    # Integration / preprocessing
    c.rect(215, 95, 360, 175, MED_GREEN, LIGHT_GREEN)
    c.text_c(287, 118, "Data", BLACK, 1)
    c.text_c(287, 133, "Harmonization", BLACK, 1)
    c.text_c(287, 150, "& Features", BLACK, 1)

    # Model
    c.rect(215, 210, 360, 300, ORANGE, LIGHT_ORANGE)
    c.text_c(287, 232, "Predictive", BLACK, 1)
    c.text_c(287, 248, "Models", BLACK, 2)
    c.text_c(287, 272, "ML / DL / RL", GRAY, 1)

    # Predictions
    c.rect(410, 95, 570, 300, PURPLE, LIGHT_PURPLE)
    c.text_c(490, 108, "Predictions", BLACK, 1)
    preds = ["Drug choice", "Dose / titration", "ADR risk", "Response prob."]
    for i, p in enumerate(preds):
        c.text(420, 138 + i*36, "- " + p, PURPLE, 1)

    # Clinician
    c.rect(615, 150, 745, 245, RED, LIGHT_RED)
    c.text_c(680, 175, "Clinician", BLACK, 1)
    c.text_c(680, 192, "Decision", BLACK, 1)
    c.text_c(680, 212, "+ Patient", GRAY, 1)

    # Arrows
    c.arrow(175, 190, 215, 150, GRAY, 2, 8)
    c.arrow(287, 175, 287, 210, GRAY, 2, 8)
    c.arrow(360, 250, 410, 210, GRAY, 2, 8)
    c.arrow(570, 197, 615, 197, GRAY, 2, 8)

    # Feedback loop
    c.text_c(400, 355, "Outcome Feedback / Active Learning Loop", GOLD, 1)
    c.line(680, 245, 680, 400, GOLD, 2)
    c.line(680, 400, 120, 400, GOLD, 2)
    c.line(120, 400, 120, 320, GOLD, 2)
    c.arrow(120, 320, 120, 315, GOLD, 2, 8)
    c.line(287, 300, 287, 375, GOLD, 1)
    c.line(287, 375, 680, 375, GOLD, 1)

    c.text(20, 445, "Figure 1: AI-enabled decision-support pipeline for pharmacotherapy.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1.png'))
    print("  Figure_1.png done")


def gen_fig2():
    """Figure 2: Multimodal data integration in precision oncology."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Multimodal Integration in Precision Oncology", BLACK, 2)

    # Modalities (left)
    mods = [("Genomics", DARK_BLUE, PALE_BLUE),
            ("Transcriptomics", MED_GREEN, LIGHT_GREEN),
            ("Radiomics", ORANGE, LIGHT_ORANGE),
            ("Histopathology", PURPLE, LIGHT_PURPLE),
            ("Clinical / ctDNA", RED, LIGHT_RED)]
    for i, (label, col, fill) in enumerate(mods):
        by = 60 + i*72
        c.rect(20, by, 175, by+52, col, fill)
        c.text_c(97, by+20, label, BLACK, 1)
        c.arrow(175, by+26, 235, 235, GRAY, 2, 7)

    # Shared representation (center)
    c.rect(235, 150, 400, 320, DARK_GREEN, LIGHT_GREEN)
    c.text_c(317, 175, "Shared", BLACK, 1)
    c.text_c(317, 192, "Latent", BLACK, 2)
    c.text_c(317, 216, "Representation", BLACK, 1)
    c.text_c(317, 250, "(embedding)", GRAY, 1)
    # nodes
    for r in range(4):
        for cc in range(3):
            c.circle(268 + cc*28, 275 + r*10, 3, MED_BLUE, MED_BLUE)

    # Outputs (right)
    outs = [("Therapy Selection", MED_BLUE, LIGHT_BLUE),
            ("Resistance Forecast", ORANGE, LIGHT_ORANGE),
            ("Combination Scoring", PURPLE, LIGHT_PURPLE),
            ("Toxicity Prediction", RED, LIGHT_RED)]
    for i, (label, col, fill) in enumerate(outs):
        by = 90 + i*80
        c.rect(460, by, 745, by+56, col, fill)
        c.text_c(602, by+24, label, BLACK, 1)
        c.arrow(400, 235, 460, by+28, GRAY, 2, 7)

    c.text(20, 445, "Figure 2: Multimodal data integration workflow for individualized cancer therapy.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2.png'))
    print("  Figure_2.png done")


def gen_fig3():
    """Figure 3: Closed-loop adaptive glycemic control."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Closed-Loop Adaptive Glycemic Control", BLACK, 2)

    # Loop boxes
    c.rect(60, 70, 230, 140, MED_GREEN, LIGHT_GREEN)
    c.text_c(145, 90, "Continuous", BLACK, 1)
    c.text_c(145, 106, "Glucose Sensor", BLACK, 1)

    c.rect(530, 70, 700, 140, MED_BLUE, LIGHT_BLUE)
    c.text_c(615, 90, "Control", BLACK, 1)
    c.text_c(615, 106, "Algorithm (AI)", BLACK, 1)

    c.rect(530, 250, 700, 320, ORANGE, LIGHT_ORANGE)
    c.text_c(615, 270, "Insulin Pump", BLACK, 1)
    c.text_c(615, 286, "Dosing", BLACK, 1)

    c.rect(60, 250, 230, 320, RED, LIGHT_RED)
    c.text_c(145, 270, "Patient", BLACK, 1)
    c.text_c(145, 286, "Physiology", BLACK, 1)

    # Arrows (clockwise)
    c.arrow(230, 105, 530, 105, GRAY, 2, 9)
    c.text_c(380, 88, "glucose data", GRAY, 1)
    c.arrow(615, 140, 615, 250, GRAY, 2, 9)
    c.text(625, 190, "dose", GRAY, 1)
    c.arrow(530, 285, 230, 285, GRAY, 2, 9)
    c.text_c(380, 268, "insulin delivery", GRAY, 1)
    c.arrow(145, 250, 145, 140, GRAY, 2, 9)
    c.text(30, 190, "response", GRAY, 1)

    # Glucose trace inset
    c.text(60, 350, "Time in range improves under closed-loop control:", BLACK, 1)
    c.vline(60, 370, 445, BLACK)
    c.hline(60, 720, 445, BLACK)
    # target band
    c.fill_rect(61, 400, 719, 425, (225, 240, 225))
    c.text(725, 405, "target", MED_GREEN, 1)
    # open loop (wavy, wide)
    for x in range(61, 390):
        t = (x-61)/50.0
        y = int(412 - 32*math.sin(t))
        c.pixel(x, y, RED); c.pixel(x, y+1, RED)
    # closed loop (tight)
    for x in range(390, 720):
        t = (x-390)/40.0
        y = int(412 - 10*math.sin(t))
        c.pixel(x, y, MED_BLUE); c.pixel(x, y+1, MED_BLUE)
    c.line(390, 375, 390, 445, GRAY, 1)
    c.text(200, 452, "open loop", RED, 1)
    c.text(520, 452, "closed loop (AI)", MED_BLUE, 1)

    c.text(20, 462, "Figure 3: Real-time feedback control of insulin delivery.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3.png'))
    print("  Figure_3.png done")


def gen_fig4():
    """Figure 4: Integrated antimicrobial/antiviral AI framework."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Integrated AI Framework for Anti-Infective Therapy", BLACK, 2)

    # Lifecycle stages left-to-right
    stages = [("Pathogen ID", 30, DARK_BLUE, PALE_BLUE),
              ("Resistance\nPrediction", 210, ORANGE, LIGHT_ORANGE),
              ("PK/PD\nOptimization", 390, MED_GREEN, LIGHT_GREEN),
              ("Therapy &\nStewardship", 570, PURPLE, LIGHT_PURPLE)]
    for label, bx, col, fill in stages:
        c.rect(bx, 70, bx+150, 160, col, fill)
        lines = label.split("\n")
        for li, ln in enumerate(lines):
            c.text_c(bx+75, 100 + li*18, ln, BLACK, 1)
        if bx < 560:
            c.arrow(bx+150, 115, bx+180, 115, GRAY, 2, 8)

    # Discovery branch (top)
    c.rect(210, 195, 550, 265, RED, LIGHT_RED)
    c.text_c(380, 212, "AI-Driven Discovery", BLACK, 1)
    c.text_c(380, 232, "Generative design | Deep docking | Novel classes", GRAY, 1)
    c.arrow(380, 195, 380, 160, RED, 2, 8)
    c.text(390, 172, "new agents", RED, 1)

    # Surveillance feedback (bottom)
    c.rect(120, 300, 640, 370, GOLD, LIGHT_GOLD)
    c.text_c(380, 318, "Genomic Surveillance & Viral-Escape Prediction", BLACK, 1)
    c.text_c(380, 338, "anticipates emerging variants -> updates targets", GRAY, 1)
    c.line(105, 335, 105, 115, GOLD, 2)
    c.arrow(105, 115, 30, 115, GOLD, 2, 8)
    c.line(645, 335, 720, 335, GOLD, 2)
    c.line(720, 335, 720, 115, GOLD, 2)
    c.arrow(720, 115, 645, 115, GOLD, 2, 8)

    c.text(20, 445, "Figure 4: AI spanning discovery, stewardship, and surveillance in anti-infective pharmacology.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4.png'))
    print("  Figure_4.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Chapter 18 figures...")
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
