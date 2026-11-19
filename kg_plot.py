#!/usr/bin/env python3
"""
Minimal line-plot helper on top of the standard-library PNGCanvas used in this
repository (generate_figures.py).  Supports multi-panel figures, linear or
log10 axes, dashed/dotted lines, vertical shaded bands and legends.
"""

import math

from generate_figures import PNGCanvas, BLACK, WHITE, GRAY, LIGHT_GRAY

COLORS = {
    'LS': (0, 0, 0),
    'GN-II': (0, 150, 60),
    'GN-III': (30, 90, 220),
    'DPL-1': (0, 175, 210),
    'HDPL': (220, 0, 160),
    'MGT': (220, 40, 30),
    'KG': (220, 0, 160),
    'NE': (30, 90, 220),
    'C': (0, 0, 0),
    'ORANGE': (237, 125, 49),
    'PURPLE': (112, 48, 160),
    'GOLD': (191, 144, 0),
}
DASH = {'LS': 'dash', 'MGT': 'solid', 'GN-II': 'solid', 'GN-III': 'solid',
        'DPL-1': 'dash', 'HDPL': 'solid'}

SHADE_P = (253, 224, 224)
SHADE_S = (222, 235, 252)
SHADE_G = (255, 240, 200)


def fmt_tick(v):
    if v == 0:
        return '0'
    a = abs(v)
    if a >= 1e4 or a < 1e-3:
        e = int(math.floor(math.log10(a)))
        m = v / 10 ** e
        if abs(m - round(m)) < 1e-9:
            return f'{int(round(m))}e{e}' if round(m) != 1 else f'1e{e}'
        return f'{m:.1f}e{e}'
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    s = f'{v:.3f}'.rstrip('0').rstrip('.')
    return s


def nice_ticks(lo, hi, n=5):
    span = hi - lo
    if span <= 0:
        return [lo]
    raw = span / n
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        step = m * mag
        if span / step <= n + 0.5:
            break
    start = math.ceil(lo / step - 1e-9) * step
    ticks = []
    v = start
    while v <= hi + 1e-9 * step:
        ticks.append(round(v, 12))
        v += step
    return ticks


