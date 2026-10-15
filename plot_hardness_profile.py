#!/usr/bin/env python3
"""
Realistic Vickers microhardness traverse across API X70 SMAW weld joints
for three electrodes (E6018, E7018, E9018), grounded in published data.

Traverse: -8 mm -> +8 mm, 0.05 mm interval (321 points per curve).
Weld centreline at x = 0. Fusion line at |x| = 5 mm.

Literature-based reasoning (see chat for citations):
  * X70 base metal         ~ 210-225 HV  -> ~215 HV flat, low scatter
  * HAZ is NOT flat: a coarse-grain HAZ (CGHAZ) hardness PEAK forms just
    outside the fusion line (bainitic, fast cooling), followed by a softer
    fine-grain / inter-critical / sub-critical HAZ that returns to BM.
  * Because all three joints use the SAME base metal and SAME heat input,
    their BM + HAZ profiles nearly overlap. The curves fan apart only in
    the fusion zone, where the consumable sets the weld-metal hardness:
        E6018 (E60) weld ~ 210 HV  (under-matched, soft)
        E7018 (E70) weld ~ 232 HV
        E9018 (E90) weld ~ 258 HV
  * Multi-pass weld metal shows scatter (columnar vs reheated bands), so a
    low-frequency "wander" + white noise is added instead of uniform fuzz.

No third-party libraries: writes an SVG + CSV; a companion Java program
(HardnessPlot.java) renders the PNG from the CSV.
"""

import math
import random
import csv

X_MIN, X_MAX, STEP = -8.0, 8.0, 0.05
BM_LEVEL = 215.0
FZ_HALF, HAZ_HALF = 5.0, 7.0

# Mean-hardness control knots as a function of |x| (mm). Interpolated linearly.
# Each list is sorted by distance from centreline.
KNOTS = {
    "E6018": [  # E60 - soft, under-matched weld metal
        (0.0, 209), (1.5, 212), (2.5, 205), (3.5, 213), (4.5, 208), (4.9, 210),
        (5.1, 240), (5.25, 246), (5.6, 238), (6.0, 229), (6.4, 221),
        (6.8, 214), (7.1, 214), (7.4, 215), (8.0, 215),
    ],
    "E7018": [  # E70 - moderate weld-metal hardness
        (0.0, 231), (1.5, 234), (2.5, 227), (3.5, 235), (4.5, 230), (4.9, 232),
        (5.1, 250), (5.25, 256), (5.6, 246), (6.0, 236), (6.4, 227),
        (6.8, 219), (7.1, 216), (7.4, 215), (8.0, 215),
    ],
    "E9018": [  # E90 - alloyed, hardest weld metal; fine acicular ferrite
        (0.0, 257), (1.5, 260), (2.5, 253), (3.5, 261), (4.5, 256), (4.9, 258),
        (5.1, 266), (5.25, 270), (5.6, 258), (6.0, 244), (6.4, 232),
        (6.8, 222), (7.1, 217), (7.4, 215), (8.0, 215),
    ],
}
COLORS = {"E6018": "#d62728", "E7018": "#1f77b4", "E9018": "#2ca02c"}


def x_axis():
    n = int(round((X_MAX - X_MIN) / STEP))
    return [round(X_MIN + i * STEP, 2) for i in range(n + 1)]


def interp(knots, d):
    """Linear interpolation of mean hardness at distance d (mm) from centreline."""
    if d <= knots[0][0]:
        return knots[0][1]
    if d >= knots[-1][0]:
        return knots[-1][1]
    for i in range(len(knots) - 1):
        d0, h0 = knots[i]
        d1, h1 = knots[i + 1]
        if d0 <= d <= d1:
            t = (d - d0) / (d1 - d0)
            return h0 + t * (h1 - h0)
    return knots[-1][1]


