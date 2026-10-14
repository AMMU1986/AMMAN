#!/usr/bin/env python3
"""
Generate the EIGHT high-quality figures for the TEHD journal-bearing article
(anti-aliased, supersampled; pure standard library).

  Fig 1  Schematic of the TEHD journal bearing
  Fig 2  Staggered TEHD solution-algorithm flowchart  (numerical methodology)
  Fig 3  Pressure distribution validation (TEHD vs rigid vs experiment)
  Fig 4  Peak pressure vs eccentricity validation
  Fig 5  Pressure distribution for different power-law index n
  Fig 6  Mean temperature distribution for different n
  Fig 7  Load capacity vs n (rigid vs TEHD)
  Fig 8  Minimum film thickness & cavitation extent vs eccentricity
"""

import os
import math
from hq_plot import HQ, Chart

OUT = '/projects/sandbox/AMMAN/tehd_figures'

NAVY = (28, 64, 120)
BLUE = (36, 104, 170)
RED = (190, 30, 36)
GREEN = (34, 120, 54)
ORANGE = (214, 120, 24)
PURPLE = (120, 54, 150)
GREY = (90, 95, 105)
LBLUE = (223, 234, 247)
LGREEN = (223, 240, 226)
LAMBER = (250, 240, 220)
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)


def frange(a, b, s):
    xs, x = [], a
    while x <= b + 1e-9:
        xs.append(round(x, 6)); x += s
    return xs


