#!/usr/bin/env python3
"""Render all figures for the three articles from results/*.json."""
import json
import math
import os
from collections import defaultdict

from plotlib import (PNGCanvas, Axes, legend, heatmap, swatch_legend, panel_label,
                     PALETTE, BLACK, GRAY, WHITE)

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, 'results')
L = lambda n: json.load(open(os.path.join(RES, n + '.json')))
DET = 0.1
C_P, C_S, C_M, C_E = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def outdir(n):
    d = os.path.join(HERE, f'article{n}_figures')
    os.makedirs(d, exist_ok=True)
    return d


def clip(v, lo=1e-5):
    return [max(x, lo) for x in v]


# ============================================================== Article 1
def a1_fig1(d):
    tc = L('a1_timecourse')
    s, n = tc['surg'], tc['nos']
    cv = PNGCanvas(1700, 760)
    ax = Axes(cv, 150, 110, 650, 520, (0, 1500), (1e-4, 1e2), logy=True)
    ax.frame('Time (days)', 'Mass (dimensionless)', 'A. Resection at day 540')
    ax.hmark(DET, GRAY, 'detection threshold')
    ax.vmark(540, GRAY, 'surgery')
    ax.plot(s['t'], clip(s['Mp']), C_P)
    ax.plot(s['t'], clip(s['Ms']), C_S)
    ax.plot(s['t'], clip(s['Mm']), C_M)
    ax.plot(n['t'], clip(n['Ms']), C_S, 2, dash=True)
    legend(cv, 470, 470, [('primary tumour', C_P), ('satellite', C_S), ('immune cells', C_M), ('satellite, no surgery', C_S, True)])
    panel_label(cv, 20, 20, 'A')
    # profiles
    ax2 = Axes(cv, 1000, 110, 650, 520, (0, 4), (0, 0.3))
    ax2.frame('Radius r (mm)', 'Immune cell density m', 'B. Immune field around the lesion')
    cols = [PALETTE[0], PALETTE[4], PALETTE[1], PALETTE[3], PALETTE[5]]
    items = []
    for k, pr in enumerate(s['profiles'][:4]):
        ax2.plot(pr['r'], pr['m'], cols[k])
        items.append((f"day {int(pr['t'])}", cols[k]))
    ax2.vmark(2.0, C_S, 'satellite', dy=40)
    ax2.vmark(1.4, GRAY, 'excision edge', dy=10)
    legend(cv, 1430, 250, items)
    panel_label(cv, 880, 20, 'B')
    cv.save(os.path.join(d, 'Figure_1_Resection_Recurrence.png'))


def a1_fig2(d):
    f = L('a1_fatemap')
    rs, ms = f['rs'], f['ms']
    m = {(round(x['r'], 2), x['margin']): x for x in f['fate']}
    grid = []
    for mg in ms:
        row = []
        for r in rs:
            x = m[(round(r, 2), mg)]
            row.append('P' if x['preMs'] > DET else ('R' if x['finalMs'] > DET else ('d' if x['finalMs'] > 0 else 'E')))
        grid.append(row)
    colors = {'E': (198, 224, 180), 'd': (255, 230, 153), 'R': (237, 125, 49), 'P': (150, 30, 30)}
    cv = PNGCanvas(1700, 760)
    heatmap(cv, 150, 110, 700, 520, grid, colors, rs, ms, 'Satellite seeding radius r (mm)', 'Excision margin (mm)',
            'A. Satellite fate after resection', xtick_every=5, ytick_every=2)
    swatch_legend(cv, 160, 700 - 10, [], 2)
    swatch_legend(cv, 880, 120, [('no recurrence', colors['E']), ('recurrence after surgery', colors['R']),
                                 ('escaped before surgery', colors['P'])])
    panel_label(cv, 20, 20, 'A')
    # time to detection for margin 0.5
    ax = Axes(cv, 1180, 300, 470, 330, (1.0, 4.0), (0, 80))
    ax.frame('Seeding radius r (mm)', 'Days to detection', 'B. Margin 0.5 mm')
    xs, ys = [], []
    for r in rs:
        x = m[(round(r, 2), 0.5)]
        if x['trec'] is not None and x['preMs'] <= DET:
            xs.append(r); ys.append(x['trec'])
    ax.plot(xs, ys, C_S)
    ax.scatter(xs, ys, C_S)
    panel_label(cv, 1060, 230, 'B')
    cv.save(os.path.join(d, 'Figure_2_Fate_Map_Margin.png'))


