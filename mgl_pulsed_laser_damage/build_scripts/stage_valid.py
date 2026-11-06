"""Stage A: verification and validation computations -> part_valid.json"""
import json, math, time, cmath
import model, fem1d, lap, opt

OUT = {}
XS_MM = [0, 1, 2, 3, 4, 6, 8, 12, 16]
TIMES = [1.0, 3.0, 6.0, 12.0]
DES = dict(I0=3e5, tp=2.0, per=2.0, Np=1)


def lin(name, **kw):
    P = model.make(name)
    P["cw"] = (0.0, 0.0); P["thc"] = (1e6, 1e6)
    P.update(kw)
    return P


def fe_at(R, xs_m, t):
    n = int(round(t / R.dt))
    out = []
    P = R.P
    for x in xs_m:
        i = min(range(len(R.xs)), key=lambda k: abs(R.xs[k] - x))
        a, b, c = R.th[n][i], R.th[n - 1][i], R.th[n - 2][i]
        Dth = (1.5 * a - 2 * b + 0.5 * c) / R.dt
        lay = 0 if x < P["h"] - 1e-12 else 1          # at x = h report the normal side
        sl = P["lay"][lay]["sl"]
        out.append((a, -sl * (a + P["tau1"] * Dth)))
    return out


def lap_at(P, xs_m, t, rscale=1.0):
    acc, full, half = lap.invert(P, DES, xs_m, t, rscale=rscale, N=2500)
    return acc, full, half


def validation():
    res = {}
    xs_m = [v * 1e-3 for v in XS_MM]
    # normal-side evaluation at x = h: Laplace code uses the left (tumour) layer for x <= h, so shift by 1 nm
    xs_l = [x if abs(x - 0.004) > 1e-9 else 0.004 + 1e-9 for x in xs_m]
    for name in ("Pennes", "CV", "MGT", "MGL"):
        P = lin(name)
        R = fem1d.run(P, DES, dx=1.25e-4, dt=0.02, Tend=12.0, keep=False)
        rec = dict(t=TIMES, x=XS_MM, th_fe=[], th_lap=[], sg_fe=[], sg_lap=[], eth=[], esg=[], trunc=[])
        for t in TIMES:
            a = fe_at(R, xs_m, t)
            acc, full, half = lap_at(P, xs_l, t)
            thL = [r[0] for r in acc]
            sgL = [r[4] for r in acc]
            thF = [v[0] for v in a]; sgF = [v[1] for v in a]
            rec["th_fe"].append(thF); rec["th_lap"].append(thL); rec["sg_fe"].append(sgF); rec["sg_lap"].append(sgL)
            rec["eth"].append(max(abs(p - q) for p, q in zip(thF, thL)) / max(abs(q) for q in thL))
            rec["esg"].append(max(abs(p - q) for p, q in zip(sgF, sgL)) / max(abs(q) for q in sgL))
            rec["trunc"].append(max(abs(r[0] - f[0]) for r, f in zip(acc, full)) / max(abs(q) for q in thL))
        res[name] = rec
        print(name, [round(e, 5) for e in rec["eth"]], [round(e, 4) for e in rec["esg"]], flush=True)
    return res


def profile_curves():
    """theta(t) at x = h (tumour side) for Figure 2: FE vs Laplace inversion on a time grid, model MGL & Pennes & CV"""
    out = {}
    ts = [1.0 + 1.0 * k for k in range(0, 15)]
    for name in ("Pennes", "CV", "MGL"):
        P = lin(name)
        R = fem1d.run(P, DES, dx=1.25e-4, dt=0.02, Tend=15.0, keep=False)
        xs = [0.0, 0.004 - 1e-9, 0.008]
        fe = []; la = []
        for t in ts:
            a = fe_at(R, [0.0, 0.004 - 1e-9, 0.008], t)
            fe.append([v[0] for v in a])
            acc, _, _ = lap.invert(P, DES, xs, t, N=1800)
            la.append([r[0] for r in acc])
        out[name] = dict(t=ts, fe=fe, lap=la)
    return out


