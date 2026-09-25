#!/usr/bin/env python3
"""
Vickers microhardness (HV) TRAVERSE across the weld, at room temperature.

A continuous hardness profile is generated from x = -8 mm to x = +8 mm at a
0.1 mm interval (161 points per weld), reported in Vickers hardness (VHN / HV0.5).
The fusion-line interfaces are located at x = -5 mm and x = +5 mm.

Weld configurations (all deposited with an E6018 low-hydrogen filler):
    1. X70-X70    : similar weld (API 5L X70 pipeline steel)
    2. S355-S355  : similar weld (EN 10025 S355 structural steel)
    3. X70-S355   : dissimilar weld (asymmetric: X70 on the left, S355 on the right)

Spatial layout along x (fusion lines at +/-5 mm):
    Base Metal  : 5 <= |x| <= 8 mm
    HAZ         : a 1.2 mm band just INSIDE each fusion line (3.8 <= |x| < 5 mm)
    Fusion Zone : the central weld metal, |x| < 3.8 mm

At every 0.1 mm point n = 3 replicate traverses are simulated; the mean and
sample standard deviation (n-1) are reported. Values are representative,
literature-consistent HV levels for these steels welded with a 60-ksi-class
E6018 electrode (they are synthetic, not measured lab results). The zone
plateau/peak targets match the repo's room-temperature averages.

Outputs (all pure Python stdlib, no numpy / matplotlib / pandas):
    weld_hardness_traverse.csv         full 3 x 161 profile with replicates
    weld_hardness_traverse.md          condensed readable summary (every 0.5 mm)
    hardness_traverse_X70-X70.svg      profile plot per weld
    hardness_traverse_S355-S355.svg
    hardness_traverse_X70-S355.svg
    hardness_traverse_comparison.svg   combined mean-profile comparison
"""

import csv
import math
import random
import statistics
from pathlib import Path

OUT_DIR = Path(__file__).parent
FILLER = "E6018"

SEED = 20240517          # fixed seed for reproducibility
random.seed(SEED)

X_MIN = -8.0
X_MAX = 8.0
X_STEP = 0.1
N_POINTS = int(round((X_MAX - X_MIN) / X_STEP)) + 1   # 161 inclusive
N_REPLICATES = 3

FUSION_LEFT = -5.0
FUSION_RIGHT = 5.0
HAZ_WIDTH = 1.2          # mm band inside each fusion line
FZ_HALF = FUSION_RIGHT - HAZ_WIDTH   # 3.8 mm -> fusion-zone half width

# ---------------------------------------------------------------------------
# Zone target hardness levels (mean HV), consistent with the room-temp table.
# Each weld side is described by base plateau, HAZ peak and weld-metal level.
# ---------------------------------------------------------------------------
PROFILES = {
    "X70-X70": {
        "left_base": 215.0,  "left_haz": 252.0,
        "weld": 194.0,
        "right_base": 215.0, "right_haz": 252.0,
        "scatter": 5.5,
    },
    "S355-S355": {
        "left_base": 165.0,  "left_haz": 206.0,
        "weld": 186.0,
        "right_base": 165.0, "right_haz": 206.0,
        "scatter": 5.5,
    },
    # dissimilar: X70 on the left, S355 on the right -> asymmetric profile
    "X70-S355": {
        "left_base": 215.0,  "left_haz": 249.0,
        "weld": 192.0,
        "right_base": 164.0, "right_haz": 202.0,
        "scatter": 5.5,
    },
}


def zone_label(x, weld):
    """Return the metallurgical zone name for a given position x (mm)."""
    ax = abs(x)
    if ax >= FUSION_RIGHT:                       # base metal (outside fusion line)
        side = "X70" if x < 0 else "S355"
        if weld == "X70-X70":
            return "Base Metal - X70"
        if weld == "S355-S355":
            return "Base Metal - S355"
        return f"Base Metal - {side} side"
    if ax >= FZ_HALF:                            # HAZ band inside the fusion line
        side = "X70" if x < 0 else "S355"
        if weld == "X70-X70":
            return "HAZ - X70"
        if weld == "S355-S355":
            return "HAZ - S355"
        return f"HAZ - {side} side"
    return "Fusion Zone (E6018)"                 # central weld metal


