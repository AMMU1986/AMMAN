#!/usr/bin/env python3
"""
Generate 4 high-resolution figure images (PNG) for the chapter
"Artificial Intelligence, Cognitive Offloading and Brain Fog:
 Navigating Digital Overload in the AI-Driven World".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py
so it runs without any third-party dependencies in the sandbox. Rendered at
large canvas sizes with up-scaled bitmap text and thicker strokes to yield
crisp, print-ready (high-resolution) PNGs.

Figures:
  Figure 1 - Conceptual framework: AI/digital overload -> cognitive
             offloading -> reduced engagement -> brain fog (with feedback loop)
  Figure 2 - Taxonomy of cognitive offloading in AI-driven environments
  Figure 3 - The reinforcing (vicious) cycle of AI reliance and brain fog
  Figure 4 - Multi-level countermeasures framework
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/brainfog_figures'


def box_text(c, x1, y1, x2, y2, outline, fill, lines, scale=2,
             title_scale=None, line_h=None, top_pad=14):
    """Draw a rounded-ish rectangle with a stack of centered text lines.

    lines: list of (text, color) or plain strings (defaults to BLACK).
    The first line is drawn with title_scale if provided.
    """
    c.rect(x1, y1, x2, y2, outline, fill)
    # thicken the outline by drawing a second inset rectangle
    c.rect(x1 + 1, y1 + 1, x2 - 1, y2 - 1, outline)
    cx = (x1 + x2) // 2
    if line_h is None:
        line_h = 14 * scale
    y = y1 + top_pad
    for i, item in enumerate(lines):
        if isinstance(item, tuple):
            txt, col = item
        else:
            txt, col = item, BLACK
        s = scale
        if i == 0 and title_scale:
            s = title_scale
        c.text_c(cx, y, txt, col, s)
        y += (16 * title_scale) if (i == 0 and title_scale) else line_h


def gen_fig1():
    """Figure 1: Conceptual framework from digital overload to brain fog."""
    W, H = 1600, 1000
    c = PNGCanvas(W, H)
    c.text_c(W // 2, 26, "From AI-Driven Digital Overload to Brain Fog:", BLACK, 3)
    c.text_c(W // 2, 70, "A Conceptual Framework", BLACK, 3)

    bw, bh = 330, 230
    top = 150
    gap = (W - 60 - 4 * bw) // 3
    xs = []
    stages = [
        (DARK_BLUE, PALE_BLUE, [
            ("AI TOOLS &", DARK_BLUE),
            ("DIGITAL OVERLOAD", DARK_BLUE),
            ("", BLACK),
            ("Search engines", GRAY),
            ("Generative chatbots", GRAY),
            ("Recommender feeds", GRAY),
            ("Constant notifications", GRAY),
        ]),
        (PURPLE, LIGHT_PURPLE, [
            ("COGNITIVE", PURPLE),
            ("OFFLOADING", PURPLE),
            ("", BLACK),
            ("Delegating memory,", GRAY),
            ("computation, navigation", GRAY),
            ("and decisions to", GRAY),
            ("external AI systems", GRAY),
        ]),
        (ORANGE, LIGHT_ORANGE, [
            ("REDUCED COGNITIVE", ORANGE),
            ("ENGAGEMENT", ORANGE),
            ("", BLACK),
            ("Less effortful encoding,", GRAY),
            ("weaker metacognition,", GRAY),
            ("shallower attention,", GRAY),
            ("skill under-use", GRAY),
        ]),
        (RED, LIGHT_RED, [
            ("BRAIN FOG", RED),
            ("", BLACK),
            ("", BLACK),
            ("Inattention,", GRAY),
            ("memory lapses,", GRAY),
            ("mental fatigue,", GRAY),
            ("slowed thinking", GRAY),
        ]),
    ]
    for i, (col, fill, lines) in enumerate(stages):
        bx = 30 + i * (bw + gap)
        xs.append((bx, bx + bw))
        box_text(c, bx, top, bx + bw, top + bh, col, fill, lines,
                 scale=2, title_scale=2, line_h=26, top_pad=22)
        if i > 0:
            px = xs[i - 1][1]
            c.arrow(px + 6, top + bh // 2, bx - 6, top + bh // 2, DARK_GREEN, 5, 22)

    # Moderators box (top band)
    c.rect(30, top + bh + 60, W - 30, top + bh + 150, GRAY, (245, 245, 245))
    c.text_c(W // 2, top + bh + 74, "MODERATING FACTORS", MED_BLUE, 2)
    c.text_c(W // 2, top + bh + 104,
             "Task type   -   Trust in AI   -   Individual differences   -   Frequency & duration of use   -   Metacognitive skill",
             GRAY, 2)

    # Feedback loop from Brain Fog back to Cognitive Offloading
    loop_y = top + bh + 230
    bx_fog = xs[3][0] + bw // 2
    bx_off = xs[1][0] + bw // 2
    c.line(bx_fog, top + bh, bx_fog, loop_y, RED, 4)
    c.line(bx_fog, loop_y, bx_off, loop_y, RED, 4)
    c.arrow(bx_off, loop_y, bx_off, top + bh + 4, RED, 4, 20)
    c.text_c((bx_fog + bx_off) // 2, loop_y - 34,
             "Reinforcing loop: fog -> greater reliance on AI -> further offloading", RED, 2)

    c.text(30, H - 40,
           "Figure 1: Conceptual framework from AI-driven digital overload to brain fog.",
           BLACK, 2)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Conceptual_Framework.png'))
    print("  Figure_1_Conceptual_Framework.png done")


def gen_fig2():
    """Figure 2: Taxonomy of cognitive offloading in AI environments."""
    W, H = 1600, 1050
    c = PNGCanvas(W, H)
    c.text_c(W // 2, 26, "A Taxonomy of Cognitive Offloading in AI-Driven Environments", BLACK, 3)

    # Root
    rx1, ry1, rx2, ry2 = W // 2 - 300, 90, W // 2 + 300, 180
    box_text(c, rx1, ry1, rx2, ry2, DARK_GREEN, LIGHT_GREEN,
             [("COGNITIVE OFFLOADING", DARK_GREEN),
              ("Delegating cognition to external AI", GRAY)],
             scale=2, title_scale=2, line_h=30, top_pad=22)

    cats = [
        (DARK_BLUE, PALE_BLUE, "MEMORY", [
            "Storing & recalling",
            "facts via AI",
            "Notes, search,",
            "retrieval chatbots"]),
        (MED_BLUE, LIGHT_BLUE, "COMPUTATIONAL", [
            "Calculation &",
            "data processing",
            "Solvers, code",
            "assistants, analytics"]),
        (PURPLE, LIGHT_PURPLE, "NAVIGATIONAL", [
            "Spatial & procedural",
            "wayfinding",
            "GPS, step-by-step",
            "AI guidance"]),
        (ORANGE, LIGHT_ORANGE, "DECISION", [
            "Judgement &",
            "choice",
            "Recommenders,",
            "advisory agents"]),
        (RED, LIGHT_RED, "CREATIVE /", [
            "GENERATIVE",
            "Ideation & writing",
            "LLM drafting,",
            "image generation"]),
    ]
    n = len(cats)
    bw, bh = 270, 240
    total = n * bw + (n - 1) * 30
    startx = (W - total) // 2
    cy_top = 320
    root_cx = (rx1 + rx2) // 2
    for i, (col, fill, title, bullets) in enumerate(cats):
        bx = startx + i * (bw + 30)
        lines = [(title, col), ("", BLACK)] + [(b, GRAY) for b in bullets]
        box_text(c, bx, cy_top, bx + bw, cy_top + bh, col, fill, lines,
                 scale=2, title_scale=2, line_h=26, top_pad=18)
        # connector from root to each category
        c.line(root_cx, ry2, bx + bw // 2, cy_top - 1, GRAY, 3)
        c.arrow(bx + bw // 2, cy_top - 20, bx + bw // 2, cy_top - 2, GRAY, 3, 12)

    # Dimension band: degree of offloading
    band_y = cy_top + bh + 70
    c.text_c(W // 2, band_y, "Cross-cutting dimension: depth of offloading", MED_BLUE, 2)
    c.arrow(120, band_y + 50, W - 120, band_y + 50, DARK_GREEN, 5, 22)
    c.text(140, band_y + 60, "Supplementary (augments own cognition)", DARK_GREEN, 2)
    c.text(W - 560, band_y + 60, "Substitutive (replaces own cognition)", RED, 2)

    # Consequence note
    ny = band_y + 150
    c.rect(120, ny, W - 120, ny + 110, GOLD, LIGHT_GOLD)
    c.text_c(W // 2, ny + 20,
             "Substitutive offloading, when habitual and unmonitored, is most strongly linked to", BLACK, 2)
    c.text_c(W // 2, ny + 54,
             "disengagement, skill decay and self-reported brain fog", BLACK, 2)

    c.text(30, H - 40,
           "Figure 2: Taxonomy of cognitive offloading across five functional domains.",
           BLACK, 2)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Taxonomy.png'))
    print("  Figure_2_Taxonomy.png done")


def gen_fig3():
    """Figure 3: Reinforcing (vicious) cycle of AI reliance and brain fog."""
    import math
    W, H = 1400, 1150
    c = PNGCanvas(W, H)
    c.text_c(W // 2, 26, "The Reinforcing Cycle of AI Reliance and Brain Fog", BLACK, 3)

    cx, cy = W // 2, H // 2 + 40
    R = 390
    nodes = [
        (DARK_BLUE, PALE_BLUE, ["Habitual use of", "AI & digital tools"]),
        (PURPLE, LIGHT_PURPLE, ["Cognitive offloading;", "effortful thinking", "is bypassed"]),
        (ORANGE, LIGHT_ORANGE, ["Weaker encoding,", "attention & memory", "consolidation"]),
        (RED, LIGHT_RED, ["Brain fog:", "fatigue, inattention,", "forgetfulness"]),
        (MED_GREEN, LIGHT_GREEN, ["Reduced confidence", "in own cognition;", "more help-seeking"]),
    ]
    n = len(nodes)
    bw, bh = 300, 150
    centers = []
    for i in range(n):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        nx = int(cx + R * math.cos(ang))
        ny = int(cy + R * math.sin(ang))
        centers.append((nx, ny, ang))

    # draw arrows between consecutive nodes (clockwise) first (under boxes)
    for i in range(n):
        x1, y1, a1 = centers[i]
        x2, y2, a2 = centers[(i + 1) % n]
        # points on circle between boxes
        sx = int(cx + (R - 10) * math.cos(a1 + 0.55))
        sy = int(cy + (R - 10) * math.sin(a1 + 0.55))
        ex = int(cx + (R - 10) * math.cos(a2 - 0.55))
        ey = int(cy + (R - 10) * math.sin(a2 - 0.55))
        c.arrow(sx, sy, ex, ey, GRAY, 5, 22)

    for i, (col, fill, lines) in enumerate(nodes):
        nx, ny, _ = centers[i]
        x1, y1 = nx - bw // 2, ny - bh // 2
        x2, y2 = nx + bw // 2, ny + bh // 2
        box_text(c, x1, y1, x2, y2, col, fill,
                 [(lines[0], col)] + [(l, BLACK) for l in lines[1:]],
                 scale=2, title_scale=2, line_h=28, top_pad=24)

    # center label
    c.rect(cx - 220, cy - 60, cx + 220, cy + 60, RED, (255, 240, 240))
    c.text_c(cx, cy - 34, "SELF-REINFORCING", RED, 3)
    c.text_c(cx, cy + 6, "FEEDBACK LOOP", RED, 3)

    c.text(30, H - 40,
           "Figure 3: Self-reinforcing cycle of AI reliance, cognitive offloading and brain fog.",
           BLACK, 2)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Reinforcing_Cycle.png'))
    print("  Figure_3_Reinforcing_Cycle.png done")


def gen_fig4():
    """Figure 4: Multi-level countermeasures framework."""
    W, H = 1600, 1050
    c = PNGCanvas(W, H)
    c.text_c(W // 2, 26, "A Multi-Level Framework of Countermeasures", BLACK, 3)

    layers = [
        (PURPLE, LIGHT_PURPLE, "POLICY & GOVERNANCE",
         "Digital-wellbeing standards, transparency, duty-of-care, research funding"),
        (DARK_BLUE, PALE_BLUE, "TECHNOLOGICAL / DESIGN",
         "Friction by design, effort-preserving defaults, explainability, usage dashboards"),
        (MED_GREEN, LIGHT_GREEN, "ORGANISATIONAL",
         "Focus-time norms, notification hygiene, workload & meeting redesign"),
        (ORANGE, LIGHT_ORANGE, "EDUCATIONAL / METACOGNITIVE",
         "AI literacy, desirable difficulties, retrieval practice, critical-thinking training"),
        (RED, LIGHT_RED, "INDIVIDUAL",
         "Selective offloading, attention management, breaks, sleep, cognitive hygiene"),
    ]
    # Pyramid-style stacked trapezoids (wider at bottom = foundational individual)
    n = len(layers)
    lh = 150
    gap = 14
    top = 110
    base_w = 1300
    min_w = 560
    for i, (col, fill, title, sub) in enumerate(layers):
        # bottom layer widest
        frac_top = i / n
        frac_bot = (i + 1) / n
        w_top = int(min_w + (base_w - min_w) * frac_top)
        w_bot = int(min_w + (base_w - min_w) * frac_bot)
        y1 = top + i * (lh + gap)
        y2 = y1 + lh
        w = max(w_top, w_bot)
        x1 = (W - w) // 2
        x2 = x1 + w
        box_text(c, x1, y1, x2, y2, col, fill,
                 [(title, col), (sub, GRAY)],
                 scale=2, title_scale=2, line_h=34, top_pad=40)

    # side arrow indicating scope / leverage
    c.arrow(90, top + n * (lh + gap) - 20, 90, top + 10, DARK_GREEN, 5, 22)
    c.text(30, top + 10, "Broader", DARK_GREEN, 2)
    c.text(20, top + 40, "scope", DARK_GREEN, 2)
    c.text(30, top + n * (lh + gap) - 60, "Personal", DARK_GREEN, 2)
    c.text(30, top + n * (lh + gap) - 30, "control", DARK_GREEN, 2)

    c.text(30, H - 40,
           "Figure 4: Multi-level countermeasures framework.",
           BLACK, 2)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Countermeasures.png'))
    print("  Figure_4_Countermeasures.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating brain fog chapter figures...")
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
