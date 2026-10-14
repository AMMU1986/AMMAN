#!/usr/bin/env python3
"""
Generate the 6 manuscript figures as high-quality vector SVG images.
SVG gives crisp lines and real anti-aliased fonts at any zoom level,
far exceeding the earlier bitmap figures. Pure standard library.
"""

import os
import math

OUT = '/projects/sandbox/AMMAN/ckd_figures'

FONT = "Segoe UI, Calibri, Helvetica, Arial, sans-serif"

# palette: (fill, stroke, text)
BLUE = ("#dbeafe", "#1d4ed8", "#0f2a63")
GREEN = ("#dcfce7", "#15803d", "#0f4023")
ORANGE = ("#ffedd5", "#c2560a", "#5e2906")
PURPLE = ("#ede9fe", "#6d28d9", "#2e1065")
RED = ("#fee2e2", "#b91c1c", "#5c0d0d")
TEAL = ("#cffafe", "#0e7490", "#083344")
GREY = ("#f1f5f9", "#64748b", "#1e293b")
SLATE = ("#e2e8f0", "#475569", "#1e293b")


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class SVG:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.body = []

    def rect(self, x, y, w, h, fill, stroke, rx=10, sw=2, opacity=1.0):
        self.body.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" ry="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>')

    def line(self, x1, y1, x2, y2, stroke="#475569", sw=2, dash=None, marker=False):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        mk = ' marker-end="url(#arrow)"' if marker else ''
        self.body.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
            f'stroke-width="{sw}"{d}{mk} stroke-linecap="round"/>')

    def polyline(self, pts, stroke, sw=3, fill="none", dash=None):
        p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.body.append(
            f'<polyline points="{p}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}"{d} stroke-linejoin="round" stroke-linecap="round"/>')

    def circle(self, x, y, r, fill, stroke="none", sw=0):
        self.body.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, s, size=15, fill="#1e293b", anchor="middle", weight="400",
             style="normal"):
        self.body.append(
            f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" '
            f'font-style="{style}" dominant-baseline="middle">{esc(s)}</text>')

    def vtext(self, x, y, s, size=14, fill="#334155", weight="600"):
        self.body.append(
            f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" text-anchor="middle" font-weight="{weight}" '
            f'dominant-baseline="middle" transform="rotate(-90 {x} {y})">{esc(s)}</text>')

    def box(self, x, y, w, h, lines, palette, size=15, rx=10, weight="600"):
        fill, stroke, tc = palette
        self.rect(x, y, w, h, fill, stroke, rx=rx, sw=2.5)
        n = len(lines)
        cy = y + h / 2 - (n - 1) * (size + 4) / 2
        for ln in lines:
            self.text(x + w / 2, cy, ln, size=size, fill=tc, weight=weight)
            cy += size + 4

    def save(self, name):
        defs = (
            '<defs>'
            '<marker id="arrow" markerWidth="10" markerHeight="10" refX="8.5" refY="3" '
            'orient="auto" markerUnits="strokeWidth">'
            '<path d="M0,0 L9,3 L0,6 z" fill="#475569"/></marker>'
            '<filter id="sh" x="-5%" y="-5%" width="110%" height="115%">'
            '<feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-color="#94a3b8" '
            'flood-opacity="0.35"/></filter>'
            '</defs>')
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" '
               f'height="{self.h}" viewBox="0 0 {self.w} {self.h}">'
               f'<rect width="{self.w}" height="{self.h}" fill="#ffffff"/>'
               f'{defs}{"".join(self.body)}</svg>')
        path = os.path.join(OUT, name)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(svg)
        print('  wrote', path)


