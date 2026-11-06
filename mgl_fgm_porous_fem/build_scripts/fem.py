"""Galerkin finite element solver for MGL thermoelasticity of a radially graded / porous medium
heated by a (regularized) line heat source.  Pure Python (no numpy).

Nondimensional MGL system (ratios a_* are property fields relative to the reference copper data):
  a_rho u_tt = (1+t1 d/dt) [ d_r Srr + (Srr - Stt)/r ]
  Srr = P u_r + L u/r - d1 a_g theta ,  Stt = L u_r + P u/r - d1 a_g theta
  d_r(a_k theta_r) + a_k theta_r/r = (1+t0 d/dt)[ a_rc theta_t + d2 a_g (u_r+u/r)_t ] - Q
State-space form (m = momentum-like, g = heat-content rate) removes the operators (1+t d/dt):
  M u' = m + t1 f,  m' = f,   f = -K u + G theta
  g = Mth theta' + D u',  t0 g' = -g - Kt theta + Q
Time marching: trapezoidal rule on (u, m, theta, g)  (Newmark average-acceleration + Crank-Nicolson).
"""
import math
import mgl

LAM0, MU0 = mgl.LAM, mgl.MU
D1, D2, EPS = mgl.D1, mgl.D2, mgl.EPS
L1 = mgl.LAMBDA1
KAP = 1.0 - L1
GL = {
    3: ([-0.7745966692414834, 0.0, 0.7745966692414834], [5 / 9, 8 / 9, 5 / 9]),
    5: ([-0.9061798459386640, -0.5384693101056831, 0.0, 0.5384693101056831, 0.9061798459386640],
        [0.2369268850561891, 0.4786286704993665, 0.5688888888888889, 0.4786286704993665, 0.2369268850561891]),
}
CER = dict(lam=2.0, mu=2.0, k=0.1, rho=0.5, alpha=0.5, c=2.0)   # illustrative second phase (ratios to copper)


class Props:
    """Radial property fields.  Fraction of reference (copper) phase: Vm(r); the other phase has ratios CER.
    Porosity phi(r) = phi0 * w(r); w = 1 (uniform) or 1 - Vm (graded, vanishing outside the graded zone)."""

    def __init__(self, law="power", n=0.0, Lg=1.0, beta=2.0, phi0=0.0, pgrade=False,
                 cer=None, em=2.0, ek=1.5, tau0=0.02, tau1=0.05, vfix=None):
        self.law, self.n, self.Lg, self.beta = law, n, Lg, beta
        self.phi0, self.pgrade, self.em, self.ek = phi0, pgrade, em, ek
        self.cer = cer or CER
        self.tau0, self.tau1 = tau0, tau1
        self.vfix = vfix

    def Vm(self, r):
        if self.vfix is not None:
            return self.vfix
        if r >= self.Lg:
            return 1.0
        s = r / self.Lg
        if self.law == "power":
            return s ** self.n if self.n > 0 else 1.0
        b = self.beta
        return (math.exp(b * s) - 1.0) / (math.exp(b) - 1.0)

    def phi(self, r):
        if self.phi0 == 0.0:
            return 0.0
        return self.phi0 * ((1.0 - self.Vm(r)) if self.pgrade else 1.0)

    def ratios(self, r):
        v = self.Vm(r)
        c = self.cer
        mix = lambda key: v * 1.0 + (1.0 - v) * c[key]
        lam, mu, k, rho, al, cc = (mix("lam"), mix("mu"), mix("k"), mix("rho"), mix("alpha"), mix("c"))
        ph = self.phi(r)
        fm = (1.0 - ph) ** self.em
        fk = (1.0 - ph) ** self.ek
        lam *= fm
        mu *= fm
        k *= fk
        rho *= (1.0 - ph)
        # volumetric heat capacity rho*c: porosity reduces rho only (c per unit mass unchanged)
        P = L1 * lam + KAP * mu
        lamh = L1 * lam
        gam = al * (3.0 * LAM0 * lam + 2.0 * MU0 * mu) / (3.0 * LAM0 + 2.0 * MU0)
        return dict(P=P, L=lamh, k=k, rho=rho, rc=rho * cc, g=gam, mu=mu, lam=lam)

    def speed(self, r):
        q = self.ratios(r)
        return math.sqrt(q["k"] * q["P"] / (self.tau0 * (q["rc"] * q["P"] + EPS * q["g"] ** 2)))


