"""Exact Laplace-domain line-source solution for a UNIFORM medium whose properties are the copper data of the base
paper multiplied by constant ratios (P, L, k, rho, rc, g).  Derived by a Hankel transform in r (see manuscript Sec. 4.1);
for unit ratios it reduces to the solution of the base paper and of model.py."""
import cmath
import math
import mgl
from mgl import kscaled, D1, D2, EPS


def roots(s, q, tau0, tau1):
    p = 1.0 + tau1 * s
    ps = 1.0 + tau0 * s
    A = q["k"] * q["P"]
    B = q["k"] * q["rho"] * s * s / p + ps * s * (q["rc"] * q["P"] + EPS * q["g"] ** 2)
    C = ps * s ** 3 * q["rc"] * q["rho"] / p
    disc = cmath.sqrt(B * B - 4.0 * A * C)
    x1 = (B + disc) / (2 * A)
    x2 = (B - disc) / (2 * A)
    if abs(x2) > abs(x1):
        x1, x2 = x2, x1
    x2 = (C / A) / x1
    m1, m2 = cmath.sqrt(x1), cmath.sqrt(x2)
    if m1.real < 0:
        m1 = -m1
    if m2.real < 0:
        m2 = -m2
    return p, m1, m2


def fields(s, rs, q, tau0, tau1):
    p, m1, m2 = roots(s, q, tau0, tau1)
    G = D1 * q["g"] / (2.0 * math.pi * s * q["P"] * q["k"] * (m1 * m1 - m2 * m2))
    out = []
    for r in rs:
        phi = u = th = lap = 0j
        for m, sg in ((m1, 1.0), (m2, -1.0)):
            k0, k1 = kscaled(m * r)
            e = cmath.exp(-m * r)
            k0 *= e
            k1 *= e
            phi += sg * G * k0
            u += -sg * G * m * k1
            th += sg * G * (q["P"] * m * m - q["rho"] * s * s / p) / (D1 * q["g"]) * k0
            lap += sg * G * m * m * k0
        d = q["P"] - q["L"]
        srr = q["rho"] * s * s * phi - p * d * u / r
        stt = q["rho"] * s * s * phi + p * d * (u / r - lap)
        out.append((th, u, srr, stt))
    return out


def invert(t, rs, q, tau0, tau1, N=1200, nwynn=8):
    f = lambda s: fields(s, rs, q, tau0, tau1)
    return mgl.durbin(f, t, 4, len(rs), N=N, nwynn=nwynn)[0]
