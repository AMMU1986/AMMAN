#!/usr/bin/env python3
"""
Figures and numerical tables for Paper A:
"Stop bands, evanescent regimes and amplifying pass bands of thermoelastic waves
in Klein-Gordon nonlocal solids under six non-Fourier heat conduction models".

Standard library only.  Output: kg_stopband_figures/*.png and a text summary
kg_stopband_figures/numerical_summary.txt used to fill the manuscript tables.
"""

import math
import os

from kg_thermoelastic_core import (
    MODELS, EPS1, TAU1, CS, CS2, COUP, COUP_SOURCE, TQ, TT, CT2,
    critical_freqs, elastic_k2, elastic_group_velocity, track_modes,
    wave_props, thermal_front_attenuation, wavefront_speed, phys_branch,
    logspace, linspace,
)
from kg_plot import Figure, COLORS, DASH, SHADE_P, SHADE_S, SHADE_G

OUT = '/projects/sandbox/AMMAN/kg_stopband_figures'
os.makedirs(OUT, exist_ok=True)
summary = []


def log(s=''):
    print(s)
    summary.append(s)


# ---------------------------------------------------------------------------
# Figure 1 - regime map in the (tau1, beta) plane
# ---------------------------------------------------------------------------
def fig1():
    f = Figure(900, 520, 'Fig. 1  KG regime map (eps1 = 0.01)')
    p = f.panel(90, 50, 760, 400, (0.0005, 0.025), (0, 400),
                xlabel='tau1 (non-dimensional)', ylabel='beta')
    taus = linspace(0.0005, 0.025, 760)
    om_t = [1 / t for t in taus]
    p.fill_between_x(taus, [CS / EPS1] * len(taus), om_t, SHADE_S)
    p.fill_between_x(taus, [1 / EPS1] * len(taus), om_t, SHADE_P)
    p.plot(taus, om_t, (0, 0, 0), thick=2, label='beta = 1/tau1')
    p.hline(1 / EPS1, (200, 0, 0), 'dash')
    p.hline(CS / EPS1, (30, 90, 220), 'dash')
    p.legend_items.append(('beta = c_d/eps1 = 100 (P cut-off)', (200, 0, 0), 'dash'))
    p.legend_items.append(('beta = c_s/eps1 = 49.9 (S cut-off)', (30, 90, 220), 'dash'))
    p.vline(EPS1 / 1.0, (120, 120, 120), 'dot')
    p.vline(EPS1 / CS, (120, 120, 120), 'dot')
    p.vline(TAU1, (0, 150, 60), 'solid')
    p.axes()
    p.text(0.0012, 385, 'pink: P and S stop band   blue: S stop band only', (0, 0, 0))
    p.text(0.0102, 380, 'tau1 = eps1/c_d', (90, 90, 90))
    p.text(0.0202, 380, 'tau1 = eps1/c_s', (90, 90, 90))
    p.text(0.0062, 20, 'tau1 = 0.006 (source paper)', (0, 120, 50))
    p.legend('tr')
    f.save(os.path.join(OUT, 'Figure_1_Regime_Map.png'))


# ---------------------------------------------------------------------------
# Figure 2 - purely elastic P wave: Re W and Im W
# ---------------------------------------------------------------------------
CASES = [('KG (eps1=0.01, tau1=0.006)', EPS1, TAU1, COLORS['KG'], 'solid'),
         ('Eringen (eps1=0.01, tau1=0)', EPS1, 0.0, COLORS['NE'], 'dash'),
         ('Classical', 0.0, 0.0, COLORS['C'], 'dot')]


def elastic_W(beta, c2, e1, t1):
    k2 = elastic_k2(beta, c2, e1, t1)
    if isinstance(k2, complex) and math.isinf(k2.real):
        return complex('inf')
    return phys_branch(complex(k2))


