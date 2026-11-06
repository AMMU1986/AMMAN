"""Figures 1-13 (SVG -> PNG via headless Chromium) from results.json.
Figures 1 and 2 are schematics (geometry, flow chart); Figures 3-13 are computed."""
import json
import math
import os

import plot
from plot import Panel, rich
import model as M

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
R = json.load(open(os.path.join(HERE, "results.json")))
RS, TS, XS = R["rs"], R["ts"], R["mov_xs"]
EPS = R["eps"]
C_LS = 1 / math.sqrt((1 + EPS) * 0.02)
C_D = math.sqrt(2 * 0.012 / (1 + EPS)) / 0.02
W = 900
PX, PW = 105, 760
PH, GAP = 330, 95
XLR = "Radial distance r"

DEFS = ('<defs><marker id="ar" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
        '<path d="M0,0 L10,4 L0,8 z" fill="#222"/></marker></defs>')


def col(key, j):
    return [row[j] for row in R[key]]


def stacked(name, panels, legend=("ur", "ur")):
    """panels: list of dict(series=[(x,y,label)], xlabel, ylabel, scale, exp, title, vlines, xlim, ylim)"""
    body = []
    for j, pd in enumerate(panels):
        p = Panel(PX, 40 + j * (PH + GAP), PW, PH, pd["xlabel"], pd["ylabel"], pd.get("title"),
                  yscale=pd.get("scale", 1.0), ylabel_exp=pd.get("exp"))
        for k, (xs, ys, lab) in enumerate(pd["series"]):
            p.line(xs, ys, lab, k)
        for x, lab in pd.get("vlines", []):
            p.vline(x, lab)
        body.append(p.svg(xlim=pd.get("xlim"), ylim=pd.get("ylim"), legend_pos=pd.get("legend", legend[j])))
    H = 40 + len(panels) * (PH + GAP) - 30
    return plot.write(name, W, H, "\n".join(body), OUT)


