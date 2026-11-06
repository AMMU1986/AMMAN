"""Parameters and dimensionless coefficients of the layered tumor/normal-tissue MGL bioheat model."""
import math

# ---- Table 1 / Table 2 of Jangid, Singh, Mukhopadhyay (2024), SI units ----
PHYS = dict(
    cb=3770.0, rhob=1060.0, T0=310.0,
    t=dict(cv=2540.0, rho=1660.0, wb=0.009, alphaT=1e-4, k0=0.778, kstar=17.0, lam=2.481e7, mu=1.034e6),
    n=dict(cv=3720.0, rho=1000.0, wb=0.00018, alphaT=1e-4, k0=0.642, kstar=16.0, lam=8.27e7, mu=3.446e6),
    g=0.9, mus=12000.0, mua=40.0, I0=3e5, Rd=0.05, dT=10.0)


def scales():
    P = PHYS
    t = P["t"]
    c11 = t["lam"] + 2 * t["mu"]
    nu = math.sqrt(c11 / t["rho"])
    l = t["k0"] / (t["rho"] * t["cv"] * nu)      # makes a4 = 1 in the tumour layer
    return dict(nu=nu, l=l, tl=l / nu, c11=c11)


def laser_shape():
    P = PHYS
    Rd = P["Rd"]
    B1 = 3.09 + 5.44 * Rd - 2.12 * math.exp(-21.5 * Rd)
    B2 = 2.09 - 1.47 * Rd - 2.12 * math.exp(-21.5 * Rd)
    l1 = 1 - (1 - 1 / math.sqrt(3)) * math.exp(-20.1 * Rd)
    l2 = 1.63 * math.exp(3.4 * Rd)
    delta = 1.0 / math.sqrt(3 * P["mua"] * (P["mua"] + (1 - P["g"]) * P["mus"]))
    return dict(B1=B1, B2=B2, l1=l1, l2=l2, delta=delta, deltas=delta / scales()["l"])


def coeffs():
    """Dimensionless layer coefficients a1..a9-type (source definitions), layer 1 = tumour, 2 = normal."""
    P = PHYS
    S = scales()
    t, n = P["t"], P["n"]
    l, nu, c11 = S["l"], S["nu"], S["c11"]
    beta = lambda m: (3 * m["lam"] + 2 * m["mu"]) * m["alphaT"]
    b1 = beta(t)
    out = []
    for m in (t, n):
        cm = m["lam"] + 2 * m["mu"]
        bm = beta(m)
        out.append(dict(
            rho=m["rho"] / t["rho"],                       # rho_hat
            a8=cm / c11,                                   # (lam+2mu)/(lam1+2mu1)
            a9=bm / b1,                                    # beta/beta1
            kappa=m["k0"] / t["k0"],
            C=m["rho"] * m["cv"] / (t["rho"] * t["cv"]),
            a5=P["T0"] * bm * b1 * l * nu / (t["k0"] * c11),
            a6=m["wb"] * P["rhob"] * P["cb"] * l * l / t["k0"],
            a3=m["kstar"] * l / (t["k0"] * nu),            # k* l/(k1 nu)
            a1=cm / (m["rho"] * nu * nu),
            a2=bm * c11 / (m["rho"] * nu * nu * b1),
            a4=m["rho"] * m["cv"] * l * nu / t["k0"],
            speed=math.sqrt(cm / m["rho"]) / nu))
    a7 = P["I0"] * P["mua"] * l * l / (t["k0"] * P["dT"])
    return out, a7


# ---- default numerical/illustrative parameters ----
BASE = dict(h=0.2, tau0=0.1, tau1=0.05, alpha=1.0, theta0=1.0,
            a6=None,            # (tumour, normal); None -> literal values
            cw=(0.0, 0.0), thc=(0.6, 0.9), dth=0.1, chi=(0.0, 0.0),
            a7=0.0, tp=0.2, model="MGL", taq=0.1)


def make(**kw):
    p = dict(BASE)
    p.update(kw)
    L, a7lit = coeffs()
    p["layers"] = [dict(x) for x in L]
    if p["a6"] is not None:
        p["layers"][0]["a6"], p["layers"][1]["a6"] = p["a6"]
    p["a7lit"] = a7lit
    return p


def wratio():
    L, _ = coeffs()
    return L[1]["a6"] / L[0]["a6"]


def omega(th, cw, thc, dth):
    S = lambda x: 0.5 * (1 - math.tanh((x - thc) / dth))
    v = (1 + cw * th) * S(th) / S(0.0)
    return v if v > 0 else 0.0


if __name__ == "__main__":
    print(scales())
    L, a7 = coeffs()
    for x in L:
        print({k: float("%.4g" % v) for k, v in x.items()})
    print("a7", a7, laser_shape(), wratio())
