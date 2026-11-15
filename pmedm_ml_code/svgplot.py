"""Minimal SVG plotting helpers (standard library only) and PNG rasterisation via
headless Chromium. Used to draw every figure of the manuscript from results.json."""

import math
import os
import subprocess

FONT = "Noto Sans, Arial, Helvetica, sans-serif"
CHROME_CANDIDATES = [
    "/inner_container/opt/playwright/chromium_headless_shell-1232/chrome-headless-shell-linux64/chrome-headless-shell",
    "chromium", "google-chrome", "chrome-headless-shell",
]

PALETTE = {
    "graphite": "#1f4e79", "alumina": "#c55a11", "none": "#548235",
    "grey": "#7f7f7f", "light": "#d9d9d9", "red": "#c00000", "gold": "#bf9000",
    "purple": "#7030a0", "teal": "#0b7a75", "black": "#222222",
}


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def nice_ticks(lo, hi, n=5):
    if hi <= lo:
        hi = lo + 1.0
    span = hi - lo
    raw = span / max(n, 1)
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        step = m * mag
        if span / step <= n + 0.5:
            break
    start = math.ceil(lo / step - 1e-9) * step
    ticks = []
    v = start
    while v <= hi + 1e-9 * step:
        ticks.append(round(v, 10))
        v += step
    return ticks


def fmt_tick(v):
    if abs(v) >= 100 or float(v).is_integer():
        return "%d" % round(v)
    if abs(v) >= 1:
        return ("%.1f" % v).rstrip("0").rstrip(".")
    return ("%.2f" % v).rstrip("0").rstrip(".")


