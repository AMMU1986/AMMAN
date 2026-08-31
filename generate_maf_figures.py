#!/usr/bin/env python3
"""
Generate 20 scientific figure images (PNG) for the chapter
"Machine Learning-Based Prediction of Surface Roughness in Magnetic Abrasive Finishing".

Reuses the pure-stdlib PNGCanvas class from generate_figures.py (no external deps).
Outputs to MAF_ML_figures/ as Figure_1.png .. Figure_20.png.
"""

import os
import math
import random

# Reuse the PNGCanvas + colors + font from the existing generator.
from generate_figures import (
    PNGCanvas,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE, RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/MAF_ML_figures'

W, H = 760, 480


def axes(c, x0, y0, x1, y1, color=BLACK):
    """Draw simple x (bottom) and y (left) axes given plot corners."""
    c.vline(x0, y0, y1, color)
    c.hline(x0, x1, y1, color)


def title(c, s):
    c.text_c(W // 2, 10, s, BLACK, 2)


def caption(c, s):
    c.text(40, H - 22, s, BLACK, 1)


def new_canvas():
    return PNGCanvas(W, H)


def curve(c, x0, x1, fn, color, ytop, ybot, thick=2):
    """Plot fn(t in 0..1) -> 0..1 mapped into [ybot..ytop] over x0..x1."""
    px = px_prev = None
    py_prev = None
    for x in range(x0, x1):
        t = (x - x0) / float(x1 - x0)
        v = max(0.0, min(1.0, fn(t)))
        y = int(ybot - v * (ybot - ytop))
        if px_prev is not None:
            c.line(px_prev, py_prev, x, y, color, thick)
        px_prev, py_prev = x, y


# ---------------------------------------------------------------------------
# Figure 1: Schematic of a typical MAF system
# ---------------------------------------------------------------------------
def fig1():
    c = new_canvas()
    title(c, "Typical Magnetic Abrasive Finishing System")

    # N pole (top), workpiece band, S pole (bottom)
    c.rect(230, 70, 520, 120, DARK_BLUE, LIGHT_BLUE)
    c.text_c(375, 88, "Magnetic Pole (N)", BLACK, 1)
    c.rect(230, 300, 520, 350, DARK_BLUE, LIGHT_BLUE)
    c.text_c(375, 318, "Magnetic Pole (S)", BLACK, 1)

    # Working gap with brush chains
    c.text(535, 175, "Working", BLACK, 1)
    c.text(535, 190, "gap (G)", BLACK, 1)
    for i in range(9):
        x = 250 + i * 30
        # chain of particles between poles
        for j in range(5):
            y = 135 + j * 30
            c.circle(x, y, 5, DARK_GREEN, MED_GREEN)
        c.line(x, 125, x, 285, GRAY, 1)

    # Workpiece (rotating cylinder) in middle
    c.rect(250, 195, 500, 225, BLACK, LIGHT_ORANGE)
    c.text_c(375, 205, "Workpiece", BLACK, 1)
    c.arrow(505, 210, 545, 210, ORANGE, 2, 7)
    c.text(548, 205, "rotation", ORANGE, 1)

    # Electromagnet coil / source
    c.rect(60, 120, 200, 300, GRAY, PALE_BLUE)
    c.text_c(130, 135, "Field Source", BLACK, 1)
    c.text_c(130, 155, "(electromagnet /", BLACK, 1)
    c.text_c(130, 170, "permanent magnet)", BLACK, 1)
    c.arrow(200, 95, 230, 95, GRAY, 2, 7)
    c.arrow(200, 325, 230, 325, GRAY, 2, 7)

    # Control system
    c.rect(590, 120, 720, 300, DARK_GREEN, LIGHT_GREEN)
    c.text_c(655, 135, "Control", BLACK, 1)
    c.text_c(655, 152, "System", BLACK, 1)
    c.text(600, 175, "- current/field", BLACK, 1)
    c.text(600, 195, "- speed", BLACK, 1)
    c.text(600, 215, "- feed/time", BLACK, 1)
    c.text(600, 235, "- sensing", BLACK, 1)

    # Inset: single chain engaging asperity
    c.rect(250, 375, 520, 445, LIGHT_GRAY, (250, 250, 250))
    c.text(258, 380, "Inset: chain engaging a surface asperity", BLACK, 1)
    for j in range(4):
        c.circle(300 + j * 18, 405, 6, DARK_GREEN, MED_GREEN)
    # asperity profile
    xs = list(range(390, 500))
    for k in range(len(xs) - 1):
        x = xs[k]
        y = int(425 - 8 * abs(math.sin((x - 390) * 0.15)))
        c.pixel(x, y, BLACK)
        c.pixel(x, y + 1, BLACK)
    c.circle(430, 412, 6, DARK_GREEN, MED_GREEN)

    caption(c, "Figure 1: Schematic of a typical MAF system and the magnetic abrasive brush.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1.png'))


# ---------------------------------------------------------------------------
# Figure 2: Three stages of surface topography evolution
# ---------------------------------------------------------------------------
def fig2():
    c = new_canvas()
    title(c, "Three Stages of Surface Topography Evolution")

    random.seed(1)
    panels = [("Stage I: Engagement", 40, 3.0),
              ("Stage II: Micro-cutting", 285, 1.6),
              ("Stage III: Leveling", 530, 0.7)]
    for label, x0, amp in panels:
        base = 300
        c.rect(x0, 90, x0 + 200, 330, GRAY, (250, 250, 250))
        c.text_c(x0 + 100, 100, label, BLACK, 1)
        # surface profile with decreasing amplitude
        prev = None
        for i in range(x0 + 10, x0 + 190):
            r = (math.sin(i * 0.25) + 0.5 * math.sin(i * 0.6) +
                 0.3 * random.uniform(-1, 1))
            y = int(base - amp * 12 * r)
            if prev:
                c.line(prev[0], prev[1], i, y, MED_BLUE, 2)
            prev = (i, y)
        # abrasive grains above
        for g in range(6):
            gx = x0 + 25 + g * 28
            c.circle(gx, 150, 7, DARK_GREEN, MED_GREEN)
        c.hline(x0 + 10, x0 + 190, base + 15, BLACK)
        c.text(x0 + 60, base + 22, "workpiece", BLACK, 1)

    # arrows between panels
    c.arrow(245, 210, 280, 210, ORANGE, 2, 8)
    c.arrow(490, 210, 525, 210, ORANGE, 2, 8)
    c.text(250, 190, "time", ORANGE, 1)
    c.text(495, 190, "time", ORANGE, 1)

    caption(c, "Figure 2: Evolution of surface topography through the three finishing stages.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2.png'))


# ---------------------------------------------------------------------------
# Figure 3: Single abrasive grain micro-mechanics
# ---------------------------------------------------------------------------
def fig3():
    c = new_canvas()
    title(c, "Micro-scale Interaction of a Single Abrasive Grain")

    # Surface
    c.fill_rect(120, 300, 640, 380, LIGHT_ORANGE)
    c.hline(120, 640, 300, BLACK)
    c.text(130, 355, "Workpiece (hardness resists penetration)", BLACK, 1)

    # Grain (cone) indenting
    cx, cy = 380, 260
    c.line(cx, cy, cx - 30, 300, BLACK, 2)
    c.line(cx, cy, cx + 30, 300, BLACK, 2)
    c.line(cx - 30, 300, cx + 30, 300, BLACK, 2)
    c.text(cx - 20, 235, "grain", BLACK, 1)

    # Normal force (down) and tangential force (along)
    c.arrow(cx, cy - 5, cx, cy + 55, RED, 3, 9)
    c.text(cx + 8, cy + 20, "Fn (normal)", RED, 1)
    c.arrow(cx + 40, 285, cx + 130, 285, MED_BLUE, 3, 9)
    c.text(cx + 55, 268, "Ft (tangential)", MED_BLUE, 1)

    # regimes bar
    c.text(130, 405, "Increasing penetration / attack angle:", BLACK, 1)
    segs = [("Sliding", 130, LIGHT_GRAY), ("Ploughing", 330, LIGHT_GREEN),
            ("Micro-cutting", 520, LIGHT_ORANGE)]
    for lbl, x, col in segs:
        c.rect(x, 420, x + 170, 450, BLACK, col)
        c.text_c(x + 85, 430, lbl, BLACK, 1)
    c.arrow(130, 465, 690, 465, ORANGE, 2, 8)

    caption(c, "Figure 3: Normal/tangential forces and the sliding-ploughing-cutting transition.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3.png'))


# ---------------------------------------------------------------------------
# Figure 4: Ra vs finishing time, families for flux density
# ---------------------------------------------------------------------------
def fig4():
    c = new_canvas()
    title(c, "Surface Roughness vs Finishing Time")
    x0, x1, ytop, ybot = 90, 700, 70, 400
    axes(c, x0, ybot, x1, ytop)
    c.text(30, 60, "Ra", BLACK, 1)
    c.text(x1 - 70, ybot + 15, "Time (min)", BLACK, 1)
    c.text(20, ybot - 5, "high", BLACK, 1)
    c.text(25, ytop, "low", BLACK, 1)

    # different flux densities -> different rates & saturation
    cfgs = [(RED, 1.6, 0.85, "B low"),
            (ORANGE, 2.6, 0.60, "B med"),
            (MED_BLUE, 4.0, 0.38, "B high")]
    for i, (col, rate, sat, lbl) in enumerate(cfgs):
        curve(c, x0, x1, lambda t, r=rate, s=sat: s + (1 - s) * math.exp(-r * t),
              col, ytop, ybot, 2)
        c.hline(x1 - 120, x1 - 90, ytop + 20 + i * 16, col)
        c.text(x1 - 85, ytop + 15 + i * 16, lbl, BLACK, 1)
    # saturation annotation
    c.text(300, ytop + 30, "approach to saturation", GRAY, 1)

    caption(c, "Figure 4: Time-roughness curves showing saturation; families vary flux density.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4.png'))


# ---------------------------------------------------------------------------
# Figure 5: Response surfaces (interaction) - contour style
# ---------------------------------------------------------------------------
def _contour_panel(c, x0, y0, size, fn, label):
    n = size
    # draw filled by shading based on value
    for i in range(n):
        for j in range(n):
            u = i / float(n)
            v = j / float(n)
            val = fn(u, v)
            # map val 0..1 to color between MED_BLUE(low) and RED(high)
            r = int(60 + val * 180)
            g = int(90 + (1 - val) * 100)
            b = int(200 - val * 150)
            c.pixel(x0 + i, y0 + (n - 1 - j), (r, g, b))
    c.rect(x0, y0, x0 + n, y0 + n, BLACK)
    c.text_c(x0 + n // 2, y0 + n + 6, label, BLACK, 1)


def fig5():
    c = new_canvas()
    title(c, "Interaction Effects: Roughness Response Surfaces")

    def bowl(u, v, cu, cv):
        d = (u - cu) ** 2 + (v - cv) ** 2
        return max(0.0, min(1.0, d * 2.2))

    _contour_panel(c, 70, 90, 150, lambda u, v: bowl(u, v, 0.4, 0.5),
                   "B x G  (gap low)")
    _contour_panel(c, 300, 90, 150, lambda u, v: bowl(u, v, 0.6, 0.4),
                   "B x G  (gap med)")
    _contour_panel(c, 530, 90, 150, lambda u, v: bowl(u, v, 0.75, 0.35),
                   "B x G  (gap high)")
    c.text(70, 270, "The location of the roughness minimum (dark) shifts as the third", BLACK, 1)
    c.text(70, 288, "parameter (working gap) changes - a hallmark of high-order interaction.", BLACK, 1)
    # legend
    c.text(70, 330, "Low roughness", MED_BLUE, 1)
    c.fill_rect(200, 328, 240, 342, MED_BLUE)
    c.fill_rect(240, 328, 280, 342, (150, 100, 120))
    c.fill_rect(280, 328, 320, 342, RED)
    c.text(325, 330, "High roughness", RED, 1)

    caption(c, "Figure 5: Roughness response surfaces over B and rotational speed at three gaps.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_5.png'))


# ---------------------------------------------------------------------------
# Figure 6: Experimental design strategies (4 panels)
# ---------------------------------------------------------------------------
def fig6():
    c = new_canvas()
    title(c, "Experimental Design Strategies")
    random.seed(7)
    boxes = [(60, "(a) Full factorial"), (250, "(b) Central composite"),
             (440, "(c) Latin hypercube"), (620, "(d) Sequential/active")]

    def frame(x):
        c.rect(x, 90, x + 150, 240, BLACK, (252, 252, 252))

    # (a) corners
    x = 60; frame(x)
    for px in (x + 15, x + 135):
        for py in (105, 225):
            c.circle(px, py, 5, MED_BLUE, MED_BLUE)
    c.text_c(x + 75, 250, boxes[0][1], BLACK, 1)

    # (b) ccd
    x = 250; frame(x)
    for px in (x + 25, x + 125):
        for py in (115, 215):
            c.circle(px, py, 5, MED_BLUE, MED_BLUE)
    c.circle(x + 75, 165, 5, ORANGE, ORANGE)
    for px, py in [(x + 10, 165), (x + 140, 165), (x + 75, 100), (x + 75, 230)]:
        c.circle(px, py, 5, MED_GREEN, MED_GREEN)
    c.text_c(x + 75, 250, boxes[1][1], BLACK, 1)

    # (c) LHS
    x = 440; frame(x)
    for k in range(10):
        c.circle(x + 12 + int(k * 13.2), 100 + random.randint(0, 130), 5,
                 PURPLE, PURPLE)
    c.text_c(x + 75, 250, boxes[2][1], BLACK, 1)

    # (d) sequential
    x = 620; frame(x)
    for k in range(6):
        c.circle(x + 15 + k * 20, 110 + random.randint(0, 120), 4,
                 GRAY, GRAY)
    for px, py in [(x + 90, 150), (x + 105, 170), (x + 120, 140)]:
        c.circle(px, py, 6, RED, RED)
    c.text_c(x + 75, 250, boxes[3][1], BLACK, 1)
    c.text(x - 5, 268, "red = high-uncertainty", RED, 1)

    caption(c, "Figure 6: Corner-based vs space-filling vs sequential designs in a 2-parameter space.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_6.png'))


# ---------------------------------------------------------------------------
# Figure 7: Preprocessing pipeline
# ---------------------------------------------------------------------------
def fig7():
    c = new_canvas()
    title(c, "Data Preprocessing Pipeline")
    steps = ["Raw data", "Clean", "Impute", "Outliers", "Scale",
             "Encode", "Engineer", "Select", "Split"]
    cols = [LIGHT_GRAY, LIGHT_BLUE, LIGHT_BLUE, LIGHT_GREEN, LIGHT_GREEN,
            LIGHT_ORANGE, LIGHT_ORANGE, LIGHT_PURPLE, LIGHT_GOLD]
    x = 30
    y = 150
    for i, (s, col) in enumerate(zip(steps, cols)):
        c.rect(x, y, x + 68, y + 55, BLACK, col)
        c.text_c(x + 34, y + 24, s, BLACK, 1)
        if i < len(steps) - 1:
            c.arrow(x + 68, y + 27, x + 80, y + 27, GRAY, 2, 6)
        x += 80
    # model-ready output
    c.rect(300, 260, 460, 320, DARK_GREEN, LIGHT_GREEN)
    c.text_c(380, 278, "Model-ready", BLACK, 1)
    c.text_c(380, 295, "X (features), Y (Ra)", BLACK, 1)
    c.arrow(380, 215, 380, 258, GRAY, 2, 7)
    c.text(120, 360, "All fitted transforms (scale/impute/select) learned from TRAINING data only.", RED, 1)
    caption(c, "Figure 7: The preprocessing pipeline from raw records to a model-ready dataset.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_7.png'))


# ---------------------------------------------------------------------------
# Figure 8: k-fold cross-validation
# ---------------------------------------------------------------------------
def fig8():
    c = new_canvas()
    title(c, "k-Fold Cross-Validation (k = 5)")
    k = 5
    cell_w = 110
    x0 = 120
    y0 = 90
    row_h = 55
    for row in range(k):
        y = y0 + row * (row_h + 8)
        c.text(30, y + 20, "Iter " + str(row + 1), BLACK, 1)
        for col in range(k):
            x = x0 + col * (cell_w + 5)
            if col == row:
                c.rect(x, y, x + cell_w, y + row_h, BLACK, LIGHT_ORANGE)
                c.text_c(x + cell_w // 2, y + 20, "VALID", BLACK, 1)
            else:
                c.rect(x, y, x + cell_w, y + row_h, BLACK, LIGHT_BLUE)
                c.text_c(x + cell_w // 2, y + 20, "train", BLACK, 1)
    c.text(120, y0 + k * (row_h + 8) + 15,
           "Each fold serves once for validation; the k scores are averaged.", BLACK, 1)
    caption(c, "Figure 8: k-fold cross-validation uses scarce data efficiently for validation.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_8.png'))


# ---------------------------------------------------------------------------
# Figure 9: Map of algorithm families (flexibility vs interpretability)
# ---------------------------------------------------------------------------
def fig9():
    c = new_canvas()
    title(c, "Map of ML Algorithm Families")
    x0, x1, ytop, ybot = 110, 700, 80, 400
    axes(c, x0, ybot, x1, ytop)
    c.text(x1 - 130, ybot + 15, "Interpretability >", BLACK, 1)
    c.text(20, 75, "Flexibility", BLACK, 1)
    c.arrow(x0, ybot, x1, ybot, BLACK, 1, 6)
    c.arrow(x0, ybot, x0, ytop, BLACK, 1, 6)

    pts = [("Linear", 640, 380, GRAY),
           ("kNN", 520, 350, LIGHT_BLUE),
           ("Decision tree", 590, 300, MED_GREEN),
           ("SVR", 300, 200, MED_BLUE),
           ("Random forest", 470, 210, DARK_GREEN),
           ("Gradient boost", 360, 150, ORANGE),
           ("Gaussian proc.", 330, 240, PURPLE),
           ("Neural net", 200, 120, RED)]
    for lbl, x, y, col in pts:
        c.circle(x, y, 9, BLACK, col)
        c.text(x + 12, y - 4, lbl, BLACK, 1)

    caption(c, "Figure 9: Algorithm families positioned by flexibility and interpretability.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_9.png'))


# ---------------------------------------------------------------------------
# Figure 10: Feedforward neural network
# ---------------------------------------------------------------------------
def fig10():
    c = new_canvas()
    title(c, "Feedforward Neural Network for Ra Prediction")
    layers = [(120, 6, "Inputs\n(B,N,G,C,D,T)"), (330, 5, "Hidden 1"),
              (500, 4, "Hidden 2"), (660, 1, "Output Ra")]
    positions = []
    for lx, n, lbl in layers:
        ys = []
        span = 300
        top = 110
        for i in range(n):
            y = top + (span * i // max(1, n - 1)) if n > 1 else top + span // 2
            ys.append(y)
        positions.append((lx, ys))
    # connections
    for li in range(len(positions) - 1):
        lx, ys = positions[li]
        lx2, ys2 = positions[li + 1]
        for y in ys:
            for y2 in ys2:
                c.line(lx, y, lx2, y2, LIGHT_GRAY, 1)
    # nodes
    palette = [MED_BLUE, MED_GREEN, ORANGE, RED]
    for li, (lx, ys) in enumerate(positions):
        for y in ys:
            c.circle(lx, y, 12, BLACK, palette[li % len(palette)])
    c.text(80, 420, "Inputs: B,N,G,C,D,T", BLACK, 1)
    c.text(300, 420, "Hidden layers (nonlinear activation)", BLACK, 1)
    c.text(610, 420, "Output: Ra", BLACK, 1)
    # neuron inset
    c.text(300, 90, "y = f( sum(wi*xi) + b )", PURPLE, 1)
    caption(c, "Figure 10: A compact feedforward ANN mapping process parameters to Ra.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_10.png'))


# ---------------------------------------------------------------------------
# Figure 11: SVR epsilon-tube
# ---------------------------------------------------------------------------
def fig11():
    c = new_canvas()
    title(c, "Support Vector Regression: Epsilon-Insensitive Tube")
    x0, x1, ytop, ybot = 90, 700, 90, 390
    axes(c, x0, ybot, x1, ytop)
    random.seed(3)
    eps = 22

    def f(t):
        return 0.25 + 0.5 * t + 0.12 * math.sin(3.5 * t)

    # central function
    prev = None
    for x in range(x0, x1):
        t = (x - x0) / float(x1 - x0)
        y = int(ybot - f(t) * (ybot - ytop))
        if prev:
            c.line(prev[0], prev[1], x, y, MED_BLUE, 2)
        prev = (x, y)
    # tube lines
    for off in (-eps, eps):
        prev = None
        for x in range(x0, x1):
            t = (x - x0) / float(x1 - x0)
            y = int(ybot - f(t) * (ybot - ytop)) + off
            if prev and x % 4 < 2:
                c.line(prev[0], prev[1], x, y, GRAY, 1)
            prev = (x, y)
    # data points
    for _ in range(40):
        x = random.randint(x0 + 10, x1 - 10)
        t = (x - x0) / float(x1 - x0)
        yc = int(ybot - f(t) * (ybot - ytop))
        y = yc + random.randint(-40, 40)
        inside = abs(y - yc) <= eps
        col = LIGHT_BLUE if inside else RED
        c.circle(x, y, 4, BLACK, col)
    c.text(x1 - 150, ytop + 10, "red = support vectors", RED, 1)
    c.text(x1 - 150, ytop + 26, "grey = epsilon tube", GRAY, 1)
    caption(c, "Figure 11: Only points outside the epsilon-tube (support vectors) shape the fit.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_11.png'))


# ---------------------------------------------------------------------------
# Figure 12: Random forest ensemble
# ---------------------------------------------------------------------------
def _mini_tree(c, cx, cy, col):
    c.circle(cx, cy, 7, BLACK, col)
    c.line(cx, cy, cx - 22, cy + 30, BLACK, 1)
    c.line(cx, cy, cx + 22, cy + 30, BLACK, 1)
    c.circle(cx - 22, cy + 30, 5, BLACK, col)
    c.circle(cx + 22, cy + 30, 5, BLACK, col)
    c.line(cx - 22, cy + 30, cx - 33, cy + 55, BLACK, 1)
    c.line(cx - 22, cy + 30, cx - 11, cy + 55, BLACK, 1)
    c.line(cx + 22, cy + 30, cx + 11, cy + 55, BLACK, 1)
    c.line(cx + 22, cy + 30, cx + 33, cy + 55, BLACK, 1)
    for dx in (-33, -11, 11, 33):
        c.circle(cx + dx, cy + 55, 4, BLACK, col)


def fig12():
    c = new_canvas()
    title(c, "Random Forest Ensemble")
    cols = [MED_GREEN, MED_BLUE, ORANGE, PURPLE]
    for i in range(4):
        _mini_tree(c, 110 + i * 160, 120, cols[i])
        c.text_c(110 + i * 160, 195, "Tree " + str(i + 1), BLACK, 1)
        c.arrow(110 + i * 160, 205, 380, 285, GRAY, 1, 6)
    c.rect(300, 290, 460, 345, DARK_GREEN, LIGHT_GREEN)
    c.text_c(380, 305, "Average", BLACK, 1)
    c.text_c(380, 322, "-> Ra prediction", BLACK, 1)
    c.text(120, 370, "Each tree: bootstrap sample + random feature subset per split.", BLACK, 1)
    c.text(120, 390, "Averaging decorrelated trees reduces variance -> robust prediction.", BLACK, 1)
    caption(c, "Figure 12: Bagged decision trees averaged into a robust ensemble prediction.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_12.png'))


# ---------------------------------------------------------------------------
# Figure 13: Smooth vs stepped response surfaces
# ---------------------------------------------------------------------------
def fig13():
    c = new_canvas()
    title(c, "Smooth vs Stepped Model Response Surfaces")
    # left: smooth
    x0, x1, ytop, ybot = 70, 360, 100, 360
    axes(c, x0, ybot, x1, ytop)
    c.text_c((x0 + x1) // 2, ybot + 18, "(a) Smooth (ANN/SVR/GPR)", BLACK, 1)
    curve(c, x0, x1, lambda t: 0.5 + 0.4 * math.sin(2.5 * t + 0.3), MED_BLUE, ytop, ybot, 2)
    # right: stepped
    x0, x1 = 430, 720
    axes(c, x0, ybot, x1, ytop)
    c.text_c((x0 + x1) // 2, ybot + 18, "(b) Stepped (tree ensembles)", BLACK, 1)
    steps = 9
    prevy = None
    for s in range(steps):
        t = s / float(steps)
        v = 0.5 + 0.4 * math.sin(2.5 * t + 0.3)
        y = int(ybot - v * (ybot - ytop))
        xa = x0 + int((x1 - x0) * s / steps)
        xb = x0 + int((x1 - x0) * (s + 1) / steps)
        c.hline(xa, xb, y, ORANGE)
        c.line(xa, y, xa, y + 2, ORANGE, 2)
        if prevy is not None:
            c.vline(xa, min(prevy, y), max(prevy, y), ORANGE)
        prevy = y
    caption(c, "Figure 13: Smooth learners vs the piecewise-constant surfaces of tree ensembles.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_13.png'))


# ---------------------------------------------------------------------------
# Figure 14: Predicted vs measured scatter
# ---------------------------------------------------------------------------
def fig14():
    c = new_canvas()
    title(c, "Predicted vs Measured Surface Roughness")
    x0, x1, ytop, ybot = 110, 690, 80, 400
    axes(c, x0, ybot, x1, ytop)
    c.text(x1 - 150, ybot + 15, "Measured Ra", BLACK, 1)
    c.text(20, 75, "Predicted Ra", BLACK, 1)
    # ideal line
    c.line(x0, ybot, x1, ytop, GRAY, 1)
    c.text(x1 - 120, ytop + 10, "ideal (y = x)", GRAY, 1)
    random.seed(11)
    for _ in range(70):
        t = random.random()
        mx = x0 + int(t * (x1 - x0))
        my = ybot - int(t * (ybot - ytop))
        noise = random.randint(-18, 18)
        c.circle(mx, my + noise, 4, BLACK, MED_BLUE)
    caption(c, "Figure 14: Predicted vs measured plot; scatter about y = x reveals bias and spread.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_14.png'))


# ---------------------------------------------------------------------------
# Figure 15: Learning curves
# ---------------------------------------------------------------------------
def fig15():
    c = new_canvas()
    title(c, "Learning Curves")
    x0, x1, ytop, ybot = 100, 690, 80, 400
    axes(c, x0, ybot, x1, ytop)
    c.text(x1 - 160, ybot + 15, "Training set size", BLACK, 1)
    c.text(20, 75, "Error", BLACK, 1)
    # validation error decreasing, training error increasing toward it
    curve(c, x0, x1, lambda t: 0.15 + 0.6 * math.exp(-2.5 * t), RED, ytop, ybot, 2)
    curve(c, x0, x1, lambda t: 0.05 + 0.25 * (1 - math.exp(-3.0 * t)), MED_BLUE, ytop, ybot, 2)
    # noise floor
    yf = int(ybot - 0.12 * (ybot - ytop))
    for x in range(x0, x1, 6):
        c.pixel(x, yf, GRAY); c.pixel(x + 1, yf, GRAY)
    c.text(x1 - 150, yf - 14, "noise floor", GRAY, 1)
    c.hline(x1 - 150, x1 - 120, ytop + 20, RED); c.text(x1 - 115, ytop + 15, "validation", BLACK, 1)
    c.hline(x1 - 150, x1 - 120, ytop + 36, MED_BLUE); c.text(x1 - 115, ytop + 31, "training", BLACK, 1)
    caption(c, "Figure 15: Learning curves; gap to noise floor indicates room for more data.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_15.png'))


# ---------------------------------------------------------------------------
# Figure 16: Predictive uncertainty band
# ---------------------------------------------------------------------------
def fig16():
    c = new_canvas()
    title(c, "Predictive Uncertainty Widens Where Data Are Sparse")
    x0, x1, ytop, ybot = 90, 700, 80, 400
    axes(c, x0, ybot, x1, ytop)
    c.text(x1 - 130, ybot + 15, "Parameter", BLACK, 1)
    c.text(20, 75, "Ra", BLACK, 1)

    def mean(t):
        return 0.5 + 0.28 * math.sin(3.2 * t)

    # band width small near data clusters (t~0.2, 0.75), large elsewhere
    def width(t):
        d = min(abs(t - 0.2), abs(t - 0.75))
        return 8 + d * 90

    for x in range(x0, x1):
        t = (x - x0) / float(x1 - x0)
        yc = int(ybot - mean(t) * (ybot - ytop))
        w = int(width(t))
        for yy in range(yc - w, yc + w):
            if ytop <= yy <= ybot and (yy % 3 == 0):
                c.pixel(x, yy, LIGHT_BLUE)
    # mean curve
    curve(c, x0, x1, mean, MED_BLUE, ytop, ybot, 2)
    # data points at clusters
    random.seed(5)
    for center in (0.2, 0.75):
        for _ in range(9):
            t = center + random.uniform(-0.05, 0.05)
            x = x0 + int(t * (x1 - x0))
            y = int(ybot - mean(t) * (ybot - ytop)) + random.randint(-6, 6)
            c.circle(x, y, 4, BLACK, RED)
    c.text(x0 + 30, ytop + 10, "narrow band = confident (near data)", BLACK, 1)
    c.text(x0 + 250, ytop + 30, "wide band = uncertain (sparse)", BLACK, 1)
    caption(c, "Figure 16: Uncertainty band narrow near data, wide in sparsely sampled regions.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_16.png'))


# ---------------------------------------------------------------------------
# Figure 17: Feature importance + partial dependence
# ---------------------------------------------------------------------------
def fig17():
    c = new_canvas()
    title(c, "Model Explainability")
    # (a) feature importance bars
    c.text(60, 70, "(a) Feature importance", BLACK, 1)
    feats = [("Grain D", 0.30, ORANGE), ("Flux B", 0.26, RED),
             ("Time T", 0.20, MED_BLUE), ("Gap G", 0.14, MED_GREEN),
             ("Speed N", 0.06, PURPLE), ("Conc C", 0.04, GOLD)]
    x0 = 130
    ybase = 250
    for i, (name, imp, col) in enumerate(feats):
        y = 95 + i * 26
        c.text(50, y + 2, name, BLACK, 1)
        c.rect(x0, y, x0 + int(imp * 500), y + 18, BLACK, col)
    # (b) partial dependence for flux density (non-monotonic)
    c.text(430, 70, "(b) Partial dependence (Flux B)", BLACK, 1)
    x0p, x1p, ytop, ybot = 440, 700, 110, 360
    axes(c, x0p, ybot, x1p, ytop)
    curve(c, x0p, x1p, lambda t: 0.25 + 1.6 * (t - 0.55) ** 2, MED_BLUE, ytop, ybot, 2)
    c.text(x0p + 60, ybot + 15, "Flux density B", BLACK, 1)
    c.text(x0p - 30, 100, "Ra", BLACK, 1)
    c.text(x0p + 70, ytop + 6, "interior optimum", GRAY, 1)
    caption(c, "Figure 17: Feature importance ranking and a partial-dependence relationship.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_17.png'))


# ---------------------------------------------------------------------------
# Figure 18: Pareto front
# ---------------------------------------------------------------------------
def fig18():
    c = new_canvas()
    title(c, "Pareto Front: Roughness vs Finishing Time")
    x0, x1, ytop, ybot = 100, 690, 80, 400
    axes(c, x0, ybot, x1, ytop)
    c.text(x1 - 150, ybot + 15, "Finishing time", BLACK, 1)
    c.text(20, 75, "Ra", BLACK, 1)
    # front: convex decreasing
    pts = []
    for i in range(9):
        t = i / 8.0
        x = x0 + int(t * (x1 - x0))
        v = 0.15 + 0.7 * math.exp(-2.6 * t)
        y = int(ybot - v * (ybot - ytop))
        pts.append((x, y))
    for i in range(len(pts) - 1):
        c.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], RED, 2)
    for px, py in pts:
        c.circle(px, py, 5, BLACK, RED)
    # dominated points above front
    random.seed(9)
    for _ in range(30):
        x = random.randint(x0 + 20, x1 - 20)
        t = (x - x0) / float(x1 - x0)
        yf = int(ybot - (0.15 + 0.7 * math.exp(-2.6 * t)) * (ybot - ytop))
        y = random.randint(ytop + 10, yf - 12)
        c.circle(x, y, 3, LIGHT_BLUE, LIGHT_BLUE)
    c.circle(x1 - 150, ytop + 20, 5, BLACK, RED); c.text(x1 - 138, ytop + 16, "Pareto-efficient", BLACK, 1)
    c.circle(x1 - 150, ytop + 38, 3, LIGHT_BLUE, LIGHT_BLUE); c.text(x1 - 138, ytop + 34, "dominated", BLACK, 1)
    caption(c, "Figure 18: The Pareto front presents the menu of efficient roughness-time trade-offs.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_18.png'))


# ---------------------------------------------------------------------------
# Figure 19: Closed-loop Bayesian optimization / active learning cycle
# ---------------------------------------------------------------------------
def fig19():
    c = new_canvas()
    title(c, "Closed-Loop Uncertainty-Guided Experimentation")
    nodes = [("Fit surrogate\n(GP + uncertainty)", 200, 130, MED_BLUE, LIGHT_BLUE),
             ("Acquisition:\nexplore/exploit", 560, 130, PURPLE, LIGHT_PURPLE),
             ("Run selected\nexperiment", 560, 320, MED_GREEN, LIGHT_GREEN),
             ("Add data,\nupdate model", 200, 320, ORANGE, LIGHT_ORANGE)]
    centers = []
    for lbl, x, y, col, fill in nodes:
        c.rect(x - 90, y - 35, x + 90, y + 35, col, fill)
        parts = lbl.split("\n")
        for i, p in enumerate(parts):
            c.text_c(x, y - 8 + i * 15, p, BLACK, 1)
        centers.append((x, y))
    c.arrow(290, 120, 470, 120, GRAY, 2, 8)
    c.arrow(560, 165, 560, 285, GRAY, 2, 8)
    c.arrow(470, 330, 290, 330, GRAY, 2, 8)
    c.arrow(200, 285, 200, 165, GRAY, 2, 8)
    c.text_c(380, 100, "iterate to optimum with minimum experiments", GOLD, 1)
    caption(c, "Figure 19: Bayesian optimization / active-learning loop for efficient experimentation.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_19.png'))


# ---------------------------------------------------------------------------
# Figure 20: Comparative performance across algorithm families
# ---------------------------------------------------------------------------
def fig20():
    c = new_canvas()
    title(c, "Comparative Model Performance (R-squared)")
    x0, x1, ytop, ybot = 110, 700, 90, 380
    axes(c, x0, ybot, x1, ytop)
    c.text(20, 80, "R^2", BLACK, 1)
    algos = [("Linear", 0.62, GRAY), ("kNN", 0.74, LIGHT_BLUE),
             ("ANN", 0.90, RED), ("SVR", 0.92, MED_BLUE),
             ("RF", 0.93, DARK_GREEN), ("GBM", 0.95, ORANGE),
             ("XGBoost", 0.96, GOLD), ("GPR", 0.94, PURPLE)]
    n = len(algos)
    slot = (x1 - x0) // n
    for i, (name, r2, col) in enumerate(algos):
        bx = x0 + i * slot + 10
        bw = slot - 20
        bh = int((r2 - 0.5) / 0.5 * (ybot - ytop))
        c.rect(bx, ybot - bh, bx + bw, ybot, BLACK, col)
        c.text_c(bx + bw // 2, ybot + 8, name, BLACK, 1)
        c.text_c(bx + bw // 2, ybot - bh - 12, "%.2f" % r2, BLACK, 1)
    # error-bar style whisker (indicative spread)
    for i, (name, r2, col) in enumerate(algos):
        bx = x0 + i * slot + 10 + (slot - 20) // 2
        top = ybot - int((r2 - 0.5) / 0.5 * (ybot - ytop))
        c.vline(bx, top - 10, top + 10, BLACK)
    caption(c, "Figure 20: Indicative R-squared across families; ensembles/SVR/GPR strong on small data.")
    c.save(os.path.join(OUTPUT_DIR, 'Figure_20.png'))


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    funcs = [fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10,
             fig11, fig12, fig13, fig14, fig15, fig16, fig17, fig18, fig19, fig20]
    for i, fn in enumerate(funcs, 1):
        fn()
        print("Figure_%d.png done" % i)
    print("\nAll figures saved to %s/" % OUTPUT_DIR)


if __name__ == '__main__':
    main()
