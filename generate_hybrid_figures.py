#!/usr/bin/env python3
"""
Seven high-quality figures for the Al7075-SiC/Gr + Al2O3 nanofluid bearing paper.
Pure standard library; reuses the anti-aliased HQ engine from hq_plot.py.

  Fig 1  Hybrid bearing + rig schematic
  Fig 2  Integrated experimental-CFD-FEA methodology flowchart
  Fig 3  Al2O3 nanofluid thermal conductivity & relative viscosity vs volume fraction
  Fig 4  Hydrodynamic pressure distribution for base oil & nanofluid concentrations
  Fig 5  Coefficient of friction & specific wear rate vs concentration
  Fig 6  Max bush temperature vs load (base oil vs 0.4 wt%)
  Fig 7  FEA von Mises stress & radial deformation vs load
"""

import os
import math
from hq_plot import HQ, Chart

OUT = '/projects/sandbox/AMMAN/hybrid_figures'

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
LGREY = (232, 232, 236)
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


# ---------------------------------------------------------------- Fig 1
def fig1_schematic():
    c = HQ(1300, 980, ss=2)
    c.text(650, 26, 'Figure 1.  Al7075-SiC/Gr hybrid bearing and test rig', NAVY,
           size=28, align='c', bold=True)
    cx, cy, Rb, Rj, ecc = 440, 520, 300, 244, 52
    jx, jy = cx, cy + ecc
    # nanofluid film annulus (light blue)
    for a in range(0, 360, 2):
        r = math.radians(a)
        c.line(jx + Rj * math.cos(r), jy + Rj * math.sin(r),
               cx + Rb * math.cos(r), cy + Rb * math.sin(r), LBLUE, 1.2)
    # bush (composite) ring with speckle to suggest SiC/Gr
    c.ring(cx, cy, Rb, GREY, 3.4)
    c.ring(cx, cy, Rb + 26, GREY, 3.0)
    for i in range(140):
        a = (i * 2.39996) % (2 * math.pi)
        rr = Rb + 4 + (i % 11)
        col = BLACK if i % 3 else ORANGE
        c.disk(cx + rr * math.cos(a), cy + rr * math.sin(a), 2.0, col)
    # journal
    c.ring(jx, jy, Rj, NAVY, 4.0, fill=(236, 242, 250))
    c.disk(cx, cy, 4, BLACK); c.disk(jx, jy, 4, RED)
    c.line(cx, cy, jx, jy, RED, 2.2)
    c.text(cx + 12, (cy + jy) / 2 - 6, 'e', RED, size=22, bold=True)
    c.arrow(jx + 55, jy - 190, jx + 125, jy - 160, NAVY, 3.0, 16)
    c.text(jx + 100, jy - 220, 'U', NAVY, size=24, bold=True)
    c.text(cx - 60, cy + 2, 'journal', NAVY, size=18, align='c')
    c.text(cx, cy - Rb - 44, 'composite bush (Al7075-SiC/Gr)', GREY, size=18, align='c')
    c.text(cx + Rb + 36, cy + 120, 'Al2O3', BLUE, size=18)
    c.text(cx + Rb + 36, cy + 144, 'nanofluid film', BLUE, size=18)
    # sensor callouts on the right
    sx = 980
    items = [('pressure sensor', RED), ('thermocouples', ORANGE),
             ('friction load cell', GREEN), ('eccentricity probe', PURPLE)]
    c.rect(sx - 20, 150, 1290, 150 + 52 * len(items) + 10, BLACK, 1.8, fill=(251, 251, 253))
    c.text(sx - 6, 120, 'Rig instrumentation', NAVY, size=18, bold=True)
    for i, (lab, col) in enumerate(items):
        yy = 170 + i * 52
        c.disk(sx, yy, 7, col)
        c.text(sx + 24, yy - 9, lab, BLACK, size=18)
        c.arrow(sx - 8, yy, cx + Rb * math.cos(math.radians(300 + i * 15)),
                cy + Rb * math.sin(math.radians(300 + i * 15)), col, 1.6, 10)
    save(c, 'Fig1_schematic.png')


# ---------------------------------------------------------------- Fig 2
def _box(c, x0, y0, x1, y1, lines, fill, tag=None):
    c.round_rect(x0, y0, x1, y1, BLACK, 2.4, fill=fill, rad=12)
    n = len(lines)
    cxm, cym = (x0 + x1) / 2, (y0 + y1) / 2
    for i, ln in enumerate(lines):
        c.text(cxm, cym - (n * 13) + i * 26, ln, BLACK, size=19, align='c')
    if tag:
        c.text(x0 - 18, cym - 8, tag, (120, 60, 150), size=16, align='r')


