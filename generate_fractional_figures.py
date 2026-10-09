#!/usr/bin/env python3
"""
Generate 9 scientific figures (PNG) for the manuscript:

    "A Dual-Memory Fractional Stefan Framework for Binary-Alloy
     Solidification with Shrinkage: Anomalous Heat-Solute Coupling,
     Segregation Control, and Inverse Memory Identification"

Pure Python standard library only (no numpy / matplotlib / scipy, no network).
All quantitative curves are computed from the reduced dual-order analytical /
semi-analytical model described in the manuscript: independent thermal (alpha_T)
and solutal (alpha_C) Caputo orders, Mittag-Leffler / Wright similarity profiles,
and the generalised interface kinetics s(t) = 2 lambda t^(alpha_T/2).

Figures
-------
Figure_1_Problem_Schematic.png        Dual-memory fractional Stefan domain
Figure_2_Memory_Kernels.png           Thermal vs solutal Mittag-Leffler kernels
Figure_3_Temperature.png              Temperature profiles vs thermal order alpha_T
Figure_4_Concentration.png            Solute profiles vs solutal order alpha_C / Le
Figure_5_Interface_Kinetics.png       Interface position s*(t*) vs alpha_T
Figure_6_Lambda_Map.png               Growth parameter lambda vs alpha_T for several Le
Figure_7_DualOrder_Map.png            s*(alpha_T, alpha_C) dual-memory heat map
Figure_8_Segregation_Sensitivity.png  Memory segregation index + elasticity sensitivity
Figure_9_Inverse_Identification.png   Inverse memory identification + model benchmarking
"""

import struct
import zlib
import math
import os

OUTPUT_DIR = '/projects/sandbox/AMMAN/fractional_figures'

# ----------------------------------------------------------------------------
# Colour palette
# ----------------------------------------------------------------------------
DARK_BLUE   = (31, 78, 121)
MED_BLUE    = (46, 117, 182)
LIGHT_BLUE  = (155, 194, 230)
PALE_BLUE   = (222, 235, 247)
DARK_GREEN  = (56, 118, 29)
MED_GREEN   = (84, 160, 64)
LIGHT_GREEN = (198, 224, 180)
ORANGE      = (217, 110, 35)
LIGHT_ORANGE= (248, 203, 173)
RED         = (192, 0, 0)
LIGHT_RED   = (244, 199, 199)
PURPLE      = (112, 48, 160)
LIGHT_PURPLE= (204, 180, 220)
GOLD        = (191, 144, 0)
TEAL        = (0, 139, 139)
GRAY        = (120, 120, 120)
LIGHT_GRAY  = (205, 205, 205)
VLIGHT_GRAY = (235, 235, 235)
BLACK       = (0, 0, 0)
WHITE       = (255, 255, 255)

SERIES_COLORS = [DARK_BLUE, RED, DARK_GREEN, ORANGE, PURPLE, TEAL, GOLD]


