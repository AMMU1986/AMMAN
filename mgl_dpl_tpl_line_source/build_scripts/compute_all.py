"""Run every computation that feeds the figures/tables; writes results.json."""
import json
import math
import os
import sys
import time
from multiprocessing import Pool

import mgl
import model as M
from model import Model
import fd2

HERE = os.path.dirname(os.path.abspath(__file__))
EPS = M.EPS
TQ, TT, TV, KS, T1 = 0.02, 0.012, 0.03, 0.1, 0.05

MODELS = {
    "Fourier": dict(name="Fourier", tq=0.0, order=1),
    "GL": dict(name="GL", flavor="GL", tq=TQ),
    "MGL-LS": dict(name="MGL-LS", tq=TQ, order=1),
    "MGL-DPL1": dict(name="MGL-DPL1", tq=TQ, tT=TT, order=1),
    "MGL-DPL2": dict(name="MGL-DPL2", tq=TQ, tT=TT, order=2),
    "MGL-TPL": dict(name="MGL-TPL", tq=TQ, tT=TT, tv=TV, K=KS, order=2),
    "MGL-TPL1": dict(name="MGL-TPL1", tq=TQ, tT=0.0, tv=TV, K=KS, order=1),
    "DPL2-unstable": dict(name="DPL2-unstable", tq=TQ, tT=0.006, order=2),
}
RS_PROF = [round(0.05 + 0.01 * i, 3) for i in range(0, 76)]       # 0.05 .. 0.80
TS_HIST = [round(0.004 * i, 4) for i in range(1, 76)]              # 0.004 .. 0.300
R_OBS = 0.3
NW = 12


def mk(**kw):
    return Model(**kw)


def prof_profile(args):
    """theta,u,srr,spp over RS_PROF at time t."""
    kw, prof, t, N = args
    out = M.invert_line(mk(**kw), tuple(prof), RS_PROF, t, N=N, nwynn=NW)
    return out


def prof_history(args):
    kw, prof, N = args
    m = mk(**kw)
    res = []
    for t in TS_HIST:
        res.append(M.invert_line(m, tuple(prof), [R_OBS], t, N=N, nwynn=NW)[0])
    return res


def moving(args):
    kw, prof, V, t, y, xs, N, h, xim = args
    m = mk(**kw)
    out = M.invert_moving(m, tuple(prof), xs, y, t, V, N=N, nwynn=NW, h=h, xi_max=xim)
    return [[v for v in row] for row in out]


def asym(_):
    res = {}
    xis = [0.1, 0.3, 1, 3, 10, 30, 100, 300, 1000, 3000]
    for k, kw in MODELS.items():
        m = mk(**kw)
        ex = M.asymptotic_exponents(m, 1e5, 1e6)
        mm = m.roots(complex(1e6))
        g = max(M.max_growth(m, xi) if k != "GL" else 0.0 for xi in xis)
        res[k] = dict(exp=ex, c1=1e6 / mm[0].real, ratio2=abs(mm[1]) / math.sqrt(1e6), growth=g)
    # |m|/s curves
    ss = [10 ** (1 + 0.25 * i) for i in range(0, 17)]
    curves = {}
    for k in ("MGL-LS", "MGL-DPL1", "MGL-DPL2", "MGL-TPL", "GL"):
        m = mk(**MODELS[k])
        c1, c2 = [], []
        for s in ss:
            a, b = m.roots(complex(s))
            c1.append(abs(a) / s)
            c2.append(abs(b) / math.sqrt(s))
        curves[k] = dict(c1=c1, c2=c2)
    res["_curves"] = dict(s=ss, curves=curves)
    xl = [0.03, 0.1, 0.3, 1, 3, 10, 30, 100, 300, 1000, 3000, 10000]

    def gr(tv, K):
        mm = Model("t", tq=TQ, tT=TT, tv=tv, K=K, order=2)
        return max(M.max_growth(mm, x) for x in xl)
    thr = {}
    for K in (0.1, 0.5, 2.0):
        lo, hi = 0.0, 5.0
        for _ in range(14):
            mid = 0.5 * (lo + hi)
            if gr(mid, K) > 1e-6:
                hi = mid
            else:
                lo = mid
        thr[str(K)] = [lo, lo * K]
    res["_tpl_threshold"] = thr
    res["_tpl_unstable_examples"] = {"tv1_K0.5": gr(1.0, 0.5), "tv3_K0.5": gr(3.0, 0.5), "tv0.5_K0.5": gr(0.5, 0.5)}
    return res


