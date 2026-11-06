import json, model, lap, fem, math
base = dict(h=0.2, tau0=0.1, tau1=0.05)
out = {}
ts = [round(0.02 * k, 2) for k in range(1, 31)]
xo = [0.1, 0.3]
for al in (1.0, 0.6):
    p = model.make(alpha=al, **base)
    R = fem.run(p, dx=0.0025, dt=0.0025, T=0.6)
    d = dict(t=ts, lap=[], fem=[])
    for t in ts:
        n = int(round(t / R.dt))
        a, _, _ = lap.invert(p, xo + [x + 0.00125 for x in xo], t, N=3000, nwynn=40)
        d["lap"].append([[a[0][0], a[1][0]], [a[0][1], a[1][1]], [a[2][2], a[3][2]]])
        xm, sg = fem.stress(R, n)
        mid = lambda x: min(range(len(xm)), key=lambda k: abs(xm[k] - x))
        d["fem"].append([[fem.at(R, n, x, "th") for x in xo], [fem.at(R, n, x, "u") for x in xo], [sg[mid(x + 0.00125)] for x in xo]])
    out["a%g" % al] = d
json.dump(out, open("valfig.json", "w"))
