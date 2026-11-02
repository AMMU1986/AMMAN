#!/usr/bin/env python3
"""
Reproducible simulation + machine-learning pipeline for the paper
"Low-Cost IoT Sensor Network with Edge Machine Learning for Real-Time
Multi-Depth Soil Temperature Forecasting in the Rice-Wheat System of Haryana".

IMPORTANT: no field data are used. Weather is produced by a stochastic weather
generator tuned to the published climatology of Karnal and Hisar, soil
temperature by a 1-D Crank-Nicolson heat-conduction model, and sensor readings
by a DS18B20 error model. All numbers reported in the paper are outputs of
this script (pure Python standard library; fixed random seed).

Usage:  python3 simulate_and_model.py      -> writes results.json, series.csv
"""

import json
import math
import os
import random
import time

OUT = os.path.dirname(os.path.abspath(__file__))
SEED = 2026
DEPTHS_CM = [5, 10, 20, 50]
HORIZONS = [1, 3, 7]
GSC = 0.0820  # solar constant, MJ m-2 min-1

# --------------------------------------------------------------------------
# Site climatology (approximate published normals; see paper Section 2.1)
# --------------------------------------------------------------------------
SITES = {
    'Karnal': dict(lat=29.69, a0=24.0, a1=11.0, phase=175, sig=1.4, rho=0.75,
                   pw0=0.04, pw1=0.45, am0=7.0, am1=11.0, rh0=38.0, rh1=40.0,
                   rhw=25.0, fog=0.20, wind=1.2),
    'Hisar': dict(lat=29.15, a0=24.5, a1=12.0, phase=172, sig=1.6, rho=0.75,
                  pw0=0.03, pw1=0.30, am0=6.0, am1=9.0, rh0=33.0, rh1=38.0,
                  rhw=22.0, fog=0.10, wind=1.35),
}

# Soil (sandy loam to loam, typical of Haryana alluvium)
RHO_B = 1450.0      # bulk density kg m-3
C_S = 800.0         # specific heat of solids J kg-1 K-1
C_W = 4.18e6        # volumetric heat capacity of water J m-3 K-1
LAM_DRY, LAM_SAT = 0.35, 1.60   # W m-1 K-1
TH_S, TH_FC, TH_WP = 0.45, 0.30, 0.12
ROOT_Z = 0.30       # m
BETA = 0.30         # degC per MJ m-2 d-1, surface heating coefficient


def circ_dist(d, c):
    x = abs(d - c) % 365
    return min(x, 365 - x)


def monsoon(d):
    return math.exp(-(circ_dist(d, 215) ** 2) / (2 * 30 ** 2))


def winter(d):
    return math.exp(-(circ_dist(d, 5) ** 2) / (2 * 20 ** 2))


def premonsoon(d):
    return math.exp(-(circ_dist(d, 140) ** 2) / (2 * 30 ** 2))


def extraterrestrial(lat_deg, J):
    """FAO-56: returns Ra (MJ m-2 d-1) and daylength N (h)."""
    phi = math.radians(lat_deg)
    dr = 1 + 0.033 * math.cos(2 * math.pi * J / 365)
    dec = 0.409 * math.sin(2 * math.pi * J / 365 - 1.39)
    ws = math.acos(-math.tan(phi) * math.tan(dec))
    ra = (24 * 60 / math.pi) * GSC * dr * (
        ws * math.sin(phi) * math.sin(dec) + math.cos(phi) * math.cos(dec) * math.sin(ws))
    return ra, 24 * ws / math.pi


# --------------------------------------------------------------------------
# Crop calendar (rice-wheat), cover fraction and residue fraction
# --------------------------------------------------------------------------
def crop_state(d, practice):
    """Return (cover fraction fc, residue fraction fr, ponded flag, season)."""
    if 180 <= d < 290:                         # rice
        fc = min(0.85, 0.10 + 0.75 * (d - 180) / 60.0)
        return fc, 0.0, d < 270, 'rice'
    # wheat from day 315 to day 105 of next year
    if d >= 315 or d <= 105:
        k = d - 315 if d >= 315 else d + 365 - 315
        if k <= 5:
            fc = 0.0
        elif k <= 95:
            fc = 0.9 * (k - 5) / 90.0
        elif k <= 135:
            fc = 0.9
        else:
            fc = max(0.4, 0.9 - 0.5 * (k - 135) / 20.0)
        fr = 0.7 * math.exp(-max(0, (d - 295) if d >= 295 else d + 365 - 295) / 200.0) \
            if practice == 'ZT-R' else 0.0
        return fc, fr, False, 'wheat'
    if 290 <= d < 315:                          # turnaround (residue on ZT-R)
        fr = 0.7 if practice == 'ZT-R' else 0.0
        return 0.0, fr, False, 'turnaround'
    fr = 0.3 * math.exp(-(d - 106) / 60.0) if practice == 'ZT-R' else 0.0
    return 0.0, fr, False, 'fallow'


