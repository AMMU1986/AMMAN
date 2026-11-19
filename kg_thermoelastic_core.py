#!/usr/bin/env python3
"""
Shared numerical core for the two Klein-Gordon (KG) nonlocal thermoelasticity
manuscripts:

  Paper A  - Stop bands, evanescent regimes and wavefront limits
  Paper B  - Energy, stability and domain of influence

Standard library only (cmath / math), so it runs in the sandbox without numpy.

Non-dimensional model (copper data of Mondal & Mukhopadhyay 2026 / Jangid et al.
2021).  Unit of speed  V = sqrt((lambda+2mu)/rho)  (so c_d = 1); unit of
frequency  w* = rho c V^2 / k_ref  with k_ref = k of copper.  The SAME scaling is
used for every heat model, including GN-II (where the model sets k = 0); this
avoids the k-based length l = k/(rho c V) that degenerates for GN-II.

Displacement (P part, potential phi):
    grad^2 phi - (1 - eps1^2 grad^2 + tau1^2 d_t^2) phi_tt = Theta
Shear potential psi:
    c_s^2 grad^2 psi - (1 - eps1^2 grad^2 + tau1^2 d_t^2) psi_tt = 0
Unified heat equation, written with polynomials a(s), b(s) in s = d/dt:
    a(s) grad^2 Theta = b(s) (Theta + coup * grad^2 phi)

    model    a(s)                 b(s)
    CTE      kap                  s
    LS       kap                  s (1 + tq s)
    GN-II    CT2                  s^2
    GN-III   CT2 + kap s          s^2
    MGT      CT2 + kap s          s^2 (1 + tq s)
    DPL-1    kap (1 + tT s)       s (1 + tq s)
    HDPL     kap (1 + tT s)       s (1 + tq s + tq^2 s^2 / 2)
"""

import cmath
import math

# ----------------------------------------------------------------------------
# Material data (SI) - copper, as used by Mondal & Mukhopadhyay (2026)
# ----------------------------------------------------------------------------
RHO = 8954.0
C_E = 383.1
K_TH = 386.0
K_STAR = 5930.38e10
LAM = 7.76e10
MU = 3.86e10
ALPHA_T = 1.78e-5          # physical copper value (K^-1)
ALPHA_T_SOURCE = 1.78e-4   # value printed in Mondal & Mukhopadhyay (2026)
T0 = 293.0

GAMMA = ALPHA_T * (3 * LAM + 2 * MU)
GAMMA_SOURCE = ALPHA_T_SOURCE * (3 * LAM + 2 * MU)
V_REF = math.sqrt((LAM + 2 * MU) / RHO)
OMEGA_STAR = RHO * C_E * V_REF ** 2 / K_TH          # 1/s
L_STAR = V_REF / OMEGA_STAR                           # m

CS2 = MU / (LAM + 2 * MU)                             # (c_s / c_d)^2
CS = math.sqrt(CS2)
COUP = GAMMA ** 2 * T0 / (RHO * C_E * (LAM + 2 * MU))  # thermoelastic coupling
COUP_SOURCE = GAMMA_SOURCE ** 2 * T0 / (RHO * C_E * (LAM + 2 * MU))
CT2 = K_STAR / (RHO * C_E * V_REF ** 2)               # GN thermal speed^2
KAP = 1.0                                             # k / k_ref

# Non-dimensional relaxation / nonlocal parameters (same as the source paper)
TQ = 0.01
TT = 0.015
EPS1 = 0.01
TAU1 = 0.006

MODELS = ['LS', 'GN-II', 'GN-III', 'DPL-1', 'HDPL', 'MGT']


# ----------------------------------------------------------------------------
# Polynomial helpers (coefficients in ASCENDING powers)
# ----------------------------------------------------------------------------
def padd(p, q):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0)
            for i in range(n)]


def pmul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return r


def pscale(p, c):
    return [c * a for a in p]


def peval(p, x):
    v = 0
    for a in reversed(p):
        v = v * x + a
    return v


