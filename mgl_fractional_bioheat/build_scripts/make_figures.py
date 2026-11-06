"""Seven figures (SVG -> PNG via headless Chromium).  Figure 1 is a schematic (no data); Figures 2-7 are
computed from results.json / valfig.json (FE solutions, Laplace-domain reference solutions, steady-state checks)."""
import json, math, os
import plot
from plot import Panel, rich
import model

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
R = json.load(open(os.path.join(HERE, "results.json")))
VF = json.load(open(os.path.join(HERE, "valfig.json")))
S = R["studies"]
W, PX, PW, PH, GAP = 900, 105, 760, 280, 95
XG = [round(0.01 * i, 2) for i in range(101)]
DEFS = ('<defs><marker id="ar" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
        '<path d="M0,0 L10,4 L0,8 z" fill="#222"/></marker></defs>')


def stacked(name, panels):
    body = []
    for j, pd in enumerate(panels):
        p = Panel(PX, 40 + j * (PH + GAP), PW, PH, pd["xlabel"], pd["ylabel"], pd.get("title"))
        for k, (xs, ys, lab) in enumerate(pd["series"]):
            p.line(xs, ys, lab, pd.get("ks", list(range(len(pd["series"]))))[k])
        for x, lab in pd.get("vlines", []):
            p.vline(x, lab)
        body.append(p.svg(xlim=pd.get("xlim"), ylim=pd.get("ylim"), legend_pos=pd.get("legend", "ur")))
    H = 40 + len(panels) * (PH + GAP) - 30
    return plot.write(name, W, H, "\n".join(body), OUT)


def snap(case, t, j):
    return [r[j] for r in case["snaps"][str(t)]]


def hist(case, k, j):
    return case["t"], [h[j] for h in case["hist"][k]]


def fig1():
    o = [DEFS]
    t = lambda x, y, s, **kw: o.append('<text x="%g" y="%g" font-size="%d" %s>%s</text>' % (
        x, y, kw.get("fs", 14), kw.get("extra", ""), rich(s)))
    t(450, 22, "(a) Layered slab: tumour 0 < x < h, normal tissue h < x < L", fs=15, extra='font-weight="bold" text-anchor="middle"')
    o.append('<rect x="80" y="60" width="150" height="120" fill="#e8c9c9" stroke="#444" stroke-width="1.5"/>')
    o.append('<rect x="230" y="60" width="590" height="120" fill="#d6e4f0" stroke="#444" stroke-width="1.5"/>')
    t(155, 112, "tumour (1)", extra='text-anchor="middle"')
    t(155, 134, "w_{b1}(θ), k_{1}(θ)", extra='text-anchor="middle"')
    t(525, 112, "normal tissue (2)", extra='text-anchor="middle"')
    t(525, 134, "w_{b2}(θ), k_{2}", extra='text-anchor="middle"')
    o.append('<line x1="230" y1="52" x2="230" y2="190" stroke="#222" stroke-dasharray="4,3"/>')
    t(230, 208, "x = h (interface)", extra='text-anchor="middle"')
    t(80, 208, "x = 0", extra='text-anchor="middle"')
    t(820, 208, "x = L", extra='text-anchor="middle"')
    t(10, 100, "θ=θ_{0}H(t)", fs=12, extra='')
    t(10, 120, "σ = 0", extra='')
    t(826, 100, "u = 0", extra='')
    t(826, 120, "θ = 0", extra='')
    o.append('<line x1="130" y1="46" x2="130" y2="58" stroke="#c0392b" stroke-width="2.5" marker-end="url(#ar)"/>')
    t(142, 36, "laser I_{0}f(t)", extra='fill="#c0392b"')
    # (b) mesh
    t(450, 252, "(b) Finite element mesh: nodes at the interface, linear elements", fs=15, extra='font-weight="bold" text-anchor="middle"')
    o.append('<line x1="80" y1="290" x2="820" y2="290" stroke="#222" stroke-width="2"/>')
    for i in range(0, 38):
        x = 80 + i * 20
        o.append('<line x1="%g" y1="282" x2="%g" y2="298" stroke="#222"/>' % (x, x))
    o.append('<line x1="230" y1="270" x2="230" y2="310" stroke="#c0392b" stroke-width="2.5"/>')
    t(230, 328, "interface node", extra='text-anchor="end" fill="#c0392b"')
    t(260, 328, "dofs per node: u, θ ;  banded matrix, half bandwidth 3", extra='')
    # (c) flow chart
    t(450, 372, "(c) Solution procedure for each time step t_{n}", fs=15, extra='font-weight="bold" text-anchor="middle"')
    boxes = [("history sums", "Σ c_{j}z_{n-j}, j > 0"), ("assemble", "K(θ^{k}), ω(θ^{k})"), ("banded LU", "solve u^{k+1}, θ^{k+1}"),
             ("Picard test", "max|Δθ| < 10^{-11}?"), ("post-process", "σ, flux, metrics")]
    for i, (a, b) in enumerate(boxes):
        x = 40 + i * 168
        o.append('<rect x="%g" y="392" width="140" height="64" rx="6" fill="#f3f3f3" stroke="#444"/>' % x)
        t(x + 70, 418, a, extra='text-anchor="middle" font-weight="bold"')
        t(x + 70, 440, b, fs=12, extra='text-anchor="middle"')
        if i < 4:
            o.append('<line x1="%g" y1="424" x2="%g" y2="424" stroke="#222" marker-end="url(#ar)"/>' % (x + 140, x + 168))
    o.append('<path d="M 544 456 L 544 480 L 296 480 L 296 458" fill="none" stroke="#222" marker-end="url(#ar)"/>')
    t(420, 498, "not converged: next Picard iteration", fs=12, extra='text-anchor="middle"')
    t(450, 540, "Schematic only: contains no computed data.", fs=13, extra='text-anchor="middle" font-style="italic"')
    return plot.write("Figure_1", W, 560, "\n".join(o), OUT)


