#!/usr/bin/env python3
"""
Ultrashort-pulse laser heating of a thin metal film: 1-D coupled
thermoelasticity with Quintanilla's exact single-delay heat conduction law.

Standard library only (cmath / math).

Model (uniaxial strain, 0 <= x <= L, front face x = 0 irradiated):
    rho u_tt = M u_xx - beta theta_x                              (motion)
    rho c theta_t + beta T0 u_xt = -q_x + Q                       (energy)
    q_t = -k* theta_x - (k + tau0 k*) theta_xt - (tau0^2/2) k* theta_xtt  (delay law)
Laplace transform (zero initial data):
    M u'' - beta theta' = rho s^2 u
    K(s) theta'' = s rho c theta + s beta T0 u' - Q
    K(s) = k + tau0 k* + k*/s + s tau0^2 k*/2   (effective conductivity)
Source: Q(x,t) = Fa g(t) exp(-x/delta) / (delta (1 - exp(-L/delta))),
        g(t) Gaussian of 1/e half-width tp centred at t0 = 3 tp.
Boundary conditions: x = 0 traction-free, adiabatic.
                     x = L traction-free ("free") or clamped ("rigid"), adiabatic.
Inversion: Durbin's Fourier-series method with Lanczos sigma factors.
"""

import cmath
import math

T0 = 300.0

# Isotropic room-temperature data; delta = optical absorption depth at 800 nm.
MATERIALS = {
    "Au": dict(name="Gold", rho=19300.0, E=79e9, nu=0.42, alpha=14.2e-6, k=317.0, c=129.0,
               delta=15.3e-9, Tm=1337.0, gamma_e=71.0, G=2.6e16, ke0=317.0),
    "Cu": dict(name="Copper", rho=8960.0, E=130e9, nu=0.34, alpha=16.5e-6, k=401.0, c=385.0,
               delta=12.6e-9, Tm=1358.0, gamma_e=96.6, G=1.0e17, ke0=401.0),
}


def derived(m):
    E, nu = m["E"], m["nu"]
    lam = E * nu / ((1 + nu) * (1 - 2 * nu))
    mu = E / (2 * (1 + nu))
    M = lam + 2 * mu
    beta = (3 * lam + 2 * mu) * m["alpha"]
    rc = m["rho"] * m["c"]
    return dict(lam=lam, mu=mu, M=M, beta=beta, rc=rc, cL=math.sqrt(M / m["rho"]),
                chi=m["k"] / rc, eps=beta ** 2 * T0 / (rc * M))


# ---------------------------------------------------------------------------
# Source
# ---------------------------------------------------------------------------
def gauss_pulse(t, tp):
    t0 = 3.0 * tp
    return math.exp(-((t - t0) / tp) ** 2) / (math.sqrt(math.pi) * tp)


def gauss_laplace(s, tp, n=400):
    """Laplace transform of the normalised Gaussian pulse by Simpson quadrature
    on [0, 6 tp] (the pulse is < 1e-15 of its peak outside this interval)."""
    t0 = 3.0 * tp
    a, b = 0.0, 6.0 * tp
    h = (b - a) / n
    acc = 0j
    for i in range(n + 1):
        t = a + i * h
        w = 1 if i in (0, n) else (4 if i % 2 else 2)
        acc += w * math.exp(-((t - t0) / tp) ** 2) * cmath.exp(-s * t)
    return acc * h / 3.0 / (math.sqrt(math.pi) * tp)


def keff(m, s, tau0, kstar):
    return m["k"] + tau0 * kstar + kstar / s + s * tau0 ** 2 * kstar / 2.0


# ---------------------------------------------------------------------------
# Small complex linear solver
# ---------------------------------------------------------------------------
def csolve(A, b):
    n = len(b)
    A = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c]))
        A[c], A[p] = A[p], A[c]
        piv = A[c][c]
        for r in range(c + 1, n):
            f = A[r][c] / piv
            if f != 0:
                for j in range(c, n + 1):
                    A[r][j] -= f * A[c][j]
    x = [0j] * n
    for r in range(n - 1, -1, -1):
        acc = A[r][n] - sum(A[r][j] * x[j] for j in range(r + 1, n))
        x[r] = acc / A[r][r]
    return x


