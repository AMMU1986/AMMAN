# -*- coding: utf-8 -*-
import json, os, math
import model

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))
EX = json.load(open(os.path.join(HERE, "extra.json")))
S = R["studies"]
L, A7 = model.coeffs()
SC = model.scales()
LS = model.laser_shape()
P = model.PHYS


def g(x, n=3):
    return ("%." + str(n) + "g") % x


def sci(x, n=2):
    m, e = ("%." + str(n) + "e") % x
    return x


def sc(x, n=2):
    s = ("%." + str(n) + "e") % x
    m, e = s.split("e")
    return "$%s\\times10^{%d}$" % (m, int(e))


def T1():
    t, n = P["t"], P["n"]
    rows = [["Quantity", "Tumour (1)", "Normal tissue (2)"],
            ["Specific heat $c_v$ (J/kg K)", g(t["cv"]), g(n["cv"])],
            ["Density $\\rho$ (kg/m³)", g(t["rho"]), g(n["rho"])],
            ["Blood perfusion rate $w_{b0}$ (1/s)", g(t["wb"]), g(n["wb"])],
            ["Thermal expansion $\\alpha_T$ (1/K)", "$10^{-4}$", "$10^{-4}$"],
            ["Conductivity $k_0$ (W/m K)", g(t["k0"]), g(n["k0"])],
            ["MGT parameter $k^{*}_0$ (W/m K s)", g(t["kstar"]), g(n["kstar"])],
            ["Lamé constant $\\lambda$ (kg/m s²)", sc(t["lam"], 3), sc(n["lam"], 3)],
            ["Lamé constant $\\mu$ (kg/m s²)", sc(t["mu"], 3), sc(n["mu"], 3)],
            ["Blood $c_b$, $\\rho_b$; reference $T_0$", "3770 J/kg K; 1060 kg/m³; 310 K", ""],
            ["Laser: $g$, $\\mu_s$, $\\mu_a$, $I_0$, $R_d$", "0.9; 12000 1/m; 40 1/m; $3\\times10^{5}$ W/m²; 0.05", ""],
            ["Derived: $\\nu$ (m/s), $l$ (m), $l/\\nu$ (s)", "%s; %s; %s" % (g(SC["nu"], 4), sc(SC["l"], 3), sc(SC["tl"], 3)), ""],
            ["Derived: optical depth $\\delta$ (m), $\\delta/l$", "%s; %s" % (sc(LS["delta"], 3), sc(LS["deltas"], 3)), ""]]
    return ("Material, laser and scale data (physical units; tumour and normal-tissue values from Table 1 and Table 2 of [13]; derived scales computed here). The reference temperature rise is taken as $T_\\infty-T_0=10$ K (illustrative choice).", rows, [3300, 2900, 2826])


def T2():
    a, b = L
    key = [("$\\hat\\rho=\\rho_i/\\rho_1$", "rho"), ("$a_8=(\\lambda+2\\mu)_i/(\\lambda_1+2\\mu_1)$", "a8"), ("$a_9=\\beta_i/\\beta_1$", "a9"),
           ("$\\hat\\kappa=k_{i0}/k_{10}$", "kappa"), ("$\\hat C=\\rho_ic_{vi}/(\\rho_1c_{v1})$", "C"), ("$a_1$", "a1"), ("$a_2$", "a2"),
           ("$a_3=k^{*}l/(k_1\\nu)$", "a3"), ("$a_4$", "a4"), ("$a_5$", "a5"), ("$a_6$ (literal perfusion)", "a6")]
    rows = [["Coefficient", "Tumour (1)", "Normal (2)"]]
    for lab, k in key:
        f = sc if (abs(a[k]) < 1e-2 or abs(a[k]) > 1e3) else (lambda v: g(v, 4))
        rows.append([lab, f(a[k]), f(b[k])])
    rows.append(["$a_7=I_0\\mu_al^2/(k_1\\Delta T)$ (literal laser)", sc(A7, 3), ""])
    rows.append(["$\\tau_0$, $\\tau_1$, $\\tau_p$, $\\theta_0$, $h$, $L$", "0.1, 0.05, 0.2, 1, 0.2, 1", ""])
    rows.append(["Perfusion law: $c_w$, $\\theta_c$, $\\Delta_c$", "0.5, 0.6, 0.1", "3, 0.9, 0.1"])
    rows.append(["Conductivity slope $\\chi_i$ (when active)", "0.2 to 0.3", "0"])
    return ("Dimensionless coefficients of the layered model computed from Table 1 and the illustrative model parameters used in the parametric studies. The literal perfusion and laser numbers $a_6$, $a_7$ are of order $10^{-13}$ and $10^{-12}$ because the length scale $l$ is of nanometre size.", rows, [4000, 2513, 2513])


def pct(x):
    v = 100 * x
    if v < 0.01:
        m, e = ("%.1e" % v).split("e")
        return "$%s\\times10^{%d}$" % (m, int(e))
    return "%.2g" % v


