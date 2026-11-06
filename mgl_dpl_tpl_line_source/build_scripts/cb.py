# -*- coding: utf-8 -*-
"""Content-block helpers and computed numbers shared by the section files."""
import json
import math
import os

import mgl

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))
X = json.load(open(os.path.join(HERE, "extra.json")))
C = mgl.constants()
EPS = C["eps"]
B = []
_eq = [0]
_fig = [0]
_tab = [0]


def add(b):
    B.append(b)


def P(t):
    B.append(("p", t))


def H1(t):
    B.append(("h1", t))


def H2(t):
    B.append(("h2", t))


def EQ(latex):
    _eq[0] += 1
    B.append(("eq", latex, _eq[0]))
    return _eq[0]


def FIG(fname, cap):
    _fig[0] += 1
    B.append(("fig", fname, "Figure %d. %s" % (_fig[0], cap)))


def TAB(cap, rows, widths):
    _tab[0] += 1
    B.append(("table", "Table %d. %s" % (_tab[0], cap), rows, widths))


def g(x, n=3):
    return ("%." + str(n) + "g") % x


def sci(x, n=2):
    m, e = ("%." + str(n) + "e") % x
    return x


def e10(x, n=1):
    s = ("%." + str(n) + "e") % x
    m, e = s.split("e")
    return "%s×10^{%d}" % (m, int(e))


TS, RS = R["ts"], R["rs"]


def hist(key, j):
    return [row[j] for row in R[key]]


def peak(key, j, sign=1):
    v = hist(key, j)
    i = max(range(len(v)), key=lambda k: sign * v[k])
    return v[i], TS[i]


def arrival(key, thr=1e-4):
    v = hist(key, 0)
    for t, x in zip(TS, v):
        if abs(x) > thr:
            return t
    return float("nan")


def prof_at(key, r, j):
    return R[key][RS.index(round(r, 3))][j]