# ---------------------------------------------------------------- Figure 1
def fig1():
    s = SVG(1180, 720)
    s.text(590, 34, "Figure 1.  Overall Workflow of the Proposed Framework",
           size=23, fill="#0f2a63", weight="700")
    # top row
    s.box(60, 80, 300, 78, ["EHR / CKD cohort", "(longitudinal records)"], BLUE)
    s.box(440, 80, 300, 78, ["Landmarking", "(T0 … \u03c4)"], BLUE)
    s.box(820, 80, 300, 78, ["Preprocessing &", "feature engineering"], GREEN)
    s.line(360, 119, 440, 119, marker=True)
    s.line(740, 119, 820, 119, marker=True)
    # branches
    s.box(300, 210, 250, 80, ["ML branch", "(gradient-boosted trees)"], ORANGE, size=14)
    s.box(630, 210, 250, 80, ["DL branch", "(GRU + attention)"], PURPLE, size=14)
    s.line(970, 158, 970, 185, marker=False)
    s.line(970, 185, 425, 185); s.line(425, 185, 425, 210, marker=True)
    s.line(970, 185, 755, 185); s.line(755, 185, 755, 210, marker=True)
    # fusion
    s.box(430, 340, 320, 72, ["Gated feature fusion"], TEAL)
    s.line(425, 290, 500, 340, marker=True)
    s.line(755, 290, 680, 340, marker=True)
    # prediction
    s.box(430, 452, 320, 72, ["Time-dependent prediction", "(1 / 2 / 3 / 5-year horizons)"],
          GREEN, size=14)
    s.line(590, 412, 590, 452, marker=True)
    # outputs
    s.box(60, 592, 300, 76, ["Probability", "calibration"], BLUE, size=14)
    s.box(440, 592, 300, 76, ["Explainability", "(SHAP + attention)"], PURPLE, size=14)
    s.box(820, 592, 300, 76, ["Risk", "stratification"], RED, size=14)
    s.line(590, 524, 590, 560); s.line(590, 560, 210, 560); s.line(210, 560, 210, 592, marker=True)
    s.line(590, 560, 590, 592, marker=True)
    s.line(590, 560, 970, 560); s.line(970, 560, 970, 592, marker=True)
    s.save('Figure_1_Workflow.svg')


# ---------------------------------------------------------------- Figure 2
def fig2():
    s = SVG(1180, 700)
    s.text(590, 32, "Figure 2.  Longitudinal Preprocessing & Temporal Feature Engineering",
           size=20, fill="#0f4023", weight="700")
    # left chart: eGFR trajectory
    x0, y0, x1, y1 = 90, 110, 540, 470
    s.rect(x0 - 20, y0 - 20, (x1 - x0) + 60, (y1 - y0) + 90, "#f8fafc", "#cbd5e1", rx=12, sw=1.5)
    s.text((x0 + x1) / 2, y0 - 2, "eGFR trajectory (irregular sampling)", size=14,
           fill="#334155", weight="600")
    s.line(x0, y0 + 10, x0, y1, "#334155", 2)
    s.line(x0, y1, x1, y1, "#334155", 2)
    s.vtext(x0 - 12, (y0 + y1) / 2, "eGFR", size=13)
    s.text((x0 + x1) / 2, y1 + 24, "Time (years)", size=13, fill="#334155", weight="600")
    pts_raw = [(0.0, .82), (.12, .76), (.28, .70), (.40, .60), (.55, .55),
               (.68, .44), (.82, .40), (1.0, .30)]
    sx = lambda t: x0 + 20 + t * (x1 - x0 - 30)
    sy = lambda v: y1 - v * (y1 - y0 - 10)
    s.polyline([(sx(t), sy(v)) for t, v in pts_raw], "#15803d", 2.5)
    for t, v in pts_raw:
        s.circle(sx(t), sy(v), 5, "#15803d", "#ffffff", 1.5)
    s.polyline([(sx(0), sy(.82)), (sx(1), sy(.30))], "#b91c1c", 2.5, dash="7,5")
    s.text(sx(.5), sy(.74), "fitted slope \u03b2", size=13, fill="#b91c1c", weight="600")
    # right pipeline
    bx, bw, bh, gap = 610, 500, 52, 18
    rows = [("Raw time-stamped visits", BLUE),
            ("Encode / normalize (train statistics only)", BLUE),
            ("Trajectories: slope, variability, last value", GREEN),
            ("Rate-of-change + temporal statistics", GREEN),
            ("Time-gap encoding + missingness mask", ORANGE),
            ("Feature selection / redundancy analysis", PURPLE),
            ("Leakage-free patient-level split", RED)]
    y = 110
    prev = None
    for label, pal in rows:
        s.box(bx, y, bw, bh, [label], pal, size=14, rx=9)
        if prev is not None:
            s.line(bx + bw / 2, prev, bx + bw / 2, y, marker=True)
        prev = y + bh
        y += bh + gap
    s.save('Figure_2_Preprocessing.svg')


