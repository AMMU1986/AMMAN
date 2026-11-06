# -*- coding: utf-8 -*-
from cb import *

A = R["asym"]
cD = math.sqrt(2 * 0.012 / (1 + EPS)) / 0.02
cLS = 1 / math.sqrt((1 + EPS) * 0.02)

H1("5. Short-time asymptotics, wave structure and stability")
H2("5.1 Large-parameter expansion of the characteristic roots")
P("Wavefronts are governed by the behaviour of the roots $m_1(s)$ and $m_2(s)$ for large $|s|$. If $m\\sim s/c$ then $e^{-mr}$ transforms back to a "
  "function that vanishes for $t<r/c$, so that $c$ is a finite propagation speed; if $m\\sim\\sqrt{s}$ the corresponding contribution is "
  "diffusive, has an infinite speed of propagation and is exponentially small ahead of the wave. The classification therefore reduces to the "
  "exponent in $m\\sim s^{\\nu}$. For the second-order DPL law with $\\tau_T>0$, the large-$s$ forms of the operators are")
EQ(r"\Phi(s)\simeq\frac{\tau_q^2s^2}{2},\qquad \Psi(s)\simeq\tau_Ts,\qquad \frac{\Phi}{\Psi}\simeq\frac{\tau_q^2s}{2\tau_T}\left[1+\frac{1}{s}\left(\frac{2}{\tau_q}-\frac{1}{\tau_T}\right)\right]")
P("The coefficients of the quadratic for $x=m^2$ become")
EQ(r"B\simeq a s^2+\left[a\left(\frac{2}{\tau_q}-\frac{1}{\tau_T}\right)+\frac{1}{\tau_1}\right]s,\qquad a=\frac{(1+\epsilon)\tau_q^2}{2\tau_T}")
EQ(r"C\simeq\frac{\tau_q^2}{2\tau_T\tau_1}s^3")
P("Since $B$ is of order $s^2$ and $C$ of order $s^3$ the two roots separate, $x_1\\simeq B-C/B$ and $x_2\\simeq C/B$, which leads to a fast root that "
  "is linear in $s$ and a slow root that behaves like $\\sqrt{s}$:")
EQ(r"m_1\simeq\frac{s}{c_w}+\beta,\qquad c_w=\frac{1}{\tau_q}\sqrt{\frac{2\tau_T}{1+\epsilon}}")
EQ(r"\beta=\frac{1}{2c_w}\left(\frac{2}{\tau_q}-\frac{1}{\tau_T}\right)+\frac{c_w\,\epsilon}{2\left(1+\epsilon\right)\tau_1}")
EQ(r"m_2^2\simeq\frac{s}{\left(1+\epsilon\right)\tau_1}")
P("The fast root gives a thermoelastic wave with the finite speed $c_w$ and a spatial attenuation $e^{-\\beta r}$ of its amplitude; the slow "
  "root carries the diffusive, strain-rate controlled part. For the base data $c_w=%s$ and $\\beta=%s$. The closed-form attenuation "
  "agrees with the numerical value of $\\mathrm{Re}(m_1-s/c_w)$ computed at $s=10^7$, which is %s. The first term of $\\beta$ is the lag "
  "contribution and the second is the strain-rate contribution; the second is proportional to $\\epsilon/\\tau_1$ and "
  "therefore vanishes as the thermoelastic coupling vanishes." % (
      g(cD, 4), g(X["beta"]["MGL-DPL2"]["beta_cf"], 4), g(X["beta"]["MGL-DPL2"]["beta_num"], 4)))
P("For the Lord–Shulman MGL law the same procedure gives the speed of [1], with a corresponding attenuation constant of %s that "
  "was also checked numerically (numerical value %s):" % (g(X["beta_LS_cf"], 4), g(X["beta"]["MGL-LS"]["beta_num"], 4)))
EQ(r"c_{LS}=\frac{1}{\sqrt{\left(1+\epsilon\right)\tau_0}}")
P("which equals %s for the data of [1], in agreement with the value of about 7.01 quoted there. The original Green–Lindsay type law has two finite "
  "speeds, from $\\rho^2-(1+\\tau_0)\\rho+\\tau_0=0$ with $x=\\rho s^2$, equal to $1$ (the elastic speed) and $1/\\sqrt{\\tau_0}$, which "
  "explains the two wavefronts that [1] reports for that theory." % g(cLS, 4))
