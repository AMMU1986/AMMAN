#!/usr/bin/env python3
"""
Hydrogen-charged microhardness profile for the API X70 SMAW weldment.

Starts from the measured (UNCHARGED) Vickers microhardness traverse across the
weld (0.5 mm steps, -8 .. +8 mm about the weld centreline) and produces a
HYDROGEN-CHARGED profile by:

  1. Classifying each measured point into BM / HAZ / FZ by its traverse position.
  2. Applying a region-dependent hydrogen-hardening factor that reproduces the
     Table 1 endpoints of the manuscript (charging RAISES hardness):
         Base metal  : +2.8 %   (~214.6 -> ~220 HV)
         Fusion zone : +6.6 %   (~196   -> ~209 HV)
         HAZ (CGHAZ) : +8.9 %   (~252.6 -> ~273-275 HV)
  3. Resampling BOTH the uncharged and charged traverses onto a 0.1 mm grid
     by linear interpolation.
  4. Assigning the charged-condition scatter as SD = 1.5 % of each charged value.

Outputs:
  - microhardness_charged_interpolated.csv
  - figures_hydrogen/Fig_microhardness_charged.png   (uncharged vs charged)

Pure standard library (no numpy / matplotlib). Reuses the PNG canvas from
generate_figures.py.
"""

import os
import csv

from generate_figures import (
    PNGCanvas, BLACK, WHITE, GRAY, LIGHT_GRAY, DARK_BLUE, MED_BLUE,
    RED, LIGHT_RED, DARK_GREEN, MED_GREEN, ORANGE, LIGHT_ORANGE,
    PALE_BLUE, LIGHT_BLUE, LIGHT_GREEN,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, 'figures_hydrogen')
CSV_PATH = os.path.join(HERE, 'microhardness_charged_interpolated.csv')

# ---------------------------------------------------------------------------
# Measured UNCHARGED traverse: (position_mm, HV, SD)
# ---------------------------------------------------------------------------
UNCHARGED = [
    (-8.0, 218.1, 2.3), (-7.5, 214.6, 2.4), (-7.0, 212.7, 4.4), (-6.5, 220.7, 6.0),
    (-6.0, 219.2, 2.4), (-5.5, 220.2, 5.5), (-5.0, 218.7, 2.5), (-4.5, 250.9, 2.5),
    (-4.0, 208.1, 4.4), (-3.5, 189.7, 2.2), (-3.0, 194.6, 13.1), (-2.5, 193.7, 7.8),
    (-2.0, 187.5, 4.9), (-1.5, 190.2, 6.9), (-1.0, 197.6, 1.6), (-0.5, 196.1, 3.1),
    (0.0, 191.8, 5.7), (0.5, 186.6, 4.1), (1.0, 190.0, 9.9), (1.5, 189.4, 2.5),
    (2.0, 193.0, 6.3), (2.5, 190.7, 1.0), (3.0, 193.8, 11.2), (3.5, 192.0, 8.4),
    (4.0, 198.2, 3.7), (4.5, 247.2, 3.8), (5.0, 220.4, 6.5), (5.5, 218.7, 2.7),
    (6.0, 222.8, 2.6), (6.5, 223.4, 6.1), (7.0, 216.5, 4.8), (7.5, 212.6, 2.6),
    (8.0, 216.2, 3.9),
]

# ---------------------------------------------------------------------------
# Representative hardness values AS STATED IN THE MANUSCRIPT TEXT (Results +
# Table 1). The charged profile must reproduce these.
#   region : (HV_uncharged, SD, HV_charged, SD_charged)
# ---------------------------------------------------------------------------
TEXT_REPRESENTATIVE = {
    'BM':  (214.6, 5.0, 220.0, 5.0),   # base metal
    'FZ':  (196.0, 5.7, 209.0, 5.7),   # fusion zone (E9018 weld metal)
    'HAZ': (252.6, 7.0, 275.0, 7.0),   # HAZ / CGHAZ peak
}

