#!/usr/bin/env python3
"""
Generate 4 scientific figures (PNG) for Chapter 1:
Introduction to AI-Driven Pharmacology and Biomedical Engineering.

Reuses the pure-Python PNGCanvas from generate_figures.py (no external deps).
"""

import os
import math
import random

# Reuse the proven PNGCanvas + font from the existing repo module.
from generate_figures import (
    PNGCanvas, DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN, ORANGE, LIGHT_ORANGE,
    RED, LIGHT_RED, PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/pharma_figures'


def fig1_pipeline():
    """Figure 1: Integrated AI-driven discovery/design/modeling pipeline."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Integrated AI-Driven Discovery and Design Pipeline", BLACK, 2)

    # Three discipline lanes (labels on left)
    lanes = [("Pharmacology", 90, DARK_BLUE, PALE_BLUE),
             ("Engineering", 210, DARK_GREEN, LIGHT_GREEN),
             ("Computation", 330, PURPLE, LIGHT_PURPLE)]
    for name, ly, col, fill in lanes:
        c.fill_rect(10, ly-18, 150, ly+18, fill)
        c.rect(10, ly-18, 150, ly+18, col)
        c.text_c(80, ly-4, name, BLACK, 1)

    # Pipeline stages across the top flow
    stages = [
        ("Target ID", 180, 70, DARK_BLUE, PALE_BLUE),
        ("Generative\nDesign", 320, 70, PURPLE, LIGHT_PURPLE),
        ("Property\nPrediction", 460, 70, MED_BLUE, LIGHT_BLUE),
        ("Synthesis /\nFabrication", 600, 70, DARK_GREEN, LIGHT_GREEN),
        ("Assay &\nValidation", 680, 210, ORANGE, LIGHT_ORANGE),
    ]
    bw, bh = 120, 60
    centers = []
    for label, bx, by, col, fill in stages:
        c.rect(bx-bw//2, by-bh//2, bx+bw//2, by+bh//2, col, fill)
        parts = label.split("\n")
        for k, p in enumerate(parts):
            c.text_c(bx, by-6+k*12, p, BLACK, 1)
        centers.append((bx, by))

    # Arrows connecting stages
    for i in range(len(centers)-1):
        x1, y1 = centers[i]; x2, y2 = centers[i+1]
        dx, dy = x2-x1, y2-y1
        d = math.sqrt(dx*dx+dy*dy)
        off = 62
        c.arrow(int(x1+dx/d*off), int(y1+dy/d*off),
                int(x2-dx/d*off), int(y2-dy/d*off), GRAY, 2, 8)

    # Central feedback loop box
    c.rect(300, 200, 470, 250, GOLD, LIGHT_GOLD)
    c.text_c(385, 212, "Active-Learning", BLACK, 1)
    c.text_c(385, 228, "Feedback Loop", BLACK, 1)
    # feedback arrow from validation back to generative design
    c.line(680, 245, 680, 300, RED, 2)
    c.line(680, 300, 320, 300, RED, 2)
    c.arrow(320, 300, 320, 105, RED, 2, 8)
    c.text(430, 305, "Iterate: refine designs from experimental feedback", RED, 1)

    # Data foundation bar
    c.rect(180, 360, 700, 410, DARK_BLUE, PALE_BLUE)
    c.text_c(440, 370, "Shared Data Foundation (FAIR)", BLACK, 1)
    c.text(200, 388, "Genomic  |  Chemical  |  Imaging  |  Sensor  |  Clinical", MED_BLUE, 1)
    for cx in centers:
        c.line(cx[0], min(cx[1]+30, 250), cx[0], 360, LIGHT_GRAY, 1)

    c.text(30, 445, "Figure 1. Integrated AI-driven pipeline linking pharmacological "
                    "discovery, engineering design, and computation.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Pipeline.png'))
    print("  Figure_1_Pipeline.png done")


def fig2_autonomous_lab():
    """Figure 2: Closed-loop autonomous laboratory architecture."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Closed-Loop Autonomous Laboratory Architecture", BLACK, 2)

    # Four modules arranged in a cycle
    nodes = [
        ("AI Reasoning\n& Planning", 200, 120, DARK_BLUE, PALE_BLUE),
        ("Robotic\nExecution", 560, 120, DARK_GREEN, LIGHT_GREEN),
        ("Automated\nCharacterization", 560, 330, ORANGE, LIGHT_ORANGE),
        ("Data Analysis\n& Model Update", 200, 330, PURPLE, LIGHT_PURPLE),
    ]
    bw, bh = 160, 80
    ctr = []
    for label, bx, by, col, fill in nodes:
        c.rect(bx-bw//2, by-bh//2, bx+bw//2, by+bh//2, col, fill)
        for k, p in enumerate(label.split("\n")):
            c.text_c(bx, by-8+k*14, p, BLACK, 1)
        ctr.append((bx, by))

    # Clockwise arrows with labels
    labels = ["hypotheses / actions", "synthesize", "measurements", "update policy"]
    lab_pos = [(380, 100), (600, 225), (380, 350), (150, 225)]
    for i in range(4):
        x1, y1 = ctr[i]; x2, y2 = ctr[(i+1) % 4]
        dx, dy = x2-x1, y2-y1
        d = math.sqrt(dx*dx+dy*dy)
        c.arrow(int(x1+dx/d*90), int(y1+dy/d*45),
                int(x2-dx/d*90), int(y2-dy/d*45), MED_BLUE, 2, 8)
    c.text_c(380, 92, "hypotheses / actions", GRAY, 1)
    c.text_c(640, 225, "synthesize", GRAY, 1)
    c.text_c(380, 360, "raw measurements", GRAY, 1)
    c.text_c(110, 225, "model update", GRAY, 1)

    # Center: closed loop indicator
    c.circle(380, 225, 34, GOLD, LIGHT_GOLD)
    c.text_c(380, 212, "Closed", BLACK, 1)
    c.text_c(380, 226, "Loop", BLACK, 1)

    # Human oversight box
    c.rect(300, 400, 460, 440, RED, LIGHT_RED)
    c.text_c(380, 414, "Human Oversight & Objectives", BLACK, 1)
    c.arrow(380, 400, 380, 259, RED, 1, 7)

    c.text(30, 455, "Figure 2. Architecture of a closed-loop autonomous laboratory "
                    "integrating AI reasoning, robotic execution, and feedback.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Autonomous_Lab.png'))
    print("  Figure_2_Autonomous_Lab.png done")


def fig3_treatment_cycle():
    """Figure 3: Personalized closed-loop treatment cycle."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Personalized Closed-Loop Treatment Cycle", BLACK, 2)

    # Left: multi-modal patient data inputs
    c.rect(20, 60, 190, 300, DARK_BLUE, PALE_BLUE)
    c.text_c(105, 70, "Patient Data", BLACK, 1)
    inputs = [("Genomics", MED_BLUE), ("Wearable sensors", MED_GREEN),
              ("Imaging", ORANGE), ("EHR history", PURPLE),
              ("Labs / biomarkers", RED)]
    for k, (lbl, col) in enumerate(inputs):
        yy = 100 + k*38
        c.fill_rect(35, yy, 55, yy+20, col)
        c.text(65, yy+4, lbl, BLACK, 1)

    # Middle: predictive model
    c.rect(260, 120, 470, 240, PURPLE, LIGHT_PURPLE)
    c.text_c(365, 140, "Predictive Model", BLACK, 2)
    c.text_c(365, 170, "risk / response", BLACK, 1)
    c.text_c(365, 186, "estimation", BLACK, 1)
    c.text_c(365, 210, "dose optimization", GRAY, 1)
    c.arrow(190, 180, 260, 180, GRAY, 2, 8)

    # Right: adaptive therapy
    c.rect(540, 120, 730, 240, DARK_GREEN, LIGHT_GREEN)
    c.text_c(635, 140, "Adaptive Therapy", BLACK, 1)
    c.text_c(635, 168, "drug / dose", BLACK, 1)
    c.text_c(635, 186, "device settings", BLACK, 1)
    c.text_c(635, 210, "delivered to patient", GRAY, 1)
    c.arrow(470, 180, 540, 180, GRAY, 2, 8)

    # Feedback: monitor outcomes back to data
    c.line(635, 240, 635, 340, RED, 2)
    c.line(635, 340, 105, 340, RED, 2)
    c.arrow(105, 340, 105, 300, RED, 2, 8)
    c.text_c(370, 350, "continuous monitoring of outcomes  ->  re-personalize", RED, 1)

    # bottom: contrast episodic vs continuous
    c.rect(20, 380, 730, 430, LIGHT_GRAY, (248, 248, 248))
    c.text(35, 392, "Episodic care: decide -> treat -> reassess at next visit", GRAY, 1)
    c.text(35, 410, "AI-enabled care: sense -> model -> adjust  (continuous, individualized)",
           DARK_GREEN, 1)

    c.text(30, 455, "Figure 3. Personalized closed-loop treatment cycle integrating "
                    "multi-modal data, prediction, and adaptive therapy.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Treatment_Cycle.png'))
    print("  Figure_3_Treatment_Cycle.png done")


def fig4_governance():
    """Figure 4: Governance framework balancing opportunities and challenges."""
    c = PNGCanvas(760, 490)
    c.text_c(380, 10, "Governance Framework: Opportunities vs. Challenges", BLACK, 2)

    # Left column: opportunities
    c.rect(20, 55, 250, 300, DARK_GREEN, LIGHT_GREEN)
    c.text_c(135, 66, "Opportunities", BLACK, 2)
    opps = ["Accelerated discovery", "Personalized therapy",
            "Democratized expertise", "Scientific insight"]
    for k, o in enumerate(opps):
        yy = 100 + k*45
        c.circle(45, yy+6, 5, DARK_GREEN, MED_GREEN)
        c.text(60, yy, o, BLACK, 1)

    # Right column: challenges
    c.rect(510, 55, 740, 300, RED, LIGHT_RED)
    c.text_c(625, 66, "Challenges", BLACK, 2)
    chs = ["Data quality & bias", "Interpretability",
           "Validation & drift", "Regulation & privacy"]
    for k, ch in enumerate(chs):
        yy = 100 + k*45
        c.circle(535, yy+6, 5, RED, (220, 80, 80))
        c.text(550, yy, ch, BLACK, 1)

    # Center: balance / governance pillar
    c.rect(290, 90, 470, 260, DARK_BLUE, PALE_BLUE)
    c.text_c(380, 102, "Responsible", BLACK, 1)
    c.text_c(380, 118, "Governance", BLACK, 1)
    pillars = ["Technical rigor", "Clinical oversight",
               "Regulatory frameworks", "Ethics & equity"]
    for k, p in enumerate(pillars):
        c.text_c(380, 145 + k*26, p, MED_BLUE, 1)

    # Balance arrows from both sides into center
    c.arrow(250, 150, 290, 150, GRAY, 2, 8)
    c.arrow(510, 150, 470, 150, GRAY, 2, 8)

    # Lifecycle bar at the bottom
    c.rect(20, 330, 740, 420, GOLD, LIGHT_GOLD)
    c.text_c(380, 340, "Lifecycle Governance (continuous obligation)", BLACK, 1)
    phases = [("Pre-deployment\nvalidation", 130),
              ("Deployment\nmonitoring", 380),
              ("Post-deployment\naudit & update", 630)]
    for label, px in phases:
        c.rect(px-90, 365, px+90, 410, DARK_BLUE, PALE_BLUE)
        for k, p in enumerate(label.split("\n")):
            c.text_c(px, 375+k*14, p, BLACK, 1)
    c.arrow(220, 388, 290, 388, GRAY, 2, 7)
    c.arrow(470, 388, 540, 388, GRAY, 2, 7)

    c.text(30, 470, "Figure 4. Governance framework balancing opportunities and "
                    "challenges across technical, clinical, regulatory, and ethical dimensions.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Governance.png'))
    print("  Figure_4_Governance.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Chapter 1 figures...")
    fig1_pipeline()
    fig2_autonomous_lab()
    fig3_treatment_cycle()
    fig4_governance()
    print(f"\nAll 4 figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz/1024:.1f} KB")


if __name__ == '__main__':
    main()
