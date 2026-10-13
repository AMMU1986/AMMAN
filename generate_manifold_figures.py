#!/usr/bin/env python3
"""
Generate 4 figure images (PNG) for the chapter
"Application of Manifolds in General Relativity and Cosmology".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs with no third-party dependencies (matplotlib is unavailable and the
sandbox has no PyPI access).

Figures:
  Figure 1 - Manifold with overlapping charts, transition map, tangent space,
             and light-cone (causal) structure.
  Figure 2 - Geodesic deviation on a curved surface, the Einstein-equation
             balance G = 8 pi T, and gravitational light bending.
  Figure 3 - The three FLRW spatial geometries (closed, flat, open) and the
             evolution of the scale factor a(t).
  Figure 4 - Advanced tools: vielbein (tetrad) frame on a worldline, an
             embedded hypersurface (Gauss-Codazzi), and a brane in a bulk.
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/manifold_figures'


def dashed_line(c, x1, y1, x2, y2, color, dash=8, gap=6, thick=1):
    """Draw a dashed straight line between two points."""
    dx, dy = x2 - x1, y2 - y1
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    ux, uy = dx / dist, dy / dist
    t = 0.0
    while t < dist:
        sx = int(x1 + ux * t)
        sy = int(y1 + uy * t)
        e = min(t + dash, dist)
        ex = int(x1 + ux * e)
        ey = int(y1 + uy * e)
        c.line(sx, sy, ex, ey, color, thick)
        t += dash + gap


def grid(c, x1, y1, x2, y2, color, step=18):
    """Draw a rectangular coordinate grid."""
    x = x1
    while x <= x2:
        c.vline(x, y1, y2, color)
        x += step
    y = y1
    while y <= y2:
        c.hline(x1, x2, y, color)
        y += step


def blob(c, cx, cy, rx, ry, outline, fill):
    """Draw a filled ellipse ('manifold' patch) with an outline."""
    for dy in range(-ry, ry + 1):
        span = int(rx * math.sqrt(max(0.0, 1.0 - (dy / ry) ** 2)))
        c.hline(cx - span, cx + span, cy + dy, fill)
    # outline
    prev = None
    for a in range(0, 361, 3):
        rad = math.radians(a)
        px = int(cx + rx * math.cos(rad))
        py = int(cy + ry * math.sin(rad))
        if prev:
            c.line(prev[0], prev[1], px, py, outline, 1)
        prev = (px, py)


def gen_fig1():
    """Figure 1: manifold, charts, transition map, tangent space, light cone."""
    c = PNGCanvas(820, 500)
    c.text_c(410, 10, "Spacetime Manifold: Charts, Tangent Space and Light Cones", BLACK, 2)

    # The manifold M as a large curved region
    blob(c, 410, 150, 330, 95, DARK_BLUE, PALE_BLUE)
    c.text(120, 70, "Manifold M", DARK_BLUE, 1)

    # Two overlapping coordinate patches U and V
    blob(c, 300, 155, 120, 62, MED_BLUE, LIGHT_BLUE)
    blob(c, 500, 155, 120, 62, DARK_GREEN, LIGHT_GREEN)
    c.text(235, 118, "Patch U", MED_BLUE, 1)
    c.text(520, 118, "Patch V", DARK_GREEN, 1)
    c.text(372, 200, "overlap", GRAY, 1)

    # Event p in the overlap, with tangent plane and light cone
    px, py = 410, 158
    c.circle(px, py, 4, BLACK, BLACK)
    c.text(px + 8, py - 4, "p", BLACK, 1)
    # tangent plane (parallelogram)
    c.line(px - 55, py + 18, px + 55, py + 18, ORANGE, 2)
    c.line(px + 55, py + 18, px + 78, py - 2, ORANGE, 2)
    c.line(px + 78, py - 2, px - 32, py - 2, ORANGE, 2)
    c.line(px - 32, py - 2, px - 55, py + 18, ORANGE, 2)
    c.text(px + 82, py + 6, "tangent space Tp M", ORANGE, 1)
    # light cone at p (double cone)
    c.line(px, py, px - 26, py - 40, RED, 2)
    c.line(px, py, px + 26, py - 40, RED, 2)
    c.line(px - 26, py - 40, px + 26, py - 40, RED, 1)
    c.line(px, py, px - 26, py + 40, RED, 2)
    c.line(px, py, px + 26, py + 40, RED, 2)
    c.text(px + 30, py - 44, "light cone", RED, 1)
    c.text(px + 30, py - 30, "future", GRAY, 1)

    # Charts down to R^2 with coordinate grids
    gy1, gy2 = 330, 430
    # phi(U)
    c.rect(120, gy1, 320, gy2, MED_BLUE)
    grid(c, 121, gy1 + 1, 319, gy2 - 1, LIGHT_BLUE)
    c.text(150, gy2 + 10, "phi(U) in R^2", MED_BLUE, 1)
    # psi(V)
    c.rect(500, gy1, 700, gy2, DARK_GREEN)
    grid(c, 501, gy1 + 1, 699, gy2 - 1, LIGHT_GREEN)
    c.text(530, gy2 + 10, "psi(V) in R^2", DARK_GREEN, 1)

    # Projection arrows from patches to charts
    c.arrow(280, 205, 230, gy1 - 4, MED_BLUE, 2, 9)
    c.text(150, 250, "chart phi", MED_BLUE, 1)
    c.arrow(520, 205, 600, gy1 - 4, DARK_GREEN, 2, 9)
    c.text(605, 250, "chart psi", DARK_GREEN, 1)

    # Transition map between the two charts
    c.arrow(322, 380, 498, 380, PURPLE, 3, 11)
    c.arrow(498, 405, 322, 405, PURPLE, 2, 9)
    c.text(360, 355, "transition map (smooth)", PURPLE, 1)
    c.text(360, 412, "psi o phi inverse", GRAY, 1)

    c.text(30, 478, "Figure 1: Overlapping charts on a manifold, related by a smooth transition map, "
                    "with tangent space and light cone at event p", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Manifold_Charts.png'))
    print("  Figure_1_Manifold_Charts.png done")


def gen_fig2():
    """Figure 2: geodesic deviation, Einstein equation, light bending."""
    c = PNGCanvas(820, 520)
    c.text_c(410, 10, "Curvature, Einstein Field Equations and Light Bending", BLACK, 2)

    # ---- Left panel: geodesic deviation on a curved surface ----
    c.text(70, 45, "(a) Geodesic deviation", BLACK, 1)
    blob(c, 190, 175, 150, 95, DARK_BLUE, PALE_BLUE)
    # two geodesics that start parallel (bottom) and converge (top)
    def geo(x0):
        pts = []
        for i in range(0, 21):
            t = i / 20.0
            x = int(x0 + (190 - x0) * (t ** 1.6))
            y = int(255 - t * 160)
            pts.append((x, y))
        return pts
    for path, col in [(geo(120), DARK_GREEN), (geo(260), RED)]:
        for k in range(len(path) - 1):
            c.line(path[k][0], path[k][1], path[k + 1][0], path[k + 1][1], col, 2)
    # separation markers
    c.line(120, 250, 260, 250, GRAY, 1)
    c.text(150, 256, "initial separation", GRAY, 1)
    c.line(178, 100, 202, 100, GRAY, 1)
    c.text(150, 82, "converging", GRAY, 1)
    c.text(70, 300, "Curvature -> tidal", BLACK, 1)
    c.text(70, 314, "acceleration of", BLACK, 1)
    c.text(70, 328, "nearby geodesics", BLACK, 1)

    # ---- Right panel: Einstein equation balance ----
    c.text(470, 45, "(b) Field equations", BLACK, 1)
    c.rect(430, 70, 590, 150, DARK_GREEN, LIGHT_GREEN)
    c.text_c(510, 92, "CURVATURE", BLACK, 1)
    c.text_c(510, 110, "Einstein tensor", BLACK, 1)
    c.text_c(510, 126, "G_ab", BLACK, 1)
    c.rect(640, 70, 800, 150, ORANGE, LIGHT_ORANGE)
    c.text_c(720, 92, "MATTER-ENERGY", BLACK, 1)
    c.text_c(720, 110, "stress-energy", BLACK, 1)
    c.text_c(720, 126, "T_ab", BLACK, 1)
    c.text_c(615, 100, "=", BLACK, 2)
    c.text_c(615, 122, "8 pi T", GRAY, 1)
    c.arrow(590, 138, 640, 138, GRAY, 2, 8)
    c.arrow(640, 120, 590, 120, GRAY, 2, 8)
    c.text_c(615, 165, "G_ab = 8 pi G / c^4 T_ab", DARK_GREEN, 1)

    # ---- Bottom: light bending around a mass ----
    c.text(70, 360, "(c) Deflection of light by a massive body", BLACK, 1)
    sun_x, sun_y = 410, 440
    c.circle(sun_x, sun_y, 26, ORANGE, LIGHT_ORANGE)
    c.text_c(sun_x, sun_y - 4, "Sun", BLACK, 1)
    # star on the left, observer on the right
    c.circle(70, 415, 5, GOLD, GOLD)
    c.text(40, 392, "star", BLACK, 1)
    c.circle(770, 415, 5, MED_BLUE, MED_BLUE)
    c.text(740, 392, "observer", BLACK, 1)
    # true (straight) apparent path - dashed
    dashed_line(c, 770, 415, 70, 470, GRAY, 8, 6, 1)
    c.text(150, 476, "apparent (straight) direction", GRAY, 1)
    # actual bent ray: star -> curves near Sun -> observer
    bend = [(70, 415), (250, 425), (sun_x - 30, sun_y - 34),
            (sun_x + 40, sun_y - 30), (600, 420), (770, 415)]
    for k in range(len(bend) - 1):
        c.line(bend[k][0], bend[k][1], bend[k + 1][0], bend[k + 1][1], RED, 2)
    c.text(300, 398, "deflected light ray", RED, 1)

    c.text(30, 500, "Figure 2: Geodesic deviation, the balance of Einstein's equations, "
                    "and gravitational bending of starlight", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Curvature_Einstein.png'))
    print("  Figure_2_Curvature_Einstein.png done")


def gen_fig3():
    """Figure 3: FLRW spatial geometries and scale-factor evolution."""
    c = PNGCanvas(820, 520)
    c.text_c(410, 10, "FLRW Geometries and the Expanding Universe", BLACK, 2)

    # ---- Top: three spatial geometries ----
    # Closed (positive curvature) - sphere with lat/long lines
    c.text_c(150, 45, "Closed (k > 0)", DARK_GREEN, 1)
    cx, cy, r = 150, 130, 60
    c.circle(cx, cy, r, DARK_GREEN, LIGHT_GREEN)
    # longitude lines (vertical ellipse chords)
    for f in (0.5, 0.82):
        span_x = int(r * f)
        span_y = int(r * (1 - f * f) ** 0.5)
        c.line(cx - span_x, cy - span_y, cx - span_x, cy + span_y, MED_GREEN, 1)
        c.line(cx + span_x, cy - span_y, cx + span_x, cy + span_y, MED_GREEN, 1)
    # latitude circles (horizontal chords)
    for dy in (-30, 0, 30):
        span = int((r * r - dy * dy) ** 0.5)
        c.hline(cx - span, cx + span, cy + dy, MED_GREEN)
    c.text_c(150, 205, "spherical", GRAY, 1)

    # Flat (zero curvature) - square grid
    c.text_c(410, 45, "Flat (k = 0)", MED_BLUE, 1)
    c.rect(340, 75, 480, 190, MED_BLUE, PALE_BLUE)
    grid(c, 341, 76, 479, 189, LIGHT_BLUE, 20)
    c.text_c(410, 205, "Euclidean", GRAY, 1)

    # Open (negative curvature) - saddle-like grid
    c.text_c(670, 45, "Open (k < 0)", PURPLE, 1)
    ox1, oy0 = 600, 130
    # draw a saddle: family of curves bowing opposite ways
    for off in range(-50, 51, 20):
        prev = None
        for x in range(-70, 71, 7):
            y = int(oy0 + off - (x * x) / 140.0 + (off * off) / 260.0)
            px = ox1 + 70 + x
            if prev:
                c.line(prev[0], prev[1], px, y, LIGHT_PURPLE, 1)
            prev = (px, y)
    for x in range(-60, 61, 20):
        prev = None
        for yy in range(-55, 56, 7):
            y = int(oy0 + yy)
            xx = int(ox1 + 70 + x + (yy * yy) / 200.0 - (x * x) / 400.0)
            if prev:
                c.line(prev[0], prev[1], xx, y, PURPLE, 1)
            prev = (xx, y)
    c.text_c(670, 205, "hyperbolic", GRAY, 1)

    # ---- Bottom: scale factor a(t) ----
    c.text(60, 250, "Evolution of the scale factor a(t)", BLACK, 1)
    ax0, ay0 = 90, 470     # origin
    axmax, aymin = 720, 280
    c.arrow(ax0, ay0, axmax, ay0, BLACK, 2, 9)   # time axis
    c.arrow(ax0, ay0, ax0, aymin, BLACK, 2, 9)   # a axis
    c.text(axmax - 40, ay0 + 12, "time t", BLACK, 1)
    c.text(ax0 - 30, aymin - 2, "a(t)", BLACK, 1)

    def curve(fn, col, thick=2):
        prev = None
        for i in range(0, 121):
            t = i / 120.0
            x = int(ax0 + t * (axmax - ax0 - 20))
            y = int(ay0 - fn(t) * (ay0 - aymin - 10))
            if prev:
                c.line(prev[0], prev[1], x, y, col, thick)
            prev = (x, y)

    # decelerating (matter): a ~ t^(2/3)
    curve(lambda t: t ** 0.667, MED_GREEN)
    # coasting (empty): a ~ t
    curve(lambda t: t, MED_BLUE)
    # accelerating (dark energy): exponential-like
    curve(lambda t: (math.exp(1.7 * t) - 1) / (math.exp(1.7) - 1), RED)

    c.line(560, 300, 590, 300, RED, 2)
    c.text(596, 296, "accelerating (dark energy)", RED, 1)
    c.line(560, 320, 590, 320, MED_BLUE, 2)
    c.text(596, 316, "coasting (empty)", MED_BLUE, 1)
    c.line(560, 340, 590, 340, MED_GREEN, 2)
    c.text(596, 336, "decelerating (matter)", MED_GREEN, 1)

    c.text(30, 500, "Figure 3: The three FLRW spatial geometries and representative "
                    "expansion histories of the scale factor", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_FLRW_Geometries.png'))
    print("  Figure_3_FLRW_Geometries.png done")


def gen_fig4():
    """Figure 4: vielbein frame, embedded hypersurface, brane in bulk."""
    c = PNGCanvas(820, 500)
    c.text_c(410, 10, "Advanced Geometric Tools", BLACK, 2)

    # ---- (a) Vielbein / tetrad frame along a worldline ----
    c.text(50, 45, "(a) Vielbein (tetrad)", BLACK, 1)
    # worldline curve
    wl = []
    for i in range(0, 41):
        t = i / 40.0
        x = int(70 + t * 180)
        y = int(400 - t * 300 + 30 * math.sin(t * 6))
        wl.append((x, y))
    for k in range(len(wl) - 1):
        c.line(wl[k][0], wl[k][1], wl[k + 1][0], wl[k + 1][1], DARK_BLUE, 2)
    c.text(60, 410, "worldline", DARK_BLUE, 1)
    # orthonormal frames at two points
    for idx in (12, 30):
        ox, oy = wl[idx]
        c.arrow(ox, oy, ox + 34, oy - 6, RED, 2, 7)      # e_1
        c.arrow(ox, oy, ox + 6, oy - 34, DARK_GREEN, 2, 7)  # e_0 (time)
        c.circle(ox, oy, 3, BLACK, BLACK)
    c.text(150, 150, "orthonormal", ORANGE, 1)
    c.text(150, 164, "frame e_a", ORANGE, 1)
    c.text(150, 300, "flat metric in", GRAY, 1)
    c.text(150, 314, "each frame", GRAY, 1)

    # ---- (b) Embedded hypersurface (Gauss-Codazzi) ----
    c.text(330, 45, "(b) Hypersurface (Gauss-Codazzi)", BLACK, 1)
    # ambient spacetime block
    c.rect(330, 70, 560, 340, DARK_BLUE, PALE_BLUE)
    c.text(340, 78, "spacetime M", DARK_BLUE, 1)
    # the hypersurface Sigma as a slanted band
    c.line(345, 260, 545, 210, DARK_GREEN, 2)
    c.line(345, 275, 545, 225, DARK_GREEN, 2)
    c.text(360, 285, "hypersurface Sigma", DARK_GREEN, 1)
    # unit normal n
    midx, midy = 445, 235
    c.arrow(midx, midy, midx + 18, midy - 46, RED, 2, 8)
    c.text(midx + 22, midy - 40, "normal n", RED, 1)
    # tangent vector
    c.arrow(midx, midy, midx + 48, midy - 12, ORANGE, 2, 8)
    c.text(midx + 20, midy + 12, "tangent", ORANGE, 1)
    c.text(340, 310, "intrinsic + extrinsic curvature K", GRAY, 1)

    # ---- (c) Brane in a higher-dimensional bulk ----
    c.text(600, 45, "(c) Brane-world", BLACK, 1)
    # bulk box (5D)
    c.rect(600, 70, 800, 340, PURPLE, LIGHT_PURPLE)
    c.text(610, 78, "bulk (5D)", PURPLE, 1)
    # extra-dimension arrow
    c.arrow(620, 320, 620, 100, GRAY, 2, 8)
    c.text(626, 110, "extra dim y", GRAY, 1)
    # the brane (4D) as a highlighted plane
    c.fill_rect(650, 195, 795, 215, LIGHT_ORANGE)
    c.rect(650, 195, 795, 215, ORANGE)
    c.text(658, 199, "brane (4D universe)", BLACK, 1)
    c.text(650, 250, "our observable", RED, 1)
    c.text(650, 264, "universe on brane", RED, 1)

    c.text(30, 470, "Figure 4: Vielbein frame on a worldline, an embedded hypersurface with its "
                    "normal, and a 4D brane in a 5D bulk", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Advanced_Tools.png'))
    print("  Figure_4_Advanced_Tools.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating differential-geometry chapter figures...")
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