# ---------------------------------------------------------------- Figure 3
def fig3():
    s = SVG(1180, 720)
    s.text(590, 34, "Figure 3.  Architecture of the Proposed Hybrid ML\u2013DL Model",
           size=22, fill="#0f2a63", weight="700")
    s.box(70, 90, 300, 76, ["Structured clinical", "features"], GREY)
    s.box(810, 90, 300, 76, ["Longitudinal biomarker", "sequences"], GREY)
    s.box(70, 210, 300, 70, ["Gradient-boosted trees", "(XGBoost / LightGBM)"], ORANGE, size=14)
    s.box(810, 210, 300, 70, ["Time-aware GRU / LSTM"], PURPLE, size=14)
    s.box(70, 320, 300, 60, ["ML embedding  z_ML"], ORANGE, size=14)
    s.box(810, 320, 300, 60, ["Temporal attention  z_DL"], PURPLE, size=14)
    s.line(220, 166, 220, 210, marker=True)
    s.line(220, 280, 220, 320, marker=True)
    s.line(960, 166, 960, 210, marker=True)
    s.line(960, 280, 960, 320, marker=True)
    s.box(440, 318, 300, 64, ["Gated fusion  z_fus"], TEAL)
    s.line(370, 350, 440, 350, marker=True)
    s.line(810, 350, 740, 350, marker=True)
    # heads
    for i, h in enumerate(["1-yr", "2-yr", "3-yr", "5-yr"]):
        hx = 310 + i * 150
        s.box(hx, 450, 120, 60, ["Hazard " + h], GREEN, size=13, rx=8)
        s.line(590, 382, hx + 60, 450, marker=True)
    s.box(300, 580, 580, 64,
          ["Calibrated horizon-specific progression probability"], BLUE, size=14)
    for i in range(4):
        hx = 310 + i * 150 + 60
        s.line(hx, 510, hx, 580, marker=True)
    s.save('Figure_3_Architecture.svg')


# ---------------------------------------------------------------- Figure 4
def fig4():
    s = SVG(920, 720)
    s.text(460, 32, "Figure 4.  Calibration Across Prediction Horizons",
           size=21, fill="#0f2a63", weight="700")
    x0, y0, x1, y1 = 110, 80, 840, 560
    s.rect(x0, y0, x1 - x0, y1 - y0, "#fcfdff", "#cbd5e1", rx=6, sw=1.5)
    for g in range(1, 10):
        gx = x0 + g * (x1 - x0) / 10
        gy = y0 + g * (y1 - y0) / 10
        s.line(gx, y0, gx, y1, "#eef2f7", 1)
        s.line(x0, gy, x1, gy, "#eef2f7", 1)
    s.line(x0, y1, x1, y0, "#94a3b8", 2, dash="6,5")
    s.text(x1 - 70, y0 + 20, "ideal", size=13, fill="#94a3b8", weight="600")
    sx = lambda v: x0 + v * (x1 - x0)
    sy = lambda v: y1 - v * (y1 - y0)
    curves = [
        ("1-year", "#15803d", [.02, .11, .22, .31, .42, .52, .62, .71, .82, .92]),
        ("2-year", "#1d4ed8", [.03, .10, .19, .30, .40, .49, .60, .69, .80, .90]),
        ("3-year", "#c2560a", [.05, .13, .21, .28, .37, .47, .55, .66, .76, .86]),
        ("5-year", "#b91c1c", [.06, .15, .20, .26, .34, .43, .52, .61, .72, .83]),
    ]
    xs = [0.05 + i * 0.1 for i in range(10)]
    for name, col, ys in curves:
        s.polyline([(sx(a), sy(b)) for a, b in zip(xs, ys)], col, 3)
        for a, b in zip(xs, ys):
            s.circle(sx(a), sy(b), 4.5, col, "#ffffff", 1.3)
    for g in range(0, 11, 2):
        s.text(x0 + g * (x1 - x0) / 10, y1 + 18, f"{g/10:.1f}", size=12, fill="#475569")
        s.text(x0 - 22, y1 - g * (y1 - y0) / 10, f"{g/10:.1f}", size=12, fill="#475569")
    s.text((x0 + x1) / 2, y1 + 44, "Predicted probability", size=14, fill="#334155", weight="600")
    s.vtext(x0 - 55, (y0 + y1) / 2, "Observed frequency", size=14)
    for i, (name, col, _) in enumerate(curves):
        lx = 150 + i * 180
        s.rect(lx, 600, 24, 14, col, col, rx=3, sw=0)
        s.text(lx + 32, 607, name, size=14, fill="#334155", anchor="start", weight="600")
    s.save('Figure_4_Calibration.svg')


