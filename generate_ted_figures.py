#!/usr/bin/env python3
"""
Generate all figures and numerical tables for the manuscript
"Thermoelastic damping and quality factor of micro/nano-beam resonators
under an exact single-delay heat conduction model".

Outputs:
  ted_figures/Figure_1 ... Figure_10 (.png + .svg)
  ted_figures/ted_results.json  (numbers quoted in the tables / text)
"""

import json
import math
import os

from ted_model import (MATERIALS, BC_NAMES, LAMBDA1, solve, relaxation_strength, diffusivity,
                       omega0, lr_closed_form, zener, logspace, peak)
from svgplot import Axes, svg_doc, save, COLORS, DASHES, FONT, esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ted_figures")
os.makedirs(OUT, exist_ok=True)

SI = MATERIALS["Si"]
TAU0 = 1e-11       # baseline delay time, 10 ps
KSTAR = 1e10       # baseline conductivity rate, W/(m K s)
H = logspace(-9, -4, 501)          # 1 nm ... 100 um
RES = {}

QINV = "Q<tspan baseline-shift=\"super\" font-size=\"10\">\u22121</tspan>"
HLAB = "Beam thickness h (m)"


def qcurve(m, model, hs=H, bc="CC", **p):
    return [solve(m, h, model, bc=bc, **p)["Qinv"] for h in hs]


def pk(m, model, bc="CC", **p):
    hs = logspace(-9, -4, 1501)
    return peak(hs, qcurve(m, model, hs, bc, **p))


# ---------------------------------------------------------------------------
# Figure 1: schematic
# ---------------------------------------------------------------------------
def fig1():
    W, Hh = 900, 470
    b = []
    # supports
    b.append('<rect x="70" y="120" width="40" height="150" fill="#bfbfbf" stroke="#000"/>')
    b.append('<rect x="790" y="120" width="40" height="150" fill="#bfbfbf" stroke="#000"/>')
    for i in range(8):
        b.append('<line x1="70" y1="%d" x2="55" y2="%d" stroke="#000"/>' % (125 + 18 * i, 140 + 18 * i))
        b.append('<line x1="830" y1="%d" x2="845" y2="%d" stroke="#000"/>' % (125 + 18 * i, 140 + 18 * i))
    # deformed beam (first clamped-clamped mode shape, exaggerated)
    top, bot = [], []
    for i in range(0, 101):
        s = i / 100
        x = 110 + 680 * s
        lam = 4.730040745
        sig = (math.cosh(lam) - math.cos(lam)) / (math.sinh(lam) - math.sin(lam))
        phi = (math.cosh(lam * s) - math.cos(lam * s) - sig * (math.sinh(lam * s) - math.sin(lam * s))) / 1.588
        y = 175 + 45 * phi
        top.append("%.1f,%.1f" % (x, y))
        bot.append("%.1f,%.1f" % (x, y + 42))
    b.append('<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#e06666"/><stop offset="0.5" stop-color="#f2f2f2"/>'
             '<stop offset="1" stop-color="#5b9bd5"/></linearGradient></defs>')
    b.append('<polygon points="%s %s" fill="url(#g)" stroke="#000" stroke-width="1.5"/>' % (" ".join(top), " ".join(reversed(bot))))
    # undeformed centre line
    b.append('<line x1="110" y1="196" x2="790" y2="196" stroke="#555" stroke-dasharray="6,4"/>')
    # coordinate axes
    b.append('<line x1="110" y1="330" x2="190" y2="330" stroke="#000" stroke-width="2" marker-end="url(#a)"/>')
    b.append('<line x1="110" y1="330" x2="110" y2="390" stroke="#000" stroke-width="2" marker-end="url(#a)"/>')
    b.append('<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">'
             '<path d="M0,0 L0,6 L9,3 z" fill="#000"/></marker></defs>')
    b.append('<text x="196" y="335" font-size="16" font-family="%s">x</text>' % FONT)
    b.append('<text x="102" y="408" font-size="16" font-family="%s">z</text>' % FONT)
    # length / thickness annotations
    b.append('<line x1="110" y1="300" x2="790" y2="300" stroke="#000" marker-end="url(#a)"/>')
    b.append('<line x1="790" y1="300" x2="110" y2="300" stroke="#000" marker-end="url(#a)"/>')
    b.append('<text x="450" y="292" font-size="16" text-anchor="middle" font-family="%s">L = 10 h</text>' % FONT)
    b.append('<text x="450" y="160" font-size="14" text-anchor="middle" font-family="%s">mid-span, compression (z &lt; 0): heats up</text>' % FONT)
    b.append('<text x="450" y="245" font-size="14" text-anchor="middle" font-family="%s">mid-span, tension (z &gt; 0): cools down</text>' % FONT)
    # heat-flux arrows across the thickness
    for xx in (300, 600):
        b.append('<line x1="%d" y1="212" x2="%d" y2="232" stroke="#c00000" stroke-width="2.5" marker-end="url(#a)"/>' % (xx, xx))
        b.append('<text x="%d" y="230" font-size="13" fill="#c00000" font-family="%s">q<tspan baseline-shift="sub" font-size="10">z</tspan></text>' % (xx + 8, FONT))
    # thickness callout
    b.append('<line x1="845" y1="175" x2="845" y2="217" stroke="#000"/>')
    b.append('<text x="852" y="201" font-size="15" font-family="%s">h</text>' % FONT)
    # legend box for the heat law
    b.append('<rect x="300" y="330" width="560" height="120" fill="#fbfbfb" stroke="#999"/>')
    lines = ["Heat conduction across the thickness (exact single-delay law):",
             "q,t = \u2212k* \u03b8,z \u2212 (k + \u03c4\u2080k*) \u03b8,zt \u2212 (\u03c4\u2080\u00b2/2) k* \u03b8,ztt",
             "Adiabatic faces:  \u03b8,z = 0  at  z = \u00b1h/2",
             "Supports: clamped\u2013clamped (shown), simply supported, cantilever"]
    for i, s in enumerate(lines):
        b.append('<text x="315" y="%d" font-size="%d" font-family="%s">%s</text>' % (356 + 26 * i, 14 if i else 15, FONT, esc(s)))
    b.append('<text x="40" y="40" font-size="17" font-weight="bold" font-family="%s">Vibrating micro/nano-beam: bending strain drives a transverse temperature gradient</text>' % FONT)
    save(svg_doc(W, Hh, "\n".join(b)), os.path.join(OUT, "Figure_1_Beam_Schematic.png"), W, Hh)


