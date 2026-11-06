"""Stage C: model comparison, relaxation-time / k* sweeps, field histories for the figures -> part_compare.json"""
import json, math, time
import model, fem1d, opt

FDX, FDT = opt.FDX, opt.FDT
OPT = json.load(open("part_opt_models.json"))
SENS = json.load(open("part_opt_sens.json"))
OUT = {}


def ev(name, ov, des, cov=1.0, **kw):
    return opt.evaluate(name, ov, des, cov, FDX, FDT)


def scale_to_kill(name, ov, des, lo=0.3, hi=3.0):
    """smallest multiplier of I0 giving min Omega_T = Omega_c (monotone), by bisection"""
    def f(s):
        P, R, m = ev(name, ov, dict(des, I0=des["I0"] * s))
        return m["minOmT"] - P["Om_c"], m
    a, b = lo, hi
    fa, _ = f(a); fb, _ = f(b)
    if fa > 0 or fb < 0:
        return None
    for _ in range(22):
        c = 0.5 * (a + b)
        fc, _ = f(c)
        if fc >= 0: b = c
        else: a = c
    fc, m = f(b)
    return b, m


def slim(m):
    return {k: m[k] for k in ("Tmax", "sabs", "sifT", "sifN", "minOmT", "OmT_h", "OmN_h", "JO", "JF", "dd", "smax", "smin", "kd")}


def hist(R, xsel, every):
    """downsampled theta histories (K rise) at selected x [m] and Omega profiles"""
    idx = [min(range(len(R.xs)), key=lambda k: abs(R.xs[k] - x)) for x in xsel]
    n = list(range(0, R.nstep + 1, every))
    gam, sT, sN = fem1d.stress_hist(R)
    out = dict(t=[k * R.dt for k in n], th=[[R.th[k][i] for k in n] for i in idx],
               sigT_h=[-sT * gam[k][R.n1] for k in n], sigN_h=[-sN * gam[k][R.n1] for k in n],
               sig_0=[-sT * gam[k][0] for k in n])
    out["x"] = R.xs; out["n1"] = R.n1
    out["OmT"] = R.OmT[: R.n1 + 1]; out["OmN"] = R.OmN[R.n1:]
    return out


def main():
    t0 = time.time()
    base = OPT["S1_Pennes"]["best"]["des"]
    OUT["pennes_design"] = base
    # (1) common (Pennes-optimal) design evaluated under each model, unscaled and scaled to just kill
    rows = {}
    for name in ("Pennes", "CV", "MGT", "MGL"):
        P, R, m = ev(name, {}, base)
        sc = scale_to_kill(name, {}, base)
        rows[name] = dict(unscaled=slim(m), scale=sc[0] if sc else None, scaled=slim(sc[1]) if sc else None,
                          hist=hist(R, [0.0, 0.004, 0.006], 20))
        print(name, rows[name]["scale"], rows[name]["unscaled"]["minOmT"], flush=True)
    OUT["common"] = rows
    # (2) each model's own optimum design under the other models (cross evaluation)
    cross = {}
    for a in ("Pennes", "CV", "MGT", "MGL"):
        des = OPT["S1_" + a]["best"]["des"]
        cross[a] = {}
        for b in ("Pennes", "CV", "MGT", "MGL"):
            P, R, m = ev(b, {}, des)
            cross[a][b] = slim(m)
    OUT["cross"] = cross
    # (3) tau sweep: dose multiplier needed for kill (design shape fixed)
    tsw = {}
    for name, key in (("CV", "tauq"), ("MGL", "tau0")):
        tsw[name] = []
        for tau in (0.0, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0):
            ov = {key: tau}
            sc = scale_to_kill(name, ov, base)
            P, R, m = ev(name, ov, base)
            tsw[name].append(dict(tau=tau, scale=sc[0] if sc else None, minOmT=m["minOmT"], Tmax=m["Tmax"], JF=m["JF"],
                                  scaled=slim(sc[1]) if sc else None))
        print(name, [(r["tau"], r["scale"]) for r in tsw[name]], flush=True)
    OUT["tau_sweep"] = tsw
    esw = []
    for eta in (0.0, 0.1, 0.25, 0.5, 0.75, 0.9):
        ov = {"eta": eta}
        name = "MGT" if eta > 0 else "CV"
        sc = scale_to_kill(name, ov, base, lo=0.2, hi=6.0)
        P, R, m = ev(name, ov, base)
        esw.append(dict(eta=eta, scale=sc[0] if sc else None, minOmT=m["minOmT"], Tmax=m["Tmax"], JF=m["JF"],
                        scaled=slim(sc[1]) if sc else None))
    OUT["eta_sweep"] = esw
    print("eta", [(r["eta"], r["scale"]) for r in esw], flush=True)
    # (4) field histories of the baseline optimum (MGL, S1) and the pulsed alternative from the sensitivity base
    fields = {}
    for tag, des in (("opt", OPT["S1_MGL"]["best"]["des"]), ("pulsed", SENS["base"]["best"]["des"])):
        P, R, m = ev("MGL", {}, des)
        fields[tag] = dict(des=des, m=slim(m), hist=hist(R, [0.0, 0.002, 0.004, 0.006, 0.010], 5))
        fields[tag]["fbar"] = fem1d.fbar_array(des, R.nstep, R.dt)[::5]
        # Omega profiles at several times
        fields[tag]["profiles"] = {}
    # Omega profiles at selected times for the optimum (re-run with keep=True)
    des = OPT["S1_MGL"]["best"]["des"]
    P = opt.build("MGL", {})
    R = fem1d.run(P, des, dx=FDX, dt=FDT, keep=True)
    prof = {}
    for t in (10.0, 20.0, 40.0, 80.0, 120.0):
        n = int(round(t / R.dt))
        prof[str(t)] = dict(OmT=R.OmTh[n][: R.n1 + 1], OmN=R.OmNh[n][R.n1:], th=R.th[n])
    fields["opt"]["profiles"] = prof
    fields["opt"]["x"] = R.xs; fields["opt"]["n1"] = R.n1
    OUT["fields"] = fields
    # (5) horizon effect on a fixed design
    hz = []
    for Th in (30.0, 60.0, 120.0, 300.0):
        P, R, m = ev("MGL", {"Teval": Th}, OPT["S1_MGL"]["best"]["des"])
        hz.append(dict(Teval=Th, minOmT=m["minOmT"], JF=m["JF"], OmN_h=m["OmN_h"]))
    OUT["horizon"] = hz
    json.dump(OUT, open("part_compare.json", "w"))
    print("done", time.time() - t0)


if __name__ == "__main__":
    main()
