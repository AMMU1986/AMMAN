#!/usr/bin/env python3
"""
Generate the corrected figures for the Carreau EMHD squeezing manuscript.
Pure stdlib: uses carreau_emhd_solver + pyplot_stdlib. Writes PNGs to
carreau_emhd_figures/.
"""

import os
from carreau_emhd_solver import Params, solve, solve_continuation, engineering, entropy_number
from pyplot_stdlib import plot, Canvas, PALETTE

OUT = "/projects/sandbox/AMMAN/carreau_emhd_figures"
os.makedirs(OUT, exist_ok=True)


def col(i):
    return PALETTE[i % len(PALETTE)]


def sample(sol, comp):
    """Return (eta_list, value_list) for a state component index."""
    xs = [e for e, _ in sol]
    ys = [y[comp] for _, y in sol]
    return xs, ys


# baseline converged unknowns, used as a warm start for hard cases
_BASE_SOL, _BASE_U = solve(Params())


def solve_warm(**kw):
    """Solve a parameter set warm-started from the baseline unknowns."""
    pr = Params(**kw)
    sol, u = solve(pr, u0=_BASE_U)
    return pr, sol, u


# ---------------------------------------------------------------------------
# Figure 1 : schematic of the squeezing channel (hand-drawn)
# ---------------------------------------------------------------------------
def figure1():
    c = Canvas(760, 480, bg=(255, 255, 255), ss=2)
    # plates
    c.line(90, 90, 670, 90, (90, 90, 90), 3)
    c.line(90, 380, 670, 380, (90, 90, 90), 3)
    c.text(300, 66, "Upper plate  (squeezing)", (30, 30, 30), 1)
    c.text(305, 388, "Lower plate  (stretching)", (30, 30, 30), 1)
    # squeezing arrows (down) from top plate
    for x in (200, 320, 440, 560):
        c.line(x, 40, x, 84, (214, 39, 40), 2)
        c.line(x, 84, x - 5, 76, (214, 39, 40), 2)
        c.line(x, 84, x + 5, 76, (214, 39, 40), 2)
    # magnetic field arrows (up, green) through the gap
    for x in (150, 270, 390, 510, 630):
        c.line(x, 376, x, 96, (44, 160, 44), 1)
        c.line(x, 96, x - 4, 104, (44, 160, 44), 1)
        c.line(x, 96, x + 4, 104, (44, 160, 44), 1)
    # nanoparticles
    import random
    random.seed(3)
    for _ in range(70):
        px = random.randint(110, 650)
        py = random.randint(110, 360)
        cc = (31, 119, 180) if random.random() < 0.5 else (255, 140, 0)
        for oy in range(-2, 3):
            for ox in range(-2, 3):
                if ox * ox + oy * oy <= 4:
                    c.px(px + ox, py + oy, cc)
    # axes
    c.line(60, 380, 60, 300, (0, 0, 0), 1); c.text(48, 288, "y", (0, 0, 0), 1)
    c.line(60, 380, 140, 380, (0, 0, 0), 1); c.text(146, 372, "x", (0, 0, 0), 1)
    # stretch arrow lower plate
    c.line(120, 396, 240, 396, (31, 119, 180), 2)
    c.line(240, 396, 232, 391, (31, 119, 180), 2)
    c.line(240, 396, 232, 401, (31, 119, 180), 2)
    c.text(120, 420, "Uw(x,t) stretch", (31, 119, 180), 1)
    c.text(430, 420, "B(t) magnetic  E(t) electric (aligned)", (44, 160, 44), 1)
    c.text(150, 20, "AA7072-AA7075 / Methanol Carreau hybrid nanofluid", (0, 0, 0), 1)
    c.downsample_png(os.path.join(OUT, "Figure_1_Schematic.png"))
    print("Figure 1 done")


# ---------------------------------------------------------------------------
# Figure 2 : f'(eta) for varying Sq
# ---------------------------------------------------------------------------
def figure2():
    res = solve_continuation({}, 'Sq', [0.2, 0.5, 0.8, 1.2])
    series = []
    for i, (v, sol, u, pr) in enumerate(res):
        xs, ys = sample(sol, 1)  # f'
        series.append({'x': xs, 'y': ys, 'label': "Sq = %.1f" % v, 'color': col(i)})
    plot(series, "eta", "f'(eta)", "Figure 2  Axial velocity f'(eta) vs Sq",
         os.path.join(OUT, "Figure_2_velocity_Sq.png"))
    print("Figure 2 done")


