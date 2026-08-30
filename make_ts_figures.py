"""Generate the four figures for the Time-Series Crop Monitoring chapter.
Uses the stdlib-only Canvas from ts_pnglib (no matplotlib/numpy)."""
import math
import os
from ts_pnglib import Canvas

OUT = "ts_figures"
os.makedirs(OUT, exist_ok=True)

# Palette
DARK = (30, 40, 55)
GRID = (210, 214, 220)
AXIS = (90, 96, 105)
GREEN = (40, 150, 70)
BLUE = (40, 100, 190)
ORANGE = (230, 140, 30)
RED = (200, 55, 55)
PURPLE = (120, 70, 170)
GREY = (140, 145, 152)
LIGHT = (245, 247, 250)


def frame(c, x0, y0, x1, y1, title, xlabel, ylabel):
    # plot background
    c.rect(x0, y0, x1, y1, (252, 252, 253), fill=True)
    c.rect(x0, y0, x1, y1, AXIS, fill=False)
    c.text_center((x0 + x1) // 2, y0 - 26, title, DARK, 2)
    c.text_center((x0 + x1) // 2, y1 + 20, xlabel, DARK, 2)
    # y label vertical-ish: place rotated is hard; put at top-left
    c.text(x0 - 34, (y0 + y1) // 2 - 30, ylabel, DARK, 1)


def gridlines(c, x0, y0, x1, y1, nx, ny):
    for i in range(1, ny):
        y = y0 + (y1 - y0) * i / ny
        c.hline(x0 + 1, x1 - 1, y, GRID)
    for i in range(1, nx):
        x = x0 + (x1 - x0) * i / nx
        c.vline(x, y0 + 1, y1 - 1, GRID)


def legend(c, x, y, items):
    for i, (label, color) in enumerate(items):
        yy = y + i * 22
        c.rect(x, yy, x + 22, yy + 12, color, fill=True)
        c.text(x + 30, yy, label, DARK, 1)


# ---------------------------------------------------------------------------
# FIGURE 1: NDVI time-series curves for three crops across the growing season
# ---------------------------------------------------------------------------
def figure1():
    W, H = 1100, 720
    c = Canvas(W, H, bg=(255, 255, 255))
    x0, y0, x1, y1 = 120, 90, 1000, 560

    def sx(t):   # t in 0..1
        return x0 + t * (x1 - x0)

    def sy(v):   # NDVI 0..1
        return y1 - v * (y1 - y0)

    frame(c, x0, y0, x1, y1,
          "NDVI Temporal Profiles for Delta Crops", "Day of Year (DOY)", "NDVI")
    gridlines(c, x0, y0, x1, y1, 8, 5)

    # axis ticks
    for i in range(6):
        v = i * 0.2
        yy = sy(v)
        c.text(x0 - 40, yy - 4, f"{v:.1f}", AXIS, 1)
    doys = [30, 90, 150, 210, 270, 330]
    for i, d in enumerate(doys):
        xx = sx(i / (len(doys) - 1))
        c.text_center(xx, y1 + 4, str(d), AXIS, 1)

    N = 120

    def curve(peak_t, width, base, amp):
        pts = []
        for i in range(N + 1):
            t = i / N
            v = base + amp * math.exp(-((t - peak_t) ** 2) / (2 * width ** 2))
            pts.append((sx(t), sy(min(0.98, v))))
        return pts

    c.polyline(curve(0.42, 0.14, 0.15, 0.75), GREEN, 3)   # rice (single peak)
    # double crop pattern (wheat then maize-like)
    pts = []
    for i in range(N + 1):
        t = i / N
        v = 0.14 + 0.62 * math.exp(-((t - 0.28) ** 2) / (2 * 0.09 ** 2)) \
            + 0.60 * math.exp(-((t - 0.72) ** 2) / (2 * 0.10 ** 2))
        pts.append((sx(t), sy(min(0.95, v))))
    c.polyline(pts, BLUE, 3)
    c.polyline(curve(0.55, 0.11, 0.12, 0.70), ORANGE, 3)  # maize

    legend(c, x0 + 20, y0 + 10,
           [("Rice (single crop)", GREEN),
            ("Wheat-Maize (double crop)", BLUE),
            ("Maize (single crop)", ORANGE)])
    c.text(x0, H - 30, "Fig. 1  Idealized NDVI trajectories illustrating crop-specific phenology.", DARK, 1)
    c.save_png(os.path.join(OUT, "Figure_1_NDVI_Profiles.png"))
    print("Figure 1 done")


# ---------------------------------------------------------------------------
# FIGURE 2: Raw vs smoothed time series (curve fitting / gap filling)
# ---------------------------------------------------------------------------
def figure2():
    W, H = 1100, 720
    c = Canvas(W, H, bg=(255, 255, 255))
    x0, y0, x1, y1 = 120, 90, 1000, 560

    def sx(t): return x0 + t * (x1 - x0)
    def sy(v): return y1 - v * (y1 - y0)

    frame(c, x0, y0, x1, y1,
          "Curve Fitting and Gap Filling of Noisy NDVI Series",
          "Acquisition index (time)", "NDVI")
    gridlines(c, x0, y0, x1, y1, 8, 5)
    for i in range(6):
        v = i * 0.2
        c.text(x0 - 40, sy(v) - 4, f"{v:.1f}", AXIS, 1)

    N = 60
    import random
    random.seed(7)
    smooth = []
    raw = []
    for i in range(N + 1):
        t = i / N
        base = 0.15 + 0.7 * math.exp(-((t - 0.5) ** 2) / (2 * 0.16 ** 2))
        smooth.append((t, base))
        # add cloud drops + noise, and simulate missing points
        noisy = base - random.random() * 0.28 if random.random() < 0.35 else base + (random.random() - 0.5) * 0.06
        raw.append((t, max(0.02, noisy)))

    # raw points (scatter) + thin connecting line
    c.polyline([(sx(t), sy(v)) for t, v in raw], GREY, 1)
    for t, v in raw:
        c.circle(sx(t), sy(v), 4, RED, fill=True)
    # smoothed / fitted curve
    c.polyline([(sx(t), sy(v)) for t, v in smooth], GREEN, 3)

    legend(c, x0 + 20, y0 + 10,
           [("Raw observations (cloud-affected)", RED),
            ("Fitted / smoothed trajectory", GREEN)])
    c.text(x0, H - 30, "Fig. 2  Noise reduction and reconstruction of a seasonal NDVI signal.", DARK, 1)
    c.save_png(os.path.join(OUT, "Figure_2_Curve_Fitting.png"))
    print("Figure 2 done")


# ---------------------------------------------------------------------------
# FIGURE 3: Bar chart - classification accuracy of methods
# ---------------------------------------------------------------------------
def figure3():
    W, H = 1100, 720
    c = Canvas(W, H, bg=(255, 255, 255))
    x0, y0, x1, y1 = 130, 90, 1000, 560

    frame(c, x0, y0, x1, y1,
          "Reported Accuracy of Temporal Crop-Classification Methods",
          "Method", "Overall Accuracy (%)")
    gridlines(c, x0, y0, x1, y1, 1, 5)

    def sy(v):  # 0..100
        return y1 - (v / 100.0) * (y1 - y0)

    for i in range(6):
        v = i * 20
        c.text(x0 - 45, sy(v) - 4, f"{v}", AXIS, 1)
        c.hline(x0 + 1, x1 - 1, sy(v), GRID)

    data = [("SVM", 82, BLUE), ("RF", 87, GREEN),
            ("CNN", 90, ORANGE), ("LSTM", 92, PURPLE),
            ("Transformer", 94, RED)]
    n = len(data)
    span = (x1 - x0)
    bw = span / (n * 1.8)
    for i, (name, val, col) in enumerate(data):
        cx = x0 + span * (i + 0.5) / n
        left = cx - bw / 2
        right = cx + bw / 2
        c.rect(left, sy(val), right, y1 - 1, col, fill=True)
        c.text_center(int(cx), sy(val) - 20, f"{val}%", DARK, 2)
        c.text_center(int(cx), y1 + 6, name, DARK, 1)

    c.text(x0, H - 30, "Fig. 3  Representative overall accuracies across classifier families (illustrative).", DARK, 1)
    c.save_png(os.path.join(OUT, "Figure_3_Accuracy_Bars.png"))
    print("Figure 3 done")


# ---------------------------------------------------------------------------
# FIGURE 4: Data fusion / workflow schematic
# ---------------------------------------------------------------------------
def figure4():
    W, H = 1150, 720
    c = Canvas(W, H, bg=(255, 255, 255))
    c.text_center(W // 2, 30, "Multi-Source Data Fusion Workflow for Continuous Crop Monitoring", DARK, 2)

    def box(x, y, w, h, label, color, lines=None):
        c.rect(x, y, x + w, y + h, color, fill=True)
        c.rect(x, y, x + w, y + h, DARK, fill=False)
        if lines is None:
            lines = [label]
        ly = y + h // 2 - (len(lines) * 9) // 2
        for ln in lines:
            c.text_center(x + w // 2, ly, ln, (255, 255, 255), 1)
            ly += 16

    # Column 1: sources
    sx = 60
    box(sx, 120, 190, 70, "", (60, 120, 200), ["Optical", "satellites"])
    box(sx, 220, 190, 70, "", (200, 90, 90), ["SAR", "missions"])
    box(sx, 320, 190, 70, "", (90, 160, 90), ["UAV", "imagery"])
    box(sx, 420, 190, 70, "", (180, 140, 60), ["Field / IoT", "sensors"])

    # Column 2: preprocessing
    px = 360
    box(px, 220, 200, 170, "", (110, 110, 130),
        ["Preprocessing:", "atmospheric corr.,", "geometric align.,", "gap filling,", "harmonization"])

    # Column 3: fusion / model
    fx = 660
    box(fx, 230, 200, 150, "", (120, 70, 170),
        ["Data assimilation", "& ML / DL fusion", "(CNN-LSTM,", "Transformer)"])

    # Column 4: outputs
    ox = 960
    box(ox, 120, 150, 70, "", (40, 150, 90), ["Crop maps"])
    box(ox, 220, 150, 70, "", (40, 150, 90), ["Yield", "forecasts"])
    box(ox, 320, 150, 70, "", (40, 150, 90), ["Stress /", "anomaly alerts"])
    box(ox, 420, 150, 70, "", (40, 150, 90), ["Decision", "support"])

    def arrow(x0, y0, x1, y1):
        c.line(x0, y0, x1, y1, DARK, 2)
        # arrowhead
        ang = math.atan2(y1 - y0, x1 - x0)
        for a in (ang + 2.6, ang - 2.6):
            c.line(x1, y1, x1 + 12 * math.cos(a), y1 + 12 * math.sin(a), DARK, 2)

    # sources -> preprocessing
    for yy in (155, 255, 355, 455):
        arrow(sx + 190, yy, px, 305)
    # preprocessing -> fusion
    arrow(px + 200, 305, fx, 305)
    # fusion -> outputs
    for yy in (155, 255, 355, 455):
        arrow(fx + 200, 305, ox, yy)

    c.text(60, H - 30, "Fig. 4  End-to-end fusion pipeline integrating optical, SAR, UAV and in-situ data streams.", DARK, 1)
    c.save_png(os.path.join(OUT, "Figure_4_Fusion_Workflow.png"))
    print("Figure 4 done")


if __name__ == "__main__":
    figure1()
    figure2()
    figure3()
    figure4()
    print("All figures generated in", OUT)
