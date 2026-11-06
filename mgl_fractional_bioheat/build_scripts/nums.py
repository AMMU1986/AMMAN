# -*- coding: utf-8 -*-
from cb import *
from tables import T1, T2, T3, T4, T5, EX, L as LAY, A7, SC, LS, sc, g, pct
import model, math
V = R["valid"]; C = R["conv"]; LM = R["limits"]; S = R["studies"]; M = R["models"]; XG = R["xg_models"]
WR = model.wratio()
def f3(x): return "%.3f" % x
def f2(x): return "%.2f" % x
def f4(x): return "%.4f" % x
def hs(case, k=2): return S[case]["hist"][k]
def th_at(case, k, t): return hs(case, k)[int(round(t / 0.01))][0]
def u_at(case, k, t): return hs(case, k)[int(round(t / 0.01))][1]
def sig_at(case, k, t): return hs(case, k)[int(round(t / 0.01))][2]
def edge_peak(case):
    h = hs(case, 2); sg = [abs(x[2]) for x in h]; i = max(range(len(sg)), key=lambda j: sg[j]); return sg[i], S[case]["t"][i]
def mrow(name, t, x): return M[name]["snaps"][str(t)][XG.index(x)]
def snapth(case, t, x): return S[case]["snaps"][str(t)][int(round(x * 100))][0]
a1, a2 = LAY
cth1 = 1 / math.sqrt(0.1)
cth2 = math.sqrt(a2["kappa"] / (a2["C"] * 0.1))
ce2 = math.sqrt(a2["a8"] / a2["rho"])
th_arr = 0.2 / cth1
STEADY = LM["steady"]

def sc(x, n=2):
    s = ("%." + str(n) + "e") % x
    m, e = s.split("e")
    return "%s\\times10^{%d}" % (m, int(e))
def sct(x, n=2):
    return "$" + sc(x, n) + "$"