def a1_fig3(d):
    t = L('a1_timing')
    offs = t['offs']
    arms = t['arms']
    lab = lambda a: (f"Q x{a['F']} {a['D']}d" if a['key'] == 'Q_boost' else f"bK x{a['F']} {a['D']}d")
    by = {}
    for x in t['timing']:
        by[(lab(x['arm']), x['off'])] = x
    rows = [lab(a) for a in arms]
    grid = [['E' if by[(r, o)]['finalMs'] < 1e-3 else 'R' for o in offs] for r in rows]
    colors = {'E': (84, 172, 64), 'R': (237, 125, 49)}
    cv = PNGCanvas(1700, 820)
    heatmap(cv, 260, 110, 620, 560, grid, colors, offs, list(range(len(rows))), 'Therapy start relative to surgery (days)',
            'Schedule', 'A. Outcome at day 1500', xtick_every=5, ytick_every=1, yfmt=lambda j: rows[j])
    swatch_legend(cv, 270, 760, [('eradicated', colors['E'])])
    swatch_legend(cv, 560, 760, [('recurrence persists', colors['R'])])
    panel_label(cv, 20, 20, 'A')
    ax = Axes(cv, 1060, 110, 600, 560, (400, 1500), (1e-5, 1e2), logy=True)
    ax.frame('Time (days)', 'Satellite mass', 'B. Q x3 for 60 days')
    ax.vmark(540, GRAY, 'surgery')
    ax.hmark(DET, GRAY, '')
    cols = [BLACK, PALETTE[0], PALETTE[2], PALETTE[3]]
    items = []
    for k, rt in enumerate(t['repTC']):
        ax.plot(rt['t'], clip(rt['Ms']), cols[k])
        items.append((rt['name'], cols[k]))
    legend(cv, 1330, 470, items)
    panel_label(cv, 940, 20, 'B')
    cv.save(os.path.join(d, 'Figure_3_Immunotherapy_Timing.png'))


def a1_fig4(d):
    t = L('a1_timing')
    cv = PNGCanvas(1000, 720)
    ax = Axes(cv, 150, 110, 780, 500, (400, 1500), (1e-3, 1e2), logy=True)
    ax.frame('Time (days)', 'Satellite mass', 'Continuous adjuvant recruitment boost from day 540')
    ax.vmark(540, GRAY, 'surgery')
    ax.hmark(DET, GRAY, 'detection')
    base = L('a1_timecourse')['surg']
    ax.plot(base['t'], clip(base['Ms'], 1e-3), BLACK)
    items = [('no adjuvant', BLACK)]
    for k, c in enumerate(t['cont']):
        ts = [5 * i for i in range(len(c['Ms']))]
        ax.plot(ts, clip(c['Ms'], 1e-3), PALETTE[k])
        items.append((f"Q x{c['F']}", PALETTE[k]))
    legend(cv, 700, 380, items)
    cv.save(os.path.join(d, 'Figure_4_Continuous_Adjuvant.png'))


# ============================================================== Article 2
def a2_fig1(d):
    tc = L('a2_timecourse')
    cv = PNGCanvas(1700, 760)
    ax = Axes(cv, 150, 110, 650, 520, (0, 2000), (0.1, 1000), logy=True)
    ax.frame('Time (days)', 'Primary tumour mass', 'A. Effect of immune-derived TAF')
    items = []
    for k, x in enumerate(tc['tcs']):
        ax.plot(x['t'], clip(x['Mp'], 0.1), PALETTE[k])
        items.append((f"g_vm = {x['g']}", PALETTE[k]))
    legend(cv, 520, 470, items)
    panel_label(cv, 20, 20, 'A')
    x = tc['tcs'][1]
    ax2 = Axes(cv, 1000, 110, 650, 520, (0, 1000), (0.01, 1000), logy=True)
    ax2.frame('Time (days)', 'Mass', 'B. g_vm = 900: two-phase growth')
    ax2.plot(x['t'], clip(x['Mp'], 0.01), C_P)
    ax2.plot(x['t'], clip(x['Mm'], 0.01), C_M)
    ax2.plot(x['t'], clip(x['Me'], 0.01), C_E)
    te = next(k for k, e in enumerate(x['Me']) if e > 1)
    ax2.vmark(te, GRAY, 'angiogenic switch')
    legend(cv, 1360, 470, [('tumour', C_P), ('immune cells', C_M), ('vasculature', C_E)])
    panel_label(cv, 880, 20, 'B')
    cv.save(os.path.join(d, 'Figure_1_Two_Phase_Growth.png'))