# --------------------------------------------------------------------------
# Weather generator + water balance + heat conduction
# --------------------------------------------------------------------------
def thermal(theta):
    """Volumetric heat capacity, conductivity (Johansen), diffusivity (m2 d-1)."""
    C = RHO_B * C_S + theta * C_W
    sr = max(theta / TH_S, 1e-3)
    ke = max(0.0, math.log10(sr) + 1.0) if sr > 0.1 else 0.0
    lam = LAM_DRY + (LAM_SAT - LAM_DRY) * ke
    return lam / C * 86400.0


def thomas(a, b, c, d):
    n = len(d)
    cp, dp = [0.0] * n, [0.0] * n
    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]
    for i in range(1, n):
        m = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / m if i < n - 1 else 0.0
        dp[i] = (d[i] - a[i] * dp[i - 1]) / m
    x = [0.0] * n
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


def simulate_site(name, rng, practice='CT', years=4, weather=None):
    p = SITES[name]
    dz, nz = 0.025, 80                     # 2.0 m profile
    t_bot = p['a0'] + 1.5
    T = [p['a0']] * (nz + 1)
    theta, theta_deep = 0.22, 0.22
    anom = 0.0
    rows = []
    wx_out = []
    for y in range(years):
        for d in range(1, 366):
            k = y * 365 + d - 1
            if weather is None:
                M, W = monsoon(d), winter(d)
                anom = p['rho'] * anom + p['sig'] * rng.gauss(0, 1)
                tclim = p['a0'] + p['a1'] * math.cos(2 * math.pi * (d - p['phase']) / 365) - 1.5 * M
                ta = tclim + anom
                wet = rng.random() < p['pw0'] + p['pw1'] * M
                rain = rng.expovariate(1.0 / (p['am0'] + p['am1'] * M)) if wet else 0.0
                ra, N = extraterrestrial(p['lat'], d)
                s = 0.82 - 0.30 * M - 0.30 * wet - p['fog'] * W + rng.gauss(0, 0.07)
                s = min(0.95, max(0.05, s))
                ssh = s * N
                rs = (0.25 + 0.50 * s) * ra
                rh = p['rh0'] + p['rh1'] * M + p['rhw'] * W + 10 * wet - 0.8 * anom + rng.gauss(0, 5)
                rh = min(98.0, max(12.0, rh))
                ws = (p['wind'] + 1.2 * premonsoon(d)) * math.exp(rng.gauss(0, 0.30))
                dtr = 6.0 + 10.0 * s
                wx = dict(ta=ta, rain=rain, ra=ra, ssh=ssh, rs=rs, rh=rh, ws=ws, dtr=dtr)
                wx_out.append(wx)
            else:
                wx = weather[k]
            fc, fr, ponded, season = crop_state(d, practice)
            # --- water balance
            et0 = 0.0023 * 0.408 * wx['ra'] * (wx['ta'] + 17.8) * math.sqrt(wx['dtr'])
            kc = 0.40 + 0.75 * fc + (0.20 if ponded else 0.0)
            ks = min(1.0, max(0.0, (theta - TH_WP) / (0.6 * (TH_FC - TH_WP))))
            irr = 0.0
            if season == 'wheat' and theta < 0.18:
                irr = 60.0
            if d == 310:
                irr = 60.0
            theta += (wx['rain'] + irr - kc * et0 * ks) / (ROOT_Z * 1000.0)
            if theta > TH_FC:
                theta -= 0.5 * (theta - TH_FC)
            if ponded:
                theta = TH_S
            theta = min(TH_S, max(0.05, theta))
            theta_deep += (theta - theta_deep) / 30.0
            se = (theta - TH_WP) / (TH_S - TH_WP)
            se = min(1.0, max(0.0, se))
            # --- upper boundary
            t0 = wx['ta'] + BETA * wx['rs'] * (1 - fc) * (1 - 0.6 * fr) * (1 - 0.5 * se)
            # --- Crank-Nicolson, 4 sub-steps per day
            alpha = [thermal(theta if i * dz <= ROOT_Z else theta_deep) for i in range(nz + 1)]
            dt = 0.25
            acc = {zc: 0.0 for zc in DEPTHS_CM}
            for _ in range(4):
                n_int = nz - 1
                a, b, c, rhs = [0.0] * n_int, [0.0] * n_int, [0.0] * n_int, [0.0] * n_int
                for j in range(n_int):
                    i = j + 1
                    r = alpha[i] * dt / (dz * dz)
                    a[j], b[j], c[j] = -r / 2, 1 + r, -r / 2
                    rhs[j] = (r / 2) * T[i - 1] + (1 - r) * T[i] + (r / 2) * T[i + 1]
                r1 = alpha[1] * dt / (dz * dz)
                rn = alpha[nz - 1] * dt / (dz * dz)
                rhs[0] += (r1 / 2) * t0
                rhs[-1] += (rn / 2) * t_bot
                inner = thomas(a, b, c, rhs)
                T = [t0] + inner + [t_bot]
                for zc in DEPTHS_CM:
                    acc[zc] += T[int(round(zc / 100 / dz))] / 4
            if y >= 1:   # discard spin-up year
                rows.append(dict(doy=d, year=y, ta=wx['ta'], rh=wx['rh'], ws=wx['ws'],
                                 ssh=wx['ssh'], rs=wx['rs'], rain=wx['rain'], theta=theta,
                                 fc=fc, fr=fr, **{f'tz{zc}': acc[zc] for zc in DEPTHS_CM}))
    return rows, wx_out