def heat_polys(model, tq=TQ, tT=TT, kap=KAP, ct2=CT2):
    """Return (a, b) as ascending coefficient lists in s = d/dt."""
    if model == 'CTE':
        return [kap], [0, 1]
    if model == 'LS':
        return [kap], [0, 1, tq]
    if model == 'GN-II':
        return [ct2], [0, 0, 1]
    if model == 'GN-III':
        return [ct2, kap], [0, 0, 1]
    if model == 'MGT':
        return [ct2, kap], [0, 0, 1, tq]
    if model == 'DPL-1':
        return [kap, kap * tT], [0, 1, tq]
    if model == 'HDPL':
        return [kap, kap * tT], [0, 1, tq, tq * tq / 2]
    raise ValueError(model)


# ----------------------------------------------------------------------------
# (A) Real frequency beta, complex wavenumber W   (Paper A)
# ----------------------------------------------------------------------------
def thermal_q2(model, beta, **kw):
    """Uncoupled thermal wavenumber^2 q^2 = -b(s)/a(s), s = -i beta."""
    a, b = heat_polys(model, **kw)
    s = -1j * beta
    return -peval(b, s) / peval(a, s)


def sqrt_branch(x):
    """sqrt with Im >= 0 (decay along +x for exp(i(Wx - beta t)));
    if purely real, choose Re >= 0."""
    w = cmath.sqrt(x)
    if w.imag < 0 or (abs(w.imag) < 1e-300 and w.real < 0):
        w = -w
    return w


def elastic_k2(beta, c2=1.0, eps1=EPS1, tau1=TAU1):
    """Purely elastic KG wavenumber^2:  beta^2 (1 - tau1^2 beta^2)/(c^2 - eps1^2 beta^2)."""
    den = c2 - eps1 ** 2 * beta ** 2
    if den == 0:
        return complex('inf')
    return beta ** 2 * (1 - tau1 ** 2 * beta ** 2) / den


def coupled_roots(model, beta, eps1=EPS1, tau1=TAU1, coup=COUP, **kw):
    """Roots X = W^2 of  s X^2 - (beta^2 r + q^2 (s + coup)) X + q^2 beta^2 r = 0,
    s = 1 - eps1^2 beta^2, r = 1 - tau1^2 beta^2   (c_d = 1)."""
    q2 = thermal_q2(model, beta, **kw)
    s = 1 - eps1 ** 2 * beta ** 2
    r = 1 - tau1 ** 2 * beta ** 2
    A = s
    B = -(beta ** 2 * r + q2 * (s + coup))
    C = q2 * beta ** 2 * r
    if abs(A) < 1e-14:
        return [complex('inf'), -C / B]
    d = cmath.sqrt(B * B - 4 * A * C)
    x1 = (-B + d) / (2 * A)
    x2 = (-B - d) / (2 * A)
    # numerically stable small root
    if abs(x1) > abs(x2):
        x2 = C / (A * x1)
    else:
        x1 = C / (A * x2)
    return [x1, x2]


def phys_branch(x):
    """Physical square root of X = W^2 for a wave launched into x > 0.
    Pass band (|Re W| >= |Im W|): choose Re W > 0 (energy travels to +x for
    every branch considered here, whose group velocity is positive); the sign of
    Im W is then free - Im W < 0 means spatial AMPLIFICATION.
    Stop band (|Im W| > |Re W|): choose Im W > 0 (evanescent decay)."""
    if cmath.isinf(x):
        return complex('inf')
    w = cmath.sqrt(x)
    if abs(w.real) >= abs(w.imag):
        return w if w.real > 0 else -w
    return w if w.imag > 0 else -w


