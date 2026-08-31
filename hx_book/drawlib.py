#!/usr/bin/env python3
"""
Pure-Python raster drawing library + PNG encoder (stdlib only: zlib, struct).
Provides a small Canvas with lines, rectangles, filled rects, circles, polylines,
bars, and a built-in 5x7 bitmap font for text (scalable). Used to render the
20 book figures as PNG files without matplotlib/PIL.
"""
import zlib
import struct
import math

# ----------------------------- 5x7 bitmap font -----------------------------
# Each glyph is 5 wide x 7 tall, rows top->bottom, bits left->right (MSB first of 5).
_FONT = {
    ' ': ["00000","00000","00000","00000","00000","00000","00000"],
    '!': ["00100","00100","00100","00100","00100","00000","00100"],
    '"': ["01010","01010","00000","00000","00000","00000","00000"],
    '#': ["01010","11111","01010","01010","11111","01010","00000"],
    '%': ["11001","11010","00100","01011","10011","00000","00000"],
    '&': ["01100","10010","01100","10101","10010","01101","00000"],
    "'": ["00100","00100","00000","00000","00000","00000","00000"],
    '(': ["00010","00100","01000","01000","01000","00100","00010"],
    ')': ["01000","00100","00010","00010","00010","00100","01000"],
    '*': ["00000","01010","00100","11111","00100","01010","00000"],
    '+': ["00000","00100","00100","11111","00100","00100","00000"],
    ',': ["00000","00000","00000","00000","00100","00100","01000"],
    '-': ["00000","00000","00000","11111","00000","00000","00000"],
    '.': ["00000","00000","00000","00000","00000","00110","00110"],
    '/': ["00001","00010","00100","01000","10000","00000","00000"],
    '0': ["01110","10001","10011","10101","11001","10001","01110"],
    '1': ["00100","01100","00100","00100","00100","00100","01110"],
    '2': ["01110","10001","00001","00110","01000","10000","11111"],
    '3': ["11111","00010","00100","00010","00001","10001","01110"],
    '4': ["00010","00110","01010","10010","11111","00010","00010"],
    '5': ["11111","10000","11110","00001","00001","10001","01110"],
    '6': ["00110","01000","10000","11110","10001","10001","01110"],
    '7': ["11111","00001","00010","00100","01000","01000","01000"],
    '8': ["01110","10001","10001","01110","10001","10001","01110"],
    '9': ["01110","10001","10001","01111","00001","00010","01100"],
    ':': ["00000","00110","00110","00000","00110","00110","00000"],
    ';': ["00000","00110","00110","00000","00110","00100","01000"],
    '<': ["00010","00100","01000","10000","01000","00100","00010"],
    '=': ["00000","00000","11111","00000","11111","00000","00000"],
    '>': ["01000","00100","00010","00001","00010","00100","01000"],
    '?': ["01110","10001","00001","00110","00100","00000","00100"],
    '@': ["01110","10001","10111","10101","10111","10000","01110"],
    'A': ["01110","10001","10001","11111","10001","10001","10001"],
    'B': ["11110","10001","10001","11110","10001","10001","11110"],
    'C': ["01110","10001","10000","10000","10000","10001","01110"],
    'D': ["11100","10010","10001","10001","10001","10010","11100"],
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
    '[': ["01110","01000","01000","01000","01000","01000","01110"],
    ']': ["01110","00010","00010","00010","00010","00010","01110"],
    '_': ["00000","00000","00000","00000","00000","00000","11111"],
    'a': ["00000","00000","01110","00001","01111","10001","01111"],
    'b': ["10000","10000","10110","11001","10001","10001","11110"],
    'c': ["00000","00000","01110","10000","10000","10001","01110"],
    'd': ["00001","00001","01101","10011","10001","10001","01111"],
    'e': ["00000","00000","01110","10001","11111","10000","01110"],
    'f': ["00110","01001","01000","11100","01000","01000","01000"],
    'g': ["00000","01111","10001","10001","01111","00001","01110"],
    'h': ["10000","10000","10110","11001","10001","10001","10001"],
    'i': ["00100","00000","01100","00100","00100","00100","01110"],
    'j': ["00010","00000","00110","00010","00010","10010","01100"],
    'k': ["10000","10000","10010","10100","11000","10100","10010"],
    'l': ["01100","00100","00100","00100","00100","00100","01110"],
    'm': ["00000","00000","11010","10101","10101","10001","10001"],
    'n': ["00000","00000","10110","11001","10001","10001","10001"],
    'o': ["00000","00000","01110","10001","10001","10001","01110"],
    'p': ["00000","11110","10001","10001","11110","10000","10000"],
    'q': ["00000","01101","10011","10001","01111","00001","00001"],
    'r': ["00000","00000","10110","11001","10000","10000","10000"],
    's': ["00000","00000","01111","10000","01110","00001","11110"],
    't': ["01000","01000","11100","01000","01000","01001","00110"],
    'u': ["00000","00000","10001","10001","10001","10011","01101"],
    'v': ["00000","00000","10001","10001","10001","01010","00100"],
    'w': ["00000","00000","10001","10001","10101","10101","01010"],
    'x': ["00000","00000","10001","01010","00100","01010","10001"],
    'y': ["00000","10001","10001","01111","00001","00001","01110"],
    'z': ["00000","00000","11111","00010","00100","01000","11111"],
    '°': ["01100","10010","01100","00000","00000","00000","00000"],
    '(': ["00010","00100","01000","01000","01000","00100","00010"],
}
_MISSING = ["11111","10001","10001","10001","10001","10001","11111"]