def smoothstep(a, b, t):
    """Smooth Hermite interpolation from a to b as t goes 0 -> 1."""
    t = max(0.0, min(1.0, t))
    s = t * t * (3.0 - 2.0 * t)
    return a + (b - a) * s


def side_profile(x, base, haz, weld):
    """
    Mean hardness on ONE side of the weld centerline for the base-metal and
    HAZ regions (used only where the absolute distance ax >= FZ_HALF; the
    central fusion zone is handled separately in `mean_hardness`).

    Regions (using absolute distance ax from centerline):
      ax >= 5.0            : base-metal plateau (`base`), gentle rise toward FL
      4.6 <= ax < 5.0      : rising limb of the HAZ up to the peak (`haz`)
      3.8 <= ax < 4.6      : falling limb of the HAZ down toward weld metal
    Transitions are smoothed so there are no discontinuities.
    """
    ax = abs(x)
    # Peak of the coarse-grained HAZ sits just inside the fusion line.
    haz_peak_pos = FUSION_RIGHT - 0.4      # ~4.6 mm from centerline

    if ax >= FUSION_RIGHT:
        # Base metal, with a gentle rise toward the fusion line (fine-grained
        # HAZ tail): from base plateau at 8 mm up toward the peak start at FL.
        t = (X_MAX - ax) / (X_MAX - FUSION_RIGHT)   # 0 at 8 mm, 1 at 5 mm
        return smoothstep(base, base + 0.15 * (haz - base), t)
    if ax >= haz_peak_pos:
        # Rising limb of the HAZ: from ~fusion-line level up to the HAZ peak.
        start = base + 0.15 * (haz - base)
        t = (FUSION_RIGHT - ax) / (FUSION_RIGHT - haz_peak_pos)
        return smoothstep(start, haz, t)
    # Falling limb of the HAZ: from HAZ peak down toward the weld metal.
    t = (haz_peak_pos - ax) / (haz_peak_pos - FZ_HALF)
    return smoothstep(haz, weld, t)


def mean_hardness(x, prof):
    """Full mean hardness at position x for a given weld profile (asymmetric aware)."""
    ax = abs(x)
    if ax >= FZ_HALF:
        # Base metal + HAZ, taken from the appropriate side (asymmetric aware).
        if x < 0:
            return side_profile(x, prof["left_base"], prof["left_haz"],
                                prof["weld"])
        return side_profile(x, prof["right_base"], prof["right_haz"],
                            prof["weld"])
    # Central fusion zone / weld metal: common plateau with a mild centerline
    # softening so the two HAZ limbs meet smoothly at the weld-metal level.
    weld = prof["weld"]
    dip = 3.0 * (1.0 - (ax / FZ_HALF))       # small softening toward centerline
    val = weld - dip
    # For the dissimilar weld, tilt the weld metal slightly toward each side.
    if prof["left_base"] != prof["right_base"]:
        val += 2.0 * (x / FZ_HALF)           # +/- a couple HV across the FZ
    return val


def build_traverse():
    """Return dict weld -> list of point dicts (x, replicates, mean, sd, zone)."""
    result = {}
    for weld, prof in PROFILES.items():
        points = []
        for i in range(N_POINTS):
            x = round(X_MIN + i * X_STEP, 1)
            mu = mean_hardness(x, prof)
            reps = [round(mu + random.gauss(0.0, prof["scatter"]), 1)
                    for _ in range(N_REPLICATES)]
            mean = statistics.mean(reps)
            sd = statistics.stdev(reps)
            points.append({
                "x": x,
                "reps": reps,
                "mean": round(mean, 1),
                "sd": round(sd, 1),
                "zone": zone_label(x, weld),
            })
        result[weld] = points
    return result


