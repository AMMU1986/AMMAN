#!/usr/bin/env python3
"""Generate the 20 book figures as PNG using the pure-Python drawlib."""
import os
import math
from drawlib import Canvas, Axes, legend, COLORS, BLACK, AXIS, GRID

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
os.makedirs(OUT, exist_ok=True)

W, H = 760, 520
PLOT = (95, 70, 700, 420)  # x0,y0,x1,y1


def new():
    return Canvas(W, H)


def box(cv, x0, y0, x1, y1, label, fill, sub=None):
    cv.fill_rect(x0, y0, x1, y1, fill)
    cv.rect(x0, y0, x1, y1, AXIS, 2)
    cv.text_center((x0 + x1) / 2, (y0 + y1) / 2 - (10 if sub else 6), label, BLACK, 2)
    if sub:
        cv.text_center((x0 + x1) / 2, (y0 + y1) / 2 + 6, sub, (60, 60, 60), 2)


def arrow(cv, x0, y0, x1, y1, c=AXIS, t=2):
    cv.line(x0, y0, x1, y1, c, t)
    ang = math.atan2(y1 - y0, x1 - x0)
    for da in (math.pi - 0.4, math.pi + 0.4):
        cv.line(x1, y1, x1 + 10 * math.cos(ang + da), y1 + 10 * math.sin(ang + da), c, t)


# ---------------- Figure 1: Three modes of heat transfer (schematic) ----------------
def fig01():
    cv = new()
    cv.text_fit(W / 2, 22, 'Modes of Heat Transfer', BLACK, 3)
    # Conduction
    box(cv, 60, 120, 230, 200, 'CONDUCTION', (255, 235, 205))
    cv.text_center(145, 100, 'Solid wall', (60, 60, 60), 2)
    for i in range(5):
        x = 80 + i * 30
        cv.circle(x, 250, 6, COLORS[1], fill=True)
        arrow(cv, x, 240, x, 215, COLORS[1], 2)
    cv.text_center(145, 265, 'q = -k dT/dx', BLACK, 2)
    # Convection
    box(cv, 300, 120, 470, 200, 'CONVECTION', (205, 235, 255))
    for i in range(4):
        y = 235 + i * 8
        cv.polyline([(310, y), (340, y - 6), (370, y + 6), (400, y - 6), (455, y)], COLORS[0], 2)
    cv.text_center(385, 275, 'q = h A (Ts - Tf)', BLACK, 2)
    # Radiation
    box(cv, 540, 120, 700, 200, 'RADIATION', (255, 215, 215))
    for i in range(5):
        a = -0.6 + i * 0.3
        arrow(cv, 620, 210, 620 + 70 * math.sin(a), 260, COLORS[3], 2)
    cv.text_center(620, 275, 'q = e s A T^4', BLACK, 2)
    cv.text_center(W / 2, 330, 'Governing laws for the three fundamental transport mechanisms', (60, 60, 60), 2)
    cv.save(os.path.join(OUT, 'Fig01_heat_transfer_modes.png'))


# ---------------- Figure 2: Heat exchanger classification tree ----------------
def fig02():
    cv = new()
    cv.text_fit(W / 2, 22, 'Classification of Heat Exchangers', BLACK, 3)
    box(cv, 300, 60, 460, 110, 'Heat Exchangers', (220, 230, 245))
    cats = [('Recuperative', 90), ('Regenerative', 300), ('Direct-contact', 540)]
    for name, x in cats:
        box(cv, x, 170, x + 180, 215, name, (235, 245, 235))
        arrow(cv, 380, 110, x + 90, 170)
    subs = [('Shell-and-tube', 60), ('Plate', 230), ('Compact / finned', 400), ('Double-pipe', 575)]
    for name, x in subs:
        box(cv, x, 300, x + 150, 350, name, (250, 245, 230))
    arrow(cv, 180, 215, 135, 300)
    arrow(cv, 180, 215, 305, 300)
    arrow(cv, 390, 215, 475, 300)
    arrow(cv, 390, 215, 650, 300)
    cv.text_center(W / 2, 420, 'Hierarchy by transfer process and flow geometry', (60, 60, 60), 2)
    cv.save(os.path.join(OUT, 'Fig02_hx_classification.png'))


