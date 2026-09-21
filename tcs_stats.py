#!/usr/bin/env python3
"""
Statistical engine for the research article:
"Burden of Topical Corticosteroid Misuse: Self-Medicated vs Prescribed Use"

Generates a SYNTHETIC, literature-calibrated cohort of dermatology outpatients
and computes genuine inferential statistics using ONLY the Python standard
library (no numpy/scipy). Results are written to tcs_results.json and printed.

Calibration anchors (from published literature):
  - ~90% adverse-effect rate among unsupervised facial TC users (Saraswat 2011)
  - Majority of TC reaches patients without valid prescription
  - Steroid-modified tinea ~2.4x direct cost of steroid-naive disease
  - TSDF in ~40-45% of chronic facial misusers
This is a MODELLED dataset for methodological illustration, not real patients.
"""
import random
import math
import json
import os

SEED = 20260921
random.seed(SEED)
N = 1200

# ----------------------------------------------------------------------
# Math helpers (stdlib only)
# ----------------------------------------------------------------------
def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def norm_sf(x):
    return 1.0 - norm_cdf(x)

def two_sided_z_p(z):
    return 2.0 * norm_sf(abs(z))

def chi2_p_df1(x):
    # survival function of chi-square with 1 df: erfc(sqrt(x/2))
    return math.erfc(math.sqrt(x / 2.0))

def chi2_2x2(a, b, c, d):
    """Pearson chi-square with Yates continuity correction for a 2x2 table.
       Table: [[a,b],[c,d]]. Returns (chi2, p)."""
    n = a + b + c + d
    row1, row2 = a + b, c + d
    col1, col2 = a + c, b + d
    chi2 = 0.0
    obs = [a, b, c, d]
    exp = [row1 * col1 / n, row1 * col2 / n, row2 * col1 / n, row2 * col2 / n]
    for o, e in zip(obs, exp):
        chi2 += (abs(o - e) - 0.5) ** 2 / e
    return chi2, chi2_p_df1(chi2)

def odds_ratio_ci(a, b, c, d):
    """OR and 95% CI (Woolf/logit). a,b exposed(out+,out-); c,d unexposed."""
    # add 0.5 continuity correction if any zero
    if 0 in (a, b, c, d):
        a += 0.5; b += 0.5; c += 0.5; d += 0.5
    orr = (a * d) / (b * c)
    se = math.sqrt(1/a + 1/b + 1/c + 1/d)
    lo = math.exp(math.log(orr) - 1.96 * se)
    hi = math.exp(math.log(orr) + 1.96 * se)
    return orr, lo, hi

def welch_t(x, y):
    """Welch's t-test; large-sample normal approximation for p-value."""
    nx, ny = len(x), len(y)
    mx, my = sum(x)/nx, sum(y)/ny
    vx = sum((v-mx)**2 for v in x)/(nx-1)
    vy = sum((v-my)**2 for v in y)/(ny-1)
    se = math.sqrt(vx/nx + vy/ny)
    t = (mx - my) / se
    # Welch-Satterthwaite df
    df = (vx/nx + vy/ny)**2 / ((vx/nx)**2/(nx-1) + (vy/ny)**2/(ny-1))
    p = two_sided_z_p(t)  # large df -> normal
    return mx, my, math.sqrt(vx), math.sqrt(vy), t, df, p

def mean_sd(x):
    n = len(x); m = sum(x)/n
    sd = math.sqrt(sum((v-m)**2 for v in x)/(n-1)) if n > 1 else 0.0
    return m, sd

# ----------------------------------------------------------------------
# Logistic regression via IRLS (Newton-Raphson)
# ----------------------------------------------------------------------
def mat_inv(M):
    n = len(M)
    A = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(M)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(A[r][col]))
        A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        A[col] = [v / pv for v in A[col]]
        for r in range(n):
            if r != col:
                f = A[r][col]
                A[r] = [a - f * b for a, b in zip(A[r], A[col])]
    return [row[n:] for row in A]