def fig_elastic(c2, name, fname, band):
    f = Figure(1000, 470, f'Fig. {name}')
    pa = f.panel(80, 50, 400, 340, (0, 400), (0, 400), xlabel='beta', ylabel='Re W')
    pb = f.panel(570, 50, 400, 340, (0, 400), (0, 120), xlabel='beta', ylabel='Im W (decay rate)')
    for p in (pa, pb):
        p.vband(band[0], band[1], SHADE_P if c2 == 1.0 else SHADE_S)
    bs = linspace(0.5, 400, 1600)
    for lab, e1, t1, col, sty in CASES:
        W = [elastic_W(b, c2, e1, t1) for b in bs]
        pa.plot(bs, [w.real if not math.isinf(w.real) else None for w in W], col, sty, label=lab)
        pb.plot(bs, [w.imag if not math.isinf(w.real) else None for w in W], col, sty, label=lab)
    pa.axes()
    pb.axes()
    pa.legend('tl')
    pb.legend('tr')
    f.save(os.path.join(OUT, fname))


# ---------------------------------------------------------------------------
# Figure 4 - phase and group velocity of elastic P wave
# ---------------------------------------------------------------------------
def fig4():
    f = Figure(1000, 470, 'Fig. 4  Elastic P wave: phase and group velocity')
    pa = f.panel(80, 50, 400, 340, (0, 600), (0, 3), xlabel='beta', ylabel='phase velocity')
    pb = f.panel(570, 50, 400, 340, (0, 600), (0, 2), xlabel='beta', ylabel='group velocity')
    for p in (pa, pb):
        p.vband(1 / EPS1, 1 / TAU1, SHADE_P)
    bs = linspace(0.5, 600, 2400)
    sets = [('KG tau1=0.006', EPS1, 0.006, COLORS['KG'], 'solid'),
            ('KG tau1=0.010 (= eps1/c_d)', EPS1, 0.010, COLORS['ORANGE'], 'dashdot'),
            ('Eringen tau1=0', EPS1, 0.0, COLORS['NE'], 'dash'),
            ('Classical', 0.0, 0.0, COLORS['C'], 'dot')]
    for lab, e1, t1, col, sty in sets:
        vp, vg = [], []
        for b in bs:
            k2 = elastic_k2(b, 1.0, e1, t1)
            if isinstance(k2, complex) or k2 <= 0:
                vp.append(None)
                vg.append(None)
            else:
                vp.append(b / math.sqrt(k2))
                vg.append(elastic_group_velocity(b, 1.0, e1, t1))
        pa.plot(bs, vp, col, sty, label=lab)
        pb.plot(bs, vg, col, sty, label=lab)
    pa.hline(EPS1 / TAU1, (120, 120, 120), 'dot')
    pb.hline(EPS1 / TAU1, (120, 120, 120), 'dot')
    pa.axes()
    pb.axes()
    pa.text(420, 1.85, 'eps1/tau1 = 1.667', (90, 90, 90))
    pa.legend('tl')
    pb.legend('br')
    f.save(os.path.join(OUT, 'Figure_4_Phase_Group_Velocity.png'))


# ---------------------------------------------------------------------------
# Thermoelastic computations
# ---------------------------------------------------------------------------
BETAS = logspace(0.05, 3000, 2500)


def compute_all(eps1=EPS1, tau1=TAU1, coup=COUP):
    res = {}
    for m in MODELS:
        m1, m2 = track_modes(m, BETAS, eps1=eps1, tau1=tau1, coup=coup)
        res[m] = (m1, m2)
    return res


