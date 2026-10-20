#!/usr/bin/env python3
"""
Dependency-free simulation + SVG plotting for the manuscript
"Fixed-Time Stability of Delayed Cohen-Grossberg BAM Neural Networks
 with Destabilizing Impulsive Perturbations".

No numpy / matplotlib required (offline sandbox). Explicit Euler with a
delay history buffer; figures emitted as SVG. All reported settling times
are computed from these trajectories.
"""
import math, os

OUT = os.path.join(os.path.dirname(__file__), "fxts_figures")
os.makedirs(OUT, exist_ok=True)

COLORS = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e", "#17becf"]


# ----------------------------------------------------------------------
# SVG line-plot helper
# ----------------------------------------------------------------------
def svg_plot(path, series, title, xlabel, ylabel, T, vmark=None, vlabel=None):
    """series: list of (label, list_of_(t,value)). vmark: optional x to mark."""
    W, H = 680, 420
    ml, mr, mt, mb = 70, 140, 48, 56
    pw, ph = W - ml - mr, H - mt - mb
    ys = [v for _, pts in series for _, v in pts]
    ymin, ymax = min(ys), max(ys)
    if ymax - ymin < 1e-9:
        ymax += 1.0; ymin -= 1.0
    pad = 0.08 * (ymax - ymin)
    ymin -= pad; ymax += pad
    xmin, xmax = 0.0, T

    def X(t): return ml + (t - xmin) / (xmax - xmin) * pw
    def Y(v): return mt + (ymax - v) / (ymax - ymin) * ph

    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
         'font-family="Helvetica,Arial,sans-serif">' % (W, H)]
    s.append('<rect width="%d" height="%d" fill="white"/>' % (W, H))
    # axes box
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" '
             'stroke="#333" stroke-width="1"/>' % (ml, mt, pw, ph))
    # gridlines + y ticks
    for i in range(6):
        v = ymin + (ymax - ymin) * i / 5
        yy = Y(v)
        s.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#eee"/>'
                 % (ml, yy, ml + pw, yy))
        s.append('<text x="%d" y="%.1f" font-size="11" text-anchor="end" '
                 'fill="#333">%.2f</text>' % (ml - 6, yy + 4, v))
    # x ticks
    for i in range(7):
        t = xmin + (xmax - xmin) * i / 6
        xx = X(t)
        s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#eee"/>'
                 % (xx, mt, xx, mt + ph))
        s.append('<text x="%.1f" y="%d" font-size="11" text-anchor="middle" '
                 'fill="#333">%.1f</text>' % (xx, mt + ph + 18, t))
    # settling marker
    if vmark is not None and vmark <= T:
        xx = X(vmark)
        s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#000" '
                 'stroke-dasharray="5,4" stroke-width="1.2"/>'
                 % (xx, mt, xx, mt + ph))
        s.append('<text x="%.1f" y="%d" font-size="11" text-anchor="middle" '
                 'fill="#000">%s</text>' % (xx, mt - 6, vlabel or ""))
    # data
    for idx, (label, pts) in enumerate(series):
        col = COLORS[idx % len(COLORS)]
        d = " ".join("%.2f,%.2f" % (X(t), Y(v)) for t, v in pts)
        s.append('<polyline fill="none" stroke="%s" stroke-width="1.6" '
                 'points="%s"/>' % (col, d))
        ly = mt + 16 + idx * 20
        s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" '
                 'stroke-width="2.4"/>' % (ml + pw + 14, ly, ml + pw + 40, ly, col))
        s.append('<text x="%d" y="%d" font-size="12" fill="#333">%s</text>'
                 % (ml + pw + 46, ly + 4, label))
    # labels
    s.append('<text x="%d" y="22" font-size="14" font-weight="bold" '
             'text-anchor="middle" fill="#111">%s</text>' % (W // 2, title))
    s.append('<text x="%d" y="%d" font-size="12" text-anchor="middle" '
             'fill="#111">%s</text>' % (ml + pw // 2, H - 14, xlabel))
    s.append('<text x="18" y="%d" font-size="12" text-anchor="middle" '
             'fill="#111" transform="rotate(-90 18 %d)">%s</text>'
             % (mt + ph // 2, mt + ph // 2, ylabel))
    s.append('</svg>')
    with open(path, "w") as f:
        f.write("\n".join(s))
    print("wrote", path)


def sign_pow(x, p):
    return math.copysign(abs(x) ** p, x) if x != 0 else 0.0


def impulse_times(tau_a, N0, h, T):
    """Impulse sequence (Eq. 45): spacing h, except every N0-th gap = N0(tau_a-h)+h."""
    ts, t, l = [], 0.0, 0
    while True:
        l += 1
        gap = h if (l % N0) != 0 else N0 * (tau_a - h) + h
        t += gap
        if t > T:
            break
        ts.append(t)
    return ts


# ----------------------------------------------------------------------
# Generic Euler integrator with delay + impulses
# ----------------------------------------------------------------------
def integrate(rhs, x0, T, dt, imp_times, imp_factor, tau, keep=25):
    n = len(x0)
    steps = int(T / dt)
    delay_steps = int(round(tau / dt)) if tau > 0 else 0
    hist = [list(x0) for _ in range(delay_steps + 1)]  # ring not needed; store all
    full = [list(x0)]
    x = list(x0)
    t = 0.0
    ip = 0
    traj = [(0.0, list(x))]
    for k in range(steps):
        # delayed state
        didx = max(0, len(full) - 1 - delay_steps)
        xd = full[didx]
        dx = rhs(t, x, xd)
        x = [x[i] + dt * dx[i] for i in range(n)]
        t += dt
        # apply impulses that occurred in (t-dt, t]
        while ip < len(imp_times) and imp_times[ip] <= t:
            x = [xi * imp_factor for xi in x]
            ip += 1
        full.append(list(x))
        if k % keep == 0:
            traj.append((t, list(x)))
    traj.append((t, list(x)))
    return traj


def settling_time(traj, idxs, eps=2e-2):
    """first time after which max|state components| stays below eps."""
    T = traj[-1][0]
    st = None
    for i in range(len(traj)):
        t, x = traj[i]
        if all(abs(x[j]) < eps for j in idxs):
            ok = all(all(abs(xx[j]) < eps for j in idxs) for _, xx in traj[i:])
            if ok:
                st = t
                break
    return st


# ======================================================================
# EXAMPLE 1 : cyber-physical system with impulsive deception attacks
# ======================================================================
SIG1 = 0.1  # transmission delay

def cps_free(t, x, xd):           # no control, no attack
    return [0.1 * math.sin(x[1]) + 0.05 * math.sin(xd[1]),
            0.1 * math.sin(x[0]) + 0.05 * math.sin(xd[0])]

def cps_ctrl(t, x, xd):           # controller (signum), Eq.(65)
    u = [-0.5 * x[i]
         - 0.4 * sign_pow(x[i], 0.5)
         - 1.2 * sign_pow(x[i], 1.5) for i in range(2)]
    return [0.1 * math.sin(x[1]) + 0.05 * math.sin(xd[1]) + u[0],
            0.1 * math.sin(x[0]) + 0.05 * math.sin(xd[0]) + u[1]]

x0_1 = [0.2, 0.1]

# Fig1: free, no attack
tr = integrate(cps_free, x0_1, 40, 0.002, [], 1.0, SIG1)
svg_plot(os.path.join(OUT, "Fig1_CPS_free_noattack.svg"),
         [("x1(t)", [(t, x[0]) for t, x in tr]),
          ("x2(t)", [(t, x[1]) for t, x in tr])],
         "Fig. 1  CPS (43): no controller, no deception attack",
         "t", "x1(t), x2(t)", 40)

# Fig2: attacks (destabilizing xi=1.2) no control -> unbounded
imp = impulse_times(2.0, 2, 0.1, 40)
tr = integrate(cps_free, x0_1, 40, 0.002, imp, 1.2, SIG1)
svg_plot(os.path.join(OUT, "Fig2_CPS_attack_noctrl.svg"),
         [("x1(t)", [(t, x[0]) for t, x in tr]),
          ("x2(t)", [(t, x[1]) for t, x in tr])],
         "Fig. 2  CPS (43): destabilizing impulses xi=1.2, no control",
         "t", "x1(t), x2(t)", 40)

# Fig3: controller + tau_a=1 (> ln1.2/0.34=0.536) -> FXTS
imp = impulse_times(1.0, 2, 0.1, 12)
tr = integrate(cps_ctrl, x0_1, 12, 0.001, imp, 1.2, SIG1)
st = settling_time(tr, [0, 1])
svg_plot(os.path.join(OUT, "Fig3_CPS_ctrl_FXTS.svg"),
         [("x1(t)", [(t, x[0]) for t, x in tr]),
          ("x2(t)", [(t, x[1]) for t, x in tr])],
         "Fig. 3  CPS (64): controller (65), tau_a=1>0.536  ->  FXTS",
         "t", "x1(t), x2(t)", 12,
         vmark=st, vlabel=("T~%.2f" % st) if st else None)
print("Ex1 FXTS observed settling:", st)

# Fig4: controller but tau_a=0.1 (<0.536) -> not FXTS
imp = impulse_times(0.1, 2, 0.02, 20)
tr = integrate(cps_ctrl, x0_1, 20, 0.0005, imp, 1.2, SIG1)
svg_plot(os.path.join(OUT, "Fig4_CPS_ctrl_notFXTS.svg"),
         [("x1(t)", [(t, x[0]) for t, x in tr]),
          ("x2(t)", [(t, x[1]) for t, x in tr])],
         "Fig. 4  CPS (64): controller (65), tau_a=0.1<0.536  ->  not FXTS",
         "t", "x1(t), x2(t)", 20)


# ======================================================================
# EXAMPLE 2 : delayed CGBAM neural network (2 + 2 neurons)
# ======================================================================
SIG2 = 0.2
Hm  = [[2.5, 0.5], [0.3, 1.5]]       # h_rs
Wm  = [[-0.4, 1.3], [1.5, -0.4]]     # w_sr
Hmt = [[0.5, 0.1], [0.06, 0.3]]      # h_rs^tau (delayed, ~0.2*H)
Wmt = [[-0.08, 0.26], [0.3, -0.08]]  # w_sr^tau

def a_amp(r, x): return (0.8 + 0.2 / (1 + x * x)) if r == 0 else (0.6 + 0.3 / (1 + x * x))
def c_amp(s, y): return (1.4 + 0.6 / (1 + y * y)) if s == 0 else (0.74 + 0.6 / (1 + y * y))
def b_beh(r, x): return (0.5 * x) if r == 0 else (0.74 * x)
def d_beh(s, y): return (0.2 * y) if s == 0 else (0.3 * y)
def g_act(x):   return 0.5 * math.tanh(x)
def f_act(y):   return 0.5 * (abs(y + 1) - abs(y - 1))

# state = [x1,x2,y1,y2]
def bam_rhs(ctrl):
    def rhs(t, st, sd):
        x = [st[0], st[1]]; y = [st[2], st[3]]
        xd = [sd[0], sd[1]]; yd = [sd[2], sd[3]]
        dx = [0.0, 0.0]; dy = [0.0, 0.0]
        for r in range(2):
            syn = sum(Hm[r][s] * f_act(y[s]) for s in range(2)) \
                + sum(Hmt[r][s] * f_act(yd[s]) for s in range(2))
            dx[r] = -a_amp(r, x[r]) * (b_beh(r, x[r]) - syn)
        for s in range(2):
            syn = sum(Wm[s][r] * g_act(x[r]) for r in range(2)) \
                + sum(Wmt[s][r] * g_act(xd[r]) for r in range(2))
            dy[s] = -c_amp(s, y[s]) * (d_beh(s, y[s]) - syn)
        ux, uy = ctrl(x, y)
        return [dx[0] + ux[0], dx[1] + ux[1], dy[0] + uy[0], dy[1] + uy[1]]
    return rhs

def no_ctrl(x, y): return [[0, 0], [0, 0]]

# controller 1 (signum): gains k=4(x), m=4(y); k1=m1=1.25, k2=m2=4; a=.8,b=1.8
#   (k,m chosen to satisfy delayed gain conditions (40)-(41) with q=1.2)
def ctrl1(x, y):
    ux = [-4 * x[r] - 1.25 * sign_pow(x[r], 0.8) - 4 * sign_pow(x[r], 1.8) for r in range(2)]
    uy = [-4 * y[s] - 1.25 * sign_pow(y[s], 0.8) - 4 * sign_pow(y[s], 1.8) for s in range(2)]
    return [ux, uy]

# controller 2 (no signum): Phi=Psi=6; k3=m3=0.5,k4=m4=1.5; a1=3,b1=7,a2=9,b2=5
#   (Phi,Psi chosen to satisfy delayed gain conditions (53)-(54) with q=1.2)
def ctrl2(x, y):
    ux = [-6 * x[r] - 0.5 * sign_pow(x[r], 3/7) - 1.5 * sign_pow(x[r], 9/5) for r in range(2)]
    uy = [-6 * y[s] - 0.5 * sign_pow(y[s], 3/7) - 1.5 * sign_pow(y[s], 9/5) for s in range(2)]
    return [ux, uy]

# controller 2 WITHOUT linear term (ablation: remove -Phi,-Psi and no linear decay)
def ctrl2_ablate(x, y):
    ux = [-0.5 * sign_pow(x[r], 3/7) - 1.5 * sign_pow(x[r], 9/5) for r in range(2)]
    uy = [-0.5 * sign_pow(y[s], 3/7) - 1.5 * sign_pow(y[s], 9/5) for s in range(2)]
    return [ux, uy]

x0_2 = [1.5, -1.0, -1.5, 1.0]

# Fig5: no controller -> oscillatory / non-convergent
tr = integrate(bam_rhs(no_ctrl), x0_2, 50, 0.002, [], 1.0, SIG2)
svg_plot(os.path.join(OUT, "Fig5_BAM_nocontrol.svg"),
         [("x1(t)", [(t, s[0]) for t, s in tr]),
          ("x2(t)", [(t, s[1]) for t, s in tr]),
          ("y1(t)", [(t, s[2]) for t, s in tr]),
          ("y2(t)", [(t, s[3]) for t, s in tr])],
         "Fig. 5  Delayed CGBAMNN (46): no controller",
         "t", "states", 50)

# Fig6: controller 1, tau_a=0.8 > ln(1.1)/delta ; xi=1.1 destabilizing
imp = impulse_times(0.8, 2, 0.4, 7)
tr = integrate(bam_rhs(ctrl1), x0_2, 7, 0.0005, imp, 1.1, SIG2)
st = settling_time(tr, [0, 1, 2, 3])
svg_plot(os.path.join(OUT, "Fig6_BAM_ctrl1_FXTS.svg"),
         [("x1(t)", [(t, s[0]) for t, s in tr]),
          ("x2(t)", [(t, s[1]) for t, s in tr]),
          ("y1(t)", [(t, s[2]) for t, s in tr]),
          ("y2(t)", [(t, s[3]) for t, s in tr])],
         "Fig. 6  Delayed CGBAMNN (46): controller (38), tau_a=0.8  ->  FXTS",
         "t", "states", 7, vmark=st, vlabel=("T~%.2f" % st) if st else None)
print("Ex2 ctrl1 FXTS observed settling:", st)

# Fig7: controller 2 (stable) vs ablation (no linear term -> fails under impulses)
imp = impulse_times(0.5, 1, 0.2, 7)
tr_ok = integrate(bam_rhs(ctrl2), x0_2, 7, 0.0005, imp, 1.2, SIG2)
tr_ab = integrate(bam_rhs(ctrl2_ablate), x0_2, 7, 0.0005, imp, 1.2, SIG2)
st2 = settling_time(tr_ok, [0, 1, 2, 3])
# plot norm ||state||_inf for each case
def inf_norm(tr): return [(t, max(abs(v) for v in s)) for t, s in tr]
svg_plot(os.path.join(OUT, "Fig7_BAM_ctrl2_ablation.svg"),
         [("with linear term (FXTS)", inf_norm(tr_ok)),
          ("linear term removed (ablation)", inf_norm(tr_ab))],
         "Fig. 7  Delayed CGBAMNN (46): controller (51) vs ablation",
         "t", "max |state component|", 7,
         vmark=st2, vlabel=("T~%.2f" % st2) if st2 else None)
print("Ex2 ctrl2 FXTS observed settling:", st2)

print("ln(1.2)/0.1 =", math.log(1.2) / 0.1)
print("done")
