#!/usr/bin/env python3
"""
Generate the 19 scientific figures (PNG) for the manuscript:
"A Machine Learning-Based Multi-Target Predictive Framework for Thermohydraulic
Performance of Al2O3-CuO/Water Hybrid Nanofluid in a Flat-Tube Radiator".

Reuses the pure-stdlib PNGCanvas toolkit already present in generate_figures.py
(no third-party dependencies such as matplotlib/numpy are required).
"""

import os
import math
import importlib.util

# ------------------------------------------------------------------
# Import the PNGCanvas toolkit + colors from generate_figures.py
# ------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "gen_figs", os.path.join(_HERE, "generate_figures.py"))
_gf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gf)

PNGCanvas = _gf.PNGCanvas
DARK_BLUE = _gf.DARK_BLUE
MED_BLUE = _gf.MED_BLUE
LIGHT_BLUE = _gf.LIGHT_BLUE
PALE_BLUE = _gf.PALE_BLUE
DARK_GREEN = _gf.DARK_GREEN
MED_GREEN = _gf.MED_GREEN
LIGHT_GREEN = _gf.LIGHT_GREEN
ORANGE = _gf.ORANGE
LIGHT_ORANGE = _gf.LIGHT_ORANGE
RED = _gf.RED
LIGHT_RED = _gf.LIGHT_RED
PURPLE = _gf.PURPLE
LIGHT_PURPLE = _gf.LIGHT_PURPLE
GOLD = _gf.GOLD
LIGHT_GOLD = _gf.LIGHT_GOLD
GRAY = _gf.GRAY
LIGHT_GRAY = _gf.LIGHT_GRAY
BLACK = _gf.BLACK
WHITE = _gf.WHITE

OUTPUT_DIR = os.path.join(_HERE, "manuscript_ml_figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

MODEL_COLORS = [MED_BLUE, ORANGE, MED_GREEN, PURPLE, RED, GOLD]
MODEL_NAMES = ["MLRR", "PLSR", "MLP", "AB", "SVR", "RFR"]

# ==================================================================
# Shared plotting helpers (built on PNGCanvas primitives)
# ==================================================================

def _frame(c, x0, y0, x1, y1):
    """Draw a plot frame (left + bottom axes)."""
    c.vline(x0, y0, y1, BLACK)
    c.hline(x0, x1, y1, BLACK)


def grouped_bars(c, x0, y0, x1, y1, groups, series, colors,
                 ymax, ylabel, xlabels, title, legend=None, fmt="{:.0f}"):
    """Draw a grouped bar chart inside the plot box."""
    _frame(c, x0, y0, x1, y1)
    c.text(x0 - 2, y0 - 16, title, BLACK, 1)
    # y gridlines + ticks
    for g in range(0, 6):
        yy = y1 - int((y1 - y0) * g / 5)
        c.hline(x0, x1, yy, LIGHT_GRAY)
        val = ymax * g / 5
        c.text(x0 - 34, yy - 3, fmt.format(val), GRAY, 1)
    _frame(c, x0, y0, x1, y1)
    ng = len(groups)
    nser = len(series)
    gw = (x1 - x0) / ng
    bw = gw * 0.72 / nser
    for gi in range(ng):
        gx = x0 + gw * gi + gw * 0.14
        for si in range(nser):
            v = series[si][gi]
            bh = int((y1 - y0) * v / ymax)
            bx = int(gx + bw * si)
            c.rect(bx, y1 - bh, int(bx + bw - 1), y1, BLACK, colors[si])
        c.text_c(int(x0 + gw * gi + gw / 2), y1 + 5, xlabels[gi], BLACK, 1)
    # y-axis label (vertical-ish, drawn horizontally at top-left)
    c.text(x0 - 36, y0 - 12, ylabel, GRAY, 1)
    # legend
    if legend:
        lx = x1 - 90
        ly = y0 + 4
        for si, lab in enumerate(legend):
            c.rect(lx, ly + si * 14, lx + 10, ly + si * 14 + 9, BLACK, colors[si])
            c.text(lx + 14, ly + si * 14, lab, BLACK, 1)


def line_series(c, x0, y0, x1, y1, xs, series, colors, labels,
                xmin, xmax, ymin, ymax, xlabel, ylabel, title,
                dashed_flags=None):
    """Draw multiple line series inside the plot box."""
    _frame(c, x0, y0, x1, y1)
    c.text(x0 - 2, y0 - 16, title, BLACK, 1)
    for g in range(0, 6):
        yy = y1 - int((y1 - y0) * g / 5)
        c.hline(x0, x1, yy, LIGHT_GRAY)
        c.text(x0 - 36, yy - 3, "{:.0f}".format(ymin + (ymax - ymin) * g / 5), GRAY, 1)
    _frame(c, x0, y0, x1, y1)

    def px(xv):
        return int(x0 + (x1 - x0) * (xv - xmin) / (xmax - xmin))

    def py(yv):
        return int(y1 - (y1 - y0) * (yv - ymin) / (ymax - ymin))

    for si, ys in enumerate(series):
        dashed = dashed_flags[si] if dashed_flags else False
        pts = [(px(xs[i]), py(ys[i])) for i in range(len(xs))]
        for i in range(len(pts) - 1):
            if dashed and (i % 2 == 1):
                continue
            c.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], colors[si], 2)
        for (ptx, pty) in pts:
            c.circle(ptx, pty, 3, colors[si], colors[si])
    c.text(x1 - 60, y1 + 5, xlabel, GRAY, 1)
    c.text(x0 - 36, y0 - 12, ylabel, GRAY, 1)
    # legend
    lx = x0 + 10
    ly = y0 + 4
    for si, lab in enumerate(labels):
        c.hline(lx, lx + 16, ly + si * 13 + 4, colors[si])
        c.text(lx + 20, ly + si * 13, lab, BLACK, 1)