def fig5(res):
    f = Figure(1000, 470, 'Fig. 6  Elastic-mode decay length and signed specific loss (KG)')
    pa = f.panel(80, 50, 400, 340, (0, 400), (1e-3, 1e5), ylog=True,
                 xlabel='beta', ylabel='decay length 1/|Im W2|')
    pb = f.panel(570, 50, 400, 340, (170, 3000), (-6, 1), xlog=True,
                 xlabel='beta (optical pass band)', ylabel='SL2 x 1000 (negative = gain)')
    pa.vband(1 / EPS1, 1 / TAU1, SHADE_P)
    for m in MODELS:
        W2 = res[m][1]
        xs, ya, xb, yb = [], [], [], []
        for b, w in zip(BETAS, W2):
            if math.isinf(w.real):
                continue
            if b <= 400:
                xs.append(b)
                ya.append(1 / abs(w.imag) if abs(w.imag) > 0 else None)
            if b >= 170:
                xb.append(b)
                yb.append(1000 * 4 * math.pi * w.imag / abs(w.real))
        pa.plot(xs, ya, COLORS[m], DASH[m], label=m)
        pb.plot(xb, yb, COLORS[m], DASH[m], label=m)
    pb.hline(0, (120, 120, 120), 'dot')
    pa.axes()
    pb.axes(xticks=[200, 500, 1000, 2000])
    pa.legend('tr')
    pb.legend('br')
    f.save(os.path.join(OUT, 'Figure_6_Elastic_Mode_Decay_and_Gain.png'))


def fig6(res, res_cl):
    f = Figure(1000, 470, 'Fig. 5  Thermal mode: phase velocity and attenuation (KG solid, classical dotted)')
    pa = f.panel(80, 50, 400, 340, (0.1, 3000), (0, 40), xlog=True, xlabel='beta', ylabel='V1')
    pb = f.panel(570, 50, 400, 340, (0.1, 3000), (0, 20), xlog=True, xlabel='beta', ylabel='Q1 = Im W1')
    for m in MODELS:
        for R, sty, lab in ((res, DASH[m], m), (res_cl, 'dot', None)):
            W1 = R[m][0]
            v = [wave_props(b, w)[0] for b, w in zip(BETAS, W1)]
            q = [w.imag for w in W1]
            pa.plot(BETAS, v, COLORS[m], sty, label=lab)
            pb.plot(BETAS, q, COLORS[m], sty, label=lab)
    for val in (1 / math.sqrt(TQ), math.sqrt(2 * TT) / TQ):
        pa.hline(val, (120, 120, 120), 'dot')
    for m in ('LS', 'MGT', 'HDPL'):
        pb.hline(thermal_front_attenuation(m), (120, 120, 120), 'dot')
    pa.axes()
    pb.axes()
    pa.legend('tl')
    pb.legend('tl')
    f.save(os.path.join(OUT, 'Figure_5_Thermal_Mode.png'))


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------
def table_values(res, label):
    log(f'\n=== {label}: (V1, Q1) thermal | (V2, Q2) elastic at selected beta ===')
    probe = [1, 10, 50, 99, 120, 160, 200, 500, 3000]
    for m in MODELS:
        row = []
        for pbeta in probe:
            i = min(range(len(BETAS)), key=lambda j: abs(BETAS[j] - pbeta))
            v1, q1, _, _ = wave_props(BETAS[i], res[m][0][i])
            v2, q2, _, _ = wave_props(BETAS[i], res[m][1][i])
            row.append(f'b={pbeta}: {v1:.4g},{q1:.4g} | {v2:.4g},{q2:.4g}')
        log(f'{m:7s} ' + ' ; '.join(row))


def perturb_imW2(model, beta, eps1=EPS1, tau1=TAU1, coup=COUP):
    """First-order (in coupling) elastic-mode attenuation, Eq. (67):
    Im W2 ~ coup k_e^3 Im q^2 / (2 S |k_e^2 - q^2|^2)."""
    from kg_thermoelastic_core import thermal_q2
    S = 1 - eps1 ** 2 * beta ** 2
    ke2 = elastic_k2(beta, 1.0, eps1, tau1)
    if isinstance(ke2, complex) or ke2 <= 0:
        return None
    ke = math.sqrt(ke2)
    q2 = thermal_q2(model, beta)
    return coup * ke ** 3 * q2.imag / (2 * S * abs(ke2 - q2) ** 2)


