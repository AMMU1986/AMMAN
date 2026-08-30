#!/usr/bin/env python3
"""
Generate 4 figure images (PNG) for the chapter
"Smart Biomaterials and Drug-Eluting Medical Devices".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - Classification and design landscape of smart biomaterials
  Figure 2 - Architecture and release mechanisms of a drug-eluting implant
  Figure 3 - In-vitro drug-release kinetics for different reservoir designs
  Figure 4 - AI-driven closed-loop design/optimization workflow for smart
             biomaterials
"""

import os
import math
import random

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

OUTPUT_DIR = '/projects/sandbox/AMMAN/biomaterials_figures'


def gen_fig1():
    """Figure 1: Classification / design landscape of smart biomaterials."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 8, "Classification and Design Landscape of Smart Biomaterials", BLACK, 2)

    # Central hub
    c.rect(300, 200, 460, 260, DARK_BLUE, PALE_BLUE)
    c.text_c(380, 218, "SMART", BLACK, 2)
    c.text_c(380, 238, "BIOMATERIALS", BLACK, 1)

    # Four surrounding categories
    cats = [
        ("Stimuli-Responsive", 40, 60, MED_BLUE, LIGHT_BLUE,
         ["pH / temperature", "enzyme / redox", "light / magnetic"]),
        ("Bioresorbable", 520, 60, DARK_GREEN, LIGHT_GREEN,
         ["PLGA / PLA / PCL", "Mg alloys", "controlled erosion"]),
        ("Bioactive / Osteo", 40, 340, ORANGE, LIGHT_ORANGE,
         ["bioactive glass", "hydroxyapatite", "growth factors"]),
        ("Self-Healing / Shape", 520, 340, PURPLE, LIGHT_PURPLE,
         ["shape memory", "hydrogels", "reversible bonds"]),
    ]
    box_centers = []
    for label, bx, by, col, fill, items in cats:
        c.rect(bx, by, bx+200, by+95, col, fill)
        c.text_c(bx+100, by+10, label, BLACK, 1)
        for k, it in enumerate(items):
            c.text(bx+12, by+32 + k*17, "- " + it, GRAY, 1)
        box_centers.append((bx+100, by+47))

    hub = (380, 230)
    for cx, cy in box_centers:
        dx, dy = hub[0]-cx, hub[1]-cy
        d = math.sqrt(dx*dx + dy*dy)
        c.arrow(int(cx + dx/d*70), int(cy + dy/d*40),
                int(hub[0] - dx/d*95), int(hub[1] - dy/d*40), GRAY, 2, 8)

    # Property band at bottom
    c.rect(30, 445, 730, 465, LIGHT_GRAY, (245, 245, 245))
    c.text_c(380, 451, "Key design targets: biocompatibility  -  degradation rate  -  mechanical match  -  controlled release", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Smart_Biomaterials_Classification.png'))
    print("  Figure_1 done")


def gen_fig2():
    """Figure 2: Architecture and release mechanisms of a drug-eluting implant."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 8, "Architecture of a Drug-Eluting Implant", BLACK, 2)

    # (a) Cross-section of a coated stent strut
    c.text(25, 35, "(a) Drug-Eluting Coating Cross-Section", BLACK, 1)
    # metal substrate
    c.fill_rect(60, 120, 340, 175, GRAY)
    c.text_c(200, 143, "Metal / Polymer Substrate", WHITE, 1)
    # primer
    c.fill_rect(60, 105, 340, 120, MED_BLUE)
    c.text(64, 108, "Primer layer", WHITE, 1)
    # drug-polymer matrix
    c.fill_rect(60, 70, 340, 105, LIGHT_ORANGE)
    c.text(64, 74, "Drug + polymer matrix", BLACK, 1)
    # drug particles
    random.seed(3)
    for _ in range(40):
        px = random.randint(70, 330)
        py = random.randint(78, 100)
        c.circle(px, py, 2, RED, RED)
    # topcoat
    c.fill_rect(60, 58, 340, 70, LIGHT_GREEN)
    c.text(64, 59, "Diffusion topcoat", BLACK, 1)
    # release arrows
    for ax in range(90, 340, 45):
        c.arrow(ax, 58, ax, 40, RED, 1, 5)
    c.text(140, 28, "Drug release to tissue", RED, 1)

    # (b) Release mechanisms
    c.text(400, 35, "(b) Release Mechanisms", BLACK, 1)
    mechs = [
        ("Diffusion", MED_BLUE, LIGHT_BLUE),
        ("Polymer erosion", DARK_GREEN, LIGHT_GREEN),
        ("Osmotic pumping", ORANGE, LIGHT_ORANGE),
        ("Stimuli-triggered", PURPLE, LIGHT_PURPLE),
    ]
    for i, (label, col, fill) in enumerate(mechs):
        by = 60 + i*38
        c.rect(400, by, 720, by+30, col, fill)
        c.text(410, by+10, label, BLACK, 1)

    # (c) Device family
    c.text(25, 200, "(c) Representative Device Platforms", BLACK, 1)
    devs = [
        ("Drug-Eluting\nStent", 60, MED_BLUE, LIGHT_BLUE),
        ("Ocular\nImplant", 235, DARK_GREEN, LIGHT_GREEN),
        ("Orthopedic\nCoating", 410, ORANGE, LIGHT_ORANGE),
        ("Contraceptive /\nDepot", 585, PURPLE, LIGHT_PURPLE),
    ]
    for label, bx, col, fill in devs:
        c.rect(bx, 225, bx+140, 300, col, fill)
        parts = label.split("\n")
        for k, p in enumerate(parts):
            c.text_c(bx+70, 245 + k*16, p, BLACK, 1)

    # (d) Timeline of dose
    c.text(25, 320, "(d) Idealized Therapeutic Window vs Time", BLACK, 1)
    c.vline(60, 340, 445, BLACK)
    c.hline(60, 720, 445, BLACK)
    c.text(25, 340, "Conc", BLACK, 1)
    c.text(660, 450, "Time", BLACK, 1)
    # therapeutic band
    for x in range(60, 720):
        c.pixel(x, 375, MED_GREEN)
        c.pixel(x, 420, MED_GREEN)
    c.text(600, 362, "Toxic", RED, 1)
    c.text(600, 425, "Sub-therapeutic", GRAY, 1)
    # burst then plateau (bad) vs controlled (good)
    for x in range(60, 720):
        t = (x-60)/660.0
        yb = int(445 - 250*math.exp(-6*t) - 10)
        c.pixel(x, yb, RED); c.pixel(x, yb+1, RED)
        yc = int(445 - 70 - 20*math.sin(t*3) if False else 445 - 78 - 8*math.sin(t*6))
        yc = int(400 - 8*math.sin(t*6))
        c.pixel(x, yc, MED_BLUE); c.pixel(x, yc+1, MED_BLUE)
    c.hline(500, 530, 335, RED); c.text(535, 332, "Burst (uncontrolled)", BLACK, 1)
    c.hline(500, 530, 348, MED_BLUE); c.text(535, 345, "Controlled release", BLACK, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Drug_Eluting_Implant_Architecture.png'))
    print("  Figure_2 done")


def gen_fig3():
    """Figure 3: In-vitro drug-release kinetics for different reservoir designs."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 8, "In-Vitro Cumulative Drug-Release Kinetics", BLACK, 2)

    # Axes
    ox, oy = 80, 400
    c.vline(ox, 50, oy, BLACK)
    c.hline(ox, 700, oy, BLACK)
    c.text_c(390, 445, "Time (days)", BLACK, 1)
    # y label
    for k, ch in enumerate("Release (%)"):
        c.text(25, 130 + k*14, ch, BLACK, 1)
    # gridlines and y ticks
    for pct in range(0, 101, 20):
        gy = oy - int(pct/100.0 * (oy-60))
        c.hline(ox, 700, gy, LIGHT_GRAY)
        c.text(50, gy-3, f"{pct}", BLACK, 1)
    for d in range(0, 61, 10):
        gx = ox + int(d/60.0 * (700-ox))
        c.vline(gx, 50, oy, LIGHT_GRAY)
        c.text_c(gx, oy+6, f"{d}", BLACK, 1)
    # redraw axes on top
    c.vline(ox, 50, oy, BLACK)
    c.hline(ox, 700, oy, BLACK)

    def plot_curve(fn, color, thick=2):
        prev = None
        for px in range(ox, 701):
            t = (px-ox)/(700-ox) * 60.0
            val = fn(t)
            py = oy - int(val/100.0 * (oy-60))
            if prev is not None:
                c.line(prev[0], prev[1], px, py, color, thick)
            prev = (px, py)

    # Zero-order (linear reservoir)
    plot_curve(lambda t: min(100, 1.7*t), MED_BLUE)
    # First-order / matrix (Higuchi sqrt)
    plot_curve(lambda t: min(100, 13.5*math.sqrt(t)), DARK_GREEN)
    # Burst + plateau
    plot_curve(lambda t: min(100, 45*(1-math.exp(-1.5*t)) + 0.6*t), ORANGE)
    # Stimuli-triggered pulsatile (step-like)
    def pulsatile(t):
        base = 10*math.floor(t/12.0) * 1.0
        ramp = 8*(t % 12)/12.0
        return min(100, base + ramp + 5)
    plot_curve(lambda t: pulsatile(t), PURPLE)

    # Legend
    leg = [("Zero-order reservoir", MED_BLUE),
           ("Higuchi matrix (sqrt-t)", DARK_GREEN),
           ("Burst then plateau", ORANGE),
           ("Stimuli-triggered pulsatile", PURPLE)]
    for i, (lbl, col) in enumerate(leg):
        ly = 70 + i*20
        c.hline(500, 540, ly, col)
        c.hline(500, 540, ly+1, col)
        c.text(548, ly-3, lbl, BLACK, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Drug_Release_Kinetics.png'))
    print("  Figure_3 done")


def gen_fig4():
    """Figure 4: AI-driven closed-loop design/optimization workflow."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 8, "AI-Driven Closed-Loop Design of Smart Biomaterials", BLACK, 2)

    boxes = [
        ("Data & Descriptors", 60, 70, DARK_BLUE, PALE_BLUE,
         ["composition, MW", "porosity, modulus", "in-vitro assays"]),
        ("ML / DL Models", 300, 55, MED_BLUE, LIGHT_BLUE,
         ["RF / XGBoost", "GNN, transformers", "surrogate models"]),
        ("Property Prediction", 545, 70, DARK_GREEN, LIGHT_GREEN,
         ["release profile", "degradation", "biocompatibility"]),
        ("Multi-Objective Opt.", 545, 250, ORANGE, LIGHT_ORANGE,
         ["Bayesian opt.", "genetic algo.", "Pareto fronts"]),
        ("Generative / Inverse", 300, 330, PURPLE, LIGHT_PURPLE,
         ["VAE / GAN / diffusion", "candidate design", "constraints"]),
        ("Synthesis & Validation", 60, 250, RED, LIGHT_RED,
         ["fabrication", "in-vitro / in-vivo", "characterization"]),
    ]
    bw, bh = 170, 78
    centers = []
    for label, bx, by, col, fill, items in boxes:
        c.rect(bx, by, bx+bw, by+bh, col, fill)
        c.text_c(bx+bw//2, by+8, label, BLACK, 1)
        for k, it in enumerate(items):
            c.text(bx+10, by+28 + k*15, "- " + it, GRAY, 1)
        centers.append((bx+bw//2, by+bh//2))

    order = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]
    for i, j in order:
        x1, y1 = centers[i]; x2, y2 = centers[j]
        dx, dy = x2-x1, y2-y1
        d = math.sqrt(dx*dx+dy*dy)
        off1, off2 = 95, 100
        c.arrow(int(x1+dx/d*off1), int(y1+dy/d*45),
                int(x2-dx/d*off2), int(y2-dy/d*45), GRAY, 2, 8)

    # Center loop label
    c.rect(320, 175, 440, 215, GOLD, LIGHT_GOLD)
    c.text_c(380, 185, "Active Learning", BLACK, 1)
    c.text_c(380, 198, "Feedback Loop", BLACK, 1)

    c.text(60, 445, "Closed loop iterates until targets (efficacy, safety, degradation) are met", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_AI_Design_Workflow.png'))
    print("  Figure_4 done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating biomaterials figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print(f"\nAll figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz/1024:.1f} KB")


if __name__ == '__main__':
    main()
