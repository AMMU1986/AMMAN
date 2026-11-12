#!/usr/bin/env python3
"""
Analysis pipeline for the manuscript
"Comparing empirical and machine-learning models for predicting soil
infiltration rate in Hisar, Haryana".

IMPORTANT - DATA STATUS
    The sandbox has no field data and no third-party Python packages, so this
    script GENERATES AN ILLUSTRATIVE (SYNTHETIC) DATASET for 15 test sites using
    soil-property ranges typical of the Hisar region, then runs the complete
    modelling workflow on it. All numbers in the manuscript come from this
    script. Replace `hisar_data/infiltration_observations.csv` and
    `hisar_data/site_properties.csv` with real double-ring infiltrometer data
    and set USE_SYNTHETIC = False to reproduce every table and figure from
    field measurements.

Workflow
    1. Site soil properties + time series of infiltration rate (double ring).
    2. Empirical models fitted per site (Levenberg-Marquardt least squares):
       Kostiakov, Modified Kostiakov, Philip, Horton, Novel (Sihag et al. 2017).
    3. Machine-learning models trained on pooled data (inputs: t, sand, clay,
       bulk density, moisture content, organic carbon):
       MLR, ANN (MLP), Random Forest, Gaussian Process Regression.
    4. Random 70/30 split (same split for every model) + leave-sites-out test.
    5. Statistics: CC, RMSE, MAE, NSE, Bias; one-way ANOVA; sensitivity.

Pure standard library only. Usage:  python3 hisar_infiltration_analysis.py
"""

import csv
import json
import math
import os
import random

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, 'hisar_data')
USE_SYNTHETIC = True
SEED = 2026

TIMES = [5, 10, 15, 20, 30, 40, 50, 60, 75, 90, 105, 120, 150, 180]  # minutes
FEATURES = ['t', 'sand', 'clay', 'bd', 'mc', 'oc']
FEATURE_LABELS = {'t': 'Time', 'sand': 'Sand', 'clay': 'Clay',
                  'bd': 'Bulk density', 'mc': 'Moisture content',
                  'oc': 'Organic carbon'}

# ----------------------------------------------------------------------------
# 1. Data
# ----------------------------------------------------------------------------

# id, land use, sand %, clay %, bulk density g/cm3, moisture %, organic C %
SITE_TEMPLATE = [
    ('S1', 'Cultivated (wheat-cotton)', 68, 12, 1.52, 6.8, 0.42),
    ('S2', 'Cultivated (wheat-cotton)', 64, 14, 1.55, 8.4, 0.38),
    ('S3', 'Cultivated (mustard-pearl millet)', 74, 9, 1.49, 5.1, 0.35),
    ('S4', 'Cultivated (wheat-rice)', 58, 18, 1.61, 10.9, 0.51),
    ('S5', 'Fallow land', 79, 7, 1.57, 3.2, 0.24),
    ('S6', 'Fallow land', 72, 10, 1.60, 4.5, 0.27),
    ('S7', 'Fallow land', 66, 13, 1.63, 5.9, 0.30),
    ('S8', 'Orchard (citrus/guava)', 70, 11, 1.44, 7.6, 0.63),
    ('S9', 'Agroforestry (Eucalyptus)', 73, 9, 1.46, 6.2, 0.58),
    ('S10', 'Grassland', 69, 12, 1.48, 8.9, 0.66),
    ('S11', 'Grassland', 62, 15, 1.50, 9.7, 0.55),
    ('S12', 'Compacted (roadside/campus)', 60, 16, 1.71, 4.8, 0.21),
    ('S13', 'Compacted (cattle track)', 63, 15, 1.68, 6.1, 0.25),
    ('S14', 'Sand dune / sandy plain', 86, 5, 1.53, 2.1, 0.16),
    ('S15', 'Sand dune / sandy plain', 83, 6, 1.55, 2.6, 0.19),
]


def texture_class(sand, clay):
    silt = 100 - sand - clay
    if sand >= 85 and silt + 1.5 * clay < 15:
        return 'Sand'
    if 70 <= sand < 91 and silt + 1.5 * clay >= 15 and silt + 2 * clay < 30:
        return 'Loamy sand'
    if clay < 20 and sand > 52:
        return 'Sandy loam'
    if clay < 27:
        return 'Loam'
    return 'Sandy clay loam'


