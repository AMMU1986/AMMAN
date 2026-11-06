"""Constrained design optimisation of the laser pulse train (pure Python Nelder-Mead with exact-penalty
constraints, multi-start over the integer pulse number) and epsilon-constraint Pareto sweeps."""
import math, random
import model, fem1d

TCOOL = 30.0
BOUNDS = dict(I0=(2e4, 8e5), tp=(0.2, 60.0), duty=(0.1, 1.0))
DX, DT = 2.5e-4, 0.4
FDX, FDT = 2.5e-4, 0.05      # fine settings used to polish and report final designs


def apply(P, ov):
    """declarative overrides (picklable) -> modified copy of P"""
    for k, v in ov.items():
        if k == "mua": P["las"]["mua"] = v
        elif k == "mus": P["las"]["mus"] = v
        elif k == "EaT": P["arr"][0]["Ea"] = v; P["arr"][0].update(model.tumour_arrhenius(Ea=v, tref=ov.get("trefT", 3600.0)))
        elif k == "trefT": P["arr"][0].update(model.tumour_arrhenius(Ea=P["arr"][0]["Ea"], tref=v))
        elif k == "AfacT": P["arr"][0]["A"] *= v
        elif k == "AfacN": P["arr"][1]["A"] *= v
        elif k == "EaN": P["arr"][1]["Ea"] = v
        elif k == "normal_as_tumour": P["arr"][1] = dict(P["arr"][0])
        elif k == "wbscale":
            for i in (0, 1): P["lay"][i]["om0"] *= v
        elif k == "kv": P["kv"] = v
        elif k == "cw": P["cw"] = tuple(v)
        elif k == "thc": P["thc"] = tuple(v)
        elif k == "kstar_lit": P["kstar_lit"] = v
        else: P[k] = v
    return P


def build(model_name, ov):
    P = model.make(model_name)
    # re-parameterise tumour Arrhenius if Ea/tref overrides are present
    ov = dict(ov)
    if "EaT" in ov or "trefT" in ov:
        P["arr"][0] = model.tumour_arrhenius(Ea=ov.pop("EaT", 5.5e5), tref=ov.pop("trefT", 3600.0))
    return apply(P, ov)


def design_from(I0, tp, duty, Np):
    return dict(I0=I0, tp=tp, per=tp / duty, Np=Np)


def evaluate(model_name, ov, des, cov=1.0, dx=DX, dt=DT, picard=1):
    P = build(model_name, ov)
    R = fem1d.run(P, des, dx=dx, dt=dt, picard=picard, keep=False)
    return P, R, fem1d.metrics(R, cov)


def violations(P, m, des):
    Oc = P["Om_c"]
    v1 = max(0.0, (math.log(Oc) - math.log(max(m["minOmT"], 1e-30))) / math.log(Oc))
    v2 = max(0.0, (m["Tmax"] - P["Tvap"]) / 20.0)
    v3 = max(0.0, (m["sabs"] - P["sig_lim"]) / P["sig_lim"])
    v4 = max(0.0, (des["Np"] * des["per"] - P["Ttreat"]) / P["Ttreat"])
    return v1, v2, v3, v4


def objective(m):
    return math.log(1.0 + 1e3 * m["JO"])         # JO in m * Omega -> mm * Omega


def penalised(model_name, ov, x, Np, cov=1.0):
    I0 = min(max(math.exp(x[0]), BOUNDS["I0"][0]), BOUNDS["I0"][1])
    tp = min(max(math.exp(x[1]), BOUNDS["tp"][0]), BOUNDS["tp"][1])
    du = BOUNDS["duty"][0] + (BOUNDS["duty"][1] - BOUNDS["duty"][0]) / (1 + math.exp(-x[2]))
    des = design_from(I0, tp, du, Np)
    pen_b = sum(max(0.0, abs(a) - 12) for a in x)
    P, R, m = evaluate(model_name, ov, des, cov)
    v = violations(P, m, des)
    J = min(objective(m), 30.0)
    f = J + 50.0 * sum(v) + 200.0 * sum(a * a for a in v) + pen_b
    return f, des, m, v, J


