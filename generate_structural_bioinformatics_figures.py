#!/usr/bin/env python3
"""
Generate 5 figure images (PNG) for the chapter
"Comparative and Structural Bioinformatics of Enzymes".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py
so it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - Comparative bioinformatics workflow (sequence -> fold recognition
             -> structural superposition)
  Figure 2 - Experimental and computational routes to enzyme structures
             converging on validation
  Figure 3 - Binding-site detection, characterization, and druggability
             assessment workflow
  Figure 4 - Structural dynamics: conformational ensembles, collective motions,
             and allosteric communication
  Figure 5 - Integrated comparative/structural bioinformatics pipeline to
             structure-based drug design
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/structural_figures'


def gen_fig1():
    """Figure 1: Comparative bioinformatics workflow for enzyme analysis."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Comparative Bioinformatics Workflow for Enzymes", BLACK, 2)

    # Vertical pipeline of stages with escalating sensitivity
    stages = [
        ("Target Enzyme Sequence", "Query from UniProt / GenBank",
         DARK_BLUE, PALE_BLUE),
        ("Pairwise & Database Search", "BLAST homologue detection (>30% id)",
         MED_BLUE, LIGHT_BLUE),
        ("Profile / HMM Search", "PSI-BLAST, HMM - twilight zone",
         MED_GREEN, LIGHT_GREEN),
        ("Fold Recognition (Threading)", "Remote homologues, no sequence signal",
         ORANGE, LIGHT_ORANGE),
        ("Structural Superposition", "RMSD / TM-score, conserved motifs",
         PURPLE, LIGHT_PURPLE),
    ]
    bx1, bx2 = 210, 560
    top = 55
    bh = 56
    gap = 18
    for i, (title, sub, col, fill) in enumerate(stages):
        y1 = top + i * (bh + gap)
        y2 = y1 + bh
        c.rect(bx1, y1, bx2, y2, col, fill)
        c.text_c((bx1 + bx2) // 2, y1 + 16, title, BLACK, 1)
        c.text_c((bx1 + bx2) // 2, y1 + 34, sub, GRAY, 1)
        if i < len(stages) - 1:
            midx = (bx1 + bx2) // 2
            c.arrow(midx, y2 + 2, midx, y2 + gap - 2, GRAY, 3, 9)

    # Sensitivity indicator on the left
    c.arrow(70, top + 4 * (bh + gap) + bh, 70, top, DARK_GREEN, 3, 11)
    c.text(20, top + 150, "Increasing", DARK_GREEN, 1)
    c.text(20, top + 164, "detection", DARK_GREEN, 1)
    c.text(20, top + 178, "sensitivity", DARK_GREEN, 1)

    # Outcome box on the right
    c.rect(600, 120, 745, 300, GOLD, LIGHT_GOLD)
    c.text_c(672, 132, "Outcome", BLACK, 1)
    c.text_c(672, 152, "Template", BLACK, 1)
    c.text_c(672, 166, "identified +", BLACK, 1)
    c.text_c(672, 180, "aligned", BLACK, 1)
    c.text_c(672, 206, "Confidence", BLACK, 1)
    c.text_c(672, 220, "calibrated to", BLACK, 1)
    c.text_c(672, 234, "identity", BLACK, 1)
    c.text_c(672, 260, "Feeds", BLACK, 1)
    c.text_c(672, 274, "homology", BLACK, 1)
    c.text_c(672, 288, "modelling", BLACK, 1)
    c.arrow(560, 250, 600, 200, GRAY, 2, 8)

    c.text(40, 452, "Figure 1: Layered comparative analysis from sequence search to structural superposition", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Comparative_Workflow.png'))
    print("  Figure_1_Comparative_Workflow.png done")


def gen_fig2():
    """Figure 2: Experimental and computational routes converging on validation."""
    c = PNGCanvas(760, 480)
    c.text_c(380, 10, "Routes to Enzyme Structures and Model Validation", BLACK, 2)

    # Two branches at top: experimental (left) and computational (right)
    c.text_c(200, 42, "Experimental Determination", DARK_BLUE, 1)
    c.text_c(560, 42, "Computational Prediction", DARK_GREEN, 1)

    exp = [
        ("X-ray Crystallography", "1-3 Angstrom, ligand complexes", MED_BLUE, LIGHT_BLUE),
        ("Cryo-EM", "Large complexes, multiple states", DARK_BLUE, PALE_BLUE),
        ("NMR Spectroscopy", "Small proteins, solution dynamics", PURPLE, LIGHT_PURPLE),
    ]
    comp = [
        ("Homology Modelling", "Template-based, identity-dependent", MED_GREEN, LIGHT_GREEN),
        ("Threading / Fold Rec.", "No clear template", GOLD, LIGHT_GOLD),
        ("Deep Learning (AlphaFold)", "Proteome-scale, high accuracy", ORANGE, LIGHT_ORANGE),
    ]

    bw = 320
    bh = 46
    top = 60
    gap = 14
    lx = 40
    rx = 400
    for i, (title, sub, col, fill) in enumerate(exp):
        y1 = top + i * (bh + gap)
        c.rect(lx, y1, lx + bw, y1 + bh, col, fill)
        c.text_c(lx + bw // 2, y1 + 13, title, BLACK, 1)
        c.text_c(lx + bw // 2, y1 + 29, sub, GRAY, 1)
    for i, (title, sub, col, fill) in enumerate(comp):
        y1 = top + i * (bh + gap)
        c.rect(rx, y1, rx + bw, y1 + bh, col, fill)
        c.text_c(rx + bw // 2, y1 + 13, title, BLACK, 1)
        c.text_c(rx + bw // 2, y1 + 29, sub, GRAY, 1)

    # Converging arrows to validation box
    conv_y = top + 3 * (bh + gap) + 20
    val_x1, val_x2 = 250, 510
    val_y1, val_y2 = conv_y, conv_y + 70
    c.arrow(lx + bw // 2, top + 3 * (bh + gap) - 4, (val_x1 + val_x2) // 2 - 30, val_y1 - 4, MED_BLUE, 3, 10)
    c.arrow(rx + bw // 2, top + 3 * (bh + gap) - 4, (val_x1 + val_x2) // 2 + 30, val_y1 - 4, MED_GREEN, 3, 10)
    c.rect(val_x1, val_y1, val_x2, val_y2, RED, LIGHT_RED)
    c.text_c((val_x1 + val_x2) // 2, val_y1 + 14, "MODEL VALIDATION", BLACK, 1)
    c.text_c((val_x1 + val_x2) // 2, val_y1 + 32, "Ramachandran, statistical potentials,", GRAY, 1)
    c.text_c((val_x1 + val_x2) // 2, val_y1 + 46, "per-residue confidence, active-site check", GRAY, 1)

    # Down arrow to SBDD
    midx = (val_x1 + val_x2) // 2
    c.arrow(midx, val_y2 + 2, midx, val_y2 + 30, GRAY, 3, 10)
    sb_y1 = val_y2 + 32
    c.rect(val_x1 - 20, sb_y1, val_x2 + 20, sb_y1 + 50, DARK_GREEN, LIGHT_GREEN)
    c.text_c(midx, sb_y1 + 15, "Structure-Based Drug Design", BLACK, 1)
    c.text_c(midx, sb_y1 + 32, "Docking / virtual screening / optimization", GRAY, 1)

    c.text(40, 462, "Figure 2: Experimental and computational routes converge on validation before SBDD", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Structure_Routes.png'))
    print("  Figure_2_Structure_Routes.png done")


def gen_fig3():
    """Figure 3: Binding-site detection, characterization, druggability."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Enzyme Binding-Site Detection and Druggability", BLACK, 2)

    # (a) schematic enzyme surface with pockets on the left
    c.text(30, 40, "(a) Enzyme surface with pockets", BLACK, 1)
    cx, cy = 150, 180
    c.circle(cx, cy, 95, DARK_BLUE, PALE_BLUE)
    # orthosteric (deep) pocket
    c.circle(130, 150, 26, ORANGE, LIGHT_ORANGE)
    c.text_c(130, 146, "Active", BLACK, 1)
    c.text_c(130, 158, "site", BLACK, 1)
    # allosteric pocket
    c.circle(200, 220, 20, PURPLE, LIGHT_PURPLE)
    c.text_c(200, 216, "Allo-", BLACK, 1)
    c.text_c(200, 228, "steric", BLACK, 1)
    # cryptic (dashed look) pocket
    c.circle(95, 235, 14, GRAY, LIGHT_GRAY)
    c.text_c(95, 231, "Cryptic", BLACK, 1)
    c.text(55, 290, "Catalytic residues (conserved)", RED, 1)

    # (b) characterization steps on the right (pipeline)
    c.text(430, 40, "(b) Characterization pipeline", BLACK, 1)
    steps = [
        ("Pocket Detection", "Geometric / energetic cavity search", MED_BLUE, LIGHT_BLUE),
        ("Physicochemical Profile", "Volume, enclosure, hydrophobicity, H-bonds", MED_GREEN, LIGHT_GREEN),
        ("Conservation Mapping", "Catalytic vs variable residues", ORANGE, LIGHT_ORANGE),
        ("Druggability Score", "Quantitative tractability estimate", PURPLE, LIGHT_PURPLE),
    ]
    sx1, sx2 = 400, 735
    top = 60
    bh = 52
    gap = 14
    for i, (title, sub, col, fill) in enumerate(steps):
        y1 = top + i * (bh + gap)
        c.rect(sx1, y1, sx2, y1 + bh, col, fill)
        c.text_c((sx1 + sx2) // 2, y1 + 15, title, BLACK, 1)
        c.text_c((sx1 + sx2) // 2, y1 + 33, sub, GRAY, 1)
        if i < len(steps) - 1:
            midx = (sx1 + sx2) // 2
            c.arrow(midx, y1 + bh + 2, midx, y1 + bh + gap - 2, GRAY, 2, 8)

    # go/no-go box at bottom
    c.rect(220, 360, 540, 420, GOLD, LIGHT_GOLD)
    c.text_c(380, 374, "Go / No-Go Decision", BLACK, 1)
    c.text_c(380, 394, "Druggable pocket + mechanistic rationale", GRAY, 1)
    c.text_c(380, 408, "+ selectivity prospect -> prioritize", GRAY, 1)
    c.arrow(567, 320, 500, 360, GRAY, 2, 8)
    c.arrow(150, 280, 230, 375, GRAY, 2, 8)

    c.text(40, 452, "Figure 3: From pocket detection through characterization to druggability-driven decision", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Druggability.png'))
    print("  Figure_3_Druggability.png done")


def gen_fig4():
    """Figure 4: Structural dynamics - ensembles, collective motions, allostery."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Structural Dynamics and Allosteric Communication", BLACK, 2)

    # (a) conformational ensemble / energy landscape
    c.text(30, 40, "(a) Conformational ensemble", BLACK, 1)
    # energy landscape curve with two minima
    ax0, ay0 = 50, 230
    c.vline(ax0, 70, ay0, BLACK)
    c.hline(ax0, 360, ay0, BLACK)
    c.text(10, 140, "Free", BLACK, 1)
    c.text(10, 154, "energy", BLACK, 1)
    c.text(250, ay0 + 28, "Conformation", BLACK, 1)
    prev = None
    for x in range(ax0 + 5, 360):
        t = (x - ax0) / 310.0
        # double-well landscape
        y = ay0 - int(110 * (0.5 + 0.5 * math.cos(2 * math.pi * (t - 0.1)))
                      * (0.6 + 0.4 * math.exp(-((t - 0.5) ** 2) / 0.08)))
        if prev is not None:
            c.line(prev[0], prev[1], x, y, MED_BLUE, 2)
        prev = (x, y)
    # state labels
    c.circle(130, 150, 7, ORANGE, LIGHT_ORANGE)
    c.text(100, 120, "Closed", ORANGE, 1)
    c.circle(290, 150, 7, DARK_GREEN, LIGHT_GREEN)
    c.text(270, 120, "Open", DARK_GREEN, 1)
    c.text(90, 250, "Cryptic pocket opens in open state", GRAY, 1)

    # (b) collective motion (hinge-bending) via NMA
    c.text(420, 40, "(b) Collective motion (NMA)", BLACK, 1)
    # two domains connected by a hinge, arrows showing hinge-bend
    c.circle(500, 130, 34, DARK_BLUE, PALE_BLUE)
    c.text_c(500, 126, "Dom A", BLACK, 1)
    c.circle(640, 130, 34, DARK_BLUE, PALE_BLUE)
    c.text_c(640, 126, "Dom B", BLACK, 1)
    c.circle(570, 160, 12, GOLD, LIGHT_GOLD)
    c.text_c(570, 185, "hinge", BLACK, 1)
    c.line(534, 135, 558, 155, GRAY, 2)
    c.line(606, 135, 582, 155, GRAY, 2)
    # motion arrows
    c.arrow(500, 90, 470, 75, RED, 2, 8)
    c.arrow(640, 90, 670, 75, RED, 2, 8)
    c.text(520, 60, "low-frequency mode", RED, 1)

    # (c) allosteric communication network
    c.text(30, 300, "(c) Allosteric communication pathway", BLACK, 1)
    c.rect(30, 315, 730, 420, LIGHT_GRAY, (250, 250, 250))
    # nodes
    nodes = [(80, 390), (150, 350), (230, 380), (320, 345),
             (410, 375), (500, 350), (590, 380), (680, 355)]
    # edges along path
    for i in range(len(nodes) - 1):
        c.line(nodes[i][0], nodes[i][1], nodes[i + 1][0], nodes[i + 1][1], MED_GREEN, 2)
    for i, (nx, ny) in enumerate(nodes):
        col = PURPLE if i == 0 else (ORANGE if i == len(nodes) - 1 else MED_BLUE)
        fill = LIGHT_PURPLE if i == 0 else (LIGHT_ORANGE if i == len(nodes) - 1 else LIGHT_BLUE)
        c.circle(nx, ny, 10, col, fill)
    c.text(55, 365, "Allosteric", PURPLE, 1)
    c.text(55, 405, "site", PURPLE, 1)
    c.text(650, 330, "Active", ORANGE, 1)
    c.text(650, 405, "site", ORANGE, 1)
    c.text(300, 405, "signal propagation via dynamic network", GRAY, 1)

    c.text(40, 452, "Figure 4: Ensembles, collective motions, and allosteric signal propagation in enzymes", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Dynamics.png'))
    print("  Figure_4_Dynamics.png done")


def gen_fig5():
    """Figure 5: Integrated pipeline linking analysis to structure-based design."""
    c = PNGCanvas(760, 480)
    c.text_c(380, 10, "Integrated Structural Bioinformatics Pipeline for Drug Design", BLACK, 2)

    stages = [
        ("Target Sequence &\nComparative Analysis", DARK_BLUE, PALE_BLUE),
        ("Structure Determination\nor Prediction", MED_BLUE, LIGHT_BLUE),
        ("Binding-Site\nCharacterization", MED_GREEN, LIGHT_GREEN),
        ("Structural Dynamics\n& Ensembles", ORANGE, LIGHT_ORANGE),
        ("Selectivity &\nPrioritization", PURPLE, LIGHT_PURPLE),
        ("Structure-Based\nDrug Design", RED, LIGHT_RED),
    ]
    bw, bh = 210, 64
    positions = [
        (40, 60), (280, 60), (520, 60),
        (520, 180), (280, 180), (40, 180),
    ]
    centers = []
    for (title, col, fill), (bx, by) in zip(stages, positions):
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        lines = title.split('\n')
        for j, ln in enumerate(lines):
            c.text_c(bx + bw // 2, by + 18 + j * 16, ln, BLACK, 1)
        centers.append((bx + bw // 2, by + bh // 2, bx, by))

    # Arrows along the snake path 0->1->2 (top row L->R), 2->3 (down),
    # 3->4->5 (bottom row R->L)
    def edge(a, b, color=GRAY):
        ax, ay, abx, aby = centers[a]
        bx, by, bbx, bby = centers[b]
        if ay == by and bx > ax:          # left-to-right
            c.arrow(abx + bw + 2, ay, bbx - 2, by, color, 3, 10)
        elif ay == by and bx < ax:        # right-to-left
            c.arrow(abx - 2, ay, bbx + bw + 2, by, color, 3, 10)
        else:                              # vertical (top to bottom row)
            c.arrow(ax, aby + bh + 2, bx, bby - 2, color, 3, 10)

    edge(0, 1); edge(1, 2); edge(2, 3); edge(3, 4); edge(4, 5)

    # Feedback arrow from SBDD back up to structure (iterative refinement)
    sx, sy, sbx, sby = centers[5]
    c.line(sbx, sby + bh + 4, sbx, 320, DARK_GREEN, 2)
    c.line(sbx, 320, 630, 320, DARK_GREEN, 2)
    c.line(630, 320, 630, centers[1][1] + bh, DARK_GREEN, 2)
    c.arrow(630, centers[1][1] + bh, 630, centers[1][1] + bh - 4, DARK_GREEN, 2, 8)
    c.text(250, 310, "Iterative refinement: co-crystal structures feed back", DARK_GREEN, 1)

    # Comparative-context side note
    c.rect(60, 360, 700, 430, GOLD, LIGHT_GOLD)
    c.text_c(380, 374, "Comparative framework supplies context at every stage", BLACK, 1)
    c.text_c(380, 394, "which relatives inform the model - which features confer selectivity", GRAY, 1)
    c.text_c(380, 408, "- which pockets are tractable", GRAY, 1)

    c.text(40, 462, "Figure 5: Continuous flow from enzyme analysis to iterative structure-based drug design", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_5_Integrated_Pipeline.png'))
    print("  Figure_5_Integrated_Pipeline.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating structural bioinformatics chapter figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    gen_fig5()
    print(f"\nAll figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz / 1024:.1f} KB")


if __name__ == '__main__':
    main()
