#!/usr/bin/env python3
"""
Generate the three figures for the PPI deprescribing manuscript using the
pure-standard-library drawing helper (no matplotlib/numpy).

Figure 1  Outcomes heatmap (Intervention vs Control, baseline vs 6 months)
Figure 2  Forest plot of multivariable predictors of appropriate PPI use
Figure 3  Stacked-bar distribution of PPI management outcomes by group
"""

import math
import os
from ppi_plot_lib import Canvas, viridis, text_color_for, text_width

OUT = '/projects/sandbox/AMMAN/ppi_figures'
os.makedirs(OUT, exist_ok=True)

AXIS = (30, 30, 30)
GRID = (200, 200, 200)


# ===========================================================================
# Figure 1 — Heatmap
# ===========================================================================
def figure1_heatmap():
    rows = [
        "Inappropriate PPI use (%)",
        "Complete discontinuation (%)",
        "Dose reduction/step-down (%)",
        "On-demand use (%)",
        "Adequate symptom control (%)",
        "Knowledge score (of 12)",
        ">=3 long-term risks (%)",
        "Monthly PPI cost index",
    ]
    cols = [
        ["Intervention", "Baseline"],
        ["Intervention", "6 months"],
        ["Control", "Baseline"],
        ["Control", "6 months"],
    ]
    N = None
    data = [
        [68.6, 31.4, 66.7, 60.5],
        [N,    27.6, N,    8.6],
        [N,    34.3, N,    14.3],
        [N,    21.0, N,    7.1],
        [85.0, 85.2, 84.0, 83.3],
        [4.1,  8.6,  4.2,  4.9],
        [11.9, 71.4, 12.4, 18.6],
        [100.0, 58.0, 100.0, 92.0],
    ]

    W, H = 1200, 720
    c = Canvas(W, H)
    left, top = 380, 90
    right, bottom = 980, 630
    ncol, nrow = 4, 8
    cw = (right - left) / ncol
    rh = (bottom - top) / nrow

    c.text_center(W // 2, 24, "PPI Treatment and Educational Outcomes: Baseline vs 6 Months",
                  color=(20, 20, 20), scale=3)

    # cells
    for r in range(nrow):
        for k in range(ncol):
            x0 = left + k * cw
            y0 = top + r * rh
            v = data[r][k]
            if v is None:
                c.fill_rect(x0, y0, x0 + cw, y0 + rh, (255, 255, 255))
                c.rect_outline(x0, y0, x0 + cw, y0 + rh, (225, 225, 225), 1)
                continue
            t = max(0.0, min(1.0, v / 100.0))
            bg = viridis(t)
            c.fill_rect(x0, y0, x0 + cw, y0 + rh, bg)
            c.rect_outline(x0, y0, x0 + cw, y0 + rh, (255, 255, 255), 1)
            label = ("%g" % v)
            c.text_center(int(x0 + cw / 2), int(y0 + rh / 2 - 8), label,
                          color=text_color_for(bg), scale=3)

    # row labels
    for r in range(nrow):
        y = top + r * rh + rh / 2 - 6
        c.text_right(left - 12, int(y), rows[r], color=(20, 20, 20), scale=2)

    # column labels (two lines) at bottom
    for k in range(ncol):
        x = left + k * cw + cw / 2
        c.text_center(int(x), bottom + 14, cols[k][0], color=(20, 20, 20), scale=2)
        c.text_center(int(x), bottom + 34, cols[k][1], color=(20, 20, 20), scale=2)

    # axis titles
    c.text_center((left + right) // 2, bottom + 62,
                  "Study Group and Time Point", color=(20, 20, 20), scale=2)
    c.vtext(18, top + 60, "Outcome", color=(20, 20, 20), scale=2)

    # colorbar
    cb_x0, cb_x1 = 1040, 1080
    cb_y0, cb_y1 = top, bottom
    steps = 240
    for i in range(steps):
        yy0 = cb_y1 - (i + 1) * (cb_y1 - cb_y0) / steps
        yy1 = cb_y1 - i * (cb_y1 - cb_y0) / steps
        col = viridis(i / (steps - 1))
        c.fill_rect(cb_x0, yy0, cb_x1, yy1, col)
    c.rect_outline(cb_x0, cb_y0, cb_x1, cb_y1, AXIS, 1)
    for tick in range(0, 101, 20):
        yy = cb_y1 - tick / 100.0 * (cb_y1 - cb_y0)
        c.hline(cb_x1, cb_x1 + 6, yy, AXIS)
        c.text(cb_x1 + 10, int(yy) - 6, str(tick), color=(20, 20, 20), scale=2)
    c.vtext(cb_x1 + 58, cb_y0 + 150, "Value", color=(20, 20, 20), scale=2)

    path = os.path.join(OUT, "Figure_1_Outcomes_Heatmap.png")
    c.save_png(path)
    print("  ", path)