def a2_fig2(d):
    tc = L('a2_timecourse')
    cv = PNGCanvas(1700, 760)
    ax = Axes(cv, 150, 110, 650, 520, (0, 4), (0, 1.4))
    ax.frame('Radius r (mm)', 'TAF v (scaled)', 'A. TAF profiles, g_vm = 900')
    ax2 = Axes(cv, 1000, 110, 650, 520, (0, 4), (0, 1.05))
    ax2.frame('Radius r (mm)', 'Density', 'B. Tumour (solid) and vessels (dashed)')
    items = []
    for k, pr in enumerate(tc['prof']):
        col = PALETTE[k]
        ax.plot(pr['r'], pr['v'], col)
        ax2.plot(pr['r'], pr['p'], col)
        ax2.plot(pr['r'], pr['e'], col, 2, dash=True)
        items.append((f"day {int(pr['t'])}", col))
    ax.hmark(0.5, GRAY, 'switch threshold V_T')
    legend(cv, 620, 130, items)
    panel_label(cv, 20, 20, 'A')
    panel_label(cv, 880, 20, 'B')
    cv.save(os.path.join(d, 'Figure_2_TAF_Profiles.png'))


def a2_fig3(d):
    r = L('a2_dormancy')
    gc = r['gc']
    xs = [x['g'] - gc for x in r['esc'] if x['tesc']]
    ys = [x['tesc'] for x in r['esc'] if x['tesc']]
    cv = PNGCanvas(1000, 720)
    ax = Axes(cv, 150, 110, 780, 500, (0.1, 1000), (10, 10000), logy=True, logx=True)
    ax.frame('g_vm - g_c', 'Time to angiogenic switch (days)', 'Dormancy duration near the critical point')
    ax.scatter(xs, ys, C_P, 6)
    # reference slope -1/2 through the geometric centre of points
    lx = [math.log10(x) for x in xs]; ly = [math.log10(y) for y in ys]
    cx, cy = sum(lx) / len(lx), sum(ly) / len(ly)
    ref = [10 ** (cy - 0.5 * (math.log10(x) - cx)) for x in (0.1, 1000)]
    ax.plot([0.1, 1000], ref, GRAY, 2, dash=True)
    legend(cv, 560, 130, [('simulation', C_P), ('slope -1/2 reference', GRAY, True)])
    cv.save(os.path.join(d, 'Figure_3_Dormancy_Scaling.png'))


def a2_cls(x):
    if x['Mp'] < 1e-3:
        return '.'
    if x['tesc'] is None:
        return 'c' if x['Mp'] < 2 else 'A'
    return 'V' if x['Mp'] < 2 else 'X'


def a2_fig4(d):
    p = L('a2_phase')
    colors = {'.': (230, 230, 230), 'c': (198, 224, 180), 'A': (255, 230, 153), 'V': (155, 194, 230), 'X': (192, 0, 0)}
    cv = PNGCanvas(1700, 820)
    for k, (key, title, x0) in enumerate((('phase', 'A. Constitutive TAF g_v = 20', 150), ('phase2', 'B. Constitutive TAF g_v = 15', 900))):
        m = {(round(x['Q'], 3), x['g']): x for x in p[key]}
        grid = [[a2_cls(m[(round(Q, 3), g)]) for Q in p['Qs']] for g in p['Gs']]
        heatmap(cv, x0, 110, 600, 560, grid, colors, p['Qs'], p['Gs'], 'Immune influx Q', 'Immune TAF g_vm',
                title, xtick_every=3, ytick_every=2)
        panel_label(cv, x0 - 130, 20, 'AB'[k])
    swatch_legend(cv, 150, 760, [('controlled, avascular', colors['c'])])
    swatch_legend(cv, 520, 760, [('vascularised, controlled', colors['V'])])
    swatch_legend(cv, 920, 760, [('angiogenic escape', colors['X'])])
    swatch_legend(cv, 1220, 760, [('avascular escape', colors['A'])])
    cv.save(os.path.join(d, 'Figure_4_Phase_Diagram.png'))