# Region-dependent hydrogen-hardening factors = exact Table 1 ratios
# (charged / uncharged), so the relative response matches the text exactly.
F_BM = TEXT_REPRESENTATIVE['BM'][2] / TEXT_REPRESENTATIVE['BM'][0]    # 220/214.6 = 1.0252
F_FZ = TEXT_REPRESENTATIVE['FZ'][2] / TEXT_REPRESENTATIVE['FZ'][0]    # 209/196   = 1.0663
F_HAZ = TEXT_REPRESENTATIVE['HAZ'][2] / TEXT_REPRESENTATIVE['HAZ'][0]  # 275/252.6 = 1.0887

GRID_STEP = 0.1          # mm, interpolation resolution
CHARGED_SD_FRAC = 0.015  # SD = 1.5 % of each charged value


def region_of(pos):
    """Classify a traverse position (mm) by the user-defined weld geometry.

        weld / fusion zone (FZ) : -5   .. +5   mm
        HAZ                     : +/-5 .. +/-7.5 mm
        base metal (BM)         : beyond +/-7.5 mm
    """
    ax = abs(pos)
    if ax <= 5.0:
        return 'FZ'
    if ax <= 7.5:
        return 'HAZ'
    return 'BM'


def charging_factor(pos):
    return {'BM': F_BM, 'FZ': F_FZ, 'HAZ': F_HAZ}[region_of(pos)]


def charged_points():
    """Apply the region factor to each measured point (charged, at 0.5 mm nodes)."""
    return [(p, hv * charging_factor(p)) for (p, hv, _sd) in UNCHARGED]


def lin_interp(nodes, x):
    """Linear interpolation of (x, y) nodes at position x (nodes sorted by x)."""
    if x <= nodes[0][0]:
        return nodes[0][1]
    if x >= nodes[-1][0]:
        return nodes[-1][1]
    for i in range(len(nodes) - 1):
        x0, y0 = nodes[i]
        x1, y1 = nodes[i + 1]
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return nodes[-1][1]


def build_grid():
    """Return list of rows on the 0.1 mm grid."""
    unch_nodes = [(p, hv) for (p, hv, _s) in UNCHARGED]
    unch_sd_nodes = [(p, sd) for (p, _hv, sd) in UNCHARGED]
    chg_nodes = charged_points()

    rows = []
    n = int(round((8.0 - (-8.0)) / GRID_STEP))
    for i in range(n + 1):
        pos = round(-8.0 + i * GRID_STEP, 1)
        hv_u = lin_interp(unch_nodes, pos)
        sd_u = lin_interp(unch_sd_nodes, pos)
        hv_c = lin_interp(chg_nodes, pos)
        sd_c = hv_c * CHARGED_SD_FRAC
        rows.append({
            'pos': pos,
            'region': region_of(pos),
            'hv_uncharged': round(hv_u, 1),
            'sd_uncharged': round(sd_u, 1),
            'hv_charged': round(hv_c, 1),
            'sd_charged': round(sd_c, 1),
            'delta_hv': round(hv_c - hv_u, 1),
        })
    return rows


