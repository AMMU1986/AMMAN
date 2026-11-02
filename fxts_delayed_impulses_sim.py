#!/usr/bin/env python3
"""
Numerical companion for the manuscript
"Fixed-time stability of Cohen-Grossberg BAM neural networks with delayed
destabilizing impulses".

Pure standard library (no numpy/matplotlib), consistent with the rest of this
repository. It
  * integrates the impulsive systems with fixed-step RK4 and exact handling of
    delayed impulses x(t_l^+) = G1 x(t_l) + G2 x(t_l - d_l),
  * evaluates every constant, sufficient condition and settling-time bound used
    in the paper (Theorems 1-3),
  * writes all numbers to fxts_figures/results.json, and
  * renders Figures 1-6 as PNG files with the PNGCanvas toolkit.

Usage:
    python3 fxts_delayed_impulses_sim.py
"""

import json
import math
import os
import random

from generate_figures import (
    PNGCanvas, BLACK, WHITE, GRAY, LIGHT_GRAY, DARK_BLUE, MED_BLUE,
    LIGHT_BLUE, PALE_BLUE, RED, LIGHT_RED, ORANGE, LIGHT_ORANGE, DARK_GREEN,
    MED_GREEN, LIGHT_GREEN, PURPLE, GOLD,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'fxts_figures')
H = 1e-3            # integration step
TOL = 1e-3          # settling tolerance on the 1-norm of the state


def sgnpow(v, e):
    """sign(v)|v|^e (also the odd-rational power p^(a/b) with a, b odd)."""
    if v == 0.0:
        return 0.0
    return math.copysign(abs(v) ** e, v)


# ---------------------------------------------------------------------------
# Impulse sequences
# ---------------------------------------------------------------------------

def impulse_sequence(tau_a, N0, theta, T):
    """Sequence (45) of Lu, Ho & Cao (2010): AII tau_a, elasticity N0,
    minimum inter-impulse interval theta."""
    ts, t, l = [], 0.0, 0
    while True:
        l += 1
        t += theta if l % N0 != 0 else N0 * (tau_a - theta) + theta
        if t > T:
            break
        ts.append(round(t, 6))
    return ts


# ---------------------------------------------------------------------------
# Generic RK4 integrator with delayed impulses
# ---------------------------------------------------------------------------

def simulate(rhs, x0, T, imp_times, d, G1, G2, h=H):
    """Integrate x' = rhs(x) with jumps x(t_l^+) = G1*x(t_l) + G2*x(t_l - d).

    G1, G2 are per-component gain lists. Returns (ts, xs)."""
    n = len(x0)
    steps = int(round(T / h))
    imp_idx = {int(round(t / h)) for t in imp_times}
    dk = int(round(d / h))
    x = list(x0)
    ts, xs = [0.0], [list(x)]
    for k in range(1, steps + 1):
        k1 = rhs(x)
        k2 = rhs([x[i] + 0.5 * h * k1[i] for i in range(n)])
        k3 = rhs([x[i] + 0.5 * h * k2[i] for i in range(n)])
        k4 = rhs([x[i] + h * k3[i] for i in range(n)])
        x = [x[i] + h / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
             for i in range(n)]
        if k in imp_idx:
            past = xs[k - dk] if dk > 0 else x
            x = [G1[i] * x[i] + G2[i] * past[i] for i in range(n)]
        ts.append(k * h)
        xs.append(list(x))
    return ts, xs


def norm1(v):
    return sum(abs(c) for c in v)


def settling_time(ts, xs, tol=TOL):
    """Last instant at which ||x||_1 exceeds tol (None if never settles)."""
    last = None
    for t, v in zip(ts, xs):
        if norm1(v) > tol:
            last = t
    if last is not None and last > ts[-1] - 1.0:
        return None
    return 0.0 if last is None else last


# ---------------------------------------------------------------------------
# Theorem 1: constants and settling-time bound
# ---------------------------------------------------------------------------

def theorem1(a, b, c, alpha, beta, xi, tau_a, N0, dbar):
    """Return a dict with all quantities of Theorem 1 (delayed impulses)."""
    tt = tau_a - dbar                       # effective AII
    out = {'tau_tilde': tt, 'threshold': dbar + math.log(xi) / c}
    if tt <= 0 or c - math.log(xi) / tt <= 0:
        out.update(feasible=False)
        return out
    Nt = (N0 * tau_a + dbar) / tt           # effective elasticity number
    k = c - math.log(xi) / tt
    U1 = math.log(1 + k / (b * xi ** (Nt * (1 - beta)))) / (k * (beta - 1))
    kp = c - math.log(xi) / tau_a           # kappa' (uses the lower AII bound)
    U2 = math.log(1 + kp * xi ** ((Nt + N0) * (1 - alpha)) / a) / \
        (k * (1 - alpha))
    Tmax = (U1 + U2) * tau_a / tt + dbar * Nt
    out.update(feasible=True, N0_tilde=Nt, kappa=k, kappa_p=kp, U1=U1, U2=U2,
               Tmax=Tmax)
    return out


