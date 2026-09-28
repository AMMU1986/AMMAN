#!/usr/bin/env python3
"""
Pure-stdlib solver for the CORRECTED unsteady EMHD squeezing Carreau hybrid
nanofluid boundary-value problem (see DERIVATION_NOTES_Carreau_EMHD.md).

No numpy/scipy: RK4 integrator + multi-parameter Newton shooting.

State vector (8 first-order equations):
    y[0] = f
    y[1] = f'
    y[2] = f''
    y[3] = f'''
    y[4] = theta
    y[5] = theta'
    y[6] = phi
    y[7] = phi'

Fourth-order momentum (highest derivative f'''' solved from the differentiated,
pressure-eliminated x-momentum balance):

    P(f'') f'''' + P'(f'') (f''')^2 (via chain rule) ... handled by linearising in f''''
    + f f''' - f' f''
    - Sq( (3/2) f'' + (eta/2) f''' )
    - (A1/(A2 Da)) f''  - (A3/A2) M f''  - 2 Fr f' f''  = 0

where the Carreau prefactor is
    P(s) = (A1/A2) [1 + We^2 s^2]^{(n-3)/2} [1 + n We^2 s^2],  s = f''.
The eta-derivative of P(f'') f''' is P(f'') f'''' + P'(f'') f''' * f''', with
    P'(s) = dP/ds.
So the highest-derivative coefficient multiplying f'''' is exactly P(f''), and the
remaining P'(f'')(f''')^2 term is moved to the RHS.

Energy + species couple through Df (phi'' in energy) and Sr (theta'' in species);
theta'' and phi'' are obtained from a 2x2 linear solve at each step.
"""

import math

# ----------------------------------------------------------------------------
# Thermophysical property ratios (AA7072-AA7075 / methanol), Table 1 values.
# ----------------------------------------------------------------------------
PROPS = {
    "rho_f": 792.0,   "rho_s1": 2720.0,  "rho_s2": 2810.0,
    "cp_f": 2545.0,   "cp_s1": 893.0,    "cp_s2": 960.0,
    "k_f": 0.2035,    "k_s1": 222.0,     "k_s2": 173.0,
    "sig_f": 0.5e-6,  "sig_s1": 34.83e6, "sig_s2": 26.77e6,
}


def property_ratios(phi1, phi2, p=PROPS):
    """Return A1..A5 = mu, rho, sigma, kappa, (rho cp) ratios (hnf/f)."""
    # Viscosity (Brinkman)
    A1 = 1.0 / ((1 - phi1) ** 2.5 * (1 - phi2) ** 2.5)
    # Density
    rho_hnf = (1 - phi2) * ((1 - phi1) * p["rho_f"] + phi1 * p["rho_s1"]) + phi2 * p["rho_s2"]
    A2 = rho_hnf / p["rho_f"]
    # Heat capacity
    rc_f = p["rho_f"] * p["cp_f"]
    rc_hnf = (1 - phi2) * ((1 - phi1) * rc_f + phi1 * p["rho_s1"] * p["cp_s1"]) + phi2 * p["rho_s2"] * p["cp_s2"]
    A5 = rc_hnf / rc_f
    # Thermal conductivity (two-step Maxwell)
    kf, ks1, ks2 = p["k_f"], p["k_s1"], p["k_s2"]
    k_bf = kf * (ks1 + 2 * kf - 2 * phi1 * (kf - ks1)) / (ks1 + 2 * kf + phi1 * (kf - ks1))
    k_hnf = k_bf * (ks2 + 2 * k_bf - 2 * phi2 * (k_bf - ks2)) / (ks2 + 2 * k_bf + phi2 * (k_bf - ks2))
    A4 = k_hnf / kf
    # Electrical conductivity (two-step Maxwell-Garnett)
    sf, ss1, ss2 = p["sig_f"], p["sig_s1"], p["sig_s2"]
    s_bf = sf * (1 + 3 * (ss1 / sf - 1) * phi1 / ((ss1 / sf + 2) - (ss1 / sf - 1) * phi1))
    s_hnf = s_bf * (1 + 3 * (ss2 / s_bf - 1) * phi2 / ((ss2 / s_bf + 2) - (ss2 / s_bf - 1) * phi2))
    A3 = s_hnf / sf
    return A1, A2, A3, A4, A5