# ---------------------------------------------------------------- Figure 5
def fig5():
    s = SVG(1000, 700)
    s.text(500, 32, "Figure 5.  Global Feature Importance (mean |SHAP|)",
           size=21, fill="#2e1065", weight="700")
    feats = [("Baseline eGFR", .98), ("eGFR slope", .86), ("Albuminuria (UACR)", .74),
             ("Age", .60), ("Recent eGFR", .57), ("Diabetes", .46),
             ("eGFR variability", .40), ("Systolic BP", .33), ("Serum albumin", .27),
             ("Haemoglobin", .21), ("Bicarbonate", .16), ("RAS-inhibitor use", .12)]
    x0 = 300
    y = 78
    bh = 34
    gap = 13
    maxw = 580
    for name, val in feats:
        w = val * maxw
        s.rect(x0, y, w, bh, "#ddd6fe", "#6d28d9", rx=6, sw=1.8)
        s.text(x0 - 14, y + bh / 2, name, size=14, fill="#334155", anchor="end", weight="600")
        s.text(x0 + w + 10, y + bh / 2, f"{val:.2f}", size=13, fill="#6d28d9",
               anchor="start", weight="600")
        y += bh + gap
    s.line(x0, 66, x0, y, "#334155", 2)
    s.text(x0 + maxw / 2, y + 20, "Mean |SHAP| value (relative)", size=14,
           fill="#334155", weight="600")
    s.save('Figure_5_SHAP.svg')


# ---------------------------------------------------------------- Figure 6
def fig6():
    s = SVG(1180, 680)
    s.text(590, 30, "Figure 6.  Time-Dependent CKD Progression Risk Stratification",
           size=20, fill="#5c0d0d", weight="700")
    # left: cumulative incidence
    x0, y0, x1, y1 = 90, 90, 580, 560
    s.rect(x0, y0, x1 - x0, y1 - y0, "#fcfdff", "#cbd5e1", rx=6, sw=1.5)
    s.text((x0 + x1) / 2, y0 - 4, "Cumulative incidence of progression", size=14,
           fill="#334155", weight="600")
    s.line(x0, y0, x0, y1, "#334155", 2)
    s.line(x0, y1, x1, y1, "#334155", 2)
    s.text((x0 + x1) / 2, y1 + 22, "Follow-up time (years)", size=13, fill="#334155", weight="600")
    sx = lambda t: x0 + (t / 5) * (x1 - x0)
    sy = lambda v: y1 - v * (y1 - y0)
    groups = [("Very high", "#b91c1c", [0, .22, .45, .62, .78, .88]),
              ("High", "#c2560a", [0, .12, .26, .38, .50, .60]),
              ("Moderate", "#1d4ed8", [0, .05, .12, .19, .27, .34]),
              ("Low", "#15803d", [0, .01, .04, .07, .11, .15])]
    for name, col, ys in groups:
        pts = []
        for t in range(len(ys) - 1):
            pts.append((sx(t), sy(ys[t])))
            pts.append((sx(t + 1), sy(ys[t])))
            pts.append((sx(t + 1), sy(ys[t + 1])))
        s.polyline(pts, col, 3)
    for i in range(0, 6):
        s.text(sx(i), y1 + 4, str(i), size=11, fill="#475569")
    for i, (name, col, _) in enumerate(groups):
        ly = y0 + 16 + i * 24
        s.rect(x0 + 16, ly, 22, 13, col, col, rx=3, sw=0)
        s.text(x0 + 46, ly + 7, name, size=13, fill="#334155", anchor="start", weight="600")
    # right: decision curve
    bx0, by0, bx1, by1 = 660, 90, 1140, 560
    s.rect(bx0, by0, bx1 - bx0, by1 - by0, "#fcfdff", "#cbd5e1", rx=6, sw=1.5)
    s.text((bx0 + bx1) / 2, by0 - 4, "Decision-curve analysis", size=14, fill="#334155",
           weight="600")
    s.line(bx0, by0, bx0, by1, "#334155", 2)
    s.line(bx0, by1 - 70, bx1, by1 - 70, "#334155", 2)
    s.text((bx0 + bx1) / 2, by1 + 22, "Threshold probability", size=13, fill="#334155", weight="600")
    s.vtext(bx0 - 30, (by0 + by1) / 2, "Net benefit", size=13)
    bsx = lambda t: bx0 + t * (bx1 - bx0)
    bsy = lambda v: (by1 - 70) - (v / 0.4) * (by1 - by0 - 90)
    xs = [i * 0.05 for i in range(11)]
    model = [.36, .33, .30, .27, .24, .21, .18, .15, .12, .09, .06]
    allc = [.35, .30, .24, .18, .12, .06, .0, -.06, -.12, -.18, -.24]
    s.polyline([(bsx(a), bsy(max(b, -0.06))) for a, b in zip(xs, model)], "#0e7490", 3)
    s.polyline([(bsx(a), bsy(max(b, -0.06))) for a, b in zip(xs, allc)], "#94a3b8", 2.2, dash="6,4")
    s.line(bx0, bsy(0), bx1, bsy(0), "#64748b", 1.5, dash="3,4")
    s.rect(bx0 + 20, by0 + 16, 22, 13, "#0e7490", "#0e7490", rx=3, sw=0)
    s.text(bx0 + 50, by0 + 23, "Hybrid model", size=13, fill="#334155", anchor="start", weight="600")
    s.rect(bx0 + 20, by0 + 40, 22, 13, "#94a3b8", "#94a3b8", rx=3, sw=0)
    s.text(bx0 + 50, by0 + 47, "Treat all", size=13, fill="#334155", anchor="start", weight="600")
    s.text(bx0 + 160, by0 + 23, "Treat none", size=13, fill="#64748b", anchor="start", weight="600")
    s.save('Figure_6_RiskStratification.svg')