def base_paper_bound(a, b, c, alpha, beta, xi, tau_a, N0):
    """Settling-time estimate of Theorem 1 in Jamal et al. (2023), no delay."""
    k = c - math.log(xi) / tau_a
    if k <= 0:
        return None
    T1 = math.log(1 + k / (b * xi ** (N0 * (1 - beta)))) / (k * (beta - 1))
    z = xi ** (-N0 * (1 - alpha))
    T2 = math.log(a * z / (xi ** (N0 * (1 - alpha)) * k + a * z)) / \
        ((-k) * (1 - alpha))
    return T1 + T2


def majorant(N0val, T, imp_times, d, a, b, c, alpha, beta, xi, hold=True,
             h=H):
    """Scalar comparison function of Lemma 3 (hold=True) or the naive
    delay-free comparison function (hold=False)."""
    steps = int(round(T / h))
    imp_idx = {int(round(t / h)) for t in imp_times}
    hold_idx = set()
    if hold:
        dk = int(round(d / h))
        for ki in imp_idx:
            hold_idx.update(range(ki - dk + 1, ki + 1))

    def g(N):
        if N <= 0:
            return 0.0
        return -a * N ** alpha - b * N ** beta - c * N

    N = N0val
    out = [N]
    for kk in range(1, steps + 1):
        if kk not in hold_idx and N > 0:
            k1 = g(N); k2 = g(max(N + 0.5 * h * k1, 0))
            k3 = g(max(N + 0.5 * h * k2, 0)); k4 = g(max(N + h * k3, 0))
            N = max(N + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4), 0.0)
        if kk in imp_idx:
            N = xi * N
        out.append(N)
    return out


# ---------------------------------------------------------------------------
# Example 1: two-dimensional cyber-physical system with deception attacks
# ---------------------------------------------------------------------------

EX1 = dict(a=0.4, b=0.8, c=0.1, alpha=0.5, beta=1.5,
           xi1=1.0, xi2=0.2, theta=0.5, N0=2, d=0.4)


def ex1_rhs(controlled=True):
    def f(x):
        u = [0.0, 0.0]
        if controlled:
            u = [-0.4 * sgnpow(x[i], 0.5) - 1.2 * sgnpow(x[i], 1.5)
                 - 0.2 * x[i] for i in range(2)]
        return [0.1 * math.sin(x[1]) + u[0], 0.1 * math.sin(x[0]) + u[1]]
    return f


# ---------------------------------------------------------------------------
# Example 2: Cohen-Grossberg BAM neural network (2 + 2 neurons)
# ---------------------------------------------------------------------------

Hm = [[-2.5, 0.5], [0.3, -1.5]]         # h_rs  (X-layer receives from Y)
Wm = [[-0.4, -1.3], [1.5, -0.4]]        # w_sr  (Y-layer receives from X)
a_lo, a_hi = [0.8, 0.6], [1.0, 0.9]     # bounds of a_r
c_lo, c_hi = [1.4, 0.74], [2.0, 1.34]   # bounds of c_s
bd, dd = [0.5, 0.74], [0.2, 0.3]        # b_r' and d_s' (linear)
A_l, B_l = [1.0, 1.0], [1.0, 1.0]       # Lipschitz constants


def ampl_a(r, x):
    return [0.8 + 0.2 / (1 + x * x), 0.6 + 0.3 / (1 + x * x)][r]


def ampl_c(s, y):
    return [1.4 + 0.6 / (1 + y * y), 0.74 + 0.6 / (1 + y * y)][s]


def fact(y):
    return 0.5 * (abs(y + 1) - abs(y - 1))


def gact(x):
    return 0.5 * math.tanh(x)


def bam_rhs(control):
    def f(z):
        x, y = z[:2], z[2:]
        dx, dy = [], []
        for r in range(2):
            s_in = sum(Hm[r][s] * fact(y[s]) for s in range(2))
            dx.append(-ampl_a(r, x[r]) * (bd[r] * x[r] - s_in)
                      + control('x', r, x[r]))
        for s in range(2):
            r_in = sum(Wm[s][r] * gact(x[r]) for r in range(2))
            dy.append(-ampl_c(s, y[s]) * (dd[s] * y[s] - r_in)
                      + control('y', s, y[s]))
        return dx + dy
    return f


C1 = dict(k=[4.0, 4.0], m=[3.0, 3.0], k1=1.25, m1=1.25, k2=4.0, m2=4.0,
          alpha=0.8, beta=1.8)
C2 = dict(Phi=[4.0, 4.0], Psi=[5.0, 4.0], k3=0.5, m3=0.5, k4=1.5, m4=1.5,
          a1=3, b1=7, a2=9, b2=5, eps=0.5, veps=0.5)
IMP2 = dict(rho1=1.05, rho2=0.15, om1=1.10, om2=0.15, theta=0.2, N0=2,
            d=0.1)


def controller1(par=C1):
    def u(layer, i, v):
        if layer == 'x':
            return (-par['k'][i] * v - par['k1'] * sgnpow(v, par['alpha'])
                    - par['k2'] * sgnpow(v, par['beta']))
        return (-par['m'][i] * v - par['m1'] * sgnpow(v, par['alpha'])
                - par['m2'] * sgnpow(v, par['beta']))
    return u