class Params:
    """Baseline parameter set (manuscript Section 4)."""
    def __init__(self, **kw):
        self.Sq = 0.5
        self.We = 1.0
        self.n = 1.5
        self.M = 1.0
        self.Ee = 0.2
        self.Da = 0.5
        self.Fr = 0.3
        self.Pr = 7.38
        self.Rd = 0.5
        self.Ec = 0.3
        self.Df = 0.2
        self.Sc = 1.2
        self.Sr = 0.2
        self.K = 0.5
        self.Bi = 1.0
        self.S1 = 0.1
        self.S3 = 0.1
        self.theta_r = 1.2
        self.phi1 = 0.03
        self.phi2 = 0.03
        # entropy groups
        self.Br = 1.0
        self.Omega = 1.0
        self.Lambda = 0.5
        self.zeta = 1.0
        for k, v in kw.items():
            setattr(self, k, v)
        self.refresh()

    def refresh(self):
        self.A1, self.A2, self.A3, self.A4, self.A5 = property_ratios(self.phi1, self.phi2)
        return self


def _carreau_P(s, pr):
    """Carreau momentum prefactor P(f'') and its derivative P'(f'')."""
    We2 = pr.We ** 2
    n = pr.n
    base = 1.0 + We2 * s * s
    P = (pr.A1 / pr.A2) * base ** ((n - 3) / 2.0) * (1.0 + n * We2 * s * s)
    # dP/ds
    d_base = 2.0 * We2 * s
    term1 = ((n - 3) / 2.0) * base ** ((n - 5) / 2.0) * d_base * (1.0 + n * We2 * s * s)
    term2 = base ** ((n - 3) / 2.0) * (2.0 * n * We2 * s)
    Pp = (pr.A1 / pr.A2) * (term1 + term2)
    return P, Pp


def rhs(eta, y, pr):
    """Right-hand side of the 8-variable first-order system."""
    f, fp, fpp, fppp, th, thp, ph, php = y

    # ----- momentum: solve for f'''' -----
    P, Pp = _carreau_P(fpp, pr)
    # d/deta[ P(f'') f''' ] = P f'''' + Pp * f''' * f'''  (since d f''/deta = f''')
    # Equation: P f'''' + Pp (f''')^2 + f f''' - f' f''
    #           - Sq((3/2) f'' + (eta/2) f''') - (A1/(A2 Da)) f''
    #           - (A3/A2) M f'' - 2 Fr f' f'' = 0
    A1, A2, A3 = pr.A1, pr.A2, pr.A3
    rest = (Pp * fppp * fppp
            + f * fppp - fp * fpp
            - pr.Sq * (1.5 * fpp + 0.5 * eta * fppp)
            - (A1 / (A2 * pr.Da)) * fpp
            - (A3 / A2) * pr.M * fpp
            - 2.0 * pr.Fr * fp * fpp)
    fpppp = -rest / P

    # ----- energy + species: 2x2 coupled solve for theta'' and phi'' -----
    F = 1.0 + (pr.theta_r - 1.0) * th
    a11 = pr.A4 + (4.0 / 3.0) * pr.Rd * F ** 3        # coeff of theta''
    a12 = pr.Pr * pr.A2 * pr.Df                        # coeff of phi'' in energy
    # energy RHS (everything except the theta'' and phi'' terms), moved to RHS:
    #  a11 theta'' + a12 phi'' = -[ 4 Rd(tr-1)F^2 (theta')^2 + A5 Pr(f theta' - Sq/2 eta theta')
    #                               + Pr( A1 Ec (f'')^2 (1+We^2 f''^2)^{(n-1)/2} + A3 M Ec (f'-Ee)^2 ) ]
    visc = pr.A1 * pr.Ec * fpp * fpp * (1.0 + pr.We ** 2 * fpp * fpp) ** ((pr.n - 1) / 2.0)
    joule = pr.A3 * pr.M * pr.Ec * (fp - pr.Ee) ** 2
    b1 = -(4.0 * pr.Rd * (pr.theta_r - 1.0) * F * F * thp * thp
           + pr.A5 * pr.Pr * (f * thp - 0.5 * pr.Sq * eta * thp)
           + pr.Pr * (visc + joule))
    # species:  phi'' + Sc(f phi' - Sq/2 eta phi') + Sc Sr theta'' - K Sc phi = 0
    #  => Sc Sr theta'' + 1 phi'' = -( Sc(f phi' - Sq/2 eta phi') - K Sc phi )
    a21 = pr.Sc * pr.Sr
    a22 = 1.0
    b2 = -(pr.Sc * (f * php - 0.5 * pr.Sq * eta * php) - pr.K * pr.Sc * ph)
    det = a11 * a22 - a12 * a21
    thpp = (b1 * a22 - a12 * b2) / det
    phpp = (a11 * b2 - b1 * a21) / det

    return [fp, fpp, fppp, fpppp, thp, thpp, php, phpp]