def smooth(values, half_window):
    sigma = max(half_window / 2.0, 1e-6)
    w = [math.exp(-(k * k) / (2 * sigma * sigma))
         for k in range(-half_window, half_window + 1)]
    out = []
    n = len(values)
    for i in range(n):
        num = den = 0.0
        for off, ww in zip(range(-half_window, half_window + 1), w):
            j = min(max(i + off, 0), n - 1)
            num += values[j] * ww
            den += ww
        out.append(num / den)
    return out


def amplitude(d):
    """Measurement scatter amplitude by region (HV)."""
    if d >= HAZ_HALF:
        return 1.5          # base metal: calm
    elif d >= FZ_HALF:
        return 2.6          # HAZ: steep gradients, more scatter
    else:
        return 2.8          # multi-pass weld metal: columnar/reheated scatter


def build_profiles():
    xs = x_axis()
    profiles = {}
    for name in KNOTS:
        rng = random.Random((hash(name) & 0xFFFF) + 7)
        # correlated low-frequency wander (unique per electrode & side)
        raw = [rng.gauss(0, 1) for _ in xs]
        wander = smooth(raw, half_window=9)
        wstd = (sum(v * v for v in wander) / len(wander)) ** 0.5 or 1.0
        wander = [v / wstd for v in wander]       # unit std

        series = []
        for x, w in zip(xs, wander):
            d = abs(x)
            mean = interp(KNOTS[name], d)
            # gentle left/right asymmetry so the two HAZs are not identical
            if x < 0:
                mean += 0.04 * (mean - BM_LEVEL)
            amp = amplitude(d)
            val = mean + w * amp + rng.gauss(0, 0.8)
            series.append(round(val, 1))
        profiles[name] = series
    return xs, profiles


def write_csv(xs, profiles, path):
    with open(path, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["Position_mm", "E6018_HV", "E7018_HV", "E9018_HV", "Zone"])
        for i, x in enumerate(xs):
            d = abs(x)
            zone = ("BM" if d >= HAZ_HALF else
                    ("HAZ" if d >= FZ_HALF else "FZ"))
            wr.writerow([x, profiles["E6018"][i], profiles["E7018"][i],
                         profiles["E9018"][i], zone])
    print(f"wrote {path} ({len(xs)} rows)")


# ---------------- SVG (dependency-free) ----------------
W, H = 980, 600
ML, MR, MT, MB = 85, 220, 60, 72
PW, PH = W - ML - MR, H - MT - MB
Y_MIN, Y_MAX = 190.0, 290.0


def sx(x): return ML + (x - X_MIN) / (X_MAX - X_MIN) * PW
def sy(y): return MT + (Y_MAX - y) / (Y_MAX - Y_MIN) * PH


