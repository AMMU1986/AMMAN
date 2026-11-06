"""SI-unit parameters of the layered tumour / normal-tissue pulsed-laser damage model.
Tissue data: Jangid, Singh, Mukhopadhyay, Math. Comput. Simul. 219 (2024) 404-423 (Tables 1-2).
Everything below is dimensional (m, s, K, Pa, W)."""
import math

RGAS = 8.314462618  # J/(mol K)

TISSUE = dict(
    cb=3770.0, rhob=1060.0, T0=310.0,
    tumour=dict(cv=2540.0, rho=1660.0, wb=0.009, alphaT=1e-4, k=0.778, kstar=17.0, lam=2.481e7, mu=1.034e6),
    normal=dict(cv=3720.0, rho=1000.0, wb=0.00018, alphaT=1e-4, k=0.642, kstar=16.0, lam=8.27e7, mu=3.446e6),
)
LASER = dict(g=0.9, mus=12000.0, mua=40.0, I0=3e5, Rd=0.05)


def laser_shape(las=LASER):
    Rd = las["Rd"]
    B1 = 3.09 + 5.44 * Rd - 2.12 * math.exp(-21.5 * Rd)
    B2 = 2.09 - 1.47 * Rd - 2.12 * math.exp(-21.5 * Rd)
    l1 = 1 - (1 - 1 / math.sqrt(3)) * math.exp(-20.1 * Rd)
    l2 = 1.63 * math.exp(3.4 * Rd)
    delta = 1.0 / math.sqrt(3 * las["mua"] * (las["mua"] + (1 - las["g"]) * las["mus"]))
    return dict(B1=B1, B2=B2, l1=l1, l2=l2, delta=delta)


def layer_coeffs(m, cb=TISSUE["cb"], rhob=TISSUE["rhob"], T0=TISSUE["T0"]):
    c11 = m["lam"] + 2 * m["mu"]
    beta = (3 * m["lam"] + 2 * m["mu"]) * m["alphaT"]
    C0 = m["rho"] * m["cv"]
    cpl = T0 * beta * beta / c11              # quasi-static thermoelastic heat-capacity increment
    return dict(c11=c11, beta=beta, C0=C0, cpl=cpl, C=C0 + cpl, k=m["k"], kstar=m["kstar"],
                om0=m["wb"] * rhob * cb, rho=m["rho"], mu=m["mu"], lam=m["lam"],
                sl=2 * m["mu"] * beta / c11,              # in-plane (laterally constrained) stress per kelvin
                cwave=math.sqrt(c11 / m["rho"]))


# Arrhenius sets (illustrative; see paper Section 3.3)
HM = dict(A=3.1e98, Ea=6.28e5)                    # Henriques-Moritz skin values, used as healthy-tissue proxy


def tumour_arrhenius(Ea=5.5e5, Tref=316.15, tref=3600.0):
    """A chosen so that the damage integral reaches 1 after tref seconds at Tref (43 C, 1 h)."""
    return dict(A=math.exp(Ea / (RGAS * Tref)) / tref, Ea=Ea)


def default():
    P = dict(
        L=0.020, h=0.004, T0=310.0,
        lay=[layer_coeffs(TISSUE["tumour"]), layer_coeffs(TISSUE["normal"])],
        las=dict(LASER), arr=[tumour_arrhenius(), dict(HM)],
        # perfusion law: omega/omega0 = (1 + cw*theta/10K) * S(theta)/S(0), S = (1 - tanh((theta-thc)/dth))/2
        cw=(0.5, 3.0), thc=(6.0, 9.0), dth=2.0, kv=0.0,
        tauq=0.0, tau0=0.0, tau1=1.0, kstar_on=False,
        Tvap=373.15, sig_lim=3.6e4, Ttreat=30.0, Teval=120.0, Om_c=math.log(100.0),
    )
    return P


MODELS = {
    "Pennes": dict(tauq=0.0, tau0=0.0, kstar_on=False),
    "CV": dict(tauq=2.0, tau0=0.0, kstar_on=False),
    "MGT": dict(tauq=2.0, tau0=0.0, kstar_on=True),
    "MGL": dict(tauq=0.0, tau0=2.0, kstar_on=False),
}


def make(model="MGL", **kw):
    P = default()
    P.update(MODELS[model])
    P["model"] = model
    for k, v in kw.items():
        P[k] = v
    return P


def perfusion_factor(P, i, th, Om):
    """omega/omega0 for layer i at temperature rise th (K) and damage integral Om."""
    S = lambda x: 0.5 * (1 - math.tanh((x - P["thc"][i]) / P["dth"]))
    v = (1 + P["cw"][i] * th / 10.0) * S(th) / S(0.0)
    if v < 0:
        v = 0.0
    if P["kv"]:
        v *= math.exp(-P["kv"] * min(Om, 50.0))
    return v


if __name__ == "__main__":
    print(laser_shape())
    for m in ("tumour", "normal"):
        print(m, layer_coeffs(TISSUE[m]))
    print(tumour_arrhenius())