def fd_case(_):
    m = mk(**MODELS["MGL-LS"])
    out = {}
    for tag, prof, t in (("rect", ("rect", 0.03), 0.05), ("step", ("step",), 0.05)):
        rn, th, un, srr, spp, rce, dt, ns = fd2.fd_line(m, prof, t)
        ids = list(range(25, 281, 5))
        rs = [rn[i] for i in ids]
        ex = fd2.invert_disc(m, prof, rs, t, rce, N=3000, nwynn=NW)
        out[tag] = dict(r=rs, fd=[[th[i], un[i], srr[i], spp[i]] for i in ids],
                        lt=[list(e) for e in ex], rc_eff=rce, dt=dt, nsteps=ns, prof=list(prof), t=t)
    return out


def checks(_):
    out = {}
    m0 = mk(**MODELS["Fourier"])
    # (1) Fourier, eps = 0, versus exact E1
    fo = Model("F0", t1=0.0, tq=0.0, tT=0.0, eps=0.0)

    def E1(x):
        if x < 1:
            s = -0.5772156649015329 - math.log(x)
            t = 1.0
            for k in range(1, 60):
                t *= -x / k
                s -= t / k
            return s
        f = 0.0
        for k in range(60, 0, -1):
            f = k / (1 + k / (x + f))
        return math.exp(-x) / (x + f)
    err = 0.0
    for r in (0.05, 0.2, 0.5):
        for t in (0.05, 0.1, 0.5):
            v = M.invert_line(fo, ("step",), [r], t, N=2000)[0][0]
            ex = E1(r * r / (4 * t)) / (4 * math.pi)
            err = max(err, abs(v - ex) / ex)
    out["fourier_E1_maxrel"] = err
    # (2) DPL (tT -> 0, order 1, tq = tau0) vs MGL-LS ; (3) tq = tT -> Fourier
    rs = [0.1, 0.2, 0.3, 0.4, 0.42]
    ls = M.invert_line(mk(**MODELS["MGL-LS"]), ("step",), rs, 0.06, N=3000, nwynn=NW)
    d1 = M.invert_line(Model("d", tq=TQ, tT=1e-9, order=1), ("step",), rs, 0.06, N=3000, nwynn=NW)
    mx = max(abs(a[0]) for a in ls)
    out["dpl_tT0_vs_ls"] = max(abs(a[0] - b[0]) for a, b in zip(ls, d1)) / mx
    fo_ = M.invert_line(Model("Fp", tq=0.0, order=1, src="phys"), ("step",), rs, 0.06, N=3000, nwynn=NW)
    eqd = M.invert_line(Model("e", tq=TQ, tT=TQ, order=1, src="phys"), ("step",), rs, 0.06, N=3000, nwynn=NW)
    out["dpl_tq_eq_tT_vs_fourier"] = max(abs(a[0] - b[0]) for a, b in zip(fo_, eqd)) / max(abs(a[0]) for a in fo_)
    # (4) TPL -> DPL2 when K = 0
    dd = M.invert_line(mk(**MODELS["MGL-DPL2"]), ("step",), rs, 0.06, N=3000, nwynn=NW)
    tt = M.invert_line(Model("t", tq=TQ, tT=TT, tv=TV, K=0.0, order=2), ("step",), rs, 0.06, N=3000, nwynn=NW)
    out["tpl_K0_vs_dpl2"] = max(abs(a[0] - b[0]) for a, b in zip(dd, tt))
    # (5) Durbin truncation: N vs N/2 for each model at r = 0.2, 0.4 and t = 0.06
    tr = {}
    for k in ("MGL-LS", "MGL-DPL2", "MGL-TPL", "MGL-DPL1"):
        m = mk(**MODELS[k])
        row = []
        for N in (500, 1000, 2000, 4000, 8000):
            f = lambda s: M.line_fields(m, s, [0.2, 0.4], ("step",))
            full, half = mgl.durbin(f, 0.06, 4, 2, N=N)
            row.append([max(abs(full[i][0] - half[i][0]) / max(abs(full[i][0]), 1e-30) for i in range(2)),
                        max(abs(full[i][3] - half[i][3]) / max(abs(full[i][3]), 1e-30) for i in range(2))])
        tr[k] = row
    out["truncation"] = tr
    # (6) far-field decay and wavefront location (DPL2 step, t = 0.06)
    for k in ("MGL-LS", "MGL-DPL2", "MGL-TPL"):
        m = mk(**MODELS[k])
        v = M.invert_line(m, ("step",), [0.2, 1.0, 1.5, 2.0], 0.06, N=3000, nwynn=NW)
        out["far_" + k] = [[x for x in row] for row in v]
    # (7) strain-rate smoothing: u, srr, spp across the LS front at t = 0.06
    rs2 = [0.36 + 0.005 * i for i in range(0, 25)]
    for k in ("MGL-LS", "MGL-DPL2"):
        m = mk(**MODELS[k])
        out["front_" + k] = dict(r=rs2, v=M.invert_line(m, ("step",), rs2, 0.06, N=6000, nwynn=NW))
    # (8) V -> 0 moving-source vs axisymmetric reference as a function of quadrature step h
    m = mk(**MODELS["MGL-DPL2"])
    xs = [0.0, 0.3, 0.5]
    y = 0.2
    t = 0.08
    ref = M.invert_line(m, ("step",), [math.hypot(x, y) for x in xs], t, N=1500, nwynn=NW)
    hh = {}
    for h in (1.0, 0.5, 0.25, 0.125):
        mv = M.invert_moving(m, ("step",), xs, y, t, 0.0, N=1500, nwynn=NW, h=h, xi_max=120.0)
        hh[str(h)] = max(abs(a[0].real - b[0]) / abs(b[0]) for a, b in zip(mv, ref))
    out["v0_h"] = hh
    return out


