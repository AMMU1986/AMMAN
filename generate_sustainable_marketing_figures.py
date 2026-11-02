#!/usr/bin/env python3
"""
Generate 4 figure images (PNG) for the chapter
"AI-Powered Digital Marketing for Sustainability" (Chapter ID ADSM-2).

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py.

Figures:
  Figure 1 - Conceptual model of responsible AI-driven sustainable marketing
  Figure 2 - AI technology pipeline: data -> AI -> applications -> outcomes
  Figure 3 - Double-edged sword: AI capabilities and corresponding risks
  Figure 4 - Responsible AI governance cycle for sustainable marketing
"""

import os
import math

from generate_figures import (
    PNGCanvas,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE,
    RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE,
    GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY,
    BLACK,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/sustainable_marketing_figures'


def box(c, x1, y1, x2, y2, outline, fill, title, lines=(), line_h=13):
    c.rect(x1, y1, x2, y2, outline, fill)
    cx = (x1 + x2) // 2
    c.text_c(cx, y1 + 8, title, BLACK, 1)
    for i, ln in enumerate(lines):
        c.text_c(cx, y1 + 26 + i * line_h, ln, BLACK, 1)


def gen_fig1():
    """Four-layer conceptual model with governance band and feedback loop."""
    c = PNGCanvas(820, 520)
    c.text_c(410, 10, "Responsible AI-Driven Sustainable Marketing Model", BLACK, 2)

    layers = [
        ("INPUT LAYER", DARK_BLUE, PALE_BLUE,
         ["Consumer data", "Product life-cycle", "data", "Context signals"]),
        ("INTELLIGENCE", PURPLE, LIGHT_PURPLE,
         ["Predictive analytics", "NLP, vision", "Recommenders", "Pricing, personal."]),
        ("ENGAGEMENT", ORANGE, LIGHT_ORANGE,
         ["SHIFT levers:", "Social, Habit, Self,", "Feelings, Tangible", ""]),
        ("OUTCOMES", DARK_GREEN, LIGHT_GREEN,
         ["Triple bottom line:", "People", "Planet", "Profit"]),
    ]
    bw, bh, gap, top = 165, 150, 33, 80
    for i, (title, col, fill, lines) in enumerate(layers):
        x1 = 30 + i * (bw + gap)
        box(c, x1, top, x1 + bw, top + bh, col, fill, title, lines, 16)
        if i > 0:
            c.arrow(x1 - gap + 3, top + bh // 2, x1 - 3, top + bh // 2, GRAY, 3, 10)

    # Feedback loop from outcomes back to inputs
    fy = top + bh + 40
    right_x = 30 + 3 * (bw + gap) + bw // 2
    left_x = 30 + bw // 2
    c.line(right_x, top + bh + 2, right_x, fy, MED_GREEN, 3)
    c.line(left_x, fy, right_x, fy, MED_GREEN, 3)
    c.arrow(left_x, fy, left_x, top + bh + 4, MED_GREEN, 3, 10)
    c.text_c(410, fy + 8, "Feedback: environmental and social results retrain models", DARK_GREEN, 1)

    # Governance band
    gy = fy + 40
    c.rect(30, gy, 790, gy + 90, RED, LIGHT_RED)
    c.text_c(410, gy + 10, "GOVERNANCE BAND (applies to all layers)", BLACK, 1)
    principles = ["Transparency", "Accountability", "Fairness", "Consumer autonomy"]
    pw = 170
    for i, p in enumerate(principles):
        px = 50 + i * (pw + 15)
        c.rect(px, gy + 35, px + pw, gy + 70, RED, LIGHT_GOLD)
        c.text_c(px + pw // 2, gy + 47, p, BLACK, 1)

    c.text(30, 500, "Figure 1: Conceptual model of responsible AI-driven sustainable marketing", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Conceptual_Model.png'))
    print("  Figure_1_Conceptual_Model.png done")


def gen_fig2():
    """Pipeline: data sources -> AI technologies -> applications -> outcomes."""
    c = PNGCanvas(820, 500)
    c.text_c(410, 10, "AI Technology Pipeline for Sustainable Marketing", BLACK, 2)

    cols = [
        ("DATA SOURCES", DARK_BLUE, PALE_BLUE,
         ["Transactions", "Reviews, social", "Product images", "Smart meters", "Supply chain"]),
        ("AI TECHNOLOGIES", PURPLE, LIGHT_PURPLE,
         ["Predictive analytics", "NLP", "Computer vision", "Recommenders", "Dynamic pricing",
          "Personalisation"]),
        ("APPLICATIONS", ORANGE, LIGHT_ORANGE,
         ["Green segmentation", "Claim checking", "Footprint labels", "Second-hand ranking",
          "Waste-cutting prices", "Context nudges"]),
        ("OUTCOMES", DARK_GREEN, LIGHT_GREEN,
         ["Less overproduction", "Less food waste", "Lower emissions", "Longer product life",
          "Trust in claims"]),
    ]
    bw, gap, top = 170, 30, 70
    for i, (title, col, fill, items) in enumerate(cols):
        x1 = 25 + i * (bw + gap)
        c.rect(x1, top, x1 + bw, top + 34, col, col)
        c.text_c(x1 + bw // 2, top + 13, title, (255, 255, 255), 1)
        for j, it in enumerate(items):
            y = top + 48 + j * 48
            c.rect(x1 + 8, y, x1 + bw - 8, y + 34, col, fill)
            c.text_c(x1 + bw // 2, y + 13, it, BLACK, 1)
        if i > 0:
            c.arrow(x1 - gap + 3, top + 17, x1 - 3, top + 17, GRAY, 3, 10)

    # Learning loop
    ly = 420
    c.line(25 + 3 * (bw + gap) + bw // 2, top + 48 + 5 * 48 - 10, 25 + 3 * (bw + gap) + bw // 2, ly, MED_GREEN, 3)
    c.line(25 + bw // 2, ly, 25 + 3 * (bw + gap) + bw // 2, ly, MED_GREEN, 3)
    c.arrow(25 + bw // 2, ly, 25 + bw // 2, top + 48 + 5 * 48 - 10, MED_GREEN, 3, 10)
    c.text_c(410, ly + 8, "Measured outcomes become new training data", DARK_GREEN, 1)

    c.text(25, 478, "Figure 2: AI technology pipeline from data to sustainability outcomes", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_AI_Technology_Pipeline.png'))
    print("  Figure_2_AI_Technology_Pipeline.png done")


def gen_fig3():
    """Capabilities (left) paired with corresponding risks (right)."""
    c = PNGCanvas(820, 470)
    c.text_c(410, 10, "The Double-Edged Sword of AI in Sustainable Marketing", BLACK, 2)

    c.rect(40, 55, 360, 85, DARK_GREEN, DARK_GREEN)
    c.text_c(200, 66, "CAPABILITY (benefit)", (255, 255, 255), 1)
    c.rect(460, 55, 780, 85, RED, RED)
    c.text_c(620, 66, "CORRESPONDING RISK", (255, 255, 255), 1)

    pairs = [
        ("Hyper-personalisation", "Context-aware green nudges",
         "Privacy loss", "Sensitive energy, diet data"),
        ("Segmentation, targeting", "Reach consumers near switching",
         "Algorithmic bias", "Excludes low-income groups"),
        ("Generative content", "Clear impact explanations",
         "AI-enabled greenwashing", "Cheap unsupported claims"),
        ("Analytical power", "Forecasting, waste reduction",
         "AI energy footprint", "Data centre electricity, CO2"),
        ("Engagement optimisation", "Higher campaign response",
         "Over-consumption", "Conflicts with sufficiency"),
    ]
    for i, (b1, b2, r1, r2) in enumerate(pairs):
        y = 100 + i * 66
        c.rect(40, y, 360, y + 52, DARK_GREEN, LIGHT_GREEN)
        c.text_c(200, y + 12, b1, BLACK, 1)
        c.text_c(200, y + 30, b2, GRAY, 1)
        c.rect(460, y, 780, y + 52, RED, LIGHT_RED)
        c.text_c(620, y + 12, r1, BLACK, 1)
        c.text_c(620, y + 30, r2, GRAY, 1)
        c.arrow(364, y + 26, 456, y + 26, GOLD, 3, 10)

    c.text_c(410, 432, "Human oversight and governance needed at every pairing", PURPLE, 1)
    c.text(40, 452, "Figure 3: AI capabilities in sustainable marketing and their corresponding risks", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Double_Edged_Sword.png'))
    print("  Figure_3_Double_Edged_Sword.png done")


def gen_fig4():
    """Five-stage circular governance cycle."""
    c = PNGCanvas(820, 560)
    c.text_c(410, 10, "Responsible AI Governance Cycle for Sustainable Marketing", BLACK, 2)

    cx, cy, R = 410, 285, 185
    c.circle(cx, cy, 70, DARK_BLUE, PALE_BLUE)
    c.text_c(cx, cy - 20, "RESPONSIBLE", BLACK, 1)
    c.text_c(cx, cy - 6, "AI FOR", BLACK, 1)
    c.text_c(cx, cy + 8, "SUSTAINABLE", BLACK, 1)
    c.text_c(cx, cy + 22, "MARKETING", BLACK, 1)

    stages = [
        ("1. PURPOSE", ["Define outcome", "and metric"], MED_BLUE, LIGHT_BLUE),
        ("2. DATA", ["Minimise, verify,", "meaningful consent"], PURPLE, LIGHT_PURPLE),
        ("3. MODEL AUDIT", ["Bias, objectives,", "energy use"], ORANGE, LIGHT_ORANGE),
        ("4. DEPLOYMENT", ["Disclose AI content,", "substantiate claims"], RED, LIGHT_RED),
        ("5. IMPACT", ["Measure, verify,", "feed back"], DARK_GREEN, LIGHT_GREEN),
    ]
    bw, bh = 170, 62
    pts = []
    for i in range(5):
        ang = -math.pi / 2 + i * 2 * math.pi / 5
        pts.append((int(cx + R * math.cos(ang)), int(cy + R * math.sin(ang))))
    for i, ((px, py), (title, lines, col, fill)) in enumerate(zip(pts, stages)):
        box(c, px - bw // 2, py - bh // 2, px + bw // 2, py + bh // 2, col, fill, title, lines, 14)
    # Arrows between consecutive stages (clockwise), shortened to avoid boxes
    for i in range(5):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % 5]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        s = 0.33
        c.arrow(int(x1 + dx * s), int(y1 + dy * s), int(x2 - dx * s), int(y2 - dy * s), GRAY, 3, 10)

    c.text(30, 540, "Figure 4: Five-stage responsible AI governance cycle for sustainable marketing", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Governance_Cycle.png'))
    print("  Figure_4_Governance_Cycle.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()


if __name__ == '__main__':
    main()
