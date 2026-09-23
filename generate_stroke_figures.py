#!/usr/bin/env python3
"""
Generate four publication-style figures for the manuscript
"Sex Differences in Early Functional Outcomes After Acute Stroke".

Pure standard library only (no matplotlib/numpy/PIL available in the sandbox).
Implements a tiny raster canvas, a 5x7 bitmap font, basic drawing primitives,
and a minimal PNG encoder (zlib + struct).
"""

import os
import zlib
import struct

OUTDIR = '/projects/sandbox/AMMAN/stroke_figures'

# ----------------------------------------------------------------------------
# 5x7 bitmap font (uppercase letters, digits, common punctuation).
# Each glyph = 7 rows of 5 columns; '#' = ink, '.' = blank.
# ----------------------------------------------------------------------------
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
    '3': ["11110","00001","00001","01110","00001","00001","11110"],
    '4': ["00010","00110","01010","10010","11111","00010","00010"],
    '5': ["11111","10000","11110","00001","00001","10001","01110"],
    '6': ["00110","01000","10000","11110","10001","10001","01110"],
    '7': ["11111","00001","00010","00100","01000","01000","01000"],
    '8': ["01110","10001","10001","01110","10001","10001","01110"],
    '9': ["01110","10001","10001","01111","00001","00010","01100"],
    ' ': ["00000","00000","00000","00000","00000","00000","00000"],
    '.': ["00000","00000","00000","00000","00000","01100","01100"],
    ',': ["00000","00000","00000","00000","01100","00100","01000"],
    '-': ["00000","00000","00000","11111","00000","00000","00000"],
    '%': ["11001","11010","00010","00100","01000","01011","10011"],
    '(': ["00010","00100","01000","01000","01000","00100","00010"],
    ')': ["01000","00100","00010","00010","00010","00100","01000"],
    ':': ["00000","01100","01100","00000","01100","01100","00000"],
    '/': ["00001","00010","00010","00100","01000","01000","10000"],
    '<': ["00010","00100","01000","10000","01000","00100","00010"],
    '>': ["01000","00100","00010","00001","00010","00100","01000"],
    '=': ["00000","00000","11111","00000","11111","00000","00000"],
    '+': ["00000","00100","00100","11111","00100","00100","00000"],
    "'": ["00100","00100","01000","00000","00000","00000","00000"],
    '[': ["01110","01000","01000","01000","01000","01000","01110"],
    ']': ["01110","00010","00010","00010","00010","00010","01110"],
}


