#!/usr/bin/env python3
"""
Generate 4 figure images (PNG) for Chapter 5
"AI-Powered Digital Marketing for Sustainability".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py
so it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - Conceptual framework: drivers -> AI capabilities -> outcomes
  Figure 2 - AI-driven carbon labelling and transparency pipeline
  Figure 3 - Responsible AI-powered sustainable marketing framework (pillars)
  Figure 4 - Sustainability outcome measurement dashboard (bar chart)
"""

import os

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

OUTPUT_DIR = '/projects/sandbox/AMMAN/digital_marketing_figures'


def _lines(c, cx, y, lines, color, scale=1, lh=12):
    for i, ln in enumerate(lines):
        c.text_c(cx, y + i * lh, ln, color, scale)


def gen_fig1():
    """Figure 1: Conceptual framework linking drivers, AI, and outcomes."""
    c = PNGCanvas(840, 470)
    c.text_c(420, 10, "Conceptual Framework of AI-Powered Sustainable Marketing", BLACK, 2)

    # Column headers
    c.text_c(120, 48, "SUSTAINABILITY DRIVERS", DARK_BLUE, 1)
    c.text_c(420, 48, "AI CAPABILITIES", DARK_GREEN, 1)
    c.text_c(720, 48, "MARKETING OUTCOMES", ORANGE, 1)

    drivers = ["Climate change", "Resource depletion",
               "Ethical consumption", "Consumer expectations"]
    caps = ["Predictive analytics", "Natural language proc.",
            "Computer vision", "Recommendation systems", "Intelligent segmentation"]
    outcomes = ["Sustainable consumption", "Responsible branding",
                "Brand transparency", "Environmental awareness"]

    # Left column (drivers)
    lx1, lx2 = 25, 225
    y = 72
    for d in drivers:
        c.rect(lx1, y, lx2, y + 56, DARK_BLUE, PALE_BLUE)
        c.text_c((lx1 + lx2) // 2, y + 24, d, BLACK, 1)
        y += 66

    # Center column (capabilities)
    cx1, cx2 = 320, 520
    y = 68
    for cp in caps:
        c.rect(cx1, y, cx2, y + 44, DARK_GREEN, LIGHT_GREEN)
        c.text_c((cx1 + cx2) // 2, y + 18, cp, BLACK, 1)
        y += 54

    # Right column (outcomes)
    rx1, rx2 = 615, 815
    y = 72
    for o in outcomes:
        c.rect(rx1, y, rx2, y + 56, ORANGE, LIGHT_ORANGE)
        c.text_c((rx1 + rx2) // 2, y + 24, o, BLACK, 1)
        y += 66

    # Flow arrows between columns
    c.arrow(lx2 + 4, 200, cx1 - 4, 200, GRAY, 3, 12)
    c.text_c((lx2 + cx1) // 2, 182, "inform", GRAY, 1)
    c.arrow(cx2 + 4, 200, rx1 - 4, 200, GRAY, 3, 12)
    c.text_c((cx2 + rx1) // 2, 182, "enable", GRAY, 1)

    # Feedback loop along the bottom (outcomes measured -> refine engagement)
    c.line(720, 405, 720, 435, PURPLE, 2)
    c.line(720, 435, 120, 435, PURPLE, 2)
    c.arrow(120, 435, 120, 405, PURPLE, 2, 10)
    c.text_c(420, 448, "Feedback: measured outcomes refine future engagement", PURPLE, 1)

    c.text(25, 462, "Figure 1: From sustainability drivers through AI capabilities to measurable marketing outcomes", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Conceptual_Framework.png'))
    print("  Figure_1_Conceptual_Framework.png done")


def gen_fig2():
    """Figure 2: AI-driven carbon labelling and transparency pipeline."""
    c = PNGCanvas(880, 330)
    c.text_c(440, 10, "AI-Driven Carbon Labelling and Transparency Pipeline", BLACK, 2)

    stages = [
        ("SUPPLY and", "PRODUCT DATA", ["LCA, sourcing,", "logistics records"], MED_BLUE, LIGHT_BLUE),
        ("AI FOOTPRINT", "ESTIMATION", ["ML fills gaps,", "uncertainty ranges"], DARK_GREEN, LIGHT_GREEN),
        ("AUTOMATED", "LABELLING", ["carbon + eco", "attributes at scale"], GOLD, LIGHT_GOLD),
        ("DIGITAL", "DISCLOSURE", ["product pages,", "QR codes, in-app"], ORANGE, LIGHT_ORANGE),
        ("INFORMED", "CHOICE", ["lower-impact", "purchase decisions"], PURPLE, LIGHT_PURPLE),
    ]

    bw, bh = 150, 100
    gap = 23
    top = 80
    xs = []
    for i, (t1, t2, subs, col, fill) in enumerate(stages):
        bx = 15 + i * (bw + gap)
        xs.append((bx, bx + bw))
        c.rect(bx, top, bx + bw, top + bh, col, fill)
        cxm = bx + bw // 2
        c.text_c(cxm, top + 14, t1, BLACK, 1)
        c.text_c(cxm, top + 28, t2, BLACK, 1)
        for j, s in enumerate(subs):
            c.text_c(cxm, top + 52 + j * 13, s, GRAY, 1)
        if i > 0:
            c.arrow(xs[i - 1][1] + 2, top + bh // 2, bx - 2, top + bh // 2, GRAY, 3, 11)

    # Feedback arrow from choice back to estimation
    by = top + bh + 35
    c.line(xs[4][0] + bw // 2, top + bh, xs[4][0] + bw // 2, by, RED, 2)
    c.line(xs[4][0] + bw // 2, by, xs[1][0] + bw // 2, by, RED, 2)
    c.arrow(xs[1][0] + bw // 2, by, xs[1][0] + bw // 2, top + bh, RED, 2, 10)
    c.text_c(440, by + 12, "Feedback: anonymised purchase data refines future footprint estimates", RED, 1)

    c.text(15, 318, "Figure 2: Pipeline converting supply-chain data into trusted consumer-facing carbon labels", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Carbon_Labelling_Pipeline.png'))
    print("  Figure_2_Carbon_Labelling_Pipeline.png done")


def gen_fig3():
    """Figure 3: Responsible AI-powered sustainable marketing framework."""
    c = PNGCanvas(780, 430)
    c.text_c(390, 10, "Responsible AI-Powered Sustainable Marketing Framework", BLACK, 2)

    # Top beam
    c.rect(55, 55, 725, 105, DARK_GREEN, LIGHT_GREEN)
    c.text_c(390, 72, "TRUSTWORTHY SUSTAINABLE MARKETING", BLACK, 1)

    pillars = [
        ("ETHICAL", ["AI", "DESIGN", "", "fairness,", "accountability"], DARK_BLUE, PALE_BLUE),
        ("TRANS-", ["PARENCY", "", "explainable", "models,", "disclosure"], MED_BLUE, LIGHT_BLUE),
        ("PRIVACY", ["PROTECTION", "", "data minim.,", "privacy by", "design"], PURPLE, LIGHT_PURPLE),
        ("CONSUMER", ["EMPOWER-", "MENT", "", "control over", "data, choice"], ORANGE, LIGHT_ORANGE),
        ("MEASURABLE", ["INDICATORS", "", "auditable", "metrics, ESG", "alignment"], GOLD, LIGHT_GOLD),
    ]

    pw = 112
    gap = 24
    total = 5 * pw + 4 * gap
    start = (780 - total) // 2
    ptop, pbot = 135, 335
    for i, (head, body, col, fill) in enumerate(pillars):
        px = start + i * (pw + gap)
        c.rect(px, ptop, px + pw, pbot, col, fill)
        cxm = px + pw // 2
        c.text_c(cxm, ptop + 12, head, BLACK, 1)
        _lines(c, cxm, ptop + 28, body, BLACK, 1, 14)

    # Base
    c.rect(35, 345, 745, 390, GRAY, LIGHT_GRAY)
    c.text_c(390, 362, "FOUNDATION: measurable, auditable, verifiable sustainability", BLACK, 1)

    c.text(35, 418, "Figure 3: Five pillars supporting trustworthy AI-powered sustainable marketing", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Responsible_Framework.png'))
    print("  Figure_3_Responsible_Framework.png done")


def gen_fig4():
    """Figure 4: Sustainability outcome measurement dashboard (bar chart)."""
    c = PNGCanvas(820, 470)
    c.text_c(410, 10, "Sustainability Outcome Measurement Dashboard", BLACK, 2)

    domains = [
        ("Consumer", "behaviour", 68, 80, MED_BLUE),
        ("Resource", "efficiency", 61, 75, DARK_GREEN),
        ("Carbon", "reduction", 55, 70, MED_GREEN),
        ("Brand", "trust", 72, 85, ORANGE),
        ("Social", "impact", 49, 65, PURPLE),
    ]

    ax, ay_top, ay_bot = 110, 70, 360
    ax_right = 760
    plot_h = ay_bot - ay_top  # 290 px == 100%

    # Axes
    c.vline(ax, ay_top, ay_bot, BLACK)
    c.hline(ax, ax_right, ay_bot, BLACK)

    # Gridlines + y labels (0..100)
    for v in range(0, 101, 25):
        gy = ay_bot - int(v / 100 * plot_h)
        c.hline(ax, ax_right, gy, LIGHT_GRAY)
        c.vline(ax, ay_top, ay_bot, BLACK)
        c.text(ax - 40, gy - 3, f"{v}%", GRAY, 1)
    c.hline(ax, ax_right, ay_bot, BLACK)

    bw = 70
    slot = (ax_right - ax) // len(domains)
    for i, (l1, l2, cur, tgt, col) in enumerate(domains):
        bx = ax + i * slot + (slot - bw) // 2
        ch = int(cur / 100 * plot_h)
        th = int(tgt / 100 * plot_h)
        # current bar
        c.rect(bx, ay_bot - ch, bx + bw, ay_bot, BLACK, col)
        c.text_c(bx + bw // 2, ay_bot - ch - 12, f"{cur}%", BLACK, 1)
        # target marker (dashed line across bar)
        ty = ay_bot - th
        for x in range(bx - 6, bx + bw + 6, 8):
            c.hline(x, x + 4, ty, RED)
            c.hline(x, x + 4, ty + 1, RED)
        c.text_c(bx + bw // 2, ay_bot + 12, l1, BLACK, 1)
        c.text_c(bx + bw // 2, ay_bot + 25, l2, BLACK, 1)

    # Legend
    c.rect(560, 60, 580, 75, BLACK, MED_BLUE)
    c.text(588, 62, "Current performance", BLACK, 1)
    c.hline(560, 580, 90, RED)
    c.hline(560, 580, 91, RED)
    c.text(588, 85, "Target", BLACK, 1)

    c.text(40, 420, "Figure 4: Illustrative outcomes across five domains, each tracked against an explicit target", BLACK, 1)
    c.text(40, 440, "to support balanced, transparent, and auditable sustainability reporting", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Outcome_Dashboard.png'))
    print("  Figure_4_Outcome_Dashboard.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating sustainable digital marketing chapter figures...")
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