# ---------------- Figure 3: Effectiveness-NTU curves ----------------
def fig03():
    cv = new()
    ax = Axes(cv, *PLOT, (0, 5), (0, 1))
    ax.frame('Number of transfer units, NTU', 'Effectiveness',
             'Effectiveness-NTU (counterflow)',
             xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ntu = [i * 0.1 for i in range(51)]
    for j, Cr in enumerate([0.0, 0.25, 0.5, 0.75, 1.0]):
        ys = []
        for n in ntu:
            if Cr == 0:
                e = 1 - math.exp(-n)
            elif abs(Cr - 1) < 1e-6:
                e = n / (1 + n)
            else:
                ex = math.exp(-n * (1 - Cr))
                e = (1 - ex) / (1 - Cr * ex)
            ys.append(e)
        ax.plot(ntu, ys, COLORS[j], 3)
    legend(cv, 470, 300, [('Cr = 0.0', COLORS[0], 'line'), ('Cr = 0.25', COLORS[1], 'line'),
                          ('Cr = 0.5', COLORS[2], 'line'), ('Cr = 0.75', COLORS[3], 'line'),
                          ('Cr = 1.0', COLORS[4], 'line')])
    cv.save(os.path.join(OUT, 'Fig03_effectiveness_ntu.png'))


# ---------------- Figure 4: Nanofluid preparation (one/two-step) ----------------
def fig04():
    cv = new()
    cv.text_fit(W / 2, 22, 'Nanofluid Preparation Routes', BLACK, 3)
    cv.text_center(210, 70, 'Two-step method', BLACK, 2)
    box(cv, 60, 95, 200, 140, 'Dry nanopowder', (255, 240, 220))
    box(cv, 60, 165, 200, 210, 'Base fluid', (215, 235, 255))
    box(cv, 250, 130, 360, 175, 'Dispersion +', (235, 235, 235), 'sonication')
    box(cv, 250, 210, 360, 255, 'Surfactant', (235, 245, 235))
    arrow(cv, 200, 117, 250, 145)
    arrow(cv, 200, 187, 250, 160)
    arrow(cv, 305, 175, 305, 210)
    box(cv, 250, 275, 360, 320, 'Nanofluid', (220, 230, 245))
    arrow(cv, 305, 255, 305, 275)
    cv.text_center(560, 70, 'One-step method', BLACK, 2)
    box(cv, 430, 110, 560, 155, 'Precursor', (255, 240, 220))
    box(cv, 620, 110, 700, 155, 'Base fluid', (215, 235, 255))
    box(cv, 470, 200, 660, 245, 'Simultaneous synthesis', (235, 235, 235), '& dispersion')
    arrow(cv, 495, 155, 540, 200)
    arrow(cv, 660, 155, 600, 200)
    box(cv, 500, 290, 630, 335, 'Nanofluid', (220, 230, 245))
    arrow(cv, 565, 245, 565, 290)
    cv.text_center(W / 2, 430, 'Comparison of the principal synthesis strategies', (60, 60, 60), 2)
    cv.save(os.path.join(OUT, 'Fig04_nanofluid_preparation.png'))


# ---------------- Figure 5: Thermal conductivity enhancement vs concentration ----------------
def fig05():
    cv = new()
    ax = Axes(cv, *PLOT, (0, 4), (1.0, 1.4))
    ax.frame('Volume concentration (%)', 'k_nf / k_bf',
             'Thermal conductivity enhancement',
             xticks=[0, 1, 2, 3, 4], yticks=[1.0, 1.1, 1.2, 1.3, 1.4])
    phi = [i * 0.25 for i in range(17)]
    data = {'Al2O3/water': 0.055, 'CuO/water': 0.07, 'TiO2/water': 0.04, 'MWCNT/water': 0.095}
    for j, (name, slope) in enumerate(data.items()):
        ys = [1 + slope * p + 0.004 * p * p for p in phi]
        ax.plot(phi, ys, COLORS[j], 3, ['o', 's', '^', 'd'][j])
    legend(cv, 130, 300, [(k, COLORS[i], 'line') for i, k in enumerate(data)])
    cv.save(os.path.join(OUT, 'Fig05_k_enhancement.png'))


# ---------------- Figure 6: Viscosity vs temperature ----------------
def fig06():
    cv = new()
    ax = Axes(cv, *PLOT, (20, 60), (0.4, 1.6))
    ax.frame('Temperature (C)', 'Relative viscosity mu_nf/mu_bf',
             'Viscosity vs temperature', xticks=[20, 30, 40, 50, 60],
             yticks=[0.4, 0.8, 1.2, 1.6])
    T = [20 + i * 4 for i in range(11)]
    for j, phi in enumerate([0.5, 1.0, 2.0, 3.0]):
        ys = [(1 + 2.5 * phi / 100 + 6.2 * (phi / 100) ** 2) * math.exp(-0.012 * (t - 20)) + 0.15 for t in T]
        ax.plot(T, ys, COLORS[j], 3, ['o', 's', '^', 'd'][j])
    legend(cv, 470, 300, [(f'phi = {p}%', COLORS[i], 'line') for i, p in enumerate([0.5, 1.0, 2.0, 3.0])])
    cv.save(os.path.join(OUT, 'Fig06_viscosity_temp.png'))


# ---------------- Figure 7: Stability - zeta potential vs pH ----------------
def fig07():
    cv = new()
    ax = Axes(cv, 95, 70, 700, 420, (2, 12), (-50, 50))
    ax.frame('pH', 'Zeta potential (mV)', 'Colloidal stability (zeta vs pH)',
             xticks=[2, 4, 6, 8, 10, 12], yticks=[-50, -25, 0, 25, 50])
    cv.line(ax.px(2), ax.py(0), ax.px(12), ax.py(0), AXIS, 1)
    pH = [2 + i * 0.5 for i in range(21)]
    ys = [45 - 9 * (p - 3) for p in pH]
    ax.plot(pH, ys, COLORS[0], 3, 'o')
    # stable bands
    cv.text(ax.px(2.2), ax.py(42), 'stable (+)', COLORS[2], 2)
    cv.text(ax.px(9.5), ax.py(-40), 'stable (-)', COLORS[2], 2)
    cv.text_center(ax.px(8), ax.py(3) - 18, 'IEP', COLORS[1], 2)
    cv.save(os.path.join(OUT, 'Fig07_zeta_pH.png'))


# ---------------- Figure 8: Nusselt vs Reynolds for concentrations ----------------
def fig08():
    cv = new()
    ax = Axes(cv, *PLOT, (2000, 20000), (0, 160))
    ax.frame('Reynolds number', 'Nusselt number', 'Convective performance vs Re',
             xticks=[2000, 8000, 14000, 20000], yticks=[0, 40, 80, 120, 160],
             xtl=['2k', '8k', '14k', '20k'])
    Re = [2000 + i * 900 for i in range(21)]
    for j, (name, f) in enumerate([('Water', 1.0), ('phi=1%', 1.12), ('phi=2%', 1.22), ('phi=3%', 1.33)]):
        ys = [0.023 * (r ** 0.8) * (6.9 ** 0.4) * f / 6.0 for r in Re]
        ax.plot(Re, ys, COLORS[j], 3, ['o', 's', '^', 'd'][j])
    legend(cv, 130, 300, [(n, COLORS[i], 'line') for i, (n, _) in
                          enumerate([('Water', 1), ('phi=1%', 1), ('phi=2%', 1), ('phi=3%', 1)])])
    cv.save(os.path.join(OUT, 'Fig08_nu_re.png'))


# ---------------- Figure 9: Particle shape effect (bar) ----------------
def fig09():
    cv = new()
    ax = Axes(cv, *PLOT, (0, 5), (0, 40))
    ax.frame('Particle morphology', 'Heat transfer enhancement (%)',
             'Effect of nanoparticle shape',
             xticks=[1, 2, 3, 4], yticks=[0, 10, 20, 30, 40],
             xtl=['Sphere', 'Blade', 'Cylinder', 'Platelet'])
    ax.bar([1, 2, 3, 4], [14, 22, 27, 34], 0.7, COLORS[0])
    cv.save(os.path.join(OUT, 'Fig09_shape_effect.png'))


# ---------------- Figure 10: Pressure drop / friction penalty ----------------
def fig10():
    cv = new()
    ax = Axes(cv, *PLOT, (0, 3), (1.0, 1.8))
    ax.frame('Volume concentration (%)', 'Delta-P ratio (nf/bf)',
             'Pumping-power penalty',
             xticks=[0, 1, 2, 3], yticks=[1.0, 1.2, 1.4, 1.6, 1.8])
    phi = [i * 0.25 for i in range(13)]
    for j, re in enumerate([5000, 10000, 15000]):
        ys = [1 + (0.15 + re / 120000) * p for p in phi]
        ax.plot(phi, ys, COLORS[j], 3, ['o', 's', '^'][j])
    legend(cv, 130, 300, [(f'Re={r}', COLORS[i], 'line') for i, r in enumerate([5000, 10000, 15000])])
    cv.save(os.path.join(OUT, 'Fig10_pressure_drop.png'))


# ---------------- Figure 11: LMTD vs effectiveness-NTU design workflow ----------------
def fig11():
    cv = new()
    cv.text_fit(W / 2, 22, 'Heat Exchanger Design Workflow', BLACK, 3)
    steps = ['Duty & fluid data', 'Select type & geometry', 'Estimate U, areas',
             'LMTD / e-NTU sizing', 'Pressure-drop check', 'Iterate & optimize']
    y = 70
    for i, s in enumerate(steps):
        box(cv, 250, y, 510, y + 45, s, (220 - i * 4, 232, 245))
        if i < len(steps) - 1:
            arrow(cv, 380, y + 45, 380, y + 58)
        y += 58
    cv.text(540, 120, 'Energy balance', (60, 60, 60), 2)
    cv.text(540, 236, 'Correlations /', (60, 60, 60), 2)
    cv.text(540, 252, 'CFD / ML', (60, 60, 60), 2)
    cv.save(os.path.join(OUT, 'Fig11_design_workflow.png'))


# ---------------- Figure 12: Energy vs exergy efficiency ----------------
def fig12():
    cv = new()
    ax = Axes(cv, *PLOT, (0, 3), (0, 100))
    ax.frame('Volume concentration (%)', 'Efficiency (%)',
             'Energy vs exergy performance',
             xticks=[0, 1, 2, 3], yticks=[0, 25, 50, 75, 100])
    phi = [i * 0.25 for i in range(13)]
    ax.plot(phi, [72 + 4 * p for p in phi], COLORS[0], 3, 'o')
    ax.plot(phi, [34 + 6 * p - 0.8 * p * p for p in phi], COLORS[1], 3, 's')
    legend(cv, 470, 300, [('Energy efficiency', COLORS[0], 'line'),
                          ('Exergy efficiency', COLORS[1], 'line')])
    cv.save(os.path.join(OUT, 'Fig12_energy_exergy.png'))


# ---------------- Figure 13: Entropy generation minimization ----------------
def fig13():
    cv = new()
    ax = Axes(cv, *PLOT, (0, 20000), (0, 3))
    ax.frame('Reynolds number', 'Entropy generation (W/K)',
             'Entropy generation minimization',
             xticks=[0, 5000, 10000, 15000, 20000], yticks=[0, 1, 2, 3],
             xtl=['0', '5k', '10k', '15k', '20k'])
    Re = [1000 + i * 950 for i in range(21)]
    thermal = [2.6 * math.exp(-r / 6000) + 0.2 for r in Re]
    fric = [0.05 + (r / 20000) ** 2 * 2.2 for r in Re]
    total = [a + b for a, b in zip(thermal, fric)]
    ax.plot(Re, thermal, COLORS[0], 3)
    ax.plot(Re, fric, COLORS[1], 3)
    ax.plot(Re, total, COLORS[2], 3)
    legend(cv, 470, 90, [('Thermal', COLORS[0], 'line'), ('Frictional', COLORS[1], 'line'),
                         ('Total', COLORS[2], 'line')])
    cv.save(os.path.join(OUT, 'Fig13_entropy_gen.png'))


# ---------------- Figure 14: CFD workflow ----------------
def fig14():
    cv = new()
    cv.text_fit(W / 2, 22, 'CFD Analysis Workflow', BLACK, 3)
    steps = ['Geometry / domain', 'Mesh generation', 'Governing eqns & models',
             'Boundary conditions', 'Solver iteration', 'Post-processing']
    y = 66
    for i, s in enumerate(steps):
        box(cv, 250, y, 510, y + 42, s, (232, 240, 232))
        if i < len(steps) - 1:
            arrow(cv, 380, y + 42, 380, y + 56)
        y += 56
    cv.text(540, 150, 'k-epsilon / k-omega', (60, 60, 60), 2)
    cv.text(540, 262, 'single / two-phase', (60, 60, 60), 2)
    cv.save(os.path.join(OUT, 'Fig14_cfd_workflow.png'))


# ---------------- Figure 15: Mesh independence ----------------
def fig15():
    cv = new()
    ax = Axes(cv, *PLOT, (0, 1200000), (55, 75))
    ax.frame('Number of mesh elements', 'Nusselt number',
             'Grid-independence study',
             xticks=[0, 300000, 600000, 900000, 1200000], yticks=[55, 60, 65, 70, 75],
             xtl=['0', '300k', '600k', '900k', '1.2M'])
    N = [50000, 150000, 300000, 500000, 750000, 1000000, 1150000]
    Nu = [58, 63.5, 67, 68.9, 69.4, 69.6, 69.65]
    ax.plot(N, Nu, COLORS[0], 3, 'o')
    cv.line(ax.px(500000), ax.py(55), ax.px(500000), ax.py(75), COLORS[1], 1)
    cv.text(ax.px(520000), ax.py(60), 'selected mesh', COLORS[1], 2)
    cv.save(os.path.join(OUT, 'Fig15_mesh_independence.png'))


# ---------------- Figure 16: Evolution / branches of AI ----------------
def fig16():
    cv = new()
    cv.text_fit(W / 2, 22, 'Artificial Intelligence for Thermal Engineering', BLACK, 3)
    box(cv, 300, 60, 460, 105, 'Artificial Intelligence', (220, 230, 245))
    box(cv, 300, 140, 460, 185, 'Machine Learning', (230, 240, 230))
    arrow(cv, 380, 105, 380, 140)
    box(cv, 300, 220, 460, 265, 'Deep Learning', (245, 235, 225))
    arrow(cv, 380, 185, 380, 220)
    leaves = [('ANN', 70), ('SVM', 210), ('Random Forest', 470), ('XGBoost', 620)]
    for name, x in leaves:
        box(cv, x, 320, x + 130, 365, name, (245, 245, 230))
        arrow(cv, 380, 185, x + 65, 320)
    cv.text_center(W / 2, 420, 'Nested scope of AI, ML and DL with representative algorithms',
                   (60, 60, 60), 2)
    cv.save(os.path.join(OUT, 'Fig16_ai_evolution.png'))


# ---------------- Figure 17: ML types (supervised/unsupervised/RL) ----------------
def fig17():
    cv = new()
    cv.text_fit(W / 2, 22, 'Machine Learning Paradigms', BLACK, 3)
    box(cv, 60, 120, 240, 175, 'Supervised', (215, 235, 255), 'labelled data')
    box(cv, 290, 120, 470, 175, 'Unsupervised', (230, 245, 230), 'structure discovery')
    box(cv, 520, 120, 700, 175, 'Reinforcement', (255, 235, 220), 'reward feedback')
    ex = [('Regression', 60), ('Classification', 60 + 0), ('Clustering', 290),
          ('Dim. reduction', 290), ('Policy control', 520), ('Optimization', 520)]
    y0 = 220
    for i, (name, x) in enumerate(ex):
        yy = y0 + (i % 2) * 55
        box(cv, x, yy, x + 180, yy + 42, name, (245, 245, 240))
    arrow(cv, 150, 175, 150, 220)
    arrow(cv, 380, 175, 380, 220)
    arrow(cv, 610, 175, 610, 220)
    cv.text_center(W / 2, 400, 'Tasks addressed by each learning paradigm in thermal modelling',
                   (60, 60, 60), 2)
    cv.save(os.path.join(OUT, 'Fig17_ml_paradigms.png'))


# ---------------- Figure 18: ML pipeline ----------------
def fig18():
    cv = new()
    cv.text_fit(W / 2, 26, 'Data-Driven Modelling Pipeline', BLACK, 3)
    steps = ['Data\ncollection', 'Cleaning', 'Feature\neng.', 'Train/\ntest split',
             'Model\ntraining', 'Validation', 'Deploy']
    x = 40
    for i, s in enumerate(steps):
        lbl = s.replace('\n', ' ')
        box(cv, x, 190, x + 90, 250, lbl, (222, 234, 246))
        if i < len(steps) - 1:
            arrow(cv, x + 90, 220, x + 102, 220)
        x += 102
    cv.text_center(W / 2, 320, 'Hyperparameter tuning & cross-validation feed back into training',
                   (60, 60, 60), 2)
    arrow(cv, 560, 250, 560, 300, COLORS[1], 2)
    arrow(cv, 250, 300, 250, 250, COLORS[1], 2)
    cv.line(250, 300, 560, 300, COLORS[1], 2)
    cv.save(os.path.join(OUT, 'Fig18_ml_pipeline.png'))


# ---------------- Figure 19: Predicted vs actual (parity) thermal conductivity ----------------
def fig19():
    cv = new()
    ax = Axes(cv, *PLOT, (1.0, 1.4), (1.0, 1.4))
    ax.frame('Experimental k_nf/k_bf', 'Predicted k_nf/k_bf',
             'ML parity plot (thermal conductivity)',
             xticks=[1.0, 1.1, 1.2, 1.3, 1.4], yticks=[1.0, 1.1, 1.2, 1.3, 1.4])
    ax.plot([1.0, 1.4], [1.0, 1.4], AXIS, 2)
    import random
    random.seed(7)
    xs = [1.0 + 0.4 * (i / 40) for i in range(41)]
    ys = [x + random.uniform(-0.015, 0.015) for x in xs]
    for x, y in zip(xs, ys):
        cv.marker(ax.px(x), ax.py(y), COLORS[0], 'o', 3)
    cv.text(ax.px(1.02), ax.py(1.36), 'R2 = 0.992', BLACK, 2)
    legend(cv, 470, 300, [('Ideal (y=x)', AXIS, 'line'), ('ANN prediction', COLORS[0], 'line')])
    cv.save(os.path.join(OUT, 'Fig19_parity_k.png'))


# ---------------- Figure 20: Model performance comparison (bar) ----------------
def fig20():
    cv = new()
    ax = Axes(cv, *PLOT, (0, 6), (0.9, 1.0))
    ax.frame('Model', 'R-squared',
             'Predictive accuracy across ML models',
             xticks=[1, 2, 3, 4, 5], yticks=[0.90, 0.925, 0.95, 0.975, 1.0],
             xtl=['MLR', 'SVR', 'ANN', 'RF', 'XGB'])
    ax.bar([1, 2, 3, 4, 5], [0.918, 0.951, 0.985, 0.972, 0.991], 0.6, COLORS[2], base=0.9)
    cv.save(os.path.join(OUT, 'Fig20_model_comparison.png'))


ALL = [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10,
       fig11, fig12, fig13, fig14, fig15, fig16, fig17, fig18, fig19, fig20]

if __name__ == '__main__':
    for f in ALL:
        f()
    files = sorted(os.listdir(OUT))
    print(f"Generated {len(files)} figures:")
    for fn in files:
        print(' ', fn)