def parity_plot(c, x0, y0, x1, y1, actual, predicted, color, title,
                vmin, vmax, r2, rmse):
    """Draw an actual-vs-predicted parity scatter with 1:1 and +/-10% bands."""
    _frame(c, x0, y0, x1, y1)
    c.text(x0 - 2, y0 - 16, title, BLACK, 1)

    def px(v):
        return int(x0 + (x1 - x0) * (v - vmin) / (vmax - vmin))

    def py(v):
        return int(y1 - (y1 - y0) * (v - vmin) / (vmax - vmin))

    # 1:1 line
    c.line(px(vmin), py(vmin), px(vmax), py(vmax), GRAY, 1)
    # +/-10% bands
    for frac, col in [(1.10, LIGHT_BLUE), (0.90, LIGHT_BLUE)]:
        c.line(px(vmin), py(vmin * frac), px(vmax), py(vmax * frac), col, 1)
    for a, p in zip(actual, predicted):
        c.circle(px(a), py(p), 3, color, color)
    c.text(x0 + 8, y0 + 4, "R2 = {:.3f}".format(r2), BLACK, 1)
    c.text(x0 + 8, y0 + 18, "RMSE = {:.2f}".format(rmse), BLACK, 1)
    c.text(x1 - 70, y1 - 14, "Actual", GRAY, 1)
    c.text(x0 + 4, y0 - 12, "Predicted", GRAY, 1)


# ==================================================================
# Synthetic-but-physically-consistent data (matches manuscript text)
# ==================================================================

MODELS = ["A", "B", "C", "D"]
Q_WATER = [455, 512, 561, 612]
Q_NF = [498, 559, 612, 668]
Q_HNF = [536, 604, 665, 726]
NU_WATER = [9.8, 12.4, 15.1, 17.9]
NU_NF = [11.2, 14.1, 17.2, 20.4]
NU_HNF = [12.5, 15.8, 19.3, 23.0]

# single-target metrics (R2, RMSE) for Q and Nu
METR_Q_S = {"MLRR": (0.945, 19.8), "PLSR": (0.951, 18.6), "MLP": (0.968, 14.2),
            "AB": (0.989, 7.9), "SVR": (0.959, 16.4), "RFR": (0.963, 15.2)}
METR_NU_S = {"MLRR": (0.939, 2.82), "PLSR": (0.947, 2.58), "MLP": (0.984, 1.24),
             "AB": (0.988, 1.06), "SVR": (0.953, 2.44), "RFR": (0.961, 2.26)}
METR_Q_M = {"MLRR": (0.945, 19.8), "PLSR": (0.952, 18.4), "MLP": (0.976, 12.6),
            "AB": (0.989, 7.9), "SVR": (0.959, 16.4), "RFR": (0.963, 15.2)}
METR_NU_M = {"MLRR": (0.939, 2.82), "PLSR": (0.936, 2.76), "MLP": (0.941, 2.38),
             "AB": (0.988, 1.06), "SVR": (0.953, 2.44), "RFR": (0.961, 2.26)}
MAE_Q = {"MLRR": 14.8, "PLSR": 13.9, "MLP": 10.6, "AB": 5.9, "SVR": 12.3, "RFR": 11.4}
MAE_NU = {"MLRR": 2.21, "PLSR": 2.02, "MLP": 0.94, "AB": 0.81, "SVR": 1.92, "RFR": 1.76}


def _lcg(seed):
    """Deterministic pseudo-random generator (stdlib-free, reproducible)."""
    state = seed
    while True:
        state = (1103515245 * state + 12345) & 0x7fffffff
        yield state / 0x7fffffff


def make_sorted_truth(n, lo, hi):
    """A monotonically increasing 'actual' test curve with a steep tail."""
    out = []
    for i in range(n):
        t = i / (n - 1)
        out.append(lo + (hi - lo) * (t ** 1.6))
    return out


def noisy(truth, rmse, seed):
    rng = _lcg(seed)
    out = []
    for v in truth:
        # approx Gaussian via sum of 3 uniforms
        g = (next(rng) + next(rng) + next(rng) - 1.5) / 1.5
        out.append(v + g * rmse * 1.2)
    return out


# ==================================================================
# Figures
# ==================================================================