P("The first-order DPL law behaves differently. Because $\\Phi/\\Psi\\to\\tau_q/\\tau_T$ the coefficients $B$ and $C$ are of order $s$ and $s^2$, and "
  "both roots scale like $\\sqrt{s}$. Writing $x=\\varrho s$,")
EQ(r"\varrho^2-\left[\frac{1}{\tau_1}+\left(1+\epsilon\right)\frac{\tau_q}{\tau_T}\right]\varrho+\frac{\tau_q}{\tau_T\tau_1}=0")
P("so that both branches are diffusive and the first-order DPL model, like the Fourier model, has no wavefront: the numerical exponents in Table 3 "
  "are 0.50 for both roots. The statement in the literature that the first-order DPL equation is wave-like when $\\tau_q>\\tau_T$ refers to "
  "the uncoupled heat equation expanded to second order in $\\tau_q$; the first-order expansion is of parabolic type. The TPL law with a first-order "
  "flux expansion and $\\tau_T=0$ has $\\Psi\\to1+K\\tau_v$ and a finite speed")
EQ(r"c_{TPL1}=\sqrt{\frac{1+K\tau_v}{\left(1+\epsilon\right)\tau_q}}")
P("which equals %s for $K=0.1$, $\\tau_v=0.03$ and is confirmed numerically in Table 3. For the second-order TPL law with $\\tau_T>0$ the "
  "leading large-$s$ terms are unchanged, because $K(1+\\tau_vs)/s\\to K\\tau_v$ is a constant that is small compared with $\\tau_Ts$; the "
  "parameters $\\tau_v$ and $K$ affect the speed only through corrections of relative order $1/s$, so the numerical speed of the TPL model "
  "in Table 3 coincides with that of the DPL model to six digits." % g(math.sqrt((1 + 0.1 * 0.03) / ((1 + EPS) * 0.02)), 4))
H2("5.2 Stability of the second-order lag laws")
P("A second-order expansion in $\\tau_q$ combined with a first-order expansion in $\\tau_T$ is not unconditionally well posed. The stability can "
  "be tested directly on the plane-wave dispersion relation of the coupled system. With wave number $\\xi$ and $\\Psi^{\\prime}=s\\Psi$ the relation, "
  "after multiplication by $p$ and by $s$, is the polynomial equation")
EQ(r"\Psi^{\prime}p\,\xi^4+\left[\Psi^{\prime}s^2+\left(1+\epsilon\right)\Phi\,p\,s^2\right]\xi^2+\Phi s^4=0")
P("whose roots $s(\\xi)$ must lie in the closed left half-plane for the initial value problem to be stable, and for the Laplace inversion with a "
  "contour to the right of all singularities to be valid. The polynomial has degree five for DPL and six for TPL and was solved by an Aberth iteration "
  "for ten wave numbers between 0.1 and 3000. The largest real part found is listed in Table 3. For the uncoupled heat equation it is known "
  "from the stability analysis of Quintanilla and Racke that the second-order DPL law is stable if")
EQ(r"\tau_T>\frac{\tau_q}{2}")
P("and the dispersion scan reproduces this threshold for the coupled MGL system: with $\\tau_q=0.02$ and $\\tau_T=0.012$ the maximal growth rate is zero, whereas for "
  "$\\tau_T=0.006$ it equals %s, so that a Laplace inversion for that case would be meaningless. All results for second-order DPL and TPL "
  "models in this paper use $\\tau_T=0.012>\\tau_q/2$ or larger. The stable wave speed then exceeds the Lord–Shulman speed with the same $\\tau_q$; for "
  "$\\tau_T=\\tau_q/2$ the two speeds coincide at leading order. This is a structural property of the second-order law and not a "
  "numerical artefact." % g(A["DPL2-unstable"]["growth"], 3))
P("The three-phase-lag law has its own restriction. Keeping $\\tau_q=0.02$ and $\\tau_T=0.012$ and varying the thermal-displacement lag, the dispersion scan "
  "shows that the TPL system is stable only when the product $K\\tau_v$ stays below a threshold, which was located by bisection and found to be "
  "%s, %s and %s for $K=0.1$, $0.5$ and $2$ respectively, that is, $K\\tau_v\\approx0.28$ independently of $K$ over this range. "
  "For $K=0.5$ the maximal growth rate is %s for $\\tau_v=1$ and %s for $\\tau_v=3$. A first set of parametric calculations that used $\\tau_v$ up to 3 was therefore discarded "
  "and repeated with $\\tau_v\\le0.5$. The threshold is a numerical finding for these lags; no closed-form condition is claimed here." % (
      g(A["_tpl_threshold"]["0.1"][1], 3), g(A["_tpl_threshold"]["0.5"][1], 3), g(A["_tpl_threshold"]["2.0"][1], 3),
      g(A["_tpl_unstable_examples"]["tv1_K0.5"], 3), g(A["_tpl_unstable_examples"]["tv3_K0.5"], 3)))