def logistic_regression(X, y, iters=50):
    n, k = len(X), len(X[0])
    beta = [0.0] * k
    for _ in range(iters):
        # gradient and Hessian
        grad = [0.0] * k
        H = [[0.0]*k for _ in range(k)]
        for i in range(n):
            eta = sum(beta[j]*X[i][j] for j in range(k))
            eta = max(-30, min(30, eta))
            p = 1.0/(1.0+math.exp(-eta))
            w = p*(1-p)
            r = y[i]-p
            for a in range(k):
                grad[a] += X[i][a]*r
                for b in range(k):
                    H[a][b] += X[i][a]*X[i][b]*w
        Hinv = mat_inv(H)
        step = [sum(Hinv[a][b]*grad[b] for b in range(k)) for a in range(k)]
        beta = [beta[a]+step[a] for a in range(k)]
        if max(abs(s) for s in step) < 1e-8:
            break
    # covariance = inverse Hessian
    cov = mat_inv(H)
    se = [math.sqrt(cov[a][a]) for a in range(k)]
    return beta, se

# ----------------------------------------------------------------------
# Simulate the cohort
# ----------------------------------------------------------------------
records = []
for _ in range(N):
    # 63% self-medicated (source: OTC/pharmacist/friend/quack), else prescribed
    self_med = 1 if random.random() < 0.63 else 0

    # duration of continuous use (weeks) - self-medicated longer, right-skewed
    if self_med:
        dur = max(1, round(random.lognormvariate(math.log(14), 0.7)))
    else:
        dur = max(1, round(random.lognormvariate(math.log(4.5), 0.6)))

    # facial application more common in self-medicated (cosmetic use)
    facial = 1 if random.random() < (0.72 if self_med else 0.38) else 0
    # super-potent molecule use
    superpot = 1 if random.random() < (0.55 if self_med else 0.18) else 0
    # fixed-drug combination cream
    fdc = 1 if random.random() < (0.68 if self_med else 0.12) else 0

    # latent risk -> probability of ANY adverse effect (logit)
    logit = (-2.3 + 1.55*self_med + 0.055*dur + 0.75*facial
             + 0.85*superpot + 0.6*fdc)
    p_ae = 1.0/(1.0+math.exp(-max(-30, min(30, logit))))
    ae = 1 if random.random() < p_ae else 0

    # cost of care (USD) - higher with adverse effects / steroid modification
    base = random.gauss(18, 5)
    cost = base + (55 if ae else 0) + (0.9*dur) + (22 if (fdc and facial) else 0)
    cost = max(5, cost)

    # tinea incognito (steroid-modified dermatophytosis) among FDC/facial users
    p_tinea = 0.05 + 0.35*fdc + 0.12*self_med
    tinea = 1 if (ae and random.random() < min(0.9, p_tinea)) else 0
    # TSDF among chronic facial users
    tsdf = 1 if (facial and dur >= 8 and random.random() < 0.62) else 0

    records.append(dict(self_med=self_med, dur=dur, facial=facial,
                        superpot=superpot, fdc=fdc, ae=ae, cost=cost,
                        tinea=tinea, tsdf=tsdf))

R = records
def sub(pred): return [r for r in R if pred(r)]
sm = sub(lambda r: r["self_med"] == 1)
pr = sub(lambda r: r["self_med"] == 0)

out = {"meta": {"seed": SEED, "N": N,
                "n_self_medicated": len(sm), "n_prescribed": len(pr),
                "pct_self_medicated": round(100*len(sm)/N, 1)}}

# --- Primary outcome: any adverse effect by group ---
a = sum(r["ae"] for r in sm); b = len(sm)-a
c = sum(r["ae"] for r in pr); d = len(pr)-c
chi2, p = chi2_2x2(a, b, c, d)
orr, lo, hi = odds_ratio_ci(a, b, c, d)
out["primary_ae"] = {
    "self_med_ae_n": a, "self_med_ae_pct": round(100*a/len(sm), 1),
    "prescribed_ae_n": c, "prescribed_ae_pct": round(100*c/len(pr), 1),
    "chi2": round(chi2, 2), "p": p,
    "OR": round(orr, 2), "OR_lo": round(lo, 2), "OR_hi": round(hi, 2),
}

# --- Duration comparison ---
mx, my, sdx, sdy, t, df, pdur = welch_t([r["dur"] for r in sm], [r["dur"] for r in pr])
out["duration"] = {"self_med_mean": round(mx,1), "self_med_sd": round(sdx,1),
                   "prescribed_mean": round(my,1), "prescribed_sd": round(sdy,1),
                   "t": round(t,2), "df": round(df,0), "p": pdur}

