"""Six figures (SVG -> PNG via headless Chromium).  Figure 1 is a schematic/flow chart (no data); Figures 2-6 are
computed from the finite element, Laplace-reference and optimisation results (JSON files of the compute stages)."""
import math, os
import plot
from plot import Panel, rich
from nums import V, OM, OP, OF, OS, C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
W, PX, PW, PH, GAP = 900, 105, 760, 280, 95
DEFS = ('<defs><marker id="ar" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
        '<path d="M0,0 L10,4 L0,8 z" fill="#222"/></marker></defs>')
TC = 310.0 - 273.15


def stacked(name, panels, extra_h=0):
    body = []
    for j, pd in enumerate(panels):
        y0 = 40 + j * (PH + GAP)
        if pd.get("custom"):
            body.append(pd["custom"](PX, y0, PW, PH))
            continue
        p = Panel(PX, y0, PW, PH, pd["xlabel"], pd["ylabel"], pd.get("title"))
        for k, (xs, ys, lab) in enumerate(pd["series"]):
            p.line(xs, ys, lab, pd.get("ks", list(range(len(pd["series"]))))[k])
        for x, lab in pd.get("vlines", []):
            p.vline(x, lab)
        body.append(p.svg(xlim=pd.get("xlim"), ylim=pd.get("ylim"), legend_pos=pd.get("legend", "ur")))
    H = 40 + len(panels) * (PH + GAP) - 30 + extra_h
    return plot.write(name, W, H, "\n".join(body), OUT)


def fig1():
    o = [DEFS]
    t = lambda x, y, s, **kw: o.append('<text x="%g" y="%g" font-size="%d" %s>%s</text>' % (
        x, y, kw.get("fs", 14), kw.get("extra", ""), rich(s)))
    t(450, 22, "(a) Layered slab, 1-D: tumour 0 < x < h, normal tissue h < x < L", fs=15, extra='font-weight="bold" text-anchor="middle"')
    o.append('<rect x="80" y="70" width="140" height="110" fill="#e8c9c9" stroke="#444" stroke-width="1.5"/>')
    o.append('<rect x="220" y="70" width="600" height="110" fill="#d6e4f0" stroke="#444" stroke-width="1.5"/>')
    t(150, 118, "tumour (1)", extra='text-anchor="middle"')
    t(150, 140, "kill: Ω ≥ Ω_{c}", fs=12, extra='text-anchor="middle"')
    t(520, 118, "normal tissue (2)", extra='text-anchor="middle"')
    t(520, 140, "collateral damage J (to be minimised)", fs=12, extra='text-anchor="middle"')
    o.append('<line x1="220" y1="62" x2="220" y2="190" stroke="#222" stroke-dasharray="4,3"/>')
    t(220, 208, "x = h = 4 mm", extra='text-anchor="middle"')
    t(80, 208, "x = 0", extra='text-anchor="middle"')
    t(820, 208, "x = L = 20 mm", extra='text-anchor="end"')
    for xx in (100, 130, 160):
        o.append('<line x1="%d" y1="44" x2="%d" y2="66" stroke="#c0392b" stroke-width="2.5" marker-end="url(#ar)"/>' % (xx, xx))
    t(180, 52, "pulse train I_{0}f(t)", extra='fill="#c0392b"')
    t(84, 232, "σ_{xx}=0, adiabatic at x = 0;  u = 0, θ = 0 at x = L;  continuity of u, σ, θ and flux at x = h", fs=13, extra='')
    # pulse train sketch
    t(450, 268, "(b) Decision variables: pulse train f(t) = Σ [H(t − mP) − H(t − mP − t_{p})], m = 0 … N_{p}−1", fs=15, extra='font-weight="bold" text-anchor="middle"')
    o.append('<line x1="80" y1="340" x2="820" y2="340" stroke="#222" stroke-width="1.5"/>')
    pts = []
    for m in range(4):
        x0 = 100 + m * 150
        o.append('<polyline points="%d,340 %d,340 %d,296 %d,296 %d,340" fill="none" stroke="#1f4e9c" stroke-width="2.5"/>' % (x0 - 1, x0, x0, x0 + 70, x0 + 70))
    o.append('<line x1="100" y1="360" x2="170" y2="360" stroke="#222" marker-end="url(#ar)"/>')
    t(135, 378, "t_{p}", extra='text-anchor="middle"')
    o.append('<line x1="100" y1="388" x2="250" y2="388" stroke="#222" marker-end="url(#ar)"/>')
    t(175, 406, "period P", extra='text-anchor="middle"')
    t(60, 300, "I_{0}", extra='text-anchor="end"')
    t(700, 322, "N_{p} pulses, t_{treat} = N_{p}P ≤ 30 s", extra='')
    # flow chart
    t(450, 436, "(c) Design workflow", fs=15, extra='font-weight="bold" text-anchor="middle"')
    boxes = [("design d", "I_{0}, t_{p}, P, N_{p}"), ("heat model", "θ(x,t): FE + BDF2"), ("damage", "Ω = ∫ A e^{−E_{a}/RT} dt"),
             ("stress", "σ_{∥} = −s(θ + τ_{1}θ_{t})"), ("Nelder–Mead", "min J + penalties")]
    for i, (a, b) in enumerate(boxes):
        x = 40 + i * 168
        o.append('<rect x="%g" y="456" width="140" height="64" rx="6" fill="#f3f3f3" stroke="#444"/>' % x)
        t(x + 70, 482, a, extra='text-anchor="middle" font-weight="bold"')
        t(x + 70, 504, b, fs=11, extra='text-anchor="middle"')
        if i < 4:
            o.append('<line x1="%g" y1="488" x2="%g" y2="488" stroke="#222" marker-end="url(#ar)"/>' % (x + 140, x + 168))
    o.append('<path d="M 784 520 L 784 544 L 110 544 L 110 522" fill="none" stroke="#222" marker-end="url(#ar)"/>')
    t(450, 562, "update d until constraints (kill, T_{max}, |σ|, t_{treat}) hold and J stops decreasing", fs=12, extra='text-anchor="middle"')
    t(450, 596, "Schematic only: contains no computed data.", fs=13, extra='text-anchor="middle" font-style="italic"')
    return plot.write("Figure_1", W, 616, "\n".join(o), OUT)