# ---------------------------------------------------------------------------
# CSV / Markdown writers
# ---------------------------------------------------------------------------
def write_csv(traverse, path):
    fields = ["Weld_Type", "Filler", "x_mm", "R1_HV", "R2_HV", "R3_HV",
              "Mean_HV", "StdDev_HV", "Zone"]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for weld, points in traverse.items():
            for p in points:
                w.writerow({
                    "Weld_Type": weld,
                    "Filler": FILLER,
                    "x_mm": p["x"],
                    "R1_HV": p["reps"][0],
                    "R2_HV": p["reps"][1],
                    "R3_HV": p["reps"][2],
                    "Mean_HV": p["mean"],
                    "StdDev_HV": p["sd"],
                    "Zone": p["zone"],
                })


def zone_stats(points, zone_key):
    vals = [p["mean"] for p in points if zone_key in p["zone"]]
    if not vals:
        return None
    return (round(statistics.mean(vals), 1), min(vals), max(vals))


def write_markdown(traverse, path):
    lines = [
        "# Vickers Microhardness Traverse Across the Weld (VHN / HV0.5)\n",
        f"**Filler wire:** {FILLER}  |  **Load:** HV0.5  |  "
        "**Temperature:** ~23 C (room)  |  ISO 6507-1\n",
        "**Traverse:** x = -8.0 mm to +8.0 mm at 0.1 mm interval "
        f"({N_POINTS} points per weld)  |  **Replicates:** n = {N_REPLICATES} "
        "per point (Mean +/- sample StdDev).\n",
        "**Fusion-line interfaces:** x = -5 mm and x = +5 mm.\n",
        "> These are representative, literature-consistent (synthetic) values, "
        "not measured laboratory results.\n",
        "## Zone boundary definitions\n",
        f"| Zone | Position (distance from centerline, mm) |",
        "|---|---|",
        f"| Fusion Zone / Weld Metal (E6018) | |x| < {FZ_HALF:.1f} |",
        f"| Heat-Affected Zone (HAZ) | {FZ_HALF:.1f} <= |x| < {FUSION_RIGHT:.1f} "
        "(1.2 mm band inside each fusion line) |",
        f"| Base Metal | {FUSION_RIGHT:.1f} <= |x| <= 8.0 |",
        "",
        "## Peak / plateau summary per weld\n",
        "| Weld Type | Left Base (HV) | Left HAZ peak (HV) | "
        "Weld Metal (HV) | Right HAZ peak (HV) | Right Base (HV) |",
        "|---|---|---|---|---|---|",
    ]
    for weld, prof in PROFILES.items():
        lines.append(
            f"| {weld} | {prof['left_base']:.0f} | {prof['left_haz']:.0f} | "
            f"{prof['weld']:.0f} | {prof['right_haz']:.0f} | {prof['right_base']:.0f} |"
        )
    lines.append("")
    lines.append("The X70-S355 dissimilar weld is **asymmetric**: the higher X70 "
                 "base/HAZ appears on the left (x < 0) and the softer S355 "
                 "base/HAZ on the right (x > 0).\n")

    # Condensed table: every 0.5 mm for each weld.
    for weld, points in traverse.items():
        lines.append(f"## Condensed profile: {weld} (every 0.5 mm)\n")
        lines.append("| x (mm) | Mean (HV) | StdDev (HV) | Zone |")
        lines.append("|---|---|---|---|")
        for p in points:
            if abs((p["x"] * 10) % 5) < 1e-6:   # x is a multiple of 0.5 mm
                lines.append(
                    f"| {p['x']:.1f} | {p['mean']} | {p['sd']} | {p['zone']} |"
                )
        lines.append("")
        lines.append(f"_Full {N_POINTS}-point profile at 0.1 mm resolution is in "
                     "`weld_hardness_traverse.csv`._\n")

    Path(path).write_text("\n".join(lines))


# ---------------------------------------------------------------------------
# SVG plotting (pure text, no libraries)
# ---------------------------------------------------------------------------
SVG_W = 900
SVG_H = 540
M_LEFT = 80
M_RIGHT = 210      # room for the legend
M_TOP = 50
M_BOTTOM = 70
PLOT_W = SVG_W - M_LEFT - M_RIGHT
PLOT_H = SVG_H - M_TOP - M_BOTTOM

Y_MIN = 140.0
Y_MAX = 280.0