class Axes:
    def __init__(self, fig, x, y, w, h, xlim, ylim, xlabel="", ylabel="", title="",
                 xlog=False, ylog=False, xticks=None, yticks=None, grid=True,
                 xticklabels=None, panel=None):
        self.fig, self.x, self.y, self.w, self.h = fig, x, y, w, h
        self.xlim, self.ylim, self.xlog, self.ylog = xlim, ylim, xlog, ylog
        self.els = []
        self._frame(xlabel, ylabel, title, xticks, yticks, grid, xticklabels, panel)

    def tx(self, v):
        lo, hi = self.xlim
        if self.xlog:
            v, lo, hi = math.log10(v), math.log10(lo), math.log10(hi)
        return self.x + (v - lo) / (hi - lo) * self.w

    def ty(self, v):
        lo, hi = self.ylim
        if self.ylog:
            v, lo, hi = math.log10(v), math.log10(lo), math.log10(hi)
        return self.y + self.h - (v - lo) / (hi - lo) * self.h

    def _frame(self, xlabel, ylabel, title, xticks, yticks, grid, xticklabels, panel):
        f = self.fig
        if xticks is None:
            xticks = ([10 ** k for k in range(int(math.floor(math.log10(self.xlim[0]))),
                                               int(math.ceil(math.log10(self.xlim[1]))) + 1)
                       if self.xlim[0] <= 10 ** k <= self.xlim[1]]
                      if self.xlog else nice_ticks(*self.xlim))
        if yticks is None:
            yticks = nice_ticks(*self.ylim)
        for t in xticks:
            px = self.tx(t)
            if grid:
                f.line(px, self.y, px, self.y + self.h, "#ececec", 1)
            f.line(px, self.y + self.h, px, self.y + self.h + 5, "#333", 1)
            lab = xticklabels.get(t, fmt_tick(t)) if isinstance(xticklabels, dict) else \
                (("%g" % t) if self.xlog else fmt_tick(t))
            f.text(px, self.y + self.h + 19, lab, 12, anchor="middle")
        for t in yticks:
            py = self.ty(t)
            if grid:
                f.line(self.x, py, self.x + self.w, py, "#ececec", 1)
            f.line(self.x - 5, py, self.x, py, "#333", 1)
            f.text(self.x - 8, py + 4, fmt_tick(t), 12, anchor="end")
        f.rect(self.x, self.y, self.w, self.h, stroke="#333", fill="none", sw=1.1)
        if xlabel:
            f.text(self.x + self.w / 2, self.y + self.h + 40, xlabel, 13.5, anchor="middle")
        if ylabel:
            f.text(self.x - 46, self.y + self.h / 2, ylabel, 13.5, anchor="middle", rotate=-90)
        if title:
            f.text(self.x + self.w / 2, self.y - 9, title, 13.5, anchor="middle", weight="600")
        if panel:
            f.text(self.x - 52, self.y - 9, panel, 15, anchor="start", weight="700")

    def clip_x(self, v):
        return min(max(v, self.xlim[0]), self.xlim[1])

    def clip_y(self, v):
        return min(max(v, self.ylim[0]), self.ylim[1])

    def line(self, xs, ys, color, sw=1.8, dash=None, opacity=1.0):
        pts = " ".join("%.2f,%.2f" % (self.tx(a), self.ty(b)) for a, b in zip(xs, ys))
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.fig.raw('<polyline points="%s" fill="none" stroke="%s" stroke-width="%.2f"%s '
                     'stroke-opacity="%.2f" stroke-linejoin="round"/>' % (pts, color, sw, d, opacity))

    def band(self, xs, lo, hi, color, opacity=0.18):
        pts = ["%.2f,%.2f" % (self.tx(a), self.ty(b)) for a, b in zip(xs, hi)]
        pts += ["%.2f,%.2f" % (self.tx(a), self.ty(b)) for a, b in zip(reversed(xs), reversed(lo))]
        self.fig.raw('<polygon points="%s" fill="%s" fill-opacity="%.2f" stroke="none"/>'
                     % (" ".join(pts), color, opacity))

    def scatter(self, xs, ys, color, r=4.2, marker="o", hollow=False, sw=1.3, opacity=1.0,
                edge="white"):
        for a, b in zip(xs, ys):
            self.fig.marker(self.tx(a), self.ty(b), marker, r, color, hollow, sw, opacity, edge)

    def errorbar(self, xs, ys, lo, hi, color, sw=1.0, cap=3):
        for a, b, l, h in zip(xs, ys, lo, hi):
            px = self.tx(a)
            y1, y2 = self.ty(self.clip_y(l)), self.ty(self.clip_y(h))
            self.fig.line(px, y1, px, y2, color, sw)
            self.fig.line(px - cap, y1, px + cap, y1, color, sw)
            self.fig.line(px - cap, y2, px + cap, y2, color, sw)

    def hline(self, v, color="#888", sw=1.0, dash="4,3"):
        py = self.ty(v)
        self.fig.line(self.x, py, self.x + self.w, py, color, sw, dash)

    def diag(self, color="#888", sw=1.0, dash="4,3"):
        lo = max(self.xlim[0], self.ylim[0])
        hi = min(self.xlim[1], self.ylim[1])
        self.fig.line(self.tx(lo), self.ty(lo), self.tx(hi), self.ty(hi), color, sw, dash)

    def text(self, xv, yv, s, size=11.5, anchor="start", color="#222", weight="normal", dx=0, dy=0):
        self.fig.text(self.tx(xv) + dx, self.ty(yv) + dy, s, size, anchor=anchor, color=color,
                      weight=weight)


