"""Independent steady-state solver (finite volume + Picard) for  (kappa(1+chi th) th')' = a6 omega(th) th,
th(0)=theta0, th(1)=0, flux and value continuous at x=h.  Used to validate the nonlinear FE at large t."""
import model


def steady(p, n=2000, tol=1e-13):
    h = p["h"]
    L = p["layers"]
    xs = [i / n for i in range(n + 1)]
    # make h a node
    n1 = int(round(h * n)); xs = [h * i / n1 for i in range(n1 + 1)] + [h + (1 - h) * i / (n - n1) for i in range(1, n - n1 + 1)]
    N = len(xs)
    th = [p["theta0"] * (1 - x) for x in xs]
    for it in range(200):
        a = [0.0] * N; b = [0.0] * N; c = [0.0] * N; r = [0.0] * N
        b[0] = 1.0; r[0] = p["theta0"]; b[-1] = 1.0; r[-1] = 0.0
        # face conductivities
        def kface(i):  # between node i and i+1, layer index of element i
            k = 0 if i < n1 else 1
            tm = 0.5 * (th[i] + th[i + 1])
            return L[k]["kappa"] * (1 + p["chi"][k] * tm)
        for i in range(1, N - 1):
            hl, hr = xs[i] - xs[i - 1], xs[i + 1] - xs[i]
            kl, kr = kface(i - 1), kface(i)
            vol = 0.5 * (hl + hr)
            # perfusion source: layer of the control volume (split at interface node)
            src = 0.0
            for (lo, hi, k) in ((xs[i] - hl / 2, xs[i], 0 if i - 1 < n1 else 1), (xs[i], xs[i] + hr / 2, 0 if i < n1 else 1)):
                om = model.omega(th[i], p["cw"][k], p["thc"][k], p["dth"]) if p["cw"][k] else 1.0
                src += L[k]["a6"] * om * (hi - lo)
            a[i] = kl / hl; c[i] = kr / hr; b[i] = -(kl / hl + kr / hr) - src
        # Thomas
        for i in range(1, N):
            m = a[i] / b[i - 1]
            b[i] -= m * c[i - 1]; r[i] -= m * r[i - 1]
        new = [0.0] * N
        new[-1] = r[-1] / b[-1]
        for i in range(N - 2, -1, -1):
            new[i] = (r[i] - c[i] * new[i + 1]) / b[i]
        d = max(abs(x - y) for x, y in zip(new, th))
        th = new
        if d < tol:
            break
    return xs, th, it