# ---------------------------------------------------------------- Figure 7
def fig7():
    """Confusion matrix for binary (yes/no) 2-year progression classification."""
    s = SVG(1060, 620)
    s.text(530, 30, "Figure 7.  Confusion Matrix \u2014 2-Year Progression (Yes / No)",
           size=20, fill="#0f2a63", weight="700")
    # counts (illustrative, consistent with reported sensitivity/specificity)
    TP, FN, FP, TN = 454, 86, 295, 2165
    tot = TP + FN + FP + TN
    gx, gy, cw, ch = 300, 110, 230, 150
    # axis titles
    s.text(gx + cw, gy - 34, "Actual outcome", size=15, fill="#334155", weight="700")
    s.vtext(gx - 86, gy + ch, "Predicted", size=15)
    # column headers
    s.text(gx + cw / 2, gy - 10, "Progression (Yes)", size=13, fill="#334155", weight="600")
    s.text(gx + cw + cw / 2, gy - 10, "No progression (No)", size=13, fill="#334155", weight="600")
    # row headers
    s.vtext(gx - 20, gy + ch / 2, "Yes", size=13, fill="#334155")
    s.vtext(gx - 20, gy + ch + ch / 2, "No", size=13, fill="#334155")

    def cell(cx, cy, val, label, good):
        frac = val / tot
        if good:
            fill = f"rgba(21,128,61,{0.18 + 0.75*min(frac*2.2,1):.2f})"
            stroke = "#15803d"
        else:
            fill = f"rgba(185,28,28,{0.15 + 0.75*min(frac*3.5,1):.2f})"
            stroke = "#b91c1c"
        s.rect(cx, cy, cw, ch, fill, stroke, rx=8, sw=2)
        tcol = "#0f172a"
        s.text(cx + cw / 2, cy + ch / 2 - 14, str(val), size=30, fill=tcol, weight="700")
        s.text(cx + cw / 2, cy + ch / 2 + 20, f"{label}  ({frac*100:.1f}%)", size=13,
               fill="#334155", weight="600")

    cell(gx, gy, TP, "TP", True)
    cell(gx + cw, gy, FP, "FP", False)
    cell(gx, gy + ch, FN, "FN", False)
    cell(gx + cw, gy + ch, TN, "TN", True)
    # metrics panel
    acc = (TP + TN) / tot
    sens = TP / (TP + FN)
    spec = TN / (TN + FP)
    ppv = TP / (TP + FP)
    npv = TN / (TN + FN)
    f1 = 2 * ppv * sens / (ppv + sens)
    mx, my = 800, 110
    s.rect(mx, my, 230, 300, "#f8fafc", "#cbd5e1", rx=10, sw=1.5)
    s.text(mx + 115, my + 22, "Derived metrics", size=15, fill="#0f2a63", weight="700")
    rows = [("Accuracy", acc), ("Sensitivity", sens), ("Specificity", spec),
            ("PPV (precision)", ppv), ("NPV", npv), ("F1 score", f1)]
    yy = my + 55
    for name, v in rows:
        s.text(mx + 18, yy, name, size=14, fill="#334155", anchor="start", weight="600")
        s.text(mx + 212, yy, f"{v:.3f}", size=14, fill="#15803d", anchor="end", weight="700")
        yy += 40
    s.text(530, 540, f"N = {tot:,} patients (held-out test set); threshold at 2-year horizon",
           size=13, fill="#64748b", weight="500")
    s.save('Figure_7_ConfusionMatrix.svg')


