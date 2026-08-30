#!/usr/bin/env python3
"""
Generate 4 scientific figures (PNG) for the chapter
"Differential Equations and Dynamical Systems in Biology".
Stdlib only (no matplotlib/PIL/numpy).
"""

import os
import math
from biomath_pngcanvas import (PNGCanvas, DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
                               DARK_GREEN, MED_GREEN, LIGHT_GREEN, ORANGE, RED, LIGHT_RED,
                               PURPLE, GOLD, GRAY, LIGHT_GRAY, BLACK, WHITE)

OUT = '/projects/sandbox/AMMAN/biomath_figures'
os.makedirs(OUT, exist_ok=True)


def draw_axes(c, x0, y0, x1, y1, xlabel, ylabel, title):
    """Draw a plot frame with axes and labels. Origin at (x0,y1)."""
    # axes
    c.line(x0, y1, x1, y1, BLACK, 2)   # x-axis
    c.line(x0, y0, x0, y1, BLACK, 2)   # y-axis
    c.arrow(x1 - 4, y1, x1 + 8, y1, BLACK, 2)
    c.arrow(x0, y0 + 4, x0, y0 - 8, BLACK, 2)
    c.text(x1 - len(xlabel) * 6, y1 + 12, xlabel, BLACK, 1)
    c.text_v(x0 - 22, (y0 + y1) // 2, ylabel, BLACK, 1)
    c.text_c((x0 + x1) // 2, y0 - 22, title, DARK_BLUE, 2)


def fig1_growth():
    """Figure 1: Exponential vs logistic growth curves + carrying capacity."""
    W, H = 900, 560
    c = PNGCanvas(W, H)
    c.text_c(W // 2, 18, 'Population Growth Dynamics', DARK_BLUE, 2)

    x0, y0, x1, y1 = 90, 70, 830, 470
    draw_axes(c, x0, y0, x1, y1, 'Time t', 'Population N(t)', '')

    # gridlines
    for gy in range(1, 5):
        yy = y1 - gy * (y1 - y0) // 5
        c.hline(x0 + 1, x1, yy, LIGHT_GRAY)

    K = 1.0
    N0 = 0.05
    r = 0.09
    span = 100.0
    # carrying capacity line
    yK = y1 - int(0.9 * (y1 - y0))
    c.dashed_line(x0, yK, x1, yK, RED, 8, 6, 2)
    c.text(x1 - 150, yK - 16, 'Carrying capacity K', RED, 1)

    # logistic
    pts = []
    for i in range(0, 301):
        t = span * i / 300.0
        N = K / (1 + (K - N0) / N0 * math.exp(-r * t))
        px = x0 + int((x1 - x0) * t / span)
        py = y1 - int((y1 - y0) * (N / K) * 0.9)
        pts.append((px, py))
    c.polyline(pts, MED_GREEN, 3)

    # exponential (clipped)
    pts2 = []
    for i in range(0, 301):
        t = span * i / 300.0
        N = N0 * math.exp(r * t)
        if N > K * 1.05:
            break
        px = x0 + int((x1 - x0) * t / span)
        py = y1 - int((y1 - y0) * (N / K) * 0.9)
        pts2.append((px, py))
    c.polyline(pts2, MED_BLUE, 3)

    # legend
    lx, ly = x0 + 30, y0 + 8
    c.line(lx, ly, lx + 28, ly, MED_BLUE, 3)
    c.text(lx + 34, ly - 4, 'Exponential  dN/dt = rN', MED_BLUE, 1)
    c.line(lx, ly + 22, lx + 28, ly + 22, MED_GREEN, 3)
    c.text(lx + 34, ly + 18, 'Logistic  dN/dt = rN(1-N/K)', MED_GREEN, 1)

    c.save(os.path.join(OUT, 'Figure_1_Growth_Models.png'))
    print('Figure 1 saved')


def fig2_predator_prey():
    """Figure 2: Lotka-Volterra time series + phase portrait (two panels)."""
    W, H = 960, 560
    c = PNGCanvas(W, H)
    c.text_c(W // 2, 16, 'Lotka-Volterra Predator-Prey Dynamics', DARK_BLUE, 2)

    # simulate
    alpha, beta, delta, gamma = 1.0, 0.1, 0.075, 1.5
    x, y = 10.0, 5.0
    dt = 0.005
    steps = 8000
    xs, ys = [], []
    for _ in range(steps):
        dx = alpha * x - beta * x * y
        dy = delta * x * y - gamma * y
        x += dx * dt
        y += dy * dt
        xs.append(x); ys.append(y)

    # Panel A: time series
    ax0, ay0, ax1, ay1 = 70, 70, 470, 470
    draw_axes(c, ax0, ay0, ax1, ay1, 'Time', 'Density', '')
    c.text_c((ax0 + ax1) // 2, ay0 - 20, 'A  Time Series', DARK_BLUE, 1)
    maxv = max(max(xs), max(ys))
    prey = []
    pred = []
    N = len(xs)
    for i in range(0, N, 15):
        px = ax0 + int((ax1 - ax0) * i / N)
        py1 = ay1 - int((ay1 - ay0) * xs[i] / maxv * 0.95)
        py2 = ay1 - int((ay1 - ay0) * ys[i] / maxv * 0.95)
        prey.append((px, py1)); pred.append((px, py2))
    c.polyline(prey, MED_GREEN, 2)
    c.polyline(pred, RED, 2)
    c.line(ax0 + 20, ay0 + 6, ax0 + 44, ay0 + 6, MED_GREEN, 3)
    c.text(ax0 + 50, ay0 + 2, 'Prey x', MED_GREEN, 1)
    c.line(ax0 + 20, ay0 + 26, ax0 + 44, ay0 + 26, RED, 3)
    c.text(ax0 + 50, ay0 + 22, 'Predator y', RED, 1)

    # Panel B: phase portrait
    bx0, by0, bx1, by1 = 560, 70, 920, 470
    draw_axes(c, bx0, by0, bx1, by1, 'Prey x', 'Predator y', '')
    c.text_c((bx0 + bx1) // 2, by0 - 20, 'B  Phase Portrait', DARK_BLUE, 1)
    mx = max(xs) * 1.05
    my = max(ys) * 1.05
    phase = []
    for i in range(0, N, 12):
        px = bx0 + int((bx1 - bx0) * xs[i] / mx)
        py = by1 - int((by1 - by0) * ys[i] / my)
        phase.append((px, py))
    c.polyline(phase, PURPLE, 2)
    # equilibrium point (gamma/delta, alpha/beta)
    ex = gamma / delta
    ey = alpha / beta
    epx = bx0 + int((bx1 - bx0) * ex / mx)
    epy = by1 - int((by1 - by0) * ey / my)
    c.circle(epx, epy, 5, BLACK, ORANGE, 2)
    c.text(epx + 8, epy - 6, 'Equilibrium', BLACK, 1)

    c.save(os.path.join(OUT, 'Figure_2_Predator_Prey.png'))
    print('Figure 2 saved')


def fig3_sir():
    """Figure 3: SIR epidemic compartmental curves + flow diagram."""
    W, H = 960, 560
    c = PNGCanvas(W, H)
    c.text_c(W // 2, 16, 'SIR Epidemic Model', DARK_BLUE, 2)

    # flow diagram (top)
    fy = 70
    boxes = [('S', LIGHT_GREEN, 150), ('I', LIGHT_RED, 460), ('R', LIGHT_BLUE, 770)]
    for label, col, cx in boxes:
        c.rounded_panel(cx - 46, fy, cx + 46, fy + 60, DARK_BLUE, col)
        c.text_c(cx, fy + 22, label, BLACK, 3)
    c.arrow(196, fy + 30, 414, fy + 30, DARK_BLUE, 3)
    c.text_c(305, fy + 6, 'beta S I / N', DARK_BLUE, 1)
    c.arrow(506, fy + 30, 724, fy + 30, DARK_BLUE, 3)
    c.text_c(615, fy + 6, 'gamma I', DARK_BLUE, 1)

    # simulate SIR
    N = 1.0
    S, I, R = 0.99, 0.01, 0.0
    beta, gamma = 0.5, 0.12
    dt = 0.1
    steps = 1600
    Ss, Is, Rs = [], [], []
    for _ in range(steps):
        dS = -beta * S * I / N
        dI = beta * S * I / N - gamma * I
        dR = gamma * I
        S += dS * dt; I += dI * dt; R += dR * dt
        Ss.append(S); Is.append(I); Rs.append(R)

    x0, y0, x1, y1 = 90, 200, 890, 500
    draw_axes(c, x0, y0, x1, y1, 'Time (days)', 'Fraction of population', '')
    for gy in range(1, 5):
        yy = y1 - gy * (y1 - y0) // 5
        c.hline(x0 + 1, x1, yy, LIGHT_GRAY)

    def series(vals, col):
        pts = []
        M = len(vals)
        for i in range(0, M, 4):
            px = x0 + int((x1 - x0) * i / M)
            py = y1 - int((y1 - y0) * vals[i] * 0.97)
            pts.append((px, py))
        c.polyline(pts, col, 3)

    series(Ss, MED_GREEN)
    series(Is, RED)
    series(Rs, MED_BLUE)

    lx, ly = x0 + 400, y0 + 10
    c.line(lx, ly, lx + 26, ly, MED_GREEN, 3); c.text(lx + 32, ly - 4, 'Susceptible S', MED_GREEN, 1)
    c.line(lx, ly + 22, lx + 26, ly + 22, RED, 3); c.text(lx + 32, ly + 18, 'Infected I', RED, 1)
    c.line(lx, ly + 44, lx + 26, ly + 44, MED_BLUE, 3); c.text(lx + 32, ly + 40, 'Recovered R', MED_BLUE, 1)

    c.save(os.path.join(OUT, 'Figure_3_SIR_Model.png'))
    print('Figure 3 saved')


def fig4_bifurcation():
    """Figure 4: Hopf bifurcation schematic + stability regions."""
    W, H = 900, 560
    c = PNGCanvas(W, H)
    c.text_c(W // 2, 16, 'Bifurcation and Stability Landscape', DARK_BLUE, 2)

    x0, y0, x1, y1 = 90, 80, 830, 480
    draw_axes(c, x0, y0, x1, y1, 'Parameter mu', 'State x*', '')
    # vertical bifurcation line at mu = 0 (mapped to centre)
    mu0 = x0 + (x1 - x0) // 2
    c.dashed_line(mu0, y0, mu0, y1, GRAY, 6, 5, 1)
    c.text(mu0 - 40, y0 - 4, 'mu = 0 (Hopf)', GRAY, 1)

    midy = (y0 + y1) // 2
    # stable equilibrium branch (solid) for mu<0
    c.line(x0 + 10, midy, mu0, midy, MED_BLUE, 3)
    c.text(x0 + 30, midy + 12, 'Stable focus', MED_BLUE, 1)
    # unstable equilibrium branch (dashed) for mu>0
    c.dashed_line(mu0, midy, x1 - 10, midy, RED, 7, 5, 3)
    c.text(mu0 + 120, midy + 12, 'Unstable focus', RED, 1)

    # emerging limit cycle envelope (parabola opening right)
    top = []
    bot = []
    for i in range(0, 200):
        frac = i / 200.0
        mu = frac * (x1 - 10 - mu0)
        amp = int(150 * math.sqrt(max(0, frac)))
        px = mu0 + mu
        top.append((px, midy - amp))
        bot.append((px, midy + amp))
    c.polyline(top, DARK_GREEN, 2)
    c.polyline(bot, DARK_GREEN, 2)
    c.text(x1 - 210, midy - 150, 'Stable limit cycle', DARK_GREEN, 1)

    # small phase inset circles
    c.circle(x0 + 90, y0 + 60, 22, MED_BLUE, None, 2)
    c.arrow(x0 + 90 + 22, y0 + 60, x0 + 90 + 10, y0 + 60 - 18, MED_BLUE, 2)
    c.text_c(x0 + 90, y0 + 96, 'spiral in', MED_BLUE, 1)

    c.circle(x1 - 120, y0 + 60, 26, DARK_GREEN, None, 2)
    c.circle(x1 - 120, y0 + 60, 8, RED, None, 2)
    c.text_c(x1 - 120, y0 + 100, 'oscillation', DARK_GREEN, 1)

    c.save(os.path.join(OUT, 'Figure_4_Bifurcation.png'))
    print('Figure 4 saved')


if __name__ == '__main__':
    fig1_growth()
    fig2_predator_prey()
    fig3_sir()
    fig4_bifurcation()
    print('All figures generated in', OUT)