def fig2():
    cur = V["curves"]
    P = []
    s = []
    names = ["x = 0", "x = h", "x = 8 mm"]
    for j in (0, 1, 2):
        s.append((cur["MGL"]["t"], [r[j] for r in cur["MGL"]["fe"]], "FE, " + names[j]))
        s.append((cur["MGL"]["t"], [r[j] for r in cur["MGL"]["lap"]], "Laplace, " + names[j]))
    P.append(dict(xlabel="t (s)", ylabel="θ (K)", title="(a) MGL, linear problem, 2 s pulse: FE vs Laplace inversion", series=s,
                  ks=[0, 0, 1, 1, 2, 2], legend="ur"))
    s = []
    for k, nm in enumerate(("Pennes", "CV", "MGL")):
        s.append((cur[nm]["t"], [r[1] for r in cur[nm]["fe"]], "FE, " + nm))
        s.append((cur[nm]["t"], [r[1] for r in cur[nm]["lap"]], "Laplace, " + nm))
    P.append(dict(xlabel="t (s)", ylabel="θ(h, t) (K)", title="(b) temperature at the interface for three heat models", series=s,
                  ks=[0, 0, 1, 1, 2, 2], legend="ur"))
    v = V["valid"]["MGL"]
    s = []
    for ti, tt in ((1, 3), (2, 6)):
        s.append((v["x"], [a / 1e3 for a in v["sg_fe"][ti]], "FE, t = %g s" % tt))
        s.append((v["x"], [a / 1e3 for a in v["sg_lap"][ti]], "Laplace, t = %g s" % tt))
    P.append(dict(xlabel="x (mm)", ylabel="σ_{∥} (kPa)", title="(c) in-plane stress, MGL (τ_{1} = 1 s)", series=s, ks=[0, 0, 1, 1], legend="lr",
                  vlines=[(4, "h")]))
    return stacked("Figure_2", P)


