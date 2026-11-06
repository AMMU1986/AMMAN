import json, math, model, lap, fem
base = dict(h=0.2, tau0=0.1, tau1=0.05)
out = {}
pts = [round(0.05 * k, 3) for k in range(1, 20)]
cth = 1 / math.sqrt(0.1)
def fronts(t):
    th_h = 0.2 / cth
    c2 = math.sqrt(0.8252 / (0.8823 * 0.1))
    xt = 0.2 + c2 * (t - th_h) if t > th_h else cth * t
    if xt > 1: xt = 1 - (xt - 1)
    xe = t if t < 0.2 else 0.2 + 2.352 * (t - 0.2)
    return [xt, xe]
rel = lambda a, b: math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)) / max(1e-300, sum(y * y for y in b)))
p = model.make(alpha=1.0, **base)
R = fem.run(p, dx=0.0025, dt=0.0025, T=0.4)
for t in (0.1, 0.2, 0.4):
    n = int(round(t / R.dt))
    ref, _, _ = lap.invert(p, pts, t, N=3000, nwynn=40)
    refm, _, _ = lap.invert(p, [x + 0.00125 for x in pts], t, N=3000, nwynn=40)
    xm, sg = fem.stress(R, n)
    fr = fronts(t)
    keep = [i for i, x in enumerate(pts) if all(abs(x - f) > 0.08 for f in fr)]
    mid = lambda x: min(range(len(xm)), key=lambda k: abs(xm[k] - x))
    e = dict(n=len(keep), fronts=fr)
    e["th"] = rel([fem.at(R, n, pts[i], "th") for i in keep], [ref[i][0] for i in keep])
    e["u"] = rel([fem.at(R, n, pts[i], "u") for i in keep], [ref[i][1] for i in keep])
    e["sg"] = rel([sg[mid(pts[i] + 0.00125)] for i in keep], [refm[i][2] for i in keep])
    out["masked_t%g" % t] = e
# Laplace self-consistency: vary Durbin parameters
for al in (1.0, 0.6):
    p = model.make(alpha=al, **base)
    d = 0
    for t in (0.1, 0.3, 0.5):
        a, _, _ = lap.invert(p, pts, t, N=3000, nwynn=40)
        b, _, _ = lap.invert(p, pts, t, N=4000, nwynn=60, ct=8.0, Tfac=3.0)
        d = max(d, max(abs(x[k] - y[k]) / (abs(x[k]) + 1e-3) for x, y in zip(a, b) for k in range(3)))
    out["lap_param_a%g" % al] = d
json.dump(out, open("extra.json", "w"))
print(out)
