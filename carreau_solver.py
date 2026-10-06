#!/usr/bin/env python3
"""
Pure-standard-library solver for the unsteady EMHD Carreau hybrid-nanofluid
squeezing-flow BVP (fourth-order momentum + 2nd-order energy + 2nd-order species).

No numpy/scipy. Uses:
  - fixed-step RK4 integration of the first-order state vector (length 8),
  - multi-parameter Newton shooting to satisfy the right-wall conditions,
  - finite-difference Jacobian.

State vector y = [f, f', f'', f''', theta, theta', phi, phi'].

Momentum (fourth order), from manuscript Eq. (29):
  (a_mu/a_rho) d/deta{ B(f'') f''' } + f f''' - f' f''
     - Sq( 1.5 f'' + 0.5 eta f''' ) - (a_mu/(a_rho Da)) f''
     - (a_sigma/a_rho) M f'' - 2 Fr f' f'' = 0
  with B(f'') = [1 + We^2 f''^2]^((n-3)/2) [1 + n We^2 f''^2].

We solve for f'''' (= y3') analytically from d/deta{ B f''' }:
  d/deta{ B f''' } = B f'''' + B'(f'') f'''^2 ,   B'(u) = dB/du evaluated at u=f''.

Energy & species solved as coupled 2x2 for (theta'', phi'') -- manuscript Eq. (61).

Boundary conditions (Eq. 36-37):
  f(0)=0, f'(0)=1+S1 f''(0), f(1)=Sq/2, f'(1)=0
  theta'(0)=-Bi[1-theta(0)], theta(1)=0, phi(0)=1+S3 phi'(0), phi(1)=0
"""

import math

# ----------------------------------------------------------------------
# Hybrid-nanofluid property ratios (AA7072-AA7075 / methanol)
# ----------------------------------------------------------------------
def properties(phi1, phi2):
    # base fluid: methanol; solids: AA7072, AA7075 (alloys ~ aluminium)
    rho_f, cp_f, k_f, sig_f = 792.0, 2545.0, 0.2035, 5.0e-6
    rho_s1, cp_s1, k_s1, sig_s1 = 2720.0, 893.0, 222.0, 3.5e7
    rho_s2, cp_s2, k_s2, sig_s2 = 2810.0, 960.0, 173.0, 2.6e7

    a_mu = 1.0 / ((1 - phi1) ** 2.5 * (1 - phi2) ** 2.5)

    rho_hnf = (1 - phi2) * ((1 - phi1) * rho_f + phi1 * rho_s1) + phi2 * rho_s2
    a_rho = rho_hnf / rho_f

    rcp_f = rho_f * cp_f
    rcp_hnf = (1 - phi2) * ((1 - phi1) * rcp_f + phi1 * rho_s1 * cp_s1) + phi2 * rho_s2 * cp_s2
    a_c = rcp_hnf / rcp_f

    # two-step Maxwell for conductivity
    k_bf = k_f * (k_s1 + 2 * k_f - 2 * phi1 * (k_f - k_s1)) / (k_s1 + 2 * k_f + phi1 * (k_f - k_s1))
    k_hnf = k_bf * (k_s2 + 2 * k_bf - 2 * phi2 * (k_bf - k_s2)) / (k_s2 + 2 * k_bf + phi2 * (k_bf - k_s2))
    a_k = k_hnf / k_f

    # two-step Maxwell-Garnett for electrical conductivity
    s_bf = sig_f * (1 + 3 * ((sig_s1 / sig_f) - 1) * phi1 /
                    (((sig_s1 / sig_f) + 2) - ((sig_s1 / sig_f) - 1) * phi1))
    s_hnf = s_bf * (1 + 3 * ((sig_s2 / s_bf) - 1) * phi2 /
                    (((sig_s2 / s_bf) + 2) - ((sig_s2 / s_bf) - 1) * phi2))
    a_sig = s_hnf / sig_f
    return dict(a_mu=a_mu, a_rho=a_rho, a_c=a_c, a_k=a_k, a_sig=a_sig)


