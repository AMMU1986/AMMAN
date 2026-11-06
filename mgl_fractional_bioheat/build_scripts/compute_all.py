"""All computations for the paper -> results.json (cached per case)."""
import json, math, os, sys, time
import model, lap, fem, steady

HERE = os.path.dirname(os.path.abspath(__file__))
DX, DT, TEND = 0.0025, 0.0025, 0.6
SNAPS = [0.05, 0.1, 0.2, 0.4, 0.6]
XG = [round(0.01 * i, 2) for i in range(101)]
WR = model.wratio()
CW = (0.5, 3.0)
OUT = {}
CACHE = os.path.join(HERE, "cache")
os.makedirs(CACHE, exist_ok=True)


def node(R, x):
    return min(range(len(R.xs)), key=lambda k: abs(R.xs[k] - x))


def mid(xm, x):
    return min(range(len(xm)), key=lambda k: abs(xm[k] - x))


def summarize(R, h, thr=1e-3):
    p = R.p
    dt = R.dt
    step = max(1, int(round(0.01 / dt)))
    ts = [n * dt for n in range(0, R.nstep + 1, step)]
    obsx = [0.05, 0.1, h, 0.3, 0.5, 0.8]
    out = dict(t=ts, obsx=obsx, hist=[], snaps={}, peak=None)
    ns = list(range(0, R.nstep + 1, step))
    sig = {}
    peak = (0.0, 0.0, 0.0)
    for n in ns:
        xm, sg = fem.stress(R, n)
        sig[n] = (xm, sg)
        for xx, v in zip(xm, sg):
            if abs(v) > abs(peak[0]) and xx > 0.01:
                peak = (v, xx, n * dt)
    out["peak"] = peak
    for x in obsx:
        i = node(R, x)
        hist = []
        for n in ns:
            xm, sg = sig[n]
            k = mid(xm, x)
            hist.append([R.TH[n][i], R.U[n][i], sg[k]])
        out["hist"].append(hist)
    for ts_ in SNAPS:
        n = int(round(ts_ / dt))
        if n not in sig:
            xm, sg = fem.stress(R, n)
        else:
            xm, sg = sig[n]
        rows = []
        for x in XG:
            i = node(R, x)
            rows.append([R.TH[n][i], R.U[n][i], sg[mid(xm, x)]])
        out["snaps"][str(ts_)] = rows
        th = R.TH[n]
        xf = 0.0
        for i, v in enumerate(th):
            if abs(v) > thr:
                xf = R.xs[i]
        out.setdefault("front", {})[str(ts_)] = xf
    out["iters_max"] = max(R.iters)
    out["iters_mean"] = sum(R.iters) / len(R.iters)
    return out


def case(name, **kw):
    f = os.path.join(CACHE, name + ".json")
    if os.path.exists(f):
        return json.load(open(f))
    t0 = time.time()
    dx = kw.pop("dx", DX); dt = kw.pop("dt", DT); T = kw.pop("T", TEND)
    p = model.make(**kw)
    R = fem.run(p, dx=dx, dt=dt, T=T)
    s = summarize(R, p["h"])
    s["secs"] = time.time() - t0
    json.dump(s, open(f, "w"))
    print("case", name, round(s["secs"], 1), "s", file=sys.stderr, flush=True)
    return s


def lap_fields(p, xs, t, N=3000):
    a, _, _ = lap.invert(p, xs, t, N=N, nwynn=40)
    return a


def rel(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)) / max(1e-300, sum(y * y for y in b)))


def fem_vs_lap(p, dx, dt, t, pts=None, R=None):
    pts = pts or [round(0.05 * k, 3) for k in range(1, 20)]
    ref = lap_fields(p, pts, t)
    if R is None:
        R = fem.run(p, dx=dx, dt=t if False else dt, T=t)
    n = int(round(t / R.dt))
    th = [fem.at(R, n, x, "th") for x in pts]
    u = [fem.at(R, n, x, "u") for x in pts]
    xm, sg = fem.stress(R, n)
    ptm = [x + 0.5 * dx for x in pts]
    refs = lap_fields(p, ptm, t)
    sgf = [sg[mid(xm, x)] for x in ptm]
    return dict(th=rel(th, [r[0] for r in ref]), u=rel(u, [r[1] for r in ref]), sg=rel(sgf, [r[2] for r in refs]))


