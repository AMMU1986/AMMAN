"""Surrogate models for the PM-EDM reanalysis (standard library only).

Every model is trained on z = ln(y) and returns, for each query point, a
predictive distribution on the log scale:

    ("normal", mean, sd)          Gaussian predictive distribution
    ("t", mean, scale, dof)       Student-t predictive distribution (OLS models)
    ("point", mean)               point prediction only

Inputs are tuples x = (t_off [us], t_on [us], current [A], powder) with
powder coded 0 = graphite, 1 = alumina, 2 = none (plain dielectric).
"""

import math
import random

from core import (bfgs, chol_inverse, chol_solve, cholesky_safe, chol_logdet,
                  dot, lstsq, mean, norm_ppf, solve_lower, transpose, var)

POWDERS = ("graphite", "alumina", "none")
BOUNDS = ((10.0, 75.0), (15.0, 100.0), (3.0, 9.0))  # design bounds of A, B, D
LEVELS = ((10.0, 50.0, 75.0), (15.0, 50.0, 100.0), (3.0, 6.0, 9.0))


def scale01(x):
    """Design-bound scaling of the three numeric factors to [0, 1]."""
    return [(x[j] - BOUNDS[j][0]) / (BOUNDS[j][1] - BOUNDS[j][0]) for j in range(3)]


def coded(x):
    """Design-bound coding to [-1, 1] used by the response-surface model."""
    return [2.0 * u - 1.0 for u in scale01(x)]


# ----------------------------------------------------------------------------
# Baselines and linear models
# ----------------------------------------------------------------------------

class MeanModel:
    name = "Mean"

    def fit(self, xs, z):
        self.m = mean(z)
        self.s2 = var(z) * (1.0 + 1.0 / len(z))
        self.n = len(z)
        return self

    def predict(self, xs):
        return [("t", self.m, math.sqrt(self.s2), self.n - 1) for _ in xs]

    def n_params(self):
        return 1


def _level_index(value, j):
    return min(range(3), key=lambda k: abs(LEVELS[j][k] - value))


def taguchi_features(x):
    f = [1.0]
    for j in range(3):
        lev = _level_index(x[j], j)
        f += [1.0 if lev == 1 else 0.0, 1.0 if lev == 2 else 0.0]
    f += [1.0 if x[3] == 1 else 0.0, 1.0 if x[3] == 2 else 0.0]
    return f


def powerlaw_features(x):
    t_off, t_on, cur, c = x
    return [1.0, math.log(cur), math.log(t_on), math.log(t_on + t_off),
            1.0 if c == 1 else 0.0, 1.0 if c == 2 else 0.0]


def rsm_features(x):
    v1, v2, v3 = coded(x)
    c = x[3]
    return [1.0, v1, v2, v3, v1 * v1, v2 * v2, v3 * v3, v1 * v2, v1 * v3, v2 * v3,
            1.0 if c == 1 else 0.0, 1.0 if c == 2 else 0.0]


RSM_TERMS = ["Intercept", "A", "B", "D", "A^2", "B^2", "D^2", "AB", "AD", "BD",
             "C[alumina]", "C[none]"]
POWERLAW_TERMS = ["ln C0", "ln I", "ln t_on", "ln(t_on+t_off)", "C[alumina]", "C[none]"]
TAGUCHI_TERMS = ["Intercept", "A=50", "A=75", "B=50", "B=100", "D=6", "D=9",
                 "C[alumina]", "C[none]"]


class LinearModel:
    """OLS on a fixed feature map with exact Student-t prediction intervals."""

    def __init__(self, name, feature_fn, terms=None):
        self.name = name
        self.feature_fn = feature_fn
        self.terms = terms

    def fit(self, xs, z):
        x_mat = [self.feature_fn(x) for x in xs]
        self.p = len(x_mat[0])
        self.n = len(z)
        self.beta, self.xtx_inv = lstsq(x_mat, z, ridge=1e-12)
        resid = [zi - dot(self.beta, fi) for zi, fi in zip(z, x_mat)]
        self.dof = self.n - self.p
        self.s2 = sum(r * r for r in resid) / self.dof
        self.sse = sum(r * r for r in resid)
        zbar = mean(z)
        self.r2 = 1.0 - self.sse / sum((zi - zbar) ** 2 for zi in z)
        self.se = [math.sqrt(self.s2 * self.xtx_inv[i][i]) for i in range(self.p)]
        return self

    def predict(self, xs):
        out = []
        for x in xs:
            f = self.feature_fn(x)
            m = dot(self.beta, f)
            lev = dot(f, [dot(row, f) for row in self.xtx_inv])
            out.append(("t", m, math.sqrt(self.s2 * (1.0 + lev)), self.dof))
        return out

    def n_params(self):
        return len(self.feature_fn((10.0, 15.0, 3.0, 0)))


