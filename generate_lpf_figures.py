#!/usr/bin/env python3
"""
Figures and tables for the manuscript
"Thermo-mechanical response of thin metal films to femtosecond/picosecond laser
pulses using an exact single-delay thermoelastic model".

Outputs: lpf_figures/Figure_1 ... Figure_11 (.png + .svg), lpf_figures/lpf_results.json
Standard library only (plus headless Chromium for PNG rasterisation).
"""

import cmath
import json
import math
import os
import time

from lpf_model import (MATERIALS, T0, derived, solve_time, heat_time, fd_solve, ttm_solve,
                       ttm_stress, keff)
from svgplot import Axes, svg_doc, save, COLORS, DASHES, FONT, esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lpf_figures")
os.makedirs(OUT, exist_ok=True)
RES = {}
FA = 1.0          # absorbed fluence, J/m^2 (linear theory: results scale with FA)
TP = 100e-15      # 1/e half-width of the Gaussian pulse
L0 = 200e-9       # reference film thickness
GPA = 1e9
PS = 1e-12
NM = 1e-9


def logspace(a, b, n):
    return [10 ** (a + (b - a) * i / (n - 1)) for i in range(n)]


def linspace(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


def sup(e):
    return str(e).translate(str.maketrans("-0123456789", "\u207b\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079"))


# ---------------------------------------------------------------------------
# Calibration against the two-temperature model
# ---------------------------------------------------------------------------
CAL_TIMES = [1 * PS, 2 * PS, 5 * PS, 10 * PS, 20 * PS, 50 * PS]


def ttm_reference(m, L):
    xs, rl, _ = ttm_solve(m, L, FA, TP, CAL_TIMES, nx=101, dt=5e-15)
    ix = list(range(0, 101, 5))
    return [xs[i] for i in ix], [[rl[t][i] for i in ix] for t in CAL_TIMES]


def fit_error(m, L, xx, ref, tau0, ks, delta=None, cache=None):
    th = heat_time(m, L, FA, TP, CAL_TIMES, xx, tau0, ks, N=500, Tw=60 * PS, delta=delta, cache=cache)
    mx = max(max(r) for r in ref)
    s = sum((th[i][j] - ref[j][i]) ** 2 for j in range(len(CAL_TIMES)) for i in range(len(xx)))
    return math.sqrt(s / (len(CAL_TIMES) * len(xx))) / mx


def calibrate():
    out = {}
    for key in ("Au", "Cu"):
        m = MATERIALS[key]
        xx, ref = ttm_reference(m, L0)
        cache = {}
        grid_t = [10 ** (-12 + a * 0.09375) for a in range(33)]
        grid_k = [10 ** (11 + b * 0.125) for b in range(41)]
        emap = []
        best = (9.0, 0, 0)
        for t0 in grid_t:
            row = []
            for ks in grid_k:
                e = fit_error(m, L0, xx, ref, t0, ks, cache=cache)
                row.append(e)
                if e < best[0]:
                    best = (e, t0, ks)
            emap.append(row)
        # local refinement (pattern search in log space)
        e0, lt, lk = best[0], math.log10(best[1]), math.log10(best[2])
        step = 0.05
        while step > 0.002:
            improved = False
            for dt_, dk_ in ((step, 0), (-step, 0), (0, step), (0, -step)):
                e = fit_error(m, L0, xx, ref, 10 ** (lt + dt_), 10 ** (lk + dk_), cache=cache)
                if e < e0:
                    e0, lt, lk, improved = e, lt + dt_, lk + dk_, True
            if not improved:
                step /= 2
        tau0, ks = 10 ** lt, 10 ** lk
        e_four = fit_error(m, L0, xx, ref, 0.0, 0.0, cache=cache)
        de_list = [10 ** (-8 + 0.025 * i) for i in range(81)]
        ef = [(fit_error(m, L0, xx, ref, 0, 0, delta=de, cache=cache), de) for de in de_list]
        e_deff, deff = min(ef)
        rc = m["rho"] * m["c"]
        ell = tau0 * math.sqrt(ks / (2 * rc))
        out[key] = dict(tau0=tau0, kstar=ks, err=e0, err_fourier=e_four, err_deff=e_deff, deff=deff,
                        ell=ell, b=m["k"] + tau0 * ks, a=tau0 ** 2 * ks / 2, sqrt_k_over_G=math.sqrt(m["k"] / m["G"]),
                        tau_e=m["gamma_e"] * T0 / m["G"], ratio_tk=tau0 * ks / m["k"],
                        kstar_overdamp=m["k"] ** 2 * (math.pi / L0) ** 2 / (4 * rc),
                        lam_crit=2 * math.pi * m["k"] / math.sqrt(4 * rc * ks),
                        grid_t=grid_t, grid_k=grid_k, emap=emap)
        print("  calibrated", key, {k: v for k, v in out[key].items() if k not in ("grid_t", "grid_k", "emap")})
    return out


# ---------------------------------------------------------------------------
# Figure 1: schematic
# ---------------------------------------------------------------------------
def fig1():
    W, H = 960, 470
    b = ['<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">'
         '<path d="M0,0 L0,6 L9,3 z" fill="#000"/></marker>'
         '<linearGradient id="hg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e06666"/>'
         '<stop offset="0.25" stop-color="#f4cccc"/><stop offset="1" stop-color="#fff2cc"/></linearGradient></defs>']
    # laser pulse
    b.append('<text x="40" y="40" font-size="17" font-weight="bold" font-family="%s">Ultrashort pulse heating of a metal film (1-D, uniaxial strain)</text>' % FONT)
    pts = []
    for i in range(101):
        t = -3 + 6 * i / 100
        pts.append("%.1f,%.1f" % (70 + 18 * t + 54, 200 - 70 * math.exp(-t * t)))
    b.append('<polyline fill="none" stroke="#c00000" stroke-width="2.5" points="%s"/>' % " ".join(pts))
    b.append('<text x="60" y="230" font-size="14" font-family="%s">Gaussian pulse g(t)</text>' % FONT)
    b.append('<text x="60" y="250" font-size="14" font-family="%s">t\u209a = 100 fs</text>' % FONT)
    for yy in (150, 190, 230, 270, 310):
        b.append('<line x1="200" y1="%d" x2="300" y2="%d" stroke="#c00000" stroke-width="3" marker-end="url(#a)"/>' % (yy, yy))
    # film
    b.append('<rect x="310" y="110" width="330" height="240" fill="url(#hg)" stroke="#000" stroke-width="1.5"/>')
    b.append('<text x="475" y="100" font-size="15" text-anchor="middle" font-family="%s">metal film (Au, Cu), thickness L</text>' % FONT)
    b.append('<text x="318" y="370" font-size="14" font-family="%s">x = 0</text>' % FONT)
    b.append('<text x="600" y="370" font-size="14" font-family="%s">x = L</text>' % FONT)
    b.append('<text x="322" y="135" font-size="13" font-family="%s">Q = Q\u2080 exp(\u2212x/\u03b4) g(t)</text>' % FONT)
    b.append('<text x="322" y="155" font-size="13" font-family="%s">\u03b4 = 12.6\u201315.3 nm</text>' % FONT)
    # waves
    b.append('<line x1="360" y1="230" x2="470" y2="230" stroke="#1f4e79" stroke-width="2.5" marker-end="url(#a)"/>')
    b.append('<text x="380" y="220" font-size="13" fill="#1f4e79" font-family="%s">stress wave, speed c_L</text>' % FONT)
    b.append('<line x1="360" y1="290" x2="430" y2="290" stroke="#2e8b57" stroke-width="2.5" stroke-dasharray="6,3" marker-end="url(#a)"/>')
    b.append('<text x="370" y="310" font-size="13" fill="#2e8b57" font-family="%s">heat (single-delay law)</text>' % FONT)
    # rear options
    b.append('<rect x="640" y="110" width="40" height="240" fill="#d9d9d9" stroke="#000" stroke-dasharray="5,3"/>')
    b.append('<text x="690" y="200" font-size="13" font-family="%s">(a) free-standing:</text>' % FONT)
    b.append('<text x="690" y="218" font-size="13" font-family="%s">\u03c3 = 0 at x = L</text>' % FONT)
    b.append('<text x="690" y="250" font-size="13" font-family="%s">(b) rigid substrate:</text>' % FONT)
    b.append('<text x="690" y="268" font-size="13" font-family="%s">u = 0 at x = L</text>' % FONT)
    b.append('<text x="690" y="300" font-size="13" font-family="%s">both faces adiabatic</text>' % FONT)
    b.append('<text x="40" y="420" font-size="14" font-family="%s">%s</text>' % (FONT, esc(
        "Single-delay law: q,t = \u2212k*\u03b8,x \u2212 (k + \u03c4\u2080k*)\u03b8,xt \u2212 (\u03c4\u2080\u00b2/2)k*\u03b8,xtt ;  "
        "motion: \u03c1u,tt = M u,xx \u2212 \u03b2\u03b8,x")))
    b.append('<text x="40" y="445" font-size="14" font-family="%s">%s</text>' % (FONT, esc(
        "Solution: Laplace transform in t, closed form in x, Durbin numerical inversion")))
    save(svg_doc(W, H, "\n".join(b)), os.path.join(OUT, "Figure_1_Film_Schematic.png"), W, H)


# ---------------------------------------------------------------------------
# Figure 2: validation
# ---------------------------------------------------------------------------
def fig2():
    au = dict(MATERIALS["Au"])
    d = derived(au)
    # (a) Thomsen: k -> 0, uncoupled, short pulse
    au0 = dict(au)
    au0["k"] = 1e-6
    tp = 20e-15
    L = 200 * NM
    th0 = FA / (d["rc"] * au["delta"] * (1 - math.exp(-L / au["delta"])))
    c, dl, beta = d["cL"], au["delta"], d["beta"]

    def thom(x, t):
        t = t - 3 * tp
        sg = 1 if x - c * t > 0 else -1
        return beta * th0 * (-0.5 * math.exp(-x / dl) * math.exp(-c * t / dl) - 0.5 * math.exp(-abs(x - c * t) / dl) * sg)

    xs = linspace(0, 160 * NM, 161)
    ts = [5 * PS, 20 * PS, 40 * PS]
    r = solve_time(au0, L, FA, tp, ts, xs, coupled=False, N=4000, Tw=60 * PS)
    W, Hh = 1500, 560
    a1 = Axes(110, 50, 600, 400, (0, 160), (-150, 150), xlog=False, ylog=False, xlabel="Depth x (nm)",
              ylabel="Stress \u03c3 (MPa)", title="(a) Laplace solution vs Thomsen analytic solution")
    rows_a = []
    for j, t in enumerate(ts):
        a1.line([x / NM for x in xs], [thom(x, t) / 1e6 for x in xs], COLORS[j], 2.0, "", "Analytic, t = %g ps" % (t / PS))
        sel = list(range(0, 161, 8))
        a1.markers([xs[i] / NM for i in sel], [r["sigma"][i][j] / 1e6 for i in sel], COLORS[j], "o", 4)
        for xi in (20 * NM, 60 * NM, 100 * NM, 140 * NM):
            i = min(range(len(xs)), key=lambda q: abs(xs[q] - xi))
            rows_a.append(dict(t=t, x=xs[i], lap=r["sigma"][i][j], ana=thom(xs[i], t)))
    a1.markers([], [], "#000", "o", 4, "Present (Laplace + Durbin)")
    # (b) FD vs Laplace, tp = 1 ps, coupled, Fourier and delay
    tp2 = 1 * PS
    xm = [100 * NM]
    tsb = [i * 1 * PS for i in range(1, 121)]
    rL = solve_time(au, L, FA, tp2, tsb, xm, N=3000, Tw=130 * PS)
    rLd = solve_time(au, L, FA, tp2, tsb, xm, tau0=1e-11, kstar=1e13, N=3000, Tw=130 * PS)
    cr = 0.5
    dtm = cr * (L / 400) / (d["cL"] * math.sqrt(1 + d["eps"]))
    tq = [round(t / dtm) * dtm for t in tsb[4::5]]
    fth, fsg = fd_solve(au, L, FA, tp2, tq, xm, nx=401, nsub=15, courant=cr)
    fthd, fsgd = fd_solve(au, L, FA, tp2, tq, xm, tau0=1e-11, kstar=1e13, nx=401, nsub=15, courant=cr)
    a2 = Axes(860, 50, 600, 400, (0, 120), (-50, 100), xlog=False, ylog=False, xlabel="Time t (ps)",
              ylabel="Stress at x = L/2 (MPa)", title="(b) Laplace solution vs finite differences")
    a2.line([t / PS for t in tsb], [v / 1e6 for v in rL["sigma"][0]], COLORS[0], 2.0, "", "Laplace, Fourier")
    a2.line([t / PS for t in tsb], [v / 1e6 for v in rLd["sigma"][0]], COLORS[1], 2.0, "8,4", "Laplace, delay")
    a2.markers([t / PS for t in tq], [fsg[t][0] / 1e6 for t in tq], COLORS[0], "o", 4, "FD, Fourier")
    a2.markers([t / PS for t in tq], [fsgd[t][0] / 1e6 for t in tq], COLORS[1], "s", 4, "FD, delay")
    save(svg_doc(W, Hh, a1.render("lr") + a2.render("ur")), os.path.join(OUT, "Figure_2_Validation.png"), W, Hh)
    rows_b = []
    for t in (20 * PS, 40 * PS, 60 * PS, 80 * PS, 100 * PS):
        tt = min(tq, key=lambda q: abs(q - t))
        j = min(range(len(tsb)), key=lambda q: abs(tsb[q] - tt))
        rd = solve_time(au, L, FA, tp2, [tt], xm, N=3000, Tw=130 * PS)
        rdd = solve_time(au, L, FA, tp2, [tt], xm, tau0=1e-11, kstar=1e13, N=3000, Tw=130 * PS)
        rows_b.append(dict(t=tt, lapF=rd["sigma"][0][0], fdF=fsg[tt][0], lapD=rdd["sigma"][0][0], fdD=fsgd[tt][0],
                           thF=rd["theta"][0][0], fthF=fth[tt][0]))
    # energy check: late-time mean temperature
    xe = linspace(0, L, 41)
    rE = solve_time(au, L, FA, TP, [120 * PS], xe, N=2500, Tw=130 * PS, tau0=CAL["Au"]["tau0"], kstar=CAL["Au"]["kstar"])
    mean = sum(rE["theta"][i][0] for i in range(41)) / 41
    RES["validation"] = dict(thomsen=rows_a, fd=rows_b, energy=dict(mean_theta=mean, expected=FA / (d["rc"] * L)))


# ---------------------------------------------------------------------------
# Figure 3: thermal dispersion of the heat conduction laws
# ---------------------------------------------------------------------------
def fig3():
    m = MATERIALS["Au"]
    rc = m["rho"] * m["c"]
    ws = logspace(8, 15, 300)
    cal = CAL["Au"]
    laws = [("Fourier", lambda s: m["k"]),
            ("Lord\u2013Shulman, \u03c4 = 1 ps", lambda s: m["k"] / (1 + s * 1e-12)),
            ("Single delay (calibrated Au)", lambda s: keff(m, s, cal["tau0"], cal["kstar"])),
            ("Single delay, \u03c4\u2080 = 10 ps, k* = 10\u00b9\u00b3", lambda s: keff(m, s, 1e-11, 1e13))]
    W, Hh = 1500, 560
    a1 = Axes(110, 50, 600, 400, (1e8, 1e15), (1e-1, 1e7), xlabel="Angular frequency \u03c9 (rad/s)",
              ylabel="Phase speed of thermal mode (m/s)", title="(a) Phase speed \u03c9/Im m")
    a2 = Axes(860, 50, 600, 400, (1e8, 1e15), (1e-10, 1e-5), xlabel="Angular frequency \u03c9 (rad/s)",
              ylabel="Penetration depth 1/Re m (m)", title="(b) Thermal penetration depth")
    rows = []
    for i, (lab, kf) in enumerate(laws):
        vp, dp = [], []
        for w in ws:
            s = 1j * w
            mm = cmath.sqrt(s * rc / kf(s))
            if mm.real < 0:
                mm = -mm
            vp.append(w / abs(mm.imag) if abs(mm.imag) > 0 else None)
            dp.append(1 / mm.real)
        a1.line(ws, vp, COLORS[i], 2.2, DASHES[i], lab)
        a2.line(ws, dp, COLORS[i], 2.2, DASHES[i])
        for w in (1e10, 1e12, 1e13, 1e14):
            s = 1j * w
            mm = cmath.sqrt(s * rc / kf(s))
            if mm.real < 0:
                mm = -mm
            rows.append(dict(law=lab, w=w, vp=w / abs(mm.imag), depth=1 / mm.real))
    a2.hline(cal["ell"], "#666", "3,3", "\u2113 = \u03c4\u2080\u221a(k*/2\u03c1c), calibrated Au")
    a1.hline(m["k"] and math.sqrt(m["k"] / (rc * 1e-12)), "#999", "2,2", "LS limit \u221a(\u03c7/\u03c4)")
    save(svg_doc(W, Hh, a1.render("ul") + a2.render()), os.path.join(OUT, "Figure_3_Thermal_Dispersion.png"), W, Hh)
    RES["dispersion"] = rows


# ---------------------------------------------------------------------------
# Figure 4: temperature profiles and thermal front, Au
# ---------------------------------------------------------------------------
def fig4():
    m = MATERIALS["Au"]
    cal = CAL["Au"]
    L = L0
    ts = [0.5 * PS, 2 * PS, 10 * PS, 50 * PS]
    xs101, rl, _ = ttm_solve(m, L, FA, TP, ts + [i * 0.5 * PS for i in range(1, 61)], nx=101, dt=5e-15)
    xs = linspace(0, L, 101)
    thF = heat_time(m, L, FA, TP, ts, xs, N=800, Tw=60 * PS)
    thD = heat_time(m, L, FA, TP, ts, xs, cal["tau0"], cal["kstar"], N=800, Tw=60 * PS)
    W, Hh = 1500, 560
    a1 = Axes(110, 50, 600, 400, (0, 200), (0, 20), xlog=False, ylog=False, xlabel="Depth x (nm)",
              ylabel="Lattice temperature rise \u03b8 (K)", title="(a) Temperature profiles, Au, L = 200 nm")
    for j, t in enumerate(ts):
        a1.line([x / NM for x in xs], [thF[i][j] for i in range(101)], COLORS[j], 1.6, "5,4")
        a1.line([x / NM for x in xs], [thD[i][j] for i in range(101)], COLORS[j], 2.4, "", "t = %g ps" % (t / PS))
        a1.markers([xs101[i] / NM for i in range(0, 101, 10)], [rl[t][i] for i in range(0, 101, 10)], COLORS[j], "o", 4)
    a1.line([], [], "#000", 1.6, "5,4", "dashed: Fourier")
    a1.markers([], [], "#000", "o", 4, "circles: two-temperature model")
    a1.text(60, 18.5, "solid: single delay (calibrated)", 13)
    # (b) thermal front position (1% of the instantaneous surface value)
    tt = [i * 0.5 * PS for i in range(1, 61)]
    xf = linspace(0, L, 201)
    tF = heat_time(m, L, FA, TP, tt, xf, N=800, Tw=60 * PS)
    tD = heat_time(m, L, FA, TP, tt, xf, cal["tau0"], cal["kstar"], N=800, Tw=60 * PS)

    def front(prof, xg):
        mx = max(prof)
        thr = 0.1 * mx
        for i in range(len(prof) - 1, -1, -1):
            if prof[i] >= thr:
                return xg[i]
        return 0.0
    fF = [front([tF[i][j] for i in range(201)], xf) / NM for j in range(len(tt))]
    fD = [front([tD[i][j] for i in range(201)], xf) / NM for j in range(len(tt))]
    fT = [front(rl[t], xs101) / NM for t in tt]
    a2 = Axes(860, 50, 600, 400, (0, 30), (0, 210), xlog=False, ylog=False, xlabel="Time t (ps)",
              ylabel="Depth where \u03b8 = 10% of its maximum (nm)", title="(b) Position of the thermal front")
    a2.line([t / PS for t in tt], fF, COLORS[0], 2.2, "5,4", "Fourier")
    a2.line([t / PS for t in tt], fD, COLORS[1], 2.4, "", "Single delay (calibrated)")
    a2.markers([t / PS for t in tt[::3]], fT[::3], COLORS[2], "o", 4, "Two-temperature model")
    a2.line([t / PS for t in tt], [math.sqrt(m["k"] / (m["rho"] * m["c"]) * t) * 2 / NM for t in tt], "#999", 1.2, "2,2", "2\u221a(\u03c7t)")
    save(svg_doc(W, Hh, a1.render("ur") + a2.render("lr")), os.path.join(OUT, "Figure_5_Temperature_Profiles.png"), W, Hh)
    RES["front"] = dict(t=[t / PS for t in tt], F=fF, D=fD, T=fT)
    RES["profiles"] = [dict(t=t / PS, surfF=thF[0][j], surfD=thD[0][j], surfT=rl[t][0], rearF=thF[-1][j],
                            rearD=thD[-1][j], rearT=rl[t][-1]) for j, t in enumerate(ts)]


# ---------------------------------------------------------------------------
# Figure 5: calibration map
# ---------------------------------------------------------------------------
def fig5():
    W, Hh = 1500, 560
    body = ""
    for p, key in enumerate(("Au", "Cu")):
        c = CAL[key]
        x0 = 110 + 750 * p
        ax = Axes(x0, 50, 520, 400, (1e-12, 1e-9), (1e11, 1e16), xlabel="Delay time \u03c4\u2080 (s)",
                  ylabel="Conductivity rate k* (W m\u207b\u00b9K\u207b\u00b9s\u207b\u00b9)", title="(%s) %s, L = 200 nm" % ("ab"[p], MATERIALS[key]["name"]))
        gt, gk, em = c["grid_t"], c["grid_k"], c["emap"]
        dlt, dlk = 0.09375 / 2, 0.125 / 2
        for i, t0 in enumerate(gt):
            for j, ks in enumerate(gk):
                v = math.log10(em[i][j])
                col = _cmap((v + 1.7) / 1.7)
                xa, xb = ax.tx(t0 / 10 ** dlt), ax.tx(t0 * 10 ** dlt)
                ya, yb = ax.ty(ks * 10 ** dlk), ax.ty(ks / 10 ** dlk)
                ax.raw('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"/>' % (xa, ya, xb - xa + 0.5, yb - ya + 0.5, col))
        rc = MATERIALS[key]["rho"] * MATERIALS[key]["c"]
        for ell, dash in ((50 * NM, "2,3"), (c["ell"], "6,3"), (300 * NM, "2,3")):
            tsx = logspace(-12, -9, 50)
            ax.line(tsx, [2 * rc * ell ** 2 / t ** 2 for t in tsx], "#000", 1.4, dash)
        ax.text(1.3e-12, 10 ** 15.6, "dashed lines: \u2113 = 50, %.0f, 300 nm" % (c["ell"] / NM), 12)
        ax.markers([c["tau0"]], [c["kstar"]], "#ffffff", "o", 6)
        ax.markers([c["tau0"]], [c["kstar"]], "#000000", "o", 3)
        body += ax.render()
    cb = []
    for i in range(100):
        cb.append('<rect x="1410" y="%.1f" width="22" height="4.4" fill="%s"/>' % (450 - 4.0 * (i + 1), _cmap(i / 99)))
    for v in (-1.5, -1.0, -0.5, 0.0):
        y = 450 - (v + 1.7) / 1.7 * 400
        cb.append('<text x="1438" y="%.1f" font-size="12" font-family="%s">%s</text>' % (y + 4, FONT, ("%.1f" % v).replace("-", "\u2212")))
    cb.append('<text transform="translate(1490,250) rotate(-90)" font-size="13" text-anchor="middle" font-family="%s">log\u2081\u2080 (relative RMS error)</text>' % FONT)
    save(svg_doc(W, Hh, body + "\n".join(cb)), os.path.join(OUT, "Figure_4_Calibration_Map.png"), W, Hh)


def _cmap(t):
    t = max(0.0, min(1.0, t))
    stops = [(0.0, (49, 54, 149)), (0.35, (116, 173, 209)), (0.6, (254, 224, 144)), (0.8, (244, 109, 67)), (1.0, (165, 0, 38))]
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if t <= b:
            s = (t - a) / (b - a)
            return "#%02x%02x%02x" % tuple(int(ca[k] + (cb[k] - ca[k]) * s) for k in range(3))
    return "#a50026"


# ---------------------------------------------------------------------------
# Figure 6: surface temperature histories, Au and Cu
# ---------------------------------------------------------------------------
def fig6():
    W, Hh = 1500, 560
    body = ""
    tt = [0.25 * PS * i for i in range(1, 201)]
    RES["surface"] = {}
    for p, key in enumerate(("Au", "Cu")):
        m = MATERIALS[key]
        c = CAL[key]
        _, rl, re_ = ttm_solve(m, L0, FA, TP, tt, nx=101, dt=5e-15)
        xs = [0.0, L0]
        tF = heat_time(m, L0, FA, TP, tt, xs, N=900, Tw=60 * PS)
        tD = heat_time(m, L0, FA, TP, tt, xs, c["tau0"], c["kstar"], N=900, Tw=60 * PS)
        tE = heat_time(m, L0, FA, TP, tt, xs, N=900, Tw=60 * PS, delta=c["deff"])
        ax = Axes(110 + 750 * p, 50, 600, 400, (0, 50), (0, 16), xlog=False, ylog=False, xlabel="Time t (ps)",
                  ylabel="Lattice temperature rise (K)", title="(%s) %s, L = 200 nm, F\u2090 = 1 J/m\u00b2" % ("ab"[p], m["name"]))
        tps = [t / PS for t in tt]
        ax.line(tps, tF[0], COLORS[0], 1.8, "5,4", "Fourier, front x = 0")
        ax.line(tps, tE[0], COLORS[3], 1.8, "2,2", "Fourier, \u03b4_eff = %.0f nm, front" % (c["deff"] / NM))
        ax.line(tps, tD[0], COLORS[1], 2.4, "", "Single delay, front x = 0")
        ax.line(tps, tD[1], COLORS[1], 2.4, "8,3", "Single delay, rear x = L")
        ax.markers(tps[3::8], [rl[t][0] for t in tt[3::8]], COLORS[2], "o", 4, "TTM, front")
        ax.markers(tps[3::8], [rl[t][-1] for t in tt[3::8]], COLORS[2], "s", 4, "TTM, rear")
        body += ax.render("ur")
        RES["surface"][key] = dict(peak_front_F=max(tF[0]), peak_front_D=max(tD[0]), peak_front_T=max(rl[t][0] for t in tt),
                                   rear50_D=tD[1][-1], rear50_T=rl[tt[-1]][-1], rear50_F=tF[1][-1],
                                   t_rear_half_D=_t_reach(tps, tD[1], 0.5 * tD[1][-1]),
                                   t_rear_half_T=_t_reach(tps, [rl[t][-1] for t in tt], 0.5 * rl[tt[-1]][-1]),
                                   peak_Te=max(re_[t][0] for t in tt))
    save(svg_doc(W, Hh, body), os.path.join(OUT, "Figure_6_Surface_Temperatures.png"), W, Hh)


def _t_reach(ts, ys, thr):
    for t, y in zip(ts, ys):
        if y >= thr:
            return t
    return None


# ---------------------------------------------------------------------------
# Figure 7: stress histories, Au, free and rigid
# ---------------------------------------------------------------------------
def fig7():
    m = MATERIALS["Au"]
    d = derived(m)
    c = CAL["Au"]
    W, Hh = 1500, 560
    body = ""
    ts = [0.5 * PS * i for i in range(1, 301)]
    RES["stress_hist"] = {}
    for p, rear in enumerate(("free", "rigid")):
        xm = [L0 / 2]
        rF = solve_time(m, L0, FA, TP, ts, xm, rear=rear, N=3000, Tw=160 * PS)
        rD = solve_time(m, L0, FA, TP, ts, xm, rear=rear, tau0=c["tau0"], kstar=c["kstar"], N=3000, Tw=160 * PS)
        dtm = 0.5 * (L0 / 400) / (d["cL"] * math.sqrt(1 + d["eps"]))
        tq = [round(t / dtm) * dtm for t in ts[3::6]]
        tth, tsg = ttm_stress(m, L0, FA, TP, tq, xm, rear=rear, nx=401, nsub=15)
        ax = Axes(110 + 750 * p, 50, 600, 400, (0, 150), (-120, 120), xlog=False, ylog=False, xlabel="Time t (ps)",
                  ylabel="Stress at x = L/2 (MPa)", title="(%s) Au, L = 200 nm, %s rear face" % ("ab"[p], rear))
        tps = [t / PS for t in ts]
        ax.line(tps, [v / 1e6 for v in rF["sigma"][0]], COLORS[0], 1.8, "5,4", "Fourier")
        ax.line(tps, [v / 1e6 for v in rD["sigma"][0]], COLORS[1], 2.4, "", "Single delay (calibrated)")
        ax.markers([t / PS for t in tq], [tsg[t][0] / 1e6 for t in tq], COLORS[2], "o", 3.5, "TTM-driven stress")
        ax.hline(0, "#999", "2,2")
        body += ax.render("lr")
        RES["stress_hist"][rear] = dict(maxT_F=max(rF["sigma"][0]), minC_F=min(rF["sigma"][0]),
                                        maxT_D=max(rD["sigma"][0]), minC_D=min(rD["sigma"][0]),
                                        maxT_T=max(tsg[t][0] for t in tq), minC_T=min(tsg[t][0] for t in tq),
                                        rms_D_vs_T=_rms([rD["sigma"][0][ts.index(min(ts, key=lambda q: abs(q - t)))] for t in tq], [tsg[t][0] for t in tq]),
                                        rms_F_vs_T=_rms([rF["sigma"][0][ts.index(min(ts, key=lambda q: abs(q - t)))] for t in tq], [tsg[t][0] for t in tq]))
    save(svg_doc(W, Hh, body), os.path.join(OUT, "Figure_7_Stress_Histories.png"), W, Hh)


def _rms(a, b):
    mx = max(abs(v) for v in b)
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)) / len(b)) / mx


