#!/usr/bin/env python3
"""
Generate a Vickers microhardness traverse (with and without cathodic hydrogen
charging) for the API X70 SMAW weldment described in the manuscript.

Traverse: -8 mm to +8 mm, step 0.01 mm (weld centre = 0 mm).

Region layout (symmetric about the weld centreline):
    Weld / Fusion zone (FZ):  -5.0  <= x <= +5.0 mm
    HAZ:                      -7.5  <= x <  -5.0 mm   and  +5.0 < x <= +7.5 mm
    Base metal (BM):          |x| > 7.5 mm

Hardness levels (HV0.5) taken from the manuscript (Table 1 / text):
    Region   Uncharged    Charged
    FZ       196.0        209.0
    HAZ      252.6        275.0
    BM       214.6        220.0

Pure-Python: produces a CSV of the data and a self-contained SVG plot
(no numpy / matplotlib required).
"""

import math
import random

# ----------------------------------------------------------------------------
# 1. Data generation
# ----------------------------------------------------------------------------
X_MIN, X_MAX, STEP = -8.0, 8.0, 0.01

FZ_HALF, HAZ_OUTER = 5.0, 7.5          # region boundaries (mm, |x|)
TW = 0.35                               # transition (blend) width, mm

# (uncharged mean, charged mean, scatter std) per region
FZ  = (196.0, 209.0, 5.7)
HAZ = (252.6, 275.0, 7.0)
BM  = (214.6, 220.0, 5.0)


def sigmoid(t):
    return 1.0 / (1.0 + math.exp(-t))


def region_weights(x):
    """Smoothly blended weights (w_fz, w_haz, w_bm) summing to 1."""
    a = abs(x)
    w1 = sigmoid((a - FZ_HALF) / TW)     # 0 inside FZ -> 1 outside
    w2 = sigmoid((a - HAZ_OUTER) / TW)   # 0 inside HAZ -> 1 in BM
    w_fz = 1.0 - w1
    w_haz = w1 * (1.0 - w2)
    w_bm = w2
    return w_fz, w_haz, w_bm


def mean_at(x, which):
    """which = 0 -> uncharged mean, 1 -> charged mean."""
    w_fz, w_haz, w_bm = region_weights(x)
    return w_fz * FZ[which] + w_haz * HAZ[which] + w_bm * BM[which]


def std_at(x):
    w_fz, w_haz, w_bm = region_weights(x)
    return w_fz * FZ[2] + w_haz * HAZ[2] + w_bm * BM[2]


def region_name(x):
    a = abs(x)
    if a <= FZ_HALF:
        return "Weld (FZ)"
    if a <= HAZ_OUTER:
        return "HAZ"
    return "Base metal"


def build_profile(seed):
    rng = random.Random(seed)
    n = int(round((X_MAX - X_MIN) / STEP))
    xs, unch, chg = [], [], []
    for i in range(n + 1):
        x = round(X_MIN + i * STEP, 2)
        s = std_at(x)
        # modest measurement scatter (0.25*std) so trend stays readable at 0.01 mm
        xs.append(x)
        unch.append(mean_at(x, 0) + rng.gauss(0.0, 0.25 * s))
        chg.append(mean_at(x, 1) + rng.gauss(0.0, 0.25 * s))
    return xs, unch, chg


xs, y_unch, y_chg = build_profile(seed=20250117)

# ----------------------------------------------------------------------------
# 2. Write CSV
# ----------------------------------------------------------------------------
with open("hardness_profile_data.csv", "w") as f:
    f.write("x_mm,region,hardness_uncharged_HV,hardness_charged_HV\n")
    for x, u, c in zip(xs, y_unch, y_chg):
        f.write(f"{x:.2f},{region_name(x)},{u:.2f},{c:.2f}\n")

# ----------------------------------------------------------------------------
# 3. Build SVG plot
# ----------------------------------------------------------------------------
W, H = 1040, 640
ML, MR, MT, MB = 90, 230, 70, 70          # margins (big right margin for legend)
PW, PH = W - ML - MR, H - MT - MB          # plot area

Y_MIN, Y_MAX = 170.0, 295.0
X_TICKS = [-8, -6, -4, -2, 0, 2, 4, 6, 8]
Y_TICKS = [170, 190, 210, 230, 250, 270, 290]


def px(x):
    return ML + (x - X_MIN) / (X_MAX - X_MIN) * PW


def py(y):
    return MT + (Y_MAX - y) / (Y_MAX - Y_MIN) * PH


def polyline(ys, color, width):
    pts = " ".join(f"{px(x):.2f},{py(y):.2f}" for x, y in zip(xs, ys))
    return (f'<polyline fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linejoin="round" points="{pts}"/>')


# region shading bands: (x0, x1, colour, label)
bands = [
    (-8.0, -7.5, "#eaf2e9", "BM"),
    (-7.5, -5.0, "#fdecec", "HAZ"),
    (-5.0,  5.0, "#eaf0fb", "Weld (FZ)"),
    ( 5.0,  7.5, "#fdecec", "HAZ"),
    ( 7.5,  8.0, "#eaf2e9", "BM"),
]

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif">')
svg.append(f'<rect width="{W}" height="{H}" fill="white"/>')

# region bands + boundary lines + band labels
for x0, x1, col, lab in bands:
    x0c, x1c = px(x0), px(x1)
    svg.append(f'<rect x="{x0c:.2f}" y="{MT}" width="{(x1c-x0c):.2f}" '
               f'height="{PH}" fill="{col}"/>')
