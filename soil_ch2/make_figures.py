"""Generate 4 PNG figures for Chapter 2 using the pure-Python PNG lib."""
import os
from pnglib import Canvas, text, text_center

OUT = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(OUT, exist_ok=True)

# palette
BLACK = (25, 25, 30)
GRID = (210, 210, 215)
AXIS = (60, 60, 70)
BLUE = (44, 110, 180)
GREEN = (46, 150, 90)
ORANGE = (225, 145, 40)
RED = (200, 60, 55)
PURPLE = (130, 80, 170)
TEAL = (30, 160, 160)
LGRAY = (240, 240, 244)


def frame(c, m):
    """draw plot frame, return plot rect (x0,y0,x1,y1)"""
    x0, y0, x1, y1 = m, m + 40, c.w - m, c.h - m - 30
    c.rect(x0, y0, x1, y1, (252, 252, 253))
    c.rect_outline(x0, y0, x1, y1, AXIS, 2)
    return x0, y0, x1, y1


# ---------------- Figure 1: Global heavy-metal contamination by region (grouped bars) ----------------
def figure1():
    c = Canvas(900, 560, (255, 255, 255))
    text_center(c, 450, 12, "GLOBAL SOIL HEAVY-METAL LEVELS BY REGION", BLACK, 3)
    x0, y0, x1, y1 = frame(c, 70)
    regions = ["ASIA", "EUROPE", "AFRICA", "N AMERICA", "S AMERICA"]
    # three metals: Cd, Pb, As (relative index)
    series = {
        "CD": ([2.8, 1.6, 1.1, 1.3, 1.9], ORANGE),
        "PB": ([4.2, 2.9, 2.1, 2.6, 3.1], BLUE),
        "AS": ([3.5, 1.9, 1.4, 1.7, 2.4], GREEN),
    }
    maxv = 5.0
    # gridlines + y labels
    for i in range(6):
        yy = y1 - int((y1 - y0) * i / 5)
        c.line(x0, yy, x1, yy, GRID, 1)
        text(c, x0 - 32, yy - 3, str(i), AXIS, 1)
    text(c, 20, (y0 + y1) // 2 - 20, "INDEX", AXIS, 1)
    n_reg = len(regions)
    group_w = (x1 - x0) / n_reg
    bar_w = int(group_w / 5)
    metals = list(series.keys())
    for gi, reg in enumerate(regions):
        gx = x0 + int(group_w * gi) + bar_w // 2
        for mi, m in enumerate(metals):
            val = series[m][0][gi]
            col = series[m][1]
            bx0 = gx + mi * bar_w
            bh = int((y1 - y0) * val / maxv)
            c.rect(bx0, y1 - bh, bx0 + bar_w - 3, y1 - 1, col)
        text_center(c, gx + int(1.5 * bar_w), y1 + 8, reg, AXIS, 1)
    # legend
    lx, ly = x1 - 150, y0 + 10
    for mi, m in enumerate(metals):
        c.rect(lx, ly + mi * 18, lx + 12, ly + mi * 18 + 12, series[m][1])
        text(c, lx + 18, ly + mi * 18 + 2, m, BLACK, 1)
    c.save(os.path.join(OUT, "figure1_heavy_metal_regions.png"))


# ---------------- Figure 2: Temporal trend of soil pollution indicators (line chart) ----------------
def figure2():
    c = Canvas(900, 560, (255, 255, 255))
    text_center(c, 450, 12, "TEMPORAL TRENDS IN SOIL POLLUTION 1970-2020", BLACK, 3)
    x0, y0, x1, y1 = frame(c, 70)
    years = [1970, 1980, 1990, 2000, 2010, 2020]
    lines = {
        "METALS": ([30, 45, 62, 70, 66, 58], BLUE),
        "PESTICIDES": ([20, 40, 68, 82, 88, 92], RED),
        "MICROPLASTIC": ([2, 6, 15, 34, 62, 90], PURPLE),
    }
    maxv = 100
    for i in range(6):
        yy = y1 - int((y1 - y0) * i / 5)
        c.line(x0, yy, x1, yy, GRID, 1)
        text(c, x0 - 40, yy - 3, str(i * 20), AXIS, 1)
    text(c, 18, (y0 + y1) // 2 - 30, "INDEX", AXIS, 1)
    n = len(years)
    for i, yr in enumerate(years):
        xx = x0 + int((x1 - x0) * i / (n - 1))
        text_center(c, xx, y1 + 8, str(yr), AXIS, 1)
    for name, (vals, col) in lines.items():
        pts = []
        for i, v in enumerate(vals):
            xx = x0 + int((x1 - x0) * i / (n - 1))
            yy = y1 - int((y1 - y0) * v / maxv)
            pts.append((xx, yy))
        for i in range(len(pts) - 1):
            c.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], col, 3)
        for p in pts:
            c.circle(p[0], p[1], 4, col)
    lx, ly = x0 + 20, y0 + 10
    for i, (name, (vals, col)) in enumerate(lines.items()):
        c.rect(lx, ly + i * 18, lx + 12, ly + i * 18 + 12, col)
        text(c, lx + 18, ly + i * 18 + 2, name, BLACK, 1)
    c.save(os.path.join(OUT, "figure2_temporal_trends.png"))


