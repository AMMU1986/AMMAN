"""Seven figures (SVG -> PNG via headless Chromium).  Fig 1 is a schematic (geometry, mesh, flow chart);
Figures 2-7 are computed from results.json (the FE solutions, the exact solution and the property model)."""
import json, math, os, re
import plot
from plot import Panel, rich

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
R = json.load(open(os.path.join(HERE, "results.json")))
C = R["cases"]
W, PX, PW, PH, GAP = 900, 105, 760, 300, 95
SAMPLE = [round(0.05 * k, 3) for k in range(2, 41)]
DEFS = ('<defs><marker id="ar" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
        '<path d="M0,0 L10,4 L0,8 z" fill="#222"/></marker></defs>')


def stacked(name, panels):
    body = []
    for j, pd in enumerate(panels):
        p = Panel(PX, 40 + j * (PH + GAP), PW, PH, pd["xlabel"], pd["ylabel"], pd.get("title"),
                  yscale=pd.get("scale", 1.0), ylabel_exp=pd.get("exp"))
        for k, (xs, ys, lab) in enumerate(pd["series"]):
            p.line(xs, ys, lab, pd.get("ks", list(range(len(pd["series"]))))[k])
        for x, lab in pd.get("vlines", []):
            p.vline(x, lab)
        body.append(p.svg(xlim=pd.get("xlim"), ylim=pd.get("ylim"), legend_pos=pd.get("legend", "ur")))
    H = 40 + len(panels) * (PH + GAP) - 30
    return plot.write(name, W, H, "\n".join(body), OUT)


def hist(case, k, j):
    return C[case]["t"], [h[j] for h in C[case]["hist"][k]]


def prof(case, tkey, j):
    rows = C[case]["snaps"][tkey]
    return SAMPLE, [r[j] for r in rows]


def fig1():
    o = [DEFS]
    t = lambda x, y, s, **kw: o.append('<text x="%g" y="%g" font-size="%d" %s>%s</text>' % (
        x, y, kw.get("fs", 14), kw.get("extra", ""), rich(s)))
    # (a) geometry
    t(450, 18, "(a) Geometry: radially graded / porous medium around the line source", fs=15, extra='font-weight="bold" text-anchor="middle"')
    o.append('<rect x="60" y="50" width="780" height="130" fill="#eef2f7" stroke="#555"/>')
    o.append('<rect x="60" y="50" width="340" height="130" fill="#d9c7a8" stroke="#555"/>')
    o.append('<line x1="60" y1="115" x2="860" y2="115" stroke="#222" stroke-width="1.5" marker-end="url(#ar)"/>')
    o.append('<circle cx="60" cy="115" r="7" fill="#c0392b"/>')
    t(66, 44, "line source (r = 0), Q = Q_{0}δ(r)H(t)/(2πr)", extra='fill="#c0392b"')
    t(230, 90, "graded zone 0 < r < L_{g}", extra='text-anchor="middle"')
    t(230, 140, "V_{m}(r) = (r/L_{g})^{n},  porosity φ(r)", extra='text-anchor="middle"')
    t(620, 90, "homogeneous far field (V_{m} = 1)", extra='text-anchor="middle"')
    t(620, 140, "wave front r = c_{w}t stays inside R_{out}", extra='text-anchor="middle"')
    o.append('<line x1="400" y1="50" x2="400" y2="180" stroke="#555" stroke-dasharray="4,3"/>')
    t(400, 198, "L_{g}", extra='text-anchor="middle"')
    t(840, 198, "R_{out}", extra='text-anchor="end"')
    t(868, 120, "r", extra='font-style="italic"')
    # (b) mesh
    t(450, 238, "(b) Finite element mesh (quadratic elements, regularised source of radius a)", fs=15, extra='font-weight="bold" text-anchor="middle"')
    o.append('<line x1="60" y1="290" x2="840" y2="290" stroke="#222" stroke-width="1.5"/>')
    for k in range(0, 40):
        x = 60 + k * 12
        o.append('<line x1="%g" y1="282" x2="%g" y2="298" stroke="#1f4e9c" stroke-width="1.6"/>' % (x, x))
        if x + 6 < 840:
            o.append('<circle cx="%g" cy="290" r="2.6" fill="#1f4e9c"/>' % (x + 6))
    x = 60 + 39 * 12
    h = 12.0
    while x < 840:
        h *= 1.1
        x += h
        o.append('<line x1="%g" y1="282" x2="%g" y2="298" stroke="#1f4e9c" stroke-width="1.6"/>' % (min(x, 840), min(x, 840)))
    o.append('<rect x="60" y="305" width="60" height="10" fill="#c0392b" fill-opacity="0.5"/>')
    t(60, 335, "source disc, r < a (mesh aligned to a)", extra='fill="#c0392b"')
    t(480, 335, "uniform h = 0.0125 to r = 2.5", extra='text-anchor="middle"')
    t(790, 335, "geometric growth 1.1", extra='text-anchor="middle"')
    t(60, 270, "u(0) = 0, θ_{r}(0) = 0")
    t(840, 270, "u = θ = 0 at R_{out}", extra='text-anchor="end"')
    # (c) flow chart
    t(450, 378, "(c) Solution procedure", fs=15, extra='font-weight="bold" text-anchor="middle"')
    boxes = ["property fields P, L, k, ρ, ρc, g (grading + porosity)", "weak form, element matrices M, K, G, M_{θ}, D, K_{θ}",
             "state variables (u, m, θ, g): operators (1+τ_{1}d/dt), (1+τ_{0}d/dt) removed",
             "trapezoidal marching: banded LU once, back-substitution per step",
             "checks: exact K_{0} solution, Laplace-domain FE, convergence, heat balance"]
    for i, b in enumerate(boxes):
        y = 392 + i * 62
        o.append('<rect x="120" y="%d" width="660" height="44" rx="8" fill="#eef2f7" stroke="#1f4e9c" stroke-width="1.5"/>' % y)
        t(450, y + 27, b, extra='text-anchor="middle"')
        if i < 4:
            o.append('<line x1="450" y1="%d" x2="450" y2="%d" stroke="#222" stroke-width="1.5" marker-end="url(#ar)"/>' % (y + 44, y + 62))
    body = "\n".join(o)
    return plot.write("Figure_1", 900, 720, body, OUT)