def conv_vs_laplace():
    out = {}
    t = 6.0
    xs_m = [v * 1e-3 for v in (0, 1, 2, 3, 4, 6, 8, 12)]
    xs_l = [x if abs(x - 0.004) > 1e-9 else 0.004 - 1e-9 for x in xs_m]
    for name in ("Pennes", "MGL"):
        P = lin(name)
        acc, _, _ = lap.invert(P, DES, xs_l, t, N=2500)
        ref = [r[0] for r in acc]
        mx = max(abs(v) for v in ref)
        dts = [0.32, 0.16, 0.08, 0.04, 0.02]
        edt = []
        for dt in dts:
            R = fem1d.run(P, DES, dx=1.25e-4, dt=dt, Tend=t, keep=False)
            a = fe_at(R, xs_m, t)
            edt.append(max(abs(v[0] - q) for v, q in zip(a, ref)) / mx)
        dxs = [1e-3, 5e-4, 2.5e-4, 1.25e-4]
        edx = []
        for dx in dxs:
            R = fem1d.run(P, DES, dx=dx, dt=0.02, Tend=t, keep=False)
            a = fe_at(R, xs_m, t)
            edx.append(max(abs(v[0] - q) for v, q in zip(a, ref)) / mx)
        out[name] = dict(dt=dts, edt=edt, dx=dxs, edx=edx)
        print(name, edt, edx, flush=True)
    return out


def damage_quadrature():
    out = {}
    T0 = 310.0
    A, E = model.HM["A"], model.HM["Ea"]
    # (a) constant temperature: exact
    errs = []
    for th in (10.0, 30.0, 45.0):
        T = T0 + th
        ex = A * math.exp(-E / (model.RGAS * T)) * 7.3
        num = 0.0
        for _ in range(73):
            num += fem1d.arrhenius_step(th, th, T0, A, E, 0.1, 4)
        errs.append(abs(num - ex) / ex)
    out["const"] = errs
    # (b) linear ramp theta = r t, r = 0.5 K/s for 60 s (T up to 340 K), tumour kinetics; reference by 20000 Simpson panels
    At, Et = model.tumour_arrhenius()["A"], model.tumour_arrhenius()["Ea"]
    r = 0.5; tend = 60.0
    ref = fem1d.arrhenius_step(0.0, r * tend, T0, At, Et, tend, 20000)
    rows = []
    for dt in (10.0, 5.0, 2.5, 1.25, 0.625):
        n = int(round(tend / dt))
        row = []
        for nsub in (2, 4, 8):
            s = 0.0
            for k in range(n):
                s += fem1d.arrhenius_step(r * k * dt, r * (k + 1) * dt, T0, At, Et, dt, nsub)
            row.append(abs(s - ref) / ref)
        tr = 0.0
        for k in range(n):
            ra = At * math.exp(-Et / (model.RGAS * (T0 + r * k * dt)))
            rb = At * math.exp(-Et / (model.RGAS * (T0 + r * (k + 1) * dt)))
            tr += 0.5 * dt * (ra + rb)
        row.append(abs(tr - ref) / ref)
        rows.append((dt, row))
    out["ramp"] = dict(ref=ref, rows=rows)
    print("damage quadrature", out["const"], rows[0], rows[-1], flush=True)
    return out


