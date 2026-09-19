#!/usr/bin/env python3
"""
Generate the 4 figures (PNG) for Chapter 5
"Human-in-the-Loop and Explainable AI in Mission Control Systems".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 5.1 - Round-trip communication latency vs. obligatory onboard autonomy
  Figure 5.2 - Taxonomy of explainable AI (scope / timing / form)
  Figure 5.3 - Reference architecture for a HITL, explainable mission-control system
  Figure 5.4 - Transparency-cognitive-load trade-off and trust calibration
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/hitl_figures'


def gen_fig1():
    """Figure 5.1: round-trip latency for destinations vs. required autonomy."""
    c = PNGCanvas(780, 480)
    c.text_c(390, 12, "Communication Latency and the Shift to Onboard Autonomy", BLACK, 2)

    # Destinations: label, one-way description, round-trip seconds, bar color
    # RTLT computed from equation 5.1 (T_rt = 2d/c); values rounded for display.
    dests = [
        ("LEO", "~0.01 s", 0.01, MED_GREEN, "Ground-interactive"),
        ("GEO", "~0.24 s", 0.24, MED_GREEN, "Ground-interactive"),
        ("Moon", "~2.6 s", 2.6, MED_BLUE, "Human-on-the-loop"),
        ("Mars (near)", "~6 min", 360.0, ORANGE, "Conditionally auto."),
        ("Mars (far)", "~44 min", 2640.0, RED, "Obligatory autonomy"),
    ]

    # Plot area
    ax_x, ax_y0, ax_y1 = 90, 90, 330
    ax_x1 = 700
    c.vline(ax_x, ax_y0, ax_y1, BLACK)
    c.hline(ax_x, ax_x1, ax_y1, BLACK)
    c.text(20, ax_y0 - 4, "Round-trip", GRAY, 1)
    c.text(20, ax_y0 + 8, "light-time", GRAY, 1)
    c.text(20, ax_y0 + 20, "(log scale)", GRAY, 1)

    # Log scale gridlines: 0.01 s .. 10000 s
    labels = [("0.01 s", 0.01), ("1 s", 1.0), ("1 min", 60.0),
              ("1 hr", 3600.0)]
    lo, hi = math.log10(0.005), math.log10(3600.0)

    def y_of(v):
        t = (math.log10(v) - lo) / (hi - lo)
        return int(ax_y1 - t * (ax_y1 - ax_y0))

    for txt, v in labels:
        yy = y_of(v)
        c.hline(ax_x, ax_x1, yy, LIGHT_GRAY)
        c.text(ax_x - 55, yy - 3, txt, GRAY, 1)

    n = len(dests)
    slot = (ax_x1 - ax_x) // n
    bw = 58
    for i, (name, one_way, rt, col, level) in enumerate(dests):
        bx = ax_x + i * slot + (slot - bw) // 2
        top = y_of(rt)
        c.rect(bx, top, bx + bw, ax_y1 - 1, BLACK, col)
        c.text_c(bx + bw // 2, ax_y1 + 8, name, BLACK, 1)
        c.text_c(bx + bw // 2, top - 12, one_way, BLACK, 1)

    # Autonomy gradient band beneath the chart
    band_y0, band_y1 = 380, 415
    c.text(20, band_y0 - 16, "Required control mode as distance grows:", BLACK, 1)
    seg = (ax_x1 - ax_x) // n
    seg_cols = [LIGHT_GREEN, LIGHT_GREEN, LIGHT_BLUE, LIGHT_ORANGE, LIGHT_RED]
    for i, (name, one_way, rt, col, level) in enumerate(dests):
        sx = ax_x + i * seg
        c.rect(sx, band_y0, sx + seg, band_y1, GRAY, seg_cols[i])
        c.text_c(sx + seg // 2, band_y0 + 8, level, BLACK, 1)
    c.arrow(ax_x, band_y1 + 18, ax_x1, band_y1 + 18, DARK_GREEN, 3, 12)
    c.text_c(390, band_y1 + 26, "increasing distance and delay (equation 5.1)", DARK_GREEN, 1)

    c.text(20, 462, "Figure 5.1: Round-trip latency by destination and the corresponding shift toward obligatory onboard autonomy", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_5_1_Latency_Autonomy.png'))
    print("  Figure_5_1_Latency_Autonomy.png done")


def gen_fig2():
    """Figure 5.2: taxonomy of explainable AI by scope, timing, form."""
    c = PNGCanvas(780, 470)
    c.text_c(390, 12, "A Taxonomy of Explainable AI for Mission Control", BLACK, 2)

    # Root
    c.rect(300, 45, 480, 85, DARK_BLUE, PALE_BLUE)
    c.text_c(390, 58, "Explainable AI", BLACK, 1)
    c.text_c(390, 72, "(operator-facing)", GRAY, 1)

    # Three axis branches
    axes = [
        (120, "SCOPE", MED_BLUE, LIGHT_BLUE,
         ["Local: one decision", "Global: overall model"]),
        (390, "TIMING", MED_GREEN, LIGHT_GREEN,
         ["Ante-hoc: intrinsic", "Post-hoc: after training"]),
        (655, "FORM", PURPLE, LIGHT_PURPLE,
         ["Attribution", "Contrastive / counterfactual", "Example-based"]),
    ]
    for cx, title, col, fill, items in axes:
        c.arrow(390, 85, cx, 118, GRAY, 2, 8)
        c.rect(cx - 80, 120, cx + 80, 158, col, fill)
        c.text_c(cx, 134, title, BLACK, 1)
        for j, it in enumerate(items):
            c.text_c(cx, 172 + j * 15, it, BLACK, 1)

    # Technique boxes mapped under FORM/SCOPE with example applications
    c.text(40, 245, "Representative techniques (Table 5.2):", BLACK, 1)
    techs = [
        ("Local surrogate", "attribution / local", MED_BLUE, LIGHT_BLUE,
         "telemetry anomaly ranking"),
        ("Shapley attribution", "attribution / local-global", MED_BLUE, LIGHT_BLUE,
         "fault-diagnosis support"),
        ("Gradient saliency", "attribution / local", ORANGE, LIGHT_ORANGE,
         "vision hazard detection"),
        ("Counterfactual", "contrastive / local", PURPLE, LIGHT_PURPLE,
         "manoeuvre & abort planning"),
        ("Case-based reasoning", "example / ante-hoc", DARK_GREEN, LIGHT_GREEN,
         "procedure & precedent recall"),
        ("Interpretable rules", "global / ante-hoc", GOLD, LIGHT_GOLD,
         "certification & review"),
    ]
    bw, bh = 220, 52
    for i, (name, kind, col, fill, app) in enumerate(techs):
        row, cc = i // 3, i % 3
        bx = 40 + cc * 245
        by = 265 + row * 80
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        c.text_c(bx + bw // 2, by + 8, name, BLACK, 1)
        c.text_c(bx + bw // 2, by + 23, kind, GRAY, 1)
        c.text_c(bx + bw // 2, by + 38, app, BLACK, 1)

    c.text(20, 452, "Figure 5.2: Explanation approaches organised by scope, timing, and form, with techniques and applications", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_5_2_XAI_Taxonomy.png'))
    print("  Figure_5_2_XAI_Taxonomy.png done")


def gen_fig3():
    """Figure 5.3: HITL, explainable mission-control reference architecture."""
    c = PNGCanvas(800, 500)
    c.text_c(400, 12, "Reference Architecture: HITL, Explainable Mission Control", BLACK, 2)

    # Pipeline boxes left-to-right
    c.rect(30, 90, 190, 175, MED_BLUE, LIGHT_BLUE)
    c.text_c(110, 108, "PERCEPTION &", BLACK, 1)
    c.text_c(110, 122, "STATE ESTIMATION", BLACK, 1)
    c.text_c(110, 142, "telemetry, sensors,", GRAY, 1)
    c.text_c(110, 156, "knowledge base", GRAY, 1)

    c.rect(230, 90, 400, 175, DARK_GREEN, LIGHT_GREEN)
    c.text_c(315, 108, "REASONING &", BLACK, 1)
    c.text_c(315, 122, "DECISION CORE", BLACK, 1)
    c.text_c(315, 142, "planning + learned", GRAY, 1)
    c.text_c(315, 156, "components", GRAY, 1)

    c.rect(440, 90, 610, 175, PURPLE, LIGHT_PURPLE)
    c.text_c(525, 108, "EXPLANATION", BLACK, 1)
    c.text_c(525, 122, "GENERATOR", BLACK, 1)
    c.text_c(525, 142, "contrastive, attribution,", GRAY, 1)
    c.text_c(525, 156, "example-based", GRAY, 1)

    c.rect(650, 90, 780, 175, ORANGE, LIGHT_ORANGE)
    c.text_c(715, 108, "AUTHORITY", BLACK, 1)
    c.text_c(715, 122, "GATE", BLACK, 1)
    c.text_c(715, 142, "adjustable", GRAY, 1)
    c.text_c(715, 156, "autonomy level", GRAY, 1)

    c.arrow(190, 132, 228, 132, GRAY, 3, 9)
    c.arrow(400, 132, 438, 132, GRAY, 3, 9)
    c.arrow(610, 132, 648, 132, GRAY, 3, 9)

    # Actuation
    c.rect(650, 220, 780, 275, RED, LIGHT_RED)
    c.text_c(715, 238, "ACTUATION", BLACK, 1)
    c.text_c(715, 256, "commands to vehicle", GRAY, 1)
    c.arrow(715, 175, 715, 218, RED, 3, 9)
    c.text(725, 192, "act", RED, 1)

    # Human operator / crew
    c.rect(360, 300, 610, 385, DARK_BLUE, PALE_BLUE)
    c.text_c(485, 318, "HUMAN OPERATOR / CREW", BLACK, 1)
    c.text_c(485, 338, "approve  -  monitor  -  intervene", BLACK, 1)
    c.text_c(485, 358, "retains ultimate authority", GRAY, 1)
    # explanation to human
    c.arrow(525, 175, 525, 298, PURPLE, 3, 9)
    c.text(530, 250, "explanation", PURPLE, 1)
    # human approval / redirection to gate
    c.line(610, 342, 715, 342, DARK_BLUE, 2)
    c.arrow(715, 342, 715, 277, DARK_BLUE, 2, 8)
    c.text(618, 330, "approve / redirect", DARK_BLUE, 1)

    # Autonomy-level selector (maps to Table 5.1)
    c.rect(30, 300, 330, 400, GOLD, LIGHT_GOLD)
    c.text_c(180, 314, "AUTONOMY LEVEL (Table 5.1)", BLACK, 1)
    levels = ["Advisory", "Human-in-the-loop", "Human-on-the-loop",
              "Conditionally autonomous", "Fully autonomous"]
    for j, lv in enumerate(levels):
        c.text(45, 332 + j * 13, "- " + lv, BLACK, 1)
    c.arrow(180, 400, 640, 344, GRAY, 1, 7)

    # Feedback loop environment -> perception
    c.line(715, 275, 715, 430, GRAY, 1)
    c.line(715, 430, 110, 430, GRAY, 1)
    c.line(110, 430, 110, 177, GRAY, 1)
    c.arrow(110, 177, 110, 179, GRAY, 1, 6)
    c.text(360, 420, "environment feedback loop (new telemetry)", GRAY, 1)

    c.text(20, 482, "Figure 5.3: Flow from perception through reasoning to an explanation layer and an adjustable human-authority gate", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_5_3_Reference_Architecture.png'))
    print("  Figure_5_3_Reference_Architecture.png done")


def gen_fig4():
    """Figure 5.4: transparency-cognitive-load trade-off and trust calibration."""
    c = PNGCanvas(800, 430)
    c.text_c(400, 12, "Transparency-Load Trade-off and Trust Calibration", BLACK, 2)

    # ---- Left panel: net value vs explanation depth (inverted U) ----
    lx0, ly0, lx1, ly1 = 70, 60, 360, 340
    c.text(90, 44, "(a) Net decision value vs. depth", BLACK, 1)
    c.vline(lx0, ly0, ly1, BLACK)
    c.hline(lx0, lx1, ly1, BLACK)
    c.text(lx0 - 55, ly0 + 4, "value", GRAY, 1)
    c.text(lx0 - 55, ly0 + 18, "V (5.2)", GRAY, 1)
    c.text(lx1 - 70, ly1 + 14, "explanation depth", GRAY, 1)

    # Understanding curve U (saturating) - green
    prevx = prevy = None
    for px in range(lx0, lx1):
        t = (px - lx0) / (lx1 - lx0)
        u = 1 - math.exp(-3.2 * t)
        py = int(ly1 - u * (ly1 - ly0) * 0.9)
        if prevx is not None:
            c.line(prevx, prevy, px, py, LIGHT_GREEN, 2)
        prevx, prevy = px, py
    c.text(lx1 - 60, ly0 + 20, "U: understanding", MED_GREEN, 1)

    # Load curve L (accelerating) - red
    prevx = prevy = None
    for px in range(lx0, lx1):
        t = (px - lx0) / (lx1 - lx0)
        l = t * t
        py = int(ly1 - l * (ly1 - ly0) * 0.9)
        if prevx is not None:
            c.line(prevx, prevy, px, py, LIGHT_RED, 2)
        prevx, prevy = px, py
    c.text(lx1 - 55, ly1 - 60, "L: load", RED, 1)

    # Net value V = U - lambda L - blue, peaks at intermediate depth
    lam = 0.85
    best_x, best_y, best_v = lx0, ly1, -1
    prevx = prevy = None
    for px in range(lx0, lx1):
        t = (px - lx0) / (lx1 - lx0)
        u = 1 - math.exp(-3.2 * t)
        l = t * t
        v = u - lam * l
        py = int(ly1 - v * (ly1 - ly0) * 0.9)
        if v > best_v:
            best_v, best_x, best_y = v, px, py
        if prevx is not None:
            c.line(prevx, prevy, px, py, MED_BLUE, 3)
        prevx, prevy = px, py
    # optimum marker (equation 5.3)
    c.vline(best_x, best_y, ly1, GRAY)
    c.circle(best_x, best_y, 5, DARK_BLUE, MED_BLUE)
    c.text_c(best_x, best_y - 16, "optimum (5.3)", DARK_BLUE, 1)
    c.text(lx0 + 10, ly0 + 4, "V = U - lambda*L", MED_BLUE, 1)

    # ---- Right panel: trust calibration (reliance vs reliability) ----
    rx0, ry0, rx1, ry1 = 470, 60, 760, 340
    c.text(500, 44, "(b) Trust calibration (5.4)", BLACK, 1)
    c.vline(rx0, ry0, ry1, BLACK)
    c.hline(rx0, rx1, ry1, BLACK)
    c.text(rx0 - 60, (ry0 + ry1) // 2 - 6, "reliance r", GRAY, 1)
    c.text(rx1 - 70, ry1 + 14, "reliability rho", GRAY, 1)

    # Appropriate-reliance diagonal band (r = rho)
    for off in range(-14, 15):
        prevx = prevy = None
        for px in range(rx0, rx1):
            t = (px - rx0) / (rx1 - rx0)
            py = int(ry1 - t * (ry1 - ry0)) + off
            if ry0 <= py <= ry1 and prevx is not None:
                c.line(prevx, prevy, px, py, LIGHT_GREEN, 1)
            prevx, prevy = px, py
    # diagonal center line
    c.line(rx0, ry1, rx1, ry0, DARK_GREEN, 2)
    c.text_c((rx0 + rx1) // 2 + 40, (ry0 + ry1) // 2 - 24, "appropriate", DARK_GREEN, 1)
    c.text_c((rx0 + rx1) // 2 + 40, (ry0 + ry1) // 2 - 10, "reliance", DARK_GREEN, 1)

    # Over-trust region (above diagonal) and disuse (below)
    c.text(rx0 + 12, ry0 + 16, "over-trust", RED, 1)
    c.text(rx0 + 12, ry0 + 30, "(automation bias)", RED, 1)
    c.text(rx1 - 70, ry1 - 22, "disuse", PURPLE, 1)

    # Arrow showing explanation moves points toward the band
    c.circle(rx0 + 60, ry0 + 55, 4, RED, LIGHT_RED)
    c.arrow(rx0 + 66, ry0 + 58, rx0 + 120, ry0 + 100, GRAY, 2, 8)
    c.text(rx0 + 74, ry0 + 74, "explanation", GRAY, 1)

    c.text(20, 402, "Figure 5.4: (a) Net value peaks at intermediate explanation depth; (b) explanation drives reliance toward the", BLACK, 1)
    c.text(20, 416, "region of appropriate reliance where r tracks rho.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_5_4_Tradeoff_Calibration.png'))
    print("  Figure_5_4_Tradeoff_Calibration.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Chapter 5 (HITL & XAI) figures...")
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
