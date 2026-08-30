#!/usr/bin/env python3
"""
Generate 4 scientific figures (PNG) for Chapter 19:
Ethics, Regulation, and Clinical Translation of AI.
Reuses the pure-stdlib PNGCanvas from generate_figures.py.
"""

import os
import math

# Reuse the drawing engine and colors from the existing figure generator
from generate_figures import (
    PNGCanvas,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE, RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/ch19_figures'


def gen_fig1():
    """Figure 1: Taxonomy of explainability approaches for medical AI."""
    c = PNGCanvas(760, 500)
    c.text_c(380, 10, "Taxonomy of Explainability Approaches in Medical AI", BLACK, 2)

    # Root box
    c.rect(300, 45, 460, 85, DARK_BLUE, PALE_BLUE)
    c.text_c(380, 55, "Explainability", BLACK, 1)
    c.text_c(380, 70, "in Medical AI", BLACK, 1)

    # Two branches
    c.rect(90, 130, 320, 170, DARK_GREEN, LIGHT_GREEN)
    c.text_c(205, 140, "Intrinsically", BLACK, 1)
    c.text_c(205, 154, "Interpretable Models", BLACK, 1)
    c.rect(440, 130, 670, 170, ORANGE, LIGHT_ORANGE)
    c.text_c(555, 140, "Post-hoc", BLACK, 1)
    c.text_c(555, 154, "Explanation Methods", BLACK, 1)

    c.arrow(340, 85, 210, 130, GRAY, 2, 8)
    c.arrow(420, 85, 555, 130, GRAY, 2, 8)

    # Intrinsic leaves
    intrinsic = ["Linear / logistic", "Decision trees", "Generalized additive", "Rule lists"]
    for i, name in enumerate(intrinsic):
        y = 200 + i * 40
        c.rect(70, y, 340, y + 30, MED_GREEN, (235, 245, 235))
        c.text_c(205, y + 10, name, BLACK, 1)
        c.arrow(205, 170 if i == 0 else y - 10, 205, y, GRAY, 1, 5)

    # Post-hoc leaves
    posthoc = ["Feature attribution (SHAP/LIME)", "Saliency maps (imaging)",
               "Counterfactual explanations", "Example-based (similar cases)"]
    for i, name in enumerate(posthoc):
        y = 200 + i * 40
        c.rect(410, y, 700, y + 30, ORANGE, (255, 245, 235))
        c.text_c(555, y + 10, name, BLACK, 1)
        c.arrow(555, 170 if i == 0 else y - 10, 555, y, GRAY, 1, 5)

    # Audience mapping band
    c.rect(60, 395, 700, 470, LIGHT_GRAY, (248, 248, 248))
    c.text(75, 402, "Audience -> Question the explanation must answer:", BLACK, 1)
    c.text(75, 422, "Regulator: Does it behave safely across subgroups?", MED_BLUE, 1)
    c.text(75, 440, "Clinician: What drives this recommendation / confidence?", DARK_GREEN, 1)
    c.text(75, 458, "Patient: What role did AI play in my care?", PURPLE, 1)

    c.text(60, 482, "Figure 1: Explainability taxonomy mapped to clinical audiences", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1.png'))
    print("  Figure_1.png done")


def gen_fig2():
    """Figure 2: Lifecycle regulatory model for adaptive AI (continuous loop)."""
    c = PNGCanvas(760, 500)
    c.text_c(380, 10, "Lifecycle Regulatory Model for Adaptive Medical AI", BLACK, 2)

    cx, cy, r = 380, 250, 135

    nodes = [
        ("Premarket\nAuthorization", DARK_BLUE, PALE_BLUE),
        ("Predetermined\nChange Control", PURPLE, LIGHT_PURPLE),
        ("Deployment &\nModel Update", DARK_GREEN, LIGHT_GREEN),
        ("Post-market\nSurveillance", ORANGE, LIGHT_ORANGE),
    ]
    centers = []
    for i, (label, col, fill) in enumerate(nodes):
        ang = -math.pi / 2 + i * (math.pi / 2)
        nx = int(cx + r * math.cos(ang))
        ny = int(cy + r * math.sin(ang))
        c.rect(nx - 85, ny - 32, nx + 85, ny + 32, col, fill)
        parts = label.split("\n")
        for j, p in enumerate(parts):
            c.text_c(nx, ny - 8 + j * 14, p, BLACK, 1)
        centers.append((nx, ny))

    # Arrows around the loop (clockwise)
    for i in range(4):
        x1, y1 = centers[i]
        x2, y2 = centers[(i + 1) % 4]
        dx, dy = x2 - x1, y2 - y1
        d = math.sqrt(dx * dx + dy * dy)
        off = 95
        c.arrow(int(x1 + dx / d * off), int(y1 + dy / d * off),
                int(x2 - dx / d * off), int(y2 - dy / d * off), GRAY, 2, 9)

    # Center hub
    c.circle(cx, cy, 58, GOLD, LIGHT_GOLD)
    c.text_c(cx, cy - 14, "Continuous", BLACK, 1)
    c.text_c(cx, cy, "Governance", BLACK, 1)
    c.text_c(cx, cy + 14, "Loop", BLACK, 1)

    # Re-authorization boundary note
    c.rect(30, 430, 730, 470, LIGHT_RED, (255, 245, 245))
    c.text_c(380, 442, "Changes beyond predefined boundaries trigger re-authorization;", BLACK, 1)
    c.text_c(380, 456, "real-world evidence feeds back to developers and regulators", BLACK, 1)

    c.text(60, 484, "Figure 2: Continuous lifecycle oversight for learning systems", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2.png'))
    print("  Figure_2.png done")


def gen_fig3():
    """Figure 3: Clinical validation-to-deployment pipeline (evidentiary ladder)."""
    c = PNGCanvas(760, 500)
    c.text_c(380, 10, "Clinical Validation-to-Deployment Pipeline", BLACK, 2)

    stages = [
        ("1. Analytical / Technical Validation", "Accurate on training-like data", DARK_BLUE, PALE_BLUE),
        ("2. External Validation", "Holds across new sites & populations", MED_BLUE, LIGHT_BLUE),
        ("3. Temporal Validation", "Robust to drift over time", DARK_GREEN, LIGHT_GREEN),
        ("4. Clinical Utility (Prospective RCT)", "Improves patient outcomes", ORANGE, LIGHT_ORANGE),
        ("5. Post-market Monitoring", "Recurring local revalidation", PURPLE, LIGHT_PURPLE),
    ]
    # Ascending "ladder" of boxes
    bx = 120
    for i, (title, sub, col, fill) in enumerate(stages):
        y = 400 - i * 70
        w = 520
        c.rect(bx, y, bx + w, y + 52, col, fill)
        c.text(bx + 12, y + 12, title, BLACK, 1)
        c.text(bx + 12, y + 30, sub, GRAY, 1)
        # gate arrow upward
        if i < len(stages) - 1:
            c.arrow(bx + w // 2, y - 2, bx + w // 2, y - 16, GRAY, 2, 8)
        # rung number circle
        c.circle(bx - 30, y + 26, 16, col, fill)
        c.text_c(bx - 30, y + 20, str(i + 1), BLACK, 1)

    # Gate label
    c.rect(670, 60, 745, 410, LIGHT_GRAY, (248, 248, 248))
    c.text_c(707, 70, "Evidentiary", BLACK, 1)
    c.text_c(707, 84, "gates", BLACK, 1)
    c.text_c(707, 230, "higher", DARK_GREEN, 1)
    c.text_c(707, 244, "rung =", DARK_GREEN, 1)
    c.text_c(707, 258, "stronger", DARK_GREEN, 1)
    c.text_c(707, 272, "claim", DARK_GREEN, 1)
    c.arrow(707, 400, 707, 110, DARK_GREEN, 2, 9)

    c.text(60, 484, "Figure 3: Evidentiary ladder from technical validity to clinical utility", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3.png'))
    print("  Figure_3.png done")


def gen_fig4():
    """Figure 4: Human oversight and continuous monitoring framework."""
    c = PNGCanvas(760, 500)
    c.text_c(380, 10, "Human Oversight & Continuous Monitoring Framework", BLACK, 2)

    # Three core actors
    # AI model
    c.rect(60, 90, 250, 175, DARK_GREEN, LIGHT_GREEN)
    c.text_c(155, 108, "AI MODEL", BLACK, 2)
    c.text_c(155, 135, "Prediction +", BLACK, 1)
    c.text_c(155, 150, "uncertainty +", BLACK, 1)
    c.text_c(155, 165, "OOD flag", BLACK, 1)

    # Clinician
    c.rect(510, 90, 700, 175, DARK_BLUE, PALE_BLUE)
    c.text_c(605, 108, "CLINICIAN", BLACK, 2)
    c.text_c(605, 135, "Point-of-care", BLACK, 1)
    c.text_c(605, 150, "judgment &", BLACK, 1)
    c.text_c(605, 165, "override", BLACK, 1)

    # Governance body
    c.rect(285, 330, 475, 420, PURPLE, LIGHT_PURPLE)
    c.text_c(380, 348, "INSTITUTIONAL", BLACK, 1)
    c.text_c(380, 363, "GOVERNANCE", BLACK, 1)
    c.text_c(380, 385, "Approve / monitor /", BLACK, 1)
    c.text_c(380, 400, "recalibrate / retire", BLACK, 1)

    # Flows
    c.arrow(250, 120, 510, 120, ORANGE, 2, 9)
    c.text_c(380, 105, "recommendation + confidence", ORANGE, 1)
    c.arrow(510, 155, 250, 155, MED_BLUE, 2, 9)
    c.text_c(380, 168, "override / feedback", MED_BLUE, 1)

    c.arrow(155, 175, 300, 330, GRAY, 2, 8)
    c.text(150, 250, "performance", GRAY, 1)
    c.text(150, 265, "logs", GRAY, 1)
    c.arrow(605, 175, 460, 330, GRAY, 2, 8)
    c.text(560, 250, "usage &", GRAY, 1)
    c.text(560, 265, "outcomes", GRAY, 1)

    # Monitoring feedback from governance to model (dashed-like via segments)
    c.arrow(300, 375, 155, 175, RED, 2, 8)
    c.text(175, 300, "recalibrate", RED, 1)

    # Monitoring band bottom
    c.rect(40, 435, 720, 470, LIGHT_GRAY, (248, 248, 248))
    c.text_c(380, 442, "Continuous monitoring: calibration & subgroup accuracy vs. predefined thresholds", BLACK, 1)
    c.text_c(380, 458, "Thresholds breached -> review, recalibrate, or withdraw the model", RED, 1)

    c.text(60, 484, "Figure 4: Oversight as a continuous relationship, not a checkpoint", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4.png'))
    print("  Figure_4.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Chapter 19 figures...")
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