# ----------------------------------------------------------------------------
# Gaussian process regression with a mixed (quantitative + qualitative) kernel
# ----------------------------------------------------------------------------

SQRT5 = math.sqrt(5.0)


class GPR:
    """Zero-mean GP on standardised ln(y); ARD Matern-5/2 x exchangeable powder kernel.

    Hyperparameters theta = [ln sf2, ln l1, ln l2, ln l3, logit rho, ln sn2] are
    estimated by maximising the log marginal likelihood plus weakly informative
    log-priors (type-II MAP).
    """

    name = "GPR"
    # Gamma(shape, rate) priors on sf2, lengthscales and noise; Beta(2, 2) on rho
    PRIOR_SF2 = (2.0, 0.15)
    PRIOR_LS = (3.0, 6.0)
    PRIOR_SN2 = (1.1, 0.05)
    PRIOR_RHO = (2.0, 2.0)
    NOISE_FLOOR = 1e-6

    def __init__(self, seed=0, n_starts=4, fixed_theta=None, fixed_noise_sd_log=None):
        self.seed = seed
        self.n_starts = n_starts
        self.fixed_theta = fixed_theta
        # optional: noise s.d. on the ln(y) scale fixed at the replicate (pure-error) value
        self.fixed_noise_sd_log = fixed_noise_sd_log
        if fixed_noise_sd_log is not None:
            self.name = "GPR (pure-error noise)"

    # --- kernel -----------------------------------------------------------
    @staticmethod
    def _unpack(theta):
        sf2 = math.exp(theta[0])
        ls = [math.exp(t) for t in theta[1:4]]
        rho = 1.0 / (1.0 + math.exp(-theta[4]))
        sn2 = math.exp(theta[5]) + GPR.NOISE_FLOOR
        return sf2, ls, rho, sn2

    def kernel(self, a, b, theta=None):
        sf2, ls, rho, _ = self._unpack(self.theta if theta is None else theta)
        r2 = sum(((a[j] - b[j]) / ls[j]) ** 2 for j in range(3))
        r = math.sqrt(r2)
        km = (1.0 + SQRT5 * r + 5.0 * r2 / 3.0) * math.exp(-SQRT5 * r)
        return sf2 * km * (1.0 if a[3] == b[3] else rho)

    def _neg_log_post(self, theta, us, zt):
        n = len(us)
        sf2, ls, rho, sn2 = self._unpack(theta)
        kmat = [[0.0] * n for _ in range(n)]
        dks = [[[0.0] * n for _ in range(n)] for _ in range(6)]
        for i in range(n):
            ui = us[i]
            for j in range(i + 1):
                uj = us[j]
                d2 = [((ui[k] - uj[k]) / ls[k]) ** 2 for k in range(3)]
                r2 = d2[0] + d2[1] + d2[2]
                r = math.sqrt(r2)
                e = math.exp(-SQRT5 * r)
                km = (1.0 + SQRT5 * r + 5.0 * r2 / 3.0) * e
                cat = 1.0 if ui[3] == uj[3] else rho
                kij = sf2 * km * cat
                kmat[i][j] = kmat[j][i] = kij
                dks[0][i][j] = dks[0][j][i] = kij
                common = sf2 * cat * (5.0 / 3.0) * (1.0 + SQRT5 * r) * e
                for k in range(3):
                    v = common * d2[k]
                    dks[1 + k][i][j] = dks[1 + k][j][i] = v
                if ui[3] != uj[3]:
                    v = sf2 * km * rho * (1.0 - rho)
                    dks[4][i][j] = dks[4][j][i] = v
            kmat[i][i] += sn2
            dks[5][i][i] = sn2 - self.NOISE_FLOOR
        low = cholesky_safe(kmat)
        alpha = chol_solve(low, zt)
        nll = 0.5 * dot(zt, alpha) + 0.5 * chol_logdet(low) + 0.5 * n * math.log(2 * math.pi)
        kinv = chol_inverse(low)
        grad = []
        for d in dks:
            # d(NLL)/d(theta) = -0.5 tr((alpha alpha^T - K^-1) dK)
            tr = 0.0
            for i in range(n):
                ai = alpha[i]
                di = d[i]
                ki = kinv[i]
                tr += sum((ai * alpha[j] - ki[j]) * di[j] for j in range(n))
            grad.append(-0.5 * tr)
        # log-priors (with Jacobian of the log / logit transforms)
        lp, glp = 0.0, [0.0] * 6
        for idx, (shape, rate) in [(0, self.PRIOR_SF2), (1, self.PRIOR_LS), (2, self.PRIOR_LS),
                                   (3, self.PRIOR_LS), (5, self.PRIOR_SN2)]:
            s = math.exp(theta[idx])
            lp += shape * theta[idx] - rate * s
            glp[idx] = shape - rate * s
        a_b, b_b = self.PRIOR_RHO
        lp += a_b * math.log(rho) + b_b * math.log(1.0 - rho)
        glp[4] = a_b * (1.0 - rho) - b_b * rho
        out = [g - h for g, h in zip(grad, glp)]
        if self.fixed_noise_sd_log is not None:
            out[5] = 0.0  # noise held fixed: no gradient, BFGS keeps theta[5] constant
        return nll - lp, out

    def fit(self, xs, z):
        self.xs = list(xs)
        self.us = [scale01(x) + [x[3]] for x in xs]
        self.zm = mean(z)
        self.zs = math.sqrt(var(z)) if len(z) > 1 else 1.0
        zt = [(v - self.zm) / self.zs for v in z]
        if self.fixed_theta is not None:
            self.theta = list(self.fixed_theta)
            self.obj = None
        else:
            rng = random.Random(self.seed)
            starts = [[0.0, math.log(0.5), math.log(0.5), math.log(0.5), 0.0, math.log(0.1)]]
            for _ in range(self.n_starts - 1):
                starts.append([math.log(rng.gammavariate(2.0, 1.0 / 2.0)),
                               math.log(rng.gammavariate(3.0, 1.0 / 6.0)),
                               math.log(rng.gammavariate(3.0, 1.0 / 6.0)),
                               math.log(rng.gammavariate(3.0, 1.0 / 6.0)),
                               rng.uniform(-1.5, 1.5),
                               math.log(rng.uniform(0.01, 0.5))])
            if self.fixed_noise_sd_log is not None:
                sn2 = (self.fixed_noise_sd_log / self.zs) ** 2
                for s0 in starts:
                    s0[5] = math.log(max(sn2 - self.NOISE_FLOOR, 1e-12))
            best = None
            for s0 in starts:
                th, f = bfgs(lambda t: self._neg_log_post(t, self.us, zt), s0, max_iter=80)
                if best is None or f < best[1]:
                    best = (th, f)
            self.theta, self.obj = best
        self._prepare(zt)
        return self

    def _prepare(self, zt):
        n = len(self.us)
        _, _, _, sn2 = self._unpack(self.theta)
        self.sn2 = sn2
        kmat = [[self.kernel(self.us[i], self.us[j]) for j in range(n)] for i in range(n)]
        for i in range(n):
            kmat[i][i] += sn2
        self.low = cholesky_safe(kmat)
        self.low_t = transpose(self.low)
        self.alpha = chol_solve(self.low, zt, self.low_t)
        self.zt = zt

    def latent(self, xs):
        """Posterior mean and variance of the latent f (log scale, no noise)."""
        out = []
        sf2 = self._unpack(self.theta)[0]
        for x in xs:
            u = scale01(x) + [x[3]]
            ks = [self.kernel(u, ui) for ui in self.us]
            m = dot(ks, self.alpha)
            v = solve_lower(self.low, ks)
            fv = max(sf2 - dot(v, v), 1e-12)
            out.append((self.zm + self.zs * m, self.zs * self.zs * fv))
        return out

    def latent_mean(self, xs):
        out = []
        for x in xs:
            u = scale01(x) + [x[3]]
            out.append(self.zm + self.zs * dot([self.kernel(u, ui) for ui in self.us], self.alpha))
        return out

    def predict(self, xs):
        noise = self.zs * self.zs * self.sn2
        return [("normal", m, math.sqrt(v + noise)) for m, v in self.latent(xs)]

    def latent_joint(self, xs):
        """Joint posterior mean vector and covariance matrix of latent f at xs."""
        us = [scale01(x) + [x[3]] for x in xs]
        means = []
        vs = []
        for u in us:
            ks = [self.kernel(u, ui) for ui in self.us]
            means.append(self.zm + self.zs * dot(ks, self.alpha))
            vs.append(solve_lower(self.low, ks))
        m = len(us)
        cov = [[0.0] * m for _ in range(m)]
        s2 = self.zs * self.zs
        for i in range(m):
            for j in range(i + 1):
                c = s2 * (self.kernel(us[i], us[j]) - dot(vs[i], vs[j]))
                cov[i][j] = cov[j][i] = c
        return means, cov

    def hyper(self):
        sf2, ls, rho, sn2 = self._unpack(self.theta)
        return {"sf2": sf2, "lengthscales": ls, "rho": rho, "sn2": sn2,
                "noise_sd_log": self.zs * math.sqrt(sn2), "z_mean": self.zm, "z_sd": self.zs}

    def effective_dof(self):
        """tr(K_f (K_f + sn2 I)^-1): effective number of parameters of the GP smoother."""
        n = len(self.us)
        kinv = chol_inverse(self.low)
        kf = [[self.kernel(self.us[i], self.us[j]) for j in range(n)] for i in range(n)]
        return sum(dot(kf[i], [kinv[k][i] for k in range(n)]) for i in range(n))

    def n_params(self):
        return 6

    def loo_from_fixed(self):
        """Closed-form LOO predictive means/variances with fixed hyperparameters."""
        kinv = chol_inverse(self.low)
        out = []
        for i in range(len(self.us)):
            kii = kinv[i][i]
            m = self.zt[i] - self.alpha[i] / kii
            out.append((self.zm + self.zs * m, self.zs * self.zs / kii))
        return out