def production_convergence():
    """self-convergence of the nonlinear production run (temperature dependent perfusion, pulse train)"""
    des = dict(I0=2.0e5, tp=3.0, per=4.0, Np=3)
    out = {}
    keys = ("Tmax", "minOmT", "OmN_h", "JF", "sabs")
    def run_(dx, dt, picard=1):
        P = model.make("MGL")
        R = fem1d.run(P, des, dx=dx, dt=dt, picard=picard, keep=False)
        m = fem1d.metrics(R)
        return [m[k] for k in keys], R
    ref, _ = run_(6.25e-5, 0.0125, picard=8)
    out["ref"] = ref; out["keys"] = keys
    out["dt"] = []
    for dt in (0.8, 0.4, 0.2, 0.1, 0.05):
        v, _ = run_(1.25e-4, dt)
        out["dt"].append((dt, [abs(a - b) / abs(b) for a, b in zip(v, ref)]))
    out["dx"] = []
    for dx in (1e-3, 5e-4, 2.5e-4, 1.25e-4):
        v, _ = run_(dx, 0.05)
        out["dx"].append((dx, [abs(a - b) / abs(b) for a, b in zip(v, ref)]))
    v1, _ = run_(2.5e-4, 0.1, picard=1)
    v2, R2 = run_(2.5e-4, 0.1, picard=12)
    out["picard"] = [abs(a - b) / abs(b) for a, b in zip(v1, v2)]
    out["iters_mean"] = sum(R2.iters) / len(R2.iters); out["iters_max"] = max(R2.iters)
    print("prod conv", out["dt"][:2], out["dx"][:2], out["picard"], flush=True)
    return out


def energy_balance():
    out = {}
    for name in ("Pennes", "MGL", "CV"):
        for nl in (False, True):
            P = lin(name) if not nl else model.make(name)
            des = dict(I0=2.0e5, tp=3.0, per=4.0, Np=3)
            dt = 0.05
            R = fem1d.run(P, des, dx=2.5e-4, dt=dt, keep=False)
            xs = R.xs; nn = len(xs); ne = nn - 1
            Lc = P["lay"]
            # incident energy per unit area: sum of nodal loads x time factor
            q0 = fem1d.laser_load(P, xs, ne)
            fb = fem1d.fbar_array(des, R.nstep, dt)
            Ein_fe = sum(q0) * des["I0"] * sum(fb) * dt
            ls = model.laser_shape(P["las"]); mua = P["las"]["mua"]
            Ein_an = des["I0"] * des["Np"] * des["tp"] * mua * (
                ls["B1"] * ls["delta"] / ls["l1"] * (1 - math.exp(-ls["l1"] * P["L"] / ls["delta"]))
                - ls["B2"] * ls["delta"] / ls["l2"] * (1 - math.exp(-ls["l2"] * P["L"] / ls["delta"])))
            # stored energy S = int C (theta + tau0 theta_t) dx at the end (continuum form)
            tau0 = P["tau0"]
            def stored(n):
                a, b, c = R.th[n], R.th[n - 1], R.th[n - 2]
                s = 0.0
                for e in range(ne):
                    C = Lc[R.li[e]]["C"]; le = R.le[e]
                    f = lambda i: a[i] + tau0 * (1.5 * a[i] - 2 * b[i] + 0.5 * c[i]) / dt
                    s += C * le * 0.5 * (f(e) + f(e + 1))
                return s
            S_end = stored(R.nstep)
            # perfusion loss  int dt sum w g theta (trapezoid in time, lumped in space)
            pf = model.perfusion_factor
            loss = 0.0
            prevv = 0.0
            for n in range(1, R.nstep + 1):
                v = 0.0
                for e in range(ne):
                    lay = R.li[e]; le = R.le[e]
                    for i in (e, e + 1):
                        t = R.th[n][i]
                        om = Lc[lay]["om0"] * pf(P, lay, t, 0.0)
                        v += om * t * le / 2
                loss += 0.5 * dt * (v + prevv)
                prevv = v
            # boundary flux at x = L
            flux = 0.0
            for n in range(1, R.nstep + 1):
                flux += dt * Lc[1]["k"] * (R.th[n][-2] - R.th[n][-1]) / R.le[-1]
            res = Ein_fe - S_end - loss - flux
            key = name + ("_nonlinear" if nl else "_linear")
            out[key] = dict(Ein_fe=Ein_fe, Ein_an=Ein_an, S=S_end, loss=loss, flux=flux,
                            rel_src=abs(Ein_fe - Ein_an) / Ein_an, rel_res=abs(res) / Ein_fe)
            print(key, out[key], flush=True)
    return out