def fig3():
    lg = math.log10
    cl = V["conv_lap"]
    s = []
    for nm, k in (("Pennes", 0), ("MGL", 1)):
        s.append(([lg(a) for a in cl[nm]["dt"]], [lg(a) for a in cl[nm]["edt"]], nm + " vs Laplace"))
    pr = V["prod"]
    s.append(([lg(r[0]) for r in pr["dt"]], [lg(max(r[1][1], 1e-12)) for r in pr["dt"]], "Ω_{T,min}, pulse train"))
    P = [dict(xlabel="log_{10} Δt", ylabel="log_{10} (relative error)", title="(a) time-step convergence (Δx = 0.125 mm)", series=s, ks=[0, 1, 2], legend="lr")]
    s = []
    for nm in ("Pennes", "MGL"):
        s.append(([lg(a * 1e3) for a in cl[nm]["dx"]], [lg(a) for a in cl[nm]["edx"]], nm + " vs Laplace"))
    s.append(([lg(r[0] * 1e3) for r in pr["dx"]], [lg(max(r[1][1], 1e-12)) for r in pr["dx"]], "Ω_{T,min}, pulse train"))
    s.append(([lg(r[0] * 1e3) for r in pr["dx"]], [lg(max(r[1][3], 1e-12)) for r in pr["dx"]], "J_{F}, pulse train"))
    P.append(dict(xlabel="log_{10} Δx (mm)", ylabel="log_{10} (relative error)", title="(b) mesh convergence (Δt = 0.02 s, or 0.05 s for the pulse train)", series=s, ks=[0, 1, 2, 3], legend="lr"))
    rows = V["quad"]["ramp"]["rows"]
    s = []
    for j, lab in ((0, "Simpson, 2 panels"), (1, "Simpson, 4 panels"), (2, "Simpson, 8 panels"), (3, "trapezoid on rate")):
        s.append(([lg(r[0]) for r in rows], [lg(r[1][j]) for r in rows], lab))
    P.append(dict(xlabel="log_{10} Δt (s)", ylabel="log_{10} (relative error of Ω)", title="(c) Arrhenius quadrature on a 0.5 K/s ramp", series=s, ks=[0, 1, 2, 3], legend="ur"))
    return stacked("Figure_3", P)


def fig4():
    F = C["fields"]["opt"]
    h = F["hist"]
    xm = [0, 2, 4, 6, 10]
    s = [(h["t"], [v + TC for v in h["th"][i]], "x = %g mm" % xm[i]) for i in range(5)]
    P = [dict(xlabel="t (s)", ylabel="T (°C)", title="(a) temperature histories of the optimal MGL design (S1)", series=s, ks=[0, 1, 2, 3, 4], legend="ur")]
    prof = F["profiles"]
    xs = F["x"]; n1 = F["n1"]
    s = []
    for tt in ("10.0", "40.0", "120.0"):
        om = prof[tt]["OmT"] + prof[tt]["OmN"][1:]
        s.append(([x * 1e3 for x in xs[: len(om)]], [1 - math.exp(-min(o_, 50)) for o_ in om], "t = %g s" % float(tt)))
    s.append(([0, 12], [0.99, 0.99], "threshold 0.99"))
    P.append(dict(xlabel="x (mm)", ylabel="1 − exp(−Ω)", title="(b) damage fraction profile (tumour: tumour kinetics, x > h: Henriques–Moritz)", series=s,
                  ks=[0, 1, 2, 3], xlim=(0, 12), legend="ur", vlines=[(4, "h")], ylim=(-0.02, 1.05)))
    s = [(h["t"], [a / 1e3 for a in h["sigN_h"]], "normal side of x = h"),
         (h["t"], [a / 1e3 for a in h["sigT_h"]], "tumour side of x = h"),
         (h["t"], [a / 1e3 for a in h["sig_0"]], "surface x = 0"),
         ([0, h["t"][-1]], [-36, -36], "limit (−36 kPa)")]
    P.append(dict(xlabel="t (s)", ylabel="σ_{∥} (kPa)", title="(c) in-plane stress at the interface and at the surface", series=s, ks=[0, 1, 2, 3], legend="lr"))
    return stacked("Figure_4", P)


def fig5():
    co = C["common"]
    s = [(co[nm]["hist"]["t"], co[nm]["hist"]["th"][1], nm) for nm in ("Pennes", "CV", "MGT", "MGL")]
    P = [dict(xlabel="t (s)", ylabel="θ(h, t) (K)", title="(a) interface temperature for the Pennes-optimal pulse train under four models", series=s, ks=[0, 1, 2, 3], legend="ur", xlim=(0, 120))]
    ts = C["tau_sweep"]
    s = []
    for nm, lab in (("CV", "CV: τ_{q}"), ("MGL", "MGL: τ_{0}")):
        rows = [r for r in ts[nm] if r["scale"]]
        s.append(([r["tau"] for r in rows], [r["scale"] for r in rows], lab))
    P.append(dict(xlabel="relaxation time τ (s)", ylabel="dose multiplier s*", title="(b) I_{0} multiplier that just satisfies the kill constraint", series=s, ks=[0, 1], legend="ll"))
    es = C["eta_sweep"]
    P.append(dict(xlabel="η = k* τ_{q} / k", ylabel="dose multiplier s*", title="(c) MGT-type model: dependence on the thermal-displacement coefficient (τ_{q} = 2 s)",
                  series=[([r["eta"] for r in es], [r["scale"] for r in es], "MGT, τ_{q} = 2 s")], ks=[2], legend="ll"))
    return stacked("Figure_5", P)