# ---------------------------------------------------------------------------
# Figure 8: x-t stress maps (Fourier vs delay), Au free film
# ---------------------------------------------------------------------------
def fig8():
    m = MATERIALS["Au"]
    c = CAL["Au"]
    nx, nt = 61, 121
    xs = linspace(0, L0, nx)
    ts = linspace(0.5 * PS, 150 * PS, nt)
    W, Hh = 1500, 560
    body = ""
    smax = 40.0
    maps = {}
    for p, (lab, par) in enumerate((("Fourier", {}), ("Single delay (calibrated)", dict(tau0=c["tau0"], kstar=c["kstar"])))):
        r = solve_time(m, L0, FA, TP, ts, xs, N=3000, Tw=160 * PS, fields=("sigma",), **par)
        maps[lab] = r["sigma"]
        ax = Axes(110 + 700 * p, 50, 560, 400, (0, 200), (0, 150), xlog=False, ylog=False, xlabel="Depth x (nm)",
                  ylabel="Time t (ps)", title="(%s) %s" % ("ab"[p], lab))
        dxp = (ax.tx(xs[1]/NM) - ax.tx(xs[0]/NM))
        dyp = (ax.ty(ts[0]/PS) - ax.ty(ts[1]/PS))
        for i in range(nx):
            for j in range(nt):
                v = r["sigma"][i][j] / 1e6
                col = _div((v + smax) / (2 * smax))
                ax.raw('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"/>'
                       % (ax.tx(xs[i] / NM) - dxp / 2, ax.ty(ts[j] / PS) - dyp / 2, dxp + 0.4, dyp + 0.4, col))
        cl = derived(m)["cL"]
        tl = [x / cl / PS for x in xs]
        ax.line([x / NM for x in xs], tl, "#000", 1.0, "4,3")
        ax.line([x / NM for x in xs], [2 * L0 / cl / PS - t for t in tl], "#000", 1.0, "4,3")
        ax.line([x / NM for x in xs], [2 * L0 / cl / PS + t for t in tl], "#000", 1.0, "4,3")
        body += ax.render()
    cb = []
    for i in range(100):
        cb.append('<rect x="1410" y="%.1f" width="22" height="4.4" fill="%s"/>' % (450 - 4.0 * (i + 1), _div(i / 99)))
    for v in (-40, -20, 0, 20, 40):
        y = 450 - (v + smax) / (2 * smax) * 400
        cb.append('<text x="1438" y="%.1f" font-size="12" font-family="%s">%s</text>' % (y + 4, FONT, str(v).replace("-", "\u2212")))
    cb.append('<text transform="translate(1490,250) rotate(-90)" font-size="13" text-anchor="middle" font-family="%s">Stress \u03c3 (MPa); tension &gt; 0</text>' % FONT)
    save(svg_doc(W, Hh, body + "\n".join(cb)), os.path.join(OUT, "Figure_8_Stress_Maps.png"), W, Hh)
    # location of max tension
    loc = {}
    for lab, sg in maps.items():
        best = max(((sg[i][j], i, j) for i in range(nx) for j in range(nt)))
        worst = min(((sg[i][j], i, j) for i in range(nx) for j in range(nt)))
        loc[lab] = dict(maxT=best[0], x_maxT=xs[best[1]], t_maxT=ts[best[2]], minC=worst[0], x_minC=xs[worst[1]], t_minC=ts[worst[2]])
    RES["maps"] = loc