def track_modes(model, betas, **kw):
    """Continuation of the two longitudinal modes across a frequency grid.
    Identification is made at the HIGHEST frequency, where KG/Eringen
    nonlocality decouples the fields (effective coupling coup/s -> 0):
    mode 1 ('thermal') is the root closest to the uncoupled thermal q^2, mode 2
    ('elastic') the other one; ties (classical GN-II, where q^2 = k_e^2) are
    broken by calling the faster root thermal.  The labels are then carried
    down in frequency by minimum-relative-distance continuation.
    Returns lists of complex W for mode 1 and mode 2 (see phys_branch)."""
    order = sorted(range(len(betas)), key=lambda i: -betas[i])
    prev = None
    out = {}

    def rd(u, v):
        if cmath.isinf(u) or cmath.isinf(v):
            return 1e30
        return abs(u - v) / (abs(v) + 1e-30)

    for i in order:
        b = betas[i]
        x = coupled_roots(model, b, **kw)
        if prev is None:
            q2 = thermal_q2(model, b, **{k: v for k, v in kw.items()
                                          if k in ('tq', 'tT', 'kap', 'ct2')})
            d0, d1 = rd(x[0], q2), rd(x[1], q2)
            if abs(d0 - d1) < 1e-9 * (d0 + d1 + 1e-30):
                x = sorted(x, key=lambda z: abs(z))      # faster = thermal
            elif d1 < d0:
                x = [x[1], x[0]]
        else:
            keep = rd(x[0], prev[0]) + rd(x[1], prev[1])
            swap = rd(x[1], prev[0]) + rd(x[0], prev[1])
            if swap < keep:
                x = [x[1], x[0]]
        prev = x
        out[i] = (phys_branch(x[0]), phys_branch(x[1]))
    m1 = [out[i][0] for i in range(len(betas))]
    m2 = [out[i][1] for i in range(len(betas))]
    return m1, m2


def wave_props(beta, W):
    """Phase velocity, attenuation Im W (negative = amplification), signed
    specific loss 4 pi Im W/|Re W|, and decay/growth length 1/|Im W|."""
    if cmath.isinf(W) or W == 0:
        return float('nan'), float('nan'), float('nan'), float('nan')
    re, im = W.real, W.imag
    v = beta / re if re > 1e-12 else float('inf')
    sl = 4 * math.pi * im / abs(re) if abs(re) > 1e-12 else float('inf')
    pen = 1 / abs(im) if abs(im) > 1e-300 else float('inf')
    return v, im, sl, pen


# ----------------------------------------------------------------------------
# KG elastic critical frequencies and group velocity (Paper A, Section 3)
# ----------------------------------------------------------------------------
def critical_freqs(c=1.0, eps1=EPS1, tau1=TAU1):
    om_e = c / eps1 if eps1 > 0 else float('inf')
    om_t = 1 / tau1 if tau1 > 0 else float('inf')
    return om_e, om_t


def elastic_group_velocity(beta, c=1.0, eps1=EPS1, tau1=TAU1):
    """Group velocity d beta/dk on a propagating branch of
    F = k^2 (c^2 - eps1^2 beta^2) - beta^2 (1 - tau1^2 beta^2) = 0."""
    k2 = elastic_k2(beta, c * c, eps1, tau1)
    if isinstance(k2, complex) or k2 <= 0:
        return float('nan')
    k = math.sqrt(k2)
    Fk = 2 * k * (c * c - eps1 ** 2 * beta ** 2)
    Fb = -2 * eps1 ** 2 * beta * k2 - 2 * beta + 4 * tau1 ** 2 * beta ** 3
    return -Fk / Fb


