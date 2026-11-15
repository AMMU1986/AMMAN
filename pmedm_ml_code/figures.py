#!/usr/bin/env python3
"""Draw Figures 1-9 of the manuscript from pmedm_ml_results/results.json."""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from data import load_confirmation, load_runs  # noqa: E402
from models import GPR, PURE_ERROR_SD_LOG  # noqa: E402
from svgplot import PALETTE, Axes, Figure  # noqa: E402

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "pmedm_ml_figures")
R = json.load(open(os.path.join(ROOT, "pmedm_ml_results", "results.json")))
ROWS = load_runs()
CONF = load_confirmation()
POW = ("graphite", "alumina", "none")
POW_LABEL = {"graphite": "Graphite", "alumina": "Alumina", "none": "No powder"}
POW_MARK = {"graphite": "o", "alumina": "^", "none": "s"}
SHORT = {"mean": "Mean", "taguchi": "TME", "powerlaw": "PL", "rsm": "RSM", "gpr": "GPR",
         "gpr_pe": "GPR-PE", "rf": "RF", "xgb": "XGB", "anfis2": "ANFIS-2", "anfis3": "ANFIS-3",
         "mcdrop": "MCD", "deepens": "DE"}


def fig1():
    f = Figure(1000, 640)

    def box(x, y, w, h, title, lines, fill="#eef3fa", stroke="#1f4e79"):
        f.rect(x, y, w, h, stroke=stroke, fill=fill, sw=1.4, rx=8)
        f.text(x + w / 2, y + 22, title, 14, anchor="middle", weight="700", color=stroke)
        for k, s in enumerate(lines):
            f.text(x + w / 2, y + 44 + 18 * k, s, 12, anchor="middle")

    def arrow(x1, y1, x2, y2):
        f.line(x1, y1, x2, y2, "#555", 1.6)
        ang = math.atan2(y2 - y1, x2 - x1)
        a1 = (x2 - 9 * math.cos(ang - 0.4), y2 - 9 * math.sin(ang - 0.4))
        a2 = (x2 - 9 * math.cos(ang + 0.4), y2 - 9 * math.sin(ang + 0.4))
        f.raw('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#555"/>'
              % (x2, y2, a1[0], a1[1], a2[0], a2[1]))

    box(30, 20, 440, 92, "1  Published data (anchor study)",
        ["L27 runs: t_off, t_on, current, powder; responses MRR, TWR",
         "+ 3 confirmation replicates at A2B3C1D3"])
    box(530, 20, 440, 92, "2  Consistency audit",
        ["GRA recomputed from raw MRR/TWR", "ANOVA, regression R², alias structure"],
        fill="#fbeee6", stroke="#c55a11")
    box(30, 150, 940, 72, "3  Leakage-free representation and validation",
        ["ln(y) targets · design-bound scaling · powder as a categorical factor · every fit,"
         " scaling and hyperparameter step inside the fold · LOO + 10 × 5-fold CV"])
    box(30, 262, 940, 92, "4  Surrogate models (12)",
        ["Null mean · Taguchi main effects · physics-guided power law · quadratic RSM",
         "GPR (Matérn-5/2 × powder kernel; also with replicate-error noise) · random forest · XGBoost-type GBT",
         ""], fill="#eef7ee", stroke="#548235")
    f.text(500, 343, "ANFIS (2 and 3 MF per input) · MC-dropout MLP · deep ensemble", 12,
           anchor="middle")
    box(30, 394, 300, 112, "5a  Uncertainty",
        ["GP and OLS predictive intervals", "MC dropout · deep ensemble",
         "jackknife+ conformal", "coverage, NLL, calibration"], fill="#f4eefa", stroke="#7030a0")
    box(350, 394, 300, 112, "5b  Explanation",
        ["exact interventional SHAP", "partial dependence", "versus main-effects ANOVA",
         "permutation tests of Q²"], fill="#f4eefa", stroke="#7030a0")
    box(670, 394, 300, 112, "5c  Decision",
        ["NSGA-II fronts: nominal and risk-aware", "TOPSIS (entropy, CRITIC weights)",
         "P(Pareto-optimal) over 81 settings", "MC-EHVI Bayesian optimization"],
        fill="#f4eefa", stroke="#7030a0")
    box(180, 546, 640, 74, "6  Outputs",
        ["Out-of-sample test of the published optimum A2B3C1D3",
         "and a ranked batch of next experiments"], fill="#fff7e0", stroke="#bf9000")
    arrow(250, 112, 250, 150)
    arrow(470, 66, 530, 66)
    arrow(500, 222, 500, 262)
    for xc in (180, 500, 820):
        arrow(xc, 354, xc, 394)
    for xc in (180, 500, 820):
        arrow(xc, 506, 500 + (xc - 500) * 0.45, 546)
    return f.save(os.path.join(OUT, "Figure_1_Workflow.png"))