def fig2():
    P = []
    ser = lambda f, comp, k: [r[comp][k] for r in f]
    for comp, ylab, xo, ttl in ((0, "θ", 1, "(a) temperature at x = 0.3 (normal tissue)"), (1, "u", 0, "(b) displacement at x = 0.1 (tumour)"), (2, "σ", 0, "(c) stress at x = 0.1 (tumour)")):
        s = []
        for al in ("a1", "a0.6"):
            d = VF[al]
            lab = "α = " + al[1:]
            s.append((d["t"], ser(d["fem"], comp, xo), "FE, " + lab))
            s.append((d["t"], ser(d["lap"], comp, xo), "Laplace, " + lab))
        P.append(dict(xlabel="t", ylabel=ylab, title=ttl, series=s, ks=[0, 1, 2, 3], legend={0: "lr", 1: "ur", 2: "lr"}[comp]))
    return stacked("Figure_2", P)


def fig3():
    C = R["conv"]
    lg = lambda v: math.log10(v)
    s = []
    for k, (key, lab) in enumerate((("dt_H_a1", "Heaviside, α=1"), ("dt_H_a0.6", "Heaviside, α=0.6"), ("dt_ramp_a1", "smooth ramp, α=1"), ("dt_ramp_a0.6", "smooth ramp, α=0.6"))):
        rows = C[key]
        s.append(([lg(r[0]) for r in rows], [lg(r[2]) for r in rows], lab))
    P = [dict(xlabel="log_{10} Δt", ylabel="log_{10} (u error)", title="(a) time-step convergence of displacement", series=s, ks=[0, 1, 2, 3], legend="ul")]
    s = []
    for k, (key, lab) in enumerate((("dx_ramp_a0.6", "smooth ramp, α=0.6"), ("dx_H_a0.6", "Heaviside, α=0.6"))):
        rows = C[key]
        s.append(([lg(r[0]) for r in rows], [lg(max(r[1], 1e-12)) for r in rows], lab + ", θ"))
        s.append(([lg(r[0]) for r in rows], [lg(max(r[2], 1e-12)) for r in rows], lab + ", u"))
    P.append(dict(xlabel="log_{10} Δx", ylabel="log_{10} (error)", title="(b) mesh convergence at Δt = 0.0025", series=s, ks=[0, 1, 2, 3], legend="lr"))
    pic = R["picard"]
    res = pic["resid"]
    P.append(dict(xlabel="Picard iteration k (final step)", ylabel="log_{10} max|Δθ|", title="(c) Picard residual, Π = 10, c_{w} = (0.5, 3), χ_{1} = 0.2",
                  series=[(list(range(1, len(res) + 1)), [math.log10(max(v, 1e-18)) for v in res], "residual")], ks=[0], legend="ur"))
    return stacked("Figure_3", P)


def fig4():
    M = R["models"]
    xg = R["xg_models"]
    names = [("Pennes", "Pennes"), ("MGT", "MGT"), ("LS-type", "LS-type"), ("MGL", "MGL, α=1"), ("fMGL0.75", "fMGL, α=0.75"), ("fMGL0.5", "fMGL, α=0.5")]
    P = []
    for t, ttl in ((0.1, "(a) temperature profile at t = 0.1"), (0.4, "(b) temperature profile at t = 0.4")):
        P.append(dict(xlabel="x", ylabel="θ", title=ttl, series=[(xg, [r[0] for r in M[n]["snaps"][str(t)]], lab) for n, lab in names],
                      ks=list(range(6)), vlines=[(0.2, "h")], legend="ur"))
    P.append(dict(xlabel="x", ylabel="σ", title="(c) stress profile at t = 0.1", series=[(xg, [r[2] for r in M[n]["snaps"]["0.1"]], lab) for n, lab in names],
                  ks=list(range(6)), vlines=[(0.2, "h")], legend="lr"))
    return stacked("Figure_4", P)