# ---------------------------------------------------------------------------
# Figure 2: validation, Fourier limit vs Lifshitz-Roukes and Zener
# ---------------------------------------------------------------------------
def fig2():
    dE = relaxation_strength(SI)
    hs = logspace(-8, -4, 400)
    present = [solve(SI, h)["Qinv"] for h in hs]
    chi = diffusivity(SI)
    lr = [dE * lr_closed_form(h * math.sqrt(omega0(SI, h) / (2 * chi))) for h in hs]
    zn = [zener(SI, h, omega0(SI, h)) for h in hs]
    ax = Axes(110, 50, 640, 400, (1e-8, 1e-4), (1e-7, 3e-4), xlabel=HLAB, ylabel=QINV)
    ax.line(hs, lr, COLORS[0], 2.4, "", "Lifshitz\u2013Roukes, Eq. (45)")
    ax.line(hs, zn, COLORS[1], 2.0, "8,4", "Zener, Eq. (46)")
    sel = list(range(0, 400, 20))
    ax.markers([hs[i] for i in sel], [present[i] for i in sel], COLORS[2], "o", 5, "Present, delay law with \u03c4\u2080 = k* = 0")
    save(svg_doc(800, 510, ax.render("lr")), os.path.join(OUT, "Figure_2_Validation.png"), 800, 510)
    table = []
    for h in (1e-7, 5e-7, 1e-6, 1.6e-6, 2e-6, 5e-6, 1e-5, 5e-5):
        r = solve(SI, h)
        x = h * math.sqrt(r["omega0"] / (2 * chi))
        table.append(dict(h=h, f0=r["omega0"] / (2 * math.pi), present=r["Qinv"], lr=dE * lr_closed_form(x),
                          zener=zener(SI, h, r["omega0"])))
    RES["validation"] = table


# ---------------------------------------------------------------------------
# Figure 3: comparison of heat conduction laws (two panels)
# ---------------------------------------------------------------------------
MODELS = [
    ("Fourier (classical)", "Fourier", {}),
    ("LS, \u03c4 = 10 ps", "LS", dict(tau=TAU0)),
    ("GN-III, k* = 10\u00b9\u2070", "GN-III", dict(kstar=KSTAR)),
    ("DPL, \u03c4q = 10, \u03c4\u03b8 = 5 ps", "DPL", dict(tauq=TAU0, taut=TAU0 / 2)),
    ("MGT, \u03c4 = 10 ps, k* = 10\u00b9\u2070", "MGT", dict(tau=TAU0, kstar=KSTAR)),
    ("Delay, \u03c4\u2080 = 10 ps, k* = 10\u00b9\u2070", "Delay", dict(tau0=TAU0, kstar=KSTAR)),
]