# --- Cost comparison ---
cmx, cmy, csdx, csdy, ct, cdf, pcost = welch_t([r["cost"] for r in sm], [r["cost"] for r in pr])
out["cost"] = {"self_med_mean": round(cmx,1), "self_med_sd": round(csdx,1),
               "prescribed_mean": round(cmy,1), "prescribed_sd": round(csdy,1),
               "t": round(ct,2), "p": pcost,
               "cost_ratio": round(cmx/cmy, 2)}

# --- Specific adverse effect / entity prevalence by group ---
def rate(group, key): 
    n = len(group); k = sum(r[key] for r in group)
    return k, round(100*k/n, 1)
out["entities"] = {}
for key, label in [("tinea","Tinea incognito"), ("tsdf","Steroid-dependent/damaged face")]:
    ka, pa = rate(sm, key); kb, pb = rate(pr, key)
    a2 = ka; b2 = len(sm)-ka; c2 = kb; d2 = len(pr)-kb
    chi2e, pe = chi2_2x2(a2, b2, c2, d2)
    ore, loe, hie = odds_ratio_ci(a2, b2, c2, d2)
    out["entities"][key] = {"label": label,
        "self_med_pct": pa, "prescribed_pct": pb, "chi2": round(chi2e,2),
        "p": pe, "OR": round(ore,2), "OR_lo": round(loe,2), "OR_hi": round(hie,2)}

# --- Multivariable logistic regression for ANY adverse effect ---
# predictors: intercept, self_med, dur(std), facial, superpot, fdc
durs = [r["dur"] for r in R]
mdur, sddur = mean_sd(durs)
X = [[1.0, r["self_med"], (r["dur"]-mdur)/sddur, r["facial"], r["superpot"], r["fdc"]] for r in R]
Y = [r["ae"] for r in R]
beta, se = logistic_regression(X, Y)
names = ["Intercept", "Self-medication", "Duration (per SD)", "Facial application",
         "Super-potent molecule", "FDC cream"]
out["logit"] = []
for nm, bcoef, s in zip(names, beta, se):
    z = bcoef/s
    out["logit"].append({"var": nm, "beta": round(bcoef,3),
        "aOR": round(math.exp(bcoef),2),
        "aOR_lo": round(math.exp(bcoef-1.96*s),2),
        "aOR_hi": round(math.exp(bcoef+1.96*s),2),
        "z": round(z,2), "p": two_sided_z_p(z)})

# --- Demographic-ish exposure prevalences ---
out["exposures"] = {
    "facial_self": round(100*sum(r["facial"] for r in sm)/len(sm),1),
    "facial_presc": round(100*sum(r["facial"] for r in pr)/len(pr),1),
    "superpot_self": round(100*sum(r["superpot"] for r in sm)/len(sm),1),
    "superpot_presc": round(100*sum(r["superpot"] for r in pr)/len(pr),1),
    "fdc_self": round(100*sum(r["fdc"] for r in sm)/len(sm),1),
    "fdc_presc": round(100*sum(r["fdc"] for r in pr)/len(pr),1),
}

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "tcs_results.json"), "w") as f:
    json.dump(out, f, indent=2)

def fp(p): return "<0.001" if p < 0.001 else f"{p:.3f}"
print("Cohort N =", N, "| self-medicated =", len(sm), f"({out['meta']['pct_self_medicated']}%)")
print("\nPrimary outcome (any adverse effect):")
pa = out["primary_ae"]
print(f"  Self-medicated: {pa['self_med_ae_pct']}%  vs  Prescribed: {pa['prescribed_ae_pct']}%")
print(f"  chi2={pa['chi2']}, p={fp(pa['p'])}, OR={pa['OR']} (95% CI {pa['OR_lo']}-{pa['OR_hi']})")
print("\nDuration (weeks):", out["duration"]["self_med_mean"], "vs", out["duration"]["prescribed_mean"],
      "p=", fp(out["duration"]["p"]))
print("Cost (USD):", out["cost"]["self_med_mean"], "vs", out["cost"]["prescribed_mean"],
      "ratio=", out["cost"]["cost_ratio"], "p=", fp(out["cost"]["p"]))
print("\nMultivariable logistic regression (adjusted ORs):")
for row in out["logit"]:
    print(f"  {row['var']:<24} aOR={row['aOR']:>5} (95% CI {row['aOR_lo']}-{row['aOR_hi']}), p={fp(row['p'])}")
print("\nWrote tcs_results.json")