# ----------------------------------------------------------------------------
# Regression trees, random forest and second-order gradient boosting
# ----------------------------------------------------------------------------

CAT_SPLITS = ((0,), (1,), (2,))  # one-vs-rest partitions of the 3 powder levels


def _feat(x):
    return (x[0], x[1], x[2], x[3])


class _Node:
    __slots__ = ("feat", "thr", "cats", "left", "right", "value")

    def __init__(self):
        self.feat = None
        self.thr = None
        self.cats = None
        self.left = None
        self.right = None
        self.value = 0.0


def _goes_left(node, x):
    if node.feat == 3:
        return x[3] in node.cats
    return x[node.feat] <= node.thr


def tree_predict(node, x):
    while node.feat is not None:
        node = node.left if _goes_left(node, x) else node.right
    return node.value


def tree_leaves(node):
    if node.feat is None:
        return 1
    return tree_leaves(node.left) + tree_leaves(node.right)


def build_cart(xs, y, idx, rng, mtry, min_leaf, depth=0, max_depth=None):
    node = _Node()
    vals = [y[i] for i in idx]
    node.value = sum(vals) / len(vals)
    if len(idx) < 2 * min_leaf or (max_depth is not None and depth >= max_depth):
        return node
    feats = rng.sample(range(4), mtry) if mtry < 4 else list(range(4))
    total = sum(vals)
    n = len(idx)
    best = (1e-12, None)
    for f in feats:
        if f == 3:
            for cats in CAT_SPLITS:
                left = [i for i in idx if xs[i][3] in cats]
                nl = len(left)
                if nl < min_leaf or n - nl < min_leaf:
                    continue
                sl = sum(y[i] for i in left)
                sr = total - sl
                gain = sl * sl / nl + sr * sr / (n - nl) - total * total / n
                if gain > best[0]:
                    best = (gain, (3, None, cats))
        else:
            order = sorted(idx, key=lambda i: xs[i][f])
            sl = 0.0
            for k in range(n - 1):
                sl += y[order[k]]
                nl = k + 1
                a, b = xs[order[k]][f], xs[order[k + 1]][f]
                if a == b or nl < min_leaf or n - nl < min_leaf:
                    continue
                sr = total - sl
                gain = sl * sl / nl + sr * sr / (n - nl) - total * total / n
                if gain > best[0]:
                    best = (gain, (f, 0.5 * (a + b), None))
    if best[1] is None:
        return node
    f, thr, cats = best[1]
    node.feat, node.thr, node.cats = f, thr, cats
    li = [i for i in idx if _goes_left(node, xs[i])]
    ri = [i for i in idx if not _goes_left(node, xs[i])]
    node.left = build_cart(xs, y, li, rng, mtry, min_leaf, depth + 1, max_depth)
    node.right = build_cart(xs, y, ri, rng, mtry, min_leaf, depth + 1, max_depth)
    return node


