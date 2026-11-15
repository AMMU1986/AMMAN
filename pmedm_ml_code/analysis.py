#!/usr/bin/env python3
"""Full reanalysis pipeline for the PM-EDM WC-Co dataset of Singh (2022).

Run from the repository root:  python3 pmedm_ml_code/analysis.py
Writes pmedm_ml_results/results.json (all numbers quoted in the manuscript).
Standard library only; parallelised over 8 worker processes.
"""

import json
import math
import os
import random
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from core import (chol_solve, cholesky_safe, f_sf, kendall_tau_b, lstsq, mean, pearson,  # noqa: E402
                  quantile, rankdata, spearman, std, t_ppf, t_two_sided_p, var, dot, f_ppf)
from data import design_label, load_confirmation, load_runs  # noqa: E402
from decision import (critic_weights, entropy_weights, gra, hv_improvement,  # noqa: E402
                      hypervolume_2d, nondominated, nsga2, topsis)
from models import (BOUNDS, GPR, LEVELS, MODEL_KEYS, MODEL_LABELS, POWDERS,  # noqa: E402
                    GradientBoosting, LinearModel, POWERLAW_TERMS, RSM_TERMS, interval,
                    make_model, powerlaw_features, rsm_features)

OUT_DIR = os.path.join(os.path.dirname(HERE), "pmedm_ml_results")
RESP = ("mrr", "twr")
LEVELS_CAL = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95)
N_REPEATS, K_FOLDS = 10, 5

ROWS = load_runs()
XS = [r["x"] for r in ROWS]
Y = {k: [r[k] for r in ROWS] for k in RESP}
Z = {k: [math.log(v) for v in Y[k]] for k in RESP}
N = len(ROWS)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------

def r6(v):
    if isinstance(v, float):
        return round(v, 6)
    if isinstance(v, (list, tuple)):
        return [r6(u) for u in v]
    if isinstance(v, dict):
        return {k: r6(u) for k, u in v.items()}
    return v


def logpdf(dist, z):
    if dist[0] == "normal":
        _, m, s = dist
        return -0.5 * math.log(2 * math.pi * s * s) - 0.5 * ((z - m) / s) ** 2
    if dist[0] == "t":
        _, m, s, df = dist
        u = (z - m) / s
        return (math.lgamma(0.5 * (df + 1)) - math.lgamma(0.5 * df)
                - 0.5 * math.log(df * math.pi) - math.log(s)
                - 0.5 * (df + 1) * math.log1p(u * u / df))
    raise ValueError


def anova_main_effects(y):
    """Main-effects ANOVA for the four 3-level factors of the L27 design."""
    grand = mean(y)
    sst = sum((v - grand) ** 2 for v in y)
    keys = [("A (t_off)", lambda x: x[0]), ("B (t_on)", lambda x: x[1]),
            ("C (powder)", lambda x: x[3]), ("D (current)", lambda x: x[2])]
    out = {}
    ss_f = 0.0
    for name, fn in keys:
        groups = {}
        for x, v in zip(XS, y):
            groups.setdefault(fn(x), []).append(v)
        ss = sum(len(g) * (mean(g) - grand) ** 2 for g in groups.values())
        out[name] = {"ss": ss, "levels": {str(k): mean(g) for k, g in groups.items()}}
        ss_f += ss
    sse = sst - ss_f
    df_e = N - 1 - 8
    mse = sse / df_e
    for name in out:
        f = (out[name]["ss"] / 2) / mse
        out[name].update({"df": 2, "F": f, "p": f_sf(f, 2, df_e), "pct": 100 * out[name]["ss"] / sst})
    out["Error"] = {"ss": sse, "df": df_e, "pct": 100 * sse / sst}
    out["Total"] = {"ss": sst, "df": N - 1}
    out["F_crit_0.05"] = f_ppf(0.95, 2, df_e)
    return out


# ----------------------------------------------------------------------------
# 1. Consistency audit of the published analysis
# ----------------------------------------------------------------------------

