#!/usr/bin/env python3
"""
Shared pure-Python PNG canvas for Chapter 4 (Experimentation) figures.
No external dependencies - uses only the standard library (zlib, struct, math).
Provides a small drawing API plus a 5x7 bitmap font.
"""

import struct
import zlib
import math

# ---- Color palette ----
DARK_BLUE = (31, 78, 121)
MED_BLUE = (46, 117, 182)
LIGHT_BLUE = (155, 194, 230)
PALE_BLUE = (218, 232, 252)
DARK_GREEN = (56, 118, 29)
MED_GREEN = (84, 172, 64)
LIGHT_GREEN = (198, 224, 180)
ORANGE = (237, 125, 49)
LIGHT_ORANGE = (248, 203, 173)
RED = (192, 0, 0)
LIGHT_RED = (248, 203, 203)
PURPLE = (112, 48, 160)
LIGHT_PURPLE = (204, 180, 220)
GOLD = (191, 144, 0)
LIGHT_GOLD = (255, 230, 153)
GRAY = (128, 128, 128)
DGRAY = (80, 80, 80)
LIGHT_GRAY = (217, 217, 217)
STEEL = (150, 150, 160)
DK_STEEL = (95, 95, 105)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class PNGCanvas:
    """Fast RGB PNG canvas backed by a bytearray."""

    def __init__(self, width, height, bg=(255, 255, 255)):
        self.w = width
        self.h = height
        self.data = bytearray(width * height * 3)
        r, g, b = bg
        d = self.data
        for i in range(0, len(d), 3):
            d[i] = r
            d[i + 1] = g
            d[i + 2] = b

    def pixel(self, x, y, color):
        x = int(x); y = int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            idx = (y * self.w + x) * 3
            self.data[idx] = color[0]
            self.data[idx + 1] = color[1]
            self.data[idx + 2] = color[2]

    def blend(self, x, y, color, alpha):
        x = int(x); y = int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            idx = (y * self.w + x) * 3
            for k in range(3):
                self.data[idx + k] = int(self.data[idx + k] * (1 - alpha) + color[k] * alpha)

    def fill_rect(self, x1, y1, x2, y2, color):
        x1, x2 = int(x1), int(x2)
        y1, y2 = int(y1), int(y2)
        x1, x2 = max(0, min(x1, x2)), min(self.w - 1, max(x1, x2))
        y1, y2 = max(0, min(y1, y2)), min(self.h - 1, max(y1, y2))
        for y in range(y1, y2 + 1):
            idx = (y * self.w + x1) * 3
            for _ in range(x1, x2 + 1):
                self.data[idx] = color[0]
                self.data[idx + 1] = color[1]
                self.data[idx + 2] = color[2]
                idx += 3

    def rect(self, x1, y1, x2, y2, outline, fill=None):
        if fill:
            self.fill_rect(x1, y1, x2, y2, fill)
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.pixel(x, y1, outline)
            self.pixel(x, y2, outline)
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.pixel(x1, y, outline)
            self.pixel(x2, y, outline)

    def hline(self, x1, x2, y, color):
        y = int(y)
        if y < 0 or y >= self.h:
            return
        x1, x2 = int(x1), int(x2)
        x1, x2 = max(0, min(x1, x2)), min(self.w - 1, max(x1, x2))
        idx = (y * self.w + x1) * 3
        for _ in range(x1, x2 + 1):
            self.data[idx] = color[0]
            self.data[idx + 1] = color[1]
            self.data[idx + 2] = color[2]
            idx += 3

    def vline(self, x, y1, y2, color):
        x = int(x)
        if x < 0 or x >= self.w:
            return
        y1, y2 = int(y1), int(y2)
        y1, y2 = max(0, min(y1, y2)), min(self.h - 1, max(y1, y2))
        for y in range(y1, y2 + 1):
            idx = (y * self.w + x) * 3
            self.data[idx] = color[0]
            self.data[idx + 1] = color[1]
            self.data[idx + 2] = color[2]

    def line(self, x1, y1, x2, y2, color, thick=1):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        dx = abs(x2 - x1); dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        half = thick // 2
        while True:
            if thick <= 1:
                self.pixel(x1, y1, color)
            else:
                for t in range(-half, half + 1):
                    if dy > dx:
                        self.pixel(x1 + t, y1, color)
                    else:
                        self.pixel(x1, y1 + t, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy; x1 += sx
            if e2 < dx:
                err += dx; y1 += sy

    def dline(self, x1, y1, x2, y2, color, dash=6, gap=4):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist == 0:
            return
        steps = int(dist)
        on = True
        cnt = 0
        for i in range(steps + 1):
            t = i / dist
            x = int(x1 + (x2 - x1) * t)
            y = int(y1 + (y2 - y1) * t)
            if on:
                self.pixel(x, y, color)
            cnt += 1
            if on and cnt >= dash:
                on = False; cnt = 0
            elif not on and cnt >= gap:
                on = True; cnt = 0

    def arrow(self, x1, y1, x2, y2, color, thick=2, hs=9):
        self.line(x1, y1, x2, y2, color, thick)
        angle = math.atan2(y2 - y1, x2 - x1)
        for a_off in (0.42, -0.42):
            ax = int(x2 - hs * math.cos(angle - a_off))
            ay = int(y2 - hs * math.sin(angle - a_off))
            self.line(x2, y2, ax, ay, color, thick)

    def circle(self, cx, cy, r, color, fill=None):
        cx, cy, r = int(cx), int(cy), int(r)
        if fill:
            for y in range(-r, r + 1):
                x_span = int(math.sqrt(max(0, r * r - y * y)))
                self.hline(cx - x_span, cx + x_span, cy + y, fill)
        x, y = r, 0
        err = 1 - r
        while x >= y:
            for px, py in [(cx + x, cy + y), (cx - x, cy + y), (cx + x, cy - y), (cx - x, cy - y),
                           (cx + y, cy + x), (cx - y, cy + x), (cx + y, cy - x), (cx - y, cy - x)]:
                self.pixel(px, py, color)
            y += 1
            if err < 0:
                err += 2 * y + 1
            else:
                x -= 1
                err += 2 * (y - x) + 1

    def poly(self, pts, outline, fill=None):
        if fill:
            ys = [p[1] for p in pts]
            ymin, ymax = int(min(ys)), int(max(ys))
            for y in range(ymin, ymax + 1):
                xs = []
                n = len(pts)
                for i in range(n):
                    x1, y1 = pts[i]
                    x2, y2 = pts[(i + 1) % n]
                    if (y1 <= y < y2) or (y2 <= y < y1):
                        xs.append(x1 + (x2 - x1) * (y - y1) / (y2 - y1))
                xs.sort()
                for i in range(0, len(xs) - 1, 2):
                    self.hline(int(xs[i]), int(xs[i + 1]), y, fill)
        n = len(pts)
        for i in range(n):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % n]
            self.line(x1, y1, x2, y2, outline, 1)

    def text(self, x, y, s, color, scale=1):
        x = int(x); y = int(y)
        for ch in s:
            bm = _FONT.get(ch)
            if bm is None:
                x += 6 * scale
                continue
            for ri, row in enumerate(bm):
                for ci in range(5):
                    if row & (1 << (4 - ci)):
                        px, py = x + ci * scale, y + ri * scale
                        for sy in range(scale):
                            for sx in range(scale):
                                self.pixel(px + sx, py + sy, color)
            x += 6 * scale

    def text_c(self, cx, y, s, color, scale=1):
        w = len(s) * 6 * scale
        self.text(cx - w // 2, y, s, color, scale)

    def text_v(self, x, cy, s, color, scale=1):
        """Draw text rotated 90 deg (bottom-to-top) for y-axis labels."""
        total = len(s) * 6 * scale
        start_y = cy + total // 2
        cx = x
        for ch in s:
            bm = _FONT.get(ch)
            if bm is not None:
                for ri, row in enumerate(bm):
                    for ci in range(5):
                        if row & (1 << (4 - ci)):
                            # rotate: (ci, ri) -> (ri, -ci)
                            px = cx + ri * scale
                            py = start_y - ci * scale
                            for sy in range(scale):
                                for sx in range(scale):
                                    self.pixel(px + sx, py - sy, color)
            start_y -= 6 * scale

    def save(self, path):
        raw = bytearray()
        w3 = self.w * 3
        for y in range(self.h):
            raw.append(0)
            off = y * w3
            raw.extend(self.data[off:off + w3])
        compressed = zlib.compress(bytes(raw), 9)

        def chunk(ctype, data):
            c = ctype + data
            crc = zlib.crc32(c) & 0xffffffff
            return struct.pack('>I', len(data)) + c + struct.pack('>I', crc)

        with open(path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0)))
            f.write(chunk(b'IDAT', compressed))
            f.write(chunk(b'IEND', b''))