class Figure:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.parts = ['<rect x="0" y="0" width="%d" height="%d" fill="white"/>' % (width, height)]

    def raw(self, s):
        self.parts.append(s)

    def line(self, x1, y1, x2, y2, color="#333", sw=1.0, dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" '
                          'stroke-width="%.2f"%s/>' % (x1, y1, x2, y2, color, sw, d))

    def rect(self, x, y, w, h, stroke="none", fill="none", sw=1.0, rx=0, opacity=1.0):
        self.parts.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.1f" '
                          'stroke="%s" fill="%s" stroke-width="%.2f" fill-opacity="%.2f"/>'
                          % (x, y, w, h, rx, stroke, fill, sw, opacity))

    def text(self, x, y, s, size=12, anchor="start", color="#222", weight="normal", rotate=None,
             italic=False):
        tr = ' transform="rotate(%d %.2f %.2f)"' % (rotate, x, y) if rotate else ""
        st = ' font-style="italic"' if italic else ""
        self.parts.append('<text x="%.2f" y="%.2f" font-family="%s" font-size="%.1f" '
                          'text-anchor="%s" fill="%s" font-weight="%s"%s%s>%s</text>'
                          % (x, y, FONT, size, anchor, color, weight, tr, st, esc(s)))

    def marker(self, x, y, kind, r, color, hollow=False, sw=1.3, opacity=1.0, edge="white"):
        fill = "white" if hollow else color
        attrs = 'fill="%s" stroke="%s" stroke-width="%.2f" fill-opacity="%.2f"' % (
            fill, color if hollow else (edge or "none"), sw if edge else 0.0, opacity)
        if hollow:
            attrs = 'fill="white" fill-opacity="0.0" stroke="%s" stroke-width="%.2f"' % (color, sw)
        if kind == "o":
            self.parts.append('<circle cx="%.2f" cy="%.2f" r="%.2f" %s/>' % (x, y, r, attrs))
        elif kind == "s":
            self.parts.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" %s/>'
                              % (x - r, y - r, 2 * r, 2 * r, attrs))
        elif kind == "^":
            pts = "%.2f,%.2f %.2f,%.2f %.2f,%.2f" % (x, y - 1.2 * r, x - 1.1 * r, y + 0.8 * r,
                                                     x + 1.1 * r, y + 0.8 * r)
            self.parts.append('<polygon points="%s" %s/>' % (pts, attrs))
        elif kind == "v":
            pts = "%.2f,%.2f %.2f,%.2f %.2f,%.2f" % (x, y + 1.2 * r, x - 1.1 * r, y - 0.8 * r,
                                                     x + 1.1 * r, y - 0.8 * r)
            self.parts.append('<polygon points="%s" %s/>' % (pts, attrs))
        elif kind == "D":
            pts = "%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" % (x, y - 1.3 * r, x + 1.1 * r, y,
                                                               x, y + 1.3 * r, x - 1.1 * r, y)
            self.parts.append('<polygon points="%s" %s/>' % (pts, attrs))
        elif kind == "*":
            pts = []
            for k in range(10):
                ang = -math.pi / 2 + k * math.pi / 5
                rr = 1.6 * r if k % 2 == 0 else 0.7 * r
                pts.append("%.2f,%.2f" % (x + rr * math.cos(ang), y + rr * math.sin(ang)))
            self.parts.append('<polygon points="%s" fill="%s" stroke="#222" stroke-width="0.8"/>'
                              % (" ".join(pts), color))
        elif kind == "x":
            self.line(x - r, y - r, x + r, y + r, color, sw + 0.4)
            self.line(x - r, y + r, x + r, y - r, color, sw + 0.4)

    def legend(self, x, y, items, size=11.5, row_h=18, box=True, cols=1, col_w=170):
        n = len(items)
        rows = int(math.ceil(n / cols))
        if box:
            self.rect(x - 6, y - 13, cols * col_w + 4, rows * row_h + 6, stroke="#bbb",
                      fill="white", sw=0.8, opacity=0.92)
        for k, it in enumerate(items):
            c, r_ = divmod(k, rows)
            xx, yy = x + c * col_w, y + r_ * row_h
            kind = it.get("kind", "o")
            if kind == "line":
                self.line(xx, yy - 4, xx + 22, yy - 4, it["color"], it.get("sw", 2.0), it.get("dash"))
            elif kind == "band":
                self.rect(xx, yy - 10, 22, 11, fill=it["color"], opacity=0.25)
            elif kind == "bar":
                self.rect(xx + 4, yy - 11, 14, 12, fill=it["color"], stroke="#333", sw=0.5)
            else:
                self.marker(xx + 11, yy - 4, kind, it.get("r", 4.5), it["color"],
                            it.get("hollow", False))
            self.text(xx + 30, yy, it["label"], size)

    def svg(self):
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
                % (self.width, self.height, self.width, self.height) + "".join(self.parts) + "</svg>")

    def save(self, path_png, scale=3):
        svg_path = os.path.splitext(path_png)[0] + ".svg"
        with open(svg_path, "w") as fh:
            fh.write(self.svg())
        html_path = os.path.splitext(path_png)[0] + ".tmp.html"
        with open(html_path, "w") as fh:
            fh.write('<html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;'
                     'background:white}</style></head><body>' + self.svg() + "</body></html>")
        chrome = next((c for c in CHROME_CANDIDATES if os.path.exists(c)), CHROME_CANDIDATES[1])
        cmd = [chrome, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
               "--force-device-scale-factor=%d" % scale,
               "--window-size=%d,%d" % (self.width, self.height),
               "--screenshot=%s" % path_png, "file://" + html_path]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       timeout=120)
        os.remove(html_path)
        return path_png