class RandomForest:
    name = "RF"

    def __init__(self, n_trees=300, mtry=2, min_leaf=2, seed=0):
        self.n_trees, self.mtry, self.min_leaf, self.seed = n_trees, mtry, min_leaf, seed

    def fit(self, xs, z):
        rng = random.Random(self.seed)
        xs = [_feat(x) for x in xs]
        n = len(xs)
        self.trees = []
        for _ in range(self.n_trees):
            boot = [rng.randrange(n) for _ in range(n)]
            self.trees.append(build_cart(xs, z, boot, rng, self.mtry, self.min_leaf))
        return self

    def predict_point(self, xs):
        return [sum(tree_predict(t, _feat(x)) for t in self.trees) / len(self.trees) for x in xs]

    def predict(self, xs):
        return [("point", m) for m in self.predict_point(xs)]

    def n_params(self):
        return sum(tree_leaves(t) for t in self.trees)


def build_xgb_tree(xs, g, h, idx, lam, gamma, min_child, depth, max_depth):
    node = _Node()
    gs = sum(g[i] for i in idx)
    hs = sum(h[i] for i in idx)
    node.value = -gs / (hs + lam)
    if depth >= max_depth:
        return node
    parent = gs * gs / (hs + lam)
    best = (0.0, None)
    for f in range(4):
        if f == 3:
            for cats in CAT_SPLITS:
                gl = hl = 0.0
                for i in idx:
                    if xs[i][3] in cats:
                        gl += g[i]
                        hl += h[i]
                gr, hr = gs - gl, hs - hl
                if hl < min_child or hr < min_child:
                    continue
                gain = 0.5 * (gl * gl / (hl + lam) + gr * gr / (hr + lam) - parent) - gamma
                if gain > best[0]:
                    best = (gain, (3, None, cats))
        else:
            order = sorted(idx, key=lambda i: xs[i][f])
            gl = hl = 0.0
            for k in range(len(order) - 1):
                gl += g[order[k]]
                hl += h[order[k]]
                a, b = xs[order[k]][f], xs[order[k + 1]][f]
                if a == b:
                    continue
                gr, hr = gs - gl, hs - hl
                if hl < min_child or hr < min_child:
                    continue
                gain = 0.5 * (gl * gl / (hl + lam) + gr * gr / (hr + lam) - parent) - gamma
                if gain > best[0]:
                    best = (gain, (f, 0.5 * (a + b), None))
    if best[1] is None:
        return node
    node.feat, node.thr, node.cats = best[1]
    li = [i for i in idx if _goes_left(node, xs[i])]
    ri = [i for i in idx if not _goes_left(node, xs[i])]
    node.left = build_xgb_tree(xs, g, h, li, lam, gamma, min_child, depth + 1, max_depth)
    node.right = build_xgb_tree(xs, g, h, ri, lam, gamma, min_child, depth + 1, max_depth)
    return node