def audit():
    mrr, twr = Y["mrr"], Y["twr"]
    nb, nc, grc, grg = gra(mrr, twr)
    res = {}
    r = pearson(mrr, twr)
    t = r * math.sqrt((N - 2) / (1 - r * r))
    tcrit = t_ppf(0.975, N - 2)
    res["corr_mrr_twr"] = {"r": r, "p": t_two_sided_p(t, N - 2),
                           "r_crit_0.05": tcrit / math.sqrt(N - 2 + tcrit ** 2),
                           "spearman": spearman(mrr, twr)}
    rows = []
    for i, row in enumerate(ROWS):
        rep = row["rep"]
        rows.append({
            "run": row["run"], "label": design_label(row["x"]),
            "norm_mrr": nb[i], "norm_twr": nc[i], "grc_mrr": grc[i][0], "grc_twr": grc[i][1],
            "grg": grg[i],
            "rep_norm_mrr": rep["mrr_norm_reported"], "rep_norm_twr": rep["twr_norm_reported"],
            "rep_grc_mrr": rep["grc_mrr_reported"], "rep_grc_twr": rep["grc_twr_reported"],
            "rep_grg": rep["grg_reported"], "rep_rank": row["rank_grg"],
            "rep_ganfis": rep["ganfis_reported"], "rep_rank_ganfis": row["rank_ganfis"],
        })
    ranks = rankdata([-g for g in grg])
    for rr, k in zip(rows, ranks):
        rr["rank"] = k
    res["gra_rows"] = rows
    res["max_abs_diff_norm"] = max(max(abs(a["norm_mrr"] - a["rep_norm_mrr"]),
                                       abs(a["norm_twr"] - a["rep_norm_twr"])) for a in rows)
    res["discrepancies"] = [
        {k: a[k] for k in ("run", "grc_mrr", "rep_grc_mrr", "grc_twr", "rep_grc_twr", "grg",
                           "rep_grg", "rank", "rep_rank")}
        for a in rows
        if abs(a["grc_mrr"] - a["rep_grc_mrr"]) > 0.005 or abs(a["grc_twr"] - a["rep_grc_twr"]) > 0.005
        or abs(a["grg"] - a["rep_grg"]) > 0.005]
    res["anova_grg_recomputed"] = anova_main_effects(grg)
    res["anova_grg_reported"] = anova_main_effects([row["rep"]["grg_reported"] for row in ROWS])
    res["anova_ganfis_reported"] = anova_main_effects([row["rep"]["ganfis_reported"] for row in ROWS])

    # Linear regression of Eq. (8) in the source paper: abrasive coded 1, 2, 3
    def lin(y):
        xm = [[1.0, x[1], x[0], x[2], float(x[3] + 1)] for x in XS]
        beta, xtx_inv = lstsq(xm, y, ridge=1e-14)
        fit = [dot(beta, f) for f in xm]
        sse = sum((a - b) ** 2 for a, b in zip(y, fit))
        sst = sum((a - mean(y)) ** 2 for a in y)
        r2 = 1 - sse / sst
        p = 4
        fstat = ((sst - sse) / p) / (sse / (N - p - 1))
        return {"beta[const,t_on,t_off,I,abrasive]": beta, "R2": r2,
                "R2_adj": 1 - (1 - r2) * (N - 1) / (N - p - 1), "F": fstat,
                "SS_reg": sst - sse, "SS_res": sse, "SS_tot": sst,
                "S": math.sqrt(sse / (N - p - 1))}

    res["regression_grg_reported"] = lin([row["rep"]["grg_reported"] for row in ROWS])
    res["regression_grg_recomputed"] = lin(grg)
    res["regression_ganfis_reported"] = lin([row["rep"]["ganfis_reported"] for row in ROWS])

    # implied R2 from the ANOVA tables printed in the paper (Table 10)
    res["implied_from_table10"] = {"R2_grg": 0.16 / 0.24, "R2_ganfis": 0.16 / 0.22,
                                   "R2_from_F_grg": (11.33 * 4 / 22) / (1 + 11.33 * 4 / 22),
                                   "R2_from_F_ganfis": (14.81 * 4 / 22) / (1 + 14.81 * 4 / 22),
                                   "adjR2_if_R2_0.8891": 1 - (1 - 0.8891) * 26 / 22}
    # replicate (pure-error) information at A2B3C1D3: run 24 + three confirmation runs
    conf = load_confirmation()
    rep_mrr = [Y["mrr"][23]] + [c["mrr"] for c in conf]
    rep_twr = [Y["twr"][23]] + [c["twr"] for c in conf]
    res["replicates"] = {
        "mrr": rep_mrr, "twr": rep_twr,
        "sd_mrr": std(rep_mrr), "sd_twr": std(rep_twr),
        "sd_ln_mrr": std([math.log(v) for v in rep_mrr]),
        "sd_ln_twr": std([math.log(v) for v in rep_twr]),
        "cv_mrr_pct": 100 * std(rep_mrr) / mean(rep_mrr),
        "cv_twr_pct": 100 * std(rep_twr) / mean(rep_twr),
        "conf_mean_mrr": mean([c["mrr"] for c in conf]),
        "conf_mean_twr": mean([c["twr"] for c in conf]),
    }
    # aliasing structure: powder level == (D - A + B) mod 3 in level codes
    def code(v, j):
        return min(range(3), key=lambda k: abs(LEVELS[j][k] - v))

    res["alias_check"] = all(x[3] == (code(x[2], 2) - code(x[0], 0) + code(x[1], 1)) % 3 for x in XS)
    # observed Pareto set (maximise MRR, minimise TWR)
    pts = [(-a, b) for a, b in zip(mrr, twr)]
    nd = nondominated(pts)
    res["observed_pareto_runs"] = sorted(ROWS[i]["run"] for i in nd)
    return res, grg


# ----------------------------------------------------------------------------
# 2. Cross-validation
# ----------------------------------------------------------------------------