def fig2():
    r = R["prof_r"]
    P = R["prof"]
    a = [(r, P[k]["c"], lab) for k, lab in (("hom", "n = 0 (homogeneous)"), ("n0.5", "n = 0.5"), ("n1", "n = 1"), ("n2", "n = 2"), ("n5", "n = 5"))]
    b = [(r, P[k]["c"], lab) for k, lab in (("hom", "φ = 0"), ("p0.2", "φ = 0.2 uniform"), ("p0.3", "φ = 0.3 uniform"),
                                              ("n1p0.2", "n = 1, φ = 0.2"), ("pg", "n = 1, graded φ_{0}=0.3"))]
    c = [(r, [q["k"] for q in P[k]["q"]], lab) for k, lab in (("n1", "k̂, n = 1"), ("n2", "k̂, n = 2"))]
    c += [(r, [q["P"] for q in P[k]["q"]], lab) for k, lab in (("n1", "P, n = 1"), ("n2", "P, n = 2"))]
    return stacked("Figure_2", [
        dict(series=a, xlabel="Radial distance r", ylabel="Local wave speed c(r)", title="(a) Power-law grading", legend="lr", ylim=(0, 8)),
        dict(series=b, xlabel="Radial distance r", ylabel="Local wave speed c(r)", title="(b) Porosity and combined models", legend="lr", ylim=(0, 8)),
        dict(series=c, xlabel="Radial distance r", ylabel="Property ratio", title="(c) Conductivity and P-modulus ratios", legend="lr", ylim=(0, 2.1), ks=[0, 1, 2, 3])])


def fig3():
    td = R["tdense"]
    ex = R["exact_dense_H0"]
    t, th = hist("H0", 0, 0)
    t_, su = hist("H0", 0, 2)
    _, sp = hist("H0", 0, 3)
    ra = R["exact_prof_dense_r"]
    exp_ = R["exact_prof_dense"]
    rs, thp = prof("H0", "0.2", 0)
    return stacked("Figure_3", [
        dict(series=[(t, th, "FE (P2)"), (td, [e[0] for e in ex], "exact")], xlabel="Time t", ylabel="Temperature θ(0.3, t)",
             title="(a) Temperature history at r = 0.3", legend="ul", ks=[0, 1]),
        dict(series=[(t, su, "FE σ_{rr}"), (td, [e[2] for e in ex], "exact σ_{rr}"), (t, sp, "FE σ_{φφ}"), (td, [e[3] for e in ex], "exact σ_{φφ}")],
             xlabel="Time t", ylabel="Stress", scale=1e3, exp=-3, title="(b) Stress histories at r = 0.3", legend="lr", ks=[0, 1, 2, 3]),
        dict(series=[(rs, thp, "FE (P2)"), (ra, [e[0] for e in exp_], "exact")], xlabel="Radial distance r", ylabel="Temperature θ(r, 0.2)",
             title="(c) Radial profile at t = 0.2", legend="ur", ks=[0, 1], xlim=(0, 1.6))])


def lg(x):
    return math.log10(max(x, 1e-12))


