# -*- coding: utf-8 -*-
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))
VF = json.load(open(os.path.join(HERE, "valfig.json")))
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



def pct(x, n=2):
    v = 100 * x
    if v < 0.01:
        m, e = ("%.1e" % v).split("e")
        return "$%s\\times10^{%d}$" % (m, int(e))
    return ("%." + str(n) + "g") % v