# ===========================================================================
# Figure 2 — Forest plot
# ===========================================================================
def figure2_forest():
    preds = [
        ("Intervention (vs control)",         3.86, 2.52, 5.91, (31, 119, 180), "3.86 (2.52-5.91)"),
        ("Knowledge score (per point)",       1.34, 1.21, 1.49, (255, 127, 14), "1.34 (1.21-1.49)"),
        ("Shorter prior PPI duration",        1.28, 1.06, 1.55, (44, 160, 44),  "1.28 (1.06-1.55)"),
        ("Age (per 10 years)",                0.83, 0.71, 0.97, (214, 39, 40),  "0.83 (0.71-0.97)"),
        ("Polypharmacy (>=5 medicines)",      0.66, 0.44, 0.99, (148, 103, 189),"0.66 (0.44-0.99)"),
    ]
    W, H = 1160, 620
    c = Canvas(W, H)
    left, right = 370, 740
    top, bottom = 90, 470

    c.text_center(W // 2, 24,
                  "Multivariable Predictors of Appropriate PPI Use at 6 Months",
                  color=(20, 20, 20), scale=3)

    lo_or, hi_or = 0.4, 6.6
    lx0, lx1 = math.log10(lo_or), math.log10(hi_or)

    def xpos(orv):
        return left + (math.log10(orv) - lx0) / (lx1 - lx0) * (right - left)

    # gridlines / ticks
    ticks = [0.5, 1, 2, 4, 6]
    for tk in ticks:
        x = xpos(tk)
        col = AXIS if tk == 1 else GRID
        if tk == 1:
            # dashed reference line
            y = top - 10
            while y < bottom + 10:
                c.vline(x, y, min(y + 8, bottom + 10), (70, 130, 180))
                y += 16
        else:
            c.vline(x, top - 10, bottom + 10, col)
        lab = ("%g" % tk)
        c.text_center(int(x), bottom + 18, lab, color=(20, 20, 20), scale=2)

    n = len(preds)
    rh = (bottom - top) / n
    for i, (name, orv, lo, hi, col, ann) in enumerate(preds):
        yc = top + i * rh + rh / 2
        c.text_right(left - 16, int(yc) - 6, name, color=(20, 20, 20), scale=2)
        x_lo, x_hi, x_c = xpos(lo), xpos(hi), xpos(orv)
        # CI line
        c.line(x_lo, yc, x_hi, yc, col, thickness=3)
        # caps
        c.vline(x_lo, yc - 8, yc + 8, col)
        c.vline(x_hi, yc - 8, yc + 8, col)
        # point
        c.fill_circle(x_c, yc, 7, col)
        # annotation
        c.text(right + 24, int(yc) - 6, ann, color=(20, 20, 20), scale=2)

    # axis line + label
    c.hline(left - 10, right + 10, bottom + 8, AXIS)
    c.text_center((left + right) // 2, bottom + 44,
                  "Adjusted odds ratio (aOR), log scale", color=(20, 20, 20), scale=2)

    # footnote
    c.text(60, H - 70,
           "Points are adjusted odds ratios from multivariable logistic regression;",
           color=(90, 90, 90), scale=2)
    c.text(60, H - 48,
           "horizontal bars show 95% confidence intervals. Reference line at aOR = 1.",
           color=(90, 90, 90), scale=2)
    c.text(60, H - 26,
           "OR > 1 favours appropriate PPI use; OR < 1 indicates lower odds.",
           color=(90, 90, 90), scale=2)

    path = os.path.join(OUT, "Figure_2_Forest_Plot.png")
    c.save_png(path)
    print("  ", path)


# ===========================================================================
# Figure 3 — Stacked bar: management outcomes by group
# ===========================================================================
def figure3_stacked():
    cats = ["Discontinued", "Dose reduced / step-down", "On-demand use", "No change"]
    colors = [(26, 152, 80), (145, 207, 96), (253, 174, 97), (215, 48, 39)]
    groups = [
        ("Intervention", [27.6, 34.3, 21.0, 17.1]),
        ("Control",      [8.6, 14.3, 7.1, 70.0]),
    ]

    W, H = 1120, 560
    c = Canvas(W, H)
    left, right = 210, 1000
    top, bottom = 110, 360

    c.text_center(W // 2, 26,
                  "Distribution of PPI Management Outcomes at 6 Months by Group",
                  color=(20, 20, 20), scale=3)

    n = len(groups)
    band = (bottom - top) / n
    barh = band * 0.55
    for gi, (gname, vals) in enumerate(groups):
        yc = top + gi * band + band / 2
        y0 = yc - barh / 2
        c.text_right(left - 16, int(yc) - 6, gname, color=(20, 20, 20), scale=2)
        cum = 0.0
        for ci, v in enumerate(vals):
            xs = left + cum / 100.0 * (right - left)
            xe = left + (cum + v) / 100.0 * (right - left)
            c.fill_rect(xs, y0, xe, y0 + barh, colors[ci])
            if v >= 4:
                tc = text_color_for(colors[ci])
                c.text_center(int((xs + xe) / 2), int(yc) - 6, ("%.1f" % v), color=tc, scale=2)
            cum += v

    # x-axis 0-100
    c.hline(left, right, bottom + 6, AXIS)
    for tick in range(0, 101, 20):
        x = left + tick / 100.0 * (right - left)
        c.vline(x, bottom + 6, bottom + 12, AXIS)
        c.text_center(int(x), bottom + 18, str(tick), color=(20, 20, 20), scale=2)
    c.text_center((left + right) // 2, bottom + 44,
                  "Percentage of participants within group (%)", color=(20, 20, 20), scale=2)

    # legend
    ly = H - 70
    lx = 150
    for ci, cat in enumerate(cats):
        c.fill_rect(lx, ly, lx + 26, ly + 26, colors[ci])
        c.rect_outline(lx, ly, lx + 26, ly + 26, (120, 120, 120), 1)
        c.text(lx + 34, ly + 4, cat, color=(20, 20, 20), scale=2)
        lx += 60 + text_width(cat, 2, 1)

    path = os.path.join(OUT, "Figure_3_Management_Stacked_Bar.png")
    c.save_png(path)
    print("  ", path)


if __name__ == '__main__':
    print("Generating PPI manuscript figures...")
    figure1_heatmap()
    figure2_forest()
    figure3_stacked()
    print("Done.")
