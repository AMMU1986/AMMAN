#!/usr/bin/env python3
"""
Generate 4 conceptual figure images (PNG) for the chapter
"AI-Powered Digital Marketing for Sustainability".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - The convergence of AI, digital marketing, and the sustainability
             imperative
  Figure 2 - The AI-enabled sustainable consumer journey
  Figure 3 - The environmental footprint paradox of AI systems
  Figure 4 - A framework for responsible AI-driven sustainable marketing
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
    BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/ai_marketing_figures'


def gen_fig1():
    """Figure 1: Convergence of AI, digital marketing, and sustainability."""
    c = PNGCanvas(780, 560)
    c.text_c(390, 10, "The Convergence of AI, Digital Marketing, and Sustainability", BLACK, 2)

    # Three large overlapping domain circles arranged in a triad
    r = 150
    centers = {
        'AI': (265, 200, MED_BLUE, PALE_BLUE),
        'MARKETING': (515, 200, ORANGE, LIGHT_ORANGE),
        'SUSTAINABILITY': (390, 390, DARK_GREEN, LIGHT_GREEN),
    }
    # draw filled circles first (lighter), then outlines
    for label, (cx, cy, col, fill) in centers.items():
        c.circle(cx, cy, r, col, fill)
    for label, (cx, cy, col, fill) in centers.items():
        c.circle(cx, cy, r, col)

    # Domain labels (outer)
    c.text_c(195, 70, "ARTIFICIAL", DARK_BLUE, 1)
    c.text_c(195, 84, "INTELLIGENCE", DARK_BLUE, 1)
    c.text_c(195, 100, "predictive, NLP,", GRAY, 1)
    c.text_c(195, 114, "vision, recommenders", GRAY, 1)

    c.text_c(590, 70, "DIGITAL", ORANGE, 1)
    c.text_c(590, 84, "MARKETING", ORANGE, 1)
    c.text_c(590, 100, "segmentation,", GRAY, 1)
    c.text_c(590, 114, "targeting, content", GRAY, 1)

    c.text_c(390, 500, "SUSTAINABILITY IMPERATIVE", DARK_GREEN, 1)
    c.text_c(390, 516, "green consumer, transparency, accountability", GRAY, 1)

    # Pairwise overlap labels
    c.text_c(390, 185, "hyper-personalized,", BLACK, 1)
    c.text_c(390, 200, "context-aware campaigns", BLACK, 1)
    c.text_c(300, 320, "credible green", BLACK, 1)
    c.text_c(300, 334, "nudges", BLACK, 1)
    c.text_c(480, 320, "verifiable", BLACK, 1)
    c.text_c(480, 334, "claims", BLACK, 1)

    # Central intersection node
    c.circle(390, 285, 52, RED, LIGHT_RED)
    c.text_c(390, 268, "AI-powered", BLACK, 1)
    c.text_c(390, 282, "sustainable", BLACK, 1)
    c.text_c(390, 296, "marketing", BLACK, 1)

    c.text(30, 540, "Figure 1: The emerging field forms where three forces intersect", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Convergence.png'))
    print("  Figure_1_Convergence.png done")


def gen_fig2():
    """Figure 2: AI-enabled sustainable consumer journey."""
    c = PNGCanvas(900, 420)
    c.text_c(450, 10, "The AI-Enabled Sustainable Consumer Journey", BLACK, 2)

    stages = [
        ("Segment", "Behavioral clustering of\neco-conscious audiences", MED_BLUE, LIGHT_BLUE),
        ("Recommend", "Surface eco-friendly\nalternatives at discovery", DARK_GREEN, LIGHT_GREEN),
        ("Incentivize", "Dynamic pricing &\npersonalized nudges", ORANGE, LIGHT_ORANGE),
        ("Inform", "Carbon labelling &\noptimized messaging", PURPLE, LIGHT_PURPLE),
        ("Act", "Sustainable purchase\n& loyalty", RED, LIGHT_RED),
    ]
    n = len(stages)
    bw = 150
    gap = 25
    total = n * bw + (n - 1) * gap
    x0 = (900 - total) // 2
    top = 130
    bh = 120
    for i, (title, sub, col, fill) in enumerate(stages):
        bx = x0 + i * (bw + gap)
        c.rect(bx, top, bx + bw, top + bh, col, fill)
        c.text_c(bx + bw // 2, top + 14, title, BLACK, 2)
        for j, ln in enumerate(sub.split("\n")):
            c.text_c(bx + bw // 2, top + 54 + j * 16, ln, GRAY, 1)
        if i < n - 1:
            ax = bx + bw
            c.arrow(ax + 2, top + bh // 2, ax + gap - 2, top + bh // 2, GRAY, 3, 10)

    # Data / learning feedback loop beneath
    y_loop = top + bh + 50
    c.line(x0 + bw // 2, top + bh + 2, x0 + bw // 2, y_loop, MED_BLUE, 2)
    c.line(x0 + bw // 2, y_loop, x0 + total - bw // 2, y_loop, MED_BLUE, 2)
    c.arrow(x0 + total - bw // 2, y_loop, x0 + total - bw // 2, top + bh + 2, MED_BLUE, 2, 9)
    c.text_c(450, y_loop + 8, "Behavioral data feeds continuous learning and re-personalization", MED_BLUE, 1)

    c.text_c(450, 90, "AI acts at every stage; the architecture is neutral between genuine and merely apparent sustainability", GRAY, 1)
    c.text(30, 400, "Figure 2: Segmentation, recommendation, incentivization, and transparency across the journey", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Consumer_Journey.png'))
    print("  Figure_2_Consumer_Journey.png done")


def gen_fig3():
    """Figure 3: Environmental footprint paradox of AI systems (a balance)."""
    c = PNGCanvas(820, 500)
    c.text_c(410, 10, "The Environmental Footprint Paradox of AI Systems", BLACK, 2)

    # Balance beam
    fulcrum_x, fulcrum_y = 410, 200
    beam_half = 300
    c.line(fulcrum_x - beam_half, fulcrum_y, fulcrum_x + beam_half, fulcrum_y, BLACK, 3)
    # fulcrum triangle
    for dy in range(60):
        c.hline(fulcrum_x - dy // 2, fulcrum_x + dy // 2, fulcrum_y + dy, GRAY)
    c.text_c(fulcrum_x, fulcrum_y + 68, "Net sustainability balance", BLACK, 1)

    # Left pan: environmental COSTS
    lx = fulcrum_x - 230
    c.line(lx, fulcrum_y, lx, fulcrum_y + 40, GRAY, 2)
    c.rect(lx - 150, fulcrum_y + 40, lx + 150, fulcrum_y + 170, RED, LIGHT_RED)
    c.text_c(lx, fulcrum_y + 54, "ENVIRONMENTAL COSTS", RED, 1)
    costs = ["Model training energy", "Recurring inference load",
             "Data-center electricity", "ICT manufacturing & networks"]
    for i, t in enumerate(costs):
        c.text_c(lx, fulcrum_y + 78 + i * 20, "- " + t, BLACK, 1)

    # Right pan: sustainability BENEFITS
    rx = fulcrum_x + 230
    c.line(rx, fulcrum_y, rx, fulcrum_y + 40, GRAY, 2)
    c.rect(rx - 150, fulcrum_y + 40, rx + 150, fulcrum_y + 170, DARK_GREEN, LIGHT_GREEN)
    c.text_c(rx, fulcrum_y + 54, "SUSTAINABILITY BENEFITS", DARK_GREEN, 1)
    bens = ["Less overproduction & waste", "Lower-emission logistics",
            "Informed greener choices", "Scaled behavior change"]
    for i, t in enumerate(bens):
        c.text_c(rx, fulcrum_y + 78 + i * 20, "+ " + t, BLACK, 1)

    # Condition note
    c.rect(60, 420, 760, 470, GRAY, (250, 250, 250))
    c.text_c(410, 432, "Responsible condition: measured benefits must demonstrably exceed the", BLACK, 1)
    c.text_c(410, 450, "footprint of the computation, net of rebound effects", GRAY, 1)

    c.text(30, 486, "Figure 3: Weighing the costs of the AI lifecycle against the benefits of well-governed applications", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Footprint_Paradox.png'))
    print("  Figure_3_Footprint_Paradox.png done")


def gen_fig4():
    """Figure 4: Framework for responsible AI-driven sustainable marketing."""
    c = PNGCanvas(860, 520)
    c.text_c(430, 10, "A Framework for Responsible AI-Driven Sustainable Marketing", BLACK, 2)

    # Four principle pillars feeding a transformative-outcome bar
    principles = [
        ("Ethical", "Design", ["Bias audits", "Data minimization", "Efficient models", "Clear accountability"], MED_BLUE, LIGHT_BLUE),
        ("Radical", "Transparency", ["Disclose AI use", "Substantiate claims", "Open data handling", "Beyond compliance"], DARK_GREEN, LIGHT_GREEN),
        ("Consumer", "Empowerment", ["Data control", "Genuine agency", "Aid not manipulate", "Informed choice"], ORANGE, LIGHT_ORANGE),
        ("Measurable", "Impact", ["Real vs metric", "Footprint accounting", "Rebound effects", "Honest reporting"], PURPLE, LIGHT_PURPLE),
    ]
    n = len(principles)
    bw = 180
    gap = 22
    total = n * bw + (n - 1) * gap
    x0 = (860 - total) // 2
    top = 70
    bh = 180
    for i, (l1, l2, items, col, fill) in enumerate(principles):
        bx = x0 + i * (bw + gap)
        c.rect(bx, top, bx + bw, top + bh, col, fill)
        c.text_c(bx + bw // 2, top + 12, l1, BLACK, 2)
        c.text_c(bx + bw // 2, top + 32, l2, BLACK, 2)
        for j, it in enumerate(items):
            c.text_c(bx + bw // 2, top + 70 + j * 22, "- " + it, GRAY, 1)
        # arrow down to outcome bar
        midx = bx + bw // 2
        c.arrow(midx, top + bh + 2, midx, top + bh + 38, GRAY, 3, 10)

    # Outcome bar
    oy = top + bh + 40
    c.rect(x0, oy, x0 + total, oy + 48, RED, LIGHT_RED)
    c.text_c(x0 + total // 2, oy + 12, "TRANSFORMATIVE OUTCOME", BLACK, 1)
    c.text_c(x0 + total // 2, oy + 30, "Real environmental impact, not merely marketing performance", GRAY, 1)

    # Continuous monitoring loop (right side)
    loop_x = x0 + total + 20
    if loop_x < 840:
        c.line(x0 + total + 2, oy + 24, loop_x, oy + 24, MED_BLUE, 2)
        c.line(loop_x, oy + 24, loop_x, top + bh // 2, MED_BLUE, 2)
        c.arrow(loop_x, top + bh // 2, x0 + total + 2, top + bh // 2, MED_BLUE, 2, 9)

    c.text_c(430, oy + 72, "Principles are mutually reinforcing and sustained by an iterative monitor-learn-adjust loop", GRAY, 1)
    c.text(30, 506, "Figure 4: Four principles converging on measurable, verifiable sustainable impact", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Responsible_Framework.png'))
    print("  Figure_4_Responsible_Framework.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating AI marketing chapter figures...")
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
