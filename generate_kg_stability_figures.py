#!/usr/bin/env python3
"""
Figures and numerical tables for Paper B:
"Energy, dissipation-induced instability and domain of influence in
Klein-Gordon nonlocal thermoelasticity: a unified analysis of six non-Fourier
heat conduction models".

Standard library only.  Output: kg_stability_figures/*.png and
kg_stability_figures/numerical_summary.txt.
"""

import math
import os

from kg_thermoelastic_core import (
    MODELS, EPS1, TAU1, CS, CS2, COUP, COUP_SOURCE, TQ, TT, CT2, KAP,
    OMEGA_STAR, heat_polys, peval, pmul, padd, pscale,
    p_dispersion_poly, s_dispersion_poly, poly_roots, max_growth,
    backward_error, elastic_instability_band, wavefront_speed, logspace,
    linspace,
)
from kg_plot import Figure, COLORS, DASH, SHADE_P, SHADE_G

OUT = '/projects/sandbox/AMMAN/kg_stability_figures'
os.makedirs(OUT, exist_ok=True)
summary = []
DISSIPATIVE = ['LS', 'GN-III', 'DPL-1', 'HDPL', 'MGT']


def log(s=''):
    print(s)
    summary.append(s)


def small_k_growth(model, k, coup=COUP, tau1=TAU1):
    """Leading-order growth rate of the optical branch, Eq. (47):
    Re s = -(coup k^4 tau1 / 2) Im[a(i/tau1) / b(i/tau1)]."""
    a, b = heat_polys(model)
    s0 = 1j / tau1
    return -(coup * k ** 4 * tau1 / 2) * (peval(a, s0) / peval(b, s0)).imag


def modified_poly(model, k, bb, coup=COUP):
    """Energy-consistent coupling: heat equation sees div(u_t + bb u_ttt)."""
    a, b = heat_polys(model)
    k2 = k * k
    E = [-k2, 0, -(1 + EPS1 ** 2 * k2), 0, -TAU1 ** 2]
    cpl = pmul(b, [1, 0, bb])
    return padd(pmul(padd(b, pscale(a, k2)), E), pscale(cpl, -coup * k2))


# ---------------------------------------------------------------------------
# Fig. 1 - elastic KG: temporal spectrum and tau1 c > eps1 instability
# ---------------------------------------------------------------------------
def fig1():
    f = Figure(1000, 470, 'Fig. 1  Elastic KG wave: branches and growth band')
    pa = f.panel(80, 50, 400, 340, (0, 400), (0, 800),
                 xlabel='wavenumber k', ylabel='frequency |Im s|')
    pb = f.panel(570, 50, 400, 340, (0, 400), (0, 60),
                 xlabel='wavenumber k', ylabel='growth rate Re s')
    ks = linspace(0.5, 400, 800)
    ac, op = [], []
    for k in ks:
        r = sorted([abs(z.imag) for z in poly_roots(s_dispersion_poly(k, c2=1.0))])
        ac.append(r[0])
        op.append(r[-1])
    pa.plot(ks, ac, COLORS['KG'], 'solid', label='acoustic branch (P, tau1=0.006)')
    pa.plot(ks, op, COLORS['ORANGE'], 'solid', label='optical branch (P, tau1=0.006)')
    pa.plot(ks, [k for k in ks], (0, 0, 0), 'dot', label='classical, |s| = k')
    pa.plot(ks, [EPS1 / TAU1 * k for k in ks], (120, 120, 120), 'dash',
            label='slope eps1/tau1 = 1.667')
    pa.hline(1 / TAU1, (120, 120, 120), 'dot')
    pa.hline(1 / EPS1, (200, 0, 0), 'dot')
    for t1, col in ((0.012, COLORS['GN-III']), (0.015, COLORS['HDPL']), (0.020, COLORS['LS'])):
        g = [max(0.0, max_growth(s_dispersion_poly(k, c2=1.0, tau1=t1))) for k in ks]
        pb.plot(ks, g, col, 'solid', label=f'tau1 = {t1}')
        band = elastic_instability_band(1.0, EPS1, t1)
        if band:
            pb.vline(band[0], col, 'dot')
            if band[1] < 400:
                pb.vline(band[1], col, 'dot')
    pa.axes()
    pb.axes()
    pa.legend('tl')
    pb.legend('tr')
    f.save(os.path.join(OUT, 'Figure_1_Elastic_Spectrum_and_Growth_Band.png'))