def rk4_integrate(y0, pr, N=400):
    """Integrate from eta=0 to eta=1 with N steps; return list of (eta, y)."""
    h = 1.0 / N
    y = list(y0)
    out = [(0.0, list(y))]
    eta = 0.0
    for i in range(N):
        k1 = rhs(eta, y, pr)
        k2 = rhs(eta + h / 2, [y[j] + h / 2 * k1[j] for j in range(8)], pr)
        k3 = rhs(eta + h / 2, [y[j] + h / 2 * k2[j] for j in range(8)], pr)
        k4 = rhs(eta + h, [y[j] + h * k3[j] for j in range(8)], pr)
        y = [y[j] + h / 6 * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]) for j in range(8)]
        eta += h
        out.append((eta, list(y)))
    return out


def _initial_state(unknowns, pr):
    """Build y(0) from the 4 unknown shooting parameters and the known BCs.
    Unknowns: u = [f''(0), f'''(0), theta(0), phi'(0)].
    Known at 0: f(0)=0; f'(0)=1+S1 f''(0); theta'(0)=-Bi(1-theta(0)); phi(0)=1+S3 phi'(0)."""
    fpp0, fppp0, th0, php0 = unknowns
    fp0 = 1.0 + pr.S1 * fpp0
    thp0 = -pr.Bi * (1.0 - th0)
    ph0 = 1.0 + pr.S3 * php0
    return [0.0, fp0, fpp0, fppp0, th0, thp0, ph0, php0]


def _residuals(unknowns, pr, N):
    """Residuals of the 4 far-wall BCs: f(1)=Sq/2, f'(1)=0, theta(1)=0, phi(1)=0."""
    y0 = _initial_state(unknowns, pr)
    sol = rk4_integrate(y0, pr, N)
    y1 = sol[-1][1]
    return [y1[0] - pr.Sq / 2.0, y1[1] - 0.0, y1[4] - 0.0, y1[6] - 0.0], sol


def solve(pr, N=400, tol=1e-9, maxit=80, u0=None):
    """Newton shooting on 4 unknowns. Returns (solution list, converged unknowns)."""
    # initial guess
    u = list(u0) if u0 is not None else [-1.0, -1.0, 0.5, -0.5]
    res, sol = _residuals(u, pr, N)
    for _ in range(maxit):
        nrm = math.sqrt(sum(r * r for r in res))
        if nrm < tol:
            break
        # numerical Jacobian (4x4)
        J = [[0.0] * 4 for _ in range(4)]
        for j in range(4):
            du = 1e-6 * (abs(u[j]) + 1e-3)
            up = list(u); up[j] += du
            rp, _ = _residuals(up, pr, N)
            for i in range(4):
                J[i][j] = (rp[i] - res[i]) / du
        # solve J d = -res  (Gaussian elimination, 4x4)
        d = _gauss_solve(J, [-r for r in res])
        # damped update
        lam = 1.0
        for _ls in range(20):
            un = [u[k] + lam * d[k] for k in range(4)]
            rn, sn = _residuals(un, pr, N)
            if math.sqrt(sum(r * r for r in rn)) < nrm:
                u, res, sol = un, rn, sn
                break
            lam *= 0.5
        else:
            u, res, sol = un, rn, sn
    return sol, u


