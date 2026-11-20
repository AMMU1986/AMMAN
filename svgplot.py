#!/usr/bin/env python3
"""Minimal SVG plotting helpers (standard library only) + PNG rasterisation
through the headless Chromium shipped with Playwright in this sandbox."""

import math
import os
import subprocess

CHROME_CANDIDATES = [
    "/inner_container/opt/playwright/chromium_headless_shell-1232/chrome-headless-shell-linux64/chrome-headless-shell",
    "/inner_container/opt/playwright/chromium-1232/chrome-linux64/chrome",
]

FONT = "DejaVu Sans, Arial, Helvetica, sans-serif"
COLORS = ["#1f4e79", "#c00000", "#2e8b57", "#ed7d31", "#7030a0", "#000000", "#bf9000", "#5b9bd5"]
DASHES = ["", "8,4", "3,3", "10,3,2,3", "2,2", "", "6,2", "4,4"]


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class Axes:
    """A single log/linear axes panel inside an SVG canvas."""

    def __init__(self, x0, y0, w, h, xlim, ylim, xlog=True, ylog=True,
                 xlabel="", ylabel="", title=""):
        self.x0, self.y0, self.w, self.h = x0, y0, w, h
        self.xlim, self.ylim = xlim, ylim
        self.xlog, self.ylog = xlog, ylog
        self.xlabel, self.ylabel, self.title = xlabel, ylabel, title
        self.items = []
        self.legend_items = []

    def tx(self, x):
        a, b = self.xlim
        if self.xlog:
            x, a, b = math.log10(max(x, 1e-300)), math.log10(a), math.log10(b)
        return self.x0 + (x - a) / (b - a) * self.w

    def ty(self, y):
        a, b = self.ylim
        if self.ylog:
            y, a, b = math.log10(max(y, 1e-300)), math.log10(a), math.log10(b)
        return self.y0 + self.h - (y - a) / (b - a) * self.h

    def line(self, xs, ys, color="#000", width=2.0, dash="", label=None):
        pts = []
        segs = []
        for x, y in zip(xs, ys):
            if y is None or (isinstance(y, float) and (math.isnan(y) or math.isinf(y))):
                if pts:
                    segs.append(pts)
                pts = []
                continue
            px, py = self.tx(x), self.ty(y)
            py = min(max(py, self.y0 - 2), self.y0 + self.h + 2)
            pts.append("%.2f,%.2f" % (px, py))
        if pts:
            segs.append(pts)
        for s in segs:
            self.items.append('<polyline fill="none" stroke="%s" stroke-width="%.1f" %s points="%s"/>'
                              % (color, width, ('stroke-dasharray="%s"' % dash) if dash else "", " ".join(s)))
        if label:
            self.legend_items.append(("line", color, dash, width, label))

    def markers(self, xs, ys, color="#000", shape="o", size=4.5, label=None):
        for x, y in zip(xs, ys):
            px, py = self.tx(x), self.ty(y)
            if shape == "o":
                self.items.append('<circle cx="%.2f" cy="%.2f" r="%.1f" fill="white" stroke="%s" stroke-width="1.6"/>'
                                  % (px, py, size, color))
            elif shape == "s":
                self.items.append('<rect x="%.2f" y="%.2f" width="%.1f" height="%.1f" fill="white" stroke="%s" stroke-width="1.6"/>'
                                  % (px - size, py - size, 2 * size, 2 * size, color))
            else:
                self.items.append('<path d="M%.2f,%.2f L%.2f,%.2f L%.2f,%.2f Z" fill="white" stroke="%s" stroke-width="1.6"/>'
                                  % (px, py - size, px - size, py + size, px + size, py + size, color))
        if label:
            self.legend_items.append(("marker", color, shape, size, label))

    def vline(self, x, color="#666", dash="4,3", text=None):
        px = self.tx(x)
        self.items.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.3" stroke-dasharray="%s"/>'
                          % (px, self.y0, px, self.y0 + self.h, color, dash))
        if text:
            self.items.append('<text x="%.2f" y="%.2f" font-size="12" fill="%s" font-family="%s">%s</text>'
                              % (px + 4, self.y0 + 16, color, FONT, esc(text)))

    def hline(self, y, color="#666", dash="4,3", text=None):
        py = self.ty(y)
        self.items.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.3" stroke-dasharray="%s"/>'
                          % (self.x0, py, self.x0 + self.w, py, color, dash))
        if text:
            self.items.append('<text x="%.2f" y="%.2f" font-size="12" fill="%s" font-family="%s">%s</text>'
                              % (self.x0 + 6, py - 5, color, FONT, esc(text)))

    def text(self, x, y, s, size=13, color="#000", anchor="start"):
        self.items.append('<text x="%.2f" y="%.2f" font-size="%d" fill="%s" text-anchor="%s" font-family="%s">%s</text>'
                          % (self.tx(x), self.ty(y), size, color, anchor, FONT, esc(s)))

    def raw(self, s):
        self.items.append(s)

    def _ticks(self, lim, log):
        a, b = lim
        if log:
            lo, hi = math.floor(math.log10(a) + 1e-9), math.ceil(math.log10(b) - 1e-9)
            step = 1 if hi - lo <= 8 else 2
            return [10 ** e for e in range(lo, hi + 1, step) if a * 0.999 <= 10 ** e <= b * 1.001]
        span = b - a
        raw = span / 6
        mag = 10 ** math.floor(math.log10(raw))
        for m in (1, 2, 2.5, 5, 10):
            if raw <= m * mag:
                st = m * mag
                break
        t = math.ceil(a / st) * st
        out = []
        while t <= b + 1e-12 * span:
            out.append(round(t, 12))
            t += st
        return out

    @staticmethod
    def _fmt(v, log):
        if log:
            e = int(round(math.log10(v)))
            sup = str(e).replace("-", "\u2212")
            return "10<tspan baseline-shift=\"super\" font-size=\"10\">%s</tspan>" % sup
        if abs(v) < 1e-12:
            return "0"
        if abs(v) >= 1000 or abs(v) < 0.01:
            return "%.0e" % v
        s = ("%.3f" % v).rstrip("0").rstrip(".")
        return s.replace("-", "\u2212")

    def render(self, legend_pos="ur", legend_cols=1):
        out = []
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="white" stroke="#000" stroke-width="1.2"/>'
                   % (self.x0, self.y0, self.w, self.h))
        # grid + ticks
        for t in self._ticks(self.xlim, self.xlog):
            px = self.tx(t)
            out.append('<line x1="%.2f" y1="%.1f" x2="%.2f" y2="%.1f" stroke="#e3e3e3" stroke-width="1"/>' % (px, self.y0, px, self.y0 + self.h))
            out.append('<line x1="%.2f" y1="%.1f" x2="%.2f" y2="%.1f" stroke="#000" stroke-width="1"/>' % (px, self.y0 + self.h, px, self.y0 + self.h - 6))
            out.append('<text x="%.2f" y="%.1f" font-size="13" text-anchor="middle" font-family="%s">%s</text>'
                       % (px, self.y0 + self.h + 20, FONT, self._fmt(t, self.xlog)))
        for t in self._ticks(self.ylim, self.ylog):
            py = self.ty(t)
            out.append('<line x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="#e3e3e3" stroke-width="1"/>' % (self.x0, py, self.x0 + self.w, py))
            out.append('<line x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="#000" stroke-width="1"/>' % (self.x0, py, self.x0 + 6, py))
            out.append('<text x="%.1f" y="%.2f" font-size="13" text-anchor="end" font-family="%s">%s</text>'
                       % (self.x0 - 7, py + 4.5, FONT, self._fmt(t, self.ylog)))
        out.append('<clipPath id="c%d"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath>'
                   % (id(self) % 100000, self.x0, self.y0, self.w, self.h))
        out.append('<g clip-path="url(#c%d)">' % (id(self) % 100000))
        out.extend(self.items)
        out.append('</g>')
        # labels
        out.append('<text x="%.1f" y="%.1f" font-size="15" text-anchor="middle" font-family="%s">%s</text>'
                   % (self.x0 + self.w / 2, self.y0 + self.h + 44, FONT, self.xlabel))
        out.append('<text transform="translate(%.1f,%.1f) rotate(-90)" font-size="15" text-anchor="middle" font-family="%s">%s</text>'
                   % (self.x0 - 62, self.y0 + self.h / 2, FONT, self.ylabel))
        if self.title:
            out.append('<text x="%.1f" y="%.1f" font-size="15" font-weight="bold" text-anchor="start" font-family="%s">%s</text>'
                       % (self.x0, self.y0 - 10, FONT, self.title))
        # legend
        if self.legend_items:
            n = len(self.legend_items)
            rows = math.ceil(n / legend_cols)
            lw = 215 * legend_cols
            lh = 20 * rows + 10
            if legend_pos == "ur":
                lx, ly = self.x0 + self.w - lw - 8, self.y0 + 8
            elif legend_pos == "ul":
                lx, ly = self.x0 + 8, self.y0 + 8
            elif legend_pos == "lr":
                lx, ly = self.x0 + self.w - lw - 8, self.y0 + self.h - lh - 8
            else:
                lx, ly = self.x0 + 8, self.y0 + self.h - lh - 8
            out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="white" fill-opacity="0.92" stroke="#999"/>' % (lx, ly, lw, lh))
            for i, it in enumerate(self.legend_items):
                c, r = divmod(i, rows)
                yy = ly + 16 + r * 20
                xx = lx + 8 + c * 215
                if it[0] == "line":
                    _, col, dash, wd, lab = it
                    out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f" %s/>'
                               % (xx, yy - 4, xx + 30, yy - 4, col, wd, ('stroke-dasharray="%s"' % dash) if dash else ""))
                else:
                    _, col, shape, sz, lab = it
                    if shape == "o":
                        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="white" stroke="%s" stroke-width="1.6"/>' % (xx + 15, yy - 4, sz, col))
                    else:
                        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="white" stroke="%s" stroke-width="1.6"/>'
                                   % (xx + 15 - sz, yy - 4 - sz, 2 * sz, 2 * sz, col))
                out.append('<text x="%.1f" y="%.1f" font-size="12.5" font-family="%s">%s</text>' % (xx + 38, yy, FONT, lab))
        return "\n".join(out)


def svg_doc(width, height, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
            '<rect width="100%%" height="100%%" fill="white"/>%s</svg>' % (width, height, width, height, body))


def save(svg_text, path_png, width, height):
    """Write <name>.svg next to the PNG and rasterise it with headless Chromium (2x scale)."""
    svg_path = os.path.splitext(path_png)[0] + ".svg"
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_text)
    chrome = next((c for c in CHROME_CANDIDATES if os.path.exists(c)), None)
    if chrome is None:
        print("  [warn] no Chromium found; only SVG written:", svg_path)
        return svg_path
    html_path = os.path.splitext(path_png)[0] + "._render.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write('<html><body style="margin:0">%s</body></html>' % svg_text)
    subprocess.run([chrome, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--screenshot=" + os.path.abspath(path_png),
                    "--window-size=%d,%d" % (width, height), "file://" + os.path.abspath(html_path)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False, timeout=120)
    os.remove(html_path)
    print("  wrote", path_png)
    return path_png