# ---------------------------------------------------------------------------
# Figure 3 : f'(eta) for varying We and M
# ---------------------------------------------------------------------------
def figure3():
    series = []
    combos = [("We", 0.5, {}), ("We", 2.0, {}), ("M", 0.5, {}), ("M", 2.0, {})]
    for i, (key, val, extra) in enumerate(combos):
        kw = dict(extra); kw[key] = val
        pr, sol, u = solve_warm(**kw)
        xs, ys = sample(sol, 1)
        series.append({'x': xs, 'y': ys, 'label': "%s = %.1f" % (key, val), 'color': col(i)})
    plot(series, "eta", "f'(eta)", "Figure 3  Velocity f'(eta) vs We and M",
         os.path.join(OUT, "Figure_3_velocity_We_M.png"))
    print("Figure 3 done")


# ---------------------------------------------------------------------------
# Figure 4 : theta(eta) for varying Rd and Ec
# ---------------------------------------------------------------------------
def figure4():
    series = []
    combos = [("Rd", 0.2), ("Rd", 1.0), ("Ec", 0.5), ("Ec", 0.9)]
    for i, (key, val) in enumerate(combos):
        pr, sol, u = solve_warm(**{key: val})
        xs, ys = sample(sol, 4)  # theta
        series.append({'x': xs, 'y': ys, 'label': "%s = %.1f" % (key, val), 'color': col(i)})
    plot(series, "eta", "theta(eta)", "Figure 4  Temperature theta(eta) vs Rd and Ec",
         os.path.join(OUT, "Figure_4_temperature_Rd_Ec.png"))
    print("Figure 4 done")


# ---------------------------------------------------------------------------
# Figure 5 : Ns(eta) for varying Br and M
# ---------------------------------------------------------------------------
def figure5():
    series = []
    combos = [("Br", 0.5, 1.0), ("Br", 1.0, 1.0), ("Br", 1.5, 1.0), ("M", 1.0, 2.0)]
    labels = ["Br=0.5, M=1.0", "Br=1.0, M=1.0", "Br=1.5, M=1.0", "Br=1.0, M=2.0"]
    for i, (key, br, m) in enumerate(combos):
        pr, sol, u = solve_warm(Br=br, M=m)
        xs = [e for e, _ in sol]
        ys = [entropy_number(e, y, pr)[0] for e, y in sol]
        series.append({'x': xs, 'y': ys, 'label': labels[i], 'color': col(i)})
    plot(series, "eta", "Ns(eta)", "Figure 5  Entropy generation Ns(eta) vs Br and M",
         os.path.join(OUT, "Figure_5_entropy_Br_M.png"))
    print("Figure 5 done")


# ---------------------------------------------------------------------------
# Figure 6 : Be(eta) for varying Rd and Br
# ---------------------------------------------------------------------------
def figure6():
    series = []
    combos = [("Rd", 0.2, 1.0), ("Rd", 1.0, 1.0), ("Br", 0.5, 0.5), ("Br", 1.5, 0.5)]
    labels = ["Rd=0.2", "Rd=1.0", "Br=0.5", "Br=1.5"]
    for i, (key, a, b) in enumerate(combos):
        if key == "Rd":
            pr, sol, u = solve_warm(Rd=a)
        else:
            pr, sol, u = solve_warm(Br=a)
        xs = [e for e, _ in sol]
        ys = [entropy_number(e, y, pr)[1] for e, y in sol]
        series.append({'x': xs, 'y': ys, 'label': labels[i], 'color': col(i)})
    plot(series, "eta", "Be(eta)", "Figure 6  Bejan number Be(eta) vs Rd and Br",
         os.path.join(OUT, "Figure_6_bejan_Rd_Br.png"), ylim=(0, 1))
    print("Figure 6 done")


# ---------------------------------------------------------------------------
# Figure 7 : Cf, Nu, Sh vs nanoparticle volume fraction phi (= phi1 = phi2)
# ---------------------------------------------------------------------------
def figure7():
    phis = [0.0, 0.01, 0.02, 0.03, 0.04, 0.05]
    Cf_list, Nu_list, Sh_list = [], [], []
    u = None
    for p in phis:
        pr = Params(phi1=p, phi2=p)
        sol, u = solve(pr, u0=u)
        Cf, Nu, Sh = engineering(sol, pr)
        Cf_list.append(Cf); Nu_list.append(Nu); Sh_list.append(Sh)
    series = [
        {'x': phis, 'y': Nu_list, 'label': "Re^-1/2 Nu", 'color': col(1)},
        {'x': phis, 'y': Sh_list, 'label': "Re^-1/2 Sh", 'color': col(2)},
        {'x': phis, 'y': Cf_list, 'label': "Re^1/2 Cf", 'color': col(0)},
    ]
    plot(series, "phi (volume fraction)", "value",
         "Figure 7  Cf, Nu, Sh vs volume fraction",
         os.path.join(OUT, "Figure_7_engineering_phi.png"), legend_loc='upper left')
    print("Figure 7 done")
    return phis, Cf_list, Nu_list, Sh_list


if __name__ == "__main__":
    figure1()
    figure2()
    figure3()
    figure4()
    figure5()
    figure6()
    figure7()
    print("All figures written to", OUT)