def fig3():
    W, Hh = 1500, 560
    a1 = Axes(110, 50, 600, 400, (1e-9, 1e-4), (1e-8, 5e-4), xlabel=HLAB, ylabel=QINV, title="(a) Inverse quality factor")
    a2 = Axes(860, 50, 600, 400, (1e-9, 1e-4), (0.0, 2.5), ylog=False, xlabel=HLAB,
              ylabel=QINV + " / " + QINV + "(Fourier)", title="(b) Ratio to the Fourier prediction")
    base = qcurve(SI, "Fourier")
    order = [0, 1, 2, 3, 4, 5]
    widths = [3.0, 2.0, 2.0, 2.0, 2.0, 2.6]
    for i in order:
        lab, mdl, p = MODELS[i]
        q = qcurve(SI, mdl, **p)
        a1.line(H, q, COLORS[i], widths[i], DASHES[i], lab)
        a2.line(H, [qq / bb for qq, bb in zip(q, base)], COLORS[i], widths[i], DASHES[i])
    a2.hline(1.0, "#999", "2,2")
    save(svg_doc(W, Hh, a1.render("lr") + a2.render()), os.path.join(OUT, "Figure_3_Model_Comparison.png"), W, Hh)
    RES["model_peaks"] = []
    for lab, mdl, p in MODELS:
        hc, qm = pk(SI, mdl, **p)
        RES["model_peaks"].append(dict(model=lab, hc=hc, qmax=qm,
                                       q10nm=solve(SI, 1e-8, mdl, **p)["Qinv"],
                                       q100nm=solve(SI, 1e-7, mdl, **p)["Qinv"],
                                       q10um=solve(SI, 1e-5, mdl, **p)["Qinv"]))


# ---------------------------------------------------------------------------
# Figure 4: effect of the conductivity rate k*
# ---------------------------------------------------------------------------
KS_LIST = [0.0, 1e9, 3e9, 1e10, 3e10, 1e11]


def fig4():
    ax = Axes(110, 50, 640, 420, (1e-9, 1e-4), (1e-8, 5e-4), xlabel=HLAB, ylabel=QINV)
    rows = []
    for i, ks in enumerate(KS_LIST):
        q = qcurve(SI, "Delay", tau0=TAU0, kstar=ks)
        lab = "k* = 0 (Fourier)" if ks == 0 else "k* = %s W m\u207b\u00b9K\u207b\u00b9s\u207b\u00b9" % _sci(ks)
        ax.line(H, q, COLORS[i], 2.4 if i == 0 else 2.0, DASHES[i], lab)
        hc, qm = pk(SI, "Delay", tau0=TAU0, kstar=ks)
        rows.append(dict(kstar=ks, hc=hc, qmax=qm, Qmin=1 / qm,
                         G_at_hc=(ks / (SI["k"] * omega0(SI, hc))) if ks else 0.0))
    ax.text(1.5e-9, 2.5e-4, "Si, clamped\u2013clamped, L/h = 10, \u03c4\u2080 = 10 ps", 13)
    save(svg_doc(800, 530, ax.render("lr")), os.path.join(OUT, "Figure_4_Effect_of_kstar.png"), 800, 530)
    RES["kstar_effect"] = rows


def _sci(v):
    e = int(math.floor(math.log10(v)))
    m = v / 10 ** e
    sup = str(e).translate(str.maketrans("-0123456789", "\u207b\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079"))
    return ("10" + sup) if abs(m - 1) < 1e-9 else ("%g\u00d710%s" % (m, sup))


# ---------------------------------------------------------------------------
# Figure 5: effect of tau0 in the nanoscale regime + thin-beam asymptote
# ---------------------------------------------------------------------------
TAU_LIST = [1e-12, 1e-11, 5e-11, 1e-10]
KS5 = 1e11


def thin_ratio(m, h, tau0, ks, bc="CC"):
    """Eq. (55) ratio: Q^-1(delay)/Q^-1(Fourier) for |xi| << 1."""
    w = omega0(m, h, bc=bc)
    k = m["k"]
    G = ks / (k * w)
    Om = w * tau0
    a = 1 + G * Om
    bimag = G * (Om ** 2 / 2 - 1)
    return a / (a * a + bimag * bimag)


