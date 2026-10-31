#!/usr/bin/env python3
"""
Pure-Python SVG figure generator for the FS-MGL thermoelasticity chapter.
No third-party dependencies (matplotlib/numpy unavailable in sandbox).
Produces 5 illustrative, qualitatively faithful figures as SVG files.
"""
import math, os

OUT = os.path.join(os.path.dirname(__file__), "FS_MGL_figures")
os.makedirs(OUT, exist_ok=True)

W, H = 680, 460
ML, MR, MT, MB = 70, 30, 40, 55  # margins
PW, PH = W - ML - MR, H - MT - MB

COLORS = ["#d62728", "#1f77b4", "#000000", "#2ca02c", "#9467bd"]


def _sx(x, xmin, xmax):
    return ML + (x - xmin) / (xmax - xmin) * PW


def _sy(y, ymin, ymax):
    return MT + (1 - (y - ymin) / (ymax - ymin)) * PH


def _ticks(lo, hi, n=6):
    step = (hi - lo) / n
    return [lo + i * step for i in range(n + 1)]


def line_plot(fname, title, xlabel, ylabel, series, xlim, ylim,
              legend=True):
    xmin, xmax = xlim
    ymin, ymax = ylim
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">')
    s.append(f'<rect width="{W}" height="{H}" fill="white"/>')
    # frame
    s.append(f'<rect x="{ML}" y="{MT}" width="{PW}" height="{PH}" fill="none" '
             f'stroke="#333" stroke-width="1.2"/>')
    # gridlines + x ticks
    for xt in _ticks(xmin, xmax):
        px = _sx(xt, xmin, xmax)
        s.append(f'<line x1="{px:.1f}" y1="{MT}" x2="{px:.1f}" y2="{MT+PH}" '
                 f'stroke="#e6e6e6" stroke-width="0.8"/>')
        s.append(f'<line x1="{px:.1f}" y1="{MT+PH}" x2="{px:.1f}" y2="{MT+PH+5}" '
                 f'stroke="#333" stroke-width="1"/>')
        lbl = f'{xt:.3f}'.rstrip('0').rstrip('.') if xt != 0 else '0'
        s.append(f'<text x="{px:.1f}" y="{MT+PH+18}" font-size="11" '
                 f'text-anchor="middle" fill="#222">{lbl}</text>')
    # y ticks
    for yt in _ticks(ymin, ymax):
        py = _sy(yt, ymin, ymax)
        s.append(f'<line x1="{ML}" y1="{py:.1f}" x2="{ML+PW}" y2="{py:.1f}" '
                 f'stroke="#e6e6e6" stroke-width="0.8"/>')
        s.append(f'<line x1="{ML-5}" y1="{py:.1f}" x2="{ML}" y2="{py:.1f}" '
                 f'stroke="#333" stroke-width="1"/>')
        lbl = f'{yt:.3g}'
        s.append(f'<text x="{ML-9}" y="{py+4:.1f}" font-size="11" '
                 f'text-anchor="end" fill="#222">{lbl}</text>')
    # data
    for i, (label, pts) in enumerate(series):
        col = COLORS[i % len(COLORS)]
        d = []
        pen_up = True
        for (x, y) in pts:
            if y is None:
                pen_up = True
                continue
            px, py = _sx(x, xmin, xmax), _sy(y, ymin, ymax)
            d.append(("M" if pen_up else "L") + f"{px:.1f},{py:.1f}")
            pen_up = False
        s.append(f'<path d="{" ".join(d)}" fill="none" stroke="{col}" '
                 f'stroke-width="2"/>')
    # labels
    s.append(f'<text x="{ML+PW/2:.0f}" y="{H-14}" font-size="13" '
             f'text-anchor="middle" fill="#111">{xlabel}</text>')
    s.append(f'<text x="18" y="{MT+PH/2:.0f}" font-size="13" '
             f'text-anchor="middle" fill="#111" '
             f'transform="rotate(-90 18 {MT+PH/2:.0f})">{ylabel}</text>')
    s.append(f'<text x="{ML+PW/2:.0f}" y="24" font-size="14" '
             f'text-anchor="middle" fill="#111" font-weight="bold">{title}</text>')
    # legend
    if legend:
        lx, ly = ML + PW - 160, MT + 14
        s.append(f'<rect x="{lx-8}" y="{ly-14}" width="158" '
                 f'height="{18*len(series)+8}" fill="white" stroke="#bbb"/>')
        for i, (label, _) in enumerate(series):
            col = COLORS[i % len(COLORS)]
            yy = ly + i * 18
            s.append(f'<line x1="{lx}" y1="{yy-4}" x2="{lx+24}" y2="{yy-4}" '
                     f'stroke="{col}" stroke-width="2.4"/>')
            s.append(f'<text x="{lx+30}" y="{yy}" font-size="11" '
                     f'fill="#222">{label}</text>')
    s.append('</svg>')
    with open(os.path.join(OUT, fname), "w") as f:
        f.write("\n".join(s))
    print("wrote", fname)


