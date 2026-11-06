# -*- coding: utf-8 -*-
from cb import *
import fem

def T1():
    c = CONST
    rows = [["Quantity", "Symbol", "Value"],
            ["Lamé modulus", "$\\lambda_0$", "$7.76\\times10^{10}$ Pa"],
            ["Shear modulus", "$\\mu_0$", "$3.86\\times10^{10}$ Pa"],
            ["Thermal expansion coefficient", "$\\alpha_t$", "$1.78\\times10^{-5}$ K⁻¹"],
            ["Specific heat at constant strain", "$c_E$", "383.1 J kg⁻¹ K⁻¹"],
            ["Thermal conductivity", "$k_0$", "386 W m⁻¹ K⁻¹"],
            ["Density", "$\\rho_0$", "8954 kg m⁻³"],
            ["Reference temperature", "$T_0$", "293 K"],
            ["Thermal viscosity coefficient", "$\\eta$", g(c["eta"], 6) + " s m⁻²"],
            ["Longitudinal wave speed", "$c_0$", g(c["v"], 5) + " m s⁻¹"],
            ["Coupling constants", "$\\delta_1$, $\\delta_2$", g(c["d1"], 4) + ", " + g(c["d2"], 5)],
            ["Dimensionless parameters", "$\\epsilon$, $\\lambda_1$", g(c["eps"], 4) + ", " + g(c["lambda1"], 5)],
            ["Heat-flux relaxation time", "$\\tau_0$", "0.02"],
            ["Strain-rate relaxation time", "$\\tau_1$", "0.05"],
            ["Source radius, graded zone, domain", "$a$, $L_g$, $R_{out}$", "0.05, 1.0, 3.2"],
            ["Element size, time step", "$h$, $\\Delta t$", "0.0125, 0.0005"]]
    return ("Input data: reference (copper) properties of [1] and numerical parameters. Dimensionless values are in units of the scales of Eq. (@scale@).", rows, [3500, 2100, 3426])


def T2():
    pa = fem.Props(n=1.0).ratios(1e-6)
    pb = fem.Props(n=1.0, phi0=0.2).ratios(1e-6)
    pc = fem.Props(n=1.0, phi0=0.2).ratios(2.0)
    C = fem.CER
    al = lambda v: v + (1 - v) * C["alpha"]
    rows = [["Ratio", "Contrast phase $\\chi$", "Porosity factor", "$r\\to0$, $\\phi=0$", "$r\\to0$, $\\phi=0.2$", "$r\\ge L_g$, $\\phi=0.2$"],
            ["$\\hat\\lambda$", g(C["lam"], 2), "$(1-\\phi)^2$", fx(pa["lam"], 3), fx(pb["lam"], 3), fx(pc["lam"], 3)],
            ["$\\hat\\mu$", g(C["mu"], 2), "$(1-\\phi)^2$", fx(pa["mu"], 3), fx(pb["mu"], 3), fx(pc["mu"], 3)],
            ["$\\hat k$", g(C["k"], 2), "$(1-\\phi)^{3/2}$", fx(pa["k"], 3), fx(pb["k"], 4), fx(pc["k"], 4)],
            ["$\\hat\\rho$", g(C["rho"], 2), "$1-\\phi$", fx(pa["rho"], 3), fx(pb["rho"], 3), fx(pc["rho"], 3)],
            ["$\\hat\\alpha$", g(C["alpha"], 2), "1", fx(al(0.0), 3), fx(al(0.0), 3), fx(1.0, 3)],
            ["$\\hat\\rho\\hat c$", g(C["rho"] * C["c"], 2), "$1-\\phi$", fx(pa["rc"], 3), fx(pb["rc"], 3), fx(pc["rc"], 3)],
            ["$P$", "-", "-", fx(pa["P"], 3), fx(pb["P"], 3), fx(pc["P"], 3)],
            ["$L$", "-", "-", fx(pa["L"], 4), fx(pb["L"], 4), fx(pc["L"], 4)],
            ["$g$", "-", "-", fx(pa["g"], 3), fx(pb["g"], 3), fx(pc["g"], 3)]]
    return ("Property ratios of the contrast phase, porosity factors and effective ratios for the linear grading ($n=1$) at the source and in the far field.", rows, [1000, 1500, 1700, 1500, 1650, 1676])


def ray(pr, r1, n=3000):
    h = r1 / n
    return sum(h / pr.speed((i + 0.5) * h) for i in range(n))


