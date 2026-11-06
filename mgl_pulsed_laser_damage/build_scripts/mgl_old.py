"""Pure-Python Laplace-domain solution and Durbin inversion for the
fractional-order MGL cavity problem (sphere: eqs 27-35, cylinder: eqs 36-42)."""
import cmath
import math

# ---------------- material constants (Table 1, copper data of [1]) ----------
LAM, MU, ALPHA_T = 7.76e10, 3.86e10, 1.78e-5
CE, KCOND, RHO, T0 = 383.1, 386.0, 8954.0, 293.0
GAMMA = (3 * LAM + 2 * MU) * ALPHA_T
D1 = GAMMA * T0 / (LAM + 2 * MU)
D2 = GAMMA / (RHO * CE)
EPS = D1 * D2
LAMBDA1 = LAM / (LAM + 2 * MU)
KAPPA = 1.0 - LAMBDA1
EULER = 0.5772156649015329


def constants():
    return dict(gamma=GAMMA, d1=D1, d2=D2, eps=EPS, lambda1=LAMBDA1, kappa=KAPPA,
                eta=RHO * CE / KCOND,
                v=math.sqrt((LAM + 2 * MU) / RHO))


# ---------------- modified Bessel functions, scaled: K_n(z) e^z -------------
def _k_series(z):
    """K0, K1 by ascending series (|z| <= 2)."""
    q = z * z / 4.0
    lg = cmath.log(z / 2.0)
    # I0, I1
    i0 = 0j
    i1 = 0j
    k0s = 0j
    k1s = 0j
    term0 = 1.0 + 0j  # q^k/(k!)^2
    term1 = 1.0 + 0j  # q^k/(k!(k+1)!)
    h = 0.0           # harmonic number H_k
    for k in range(0, 60):
        if k > 0:
            term0 *= q / (k * k)
            term1 *= q / (k * (k + 1))
            h += 1.0 / k
        i0 += term0
        i1 += term1
        k0s += term0 * h
        psi1 = -EULER + h
        psi2 = -EULER + h + 1.0 / (k + 1)
        k1s += term1 * (psi1 + psi2)
        if abs(term0) < 1e-18 * abs(i0) and k > 3:
            break
    i1 *= z / 2.0
    K0 = -(lg + EULER) * i0 + k0s
    K1 = 1.0 / z + lg * i1 - (z / 4.0) * k1s
    ez = cmath.exp(z)
    return K0 * ez, K1 * ez


_H = 0.2
_W = [k * _H for k in range(0, 36)]


def _k_integral(z):
    """Scaled K0, K1 for |z| > 2, Re z > 0, via
    K_nu(z) e^z = sqrt(pi/2z)/Gamma(nu+1/2) * int_0^inf e^-u u^(nu-1/2)(1+u/2z)^(nu-1/2) du,
    with u = w^2 and the trapezoidal rule (spectrally accurate here)."""
    s0 = 0j
    s1 = 0j
    inv2z = 1.0 / (2.0 * z)
    for j, w in enumerate(_W):
        w2 = w * w
        e = math.exp(-w2)
        root = cmath.sqrt(1.0 + w2 * inv2z)
        f0 = 2.0 * e / root
        f1 = 2.0 * w2 * e * root
        wt = 0.5 if j == 0 else 1.0
        s0 += wt * f0
        s1 += wt * f1
    pref = cmath.sqrt(math.pi / (2.0 * z))
    return pref * s0 * _H / math.sqrt(math.pi), pref * s1 * _H / (math.sqrt(math.pi) / 2.0)


def kscaled(z):
    if abs(z) <= 2.0:
        return _k_series(z)
    return _k_integral(z)


# ---------------- roots m1, m2 (eqs 25-26) -----------------------------------
def roots(s, alpha, tau0, tau1):
    p = 1.0 + tau1 * s
    g = 1.0 + tau0 ** alpha * s ** alpha / math.gamma(alpha + 1.0)  # principal branch
    B = s * s / p + (1.0 + EPS) * s * g
    C = s ** 3 * g / p
    disc = cmath.sqrt(B * B - 4.0 * C)
    x1 = (B + disc) / 2.0
    x2 = (B - disc) / 2.0
    if abs(x2) > abs(x1):
        x1, x2 = x2, x1
    x2 = C / x1
    m1 = cmath.sqrt(x1)
    m2 = cmath.sqrt(x2)
    if m1.real < 0:
        m1 = -m1
    if m2.real < 0:
        m2 = -m2
    return p, m1, m2