def controller2(par=C2, linear=True):
    e1 = par['a1'] / par['b1']
    e2 = par['a2'] / par['b2']

    def u(layer, i, v):
        if layer == 'x':
            lin = par['Phi'][i] * v if linear else 0.0
            return -lin - par['k3'] * sgnpow(v, e1) - par['k4'] * sgnpow(v, e2)
        lin = par['Psi'][i] * v if linear else 0.0
        return -lin - par['m3'] * sgnpow(v, e1) - par['m4'] * sgnpow(v, e2)
    return u


def no_control(layer, i, v):
    return 0.0


def thm2_constants(par=C1, imp=IMP2):
    """Gain thresholds and Lyapunov constants of Theorem 2 (L1 function)."""
    m = 4
    kthr = [B_l[r] * sum(c_hi[s] * abs(Wm[s][r]) for s in range(2))
            - a_lo[r] * bd[r] for r in range(2)]
    mthr = [A_l[s] * sum(a_hi[r] * abs(Hm[r][s]) for r in range(2))
            - c_lo[s] * dd[s] for s in range(2)]
    eta = [par['k'][r] - kthr[r] for r in range(2)]
    mu = [par['m'][s] - mthr[s] for s in range(2)]
    delta = min(eta + mu)
    phi = min(par['k1'], par['m1'])
    psi_t = min(par['k2'], par['m2']) * m ** (1 - par['beta'])
    xi1 = max(abs(imp['rho1']), abs(imp['om1']))
    xi2 = max(abs(imp['rho2']), abs(imp['om2']))
    return dict(kthr=kthr, mthr=mthr, eta=eta, mu=mu, delta=delta, phi=phi,
                psi_tilde=psi_t, xi1=xi1, xi2=xi2, xi=xi1 + xi2,
                alpha=par['alpha'], beta=par['beta'])


def thm3_constants(par=C2, imp=IMP2):
    """Gain thresholds and Lyapunov constants of Theorem 3 (quadratic)."""
    m = 4
    eps, veps = par['eps'], par['veps']
    Phithr = [sum(a_hi[r] * A_l[s] * abs(Hm[r][s]) / (2 * eps)
                  + c_hi[s] * B_l[r] * abs(Wm[s][r]) * veps / 2
                  for s in range(2)) - a_lo[r] * bd[r] for r in range(2)]
    Psithr = [sum(a_hi[r] * A_l[s] * abs(Hm[r][s]) * eps / 2
                  + c_hi[s] * B_l[r] * abs(Wm[s][r]) / (2 * veps)
                  for r in range(2)) - c_lo[s] * dd[s] for s in range(2)]
    gam = [par['Phi'][r] - Phithr[r] for r in range(2)]
    lam = [par['Psi'][s] - Psithr[s] for s in range(2)]
    Theta = min(gam + lam)
    ea = (par['a1'] + par['b1']) / (2 * par['b1'])
    eb = (par['a2'] + par['b2']) / (2 * par['b2'])
    chi = min(par['k3'], par['m3']) * 2 ** ea
    rho = min(par['k4'], par['m4']) * 2 ** eb * m ** (1 - eb)
    sx = abs(imp['rho1']) + abs(imp['rho2'])
    sy = abs(imp['om1']) + abs(imp['om2'])
    xi1 = max(sx * abs(imp['rho1']), sy * abs(imp['om1']))
    xi2 = max(sx * abs(imp['rho2']), sy * abs(imp['om2']))
    return dict(Phithr=Phithr, Psithr=Psithr, gamma=gam, lam=lam,
                Theta=Theta, Theta_tilde=2 * Theta, chi_tilde=chi,
                rho_tilde=rho, alpha=ea, beta=eb, xi1=xi1, xi2=xi2,
                xi=xi1 + xi2)


# ---------------------------------------------------------------------------
# Plotting helpers on top of PNGCanvas
# ---------------------------------------------------------------------------

def fmt(v):
    if v == 0:
        return '0'
    if abs(v) >= 100 or abs(v) < 0.01:
        e = int(math.floor(math.log10(abs(v))))
        m = v / 10 ** e
        return ('%g' % round(m, 2)) + 'e' + str(e)
    return ('%g' % round(v, 3))


def nice_ticks(lo, hi, n=5):
    span = hi - lo
    if span <= 0:
        return [lo]
    raw = span / n
    mag = 10 ** math.floor(math.log10(raw))
    step = min((s * mag for s in (1, 2, 2.5, 5, 10) if s * mag >= raw),
               default=10 * mag)
    start = math.ceil(lo / step) * step
    out, v = [], start
    while v <= hi + 1e-12:
        out.append(round(v, 10))
        v += step
    return out


