#!/usr/bin/env python3
"""
Stdlib-only PNG drawing engine for the Biomathematics chapter figures.
No external dependencies (no matplotlib / PIL / numpy) — uses struct + zlib.
Adapted from the repository's generate_figures.py PNGCanvas pattern.
"""

import struct
import zlib
import math

# Palette
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
LIGHT_GRAY = (217, 217, 217)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class PNGCanvas:
    """Fast RGB PNG canvas using bytearray."""

    def __init__(self, width, height, bg=WHITE):
        self.w = width
        self.h = height
        self.data = bytearray(width * height * 3)
        for i in range(width * height):
            self.data[i * 3] = bg[0]
            self.data[i * 3 + 1] = bg[1]
            self.data[i * 3 + 2] = bg[2]

    def pixel(self, x, y, color):
        x = int(x); y = int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            idx = (y * self.w + x) * 3
            self.data[idx] = color[0]
            self.data[idx + 1] = color[1]
            self.data[idx + 2] = color[2]

    def fill_rect(self, x1, y1, x2, y2, color):
        x1, x2 = int(max(0, min(x1, x2))), int(min(self.w - 1, max(x1, x2)))
        y1, y2 = int(max(0, min(y1, y2))), int(min(self.h - 1, max(y1, y2)))
        for y in range(y1, y2 + 1):
            idx = (y * self.w + x1) * 3
            for x in range(x1, x2 + 1):
                self.data[idx] = color[0]
                self.data[idx + 1] = color[1]
                self.data[idx + 2] = color[2]
                idx += 3

    def rect(self, x1, y1, x2, y2, outline, fill=None, thick=1):
        if fill:
            self.fill_rect(x1, y1, x2, y2, fill)
        for t in range(thick):
            self.hline(x1, x2, y1 + t, outline)
            self.hline(x1, x2, y2 - t, outline)
            self.vline(x1 + t, y1, y2, outline)
            self.vline(x2 - t, y1, y2, outline)

    def rounded_panel(self, x1, y1, x2, y2, outline, fill):
        # Simple filled rect with a border; "rounded" corners faked by clipping
        self.fill_rect(x1, y1, x2, y2, fill)
        self.rect(x1, y1, x2, y2, outline, thick=2)

    def hline(self, x1, x2, y, color):
        y = int(y)
        if y < 0 or y >= self.h:
            return
        x1, x2 = int(max(0, min(x1, x2))), int(min(self.w - 1, max(x1, x2)))
        idx = (y * self.w + x1) * 3
        for x in range(x1, x2 + 1):
            self.data[idx] = color[0]
            self.data[idx + 1] = color[1]
            self.data[idx + 2] = color[2]
            idx += 3

    def vline(self, x, y1, y2, color):
        x = int(x)
        if x < 0 or x >= self.w:
            return
        y1, y2 = int(max(0, min(y1, y2))), int(min(self.h - 1, max(y1, y2)))
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
        while True:
            for t in range(-(thick // 2), (thick + 1) // 2):
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

    def dashed_line(self, x1, y1, x2, y2, color, dash=6, gap=5, thick=1):
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist == 0:
            return
        steps = int(dist)
        on = True
        acc = 0
        px, py = x1, y1
        for s in range(steps + 1):
            t = s / steps
            cx = x1 + (x2 - x1) * t
            cy = y1 + (y2 - y1) * t
            if on:
                self.line(px, py, cx, cy, color, thick)
            px, py = cx, cy
            acc += 1
            if on and acc >= dash:
                on = False; acc = 0
            elif not on and acc >= gap:
                on = True; acc = 0

    def arrow(self, x1, y1, x2, y2, color, thick=2, hs=9):
        self.line(x1, y1, x2, y2, color, thick)
        angle = math.atan2(y2 - y1, x2 - x1)
        for sign in (1, -1):
            ax = x2 - hs * math.cos(angle - sign * 0.4)
            ay = y2 - hs * math.sin(angle - sign * 0.4)
            self.line(x2, y2, ax, ay, color, thick)

    def circle(self, cx, cy, r, color, fill=None, thick=1):
        cx, cy, r = int(cx), int(cy), int(r)
        if fill:
            for y in range(-r, r + 1):
                xs = int(math.sqrt(max(0, r * r - y * y)))
                self.hline(cx - xs, cx + xs, cy + y, fill)
        for tt in range(thick):
            rr = r - tt
            x, y = rr, 0
            err = 1 - rr
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

    def polyline(self, points, color, thick=2):
        for i in range(len(points) - 1):
            self.line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], color, thick)

    def text(self, x, y, s, color, scale=1):
        x = int(x); y = int(y)
        for ch in s:
            bm = _FONT.get(ch)
            if bm is None:
                x += 4 * scale
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
        # crude vertical text: stack characters
        h = len(s) * 8 * scale
        yy = cy - h // 2
        for ch in s:
            self.text(x, yy, ch, color, scale)
            yy += 8 * scale

    def save(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)
            offset = y * self.w * 3
            raw.extend(self.data[offset:offset + self.w * 3])
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


# Minimal 5x7 bitmap font
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
    '.': [0, 0, 0, 0, 0, 0b00110, 0b00110],
    ',': [0, 0, 0, 0, 0, 0b00110, 0b01100],
    '-': [0, 0, 0, 0b11111, 0, 0, 0],
    '+': [0, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0],
    '=': [0, 0, 0b11111, 0, 0b11111, 0, 0],
    '/': [0b00001, 0b00010, 0b00100, 0b00100, 0b01000, 0b10000, 0b10000],
    '(': [0b00010, 0b00100, 0b01000, 0b01000, 0b01000, 0b00100, 0b00010],
    ')': [0b01000, 0b00100, 0b00010, 0b00010, 0b00010, 0b00100, 0b01000],
    ':': [0, 0b00110, 0b00110, 0, 0b00110, 0b00110, 0],
    "'": [0b00100, 0b00100, 0b01000, 0, 0, 0, 0],
    '*': [0, 0b10101, 0b01110, 0b11111, 0b01110, 0b10101, 0],
    '%': [0b11001, 0b11010, 0b00100, 0b01000, 0b10011, 0b00011, 0],
    '<': [0b00010, 0b00100, 0b01000, 0b10000, 0b01000, 0b00100, 0b00010],
    '>': [0b01000, 0b00100, 0b00010, 0b00001, 0b00010, 0b00100, 0b01000],
    '&': [0b01100, 0b10010, 0b10100, 0b01000, 0b10101, 0b10010, 0b01101],
    '[': [0b01110, 0b01000, 0b01000, 0b01000, 0b01000, 0b01000, 0b01110],
    ']': [0b01110, 0b00010, 0b00010, 0b00010, 0b00010, 0b00010, 0b01110],
}