# ---------------------------------------------------------------- Figure 1 (schematic)
def fig1():
    o = [DEFS]
    # (a) pulsed axisymmetric source
    cx, cy = 230, 270
    o.append('<text x="%d" y="30" font-size="15" font-weight="bold" text-anchor="middle">(a) Pulsed line source (axisymmetric)</text>' % cx)
    o.append('<rect x="20" y="50" width="420" height="420" fill="#eef2f7" stroke="#555"/>')
    o.append('<circle cx="%d" cy="%d" r="170" fill="none" stroke="#c0392b" stroke-width="1.8" stroke-dasharray="7,5"/>' % (cx, cy))
    o.append('<circle cx="%d" cy="%d" r="110" fill="none" stroke="#c0392b" stroke-width="1.2" stroke-dasharray="3,4"/>' % (cx, cy))
    o.append('<circle cx="%d" cy="%d" r="7" fill="#1f4e9c"/>' % (cx, cy))
    o.append('<text x="%d" y="%d" font-size="13">line source, Q(r,t)=Q_{0}δ(r)f(t)/(2πr)</text>' % (cx - 200, cy + 150))
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#222" stroke-width="1.5" marker-end="url(#ar)"/>' % (cx, cy, cx + 200, cy))
    o.append('<text x="%d" y="%d" font-size="15" font-style="italic">r</text>' % (cx + 195, cy - 8))
    o.append('<text x="%d" y="%d" font-size="13" fill="#c0392b" text-anchor="middle">thermal wavefront r = c_{w}t</text>' % (cx, cy - 178))
    o.append('<text x="%d" y="%d" font-size="13" text-anchor="middle">diffusive/strain-rate tail (infinite speed, exponentially small)</text>' % (cx, 455))
    o.append('<text x="%d" y="%d" font-size="13" text-anchor="middle">z axis out of plane: plane strain, u = u(r,t)</text>' % (cx, 70))
    # (b) moving source
    ox, oy = 700, 270
    o.append('<text x="%d" y="30" font-size="15" font-weight="bold" text-anchor="middle">(b) Source translating at speed V</text>' % ox)
    o.append('<rect x="480" y="50" width="420" height="420" fill="#eef2f7" stroke="#555"/>')
    sx = 780
    o.append('<circle cx="%d" cy="%d" r="90" fill="none" stroke="#c0392b" stroke-width="1.8" stroke-dasharray="7,5"/>' % (ox - 50, oy))
    o.append('<circle cx="%d" cy="%d" r="6" fill="#1f4e9c" fill-opacity="0.4"/>' % (ox - 50, oy))
    o.append('<circle cx="%d" cy="%d" r="7" fill="#1f4e9c"/>' % (sx, oy))
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#1f4e9c" stroke-width="2" marker-end="url(#ar)"/>' % (ox - 44, oy, sx - 10, oy))
    o.append('<text x="%d" y="%d" font-size="13">source at x = Vt</text>' % (sx - 40, oy + 26))
    o.append('<text x="%d" y="%d" font-size="13" text-anchor="middle">x = 0 at t = 0</text>' % (ox - 50, oy + 110))
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#c0392b" stroke-width="1.2" stroke-dasharray="4,3"/>' % (sx, oy, sx - 190, oy - 120))
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#c0392b" stroke-width="1.2" stroke-dasharray="4,3"/>' % (sx, oy, sx - 190, oy + 120))
    o.append('<text x="%d" y="%d" font-size="13" fill="#c0392b">Mach cone, sin β = c_{w}/V (V > c_{w})</text>' % (500, 95))
    o.append('<line x1="500" y1="445" x2="600" y2="445" stroke="#222" stroke-width="1.5" marker-end="url(#ar)"/>')
    o.append('<text x="606" y="450" font-size="14" font-style="italic">x</text>')
    o.append('<line x1="500" y1="445" x2="500" y2="355" stroke="#222" stroke-width="1.5" marker-end="url(#ar)"/>')
    o.append('<text x="508" y="362" font-size="14" font-style="italic">y</text>')
    # rich() for subscripts
    body = "\n".join(o)
    import re
    body = re.sub(r'(<text[^>]*>)([^<]*)(</text>)', lambda m: m.group(1) + rich(m.group(2)) + m.group(3), body)
    return plot.write("Figure_1", 920, 490, body, OUT)


# ---------------------------------------------------------------- Figure 2 (flow chart)
def fig2():
    boxes = [
        ("Nondimensional MGL + LS/DPL/TPL equations", 30),
        ("Laplace transform in t; potential u = ∂φ/∂r (or ∇φ)", 105),
        ("Fourth-order equation: (∇²−m_{1}²)(∇²−m_{2}²)φ = −δ_{1}Q/Ψ", 180),
        ("Pulsed source: K_{0}(m_{j}r)   |   Moving source: Fourier in x, closed form in y", 255),
        ("Fields θ, u, σ in the s-domain; large-s asymptotics (waves, speeds)", 330),
        ("Durbin inversion + Wynn-ε; ξ-quadrature for the moving source", 405),
        ("Validation: FD solver, limits, truncation, decay, heat content", 480),
    ]
    o = [DEFS]
    for txt, y in boxes:
        o.append('<rect x="70" y="%d" width="760" height="52" rx="8" fill="#eef2f7" stroke="#1f4e9c" stroke-width="1.6"/>' % y)
        o.append('<text x="450" y="%d" font-size="15" text-anchor="middle">%s</text>' % (y + 31, rich(txt)))
        if y < 480:
            o.append('<line x1="450" y1="%d" x2="450" y2="%d" stroke="#222" stroke-width="1.6" marker-end="url(#ar)"/>' % (y + 52, y + 75))
    return plot.write("Figure_2", 900, 550, "\n".join(o), OUT)


