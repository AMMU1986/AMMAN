# -*- coding: utf-8 -*-
from vals import *

T = model.TISSUE


def T1():
    t, n = T["tumour"], T["normal"]
    a, b = LC
    rows = [["Quantity", "Tumour (layer 1)", "Normal tissue (layer 2)"],
            ["Geometry: $h$, $L$, $T_0$", "4 mm, 20 mm, 310 K", ""],
            ["Density $\\rho$ (kg/m³)", "1660", "1000"],
            ["Specific heat $c_v$ (J/kg K)", "2540", "3720"],
            ["Conductivity $k$ (W/m K)", "0.778", "0.642"],
            ["Thermal diffusivity (m²/s)", sc(t["k"] / a["C0"], 3), sc(n["k"] / b["C0"], 3)],
            ["Basal perfusion $w_b$ (1/s); $\\omega_0$ (W/m³ K)", "0.009; " + sc(a["om0"], 3), "0.00018; " + sc(b["om0"], 3)],
            ["Lamé $\\lambda$, $\\mu$ (Pa)", "$2.481\\times10^{7}$, $1.034\\times10^{6}$", "$8.27\\times10^{7}$, $3.446\\times10^{6}$"],
            ["$\\alpha_T$ (1/K); $\\beta$ (Pa/K)", "$10^{-4}$; " + k0(a["beta"]), "$10^{-4}$; " + k0(b["beta"])],
            ["$c_{11}$ (MPa); wave speed (m/s)", f1(a["c11"] / 1e6) + "; " + k0(a["cwave"]), f1(b["c11"] / 1e6) + "; " + k0(b["cwave"])],
            ["In-plane stress factor $s$ (Pa/K)", f1(a["sl"]), f1(b["sl"])],
            ["$T_0\\beta^2/c_{11}$ (J/m³ K)", f1(a["cpl"]), f1(b["cpl"])],
            ["Source $k^*$ (W/m K s) [13]; used (MGT) $\\eta k/\\tau_q$", "17; 0.195", "16; 0.161"],
            ["Perfusion law $c_w$; $\\theta_c$ (K); $\\Delta\\theta$ (K)", "0.5; 6; 2", "3; 9; 2"],
            ["Arrhenius $A$ (1/s)", sc(TUM["A"], 3) + " (illustrative)", "$3.1\\times10^{98}$ (Henriques–Moritz)"],
            ["Arrhenius $E_a$ (J/mol)", "$5.5\\times10^{5}$ (illustrative)", "$6.28\\times10^{5}$"],
            ["Time to $\\Omega=1$ at 50, 55, 60 °C (s)", f1(tdam(TUM, 50)) + ", " + f2(tdam(TUM, 55)) + ", " + f3(tdam(TUM, 60)),
             k0(tdam(HM, 50)) + ", " + f1(tdam(HM, 55)) + ", " + f2(tdam(HM, 60))],
            ["Blood $\\rho_b$, $c_b$", "1060 kg/m³, 3770 J/kg K", ""],
            ["Laser: $g$, $\\mu_s$, $\\mu_a$, $R_d$; $\\delta$", "0.9, 12000 1/m, 40 1/m, 0.05; " + f2(LS["delta"] * 1e3) + " mm", ""],
            ["Relaxation times (illustrative)", "$\\tau_q=\\tau_0=2$ s, $\\tau_1=1$ s, $\\eta=0.5$", ""],
            ["Limits", "$F_c=0.99$, $T_{\\mathrm{vap}}=100$ °C, $\\sigma_{\\lim}=36$ kPa, $t_{\\mathrm{treat,max}}=30$ s, $t_e=120$ s", ""]]
    return ("Input data. Tissue and laser data from [13] (SI units); Arrhenius, perfusion-law, relaxation-time and limit values are illustrative choices of this study, not measurements.", rows, [3000, 3013, 3013])