H2("5.3 Long-time behaviour of the TPL model")
P("The conductivity rate $K$ introduces a pole $K/s$ in $\\Psi$ that dominates at small $s$. For $|s|\\ll1$ the quantities $\\Psi\\simeq K/s$, $\\Phi\\simeq1$ and $p\\simeq1$ give "
  "$B\\simeq s^2[1+(1+\\epsilon)/K]$ and $C\\simeq s^4/K$, so that both roots are linear in $s$ at long times, $x=\\rho s^2$, with")
EQ(r"\rho^2-\left[1+\frac{1+\epsilon}{K}\right]\rho+\frac{1}{K}=0")
P("This means that at late times the TPL model has two finite speeds $1/\\sqrt{\\rho_{\\pm}}$ instead of a diffusive tail. For vanishing coupling the roots are $1$ and "
  "$1/K$, so one speed is the elastic speed and the other is $\\sqrt{K}$ (in units of the elastic speed), which is the thermal-displacement wave "
  "of Green–Naghdi type. This is why the conductivity rate changes the far field at later times in Figure 10 and why its effect is very small at "
  "the early times of Figure 9. The practical consequence is that $K^*$ must be treated as a long-time parameter.")
H2("5.4 Arrival time and amplitude of the front")
P("For a given point $r$ the front arrives at the time")
EQ(r"t_f(r)=\frac{r}{c_w},\qquad \theta,\sigma\sim e^{-\beta r}\ \text{ at the front}")
P("The exponential attenuation with $\\beta$ of order 2 to 5 explains why wave effects are visible only for $r\\lesssim1$ in the figures; further out the "
  "wave amplitude has decayed to the level of the numerical noise and the response is controlled by the diffusive root.")

P("A practical consequence of Sections 5.1 to 5.3 is a procedure for choosing lag parameters. For a given flux lag $\\tau_q$ the temperature-gradient lag must satisfy $\\tau_T>\\tau_q/2$, "
  "and the wave speed then follows from $c_w$ without any numerical solution. If a measured front speed is available, the formula can be inverted to give $\\tau_T=(1+\\epsilon)\\tau_q^2c_w^2/2$, "
  "which must then be tested against the stability limit. The thermal-displacement lag and the conductivity rate do not change the speed at leading order and must be identified from "
  "long-time data. This separation of roles between the leading and the corrective parameters is a useful structural result of the asymptotic analysis, and it explains why "
  "the DPL and TPL curves of Section 7 nearly coincide at early times.")

FIG("Figure_4.png", "Large-parameter behaviour of the characteristic roots for real $s$: (a) $|m_1|/s$, which tends to the reciprocal of a finite wave speed for the LS, second-order DPL and TPL models, and to zero for first-order DPL; (b) $|m_2|/\\sqrt{s}$, which tends to a constant for a diffusive branch. The GL curve belongs to the original Green–Lindsay type law with two finite speeds.")
TAB("Physical data for copper (from [1]) and nondimensional parameters used in the computations.",
    [["Quantity", "Symbol", "Value"],
     ["Lamé constant", "$\\lambda$", "7.76×10¹⁰ N/m²"],
     ["Shear modulus", "$\\mu$", "3.86×10¹⁰ N/m²"],
     ["Thermal expansion coefficient", "$\\alpha_t$", "1.78×10⁻⁵ K⁻¹"],
     ["Specific heat", "$c_E$", "383.1 J/(kg K)"],
     ["Thermal conductivity", "$k$", "386 W/(m K)"],
     ["Density", "$\\rho$", "8954 kg/m³"],
     ["Reference temperature", "$T_0$", "293 K"],
     ["Thermal diffusion parameter", "$\\eta$", "8886.73 s/m²"],
     ["Strain-rate lag", "$\\tau_1$", "0.05"],
     ["Flux lag (Lord–Shulman role $\\tau_0$)", "$\\tau_q$", "0.02"],
     ["Temperature-gradient lag", "$\\tau_T$", "0.012"],
     ["Thermal-displacement lag, conductivity rate", "$\\tau_v$, $K$", "0.03, 0.1"],
     ["Source strength", "$Q_0$", "1"]],
    [3700, 1500, 3200])