# ----------------------------------------------------------------------------
# (B) Real wavenumber k, complex temporal root s = -i omega   (Paper B)
# ----------------------------------------------------------------------------
def p_dispersion_poly(model, k, eps1=EPS1, tau1=TAU1, coup=COUP, taud=0.0, eta=0.0, **kw):
    """Ascending coefficients in s of
        D(s) = (b + k^2 a) E - coup k^2 b,
        E(s) = -k^2 - s^2 (1 + eps1^2 k^2) - taud s^3 - tau1^2 s^4   (c_d = 1).
    taud > 0 adds a first-order damping term to the KG operator,
    1 - eps1^2 grad^2 + taud d_t + tau1^2 d_t^2 (shown in Paper B to DEstabilise).
    eta > 0 adds Kelvin-Voigt viscosity to the local elastic stress,
    L sigma = (1 + eta d_t) C:e - gamma Theta I  (shown in Paper B to stabilise),
    which replaces -k^2 by -k^2 (1 + eta s) in E.
    Solutions grow like exp(s t); stability <=> Re s <= 0.
    model may also be 'ELASTIC' (gamma = 0)."""
    k2 = k * k
    E = [-k2, -eta * k2, -(1 + eps1 ** 2 * k2), -taud, -tau1 ** 2]
    while len(E) > 1 and E[-1] == 0:
        E.pop()
    if model == 'ELASTIC':
        return E
    a, b = heat_polys(model, **kw)
    D = padd(pmul(padd(b, pscale(a, k2)), E), pscale(b, -coup * k2))
    while len(D) > 1 and abs(D[-1]) == 0:
        D.pop()
    return D


def s_dispersion_poly(k, c2=CS2, eps1=EPS1, tau1=TAU1, taud=0.0, eta=0.0):
    """Uncoupled KG wave (shear if c2 = c_s^2):
    tau1^2 s^4 + taud s^3 + (1+eps1^2 k^2) s^2 + eta c2 k^2 s + c2 k^2."""
    k2 = k * k
    p = [c2 * k2, eta * c2 * k2, 1 + eps1 ** 2 * k2, taud, tau1 ** 2]
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def poly_roots(coeffs, iters=500):
    """All complex roots of a polynomial (ascending coefficients), Aberth-Ehrlich
    iteration followed by Newton polishing.  Standard library only."""
    c = [complex(x) for x in coeffs]
    while len(c) > 1 and c[-1] == 0:
        c.pop()
    # strip zero roots
    nzero = 0
    while len(c) > 1 and c[0] == 0:
        c.pop(0)
        nzero += 1
    n = len(c) - 1
    if n == 0:
        return [0j] * nzero
    orig = list(c)
    lead = c[-1]
    c = [x / lead for x in c]
    # Fujiwara bound -> rescale variable z = R * w so that roots lie in |w| <= 1
    R = 2 * max(abs(c[n - j]) ** (1.0 / j) for j in range(1, n + 1))
    if R <= 0:
        R = 1.0
    c = [c[j] * R ** j for j in range(n + 1)]
    c = [x / c[-1] for x in c]
    # initial guesses: Newton-polygon-like spread over magnitudes
    mags = []
    for j in range(n):
        # crude magnitude estimate from |c_j|^(1/(n-j))
        mags.append(max(abs(c[j]) ** (1.0 / (n - j)), 1e-12))
    mags.sort()
    z = [mags[j] * cmath.exp(1j * (2 * math.pi * j / n + 0.4)) for j in range(n)]
    dc = [j * c[j] for j in range(1, n + 1)]
    for _ in range(iters):
        maxstep = 0
        for i in range(n):
            pv = peval(c, z[i])
            dv = peval(dc, z[i])
            if pv == 0:
                continue
            ratio = pv / dv if dv != 0 else 1e-3
            ssum = sum(1 / (z[i] - z[j]) for j in range(n) if j != i and z[i] != z[j])
            w = ratio / (1 - ratio * ssum)
            z[i] -= w
            maxstep = max(maxstep, abs(w) / (abs(z[i]) + 1e-300))
        if maxstep < 1e-15:
            break
    # Newton polish on the scaled polynomial
    for i in range(n):
        for _ in range(5):
            dv = peval(dc, z[i])
            if dv == 0:
                break
            z[i] -= peval(c, z[i]) / dv
    return [R * w for w in z] + [0j] * nzero


def backward_error(coeffs, z):
    """Relative backward error |p(z)| / sum |c_j| |z|^j."""
    num = abs(peval(coeffs, z))
    den = sum(abs(a) * abs(z) ** j for j, a in enumerate(coeffs))
    return num / den if den else 0.0


