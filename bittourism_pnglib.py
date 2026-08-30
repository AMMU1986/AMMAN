#!/usr/bin/env python3
"""
Pure-standard-library PNG drawing toolkit (no PIL / matplotlib).
Provides a Canvas with rectangles, lines, polylines, circles and a
built-in 5x7 bitmap font for labels. Used to generate the figures for
the Bio-Integrated Urban Tourism chapter.
"""

import struct
import zlib

# ─── 5x7 bitmap font (uppercase, digits, punctuation) ───
FONT = {
    'A': ["01110","10001","10001","11111","10001","10001","10001"],
    'B': ["11110","10001","10001","11110","10001","10001","11110"],
    'C': ["01111","10000","10000","10000","10000","10000","01111"],
    'D': ["11110","10001","10001","10001","10001","10001","11110"],
    'E': ["11111","10000","10000","11110","10000","10000","11111"],
    'F': ["11111","10000","10000","11110","10000","10000","10000"],
    'G': ["01111","10000","10000","10111","10001","10001","01111"],
    'H': ["10001","10001","10001","11111","10001","10001","10001"],
    'I': ["11111","00100","00100","00100","00100","00100","11111"],
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
    '.': ["00000","00000","00000","00000","00000","00110","00110"],
    ',': ["00000","00000","00000","00000","00110","00110","01100"],
    '-': ["00000","00000","00000","11111","00000","00000","00000"],
    '%': ["11001","11010","00100","01000","01011","10011","00011"],
    '/': ["00001","00010","00010","00100","01000","01000","10000"],
    '(': ["00010","00100","01000","01000","01000","00100","00010"],
    ')': ["01000","00100","00010","00010","00010","00100","01000"],
    ':': ["00000","00110","00110","00000","00110","00110","00000"],
    '+': ["00000","00100","00100","11111","00100","00100","00000"],
    '&': ["01100","10010","10010","01100","10101","10010","01101"],
    ' ': ["00000","00000","00000","00000","00000","00000","00000"],
}


class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w = w
        self.h = h
        self.px = bytearray()
        for _ in range(w * h):
            self.px += bytes(bg)

    def _set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x0, y0, x1, y1, color, fill=True):
        x0, x1 = sorted((int(x0), int(x1)))
        y0, y1 = sorted((int(y0), int(y1)))
        if fill:
            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1):
                    self._set(x, y, color)
        else:
            for x in range(x0, x1 + 1):
                self._set(x, y0, color); self._set(x, y1, color)
            for y in range(y0, y1 + 1):
                self._set(x0, y, color); self._set(x1, y, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            for tx in range(-(thick // 2), thick // 2 + 1):
                for ty in range(-(thick // 2), thick // 2 + 1):
                    self._set(x0 + tx, y0 + ty, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy; x0 += sx
            if e2 < dx:
                err += dx; y0 += sy

    def polyline(self, pts, color, thick=2):
        for i in range(len(pts) - 1):
            self.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], color, thick)

    def circle(self, cx, cy, r, color, fill=True):
        for y in range(-r, r + 1):
            for x in range(-r, r + 1):
                if x * x + y * y <= r * r:
                    if fill or (x * x + y * y >= (r - 1) * (r - 1)):
                        self._set(cx + x, cy + y, color)

    def text(self, x, y, s, color=(0, 0, 0), scale=2):
        s = s.upper()
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT[' '])
            for ry, row in enumerate(glyph):
                for rx, bit in enumerate(row):
                    if bit == '1':
                        self.rect(cx + rx * scale, y + ry * scale,
                                  cx + rx * scale + scale - 1,
                                  y + ry * scale + scale - 1, color)
            cx += (6 * scale)
        return cx

    def text_center(self, cx, y, s, color=(0, 0, 0), scale=2):
        width = len(s) * 6 * scale
        self.text(int(cx - width / 2), y, s, color, scale)

    def save(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)  # filter type 0
            start = y * self.w * 3
            raw += self.px[start:start + self.w * 3]
        compressed = zlib.compress(bytes(raw), 9)

        def chunk(typ, data):
            c = struct.pack(">I", len(data)) + typ + data
            c += struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)
            return c

        with open(path, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")
            f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)))
            f.write(chunk(b"IDAT", compressed))
            f.write(chunk(b"IEND", b""))