def add_sensor_noise(rows, rng):
    """DS18B20 observation model (bias, noise, 0.0625 C resolution, 2% gaps)."""
    bias = {zc: rng.uniform(-0.3, 0.3) for zc in DEPTHS_CM}
    for zc in DEPTHS_CM:
        vals = [r[f'tz{zc}'] + bias[zc] + rng.gauss(0, 0.15) for r in rows]
        vals = [round(v / 0.0625) * 0.0625 for v in vals]
        miss = [rng.random() < 0.02 for _ in vals]
        for i in range(len(vals)):
            if miss[i] and 0 < i < len(vals) - 1:
                vals[i] = None
        for i in range(len(vals)):       # linear gap filling
            if vals[i] is None:
                j = i
                while vals[j] is None:
                    j += 1
                vals[i] = vals[i - 1] + (vals[j] - vals[i - 1]) / (j - i + 1)
        for r, v in zip(rows, vals):
            r[f'obs{zc}'] = v
    return rows


# --------------------------------------------------------------------------
# Feature construction
# --------------------------------------------------------------------------
FEATURES = ['ta', 'ta_l1', 'ta_l2', 'rh', 'ws', 'ssh', 'rs', 'rain', 'theta',
            'obs5', 'obs10', 'obs20', 'obs50', 'obs5_l1', 'sin_doy', 'cos_doy']


def build_xy(rows, h):
    X, Y, meta = [], [], []
    for t in range(2, len(rows) - h):
        r = rows[t]
        x = [r['ta'], rows[t - 1]['ta'], rows[t - 2]['ta'], r['rh'], r['ws'], r['ssh'],
             r['rs'], r['rain'], r['theta'], r['obs5'], r['obs10'], r['obs20'], r['obs50'],
             rows[t - 1]['obs5'], math.sin(2 * math.pi * r['doy'] / 365),
             math.cos(2 * math.pi * r['doy'] / 365)]
        X.append(x)
        Y.append([rows[t + h][f'obs{zc}'] for zc in DEPTHS_CM])
        meta.append((r['year'], r['doy'], [r[f'obs{zc}'] for zc in DEPTHS_CM]))
    return X, Y, meta