def generate_synthetic(rng):
    """Create site table and observation table (synthetic, documented)."""
    sites, obs = [], []
    for sid, lu, sand, clay, bd, mc, oc in SITE_TEMPLATE:
        # steady (basic) infiltration rate, mm/h
        ic = 0.55 * sand - 1.1 * clay - 40.0 * (bd - 1.5) + 14.0 * oc - 22.0
        ic = 2.5 + math.log1p(math.exp(ic - 2.5))  # smooth floor at ~2.5
        # sorptive excess at early time, mm/h (drier, sandier, looser => larger)
        dry = max(0.15, 1.0 - mc / 16.0)
        D = (28.0 + 0.9 * sand) * dry * (1.0 + 0.6 * oc) * max(0.3, (1.78 - bd) / 0.28)
        k = 0.030 + 0.0012 * (sand - 50)          # 1/min
        w = 0.55
        # site-level variability not explained by the measured properties
        # (macropores, root channels, surface crusting, ring insertion effects)
        ic *= math.exp(rng.gauss(0, 0.15))
        D *= math.exp(rng.gauss(0, 0.15))
        rates = []
        for t in TIMES:
            f = ic + D * (w * math.exp(-k * t) + (1 - w) * (t / 5.0) ** -0.6)
            f = f * (1.0 + rng.gauss(0, 0.045)) + rng.gauss(0, 0.35)
            rates.append(round(max(0.5, f), 1))
        sites.append({'site': sid, 'land_use': lu, 'sand': sand,
                      'silt': 100 - sand - clay, 'clay': clay,
                      'texture': texture_class(sand, clay), 'bd': bd,
                      'mc': mc, 'oc': oc,
                      'f_initial': rates[0], 'f_final': rates[-1]})
        for t, f in zip(TIMES, rates):
            obs.append({'site': sid, 't': t, 'sand': sand, 'clay': clay,
                        'bd': bd, 'mc': mc, 'oc': oc, 'f': f})
    return sites, obs


def write_csv(path, rows, fields):
    with open(path, 'w', newline='') as fh:
        wr = csv.DictWriter(fh, fieldnames=fields)
        wr.writeheader()
        for r in rows:
            wr.writerow({k: r[k] for k in fields})


def read_csv(path, numeric):
    with open(path) as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        for k in numeric:
            r[k] = float(r[k])
    return rows


# ----------------------------------------------------------------------------
# 2. Linear algebra + statistics helpers
# ----------------------------------------------------------------------------

def solve(A, b):
    """Gaussian elimination with partial pivoting."""
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        if abs(M[c][c]) < 1e-14:
            M[c][c] = 1e-14
        for r in range(c + 1, n):
            fct = M[r][c] / M[c][c]
            for j in range(c, n + 1):
                M[r][j] -= fct * M[c][j]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (M[r][n] - sum(M[r][j] * x[j] for j in range(r + 1, n))) / M[r][r]
    return x


def cholesky(K):
    n = len(K)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        Li = L[i]
        for j in range(i + 1):
            Lj = L[j]
            s = K[i][j]
            for k in range(j):
                s -= Li[k] * Lj[k]
            if i == j:
                Li[j] = math.sqrt(max(s, 1e-12))
            else:
                Li[j] = s / Lj[j]
    return L


def chol_solve(L, b):
    n = len(L)
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(L[i][k] * y[k] for k in range(i))) / L[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(L[k][i] * x[k] for k in range(i + 1, n))) / L[i][i]
    return x


def mean(v):
    return sum(v) / len(v)


def std(v):
    m = mean(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))


def metrics(obs, pred):
    n = len(obs)
    mo, mp = mean(obs), mean(pred)
    cov = sum((o - mo) * (p - mp) for o, p in zip(obs, pred))
    so = math.sqrt(sum((o - mo) ** 2 for o in obs))
    sp = math.sqrt(sum((p - mp) ** 2 for p in pred))
    sse = sum((o - p) ** 2 for o, p in zip(obs, pred))
    return {
        'CC': cov / (so * sp) if so * sp > 0 else 0.0,
        'RMSE': math.sqrt(sse / n),
        'MAE': sum(abs(o - p) for o, p in zip(obs, pred)) / n,
        'NSE': 1 - sse / (so ** 2),
        'Bias': sum(p - o for o, p in zip(obs, pred)) / n,
        'within20': 100.0 * sum(1 for o, p in zip(obs, pred)
                                if abs(p - o) <= 0.2 * o) / n,
    }