class GradientBoosting:
    """Second-order boosted trees following the XGBoost objective (squared loss)."""

    name = "XGB"

    def __init__(self, n_rounds=300, eta=0.05, max_depth=2, lam=1.0, gamma=0.0,
                 min_child=2.0, subsample=0.8, seed=0):
        self.n_rounds, self.eta, self.max_depth = n_rounds, eta, max_depth
        self.lam, self.gamma, self.min_child = lam, gamma, min_child
        self.subsample, self.seed = subsample, seed

    def fit(self, xs, z):
        rng = random.Random(self.seed)
        xs = [_feat(x) for x in xs]
        n = len(xs)
        self.base = mean(z)
        pred = [self.base] * n
        self.trees = []
        for _ in range(self.n_rounds):
            g = [pred[i] - z[i] for i in range(n)]
            h = [1.0] * n
            if self.subsample < 1.0:
                m = max(2, int(round(self.subsample * n)))
                idx = rng.sample(range(n), m)
            else:
                idx = list(range(n))
            tree = build_xgb_tree(xs, g, h, idx, self.lam, self.gamma, self.min_child, 0,
                                  self.max_depth)
            self.trees.append(tree)
            for i in range(n):
                pred[i] += self.eta * tree_predict(tree, xs[i])
        return self

    def predict_point(self, xs):
        out = []
        for x in xs:
            f = _feat(x)
            out.append(self.base + self.eta * sum(tree_predict(t, f) for t in self.trees))
        return out

    def predict(self, xs):
        return [("point", m) for m in self.predict_point(xs)]

    def n_params(self):
        return 1 + sum(tree_leaves(t) for t in self.trees)


# ----------------------------------------------------------------------------
# ANFIS (zero-order Takagi-Sugeno, grid partition, generalised bell MFs)
# ----------------------------------------------------------------------------