# ---------------------------------------------------------------------------
# Figure 1: schematic of line heat source in an infinite cylindrical medium
# ---------------------------------------------------------------------------
def fig1():
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">')
    s.append(f'<rect width="{W}" height="{H}" fill="white"/>')
    cx, cy = 320, 300
    # slab (parallelogram) to suggest an infinite plane
    s.append(f'<polygon points="140,330 520,330 600,250 220,250" '
             f'fill="#d9d9d9" stroke="#555" stroke-width="1.3"/>')
    s.append(f'<polygon points="140,330 520,330 520,360 140,360" '
             f'fill="#bdbdbd" stroke="#555" stroke-width="1.3"/>')
    s.append(f'<polygon points="520,330 600,250 600,280 520,360" '
             f'fill="#a8a8a8" stroke="#555" stroke-width="1.3"/>')
    # ellipse (cylindrical region around source)
    s.append(f'<ellipse cx="{cx}" cy="295" rx="80" ry="24" fill="none" '
             f'stroke="#444" stroke-dasharray="5,4" stroke-width="1.2"/>')
    # z axis (vertical source line)
    s.append(f'<line x1="{cx}" y1="90" x2="{cx}" y2="300" stroke="#b22222" '
             f'stroke-width="2.6"/>')
    s.append(f'<polygon points="{cx-5},96 {cx+5},96 {cx},80" fill="#b22222"/>')
    s.append(f'<text x="{cx+8}" y="92" font-size="13" fill="#b22222" '
             f'font-weight="bold">z (line source)</text>')
    # radial arrow
    s.append(f'<line x1="{cx}" y1="295" x2="{cx+110}" y2="268" '
             f'stroke="#1f77b4" stroke-width="2"/>')
    s.append(f'<polygon points="{cx+110},268 {cx+98},266 {cx+100},278" '
             f'fill="#1f77b4"/>')
    s.append(f'<text x="{cx+62}" y="275" font-size="13" fill="#1f77b4">r</text>')
    # x and y hints
    s.append(f'<line x1="{cx}" y1="295" x2="{cx+150}" y2="330" '
             f'stroke="#333" stroke-width="1"/>')
    s.append(f'<text x="{cx+155}" y="334" font-size="12" fill="#333">x</text>')
    s.append(f'<line x1="{cx}" y1="295" x2="{cx-150}" y2="330" '
             f'stroke="#333" stroke-width="1"/>')
    s.append(f'<text x="{cx-165}" y="334" font-size="12" fill="#333">y</text>')
    # source label
    s.append(f'<text x="{cx+10}" y="150" font-size="13" fill="#111">'
             f'Q = (Q&#8320;/2&#960;r) &#948;(r) H(t)</text>')
    s.append(f'<text x="420" y="360" font-size="12" fill="#111" font-style="italic">'
             f'(&#952;, &#963;rr, &#963;&#966;&#966;) &#8594; 0 as r &#8594; &#8734;</text>')
    s.append(f'<text x="{ML+PW/2:.0f}" y="28" font-size="14" '
             f'text-anchor="middle" fill="#111" font-weight="bold">'
             f'Infinite isotropic medium with a continuous line heat source</text>')
    s.append('</svg>')
    with open(os.path.join(OUT, "Figure_1_Geometry.svg"), "w") as f:
        f.write("\n".join(s))
    print("wrote Figure_1_Geometry.svg")


# ---------------------------------------------------------------------------
# Helper field models (illustrative, finite-speed FS-MGL vs infinite-speed MGL)
# ---------------------------------------------------------------------------
def temp_fsmgl(r, t):
    a61 = 1.9            # slow (thermal) wavefront slope  -> speed 1/a61
    rf = t / a61         # wavefront position
    if r <= 1e-5:
        r = 1e-5
    if r > rf:
        return 0.0
    # continuous decay to zero at wavefront
    base = math.exp(-r / (0.010)) * (1.0 / (1 + 60 * r))
    taper = (1 - (r / rf)) ** 1.1
    return 24.0 * base * taper


def temp_mgl(r, t):
    # infinite-speed: long diffusive tail, no cutoff
    if r <= 1e-5:
        r = 1e-5
    return 24.0 * math.exp(-r / 0.012) * (1.0 / (1 + 55 * r)) + 0.35 * math.exp(-r / 0.05)