# ---- Minimal 5x7 bitmap font ----
_FONT = {
    'A': [0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    'B': [0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110],
    'C': [0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110],
    'D': [0b11110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11110],
    'E': [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111],
    'F': [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000],
    'G': [0b01110, 0b10001, 0b10000, 0b10111, 0b10001, 0b10001, 0b01110],
    'H': [0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    'I': [0b01110, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    'J': [0b00111, 0b00010, 0b00010, 0b00010, 0b00010, 0b10010, 0b01100],
    'K': [0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001],
    'L': [0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111],
    'M': [0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001],
    'N': [0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001, 0b10001],
    'O': [0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    'P': [0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000],
    'Q': [0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101],
    'R': [0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001],
    'S': [0b01110, 0b10001, 0b10000, 0b01110, 0b00001, 0b10001, 0b01110],
    'T': [0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100],
    'U': [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    'V': [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100],
    'W': [0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b11011, 0b10001],
    'X': [0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001],
    'Y': [0b10001, 0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b00100],
    'Z': [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111],
    'a': [0b00000, 0b00000, 0b01110, 0b00001, 0b01111, 0b10001, 0b01111],
    'b': [0b10000, 0b10000, 0b10110, 0b11001, 0b10001, 0b10001, 0b11110],
    'c': [0b00000, 0b00000, 0b01110, 0b10000, 0b10000, 0b10001, 0b01110],
    'd': [0b00001, 0b00001, 0b01101, 0b10011, 0b10001, 0b10001, 0b01111],
    'e': [0b00000, 0b00000, 0b01110, 0b10001, 0b11111, 0b10000, 0b01110],
    'f': [0b00110, 0b01001, 0b01000, 0b11100, 0b01000, 0b01000, 0b01000],
    'g': [0b00000, 0b01111, 0b10001, 0b10001, 0b01111, 0b00001, 0b01110],
    'h': [0b10000, 0b10000, 0b10110, 0b11001, 0b10001, 0b10001, 0b10001],
    'i': [0b00100, 0b00000, 0b01100, 0b00100, 0b00100, 0b00100, 0b01110],
    'j': [0b00010, 0b00000, 0b00110, 0b00010, 0b00010, 0b10010, 0b01100],
    'k': [0b10000, 0b10000, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010],
    'l': [0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    'm': [0b00000, 0b00000, 0b11010, 0b10101, 0b10101, 0b10001, 0b10001],
    'n': [0b00000, 0b00000, 0b10110, 0b11001, 0b10001, 0b10001, 0b10001],
    'o': [0b00000, 0b00000, 0b01110, 0b10001, 0b10001, 0b10001, 0b01110],
    'p': [0b00000, 0b00000, 0b11110, 0b10001, 0b11110, 0b10000, 0b10000],
    'q': [0b00000, 0b00000, 0b01101, 0b10011, 0b01111, 0b00001, 0b00001],
    'r': [0b00000, 0b00000, 0b10110, 0b11001, 0b10000, 0b10000, 0b10000],
    's': [0b00000, 0b00000, 0b01110, 0b10000, 0b01110, 0b00001, 0b11110],
    't': [0b01000, 0b01000, 0b11100, 0b01000, 0b01000, 0b01001, 0b00110],
    'u': [0b00000, 0b00000, 0b10001, 0b10001, 0b10001, 0b10011, 0b01101],
    'v': [0b00000, 0b00000, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100],
    'w': [0b00000, 0b00000, 0b10001, 0b10001, 0b10101, 0b10101, 0b01010],
    'x': [0b00000, 0b00000, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001],
    'y': [0b00000, 0b00000, 0b10001, 0b10001, 0b01111, 0b00001, 0b01110],
    'z': [0b00000, 0b00000, 0b11111, 0b00010, 0b00100, 0b01000, 0b11111],
    '0': [0b01110, 0b10001, 0b10011, 0b10101, 0b11001, 0b10001, 0b01110],
    '1': [0b00100, 0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    '2': [0b01110, 0b10001, 0b00001, 0b00010, 0b00100, 0b01000, 0b11111],
    '3': [0b11111, 0b00010, 0b00100, 0b00010, 0b00001, 0b10001, 0b01110],
    '4': [0b00010, 0b00110, 0b01010, 0b10010, 0b11111, 0b00010, 0b00010],
    '5': [0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b10001, 0b01110],
    '6': [0b00110, 0b01000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110],
    '7': [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b01000, 0b01000],
    '8': [0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110],
    '9': [0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00010, 0b01100],
    ' ': [0, 0, 0, 0, 0, 0, 0],
    '.': [0, 0, 0, 0, 0, 0b01100, 0b01100],
    ',': [0, 0, 0, 0, 0b01100, 0b00100, 0b01000],
    ':': [0, 0b01100, 0b01100, 0, 0b01100, 0b01100, 0],
    ';': [0, 0b01100, 0b01100, 0, 0b01100, 0b00100, 0b01000],
    '-': [0, 0, 0, 0b11111, 0, 0, 0],
    '+': [0, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0],
    '(': [0b00010, 0b00100, 0b01000, 0b01000, 0b01000, 0b00100, 0b00010],
    ')': [0b01000, 0b00100, 0b00010, 0b00010, 0b00010, 0b00100, 0b01000],
    '/': [0b00001, 0b00010, 0b00010, 0b00100, 0b01000, 0b01000, 0b10000],
    '>': [0b10000, 0b01000, 0b00100, 0b00010, 0b00100, 0b01000, 0b10000],
    '<': [0b00001, 0b00010, 0b00100, 0b01000, 0b00100, 0b00010, 0b00001],
    '=': [0, 0, 0b11111, 0, 0b11111, 0, 0],
    '%': [0b11001, 0b11001, 0b00010, 0b00100, 0b01000, 0b10011, 0b10011],
    '^': [0b00100, 0b01010, 0b10001, 0, 0, 0, 0],
    '|': [0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100],
    '[': [0b01110, 0b01000, 0b01000, 0b01000, 0b01000, 0b01000, 0b01110],
    ']': [0b01110, 0b00010, 0b00010, 0b00010, 0b00010, 0b00010, 0b01110],
    '_': [0, 0, 0, 0, 0, 0, 0b11111],
    'x2082': [0, 0, 0, 0, 0b01110, 0b00100, 0b01110],  # subscript-ish placeholder
    'o': [0b00000, 0b00000, 0b01110, 0b10001, 0b10001, 0b10001, 0b01110],
    'd_deg': [0b01100, 0b10010, 0b10010, 0b01100, 0, 0, 0],
}
