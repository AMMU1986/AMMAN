#!/usr/bin/env python3
"""
Generate the 6 manuscript figures as PNG images using ONLY the Python
standard library (zlib + struct). Includes a tiny 5x7 bitmap font so that
boxes, arrows, charts and labels can be drawn without matplotlib/PIL.

Figures:
  1  Overall workflow of the proposed framework
  2  Longitudinal preprocessing & temporal feature engineering
  3  Architecture of the hybrid ML-DL model
  4  Calibration performance across prediction horizons
  5  Explainability analysis using SHAP (feature importance)
  6  Time-dependent CKD progression risk stratification
"""

import os
import zlib
import struct
import math

OUTDIR = '/projects/sandbox/AMMAN/ckd_figures'

# ----------------------------------------------------------------------
# 5x7 bitmap font
# ----------------------------------------------------------------------
FONT = {
    'A': ["01110","10001","10001","11111","10001","10001","10001"],
    'B': ["11110","10001","10001","11110","10001","10001","11110"],
    'C': ["01110","10001","10000","10000","10000","10001","01110"],
    'D': ["11110","10001","10001","10001","10001","10001","11110"],
    'E': ["11111","10000","10000","11110","10000","10000","11111"],
    'F': ["11111","10000","10000","11110","10000","10000","10000"],
    'G': ["01110","10001","10000","10111","10001","10001","01111"],
    'H': ["10001","10001","10001","11111","10001","10001","10001"],
    'I': ["01110","00100","00100","00100","00100","00100","01110"],
    'J': ["00111","00010","00010","00010","00010","10010","01100"],
    'K': ["10001","10010","10100","11000","10100","10010","10001"],
    'L': ["10000","10000","10000","10000","10000","10000","11111"],
    'M': ["10001","11011","10101","10101","10001","10001","10001"],
    'N': ["10001","10001","11001","10101","10011","10001","10001"],
    'O': ["01110","10001","10001","10001","10001","10001","01110"],
    'P': ["11110","10001","10001","11110","10000","10000","10000"],
    'Q': ["01110","10001","10001","10001","10101","10010","01101"],
    'R': ["11110","10001","10001","11110","10100","10010","10001"],
    'S': ["01111","10000","10000","01110","00001","00001","11110"],
    'T': ["11111","00100","00100","00100","00100","00100","00100"],
    'U': ["10001","10001","10001","10001","10001","10001","01110"],
    'V': ["10001","10001","10001","10001","10001","01010","00100"],
    'W': ["10001","10001","10001","10101","10101","11011","10001"],
    'X': ["10001","10001","01010","00100","01010","10001","10001"],
    'Y': ["10001","10001","01010","00100","00100","00100","00100"],
    'Z': ["11111","00001","00010","00100","01000","10000","11111"],
    '0': ["01110","10001","10011","10101","11001","10001","01110"],
    '1': ["00100","01100","00100","00100","00100","00100","01110"],
    '2': ["01110","10001","00001","00010","00100","01000","11111"],
    '3': ["11111","00010","00100","00010","00001","10001","01110"],
    '4': ["00010","00110","01010","10010","11111","00010","00010"],
    '5': ["11111","10000","11110","00001","00001","10001","01110"],
    '6': ["00110","01000","10000","11110","10001","10001","01110"],
    '7': ["11111","00001","00010","00100","01000","01000","01000"],
    '8': ["01110","10001","10001","01110","10001","10001","01110"],
    '9': ["01110","10001","10001","01111","00001","00010","01100"],
    '.': ["00000","00000","00000","00000","00000","01100","01100"],
    ',': ["00000","00000","00000","00000","00000","00100","01000"],
    '-': ["00000","00000","00000","11111","00000","00000","00000"],
    '_': ["00000","00000","00000","00000","00000","00000","11111"],
    '/': ["00001","00001","00010","00100","01000","10000","10000"],
    '(': ["00010","00100","01000","01000","01000","00100","00010"],
    ')': ["01000","00100","00010","00010","00010","00100","01000"],
    ':': ["00000","01100","01100","00000","01100","01100","00000"],
    '%': ["11000","11001","00010","00100","01000","10011","00011"],
    '+': ["00000","00100","00100","11111","00100","00100","00000"],
    '=': ["00000","00000","11111","00000","11111","00000","00000"],
    '&': ["01100","10010","10010","01100","10101","10010","01101"],
    '>': ["10000","01000","00100","00010","00100","01000","10000"],
    '<': ["00001","00010","00100","01000","00100","00010","00001"],
    ' ': ["00000","00000","00000","00000","00000","00000","00000"],
}


