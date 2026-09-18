#!/usr/bin/env python3
"""
make_figures.py - Generate the four JPEG figures for Chapter 5,
"Human-in-the-Loop and Explainable AI in Mission Control Systems".

Figures (numbered per the book chapter):
  Figure 5.1  Autonomy spectrum vs. communication latency in mission control
  Figure 5.2  Reference architecture of a HITL-XAI mission control system
  Figure 5.3  Taxonomy of explanation types for mission-control XAI
  Figure 5.4  Explanation depth vs. operator performance / cognitive load
"""

import os
import math
from figlib import Canvas, save_jpeg, text_width

OUT = os.path.join(os.path.dirname(__file__), '..', 'hitl_figures')
os.makedirs(OUT, exist_ok=True)

# palette
NAVY = (25, 47, 89)
BLUE = (52, 120, 200)
LBLUE = (208, 224, 246)
TEAL = (33, 138, 140)
LTEAL = (206, 234, 234)
GREEN = (46, 158, 96)
LGREEN = (210, 236, 220)
AMBER = (224, 158, 52)
LAMBER = (250, 234, 200)
RED = (198, 74, 66)
LRED = (247, 218, 214)
GRAY = (112, 122, 138)
LGRAY = (233, 236, 242)
DARK = (28, 32, 42)
WHITE = (255, 255, 255)
BG = (248, 250, 253)


def footer(c, txt):
    # Caption is rendered by the document, not baked into the raster.
    return