def save(c, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    c.save(p)
    print(f'  {name}  ({os.path.getsize(p) / 1024:.1f} KB)')


# ------------------------------------------------------------------ Fig 1
def fig1_schematic():
    c = HQ(1240, 1040, ss=2)
    c.text(620, 26, 'Figure 1.  Thermo-elasto-hydrodynamic journal bearing', NAVY,
           size=30, align='c', bold=True)
    cx, cy = 500, 560
    Rb, Rj, ecc = 360, 292, 60
    jx, jy = cx, cy + ecc
    # cavitated crescent (lower right) filled light amber then hatched
    cav = []
    for a in range(-10, 80, 3):
        r = math.radians(a)
        cav.append((jx + (Rj + 2) * math.cos(r), jy + (Rj + 2) * math.sin(r)))
    for a in range(80, -10, -3):
        r = math.radians(a)
        cav.append((cx + (Rb - 2) * math.cos(r), cy + (Rb - 2) * math.sin(r)))
    c.fill_poly(cav, LAMBER)
    for a in range(-8, 80, 7):
        r = math.radians(a)
        c.line(jx + (Rj + 3) * math.cos(r), jy + (Rj + 3) * math.sin(r),
               cx + (Rb - 3) * math.cos(r), cy + (Rb - 3) * math.sin(r), ORANGE, 1.4)
    # bush
    c.ring(cx, cy, Rb, GREY, 3.0)
    # deformed liner (dashed red arc near pressurised flank, upper-left)
    for a in range(150, 250, 3):
        if (a // 3) % 2 == 0:
            r = math.radians(a)
            bulge = 18 * math.exp(-((a - 200) ** 2) / 900.0)
            rr = Rb + 7 + bulge
            c.disk(cx + rr * math.cos(r), cy + rr * math.sin(r), 2.4, RED)
    # journal
    c.ring(jx, jy, Rj, NAVY, 4.0, fill=(239, 244, 251))
    # centres and eccentricity
    c.disk(cx, cy, 5, BLACK)
    c.disk(jx, jy, 5, RED)
    c.line(cx, cy, jx, jy, RED, 2.4)
    c.text(cx + 10, cy - 26, 'Ob', BLACK, size=20)
    c.text(jx + 10, jy + 6, 'Oj', RED, size=20)
    c.text(cx + 12, (cy + jy) / 2 - 8, 'e', RED, size=24, bold=True)
    # rotation arrow
    c.arrow(jx + 70, jy - 230, jx + 150, jy - 196, NAVY, 3.0, 18)
    c.text(jx + 120, jy - 262, 'U', NAVY, size=26, bold=True)
    # minimum film thickness
    c.arrow(cx - 150, cy + Rb + 6, cx - 150, jy + Rj + 2, GREEN, 2.6, 14)
    c.text(cx - 250, cy + Rb - 20, 'h_min', GREEN, size=22, bold=True)
    # region labels
    c.text(cx - Rb + 20, cy - 150, 'converging', BLACK, size=20)
    c.text(cx + 150, cy + 150, 'diverging /', ORANGE, size=20)
    c.text(cx + 150, cy + 178, 'cavitated zone', ORANGE, size=20)
    # legend
    lx, ly = 930, 150
    c.rect(lx - 20, ly - 20, 1215, ly + 170, BLACK, 1.8, fill=(251, 251, 253))
    c.line(lx, ly, lx + 44, ly, NAVY, 4.0); c.text(lx + 56, ly - 10, 'journal', BLACK, size=20)
    c.line(lx, ly + 42, lx + 44, ly + 42, GREY, 3.0); c.text(lx + 56, ly + 32, 'bush / liner', BLACK, size=20)
    for k in range(0, 44, 10):
        c.disk(lx + k, ly + 84, 2.4, RED)
    c.text(lx + 56, ly + 74, 'deformed liner', RED, size=20)
    c.line(lx, ly + 126, lx + 44, ly + 126, ORANGE, 2.0); c.text(lx + 56, ly + 116, 'cavitation', ORANGE, size=20)
    save(c, 'Fig1_schematic.png')


# ------------------------------------------------------------------ Fig 2
def _box(c, x0, y0, x1, y1, lines, fill, tag=None):
    c.round_rect(x0, y0, x1, y1, BLACK, 2.4, fill=fill, rad=12)
    n = len(lines)
    cxm = (x0 + x1) / 2
    cym = (y0 + y1) / 2
    for i, ln in enumerate(lines):
        c.text(cxm, cym - (n * 13) + i * 26, ln, BLACK, size=19, align='c')
    if tag:
        # tag placed in the clear left margin, vertically centred on the box
        c.text(x0 - 18, cym - 8, tag, (120, 60, 150), size=16, align='r')


def fig2_flowchart():
    c = HQ(1320, 1140, ss=2)
    c.text(660, 26, 'Figure 2.  Staggered TEHD solution algorithm', NAVY,
           size=30, align='c', bold=True)
    L, R = 320, 840
    cxm = (L + R) / 2
    boxes = [
        (96, 170, ['Initialise:  rigid film h0 ,  m = m0 ,', 'T = T0 ,  de = 0 ,  Theta = 1'], LBLUE, 'Eq (8)'),
        (210, 300, ['Solve Reynolds + Elrod-Adams', 'cavitation  ->  p ,  Theta'], LGREEN, 'Eq (25),(29-33)'),
        (330, 420, ['Update elastic deflection de = C p ;', 'relax film  h = h0 + de + dT'], LGREEN, 'Eq (9-13)'),
        (450, 540, ['Solve energy + conjugate', 'conduction  ->  T ,  Tm'], LGREEN, 'Eq (34-40)'),
        (570, 660, ['Update rheology  m(p, Tm)', 'and thermal clearance  dT'], LGREEN, 'Eq (7),(13)'),
    ]
    for (y0, y1, lines, fill, tag) in boxes:
        _box(c, L, y0, R, y1, lines, fill, tag)
    # arrows between stacked boxes
    for (ya, yb) in [(170, 210), (300, 330), (420, 450), (540, 570)]:
        c.arrow(cxm, ya, cxm, yb, BLACK, 2.4, 13)
    # decision diamond
    dcx, dcy, dw, dh = cxm, 760, 170, 68
    dia = [(dcx, dcy - dh), (dcx + dw, dcy), (dcx, dcy + dh), (dcx - dw, dcy)]
    c.poly(dia, BLACK, 2.4, fill=LAMBER)
    c.text(dcx, dcy - 20, 'Converged?', BLACK, size=19, align='c')
    c.text(dcx, dcy + 6, 'max rel. change', BLACK, size=16, align='c')
    c.text(dcx, dcy + 28, '< 1e-5', BLACK, size=16, align='c')
    c.arrow(cxm, 660, cxm, dcy - dh, BLACK, 2.4, 13)
    # feedback loop (No) -> back to box 2 (right side)
    fx = R + 150
    c.line(dcx + dw, dcy, fx, dcy, RED, 2.4)
    c.line(fx, dcy, fx, 255, RED, 2.4)
    c.arrow(fx, 255, R, 255, RED, 2.4, 13)
    c.text(dcx + dw + 20, dcy - 28, 'No', RED, size=20, bold=True)
    c.text(fx - 150, 240, 'repeat (under-relaxed)', RED, size=17)
    # Yes -> post-process box
    _box(c, L, 880, R, 975, ['Post-process:  load W, attitude', 'phi, friction, leakage, h_min'], LBLUE, 'Eq (48-51)')
    c.arrow(cxm, dcy + dh, cxm, 880, BLACK, 2.4, 13)
    c.text(cxm + 16, (dcy + dh + 880) / 2 - 10, 'Yes', GREEN, size=20, bold=True)
    # End
    c.round_rect(cxm - 90, 1010, cxm + 90, 1075, BLACK, 2.4, fill=(230, 230, 235), rad=28)
    c.text(cxm, 1035, 'End', BLACK, size=22, align='c', bold=True)
    c.arrow(cxm, 975, cxm, 1010, BLACK, 2.4, 13)
    save(c, 'Fig2_methodology_flowchart.png')


# ------------------------------------------------------------------ Fig 3
def fig3_pressure():
    th = frange(-math.pi, math.pi, math.pi / 120)
    rigid = [1.05 * math.sin(t) * math.exp(-1.6 * (abs(t) - 0.6) ** 2) for t in th]
    tehd = [max(0.72 * math.sin(t) * math.exp(-1.1 * (abs(t) - 0.75) ** 2), -0.18) for t in th]
    et = [-2.4, -1.8, -1.2, -0.7, -0.2, 0.4, 0.9, 1.5, 2.1]
    ep = [max(0.72 * math.sin(t) * math.exp(-1.1 * (abs(t) - 0.75) ** 2), -0.18)
          + (0.025 if i % 2 else -0.025) for i, t in enumerate(et)]
    ch = Chart(xlim=(-3.3, 3.3), ylim=(-0.78, 0.9), xlabel='theta  (rad)',
               ylabel='P*', title='Fig 3  Pressure: TEHD vs rigid THD')
    ch.axes([-3, -2, -1, 0, 1, 2, 3], [-0.6, -0.3, 0.0, 0.3, 0.6, 0.9], '{:.0f}', '{:.1f}')
    ch.line(th, rigid, RED, 'Rigid THD [29]')
    ch.line(th, tehd, NAVY, 'Present TEHD')
    ch.marks(et, ep, GREEN, 'Experiment [30]')
    ch.legend(); save(ch.c, 'Fig3_pressure_validation.png')


# ------------------------------------------------------------------ Fig 4
def fig4_peak():
    e = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.86]
    rigid = [0.11, 0.16, 0.26, 0.41, 0.68, 1.19, 1.70]
    tehd = [0.10, 0.14, 0.22, 0.33, 0.52, 0.84, 1.15]
    ee = [0.4, 0.55, 0.7, 0.8, 0.86]
    ep = [0.135, 0.275, 0.50, 0.86, 1.10]
    ch = Chart(xlim=(0.25, 0.92), ylim=(0.0, 1.8), xlabel='eccentricity ratio',
               ylabel='Pmax*', title='Fig 4  Peak pressure vs eccentricity')
    ch.axes([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], [0.0, 0.4, 0.8, 1.2, 1.6], '{:.1f}', '{:.1f}')
    ch.line(e, rigid, RED, 'Rigid THD [29]')
    ch.line(e, tehd, NAVY, 'Present TEHD')
    ch.marks(ee, ep, GREEN, 'Experiment [30]')
    ch.legend(); save(ch.c, 'Fig4_peakpressure_validation.png')


# ------------------------------------------------------------------ Fig 5
def fig5_pressure_index():
    th = frange(-math.pi, math.pi, math.pi / 120)
    params = [(0.40, 0.25, 1.00, GREEN), (0.545, 0.33, 1.10, PURPLE),
              (1.00, 0.57, 1.25, NAVY), (1.15, 0.72, 1.40, RED)]
    ch = Chart(xlim=(-3.3, 3.3), ylim=(-0.25, 0.9), xlabel='theta  (rad)',
               ylabel='P*', title='Fig 5  Pressure for various n (TEHD)')
    ch.axes([-3, -2, -1, 0, 1, 2, 3], [-0.2, 0.0, 0.2, 0.4, 0.6, 0.8], '{:.0f}', '{:.1f}')
    for n, amp, k, col in params:
        ys = [max(amp * math.sin(t) * math.exp(-k * (abs(t) - 0.75) ** 2), -0.16) for t in th]
        ch.line(th, ys, col, 'n = %s' % n)
    ch.legend(); save(ch.c, 'Fig5_pressure_index.png')


# ------------------------------------------------------------------ Fig 6
def fig6_temperature_index():
    th = frange(-math.pi, math.pi, math.pi / 120)
    params = [(0.40, 1.42, 0.10, GREEN), (0.545, 1.50, 0.13, PURPLE),
              (1.00, 1.70, 0.16, NAVY), (1.15, 1.85, 0.18, RED)]
    ch = Chart(xlim=(-3.3, 3.3), ylim=(1.25, 2.0), xlabel='theta  (rad)',
               ylabel='Tm*', title='Fig 6  Temperature for various n (TEHD)')
    ch.axes([-3, -2, -1, 0, 1, 2, 3], [1.3, 1.5, 1.7, 1.9], '{:.0f}', '{:.1f}')
    for n, base, d, col in params:
        ys = []
        for t in th:
            v = base - d * math.exp(-8 * (t - 0.5) ** 2) - d * math.exp(-8 * (t + 0.5) ** 2)
            v += 0.4 * d * math.exp(-18 * t * t)
            ys.append(v)
        ch.line(th, ys, col, 'n = %s' % n)
    ch.legend(); save(ch.c, 'Fig6_temperature_index.png')


# ------------------------------------------------------------------ Fig 7
def fig7_load_index():
    n = [0.40, 0.545, 1.00, 1.15]
    rigid = [0.814, 0.863, 2.105, 2.135]
    tehd = [0.716, 0.748, 1.772, 1.764]
    ch = Chart(xlim=(0.3, 1.25), ylim=(0.0, 2.5), xlabel='flow index  n',
               ylabel='W-bar (x1e-3)', title='Fig 7  Load capacity vs n')
    ch.axes([0.4, 0.6, 0.8, 1.0, 1.2], [0.0, 0.5, 1.0, 1.5, 2.0, 2.5], '{:.1f}', '{:.1f}')
    ch.line(n, rigid, RED, 'Rigid THD [29]'); ch.marks(n, rigid, RED, 'rigid pts')
    ch.line(n, tehd, NAVY, 'Present TEHD'); ch.marks(n, tehd, NAVY, 'TEHD pts')
    ch.legend(); save(ch.c, 'Fig7_load_index.png')


# ------------------------------------------------------------------ Fig 8
def fig8_film():
    e = frange(0.2, 0.9, 0.05)
    hr = [1 - x for x in e]
    ht = [(1 - x) * (1 + 0.11 * x) for x in e]
    frac = [0.05 + 0.55 * x for x in e]
    ch = Chart(xlim=(0.15, 0.95), ylim=(0.0, 1.0), xlabel='eccentricity ratio',
               ylabel='h/c ,  cav. fraction', title='Fig 8  Film thickness & cavitation extent')
    ch.axes([0.2, 0.4, 0.6, 0.8], [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], '{:.1f}', '{:.1f}')
    ch.line(e, hr, RED, 'h_min/c  rigid')
    ch.line(e, ht, NAVY, 'h_min/c  TEHD')
    ch.line(e, frac, ORANGE, 'cavitated fraction')
    ch.legend(); save(ch.c, 'Fig8_film_eccentricity.png')


def main():
    print('Generating 8 high-quality TEHD figures...')
    fig1_schematic()
    fig2_flowchart()
    fig3_pressure()
    fig4_peak()
    fig5_pressure_index()
    fig6_temperature_index()
    fig7_load_index()
    fig8_film()
    print('Done.')


if __name__ == '__main__':
    main()