# ---------------------------------------------------------------------------
# Laplace-domain solution of the coupled problem
# ---------------------------------------------------------------------------
def laplace_fields(m, d, s, xs, L, Fa, tp, tau0=0.0, kstar=0.0, rear="free", coupled=True, Gs=None):
    """Return lists (theta, u, sigma) in the Laplace domain at points xs."""
    M, beta, rho, rc, delta = d["M"], d["beta"], m["rho"], d["rc"], m["delta"]
    K = keff(m, s, tau0, kstar)
    bT = beta * T0 if coupled else 0.0
    bm = beta  # stress-temperature coupling always present
    if Gs is None:
        Gs = gauss_laplace(s, tp)
    q0 = Fa * Gs / (delta * (1.0 - math.exp(-L / delta)))
    # characteristic equation M K z^2 - B z + rho^2 c s^3 = 0, z = m^2
    B = M * rc * s + K * rho * s * s + s * bm * bT
    C = rho * rc * s ** 3 * M / M  # rho * (rho c) * s^3
    disc = cmath.sqrt(B * B - 4 * M * K * C)
    z1 = (B + disc) / (2 * M * K)
    z2 = (B - disc) / (2 * M * K)
    roots = []
    for z in (z1, z2):
        r = cmath.sqrt(z)
        if r.real < 0:
            r = -r
        roots.append(r)
    # particular solution for exp(-x/delta)
    D = -1.0 / delta
    a11, a12 = M * D * D - rho * s * s, -bm * D
    a21, a22 = -s * bT * D, K * D * D - s * rc
    det = a11 * a22 - a12 * a21
    Ap = (0 * a22 - a12 * (-q0)) / det
    Bp = (a11 * (-q0) - a21 * 0) / det
    # homogeneous basis: for root r, f1 = exp(-r x) (D=-r), f2 = exp(-r (L-x)) (D=+r)
    # theta coefficient per unit u coefficient: H/(D) with H = (M r^2 - rho s^2)/beta
    basis = []
    for r in roots:
        H = (M * r * r - rho * s * s) / bm
        basis.append((r, -1, H / (-r)))   # exp(-r x)
        basis.append((r, +1, H / (r)))    # exp(-r (L - x))

    def evalf(x, kind):
        """kind: 'u','up','th','thp' -> value of each basis function at x"""
        row = []
        for r, sg, ratio in basis:
            e = cmath.exp(-r * x) if sg < 0 else cmath.exp(-r * (L - x))
            Dd = -r if sg < 0 else r
            if kind == "u":
                row.append(e)
            elif kind == "up":
                row.append(Dd * e)
            elif kind == "th":
                row.append(ratio * e)
            elif kind == "thp":
                row.append(ratio * Dd * e)
        return row

    ep0, epL = 1.0, math.exp(-L / delta)
    rows, rhs = [], []
    # sigma(0) = M u' - beta theta = 0
    ru, rt = evalf(0.0, "up"), evalf(0.0, "th")
    rows.append([M * a - bm * b for a, b in zip(ru, rt)])
    rhs.append(-(M * Ap * D * ep0 - bm * Bp * ep0))
    # theta'(0) = 0
    rows.append(evalf(0.0, "thp"))
    rhs.append(-(Bp * D * ep0))
    # rear mechanical
    if rear == "free":
        ru, rt = evalf(L, "up"), evalf(L, "th")
        rows.append([M * a - bm * b for a, b in zip(ru, rt)])
        rhs.append(-(M * Ap * D * epL - bm * Bp * epL))
    else:
        rows.append(evalf(L, "u"))
        rhs.append(-(Ap * epL))
    # theta'(L) = 0
    rows.append(evalf(L, "thp"))
    rhs.append(-(Bp * D * epL))
    cf = csolve(rows, rhs)
    th, uu, sg = [], [], []
    for x in xs:
        ex = math.exp(-x / delta)
        u = Ap * ex + sum(c * v for c, v in zip(cf, evalf(x, "u")))
        up = Ap * D * ex + sum(c * v for c, v in zip(cf, evalf(x, "up")))
        t = Bp * ex + sum(c * v for c, v in zip(cf, evalf(x, "th")))
        th.append(t)
        uu.append(u)
        sg.append(M * up - bm * t)
    return th, uu, sg


