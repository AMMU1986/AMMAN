#!/usr/bin/env python3
"""
Generate 4 figure images (PNG) for the chapter
"Responsible Innovation and Ethical AI Governance".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - Responsible Innovation dimensions integrated across the AI
             innovation lifecycle (AREA: Anticipation, Reflexivity, Inclusion,
             Responsiveness).
  Figure 2 - Five core ethical principles as pillars supporting trustworthy AI.
  Figure 3 - Integrated ethical AI governance model mapped across the AI
             lifecycle with layered governance mechanisms.
  Figure 4 - Multi-stakeholder deliberative governance ecosystem.
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/ethics_figures'


def gen_fig1():
    """Figure 1: Responsible innovation dimensions across the AI lifecycle."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Responsible Innovation Dimensions in the AI Lifecycle", BLACK, 2)

    # Central node
    cx1, cy1, cx2, cy2 = 300, 195, 460, 275
    c.rect(cx1, cy1, cx2, cy2, DARK_BLUE, PALE_BLUE)
    c.text_c(380, 218, "RESPONSIBLE", BLACK, 1)
    c.text_c(380, 234, "AI INNOVATION", BLACK, 1)
    c.text_c(380, 252, "values + trust", GRAY, 1)

    # Four AREA dimensions around the centre
    dims = [
        ("ANTICIPATION", "Foresight of impacts,", "risks and futures", 60, 70, MED_BLUE, LIGHT_BLUE),
        ("REFLEXIVITY", "Scrutiny of values,", "assumptions and limits", 500, 70, DARK_GREEN, LIGHT_GREEN),
        ("INCLUSION", "Deliberation with", "diverse stakeholders", 60, 330, ORANGE, LIGHT_ORANGE),
        ("RESPONSIVENESS", "Capacity to adapt,", "correct and redirect", 500, 330, PURPLE, LIGHT_PURPLE),
    ]
    bw, bh = 200, 70
    for title, l1, l2, bx, by, col, fill in dims:
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        c.text_c(bx + bw // 2, by + 12, title, BLACK, 1)
        c.text_c(bx + bw // 2, by + 34, l1, GRAY, 1)
        c.text_c(bx + bw // 2, by + 48, l2, GRAY, 1)

    # Connectors to the centre
    c.arrow(160, 140, 320, 195, MED_BLUE, 2, 8)
    c.arrow(600, 140, 445, 195, DARK_GREEN, 2, 8)
    c.arrow(160, 330, 320, 275, ORANGE, 2, 8)
    c.arrow(600, 330, 445, 275, PURPLE, 2, 8)

    # Lifecycle strip along the bottom
    stages = ["Design", "Development", "Deployment", "Monitoring"]
    sx = 90
    sw = 140
    sy = 425
    prev = None
    for i, st in enumerate(stages):
        bx = sx + i * (sw + 10)
        c.rect(bx, sy, bx + sw, sy + 26, GOLD, LIGHT_GOLD)
        c.text_c(bx + sw // 2, sy + 8, st, BLACK, 1)
        if prev is not None:
            c.arrow(prev, sy + 13, bx - 2, sy + 13, GRAY, 2, 6)
        prev = bx + sw
    c.text_c(380, 405, "Applied iteratively across the AI innovation lifecycle", GRAY, 1)

    c.text(30, 458, "Figure 1: The AREA dimensions of responsible innovation integrated across the AI lifecycle.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_RI_Dimensions.png'))
    print("  Figure_1_RI_Dimensions.png done")


def gen_fig2():
    """Figure 2: Five ethical principles as pillars of trustworthy AI."""
    c = PNGCanvas(760, 460)
    c.text_c(380, 10, "Core Ethical Principles Supporting Trustworthy AI", BLACK, 2)

    # Roof
    c.rect(70, 60, 690, 100, DARK_BLUE, PALE_BLUE)
    c.text_c(380, 72, "TRUSTWORTHY AND RESPONSIBLE AI", BLACK, 1)
    c.text_c(380, 88, "lawful, ethical and robust", GRAY, 1)

    pillars = [
        ("TRANS-", "PARENCY", "Explainable,", "documented", MED_BLUE, LIGHT_BLUE),
        ("FAIRNESS", "", "Non-", "discrimination", DARK_GREEN, LIGHT_GREEN),
        ("ACCOUNT-", "ABILITY", "Answerability,", "redress", ORANGE, LIGHT_ORANGE),
        ("PRIVACY", "", "Data", "protection", PURPLE, LIGHT_PURPLE),
        ("HUMAN-", "CENTRICITY", "Oversight,", "autonomy", RED, LIGHT_RED),
    ]
    pw = 108
    gap = 12
    start = 70
    top = 120
    bot = 360
    for i, (t1, t2, s1, s2, col, fill) in enumerate(pillars):
        bx = start + i * (pw + gap)
        c.rect(bx, top, bx + pw, bot, col, fill)
        c.text_c(bx + pw // 2, top + 22, t1, BLACK, 1)
        if t2:
            c.text_c(bx + pw // 2, top + 38, t2, BLACK, 1)
        c.text_c(bx + pw // 2, top + 120, s1, GRAY, 1)
        c.text_c(bx + pw // 2, top + 136, s2, GRAY, 1)

    # Foundation
    c.rect(70, 375, 690, 415, GRAY, LIGHT_GRAY)
    c.text_c(380, 388, "Foundation: societal values, human rights and rule of law", BLACK, 1)

    c.text(30, 442, "Figure 2: Five interdependent ethical principles as pillars of trustworthy AI.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Ethical_Principles.png'))
    print("  Figure_2_Ethical_Principles.png done")


def gen_fig3():
    """Figure 3: Integrated ethical AI governance model across the lifecycle."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Integrated Ethical AI Governance Model", BLACK, 2)

    # Governance layers (rows)
    layers = [
        ("Value Layer", "Societal values, human rights, organisational purpose", PURPLE, LIGHT_PURPLE),
        ("Principle Layer", "Transparency, fairness, accountability, privacy", DARK_GREEN, LIGHT_GREEN),
        ("Process Layer", "Impact assessment, audits, documentation, testing", ORANGE, LIGHT_ORANGE),
        ("Oversight Layer", "Ethics boards, regulators, redress and monitoring", MED_BLUE, LIGHT_BLUE),
    ]
    lx1, lx2 = 60, 700
    top = 55
    lh = 50
    gap = 10
    for i, (title, sub, col, fill) in enumerate(layers):
        y1 = top + i * (lh + gap)
        y2 = y1 + lh
        c.rect(lx1, y1, lx2, y2, col, fill)
        c.text_c(160, y1 + 16, title, BLACK, 1)
        c.text_c(430, y1 + 24, sub, GRAY, 1)

    # Lifecycle columns beneath
    stages = [
        ("Design", DARK_BLUE, PALE_BLUE, "Anticipate impacts"),
        ("Development", MED_GREEN, LIGHT_GREEN, "Bias + robustness tests"),
        ("Deployment", ORANGE, LIGHT_ORANGE, "Transparency + consent"),
        ("Monitoring", RED, LIGHT_RED, "Audit + redress"),
    ]
    sx = 60
    sw = 150
    sgap = 13
    sy1 = 310
    sy2 = 400
    prev = None
    for i, (st, col, fill, note) in enumerate(stages):
        bx = sx + i * (sw + sgap)
        c.rect(bx, sy1, bx + sw, sy2, col, fill)
        c.text_c(bx + sw // 2, sy1 + 14, st, BLACK, 1)
        c.text_c(bx + sw // 2, sy1 + 42, note, GRAY, 1)
        if prev is not None:
            c.arrow(prev, sy1 + 30, bx - 2, sy1 + 30, GRAY, 2, 7)
        prev = bx + sw

    # Feedback loop arrow from monitoring back to design
    c.line(prev - sw // 2, sy2 + 5, prev - sw // 2, sy2 + 25, GRAY, 2)
    c.line(prev - sw // 2, sy2 + 25, sx + sw // 2, sy2 + 25, GRAY, 2)
    c.arrow(sx + sw // 2, sy2 + 25, sx + sw // 2, sy2 + 5, GRAY, 2, 7)
    c.text_c(380, sy2 + 34, "Continuous feedback: monitoring informs redesign", GRAY, 1)

    c.text(30, 458, "Figure 3: Layered governance mechanisms applied across each stage of the AI lifecycle.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Governance_Model.png'))
    print("  Figure_3_Governance_Model.png done")


def gen_fig4():
    """Figure 4: Multi-stakeholder deliberative governance ecosystem."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Multi-Stakeholder Deliberative Governance Ecosystem", BLACK, 2)

    # Central AI system
    ccx, ccy, r = 380, 240, 62
    c.circle(ccx, ccy, r, DARK_BLUE, PALE_BLUE)
    c.text_c(ccx, ccy - 14, "AI SYSTEM", BLACK, 1)
    c.text_c(ccx, ccy + 2, "and its", GRAY, 1)
    c.text_c(ccx, ccy + 16, "decisions", GRAY, 1)

    # Stakeholders around the centre
    nodes = [
        ("Developers", "and vendors", 380, 70, MED_BLUE, LIGHT_BLUE),
        ("Business", "leaders", 620, 150, DARK_GREEN, LIGHT_GREEN),
        ("Regulators", "and policy", 620, 330, ORANGE, LIGHT_ORANGE),
        ("Affected", "communities", 380, 410, RED, LIGHT_RED),
        ("Civil society", "and academia", 140, 330, PURPLE, LIGHT_PURPLE),
        ("End users", "", 140, 150, GOLD, LIGHT_GOLD),
    ]
    bw, bh = 150, 56
    for t1, t2, cxp, cyp, col, fill in nodes:
        x1 = cxp - bw // 2
        y1 = cyp - bh // 2
        c.rect(x1, y1, x1 + bw, y1 + bh, col, fill)
        c.text_c(cxp, cyp - 8, t1, BLACK, 1)
        if t2:
            c.text_c(cxp, cyp + 8, t2, GRAY, 1)
        # Bidirectional connectors (deliberation + feedback)
        c.line(cxp, cyp, ccx, ccy, GRAY, 1)

    c.text_c(380, 445, "Bidirectional deliberation, contestation and feedback among all actors", GRAY, 1)

    c.text(30, 460, "Figure 4: Deliberative, multi-stakeholder ecosystem surrounding an AI system.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Stakeholder_Ecosystem.png'))
    print("  Figure_4_Stakeholder_Ecosystem.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating ethical AI governance chapter figures...")
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