def _div(t):
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        s = t / 0.5
        return "#%02x%02x%02x" % (int(33 + 222 * s), int(102 + 153 * s), int(172 + 83 * s))
    s = (t - 0.5) / 0.5
    return "#%02x%02x%02x" % (int(255 - 77 * s), int(255 - 231 * s), int(255 - 212 * s))


# ---------------------------------------------------------------------------
# Figure 9: peak tensile stress and threshold fluence vs thickness
# ---------------------------------------------------------------------------
def peak_stress(m, L, tp=TP, rear="free", **par):
    """Peak tension over three acoustic transits (searched over the rear 40% of the
    film, where the reflected tensile pulse forms; 0.5 ps / 2.5 nm sampling, N = 2500,
    converged to <0.5%) and peak front-surface temperature."""
    d = derived(m)
    tmax = 3.0 * L / d["cL"] + 10 * PS
    nt = int(tmax / (0.5 * PS))
    ts = linspace(tmax / nt, tmax, nt)
    nx = int(round(0.4 * L / (2.5 * NM))) + 1
    xs = linspace(0.6 * L, L, nx)
    r = solve_time(m, L, FA, tp, ts, xs, rear=rear, N=2500, Tw=tmax * 1.05, fields=("sigma",), **par)
    best = max((r["sigma"][i][j], xs[i], ts[j]) for i in range(nx) for j in range(nt))
    tth = linspace(0.05 * PS, 20 * PS, 400)
    th = heat_time(m, L, FA, tp, tth, [0.0], N=1500, Tw=25 * PS, **{k: v for k, v in par.items()})
    return best[0], best[1], max(th[0])


