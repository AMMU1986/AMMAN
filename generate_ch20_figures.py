#!/usr/bin/env python3
"""
Generate 4 scientific figures (PNG) for Chapter 20:
Future of AI-Driven Pharmacology and Biomedical Engineering.

Reuses the pure-standard-library PNGCanvas drawing library from
generate_figures.py (no matplotlib / PIL required).
"""

import os
import math
import importlib.util

# ─── Import PNGCanvas + colors + font from existing repo module ───
_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "genfigs", os.path.join(_here, "generate_figures.py"))
_gf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gf)

PNGCanvas = _gf.PNGCanvas
DARK_BLUE = _gf.DARK_BLUE
MED_BLUE = _gf.MED_BLUE
LIGHT_BLUE = _gf.LIGHT_BLUE
PALE_BLUE = _gf.PALE_BLUE
DARK_GREEN = _gf.DARK_GREEN
MED_GREEN = _gf.MED_GREEN
LIGHT_GREEN = _gf.LIGHT_GREEN
ORANGE = _gf.ORANGE
LIGHT_ORANGE = _gf.LIGHT_ORANGE
RED = _gf.RED
LIGHT_RED = _gf.LIGHT_RED
PURPLE = _gf.PURPLE
LIGHT_PURPLE = _gf.LIGHT_PURPLE
GOLD = _gf.GOLD
LIGHT_GOLD = _gf.LIGHT_GOLD
GRAY = _gf.GRAY
LIGHT_GRAY = _gf.LIGHT_GRAY
BLACK = _gf.BLACK
WHITE = _gf.WHITE

