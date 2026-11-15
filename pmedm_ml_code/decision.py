"""Multi-objective optimisation and decision-making tools (standard library only).

* NSGA-II (SBX crossover, polynomial mutation, crowding distance)
* exact 2-D hypervolume and hypervolume improvement
* grey relational analysis (GRA), TOPSIS, entropy and CRITIC weights
"""

import math
import random


# ----------------------------------------------------------------------------
# Pareto utilities (all objectives minimised)
# ----------------------------------------------------------------------------

def dominates(a, b):
    return all(x <= y for x, y in zip(a, b)) and any(x < y for x, y in zip(a, b))


def nondominated(points):
    """Indices of the non-dominated points."""
    idx = []
    for i, p in enumerate(points):
        if not any(dominates(q, p) for j, q in enumerate(points) if j != i):
            idx.append(i)
    return idx


def fast_nondominated_sort(objs):
    n = len(objs)
    s = [[] for _ in range(n)]
    cnt = [0] * n
    fronts = [[]]
    rank = [0] * n
    for p in range(n):
        for q in range(n):
            if p == q:
                continue
            if dominates(objs[p], objs[q]):
                s[p].append(q)
            elif dominates(objs[q], objs[p]):
                cnt[p] += 1
        if cnt[p] == 0:
            rank[p] = 0
            fronts[0].append(p)
    i = 0
    while fronts[i]:
        nxt = []
        for p in fronts[i]:
            for q in s[p]:
                cnt[q] -= 1
                if cnt[q] == 0:
                    rank[q] = i + 1
                    nxt.append(q)
        i += 1
        fronts.append(nxt)
    return fronts[:-1], rank


def crowding_distance(objs, front):
    dist = {i: 0.0 for i in front}
    if len(front) <= 2:
        for i in front:
            dist[i] = float("inf")
        return dist
    m = len(objs[front[0]])
    for k in range(m):
        srt = sorted(front, key=lambda i: objs[i][k])
        lo, hi = objs[srt[0]][k], objs[srt[-1]][k]
        dist[srt[0]] = dist[srt[-1]] = float("inf")
        if hi - lo <= 0:
            continue
        for a in range(1, len(srt) - 1):
            dist[srt[a]] += (objs[srt[a + 1]][k] - objs[srt[a - 1]][k]) / (hi - lo)
    return dist


def nsga2(evaluate, bounds, pop_size=100, generations=150, eta_c=15.0, eta_m=20.0,
          p_c=0.9, seed=0):
    """Minimise a vector objective over a box. Returns final population and objectives."""
    rng = random.Random(seed)
    d = len(bounds)
    p_m = 1.0 / d

    def clip(v, j):
        return min(max(v, bounds[j][0]), bounds[j][1])

    pop = [[rng.uniform(lo, hi) for lo, hi in bounds] for _ in range(pop_size)]
    objs = [evaluate(x) for x in pop]

    def tournament(rank, crowd):
        a, b = rng.randrange(len(pop)), rng.randrange(len(pop))
        if rank[a] != rank[b]:
            return a if rank[a] < rank[b] else b
        return a if crowd[a] >= crowd[b] else b

    for _ in range(generations):
        fronts, rank = fast_nondominated_sort(objs)
        crowd = {}
        for f in fronts:
            crowd.update(crowding_distance(objs, f))
        children = []
        while len(children) < pop_size:
            p1 = pop[tournament(rank, crowd)]
            p2 = pop[tournament(rank, crowd)]
            c1, c2 = list(p1), list(p2)
            if rng.random() < p_c:
                for j in range(d):
                    if rng.random() <= 0.5 and abs(p1[j] - p2[j]) > 1e-14:
                        u = rng.random()
                        beta = (2 * u) ** (1 / (eta_c + 1)) if u <= 0.5 else \
                            (1 / (2 * (1 - u))) ** (1 / (eta_c + 1))
                        c1[j] = clip(0.5 * ((1 + beta) * p1[j] + (1 - beta) * p2[j]), j)
                        c2[j] = clip(0.5 * ((1 - beta) * p1[j] + (1 + beta) * p2[j]), j)
            for c in (c1, c2):
                for j in range(d):
                    if rng.random() < p_m:
                        lo, hi = bounds[j]
                        u = rng.random()
                        if u < 0.5:
                            delta = (2 * u) ** (1 / (eta_m + 1)) - 1
                        else:
                            delta = 1 - (2 * (1 - u)) ** (1 / (eta_m + 1))
                        c[j] = clip(c[j] + delta * (hi - lo), j)
                children.append(c)
        children = children[:pop_size]
        cobjs = [evaluate(x) for x in children]
        allp, allo = pop + children, objs + cobjs
        fronts, _ = fast_nondominated_sort(allo)
        new_idx = []
        for f in fronts:
            if len(new_idx) + len(f) <= pop_size:
                new_idx += f
            else:
                cd = crowding_distance(allo, f)
                rest = sorted(f, key=lambda i: -cd[i])
                new_idx += rest[:pop_size - len(new_idx)]
                break
        pop = [allp[i] for i in new_idx]
        objs = [allo[i] for i in new_idx]
    return pop, objs