def split(X, Y, meta, test_year=3):
    tr = [i for i, m in enumerate(meta) if m[0] < test_year]
    te = [i for i, m in enumerate(meta) if m[0] == test_year]
    return ([X[i] for i in tr], [Y[i] for i in tr], [meta[i] for i in tr],
            [X[i] for i in te], [Y[i] for i in te], [meta[i] for i in te])


class Scaler:
    def fit(self, X):
        n, f = len(X), len(X[0])
        self.mu = [sum(x[j] for x in X) / n for j in range(f)]
        self.sd = [max(1e-9, math.sqrt(sum((x[j] - self.mu[j]) ** 2 for x in X) / n)) for j in range(f)]
        return self

    def tf(self, X):
        return [[(x[j] - self.mu[j]) / self.sd[j] for j in range(len(x))] for x in X]


# --------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------
def solve(A, b):
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                for k in range(c, n + 1):
                    M[r][k] -= f * M[c][k]
    return [M[i][n] / M[i][i] for i in range(n)]


class Ridge:
    def __init__(self, lam=1e-2):
        self.lam = lam

    def fit(self, X, y):
        Xa = [x + [1.0] for x in X]
        p = len(Xa[0])
        A = [[sum(r[i] * r[j] for r in Xa) + (self.lam if i == j and i < p - 1 else 0) for j in range(p)]
             for i in range(p)]
        b = [sum(r[i] * yy for r, yy in zip(Xa, y)) for i in range(p)]
        self.w = solve(A, b)
        return self

    def predict(self, X):
        return [sum(wi * xi for wi, xi in zip(self.w, x + [1.0])) for x in X]


class Binner:
    def fit(self, X, nb=32):
        f = len(X[0])
        self.edges = []
        for j in range(f):
            v = sorted(x[j] for x in X)
            e = sorted(set(v[int(len(v) * q / nb)] for q in range(1, nb)))
            self.edges.append(e)
        return self

    def tf(self, X):
        out = []
        for x in X:
            row = []
            for j, v in enumerate(x):
                e = self.edges[j]
                lo, hi = 0, len(e)
                while lo < hi:
                    m = (lo + hi) // 2
                    if v > e[m]:
                        lo = m + 1
                    else:
                        hi = m
                row.append(lo)
            out.append(row)
        return out


def grow(B, y, idx, depth, max_depth, min_leaf, mtry, nbins, rng):
    n = len(idx)
    s = sum(y[i] for i in idx)
    if depth >= max_depth or n < 2 * min_leaf:
        return s / n
    feats = rng.sample(range(len(B[0])), mtry) if mtry < len(B[0]) else range(len(B[0]))
    best = (0.0, None, None)
    base = s * s / n
    for j in feats:
        cnt = [0] * (nbins + 1)
        sm = [0.0] * (nbins + 1)
        for i in idx:
            cnt[B[i][j]] += 1
            sm[B[i][j]] += y[i]
        nl, sl = 0, 0.0
        for bnum in range(nbins):
            nl += cnt[bnum]
            sl += sm[bnum]
            nr = n - nl
            if nl < min_leaf or nr < min_leaf:
                continue
            g = sl * sl / nl + (s - sl) ** 2 / nr - base
            if g > best[0]:
                best = (g, j, bnum)
    if best[1] is None:
        return s / n
    j, t = best[1], best[2]
    L = [i for i in idx if B[i][j] <= t]
    R = [i for i in idx if B[i][j] > t]
    return (j, t, grow(B, y, L, depth + 1, max_depth, min_leaf, mtry, nbins, rng),
            grow(B, y, R, depth + 1, max_depth, min_leaf, mtry, nbins, rng))


def tree_pred(node, b):
    while isinstance(node, tuple):
        node = node[2] if b[node[0]] <= node[1] else node[3]
    return node