def T3():
    C = R["conv"]
    rows = [["Block", "Step", "$\\theta$ error", "$u$ error", "$\\sigma$ error", "Order ($u$)"]]

    def block(name, key, lab):
        d = C[key]
        for i, r in enumerate(d):
            od = "-" if i == 0 else "%.2f" % (math.log(d[i - 1][2] / r[2]) / math.log(d[i - 1][0] / r[0]))
            rows.append([name if i == 0 else "", ("%g" % r[0]), pct(r[1]) + "%", pct(r[2]) + "%", pct(r[3]) + "%", od])
    block("$\\Delta t$, Heaviside, $\\alpha=0.6$", "dt_H_a0.6", "")
    block("$\\Delta t$, smooth ramp, $\\alpha=0.6$", "dt_ramp_a0.6", "")
    block("$\\Delta t$, Heaviside, $\\alpha=1$", "dt_H_a1", "")
    block("$\\Delta x$, smooth ramp, $\\alpha=0.6$", "dx_ramp_a0.6", "")
    return ("Convergence of the finite element solution against the Laplace-domain reference at $t=0.4$, relative $L_2$ errors over 19 points $x=0.05,\\dots,0.95$ (blocks 1 to 3 at $\\Delta x=0.00125$; block 4 at $\\Delta t=0.0025$). The order is computed from the $u$ error.", rows, [2600, 900, 1250, 1250, 1250, 1100])


def T4():
    V = R["valid"]
    rows = [["Case", "$\\theta$ (%)", "$u$ (%)", "$\\sigma$ (%)"]]
    for k, lab in (("H_a1_t0.1", "$\\alpha=1$, $t=0.1$"), ("H_a1_t0.2", "$\\alpha=1$, $t=0.2$"), ("H_a1_t0.4", "$\\alpha=1$, $t=0.4$"), ("H_a1_t0.6", "$\\alpha=1$, $t=0.6$"),
                   ("H_a0.6_t0.1", "$\\alpha=0.6$, $t=0.1$"), ("H_a0.6_t0.2", "$\\alpha=0.6$, $t=0.2$"), ("H_a0.6_t0.4", "$\\alpha=0.6$, $t=0.4$"), ("H_a0.6_t0.6", "$\\alpha=0.6$, $t=0.6$"),
                   ("L_a0.7_t0.2", "laser only, $\\alpha=0.7$, $t=0.2$"), ("L_a0.7_t0.4", "laser only, $\\alpha=0.7$, $t=0.4$"), ("L_a0.7_t0.6", "laser only, $\\alpha=0.7$, $t=0.6$"),
                   ("pennes", "Pennes limit ($\\tau_0=\\tau_1=0$), $t=0.4$"), ("tau1_0", "$\\tau_1=0$, $\\alpha=0.8$, $t=0.4$")):
        v = V[k]
        rows.append([lab, pct(v["th"]), pct(v["u"]), pct(v["sg"])])
    for t in (0.1, 0.2, 0.4):
        v = EX["masked_t%g" % t]
        rows.append(["$\\alpha=1$, $t=%g$, fronts masked" % t, pct(v["th"]), pct(v["u"]), pct(v["sg"])])
    return ("Validation of the finite element solution ($\\Delta x=\\Delta t=0.0025$, Heaviside boundary data) against the independent Laplace-domain solution: relative $L_2$ errors over 19 points. Masked rows exclude points within 0.08 of the estimated thermal and elastic fronts (13 points remain).", rows, [4200, 1600, 1600, 1626])


def T5():
    rows = [["Case", "$\\theta(h,0.1)$", "$\\theta(h,0.3)$", "$\\theta(0.5,0.2)$", "$\\max|\\sigma(h,t)|$", "Picard its. (max)"]]
    hi = {"t10": 10, "t30": 30, "t20": 20}

    def add(lab, key):
        s = S[key]
        h = s["hist"]
        sg = max(abs(x[2]) for x in h[2])
        rows.append([lab, "%.3f" % h[2][10][0], "%.3f" % h[2][30][0], "%.3f" % h[4][20][0], "%.2f" % sg, str(s["iters_max"])])
    for lab, k in (("MGL, $\\alpha=1$ (base)", "base"), ("$\\alpha=0.9$", "alpha_0.9"), ("$\\alpha=0.75$", "alpha_0.75"), ("$\\alpha=0.6$", "alpha_0.6"), ("$\\alpha=0.45$", "alpha_0.45"), ("$\\alpha=0.3$", "alpha_0.3"),
                   ("$\\tau_1=0$ ($\\alpha=1$)", "tau1_0"), ("$\\tau_1=0.1$ ($\\alpha=1$)", "tau1_0.1"), ("$\\tau_1=0.2$ ($\\alpha=1$)", "tau1_0.2"),
                   ("$\\tau_0=0.05$ ($\\alpha=1$)", "tau0_0.05"), ("$\\tau_0=0.2$ ($\\alpha=1$)", "tau0_0.2"),
                   ("$h=0.1$ ($\\alpha=0.75$)", "h_0.1"), ("$h=0.3$ ($\\alpha=0.75$)", "h_0.3"), ("$h=0.4$ ($\\alpha=0.75$)", "h_0.4"),
                   ("$\\Pi=10$, constant $w_b$", "Pi_10_c0"), ("$\\Pi=10$, $w_b(\\theta)$", "Pi_10"), ("$\\Pi=20$, constant $w_b$", "Pi_20_c0"), ("$\\Pi=20$, $w_b(\\theta)$", "Pi_20"),
                   ("$\\Pi=10$, $4\\times$ stronger $c_w$", "cw_4"), ("$\\chi_1=0.3$", "chi"), ("$\\chi_1=0.3$, $\\Pi=10$, $w_b(\\theta)$", "chi_cw")):
        add(lab, k)
    return ("Parametric summary from the finite element solutions ($\\Delta x=\\Delta t=0.0025$). Unless stated, $\\alpha=0.75$ for the perfusion, conductivity and interface rows, $h=0.2$, $\\tau_0=0.1$, $\\tau_1=0.05$. $\\max|\\sigma(h,t)|$ is the largest stress magnitude at the tumour edge over $0\\le t\\le0.6$ and is front-limited (see text).", rows, [3300, 1100, 1100, 1200, 1300, 1026])
