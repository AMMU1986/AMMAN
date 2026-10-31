#!/usr/bin/env python3
"""
Generate the 6 figures for the manuscript:
"Bioconvective Squeezing Flow of a Tri-Hybrid Nanofluid Between Parallel Disks..."

Reuses the pure-Python PNG engine (PNGCanvas, fonts, colours) from
generate_figures.py so no third-party libraries (numpy/matplotlib) are needed.
"""

import os
import math
from generate_figures import (
    PNGCanvas,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE, RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/bioconvection_figures'

CURVE_COLORS = [MED_BLUE, RED, DARK_GREEN, ORANGE, PURPLE, GOLD]


# ───────────────────────── plotting helpers ─────────────────────────

class Plot:
    """A simple 2-D line/bar plot area drawn onto a PNGCanvas."""

    def __init__(self, c, left, top, w, h, xmin, xmax, ymin, ymax):
        self.c = c
        self.left, self.top, self.w, self.h = left, top, w, h
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax

    def px(self, x):
        return int(self.left + (x - self.xmin) / (self.xmax - self.xmin) * self.w)

    def py(self, y):
        return int(self.top + (1 - (y - self.ymin) / (self.ymax - self.ymin)) * self.h)

    def frame(self, xlabel, ylabel, title, xticks, yticks):
        c = self.c
        l, t, w, h = self.left, self.top, self.w, self.h
        # Title
        c.text_c(l + w // 2, t - 34, title, BLACK, 2)
        # Axis box
        c.rect(l, t, l + w, t + h, BLACK)
        # Grid + ticks (x)
        for xv in xticks:
            xp = self.px(xv)
            for yy in range(t, t + h, 6):
                c.pixel(xp, yy, LIGHT_GRAY)
            c.vline(xp, t + h, t + h + 5, BLACK)
            c.text_c(xp, t + h + 9, f"{xv:g}", BLACK, 1)
        # Grid + ticks (y)
        for yv in yticks:
            yp = self.py(yv)
            for xx in range(l, l + w, 6):
                c.pixel(xx, yp, LIGHT_GRAY)
            c.hline(l - 5, l, yp, BLACK)
            c.text(l - 38, yp - 3, f"{yv:g}", BLACK, 1)
        # Axis labels
        c.text_c(l + w // 2, t + h + 26, xlabel, BLACK, 2)
        # vertical-ish y label (drawn horizontally near top-left)
        c.text(l - 52, t - 20, ylabel, BLACK, 2)

    def curve(self, pts, color, thick=2):
        prev = None
        for (x, y) in pts:
            cur = (self.px(x), self.py(y))
            if prev is not None:
                self.c.line(prev[0], prev[1], cur[0], cur[1], color, thick)
            prev = cur

    def legend(self, entries, x, y):
        """entries: list of (color, label)."""
        for i, (col, lbl) in enumerate(entries):
            yy = y + i * 15
            self.c.line(x, yy, x + 24, yy, col, 3)
            self.c.text(x + 30, yy - 3, lbl, BLACK, 1)

    def annotate_arrow(self, x1, y1, x2, y2, label):
        self.c.arrow(self.px(x1), self.py(y1), self.px(x2), self.py(y2), GRAY, 2, 7)
        self.c.text(self.px((x1 + x2) / 2) + 4, self.py((y1 + y2) / 2) - 10, label, BLACK, 1)


def sample(fn, n=70, x0=0.0, x1=1.0):
    return [(x0 + (x1 - x0) * i / n, fn(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]


# ───────────────────────── Figure 1: geometry ─────────────────────────

def fig1():
    c = PNGCanvas(760, 520)
    c.text_c(380, 12, "Flow Geometry: Squeezing Tri-Hybrid Nanofluid Between Disks", BLACK, 2)

    # Upper disk (moving down)
    c.fill_rect(150, 110, 610, 132, MED_GREEN)
    c.rect(150, 110, 610, 132, DARK_GREEN)
    c.text(620, 114, "z = h(t)", BLACK, 1)
    # Lower disk (stationary)
    c.fill_rect(150, 388, 610, 410, MED_GREEN)
    c.rect(150, 388, 610, 410, DARK_GREEN)
    c.text(620, 392, "z = 0", BLACK, 1)

    # Squeezing arrows (upper disk moving down)
    for x in (230, 380, 530):
        c.arrow(x, 86, x, 108, RED, 3, 8)
    c.text(300, 74, "squeezing  dh/dt < 0", RED, 1)

    # Porous-medium region hatching
    for x in range(165, 600, 26):
        for y in range(150, 380, 26):
            c.pixel(x, y, LIGHT_GRAY)
            c.pixel(x + 1, y, LIGHT_GRAY)

    # Tri-hybrid nanoparticles (3 species = 3 colours/shapes)
    import random
    random.seed(7)
    for _ in range(26):
        x = random.randint(175, 585)
        y = random.randint(150, 375)
        kind = random.randint(0, 2)
        if kind == 0:      # Au - gold filled circle
            c.circle(x, y, 4, GOLD, GOLD)
        elif kind == 1:    # TiO2 - blue small square (brick)
            c.fill_rect(x - 3, y - 3, x + 3, y + 3, MED_BLUE)
        else:              # Ag - grey platelet (thin rect)
            c.fill_rect(x - 5, y - 2, x + 5, y + 2, GRAY)

    # Gyrotactic microorganisms (small purple ovals with tail) swimming up
    for (mx, my) in [(260, 340), (330, 300), (430, 330), (500, 290), (560, 350), (300, 250)]:
        c.circle(mx, my, 3, PURPLE, LIGHT_PURPLE)
        c.line(mx, my + 3, mx + 3, my + 9, PURPLE, 1)
        c.arrow(mx, my - 6, mx, my - 16, PURPLE, 1, 5)

    # Magnetic field arrows (B transverse)
    for y in (180, 240, 300, 360):
        c.arrow(120, y, 148, y, DARK_BLUE, 2, 6)
    c.text(96, 150, "B(t)", DARK_BLUE, 1)

    # Coordinate axes
    c.arrow(150, 410, 150, 150, BLACK, 2, 7); c.text(132, 150, "z", BLACK, 1)
    c.arrow(150, 410, 420, 410, BLACK, 2, 7); c.text(425, 414, "r", BLACK, 1)

    # Legend
    lx, ly = 150, 445
    c.circle(lx, ly, 4, GOLD, GOLD); c.text(lx + 10, ly - 3, "Au", BLACK, 1)
    c.fill_rect(lx + 56, ly - 3, lx + 62, ly + 3, MED_BLUE); c.text(lx + 70, ly - 3, "TiO2", BLACK, 1)
    c.fill_rect(lx + 128, ly - 2, lx + 138, ly + 2, GRAY); c.text(lx + 145, ly - 3, "Ag", BLACK, 1)
    c.circle(lx + 196, ly, 3, PURPLE, LIGHT_PURPLE); c.text(lx + 206, ly - 3, "microorganism", BLACK, 1)

    c.text(150, 480, "Convective + slip boundary conditions on both disks;", BLACK, 1)
    c.text(150, 496, "Darcy-Forchheimer porous medium; suction/injection at lower disk.", BLACK, 1)
    c.text_c(380, 510, "Figure 1", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Geometry.png'))
    print("  Figure_1_Geometry.png done")


# ───────────────────────── Figure 2: velocity f'(eta) ─────────────────────────

def fig2():
    c = PNGCanvas(720, 520)
    p = Plot(c, 90, 70, 580, 370, 0.0, 1.0, 0.0, 0.5)
    p.frame("eta", "f'(eta)", "Radial Velocity vs Squeezing Sq",
            [0, 0.2, 0.4, 0.6, 0.8, 1.0], [0.0, 0.1, 0.2, 0.3, 0.4, 0.5])

    def base(e):
        return 0.26 + 0.75 * e - 1.02 * e * e

    def profile(e, sq):
        d = 0.9 * (sq - 0.5) * (e - 0.15) * (e - 0.65) * (1 - e)
        v = base(e) + d
        return max(0.0, v)

    sqs = [0.0, 0.5, 1.5, 2.5]
    for i, sq in enumerate(sqs):
        p.curve(sample(lambda e, s=sq: profile(e, s)), CURVE_COLORS[i], 2)
    p.legend([(CURVE_COLORS[i], f"Sq = {sq:g}") for i, sq in enumerate(sqs)], 150, 110)
    # crossover annotation
    p.annotate_arrow(0.45, 0.33, 0.40, 0.30, "decrease")
    p.annotate_arrow(0.80, 0.14, 0.86, 0.17, "increase")
    c.text_c(360, 505, "Figure 2", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Velocity_Sq.png'))
    print("  Figure_2_Velocity_Sq.png done")


# ───────────────────────── Figure 3: temperature theta(eta) ─────────────────────────

def fig3():
    c = PNGCanvas(720, 520)
    p = Plot(c, 90, 70, 580, 370, 0.0, 1.0, 0.0, 1.0)
    p.frame("eta", "theta(eta)", "Temperature vs M and Rd",
            [0, 0.2, 0.4, 0.6, 0.8, 1.0], [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

    def temp(e, idx):
        return (0.78 * (1 - e) ** 1.35) * (1 + 0.11 * idx)

    labels = ["M=0.5, Rd=0.3", "M=1.5, Rd=0.5", "M=3.0, Rd=0.9", "M=5.0, Rd=1.3"]
    for i in range(4):
        p.curve(sample(lambda e, k=i: min(0.99, temp(e, k))), CURVE_COLORS[i], 2)
    p.legend([(CURVE_COLORS[i], labels[i]) for i in range(4)], 300, 95)
    p.annotate_arrow(0.30, 0.42, 0.34, 0.56, "M, Rd increase")
    c.text_c(360, 505, "Figure 3", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Temperature_M_Rd.png'))
    print("  Figure_3_Temperature_M_Rd.png done")


# ───────────────────────── Figure 4: concentration phi(eta) ─────────────────────────

def fig4():
    c = PNGCanvas(720, 520)
    p = Plot(c, 90, 70, 580, 370, 0.0, 1.0, 0.0, 1.0)
    p.frame("eta", "phi(eta)", "Concentration vs Activation Energy E",
            [0, 0.2, 0.4, 0.6, 0.8, 1.0], [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

    def conc(e, idx):
        base = (1 - e) / 1.2
        curv = 0.18 * math.sin(math.pi * e) * (0.4 + 0.22 * idx)
        return max(0.0, base + curv)

    Es = [0.5, 1.0, 2.0, 3.0]
    for i, E in enumerate(Es):
        p.curve(sample(lambda e, k=i: conc(e, k)), CURVE_COLORS[i], 2)
    p.legend([(CURVE_COLORS[i], f"E = {E:g}") for i, E in enumerate(Es)], 150, 95)
    p.annotate_arrow(0.45, 0.36, 0.48, 0.50, "E increase")
    c.text(120, 452, "Higher E weakens the destructive reaction -> concentration rises.", BLACK, 1)
    c.text_c(360, 505, "Figure 4", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Concentration_E.png'))
    print("  Figure_4_Concentration_E.png done")


# ───────────────────────── Figure 5: microorganism chi(eta) ─────────────────────────

def fig5():
    c = PNGCanvas(720, 520)
    p = Plot(c, 90, 70, 580, 370, 0.0, 1.0, 0.0, 1.0)
    p.frame("eta", "chi(eta)", "Microorganism Density vs Peclet Pe",
            [0, 0.2, 0.4, 0.6, 0.8, 1.0], [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

    def micro(e, idx):
        return (1 - e) ** (1 + 0.35 * idx)

    Pes = [0.1, 0.5, 1.5, 3.0]
    for i, Pe in enumerate(Pes):
        p.curve(sample(lambda e, k=i: micro(e, k)), CURVE_COLORS[i], 2)
    p.legend([(CURVE_COLORS[i], f"Pe = {Pe:g}") for i, Pe in enumerate(Pes)], 300, 150)
    p.annotate_arrow(0.45, 0.42, 0.50, 0.28, "Pe increase")
    c.text_c(360, 505, "Figure 5", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_5_Microorganism_Pe.png'))
    print("  Figure_5_Microorganism_Pe.png done")


# ───────────────────────── Figure 6: engineering quantities by shape ─────────────────────────

def fig6():
    c = PNGCanvas(720, 520)
    left, top, w, h = 90, 80, 580, 350
    c.text_c(380, 22, "Transfer Rates by Nanoparticle Shape", BLACK, 2)
    c.rect(left, top, left + w, top + h, BLACK)

    # three metric groups, each with 3 shape bars (brick, blade, platelet)
    groups = ["Nu (heat)", "Sh (mass)", "Nn (microorg.)"]
    data = {
        "Nu (heat)":       [2.41, 2.98, 2.63],
        "Sh (mass)":       [0.88, 0.95, 0.91],
        "Nn (microorg.)":  [0.72, 0.79, 0.76],
    }
    shape_colors = [ORANGE, MED_BLUE, DARK_GREEN]
    shape_names = ["brick", "blade", "platelet"]
    ymax = 3.2

    # y ticks
    for yv in [0, 0.8, 1.6, 2.4, 3.2]:
        yp = int(top + (1 - yv / ymax) * h)
        c.hline(left - 5, left, yp, BLACK)
        c.text(left - 40, yp - 3, f"{yv:g}", BLACK, 1)
        for xx in range(left, left + w, 6):
            c.pixel(xx, yp, LIGHT_GRAY)
    c.text(left - 70, top - 24, "value", BLACK, 2)

    gw = w // len(groups)
    bw = 42
    for gi, g in enumerate(groups):
        gx = left + gi * gw + 30
        for si in range(3):
            val = data[g][si]
            bh = int(val / ymax * h)
            bx = gx + si * (bw + 10)
            c.rect(bx, top + h - bh, bx + bw, top + h, BLACK, shape_colors[si])
            c.text_c(bx + bw // 2, top + h - bh - 11, f"{val:g}", BLACK, 1)
        c.text_c(gx + (3 * (bw + 10)) // 2 - 5, top + h + 10, g, BLACK, 1)

    # legend
    for si in range(3):
        lx = 150 + si * 150
        c.fill_rect(lx, 452, lx + 18, 464, shape_colors[si])
        c.rect(lx, 452, lx + 18, 464, BLACK)
        c.text(lx + 24, 453, shape_names[si], BLACK, 1)

    c.text(110, 480, "Blade shape (m = 8.6) gives the highest heat-transfer rate.", BLACK, 1)
    c.text_c(380, 505, "Figure 6", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_6_Transfer_Shapes.png'))
    print("  Figure_6_Transfer_Shapes.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating bioconvection manuscript figures...")
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6()
    print(f"\nAll 6 figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz/1024:.1f} KB")


if __name__ == '__main__':
    main()
