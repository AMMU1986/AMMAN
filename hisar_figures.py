#!/usr/bin/env python3
"""
Generate the four figures for the Hisar infiltration manuscript from
hisar_data/results.json (run hisar_infiltration_analysis.py first).

Pure standard library: reuses PNGCanvas from generate_figures.py and adds
small plotting helpers (axes, ticks, dashed lines, markers, vertical text).

Figures (hisar_figures/):
  Figure_1_Methodology_Flowchart.png
  Figure_2_Empirical_Model_Fits.png
  Figure_3_ML_Observed_vs_Predicted.png
  Figure_4_Model_Comparison_Sensitivity.png
"""

import json
import math
import os

from generate_figures import (PNGCanvas, _FONT, DARK_BLUE, MED_BLUE, LIGHT_BLUE,
                              PALE_BLUE, DARK_GREEN, MED_GREEN, LIGHT_GREEN,
                              ORANGE, LIGHT_ORANGE, RED, PURPLE, LIGHT_PURPLE,
                              GOLD, LIGHT_GOLD, GRAY, LIGHT_GRAY, BLACK, WHITE)

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'hisar_figures')
RES = os.path.join(ROOT, 'hisar_data', 'results.json')

MODEL_COLORS = {
    'Kostiakov': RED,
    'Modified Kostiakov': MED_BLUE,
    'Philip': DARK_GREEN,
    'Horton': ORANGE,
    'Novel (Sihag et al.)': PURPLE,
    'MLR': GRAY,
    'ANN': MED_BLUE,
    'RF': DARK_GREEN,
    'GPR': PURPLE,
}


# ---------------------------------------------------------------- helpers
def text_w(s, scale):
    return len(s) * 6 * scale


def vtext(c, x, y_center, s, color, scale=2):
    """Text rotated 90 degrees counter-clockwise, centred on y_center."""
    total = len(s) * 6 * scale
    y = y_center + total // 2
    for ch in s:
        bm = _FONT.get(ch)
        if bm is not None:
            for ri, row in enumerate(bm):
                for ci in range(5):
                    if row & (1 << (4 - ci)):
                        px, py = x + ri * scale, y - ci * scale
                        for sy in range(scale):
                            for sx in range(scale):
                                c.pixel(px + sx, py - sy, color)
        y -= 6 * scale


def dashed(c, x1, y1, x2, y2, color, thick=2, dash=10, gap=7):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    pos = 0.0
    while pos < L:
        e = min(L, pos + dash)
        c.line(int(x1 + (x2 - x1) * pos / L), int(y1 + (y2 - y1) * pos / L),
               int(x1 + (x2 - x1) * e / L), int(y1 + (y2 - y1) * e / L), color, thick)
        pos += dash + gap


def marker(c, x, y, color, kind='circle', r=5):
    if kind == 'circle':
        c.circle(x, y, r, BLACK, fill=color)
    elif kind == 'square':
        c.rect(x - r, y - r, x + r, y + r, BLACK, fill=color)
    elif kind == 'tri':
        for dy in range(-r, r + 1):
            half = int((dy + r) / 2)
            c.hline(x - half, x + half, y + dy, color)


def nice_ticks(lo, hi, n=5):
    span = hi - lo
    raw = span / n
    mag = 10 ** math.floor(math.log10(raw))
    step = min([1, 2, 2.5, 5, 10], key=lambda m: abs(m * mag - raw)) * mag
    t = math.ceil(lo / step) * step
    out = []
    while t <= hi + 1e-9:
        out.append(round(t, 10))
        t += step
    return out


