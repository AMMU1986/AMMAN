#!/usr/bin/env python3
"""
Generate 4 figure images (PNG) for the chapter
"AI-Driven Research Support, Research Data Management, and Research Workflows".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - The AI-augmented research life cycle (four interdependent phases)
  Figure 2 - AI-driven, FAIR-aligned research data management pipeline
  Figure 3 - AI-augmented research workflow (design -> experiment -> document)
  Figure 4 - Layered framework for responsible AI in research
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/research_figures'


def gen_fig1():
    """Figure 1: The AI-augmented research life cycle (four phases in a loop)."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "The AI-Augmented Research Life Cycle", BLACK, 2)

    # Four phase boxes arranged as a cycle
    bw, bh = 230, 78
    phases = [
        # (title, sub1, sub2, x, y, outline, fill)
        ("1. Literature Discovery", "Semantic search, screening,", "summarization, hypotheses",
         40, 60, DARK_BLUE, PALE_BLUE),
        ("2. Research Data Mgmt (RDM)", "Metadata, quality checks,", "FAIR-compliant archiving",
         490, 60, DARK_GREEN, LIGHT_GREEN),
        ("3. Research Workflows", "Intelligent design, autonomous", "labs, documentation",
         490, 320, ORANGE, LIGHT_ORANGE),
        ("4. Communication & Eval.", "Peer review, dissemination,", "impact analysis",
         40, 320, PURPLE, LIGHT_PURPLE),
    ]
    centers = []
    for title, s1, s2, x, y, col, fill in phases:
        c.rect(x, y, x + bw, y + bh, col, fill)
        c.text_c(x + bw // 2, y + 12, title, BLACK, 1)
        c.text_c(x + bw // 2, y + 34, s1, GRAY, 1)
        c.text_c(x + bw // 2, y + 48, s2, GRAY, 1)
        centers.append((x + bw // 2, y + bh // 2, x, y))

    # Clockwise arrows between phases: 1->2 (top), 2->3 (right), 3->4 (bottom), 4->1 (left)
    # 1 -> 2 (top horizontal)
    c.arrow(270 + 4, 99, 490 - 4, 99, GRAY, 3, 11)
    # 2 -> 3 (right vertical)
    c.arrow(605, 138 + 4, 605, 320 - 4, GRAY, 3, 11)
    # 3 -> 4 (bottom horizontal, right to left)
    c.arrow(490 - 4, 359, 270 + 4, 359, GRAY, 3, 11)
    # 4 -> 1 (left vertical, bottom to top)
    c.arrow(155, 320 - 4, 155, 138 + 4, GRAY, 3, 11)

    # Central AI hub
    c.rect(300, 195, 460, 275, GOLD, LIGHT_GOLD)
    c.text_c(380, 212, "AI CORE", BLACK, 2)
    c.text_c(380, 234, "NLP - LLMs - ML", BLACK, 1)
    c.text_c(380, 250, "Knowledge graphs", GRAY, 1)
    # Spokes from hub to each phase
    for cx, cy, x, y in centers:
        c.line(380, 235, cx, cy, LIGHT_GRAY, 1)

    c.text_c(380, 300, "Human-centred augmentation (Education 5.0)", MED_BLUE, 1)

    c.text(40, 452, "Figure 1: AI capabilities connect and augment the four phases of the research life cycle", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Research_Life_Cycle.png'))
    print("  Figure_1_Research_Life_Cycle.png done")


def gen_fig2():
    """Figure 2: AI-driven, FAIR-aligned RDM pipeline."""
    c = PNGCanvas(780, 430)
    c.text_c(390, 10, "AI-Driven, FAIR-Aligned Research Data Management Pipeline", BLACK, 2)

    stages = [
        ("Raw Data", "& Context", "Instruments,", "notes, files", MED_BLUE, LIGHT_BLUE),
        ("Automated", "Ingestion", "Parse,", "normalize", DARK_BLUE, PALE_BLUE),
        ("Metadata", "Generation", "NLP, NER,", "ontologies", DARK_GREEN, LIGHT_GREEN),
        ("Quality", "Gates", "Anomaly &", "error checks", ORANGE, LIGHT_ORANGE),
        ("FAIR", "Archiving", "IDs, licences,", "compliance", PURPLE, LIGHT_PURPLE),
    ]
    bw, bh = 128, 95
    top = 110
    gap = 22
    xs = []
    for i, (l1, l2, s1, s2, col, fill) in enumerate(stages):
        x = 20 + i * (bw + gap)
        xs.append((x, x + bw))
        c.rect(x, top, x + bw, top + bh, col, fill)
        c.text_c(x + bw // 2, top + 12, l1, BLACK, 1)
        c.text_c(x + bw // 2, top + 26, l2, BLACK, 1)
        c.text_c(x + bw // 2, top + 50, s1, GRAY, 1)
        c.text_c(x + bw // 2, top + 64, s2, GRAY, 1)
        if i > 0:
            c.arrow(xs[i - 1][1] + 2, top + bh // 2, x - 2, top + bh // 2, GRAY, 3, 10)

    # FAIR banner above the flow
    c.rect(20, 60, 748, 92, DARK_GREEN, LIGHT_GREEN)
    c.text_c(384, 68, "FAIR: Findable - Accessible - Interoperable - Reusable", BLACK, 1)
    c.text_c(384, 82, "Data described for machine actionability", GRAY, 1)

    # Human-in-the-loop checkpoints under metadata & quality stages
    mx = xs[2][0] + bw // 2
    qx = xs[3][0] + bw // 2
    hy = top + bh + 40
    c.rect(mx - 70, hy, qx + 70, hy + 46, GOLD, LIGHT_GOLD)
    c.text_c((mx + qx) // 2, hy + 12, "Human-in-the-loop review", BLACK, 1)
    c.text_c((mx + qx) // 2, hy + 30, "Curators validate & correct AI output", GRAY, 1)
    c.arrow(mx, top + bh + 2, mx, hy - 2, GRAY, 2, 8)
    c.arrow(qx, top + bh + 2, qx, hy - 2, GRAY, 2, 8)

    # Continuous feedback loop arrow (archiving -> ingestion)
    ax = xs[4][0] + bw // 2
    ix = xs[1][0] + bw // 2
    c.line(ax, top - 4, ax, top - 24, GRAY, 2)
    c.line(ax, top - 24, ix, top - 24, GRAY, 2)
    c.arrow(ix, top - 24, ix, top - 4, GRAY, 2, 8)
    c.text_c((ax + ix) // 2, top - 36, "continuous curation feedback", GRAY, 1)

    c.text(20, 412, "Figure 2: Continuous, largely automated curation with human validation at key checkpoints", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_RDM_Pipeline.png'))
    print("  Figure_2_RDM_Pipeline.png done")


def gen_fig3():
    """Figure 3: AI-augmented research workflow with a closed loop."""
    c = PNGCanvas(760, 440)
    c.text_c(380, 10, "AI-Augmented Research Workflow", BLACK, 2)

    # Top row: Hypothesis -> Intelligent Design -> Experimentation
    boxes = [
        ("Hypothesis", "& Goal", 40, 60, DARK_BLUE, PALE_BLUE),
        ("Intelligent", "Design", 300, 60, DARK_GREEN, LIGHT_GREEN),
        ("Experimentation", "(auto / human)", 560, 60, ORANGE, LIGHT_ORANGE),
    ]
    bw, bh = 160, 70
    cen = []
    for l1, l2, x, y, col, fill in boxes:
        c.rect(x, y, x + bw, y + bh, col, fill)
        c.text_c(x + bw // 2, y + 22, l1, BLACK, 1)
        c.text_c(x + bw // 2, y + 40, l2, GRAY, 1)
        cen.append((x + bw // 2, y + bh // 2))

    # Design detail note
    c.text_c(380, 145, "Bayesian optimization - active learning - digital twins", MED_BLUE, 1)

    # Bottom row: Automated Analysis -> Documentation -> Dissemination
    boxes2 = [
        ("Automated", "Analysis", 560, 250, PURPLE, LIGHT_PURPLE),
        ("Automated", "Documentation", 300, 250, MED_BLUE, LIGHT_BLUE),
        ("Dissemination", "& Reuse", 40, 250, RED, LIGHT_RED),
    ]
    cen2 = []
    for l1, l2, x, y, col, fill in boxes2:
        c.rect(x, y, x + bw, y + bh, col, fill)
        c.text_c(x + bw // 2, y + 22, l1, BLACK, 1)
        c.text_c(x + bw // 2, y + 40, l2, GRAY, 1)
        cen2.append((x + bw // 2, y + bh // 2))

    # Arrows top row L->R
    c.arrow(cen[0][0] + 82, cen[0][1], cen[1][0] - 82, cen[1][1], GRAY, 3, 10)
    c.arrow(cen[1][0] + 82, cen[1][1], cen[2][0] - 82, cen[2][1], GRAY, 3, 10)
    # Down from experimentation to analysis
    c.arrow(cen[2][0], 130 + 4, cen2[0][0], 250 - 4, GRAY, 3, 10)
    # Bottom row R->L (analysis -> documentation -> dissemination)
    c.arrow(cen2[0][0] - 82, cen2[0][1], cen2[1][0] + 82, cen2[1][1], GRAY, 3, 10)
    c.arrow(cen2[1][0] - 82, cen2[1][1], cen2[2][0] + 82, cen2[2][1], GRAY, 3, 10)
    # Feedback loop dissemination -> hypothesis
    c.arrow(cen2[2][0], 250 - 4, cen[0][0], 130 + 4, DARK_GREEN, 3, 10)
    c.text(70, 190, "feedback: results inform next study", DARK_GREEN, 1)

    # Provenance capture banner
    c.rect(300, 340, 460, 385, GOLD, LIGHT_GOLD)
    c.text_c(380, 352, "Provenance captured", BLACK, 1)
    c.text_c(380, 368, "throughout (reproducibility)", GRAY, 1)

    c.text(40, 422, "Figure 3: A closed-loop workflow with provenance captured at every step", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Research_Workflow.png'))
    print("  Figure_3_Research_Workflow.png done")


def gen_fig4():
    """Figure 4: Layered framework for responsible AI in research."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "A Layered Framework for Responsible AI in Research", BLACK, 2)

    layers = [
        ("Community Norms", "Disclosure, integrity, authorship, equitable access", PURPLE, LIGHT_PURPLE),
        ("Institutional Governance", "Policies, secure infrastructure, aligned incentives", DARK_GREEN, LIGHT_GREEN),
        ("Technical Safeguards", "Bias auditing, provenance, privacy-preserving methods", MED_BLUE, LIGHT_BLUE),
    ]
    lx1, lx2 = 60, 520
    top = 55
    lh = 62
    gap = 16
    for i, (title, sub, col, fill) in enumerate(layers):
        y1 = top + i * (lh + gap)
        y2 = y1 + lh
        c.rect(lx1, y1, lx2, y2, col, fill)
        c.text_c((lx1 + lx2) // 2, y1 + 18, title, BLACK, 1)
        c.text_c((lx1 + lx2) // 2, y1 + 38, sub, GRAY, 1)

    # Bracket: layers jointly constrain AI use
    c.text_c((lx1 + lx2) // 2, top + 3 * (lh + gap) + 4, "Layers jointly constrain AI use", GRAY, 1)

    # Right column: the five dilemmas addressed
    dx1, dx2 = 560, 745
    c.text_c((dx1 + dx2) // 2, top - 2, "Dilemmas Addressed", BLACK, 1)
    dilemmas = [
        ("Algorithmic bias", RED, LIGHT_RED),
        ("Privacy & security", ORANGE, LIGHT_ORANGE),
        ("Reproducibility", DARK_BLUE, PALE_BLUE),
        ("Academic integrity", DARK_GREEN, LIGHT_GREEN),
        ("Digital divide", PURPLE, LIGHT_PURPLE),
    ]
    dy = top + 14
    dh = 34
    dgap = 8
    for i, (name, col, fill) in enumerate(dilemmas):
        y1 = dy + i * (dh + dgap)
        c.rect(dx1, y1, dx2, y1 + dh, col, fill)
        c.text_c((dx1 + dx2) // 2, y1 + 12, name, BLACK, 1)
    # connector from layer stack to dilemmas
    c.arrow(lx2 + 4, top + lh, dx1 - 4, dy + 2 * (dh + dgap), GRAY, 2, 9)

    # Foundation bar
    c.rect(60, 400, 745, 438, GOLD, LIGHT_GOLD)
    c.text_c(402, 410, "Human-centred, responsible scholarship (Education 5.0)", BLACK, 1)
    c.text_c(402, 426, "Capability and responsibility held together", GRAY, 1)

    c.text(40, 458, "Figure 4: Technical, institutional, and community layers jointly govern AI use in research", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Responsible_AI_Framework.png'))
    print("  Figure_4_Responsible_AI_Framework.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating research-support chapter figures...")
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