def laplace_heat_only(m, s, xs, L, Fa, tp, tau0=0.0, kstar=0.0, Gs=None, delta=None):
    """Uncoupled heat conduction in the Laplace domain (fast; used for calibration)."""
    rc = m["rho"] * m["c"]
    delta = delta or m["delta"]
    K = keff(m, s, tau0, kstar)
    if Gs is None:
        Gs = gauss_laplace(s, tp)
    q0 = Fa * Gs / (delta * (1.0 - math.exp(-L / delta)))
    r = cmath.sqrt(s * rc / K)
    if r.real < 0:
        r = -r
    P = -q0 / (K / delta ** 2 - s * rc)
    eL = cmath.exp(-r * L)
    edl = math.exp(-L / delta)
    # theta'(0)=0: -P/delta - r C1 + r C2 eL = 0 ; theta'(L)=0: -P edl/delta - r C1 eL + r C2 = 0
    a11, a12, b1 = -r, r * eL, P / delta
    a21, a22, b2 = -r * eL, r, P * edl / delta
    det = a11 * a22 - a12 * a21
    C1 = (b1 * a22 - a12 * b2) / det
    C2 = (a11 * b2 - a21 * b1) / det
    return [P * math.exp(-x / delta) + C1 * cmath.exp(-r * x) + C2 * cmath.exp(-r * (L - x)) for x in xs]


# ---------------------------------------------------------------------------
# Durbin inversion
# ---------------------------------------------------------------------------
def durbin_nodes(Tw, N, aT=6.0):
    a = aT / Tw
    return a, [complex(a, k * math.pi / Tw) for k in range(N + 1)]


def durbin_invert(Fvals, ts, Tw, a, N):
    """Fvals[k] = F(a + i k pi / Tw) (any scalar). Returns f(t) for t in ts (t <= Tw)."""
    sig = [1.0] + [math.sin(k * math.pi / (N + 1)) / (k * math.pi / (N + 1)) for k in range(1, N + 1)]
    out = []
    for t in ts:
        acc = 0.5 * Fvals[0].real
        w = cmath.exp(1j * math.pi * t / Tw)
        z = 1.0 + 0j
        for k in range(1, N + 1):
            z *= w
            acc += sig[k] * (Fvals[k] * z).real
        out.append(math.exp(a * t) / Tw * acc)
    return out


def solve_time(m, L, Fa, tp, ts, xs, tau0=0.0, kstar=0.0, rear="free", coupled=True, N=1500, Tw=None,
               fields=("theta", "u", "sigma")):
    """Return dict of theta[x][t], u[x][t], sigma[x][t] via Durbin inversion."""
    d = derived(m)
    Tw = Tw or max(ts) * 1.0
    a, nodes = durbin_nodes(Tw, N)
    Fth = [[] for _ in xs]
    Fu = [[] for _ in xs]
    Fs = [[] for _ in xs]
    for s in nodes:
        th, uu, sg = laplace_fields(m, d, s, xs, L, Fa, tp, tau0, kstar, rear, coupled)
        for i in range(len(xs)):
            Fth[i].append(th[i])
            Fu[i].append(uu[i])
            Fs[i].append(sg[i])
    res = dict(theta=[], u=[], sigma=[])
    src = dict(theta=Fth, u=Fu, sigma=Fs)
    for f in fields:
        for i in range(len(xs)):
            res[f].append(durbin_invert(src[f][i], ts, Tw, a, N))
    return res