def T3_data():
    cases = [("Reference ($n=0$)", "H0", {"n": 0}), ("$n=0.5$", "FG_n0.5", {"n": 0.5}), ("$n=1$", "FG_n1", {"n": 1.0}),
             ("$n=2$", "FG_n2", {"n": 2.0}), ("$n=5$", "FG_n5", {"n": 5.0}), ("exponential $\\beta=3$", "FG_exp3", dict(law="exp", beta=3.0)),
             ("$\\phi=0.2$ uniform", "P_0.2", {"phi0": 0.2}), ("$\\phi=0.3$ uniform", "P_0.3", {"phi0": 0.3}),
             ("$n=1$, $\\phi=0.2$", "FGP_n1_0.2", dict(n=1.0, phi0=0.2)), ("$n=1$, graded $\\phi_0=0.3$", "PG_0.3_n1", dict(n=1.0, phi0=0.3, pgrade=True))]
    out = []
    for lab, name, kw in cases:
        pr = fem.Props(**kw)
        out.append((lab, name, pr.speed(0.01), pr.speed(0.5), pr.speed(1.0), ray(pr, 0.3), arrival(name)))
    return out


def T3():
    rows = [["Medium", "$c(0)$", "$c(0.5)$", "$c(L_g)$", "Ray time to $r=0.3$", "FE arrival, $\\theta>0.005$"]]
    for lab, name, c0, c5, c1, tr, ta in T3_data():
        rows.append([lab, fx(c0, 3), fx(c5, 3), fx(c1, 3), fx(tr, 4), fx(ta, 4)])
    return ("Local wave speed from Eq. (@wave@), ray-theory travel time from the source to $r=0.3$ from Eq. (@travel@), and the time at which the computed temperature at $r=0.3$ first exceeds 0.005 (sampling interval 0.0025).", rows, [2600, 1000, 1000, 1000, 1700, 1726])


def T4():
    cv = R["conv"]
    rows = [["Series", "Parameter", "Nodes", "$E_\\theta$ (%)", "$E_u$ (%)", "$E_{\\sigma_{rr}}$ (%)", "$p_{obs}$ ($\\theta$)"]]
    def block(title, keys, par, fmt, hs):
        prev = None
        for k, h in zip(keys, hs):
            v = cv[k]
            e = v["hist"]
            o = "-" if prev is None or e[0] <= 0 else fx(math.log(prev[0] / e[0]) / math.log(prev[1] / h), 2)
            rows.append([title, fmt % h, str(v["nn"]), g(e[0], 3), g(e[1], 3), g(e[2], 3), o])
            prev = (e[0], h)
    block("P1, space", ["P1_h0.05", "P1_h0.025", "P1_h0.0125", "P1_h0.00625"], "h", "h = %g", [0.05, 0.025, 0.0125, 0.00625])
    block("P2, space", ["P2_h0.1", "P2_h0.05", "P2_h0.025", "P2_h0.0125"], "h", "h = %g", [0.1, 0.05, 0.025, 0.0125])
    block("P2, time", ["dt_0.005", "dt_0.0025", "dt_0.00125", "dt_0.000625", "dt_0.0003125"], "dt", "Δt = %g", [0.005, 0.0025, 0.00125, 0.000625, 0.0003125])
    return ("Self-convergence of the history at $r=0.3$ ($t=0.05$ to $0.3$): errors against the finest solutions of the same regularised problem (P2, $h=0.003125$, $\\Delta t=10^{-4}$ for space; P2, $h=0.0125$, $\\Delta t=3.1\\times10^{-5}$ for time) and observed orders from Eq. (@order@). Space series use $\\Delta t=2.5\\times10^{-4}$.", rows, [1400, 1500, 900, 1300, 1200, 1500, 1226])


def T5():
    V = R["valid"]
    f = lambda l: [g(x, 3) for x in l]
    rows = [["Case", "$E_\\theta$ (%)", "$E_u$ (%)", "$E_{\\sigma_{rr}}$ (%)", "$E_{\\sigma_{\\phi\\phi}}$ (%)"]]
    def add_(lab, l): rows.append([lab] + f(l))
    add_("Reference MGL, history at $r=0.3$", V["H0"]["hist"])
    add_("Reference MGL, history at $r=0.8$", V["H0"]["hist08"])
    add_("Reference MGL, profile at $t=0.2$", V["H0"]["prof"])
    add_("Lord–Shulman-type limit ($\\tau_1=0$), $r=0.3$", V["H_LS"]["hist"])
    add_("Classical limit ($\\tau_0=\\tau_1=0$), $r=0.3$", V["H_CTE"]["hist"])
    add_("Uniform porosity 0.2, MGL, $r=0.3$", V["P_0.2"]["hist"])
    add_("Uniform porosity 0.2, $\\tau_1=0$, $r=0.3$", V["U_P0.2_LS"]["hist"])
    add_("Uniform porosity 0.2, classical, $r=0.3$", V["U_P0.2_CTE"]["hist"])
    add_("Uniform contrast phase, MGL, $r=0.3$", V["U_cer"]["hist"])
    add_("Uniform contrast phase, MGL, profile", V["U_cer"]["prof"])
    for nm, e1, e2 in R["reg"]:
        add_("Source radius $a=%s$ vs exact, $r=0.3$" % nm.split("_")[1], e1)
    add_("Laplace-domain FE vs time-domain FE ($n=1$, $\\phi=0.2$), $r=0.3$", R["laplace_L2"][0])
    add_("Laplace-domain FE vs time-domain FE ($n=1$, $\\phi=0.2$), $r=0.8$", R["laplace_L2"][1])
    return ("Validation errors (relative $L^2$, per cent, Eq. (@err@)) of the finite element solution against the exact solution of Section 4 for uniform media, and of the time-domain against the Laplace-domain finite element solution for the graded porous medium.", rows, [4026, 1250, 1250, 1250, 1250])


