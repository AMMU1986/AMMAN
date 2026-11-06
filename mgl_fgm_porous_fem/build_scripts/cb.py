# -*- coding: utf-8 -*-
import json, math, os
import mgl
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))
CS = R["cases"]
CONST = mgl.constants()
EPS = CONST["eps"]
TCMP = [round(0.05 + 0.025 * k, 4) for k in range(11)]
B = []
_c = {"eq": 0, "fig": 0, "tab": 0}


def add(b): B.append(b)
def P(t): B.append(("p", t))
def H1(t): B.append(("h1", t))
def H2(t): B.append(("h2", t))


LAB = {}


def EQ(latex, label=None):
    _c["eq"] += 1
    B.append(("eq", latex, _c["eq"]))
    if label:
        LAB[label] = _c["eq"]


def resolve():
    import re
    for i, b in enumerate(B):
        if b[0] in ("p", "abstract"):
            B[i] = (b[0], re.sub(r"@(\w+)@", lambda m: str(LAB[m.group(1)]), b[1]))
        elif b[0] == "table":
            B[i] = (b[0], re.sub(r"@(\w+)@", lambda m: str(LAB[m.group(1)]), b[1])) + tuple(b[2:])
        elif b[0] == "fig":
            B[i] = (b[0], b[1], re.sub(r"@(\w+)@", lambda m: str(LAB[m.group(1)]), b[2]))


def FIG(fname, cap):
    _c["fig"] += 1
    B.append(("fig", fname, "Figure %d. %s" % (_c["fig"], cap)))


def TAB(cap, rows, widths):
    _c["tab"] += 1
    B.append(("table", "Table %d. %s" % (_c["tab"], cap), rows, widths))


def g(x, n=3): return ("%." + str(n) + "g") % x


def fx(x, n=3): return ("%." + str(n) + "f") % x


def e10(x, n=2):
    m, e = ("%." + str(n) + "e") % x
    return x


def sc(x, n=2):
    """x in scientific form with Unicode superscript-free notation: 1.23e-4 -> 1.23×10^{-4} as math"""
    s = ("%." + str(n) + "e") % x
    m, e = s.split("e")
    return "$%s\\times10^{%d}$" % (m, int(e))


def at(case, k, j, t):
    """value of field j at obs k, time t (grid 0.0025)"""
    return CS[case]["hist"][k][int(round(t / 0.0025))][j]


def arrival(case, k=0, thr=0.005):
    t = CS[case]["t"]
    for tt, h in zip(t, CS[case]["hist"][k]):
        if h[0] > thr:
            return tt
    return float("nan")


def peak_abs(case, k, j, t0=0.0, t1=0.3):
    best = (0, 0)
    for tt, h in zip(CS[case]["t"], CS[case]["hist"][k]):
        if t0 <= tt <= t1 and abs(h[j]) > abs(best[0]):
            best = (h[j], tt)
    return best