def heat_time(m, L, Fa, tp, ts, xs, tau0=0.0, kstar=0.0, N=600, Tw=None, delta=None, cache=None):
    Tw = Tw or max(ts)
    a, nodes = durbin_nodes(Tw, N)
    key = (tp, Tw, N)
    if cache is not None and key in cache:
        Gl = cache[key]
    else:
        Gl = [gauss_laplace(s, tp) for s in nodes]
        if cache is not None:
            cache[key] = Gl
    F = [[] for _ in xs]
    for s, g in zip(nodes, Gl):
        th = laplace_heat_only(m, s, xs, L, Fa, tp, tau0, kstar, Gs=g, delta=delta)
        for i in range(len(xs)):
            F[i].append(th[i])
    return [durbin_invert(F[i], ts, Tw, a, N) for i in range(len(xs))]


# ---------------------------------------------------------------------------
# Independent finite-difference solver (validation)
# ---------------------------------------------------------------------------
def thomas(a, b, c, d):
    n = len(d)
    cp, dp = [0.0] * n, [0.0] * n
    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]
    for i in range(1, n):
        den = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / den if i < n - 1 else 0.0
        dp[i] = (d[i] - a[i] * dp[i - 1]) / den
    x = [0.0] * n
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


class StaggeredElastic:
    """1-D elastodynamics, staggered velocity-stress leapfrog (2nd order):
        rho v_t = sigma_x,  sigma_t = M v_x - beta theta_t.
    sigma lives on the nodes x_i (i = 0..nx-1), v on the half nodes.
    x = 0 traction-free; x = L traction-free or clamped (v = 0)."""

    def __init__(self, M, beta, rho, dx, nx, rear):
        self.M, self.beta, self.rho, self.dx, self.nx, self.rear = M, beta, rho, dx, nx, rear
        self.sig = [0.0] * nx
        self.v = [0.0] * (nx - 1)

    def step(self, dt, dtheta):
        """Advance one step; dtheta = theta^{n+1} - theta^n at nodes. Returns strain rate at nodes."""
        nx, dx = self.nx, self.dx
        sig, v = self.sig, self.v
        for j in range(nx - 1):
            v[j] += dt / self.rho * (sig[j + 1] - sig[j]) / dx
        vx = [0.0] * nx
        for i in range(1, nx - 1):
            vx[i] = (v[i] - v[i - 1]) / dx
        # rigid rear: mirror v_{N+1/2} = -v_{N-1/2}; free faces: sigma = 0 imposed directly
        vx[-1] = -2.0 * v[-1] / dx if self.rear == "rigid" else vx[-2]
        vx[0] = vx[1]                     # used only in the heat-equation coupling term
        for i in range(1, nx - 1):
            sig[i] += dt * self.M * vx[i] - self.beta * dtheta[i]
        if self.rear == "rigid":
            sig[-1] += dt * self.M * vx[-1] - self.beta * dtheta[-1]
        sig[0] = 0.0
        if self.rear == "free":
            sig[-1] = 0.0
        return vx