def make_folds():
    folds = {"loo": [[[i] for i in range(N)]]}
    rk = []
    for r in range(N_REPEATS):
        rng = random.Random(2024 + r)
        perm = list(range(N))
        rng.shuffle(perm)
        rk.append([sorted(perm[k::K_FOLDS]) for k in range(K_FOLDS)])
    folds["rkf"] = rk
    return folds


def run_task(task):
    key, resp, scheme, rep, fold, test_idx = task
    train_idx = [i for i in range(N) if i not in test_idx]
    xs = [XS[i] for i in train_idx]
    z = [Z[resp][i] for i in train_idx]
    seed = 101 + 31 * rep + fold
    t0 = time.time()
    model = make_model(key, seed=seed, resp=resp).fit(xs, z)
    preds = model.predict([XS[i] for i in test_idx])
    out = {"key": key, "resp": resp, "scheme": scheme, "rep": rep, "fold": fold,
           "test": test_idx, "pred": preds, "sec": time.time() - t0}
    if key == "gpr":
        out["theta"] = model.theta
    return out


def run_jackknife_task(task):
    """Jackknife+ for one outer LOO fold (base model: 'gpr' or 'xgb')."""
    key, resp, j = task
    train_idx = [i for i in range(N) if i != j]
    if key == "gpr":
        outer = GPR(seed=101 + j).fit([XS[i] for i in train_idx], [Z[resp][i] for i in train_idx])
        theta = outer.theta
    mus_test, resid = [], []
    for i in train_idx:
        inner_idx = [k for k in train_idx if k != i]
        xs = [XS[k] for k in inner_idx]
        z = [Z[resp][k] for k in inner_idx]
        if key == "gpr":
            m = GPR(fixed_theta=theta).fit(xs, z)
            pi, pj = [d[1] for d in m.predict([XS[i], XS[j]])]
        else:
            m = GradientBoosting(seed=101 + j).fit(xs, z)
            pi, pj = m.predict_point([XS[i], XS[j]])
        resid.append(abs(Z[resp][i] - pi))
        mus_test.append(pj)
    return {"key": key, "resp": resp, "j": j, "mu": mus_test, "R": resid}


def jackknife_interval(mu, resid, level):
    n = len(mu)
    alpha = 1.0 - level
    lo_vals = sorted(m - r for m, r in zip(mu, resid))
    hi_vals = sorted(m + r for m, r in zip(mu, resid))
    k_lo = int(math.floor(alpha * (n + 1)))
    k_hi = int(math.ceil((1 - alpha) * (n + 1)))
    lo = lo_vals[k_lo - 1] if k_lo >= 1 else -float("inf")
    hi = hi_vals[k_hi - 1] if k_hi <= n else float("inf")
    return lo, hi


def point_metrics(y, yhat):
    err = [a - b for a, b in zip(y, yhat)]
    ybar = mean(y)
    press = sum(e * e for e in err)
    z = [math.log(a) for a in y]
    zbar = mean(z)
    with_overflow = any(b > 1e6 or b < 1e-6 for b in yhat)
    zhat = [math.log(min(max(b, 1e-300), 1e300)) for b in yhat]
    return {"RMSE": math.sqrt(press / len(y)), "MAE": mean([abs(e) for e in err]),
            "MAPE": 100 * mean([abs(e) / a for e, a in zip(err, y)]),
            "Q2": 1 - press / sum((a - ybar) ** 2 for a in y),
            "Q2_log": 1 - sum((a - b) ** 2 for a, b in zip(z, zhat)) / sum((a - zbar) ** 2 for a in z),
            "RMSLE": math.sqrt(mean([(a - b) ** 2 for a, b in zip(z, zhat)])),
            "diverged": 1.0 if with_overflow else 0.0}


def safe_exp(v):
    return math.exp(min(v, 690.0))


def prob_metrics(y, dists):
    z = [math.log(v) for v in y]
    out = {"NLL": mean([-logpdf(d, zi) for d, zi in zip(dists, z)])}
    cal = {}
    for lev in LEVELS_CAL:
        ivs = [interval(d, lev) for d in dists]
        cal[str(lev)] = mean([1.0 if lo <= zi <= hi else 0.0 for (lo, hi), zi in zip(ivs, z)])
        if lev in (0.9, 0.95):
            out["PICP%d" % round(lev * 100)] = cal[str(lev)]
            out["MPIW%d" % round(lev * 100)] = mean([math.exp(hi) - math.exp(lo) for lo, hi in ivs])
    out["calibration"] = cal
    out["miscal_area"] = mean([abs(cal[str(l)] - l) for l in LEVELS_CAL])
    return out