def hypervolume_2d(points, ref):
    """Exact hypervolume of a 2-D point set (minimisation) w.r.t. a reference point."""
    pts = [p for p in points if p[0] < ref[0] and p[1] < ref[1]]
    if not pts:
        return 0.0
    pts = sorted(pts)
    hv, best_b = 0.0, ref[1]
    for a, b in pts:
        if b < best_b:
            hv += (ref[0] - a) * (best_b - b)
            best_b = b
    return hv


def hv_improvement(front, ref, y, base_hv=None):
    if y[0] >= ref[0] or y[1] >= ref[1]:
        return 0.0
    for p in front:
        if p[0] <= y[0] and p[1] <= y[1]:
            return 0.0
    if base_hv is None:
        base_hv = hypervolume_2d(front, ref)
    return hypervolume_2d(list(front) + [y], ref) - base_hv


# ----------------------------------------------------------------------------
# Grey relational analysis, TOPSIS and objective weighting
# ----------------------------------------------------------------------------

def gra(benefit, cost, zeta=0.5):
    """Grey relational coefficients and grades for one benefit and one cost criterion."""
    bmin, bmax = min(benefit), max(benefit)
    cmin, cmax = min(cost), max(cost)
    nb = [(v - bmin) / (bmax - bmin) for v in benefit]
    nc = [(cmax - v) / (cmax - cmin) for v in cost]
    deltas = [[1.0 - a, 1.0 - b] for a, b in zip(nb, nc)]
    dmin = min(min(d) for d in deltas)
    dmax = max(max(d) for d in deltas)
    grc = [[(dmin + zeta * dmax) / (d + zeta * dmax) for d in row] for row in deltas]
    grg = [sum(r) / len(r) for r in grc]
    return nb, nc, grc, grg


def entropy_weights(matrix):
    """Shannon-entropy weights of the columns of a positive decision matrix."""
    m, n = len(matrix), len(matrix[0])
    w = []
    for j in range(n):
        col = [row[j] for row in matrix]
        s = sum(col)
        e = 0.0
        for v in col:
            p = v / s
            if p > 0:
                e -= p * math.log(p)
        e /= math.log(m)
        w.append(1.0 - e)
    tot = sum(w)
    return [v / tot for v in w]


def critic_weights(matrix, benefit_flags):
    m, n = len(matrix), len(matrix[0])
    norm = []
    for j in range(n):
        col = [row[j] for row in matrix]
        lo, hi = min(col), max(col)
        if benefit_flags[j]:
            norm.append([(v - lo) / (hi - lo) for v in col])
        else:
            norm.append([(hi - v) / (hi - lo) for v in col])
    sds = []
    for col in norm:
        mu = sum(col) / m
        sds.append(math.sqrt(sum((v - mu) ** 2 for v in col) / (m - 1)))

    def corr(a, b):
        ma, mb = sum(a) / m, sum(b) / m
        sab = sum((x - ma) * (y - mb) for x, y in zip(a, b))
        return sab / math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))

    c = []
    for j in range(n):
        c.append(sds[j] * sum(1.0 - corr(norm[j], norm[k]) for k in range(n)))
    tot = sum(c)
    return [v / tot for v in c]


def topsis(matrix, weights, benefit_flags):
    m, n = len(matrix), len(matrix[0])
    norms = [math.sqrt(sum(row[j] ** 2 for row in matrix)) for j in range(n)]
    v = [[weights[j] * row[j] / norms[j] for j in range(n)] for row in matrix]
    best = [max(r[j] for r in v) if benefit_flags[j] else min(r[j] for r in v) for j in range(n)]
    worst = [min(r[j] for r in v) if benefit_flags[j] else max(r[j] for r in v) for j in range(n)]
    cc = []
    for r in v:
        dp = math.sqrt(sum((r[j] - best[j]) ** 2 for j in range(n)))
        dm = math.sqrt(sum((r[j] - worst[j]) ** 2 for j in range(n)))
        cc.append(dm / (dp + dm) if dp + dm > 0 else 0.0)
    return cc