COLORS = {
    "X70-X70": "#c0392b",
    "S355-S355": "#2471a3",
    "X70-S355": "#1e8449",
}
BAND_COLORS = {
    "X70-X70": "#c0392b",
    "S355-S355": "#2471a3",
    "X70-S355": "#1e8449",
}


def sx(x):
    return M_LEFT + (x - X_MIN) / (X_MAX - X_MIN) * PLOT_W


def sy(y):
    return M_TOP + (Y_MAX - y) / (Y_MAX - Y_MIN) * PLOT_H


def _axes_and_grid(parts, title, subtitle):
    parts.append(f'<rect x="0" y="0" width="{SVG_W}" height="{SVG_H}" '
                 'fill="#ffffff"/>')
    parts.append(f'<text x="{M_LEFT}" y="26" font-family="Arial" '
                 f'font-size="18" font-weight="bold" fill="#111">{title}</text>')
    parts.append(f'<text x="{M_LEFT}" y="44" font-family="Arial" '
                 f'font-size="12" fill="#555">{subtitle}</text>')
    # plot border
    parts.append(f'<rect x="{M_LEFT}" y="{M_TOP}" width="{PLOT_W}" '
                 f'height="{PLOT_H}" fill="#fbfbfb" stroke="#888" '
                 'stroke-width="1"/>')
    # Y gridlines / ticks every 20 HV
    y = Y_MIN
    while y <= Y_MAX + 1e-6:
        yy = sy(y)
        parts.append(f'<line x1="{M_LEFT}" y1="{yy:.1f}" x2="{M_LEFT + PLOT_W}" '
                     f'y2="{yy:.1f}" stroke="#e2e2e2" stroke-width="1"/>')
        parts.append(f'<text x="{M_LEFT - 10}" y="{yy + 4:.1f}" '
                     'font-family="Arial" font-size="11" fill="#333" '
                     f'text-anchor="end">{int(y)}</text>')
        y += 20
    # X gridlines / ticks every 2 mm
    x = X_MIN
    while x <= X_MAX + 1e-6:
        xx = sx(x)
        parts.append(f'<line x1="{xx:.1f}" y1="{M_TOP}" x2="{xx:.1f}" '
                     f'y2="{M_TOP + PLOT_H}" stroke="#e2e2e2" stroke-width="1"/>')
        parts.append(f'<text x="{xx:.1f}" y="{M_TOP + PLOT_H + 18:.1f}" '
                     'font-family="Arial" font-size="11" fill="#333" '
                     f'text-anchor="middle">{int(x)}</text>')
        x += 2
    # Axis labels
    parts.append(f'<text x="{M_LEFT + PLOT_W / 2:.1f}" '
                 f'y="{M_TOP + PLOT_H + 46:.1f}" font-family="Arial" '
                 'font-size="13" fill="#111" text-anchor="middle">'
                 'Distance from weld centerline, x (mm)</text>')
    parts.append(f'<text x="22" y="{M_TOP + PLOT_H / 2:.1f}" '
                 'font-family="Arial" font-size="13" fill="#111" '
                 'text-anchor="middle" '
                 f'transform="rotate(-90 22 {M_TOP + PLOT_H / 2:.1f})">'
                 'Vickers hardness (HV0.5 / VHN)</text>')


def _fusion_lines(parts):
    for xf, lbl in ((FUSION_LEFT, "FL -5 mm"), (FUSION_RIGHT, "FL +5 mm")):
        xx = sx(xf)
        parts.append(f'<line x1="{xx:.1f}" y1="{M_TOP}" x2="{xx:.1f}" '
                     f'y2="{M_TOP + PLOT_H}" stroke="#333" stroke-width="1.4" '
                     'stroke-dasharray="6 4"/>')
        parts.append(f'<text x="{xx + 3:.1f}" y="{M_TOP + 14:.1f}" '
                     'font-family="Arial" font-size="10" fill="#333">'
                     f'{lbl}</text>')


