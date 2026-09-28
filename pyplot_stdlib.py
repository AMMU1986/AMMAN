#!/usr/bin/env python3
"""
Minimal pure-stdlib line-plot -> PNG renderer (no numpy/matplotlib/PIL).

Supports: multiple line series, axes with ticks and numeric labels, gridlines,
axis titles, a title, and a legend. Rendering is done on a 2x supersampled RGB
canvas then box-downsampled for smoother lines and text.
"""

import struct
import zlib


# ---- 5x7 bitmap font (columns are 5 wide, rows 7 tall) --------------------
# Each glyph is 7 strings of 5 chars ('#', ' ').
_FONT = {
    ' ': ["     "] * 7,
    '0': [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    '1': ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    '2': [" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"],
    '3': [" ### ", "#   #", "    #", "  ## ", "    #", "#   #", " ### "],
    '4': ["   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "],
    '5': ["#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "],
    '6': ["  ## ", " #   ", "#    ", "#### ", "#   #", "#   #", " ### "],
    '7': ["#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "],
    '8': [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    '9': [" ### ", "#   #", "#   #", " ####", "    #", "   # ", " ##  "],
    '.': ["     ", "     ", "     ", "     ", "     ", " ##  ", " ##  "],
    '-': ["     ", "     ", "     ", "#####", "     ", "     ", "     "],
    '=': ["     ", "     ", "#####", "     ", "#####", "     ", "     "],
    '(': ["  #  ", " #   ", " #   ", " #   ", " #   ", " #   ", "  #  "],
    ')': ["  #  ", "   # ", "   # ", "   # ", "   # ", "   # ", "  #  "],
    '/': ["    #", "    #", "   # ", "  #  ", " #   ", "#    ", "#    "],
    ',': ["     ", "     ", "     ", "     ", " ##  ", " ##  ", "#    "],
    "'": [" ##  ", " ##  ", " #   ", "     ", "     ", "     ", "     "],
    ':': ["     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "     "],
    '+': ["     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "],
    '_': ["     ", "     ", "     ", "     ", "     ", "     ", "#####"],
    '^': ["  #  ", " # # ", "#   #", "     ", "     ", "     ", "     "],
    '?': [" ### ", "#   #", "   # ", "  #  ", "  #  ", "     ", "  #  "],
    'A': [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    'B': ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    'C': [" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "],
    'D': ["###  ", "#  # ", "#   #", "#   #", "#   #", "#  # ", "###  "],
    'E': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    'F': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    'G': [" ### ", "#   #", "#    ", "# ###", "#   #", "#   #", " ### "],
    'H': ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    'I': [" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    'J': ["  ###", "   # ", "   # ", "   # ", "#  # ", "#  # ", " ##  "],
    'K': ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    'L': ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    'M': ["#   #", "## ##", "# # #", "#   #", "#   #", "#   #", "#   #"],
    'N': ["#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"],
    'O': [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    'P': ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    'Q': [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    'R': ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    'S': [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    'T': ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    'U': ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    'V': ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    'W': ["#   #", "#   #", "#   #", "#   #", "# # #", "## ##", "#   #"],
    'X': ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    'Y': ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    'Z': ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    'a': ["     ", "     ", " ### ", "    #", " ####", "#   #", " ####"],
    'b': ["#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#### "],
    'c': ["     ", "     ", " ### ", "#    ", "#    ", "#   #", " ### "],
    'd': ["    #", "    #", " ####", "#   #", "#   #", "#   #", " ####"],
    'e': ["     ", "     ", " ### ", "#   #", "#####", "#    ", " ### "],
    'f': ["  ## ", " #  #", " #   ", "###  ", " #   ", " #   ", " #   "],
    'g': ["     ", " ####", "#   #", "#   #", " ####", "    #", " ### "],
    'h': ["#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#   #"],
    'i': ["  #  ", "     ", " ##  ", "  #  ", "  #  ", "  #  ", " ### "],
    'j': ["   # ", "     ", "  ## ", "   # ", "   # ", "#  # ", " ##  "],
    'l': [" ##  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    'm': ["     ", "     ", "## # ", "# # #", "# # #", "#   #", "#   #"],
    'n': ["     ", "     ", "#### ", "#   #", "#   #", "#   #", "#   #"],
    'o': ["     ", "     ", " ### ", "#   #", "#   #", "#   #", " ### "],
    'p': ["     ", "     ", "#### ", "#   #", "#### ", "#    ", "#    "],
    'q': ["     ", "     ", " ####", "#   #", " ####", "    #", "    #"],
    'k': ["#    ", "#    ", "#  # ", "# #  ", "##   ", "# #  ", "#  # "],
    'r': ["     ", "     ", "# ## ", "##  #", "#    ", "#    ", "#    "],
    's': ["     ", "     ", " ####", "#    ", " ### ", "    #", "#### "],
    't': [" #   ", " #   ", "###  ", " #   ", " #   ", " #  #", "  ## "],
    'u': ["     ", "     ", "#   #", "#   #", "#   #", "#   #", " ####"],
    'v': ["     ", "     ", "#   #", "#   #", "#   #", " # # ", "  #  "],
    'w': ["     ", "     ", "#   #", "#   #", "# # #", "# # #", " # # "],
    'x': ["     ", "     ", "#   #", " # # ", "  #  ", " # # ", "#   #"],
    'y': ["     ", "     ", "#   #", "#   #", " ####", "    #", " ### "],
    'z': ["     ", "     ", "#####", "   # ", "  #  ", " #   ", "#####"],
}


def _glyph(ch):
    if ch in _FONT:
        return _FONT[ch]
    return _FONT['?']


PALETTE = [
    (31, 119, 180),   # blue
    (214, 39, 40),    # red
    (44, 160, 44),    # green
    (148, 103, 189),  # purple
    (255, 127, 14),   # orange
    (140, 86, 75),    # brown
]


class Canvas:
    def __init__(self, width, height, bg=(255, 255, 255), ss=2):
        self.ss = ss
        self.W = width * ss
        self.H = height * ss
        self.w = width
        self.h = height
        self.buf = bytearray(bg * (self.W * self.H))

    def _set(self, x, y, rgb):
        if 0 <= x < self.W and 0 <= y < self.H:
            i = (y * self.W + x) * 3
            self.buf[i] = rgb[0]
            self.buf[i + 1] = rgb[1]
            self.buf[i + 2] = rgb[2]

    def px(self, x, y, rgb):
        """user-space (unsupersampled) pixel -> filled ss x ss block."""
        s = self.ss
        for dy in range(s):
            for dx in range(s):
                self._set(x * s + dx, y * s + dy, rgb)

    def line(self, x0, y0, x1, y1, rgb, width=1):
        # supersampled Bresenham
        s = self.ss
        x0 *= s; y0 *= s; x1 *= s; y1 *= s
        x0 = int(round(x0)); y0 = int(round(y0)); x1 = int(round(x1)); y1 = int(round(y1))
        dx = abs(x1 - x0); dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        r = width * s // 2
        while True:
            for oy in range(-r, r + 1):
                for ox in range(-r, r + 1):
                    self._set(x0 + ox, y0 + oy, rgb)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x0 += sx
            if e2 <= dx:
                err += dx; y0 += sy

    def text(self, x, y, s, rgb=(0, 0, 0), scale=1):
        """Draw text at user-space (x,y) top-left, 5x7 font, char spacing 1."""
        cx = x
        for ch in s:
            g = _glyph(ch)
            for ry in range(7):
                row = g[ry]
                for rx in range(5):
                    if row[rx] == '#':
                        for a in range(scale):
                            for b in range(scale):
                                self.px(cx + rx * scale + a, y + ry * scale + b, rgb)
            cx += (5 + 1) * scale

    def text_w(self, s, scale=1):
        return len(s) * 6 * scale

    def downsample_png(self, path):
        s = self.ss
        out = bytearray()
        for y in range(self.h):
            out.append(0)  # filter: none
            for x in range(self.w):
                r = g = b = 0
                for dy in range(s):
                    for dx in range(s):
                        i = ((y * s + dy) * self.W + (x * s + dx)) * 3
                        r += self.buf[i]; g += self.buf[i + 1]; b += self.buf[i + 2]
                n = s * s
                out.append(r // n); out.append(g // n); out.append(b // n)
        _write_png(path, self.w, self.h, bytes(out))


def _write_png(path, w, h, raw_rows):
    def chunk(ctype, data):
        c = ctype + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
    idat = chunk(b'IDAT', zlib.compress(raw_rows, 9))
    iend = chunk(b'IEND', b'')
    with open(path, 'wb') as fh:
        fh.write(sig + ihdr + idat + iend)


def _nice_ticks(lo, hi, n=5):
    if hi <= lo:
        hi = lo + 1.0
    raw = (hi - lo) / n
    mag = 10 ** _floor_log10(raw)
    norm = raw / mag
    if norm < 1.5:
        step = 1 * mag
    elif norm < 3:
        step = 2 * mag
    elif norm < 7:
        step = 5 * mag
    else:
        step = 10 * mag
    start = _ceil_div(lo, step) * step
    ticks = []
    t = start
    while t <= hi + step * 1e-6:
        ticks.append(round(t, 10))
        t += step
    return ticks


def _floor_log10(x):
    import math
    return int(math.floor(math.log10(x))) if x > 0 else 0


def _ceil_div(a, b):
    import math
    return math.ceil(a / b - 1e-9)


def _fmt(v):
    if abs(v) < 1e-9:
        return "0"
    if v == int(v) and abs(v) < 1e6:
        return str(int(v))
    return ("%.2f" % v).rstrip('0').rstrip('.')


def plot(series, xlabel, ylabel, title, path,
         width=760, height=540, xlim=None, ylim=None, legend_loc='upper right'):
    """series: list of dicts {x:[...], y:[...], label:str, color:(r,g,b)}"""
    c = Canvas(width, height, bg=(255, 255, 255), ss=2)
    L, R, T, B = 78, 28, 46, 62
    plot_w = width - L - R
    plot_h = height - T - B

    xs_all = [v for s in series for v in s['x']]
    ys_all = [v for s in series for v in s['y']]
    xmin, xmax = (xlim if xlim else (min(xs_all), max(xs_all)))
    ymin, ymax = (ylim if ylim else (min(ys_all), max(ys_all)))
    if ymax == ymin:
        ymax = ymin + 1.0
    # pad y a touch
    if not ylim:
        pad = 0.06 * (ymax - ymin)
        ymin -= pad; ymax += pad

    def X(v):
        return L + (v - xmin) / (xmax - xmin) * plot_w
    def Y(v):
        return T + (1 - (v - ymin) / (ymax - ymin)) * plot_h

    grid = (225, 225, 225)
    axis = (0, 0, 0)

    # gridlines + ticks
    for xt in _nice_ticks(xmin, xmax):
        gx = X(xt)
        c.line(gx, T, gx, T + plot_h, grid, 1)
        c.line(gx, T + plot_h, gx, T + plot_h + 4, axis, 1)
        lab = _fmt(xt)
        c.text(int(gx) - c.text_w(lab) // 2, T + plot_h + 10, lab, (30, 30, 30), 1)
    for yt in _nice_ticks(ymin, ymax):
        gy = Y(yt)
        c.line(L, gy, L + plot_w, gy, grid, 1)
        c.line(L - 4, gy, L, gy, axis, 1)
        lab = _fmt(yt)
        c.text(L - 8 - c.text_w(lab), int(gy) - 3, lab, (30, 30, 30), 1)

    # frame
    c.line(L, T, L, T + plot_h, axis, 1)
    c.line(L, T + plot_h, L + plot_w, T + plot_h, axis, 1)
    c.line(L, T, L + plot_w, T, axis, 1)
    c.line(L + plot_w, T, L + plot_w, T + plot_h, axis, 1)

    # series
    for s in series:
        col = s.get('color', PALETTE[0])
        xs, ys = s['x'], s['y']
        for i in range(len(xs) - 1):
            c.line(X(xs[i]), Y(ys[i]), X(xs[i + 1]), Y(ys[i + 1]), col, 2)

    # labels
    c.text(L + plot_w // 2 - c.text_w(xlabel) // 2, height - 20, xlabel, (0, 0, 0), 1)
    # y label (vertical, drawn char-by-char down the left margin)
    yl_x = 6
    yl_y = T + plot_h // 2 - (len(ylabel) * 8) // 2
    for i, ch in enumerate(ylabel):
        c.text(yl_x, yl_y + i * 8, ch, (0, 0, 0), 1)
    c.text(width // 2 - c.text_w(title) // 2, 14, title, (0, 0, 0), 1)

    # legend
    labels = [s for s in series if s.get('label')]
    if labels:
        lw = max(c.text_w(s['label']) for s in labels) + 34
        lh = len(labels) * 16 + 8
        if 'right' in legend_loc:
            lx = L + plot_w - lw - 8
        else:
            lx = L + 10
        ly = T + 8
        # box
        for xx in range(lx, lx + lw):
            c.px(xx, ly, (120, 120, 120)); c.px(xx, ly + lh, (120, 120, 120))
        for yy in range(ly, ly + lh):
            c.px(lx, yy, (120, 120, 120)); c.px(lx + lw, yy, (120, 120, 120))
        for i, s in enumerate(labels):
            yy = ly + 6 + i * 16
            c.line(lx + 6, yy + 4, lx + 26, yy + 4, s.get('color', PALETTE[0]), 2)
            c.text(lx + 30, yy, s['label'], (20, 20, 20), 1)

    c.downsample_png(path)
    return path
