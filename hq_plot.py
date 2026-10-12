#!/usr/bin/env python3
"""
High-quality, anti-aliased PNG rendering (pure standard library).

Supersampled canvas (draws at ss x resolution, box-filter downsamples) giving
smooth thick curves, round markers, filled polygons and legible text. Includes
a Chart helper for scientific line/scatter plots with grid, ticks, legend, and
a FlowChart helper for process diagrams.
"""

import struct
import zlib
import math
from generate_figures import _FONT

WHITE = (255, 255, 255)


class HQ:
    def __init__(self, W, H, ss=2, bg=WHITE):
        self.W, self.H, self.ss = W, H, ss
        self.w, self.h = W * ss, H * ss
        self.buf = bytearray(bytes(bg) * (self.w * self.h))

    # ---- low level (supersampled integer space) ----
    def _set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i] = c[0]; self.buf[i + 1] = c[1]; self.buf[i + 2] = c[2]

    def _disk(self, cx, cy, r, c):
        r2 = r * r
        for y in range(int(cy - r), int(cy + r) + 1):
            dy = y + 0.5 - cy
            dd = r2 - dy * dy
            if dd < 0:
                continue
            hx = math.sqrt(dd)
            for x in range(int(cx - hx), int(cx + hx) + 1):
                self._set(x, y, c)

    # ---- public (final-pixel float space) ----
    def line(self, x0, y0, x1, y1, c, w=2.0):
        s = self.ss
        X0, Y0, X1, Y1 = x0 * s, y0 * s, x1 * s, y1 * s
        r = max(0.5, w * s / 2.0)
        L = math.hypot(X1 - X0, Y1 - Y0)
        n = max(1, int(L))
        for i in range(n + 1):
            t = i / n
            self._disk(X0 + (X1 - X0) * t, Y0 + (Y1 - Y0) * t, r, c)

    def polyline(self, pts, c, w=2.0):
        for a, b in zip(pts, pts[1:]):
            self.line(a[0], a[1], b[0], b[1], c, w)

    def fill_rect(self, x0, y0, x1, y1, c):
        s = self.ss
        for y in range(int(min(y0, y1) * s), int(max(y0, y1) * s)):
            for x in range(int(min(x0, x1) * s), int(max(x0, x1) * s)):
                self._set(x, y, c)

    def rect(self, x0, y0, x1, y1, c, w=2.0, fill=None):
        if fill:
            self.fill_rect(x0, y0, x1, y1, fill)
        self.line(x0, y0, x1, y0, c, w); self.line(x1, y0, x1, y1, c, w)
        self.line(x1, y1, x0, y1, c, w); self.line(x0, y1, x0, y0, c, w)

    def round_rect(self, x0, y0, x1, y1, c, w=2.0, fill=None, rad=14):
        if fill:
            self.fill_rect(x0 + rad, y0, x1 - rad, y1, fill)
            self.fill_rect(x0, y0 + rad, x1, y1 - rad, fill)
            for (cx, cy) in [(x0 + rad, y0 + rad), (x1 - rad, y0 + rad),
                             (x0 + rad, y1 - rad), (x1 - rad, y1 - rad)]:
                self._disk(cx * self.ss, cy * self.ss, rad * self.ss, fill)
        self.line(x0 + rad, y0, x1 - rad, y0, c, w)
        self.line(x0 + rad, y1, x1 - rad, y1, c, w)
        self.line(x0, y0 + rad, x0, y1 - rad, c, w)
        self.line(x1, y0 + rad, x1, y1 - rad, c, w)
        self._arc(x0 + rad, y0 + rad, rad, 180, 270, c, w)
        self._arc(x1 - rad, y0 + rad, rad, 270, 360, c, w)
        self._arc(x0 + rad, y1 - rad, rad, 90, 180, c, w)
        self._arc(x1 - rad, y1 - rad, rad, 0, 90, c, w)

    def _arc(self, cx, cy, r, a0, a1, c, w):
        s = self.ss
        steps = max(6, int((a1 - a0) / 4))
        pts = []
        for i in range(steps + 1):
            a = math.radians(a0 + (a1 - a0) * i / steps)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        self.polyline(pts, c, w)

    def disk(self, x, y, r, c):
        self._disk(x * self.ss, y * self.ss, r * self.ss, c)

    def ring(self, x, y, r, c, w=2.0, fill=None):
        if fill:
            self.disk(x, y, r, fill)
        s = self.ss
        cx, cy, rr = x * s, y * s, r * s
        rw = max(0.5, w * s / 2)
        steps = int(2 * math.pi * rr) + 8
        for i in range(steps):
            a = 2 * math.pi * i / steps
            self._disk(cx + rr * math.cos(a), cy + rr * math.sin(a), rw, c)

    def fill_poly(self, pts, c):
        s = self.ss
        ys = [p[1] * s for p in pts]
        y0, y1 = int(min(ys)), int(max(ys)) + 1
        P = [(p[0] * s, p[1] * s) for p in pts]
        for y in range(y0, y1):
            xs = []
            for i in range(len(P)):
                ax, ay = P[i]; bx, by = P[(i + 1) % len(P)]
                if (ay <= y < by) or (by <= y < ay):
                    xs.append(ax + (bx - ax) * (y - ay) / (by - ay))
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                for x in range(int(xs[j]), int(xs[j + 1]) + 1):
                    self._set(x, y, c)

    def poly(self, pts, c, w=2.0, fill=None):
        if fill:
            self.fill_poly(pts, fill)
        self.polyline(pts + [pts[0]], c, w)

    def arrow(self, x0, y0, x1, y1, c, w=2.0, head=14):
        self.line(x0, y0, x1, y1, c, w)
        ang = math.atan2(y1 - y0, x1 - x0)
        for da in (0.4, -0.4):
            hx = x1 - head * math.cos(ang - da)
            hy = y1 - head * math.sin(ang - da)
            self.line(x1, y1, hx, hy, c, w)

    def text(self, x, y, s, c, size=20, align='l', bold=False):
        cell = size / 7.0
        width = len(s) * 6 * cell
        if align == 'c':
            x -= width / 2
        elif align == 'r':
            x -= width
        bump = cell * 0.35 if bold else 0
        cx = x
        for ch in s:
            bm = _FONT.get(ch)
            if bm is None:
                cx += 6 * cell; continue
            for ri, row in enumerate(bm):
                for ci in range(5):
                    if row & (1 << (4 - ci)):
                        px = cx + ci * cell; py = y + ri * cell
                        self.fill_rect(px, py, px + cell + bump, py + cell + bump, c)
            cx += 6 * cell

    def text_v(self, x, y, s, c, size=20):
        """Vertical (rotated 90 deg CCW) text, read bottom-to-top."""
        cell = size / 7.0
        cy = y
        for ch in s:
            bm = _FONT.get(ch)
            if bm is None:
                cy -= 6 * cell; continue
            for ri, row in enumerate(bm):
                for ci in range(5):
                    if row & (1 << (4 - ci)):
                        # rotate: col->up, row->right
                        px = x + ri * cell
                        py = cy - ci * cell
                        self.fill_rect(px, py, px + cell, py + cell, c)
            cy -= 6 * cell

    # ---- output ----
    def _down(self):
        W, H, s = self.W, self.H, self.ss
        out = bytearray(W * H * 3)
        inv = 1.0 / (s * s)
        srcw = self.w
        buf = self.buf
        for Y in range(H):
            yb = Y * s
            for X in range(W):
                xb = X * s * 3
                r = g = b = 0
                for dy in range(s):
                    idx = ((yb + dy) * srcw) * 3 + xb
                    for dx in range(s):
                        r += buf[idx]; g += buf[idx + 1]; b += buf[idx + 2]
                        idx += 3
                o = (Y * W + X) * 3
                out[o] = int(r * inv); out[o + 1] = int(g * inv); out[o + 2] = int(b * inv)
        return out

    def save(self, path):
        data = self._down()
        W, H = self.W, self.H
        raw = bytearray()
        for y in range(H):
            raw.append(0)
            raw.extend(data[y * W * 3:(y + 1) * W * 3])
        comp = zlib.compress(bytes(raw), 9)

        def chunk(t, d):
            cc = t + d
            return struct.pack('>I', len(d)) + cc + struct.pack('>I', zlib.crc32(cc) & 0xffffffff)
        with open(path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)))
            f.write(chunk(b'IDAT', comp))
            f.write(chunk(b'IEND', b''))