class RandomForest:
    def __init__(self, n_trees=60, max_depth=12, min_leaf=5, seed=0):
        self.n, self.md, self.ml, self.rng = n_trees, max_depth, min_leaf, random.Random(seed)

    def fit(self, X, y):
        self.bn = Binner().fit(X)
        B = self.bn.tf(X)
        mtry = max(1, len(X[0]) // 3)
        self.trees = []
        for _ in range(self.n):
            idx = [self.rng.randrange(len(y)) for _ in range(len(y))]
            self.trees.append(grow(B, y, idx, 0, self.md, self.ml, mtry, 32, self.rng))
        return self

    def predict(self, X):
        B = self.bn.tf(X)
        return [sum(tree_pred(t, b) for t in self.trees) / self.n for b in B]


class GBT:
    def __init__(self, n_trees=120, lr=0.1, max_depth=3, min_leaf=10, sub=0.8, seed=0):
        self.n, self.lr, self.md, self.ml, self.sub = n_trees, lr, max_depth, min_leaf, sub
        self.rng = random.Random(seed)

    def fit(self, X, y):
        self.bn = Binner().fit(X)
        B = self.bn.tf(X)
        self.f0 = sum(y) / len(y)
        F = [self.f0] * len(y)
        self.trees = []
        for _ in range(self.n):
            res = [yy - ff for yy, ff in zip(y, F)]
            idx = self.rng.sample(range(len(y)), int(self.sub * len(y)))
            t = grow(B, res, idx, 0, self.md, self.ml, len(X[0]), 32, self.rng)
            self.trees.append(t)
            F = [ff + self.lr * tree_pred(t, b) for ff, b in zip(F, B)]
        return self

    def predict(self, X):
        B = self.bn.tf(X)
        return [self.f0 + self.lr * sum(tree_pred(t, b) for t in self.trees) for b in B]


class MLP:
    def __init__(self, n_in, n_hid=12, n_out=4, seed=0):
        rng = random.Random(seed)
        self.W1 = [[rng.gauss(0, math.sqrt(2 / n_in)) for _ in range(n_in)] for _ in range(n_hid)]
        self.b1 = [0.0] * n_hid
        self.W2 = [[rng.gauss(0, math.sqrt(1 / n_hid)) for _ in range(n_hid)] for _ in range(n_out)]
        self.b2 = [0.0] * n_out
        self.rng = rng

    def forward(self, x):
        h = [max(0.0, sum(w * xi for w, xi in zip(row, x)) + b) for row, b in zip(self.W1, self.b1)]
        return h, [sum(w * hi for w, hi in zip(row, h)) + b for row, b in zip(self.W2, self.b2)]

    def params(self):
        return [self.W1, self.b1, self.W2, self.b2]

    def fit(self, X, Y, Xv, Yv, epochs=150, lr=0.005, batch=32):
        shapes = self.params()
        m = [[[0.0] * len(r) for r in p] if isinstance(p[0], list) else [0.0] * len(p) for p in shapes]
        v = [[[0.0] * len(r) for r in p] if isinstance(p[0], list) else [0.0] * len(p) for p in shapes]
        b1c, b2c, eps, step = 0.9, 0.999, 1e-8, 0
        best, best_state, patience = 1e18, None, 0
        idx = list(range(len(X)))
        nh, no = len(self.b1), len(self.b2)
        for ep in range(epochs):
            self.rng.shuffle(idx)
            for s0 in range(0, len(idx), batch):
                bi = idx[s0:s0 + batch]
                gW1 = [[0.0] * len(X[0]) for _ in range(nh)]
                gb1 = [0.0] * nh
                gW2 = [[0.0] * nh for _ in range(no)]
                gb2 = [0.0] * no
                for i in bi:
                    x = X[i]
                    h, o = self.forward(x)
                    do = [2 * (oo - yy) / (len(bi) * no) for oo, yy in zip(o, Y[i])]
                    for k in range(no):
                        gb2[k] += do[k]
                        row = gW2[k]
                        for j in range(nh):
                            row[j] += do[k] * h[j]
                    for j in range(nh):
                        if h[j] > 0:
                            dh = sum(do[k] * self.W2[k][j] for k in range(no))
                            gb1[j] += dh
                            row = gW1[j]
                            for q in range(len(x)):
                                row[q] += dh * x[q]
                step += 1
                grads = [gW1, gb1, gW2, gb2]
                for pi, (P, G) in enumerate(zip(self.params(), grads)):
                    if isinstance(P[0], list):
                        for r in range(len(P)):
                            for c in range(len(P[r])):
                                g = G[r][c]
                                m[pi][r][c] = b1c * m[pi][r][c] + (1 - b1c) * g
                                v[pi][r][c] = b2c * v[pi][r][c] + (1 - b2c) * g * g
                                mh = m[pi][r][c] / (1 - b1c ** step)
                                vh = v[pi][r][c] / (1 - b2c ** step)
                                P[r][c] -= lr * mh / (math.sqrt(vh) + eps)
                    else:
                        for c in range(len(P)):
                            g = G[c]
                            m[pi][c] = b1c * m[pi][c] + (1 - b1c) * g
                            v[pi][c] = b2c * v[pi][c] + (1 - b2c) * g * g
                            mh = m[pi][c] / (1 - b1c ** step)
                            vh = v[pi][c] / (1 - b2c ** step)
                            P[c] -= lr * mh / (math.sqrt(vh) + eps)
            vl = sum(sum((a - b) ** 2 for a, b in zip(self.forward(x)[1], y)) for x, y in zip(Xv, Yv))
            if vl < best:
                best, patience = vl, 0
                best_state = json.loads(json.dumps(self.params()))
            else:
                patience += 1
                if patience >= 20:
                    break
        self.W1, self.b1, self.W2, self.b2 = best_state
        self.epochs_run = ep + 1
        return self

    def predict(self, X):
        return [self.forward(x)[1] for x in X]


def quantize_mlp(mlp, Xcal):
    """Post-training int8 quantisation (symmetric weights, per-tensor)."""
    def qparams(vals):
        s = max(abs(v) for v in vals) / 127.0
        return s if s > 0 else 1.0

    sx = qparams([v for x in Xcal for v in x])
    sw1 = qparams([w for r in mlp.W1 for w in r])
    hs = [mlp.forward(x)[0] for x in Xcal]
    sh = qparams([v for h in hs for v in h])
    sw2 = qparams([w for r in mlp.W2 for w in r])
    q = lambda v, s: max(-127, min(127, int(round(v / s))))
    W1q = [[q(w, sw1) for w in r] for r in mlp.W1]
    W2q = [[q(w, sw2) for w in r] for r in mlp.W2]
    b1q = [int(round(b / (sx * sw1))) for b in mlp.b1]     # int32 biases
    b2q = [int(round(b / (sh * sw2))) for b in mlp.b2]

    def predict(X):
        out = []
        for x in X:
            xq = [q(v, sx) for v in x]
            acc = [sum(w * xi for w, xi in zip(r, xq)) + b for r, b in zip(W1q, b1q)]
            h = [max(0, a) * sx * sw1 for a in acc]
            hq = [q(v, sh) for v in h]
            acc2 = [sum(w * hi for w, hi in zip(r, hq)) + b for r, b in zip(W2q, b2q)]
            out.append([a * sh * sw2 for a in acc2])
        return out
    return predict


# --------------------------------------------------------------------------
# Metrics
# --------------------------------------------------------------------------
def metrics(o, p):
    n = len(o)
    mo, mp = sum(o) / n, sum(p) / n
    rmse = math.sqrt(sum((a - b) ** 2 for a, b in zip(o, p)) / n)
    mae = sum(abs(a - b) for a, b in zip(o, p)) / n
    nse = 1 - sum((a - b) ** 2 for a, b in zip(o, p)) / sum((a - mo) ** 2 for a in o)
    so = math.sqrt(sum((a - mo) ** 2 for a in o) / n)
    sp = math.sqrt(sum((b - mp) ** 2 for b in p) / n)
    r = sum((a - mo) * (b - mp) for a, b in zip(o, p)) / (n * so * sp)
    kge = 1 - math.sqrt((r - 1) ** 2 + (sp / so - 1) ** 2 + (mp / mo - 1) ** 2)
    return dict(RMSE=rmse, MAE=mae, NSE=nse, KGE=kge, R2=r * r)


def run_all_models(Xtr, Ytr, Xte, Yte, mte, h, seed):
    sc = Scaler().fit(Xtr)
    Xs, Xts = sc.tf(Xtr), sc.tf(Xte)
    ysc = [Scaler().fit([[y[k]] for y in Ytr]) for k in range(4)]
    Ys = [[(y[k] - ysc[k].mu[0]) / ysc[k].sd[0] for k in range(4)] for y in Ytr]
    res, preds = {}, {}
    # persistence
    preds['Persistence'] = [[m[2][k] for k in range(4)] for m in mte]
    for name, ctor in [('MLR', lambda: Ridge()), ('RF', lambda: RandomForest(seed=seed)),
                       ('GBT', lambda: GBT(seed=seed))]:
        cols = []
        for k in range(4):
            mdl = ctor().fit(Xs if name != 'MLR' else Xs, [y[k] for y in Ytr])
            cols.append(mdl.predict(Xts))
        preds[name] = [[cols[k][i] for k in range(4)] for i in range(len(Xte))]
    nv = int(0.15 * len(Xs))
    mlp = MLP(len(FEATURES), seed=seed).fit(Xs[:-nv], Ys[:-nv], Xs[-nv:], Ys[-nv:])
    ps = mlp.predict(Xts)
    preds['MLP'] = [[p[k] * ysc[k].sd[0] + ysc[k].mu[0] for k in range(4)] for p in ps]
    for name, P in preds.items():
        res[name] = {str(DEPTHS_CM[k]): metrics([y[k] for y in Yte], [p[k] for p in P]) for k in range(4)}
    return res, preds, mlp, sc, ysc, Xts


def main():
    t_start = time.time()
    rng = random.Random(SEED)
    data, weather = {}, {}
    for s in SITES:
        rows, wx = simulate_site(s, rng, 'CT')
        data[s] = add_sensor_noise(rows, rng)
        weather[s] = wx
    ztr, _ = simulate_site('Karnal', rng, 'ZT-R', weather=weather['Karnal'])
    ztr = add_sensor_noise(ztr, rng)
    print(f'simulation done {time.time() - t_start:.0f}s')

    out = {'descriptive': {}, 'perf': {}, 'loso': {}, 'treatment': {}, 'edge': {}, 'importance': {}}
    # descriptive statistics (Table 2)
    for s, rows in data.items():
        d = {}
        for v in ['ta', 'rh', 'ws', 'ssh', 'rs', 'theta', 'obs5', 'obs10', 'obs20', 'obs50']:
            vals = [r[v] for r in rows]
            mu = sum(vals) / len(vals)
            d[v] = dict(mean=mu, min=min(vals), max=max(vals),
                        sd=math.sqrt(sum((x - mu) ** 2 for x in vals) / len(vals)))
        d['rain_annual'] = sum(r['rain'] for r in rows) / 3.0
        out['descriptive'][s] = d

    # treatment effect, wheat season (Nov-Feb), Karnal
    def season_stats(rows, z):
        v = [r[f'tz{z}'] for r in rows if r['doy'] >= 320 or r['doy'] <= 60]
        mu = sum(v) / len(v)
        return mu, math.sqrt(sum((x - mu) ** 2 for x in v) / len(v))
    for z in [5, 10]:
        ct, zt = season_stats(data['Karnal'], z), season_stats(ztr, z)
        may_ct = [r[f'tz{z}'] for r in data['Karnal'] if 290 <= r['doy'] <= 330]
        may_zt = [r[f'tz{z}'] for r in ztr if 290 <= r['doy'] <= 330]
        out['treatment'][str(z)] = dict(ct_mean=ct[0], ct_sd=ct[1], zt_mean=zt[0], zt_sd=zt[1],
                                        sow_ct=sum(may_ct) / len(may_ct), sow_zt=sum(may_zt) / len(may_zt))

    series = data['Karnal']
    saved = {}
    for s, rows in data.items():
        for h in HORIZONS:
            X, Y, meta = build_xy(rows, h)
            Xtr, Ytr, mtr, Xte, Yte, mte = split(X, Y, meta)
            res, preds, mlp, sc, ysc, Xts = run_all_models(Xtr, Ytr, Xte, Yte, mte, h, SEED + h)
            out['perf'][f'{s}_h{h}'] = res
            print(f'{s} h={h} done {time.time() - t_start:.0f}s  MLP epochs={mlp.epochs_run}')
            if h == 1:
                saved[s] = (mlp, sc, ysc, Xts, Yte, preds, mte, Xtr)
    # scatter & series data for figures (Karnal, h=1, test year)
    mlp, sc, ysc, Xts, Yte, preds, mte, Xtr = saved['Karnal']
    out['scatter'] = dict(obs=[y[0] for y in Yte], mlp=[p[0] for p in preds['MLP']])

    # permutation importance, MLP Karnal h=1, 5 cm
    def mlp_rmse5(Xs):
        P = mlp.predict(Xs)
        p = [q[0] * ysc[0].sd[0] + ysc[0].mu[0] for q in P]
        return metrics([y[0] for y in Yte], p)['RMSE']
    base = mlp_rmse5(Xts)
    prng = random.Random(7)
    for j, f in enumerate(FEATURES):
        incs = []
        for _ in range(5):
            col = [x[j] for x in Xts]
            prng.shuffle(col)
            Xp = [x[:j] + [c] + x[j + 1:] for x, c in zip(Xts, col)]
            incs.append(mlp_rmse5(Xp) - base)
        out['importance'][f] = sum(incs) / len(incs)

    # edge: int8 quantisation
    qpred = quantize_mlp(mlp, sc.tf(Xtr))
    qp = qpred(Xts)
    qp = [[p[k] * ysc[k].sd[0] + ysc[k].mu[0] for k in range(4)] for p in qp]
    nparam = len(mlp.W1) * len(mlp.W1[0]) + len(mlp.b1) + len(mlp.W2) * len(mlp.W2[0]) + len(mlp.b2)
    macs = len(mlp.W1) * len(mlp.W1[0]) + len(mlp.W2) * len(mlp.W2[0])
    out['edge'] = dict(
        n_params=nparam, macs=macs, size_fp32_bytes=4 * nparam,
        size_int8_bytes=len(mlp.W1) * len(mlp.W1[0]) + len(mlp.W2) * len(mlp.W2[0]) + 4 * (len(mlp.b1) + len(mlp.b2)) + 16,
        fp32={str(DEPTHS_CM[k]): metrics([y[k] for y in Yte], [p[k] for p in preds['MLP']]) for k in range(4)},
        int8={str(DEPTHS_CM[k]): metrics([y[k] for y in Yte], [p[k] for p in qp]) for k in range(4)})

    # transfer to residue-retained plot (train CT, test ZT-R year 3), MLP h=1
    X, Y, meta = build_xy(ztr, 1)
    _, _, _, Xz, Yz, _ = split(X, Y, meta)
    Pz = mlp.predict(sc.tf(Xz))
    Pz = [[p[k] * ysc[k].sd[0] + ysc[k].mu[0] for k in range(4)] for p in Pz]
    out['treatment']['transfer'] = {str(DEPTHS_CM[k]): metrics([y[k] for y in Yz], [p[k] for p in Pz]) for k in range(4)}

    # leave-one-site-out: train Karnal years 1-3, test Hisar year 3 (h=1)
    Xk, Yk, mk = build_xy(data['Karnal'], 1)
    Xh, Yh, mh = build_xy(data['Hisar'], 1)
    _, _, _, Xhte, Yhte, mhte = split(Xh, Yh, mh)
    nk = [i for i, m in enumerate(mk) if m[0] < 3]
    res, _, _, _, _, _ = run_all_models([Xk[i] for i in nk], [Yk[i] for i in nk], Xhte, Yhte, mhte, 1, SEED + 11)
    out['loso'] = res

    # time series for Figure 3 (Karnal, year 3)
    with open(os.path.join(OUT, 'series.csv'), 'w') as f:
        f.write('doy,ta,t5,t10,t20,t50,theta\n')
        for r in series:
            if r['year'] == 3:
                f.write(f"{r['doy']},{r['ta']:.3f},{r['obs5']:.3f},{r['obs10']:.3f},{r['obs20']:.3f},{r['obs50']:.3f},{r['theta']:.3f}\n")
    # node energy budget (datasheet-typical values; calculated, not measured)
    T_cyc = 900.0
    phases = dict(active=(4.0, 80.0), lora_tx=(0.2, 120.0), sleep=(T_cyc - 4.2, 0.150))
    q_mAs = sum(t * i for t, i in phases.values())
    i_avg = q_mAs / T_cyc
    cap = 6000.0 * 0.8
    out['energy'] = dict(i_avg_mA=i_avg, days_no_solar=cap / i_avg / 24, daily_mAh=i_avg * 24)
    out['runtime_s'] = time.time() - t_start
    with open(os.path.join(OUT, 'results.json'), 'w') as f:
        json.dump(out, f, indent=1)
    print(f'all done {time.time() - t_start:.0f}s')


if __name__ == '__main__':
    main()