DEFAULT = dict(Sq=0.5, We=1.0, n=1.5, M=1.0, Ee=0.2, Da=0.5, Fr=0.3,
               Pr=7.38, Rd=0.5, Ec=0.3, Df=0.2, Sc=1.2, Sr=0.2, K=0.5,
               Bi=1.0, S1=0.1, S3=0.1, thr=1.2, phi1=0.03, phi2=0.03)


def rhs(eta, y, P, props):
    f, fp, fpp, fppp, th, thp, ph, php = y
    a_mu, a_rho, a_c = props['a_mu'], props['a_rho'], props['a_c']
    a_k, a_sig = props['a_k'], props['a_sig']
    We, n, Sq = P['We'], P['n'], P['Sq']
    M, Ee, Da, Fr = P['M'], P['Ee'], P['Da'], P['Fr']
    Pr, Rd, Ec, Df = P['Pr'], P['Rd'], P['Ec'], P['Df']
    Sc, Sr, K, thr = P['Sc'], P['Sr'], P['K'], P['thr']

    # Carreau bracket B(u) and derivative B'(u), u = fpp
    u = fpp
    w2 = We * We * u * u
    base = 1.0 + w2
    Bc = base ** ((n - 3) / 2.0) * (1.0 + n * w2)
    # dB/du
    d_base = 2.0 * We * We * u
    term1 = ((n - 3) / 2.0) * base ** ((n - 5) / 2.0) * d_base * (1.0 + n * w2)
    term2 = base ** ((n - 3) / 2.0) * (2.0 * n * We * We * u)
    Bp = term1 + term2  # dB/d(fpp)

    # momentum: (a_mu/a_rho)[Bc*fpppp + Bp*fppp^2] + f*fppp - fp*fpp
    #   - Sq(1.5 fpp + 0.5 eta fppp) - (a_mu/(a_rho Da)) fpp
    #   - (a_sig/a_rho) M fpp - 2 Fr fp*fpp = 0
    coef = (a_mu / a_rho) * Bc
    rest = ((a_mu / a_rho) * Bp * fppp * fppp
            + f * fppp - fp * fpp
            - Sq * (1.5 * fpp + 0.5 * eta * fppp)
            - (a_mu / (a_rho * Da)) * fpp
            - (a_sig / a_rho) * M * fpp
            - 2.0 * Fr * fp * fpp)
    fpppp = -rest / coef

    # energy/species coupled 2x2 (Eq. 61)
    F = 1.0 + (thr - 1.0) * th
    Kr = a_k + (4.0 / 3.0) * Rd * F ** 3
    b1 = -(4.0 * Rd * (thr - 1.0) * F * F * thp * thp
           + a_c * Pr * (f * thp - fp * th - Sq * th - 0.5 * Sq * eta * thp)
           + Pr * (a_mu * Ec * fpp * fpp * base ** ((n - 1) / 2.0)
                   + a_sig * M * Ec * (fp - Ee) ** 2))
    b2 = -(Sc * (f * php - fp * ph - Sq * ph - 0.5 * Sq * eta * php)) + K * Sc * ph
    # [[Kr, Pr a_rho Df],[Sc Sr, 1]] [th'';ph''] = [b1;b2]
    det = Kr * 1.0 - (Pr * a_rho * Df) * (Sc * Sr)
    thpp = (b1 * 1.0 - (Pr * a_rho * Df) * b2) / det
    phpp = (Kr * b2 - (Sc * Sr) * b1) / det

    return [fp, fpp, fppp, fpppp, thp, thpp, php, phpp]