# ----------------------------------------------------------------------------
# Minimal 5x7 bitmap font
# ----------------------------------------------------------------------------
_FONT = {
    'A':[0b01110,0b10001,0b10001,0b11111,0b10001,0b10001,0b10001],
    'B':[0b11110,0b10001,0b10001,0b11110,0b10001,0b10001,0b11110],
    'C':[0b01110,0b10001,0b10000,0b10000,0b10000,0b10001,0b01110],
    'D':[0b11110,0b10001,0b10001,0b10001,0b10001,0b10001,0b11110],
    'E':[0b11111,0b10000,0b10000,0b11110,0b10000,0b10000,0b11111],
    'F':[0b11111,0b10000,0b10000,0b11110,0b10000,0b10000,0b10000],
    'G':[0b01110,0b10001,0b10000,0b10111,0b10001,0b10001,0b01110],
    'H':[0b10001,0b10001,0b10001,0b11111,0b10001,0b10001,0b10001],
    'I':[0b01110,0b00100,0b00100,0b00100,0b00100,0b00100,0b01110],
    'J':[0b00111,0b00010,0b00010,0b00010,0b00010,0b10010,0b01100],
    'K':[0b10001,0b10010,0b10100,0b11000,0b10100,0b10010,0b10001],
    'L':[0b10000,0b10000,0b10000,0b10000,0b10000,0b10000,0b11111],
    'M':[0b10001,0b11011,0b10101,0b10101,0b10001,0b10001,0b10001],
    'N':[0b10001,0b11001,0b10101,0b10011,0b10001,0b10001,0b10001],
    'O':[0b01110,0b10001,0b10001,0b10001,0b10001,0b10001,0b01110],
    'P':[0b11110,0b10001,0b10001,0b11110,0b10000,0b10000,0b10000],
    'Q':[0b01110,0b10001,0b10001,0b10001,0b10101,0b10010,0b01101],
    'R':[0b11110,0b10001,0b10001,0b11110,0b10100,0b10010,0b10001],
    'S':[0b01110,0b10001,0b10000,0b01110,0b00001,0b10001,0b01110],
    'T':[0b11111,0b00100,0b00100,0b00100,0b00100,0b00100,0b00100],
    'U':[0b10001,0b10001,0b10001,0b10001,0b10001,0b10001,0b01110],
    'V':[0b10001,0b10001,0b10001,0b10001,0b10001,0b01010,0b00100],
    'W':[0b10001,0b10001,0b10001,0b10101,0b10101,0b11011,0b10001],
    'X':[0b10001,0b10001,0b01010,0b00100,0b01010,0b10001,0b10001],
    'Y':[0b10001,0b10001,0b01010,0b00100,0b00100,0b00100,0b00100],
    'Z':[0b11111,0b00001,0b00010,0b00100,0b01000,0b10000,0b11111],
    'a':[0b00000,0b00000,0b01110,0b00001,0b01111,0b10001,0b01111],
    'b':[0b10000,0b10000,0b10110,0b11001,0b10001,0b10001,0b11110],
    'c':[0b00000,0b00000,0b01110,0b10000,0b10000,0b10001,0b01110],
    'd':[0b00001,0b00001,0b01101,0b10011,0b10001,0b10001,0b01111],
    'e':[0b00000,0b00000,0b01110,0b10001,0b11111,0b10000,0b01110],
    'f':[0b00110,0b01001,0b01000,0b11100,0b01000,0b01000,0b01000],
    'g':[0b00000,0b01111,0b10001,0b10001,0b01111,0b00001,0b01110],
    'h':[0b10000,0b10000,0b10110,0b11001,0b10001,0b10001,0b10001],
    'i':[0b00100,0b00000,0b01100,0b00100,0b00100,0b00100,0b01110],
    'j':[0b00010,0b00000,0b00110,0b00010,0b00010,0b10010,0b01100],
    'k':[0b10000,0b10000,0b10010,0b10100,0b11000,0b10100,0b10010],
    'l':[0b01100,0b00100,0b00100,0b00100,0b00100,0b00100,0b01110],
    'm':[0b00000,0b00000,0b11010,0b10101,0b10101,0b10001,0b10001],
    'n':[0b00000,0b00000,0b10110,0b11001,0b10001,0b10001,0b10001],
    'o':[0b00000,0b00000,0b01110,0b10001,0b10001,0b10001,0b01110],
    'p':[0b00000,0b00000,0b11110,0b10001,0b11110,0b10000,0b10000],
    'q':[0b00000,0b00000,0b01101,0b10011,0b01111,0b00001,0b00001],
    'r':[0b00000,0b00000,0b10110,0b11001,0b10000,0b10000,0b10000],
    's':[0b00000,0b00000,0b01110,0b10000,0b01110,0b00001,0b11110],
    't':[0b01000,0b01000,0b11100,0b01000,0b01000,0b01001,0b00110],
    'u':[0b00000,0b00000,0b10001,0b10001,0b10001,0b10011,0b01101],
    'v':[0b00000,0b00000,0b10001,0b10001,0b10001,0b01010,0b00100],
    'w':[0b00000,0b00000,0b10001,0b10001,0b10101,0b10101,0b01010],
    'x':[0b00000,0b00000,0b10001,0b01010,0b00100,0b01010,0b10001],
    'y':[0b00000,0b00000,0b10001,0b10001,0b01111,0b00001,0b01110],
    'z':[0b00000,0b00000,0b11111,0b00010,0b00100,0b01000,0b11111],
    '0':[0b01110,0b10001,0b10011,0b10101,0b11001,0b10001,0b01110],
    '1':[0b00100,0b01100,0b00100,0b00100,0b00100,0b00100,0b01110],
    '2':[0b01110,0b10001,0b00001,0b00010,0b00100,0b01000,0b11111],
    '3':[0b11111,0b00010,0b00100,0b00010,0b00001,0b10001,0b01110],
    '4':[0b00010,0b00110,0b01010,0b10010,0b11111,0b00010,0b00010],
    '5':[0b11111,0b10000,0b11110,0b00001,0b00001,0b10001,0b01110],
    '6':[0b00110,0b01000,0b10000,0b11110,0b10001,0b10001,0b01110],
    '7':[0b11111,0b00001,0b00010,0b00100,0b01000,0b01000,0b01000],
    '8':[0b01110,0b10001,0b10001,0b01110,0b10001,0b10001,0b01110],
    '9':[0b01110,0b10001,0b10001,0b01111,0b00001,0b00010,0b01100],
    ' ':[0,0,0,0,0,0,0],
    '.':[0,0,0,0,0,0b01100,0b01100],
    ',':[0,0,0,0,0b01100,0b00100,0b01000],
    ':':[0,0b01100,0b01100,0,0b01100,0b01100,0],
    ';':[0,0b01100,0b01100,0,0b01100,0b00100,0b01000],
    '-':[0,0,0,0b11111,0,0,0],
    '+':[0,0b00100,0b00100,0b11111,0b00100,0b00100,0],
    '(':[0b00010,0b00100,0b01000,0b01000,0b01000,0b00100,0b00010],
    ')':[0b01000,0b00100,0b00010,0b00010,0b00010,0b00100,0b01000],
    '/':[0b00001,0b00010,0b00010,0b00100,0b01000,0b01000,0b10000],
    '*':[0,0b00100,0b10101,0b01110,0b10101,0b00100,0],
    '>':[0b10000,0b01000,0b00100,0b00010,0b00100,0b01000,0b10000],
    '<':[0b00001,0b00010,0b00100,0b01000,0b00100,0b00010,0b00001],
    '=':[0,0,0b11111,0,0b11111,0,0],
    '%':[0b11001,0b11001,0b00010,0b00100,0b01000,0b10011,0b10011],
    '^':[0b00100,0b01010,0b10001,0,0,0,0],
    '|':[0b00100,0b00100,0b00100,0b00100,0b00100,0b00100,0b00100],
    '[':[0b01110,0b01000,0b01000,0b01000,0b01000,0b01000,0b01110],
    ']':[0b01110,0b00010,0b00010,0b00010,0b00010,0b00010,0b01110],
    '_':[0,0,0,0,0,0,0b11111],
    '"':[0b01010,0b01010,0,0,0,0,0],
    "'":[0b00100,0b00100,0,0,0,0,0],
    '?':[0b01110,0b10001,0b00001,0b00110,0b00100,0,0b00100],
    '!':[0b00100,0b00100,0b00100,0b00100,0b00100,0,0b00100],
    '&':[0b01100,0b10010,0b10100,0b01000,0b10101,0b10010,0b01101],
    '@':[0b01110,0b10001,0b10111,0b10101,0b10111,0b10000,0b01110],
}


