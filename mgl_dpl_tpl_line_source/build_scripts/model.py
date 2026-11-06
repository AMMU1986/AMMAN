"""MGL thermoelasticity with LS / DPL / TPL heat conduction: Laplace-domain solution
for (a) a pulsed axisymmetric line source (K0 solution) and (b) a line source
translating at constant speed V (Fourier in x, Laplace in t).  Pure Python.

Unified heat-flux law in the Laplace domain (zero initial data):
    Phi(s) q = -Psi(s) grad(theta),
    Phi = 1 + tq s (+ tq^2 s^2/2 if order == 2),
    Psi = 1 + tT s + K (1 + tv s)/s   (K = 0 outside TPL).
Combined potential equation (u = grad phi):
    Lap^2 phi - B Lap phi + C phi = -d1 Q/Psi,
    B = s^2/p + (1+eps) Phi s/Psi,  C = Phi s^3/(Psi p),  p = 1 + t1 s     (MGL)
Classical pre-2013 sources (Lord-Shulman, Green-Lindsay, Tzou, Roychoudhuri,
Chandrasekharaiah) are named in prose only; add them to the reference list if the
user wants pre-2013 items.
"""
import cmath
import math
from dataclasses import dataclass, replace

import mgl
from mgl import kscaled, durbin

D1, D2, EPS, LAMBDA1, KAPPA = mgl.D1, mgl.D2, mgl.EPS, mgl.LAMBDA1, mgl.KAPPA


@dataclass(frozen=True)
class Model:
    name: str = "MGL-LS"
    t1: float = 0.05      # strain-rate / temperature-rate lag tau_1
    tq: float = 0.02      # heat-flux phase lag tau_q (tau_0 role)
    tT: float = 0.0       # temperature-gradient lag tau_T
    tv: float = 0.0       # thermal-displacement lag tau_v
    K: float = 0.0        # K* (nondimensional)
    order: int = 1        # Taylor order in tau_q
    flavor: str = "MGL"   # "MGL" or "GL"
    eps: float = EPS
    src: str = "eff"      # "eff": source enters as -Q (base-paper convention); "phys": -Phi(s) Q

    def Phi(self, s):
        if self.order == 2:
            return 1.0 + self.tq * s + 0.5 * (self.tq * s) ** 2
        return 1.0 + self.tq * s

    def Psi(self, s):
        v = 1.0 + self.tT * s
        if self.K:
            v += self.K * (1.0 + self.tv * s) / s
        return v

    def BC(self, s):
        p = 1.0 + self.t1 * s
        if self.flavor == "GL":
            return s * s + s * self.Phi(s) + self.eps * s * p, s ** 3 * self.Phi(s)
        ph, ps = self.Phi(s), self.Psi(s)
        return s * s / p + (1.0 + self.eps) * ph * s / ps, ph * s ** 3 / (ps * p)

    def roots(self, s):
        B, C = self.BC(s)
        disc = cmath.sqrt(B * B - 4.0 * C)
        x1 = (B + disc) / 2.0
        x2 = (B - disc) / 2.0
        if abs(x2) > abs(x1):
            x1, x2 = x2, x1
        x2 = C / x1
        m1, m2 = cmath.sqrt(x1), cmath.sqrt(x2)
        if m1.real < 0:
            m1 = -m1
        if m2.real < 0:
            m2 = -m2
        return m1, m2

    # per-mode temperature factor, stress factor, source prefactor
    def parts(self, s):
        p = 1.0 + self.t1 * s
        m1, m2 = self.roots(s)
        if self.flavor == "GL":
            th = [(m * m - s * s) / (D1 * p) for m in (m1, m2)]
            kp = KAPPA
            pref = D1 * p / (m1 * m1 - m2 * m2)
        else:
            th = [(m * m - s * s / p) / D1 for m in (m1, m2)]
            kp = p * KAPPA
            pref = D1 / (self.Psi(s) * (m1 * m1 - m2 * m2))
            if self.src == "phys":
                pref *= self.Phi(s)
        return (m1, m2), th, kp, pref


