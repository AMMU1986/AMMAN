#!/usr/bin/env python3
"""
Figures for Chapter 16 "AI-Assisted Design of Nanomaterials" (written as code).

    python3 generate_ch16_figures.py

Figure 1 - AI-assisted nanomaterial design workflow (schematic cycle)
Figure 2 - ML model performance: parity, learning curves, radar (illustrative)
Figure 3 - cGAN inverse design: architecture, morphologies, distributions
Figure 4 - Reinforcement learning: loop, convergence, Pareto front (illustrative)
Figure 5 - High-throughput screening funnel, active learning loop, sampling efficiency
Figure 6 - AI-designed nanomaterials for forensic applications (four panels)

The chapter is a review and reports no raw data for these plots.  Data-like
panels are therefore drawn as *illustrative* curves generated from simple,
deterministic functions (fixed random seed) and are labelled as such on the
figure; the only quantitative anchors used are values stated in the text
(Table 2 XGBoost band-gap MAE 0.28 eV; 10^6 -> 10 screening funnel; 3-5x
fewer experiments; RL 2-5x better than random; SERS EF 10^6-10^10).
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))
from svgfig import Figure, Axes, col, lerp_hex  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
ILLUS = 'Illustrative schematic of typical behaviour reported in the literature, not fitted to new data.'


def panel(f, x, y, w, h, letter, title, color):
    f.rect(x, y, w, h, fill='#FFFFFF', stroke=col(color, 1), sw=2, rx=16)
    f.panel_label(x + 14, y + 12, letter, color=color)
    f.text(x + 58, y + 32, title, size=16.5, weight=700, color=col(color, 2), anchor='start')


# --------------------------------------------------------------------------- Figure 1
def fig1():
    f = Figure(1500, 860, title='AI-Assisted Nanomaterial Design Workflow',
               subtitle='An iterative, closed-loop cycle from data to validated material')
    cx, cy, rx, ry = 750, 470, 520, 270
    stages = [
        ('1  Data collection', 'Experimental literature, Materials Project, OQMD, AFLOW; curation &amp; FAIR metadata', 'blue'),
        ('2  Feature engineering', 'Compositional, structural, graph and image descriptors', 'cyan'),
        ('3  Model training', 'RF, XGBoost, GNN, CNN; cross-validation &amp; model selection', 'emerald'),
        ('4  Property prediction', 'Virtual screening of candidates with uncertainty estimates', 'amber'),
        ('5  Inverse design', 'VAE, GAN, diffusion, RL and Bayesian optimization', 'rose'),
        ('6  Experimental validation', 'Synthesis &amp; characterization of top candidates', 'violet'),
    ]
    n = len(stages)
    pos = []
    for i in range(n):
        a = -math.pi / 2 + i * 2 * math.pi / n
        pos.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    W, H = 300, 118
    # ring
    f.ellipse(cx, cy, rx, ry, fill='none', stroke=col('indigo', 1), sw=26)
    for i in range(n):
        x1, y1 = pos[i]
        x2, y2 = pos[(i + 1) % n]
        if i == n - 1:
            continue
        a1 = -math.pi / 2 + (i + 0.30) * 2 * math.pi / n
        a2 = -math.pi / 2 + (i + 0.70) * 2 * math.pi / n
        f.arrow(cx + rx * math.cos(a1), cy + ry * math.sin(a1), cx + rx * math.cos(a2),
                cy + ry * math.sin(a2), color=stages[i][2], sw=5, curve=-22 if i in (0, 1, 2) else -22)
    # feedback arrow 6 -> 1 (dashed)
    a1 = -math.pi / 2 + (5 + 0.30) * 2 * math.pi / n
    a2 = -math.pi / 2 + (5 + 0.70) * 2 * math.pi / n
    f.arrow(cx + rx * math.cos(a1), cy + ry * math.sin(a1), cx + rx * math.cos(a2),
            cy + ry * math.sin(a2), color='fuchsia', sw=5, dash='10,7', curve=-22)
    f.pill(cx - 330, cy - 280, 'Active-learning feedback', color='fuchsia', size=14)
    for (x, y), (t, b, c) in zip(pos, stages):
        f.card(x - W / 2, y - H / 2, W, H, t, b, color=c, title_size=16, body_size=13, header_h=38)
    # centre hub
    f.circle(cx, cy, 128, fill=f.radgrad('#818CF8', '#4F46E5'), shadow=True)
    f.html(cx - 120, cy - 70, 240, 140, '<div><b style="font-size:21px">AI-assisted<br/>nanomaterial<br/>design</b>'
           '<div style="font-size:13px;margin-top:6px;opacity:0.9">models improve with every iteration</div></div>',
           color='#FFFFFF', size=16)
    f.footnote('Stages follow the six-step cycle described in Section 1; validated results re-enter the data '
               'pool, refining models through active learning.', y=840)
    f.save(os.path.join(OUT, 'Figure_1.png'))


# --------------------------------------------------------------------------- Figure 2
def radar(f, cx, cy, R, axes_labels, series, levels=4):
    k = len(axes_labels)
    ang = [-math.pi / 2 + i * 2 * math.pi / k for i in range(k)]
    for L in range(1, levels + 1):
        r = R * L / levels
        f.polygon([(cx + r * math.cos(a), cy + r * math.sin(a)) for a in ang],
                  fill='#F8FAFC' if L % 2 else '#FFFFFF', stroke='#CBD5E1', sw=1)
    for a, lab in zip(ang, axes_labels):
        f.line(cx, cy, cx + R * math.cos(a), cy + R * math.sin(a), color='#CBD5E1', sw=1)
        lx, ly = cx + (R + 30) * math.cos(a), cy + (R + 22) * math.sin(a)
        anchor = 'middle' if abs(math.cos(a)) < 0.3 else ('start' if math.cos(a) > 0 else 'end')
        parts = lab.split('\n')
        for k, part in enumerate(parts):
            f.text(lx, ly + 5 + (k - (len(parts) - 1) / 2.0) * 16, part, size=12.5, weight=600,
                   color='#334155', anchor=anchor)
    for vals, c in series:
        pts = [(cx + R * v * math.cos(a), cy + R * v * math.sin(a)) for v, a in zip(vals, ang)]
        f.polygon(pts, fill=col(c), opacity=0.18)
        f.polygon(pts, fill='none', stroke=col(c), sw=3)
        for p in pts:
            f.circle(p[0], p[1], 4.5, fill=col(c), stroke='#FFFFFF', sw=1.5)


def fig2():
    random.seed(16)
    f = Figure(1500, 660, title='Performance Comparison of ML Models for Nanomaterial Property Prediction',
               subtitle='Random forest (RF), graph neural network (GNN) and XGBoost')
    models = [('RF', 'orange', 0.45), ('GNN', 'violet', 0.30), ('XGBoost', 'emerald', 0.35)]
    # (a) parity
    panel(f, 20, 100, 475, 510, 'a', 'Parity plot: band gap', 'blue')
    ax = Axes(f, 95, 160, 370, 370, (0, 6.5), (0, 6.5), xlabel='DFT / experimental band gap (eV)',
              ylabel='Predicted band gap (eV)', yticks=[0, 1, 2, 3, 4, 5, 6], xticks=[0, 1, 2, 3, 4, 5, 6])
    f.polygon([(ax.px(0), ax.py(0.28)), (ax.px(6.5 - 0.28), ax.py(6.5)), (ax.px(6.5), ax.py(6.5)),
               (ax.px(6.5), ax.py(6.5 - 0.28)), (ax.px(0.28), ax.py(0)), (ax.px(0), ax.py(0))],
              fill=col('emerald'), opacity=0.12)
    f.line(ax.px(0), ax.py(0), ax.px(6.5), ax.py(6.5), color='#334155', sw=2, dash='6,5')
    for name, c, s in models:
        for _ in range(32):
            t = random.uniform(0.4, 6.0)
            p = min(6.4, max(0.05, t + random.gauss(0, s)))
            f.circle(ax.px(t), ax.py(p), 5, fill=col(c), stroke='#FFFFFF', sw=1.2, opacity=0.85)
    f.legend(115, 190, [(m, c, 'dot') for m, c, _ in models], size=13, gap=22)
    f.pill(ax.px(4.6), ax.py(0.9), 'XGBoost MAE 0.28 eV (Table 2)', color='emerald', size=12.5)

    # (b) learning curves
    panel(f, 512, 100, 475, 510, 'b', 'Learning curves', 'emerald')
    ax = Axes(f, 590, 160, 370, 370, (2, 5), (0, 1.1), xlabel='Training-set size (samples, log scale)',
              ylabel='Relative MAE (normalised)', yticks=[0, 0.25, 0.5, 0.75, 1.0],
              xticks=[2, 3, 4, 5], xticklabels=['10²', '10³', '10⁴', '10⁵'])
    xs = [2 + i * 0.25 for i in range(13)]
    curves = [('RF', 'orange', 0.55, 0.40), ('XGBoost', 'emerald', 0.36, 0.42), ('GNN', 'violet', 0.12, 0.62)]
    for name, c, floor, slope in curves:
        ys = [floor + (1 - floor) * 10 ** (-slope * (x - 2)) for x in xs]
        ax.line(xs, ys, color=c, sw=3.5, smooth=True, marker=False)
        ax.line([xs[0], xs[6], xs[-1]], [ys[0], ys[6], ys[-1]], color=c, sw=0, marker=True, r=5)
        f.text(ax.px(5) - 4, ax.py(ys[-1]) - 9, name, size=13, weight=800, color=col(c, 2), anchor='end')
    f.html(600, 170, 230, 60, 'GNNs learn their own representation and keep improving with more data',
           size=12, color=col('violet', 2), align='left', italic=True)

    # (c) radar
    panel(f, 1004, 100, 476, 510, 'c', 'Accuracy across six properties', 'violet')
    labels = ['Band gap', 'Formation\nenergy', 'Plasmon\nresonance', 'Particle size',
              'Catalytic\nactivity', 'Elastic\nmodulus']
    radar(f, 1242, 380, 135, labels, [([0.70, 0.66, 0.78, 0.74, 0.62, 0.64], 'orange'),
                                      ([0.80, 0.74, 0.70, 0.66, 0.72, 0.76], 'emerald'),
                                      ([0.86, 0.92, 0.62, 0.58, 0.84, 0.90], 'violet')])
    f.legend(1060, 585, [('RF', 'orange'), ('XGBoost', 'emerald'), ('GNN', 'violet')], cols=3, col_w=120, size=13)
    f.text(1242, 160, 'outer ring = higher relative accuracy', size=12, color='#64748B', italic=True)
    f.footnote(ILLUS + ' Benchmarks with sources are listed in Table 2.', y=640)
    f.save(os.path.join(OUT, 'Figure_2.png'))


# --------------------------------------------------------------------------- Figure 3
def particle(f, kind, cx, cy, s, c, jitter=0.0):
    base, light, dark = col(c), col(c, 1), col(c, 2)
    g = f.radgrad(light, base)
    if kind == 'sphere':
        f.circle(cx, cy, s, fill=g, stroke=dark, sw=1.5, shadow=True)
    elif kind == 'rod':
        f.rect(cx - s * 1.5, cy - s * 0.5, s * 3, s, fill=g, stroke=dark, sw=1.5, rx=s * 0.5)
    elif kind == 'cube':
        d = s * 0.45
        f.polygon([(cx - s, cy - s + d), (cx - s + d, cy - s), (cx + s, cy - s), (cx + s - d, cy - s + d)],
                  fill=light, stroke=dark, sw=1.5)
        f.polygon([(cx + s - d, cy - s + d), (cx + s, cy - s), (cx + s, cy + s - d), (cx + s - d, cy + s)],
                  fill=dark, stroke=dark, sw=1.5, opacity=0.8)
        f.rect(cx - s, cy - s + d, 2 * s - d, 2 * s - d, fill=g, stroke=dark, sw=1.5, rx=3, shadow=False)
    elif kind == 'triangle':
        f.polygon([(cx, cy - s * 1.1), (cx + s * 1.1, cy + s * 0.8), (cx - s * 1.1, cy + s * 0.8)],
                  fill=g, stroke=dark, sw=1.5, shadow=True)
    elif kind == 'star':
        pts = []
        for i in range(16):
            r = s * (1.15 if i % 2 == 0 else 0.55) * (1 + jitter * math.sin(i * 1.7))
            a = i * math.pi / 8
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        f.polygon(pts, fill=g, stroke=dark, sw=1.5, shadow=True)
    elif kind == 'coreshell':
        f.circle(cx, cy, s, fill=col(c, 1), stroke=base, sw=3, shadow=True)
        f.circle(cx, cy, s * 0.55, fill=f.radgrad('#FDE68A', '#D97706'), stroke='#92400E', sw=1.2)


def gauss(x, m, s):
    return math.exp(-0.5 * ((x - m) / s) ** 2)


def fig3():
    f = Figure(1500, 680, title='Conditional GAN for Nanomaterial Inverse Design',
               subtitle='Generator proposes structures for a target property; discriminator judges realism')
    # (a) architecture
    panel(f, 20, 100, 620, 540, 'a', 'cGAN framework', 'rose')
    f.tile(45, 170, 150, 64, 'Noise <i>z</i>', color='slate', size=16)
    f.tile(45, 260, 150, 64, 'Condition <i>c</i><br/><span style="font-size:12px">target property</span>',
           color='amber', size=15)
    f.card(240, 190, 150, 120, 'Generator G', 'maps (z, c) to a candidate structure', color='rose',
           title_size=15, body_size=12.5)
    f.arrow(197, 202, 238, 232, color='slate', sw=3)
    f.arrow(197, 292, 238, 268, color='amber', sw=3)
    f.soft(425, 190, 190, 120, '<div><b>Generated</b><br/>structure G(z, c)</div>', color='rose', size=14)
    f.arrow(392, 250, 423, 250, color='rose', sw=3)
    f.soft(45, 430, 190, 110, '<div><b>Real structures</b><br/>databases &amp; microscopy</div>',
           color='blue', size=14)
    f.card(300, 420, 160, 130, 'Discriminator D', 'real or generated? (conditioned on c)', color='indigo',
           title_size=15, body_size=12.5)
    f.arrow(237, 485, 298, 485, color='blue', sw=3)
    f.arrow(520, 312, 440, 418, color='rose', sw=3)
    f.arrow(170, 326, 320, 418, color='amber', sw=2.5, dash='6,5')
    f.soft(485, 445, 135, 80, '<div><b>Real / Fake</b><br/>probability</div>', color='violet', size=13.5)
    f.arrow(462, 485, 483, 485, color='indigo', sw=3)
    f.path('M552,527 L552,585 Q552,592 545,592 L275,592 Q268,592 268,585 L268,316', stroke=col('fuchsia'),
           sw=3, dash='8,6', arrow=True)
    f.text(410, 618, 'adversarial gradient updates G', size=13, weight=700, color=col('fuchsia', 2))

    # (b) morphologies
    panel(f, 655, 100, 420, 540, 'b', 'Real vs generated morphologies', 'amber')
    kinds = ['sphere', 'rod', 'cube', 'triangle', 'star', 'coreshell']
    names = ['Sphere', 'Rod', 'Cube', 'Prism', 'Star', 'Core–shell']
    colors = ['amber', 'orange', 'rose', 'pink', 'violet', 'cyan']
    for row, (lab, yy, jit, cc) in enumerate([('Real', 205, 0.0, 'blue'), ('GAN-generated', 435, 0.12, 'rose')]):
        f.pill(865, yy - 45, lab, color=cc, size=13.5)
        for i, (k, nm, c) in enumerate(zip(kinds, names, colors)):
            x = 730 + (i % 3) * 135
            y = yy + 8 + (i // 3) * 88
            s = 22 * (1 + (jit * math.sin(i * 2.1)))
            particle(f, k, x, y, s, c, jitter=jit)
            f.text(x, y + 42, nm, size=12, color='#475569')
    f.line(675, 372, 1055, 372, color='#CBD5E1', sw=2, dash='6,5')

    # (c) distributions
    panel(f, 1090, 100, 390, 540, 'c', 'Property distributions', 'teal')
    ax = Axes(f, 1145, 170, 310, 380, (-3.5, 3.5), (0, 1.15), xlabel='Target property (standardised)',
              ylabel='Relative frequency', yticks=[0, 0.5, 1.0], xticks=[-3, -2, -1, 0, 1, 2, 3])
    xs = [-3.5 + i * 0.1 for i in range(71)]
    real = [gauss(x, 0, 1.0) for x in xs]
    gen = [0.92 * gauss(x, 0.25, 1.1) for x in xs]
    ax.area(xs, [0] * len(xs), real, color='blue', opacity=0.22)
    ax.area(xs, [0] * len(xs), gen, color='rose', opacity=0.22)
    ax.line(xs, real, color='blue', sw=3, marker=False, smooth=True)
    ax.line(xs, gen, color='rose', sw=3, marker=False, smooth=True, dash='8,5')
    f.legend(1160, 200, [('Real', 'blue', 'line'), ('Generated', 'rose', 'dash')], size=13, gap=22)
    f.html(1148, 300, 100, 90, 'large overlap = realistic generation', size=12, align='left',
           color=col('teal', 2), italic=True)
    f.footnote('Panels (b) and (c) are illustrative schematics; morphologies are stylised, not microscopy images.', y=662)
    f.save(os.path.join(OUT, 'Figure_3.png'))


# --------------------------------------------------------------------------- Figure 4
def fig4():
    random.seed(4)
    f = Figure(1500, 680, title='Reinforcement Learning Framework for Nanomaterial Design',
               subtitle='An agent builds materials step by step and learns from property-based rewards')
    # (a) loop
    panel(f, 20, 100, 520, 540, 'a', 'State–action–reward loop', 'indigo')
    f.card(170, 160, 220, 120, 'Agent', 'policy network (DQN, PPO) chooses the next modification',
           color='indigo', title_size=16, body_size=12.5)
    f.card(170, 430, 220, 130, 'Environment', 'ML surrogate / DFT evaluates the candidate material',
           color='emerald', title_size=16, body_size=12.5)
    f.path('M392,220 C500,230 500,480 392,495', stroke=col('amber'), sw=4, arrow=True)
    f.soft(410, 320, 120, 74, '<div><b>Action a<sub>t</sub></b><br/>add / swap element</div>', color='amber', size=12.5)
    f.path('M168,495 C60,480 60,240 168,215', stroke=col('blue'), sw=4, arrow=True)
    f.soft(30, 290, 128, 74, '<div><b>State s<sub>t+1</sub></b><br/>composition / graph</div>', color='blue', size=12.5)
    f.path('M210,428 C230,380 230,330 210,284', stroke=col('rose'), sw=4, arrow=True, dash='8,5')
    f.soft(240, 320, 150, 74, '<div><b>Reward r<sub>t</sub></b><br/>from target properties</div>', color='rose', size=12.5)

    # (b) convergence
    panel(f, 555, 100, 450, 540, 'b', 'Training convergence', 'emerald')
    ax = Axes(f, 625, 165, 355, 380, (0, 1000), (0, 1.05), xlabel='Training episode',
              ylabel='Mean reward (normalised)', yticks=[0, 0.25, 0.5, 0.75, 1.0], xticks=[0, 250, 500, 750, 1000])
    eps = list(range(0, 1001, 25))
    series = [('PPO', 'violet', 180, 0.92), ('DQN', 'blue', 320, 0.82), ('Random', 'gray', None, 0.22)]
    for name, c, tau, top in series:
        ys = []
        for e in eps:
            v = top if tau is None else top * (1 - math.exp(-e / tau))
            ys.append(max(0, min(1.02, v + random.gauss(0, 0.025))))
        if tau is None:
            ys = [0.18 + 0.04 * (1 - math.exp(-e / 300)) + random.gauss(0, 0.015) for e in eps]
        ax.line(eps, ys, color=c, sw=3, marker=False)
    f.legend(ax.px(330), ax.py(0.33), [(n, c, 'line') for n, c, _, _ in series], cols=3, col_w=80, size=12.5)
    f.pill(ax.px(640), ax.py(0.43), 'Reported: 2–5× better than random', color='emerald', size=12.5)

    # (c) pareto
    panel(f, 1020, 100, 460, 540, 'c', 'Pareto front of discovered materials', 'rose')
    ax = Axes(f, 1095, 165, 360, 380, (0, 4), (0, 1), xlabel='Band gap (eV)',
              ylabel='Stability score (normalised)', yticks=[0, 0.25, 0.5, 0.75, 1.0], xticks=[0, 1, 2, 3, 4])
    pts = []
    for _ in range(70):
        bg = random.uniform(0.2, 3.9)
        lim = 0.95 - 0.055 * bg ** 1.6
        st = random.uniform(0.05, max(0.1, lim))
        pts.append((bg, st))
    front = []
    for i in range(14):
        bg = 0.3 + i * 0.27
        front.append((bg, 0.95 - 0.055 * bg ** 1.6))
    for bg, st in pts:
        f.circle(ax.px(bg), ax.py(st), 5, fill=col('slate', 0), opacity=0.45)
    ax.line([p[0] for p in front], [p[1] for p in front], color='rose', sw=3, smooth=True, marker=False, dash='7,5')
    for bg, st in front:
        f.circle(ax.px(bg), ax.py(st), 7, fill=f.vivid_for('rose'), stroke='#FFFFFF', sw=2, shadow=True)
    f.legend(1260, 200, [('Pareto-optimal', 'rose', 'dot'), ('Other candidates', 'slate', 'dot')], size=13, gap=22)
    f.footnote('Panels (b) and (c): ' + ILLUS, y=662)
    f.save(os.path.join(OUT, 'Figure_4.png'))


# --------------------------------------------------------------------------- Figure 5
def fig5():
    random.seed(5)
    f = Figure(1500, 700, title='High-Throughput Screening and Active Learning',
               subtitle='From a million virtual candidates to a handful of confirmed materials')
    # (a) funnel
    panel(f, 20, 100, 520, 560, 'a', 'Screening funnel', 'blue')
    stages = [('Combinatorial enumeration', '~10⁶ candidates', 'blue'),
              ('Thermodynamic stability (ML)', '', 'cyan'),
              ('Target-property prediction (ML)', '', 'teal'),
              ('DFT validation of top candidates', '', 'emerald'),
              ('Synthesis feasibility', '', 'amber'),
              ('Experimental confirmation', '~10 confirmed', 'rose')]
    top, h = 165, 76
    cx = 280
    for i, (name, num, c) in enumerate(stages):
        w0 = 470 - i * 50
        w1 = 470 - (i + 1) * 50
        y = top + i * h
        f.polygon([(cx - w0 / 2, y), (cx + w0 / 2, y), (cx + w1 / 2, y + h - 6), (cx - w1 / 2, y + h - 6)],
                  fill=f.vivid_for(c), shadow=True)
        f.text(cx, y + (30 if num else 41), name, size=14 if i < 5 else 13, weight=700, color='#FFFFFF')
        if num:
            f.text(cx, y + 54, num, size=13.5, weight=800, color='#FFFFFF')
    f.text(cx, 640, 'each stage is more accurate and more expensive than the last', size=12.5,
           color='#475569', italic=True)

    # (b) active learning loop
    panel(f, 555, 100, 450, 560, 'b', 'Active-learning loop', 'violet')
    cx, cy, R, RX = 780, 395, 165, 128
    steps = [('Train surrogate', 'on labelled data', 'violet'), ('Predict with UQ', 'mean + uncertainty', 'blue'),
             ('Acquisition', 'pick most informative', 'amber'), ('Experiment / DFT', 'label new points', 'emerald')]
    for i, (t, b, c) in enumerate(steps):
        a = -math.pi / 2 + i * math.pi / 2
        a2 = a + math.pi / 2
        f.arrow(cx + RX * math.cos(a + 0.62), cy + R * math.sin(a + 0.62), cx + RX * math.cos(a2 - 0.62),
                cy + R * math.sin(a2 - 0.62), color=c, sw=4, curve=-20)
    for i, (t, b, c) in enumerate(steps):
        a = -math.pi / 2 + i * math.pi / 2
        x, y = cx + RX * math.cos(a), cy + R * math.sin(a)
        f.card(x - 76, y - 42, 152, 84, t, b, color=c, title_size=13.5, body_size=12, header_h=32)
    f.circle(cx, cy, 44, fill=f.radgrad('#C4B5FD', '#7C3AED'), shadow=True)
    f.html(cx - 44, cy - 34, 88, 68, '<b>add to<br/>training<br/>set</b>', color='#FFFFFF', size=12)

    # (c) efficiency
    panel(f, 1020, 100, 460, 560, 'c', 'Random vs intelligent sampling', 'emerald')
    ax = Axes(f, 1095, 170, 360, 400, (0, 100), (0, 1.05), xlabel='Number of experiments',
              ylabel='Best property found (normalised)', yticks=[0, 0.25, 0.5, 0.75, 1.0],
              xticks=[0, 25, 50, 75, 100])
    xs = list(range(0, 101, 4))
    rnd = [0.15 + 0.8 * (1 - math.exp(-x / 70.0)) for x in xs]
    al = [0.15 + 0.82 * (1 - math.exp(-x / 18.0)) for x in xs]
    ax.area(xs, rnd, al, color='emerald', opacity=0.14)
    ax.line(xs, rnd, color='gray', sw=3.5, marker=False, smooth=True, dash='8,5')
    ax.line(xs, al, color='emerald', sw=3.5, marker=False, smooth=True)
    f.legend(1230, 470, [('Active learning / BO', 'emerald', 'line'), ('Random sampling', 'gray', 'dash')],
             size=13, gap=24)
    target = 0.15 + 0.8 * (1 - math.exp(-75 / 70.0))
    xa = -18 * math.log(1 - (target - 0.15) / 0.82)
    ax.hline(target, color='slate', sw=1.5, dash='4,4')
    f.arrow(ax.px(75), ax.py(target) - 18, ax.px(xa) + 6, ax.py(target) - 18, color='rose', sw=3)
    f.pill((ax.px(75) + ax.px(xa)) / 2, ax.py(target) - 44, '3–5× fewer experiments', color='rose', size=13)
    f.footnote('Funnel end points (10⁶ to 10) and the 3–5× saving are from the text; intermediate stage sizes '
               'and the curves in (c) are illustrative.', y=683)
    f.save(os.path.join(OUT, 'Figure_5.png'))


# --------------------------------------------------------------------------- Figure 6
def fingerprint(f, cx, cy, s, color):
    for i in range(1, 8):
        r = s * i / 7.0
        f.path('M%.1f,%.1f A%.1f,%.1f 0 1 1 %.1f,%.1f' % (cx - r * 0.75, cy + r * 0.7, r, r * 1.25,
                                                       cx + r * 0.75, cy + r * 0.7),
               stroke=color, sw=2.6, opacity=0.95)


def fig6():
    random.seed(6)
    f = Figure(1500, 900, title='AI-Designed Nanomaterials for Forensic Applications',
               subtitle='Four application areas discussed in Section 3.4')
    # (a) fingerprints
    panel(f, 20, 95, 720, 380, 'a', 'Fluorescent nanoparticles for latent fingerprints', 'fuchsia')
    subs = [('Paper', '#FEF3C7', 'amber'), ('Glass', '#E0F2FE', 'sky'), ('Plastic', '#F3E8FF', 'purple'),
            ('Metal', '#E2E8F0', 'slate')]
    glow = ['#22D3EE', '#A3E635', '#F472B6', '#FACC15']
    for i, (name, bg, c) in enumerate(subs):
        x = 45 + i * 172
        f.rect(x, 150, 155, 220, fill=f.lingrad(bg, '#FFFFFF'), stroke=col(c), sw=2, rx=12)
        f.rect(x + 12, 165, 131, 160, fill='#0F172A', rx=10, shadow=False)
        fingerprint(f, x + 77, 240, 52, glow[i])
        f.text(x + 77, 350, name, size=14, weight=700, color=col(c, 2))
    f.html(45, 385, 680, 80, 'AI multi-objective optimisation balances <b>quantum yield</b>, <b>photostability</b> '
           'and <b>ridge contrast</b> across substrates; deep-learning image analysis then extracts minutiae.',
           size=13.5, align='left', color='#334155')

    # (b) SERS
    panel(f, 760, 95, 720, 380, 'b', 'GAN-designed SERS substrates', 'amber')
    f.rect(785, 150, 430, 300, fill='#0B1026', rx=12, shadow=False)
    hot = f.radgrad('#FFFFFF', '#FDE047')
    for rr, op, cc in [(150, 0.18, '#7C3AED'), (110, 0.25, '#DB2777'), (75, 0.35, '#F97316'), (45, 0.55, '#FACC15')]:
        f.ellipse(1000, 300, rr * 1.15, rr * 0.7, fill=cc, opacity=op)
    f.ellipse(1000, 300, 22, 16, fill=hot, opacity=0.95)
    for x in (920, 1080):
        f.circle(x, 300, 62, fill=f.radgrad('#FDE68A', '#B45309'), stroke='#78350F', sw=2, shadow=True)
    f.text(1000, 255, 'hot spot', size=13, weight=800, color='#FEF08A')
    f.text(1000, 430, 'nanogap dimer (size, shape, gap optimised)', size=12.5, color='#E2E8F0')
    # colour bar
    f.rect(1250, 160, 26, 270, fill=f.lingrad('#FFFFFF', '#1E1B4B', stops=[(0, '#FEF9C3'), (0.3, '#FACC15'),
                                                                          (0.55, '#F97316'), (0.8, '#DB2777'),
                                                                          (1, '#4C1D95')]), rx=6)
    f.text(1290, 172, 'EF 10¹⁰', size=13, weight=700, anchor='start', color='#334155')
    f.text(1290, 430, 'EF 10⁶', size=13, weight=700, anchor='start', color='#334155')
    f.html(1288, 230, 180, 140, 'Enhancement factors of 10⁶–10¹⁰ enable femtomolar trace detection',
           size=13, align='left', color=col('amber', 2))

    # (c) biosensor strip
    panel(f, 20, 495, 720, 380, 'c', 'Nanobiosensor (lateral-flow) for body fluids', 'rose')
    sx, sy = 60, 610
    f.rect(sx, sy, 640, 70, fill='#F8FAFC', stroke='#94A3B8', sw=2, rx=10)
    segs = [('Sample pad', 0, 120, 'sky'), ('AuNP conjugate pad', 120, 180, 'rose'),
            ('Detection zone', 300, 230, 'slate'), ('Absorbent pad', 530, 110, 'amber')]
    for name, x0, w, c in segs:
        f.rect(sx + x0 + 3, sy + 4, w - 6, 62, fill=col(c, 1), rx=8, shadow=False)
        f.text(sx + x0 + w / 2, sy + 100, name, size=12.5, weight=700, color=col(c, 2))
    for i in range(14):
        f.circle(sx + 140 + (i % 7) * 22, sy + 22 + (i // 7) * 26, 7, fill=f.radgrad('#FCA5A5', '#B91C1C'))
    f.rect(sx + 370, sy + 6, 14, 58, fill=col('rose'), rx=3, shadow=False)
    f.rect(sx + 450, sy + 6, 14, 58, fill=col('indigo'), rx=3, shadow=False)
    f.text(sx + 377, sy - 10, 'Test', size=12.5, weight=800, color=col('rose', 2))
    f.text(sx + 457, sy - 10, 'Control', size=12.5, weight=800, color=col('indigo', 2))
    f.arrow(sx + 20, sy - 30, sx + 280, sy - 30, color='sky', sw=3, label='capillary flow', label_dy=-14)
    f.html(60, 735, 660, 120, 'AI-optimised gold-nanoparticle conjugates and recognition elements '
           '(antibodies, aptamers, molecularly imprinted polymers) give rapid, presumptive on-scene '
           'identification; electrochemical and plasmonic variants extend this to drugs and DNA.',
           size=13.5, align='left', color='#334155')

    # (d) MOF sensor array heatmap
    panel(f, 760, 495, 720, 380, 'd', 'MOF sensor array: explosive vapour responses', 'teal')
    analytes = ['Nitroaromatic', 'Peroxide-based', 'Inorganic oxidizer', 'Blank air']
    sensors = ['MOF-1', 'MOF-2', 'MOF-3', 'MOF-4', 'MOF-5', 'MOF-6']
    pattern = [[0.95, 0.70, 0.30, 0.55, 0.15, 0.80],
               [0.20, 0.45, 0.90, 0.35, 0.75, 0.25],
               [0.55, 0.15, 0.40, 0.90, 0.60, 0.35],
               [0.05, 0.08, 0.06, 0.04, 0.07, 0.05]]
    stops = ['#F0FDFA', '#5EEAD4', '#14B8A6', '#7C3AED', '#4C1D95']

    def cmap(v):
        k = min(3.999, v * 4)
        i = int(k)
        return lerp_hex(stops[i], stops[i + 1], k - i)
    x0, y0, cw, ch = 950, 560, 70, 56
    for j, s in enumerate(sensors):
        f.text(x0 + j * cw + cw / 2, y0 - 10, s, size=12.5, weight=700, color='#334155')
    for i, a in enumerate(analytes):
        f.text(x0 - 12, y0 + i * ch + ch / 2 + 5, a, size=13, weight=700, color='#334155', anchor='end')
        for j in range(len(sensors)):
            v = pattern[i][j]
            f.rect(x0 + j * cw + 3, y0 + i * ch + 3, cw - 6, ch - 6, fill=cmap(v), rx=8, shadow=False)
    f.rect(x0, y0 + 4 * ch + 18, 6 * cw, 16,
           fill=f.lingrad('#000', '#000', horizontal=True, stops=[(k / 4.0, c) for k, c in enumerate(stops)]),
           rx=5, shadow=False)
    f.text(x0, y0 + 4 * ch + 52, 'low response', size=12, anchor='start', color='#475569')
    f.text(x0 + 6 * cw, y0 + 4 * ch + 52, 'high response', size=12, anchor='end', color='#475569')
    f.text(1120, 860, 'each analyte gives a distinct fingerprint pattern for pattern recognition', size=12,
           color='#475569', italic=True)
    f.footnote('Schematic illustrations; response patterns in (d) are illustrative, not measured data. '
               'EF range from the text [17].', y=890)
    f.save(os.path.join(OUT, 'Figure_6.png'))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    which = sys.argv[1:] or ['1', '2', '3', '4', '5', '6']
    for w in which:
        globals()['fig' + w]()