def fig2():
    f = Figure(1000, 470)
    ax = Axes(f, 75, 40, 360, 360, (0, 14), (0.3, 1.9), "MRR (mm³/min)", "TWR (mm³/min)",
              "Measured responses of the 27 runs", panel="(a)")
    front = R["audit"]["observed_pareto_runs"]
    fr = sorted([r for r in ROWS if r["run"] in front], key=lambda r: r["mrr"])
    xs, ys = [], []
    for r in fr:
        xs.append(r["mrr"])
        ys.append(r["twr"])
    sx, sy = [xs[0]], [ys[0]]
    for a, b in zip(xs[1:], ys[1:]):
        sx += [a, a]
        sy += [sy[-1], b]
    ax.line(sx, sy, "#999", 1.4, dash="5,3")
    for p in POW:
        pts = [r for r in ROWS if r["powder"] == p]
        ax.scatter([r["mrr"] for r in pts], [r["twr"] for r in pts], PALETTE[p], 5.2, POW_MARK[p])
    ax.scatter([c["mrr"] for c in CONF], [c["twr"] for c in CONF], PALETTE["red"], 5.5, "D",
               hollow=True, sw=1.4)
    for r in fr:
        ax.text(r["mrr"], r["twr"], "run " + str(r["run"]), 10.5, dx=7, dy=-6)
    f.legend(ax.tx(2.4), ax.ty(1.83), [{"label": POW_LABEL[p], "color": PALETTE[p], "kind": POW_MARK[p]} for p in POW]
             + [{"label": "Confirmation runs", "color": PALETTE["red"], "kind": "D", "hollow": True},
                {"label": "Observed Pareto front", "color": "#999", "kind": "line", "dash": "5,3"}],
             size=11, row_h=17, col_w=175)
    # (b) main effects of ln(MRR) and ln(TWR)
    factors = [("A: t_off (µs)", 0, (10, 50, 75)), ("B: t_on (µs)", 1, (15, 50, 100)),
               ("C: powder", 3, (0, 1, 2)), ("D: current (A)", 2, (3, 6, 9))]
    x0, y0, w, h = 530, 40, 100, 150
    for row, (resp, lab, lim) in enumerate((("mrr", "MRR", (0, 10.5)), ("twr", "TWR", (0.6, 1.25)))):
        grand = sum(r[resp] for r in ROWS) / 27
        for col, (name, j, lv) in enumerate(factors):
            means = []
            for v in lv:
                g = [r[resp] for r in ROWS if (r["x"][j] == v)]
                means.append(sum(g) / len(g))
            ticks = {0: "G", 1: "Al", 2: "–"} if j == 3 else None
            pos = list(range(3))
            axm = Axes(f, x0 + col * (w + 12), y0 + row * (h + 62), w, h, (-0.4, 2.4), lim,
                       name if row == 1 else "", ("Mean " + lab) if col == 0 else "",
                       xticks=pos, xticklabels={k: (ticks[k] if ticks else str(lv[k])) for k in pos},
                       yticks=None if col == 0 else [], panel="(b)" if (row == 0 and col == 0) else None)
            axm.hline(grand, "#999", 1.0)
            axm.line(pos, means, PALETTE["graphite"] if resp == "mrr" else PALETTE["alumina"], 2.0)
            axm.scatter(pos, means, PALETTE["graphite"] if resp == "mrr" else PALETTE["alumina"], 4.2)
    f.text(530 + 2 * (w + 12), 26, "Main-effect level means (dashed line: grand mean)", 13,
           anchor="middle", weight="600")
    return f.save(os.path.join(OUT, "Figure_2_Data_Overview.png"))