def _zone_annotations(parts):
    """Light shaded backgrounds + labels for BM / HAZ / FZ."""
    bands = [
        (X_MIN, FUSION_LEFT, "#f4ecec", "Base Metal"),
        (FUSION_LEFT, -FZ_HALF, "#eef4fb", "HAZ"),
        (-FZ_HALF, FZ_HALF, "#eef8ef", "Fusion Zone"),
        (FZ_HALF, FUSION_RIGHT, "#eef4fb", "HAZ"),
        (FUSION_RIGHT, X_MAX, "#f4ecec", "Base Metal"),
    ]
    for x0, x1, col, lbl in bands:
        xx0 = sx(x0)
        w = sx(x1) - xx0
        parts.append(f'<rect x="{xx0:.1f}" y="{M_TOP}" width="{w:.1f}" '
                     f'height="{PLOT_H}" fill="{col}" opacity="0.6"/>')
        parts.append(f'<text x="{xx0 + w / 2:.1f}" '
                     f'y="{M_TOP + PLOT_H - 8:.1f}" font-family="Arial" '
                     'font-size="10" fill="#777" text-anchor="middle">'
                     f'{lbl}</text>')


def _polyline(points_xy, color, width=2.0):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points_xy)
    return (f'<polyline points="{pts}" fill="none" stroke="{color}" '
            f'stroke-width="{width}"/>')


def _error_band(points, color):
    """Return an SVG path polygon for mean +/- 1 SD (semi-transparent)."""
    upper = [(sx(p["x"]), sy(p["mean"] + p["sd"])) for p in points]
    lower = [(sx(p["x"]), sy(p["mean"] - p["sd"])) for p in reversed(points)]
    ring = upper + lower
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in ring)
    return (f'<polygon points="{pts}" fill="{color}" fill-opacity="0.18" '
            'stroke="none"/>')


def write_weld_svg(weld, points, path):
    parts = ['<?xml version="1.0" encoding="UTF-8"?>']
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" '
                 f'height="{SVG_H}" viewBox="0 0 {SVG_W} {SVG_H}">')
    title = f"Microhardness traverse: {weld} weld (E6018 filler)"
    sub = ("HV0.5 vs distance, 0.1 mm interval, n=3 replicates, "
           "band = mean +/- 1 SD")
    _axes_and_grid(parts, title, sub)
    _zone_annotations(parts)
    _fusion_lines(parts)

    color = COLORS[weld]
    parts.append(_error_band(points, BAND_COLORS[weld]))
    mean_xy = [(sx(p["x"]), sy(p["mean"])) for p in points]
    parts.append(_polyline(mean_xy, color, 2.0))

    # Legend
    lx = M_LEFT + PLOT_W + 20
    ly = M_TOP + 10
    parts.append(f'<rect x="{lx}" y="{ly}" width="180" height="120" '
                 'fill="#ffffff" stroke="#ccc" stroke-width="1"/>')
    parts.append(f'<text x="{lx + 10}" y="{ly + 20}" font-family="Arial" '
                 'font-size="12" font-weight="bold" fill="#111">Legend</text>')
    parts.append(f'<line x1="{lx + 10}" y1="{ly + 38}" x2="{lx + 40}" '
                 f'y2="{ly + 38}" stroke="{color}" stroke-width="2.5"/>')
    parts.append(f'<text x="{lx + 46}" y="{ly + 42}" font-family="Arial" '
                 'font-size="11" fill="#333">Mean HV</text>')
    parts.append(f'<rect x="{lx + 10}" y="{ly + 50}" width="30" height="12" '
                 f'fill="{color}" fill-opacity="0.18"/>')
    parts.append(f'<text x="{lx + 46}" y="{ly + 60}" font-family="Arial" '
                 'font-size="11" fill="#333">+/- 1 SD band</text>')
    parts.append(f'<line x1="{lx + 10}" y1="{ly + 76}" x2="{lx + 40}" '
                 f'y2="{ly + 76}" stroke="#333" stroke-width="1.4" '
                 'stroke-dasharray="6 4"/>')
    parts.append(f'<text x="{lx + 46}" y="{ly + 80}" font-family="Arial" '
                 'font-size="11" fill="#333">Fusion line</text>')
    parts.append(f'<text x="{lx + 10}" y="{ly + 102}" font-family="Arial" '
                 'font-size="10" fill="#777">Zones shaded:</text>')
    parts.append(f'<text x="{lx + 10}" y="{ly + 116}" font-family="Arial" '
                 'font-size="10" fill="#777">BM / HAZ / FZ</text>')

    parts.append('</svg>')
    Path(path).write_text("\n".join(parts))


