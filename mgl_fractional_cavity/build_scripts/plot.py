"""Minimal SVG line-plot library + Chromium rasterization (no matplotlib available)."""
import math
import os
import subprocess

CHROME = ("/inner_container/opt/playwright/chromium_headless_shell-1232/"
          "chrome-headless-shell-linux64/chrome-headless-shell")
FONT = "Noto Sans, DejaVu Sans, Arial, sans-serif"
COLORS = ["#1f4e9c", "#c0392b", "#1e8449", "#7d3c98", "#d35400"]
DASHES = ["", "7,4", "2,3", "9,3,2,3", "4,2"]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rich(s):
    """Tiny markup: _{..} subscript, ^{..} superscript."""
    out = []
    i = 0
    while i < len(s):
        if s[i] in "_^" and i + 1 < len(s) and s[i + 1] == "{":
            j = s.index("}", i)
            shift = "-25%" if s[i] == "_" else "40%"
            out.append('<tspan baseline-shift="%s" font-size="75%%">%s</tspan>' % (shift, esc(s[i + 2:j])))
            i = j + 1
        else:
            j = i
            while j < len(s) and not (s[j] in "_^" and j + 1 < len(s) and s[j + 1] == "{"):
                j += 1
            out.append(esc(s[i:j]))
            i = j
    return "".join(out)


def nice_ticks(lo, hi, n=5):
    if hi == lo:
        hi = lo + 1
    span = hi - lo
    raw = span / n
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        step = m * mag
        if span / step <= n + 0.5:
            break
    start = math.floor(lo / step + 1e-9) * step
    ticks = []
    v = start
    while v <= hi + 1e-9 * step:
        if v >= lo - 1e-9 * step:
            ticks.append(round(v, 12))
        v += step
    return ticks, step


def fmt(v, step):
    if v == 0:
        return "0"
    dec = max(0, -int(math.floor(math.log10(step))) + (1 if step / 10 ** math.floor(math.log10(step)) == 2.5 else 0))
    return ("%." + str(dec) + "f") % v


class Panel:
    def __init__(self, x, y, w, h, xlabel, ylabel, title=None, yscale=1.0, ylabel_exp=None):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.xlabel, self.ylabel, self.title = xlabel, ylabel, title
        self.series = []
        self.yscale = yscale
        self.ylabel_exp = ylabel_exp
        self.vlines = []
        self.annos = []

    def line(self, xs, ys, label, k):
        self.series.append((xs, [y * self.yscale for y in ys], label, k))

    def vline(self, x, label):
        self.vlines.append((x, label))

    def svg(self, xlim=None, ylim=None, legend_pos="ur"):
        xs_all = [v for s in self.series for v in s[0]]
        ys_all = [v for s in self.series for v in s[1]]
        x0, x1 = xlim or (min(xs_all), max(xs_all))
        if ylim:
            y0, y1 = ylim
        else:
            y0, y1 = min(ys_all), max(ys_all)
            pad = 0.06 * (y1 - y0 or 1)
            y0 -= pad
            y1 += pad
        xt, xs_ = nice_ticks(x0, x1, 8)
        yt, ys_ = nice_ticks(y0, y1, 6)
        y0 = min(y0, yt[0])
        y1 = max(y1, yt[-1])
        X = lambda v: self.x + (v - x0) / (x1 - x0) * self.w
        Y = lambda v: self.y + self.h - (v - y0) / (y1 - y0) * self.h
        o = []
        o.append('<rect x="%g" y="%g" width="%g" height="%g" fill="white" stroke="#222" stroke-width="1.2"/>' % (self.x, self.y, self.w, self.h))
        for t in xt:
            o.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#e3e3e3"/>' % (X(t), self.y, X(t), self.y + self.h))
            o.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#222"/>' % (X(t), self.y + self.h, X(t), self.y + self.h - 5))
            o.append('<text x="%g" y="%g" font-size="13" text-anchor="middle">%s</text>' % (X(t), self.y + self.h + 18, fmt(t, xs_)))
        for t in yt:
            o.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#e3e3e3"/>' % (self.x, Y(t), self.x + self.w, Y(t)))
            o.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#222"/>' % (self.x, Y(t), self.x + 5, Y(t)))
            o.append('<text x="%g" y="%g" font-size="13" text-anchor="end">%s</text>' % (self.x - 6, Y(t) + 4, fmt(t, ys_)))
        if y0 < 0 < y1:
            o.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#888" stroke-width="0.8"/>' % (self.x, Y(0), self.x + self.w, Y(0)))
        o.append('<clipPath id="c%d"><rect x="%g" y="%g" width="%g" height="%g"/></clipPath>' % (id(self) % 100000, self.x, self.y, self.w, self.h))
        for xv, lab in self.vlines:
            o.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#999" stroke-dasharray="3,3"/>' % (X(xv), self.y, X(xv), self.y + self.h))
            o.append('<text x="%g" y="%g" font-size="11" fill="#555">%s</text>' % (X(xv) + 3, self.y + 14, rich(lab)))
        for xs, ys, lab, k in self.series:
            pts = " ".join("%.2f,%.2f" % (X(a), Y(b)) for a, b in zip(xs, ys))
            o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="%s" clip-path="url(#c%d)"/>' % (pts, COLORS[k], DASHES[k], id(self) % 100000))
        # legend
        lw = 150
        lh = 20 * len(self.series) + 8
        lx = self.x + self.w - lw - 10 if legend_pos[1] == "r" else self.x + 10
        ly = self.y + 10 if legend_pos[0] == "u" else self.y + self.h - lh - 10
        o.append('<rect x="%g" y="%g" width="%g" height="%g" fill="white" fill-opacity="0.9" stroke="#999"/>' % (lx, ly, lw, lh))
        for j, (_, _, lab, k) in enumerate(self.series):
            yy = ly + 16 + 20 * j
            o.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="2" stroke-dasharray="%s"/>' % (lx + 8, yy - 4, lx + 40, yy - 4, COLORS[k], DASHES[k]))
            o.append('<text x="%g" y="%g" font-size="13">%s</text>' % (lx + 46, yy, rich(lab)))
        o.append('<text x="%g" y="%g" font-size="15" text-anchor="middle">%s</text>' % (self.x + self.w / 2, self.y + self.h + 40, rich(self.xlabel)))
        yl = self.ylabel + (" (×10^{%d})" % self.ylabel_exp if self.ylabel_exp is not None else "")
        cx, cy = self.x - 58, self.y + self.h / 2
        o.append('<text x="%g" y="%g" font-size="15" text-anchor="middle" transform="rotate(-90 %g %g)">%s</text>' % (cx, cy, cx, cy, rich(yl)))
        if self.title:
            o.append('<text x="%g" y="%g" font-size="15" font-weight="bold">%s</text>' % (self.x, self.y - 8, rich(self.title)))
        return "\n".join(o)


def write(name, width, height, body, outdir):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="%s">'
           '<rect width="100%%" height="100%%" fill="white"/>%s</svg>') % (width, height, FONT, body)
    path = os.path.join(outdir, name + ".svg")
    with open(path, "w") as fh:
        fh.write(svg)
    png = os.path.join(outdir, name + ".png")
    subprocess.run([CHROME, "--no-sandbox", "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--screenshot=" + png, "--window-size=%d,%d" % (width, height),
                    "file://" + path], check=True, capture_output=True)
    return png
