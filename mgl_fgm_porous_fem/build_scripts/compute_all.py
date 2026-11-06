"""Every computation feeding the manuscript; writes results.json."""
import json, math, os, sys, time
from multiprocessing import Pool
import fem, mgl, exact_uniform as E, model as M

HERE = os.path.dirname(os.path.abspath(__file__))
EPS = mgl.EPS
T0, T1 = 0.02, 0.05
BASE = dict(Rout=3.2, h0=0.0125, Lfine=2.5, grow=1.1, p=2, dt=0.0005, a_src=0.05, tend=0.3)
OBS = [0.3, 0.8]
SNAPS = (0.1, 0.2, 0.3)
SAMPLE = [round(0.05 * k, 3) for k in range(2, 41)]       # 0.10 .. 2.00
TCMP = [round(0.05 + 0.025 * k, 4) for k in range(11)]     # 0.05 .. 0.30


def run_case(spec):
    sp = dict(BASE)
    sp.update(spec.get("num", {}))
    tau0, tau1 = spec.get("tau0", T0), spec.get("tau1", T1)
    pk = dict(spec.get("props", {}))
    pr = fem.Props(tau0=T0, tau1=tau1, **pk)
    nodes = fem.make_mesh(sp["Rout"], sp["h0"], sp["Lfine"], sp["grow"])
    S = fem.Solver(pr, nodes, p=sp["p"], tau0=tau0, tau1=tau1, a_src=sp["a_src"])
    t0 = time.time()
    dt = sp["dt"]
    res = S.run(dt, sp["tend"] + 2 * dt, obs_r=spec.get("obs", OBS), snap_t=spec.get("snaps", SNAPS),
                sample_r=spec.get("sample", SAMPLE), record_energy=True)
    out = dict(name=spec["name"], nn=S.nn, ne=S.ne, dt=dt, cpu=time.time() - t0)
    stride = max(1, int(round(0.0025 / dt)))
    out["t"] = res["times"][::stride]
    out["hist"] = [[list(h) for h in H[::stride]] for H in res["hist"]]
    # values at comparison times
    out["cmp"] = [[list(H[int(round(t / dt))]) for t in TCMP] for H in res["hist"]]
    out["snaps"] = {str(k): [list(r) for r in v] for k, v in res["snaps"].items()}
    # heat-content identity
    errs = []
    for t, e in res["energy"]:
        if t < 0.05 or t > 0.3 + 1e-9:
            continue
        ex = (t - (tau0 * (1 - math.exp(-t / tau0)) if tau0 > 0 else 0.0)) / (2 * math.pi)
        errs.append(abs(e - ex) / ex)
    out["energy_err"] = max(errs)
    # full-field final state at t_end for domain tests
    return out


def exact_hist(args):
    key, q, tau0, tau1, r, ts = args
    return key, [E.invert(t, [r], q, tau0, tau1)[0] for t in ts]


def exact_prof(args):
    key, q, tau0, tau1, rs, t = args
    return key, E.invert(t, rs, q, tau0, tau1)


def rel(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)) / sum(y * y for y in b))


def errs_hist(fe_cmp, ex):
    """fe_cmp: list over TCMP of (th,u,srr,stt); ex same -> relative L2 (%) per field"""
    return [100 * rel([f[j] for f in fe_cmp], [e[j] for e in ex]) for j in range(4)]