def fig3():
    keys = ["powerlaw", "gpr", "xgb", "anfis3"]
    titles = {"powerlaw": "Physics-guided power law", "gpr": "GPR", "xgb": "XGBoost-type GBT",
              "anfis3": "ANFIS, 3 MF/input"}
    f = Figure(1000, 575)
    for row, (resp, lab, lim) in enumerate((("mrr", "MRR", (0, 20)), ("twr", "TWR", (0, 2.0)))):
        y = [r[resp] for r in ROWS]
        for col, k in enumerate(keys):
            e = R["cv"][resp][k]
            ax = Axes(f, 70 + col * 232, 40 + row * 262, 185, 175, lim, lim,
                      "Observed " + lab, ("LOO-predicted " + lab) if col == 0 else "",
                      titles[k] if row == 0 else "", panel=("(a)" if row == 0 else "(b)") if col == 0 else None)
            ax.diag()
            pred = [math.exp(z) for z in e["loo_pred"]]
            if "loo_dist" in e:
                lo, hi = [], []
                for d in e["loo_dist"]:
                    from models import interval
                    a, b = interval(tuple(d), 0.95)
                    lo.append(math.exp(a))
                    hi.append(math.exp(b))
                ax.errorbar(y, [ax.clip_y(p) for p in pred], lo, hi, "#b4c7e7", 0.9, 2)
            clipped = [ax.clip_y(p) for p in pred]
            for p in POW:
                idx = [i for i, r in enumerate(ROWS) if r["powder"] == p]
                ax.scatter([y[i] for i in idx], [clipped[i] for i in idx], PALETTE[p], 3.8, POW_MARK[p])
            m = e["loo"]
            f.rect(ax.x + 3, ax.y + 3, 96, 38, fill="white", opacity=0.9)
            ax.text(lim[0] + 0.04 * (lim[1] - lim[0]), lim[1] - 0.08 * (lim[1] - lim[0]),
                    "Q²(ln) = %.2f" % m["Q2_log"], 11.5)
            ax.text(lim[0] + 0.04 * (lim[1] - lim[0]), lim[1] - 0.17 * (lim[1] - lim[0]),
                    "RMSE = %.2f" % m["RMSE"], 11.5)
    f.legend(250, 560, [{"label": POW_LABEL[p], "color": PALETTE[p], "kind": POW_MARK[p]} for p in POW]
             + [{"label": "95% prediction interval", "color": "#b4c7e7", "kind": "line"}],
             size=11, cols=4, col_w=150, box=False)
    return f.save(os.path.join(OUT, "Figure_3_LOO_Parity.png"))


def gpr_pe_edof(resp):
    from data import log_targets
    xs = [r["x"] for r in ROWS]
    m = GPR(seed=7, n_starts=6, fixed_noise_sd_log=PURE_ERROR_SD_LOG[resp]).fit(xs, log_targets(ROWS, resp))
    return m.effective_dof()


def fig4():
    f = Figure(1000, 470)
    keys = ["mean", "taguchi", "powerlaw", "rsm", "gpr", "gpr_pe", "rf", "xgb", "anfis2", "anfis3",
            "mcdrop", "deepens"]
    # label offsets (dx, dy) in pixels; negative dx = label to the left of the point
    offsets = {
        "mrr": {"mean": (7, 4), "taguchi": (-7, 15), "powerlaw": (-7, -7), "rsm": (0, 19),
                "gpr": (-7, -8), "gpr_pe": (7, 15), "rf": (7, 4), "xgb": (-7, -8),
                "anfis2": (7, 4), "anfis3": (7, 4), "mcdrop": (7, 4), "deepens": (0, 19)},
        "twr": {"mean": (7, 4), "taguchi": (-7, 15), "powerlaw": (-7, 4), "rsm": (-7, -7),
                "gpr": (7, -8), "gpr_pe": (7, 15), "rf": (-7, -6), "xgb": (7, 4),
                "anfis2": (7, -3), "anfis3": (7, 4), "mcdrop": (7, 4), "deepens": (0, 19)},
    }
    complexity = {}
    for resp in ("mrr", "twr"):
        complexity[resp] = {}
        for k in keys:
            p = R["full"]["n_params"][k][resp]
            if k == "gpr":
                p = R["full"]["gpr_hyper"][resp]["edof"]
            if k == "gpr_pe":
                p = gpr_pe_edof(resp)
            complexity[resp][k] = p / 27.0
    R.setdefault("derived", {})["complexity_ratio"] = complexity
    for col, (resp, lab) in enumerate((("mrr", "ln MRR"), ("twr", "ln TWR"))):
        ax = Axes(f, 80 + col * 470, 40, 400, 330, (0.02, 200), (-1.6, 1.08),
                  "Parameter-to-sample ratio p/n (log scale)", "R² on the ln scale" if col == 0 else "",
                  lab, xlog=True, yticks=[-1.5, -1, -0.5, 0, 0.5, 1], panel="(a)" if col == 0 else "(b)")
        ax.hline(-0.078, "#c00000", 1.0)
        ax.text(190, -0.078, "null model, LOO Q² = -0.08", 10.5, anchor="end", color="#c00000", dy=-5)
        ax.hline(1.0, "#bbb", 0.8, "2,2")
        for k in keys:
            x = complexity[resp][k]
            tr = R["full"]["train_r2_log"][k][resp]
            q = R["cv"][resp][k]["loo"]["Q2_log"]
            qc = max(q, -1.55)
            ax.line([x, x], [tr, qc], "#bbb", 1.2)
            ax.scatter([x], [tr], "#555", 4.2, "o", hollow=True, sw=1.3)
            col_ = PALETTE["red"] if q < -0.078 else PALETTE["graphite"]
            ax.scatter([x], [qc], col_, 4.8, "v" if q < -1.55 else "o")
            off = offsets[resp][k]
            lab = SHORT[k] + (" (Q² = %.0f)" % q if q < -1.55 else "")
            anchor = "middle" if off[0] == 0 else ("end" if off[0] < 0 else "start")
            ax.text(x, qc, lab, 10.5, anchor=anchor, dx=off[0], dy=off[1])
    f.legend(250, 455, [{"label": "Training R² (all 27 runs)", "color": "#555", "kind": "o", "hollow": True},
                        {"label": "LOO Q² (better than null)", "color": PALETTE["graphite"], "kind": "o"},
                        {"label": "LOO Q² (worse than null)", "color": PALETTE["red"], "kind": "o"}],
             size=11, cols=3, col_w=215, box=False)
    return f.save(os.path.join(OUT, "Figure_4_Complexity_vs_Generalization.png"))