def T2():
    rows = [["Scenario, model", "$N_p$", "$t_p$ (s)", "$P$ (s)", "$I_0$ (kW/m²)", "$T_{\\max}$ (°C)", "$\\sigma_{\\max}$ (kPa)", "$F_N(h)$", "$J_F$ (mm)", "$J$"]]
    for sc_ in ("S1", "S2"):
        for nm in ("Pennes", "CV", "MGT", "MGL"):
            b = B1(nm, sc_); m = b["m"]; d = b["des"]
            rows.append([sc_ + ", " + nm, str(int(d["Np"])), f2(d["tp"]), f2(d["per"]), f1(d["I0"] / 1e3), f1(m["Tmax"] - 273.15),
                         f1(m["sabs"] / 1e3), f3(1 - math.exp(-m["OmN_h"])), f3(m["JF"] * 1e3), f3(b["J"])])
    return ("Optimal pulse-train designs found by the Nelder–Mead search for each conduction model in the selective scenario S1 (normal tissue with Henriques–Moritz kinetics) and the non-selective scenario S2 (normal tissue with tumour kinetics). All designs satisfy the kill, vaporization, stress and treatment-time constraints. $F_N(h)$ is the damage fraction on the normal side of the interface; $J_F$ is the integrated damage fraction in the normal tissue.",
            rows, [1450, 520, 780, 780, 900, 900, 950, 880, 880, 986])


def T3():
    rows = [["Model", "$\\min\\Omega_T$ at $s=1$", "$F_N(h)$ at $s=1$", "$T_{\\max}$ at $s=1$ (°C)", "$s^{*}$", "$J_F$ at $s^{*}$ (mm)", "$\\sigma_{\\max}$ at $s^{*}$ (kPa)", "$T_{\\max}$ at $s^{*}$ (°C)"]]
    for nm in ("Pennes", "CV", "MGT", "MGL"):
        c = C["common"][nm]
        u, s_ = c["unscaled"], c["scaled"]
        rows.append([nm, f2(u["minOmT"]), f3(1 - math.exp(-u["OmN_h"])), f1(u["Tmax"] - 273.15), f3(c["scale"]), f3(s_["JF"] * 1e3),
                     f1(s_["sabs"] / 1e3), f1(s_["Tmax"] - 273.15)])
    return ("Model comparison for the pulse train that is optimal under the Pennes model (S1: $N_p=" + str(int(pd_["Np"])) + "$, $t_p=" + f2(pd_["tp"]) + "$ s, $P=" + f2(pd_["per"]) + "$ s, $I_0=" + f1(pd_["I0"] / 1e3) + "$ kW/m²). Columns 2 to 4 give the response when the same pulse train is applied under each model; $s^*$ is the multiplier on $I_0$ that just satisfies the kill constraint, and the last three columns are evaluated at $s^*$.",
            rows, [1200, 1250, 1100, 1200, 900, 1150, 1226, 1000])


