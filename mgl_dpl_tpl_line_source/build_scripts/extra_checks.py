"""Additional checks: heat-content identity, wave attenuation coefficient, front arrival, time-profile inversion."""
import json
import math
import os

import mgl
import model as M
from model import Model
from compute_all import MODELS, mk

HERE = os.path.dirname(os.path.abspath(__file__))
out = {}

# (a) global heat-content identity  int theta dA = Q0 L^-1[ F(s)/(s Phi(s)) ]
rs = [10 ** (-4 + 0.07 * i) for i in range(0, 58)]     # 1e-4 .. ~1.0 (log grid)
rs = [r for r in rs if r <= 1.6]
hc = {}
for k in ("Fourier", "MGL-LS", "MGL-DPL2", "MGL-TPL"):
    m = mk(**MODELS[k])
    t = 0.06
    v = M.invert_line(m, ("step",), rs, t, N=3000, nwynn=12)
    th = [row[0] for row in v]
    # integrate theta 2 pi r^2 dln r (trapezoid in ln r) + analytic inner part -(1/2pi) ln r * 2 pi r dr
    I = 0.0
    for i in range(len(rs) - 1):
        f0 = th[i] * rs[i] ** 2
        f1 = th[i + 1] * rs[i + 1] ** 2
        I += 0.5 * (f0 + f1) * (math.log(rs[i + 1]) - math.log(rs[i]))
    I *= 2 * math.pi
    # inner disc r < rs[0]: theta ~ th0 - (1/(2pi Psi...)) ln(r/r0) ; use leading log
    r0 = rs[0]
    inner = 2 * math.pi * th[0] * r0 ** 2 / 2
    I += inner
    # exact: L^-1 of 1/(s^2 Phi(s)) by Durbin
    ex = mgl.durbin(lambda s: [(1.0 / (s * s * m.Phi(s)),)], t, 1, 1, N=3000, nwynn=12)[0][0][0]
    hc[k] = dict(numeric=I, exact=ex, rel=abs(I - ex) / abs(ex))
out["heat_content"] = hc

# (b) wave attenuation beta: Re(m1 - s/c) at large real s versus closed form
EPS = M.EPS
bt = {}
for k in ("MGL-LS", "MGL-DPL2", "MGL-TPL"):
    kw = MODELS[k]
    m = mk(**kw)
    tq, tT, t1 = kw["tq"], kw.get("tT", 0.0), 0.05
    if k == "MGL-LS":
        c = 1.0 / math.sqrt((1 + EPS) * tq)
        # B = s^2/p + (1+eps) s (1 + tq s):  a = (1+eps) tq ; b = (1+eps) + 1/t1 - 1/((1+eps) t1) * ... derived numerically
        beta_cf = None
    else:
        c = math.sqrt(2 * tT / (1 + EPS)) / tq
        beta_cf = (1 / (2 * c)) * (2 / tq - 1 / tT) + c * EPS / (2 * (1 + EPS) * t1)
    s = 1e7
    m1 = m.roots(complex(s))[0]
    bt[k] = dict(c=c, beta_num=(m1.real - s / c), beta_cf=beta_cf)
out["beta"] = bt

# (c) closed form check of LS attenuation:  B = s^2/p + (1+eps) s (1+tq s)
tq, t1 = 0.02, 0.05
a = (1 + EPS) * tq
b = ((1 + EPS) + 1.0 / t1) - 1.0 / ((1 + EPS) * t1)  # x1 = B - C/B ; C/B -> s/((1+eps) t1) ... first order
c = 1 / math.sqrt(a)
out["beta_LS_cf"] = b / (2 * math.sqrt(a))

# (d) inversion test of the pulse-profile transforms
tests = {}
for prof in (("step",), ("rect", 0.04), ("exp", 0.05), ("gamma", 0.03), ("sin2", 0.08)):
    err = 0.0
    for t in (0.01, 0.03, 0.05, 0.08, 0.12, 0.2):
        if prof[0] == "rect" and abs(t - prof[1]) < 1e-9:
            continue
        v = mgl.durbin(lambda s: [(M.Fbar(prof, s),)], t, 1, 1, N=3000, nwynn=12)[0][0][0]
        ex = M.ftime(prof, t)
        err = max(err, abs(v - ex))
    tests["_".join(str(x) for x in prof)] = err
out["profile_inversion"] = tests
json.dump(out, open(os.path.join(HERE, "extra.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