# ---------------- Figure 3: Source contribution to soil contamination (stacked/proportional bars) ----------------
def figure3():
    c = Canvas(900, 560, (255, 255, 255))
    text_center(c, 450, 12, "SOURCE CONTRIBUTION TO SOIL CONTAMINATION", BLACK, 3)
    x0, y0, x1, y1 = frame(c, 70)
    cats = ["MINING", "INDUSTRY", "AGRICULTURE", "URBAN WASTE", "ATMOSPHERE"]
    parts = [
        ("METALS", 0.0, None),
    ]
    # each category split into three stacked shares
    data = {
        "MINING": [(0.70, ORANGE), (0.20, BLUE), (0.10, GREEN)],
        "INDUSTRY": [(0.55, ORANGE), (0.30, BLUE), (0.15, GREEN)],
        "AGRICULTURE": [(0.15, ORANGE), (0.20, BLUE), (0.65, GREEN)],
        "URBAN WASTE": [(0.35, ORANGE), (0.25, BLUE), (0.40, GREEN)],
        "ATMOSPHERE": [(0.60, ORANGE), (0.30, BLUE), (0.10, GREEN)],
    }
    labels = ["HEAVY METALS", "ORGANICS", "NUTRIENTS/OTHER"]
    for i in range(6):
        yy = y1 - int((y1 - y0) * i / 5)
        c.line(x0, yy, x1, yy, GRID, 1)
        text(c, x0 - 40, yy - 3, str(i * 20) + "%", AXIS, 1)
    n = len(cats)
    group_w = (x1 - x0) / n
    bar_w = int(group_w * 0.5)
    for gi, cat in enumerate(cats):
        bx = x0 + int(group_w * gi) + (int(group_w) - bar_w) // 2
        base = y1
        for share, col in data[cat]:
            h = int((y1 - y0) * share)
            c.rect(bx, base - h, bx + bar_w, base, col)
            base -= h
        text_center(c, bx + bar_w // 2, y1 + 8, cat, AXIS, 1)
    lx, ly = x1 - 190, y0 + 8
    cols = [ORANGE, BLUE, GREEN]
    for i, lab in enumerate(labels):
        c.rect(lx, ly + i * 18, lx + 12, ly + i * 18 + 12, cols[i])
        text(c, lx + 18, ly + i * 18 + 2, lab, BLACK, 1)
    c.save(os.path.join(OUT, "figure3_source_contribution.png"))


# ---------------- Figure 4: Risk-based prioritization scatter (hotspot map) ----------------
def figure4():
    c = Canvas(900, 560, (255, 255, 255))
    text_center(c, 450, 12, "RISK-BASED HOTSPOT PRIORITIZATION MATRIX", BLACK, 3)
    x0, y0, x1, y1 = frame(c, 70)
    for i in range(6):
        yy = y1 - int((y1 - y0) * i / 5)
        c.line(x0, yy, x1, yy, GRID, 1)
        xx = x0 + int((x1 - x0) * i / 5)
        c.line(xx, y0, xx, y1, GRID, 1)
        text(c, x0 - 32, yy - 3, str(i * 2), AXIS, 1)
        text_center(c, xx, y1 + 8, str(i * 2), AXIS, 1)
    text_center(c, (x0 + x1) // 2, y1 + 26, "HUMAN-HEALTH RISK", AXIS, 1)
    text(c, 16, (y0 + y1) // 2 - 40, "ECO RISK", AXIS, 1)
    # bubbles: (health, eco, size, color, label)
    pts = [
        (8.5, 8.0, 22, RED, "MINING BELT"),
        (7.5, 6.0, 18, ORANGE, "IND CORRIDOR"),
        (5.5, 7.5, 16, PURPLE, "E-WASTE"),
        (6.0, 4.5, 14, BLUE, "URBAN FRINGE"),
        (4.0, 6.5, 13, TEAL, "IRRIGATED"),
        (3.0, 3.0, 10, GREEN, "RURAL"),
    ]
    for hx, ex, sz, col, lab in pts:
        px = x0 + int((x1 - x0) * hx / 10)
        py = y1 - int((y1 - y0) * ex / 10)
        c.circle(px, py, sz, col)
        text(c, px + sz + 3, py - 3, lab, BLACK, 1)
    # priority threshold line
    c.line(x0, y0 + int((y1 - y0) * 0.4), x1, y0, RED, 1)
    text(c, x1 - 150, y0 + 6, "HIGH PRIORITY", RED, 1)
    c.save(os.path.join(OUT, "figure4_risk_prioritization.png"))


if __name__ == "__main__":
    figure1()
    figure2()
    figure3()
    figure4()
    print("Figures written to", OUT)
    for f in sorted(os.listdir(OUT)):
        p = os.path.join(OUT, f)
        print(f, os.path.getsize(p), "bytes")