class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w = w
        self.h = h
        self.px = [[bg for _ in range(w)] for _ in range(h)]

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = c

    def fill_rect(self, x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(self.h, y1)):
            row = self.px[y]
            for x in range(max(0, x0), min(self.w, x1)):
                row[x] = c

    def rect(self, x0, y0, x1, y1, c, t=1):
        for i in range(t):
            self.hline(x0, x1, y0 + i, c)
            self.hline(x0, x1, y1 - 1 - i, c)
            self.vline(x0 + i, y0, y1, c)
            self.vline(x1 - 1 - i, y0, y1, c)

    def hline(self, x0, x1, y, c, t=1):
        if x1 < x0:
            x0, x1 = x1, x0
        for yy in range(y, y + t):
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                self.set(x, yy, c)

    def vline(self, x, y0, y1, c, t=1):
        if y1 < y0:
            y0, y1 = y1, y0
        for xx in range(x, x + t):
            for y in range(max(0, y0), min(self.h, y1 + 1)):
                self.set(xx, y, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for ox in range(t):
                for oy in range(t):
                    self.set(x0 + ox, y0 + oy, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def text(self, x, y, s, c=(0, 0, 0), scale=2, spacing=1):
        cx = x
        for ch in s.upper():
            glyph = FONT.get(ch, FONT[' '])
            for ry, row in enumerate(glyph):
                for rx, bit in enumerate(row):
                    if bit == '1':
                        self.fill_rect(cx + rx * scale, y + ry * scale,
                                       cx + rx * scale + scale, y + ry * scale + scale, c)
            cx += (5 + spacing) * scale
        return cx

    def text_w(self, s, scale=2, spacing=1):
        return len(s) * (5 + spacing) * scale

    def text_center(self, cx, y, s, c=(0, 0, 0), scale=2, spacing=1):
        self.text(cx - self.text_w(s, scale, spacing) // 2, y, s, c, scale, spacing)

    def save_png(self, path):
        raw = bytearray()
        for row in self.px:
            raw.append(0)
            for (r, g, b) in row:
                raw += bytes((r, g, b))

        def chunk(t, d):
            c = t + d
            return struct.pack('>I', len(d)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

        sig = b'\x89PNG\r\n\x1a\n'
        ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0))
        idat = chunk(b'IDAT', zlib.compress(bytes(raw), 9))
        iend = chunk(b'IEND', b'')
        with open(path, 'wb') as f:
            f.write(sig + ihdr + idat + iend)
        print("  wrote", path)


# Palette
NAVY = (31, 59, 102)
BLUE = (46, 105, 178)
TEAL = (36, 149, 154)
CORAL = (214, 96, 77)
PLUM = (142, 68, 132)
GREY = (110, 118, 130)
LGREY = (222, 227, 234)
BLACK = (25, 28, 34)
WHITE = (255, 255, 255)
WOMEN = (198, 74, 92)     # rose
MEN = (46, 105, 178)      # blue


def rounded_box(cv, x0, y0, x1, y1, fill, border, label_lines, tcol=WHITE, scale=2):
    cv.fill_rect(x0, y0, x1, y1, fill)
    cv.rect(x0, y0, x1, y1, border, t=2)
    total_h = len(label_lines) * (7 * scale) + (len(label_lines) - 1) * (3 * scale)
    ty = (y0 + y1) // 2 - total_h // 2
    for ln in label_lines:
        cv.text_center((x0 + x1) // 2, ty, ln, tcol, scale=scale, spacing=1)
        ty += 7 * scale + 3 * scale


def arrow(cv, x0, y0, x1, y1, c=BLACK, t=2):
    cv.line(x0, y0, x1, y1, c, t=t)
    # arrowhead
    import math
    ang = math.atan2(y1 - y0, x1 - x0)
    for da in (math.radians(150), math.radians(-150)):
        hx = int(x1 + 12 * math.cos(ang + da))
        hy = int(y1 + 12 * math.sin(ang + da))
        cv.line(x1, y1, hx, hy, c, t=t)


# ----------------------------------------------------------------------------
# Figure 1: Conceptual framework
# ----------------------------------------------------------------------------
def figure1():
    W, H = 1100, 760
    cv = Canvas(W, H)
    cv.fill_rect(0, 0, W, 64, NAVY)
    cv.text_center(W // 2, 22, "FIGURE 1. CONCEPTUAL FRAMEWORK OF SEX DIFFERENCES IN EARLY OUTCOME", WHITE, scale=2)

    # Top source box
    rounded_box(cv, 420, 96, 680, 176, PLUM, PLUM, ["BIOLOGICAL SEX", "AND GENDER"], WHITE, 2)

    # Four mediator boxes
    my0, my1 = 300, 420
    boxes = [
        (60, 300, "BASELINE", ["BASELINE:", "AGE, NIHSS,", "PRE-STROKE MRS"], TEAL),
        (330, 300, "PRESENT", ["PRESENTATION", "AND", "RECOGNITION"], BLUE),
        (600, 300, "TREAT", ["ACUTE", "TREATMENT", "ACCESS"], CORAL),
        (870, 300, "BIO", ["BIOLOGICAL", "RESPONSE", "(INFLAMMATION)"], GREY),
    ]
    centers = []
    for x0, y0, _k, lines, col in boxes:
        rounded_box(cv, x0, my0, x0 + 170, my1, col, col, lines, WHITE, 2)
        centers.append((x0 + 85, my0, x0 + 85, my1))

    # arrows from source to mediators
    for cxs, top, _cxb, _bot in centers:
        arrow(cv, 550, 176, cxs, top, BLACK, 2)

    # Outcome box
    rounded_box(cv, 360, 560, 740, 660, NAVY, NAVY,
                ["EARLY FUNCTIONAL OUTCOME", "MODIFIED RANKIN SCALE (MRS)", "AT DISCHARGE AND 90 DAYS"], WHITE, 2)
    for _cxs, _top, cxb, bot in centers:
        arrow(cv, cxb, bot, 550, 560, BLACK, 2)

    cv.text_center(W // 2, 700, "CRUDE SEX GAP LARGELY MEDIATED BY BASELINE AGE AND PRE-STROKE STATUS", GREY, scale=2)
    cv.save_png(os.path.join(OUTDIR, 'Figure_1_Framework.png'))


# ----------------------------------------------------------------------------
# Generic grouped bar chart helper
# ----------------------------------------------------------------------------
def grouped_bar(cv, ox, oy, pw, ph, groups, series, ymax, ylab, colors, ytick=20):
    # axes
    cv.vline(ox, oy - ph, oy, BLACK, t=2)
    cv.hline(ox, ox + pw, oy, BLACK, t=2)
    # y gridlines + labels
    steps = int(ymax // ytick)
    for i in range(steps + 1):
        val = i * ytick
        yy = oy - int(ph * val / ymax)
        if i > 0:
            cv.hline(ox, ox + pw, yy, LGREY, t=1)
        cv.text(ox - 62, yy - 7, "%d" % val, BLACK, scale=2)
    # y axis label (vertical-ish: stacked short)
    cv.text(ox - 58, oy - ph - 34, ylab, NAVY, scale=2)

    n_groups = len(groups)
    gw = pw / n_groups
    n_series = len(series)
    bw = gw * 0.62 / n_series
    for gi, gname in enumerate(groups):
        gx = ox + gi * gw
        for si, (sname, vals) in enumerate(series):
            v = vals[gi]
            bx0 = int(gx + gw * 0.19 + si * bw)
            bx1 = int(bx0 + bw - 4)
            by = oy - int(ph * v / ymax)
            cv.fill_rect(bx0, by, bx1, oy, colors[si])
            cv.rect(bx0, by, bx1, oy, BLACK, t=1)
            cv.text_center((bx0 + bx1) // 2, by - 22, "%d" % v, BLACK, scale=2)
        # group label
        cv.text_center(int(gx + gw / 2), oy + 12, gname, BLACK, scale=2)
    return


def legend(cv, x, y, items):
    for name, col in items:
        cv.fill_rect(x, y, x + 26, y + 20, col)
        cv.rect(x, y, x + 26, y + 20, BLACK, t=1)
        cv.text(x + 34, y + 2, name, BLACK, scale=2)
        x += 34 + cv.text_w(name, 2) + 40


# ----------------------------------------------------------------------------
# Figure 2: good outcome (mRS 0-2) by sex across cohorts
# ----------------------------------------------------------------------------
def figure2():
    W, H = 1100, 720
    cv = Canvas(W, H)
    cv.fill_rect(0, 0, W, 64, NAVY)
    cv.text_center(W // 2, 22, "FIGURE 2. GOOD EARLY OUTCOME (MRS 0-2) BY SEX ACROSS COHORTS", WHITE, scale=2)

    groups = ["COHORT A", "COHORT B", "COHORT C", "POOLED"]
    women = [53, 46, 49, 50]
    men = [71, 60, 62, 64]
    grouped_bar(cv, 150, 600, 820, 460, groups,
                [("WOMEN", women), ("MEN", men)], 80,
                "PERCENT MRS 0-2", [WOMEN, MEN], ytick=20)
    legend(cv, 360, 650, [("WOMEN", WOMEN), ("MEN", MEN)])
    cv.text_center(W // 2, 686, "ILLUSTRATIVE VALUES SYNTHESISED FROM CITED SOURCES", GREY, scale=2)
    cv.save_png(os.path.join(OUTDIR, 'Figure_2_GoodOutcome.png'))


# ----------------------------------------------------------------------------
# Figure 3: forest plot of adjusted OR (female vs male)
# ----------------------------------------------------------------------------
def figure3():
    W, H = 1320, 720
    cv = Canvas(W, H)
    cv.fill_rect(0, 0, W, 64, NAVY)
    cv.text_center(W // 2, 22, "FIGURE 3. ADJUSTED ODDS OF POOR EARLY OUTCOME (WOMEN VS MEN)", WHITE, scale=2)

    # plot area maps OR 0.5 .. 2.0 on a log scale
    import math
    px0, px1 = 470, 960
    lo, hi = 0.5, 2.0
    def xof(orv):
        return int(px0 + (math.log(orv) - math.log(lo)) / (math.log(hi) - math.log(lo)) * (px1 - px0))

    rows = [
        ("CARCEL 2019 [5]", 1.20, 1.06, 1.36),
        ("WANG 2020 [8]", 1.14, 1.02, 1.28),
        ("SPAANDER 2017 [7]", 1.04, 0.86, 1.25),
        ("FIFI 2023 [10]", 1.35, 1.02, 1.79),
        ("PROMS 2023", 1.30, 1.08, 1.57),
    ]
    top = 120
    dy = 96
    # reference line at OR=1
    x1 = xof(1.0)
    cv.vline(x1, top - 30, top + dy * len(rows) - 40, GREY, t=2)
    cv.text(x1 - 8, top + dy * len(rows) - 30, "1", GREY, scale=2)
    # ticks
    for tick in (0.5, 0.75, 1.0, 1.5, 2.0):
        xt = xof(tick)
        cv.vline(xt, top + dy * len(rows) - 44, top + dy * len(rows) - 34, BLACK, t=1)
        cv.text_center(xt, top + dy * len(rows) - 24, str(tick), BLACK, scale=2)

    for i, (name, orv, lcl, ucl) in enumerate(rows):
        yy = top + i * dy
        cv.text(40, yy - 8, name, BLACK, scale=2)
        # CI line
        cv.hline(xof(lcl), xof(ucl), yy, NAVY, t=3)
        cv.vline(xof(lcl), yy - 8, yy + 8, NAVY, t=2)
        cv.vline(xof(ucl), yy - 8, yy + 8, NAVY, t=2)
        # point
        cx = xof(orv)
        cv.fill_rect(cx - 8, yy - 8, cx + 8, yy + 8, CORAL)
        cv.rect(cx - 8, yy - 8, cx + 8, yy + 8, BLACK, t=1)
        cv.text(xof(ucl) + 14, yy - 8, "%.2f (%.2f-%.2f)" % (orv, lcl, ucl), BLACK, scale=2)

    cv.text(px0 - 150, top + dy * len(rows) + 4, "FAVOURS WOMEN", GREY, scale=2)
    cv.text(px1 - 150, top + dy * len(rows) + 4, "WORSE IN WOMEN", GREY, scale=2)
    cv.save_png(os.path.join(OUTDIR, 'Figure_3_Forest.png'))


# ----------------------------------------------------------------------------
# Figure 4: acute treatment / time metrics by sex
# ----------------------------------------------------------------------------
def figure4():
    W, H = 1100, 720
    cv = Canvas(W, H)
    cv.fill_rect(0, 0, W, 64, NAVY)
    cv.text_center(W // 2, 22, "FIGURE 4. ACUTE TREATMENT AND TIME METRICS BY SEX", WHITE, scale=2)

    # Left panel: treatment rates (%)
    groups = ["IV LYSIS", "THROMBECT"]
    women = [12, 8]
    men = [16, 9]
    grouped_bar(cv, 130, 560, 380, 420, groups,
                [("WOMEN", women), ("MEN", men)], 20,
                "PERCENT TREATED", [WOMEN, MEN], ytick=5)
    cv.text_center(300, 600, "TREATMENT RATES", NAVY, scale=2)

    # Right panel: time metrics (minutes)
    groups2 = ["ONSET-DOOR", "DOOR-NEEDLE"]
    womenT = [168, 49]
    menT = [150, 48]
    grouped_bar(cv, 640, 560, 380, 420, groups2,
                [("WOMEN", womenT), ("MEN", menT)], 200,
                "MINUTES", [WOMEN, MEN], ytick=50)
    cv.text_center(820, 600, "TIME METRICS", NAVY, scale=2)

    legend(cv, 400, 650, [("WOMEN", WOMEN), ("MEN", MEN)])
    cv.text_center(W // 2, 690, "REPRESENTATIVE VALUES; GAPS NARROW IN ORGANISED STROKE SYSTEMS", GREY, scale=2)
    cv.save_png(os.path.join(OUTDIR, 'Figure_4_Treatment.png'))


if __name__ == '__main__':
    os.makedirs(OUTDIR, exist_ok=True)
    print("Generating figures ->", OUTDIR)
    figure1()
    figure2()
    figure3()
    figure4()
    print("Done.")