class Axes:
    def __init__(self, c, x0, y0, w, h, xlim, ylim, title='', xlabel='', ylabel='',
                 scale=2, xticks=None, yticks=None, grid=True):
        self.c, self.x0, self.y0, self.w, self.h = c, x0, y0, w, h
        self.xlim, self.ylim = xlim, ylim
        c.rect(x0, y0, x0 + w, y0 + h, BLACK)
        xticks = xticks if xticks is not None else nice_ticks(*xlim)
        yticks = yticks if yticks is not None else nice_ticks(*ylim)
        for t in xticks:
            px = self.px(t)
            if grid:
                for yy in range(y0 + 1, y0 + h, 4):
                    c.pixel(px, yy, LIGHT_GRAY)
            c.vline(px, y0 + h, y0 + h + 6, BLACK)
            lab = fmt(t)
            c.text(px - text_w(lab, scale) // 2, y0 + h + 12, lab, BLACK, scale)
        for t in yticks:
            py = self.py(t)
            if grid:
                for xx in range(x0 + 1, x0 + w, 4):
                    c.pixel(xx, py, LIGHT_GRAY)
            c.hline(x0 - 6, x0, py, BLACK)
            lab = fmt(t)
            c.text(x0 - 12 - text_w(lab, scale), py - 7, lab, BLACK, scale)
        c.rect(x0, y0, x0 + w, y0 + h, BLACK)
        if title:
            c.text_c(x0 + w // 2, y0 - 30, title, BLACK, scale)
        if xlabel:
            c.text_c(x0 + w // 2, y0 + h + 42, xlabel, BLACK, scale)
        if ylabel:
            vtext(c, x0 - 88, y0 + h // 2, ylabel, BLACK, scale)

    def px(self, x):
        return int(self.x0 + (x - self.xlim[0]) / (self.xlim[1] - self.xlim[0]) * self.w)

    def py(self, y):
        return int(self.y0 + self.h - (y - self.ylim[0]) / (self.ylim[1] - self.ylim[0]) * self.h)

    def inside(self, x, y):
        return self.xlim[0] <= x <= self.xlim[1] and self.ylim[0] <= y <= self.ylim[1]

    def polyline(self, xs, ys, color, thick=3, dash=False):
        pts = [(self.px(x), self.py(y)) for x, y in zip(xs, ys) if self.inside(x, y)]
        for (a, b), (c2, d) in zip(pts, pts[1:]):
            if dash:
                dashed(self.c, a, b, c2, d, color, thick)
            else:
                self.c.line(a, b, c2, d, color, thick)

    def scatter(self, xs, ys, color, kind='circle', r=5):
        for x, y in zip(xs, ys):
            if self.inside(x, y):
                marker(self.c, self.px(x), self.py(y), color, kind, r)


def fmt(v):
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return ('%.2f' % v).rstrip('0').rstrip('.')


def legend(c, x, y, items, scale=2, line_len=36, row_h=26, box=True):
    w = max(text_w(lbl, scale) for lbl, _, _ in items) + line_len + 30
    h = row_h * len(items) + 10
    if box:
        c.rect(x, y, x + w, y + h, GRAY, fill=WHITE)
    for i, (lbl, color, style) in enumerate(items):
        yy = y + 8 + i * row_h + 7
        if style == 'line':
            c.line(x + 10, yy, x + 10 + line_len, yy, color, 3)
        elif style == 'dash':
            dashed(c, x + 10, yy, x + 10 + line_len, yy, color, 3, 8, 5)
        elif style == 'bar':
            c.rect(x + 14, yy - 8, x + 6 + line_len, yy + 8, BLACK, fill=color)
        else:
            marker(c, x + 10 + line_len // 2, yy, color, style, 6)
        c.text(x + 20 + line_len, yy - 7, lbl, BLACK, scale)


# ---------------------------------------------------------------- models
def emp_eval(name, p, t, ic):
    if name == 'Kostiakov':
        return p[0] * t ** (-p[1])
    if name == 'Modified Kostiakov':
        return p[0] * t ** (-p[1]) + p[2]
    if name == 'Philip':
        return 0.5 * p[0] * (t / 60.0) ** -0.5 + p[1]
    if name == 'Horton':
        return p[1] + (p[0] - p[1]) * math.exp(-p[2] * t)
    return p[0] * t ** (-p[1]) + p[2] * ic


# ---------------------------------------------------------------- figure 1
def fig1(r):
    c = PNGCanvas(1600, 1150)
    c.text_c(800, 22, 'Methodological framework of the study', BLACK, 3)

    def box(x, y, w, h, lines, fill, edge):
        c.rect(x, y, x + w, y + h, edge, fill=fill)
        c.rect(x + 1, y + 1, x + w - 1, y + h - 1, edge)
        top = y + h // 2 - len(lines) * 13
        for i, ln in enumerate(lines):
            c.text_c(x + w // 2, top + i * 26, ln, BLACK, 2)

    # row 1: field work
    box(80, 90, 440, 150, ['FIELD INVESTIGATION', '15 sites, 7 land-use groups', 'Double-ring infiltrometer',
                           '(30 / 60 cm rings)'], PALE_BLUE, DARK_BLUE)
    box(580, 90, 440, 150, ['SOIL ANALYSIS', 'Sand, silt, clay (hydrometer)', 'Bulk density (core)',
                            'Moisture (oven), OC (Walkley-Black)'], PALE_BLUE, DARK_BLUE)
    box(1080, 90, 440, 150, ['DATASET', '%d sites x %d readings' % (r['n_sites'], len(r['times'])),
                             '= %d observations' % r['n_obs'], 't = 5 to 180 min'], PALE_BLUE, DARK_BLUE)
    c.arrow(520, 165, 578, 165, DARK_BLUE, 3, 12)
    c.arrow(1020, 165, 1078, 165, DARK_BLUE, 3, 12)
    # split
    box(560, 300, 480, 110, ['DATA PARTITION', 'Training %d (70%%) / Testing %d (30%%)'
                             % (r['n_train'], r['n_test']), 'same split for all models'],
        LIGHT_GOLD, GOLD)
    c.arrow(1300, 240, 1300, 270, DARK_BLUE, 3, 0)
    c.line(1300, 270, 800, 270, DARK_BLUE, 3)
    c.arrow(800, 270, 800, 298, DARK_BLUE, 3, 12)
    # two branches
    c.line(800, 410, 800, 440, BLACK, 3)
    c.line(380, 440, 1220, 440, BLACK, 3)
    c.arrow(380, 440, 380, 478, BLACK, 3, 12)
    c.arrow(1220, 440, 1220, 478, BLACK, 3, 12)
    box(110, 480, 540, 250, ['EMPIRICAL MODELS', '(fitted separately at each site,', 'Levenberg-Marquardt)',
                             '', 'Kostiakov  f = a t^-b', 'Modified Kostiakov  f = a t^-b + ic',
                             'Philip  f = S/2 t^-1/2 + A', 'Horton  f = fc + (f0-fc) e^-kt',
                             'Novel  f = a t^-b + c ic'], LIGHT_GREEN, DARK_GREEN)
    box(950, 480, 540, 250, ['MACHINE-LEARNING MODELS', '(pooled data from all sites)', '',
                             'Inputs: t, sand, clay, BD, MC, OC', 'Output: infiltration rate f',
                             '', 'MLR | ANN (6-8-1) | RF (200 trees)', 'GPR (ARD squared-exponential)'],
        LIGHT_PURPLE, PURPLE)
    c.arrow(380, 730, 380, 790, BLACK, 3, 12)
    c.arrow(1220, 730, 1220, 790, BLACK, 3, 12)
    box(110, 792, 1380, 130, ['PERFORMANCE EVALUATION', 'CC, RMSE, MAE, NSE, Bias, % within +/-20 %',
                              'Random 70/30 test  +  leave-sites-out (5-fold) spatial transfer test'],
        LIGHT_ORANGE, ORANGE)
    c.arrow(800, 922, 800, 970, BLACK, 3, 12)
    box(350, 972, 900, 130, ['ANALYSIS AND RECOMMENDATION', 'One-way ANOVA, sensitivity (drop-one-input)',
                             'Best model for the Hisar region'], LIGHT_BLUE, DARK_BLUE)
    c.save(os.path.join(OUT, 'Figure_1_Methodology_Flowchart.png'))


# ---------------------------------------------------------------- figure 2
def fig2(r):
    sites = {s['site']: s for s in r['sites']}
    obs = {}
    with open(os.path.join(ROOT, 'hisar_data', 'infiltration_observations.csv')) as fh:
        next(fh)
        for line in fh:
            p = line.strip().split(',')
            obs.setdefault(p[0], []).append((float(p[1]), float(p[-1])))
    panels = ['S14', 'S8', 'S4', 'S12']
    c = PNGCanvas(1600, 1300)
    c.text_c(800, 18, 'Observed and fitted infiltration rates at four representative sites', BLACK, 3)
    order = ['Kostiakov', 'Modified Kostiakov', 'Philip', 'Horton', 'Novel (Sihag et al.)']
    fine = [5 + i * 1.0 for i in range(176)]
    for k, sid in enumerate(panels):
        col, row = k % 2, k // 2
        x0, y0 = 150 + col * 790, 110 + row * 560
        ymax = max(f for _, f in obs[sid]) * 1.15
        ymax = math.ceil(ymax / 10) * 10
        s = sites[sid]
        ax = Axes(c, x0, y0, 600, 380, (0, 180), (0, ymax),
                  title='(%s) %s - %s' % ('abcd'[k], sid, s['land_use'].split(' (')[0]),
                  xlabel='Elapsed time (min)', ylabel='Infiltration rate (mm/h)',
                  xticks=[0, 30, 60, 90, 120, 150, 180])
        for name in order:
            p = r['empirical'][name]['params'][sid]
            ys = [emp_eval(name, p, t, s['f_final']) for t in fine]
            ax.polyline(fine, ys, MODEL_COLORS[name], 3,
                        dash=(name == 'Novel (Sihag et al.)'))
        ts = [t for t, _ in obs[sid]]
        fs = [f for _, f in obs[sid]]
        ax.scatter(ts, fs, WHITE, 'circle', 6)
        c.text(x0 + 300, y0 + 20, '%s, BD %.2f' % (s['texture'], s['bd']), BLACK, 2)
        c.text(x0 + 300, y0 + 46, 'MC %.1f %%' % s['mc'], BLACK, 2)
    items = [('Observed', WHITE, 'circle')] + [
        (n, MODEL_COLORS[n], 'dash' if n.startswith('Novel') else 'line') for n in order]
    # horizontal legend at bottom
    x = 110
    y = 1230
    for lbl, color, style in items:
        if style == 'circle':
            marker(c, x + 18, y + 8, color, 'circle', 6)
        elif style == 'dash':
            dashed(c, x, y + 8, x + 36, y + 8, color, 3, 8, 5)
        else:
            c.line(x, y + 8, x + 36, y + 8, color, 3)
        c.text(x + 46, y + 1, lbl, BLACK, 2)
        x += 46 + text_w(lbl, 2) + 40
    c.save(os.path.join(OUT, 'Figure_2_Empirical_Model_Fits.png'))


# ---------------------------------------------------------------- figure 3
def fig3(r):
    c = PNGCanvas(1600, 1300)
    c.text_c(800, 18, 'Observed vs. predicted infiltration rate (testing data, n = %d)' % r['n_test'],
             BLACK, 3)
    yo = r['test_obs']
    lim = math.ceil(max(yo + [v for m in r['ml'].values() for v in m['test_pred']]) / 20) * 20
    for k, name in enumerate(['MLR', 'ANN', 'RF', 'GPR']):
        col, row = k % 2, k // 2
        x0, y0 = 170 + col * 780, 110 + row * 590
        ax = Axes(c, x0, y0, 470, 470, (0, lim), (0, lim),
                  title='(%s) %s' % ('abcd'[k], name),
                  xlabel='Observed f (mm/h)', ylabel='Predicted f (mm/h)')
        ax.polyline([0, lim], [0, lim], BLACK, 2)
        ax.polyline([0, lim / 1.2], [0, lim], GRAY, 2, dash=True)
        ax.polyline([0, lim], [0, lim * 0.8], GRAY, 2, dash=True)
        ax.scatter(yo, r['ml'][name]['test_pred'], MODEL_COLORS[name], 'circle', 5)
        m = r['ml'][name]['test']
        lines = ['CC   = %.3f' % m['CC'], 'RMSE = %.2f' % m['RMSE'],
                 'NSE  = %.3f' % m['NSE'], '+/-20%% : %.0f %%' % m['within20']]
        for i, ln in enumerate(lines):
            c.text(x0 + 16, y0 + 16 + i * 26, ln, BLACK, 2)
    x, y = 420, 1245
    c.line(x, y + 8, x + 40, y + 8, BLACK, 2)
    c.text(x + 50, y + 1, 'Line of perfect agreement', BLACK, 2)
    x += 50 + text_w('Line of perfect agreement', 2) + 50
    dashed(c, x, y + 8, x + 40, y + 8, GRAY, 2, 8, 5)
    c.text(x + 50, y + 1, '+/-20 % error lines', BLACK, 2)
    c.save(os.path.join(OUT, 'Figure_3_ML_Observed_vs_Predicted.png'))


# ---------------------------------------------------------------- figure 4
def fig4(r):
    c = PNGCanvas(1600, 1350)
    c.text_c(800, 18, 'Model comparison and sensitivity analysis', BLACK, 3)
    # (a) RMSE bars, test and leave-sites-out
    names = ['Kostiakov', 'Modified Kostiakov', 'Philip', 'Horton', 'Novel (Sihag et al.)',
             'MLR', 'ANN', 'RF', 'GPR']
    short = ['KOS', 'M-KOS', 'PHI', 'HOR', 'NOVEL', 'MLR', 'ANN', 'RF', 'GPR']
    test = [r['empirical'][n]['test']['RMSE'] if n in r['empirical'] else r['ml'][n]['test']['RMSE']
            for n in names]
    lso = [None] * 5 + [r['leave_sites_out'][n]['RMSE'] for n in ['MLR', 'ANN', 'RF', 'GPR']]
    ymax = math.ceil(max(test + [v for v in lso if v]) * 1.25 / 5) * 5
    x0, y0, w, h = 170, 110, 1340, 440
    ax = Axes(c, x0, y0, w, h, (0, len(names)), (0, ymax), title='(a) RMSE of all models',
              ylabel='RMSE (mm/h)', xticks=[], grid=True)
    for i, (sn, tv, lv) in enumerate(zip(short, test, lso)):
        cx = ax.px(i + 0.5)
        bw = 46
        color = DARK_GREEN if i < 5 else PURPLE
        if lv is None:
            c.rect(cx - bw // 2, ax.py(tv), cx + bw // 2, ax.py(0), BLACK, fill=LIGHT_GREEN)
            c.text_c(cx, ax.py(tv) - 22, '%.2f' % tv, BLACK, 2)
        else:
            c.rect(cx - bw - 2, ax.py(tv), cx - 2, ax.py(0), BLACK, fill=LIGHT_PURPLE)
            c.rect(cx + 2, ax.py(lv), cx + bw + 2, ax.py(0), BLACK, fill=ORANGE)
            c.text_c(cx - bw // 2, ax.py(tv) - 22, '%.1f' % tv, BLACK, 2)
            c.text_c(cx + bw // 2, ax.py(lv) - 22, '%.1f' % lv, BLACK, 2)
        c.text_c(cx, y0 + h + 14, sn, color, 2)
    c.vline(ax.px(5), y0, y0 + h, GRAY)
    c.text_c(ax.px(2.5), y0 + h + 44, 'Empirical (site-calibrated)', DARK_GREEN, 2)
    c.text_c(ax.px(7), y0 + h + 44, 'Machine learning (pooled)', PURPLE, 2)
    legend(c, x0 + 20, y0 + 12,
           [('Empirical, testing data', LIGHT_GREEN, 'bar'),
            ('ML, testing data (random split)', LIGHT_PURPLE, 'bar'),
            ('ML, leave-sites-out', ORANGE, 'bar')])
    # (b) sensitivity
    feats = ['t', 'sand', 'clay', 'bd', 'mc', 'oc']
    labels = ['Time', 'Sand', 'Clay', 'BD', 'MC', 'OC']
    sens = r['sensitivity']
    base = {m: r['ml'][m]['test']['RMSE'] for m in ['RF', 'GPR']}
    vals = [sens[m][f]['RMSE'] for m in ['RF', 'GPR'] for f in feats]
    ymax = math.ceil(max(vals) * 1.2 / 2) * 2
    x0, y0, w, h = 170, 760, 1340, 440
    ax = Axes(c, x0, y0, w, h, (0, len(feats)), (0, ymax),
              title='(b) Sensitivity: testing RMSE after removing one input',
              ylabel='RMSE (mm/h)', xticks=[])
    for m, col in [('RF', DARK_GREEN), ('GPR', PURPLE)]:
        ax.polyline([0, len(feats)], [base[m], base[m]], col, 2, dash=True)
    for i, (f, lb) in enumerate(zip(feats, labels)):
        cx = ax.px(i + 0.5)
        bw = 64
        v1, v2 = sens['RF'][f]['RMSE'], sens['GPR'][f]['RMSE']
        c.rect(cx - bw - 6, ax.py(v1), cx - 6, ax.py(0), BLACK, fill=LIGHT_GREEN)
        c.rect(cx + 6, ax.py(v2), cx + bw + 6, ax.py(0), BLACK, fill=LIGHT_PURPLE)
        c.text_c(cx - bw // 2 - 6, ax.py(v1) - 22, '%.2f' % v1, BLACK, 2)
        c.text_c(cx + bw // 2 + 6, ax.py(v2) - 22, '%.2f' % v2, BLACK, 2)
        c.text_c(cx, y0 + h + 14, 'without ' + lb, BLACK, 2)
    legend(c, x0 + w - 430, y0 + 12,
           [('RF', LIGHT_GREEN, 'bar'), ('GPR', LIGHT_PURPLE, 'bar'),
            ('RF, all inputs (%.2f)' % base['RF'], DARK_GREEN, 'dash'),
            ('GPR, all inputs (%.2f)' % base['GPR'], PURPLE, 'dash')])
    c.save(os.path.join(OUT, 'Figure_4_Model_Comparison_Sensitivity.png'))


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(RES) as fh:
        r = json.load(fh)
    fig1(r)
    fig2(r)
    fig3(r)
    fig4(r)
    print('figures written to', OUT)


if __name__ == '__main__':
    main()