def fig5():
    ax = Axes(110, 50, 640, 420, (1e-9, 1e-6), (0.0, 1.2), ylog=False, xlabel=HLAB,
              ylabel=QINV + "(delay) / " + QINV + "(Fourier)")
    base = qcurve(SI, "Fourier")
    rows = []
    for i, t in enumerate(TAU_LIST):
        q = qcurve(SI, "Delay", tau0=t, kstar=KS5)
        ax.line(H, [a / b for a, b in zip(q, base)], COLORS[i], 2.2, DASHES[i], "\u03c4\u2080 = %g ps" % (t * 1e12))
        hm = logspace(-9, -7.3, 8)
        ax.markers(hm, [thin_ratio(SI, h, t, KS5) for h in hm], COLORS[i], "o", 4)
        for h in (1e-9, 3e-9, 1e-8, 3e-8, 1e-7):
            r = solve(SI, h, "Delay", tau0=t, kstar=KS5)
            rows.append(dict(tau0=t, h=h, Omega=r["omega0"] * t, ratio=r["Qinv"] / solve(SI, h)["Qinv"],
                             asym=thin_ratio(SI, h, t, KS5)))
    ax.markers([], [], "#000", "o", 4, "Thin-beam asymptote, Eq. (55)")
    ax.hline(1.0, "#999", "2,2")
    ax.text(1.4e-9, 1.13, "Si, clamped\u2013clamped, k* = 10\u00b9\u00b9 W m\u207b\u00b9K\u207b\u00b9s\u207b\u00b9", 13)
    save(svg_doc(800, 530, ax.render("ll")), os.path.join(OUT, "Figure_5_Effect_of_tau0.png"), 800, 530)
    RES["tau_effect"] = rows
    # the special point Omega = sqrt(2): h where omega0*tau0 = sqrt(2)
    sp = []
    for t in TAU_LIST:
        # omega0 * h = const for fixed aspect ratio -> h* = const * tau0 / sqrt(2)
        c = omega0(SI, 1e-6) * 1e-6
        hstar = c * t / math.sqrt(2)
        sp.append(dict(tau0=t, h_star=hstar, f_star=math.sqrt(2) / t / (2 * math.pi)))
    RES["neutral_point"] = sp


# ---------------------------------------------------------------------------
# Figure 6: map of log10(Q^-1 delay / Q^-1 Fourier) over (h, k*)
# ---------------------------------------------------------------------------
def fig6():
    W, Hh = 900, 560
    nx, ny = 90, 70
    hs = logspace(-9, -4, nx)
    ks = logspace(8, 12, ny)
    ax = Axes(110, 50, 620, 420, (1e-9, 1e-4), (1e8, 1e12), xlabel=HLAB,
              ylabel="Conductivity rate k* (W m\u207b\u00b9K\u207b\u00b9s\u207b\u00b9)")
    vmin, vmax = -2.0, 2.0
    for j, k in enumerate(ks):
        for i, h in enumerate(hs):
            q = solve(SI, h, "Delay", tau0=TAU0, kstar=k)["Qinv"]
            q0 = solve(SI, h)["Qinv"]
            v = max(vmin, min(vmax, math.log10(q / q0)))
            col = _cmap((v - vmin) / (vmax - vmin))
            x0 = ax.tx(hs[i] / 10 ** (2.5 / (nx - 1)))
            x1 = ax.tx(hs[i] * 10 ** (2.5 / (nx - 1)))
            y0 = ax.ty(ks[j] * 10 ** (2.0 / (ny - 1)))
            y1 = ax.ty(ks[j] / 10 ** (2.0 / (ny - 1)))
            ax.raw('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"/>' % (x0, y0, x1 - x0 + 0.4, y1 - y0 + 0.4, col))
    # predicted first thermal-wave resonance k*_1 (Eq. 54), independent of h for fixed L/h
    wh = omega0(SI, 1e-6) * 1e-6
    k1 = SI["rho"] * SI["c"] * (wh / math.pi) ** 2
    ax.hline(k1, "#000", "6,3", "k*\u2081 from Eq. (54)")
    body = ax.render()
    # colour bar
    cb = []
    for i in range(100):
        v = i / 99
        cb.append('<rect x="790" y="%.1f" width="26" height="4.4" fill="%s"/>' % (470 - 4.2 * (i + 1), _cmap(v)))
    for v in (-2, -1, 0, 1, 2):
        y = 470 - (v - vmin) / (vmax - vmin) * 420
        cb.append('<text x="824" y="%.1f" font-size="13" font-family="%s">%s</text>' % (y + 4, FONT, ("%+d" % v).replace("-", "\u2212")))
    cb.append('<text transform="translate(880,260) rotate(-90)" font-size="14" text-anchor="middle" font-family="%s">log\u2081\u2080[%s(delay)/%s(Fourier)]</text>' % (FONT, QINV, QINV))
    save(svg_doc(W, Hh, body + "\n".join(cb)), os.path.join(OUT, "Figure_6_Parameter_Map.png"), W, Hh)
    RES["k1_resonance_CC"] = k1