def make_mesh(Rout, h0, Lfine, grow=1.08, p=1):
    """Element end points: uniform h0 on [0, Lfine], geometric growth beyond; a node at Lg kinks handled by caller."""
    nf = int(round(Lfine / h0))
    x = [k * h0 for k in range(nf + 1)]
    h = h0
    while x[-1] < Rout - 1e-12:
        h *= grow
        x.append(min(x[-1] + h, Rout))
    return x


def shape(p, xi):
    if p == 1:
        return [0.5 * (1 - xi), 0.5 * (1 + xi)], [-0.5, 0.5]
    return ([0.5 * xi * (xi - 1), 1 - xi * xi, 0.5 * xi * (xi + 1)], [xi - 0.5, -2 * xi, xi + 0.5])


class Banded:
    """Banded matrix with half bandwidth bw, LU without pivoting."""

    def __init__(self, n, bw):
        self.n, self.bw = n, bw
        self.a = [[0.0] * (2 * bw + 1) for _ in range(n)]  # a[i][j-i+bw]

    def add(self, i, j, v):
        self.a[i][j - i + self.bw] += v

    def lu(self):
        n, bw, a = self.n, self.bw, self.a
        for k in range(n):
            piv = a[k][bw]
            hi = min(n, k + bw + 1)
            for i in range(k + 1, hi):
                aik = a[i][k - i + bw]
                if aik == 0.0:
                    continue
                m = aik / piv
                a[i][k - i + bw] = m
                ri, rk = a[i], a[k]
                for j in range(k + 1, hi):
                    ri[j - i + bw] -= m * rk[j - k + bw]

    def solve(self, b):
        n, bw, a = self.n, self.bw, self.a
        y = list(b)
        for i in range(n):
            lo = max(0, i - bw)
            s = y[i]
            ai = a[i]
            for j in range(lo, i):
                s -= ai[j - i + bw] * y[j]
            y[i] = s
        for i in range(n - 1, -1, -1):
            hi = min(n, i + bw + 1)
            s = y[i]
            ai = a[i]
            for j in range(i + 1, hi):
                s -= ai[j - i + bw] * y[j]
            y[i] = s / ai[bw]
        return y


class Sparse:
    def __init__(self, n):
        self.rows = [dict() for _ in range(n)]

    def add(self, i, j, v):
        d = self.rows[i]
        d[j] = d.get(j, 0.0) + v

    def freeze(self):
        self.r = [(list(d.keys()), list(d.values())) for d in self.rows]

    def mv(self, x):
        out = []
        for js, vs in self.r:
            s = 0.0
            for j, v in zip(js, vs):
                s += v * x[j]
            out.append(s)
        return out


def default_source(a):
    """Q(r) with int Q 2 pi r dr = 1 (unit line power); compact bump of radius a."""
    def q(r):
        return 2.0 / (math.pi * a * a) * (1.0 - (r / a) ** 2) if r < a else 0.0
    return q