def fig4():
    cv = R["conv"]
    p1 = [(0.05, "P1_h0.05"), (0.025, "P1_h0.025"), (0.0125, "P1_h0.0125"), (0.00625, "P1_h0.00625")]
    p2 = [(0.05, "P2_h0.05"), (0.025, "P2_h0.025"), (0.0125, "P2_h0.0125")]
    dts = [(0.005, "dt_0.005"), (0.0025, "dt_0.0025"), (0.00125, "dt_0.00125"), (0.000625, "dt_0.000625"), (0.0003125, "dt_0.0003125")]
    a = []
    for lab, pts, j in (("P1, θ", p1, 0), ("P1, σ_{rr}", p1, 2), ("P2, θ", p2, 0), ("P2, σ_{rr}", p2, 2)):
        a.append(([lg(h) for h, _ in pts], [lg(cv[k]["hist"][j]) for _, k in pts], lab))
    b = []
    for lab, j in (("θ", 0), ("u", 1), ("σ_{rr}", 2)):
        b.append(([lg(h) for h, _ in dts], [lg(cv[k]["hist"][j]) for _, k in dts], lab))
    reg = R["reg"]
    av = [0.2, 0.1, 0.05, 0.025]
    c = []
    for lab, j in (("θ", 0), ("u", 1), ("σ_{rr}", 2), ("σ_{φφ}", 3)):
        c.append(([lg(x) for x in av], [lg(rg[1][j]) for rg in reg], lab))
    return stacked("Figure_4", [
        dict(series=a, xlabel="log_{10} h (spatial refinement, dt = 2.5×10^{-4})", ylabel="log_{10} E (%)", title="(a) Spatial self-convergence", legend="ur"),
        dict(series=b, xlabel="log_{10} Δt (h = 0.0125, P2)", ylabel="log_{10} E (%)", title="(b) Time-step self-convergence", legend="lr", ks=[0, 1, 2]),
        dict(series=c, xlabel="log_{10} a (source radius)", ylabel="log_{10} E (%)", title="(c) Regularisation error against the exact line source", legend="lr", ks=[0, 1, 2, 3])])


def fig5():
    cs = [("H0", "n = 0"), ("FG_n1", "n = 1"), ("FG_n2", "n = 2"), ("FG_n5", "n = 5"), ("FG_exp3", "exp, β = 3")]
    pan = []
    for j, (yl, ti, sc, ex) in enumerate((("Temperature θ", "(a) Temperature at r = 0.3", 1.0, None),
                                           ("Displacement u", "(b) Radial displacement at r = 0.3", 1e4, -4),
                                           ("Stress σ_{rr}", "(c) Radial stress at r = 0.3", 1e3, -3))):
        jj = (0, 1, 2)[j]
        pan.append(dict(series=[hist(c, 0, jj) + (lab,) for c, lab in cs], xlabel="Time t", ylabel=yl, title=ti,
                        scale=sc, exp=ex, legend="ul" if j < 2 else "lr"))
    return stacked("Figure_5", pan)


def fig6():
    cs = [("H0", "φ = 0"), ("P_0.1", "φ = 0.1"), ("P_0.2", "φ = 0.2"), ("P_0.3", "φ = 0.3"), ("PG_0.3_n1", "graded φ_{0}=0.3, n = 1")]
    a = [hist(c, 0, 0) + (lab,) for c, lab in cs]
    b = [hist(c, 0, 3) + (lab,) for c, lab in cs]
    c_ = [prof(c, "0.2", 1) + (lab,) for c, lab in cs]
    return stacked("Figure_6", [
        dict(series=a, xlabel="Time t", ylabel="Temperature θ(0.3, t)", title="(a) Temperature at r = 0.3", legend="ul"),
        dict(series=b, xlabel="Time t", ylabel="Hoop stress σ_{φφ}(0.3, t)", scale=1e3, exp=-3, title="(b) Hoop stress at r = 0.3", legend="lr"),
        dict(series=c_, xlabel="Radial distance r", ylabel="Displacement u(r, 0.2)", scale=1e4, exp=-4, title="(c) Displacement profile at t = 0.2", legend="ur", xlim=(0, 1.6))])


def fig7():
    a = [prof(c, "0.2", 2) + (lab,) for c, lab in (("FG_t1_0", "τ_{1} = 0"), ("FG_t1_0.02", "τ_{1} = 0.02"), ("FG_t1_0.05", "τ_{1} = 0.05"), ("FG_t1_0.1", "τ_{1} = 0.1"))]
    b = [prof(c, "0.1", 0) + (lab,) for c, lab in (("FG_t0_0", "τ_{0} = 0"), ("FG_t0_0.01", "τ_{0} = 0.01"), ("FG_t1_0.05", "τ_{0} = 0.02"), ("FG_t0_0.04", "τ_{0} = 0.04"))]
    c_ = [hist(c, 0, 0) + (lab,) for c, lab in (("FGP_CTE", "CTE (τ_{0}=τ_{1}=0)"), ("FGP_LS", "LS-type (τ_{1}=0)"), ("FGP_n1_0.2", "MGL"))]
    return stacked("Figure_7", [
        dict(series=a, xlabel="Radial distance r", ylabel="Stress σ_{rr}(r, 0.2)", scale=1e3, exp=-3, title="(a) Effect of τ_{1} (n = 1, MGL)", legend="lr", xlim=(0, 1.6)),
        dict(series=b, xlabel="Radial distance r", ylabel="Temperature θ(r, 0.1)", title="(b) Effect of τ_{0} (n = 1, MGL)", legend="ur", xlim=(0, 1.2)),
        dict(series=c_, xlabel="Time t", ylabel="Temperature θ(0.3, t)", title="(c) Theories in the graded porous medium (n = 1, φ = 0.2)", legend="ul", ks=[0, 1, 2])])


if __name__ == "__main__":
    for f in (fig1, fig2, fig3, fig4, fig5, fig6, fig7):
        print(f.__name__, f())
