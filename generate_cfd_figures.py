#!/usr/bin/env python3
"""
Generate 4 scientific figures (PNG) for Chapter 12:
Computational Fluid Dynamics and AI in Drug Delivery.

Reuses the pure-Python PNGCanvas class from generate_figures.py
(matplotlib is unavailable in this sandbox).
"""

import os
import math
import random

# Reuse the proven canvas + font + colors from the existing figure module.
from generate_figures import (
    PNGCanvas,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE, RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/cfd_figures'


def fig1_airway_deposition():
    """Figure 1: Respiratory tract model with deposition mechanisms + regional profile."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 8, "Airway Model and Regional Drug Deposition", BLACK, 2)

    # (a) Schematic airway tree with deposition mechanisms
    c.text(20, 34, "(a) Deposition Mechanisms in the Airways", BLACK, 1)

    # Trachea
    c.rect(70, 55, 110, 130, DARK_BLUE, PALE_BLUE)
    c.text_c(90, 88, "Tra", BLACK, 1)
    # bifurcation to two bronchi
    c.line(90, 130, 60, 175, MED_BLUE, 3)
    c.line(90, 130, 130, 175, MED_BLUE, 3)
    c.rect(40, 175, 75, 235, MED_BLUE, LIGHT_BLUE)
    c.rect(115, 175, 150, 235, MED_BLUE, LIGHT_BLUE)
    # smaller airways
    c.line(57, 235, 45, 275, MED_GREEN, 2)
    c.line(57, 235, 72, 275, MED_GREEN, 2)
    c.line(132, 235, 118, 275, MED_GREEN, 2)
    c.line(132, 235, 148, 275, MED_GREEN, 2)
    # alveoli
    for cx in (45, 72, 118, 148):
        c.circle(cx, 292, 9, DARK_GREEN, LIGHT_GREEN)

    # Impaction (large particle hitting bend)
    c.circle(120, 150, 5, RED, LIGHT_RED)
    c.arrow(105, 138, 122, 152, RED, 2, 6)
    c.text(155, 145, "Impaction", RED, 1)
    c.text(155, 158, "(>5 micron)", GRAY, 1)
    # Sedimentation
    c.circle(70, 250, 4, ORANGE, LIGHT_ORANGE)
    c.arrow(70, 240, 70, 258, ORANGE, 2, 6)
    c.text(160, 235, "Sedimentation", ORANGE, 1)
    c.text(160, 248, "(1-5 micron)", GRAY, 1)
    # Diffusion
    c.circle(148, 292, 3, PURPLE, LIGHT_PURPLE)
    c.text(160, 285, "Diffusion", PURPLE, 1)
    c.text(160, 298, "(<1 micron)", GRAY, 1)

    # inhaled flow arrow
    c.arrow(90, 45, 90, 55, DARK_BLUE, 2, 6)
    c.text(100, 40, "Inhaled aerosol", DARK_BLUE, 1)

    # velocity streamlines (decorative)
    for i, y in enumerate(range(70, 120, 12)):
        for x in range(72, 108):
            yy = y + int(3 * math.sin((x + i * 6) * 0.2))
            c.pixel(x, yy, LIGHT_GRAY)

    # (b) Regional deposition bar chart
    c.text(300, 34, "(b) Predicted Regional Deposition Fraction", BLACK, 1)
    c.vline(340, 55, 300, BLACK)
    c.hline(340, 730, 300, BLACK)
    c.text(305, 55, "%", BLACK, 1)
    regions = [("Mouth/", 32, RED), ("Central", 26, ORANGE),
               ("Small", 22, MED_GREEN), ("Alveolar", 20, DARK_GREEN)]
    labels2 = ["throat", "bronchi", "airways", "region"]
    for i, (name, val, col) in enumerate(regions):
        bx = 365 + i * 90
        bh = int(val / 40.0 * 240)
        c.rect(bx, 300 - bh, bx + 55, 300, BLACK, col)
        c.text_c(bx + 27, 300 - bh - 12, f"{val}%", BLACK, 1)
        c.text_c(bx + 27, 305, name, BLACK, 1)
        c.text_c(bx + 27, 318, labels2[i], BLACK, 1)
    # y ticks
    for v, yy in [("40", 60), ("20", 180), ("0", 296)]:
        c.text(315, yy, v, BLACK, 1)

    # Deposition-vs-size curve inset
    c.text(300, 345, "Deposition vs particle size:", BLACK, 1)
    c.vline(340, 360, 445, BLACK)
    c.hline(340, 720, 445, BLACK)
    c.text(345, 448, "Particle diameter (micron)", BLACK, 1)
    for x in range(345, 715):
        t = (x - 345) / 370.0
        # bimodal-ish deposition curve
        y = int(440 - 70 * math.exp(-((t - 0.75) ** 2) / 0.03)
                - 45 * math.exp(-((t - 0.1) ** 2) / 0.01))
        c.pixel(x, y, MED_BLUE)
        c.pixel(x, y + 1, MED_BLUE)

    c.text(20, 455, "Figure 1: Airway deposition mechanisms and predicted regional deposition profile", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Airway_Deposition.png'))
    print("  Figure_1_Airway_Deposition.png done")


def fig2_arterial_wss():
    """Figure 2: Arterial bifurcation WSS distribution + near-wall nanoparticle accumulation."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 8, "Wall Shear Stress and Nanoparticle Accumulation", BLACK, 2)

    # (a) Bifurcation geometry with WSS color bands
    c.text(20, 34, "(a) Wall Shear Stress in a Bifurcating Artery", BLACK, 1)
    # parent vessel
    def band_color(level):
        # level 0 (low WSS) -> blue, high -> red
        table = [DARK_BLUE, MED_BLUE, LIGHT_BLUE, LIGHT_GREEN,
                 LIGHT_ORANGE, ORANGE, RED]
        return table[max(0, min(len(table) - 1, level))]

    # Draw parent trunk as stacked horizontal segments with varying WSS
    for i, x in enumerate(range(50, 200, 10)):
        lvl = 4 + (i % 3)
        c.fill_rect(x, 90, x + 10, 150, band_color(lvl))
    # bifurcation apex (high WSS)
    for x in range(200, 235):
        c.fill_rect(x, 90, x + 2, 150, band_color(6))
    # two daughter branches (upper & lower)
    for i, x in enumerate(range(235, 400, 10)):
        # inner wall high, outer wall low -> approximate with alternating
        c.fill_rect(x, 70 - i, x + 10, 112 - i, band_color(5 - (i % 4)))
        c.fill_rect(x, 128 + i, x + 10, 170 + i, band_color(2 + (i % 3)))
    # recirculation / low-WSS zones (outer walls)
    c.circle(300, 60, 12, DARK_BLUE, DARK_BLUE)
    c.circle(300, 185, 12, DARK_BLUE, DARK_BLUE)
    c.text(315, 52, "Low WSS", DARK_BLUE, 1)
    c.text(315, 180, "recirculation", DARK_BLUE, 1)
    c.text(205, 200, "Apex: high WSS", RED, 1)
    # flow arrow
    c.arrow(35, 120, 50, 120, BLACK, 2, 6)
    c.text(20, 108, "Flow", BLACK, 1)

    # WSS color legend
    c.text(560, 34, "WSS (Pa)", BLACK, 1)
    labels = ["High", "", "", "Mid", "", "", "Low"]
    for i in range(7):
        col = band_color(6 - i)
        c.fill_rect(560, 48 + i * 20, 590, 66 + i * 20, col)
        if labels[i]:
            c.text(596, 52 + i * 20, labels[i], BLACK, 1)

    # (b) Near-wall nanoparticle accumulation vs WSS
    c.text(20, 245, "(b) Near-Wall Nanoparticle Accumulation", BLACK, 1)
    c.vline(60, 265, 430, BLACK)
    c.hline(60, 420, 430, BLACK)
    c.text(20, 265, "Accum.", BLACK, 1)
    c.text(200, 435, "Wall shear stress", BLACK, 1)
    # accumulation is high at low WSS -> decreasing curve
    for x in range(65, 415):
        t = (x - 65) / 350.0
        y = int(420 - 140 * math.exp(-3.0 * t))
        c.pixel(x, y, RED)
        c.pixel(x, y + 1, RED)
    c.text(80, 290, "High accumulation", RED, 1)
    c.text(80, 303, "in low-WSS zones", GRAY, 1)

    # (c) particle margination sketch
    c.text(450, 245, "(c) Margination Toward Vessel Wall", BLACK, 1)
    c.rect(460, 270, 740, 430, GRAY, (245, 245, 250))
    # vessel walls
    c.hline(460, 740, 278, DARK_BLUE)
    c.hline(460, 740, 422, DARK_BLUE)
    c.text(465, 282, "Cell-free layer", MED_BLUE, 1)
    # red cells in core
    random.seed(3)
    for _ in range(24):
        rx = random.randint(480, 720)
        ry = random.randint(320, 380)
        c.circle(rx, ry, 6, RED, LIGHT_RED)
    # nanoparticles marginating to wall
    for _ in range(14):
        nx = random.randint(475, 725)
        ny = random.choice([random.randint(288, 305), random.randint(398, 415)])
        c.circle(nx, ny, 3, DARK_GREEN, MED_GREEN)
    c.text(560, 300, "Nanoparticles marginate", DARK_GREEN, 1)

    c.text(20, 455, "Figure 2: Arterial wall shear stress and near-wall nanoparticle accumulation", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_WSS_Nanoparticle.png'))
    print("  Figure_2_WSS_Nanoparticle.png done")


def fig3_surrogate_workflow():
    """Figure 3: CFD-ML surrogate workflow + computational time reduction."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 8, "CFD-Machine Learning Surrogate Workflow", BLACK, 2)

    # (a) Offline training pipeline
    c.text(20, 34, "(a) Offline: Build the Surrogate", BLACK, 1)
    boxes = [
        ("Sample design\nspace (LHS)", 30, MED_BLUE, LIGHT_BLUE),
        ("Run full CFD\nsimulations", 185, DARK_BLUE, PALE_BLUE),
        ("Extract quantities\nof interest", 340, ORANGE, LIGHT_ORANGE),
        ("Train ML\nsurrogate", 495, DARK_GREEN, LIGHT_GREEN),
    ]
    for label, bx, col, fill in boxes:
        c.rect(bx, 55, bx + 130, 110, col, fill)
        parts = label.split("\n")
        for k, p in enumerate(parts):
            c.text_c(bx + 65, 68 + k * 16, p, BLACK, 1)
    for bx in (160, 315, 470):
        c.arrow(bx, 82, bx + 25, 82, GRAY, 2, 7)
    # trained model output box
    c.rect(625, 55, 735, 110, GOLD, LIGHT_GOLD)
    c.text_c(680, 72, "Fast", BLACK, 1)
    c.text_c(680, 88, "surrogate", BLACK, 1)
    c.arrow(625, 82, 625, 82, GRAY, 2, 6)

    # (b) Online inference
    c.text(20, 135, "(b) Online: Query the Surrogate (milliseconds)", BLACK, 1)
    c.rect(40, 155, 150, 205, PURPLE, LIGHT_PURPLE)
    c.text_c(95, 168, "New patient /", BLACK, 1)
    c.text_c(95, 183, "design inputs", BLACK, 1)
    c.rect(300, 155, 410, 205, GOLD, LIGHT_GOLD)
    c.text_c(355, 172, "Surrogate", BLACK, 1)
    c.rect(560, 155, 700, 205, RED, LIGHT_RED)
    c.text_c(630, 168, "Prediction:", BLACK, 1)
    c.text_c(630, 183, "deposition, WSS", BLACK, 1)
    c.arrow(150, 180, 300, 180, MED_GREEN, 2, 8)
    c.arrow(410, 180, 560, 180, MED_GREEN, 2, 8)
    c.text(190, 165, "~ms", MED_GREEN, 1)

    # (c) computational time comparison (log-ish bars)
    c.text(20, 235, "(c) Computation Time per Prediction", BLACK, 1)
    c.vline(150, 255, 360, BLACK)
    c.hline(150, 720, 360, BLACK)
    items = [("Full CFD", 300, DARK_BLUE, "hours-days"),
             ("Reduced-order", 130, ORANGE, "seconds"),
             ("ML surrogate", 22, DARK_GREEN, "milliseconds")]
    for i, (name, blen, col, note) in enumerate(items):
        by = 275 + i * 30
        c.fill_rect(150, by, 150 + blen * 2, by + 20, col)
        c.text(155, by + 4, name, WHITE if blen > 60 else BLACK, 1)
        c.text(160 + blen * 2, by + 4, note, BLACK, 1)
    c.text(150, 372, "Bars illustrative (log scale); surrogate ~10^6x faster than full CFD", GRAY, 1)

    # (d) accuracy scatter (predicted vs CFD)
    c.text(20, 395, "(d) Surrogate accuracy vs CFD:", BLACK, 1)
    c.vline(260, 400, 455, BLACK)
    c.hline(260, 360, 455, BLACK)
    random.seed(11)
    for _ in range(30):
        t = random.random()
        px = int(260 + t * 95)
        py = int(455 - t * 50 + random.uniform(-3, 3))
        c.circle(px, py, 2, MED_BLUE, MED_BLUE)
    c.line(260, 455, 355, 405, RED, 1)
    c.text(365, 415, "y = x (ideal)", RED, 1)
    c.text(365, 430, "R-squared ~ 0.98", BLACK, 1)

    c.text(20, 460, "Figure 3: CFD-ML surrogate workflow and computational-time reduction", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Surrogate_Workflow.png'))
    print("  Figure_3_Surrogate_Workflow.png done")


def fig4_digital_twin():
    """Figure 4: Closed-loop CFD-AI digital twin architecture for personalized delivery."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 8, "Closed-Loop CFD-AI Digital Twin for Drug Delivery", BLACK, 2)

    # Central cycle of 4 boxes
    nodes = [
        ("PATIENT DATA", 60, 60, DARK_BLUE, PALE_BLUE,
         ["Imaging (CT/MRI)", "Physiological", "monitoring"]),
        ("CFD-AI MODEL", 500, 60, DARK_GREEN, LIGHT_GREEN,
         ["Surrogate +", "reduced-order", "transport model"]),
        ("PREDICTION", 500, 300, ORANGE, LIGHT_ORANGE,
         ["Drug distribution", "& concentration", "at target site"]),
        ("DOSING DECISION", 60, 300, RED, LIGHT_RED,
         ["Device settings,", "dose, timing", "recommendation"]),
    ]
    bw, bh = 200, 95
    centers = []
    for title, bx, by, col, fill, lines in nodes:
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        c.text_c(bx + bw // 2, by + 10, title, BLACK, 2)
        for k, ln in enumerate(lines):
            c.text_c(bx + bw // 2, by + 38 + k * 15, ln, BLACK, 1)
        centers.append((bx + bw // 2, by + bh // 2))

    # Arrows forming the loop (clockwise)
    c.arrow(260, 90, 500, 90, GRAY, 3, 10)      # data -> model
    c.text_c(380, 74, "assimilate", DARK_BLUE, 1)
    c.arrow(600, 155, 600, 300, GRAY, 3, 10)     # model -> prediction
    c.text(610, 220, "simulate", DARK_GREEN, 1)
    c.arrow(500, 347, 260, 347, GRAY, 3, 10)      # prediction -> decision
    c.text_c(380, 331, "optimize", ORANGE, 1)
    c.arrow(160, 300, 160, 155, GRAY, 3, 10)      # decision -> patient
    c.text(60, 220, "administer", RED, 1)

    # Center label
    c.rect(300, 175, 460, 225, GOLD, LIGHT_GOLD)
    c.text_c(380, 188, "Continuous", BLACK, 1)
    c.text_c(380, 203, "update loop", BLACK, 1)

    # Bottom benefits banner
    c.rect(60, 410, 700, 452, LIGHT_GRAY, (248, 248, 248))
    c.text(75, 418, "Personalized dosing", MED_BLUE, 1)
    c.text(280, 418, "Real-time adaptation", MED_GREEN, 1)
    c.text(500, 418, "Quantified uncertainty", PURPLE, 1)
    c.text(75, 434, "Patient-specific anatomy and physiology drive each recommendation", GRAY, 1)

    c.text(20, 462, "Figure 4: Architecture of a closed-loop CFD-AI digital twin for personalized drug delivery", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Digital_Twin.png'))
    print("  Figure_4_Digital_Twin.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Chapter 12 CFD figures...")
    fig1_airway_deposition()
    fig2_arterial_wss()
    fig3_surrogate_workflow()
    fig4_digital_twin()
    print(f"\nAll 4 figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz/1024:.1f} KB")


if __name__ == '__main__':
    main()