class Solver:
    def __init__(self, props, nodes, p=1, tau0=0.02, tau1=0.05, a_src=0.05, nq=3, coupled=True, q=None):
        self.pr, self.p, self.tau0, self.tau1 = props, p, tau0, tau1
        props.tau0 = tau0 if tau0 > 0 else props.tau0
        xe = nodes
        ne = len(xe) - 1
        self.ne = ne
        # global node coordinates
        xs = []
        for e in range(ne):
            for kk in range(p):
                xs.append(xe[e] + (xe[e + 1] - xe[e]) * kk / p)
        xs.append(xe[-1])
        self.x = xs
        nn = len(xs)
        self.nn = nn
        self.nd = 2 * nn
        qf = q or default_source(a_src)
        K, G, M, Mth, D, Kt = (Sparse(nn) for _ in range(6))
        Qv = [0.0] * nn
        gp, gw = GL[5] if (nq == 5 or p == 2) else GL[3]
        coup = 1.0 if coupled else 0.0
        for e in range(ne):
            ids = [e * p + kk for kk in range(p + 1)]
            xa, xb = xe[e], xe[e + 1]
            J = 0.5 * (xb - xa)
            for g_, w_ in zip(gp, gw):
                xi = g_
                r = xa + J * (xi + 1)
                N, dN = shape(p, xi)
                dN = [d / J for d in dN]
                q_ = props.ratios(r)
                wt = w_ * J * r
                for i, ii in enumerate(ids):
                    Qv[ii] += wt * N[i] * qf(r)
                    for j, jj in enumerate(ids):
                        K.add(ii, jj, wt * (dN[i] * (q_["P"] * dN[j] + q_["L"] * N[j] / r)
                                            + N[i] / r * (q_["L"] * dN[j] + q_["P"] * N[j] / r)))
                        G.add(ii, jj, coup * D1 * wt * q_["g"] * (dN[i] + N[i] / r) * N[j])
                        M.add(ii, jj, wt * q_["rho"] * N[i] * N[j])
                        Mth.add(ii, jj, wt * q_["rc"] * N[i] * N[j])
                        D.add(ii, jj, coup * D2 * wt * q_["g"] * N[i] * (dN[j] + N[j] / r))
                        Kt.add(ii, jj, wt * q_["k"] * dN[i] * dN[j])
        for m_ in (K, G, M, Mth, D, Kt):
            m_.freeze()
        self.K, self.G, self.M, self.Mth, self.D, self.Kt, self.Q = K, G, M, Mth, D, Kt, Qv
        self.coup = coup

    # --- indices: u_i -> 2i, theta_i -> 2i+1 ---
    def factor(self, dt):
        nn, p = self.nn, self.p
        tau0, tau1 = self.tau0, self.tau1
        a = 0.5 * dt * (0.5 * dt + tau1)
        beta = dt / (2 * tau0) if tau0 > 0 else None
        cb = (beta / (1 + beta)) if tau0 > 0 else 1.0
        bw = 2 * p + 1
        A = Banded(2 * nn, bw)
        for i in range(nn):
            if i == 0 or i == nn - 1:
                A.add(2 * i, 2 * i, 1.0)          # u(0)=0, u(R)=0
            else:
                for j, v in self.M.rows[i].items():
                    if j == 0 or j == nn - 1:
                        continue
                    A.add(2 * i, 2 * j, v)
                for j, v in self.K.rows[i].items():
                    if j == 0 or j == nn - 1:
                        continue
                    A.add(2 * i, 2 * j, a * v)
                for j, v in self.G.rows[i].items():
                    if j == nn - 1:
                        continue
                    A.add(2 * i, 2 * j + 1, -a * v)
            if i == nn - 1:
                A.add(2 * i + 1, 2 * i + 1, 1.0)   # theta(R)=0
            else:
                for j, v in self.D.rows[i].items():
                    if j == 0 or j == nn - 1:
                        continue
                    A.add(2 * i + 1, 2 * j, 2.0 / dt * v)
                for j, v in self.Mth.rows[i].items():
                    if j == nn - 1:
                        continue
                    A.add(2 * i + 1, 2 * j + 1, 2.0 / dt * v)
                for j, v in self.Kt.rows[i].items():
                    if j == nn - 1:
                        continue
                    A.add(2 * i + 1, 2 * j + 1, cb * v)
        A.lu()
        return A, a, beta

    def run(self, dt, tend, obs_r=(), snap_t=(), sample_r=None, record_energy=False):
        nn = self.nn
        A, a, beta = self.factor(dt)
        tau0 = self.tau0
        u = [0.0] * nn
        th = [0.0] * nn
        m = [0.0] * nn
        g = [0.0] * nn
        f = [0.0] * nn
        R = list(self.Q)               # R_0 = Q (source on at t=0+)
        R[nn - 1] = 0.0
        if tau0 == 0:
            g = list(R)
        nsteps = int(round(tend / dt))
        obs = [self.locate(r) for r in obs_r]
        hist = [[] for _ in obs]
        times = [0.0]
        for k, o in enumerate(obs):
            hist[k].append(self.fields_at(o, u, th))
        snaps = {}
        snap_idx = {}
        for t in snap_t:
            for dn in (-1, 0, 1):
                snap_idx.setdefault(int(round(t / dt)) + dn, []).append((dn, t))
        sample = [self.locate(r) for r in sample_r] if sample_r else None
        raw = {}
        energy = []
        one = None
        for n in range(1, nsteps + 1):
            rhs = [0.0] * (2 * nn)
            for i in range(1, nn - 1):
                rhs[2 * i] = dt * m[i] + 2 * a * f[i]
            if tau0 > 0:
                for i in range(nn - 1):
                    rhs[2 * i + 1] = g[i] + ((1 - beta) * g[i] + 2 * beta * R[i]) / (1 + beta)
            else:
                for i in range(nn - 1):
                    rhs[2 * i + 1] = 2 * R[i]
            sol = A.solve(rhs)
            du = sol[0::2]
            dth = sol[1::2]
            Kdu = self.K.mv(du)
            Gdth = self.G.mv(dth)
            Ktdth = self.Kt.mv(dth)
            for i in range(nn):
                fn = f[i]
                f[i] = fn - Kdu[i] + Gdth[i]
                m[i] += 0.5 * dt * (fn + f[i])
                u[i] += du[i]
                th[i] += dth[i]
                Rn = R[i]
                R[i] = Rn - Ktdth[i]
                if tau0 > 0:
                    g[i] = ((1 - beta) * g[i] + beta * (Rn + R[i])) / (1 + beta)
                else:
                    g[i] = R[i]
            # boundary rows: the Dirichlet nodes carry no source/heat content
            f[0] = f[0]
            t = n * dt
            times.append(t)
            for k, o in enumerate(obs):
                hist[k].append(self.fields_at(o, u, th))
            if n in snap_idx:
                for dn, tt in snap_idx[n]:
                    raw[(tt, dn)] = ([self.fields_at(o, u, th) for o in sample] if sample
                                     else self.profile(u, th))
            if record_energy:
                energy.append((t, self.heat_content(u, th)))
        for tt in snap_t:
            a_, b_, c_ = raw[(tt, -1)], raw[(tt, 0)], raw[(tt, 1)]
            rows = []
            for x0, x1, x2 in zip(a_, b_, c_):
                off = 1 if not sample else 0
                rr = (x1[0],) if not sample else ()
                v = x1[off:]
                d = [(x2[off + j] - x0[off + j]) / (2 * dt) for j in range(4)]
                rows.append(rr + (v[0], v[1], v[2] + self.tau1 * d[2], v[3] + self.tau1 * d[3]))
            snaps[tt] = rows
        hist = [stress_from_S(h_, dt, self.tau1) for h_ in hist]
        return dict(times=times, hist=hist, snaps=snaps, energy=energy, u=u, th=th)

    # --- post-processing ---
    def locate(self, r):
        xe = [self.x[e * self.p] for e in range(self.ne)] + [self.x[-1]]
        lo, hi = 0, self.ne - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if xe[mid + 1] < r:
                lo = mid + 1
            else:
                hi = mid
        e = lo
        xa, xb = xe[e], xe[e + 1]
        xi = 2 * (r - xa) / (xb - xa) - 1
        N, dN = shape(self.p, xi)
        J = 0.5 * (xb - xa)
        return (e, r, N, [d / J for d in dN])

    def fields_at(self, o, u, th):
        e, r, N, dN = o
        p = self.p
        ids = range(e * p, e * p + p + 1)
        uu = sum(N[i] * u[j] for i, j in enumerate(ids))
        ur = sum(dN[i] * u[j] for i, j in enumerate(ids))
        tt = sum(N[i] * th[j] for i, j in enumerate(ids))
        q = self.pr.ratios(r)
        Srr = q["P"] * ur + q["L"] * uu / r - D1 * q["g"] * tt
        Stt = q["L"] * ur + q["P"] * uu / r - D1 * q["g"] * tt
        return (tt, uu, Srr, Stt)

    def profile(self, u, th):
        """fields at the element mid-points"""
        out = []
        xe = [self.x[e * self.p] for e in range(self.ne)] + [self.x[-1]]
        for e in range(self.ne):
            r = 0.5 * (xe[e] + xe[e + 1])
            o = self.locate(r)
            out.append((r,) + self.fields_at(o, u, th))
        return out

    def heat_content(self, u, th):
        """int (a_rc theta + d2 a_g e) r dr  = 1^T Mth theta + 1^T D u  (unit-source normalisation: times 2 pi)"""
        s = 0.0
        a = self.Mth.mv(th)
        b = self.D.mv(u)
        return sum(a[:-1]) + sum(b)


