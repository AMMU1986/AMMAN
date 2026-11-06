"""Compute all figure data (Figs 2-8) and validation metrics; writes results.json."""
import json
import time
import mgl

A = 0.01
TAU0 = 0.02
TAU1 = 0.05
TIMES = [0.005, 0.007, 0.009]
ALPHAS = [0.5, 0.75, 0.9, 1.0]
N = 4000
NW = 60


def grid(n, r0=A, r1=0.09):
    return [r0 + (r1 - r0) * i / (n - 1) for i in range(n)]


def run(geom, rs, t, alpha, tau1):
    f = mgl.sphere_fields if geom == "sphere" else mgl.cylinder_fields
    F = lambda s: f(s, rs, A, alpha, TAU0, tau1)
    full, _, _ = mgl.durbin(F, t, 4, len(rs), N=N, nwynn=NW)
    half, _, _ = mgl.durbin(F, t, 4, len(rs), N=N // 2, nwynn=NW)
    conv = []
    for k in range(4):
        scale = max(abs(full[i][k]) for i in range(len(rs)))
        diff = max(abs(full[i][k] - half[i][k]) for i in range(len(rs)))
        conv.append(diff / scale)
    npass = sum(1 for i in range(len(rs)) for k in range(4)
                if abs(full[i][k] - half[i][k]) <= 1e-6 * max(abs(full[i][k]), 1e-12))
    return dict(geom=geom, t=t, alpha=alpha, tau1=tau1, r=rs,
                theta=[x[0] for x in full], u=[x[1] for x in full],
                srr=[x[2] for x in full], spp=[x[3] for x in full],
                conv_rel=conv, frac_pointwise_1e6=npass / (4.0 * len(rs)))


def main():
    t0 = time.time()
    res = {"constants": mgl.constants(), "a": A, "tau0": TAU0, "tau1": TAU1,
           "N": N, "nwynn": NW, "runs": {}}
    rs = grid(321)
    for t in TIMES:
        res["runs"][f"sph_a1_t{t}"] = run("sphere", rs, t, 1.0, TAU1)
    for al in ALPHAS:
        res["runs"][f"sph_a{al}_t0.007"] = run("sphere", rs, 0.007, al, TAU1)
    for tau1 in (0.03, 0.08):
        res["runs"][f"sph_a1_t0.007_tau{tau1}"] = run("sphere", rs, 0.007, 1.0, tau1)
    res["runs"]["cyl_a1_t0.007"] = run("cylinder", grid(161), 0.007, 1.0, TAU1)
    # wall checks in the time domain for every run
    for k, v in res["runs"].items():
        v["theta_wall"] = v["theta"][0]
        v["srr_wall"] = v["srr"][0]
    res["elapsed_s"] = time.time() - t0
    with open("results.json", "w") as fh:
        json.dump(res, fh)
    for k, v in res["runs"].items():
        print(k, "theta(a)=%.10f srr(a)=%.2e conv=%s pass=%.3f" % (
            v["theta_wall"], v["srr_wall"], ["%.1e" % c for c in v["conv_rel"]],
            v["frac_pointwise_1e6"]))
    print(res["constants"], res["elapsed_s"])


if __name__ == "__main__":
    main()
