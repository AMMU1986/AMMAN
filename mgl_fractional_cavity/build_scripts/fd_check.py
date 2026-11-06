"""n = 2: sphere, n = 1: cylinder (plane strain).
Independent explicit finite-difference solution of the alpha = 1 spherical
MGL problem (eqs 12-15 with eqs 7-10), used to validate the Laplace/Durbin
results. Staggered grid: theta at nodes r_i, u at half-nodes."""
import math
from mgl import D1, D2, LAMBDA1, KAPPA


def fd_sphere(a, tau0, tau1, t_end, dr=0.0005, rmax=0.16, dt=None, n=2):
    M = int(round((rmax - a) / dr))
    rn = [a + i * dr for i in range(M + 1)]          # nodes
    rh = [a + (i + 0.5) * dr for i in range(M)]       # half nodes r_{i+1/2}
    if dt is None:
        dt = min(0.2 * dr * dr / tau1, 0.1 * dr)
    nsteps = int(math.ceil(t_end / dt))
    dt = t_end / nsteps
    u = [0.0] * M
    v = [0.0] * M
    th = [0.0] * (M + 1)
    w = [0.0] * (M + 1)
    th[0] = 1.0
    l1 = LAMBDA1

    def ghost(x, bc):
        # (x0 - g)/dr + n l1 (x0 + g)/(2a) - bc = 0
        return (x[0] / dr + 0.5 * n * l1 * x[0] / a - bc) / (1.0 / dr - 0.5 * n * l1 / a)

    def div(x, g):
        out = [0.0] * (M + 1)
        out[0] = (x[0] - g) / dr + 0.5 * n * (x[0] + g) / rn[0]
        for i in range(1, M):
            out[i] = (x[i] - x[i - 1]) / dr + 0.5 * n * (x[i] + x[i - 1]) / rn[i]
        return out

    for _step in range(nsteps):
        gu = ghost(u, D1 * th[0])
        gv = ghost(v, 0.0)
        e = div(u, gu)
        et = div(v, gv)
        q = [e[i] - D1 * th[i] + tau1 * (et[i] - D1 * w[i]) for i in range(M + 1)]
        acc = [(q[i + 1] - q[i]) / dr for i in range(M)]
        acc[-1] = 0.0
        ga = ghost(acc, 0.0)
        ett = div(acc, ga)
        for i in range(M - 1):
            v[i] += dt * acc[i]
            u[i] += dt * v[i]
        for i in range(1, M):
            lap = (th[i + 1] - 2 * th[i] + th[i - 1]) / (dr * dr) + \
                0.5 * n * (th[i + 1] - th[i - 1]) / (dr * rn[i])
            w[i] += dt / tau0 * (lap - w[i] - D2 * et[i] - D2 * tau0 * ett[i])
        for i in range(1, M):
            th[i] += dt * w[i]
    gu = ghost(u, D1 * th[0])
    # stress brackets at nodes, u at nodes by averaging
    un = [0.5 * (gu + u[0])] + [0.5 * (u[i] + u[i - 1]) for i in range(1, M)] + [0.0]
    gv = ghost(v, 0.0)
    vn = [0.5 * (gv + v[0])] + [0.5 * (v[i] + v[i - 1]) for i in range(1, M)] + [0.0]
    srr, spp = [], []
    for i in range(M + 1):
        if i == 0:
            ur, vr = (u[0] - gu) / dr, (v[0] - gv) / dr
        elif i < M:
            ur, vr = (u[i] - u[i - 1]) / dr, (v[i] - v[i - 1]) / dr
        else:
            ur = vr = 0.0
        r = rn[i]
        srr.append(ur + n * l1 * un[i] / r - D1 * th[i] + tau1 * (vr + n * l1 * vn[i] / r - D1 * w[i]))
        h = 1 + (n - 1) * l1
        spp.append(h * un[i] / r + l1 * ur - D1 * th[i] +
                   tau1 * (h * vn[i] / r + l1 * vr - D1 * w[i]))
    return rn, th, un, srr, spp