mm = mgl.constants()
TAB("Derived dimensionless constants and characteristic speeds.",
    [["Quantity", "Expression", "Value"],
     ["Coupling constant", "$\\delta_1=\\gamma T_0/(\\lambda+2\\mu)$", g(mm["d1"], 4)],
     ["Coupling constant", "$\\delta_2=\\gamma/(\\rho c_E)$", g(mm["d2"], 4)],
     ["Coupling product", "$\\epsilon=\\delta_1\\delta_2$", g(mm["eps"], 4)],
     ["Modulus ratio", "$\\lambda_1=\\lambda/(\\lambda+2\\mu)$", g(mm["lambda1"], 4)],
     ["Shear ratio", "$\\kappa=1-\\lambda_1$", g(mm["kappa"], 4)],
     ["Elastic speed", "$c_1=\\sqrt{(\\lambda+2\\mu)/\\rho}$", g(mm["v"], 4) + " m/s"],
     ["Length unit", "$1/(\\eta c_1)$", g(1 / (8886.73 * mm["v"]), 3) + " m"],
     ["Time unit", "$1/(\\eta c_1^2)$", g(1 / (8886.73 * mm["v"] ** 2), 3) + " s"],
     ["Lord–Shulman MGL wave speed", "$c_{LS}$", g(cLS, 4)],
     ["Second-order DPL wave speed", "$c_w$", g(cD, 4)],
     ["First-order TPL speed ($\\tau_T=0$)", "$c_{TPL1}$", g(math.sqrt((1 + 0.003) / ((1 + EPS) * 0.02)), 4)]],
    [3200, 3500, 1700])

rows = [["Model", "Large-$s$ operators", "Exponent $m_1$", "Exponent $m_2$", "Numerical $c$", "Formula $c$", "Max growth", "Fronts"]]
spec = [("Fourier", "$\\Phi=\\Psi=1$", "-", "none"),
        ("GL", "GL-type", "1 and %s" % g(1 / math.sqrt(0.02), 4), "two"),
        ("MGL-LS", "$\\Phi\\sim\\tau_0s$, $\\Psi=1$", g(cLS, 4), "one"),
        ("MGL-DPL1", "$\\Phi/\\Psi\\to\\tau_q/\\tau_T$", "none", "none"),
        ("MGL-DPL2", "$\\Phi\\sim\\tau_q^2s^2/2$, $\\Psi\\sim\\tau_Ts$", g(cD, 4), "one"),
        ("MGL-TPL", "as DPL2, plus $K(1+\\tau_vs)/s$", g(cD, 4), "one"),
        ("MGL-TPL1", "$\\Phi\\sim\\tau_qs$, $\\Psi\\to1+K\\tau_v$", g(math.sqrt((1 + 0.003) / ((1 + EPS) * 0.02)), 4), "one"),
        ("DPL2-unstable", "as DPL2, $\\tau_T=0.006$", g(math.sqrt(2 * 0.006 / (1 + EPS)) / 0.02, 4), "one (unstable)")]
for k, ops, cf, fr in spec:
    a = A[k]
    cn = "-" if k in ("Fourier", "MGL-DPL1") else g(a["c1"], 4)
    rows.append([k, ops, g(a["exp"][0], 3), g(a["exp"][1], 3), cn, cf, g(a["growth"], 2), fr])
TAB("Asymptotic classification of the characteristic roots at large $s$ (numerical exponents from $s=10^5$ and $10^6$; maximal growth rate from the dispersion scan).",
    rows, [1150, 1900, 800, 800, 1100, 1000, 900, 750])

H1("6. Numerical inversion and validation tools")
H2("6.1 Inversion of the Laplace transform")
P("The transformed fields are inverted with the Fourier-series method of Durbin, in its standard form. For a "
  "target time $t$ and an interval length $T=2t$ the approximation with $N$ terms is")
