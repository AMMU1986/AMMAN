"""Stage B: optimisation runs.  usage: python3 stage_opt.py <chunk>   chunks: models pareto frontier sens"""
import json, sys, time
from multiprocessing import Pool
import opt

S1 = {}
S2 = {"normal_as_tumour": True}
NPS = (1, 2, 3, 4, 6, 8, 12)


def go(pool, name, ov, cov=1.0, nps=NPS, nstart=2):
    t = time.time()
    r = opt.run_case(pool, name, ov, cov=cov, nps=nps, nstart=nstart)
    b = r["best"]
    print("%-8s %-40s J=%.4f Np=%d I0=%.0f tp=%.2f per=%.2f minOm=%.3f Tmax=%.1f sabs=%.0f JF=%.4g viol=%s (%.0fs)" % (
        name, str(ov)[:40], b["J"], b["des"]["Np"], b["des"]["I0"], b["des"]["tp"], b["des"]["per"],
        b["m"]["minOmT"], b["m"]["Tmax"] - 273.15, b["m"]["sabs"], b["m"]["JF"] * 1e3, [round(x, 4) for x in b["v"]], time.time() - t), flush=True)
    return r


if __name__ == "__main__":
    chunk = sys.argv[1]
    out = {}
    with Pool(8) as pool:
        if chunk == "models":
            for sc, ov in (("S1", S1), ("S2", S2)):
                for name in ("Pennes", "CV", "MGT", "MGL"):
                    out[sc + "_" + name] = go(pool, name, ov)
        elif chunk == "pareto":
            for sc, ov in (("S1", S1), ("S2", S2)):
                for cov in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
                    out["%s_cov%.1f" % (sc, cov)] = go(pool, "MGL", ov, cov=cov, nps=(1, 2, 4, 8), nstart=1)
        elif chunk == "frontier":
            for tt in (10.0, 30.0, 60.0):
                for sl in (26e3, 28e3, 30e3, 32e3, 36e3):
                    out["T%g_S%g" % (tt, sl / 1e3)] = go(pool, "MGL", {"Ttreat": tt, "sig_lim": sl}, nps=(1, 2, 4, 8), nstart=1)
        elif chunk == "sens":
            cases = [
                ("base", {}),
                ("EaT=5.0e5", {"EaT": 5.0e5}), ("EaT=6.0e5", {"EaT": 6.0e5}),
                ("trefT=1800s", {"trefT": 1800.0}), ("trefT=7200s", {"trefT": 7200.0}),
                ("AfacN=10", {"AfacN": 10.0}), ("AfacN=0.1", {"AfacN": 0.1}),
                ("wbscale=0", {"wbscale": 0.0}), ("wbscale=3", {"wbscale": 3.0}), ("wbscale=10", {"wbscale": 10.0}),
                ("kv=1", {"kv": 1.0}), ("no vasodilation", {"cw": (0.0, 0.0)}),
                ("tau0=0.5", {"tau0": 0.5}), ("tau0=5", {"tau0": 5.0}), ("tau0=10", {"tau0": 10.0}),
                ("tau1=0", {"tau1": 0.0}), ("tau1=5", {"tau1": 5.0}), ("tau1=10", {"tau1": 10.0}),
                ("mua x0.8", {"mua": 32.0}), ("mua x1.25", {"mua": 50.0}),
                ("mus x0.8", {"mus": 9600.0}), ("mus x1.25", {"mus": 15000.0}),
                ("h=3mm", {"h": 0.003}), ("h=5mm", {"h": 0.005}),
                ("Teval=60s", {"Teval": 60.0}), ("Teval=300s", {"Teval": 300.0}),
            ]
            for tag, ov in cases:
                out[tag] = go(pool, "MGL", ov, nps=(1, 2, 4, 8), nstart=1)
                out[tag]["ov"] = {k: (list(v) if isinstance(v, tuple) else v) for k, v in ov.items()}
    json.dump(out, open("part_opt_%s.json" % chunk, "w"))