def _betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > 1e-30 else 1e-30)
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > 1e-30 else 1e-30)
        c = 1 + aa / c if abs(c) > 1e-30 else 1e-30
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > 1e-30 else 1e-30)
        c = 1 + aa / c if abs(c) > 1e-30 else 1e-30
        de = d * c
        h *= de
        if abs(de - 1) < 1e-12:
            break
    return h


def betainc(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lb = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lb + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2):
        return front * _betacf(a, b, x) / a
    return 1 - front * _betacf(b, a, 1 - x) / b


def f_sf(F, d1, d2):
    """Survival function of the F distribution."""
    x = d2 / (d2 + d1 * F)
    return betainc(d2 / 2, d1 / 2, x)


def f_crit(d1, d2, alpha=0.05):
    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if f_sf(mid, d1, d2) > alpha:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def anova_oneway(groups):
    allv = [x for g in groups for x in g]
    gm = mean(allv)
    k, n = len(groups), len(allv)
    ssb = sum(len(g) * (mean(g) - gm) ** 2 for g in groups)
    ssw = sum((x - mean(g)) ** 2 for g in groups for x in g)
    d1, d2 = k - 1, n - k
    F = (ssb / d1) / (ssw / d2)
    return {'F': F, 'p': f_sf(F, d1, d2), 'Fcrit': f_crit(d1, d2),
            'df1': d1, 'df2': d2}


# ----------------------------------------------------------------------------
# 3. Empirical models (fitted per site)
# ----------------------------------------------------------------------------

def m_kostiakov(t, p, ic=None):
    return p[0] * t ** (-p[1])


def m_mod_kostiakov(t, p, ic=None):
    return p[0] * t ** (-p[1]) + p[2]


def m_philip(t, p, ic=None):
    # f = 0.5 S t^-0.5 + A ; t in h for S (mm/h^0.5) and A (mm/h)
    th = t / 60.0
    return 0.5 * p[0] * th ** -0.5 + p[1]


def m_horton(t, p, ic=None):
    return p[1] + (p[0] - p[1]) * math.exp(-p[2] * t)


def m_novel(t, p, ic):
    return p[0] * t ** (-p[1]) + p[2] * ic


EMPIRICAL = {
    'Kostiakov': (m_kostiakov, ['a', 'b']),
    'Modified Kostiakov': (m_mod_kostiakov, ['a', 'b', 'ic']),
    'Philip': (m_philip, ['S', 'A']),
    'Horton': (m_horton, ['f0', 'fc', 'k']),
    'Novel (Sihag et al.)': (m_novel, ['a', 'b', 'c']),
}


def initial_guess(name, ts, fs):
    f0, fend = fs[0], fs[-1]
    if name == 'Kostiakov':
        return [f0 * 5 ** 0.5, 0.5]
    if name == 'Modified Kostiakov':
        return [(f0 - fend) * 5 ** 0.7, 0.7, fend * 0.8]
    if name == 'Philip':
        return [max(1.0, (f0 - fend) * 0.6), fend]
    if name == 'Horton':
        return [f0 * 1.2, fend, 0.05]
    return [(f0 - fend) * 5 ** 0.7, 0.7, 0.8]


def lm_fit(model, p0, ts, fs, ic, iters=400):
    """Levenberg-Marquardt least squares with numerical Jacobian."""
    p = list(p0)
    lam = 1e-2

    def sse(pp):
        try:
            return sum((model(t, pp, ic) - f) ** 2 for t, f in zip(ts, fs))
        except (OverflowError, ValueError, ZeroDivisionError):
            return float('inf')

    cur = sse(p)
    for _ in range(iters):
        r = [f - model(t, p, ic) for t, f in zip(ts, fs)]
        J = []
        for t in ts:
            row = []
            for j in range(len(p)):
                h = 1e-6 * max(1.0, abs(p[j]))
                pp = p[:]; pp[j] += h
                row.append((model(t, pp, ic) - model(t, p, ic)) / h)
            J.append(row)
        npar = len(p)
        JTJ = [[sum(J[i][a] * J[i][b] for i in range(len(ts))) for b in range(npar)]
               for a in range(npar)]
        JTr = [sum(J[i][a] * r[i] for i in range(len(ts))) for a in range(npar)]
        improved = False
        for _ in range(20):
            A = [[JTJ[a][b] + (lam * JTJ[a][a] if a == b else 0) for b in range(npar)]
                 for a in range(npar)]
            dp = solve(A, JTr)
            pn = [p[j] + dp[j] for j in range(npar)]
            new = sse(pn)
            if new < cur:
                rel = (cur - new) / max(cur, 1e-12)
                p, cur = pn, new
                lam = max(lam / 3, 1e-9)
                improved = True
                break
            lam *= 4
        if not improved or rel < 1e-11:
            break
    return p