def fig5():
    f = Figure(1000, 500)
    series = [("gpr", "GPR", PALETTE["graphite"], None), ("powerlaw", "Power law (t)", PALETTE["teal"], None),
              ("mcdrop", "MC dropout", PALETTE["red"], None), ("deepens", "Deep ensemble", PALETTE["alumina"], None),
              ("jk+_gpr", "Jackknife+ (GPR)", PALETTE["purple"], "5,3"),
              ("jk+_xgb", "Jackknife+ (XGB)", PALETTE["gold"], "5,3")]
    levels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]
    for col, (resp, lab) in enumerate((("mrr", "MRR"), ("twr", "TWR"))):
        ax = Axes(f, 80 + col * 470, 40, 330, 330, (0, 1), (0, 1), "Nominal coverage",
                  "Observed LOO coverage" if col == 0 else "", lab, panel="(a)" if col == 0 else "(b)")
        ax.diag("#888", 1.0)
        for k, name, c, dash in series:
            cal = R["cv"][resp][k]["loo"]["calibration"]
            ys = [cal[str(l)] for l in levels]
            ax.line(levels, ys, c, 2.0, dash)
            ax.scatter(levels, ys, c, 3.0)
    f.legend(140, 458, [{"label": s[1], "color": s[2], "kind": "line", "dash": s[3]} for s in series],
             size=11, row_h=20, cols=3, col_w=250, box=False)
    return f.save(os.path.join(OUT, "Figure_5_Calibration.png"))


