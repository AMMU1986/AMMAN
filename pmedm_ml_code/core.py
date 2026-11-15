"""Dependency-free numerical core: dense linear algebra, special functions and statistics.

Everything is written against the Python standard library only, so the whole
reanalysis can be reproduced on any machine with Python >= 3.9.
"""

import math
import random
from operator import mul
from statistics import NormalDist

_STD_NORMAL = NormalDist()


# ----------------------------------------------------------------------------
# Dense linear algebra (lists of lists)
# ----------------------------------------------------------------------------

def zeros(n, m):
    return [[0.0] * m for _ in range(n)]


def eye(n):
    a = zeros(n, n)
    for i in range(n):
        a[i][i] = 1.0
    return a


def transpose(a):
    return [list(col) for col in zip(*a)]


def dot(a, b):
    return sum(map(mul, a, b))


def matvec(a, x):
    return [sum(map(mul, row, x)) for row in a]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(map(mul, row, col)) for col in bt] for row in a]


def cholesky(a, jitter=0.0):
    """Lower Cholesky factor of a symmetric positive-definite matrix."""
    n = len(a)
    low = [[0.0] * n for _ in range(n)]
    for i in range(n):
        li = low[i]
        ai = a[i]
        for j in range(i + 1):
            lj = low[j]
            s = ai[j] - sum(map(mul, li[:j], lj[:j]))
            if i == j:
                s += jitter
                if s <= 0.0:
                    raise ValueError("matrix is not positive definite")
                li[i] = math.sqrt(s)
            else:
                li[j] = s / lj[j]
    return low


def cholesky_safe(a, start_jitter=1e-10, max_tries=8):
    jitter = 0.0
    for _ in range(max_tries):
        try:
            return cholesky(a, jitter)
        except ValueError:
            jitter = start_jitter if jitter == 0.0 else jitter * 100.0
    raise ValueError("Cholesky failed even with jitter")


def solve_lower(low, b):
    n = len(low)
    y = [0.0] * n
    for i in range(n):
        li = low[i]
        y[i] = (b[i] - sum(map(mul, li[:i], y[:i]))) / li[i]
    return y


def solve_upper_from_lower(low, y, low_t=None):
    """Solve L^T x = y given the lower factor L."""
    n = len(low)
    if low_t is None:
        low_t = transpose(low)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        ri = low_t[i]
        x[i] = (y[i] - sum(map(mul, ri[i + 1:], x[i + 1:]))) / ri[i]
    return x


def chol_solve(low, b, low_t=None):
    return solve_upper_from_lower(low, solve_lower(low, b), low_t)


def chol_inverse(low):
    n = len(low)
    low_t = transpose(low)
    cols = []
    for j in range(n):
        e = [0.0] * n
        e[j] = 1.0
        cols.append(chol_solve(low, e, low_t))
    return transpose(cols)


def chol_logdet(low):
    return 2.0 * sum(math.log(low[i][i]) for i in range(len(low)))


def lstsq(x, y, ridge=1e-10):
    """Ordinary (or lightly ridged) least squares. Returns beta and (X'X+rI)^-1."""
    p = len(x[0])
    xt = transpose(x)
    xtx = [[dot(xt[i], xt[j]) for j in range(p)] for i in range(p)]
    tr = sum(xtx[i][i] for i in range(p)) / p
    for i in range(p):
        xtx[i][i] += ridge * tr
    low = cholesky_safe(xtx)
    xty = [dot(xt[i], y) for i in range(p)]
    beta = chol_solve(low, xty)
    return beta, chol_inverse(low)


# ----------------------------------------------------------------------------
# Special functions and distributions
# ----------------------------------------------------------------------------

def norm_cdf(z):
    return _STD_NORMAL.cdf(z)


def norm_ppf(p):
    return _STD_NORMAL.inv_cdf(p)