# ----------------------------------------------------------------------------
# 4. Machine-learning models (pooled)
# ----------------------------------------------------------------------------

class Scaler:
    def fit(self, X):
        cols = list(zip(*X))
        self.mu = [mean(c) for c in cols]
        self.sd = [std(c) or 1.0 for c in cols]
        return self

    def transform(self, X):
        return [[(x - m) / s for x, m, s in zip(row, self.mu, self.sd)] for row in X]


class MLR:
    name = 'MLR'

    def fit(self, X, y):
        self.sc = Scaler().fit(X)
        Z = [[1.0] + r for r in self.sc.transform(X)]
        p = len(Z[0])
        A = [[sum(z[a] * z[b] for z in Z) for b in range(p)] for a in range(p)]
        b = [sum(z[a] * yy for z, yy in zip(Z, y)) for a in range(p)]
        self.beta = solve(A, b)
        # back-transform to raw-unit coefficients for reporting
        self.coef = [self.beta[j + 1] / self.sc.sd[j] for j in range(p - 1)]
        self.intercept = self.beta[0] - sum(
            self.beta[j + 1] * self.sc.mu[j] / self.sc.sd[j] for j in range(p - 1))
        return self

    def predict(self, X):
        return [self.beta[0] + sum(b * z for b, z in zip(self.beta[1:], r))
                for r in self.sc.transform(X)]


class ANN:
    """One-hidden-layer MLP, tanh, Adam, trained on standardized log(f)."""
    name = 'ANN'

    def __init__(self, hidden=8, epochs=4000, lr=0.01, l2=1e-4, seed=1):
        self.h, self.epochs, self.lr, self.l2 = hidden, epochs, lr, l2
        self.rng = random.Random(seed)

    def fit(self, X, y):
        self.sc = Scaler().fit(X)
        Z = self.sc.transform(X)
        ly = [math.log(v) for v in y]
        self.ym, self.ys = mean(ly), std(ly)
        T = [(v - self.ym) / self.ys for v in ly]
        d, H = len(Z[0]), self.h
        r = self.rng
        W1 = [[r.gauss(0, 1 / math.sqrt(d)) for _ in range(d)] for _ in range(H)]
        b1 = [0.0] * H
        W2 = [r.gauss(0, 1 / math.sqrt(H)) for _ in range(H)]
        b2 = 0.0
        params = {'W1': W1, 'b1': b1, 'W2': W2}
        m = {'W1': [[0.0] * d for _ in range(H)], 'b1': [0.0] * H, 'W2': [0.0] * H, 'b2': 0.0}
        v = {'W1': [[0.0] * d for _ in range(H)], 'b1': [0.0] * H, 'W2': [0.0] * H, 'b2': 0.0}
        n = len(Z)
        b1_, b2_, eps = 0.9, 0.999, 1e-8
        self.loss_curve = []
        for ep in range(1, self.epochs + 1):
            gW1 = [[0.0] * d for _ in range(H)]
            gb1 = [0.0] * H
            gW2 = [0.0] * H
            gb2 = 0.0
            loss = 0.0
            for z, tt in zip(Z, T):
                a = [math.tanh(sum(W1[j][k] * z[k] for k in range(d)) + b1[j]) for j in range(H)]
                out = sum(W2[j] * a[j] for j in range(H)) + b2
                e = out - tt
                loss += e * e
                gb2 += e
                for j in range(H):
                    gW2[j] += e * a[j]
                    da = e * W2[j] * (1 - a[j] * a[j])
                    gb1[j] += da
                    rowg = gW1[j]
                    for k in range(d):
                        rowg[k] += da * z[k]
            sc = 2.0 / n
            corr1, corr2 = 1 - b1_ ** ep, 1 - b2_ ** ep
            for j in range(H):
                for k in range(d):
                    g = sc * gW1[j][k] + self.l2 * W1[j][k]
                    m['W1'][j][k] = b1_ * m['W1'][j][k] + (1 - b1_) * g
                    v['W1'][j][k] = b2_ * v['W1'][j][k] + (1 - b2_) * g * g
                    W1[j][k] -= self.lr * (m['W1'][j][k] / corr1) / (math.sqrt(v['W1'][j][k] / corr2) + eps)
                g = sc * gb1[j]
                m['b1'][j] = b1_ * m['b1'][j] + (1 - b1_) * g
                v['b1'][j] = b2_ * v['b1'][j] + (1 - b2_) * g * g
                b1[j] -= self.lr * (m['b1'][j] / corr1) / (math.sqrt(v['b1'][j] / corr2) + eps)
                g = sc * gW2[j] + self.l2 * W2[j]
                m['W2'][j] = b1_ * m['W2'][j] + (1 - b1_) * g
                v['W2'][j] = b2_ * v['W2'][j] + (1 - b2_) * g * g
                W2[j] -= self.lr * (m['W2'][j] / corr1) / (math.sqrt(v['W2'][j] / corr2) + eps)
            g = sc * gb2
            m['b2'] = b1_ * m['b2'] + (1 - b1_) * g
            v['b2'] = b2_ * v['b2'] + (1 - b2_) * g * g
            b2 -= self.lr * (m['b2'] / corr1) / (math.sqrt(v['b2'] / corr2) + eps)
            if ep % 100 == 0:
                self.loss_curve.append((ep, loss / n))
        self.W1, self.b1, self.W2, self.b2 = W1, b1, W2, b2
        return self

    def predict(self, X):
        out = []
        for z in self.sc.transform(X):
            a = [math.tanh(sum(w * x for w, x in zip(self.W1[j], z)) + self.b1[j])
                 for j in range(self.h)]
            o = sum(w * x for w, x in zip(self.W2, a)) + self.b2
            out.append(math.exp(o * self.ys + self.ym))
        return out