def fig5():
    als = [1, 0.9, 0.75, 0.6, 0.45, 0.3]
    key = lambda a: "base" if a == 1 else "alpha_%g" % a
    P = []
    P.append(dict(xlabel="x", ylabel="θ", title="(a) temperature at t = 0.2", series=[(XG, snap(S[key(a)], 0.2, 0), "α = %g" % a) for a in als], ks=list(range(6)), vlines=[(0.2, "h")], legend="ur"))
    P.append(dict(xlabel="t", ylabel="θ(h, t)", title="(b) tumour-edge temperature", series=[(S[key(a)]["t"], [h[0] for h in S[key(a)]["hist"][2]], "α = %g" % a) for a in als], ks=list(range(6)), legend="lr"))
    P.append(dict(xlabel="x", ylabel="σ", title="(c) stress at t = 0.2", series=[(XG, snap(S[key(a)], 0.2, 2), "α = %g" % a) for a in als], ks=list(range(6)), vlines=[(0.2, "h")], legend="lr"))
    return stacked("Figure_5", P)


def fig6():
    th = [0.02 * i for i in range(0, 76)]
    P = [dict(xlabel="θ", ylabel="ω(θ) = w_{b}/w_{b0}", title="(a) perfusion law: tumour (c_{w}=0.5, θ_{c}=0.6) and normal tissue (c_{w}=3, θ_{c}=0.9)",
              series=[(th, [model.omega(v, 0.5, 0.6, 0.1) for v in th], "tumour"), (th, [model.omega(v, 3.0, 0.9, 0.1) for v in th], "normal")], ks=[0, 1], legend="ur")]
    P.append(dict(xlabel="x", ylabel="θ", title="(b) temperature at t = 0.6, nonlinear perfusion",
                  series=[(XG, snap(S["Pi_%g" % v], 0.6, 0), "Π = %g" % v) for v in (0, 2, 5, 10, 20)], ks=list(range(5)), vlines=[(0.2, "h")], legend="ur"))
    P.append(dict(xlabel="x", ylabel="θ", title="(c) Π = 10 at t = 0.6: constant vs temperature-dependent perfusion",
                  series=[(XG, snap(S["Pi_10_c0"], 0.6, 0), "w_{b} constant"), (XG, snap(S["Pi_10"], 0.6, 0), "w_{b}(θ)"), (XG, snap(S["chi_cw"], 0.6, 0), "w_{b}(θ), χ_{1}=0.3 (Π=10)")][:2],
                  ks=[0, 1], vlines=[(0.2, "h")], legend="ur"))
    return stacked("Figure_6", P)


def fig7():
    P = []
    ts = ("base", "tau1_0", "tau1_0.025", "tau1_0.1", "tau1_0.2")
    labs = ("τ_{1}=0.05", "τ_{1}=0", "τ_{1}=0.025", "τ_{1}=0.1", "τ_{1}=0.2")
    P.append(dict(xlabel="t", ylabel="σ(0.1, t)", title="(a) stress at x = 0.1: strain-rate lag τ_{1} (α = 1)", series=[(S[k]["t"], [h[2] for h in S[k]["hist"][1]], l) for k, l in zip(ts, labs)], ks=list(range(5)), legend="lr"))
    hs = (("h_0.1", 0.1), ("h_0.2", 0.2), ("h_0.3", 0.3), ("h_0.4", 0.4))
    P.append(dict(xlabel="x", ylabel="θ", title="(b) temperature at t = 0.2 for interface positions (α = 0.75)", series=[(XG, snap(S[k], 0.2, 0), "h = %g" % h) for k, h in hs], ks=list(range(4)), legend="ur"))
    al = (("base", "α = 1"), ("alpha_0.75", "α = 0.75"), ("alpha_0.45", "α = 0.45"))
    P.append(dict(xlabel="t", ylabel="θ(0.5, t)", title="(c) temperature far beyond the interface, x = 0.5", series=[(S[k]["t"], [h[0] for h in S[k]["hist"][4]], l) for k, l in al], ks=[0, 1, 2], legend="ul"))
    return stacked("Figure_7", P)


if __name__ == "__main__":
    for f in (fig1, fig2, fig3, fig4, fig5, fig6, fig7):
        print(f.__name__, f())