def tornado(items, title):
    def draw(x0, y0, w, h):
        o = []
        vmax = max(abs(v) for _, v, _ in items) * 1.15
        vmax = max(vmax, 1.0)
        cx = x0 + w * 0.55
        scale = (w * 0.42) / vmax
        o.append('<text x="%g" y="%g" font-size="15" font-weight="bold">%s</text>' % (x0, y0 - 8, rich(title)))
        o.append('<rect x="%g" y="%g" width="%g" height="%g" fill="white" stroke="#222" stroke-width="1.2"/>' % (x0, y0, w, h))
        rh = (h - 10) / len(items)
        o.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#222"/>' % (cx, y0, cx, y0 + h))
        for i, (lab, v, feas) in enumerate(items):
            yy = y0 + 6 + i * rh
            bw = abs(v) * scale
            xx = cx if v >= 0 else cx - bw
            col = "#1f4e9c" if feas else "#c0392b"
            o.append('<rect x="%g" y="%g" width="%g" height="%g" fill="%s" fill-opacity="0.8"/>' % (xx, yy, max(bw, 1.0), rh * 0.72, col))
            o.append('<text x="%g" y="%g" font-size="11" text-anchor="end">%s</text>' % (x0 + w * 0.12 + 40, yy + rh * 0.55, rich(lab)))
            tx = cx + bw + 4 if v >= 0 else cx - bw - 4
            o.append('<text x="%g" y="%g" font-size="10" text-anchor="%s">%+.0f%%</text>' % (tx, yy + rh * 0.55, "start" if v >= 0 else "end", v))
        o.append('<text x="%g" y="%g" font-size="12" text-anchor="middle">relative change of the minimal collateral objective J (%%); red: constraint violated at best design</text>' % (x0 + w / 2, y0 + h + 34))
        return "\n".join(o)
    return draw


def fig6():
    s = []
    for k, nm in enumerate(("Pennes", "CV", "MGT", "MGL")):
        pn = OM["S1_" + nm]["per_np"]
        s.append(([r["Np"] for r in pn], [r["J"] for r in pn], nm))
    P = [dict(xlabel="number of pulses N_{p}", ylabel="min J (scenario S1)", title="(a) best objective for each pulse number", series=s, ks=[0, 1, 2, 3], legend="ul", ylim=(0, 0.35))]
    covs = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    s = []
    for sc, lab in (("S1", "S1 selective"), ("S2", "S2 non-selective")):
        s.append(([c * 4.0 for c in covs], [math.log10(OP["%s_cov%.1f" % (sc, c)]["best"]["m"]["JF"] * 1e3) for c in covs], lab))
    P.append(dict(xlabel="guaranteed kill depth (mm), damage fraction at least 0.99", ylabel="log_{10} J_{F} (mm)", title="(b) Pareto front: collateral damage vs kill depth (MGL)", series=s, ks=[0, 1], legend="lr"))
    base = OS["base"]["best"]["J"]
    items = []
    names = {"EaT=5.0e5": "E_a(T) 5.0e5", "EaT=6.0e5": "E_a(T) 6.0e5", "trefT=1800s": "t_ref 1800 s", "trefT=7200s": "t_ref 7200 s",
             "AfacN=10": "A_N x10", "AfacN=0.1": "A_N x0.1", "wbscale=0": "perfusion x0", "wbscale=3": "perfusion x3", "wbscale=10": "perfusion x10",
             "kv=1": "shutdown kv=1", "no vasodilation": "no vasodilation", "tau0=0.5": "τ0 0.5 s", "tau0=5": "τ0 5 s", "tau0=10": "τ0 10 s",
             "tau1=0": "τ1 0", "tau1=5": "τ1 5 s", "tau1=10": "τ1 10 s", "mua x0.8": "μa x0.8", "mua x1.25": "μa x1.25", "mus x0.8": "μs x0.8",
             "mus x1.25": "μs x1.25", "h=3mm": "h 3 mm", "h=5mm": "h 5 mm", "Teval=60s": "t_eval 60 s", "Teval=300s": "t_eval 300 s"}
    for k, lab in names.items():
        r = OS[k]
        items.append((lab, 100 * (r["best"]["J"] / base - 1), sum(r["best"]["v"]) < 1e-9))
    items.sort(key=lambda a: -abs(a[1]))
    items = items[:16]
    P.append(dict(custom=tornado(items, "(c) one-at-a-time sensitivity of the optimum (largest 16 effects)")))
    return stacked("Figure_6", P, extra_h=30)


if __name__ == "__main__":
    for f in (fig1, fig2, fig3, fig4, fig5, fig6):
        print(f.__name__, f())