def write_comparison_svg(traverse, path):
    parts = ['<?xml version="1.0" encoding="UTF-8"?>']
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" '
                 f'height="{SVG_H}" viewBox="0 0 {SVG_W} {SVG_H}">')
    _axes_and_grid(parts,
                   "Microhardness traverse comparison (E6018 filler)",
                   "Mean HV0.5 vs distance for the three welds; "
                   "band = mean +/- 1 SD")
    _zone_annotations(parts)
    _fusion_lines(parts)

    ly = M_TOP + 10
    lx = M_LEFT + PLOT_W + 20
    parts.append(f'<rect x="{lx}" y="{ly}" width="180" height="150" '
                 'fill="#ffffff" stroke="#ccc" stroke-width="1"/>')
    parts.append(f'<text x="{lx + 10}" y="{ly + 20}" font-family="Arial" '
                 'font-size="12" font-weight="bold" fill="#111">Weld type</text>')

    row = ly + 40
    for weld, points in traverse.items():
        color = COLORS[weld]
        parts.append(_error_band(points, BAND_COLORS[weld]))
        mean_xy = [(sx(p["x"]), sy(p["mean"])) for p in points]
        parts.append(_polyline(mean_xy, color, 2.0))
        parts.append(f'<line x1="{lx + 10}" y1="{row}" x2="{lx + 40}" '
                     f'y2="{row}" stroke="{color}" stroke-width="2.5"/>')
        parts.append(f'<text x="{lx + 46}" y="{row + 4}" font-family="Arial" '
                     f'font-size="11" fill="#333">{weld}</text>')
        row += 24

    parts.append(f'<line x1="{lx + 10}" y1="{row + 6}" x2="{lx + 40}" '
                 f'y2="{row + 6}" stroke="#333" stroke-width="1.4" '
                 'stroke-dasharray="6 4"/>')
    parts.append(f'<text x="{lx + 46}" y="{row + 10}" font-family="Arial" '
                 'font-size="11" fill="#333">Fusion line</text>')

    parts.append('</svg>')
    Path(path).write_text("\n".join(parts))


def print_summary(traverse):
    print(f"Traverse: {X_MIN} to {X_MAX} mm @ {X_STEP} mm = {N_POINTS} points/weld "
          f"({N_REPLICATES} replicates each)")
    print(f"Fusion lines at x = {FUSION_LEFT} and {FUSION_RIGHT} mm; "
          f"HAZ band width {HAZ_WIDTH} mm; fusion-zone half-width {FZ_HALF} mm\n")
    header = f"{'Weld':<11}{'Zone':<26}{'Mean HV':>9}{'Min':>7}{'Max':>7}"
    print(header)
    print("-" * len(header))
    for weld, points in traverse.items():
        for key in ("Base Metal", "HAZ", "Fusion Zone"):
            st = zone_stats(points, key)
            if st:
                print(f"{weld:<11}{key:<26}{st[0]:>9}{st[1]:>7}{st[2]:>7}")
        print("-" * len(header))


if __name__ == "__main__":
    traverse = build_traverse()

    write_csv(traverse, OUT_DIR / "weld_hardness_traverse.csv")
    write_markdown(traverse, OUT_DIR / "weld_hardness_traverse.md")

    for weld, points in traverse.items():
        write_weld_svg(weld, points, OUT_DIR / f"hardness_traverse_{weld}.svg")
    write_comparison_svg(traverse, OUT_DIR / "hardness_traverse_comparison.svg")

    print_summary(traverse)
    print("\nWrote:")
    print("  weld_hardness_traverse.csv")
    print("  weld_hardness_traverse.md")
    print("  hardness_traverse_X70-X70.svg")
    print("  hardness_traverse_S355-S355.svg")
    print("  hardness_traverse_X70-S355.svg")
    print("  hardness_traverse_comparison.svg")