class RegTree:
    def __init__(self, max_depth, min_leaf, max_features, rng):
        self.max_depth, self.min_leaf = max_depth, min_leaf
        self.max_features, self.rng = max_features, rng

    def fit(self, X, y, idx=None):
        self.root = self._build(X, y, list(range(len(y))) if idx is None else idx, 0)
        return self

    def _build(self, X, y, idx, depth):
        vals = [y[i] for i in idx]
        node_mean = sum(vals) / len(vals)
        if depth >= self.max_depth or len(idx) < 2 * self.min_leaf:
            return node_mean
        nfeat = len(X[0])
        feats = self.rng.sample(range(nfeat), self.max_features)
        best = None
        tot, tot2, n = sum(vals), sum(v * v for v in vals), len(vals)
        parent = tot2 - tot * tot / n
        for f in feats:
            order = sorted(idx, key=lambda i: X[i][f])
            ls = ls2 = 0.0
            for k in range(len(order) - 1):
                yi = y[order[k]]
                ls += yi; ls2 += yi * yi
                nl = k + 1
                if nl < self.min_leaf or n - nl < self.min_leaf:
                    continue
                if X[order[k]][f] == X[order[k + 1]][f]:
                    continue
                rs, rs2, nr = tot - ls, tot2 - ls2, n - nl
                sse = (ls2 - ls * ls / nl) + (rs2 - rs * rs / nr)
                if best is None or sse < best[0]:
                    thr = (X[order[k]][f] + X[order[k + 1]][f]) / 2
                    best = (sse, f, thr)
        if best is None or best[0] >= parent - 1e-12:
            return node_mean
        _, f, thr = best
        left = [i for i in idx if X[i][f] <= thr]
        right = [i for i in idx if X[i][f] > thr]
        return (f, thr, self._build(X, y, left, depth + 1),
                self._build(X, y, right, depth + 1))

    def predict_one(self, x):
        node = self.root
        while isinstance(node, tuple):
            f, thr, l, r = node
            node = l if x[f] <= thr else r
        return node