def fig2_flowchart():
    c = HQ(1340, 1120, ss=2)
    c.text(670, 24, 'Figure 2.  Integrated experimental-CFD-FEA workflow', NAVY,
           size=28, align='c', bold=True)
    L, R = 360, 980
    cxm = (L + R) / 2
    # top inputs: two boxes feeding the loop
    _box(c, 150, 90, 560, 170, ['Fabricate & characterise', 'Al7075-SiC/Gr composite'], LAMBER)
    _box(c, 620, 90, 1030, 170, ['Prepare & characterise', 'Al2O3 nanofluid'], LAMBER)
    c.text(240, 188, '(Table 1, 2)', (120, 60, 150), size=16, align='c')
    c.text(940, 188, '(Table 3)', (120, 60, 150), size=16, align='c')
    _box(c, L, 230, R, 320, ['CFD film solver:  Navier-Stokes', '+ energy + cavitation  ->  p, T'], LGREEN, 'Eq (15-32)')
    _box(c, L, 350, R, 440, ['FEA structural + thermal:', 'stress, deflection  ->  delta'], LGREEN, 'Eq (42-50)')
    _box(c, L, 470, R, 560, ['FSI exchange: pressure <-> deflection,', 'update film  h = h0 + delta'], LBLUE, 'Eq (51-53)')
    c.arrow(355, 170, 420, 230, BLACK, 2.2, 12)
    c.arrow(825, 170, 760, 230, BLACK, 2.2, 12)
    c.arrow(cxm, 320, cxm, 350, BLACK, 2.4, 12)
    c.arrow(cxm, 440, cxm, 470, BLACK, 2.4, 12)
    # decision diamond
    dcx, dcy, dw, dh = cxm, 650, 175, 66
    c.poly([(dcx, dcy - dh), (dcx + dw, dcy), (dcx, dcy + dh), (dcx - dw, dcy)], BLACK, 2.4, fill=LAMBER)
    c.text(dcx, dcy - 16, 'Converged?', BLACK, size=19, align='c')
    c.text(dcx, dcy + 12, '(p, T, delta < 1e-5)', BLACK, size=16, align='c')
    c.arrow(cxm, 560, cxm, dcy - dh, BLACK, 2.4, 12)
    # feedback No
    fx = R + 140
    c.line(dcx + dw, dcy, fx, dcy, RED, 2.4)
    c.line(fx, dcy, fx, 275, RED, 2.4)
    c.arrow(fx, 275, R, 275, RED, 2.4, 12)
    c.text(dcx + dw + 16, dcy - 26, 'No', RED, size=20, bold=True)
    c.text(fx - 150, 258, 'under-relaxed repeat', RED, size=16)
    # Yes -> compare with experiment
    _box(c, L, 770, R, 860, ['Predict friction, wear, pressure, T', '->  compare with rig measurements'], LBLUE, 'Table 5')
    c.arrow(cxm, dcy + dh, cxm, 770, BLACK, 2.4, 12)
    c.text(cxm + 16, (dcy + dh + 770) / 2 - 8, 'Yes', GREEN, size=20, bold=True)
    c.round_rect(cxm - 95, 900, cxm + 95, 965, BLACK, 2.4, fill=LGREY, rad=28)
    c.text(cxm, 925, 'Design output', BLACK, size=20, align='c', bold=True)
    c.arrow(cxm, 860, cxm, 900, BLACK, 2.4, 12)
    save(c, 'Fig2_methodology_flowchart.png')


# ---------------------------------------------------------------- Fig 3
def fig3_nanofluid():
    # x = volume fraction in % ; model lines pass through the measured points
    xl = [0.0, 0.047, 0.094, 0.142, 0.16]
    k_line = [1.000, 1.021, 1.048, 1.111, 1.130]
    mu_line = [1.000, 1.023, 1.040, 1.090, 1.100]
    km = [0.047, 0.094, 0.142]; kv = [1.021, 1.048, 1.111]
    mm = [0.047, 0.094, 0.142]; mv = [1.023, 1.040, 1.090]
    ch = Chart(xlim=(0, 0.16), ylim=(1.0, 1.16), xlabel='nanoparticle volume fraction (%)',
               ylabel='relative k , relative mu', title='Fig 3  Al2O3 nanofluid properties')
    ch.axes([0.0, 0.04, 0.08, 0.12, 0.16], [1.0, 1.04, 1.08, 1.12, 1.16], '{:.2f}', '{:.2f}')
    ch.line(xl, k_line, RED, 'k ratio (model)')
    ch.line(xl, mu_line, NAVY, 'mu ratio (model)')
    ch.marks(km, kv, RED, 'k measured')
    ch.marks(mm, mv, NAVY, 'mu measured')
    ch.legend(); save(ch.c, 'Fig3_nanofluid_properties.png')


