#!/usr/bin/env python3
"""Small standard-library plotting helpers (line plots, heatmaps) built on the
PNGCanvas class from ../generate_figures.py."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from generate_figures import PNGCanvas  # noqa: E402

BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LGRAY = (225, 225, 225)
WHITE = (255, 255, 255)
PALETTE = [(31, 119, 180), (214, 39, 40), (44, 160, 44), (148, 103, 189),
           (255, 127, 14), (140, 86, 75), (23, 190, 207), (127, 127, 127)]


def _fmt(v):
    if v == 0:
        return '0'
    a = abs(v)
    if a >= 1e4 or a < 1e-2:
        e = int(math.floor(math.log10(a)))
        m = v / 10 ** e
        return ('%g' % round(m, 2)) + 'e' + str(e) if abs(m - 1) > 1e-9 else '1e' + str(e)
    return '%g' % round(v, 3)


def nice_ticks(lo, hi, n=5):
    if hi <= lo:
        hi = lo + 1
    span = hi - lo
    step = 10 ** math.floor(math.log10(span / n))
    for m in (1, 2, 2.5, 5, 10):
        if span / (step * m) <= n:
            step *= m
            break
    t = math.ceil(lo / step - 1e-9) * step
    out = []
    while t <= hi + 1e-9 * span:
        out.append(round(t, 10))
        t += step
    return out


class Axes:
    def __init__(self, cv, x0, y0, w, h, xlim, ylim, logy=False, logx=False):
        self.cv, self.x0, self.y0, self.w, self.h = cv, x0, y0, w, h
        self.xlim, self.ylim, self.logy, self.logx = xlim, ylim, logy, logx

    def _tx(self, x):
        lo, hi = self.xlim
        if self.logx:
            x, lo, hi = math.log10(max(x, 1e-300)), math.log10(lo), math.log10(hi)
        return int(self.x0 + (x - lo) / (hi - lo) * self.w)

    def _ty(self, y):
        lo, hi = self.ylim
        if self.logy:
            y, lo, hi = math.log10(max(y, 1e-300)), math.log10(lo), math.log10(hi)
        f = (y - lo) / (hi - lo)
        f = min(max(f, -0.02), 1.02)
        return int(self.y0 + self.h - f * self.h)

    def frame(self, xlabel='', ylabel='', title='', xticks=None, yticks=None, grid=True, s=2):
        cv = self.cv
        if xticks is None:
            xticks = ([10 ** k for k in range(math.ceil(math.log10(self.xlim[0])), math.floor(math.log10(self.xlim[1])) + 1)]
                      if self.logx else nice_ticks(*self.xlim))
        if yticks is None:
            yticks = ([10 ** k for k in range(math.ceil(math.log10(self.ylim[0]) - 1e-9), math.floor(math.log10(self.ylim[1]) + 1e-9) + 1)]
                      if self.logy else nice_ticks(*self.ylim))
        for xt in xticks:
            px = self._tx(xt)
            if grid:
                cv.vline(px, self.y0, self.y0 + self.h, LGRAY)
            cv.vline(px, self.y0 + self.h, self.y0 + self.h + 6, BLACK)
            cv.text_c(px, self.y0 + self.h + 10, _fmt(xt), BLACK, s)
        for yt in yticks:
            py = self._ty(yt)
            if grid:
                cv.hline(self.x0, self.x0 + self.w, py, LGRAY)
            cv.hline(self.x0 - 6, self.x0, py, BLACK)
            lab = _fmt(yt)
            cv.text(self.x0 - 10 - len(lab) * 6 * s, py - 3 * s, lab, BLACK, s)
        cv.rect(self.x0, self.y0, self.x0 + self.w, self.y0 + self.h, BLACK)
        if xlabel:
            cv.text_c(self.x0 + self.w // 2, self.y0 + self.h + 34, xlabel, BLACK, s)
        if ylabel:
            # vertical label: draw characters stacked is unreadable; put it above the axis instead
            cv.text(self.x0 - 10, self.y0 - 22, ylabel, BLACK, s)
        if title:
            cv.text_c(self.x0 + self.w // 2, self.y0 - 48, title, BLACK, s + 0)

    def plot(self, xs, ys, color, thick=3, dash=False):
        pts = [(self._tx(x), self._ty(y)) for x, y in zip(xs, ys)
               if (not self.logy or y > 0) and self.xlim[0] <= x <= self.xlim[1]]
        if not dash:
            for i in range(1, len(pts)):
                self.cv.line(pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1], color, thick)
            return
        # dashed: walk along the polyline in ~1 px steps, 12 px on / 10 px off
        acc = 0.0
        for i in range(1, len(pts)):
            (xa, ya), (xb, yb) = pts[i - 1], pts[i]
            seg = math.hypot(xb - xa, yb - ya)
            n = max(1, int(seg))
            for k in range(n):
                if (acc % 22) < 12:
                    x1 = int(xa + (xb - xa) * k / n); y1 = int(ya + (yb - ya) * k / n)
                    x2 = int(xa + (xb - xa) * (k + 1) / n); y2 = int(ya + (yb - ya) * (k + 1) / n)
                    self.cv.line(x1, y1, x2, y2, color, thick)
                acc += seg / n

    def scatter(self, xs, ys, color, r=4):
        for x, y in zip(xs, ys):
            self.cv.circle(self._tx(x), self._ty(y), r, color, color)

    def vmark(self, x, color=GRAY, label='', s=2, dy=8):
        px = self._tx(x)
        for y in range(self.y0, self.y0 + self.h, 8):
            self.cv.vline(px, y, y + 4, color)
        if label:
            self.cv.text(px + 6, self.y0 + dy, label, color, s)

    def hmark(self, y, color=GRAY, label='', s=2):
        py = self._ty(y)
        for x in range(self.x0, self.x0 + self.w, 8):
            self.cv.hline(x, x + 4, py, color)
        if label:
            self.cv.text(self.x0 + 8, py - 18, label, color, s)


def legend(cv, x, y, items, s=2, box=True):
    """items: list of (label, color, dashed?)"""
    wmax = max(len(l) for l, *_ in items) * 6 * s + 60
    hh = len(items) * 11 * s + 12
    if box:
        cv.rect(x, y, x + wmax, y + hh, GRAY, WHITE)
    for i, it in enumerate(items):
        lab, col = it[0], it[1]
        dash = it[2] if len(it) > 2 else False
        yy = y + 10 + i * 11 * s + 3 * s
        if dash:
            for k in range(0, 36, 12):
                cv.line(x + 8 + k, yy, x + 14 + k, yy, col, 3)
        else:
            cv.line(x + 8, yy, x + 44, yy, col, 3)
        cv.text(x + 52, yy - 3 * s, lab, BLACK, s)


def heatmap(cv, x0, y0, w, h, grid, colors, xvals, yvals, xlabel, ylabel, title,
            xtick_every=1, ytick_every=1, s=2, xfmt=_fmt, yfmt=_fmt):
    """grid[j][i] -> category key (row j = yvals[j], bottom row j=0)."""
    nx, ny = len(xvals), len(yvals)
    cw, ch = w / nx, h / ny
    for j in range(ny):
        for i in range(nx):
            c = colors[grid[j][i]]
            cv.fill_rect(int(x0 + i * cw), int(y0 + h - (j + 1) * ch), int(x0 + (i + 1) * cw) - 1, int(y0 + h - j * ch) - 1, c)
    cv.rect(x0, y0, x0 + w, y0 + h, BLACK)
    for i in range(0, nx, xtick_every):
        px = int(x0 + (i + 0.5) * cw)
        cv.vline(px, y0 + h, y0 + h + 6, BLACK)
        cv.text_c(px, y0 + h + 10, xfmt(xvals[i]), BLACK, s)
    for j in range(0, ny, ytick_every):
        py = int(y0 + h - (j + 0.5) * ch)
        cv.hline(x0 - 6, x0, py, BLACK)
        lab = yfmt(yvals[j])
        cv.text(x0 - 10 - len(lab) * 6 * s, py - 3 * s, lab, BLACK, s)
    cv.text_c(x0 + w // 2, y0 + h + 34, xlabel, BLACK, s)
    cv.text(x0 - 10, y0 - 22, ylabel, BLACK, s)
    if title:
        cv.text_c(x0 + w // 2, y0 - 48, title, BLACK, s)


def swatch_legend(cv, x, y, items, s=2):
    for i, (lab, col) in enumerate(items):
        yy = y + i * 11 * s
        cv.fill_rect(x, yy, x + 22, yy + 7 * s, col)
        cv.rect(x, yy, x + 22, yy + 7 * s, BLACK)
        cv.text(x + 32, yy, lab, BLACK, s)


def panel_label(cv, x, y, lab):
    """Panel letters are carried in the panel titles; kept as a no-op for API stability."""
    return None