def max_growth(coeffs):
    """max Re s over all roots (positive => exponential instability)."""
    return max(r.real for r in poly_roots(coeffs))


def elastic_instability_band(c=1.0, eps1=EPS1, tau1=TAU1):
    """Real wavenumber band (k_lo, k_hi) in which the KG wave equation
    tau1^2 s^4 + (1 + eps1^2 k^2) s^2 + c^2 k^2 = 0 has complex s^2,
    i.e. exponentially growing solutions.  Exists iff tau1 c > eps1.
    Returns None if stable."""
    if tau1 * c <= eps1:
        return None
    # D(X) = eps1^4 X^2 + (2 eps1^2 - 4 tau1^2 c^2) X + 1 < 0, X = k^2
    A = eps1 ** 4
    B = 2 * eps1 ** 2 - 4 * tau1 ** 2 * c ** 2
    disc = B * B - 4 * A
    if A == 0:
        return (1 / math.sqrt(-B), float('inf'))
    X1 = (-B - math.sqrt(disc)) / (2 * A)
    X2 = (-B + math.sqrt(disc)) / (2 * A)
    return (math.sqrt(X1), math.sqrt(X2))


def wavefront_speed(model, eps1=EPS1, tau1=TAU1, tq=TQ, tT=TT, kap=KAP, ct2=CT2):
    """Upper bound of the domain-of-influence speed from the principal part
    (Garding).  Returns inf if the principal part is not hyperbolic."""
    if tau1 > 0:
        v_el = eps1 / tau1
    elif eps1 > 0:
        return float('inf')            # Eringen differential model
    else:
        v_el = 1.0                     # classical: c_d = 1
    v_th = {
        'LS': 1 / math.sqrt(tq),
        'MGT': math.sqrt(kap / tq),
        'GN-II': math.sqrt(ct2),
        'HDPL': math.sqrt(2 * kap * tT) / tq,
        'GN-III': float('inf'),
        'DPL-1': float('inf'),
        'CTE': float('inf'),
    }[model]
    return max(v_el, v_th)


def thermal_front_attenuation(model, tq=TQ, tT=TT, kap=KAP, ct2=CT2):
    """High-frequency limit of Im q for the uncoupled thermal wavenumber
    (exact limit of the thermal-mode attenuation under KG/Eringen nonlocality,
    where the effective coupling coup/s -> 0)."""
    if model == 'LS':
        return 1 / (2 * math.sqrt(tq * kap))
    if model == 'MGT':
        return (1 - tq * ct2 / kap) / (2 * math.sqrt(tq * kap))
    if model == 'HDPL':
        return (1 - tq / (2 * tT)) / math.sqrt(2 * kap * tT)
    if model == 'GN-II':
        return 0.0
    return float('inf')


def logspace(a, b, n):
    la, lb = math.log10(a), math.log10(b)
    return [10 ** (la + (lb - la) * i / (n - 1)) for i in range(n)]


def linspace(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


if __name__ == '__main__':
    print(f'V_ref = {V_REF:.2f} m/s, omega* = {OMEGA_STAR:.4e} 1/s, l* = {L_STAR:.4e} m')
    print(f'c_s = {CS:.5f}, coupling eps = {COUP:.5f} (source alpha_t gives {COUP_SOURCE:.4f}), C_T^2 = {CT2:.5f}')
    for c, name in [(1.0, 'P'), (CS, 'S')]:
        oe, ot = critical_freqs(c)
        print(f'{name}: Omega_eps = {oe:.3f}, Omega_tau = {ot:.3f}, '
              f'high-f speed eps1/tau1 = {EPS1 / TAU1:.4f}')
    for m in MODELS:
        print(f'{m:7s} front speed = {wavefront_speed(m):.4f}   '
              f'front attenuation = {thermal_front_attenuation(m):.4f}')