def main(stage):
    res = {}
    st = lambda n: stage == n
    base = dict(h=0.2, tau0=0.1, tau1=0.05)
    if st('valid'):
        # ------------------------------------------------ validation (Laplace)
        V = {}
        for al in (1.0, 0.6):
            p = model.make(alpha=al, **base)
            R = fem.run(p, dx=DX, dt=DT, T=0.6)
            for t in (0.1, 0.2, 0.4, 0.6):
                V["H_a%g_t%g" % (al, t)] = fem_vs_lap(p, DX, DT, t, R=R)
        print("val1", V, file=sys.stderr, flush=True)
        # laser (linear)
        pl = model.make(alpha=0.7, theta0=0.0, a7=2.0, tp=0.2, **base)
        pl["laser"] = True
        Rl = fem.run(pl, dx=DX, dt=DT, T=0.6)
        for t in (0.2, 0.4, 0.6):
            V["L_a0.7_t%g" % t] = fem_vs_lap(pl, DX, DT, t, R=Rl)
        # Pennes (tau0=0,tau1=0) and tau1=0 limit
        for nm, kw in (("pennes", dict(tau0=0.0, tau1=0.0, alpha=1.0)), ("tau1_0", dict(tau0=0.1, tau1=0.0, alpha=0.8))):
            p = model.make(h=0.2, **kw)
            R = fem.run(p, dx=DX, dt=DT, T=0.4)
            V[nm] = fem_vs_lap(p, DX, DT, 0.4, R=R)
        res["valid"] = V
        # Laplace self check (N)
        p = model.make(alpha=0.6, **base)
        pts = [0.1, 0.2, 0.3, 0.5]
        a1 = lap_fields(p, pts, 0.3, N=3000); a2 = lap_fields(p, pts, 0.3, N=6000)
        res["lap_self"] = max(abs(x[k] - y[k]) for x, y in zip(a1, a2) for k in range(3))
    if st('conv'):
        # ------------------------------------------------ convergence
        C = {}
        pts = [round(0.05 * k, 3) for k in range(1, 20)]
        for al in (1.0, 0.6):
            for bc in ("H", "ramp"):
                kw = dict(alpha=al, **base)
                if bc == "ramp":
                    kw["bc_tau"] = 0.05
                p = model.make(**kw)
                rows = []
                for dt in (0.02, 0.01, 0.005, 0.0025):
                    R = fem.run(p, dx=0.00125, dt=dt, T=0.4)
                    e = fem_vs_lap(p, 0.00125, dt, 0.4, R=R)
                    rows.append([dt, e["th"], e["u"], e["sg"]])
                C["dt_%s_a%g" % (bc, al)] = rows
        p = model.make(alpha=0.6, bc_tau=0.05, **base)
        rows = []
        for dx in (0.04, 0.02, 0.01, 0.005, 0.0025):
            R = fem.run(p, dx=dx, dt=0.0025, T=0.4)
            e = fem_vs_lap(p, dx, 0.0025, 0.4, R=R)
            rows.append([dx, e["th"], e["u"], e["sg"]])
        C["dx_ramp_a0.6"] = rows
        p = model.make(alpha=0.6, **base)
        rows = []
        for dx in (0.04, 0.02, 0.01, 0.005, 0.0025):
            R = fem.run(p, dx=dx, dt=0.0025, T=0.4)
            e = fem_vs_lap(p, dx, 0.0025, 0.4, R=R)
            rows.append([dx, e["th"], e["u"], e["sg"]])
        C["dx_H_a0.6"] = rows
        res["conv"] = C
        print("conv done", file=sys.stderr, flush=True)
    if st('limits'):
        # ------------------------------------------------ limit checks
        Lm = {}
        p1 = model.make(alpha=1.0, **base); p2 = model.make(alpha=0.999, **base); p3 = model.make(alpha=0.9, **base)
        R1 = fem.run(p1, dx=DX, dt=DT, T=0.4); R2 = fem.run(p2, dx=DX, dt=DT, T=0.4); R3 = fem.run(p3, dx=DX, dt=DT, T=0.4)
        d = lambda A, B: max(abs(x - y) for x, y in zip(A.TH[-1], B.TH[-1]))
        Lm["alpha_0.999_vs_1"] = d(R1, R2)
        Lm["alpha_0.9_vs_1"] = d(R1, R3)
        p0 = model.make(alpha=0.7, a6=(0.0, 0.0), **base); pq = model.make(alpha=0.7, **base)
        Ra = fem.run(p0, dx=DX, dt=DT, T=0.4); Rb = fem.run(pq, dx=DX, dt=DT, T=0.4)
        Lm["literal_perfusion_vs_zero"] = max(max(abs(x - y) for x, y in zip(Ra.TH[-1], Rb.TH[-1])), max(abs(x - y) for x, y in zip(Ra.U[-1], Rb.U[-1])))
        Lm["a6_literal"] = model.coeffs()[0][0]["a6"]
        pc = model.make(alpha=0.7, cw=(1e-12, 1e-12), **base)
        Rc = fem.run(pc, dx=DX, dt=DT, T=0.4)
        Lm["cw0_vs_linear"] = max(abs(x - y) for x, y in zip(Rc.TH[-1], Rb.TH[-1]))
        Lm["cw0_iters"] = max(Rc.iters)
        # steady-state nonlinear check
        SS = []
        for nm, kw in (("perfusion", dict(cw=CW, a6=(20.0, 20.0 * WR))), ("perfusion+chi", dict(cw=CW, a6=(20.0, 20.0 * WR), chi=(0.2, 0.0)))):
            p = model.make(alpha=0.7, **base, **kw)
            xs, th, it = steady.steady(p)
            R = fem.run(p, dx=0.005, dt=0.05, T=8.0)
            err = max(abs(R.TH[-1][i] - th[min(range(len(xs)), key=lambda k: abs(xs[k] - R.xs[i]))]) for i in range(len(R.xs)))
            SS.append([nm, err, it, max(R.iters)])
        Lm["steady"] = SS
        res["limits"] = Lm
        # Picard record
        pp = model.make(alpha=0.7, cw=CW, a6=(10.0, 10.0 * WR), chi=(0.2, 0.0), **base)
        Rp = fem.run(pp, dx=DX, dt=DT, T=0.6)
        res["picard"] = dict(resid=Rp.resid, iters=Rp.iters)
    if st('studies'):
        # ------------------------------------------------ main studies
        S = {}
        S["base"] = case("base", alpha=1.0, **base)
        for al in (0.9, 0.75, 0.6, 0.45, 0.3):
            S["alpha_%g" % al] = case("alpha_%g" % al, alpha=al, **base)
        for t1 in (0.0, 0.025, 0.1, 0.2):
            S["tau1_%g" % t1] = case("tau1_%g" % t1, alpha=1.0, **{**base, "tau1": t1})
        for tau0 in (0.05, 0.2):
            S["tau0_%g" % tau0] = case("tau0_%g" % tau0, alpha=1.0, **{**base, "tau0": tau0})
        for h in (0.1, 0.3, 0.4):
            S["h_%g" % h] = case("h_%g" % h, alpha=0.75, **{**base, "h": h})
        S["h_0.2"] = case("alpha_0.75b", alpha=0.75, **base)
        for Pi in (0.0, 2.0, 5.0, 10.0, 20.0):
            S["Pi_%g" % Pi] = case("Pi_%g" % Pi, alpha=0.75, cw=CW, a6=(Pi, Pi * WR), **base)
            S["Pi_%g_c0" % Pi] = case("Pi_%g_c0" % Pi, alpha=0.75, cw=(0.0, 0.0), a6=(Pi, Pi * WR), **base)
        for sc in (0.5, 2.0, 4.0):
            S["cw_%g" % sc] = case("cw_%g" % sc, alpha=0.75, cw=(CW[0] * sc, CW[1] * sc), a6=(10.0, 10.0 * WR), **base)
        S["chi"] = case("chi", alpha=0.75, chi=(0.3, 0.0), **base)
        S["chi_cw"] = case("chi_cw", alpha=0.75, chi=(0.3, 0.0), cw=CW, a6=(10.0, 10.0 * WR), **base)
        S["laser"] = case("laser", alpha=0.75, theta0=0.0, a7=2.0, laser=True, **base) if False else None
        res["studies"] = S
        # laser (stored from earlier run)
        pl2 = model.make(alpha=0.75, theta0=0.0, a7=2.0, tp=0.2, **base); pl2["laser"] = True
        Rl2 = fem.run(pl2, dx=DX, dt=DT, T=0.6)
        res["laser"] = summarize(Rl2, 0.2)
        pl3 = model.make(alpha=0.75, theta0=0.0, a7=2.0, tp=0.2, cw=CW, a6=(10.0, 10.0 * WR), **base); pl3["laser"] = True
        res["laser_perf"] = summarize(fem.run(pl3, dx=DX, dt=DT, T=0.6), 0.2)
    if st('models'):
        # ------------------------------------------------ model comparison (Laplace)
        MC = {}
        xg = [round(0.02 * i, 2) for i in range(51)]
        models = {
            "Pennes": dict(model="MGL", tau0=0.0, tau1=0.0, alpha=1.0),
            "MGT": dict(model="MGT", taq=0.1, tau1=0.0, alpha=1.0),
            "LS-type": dict(model="MGL", tau0=0.1, tau1=0.0, alpha=1.0),
            "MGL": dict(model="MGL", tau0=0.1, tau1=0.05, alpha=1.0),
            "fMGL0.75": dict(model="MGL", tau0=0.1, tau1=0.05, alpha=0.75),
            "fMGL0.5": dict(model="MGL", tau0=0.1, tau1=0.05, alpha=0.5),
        }
        ts = [round(0.01 * k, 2) for k in range(1, 61)]
        for nm, kw in models.items():
            p = model.make(h=0.2, **kw)
            MC[nm] = dict(snaps={}, hist=[])
            for t in SNAPS:
                MC[nm]["snaps"][str(t)] = [list(map(float, r[:3])) for r in lap_fields(p, xg, t, N=3000)]
            hobs = [0.2, 0.3]
            for t in ts[4::2]:
                pass
            edge = []
            for t in [0.02 * k for k in range(1, 31)]:
                r = lap_fields(p, [0.1, 0.2, 0.3], t, N=2000)
                edge.append([t] + [v for rr in r for v in rr[:3]])
            MC[nm]["edge"] = edge
            print("mc", nm, file=sys.stderr, flush=True)
        res["models"] = MC
        res["xg_models"] = xg
    res["meta"] = dict(dx=DX, dt=DT, T=TEND)
    json.dump(res, open(os.path.join(HERE, "part_%s.json" % stage), "w"))
    print("done", stage, file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1])