def a2_fig5(d):
    a = L('a2_antivegf')
    cv = PNGCanvas(1700, 760)
    for k, (g, x0) in enumerate(((900, 150), (1000, 1000))):
        ax = Axes(cv, x0, 110, 650, 520, (0, 2000), (0.1, 1000), logy=True)
        ax.frame('Time (days)', 'Primary tumour mass', f'{"AB"[k]}. g_vm = {g}, 50 pct TAF neutralised')
        items = []
        for j, sname in enumerate(a['scheds']):
            x = next(z for z in a['anti'] if z['g'] == g and z['f'] == 0.5 and z['sched'] == sname)
            ts = [5 * i for i in range(len(x['series']))]
            ax.plot(ts, clip(x['series'], 0.1), PALETTE[j], 3 if j else 4)
            items.append((sname, PALETTE[j]))
        legend(cv, x0 + 10, 120, items)
        panel_label(cv, x0 - 130, 20, 'AB'[k])
    cv.save(os.path.join(d, 'Figure_5_Anti_VEGF_Schedules.png'))


# ============================================================== Article 3
def a3_fig1(d):
    h = L('a3_halo')
    colors = {'.': (198, 224, 180), 'd': (255, 230, 153), 'E': (192, 0, 0), 'R': (237, 125, 49), 'P': (150, 30, 30)}
    cv = PNGCanvas(1700, 820)
    m = {(round(x['Q'], 3), round(x['r'], 2)): x for x in h['halo']}
    ms = {(round(x['Q'], 3), round(x['r'], 2)): x for x in h['haloS']}
    g1 = [['.' if m[(round(Q, 3), round(r, 2))]['Ms'] == 0 else ('d' if m[(round(Q, 3), round(r, 2))]['Ms'] < DET else 'E') for r in h['rs']] for Q in h['Qs']]
    def c2(y):
        if y['Ms'] == 0: return '.'
        if y['Ms'] < DET: return 'd'
        return 'P' if y['pre'] > DET else 'R'
    g2 = [[c2(ms[(round(Q, 3), round(r, 2))]) for r in h['rs']] for Q in h['Qs']]
    heatmap(cv, 150, 110, 650, 560, g1, colors, h['rs'], h['Qs'], 'Seeding radius r (mm)', 'Immune influx Q',
            'A. Primary left in place', xtick_every=10, ytick_every=1)
    heatmap(cv, 1000, 110, 650, 560, g2, colors, h['rs'], h['Qs'], 'Seeding radius r (mm)', 'Immune influx Q',
            'B. Primary resected at day 540', xtick_every=10, ytick_every=1)
    panel_label(cv, 20, 20, 'A'); panel_label(cv, 870, 20, 'B')
    swatch_legend(cv, 150, 760, [('eliminated or excised', colors['.'])])
    swatch_legend(cv, 520, 760, [('dormant', colors['d'])])
    swatch_legend(cv, 760, 760, [('escaped (primary present)', colors['E'])])
    swatch_legend(cv, 1200, 760, [('recurrence after surgery', colors['R'])])
    cv.save(os.path.join(d, 'Figure_1_Immune_Halo_Map.png'))