# ---------------------------------------------------------------- Figure 3
def fig3():
    profs = [(("step",), "step"), (("rect", 0.04), "rect, t_{p}=0.04"), (("exp", 0.05), "exp, t_{d}=0.05"),
             (("gamma", 0.03), "gamma, t_{m}=0.03"), (("sin2", 0.08), "sin², P=0.08")]
    ts = [0.002 * i for i in range(0, 101)]
    ser = [(ts, [M.ftime(p, t) for t in ts], lab) for p, lab in profs]
    ws = [5 + 1.0 * i for i in range(0, 196)]
    ser2 = []
    for p, lab in profs:
        ys = []
        for w in ws:
            v = abs(M.Fbar(p, 1j * w))
            ys.append(min(v, 0.3))
        ser2.append((ws, ys, lab))
    return stacked("Figure_3", [
        dict(series=ser, xlabel="Time t", ylabel="Source profile f(t)", title="(a) Temporal profiles", ylim=(0, 1.1)),
        dict(series=ser2, xlabel="Angular frequency ω", ylabel="|F(iω)|", title="(b) Spectral content", ylim=(0, 0.3))],
        legend=("ur", "ur"))


# ---------------------------------------------------------------- Figure 4
def fig4():
    A = R["asym"]["_curves"]
    xs = [math.log10(s) for s in A["s"]]
    names = [("MGL-LS", "MGL-LS"), ("MGL-DPL1", "MGL-DPL1"), ("MGL-DPL2", "MGL-DPL2"), ("MGL-TPL", "MGL-TPL"), ("GL", "GL")]
    s1 = [(xs, A["curves"][k]["c1"], lab) for k, lab in names]
    s2 = [(xs, A["curves"][k]["c2"], lab) for k, lab in names]
    return stacked("Figure_4", [
        dict(series=s1, xlabel="log_{10} s", ylabel="|m_{1}|/s", title="(a) Fast root: wave-type if |m|/s tends to 1/c", ylim=(0, 0.6), legend="ur"),
        dict(series=s2, xlabel="log_{10} s", ylabel="|m_{2}|/√s", title="(b) Slow root: diffusive-type if |m|/√s tends to a constant", ylim=(0, 10), legend="ur")],
        legend=("ur", "ur"))


# ---------------------------------------------------------------- Figure 5
def fig5():
    ks = [("prof_DPL2_t0.03", 0.03), ("prof_DPL2_t0.06", 0.06), ("prof_DPL2_t0.09", 0.09)]
    th = [(RS, col(k, 0), "t = %g" % t) for k, t in ks]
    sp = [(RS, col(k, 3), "t = %g" % t) for k, t in ks]
    vl = [(C_D * t, "") for _, t in ks]
    return stacked("Figure_5", [
        dict(series=th, xlabel=XLR, ylabel="Temperature θ", title="(a) Temperature, MGL-DPL (step source)", vlines=vl, xlim=(0.05, 0.8)),
        dict(series=sp, xlabel=XLR, ylabel="Hoop stress σ_{φφ}", scale=1e3, exp=-3, title="(b) Hoop stress", vlines=vl, xlim=(0.05, 0.8), legend="lr")],
        legend=("ur", "lr"))


# ---------------------------------------------------------------- Figure 6
def fig6():
    ks = [("prof_t1_0", "τ_{1} = 0"), ("prof_t1_0.02", "τ_{1} = 0.02"), ("prof_t1_0.05", "τ_{1} = 0.05"), ("prof_t1_0.1", "τ_{1} = 0.1")]
    u = [(RS, col(k, 1), lab) for k, lab in ks]
    sp = [(RS, col(k, 3), lab) for k, lab in ks]
    vl = [(C_D * 0.06, "c_{w}t")]
    return stacked("Figure_6", [
        dict(series=u, xlabel=XLR, ylabel="Displacement u", scale=1e3, exp=-3, title="(a) Displacement (t = 0.06)", vlines=vl, xlim=(0.05, 0.8)),
        dict(series=sp, xlabel=XLR, ylabel="Hoop stress σ_{φφ}", scale=1e3, exp=-3, title="(b) Hoop stress (t = 0.06)", vlines=vl, xlim=(0.05, 0.8), legend="lr")],
        legend=("ur", "lr"))


