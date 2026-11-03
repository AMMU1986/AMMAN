#!/usr/bin/env python3
"""
Generate 5 figure images (PNG) for the chapter
"Sequence Analysis, Motif Discovery, and Functional Annotation".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py
so it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - Orthology vs paralogy and implications for inference
  Figure 2 - MSA -> per-residue conservation profile
  Figure 3 - Geometric catalytic-template matching (sequence-invisible)
  Figure 4 - Pathway contextualization: bottleneck vs redundant node
  Figure 5 - Integrated target-prioritization workflow
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/sequence_figures'


def gen_fig1():
    """Figure 1: Orthology vs paralogy gene tree and inference implications."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Orthology, Paralogy, and Functional Inference", BLACK, 2)

    # Ancestral gene node
    anc_x, anc_y = 380, 60
    c.circle(anc_x, anc_y, 10, DARK_BLUE, PALE_BLUE)
    c.text_c(anc_x, 38, "Ancestral enzyme gene", BLACK, 1)

    # Duplication event -> two paralog lineages
    dup_y = 120
    c.line(anc_x, anc_y + 10, 240, dup_y, GRAY, 2)
    c.line(anc_x, anc_y + 10, 520, dup_y, GRAY, 2)
    c.circle(240, dup_y, 8, PURPLE, LIGHT_PURPLE)
    c.circle(520, dup_y, 8, PURPLE, LIGHT_PURPLE)
    c.text_c(140, dup_y, "Duplication", PURPLE, 1)
    c.text_c(615, dup_y, "(gene duplication)", PURPLE, 1)

    # Speciation of each lineage -> orthologs across species
    def speciation(px, py, color, fill, labels):
        sy = py + 80
        lx, rx = px - 70, px + 70
        c.line(px, py + 8, lx, sy, GRAY, 2)
        c.line(px, py + 8, rx, sy, GRAY, 2)
        c.circle(lx, sy, 14, color, fill)
        c.circle(rx, sy, 14, color, fill)
        c.text_c(lx, sy + 24, labels[0], BLACK, 1)
        c.text_c(rx, sy + 24, labels[1], BLACK, 1)
        return (lx, sy), (rx, sy)

    la = speciation(240, dup_y, MED_GREEN, LIGHT_GREEN, ["Sp.A / geneX", "Sp.B / geneX"])
    lb = speciation(520, dup_y, ORANGE, LIGHT_ORANGE, ["Sp.A / geneY", "Sp.B / geneY"])

    # Ortholog bracket (same color lineage, across species)
    c.line(la[0][0], 250, la[1][0], 250, MED_GREEN, 2)
    c.text_c(240, 258, "ORTHOLOGS - same function", DARK_GREEN, 1)
    c.line(lb[0][0], 250, lb[1][0], 250, ORANGE, 2)
    c.text_c(520, 258, "ORTHOLOGS - same function", ORANGE, 1)

    # Paralog bracket (across the two lineages)
    c.line(la[1][0], 285, lb[0][0], 285, PURPLE, 2)
    c.text_c(380, 293, "PARALOGS - may have diverged function", PURPLE, 1)

    # Implications box
    c.rect(60, 320, 700, 430, GOLD, LIGHT_GOLD)
    c.text_c(380, 332, "Implications for drug-target inference", BLACK, 1)
    c.text(80, 352, "Orthologs: safe transfer of function + druggable-site information", DARK_GREEN, 1)
    c.text(80, 372, "Paralogs: verify - substrate specificity / binding site may differ", PURPLE, 1)
    c.text(80, 392, "Misreading a paralog as an ortholog -> wrong function, wrong pocket", RED, 1)
    c.text(80, 412, "Correct evolutionary context decides which features are recognized", BLACK, 1)

    c.text(40, 452, "Figure 1: Orthologs (conserved function) versus paralogs (possible divergence)", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Orthology_Paralogy.png'))
    print("  Figure_1_Orthology_Paralogy.png done")


def gen_fig2():
    """Figure 2: MSA to per-residue conservation profile."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "From Multiple Sequence Alignment to Conservation Profile", BLACK, 2)

    # (a) alignment block of colored residues
    c.text(30, 38, "(a) Multiple sequence alignment (enzyme family)", BLACK, 1)
    cols = 16
    rows = 6
    cell = 26
    x0, y0 = 60, 58
    # define columns: some fully conserved (catalytic), some variable
    # 0=conserved catalytic, 1=conserved core, 2=variable
    coltype = [1,2,1,0,2,1,2,2,0,1,2,1,2,0,2,1]
    colors_for = {
        0: (RED, LIGHT_RED),        # catalytic (invariant)
        1: (MED_BLUE, LIGHT_BLUE),  # conserved core
        2: (GRAY, LIGHT_GRAY),      # variable
    }
    import random
    random.seed(11)
    for r in range(rows):
        for cc in range(cols):
            x = x0 + cc * cell
            y = y0 + r * (cell - 6)
            t = coltype[cc]
            outline, fill = colors_for[t]
            # variable columns get occasional different shade per row
            if t == 2 and random.random() < 0.5:
                fill = PALE_BLUE
            c.rect(x, y, x + cell - 4, y + cell - 8, outline, fill)
    # mark catalytic columns
    for cc in range(cols):
        if coltype[cc] == 0:
            x = x0 + cc * cell + (cell - 4) // 2
            c.arrow(x, y0 + rows * (cell - 6) + 20, x, y0 + rows * (cell - 6) + 4, RED, 2, 7)

    # (b) conservation profile bar chart aligned under the columns
    prof_top = 300
    c.text(30, prof_top - 24, "(b) Per-residue conservation (low entropy = conserved)", BLACK, 1)
    axis_y = prof_top + 110
    c.hline(x0, x0 + cols * cell, axis_y, BLACK)
    c.vline(x0 - 6, prof_top, axis_y, BLACK)
    c.text(10, prof_top + 40, "Cons.", BLACK, 1)
    heights = {0: 100, 1: 70, 2: 25}
    for cc in range(cols):
        x = x0 + cc * cell
        t = coltype[cc]
        h = heights[t] + (5 if t == 2 else 0)
        outline, fill = colors_for[t]
        c.rect(x, axis_y - h, x + cell - 4, axis_y, outline, fill)

    # legend
    c.rect(560, 60, 740, 180, LIGHT_GRAY, (250, 250, 250))
    c.text(572, 70, "Legend", BLACK, 1)
    c.rect(572, 90, 590, 104, RED, LIGHT_RED); c.text(596, 92, "Catalytic (invariant)", BLACK, 1)
    c.rect(572, 112, 590, 126, MED_BLUE, LIGHT_BLUE); c.text(596, 114, "Conserved core", BLACK, 1)
    c.rect(572, 134, 590, 148, GRAY, LIGHT_GRAY); c.text(596, 136, "Variable (specificity)", BLACK, 1)
    c.text(572, 158, "-> prioritize residues", DARK_GREEN, 1)

    c.text(40, 452, "Figure 2: Alignment columns map to conservation scores revealing catalytic vs variable sites", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Conservation_Profile.png'))
    print("  Figure_2_Conservation_Profile.png done")


def gen_fig3():
    """Figure 3: Geometric catalytic-template matching across low sequence identity."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Geometric Catalytic-Template Matching", BLACK, 2)

    # Left: query structure with catalytic residues; right: template
    c.text(90, 42, "Query enzyme (predicted structure)", BLACK, 1)
    c.text(500, 42, "Catalytic template (M-CSA)", BLACK, 1)

    # query blob
    c.circle(170, 170, 95, MED_BLUE, PALE_BLUE)
    # catalytic triad positions (a small constellation)
    q = [(140, 140), (205, 150), (175, 210)]
    qlabels = ["Ser", "His", "Asp"]
    for (px, py), lab in zip(q, qlabels):
        c.circle(px, py, 10, RED, LIGHT_RED)
        c.text_c(px, py - 18, lab, BLACK, 1)
    # draw triangle between them (geometry)
    for i in range(3):
        a = q[i]; b = q[(i + 1) % 3]
        c.line(a[0], a[1], b[0], b[1], RED, 2)

    # template blob (different fold/sequence)
    c.circle(590, 170, 95, DARK_GREEN, LIGHT_GREEN)
    t = [(560, 138), (625, 152), (596, 212)]
    for (px, py), lab in zip(t, qlabels):
        c.circle(px, py, 10, RED, LIGHT_RED)
        c.text_c(px, py - 18, lab, BLACK, 1)
    for i in range(3):
        a = t[i]; b = t[(i + 1) % 3]
        c.line(a[0], a[1], b[0], b[1], RED, 2)

    # matching arrows (geometry equivalence)
    c.arrow(275, 160, 480, 160, PURPLE, 3, 11)
    c.text_c(380, 142, "superpose 3-6 residue", PURPLE, 1)
    c.text_c(380, 156, "constellation", PURPLE, 1)
    c.text_c(380, 190, "RMSD within tolerance", GRAY, 1)

    # sequence-identity note
    c.rect(120, 300, 640, 360, GOLD, LIGHT_GOLD)
    c.text_c(380, 312, "Sequence identity < 40%  ->  sequence motifs FAIL", RED, 1)
    c.text_c(380, 332, "Geometry conserved  ->  functional match DETECTED", DARK_GREEN, 1)
    c.text_c(380, 348, "captures convergent evolution AND remote divergence", GRAY, 1)

    # downstream
    c.rect(220, 380, 540, 430, MED_GREEN, LIGHT_GREEN)
    c.text_c(380, 394, "Active-site geometry defined", BLACK, 1)
    c.text_c(380, 412, "-> guides pharmacophore design", GRAY, 1)

    c.text(40, 452, "Figure 3: A small residue constellation matches despite undetectable sequence similarity", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Template_Matching.png'))
    print("  Figure_3_Template_Matching.png done")


def gen_fig4():
    """Figure 4: Pathway contextualization - bottleneck vs redundant node."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Pathway Context: Druggable Bottleneck vs Redundant Node", BLACK, 2)

    def node(cx, cy, label, color, fill, r=22):
        c.circle(cx, cy, r, color, fill)
        c.text_c(cx, cy - 3, label, BLACK, 1)

    # (a) bottleneck pathway (top)
    c.text(30, 44, "(a) Bottleneck / rate-limiting node - good target", BLACK, 1)
    ys = 100
    xs = [90, 230, 370, 510, 650]
    labels = ["S", "A", "E*", "B", "P"]
    cols = [(MED_BLUE, LIGHT_BLUE)] * 5
    cols[2] = (RED, LIGHT_RED)
    for i, (x, lab, (co, fi)) in enumerate(zip(xs, labels, cols)):
        node(x, ys, lab, co, fi)
        if i < len(xs) - 1:
            c.arrow(x + 24, ys, xs[i + 1] - 24, ys, GRAY, 2, 9)
    c.text_c(370, 140, "single route - inhibiting E* blocks flux to product P", DARK_GREEN, 1)
    # inhibitor marker
    c.text_c(370, 66, "inhibitor", RED, 1)
    c.arrow(370, 74, 370, ys - 24, RED, 2, 8)

    # (b) redundant pathway (bottom)
    c.text(30, 210, "(b) Redundant node - inhibition is buffered - poor target", BLACK, 1)
    yb = 300
    node(90, yb, "S", MED_BLUE, LIGHT_BLUE)
    node(650, yb, "P", MED_BLUE, LIGHT_BLUE)
    # two parallel routes
    node(300, yb - 55, "E1*", RED, LIGHT_RED)
    node(300, yb + 55, "E2", MED_GREEN, LIGHT_GREEN)
    node(470, yb - 55, "B1", MED_BLUE, LIGHT_BLUE)
    node(470, yb + 55, "B2", MED_BLUE, LIGHT_BLUE)
    c.arrow(114, yb - 8, 280, yb - 50, GRAY, 2, 8)
    c.arrow(114, yb + 8, 280, yb + 50, GRAY, 2, 8)
    c.arrow(322, yb - 55, 448, yb - 55, GRAY, 2, 8)
    c.arrow(322, yb + 55, 448, yb + 55, GRAY, 2, 8)
    c.arrow(492, yb - 50, 628, yb - 8, GRAY, 2, 8)
    c.arrow(492, yb + 50, 628, yb + 8, GRAY, 2, 8)
    c.text_c(220, yb - 55, "inhibitor", RED, 1)
    c.arrow(252, yb - 55, 277, yb - 55, RED, 2, 7)
    c.text_c(300, yb + 95, "parallel route compensates", MED_GREEN, 1)

    c.text(40, 452, "Figure 4: Network position determines whether inhibition produces a useful perturbation", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Pathway_Context.png'))
    print("  Figure_4_Pathway_Context.png done")


def gen_fig5():
    """Figure 5: Integrated target-prioritization workflow."""
    c = PNGCanvas(760, 480)
    c.text_c(380, 10, "Integrated Enzyme Target-Prioritization Workflow", BLACK, 2)

    # Four evidence inputs (left column)
    inputs = [
        ("Active-site\nconservation", MED_BLUE, LIGHT_BLUE),
        ("Catalytic motif /\ntemplate match", MED_GREEN, LIGHT_GREEN),
        ("Human-homolog\nsimilarity", ORANGE, LIGHT_ORANGE),
        ("Pathway\nposition", PURPLE, LIGHT_PURPLE),
    ]
    ix1, ix2 = 30, 230
    top = 60
    bh = 70
    gap = 20
    centers = []
    for i, (title, col, fill) in enumerate(inputs):
        y1 = top + i * (bh + gap)
        c.rect(ix1, y1, ix2, y1 + bh, col, fill)
        for j, ln in enumerate(title.split('\n')):
            c.text_c((ix1 + ix2) // 2, y1 + 22 + j * 16, ln, BLACK, 1)
        centers.append((ix2, y1 + bh // 2))

    # Central integration/scoring node
    sx1, sx2 = 300, 470
    sy1, sy2 = 170, 290
    c.rect(sx1, sy1, sx2, sy2, GOLD, LIGHT_GOLD)
    c.text_c((sx1 + sx2) // 2, sy1 + 24, "WEIGHTED", BLACK, 1)
    c.text_c((sx1 + sx2) // 2, sy1 + 42, "INTEGRATION", BLACK, 1)
    c.text_c((sx1 + sx2) // 2, sy1 + 66, "& SCORING", BLACK, 1)
    c.text_c((sx1 + sx2) // 2, sy1 + 90, "(transparent,", GRAY, 1)
    c.text_c((sx1 + sx2) // 2, sy1 + 104, "documented)", GRAY, 1)
    for (ex, ey) in centers:
        c.arrow(ex + 2, ey, sx1 - 2, (sy1 + sy2) // 2, GRAY, 2, 8)

    # Tiered output (right column)
    tiers = [
        ("HIGH - advance to SBDD", DARK_GREEN, LIGHT_GREEN),
        ("INTERMEDIATE - gather evidence", GOLD, LIGHT_GOLD),
        ("CONDITIONAL - if selectivity OK", ORANGE, LIGHT_ORANGE),
        ("LOW - deprioritize", RED, LIGHT_RED),
    ]
    tx1, tx2 = 520, 735
    ttop = 70
    tbh = 60
    tgap = 16
    for i, (title, col, fill) in enumerate(tiers):
        y1 = ttop + i * (tbh + tgap)
        c.rect(tx1, y1, tx2, y1 + tbh, col, fill)
        c.text_c((tx1 + tx2) // 2, y1 + tbh // 2 - 4, title, BLACK, 1)
    c.arrow(sx2 + 2, (sy1 + sy2) // 2, tx1 - 2, ttop + 2 * (tbh + tgap) - 20, GRAY, 3, 10)
    c.text_c((sx1 + sx2) // 2, sy2 + 18, "tiered classification", PURPLE, 1)

    # downstream handoff note
    c.rect(300, 330, 470, 430, DARK_GREEN, LIGHT_GREEN)
    c.text_c(385, 344, "Feeds downstream", BLACK, 1)
    c.text_c(385, 364, "- docking constraints", GRAY, 1)
    c.text_c(385, 380, "- allosteric-site", GRAY, 1)
    c.text_c(385, 394, "  candidates", GRAY, 1)
    c.text_c(385, 410, "- selectivity reqs", GRAY, 1)
    c.arrow((sx1 + sx2) // 2, sy2 + 24, 385, 330 - 2, DARK_GREEN, 2, 8)

    c.text(40, 462, "Figure 5: Conservation, motif, homology, and pathway evidence combine into tiered priorities", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_5_Prioritization.png'))
    print("  Figure_5_Prioritization.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating sequence-analysis chapter figures...")
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