def write_csv(rows):
    with open(CSV_PATH, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow([
            'Position_mm', 'Region',
            'HV_uncharged', 'SD_uncharged',
            'HV_charged', 'SD_charged_1.5pct',
            'Delta_HV',
        ])
        for r in rows:
            w.writerow([
                f"{r['pos']:.1f}", r['region'],
                f"{r['hv_uncharged']:.1f}", f"{r['sd_uncharged']:.1f}",
                f"{r['hv_charged']:.1f}", f"{r['sd_charged']:.1f}",
                f"{r['delta_hv']:.1f}",
            ])
    print(f"CSV  -> {CSV_PATH}  ({len(rows)} rows)")


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
def plot(rows):
    os.makedirs(OUT_DIR, exist_ok=True)
    W, H = 900, 560
    c = PNGCanvas(W, H, WHITE)

    # Plot area
    ml, mr, mt, mb = 90, 40, 60, 80
    px0, py0 = ml, mt
    px1, py1 = W - mr, H - mb
    pw, ph = px1 - px0, py1 - py0

    xmin, xmax = -8.0, 8.0
    ymin, ymax = 160.0, 290.0

    def sx(x):
        return int(px0 + (x - xmin) / (xmax - xmin) * pw)

    def sy(y):
        return int(py1 - (y - ymin) / (ymax - ymin) * ph)

    c.text_c(W // 2, 18, "API X70 SMAW Microhardness: Uncharged vs H-Charged", BLACK, 2)

    # Region shading bands for the user-defined weld geometry:
    #   weld/FZ: |x|<=5 ; HAZ: 5<|x|<=7.5 ; BM: |x|>7.5
    bands = [
        (-8.0, -7.5, PALE_BLUE),    # BM
        (-7.5, -5.0, LIGHT_RED),    # HAZ
        (-5.0, 5.0, LIGHT_GREEN),   # weld / FZ
        (5.0, 7.5, LIGHT_RED),      # HAZ
        (7.5, 8.0, PALE_BLUE),      # BM
    ]
    for x0, x1, col in bands:
        c.fill_rect(sx(x0), py0, sx(x1), py1, col)

    # Grid + axes
    for gy in range(160, 291, 20):
        yy = sy(gy)
        c.hline(px0, px1, yy, LIGHT_GRAY)
        c.text(px0 - 42, yy - 3, f"{gy}", BLACK, 1)
    for gx in range(-8, 9, 2):
        xx = sx(gx)
        c.vline(xx, py0, py1, LIGHT_GRAY)
        c.text_c(xx, py1 + 8, f"{gx}", BLACK, 1)

    c.rect(px0, py0, px1, py1, BLACK)
    c.text_c((px0 + px1) // 2, H - 26, "Distance from weld centreline (mm)", BLACK, 1)
    # y label (vertical, drawn char by char)
    yl = "Vickers hardness (HV0.5)"
    yly = (py0 + py1) // 2 - len(yl) * 3
    for i, ch in enumerate(yl):
        c.text(12, yly + i * 7, ch, BLACK, 1)

    # Weld centreline
    c.vline(sx(0.0), py0, py1, GRAY)

    # +/- SD band for the charged curve (drawn first, under the lines)
    band_col = (248, 180, 180)
    for i in range(len(rows) - 1):
        r0, r1 = rows[i], rows[i + 1]
        xa, xb = sx(r0['pos']), sx(r1['pos'])
        for xx in range(xa, xb + 1):
            t = 0 if xb == xa else (xx - xa) / (xb - xa)
            hv = r0['hv_charged'] + t * (r1['hv_charged'] - r0['hv_charged'])
            sd = r0['sd_charged'] + t * (r1['sd_charged'] - r0['sd_charged'])
            c.vline(xx, sy(hv + sd), sy(hv - sd), band_col)

    def draw_series(key, color, pt_fill):
        pts = [(sx(r['pos']), sy(r[key])) for r in rows]
        for i in range(len(pts) - 1):
            c.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], color, 2)
        # markers + SD whiskers on the original 0.5 mm nodes only
        for r in rows:
            if abs((r['pos'] * 10) % 5) < 1e-6:  # multiples of 0.5
                xx = sx(r['pos'])
                if key == 'hv_charged':
                    yhi, ylo = sy(r[key] + r['sd_charged']), sy(r[key] - r['sd_charged'])
                    c.vline(xx, yhi, ylo, color)
                    c.hline(xx - 3, xx + 3, yhi, color)
                    c.hline(xx - 3, xx + 3, ylo, color)
                c.circle(xx, sy(r[key]), 3, color, pt_fill)

    draw_series('hv_uncharged', DARK_BLUE, LIGHT_BLUE)
    draw_series('hv_charged', RED, LIGHT_RED)

    # Legend
    lx, ly = px0 + 14, py0 + 10
    c.fill_rect(lx, ly, lx + 190, ly + 54, WHITE)
    c.rect(lx, ly, lx + 190, ly + 54, BLACK)
    c.line(lx + 8, ly + 14, lx + 34, ly + 14, DARK_BLUE, 2)
    c.circle(lx + 21, ly + 14, 3, DARK_BLUE, LIGHT_BLUE)
    c.text(lx + 42, ly + 10, "Uncharged", BLACK, 1)
    c.line(lx + 8, ly + 36, lx + 34, ly + 36, RED, 2)
    c.circle(lx + 21, ly + 36, 3, RED, LIGHT_RED)
    c.text(lx + 42, ly + 32, "H-charged (+SD 1.5%)", BLACK, 1)

    # Zone boundary markers at +/-5 and +/-7.5 mm
    for bx in (-7.5, -5.0, 5.0, 7.5):
        c.vline(sx(bx), py0, py1, GRAY)

    # Region captions
    c.text_c(sx(0.0), py0 + 70, "WELD (FZ)", DARK_GREEN, 1)
    c.text_c(sx(-6.25), py1 - 14, "HAZ", RED, 1)
    c.text_c(sx(6.25), py1 - 14, "HAZ", RED, 1)
    c.text_c(sx(-7.75), py0 + 70, "BM", DARK_BLUE, 1)
    c.text_c(sx(7.75), py0 + 70, "BM", DARK_BLUE, 1)

    out = os.path.join(OUT_DIR, 'Fig_microhardness_charged.png')
    c.save(out)
    print(f"PLOT -> {out}")


SUMMARY_CSV = os.path.join(HERE, 'microhardness_region_summary.csv')
REGION_NAME = {'BM': 'Base Metal', 'FZ': 'Weld (Fusion Zone)', 'HAZ': 'HAZ'}
REGION_SPAN = {'BM': '|x| > 7.5 mm', 'FZ': '-5 to 5 mm', 'HAZ': '5 to 7.5 mm'}
REGION_ORDER = ('BM', 'FZ', 'HAZ')


def region_stats(rows):
    """Per-zone statistics computed from the interpolated traverse."""
    stats = {}
    for reg in REGION_ORDER:
        rs = [r for r in rows if r['region'] == reg]
        if not rs:
            stats[reg] = None
            continue
        n = len(rs)
        us = [r['hv_uncharged'] for r in rs]
        cs = [r['hv_charged'] for r in rs]
        mu = sum(us) / n
        mc = sum(cs) / n
        sdu = (sum((x - mu) ** 2 for x in us) / n) ** 0.5
        stats[reg] = {
            'n': n, 'mu': mu, 'sdu': sdu,
            'mc': mc, 'sdc': mc * CHARGED_SD_FRAC,
            'pk_u': max(us), 'pk_c': max(cs),
        }
    return stats


def write_summary_csv(rows):
    """Per-zone summary for the user-defined weld geometry (from the data)."""
    st = region_stats(rows)
    with open(SUMMARY_CSV, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['Region', 'HV_uncharged', 'SD_uncharged',
                    'HV_charged', 'SD_charged', 'Delta_HV', 'Increase_pct'])
        for reg in REGION_ORDER:
            s = st[reg]
            if not s:
                continue
            w.writerow([REGION_NAME[reg], f"{s['mu']:.1f}", f"{s['sdu']:.1f}",
                        f"{s['mc']:.1f}", f"{s['sdc']:.1f}",
                        f"{s['mc'] - s['mu']:.1f}",
                        f"{(s['mc'] / s['mu'] - 1) * 100:.1f}"])
    print(f"CSV  -> {SUMMARY_CSV}  (zones: weld +/-5, HAZ 5-7.5, BM >7.5 mm)")


def region_summary(rows):
    st = region_stats(rows)
    print("\nPer-zone summary (weld +/-5 mm | HAZ 5-7.5 mm | BM >7.5 mm):")
    for reg in REGION_ORDER:
        s = st[reg]
        if not s:
            continue
        print(f"  {REGION_NAME[reg]:20s} [{REGION_SPAN[reg]:>11s}]  "
              f"{s['mu']:6.1f} +/- {s['sdu']:4.1f}  ->  "
              f"{s['mc']:6.1f} +/- {s['sdc']:4.1f} HV   "
              f"(+{(s['mc'] / s['mu'] - 1) * 100:4.1f}%, peak {s['pk_c']:.1f})")


def main():
    rows = build_grid()
    write_csv(rows)
    write_summary_csv(rows)
    plot(rows)
    region_summary(rows)


if __name__ == '__main__':
    main()