def fig9():
    Ls = [50 * NM, 100 * NM, 200 * NM, 400 * NM]
    W, Hh = 1500, 560
    a1 = Axes(110, 50, 600, 400, (40, 500), (1, 300), xlabel="Film thickness L (nm)",
              ylabel="Peak tensile stress per J/m\u00b2 (MPa)", title="(a) Peak tension, free-standing film")
    a2 = Axes(860, 50, 600, 400, (40, 500), (1, 1000), xlabel="Film thickness L (nm)",
              ylabel="Absorbed fluence (J/m\u00b2)", title="(b) Thresholds: tension = 1 GPa and melting")
    rows = []
    for p, key in enumerate(("Au", "Cu")):
        m = MATERIALS[key]
        c = CAL[key]
        pF, pD, mF, mD = [], [], [], []
        for L in Ls:
            tF, xF, thF = peak_stress(m, L)
            tD, xD, thD = peak_stress(m, L, tau0=c["tau0"], kstar=c["kstar"])
            pF.append(tF / 1e6)
            pD.append(tD / 1e6)
            mF.append((m["Tm"] - T0) / thF)
            mD.append((m["Tm"] - T0) / thD)
            rows.append(dict(mat=key, L=L, maxT_F=tF, maxT_D=tD, x_F=xF, x_D=xD, thmax_F=thF, thmax_D=thD,
                             Fspall_F=GPA / tF, Fspall_D=GPA / tD, Fmelt_F=(m["Tm"] - T0) / thF, Fmelt_D=(m["Tm"] - T0) / thD))
            print("   peak", key, L, tF, tD)
        Lnm = [L / NM for L in Ls]
        a1.line(Lnm, pF, COLORS[2 * p], 1.8, "5,4", "%s, Fourier" % key)
        a1.line(Lnm, pD, COLORS[2 * p], 2.4, "", "%s, single delay" % key)
        a1.markers(Lnm, pD, COLORS[2 * p], "o", 4)
        a2.line(Lnm, [1e3 / v for v in pF], COLORS[2 * p], 1.8, "5,4", "%s spall (1 GPa), Fourier" % key)
        a2.line(Lnm, [1e3 / v for v in pD], COLORS[2 * p], 2.4, "", "%s spall (1 GPa), delay" % key)
        a2.line(Lnm, mF, COLORS[2 * p + 1], 1.8, "5,4", "%s melting, Fourier" % key)
        a2.line(Lnm, mD, COLORS[2 * p + 1], 2.4, "", "%s melting, delay" % key)
    # TTM points for 200 nm
    for p, key in enumerate(("Au", "Cu")):
        m = MATERIALS[key]
        d = derived(m)
        tmax = 3.0 * L0 / d["cL"] + 10 * PS
        dtm = 0.5 * (L0 / 400) / (d["cL"] * math.sqrt(1 + d["eps"]))
        tq = [round(t / dtm) * dtm for t in linspace(tmax / 160, tmax, 160)]
        xs = linspace(0, L0, 41)
        _, tsg = ttm_stress(m, L0, FA, TP, tq, xs, nx=401, nsub=15)
        mxT = max(max(tsg[t]) for t in tq)
        a1.markers([200], [mxT / 1e6], COLORS[2 * p], "s", 6, "%s, TTM-driven (200 nm)" % key)
        RES.setdefault("ttm_peak", {})[key] = mxT
    save(svg_doc(W, Hh, a1.render("ur") + a2.render("lr", 1)), os.path.join(OUT, "Figure_9_Peak_Stress_Thresholds.png"), W, Hh)
    RES["thickness"] = rows