# ---------------------------------------------------------------- Figure 7
def fig7():
    ks = [("Fourier", "Fourier"), ("GL", "GL"), ("MGL-LS", "MGL-LS"), ("MGL-DPL1", "MGL-DPL1"), ("MGL-DPL2", "MGL-DPL2")]
    th = [(RS, col("prof_model_" + k, 0), lab) for k, lab in ks]
    sp = [(RS, col("prof_model_" + k, 3), lab) for k, lab in ks]
    vl = [(C_LS * 0.06, "c_{LS}t"), (C_D * 0.06, "c_{DPL}t")]
    return stacked("Figure_7", [
        dict(series=th, xlabel=XLR, ylabel="Temperature θ", title="(a) Temperature (t = 0.06)", vlines=vl, xlim=(0.05, 0.8)),
        dict(series=sp, xlabel=XLR, ylabel="Hoop stress σ_{φφ}", scale=1e3, exp=-3, title="(b) Hoop stress (t = 0.06)", vlines=vl, xlim=(0.05, 0.8), legend="lr")],
        legend=("ur", "lr"))


# ---------------------------------------------------------------- Figure 8
def fig8():
    ks = [("step", "step"), ("rect", "rect t_{p}=0.04"), ("exp", "exp t_{d}=0.05"), ("gamma", "gamma t_{m}=0.03"), ("sin2", "sin² P=0.08")]
    th = [(TS, col("hist_DPL2_" + k, 0), lab) for k, lab in ks]
    sp = [(TS, col("hist_DPL2_" + k, 3), lab) for k, lab in ks]
    return stacked("Figure_8", [
        dict(series=th, xlabel="Time t", ylabel="Temperature θ", title="(a) θ at r = 0.3", vlines=[(0.3 / C_D, "arrival")]),
        dict(series=sp, xlabel="Time t", ylabel="Hoop stress σ_{φφ}", scale=1e3, exp=-3, title="(b) σ_{φφ} at r = 0.3", vlines=[(0.3 / C_D, "arrival")], legend="lr")],
        legend=("ur", "lr"))


# ---------------------------------------------------------------- Figure 9
def fig9():
    a = [("prof_tT_%s" % k, "τ_{T} = %s" % k) for k in ("0.0105", "0.012", "0.02", "0.04")]
    b = [("prof_tq_%s" % k, "τ_{q} = %s" % k) for k in ("0.01", "0.02", "0.03", "0.04")]
    return stacked("Figure_9", [
        dict(series=[(RS, col(k, 0), lab) for k, lab in a], xlabel=XLR, ylabel="Temperature θ", title="(a) Effect of τ_{T} (τ_{q} = 0.02, t = 0.06)", xlim=(0.05, 0.8)),
        dict(series=[(RS, col(k, 0), lab) for k, lab in b], xlabel=XLR, ylabel="Temperature θ", title="(b) Effect of τ_{q} (τ_{T} = 0.6τ_{q}, t = 0.06)", xlim=(0.05, 0.8))])


# ---------------------------------------------------------------- Figure 10
def fig10():
    a = [("prof_tv_%s" % k, "τ_{v} = %s" % k) for k in ("0", "0.1", "0.3", "0.5")]
    b = [("prof_K_%s" % k, "K* = %s" % k) for k in ("0", "0.1", "0.5", "2")]
    return stacked("Figure_10", [
        dict(series=[(RS, col(k, 0), lab) for k, lab in a], xlabel=XLR, ylabel="Temperature θ", title="(a) Effect of τ_{v} (K* = 0.5, t = 0.15)", xlim=(0.05, 0.8)),
        dict(series=[(RS, col(k, 0), lab) for k, lab in b], xlabel=XLR, ylabel="Temperature θ", title="(b) Effect of K* (τ_{v} = 0.03, t = 0.15)", xlim=(0.05, 0.8))])