def main():
    t00 = time.time()
    R = {"constants": mgl.constants(), "eps": EPS, "models": MODELS, "rs": RS_PROF, "ts": TS_HIST, "r_obs": R_OBS}
    jobs = []     # (key, func, arg)
    NP = 4000
    # spatial profiles at several times (DPL2 step)
    for t in (0.03, 0.06, 0.09):
        jobs.append(("prof_DPL2_t%g" % t, prof_profile, (MODELS["MGL-DPL2"], ["step"], t, NP)))
    # tau1 study
    for t1 in (0.0, 0.02, 0.05, 0.1):
        kw = dict(MODELS["MGL-DPL2"])
        kw["t1"] = t1
        jobs.append(("prof_t1_%g" % t1, prof_profile, (kw, ["step"], 0.06, NP)))
    # model comparison
    for k in ("Fourier", "GL", "MGL-LS", "MGL-DPL1", "MGL-DPL2", "MGL-TPL", "MGL-TPL1"):
        jobs.append(("prof_model_" + k, prof_profile, (MODELS[k], ["step"], 0.06, NP)))
    # tau_T and tau_q studies
    for tT in (0.0105, 0.012, 0.02, 0.04):
        kw = dict(MODELS["MGL-DPL2"])
        kw["tT"] = tT
        jobs.append(("prof_tT_%g" % tT, prof_profile, (kw, ["step"], 0.06, NP)))
    for tq in (0.01, 0.02, 0.03, 0.04):
        kw = dict(MODELS["MGL-DPL2"])
        kw["tq"] = tq
        kw["tT"] = 0.6 * tq
        jobs.append(("prof_tq_%g" % tq, prof_profile, (kw, ["step"], 0.06, NP)))
    # TPL studies (t = 0.06 and a later time 0.15 to expose K*)
    for tv in (0.0, 0.1, 0.3, 0.5):
        kw = dict(MODELS["MGL-TPL"])
        kw["tv"] = tv
        kw["K"] = 0.5
        jobs.append(("prof_tv_%g" % tv, prof_profile, (kw, ["step"], 0.15, NP)))
    for K in (0.0, 0.1, 0.5, 2.0):
        kw = dict(MODELS["MGL-TPL"])
        kw["K"] = K
        jobs.append(("prof_K_%g" % K, prof_profile, (kw, ["step"], 0.15, NP)))
    # time histories for pulse profiles (DPL2)
    PROFS = {"step": ["step"], "rect": ["rect", 0.04], "exp": ["exp", 0.05], "gamma": ["gamma", 0.03], "sin2": ["sin2", 0.08]}
    for k, p in PROFS.items():
        jobs.append(("hist_DPL2_" + k, prof_history, (MODELS["MGL-DPL2"], p, 3000)))
    for tp in (0.01, 0.03, 0.06, 0.12):
        jobs.append(("hist_rect_%g" % tp, prof_history, (MODELS["MGL-DPL2"], ["rect", tp], 3000)))
    for P in (0.04, 0.08, 0.16):
        jobs.append(("hist_sin2_%g" % P, prof_history, (MODELS["MGL-DPL2"], ["sin2", P], 3000)))
    for k in ("MGL-LS", "MGL-DPL1", "MGL-TPL", "Fourier", "GL"):
        jobs.append(("hist_%s_step" % k, prof_history, (MODELS[k], ["step"], 3000)))
        jobs.append(("hist_%s_rect" % k, prof_history, (MODELS[k], ["rect", 0.04], 3000)))
    # moving source
    xs = [round(-1.0 + 0.05 * i, 3) for i in range(0, 61)]
    R["mov_xs"] = xs
    for V in (0.0, 3.0, 7.7, 12.0):
        jobs.append(("mov_V%g" % V, moving, (MODELS["MGL-DPL2"], ["step"], V, 0.1, 0.2, xs, 2000, 0.25, 100.0)))
    jobs.append(("mov_V3_rect", moving, (MODELS["MGL-DPL2"], ["rect", 0.04], 3.0, 0.1, 0.2, xs, 2000, 0.25, 100.0)))
    jobs.append(("mov_V3_TPL", moving, (MODELS["MGL-TPL"], ["step"], 3.0, 0.1, 0.2, xs, 2000, 0.25, 100.0)))
    jobs.append(("mov_V3_LS", moving, (MODELS["MGL-LS"], ["step"], 3.0, 0.1, 0.2, xs, 2000, 0.25, 100.0)))
    R["prof_defs"] = PROFS
    specials = [("asym", asym, None), ("fd", fd_case, None), ("checks", checks, None)]
    allj = specials + jobs
    # order: heavy first
    heavy = [j for j in allj if j[0].startswith("mov_") or j[0] in ("checks", "fd")]
    light = [j for j in allj if j not in heavy]
    order = heavy + light
    print("jobs", len(order), flush=True)
    with Pool(8) as pool:
        results = pool.imap(_run, [(j[0], j[1].__name__, j[2]) for j in order])
        for (key, val) in results:
            R[key] = val
            print("done", key, "%.0fs" % (time.time() - t00), flush=True)
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(R, fh, default=lambda z: [z.real, z.imag] if isinstance(z, complex) else str(z))
    print("total %.0fs" % (time.time() - t00))


FUNCS = {f.__name__: f for f in (prof_profile, prof_history, moving, asym, fd_case, checks)}


def _run(a):
    key, fname, arg = a
    return key, FUNCS[fname](arg)


if __name__ == "__main__":
    main()