# ---------------------------------------------------------------------------
# Figure 10: effect of tau0 (fixed k*) and of pulse duration
# ---------------------------------------------------------------------------
def fig10():
    m = MATERIALS["Au"]
    c = CAL["Au"]
    W, Hh = 1500, 560
    taus = logspace(-12, -9, 7)
    a1 = Axes(110, 50, 600, 400, (1e-12, 1e-9), (0, 160), ylog=False, xlabel="Delay time \u03c4\u2080 (s)",
              ylabel="Peak tensile stress (MPa)", title="(a) Effect of \u03c4\u2080 (Au, 200 nm, k* fixed)")
    rows_t = []
    pt, pk = [], []
    rc = m["rho"] * m["c"]
    for t0 in taus:
        tT, xT, th = peak_stress(m, L0, tau0=t0, kstar=c["kstar"])
        pt.append(tT / 1e6)
        rows_t.append(dict(tau0=t0, maxT=tT, x=xT, thmax=th, ell=t0 * math.sqrt(c["kstar"] / (2 * rc))))
    for t0 in taus:
        ks = 2 * rc * c["ell"] ** 2 / t0 ** 2
        tT, xT, th = peak_stress(m, L0, tau0=t0, kstar=ks)
        pk.append(tT / 1e6)
        rows_t.append(dict(tau0=t0, kstar=ks, maxT=tT, x=xT, thmax=th, ell=c["ell"], fixed_ell=True))
    tF, xF, thF = peak_stress(m, L0)
    a1.line(taus, pt, COLORS[1], 2.4, "", "single delay, k* fixed")
    a1.markers(taus, pt, COLORS[1], "o", 4)
    a1.line(taus, pk, COLORS[2], 2.4, "8,3", "single delay, \u2113 fixed (k* \u221d \u03c4\u2080\u207b\u00b2)")
    a1.markers(taus, pk, COLORS[2], "s", 4)
    a1.hline(tF / 1e6, COLORS[0], "2,2", "Fourier")
    a1.vline(c["tau0"], "#666", "4,3", "calibrated")
    tps = [10e-15, 100e-15, 1e-12, 3e-12, 10e-12, 30e-12]
    a2 = Axes(860, 50, 600, 400, (1e-14, 3e-11), (0, 160), ylog=False, xlabel="Pulse half-width t\u209a (s)",
              ylabel="Peak tensile stress (MPa)", title="(b) Effect of pulse duration (Au, 200 nm)")
    rows_p = []
    pF, pD = [], []
    for tp in tps:
        tF2, _, thF2 = peak_stress(m, L0, tp=tp)
        tD2, _, thD2 = peak_stress(m, L0, tp=tp, tau0=c["tau0"], kstar=c["kstar"])
        pF.append(tF2 / 1e6)
        pD.append(tD2 / 1e6)
        rows_p.append(dict(tp=tp, maxT_F=tF2, maxT_D=tD2, thF=thF2, thD=thD2))
    a2.line(tps, pF, COLORS[0], 2.0, "5,4", "Fourier")
    a2.line(tps, pD, COLORS[1], 2.4, "", "Single delay (calibrated)")
    a2.markers(tps, pF, COLORS[0], "o", 4)
    a2.markers(tps, pD, COLORS[1], "s", 4)
    d = derived(m)
    a2.vline(m["delta"] / d["cL"], "#666", "4,3", "\u03b4/c_L")
    save(svg_doc(W, Hh, a1.render("ur") + a2.render("ur")), os.path.join(OUT, "Figure_10_Tau0_and_Pulse_Duration.png"), W, Hh)
    RES["tau_sweep"] = rows_t
    RES["tp_sweep"] = rows_p
    RES["fourier_peak_200"] = dict(maxT=tF, x=xF, thmax=thF)


