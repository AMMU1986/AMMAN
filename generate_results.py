#!/usr/bin/env python3
"""
Driver that runs the stdlib solver across all parametric sweeps required for the
manuscript's 6 tables and 7 figures. Writes results_data.py (a plain-python
module of literals) consumed by make_figures.py and the docx builder.
"""

import math
from solve_fractional_disks import solve_case, base_params, SHAPE, tri_hybrid_properties


def run():
    data = {}

    # ---------- Figure 1: f'(eta) velocity vs alpha (fractional order) ----------
    data["fig1"] = {"eta": None, "curves": {}}
    for alpha in [1.0, 0.9, 0.7, 0.5]:
        p = base_params(); p["alpha"] = alpha
        r = solve_case(p, Nx=24)
        data["fig1"]["eta"] = r["eta"]
        data["fig1"]["curves"][alpha] = r["fp"]

    # ---------- Figure 2: theta(eta) vs gammaT (Cattaneo relaxation) ----------
    data["fig2"] = {"eta": None, "curves": {}}
    for g in [0.0, 0.3, 0.6, 0.9]:
        p = base_params(); p["gammaT"] = g
        r = solve_case(p, Nx=24)
        data["fig2"]["eta"] = r["eta"]
        data["fig2"]["curves"][g] = r["theta"]

    # ---------- Figure 3: f'(eta) vs second-grade beta ----------
    data["fig3"] = {"eta": None, "curves": {}}
    for beta in [0.1, 0.4, 0.8, 1.2]:
        p = base_params(); p["beta"] = beta
        r = solve_case(p, Nx=24)
        data["fig3"]["eta"] = r["eta"]
        data["fig3"]["curves"][beta] = r["fp"]

    # ---------- Figure 4: theta(eta) vs shape factor ----------
    data["fig4"] = {"eta": None, "curves": {}}
    for name, m in [("brick", SHAPE["brick"]), ("platelet", SHAPE["platelet"]),
                    ("blade", SHAPE["blade"])]:
        p = base_params(); p["m"] = m
        r = solve_case(p, Nx=24)
        data["fig4"]["eta"] = r["eta"]
        data["fig4"]["curves"][name] = r["theta"]

    # ---------- Figure 5: phi(eta) vs Soret number ----------
    data["fig5"] = {"eta": None, "curves": {}}
    for sr in [0.0, 0.05, 0.10, 0.15]:
        p = base_params(); p["Sr"] = sr
        r = solve_case(p, Nx=24)
        data["fig5"]["eta"] = r["eta"]
        data["fig5"]["curves"][sr] = r["phi"]

    # ---------- Figure 6: theta(eta) vs radiation Rd ----------
    data["fig6"] = {"eta": None, "curves": {}}
    for rd in [0.2, 0.6, 1.0, 1.5]:
        p = base_params(); p["Rd"] = rd
        r = solve_case(p, Nx=24)
        data["fig6"]["eta"] = r["eta"]
        data["fig6"]["curves"][rd] = r["theta"]

    # ---------- Figure 7: Nu1 vs alpha for three shapes (bar-style line) ----------
    data["fig7"] = {"alpha": [1.0, 0.9, 0.8, 0.7, 0.6, 0.5], "curves": {}}
    for name, m in [("brick", SHAPE["brick"]), ("platelet", SHAPE["platelet"]),
                    ("blade", SHAPE["blade"])]:
        ys = []
        for alpha in data["fig7"]["alpha"]:
            p = base_params(); p["m"] = m; p["alpha"] = alpha
            r = solve_case(p, Nx=24)
            ys.append(r["Nu1"])
        data["fig7"]["curves"][name] = ys

    # ---------- Table 2: effective property ratios for 3 shapes ----------
    data["tab2"] = []
    for name, m in [("brick", SHAPE["brick"]), ("blade", SHAPE["blade"]),
                    ("platelet", SHAPE["platelet"])]:
        A1, A2, A3, A4, A5 = tri_hybrid_properties(0.02, 0.02, 0.02, m)
        data["tab2"].append((name, m, A1, A2, A3, A4, A5))

    # ---------- Table 3: spatial (Nx) convergence of wall quantities ----------
    data["tab3"] = []
    for Nx in [8, 12, 16, 20, 24, 28]:
        p = base_params()
        r = solve_case(p, Nx=Nx)
        data["tab3"].append((Nx, r["fpp0"], r["Nu1"], r["Sh1"], r["iters"]))

    # ---------- Table 4: validation vs OHAM (alpha->1, gammaT->0) ----------
    # Reproduce the integer-order benchmark style: f''(1)-like values vs M, Sq.
    # We report -f''(0) proxy and compare to a reference analytic trend.
    data["tab4"] = []
    for M, Sq in [(0.0, 0.5), (1.0, 0.5), (4.0, 0.5), (9.0, 0.5),
                  (0.5, 0.2), (0.5, 0.5), (0.5, 1.0)]:
        p = base_params(); p["alpha"] = 1.0; p["gammaT"] = 0.0
        p["M"] = M; p["Sq"] = Sq
        r = solve_case(p, Nx=28)
        # present value
        present = r["Cf1"]
        data["tab4"].append((M, Sq, present))

    # ---------- Table 5: Skin friction & Nusselt vs fractional order alpha ----------
    data["tab5"] = []
    for alpha in [1.0, 0.9, 0.8, 0.7, 0.6, 0.5]:
        p = base_params(); p["alpha"] = alpha
        r = solve_case(p, Nx=24)
        data["tab5"].append((alpha, r["Cf1"], r["Cf2"], r["Nu1"], r["Nu2"]))

    # ---------- Table 6: Nu & Sh vs gammaT, Df, Sr ----------
    data["tab6"] = []
    for label, key, val in [
        ("gammaT", "gammaT", 0.0), ("gammaT", "gammaT", 0.3), ("gammaT", "gammaT", 0.6),
        ("Df", "Df", 0.05), ("Df", "Df", 0.10), ("Df", "Df", 0.15),
        ("Sr", "Sr", 0.05), ("Sr", "Sr", 0.10), ("Sr", "Sr", 0.15),
    ]:
        p = base_params(); p[key] = val
        r = solve_case(p, Nx=24)
        data["tab6"].append((label, val, r["Nu1"], r["Sh1"]))

    return data


def fmt(v):
    if isinstance(v, float):
        return repr(round(v, 8))
    return repr(v)


def write_module(data, path):
    with open(path, "w") as fh:
        fh.write("# Auto-generated numerical results. Do not edit by hand.\n")
        fh.write("DATA = ")
        fh.write(repr(data))
        fh.write("\n")


if __name__ == "__main__":
    print("Running all parametric sweeps (this takes ~1-2 minutes)...")
    d = run()
    write_module(d, "/projects/sandbox/AMMAN/results_data.py")
    print("Wrote results_data.py")
    # quick sanity printouts
    print("\nTable 5 (alpha sweep):")
    for row in d["tab5"]:
        print("  alpha=%.1f  Cf1=%.4f Cf2=%.4f Nu1=%.4f Nu2=%.4f" % row)
    print("\nTable 2 (shape property ratios):")
    for row in d["tab2"]:
        print("  %-9s m=%.2f A1=%.3f A4=%.3f" % (row[0], row[1], row[2], row[5]))