# ---------------------------------------------------------------------------
# Fig. 2 - thermoelastic growth rate vs k, original coupling
# ---------------------------------------------------------------------------
KS = logspace(1e-2, 1e5, 260)


def growth_curve(model, **kw):
    return [max_growth(p_dispersion_poly(model, k, **kw)) for k in KS]


def fig2(curves):
    f = Figure(1000, 470, 'Fig. 4  Growth rate of the optical branch (KG, original coupling)')
    pa = f.panel(80, 50, 400, 340, (1e-2, 1e5), (1e-14, 1), xlog=True, ylog=True,
                 xlabel='wavenumber k', ylabel='max Re s (physical coupling 0.0168)')
    pb = f.panel(570, 50, 400, 340, (1e-2, 1e5), (1e-12, 100), xlog=True, ylog=True,
                 xlabel='wavenumber k', ylabel='max Re s (source coupling 1.68)')
    for m in DISSIPATIVE + ['GN-II']:
        g, gs = curves[m]
        pa.plot(KS, [x if x > 1e-14 else None for x in g], COLORS[m], DASH[m], label=m)
        pb.plot(KS, [x if x > 1e-12 else None for x in gs], COLORS[m], DASH[m], label=m)
    # small-k asymptote for LS
    kk = [k for k in KS if k < 3]
    pa.plot(kk, [small_k_growth('LS', k) for k in kk], (120, 120, 120), 'dot',
            label='LS small-k law, Eq. (47)')
    pa.axes()
    pb.axes()
    pa.legend('br')
    pb.legend('br')
    f.save(os.path.join(OUT, 'Figure_4_Growth_Rate_vs_k.png'))


# ---------------------------------------------------------------------------
# Fig. 3 - stability window of the energy-consistent coupling
# ---------------------------------------------------------------------------
def fig3():
    bbs = linspace(0.0, 1.6e-4, 33)
    ks = logspace(1e-1, 1e4, 90)
    f = Figure(700, 470, 'Fig. 5  Energy-consistent coupling: sup_k Re s vs b')
    p = f.panel(90, 50, 560, 340, (0, 1.6e-4), (1e-15, 1), ylog=True,
                xlabel='b', ylabel='sup over k of Re s (floor 1e-15)')
    p.vband(TAU1 ** 2, EPS1 ** 2, SHADE_G)
    rows = {}
    for m in ('LS', 'GN-III', 'DPL-1', 'HDPL', 'MGT'):
        g = []
        for bb in bbs:
            v = max(max_growth(modified_poly(m, k, bb)) for k in ks)
            g.append(max(v, 1e-15))
        rows[m] = g
        p.plot(bbs, g, COLORS[m], DASH[m], label=m)
    p.vline(TAU1 ** 2, (0, 0, 0), 'dot')
    p.vline(EPS1 ** 2, (0, 0, 0), 'dot')
    p.axes(xticks=[0, 3.6e-5, 1e-4, 1.6e-4])
    p.text(4.0e-5, 0.1, 'stable window tau1^2 <= b <= eps1^2/c_d^2', (0, 0, 0))
    p.legend('tr')
    f.save(os.path.join(OUT, 'Figure_5_Energy_Consistent_Window.png'))
    log('\n=== Fig.3 data: sup_k Re s for energy-consistent coupling ===')
    for m, g in rows.items():
        log(f'{m:7s} ' + ' '.join(f'{bb:.1e}:{v:.1e}' for bb, v in zip(bbs, g)))