for xb in (-7.5, -5.0, 5.0, 7.5):
    svg.append(f'<line x1="{px(xb):.2f}" y1="{MT}" x2="{px(xb):.2f}" '
               f'y2="{MT+PH}" stroke="#bbbbbb" stroke-width="1" '
               f'stroke-dasharray="4,3"/>')
for x0, x1, col, lab in bands:
    xm = px((x0 + x1) / 2.0)
    if lab == "Weld (FZ)":
        svg.append(f'<text x="{xm:.1f}" y="{MT+18}" text-anchor="middle" '
                   f'font-size="14" font-weight="bold" fill="#555">{lab}</text>')
    else:
        svg.append(f'<text x="{xm:.1f}" y="{MT+18}" text-anchor="middle" '
                   f'font-size="12" font-weight="bold" fill="#777">{lab}</text>')

# grid + axis ticks
for yt in Y_TICKS:
    yc = py(yt)
    svg.append(f'<line x1="{ML}" y1="{yc:.2f}" x2="{ML+PW}" y2="{yc:.2f}" '
               f'stroke="#e3e3e3" stroke-width="1"/>')
    svg.append(f'<text x="{ML-10}" y="{yc+4:.2f}" text-anchor="end" '
               f'font-size="13" fill="#333">{yt}</text>')
for xt in X_TICKS:
    xc = px(xt)
    svg.append(f'<line x1="{xc:.2f}" y1="{MT+PH}" x2="{xc:.2f}" '
               f'y2="{MT+PH+6}" stroke="#333" stroke-width="1"/>')
    svg.append(f'<text x="{xc:.2f}" y="{MT+PH+24:.2f}" text-anchor="middle" '
               f'font-size="13" fill="#333">{xt}</text>')

# plot frame
svg.append(f'<rect x="{ML}" y="{MT}" width="{PW}" height="{PH}" fill="none" '
           f'stroke="#333" stroke-width="1.3"/>')

# data curves
svg.append(polyline(y_unch, "#1f5fd0", 1.6))   # uncharged - blue
svg.append(polyline(y_chg,  "#d02020", 1.6))   # charged   - red

# axis labels / title
svg.append(f'<text x="{ML+PW/2:.1f}" y="{H-22}" text-anchor="middle" '
           f'font-size="15" fill="#000">Distance from weld centreline (mm)</text>')
svg.append(f'<text x="22" y="{MT+PH/2:.1f}" text-anchor="middle" font-size="15" '
           f'fill="#000" transform="rotate(-90 22 {MT+PH/2:.1f})">'
           f'Vickers microhardness (HV0.5)</text>')
svg.append(f'<text x="{ML}" y="34" font-size="18" font-weight="bold" fill="#000">'
           f'API X70 SMAW weldment \u2013 microhardness traverse</text>')
svg.append(f'<text x="{ML}" y="54" font-size="13" fill="#555">'
           f'Effect of cathodic hydrogen charging (0.5 M H\u2082SO\u2084 + 5 g/L '
           f'thiourea, 50 mA/cm\u00b2, 10 h)</text>')

# legend (right margin)
lx, ly = ML + PW + 24, MT + 10
svg.append(f'<rect x="{lx}" y="{ly}" width="196" height="150" fill="white" '
           f'stroke="#ccc" stroke-width="1" rx="6"/>')
svg.append(f'<text x="{lx+12}" y="{ly+24}" font-size="13" font-weight="bold" '
           f'fill="#000">Legend</text>')
svg.append(f'<line x1="{lx+12}" y1="{ly+44}" x2="{lx+42}" y2="{ly+44}" '
           f'stroke="#1f5fd0" stroke-width="2.4"/>')
svg.append(f'<text x="{lx+50}" y="{ly+48}" font-size="12.5" fill="#000">'
           f'Without charging</text>')
svg.append(f'<line x1="{lx+12}" y1="{ly+66}" x2="{lx+42}" y2="{ly+66}" '
           f'stroke="#d02020" stroke-width="2.4"/>')
svg.append(f'<text x="{lx+50}" y="{ly+70}" font-size="12.5" fill="#000">'
           f'With H charging</text>')
svg.append(f'<text x="{lx+12}" y="{ly+96}" font-size="11.5" fill="#444">'
           f'Mean HV (unch \u2192 chg):</text>')
svg.append(f'<text x="{lx+12}" y="{ly+114}" font-size="11.5" fill="#444">'
           f'BM 214.6 \u2192 220</text>')
svg.append(f'<text x="{lx+12}" y="{ly+130}" font-size="11.5" fill="#444">'
           f'FZ 196.0 \u2192 209</text>')
svg.append(f'<text x="{lx+12}" y="{ly+146}" font-size="11.5" fill="#444">'
           f'HAZ 252.6 \u2192 275</text>')

svg.append('</svg>')

with open("hardness_profile.svg", "w") as f:
    f.write("\n".join(svg))

print("Wrote hardness_profile_data.csv ({} rows) and hardness_profile.svg"
      .format(len(xs)))
print("Region means (uncharged / charged HV):")
print("  Base metal : {:.1f} / {:.1f}".format(BM[0], BM[1]))
print("  Weld (FZ)  : {:.1f} / {:.1f}".format(FZ[0], FZ[1]))
print("  HAZ        : {:.1f} / {:.1f}".format(HAZ[0], HAZ[1]))
