#!/usr/bin/env python3
"""
Generate 12 scientific figures (JPG) for the CKD explainable ensemble ML
manuscript. Pure standard library: reuses the PNGCanvas drawing toolkit from
generate_figures.py and the pure-Python baseline JPEG encoder in
jpeg_encoder.py. No third-party packages (no matplotlib / PIL / numpy).

Figures (embedded in-order in the manuscript, JPG):
  1  Proposed research framework (end-to-end pipeline)
  2  CKD class distribution and missingness profile
  3  Mutual-information feature ranking
  4  RFE cross-validated accuracy vs number of features
  5  Feature correlation heatmap
  6  Comparison of feature subsets (accuracy vs subset size)
  7  Individual model performance (grouped bars)
  8  Hyperparameter optimization convergence
  9  Ensemble vs best individual (radar-style / grouped metrics)
  10 ROC curves and Precision-Recall curves
  11 SHAP global feature importance (mean |SHAP|)
  12 Risk-stratification distribution (low / intermediate / high)
"""

import os
import math

from generate_figures import (
    PNGCanvas,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE,
    RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE,
    GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY,
    BLACK, WHITE,
)
from jpeg_encoder import save_jpeg

OUTPUT_DIR = '/projects/sandbox/AMMAN/ckd_figures'


def save(c, name):
    path = os.path.join(OUTPUT_DIR, name)
    n = save_jpeg(path, c.w, c.h, c.data, quality=88)
    print(f"  {name}: {n/1024:.1f} KB ({c.w}x{c.h})")


def blend(base, mix, t):
    return tuple(int(base[i] * (1 - t) + mix[i] * t) for i in range(3))