def solve_continuation(base_kw, sweep_key, values, N=400):
    """Solve for a sequence of parameter values using the previous converged
    unknowns as the next initial guess (natural parameter continuation).
    Returns list of (value, solution, unknowns)."""
    results = []
    u = None
    for v in values:
        kw = dict(base_kw)
        kw[sweep_key] = v
        pr = Params(**kw)
        sol, u = solve(pr, N=N, u0=u)
        results.append((v, sol, u, pr))
    return results


def _gauss_solve(A, b):
    """Solve A x = b for small dense systems (partial pivoting)."""
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        if abs(pv) < 1e-30:
            pv = 1e-30
        for r in range(n):
            if r != c:
                fac = M[r][c] / pv
                for k in range(c, n + 1):
                    M[r][k] -= fac * M[c][k]
    return [M[i][n] / (M[i][i] if abs(M[i][i]) > 1e-30 else 1e-30) for i in range(n)]


# ----------------------------------------------------------------------------
# Derived fields for figures
# ----------------------------------------------------------------------------
def entropy_number(eta, y, pr):
    """Local dimensionless entropy generation number Ns and Bejan number Be."""
    f, fp, fpp, fppp, th, thp, ph, php = y
    F = 1.0 + (pr.theta_r - 1.0) * th
    N_HT = (pr.A4 + (4.0 / 3.0) * pr.Rd * F ** 3) * thp * thp
    N_FF = (pr.A1 * pr.Br / pr.Omega) * fpp * fpp * (1.0 + pr.We ** 2 * fpp * fpp) ** ((pr.n - 1) / 2.0)
    N_J = (pr.A3 * pr.Br * pr.M / pr.Omega) * (fp - pr.Ee) ** 2
    N_DD = pr.Lambda * (pr.zeta / pr.Omega) ** 2 * php * php + pr.Lambda * (pr.zeta / pr.Omega) * thp * php
    Ns = N_HT + N_FF + N_J + N_DD
    Be = (N_HT + N_DD) / Ns if Ns != 0 else 0.0
    return Ns, Be, (N_HT, N_FF, N_J, N_DD)


def engineering(sol, pr):
    """Reduced skin friction, Nusselt, Sherwood at the upper wall (eta=1)."""
    y1 = sol[-1][1]
    fpp1 = y1[2]
    thp1 = y1[5]
    php1 = y1[7]
    th1 = y1[4]
    Cf = pr.A1 * fpp1 * (1.0 + pr.We ** 2 * fpp1 * fpp1) ** ((pr.n - 1) / 2.0)
    Nu = -(pr.A4 + (4.0 / 3.0) * pr.Rd * (1.0 + (pr.theta_r - 1.0) * th1) ** 3) * thp1
    Sh = -php1
    return Cf, Nu, Sh


if __name__ == "__main__":
    pr = Params()
    sol, u = solve(pr)
    Cf, Nu, Sh = engineering(sol, pr)
    print("Converged unknowns [f''(0), f'''(0), theta(0), phi'(0)]:", u)
    print("f(1)=%.6f (target %.6f), f'(1)=%.2e, theta(1)=%.2e, phi(1)=%.2e"
          % (sol[-1][1][0], pr.Sq / 2, sol[-1][1][1], sol[-1][1][4], sol[-1][1][6]))
    print("Re^1/2 Cf = %.4f,  Re^-1/2 Nu = %.4f,  Re^-1/2 Sh = %.4f" % (Cf, Nu, Sh))
    Ns0, Be0, _ = entropy_number(0.0, sol[0][1], pr)
    print("Ns(0) = %.4f, Be(0) = %.4f" % (Ns0, Be0))