# ----------------------------------------------------------------- Chart
BLACK = (20, 20, 20)
GRIDC = (210, 210, 214)
AXISC = (40, 40, 40)


class Chart:
    def __init__(self, W=1520, H=950, xlim=(0, 1), ylim=(0, 1),
                 xlabel='', ylabel='', title='', ss=2, legend_w=330):
        self.c = HQ(W, H, ss=ss)
        self.W, self.H = W, H
        self.xlim, self.ylim = xlim, ylim
        self.ml, self.mr, self.mt, self.mb = 150, legend_w, 95, 120
        self.px0, self.px1 = self.ml, W - self.mr
        self.py0, self.py1 = H - self.mb, self.mt
        self.xlabel, self.ylabel, self.title = xlabel, ylabel, title
        self._leg = []

    def X(self, x):
        a, b = self.xlim
        return self.px0 + (x - a) / (b - a) * (self.px1 - self.px0)

    def Y(self, y):
        a, b = self.ylim
        return self.py0 + (y - a) / (b - a) * (self.py1 - self.py0)

    def axes(self, xt, yt, xf='{:.1f}', yf='{:.1f}'):
        c = self.c
        for xv in xt:
            px = self.X(xv)
            c.line(px, self.py1, px, self.py0, GRIDC, 1.0)
        for yv in yt:
            py = self.Y(yv)
            c.line(self.px0, py, self.px1, py, GRIDC, 1.0)
        if self.ylim[0] < 0 < self.ylim[1]:
            c.line(self.px0, self.Y(0), self.px1, self.Y(0), (150, 150, 150), 1.5)
        c.rect(self.px0, self.py1, self.px1, self.py0, AXISC, 2.4)
        for xv in xt:
            px = self.X(xv)
            c.line(px, self.py0, px, self.py0 + 9, AXISC, 2.0)
            c.text(px, self.py0 + 16, xf.format(xv), BLACK, size=22, align='c')
        for yv in yt:
            py = self.Y(yv)
            c.line(self.px0 - 9, py, self.px0, py, AXISC, 2.0)
            c.text(self.px0 - 16, py - 8, yf.format(yv), BLACK, size=22, align='r')
        c.text((self.px0 + self.px1) / 2, self.H - 44, self.xlabel, BLACK, size=26, align='c')
        c.text_v(44, (self.py0 + self.py1) / 2 + len(self.ylabel) * 8, self.ylabel, BLACK, size=26)
        c.text((self.px0 + self.px1) / 2, 34, self.title, (25, 55, 95), size=30, align='c', bold=True)

    def line(self, xs, ys, color, label, w=2.6):
        pts = [(self.X(x), self.Y(y)) for x, y in zip(xs, ys)]
        self.c.polyline(pts, color, w)
        self._leg.append(('line', color, label))

    def marks(self, xs, ys, color, label, r=6):
        for x, y in zip(xs, ys):
            self.c.ring(self.X(x), self.Y(y), r, (255, 255, 255), 2.0, fill=color)
        self._leg.append(('mark', color, label))

    def legend(self):
        c = self.c
        lx = self.px1 + 24
        ly = self.py1 + 6
        bh = 32 * len(self._leg) + 16
        c.rect(lx - 12, ly - 12, min(lx + 290, self.W - 8), ly + bh, AXISC, 1.8, fill=(250, 250, 252))
        for i, (k, col, lab) in enumerate(self._leg):
            yy = ly + i * 32 + 6
            if k == 'line':
                c.line(lx, yy, lx + 36, yy, col, 3.6)
            else:
                c.ring(lx + 18, yy, 6, (255, 255, 255), 2.0, fill=col)
            c.text(lx + 48, yy - 8, lab, BLACK, size=18)

    def save(self, path):
        self.c.save(path)