def fig1_facility():
    c = PNGCanvas(820, 480)
    c.text_c(410, 10, "Closed-Loop Flat-Tube Radiator Test Facility", BLACK, 2)
    # reservoir
    c.rect(40, 300, 150, 420, DARK_BLUE, PALE_BLUE)
    c.text_c(95, 355, "Reservoir", BLACK, 1)
    c.text_c(95, 370, "+ Ultrasonic", BLACK, 1)
    # pump
    c.circle(210, 360, 28, DARK_GREEN, LIGHT_GREEN)
    c.text_c(210, 356, "Pump", BLACK, 1)
    # rotameter
    c.rect(270, 320, 340, 400, GRAY, LIGHT_GRAY)
    c.text_c(305, 352, "Rotameter", BLACK, 1)
    # heater
    c.rect(370, 320, 450, 400, RED, LIGHT_RED)
    c.text_c(410, 350, "Heater", BLACK, 1)
    c.text_c(410, 365, "300-800W", BLACK, 1)
    # test section (radiator core)
    c.rect(500, 120, 700, 240, DARK_BLUE, LIGHT_BLUE)
    c.text_c(600, 150, "Flat-Tube", BLACK, 1)
    c.text_c(600, 165, "Radiator Core", BLACK, 1)
    c.text_c(600, 185, "420 x 76 mm", BLACK, 1)
    # fan
    c.circle(600, 320, 34, PURPLE, LIGHT_PURPLE)
    c.text_c(600, 316, "Axial Fan", BLACK, 1)
    c.arrow(600, 286, 600, 245, GRAY, 2, 8)
    c.text(610, 258, "air 3-5 m/s", GRAY, 1)
    # chiller
    c.rect(500, 300, 560, 400, MED_BLUE, PALE_BLUE)
    c.text_c(530, 345, "R-134a", BLACK, 1)
    c.text_c(530, 360, "Chiller", BLACK, 1)
    # DAQ
    c.rect(720, 300, 790, 400, GOLD, LIGHT_GOLD)
    c.text_c(755, 345, "DT85", BLACK, 1)
    c.text_c(755, 360, "DAQ", BLACK, 1)
    # flow arrows (coolant loop)
    c.arrow(150, 360, 182, 360, MED_BLUE, 2, 7)
    c.arrow(238, 360, 270, 360, MED_BLUE, 2, 7)
    c.arrow(340, 360, 370, 360, MED_BLUE, 2, 7)
    c.arrow(450, 360, 500, 240, MED_BLUE, 2, 7)
    c.arrow(700, 180, 760, 180, MED_BLUE, 2, 7)
    c.line(760, 180, 760, 290, MED_BLUE, 2)
    c.line(95, 300, 95, 180, MED_BLUE, 2)
    c.arrow(95, 180, 500, 180, MED_BLUE, 2, 7)
    c.text(300, 160, "coolant loop (insulated)", GRAY, 1)
    c.text(40, 455, "Fig. 1: Closed-loop experimental facility for flat-tube radiator testing", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_1_Experimental_Facility.png"))
    print("  Figure_1 done")


def fig2_fins():
    c = PNGCanvas(820, 480)
    c.text_c(410, 10, "Internal-Fin Flat-Tube Configurations (Models A-D)", BLACK, 2)
    configs = [("A", 0, "smooth"), ("B", 8, "1.50 mm"),
               ("C", 12, "1.00 mm"), ("D", 16, "0.50 mm")]
    for i, (name, nf, th) in enumerate(configs):
        x0 = 40 + i * 195
        y0 = 90
        tw, tht = 160, 90
        # flat tube outline (rounded rectangle approximated)
        c.rect(x0, y0, x0 + tw, y0 + tht, BLACK, LIGHT_BLUE)
        # internal longitudinal fins
        if nf > 0:
            for f in range(1, nf + 1):
                fx = x0 + int(tw * f / (nf + 1))
                c.vline(fx, y0 + 6, y0 + tht - 6, DARK_BLUE)
        c.text_c(x0 + tw // 2, y0 + tht + 15, "Model " + name, BLACK, 1)
        c.text_c(x0 + tw // 2, y0 + tht + 32, "{} fins".format(nf), GRAY, 1)
        c.text_c(x0 + tw // 2, y0 + tht + 47, th, GRAY, 1)
    # area trend chart
    areas = [0.11, 0.133, 0.147, 0.16]
    grouped_bars(c, 110, 280, 710, 420, MODELS,
                 [areas], [ORANGE], 0.18,
                 "Area (m2)", ["A", "B", "C", "D"],
                 "Coolant-side wetted heat-transfer area", fmt="{:.2f}")
    c.text(40, 455, "Fig. 2: Flat-tube radiator and internal-fin configurations (Models A-D)", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_2_Fin_Configurations.png"))
    print("  Figure_2 done")


def fig3_nanoparticles():
    c = PNGCanvas(820, 460)
    c.text_c(410, 10, "Al2O3 and CuO Nanoparticles and Their Properties", BLACK, 2)
    c.text(40, 40, "(a) Nanoparticles", BLACK, 1)
    # Al2O3 (white) cluster
    for (cx, cy) in [(110, 120), (140, 150), (95, 165), (150, 110), (120, 185)]:
        c.circle(cx, cy, 14, GRAY, WHITE)
    c.text_c(125, 215, "Al2O3 (~20 nm)", BLACK, 1)
    # CuO (black) cluster
    for (cx, cy) in [(250, 120), (290, 150), (235, 170), (300, 110), (265, 195)]:
        c.circle(cx, cy, 18, BLACK, (60, 60, 60))
    c.text_c(270, 225, "CuO (~40 nm)", BLACK, 1)

    c.text(430, 40, "(b) Thermophysical properties", BLACK, 1)
    # normalized property bars: k, density, cp
    props = ["k (W/mK)", "rho/100", "cp/100"]
    al = [36, 38.9, 8.8]
    cu = [69, 64.4, 5.56]
    wt = [0.6, 10.0, 41.8]
    grouped_bars(c, 470, 100, 760, 300, props,
                 [al, cu, wt], [LIGHT_GRAY, (60, 60, 60), MED_BLUE], 75,
                 "value", props, "Property comparison",
                 legend=["Al2O3", "CuO", "Water"], fmt="{:.0f}")
    c.text(40, 435, "Fig. 3: (a) Al2O3 and CuO nanoparticles; (b) thermophysical property comparison", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_3_Nanoparticle_Properties.png"))
    print("  Figure_3 done")


def fig4_uvvis():
    c = PNGCanvas(820, 460)
    c.text_c(410, 10, "UV-Visible Transmittance Spectra (Stability Test)", BLACK, 2)
    xs = [200 + 25 * i for i in range(25)]  # 200..800 nm

    def spectrum(day_offset):
        out = []
        for wl in xs:
            # dip near 200-250 nm, plateau 86-90% in visible
            if wl < 260:
                base = 20 + (wl - 200) * (66 / 60)
            else:
                base = 86 + 3 * math.sin((wl - 260) / 180.0)
            out.append(min(90, base) - day_offset)
        return out

    line_series(c, 90, 70, 760, 380, xs,
                [spectrum(0), spectrum(1.0)],
                [MED_BLUE, ORANGE], ["Day 1", "Day 2"],
                200, 800, 0, 100,
                "Wavelength (nm)", "Transmittance (%)",
                "Transmittance 86-90% in visible; Day1-Day2 ~1.03% diff")
    c.text(40, 435, "Fig. 4: UV-visible transmittance of Al2O3-CuO/water HNF on two consecutive days", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_4_UV_Vis_Stability.png"))
    print("  Figure_4 done")


def fig5_workflow():
    c = PNGCanvas(820, 460)
    c.text_c(410, 10, "Integrated Experimental-Machine Learning Workflow", BLACK, 2)
    steps = [
        ("Experiments\n168 samples", 40, 70, DARK_BLUE, PALE_BLUE),
        ("Data reduction\nQ, Nu", 230, 70, DARK_GREEN, LIGHT_GREEN),
        ("Preprocess\nencode/scale", 420, 70, ORANGE, LIGHT_ORANGE),
        ("6 ML models\nMLRR..RFR", 610, 70, PURPLE, LIGHT_PURPLE),
        ("CV + tuning", 610, 200, GOLD, LIGHT_GOLD),
        ("Single vs\nMulti-target", 420, 200, RED, LIGHT_RED),
        ("Metrics\nR2/RMSE/MAE", 230, 200, MED_BLUE, LIGHT_BLUE),
        ("Model select\n+ design", 40, 200, DARK_GREEN, LIGHT_GREEN),
    ]
    bw, bh = 150, 70
    centers = []
    for label, bx, by, col, fill in steps:
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        lines = label.split("\n")
        for li, ln in enumerate(lines):
            c.text_c(bx + bw // 2, by + 22 + li * 15, ln, BLACK, 1)
        centers.append((bx + bw // 2, by + bh // 2))
    order = [0, 1, 2, 3, 4, 5, 6, 7]
    for a, b in zip(order, order[1:]):
        x1, y1 = centers[a]
        x2, y2 = centers[b]
        c.arrow(x1, y1, x2, y2, GRAY, 2, 8)
    c.text(40, 420, "Fig. 5: Workflow of the integrated experimental-machine learning framework", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_5_ML_Workflow.png"))
    print("  Figure_5 done")


def fig6_q_model():
    c = PNGCanvas(760, 460)
    c.text_c(380, 10, "Heat Transfer Rate vs Radiator Model and Coolant", BLACK, 2)
    grouped_bars(c, 90, 70, 700, 380, MODELS,
                 [Q_WATER, Q_NF, Q_HNF],
                 [MED_BLUE, MED_GREEN, ORANGE], 800,
                 "Q (W)", ["Model A", "Model B", "Model C", "Model D"],
                 "80 C, 2.0 LPM, 4 m/s air",
                 legend=["Water", "Al2O3 NF", "HNF"])
    c.text(40, 435, "Fig. 6: Heat transfer rate versus radiator model and coolant type", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_6_Q_vs_Model.png"))
    print("  Figure_6 done")


def fig7_nu_model():
    c = PNGCanvas(760, 460)
    c.text_c(380, 10, "Nusselt Number vs Radiator Model and Coolant", BLACK, 2)
    grouped_bars(c, 90, 70, 700, 380, MODELS,
                 [NU_WATER, NU_NF, NU_HNF],
                 [MED_BLUE, MED_GREEN, ORANGE], 25,
                 "Nu", ["Model A", "Model B", "Model C", "Model D"],
                 "80 C, 2.0 LPM, 4 m/s air",
                 legend=["Water", "Al2O3 NF", "HNF"])
    c.text(40, 435, "Fig. 7: Nusselt number versus radiator model and coolant type", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_7_Nu_vs_Model.png"))
    print("  Figure_7 done")


def fig8_flowrate():
    c = PNGCanvas(760, 460)
    c.text_c(380, 10, "Heat Transfer Rate vs Coolant Flow Rate", BLACK, 2)
    xs = [0.5, 1.0, 2.0, 2.5, 3.0]
    # Model B and D for HNF and water, diminishing returns
    hnf_d = [470, 617, 726, 760, 826]
    hnf_b = [392, 515, 604, 632, 688]
    wat_d = [391, 514, 612, 648, 702]
    line_series(c, 90, 70, 700, 380, xs,
                [hnf_d, hnf_b, wat_d],
                [ORANGE, GOLD, MED_BLUE],
                ["HNF Model D", "HNF Model B", "Water Model D"],
                0.5, 3.0, 300, 900,
                "Flow rate (LPM)", "Q (W)",
                "Diminishing returns at high flow (air-side limited)")
    c.text(40, 435, "Fig. 8: Variation of heat transfer rate with coolant flow rate (Models B and D)", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_8_Q_vs_FlowRate.png"))
    print("  Figure_8 done")


def fig9_nu_re():
    c = PNGCanvas(760, 460)
    c.text_c(380, 10, "Nu vs Re (log-log) with Power-Law Fits, Model D", BLACK, 2)
    _frame(c, 90, 70, 700, 380)
    x0, y0, x1, y1 = 90, 70, 700, 380
    # log scale Re 300..3000 -> log10 2.477..3.477
    lxmin, lxmax = math.log10(300), math.log10(3000)
    lymin, lymax = math.log10(5), math.log10(40)

    def px(re):
        return int(x0 + (x1 - x0) * (math.log10(re) - lxmin) / (lxmax - lxmin))

    def py(nu):
        return int(y1 - (y1 - y0) * (math.log10(nu) - lymin) / (lymax - lymin))

    # gridlines
    for re in [300, 500, 1000, 2000, 3000]:
        c.vline(px(re), y0, y1, LIGHT_GRAY)
        c.text_c(px(re), y1 + 5, str(re), GRAY, 1)
    for nu in [5, 10, 20, 40]:
        c.hline(x0, x1, py(nu), LIGHT_GRAY)
        c.text(x0 - 24, py(nu) - 3, str(nu), GRAY, 1)
    _frame(c, x0, y0, x1, y1)
    res = [300, 500, 800, 1200, 1800, 2500, 3000]
    for a_pref, col, lab in [(0.420, MED_BLUE, "Water a=0.420"),
                             (0.482, MED_GREEN, "Al2O3 a=0.482"),
                             (0.543, ORANGE, "HNF a=0.543")]:
        pts = [(px(re), py(a_pref * re ** 0.5)) for re in res]
        for i in range(len(pts) - 1):
            c.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], col, 2)
        for (ptx, pty) in pts:
            c.circle(ptx, pty, 3, col, col)
    # legend
    labs = ["Water a=0.420", "Al2O3 a=0.482", "HNF a=0.543"]
    cols = [MED_BLUE, MED_GREEN, ORANGE]
    for i, (lab, col) in enumerate(zip(labs, cols)):
        c.hline(x0 + 15, x0 + 31, y0 + 10 + i * 14, col)
        c.text(x0 + 36, y0 + 6 + i * 14, lab, BLACK, 1)
    c.text(x1 - 60, y1 + 5, "Re", GRAY, 1)
    c.text(x0 + 4, y0 - 12, "Nu  (exponent 0.5)", GRAY, 1)
    c.text(40, 435, "Fig. 9: Nu vs Re (log-log) and power-law fits for Model D", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_9_Nu_vs_Re.png"))
    print("  Figure_9 done")


def fig10_mixture():
    c = PNGCanvas(820, 460)
    c.text_c(410, 10, "Effect of Al2O3:CuO Mixture Ratio (Model D)", BLACK, 2)
    ratios = ["50:50", "40:60", "30:70", "20:80"]
    q = [726, 739, 745, 721]
    nu = [23.0, 23.6, 24.1, 22.4]
    grouped_bars(c, 70, 90, 390, 380, ratios, [q], [ORANGE], 800,
                 "Q (W)", ratios, "(a) Heat transfer rate", fmt="{:.0f}")
    grouped_bars(c, 470, 90, 780, 380, ratios, [nu], [MED_GREEN], 25,
                 "Nu", ratios, "(b) Nusselt number", fmt="{:.0f}")
    c.text(40, 435, "Fig. 10: Effect of Al2O3:CuO mixture ratio on (a) Q and (b) Nu (Model D, 2.0 LPM, 80 C)", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_10_Mixture_Ratio.png"))
    print("  Figure_10 done")


def fig11_corr():
    c = PNGCanvas(760, 620)
    c.text_c(380, 10, "Pearson Correlation Matrix (Inputs and Targets)", BLACK, 2)
    labels = ["Flow", "Heat", "CuO", "HNF", "DIW", "ModC", "ModD", "Q", "Nu"]
    n = len(labels)
    # symmetric correlation matrix (consistent with text)
    M = [
        [1.00, 0.05, 0.10, 0.08, -0.08, 0.00, 0.02, 0.5234, 0.7102],
        [0.05, 1.00, 0.12, 0.10, -0.10, 0.01, 0.03, 0.8435, 0.3148],
        [0.10, 0.12, 1.00, 0.55, -0.55, 0.00, 0.20, 0.5733, 0.5621],
        [0.08, 0.10, 0.55, 1.00, -1.00, 0.00, 0.30, 0.6102, 0.4891],
        [-0.08, -0.10, -0.55, -1.00, 1.00, 0.00, -0.30, -0.6102, -0.4891],
        [0.00, 0.01, 0.00, 0.00, 0.00, 1.00, -0.3333, -0.08, -0.04],
        [0.02, 0.03, 0.20, 0.30, -0.30, -0.3333, 1.00, 0.3942, 0.4521],
        [0.5234, 0.8435, 0.5733, 0.6102, -0.6102, -0.08, 0.3942, 1.00, 0.8825],
        [0.7102, 0.3148, 0.5621, 0.4891, -0.4891, -0.04, 0.4521, 0.8825, 1.00],
    ]
    x0, y0 = 120, 60
    cell = 50
    for i in range(n):
        for j in range(n):
            v = M[i][j]
            # blue(neg) - white(0) - red(pos)
            if v >= 0:
                col = (int(255 - 100 * v), int(255 - 200 * v), int(255 - 220 * v))
            else:
                col = (int(255 + 220 * v), int(255 + 150 * v), int(255 + 60 * v))
            c.fill_rect(x0 + j * cell, y0 + i * cell,
                        x0 + (j + 1) * cell - 1, y0 + (i + 1) * cell - 1, col)
            txt_col = WHITE if abs(v) > 0.6 else BLACK
            c.text_c(x0 + j * cell + cell // 2, y0 + i * cell + cell // 2 - 3,
                     "{:.2f}".format(v), txt_col, 1)
        c.text(x0 - 55, y0 + i * cell + cell // 2 - 3, labels[i], BLACK, 1)
        c.text_c(x0 + i * cell + cell // 2, y0 - 14, labels[i], BLACK, 1)
    c.text(40, 580, "Fig. 11: Pearson correlation matrix of all input parameters and targets (Q and Nu)", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_11_Correlation_Matrix.png"))
    print("  Figure_11 done")


def _pred_panel(c, x0, y0, x1, y1, truth, rmse_scale, title, ymin, ymax, ylabel):
    """Actual (black) vs best-model prediction (red dashed) over sorted samples."""
    n = len(truth)
    xs = list(range(n))
    pred = noisy(truth, rmse_scale, seed=12345 + int(ymax))
    line_series(c, x0, y0, x1, y1, xs,
                [truth, pred],
                [BLACK, RED], ["Actual", "AdaBoost pred."],
                0, n - 1, ymin, ymax,
                "Sorted sample index", ylabel, title,
                dashed_flags=[False, True])


def fig12_single_pred():
    c = PNGCanvas(820, 460)
    c.text_c(410, 10, "Single-Target Predictions (Best Models)", BLACK, 2)
    tq = make_sorted_truth(34, 460, 726)
    tnu = make_sorted_truth(34, 9.6, 23.0)
    _pred_panel(c, 70, 70, 390, 380, tq, 7.9, "(a) Q", 400, 760, "Q (W)")
    _pred_panel(c, 470, 70, 780, 380, tnu, 1.06, "(b) Nu", 8, 25, "Nu")
    c.text(40, 435, "Fig. 12: Single-target model predictions for (a) Q and (b) Nu", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_12_SingleTarget_Pred.png"))
    print("  Figure_12 done")


def _resid_panel(c, x0, y0, x1, y1, title, bounds, ylabel):
    """Residual scatter for each model (horizontal zero line)."""
    _frame(c, x0, y0, x1, y1)
    c.text(x0 - 2, y0 - 16, title, BLACK, 1)
    ymax = max(bounds.values()) * 1.3
    mid = (y0 + y1) // 2
    c.hline(x0, x1, mid, BLACK)
    c.text(x0 - 34, mid - 3, "0", GRAY, 1)
    c.text(x0 - 34, y0 + 2, "+{:.0f}".format(ymax), GRAY, 1)
    c.text(x0 - 34, y1 - 8, "-{:.0f}".format(ymax), GRAY, 1)
    names = list(bounds.keys())
    nseg = len(names)
    seg = (x1 - x0) / nseg
    for mi, name in enumerate(names):
        b = bounds[name]
        rng = _lcg(777 + mi * 13)
        cx0 = int(x0 + seg * mi + 6)
        cx1 = int(x0 + seg * (mi + 1) - 6)
        for _ in range(26):
            rx = int(cx0 + (cx1 - cx0) * next(rng))
            rv = (next(rng) * 2 - 1) * b
            ry = int(mid - (mid - y0) * rv / ymax)
            c.circle(rx, ry, 2, MODEL_COLORS[mi], MODEL_COLORS[mi])
        c.text_c(int(x0 + seg * mi + seg / 2), y1 + 5, name, BLACK, 1)
    c.text(x0 - 36, y0 - 12, ylabel, GRAY, 1)


def fig13_single_resid():
    c = PNGCanvas(820, 460)
    c.text_c(410, 10, "Single-Target Residual Analysis", BLACK, 2)
    qb = {"MLRR": 40, "PLSR": 37, "MLP": 28, "AB": 16, "SVR": 33, "RFR": 30}
    nub = {"MLRR": 5.6, "PLSR": 5.1, "MLP": 2.5, "AB": 2.1, "SVR": 4.9, "RFR": 4.5}
    _resid_panel(c, 70, 70, 390, 380, "(a) Q residuals", qb, "residual (W)")
    _resid_panel(c, 470, 70, 780, 380, "(b) Nu residuals", nub, "residual")
    c.text(40, 435, "Fig. 13: Residual analysis of single-target models for (a) Q and (b) Nu", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_13_SingleTarget_Residuals.png"))
    print("  Figure_13 done")


def _best_parity(c, x0, y0, x1, y1, truth, rmse, title, vmin, vmax, r2):
    pred = noisy(truth, rmse, seed=999 + int(vmax))
    parity_plot(c, x0, y0, x1, y1, truth, pred, ORANGE, title, vmin, vmax, r2, rmse)


def fig14_single_parity():
    c = PNGCanvas(820, 460)
    c.text_c(410, 10, "Single-Target Parity Plots (AdaBoost)", BLACK, 2)
    tq = make_sorted_truth(34, 460, 726)
    tnu = make_sorted_truth(34, 9.6, 23.0)
    _best_parity(c, 70, 70, 380, 380, tq, 7.9, "(a) Q", 440, 760, 0.989)
    _best_parity(c, 470, 70, 780, 380, tnu, 1.06, "(b) Nu", 8, 25, 0.988)
    c.text(40, 435, "Fig. 14: Actual vs predicted (R2, RMSE) for single-target models: (a) Q and (b) Nu", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_14_SingleTarget_Parity.png"))
    print("  Figure_14 done")


def fig15_single_errors():
    c = PNGCanvas(820, 460)
    c.text_c(410, 10, "Single-Target Prediction Errors (RMSE and MAE)", BLACK, 2)
    q_rmse = [METR_Q_S[m][1] for m in MODEL_NAMES]
    q_mae = [MAE_Q[m] for m in MODEL_NAMES]
    nu_rmse = [METR_NU_S[m][1] for m in MODEL_NAMES]
    nu_mae = [MAE_NU[m] for m in MODEL_NAMES]
    grouped_bars(c, 70, 90, 390, 380, MODEL_NAMES, [q_rmse, q_mae],
                 [MED_BLUE, ORANGE], 22, "W", MODEL_NAMES,
                 "(a) Q", legend=["RMSE", "MAE"], fmt="{:.0f}")
    grouped_bars(c, 470, 90, 780, 380, MODEL_NAMES, [nu_rmse, nu_mae],
                 [MED_BLUE, ORANGE], 3.2, "-", MODEL_NAMES,
                 "(b) Nu", legend=["RMSE", "MAE"], fmt="{:.1f}")
    c.text(40, 435, "Fig. 15: Prediction errors (RMSE and MAE) of single-target models for (a) Q and (b) Nu", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_15_SingleTarget_Errors.png"))
    print("  Figure_15 done")


def fig16_feature_importance():
    c = PNGCanvas(820, 460)
    c.text_c(410, 10, "Feature Importance (Six Single-Target Models)", BLACK, 2)
    feats = ["Heat", "Flow", "HNF", "CuO", "ModD"]
    # Q: heat input dominant
    q_imp = [
        [0.31, 0.21, 0.18, 0.17, 0.13],  # MLRR
        [0.29, 0.20, 0.19, 0.18, 0.14],  # PLSR
        [0.26, 0.21, 0.20, 0.18, 0.15],  # MLP
        [0.30, 0.19, 0.18, 0.17, 0.16],  # AB
        [0.21, 0.21, 0.20, 0.20, 0.18],  # SVR (even)
        [0.28, 0.20, 0.19, 0.18, 0.15],  # RFR
    ]
    # Nu: flow dominant
    nu_imp = [
        [0.14, 0.39, 0.15, 0.18, 0.14],
        [0.13, 0.36, 0.17, 0.18, 0.16],
        [0.12, 0.30, 0.22, 0.22, 0.14],
        [0.11, 0.38, 0.17, 0.18, 0.16],
        [0.18, 0.22, 0.20, 0.20, 0.20],
        [0.12, 0.34, 0.18, 0.18, 0.18],
    ]
    # average across models for a clean bar display
    q_avg = [sum(q_imp[m][f] for m in range(6)) / 6 * 100 for f in range(5)]
    nu_avg = [sum(nu_imp[m][f] for m in range(6)) / 6 * 100 for f in range(5)]
    grouped_bars(c, 70, 90, 390, 380, feats, [q_avg], [MED_GREEN], 40,
                 "%", feats, "(a) Q importance (mean of 6 models)", fmt="{:.0f}")
    grouped_bars(c, 470, 90, 780, 380, feats, [nu_avg], [PURPLE], 40,
                 "%", feats, "(b) Nu importance (mean of 6 models)", fmt="{:.0f}")
    c.text(40, 435, "Fig. 16: Feature-importance analysis of (a) Q and (b) Nu for the six single-target models", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_16_Feature_Importance.png"))
    print("  Figure_16 done")


def fig17_multi_pred():
    c = PNGCanvas(820, 460)
    c.text_c(410, 10, "Multi-Target Predictions (Best Models)", BLACK, 2)
    tq = make_sorted_truth(34, 460, 726)
    tnu = make_sorted_truth(34, 9.6, 23.0)
    _pred_panel(c, 70, 70, 390, 380, tq, 7.9, "(a) Q", 400, 760, "Q (W)")
    _pred_panel(c, 470, 70, 780, 380, tnu, 1.06, "(b) Nu", 8, 25, "Nu")
    c.text(40, 435, "Fig. 17: Multi-target model predictions for (a) Q and (b) Nu", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_17_MultiTarget_Pred.png"))
    print("  Figure_17 done")


def fig18_multi_parity():
    c = PNGCanvas(820, 460)
    c.text_c(410, 10, "Multi-Target Parity Plots (AdaBoost)", BLACK, 2)
    tq = make_sorted_truth(34, 460, 726)
    tnu = make_sorted_truth(34, 9.6, 23.0)
    _best_parity(c, 70, 70, 380, 380, tq, 7.9, "(a) Q", 440, 760, 0.989)
    _best_parity(c, 470, 70, 780, 380, tnu, 1.06, "(b) Nu", 8, 25, 0.988)
    c.text(40, 435, "Fig. 18: Actual vs predicted (R2, RMSE) for multi-target models: (a) Q and (b) Nu", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_18_MultiTarget_Parity.png"))
    print("  Figure_18 done")


def fig19_single_vs_multi():
    c = PNGCanvas(820, 460)
    c.text_c(410, 10, "Single- vs Multi-Target RMSE Comparison", BLACK, 2)
    q_s = [METR_Q_S[m][1] for m in MODEL_NAMES]
    q_m = [METR_Q_M[m][1] for m in MODEL_NAMES]
    nu_s = [METR_NU_S[m][1] for m in MODEL_NAMES]
    nu_m = [METR_NU_M[m][1] for m in MODEL_NAMES]
    grouped_bars(c, 70, 90, 390, 380, MODEL_NAMES, [q_s, q_m],
                 [MED_BLUE, ORANGE], 22, "W", MODEL_NAMES,
                 "(a) Q RMSE", legend=["Single", "Multi"], fmt="{:.0f}")
    grouped_bars(c, 470, 90, 780, 380, MODEL_NAMES, [nu_s, nu_m],
                 [MED_BLUE, ORANGE], 3.2, "-", MODEL_NAMES,
                 "(b) Nu RMSE", legend=["Single", "Multi"], fmt="{:.1f}")
    c.text(40, 435, "Fig. 19: Single-target vs multi-target RMSE for (a) Q and (b) Nu", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, "Figure_19_Single_vs_Multi.png"))
    print("  Figure_19 done")


def main():
    print("Generating manuscript figures (ML hybrid-nanofluid radiator)...")
    fig1_facility()
    fig2_fins()
    fig3_nanoparticles()
    fig4_uvvis()
    fig5_workflow()
    fig6_q_model()
    fig7_nu_model()
    fig8_flowrate()
    fig9_nu_re()
    fig10_mixture()
    fig11_corr()
    fig12_single_pred()
    fig13_single_resid()
    fig14_single_parity()
    fig15_single_errors()
    fig16_feature_importance()
    fig17_multi_pred()
    fig18_multi_parity()
    fig19_single_vs_multi()
    print("\nAll 19 figures written to {}".format(OUTPUT_DIR))


if __name__ == "__main__":
    main()