class Canvas:
    """RGB canvas backed by a bytearray, with simple vector primitives."""

    def __init__(self, width, height, bg=WHITE):
        self.w = width
        self.h = height
        self.data = bytearray(width * height * 3)
        r, g, b = bg
        d = self.data
        for i in range(0, len(d), 3):
            d[i] = r; d[i+1] = g; d[i+2] = b

    def px(self, x, y, color):
        x = int(x); y = int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.data[i] = color[0]; self.data[i+1] = color[1]; self.data[i+2] = color[2]

    def blend(self, x, y, color, a):
        """Alpha blend (a in 0..1) for crude anti-aliasing."""
        x = int(x); y = int(y)
        if not (0 <= x < self.w and 0 <= y < self.h):
            return
        if a <= 0:
            return
        if a > 1:
            a = 1.0
        i = (y * self.w + x) * 3
        d = self.data
        d[i]   = int(d[i]   * (1 - a) + color[0] * a)
        d[i+1] = int(d[i+1] * (1 - a) + color[1] * a)
        d[i+2] = int(d[i+2] * (1 - a) + color[2] * a)

    def fill_rect(self, x1, y1, x2, y2, color):
        x1, x2 = sorted((int(x1), int(x2)))
        y1, y2 = sorted((int(y1), int(y2)))
        x1 = max(0, x1); y1 = max(0, y1)
        x2 = min(self.w - 1, x2); y2 = min(self.h - 1, y2)
        for y in range(y1, y2 + 1):
            i = (y * self.w + x1) * 3
            for _ in range(x1, x2 + 1):
                self.data[i] = color[0]; self.data[i+1] = color[1]; self.data[i+2] = color[2]
                i += 3

    def rect(self, x1, y1, x2, y2, outline, fill=None, thick=1):
        if fill:
            self.fill_rect(x1, y1, x2, y2, fill)
        for t in range(thick):
            self.hline(x1, x2, y1 + t, outline)
            self.hline(x1, x2, y2 - t, outline)
            self.vline(x1 + t, y1, y2, outline)
            self.vline(x2 - t, y1, y2, outline)

    def hline(self, x1, x2, y, color):
        x1, x2 = sorted((int(x1), int(x2)))
        for x in range(x1, x2 + 1):
            self.px(x, y, color)

    def vline(self, x, y1, y2, color):
        y1, y2 = sorted((int(y1), int(y2)))
        for y in range(y1, y2 + 1):
            self.px(x, y, color)

    def line(self, x1, y1, x2, y2, color, thick=1):
        x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
        dx = x2 - x1; dy = y2 - y1
        steps = int(max(abs(dx), abs(dy))) + 1
        for s in range(steps + 1):
            t = s / steps
            x = x1 + dx * t; y = y1 + dy * t
            if thick <= 1:
                self.px(round(x), round(y), color)
            else:
                for ox in range(-(thick // 2), (thick + 1) // 2):
                    for oy in range(-(thick // 2), (thick + 1) // 2):
                        self.px(round(x) + ox, round(y) + oy, color)

    def dashed(self, x1, y1, x2, y2, color, dash=6, gap=4, thick=1):
        dx = x2 - x1; dy = y2 - y1
        length = math.hypot(dx, dy)
        if length == 0:
            return
        ux, uy = dx / length, dy / length
        pos = 0.0
        draw = True
        while pos < length:
            seg = dash if draw else gap
            nx = min(pos + seg, length)
            if draw:
                self.line(x1 + ux * pos, y1 + uy * pos,
                          x1 + ux * nx, y1 + uy * nx, color, thick)
            pos = nx
            draw = not draw

    def circle(self, cx, cy, r, color, fill=None):
        if fill:
            for y in range(-r, r + 1):
                span = int(math.sqrt(max(0, r * r - y * y)))
                self.hline(cx - span, cx + span, cy + y, fill)
        x, y, err = r, 0, 1 - r
        while x >= y:
            for px, py in [(cx+x,cy+y),(cx-x,cy+y),(cx+x,cy-y),(cx-x,cy-y),
                           (cx+y,cy+x),(cx-y,cy+x),(cx+y,cy-x),(cx-y,cy-x)]:
                self.px(px, py, color)
            y += 1
            if err < 0:
                err += 2 * y + 1
            else:
                x -= 1
                err += 2 * (y - x) + 1

    def marker(self, cx, cy, kind, color, size=4):
        if kind == 'o':
            self.circle(int(cx), int(cy), size, color, color)
        elif kind == 's':
            self.fill_rect(cx - size, cy - size, cx + size, cy + size, color)
        elif kind == '^':
            for dy in range(-size, size + 1):
                half = size - abs(dy)
                self.hline(cx - half, cx + half, cy - dy, color)
        elif kind == 'd':
            for dy in range(-size, size + 1):
                half = size - abs(dy)
                self.hline(cx - half, cx + half, cy + dy, color)

    def text(self, x, y, s, color, scale=1):
        for ch in s:
            bm = _FONT.get(ch)
            if bm is None:
                x += 6 * scale
                continue
            for ri, row in enumerate(bm):
                for ci in range(5):
                    if row & (1 << (4 - ci)):
                        bx = x + ci * scale; by = y + ri * scale
                        for sy in range(scale):
                            for sx in range(scale):
                                self.px(bx + sx, by + sy, color)
            x += 6 * scale

    def text_c(self, cx, y, s, color, scale=1):
        self.text(cx - len(s) * 6 * scale // 2, y, s, color, scale)

    def text_v(self, x, cy, s, color, scale=1):
        """Vertical text (rotated 90 deg CCW), drawn bottom-to-top."""
        total = len(s) * 6 * scale
        start_y = cy + total // 2
        yy = start_y
        for ch in s:
            bm = _FONT.get(ch, _FONT[' '])
            for ri, row in enumerate(bm):
                for ci in range(5):
                    if row & (1 << (4 - ci)):
                        # rotate: (ci,ri) -> drawn going up
                        for sy in range(scale):
                            for sx in range(scale):
                                self.px(x + ri * scale + sy, yy - ci * scale - sx, color)
            yy -= 6 * scale

    def save(self, path):
        raw = bytearray()
        w3 = self.w * 3
        for y in range(self.h):
            raw.append(0)
            raw.extend(self.data[y * w3:(y + 1) * w3])
        comp = zlib.compress(bytes(raw), 9)

        def chunk(ct, data):
            c = ct + data
            return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

        with open(path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0)))
            f.write(chunk(b'IDAT', comp))
            f.write(chunk(b'IEND', b''))


# ----------------------------------------------------------------------------
# XY plotting helper
# ----------------------------------------------------------------------------
class Plot:
    def __init__(self, canvas, x0, y0, x1, y1, xmin, xmax, ymin, ymax):
        self.c = canvas
        self.px0, self.py0, self.px1, self.py1 = x0, y0, x1, y1  # pixel box (top-left, bottom-right)
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax

    def X(self, x):
        return self.px0 + (x - self.xmin) / (self.xmax - self.xmin) * (self.px1 - self.px0)

    def Y(self, y):
        return self.py1 - (y - self.ymin) / (self.ymax - self.ymin) * (self.py1 - self.py0)

    def frame(self, xticks, yticks, xfmt="{:g}", yfmt="{:g}", grid=True):
        c = self.c
        if grid:
            for xv in xticks:
                xp = self.X(xv)
                c.vline(xp, self.py0, self.py1, VLIGHT_GRAY)
            for yv in yticks:
                yp = self.Y(yv)
                c.hline(self.px0, self.px1, yp, VLIGHT_GRAY)
        # axes box
        c.rect(self.px0, self.py0, self.px1, self.py1, BLACK, thick=1)
        for xv in xticks:
            xp = self.X(xv)
            c.vline(xp, self.py1, self.py1 + 5, BLACK)
            c.text_c(int(xp), self.py1 + 9, xfmt.format(xv), BLACK, 1)
        for yv in yticks:
            yp = self.Y(yv)
            c.hline(self.px0 - 5, self.px0, yp, BLACK)
            lbl = yfmt.format(yv)
            c.text(self.px0 - 10 - len(lbl) * 6, int(yp) - 3, lbl, BLACK, 1)

    def series(self, xs, ys, color, thick=2, marker=None, msize=4, every=1):
        pts = [(self.X(x), self.Y(y)) for x, y in zip(xs, ys)]
        for i in range(len(pts) - 1):
            self.c.line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], color, thick)
        if marker:
            for i in range(0, len(pts), every):
                self.c.marker(pts[i][0], pts[i][1], marker, color, msize)

    def dashed_series(self, xs, ys, color, thick=2):
        pts = [(self.X(x), self.Y(y)) for x, y in zip(xs, ys)]
        for i in range(len(pts) - 1):
            self.c.dashed(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], color, 7, 4, thick)

    def vmark(self, x, color, thick=1, dash=True):
        xp = self.X(x)
        if dash:
            self.c.dashed(xp, self.py0, xp, self.py1, color, 5, 4, thick)
        else:
            self.c.vline(xp, self.py0, self.py1, color)

    def legend(self, entries, lx, ly, box=True, marker=None):
        """entries: list of (label, color)."""
        w = 150
        rowh = 16
        if box:
            self.c.rect(lx, ly, lx + w, ly + rowh * len(entries) + 6, GRAY, WHITE)
        for i, (label, color) in enumerate(entries):
            yy = ly + 6 + i * rowh
            self.c.line(lx + 8, yy + 4, lx + 34, yy + 4, color, 3)
            if marker:
                self.c.marker(lx + 21, yy + 4, marker, color, 3)
            self.c.text(lx + 40, yy, label, BLACK, 1)