def summarise_cv(results, jk):
    summ = {}
    for resp in RESP:
        y = Y[resp]
        summ[resp] = {}
        for key in MODEL_KEYS:
            loo = [r for r in results if r["key"] == key and r["resp"] == resp and r["scheme"] == "loo"]
            preds = [None] * N
            for r in loo:
                for i, d in zip(r["test"], r["pred"]):
                    preds[i] = d
            yhat = [safe_exp(d[1]) for d in preds]
            entry = {"loo": point_metrics(y, yhat), "loo_pred": [d[1] for d in preds]}
            if preds[0][0] != "point":
                entry["loo"].update(prob_metrics(y, preds))
                entry["loo_dist"] = preds
            rk = []
            rk_pred = []
            for rep in range(N_REPEATS):
                rr = [r for r in results if r["key"] == key and r["resp"] == resp
                      and r["scheme"] == "rkf" and r["rep"] == rep]
                pr = [None] * N
                for r in rr:
                    for i, d in zip(r["test"], r["pred"]):
                        pr[i] = d
                rk_pred.append([d[1] for d in pr])
                m = point_metrics(y, [safe_exp(d[1]) for d in pr])
                if pr[0][0] != "point":
                    pm = prob_metrics(y, pr)
                    m.update({k: v for k, v in pm.items() if k != "calibration"})
                rk.append(m)
            entry["rkf"] = {k: {"mean": mean([m[k] for m in rk]), "sd": std([m[k] for m in rk]),
                                "median": quantile([m[k] for m in rk], 0.5)}
                            for k in rk[0]}
            entry["rkf_pred"] = rk_pred
            entry["fit_sec"] = mean([r["sec"] for r in loo])
            summ[resp][key] = entry
        # jackknife+ conformal intervals
        for base in ("gpr", "xgb"):
            rows = sorted([r for r in jk if r["key"] == base and r["resp"] == resp],
                          key=lambda r: r["j"])
            z = [math.log(v) for v in y]
            cal, widths = {}, {}
            for lev in LEVELS_CAL:
                ivs = [jackknife_interval(r["mu"], r["R"], lev) for r in rows]
                cal[str(lev)] = mean([1.0 if lo <= zi <= hi else 0.0 for (lo, hi), zi in zip(ivs, z)])
                widths[str(lev)] = mean([math.exp(hi) - math.exp(lo) for lo, hi in ivs])
            summ[resp]["jk+_" + base] = {"loo": {
                "PICP90": cal["0.9"], "PICP95": cal["0.95"], "MPIW90": widths["0.9"],
                "MPIW95": widths["0.95"], "calibration": cal,
                "miscal_area": mean([abs(cal[str(l)] - l) for l in LEVELS_CAL])}}
    return summ


# ----------------------------------------------------------------------------
# 3. Full-data models, interpretation and optimisation
# ----------------------------------------------------------------------------

def shapley_exact(f, x, background):
    """Exact interventional Shapley values for 4 features (powder treated as one feature)."""
    m = 4
    cache = {}

    def v(mask):
        if mask in cache:
            return cache[mask]
        pts = []
        for b in background:
            pts.append(tuple(x[j] if (mask >> j) & 1 else b[j] for j in range(m)))
        val = mean(f(pts))
        cache[mask] = val
        return val

    phi = []
    for j in range(m):
        s = 0.0
        for mask in range(1 << m):
            if (mask >> j) & 1:
                continue
            k = bin(mask).count("1")
            w = math.factorial(k) * math.factorial(m - k - 1) / math.factorial(m)
            s += w * (v(mask | (1 << j)) - v(mask))
        phi.append(s)
    return phi, v(0)


FEATURE_NAMES = ["A (t_off)", "B (t_on)", "D (current)", "C (powder)"]