def main():
    R = {"eps": EPS, "const": mgl.constants()}
    pool = Pool(8)
    t_start = time.time()
    # ------------------------------------------------ parametric runs
    cases = []
    def add(name, tau0=T0, tau1=T1, **props):
        cases.append(dict(name=name, tau0=tau0, tau1=tau1, props=props))
    add("H0")
    for n in (0.5, 1.0, 2.0, 5.0):
        add("FG_n%g" % n, n=n)
    add("FG_exp3", law="exp", beta=3.0)
    for ph in (0.1, 0.2, 0.3):
        add("P_%g" % ph, phi0=ph)
    add("PG_0.3_n1", n=1.0, phi0=0.3, pgrade=True)
    add("FGP_n1_0.2", n=1.0, phi0=0.2)
    for t1 in (0.0, 0.02, 0.1):
        add("H_t1_%g" % t1, tau1=t1)
        add("FG_t1_%g" % t1, tau1=t1, n=1.0)
    add("FG_t1_0.05", n=1.0)
    for t0 in (0.0, 0.01, 0.04):
        add("H_t0_%g" % t0, tau0=t0)
        add("FG_t0_%g" % t0, tau0=t0, n=1.0)
    add("H_CTE", tau0=0.0, tau1=0.0)
    add("FG_CTE", tau0=0.0, tau1=0.0, n=1.0)
    add("H_LS", tau1=0.0)
    add("FGP_CTE", tau0=0.0, tau1=0.0, n=1.0, phi0=0.2)
    add("FGP_LS", tau1=0.0, n=1.0, phi0=0.2)
    # validation-only uniform media
    add("U_P0.2", phi0=0.2)                       # same as P_0.2 (kept as alias for clarity)
    add("U_cer", vfix=0.0)
    add("U_ones", n=2.0, cer=dict(lam=1, mu=1, k=1, rho=1, alpha=1, c=1))
    add("U_P0.2_LS", tau1=0.0, phi0=0.2)
    add("U_P0.2_CTE", tau0=0.0, tau1=0.0, phi0=0.2)
    jobs = cases + [dict(name="H0_R4.5", num=dict(Rout=4.5), props={"n": 0}, tau0=T0, tau1=T1),
                dict(name="H0_R1.0", num=dict(Rout=1.0, Lfine=1.0), props={"n": 0}, tau0=T0, tau1=T1),
                dict(name="H0_R1.6", num=dict(Rout=1.6, Lfine=1.6), props={"n": 0}, tau0=T0, tau1=T1)]
    outs = pool.map(run_case, jobs)
    R["cases"] = {o["name"]: o for o in outs}
    print("cases done", time.time() - t_start, flush=True)

    # ------------------------------------------------ exact solutions (uniform media)
    one = fem.Props().ratios(0.5)
    p02 = fem.Props(phi0=0.2).ratios(0.5)
    cer = fem.Props(vfix=0.0).ratios(0.5)
    lsets = {"H0": (one, T0, T1), "H_LS": (one, T0, 0.0), "H_CTE": (one, 0.0, 0.0),
             "P_0.2": (p02, T0, T1), "U_cer": (cer, T0, T1),
             "U_P0.2_LS": (p02, T0, 0.0), "U_P0.2_CTE": (p02, 0.0, 0.0)}
    hj = [(k, q, a, b, 0.3, TCMP) for k, (q, a, b) in lsets.items()]
    hj += [(k + "@0.8", q, a, b, 0.8, TCMP) for k, (q, a, b) in lsets.items()]
    pj = [(k, q, a, b, SAMPLE, 0.2) for k, (q, a, b) in lsets.items()]
    EX_H = dict(pool.map(exact_hist, hj))
    EX_P = dict(pool.map(exact_prof, pj))
    R["exact_hist"] = EX_H
    R["exact_prof"] = EX_P
    # dense exact history at r=0.3 for plots (copper MGL)
    tdense = [round(0.0025 * k, 4) for k in range(1, 121)]
    R["exact_dense_H0"] = dict(pool.map(exact_hist, [("H0", one, T0, T1, 0.3, tdense)]))["H0"]
    R["tdense"] = tdense
    prof_dense_r = [round(0.02 * k, 3) for k in range(5, 101)]
    R["exact_prof_dense_r"] = prof_dense_r
    R["exact_prof_dense"] = E.invert(0.2, prof_dense_r, one, T0, T1)

    # validation table entries
    V = {}
    c = R["cases"]
    for k in lsets:
        V[k] = dict(hist=errs_hist(c[k]["cmp"][0], EX_H[k]), hist08=errs_hist(c[k]["cmp"][1], EX_H[k + "@0.8"]))
        # profile at t=0.2 for r in [0.2, 1.2]
        idx = [i for i, r in enumerate(SAMPLE) if 0.2 <= r <= 1.2]
        fe = c[k]["snaps"]["0.2"]
        pe = []
        for j in range(4):
            a = [fe[i][j] for i in idx]
            b = [EX_P[k][i][j] for i in idx]
            pe.append(100 * rel(a, b))
        V[k]["prof"] = pe
    V["U_ones"] = dict(diff=max(abs(x - y) for x, y in zip(sum(sum(c["U_ones"]["cmp"], []), []),
                                                         sum(sum(c["H0"]["cmp"], []), []))))
    for nm in ("H0_R4.5", "H0_R1.6", "H0_R1.0"):
        V[nm] = dict(diff=[max(abs(x[0] - y[0]) for x, y in zip(c[nm]["cmp"][k], c["H0"]["cmp"][k])) for k in range(2)],
                     ref=[max(abs(x[0]) for x in c["H0"]["cmp"][k]) for k in range(2)])
    R["valid"] = V
    print("exact done", time.time() - t_start, flush=True)

    # ------------------------------------------------ Laplace-domain FE vs time-domain FE (graded + porous)
    spec = dict(BASE)
    pr = fem.Props(n=1.0, phi0=0.2, tau1=T1)
    nodes = fem.make_mesh(spec["Rout"], spec["h0"], spec["Lfine"], spec["grow"])
    S = fem.Solver(pr, nodes, p=spec["p"], tau0=T0, tau1=T1, a_src=spec["a_src"])
    ob = [S.locate(r) for r in OBS]
    tl = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
    lap = {}
    for t in tl:
        lap[str(t)] = mgl.durbin(lambda s: fem.laplace_fields(S, s, ob), t, 4, 2, N=600, nwynn=8)[0]
    R["laplace_fe"] = lap
    R["laplace_t"] = tl
    fgp = c["FGP_n1_0.2"]
    # compare at time tl (indices in 'cmp' only for TCMP: use tl subset in TCMP)
    cmpd = []
    for t in tl:
        i = TCMP.index(round(t, 4)) if round(t, 4) in TCMP else None
        if i is None:
            continue
        for k in range(2):
            fe = fgp["cmp"][k][i]
            ex = lap[str(t)][k]
            cmpd.append((t, OBS[k], [abs(fe[j] - ex[j]) / max(abs(ex[j]), 1e-300) for j in range(4)], fe, list(ex)))
    R["laplace_cmp"] = cmpd
    # relative L2 over the available times, each radius
    lv = []
    for k in range(2):
        fe = [fgp["cmp"][k][TCMP.index(round(t, 4))] for t in tl if round(t, 4) in TCMP]
        ex = [lap[str(t)][k] for t in tl if round(t, 4) in TCMP]
        lv.append([100 * rel([f[j] for f in fe], [e[j] for e in ex]) for j in range(4)])
    R["laplace_L2"] = lv
    print("laplace done", time.time() - t_start, flush=True)

    # ------------------------------------------------ regularisation radius study (homogeneous, vs exact)
    reg = []
    rj = []
    for a_ in (0.2, 0.1, 0.05, 0.025):
        rj.append(dict(name="reg_%g" % a_, num=dict(a_src=a_, h0=min(0.0125, a_ / 4), Lfine=2.4), props={"n": 0}, tau0=T0, tau1=T1))
    for o in pool.map(run_case, rj):
        reg.append((o["name"], errs_hist(o["cmp"][0], EX_H["H0"]), errs_hist(o["cmp"][1], EX_H["H0@0.8"])))
    R["reg"] = reg

    # ------------------------------------------------ convergence
    TC2 = [round(0.05 + 0.025 * k, 4) for k in range(11)]
    def conv_spec(name, p, h, dt):
        return dict(name=name, num=dict(p=p, h0=h, Lfine=2.5, Rout=2.5, grow=1.0, dt=dt, tend=0.3), props={"n": 0})
    conv_jobs = [conv_spec("ref_space", 2, 0.003125, 0.0001), conv_spec("ref_time", 2, 0.0125, 0.00003125)]
    for h in (0.05, 0.025, 0.0125, 0.00625):
        conv_jobs.append(conv_spec("P1_h%g" % h, 1, h, 0.00025))
    for h in (0.1, 0.05, 0.025, 0.0125):
        conv_jobs.append(conv_spec("P2_h%g" % h, 2, h, 0.00025))
    for dt in (0.005, 0.0025, 0.00125, 0.000625, 0.0003125):
        conv_jobs.append(conv_spec("dt_%g" % dt, 2, 0.0125, dt))
    co = {o["name"]: o for o in pool.map(run_case, conv_jobs)}
    R["conv"] = {}
    def cerr(a, ref):
        e_h = errs_hist(a["cmp"][0], ref["cmp"][0])
        fe = a["snaps"]["0.2"]
        fr = ref["snaps"]["0.2"]
        idx = [i for i, r in enumerate(SAMPLE) if 0.2 <= r <= 1.2]
        e_p = [100 * rel([fe[i][j] for i in idx], [fr[i][j] for i in idx]) for j in range(4)]
        return dict(hist=e_h, prof=e_p, nn=a["nn"], dt=a["dt"], cpu=a["cpu"])
    for k, o in co.items():
        if k.startswith("P1_") or k.startswith("P2_"):
            R["conv"][k] = cerr(o, co["ref_space"])
        elif k.startswith("dt_"):
            R["conv"][k] = cerr(o, co["ref_time"])
    R["conv"]["ref_space"] = dict(nn=co["ref_space"]["nn"], dt=co["ref_space"]["dt"], cpu=co["ref_space"]["cpu"])
    R["conv"]["ref_time"] = dict(nn=co["ref_time"]["nn"], dt=co["ref_time"]["dt"], cpu=co["ref_time"]["cpu"])
    # reference vs exact (floor due to regularisation)
    R["conv"]["ref_space_vs_exact"] = errs_hist(co["ref_space"]["cmp"][0], EX_H["H0"])
    print("conv done", time.time() - t_start, flush=True)

    # ------------------------------------------------ property / wave speed profiles
    rr = [round(0.01 * k, 2) for k in range(1, 151)]
    prof = {}
    for nm, kw in (("hom", {"n": 0}), ("n0.5", {"n": 0.5}), ("n1", {"n": 1.0}), ("n2", {"n": 2.0}), ("n5", {"n": 5.0}),
                   ("exp3", dict(law="exp", beta=3.0)), ("p0.2", {"phi0": 0.2}), ("p0.3", {"phi0": 0.3}),
                   ("n1p0.2", dict(n=1.0, phi0=0.2)), ("pg", dict(n=1.0, phi0=0.3, pgrade=True))):
        pr_ = fem.Props(**kw)
        prof[nm] = dict(c=[pr_.speed(r) for r in rr], q=[pr_.ratios(r) for r in rr])
    R["prof_r"] = rr
    R["prof"] = prof
    # travel times from r = 0.05 to 0.3 and 0.8 by the local wave speed
    def ttime(pr_, r1, r2=0.05, n=2000):
        h = (r1 - r2) / n
        return sum(h / pr_.speed(r2 + (i + 0.5) * h) for i in range(n))
    tt = {}
    for nm, kw in (("H0", {"n": 0}), ("FG_n1", {"n": 1.0}), ("FG_n2", {"n": 2.0}), ("FG_n5", {"n": 5.0}),
                   ("P_0.2", {"phi0": 0.2}), ("FGP_n1_0.2", dict(n=1.0, phi0=0.2))):
        pr_ = fem.Props(**kw)
        tt[nm] = [ttime(pr_, 0.3), ttime(pr_, 0.8)]
    R["travel"] = tt
    R["wallclock"] = time.time() - t_start
    json.dump(R, open(os.path.join(HERE, "results.json"), "w"))
    print("done", R["wallclock"])


if __name__ == "__main__":
    main()