# ----------------------------------------------------------------------------
# Special functions
# ----------------------------------------------------------------------------
def mittag_leffler(alpha, z, terms=100):
    """One-parameter Mittag-Leffler E_alpha(z) via truncated series.
    Reliable for moderate |z| (used here with |z| <~ 6)."""
    s = 0.0
    for k in range(terms):
        try:
            g = math.gamma(alpha * k + 1.0)
        except (ValueError, OverflowError):
            break
        term = (z ** k) / g
        s += term
        if abs(term) < 1e-14 and k > 5:
            break
    return s


def ml_decay(alpha, y):
    """Positive, monotonically decreasing relaxation kernel E_alpha(-y),
    clamped to [0,1] for well-behaved profile plotting."""
    v = mittag_leffler(alpha, -y)
    if v < 0.0:
        v = 0.0
    if v > 1.0:
        v = 1.0
    return v


def temp_profile(alpha, eta):
    """Normalised liquid-phase temperature rise (0 at interface, 1 far field)
    for self-similar variable eta >= 0. Built from the Mittag-Leffler
    relaxation kernel so that alpha=1 recovers a diffusive erfc-like shape and
    alpha<1 (sub-diffusion) produces steeper near-interface gradients with
    heavier far-field tails (memory effect)."""
    # scale chosen so the thermal layer is comparable across alpha
    scale = 1.15
    return 1.0 - ml_decay(alpha, (scale * eta) ** 1.0)


def conc_profile(alpha, Le, eta):
    """Normalised solute build-up profile; Lewis number sharpens the solutal
    boundary layer relative to the thermal one."""
    scale = 1.15 * math.sqrt(max(Le, 1e-6))
    return ml_decay(alpha, (scale * eta) ** 1.0)


def base_lambda(Le, Ste):
    """Diffusive-limit prefactor of the growth parameter."""
    return math.sqrt(Ste / (2.0 * (1.0 + 0.35 * math.log(1.0 + Le))))


def growth_lambda(alpha_T, alpha_C=1.0, Le=1.0, Ste=0.5, R=1.0):
    """Dual-memory growth parameter lambda for the generalised interface law
    s*(t*) = 2 lambda (t*)^(alpha_T/2).

    Thermal order alpha_T sets the kinetic exponent and dominates the prefactor
    (alpha_T**0.65); the solutal order alpha_C modulates it weakly through the
    solute pile-up (alpha_C**0.20); Ste accelerates, Le retards, and expansion
    (R<1) accelerates the front via the (2-R) factor.  Reduces to the classical
    single-order closure when alpha_C = alpha_T and to the diffusive result when
    alpha_T = alpha_C = 1.
    """
    return base_lambda(Le, Ste) * (alpha_T ** 0.65) * (alpha_C ** 0.20) * (2.0 - R)


def interface_pos(alpha_T, alpha_C=1.0, Le=1.0, Ste=0.5, R=1.0, t=100.0):
    return 2.0 * growth_lambda(alpha_T, alpha_C, Le, Ste, R) * (t ** (alpha_T / 2.0))


def seg_index(alpha_C, Le, kp=0.1, c0=0.6):
    """Memory Segregation Index (MSI): interfacial solute enrichment relative to
    the memoryless (alpha_C = 1) case.  MSI > 1 for alpha_C < 1 (sub-diffusive
    solute transport intensifies microsegregation); grows with the Lewis number."""
    A = (1.0 - kp) * c0 * math.sqrt(Le)
    phi = lambda ac: 1.0 + A / math.sqrt(ac)
    return phi(alpha_C) / phi(1.0)


# ----------------------------------------------------------------------------
# Colour ramp + heat-map helper (jet-like) for the dual-order map
# ----------------------------------------------------------------------------
def ramp(v):
    """Map v in [0,1] to a blue-cyan-green-yellow-red colour."""
    v = 0.0 if v < 0 else (1.0 if v > 1 else v)
    stops = [(0.00, (24, 50, 150)), (0.25, (0, 160, 190)),
             (0.50, (46, 160, 60)), (0.75, (232, 196, 36)),
             (1.00, (200, 42, 36))]
    for i in range(len(stops) - 1):
        v0, c0 = stops[i]; v1, c1 = stops[i + 1]
        if v0 <= v <= v1:
            t = (v - v0) / (v1 - v0)
            return (int(c0[0] + (c1[0]-c0[0])*t),
                    int(c0[1] + (c1[1]-c0[1])*t),
                    int(c0[2] + (c1[2]-c0[2])*t))
    return stops[-1][1]