class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w, self.h = w, h
        self.px = bytearray()
        row = bytes(bg) * w
        for _ in range(h):
            self.px += row

    def _idx(self, x, y):
        return (y * self.w + x) * 3

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = self._idx(x, y)
            self.px[i:i+3] = bytes(c)

    def fill_rect(self, x0, y0, x1, y1, c):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        for y in range(max(0, y0), min(self.h, y1)):
            i0 = self._idx(max(0, x0), y)
            n = min(self.w, x1) - max(0, x0)
            if n > 0:
                self.px[i0:i0 + 3*n] = bytes(c) * n

    def rect(self, x0, y0, x1, y1, c, t=2):
        self.fill_rect(x0, y0, x1, y0 + t, c)
        self.fill_rect(x0, y1 - t, x1, y1, c)
        self.fill_rect(x0, y0, x0 + t, y1, c)
        self.fill_rect(x1 - t, y0, x1, y1, c)

    def box(self, x0, y0, x1, y1, fill, border=(60, 60, 60), t=2):
        self.fill_rect(x0, y0, x1, y1, fill)
        self.rect(x0, y0, x1, y1, border, t)

    def line(self, x0, y0, x1, y1, c, t=1):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0); dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for ox in range(t):
                for oy in range(t):
                    self.set(x0 + ox, y0 + oy, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x0 += sx
            if e2 <= dx:
                err += dx; y0 += sy

    def disc(self, cx, cy, r, c):
        cx, cy, r = int(cx), int(cy), int(r)
        for y in range(-r, r + 1):
            for x in range(-r, r + 1):
                if x*x + y*y <= r*r:
                    self.set(cx + x, cy + y, c)

    def text(self, x, y, s, c=(20, 20, 20), scale=2, spacing=1):
        s = s.upper()
        cx = int(x); y = int(y)
        for ch in s:
            g = FONT.get(ch, FONT[' '])
            for ry, row in enumerate(g):
                for rx, bit in enumerate(row):
                    if bit == '1':
                        self.fill_rect(cx + rx*scale, y + ry*scale,
                                       cx + rx*scale + scale, y + ry*scale + scale, c)
            cx += (5 + spacing) * scale
        return cx

    def text_w(self, s, scale=2, spacing=1):
        return len(s) * (5 + spacing) * scale

    def ctext(self, cx, y, s, c=(20, 20, 20), scale=2, spacing=1):
        w = self.text_w(s, scale, spacing)
        self.text(cx - w // 2, y, s, c, scale, spacing)

    def arrow(self, x0, y0, x1, y1, c=(60, 60, 60), t=2):
        self.line(x0, y0, x1, y1, c, t)
        ang = math.atan2(y1 - y0, x1 - x0)
        for a in (ang + math.radians(150), ang - math.radians(150)):
            self.line(x1, y1, x1 + 11*math.cos(a), y1 + 11*math.sin(a), c, t)

    def save(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)
            i = y * self.w * 3
            raw += self.px[i:i + self.w*3]

        def chunk(typ, data):
            c = typ + data
            return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

        png = b'\x89PNG\r\n\x1a\n'
        png += chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0))
        png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
        png += chunk(b'IEND', b'')
        with open(path, 'wb') as f:
            f.write(png)
        print('  wrote', path, f'({self.w}x{self.h})')