def norm_pdf(z):
    return math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def _betacf(a, b, x):
    maxit, eps, fpmin = 400, 3e-15, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, maxit + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = fpmin if abs(d) < fpmin else d
        c = 1.0 + aa / c
        c = fpmin if abs(c) < fpmin else c
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = fpmin if abs(d) < fpmin else d
        c = 1.0 + aa / c
        c = fpmin if abs(c) < fpmin else c
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def betainc(a, b, x):
    """Regularised incomplete beta function I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    ln_bt = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
             + a * math.log(x) + b * math.log(1.0 - x))
    bt = math.exp(ln_bt)
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def t_two_sided_p(t, df):
    return betainc(0.5 * df, 0.5, df / (df + t * t))


def t_cdf(t, df):
    p_tail = 0.5 * betainc(0.5 * df, 0.5, df / (df + t * t))
    return 1.0 - p_tail if t >= 0 else p_tail


def t_ppf(p, df):
    lo, hi = -50.0, 50.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if t_cdf(mid, df) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def f_sf(f, d1, d2):
    """Upper-tail probability of the F distribution."""
    if f <= 0.0:
        return 1.0
    return betainc(0.5 * d2, 0.5 * d1, d2 / (d2 + d1 * f))


def f_ppf(p, d1, d2):
    lo, hi = 0.0, 1000.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if 1.0 - f_sf(mid, d1, d2) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ----------------------------------------------------------------------------
# Descriptive statistics and rank correlation
# ----------------------------------------------------------------------------

def mean(v):
    return sum(v) / len(v)


def var(v, ddof=1):
    m = mean(v)
    return sum((x - m) ** 2 for x in v) / (len(v) - ddof)


def std(v, ddof=1):
    return math.sqrt(var(v, ddof))


def pearson(a, b):
    ma, mb = mean(a), mean(b)
    sab = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    saa = sum((x - ma) ** 2 for x in a)
    sbb = sum((y - mb) ** 2 for y in b)
    return sab / math.sqrt(saa * sbb)


def rankdata(v):
    """Average ranks (1-based) with ties."""
    order = sorted(range(len(v)), key=lambda i: v[i])
    ranks = [0.0] * len(v)
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
            j += 1
        r = 0.5 * (i + j) + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def spearman(a, b):
    return pearson(rankdata(a), rankdata(b))


def kendall_tau_b(a, b):
    n = len(a)
    conc = disc = ties_a = ties_b = 0
    for i in range(n):
        for j in range(i + 1, n):
            da = a[i] - a[j]
            db = b[i] - b[j]
            if da == 0 and db == 0:
                continue
            if da == 0:
                ties_a += 1
            elif db == 0:
                ties_b += 1
            elif da * db > 0:
                conc += 1
            else:
                disc += 1
    denom = math.sqrt((conc + disc + ties_a) * (conc + disc + ties_b))
    return (conc - disc) / denom if denom > 0 else 0.0


def quantile(v, q):
    s = sorted(v)
    if not s:
        raise ValueError("empty")
    pos = q * (len(s) - 1)
    lo = int(math.floor(pos))
    hi = min(lo + 1, len(s) - 1)
    frac = pos - lo
    return s[lo] * (1.0 - frac) + s[hi] * frac


def bootstrap_ci(values_fn, n, n_boot=2000, alpha=0.05, seed=1):
    """Percentile bootstrap CI for a statistic computed from resampled indices."""
    rng = random.Random(seed)
    stats = []
    for _ in range(n_boot):
        idx = [rng.randrange(n) for _ in range(n)]
        stats.append(values_fn(idx))
    return quantile(stats, alpha / 2.0), quantile(stats, 1.0 - alpha / 2.0)


# ----------------------------------------------------------------------------
# Optimisation
# ----------------------------------------------------------------------------

def bfgs(fun_grad, x0, max_iter=200, gtol=1e-6, ftol=1e-10):
    """Quasi-Newton BFGS with Armijo backtracking. fun_grad(x) -> (f, g)."""
    n = len(x0)
    x = list(x0)
    try:
        f, g = fun_grad(x)
    except (ValueError, OverflowError, ZeroDivisionError):
        return x, float("inf")
    h = eye(n)
    for _ in range(max_iter):
        p = [-v for v in matvec(h, g)]
        slope = dot(p, g)
        if slope >= 0.0:
            h = eye(n)
            p = [-v for v in g]
            slope = dot(p, g)
        step = 1.0
        accepted = False
        while step > 1e-12:
            xn = [xi + step * pi for xi, pi in zip(x, p)]
            try:
                fn, gn = fun_grad(xn)
            except (ValueError, OverflowError, ZeroDivisionError):
                fn, gn = float("inf"), None
            if fn <= f + 1e-4 * step * slope:
                accepted = True
                break
            step *= 0.5
        if not accepted:
            break
        s = [a - b for a, b in zip(xn, x)]
        yv = [a - b for a, b in zip(gn, g)]
        sy = dot(s, yv)
        f_old = f
        x, f, g = xn, fn, gn
        if sy > 1e-12:
            hy = matvec(h, yv)
            yhy = dot(yv, hy)
            rho = 1.0 / sy
            for i in range(n):
                for j in range(n):
                    h[i][j] += (rho * rho * (sy + yhy) * s[i] * s[j]
                                - rho * (hy[i] * s[j] + s[i] * hy[j]))
        if math.sqrt(dot(g, g)) < gtol or abs(f_old - f) < ftol * (1.0 + abs(f)):
            break
    return x, f


def sigmoid(u):
    if u >= 0:
        e = math.exp(-u)
        return 1.0 / (1.0 + e)
    e = math.exp(u)
    return e / (1.0 + e)