# ---------------------------------------------------------------------------
# Numerical checks for the tables
# ---------------------------------------------------------------------------
def checks(curves):
    log(f'coupling (alpha_t=1.78e-5) = {COUP:.5f}; source = {COUP_SOURCE:.4f}; '
        f'omega* = {OMEGA_STAR:.4e} 1/s')
    log('\n=== Table 2: small-k growth law vs numerics (optical branch) ===')
    for m in MODELS:
        a, b = heat_polys(m)
        s0 = 1j / TAU1
        im = (peval(a, s0) / peval(b, s0)).imag
        for k in (0.05, 0.2):
            num = max(z.real for z in poly_roots(p_dispersion_poly(m, k)))
            log(f'{m:7s} Im[a/b](i/tau1) = {im:.5e}  k={k}: numeric {num:.4e}  '
                f'formula {small_k_growth(m, k):.4e}')
    log('\n=== Table 3: peak growth rate (original coupling) ===')
    for m in MODELS:
        g, gs = curves[m]
        i = max(range(len(KS)), key=lambda j: g[j])
        j = max(range(len(KS)), key=lambda j: gs[j])
        dim = g[i] * OMEGA_STAR
        efold = 1 / dim if dim > 0 else float('inf')
        log(f'{m:7s} phys: max Re s = {g[i]:.4e} at k = {KS[i]:.4g} '
            f'(= {dim:.3e} 1/s, e-folding {efold:.3e} s); '
            f'source coupling: {gs[j]:.4e} at k = {KS[j]:.4g}')
    log('\n=== Eringen (tau1 = 0) and classical: sup Re s ===')
    for m in MODELS:
        ge = max(growth_curve(m, tau1=0.0))
        gc = max(growth_curve(m, tau1=0.0, eps1=0.0))
        log(f'{m:7s} Eringen {ge:.3e}  classical {gc:.3e}')
    log('\n=== root-finder backward error (max over k, all models) ===')
    worst = 0
    for m in MODELS:
        for k in KS[::13]:
            D = p_dispersion_poly(m, k)
            worst = max(worst, max(backward_error(D, z) for z in poly_roots(D)))
    log(f'max backward error = {worst:.2e}')
    log('\n=== Table 4: wavefront speeds: Garding bound vs max |Im s|/k at k = 1e6 ===')
    for m in MODELS:
        for lab, t1 in (('KG', TAU1), ('Eringen', 0.0)):
            k = 1e6
            r = poly_roots(p_dispersion_poly(m, k, tau1=t1))
            vmax = max(abs(z.imag) for z in r) / k
            log(f'{m:7s} {lab:8s} bound {wavefront_speed(m, tau1=t1):.4f}   '
                f'numeric max|Im s|/k = {vmax:.4f}')
    log('\n=== elastic instability bands (P: c = 1, S: c = c_s) ===')
    for t1 in (0.006, 0.010, 0.012, 0.015, 0.020, 0.025):
        log(f'tau1 = {t1}: P band {elastic_instability_band(1.0, EPS1, t1)}, '
            f'S band {elastic_instability_band(CS, EPS1, t1)}')
    log('\n=== damping variants (sup over k of Re s) ===')
    ks = logspace(1e-2, 1e5, 160)
    for lab, kw in (('KG operator damping taud=1e-5', {'taud': 1e-5}),
                    ('Kelvin-Voigt eta=1e-5', {'eta': 1e-5})):
        vals = [f'{m}:{max(max_growth(p_dispersion_poly(m, k, **kw)) for k in ks):.2e}'
                for m in MODELS + ['ELASTIC']]
        log(f'{lab}: ' + ' '.join(vals))


def optical_omega(k, c2=1.0, eps1=EPS1, tau1=TAU1):
    """Frequency of the purely elastic optical branch (real, stable case)."""
    A = 1 + eps1 ** 2 * k * k
    disc = A * A - 4 * tau1 ** 2 * c2 * k * k
    return math.sqrt((A + math.sqrt(disc)) / (2 * tau1 ** 2))


def first_order_growth(model, k, coup=COUP, eps1=EPS1, tau1=TAU1):
    """Eq. (61): Re s = -coup k^4 Im q^2 / (|k^2 - q^2|^2 * 2 w dD/d(w^2)),
    evaluated on the optical branch, with q^2 = -b(-i w)/a(-i w)."""
    from kg_thermoelastic_core import thermal_q2
    w = optical_omega(k, 1.0, eps1, tau1)
    dD = (1 + eps1 ** 2 * k * k) - 2 * tau1 ** 2 * w * w
    q2 = thermal_q2(model, w)
    return -coup * k ** 4 * q2.imag / (abs(k * k - q2) ** 2 * 2 * w * dD)