def T4():
    vv = V["valid"]
    mx = lambda nm, key, i0=1: max(vv[nm][key][i0:])
    rows = [["Check or case", "Setting or change", "Result"]]
    rows.append(["FE vs Laplace, temperature", "Pennes, CV, MGT, MGL; $t=3,6,12$ s; linear problem", "max relative error " + pct(max(mx(n, "eth") for n in vv), 2) + " %"])
    rows.append(["FE vs Laplace, in-plane stress", "same", "max relative error " + pct(max(mx(n, "esg") for n in vv), 2) + " %"])
    rows.append(["FE vs Laplace, early time", "$t=1$ s (pulse on)", "temperature " + pct(max(vv[n]["eth"][0] for n in vv), 2) + " %, stress " + pct(max(vv[n]["esg"][0] for n in vv), 2) + " %"])
    cl = V["conv_lap"]
    rows.append(["Time-step convergence", "$\\Delta t=0.32\\to0.02$ s, vs Laplace", "error " + sc(cl["Pennes"]["edt"][0], 1) + " to floor " + sc(cl["Pennes"]["edt"][-1], 1)])
    pr = V["prod"]
    rows.append(["Mesh convergence (pulse train)", "$\\Delta x=1\\to0.125$ mm", "$J_F$ error " + sc(pr["dx"][0][1][3], 1) + " to " + sc(pr["dx"][-1][1][3], 1) + "; order about 2"])
    rows.append(["Burn integral, constant $T$", "$\\Omega=A\\,t\\,e^{-E_a/RT}$, three temperatures", "relative error below " + sc(max(V["quad"]["const"]) * 1.0001, 1)])
    rr = V["quad"]["ramp"]["rows"]
    rows.append(["Burn integral, ramp", "0.5 K/s, 60 s, $\\Delta t=2.5$ s, $n_s=4$ Simpson", "error " + sc(rr[2][1][1], 1) + " (order 4); trapezoid " + sc(rr[2][1][3], 1)])
    en = V["energy"]
    rows.append(["Energy balance", "Pennes and MGL, linear and nonlinear perfusion", "residual " + sc(min(en[k]["rel_res"] for k in en if "CV" not in k), 1) + " to " + sc(max(en[k]["rel_res"] for k in en if "CV" not in k), 1) + " of $E_{\\mathrm{in}}$"])
    q = V["qs"]["rows"]
    rows.append(["Quasi-static limit", "inertia retained vs reduced density, $t=1$ to 12 s", "$\\Delta\\theta/\\theta_{\\max}\\le$ " + sc(max(r["dth"] for r in q), 1) + "; $|\\sigma_{xx}|/|\\sigma_\\parallel|\\le$ " + sc(max(r["ratio"] for r in q), 1)])
    rows.append(["Picard vs one pass", "five design metrics", "relative difference below " + sc(max(pr["picard"]), 1)])
    names = [("base", "Base optimum (MGL, S1)", "none"), ("EaT=5.0e5", "Tumour $E_a$", "$5.0\\times10^{5}$"), ("EaT=6.0e5", "Tumour $E_a$", "$6.0\\times10^{5}$"),
             ("trefT=1800s", "Tumour anchor time", "1800 s"), ("trefT=7200s", "Tumour anchor time", "7200 s"),
             ("AfacN=10", "Normal $A$", "$\\times10$"), ("AfacN=0.1", "Normal $A$", "$\\times0.1$"),
             ("wbscale=0", "Perfusion", "$\\times0$"), ("wbscale=10", "Perfusion", "$\\times10$"), ("kv=1", "Shutdown after damage", "$\\kappa_v=1$"),
             ("tau0=0.5", "$\\tau_0$", "0.5 s"), ("tau0=10", "$\\tau_0$", "10 s"), ("tau1=5", "$\\tau_1$", "5 s"), ("tau1=10", "$\\tau_1$", "10 s"),
             ("mua x0.8", "$\\mu_a$", "$\\times0.8$"), ("mua x1.25", "$\\mu_a$", "$\\times1.25$"), ("h=3mm", "Tumour thickness", "3 mm"), ("h=5mm", "Tumour thickness", "5 mm"),
             ("Teval=60s", "Horizon $t_e$", "60 s"), ("Teval=300s", "Horizon $t_e$", "300 s")]
    for k, par, ch in names:
        r = OS[k]["best"]
        feas = sum(r["v"]) < 1e-9
        rows.append(["Sensitivity: " + par, ch, "$J=$" + f3(r["J"]) + " (" + ("%+.0f" % (100 * (r["J"] / OS["base"]["best"]["J"] - 1))) + " %); $T_{\\max}=$" + f1(r["m"]["Tmax"] - 273.15) + " °C; $\\sigma_{\\max}=$" + f1(r["m"]["sabs"] / 1e3) + " kPa" + ("" if feas else "; stress limit violated by " + f1(100 * r["v"][2]) + " %")])
    return ("Verification results and one-at-a-time sensitivity of the optimum. Upper block: verification checks. Lower block: the collateral objective $J$ of the re-optimized MGL design (S1) when one input is changed; the percentage is the change relative to the base optimum $J=" + f3(OS["base"]["best"]["J"]) + "$.",
            rows, [2500, 2900, 3626])