EQ(r"f(t)\approx\frac{e^{ct}}{T}\left[\tfrac{1}{2}\mathrm{Re}\,\bar f(c)+\sum_{k=1}^{N}{\mathrm{Re}\left\{\bar f\!\left(c+\frac{ik\pi}{T}\right)e^{ik\pi t/T}\right\}}\right]")
P("with $ct=6$. The truncation error is estimated by comparing the result with $N$ terms to that with $N/2$ terms,")
EQ(r"\varepsilon_N=\frac{\left|f_N(t)-f_{N/2}(t)\right|}{\left|f_N(t)\right|}")
P("and the partial sums of the last twelve terms are accelerated with the Wynn epsilon algorithm,")
EQ(r"\varepsilon_{k+1}^{(n)}=\varepsilon_{k-1}^{(n+1)}+\frac{1}{\varepsilon_k^{(n+1)}-\varepsilon_k^{(n)}}")
P("which reduces the oscillation caused by the discontinuous hoop stress at the front. The modified Bessel functions of complex argument were "
  "computed with a power series for $|z|\\le2$ and, for larger $|z|$, with the exponentially convergent trapezoidal evaluation of")
EQ(r"e^{z}K_\nu(z)=\sqrt{\frac{\pi}{2z}}\frac{1}{\Gamma(\nu+1/2)}\int_0^{\infty}{e^{-u}u^{\nu-1/2}\left(1+\frac{u}{2z}\right)^{\nu-1/2}du}")
P("which avoids overflow for the large arguments encountered at the high-frequency terms. The Bessel evaluations were checked against the analytical Fourier "
  "solution: for the uncoupled Fourier model ($\\epsilon=0$) the step solution is $\\theta=Q_0E_1(r^2/4t)/4\\pi$, and the inversion reproduced it with a maximum relative "
  "error of %s over nine combinations of $r$ and $t$." % g(R["checks"]["fourier_E1_maxrel"], 2))
H2("6.2 Independent finite-difference solver")
P("An independent solver was written that does not use Laplace transforms, Bessel functions or the potential. It integrates the Lord–Shulman MGL "
  "equations for a heated disc of radius $r_c$ in a staggered grid with temperature at nodes and displacement at half nodes, using the temperature rate "
  "$w=\\partial_t\\theta$ as an auxiliary variable,")
EQ(r"\tau_0\,\partial_t w=\nabla^2\theta+Q-w-\delta_2\partial_t e-\delta_2\tau_0\,\partial_t^2e,\qquad \partial_t\theta=w")
EQ(r"\partial_t^2u=\partial_r\left[e-\delta_1\theta+\tau_1\left(\partial_te-\delta_1w\right)\right]")
P("The scheme is explicit and stable if the time step satisfies")
EQ(r"\Delta t\le\min\left\{0.2\frac{\Delta r^2}{\tau_1},\;\frac{0.2\,\Delta r}{8}\right\}")
P("with $\\Delta r=0.002$ and $r_c=0.02$ (area-equivalent radius 0.021). Since a finite-difference solver cannot represent a delta source, the "
  "exact comparator is the Laplace solution for a uniform disc, which for $r>r_c$ differs from the line solution only through the factor")
EQ(r"\Xi_j=\frac{2\,I_1(m_jr_c)}{m_jr_c},\qquad \bar\varphi=G\left[\Xi_1K_0(m_1r)-\Xi_2K_0(m_2r)\right]")
P("which follows from the mean-value property of solutions of $(\\nabla^2-m^2)w=0$ outside the disc. The function $e^{-z}I_1(z)$ is computed by "
  "the periodic trapezoidal rule of its integral representation, which is accurate for all complex arguments needed. Agreement is quantified by "
  "the maximal error normalised by the maximal value of the field,")
EQ(r"E_f=\frac{\max_r\left|f_{FD}(r)-f_{LT}(r)\right|}{\max_r\left|f_{LT}(r)\right|}")
P("and the quadrature error of the moving-source integral, defined as the relative difference with the axisymmetric $K_0$ solution at $V=0$, is "
  "expected to decay with the step as")
EQ(r"E_h\sim e^{-2\pi d/h}")
P("until another error source (the Durbin inversion itself) is reached. A final global test is the heat-content identity of Section 3.2, whose relative defect is")
EQ(r"E_Q=\frac{\left|\int\theta\,dA-Q_0\mathcal{L}^{-1}[\bar F/(s\Phi)]\right|}{Q_0\mathcal{L}^{-1}[\bar F/(s\Phi)]}")

