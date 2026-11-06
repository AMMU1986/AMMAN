"""Independent explicit finite-difference solver for the axisymmetric (plane-strain) MGL
problem with LS-type (first-order tau_0) heat conduction and a uniform heated disc of radius rc
that mimics the line source.  It does not use Laplace transforms, Bessel functions or the
displacement potential; it integrates (u_tt = p(e_r - d1 theta_r), Lap theta + Q = (1 + tau0 d/dt)
d/dt(theta + d2 e)) directly on a staggered grid (theta at nodes, u at half nodes).
Also contains the Laplace comparator for the disc source (each K0 mode times 2 I1(m rc)/(m rc))."""
import cmath
import math

import mgl
from mgl import D1, D2, LAMBDA1
import model as M


def ftime_pulse(prof, t):
    return M.ftime(prof, t)


def fd_line(model, prof, t_end, rc=0.02, dr=0.002, rmax=1.2, cfl=0.2):
    tau0, tau1 = model.tq, model.t1
    n_nodes = int(round(rmax / dr))
    rn = [i * dr for i in range(n_nodes + 1)]
    # node volumes (per radian x 1/2): V_i = (r_{i+1/2}^2 - r_{i-1/2}^2)/2
    vol = [((rn[i] + 0.5 * dr) ** 2 - max(rn[i] - 0.5 * dr, 0.0) ** 2) / 2.0 for i in range(n_nodes + 1)]
    J = int(round(rc / dr))
    area = 2.0 * math.pi * sum(vol[: J + 1])
    qsrc = [1.0 / area if i <= J else 0.0 for i in range(n_nodes + 1)]
    rc_eff = math.sqrt(area / math.pi)
    dt = min(cfl * dr * dr / max(tau1, 1e-9), 0.2 * dr / 8.0)
    nsteps = int(math.ceil(t_end / dt))
    dt = t_end / nsteps
    Mh = n_nodes                      # half nodes r_{i+1/2}, i = 0..M-1
    u = [0.0] * Mh
    v = [0.0] * Mh
    th = [0.0] * (n_nodes + 1)
    w = [0.0] * (n_nodes + 1)

    def div(x):
        out = [0.0] * (n_nodes + 1)
        out[0] = 4.0 * x[0] / dr
        for i in range(1, n_nodes):
            out[i] = (x[i] - x[i - 1]) / dr + 0.5 * (x[i] + x[i - 1]) / rn[i]
        out[n_nodes] = 0.0
        return out

    t = 0.0
    for _ in range(nsteps):
        e = div(u)
        et = div(v)
        q = [e[i] - D1 * th[i] + tau1 * (et[i] - D1 * w[i]) for i in range(n_nodes + 1)]
        acc = [(q[i + 1] - q[i]) / dr for i in range(Mh)]
        acc[-1] = 0.0
        ett = div(acc)
        fs = ftime_pulse(prof, t + 0.5 * dt)
        for i in range(Mh - 1):
            v[i] += dt * acc[i]
            u[i] += dt * v[i]
        for i in range(1, n_nodes):
            lap = (th[i + 1] - 2 * th[i] + th[i - 1]) / (dr * dr) + 0.5 * (th[i + 1] - th[i - 1]) / (dr * rn[i])
            w[i] += dt / tau0 * (lap + qsrc[i] * fs - w[i] - D2 * et[i] - D2 * tau0 * ett[i])
        lap0 = 4.0 * (th[1] - th[0]) / (dr * dr)
        w[0] += dt / tau0 * (lap0 + qsrc[0] * fs - w[0] - D2 * et[0] - D2 * tau0 * ett[0])
        for i in range(n_nodes):
            th[i] += dt * w[i]
        t += dt
    # hoop and radial stresses at nodes
    un = [0.0] + [0.5 * (u[i] + u[i - 1]) for i in range(1, n_nodes)] + [0.0]
    vn = [0.0] + [0.5 * (v[i] + v[i - 1]) for i in range(1, n_nodes)] + [0.0]
    srr, spp = [0.0] * (n_nodes + 1), [0.0] * (n_nodes + 1)
    for i in range(1, n_nodes):
        ur, vr = (u[i] - u[i - 1]) / dr, (v[i] - v[i - 1]) / dr
        r = rn[i]
        srr[i] = ur + LAMBDA1 * un[i] / r - D1 * th[i] + tau1 * (vr + LAMBDA1 * vn[i] / r - D1 * w[i])
        spp[i] = un[i] / r + LAMBDA1 * ur - D1 * th[i] + tau1 * (vn[i] / r + LAMBDA1 * vr - D1 * w[i])
    return rn, th, un, srr, spp, rc_eff, dt, nsteps


# ---------------- Laplace comparator for a uniform disc source ------------------
def i1_scaled(z):
    """e^{-z} I1(z) = (1/pi) int_0^pi e^{z(cos x - 1)} cos x dx (periodic trapezoid, spectrally accurate)."""
    n = int(abs(z)) + 40
    h = math.pi / n
    s = 0.5 * (1.0 + (cmath.exp(-2.0 * z)) * (-1.0))
    for k in range(1, n):
        c = math.cos(k * h)
        s += cmath.exp(z * (c - 1.0)) * c
    return s * h / math.pi


def disc_fields(model, s, rs, prof, rc):
    (m1, m2), th, kp, pref = model.parts(s)
    G = pref * M.Fbar(prof, s) / (2.0 * math.pi)
    out = []
    dj = [2.0 * i1_scaled(m * rc) / (m * rc) for m in (m1, m2)]
    sg = (1.0, -1.0)
    for r in rs:
        phi = u = t = lap = 0j
        for m, thj, sj, d in zip((m1, m2), th, sg, dj):
            k0, k1 = mgl.kscaled(m * r)
            e = cmath.exp(-m * (r - rc))
            k0 *= e * d
            k1 *= e * d
            phi += sj * G * k0
            u += -sj * G * m * k1
            t += sj * G * thj * k0
            lap += sj * G * m * m * k0
        srr = s * s * phi - kp * u / r
        spp = s * s * phi + kp * (u / r - lap)
        out.append((t, u, srr, spp))
    return out


def invert_disc(model, prof, rs, t, rc, N=3000, nwynn=12):
    if prof[0] == "rect":
        a = invert_disc(model, ("step",), rs, t, rc, N, nwynn)
        if t > prof[1]:
            b = invert_disc(model, ("step",), rs, t - prof[1], rc, N, nwynn)
            return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]
        return a
    f = lambda s: disc_fields(model, s, rs, prof, rc)
    res = mgl.durbin(f, t, 4, len(rs), N=N, nwynn=nwynn)
    return res[0]
