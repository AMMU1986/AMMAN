"""Pure-Python PNG canvas with basic drawing primitives (no external deps).
Supports: filled rectangles, lines, simple 5x7 bitmap text, points.
Produces valid 8-bit RGB PNG files via zlib+struct.
"""
import zlib
import struct


class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w = w
        self.h = h
        # row-major list of [r,g,b]
        self.px = bytearray()
        for _ in range(w * h):
            self.px += bytes(bg)

    def _idx(self, x, y):
        return (y * self.w + x) * 3

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = self._idx(int(x), int(y))
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def rect(self, x0, y0, x1, y1, color):
        x0, x1 = sorted((int(x0), int(x1)))
        y0, y1 = sorted((int(y0), int(y1)))
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.set(x, y, color)

    def rect_outline(self, x0, y0, x1, y1, color, t=1):
        self.rect(x0, y0, x1, y0 + t - 1, color)
        self.rect(x0, y1 - t + 1, x1, y1, color)
        self.rect(x0, y0, x0 + t - 1, y1, color)
        self.rect(x1 - t + 1, y0, x1, y1, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for ox in range(-(t // 2), t // 2 + 1):
                for oy in range(-(t // 2), t // 2 + 1):
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

    def circle(self, cx, cy, r, color):
        for y in range(-r, r + 1):
            for x in range(-r, r + 1):
                if x * x + y * y <= r * r:
                    self.set(cx + x, cy + y, color)

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

        png = b"\x89PNG\r\n\x1a\n"
        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        png += chunk(b"IHDR", ihdr)
        png += chunk(b"IDAT", compressed)
        png += chunk(b"IEND", b"")
        with open(path, "wb") as f:
            f.write(png)


# ---- 5x7 bitmap font (uppercase, digits, common punctuation) ----
FONT = {
    'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    'C': ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    'D': ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    'G': ["01110", "10001", "10000", "10111", "10001", "10001", "01110"],
    'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    'I': ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    'J': ["00111", "00010", "00010", "00010", "10010", "10010", "01100"],
    'K': ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    'M': ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    'N': ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    'O': ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    'P': ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    'Q': ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    'R': ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    'U': ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    'V': ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    'W': ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    'X': ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    'Y': ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    'Z': ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    '0': ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    '1': ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    '2': ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    '3': ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    '4': ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    '5': ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    '6': ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    '7': ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    '8': ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    '9': ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    '.': ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ',': ["00000", "00000", "00000", "00000", "01100", "01100", "01000"],
    '-': ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    '/': ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    '%': ["11001", "11010", "00010", "00100", "01000", "01011", "10011"],
    '(': ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ')': ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    ':': ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    ' ': ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
}


def text(canvas, x, y, s, color=(0, 0, 0), scale=1):
    cx = x
    for ch in s.upper():
        glyph = FONT.get(ch, FONT[' '])
        for ry, row in enumerate(glyph):
            for rx, bit in enumerate(row):
                if bit == '1':
                    canvas.rect(cx + rx * scale, y + ry * scale,
                                cx + rx * scale + scale - 1,
                                y + ry * scale + scale - 1, color)
        cx += (5 * scale) + scale
    return cx


def text_center(canvas, cx, y, s, color=(0, 0, 0), scale=1):
    width = len(s) * (6 * scale)
    text(canvas, cx - width // 2, y, s, color, scale)