def quasi_static():
    out = {}
    P = lin("MGL")
    xs_m = [v * 1e-3 for v in (0, 1, 2, 3, 4, 6, 8, 12)]
    xs_l = [x if abs(x - 0.004) > 1e-9 else 0.004 - 1e-9 for x in xs_m]
    rows = []
    for t in (1.0, 3.0, 6.0, 12.0):
        a, _, _ = lap.invert(P, DES, xs_l, t, rscale=1.0, N=2500)
        b, _, _ = lap.invert(P, DES, xs_l, t, rscale=1e-4, N=2500)
        c, _, _ = lap.invert(P, DES, xs_l, t, rscale=1e-2, N=2500)
        thm = max(abs(r[0]) for r in a)
        dth = max(abs(r[0] - q[0]) for r, q in zip(a, b)) / thm
        dth2 = max(abs(r[0] - q[0]) for r, q in zip(a, c)) / thm
        sxx = max(abs(r[2]) for r in a); syy = max(abs(r[4]) for r in a)
        sxx_b = max(abs(r[2]) for r in b)
        rows.append(dict(t=t, dth=dth, dth_1e2=dth2, sxx=sxx, syy=syy, ratio=sxx / syy, sxx_qs=sxx_b))
        print("qs", rows[-1], flush=True)
    out["rows"] = rows
    c1, c2 = P["lay"][0]["cwave"], P["lay"][1]["cwave"]
    tw = P["h"] / c1 + (P["L"] - P["h"]) / c2
    out["twave"] = tw; out["c"] = [c1, c2]
    out["ratio_sq"] = (tw / 1.0) ** 2
    return out


def mgt_stability():
    out = {}
    def roots(tau, C, k, ks, kap):
        # tau C l^3 + C l^2 + k kap^2 l + ks kap^2 = 0 ; Durand-Kerner
        co = [tau * C, C, k * kap * kap, ks * kap * kap]
        co = [c / co[0] for c in co]
        z = [complex(0.4, 0.9) ** i * max(abs(c) ** (1 / (j + 1)) for j, c in enumerate(co[1:])) for i in range(3)]
        for _ in range(400):
            for i in range(3):
                p = ((z[i] + co[1]) * z[i] + co[2]) * z[i] + co[3]
                d = 1
                for j in range(3):
                    if j != i:
                        d *= (z[i] - z[j])
                z[i] -= p / d
        return z
    P = model.make("MGT")
    for tag, lit in (("literal", True), ("eta0.5", False)):
        row = []
        for kap in (10.0, 100.0, 1e3, 1e4):
            ok = []
            for i in (0, 1):
                c = P["lay"][i]
                ks = c["kstar"] if lit else 0.5 * c["k"] / P["tauq"]
                z = roots(P["tauq"], c["C"], c["k"], ks, kap)
                ok.append(max(v.real for v in z))
            row.append(ok)
        out[tag] = row
    out["tau_crit"] = [P["lay"][i]["k"] / P["lay"][i]["kstar"] for i in (0, 1)]
    print("mgt stability", out, flush=True)
    return out


if __name__ == "__main__":
    t0 = time.time()
    OUT["valid"] = validation()
    OUT["curves"] = profile_curves()
    OUT["conv_lap"] = conv_vs_laplace()
    OUT["quad"] = damage_quadrature()
    OUT["qs"] = quasi_static()
    OUT["mgt"] = mgt_stability()
    OUT["energy"] = energy_balance()
    OUT["prod"] = production_convergence()
    json.dump(OUT, open("part_valid.json", "w"))
    print("done", time.time() - t0)