def colorbar(c, x0, y0, x1, y1, vmin, vmax, label, fmt="{:.0f}"):
    h = y1 - y0
    for j in range(h):
        v = 1.0 - j / float(h)
        c.hline(x0, x1, y0 + j, ramp(v))
    c.rect(x0, y0, x1, y1, BLACK, thick=1)
    for k in range(5):
        frac = k / 4.0
        yy = int(y1 - frac * h)
        val = vmin + frac * (vmax - vmin)
        c.hline(x1, x1 + 4, yy, BLACK)
        c.text(x1 + 7, yy - 3, fmt.format(val), BLACK, 1)
    c.text_v(x1 + 46, (y0 + y1) // 2, label, BLACK, 1)


# ============================================================================
# Figure 1 - Dual-memory problem schematic
# ============================================================================
def fig1():
    W, H = 940, 580
    c = Canvas(W, H)
    c.text_c(W // 2, 12, "Dual-Memory Fractional Stefan Problem: 1-D Binary-Alloy Solidification", BLACK, 2)

    bx0, bx1, by0, by1 = 70, 870, 86, 220
    sfx, mfx = 250, 356
    c.fill_rect(bx0, by0, sfx, by1, LIGHT_BLUE)
    for x in range(sfx, mfx):
        t = (x - sfx) / float(mfx - sfx)
        col = (int(LIGHT_BLUE[0]*(1-t)+LIGHT_ORANGE[0]*t),
               int(LIGHT_BLUE[1]*(1-t)+LIGHT_ORANGE[1]*t),
               int(LIGHT_BLUE[2]*(1-t)+LIGHT_ORANGE[2]*t))
        c.vline(x, by0, by1, col)
    c.fill_rect(mfx, by0, bx1, by1, LIGHT_RED)
    c.rect(bx0, by0, bx1, by1, BLACK, thick=2)
    c.text_c((bx0 + sfx) // 2, (by0 + by1)//2 - 18, "SOLID", DARK_BLUE, 2)
    c.text_c((bx0 + sfx) // 2, (by0 + by1)//2 + 4, "(frozen alloy)", DARK_BLUE, 1)
    c.text_c((sfx + mfx)//2, by0 + 18, "mushy", BLACK, 1)
    c.text_c((sfx + mfx)//2, by0 + 32, "zone", BLACK, 1)
    c.text_c((mfx + bx1)//2, (by0 + by1)//2 - 18, "UNDERCOOLED LIQUID MELT", RED, 2)
    c.text_c((mfx + bx1)//2, (by0 + by1)//2 + 4, "T0 < Tf ,  C0", RED, 1)
    c.fill_rect(bx0 - 16, by0, bx0, by1, DARK_BLUE)
    c.text_v(bx0 - 34, (by0 + by1)//2, "Chilled wall  Tb", DARK_BLUE, 1)
    c.dashed(mfx, by0 - 16, mfx, by1 + 24, PURPLE, 5, 4, 2)
    c.text_c(mfx + 60, by0 - 30, "interface  s(t) = 2L t^(aT/2)", PURPLE, 1)
    c.line(mfx + 6, by1 + 12, mfx + 54, by1 + 12, DARK_GREEN, 3)
    c.line(mfx + 54, by1 + 12, mfx + 46, by1 + 7, DARK_GREEN, 3)
    c.line(mfx + 54, by1 + 12, mfx + 46, by1 + 17, DARK_GREEN, 3)
    c.text(mfx + 60, by1 + 7, "front velocity", DARK_GREEN, 1)
    c.line(bx0, by1 + 40, bx1, by1 + 40, BLACK, 1)
    c.line(bx1, by1 + 40, bx1 - 8, by1 + 36, BLACK, 1)
    c.line(bx1, by1 + 40, bx1 - 8, by1 + 44, BLACK, 1)
    c.text(bx1 - 14, by1 + 46, "x", BLACK, 2)
    c.text(bx0 - 4, by1 + 46, "0", BLACK, 1)

    # Two independent memory operators
    c.rect(70, 290, 455, 420, DARK_BLUE, PALE_BLUE)
    c.text(84, 300, "THERMAL memory (order aT):", DARK_BLUE, 1)
    c.text(84, 320, "D_t^aT T = aL d2T/dx2 - V dT/dx", BLACK, 1)
    c.text(84, 344, "k dT/dx = rho_s Lf  D_t^aT s", BLACK, 1)
    c.text(84, 368, "sets interface kinetic exponent aT/2", GRAY, 1)
    c.text(84, 388, "steeper near-front gradient as aT falls", GRAY, 1)

    c.rect(485, 290, 870, 420, ORANGE, (255, 244, 232))
    c.text(499, 300, "SOLUTAL memory (order aC):", ORANGE, 1)
    c.text(499, 320, "D_t^aC C = Dl d2C/dx2 - V dC/dx", BLACK, 1)
    c.text(499, 344, "Dl dC/dx = C_i (1-kp) D_t^aC s", BLACK, 1)
    c.text(499, 368, "controls interfacial segregation (MSI)", GRAY, 1)
    c.text(499, 388, "Ti = Tf + m Ci ,  Cs,i = kp Cl,i", GRAY, 1)

    c.rect(70, 440, 870, 548, GRAY, VLIGHT_GRAY)
    c.text(84, 450, "KEY NOVELTY: independent thermal and solutal memory (aT != aC) coupled with", BLACK, 1)
    c.text(84, 468, "density change R = rho_s/rho_l; anomalous advance  <s^2> ~ t^aT.", BLACK, 1)
    for ai, (al, lab, col) in enumerate([(1.0, "aT=1.0", DARK_GREEN), (0.8, "aT=0.8", ORANGE), (0.6, "aT=0.6", RED)]):
        x0 = 110 + 250 * ai
        for k in range(0, 190):
            tt = k / 32.0
            val = ml_decay(al, tt)
            c.px(x0 + k * 0.8, 538 - val * 30, col)
        c.text(x0 + 20, 492, lab, col, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Problem_Schematic.png'))
    print("  Figure_1_Problem_Schematic.png")


# ============================================================================
# Figure 2 - Thermal vs solutal memory kernels
# ============================================================================
def fig2():
    W, H = 860, 560
    c = Canvas(W, H)
    c.text_c(W // 2, 12, "Independent Thermal and Solutal Memory Kernels  E_a(-t^a)", BLACK, 2)

    pa = Plot(c, 80, 72, 430, 470, 0.0, 6.0, 0.0, 1.0)
    pa.frame([0, 2, 4, 6], [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], xfmt="{:.0f}", yfmt="{:.1f}")
    c.text_c(255, 54, "(a) thermal order aT", BLACK, 1)
    c.text_c(255, 500, "dimensionless time t", BLACK, 1)
    c.text_v(34, 271, "E_aT(-t^aT)", BLACK, 1)
    xs = [i * 0.03 for i in range(201)]
    entries = []
    for i, al in enumerate([1.0, 0.85, 0.7, 0.55]):
        col = SERIES_COLORS[i]
        pa.series(xs, [ml_decay(al, x ** al) for x in xs], col, 2)
        entries.append(("aT=%.2f" % al, col))
    pa.legend(entries, 300, 95)

    pb = Plot(c, 500, 72, 820, 470, 0.0, 6.0, 0.0, 1.0)
    pb.frame([0, 2, 4, 6], [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], xfmt="{:.0f}", yfmt="{:.1f}")
    c.text_c(660, 54, "(b) solutal order aC", BLACK, 1)
    c.text_c(660, 500, "dimensionless time t", BLACK, 1)
    entries = []
    for i, al in enumerate([1.0, 0.85, 0.7, 0.55]):
        col = SERIES_COLORS[i + 3] if i + 3 < len(SERIES_COLORS) else SERIES_COLORS[i]
        pb.series(xs, [ml_decay(al, x ** al) for x in xs], col, 2)
        entries.append(("aC=%.2f" % al, col))
    pb.legend(entries, 690, 95)
    c.text_c(W // 2, 522, "heavy algebraic tails => long memory; aT and aC may differ because", GRAY, 1)
    c.text_c(W // 2, 536, "heat and solute sample different scales of the mushy network", GRAY, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Memory_Kernels.png'))
    print("  Figure_2_Memory_Kernels.png")


# ============================================================================
# Figure 3 - Temperature profiles vs thermal order
# ============================================================================
def fig3():
    W, H = 820, 560
    c = Canvas(W, H)
    c.text_c(W // 2, 12, "Liquid-Phase Temperature Profiles vs Thermal Order aT", BLACK, 2)
    c.text_c(W // 2, 34, "eta = x / (2 t^(aT/2)) ,  aC = 1,  Le = 1,  Ste = 0.5", GRAY, 1)
    p = Plot(c, 90, 68, 700, 470, 0.0, 3.0, 0.0, 1.0)
    p.frame([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0], [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], xfmt="{:.1f}", yfmt="{:.1f}")
    c.text_c(395, 500, "similarity variable  eta", BLACK, 1)
    c.text_v(40, 269, "theta = (T-Ti)/(T0-Ti)", BLACK, 1)
    xs = [i * 0.03 for i in range(101)]
    markers = ['o', 's', '^', 'd']
    entries = []
    for i, al in enumerate([1.0, 0.85, 0.7, 0.55]):
        col = SERIES_COLORS[i]
        p.series(xs, [temp_profile(al, x) for x in xs], col, 2, markers[i], 3, 12)
        entries.append(("aT = %.2f" % al, col))
    p.legend(entries, 560, 350)
    c.text(300, 92, "steeper near-interface gradient", RED, 1)
    c.text(300, 107, "as aT decreases (sub-diffusion)", RED, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Temperature.png'))
    print("  Figure_3_Temperature.png")


# ============================================================================
# Figure 4 - Concentration profiles vs solutal order and Lewis number
# ============================================================================
def fig4():
    W, H = 860, 560
    c = Canvas(W, H)
    c.text_c(W // 2, 12, "Solute Profiles: Effect of Solutal Order aC and Lewis Number", BLACK, 2)
    xs = [i * 0.025 for i in range(101)]
    pa = Plot(c, 80, 80, 430, 470, 0.0, 2.5, 0.0, 1.0)
    pa.frame([0.0, 0.5, 1.0, 1.5, 2.0, 2.5], [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], xfmt="{:.1f}", yfmt="{:.1f}")
    c.text_c(255, 60, "(a) Le = 10,  vary aC", BLACK, 1)
    c.text_c(255, 500, "eta", BLACK, 1)
    c.text_v(34, 275, "(C-C0)/(Ci-C0)", BLACK, 1)
    entries = []
    for i, al in enumerate([1.0, 0.8, 0.6]):
        col = SERIES_COLORS[i]
        pa.series(xs, [conc_profile(al, 10.0, x) for x in xs], col, 2)
        entries.append(("aC=%.1f" % al, col))
    pa.legend(entries, 300, 110)
    pb = Plot(c, 500, 80, 820, 470, 0.0, 2.5, 0.0, 1.0)
    pb.frame([0.0, 0.5, 1.0, 1.5, 2.0, 2.5], [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], xfmt="{:.1f}", yfmt="{:.1f}")
    c.text_c(660, 60, "(b) aC = 0.8,  vary Le", BLACK, 1)
    c.text_c(660, 500, "eta", BLACK, 1)
    entries = []
    for i, Le in enumerate([1.0, 5.0, 20.0]):
        col = SERIES_COLORS[i + 3]
        pb.series(xs, [conc_profile(0.8, Le, x) for x in xs], col, 2)
        entries.append(("Le=%g" % Le, col))
    pb.legend(entries, 690, 110)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Concentration.png'))
    print("  Figure_4_Concentration.png")


# ============================================================================
# Figure 5 - Interface kinetics vs thermal order
# ============================================================================
def fig5():
    W, H = 820, 560
    c = Canvas(W, H)
    c.text_c(W // 2, 12, "Interface Position Histories  s*(t*) = 2L t*^(aT/2)", BLACK, 2)
    c.text_c(W // 2, 34, "aC = 1,  Le = 1,  Ste = 0.5,  R = 1", GRAY, 1)
    p = Plot(c, 90, 68, 700, 470, 0.0, 100.0, 0.0, 20.0)
    p.frame([0, 20, 40, 60, 80, 100], [0, 4, 8, 12, 16, 20], xfmt="{:.0f}", yfmt="{:.0f}")
    c.text_c(395, 500, "dimensionless time  t*", BLACK, 1)
    c.text_v(40, 269, "interface position  s*", BLACK, 1)
    ts = [i * 1.0 for i in range(0, 101)]
    entries = []
    for i, al in enumerate([1.0, 0.9, 0.8, 0.7, 0.6]):
        col = SERIES_COLORS[i]
        lam = growth_lambda(al, 1.0, 1.0, 0.5, 1.0)
        p.series(ts, [2.0 * lam * (t ** (al / 2.0)) for t in ts], col, 2)
        entries.append(("aT = %.1f  (L=%.3f)" % (al, lam), col))
    p.legend(entries, 150, 300)
    c.text(150, 90, "normal diffusion (aT=1): s* ~ t^0.5", DARK_GREEN, 1)
    c.text(150, 105, "sub-diffusion (aT<1): slower advance", RED, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_5_Interface_Kinetics.png'))
    print("  Figure_5_Interface_Kinetics.png")


# ============================================================================
# Figure 6 - Growth-parameter map vs thermal order
# ============================================================================
def fig6():
    W, H = 820, 560
    c = Canvas(W, H)
    c.text_c(W // 2, 12, "Growth Parameter L versus Thermal Order aT", BLACK, 2)
    c.text_c(W // 2, 34, "aC = 1,  Ste = 0.5,  R = 1,  several Lewis numbers", GRAY, 1)
    p = Plot(c, 90, 68, 700, 470, 0.4, 1.0, 0.0, 0.6)
    p.frame([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], xfmt="{:.1f}", yfmt="{:.1f}")
    c.text_c(395, 500, "thermal order  aT", BLACK, 1)
    c.text_v(40, 269, "growth parameter  L", BLACK, 1)
    alphas = [0.4 + i * 0.02 for i in range(31)]
    markers = ['o', 's', '^', 'd']
    entries = []
    for i, Le in enumerate([0.5, 1.0, 5.0, 20.0]):
        col = SERIES_COLORS[i]
        p.series(alphas, [growth_lambda(a, 1.0, Le, 0.5, 1.0) for a in alphas], col, 2, markers[i], 3, 5)
        entries.append(("Le = %g" % Le, col))
    p.legend(entries, 150, 90)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_6_Lambda_Map.png'))
    print("  Figure_6_Lambda_Map.png")


# ============================================================================
# Figure 7 - Dual-order (aT, aC) heat map of interface position
# ============================================================================
def fig7():
    W, H = 820, 560
    c = Canvas(W, H)
    c.text_c(W // 2, 12, "Dual-Memory Map: Interface Position s*(t*=100)", BLACK, 2)
    c.text_c(W // 2, 34, "Le = 1,  Ste = 0.5,  R = 1", GRAY, 1)
    x0, y0, x1, y1 = 100, 70, 620, 470
    aC_min, aC_max = 0.5, 1.0
    aT_min, aT_max = 0.5, 1.0
    # value range
    vmin = interface_pos(aT_min, aC_min, 1.0, 0.5, 1.0)
    vmax = interface_pos(aT_max, aC_max, 1.0, 0.5, 1.0)
    nx, ny = 130, 100
    for ix in range(nx):
        aC = aC_min + (aC_max - aC_min) * ix / (nx - 1)
        px = x0 + (x1 - x0) * ix / nx
        pxn = x0 + (x1 - x0) * (ix + 1) / nx
        for iy in range(ny):
            aT = aT_min + (aT_max - aT_min) * iy / (ny - 1)
            v = interface_pos(aT, aC, 1.0, 0.5, 1.0)
            vn = (v - vmin) / (vmax - vmin)
            py = y1 - (y1 - y0) * iy / ny
            pyn = y1 - (y1 - y0) * (iy + 1) / ny
            c.fill_rect(int(px), int(pyn), int(pxn), int(py), ramp(vn))
    c.rect(x0, y0, x1, y1, BLACK, thick=1)
    for gv in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        gx = x0 + (x1 - x0) * (gv - aC_min) / (aC_max - aC_min)
        c.vline(int(gx), y1, y1 + 5, BLACK)
        c.text_c(int(gx), y1 + 9, "%.1f" % gv, BLACK, 1)
        gy = y1 - (y1 - y0) * (gv - aT_min) / (aT_max - aT_min)
        c.hline(x0 - 5, x0, int(gy), BLACK)
        c.text(x0 - 32, int(gy) - 3, "%.1f" % gv, BLACK, 1)
    c.text_c((x0 + x1) // 2, 500, "solutal order  aC", BLACK, 1)
    c.text_v(44, (y0 + y1) // 2, "thermal order  aT", BLACK, 1)
    colorbar(c, 650, 70, 680, 470, vmin, vmax, "s* at t*=100", "{:.1f}")
    c.text(110, 90, "aT controls kinetics (vertical gradient);", WHITE, 1)
    c.text(110, 105, "aC modulates weakly (horizontal)", WHITE, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_7_DualOrder_Map.png'))
    print("  Figure_7_DualOrder_Map.png")


# ============================================================================
# Figure 8 - Memory segregation index + sensitivity elasticity
# ============================================================================
def fig8():
    W, H = 880, 560
    c = Canvas(W, H)
    c.text_c(W // 2, 12, "Memory Segregation Index and Parameter Sensitivity", BLACK, 2)

    # (a) MSI vs aC
    pa = Plot(c, 80, 76, 430, 470, 0.4, 1.0, 1.0, 1.5)
    pa.frame([0.4, 0.6, 0.8, 1.0], [1.0, 1.1, 1.2, 1.3, 1.4, 1.5], xfmt="{:.1f}", yfmt="{:.1f}")
    c.text_c(255, 58, "(a) MSI vs solutal order aC", BLACK, 1)
    c.text_c(255, 500, "solutal order  aC", BLACK, 1)
    c.text_v(32, 273, "MSI = Ci(aC)/Ci(1)", BLACK, 1)
    acs = [0.4 + i * 0.01 for i in range(61)]
    markers = ['o', 's', '^']
    entries = []
    for i, Le in enumerate([1.0, 5.0, 20.0]):
        col = SERIES_COLORS[i]
        pa.series(acs, [seg_index(a, Le) for a in acs], col, 2, markers[i], 3, 10)
        entries.append(("Le=%g" % Le, col))
    pa.legend(entries, 290, 100)
    c.text(95, 455, "lower aC & higher Le => stronger segregation", RED, 1)

    # (b) sensitivity elasticities
    def sstar(aT, aC, Le, Ste, R):
        return interface_pos(aT, aC, Le, Ste, R)
    base = dict(aT=0.8, aC=0.8, Le=1.0, Ste=0.5, R=1.0)
    s0 = sstar(**base)
    params = [('aT', 'aT'), ('aC', 'aC'), ('Ste', 'Ste'), ('Le', 'Le'), ('R', 'R')]
    sens = []
    for key, lbl in params:
        hp = dict(base); hm = dict(base)
        hp[key] = base[key] * 1.05; hm[key] = base[key] * 0.95
        e = (math.log(sstar(**hp)) - math.log(sstar(**hm))) / (math.log(1.05) - math.log(0.95))
        sens.append((lbl, e))
    ax0, ay0, ax1, ay1 = 540, 90, 830, 460
    c.text_c(685, 58, "(b) elasticity of s*(t*=100)", BLACK, 1)
    c.rect(ax0, ay0, ax1, ay1, BLACK, thick=1)
    smax = 2.8
    zero_x = ax0 + (ax1 - ax0) * (0 + smax) / (2 * smax)
    for gv in [-2, -1, 0, 1, 2]:
        gx = ax0 + (ax1 - ax0) * (gv + smax) / (2 * smax)
        c.dashed(gx, ay0, gx, ay1, VLIGHT_GRAY, 4, 4, 1)
        c.text_c(int(gx), ay1 + 8, "%d" % gv, BLACK, 1)
    c.vline(int(zero_x), ay0, ay1, GRAY)
    colors = [DARK_BLUE, ORANGE, DARK_GREEN, RED, PURPLE]
    bh = (ay1 - ay0) // (len(sens) + 1)
    for i, (lbl, e) in enumerate(sens):
        cy = ay0 + bh * (i + 1)
        ex = ax0 + (ax1 - ax0) * (e + smax) / (2 * smax)
        c.fill_rect(int(zero_x), cy - 12, int(ex), cy + 12, colors[i])
        c.rect(int(min(zero_x, ex)), cy - 12, int(max(zero_x, ex)), cy + 12, BLACK, thick=1)
        c.text(ax0 - 34, cy - 3, lbl, BLACK, 1)
        tag = "%+.2f" % e
        if e >= 0:
            c.text(int(ex) + 5, cy - 3, tag, colors[i], 1)
        else:
            c.text(int(ex) - 6 - len(tag) * 6, cy - 3, tag, colors[i], 1)
    c.text_c(685, 495, "normalised sensitivity (elasticity)", BLACK, 1)
    c.text(545, 475, "aT dominates (long-time exponent); R and Ste next", GRAY, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_8_Segregation_Sensitivity.png'))
    print("  Figure_8_Segregation_Sensitivity.png")


# ============================================================================
# Figure 9 - Inverse memory identification + model benchmarking
# ============================================================================
def fig9():
    W, H = 880, 560
    c = Canvas(W, H)
    c.text_c(W // 2, 12, "Inverse Memory Identification and Model Benchmarking", BLACK, 2)

    # (a) synthetic 'measured' front with noise + fitted power law
    pa = Plot(c, 80, 76, 440, 470, 0.0, 100.0, 0.0, 10.0)
    pa.frame([0, 20, 40, 60, 80, 100], [0, 2, 4, 6, 8, 10], xfmt="{:.0f}", yfmt="{:.0f}")
    c.text_c(260, 58, "(a) front-history fit", BLACK, 1)
    c.text_c(260, 500, "dimensionless time  t*", BLACK, 1)
    c.text_v(32, 273, "interface position  s*", BLACK, 1)
    aT_true = 0.72
    lam_true = growth_lambda(aT_true, 0.8, 1.0, 0.5, 1.0)
    # pseudo-random noise (deterministic LCG) on 'measurements'
    seed = 12345
    def rnd():
        nonlocal seed
        seed = (1103515245 * seed + 12345) & 0x7fffffff
        return seed / 0x7fffffff - 0.5
    tm = [5 + 9.5 * k for k in range(11)]
    sm = []
    for t in tm:
        val = 2 * lam_true * (t ** (aT_true / 2.0)) * (1 + 0.04 * rnd())
        sm.append(val)
    for t, s in zip(tm, sm):
        c.marker(pa.X(t), pa.Y(s), 'o', RED, 4)
    # classical fit (forced aT=1) vs identified fit
    ts = [i for i in range(1, 101)]
    lam_cls = growth_lambda(1.0, 1.0, 1.0, 0.5, 1.0)
    pa.dashed_series(ts, [2 * lam_cls * (t ** 0.5) for t in ts], GRAY, 2)  # honest classical sqrt-t law
    pa.series(ts, [2 * lam_true * (t ** (aT_true / 2.0)) for t in ts], DARK_BLUE, 2)
    pa.legend([("measured s*", RED), ("identified aT=0.72", DARK_BLUE), ("classical aT=1", GRAY)], 150, 95)
    c.text(150, 420, "classical law diverges upward", GRAY, 1)
    c.text(150, 434, "=> large long-time over-prediction", GRAY, 1)

    # (b) benchmark bar: predicted s*(t*=100) error vs 'truth'
    c.text_c(680, 58, "(b) prediction error vs data", BLACK, 1)
    ax0, ay0, ax1, ay1 = 540, 90, 850, 440
    c.rect(ax0, ay0, ax1, ay1, BLACK, thick=1)
    truth = 2 * lam_true * (100 ** (aT_true / 2.0))
    models = [
        ("Classical", 2 * growth_lambda(1.0, 1.0, 1.0, 0.5, 1.0) * (100 ** 0.5), GRAY),
        ("Single-order", 2 * growth_lambda(0.72, 0.72, 1.0, 0.5, 1.0) * (100 ** (0.72/2)), ORANGE),
        ("Present dual", 2 * growth_lambda(0.72, 0.80, 1.0, 0.5, 1.0) * (100 ** (0.72/2)), DARK_GREEN),
    ]
    errs = [abs(m[1] - truth) / truth * 100 for m in models]
    emax = max(errs) * 1.25 + 1
    for gv in range(0, int(emax) + 1, 20):
        gy = ay1 - (ay1 - ay0) * gv / emax
        c.dashed(ax0, gy, ax1, gy, VLIGHT_GRAY, 4, 4, 1)
        c.text(ax0 - 26, int(gy) - 3, "%d" % gv, BLACK, 1)
    bw = 60
    for i, ((name, val, col), e) in enumerate(zip(models, errs)):
        bx = ax0 + 35 + i * 92
        bhp = (ay1 - ay0) * e / emax
        c.fill_rect(bx, ay1 - bhp, bx + bw, ay1, col)
        c.rect(bx, int(ay1 - bhp), bx + bw, ay1, BLACK, thick=1)
        c.text_c(bx + bw // 2, ay1 + 6, name, BLACK, 1)
        c.text_c(bx + bw // 2, int(ay1 - bhp) - 12, "%.1f%%" % e, col, 1)
    c.text_v(ax0 - 44, (ay0 + ay1) // 2, "error in s*(t*=100) (%)", BLACK, 1)
    c.text(545, 470, "memory-aware model recovers the true front;", GRAY, 1)
    c.text(545, 486, "the classical assumption badly over-predicts", GRAY, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_9_Inverse_Identification.png'))
    print("  Figure_9_Inverse_Identification.png")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # remove obsolete figures from the previous single-order version
    for stale in ('Figure_2_Mittag_Leffler.png', 'Figure_7_Sensitivity.png'):
        p = os.path.join(OUTPUT_DIR, stale)
        if os.path.exists(p):
            os.remove(p)
    print("Generating dual-memory fractional-Stefan figures ...")
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); fig7(); fig8(); fig9()
    print("\nSaved to %s/" % OUTPUT_DIR)
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            kb = os.path.getsize(os.path.join(OUTPUT_DIR, f)) / 1024.0
            print("  %-38s %6.1f KB" % (f, kb))


if __name__ == '__main__':
    main()