class RandomForest:
    name = 'RF'

    def __init__(self, n_trees=200, max_depth=12, min_leaf=2, max_features=3, seed=7):
        self.n, self.md, self.ml, self.mf = n_trees, max_depth, min_leaf, max_features
        self.rng = random.Random(seed)

    def fit(self, X, y):
        self.trees = []
        n = len(y)
        self.oob_sum = [0.0] * n
        self.oob_cnt = [0] * n
        for _ in range(self.n):
            idx = [self.rng.randrange(n) for _ in range(n)]
            tr = RegTree(self.md, self.ml, self.mf, self.rng).fit(X, y, idx)
            self.trees.append(tr)
            inbag = set(idx)
            for i in range(n):
                if i not in inbag:
                    self.oob_sum[i] += tr.predict_one(X[i])
                    self.oob_cnt[i] += 1
        return self

    def predict(self, X):
        return [sum(t.predict_one(x) for t in self.trees) / len(self.trees) for x in X]


class GPR:
    """GP regression, ARD squared-exponential kernel on standardized inputs,
    target = standardized log(f). Hyper-parameters by marginal-likelihood
    coordinate search."""
    name = 'GPR'

    def fit(self, X, y):
        self.sc = Scaler().fit(X)
        self.Z = self.sc.transform(X)
        ly = [math.log(v) for v in y]
        self.ym, self.ys = mean(ly), std(ly)
        self.T = [(v - self.ym) / self.ys for v in ly]
        d = len(self.Z[0])
        ls = [1.0] * d
        sf2, sn2 = 1.0, 0.01
        best = self._nlml(ls, sf2, sn2)
        grid = [0.5, 0.7, 1.4, 2.0]
        for _ in range(3):
            for j in range(d + 2):
                for g in grid:
                    l2, s2, n2 = ls[:], sf2, sn2
                    if j < d:
                        l2[j] = min(50.0, max(0.05, ls[j] * g))
                    elif j == d:
                        s2 = sf2 * g
                    else:
                        n2 = min(0.5, max(1e-4, sn2 * g))
                    val = self._nlml(l2, s2, n2)
                    if val < best:
                        best, ls, sf2, sn2 = val, l2, s2, n2
        self.ls, self.sf2, self.sn2, self.nlml = ls, sf2, sn2, best
        K = self._K(self.Z, self.Z, ls, sf2)
        for i in range(len(K)):
            K[i][i] += sn2
        self.L = cholesky(K)
        self.alpha = chol_solve(self.L, self.T)
        return self

    @staticmethod
    def _k(a, b, ls, sf2):
        return sf2 * math.exp(-0.5 * sum(((x - z) / l) ** 2 for x, z, l in zip(a, b, ls)))

    def _K(self, A, B, ls, sf2):
        return [[self._k(a, b, ls, sf2) for b in B] for a in A]

    def _nlml(self, ls, sf2, sn2):
        K = self._K(self.Z, self.Z, ls, sf2)
        for i in range(len(K)):
            K[i][i] += sn2
        L = cholesky(K)
        a = chol_solve(L, self.T)
        return (0.5 * sum(t * x for t, x in zip(self.T, a))
                + sum(math.log(L[i][i]) for i in range(len(L))))

    def predict(self, X):
        Zs = self.sc.transform(X)
        out = []
        for z in Zs:
            ks = [self._k(z, zz, self.ls, self.sf2) for zz in self.Z]
            mu = sum(k * a for k, a in zip(ks, self.alpha))
            out.append(math.exp(mu * self.ys + self.ym))
        return out


def make_models():
    return [MLR(), ANN(), RandomForest(), GPR()]


