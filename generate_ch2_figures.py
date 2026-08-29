#!/usr/bin/env python3
"""
Generate 4 figures (PNG) for Chapter 2: AI and ML in Healthcare.
Reuses the stdlib PNGCanvas + font renderer from generate_figures.py.
"""

import os
import math
from generate_figures import (
    PNGCanvas, DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN, ORANGE, LIGHT_ORANGE,
    RED, LIGHT_RED, PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/ch2_figures'


def fig1_workflow():
    """Figure 1: Iterative ML workflow for healthcare."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 12, "Machine Learning Workflow in Healthcare", BLACK, 2)

    stages = [
        ("Problem", "Formulation", 40, 70, DARK_BLUE, PALE_BLUE),
        ("Data Acquisition", "& Curation", 300, 70, MED_BLUE, LIGHT_BLUE),
        ("Feature / Rep.", "Learning", 560, 70, DARK_GREEN, LIGHT_GREEN),
        ("Model Training", "& Selection", 560, 250, ORANGE, LIGHT_ORANGE),
        ("Evaluation &", "Validation", 300, 250, PURPLE, LIGHT_PURPLE),
        ("Deployment &", "Monitoring", 40, 250, RED, LIGHT_RED),
    ]
    bw, bh = 165, 60
    centers = []
    for l1, l2, bx, by, col, fill in stages:
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        c.text_c(bx + bw // 2, by + 18, l1, BLACK, 1)
        c.text_c(bx + bw // 2, by + 34, l2, BLACK, 1)
        centers.append((bx + bw // 2, by + bh // 2))

    # Forward arrows across the top, down the right, back along bottom
    seq = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
    for i, j in seq:
        x1, y1 = centers[i]
        x2, y2 = centers[j]
        dx, dy = x2 - x1, y2 - y1
        d = math.sqrt(dx * dx + dy * dy)
        off1 = 90 if abs(dx) > abs(dy) else 34
        off2 = 90 if abs(dx) > abs(dy) else 34
        c.arrow(int(x1 + dx / d * off1), int(y1 + dy / d * off1),
                int(x2 - dx / d * off2), int(y2 - dy / d * off2), GRAY, 2, 9)

    # Feedback loop arrow (bottom-left back up to data) - dashed style via center note
    c.rect(285, 165, 475, 210, GOLD, LIGHT_GOLD)
    c.text_c(380, 178, "Feedback &", BLACK, 1)
    c.text_c(380, 192, "Iterative Refinement", BLACK, 1)
    # dashed arrow from Evaluation up toward Data
    for seg in range(0, 120, 14):
        c.line(300, 250 - 0 - seg // 3, 300, 250 - seg, GRAY, 1)
    c.arrow(300, 165, 300, 132, RED, 2, 9)

    c.text_c(380, 445, "Figure 1: Cyclical ML workflow with feedback from monitoring to earlier stages", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1.png'))
    print("  Figure_1.png done")


def fig2_supervised():
    """Figure 2: Classification vs regression."""
    c = PNGCanvas(760, 440)
    c.text_c(380, 12, "Supervised Learning: Classification vs. Regression", BLACK, 2)

    # (a) Classification scatter with boundary
    c.text(40, 45, "(a) Classification (discrete labels)", BLACK, 1)
    ax0, ay0, ax1, ay1 = 60, 70, 360, 360
    c.vline(ax0, ay0, ay1, BLACK)
    c.hline(ax0, ax1, ay1, BLACK)
    c.text(30, ay0 - 2, "y", BLACK, 1)
    c.text(ax1 - 10, ay1 + 8, "x", BLACK, 1)
    # Two clusters
    import random
    random.seed(7)
    for _ in range(28):
        px = int(ax0 + 20 + random.random() * 110)
        py = int(ay1 - 20 - random.random() * 110)
        c.circle(px, py, 4, MED_BLUE, MED_BLUE)
    for _ in range(28):
        px = int(ax0 + 150 + random.random() * 120)
        py = int(ay1 - 130 - random.random() * 120)
        c.circle(px, py, 4, ORANGE, LIGHT_ORANGE)
    # decision boundary (diagonal)
    c.line(ax0 + 40, ay1 - 10, ax1 - 10, ay0 + 40, RED, 2)
    c.text(ax0 + 20, ay0 + 6, "Class A", MED_BLUE, 1)
    c.text(ax1 - 90, ay1 - 30, "Class B", ORANGE, 1)
    c.text(ax0 + 130, ay0 + 90, "boundary", RED, 1)

    # (b) Regression scatter with line
    c.text(430, 45, "(b) Regression (continuous value)", BLACK, 1)
    bx0, by0, bx1, by1 = 450, 70, 730, 360
    c.vline(bx0, by0, by1, BLACK)
    c.hline(bx0, bx1, by1, BLACK)
    c.text(420, by0 - 2, "y", BLACK, 1)
    c.text(bx1 - 10, by1 + 8, "x", BLACK, 1)
    for _ in range(34):
        t = random.random()
        px = int(bx0 + 15 + t * 250)
        base = by1 - 20 - t * 230
        py = int(base + (random.random() - 0.5) * 40)
        c.circle(px, py, 4, DARK_GREEN, LIGHT_GREEN)
    # best-fit line
    c.line(bx0 + 15, by1 - 20, bx1 - 15, by0 + 30, RED, 2)
    c.text(bx1 - 130, by0 + 40, "fitted line", RED, 1)

    c.text_c(380, 415, "Figure 2: Classification assigns categories; regression predicts continuous values", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2.png'))
    print("  Figure_2.png done")


def fig3_cnn():
    """Figure 3: CNN pipeline for a medical image."""
    c = PNGCanvas(820, 420)
    c.text_c(410, 12, "Convolutional Neural Network for Medical Image Analysis", BLACK, 2)

    # Input image (chest-like grid)
    c.rect(30, 120, 130, 220, BLACK, (230, 230, 235))
    for gx in range(40, 130, 12):
        c.vline(gx, 122, 218, (205, 205, 210))
    for gy in range(130, 220, 12):
        c.hline(32, 128, gy, (205, 205, 210))
    # a lesion blob
    c.circle(90, 175, 12, RED, LIGHT_RED)
    c.text_c(80, 228, "Input Image", BLACK, 1)

    # Conv/pool blocks getting smaller
    blocks = [
        (180, 110, 60, 120, MED_BLUE, LIGHT_BLUE, "Conv 1"),
        (270, 125, 48, 90, MED_BLUE, LIGHT_BLUE, "Conv 2"),
        (348, 140, 38, 60, DARK_GREEN, LIGHT_GREEN, "Conv 3"),
        (416, 152, 28, 36, DARK_GREEN, LIGHT_GREEN, "Pool"),
    ]
    prev_c = (100, 170)
    for bx, by, bw, bh, col, fill, lbl in blocks:
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        c.rect(bx + 4, by + 4, bx + bw + 4, by + bh + 4, col, None)
        c.text_c(bx + bw // 2, by + bh + 10, lbl, BLACK, 1)
        c.arrow(prev_c[0], prev_c[1], bx - 2, by + bh // 2, GRAY, 2, 7)
        prev_c = (bx + bw + 6, by + bh // 2)

    c.text_c(300, 300, "Feature Extraction (learned hierarchical features)", GRAY, 1)

    # Flatten -> FC layer (dots)
    fx = 500
    c.text_c(fx + 20, 100, "Fully", BLACK, 1)
    c.text_c(fx + 20, 114, "Connected", BLACK, 1)
    for k in range(8):
        c.circle(fx + 20, 135 + k * 18, 6, PURPLE, LIGHT_PURPLE)
    c.arrow(prev_c[0], prev_c[1], fx + 10, 180, GRAY, 2, 7)

    # Output
    ox = 620
    c.rect(ox, 140, ox + 150, 180, RED, LIGHT_RED)
    c.text_c(ox + 75, 152, "Abnormal: 0.94", BLACK, 1)
    c.rect(ox, 190, ox + 150, 230, MED_GREEN, LIGHT_GREEN)
    c.text_c(ox + 75, 202, "Normal: 0.06", BLACK, 1)
    c.text_c(ox + 75, 240, "Diagnostic Output", BLACK, 1)
    for k in range(8):
        c.line(fx + 26, 135 + k * 18, ox - 2, 170, LIGHT_GRAY, 1)
    c.arrow(fx + 40, 180, ox - 2, 175, GRAY, 2, 7)

    c.text_c(410, 400, "Figure 3: Raw pixels pass through convolutional layers to a diagnostic prediction", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3.png'))
    print("  Figure_3.png done")


def fig4_rl():
    """Figure 4: Reinforcement learning cycle in a clinical context."""
    c = PNGCanvas(760, 430)
    c.text_c(380, 12, "Reinforcement Learning in a Clinical Context", BLACK, 2)

    # Agent box (left)
    c.rect(70, 150, 250, 250, DARK_BLUE, PALE_BLUE)
    c.text_c(160, 185, "AGENT", BLACK, 2)
    c.text_c(160, 212, "(learned policy)", BLACK, 1)

    # Environment box (right)
    c.rect(510, 150, 700, 250, DARK_GREEN, LIGHT_GREEN)
    c.text_c(605, 185, "ENVIRONMENT", BLACK, 1)
    c.text_c(605, 212, "(patient state)", BLACK, 1)

    # Action arrow (top: agent -> env)
    c.arrow(250, 175, 510, 175, ORANGE, 3, 12)
    c.text_c(380, 150, "Action: treatment / dose", ORANGE, 1)

    # State + reward arrows (bottom: env -> agent)
    c.arrow(510, 225, 250, 225, PURPLE, 3, 12)
    c.text_c(380, 255, "New state + Reward (outcome)", PURPLE, 1)

    # Reward detail box
    c.rect(300, 300, 460, 360, GOLD, LIGHT_GOLD)
    c.text_c(380, 315, "Reward reflects", BLACK, 1)
    c.text_c(380, 331, "long-term patient", BLACK, 1)
    c.text_c(380, 347, "outcome", BLACK, 1)

    # loop hint arrows
    c.arrow(160, 250, 160, 300, GRAY, 2, 8)
    c.text(60, 300, "policy update", GRAY, 1)
    c.arrow(605, 300, 605, 252, GRAY, 2, 8)
    c.text(560, 305, "state evolves", GRAY, 1)

    c.text_c(380, 400, "Figure 4: The agent-environment loop optimizing long-horizon clinical outcomes", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4.png'))
    print("  Figure_4.png done")


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Chapter 2 figures...")
    fig1_workflow()
    fig2_supervised()
    fig3_cnn()
    fig4_rl()
    print("All figures generated in", OUTPUT_DIR)