def T6():
    labs = [("H0", "Reference ($n=0$)"), ("FG_n0.5", "$n=0.5$"), ("FG_n1", "$n=1$"), ("FG_n2", "$n=2$"), ("FG_n5", "$n=5$"),
            ("FG_exp3", "Exponential $\\beta=3$"), ("P_0.1", "$\\phi=0.1$"), ("P_0.2", "$\\phi=0.2$"), ("P_0.3", "$\\phi=0.3$"),
            ("PG_0.3_n1", "Graded $\\phi_0=0.3$, $n=1$"), ("FGP_n1_0.2", "$n=1$, $\\phi=0.2$"),
            ("FG_t1_0", "$n=1$, $\\tau_1=0$"), ("FG_t1_0.02", "$n=1$, $\\tau_1=0.02$"), ("FG_t1_0.1", "$n=1$, $\\tau_1=0.1$"),
            ("FG_t0_0", "$n=1$, $\\tau_0=0$"), ("FG_t0_0.01", "$n=1$, $\\tau_0=0.01$"), ("FG_t0_0.04", "$n=1$, $\\tau_0=0.04$")]
    rows = [["Case", "$\\theta(0.3)$", "$10^4u(0.3)$", "$10^3\\sigma_{rr}(0.3)$", "$10^3\\sigma_{\\phi\\phi}(0.3)$", "$10^3\\max|\\sigma_{rr}|$", "$\\theta(0.8)$"]]
    for name, lab in labs:
        rows.append([lab, fx(at(name, 0, 0, 0.3), 4), fx(1e4 * at(name, 0, 1, 0.3), 3), fx(1e3 * at(name, 0, 2, 0.3), 3),
                     fx(1e3 * at(name, 0, 3, 0.3), 3), fx(1e3 * abs(peak_abs(name, 0, 2)[0]), 3), fx(at(name, 1, 0, 0.3), 4)])
    return ("Parametric summary at $t=0.3$ (observation radius $r=0.3$ unless stated; the peak stress is the largest magnitude over $0\\le t\\le0.3$ at $r=0.3$). Unlisted parameters have the base values $\\tau_0=0.02$, $\\tau_1=0.05$.", rows, [2126, 950, 1050, 1250, 1400, 1300, 950])


def T7():
    rows = [["Theory", "Medium", "Thermal front", "Elastic front", "$\\theta(0.3)$", "$10^3\\sigma_{rr}(0.3)$", "$10^3\\max|\\sigma_{rr}|$"]]
    th = [("Classical ($\\tau_0=\\tau_1=0$)", "none (parabolic)", "yes", "CTE"), ("Lord–Shulman-type ($\\tau_1=0$)", "finite, $c$", "yes", "LS"), ("MGL", "finite, $c$", "no (damped)", "MGL")]
    names = {"CTE": ("H_CTE", "FGP_CTE"), "LS": ("H_LS", "FGP_LS"), "MGL": ("H0", "FGP_n1_0.2")}
    for lab, tf, ef, key in th:
        for mi, med in enumerate(("homogeneous", "$n=1$, $\\phi=0.2$")):
            nm = names[key][mi]
            rows.append([lab, med, tf, ef, fx(at(nm, 0, 0, 0.3), 4), fx(1e3 * at(nm, 0, 2, 0.3), 3), fx(1e3 * abs(peak_abs(nm, 0, 2)[0]), 3)])
    return ("Comparison of the theories computed with the same finite element code. The qualitative wave content is the classical result for each theory; numbers are computed at $r=0.3$.", rows, [1900, 1300, 1250, 1050, 1000, 1250, 1276])