def fig7():
    """Parametric study in tau1 (LS heat law)."""
    f = Figure(1000, 470, 'Fig. 7  Effect of tau1 on the elastic mode (LS, eps1 = 0.01)')
    pa = f.panel(80, 50, 400, 340, (0, 400), (0, 3), xlabel='beta', ylabel='V2')
    pb = f.panel(570, 50, 400, 340, (0, 400), (1e-4, 1e3), ylog=True,
                 xlabel='beta', ylabel='abs(Im W2)')
    bs = linspace(0.5, 400, 1600)
    cols = [COLORS['GN-III'], COLORS['KG'], COLORS['ORANGE'], COLORS['GN-II']]
    log('\n=== Fig.7: LS elastic mode for several tau1 (V2, Im W2) ===')
    for t1, col in zip((0.004, 0.006, 0.008, 0.0095), cols):
        _, m2 = track_modes('LS', bs, tau1=t1)
        v = [wave_props(b, w)[0] if abs(w.real) >= abs(w.imag) else None for b, w in zip(bs, m2)]
        im = [abs(w.imag) if not math.isinf(w.real) and w.imag != 0 else None for w in m2]
        sty = 'solid'
        pa.plot(bs, v, col, sty, label=f'tau1 = {t1}  (1/tau1 = {1 / t1:.1f})')
        pb.plot(bs, im, col, sty, label=f'tau1 = {t1}')
        i = min(range(len(bs)), key=lambda j: abs(bs[j] - 300))
        log(f'tau1={t1}: at beta=300  V2={wave_props(bs[i], m2[i])[0]:.4f}  Im W2={m2[i].imag:.4e}')
    pa.hline(1.0, (120, 120, 120), 'dot')
    pa.axes()
    pb.axes()
    pa.legend('tr')
    pb.legend('tr')
    f.save(os.path.join(OUT, 'Figure_7_Tau1_Parametric.png'))


def fig8(res):
    """Validation of the asymptotic formulas against exact roots."""
    f = Figure(1000, 470, 'Fig. 8  Asymptotic formulas (lines) vs exact roots (dots)')
    pa = f.panel(80, 50, 400, 340, (0.1, 3000), (1e-6, 1), xlog=True, ylog=True,
                 xlabel='beta', ylabel='abs(Im W2), elastic mode (KG)')
    pb = f.panel(570, 50, 400, 340, (0.01, 10), (0.01, 10), xlog=True, ylog=True,
                 xlabel='beta (low frequency)', ylabel='thermal mode LS: V1 and Q1')
    log('\n=== Fig.8: perturbation formula Eq.(67) vs exact Im W2 ===')
    for m in ('LS', 'GN-III', 'HDPL'):
        W2 = res[m][1]
        xs, ex, ap = [], [], []
        for b, w in zip(BETAS, W2):
            if b < 0.1 or (1 / EPS1 * 0.97 < b < 1 / TAU1 * 1.03) or math.isinf(w.real):
                continue
            pv = perturb_imW2(m, b)
            if pv is None:
                continue
            xs.append(b)
            ex.append(abs(w.imag))
            ap.append(abs(pv))
        pa.plot(xs, ap, COLORS[m], 'solid', label=f'{m} Eq. (67)', thick=1)
        pa.plot(xs[::40], ex[::40], COLORS[m], 'dot', thick=4, label=f'{m} exact')
        for pb_ in (1, 50, 300, 3000):
            i = min(range(len(xs)), key=lambda j: abs(xs[j] - pb_))
            log(f'{m:7s} beta={xs[i]:.4g}: exact {ex[i]:.4e}  Eq.(67) {ap[i]:.4e}')
    pa.vband(1 / EPS1, 1 / TAU1, SHADE_P)
    # low-frequency thermal mode
    bl = logspace(0.01, 10, 300)
    m1, _ = track_modes('LS', bl)
    pb.plot(bl, [wave_props(b, w)[0] for b, w in zip(bl, m1)], COLORS['LS'], 'solid', label='V1 exact')
    pb.plot(bl, [w.imag for w in m1], COLORS['MGT'], 'solid', label='Q1 exact')
    pb.plot(bl, [math.sqrt(2 * b / (1 + COUP)) for b in bl], (120, 120, 120), 'dash',
            label='V1 = sqrt(2 beta/(1+eps))')
    pb.plot(bl, [math.sqrt(b * (1 + COUP) / 2) for b in bl], (200, 120, 120), 'dash',
            label='Q1 = sqrt(beta(1+eps)/2)')
    log('\n=== low-frequency LS thermal mode: exact vs Eq.(77) ===')
    for b0 in (0.01, 0.1, 1.0):
        i = min(range(len(bl)), key=lambda j: abs(bl[j] - b0))
        log(f'beta={bl[i]:.4g}: V1 {wave_props(bl[i], m1[i])[0]:.4f} vs {math.sqrt(2 * bl[i] / (1 + COUP)):.4f}; '
            f'Q1 {m1[i].imag:.4f} vs {math.sqrt(bl[i] * (1 + COUP) / 2):.4f}')
    pa.axes()
    pb.axes()
    pa.legend('bl')
    pb.legend('tl')
    f.save(os.path.join(OUT, 'Figure_8_Asymptotic_Validation.png'))