class Axes:
    def __init__(self, cv, x0, y0, w, h, xlim, ylim, logy=False,
                 xlabel='', ylabel='', title=''):
        self.cv, self.x0, self.y0, self.w, self.h = cv, x0, y0, w, h
        self.xlim, self.logy = xlim, logy
        self.ylim = (math.log10(ylim[0]), math.log10(ylim[1])) if logy \
            else ylim
        cv.rect(x0, y0, x0 + w, y0 + h, BLACK)
        for tx in nice_ticks(*xlim):
            px = self.px(tx)
            cv.vline(px, y0 + h, y0 + h + 4, BLACK)
            cv.vline(px, y0 + 1, y0 + h - 1, (238, 238, 238))
            cv.text_c(px, y0 + h + 8, fmt(tx), BLACK)
        if logy:
            for e in range(int(math.ceil(self.ylim[0])),
                           int(math.floor(self.ylim[1])) + 1):
                py = self.py(10 ** e)
                cv.hline(x0 - 4, x0, py, BLACK)
                cv.hline(x0 + 1, x0 + w - 1, py, (238, 238, 238))
                lab = '1e' + str(e)
                cv.text(x0 - 8 - 6 * len(lab), py - 3, lab, BLACK)
        else:
            for ty in nice_ticks(*ylim):
                py = self.py(ty)
                cv.hline(x0 - 4, x0, py, BLACK)
                cv.hline(x0 + 1, x0 + w - 1, py, (238, 238, 238))
                lab = fmt(ty)
                cv.text(x0 - 8 - 6 * len(lab), py - 3, lab, BLACK)
        cv.rect(x0, y0, x0 + w, y0 + h, BLACK)
        cv.text_c(x0 + w // 2, y0 + h + 24, xlabel, BLACK)
        if ylabel:
            cv.text(x0 + 4, y0 - 14, ylabel, BLACK)
        if title:
            cv.text_c(x0 + w // 2, y0 - 30, title, BLACK, 2)

    def px(self, x):
        return int(self.x0 + (x - self.xlim[0]) /
                   (self.xlim[1] - self.xlim[0]) * self.w)

    def py(self, y):
        if self.logy:
            y = math.log10(max(y, 10 ** self.ylim[0]))
        y = min(max(y, self.ylim[0]), self.ylim[1])
        return int(self.y0 + self.h - (y - self.ylim[0]) /
                   (self.ylim[1] - self.ylim[0]) * self.h)

    def plot(self, xs, ys, color, thick=2, stride=1, dashed=False):
        prev = None
        cnt = 0
        for i in range(0, len(xs), stride):
            if xs[i] < self.xlim[0] or xs[i] > self.xlim[1]:
                prev = None
                continue
            p = (self.px(xs[i]), self.py(ys[i]))
            if prev is not None:
                cnt += 1
                if not dashed or (cnt // 6) % 2 == 0:
                    self.cv.line(prev[0], prev[1], p[0], p[1], color, thick)
            prev = p

    def vmark(self, x, color, label=''):
        px = self.px(x)
        for y in range(self.y0 + 1, self.y0 + self.h, 6):
            self.cv.vline(px, y, min(y + 3, self.y0 + self.h - 1), color)
            self.cv.vline(px + 1, y, min(y + 3, self.y0 + self.h - 1), color)
        if label:
            self.cv.text(px + 5, self.y0 + 8, label, color)

    def hmark(self, y, color):
        py = self.py(y)
        for x in range(self.x0 + 1, self.x0 + self.w, 6):
            self.cv.hline(x, min(x + 3, self.x0 + self.w - 1), py, color)

    def scatter(self, xs, ys, color, r=3):
        for x, y in zip(xs, ys):
            self.cv.circle(self.px(x), self.py(y), r, color, color)

    def legend(self, items, corner='ne'):
        wbox = 30 + 6 * max(len(t) for t, _ in items)
        hbox = 8 + 14 * len(items)
        x = self.x0 + self.w - wbox - 8 if 'e' in corner else self.x0 + 8
        y = self.y0 + 8 if 'n' in corner else self.y0 + self.h - hbox - 8
        self.cv.rect(x, y, x + wbox, y + hbox, GRAY, WHITE)
        for i, (t, col) in enumerate(items):
            yy = y + 8 + 14 * i
            self.cv.line(x + 6, yy + 3, x + 22, yy + 3, col, 3)
            self.cv.text(x + 26, yy, t, BLACK)


def panel_label(cv, x, y, s):
    cv.text(x, y, s, BLACK, 2)


COLS = [MED_BLUE, RED, DARK_GREEN, PURPLE]


# ---------------------------------------------------------------------------
# Experiments
# ---------------------------------------------------------------------------

def run_example1(res):
    p = EX1
    xi = p['xi1'] + p['xi2']
    tau_ok, tau_bad = 3.0, 0.06
    theta_bad, d_bad = 0.05, 0.04
    th = theorem1(p['a'], p['b'], p['c'], p['alpha'], p['beta'], xi,
                  tau_ok, p['N0'], p['d'])
    naive = theorem1(p['a'], p['b'], p['c'], p['alpha'], p['beta'], xi,
                     tau_ok, p['N0'], 0.0)
    res['ex1'] = dict(params=p, xi=xi, tau_ok=tau_ok, tau_bad=tau_bad,
                      thm1=th, naive_no_delay=naive,
                      base_paper_T=base_paper_bound(
                          p['a'], p['b'], p['c'], p['alpha'], p['beta'], xi,
                          tau_ok, p['N0']))
    G1, G2 = [p['xi1']] * 2, [p['xi2']] * 2
    x0 = [0.2, 0.1]

    # (a) uncontrolled, delayed impulses with tau_a = 3
    T_unc = 40.0
    imp = impulse_sequence(tau_ok, p['N0'], p['theta'], T_unc)
    ts_u, xs_u = simulate(ex1_rhs(False), x0, T_unc, imp, p['d'], G1, G2)
    # (b) controlled, tau_a = 3 (condition holds)
    T_c = 60.0
    imp_c = impulse_sequence(tau_ok, p['N0'], p['theta'], T_c)
    ts_c, xs_c = simulate(ex1_rhs(True), x0, T_c, imp_c, p['d'], G1, G2)
    Ts_c = settling_time(ts_c, xs_c)
    # (c) controlled, very frequent impulses (condition fails)
    x0b = [3.0, -2.5]
    imp_b = impulse_sequence(tau_bad, p['N0'], theta_bad, T_c)
    ts_b, xs_b = simulate(ex1_rhs(True), x0b, T_c, imp_b, d_bad, G1, G2)
    Ts_b = settling_time(ts_b, xs_b)
    res['ex1'].update(settle_ok=Ts_c, settle_bad=Ts_b,
                      theta_bad=theta_bad, d_bad=d_bad,
                      bad_threshold=theorem1(
                          p['a'], p['b'], p['c'], p['alpha'], p['beta'], xi,
                          tau_bad, p['N0'], d_bad)['threshold'],
                      bad_final_norm=norm1(xs_b[-1]),
                      bad_min_tail_norm=min(norm1(v) for v in xs_b[-20000:]),
                      bad_max_tail_norm=max(norm1(v) for v in xs_b[-20000:]))

    # Figure 2
    cv = PNGCanvas(1500, 560)
    ax = Axes(cv, 90, 70, 380, 400, (0, T_unc), (-1, 12),
              xlabel='t', ylabel='x1(t), x2(t)',
              title='(a) no control')
    for i in range(2):
        ax.plot(ts_u, [v[i] for v in xs_u], COLS[i], stride=20)
    ax.legend([('x1(t)', COLS[0]), ('x2(t)', COLS[1])], 'nw')
    ax = Axes(cv, 580, 70, 380, 400, (0, 30), (-0.05, 0.3),
              xlabel='t', ylabel='x1(t), x2(t)',
              title='(b) tau_a=3 > %.3f' % th['threshold'])
    for i in range(2):
        ax.plot(ts_c, [v[i] for v in xs_c], COLS[i], stride=10)
    ax.vmark(Ts_c, DARK_GREEN, 'Ts=%.2f' % Ts_c)
    ax.legend([('x1(t)', COLS[0]), ('x2(t)', COLS[1])], 'ne')
    ax = Axes(cv, 1070, 70, 380, 400, (0, T_c), (-10, 10),
              xlabel='t', ylabel='x1(t), x2(t)',
              title='(c) tau_a=0.06 < %.3f' % res['ex1']['bad_threshold'])
    for i in range(2):
        ax.plot(ts_b, [v[i] for v in xs_b], COLS[i], stride=10)
    ax.legend([('x1(t)', COLS[0]), ('x2(t)', COLS[1])], 'ne')
    cv.text_c(750, 528, 'x(tl+) = 1.0 x(tl) + 0.2 x(tl - d);  (a),(b): theta = 0.5,'
              ' d = 0.4;  (c): theta = 0.05, d = 0.04;  N0 = 2', BLACK)
    cv.save(os.path.join(OUT, 'Figure_2_Example1_trajectories.png'))

    # Figure 3: Lyapunov function vs comparison functions (log scale).
    # A small initial state reaches zero inside the sampling window
    # (t_1 - d, t_1] = (0.1, 0.5]; the delayed impulse at t_1 = 0.5 then
    # re-excites the state with 0.2 x(0.1).
    FLOOR = 1e-7                 # numerical chattering floor of RK4
    x0r = [0.0035, -0.00175]
    T3 = 1.2
    imp3 = impulse_sequence(tau_ok, p['N0'], p['theta'], T3)
    ts3, xs3 = simulate(ex1_rhs(True), x0r, T3, imp3, p['d'], G1, G2)
    W = [norm1(v) for v in xs3]
    Nh = majorant(W[0], T3, imp3, p['d'], p['a'], p['b'], p['c'],
                  p['alpha'], p['beta'], xi, hold=True)
    Nn = majorant(W[0], T3, imp3, p['d'], p['a'], p['b'], p['c'],
                  p['alpha'], p['beta'], xi, hold=False)
    k1 = int(round(imp3[0] / H))
    first_zero = next(ts3[i] for i in range(len(W)) if W[i] < FLOOR)
    resettle = next(ts3[i] for i in range(k1, len(W)) if W[i] < FLOOR)
    zero_h = next((ts3[i] for i in range(len(Nh)) if Nh[i] == 0.0), None)
    zero_n = next((ts3[i] for i in range(len(Nn)) if Nn[i] == 0.0), None)
    exc_h = max(W[i] - Nh[i] for i in range(len(W)))
    exc_n = max(W[i] - Nn[i] for i in range(len(W)))
    res['ex1'].update(
        fig3_x0=x0r, fig3_first_zero=first_zero, fig3_pre_jump=W[k1 - 1],
        fig3_post_jump=W[k1], fig3_resettle=resettle,
        fig3_hold_zero=zero_h, fig3_naive_zero=zero_n,
        fig3_max_excess_hold=exc_h, fig3_max_excess_naive=exc_n,
        fig3_theory=theorem1(p['a'], p['b'], p['c'], p['alpha'], p['beta'],
                             xi, tau_ok, p['N0'], p['d']))
    cv = PNGCanvas(1100, 600)
    ax = Axes(cv, 110, 70, 900, 430, (0, T3), (1e-8, 1e-1),
              logy=True, xlabel='t',
              ylabel='W(t) = |x1|+|x2|  and comparison functions (log)',
              title='Example 1: re-excitation and the hold-window majorant')
    cv.fill_rect(ax.px(imp3[0] - p['d']), 71, ax.px(imp3[0]), 499,
                 (255, 240, 225))
    ax.plot(ts3, [max(w, 1e-12) for w in W], MED_BLUE, 3)
    ax.plot(ts3, [max(n, 1e-12) for n in Nh], RED, 2)
    ax.plot(ts3, [max(n, 1e-12) for n in Nn], ORANGE, 2, dashed=True)
    cv.circle(ax.px(imp3[0]), ax.py(W[k1]), 7, DARK_GREEN)
    ax.vmark(imp3[0], BLACK, 't1 = 0.5')
    ax.legend([('W(t) simulated', MED_BLUE),
               ('N(t) with hold window (Lemma 3)', RED),
               ('naive N(t), delay ignored', ORANGE),
               ('o  re-excitation W(t1+) = 0.2 W(t1 - d)', DARK_GREEN)], 'ne')
    cv.text_c(560, 560, 'shaded: sampling/hold window (t1 - d, t1] = '
              '(0.1, 0.5];  values below 1e-7 are RK4 chattering', BLACK)
    cv.save(os.path.join(OUT, 'Figure_3_Example1_majorants.png'))

    # Figure 1: impulse timeline, delayed sampling and active clock
    T1 = 13.0
    imp1 = impulse_sequence(tau_ok, p['N0'], p['theta'], T1)
    cv = PNGCanvas(1200, 620)
    cv.text_c(600, 12, 'Delayed impulses, hold windows and the active clock',
              BLACK, 2)
    ax = Axes(cv, 90, 70, 1040, 170, (0, T1), (0, 1), xlabel='t',
              ylabel='impulse instants tl (solid), sampling instants '
              'tl - dl (dashed), hold windows (shaded)')
    for t in imp1:
        s = t - p['d']
        cv.fill_rect(ax.px(s), 72, ax.px(t), 238, LIGHT_ORANGE)
        cv.vline(ax.px(t), 90, 238, RED)
        cv.vline(ax.px(t) + 1, 90, 238, RED)
        for y in range(110, 238, 8):
            cv.vline(ax.px(s), y, y + 4, DARK_BLUE)
        cv.arrow(ax.px(s), 130, ax.px(t), 130, DARK_GREEN, 2, 6)
    cv.rect(90, 70, 1130, 240, BLACK)
    # active clock
    sig, sv, ts1 = [], 0.0, []
    holds = [(t - p['d'], t) for t in imp1]
    k = 0
    while k * 0.01 <= T1 + 1e-9:
        t = k * 0.01
        inhold = any(a_ < t <= b_ for a_, b_ in holds)
        if k > 0 and not inhold:
            sv += 0.01
        ts1.append(t); sig.append(sv)
        k += 1
    ax2 = Axes(cv, 90, 320, 1040, 230, (0, T1), (0, T1), xlabel='t',
               ylabel='active clock sigma(t) (solid) vs t (dashed)')
    ax2.plot(ts1, ts1, GRAY, 1, dashed=True)
    ax2.plot(ts1, sig, MED_BLUE, 3)
    cv.text_c(600, 598, 'tau_a = 3, N0 = 2, theta = 0.5, d = 0.4:  '
              'impulse intervals alternate 0.5 and 5.5', BLACK)
    cv.save(os.path.join(OUT, 'Figure_1_Delayed_impulse_mechanism.png'))
    return None


def run_example2(res):
    imp = IMP2
    G1 = [imp['rho1']] * 2 + [imp['om1']] * 2
    G2 = [imp['rho2']] * 2 + [imp['om2']] * 2
    z0 = [1.5, -1.2, -1.0, 1.8]
    k2 = thm2_constants()
    k3 = thm3_constants()
    tau_ok = 0.8
    bad = dict(tau=0.03, theta=0.02, d=0.015)      # violates Theorem 2
    mid = dict(tau=0.1, theta=0.08, d=0.05)        # violates Theorem 3
    t2 = theorem1(k2['phi'], k2['psi_tilde'], k2['delta'], k2['alpha'],
                  k2['beta'], k2['xi'], tau_ok, imp['N0'], imp['d'])
    t3 = theorem1(k3['chi_tilde'], k3['rho_tilde'], k3['Theta_tilde'],
                  k3['alpha'], k3['beta'], k3['xi'], tau_ok, imp['N0'],
                  imp['d'])
    res['ex2'] = dict(imp=imp, z0=z0, thm2=k2, thm3=k3, tau_ok=tau_ok,
                      bad=bad, mid=mid, T_thm2=t2, T_thm3=t3)
    T = 12.0
    imp_ok = impulse_sequence(tau_ok, imp['N0'], imp['theta'], T)
    imp_bad = impulse_sequence(bad['tau'], imp['N0'], bad['theta'], T)
    imp_mid = impulse_sequence(mid['tau'], imp['N0'], mid['theta'], T)
    zbig = [6.0, -5.0, -4.0, 7.0]

    ts0, zs0 = simulate(bam_rhs(no_control), z0, 50.0, [], 0.0, G1, G2,
                        h=2e-3)
    ts_a, zs_a = simulate(bam_rhs(controller1()), z0, T, imp_ok, imp['d'],
                          G1, G2)
    ts_b, zs_b = simulate(bam_rhs(controller1()), zbig, T, imp_bad,
                          bad['d'], G1, G2)
    ts_c, zs_c = simulate(bam_rhs(controller2()), z0, T, imp_ok, imp['d'],
                          G1, G2)
    ts_d, zs_d = simulate(bam_rhs(controller2(linear=False)), zbig, T,
                          imp_mid, mid['d'], G1, G2)
    ts_e, zs_e = simulate(bam_rhs(controller2()), zbig, T, imp_mid,
                          mid['d'], G1, G2)
    ts_f, zs_f = simulate(bam_rhs(controller1()), zbig, T, imp_mid,
                          mid['d'], G1, G2)
    s_a, s_b = settling_time(ts_a, zs_a), settling_time(ts_b, zs_b)
    s_c, s_d = settling_time(ts_c, zs_c), settling_time(ts_d, zs_d)
    s_e, s_f = settling_time(ts_e, zs_e), settling_time(ts_f, zs_f)

    def tail(zs):
        v = [norm1(z) for z in zs[-3000:]]
        return [min(v), max(v)]

    def thr(kc, which, case):
        if which == 2:
            return theorem1(kc['phi'], kc['psi_tilde'], kc['delta'],
                            kc['alpha'], kc['beta'], kc['xi'], case['tau'],
                            imp['N0'], case['d'])['threshold']
        return theorem1(kc['chi_tilde'], kc['rho_tilde'], kc['Theta_tilde'],
                        kc['alpha'], kc['beta'], kc['xi'], case['tau'],
                        imp['N0'], case['d'])['threshold']
    res['ex2'].update(
        settle_c1_ok=s_a, settle_c1_bad=s_b, settle_c2_ok=s_c,
        settle_c2_nolinear_mid=s_d, settle_c2_mid=s_e, settle_c1_mid=s_f,
        thr_c1_bad=thr(k2, 2, bad), thr_c1_mid=thr(k2, 2, mid),
        thr_c2_mid=thr(k3, 3, mid),
        tail_c1_bad=tail(zs_b), tail_c2_nolinear_mid=tail(zs_d),
        tail_uncontrolled=tail(zs0))
    labels = ['x1', 'x2', 'y1', 'y2']

    # Figure 4: controller 1
    cv = PNGCanvas(1500, 560)
    ax = Axes(cv, 90, 70, 380, 400, (0, 50), (-6, 6), xlabel='t',
              ylabel='states', title='(a) no control, no impulses')
    for i in range(4):
        ax.plot(ts0, [v[i] for v in zs0], COLS[i], stride=10)
    ax.legend([(labels[i], COLS[i]) for i in range(4)], 'ne')
    ax = Axes(cv, 580, 70, 380, 400, (0, T), (-8, 8), xlabel='t',
              ylabel='states',
              title='(b) tau_a=0.03 < %.3f' % res['ex2']['thr_c1_bad'])
    for i in range(4):
        ax.plot(ts_b, [v[i] for v in zs_b], COLS[i], stride=5)
    ax.legend([(labels[i], COLS[i]) for i in range(4)], 'ne')
    ax = Axes(cv, 1070, 70, 380, 400, (0, 8), (-2, 2), xlabel='t',
              ylabel='states',
              title='(c) tau_a=0.8 > %.3f' % t2['threshold'])
    for i in range(4):
        ax.plot(ts_a, [v[i] for v in zs_a], COLS[i], stride=5)
    ax.vmark(s_a, DARK_GREEN, 'Ts=%.2f' % s_a)
    ax.legend([(labels[i], COLS[i]) for i in range(4)], 'ne')
    cv.text_c(750, 528, 'Controller 1 (signum type); rho = (1.05, 0.15), '
              'omega = (1.10, 0.15); (b): theta = 0.02, d = 0.015; '
              '(c): theta = 0.2, d = 0.1', BLACK)
    cv.save(os.path.join(OUT, 'Figure_4_Example2_controller1.png'))

    # Figure 5: controller 2
    cv = PNGCanvas(1500, 560)
    ax = Axes(cv, 90, 70, 380, 400, (0, T), (-10, 10), xlabel='t',
              ylabel='states', title='(a) no linear gains, tau_a=0.1')
    for i in range(4):
        ax.plot(ts_d, [v[i] for v in zs_d], COLS[i], stride=5)
    ax.legend([(labels[i], COLS[i]) for i in range(4)], 'ne')
    ax = Axes(cv, 580, 70, 380, 400, (0, T), (-8, 8), xlabel='t',
              ylabel='states',
              title='(b) full law, tau_a=0.1 < %.3f' % res['ex2']['thr_c2_mid'])
    for i in range(4):
        ax.plot(ts_e, [v[i] for v in zs_e], COLS[i], stride=5)
    if s_e is not None:
        ax.vmark(s_e, DARK_GREEN, 'Ts=%.2f' % s_e)
    ax.legend([(labels[i], COLS[i]) for i in range(4)], 'ne')
    ax = Axes(cv, 1070, 70, 380, 400, (0, 8), (-2, 2), xlabel='t',
              ylabel='states',
              title='(c) full law, tau_a=0.8 > %.3f' % t3['threshold'])
    for i in range(4):
        ax.plot(ts_c, [v[i] for v in zs_c], COLS[i], stride=5)
    if s_c is not None:
        ax.vmark(s_c, DARK_GREEN, 'Ts=%.2f' % s_c)
    ax.legend([(labels[i], COLS[i]) for i in range(4)], 'ne')
    cv.text_c(750, 528, 'Controller 2 (odd-rational powers, no signum); '
              '(a),(b): theta = 0.08, d = 0.05; (c): theta = 0.2, d = 0.1',
              BLACK)
    cv.save(os.path.join(OUT, 'Figure_5_Example2_controller2.png'))

    # Figure 6(a): bound vs delay; (b) settling time vs initial size
    curves = []
    for tau in (0.6, 0.8, 1.2):
        ds, Ts = [], []
        for i in range(0, 200):
            dbar = i * 0.001
            if dbar >= imp['theta']:
                break
            r = theorem1(k2['phi'], k2['psi_tilde'], k2['delta'],
                         k2['alpha'], k2['beta'], k2['xi'], tau, imp['N0'],
                         dbar)
            if r['feasible']:
                ds.append(dbar); Ts.append(r['Tmax'])
        curves.append((tau, ds, Ts))
    rng = random.Random(7)
    sizes, stimes = [], []
    for j in range(24):
        mag = 10 ** (-1 + 3.0 * j / 23)
        z = [rng.uniform(-1, 1) for _ in range(4)]
        sc = mag / norm1(z)
        z = [v * sc for v in z]
        ts_r, zs_r = simulate(bam_rhs(controller1()), z, 8.0, imp_ok,
                              imp['d'], G1, G2)
        sizes.append(mag); stimes.append(settling_time(ts_r, zs_r))
    res['ex2']['fixed_time_sweep'] = dict(sizes=sizes, settle=stimes)
    res['ex2']['bound_curves'] = [
        dict(tau=c[0], d_at_10=[(d, T) for d, T in zip(c[1], c[2])
                                if abs(d * 1000 - round(d * 1000)) < 1e-9
                                and round(d * 1000) % 25 == 0])
        for c in curves]
    cv = PNGCanvas(1300, 600)
    ymax = 40
    ax = Axes(cv, 90, 70, 520, 420, (0, 0.2), (0, ymax), xlabel='delay bound d',
              ylabel='settling-time bound Tmax (Theorem 2)',
              title='(a) cost of impulse delay')
    for i, (tau, ds, Ts) in enumerate(curves):
        ax.plot(ds, [min(T, ymax) for T in Ts], COLS[i], 3)
    ax.legend([('tau_a = %.1f' % c[0], COLS[i]) for i, c in
               enumerate(curves)], 'nw')
    lx = [math.log10(s) for s in sizes]
    ax = Axes(cv, 720, 70, 520, 420, (-1, 2), (0, 10),
              xlabel='log10 of ||z(0)||_1',
              ylabel='settling time (simulated) and bound',
              title='(b) fixed-time property')
    ax.scatter(lx, [s for s in stimes], MED_BLUE, 4)
    ax.hmark(t2['Tmax'], RED)
    cv.text(ax.x0 + 10, ax.py(t2['Tmax']) - 14,
            'Tmax = %.2f (Theorem 2)' % t2['Tmax'], RED)
    cv.text_c(650, 560, 'Example 2 with controller 1; (b) uses tau_a = 0.8, '
              'd = 0.1 and 24 random initial states', BLACK)
    cv.save(os.path.join(OUT, 'Figure_6_Bounds_and_fixed_time.png'))


def delay_sweep(res):
    """Table 5: settling times versus delay for Example 2, controller 1."""
    imp = IMP2
    G1 = [imp['rho1']] * 2 + [imp['om1']] * 2
    G2 = [imp['rho2']] * 2 + [imp['om2']] * 2
    k2 = thm2_constants()
    rows = []
    for d in (0.0, 0.05, 0.1, 0.15, 0.19):
        th = theorem1(k2['phi'], k2['psi_tilde'], k2['delta'], k2['alpha'],
                      k2['beta'], k2['xi'], 0.8, imp['N0'], d)
        imp_ok = impulse_sequence(0.8, imp['N0'], imp['theta'], 10.0)
        ts, zs = simulate(bam_rhs(controller1()), [1.5, -1.2, -1.0, 1.8],
                          10.0, imp_ok, d, G1, G2)
        rows.append(dict(d=d, threshold=th['threshold'],
                         Tmax=th.get('Tmax'), settle=settling_time(ts, zs)))
    res['delay_sweep'] = rows


def main():
    os.makedirs(OUT, exist_ok=True)
    res = {}
    run_example1(res)
    run_example2(res)
    delay_sweep(res)
    with open(os.path.join(OUT, 'results.json'), 'w') as f:
        json.dump(res, f, indent=2, default=str)
    print(json.dumps(res, indent=1, default=str)[:6000])


if __name__ == '__main__':
    main()
