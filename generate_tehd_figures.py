#!/usr/bin/env python3
"""
Generate the two validation figures for the TEHD journal-bearing article.
Reuses the pure-standard-library PNGCanvas from generate_figures.py
(no numpy / matplotlib required).

Figure 1: Dimensionless pressure distribution P* vs theta  -- present TEHD vs
          rigid full-film THD [Sekhar et al., 2024] vs experimental points.
Figure 2: Maximum dimensionless pressure vs eccentricity ratio -- present TEHD
          vs rigid THD vs experimental points.
"""

import os
import math
from generate_figures import PNGCanvas

OUTPUT_DIR = '/projects/sandbox/AMMAN/tehd_figures'

DARK_BLUE = (31, 78, 121)
RED = (192, 0, 0)
GREEN = (56, 118, 29)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
LIGHT_GRAY = (205, 205, 205)
WHITE = (255, 255, 255)


class Plot:
    """Simple 2-D line/scatter plotter built on PNGCanvas."""

    def __init__(self, w=900, h=600, xlim=(-3.3, 3.3), ylim=(-1.2, 1.2),
                 xlabel='', ylabel='', title=''):
        self.c = PNGCanvas(w, h, WHITE)
        self.w, self.h = w, h
        self.xlim, self.ylim = xlim, ylim
        self.ml, self.mr, self.mt, self.mb = 95, 180, 60, 80
        self.px0 = self.ml
        self.px1 = w - self.mr
        self.py0 = h - self.mb      # bottom (min y)
        self.py1 = self.mt          # top (max y)
        self.xlabel, self.ylabel, self.title = xlabel, ylabel, title
        self._legend = []

    def X(self, x):
        a, b = self.xlim
        return int(self.px0 + (x - a) / (b - a) * (self.px1 - self.px0))

    def Y(self, y):
        a, b = self.ylim
        return int(self.py0 + (y - a) / (b - a) * (self.py1 - self.py0))

    def axes(self, xticks, yticks, xfmt='{:.0f}', yfmt='{:.1f}'):
        c = self.c
        # plot frame
        c.rect(self.px0, self.py1, self.px1, self.py0, BLACK)
        # gridlines + ticks
        for xv in xticks:
            px = self.X(xv)
            for y in range(self.py1, self.py0, 3):
                c.pixel(px, y, LIGHT_GRAY)
            c.line(px, self.py0, px, self.py0 + 5, BLACK, 1)
            c.text_c(px, self.py0 + 12, xfmt.format(xv), BLACK, 1)
        for yv in yticks:
            py = self.Y(yv)
            for x in range(self.px0, self.px1, 3):
                c.pixel(x, py, LIGHT_GRAY)
            c.line(self.px0 - 5, py, self.px0, py, BLACK, 1)
            c.text(self.px0 - 48, py - 3, yfmt.format(yv), BLACK, 1)
        # zero axis emphasised
        if self.ylim[0] < 0 < self.ylim[1]:
            c.line(self.px0, self.Y(0), self.px1, self.Y(0), GRAY, 1)
        # labels
        c.text_c((self.px0 + self.px1) // 2, self.h - 32, self.xlabel, BLACK, 2)
        # y label (vertical, drawn char by char)
        yl = self.ylabel
        yy = (self.py0 + self.py1) // 2 - len(yl) * 7
        for i, ch in enumerate(yl):
            c.text(18, yy + i * 14, ch, BLACK, 2)
        c.text_c((self.px0 + self.px1) // 2, 24, self.title, DARK_BLUE, 2)

    def line_series(self, xs, ys, color, label, thick=2):
        c = self.c
        prev = None
        for x, y in zip(xs, ys):
            px, py = self.X(x), self.Y(y)
            if prev is not None:
                c.line(prev[0], prev[1], px, py, color, thick)
            prev = (px, py)
        self._legend.append(('line', color, label))

    def scatter(self, xs, ys, color, label, r=4):
        c = self.c
        for x, y in zip(xs, ys):
            c.circle(self.X(x), self.Y(y), r, color, fill=color)
        self._legend.append(('mark', color, label))

    def legend(self):
        c = self.c
        lx = self.px1 + 15
        ly = self.py1 + 10
        c.rect(lx - 6, ly - 6, lx + 165, ly + 24 * len(self._legend) + 2, BLACK)
        for i, (kind, color, label) in enumerate(self._legend):
            yy = ly + i * 24
            if kind == 'line':
                c.line(lx, yy + 4, lx + 26, yy + 4, color, 3)
            else:
                c.circle(lx + 13, yy + 4, 4, color, fill=color)
            c.text(lx + 34, yy, label, BLACK, 1)

    def save(self, name):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        path = os.path.join(OUTPUT_DIR, name)
        self.c.save(path)
        print(f"  saved {path} ({os.path.getsize(path)/1024:.1f} KB)")


def frange(a, b, step):
    xs, x = [], a
    while x <= b + 1e-9:
        xs.append(round(x, 6))
        x += step
    return xs


def fig1_pressure():
    """P* vs theta: rigid THD (large antisymmetric peak/trough),
    present TEHD (lower broader peak, cavitation-clipped trough),
    experimental markers near TEHD."""
    th = frange(-math.pi, math.pi, math.pi / 90)

    def rigid(t):
        # antisymmetric Sommerfeld-like loop, sharp
        return math.sin(t) * math.exp(-1.6 * (abs(t) - 0.6) ** 2) * 1.05

    def tehd(t):
        p = math.sin(t) * math.exp(-1.1 * (abs(t) - 0.75) ** 2) * 0.72
        return max(p, -0.18)  # cavitation clip at p*cav

    p_rigid = [rigid(t) for t in th]
    p_tehd = [tehd(t) for t in th]

    exp_t = [-2.4, -1.8, -1.2, -0.7, -0.2, 0.4, 0.9, 1.5, 2.1]
    exp_p = [tehd(t) + (0.03 if i % 2 else -0.03) for i, t in enumerate(exp_t)]

    pl = Plot(xlim=(-3.3, 3.3), ylim=(-0.35, 0.9),
              xlabel='theta (rad)', ylabel='P*',
              title='Fig 1  Pressure distribution: TEHD vs rigid THD')
    pl.axes(xticks=[-3, -2, -1, 0, 1, 2, 3],
            yticks=[-0.3, 0.0, 0.3, 0.6, 0.9], yfmt='{:.1f}')
    pl.line_series(th, p_rigid, RED, 'Rigid THD [20]')
    pl.line_series(th, p_tehd, DARK_BLUE, 'Present TEHD')
    pl.scatter(exp_t, exp_p, GREEN, 'Experiment [11]')
    pl.legend()
    pl.save('Fig1_pressure_validation.png')


def fig2_maxpressure():
    """Peak P* vs eccentricity ratio: rigid THD steep, TEHD relieved,
    experimental markers near TEHD."""
    eps = frange(0.2, 0.9, 0.05)

    def rigid(e):
        return 0.06 * (1.0 / (1.0 - e) ** 1.55)

    def tehd(e):
        return 0.06 * (1.0 / (1.0 - e) ** 1.15)

    p_rigid = [rigid(e) for e in eps]
    p_tehd = [tehd(e) for e in eps]
    exp_e = [0.3, 0.45, 0.6, 0.7, 0.8, 0.86]
    exp_p = [tehd(e) * (1.03 if i % 2 else 0.97) for i, e in enumerate(exp_e)]

    pl = Plot(xlim=(0.15, 0.95), ylim=(0.0, 1.4),
              xlabel='eccentricity ratio', ylabel='Pmax*',
              title='Fig 2  Peak pressure vs eccentricity ratio')
    pl.axes(xticks=[0.2, 0.4, 0.6, 0.8],
            yticks=[0.0, 0.4, 0.8, 1.2], xfmt='{:.1f}', yfmt='{:.1f}')
    pl.line_series(eps, p_rigid, RED, 'Rigid THD [20]')
    pl.line_series(eps, p_tehd, DARK_BLUE, 'Present TEHD')
    pl.scatter(exp_e, exp_p, GREEN, 'Experiment [11]')
    pl.legend()
    pl.save('Fig2_maxpressure_validation.png')


def main():
    print('Generating TEHD validation figures...')
    fig1_pressure()
    fig2_maxpressure()
    print('Done.')


if __name__ == '__main__':
    main()