def stress_from_S(hist, dt, tau1):
    """sigma = S + tau1 dS/dt (central differences, one-sided at the ends); hist: list of (th,u,Srr,Stt)."""
    n = len(hist)
    out = []
    for i in range(n):
        if i == 0:
            d = [(hist[1][j] - hist[0][j]) / dt for j in range(4)]
        elif i == n - 1:
            d = [(hist[i][j] - hist[i - 1][j]) / dt for j in range(4)]
        else:
            d = [(hist[i + 1][j] - hist[i - 1][j]) / (2 * dt) for j in range(4)]
        out.append((hist[i][0], hist[i][1], hist[i][2] + tau1 * d[2], hist[i][3] + tau1 * d[3]))
    return out


def laplace_fields(S, s, obs, tstep=None):
    """Laplace-domain FE solution at complex s for a unit step line source (Q-hat = Q/s).
    Returns list over observation points of (theta, u, sigma_rr, sigma_tt) transforms."""
    nn, p = S.nn, S.p
    tau0, tau1 = S.tau0, S.tau1
    pp = 1.0 + tau1 * s
    ps = 1.0 + tau0 * s
    A = Banded(2 * nn, 2 * p + 1)
    last = nn - 1
    for i in range(nn):
        if i == 0 or i == last:
            A.add(2 * i, 2 * i, 1.0)
        else:
            for j, v in S.M.rows[i].items():
                if 0 < j < last:
                    A.add(2 * i, 2 * j, s * s * v)
            for j, v in S.K.rows[i].items():
                if 0 < j < last:
                    A.add(2 * i, 2 * j, pp * v)
            for j, v in S.G.rows[i].items():
                if j < last:
                    A.add(2 * i, 2 * j + 1, -pp * v)
        if i == last:
            A.add(2 * i + 1, 2 * i + 1, 1.0)
        else:
            for j, v in S.D.rows[i].items():
                if 0 < j < last:
                    A.add(2 * i + 1, 2 * j, ps * s * v)
            for j, v in S.Mth.rows[i].items():
                if j < last:
                    A.add(2 * i + 1, 2 * j + 1, ps * s * v)
            for j, v in S.Kt.rows[i].items():
                if j < last:
                    A.add(2 * i + 1, 2 * j + 1, v)
    A.lu()
    rhs = [0j] * (2 * nn)
    for i in range(nn - 1):
        rhs[2 * i + 1] = S.Q[i] / s
    sol = A.solve(rhs)
    u = sol[0::2]
    th = sol[1::2]
    out = []
    for o in obs:
        f = S.fields_at(o, u, th)
        out.append((f[0], f[1], pp * f[2], pp * f[3]))
    return out