def fd_solve(m, L, Fa, tp, t_out, x_out, tau0=0.0, kstar=0.0, rear="free", nx=201, nsub=60, courant=0.5):
    """Time-domain FD: staggered velocity-stress mechanics + backward-Euler
    (Sobolev-type) heat equation in theta/upsilon form."""
    d = derived(m)
    M, beta, rho, rc = d["M"], d["beta"], m["rho"], d["rc"]
    k, delta = m["k"], m["delta"]
    a_s = tau0 ** 2 * kstar / 2.0
    b_s = k + tau0 * kstar
    dx = L / (nx - 1)
    dtm = courant * dx / (d["cL"] * math.sqrt(1.0 + d["eps"]))   # Courant number on the adiabatic speed
    dt = dtm / nsub
    xs = [i * dx for i in range(nx)]
    norm = Fa / (delta * (1.0 - math.exp(-L / delta)))
    prof = [norm * math.exp(-x / delta) for x in xs]
    th = [0.0] * nx
    ups = [0.0] * nx
    th_m = [0.0] * nx
    mech = StaggeredElastic(M, beta, rho, dx, nx, rear)
    vx = [0.0] * nx
    nsteps = int(round(max(t_out) / dtm)) * nsub
    out_t = {int(round(t / dtm)) * nsub: t for t in t_out}
    idx = [min(range(nx), key=lambda i: abs(xs[i] - x)) for x in x_out]
    res_th, res_sg = {}, {}
    cA = a_s + dt * b_s + dt * dt * kstar
    lo = [0.0] + [-cA / dx ** 2] * (nx - 1)
    di = [rc + 2 * cA / dx ** 2] * nx
    up_ = [-cA / dx ** 2] * (nx - 1) + [0.0]
    up_[0] = -2 * cA / dx ** 2
    lo[-1] = -2 * cA / dx ** 2

    def lap(f):
        g = [0.0] * nx
        g[0] = 2 * (f[1] - f[0]) / dx ** 2
        g[-1] = 2 * (f[-2] - f[-1]) / dx ** 2
        for i in range(1, nx - 1):
            g[i] = (f[i + 1] - 2 * f[i] + f[i - 1]) / dx ** 2
        return g

    for n in range(1, nsteps + 1):
        t = n * dt
        g = gauss_pulse(t, tp)
        lth = lap(th)
        lup = lap(ups)
        rhs = [rc * th[i] - a_s * lth[i] + dt * (kstar * lup[i] - beta * T0 * vx[i] + prof[i] * g) for i in range(nx)]
        th_new = thomas(lo, di, up_, rhs)
        ups = [ups[i] + dt * th_new[i] for i in range(nx)]
        th = th_new
        if n % nsub == 0:
            vx = mech.step(dtm, [th[i] - th_m[i] for i in range(nx)])
            th_m = th[:]
        if n in out_t:
            tt = out_t[n]
            res_th[tt] = [th[i] for i in idx]
            res_sg[tt] = [mech.sig[i] for i in idx]
    return res_th, res_sg


# ---------------------------------------------------------------------------
# Two-temperature model (reference for calibration)
# ---------------------------------------------------------------------------
def ttm_solve(m, L, Fa, tp, t_out, nx=101, dt=5e-15):
    """Nonlinear parabolic two-step (two-temperature) model with C_e = gamma Te,
    k_e = ke0 Te/Tl; lattice conduction neglected. Returns lattice temperature rise
    and electron temperature rise at the grid nodes for each t in t_out."""
    gam, G, ke0, Cl = m["gamma_e"], m["G"], m["ke0"], m["rho"] * m["c"]
    delta = m["delta"]
    dx = L / (nx - 1)
    xs = [i * dx for i in range(nx)]
    norm = Fa / (delta * (1.0 - math.exp(-L / delta)))
    prof = [norm * math.exp(-x / delta) for x in xs]
    Te = [T0] * nx
    Tl = [T0] * nx
    nsteps = int(round(max(t_out) / dt))
    out_t = {int(round(t / dt)): t for t in t_out}
    resl, rese = {}, {}
    for n in range(1, nsteps + 1):
        t = n * dt
        g = gauss_pulse(t, tp)
        ke = [ke0 * Te[i] / Tl[i] for i in range(nx)]
        kh = [0.5 * (ke[i] + ke[i + 1]) for i in range(nx - 1)]
        Ce = [gam * Te[i] for i in range(nx)]
        a = [0.0] * nx
        b = [0.0] * nx
        c = [0.0] * nx
        dd = [0.0] * nx
        for i in range(nx):
            kl = kh[i - 1] if i > 0 else 0.0
            kr = kh[i] if i < nx - 1 else 0.0
            if i == 0:
                kr2 = 2 * kr
                a[i], c[i] = 0.0, -dt * kr2 / dx ** 2
                b[i] = Ce[i] + dt * kr2 / dx ** 2 + dt * G
            elif i == nx - 1:
                kl2 = 2 * kl
                a[i], c[i] = -dt * kl2 / dx ** 2, 0.0
                b[i] = Ce[i] + dt * kl2 / dx ** 2 + dt * G
            else:
                a[i] = -dt * kl / dx ** 2
                c[i] = -dt * kr / dx ** 2
                b[i] = Ce[i] + dt * (kl + kr) / dx ** 2 + dt * G
            dd[i] = Ce[i] * Te[i] + dt * (G * Tl[i] + prof[i] * g)
        Te = thomas(a, b, c, dd)
        Tl = [Tl[i] + dt * G * (Te[i] - Tl[i]) / Cl for i in range(nx)]
        if n in out_t:
            resl[out_t[n]] = [v - T0 for v in Tl]
            rese[out_t[n]] = [v - T0 for v in Te]
    return xs, resl, rese