class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w = w
        self.h = h
        self.px = bytearray([bg[0], bg[1], bg[2]] * (w * h))

    def _set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = c[0]
            self.px[i + 1] = c[1]
            self.px[i + 2] = c[2]

    def fill_rect(self, x0, y0, x1, y1, c):
        x0, x1 = int(min(x0, x1)), int(max(x0, x1))
        y0, y1 = int(min(y0, y1)), int(max(y0, y1))
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self._set(x, y, c)

    def rect(self, x0, y0, x1, y1, c, t=1):
        for k in range(t):
            self.line(x0, y0 + k, x1, y0 + k, c)
            self.line(x0, y1 - k, x1, y1 - k, c)
            self.line(x0 + k, y0, x0 + k, y1, c)
            self.line(x1 - k, y0, x1 - k, y1, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            if t <= 1:
                self._set(x0, y0, c)
            else:
                r = t // 2
                for ox in range(-r, r + 1):
                    for oy in range(-r, r + 1):
                        self._set(x0 + ox, y0 + oy, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def polyline(self, pts, c, t=2):
        for i in range(len(pts) - 1):
            self.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], c, t)

    def circle(self, cx, cy, r, c, fill=False, t=2):
        cx, cy, r = int(cx), int(cy), int(r)
        if fill:
            for y in range(-r, r + 1):
                for x in range(-r, r + 1):
                    if x * x + y * y <= r * r:
                        self._set(cx + x, cy + y, c)
        else:
            steps = max(24, int(2 * math.pi * r))
            prev = None
            for i in range(steps + 1):
                a = 2 * math.pi * i / steps
                p = (cx + r * math.cos(a), cy + r * math.sin(a))
                if prev:
                    self.line(prev[0], prev[1], p[0], p[1], c, t)
                prev = p

    def marker(self, x, y, c, kind='o', s=4):
        if kind == 'o':
            self.circle(x, y, s, c, fill=True)
        elif kind == 's':
            self.fill_rect(x - s, y - s, x + s, y + s, c)
        elif kind == '^':
            self._tri(x, y - s, x - s, y + s, x + s, y + s, c)
        elif kind == 'd':
            self._tri(x, y - s, x - s, y, x + s, y, c)
            self._tri(x, y + s, x - s, y, x + s, y, c)

    def _tri(self, x0, y0, x1, y1, x2, y2, c):
        pts = sorted([(x0, y0), (x1, y1), (x2, y2)], key=lambda p: p[1])
        (ax, ay), (bx, by), (cx, cy) = pts
        def interp(y, p, q):
            if q[1] == p[1]:
                return p[0]
            return p[0] + (q[0] - p[0]) * (y - p[1]) / (q[1] - p[1])
        for y in range(int(ay), int(cy) + 1):
            if y < by:
                xa = interp(y, (ax, ay), (bx, by))
                xb = interp(y, (ax, ay), (cx, cy))
            else:
                xa = interp(y, (bx, by), (cx, cy))
                xb = interp(y, (ax, ay), (cx, cy))
            for x in range(int(min(xa, xb)), int(max(xa, xb)) + 1):
                self._set(x, y, c)

    # --- text ---
    def text(self, x, y, s, c=(0, 0, 0), scale=2):
        cx = x
        for ch in s:
            glyph = _FONT.get(ch, _MISSING)
            for ry, row in enumerate(glyph):
                for rx, bit in enumerate(row):
                    if bit == '1':
                        self.fill_rect(cx + rx * scale, y + ry * scale,
                                       cx + rx * scale + scale - 1,
                                       y + ry * scale + scale - 1, c)
            cx += (5 + 1) * scale
        return cx

    def text_w(self, s, scale=2):
        return len(s) * (6 * scale)

    def text_center(self, cx, y, s, c=(0, 0, 0), scale=2):
        w = self.text_w(s, scale)
        self.text(int(cx - w / 2), y, s, c, scale)

    def text_fit(self, cx, y, s, c=(0, 0, 0), scale=3, maxw=None):
        """Center text, shrinking scale down until it fits within maxw."""
        if maxw is None:
            maxw = self.w - 20
        sc = scale
        while sc > 1 and self.text_w(s, sc) > maxw:
            sc -= 1
        self.text_center(cx, y, s, c, sc)

    def text_v(self, x, cy, s, c=(0, 0, 0), scale=2):
        # vertical text drawn bottom-to-top (rotated 90 CCW) via per-char rotation
        total = self.text_w(s, scale)
        startY = int(cy + total / 2)
        yy = startY
        for ch in s:
            glyph = _FONT.get(ch, _MISSING)
            for ry, row in enumerate(glyph):
                for rx, bit in enumerate(row):
                    if bit == '1':
                        # rotate: new_x = x + ry, new_y = yy - rx
                        self.fill_rect(x + ry * scale, yy - rx * scale,
                                       x + ry * scale + scale - 1,
                                       yy - rx * scale - scale + 1, c)
            yy -= (5 + 1) * scale

    def save(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)  # filter type 0
            start = y * self.w * 3
            raw.extend(self.px[start:start + self.w * 3])
        comp = zlib.compress(bytes(raw), 9)

        def chunk(typ, data):
            c = struct.pack(">I", len(data)) + typ + data
            crc = zlib.crc32(typ + data) & 0xffffffff
            return c + struct.pack(">I", crc)

        with open(path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
            f.write(chunk(b'IHDR', ihdr))
            f.write(chunk(b'IDAT', comp))
            f.write(chunk(b'IEND', b''))


# ------------------------- higher-level chart helpers -------------------------
BLACK = (0, 0, 0)
GRID = (210, 210, 210)
AXIS = (40, 40, 40)
COLORS = [(31, 119, 180), (214, 39, 40), (44, 160, 44), (255, 127, 14),
          (148, 103, 189), (140, 86, 75), (23, 190, 207), (127, 127, 127)]


class Axes:
    """A plotting area inside a Canvas with data->pixel mapping."""
    def __init__(self, cv, x0, y0, x1, y1, xlim, ylim):
        self.cv = cv
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1  # pixel box (y0 top)
        self.xmin, self.xmax = xlim
        self.ymin, self.ymax = ylim

    def px(self, x):
        return self.x0 + (x - self.xmin) / (self.xmax - self.xmin) * (self.x1 - self.x0)

    def py(self, y):
        return self.y1 - (y - self.ymin) / (self.ymax - self.ymin) * (self.y1 - self.y0)

    def frame(self, xlabel='', ylabel='', title='', xticks=None, yticks=None,
              xtl=None, ytl=None):
        cv = self.cv
        cv.fill_rect(self.x0, self.y0, self.x1, self.y1, (252, 252, 252))
        if xticks:
            for i, xt in enumerate(xticks):
                X = self.px(xt)
                cv.line(X, self.y0, X, self.y1, GRID)
                cv.line(X, self.y1, X, self.y1 + 6, AXIS)
                lab = xtl[i] if xtl else _fmt(xt)
                cv.text_center(X, self.y1 + 10, lab, BLACK, 2)
        if yticks:
            for i, yt in enumerate(yticks):
                Y = self.py(yt)
                cv.line(self.x0, Y, self.x1, Y, GRID)
                cv.line(self.x0 - 6, Y, self.x0, Y, AXIS)
                lab = ytl[i] if ytl else _fmt(yt)
                cv.text(self.x0 - 12 - cv.text_w(lab, 2), Y - 7, lab, BLACK, 2)
        cv.rect(self.x0, self.y0, self.x1, self.y1, AXIS, 2)
        if xlabel:
            cv.text_center((self.x0 + self.x1) / 2, self.y1 + 34, xlabel, BLACK, 2)
        if ylabel:
            cv.text_v(self.x0 - 66, (self.y0 + self.y1) / 2, ylabel, BLACK, 2)
        if title:
            cv.text_fit((self.x0 + self.x1) / 2, self.y0 - 30, title, BLACK, 3,
                        maxw=(self.x1 - self.x0))

    def plot(self, xs, ys, c, t=3, marker=None, ms=4):
        pts = [(self.px(x), self.py(y)) for x, y in zip(xs, ys)]
        self.cv.polyline(pts, c, t)
        if marker:
            for p in pts:
                self.cv.marker(p[0], p[1], c, marker, ms)

    def bar(self, centers, values, width, c, base=None):
        base = self.ymin if base is None else base
        for cx, v in zip(centers, values):
            X = self.px(cx)
            w = (self.px(cx + width / 2) - self.px(cx - width / 2))
            self.cv.fill_rect(X - w / 2, self.py(v), X + w / 2, self.py(base), c)
            self.cv.rect(X - w / 2, self.py(v), X + w / 2, self.py(base), AXIS, 1)


def _fmt(v):
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:.2f}".rstrip('0').rstrip('.')


def legend(cv, x, y, items, scale=2):
    """items: list of (label, color, kind) kind in {'line','box'}"""
    yy = y
    maxw = max(cv.text_w(lbl, scale) for lbl, _, _ in items) + 46
    cv.fill_rect(x - 8, y - 8, x + maxw, y + len(items) * 22 + 4, (255, 255, 255))
    cv.rect(x - 8, y - 8, x + maxw, y + len(items) * 22 + 4, AXIS, 1)
    for lbl, col, kind in items:
        if kind == 'box':
            cv.fill_rect(x, yy + 2, x + 26, yy + 12, col)
            cv.rect(x, yy + 2, x + 26, yy + 12, AXIS, 1)
        else:
            cv.line(x, yy + 7, x + 26, yy + 7, col, 3)
            cv.marker(x + 13, yy + 7, col, 'o', 3)
        cv.text(x + 34, yy, lbl, BLACK, scale)
        yy += 22