# ---------------------------------------------------------------- pulse profiles
def Fbar(prof, s):
    """Laplace transform of the temporal profile f(t) (peak value 1 where stated)."""
    k = prof[0]
    if k == "step":
        return 1.0 / s
    if k == "rect":          # f = H(t) - H(t - tp)
        return (1.0 - cmath.exp(-s * prof[1])) / s
    if k == "exp":           # f = exp(-t/td)
        return 1.0 / (s + 1.0 / prof[1])
    if k == "gamma":         # f = (t/tm) exp(1 - t/tm), peak 1 at t = tm
        tm = prof[1]
        return math.e * tm / (1.0 + tm * s) ** 2
    if k == "sin2":          # f = sin^2(pi t/P) = (1 - cos(2 pi t/P))/2
        w = 2.0 * math.pi / prof[1]
        return 0.5 * w * w / (s * (s * s + w * w))
    raise ValueError(k)


def ftime(prof, t):
    k = prof[0]
    if t < 0:
        return 0.0
    if k == "step":
        return 1.0
    if k == "rect":
        return 1.0 if t < prof[1] else 0.0
    if k == "exp":
        return math.exp(-t / prof[1])
    if k == "gamma":
        return t / prof[1] * math.exp(1.0 - t / prof[1])
    if k == "sin2":
        return math.sin(math.pi * t / prof[1]) ** 2
    raise ValueError(k)


# ---------------------------------------------------------------- axisymmetric fields
def line_fields(model, s, rs, prof):
    """(theta, u, srr, spp) Laplace transforms at radii rs for unit Q0."""
    (m1, m2), th, kp, pref = model.parts(s)
    ms = (m1, m2)
    G = pref * Fbar(prof, s) / (2.0 * math.pi)
    sg = (1.0, -1.0)
    out = []
    for r in rs:
        phi = u = t = lap = 0j
        for m, thj, sj in zip(ms, th, sg):
            k0, k1 = kscaled(m * r)
            e = cmath.exp(-m * r)
            k0 *= e
            k1 *= e
            phi += sj * G * k0
            u += -sj * G * m * k1
            t += sj * G * thj * k0
            lap += sj * G * m * m * k0
        srr = s * s * phi - kp * u / r
        spp = s * s * phi + kp * (u / r - lap)
        out.append((t, u, srr, spp))
    return out


def invert_line(model, prof, rs, t, N=2000, nwynn=0, ct=6.0, Tfac=2.0):
    """Durbin inversion; returns list over r of [theta, u, srr, spp]. Rect pulse by time shift."""
    if prof[0] == "rect":
        step = ("step",)
        a = invert_line(model, step, rs, t, N, nwynn, ct, Tfac)
        if t > prof[1]:
            b = invert_line(model, step, rs, t - prof[1], N, nwynn, ct, Tfac)
            return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]
        return a
    f = lambda s: line_fields(model, s, rs, prof)
    res = durbin(f, t, 4, len(rs), N=N, ct=ct, Tfac=Tfac, nwynn=nwynn)
    return res[0] if nwynn == 0 else res[0]


# ---------------------------------------------------------------- moving source
def moving_fields(model, s, xs, y, prof, V, h=0.5, xi_max=150.0):
    """(theta, ux, uy, sxx, syy, sxy) Laplace transforms at (x, y), y > 0, source at (Vt, 0).
    phi = (1/2pi) int dxi e^{i xi x} Lam(xi) [g1 - g2], g_j = e^{-a_j y}/(2 a_j)."""
    (m1, m2), th, kp, pref = model.parts(s)
    n = int(xi_max / h)
    acc = [[0j] * 6 for _ in xs]
    s2 = s * s
    for j in range(-n, n + 1):
        xi = j * h
        lam = pref * Fbar(prof, s + 1j * xi * V) if prof[0] != "step" else pref / (s + 1j * xi * V)
        a1 = cmath.sqrt(xi * xi + m1 * m1)
        a2 = cmath.sqrt(xi * xi + m2 * m2)
        g1 = cmath.exp(-a1 * y) / (2.0 * a1)
        g2 = cmath.exp(-a2 * y) / (2.0 * a2)
        c_th = lam * (th[0] * g1 - th[1] * g2)
        c_ux_core = lam * (g1 - g2)            # times i xi
        c_uy = lam * (-a1 * g1 + a2 * g2)
        c_sxx = lam * ((s2 - kp * a1 * a1) * g1 - (s2 - kp * a2 * a2) * g2)
        c_syy = lam * (s2 + kp * xi * xi) * (g1 - g2)
        c_sxy = kp * 1j * xi * c_uy
        c_ux = 1j * xi * c_ux_core
        vals = (c_th, c_ux, c_uy, c_sxx, c_syy, c_sxy)
        for ix, x in enumerate(xs):
            ph = cmath.exp(1j * xi * x)
            row = acc[ix]
            for k in range(6):
                row[k] += vals[k] * ph
    f = h / (2.0 * math.pi)
    return [tuple(v * f for v in row) for row in acc]