class Panel:
    def __init__(self, fig, x0, y0, w, h, xlim, ylim, xlog=False, ylog=False,
                 xlabel='', ylabel='', title=''):
        self.c = fig.c
        self.x0, self.y0, self.w, self.h = x0, y0, w, h
        self.xlim, self.ylim = xlim, ylim
        self.xlog, self.ylog = xlog, ylog
        self.xlabel, self.ylabel, self.title = xlabel, ylabel, title
        self.legend_items = []

    # coordinate transforms -------------------------------------------------
    def _tx(self, x):
        lo, hi = self.xlim
        if self.xlog:
            if x <= 0:
                return None
            x, lo, hi = math.log10(x), math.log10(lo), math.log10(hi)
        return self.x0 + (x - lo) / (hi - lo) * self.w

    def _ty(self, y):
        lo, hi = self.ylim
        if self.ylog:
            if y <= 0:
                return None
            y, lo, hi = math.log10(y), math.log10(lo), math.log10(hi)
        return self.y0 + self.h - (y - lo) / (hi - lo) * self.h

    def inside(self, px, py):
        return self.x0 <= px <= self.x0 + self.w and self.y0 <= py <= self.y0 + self.h

    # drawing ----------------------------------------------------------------
    def vband(self, xa, xb, color):
        pa, pb = self._tx(max(xa, self.xlim[0])), self._tx(min(xb, self.xlim[1]))
        if pa is None or pb is None or pb <= pa:
            return
        self.c.fill_rect(int(pa), self.y0, int(pb), self.y0 + self.h, color)

    def fill_between_x(self, xs, ylo, yhi, color):
        """Shade between two curves ylo(x), yhi(x) column by column."""
        for x, a, b in zip(xs, ylo, yhi):
            px = self._tx(x)
            pa, pb = self._ty(min(max(a, self.ylim[0]), self.ylim[1])), \
                self._ty(min(max(b, self.ylim[0]), self.ylim[1]))
            if px is None or pa is None or pb is None:
                continue
            self.c.vline(int(px), int(min(pa, pb)), int(max(pa, pb)), color)

    def hline(self, y, color, style='dot'):
        self.plot([self.xlim[0], self.xlim[1]], [y, y], color, style=style, thick=1)

    def vline(self, x, color, style='dot'):
        px = self._tx(x)
        if px is None:
            return
        px = int(px)
        for py in range(self.y0, self.y0 + self.h):
            if style == 'solid' or (py // 4) % 2 == 0:
                self.c.pixel(px, py, color)

    def plot(self, xs, ys, color, style='solid', thick=2, label=None):
        if label:
            self.legend_items.append((label, color, style))
        prev = None
        dist = 0.0
        for x, y in zip(xs, ys):
            if y is None or x is None or isinstance(y, complex) or \
                    (isinstance(y, float) and (math.isnan(y) or math.isinf(y))):
                prev = None
                continue
            px, py = self._tx(x), self._ty(y)
            if px is None or py is None:
                prev = None
                continue
            if prev is not None:
                self._segment(prev[0], prev[1], px, py, color, style, thick, dist)
                dist += math.hypot(px - prev[0], py - prev[1])
            prev = (px, py)

    def _segment(self, x1, y1, x2, y2, color, style, thick, d0):
        n = int(max(abs(x2 - x1), abs(y2 - y1))) + 1
        if n > 4000:
            n = 4000
        for i in range(n + 1):
            t = i / n
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            d = d0 + math.hypot(x - x1, y - y1)
            if style == 'dash' and (d % 14) > 8:
                continue
            if style == 'dot' and (d % 6) > 2:
                continue
            if style == 'dashdot' and ((d % 20) > 9 and not 13 < (d % 20) < 16):
                continue
            for ox in range(-(thick // 2), (thick + 1) // 2):
                for oy in range(-(thick // 2), (thick + 1) // 2):
                    px, py = int(round(x)) + ox, int(round(y)) + oy
                    if self.inside(px, py):
                        self.c.pixel(px, py, color)

    def text(self, x, y, s, color=BLACK, scale=1):
        px, py = self._tx(x), self._ty(y)
        if px is None or py is None:
            return
        self.c.text(int(px), int(py), s, color, scale)

    def axes(self, xticks=None, yticks=None):
        c = self.c
        c.rect(self.x0, self.y0, self.x0 + self.w, self.y0 + self.h, BLACK)
        # ticks
        if xticks is None:
            if self.xlog:
                lo, hi = math.ceil(math.log10(self.xlim[0]) - 1e-9), math.floor(math.log10(self.xlim[1]) + 1e-9)
                xticks = [10 ** e for e in range(lo, hi + 1)]
            else:
                xticks = nice_ticks(*self.xlim)
        if yticks is None:
            if self.ylog:
                lo, hi = math.ceil(math.log10(self.ylim[0]) - 1e-9), math.floor(math.log10(self.ylim[1]) + 1e-9)
                step = max(1, (hi - lo) // 6 + 1)
                yticks = [10 ** e for e in range(lo, hi + 1, step)]
            else:
                yticks = nice_ticks(*self.ylim)
        for xt in xticks:
            px = self._tx(xt)
            if px is None or not (self.x0 - 1 <= px <= self.x0 + self.w + 1):
                continue
            px = int(round(px))
            c.vline(px, self.y0 + self.h - 5, self.y0 + self.h, BLACK)
            for py in range(self.y0, self.y0 + self.h, 3):
                c.pixel(px, py, LIGHT_GRAY)
            c.text_c(px, self.y0 + self.h + 6, fmt_tick(xt), BLACK, 1)
        for yt in yticks:
            py = self._ty(yt)
            if py is None or not (self.y0 - 1 <= py <= self.y0 + self.h + 1):
                continue
            py = int(round(py))
            c.hline(self.x0, self.x0 + 5, py, BLACK)
            for px in range(self.x0, self.x0 + self.w, 3):
                c.pixel(px, py, LIGHT_GRAY)
            s = fmt_tick(yt)
            c.text(self.x0 - 6 * len(s) - 4, py - 3, s, BLACK, 1)
        c.rect(self.x0, self.y0, self.x0 + self.w, self.y0 + self.h, BLACK)
        if self.xlabel:
            c.text_c(self.x0 + self.w // 2, self.y0 + self.h + 20, self.xlabel, BLACK, 1)
        if self.ylabel:
            # write vertically stacked short label at left-top
            c.text(self.x0 - 6 * len(self.ylabel) // 2 - 10 if False else self.x0, self.y0 - 12,
                   self.ylabel, BLACK, 1)
        if self.title:
            c.text_c(self.x0 + self.w // 2, self.y0 + self.h + 34, self.title, BLACK, 1)

    def legend(self, corner='tr', bg=WHITE):
        if not self.legend_items:
            return
        wmax = max(len(s) for s, _, _ in self.legend_items) * 6 + 36
        hgt = 12 * len(self.legend_items) + 6
        if corner == 'tr':
            lx, ly = self.x0 + self.w - wmax - 6, self.y0 + 6
        elif corner == 'tl':
            lx, ly = self.x0 + 6, self.y0 + 6
        elif corner == 'br':
            lx, ly = self.x0 + self.w - wmax - 6, self.y0 + self.h - hgt - 6
        else:
            lx, ly = self.x0 + 6, self.y0 + self.h - hgt - 6
        self.c.rect(lx, ly, lx + wmax, ly + hgt, GRAY, fill=bg)
        for i, (s, col, sty) in enumerate(self.legend_items):
            yy = ly + 8 + 12 * i
            for xx in range(lx + 4, lx + 26):
                d = xx - lx - 4
                if sty == 'dash' and d % 14 > 8:
                    continue
                if sty == 'dot' and d % 6 > 2:
                    continue
                self.c.pixel(xx, yy, col)
                self.c.pixel(xx, yy + 1, col)
            self.c.text(lx + 30, yy - 3, s, BLACK, 1)


class Figure:
    def __init__(self, width, height, title=None):
        self.c = PNGCanvas(width, height, WHITE)
        if title:
            self.c.text_c(width // 2, 8, title, BLACK, 2)

    def panel(self, *a, **k):
        return Panel(self, *a, **k)

    def save(self, path):
        self.c.save(path)