class ANFIS:
    """Zero-order Sugeno ANFIS on the three numeric factors with additive powder offsets.

    Hybrid learning: consequents (rule constants and powder offsets) by least
    squares for fixed premises; premise parameters (a, b, c of every bell MF)
    by quasi-Newton descent on the training SSE (at most 100 iterations).
    """

    def __init__(self, n_mf=2, max_iter=100, ridge=1e-6):
        self.m = n_mf
        self.name = "ANFIS-%dMF" % n_mf
        self.max_iter = max_iter
        self.ridge = ridge
        self.rules = [(i, j, k) for i in range(n_mf) for j in range(n_mf) for k in range(n_mf)]

    def _init_premise(self):
        th = []
        for _ in range(3):
            for q in range(self.m):
                c = q / (self.m - 1)
                a = 0.5 / (self.m - 1)
                th += [math.log(a), math.log(2.0), c]
        return th

    def _mfs(self, th, u):
        """Membership grades mu[j][q] of input j in MF q."""
        out = []
        for j in range(3):
            row = []
            for q in range(self.m):
                base = (j * self.m + q) * 3
                a, b, c = math.exp(th[base]), math.exp(th[base + 1]), th[base + 2]
                t = abs((u[j] - c) / a)
                row.append(1.0 / (1.0 + t ** (2.0 * b)) if t > 0 else 1.0)
            out.append(row)
        return out

    def _design(self, th, us, cs):
        rows = []
        for u, c in zip(us, cs):
            mu = self._mfs(th, u)
            w = [mu[0][i] * mu[1][j] * mu[2][k] for i, j, k in self.rules]
            sw = sum(w)
            wn = [v / sw for v in w] if sw > 0 else [1.0 / len(w)] * len(w)
            rows.append(wn + [1.0 if c == 1 else 0.0, 1.0 if c == 2 else 0.0])
        return rows

    def _sse(self, th, us, cs, z):
        x_mat = self._design(th, us, cs)
        beta, _ = lstsq(x_mat, z, ridge=self.ridge)
        return sum((zi - dot(beta, r)) ** 2 for zi, r in zip(z, x_mat)), beta

    def fit(self, xs, z):
        us = [scale01(x) for x in xs]
        cs = [x[3] for x in xs]

        def fg(th):
            f0, _ = self._sse(th, us, cs, z)
            g = []
            for i in range(len(th)):
                tp = list(th)
                tm = list(th)
                tp[i] += 1e-5
                tm[i] -= 1e-5
                g.append((self._sse(tp, us, cs, z)[0] - self._sse(tm, us, cs, z)[0]) / 2e-5)
            return f0, g

        th, _ = bfgs(fg, self._init_premise(), max_iter=self.max_iter, gtol=1e-8)
        self.th = th
        self.sse, self.beta = self._sse(th, us, cs, z)
        return self

    def predict(self, xs):
        us = [scale01(x) for x in xs]
        cs = [x[3] for x in xs]
        return [("point", dot(self.beta, r)) for r in self._design(self.th, us, cs)]

    def n_params(self):
        return 3 * 3 * self.m + self.m ** 3 + 2


# ----------------------------------------------------------------------------
# Neural networks: MC-dropout MLP and deep ensemble (Adam, full batch)
# ----------------------------------------------------------------------------

def nn_inputs(x):
    v = coded(x)
    return v + [1.0 if x[3] == q else 0.0 for q in range(3)]


def _softplus(u):
    return math.log1p(math.exp(-abs(u))) + max(u, 0.0)


class _MLP:
    """One hidden tanh layer; n_out = 1 (mean) or 2 (mean, softplus variance)."""

    def __init__(self, n_in, n_hidden, n_out, rng):
        lim1 = math.sqrt(6.0 / (n_in + n_hidden))
        lim2 = math.sqrt(6.0 / (n_hidden + n_out))
        self.w1 = [[rng.uniform(-lim1, lim1) for _ in range(n_in)] for _ in range(n_hidden)]
        self.b1 = [0.0] * n_hidden
        self.w2 = [[rng.uniform(-lim2, lim2) for _ in range(n_hidden)] for _ in range(n_out)]
        self.b2 = [0.0] * n_out
        if n_out == 2:
            self.b2[1] = math.log(math.exp(0.5) - 1.0)
        self.n_in, self.n_hidden, self.n_out = n_in, n_hidden, n_out

    def params(self):
        return [self.w1, self.b1, self.w2, self.b2]

    def count(self):
        return self.n_hidden * (self.n_in + 1) + self.n_out * (self.n_hidden + 1)

    def forward(self, x, mask=None):
        h = []
        for k in range(self.n_hidden):
            a = self.b1[k] + dot(self.w1[k], x)
            v = math.tanh(a)
            if mask is not None:
                v *= mask[k]
            h.append(v)
        out = [self.b2[o] + dot(self.w2[o], h) for o in range(self.n_out)]
        return h, out