def _cmap(t):
    # blue (reduction) - white - red (enhancement)
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        s = t / 0.5
        r, g, b = 33 + (255 - 33) * s, 102 + (255 - 102) * s, 172 + (255 - 172) * s
    else:
        s = (t - 0.5) / 0.5
        r, g, b = 255 - (255 - 178) * s, 255 - (255 - 24) * s, 255 - (255 - 43) * s
    return "#%02x%02x%02x" % (int(r), int(g), int(b))


# ---------------------------------------------------------------------------
# Figure 7: design chart, Q_TED vs h for four materials
# ---------------------------------------------------------------------------
def fig7():
    ax = Axes(110, 50, 640, 420, (1e-9, 1e-4), (1e2, 1e11), xlabel=HLAB, ylabel="Q<tspan baseline-shift=\"sub\" font-size=\"10\">TED</tspan> = 1/" + QINV)
    rows = []
    for i, key in enumerate(["Si", "PolySi", "Au", "SiC"]):
        m = MATERIALS[key]
        qf = qcurve(m, "Fourier")
        qd = qcurve(m, "Delay", tau0=TAU0, kstar=KSTAR)
        ax.line(H, [1 / q for q in qd], COLORS[i], 2.4, "", m["name"] + " (delay)")
        ax.line(H, [1 / q for q in qf], COLORS[i], 1.5, "5,4")
        hcf, qmf = pk(m, "Fourier")
        hcd, qmd = pk(m, "Delay", tau0=TAU0, kstar=KSTAR)
        rows.append(dict(material=m["name"], key=key, dE=relaxation_strength(m), chi=diffusivity(m),
                         hc_F=hcf, Qmin_F=1 / qmf, f_F=omega0(m, hcf) / (2 * math.pi),
                         hc_D=hcd, Qmin_D=1 / qmd, f_D=omega0(m, hcd) / (2 * math.pi),
                         Q10nm_F=1 / solve(m, 1e-8)["Qinv"],
                         Q10nm_D=1 / solve(m, 1e-8, "Delay", tau0=TAU0, kstar=KSTAR)["Qinv"]))
    ax.line([], [], "#000", 1.5, "5,4", "dashed: Fourier (same colour)")
    save(svg_doc(800, 530, ax.render("ul")), os.path.join(OUT, "Figure_8_Material_Design_Chart.png"), 800, 530)
    RES["materials"] = rows


# ---------------------------------------------------------------------------
# Figure 8: boundary conditions
# ---------------------------------------------------------------------------
def fig8():
    ax = Axes(110, 50, 640, 420, (1e-9, 1e-4), (1e-8, 1e-2), xlabel=HLAB, ylabel=QINV)
    rows = []
    for i, bc in enumerate(["CC", "SS", "CF"]):
        qf = qcurve(SI, "Fourier", bc=bc)
        qd = qcurve(SI, "Delay", bc=bc, tau0=TAU0, kstar=KSTAR)
        ax.line(H, qd, COLORS[i], 2.4, "", BC_NAMES[bc] + " (delay)")
        ax.line(H, qf, COLORS[i], 1.5, "5,4")
        hcf, qmf = pk(SI, "Fourier", bc=bc)
        hcd, qmd = pk(SI, "Delay", bc=bc, tau0=TAU0, kstar=KSTAR)
        rows.append(dict(bc=BC_NAMES[bc], lam=LAMBDA1[bc], hc_F=hcf, Qmin_F=1 / qmf,
                         f_F=omega0(SI, hcf, bc=bc) / (2 * math.pi), hc_D=hcd, Qmin_D=1 / qmd,
                         f_D=omega0(SI, hcd, bc=bc) / (2 * math.pi)))
    ax.line([], [], "#000", 1.5, "5,4", "dashed: Fourier (same colour)")
    save(svg_doc(800, 530, ax.render("ul")), os.path.join(OUT, "Figure_9_Boundary_Conditions.png"), 800, 530)
    RES["bcs"] = rows