# ---------------------------------------------------------------------------
# Figure 11: rear-surface displacement (measurable)
# ---------------------------------------------------------------------------
def fig11():
    W, Hh = 1500, 560
    body = ""
    RES["rear_disp"] = {}
    ts = [0.5 * PS * i for i in range(1, 301)]
    for p, key in enumerate(("Au", "Cu")):
        m = MATERIALS[key]
        c = CAL[key]
        xs = [L0]
        rF = solve_time(m, L0, FA, TP, ts, xs, N=3000, Tw=160 * PS)
        rD = solve_time(m, L0, FA, TP, ts, xs, N=3000, Tw=160 * PS, tau0=c["tau0"], kstar=c["kstar"])
        r2 = solve_time(m, L0, FA, TP, ts, xs, N=3000, Tw=160 * PS, tau0=c["tau0"] / 3, kstar=c["kstar"] * 9)
        ax = Axes(110 + 750 * p, 50, 600, 400, (0, 150), (-1, 12), xlog=False, ylog=False, xlabel="Time t (ps)",
                  ylabel="Rear-surface displacement u(L,t) (pm)", title="(%s) %s, L = 200 nm, free film" % ("ab"[p], m["name"]))
        tp_ = [t / PS for t in ts]
        ax.line(tp_, [v * 1e12 for v in rF["u"][0]], COLORS[0], 1.8, "5,4", "Fourier")
        ax.line(tp_, [v * 1e12 for v in rD["u"][0]], COLORS[1], 2.4, "", "Single delay (calibrated)")
        ax.line(tp_, [v * 1e12 for v in r2["u"][0]], COLORS[3], 1.8, "2,2", "same \u2113, \u03c4\u2080/3 and 9k*")
        cl = derived(m)["cL"]
        ax.vline(L0 / cl / PS, "#666", "4,3", "L/c_L")
        ax.vline(3 * L0 / cl / PS, "#666", "4,3", "3L/c_L")
        body += ax.render("lr")
        RES["rear_disp"][key] = dict(jumpF=_jump(ts, rF["u"][0], L0 / cl), jumpD=_jump(ts, rD["u"][0], L0 / cl),
                                     jump2=_jump(ts, r2["u"][0], L0 / cl), finalF=rF["u"][0][-1], finalD=rD["u"][0][-1],
                                     final2=r2["u"][0][-1], pre_arrival_D=_at(ts, rD["u"][0], 0.8 * L0 / cl),
                                     pre_arrival_F=_at(ts, rF["u"][0], 0.8 * L0 / cl))
    save(svg_doc(W, Hh, body), os.path.join(OUT, "Figure_11_Rear_Displacement.png"), W, Hh)


