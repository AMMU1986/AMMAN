#!/usr/bin/env python3
"""Supplementary analyses: decision-weight sensitivity and learning curves.

Writes pmedm_ml_results/results_extra.json. Run after analysis.py.
"""

import json
import math
import os
import random
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from core import mean, spearman  # noqa: E402
from data import load_runs  # noqa: E402
from decision import gra, topsis  # noqa: E402
from models import GPR, LinearModel, powerlaw_features, taguchi_features  # noqa: E402

ROWS = load_runs()
XS = [r["x"] for r in ROWS]
Y = {k: [r[k] for r in ROWS] for k in ("mrr", "twr")}
Z = {k: [math.log(v) for v in Y[k]] for k in Y}
N = len(ROWS)
OUT = os.path.join(os.path.dirname(HERE), "pmedm_ml_results", "results_extra.json")


def weight_sensitivity():
    mat = [[a, b] for a, b in zip(Y["mrr"], Y["twr"])]
    flags = [True, False]
    sweep = []
    for k in range(0, 101):
        w = k / 100.0
        cc = topsis(mat, [w, 1 - w], flags)
        best = max(range(N), key=lambda i: cc[i])
        # weighted grey relational grade with the same weights
        _, _, grc, _ = gra(Y["mrr"], Y["twr"])
        g = [w * a + (1 - w) * b for a, b in grc]
        best_g = max(range(N), key=lambda i: g[i])
        sweep.append({"w_mrr": w, "topsis_best": ROWS[best]["run"], "gra_best": ROWS[best_g]["run"]})
    zeta = []
    _, _, _, base = gra(Y["mrr"], Y["twr"], 0.5)
    for z10 in range(1, 10):
        z = z10 / 10.0
        _, _, _, g = gra(Y["mrr"], Y["twr"], z)
        order = sorted(range(N), key=lambda i: -g[i])
        zeta.append({"zeta": z, "best": ROWS[order[0]]["run"], "second": ROWS[order[1]]["run"],
                     "spearman_vs_0.5": spearman(g, base)})

    def ranges(key):
        out, cur = [], None
        for s in sweep:
            if cur is None or s[key] != cur["run"]:
                cur = {"run": s[key], "from": s["w_mrr"], "to": s["w_mrr"]}
                out.append(cur)
            else:
                cur["to"] = s["w_mrr"]
        return out

    return {"topsis_winner_ranges": ranges("topsis_best"), "gra_winner_ranges": ranges("gra_best"),
            "zeta": zeta}


SIZES = (9, 12, 15, 18, 21, 24)
N_SPLITS = 100


def lc_task(task):
    key, resp, n_train, s = task
    rng = random.Random(7000 + 97 * n_train + s)
    idx = list(range(N))
    rng.shuffle(idx)
    tr, te = idx[:n_train], idx[n_train:]
    xs, z = [XS[i] for i in tr], [Z[resp][i] for i in tr]
    if key == "powerlaw":
        m = LinearModel("pl", powerlaw_features).fit(xs, z)
    elif key == "taguchi":
        m = LinearModel("tme", taguchi_features).fit(xs, z)
    elif key == "gpr":
        m = GPR(seed=s, n_starts=3).fit(xs, z)
    else:
        m = None
    zbar = mean(z)
    if m is None:
        pred = [zbar] * len(te)
    else:
        pred = [d[1] for d in m.predict([XS[i] for i in te])]
    sse = sum((Z[resp][i] - p) ** 2 for i, p in zip(te, pred))
    sst = sum((Z[resp][i] - zbar) ** 2 for i in te)
    return key, resp, n_train, sse, sst


def learning_curves():
    tasks = []
    for key in ("mean", "taguchi", "powerlaw", "gpr"):
        for resp in ("mrr", "twr"):
            for n in SIZES:
                if key == "taguchi" and n < 12:
                    continue
                for s in range(N_SPLITS):
                    tasks.append((key, resp, n, s))
    with Pool(8) as pool:
        res = pool.map(lc_task, tasks, chunksize=4)
    out = {}
    for key, resp, n, sse, sst in res:
        d = out.setdefault(key, {}).setdefault(resp, {}).setdefault(str(n), [0.0, 0.0])
        d[0] += sse
        d[1] += sst
    return {k: {r: {n: 1 - v[0] / v[1] for n, v in d2.items()} for r, d2 in d1.items()}
            for k, d1 in out.items()}


def main():
    res = {"weights": weight_sensitivity(), "learning_curves": learning_curves(),
           "sizes": SIZES, "n_splits": N_SPLITS}
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res["weights"], indent=1))
    print(json.dumps(res["learning_curves"], indent=1))


if __name__ == "__main__":
    main()