def full_data_analysis(cv_summary):
    res = {}
    gp = {resp: GPR(seed=7, n_starts=6).fit(XS, Z[resp]) for resp in RESP}
    res["gpr_hyper"] = {resp: dict(gp[resp].hyper(), edof=gp[resp].effective_dof(),
                                   neg_log_post=gp[resp].obj) for resp in RESP}
    # linear models: coefficients
    lin = {}
    for name, fn, terms in (("rsm", rsm_features, RSM_TERMS),
                            ("powerlaw", powerlaw_features, POWERLAW_TERMS)):
        lin[name] = {}
        for resp in RESP:
            m = LinearModel(name, fn, terms).fit(XS, Z[resp])
            tq = t_ppf(0.975, m.dof)
            lin[name][resp] = {"terms": terms, "beta": m.beta, "se": m.se,
                               "p": [t_two_sided_p(b / s, m.dof) if s > 0 else None
                                     for b, s in zip(m.beta, m.se)],
                               "ci95": [[b - tq * s, b + tq * s] for b, s in zip(m.beta, m.se)],
                               "R2_fit": m.r2, "s": math.sqrt(m.s2), "dof": m.dof}
    res["linear"] = lin
    # parameter counts and in-sample (training) R2 on the log scale with all 27 runs
    counts, train_r2 = {}, {}
    for key in MODEL_KEYS:
        counts[key], train_r2[key] = {}, {}
        for resp in RESP:
            m = make_model(key, seed=7, resp=resp).fit(XS, Z[resp])
            counts[key][resp] = m.n_params()
            zhat = [d[1] for d in m.predict(XS)]
            zbar = mean(Z[resp])
            train_r2[key][resp] = 1 - (sum((a - b) ** 2 for a, b in zip(Z[resp], zhat))
                                       / sum((a - zbar) ** 2 for a in Z[resp]))
    res["n_params"] = counts
    res["train_r2_log"] = train_r2
    res["gpr_pe_hyper"] = {resp: GPR(seed=7, n_starts=6, fixed_noise_sd_log=__import__("models").PURE_ERROR_SD_LOG[resp]).fit(XS, Z[resp]).hyper()
                           for resp in RESP}
    # ANOVA on ln responses and raw responses
    res["anova"] = {resp: {"ln": anova_main_effects(Z[resp]), "raw": anova_main_effects(Y[resp])}
                    for resp in RESP}
    # SHAP (exact) for GPR and XGB on the log scale
    xgb = {resp: GradientBoosting(seed=7).fit(XS, Z[resp]) for resp in RESP}
    shap = {}
    for resp in RESP:
        shap[resp] = {}
        for name, fn in (("gpr", gp[resp].latent_mean), ("xgb", xgb[resp].predict_point)):
            vals = []
            base = None
            for x in XS:
                phi, base = shapley_exact(fn, x, XS)
                vals.append(phi)
            imp = [mean([abs(v[j]) for v in vals]) for j in range(4)]
            tot = sum(imp)
            shap[resp][name] = {"base": base, "values": vals, "mean_abs": imp,
                                "share_pct": [100 * v / tot for v in imp]}
    res["shap"] = shap
    # Partial dependence (GPR, original scale), per powder and averaged
    pdp = {}
    for resp in RESP:
        pdp[resp] = {}
        for j, (lo, hi) in enumerate(BOUNDS):
            grid = [lo + (hi - lo) * k / 24 for k in range(25)]
            curves = {}
            for c in range(3):
                curve = []
                for g in grid:
                    pts = []
                    for b in XS:
                        q = list(b)
                        q[j] = g
                        q[3] = c
                        pts.append(tuple(q))
                    curve.append(mean([math.exp(v) for v in gp[resp].latent_mean(pts)]))
                curves[POWDERS[c]] = curve
            avg = []
            for g in grid:
                pts = []
                for b in XS:
                    q = list(b)
                    q[j] = g
                    pts.append(tuple(q))
                avg.append(mean([math.exp(v) for v in gp[resp].latent_mean(pts)]))
            curves["average"] = avg
            pdp[resp][FEATURE_NAMES[j]] = {"grid": grid, "curves": curves}
        pc = {}
        for c in range(3):
            pts = [(b[0], b[1], b[2], c) for b in XS]
            pc[POWDERS[c]] = mean([math.exp(v) for v in gp[resp].latent_mean(pts)])
        pdp[resp]["C (powder)"] = pc
    res["pdp"] = pdp
    return res, gp


def evaluate_point(gp, x):
    out = {}
    for resp in RESP:
        (m, v), = gp[resp].latent([x])
        noise = gp[resp].zs ** 2 * gp[resp].sn2
        s_pred = math.sqrt(v + noise)
        out[resp] = {"median": math.exp(m), "latent_sd_log": math.sqrt(v),
                     "pred_sd_log": s_pred,
                     "ci95_mean": [math.exp(m - 1.96 * math.sqrt(v)), math.exp(m + 1.96 * math.sqrt(v))],
                     "pi95": [math.exp(m - 1.96 * s_pred), math.exp(m + 1.96 * s_pred)]}
    return out