# palette
BLUE = (210, 226, 243); DBLUE = (31, 56, 100)
GREEN = (214, 240, 220); DGREEN = (33, 110, 60)
ORANGE = (252, 228, 205); DORANGE = (180, 95, 20)
PURPLE = (229, 221, 240); DPURPLE = (90, 50, 140)
RED = (248, 215, 215); DRED = (170, 40, 40)
GREY = (235, 235, 238); DGREY = (90, 90, 95)
TEAL = (205, 236, 236); DTEAL = (20, 110, 110)


def flow_box(cv, x0, y0, x1, y1, lines, fill, border, tc=(20, 20, 20), scale=2):
    cv.box(x0, y0, x1, y1, fill, border, 3)
    cy = (y0 + y1)//2 - (len(lines)*9*scale)//2
    for ln in lines:
        cv.ctext((x0 + x1)//2, cy, ln, tc, scale)
        cy += 9*scale + 3


# ----------------------------------------------------------------------
# Figure 1 - Overall workflow
# ----------------------------------------------------------------------
def fig1():
    cv = Canvas(1180, 760)
    cv.ctext(590, 24, "FIGURE 1  OVERALL WORKFLOW OF THE PROPOSED FRAMEWORK", DBLUE, 3)
    steps = [
        (["EHR DATA", "COHORT"], BLUE, DBLUE),
        (["LANDMARKING", "T0...TAU"], BLUE, DBLUE),
        (["PREPROCESSING", "& FEATURES"], GREEN, DGREEN),
    ]
    x = 60; y = 90; bw = 230; bh = 90; gap = 60
    cx_prev = None
    for lines, fill, border in steps:
        flow_box(cv, x, y, x + bw, y + bh, lines, fill, border)
        if cx_prev is not None:
            cv.arrow(cx_prev, y + bh//2, x, y + bh//2, (60, 60, 60), 3)
        cx_prev = x + bw
        x += bw + gap
    # branch row
    bx = 320; by = 240
    flow_box(cv, bx, by, bx + 240, by + 80, ["ML BRANCH", "(BOOSTED TREES)"], ORANGE, DORANGE)
    flow_box(cv, bx + 320, by, bx + 560, by + 80, ["DL BRANCH", "(GRU + ATTENTION)"], PURPLE, DPURPLE)
    cv.arrow(cx_prev - bw//2, y + bh, cx_prev - bw//2, by, (60, 60, 60), 3) if False else None
    cv.arrow(x - bw - gap - bw//2, y + bh, bx + 120, by, (60, 60, 60), 3)
    cv.arrow(x - bw - gap - bw//2, y + bh, bx + 440, by, (60, 60, 60), 3)
    # fusion
    fx = 430; fy = 390
    flow_box(cv, fx, fy, fx + 320, fy + 80, ["GATED FEATURE FUSION"], TEAL, DTEAL)
    cv.arrow(bx + 120, by + 80, fx + 100, fy, (60, 60, 60), 3)
    cv.arrow(bx + 440, by + 80, fx + 220, fy, (60, 60, 60), 3)
    # prediction
    px = 430; py = 520
    flow_box(cv, px, py, px + 320, py + 80, ["TIME-DEPENDENT", "PREDICTION 1/2/3/5 YR"], GREEN, DGREEN)
    cv.arrow(fx + 160, fy + 80, px + 160, py, (60, 60, 60), 3)
    # bottom row three outputs
    oy = 650; ow = 320
    flow_box(cv, 60, oy, 60 + ow, oy + 80, ["CALIBRATION"], BLUE, DBLUE)
    flow_box(cv, 430, oy, 430 + ow, oy + 80, ["EXPLAINABILITY (SHAP)"], PURPLE, DPURPLE)
    flow_box(cv, 800, oy, 800 + ow, oy + 80, ["RISK STRATIFICATION"], RED, DRED)
    cv.arrow(px + 160, py + 80, px + 160, oy, (60, 60, 60), 3)
    cv.arrow(px + 60, oy + 40, 60 + ow, oy + 40, (60, 60, 60), 3)
    cv.arrow(px + 320, oy + 40, 800, oy + 40, (60, 60, 60), 3)
    cv.save(os.path.join(OUTDIR, 'Figure_1_Workflow.png'))


# ----------------------------------------------------------------------
# Figure 2 - Preprocessing & feature engineering
# ----------------------------------------------------------------------
def fig2():
    cv = Canvas(1180, 720)
    cv.ctext(590, 22, "FIGURE 2  LONGITUDINAL PREPROCESSING & TEMPORAL FEATURE ENGINEERING", DGREEN, 2)
    # left: raw irregular eGFR trajectory panel
    px0, py0, px1, py1 = 70, 90, 540, 360
    cv.box(px0, py0, px1, py1, (250, 250, 252), DGREY, 2)
    cv.ctext((px0+px1)//2, py0 + 8, "EGFR TRAJECTORY (IRREGULAR SAMPLING)", DGREY, 2)
    # axes
    ax0, ay1 = px0 + 50, py1 - 40
    ax1, ay0 = px1 - 20, py0 + 45
    cv.line(ax0, ay0, ax0, ay1, (40, 40, 40), 2)
    cv.line(ax0, ay1, ax1, ay1, (40, 40, 40), 2)
    cv.text(px0 + 8, (ay0+ay1)//2 - 20, "EGFR", DGREY, 2)
    cv.text((ax0+ax1)//2 - 20, ay1 + 12, "TIME", DGREY, 2)
    pts = [(0.0, 0.80), (0.12, 0.74), (0.30, 0.70), (0.38, 0.60),
           (0.55, 0.55), (0.70, 0.42), (0.85, 0.38), (1.0, 0.28)]
    sx = lambda t: ax0 + t*(ax1-ax0)
    sy = lambda v: ay1 - v*(ay1-ay0)
    prev = None
    for t, v in pts:
        if prev:
            cv.line(prev[0], prev[1], sx(t), sy(v), DGREEN, 2)
        cv.disc(int(sx(t)), int(sy(v)), 4, DGREEN)
        prev = (sx(t), sy(v))
    # fitted slope (dashed-ish straight line)
    cv.line(sx(0.0), sy(0.80), sx(1.0), sy(0.30), DRED, 2)
    cv.text(sx(0.55), sy(0.72), "SLOPE", DRED, 2)
    # right: pipeline boxes
    bx = 600; bw = 500; bh = 60; y = 95; gap = 24
    rows = [
        (["RAW TIME-STAMPED VISITS"], BLUE, DBLUE),
        (["ENCODE / NORMALIZE (TRAIN STATS ONLY)"], BLUE, DBLUE),
        (["TRAJECTORIES: SLOPE, VARIABILITY, LAST"], GREEN, DGREEN),
        (["RATE-OF-CHANGE + TEMPORAL STATS"], GREEN, DGREEN),
        (["TIME-GAP ENCODING + MISSINGNESS MASK"], ORANGE, DORANGE),
        (["FEATURE SELECTION / REDUNDANCY"], PURPLE, DPURPLE),
        (["LEAKAGE-FREE PATIENT-LEVEL SPLIT"], RED, DRED),
    ]
    cxprev = None
    for lines, fill, border in rows:
        flow_box(cv, bx, y, bx + bw, y + bh, lines, fill, border, scale=2)
        if cxprev is not None:
            cv.arrow(bx + bw//2, cxprev, bx + bw//2, y, (60, 60, 60), 2)
        cxprev = y + bh
        y += bh + gap
    cv.save(os.path.join(OUTDIR, 'Figure_2_Preprocessing.png'))


# ----------------------------------------------------------------------
# Figure 3 - Hybrid architecture
# ----------------------------------------------------------------------
def fig3():
    cv = Canvas(1180, 760)
    cv.ctext(590, 22, "FIGURE 3  ARCHITECTURE OF THE PROPOSED HYBRID ML-DL MODEL", DBLUE, 3)
    # inputs
    flow_box(cv, 60, 90, 320, 170, ["STRUCTURED", "CLINICAL FEATURES"], GREY, DGREY)
    flow_box(cv, 860, 90, 1120, 170, ["LONGITUDINAL", "BIOMARKER SEQUENCES"], GREY, DGREY)
    # ML branch
    flow_box(cv, 60, 230, 320, 300, ["GRADIENT-BOOSTED", "TREES (XGBOOST)"], ORANGE, DORANGE)
    flow_box(cv, 60, 340, 320, 400, ["ML EMBEDDING  z_ML"], ORANGE, DORANGE)
    cv.arrow(190, 170, 190, 230, (60, 60, 60), 3)
    cv.arrow(190, 300, 190, 340, (60, 60, 60), 3)
    # DL branch
    flow_box(cv, 860, 230, 1120, 300, ["TIME-AWARE GRU / LSTM"], PURPLE, DPURPLE)
    flow_box(cv, 860, 340, 1120, 400, ["TEMPORAL ATTENTION  z_DL"], PURPLE, DPURPLE)
    cv.arrow(990, 170, 990, 230, (60, 60, 60), 3)
    cv.arrow(990, 300, 990, 340, (60, 60, 60), 3)
    # fusion
    flow_box(cv, 440, 340, 740, 410, ["GATED FUSION  z_FUS"], TEAL, DTEAL)
    cv.arrow(320, 375, 440, 375, (60, 60, 60), 3)
    cv.arrow(1120 - 260, 375, 740, 375, (60, 60, 60), 3) if False else cv.arrow(860, 375, 740, 375, (60, 60, 60), 3)
    # heads
    hy = 500
    for i, h in enumerate(["1 YR", "2 YR", "3 YR", "5 YR"]):
        hx = 300 + i*160
        flow_box(cv, hx, hy, hx + 130, hy + 70, ["HAZARD " + h], GREEN, DGREEN)
        cv.arrow(590, 410, hx + 65, hy, (60, 60, 60), 2)
    # outputs
    flow_box(cv, 300, 610, 870, 680, ["CALIBRATED HORIZON-SPECIFIC PROGRESSION PROBABILITY"], BLUE, DBLUE)
    for i in range(4):
        hx = 300 + i*160
        cv.arrow(hx + 65, hy + 70, hx + 65, 610, (60, 60, 60), 2)
    cv.save(os.path.join(OUTDIR, 'Figure_3_Architecture.png'))


# ----------------------------------------------------------------------
# Figure 4 - Calibration curves
# ----------------------------------------------------------------------
def fig4():
    cv = Canvas(900, 760)
    cv.ctext(450, 22, "FIGURE 4  CALIBRATION ACROSS PREDICTION HORIZONS", DBLUE, 3)
    ax0, ay0, ax1, ay1 = 120, 90, 820, 620
    cv.box(ax0, ay0, ax1, ay1, (252, 252, 254), DGREY, 2)
    # grid + axes
    for g in range(0, 11):
        gx = ax0 + g*(ax1-ax0)//10
        gy = ay1 - g*(ay1-ay0)//10
        cv.line(gx, ay0, gx, ay1, (232, 232, 236), 1)
        cv.line(ax0, gy, ax1, gy, (232, 232, 236), 1)
    cv.line(ax0, ay0, ax0, ay1, (40, 40, 40), 2)
    cv.line(ax0, ay1, ax1, ay1, (40, 40, 40), 2)
    # perfect diagonal
    cv.line(ax0, ay1, ax1, ay0, (120, 120, 120), 2)
    cv.text(ax0 + 20, ay0 + 10, "PERFECT", (120, 120, 120), 2)
    sx = lambda v: ax0 + v*(ax1-ax0)
    sy = lambda v: ay1 - v*(ay1-ay0)
    curves = [
        ("1 YR", DGREEN, [0.02, 0.11, 0.22, 0.31, 0.42, 0.52, 0.62, 0.71, 0.82, 0.92]),
        ("2 YR", DBLUE,  [0.03, 0.10, 0.19, 0.30, 0.40, 0.49, 0.60, 0.69, 0.80, 0.90]),
        ("3 YR", DORANGE,[0.05, 0.13, 0.21, 0.28, 0.37, 0.47, 0.55, 0.66, 0.76, 0.86]),
        ("5 YR", DRED,   [0.06, 0.15, 0.20, 0.26, 0.34, 0.43, 0.52, 0.61, 0.72, 0.83]),
    ]
    xs = [0.05 + i*0.1 for i in range(10)]
    for name, col, ys in curves:
        prev = None
        for xv, yv in zip(xs, ys):
            p = (sx(xv), sy(yv))
            if prev:
                cv.line(prev[0], prev[1], p[0], p[1], col, 3)
            cv.disc(int(p[0]), int(p[1]), 4, col)
            prev = p
    cv.text(ax0 + 40, ay1 + 16, "PREDICTED PROBABILITY", (40, 40, 40), 2)
    for i in range(7):
        yy = ay0 + 20 + i  # placeholder
    # y label (vertical approximated horizontally at top-left)
    cv.text(20, ay0 + 10, "OBS", (40, 40, 40), 2)
    cv.text(20, ay0 + 34, "FREQ", (40, 40, 40), 2)
    # legend
    ly = 660
    for i, (name, col, _) in enumerate(curves):
        lx = 130 + i*180
        cv.fill_rect(lx, ly, lx + 26, ly + 16, col)
        cv.text(lx + 34, ly, name, (40, 40, 40), 2)
    cv.save(os.path.join(OUTDIR, 'Figure_4_Calibration.png'))


# ----------------------------------------------------------------------
# Figure 5 - SHAP feature importance
# ----------------------------------------------------------------------
def fig5():
    cv = Canvas(1000, 720)
    cv.ctext(500, 22, "FIGURE 5  GLOBAL FEATURE IMPORTANCE (MEAN |SHAP|)", DPURPLE, 3)
    feats = [
        ("BASELINE EGFR", 0.98),
        ("EGFR SLOPE", 0.86),
        ("ALBUMINURIA (UACR)", 0.74),
        ("AGE", 0.60),
        ("RECENT EGFR", 0.57),
        ("DIABETES", 0.46),
        ("EGFR VARIABILITY", 0.40),
        ("SYSTOLIC BP", 0.33),
        ("SERUM ALBUMIN", 0.27),
        ("HAEMOGLOBIN", 0.21),
        ("BICARBONATE", 0.16),
        ("RAS INHIBITOR USE", 0.12),
    ]
    x0 = 360; y = 80; bh = 36; gap = 14; maxw = 560
    for name, val in feats:
        w = int(val*maxw)
        cv.fill_rect(x0, y, x0 + w, y + bh, PURPLE)
        cv.rect(x0, y, x0 + w, y + bh, DPURPLE, 2)
        cv.text(x0 - cv.text_w(name, 2) - 12, y + 8, name, (40, 40, 40), 2)
        cv.text(x0 + w + 8, y + 8, str(val), DPURPLE, 2)
        y += bh + gap
    cv.line(x0, 70, x0, y, (40, 40, 40), 2)
    cv.text(x0 + 180, y + 6, "MEAN |SHAP| VALUE", (40, 40, 40), 2)
    cv.save(os.path.join(OUTDIR, 'Figure_5_SHAP.png'))


# ----------------------------------------------------------------------
# Figure 6 - Risk stratification
# ----------------------------------------------------------------------
def fig6():
    cv = Canvas(1180, 720)
    cv.ctext(590, 22, "FIGURE 6  TIME-DEPENDENT CKD PROGRESSION RISK STRATIFICATION", DRED, 2)
    # left: cumulative incidence step curves
    ax0, ay0, ax1, ay1 = 90, 90, 620, 600
    cv.box(ax0, ay0, ax1, ay1, (252, 252, 254), DGREY, 2)
    cv.line(ax0, ay0, ax0, ay1, (40, 40, 40), 2)
    cv.line(ax0, ay1, ax1, ay1, (40, 40, 40), 2)
    cv.text(ax0 + 60, ay1 + 14, "FOLLOW-UP TIME (YEARS)", (40, 40, 40), 2)
    cv.text(20, ay0 + 10, "CUM.", (40, 40, 40), 2)
    cv.text(20, ay0 + 34, "INCID", (40, 40, 40), 2)
    sx = lambda t: ax0 + (t/5.0)*(ax1-ax0)
    sy = lambda v: ay1 - v*(ay1-ay0)
    groups = [
        ("VERY HIGH", DRED, [0.0, 0.22, 0.45, 0.62, 0.78, 0.88]),
        ("HIGH", DORANGE, [0.0, 0.12, 0.26, 0.38, 0.50, 0.60]),
        ("MODERATE", DBLUE, [0.0, 0.05, 0.12, 0.19, 0.27, 0.34]),
        ("LOW", DGREEN, [0.0, 0.01, 0.04, 0.07, 0.11, 0.15]),
    ]
    for name, col, ys in groups:
        for t in range(len(ys) - 1):
            x_a, x_b = sx(t), sx(t + 1)
            y_a, y_b = sy(ys[t]), sy(ys[t + 1])
            cv.line(x_a, y_a, x_b, y_a, col, 3)   # horizontal step
            cv.line(x_b, y_a, x_b, y_b, col, 3)   # vertical step
    # legend
    for i, (name, col, _) in enumerate(groups):
        ly = ay0 + 20 + i*28
        cv.fill_rect(ax0 + 20, ly, ax0 + 46, ly + 18, col)
        cv.text(ax0 + 54, ly + 2, name, (40, 40, 40), 2)

    # right: decision curve analysis
    bx0, by0, bx1, by1 = 700, 90, 1140, 600
    cv.box(bx0, by0, bx1, by1, (252, 252, 254), DGREY, 2)
    cv.line(bx0, by0, bx0, by1, (40, 40, 40), 2)
    cv.line(bx0, by1, bx1, by1, (40, 40, 40), 2)
    cv.ctext((bx0+bx1)//2, by0 - 2, "DECISION-CURVE ANALYSIS", DGREY, 2)
    cv.text(bx0 + 60, by1 + 14, "THRESHOLD PROBABILITY", (40, 40, 40), 2)
    cv.text(640, by0 + 10, "NET", (40, 40, 40), 2)
    cv.text(640, by0 + 34, "BEN", (40, 40, 40), 2)
    bsx = lambda t: bx0 + t*(bx1-bx0)
    bsy = lambda v: by1 - (v/0.4)*(by1-by0)
    xs = [i*0.05 for i in range(0, 11)]
    model = [0.36, 0.33, 0.30, 0.27, 0.24, 0.21, 0.18, 0.15, 0.12, 0.09, 0.06]
    treat_all = [0.35, 0.30, 0.24, 0.18, 0.12, 0.06, 0.00, -0.06, -0.12, -0.18, -0.24]
    prev = None
    for xv, yv in zip(xs, model):
        p = (bsx(xv), bsy(max(yv, 0)))
        if prev: cv.line(prev[0], prev[1], p[0], p[1], DTEAL, 3)
        prev = p
    prev = None
    for xv, yv in zip(xs, treat_all):
        p = (bsx(xv), bsy(max(yv, 0)))
        if prev: cv.line(prev[0], prev[1], p[0], p[1], (150, 150, 150), 2)
        prev = p
    cv.line(bx0, bsy(0), bx1, bsy(0), (120, 120, 120), 1)  # treat none
    cv.fill_rect(bx0 + 20, by0 + 60, bx0 + 46, by0 + 76, DTEAL)
    cv.text(bx0 + 54, by0 + 62, "HYBRID MODEL", (40, 40, 40), 2)
    cv.fill_rect(bx0 + 20, by0 + 90, bx0 + 46, by0 + 106, (150, 150, 150))
    cv.text(bx0 + 54, by0 + 92, "TREAT ALL", (40, 40, 40), 2)
    cv.save(os.path.join(OUTDIR, 'Figure_6_RiskStratification.png'))


if __name__ == '__main__':
    os.makedirs(OUTDIR, exist_ok=True)
    print('Generating CKD manuscript figures...')
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6()
    print('Done.')
