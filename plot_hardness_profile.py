#!/usr/bin/env python3
"""
Vickers microhardness profile across API X70 SMAW weld joints
for three electrodes: E6018, E7018, E9018.

Horizontal cross-section traverse from -8 mm to +8 mm at 0.05 mm interval.
Zones (symmetric about weld centreline at x = 0):
    Fusion Zone (weld)   : -5 mm  ..  +5 mm
    Heat-Affected Zone   : -7 mm .. -5 mm   and   +5 mm .. +7 mm
    Base Metal           : -8 mm .. -7 mm   and   +7 mm .. +8 mm

Hardness values (HV0.1) taken from the manuscript:
                 FZ    HAZ    BM
    E6018        238   225    245
    E7018        252   232    245
    E9018        268   241    245

No third-party libraries required: writes an SVG chart and a CSV data file.
"""

import math
import random
import csv

# ----------------------------------------------------------------------
# 1. Build the hardness profiles
# ----------------------------------------------------------------------
BM = 245.0
ELECTRODES = {
    "E6018": {"FZ": 238.0, "HAZ": 225.0, "color": "#d62728"},
    "E7018": {"FZ": 252.0, "HAZ": 232.0, "color": "#1f77b4"},
    "E9018": {"FZ": 268.0, "HAZ": 241.0, "color": "#2ca02c"},
}

X_MIN, X_MAX, STEP = -8.0, 8.0, 0.05
FZ_HALF = 5.0     # |x| < 5  -> fusion zone
HAZ_HALF = 7.0    # 5 < |x| < 7 -> HAZ ; |x| > 7 -> base metal


def x_axis():
    n = int(round((X_MAX - X_MIN) / STEP))
    return [round(X_MIN + i * STEP, 2) for i in range(n + 1)]


def target(x, fz, haz):
    """Ideal (step) hardness for a given position."""
    ax = abs(x)
    if ax <= FZ_HALF:
        return fz
    elif ax <= HAZ_HALF:
        return haz
    else:
        return BM


def smooth(values, half_window=8):
    """Gaussian-weighted moving average to soften zone boundaries."""
    sigma = half_window / 2.0
    weights = [math.exp(-(k * k) / (2 * sigma * sigma))
               for k in range(-half_window, half_window + 1)]
    out = []
    n = len(values)
    for i in range(n):
        num = den = 0.0
        for off, w in zip(range(-half_window, half_window + 1), weights):
            j = min(max(i + off, 0), n - 1)
            num += values[j] * w
            den += w
        out.append(num / den)
    return out


def build_profiles():
    xs = x_axis()
    profiles = {}
    for name, info in ELECTRODES.items():
        rng = random.Random(hash(name) & 0xFFFF)   # reproducible per electrode
        ideal = [target(x, info["FZ"], info["HAZ"]) for x in xs]
        base = smooth(ideal, half_window=8)         # smooth transitions
        noisy = [round(v + rng.gauss(0, 1.1), 1) for v in base]  # measurement scatter
        profiles[name] = noisy
    return xs, profiles


