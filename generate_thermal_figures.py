#!/usr/bin/env python3
"""
Generate the 7 figures for the thermal-modelling manuscript using ONLY the
Python standard library (no matplotlib/numpy). Each figure is written as a
PNG built from raw bytes. A compact 5x7 bitmap font is used for all labels.

Figures:
  1  Schematic of interrupted orthogonal machining setup
  2  Finite difference discretization of the workpiece
  3  Interior node heat-energy transfer
  4  Shear-zone temperature: FD vs analytical (light & heavy)
  5  Rake-face temperature: FD vs analytical (light & heavy)
  6  Shear-zone heat partition: FD vs analytical (light & heavy)
  7  Estimated shear-zone temperature under different MWF conditions (light)
"""

import os
import struct
import zlib

OUT_DIR = '/projects/sandbox/AMMAN/thermal_figures'

# ----------------------------------------------------------------------------
# 5x7 bitmap font (uppercase, digits, common symbols). Rows are 5-char strings.
# ----------------------------------------------------------------------------
FONT = {
    ' ': ["00000"]*7,
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
    'N': ["10001","11001","10101","10011","10001","10001","10001"],
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
    '.': ["00000","00000","00000","00000","00000","00110","00110"],
    ',': ["00000","00000","00000","00000","00110","00100","01000"],
    '(': ["00010","00100","01000","01000","01000","00100","00010"],
    ')': ["01000","00100","00010","00010","00010","00100","01000"],
    '%': ["11001","11010","00100","01011","10011","00000","00000"],
    '/': ["00001","00010","00100","00100","01000","10000","10000"],
    '-': ["00000","00000","00000","11111","00000","00000","00000"],
    '+': ["00000","00100","00100","11111","00100","00100","00000"],
    ':': ["00000","00110","00110","00000","00110","00110","00000"],
    '°': ["01100","10010","10010","01100","00000","00000","00000"],
}


class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w = w
        self.h = h
        self.px = bytearray()
        r, g, b = bg
        for _ in range(w * h):
            self.px += bytes((r, g, b))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i+3] = bytes(color)

    def fill_rect(self, x0, y0, x1, y1, color):
        for y in range(int(y0), int(y1)):
            for x in range(int(x0), int(x1)):
                self.set(x, y, color)

    def rect(self, x0, y0, x1, y1, color, t=1):
        for k in range(t):
            self.hline(x0, x1, y0 + k, color)
            self.hline(x0, x1, y1 - k, color)
            self.vline(x0 + k, y0, y1, color)
            self.vline(x1 - k, y0, y1, color)

    def hline(self, x0, x1, y, color, t=1):
        if x1 < x0:
            x0, x1 = x1, x0
        for k in range(t):
            for x in range(int(x0), int(x1) + 1):
                self.set(x, int(y) + k, color)

    def vline(self, x, y0, y1, color, t=1):
        if y1 < y0:
            y0, y1 = y1, y0
        for k in range(t):
            for y in range(int(y0), int(y1) + 1):
                self.set(int(x) + k, y, color)

    def line(self, x0, y0, x1, y1, color, t=2):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for ox in range(t):
                for oy in range(t):
                    self.set(x0 + ox, y0 + oy, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def fill_circle(self, cx, cy, r, color):
        for y in range(-r, r + 1):
            for x in range(-r, r + 1):
                if x * x + y * y <= r * r:
                    self.set(cx + x, cy + y, color)

    def marker_square(self, cx, cy, s, color):
        self.fill_rect(cx - s, cy - s, cx + s, cy + s, color)

    def text(self, x, y, s, color=(0, 0, 0), scale=2, spacing=1):
        s = s.upper()
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT[' '])
            for row in range(7):
                for col in range(5):
                    if glyph[row][col] == '1':
                        self.fill_rect(cx + col * scale, y + row * scale,
                                       cx + (col + 1) * scale, y + (row + 1) * scale,
                                       color)
            cx += (5 + spacing) * scale
        return cx

    def text_vertical(self, x, y, s, color=(0, 0, 0), scale=2, spacing=1):
        """Draw text rotated 90° CCW, growing upward from (x, y)."""
        s = s.upper()
        cy = y
        for ch in s:
            glyph = FONT.get(ch, FONT[' '])
            for row in range(7):
                for col in range(5):
                    if glyph[row][col] == '1':
                        # rotate: (col,row) -> plot with row along x, col along y
                        px = x + row * scale
                        py = cy - col * scale
                        self.fill_rect(px, py, px + scale, py + scale, color)
            cy -= (5 + spacing) * scale
        return cy

    def text_width(self, s, scale=2, spacing=1):
        return len(s) * (5 + spacing) * scale

    def save(self, path):
        def chunk(ctype, data):
            c = ctype + data
            return (struct.pack('>I', len(data)) + c +
                    struct.pack('>I', zlib.crc32(c) & 0xffffffff))
        sig = b'\x89PNG\r\n\x1a\n'
        ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0))
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)
            raw += self.px[y * self.w * 3:(y + 1) * self.w * 3]
        idat = chunk(b'IDAT', zlib.compress(bytes(raw), 9))
        iend = chunk(b'IEND', b'')
        with open(path, 'wb') as f:
            f.write(sig + ihdr + idat + iend)
        print(f'  wrote {path} ({self.w}x{self.h})')


