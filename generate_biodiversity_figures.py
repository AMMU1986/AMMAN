#!/usr/bin/env python3
"""
Generate 4 figure images (PNG) for the chapter
"AI-Driven Prediction of Biodiversity Loss".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies in the sandbox (matplotlib is not
available and the environment has no external network access).

Figures:
  Figure 1 - Conceptual architecture of a cognitive digital twin for
             biodiversity forecasting (sensing -> fusion -> modelling ->
             prediction -> explanation -> decision, with a feedback loop)
  Figure 2 - Multi-source data acquisition and fusion pipeline (data cube)
  Figure 3 - Taxonomy of AI/ML methods + graph-neural-network species-range
             modelling workflow
  Figure 4 - Interacting-stressor cascade + forecast-to-decision pathway
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/biodiversity_figures'


def gen_fig1():
    """Figure 1: Cognitive digital twin architecture for biodiversity."""
    c = PNGCanvas(780, 470)
    c.text_c(390, 10, "Cognitive Digital Twin for Biodiversity Forecasting", BLACK, 2)

    # Five-stage horizontal pipeline
    stages = [
        ("MULTI-SOURCE", "SENSING", DARK_BLUE, PALE_BLUE,
         ["Satellite, IoT,", "acoustic, eDNA,", "citizen science"]),
        ("DATA FUSION", "& EBV CUBE", MED_BLUE, LIGHT_BLUE,
         ["Harmonise,", "gap-fill,", "co-register"]),
        ("AI MODELLING", "", DARK_GREEN, LIGHT_GREEN,
         ["SDM, CNN,", "GNN, Bayesian,", "hybrid models"]),
        ("PREDICTION &", "EXPLANATION", ORANGE, LIGHT_ORANGE,
         ["Risk forecasts,", "driver", "attribution"]),
        ("DECISION", "SUPPORT", PURPLE, LIGHT_PURPLE,
         ["Policy, finance,", "conservation", "action"]),
    ]

    bw, bh = 132, 118
    top = 90
    gap = 20
    left = 20
    centers = []
    for i, (l1, l2, col, fill, bullets) in enumerate(stages):
        bx = left + i * (bw + gap)
        c.rect(bx, top, bx + bw, top + bh, col, fill)
        c.text_c(bx + bw // 2, top + 12, l1, BLACK, 1)
        if l2:
            c.text_c(bx + bw // 2, top + 26, l2, BLACK, 1)
        for j, b in enumerate(bullets):
            c.text_c(bx + bw // 2, top + 52 + j * 14, b, GRAY, 1)
        centers.append((bx + bw // 2, bx, bx + bw))
        if i > 0:
            prev_r = centers[i - 1][2]
            c.arrow(prev_r + 2, top + bh // 2, bx - 2, top + bh // 2, DARK_BLUE, 3, 9)

    # "Virtual replica tracks the real ecosystem" band
    band_y = top + bh + 60
    c.rect(20, band_y, 760, band_y + 34, DARK_GREEN, LIGHT_GREEN)
    c.text_c(390, band_y + 13, "VIRTUAL REPLICA continuously tracks the REAL ECOSYSTEM", BLACK, 1)

    # Feedback / data-assimilation loop from decision back to sensing
    loop_y = top + bh + 26
    c.line(centers[4][0], top + bh, centers[4][0], loop_y, GRAY, 2)
    c.line(centers[4][0], loop_y, centers[0][0], loop_y, GRAY, 2)
    c.arrow(centers[0][0], loop_y, centers[0][0], top + bh + 2, GRAY, 2, 9)
    c.text_c(390, loop_y - 12, "Data-assimilation feedback loop (observe - compare - update)", GRAY, 1)

    # Inputs / outputs annotations
    c.text_c(86, top - 14, "Real-world observations", DARK_BLUE, 1)
    c.text_c(694, top - 14, "Anticipatory action", PURPLE, 1)

    c.text(20, 452, "Figure 1: Architecture of a cognitive digital twin for biodiversity forecasting", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Cognitive_Digital_Twin.png'))
    print("  Figure_1_Cognitive_Digital_Twin.png done")


def gen_fig2():
    """Figure 2: Multi-source data acquisition and fusion pipeline."""
    c = PNGCanvas(780, 470)
    c.text_c(390, 10, "Multi-Source Data Acquisition and Fusion Pipeline", BLACK, 2)

    # Left column: six data sources
    sources = [
        ("Satellite remote sensing", DARK_BLUE, PALE_BLUE),
        ("IoT ground sensors", MED_BLUE, LIGHT_BLUE),
        ("Passive acoustic monitoring", DARK_GREEN, LIGHT_GREEN),
        ("Camera-trap arrays", ORANGE, LIGHT_ORANGE),
        ("Environmental DNA", PURPLE, LIGHT_PURPLE),
        ("Citizen-science records", GOLD, LIGHT_GOLD),
    ]
    sx1, sx2 = 20, 210
    sy = 60
    sh = 46
    sgap = 12
    centers_r = []
    for i, (name, col, fill) in enumerate(sources):
        y1 = sy + i * (sh + sgap)
        c.rect(sx1, y1, sx2, y1 + sh, col, fill)
        c.text_c((sx1 + sx2) // 2, y1 + sh // 2 - 4, name, BLACK, 1)
        centers_r.append(y1 + sh // 2)

    # Middle: fusion / harmonisation engine
    fx1, fy1, fx2, fy2 = 300, 150, 470, 320
    c.rect(fx1, fy1, fx2, fy2, MED_BLUE, LIGHT_BLUE)
    c.text_c(385, 168, "FUSION ENGINE", BLACK, 1)
    c.text_c(385, 190, "Harmonise", GRAY, 1)
    c.text_c(385, 206, "Gap-fill", GRAY, 1)
    c.text_c(385, 222, "Co-register", GRAY, 1)
    c.text_c(385, 238, "Common grid", GRAY, 1)
    c.text_c(385, 262, "EBV semantic", DARK_GREEN, 1)
    c.text_c(385, 278, "alignment", DARK_GREEN, 1)

    for cy in centers_r:
        c.arrow(sx2 + 2, cy, fx1 - 2, (fy1 + fy2) // 2 + (cy - 235) // 6, GRAY, 1, 7)

    # Right: analysis-ready data cube (drawn as isometric stack)
    cube_x, cube_y = 560, 175
    cs = 90
    off = 26
    # back/top faces for a stacked-cube feel
    for k in range(3):
        ox = cube_x + k * 6
        oy = cube_y - k * 6
        c.rect(ox, oy, ox + cs, oy + cs, DARK_GREEN, LIGHT_GREEN)
    # top parallelogram
    c.line(cube_x, cube_y, cube_x + off, cube_y - off, DARK_GREEN, 2)
    c.line(cube_x + cs, cube_y, cube_x + cs + off, cube_y - off, DARK_GREEN, 2)
    c.line(cube_x + off, cube_y - off, cube_x + cs + off, cube_y - off, DARK_GREEN, 2)
    # right side
    c.line(cube_x + cs, cube_y, cube_x + cs + off, cube_y - off, DARK_GREEN, 2)
    c.line(cube_x + cs + off, cube_y - off, cube_x + cs + off, cube_y + cs - off, DARK_GREEN, 2)
    c.line(cube_x + cs, cube_y + cs, cube_x + cs + off, cube_y + cs - off, DARK_GREEN, 2)
    c.text_c(cube_x + cs // 2, cube_y + cs // 2 - 12, "ANALYSIS-", BLACK, 1)
    c.text_c(cube_x + cs // 2, cube_y + cs // 2 + 2, "READY", BLACK, 1)
    c.text_c(cube_x + cs // 2, cube_y + cs // 2 + 16, "DATA CUBE", BLACK, 1)
    c.text_c(cube_x + cs // 2 + 6, cube_y + cs + 24, "space x time x variable", GRAY, 1)

    c.arrow(fx2 + 2, (fy1 + fy2) // 2, cube_x - 4, cube_y + cs // 2, MED_BLUE, 3, 10)
    c.arrow(cube_x + cs + off + 4, cube_y + cs // 2, 745, cube_y + cs // 2, DARK_GREEN, 3, 10)
    c.text_c(720, cube_y + cs // 2 - 12, "to models", DARK_GREEN, 1)

    c.text_c(115, 44, "HETEROGENEOUS STREAMS", GRAY, 1)

    c.text(20, 452, "Figure 2: Acquisition and fusion of multi-source data into an analysis-ready cube", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Data_Fusion_Pipeline.png'))
    print("  Figure_2_Data_Fusion_Pipeline.png done")


def gen_fig3():
    """Figure 3: AI method taxonomy + GNN species-range workflow."""
    c = PNGCanvas(780, 470)
    c.text_c(390, 10, "AI Methods and a Graph-Neural-Network Range Workflow", BLACK, 2)

    # Left half: taxonomy tree
    c.text_c(195, 40, "Taxonomy of AI/ML methods", DARK_BLUE, 1)
    root = (150, 70, 240, 96)
    c.rect(*root, DARK_BLUE, PALE_BLUE)
    c.text_c(195, 78, "AI methods", BLACK, 1)

    leaves = [
        ("Species distribution models", MED_BLUE, LIGHT_BLUE),
        ("Convolutional networks", DARK_GREEN, LIGHT_GREEN),
        ("Temporal / recurrent models", ORANGE, LIGHT_ORANGE),
        ("Graph neural networks", PURPLE, LIGHT_PURPLE),
        ("Bayesian / hybrid models", RED, LIGHT_RED),
        ("Explainable AI overlays", GOLD, LIGHT_GOLD),
    ]
    lx1, lx2 = 40, 365
    ly = 120
    lh = 36
    lgap = 12
    spine_x = 24
    box_centers = [ly + i * (lh + lgap) + lh // 2 for i in range(len(leaves))]
    # trunk from root down and along a clean left spine
    c.line(195, 96, 195, 108, GRAY, 1)
    c.line(195, 108, spine_x, 108, GRAY, 1)
    c.line(spine_x, 108, spine_x, box_centers[-1], GRAY, 1)
    for i, (name, col, fill) in enumerate(leaves):
        y1 = ly + i * (lh + lgap)
        c.rect(lx1, y1, lx2, y1 + lh, col, fill)
        c.text_c((lx1 + lx2) // 2, y1 + lh // 2 - 4, name, BLACK, 1)
        c.arrow(spine_x, box_centers[i], lx1 - 2, box_centers[i], GRAY, 1, 6)

    # Divider
    c.line(390, 40, 390, 430, LIGHT_GRAY, 1)

    # Right half: GNN species-range workflow (vertical)
    c.text_c(590, 40, "GNN species-range workflow", PURPLE, 1)
    steps = [
        ("Occurrence + trait +", "satellite embeddings", DARK_BLUE, PALE_BLUE),
        ("Graph construction", "(species and sites as nodes)", MED_BLUE, LIGHT_BLUE),
        ("Message passing", "(share strength across taxa)", PURPLE, LIGHT_PURPLE),
        ("Range prediction", "+ uncertainty estimate", DARK_GREEN, LIGHT_GREEN),
        ("Explanation", "(driver attribution)", GOLD, LIGHT_GOLD),
    ]
    wx1, wx2 = 440, 740
    wy = 70
    wh = 52
    wgap = 20
    prev = None
    for i, (l1, l2, col, fill) in enumerate(steps):
        y1 = wy + i * (wh + wgap)
        c.rect(wx1, y1, wx2, y1 + wh, col, fill)
        c.text_c((wx1 + wx2) // 2, y1 + 14, l1, BLACK, 1)
        c.text_c((wx1 + wx2) // 2, y1 + 30, l2, GRAY, 1)
        if prev is not None:
            c.arrow((wx1 + wx2) // 2, prev, (wx1 + wx2) // 2, y1 - 2, PURPLE, 2, 8)
        prev = y1 + wh

    c.text(20, 452, "Figure 3: Method taxonomy (left) and a graph-neural-network range workflow (right)", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Methods_GNN_Workflow.png'))
    print("  Figure_3_Methods_GNN_Workflow.png done")


def gen_fig4():
    """Figure 4: Interacting-stressor cascade + forecast-to-decision pathway."""
    c = PNGCanvas(780, 470)
    c.text_c(390, 10, "From Interacting Stressors to Decisions", BLACK, 2)

    # Left: stressors converging to tipping point
    c.text_c(195, 40, "Interacting-stressor cascade", RED, 1)
    stressors = [
        ("Climate change", DARK_BLUE, PALE_BLUE),
        ("Habitat loss", DARK_GREEN, LIGHT_GREEN),
        ("Pollution", GOLD, LIGHT_GOLD),
        ("Over-exploitation", ORANGE, LIGHT_ORANGE),
        ("Invasive species", PURPLE, LIGHT_PURPLE),
    ]
    sx1, sx2 = 20, 180
    sy = 66
    sh = 40
    sgap = 14
    # convergence node
    conv_x, conv_y = 320, 180
    c.circle(conv_x, conv_y, 42, RED, LIGHT_RED)
    c.text_c(conv_x, conv_y - 14, "NON-", BLACK, 1)
    c.text_c(conv_x, conv_y, "LINEAR", BLACK, 1)
    c.text_c(conv_x, conv_y + 14, "SYNERGY", BLACK, 1)
    for i, (name, col, fill) in enumerate(stressors):
        y1 = sy + i * (sh + sgap)
        c.rect(sx1, y1, sx2, y1 + sh, col, fill)
        c.text_c((sx1 + sx2) // 2, y1 + sh // 2 - 4, name, BLACK, 1)
        c.arrow(sx2 + 2, y1 + sh // 2, conv_x - 44, conv_y + (y1 + sh // 2 - conv_y) // 4, GRAY, 2, 7)

    # tipping point below convergence
    c.arrow(conv_x, conv_y + 44, conv_x, 300, RED, 3, 11)
    c.rect(conv_x - 90, 305, conv_x + 90, 350, RED, LIGHT_RED)
    c.text_c(conv_x, 320, "ECOLOGICAL", BLACK, 1)
    c.text_c(conv_x, 335, "TIPPING POINT", BLACK, 1)

    # Divider
    c.line(400, 40, 400, 430, LIGHT_GRAY, 1)

    # Right: forecast -> decision pathway
    c.text_c(590, 40, "Forecast-to-decision pathway", DARK_GREEN, 1)
    path = [
        ("AI-driven biodiversity forecast", DARK_BLUE, PALE_BLUE),
        ("Risk and driver attribution", MED_BLUE, LIGHT_BLUE),
        ("Conservation planning", DARK_GREEN, LIGHT_GREEN),
        ("Regulation and policy", ORANGE, LIGHT_ORANGE),
        ("Economic and corporate decisions", PURPLE, LIGHT_PURPLE),
    ]
    px1, px2 = 430, 750
    py = 70
    ph = 50
    pgap = 20
    prev = None
    for i, (name, col, fill) in enumerate(path):
        y1 = py + i * (ph + pgap)
        c.rect(px1, y1, px2, y1 + ph, col, fill)
        c.text_c((px1 + px2) // 2, y1 + ph // 2 - 4, name, BLACK, 1)
        if prev is not None:
            c.arrow((px1 + px2) // 2, prev, (px1 + px2) // 2, y1 - 2, DARK_GREEN, 2, 8)
        prev = y1 + ph

    c.text(20, 452, "Figure 4: Interacting-stressor cascade (left) and the forecast-to-decision pathway (right)", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Stressor_Cascade_Decision.png'))
    print("  Figure_4_Stressor_Cascade_Decision.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating biodiversity chapter figures...")
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
