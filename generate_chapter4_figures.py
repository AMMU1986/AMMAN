#!/usr/bin/env python3
"""
Figures for Chapter 4 "Experimentation" (written as code).

    python3 generate_chapter4_figures.py

Figure 4.1 - Ternary / quaternary representation of the 25 flux compositions (Table 4.2)
Figure 4.2 - Schematic of the 25 SAW beads on the API X70 plate, coloured by BI (Tables 4.2, 4.4)
Figure 4.3 - Thermophysical properties vs flux number: reported ranges and flux-specific values (Table 4.6)
Figure 4.4 - XRD patterns of Flux 2, 12, 16, 20: reported reflection positions (Table 4.7)
Figure 4.5 - FTIR spectra, set A and set B: reported band positions (Table 4.8)

Data policy: every composition, range, position and ratio is taken from the
chapter.  Individual per-flux property values, XRD intensities and full FTIR
traces are not tabulated in the chapter, so they are NOT invented: Figure 4.3
plots only the reported ranges and the flux-specific values quoted in the text,
and Figures 4.4-4.5 draw peaks/bands at the reported positions with schematic
(relative) intensities, which is stated on each figure.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))
from svgfig import Figure, Axes, col, lerp_hex  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chapter4_figures')

# Table 4.2: run: (SiO2, TiO2, CaF2, BaO, MnO, CaO, BI)
T42 = {
    1: (10.00, 18.59, 21.42, 9.99, 25.00, 8.00, 2.253), 2: (6.37, 10.17, 35.00, 8.46, 25.00, 8.00, 4.622),
    3: (8.15, 13.98, 35.00, 10.00, 17.86, 8.00, 3.201), 4: (7.94, 15.42, 30.09, 6.55, 25.00, 8.00, 2.981),
    5: (8.15, 13.98, 35.00, 10.00, 17.86, 8.00, 3.201), 6: (5.29, 20.00, 27.44, 7.28, 25.00, 8.00, 2.677),
    7: (10.00, 14.37, 25.63, 10.00, 25.00, 8.00, 2.816), 8: (7.94, 15.42, 30.09, 6.55, 25.00, 8.00, 2.981),
    9: (7.94, 15.42, 30.09, 6.55, 25.00, 8.00, 2.981), 10: (7.99, 20.00, 28.17, 10.00, 18.84, 8.00, 2.322),
    11: (10.00, 20.00, 26.73, 5.00, 23.27, 8.00, 2.100), 12: (5.02, 20.00, 33.18, 6.31, 20.48, 8.00, 2.717),
    13: (5.00, 14.38, 30.62, 10.00, 25.00, 8.00, 3.799), 14: (7.99, 20.00, 28.17, 10.00, 18.84, 8.00, 2.322),
    15: (8.79, 15.54, 35.00, 5.35, 20.32, 8.00, 2.823), 16: (10.00, 11.45, 35.00, 5.00, 23.55, 8.00, 3.337),
    17: (10.00, 19.37, 31.71, 9.51, 14.41, 8.00, 2.166), 18: (10.00, 20.00, 35.00, 10.00, 10.00, 8.00, 2.100),
    19: (10.00, 16.88, 31.33, 7.89, 18.90, 8.00, 2.461), 20: (10.00, 16.88, 31.33, 7.89, 18.90, 8.00, 2.461),
    21: (10.00, 10.00, 30.00, 10.00, 25.00, 8.00, 3.650), 22: (10.00, 10.00, 34.07, 10.00, 20.93, 8.00, 3.650),
    23: (7.97, 20.00, 35.00, 6.01, 16.02, 8.00, 2.326), 24: (5.00, 16.16, 35.00, 5.00, 23.84, 8.00, 3.395),
    25: (5.00, 20.00, 35.00, 9.30, 15.70, 8.00, 2.720),
}
IDX = {'SiO₂': 0, 'TiO₂': 1, 'CaF₂': 2, 'BaO': 3, 'MnO': 4, 'CaO': 5}
BI_MIN, BI_MAX = 2.100, 4.622
BI_STOPS = ['#2563EB', '#06B6D4', '#10B981', '#F59E0B', '#EF4444']


def bi_color(bi):
    t = (bi - BI_MIN) / (BI_MAX - BI_MIN)
    k = min(3.999, max(0, t * 4))
    i = int(k)
    return lerp_hex(BI_STOPS[i], BI_STOPS[i + 1], k - i)


def bi_bar(f, x, y, w, h=14, label=True):
    f.rect(x, y, w, h, fill=f.lingrad('#000', '#000', horizontal=True,
                                      stops=[(k / 4.0, c) for k, c in enumerate(BI_STOPS)]), rx=5, shadow=False)
    if label:
        f.text(x, y + h + 16, '%.2f' % BI_MIN, size=12, color='#475569', anchor='start')
        f.text(x + w, y + h + 16, '%.2f' % BI_MAX, size=12, color='#475569', anchor='end')
        f.text(x + w / 2, y - 6, 'Basicity index (BI, Table 4.2)', size=12.5, weight=700, color='#334155')


def panel(f, x, y, w, h, letter, title, color):
    f.rect(x, y, w, h, fill='#FFFFFF', stroke=col(color, 1), sw=2, rx=16)
    f.panel_label(x + 14, y + 12, letter, color=color)
    f.text(x + 58, y + 32, title, size=16.5, weight=700, color=col(color, 2), anchor='start')


# --------------------------------------------------------------------------- 4.1
def ternary(f, cx, cy, side, names, colors, comps):
    h = side * math.sqrt(3) / 2
    A = (cx, cy - 2 * h / 3)
    B = (cx - side / 2, cy + h / 3)
    Cc = (cx + side / 2, cy + h / 3)
    f.polygon([A, B, Cc], fill=f.lingrad('#FFFFFF', '#F1F5F9'), stroke='#334155', sw=2)
    # grid at 20 %
    for k in range(1, 5):
        t = k / 5.0
        for P, Q, R in ((A, B, Cc), (B, Cc, A), (Cc, A, B)):
            p1 = (P[0] + (Q[0] - P[0]) * t, P[1] + (Q[1] - P[1]) * t)
            p2 = (P[0] + (R[0] - P[0]) * t, P[1] + (R[1] - P[1]) * t)
            f.line(p1[0], p1[1], p2[0], p2[1], color='#CBD5E1', sw=1, dash='3,4')
    for V, n, c, dy, anc in ((A, names[0], colors[0], -14, 'middle'), (B, names[1], colors[1], 26, 'middle'),
                             (Cc, names[2], colors[2], 26, 'middle')):
        f.circle(V[0], V[1], 7, fill=col(c), stroke='#FFFFFF', sw=2, shadow=True)
        f.text(V[0], V[1] + dy, n, size=15, weight=800, color=col(c, 2), anchor=anc)
    pts = []
    for run, (a, b, c, bi) in comps.items():
        s = a + b + c
        a, b, c = a / s, b / s, c / s
        x = a * A[0] + b * B[0] + c * Cc[0]
        y = a * A[1] + b * B[1] + c * Cc[1]
        pts.append((x, y, bi))
    # design-region hull
    hull = convex_hull([(p[0], p[1]) for p in pts])
    f.polygon(hull, fill=col('violet'), opacity=0.12, stroke=col('violet'), sw=1.5)
    for x, y, bi in sorted(pts, key=lambda p: p[2]):
        f.circle(x, y, 6, fill=bi_color(bi), stroke='#FFFFFF', sw=1.5, shadow=True)
    return A, B, Cc


def convex_hull(points):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in points))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def comps_for(keys):
    out = {}
    for run, row in T42.items():
        out[run] = tuple(sum(row[IDX[k]] for k in grp) for grp in keys) + (row[6],)
    return out


def fig41():
    f = Figure(1500, 1000, title='Ternary and Quaternary Representation of the Flux Design Space',
               subtitle='The 25 flux compositions of Table 4.2, normalised to the components of each diagram '
                        'and coloured by basicity index')
    specs = [('a', 'SiO₂–CaO–CaF₂', [['SiO₂'], ['CaO'], ['CaF₂']], ['SiO₂', 'CaO', 'CaF₂'],
              ['blue', 'amber', 'emerald']),
             ('b', 'SiO₂–MnO–TiO₂', [['SiO₂'], ['MnO'], ['TiO₂']], ['SiO₂', 'MnO', 'TiO₂'],
              ['blue', 'rose', 'violet']),
             ('c', 'BaO–SiO₂–CaF₂', [['BaO'], ['SiO₂'], ['CaF₂']], ['BaO', 'SiO₂', 'CaF₂'],
              ['orange', 'blue', 'emerald'])]
    pos = [(20, 95), (515, 95), (1010, 95)]
    for (L, title, keys, names, colors), (px, py) in zip(specs, pos):
        panel(f, px, py, 470, 420, L, title, colors[0] if L != 'a' else 'blue')
        ternary(f, px + 235, py + 255, 330, names, colors, comps_for(keys))
    # (d) quaternary framework: tetrahedron projection
    panel(f, 20, 530, 900, 440, 'd', 'Quaternary framework: SiO₂ – TiO₂ – CaF₂ – basic oxides (MnO + BaO + CaO)',
          'teal')
    V = {'SiO₂': (300, 620), 'TiO₂': (110, 900), 'CaF₂': (560, 930), 'MnO + BaO + CaO': (760, 760)}
    vc = {'SiO₂': 'blue', 'TiO₂': 'violet', 'CaF₂': 'emerald', 'MnO + BaO + CaO': 'rose'}
    keys = list(V)
    back = [('SiO₂', 'TiO₂'), ('SiO₂', 'CaF₂'), ('TiO₂', 'CaF₂'), ('CaF₂', 'MnO + BaO + CaO'),
            ('SiO₂', 'MnO + BaO + CaO')]
    f.polygon([V['SiO₂'], V['TiO₂'], V['CaF₂']], fill=col('teal', 1), opacity=0.55)
    f.polygon([V['SiO₂'], V['CaF₂'], V['MnO + BaO + CaO']], fill=col('emerald', 1), opacity=0.45)
    for a, b in back:
        f.line(V[a][0], V[a][1], V[b][0], V[b][1], color='#334155', sw=2)
    f.line(V['TiO₂'][0], V['TiO₂'][1], V['MnO + BaO + CaO'][0], V['MnO + BaO + CaO'][1], color='#64748B', sw=1.8,
           dash='7,6')
    groups = [['SiO₂'], ['TiO₂'], ['CaF₂'], ['MnO', 'BaO', 'CaO']]
    pts = []
    for run, row in T42.items():
        w = [sum(row[IDX[k]] for k in g) for g in groups]
        s = sum(w)
        w = [v / s for v in w]
        x = sum(wi * V[k][0] for wi, k in zip(w, keys))
        y = sum(wi * V[k][1] for wi, k in zip(w, keys))
        pts.append((x, y, row[6], run))
    for x, y, bi, run in sorted(pts, key=lambda p: p[2]):
        f.circle(x, y, 7, fill=bi_color(bi), stroke='#FFFFFF', sw=1.5, shadow=True)
    for k in keys:
        x, y = V[k]
        f.circle(x, y, 8, fill=col(vc[k]), stroke='#FFFFFF', sw=2, shadow=True)
        if k == 'MnO + BaO + CaO':
            f.text(x + 14, y + 26, k, size=15, weight=800, color=col(vc[k], 2), anchor='start')
            continue
        dy = -14 if k == 'SiO₂' else 28
        f.text(x, y + dy, k, size=15, weight=800, color=col(vc[k], 2))
    f.html(600, 600, 300, 120, 'Each point is one flux of Table 4.2, located by its four normalised component '
           'fractions; CaO is fixed at 8.00 g in every run.', size=12.5, align='left', color='#334155')
    # legend / notes
    f.rect(940, 530, 540, 440, fill=f.lingrad('#FFFFFF', '#F8FAFC'), stroke='#E2E8F0', sw=2, rx=16)
    f.text(1210, 570, 'How to read the diagrams', size=17, weight=800, color='#334155')
    bi_bar(f, 990, 615, 440)
    f.legend(990, 690, [('Flux composition (Table 4.2 run)', '#475569', 'dot'),
                        ('Envelope of the 25 designs', 'violet')], size=13.5, gap=28)
    f.html(980, 750, 470, 210,
           '<div style="text-align:left">Corners are the pure components; grid lines are at 20% intervals. '
           'Compositions are re-normalised to the components shown, so each diagram is a projection of the '
           'seven-component design.<br/><br/>Duplicated runs (3/5, 4/8/9, 10/14, 19/20) plot on the same point. '
           'Phase-field boundaries are discussed in the text with refs [29, 31, 33] and are not redrawn here.</div>',
           size=13, color='#334155')
    f.save(os.path.join(OUT, 'Figure_4_1_Ternary_Phase_Diagrams.png'))


# --------------------------------------------------------------------------- 4.2
def fig42():
    f = Figure(1500, 880, title='Twenty-Five Multi-Pass SAW Beads on API X70 Pipeline Steel',
               subtitle='Bead-on-plate layout (schematic, not to scale); each bead is coloured by the basicity '
                        'index of its flux')
    # plate in perspective
    x0, y0, W, H, sk = 90, 140, 960, 640, 60
    f.polygon([(x0 + sk, y0), (x0 + W + sk, y0), (x0 + W, y0 + H), (x0, y0 + H)],
              fill=f.lingrad('#E2E8F0', '#94A3B8'), stroke='#475569', sw=2, shadow=True)
    f.polygon([(x0, y0 + H), (x0 + W, y0 + H), (x0 + W, y0 + H + 26), (x0, y0 + H + 26)],
              fill='#64748B', stroke='#334155', sw=1.5)
    f.polygon([(x0 + W, y0 + H), (x0 + W + sk, y0), (x0 + W + sk, y0 + 26), (x0 + W, y0 + H + 26)],
              fill='#475569', stroke='#334155', sw=1.5)
    f.text(x0 + W / 2 + 30, y0 + H + 58, 'API X70 plate · 16 mm thick · no edge preparation', size=14,
           weight=700, color='#334155')
    # beads: 5 rows x 5
    rows, cols = 5, 5
    for r in range(rows):
        for c in range(cols):
            run = r * cols + c + 1
            bi = T42[run][6]
            t = (r + 0.5) / rows
            yy = y0 + 40 + r * (H - 80) / (rows - 1) * 0.98
            off = sk * (1 - (yy - y0) / H)
            bx = x0 + off + 40 + c * (W - 80) / cols
            bw = (W - 80) / cols - 34
            colr = bi_color(bi)
            f.rect(bx, yy - 22, bw, 44, fill=f.lingrad(lerp_hex(colr, '#FFFFFF', 0.35), lerp_hex(colr, '#000000', 0.25)),
                   rx=22, stroke=lerp_hex(colr, '#000000', 0.35), sw=1.5)
            for k in range(1, 9):
                xx = bx + k * bw / 9
                f.path('M%.1f,%.1f q6,22 0,44' % (xx, yy - 22), stroke='#FFFFFF', sw=1.2, opacity=0.45)
            f.circle(bx - 2, yy, 13, fill='#0F172A', stroke='#FFFFFF', sw=2)
            f.text(bx - 2, yy + 4.5, str(run), size=12, weight=800, color='#FFFFFF')
    f.arrow(x0 + sk + 300, y0 - 22, x0 + sk + 560, y0 - 22, color='#0F172A', sw=2.5)
    f.text(x0 + sk + 290, y0 - 16, 'welding direction', size=13.5, weight=700, color='#334155', anchor='end')
    # side panel: conditions
    f.card(1140, 140, 340, 290, 'SAW conditions (Table 4.4)',
           '<div style="text-align:left;line-height:1.55">'
           '<b>Process:</b> single-wire SAW, flat<br/><b>Current:</b> 230 A<br/><b>Voltage:</b> 25 V<br/>'
           '<b>Speed:</b> 8 in/min (3.39 mm/s)<br/><b>Heat input:</b> about 1.27 kJ/mm<br/>'
           '<b>Wire:</b> EA2TiB, 2.4 mm<br/><b>Passes per bead:</b> 5<br/>'
           '<b>Interpass:</b> 120–150 °C<br/><b>Beads:</b> 25 (one per flux)</div>',
           color='indigo', title_size=16, body_size=14, header_h=44, valign='top')
    bi_bar(f, 1150, 500, 320)
    f.html(1140, 555, 340, 110, 'Bead numbers correspond to the runs (flux numbers) of Table 4.2; '
           'the layout order is illustrative.', size=12.5, color='#475569', italic=True)
    f.save(os.path.join(OUT, 'Figure_4_2_SAW_Bead_Plate.png'))


# --------------------------------------------------------------------------- 4.3
def prop_panel(f, x, y, w, h, letter, title, color, ylim, yticks, ylabel, rng, mean=None, groups=(),
               bars=(), points=(), fmt='{:g}', point_above=False):
    panel(f, x, y, w, h, letter, title, color)
    ax = Axes(f, x + 90, y + 60, w - 120, h - 130, (0.3, 25.7), ylim, xlabel='Flux number',
              ylabel=ylabel, yticks=yticks, xticks=[1, 5, 10, 15, 20, 25], ytickfmt=fmt)
    for g0, g1, gc, glab in groups:
        f.rect(ax.px(g0 - 0.45), ax.y, ax.px(g1 + 0.45) - ax.px(g0 - 0.45), ax.h, fill=col(gc), opacity=0.09,
               rx=0, shadow=False)
        f.text((ax.px(g0 - 0.45) + ax.px(g1 + 0.45)) / 2, ax.y + 16, glab, size=11.5, weight=700, color=col(gc, 2))
    ax.band(rng[0], rng[1], color=color, opacity=0.12)
    ax.hline(rng[0], color=color, sw=1.6, dash='6,4')
    ax.hline(rng[1], color=color, sw=1.6, dash='6,4')
    f.text(ax.x + 8 if point_above else ax.x + ax.w - 6, ax.py(rng[1]) - 7, 'max ' + fmt.format(rng[1]),
           size=12, weight=700, color=col(color, 2), anchor='start' if point_above else 'end')
    f.text(ax.x + ax.w - 6, ax.py(rng[0]) + 17, 'min ' + fmt.format(rng[0]), size=12, weight=700,
           color=col(color, 2), anchor='end')
    if mean:
        ax.hline(mean[0], color='slate', sw=2, dash=None)
        ax.band(mean[0] - mean[1], mean[0] + mean[1], color='slate', opacity=0.06)
        f.text(ax.x + 8, ax.py(mean[0]) - 7, 'mean %.2f ± %.2f' % mean, size=12, weight=700, color='#334155',
               anchor='start')
    for runs, lo, hi, bc in bars:
        for r in runs:
            xx = ax.px(r)
            f.rect(xx - 7, ax.py(hi), 14, max(3, ax.py(lo) - ax.py(hi)), fill=f.vivid_for(bc), rx=5,
                   shadow='softshadow')
            f.text(xx, ax.py(lo) + 16, str(r), size=11, weight=800, color=col(bc, 2))
    for r, v, pc, lab in points:
        f.circle(ax.px(r), ax.py(v), 7, fill=col(pc), stroke='#FFFFFF', sw=2, shadow=True)
        if point_above:
            f.line(ax.px(r), ax.py(v) - 8, ax.px(r), ax.py(v) - 22, color=col(pc, 2), sw=1.4)
            f.text(ax.px(r) + 6, ax.py(v) - 28, lab, size=12, weight=800, color=col(pc, 2), anchor='end')
            continue
        f.text(ax.px(r) - 12, ax.py(v) + 22, lab, size=12, weight=800, color=col(pc, 2), anchor='end')
    return ax


def fig43():
    f = Figure(1500, 1045, title='Thermophysical Properties of the 25 Fluxes',
               subtitle='Reported ranges (shaded) and the flux-specific values quoted in the text (bars / points); '
                        'data: Table 4.6')
    W, H = 720, 430
    prop_panel(f, 20, 95, W, H, 'a', 'Tapped density, ρ', 'blue', (1.36, 1.58), [1.36, 1.40, 1.44, 1.48, 1.52, 1.56],
               'Density (g/cm³)', (1.40, 1.54), mean=(1.48, 0.04),
               groups=[(1, 6, 'amber', 'lowest: 1–6'), (14, 16, 'emerald', 'highest'),
                       (23, 25, 'emerald', 'highest')], fmt='{:.2f}')
    prop_panel(f, 760, 95, W, H, 'b', 'Thermal conductivity, k', 'orange', (0.30, 0.56),
               [0.30, 0.35, 0.40, 0.45, 0.50, 0.55], 'Conductivity (W/m·K)', (0.34, 0.52),
               groups=[(1, 6, 'sky', 'lower: silica-based 1–6')], fmt='{:.2f}')
    prop_panel(f, 20, 545, W, H, 'c', 'Specific (volumetric) heat capacity, ρ·cₚ', 'emerald', (0.85, 1.25),
               [0.85, 0.95, 1.05, 1.15, 1.25], 'ρ·cₚ (MJ/m³·K)', (0.902, 1.192),
               bars=[((1, 6, 7, 11), 0.90, 0.98, 'blue'), ((14, 19, 21), 1.05, 1.19, 'rose')],
               points=[(25, 1.192, 'rose', 'Flux 25: 1.192')], fmt='{:.3g}', point_above=True)
    prop_panel(f, 760, 545, W, H, 'd', 'Thermal diffusivity, α', 'violet', (0.17, 0.39),
               [0.18, 0.22, 0.26, 0.30, 0.34, 0.38], 'Diffusivity (mm²/s)', (0.202, 0.351),
               bars=[((3, 22), 0.202, 0.215, 'cyan'), ((2, 16), 0.215, 0.245, 'emerald'),
                     ((8,), 0.335, 0.351, 'amber')],
               points=[(20, 0.335, 'amber', 'Flux 20: 0.335')], fmt='{:.3g}')
    f.legend(150, 1022, [('Shaded band: reported range over 25 fluxes', 'slate'), ('Set A (Flux 1, 6, 7, 11): 0.90–0.98', 'blue'),
                              ('Set B (Flux 14, 19, 21, 25): 1.05–1.19', 'rose'),
                              ('Flux-specific range from text', 'amber')], cols=4, col_w=320, size=12.5)
    f.save(os.path.join(OUT, 'Figure_4_3_Thermophysical_Properties.png'))


# --------------------------------------------------------------------------- 4.4
FLUORITE = [(28.3, '(111)'), (32.2, '(200)'), (47.0, '(220)')]
RUTILE = [27.4, 36.1, 54.4]
MNO = [30.1, 50.5]


def xrd_panel(f, x, y, w, h, letter, title, color, peaks, note):
    panel(f, x, y, w, h, letter, title, color)
    ax = Axes(f, x + 70, y + 60, w - 100, h - 125, (20, 60), (0, 1.2), xlabel='2θ (degrees)',
              ylabel='Intensity (relative, schematic)', yticks=[], xticks=[20, 30, 40, 50, 60], grid=False)
    xs = [20 + i * 0.05 for i in range(801)]
    ys = []
    for xv in xs:
        v = 0.05 + 0.03 * math.exp(-((xv - 30) / 9) ** 2)
        for p, hgt, wid, _, _ in peaks:
            v += hgt * math.exp(-0.5 * ((xv - p) / wid) ** 2)
        ys.append(v)
    ax.area(xs, [0] * len(xs), ys, color=color, opacity=0.18)
    ax.line(xs, ys, color=color, sw=2.4, marker=False)
    for p, hgt, wid, sym, pc in peaks:
        f.text(ax.px(p), ax.py(hgt + 0.10) - 6, sym, size=13, weight=800, color=col(pc, 2))
    f.text(ax.x + ax.w - 8, ax.y + 18, note, size=12, color='#475569', anchor='end', italic=True)


def fig44():
    f = Figure(1500, 960, title='XRD Patterns of Selected Fluxes',
               subtitle='Peaks drawn at the reflection positions reported in Table 4.7; intensities and widths '
                        'are schematic')
    W, H = 720, 400
    xrd_panel(f, 20, 95, W, H, 'a', 'Flux 2 (35% CaF₂, 25% MnO)', 'emerald',
              [(28.3, 1.0, 0.18, 'F (111)', 'emerald'), (32.2, 0.55, 0.18, 'F (200)', 'emerald'),
               (47.0, 0.75, 0.18, 'F (220)', 'emerald')], 'strong, sharp fluorite')
    xrd_panel(f, 760, 95, W, H, 'b', 'Flux 12 (20.00 g TiO₂)', 'violet',
              [(28.3, 0.80, 0.22, 'F', 'emerald'), (32.2, 0.42, 0.22, 'F', 'emerald'), (47.0, 0.6, 0.22, 'F', 'emerald')]
              + [(p, 0.62, 0.2, 'R', 'violet') for p in RUTILE]
              + [(p, 0.22, 0.25, 'M', 'rose') for p in MNO], 'fluorite + rutile + MnO')
    xrd_panel(f, 20, 515, W, H, 'c', 'Flux 16 (35.00 g CaF₂)', 'teal',
              [(28.3, 0.95, 0.17, 'F', 'emerald'), (32.2, 0.5, 0.17, 'F', 'emerald'),
               (47.0, 0.7, 0.17, 'F', 'emerald')], 'high fluorite crystallinity')
    xrd_panel(f, 760, 515, W, H, 'd', 'Flux 20 (31.3% CaF₂)', 'rose',
              [(28.3, 0.5, 0.25, 'F', 'emerald'), (32.2, 0.28, 0.25, 'F', 'emerald'),
               (47.0, 0.38, 0.25, 'F', 'emerald')] + [(p, 0.55, 0.25, 'M', 'rose') for p in MNO],
              'weaker fluorite, MnO peaks')
    f.legend(330, 945, [('F = fluorite, CaF₂: 28.3°, 32.2°, 47.0°', 'emerald', 'dot'), ('R = rutile, TiO₂: 27.4°, 36.1°, 54.4°', 'violet', 'dot'),
                        ('M = MnO: 30.1°, 50.5°', 'rose', 'dot')], cols=3, col_w=330, size=13)
    f.save(os.path.join(OUT, 'Figure_4_4_XRD_Patterns.png'))


# --------------------------------------------------------------------------- 4.5
def ftir_trace(sio, ratio):
    xs = [4000 - i * 5 for i in range(701)]
    ys = []
    for x in xs:
        a = 0.0
        a += 0.22 * math.exp(-0.5 * ((x - 3400) / 170) ** 2)          # O-H
        a += 0.62 * math.exp(-0.5 * ((x - sio) / 45) ** 2)            # Si-O-Si
        a += 0.62 * ratio * math.exp(-0.5 * ((x - 950) / 22) ** 2)    # NBO shoulder
        a += 0.30 * math.exp(-0.5 * ((x - 600) / 90) ** 2)            # Ti-O / Mn-O lattice
        ys.append(100 - 80 * min(1.0, a))
    return xs, ys


def ftir_panel(f, x, y, w, h, letter, title, color, sio, rlo, rhi, fluxes, hc):
    panel(f, x, y, w, h, letter, title, color)
    ax = Axes(f, x + 80, y + 60, w - 110, h - 130, (4000, 500), (0, 108), xlabel='Wavenumber (cm⁻¹)',
              ylabel='Transmittance (%, schematic)', yticks=[0, 20, 40, 60, 80, 100],
              xticks=[4000, 3500, 3000, 2500, 2000, 1500, 1000, 500])
    bands = [(3600, 3200, 'sky', 'O–H ≈3400'), (1120, 1070, 'blue', 'Si–O–Si'), (965, 935, 'rose', 'NBO ≈950'),
             (800, 400, 'amber', 'Ti–O / Mn–O')]
    for b0, b1, bc, lab in bands:
        x0, x1 = ax.px(b0), ax.px(max(b1, 500))
        f.rect(x0, ax.y, x1 - x0, ax.h, fill=col(bc), opacity=0.14, rx=0, shadow=False)
    xs, ys = ftir_trace(sio, (rlo + rhi) / 2)
    ax.line(xs, ys, color=color, sw=2.8, marker=False)
    f.text(ax.px(3400), ax.y + 18, 'O–H ≈3400', size=12, weight=700, color=col('sky', 2))
    f.text(ax.px(1250), ax.y + 18, 'Si–O–Si ≈%d' % sio, size=12, weight=700, color=col('blue', 2), anchor='end')
    f.text(ax.px(950), ax.py(18), 'NBO ≈950', size=12, weight=700, color=col('rose', 2))
    f.text(ax.px(600), ax.py(8), 'Ti–O / Mn–O', size=12, weight=700, color=col('amber', 2))
    f.soft(ax.px(3150), ax.py(52), 300, 96,
           '<div style="text-align:left"><b>Fluxes %s</b><br/>I₉₅₀/I₁₁₀₀ = %.2f–%.2f<br/>ρ·cₚ = %s MJ/m³·K</div>'
           % (fluxes, rlo, rhi, hc), color=color, size=13.5, weight=500, align='left')


def fig45():
    f = Figure(1500, 620, title='FTIR Spectra of the Flux Sets',
               subtitle='Schematic transmittance traces built from the band positions and intensity ratios of '
                        'Table 4.8 (scan range 4000–500 cm⁻¹)')
    ftir_panel(f, 20, 95, 720, 480, 'A', 'Set A: Flux 1, 6, 7, 11', 'blue', 1105, 0.15, 0.25, '1, 6, 7, 11',
               '0.90–0.98')
    ftir_panel(f, 760, 95, 720, 480, 'B', 'Set B: Flux 14, 19, 21, 25', 'rose', 1085, 0.30, 0.45,
               '14, 19, 21, 25', '1.05–1.19')
    f.footnote('One representative trace per set; the stronger 950 cm⁻¹ shoulder and lower Si–O–Si position in '
               'set B indicate a more depolymerised silicate network.', y=600)
    f.save(os.path.join(OUT, 'Figure_4_5_FTIR_Spectra.png'))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    which = sys.argv[1:] or ['41', '42', '43', '44', '45']
    for w in which:
        globals()['fig' + w]()
