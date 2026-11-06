"""Galerkin FE (linear elements) + BDF2 time stepping for the layered bioheat thermoelastic slab in SI units.

Quasi-static elasticity is eliminated analytically (sigma_xx = 0, u_x = beta*theta/c11), which leaves one
temperature unknown per node and a tridiagonal system.  Energy equation (all models):

   C_eff (D th + (tauq+tau0) D^2 th) + (1 + tauq D) [omega(th) th] - (1 + tauq D) Q = k th_xx + k* v_xx,  v_t = th

with D the BDF2 operator.  Pennes: tauq = tau0 = 0, k* = 0.  CV/MGT-type: tauq > 0.  MGL: tau0 > 0.
Arrhenius integrals are advanced with composite Simpson sub-stepping on the piecewise-linear temperature."""
import math
import model

RG = model.RGAS


def make_mesh(h, L, dx):
    n1 = max(2, int(round(h / dx)))
    xs = [h * i / n1 for i in range(n1 + 1)]
    z1 = min(L - h, 0.010)
    n2 = max(2, int(round(z1 / dx)))
    xs += [h + z1 * i / n2 for i in range(1, n2 + 1)]
    rest = L - h - z1
    if rest > 1e-12:
        n3 = max(2, int(round(rest / (4 * dx))))
        xs += [h + z1 + rest * i / n3 for i in range(1, n3 + 1)]
    return xs, n1


def arrhenius_step(ta, tb, T0, A, E, dt, nsub=4):
    """increment of the damage integral over one step, temperature rise linear from ta to tb (K), composite Simpson."""
    s = 0.0
    for m in range(nsub + 1):
        T = T0 + ta + (tb - ta) * m / nsub
        s += A * math.exp(-E / (RG * T)) * (1 if m in (0, nsub) else (4 if m % 2 else 2))
    return s * dt / (3.0 * nsub)


def kstar_eff(P, c):
    """k* of a layer: literal source value if P['kstar_lit'] else eta*k/tauq (stable MGT, see paper)."""
    if P.get("kstar_lit"):
        return c["kstar"]
    return P.get("eta", 0.5) * c["k"] / P["tauq"]


def thomas(a, b, c, d):
    """a: sub, b: diag, c: super (len n; a[0], c[-1] unused)."""
    n = len(b)
    cp = [0.0] * n
    dp = [0.0] * n
    bet = b[0]
    cp[0] = c[0] / bet
    dp[0] = d[0] / bet
    for i in range(1, n):
        bet = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / bet if i < n - 1 else 0.0
        dp[i] = (d[i] - a[i] * dp[i - 1]) / bet
    x = [0.0] * n
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


