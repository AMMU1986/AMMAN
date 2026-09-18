#!/usr/bin/env python3
"""
figlib.py - Pure-Python figure toolkit (no numpy / PIL / matplotlib available).

Provides:
  * A Canvas class (RGB raster) with drawing primitives.
  * A compact 5x7 bitmap font for legible labels.
  * A baseline (sequential) JPEG encoder that writes valid .jpg files.

The JPEG encoder implements the ITU-T T.81 baseline process with the standard
Annex-K Huffman tables, 4:4:4 sampling, and a separable forward DCT.
"""

import math
import struct

# ─────────────────────────────────────────────────────────────────────────────
#  5x7 bitmap font  (each glyph = 7 rows of 5 columns, '#' = ink)
# ─────────────────────────────────────────────────────────────────────────────

_GLYPHS = {
    ' ': ".....،.....،.....،.....،.....،.....،.....",
    '!': "..#..،..#..،..#..،..#..،..#..،.....،..#..",
    '"': ".#.#.،.#.#.،.....،.....،.....،.....،.....",
    '#': ".#.#.،.#.#.،#####،.#.#.،#####،.#.#.،.#.#.",
    '%': "##..#،##.#.،..#..،.#.##،#..##،.....،.....",
    '&': ".##..،#..#.،.##..،#.#.#،#..#.،.##.#،.....",
    "'": "..#..،..#..،.....،.....،.....،.....،.....",
    '(': "...#.،..#..،.#...،.#...،.#...،..#..،...#.",
    ')': ".#...،..#..،...#.،...#.،...#.،..#..،.#...",
    '*': ".....،#.#.#،.###.،#####،.###.،#.#.#،.....",
    '+': ".....،..#..،..#..،#####،..#..،..#..،.....",
    ',': ".....،.....،.....،.....،..#..،..#..،.#...",
    '-': ".....،.....،.....،#####،.....،.....،.....",
    '.': ".....،.....،.....،.....،.....،.##..،.##..",
    '/': "....#،...#.،...#.،..#..،.#...،.#...،#....",
    '0': ".###.،#...#،#..##،#.#.#،##..#،#...#،.###.",
    '1': "..#..،.##..،..#..،..#..،..#..،..#..،.###.",
    '2': ".###.،#...#،....#،..##.،.#...،#....،#####",
    '3': "#####،...#.،..#..،...#.،....#،#...#،.###.",
    '4': "...#.،..##.،.#.#.،#..#.،#####،...#.،...#.",
    '5': "#####،#....،####.،....#،....#،#...#،.###.",
    '6': "..##.،.#...،#....،####.،#...#،#...#،.###.",
    '7': "#####،....#،...#.،..#..،.#...،.#...،.#...",
    '8': ".###.،#...#،#...#،.###.،#...#،#...#،.###.",
    '9': ".###.،#...#،#...#،.####،....#،...#.،.##..",
    ':': ".....،.##..،.##..،.....،.##..،.##..،.....",
    ';': ".....،.##..،.##..،.....،.##..،..#..،.#...",
    '<': "...#.،..#..،.#...،#....،.#...،..#..،...#.",
    '=': ".....،.....،#####،.....،#####،.....،.....",
    '>': ".#...،..#..،...#.،....#،...#.،..#..،.#...",
    '?': ".###.،#...#،....#،..##.،..#..،.....،..#..",
    '@': ".###.،#...#،#.###،#.#.#،#.###،#....،.###.",
    'A': ".###.،#...#،#...#،#####،#...#،#...#،#...#",
    'B': "####.،#...#،#...#،####.،#...#،#...#،####.",
    'C': ".###.،#...#،#....،#....،#....،#...#،.###.",
    'D': "####.،#...#،#...#،#...#،#...#،#...#،####.",
    'E': "#####،#....،#....،####.،#....،#....،#####",
    'F': "#####،#....،#....،####.،#....،#....،#....",
    'G': ".###.،#...#،#....،#.###،#...#،#...#،.###.",
    'H': "#...#،#...#،#...#،#####،#...#،#...#،#...#",
    'I': ".###.،..#..،..#..،..#..،..#..،..#..،.###.",
    'J': "..###،...#.،...#.،...#.،...#.،#..#.،.##..",
    'K': "#...#،#..#.،#.#..،##...،#.#..،#..#.،#...#",
    'L': "#....،#....،#....،#....،#....،#....،#####",
    'M': "#...#،##.##،#.#.#،#.#.#،#...#،#...#،#...#",
    'N': "#...#،#...#،##..#،#.#.#،#..##،#...#،#...#",
    'O': ".###.،#...#،#...#،#...#،#...#،#...#،.###.",
    'P': "####.،#...#،#...#،####.،#....،#....،#....",
    'Q': ".###.،#...#،#...#،#...#،#.#.#،#..#.،.##.#",
    'R': "####.،#...#،#...#،####.،#.#..،#..#.،#...#",
    'S': ".###.،#...#،#....،.###.،....#،#...#،.###.",
    'T': "#####،..#..،..#..،..#..،..#..،..#..،..#..",
    'U': "#...#،#...#،#...#،#...#،#...#،#...#،.###.",
    'V': "#...#،#...#،#...#،#...#،#...#،.#.#.،..#..",
    'W': "#...#،#...#،#...#،#.#.#،#.#.#،##.##،#...#",
    'X': "#...#،#...#،.#.#.،..#..،.#.#.،#...#،#...#",
    'Y': "#...#،#...#،.#.#.،..#..،..#..،..#..،..#..",
    'Z': "#####،....#،...#.،..#..،.#...،#....،#####",
    '[': ".###.،.#...،.#...،.#...،.#...،.#...،.###.",
    ']': ".###.،...#.،...#.،...#.،...#.،...#.،.###.",
    '_': ".....،.....،.....،.....،.....،.....،#####",
    'a': ".....،.....،.###.،....#،.####،#...#،.####",
    'b': "#....،#....،####.،#...#،#...#،#...#،####.",
    'c': ".....،.....،.###.،#...#،#....،#...#،.###.",
    'd': "....#،....#،.####،#...#،#...#،#...#،.####",
    'e': ".....،.....،.###.،#...#،#####،#....،.###.",
    'f': "..##.،.#..#،.#...،###..،.#...،.#...،.#...",
    'g': ".....،.####،#...#،#...#،.####،....#،.###.",
    'h': "#....،#....،####.،#...#،#...#،#...#،#...#",
    'i': "..#..،.....،.##..،..#..،..#..،..#..،.###.",
    'j': "...#.،.....،..##.،...#.،...#.،#..#.،.##..",
    'k': "#....،#....،#..#.،#.#..،##...،#.#..،#..#.",
    'l': ".##..،..#..،..#..،..#..،..#..،..#..،.###.",
    'm': ".....،.....،##.#.،#.#.#،#.#.#،#...#،#...#",
    'n': ".....،.....،####.،#...#،#...#،#...#،#...#",
    'o': ".....،.....،.###.،#...#،#...#،#...#،.###.",
    'p': ".....،####.،#...#،#...#،####.،#....،#....",
    'q': ".....،.####،#...#،#...#،.####،....#،....#",
    'r': ".....،.....،#.##.،##..#،#....،#....،#....",
    's': ".....،.....،.####،#....،.###.،....#،####.",
    't': ".#...،.#...،###..،.#...،.#...،.#..#،..##.",
    'u': ".....،.....،#...#،#...#،#...#،#...#،.####",
    'v': ".....،.....،#...#،#...#،#...#،.#.#.،..#..",
    'w': ".....،.....،#...#،#...#،#.#.#،#.#.#،.#.#.",
    'x': ".....،.....،#...#،.#.#.،..#..،.#.#.،#...#",
    'y': ".....،#...#،#...#،#...#،.####،....#،.###.",
    'z': ".....،.....،#####،...#.،..#..،.#...،#####",
}

