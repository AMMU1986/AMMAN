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
    """Leading-order growth rate of the optical branch, Eq. (B.17):
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
    f = Figure(1000, 470, 'Fig. 2  Growth rate of the optical branch (KG, original coupling)')
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
            label='LS small-k law (B.17)')
    pa.axes()
    pb.axes()
    pa.legend('br')
    pb.legend('br')
    f.save(os.path.join(OUT, 'Figure_2_Growth_Rate_vs_k.png'))


# ---------------------------------------------------------------------------
# Fig. 3 - stability window of the energy-consistent coupling
# ---------------------------------------------------------------------------
def fig3():
    bbs = linspace(0.0, 1.6e-4, 33)
    ks = logspace(1e-1, 1e4, 90)
    f = Figure(700, 470, 'Fig. 3  Energy-consistent coupling: sup_k Re s vs b')
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
    f.save(os.path.join(OUT, 'Figure_3_Energy_Consistent_Window.png'))
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


def main():
    curves = {}
    for m in MODELS:
        curves[m] = (growth_curve(m), growth_curve(m, coup=COUP_SOURCE))
    fig1()
    fig2(curves)
    checks(curves)
    fig3()
    with open(os.path.join(OUT, 'numerical_summary.txt'), 'w') as fh:
        fh.write('\n'.join(summary) + '\n')


if __name__ == '__main__':
    main()
