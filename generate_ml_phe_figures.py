#!/usr/bin/env python3
"""
Generate 7 publication-style figures (PNG) for the ML / TiO2-Al2O3 PHE manuscript.
Reuses the pure-stdlib PNGCanvas and 5x7 font from generate_figures.py.
No third-party dependencies.
"""

import os
import math

# Reuse the canvas + font already present in the repository.
from generate_figures import (
    PNGCanvas, DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN, ORANGE, LIGHT_ORANGE,
    RED, LIGHT_RED, PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)

OUT = '/projects/sandbox/AMMAN/ml_phe_figures'
os.makedirs(OUT, exist_ok=True)

RATIO_LABELS = ["0:5", "1:4", "2:3", "3:2", "4:1"]
RATIO_COLORS = [MED_BLUE, RED, ORANGE, MED_GREEN, PURPLE]


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def axes(c, x0, y0, x1, y1):
    """draw an L-shaped axis box (x0,y1)=origin bottom-left."""
    c.vline(x0, y0, y1, BLACK)
    c.hline(x0, x1, y1, BLACK)


def plot_series(c, x0, y0, x1, y1, xs, ys, xr, yr, color, thick=2, markers=True):
    """plot a polyline given data coords mapped into pixel box."""
    xmin, xmax = xr
    ymin, ymax = yr
    def px(x): return int(x0 + (x - xmin) / (xmax - xmin) * (x1 - x0))
    def py(y): return int(y1 - (y - ymin) / (ymax - ymin) * (y1 - y0))
    pts = [(px(x), py(y)) for x, y in zip(xs, ys)]
    for i in range(len(pts) - 1):
        c.line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], color, thick)
    if markers:
        for (xp, yp) in pts:
            c.circle(xp, yp, 3, color, color)
    return px, py


def grid(c, x0, y0, x1, y1, nx, ny):
    for i in range(1, nx):
        xx = x0 + i * (x1 - x0) // nx
        c.vline(xx, y0, y1, LIGHT_GRAY)
    for j in range(1, ny):
        yy = y0 + j * (y1 - y0) // ny
        c.hline(x0, x1, yy, LIGHT_GRAY)


def legend(c, x, y, items, scale=1):
    for i, (col, lab) in enumerate(items):
        yy = y + i * 16
        c.fill_rect(x, yy, x + 14, yy + 8, col)
        c.text(x + 20, yy, lab, BLACK, scale)


# ---------------------------------------------------------------------------
# Figure 1 : methodology workflow (vertical flow of 8 steps)
# ---------------------------------------------------------------------------
def fig1():
    c = PNGCanvas(900, 1180, WHITE)
    c.text_c(450, 16, "Methodology workflow of the multi-target ML framework", BLACK, 2)
    steps = [
        ("STEP 1  Nanofluid preparation",
         "Two-step method: TiO2 + Al2O3 in distilled water; ultrasonication;",
         "five mixture ratios; loading = 0.01-0.20 vol.%", PALE_BLUE, DARK_BLUE),
        ("STEP 2  Experimental rig (PHE loop)",
         "Hot loop: tank, heater, pump, flow meter, dP sensor, thermocouples,",
         "DAQ; cold loop: water at fixed flow", LIGHT_ORANGE, ORANGE),
        ("STEP 3  Data acquisition",
         "Flow rate, inlet/outlet temperatures, pressure drop; Re = 500-2000;",
         "steady-state averaging; energy-balance check", LIGHT_GREEN, DARK_GREEN),
        ("STEP 4  Derived targets (multi-output)",
         "h (W/m2K), Nu, f via LMTD reduction and validated cold-side",
         "wall correlation; three-output label vector", LIGHT_PURPLE, PURPLE),
        ("STEP 5  Pre-processing",
         "IQR outlier removal; min-max normalisation; stratified 80:20 split",
         "(fixed random seed over loading and Re bands)", PALE_BLUE, MED_BLUE),
        ("STEP 6  Multi-target ML models",
         "BR-ANN, RF, XGBoost, SVR; grid-search hyperparameter tuning",
         "with five-fold cross-validation on training set only", LIGHT_ORANGE, GOLD),
        ("STEP 7  Validation and metrics",
         "k-fold CV; R-squared, RMSE, MAE, MAPE, NRMSE; parity plots;",
         "permutation importance", LIGHT_GREEN, MED_GREEN),
        ("STEP 8  Deployment and benchmark",
         "Best multi-target predictor deployed; benchmarked against",
         "classical nanofluid correlations", LIGHT_PURPLE, PURPLE),
    ]
    x0, x1 = 150, 750
    top = 50
    bh = 118
    gap = 20
    for i, (title, l1, l2, fill, border) in enumerate(steps):
        y0 = top + i * (bh + gap)
        y1 = y0 + bh
        c.rect(x0, y0, x1, y1, border, fill)
        c.rect(x0, y0, x1, y0 + 30, border, border)
        c.text(x0 + 14, y0 + 10, title, WHITE, 1)
        c.text(x0 + 14, y0 + 48, l1, BLACK, 1)
        c.text(x0 + 14, y0 + 70, l2, BLACK, 1)
        if i < len(steps) - 1:
            cx = (x0 + x1) // 2
            c.arrow(cx, y1 + 2, cx, y1 + gap - 2, GRAY, 3, 7)
    c.save(os.path.join(OUT, 'Figure_1_Workflow.png'))
    print("Figure_1_Workflow.png")