def write_svg(xs, profiles, path):
    e = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="Segoe UI, Arial, sans-serif">',
         f'<rect width="{W}" height="{H}" fill="white"/>']

    def band(x0, x1, c):
        a, b = sx(x0), sx(x1)
        e.append(f'<rect x="{a:.1f}" y="{MT}" width="{b-a:.1f}" height="{PH}" '
                 f'fill="{c}" opacity="0.16"/>')
    band(X_MIN, -HAZ_HALF, "#7f7f7f"); band(-HAZ_HALF, -FZ_HALF, "#ff7f0e")
    band(-FZ_HALF, FZ_HALF, "#1f77b4"); band(FZ_HALF, HAZ_HALF, "#ff7f0e")
    band(HAZ_HALF, X_MAX, "#7f7f7f")

    for xc, t in [(0, "Fusion Zone"), (-6, "HAZ"), (6, "HAZ"),
                  (-7.5, "BM"), (7.5, "BM")]:
        e.append(f'<text x="{sx(xc):.1f}" y="{MT+17}" text-anchor="middle" '
                 f'font-size="13" font-weight="bold" fill="#444">{t}</text>')

    e.append(f'<line x1="{sx(0):.1f}" y1="{MT}" x2="{sx(0):.1f}" y2="{MT+PH}" '
             f'stroke="#999" stroke-dasharray="4,4"/>')

    y = 190
    while y <= Y_MAX + .1:
        yp = sy(y)
        e.append(f'<line x1="{ML}" y1="{yp:.1f}" x2="{ML+PW}" y2="{yp:.1f}" '
                 f'stroke="#e3e3e3"/>')
        e.append(f'<text x="{ML-10}" y="{yp+4:.1f}" text-anchor="end" '
                 f'font-size="12">{y:g}</text>')
        y += 10
    xt = -8
    while xt <= 8.1:
        xp = sx(xt)
        e.append(f'<line x1="{xp:.1f}" y1="{MT}" x2="{xp:.1f}" y2="{MT+PH}" '
                 f'stroke="#eee"/>')
        e.append(f'<text x="{xp:.1f}" y="{MT+PH+22}" text-anchor="middle" '
                 f'font-size="12">{xt:g}</text>')
        xt += 1

    e.append(f'<line x1="{ML}" y1="{sy(BM_LEVEL):.1f}" x2="{ML+PW}" '
             f'y2="{sy(BM_LEVEL):.1f}" stroke="#555" stroke-dasharray="5,4" '
             f'opacity="0.7"/>')
    e.append(f'<rect x="{ML}" y="{MT}" width="{PW}" height="{PH}" fill="none" '
             f'stroke="#333" stroke-width="1.2"/>')

    e.append(f'<text x="{ML+PW/2:.1f}" y="{H-18}" text-anchor="middle" '
             f'font-size="14" font-weight="bold">Distance from Weld Centreline (mm)</text>')
    e.append(f'<text x="22" y="{MT+PH/2:.1f}" text-anchor="middle" font-size="14" '
             f'font-weight="bold" transform="rotate(-90 22 {MT+PH/2:.1f})">'
             f'Vickers Microhardness (HV0.1)</text>')
    e.append(f'<text x="{ML+PW/2:.1f}" y="30" text-anchor="middle" font-size="16" '
             f'font-weight="bold">Microhardness Traverse: API X70 SMAW Weld Joints</text>')

    for name, c in COLORS.items():
        pts = " ".join(f"{sx(x):.2f},{sy(v):.2f}"
                       for x, v in zip(xs, profiles[name]))
        e.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="1.6"/>')

    lx, ly = ML + PW + 24, MT + 24
    e.append(f'<text x="{lx}" y="{ly-8}" font-size="13" font-weight="bold">Weld metal (FZ)</text>')
    labels = {"E6018": "E6018  ~210 HV", "E7018": "E7018  ~232 HV",
              "E9018": "E9018  ~258 HV"}
    for i, (name, c) in enumerate(COLORS.items()):
        yy = ly + i * 26
        e.append(f'<line x1="{lx}" y1="{yy}" x2="{lx+26}" y2="{yy}" '
                 f'stroke="{c}" stroke-width="3"/>')
        e.append(f'<text x="{lx+32}" y="{yy+4}" font-size="12">{labels[name]}</text>')
    yy = ly + 3 * 26 + 10
    e.append(f'<line x1="{lx}" y1="{yy}" x2="{lx+26}" y2="{yy}" stroke="#555" '
             f'stroke-width="2" stroke-dasharray="4,3"/>')
    e.append(f'<text x="{lx+32}" y="{yy+4}" font-size="12">Base metal ~215 HV</text>')
    e.append(f'<text x="{lx}" y="{yy+30}" font-size="11" fill="#555">CGHAZ peak</text>')
    e.append(f'<text x="{lx}" y="{yy+45}" font-size="11" fill="#555">just outside</text>')
    e.append(f'<text x="{lx}" y="{yy+60}" font-size="11" fill="#555">fusion line</text>')

    e.append('</svg>')
    with open(path, "w") as f:
        f.write("\n".join(e))
    print(f"wrote {path}")


if __name__ == "__main__":
    xs, profiles = build_profiles()
    write_csv(xs, profiles, "hardness_profile_data.csv")
    write_svg(xs, profiles, "hardness_profile.svg")
    print(f"points per curve: {len(xs)}  (x {X_MIN}..{X_MAX} mm, step {STEP} mm)")
