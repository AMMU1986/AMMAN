"""Galerkin FE (linear elements) + BDF2 convolution quadrature in time for the layered fractional MGL bioheat
thermoelastic slab with temperature-dependent perfusion and conductivity (Picard iteration per step)."""
import math
import model
from banded import Banded


def cq_weights(p, n, dt):
    """coefficients of ((3-4z+z^2)/(2 dt))^p, j=0..n (BDF2 convolution quadrature of an order-p derivative)"""
    f = [0.0] * (n + 2)
    f[0] = 1.5 ** p
    for k in range(0, n):
        fm = f[k - 1] if k >= 1 else 0.0
        f[k + 1] = (4 * (k - p) * f[k] + (2 * p - k + 1) * fm) / (3 * (k + 1))
    w = [x / dt ** p for x in f[:n + 1]]
    if abs(p - round(p)) < 1e-12:
        for j in range(int(round(p)) * 2 + 1, n + 1):
            w[j] = 0.0
    return w


def pulse(t, tp):
    if t < tp - 1e-12:
        return 1.0
    return 0.5 if abs(t - tp) < 1e-12 else 0.0


class Result:
    pass


def run(p, dx=0.005, dt=0.01, T=0.5, tol=1e-11, maxit=60):
    h = p["h"]
    L = p["layers"]
    n1 = max(1, int(round(h / dx)))
    n2 = max(1, int(round((1 - h) / dx)))
    xs = [h * i / n1 for i in range(n1 + 1)] + [h + (1 - h) * i / n2 for i in range(1, n2 + 1)]
    nn = len(xs)
    ne = nn - 1
    li = [0 if e < n1 else 1 for e in range(ne)]
    le_ = [xs[e + 1] - xs[e] for e in range(ne)]
    nstep = int(round(T / dt))
    a, tau0, tau1 = p["alpha"], p["tau0"], p["tau1"]
    w1 = cq_weights(1.0, nstep, dt)
    w2 = cq_weights(2.0, nstep, dt)
    wa = cq_weights(1.0 + a, nstep, dt) if tau0 > 0 else [0.0] * (nstep + 1)
    t0a = tau0 ** a if tau0 > 0 else 0.0
    cE = [w1[j] + t0a * wa[j] for j in range(nstep + 1)]
    cR = w2
    c1 = [(1.0 if j == 0 else 0.0) + tau1 * w1[j] for j in range(nstep + 1)]
    nd = 2 * nn
    nonlin = any(c != 0 for c in p["cw"]) or any(c != 0 for c in p["chi"])
    theta0 = p["theta0"]
    laser = p.get("a7", 0) != 0
    ls = model.laser_shape()
    qvec = [0.0] * nn
    if laser:
        g = lambda x: ls["B1"] * math.exp(-ls["l1"] * x / ls["deltas"]) - ls["B2"] * math.exp(-ls["l2"] * x / ls["deltas"])
        for e in range(ne):
            ga, gm, gb = g(xs[e]), g(0.5 * (xs[e] + xs[e + 1])), g(xs[e + 1])
            qvec[e] += p["a7"] * le_[e] / 6 * (ga + 2 * gm)
            qvec[e + 1] += p["a7"] * le_[e] / 6 * (2 * gm + gb)
    dir_dofs = [(1, None), (2 * (nn - 1), 0.0), (2 * (nn - 1) + 1, 0.0)]  # theta_0 value set per step

    def assemble(thit):
        A = Banded(nd, 3)
        add = A.add
        for e in range(ne):
            le = le_[e]
            k = li[e]
            c = L[k]
            tm = 0.5 * (thit[e] + thit[e + 1])
            chi = p["chi"][k]
            kk = c["kappa"] * (1 + chi * tm)
            om = model.omega(tm, p["cw"][k], p["thc"][k], p["dth"]) if p["cw"][k] != 0 else 1.0
            ms = le / 6.0
            for r in range(2):
                for q in range(2):
                    mass = ms * (2.0 if r == q else 1.0)
                    stiff = (1.0 if r == q else -1.0) / le
                    Gv = c["a9"] * (-0.5 if r == 0 else 0.5)
                    Cu = c["a5"] * 0.5 * (-1.0 if q == 0 else 1.0)
                    ir, iq = e + r, e + q
                    add(2 * ir, 2 * iq, cR[0] * c["rho"] * mass + c1[0] * c["a8"] * stiff)
                    add(2 * ir, 2 * iq + 1, -c1[0] * Gv)
                    add(2 * ir + 1, 2 * iq, cE[0] * Cu)
                    add(2 * ir + 1, 2 * iq + 1, cE[0] * c["C"] * mass + kk * stiff + c["a6"] * om * mass)
        cols = {}
        for k_, _ in dir_dofs:
            ent = []
            for j in range(max(0, k_ - 3), min(nd, k_ + 4)):
                ent.append((j, A.a[j][k_ - j + 3]))
            cols[k_] = ent
        for k_, _ in dir_dofs:
            for j in range(max(0, k_ - 3), min(nd, k_ + 4)):
                A.a[j][k_ - j + 3] = 0.0
                A.a[k_][j - k_ + 3] = 0.0
            A.a[k_][3] = 1.0
        A.lu()
        return A, cols

    btau = p.get('bc_tau', 0.0)
    bc = (lambda t: theta0 * (1 - math.exp(-t / btau))) if btau else (lambda t: theta0)
    TH = [[(0.0 if btau else 0.5 * theta0)] + [0.0] * (nn - 1)]   # Heaviside H(0)=1/2
    U = [[0.0] * nn]
    iters = []
    resid_hist = []
    if not nonlin:
        Afac, cols = assemble([0.0] * nn)
    for n in range(1, nstep + 1):
        t = n * dt
        # history sums
        SuR = [0.0] * nn; Su1 = [0.0] * nn; SuE = [0.0] * nn; Sth1 = [0.0] * nn; SthE = [0.0] * nn
        for j in range(1, n + 1):
            u_ = U[n - j]; th_ = TH[n - j]
            cr, cc1, ce = cR[j], c1[j], cE[j]
            if cr != 0.0:
                SuR = [s + cr * v for s, v in zip(SuR, u_)]
            if cc1 != 0.0:
                Su1 = [s + cc1 * v for s, v in zip(Su1, u_)]
                Sth1 = [s + cc1 * v for s, v in zip(Sth1, th_)]
            if ce != 0.0:
                SuE = [s + ce * v for s, v in zip(SuE, u_)]
                SthE = [s + ce * v for s, v in zip(SthE, th_)]
        rhs = [0.0] * nd
        fq = pulse(t, p["tp"]) if laser else 0.0
        for e in range(ne):
            le = le_[e]
            c = L[li[e]]
            ms = le / 6.0
            for r in range(2):
                ir = e + r
                su = sth = 0.0
                for q in range(2):
                    iq = e + q
                    mass = ms * (2.0 if r == q else 1.0)
                    stiff = (1.0 if r == q else -1.0) / le
                    Gv = c["a9"] * (-0.5 if r == 0 else 0.5)
                    Cu = c["a5"] * 0.5 * (-1.0 if q == 0 else 1.0)
                    su += c["rho"] * mass * SuR[iq] + c["a8"] * stiff * Su1[iq] - Gv * Sth1[iq]
                    sth += c["C"] * mass * SthE[iq] + Cu * SuE[iq]
                rhs[2 * ir] -= su
                rhs[2 * ir + 1] -= sth
        for i in range(nn):
            rhs[2 * i + 1] += qvec[i] * fq
        dvals = {1: bc(t), 2 * (nn - 1): 0.0, 2 * (nn - 1) + 1: 0.0}
        thit = list(TH[n - 1]) if n < 2 else [2 * x - y for x, y in zip(TH[n - 1], TH[n - 2])]
        if not nonlin:
            b = rhs[:]
            for k_, v in dvals.items():
                if v != 0.0:
                    for j, ajk in cols[k_]:
                        if j != k_:
                            b[j] -= ajk * v
            for k_, v in dvals.items():
                b[k_] = v
            x = Afac.solve(b)
            iters.append(1)
        else:
            for it in range(1, maxit + 1):
                A, cols = assemble(thit)
                b = rhs[:]
                for k_, v in dvals.items():
                    if v != 0.0:
                        for j, ajk in cols[k_]:
                            if j != k_:
                                b[j] -= ajk * v
                for k_, v in dvals.items():
                    b[k_] = v
                x = A.solve(b)
                thn = x[1::2]
                d = max(abs(s - r_) for s, r_ in zip(thn, thit))
                thit = thn
                if n == nstep:
                    resid_hist.append(d)
                if d < tol:
                    break
            iters.append(it)
        U.append(x[0::2])
        TH.append(x[1::2])
    R = Result()
    R.xs, R.TH, R.U, R.dt, R.nstep, R.iters, R.resid = xs, TH, U, dt, nstep, iters, resid_hist
    R.n1, R.li, R.le, R.L, R.p, R.c1 = n1, li, le_, L, p, c1
    return R


def stress(R, n):
    """sigma at element midpoints at step n (with (1+tau1 d/dt) applied by BDF2 convolution)"""
    ne = len(R.le)
    xm = [0.5 * (R.xs[e] + R.xs[e + 1]) for e in range(ne)]
    sig = [0.0] * ne
    for j in range(0, min(n, 2) + 1):
        cj = R.c1[j]
        if cj == 0.0:
            continue
        u, th = R.U[n - j], R.TH[n - j]
        for e in range(ne):
            c = R.L[R.li[e]]
            sig[e] += cj * (c["a8"] * (u[e + 1] - u[e]) / R.le[e] - c["a9"] * 0.5 * (th[e] + th[e + 1]))
    return xm, sig


def at(R, n, x, field):
    """linearly interpolated nodal value (theta/u) at x"""
    xs = R.xs
    lo, hi = 0, len(xs) - 1
    while hi - lo > 1:
        m = (lo + hi) // 2
        if xs[m] <= x:
            lo = m
        else:
            hi = m
    f = (x - xs[lo]) / (xs[hi] - xs[lo])
    v = (R.TH if field == "th" else R.U)[n]
    return v[lo] * (1 - f) + v[hi] * f