def fig6():
    f = Figure(1000, 420)
    order = [("A (t_off)", 0, "A: t_off"), ("B (t_on)", 1, "B: t_on"), ("C (powder)", 3, "C: powder"),
             ("D (current)", 2, "D: current")]
    for col, (resp, lab) in enumerate((("mrr", "ln MRR"), ("twr", "ln TWR"))):
        an = R["full"]["anova"][resp]["ln"]
        tot = sum(an[k]["pct"] for k, _, _ in order)
        anova = [100 * an[k]["pct"] / tot for k, _, _ in order]
        sg = R["full"]["shap"][resp]["gpr"]["share_pct"]
        sx = R["full"]["shap"][resp]["xgb"]["share_pct"]
        shap_g = [sg[j] for _, j, _ in order]
        shap_x = [sx[j] for _, j, _ in order]
        ax = Axes(f, 80 + col * 470, 40, 400, 290, (-0.5, 3.5), (0, 85), "",
                  "Share of attributed effect (%)" if col == 0 else "", lab, xticks=[0, 1, 2, 3],
                  xticklabels={i: order[i][2] for i in range(4)}, panel="(a)" if col == 0 else "(b)")
        for i in range(4):
            for k, (vals, c) in enumerate(((anova, "#7f7f7f"), (shap_g, PALETTE["graphite"]),
                                           (shap_x, PALETTE["gold"]))):
                x = i - 0.3 + 0.2 * k
                x1, x2 = ax.tx(x), ax.tx(x + 0.18)
                y1 = ax.ty(vals[i])
                f.rect(x1, y1, x2 - x1, ax.ty(0) - y1, stroke="#333", fill=c, sw=0.5)
                f.text((x1 + x2) / 2, y1 - 4, "%.0f" % vals[i], 9.5, anchor="middle")
            p = an[order[i][0]]["p"]
            ax.text(i, 80, "ANOVA p = %.3f" % p if p >= 0.001 else "ANOVA p < 0.001", 9.5,
                    anchor="middle", color="#555")
    f.legend(150, 395, [{"label": "Main-effects ANOVA (factor SS share)", "color": "#7f7f7f", "kind": "bar"},
                        {"label": "Exact SHAP, GPR", "color": PALETTE["graphite"], "kind": "bar"},
                        {"label": "Exact SHAP, XGB", "color": PALETTE["gold"], "kind": "bar"}],
             size=11, cols=3, col_w=290, box=False)
    return f.save(os.path.join(OUT, "Figure_6_SHAP_vs_ANOVA.png"))


def fig7():
    f = Figure(1000, 540)
    feats = [("A (t_off)", "Pulse-off time A (µs)", (10, 50, 75)),
             ("B (t_on)", "Pulse-on time B (µs)", (15, 50, 100)),
             ("D (current)", "Current D (A)", (3, 6, 9))]
    for row, (resp, lab, lim) in enumerate((("mrr", "MRR", (0, 16)), ("twr", "TWR", (0.5, 1.3)))):
        for col, (k, xl, lv) in enumerate(feats):
            d = R["full"]["pdp"][resp][k]
            g = d["grid"]
            ax = Axes(f, 80 + col * 305, 40 + row * 240, 250, 170, (g[0], g[-1]), lim,
                      xl if row == 1 else "", ("Partial dependence, " + lab) if col == 0 else "",
                      panel=("(a)" if row == 0 else "(b)") if col == 0 else None)
            for p in POW:
                ax.line(g, d["curves"][p], PALETTE[p], 2.0)
            ax.line(g, d["curves"]["average"], "#222", 1.6, dash="5,3")
            for v in lv:
                px = ax.tx(v)
                f.line(px, ax.y + ax.h - 7, px, ax.y + ax.h, "#222", 1.6)
    f.legend(250, 528, [{"label": POW_LABEL[p], "color": PALETTE[p], "kind": "line"} for p in POW]
             + [{"label": "Averaged over powders", "color": "#222", "kind": "line", "dash": "5,3"}],
             size=11, cols=4, col_w=150, box=False)
    return f.save(os.path.join(OUT, "Figure_7_Partial_Dependence.png"))


