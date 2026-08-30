#!/usr/bin/env python3
"""
Generate 4 figures (PNG) for the chapter:
"Reporting CSR and ESG Performance: Leveraging AI for Sustainability Measurement".
Reuses the pure-stdlib PNGCanvas primitives from generate_figures.py
(no matplotlib / PIL required).
"""

import os
import math

# Reuse the proven pure-stdlib PNG canvas + font from the existing repo script.
from generate_figures import (
    PNGCanvas,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE, RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/csr_esg_figures'


def gen_fig1():
    """Figure 1: Architecture of an AI-enabled CSR/ESG measurement & reporting system."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "AI-Enabled CSR and ESG Measurement System", BLACK, 2)

    # Four horizontal layers (left to right pipeline)
    layers = [
        ("DATA SOURCES", 20, DARK_BLUE, PALE_BLUE,
         ["ERP systems", "IoT sensors", "Satellite data", "Documents", "Databases"]),
        ("INGESTION and", 200, MED_BLUE, LIGHT_BLUE,
         ["NLP extraction", "OCR parsing", "Data mapping", "Unit reconcile", "Validation"]),
        ("ANALYTICS", 390, DARK_GREEN, LIGHT_GREEN,
         ["ML prediction", "Risk scoring", "Benchmarking", "Carbon calc", "Anomaly det."]),
        ("REPORTING", 580, ORANGE, LIGHT_ORANGE,
         ["Dashboards", "GenAI reports", "Evidence link", "Assurance", "Disclosure"]),
    ]
    box_w = 160
    for i, (title, x, col, fill, items) in enumerate(layers):
        c.rect(x, 60, x + box_w, 90, col, col)
        # header label text in white-ish (use black for contrast on medium fills)
        subt = "INTEGRATION" if title.startswith("INGEST") else title
        c.text_c(x + box_w // 2, 68, subt, WHITE if col in (DARK_BLUE, DARK_GREEN) else BLACK, 1)
        # body box
        c.rect(x, 92, x + box_w, 360, col, fill)
        for j, it in enumerate(items):
            c.text(x + 12, 108 + j * 46, "- " + it, BLACK, 1)
        # arrow to next layer
        if i < len(layers) - 1:
            nx = layers[i + 1][1]
            c.arrow(x + box_w + 2, 210, nx - 2, 210, GRAY, 3, 10)

    # Governance / oversight band underneath
    c.rect(20, 380, 740, 420, GOLD, LIGHT_GOLD)
    c.text_c(380, 392, "Data Governance  Human Oversight  Explainability  Security", BLACK, 1)

    # Feedback loop arrow (reporting back to sources)
    c.line(660, 360, 660, 440, PURPLE, 2)
    c.line(660, 440, 100, 440, PURPLE, 2)
    c.arrow(100, 440, 100, 362, PURPLE, 2, 8)
    c.text_c(380, 448, "Continuous feedback and assurance loop", PURPLE, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_1.png'))
    print("  Figure_1.png done")


def gen_fig2():
    """Figure 2: AI measurement maturity vs environmental impact reduction."""
    c = PNGCanvas(720, 460)
    c.text_c(360, 10, "AI Measurement Maturity and Impact Reduction", BLACK, 2)

    ox, oy = 80, 360      # origin
    ax_w, ax_h = 560, 300
    # Axes
    c.line(ox, oy, ox + ax_w, oy, BLACK, 2)      # x
    c.line(ox, oy, ox, oy - ax_h, BLACK, 2)      # y
    c.text(ox + 150, oy + 30, "AI Measurement Maturity (level)", BLACK, 1)
    # y label (vertical-ish, stacked)
    for k, ch in enumerate("IMPACT"):
        c.text(18, oy - ax_h + 30 + k * 16, ch, BLACK, 1)
    c.text(70, 36, "Impact reduction (%)", BLACK, 1)

    # y gridlines/labels
    for v in range(0, 6):
        yy = oy - int(v / 5 * ax_h)
        c.hline(ox, ox + ax_w, yy, LIGHT_GRAY)
        c.text(45, yy - 4, str(v * 10), BLACK, 1)
    # x labels (maturity levels 1..5)
    levels = ["L1", "L2", "L3", "L4", "L5"]
    for i, lv in enumerate(levels):
        xx = ox + int((i + 0.5) / 5 * ax_w)
        c.text_c(xx, oy + 10, lv, BLACK, 1)

    # Curve: impact reduction rising with maturity (diminishing then compounding)
    pts = [(0.5, 8), (1.5, 18), (2.5, 30), (3.5, 42), (4.5, 50)]
    prev = None
    for (mx, red) in pts:
        px = ox + int(mx / 5 * ax_w)
        py = oy - int(red / 50 * ax_h)
        if prev:
            c.line(prev[0], prev[1], px, py, MED_BLUE, 3)
        c.circle(px, py, 6, DARK_BLUE, MED_BLUE)
        c.text_c(px, py - 20, str(red) + "%", DARK_BLUE, 1)
        prev = (px, py)

    # Shaded band showing measurement-accuracy improvement (secondary series)
    prev = None
    acc = [(0.5, 6), (1.5, 14), (2.5, 26), (3.5, 40), (4.5, 47)]
    for (mx, a) in acc:
        px = ox + int(mx / 5 * ax_w)
        py = oy - int(a / 50 * ax_h)
        if prev:
            c.line(prev[0], prev[1], px, py, ORANGE, 2)
        prev = (px, py)

    # Legend
    c.hline(500, 540, 70, MED_BLUE)
    c.text(548, 64, "Impact reduction", BLACK, 1)
    c.hline(500, 540, 90, ORANGE)
    c.text(548, 84, "Measurement accuracy", BLACK, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_2.png'))
    print("  Figure_2.png done")


def gen_fig3():
    """Figure 3: AI-based greenwashing detection and assurance framework."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "AI-Based Greenwashing Detection and Assurance", BLACK, 2)

    # Center: claims under test
    c.rect(300, 200, 460, 270, PURPLE, LIGHT_PURPLE)
    c.text_c(380, 220, "Corporate", BLACK, 1)
    c.text_c(380, 234, "Sustainability", BLACK, 1)
    c.text_c(380, 248, "Claims", BLACK, 1)

    # Evidence sources feeding cross-validation
    sources = [
        ("Satellite and", "remote sensing", 40, 60, DARK_GREEN, LIGHT_GREEN),
        ("IoT sensor", "readings", 40, 330, MED_BLUE, LIGHT_BLUE),
        ("Third-party", "databases", 560, 60, ORANGE, LIGHT_ORANGE),
        ("Operational and", "financial data", 560, 330, GOLD, LIGHT_GOLD),
    ]
    for (l1, l2, x, y, col, fill) in sources:
        c.rect(x, y, x + 160, y + 70, col, fill)
        c.text_c(x + 80, y + 22, l1, BLACK, 1)
        c.text_c(x + 80, y + 40, l2, BLACK, 1)

    # NLP analyzer box (top center)
    c.rect(300, 90, 460, 150, DARK_BLUE, PALE_BLUE)
    c.text_c(380, 104, "NLP Claim", BLACK, 1)
    c.text_c(380, 120, "Analyzer", BLACK, 1)
    c.arrow(380, 150, 380, 198, GRAY, 2, 8)

    # Arrows from sources into cross-validation engine
    c.arrow(200, 95, 298, 205, GRAY, 2, 8)
    c.arrow(200, 365, 298, 265, GRAY, 2, 8)
    c.arrow(560, 95, 462, 205, GRAY, 2, 8)
    c.arrow(560, 365, 462, 265, GRAY, 2, 8)

    # Output: assurance decision
    c.rect(300, 320, 460, 400, RED, LIGHT_RED)
    c.text_c(380, 336, "Cross-Validation", BLACK, 1)
    c.text_c(380, 352, "and Consistency", BLACK, 1)
    c.text_c(380, 368, "Assessment", BLACK, 1)
    c.arrow(380, 270, 380, 318, GRAY, 2, 8)

    # Verdict labels
    c.text_c(380, 420, "Verified   |   Flagged for review   |   Greenwashing risk", BLACK, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_3.png'))
    print("  Figure_3.png done")


def gen_fig4():
    """Figure 4: Maturity continuum of AI-enabled CSR/ESG measurement."""
    c = PNGCanvas(780, 470)
    c.text_c(390, 10, "Maturity Continuum of AI-Enabled ESG Measurement", BLACK, 2)

    stages = [
        ("Level 1", "Manual and", "compliance", DARK_BLUE, PALE_BLUE),
        ("Level 2", "Automated", "data capture", MED_BLUE, LIGHT_BLUE),
        ("Level 3", "Predictive", "analytics", MED_GREEN, LIGHT_GREEN),
        ("Level 4", "Integrated", "intelligence", ORANGE, LIGHT_ORANGE),
        ("Level 5", "Autonomous and", "continuous", PURPLE, LIGHT_PURPLE),
    ]
    # ascending "staircase" of boxes
    bw, bh = 130, 70
    base_y = 340
    step = 40
    for i, (lv, l1, l2, col, fill) in enumerate(stages):
        x = 30 + i * 148
        y = base_y - i * step
        c.rect(x, y, x + bw, y + bh, col, fill)
        c.text_c(x + bw // 2, y + 12, lv, BLACK, 1)
        c.text_c(x + bw // 2, y + 34, l1, BLACK, 1)
        c.text_c(x + bw // 2, y + 50, l2, BLACK, 1)
        if i < len(stages) - 1:
            nx = 30 + (i + 1) * 148
            ny = base_y - (i + 1) * step
            c.arrow(x + bw, y + 10, nx, ny + bh - 10, GRAY, 2, 8)

    # ascending axis arrows
    c.arrow(20, base_y + bh + 8, 760, base_y + bh + 8, BLACK, 2, 10)
    c.text(280, base_y + bh + 16, "Increasing capability and decision value", BLACK, 1)
    c.arrow(20, base_y + bh + 4, 20, 70, BLACK, 2, 10)
    for k, ch in enumerate("VALUE"):
        c.text(4, 120 + k * 16, ch, BLACK, 1)

    # governance note
    c.text_c(390, base_y + bh + 32, "Each level requires matching data governance, skills, and oversight", GRAY, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_4.png'))
    print("  Figure_4.png done")


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating CSR/ESG figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print("All figures generated in", OUTPUT_DIR)