def shear_table():
    log('\n=== shear wave (V3, Im W3) ===')
    for lab, e1, t1 in (('KG', EPS1, TAU1), ('NE', EPS1, 0.0), ('C', 0.0, 0.0)):
        row = []
        for b in (10, 40, 49, 60, 120, 170, 300, 1000):
            w = elastic_W(b, CS2, e1, t1)
            v = b / w.real if abs(w.real) > 1e-9 and abs(w.real) >= abs(w.imag) else float('inf')
            row.append(f'b={b}: {v:.4g},{w.imag:.4g}')
        log(f'{lab}: ' + ' ; '.join(row))


def main():
    oe, ot = critical_freqs(1.0)
    se, st = critical_freqs(CS)
    log(f'coupling eps (alpha_t = 1.78e-5) = {COUP:.5f}; source alpha_t gives {COUP_SOURCE:.4f}')
    log(f'c_s = {CS:.5f};  P band edges: {oe:.3f}, {ot:.3f};  S band edges: {se:.3f}, {st:.3f}')
    log(f'high-frequency KG speed eps1/tau1 = {EPS1 / TAU1:.4f}')
    for m in MODELS:
        log(f'{m:7s} wavefront speed bound = {wavefront_speed(m):.4f}; '
            f'thermal-front attenuation limit = {thermal_front_attenuation(m):.4f}')
    fig1()
    fig_elastic(1.0, '2  Purely elastic P wave (gamma = 0)', 'Figure_2_Elastic_P_Wave.png', (oe, ot))
    fig_elastic(CS2, '3  Transverse (shear) wave', 'Figure_3_Shear_Wave.png', (se, st))
    fig4()
    res = compute_all()
    res_ne = compute_all(tau1=0.0)
    res_cl = compute_all(eps1=0.0, tau1=0.0)
    res_src = compute_all(coup=COUP_SOURCE)
    fig5(res)
    fig6(res, res_cl)
    fig7()
    fig8(res)
    shear_table()
    table_values(res, 'KG, physical coupling')
    table_values(res_ne, 'Eringen, physical coupling')
    table_values(res_cl, 'Classical, physical coupling')
    table_values(res_src, 'KG, source coupling 1.68')
    # minimum decay length in the stop band, and maximum gain in optical band
    log('\n=== elastic mode: min decay length in P stop band; max spatial gain above 1/tau1 ===')
    for m in MODELS:
        W2 = res[m][1]
        sb = [(1 / abs(w.imag), b) for b, w in zip(BETAS, W2)
              if oe < b < ot and not math.isinf(w.real) and w.imag != 0]
        ob = [(w.imag, b) for b, w in zip(BETAS, W2) if b > ot * 1.001 and not math.isinf(w.real)]
        mn = min(sb) if sb else (float('nan'), 0)
        mx = min(ob) if ob else (float('nan'), 0)
        log(f'{m:7s} min decay length {mn[0]:.4g} at beta {mn[1]:.4g}; '
            f'most negative Im W2 {mx[0]:.4g} at beta {mx[1]:.4g}')
    with open(os.path.join(OUT, 'numerical_summary.txt'), 'w') as fh:
        fh.write('\n'.join(summary) + '\n')


if __name__ == '__main__':
    main()