def fig8():
    f = Figure(1000, 545)
    opt = R["optimisation"]
    pub = opt["published_optimum"]["full_model"]
    zq = 1.6448536269514722
    for col, mode in enumerate(("nominal", "robust")):
        fr = opt["fronts"][mode]
        if mode == "nominal":
            ax = Axes(f, 80, 40, 380, 360, (0, 16), (0.3, 1.9), "MRR, posterior median (mm³/min)",
                      "TWR, posterior median (mm³/min)", "Nominal front (median predictions)", panel="(a)")
        else:
            ax = Axes(f, 570, 40, 380, 360, (0, 16), (0.3, 1.9), "MRR, 5% quantile (mm³/min)",
                      "TWR, 95% quantile (mm³/min)", "Risk-aware front (latent 90% bounds)", panel="(b)")
        ax.scatter([r["mrr"] for r in ROWS], [r["twr"] for r in ROWS], "#bdbdbd", 3.6, "o")
        for p_i, p in enumerate(POW):
            pts = [(-o[0], o[1]) for x, o in zip(fr["x"], fr["obj"]) if x[3] == p_i]
            if pts:
                ax.scatter([a for a, _ in pts], [b for _, b in pts], PALETTE[p], 2.6, POW_MARK[p],
                           edge=None)
        sel = opt["topsis_front"][mode]
        for w, c in (("entropy", PALETTE["gold"]), ("critic", PALETTE["purple"])):
            xsel = sel[w]["x"]
            k = min(range(len(fr["x"])), key=lambda i: sum((a - b) ** 2 for a, b in zip(fr["x"][i], xsel)))
            o = fr["obj"][k]
            ax.scatter([-o[0]], [o[1]], c, 6.0, "*")
        if mode == "nominal":
            ax.scatter([pub["mrr"]["median"]], [pub["twr"]["median"]], PALETTE["red"], 5.5, "s")
            label_pos = {1: (15.3, 1.10), 2: (11.4, 1.10), 3: (13.4, 1.20)}
            for s in R["bo"]["suggestions"]:
                px, py = s["pred"]["mrr"], s["pred"]["twr"]
                lx, ly = label_pos[s["step"]]
                f.line(ax.tx(px), ax.ty(py), ax.tx(lx), ax.ty(ly) + 4, PALETTE["teal"], 0.9)
                ax.scatter([px], [py], PALETTE["teal"], 5.0, "D")
                ax.text(lx, ly, "BO%d" % s["step"], 11, anchor="middle", color=PALETTE["teal"],
                        weight="600")
        else:
            mq = pub["mrr"]["median"] * math.exp(-zq * pub["mrr"]["latent_sd_log"])
            tq = pub["twr"]["median"] * math.exp(zq * pub["twr"]["latent_sd_log"])
            ax.scatter([mq], [tq], PALETTE["red"], 5.5, "s")
    f.legend(95, 488, [{"label": "Measured runs", "color": "#bdbdbd", "kind": "o"}]
             + [{"label": "Front: " + POW_LABEL[p], "color": PALETTE[p], "kind": POW_MARK[p]} for p in POW]
             + [{"label": "Published optimum A2B3C1D3", "color": PALETTE["red"], "kind": "s"},
                {"label": "TOPSIS, entropy weights", "color": PALETTE["gold"], "kind": "*"},
                {"label": "TOPSIS, CRITIC weights", "color": PALETTE["purple"], "kind": "*"},
                {"label": "BO batch (MC-EHVI)", "color": PALETTE["teal"], "kind": "D"}],
             size=11, cols=4, col_w=215, row_h=19)
    return f.save(os.path.join(OUT, "Figure_9_Pareto_Fronts.png"))


def fig9():
    tab = R["optimisation"]["level_combos"][:15]
    f = Figure(1000, 545)
    x0, y0, w, h = 190, 40, 620, 420
    ax = Axes(f, x0, y0, w, h, (0, 0.4), (-0.5, 14.5), "Posterior probability", "", "",
              yticks=[], xticks=[0, 0.1, 0.2, 0.3, 0.4])
    for i, r in enumerate(tab):
        yc = ax.ty(14 - i)
        bh = 11
        c = PALETTE["red"] if r["label"] == "A2B3C1D3" else PALETTE["graphite"]
        f.rect(ax.tx(0), yc - bh, ax.tx(r["p_pareto"]) - ax.tx(0), bh, fill=c, stroke="#333", sw=0.4)
        f.rect(ax.tx(0), yc + 1, ax.tx(r["p_gra_best"]) - ax.tx(0), bh - 2, fill=PALETTE["gold"],
               stroke="#333", sw=0.4)
        lab = r["label"] + ("  (run)" if r["observed"] else "")
        f.text(x0 - 10, yc + 4, lab, 12, anchor="end", weight="700" if r["label"] == "A2B3C1D3" else "normal")
        f.text(ax.tx(r["p_pareto"]) + 5, yc - 1, "%.2f" % r["p_pareto"], 10.5)
        f.text(x0 + w + 12, yc + 4, "%.1f / %.2f" % (r["mrr_median"], r["twr_median"]), 11)
    f.text(x0 + w + 12, y0 - 10, "Median MRR / TWR", 11.5, weight="600")
    f.legend(x0 + 20, y0 + h + 72, [{"label": "P(Pareto-optimal among the 81 level combinations)",
                                     "color": PALETTE["graphite"], "kind": "bar"},
                                    {"label": "P(best by grey relational grade)", "color": PALETTE["gold"],
                                     "kind": "bar"}], size=11, cols=2, col_w=380, box=False)
    return f.save(os.path.join(OUT, "Figure_8_Pareto_Probability.png"))


def main():
    os.makedirs(OUT, exist_ok=True)
    for fn in (fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9):
        print(fn())
    with open(os.path.join(ROOT, "pmedm_ml_results", "derived_complexity.json"), "w") as fh:
        json.dump(R.get("derived", {}), fh, indent=1)


if __name__ == "__main__":
    main()