# ---------------- Laplace-domain fields --------------------------------------
def sphere_fields(s, rs, a, alpha, tau0, tau1, theta0=1.0):
    """Return list of (theta, u, srr, spp) Laplace transforms at radii rs."""
    p, m1, m2 = roots(s, alpha, tau0, tau1)
    ms = (m1, m2)
    s2p = s * s / p
    # B_i = A_i e^{-m_i a}/a ; system (32)-(33)
    c1 = [(m * m - s2p) for m in ms]
    c2 = [(s * s + 2.0 * p * KAPPA * (1.0 + m * a) / (a * a)) for m in ms]
    det = c1[0] * c2[1] - c1[1] * c2[0]
    rhs = D1 * theta0 / s
    B1 = rhs * c2[1] / det
    B2 = -rhs * c2[0] / det
    Bs = (B1, B2)
    out = []
    for r in rs:
        phi = 0j
        u = 0j
        th = 0j
        lap = 0j
        for m, Bi in zip(ms, Bs):
            e = cmath.exp(-m * (r - a)) * a  # A_i e^{-m r} = B_i a e^{-m(r-a)}
            phi_i = Bi * e / r
            phi += phi_i
            u += -Bi * e * (1.0 + m * r) / (r * r)
            th += (m * m - s2p) * phi_i / D1
            lap += m * m * phi_i
        srr = s * s * phi - 2.0 * p * KAPPA * u / r
        spp = s * s * phi + p * KAPPA * (u / r - lap)
        out.append((th, u, srr, spp))
    return out


def cylinder_fields(s, rs, a, alpha, tau0, tau1, theta0=1.0):
    p, m1, m2 = roots(s, alpha, tau0, tau1)
    ms = (m1, m2)
    s2p = s * s / p
    ka = [kscaled(m * a) for m in ms]
    # B_i = A_i K0(m_i a)
    b1 = [(m * m - s2p) for m in ms]
    C = [s * s + p * KAPPA * m * k[1] / (k[0] * a) for m, k in zip(ms, ka)]
    det = b1[0] * C[1] - b1[1] * C[0]
    rhs = D1 * theta0 / s
    Bs = (rhs * C[1] / det, -rhs * C[0] / det)
    out = []
    for r in rs:
        phi = u = th = lap = 0j
        for m, Bi, k in zip(ms, Bs, ka):
            kr = kscaled(m * r)
            fac = cmath.exp(-m * (r - a)) / k[0]
            phi_i = Bi * kr[0] * fac
            phi += phi_i
            u += -Bi * m * kr[1] * fac
            th += (m * m - s2p) * phi_i / D1
            lap += m * m * phi_i
        srr = s * s * phi - p * KAPPA * u / r
        spp = s * s * phi + p * KAPPA * (u / r - lap)
        out.append((th, u, srr, spp))
    return out


# ---------------- Durbin inversion (eq 46) with Wynn-epsilon acceleration ---
def wynn(seq):
    """Wynn epsilon algorithm on a list of partial sums; returns accelerated value."""
    n = len(seq)
    prev = [0.0] * (n + 1)
    cur = list(seq)
    ests = [seq[-1]]
    k = 0
    while len(cur) > 1:
        nxt = []
        for j in range(len(cur) - 1):
            d = cur[j + 1] - cur[j]
            if abs(d) < 1e-280:
                d = 1e-280
            nxt.append(prev[j + 1] + 1.0 / d)
        k += 1
        prev, cur = cur, nxt
        if k % 2 == 0 and cur:
            ests.append(cur[-1])
    # choose the even-column estimate that agrees best with its predecessor
    best = ests[0]
    bestdiff = float("inf")
    for i in range(1, len(ests)):
        a, b = ests[i], ests[i - 1]
        if not (math.isfinite(a) and math.isfinite(b)) or abs(a) > 1e100:
            continue
        diff = abs(a - b)
        if diff < bestdiff:
            bestdiff, best = diff, a
    return best


def durbin(Ffun, t, nfield, npts, N=4000, ct=6.0, Tfac=2.0, nwynn=0):
    """Invert vector-valued F(s) -> list[npts][nfield] at time t.
    Ffun(s) must return list of npts tuples of nfield complex values.
    Returns (values_N, values_N/2) for the truncation test (47)."""
    T = Tfac * t
    c = ct / t
    F0 = Ffun(complex(c, 0.0))
    sums = [[0.5 * F0[i][j].real for j in range(nfield)] for i in range(npts)]
    half = None
    partial = []  # partial sums for Wynn (stored every 'stride' terms)
    stride = 1
    for k in range(1, N + 1):
        w = k * math.pi / T
        Fk = Ffun(complex(c, w))
        cs = math.cos(w * t)
        sn = math.sin(w * t)
        for i in range(npts):
            row = sums[i]
            fk = Fk[i]
            for j in range(nfield):
                row[j] += fk[j].real * cs - fk[j].imag * sn
        if k == N // 2:
            half = [list(r) for r in sums]
        if nwynn and k > N - nwynn:
            partial.append([list(r) for r in sums])
    scale = math.exp(c * t) / T
    full = [[v * scale for v in r] for r in sums]
    halfv = [[v * scale for v in r] for r in half]
    if nwynn:
        acc = [[wynn([p[i][j] for p in partial]) * scale for j in range(nfield)]
               for i in range(npts)]
        return acc, full, halfv
    return full, halfv