def rk4(P, props, s, N=400):
    """Integrate 0->1 with unknowns s=[fpp0, fppp0, th0, phi_p0]."""
    Sq, Bi, S1, S3 = P['Sq'], P['Bi'], P['S1'], P['S3']
    fpp0, fppp0, th0, php0 = s
    # apply left BCs
    f0 = 0.0
    fp0 = 1.0 + S1 * fpp0           # f'(0)=1+S1 f''(0)
    thp0 = -Bi * (1.0 - th0)        # theta'(0) = -Bi[1-theta(0)]
    ph0 = 1.0 + S3 * php0           # phi(0)=1+S3 phi'(0)
    y = [f0, fp0, fpp0, fppp0, th0, thp0, ph0, php0]
    h = 1.0 / N
    eta = 0.0
    traj = [(eta, list(y))]
    for i in range(N):
        k1 = rhs(eta, y, P, props)
        y2 = [y[j] + 0.5 * h * k1[j] for j in range(8)]
        k2 = rhs(eta + 0.5 * h, y2, P, props)
        y3 = [y[j] + 0.5 * h * k2[j] for j in range(8)]
        k3 = rhs(eta + 0.5 * h, y3, P, props)
        y4 = [y[j] + h * k3[j] for j in range(8)]
        k4 = rhs(eta + h, y4, P, props)
        y = [y[j] + (h / 6.0) * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]) for j in range(8)]
        eta += h
        traj.append((eta, list(y)))
    return y, traj


def residual(P, props, s, N=400):
    yend, _ = rk4(P, props, s, N)
    f, fp, fpp, fppp, th, thp, ph, php = yend
    Sq = P['Sq']
    # right BCs: f(1)=Sq/2, f'(1)=0, theta(1)=0, phi(1)=0
    return [f - Sq / 2.0, fp - 0.0, th - 0.0, ph - 0.0]


def solve(P, props, s0=None, N=400, tol=1e-9, maxit=60):
    if s0 is None:
        s0 = [P['Sq'], -P['Sq'], 0.6, -0.5]
    s = list(s0)
    for it in range(maxit):
        R = residual(P, props, s, N)
        nrm = math.sqrt(sum(r * r for r in R))
        if nrm < tol:
            break
        # finite-difference Jacobian (4x4)
        J = [[0.0] * 4 for _ in range(4)]
        for j in range(4):
            ds = 1e-7 * (1.0 + abs(s[j]))
            sp = list(s); sp[j] += ds
            Rp = residual(P, props, sp, N)
            for i in range(4):
                J[i][j] = (Rp[i] - R[i]) / ds
        # solve J dx = -R by Gaussian elimination
        dx = gauss(J, [-r for r in R])
        # damped update
        lam = 1.0
        for _ in range(20):
            cand = [s[k] + lam * dx[k] for k in range(4)]
            Rc = residual(P, props, cand, N)
            if math.sqrt(sum(r * r for r in Rc)) < nrm:
                s = cand
                break
            lam *= 0.5
        else:
            s = [s[k] + dx[k] for k in range(4)]
    yend, traj = rk4(P, props, s, N)
    return s, traj, nrm


def gauss(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        if abs(pv) < 1e-300:
            pv = 1e-300
        for r in range(n):
            if r != col:
                fac = M[r][col] / pv
                for c in range(col, n + 1):
                    M[r][c] -= fac * M[col][c]
    return [M[i][n] / M[i][i] for i in range(n)]


def params(**over):
    P = dict(DEFAULT)
    P.update(over)
    return P


if __name__ == "__main__":
    P = params()
    props = properties(P['phi1'], P['phi2'])
    s, traj, nrm = solve(P, props)
    print("converged residual norm = %.2e" % nrm)
    print("unknowns [f''(0), f'''(0), theta(0), phi'(0)] =",
          ["%.6f" % v for v in s])
    yend = traj[-1][1]
    print("f''(1)   = %.6f" % yend[2])
    print("-theta'(1) = %.6f" % (-yend[5]))
    print("-phi'(1)   = %.6f" % (-yend[7]))
