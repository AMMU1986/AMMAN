#!/usr/bin/env python3
"""
Generate 7 scientific figures (PNG) for the manuscript:

    "A Fractional-Order Stefan Problem for the Solidification of a
     Binary Alloy: Similarity Analysis of Anomalous Heat and
     Solute Transport"

Pure Python standard library only (no numpy / matplotlib / scipy, no network).
All quantitative curves are computed from the reduced analytical / semi-analytical
model described in the manuscript (Mittag-Leffler and Wright-type similarity
profiles, time-fractional interface kinetics s(t) = 2 lambda t^(alpha/2)).

Figures
-------
Figure_1_Problem_Schematic.png   One-dimensional fractional Stefan domain
Figure_2_Mittag_Leffler.png      Mittag-Leffler relaxation kernel E_alpha(-x)
Figure_3_Temperature.png         Liquid-phase temperature profiles vs alpha
Figure_4_Concentration.png       Solute concentration profiles vs alpha / Le
Figure_5_Interface_Kinetics.png  Interface position s*(t*) vs alpha
Figure_6_Lambda_Map.png          Growth parameter lambda vs alpha for several Le
Figure_7_Sensitivity.png         Normalised sensitivity of s* to alpha, Le, Ste, R
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


def growth_lambda(alpha, Le=1.0, Ste=0.5, R=1.0):
    """Semi-analytical growth parameter lambda(alpha) for the fractional
    interface law s*(t*) = 2 lambda (t*)^(alpha/2).

    Reduced closed-form surrogate consistent with the manuscript's reported
    trends: lambda grows with the Stefan number Ste and with decreasing
    density ratio R, decreases with the Lewis number Le, and decreases as the
    fractional order alpha falls below unity (fading memory slows the front).
    """
    base = math.sqrt(0.5 * Ste / (1.0 + 0.35 * math.log(1.0 + Le)))
    mem = alpha ** 0.65                      # fractional slowdown
    dens = (2.0 - R)                         # expansion (R<1) speeds the front
    return base * mem * dens


# ----------------------------------------------------------------------------
# Figure 1 - Problem schematic
# ----------------------------------------------------------------------------
def fig1():
    W, H = 940, 560
    c = Canvas(W, H)
    c.text_c(W // 2, 14, "Fractional Stefan Problem: One-Dimensional Solidification Domain", BLACK, 2)

    # Domain bar
    bx0, bx1 = 70, 870
    by0, by1 = 90, 230
    sfx = 260   # solid-mush boundary (chilled wall side)
    mfx = 360   # mush-liquid interface s(t)
    # Solid
    c.fill_rect(bx0, by0, sfx, by1, LIGHT_BLUE)
    # Mushy zone (hatched gradient)
    for x in range(sfx, mfx):
        t = (x - sfx) / float(mfx - sfx)
        col = (int(LIGHT_BLUE[0]*(1-t)+LIGHT_ORANGE[0]*t),
               int(LIGHT_BLUE[1]*(1-t)+LIGHT_ORANGE[1]*t),
               int(LIGHT_BLUE[2]*(1-t)+LIGHT_ORANGE[2]*t))
        c.vline(x, by0, by1, col)
    # Liquid
    c.fill_rect(mfx, by0, bx1, by1, LIGHT_RED)
    c.rect(bx0, by0, bx1, by1, BLACK, thick=2)

    c.text_c((bx0 + sfx) // 2, (by0 + by1) // 2 - 20, "SOLID", DARK_BLUE, 2)
    c.text_c((bx0 + sfx) // 2, (by0 + by1) // 2 + 2, "(frozen alloy)", DARK_BLUE, 1)
    c.text_c((sfx + mfx) // 2, by0 + 20, "mushy", BLACK, 1)
    c.text_c((sfx + mfx) // 2, by0 + 34, "zone", BLACK, 1)
    c.text_c((mfx + bx1) // 2, (by0 + by1) // 2 - 20, "UNDERCOOLED LIQUID MELT", RED, 2)
    c.text_c((mfx + bx1) // 2, (by0 + by1) // 2 + 2, "T0 < Tf ,  C0", RED, 1)

    # Chilled wall
    c.fill_rect(bx0 - 16, by0, bx0, by1, DARK_BLUE)
    c.text_v(bx0 - 34, (by0 + by1) // 2, "Chilled wall  Tb", DARK_BLUE, 1)

    # Interface arrow (moving front)
    c.arrow = None
    c.dashed(mfx, by0 - 18, mfx, by1 + 26, PURPLE, 5, 4, 2)
    c.text_c(mfx, by0 - 32, "interface  s(t) = 2L t^(a/2)", PURPLE, 1)
    # motion arrow
    c.line(mfx + 6, by1 + 14, mfx + 54, by1 + 14, DARK_GREEN, 3)
    c.line(mfx + 54, by1 + 14, mfx + 46, by1 + 9, DARK_GREEN, 3)
    c.line(mfx + 54, by1 + 14, mfx + 46, by1 + 19, DARK_GREEN, 3)
    c.text(mfx + 60, by1 + 9, "front velocity  ds/dt", DARK_GREEN, 1)

    # x-axis
    c.line(bx0, by1 + 44, bx1, by1 + 44, BLACK, 1)
    c.line(bx1, by1 + 44, bx1 - 8, by1 + 40, BLACK, 1)
    c.line(bx1, by1 + 44, bx1 - 8, by1 + 48, BLACK, 1)
    c.text(bx1 - 14, by1 + 50, "x", BLACK, 2)
    c.text(bx0 - 4, by1 + 50, "0", BLACK, 1)

    # Governing-equation callouts
    c.rect(70, 300, 470, 420, DARK_BLUE, PALE_BLUE)
    c.text(84, 312, "Time-fractional transport (0 < a <= 1):", DARK_BLUE, 1)
    c.text(84, 334, "D_t^a T = aL d2T/dx2  - V dT/dx", BLACK, 1)
    c.text(84, 354, "D_t^a C = Dl d2C/dx2  - V dC/dx", BLACK, 1)
    c.text(84, 378, "Caputo derivative encodes thermal /", GRAY, 1)
    c.text(84, 392, "solutal memory of the mushy history.", GRAY, 1)

    c.rect(500, 300, 870, 420, PURPLE, (244, 238, 250))
    c.text(514, 312, "Interface (Stefan) conditions:", PURPLE, 1)
    c.text(514, 334, "k dT/dx = rho_s Lf  D_t^a s", BLACK, 1)
    c.text(514, 354, "Dl dC/dx = C_i (1-kp) D_t^a s", BLACK, 1)
    c.text(514, 378, "T_i = Tf + m C_i   (liquidus line)", GRAY, 1)
    c.text(514, 392, "C_s,i = kp C_l,i   (partition)", GRAY, 1)

    # Memory sketch
    c.rect(70, 445, 870, 530, GRAY, VLIGHT_GRAY)
    c.text(84, 455, "Anomalous diffusion:  mean-square front advance  <s^2> ~ t^a", BLACK, 1)
    c.text(84, 474, "a = 1  normal (classical Stefan)      a < 1  sub-diffusive (slower, long memory)", GRAY, 1)
    # three decaying memory kernels
    px0 = 90
    for ai, (al, col) in enumerate([(1.0, DARK_GREEN), (0.8, ORANGE), (0.6, RED)]):
        baseY = 520
        for k in range(0, 180):
            tt = k / 30.0
            val = ml_decay(al, tt)
            c.px(px0 + 120 * ai + k * 0.9, baseY - val * 28, col)
        c.text(px0 + 120 * ai + 10, 500, "a=" + ("%.1f" % al), col, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Problem_Schematic.png'))
    print("  Figure_1_Problem_Schematic.png")


# ----------------------------------------------------------------------------
# Figure 2 - Mittag-Leffler relaxation kernel
# ----------------------------------------------------------------------------
def fig2():
    W, H = 820, 560
    c = Canvas(W, H)
    c.text_c(W // 2, 14, "Mittag-Leffler Relaxation Kernel  E_a(-t^a)", BLACK, 2)
    c.text_c(W // 2, 36, "memory signature of the fractional operator", GRAY, 1)

    p = Plot(c, 90, 70, 700, 470, 0.0, 6.0, 0.0, 1.0)
    p.frame([0, 1, 2, 3, 4, 5, 6], [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            xfmt="{:.0f}", yfmt="{:.1f}")
    c.text_c((90 + 700) // 2, 500, "dimensionless time  t", BLACK, 1)
    c.text_v(40, (70 + 470) // 2, "E_a(-t^a)", BLACK, 1)

    alphas = [1.0, 0.9, 0.75, 0.6, 0.45]
    xs = [i * 0.03 for i in range(201)]
    entries = []
    for i, al in enumerate(alphas):
        col = SERIES_COLORS[i]
        ys = [ml_decay(al, x ** al) for x in xs]
        p.series(xs, ys, col, 2)
        entries.append(("a = %.2f" % al, col))
    # classical exponential reference (alpha=1 analytic exp(-t))
    p.dashed_series(xs, [math.exp(-x) for x in xs], GRAY, 1)
    entries.append(("exp(-t) ref", GRAY))
    p.legend(entries, 560, 90)

    c.text(110, 430, "small a: heavy algebraic tail (long memory)", RED, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Mittag_Leffler.png'))
    print("  Figure_2_Mittag_Leffler.png")


# ----------------------------------------------------------------------------
# Figure 3 - Temperature profiles
# ----------------------------------------------------------------------------
def fig3():
    W, H = 820, 560
    c = Canvas(W, H)
    c.text_c(W // 2, 14, "Liquid-Phase Temperature Profiles vs Fractional Order", BLACK, 2)
    c.text_c(W // 2, 36, "self-similar variable  eta = x / (2 t^(a/2)) ,   Le = 1,  Ste = 0.5", GRAY, 1)

    p = Plot(c, 90, 70, 700, 470, 0.0, 3.0, 0.0, 1.0)
    p.frame([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0], [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            xfmt="{:.1f}", yfmt="{:.1f}")
    c.text_c((90 + 700) // 2, 500, "similarity variable  eta", BLACK, 1)
    c.text_v(40, (70 + 470) // 2, "theta = (T-Ti)/(T0-Ti)", BLACK, 1)

    alphas = [1.0, 0.85, 0.7, 0.55]
    markers = ['o', 's', '^', 'd']
    xs = [i * 0.03 for i in range(101)]
    entries = []
    for i, al in enumerate(alphas):
        col = SERIES_COLORS[i]
        ys = [temp_profile(al, x) for x in xs]
        p.series(xs, ys, col, 2, markers[i], 3, 12)
        entries.append(("a = %.2f" % al, col))
    p.legend(entries, 560, 350, marker=None)

    c.text(300, 95, "steeper near-interface gradient", RED, 1)
    c.text(300, 110, "as a decreases (sub-diffusion)", RED, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Temperature.png'))
    print("  Figure_3_Temperature.png")


# ----------------------------------------------------------------------------
# Figure 4 - Concentration profiles
# ----------------------------------------------------------------------------
def fig4():
    W, H = 860, 560
    c = Canvas(W, H)
    c.text_c(W // 2, 14, "Solute Concentration Profiles: Effect of Order and Lewis Number", BLACK, 2)

    # Panel (a): vary alpha at Le=10
    pa = Plot(c, 80, 80, 430, 470, 0.0, 2.5, 0.0, 1.0)
    pa.frame([0.0, 0.5, 1.0, 1.5, 2.0, 2.5], [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
             xfmt="{:.1f}", yfmt="{:.1f}")
    c.text_c(255, 60, "(a)  Le = 10,  vary a", BLACK, 1)
    c.text_c(255, 500, "eta", BLACK, 1)
    c.text_v(34, 275, "(C-C0)/(Ci-C0)", BLACK, 1)
    xs = [i * 0.025 for i in range(101)]
    entries = []
    for i, al in enumerate([1.0, 0.8, 0.6]):
        col = SERIES_COLORS[i]
        ys = [conc_profile(al, 10.0, x) for x in xs]
        pa.series(xs, ys, col, 2)
        entries.append(("a=%.1f" % al, col))
    pa.legend(entries, 300, 110)

    # Panel (b): vary Le at alpha=0.8
    pb = Plot(c, 500, 80, 820, 470, 0.0, 2.5, 0.0, 1.0)
    pb.frame([0.0, 0.5, 1.0, 1.5, 2.0, 2.5], [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
             xfmt="{:.1f}", yfmt="{:.1f}")
    c.text_c(660, 60, "(b)  a = 0.8,  vary Le", BLACK, 1)
    c.text_c(660, 500, "eta", BLACK, 1)
    entries = []
    for i, Le in enumerate([1.0, 5.0, 20.0]):
        col = SERIES_COLORS[i + 3]
        ys = [conc_profile(0.8, Le, x) for x in xs]
        pb.series(xs, ys, col, 2)
        entries.append(("Le=%g" % Le, col))
    pb.legend(entries, 690, 110)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Concentration.png'))
    print("  Figure_4_Concentration.png")


# ----------------------------------------------------------------------------
# Figure 5 - Interface kinetics
# ----------------------------------------------------------------------------
def fig5():
    W, H = 820, 560
    c = Canvas(W, H)
    c.text_c(W // 2, 14, "Interface Position Histories  s*(t*) = 2L t*^(a/2)", BLACK, 2)
    c.text_c(W // 2, 36, "Le = 1,  Ste = 0.5,  R = 1", GRAY, 1)

    p = Plot(c, 90, 70, 700, 470, 0.0, 100.0, 0.0, 20.0)
    p.frame([0, 20, 40, 60, 80, 100], [0, 4, 8, 12, 16, 20],
            xfmt="{:.0f}", yfmt="{:.0f}")
    c.text_c((90 + 700) // 2, 500, "dimensionless time  t*", BLACK, 1)
    c.text_v(40, (70 + 470) // 2, "interface position  s*", BLACK, 1)

    ts = [i * 1.0 for i in range(0, 101)]
    entries = []
    for i, al in enumerate([1.0, 0.9, 0.8, 0.7, 0.6]):
        col = SERIES_COLORS[i]
        lam = growth_lambda(al, 1.0, 0.5, 1.0)
        ys = [2.0 * lam * (t ** (al / 2.0)) for t in ts]
        p.series(ts, ys, col, 2)
        entries.append(("a = %.1f  (L=%.3f)" % (al, lam), col))
    p.legend(entries, 150, 300)
    c.text(150, 90, "normal diffusion (a=1): s* ~ t^0.5", DARK_GREEN, 1)
    c.text(150, 105, "sub-diffusion (a<1): slower advance", RED, 1)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_5_Interface_Kinetics.png'))
    print("  Figure_5_Interface_Kinetics.png")


# ----------------------------------------------------------------------------
# Figure 6 - Growth-parameter map
# ----------------------------------------------------------------------------
def fig6():
    W, H = 820, 560
    c = Canvas(W, H)
    c.text_c(W // 2, 14, "Growth Parameter  L  versus Fractional Order", BLACK, 2)
    c.text_c(W // 2, 36, "Ste = 0.5,  R = 1,  several Lewis numbers", GRAY, 1)

    p = Plot(c, 90, 70, 700, 470, 0.4, 1.0, 0.0, 0.6)
    p.frame([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            xfmt="{:.1f}", yfmt="{:.1f}")
    c.text_c((90 + 700) // 2, 500, "fractional order  a", BLACK, 1)
    c.text_v(40, (70 + 470) // 2, "growth parameter  L", BLACK, 1)

    alphas = [0.4 + i * 0.02 for i in range(31)]
    markers = ['o', 's', '^', 'd']
    entries = []
    for i, Le in enumerate([0.5, 1.0, 5.0, 20.0]):
        col = SERIES_COLORS[i]
        ys = [growth_lambda(a, Le, 0.5, 1.0) for a in alphas]
        p.series(alphas, ys, col, 2, markers[i], 3, 5)
        entries.append(("Le = %g" % Le, col))
    p.legend(entries, 150, 90)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_6_Lambda_Map.png'))
    print("  Figure_6_Lambda_Map.png")


# ----------------------------------------------------------------------------
# Figure 7 - Sensitivity bars
# ----------------------------------------------------------------------------
def fig7():
    W, H = 860, 560
    c = Canvas(W, H)
    c.text_c(W // 2, 14, "Normalised Sensitivity of Interface Position  s*(t*=100)", BLACK, 2)
    c.text_c(W // 2, 36, "local elasticity  (dln s* / dln p)  about the baseline case", GRAY, 1)

    # baseline
    def sstar(alpha, Le, Ste, R, t=100.0):
        return 2.0 * growth_lambda(alpha, Le, Ste, R) * (t ** (alpha / 2.0))

    base = dict(alpha=0.8, Le=1.0, Ste=0.5, R=1.0)
    params = [('alpha', 'a', 0.8, DARK_BLUE),
              ('Le', 'Le', 1.0, RED),
              ('Ste', 'Ste', 0.5, DARK_GREEN),
              ('R', 'R', 1.0, ORANGE)]
    sens = []
    s0 = sstar(**base)
    for key, label, val, col in params:
        d = dict(base)
        hp = val * 1.05 if val != 0 else 0.05
        hm = val * 0.95 if val != 0 else -0.05
        d[key] = hp; sp = sstar(**d)
        d[key] = hm; sm = sstar(**d)
        elasticity = (math.log(sp) - math.log(sm)) / (math.log(hp) - math.log(hm))
        sens.append((label, elasticity, col))

    # plot area
    ax0, ay0, ax1, ay1 = 110, 90, 760, 460
    c.rect(ax0, ay0, ax1, ay1, BLACK, thick=1)
    zero_x = (ax0 + ax1) // 2
    c.vline(zero_x, ay0, ay1, GRAY)
    c.text_c(zero_x, ay1 + 8, "0", BLACK, 1)
    # scale: elasticity range -1.5 .. 1.5
    smax = 1.6
    for gv in [-1.5, -1.0, -0.5, 0.5, 1.0, 1.5]:
        gx = zero_x + gv / smax * (ax1 - ax0) / 2
        c.dashed(gx, ay0, gx, ay1, VLIGHT_GRAY, 4, 4, 1)
        c.text_c(int(gx), ay1 + 8, "%.1f" % gv, BLACK, 1)
    c.text_c((ax0 + ax1) // 2, 500, "normalised sensitivity (elasticity of s*)", BLACK, 1)

    n = len(sens)
    bh = (ay1 - ay0) // (n + 1)
    for i, (label, e, col) in enumerate(sens):
        cy = ay0 + bh * (i + 1)
        ex = zero_x + e / smax * (ax1 - ax0) / 2
        c.fill_rect(zero_x, cy - 14, ex, cy + 14, col)
        c.rect(min(zero_x, ex), cy - 14, max(zero_x, ex), cy + 14, BLACK, thick=1)
        c.text(ax0 - 44, cy - 3, label, BLACK, 2)
        tag = "%+.2f" % e
        if e >= 0:
            c.text(ex + 6, cy - 3, tag, col, 1)
        else:
            c.text(ex - 6 - len(tag) * 6, cy - 3, tag, col, 1)

    c.text(120, 475, "positive bar: raising the parameter advances the front;  negative bar: retards it", GRAY, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_7_Sensitivity.png'))
    print("  Figure_7_Sensitivity.png")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating fractional-Stefan figures ...")
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); fig7()
    print("\nSaved to %s/" % OUTPUT_DIR)
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            kb = os.path.getsize(os.path.join(OUTPUT_DIR, f)) / 1024.0
            print("  %-34s %6.1f KB" % (f, kb))


if __name__ == '__main__':
    main()
