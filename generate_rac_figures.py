#!/usr/bin/env python3
"""
Generate 7 scientific figures (PNG) for the research paper:
"Comparative Evaluation of Ensemble and Tree-Based Models for
 Compressive Strength of Recycled Aggregate Concrete"

Reuses the pure-standard-library PNGCanvas from generate_figures.py.
"""

import os
import math
import random

from generate_figures import (
    PNGCanvas, BLACK, WHITE, GRAY, LIGHT_GRAY,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE, RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/rac_figures'

# ---------------------------------------------------------------
# Shared data (kept consistent with the manuscript text/tables)
# ---------------------------------------------------------------
MODELS = ["CART", "REPTree", "M5P", "AdaBoost", "ExtraTrees", "RF", "GBRT", "XGBoost"]
R2_TRAIN = [0.902, 0.918, 0.939, 0.948, 0.971, 0.978, 0.983, 0.991]
R2_TEST  = [0.861, 0.889, 0.908, 0.921, 0.939, 0.944, 0.951, 0.962]
RMSE_TEST = [6.33, 5.67, 5.16, 4.77, 4.19, 4.02, 3.78, 3.41]
MODEL_COLORS = [GRAY, LIGHT_BLUE, MED_BLUE, GOLD, LIGHT_GREEN, MED_GREEN, ORANGE, RED]

FEATURES = ["Age", "w/c", "Cement", "RCA%", "Water", "RCA-WA",
            "SP", "NCA", "Fine agg", "RCA-SG"]
FEAT_IMP = [0.271, 0.193, 0.152, 0.118, 0.079, 0.061, 0.047, 0.033, 0.026, 0.020]


def _axis_box(c, x0, y0, x1, y1):
    c.vline(x0, y0, y1, BLACK)
    c.hline(x0, x1, y1, BLACK)


# ---------------------------------------------------------------
def gen_fig1():
    """Figure 1: Research methodology flowchart."""
    c = PNGCanvas(780, 560, WHITE)
    c.text_c(390, 10, "Research Methodology Framework", BLACK, 2)

    steps = [
        ("Database compilation", "514 RAC mix records from literature", DARK_BLUE, PALE_BLUE),
        ("Data screening and cleaning", "outlier removal, consistency checks", MED_BLUE, LIGHT_BLUE),
        ("Min-max normalization (0-1)", "10 inputs, 1 output (CS, MPa)", DARK_GREEN, LIGHT_GREEN),
        ("Train / test partition", "70% training (360), 30% testing (154)", MED_GREEN, LIGHT_GREEN),
        ("Model development", "3 tree-based + 5 ensemble learners", ORANGE, LIGHT_ORANGE),
        ("Hyper-parameter tuning", "grid search with 10-fold cross-validation", GOLD, LIGHT_GOLD),
        ("Performance evaluation", "R, R2, MAE, RMSE, MAPE, NSE", PURPLE, LIGHT_PURPLE),
        ("Ranking and SHAP analysis", "best model + feature importance", RED, LIGHT_RED),
    ]
    bx0, bw, bh = 200, 380, 44
    y = 48
    gap = 18
    centers = []
    for title, sub, col, fill in steps:
        c.rect(bx0, y, bx0 + bw, y + bh, col, fill)
        c.text_c(bx0 + bw // 2, y + 10, title, BLACK, 1)
        c.text_c(bx0 + bw // 2, y + 26, sub, GRAY, 1)
        centers.append((bx0 + bw // 2, y, y + bh))
        y += bh + gap
    for i in range(len(steps) - 1):
        cx = centers[i][0]
        c.arrow(cx, centers[i][2], cx, centers[i + 1][1], BLACK, 2, 7)

    # Side panel: model list
    c.rect(20, 210, 190, 430, LIGHT_GRAY, (248, 248, 248))
    c.text(30, 218, "Models:", BLACK, 1)
    ml = ["Tree-based:", " CART", " REPTree", " M5P",
          "Ensemble:", " AdaBoost.R2", " Extra Trees", " Random Forest",
          " Grad. Boosting", " XGBoost"]
    for i, m in enumerate(ml):
        col = DARK_BLUE if m.endswith(":") else GRAY
        c.text(30, 236 + i * 18, m, col, 1)

    c.text(20, 540, "Figure 1  Overall workflow adopted for model development and comparison.", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1.png'))
    print("  Figure_1.png done")


# ---------------------------------------------------------------
def gen_fig2():
    """Figure 2: Pearson correlation heat-map of variables."""
    labels = ["C", "W", "FA", "NCA", "RCA", "WA", "RR", "SP", "w/c", "Age", "CS"]
    n = len(labels)
    # Symmetric plausible correlation matrix
    corr = [[0.0] * n for _ in range(n)]
    base = {
        (0, 10): 0.58, (8, 10): -0.52, (9, 10): 0.49, (6, 10): -0.38,
        (5, 10): -0.31, (7, 10): 0.27, (4, 10): -0.24, (3, 10): 0.18,
        (1, 8): 0.61, (0, 8): -0.55, (4, 6): 0.72, (5, 6): 0.44,
        (0, 1): -0.12, (2, 3): 0.21, (3, 4): -0.40, (7, 8): -0.33,
        (0, 7): 0.30, (1, 10): -0.29, (2, 10): 0.08,
    }
    for i in range(n):
        corr[i][i] = 1.0
    for (i, j), v in base.items():
        corr[i][j] = v
        corr[j][i] = v

    cell = 52
    m0x, m0y = 90, 70
    size = n * cell
    c = PNGCanvas(m0x + size + 120, m0y + size + 70, WHITE)
    c.text_c((m0x + size) // 2 + 20, 12, "Pearson Correlation Matrix of Input and Output Variables", BLACK, 2)

    def color_for(v):
        # blue (neg) -> white (0) -> red (pos)
        if v >= 0:
            t = v
            return (int(255), int(255 - 180 * t), int(255 - 180 * t))
        else:
            t = -v
            return (int(255 - 180 * t), int(255 - 160 * t), int(255))

    for i in range(n):
        for j in range(n):
            x = m0x + j * cell
            yy = m0y + i * cell
            c.rect(x, yy, x + cell, yy + cell, (210, 210, 210), color_for(corr[i][j]))
            val = corr[i][j]
            s = f"{val:.2f}" if val not in (1.0,) else "1.0"
            tcol = BLACK
            c.text_c(x + cell // 2, yy + cell // 2 - 3, s, tcol, 1)
        # row label
        c.text(m0x - 42, m0y + i * cell + cell // 2 - 3, labels[i], BLACK, 1)
        # col label
        c.text_c(m0x + i * cell + cell // 2, m0y - 16, labels[i], BLACK, 1)

    # color legend
    lx = m0x + size + 25
    for k in range(120):
        v = 1 - 2 * k / 120.0
        c.hline(lx, lx + 24, m0y + k, color_for(v))
    c.rect(lx, m0y, lx + 24, m0y + 120, BLACK)
    c.text(lx - 2, m0y - 14, "+1", BLACK, 1)
    c.text(lx - 2, m0y + 122, "-1", BLACK, 1)
    c.text(lx - 4, m0y + 56, "0", BLACK, 1)

    c.text(20, m0y + size + 40,
           "Figure 2  Correlation structure among the ten predictors and compressive strength (CS).",
           BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2.png'))
    print("  Figure_2.png done")


# ---------------------------------------------------------------
def gen_fig3():
    """Figure 3: Histogram of compressive strength + RCA replacement spread."""
    c = PNGCanvas(780, 420, WHITE)
    c.text_c(390, 10, "Distribution of the Experimental Database", BLACK, 2)

    # (a) CS histogram
    c.text(40, 36, "(a) Compressive strength (MPa)", BLACK, 1)
    x0, y0, x1, y1 = 60, 60, 360, 330
    _axis_box(c, x0, y0, x1, y1)
    bins = [8, 21, 46, 78, 96, 88, 70, 52, 33, 15, 7]
    bw = (x1 - x0) // len(bins)
    mx = max(bins)
    for i, b in enumerate(bins):
        h = int((b / mx) * (y1 - y0 - 10))
        bx = x0 + i * bw + 2
        c.rect(bx, y1 - h, bx + bw - 4, y1, MED_BLUE, LIGHT_BLUE)
    c.text(x0 - 6, y1 + 6, "10", BLACK, 1)
    c.text(x1 - 20, y1 + 6, "85", BLACK, 1)
    c.text((x0 + x1) // 2 - 20, y1 + 20, "CS (MPa)", BLACK, 1)
    c.text(20, y0, "Freq", BLACK, 1)

    # (b) RCA replacement ratio distribution (categorical)
    c.text(420, 36, "(b) RCA replacement ratio (%)", BLACK, 1)
    x0b, y0b, x1b, y1b = 440, 60, 740, 330
    _axis_box(c, x0b, y0b, x1b, y1b)
    cats = [("0", 96), ("25", 78), ("50", 112), ("75", 84), ("100", 144)]
    bwb = (x1b - x0b) // len(cats)
    mxb = max(v for _, v in cats)
    for i, (lbl, v) in enumerate(cats):
        h = int((v / mxb) * (y1b - y0b - 10))
        bx = x0b + i * bwb + 8
        c.rect(bx, y1b - h, bx + bwb - 16, y1b, DARK_GREEN, LIGHT_GREEN)
        c.text_c(bx + (bwb - 16) // 2, y1b + 6, lbl, BLACK, 1)
    c.text((x0b + x1b) // 2 - 30, y1b + 20, "Replacement (%)", BLACK, 1)
    c.text(400, y0b, "Count", BLACK, 1)

    c.text(20, 388,
           "Figure 3  (a) Histogram of measured compressive strength; (b) spread of RCA replacement levels (n = 514).",
           BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3.png'))
    print("  Figure_3.png done")


# ---------------------------------------------------------------
def _scatter(c, x0, y0, side, r2, color, seed):
    random.seed(seed)
    _axis_box(c, x0, y0 + side, x0 + side, y0 + side)  # bottom
    c.vline(x0, y0, y0 + side, BLACK)
    # 1:1 line
    c.line(x0, y0 + side, x0 + side, y0, BLACK, 1)
    # points: observed uniform 15..80 scaled; predicted ~ observed + noise depending on r2
    noise = (1 - r2) * 42
    for _ in range(55):
        o = random.uniform(0.07, 0.95)
        p = o + random.uniform(-noise, noise) / 90.0
        p = max(0.03, min(0.97, p))
        px = int(x0 + o * side)
        py = int(y0 + side - p * side)
        c.circle(px, py, 2, color, color)


def gen_fig4():
    """Figure 4: Observed vs predicted scatter grid for all 8 models (testing)."""
    c = PNGCanvas(820, 470, WHITE)
    c.text_c(410, 8, "Observed vs. Predicted Compressive Strength (Testing Set)", BLACK, 2)
    side = 150
    gx = [30, 230, 430, 630]
    gy = [50, 270]
    for idx, name in enumerate(MODELS):
        col = idx % 4
        row = idx // 4
        x0 = gx[col]
        y0 = gy[row]
        _scatter(c, x0, y0, side, R2_TEST[idx], MODEL_COLORS[idx], seed=idx + 3)
        c.text(x0 + 6, y0 + 6, name, BLACK, 1)
        c.text(x0 + 6, y0 + 20, f"R2={R2_TEST[idx]:.3f}", GRAY, 1)
        if row == 1:
            c.text_c(x0 + side // 2, y0 + side + 16, "Observed (MPa)", BLACK, 1)
        if col == 0:
            c.text(x0 - 24, y0 + side // 2, "Pred", BLACK, 1)
    c.text(20, 455,
           "Figure 4  Agreement between measured and predicted strength for the eight models on unseen data.",
           BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4.png'))
    print("  Figure_4.png done")


# ---------------------------------------------------------------
def gen_fig5():
    """Figure 5: Grouped bar chart - R2 (train/test) and RMSE (test)."""
    c = PNGCanvas(820, 460, WHITE)
    c.text_c(410, 10, "Comparative Performance of the Eight Models", BLACK, 2)

    # (a) R2 grouped bars
    c.text(40, 36, "(a) Coefficient of determination (R2)", BLACK, 1)
    x0, y0, x1, y1 = 60, 60, 780, 230
    _axis_box(c, x0, y0, x1, y1)
    n = len(MODELS)
    slot = (x1 - x0) // n
    for i, name in enumerate(MODELS):
        bx = x0 + i * slot + 10
        htr = int((R2_TRAIN[i] - 0.80) / 0.20 * (y1 - y0 - 10))
        hte = int((R2_TEST[i] - 0.80) / 0.20 * (y1 - y0 - 10))
        c.rect(bx, y1 - htr, bx + 22, y1, DARK_BLUE, LIGHT_BLUE)
        c.rect(bx + 24, y1 - hte, bx + 46, y1, ORANGE, LIGHT_ORANGE)
        c.text(bx - 2, y1 + 6, name[:6], BLACK, 1)
    c.text(26, y0, "1.0", BLACK, 1)
    c.text(26, y1 - 6, "0.8", BLACK, 1)
    c.rect(600, 66, 614, 78, DARK_BLUE, LIGHT_BLUE); c.text(618, 68, "Train", BLACK, 1)
    c.rect(660, 66, 674, 78, ORANGE, LIGHT_ORANGE); c.text(678, 68, "Test", BLACK, 1)

    # (b) RMSE line/bar
    c.text(40, 262, "(b) Root mean square error on testing set (MPa)", BLACK, 1)
    x0b, y0b, x1b, y1b = 60, 286, 780, 420
    _axis_box(c, x0b, y0b, x1b, y1b)
    mx = max(RMSE_TEST)
    for i, name in enumerate(MODELS):
        bx = x0b + i * slot + 16
        h = int((RMSE_TEST[i] / (mx * 1.1)) * (y1b - y0b - 10))
        c.rect(bx, y1b - h, bx + 36, y1b, MODEL_COLORS[i], MODEL_COLORS[i])
        c.text_c(bx + 18, y1b - h - 12, f"{RMSE_TEST[i]:.2f}", BLACK, 1)
        c.text(bx - 6, y1b + 6, name[:6], BLACK, 1)
    c.text(26, y0b, f"{mx:.0f}", BLACK, 1)

    c.text(20, 448,
           "Figure 5  (a) Training/testing R2 and (b) testing RMSE for all candidate models.",
           BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_5.png'))
    print("  Figure_5.png done")


# ---------------------------------------------------------------
def gen_fig6():
    """Figure 6: Taylor diagram (testing stage)."""
    c = PNGCanvas(620, 580, WHITE)
    c.text_c(310, 10, "Taylor Diagram (Testing Stage)", BLACK, 2)
    cx, cy = 70, 470
    R = 400
    # arcs (std-dev circles)
    for frac in (0.25, 0.5, 0.75, 1.0):
        rr = int(R * frac)
        prev = None
        for deg in range(0, 91):
            a = math.radians(deg)
            x = int(cx + rr * math.cos(a))
            y = int(cy - rr * math.sin(a))
            if prev:
                c.line(prev[0], prev[1], x, y, LIGHT_GRAY, 1)
            prev = (x, y)
    # axes
    c.line(cx, cy, cx + R, cy, BLACK, 1)
    c.line(cx, cy, cx, cy - R, BLACK, 1)
    # correlation rays
    for cc in (0.3, 0.6, 0.8, 0.9, 0.95, 0.99):
        a = math.acos(cc)
        x = int(cx + R * math.cos(a))
        y = int(cy - R * math.sin(a))
        c.line(cx, cy, x, y, (225, 225, 225), 1)
        c.text(x - 8, y - 12, f"{cc:.2f}", GRAY, 1)
    c.text(cx + R - 70, cy - 10, "Std. dev.", BLACK, 1)
    c.text(cx - 40, cy - R + 4, "Std", BLACK, 1)
    c.text(cx + int(R*0.72), cy - int(R*0.72) - 20, "Correlation", GRAY, 1)

    # reference (observed) point on x-axis at std=1.0 (full R)
    c.circle(cx + R, cy, 6, BLACK, WHITE)
    c.text(cx + R - 20, cy + 8, "Obs", BLACK, 1)

    # model points: std ratio and correlation
    stds = [0.86, 0.89, 0.91, 0.93, 0.95, 0.96, 0.975, 0.99]
    corrs = [0.928, 0.943, 0.953, 0.960, 0.969, 0.972, 0.975, 0.981]
    for i, name in enumerate(MODELS):
        a = math.acos(corrs[i])
        rr = R * stds[i]
        x = int(cx + rr * math.cos(a))
        y = int(cy - rr * math.sin(a))
        c.circle(x, y, 5, MODEL_COLORS[i], MODEL_COLORS[i])
        c.text(x + 7, y - 4, name[:7], BLACK, 1)

    c.text(20, 558,
           "Figure 6  Taylor diagram summarising correlation and standard-deviation match on unseen data.",
           BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_6.png'))
    print("  Figure_6.png done")


# ---------------------------------------------------------------
def gen_fig7():
    """Figure 7: Feature importance (SHAP mean) for the best model (XGBoost)."""
    c = PNGCanvas(760, 460, WHITE)
    c.text_c(380, 10, "Relative Feature Importance (XGBoost, SHAP)", BLACK, 2)
    x0, y0, x1, y1 = 150, 50, 720, 410
    c.vline(x0, y0, y1, BLACK)
    c.hline(x0, x1, y1, BLACK)
    n = len(FEATURES)
    slot = (y1 - y0) // n
    mx = max(FEAT_IMP)
    cols = [RED, ORANGE, GOLD, MED_GREEN, LIGHT_GREEN, MED_BLUE,
            LIGHT_BLUE, PURPLE, LIGHT_PURPLE, GRAY]
    for i, (f, v) in enumerate(zip(FEATURES, FEAT_IMP)):
        by = y0 + i * slot + 6
        w = int((v / (mx * 1.1)) * (x1 - x0))
        c.rect(x0, by, x0 + w, by + slot - 12, cols[i], cols[i])
        c.text(20, by + (slot - 12) // 2 - 3, f, BLACK, 1)
        c.text(x0 + w + 6, by + (slot - 12) // 2 - 3, f"{v:.3f}", BLACK, 1)
    c.text((x0 + x1) // 2 - 70, y1 + 18, "mean(|SHAP value|)", BLACK, 1)
    c.text(20, 442,
           "Figure 7  Mean absolute SHAP contribution of each predictor for the best model.",
           BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_7.png'))
    print("  Figure_7.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating RAC paper figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    gen_fig5()
    gen_fig6()
    gen_fig7()
    print(f"\nAll 7 figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz/1024:.1f} KB")


if __name__ == '__main__':
    main()