def nelder_mead(fun, x0, step, maxit=60, tol=1e-4):
    n = len(x0)
    sim = [list(x0)]
    for i in range(n):
        y = list(x0)
        y[i] += step[i]
        sim.append(y)
    fv = [fun(s) for s in sim]
    nev = n + 1
    for it in range(maxit):
        order = sorted(range(n + 1), key=lambda i: fv[i])
        sim = [sim[i] for i in order]; fv = [fv[i] for i in order]
        if abs(fv[-1] - fv[0]) < tol and it > 10:
            break
        cen = [sum(sim[i][j] for i in range(n)) / n for j in range(n)]
        xr = [cen[j] + (cen[j] - sim[-1][j]) for j in range(n)]
        fr = fun(xr); nev += 1
        if fr < fv[0]:
            xe = [cen[j] + 2 * (cen[j] - sim[-1][j]) for j in range(n)]
            fe = fun(xe); nev += 1
            if fe < fr: sim[-1], fv[-1] = xe, fe
            else: sim[-1], fv[-1] = xr, fr
        elif fr < fv[-2]:
            sim[-1], fv[-1] = xr, fr
        else:
            if fr < fv[-1]:
                xc = [cen[j] + 0.5 * (xr[j] - cen[j]) for j in range(n)]
            else:
                xc = [cen[j] + 0.5 * (sim[-1][j] - cen[j]) for j in range(n)]
            fc = fun(xc); nev += 1
            if fc < min(fr, fv[-1]):
                sim[-1], fv[-1] = xc, fc
            else:
                for i in range(1, n + 1):
                    sim[i] = [sim[0][j] + 0.5 * (sim[i][j] - sim[0][j]) for j in range(n)]
                    fv[i] = fun(sim[i]); nev += 1
    i = min(range(n + 1), key=lambda k: fv[k])
    return sim[i], fv[i], nev


def optimise_np(task):
    """task = (model_name, overrides, Np, seed, cov, nstart) -> best record for this pulse number"""
    model_name, ov, Np, seed, cov, nstart = task
    rnd = random.Random(seed * 1000 + Np)
    best = None
    nev_tot = 0
    # coarse random screening, then Nelder-Mead from the best nstart points
    cands = []
    for _ in range(14):
        cap = ov.get("Ttreat", model.default()["Ttreat"]) / Np
        x = [rnd.uniform(math.log(4e4), math.log(6e5)),
             rnd.uniform(math.log(0.3), math.log(max(0.5, cap))), rnd.uniform(-2.0, 3.0)]
        f = penalised(model_name, ov, x, Np, cov)[0]
        cands.append((f, x))
        nev_tot += 1
    cands.sort(key=lambda c: c[0])
    for f0, x0 in cands[:nstart]:
        xb, fb, nev = nelder_mead(lambda z: penalised(model_name, ov, z, Np, cov)[0], x0, [0.4, 0.5, 0.8])
        nev_tot += nev
        if best is None or fb < best[0]:
            best = (fb, xb)
    f, des, m, v, J = penalised(model_name, ov, best[1], Np, cov)
    return dict(Np=Np, f=f, des=des, m=m, v=v, J=J, nev=nev_tot, x=best[1])


def polish(model_name, ov, rec, cov=1.0, rel=0.08):
    """make the final design strictly feasible by bisection on the peak intensity (kill and stress compete)."""
    des = dict(rec["des"])
    P, R, m = evaluate(model_name, ov, des, cov, FDX, FDT)
    v = violations(P, m, des)
    if sum(v) <= 0:
        return des, m, v
    lo, hi = des["I0"], des["I0"] * (1 + rel)
    lo_d = des["I0"] * (1 - rel)
    for scale_range in ((lo, hi), (lo_d, lo)):
        a, b = scale_range
        da, db = dict(des, I0=a), dict(des, I0=b)
        ma = evaluate(model_name, ov, da, cov, FDX, FDT); mb = evaluate(model_name, ov, db, cov, FDX, FDT)
        va, vb = violations(ma[0], ma[2], da), violations(mb[0], mb[2], db)
        if sum(va) > 0 and sum(vb) == 0:
            for _ in range(14):
                c = 0.5 * (a + b)
                dc = dict(des, I0=c)
                mc = evaluate(model_name, ov, dc, cov, FDX, FDT)
                if sum(violations(mc[0], mc[2], dc)) == 0: b = c
                else: a = c
            dd = dict(des, I0=b)
            mm = evaluate(model_name, ov, dd, cov, FDX, FDT)
            return dd, mm[2], violations(mm[0], mm[2], dd)
        if sum(va) == 0:
            return da, ma[2], va
        if sum(vb) == 0:
            return db, mb[2], vb
    return des, m, v


def run_case(pool, model_name, ov, cov=1.0, seed=1, nps=(1, 2, 3, 4, 6, 8, 10, 12), nstart=2):
    tasks = [(model_name, ov, n, seed, cov, nstart) for n in nps]
    recs = pool.map(optimise_np, tasks)
    feas = [r for r in recs if sum(r["v"]) < 5e-3]
    pool_ = feas if feas else recs
    best = min(pool_, key=lambda r: r["J"] if feas else r["f"])
    des, m, v = polish(model_name, ov, best, cov)
    return dict(best=dict(des=des, m=m, v=v, J=objective(m)), per_np=[dict(Np=r["Np"], J=r["J"], f=r["f"], v=r["v"], des=r["des"]) for r in recs],
                nev=sum(r["nev"] for r in recs))