def _train_mlp(net, xs, ys, epochs, lr, wd, rng, p_drop=0.0, nll=False):
    """Full-batch Adam. Loss: MSE (or Gaussian NLL) + wd * ||W||^2."""
    n = len(xs)
    nh, no, ni = net.n_hidden, net.n_out, net.n_in
    m_state = [[[0.0] * ni for _ in range(nh)], [0.0] * nh, [[0.0] * nh for _ in range(no)],
               [0.0] * no]
    v_state = [[[0.0] * ni for _ in range(nh)], [0.0] * nh, [[0.0] * nh for _ in range(no)],
               [0.0] * no]
    b1c, b2c, eps = 0.9, 0.999, 1e-8
    keep = 1.0 - p_drop
    for ep in range(1, epochs + 1):
        gw1 = [[0.0] * ni for _ in range(nh)]
        gb1 = [0.0] * nh
        gw2 = [[0.0] * nh for _ in range(no)]
        gb2 = [0.0] * no
        for x, y in zip(xs, ys):
            if p_drop > 0.0:
                mask = [(1.0 / keep) if rng.random() < keep else 0.0 for _ in range(nh)]
            else:
                mask = None
            pre = [net.b1[k] + dot(net.w1[k], x) for k in range(nh)]
            th = [math.tanh(a) for a in pre]
            h = [th[k] * mask[k] for k in range(nh)] if mask else th
            out = [net.b2[o] + dot(net.w2[o], h) for o in range(no)]
            if nll:
                mu, s_raw = out
                var_ = _softplus(s_raw) + 1e-4
                r = mu - y
                d_out = [r / var_, 0.5 * (1.0 / var_ - r * r / (var_ * var_)) * (1.0 / (1.0 + math.exp(-s_raw)))]
            else:
                d_out = [2.0 * (out[0] - y)]
            dh = [0.0] * nh
            for o in range(no):
                do = d_out[o] / n
                gb2[o] += do
                row = gw2[o]
                wrow = net.w2[o]
                for k in range(nh):
                    row[k] += do * h[k]
                    dh[k] += do * wrow[k]
            for k in range(nh):
                if mask is not None:
                    dh[k] *= mask[k]
                da = dh[k] * (1.0 - th[k] * th[k])
                gb1[k] += da
                row = gw1[k]
                for i in range(ni):
                    row[i] += da * x[i]
        # weight decay and Adam update
        grads = [gw1, gb1, gw2, gb2]
        params = net.params()
        bc1 = 1.0 - b1c ** ep
        bc2 = 1.0 - b2c ** ep
        for pi, (p, g, ms, vs) in enumerate(zip(params, grads, m_state, v_state)):
            is_w = pi in (0, 2)
            if isinstance(p[0], list):
                for r in range(len(p)):
                    pr, gr, mr, vr = p[r], g[r], ms[r], vs[r]
                    for c in range(len(pr)):
                        gg = gr[c] + (2.0 * wd * pr[c] if is_w else 0.0)
                        mr[c] = b1c * mr[c] + (1 - b1c) * gg
                        vr[c] = b2c * vr[c] + (1 - b2c) * gg * gg
                        pr[c] -= lr * (mr[c] / bc1) / (math.sqrt(vr[c] / bc2) + eps)
            else:
                for c in range(len(p)):
                    gg = g[c]
                    ms[c] = b1c * ms[c] + (1 - b1c) * gg
                    vs[c] = b2c * vs[c] + (1 - b2c) * gg * gg
                    p[c] -= lr * (ms[c] / bc1) / (math.sqrt(vs[c] / bc2) + eps)
    return net


class MCDropoutMLP:
    name = "MC-dropout"

    def __init__(self, n_hidden=16, p_drop=0.1, epochs=1500, lr=0.01, wd=1e-3, t_samples=200,
                 seed=0):
        self.n_hidden, self.p, self.epochs, self.lr, self.wd = n_hidden, p_drop, epochs, lr, wd
        self.t, self.seed = t_samples, seed

    def fit(self, xs, z):
        rng = random.Random(self.seed)
        self.zm, self.zs = mean(z), math.sqrt(var(z))
        xin = [nn_inputs(x) for x in xs]
        yt = [(v - self.zm) / self.zs for v in z]
        self.net = _train_mlp(_MLP(len(xin[0]), self.n_hidden, 1, rng), xin, yt, self.epochs,
                              self.lr, self.wd, rng, p_drop=self.p)
        self.rng = random.Random(self.seed + 7)
        tr = self._mc(xin)
        self.noise_var = sum((m - y) ** 2 for (m, _), y in zip(tr, yt)) / len(yt)
        return self

    def _mc(self, xin):
        keep = 1.0 - self.p
        out = []
        for x in xin:
            vals = []
            for _ in range(self.t):
                mask = [(1.0 / keep) if self.rng.random() < keep else 0.0
                        for _ in range(self.n_hidden)]
                vals.append(self.net.forward(x, mask)[1][0])
            out.append((mean(vals), var(vals)))
        return out

    def predict(self, xs):
        res = []
        for m, v in self._mc([nn_inputs(x) for x in xs]):
            res.append(("normal", self.zm + self.zs * m,
                        self.zs * math.sqrt(v + self.noise_var)))
        return res

    def n_params(self):
        return self.n_hidden * (6 + 1) + (self.n_hidden + 1)