def a3_fig2(d):
    r = L('a3_mc')
    g = defaultdict(list)
    for x in r['mcr']:
        g[(x['ld'], x['ls'])].append(x)
    cv = PNGCanvas(1700, 820)
    ax = Axes(cv, 150, 110, 650, 520, (0.003, 3), (0, 1))
    ax.logx = True
    ax.frame('Seeding rate lambda_seed (per day)', 'Probability', 'A. Escape before surgery (dashed), recurrence (solid)')
    ax2 = Axes(cv, 1000, 110, 650, 520, (0.003, 3), (0, 1))
    ax2.logx = True
    ax2.frame('Seeding rate lambda_seed (per day)', 'Fraction of runs', 'B. Recurrence triggered by surgery')
    items = []
    for k, ld in enumerate(r['LD']):
        col = PALETTE[k]
        pre = [sum(x['pre'] > DET for x in g[(ld, ls)]) / len(g[(ld, ls)]) for ls in r['LS']]
        rec = [sum(x['fin'] > DET for x in g[(ld, ls)]) / len(g[(ld, ls)]) for ls in r['LS']]
        trig = [sum(x['fin'] > DET and x['pre'] <= DET for x in g[(ld, ls)]) / len(g[(ld, ls)]) for ls in r['LS']]
        ax.plot(r['LS'], rec, col); ax.scatter(r['LS'], rec, col)
        ax.plot(r['LS'], pre, col, 2, dash=True)
        ax2.plot(r['LS'], trig, col); ax2.scatter(r['LS'], trig, col)
        items.append((f'lambda_dist = {ld} per mm', col))
    legend(cv, 560, 700, items)
    cv.save(os.path.join(d, 'Figure_2_Monte_Carlo_Seeding.png'))


def a3_fig3(d):
    e = L('a3_example')
    cv = PNGCanvas(1700, 760)
    ax = Axes(cv, 150, 110, 650, 520, (0, 1200), (1e-4, 100), logy=True)
    ax.frame('Time (days)', 'Mass', 'A. One stochastic realisation')
    ax.plot(e['t'], clip(e['Mp'], 1e-4), C_P)
    ax.plot(e['t'], clip(e['Ms'], 1e-4), C_S)
    ax.plot(e['t'], clip(e['Mm'], 1e-4), C_M)
    ax.vmark(540, GRAY, 'surgery'); ax.hmark(DET, GRAY, '')
    legend(cv, 520, 470, [('primary', C_P), ('satellites', C_S), ('immune', C_M)])
    ax2 = Axes(cv, 1000, 110, 650, 520, (150, 560), (0.8, 3.5))
    ax2.frame('Seeding time (days)', 'Seeding radius r (mm)', 'B. Seeding events')
    ax2.scatter([s[0] for s in e['seeds']], [s[1] for s in e['seeds']], C_S, 5)
    ax2.hmark(e['events'][0]['Rex'], GRAY, 'excision boundary')
    panel_label(cv, 20, 20, 'A'); panel_label(cv, 870, 20, 'B')
    cv.save(os.path.join(d, 'Figure_3_Stochastic_Example.png'))


def a3_fig4(d):
    r = L('a3_margin')
    g = defaultdict(list)
    for x in r['mgr']:
        g[(x['ld'], x['ls'], x['mg'])].append(x)
    cv = PNGCanvas(1000, 720)
    ax = Axes(cv, 150, 110, 780, 500, (0, 3), (0, 1))
    ax.frame('Excision margin (mm)', 'Probability of recurrence', 'Recurrence probability versus margin')
    items = []
    for k, ld in enumerate((2, 4, 8)):
        for ls, dash in ((0.03, False), (0.3, True)):
            ys = [sum(x['fin'] > DET for x in g[(ld, ls, mg)]) / len(g[(ld, ls, mg)]) for mg in r['MG']]
            ax.plot(r['MG'], ys, PALETTE[k], 3, dash)
            ax.scatter(r['MG'], ys, PALETTE[k], 4)
        items.append((f'lambda_dist = {ld} per mm', PALETTE[k]))
    items += [('lambda_seed 0.03 per day', GRAY), ('lambda_seed 0.3 per day', GRAY, True)]
    legend(cv, 560, 130, items)
    cv.save(os.path.join(d, 'Figure_4_Margin.png'))


if __name__ == '__main__':
    d1, d2, d3 = outdir(1), outdir(2), outdir(3)
    for fn, d in ((a1_fig1, d1), (a1_fig2, d1), (a1_fig3, d1), (a1_fig4, d1),
                  (a2_fig1, d2), (a2_fig2, d2), (a2_fig3, d2), (a2_fig4, d2), (a2_fig5, d2),
                  (a3_fig1, d3), (a3_fig2, d3), (a3_fig3, d3), (a3_fig4, d3)):
        fn(d)
        print('ok', fn.__name__)