def fbar_array(des, nstep, dt):
    tp, per, Np, I = des["tp"], des["per"], int(des["Np"]), 1.0

    def F(t):
        k = min(int(t // per + 1e-12), Np)
        v = k * tp
        if k < Np:
            v += min(t - k * per, tp)
        return v
    return [0.0] + [(F(n * dt) - F((n - 1) * dt)) / dt for n in range(1, nstep + 1)]


def laser_load(P, xs, ne):
    """nodal integrals of phi_i * g(x) with the Gardner profile times mu_a (per unit I0)."""
    ls = model.laser_shape(P["las"])
    mua = P["las"]["mua"]
    gf = lambda x: mua * (ls["B1"] * math.exp(-ls["l1"] * x / ls["delta"]) - ls["B2"] * math.exp(-ls["l2"] * x / ls["delta"]))
    gp = [(-math.sqrt(0.6), 5 / 9.0), (0.0, 8 / 9.0), (math.sqrt(0.6), 5 / 9.0)]
    q = [0.0] * len(xs)
    for e in range(ne):
        a, b = xs[e], xs[e + 1]
        le = b - a
        for xi, w in gp:
            x = 0.5 * (a + b) + 0.5 * le * xi
            gv = gf(x) * 0.5 * le * w
            f = (x - a) / le
            q[e] += gv * (1 - f)
            q[e + 1] += gv * f
    return q


class Res:
    pass


def run(P, des, dx=2.5e-4, dt=0.1, picard=1, tol=1e-7, maxit=30, nsub=4, keep=True, Tend=None):
    h, L, T0 = P["h"], P["L"], P["T0"]
    xs, n1 = make_mesh(h, L, dx)
    nn = len(xs)
    ne = nn - 1
    li = [0 if e < n1 else 1 for e in range(ne)]
    le_ = [xs[e + 1] - xs[e] for e in range(ne)]
    if Tend is None:
        Tend = des.get("Tend", P.get("Teval", 120.0))
    nstep = int(round(Tend / dt))
    tq, t0 = P["tauq"], P["tau0"]
    tau = tq + t0
    d = [1.5 / dt, -2.0 / dt, 0.5 / dt]
    d2 = [0.0] * 5
    for i in range(3):
        for j in range(3):
            d2[i + j] += d[i] * d[j]
    gM = d[0] + tau * d2[0]
    kson = P["kstar_on"]
    Lc = P["lay"]
    # constant matrices
    MCd = [0.0] * nn; MCo = [0.0] * ne
    Kd = [0.0] * nn; Ko = [0.0] * ne      # k + k* dt/2   (matrix)
    Ksd = [0.0] * nn; Kso = [0.0] * ne    # k*            (rhs)
    wl = [[0.0, 0.0] for _ in range(nn)]  # lumped perfusion weight per node: [left-element, right-element]
    ll = [[0, 0] for _ in range(nn)]
    for e in range(ne):
        c = Lc[li[e]]
        le = le_[e]
        m = c["C"] * le / 6.0
        MCd[e] += 2 * m; MCd[e + 1] += 2 * m; MCo[e] += m
        kk = c["k"] / le
        ks = (kstar_eff(P, c) / le) if kson else 0.0
        kmat = kk + ks * dt / 2
        Kd[e] += kmat; Kd[e + 1] += kmat; Ko[e] -= kmat
        Ksd[e] += ks; Ksd[e + 1] += ks; Kso[e] -= ks
        wl[e][1] = c["om0"] * le / 2.0; ll[e][1] = li[e]
        wl[e + 1][0] = c["om0"] * le / 2.0; ll[e + 1][0] = li[e]
    base_b = [gM * MCd[i] + Kd[i] for i in range(nn)]
    base_o = [gM * MCo[i] + Ko[i] for i in range(ne)]
    q0 = laser_load(P, xs, ne)
    I0 = des["I0"]
    qv = [I0 * v for v in q0]
    fb = fbar_array(des, nstep, dt)
    arr = P["arr"]
    A0, E0 = arr[0]["A"], arr[0]["Ea"]
    A1, E1 = arr[1]["A"], arr[1]["Ea"]
    kv = P["kv"]
    th = [[0.0] * nn]
    z = [0.0] * nn
    Wh = [z, z]                 # lumped weighted perfusion history W_{n-1}, W_{n-2}
    vst = [0.0] * nn            # v_{n-1}
    OmT = [0.0] * nn
    OmN = [0.0] * nn
    OmTh = [list(OmT)] if keep else None
    OmNh = [list(OmN)] if keep else None
    pf = model.perfusion_factor
    iters = []

    def lump(thv, OmTv, OmNv):
        """returns (diag perfusion weight, weighted W) for a temperature vector"""
        pd = [0.0] * nn
        for i in range(nn):
            t = thv[i]
            s = 0.0
            for side in (0, 1):
                w = wl[i][side]
                if w:
                    lay = ll[i][side]
                    s += w * pf(P, lay, t, OmTv[i] if lay == 0 else OmNv[i])
            pd[i] = s
        return pd

    for n in range(1, nstep + 1):
        prev = th[n - 1]
        prev2 = th[n - 2] if n >= 2 else z
        prev3 = th[n - 3] if n >= 3 else z
        prev4 = th[n - 4] if n >= 4 else z
        hist = (prev, prev2, prev3, prev4)
        cj = [d[1] + tau * d2[1], d[2] + tau * d2[2], tau * d2[3], tau * d2[4]]
        S = [cj[0] * prev[i] + cj[1] * prev2[i] + cj[2] * prev3[i] + cj[3] * prev4[i] for i in range(nn)]
        rhs = [0.0] * nn
        for i in range(nn):
            v = MCd[i] * S[i]
            if i > 0:
                v += MCo[i - 1] * S[i - 1]
            if i < nn - 1:
                v += MCo[i] * S[i + 1]
            rhs[i] = -v
        if tq:
            W1, W2 = Wh[0], Wh[1]
            for i in range(nn):
                rhs[i] -= tq * (d[1] * W1[i] + d[2] * W2[i])
        f1 = fb[n - 1] if n >= 1 else 0.0
        f2 = fb[n - 2] if n >= 2 else 0.0
        fe = fb[n] + tq * (d[0] * fb[n] + d[1] * f1 + d[2] * f2)
        if fe != 0.0:
            for i in range(nn):
                rhs[i] += qv[i] * fe
        if kson:
            vs = [vst[i] + 0.5 * dt * prev[i] for i in range(nn)]
            for i in range(nn):
                v = Ksd[i] * vs[i]
                if i > 0:
                    v += Kso[i - 1] * vs[i - 1]
                if i < nn - 1:
                    v += Kso[i] * vs[i + 1]
                rhs[i] -= v
        guess = [2 * prev[i] - prev2[i] for i in range(nn)] if n >= 2 else list(prev)
        cur = guess
        for it in range(1, (maxit if picard > 1 else 1) + 1):
            pd = lump(cur, OmT, OmN)
            b = [base_b[i] + (1 + tq * d[0]) * pd[i] for i in range(nn)]
            a = [0.0] + base_o[:]
            c = base_o[:] + [0.0]
            r = rhs[:]
            b[-1] = 1.0; a[-1] = 0.0; r[-1] = 0.0
            x = thomas(a, b, c, r)
            diff = max(abs(x[i] - cur[i]) for i in range(nn))
            cur = x
            if picard <= 1 or diff < tol:
                break
        iters.append(it)
        pd = lump(cur, OmT, OmN)
        # recompute weighted W with the converged temperature
        Wn = [0.0] * nn
        for i in range(nn):
            t = cur[i]
            s = 0.0
            for side in (0, 1):
                w = wl[i][side]
                if w:
                    lay = ll[i][side]
                    s += w * pf(P, lay, t, OmT[i] if lay == 0 else OmN[i]) * t
            Wn[i] = s
        Wh = [Wn, Wh[0]]
        th.append(cur)
        if kson:
            vst = [vst[i] + 0.5 * dt * (prev[i] + cur[i]) for i in range(nn)]
        # Arrhenius integrals, composite Simpson with nsub sub-intervals (piecewise linear temperature)
        for i in range(nn):
            ta, tb = prev[i], cur[i]
            if ta < 3.0 and tb < 3.0:
                continue
            if i <= n1:
                OmT[i] += arrhenius_step(ta, tb, T0, A0, E0, dt, nsub)
            if i >= n1:
                OmN[i] += arrhenius_step(ta, tb, T0, A1, E1, dt, nsub)
        if keep:
            OmTh.append(list(OmT)); OmNh.append(list(OmN))
    R = Res()
    R.P, R.des, R.xs, R.n1, R.dt, R.nstep, R.th = P, des, xs, n1, dt, nstep, th
    R.OmT, R.OmN, R.OmTh, R.OmNh, R.iters = OmT, OmN, OmTh, OmNh, iters
    R.li, R.le = li, le_
    return R


def stress_hist(R):
    """in-plane (laterally constrained) stress at nodes: tumour-side and normal-side arrays per step [Pa]."""
    P = R.P
    t1 = P["tau1"]
    dt = R.dt
    sT, sN = P["lay"][0]["sl"], P["lay"][1]["sl"]
    nn = len(R.xs)
    out = []
    z = [0.0] * nn
    for n in range(len(R.th)):
        a = R.th[n]
        b = R.th[n - 1] if n >= 1 else z
        c = R.th[n - 2] if n >= 2 else z
        row = []
        for i in range(nn):
            Dth = (1.5 * a[i] - 2.0 * b[i] + 0.5 * c[i]) / dt
            val = a[i] + t1 * Dth
            row.append(val)
        out.append(row)
    return out, sT, sN


def metrics(R, cov=1.0):
    P = R.P
    xs, n1, nn = R.xs, R.n1, len(R.xs)
    T0 = P["T0"]
    # peak temperature
    Tpk = (-1.0, 0, 0)
    for n, a in enumerate(R.th):
        m = max(a)
        if m > Tpk[0]:
            Tpk = (m, a.index(m), n)
    thmax, ipk, npk = Tpk
    # stress
    gam, sT, sN = stress_hist(R)
    smax = -1e30; smin = 1e30
    sif_T = [0.0, 0.0]; sif_N = [0.0, 0.0]
    sloc = None
    for n, row in enumerate(gam):
        for i in range(nn):
            if i <= n1:
                s = -sT * row[i]
                if i == n1:
                    sif_T = [min(sif_T[0], s), max(sif_T[1], s)]
            if i >= n1:
                s = -sN * row[i]
                if i == n1:
                    sif_N = [min(sif_N[0], s), max(sif_N[1], s)]
            if i < n1:
                s = -sT * row[i]
            if s > smax: smax = s
            if s < smin:
                smin = s
                sloc = (xs[i], n * R.dt)
    # kill depth: contiguous from surface where OmT >= Om_c (linear interpolation of Omega)
    Oc = P["Om_c"]
    kd = 0.0
    for i in range(n1 + 1):
        if R.OmT[i] >= Oc:
            kd = xs[i]
        else:
            if i > 0:
                a, b = R.OmT[i - 1], R.OmT[i]
                kd = xs[i - 1] + (xs[i] - xs[i - 1]) * (a - Oc) / (a - b) if a > b else xs[i - 1]
            break
    minOm = min(R.OmT[i] for i in range(n1 + 1) if xs[i] <= cov * P['h'] + 1e-12)
    # collateral damage in the normal tissue
    JO = 0.0; JF = 0.0
    for i in range(n1, nn - 1):
        w = xs[i + 1] - xs[i]
        JO += 0.5 * w * (R.OmN[i] + R.OmN[i + 1])
        JF += 0.5 * w * ((1 - math.exp(-min(R.OmN[i], 700.0))) + (1 - math.exp(-min(R.OmN[i + 1], 700.0))))
    dd = 0.0
    for i in range(n1, nn):
        if R.OmN[i] >= 1.0:
            dd = xs[i] - xs[n1]
        else:
            break
    return dict(thmax=thmax, Tmax=T0 + thmax, xpk=xs[ipk], tpk=npk * R.dt,
                smax=smax, smin=smin, sabs=max(abs(smax), abs(smin)), sloc=sloc,
                sifT=sif_T, sifN=sif_N, kd=kd, minOmT=minOm, OmT_h=R.OmT[n1], OmN_h=R.OmN[n1],
                JO=JO, JF=JF, dd=dd, OmN_max=max(R.OmN[n1:]), OmT_max=max(R.OmT[: n1 + 1]))