def _jump(ts, u, ta):
    i0 = min(range(len(ts)), key=lambda i: abs(ts[i] - 0.9 * ta))
    i1 = min(range(len(ts)), key=lambda i: abs(ts[i] - 1.25 * ta))
    return u[i1] - u[i0]


def _at(ts, u, t):
    return u[min(range(len(ts)), key=lambda i: abs(ts[i] - t))]


# ---------------------------------------------------------------------------
# Transferability: calibrated on 200 nm, tested on 100 nm and 500 nm films
# ---------------------------------------------------------------------------
def transfer():
    rows = []
    for key in ("Au", "Cu"):
        m = MATERIALS[key]
        c = CAL[key]
        for L in (100 * NM, 200 * NM, 500 * NM):
            xx, ref = ttm_reference(m, L)
            cache = {}
            rows.append(dict(mat=key, L=L, err_D=fit_error(m, L, xx, ref, c["tau0"], c["kstar"], cache=cache),
                             err_F=fit_error(m, L, xx, ref, 0, 0, cache=cache),
                             err_E=fit_error(m, L, xx, ref, 0, 0, delta=c["deff"], cache=cache)))
            print("   transfer", rows[-1])
    RES["transfer"] = rows


def main(argv):
    """Stages: 'cal' (calibration, cached in lpf_figures/calibration.json) and any of
    fig1 ... fig11, transfer. With no arguments everything is run."""
    global CAL
    t0 = time.time()
    calf = os.path.join(OUT, "calibration.json")
    resf = os.path.join(OUT, "lpf_results.json")
    stages = argv or ["cal", "fig1", "fig2", "fig3", "fig4", "fig5", "fig6", "fig7", "fig8", "fig9", "fig10", "fig11", "transfer"]
    if "cal" in stages or not os.path.exists(calf):
        print("calibration ...", flush=True)
        CAL = calibrate()
        with open(calf, "w") as f:
            json.dump(CAL, f)
    else:
        CAL = json.load(open(calf))
    if os.path.exists(resf):
        RES.update(json.load(open(resf)))
    RES["calibration"] = {k: {kk: vv for kk, vv in v.items() if kk not in ("grid_t", "grid_k", "emap")} for k, v in CAL.items()}
    for name in stages:
        if name == "cal":
            continue
        print(name, "%.0f s" % (time.time() - t0), flush=True)
        globals()[name]()
        mats = {}
        for key, m in MATERIALS.items():
            mats[key] = dict(m, **derived(m))
        RES["materials"] = mats
        with open(resf, "w") as f:
            json.dump(RES, f, indent=1)
    print("done %.0f s" % (time.time() - t0), flush=True)


CAL = {}
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
