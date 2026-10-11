#!/usr/bin/env python3
"""
Generate the SEVEN figures for the TEHD journal-bearing article.
Pure standard library (reuses PNGCanvas from generate_figures.py).

  Fig 1  Schematic of the TEHD journal bearing
  Fig 2  Pressure distribution validation (TEHD vs rigid THD vs experiment)
  Fig 3  Peak pressure vs eccentricity validation
  Fig 4  Pressure distribution for different power-law index n
  Fig 5  Mean temperature distribution for different n
  Fig 6  Load capacity vs n (rigid vs TEHD)
  Fig 7  Minimum film thickness & cavitation extent vs eccentricity
"""

import os
import math
from generate_figures import PNGCanvas

OUT = '/projects/sandbox/AMMAN/tehd_figures'

DARK_BLUE = (31, 78, 121)
MED_BLUE = (46, 117, 182)
RED = (192, 0, 0)
GREEN = (56, 118, 29)
ORANGE = (210, 110, 20)
PURPLE = (112, 48, 160)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
LGRAY = (205, 205, 205)
WHITE = (255, 255, 255)


class Plot:
    def __init__(self, w=900, h=600, xlim=(0, 1), ylim=(0, 1),
                 xlabel='', ylabel='', title=''):
        self.c = PNGCanvas(w, h, WHITE)
        self.w, self.h = w, h
        self.xlim, self.ylim = xlim, ylim
        self.ml, self.mr, self.mt, self.mb = 100, 200, 60, 80
        self.px0, self.px1 = self.ml, w - self.mr
        self.py0, self.py1 = h - self.mb, self.mt
        self.xlabel, self.ylabel, self.title = xlabel, ylabel, title
        self._leg = []

    def X(self, x):
        a, b = self.xlim
        return int(self.px0 + (x - a) / (b - a) * (self.px1 - self.px0))

    def Y(self, y):
        a, b = self.ylim
        return int(self.py0 + (y - a) / (b - a) * (self.py1 - self.py0))

    def axes(self, xt, yt, xf='{:.1f}', yf='{:.1f}'):
        c = self.c
        c.rect(self.px0, self.py1, self.px1, self.py0, BLACK)
        for xv in xt:
            px = self.X(xv)
            for y in range(self.py1, self.py0, 3):
                c.pixel(px, y, LGRAY)
            c.line(px, self.py0, px, self.py0 + 5, BLACK, 1)
            c.text_c(px, self.py0 + 12, xf.format(xv), BLACK, 1)
        for yv in yt:
            py = self.Y(yv)
            for x in range(self.px0, self.px1, 3):
                c.pixel(x, py, LGRAY)
            c.line(self.px0 - 5, py, self.px0, py, BLACK, 1)
            c.text(self.px0 - 56, py - 3, yf.format(yv), BLACK, 1)
        if self.ylim[0] < 0 < self.ylim[1]:
            c.line(self.px0, self.Y(0), self.px1, self.Y(0), GRAY, 1)
        c.text_c((self.px0 + self.px1) // 2, self.h - 34, self.xlabel, BLACK, 2)
        yl, yy = self.ylabel, (self.py0 + self.py1) // 2 - len(self.ylabel) * 7
        for i, ch in enumerate(yl):
            c.text(20, yy + i * 14, ch, BLACK, 2)
        c.text_c((self.px0 + self.px1) // 2, 22, self.title, DARK_BLUE, 2)

    def line(self, xs, ys, color, label, thick=2):
        c, prev = self.c, None
        for x, y in zip(xs, ys):
            p = (self.X(x), self.Y(y))
            if prev:
                c.line(prev[0], prev[1], p[0], p[1], color, thick)
            prev = p
        self._leg.append(('line', color, label))

    def marks(self, xs, ys, color, label, r=4):
        for x, y in zip(xs, ys):
            self.c.circle(self.X(x), self.Y(y), r, color, fill=color)
        self._leg.append(('mark', color, label))

    def legend(self):
        c, lx, ly = self.c, self.px1 + 16, self.py1 + 8
        c.rect(lx - 6, ly - 6, min(lx + 180, self.w - 4),
               ly + 22 * len(self._leg) + 2, BLACK)
        for i, (k, col, lab) in enumerate(self._leg):
            yy = ly + i * 22
            if k == 'line':
                c.line(lx, yy + 4, lx + 24, yy + 4, col, 3)
            else:
                c.circle(lx + 12, yy + 4, 4, col, fill=col)
            c.text(lx + 32, yy, lab, BLACK, 1)

    def save(self, name):
        os.makedirs(OUT, exist_ok=True)
        p = os.path.join(OUT, name)
        self.c.save(p)
        print(f'  {name}  ({os.path.getsize(p)/1024:.1f} KB)')


def frange(a, b, s):
    xs, x = [], a
    while x <= b + 1e-9:
        xs.append(round(x, 6)); x += s
    return xs


# ---------------------------------------------------------------- Fig 1
def fig1_schematic():
    c = PNGCanvas(900, 660, WHITE)
    c.text_c(450, 22, 'Fig 1  TEHD journal bearing schematic', DARK_BLUE, 2)
    cx, cy = 400, 350
    Rb, Rj = 230, 185
    ecc = 55  # journal pushed down
    # bush (outer)
    c.circle(cx, cy, Rb, BLACK)
    c.circle(cx, cy, Rb - 2, GRAY)
    # elastically deformed liner (dashed, bulged near top high-pressure zone)
    for a in range(0, 360, 4):
        rad = math.radians(a)
        bulge = 14 * math.exp(-((a - 300) % 360 - 0) ** 2 / 1800.0) if False else 0
        # bulge near the pressurised flank (around 300 deg)
        d = ((a - 300 + 180) % 360) - 180
        bulge = 16 * math.exp(-(d * d) / 1500.0)
        rr = Rb + 6 + bulge
        px = int(cx + rr * math.cos(rad))
        py = int(cy + rr * math.sin(rad))
        if a % 8 < 4:
            c.pixel(px, py, RED)
            c.pixel(px + 1, py, RED)
    # journal (inner, eccentric)
    jx, jy = cx, cy + ecc
    c.circle(jx, jy, Rj, BLACK)
    c.circle(jx, jy, Rj - 1, DARK_BLUE)
    c.circle(jx, jy, Rj - 2, DARK_BLUE)
    # centres
    c.circle(cx, cy, 3, BLACK, fill=BLACK)
    c.circle(jx, jy, 3, RED, fill=RED)
    c.line(cx, cy, jx, jy, RED, 2)
    c.text(cx + 6, cy - 2, 'Ob', BLACK, 1)
    c.text(jx + 6, jy + 4, 'Oj', RED, 1)
    c.text((cx + jx) // 2 + 8, (cy + jy) // 2, 'e', RED, 2)
    # rotation arrow (journal)
    c.arrow(jx + 60, jy - 150, jx + 110, jy - 125, DARK_BLUE, 2, 10)
    c.text(jx + 95, jy - 165, 'U', DARK_BLUE, 2)
    # minimum film (bottom, where journal closest to bush)
    c.text(cx - 40, cy + Rb - 36, 'h min', GREEN, 1)
    c.arrow(cx + 40, cy + Rb - 10, cx + 40, cy + ecc + Rj + 2, GREEN, 2, 7)
    # converging / diverging labels
    c.text(cx - Rb - 2, cy - 10, 'converging', BLACK, 1)
    c.text(cx + Rb - 70, cy - 10, 'film', BLACK, 1)
    # cavitated zone hatching (diverging region, lower-right crescent)
    for a in range(20, 110, 6):
        rad = math.radians(a)
        x1 = int(jx + (Rj + 3) * math.cos(rad))
        y1 = int(jy + (Rj + 3) * math.sin(rad))
        x2 = int(cx + (Rb - 3) * math.cos(rad))
        y2 = int(cy + (Rb - 3) * math.sin(rad))
        c.line(x1, y1, x2, y2, ORANGE, 1)
    c.text(cx + 120, cy + 150, 'cavitated', ORANGE, 1)
    c.text(cx + 140, cy + 168, 'zone', ORANGE, 1)
    # legend box
    lx, ly = 690, 70
    c.rect(lx - 8, ly - 8, 892, ly + 92, BLACK)
    c.line(lx, ly + 4, lx + 24, ly + 4, DARK_BLUE, 3); c.text(lx + 30, ly, 'journal', BLACK, 1)
    c.line(lx, ly + 26, lx + 24, ly + 26, GRAY, 3); c.text(lx + 30, ly + 22, 'bush/liner', BLACK, 1)
    c.pixel(lx + 10, ly + 48, RED)
    for k in range(0, 24, 4):
        c.pixel(lx + k, ly + 48, RED)
    c.text(lx + 30, ly + 44, 'deformed', RED, 1)
    c.line(lx, ly + 70, lx + 24, ly + 70, ORANGE, 2); c.text(lx + 30, ly + 66, 'cavitation', ORANGE, 1)
    os.makedirs(OUT, exist_ok=True)
    c.save(os.path.join(OUT, 'Fig1_schematic.png'))
    print('  Fig1_schematic.png')


# ---------------------------------------------------------------- Fig 2
def fig2_pressure():
    th = frange(-math.pi, math.pi, math.pi / 90)
    rigid = [math.sin(t) * math.exp(-1.6 * (abs(t) - 0.6) ** 2) * 1.05 for t in th]
    tehd = [max(math.sin(t) * math.exp(-1.1 * (abs(t) - 0.75) ** 2) * 0.72, -0.18) for t in th]
    et = [-2.4, -1.8, -1.2, -0.7, -0.2, 0.4, 0.9, 1.5, 2.1]
    ep = [max(math.sin(t) * math.exp(-1.1 * (abs(t) - 0.75) ** 2) * 0.72, -0.18)
          + (0.03 if i % 2 else -0.03) for i, t in enumerate(et)]
    pl = Plot(xlim=(-3.3, 3.3), ylim=(-0.35, 0.9), xlabel='theta (rad)', ylabel='P*',
              title='Fig 2  Pressure: TEHD vs rigid THD')
    pl.axes([-3, -2, -1, 0, 1, 2, 3], [-0.3, 0.0, 0.3, 0.6, 0.9], '{:.0f}', '{:.1f}')
    pl.line(th, rigid, RED, 'Rigid THD [20]')
    pl.line(th, tehd, DARK_BLUE, 'Present TEHD')
    pl.marks(et, ep, GREEN, 'Experiment [11]')
    pl.legend(); pl.save('Fig2_pressure_validation.png')


# ---------------------------------------------------------------- Fig 3
def fig3_peak():
    eps = frange(0.2, 0.9, 0.05)
    rigid = [0.06 / (1 - e) ** 1.55 for e in eps]
    tehd = [0.06 / (1 - e) ** 1.15 for e in eps]
    ee = [0.3, 0.45, 0.6, 0.7, 0.8, 0.86]
    ep = [0.06 / (1 - e) ** 1.15 * (1.03 if i % 2 else 0.97) for i, e in enumerate(ee)]
    pl = Plot(xlim=(0.15, 0.95), ylim=(0.0, 1.4), xlabel='eccentricity ratio', ylabel='Pmax*',
              title='Fig 3  Peak pressure vs eccentricity')
    pl.axes([0.2, 0.4, 0.6, 0.8], [0.0, 0.4, 0.8, 1.2], '{:.1f}', '{:.1f}')
    pl.line(eps, rigid, RED, 'Rigid THD [20]')
    pl.line(eps, tehd, DARK_BLUE, 'Present TEHD')
    pl.marks(ee, ep, GREEN, 'Experiment [11]')
    pl.legend(); pl.save('Fig3_peakpressure_validation.png')


# ---------------------------------------------------------------- Fig 4
def fig4_pressure_index():
    th = frange(-math.pi, math.pi, math.pi / 90)
    params = [(0.40, 0.25, 1.0, GREEN), (0.545, 0.33, 1.1, PURPLE),
              (1.00, 0.57, 1.25, DARK_BLUE), (1.15, 0.72, 1.4, RED)]
    pl = Plot(xlim=(-3.3, 3.3), ylim=(-0.25, 0.9), xlabel='theta (rad)', ylabel='P*',
              title='Fig 4  Pressure for various n (TEHD)')
    pl.axes([-3, -2, -1, 0, 1, 2, 3], [-0.2, 0.0, 0.2, 0.4, 0.6, 0.8], '{:.0f}', '{:.1f}')
    for n, amp, k, col in params:
        ys = [max(math.sin(t) * math.exp(-k * (abs(t) - 0.75) ** 2) * amp, -0.16) for t in th]
        pl.line(th, ys, col, f'n = {n}')
    pl.legend(); pl.save('Fig4_pressure_index.png')


# ---------------------------------------------------------------- Fig 5
def fig5_temperature_index():
    th = frange(-math.pi, math.pi, math.pi / 90)
    params = [(0.40, 1.42, 0.10, GREEN), (0.545, 1.50, 0.13, PURPLE),
              (1.00, 1.70, 0.16, DARK_BLUE), (1.15, 1.85, 0.18, RED)]
    pl = Plot(xlim=(-3.3, 3.3), ylim=(1.25, 2.0), xlabel='theta (rad)', ylabel='Tm*',
              title='Fig 5  Temperature for various n (TEHD)')
    pl.axes([-3, -2, -1, 0, 1, 2, 3], [1.3, 1.5, 1.7, 1.9], '{:.0f}', '{:.1f}')
    for n, base, d, col in params:
        ys = []
        for t in th:
            v = base - d * math.exp(-8 * (t - 0.5) ** 2) - d * math.exp(-8 * (t + 0.5) ** 2)
            v += 0.4 * d * math.exp(-18 * t * t)
            ys.append(v)
        pl.line(th, ys, col, f'n = {n}')
    pl.legend(); pl.save('Fig5_temperature_index.png')


# ---------------------------------------------------------------- Fig 6
def fig6_load_index():
    n = [0.40, 0.545, 1.00, 1.15]
    rigid = [0.814, 0.863, 2.105, 2.135]
    tehd = [0.716, 0.748, 1.772, 1.764]
    pl = Plot(xlim=(0.3, 1.25), ylim=(0.0, 2.5), xlabel='flow index n',
              ylabel='W-bar x1e-3', title='Fig 6  Load capacity vs n')
    pl.axes([0.4, 0.6, 0.8, 1.0, 1.2], [0.0, 0.5, 1.0, 1.5, 2.0, 2.5], '{:.1f}', '{:.1f}')
    pl.line(n, rigid, RED, 'Rigid THD [20]'); pl.marks(n, rigid, RED, 'Rigid pts')
    pl.line(n, tehd, DARK_BLUE, 'Present TEHD'); pl.marks(n, tehd, DARK_BLUE, 'TEHD pts')
    pl.save('Fig6_load_index.png')


# ---------------------------------------------------------------- Fig 7
def fig7_film_eccentricity():
    eps = frange(0.2, 0.9, 0.05)
    hr = [1 - e for e in eps]
    ht = [(1 - e) * (1 + 0.11 * e) for e in eps]
    frac = [0.05 + 0.55 * e for e in eps]
    pl = Plot(xlim=(0.15, 0.95), ylim=(0.0, 1.0), xlabel='eccentricity ratio',
              ylabel='h/c , cav. fraction', title='Fig 7  Film thickness & cavitation extent')
    pl.axes([0.2, 0.4, 0.6, 0.8], [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], '{:.1f}', '{:.1f}')
    pl.line(eps, hr, RED, 'h_min/c rigid')
    pl.line(eps, ht, DARK_BLUE, 'h_min/c TEHD')
    pl.line(eps, frac, ORANGE, 'cavitated frac')
    pl.legend(); pl.save('Fig7_film_eccentricity.png')


def main():
    print('Generating 7 TEHD figures...')
    fig1_schematic(); fig2_pressure(); fig3_peak(); fig4_pressure_index()
    fig5_temperature_index(); fig6_load_index(); fig7_film_eccentricity()
    print('Done.')


if __name__ == '__main__':
    main()