def optimisation(gp, audit_res):
    res = {}
    zq = 1.6448536269514722
    fronts = {}
    for mode in ("nominal", "robust"):
        allx, allo = [], []
        for c in range(3):
            def evaluate(v, c=c):
                x = (v[0], v[1], v[2], c)
                (mm, vm), = gp["mrr"].latent([x])
                (mt, vt), = gp["twr"].latent([x])
                if mode == "nominal":
                    return (-math.exp(mm), math.exp(mt))
                return (-math.exp(mm - zq * math.sqrt(vm)), math.exp(mt + zq * math.sqrt(vt)))
            pop, objs = nsga2(evaluate, BOUNDS, pop_size=100, generations=150, seed=11 + c)
            for p, o in zip(pop, objs):
                allx.append((p[0], p[1], p[2], c))
                allo.append(o)
        nd = nondominated(allo)
        nd = sorted(nd, key=lambda i: allo[i][1])
        fronts[mode] = {"x": [allx[i] for i in nd], "obj": [allo[i] for i in nd]}
        per = {}
        ref = (-min(Y["mrr"]), max(Y["twr"]))
        for c in range(3):
            pts = [allo[i] for i in range(len(allo)) if allx[i][3] == c]
            per[POWDERS[c]] = hypervolume_2d([pts[i] for i in nondominated(pts)], ref)
        fronts[mode]["hv_by_powder"] = per
        fronts[mode]["hv"] = hypervolume_2d(fronts[mode]["obj"], ref)
        fronts[mode]["powder_share"] = {POWDERS[c]: sum(1 for x in fronts[mode]["x"] if x[3] == c)
                                        / len(fronts[mode]["x"]) for c in range(3)}
    obs_pts = [(-a, b) for a, b in zip(Y["mrr"], Y["twr"])]
    ref = (-min(Y["mrr"]), max(Y["twr"]))
    res["hv_reference"] = [min(Y["mrr"]), max(Y["twr"])]
    res["hv_observed"] = hypervolume_2d([obs_pts[i] for i in nondominated(obs_pts)], ref)
    # TOPSIS on the nominal front (benefit MRR, cost TWR)
    sel = {}
    for mode in ("nominal", "robust"):
        objs = fronts[mode]["obj"]
        mat = [[-o[0], o[1]] for o in objs]
        flags = [True, False]
        we = entropy_weights(mat)
        wc = critic_weights(mat, flags)
        sel[mode] = {}
        for wname, w in (("entropy", we), ("critic", wc), ("equal", [0.5, 0.5])):
            cc = topsis(mat, w, flags)
            k = max(range(len(cc)), key=lambda i: cc[i])
            x = fronts[mode]["x"][k]
            sel[mode][wname] = {"weights": w, "x": x, "cc": cc[k],
                                "pred": evaluate_point(gp, x)}
    res["fronts"] = fronts
    res["topsis_front"] = sel

    # TOPSIS and GRA on the 27 experimental runs
    mat = [[a, b] for a, b in zip(Y["mrr"], Y["twr"])]
    flags = [True, False]
    rank_tab = {}
    we, wc = entropy_weights(mat), critic_weights(mat, flags)
    _, _, _, grg = gra(Y["mrr"], Y["twr"])
    scores = {"GRA (recomputed)": grg,
              "GRG (reported)": [r["rep"]["grg_reported"] for r in ROWS],
              "G-ANFIS (reported)": [r["rep"]["ganfis_reported"] for r in ROWS],
              "TOPSIS-entropy": topsis(mat, we, flags),
              "TOPSIS-CRITIC": topsis(mat, wc, flags),
              "TOPSIS-equal": topsis(mat, [0.5, 0.5], flags)}
    for name, s in scores.items():
        order = sorted(range(N), key=lambda i: -s[i])
        rank_tab[name] = {"top5_runs": [ROWS[i]["run"] for i in order[:5]], "scores": s,
                          "ranks": rankdata([-v for v in s])}
    names = list(scores)
    corr = {a: {b: {"spearman": spearman(scores[a], scores[b]),
                    "kendall": kendall_tau_b(scores[a], scores[b])} for b in names} for a in names}
    res["run_ranking"] = {"weights_entropy": we, "weights_critic": wc, "table": rank_tab,
                          "corr": corr}

    # Posterior probability that each of the 81 level combinations is Pareto-optimal
    combos = [(a, b, d, c) for a in LEVELS[0] for b in LEVELS[1] for d in LEVELS[2] for c in range(3)]
    joint = {}
    for resp in RESP:
        mu, cov = gp[resp].latent_joint(combos)
        joint[resp] = (mu, cholesky_safe(cov, start_jitter=1e-9))
    rng = random.Random(5)
    n_s = 2000
    cnt_pareto = [0] * len(combos)
    cnt_gra = [0] * len(combos)
    cnt_top = [0] * len(combos)
    cnt_maxmrr = [0] * len(combos)
    for _ in range(n_s):
        ys = {}
        for resp in RESP:
            mu, low = joint[resp]
            e = [rng.gauss(0.0, 1.0) for _ in combos]
            ys[resp] = [math.exp(m + dot(row[:k + 1], e[:k + 1])) for k, (m, row) in enumerate(zip(mu, low))]
        pts = [(-a, b) for a, b in zip(ys["mrr"], ys["twr"])]
        for i in nondominated(pts):
            cnt_pareto[i] += 1
        _, _, _, g = gra(ys["mrr"], ys["twr"])
        cnt_gra[max(range(len(g)), key=lambda i: g[i])] += 1
        m2 = [[a, b] for a, b in zip(ys["mrr"], ys["twr"])]
        cc = topsis(m2, entropy_weights(m2), [True, False])
        cnt_top[max(range(len(cc)), key=lambda i: cc[i])] += 1
        cnt_maxmrr[max(range(len(combos)), key=lambda i: ys["mrr"][i])] += 1
    tab = []
    for i, x in enumerate(combos):
        tab.append({"label": design_label(x), "x": x, "p_pareto": cnt_pareto[i] / n_s,
                    "p_gra_best": cnt_gra[i] / n_s, "p_topsis_best": cnt_top[i] / n_s,
                    "p_max_mrr": cnt_maxmrr[i] / n_s,
                    "mrr_median": math.exp(joint["mrr"][0][i]), "twr_median": math.exp(joint["twr"][0][i]),
                    "observed": any(tuple(x) == tuple(r["x"]) for r in ROWS)})
    tab.sort(key=lambda r: -r["p_pareto"])
    res["level_combos"] = tab
    res["published_optimum"] = {"x": (50.0, 100.0, 9.0, 0),
                                "full_model": evaluate_point(gp, (50.0, 100.0, 9.0, 0))}
    return res