class DeepEnsemble:
    name = "Deep ensemble"

    def __init__(self, n_members=5, n_hidden=16, epochs=1500, lr=0.01, wd=1e-3, seed=0):
        self.k, self.n_hidden, self.epochs, self.lr, self.wd = n_members, n_hidden, epochs, lr, wd
        self.seed = seed

    def fit(self, xs, z):
        self.zm, self.zs = mean(z), math.sqrt(var(z))
        xin = [nn_inputs(x) for x in xs]
        yt = [(v - self.zm) / self.zs for v in z]
        self.nets = []
        for k in range(self.k):
            rng = random.Random(1000 * self.seed + k)
            net = _MLP(len(xin[0]), self.n_hidden, 2, rng)
            self.nets.append(_train_mlp(net, xin, yt, self.epochs, self.lr, self.wd, rng,
                                        nll=True))
        return self

    def predict(self, xs):
        res = []
        for x in xs:
            xi = nn_inputs(x)
            mus, vs = [], []
            for net in self.nets:
                mu, s_raw = net.forward(xi)[1]
                mus.append(mu)
                vs.append(_softplus(s_raw) + 1e-4)
            m = mean(mus)
            v = mean([vv + mm * mm for vv, mm in zip(vs, mus)]) - m * m
            res.append(("normal", self.zm + self.zs * m, self.zs * math.sqrt(max(v, 1e-12))))
        return res

    def n_params(self):
        return self.k * (self.n_hidden * (6 + 1) + 2 * (self.n_hidden + 1))


# ----------------------------------------------------------------------------
# Factory
# ----------------------------------------------------------------------------

MODEL_KEYS = ["mean", "taguchi", "powerlaw", "rsm", "gpr", "gpr_pe", "rf", "xgb", "anfis2",
              "anfis3", "mcdrop", "deepens"]

# replicate (pure-error) s.d. of ln(y) at A2B3C1D3 from run 24 + three confirmation runs
PURE_ERROR_SD_LOG = {"mrr": 0.002511, "twr": 0.024923}

MODEL_LABELS = {
    "mean": "Mean (null)",
    "taguchi": "Taguchi main effects",
    "powerlaw": "Physics-guided power law",
    "rsm": "RSM (quadratic)",
    "gpr": "GPR (Matern-5/2 + powder kernel)",
    "gpr_pe": "GPR, noise fixed at replicate error",
    "rf": "Random forest",
    "xgb": "XGBoost-type GBT",
    "anfis2": "ANFIS, 2 MF/input",
    "anfis3": "ANFIS, 3 MF/input",
    "mcdrop": "MC-dropout MLP",
    "deepens": "Deep ensemble",
}


def make_model(key, seed=0, resp=None):
    if key == "gpr_pe":
        return GPR(seed=seed, fixed_noise_sd_log=PURE_ERROR_SD_LOG[resp])
    if key == "mean":
        return MeanModel()
    if key == "taguchi":
        return LinearModel("Taguchi", taguchi_features, TAGUCHI_TERMS)
    if key == "powerlaw":
        return LinearModel("Power law", powerlaw_features, POWERLAW_TERMS)
    if key == "rsm":
        return LinearModel("RSM", rsm_features, RSM_TERMS)
    if key == "gpr":
        return GPR(seed=seed)
    if key == "rf":
        return RandomForest(seed=seed)
    if key == "xgb":
        return GradientBoosting(seed=seed)
    if key == "anfis2":
        return ANFIS(2)
    if key == "anfis3":
        return ANFIS(3)
    if key == "mcdrop":
        return MCDropoutMLP(seed=seed)
    if key == "deepens":
        return DeepEnsemble(seed=seed)
    raise KeyError(key)


def interval(dist, level):
    """Central predictive interval on the log scale."""
    a = 0.5 * (1.0 + level)
    if dist[0] == "normal":
        q = norm_ppf(a)
        return dist[1] - q * dist[2], dist[1] + q * dist[2]
    if dist[0] == "t":
        from core import t_ppf
        q = t_ppf(a, dist[3])
        return dist[1] - q * dist[2], dist[1] + q * dist[2]
    raise ValueError("point prediction has no interval")