def fig4(curves):
    f = Figure(1000, 470, 'Fig. 2  First-order growth law (lines) vs exact roots (dots)')
    pa = f.panel(80, 50, 400, 340, (1e-2, 1e5), (1e-14, 1), xlog=True, ylog=True,
                 xlabel='wavenumber k', ylabel='max Re s, eps = 0.0168')
    pb = f.panel(570, 50, 400, 340, (1e-1, 1e5), (0.98, 1.02), xlog=True,
                 xlabel='wavenumber k', ylabel='ratio exact / Eq. (61)')
    log('\n=== Fig.4: first-order growth law vs exact ===')
    for m in DISSIPATIVE:
        g = curves[m][0]
        fo = [first_order_growth(m, k) for k in KS]
        pa.plot(KS, [x if x > 1e-14 else None for x in fo], COLORS[m], DASH[m], thick=1, label=f'{m} Eq. (61)')
        pa.plot(KS[::12], [x if x > 1e-14 else None for x in g[::12]], COLORS[m], 'dot', thick=4)
        pb.plot(KS, [ge / fe if k >= 0.1 and fe > 1e-15 and ge > 1e-15 else None
                     for k, ge, fe in zip(KS, g, fo)],
                COLORS[m], DASH[m], label=m)
        for kk in (0.1, 1, 10, 20, 100, 1e3, 1e4):
            i = min(range(len(KS)), key=lambda j: abs(math.log(KS[j] / kk)))
            log(f'{m:7s} k={KS[i]:.4g}: exact {g[i]:.4e}  first-order {fo[i]:.4e}')
    pb.hline(1.0, (120, 120, 120), 'dot')
    pa.axes()
    pb.axes(yticks=[0.98, 0.99, 1.0, 1.01, 1.02])
    pa.legend('br')
    pb.legend('tr')
    f.save(os.path.join(OUT, 'Figure_2_First_Order_Growth_Law.png'))


def fig5():
    f = Figure(1000, 470, 'Fig. 3  Peak growth rate vs coupling constant and vs tau1')
    pa = f.panel(80, 50, 400, 340, (1e-4, 2), (1e-6, 10), xlog=True, ylog=True,
                 xlabel='coupling constant eps', ylabel='sup over k of Re s')
    pb = f.panel(570, 50, 400, 340, (1e-4, 0.0125), (1e-8, 100), xlog=True, ylog=True,
                 xlabel='tau1 (eps1 = 0.01)', ylabel='sup over k of Re s')
    ks = logspace(1e-1, 1e4, 120)
    ks_t = logspace(1e-1, 1e8, 220)
    epss = logspace(1e-4, 2, 15)
    taus = sorted(set(logspace(1e-4, 0.0125, 36) + [0.001, 5.7735e-4, 0.006, 0.0095, 0.01]))
    log('\n=== Fig.5: sup Re s vs coupling and vs tau1 ===')
    for m in ('LS', 'GN-III', 'HDPL', 'MGT', 'GN-II'):
        ge = [max(max_growth(p_dispersion_poly(m, k, coup=e)) for k in ks) for e in epss]
        gt = [max(max_growth(p_dispersion_poly(m, k, tau1=t)) for k in ks_t) for t in taus]
        pa.plot(epss, [x if x > 1e-6 else None for x in ge], COLORS[m], DASH[m], label=m)
        pb.plot(taus, [x if x > 1e-8 else None for x in gt], COLORS[m], DASH[m], label=m)
        log(f'{m:7s} vs eps: ' + ' '.join(f'{e:.1e}:{v:.2e}' for e, v in zip(epss, ge)))
        log(f'{m:7s} vs tau1: ' + ' '.join(f'{t:.4f}:{v:.2e}' for t, v in zip(taus, gt)))
    pa.vline(COUP, (120, 120, 120), 'dot')
    pa.vline(COUP_SOURCE, (120, 120, 120), 'dot')
    pb.vline(EPS1, (0, 0, 0), 'dot')
    pb.vline(TAU1, (120, 120, 120), 'dot')
    pa.axes()
    pb.vline(0.001, (200, 0, 0), 'dot')
    pb.axes(xticks=[1e-4, 1e-3, 1e-2])
    pa.legend('tl')
    pb.legend('br')
    f.save(os.path.join(OUT, 'Figure_3_Growth_vs_Coupling_and_Tau1.png'))


def main():
    curves = {}
    for m in MODELS:
        curves[m] = (growth_curve(m), growth_curve(m, coup=COUP_SOURCE))
    fig1()
    fig2(curves)
    checks(curves)
    fig3()
    fig4(curves)
    fig5()
    with open(os.path.join(OUT, 'numerical_summary.txt'), 'w') as fh:
        fh.write('\n'.join(summary) + '\n')


if __name__ == '__main__':
    main()
