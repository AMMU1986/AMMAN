#!/usr/bin/env python3
"""
Thermoelastic damping (TED) of Euler-Bernoulli micro/nano-beam resonators
under Quintanilla's exact single-delay heat conduction model and the
classical/generalized models it is compared with.

Pure standard library (cmath/math). All models are cast in the unified
"effective complex conductivity" form k_eff(omega), so that the
Lifshitz-Roukes type solution applies to every model:

    xi^2 = -i * omega * rho * c * h^2 / k_eff(omega)
    f(xi) = 24/xi^3 * (xi/2 - tan(xi/2))
    omega = omega0 * sqrt(1 + Delta_E * (1 + f(xi)))
    Q^-1  = 2 |Im omega| / Re omega
"""

import cmath
import math

# ---------------------------------------------------------------------------
# Material data at T0 = 300 K (representative room-temperature values)
# E [Pa], rho [kg/m^3], alpha [1/K], k [W/(m K)], c [J/(kg K)]
# ---------------------------------------------------------------------------
T0 = 300.0
MATERIALS = {
    "Si":     dict(name="Silicon (single crystal)", E=169e9, rho=2330.0, alpha=2.59e-6, k=148.0, c=712.0),
    "PolySi": dict(name="Polysilicon",               E=160e9, rho=2320.0, alpha=2.60e-6, k=34.0,  c=712.0),
    "Au":     dict(name="Gold",                      E=79e9,  rho=19300.0, alpha=14.2e-6, k=317.0, c=129.0),
    "SiC":    dict(name="Silicon carbide (3C)",      E=440e9, rho=3210.0, alpha=3.0e-6,  k=320.0, c=690.0),
}

# First-mode eigenvalues lambda_1 = beta_1 * L
LAMBDA1 = {"CC": 4.730040745, "SS": math.pi, "CF": 1.875104069}
BC_NAMES = {"CC": "Clamped-clamped", "SS": "Simply supported", "CF": "Cantilever (clamped-free)"}


def relaxation_strength(m):
    """Delta_E = E alpha^2 T0 / (rho c)."""
    return m["E"] * m["alpha"] ** 2 * T0 / (m["rho"] * m["c"])


def diffusivity(m):
    return m["k"] / (m["rho"] * m["c"])


def omega0(m, h, aspect=10.0, bc="CC"):
    """Isothermal first natural frequency of a rectangular beam, L = aspect*h."""
    L = aspect * h
    lam = LAMBDA1[bc]
    # EI/(rho A) = E h^2 / (12 rho) for a rectangular section
    return lam ** 2 / L ** 2 * math.sqrt(m["E"] * h ** 2 / (12.0 * m["rho"]))


# ---------------------------------------------------------------------------
# Effective complex conductivity of each heat conduction law
#   all laws written for harmonic fields ~ exp(i omega t)
# ---------------------------------------------------------------------------
def keff_fourier(k, w, **p):
    return complex(k, 0.0)


def keff_ls(k, w, tau=0.0, **p):          # q + tau dq/dt = -k grad(theta)
    return k / (1.0 + 1j * w * tau)


def keff_gn3(k, w, kstar=0.0, **p):       # q = -k grad(theta) - k* grad(upsilon)
    return k - 1j * kstar / w


def keff_dpl(k, w, tauq=0.0, taut=0.0, **p):  # q + tq dq/dt = -k (1 + tt d/dt) grad(theta)
    return k * (1.0 + 1j * w * taut) / (1.0 + 1j * w * tauq)


def keff_mgt(k, w, tau=0.0, kstar=0.0, **p):  # q + tau dq/dt = -k grad(theta) - k* grad(upsilon)
    return (k - 1j * kstar / w) / (1.0 + 1j * w * tau)


def keff_delay(k, w, tau0=0.0, kstar=0.0, **p):
    """Quintanilla single-delay law:
    dq/dt = -k* grad(theta) - (k + tau0 k*) grad(dtheta/dt) - (tau0^2/2) k* grad(d2theta/dt2)
    => k_eff = k + tau0 k* + i k* (omega tau0^2 / 2 - 1/omega)
    """
    return k + tau0 * kstar + 1j * kstar * (w * tau0 ** 2 / 2.0 - 1.0 / w)


KEFF = {
    "Fourier": keff_fourier,
    "LS": keff_ls,
    "GN-III": keff_gn3,
    "DPL": keff_dpl,
    "MGT": keff_mgt,
    "Delay": keff_delay,
}


# ---------------------------------------------------------------------------
# Lifshitz-Roukes type solution
# ---------------------------------------------------------------------------
def f_of_xi(xi):
    """f(xi) = 24/xi^3 (xi/2 - tan(xi/2)), with series for small |xi|."""
    if abs(xi) < 1e-3:
        return -1.0 - xi ** 2 / 10.0 - 17.0 * xi ** 4 / 1680.0
    x = xi / 2.0
    # For large |Im x| tan -> +-i ; cmath.tan handles this, but guard overflow
    if abs(x.imag) > 300:
        t = 1j if x.imag > 0 else -1j
    else:
        t = cmath.tan(x)
    return 24.0 / xi ** 3 * (x - t)


def solve(m, h, model="Fourier", aspect=10.0, bc="CC", **params):
    """Return dict with omega0, complex omega, Q^-1, relative frequency shift, xi."""
    w0 = omega0(m, h, aspect, bc)
    k_eff = KEFF[model](m["k"], w0, **params)
    xi2 = -1j * w0 * m["rho"] * m["c"] * h ** 2 / k_eff
    xi = cmath.sqrt(xi2)
    # choose the root with non-negative real part (f is even in xi anyway)
    if xi.real < 0:
        xi = -xi
    f = f_of_xi(xi)
    dE = relaxation_strength(m)
    w = w0 * cmath.sqrt(1.0 + dE * (1.0 + f))
    Qinv = 2.0 * abs(w.imag) / w.real
    return dict(omega0=w0, omega=w, Qinv=Qinv, shift=w.real / w0 - 1.0,
                xi=xi, f=f, keff=k_eff, imag_sign=(1 if w.imag >= 0 else -1))


def lr_closed_form(xi_real):
    """Lifshitz-Roukes exact Fourier result, Q^-1/Delta_E, xi = h sqrt(omega/(2 chi))."""
    x = xi_real
    return 6.0 / x ** 2 - 6.0 / x ** 3 * (math.sinh(x) + math.sin(x)) / (math.cosh(x) + math.cos(x))


def zener(m, h, w):
    tz = h ** 2 / (math.pi ** 2 * diffusivity(m))
    return relaxation_strength(m) * w * tz / (1.0 + (w * tz) ** 2)


def logspace(a, b, n):
    return [10 ** (a + (b - a) * i / (n - 1)) for i in range(n)]


def peak(hs, vals):
    i = max(range(len(vals)), key=lambda j: vals[j])
    # parabolic refinement in log(h)
    if 0 < i < len(vals) - 1:
        x0, x1, x2 = (math.log10(hs[i - 1]), math.log10(hs[i]), math.log10(hs[i + 1]))
        y0, y1, y2 = vals[i - 1], vals[i], vals[i + 1]
        den = (y0 - 2 * y1 + y2)
        if den != 0:
            dx = 0.5 * (y0 - y2) / den * (x1 - x0)
            return 10 ** (x1 + dx), y1
    return hs[i], vals[i]


if __name__ == "__main__":
    si = MATERIALS["Si"]
    print("Delta_E Si =", relaxation_strength(si))
    for h in (1e-8, 1e-7, 1e-6, 1e-5):
        r = solve(si, h)
        print(h, r["omega0"], r["Qinv"], r["shift"])