def ttm_stress(m, L, Fa, tp, t_out, x_out, rear="free", nx=201, nsub=60):
    """Two-temperature model with one-way coupled elastodynamics: the lattice
    temperature from the TTM drives the thermal stress (electron pressure neglected)."""
    d = derived(m)
    M, beta, rho = d["M"], d["beta"], m["rho"]
    gam, G, ke0, Cl = m["gamma_e"], m["G"], m["ke0"], m["rho"] * m["c"]
    delta = m["delta"]
    dx = L / (nx - 1)
    xs = [i * dx for i in range(nx)]
    norm = Fa / (delta * (1.0 - math.exp(-L / delta)))
    prof = [norm * math.exp(-x / delta) for x in xs]
    Te = [T0] * nx
    Tl = [T0] * nx
    Tl_m = [T0] * nx
    mech = StaggeredElastic(M, beta, rho, dx, nx, rear)
    dtm = dx / d["cL"]
    dt = dtm / nsub
    nsteps = int(round(max(t_out) / dtm)) * nsub
    out_t = {int(round(t / dtm)) * nsub: t for t in t_out}
    idx = [min(range(nx), key=lambda i: abs(xs[i] - x)) for x in x_out]
    res_th, res_sg = {}, {}
    for n in range(1, nsteps + 1):
        t = n * dt
        g = gauss_pulse(t, tp)
        ke = [ke0 * Te[i] / Tl[i] for i in range(nx)]
        kh = [0.5 * (ke[i] + ke[i + 1]) for i in range(nx - 1)]
        a = [0.0] * nx
        b = [0.0] * nx
        c = [0.0] * nx
        dd = [0.0] * nx
        for i in range(nx):
            Ce = gam * Te[i]
            kl = kh[i - 1] if i > 0 else 0.0
            kr = kh[i] if i < nx - 1 else 0.0
            if i == 0:
                kr *= 2
            if i == nx - 1:
                kl *= 2
            a[i] = -dt * kl / dx ** 2
            c[i] = -dt * kr / dx ** 2
            b[i] = Ce + dt * (kl + kr) / dx ** 2 + dt * G
            dd[i] = Ce * Te[i] + dt * (G * Tl[i] + prof[i] * g)
        Te = thomas(a, b, c, dd)
        Tl = [Tl[i] + dt * G * (Te[i] - Tl[i]) / Cl for i in range(nx)]
        if n % nsub == 0:
            mech.step(dtm, [Tl[i] - Tl_m[i] for i in range(nx)])
            Tl_m = Tl[:]
        if n in out_t:
            tt = out_t[n]
            res_th[tt] = [Tl[i] - T0 for i in idx]
            res_sg[tt] = [mech.sig[i] for i in idx]
    return res_th, res_sg


if __name__ == "__main__":
    au = MATERIALS["Au"]
    d = derived(au)
    print({k: (round(v, 4) if isinstance(v, float) and abs(v) > 1e-3 else v) for k, v in d.items()})
    L, Fa, tp = 200e-9, 1.0, 100e-15
    xs = [0.0, 50e-9, 100e-9, 199e-9]
    ts = [1e-12, 5e-12, 20e-12, 60e-12]
    r = solve_time(au, L, Fa, tp, ts, xs, N=800, Tw=80e-12)
    for i, x in enumerate(xs):
        print(x, ["%.3f" % v for v in r["theta"][i]], ["%.3e" % v for v in r["sigma"][i]])
