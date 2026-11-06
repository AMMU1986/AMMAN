"""Exact Laplace-domain solution of the LINEAR (constant perfusion) two-layer coupled thermoelastic bioheat slab
in SI units, with the full momentum equation (inertia retained, scaled by rho_scale) and numerical inversion
(Durbin + Wynn epsilon).  Used as an independent reference for the finite element code."""
import cmath, math
import model
from fem1d import kstar_eff
from mgl_old import durbin


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


def fhat(P, des, s):
    tp, per, Np = des["tp"], des["per"], int(des["Np"])
    r = cmath.exp(-s * per)
    geo = (1 - r ** Np) / (1 - r) if abs(1 - r) > 1e-14 else Np
    return (1 - cmath.exp(-s * tp)) / s * geo


class Layer:
    def __init__(self, P, des, i, s, rscale):
        c = P["lay"][i]
        self.c = c
        T0 = P["T0"]
        tq, t0 = P["tauq"], P["tau0"]
        Ts = s * (1 + (tq + t0) * s)
        Lq = 1 + tq * s
        self.sig = 1 + P["tau1"] * s
        kap = c["k"] + ((kstar_eff(P, c) / s) if P["kstar_on"] else 0.0)
        self.kap = kap
        om = c["om0"]
        r = c["beta"] / c["c11"]
        A = (c["C0"] * Ts + om * Lq) / kap
        b = T0 * c["beta"] * Ts / kap
        m = rscale * c["rho"] * s * s / (self.sig * c["c11"])
        self.s, self.r, self.rho = s, r, rscale * c["rho"]
        M = [[m + r * b, r * A], [b, A]]
        tr = M[0][0] + M[1][1]
        det = m * A                      # exact: (m + r b) A - r A b
        disc = cmath.sqrt(tr * tr / 4 - det)
        mu1 = tr / 2 + disc if abs(tr / 2 + disc) > abs(tr / 2 - disc) else tr / 2 - disc
        self.q, self.vec = [], []
        for mu in (mu1, det / mu1):
            q = cmath.sqrt(mu)
            if q.real < 0:
                q = -q
            v1 = (M[0][1], mu - M[0][0])
            v2 = (mu - M[1][1], M[1][0])
            v = v1 if abs(v1[0]) + abs(v1[1]) > abs(v2[0]) + abs(v2[1]) else v2
            nv = abs(v[0]) + abs(v[1])
            self.q.append(q)
            self.vec.append((v[0] / nv, v[1] / nv))
        self.pre = []
        ls = model.laser_shape(P["las"])
        fh = fhat(P, des, s)
        mua = P["las"]["mua"]
        for B, lam in ((ls["B1"], ls["l1"]), (-ls["B2"], ls["l2"])):
            gam = lam / ls["delta"]
            Fth = Lq * des["I0"] * mua * B * fh / kap
            Fv = (r * Fth, Fth)
            a11, a12, a21, a22 = gam * gam - M[0][0], -M[0][1], -M[1][0], gam * gam - M[1][1]
            dd = a11 * a22 - a12 * a21
            c0 = -(a22 * Fv[0] - a12 * Fv[1]) / dd
            c1 = -(-a21 * Fv[0] + a11 * Fv[1]) / dd
            self.pre.append((gam, c0, c1))

    def mode(self, k, sgn, x, xa, xb):
        """basis function of mode k: decaying/growing anchored exponentials when |q|(xb-xa) is large, else
        cosh(q(x-xa)) and sinh(q(x-xa))/q (well conditioned for the slow elastic mode)."""
        q = self.q[k]
        e0, t0 = self.vec[k]
        if abs(q) * (xb - xa) < 2.0:
            if sgn > 0:
                f = cmath.cosh(q * (x - xa)); dd = q * cmath.sinh(q * (x - xa)) / f if f != 0 else 0
                df = q * cmath.sinh(q * (x - xa))
            else:
                f = cmath.sinh(q * (x - xa)) / q
                df = cmath.cosh(q * (x - xa))
            return e0 * f, t0 * f, e0 * df, t0 * df
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
        Sx = self.sig * (c["c11"] * de - c["beta"] * dth)          # d(sigma_xx)/dx
        u = Sx / (self.rho * self.s ** 2)
        S = self.sig * (c["c11"] * e - c["beta"] * th)               # sigma_xx
        Syy = self.sig * (c["lam"] * e - c["beta"] * th)              # sigma_yy (laterally constrained)
        flux = self.kap * dth
        return th, u, S, flux, Syy


def solve_s(P, des, s, rscale):
    h, L = P["h"], P["L"]
    lay = (Layer(P, des, 0, s, rscale), Layer(P, des, 1, s, rscale))
    spans = ((0.0, h), (h, L))

    def cols(i, x):
        Ly = lay[i]
        xa, xb = spans[i]
        out = []
        for k in range(2):
            for sg in (1, -1):
                out.append(Ly.derived(*Ly.mode(k, sg, x, xa, xb)))
        return out, Ly.derived(*Ly.particular(x))
    A = [[0j] * 8 for _ in range(8)]
    rhs = [0j] * 8
    c, pe = cols(0, 0.0)
    for j in range(4):
        A[0][j] = c[j][2]; A[1][j] = c[j][3]       # sigma_xx = 0, flux = 0 at x = 0
    rhs[0] = -pe[2]; rhs[1] = -pe[3]
    c, pe = cols(1, L)
    for j in range(4):
        A[2][4 + j] = c[j][1]; A[3][4 + j] = c[j][0]   # u = 0, theta = 0 at x = L
    rhs[2] = -pe[1]; rhs[3] = -pe[0]
    cl, pl = cols(0, h)
    cr, pr = cols(1, h)
    for q_ in range(4):
        row = 4 + q_
        for j in range(4):
            A[row][j] = cl[j][q_]
            A[row][4 + j] = -cr[j][q_]
        rhs[row] = pr[q_] - pl[q_]
    return lay, spans, solve8(A, rhs)


def fields(P, des, s, xs, rscale):
    lay, spans, amp = solve_s(P, des, s, rscale)
    h = P["h"]
    out = []
    for x in xs:
        i = 0 if x <= h + 1e-12 else 1
        Ly = lay[i]
        xa, xb = spans[i]
        tot = [0j] * 5
        j = 0
        for k in range(2):
            for sg in (1, -1):
                d = Ly.derived(*Ly.mode(k, sg, x, xa, xb))
                for q in range(5):
                    tot[q] += amp[4 * i + j] * d[q]
                j += 1
        pe = Ly.derived(*Ly.particular(x))
        for q in range(5):
            tot[q] += pe[q]
        out.append(tuple(tot))
    return out


def invert(P, des, xs, t, rscale=1.0, N=2500, nwynn=40, ct=6.0, Tfac=2.0):
    """returns (values with Wynn, values_N, values_N/2); each list per x of (theta,u,sigma_xx,flux,sigma_yy)"""
    F = lambda s: fields(P, des, s, xs, rscale)
    return durbin(F, t, 5, len(xs), N=N, ct=ct, Tfac=Tfac, nwynn=nwynn)