# ---------------------------------------------------------------- Fig 4
def fig4_pressure():
    th = frange(-math.pi, math.pi, math.pi / 120)
    confs = [(0.0, 1.00, GREEN, 'base oil'), (0.2, 1.07, PURPLE, '0.2 wt%'),
             (0.4, 1.12, NAVY, '0.4 wt%'), (0.6, 1.10, RED, '0.6 wt%')]
    ch = Chart(xlim=(-3.3, 3.3), ylim=(-0.6, 5.2), xlabel='theta  (rad)',
               ylabel='pressure  (MPa)', title='Fig 4  Pressure distribution')
    ch.axes([-3, -2, -1, 0, 1, 2, 3], [0, 1, 2, 3, 4, 5], '{:.0f}', '{:.0f}')
    for w, amp, col, lab in confs:
        ys = [max(4.2 * amp * math.sin(t - 0.3) * math.exp(-1.1 * (abs(t - 0.3) - 0.7) ** 2), -0.3) for t in th]
        ch.line(th, ys, col, lab)
    ch.legend(); save(ch.c, 'Fig4_pressure_distribution.png')


# ---------------------------------------------------------------- Fig 5
def fig5_friction_wear():
    conc = [0.0, 0.2, 0.4, 0.6]
    cof = [0.082, 0.064, 0.051, 0.058]
    wear = [3.10, 2.00, 1.40, 1.80]
    ch = Chart(xlim=(-0.08, 0.7), ylim=(0.0, 3.4), xlabel='Al2O3 concentration (wt%)',
               ylabel='wear (1e-5) , 10xCOF', title='Fig 5  Friction & wear vs concentration')
    ch.axes([0.0, 0.2, 0.4, 0.6], [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0], '{:.1f}', '{:.1f}')
    cof_sc = [v * 10 for v in cof]    # 0.82,0.64,0.51,0.58  (= 10 x COF)
    ch.line(conc, cof_sc, NAVY, 'COF x10'); ch.marks(conc, cof_sc, NAVY, 'COF pts')
    ch.line(conc, wear, RED, 'wear rate'); ch.marks(conc, wear, RED, 'wear pts')
    ch.legend(); save(ch.c, 'Fig5_friction_wear.png')


# ---------------------------------------------------------------- Fig 6
def fig6_temperature():
    load = [250, 500, 750, 1000]
    base = [58, 68, 78, 90]
    nano = [55, 63, 71, 82]
    ch = Chart(xlim=(150, 1100), ylim=(40, 100), xlabel='applied load  (N)',
               ylabel='max bush temperature (C)', title='Fig 6  Thermal response')
    ch.axes([250, 500, 750, 1000], [40, 55, 70, 85, 100], '{:.0f}', '{:.0f}')
    ch.line(load, base, RED, 'base oil'); ch.marks(load, base, RED, 'base pts')
    ch.line(load, nano, NAVY, 'Al2O3 0.4 wt%'); ch.marks(load, nano, NAVY, 'nano pts')
    ch.legend(); save(ch.c, 'Fig6_temperature.png')


# ---------------------------------------------------------------- Fig 7
def fig7_fea():
    load = [250, 500, 750, 1000]
    svm = [48, 95, 142, 188]        # MPa
    defo = [1.1, 2.2, 3.3, 4.5]     # micrometre
    ch = Chart(xlim=(150, 1100), ylim=(0, 220), xlabel='applied load  (N)',
               ylabel='stress (MPa) , defl x40 (um)', title='Fig 7  FEA stress & deformation')
    ch.axes([250, 500, 750, 1000], [0, 50, 100, 150, 200], '{:.0f}', '{:.0f}')
    ch.line(load, svm, RED, 'von Mises stress'); ch.marks(load, svm, RED, 'stress pts')
    defo_sc = [d * 40 for d in defo]  # scale deflection to share axis
    ch.line(load, defo_sc, NAVY, 'deflection x40'); ch.marks(load, defo_sc, NAVY, 'defl pts')
    ch.legend(); save(ch.c, 'Fig7_fea_stress.png')


def main():
    print('Generating 7 high-quality hybrid-bearing figures...')
    fig1_schematic(); fig2_flowchart(); fig3_nanofluid(); fig4_pressure()
    fig5_friction_wear(); fig6_temperature(); fig7_fea()
    print('Done.')


if __name__ == '__main__':
    main()