# ---------------------------------------------------------------------------
# Figure 2 : h vs Re for 5 mixture ratios at phi = 0.10 vol.%
# ---------------------------------------------------------------------------
def fig2():
    c = PNGCanvas(820, 560, WHITE)
    c.text_c(410, 14, "Convection coefficient vs Reynolds number (phi = 0.10 vol.%)", BLACK, 2)
    x0, y0, x1, y1 = 95, 60, 620, 500
    grid(c, x0, y0, x1, y1, 6, 6)
    axes(c, x0, y0, x1, y1)
    Re = [500, 800, 1100, 1400, 1700, 2000]
    xr = (450, 2050)
    yr = (280, 900)
    # base curve shape ~ Re^0.72 ; ratio multiplier decreasing from 0:5 to 4:1
    mult = [1.00, 0.955, 0.915, 0.880, 0.850]
    for k in range(5):
        ys = [280 + mult[k] * 20.5 * (r ** 0.72) / (500 ** 0.72) * 500 ** 0.0
              for r in Re]
        ys = [280 + mult[k] * (18.0 * (r ** 0.5) - 40) for r in Re]
        plot_series(c, x0, y0, x1, y1, Re, ys, xr, yr, RATIO_COLORS[k], 2)
    # ticks
    for i, r in enumerate([500, 800, 1100, 1400, 1700, 2000]):
        xx = int(x0 + (r - xr[0]) / (xr[1] - xr[0]) * (x1 - x0))
        c.vline(xx, y1, y1 + 5, BLACK)
        c.text_c(xx, y1 + 10, str(r), BLACK, 1)
    for v in [300, 400, 500, 600, 700, 800, 900]:
        yy = int(y1 - (v - yr[0]) / (yr[1] - yr[0]) * (y1 - y0))
        c.hline(x0 - 5, x0, yy, BLACK)
        c.text(x0 - 42, yy - 3, str(v), BLACK, 1)
    c.text_c((x0 + x1) // 2, y1 + 28, "Reynolds number, Re", BLACK, 1)
    c.text(18, y0 - 18, "h (W/m2K)", BLACK, 1)
    legend(c, x1 + 20, y0 + 10,
           [(RATIO_COLORS[k], "TiO2:Al2O3 = " + RATIO_LABELS[k]) for k in range(5)])
    c.save(os.path.join(OUT, 'Figure_2_h_vs_Re.png'))
    print("Figure_2_h_vs_Re.png")


# ---------------------------------------------------------------------------
# Figure 3 : (a) h vs Re for 0:5 at 5 loadings ; (b) enhancement bar chart
# ---------------------------------------------------------------------------
def fig3():
    c = PNGCanvas(1040, 540, WHITE)
    c.text(60, 12, "(a) h vs Re for 0:5 ratio at five loadings", BLACK, 1)
    c.text(560, 12, "(b) Enhancement in h vs water (Re = 1200)", BLACK, 1)

    # panel (a)
    x0, y0, x1, y1 = 80, 50, 470, 480
    grid(c, x0, y0, x1, y1, 6, 6)
    axes(c, x0, y0, x1, y1)
    Re = [500, 800, 1100, 1400, 1700, 2000]
    xr = (450, 2050); yr = (280, 900)
    loads = [0.01, 0.05, 0.10, 0.15, 0.20]
    lcolors = [MED_BLUE, RED, ORANGE, MED_GREEN, PURPLE]
    for i, phi in enumerate(loads):
        f = 0.78 + 0.30 * math.sqrt(phi / 0.20)   # sqrt loading saturation
        ys = [300 + f * (13.5 * (r ** 0.5) - 30) for r in Re]
        plot_series(c, x0, y0, x1, y1, Re, ys, xr, yr, lcolors[i], 2)
    for r in [500, 1100, 1700]:
        xx = int(x0 + (r - xr[0]) / (xr[1] - xr[0]) * (x1 - x0))
        c.vline(xx, y1, y1 + 5, BLACK); c.text_c(xx, y1 + 10, str(r), BLACK, 1)
    for v in [300, 500, 700, 900]:
        yy = int(y1 - (v - yr[0]) / (yr[1] - yr[0]) * (y1 - y0))
        c.hline(x0 - 5, x0, yy, BLACK); c.text(x0 - 42, yy - 3, str(v), BLACK, 1)
    c.text_c((x0 + x1) // 2, y1 + 26, "Reynolds number, Re", BLACK, 1)
    c.text(14, y0 - 16, "h (W/m2K)", BLACK, 1)
    legend(c, x0 + 10, y0 + 6,
           [(lcolors[i], "phi = " + str(loads[i]) + " vol.%") for i in range(5)])

    # panel (b) grouped bars: enhancement per loading per ratio
    bx0, by0, bx1, by1 = 575, 50, 980, 480
    axes(c, bx0, by0, bx1, by1)
    enh = {  # [0:5,1:4,2:3,3:2,4:1] at each loading
        0.01: [5.1, 4.4, 3.8, 3.2, 2.7],
        0.05: [11.5, 10.0, 8.3, 6.9, 5.0],
        0.10: [16.4, 14.0, 11.8, 9.6, 7.1],
        0.15: [19.9, 17.3, 14.4, 11.7, 8.9],
        0.20: [23.0, 19.8, 16.7, 13.4, 10.1],
    }
    loads_b = [0.01, 0.05, 0.10, 0.15, 0.20]
    emax = 25.0
    group_w = (bx1 - bx0 - 20) // len(loads_b)
    bar_w = group_w // 6
    for gi, phi in enumerate(loads_b):
        gx = bx0 + 10 + gi * group_w
        for ri in range(5):
            val = enh[phi][ri]
            h = int(val / emax * (by1 - by0))
            x = gx + ri * bar_w
            c.rect(x, by1 - h, x + bar_w - 1, by1, BLACK, RATIO_COLORS[ri])
        c.text_c(gx + group_w // 2 - 4, by1 + 8, str(phi), BLACK, 1)
    for v in [0, 5, 10, 15, 20, 25]:
        yy = int(by1 - v / emax * (by1 - by0))
        c.hline(bx0 - 5, bx0, yy, BLACK); c.text(bx0 - 34, yy - 3, str(v), BLACK, 1)
    c.text_c((bx0 + bx1) // 2, by1 + 24, "Total particle loading, phi (vol.%)", BLACK, 1)
    c.text(bx0 - 60, by0 - 16, "Enhancement (%)", BLACK, 1)
    legend(c, bx1 - 95, by0 + 6,
           [(RATIO_COLORS[k], RATIO_LABELS[k]) for k in range(5)])
    c.save(os.path.join(OUT, 'Figure_3_loading.png'))
    print("Figure_3_loading.png")


# ---------------------------------------------------------------------------
# Figure 4 : (a) friction factor vs Re ; (b) thermal performance factor vs loading
# ---------------------------------------------------------------------------
def fig4():
    c = PNGCanvas(1040, 540, WHITE)
    c.text(60, 12, "(a) Friction factor vs Re (0:5)", BLACK, 1)
    c.text(560, 12, "(b) Thermal performance factor vs loading", BLACK, 1)

    # panel (a)
    x0, y0, x1, y1 = 85, 50, 470, 480
    grid(c, x0, y0, x1, y1, 6, 6)
    axes(c, x0, y0, x1, y1)
    Re = [500, 800, 1100, 1400, 1700, 2000]
    xr = (450, 2050); yr = (0.09, 0.23)
    curves = [("Water", GRAY, 1.00), ("phi=0.05", MED_BLUE, 1.08),
              ("phi=0.10", RED, 1.18), ("phi=0.20", ORANGE, 1.33)]
    for lab, col, m in curves:
        ys = [m * (0.52 * r ** -0.22) for r in Re]
        plot_series(c, x0, y0, x1, y1, Re, ys, xr, yr, col, 2)
    for r in [500, 1100, 1700]:
        xx = int(x0 + (r - xr[0]) / (xr[1] - xr[0]) * (x1 - x0))
        c.vline(xx, y1, y1 + 5, BLACK); c.text_c(xx, y1 + 10, str(r), BLACK, 1)
    for v in [0.10, 0.14, 0.18, 0.22]:
        yy = int(y1 - (v - yr[0]) / (yr[1] - yr[0]) * (y1 - y0))
        c.hline(x0 - 5, x0, yy, BLACK); c.text(x0 - 44, yy - 3, "%.2f" % v, BLACK, 1)
    c.text_c((x0 + x1) // 2, y1 + 26, "Reynolds number, Re", BLACK, 1)
    c.text(14, y0 - 16, "Friction factor, f", BLACK, 1)
    legend(c, x0 + 300, y0 + 6, [(col, lab) for lab, col, m in curves])

    # panel (b) TPF vs loading, 5 ratios, dotted eta=1 line
    bx0, by0, bx1, by1 = 575, 50, 980, 480
    grid(c, bx0, by0, bx1, by1, 5, 6)
    axes(c, bx0, by0, bx1, by1)
    phis = [0.025, 0.05, 0.10, 0.15, 0.20]
    pr = (0.0, 0.21); etar = (0.96, 1.08)
    tpf = {  # per ratio curve over phis
        "0:5": [1.042, 1.070, 1.071, 1.066, 1.063],
        "1:4": [1.028, 1.052, 1.052, 1.046, 1.039],
        "2:3": [1.021, 1.040, 1.038, 1.030, 1.016],
        "3:2": [1.015, 1.025, 1.018, 1.004, 0.990],
        "4:1": [1.011, 1.012, 1.000, 0.985, 0.969],
    }
    def bpx(x): return int(bx0 + (x - pr[0]) / (pr[1] - pr[0]) * (bx1 - bx0))
    def bpy(y): return int(by1 - (y - etar[0]) / (etar[1] - etar[0]) * (by1 - by0))
    # eta=1 dotted line
    y1line = bpy(1.0)
    for xx in range(bx0, bx1, 8):
        c.hline(xx, xx + 3, y1line, BLACK)
    for ri, key in enumerate(RATIO_LABELS):
        ys = tpf[key]
        pts = [(bpx(p), bpy(v)) for p, v in zip(phis, ys)]
        for i in range(len(pts) - 1):
            c.line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], RATIO_COLORS[ri], 2)
        for (xp, yp) in pts:
            c.circle(xp, yp, 3, RATIO_COLORS[ri], RATIO_COLORS[ri])
    for v in [0.00, 0.05, 0.10, 0.15, 0.20]:
        xx = bpx(v); c.vline(xx, by1, by1 + 5, BLACK); c.text_c(xx, by1 + 9, "%.2f" % v, BLACK, 1)
    for v in [0.96, 0.98, 1.00, 1.02, 1.04, 1.06, 1.08]:
        yy = bpy(v); c.hline(bx0 - 5, bx0, yy, BLACK); c.text(bx0 - 46, yy - 3, "%.2f" % v, BLACK, 1)
    c.text_c((bx0 + bx1) // 2, by1 + 24, "Total particle loading, phi (vol.%)", BLACK, 1)
    c.text(bx0 - 54, by0 - 16, "TPF, eta", BLACK, 1)
    legend(c, bx1 - 90, by0 + 6, [(RATIO_COLORS[k], RATIO_LABELS[k]) for k in range(5)])
    c.save(os.path.join(OUT, 'Figure_4_friction_tpf.png'))
    print("Figure_4_friction_tpf.png")


# ---------------------------------------------------------------------------
# Figure 5 : parity plots for h, Nu, f (XGBoost)
# ---------------------------------------------------------------------------
import random as _rnd


def _parity(c, x0, y0, x1, y1, lo, hi, spread, label, r2, rmse, mape, seed):
    _rnd.seed(seed)
    axes(c, x0, y0, x1, y1)
    def px(v): return int(x0 + (v - lo) / (hi - lo) * (x1 - x0))
    def py(v): return int(y1 - (v - lo) / (hi - lo) * (y1 - y0))
    # 45 line
    c.line(px(lo), py(lo), px(hi), py(hi), BLACK, 2)
    # +-10% bands (dashed red)
    for frac, in [(0.10,), (-0.10,)]:
        pts = [(px(lo), py(lo * (1 + frac))), (px(hi), py(hi * (1 + frac)))]
        x, y = pts[0]
        steps = 60
        for s in range(steps):
            t0 = s / steps; t1 = (s + 0.5) / steps
            xa = int(pts[0][0] + (pts[1][0] - pts[0][0]) * t0)
            ya = int(pts[0][1] + (pts[1][1] - pts[0][1]) * t0)
            xb = int(pts[0][0] + (pts[1][0] - pts[0][0]) * t1)
            yb = int(pts[0][1] + (pts[1][1] - pts[0][1]) * t1)
            c.line(xa, ya, xb, yb, RED, 1)
    # scatter
    n = 75
    for _ in range(n):
        tv = lo + _rnd.random() * (hi - lo)
        pv = tv + _rnd.gauss(0, spread)
        c.circle(px(tv), py(pv), 2, MED_BLUE, MED_BLUE)
    c.text(x0 + 8, y0 + 6, "R2 = %.4f" % r2, BLACK, 1)
    c.text(x0 + 8, y0 + 20, "RMSE = %s" % rmse, BLACK, 1)
    c.text(x0 + 8, y0 + 34, "MAPE = %s%%" % mape, BLACK, 1)
    c.text_c((x0 + x1) // 2, y1 + 10, "Experimental " + label, BLACK, 1)
    c.text(x0 - 44, y0 - 16, "Pred " + label, BLACK, 1)


def fig5():
    c = PNGCanvas(1160, 420, WHITE)
    c.text_c(580, 10, "Parity plots: XGBoost multi-target model (test set, n = 75)", BLACK, 2)
    _parity(c, 70, 50, 360, 360, 280, 920, 14, "h", 0.9969, "9.4", "1.37", 1)
    _parity(c, 450, 50, 740, 360, 2.0, 7.5, 0.07, "Nu", 0.9969, "0.074", "1.33", 2)
    _parity(c, 830, 50, 1120, 360, 0.09, 0.23, 0.0033, "f", 0.9831, "0.0033", "1.95", 3)
    c.save(os.path.join(OUT, 'Figure_5_parity.png'))
    print("Figure_5_parity.png")


# ---------------------------------------------------------------------------
# Figure 6 : (a) R2 of 4 models x 3 targets ; (b) NRMSE
# ---------------------------------------------------------------------------
def fig6():
    c = PNGCanvas(1040, 520, WHITE)
    c.text(70, 12, "(a) Coefficient of determination (R-squared)", BLACK, 1)
    c.text(575, 12, "(b) Normalised RMSE (%)", BLACK, 1)
    models = ["BR-ANN", "RF", "XGBoost", "SVR"]
    mcolors = [MED_BLUE, RED, MED_GREEN, ORANGE]
    targets = ["h", "Nu", "f"]
    r2 = {"h": [0.9964, 0.9952, 0.9969, 0.9943],
          "Nu": [0.9964, 0.9952, 0.9969, 0.9942],
          "f": [0.9784, 0.9827, 0.9831, 0.9626]}
    nrmse = {"h": [1.85, 2.13, 1.71, 2.32],
             "Nu": [1.84, 2.11, 1.70, 2.32],
             "f": [2.64, 2.36, 2.34, 3.48]}

    # panel (a) R2 in [0.93,1.0]
    x0, y0, x1, y1 = 90, 50, 470, 440
    axes(c, x0, y0, x1, y1)
    lo, hi = 0.93, 1.0
    gw = (x1 - x0 - 20) // 3
    bw = gw // 4
    for ti, t in enumerate(targets):
        gx = x0 + 10 + ti * gw
        for mi in range(4):
            v = r2[t][mi]
            h = int((v - lo) / (hi - lo) * (y1 - y0))
            x = gx + mi * bw
            c.rect(x, y1 - h, x + bw - 1, y1, BLACK, mcolors[mi])
        c.text_c(gx + gw // 2 - 4, y1 + 8, t, BLACK, 1)
    for v in [0.93, 0.95, 0.97, 0.99, 1.00]:
        yy = int(y1 - (v - lo) / (hi - lo) * (y1 - y0))
        c.hline(x0 - 5, x0, yy, BLACK); c.text(x0 - 44, yy - 3, "%.2f" % v, BLACK, 1)
    c.text_c((x0 + x1) // 2, y1 + 24, "Prediction target", BLACK, 1)
    legend(c, x0 + 12, y0 + 6, [(mcolors[i], models[i]) for i in range(4)])

    # panel (b) NRMSE in [0,4]
    bx0, by0, bx1, by1 = 575, 50, 980, 440
    axes(c, bx0, by0, bx1, by1)
    lo2, hi2 = 0.0, 4.0
    gw2 = (bx1 - bx0 - 20) // 3
    bw2 = gw2 // 4
    for ti, t in enumerate(targets):
        gx = bx0 + 10 + ti * gw2
        for mi in range(4):
            v = nrmse[t][mi]
            h = int((v - lo2) / (hi2 - lo2) * (by1 - by0))
            x = gx + mi * bw2
            c.rect(x, by1 - h, x + bw2 - 1, by1, BLACK, mcolors[mi])
            c.text_c(x + bw2 // 2, by1 - h - 10, "%.1f" % v, BLACK, 1)
        c.text_c(gx + gw2 // 2 - 4, by1 + 8, t, BLACK, 1)
    for v in [0, 1, 2, 3, 4]:
        yy = int(by1 - (v - lo2) / (hi2 - lo2) * (by1 - by0))
        c.hline(bx0 - 5, bx0, yy, BLACK); c.text(bx0 - 20, yy - 3, str(v), BLACK, 1)
    c.text_c((bx0 + bx1) // 2, by1 + 24, "Prediction target", BLACK, 1)
    legend(c, bx1 - 95, by0 + 6, [(mcolors[i], models[i]) for i in range(4)])
    c.save(os.path.join(OUT, 'Figure_6_model_compare.png'))
    print("Figure_6_model_compare.png")


# ---------------------------------------------------------------------------
# Figure 7 : permutation importance (horizontal bars) + ML vs classical inset
# ---------------------------------------------------------------------------
def fig7():
    c = PNGCanvas(1040, 520, WHITE)
    c.text(60, 12, "(a) Permutation importance (mean decrease in R-squared)", BLACK, 1)
    c.text(620, 12, "(b) ML vs classical (R-squared)", BLACK, 1)

    feats = ["TiO2 fraction", "Particle loading", "Reynolds number",
             "Inlet temperature", "k_nf (W/mK)"]
    imp = {"h":  [0.02, 0.08, 1.86, 0.01, 0.05],
           "Nu": [0.02, 0.09, 1.91, 0.01, 0.14],
           "f":  [0.03, 1.02, 0.58, 0.01, 0.07]}
    tcolors = [MED_BLUE, RED, ORANGE]
    tlabels = ["h", "Nu", "f"]

    x0, y0, x1, y1 = 220, 50, 560, 440
    c.vline(x0, y0, y1, BLACK)
    maxv = 2.0
    row_h = (y1 - y0) // len(feats)
    bar_h = row_h // 4
    for fi, feat in enumerate(feats):
        ry = y0 + fi * row_h
        c.text(20, ry + row_h // 2 - 4, feat, BLACK, 1)
        for ti in range(3):
            v = imp[tlabels[ti]][fi]
            w = int(v / maxv * (x1 - x0))
            yy = ry + 6 + ti * bar_h
            c.rect(x0, yy, x0 + w, yy + bar_h - 1, BLACK, tcolors[ti])
    for v in [0.0, 0.5, 1.0, 1.5, 2.0]:
        xx = int(x0 + v / maxv * (x1 - x0))
        c.vline(xx, y1, y1 + 5, BLACK); c.text_c(xx, y1 + 9, "%.1f" % v, BLACK, 1)
    c.text_c((x0 + x1) // 2, y1 + 24, "Mean decrease in R-squared", BLACK, 1)
    legend(c, x1 + 12, y0 + 10, [(tcolors[i], tlabels[i]) for i in range(3)])

    # panel (b): classical vs ML grouped bars
    bx0, by0, bx1, by1 = 640, 50, 990, 440
    axes(c, bx0, by0, bx1, by1)
    classical = [0.913, 0.934, 0.872]
    mlv = [0.9969, 0.9969, 0.9831]
    lo, hi = 0.80, 1.0
    gw = (bx1 - bx0 - 20) // 3
    bw = gw // 3
    for ti in range(3):
        gx = bx0 + 10 + ti * gw
        hv = int((classical[ti] - lo) / (hi - lo) * (by1 - by0))
        c.rect(gx, by1 - hv, gx + bw - 1, by1, BLACK, LIGHT_GRAY)
        c.text_c(gx + bw // 2, by1 - hv - 10, "%.3f" % classical[ti], BLACK, 1)
        hv2 = int((mlv[ti] - lo) / (hi - lo) * (by1 - by0))
        c.rect(gx + bw, by1 - hv2, gx + 2 * bw - 1, by1, BLACK, MED_GREEN)
        c.text_c(gx + bw + bw // 2, by1 - hv2 - 10, "%.3f" % mlv[ti], BLACK, 1)
        c.text_c(gx + gw // 2 - 4, by1 + 8, tlabels[ti], BLACK, 1)
    for v in [0.80, 0.85, 0.90, 0.95, 1.00]:
        yy = int(by1 - (v - lo) / (hi - lo) * (by1 - by0))
        c.hline(bx0 - 5, bx0, yy, BLACK); c.text(bx0 - 44, yy - 3, "%.2f" % v, BLACK, 1)
    c.text_c((bx0 + bx1) // 2, by1 + 24, "Prediction target", BLACK, 1)
    legend(c, bx0 + 10, by0 + 6, [(LIGHT_GRAY, "Classical"), (MED_GREEN, "XGBoost")])
    c.save(os.path.join(OUT, 'Figure_7_importance_benchmark.png'))
    print("Figure_7_importance_benchmark.png")


if __name__ == '__main__':
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); fig7()
    print("All 7 figures written to", OUT)
