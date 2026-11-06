"""Generate Figures 1-8 (SVG -> PNG) from results.json."""
import json
import os
import plot
from plot import Panel, rich

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
os.makedirs(OUT, exist_ok=True)
R = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")))
RUNS = R["runs"]
EPS = R["constants"]["eps"]
VW = 1.0 / (((1 + EPS) * R["tau0"]) ** 0.5)
A = R["a"]
W, H = 900, 560
PX, PY, PW, PH = 100, 40, 760, 440
XL = "Dimensionless radius r"


def fig1():
    o = []
    for k, (cx, title) in enumerate([(230, "(a) Spherical cavity (meridional section)"),
                                     (680, "(b) Cylindrical hole (cross-section, plane strain)")]):
        o.append('<rect x="%d" y="50" width="420" height="420" fill="#eef2f7" stroke="#555"/>' % (cx - 210))
        cy = 260
        o.append('<circle cx="%d" cy="%d" r="150" fill="none" stroke="#c0392b" stroke-width="1.6" stroke-dasharray="7,5"/>' % (cx, cy))
        o.append('<circle cx="%d" cy="%d" r="55" fill="white" stroke="#1f4e9c" stroke-width="3"/>' % (cx, cy))
        if k == 0:
            o.append('<ellipse cx="%d" cy="%d" rx="55" ry="14" fill="none" stroke="#1f4e9c" stroke-width="1" stroke-dasharray="3,3"/>' % (cx, cy))
        else:
            o.append('<circle cx="%d" cy="%d" r="4" fill="#333"/>' % (cx, cy))
            o.append('<text x="%d" y="%d" font-size="13">z axis (out of plane)</text>' % (cx - 50, cy + 30))
        o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#222" stroke-width="1.5" marker-end="url(#ar)"/>' % (cx, cy, cx + 39, cy - 39))
        o.append('<text x="%d" y="%d" font-size="16" font-style="italic">a</text>' % (cx + 8, cy - 26))
        o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#222" stroke-width="1.5" marker-end="url(#ar)"/>' % (cx, cy, cx + 200, cy))
        o.append('<text x="%d" y="%d" font-size="16" font-style="italic">r</text>' % (cx + 190, cy - 8))
        o.append('<text x="%d" y="%d" font-size="13" text-anchor="middle" fill="#1f4e9c">%s</text>' % (cx, cy + 75, rich("r = a: θ = θ_{0}H(t), σ_{rr} = 0")))
        o.append('<text x="%d" y="%d" font-size="13" text-anchor="middle" fill="#c0392b">%s</text>' % (cx, cy - 160, rich("wavefront r = a + v_{w}t (α = 1)")))
        o.append('<text x="%d" y="%d" font-size="13" text-anchor="middle">%s</text>' % (cx, 455, rich("far field (eq. 10): θ, u, σ_{rr}, σ_{φφ} vanish as r grows")))
        o.append('<text x="%d" y="%d" font-size="13" text-anchor="middle">Unbounded isotropic MGL medium</text>' % (cx, 72))
        o.append('<text x="%d" y="%d" font-size="15" font-weight="bold" text-anchor="middle">%s</text>' % (cx, 30, title))
    defs = ('<defs><marker id="ar" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
            '<path d="M0,0 L10,4 L0,8 z" fill="#222"/></marker></defs>')
    return plot.write("Figure_1", 910, 490, defs + "\n".join(o), OUT)


def single(name, key, ylabel, scale, exp, runs_labels, title=None, legend="ur", vlines=None):
    p = Panel(PX, PY, PW, PH, XL, ylabel, title, yscale=scale, ylabel_exp=exp)
    for k, (rk, lab) in enumerate(runs_labels):
        v = RUNS[rk]
        p.line(v["r"], v[key], lab, k)
    for x, lab in (vlines or []):
        p.vline(x, lab)
    return plot.write(name, W, H, p.svg(legend_pos=legend), OUT)


def double(name, specs, runs_labels, legend=("ur", "ur"), vlines=None):
    body = []
    ph = 330
    for j, (key, ylabel, scale, exp, title) in enumerate(specs):
        p = Panel(PX, 40 + j * (ph + 95), PW, ph, XL, ylabel, title, yscale=scale, ylabel_exp=exp)
        for k, (rk, lab) in enumerate(runs_labels):
            v = RUNS[rk]
            p.line(v["r"], v[key], lab, k)
        for x, lab in (vlines or []):
            p.vline(x, lab)
        body.append(p.svg(legend_pos=legend[j]))
    return plot.write(name, W, 40 + 2 * (ph + 95), "\n".join(body), OUT)


def main():
    fig1()
    tl = [("sph_a1_t0.005", "t = 0.005"), ("sph_a1_t0.007", "t = 0.007"), ("sph_a1_t0.009", "t = 0.009")]
    fr = [(A + VW * t, "") for t in (0.005, 0.007, 0.009)]
    single("Figure_2", "theta", "Temperature θ", 1.0, None, tl, vlines=fr)
    single("Figure_3", "u", "Displacement u", 1e5, -5, tl, legend="lr", vlines=fr)
    single("Figure_4", "srr", "Radial stress σ_{rr}", 1e2, -2, tl, legend="lr", vlines=fr)
    single("Figure_5", "spp", "Hoop stress σ_{φφ}", 1e2, -2, tl, legend="lr", vlines=fr)
    al = [("sph_a0.5_t0.007", "α = 0.5"), ("sph_a0.75_t0.007", "α = 0.75"),
          ("sph_a0.9_t0.007", "α = 0.9"), ("sph_a1.0_t0.007", "α = 1.0")]
    double("Figure_6", [("theta", "Temperature θ", 1.0, None, "(a) Temperature"),
                        ("spp", "Hoop stress σ_{φφ}", 1e2, -2, "(b) Hoop stress")], al,
           legend=("ur", "lr"), vlines=[(A + VW * 0.007, "r = a + v_{w}t")])
    sc = [("sph_a1_t0.007", "Spherical cavity"), ("cyl_a1_t0.007", "Cylindrical hole")]
    double("Figure_7", [("theta", "Temperature θ", 1.0, None, "(a) Temperature"),
                        ("spp", "Hoop stress σ_{φφ}", 1e2, -2, "(b) Hoop stress")], sc,
           legend=("ur", "lr"), vlines=[(A + VW * 0.007, "r = a + v_{w}t")])
    ta = [("sph_a1_t0.007_tau0.03", "τ_{1} = 0.03"), ("sph_a1_t0.007", "τ_{1} = 0.05"),
          ("sph_a1_t0.007_tau0.08", "τ_{1} = 0.08")]
    single("Figure_8", "spp", "Hoop stress σ_{φφ}", 1e2, -2, ta, legend="lr",
           vlines=[(A + VW * 0.007, "r = a + v_{w}t")])


if __name__ == "__main__":
    main()