def invert_moving(model, prof, xs, y, t, V, N=800, nwynn=0, h=0.5, xi_max=150.0, ct=6.0, Tfac=2.0):
    f = lambda s: moving_fields(model, s, xs, y, prof, V, h, xi_max)
    res = durbin(f, t, 6, len(xs), N=N, ct=ct, Tfac=Tfac, nwynn=nwynn)
    return res[0]


# ---------------------------------------------------------------- stability scan
def poly_roots(c):
    """Roots of c[0] + c[1] s + ... by Aberth iteration on a rescaled variable (complex).
    Zero roots (vanishing low-order coefficients) are returned exactly."""
    c = list(c)
    nz = 0
    while abs(c[0]) < 1e-300:
        c.pop(0)
        nz += 1
    n = len(c) - 1
    while abs(c[n]) < 1e-300:
        n -= 1
    c = c[:n + 1]
    lam = (abs(c[0] / c[n])) ** (1.0 / n)
    a = [c[k] * lam ** k / c[n] / lam ** n for k in range(n + 1)] if False else [c[k] * lam ** k for k in range(n + 1)]
    sc = max(abs(x) for x in a)
    a = [x / sc for x in a]
    z = [cmath.exp(2j * math.pi * (k + 0.3) / n) * (1.0 + 0.1 * k) for k in range(n)]
    da = [k * a[k] for k in range(1, n + 1)]

    def ev(co, x):
        v = 0j
        for q in reversed(co):
            v = v * x + q
        return v
    for _ in range(500):
        dmax = 0.0
        for i in range(n):
            p = ev(a, z[i])
            dp = ev(da, z[i])
            if dp == 0:
                dp = 1e-30
            ratio = p / dp
            ssum = 0j
            for j in range(n):
                if j != i:
                    ssum += 1.0 / (z[i] - z[j])
            dz = ratio / (1.0 - ratio * ssum)
            z[i] -= dz
            dmax = max(dmax, abs(dz) / max(abs(z[i]), 1e-3))
        if dmax < 1e-14:
            break
    return [x * lam for x in z] + [0j] * nz


def pmul(a, b):
    r = [0.0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r


def padd(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0.0) + (b[i] if i < len(b) else 0.0) for i in range(n)]


def max_growth(model, xi):
    """Largest Re(s) of the dispersion relation  Psi' p xi^4 + (Psi' s^2 + (1+eps) Phi' s^2 p) xi^2 + Phi' s^4 = 0
    with Psi' = s Psi, Phi' = Phi (MGL flavour)."""
    p = [1.0, model.t1]
    ph = [1.0, model.tq] + ([0.5 * model.tq ** 2] if model.order == 2 else [])
    psp = [model.K, 1.0 + model.K * model.tv, model.tT]
    k2 = xi * xi
    t1 = [c * k2 * k2 for c in pmul(psp, p)]
    t2 = [c * k2 for c in padd(pmul(psp, [0, 0, 1.0]), [(1 + model.eps) * c for c in pmul(pmul(ph, [0, 0, 1.0]), p)])]
    t3 = pmul(ph, [0, 0, 0, 0, 1.0])
    poly = padd(padd(t1, t2), t3)
    z = poly_roots([complex(c) for c in poly])
    return max(x.real for x in z)


def asymptotic_exponents(model, s1=2.0e3, s2=2.0e4):
    """Log-slope d ln|m_j| / d ln s of the two roots at large real s, and large-s speed 1/lim(m/s)."""
    out = []
    ra, rb = model.roots(complex(s1)), model.roots(complex(s2))
    for a, b in zip(ra, rb):
        out.append(math.log(abs(b) / abs(a)) / math.log(s2 / s1))
    return out