FONT = {}
for _ch, _pat in _GLYPHS.items():
    FONT[_ch] = _pat.split('،')

GLYPH_W = 5
GLYPH_H = 7


def text_width(s, scale, spacing=1):
    if not s:
        return 0
    return len(s) * (GLYPH_W * scale + spacing * scale) - spacing * scale


# ─────────────────────────────────────────────────────────────────────────────
#  Canvas
# ─────────────────────────────────────────────────────────────────────────────

class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w = w
        self.h = h
        self.buf = bytearray(w * h * 3)
        self.fill_bg(bg)

    def fill_bg(self, color):
        r, g, b = color
        row = bytes((r, g, b)) * self.w
        for y in range(self.h):
            off = y * self.w * 3
            self.buf[off:off + self.w * 3] = row

    def px(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            o = (y * self.w + x) * 3
            self.buf[o] = color[0]
            self.buf[o + 1] = color[1]
            self.buf[o + 2] = color[2]

    def fill_rect(self, x0, y0, x1, y1, color):
        if x1 < x0:
            x0, x1 = x1, x0
        if y1 < y0:
            y0, y1 = y1, y0
        x0 = max(0, x0); y0 = max(0, y0)
        x1 = min(self.w - 1, x1); y1 = min(self.h - 1, y1)
        r, g, b = color
        seg = bytes((r, g, b)) * (x1 - x0 + 1)
        for y in range(y0, y1 + 1):
            o = (y * self.w + x0) * 3
            self.buf[o:o + len(seg)] = seg

    def rect(self, x0, y0, x1, y1, color, thickness=2):
        for t in range(thickness):
            self.hline(x0, x1, y0 + t, color)
            self.hline(x0, x1, y1 - t, color)
            self.vline(y0, y1, x0 + t, color)
            self.vline(y0, y1, x1 - t, color)

    def round_rect(self, x0, y0, x1, y1, color, thickness=2, r=10):
        # straight edges
        for t in range(thickness):
            self.hline(x0 + r, x1 - r, y0 + t, color)
            self.hline(x0 + r, x1 - r, y1 - t, color)
            self.vline(y0 + r, y1 - r, x0 + t, color)
            self.vline(y0 + r, y1 - r, x1 - t, color)
        # corners (quarter circles)
        for (cx, cy, a0) in [(x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270),
                             (x0 + r, y1 - r, 90), (x1 - r, y1 - r, 0)]:
            self._arc(cx, cy, r, a0, a0 + 90, color, thickness)

    def fill_round_rect(self, x0, y0, x1, y1, color, r=10):
        self.fill_rect(x0 + r, y0, x1 - r, y1, color)
        self.fill_rect(x0, y0 + r, x1, y1 - r, color)
        for (cx, cy) in [(x0 + r, y0 + r), (x1 - r, y0 + r),
                         (x0 + r, y1 - r), (x1 - r, y1 - r)]:
            self._fill_disc(cx, cy, r, color)

    def _fill_disc(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            span = int(math.sqrt(max(0, r * r - dy * dy)))
            self.hline(cx - span, cx + span, cy + dy, color)

    def _arc(self, cx, cy, r, a0, a1, color, thickness):
        steps = max(8, int(r * 2))
        for i in range(steps + 1):
            a = math.radians(a0 + (a1 - a0) * i / steps)
            for t in range(thickness):
                x = int(round(cx + (r - t) * math.cos(a)))
                y = int(round(cy - (r - t) * math.sin(a)))
                self.px(x, y, color)

    def hline(self, x0, x1, y, color):
        if x1 < x0:
            x0, x1 = x1, x0
        for x in range(x0, x1 + 1):
            self.px(x, y, color)

    def vline(self, y0, y1, x, color):
        if y1 < y0:
            y0, y1 = y1, y0
        for y in range(y0, y1 + 1):
            self.px(x, y, color)

    def line(self, x0, y0, x1, y1, color, thickness=2):
        dx = abs(x1 - x0); dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        half = thickness // 2
        while True:
            self.fill_rect(x0 - half, y0 - half, x0 + half, y0 + half, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy; x0 += sx
            if e2 < dx:
                err += dx; y0 += sy

    def arrow(self, x0, y0, x1, y1, color, thickness=2, head=9):
        self.line(x0, y0, x1, y1, color, thickness)
        ang = math.atan2(y1 - y0, x1 - x0)
        for da in (math.radians(150), math.radians(-150)):
            hx = int(x1 + head * math.cos(ang + da))
            hy = int(y1 + head * math.sin(ang + da))
            self.line(x1, y1, hx, hy, color, thickness)

    def text(self, x, y, s, color=(0, 0, 0), scale=2, spacing=1):
        cx = x
        step = spacing * scale
        for ch in s:
            glyph = FONT.get(ch, FONT.get(ch.upper()))
            if glyph is None:
                cx += GLYPH_W * scale + step
                continue
            for gy in range(GLYPH_H):
                rowpat = glyph[gy]
                for gx in range(GLYPH_W):
                    if rowpat[gx] == '#':
                        px0 = cx + gx * scale
                        py0 = y + gy * scale
                        self.fill_rect(px0, py0, px0 + scale - 1,
                                       py0 + scale - 1, color)
            cx += GLYPH_W * scale + step
        return cx

    def text_center(self, cx, y, s, color=(0, 0, 0), scale=2, spacing=1):
        w = text_width(s, scale, spacing)
        return self.text(cx - w // 2, y, s, color, scale, spacing)

    def text_box(self, x0, y0, x1, s, color=(0, 0, 0), scale=2, spacing=1,
                 line_gap=6):
        """Word-wrap s within [x0,x1], starting at y0. Returns final y."""
        max_w = x1 - x0
        words = s.split(' ')
        line = ''
        y = y0
        lh = GLYPH_H * scale + line_gap
        for wd in words:
            trial = wd if not line else line + ' ' + wd
            if text_width(trial, scale, spacing) > max_w and line:
                self.text(x0, y, line, color, scale, spacing)
                y += lh
                line = wd
            else:
                line = trial
        if line:
            self.text(x0, y, line, color, scale, spacing)
            y += lh
        return y

    def labeled_box(self, x0, y0, x1, y1, title, lines, fill, border,
                    title_color=(255, 255, 255), body_color=(20, 20, 20),
                    tscale=2, bscale=2, r=12):
        self.fill_round_rect(x0, y0, x1, y1, fill, r=r)
        self.round_rect(x0, y0, x1, y1, border, thickness=2, r=r)
        cx = (x0 + x1) // 2
        self.text_center(cx, y0 + 12, title, title_color, tscale)
        ty = y0 + 12 + GLYPH_H * tscale + 12
        for ln in lines:
            self.text_center(cx, ty, ln, body_color, bscale)
            ty += GLYPH_H * bscale + 7


# ─────────────────────────────────────────────────────────────────────────────
#  Baseline JPEG encoder
# ─────────────────────────────────────────────────────────────────────────────

_STD_LUM_Q = [
    16, 11, 10, 16, 24, 40, 51, 61,
    12, 12, 14, 19, 26, 58, 60, 55,
    14, 13, 16, 24, 40, 57, 69, 56,
    14, 17, 22, 29, 51, 87, 80, 62,
    18, 22, 37, 56, 68, 109, 103, 77,
    24, 35, 55, 64, 81, 104, 113, 92,
    49, 64, 78, 87, 103, 121, 120, 101,
    72, 92, 95, 98, 112, 100, 103, 99,
]
_STD_CHR_Q = [
    17, 18, 24, 47, 99, 99, 99, 99,
    18, 21, 26, 66, 99, 99, 99, 99,
    24, 26, 56, 99, 99, 99, 99, 99,
    47, 66, 99, 99, 99, 99, 99, 99,
    99, 99, 99, 99, 99, 99, 99, 99,
    99, 99, 99, 99, 99, 99, 99, 99,
    99, 99, 99, 99, 99, 99, 99, 99,
    99, 99, 99, 99, 99, 99, 99, 99,
]

_ZIGZAG = [
    0, 1, 8, 16, 9, 2, 3, 10,
    17, 24, 32, 25, 18, 11, 4, 5,
    12, 19, 26, 33, 40, 48, 41, 34,
    27, 20, 13, 6, 7, 14, 21, 28,
    35, 42, 49, 56, 57, 50, 43, 36,
    29, 22, 15, 23, 30, 37, 44, 51,
    58, 59, 52, 45, 38, 31, 39, 46,
    53, 60, 61, 54, 47, 55, 62, 63,
]

_DC_LUM_BITS = [0, 0, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
_DC_LUM_VALS = list(range(12))
_DC_CHR_BITS = [0, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
_DC_CHR_VALS = list(range(12))

_AC_LUM_BITS = [0, 0, 2, 1, 3, 3, 2, 4, 3, 5, 5, 4, 4, 0, 0, 1, 0x7d]
_AC_LUM_VALS = [
    0x01, 0x02, 0x03, 0x00, 0x04, 0x11, 0x05, 0x12,
    0x21, 0x31, 0x41, 0x06, 0x13, 0x51, 0x61, 0x07,
    0x22, 0x71, 0x14, 0x32, 0x81, 0x91, 0xa1, 0x08,
    0x23, 0x42, 0xb1, 0xc1, 0x15, 0x52, 0xd1, 0xf0,
    0x24, 0x33, 0x62, 0x72, 0x82, 0x09, 0x0a, 0x16,
    0x17, 0x18, 0x19, 0x1a, 0x25, 0x26, 0x27, 0x28,
    0x29, 0x2a, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39,
    0x3a, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49,
    0x4a, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59,
    0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69,
    0x6a, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79,
    0x7a, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89,
    0x8a, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98,
    0x99, 0x9a, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7,
    0xa8, 0xa9, 0xaa, 0xb2, 0xb3, 0xb4, 0xb5, 0xb6,
    0xb7, 0xb8, 0xb9, 0xba, 0xc2, 0xc3, 0xc4, 0xc5,
    0xc6, 0xc7, 0xc8, 0xc9, 0xca, 0xd2, 0xd3, 0xd4,
    0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda, 0xe1, 0xe2,
    0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea,
    0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8,
    0xf9, 0xfa,
]
_AC_CHR_BITS = [0, 0, 2, 1, 2, 4, 4, 3, 4, 7, 5, 4, 4, 0, 1, 2, 0x77]
_AC_CHR_VALS = [
    0x00, 0x01, 0x02, 0x03, 0x11, 0x04, 0x05, 0x21,
    0x31, 0x06, 0x12, 0x41, 0x51, 0x07, 0x61, 0x71,
    0x13, 0x22, 0x32, 0x81, 0x08, 0x14, 0x42, 0x91,
    0xa1, 0xb1, 0xc1, 0x09, 0x23, 0x33, 0x52, 0xf0,
    0x15, 0x62, 0x72, 0xd1, 0x0a, 0x16, 0x24, 0x34,
    0xe1, 0x25, 0xf1, 0x17, 0x18, 0x19, 0x1a, 0x26,
    0x27, 0x28, 0x29, 0x2a, 0x35, 0x36, 0x37, 0x38,
    0x39, 0x3a, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48,
    0x49, 0x4a, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58,
    0x59, 0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68,
    0x69, 0x6a, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78,
    0x79, 0x7a, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87,
    0x88, 0x89, 0x8a, 0x92, 0x93, 0x94, 0x95, 0x96,
    0x97, 0x98, 0x99, 0x9a, 0xa2, 0xa3, 0xa4, 0xa5,
    0xa6, 0xa7, 0xa8, 0xa9, 0xaa, 0xb2, 0xb3, 0xb4,
    0xb5, 0xb6, 0xb7, 0xb8, 0xb9, 0xba, 0xc2, 0xc3,
    0xc4, 0xc5, 0xc6, 0xc7, 0xc8, 0xc9, 0xca, 0xd2,
    0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda,
    0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9,
    0xea, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8,
    0xf9, 0xfa,
]


def _build_huff(bits, vals):
    """bits[1..16] = counts. Return dict val -> (code, length)."""
    codes = {}
    code = 0
    k = 0
    for length in range(1, 17):
        for _ in range(bits[length]):
            codes[vals[k]] = (code, length)
            code += 1
            k += 1
        code <<= 1
    return codes


_DC_LUM = _build_huff(_DC_LUM_BITS, _DC_LUM_VALS)
_DC_CHR = _build_huff(_DC_CHR_BITS, _DC_CHR_VALS)
_AC_LUM = _build_huff(_AC_LUM_BITS, _AC_LUM_VALS)
_AC_CHR = _build_huff(_AC_CHR_BITS, _AC_CHR_VALS)


def _scaled_q(table, quality):
    if quality < 1:
        quality = 1
    if quality > 100:
        quality = 100
    scale = 5000 // quality if quality < 50 else 200 - quality * 2
    out = []
    for v in table:
        q = (v * scale + 50) // 100
        out.append(min(255, max(1, q)))
    return out


# Precompute separable DCT cosine matrix: C[u][x]
_DCT_C = [[math.cos((2 * x + 1) * u * math.pi / 16) for x in range(8)]
          for u in range(8)]
_ALPHA = [math.sqrt(1.0 / 8.0)] + [math.sqrt(2.0 / 8.0)] * 7


def _fdct(block):
    """Forward 8x8 DCT (separable). block: list[64] of floats. -> list[64]."""
    tmp = [0.0] * 64
    # rows
    for y in range(8):
        base = y * 8
        row = block[base:base + 8]
        for u in range(8):
            cu = _DCT_C[u]
            s = 0.0
            for x in range(8):
                s += row[x] * cu[x]
            tmp[base + u] = s * _ALPHA[u]
    out = [0.0] * 64
    # cols
    for u in range(8):
        for v in range(8):
            cv = _DCT_C[v]
            s = 0.0
            for y in range(8):
                s += tmp[y * 8 + u] * cv[y]
            out[v * 8 + u] = s * _ALPHA[v]
    return out


class _BitWriter:
    def __init__(self):
        self.out = bytearray()
        self.acc = 0
        self.nbits = 0

    def write(self, code, length):
        self.acc = (self.acc << length) | (code & ((1 << length) - 1))
        self.nbits += length
        while self.nbits >= 8:
            self.nbits -= 8
            byte = (self.acc >> self.nbits) & 0xFF
            self.out.append(byte)
            if byte == 0xFF:
                self.out.append(0x00)

    def flush(self):
        if self.nbits > 0:
            pad = 8 - self.nbits
            self.acc = (self.acc << pad) | ((1 << pad) - 1)
            self.nbits += pad
            byte = (self.acc >> (self.nbits - 8)) & 0xFF
            self.out.append(byte)
            if byte == 0xFF:
                self.out.append(0x00)
            self.nbits = 0
            self.acc = 0


def _magnitude(v):
    if v == 0:
        return 0, 0
    m = abs(v)
    size = m.bit_length()
    if v < 0:
        code = v + (1 << size) - 1
    else:
        code = v
    return size, code


def _encode_block(bw, block, prev_dc, qt, dc_tab, ac_tab):
    # quantize into zigzag order
    zz = [0] * 64
    for i in range(64):
        q = qt[i]
        val = block[i]
        # round toward nearest
        if val >= 0:
            zz_val = int((val + q / 2) // q)
        else:
            zz_val = -int((-val + q / 2) // q)
        zz[i] = zz_val
    coeff = [zz[_ZIGZAG[i]] for i in range(64)]

    dc = coeff[0]
    diff = dc - prev_dc
    size, code = _magnitude(diff)
    c, l = dc_tab[size]
    bw.write(c, l)
    if size:
        bw.write(code, size)

    # AC
    run = 0
    for i in range(1, 64):
        v = coeff[i]
        if v == 0:
            run += 1
        else:
            while run > 15:
                c, l = ac_tab[0xF0]
                bw.write(c, l)
                run -= 16
            size, code = _magnitude(v)
            sym = (run << 4) | size
            c, l = ac_tab[sym]
            bw.write(c, l)
            bw.write(code, size)
            run = 0
    if run > 0:
        c, l = ac_tab[0x00]  # EOB
        bw.write(c, l)
    return dc


def encode_jpeg(canvas, quality=88):
    w, h, buf = canvas.w, canvas.h, canvas.buf
    lum_q = _scaled_q(_STD_LUM_Q, quality)
    chr_q = _scaled_q(_STD_CHR_Q, quality)
    # quant tables in zigzag order for the DQT segment
    lum_q_zz = [lum_q[_ZIGZAG[i]] for i in range(64)]
    chr_q_zz = [chr_q[_ZIGZAG[i]] for i in range(64)]

    out = bytearray()

    def seg(marker, payload):
        out.extend(marker)
        out.extend(struct.pack('>H', len(payload) + 2))
        out.extend(payload)

    out.extend(b'\xFF\xD8')  # SOI
    # APP0 / JFIF
    app0 = b'JFIF\x00' + bytes([1, 1, 0]) + struct.pack('>HH', 72, 72) + bytes([0, 0])
    seg(b'\xFF\xE0', app0)

    # DQT (two tables)
    dqt = bytes([0x00]) + bytes(lum_q_zz)
    seg(b'\xFF\xDB', dqt)
    dqt2 = bytes([0x01]) + bytes(chr_q_zz)
    seg(b'\xFF\xDB', dqt2)

    # SOF0
    sof = bytes([8]) + struct.pack('>HH', h, w) + bytes([3])
    sof += bytes([1, 0x11, 0])   # Y  sampling 1x1 qt0
    sof += bytes([2, 0x11, 1])   # Cb
    sof += bytes([3, 0x11, 1])   # Cr
    seg(b'\xFF\xC0', sof)

    # DHT
    def dht_payload(cls_id, bits, vals):
        return bytes([cls_id]) + bytes(bits[1:17]) + bytes(vals)
    seg(b'\xFF\xC4', dht_payload(0x00, _DC_LUM_BITS, _DC_LUM_VALS))
    seg(b'\xFF\xC4', dht_payload(0x10, _AC_LUM_BITS, _AC_LUM_VALS))
    seg(b'\xFF\xC4', dht_payload(0x01, _DC_CHR_BITS, _DC_CHR_VALS))
    seg(b'\xFF\xC4', dht_payload(0x11, _AC_CHR_BITS, _AC_CHR_VALS))

    # SOS
    sos = bytes([3, 1, 0x00, 2, 0x11, 3, 0x11, 0, 63, 0])
    seg(b'\xFF\xDA', sos)

    # Precompute YCbCr planes
    npix = w * h
    Y = [0.0] * npix
    Cb = [0.0] * npix
    Cr = [0.0] * npix
    for i in range(npix):
        o = i * 3
        r = buf[o]; g = buf[o + 1]; b = buf[o + 2]
        Y[i] = 0.299 * r + 0.587 * g + 0.114 * b - 128.0
        Cb[i] = -0.168736 * r - 0.331264 * g + 0.5 * b
        Cr[i] = 0.5 * r - 0.418688 * g - 0.081312 * b

    bw = _BitWriter()
    dc_y = dc_cb = dc_cr = 0
    blk = [0.0] * 64
    for by in range(0, h, 8):
        for bx in range(0, w, 8):
            for comp, plane, qt, dctab, actab, prev in (
                    ('Y', Y, lum_q, _DC_LUM, _AC_LUM, 'y'),
                    ('Cb', Cb, chr_q, _DC_CHR, _AC_CHR, 'cb'),
                    ('Cr', Cr, chr_q, _DC_CHR, _AC_CHR, 'cr')):
                for yy in range(8):
                    sy = by + yy
                    if sy >= h:
                        sy = h - 1
                    rowoff = sy * w
                    for xx in range(8):
                        sx = bx + xx
                        if sx >= w:
                            sx = w - 1
                        blk[yy * 8 + xx] = plane[rowoff + sx]
                dct = _fdct(blk)
                if comp == 'Y':
                    dc_y = _encode_block(bw, dct, dc_y, qt, dctab, actab)
                elif comp == 'Cb':
                    dc_cb = _encode_block(bw, dct, dc_cb, qt, dctab, actab)
                else:
                    dc_cr = _encode_block(bw, dct, dc_cr, qt, dctab, actab)
    bw.flush()
    out.extend(bw.out)
    out.extend(b'\xFF\xD9')  # EOI
    return bytes(out)


def save_jpeg(canvas, path, quality=88):
    data = encode_jpeg(canvas, quality)
    with open(path, 'wb') as f:
        f.write(data)
    return len(data)