BLUE = (31, 119, 180)
ORANGE = (255, 127, 14)
GREEN = (44, 160, 44)
RED = (214, 39, 40)
PURPLE = (148, 103, 189)
BROWN = (140, 86, 75)
GRAY = (110, 110, 110)
LGRAY = (200, 200, 200)
BLACK = (20, 20, 20)
STEEL = (150, 165, 180)


def line_panel(cv, x0, y0, w, h, series, ymin, ymax, ystep,
               xlabels, xlabel, ylabel, title):
    """Draw a single line chart panel inside the canvas."""
    pad_l, pad_b, pad_t = 52, 40, 34
    ax0 = x0 + pad_l
    ay0 = y0 + pad_t
    ax1 = x0 + w - 12
    ay1 = y0 + h - pad_b
    # title
    cv.text(x0 + (w - cv.text_width(title, 2)) // 2, y0 + 6, title, BLACK, 2)
    # gridlines + y ticks
    steps = int(round((ymax - ymin) / ystep))
    for k in range(steps + 1):
        val = ymin + k * ystep
        yy = ay1 - (ay1 - ay0) * (val - ymin) / (ymax - ymin)
        cv.hline(ax0, ax1, yy, LGRAY)
        lbl = _fmt(val)
        cv.text(ax0 - cv.text_width(lbl, 1) - 6, int(yy) - 4, lbl, BLACK, 1)
    # axes
    cv.vline(ax0, ay0, ay1, BLACK, 2)
    cv.hline(ax0, ax1, ay1, BLACK, 2)
    # x positions
    n = len(xlabels)
    xs = [ax0 + (ax1 - ax0) * (i + 0.5) / n for i in range(n)]
    for i, xl in enumerate(xlabels):
        cv.text(int(xs[i]) - cv.text_width(xl, 1) // 2, ay1 + 6, xl, BLACK, 1)
    # data
    for s in series:
        col = s['color']
        pts = []
        for i, v in enumerate(s['data']):
            yy = ay1 - (ay1 - ay0) * (v - ymin) / (ymax - ymin)
            pts.append((int(xs[i]), int(yy)))
        for a, b in zip(pts, pts[1:]):
            cv.line(a[0], a[1], b[0], b[1], col, 2)
        for (px, py) in pts:
            if s.get('marker') == 'square':
                cv.marker_square(px, py, 4, col)
            else:
                cv.fill_circle(px, py, 4, col)
    # x axis label
    cv.text(x0 + (w - cv.text_width(xlabel, 1)) // 2, ay1 + 20, xlabel, BLACK, 1)
    # y axis label (vertical)
    cv.text_vertical(x0 + 6, (ay0 + ay1) // 2 + cv.text_width(ylabel, 1) // 2,
                     ylabel, BLACK, 1)
    # legend
    lx = ax0 + 8
    ly = ay0 + 6
    for s in series:
        cv.fill_rect(lx, ly, lx + 14, ly + 8, s['color'])
        cv.text(lx + 18, ly - 1, s['name'], BLACK, 1)
        ly += 16


def _fmt(v):
    if abs(v - round(v)) < 1e-6:
        return str(int(round(v)))
    return f'{v:.1f}'


# ----------------------------------------------------------------------------
# Figure 1 — schematic of machining setup
# ----------------------------------------------------------------------------
def fig1():
    cv = Canvas(940, 500)
    cv.text(16, 12, 'Figure 1  Interrupted orthogonal machining (peripheral down milling)', BLACK, 2)
    # dynamometer base
    cv.fill_rect(120, 360, 520, 430, (225, 225, 225))
    cv.rect(120, 360, 520, 430, BLACK, 2)
    cv.text(250, 388, 'Dynamometer / fixture', BLACK, 2)
    # workpiece slab
    cv.fill_rect(150, 300, 490, 360, STEEL)
    cv.rect(150, 300, 490, 360, BLACK, 2)
    cv.text(190, 322, 'Workpiece (AISI 1055)', BLACK, 2)
    # thermocouple location (label placed low-left to avoid the jet)
    cv.fill_circle(360, 348, 5, RED)
    cv.line(360, 348, 250, 452, RED, 2)
    cv.text(150, 456, 'K-type thermocouple (3 mm below surface)', RED, 1)
    # rotating cutter
    cx, cy, R = 560, 250, 60
    cv.fill_circle(cx, cy, R, (235, 235, 235))
    for ang in range(0, 360, 90):
        import math
        a = math.radians(ang)
        cv.line(cx, cy, cx + int(R * math.cos(a)), cy + int(R * math.sin(a)), GRAY, 2)
    cv.fill_circle(cx, cy, 6, BLACK)
    # single insert
    cv.fill_rect(cx - 8, cy + R - 6, cx + 8, cy + R + 8, BLACK)
    cv.text(cx - 24, cy - 100, 'Milling cutter', BLACK, 2)
    cv.text(cx + 70, cy, '(single insert)', BLACK, 1)
    # feed arrow
    cv.line(160, 285, 320, 285, BLACK, 3)
    cv.line(320, 285, 305, 278, BLACK, 3)
    cv.line(320, 285, 305, 292, BLACK, 3)
    cv.text(180, 262, 'Feed / table travel', BLACK, 2)
    # MQL nozzle + jet
    cv.fill_rect(690, 300, 760, 322, (180, 200, 220))
    cv.rect(690, 300, 760, 322, BLACK, 2)
    cv.text(700, 340, 'MQL nozzle', BLACK, 2)
    for dx in range(0, 130, 12):
        cv.fill_circle(690 - dx, 311 - dx // 3, 2, (90, 130, 190))
    cv.text(640, 200, 'Atomized MQL jet', (60, 100, 170), 2)
    cv.save(os.path.join(OUT_DIR, 'Figure_1_Setup.png'))


# ----------------------------------------------------------------------------
# Figure 2 — FD discretization of workpiece
# ----------------------------------------------------------------------------
def fig2():
    cv = Canvas(900, 500)
    cv.text(20, 12, 'Figure 2  Finite difference discretization of the workpiece', BLACK, 2)
    gx0, gy0, gx1, gy1 = 120, 150, 760, 380
    cv.fill_rect(gx0, gy0, gx1, gy1, (245, 245, 245))
    # grid
    cols, rows = 32, 12
    for c in range(cols + 1):
        x = gx0 + (gx1 - gx0) * c // cols
        cv.vline(x, gy0, gy1, LGRAY)
    for r in range(rows + 1):
        y = gy0 + (gy1 - gy0) * r // rows
        cv.hline(gx0, gx1, y, LGRAY)
    cv.rect(gx0, gy0, gx1, gy1, BLACK, 2)
    # convection arrows on top
    for x in range(gx0 + 10, gx1, 40):
        cv.line(x, gy0 - 26, x, gy0 - 4, BLUE, 2)
        cv.line(x, gy0 - 4, x - 4, gy0 - 12, BLUE, 2)
        cv.line(x, gy0 - 4, x + 4, gy0 - 12, BLUE, 2)
    cv.text(gx0, gy0 - 48, 'Convective heat loss from top face', BLUE, 1)
    # moving heat source
    sx = gx0 + 160
    cv.fill_rect(sx - 14, gy0, sx + 14, gy0 + 18, RED)
    cv.line(sx, gy0 - 60, sx, gy0 - 2, RED, 3)
    cv.line(sx, gy0 - 2, sx - 6, gy0 - 14, RED, 3)
    cv.line(sx, gy0 - 2, sx + 6, gy0 - 14, RED, 3)
    cv.text(sx + 8, gy0 - 78, 'Moving heat source (q)', RED, 1)
    # feed direction
    cv.line(sx, gy0 - 92, sx + 120, gy0 - 92, BLACK, 2)
    cv.line(sx + 120, gy0 - 92, sx + 108, gy0 - 98, BLACK, 2)
    cv.line(sx + 120, gy0 - 92, sx + 108, gy0 - 86, BLACK, 2)
    cv.text(sx + 20, gy0 - 112, 'Feed (X) direction', BLACK, 1)
    # thermocouple
    tx = gx0 + 220
    ty = gy0 + (gy1 - gy0) // 3
    cv.fill_circle(tx, ty, 5, RED)
    cv.text(tx + 10, ty - 4, 'Thermocouple node', RED, 1)
    # ambient labels
    cv.text_vertical(gx0 - 30, (gy0 + gy1) // 2 + 60, 'Ambient T', GRAY, 1)
    cv.text_vertical(gx1 + 14, (gy0 + gy1) // 2 + 60, 'Ambient T', GRAY, 1)
    cv.text((gx0 + gx1) // 2 - 40, gy1 + 12, 'Ambient T (bottom)', GRAY, 1)
    # dimensions
    cv.text((gx0 + gx1) // 2 - 30, gy1 + 34, '30 mm  x  8 mm domain', BLACK, 1)
    cv.save(os.path.join(OUT_DIR, 'Figure_2_Discretization.png'))


# ----------------------------------------------------------------------------
# Figure 3 — interior node
# ----------------------------------------------------------------------------
def fig3():
    cv = Canvas(760, 500)
    cv.text(20, 12, 'Figure 3  Heat energy transfer to an interior node (i, j)', BLACK, 2)
    cx, cy, d = 380, 270, 120
    nodes = {
        '(i, j)': (cx, cy),
        '(i, j+1)': (cx, cy - d),
        '(i, j-1)': (cx, cy + d),
        '(i-1, j)': (cx - d, cy),
        '(i+1, j)': (cx + d, cy),
    }
    # arrows toward center
    for key, (nx, ny) in nodes.items():
        if key == '(i, j)':
            continue
        cv.line(nx, ny, cx + (1 if nx < cx else -1 if nx > cx else 0) * 20,
                cy + (1 if ny < cy else -1 if ny > cy else 0) * 20, GRAY, 2)
    for key, (nx, ny) in nodes.items():
        col = RED if key == '(i, j)' else BLUE
        cv.fill_circle(nx, ny, 7, col)
        cv.text(nx - cv.text_width(key, 1) // 2, ny + 14, key, BLACK, 1)
    # dx dy indicators
    cv.line(cx + 20, cy + d + 40, cx + d - 20, cy + d + 40, BLACK, 2)
    cv.text(cx + 40, cy + d + 46, 'dx', BLACK, 1)
    cv.line(cx + d + 40, cy + 20, cx + d + 40, cy + d - 20, BLACK, 2)
    cv.text(cx + d + 46, cy + 50, 'dy', BLACK, 1)
    cv.save(os.path.join(OUT_DIR, 'Figure_3_InteriorNode.png'))


# ----------------------------------------------------------------------------
# Figures 4, 5, 6 — two-panel FD vs analytical comparisons
# ----------------------------------------------------------------------------
def two_panel(fname, title, ylabel, ymin, ymax, ystep,
              fd_light, an_light, fd_heavy, an_heavy):
    cv = Canvas(980, 460)
    cv.text(20, 10, title, BLACK, 2)
    xl = ['150', '200', '250']
    sA = [
        {'name': 'FD model', 'data': fd_light, 'color': BLUE, 'marker': 'circle'},
        {'name': 'Analytical', 'data': an_light, 'color': ORANGE, 'marker': 'square'},
    ]
    sB = [
        {'name': 'FD model', 'data': fd_heavy, 'color': BLUE, 'marker': 'circle'},
        {'name': 'Analytical', 'data': an_heavy, 'color': ORANGE, 'marker': 'square'},
    ]
    line_panel(cv, 10, 34, 480, 420, sA, ymin, ymax, ystep, xl,
               'Cutting speed (m/min)', ylabel, '(a) Light machining')
    line_panel(cv, 495, 34, 480, 420, sB, ymin, ymax, ystep, xl,
               'Cutting speed (m/min)', ylabel, '(b) Heavy machining')
    cv.save(os.path.join(OUT_DIR, fname))


def fig4():
    two_panel('Figure_4_ShearZoneTemp.png',
              'Figure 4  Average shear-zone temperature: FD model vs analytical',
              'Shear zone temp (C)', 0, 500, 100,
              [255, 350, 335], [145, 158, 180],
              [408, 402, 378], [160, 150, 143])


def fig5():
    two_panel('Figure_5_RakeFaceTemp.png',
              'Figure 5  Average rake-face temperature: FD model vs analytical',
              'Rake face temp (C)', 200, 600, 100,
              [415, 405, 510], [315, 372, 438],
              [446, 446, 452], [460, 470, 470])


def fig6():
    two_panel('Figure_6_HeatPartition.png',
              'Figure 6  Shear-zone heat partition: FD model vs analytical',
              'Heat partition ratio', 0, 0.7, 0.1,
              [0.64, 0.46, 0.59], [0.37, 0.38, 0.41],
              [0.49, 0.50, 0.51], [0.53, 0.57, 0.59])


# ----------------------------------------------------------------------------
# Figure 7 — estimated shear-zone temperature under different MWF (light)
# ----------------------------------------------------------------------------
def fig7():
    cv = Canvas(900, 520)
    cv.text(20, 10, 'Figure 7  Estimated shear-zone temperature under different MWF (light machining)', BLACK, 2)
    xl = ['150', '200', '250']
    series = [
        {'name': 'DRY', 'data': [255, 350, 338], 'color': BLUE, 'marker': 'circle'},
        {'name': 'OIL', 'data': [225, 325, 310], 'color': ORANGE, 'marker': 'square'},
        {'name': 'IL1', 'data': [210, 322, 362], 'color': GRAY, 'marker': 'circle'},
        {'name': 'PEG', 'data': [128, 328, 315], 'color': GREEN, 'marker': 'square'},
        {'name': 'PEG+IL1', 'data': [205, 308, 340], 'color': RED, 'marker': 'circle'},
        {'name': 'IL308(1%)', 'data': [205, 295, 315], 'color': PURPLE, 'marker': 'square'},
        {'name': 'IL308(0.5%)', 'data': [212, 308, 345], 'color': BROWN, 'marker': 'circle'},
    ]
    line_panel(cv, 10, 40, 880, 460, series, 100, 400, 50, xl,
               'Cutting speed (m/min)', 'Shear zone temp (C)',
               'Estimated shear-zone temperature (MQL, light cut)')
    cv.save(os.path.join(OUT_DIR, 'Figure_7_MWF_Temps.png'))


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    print('Generating thermal-modelling figures...')
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); fig7()
    print('Done.')