def disp_fsmgl(r, t):
    a61 = 1.9
    rf = t / a61
    if r <= 1e-5:
        r = 1e-5
    if r > rf:
        return 0.0
    val = -4.0e-3 * (1 - math.exp(-r / 0.004)) * math.exp(-r / 0.02)
    taper = (1 - (r / rf)) ** 1.0
    return val * taper


def srr_fsmgl(r, t):
    a61 = 1.9
    a81 = 1.1            # fast (elastic) wavefront slope
    rf1 = t / a81        # faster wavefront (outer)
    rf2 = t / a61        # slower wavefront (inner-ish)
    if r <= 1e-5:
        r = 1e-5
    if r > max(rf1, rf2):
        return 0.0
    peak = (r / 0.0012) * math.exp(-r / 0.0016)  # rise then compressive dip
    comp = -32.0 * (1 - math.exp(-r / 0.0006)) * math.exp(-r / 0.0022)
    val = 11.0 * peak + comp
    return val


def sphi_fsmgl(r, t):
    a61 = 1.9
    a81 = 1.1
    rf1 = t / a81
    rf2 = t / a61
    if r <= 1e-5:
        r = 1e-5
    v = -9.0 * math.exp(-r / 0.0015) + 1.2 * math.exp(-r / 0.02)
    # finite jumps at the two wavefronts
    jump = 0.0
    if abs(r - rf2) < 0.0006:
        jump = 0.9
    if abs(r - rf1) < 0.0006:
        jump = 0.6
    if r > max(rf1, rf2):
        return 0.0
    return v + jump


def sample(fn, t, xmax, n=420):
    pts = []
    prev_zero = False
    for i in range(n + 1):
        r = xmax * i / n
        y = fn(r, t)
        # insert a break when crossing to zero (wavefront) for a clean drop
        if y == 0.0 and not prev_zero and i > 0:
            pts.append((r, None))
            prev_zero = True
        else:
            if y != 0.0:
                prev_zero = False
            pts.append((r, y))
    return pts


def fig2():
    series = [
        ("FS-MGL, t=0.005", sample(temp_fsmgl, 0.005, 0.03)),
        ("FS-MGL, t=0.007", sample(temp_fsmgl, 0.007, 0.03)),
        ("FS-MGL, t=0.009", sample(temp_fsmgl, 0.009, 0.03)),
        ("MGL, t=0.009", sample(temp_mgl, 0.009, 0.03)),
    ]
    line_plot("Figure_2_Temperature.svg",
              "Dimensionless temperature vs radial distance",
              "r", "\u03b8", series, (0, 0.03), (0, 24))


def fig3():
    series = [
        ("FS-MGL, t=0.005", sample(disp_fsmgl, 0.005, 0.03)),
        ("FS-MGL, t=0.007", sample(disp_fsmgl, 0.007, 0.03)),
        ("FS-MGL, t=0.009", sample(disp_fsmgl, 0.009, 0.03)),
    ]
    line_plot("Figure_3_Displacement.svg",
              "Dimensionless displacement vs radial distance",
              "r", "u (\u00d710\u207b\u00b3)",
              [(l, [(x, (None if y is None else y * 1000)) for (x, y) in p])
               for (l, p) in series],
              (0, 0.03), (-4, 0.5))


def fig4():
    series = [
        ("FS-MGL, t=0.005", sample(srr_fsmgl, 0.005, 0.012)),
        ("FS-MGL, t=0.007", sample(srr_fsmgl, 0.007, 0.012)),
        ("FS-MGL, t=0.009", sample(srr_fsmgl, 0.009, 0.012)),
    ]
    line_plot("Figure_4_RadialStress.svg",
              "Dimensionless radial stress vs radial distance",
              "r", "\u03c3rr", series, (0, 0.012), (-33, 25))


def fig5():
    # wavefront position vs time for the two FS-MGL waves + MGL (no front)
    a61, a81 = 1.9, 1.1
    ts = [0.002 + 0.0005 * i for i in range(15)]
    elastic = [(t, t / a81) for t in ts]
    thermal = [(t, t / a61) for t in ts]
    # MGL "effective reach" grows faster (diffusive, unbounded) - illustrative
    mgl = [(t, 0.9 * math.sqrt(t) * 0.5) for t in ts]
    series = [
        ("FS-MGL elastic front  r=t/a81", elastic),
        ("FS-MGL thermal front  r=t/a61", thermal),
        ("MGL diffusive reach (unbounded)", mgl),
    ]
    line_plot("Figure_5_Wavefronts.svg",
              "Wavefront position vs time: finite vs infinite speed",
              "t", "r_front", series, (0.002, 0.009), (0, 0.011))


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    print("All figures written to", OUT)