OUTPUT_DIR = os.path.join(_here, "ch20_figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fig1_autonomous_discovery_loop():
    """Figure 1: Closed-loop autonomous drug discovery pipeline."""
    c = PNGCanvas(760, 460)
    c.text_c(380, 10, "Autonomous Closed-Loop Drug Discovery Pipeline", BLACK, 2)

    boxes = [
        ("Target ID", 40, 90, DARK_BLUE, PALE_BLUE),
        ("Generative", 250, 60, MED_BLUE, LIGHT_BLUE),
        ("Molecule Design", 250, 60, MED_BLUE, LIGHT_BLUE),
        ("ADMET Predict", 500, 90, DARK_GREEN, LIGHT_GREEN),
        ("Robotic Synth", 560, 270, ORANGE, LIGHT_ORANGE),
        ("Bio Assay", 300, 350, PURPLE, LIGHT_PURPLE),
        ("Active Learn", 50, 290, RED, LIGHT_RED),
    ]
    # Use 6 distinct nodes around a cycle
    nodes = [
        ("Target ID", 60, 95, DARK_BLUE, PALE_BLUE),
        ("Generative Design", 290, 70, MED_BLUE, LIGHT_BLUE),
        ("ADMET Predict", 520, 95, DARK_GREEN, LIGHT_GREEN),
        ("Robotic Synthesis", 540, 300, ORANGE, LIGHT_ORANGE),
        ("Bioassay + QC", 290, 360, PURPLE, LIGHT_PURPLE),
        ("Active Learning", 60, 300, RED, LIGHT_RED),
    ]
    bw, bh = 170, 52
    centers = []
    for label, bx, by, col, fill in nodes:
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        c.text_c(bx + bw // 2, by + bh // 2 - 4, label, BLACK, 1)
        centers.append((bx + bw // 2, by + bh // 2))

    pairs = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]
    for i, j in pairs:
        x1, y1 = centers[i]
        x2, y2 = centers[j]
        dx, dy = x2 - x1, y2 - y1
        d = math.sqrt(dx * dx + dy * dy)
        if d > 0:
            off = 98
            c.arrow(int(x1 + dx / d * off), int(y1 + dy / d * off),
                    int(x2 - dx / d * off), int(y2 - dy / d * off), GRAY, 2, 9)

    # center hub
    c.rect(300, 195, 470, 250, GOLD, LIGHT_GOLD)
    c.text_c(385, 210, "AI Decision", BLACK, 1)
    c.text_c(385, 228, "Engine (RL)", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_20_1_Discovery_Loop.png"))


def fig2_bar_timeline():
    """Figure 2: Comparison of discovery timeline conventional vs AI-driven."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Preclinical Timeline: Conventional vs AI-Driven", BLACK, 2)

    # plot area
    x0, y0 = 90, 400
    x1, y1 = 720, 60
    c.line(x0, y0, x1, y0, BLACK, 2)   # x axis
    c.line(x0, y0, x0, y1, BLACK, 2)   # y axis
    c.text(20, 210, "Months", BLACK, 1)

    # y gridlines (0..60 months)
    ymax = 60
    for v in range(0, ymax + 1, 10):
        yy = int(y0 - (y0 - y1) * v / ymax)
        c.hline(x0, x1, yy, LIGHT_GRAY)
        c.text(55, yy - 3, str(v), BLACK, 1)

    stages = ["Target", "Hit", "Lead", "Opt", "Cand"]
    conv = [12, 14, 16, 12, 8]
    ai = [4, 5, 6, 5, 3]
    group_w = (x1 - x0) // len(stages)
    bw = 34
    for k, st in enumerate(stages):
        gx = x0 + k * group_w + 25
        # conventional
        hc = int((y0 - y1) * conv[k] / ymax)
        c.rect(gx, y0 - hc, gx + bw, y0, DARK_BLUE, MED_BLUE)
        c.text_c(gx + bw // 2, y0 - hc - 12, str(conv[k]), BLACK, 1)
        # ai-driven
        ha = int((y0 - y1) * ai[k] / ymax)
        c.rect(gx + bw + 6, y0 - ha, gx + 2 * bw + 6, y0, DARK_GREEN, MED_GREEN)
        c.text_c(gx + bw + 6 + bw // 2, y0 - ha - 12, str(ai[k]), BLACK, 1)
        c.text_c(gx + bw + 3, y0 + 12, st, BLACK, 1)

    # legend
    c.rect(500, 70, 520, 86, DARK_BLUE, MED_BLUE)
    c.text(526, 74, "Conventional", BLACK, 1)
    c.rect(500, 95, 520, 111, DARK_GREEN, MED_GREEN)
    c.text(526, 99, "AI-Driven", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_20_2_Timeline.png"))


def fig3_smart_delivery():
    """Figure 3: Self-optimizing closed-loop drug delivery device architecture."""
    c = PNGCanvas(760, 440)
    c.text_c(380, 10, "Self-Optimizing Closed-Loop Drug Delivery Device", BLACK, 2)

    layers = [
        ("Biosensors", 40, 70, DARK_BLUE, PALE_BLUE,
         "glucose / biomarker / EIS"),
        ("Edge AI Controller", 40, 175, DARK_GREEN, LIGHT_GREEN,
         "on-device model + safety"),
        ("Micro-Actuator / Pump", 40, 280, ORANGE, LIGHT_ORANGE,
         "dose modulation"),
    ]
    bw, bh = 260, 70
    cy = []
    for label, bx, by, col, fill, sub in layers:
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        c.text_c(bx + bw // 2, by + 16, label, BLACK, 1)
        c.text_c(bx + bw // 2, by + 40, sub, GRAY, 1)
        cy.append((bx + bw, by + bh // 2))

    # feedback arrows down and up
    c.arrow(170, 140, 170, 175, GRAY, 2, 8)
    c.arrow(170, 245, 170, 280, GRAY, 2, 8)
    c.arrow(230, 315, 300, 315, PURPLE, 2, 9)
    c.text(250, 322, "drug -> body", PURPLE, 1)

    # patient / body block
    c.circle(500, 210, 70, DARK_BLUE, LIGHT_BLUE)
    c.text_c(500, 200, "Patient", BLACK, 1)
    c.text_c(500, 218, "Physiology", BLACK, 1)
    # feedback loop back to sensors
    c.arrow(500, 138, 300, 105, RED, 2, 9)
    c.text(330, 90, "physiological feedback", RED, 1)

    # cloud twin
    c.rect(560, 320, 720, 390, PURPLE, LIGHT_PURPLE)
    c.text_c(640, 340, "Cloud Digital", BLACK, 1)
    c.text_c(640, 360, "Twin + Update", BLACK, 1)
    c.arrow(570, 250, 610, 320, GRAY, 2, 8)
    c.save(os.path.join(OUTPUT_DIR, "Figure_20_3_Smart_Delivery.png"))


def fig4_adoption_radar():
    """Figure 4: Readiness of pillars toward autonomous, personalized healthcare."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Readiness of Autonomous Healthcare Enablers", BLACK, 2)

    x0, y0 = 110, 410
    x1, y1 = 720, 70
    c.line(x0, y0, x1, y0, BLACK, 2)
    c.line(x0, y0, x0, y1, BLACK, 2)
    c.text(20, 220, "TRL (1-9)", BLACK, 1)

    ymax = 9
    for v in range(0, ymax + 1, 1):
        yy = int(y0 - (y0 - y1) * v / ymax)
        if v % 1 == 0:
            c.hline(x0, x1, yy, LIGHT_GRAY)
            c.text(85, yy - 3, str(v), BLACK, 1)

    labels = ["GenMol", "DigTwin", "SmartDev", "FedLrn", "Regul", "ClinInt"]
    vals = [6, 5, 6, 5, 3, 4]
    cols = [DARK_BLUE, DARK_GREEN, ORANGE, PURPLE, RED, GOLD]
    fills = [MED_BLUE, MED_GREEN, LIGHT_ORANGE, LIGHT_PURPLE, LIGHT_RED, LIGHT_GOLD]
    group_w = (x1 - x0) // len(labels)
    bw = 46
    for k, lab in enumerate(labels):
        gx = x0 + k * group_w + 18
        h = int((y0 - y1) * vals[k] / ymax)
        c.rect(gx, y0 - h, gx + bw, y0, cols[k], fills[k])
        c.text_c(gx + bw // 2, y0 - h - 12, str(vals[k]), BLACK, 1)
        c.text_c(gx + bw // 2, y0 + 12, lab, BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_20_4_Readiness.png"))


if __name__ == "__main__":
    fig1_autonomous_discovery_loop()
    fig2_bar_timeline()
    fig3_smart_delivery()
    fig4_adoption_radar()
    for f in sorted(os.listdir(OUTPUT_DIR)):
        p = os.path.join(OUTPUT_DIR, f)
        print(f"{f}: {os.path.getsize(p)/1024:.1f} KB")