# ---------------------------------------------------------------------------
# Figure 9: thermoelastic frequency shift
# ---------------------------------------------------------------------------
def fig9():
    dE = relaxation_strength(SI)
    ax = Axes(110, 50, 640, 420, (1e-9, 1e-4), (-0.7, 1.0), ylog=False, xlabel=HLAB,
              ylabel="(Re \u03c9 \u2212 \u03c9\u2080)/(\u03c9\u2080 \u0394<tspan baseline-shift=\"sub\" font-size=\"10\">E</tspan>)")
    for i, ks in enumerate([0.0, 1e9, 1e10, 1e11]):
        y = [solve(SI, h, "Delay", tau0=TAU0, kstar=ks)["shift"] / dE for h in H]
        ax.line(H, y, COLORS[i], 2.2, DASHES[i], "k* = 0 (Fourier)" if ks == 0 else "k* = %s" % _sci(ks))
    ax.hline(0.0, "#999", "2,2", "isothermal limit")
    ax.hline(0.5, "#999", "2,2", "adiabatic limit \u0394E/2")
    save(svg_doc(800, 530, ax.render("ll")), os.path.join(OUT, "Figure_10_Frequency_Shift.png"), 800, 530)


# ---------------------------------------------------------------------------
# Figure 10: thermal-wave resonance versus k* (thick beam, G >> 1)
# ---------------------------------------------------------------------------
def fig10():
    dE = relaxation_strength(SI)
    ks = logspace(8.5, 11.5, 1500)
    ax = Axes(110, 50, 640, 420, (10 ** 8.5, 10 ** 11.5), (1e-4, 1e3), xlabel="Conductivity rate k* (W m\u207b\u00b9K\u207b\u00b9s\u207b\u00b9)",
              ylabel=QINV + " / \u0394<tspan baseline-shift=\"sub\" font-size=\"10\">E</tspan>")
    rows = []
    for i, h in enumerate([1e-5, 1e-4]):
        y = [solve(SI, h, "Delay", tau0=TAU0, kstar=k)["Qinv"] / dE for k in ks]
        ax.line(ks, y, COLORS[i], 2.0, DASHES[i], "h = %g \u00b5m" % (h * 1e6))
        # numerical peak locations
        loc = [j for j in range(1, len(y) - 1) if y[j] > y[j - 1] and y[j] > y[j + 1] and y[j] > 1.0]
        rows.append(dict(h=h, peaks=[dict(kstar=ks[j], val=y[j]) for j in loc]))
    wh = omega0(SI, 1e-6) * 1e-6
    pred = []
    for n in (1, 2, 3):
        kn = SI["rho"] * SI["c"] * (wh / ((2 * n - 1) * math.pi)) ** 2
        pred.append(kn)
        ax.vline(kn, "#555", "4,3", "n = %d" % n)
    ax.hline(0.494, "#999", "2,2", "Fourier maximum 0.494")
    save(svg_doc(800, 530, ax.render("ll")), os.path.join(OUT, "Figure_7_Thermal_Wave_Resonance.png"), 800, 530)
    RES["resonance"] = dict(pred=pred, numeric=rows, omega_h=wh,
                            cT_at_k1=math.sqrt(pred[0] / (SI["rho"] * SI["c"])))


def aspect_table():
    """Table 10: effect of the aspect ratio L/h (CC silicon)."""
    rows = []
    hs = logspace(-8, -2, 1500)
    for ar in (10, 20, 50):
        qf = [solve(SI, h, aspect=ar)["Qinv"] for h in hs]
        qd = [solve(SI, h, "Delay", aspect=ar, tau0=TAU0, kstar=KSTAR)["Qinv"] for h in hs]
        hf, mf = peak(hs, qf)
        hd, md = peak(hs, qd)
        wh = omega0(SI, 1e-6, aspect=ar) * 1e-6
        rows.append(dict(aspect=ar, k1=SI["rho"] * SI["c"] * (wh / math.pi) ** 2, hc_F=hf, Qmin_F=1 / mf,
                         f_F=omega0(SI, hf, aspect=ar) / (2 * math.pi), hc_D=hd, Qmin_D=1 / md))
    RES["aspect"] = rows


def main():
    for fn in (fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, aspect_table):
        print(fn.__name__)
        fn()
    with open(os.path.join(OUT, "ted_results.json"), "w") as f:
        json.dump(RES, f, indent=1)
    print("results ->", os.path.join(OUT, "ted_results.json"))


if __name__ == "__main__":
    main()
