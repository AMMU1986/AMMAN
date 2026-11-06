"""Exact Laplace-domain solution of the linear two-layer MGL / fractional-MGL / MGT / Pennes bioheat
thermoelastic slab, with numerical (Durbin + Wynn epsilon) inversion.  Pure Python complex arithmetic."""
import cmath, math
import model
from mgl_old import durbin


def lag(p, s):
    """returns (kap_scale, Ts, Lp, Lq, sig) for the model selected in p"""
    m = p["model"]
    if m == "MGT":
        tq = p["taq"]
        return "mgt", (1 + tq * s) * s, (1 + tq * s), (1 + tq * s), 1.0
    a = p["alpha"]
    Ts = (1 + (p["tau0"] ** a) * s ** a * (1 if p["tau0"] > 0 else 0)) * s if p["tau0"] > 0 else s
    return "mgl", Ts, 1.0, 1.0, 1 + p["tau1"] * s


def solve8(A, b):
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for k in range(n):
        piv = max(range(k, n), key=lambda i: abs(M[i][k]))
        M[k], M[piv] = M[piv], M[k]
        d = M[k][k]
        for i in range(k + 1, n):
            f = M[i][k] / d
            if f != 0:
                rk, ri = M[k], M[i]
                for j in range(k, n + 1):
                    ri[j] -= f * rk[j]
    x = [0j] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n]
        for j in range(i + 1, n):
            s -= M[i][j] * x[j]
        x[i] = s / M[i][i]
    return x


class Layer:
    def __init__(self, p, i, s):
        c = p["layers"][i]
        self.c = c
        kind, Ts, Lp, Lq, sig = lag(p, s)
        self.sig = sig
        kap = c["kappa"] + ((c["a3"] / s) if kind == "mgt" else 0.0)
        self.kap = kap
        r = c["a9"] / c["a8"]
        A = (c["C"] * Ts + c["a6"] * Lp) / kap
        b = c["a5"] * Ts / kap
        m = c["rho"] * s * s / (sig * c["a8"])
        self.s = s
        self.r, self.A, self.b, self.m, self.Lq = r, A, b, m, Lq
        M = [[m + r * b, r * A], [b, A]]
        tr = M[0][0] + M[1][1]
        det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
        disc = cmath.sqrt(tr * tr / 4 - det)
        self.q, self.vec = [], []
        for mu in (tr / 2 + disc, tr / 2 - disc):
            q = cmath.sqrt(mu)
            if q.real < 0:
                q = -q
            v1 = (M[0][1], mu - M[0][0])
            v2 = (mu - M[1][1], M[1][0])
            v = v1 if abs(v1[0]) + abs(v1[1]) > abs(v2[0]) + abs(v2[1]) else v2
            nv = abs(v[0]) + abs(v[1])
            self.q.append(q)
            self.vec.append((v[0] / nv, v[1] / nv))
        self.M = M
        self.pre = [] # particular terms (gamma, amp in forcing)
        if p.get("a7", 0) and p.get("laser", False):
            ls = model.laser_shape()
            fh = (1 - cmath.exp(-s * p["tp"])) / s
            for B, lam in ((ls["B1"], ls["l1"]), (-ls["B2"], ls["l2"])):
                gam = lam / ls["deltas"]
                Fth = Lq * p["a7"] * B * fh / kap
                Fv = (r * Fth, Fth)
                a11, a12, a21, a22 = gam * gam - M[0][0], -M[0][1], -M[1][0], gam * gam - M[1][1]
                dd = a11 * a22 - a12 * a21
                c0 = -(a22 * Fv[0] - a12 * Fv[1]) / dd
                c1 = -(-a21 * Fv[0] + a11 * Fv[1]) / dd
                self.pre.append((gam, c0, c1))

    def mode(self, k, sgn, x, xa, xb):
        """field vector of mode k, sgn=+1 decaying to the right (anchored at xa), -1 decaying to the left (anchored xb)"""
        q = self.q[k]
        e0, t0 = self.vec[k]
        if sgn > 0:
            f = cmath.exp(-q * (x - xa)); dd = -q
        else:
            f = cmath.exp(q * (x - xb)); dd = q
        return e0 * f, t0 * f, e0 * f * dd, t0 * f * dd

    def particular(self, x):
        e = th = de = dth = 0j
        for gam, c0, c1 in self.pre:
            f = cmath.exp(-gam * x)
            e += c0 * f; th += c1 * f; de += -gam * c0 * f; dth += -gam * c1 * f
        return e, th, de, dth

    def derived(self, e, th, de, dth):
        c = self.c
        u = self.sig * (c["a8"] * de - c["a9"] * dth) / (c["rho"] * self.s ** 2)
        S = c["a8"] * e - c["a9"] * th
        flux = self.kap * dth
        return th, u, S, flux