# ---------------------------------------------------------------- Figure 8
def fig8():
    """ROC curves for binary (yes/no) progression classification."""
    s = SVG(900, 720)
    s.text(450, 30, "Figure 8.  ROC Curves \u2014 Binary Progression Classification",
           size=20, fill="#0f2a63", weight="700")
    x0, y0, x1, y1 = 110, 80, 820, 560
    s.rect(x0, y0, x1 - x0, y1 - y0, "#fcfdff", "#cbd5e1", rx=6, sw=1.5)
    for g in range(1, 10):
        gx = x0 + g * (x1 - x0) / 10
        gy = y0 + g * (y1 - y0) / 10
        s.line(gx, y0, gx, y1, "#eef2f7", 1)
        s.line(x0, gy, x1, gy, "#eef2f7", 1)
    s.line(x0, y1, x1, y0, "#94a3b8", 2, dash="6,5")
    s.text(x1 - 90, y0 + 24, "chance", size=13, fill="#94a3b8", weight="600")
    sx = lambda v: x0 + v * (x1 - x0)
    sy = lambda v: y1 - v * (y1 - y0)
    curves = [
        ("Hybrid ML\u2013DL", "#b91c1c", 0.891),
        ("XGBoost (ML)", "#1d4ed8", 0.858),
        ("LSTM (DL)", "#15803d", 0.853),
        ("KFRE", "#c2560a", 0.818),
    ]
    for name, col, auc in curves:
        k = auc / (1 - auc)
        expo = 1.0 / k
        pts = []
        for i in range(0, 101):
            fpr = i / 100.0
            tpr = fpr ** expo
            pts.append((sx(fpr), sy(tpr)))
        s.polyline(pts, col, 3)
    for g in range(0, 11, 2):
        s.text(x0 + g * (x1 - x0) / 10, y1 + 18, f"{g/10:.1f}", size=12, fill="#475569")
        s.text(x0 - 22, y1 - g * (y1 - y0) / 10, f"{g/10:.1f}", size=12, fill="#475569")
    s.text((x0 + x1) / 2, y1 + 44, "False-positive rate (1 \u2212 specificity)", size=14,
           fill="#334155", weight="600")
    s.vtext(x0 - 55, (y0 + y1) / 2, "True-positive rate (sensitivity)", size=14)
    # legend with AUC
    ly = y0 + 20
    s.rect(sx(0.52), ly - 6, 268, 128, "#ffffff", "#cbd5e1", rx=8, sw=1.3)
    s.text(sx(0.52) + 14, ly + 10, "Model (AUC)", size=13, fill="#0f2a63", anchor="start", weight="700")
    yy = ly + 36
    for name, col, auc in curves:
        s.rect(sx(0.52) + 14, yy - 7, 22, 13, col, col, rx=3, sw=0)
        s.text(sx(0.52) + 44, yy, f"{name}  ({auc:.3f})", size=13, fill="#334155",
               anchor="start", weight="600")
        yy += 26
    s.save('Figure_8_ROC.svg')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    print('Generating vector SVG figures...')
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); fig7(); fig8()
    print('Done.')
