import json, math
from multiprocessing import Pool
import compute_all as C

def spec(name, h, dt=0.00025, **kw):
    return dict(name=name, num=dict(p=2, h0=h, Lfine=2.5, Rout=2.5, grow=1.0, dt=dt, tend=0.3), props=dict(n=1.0, phi0=0.2))

if __name__ == "__main__":
    jobs = [spec("ref", 0.00625, 0.0001)] + [spec("h%g" % h, h) for h in (0.1, 0.05, 0.025, 0.0125)]
    outs = {o["name"]: o for o in Pool(5).map(C.run_case, jobs)}
    ref = outs["ref"]
    res = {}
    for k, o in outs.items():
        if k == "ref":
            continue
        e = C.errs_hist(o["cmp"][0], ref["cmp"][0])
        fe, fr = o["snaps"]["0.2"], ref["snaps"]["0.2"]
        idx = [i for i, r in enumerate(C.SAMPLE) if 0.2 <= r <= 1.2]
        p = [100 * C.rel([fe[i][j] for i in idx], [fr[i][j] for i in idx]) for j in range(4)]
        res[k] = dict(hist=e, prof=p, nn=o["nn"])
    R = json.load(open("results.json"))
    R["graded_conv"] = res
    json.dump(R, open("results.json", "w"))
    for k, v in res.items(): print(k, v["nn"], ["%.3g" % x for x in v["hist"]], ["%.3g" % x for x in v["prof"]])