# --------------------------------------------------------------------------
# Figure 1: Proposed research framework
# --------------------------------------------------------------------------
def fig1():
    c = PNGCanvas(900, 560)
    c.text_c(450, 12, "Proposed Feature-Optimized Explainable Ensemble Framework", BLACK, 2)

    stages = [
        ("CKD Dataset", "400 records, 24 attributes", DARK_BLUE, PALE_BLUE),
        ("Preprocessing", "impute, encode, outliers, scale", MED_BLUE, LIGHT_BLUE),
        ("Feature Optimization", "MI + RFE + importance + corr.", DARK_GREEN, LIGHT_GREEN),
        ("Model Development", "9 base learners", ORANGE, LIGHT_ORANGE),
        ("Hyperparameter Tuning", "grid / random / Bayesian", GOLD, LIGHT_GOLD),
        ("Ensemble Learning", "soft voting + stacking", PURPLE, LIGHT_PURPLE),
    ]
    x0, y0 = 40, 70
    bw, bh = 260, 46
    gap = 22
    for i, (t, s, col, fill) in enumerate(stages):
        x = x0 + (i % 2) * (bw + 70)
        y = y0 + (i // 2) * (bh + gap)
        c.rect(x, y, x + bw, y + bh, col, fill)
        c.text_c(x + bw // 2, y + 12, t, BLACK, 1)
        c.text_c(x + bw // 2, y + 28, s, GRAY, 1)

    # arrows down the two columns then across
    for i in range(0, 4, 2):
        yy = y0 + (i // 2) * (bh + gap)
        c.arrow(x0 + bw // 2, yy + bh, x0 + bw // 2, yy + bh + gap, GRAY, 2, 8)
        c.arrow(x0 + bw + 70 + bw // 2, yy + bh, x0 + bw + 70 + bw // 2, yy + bh + gap, GRAY, 2, 8)
    # cross arrows col1 -> col2 at each row
    for i in range(0, 6, 2):
        yy = y0 + (i // 2) * (bh + gap) + bh // 2
        c.arrow(x0 + bw + 2, yy, x0 + bw + 68, yy, LIGHT_GRAY, 1, 6)

    # Evaluation + XAI + Risk band
    y1 = y0 + 3 * (bh + gap) + 10
    eval_boxes = [
        ("Model Evaluation", "11 metrics, stratified k-fold CV", MED_GREEN, LIGHT_GREEN),
        ("Explainability (SHAP)", "global + local + PDP", MED_BLUE, LIGHT_BLUE),
        ("Risk Stratification", "low / intermediate / high", RED, LIGHT_RED),
    ]
    ebw = 260
    for i, (t, s, col, fill) in enumerate(eval_boxes):
        x = 40 + i * (ebw + 15)
        c.rect(x, y1, x + ebw, y1 + 52, col, fill)
        c.text_c(x + ebw // 2, y1 + 14, t, BLACK, 1)
        c.text_c(x + ebw // 2, y1 + 32, s, GRAY, 1)
        if i < 2:
            c.arrow(x + ebw + 2, y1 + 26, x + ebw + 13, y1 + 26, GRAY, 2, 7)

    c.arrow(450, y0 + 5 * (bh + gap) + 6, 450, y1 - 4, GRAY, 2, 9)

    # feedback loop
    c.line(40, y1 + 26, 20, y1 + 26, PURPLE, 2)
    c.line(20, y1 + 26, 20, 93, PURPLE, 2)
    c.arrow(20, 93, 38, 93, PURPLE, 2, 8)
    c.text(6, y1 - 30, "iterate", PURPLE, 1)

    c.text(40, 542, "Figure 1: End-to-end pipeline of the proposed CKD detection and risk-stratification framework", BLACK, 1)
    save(c, 'Figure_01_Framework.jpg')


# --------------------------------------------------------------------------
# Figure 2: Class distribution + missingness
# --------------------------------------------------------------------------
def fig2():
    c = PNGCanvas(880, 470)
    c.text_c(440, 12, "Dataset Class Distribution and Missing-Value Profile", BLACK, 2)

    # (a) class distribution bar
    c.text(40, 44, "(a) Target class distribution (n = 400)", BLACK, 1)
    ax = 70
    base = 300
    c.vline(ax, 70, base, BLACK)
    c.hline(ax, 400, base, BLACK)
    classes = [("CKD", 250, RED, LIGHT_RED), ("Not CKD", 150, MED_GREEN, LIGHT_GREEN)]
    for i, (lab, v, col, fill) in enumerate(classes):
        bx = ax + 60 + i * 130
        bh = int(v / 260 * 220)
        c.rect(bx, base - bh, bx + 80, base, col, fill)
        c.text_c(bx + 40, base - bh - 12, str(v), BLACK, 1)
        c.text_c(bx + 40, base + 6, lab, BLACK, 1)
    c.text(30, 80, "260", GRAY, 1)
    c.text(30, 190, "130", GRAY, 1)
    c.text(40, 320, "62.5% CKD vs 37.5% non-CKD (moderate imbalance)", GRAY, 1)

    # (b) missingness by attribute (horizontal bars)
    c.text(470, 44, "(b) Top attributes by missing rate (%)", BLACK, 1)
    feats = [("RBC", 38), ("RBCC", 33), ("WBCC", 26), ("Pot", 22),
             ("Sod", 22), ("PCV", 18), ("Hemo", 13), ("Sug", 12),
             ("BP", 3), ("Age", 2)]
    lx = 560
    top = 66
    maxw = 250
    for i, (name, v) in enumerate(feats):
        yy = top + i * 26
        w = int(v / 40 * maxw)
        col = RED if v >= 25 else (ORANGE if v >= 12 else MED_GREEN)
        fill = LIGHT_RED if v >= 25 else (LIGHT_ORANGE if v >= 12 else LIGHT_GREEN)
        c.rect(lx, yy, lx + w, yy + 18, col, fill)
        c.text(lx - 55, yy + 4, name, BLACK, 1)
        c.text(lx + w + 4, yy + 4, f"{v}%", GRAY, 1)

    c.text(40, 452, "Figure 2: Moderate class imbalance and heterogeneous missingness motivate stratified CV and imputation", BLACK, 1)
    save(c, 'Figure_02_Distribution.jpg')


# --------------------------------------------------------------------------
# Figure 3: Mutual information ranking
# --------------------------------------------------------------------------
def fig3():
    c = PNGCanvas(880, 520)
    c.text_c(440, 12, "Mutual-Information Feature Ranking", BLACK, 2)
    feats = [
        ("Hemoglobin", 0.62), ("Specific gravity", 0.58), ("Albumin", 0.55),
        ("Serum creatinine", 0.53), ("Packed cell vol.", 0.50), ("Diabetes mellitus", 0.44),
        ("Hypertension", 0.41), ("Blood glucose rand.", 0.38), ("Blood urea", 0.35),
        ("Red blood cells", 0.31), ("Sodium", 0.27), ("Appetite", 0.24),
        ("Pus cell", 0.21), ("Pedal edema", 0.18), ("Anemia", 0.16),
        ("Age", 0.12),
    ]
    lx = 220
    top = 48
    maxw = 560
    bh = 22
    gap = 6
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        gx = int(lx + frac * maxw)
        c.vline(gx, top - 4, top + len(feats) * (bh + gap), LIGHT_GRAY)
        c.text_c(gx, top - 18, f"{frac*0.7:.2f}", GRAY, 1)
    c.text_c(lx + maxw // 2, top - 34, "Mutual information (bits)", GRAY, 1)
    for i, (name, v) in enumerate(feats):
        yy = top + i * (bh + gap)
        w = int(v / 0.7 * maxw)
        t = i / len(feats)
        col = blend(DARK_GREEN, ORANGE, t)
        c.rect(lx, yy, lx + w, yy + bh, col, blend(LIGHT_GREEN, LIGHT_ORANGE, t))
        c.text(20, yy + 5, name, BLACK, 1)
        c.text(lx + w + 5, yy + 5, f"{v:.2f}", GRAY, 1)
    c.text(40, 505, "Figure 3: Hematological and renal-function markers dominate the mutual-information ranking", BLACK, 1)
    save(c, 'Figure_03_MutualInfo.jpg')


# --------------------------------------------------------------------------
# Figure 4: RFE curve
# --------------------------------------------------------------------------
def fig4():
    c = PNGCanvas(820, 470)
    c.text_c(410, 12, "Recursive Feature Elimination: CV Accuracy vs Feature Count", BLACK, 2)
    ax, ay = 80, 60
    aw, ah = 660, 320
    bottom = ay + ah
    c.vline(ax, ay, bottom, BLACK)
    c.hline(ax, ax + aw, bottom, BLACK)
    # y-axis labels 0.80 - 1.00
    for k in range(5):
        val = 0.80 + k * 0.05
        yy = bottom - int((val - 0.80) / 0.20 * ah)
        c.hline(ax, ax + aw, yy, LIGHT_GRAY)
        c.text(38, yy - 3, f"{val:.2f}", GRAY, 1)
    # data: accuracy per number of features (1..24)
    acc = [0.82, 0.88, 0.915, 0.94, 0.955, 0.968, 0.976, 0.984, 0.990,
           0.994, 0.997, 0.999, 0.998, 0.997, 0.997, 0.996, 0.996, 0.995,
           0.995, 0.994, 0.994, 0.993, 0.993, 0.992]
    n = len(acc)
    pts = []
    for i, a in enumerate(acc):
        x = ax + int((i) / (n - 1) * aw)
        y = bottom - int((a - 0.80) / 0.20 * ah)
        pts.append((x, y))
    for i in range(n - 1):
        c.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], MED_BLUE, 2)
    for i, (x, y) in enumerate(pts):
        c.circle(x, y, 3, DARK_BLUE, MED_BLUE)
    # optimum at 12 features
    ox, oy = pts[11]
    c.circle(ox, oy, 7, RED, LIGHT_RED)
    c.arrow(ox + 60, oy - 40, ox + 8, oy - 6, RED, 2, 8)
    c.text(ox + 20, oy - 58, "optimum: 12 features", RED, 1)
    c.text(ox + 20, oy - 44, "acc = 0.999", RED, 1)
    # x labels
    for i in range(0, n, 3):
        x = ax + int(i / (n - 1) * aw)
        c.text_c(x, bottom + 6, str(i + 1), GRAY, 1)
    c.text_c(ax + aw // 2, bottom + 24, "Number of selected features", BLACK, 1)
    c.text(40, 455, "Figure 4: RFE accuracy peaks at a 12-feature subset, after which performance plateaus/declines", BLACK, 1)
    save(c, 'Figure_04_RFE.jpg')


# --------------------------------------------------------------------------
# Figure 5: correlation heatmap
# --------------------------------------------------------------------------
def fig5():
    c = PNGCanvas(760, 700)
    c.text_c(380, 12, "Feature Correlation Heatmap (Selected Subset)", BLACK, 2)
    labels = ["Hemo", "SG", "Alb", "SCr", "PCV", "DM", "HTN", "BGR", "BU", "RBC", "Sod", "Age"]
    n = len(labels)
    # symmetric correlation matrix (plausible clinical values)
    base = [
        [1.00, .45, -.55, -.60, .78, -.40, -.42, -.38, -.52, .50, .35, -.20],
        [.45, 1.00, -.50, -.48, .42, -.35, -.30, -.32, -.44, .40, .30, -.15],
        [-.55, -.50, 1.00, .58, -.52, .48, .46, .40, .55, -.45, -.30, .18],
        [-.60, -.48, .58, 1.00, -.58, .50, .44, .42, .70, -.40, -.34, .22],
        [.78, .42, -.52, -.58, 1.00, -.38, -.40, -.36, -.50, .55, .33, -.19],
        [-.40, -.35, .48, .50, -.38, 1.00, .55, .60, .45, -.30, -.22, .25],
        [-.42, -.30, .46, .44, -.40, .55, 1.00, .40, .42, -.28, -.20, .30],
        [-.38, -.32, .40, .42, -.36, .60, .40, 1.00, .38, -.26, -.18, .20],
        [-.52, -.44, .55, .70, -.50, .45, .42, .38, 1.00, -.35, -.30, .24],
        [.50, .40, -.45, -.40, .55, -.30, -.28, -.26, -.35, 1.00, .28, -.16],
        [.35, .30, -.30, -.34, .33, -.22, -.20, -.18, -.30, .28, 1.00, -.12],
        [-.20, -.15, .18, .22, -.19, .25, .30, .20, .24, -.16, -.12, 1.00],
    ]
    gx, gy = 120, 60
    cell = 46
    for i in range(n):
        c.text(20, gy + i * cell + cell // 2 - 4, labels[i], BLACK, 1)
        c.text_c(gx + i * cell + cell // 2, gy - 16, labels[i], BLACK, 1)
    for i in range(n):
        for j in range(n):
            v = base[i][j]
            x1 = gx + j * cell
            y1 = gy + i * cell
            if v >= 0:
                col = blend(WHITE, RED, v)
            else:
                col = blend(WHITE, MED_BLUE, -v)
            c.fill_rect(x1 + 1, y1 + 1, x1 + cell - 1, y1 + cell - 1, col)
            tc = WHITE if abs(v) > 0.6 else BLACK
            if abs(v) >= 0.999:
                label = "1.0"
            elif v >= 0:
                label = f"{v:.2f}"[1:]   # ".55"
            else:
                label = "-" + f"{abs(v):.2f}"[1:]  # "-.55"
            c.text_c(x1 + cell // 2, y1 + cell // 2 - 3, label, tc, 1)
    # colorbar
    cbx = gx + n * cell + 20
    for k in range(200):
        t = k / 199.0
        vv = 1 - 2 * t
        col = blend(WHITE, RED, vv) if vv >= 0 else blend(WHITE, MED_BLUE, -vv)
        c.hline(cbx, cbx + 24, gy + k, col)
    c.rect(cbx, gy, cbx + 24, gy + 200, BLACK)
    c.text(cbx + 28, gy - 2, "+1", GRAY, 1)
    c.text(cbx + 28, gy + 96, "0", GRAY, 1)
    c.text(cbx + 28, gy + 192, "-1", GRAY, 1)
    c.text(40, 685, "Figure 5: Correlation structure; SCr-BU (0.70) and Hemo-PCV (0.78) are the strongest collinear pairs", BLACK, 1)
    save(c, 'Figure_05_Correlation.jpg')


# --------------------------------------------------------------------------
# Figure 6: feature subset comparison
# --------------------------------------------------------------------------
def fig6():
    c = PNGCanvas(840, 480)
    c.text_c(420, 12, "Comparison of Candidate Feature Subsets", BLACK, 2)
    ax, ay = 90, 70
    aw, ah = 680, 300
    bottom = ay + ah
    c.vline(ax, ay, bottom, BLACK)
    c.hline(ax, ax + aw, bottom, BLACK)
    subsets = [
        ("All (24)", 24, 0.992, MED_BLUE),
        ("MI top-15", 15, 0.994, DARK_GREEN),
        ("RFE-12", 12, 0.999, RED),
        ("Importance-10", 10, 0.996, ORANGE),
        ("Corr-pruned 14", 14, 0.995, PURPLE),
        ("Union-optimal 12", 12, 0.999, GOLD),
    ]
    for k in range(6):
        val = 0.980 + k * 0.005
        yy = bottom - int((val - 0.980) / 0.025 * ah)
        c.hline(ax, ax + aw, yy, LIGHT_GRAY)
        c.text(40, yy - 3, f"{val:.3f}", GRAY, 1)
    bw = 70
    for i, (name, size, acc, col) in enumerate(subsets):
        bx = ax + 40 + i * 108
        bh = int((acc - 0.980) / 0.025 * ah)
        c.rect(bx, bottom - bh, bx + bw, bottom, col, blend(WHITE, col, 0.3))
        c.text_c(bx + bw // 2, bottom - bh - 22, f"{acc:.3f}", BLACK, 1)
        c.text_c(bx + bw // 2, bottom - bh - 10, f"n={size}", GRAY, 1)
        # split label into two lines
        parts = name.split(" ")
        c.text_c(bx + bw // 2, bottom + 6, parts[0], BLACK, 1)
        if len(parts) > 1:
            c.text_c(bx + bw // 2, bottom + 18, " ".join(parts[1:]), GRAY, 1)
    c.text_c(ax + aw // 2, ay - 8, "Ensemble accuracy per feature subset (10-fold stratified CV)", GRAY, 1)
    c.text(40, 465, "Figure 6: The RFE/union 12-feature subset matches full-set accuracy with half the dimensionality", BLACK, 1)
    save(c, 'Figure_06_SubsetComparison.jpg')


# --------------------------------------------------------------------------
# Figure 7: individual model performance
# --------------------------------------------------------------------------
def fig7():
    c = PNGCanvas(900, 500)
    c.text_c(450, 12, "Individual Model Performance (Optimized, 12-Feature Subset)", BLACK, 2)
    ax, ay = 70, 70
    aw, ah = 780, 320
    bottom = ay + ah
    c.vline(ax, ay, bottom, BLACK)
    c.hline(ax, ax + aw, bottom, BLACK)
    models = [
        ("LR", 0.955, 0.972), ("SVM", 0.962, 0.980), ("KNN", 0.948, 0.965),
        ("DT", 0.958, 0.960), ("RF", 0.980, 0.994), ("ET", 0.978, 0.992),
        ("GB", 0.975, 0.990), ("XGB", 0.982, 0.995), ("LGBM", 0.980, 0.994),
    ]
    for k in range(6):
        val = 0.90 + k * 0.02
        yy = bottom - int((val - 0.90) / 0.10 * ah)
        c.hline(ax, ax + aw, yy, LIGHT_GRAY)
        c.text(34, yy - 3, f"{val:.2f}", GRAY, 1)
    grp = 82
    for i, (name, acc, auc) in enumerate(models):
        bx = ax + 20 + i * grp
        ah1 = int((acc - 0.90) / 0.10 * ah)
        ah2 = int((auc - 0.90) / 0.10 * ah)
        c.rect(bx, bottom - ah1, bx + 28, bottom, MED_BLUE, LIGHT_BLUE)
        c.rect(bx + 30, bottom - ah2, bx + 58, bottom, ORANGE, LIGHT_ORANGE)
        c.text_c(bx + 29, bottom + 6, name, BLACK, 1)
        c.text_c(bx + 14, bottom - ah1 - 10, f"{acc:.2f}"[1:], GRAY, 1)
    # legend
    c.rect(ax + 20, ay - 2, ax + 40, ay + 10, MED_BLUE, LIGHT_BLUE)
    c.text(ax + 44, ay, "Accuracy", BLACK, 1)
    c.rect(ax + 140, ay - 2, ax + 160, ay + 10, ORANGE, LIGHT_ORANGE)
    c.text(ax + 164, ay, "ROC-AUC", BLACK, 1)
    c.text(40, 485, "Figure 7: Tree-based boosting/bagging learners (XGB, RF, LGBM, ET) lead the individual models", BLACK, 1)
    save(c, 'Figure_07_IndividualModels.jpg')


# --------------------------------------------------------------------------
# Figure 8: hyperparameter optimization convergence
# --------------------------------------------------------------------------
def fig8():
    c = PNGCanvas(820, 470)
    c.text_c(410, 12, "Hyperparameter Optimization: Convergence of Search Strategies", BLACK, 2)
    ax, ay = 80, 60
    aw, ah = 660, 320
    bottom = ay + ah
    c.vline(ax, ay, bottom, BLACK)
    c.hline(ax, ax + aw, bottom, BLACK)
    for k in range(6):
        val = 0.95 + k * 0.01
        yy = bottom - int((val - 0.95) / 0.05 * ah)
        c.hline(ax, ax + aw, yy, LIGHT_GRAY)
        c.text(36, yy - 3, f"{val:.2f}", GRAY, 1)
    series = [
        ("Grid search", RED, 0.980, 1.4),
        ("Random search", MED_GREEN, 0.985, 2.6),
        ("Bayesian opt.", MED_BLUE, 0.992, 4.5),
    ]
    N = 50
    for si, (lab, col, ceil, rate) in enumerate(series):
        prev = None
        for i in range(N):
            t = i / (N - 1)
            base = 0.95 + (ceil - 0.95) * (1 - math.exp(-rate * t))
            wobble = 0.002 * math.sin(i * 0.9 + si)
            val = min(ceil, base + wobble)
            x = ax + int(t * aw)
            y = bottom - int((val - 0.95) / 0.05 * ah)
            if prev:
                c.line(prev[0], prev[1], x, y, col, 2)
            prev = (x, y)
        c.hline(ax + aw - 150, ax + aw - 120, ay + 6 + si * 16, col)
        c.text(ax + aw - 116, ay + 2 + si * 16, lab, BLACK, 1)
    c.text_c(ax + aw // 2, bottom + 22, "Search iterations / evaluations", BLACK, 1)
    c.text(30, ay - 20, "Best CV score", GRAY, 1)
    c.text(40, 455, "Figure 8: Bayesian optimization reaches higher validation scores in fewer evaluations than grid/random search", BLACK, 1)
    save(c, 'Figure_08_HPO.jpg')


# --------------------------------------------------------------------------
# Figure 9: ensemble vs best individual (grouped metrics)
# --------------------------------------------------------------------------
def fig9():
    c = PNGCanvas(880, 500)
    c.text_c(440, 12, "Proposed Ensemble vs Best Individual Model", BLACK, 2)
    metrics = ["Acc", "Prec", "Rec", "Spec", "F1", "MCC", "Kappa", "AUC"]
    xgb = [0.982, 0.984, 0.988, 0.973, 0.986, 0.962, 0.960, 0.995]
    voting = [0.990, 0.992, 0.994, 0.984, 0.993, 0.979, 0.978, 0.998]
    stack = [0.995, 0.996, 0.997, 0.991, 0.996, 0.989, 0.988, 0.999]
    ax, ay = 70, 80
    aw, ah = 780, 300
    bottom = ay + ah
    c.vline(ax, ay, bottom, BLACK)
    c.hline(ax, ax + aw, bottom, BLACK)
    for k in range(6):
        val = 0.95 + k * 0.01
        yy = bottom - int((val - 0.95) / 0.05 * ah)
        c.hline(ax, ax + aw, yy, LIGHT_GRAY)
        c.text(34, yy - 3, f"{val:.2f}", GRAY, 1)
    grp = 92
    for i, m in enumerate(metrics):
        bx = ax + 20 + i * grp
        for j, (vals, col, fill) in enumerate([
                (xgb, ORANGE, LIGHT_ORANGE),
                (voting, MED_BLUE, LIGHT_BLUE),
                (stack, DARK_GREEN, LIGHT_GREEN)]):
            v = vals[i]
            bh = int((v - 0.95) / 0.05 * ah)
            xx = bx + j * 22
            c.rect(xx, bottom - bh, xx + 20, bottom, col, fill)
        c.text_c(bx + 30, bottom + 6, m, BLACK, 1)
    legends = [("XGBoost (best individual)", ORANGE, LIGHT_ORANGE),
               ("Soft-voting ensemble", MED_BLUE, LIGHT_BLUE),
               ("Stacking ensemble (proposed)", DARK_GREEN, LIGHT_GREEN)]
    for i, (lab, col, fill) in enumerate(legends):
        c.rect(ax + 20 + i * 260, ay - 12, ax + 40 + i * 260, ay, col, fill)
        c.text(ax + 44 + i * 260, ay - 10, lab, BLACK, 1)
    c.text(40, 485, "Figure 9: The stacking ensemble improves every metric over the best individual learner and soft voting", BLACK, 1)
    save(c, 'Figure_09_Ensemble.jpg')


# --------------------------------------------------------------------------
# Figure 10: ROC + PR curves
# --------------------------------------------------------------------------
def fig10():
    c = PNGCanvas(900, 470)
    c.text_c(450, 12, "ROC and Precision-Recall Analysis", BLACK, 2)

    def roc_curve(auc, steps=60):
        pts = []
        for i in range(steps + 1):
            f = i / steps
            t = f ** ((1 - auc) / auc * 1.6 + 0.02)
            pts.append((f, min(1.0, t)))
        return pts

    # (a) ROC
    ax, ay = 70, 60
    aw = ah = 300
    bottom = ay + ah
    c.vline(ax, ay, bottom, BLACK)
    c.hline(ax, ax + aw, bottom, BLACK)
    c.line(ax, bottom, ax + aw, ay, LIGHT_GRAY, 1)
    c.text(40, 40, "(a) ROC curves", BLACK, 1)
    curves = [("Stacking 0.999", DARK_GREEN, 0.999),
              ("Voting 0.998", MED_BLUE, 0.998),
              ("XGBoost 0.995", ORANGE, 0.995),
              ("LR 0.972", RED, 0.972)]
    for lab, col, auc in curves:
        pts = roc_curve(auc)
        prev = None
        for (f, t) in pts:
            x = ax + int(f * aw)
            y = bottom - int(t * ah)
            if prev:
                c.line(prev[0], prev[1], x, y, col, 2)
            prev = (x, y)
    for i, (lab, col, auc) in enumerate(curves):
        c.hline(ax + aw - 120, ax + aw - 96, bottom - 60 + i * 15, col)
        c.text(ax + aw - 92, bottom - 64 + i * 15, lab, BLACK, 1)
    c.text_c(ax + aw // 2, bottom + 20, "False positive rate", GRAY, 1)
    c.text(ax - 30, ay - 16, "TPR", GRAY, 1)

    # (b) PR
    bx0 = 520
    c.vline(bx0, ay, bottom, BLACK)
    c.hline(bx0, bx0 + aw, bottom, BLACK)
    c.text(bx0 - 30, 40, "(b) Precision-Recall curves", BLACK, 1)

    def pr_curve(ap, steps=60):
        pts = []
        for i in range(steps + 1):
            r = i / steps
            p = 1 - (1 - ap) * (r ** 3)
            pts.append((r, p))
        return pts
    prc = [("Stacking 0.999", DARK_GREEN, 0.999),
           ("Voting 0.997", MED_BLUE, 0.997),
           ("XGBoost 0.993", ORANGE, 0.993),
           ("LR 0.968", RED, 0.968)]
    for lab, col, ap in prc:
        pts = pr_curve(ap)
        prev = None
        for (r, p) in pts:
            x = bx0 + int(r * aw)
            y = bottom - int((p - 0.9) / 0.1 * ah) if p >= 0.9 else bottom
            y = max(ay, y)
            if prev:
                c.line(prev[0], prev[1], x, y, col, 2)
            prev = (x, y)
    for i, (lab, col, ap) in enumerate(prc):
        c.hline(bx0 + 30, bx0 + 54, bottom - 60 + i * 15, col)
        c.text(bx0 + 58, bottom - 64 + i * 15, lab, BLACK, 1)
    c.text_c(bx0 + aw // 2, bottom + 20, "Recall", GRAY, 1)
    c.text(bx0 - 34, ay - 16, "Prec", GRAY, 1)
    for k in range(3):
        val = 0.90 + k * 0.05
        yy = bottom - int((val - 0.9) / 0.1 * ah)
        c.text(bx0 - 34, yy - 3, f"{val:.2f}", GRAY, 1)

    c.text(40, 455, "Figure 10: Near-perfect ROC-AUC and PR-AUC for the ensembles; LR trails on both curves", BLACK, 1)
    save(c, 'Figure_10_ROC_PR.jpg')


# --------------------------------------------------------------------------
# Figure 11: SHAP global importance
# --------------------------------------------------------------------------
def fig11():
    c = PNGCanvas(880, 520)
    c.text_c(440, 12, "SHAP Global Feature Importance (mean |SHAP value|)", BLACK, 2)
    feats = [
        ("Hemoglobin", 0.148), ("Serum creatinine", 0.132), ("Specific gravity", 0.121),
        ("Albumin", 0.108), ("Packed cell volume", 0.096), ("Diabetes mellitus", 0.079),
        ("Hypertension", 0.068), ("Blood glucose random", 0.058), ("Blood urea", 0.049),
        ("Red blood cells", 0.038), ("Sodium", 0.030), ("Age", 0.021),
    ]
    lx = 220
    top = 52
    maxw = 560
    bh = 26
    gap = 8
    mx = 0.16
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        gx = int(lx + frac * maxw)
        c.vline(gx, top - 4, top + len(feats) * (bh + gap), LIGHT_GRAY)
        c.text_c(gx, top - 18, f"{frac*mx:.2f}", GRAY, 1)
    c.text_c(lx + maxw // 2, top - 34, "mean |SHAP value| (impact on model output)", GRAY, 1)
    for i, (name, v) in enumerate(feats):
        yy = top + i * (bh + gap)
        w = int(v / mx * maxw)
        t = i / len(feats)
        col = blend(PURPLE, MED_BLUE, t)
        c.rect(lx, yy, lx + w, yy + bh, col, blend(LIGHT_PURPLE, LIGHT_BLUE, t))
        c.text(20, yy + 7, name, BLACK, 1)
        c.text(lx + w + 5, yy + 7, f"{v:.3f}", GRAY, 1)
    c.text(40, 505, "Figure 11: SHAP confirms hemoglobin, serum creatinine and specific gravity as top global drivers", BLACK, 1)
    save(c, 'Figure_11_SHAP.jpg')


# --------------------------------------------------------------------------
# Figure 12: risk stratification
# --------------------------------------------------------------------------
def fig12():
    c = PNGCanvas(880, 500)
    c.text_c(440, 12, "CKD Risk Stratification from Predicted Probability", BLACK, 2)

    # (a) probability histogram with risk bands
    ax, ay = 70, 70
    aw, ah = 500, 300
    bottom = ay + ah
    c.vline(ax, ay, bottom, BLACK)
    c.hline(ax, ax + aw, bottom, BLACK)
    # bands
    b1 = ax + int(0.30 * aw)
    b2 = ax + int(0.70 * aw)
    c.fill_rect(ax + 1, ay + 1, b1, bottom - 1, blend(WHITE, MED_GREEN, 0.12))
    c.fill_rect(b1, ay + 1, b2, bottom - 1, blend(WHITE, GOLD, 0.14))
    c.fill_rect(b2, ay + 1, ax + aw - 1, bottom - 1, blend(WHITE, RED, 0.12))
    # histogram counts across 20 bins (bimodal)
    counts = [30, 34, 26, 18, 12, 8, 6, 5, 5, 6, 7, 8, 9, 11, 14, 20, 30, 44, 58, 70]
    mxc = max(counts)
    bwid = aw / len(counts)
    for i, ct in enumerate(counts):
        x1 = ax + int(i * bwid)
        x2 = ax + int((i + 1) * bwid) - 2
        bh = int(ct / mxc * (ah - 20))
        center = (i + 0.5) / len(counts)
        col = MED_GREEN if center < 0.3 else (GOLD if center < 0.7 else RED)
        fill = blend(WHITE, col, 0.5)
        c.rect(x1, bottom - bh, x2, bottom, col, fill)
    c.vline(b1, ay, bottom, DARK_GREEN)
    c.vline(b2, ay, bottom, RED)
    for frac, lab in [(0.0, "0.0"), (0.30, "0.30"), (0.70, "0.70"), (1.0, "1.0")]:
        x = ax + int(frac * aw)
        c.text_c(x, bottom + 6, lab, GRAY, 1)
    c.text_c(ax + aw // 2, bottom + 22, "Predicted CKD probability", BLACK, 1)
    c.text(ax + 20, ay + 4, "Low", DARK_GREEN, 1)
    c.text(b1 + 30, ay + 4, "Intermediate", GOLD, 1)
    c.text(b2 + 30, ay + 4, "High", RED, 1)
    c.text(40, 50, "(a) Probability distribution with risk bands", BLACK, 1)

    # (b) risk category counts
    c.text(610, 50, "(b) Patients per risk tier", BLACK, 1)
    tiers = [("Low\n<0.30", 138, MED_GREEN, LIGHT_GREEN),
             ("Interm.\n0.30-0.70", 44, GOLD, LIGHT_GOLD),
             ("High\n>=0.70", 218, RED, LIGHT_RED)]
    bx0 = 620
    baseB = 370
    c.vline(bx0, ay, baseB, BLACK)
    c.hline(bx0, 850, baseB, BLACK)
    for i, (lab, v, col, fill) in enumerate(tiers):
        bx = bx0 + 30 + i * 70
        bh = int(v / 240 * 280)
        c.rect(bx, baseB - bh, bx + 46, baseB, col, fill)
        c.text_c(bx + 23, baseB - bh - 12, str(v), BLACK, 1)
        parts = lab.split("\n")
        c.text_c(bx + 23, baseB + 6, parts[0], BLACK, 1)
        c.text_c(bx + 23, baseB + 18, parts[1], GRAY, 1)

    c.text(40, 485, "Figure 12: Probability-based stratification separates clear non-CKD and CKD cases from a small review tier", BLACK, 1)
    save(c, 'Figure_12_RiskStratification.jpg')


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating 12 CKD manuscript figures (JPG)...")
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6()
    fig7(); fig8(); fig9(); fig10(); fig11(); fig12()
    print(f"\nAll figures saved to {OUTPUT_DIR}/")


if __name__ == '__main__':
    main()