def bayes_opt(gp, n_suggest=3, n_mc=128):
    """Greedy batch MC-EHVI with the kriging-believer heuristic over a fine grid."""
    grid = [(a, b, d, c)
            for a in [10.0 + 5 * k for k in range(14)]
            for b in [15.0 + 5 * k for k in range(18)]
            for d in [3.0 + 0.5 * k for k in range(13)]
            for c in range(3)]
    ref = (-min(Y["mrr"]), max(Y["twr"]))
    front = [(-a, b) for a, b in zip(Y["mrr"], Y["twr"])]
    front = [front[i] for i in nondominated(front)]
    rng = random.Random(3)
    eps = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n_mc)]
    xs_aug = list(XS)
    z_aug = {resp: list(Z[resp]) for resp in RESP}
    models = dict(gp)
    out = []
    for step in range(n_suggest):
        base_hv = hypervolume_2d(front, ref)
        lm = models["mrr"].latent(grid)
        lt = models["twr"].latent(grid)
        best = None
        for i, x in enumerate(grid):
            (mm, vm), (mt, vt) = lm[i], lt[i]
            sm, st = math.sqrt(vm), math.sqrt(vt)
            tot = 0.0
            for e1, e2 in eps:
                y = (-math.exp(mm + sm * e1), math.exp(mt + st * e2))
                tot += hv_improvement(front, ref, y, base_hv)
            ehvi = tot / n_mc
            if best is None or ehvi > best[0]:
                best = (ehvi, i)
        ehvi, i = best
        x = grid[i]
        pred = {"mrr": math.exp(lm[i][0]), "twr": math.exp(lt[i][0]),
                "mrr_ci95": [math.exp(lm[i][0] - 1.96 * math.sqrt(lm[i][1])),
                             math.exp(lm[i][0] + 1.96 * math.sqrt(lm[i][1]))],
                "twr_ci95": [math.exp(lt[i][0] - 1.96 * math.sqrt(lt[i][1])),
                             math.exp(lt[i][0] + 1.96 * math.sqrt(lt[i][1]))]}
        out.append({"step": step + 1, "x": x, "ehvi": ehvi, "pred": pred,
                    "hv_before": base_hv})
        # kriging believer: fantasise the posterior mean and refit with fixed hyperparameters
        xs_aug.append(x)
        for resp, (m_, _) in (("mrr", lm[i]), ("twr", lt[i])):
            z_aug[resp].append(m_)
            models[resp] = GPR(fixed_theta=gp[resp].theta).fit(xs_aug, z_aug[resp])
        front = front + [(-pred["mrr"], pred["twr"])]
        front = [front[k] for k in nondominated(front)]
    return {"grid_size": len(grid), "n_mc": n_mc, "suggestions": out}


def loo_q2_ols_perm(feature_fn, z, n_perm=5000, seed=9):
    """LOO Q2 (log scale) of an OLS model and its permutation p-value (hat-matrix shortcut)."""
    x_mat = [feature_fn(x) for x in XS]
    _, xtx_inv = lstsq(x_mat, z, ridge=1e-12)
    hat = [[dot(xi, [dot(row, xj) for row in xtx_inv]) for xj in x_mat] for xi in x_mat]

    def q2(zv):
        fit = [dot(row, zv) for row in hat]
        zbar = mean(zv)
        press = sum(((a - b) / (1 - hat[i][i])) ** 2 for i, (a, b) in enumerate(zip(zv, fit)))
        return 1 - press / sum((a - zbar) ** 2 for a in zv)

    obs = q2(z)
    rng = random.Random(seed)
    null = []
    for _ in range(n_perm):
        zp = list(z)
        rng.shuffle(zp)
        null.append(q2(zp))
    return {"q2_loo": obs, "p_perm": (1 + sum(1 for v in null if v >= obs)) / (n_perm + 1),
            "null_q95": quantile(null, 0.95), "n_perm": n_perm}


def gpr_perm_task(task):
    resp, seed = task
    z = list(Z[resp])
    if seed > 0:
        random.Random(seed).shuffle(z)
    m = GPR(seed=seed, n_starts=3).fit(XS, z)
    loo = m.loo_from_fixed()
    zbar = mean(z)
    return resp, seed, 1 - sum((a - b[0]) ** 2 for a, b in zip(z, loo)) / sum((a - zbar) ** 2 for a in z)