# ----------------------------------------------------------------------------
# 5. Main
# ----------------------------------------------------------------------------

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    rng = random.Random(SEED)
    site_fields = ['site', 'land_use', 'sand', 'silt', 'clay', 'texture', 'bd',
                   'mc', 'oc', 'f_initial', 'f_final']
    obs_fields = ['site', 't', 'sand', 'clay', 'bd', 'mc', 'oc', 'f']
    sp = os.path.join(DATA_DIR, 'site_properties.csv')
    op = os.path.join(DATA_DIR, 'infiltration_observations.csv')
    if USE_SYNTHETIC:
        sites, obs = generate_synthetic(rng)
        write_csv(sp, sites, site_fields)
        write_csv(op, obs, obs_fields)
    sites = read_csv(sp, ['sand', 'silt', 'clay', 'bd', 'mc', 'oc', 'f_initial', 'f_final'])
    obs = read_csv(op, ['t', 'sand', 'clay', 'bd', 'mc', 'oc', 'f'])
    site_ids = [s['site'] for s in sites]
    ic_obs = {s['site']: s['f_final'] for s in sites}

    # ---- train/test split (70/30, stratified by site so each site has
    #      test points across the curve) ----
    split_rng = random.Random(SEED + 1)
    for s in site_ids:
        rows = [o for o in obs if o['site'] == s]
        # keep first and last reading in training (anchor the curve)
        inner = rows[1:-1]
        split_rng.shuffle(inner)
        test_n = round(0.3 * len(rows))
        for o in rows:
            o['split'] = 'train'
        for o in inner[:test_n]:
            o['split'] = 'test'
    train = [o for o in obs if o['split'] == 'train']
    test = [o for o in obs if o['split'] == 'test']
    write_csv(os.path.join(DATA_DIR, 'infiltration_observations_split.csv'),
              obs, obs_fields + ['split'])

    results = {'n_sites': len(sites), 'n_obs': len(obs), 'n_train': len(train),
               'n_test': len(test), 'times': TIMES, 'sites': sites}

    # ---- descriptive statistics of all variables ----
    desc = {}
    for v in ['t', 'sand', 'clay', 'bd', 'mc', 'oc', 'f']:
        for part, rows in [('train', train), ('test', test)]:
            vals = [o[v] for o in rows]
            m, s = mean(vals), std(vals)
            n = len(vals)
            sk = sum(((x - m) / s) ** 3 for x in vals) / n
            desc.setdefault(v, {})[part] = {
                'min': min(vals), 'max': max(vals), 'mean': m, 'sd': s, 'skew': sk}
    results['descriptive'] = desc

    # Pearson correlation of each input with f (all data)
    fvals = [o['f'] for o in obs]
    results['corr_with_f'] = {v: metrics(fvals, [o[v] for o in obs])['CC']
                              for v in FEATURES}

    # ---- empirical models ----
    emp = {}
    for name, (model, pnames) in EMPIRICAL.items():
        params, tr_o, tr_p, te_o, te_p, full_fit = {}, [], [], [], [], {}
        for s in site_ids:
            rtr = [o for o in train if o['site'] == s]
            rte = [o for o in test if o['site'] == s]
            ts, fs = [o['t'] for o in rtr], [o['f'] for o in rtr]
            p = lm_fit(model, initial_guess(name, ts, fs), ts, fs, ic_obs[s])
            params[s] = p
            tr_o += fs
            tr_p += [model(t, p, ic_obs[s]) for t in ts]
            te_o += [o['f'] for o in rte]
            te_p += [model(o['t'], p, ic_obs[s]) for o in rte]
            full_fit[s] = [model(t, p, ic_obs[s]) for t in TIMES]
        emp[name] = {'pnames': pnames, 'params': params,
                     'train': metrics(tr_o, tr_p), 'test': metrics(te_o, te_p),
                     'test_pred': te_p, 'test_obs': te_o, 'curves': full_fit}
        # per-site R2 on training data
        r2 = []
        for s in site_ids:
            rtr = [o for o in train if o['site'] == s]
            fo = [o['f'] for o in rtr]
            fp = [model(o['t'], params[s], ic_obs[s]) for o in rtr]
            r2.append(metrics(fo, fp)['NSE'])
        emp[name]['site_r2'] = dict(zip(site_ids, r2))
        print(f"{name:22s} test RMSE={emp[name]['test']['RMSE']:.3f} "
              f"NSE={emp[name]['test']['NSE']:.4f}")
    results['empirical'] = emp

    # ---- ML models ----
    def XY(rows):
        return [[o[f] for f in FEATURES] for o in rows], [o['f'] for o in rows]

    Xtr, ytr = XY(train)
    Xte, yte = XY(test)
    ml = {}
    fitted = {}
    for mdl in make_models():
        mdl.fit(Xtr, ytr)
        ptr, pte = mdl.predict(Xtr), mdl.predict(Xte)
        ml[mdl.name] = {'train': metrics(ytr, ptr), 'test': metrics(yte, pte),
                        'test_pred': pte}
        fitted[mdl.name] = mdl
        print(f"{mdl.name:22s} train RMSE={ml[mdl.name]['train']['RMSE']:.3f} "
              f"test RMSE={ml[mdl.name]['test']['RMSE']:.3f} "
              f"NSE={ml[mdl.name]['test']['NSE']:.4f}")
    results['ml'] = ml
    results['test_obs'] = yte
    results['test_site'] = [o['site'] for o in test]
    results['test_t'] = [o['t'] for o in test]
    m = fitted['MLR']
    results['mlr_equation'] = {'intercept': m.intercept,
                               'coef': dict(zip(FEATURES, m.coef))}
    g = fitted['GPR']
    results['gpr_hyper'] = {'length_scales': dict(zip(FEATURES, g.ls)),
                            'signal_var': g.sf2, 'noise_var': g.sn2}
    rf = fitted['RF']
    oob = [(ytr[i], rf.oob_sum[i] / rf.oob_cnt[i]) for i in range(len(ytr)) if rf.oob_cnt[i]]
    results['rf_oob'] = metrics([a for a, _ in oob], [b for _, b in oob])
    results['ann_loss_curve'] = fitted['ANN'].loss_curve

    # full-curve predictions of ML models for plotted sites
    results['ml_curves'] = {}
    for name, mdl in fitted.items():
        results['ml_curves'][name] = {}
        for s in sites:
            Xs = [[t, s['sand'], s['clay'], s['bd'], s['mc'], s['oc']] for t in TIMES]
            results['ml_curves'][name][s['site']] = mdl.predict(Xs)

    # ---- spatial transfer: leave-3-sites-out (5 folds) ----
    fold_rng = random.Random(SEED + 2)
    order = site_ids[:]
    fold_rng.shuffle(order)
    folds = [order[i::5] for i in range(5)]
    lso = {}
    for mk in [MLR, ANN, RandomForest, GPR]:
        allo, allp, alls = [], [], []
        for fold in folds:
            tr = [o for o in obs if o['site'] not in fold]
            te = [o for o in obs if o['site'] in fold]
            Xa, ya = XY(tr)
            Xb, yb = XY(te)
            mdl = mk().fit(Xa, ya)
            allo += yb
            allp += mdl.predict(Xb)
            alls += [o['site'] for o in te]
        lso[mk.name] = metrics(allo, allp)
        lso[mk.name]['per_site'] = {
            s: {'RMSE': metrics([a for a, ss in zip(allo, alls) if ss == s],
                                [b for b, ss in zip(allp, alls) if ss == s])['RMSE'],
                'Bias': metrics([a for a, ss in zip(allo, alls) if ss == s],
                                [b for b, ss in zip(allp, alls) if ss == s])['Bias'],
                'max_pred': max(b for b, ss in zip(allp, alls) if ss == s)}
            for s in site_ids}
        print(f"LSO {mk.name:6s} RMSE={lso[mk.name]['RMSE']:.3f} NSE={lso[mk.name]['NSE']:.4f}")
    results['leave_sites_out'] = lso
    results['lso_folds'] = folds

    # ---- sensitivity: drop one input at a time (RF and GPR) ----
    sens = {}
    for mk in [RandomForest, GPR]:
        base = ml[mk.name]['test']['RMSE']
        sens[mk.name] = {}
        for j, f in enumerate(FEATURES):
            keep = [k for k in range(len(FEATURES)) if k != j]
            Xa = [[r[k] for k in keep] for r in Xtr]
            Xb = [[r[k] for k in keep] for r in Xte]
            mdl = mk().fit(Xa, ytr)
            met = metrics(yte, mdl.predict(Xb))
            sens[mk.name][f] = {'RMSE': met['RMSE'], 'CC': met['CC'],
                                'dRMSE': met['RMSE'] - base}
        print('sensitivity', mk.name, {k: round(v['RMSE'], 2) for k, v in sens[mk.name].items()})
    results['sensitivity'] = sens

    # ---- ANOVA: observed vs each model's test predictions ----
    groups = [yte] + [emp[n]['test_pred'] for n in EMPIRICAL] + \
             [ml[n]['test_pred'] for n in ['MLR', 'ANN', 'RF', 'GPR']]
    results['anova_all'] = anova_oneway(groups)
    best_emp = min(EMPIRICAL, key=lambda n: emp[n]['test']['RMSE'])
    best_ml = min(['MLR', 'ANN', 'RF', 'GPR'], key=lambda n: ml[n]['test']['RMSE'])
    results['best_emp'], results['best_ml'] = best_emp, best_ml
    results['anova_best'] = anova_oneway([yte, emp[best_emp]['test_pred'],
                                          ml[best_ml]['test_pred']])
    print('ANOVA all', results['anova_all'])

    with open(os.path.join(DATA_DIR, 'results.json'), 'w') as fh:
        json.dump(results, fh, indent=1)
    print('done')


if __name__ == '__main__':
    main()
