"""
minichart.py — a tiny pure-standard-library plotting toolkit.

No numpy/matplotlib/Pillow required. Produces PNG files (RGB) using only
zlib + struct. Supports a simple canvas with line drawing, filled rects,
text (built-in 5x7 bitmap font), line/scatter/bar charts and legends.

This is deliberately compact but produces clean, readable scientific figures.
"""
import struct
import zlib


# ----------------------------------------------------------------------------
# 5x7 bitmap font (ASCII 32..126). Each glyph = 7 rows of 5-bit values.
# ----------------------------------------------------------------------------
_FONT = {
    ' ': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    '!': [0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x04],
    '"': [0x0A, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00],
    '#': [0x0A, 0x1F, 0x0A, 0x0A, 0x1F, 0x0A, 0x00],
    '$': [0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04],
    '%': [0x18, 0x19, 0x02, 0x04, 0x08, 0x13, 0x03],
    '&': [0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D],
    "'": [0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00],
    '(': [0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02],
    ')': [0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08],
    '*': [0x00, 0x04, 0x15, 0x0E, 0x15, 0x04, 0x00],
    '+': [0x00, 0x04, 0x04, 0x1F, 0x04, 0x04, 0x00],
    ',': [0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x08],
    '-': [0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00],
    '.': [0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C],
    '/': [0x01, 0x02, 0x02, 0x04, 0x08, 0x08, 0x10],
    '0': [0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E],
    '1': [0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E],
    '2': [0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F],
    '3': [0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E],
    '4': [0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02],
    '5': [0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E],
    '6': [0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E],
    '7': [0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08],
    '8': [0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E],
    '9': [0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C],
    ':': [0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x0C, 0x00],
    ';': [0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x04, 0x08],
    '<': [0x02, 0x04, 0x08, 0x10, 0x08, 0x04, 0x02],
    '=': [0x00, 0x00, 0x1F, 0x00, 0x1F, 0x00, 0x00],
    '>': [0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08],
    '?': [0x0E, 0x11, 0x01, 0x02, 0x04, 0x00, 0x04],
    '@': [0x0E, 0x11, 0x17, 0x15, 0x17, 0x10, 0x0E],
    'A': [0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
    'B': [0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E],
    'C': [0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E],
    'D': [0x1C, 0x12, 0x11, 0x11, 0x11, 0x12, 0x1C],
    'E': [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F],
    'F': [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10],
    'G': [0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F],
    'H': [0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
    'I': [0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E],
    'J': [0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C],
    'K': [0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11],
    'L': [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F],
    'M': [0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11],
    'N': [0x11, 0x11, 0x19, 0x15, 0x13, 0x11, 0x11],
    'O': [0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
    'P': [0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10],
    'Q': [0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D],
    'R': [0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11],
    'S': [0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E],
    'T': [0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],
    'U': [0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
    'V': [0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04],
    'W': [0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11],
    'X': [0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11],
    'Y': [0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04],
    'Z': [0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F],
    '[': [0x0E, 0x08, 0x08, 0x08, 0x08, 0x08, 0x0E],
    '\\': [0x10, 0x08, 0x08, 0x04, 0x02, 0x02, 0x01],
    ']': [0x0E, 0x02, 0x02, 0x02, 0x02, 0x02, 0x0E],
    '^': [0x04, 0x0A, 0x11, 0x00, 0x00, 0x00, 0x00],
    '_': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F],
    '`': [0x08, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00],
    'a': [0x00, 0x00, 0x0E, 0x01, 0x0F, 0x11, 0x0F],
    'b': [0x10, 0x10, 0x16, 0x19, 0x11, 0x11, 0x1E],
    'c': [0x00, 0x00, 0x0E, 0x10, 0x10, 0x11, 0x0E],
    'd': [0x01, 0x01, 0x0D, 0x13, 0x11, 0x11, 0x0F],
    'e': [0x00, 0x00, 0x0E, 0x11, 0x1F, 0x10, 0x0E],
    'f': [0x06, 0x09, 0x08, 0x1C, 0x08, 0x08, 0x08],
    'g': [0x00, 0x0F, 0x11, 0x11, 0x0F, 0x01, 0x0E],
    'h': [0x10, 0x10, 0x16, 0x19, 0x11, 0x11, 0x11],
    'i': [0x04, 0x00, 0x0C, 0x04, 0x04, 0x04, 0x0E],
    'j': [0x02, 0x00, 0x06, 0x02, 0x02, 0x12, 0x0C],
    'k': [0x10, 0x10, 0x12, 0x14, 0x18, 0x14, 0x12],
    'l': [0x0C, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E],
    'm': [0x00, 0x00, 0x1A, 0x15, 0x15, 0x11, 0x11],
    'n': [0x00, 0x00, 0x16, 0x19, 0x11, 0x11, 0x11],
    'o': [0x00, 0x00, 0x0E, 0x11, 0x11, 0x11, 0x0E],
    'p': [0x00, 0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10],
    'q': [0x00, 0x0D, 0x13, 0x11, 0x0F, 0x01, 0x01],
    'r': [0x00, 0x00, 0x16, 0x19, 0x10, 0x10, 0x10],
    's': [0x00, 0x00, 0x0F, 0x10, 0x0E, 0x01, 0x1E],
    't': [0x08, 0x08, 0x1C, 0x08, 0x08, 0x09, 0x06],
    'u': [0x00, 0x00, 0x11, 0x11, 0x11, 0x13, 0x0D],
    'v': [0x00, 0x00, 0x11, 0x11, 0x11, 0x0A, 0x04],
    'w': [0x00, 0x00, 0x11, 0x11, 0x15, 0x15, 0x0A],
    'x': [0x00, 0x00, 0x11, 0x0A, 0x04, 0x0A, 0x11],
    'y': [0x00, 0x11, 0x11, 0x0F, 0x01, 0x11, 0x0E],
    'z': [0x00, 0x00, 0x1F, 0x02, 0x04, 0x08, 0x1F],
    '{': [0x02, 0x04, 0x04, 0x08, 0x04, 0x04, 0x02],
    '|': [0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],
    '}': [0x08, 0x04, 0x04, 0x02, 0x04, 0x04, 0x08],
    '~': [0x00, 0x00, 0x08, 0x15, 0x02, 0x00, 0x00],
}
_CHAR_W = 5
_CHAR_H = 7


class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w = w
        self.h = h
        self.buf = bytearray()
        r, g, b = bg
        row = bytes((r, g, b)) * w
        for _ in range(h):
            self.buf += row

    def _set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i] = color[0]
            self.buf[i + 1] = color[1]
            self.buf[i + 2] = color[2]

    def fill_rect(self, x0, y0, x1, y1, color):
        if x1 < x0:
            x0, x1 = x1, x0
        if y1 < y0:
            y0, y1 = y1, y0
        for y in range(int(y0), int(y1) + 1):
            for x in range(int(x0), int(x1) + 1):
                self._set(x, y, color)

    def hline(self, x0, x1, y, color):
        if x1 < x0:
            x0, x1 = x1, x0
        for x in range(int(x0), int(x1) + 1):
            self._set(x, int(y), color)

    def vline(self, x, y0, y1, color):
        if y1 < y0:
            y0, y1 = y1, y0
        for y in range(int(y0), int(y1) + 1):
            self._set(int(x), y, color)

    def line(self, x0, y0, x1, y1, color, width=1):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for ox in range(-(width // 2), width // 2 + 1):
                for oy in range(-(width // 2), width // 2 + 1):
                    self._set(x0 + ox, y0 + oy, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color, fill=True):
        cx, cy, r = int(cx), int(cy), int(r)
        for y in range(-r, r + 1):
            for x in range(-r, r + 1):
                d2 = x * x + y * y
                if fill:
                    if d2 <= r * r:
                        self._set(cx + x, cy + y, color)
                else:
                    if abs(d2 - r * r) <= r:
                        self._set(cx + x, cy + y, color)

    def marker(self, cx, cy, color, kind='o', size=4):
        cx, cy = int(cx), int(cy)
        if kind == 'o':
            self.circle(cx, cy, size, color, fill=True)
        elif kind == 's':
            self.fill_rect(cx - size, cy - size, cx + size, cy + size, color)
        elif kind == '^':
            for dy in range(-size, size + 1):
                span = size - abs(dy) if dy >= 0 else size + dy
                span = max(0, size - (dy + size))
                w = int((size - abs(dy)))
                self.hline(cx - (size + dy), cx + (size + dy), cy + size - (dy + size), color)
        elif kind == 'd':
            for dy in range(-size, size + 1):
                w = size - abs(dy)
                self.hline(cx - w, cx + w, cy + dy, color)

    def text(self, x, y, s, color=(0, 0, 0), scale=1):
        cx = int(x)
        for ch in s:
            glyph = _FONT.get(ch, _FONT['?'])
            for row in range(_CHAR_H):
                bits = glyph[row]
                for col in range(_CHAR_W):
                    if bits & (1 << (_CHAR_W - 1 - col)):
                        px = cx + col * scale
                        py = int(y) + row * scale
                        for sx in range(scale):
                            for sy in range(scale):
                                self._set(px + sx, py + sy, color)
            cx += (_CHAR_W + 1) * scale

    def text_center(self, xc, y, s, color=(0, 0, 0), scale=1):
        tw = len(s) * (_CHAR_W + 1) * scale
        self.text(xc - tw // 2, y, s, color, scale)

    def text_vertical(self, x, yc, s, color=(0, 0, 0), scale=1):
        # draw rotated 90deg (bottom-to-top) by placing chars stacked
        th = len(s) * (_CHAR_W + 1) * scale
        cy = int(yc + th // 2)
        for ch in s:
            glyph = _FONT.get(ch, _FONT['?'])
            for row in range(_CHAR_H):
                bits = glyph[row]
                for col in range(_CHAR_W):
                    if bits & (1 << (_CHAR_W - 1 - col)):
                        px = int(x) + row * scale
                        py = cy - col * scale
                        for sx in range(scale):
                            for sy in range(scale):
                                self._set(px + sx, py + sy, color)
            cy -= (_CHAR_W + 1) * scale

    def save(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)  # filter type 0
            start = y * self.w * 3
            raw += self.buf[start:start + self.w * 3]
        compressed = zlib.compress(bytes(raw), 9)

        def chunk(typ, data):
            c = struct.pack('>I', len(data)) + typ + data
            crc = zlib.crc32(typ + data) & 0xFFFFFFFF
            return c + struct.pack('>I', crc)

        png = b'\x89PNG\r\n\x1a\n'
        ihdr = struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0)
        png += chunk(b'IHDR', ihdr)
        png += chunk(b'IDAT', compressed)
        png += chunk(b'IEND', b'')
        with open(path, 'wb') as f:
            f.write(png)


# palette
BLACK = (0, 0, 0)
GRID = (210, 210, 210)
AXIS = (60, 60, 60)
BLUE = (31, 119, 180)
ORANGE = (255, 127, 14)
GREEN = (44, 160, 44)
RED = (214, 39, 40)
PURPLE = (148, 103, 189)
TEAL = (23, 190, 207)
BROWN = (140, 86, 75)


def _nice_ticks(vmin, vmax, n=6):
    if vmax == vmin:
        vmax = vmin + 1
    raw = (vmax - vmin) / n
    mag = 10 ** (len(str(int(raw))) - 1) if raw >= 1 else 0.1
    for m in (1, 2, 2.5, 5, 10):
        step = m * mag
        if (vmax - vmin) / step <= n + 1:
            break
    start = step * int(vmin / step)
    ticks = []
    t = start
    while t <= vmax + step * 0.5:
        if t >= vmin - step * 0.5:
            ticks.append(round(t, 6))
        t += step
    return ticks


class Axes:
    """A plotting area with data->pixel mapping and axis rendering."""

    def __init__(self, cv, x0, y0, x1, y1, title='', xlabel='', ylabel=''):
        self.cv = cv
        self.px0, self.py0, self.px1, self.py1 = x0, y0, x1, y1  # plot box in px
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.series = []
        self.bars = []
        self.xmin = self.xmax = self.ymin = self.ymax = None
        self.xcats = None

    def _upd_bounds(self, xs, ys):
        if xs:
            self.xmin = min(xs) if self.xmin is None else min(self.xmin, min(xs))
            self.xmax = max(xs) if self.xmax is None else max(self.xmax, max(xs))
        if ys:
            self.ymin = min(ys) if self.ymin is None else min(self.ymin, min(ys))
            self.ymax = max(ys) if self.ymax is None else max(self.ymax, max(ys))

    def add_line(self, xs, ys, color, label='', marker='o', width=2, msize=3):
        self.series.append(('line', xs, ys, color, label, marker, width, msize))
        self._upd_bounds(xs, ys)

    def add_scatter(self, xs, ys, color, label='', marker='o', msize=4):
        self.series.append(('scatter', xs, ys, color, label, marker, 0, msize))
        self._upd_bounds(xs, ys)

    def set_bar_categories(self, cats):
        self.xcats = cats

    def add_bar_group(self, values, color, label=''):
        self.bars.append((values, color, label))
        self._upd_bounds([], values)

    def _tx(self, x):
        if self.xmax == self.xmin:
            return self.px0
        return self.px0 + (x - self.xmin) / (self.xmax - self.xmin) * (self.px1 - self.px0)

    def _ty(self, y):
        if self.ymax == self.ymin:
            return self.py1
        return self.py1 - (y - self.ymin) / (self.ymax - self.ymin) * (self.py1 - self.py0)

    def render(self, ylim=None, xlim=None, yfmt=None, xfmt=None, legend_loc='tr'):
        cv = self.cv
        if ylim:
            self.ymin, self.ymax = ylim
        else:
            pad = (self.ymax - self.ymin) * 0.08 if self.ymax != self.ymin else 1
            self.ymin -= pad
            self.ymax += pad
            if self.ymin > 0 and self.ymin < pad * 3:
                self.ymin = 0
        if xlim:
            self.xmin, self.xmax = xlim

        # plot border
        cv.fill_rect(self.px0, self.py0, self.px1, self.py1, (252, 252, 252))

        if self.bars:
            self._render_bars(yfmt, legend_loc)
            self._frame_and_labels()
            return

        # gridlines + ticks
        yt = _nice_ticks(self.ymin, self.ymax, 6)
        for t in yt:
            py = self._ty(t)
            cv.hline(self.px0, self.px1, py, GRID)
            lab = (yfmt(t) if yfmt else _fmt(t))
            cv.text(self.px0 - 8 - len(lab) * 6, py - 3, lab, AXIS)
            cv.hline(self.px0 - 4, self.px0, py, AXIS)
        xt = _nice_ticks(self.xmin, self.xmax, 6)
        for t in xt:
            px = self._tx(t)
            cv.vline(px, self.py0, self.py1, GRID)
            lab = (xfmt(t) if xfmt else _fmt(t))
            cv.text_center(px, self.py1 + 8, lab, AXIS)
            cv.vline(px, self.py1, self.py1 + 4, AXIS)

        # series
        for kind, xs, ys, color, label, marker, width, msize in self.series:
            pts = [(self._tx(x), self._ty(y)) for x, y in zip(xs, ys)]
            if kind == 'line':
                for i in range(len(pts) - 1):
                    cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], color, width)
                for (px, py) in pts:
                    cv.marker(px, py, color, marker, msize)
            else:
                for (px, py) in pts:
                    cv.marker(px, py, color, marker, msize)

        self._frame_and_labels()
        self._legend(legend_loc)

    def _render_bars(self, yfmt, legend_loc):
        cv = self.cv
        n_cats = len(self.xcats)
        n_groups = len(self.bars)
        yt = _nice_ticks(self.ymin, self.ymax, 6)
        self.ymax = max(yt)
        self.ymin = min(0, min(yt))
        for t in yt:
            py = self._ty(t)
            cv.hline(self.px0, self.px1, py, GRID)
            lab = (yfmt(t) if yfmt else _fmt(t))
            cv.text(self.px0 - 8 - len(lab) * 6, py - 3, lab, AXIS)
        cat_w = (self.px1 - self.px0) / n_cats
        bar_w = cat_w * 0.7 / n_groups
        for ci in range(n_cats):
            cx0 = self.px0 + ci * cat_w + cat_w * 0.15
            for gi, (values, color, label) in enumerate(self.bars):
                v = values[ci]
                bx0 = cx0 + gi * bar_w
                bx1 = bx0 + bar_w * 0.9
                by = self._ty(v)
                base = self._ty(0)
                cv.fill_rect(bx0, by, bx1, base, color)
            cv.text_center(self.px0 + ci * cat_w + cat_w / 2, self.py1 + 8,
                           self.xcats[ci], AXIS)
        self._legend(legend_loc)

    def _frame_and_labels(self):
        cv = self.cv
        cv.line(self.px0, self.py0, self.px0, self.py1, AXIS, 1)
        cv.line(self.px0, self.py1, self.px1, self.py1, AXIS, 1)
        cv.line(self.px1, self.py0, self.px1, self.py1, AXIS, 1)
        cv.line(self.px0, self.py0, self.px1, self.py0, AXIS, 1)
        if self.title:
            cv.text_center((self.px0 + self.px1) // 2, self.py0 - 22, self.title, BLACK, 2)
        if self.xlabel:
            cv.text_center((self.px0 + self.px1) // 2, self.py1 + 24, self.xlabel, BLACK, 1)
        if self.ylabel:
            cv.text_vertical(self.px0 - 46, (self.py0 + self.py1) // 2, self.ylabel, BLACK, 1)

    def _legend(self, loc):
        cv = self.cv
        items = [(s[3], s[4]) for s in self.series if s[4]]
        items += [(b[1], b[2]) for b in self.bars if b[2]]
        if not items:
            return
        lw = max(len(lab) for _, lab in items) * 6 + 40
        lh = len(items) * 16 + 8
        if loc == 'tr':
            lx1 = self.px1 - 10
            lx0 = lx1 - lw
            ly0 = self.py0 + 10
        elif loc == 'tl':
            lx0 = self.px0 + 10
            lx1 = lx0 + lw
            ly0 = self.py0 + 10
        else:  # br
            lx1 = self.px1 - 10
            lx0 = lx1 - lw
            ly0 = self.py1 - lh - 10
        ly1 = ly0 + lh
        cv.fill_rect(lx0, ly0, lx1, ly1, (255, 255, 255))
        cv.line(lx0, ly0, lx1, ly0, AXIS)
        cv.line(lx0, ly1, lx1, ly1, AXIS)
        cv.line(lx0, ly0, lx0, ly1, AXIS)
        cv.line(lx1, ly0, lx1, ly1, AXIS)
        for i, (color, lab) in enumerate(items):
            yy = ly0 + 8 + i * 16
            cv.fill_rect(lx0 + 8, yy, lx0 + 26, yy + 8, color)
            cv.text(lx0 + 32, yy, lab, BLACK)


def _fmt(v):
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    if abs(v) >= 100:
        return f"{v:.0f}"
    if abs(v) >= 1:
        return f"{v:.1f}"
    return f"{v:.2f}"