def solve_s(p, s):
    h = p["h"]
    L1, L2 = Layer(p, 0, s), Layer(p, 1, s)
    lay = (L1, L2)
    spans = ((0.0, h), (h, 1.0))

    def cols(i, x):
        """4 mode columns -> (th,u,S,flux) tuples at x for layer i; plus particular"""
        Ly = lay[i]
        xa, xb = spans[i]
        out = []
        for k in range(2):
            for sg in (1, -1):
                out.append(Ly.derived(*Ly.mode(k, sg, x, xa, xb)))
        pe = Ly.derived(*Ly.particular(x))
        return out, pe
    A = [[0j] * 8 for _ in range(8)]
    rhs = [0j] * 8
    # (1) sigma=0 at x=0, (2) theta1(0)=theta0/s
    c, pe = cols(0, 0.0)
    for j in range(4):
        A[0][j] = c[j][2]; A[1][j] = c[j][0]
    rhs[0] = -pe[2]; bt = p.get("bc_tau", 0.0)
    rhs[1] = p["theta0"] * ((1 / s - 1 / (s + 1 / bt)) if bt else 1 / s) - pe[0]
    # (3) u2(1)=0 (4) th2(1)=0
    c, pe = cols(1, 1.0)
    for j in range(4):
        A[2][4 + j] = c[j][1]; A[3][4 + j] = c[j][0]
    rhs[2] = -pe[1]; rhs[3] = -pe[0]
    # interface continuity of th,u,S,flux
    cl, pl = cols(0, h)
    cr, pr = cols(1, h)
    for q_, idx in enumerate((0, 1, 2, 3)):
        row = 4 + q_
        for j in range(4):
            A[row][j] = cl[j][idx]
            A[row][4 + j] = -cr[j][idx]
        rhs[row] = pr[idx] - pl[idx]
    amp = solve8(A, rhs)
    return lay, spans, amp


def fields(p, s, xs):
    """list of (theta, u, sigma) at points xs (sigma incl. (1+tau1 s) lag) for Laplace parameter s"""
    lay, spans, amp = solve_s(p, s)
    out = []
    for x in xs:
        i = 0 if x <= p["h"] + 1e-12 else 1
        if abs(x - p["h"]) < 1e-12:
            i = 0
        Ly = lay[i]
        xa, xb = spans[i]
        tot = [0j] * 4
        j = 0
        for k in range(2):
            for sg in (1, -1):
                d = Ly.derived(*Ly.mode(k, sg, x, xa, xb))
                for q in range(4):
                    tot[q] += amp[4 * i + j] * d[q]
                j += 1
        pe = Ly.derived(*Ly.particular(x))
        for q in range(4):
            tot[q] += pe[q]
        out.append((tot[0], tot[1], Ly.sig * tot[2], tot[3]))
    return out


def invert(p, xs, t, N=3000, nwynn=40, ct=6.0, Tfac=2.0):
    """returns list per x of (theta,u,sigma,flux) at time t"""
    F = lambda s: [tuple(v) for v in fields(p, s, xs)]
    r = durbin(F, t, 4, len(xs), N=N, ct=ct, Tfac=Tfac, nwynn=nwynn)
    if nwynn:
        return r
    return r[0], r[0], r[1]