def taguchi_additive_check(grg):
    """Additive (Taguchi) prediction of the GRG at A2B3C1D3, in-sample and with run 24 held out."""
    opt = (50.0, 100.0, 9.0, 0)
    keys = (0, 1, 2, 3)

    def predict(idx):
        vals = [grg[i] for i in idx]
        mu = mean(vals)
        s = mu
        for k in keys:
            lv = [grg[i] for i in idx if XS[i][k] == opt[k]]
            s += mean(lv) - mu
        return s

    return {"observed_grg_run24": grg[23], "in_sample": predict(list(range(N))),
            "run24_held_out": predict([i for i in range(N) if i != 23])}


def published_optimum_checks(cv_summary, gp):
    """LOO (run 24 held out) prediction at A2B3C1D3 versus the confirmation runs."""
    conf = load_confirmation()
    out = {}
    for resp in RESP:
        obs = [Y[resp][23]] + [c[resp] for c in conf]
        out[resp] = {}
        for key in ("gpr", "gpr_pe", "rsm", "powerlaw", "taguchi", "mcdrop", "deepens", "xgb", "rf",
                    "anfis2", "anfis3"):
            e = cv_summary[resp][key]
            zhat = e["loo_pred"][23]
            full = make_model(key, seed=7, resp=resp).fit(XS, Z[resp]).predict([XS[23]])[0]
            entry = {"loo_median": math.exp(zhat), "in_sample_median": math.exp(full[1])}
            if "loo_dist" in e:
                d = e["loo_dist"][23]
                lo, hi = interval(d, 0.95)
                entry["pi95"] = [math.exp(lo), math.exp(hi)]
                entry["covers_all_replicates"] = all(math.exp(lo) <= v <= math.exp(hi) for v in obs)
            entry["abs_pct_error_vs_conf_mean"] = 100 * abs(math.exp(zhat) - mean([c[resp] for c in conf])) / mean([c[resp] for c in conf])
            out[resp][key] = entry
        out[resp]["observations"] = obs
    return out


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.time()
    results = {"meta": {"n_runs": N, "models": MODEL_KEYS, "labels": MODEL_LABELS,
                        "repeats": N_REPEATS, "folds": K_FOLDS}}
    aud, _ = audit()
    results["audit"] = aud
    print("audit done %.1fs" % (time.time() - t0), flush=True)

    folds = make_folds()
    tasks = []
    heavy = ("deepens", "mcdrop", "anfis3", "anfis2", "gpr")
    for key in sorted(MODEL_KEYS, key=lambda k: 0 if k in heavy else 1):
        for resp in RESP:
            for f, test in enumerate(folds["loo"][0]):
                tasks.append((key, resp, "loo", 0, f, test))
            for rep, fl in enumerate(folds["rkf"]):
                for f, test in enumerate(fl):
                    tasks.append((key, resp, "rkf", rep, f, test))
    jk_tasks = [(base, resp, j) for base in ("gpr", "xgb") for resp in RESP for j in range(N)]
    perm_tasks = [(resp, s) for resp in RESP for s in range(0, 201)]
    with Pool(8) as pool:
        cv = pool.map(run_task, tasks, chunksize=1)
        print("cv done %.1fs (%d tasks)" % (time.time() - t0, len(tasks)), flush=True)
        jk = pool.map(run_jackknife_task, jk_tasks, chunksize=1)
        print("jackknife+ done %.1fs" % (time.time() - t0), flush=True)
        perm = pool.map(gpr_perm_task, perm_tasks, chunksize=2)
        print("permutation tests done %.1fs" % (time.time() - t0), flush=True)
    summary = summarise_cv(cv, jk)
    results["cv"] = summary
    results["folds_rkf"] = folds["rkf"]
    ptest = {}
    for resp in RESP:
        obs = [q for r, s, q in perm if r == resp and s == 0][0]
        null = [q for r, s, q in perm if r == resp and s > 0]
        ptest[resp] = {
            "gpr": {"q2_loo_fixed_hyper": obs, "p_perm": (1 + sum(1 for v in null if v >= obs)) / (len(null) + 1),
                    "null_q95": quantile(null, 0.95), "n_perm": len(null)},
            "powerlaw": loo_q2_ols_perm(powerlaw_features, Z[resp]),
            "rsm": loo_q2_ols_perm(rsm_features, Z[resp]),
        }
    results["permutation"] = ptest
    grg_rec = gra(Y["mrr"], Y["twr"])[3]
    results["audit"]["taguchi_additive_grg"] = taguchi_additive_check(grg_rec)

    full, gp = full_data_analysis(summary)
    results["full"] = full
    print("full-data analysis done %.1fs" % (time.time() - t0), flush=True)
    results["optimum_check"] = published_optimum_checks(summary, gp)
    results["optimisation"] = optimisation(gp, aud)
    print("optimisation done %.1fs" % (time.time() - t0), flush=True)
    results["bo"] = bayes_opt(gp)
    print("BO done %.1fs" % (time.time() - t0), flush=True)
    with open(os.path.join(OUT_DIR, "results.json"), "w") as fh:
        json.dump(r6(results), fh, indent=1)
    print("written results.json  total %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