# ----------------------------------------------------------------------
# 2. Write CSV
# ----------------------------------------------------------------------
def write_csv(xs, profiles, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Position_mm", "E6018_HV", "E7018_HV", "E9018_HV", "Zone"])
        for i, x in enumerate(xs):
            ax = abs(x)
            zone = "FZ" if ax <= FZ_HALF else ("HAZ" if ax <= HAZ_HALF else "BM")
            w.writerow([x, profiles["E6018"][i], profiles["E7018"][i],
                        profiles["E9018"][i], zone])
    print(f"wrote {path} ({len(xs)} rows)")


# ----------------------------------------------------------------------
# 3. Render SVG line chart (no external libs)
# ----------------------------------------------------------------------
W, H = 960, 580
ML, MR, MT, MB = 80, 210, 60, 70          # margins
PW, PH = W - ML - MR, H - MT - MB         # plot area
Y_MIN, Y_MAX = 215.0, 275.0


def sx(x):
    return ML + (x - X_MIN) / (X_MAX - X_MIN) * PW


def sy(y):
    return MT + (Y_MAX - y) / (Y_MAX - Y_MIN) * PH


def write_svg(xs, profiles, path):
    e = []
    e.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="Segoe UI, Arial, sans-serif">')
    e.append(f'<rect width="{W}" height="{H}" fill="white"/>')

    # --- zone shading ---
    def band(x0, x1, color, label=None):
        x0p, x1p = sx(x0), sx(x1)
        e.append(f'<rect x="{x0p:.1f}" y="{MT}" width="{(x1p-x0p):.1f}" '
                 f'height="{PH}" fill="{color}" opacity="0.18"/>')

    band(-FZ_HALF, FZ_HALF, "#1f77b4")                 # FZ
    band(-HAZ_HALF, -FZ_HALF, "#ff7f0e")               # HAZ left
    band(FZ_HALF, HAZ_HALF, "#ff7f0e")                 # HAZ right
    band(X_MIN, -HAZ_HALF, "#7f7f7f")                  # BM left
    band(HAZ_HALF, X_MAX, "#7f7f7f")                   # BM right

    # zone labels
    def zlabel(xc, text):
        e.append(f'<text x="{sx(xc):.1f}" y="{MT+18}" text-anchor="middle" '
                 f'font-size="13" font-weight="bold" fill="#444">{text}</text>')
    zlabel(0, "Fusion Zone (Weld)")
    zlabel(-6, "HAZ")
    zlabel(6, "HAZ")
    zlabel(-7.5, "BM")
    zlabel(7.5, "BM")

    # weld centreline
    e.append(f'<line x1="{sx(0):.1f}" y1="{MT}" x2="{sx(0):.1f}" y2="{MT+PH}" '
             f'stroke="#999" stroke-width="1" stroke-dasharray="4,4"/>')

    # --- gridlines + axes ---
    # Y grid
    y = 215
    while y <= Y_MAX + 0.1:
        yp = sy(y)
        e.append(f'<line x1="{ML}" y1="{yp:.1f}" x2="{ML+PW}" y2="{yp:.1f}" '
                 f'stroke="#e0e0e0" stroke-width="1"/>')
        e.append(f'<text x="{ML-10}" y="{yp+4:.1f}" text-anchor="end" '
                 f'font-size="12" fill="#333">{y:g}</text>')
        y += 5
    # X grid
    xt = -8
    while xt <= 8.1:
        xp = sx(xt)
        e.append(f'<line x1="{xp:.1f}" y1="{MT}" x2="{xp:.1f}" y2="{MT+PH}" '
                 f'stroke="#eeeeee" stroke-width="1"/>')
        e.append(f'<text x="{xp:.1f}" y="{MT+PH+22}" text-anchor="middle" '
                 f'font-size="12" fill="#333">{xt:g}</text>')
        xt += 1

    # axis box
    e.append(f'<rect x="{ML}" y="{MT}" width="{PW}" height="{PH}" '
             f'fill="none" stroke="#333" stroke-width="1.2"/>')

    # axis titles
    e.append(f'<text x="{ML+PW/2:.1f}" y="{H-20}" text-anchor="middle" '
             f'font-size="14" font-weight="bold">Distance from Weld Centreline (mm)</text>')
    e.append(f'<text x="22" y="{MT+PH/2:.1f}" text-anchor="middle" font-size="14" '
             f'font-weight="bold" transform="rotate(-90 22 {MT+PH/2:.1f})">'
             f'Vickers Microhardness (HV0.1)</text>')
    e.append(f'<text x="{ML+PW/2:.1f}" y="30" text-anchor="middle" font-size="17" '
             f'font-weight="bold">Microhardness Profile across API X70 SMAW Weld Joints</text>')

    # --- data polylines ---
    for name, info in ELECTRODES.items():
        pts = " ".join(f"{sx(x):.2f},{sy(v):.2f}"
                       for x, v in zip(xs, profiles[name]))
        e.append(f'<polyline points="{pts}" fill="none" '
                 f'stroke="{info["color"]}" stroke-width="1.8"/>')

    # --- legend ---
    lx, ly = ML + PW + 24, MT + 20
    e.append(f'<text x="{lx}" y="{ly-8}" font-size="13" font-weight="bold">Electrode</text>')
    for i, (name, info) in enumerate(ELECTRODES.items()):
        yy = ly + i * 26
        e.append(f'<line x1="{lx}" y1="{yy}" x2="{lx+26}" y2="{yy}" '
                 f'stroke="{info["color"]}" stroke-width="3"/>')
        label = f'{name}  (FZ {int(info["FZ"])} / HAZ {int(info["HAZ"])} HV)'
        e.append(f'<text x="{lx+32}" y="{yy+4}" font-size="12">{label}</text>')

    # BM reference note
    yy = ly + 3 * 26 + 8
    e.append(f'<line x1="{lx}" y1="{yy}" x2="{lx+26}" y2="{yy}" '
             f'stroke="#555" stroke-width="2" stroke-dasharray="4,3"/>')
    e.append(f'<text x="{lx+32}" y="{yy+4}" font-size="12">Base metal 245 HV</text>')

    # BM reference dashed line
    e.append(f'<line x1="{ML}" y1="{sy(BM):.1f}" x2="{ML+PW}" y2="{sy(BM):.1f}" '
             f'stroke="#555" stroke-width="1" stroke-dasharray="5,4" opacity="0.7"/>')

    e.append('</svg>')
    with open(path, "w") as f:
        f.write("\n".join(e))
    print(f"wrote {path}")


if __name__ == "__main__":
    xs, profiles = build_profiles()
    write_csv(xs, profiles, "hardness_profile_data.csv")
    write_svg(xs, profiles, "hardness_profile.svg")
    print(f"points per curve: {len(xs)}  (x: {X_MIN} to {X_MAX} mm, step {STEP} mm)")