# ---------------------------------------------------------------- Figure 11
def fig11():
    a = [("hist_rect_%s" % k, "t_{p} = %s" % k) for k in ("0.01", "0.03", "0.06", "0.12")]
    b = [("hist_sin2_%s" % k, "P = %s" % k) for k in ("0.04", "0.08", "0.16")]
    return stacked("Figure_11", [
        dict(series=[(TS, col(k, 0), lab) for k, lab in a], xlabel="Time t", ylabel="Temperature θ", title="(a) Rectangular pulses, θ at r = 0.3"),
        dict(series=[(TS, col(k, 3), lab) for k, lab in b], xlabel="Time t", ylabel="Hoop stress σ_{φφ}", scale=1e3, exp=-3, title="(b) Sinusoidal pulse trains, σ_{φφ} at r = 0.3", legend="lr")],
        legend=("ur", "lr"))


# ---------------------------------------------------------------- Figure 12
def fig12():
    Vs = [("0", "V = 0"), ("3", "V = 3"), ("7.7", "V = 7.7"), ("12", "V = 12")]
    th = [(XS, col("mov_V" + k, 0), lab) for k, lab in Vs]
    sm = [(XS, [0.5 * (r[3] + r[4]) for r in R["mov_V" + k]], lab) for k, lab in Vs]
    return stacked("Figure_12", [
        dict(series=th, xlabel="x", ylabel="Temperature θ", title="(a) θ(x, y = 0.2, t = 0.1)"),
        dict(series=sm, xlabel="x", ylabel="Mean in-plane stress (σ_{xx}+σ_{yy})/2", scale=1e3, exp=-3, title="(b) Mean in-plane stress", legend="lr")],
        legend=("ur", "lr"))


# ---------------------------------------------------------------- Figure 13 (validation 2x2)
def fig13():
    fd = R["fd"]["rect"]
    r = fd["r"]
    a = [(r, [x[0] for x in fd["lt"]], "Laplace (disc)"), (r, [x[0] for x in fd["fd"]], "Finite difference")]
    b = [(r, [x[3] for x in fd["lt"]], "Laplace (disc)"), (r, [x[3] for x in fd["fd"]], "Finite difference")]
    tr = R["checks"]["truncation"]
    Ns = [math.log2(n) for n in (500, 1000, 2000, 4000, 8000)]

    def lg(v):
        return math.log10(max(v, 1e-16))
    c = [(Ns, [lg(row[0]) for row in tr[k]], k) for k in ("MGL-LS", "MGL-DPL2", "MGL-DPL1")]
    hh = R["checks"]["v0_h"]
    hs = ["1.0", "0.5", "0.25", "0.125"]
    d = [([math.log2(float(h)) for h in hs], [lg(hh[h]) for h in hs], "V = 0 against K_{0}")]
    pw, ph = 480, 300
    pos = [(105, 40), (665, 40), (105, 450), (665, 450)]
    specs = [
        ("(a) θ, rect pulse t_{p}=0.03, t=0.05", "Radial distance r", "Temperature θ", a, 1.0, None, "ur"),
        ("(b) σ_{φφ}, same case", "Radial distance r", "Hoop stress σ_{φφ}", b, 1e3, -3, "lr"),
        ("(c) Durbin truncation test (θ, t=0.06)", "log_{2} N", "log_{10}(rel. diff N vs N/2)", c, 1.0, None, "ur"),
        ("(d) Moving-source code at V=0", "log_{2} h", "log_{10}(rel. error)", d, 1.0, None, "ur"),
    ]
    body = []
    for (x0, y0), (title, xl, yl, ser, sc, ex, lp) in zip(pos, specs):
        p = Panel(x0, y0, pw, ph, xl, yl, title, yscale=sc, ylabel_exp=ex)
        for k, (xs, ys, lab) in enumerate(ser):
            p.line(xs, ys, lab, k)
        body.append(p.svg(legend_pos=lp))
    svg = "\n".join(body)
    svg = plot.scale_fonts(svg, 1.0)
    return plot.write("Figure_13", 1200, 850, svg, OUT)


if __name__ == "__main__":
    for f in (fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, fig12, fig13):
        print(f.__name__, f())