# ─────────────────────────────────────────────────────────────────────────────
# Figure 5.1  Autonomy spectrum vs. communication latency
# ─────────────────────────────────────────────────────────────────────────────
def figure_1():
    W, H = 1040, 500
    c = Canvas(W, H, BG)
    c.text_center(W // 2, 26, 'Autonomy Spectrum and Communication Latency in', NAVY, 3)
    c.text_center(W // 2, 52, 'Space Mission Control', NAVY, 3)

    stages = [
        ('Manual /', 'Ground Control', 'Ground sends every', 'command; crew acts', LBLUE, BLUE),
        ('Human-in-', 'the-Loop', 'AI proposes; human', 'approves each step', LTEAL, TEAL),
        ('Human-on-', 'the-Loop', 'AI acts; human', 'watches, can veto', LGREEN, GREEN),
        ('Full', 'Autonomy', 'Onboard AI decides;', 'reviewed later', LAMBER, AMBER),
    ]
    n = len(stages)
    margin = 40
    gap = 18
    bw = (W - 2 * margin - (n - 1) * gap) // n
    top = 96
    bh = 150
    for i, (t1, t2, d1, d2, fill, border) in enumerate(stages):
        x0 = margin + i * (bw + gap)
        x1 = x0 + bw
        c.fill_round_rect(x0, top, x1, top + bh, fill, r=14)
        c.round_rect(x0, top, x1, top + bh, border, thickness=3, r=14)
        cx = (x0 + x1) // 2
        c.text_center(cx, top + 18, t1, DARK, 3)
        c.text_center(cx, top + 44, t2, DARK, 3)
        c.line(x0 + 18, top + 76, x1 - 18, top + 76, border, 2)
        c.text_center(cx, top + 90, d1, DARK, 2)
        c.text_center(cx, top + 110, d2, DARK, 2)
        if i < n - 1:
            ax = x1 + 2
            c.arrow(ax, top + bh // 2, ax + gap - 4, top + bh // 2, GRAY, 3, head=8)

    # authority / autonomy gradient bars
    by = top + bh + 40
    c.text(margin, by, 'Human authority / real-time oversight', NAVY, 2)
    c.arrow(margin + 360, by + 8, W - margin, by + 8, RED, 3, head=10)
    c.text(W - margin - 92, by + 18, 'decreasing', RED, 2)

    by2 = by + 44
    c.text(margin, by2, 'Onboard autonomy required', NAVY, 2)
    c.arrow(margin + 270, by2 + 8, W - margin, by2 + 8, GREEN, 3, head=10)
    c.text(W - margin - 92, by2 + 18, 'increasing', GREEN, 2)

    # latency axis
    ay = by2 + 78
    c.line(margin, ay, W - margin, ay, DARK, 3)
    ticks = [
        (margin + 20, 'LEO', '~0.01 s'),
        (margin + 250, 'GEO', '~0.24 s'),
        (margin + 470, 'Cislunar / Moon', '~1.3 s'),
        (margin + 720, 'Mars', '4 - 24 min'),
        (W - margin - 70, 'Deep space', '> 30 min'),
    ]
    for x, lab, lat in ticks:
        c.line(x, ay - 7, x, ay + 7, DARK, 2)
        c.text_center(x, ay + 14, lab, DARK, 2)
        c.text_center(x, ay + 34, lat, GRAY, 2)
    c.text_center(W // 2, ay - 30, 'One-way light-time delay (distance from Earth)', NAVY, 2)

    footer(c, 'Figure 5.1  As light-time delay grows, the viable operating point shifts from ground control toward onboard autonomy.')
    p = os.path.join(OUT, 'Figure_5_1_Autonomy_Spectrum.jpg')
    print('F5.1', save_jpeg(c, p, 90), p)


# ─────────────────────────────────────────────────────────────────────────────
# Figure 5.2  Reference architecture of a HITL-XAI mission control system
# ─────────────────────────────────────────────────────────────────────────────
def figure_2():
    W, H = 1040, 760
    c = Canvas(W, H, BG)
    c.text_center(W // 2, 24, 'Reference Architecture of a Human-in-the-Loop,', NAVY, 3)
    c.text_center(W // 2, 50, 'Explainable-AI Mission Control System', NAVY, 3)

    left = 60
    right = 686
    lay_x1 = right
    layers = [
        ('L5  Human Decision & Authority',
         ['Approve  -  Override  -  Delegate  -  Abort', 'Crew and controllers keep final authority'],
         LRED, RED),
        ('L4  Operator / Crew Interface',
         ['Dashboards, alerts, natural-language queries', 'Adjustable explanation depth and confidence'],
         LAMBER, AMBER),
        ('L3  Explanation Generation (XAI)',
         ['Contrastive  -  Global  -  Local  -  Example-based', 'Confidence, provenance and uncertainty reporting'],
         LGREEN, GREEN),
        ('L2  AI Reasoning Core',
         ['Hierarchical task planning  |  Truth maintenance', 'Case-based reasoning  |  Anomaly diagnosis'],
         LTEAL, TEAL),
        ('L1  Telemetry & Sensor Data Layer',
         ['Spacecraft subsystems, GN&C, life support', 'Space-domain awareness and conjunction data'],
         LBLUE, BLUE),
    ]
    top = 88
    lh = 108
    vgap = 14
    for i, (title, lines, fill, border) in enumerate(layers):
        y0 = top + i * (lh + vgap)
        y1 = y0 + lh
        c.fill_round_rect(left, y0, lay_x1, y1, fill, r=12)
        c.round_rect(left, y0, lay_x1, y1, border, thickness=3, r=12)
        c.text(left + 20, y0 + 14, title, DARK, 3)
        c.line(left + 20, y0 + 44, lay_x1 - 20, y0 + 44, border, 2)
        yy = y0 + 54
        for ln in lines:
            c.text(left + 20, yy, ln, DARK, 2)
            yy += 22

    # vertical flow arrows between layers (data up, commands down)
    midx_up = left - 26
    midx_dn = lay_x1 + 26
    c.text_center(midx_up, top - 20, 'data', NAVY, 2)
    c.text_center(midx_dn, top - 20, 'cmd', NAVY, 2)
    for i in range(len(layers) - 1):
        y_lower = top + (i + 1) * (lh + vgap) - vgap
        y_upper = top + i * (lh + vgap) + lh
        # up arrow (telemetry/explanations rising) on left
        c.arrow(midx_up, y_lower + 6, midx_up, y_upper - 6, BLUE, 3, head=8)
    for i in range(len(layers) - 1):
        y_lower = top + (i + 1) * (lh + vgap) - vgap
        y_upper = top + i * (lh + vgap) + lh
        # down arrow (authority/commands) on right
        c.arrow(midx_dn, y_upper - 6, midx_dn, y_lower + 6, RED, 3, head=8)

    # side annotations panel
    sx0 = right + 40
    sx1 = W - 20
    c.fill_round_rect(sx0, top, sx1, top + 2 * (lh + vgap) + lh - vgap, (238, 242, 248), r=12)
    c.round_rect(sx0, top, sx1, top + 2 * (lh + vgap) + lh - vgap, GRAY, thickness=2, r=12)
    c.text(sx0 + 16, top + 14, 'Trust calibration', NAVY, 2)
    c.line(sx0 + 16, top + 34, sx1 - 16, top + 34, GRAY, 1)
    c.text_box(sx0 + 16, top + 46, sx1 - 16,
               'Explanations rise so operators calibrate trust; authority flows down so humans stay in command.',
               DARK, 2, line_gap=5)

    sy0 = top + 3 * (lh + vgap)
    c.fill_round_rect(sx0, sy0, sx1, top + 5 * (lh + vgap) - vgap, (238, 242, 248), r=12)
    c.round_rect(sx0, sy0, sx1, top + 5 * (lh + vgap) - vgap, GRAY, thickness=2, r=12)
    c.text(sx0 + 16, sy0 + 14, 'Disconnected mode', NAVY, 2)
    c.line(sx0 + 16, sy0 + 34, sx1 - 16, sy0 + 34, GRAY, 1)
    c.text_box(sx0 + 16, sy0 + 46, sx1 - 16,
               'An onboard retrieval-augmented model sustains a virtual flight controller when the link to Earth drops.',
               DARK, 2, line_gap=5)

    footer(c, 'Figure 5.2  Layered design keeps ultimate authority with humans while automated reasoning and explanation support decisions.')
    p = os.path.join(OUT, 'Figure_5_2_Reference_Architecture.jpg')
    print('F5.2', save_jpeg(c, p, 90), p)


# ─────────────────────────────────────────────────────────────────────────────
# Figure 5.3  Taxonomy of explanation types
# ─────────────────────────────────────────────────────────────────────────────
def figure_3():
    W, H = 1060, 660
    c = Canvas(W, H, BG)
    c.text_center(W // 2, 26, 'Taxonomy of Explanation Types for Mission-Control XAI', NAVY, 3)

    # root
    rx0, ry0, rx1, ry1 = W // 2 - 180, 70, W // 2 + 180, 128
    c.fill_round_rect(rx0, ry0, rx1, ry1, NAVY, r=12)
    c.round_rect(rx0, ry0, rx1, ry1, DARK, thickness=2, r=12)
    c.text_center(W // 2, ry0 + 12, 'Explainable AI', WHITE, 3)
    c.text_center(W // 2, ry0 + 34, 'for Mission Control', WHITE, 2)

    # three branch categories
    cats = [
        ('By Scope', ['Global', 'Local'],
         ['Model-wide behaviour', 'Single decision'], BLUE, LBLUE),
        ('By Form', ['Contrastive', 'Feature-attribution', 'Example / case-based', 'Rule-based'],
         ['"Why A not B?"', 'Which inputs mattered', 'Similar past cases', 'If-then logic'], TEAL, LTEAL),
        ('By Timing', ['Ante-hoc (intrinsic)', 'Post-hoc'],
         ['Transparent model', 'Explains a black box'], GREEN, LGREEN),
    ]
    n = len(cats)
    margin = 40
    gap = 30
    cw = (W - 2 * margin - (n - 1) * gap) // n
    cat_top = 176
    cat_h = 52
    for i, (name, leaves, notes, border, fill) in enumerate(cats):
        x0 = margin + i * (cw + gap)
        x1 = x0 + cw
        cx = (x0 + x1) // 2
        # connector from root
        c.arrow(W // 2, ry1 + 2, cx, cat_top - 4, GRAY, 2, head=7)
        c.fill_round_rect(x0, cat_top, x1, cat_top + cat_h, border, r=10)
        c.round_rect(x0, cat_top, x1, cat_top + cat_h, DARK, thickness=2, r=10)
        c.text_center(cx, cat_top + 16, name, WHITE, 3)
        # leaves
        ly = cat_top + cat_h + 26
        lh = 74
        for leaf, note in zip(leaves, notes):
            ly1 = ly + lh - 16
            c.fill_round_rect(x0, ly, x1, ly1, fill, r=8)
            c.round_rect(x0, ly, x1, ly1, border, thickness=2, r=8)
            c.arrow(cx, (ly - (lh - 16)) if False else ly - 10, cx, ly - 2, GRAY, 2, head=6)
            c.text_center(cx, ly + 8, leaf, DARK, 2)
            c.text_center(cx, ly + 28, note, GRAY, 2)
            ly += lh

    # highlight most-effective combination
    note_y = H - 74
    c.fill_round_rect(margin, note_y, W - margin, note_y + 46, LAMBER, r=10)
    c.round_rect(margin, note_y, W - margin, note_y + 46, AMBER, thickness=2, r=10)
    c.text_center((margin + W - margin) // 2, note_y + 14,
                  'Most effective reported pairing: contrastive + global explanations.',
                  DARK, 2)

    footer(c, 'Figure 5.3  Explanation methods differ by scope, form and timing; combinations are chosen to match operator needs.')
    p = os.path.join(OUT, 'Figure_5_3_Explanation_Taxonomy.jpg')
    print('F5.3', save_jpeg(c, p, 90), p)


# ─────────────────────────────────────────────────────────────────────────────
# Figure 5.4  Explanation depth vs. performance / cognitive load
# ─────────────────────────────────────────────────────────────────────────────
def figure_4():
    W, H = 1040, 660
    c = Canvas(W, H, BG)
    c.text_center(W // 2, 24, 'Explanation Depth versus Operator Performance', NAVY, 3)
    c.text_center(W // 2, 50, 'and Cognitive Load', NAVY, 3)

    # plot area
    px0, py0 = 110, 96
    px1, py1 = W - 240, H - 120
    c.fill_rect(px0, py0, px1, py1, WHITE)
    c.rect(px0, py0, px1, py1, DARK, 2)

    # gridlines
    for k in range(1, 5):
        gx = px0 + (px1 - px0) * k // 5
        c.vline(py0, py1, gx, LGRAY)
        gy = py0 + (py1 - py0) * k // 5
        c.hline(px0, px1, gy, LGRAY)

    # axes labels
    c.text_center((px0 + px1) // 2, py1 + 40, 'Explanation depth / detail', NAVY, 2)
    c.text_center((px0 + px1) // 2, py1 + 62, '(none  ->  minimal  ->  advanced justification)', GRAY, 2)
    # y axis label (vertical, drawn as stacked chars)
    ylab = 'Performance / trust'
    yy = py0 + 10
    for ch in ylab:
        c.text(20, yy, ch, NAVY, 2)
        yy += 16

    def X(t):  # t in 0..1
        return int(px0 + (px1 - px0) * t)

    def Y(v):  # v in 0..1 (0 bottom, 1 top)
        return int(py1 - (py1 - py0) * v)

    # High-uncertainty curve: rises strongly with depth then plateaus
    hi = [(0.0, 0.18), (0.2, 0.42), (0.4, 0.66), (0.6, 0.82), (0.8, 0.88), (1.0, 0.86)]
    # Low-uncertainty curve: modest benefit, earlier plateau, slight late dip (overload)
    lo = [(0.0, 0.40), (0.2, 0.55), (0.4, 0.66), (0.6, 0.70), (0.8, 0.66), (1.0, 0.58)]

    def plot(points, color):
        for i in range(len(points) - 1):
            x0, v0 = points[i]
            x1, v1 = points[i + 1]
            c.line(X(x0), Y(v0), X(x1), Y(v1), color, 4)
        for x, v in points:
            c.fill_round_rect(X(x) - 4, Y(v) - 4, X(x) + 4, Y(v) + 4, color, r=2)

    plot(hi, RED)
    plot(lo, BLUE)

    # cognitive-load / overload region shading (right portion)
    ovx0 = X(0.72)
    for x in range(ovx0, px1, 6):
        c.vline(py0 + 2, py1 - 2, x, (245, 226, 222))
    c.rect(ovx0, py0, px1, py1, (230, 170, 160), 1)
    c.text_center((ovx0 + px1) // 2, py0 + 10, 'information', RED, 2)
    c.text_center((ovx0 + px1) // 2, py0 + 28, 'overload', RED, 2)

    # sweet-spot marker
    ssx = X(0.62)
    c.line(ssx, py0, ssx, py1, GREEN, 2)
    c.text_center(ssx, py1 - 20, 'useful depth', GREEN, 2)

    # legend
    lx0 = px1 + 30
    ly0 = py0 + 10
    c.fill_round_rect(lx0, ly0, W - 24, ly0 + 150, (240, 243, 248), r=10)
    c.round_rect(lx0, ly0, W - 24, ly0 + 150, GRAY, thickness=2, r=10)
    c.text(lx0 + 14, ly0 + 12, 'Legend', NAVY, 3)
    c.line(lx0 + 14, ly0 + 48, lx0 + 54, ly0 + 48, RED, 3)
    c.text(lx0 + 62, ly0 + 42, 'High', DARK, 2)
    c.text(lx0 + 62, ly0 + 60, 'uncertainty', DARK, 2)
    c.line(lx0 + 14, ly0 + 96, lx0 + 54, ly0 + 96, BLUE, 3)
    c.text(lx0 + 62, ly0 + 90, 'Low', DARK, 2)
    c.text(lx0 + 62, ly0 + 108, 'uncertainty', DARK, 2)

    footer(c, 'Figure 5.4  Deeper explanations help most under high uncertainty; beyond a useful depth, added detail raises workload.')
    p = os.path.join(OUT, 'Figure_5_4_Depth_vs_Performance.jpg')
    print('F5.4', save_jpeg(c, p, 90), p)


if __name__ == '__main__':
    figure_1()
    figure_2()
    figure_3()
    figure_4()
    print('done ->', os.path.abspath(OUT))
