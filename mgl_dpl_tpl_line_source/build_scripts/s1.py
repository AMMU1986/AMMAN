# -*- coding: utf-8 -*-
from cb import *

add(("title", "Modified Green–Lindsay Thermoelasticity with Dual-Phase-Lag and Three-Phase-Lag Heat Conduction: Response of an Unbounded Medium to Pulsed and Moving Line Heat Sources"))
add(("authors", "[Author names, affiliations and corresponding-author e-mail to be inserted]"))
add(("h1u", "Abstract"))
cLS = 1 / math.sqrt((1 + EPS) * 0.02)
cD = math.sqrt(2 * 0.012 / (1 + EPS)) / 0.02
add(("abstract",
     "The modified Green–Lindsay (MGL) theory of thermoelasticity removes the displacement discontinuity of the original "
     "Green–Lindsay model by adding a strain-rate term, but most MGL boundary-value problems still rely on a Fourier or "
     "Lord–Shulman type heat flux law and on a time-independent or step-type heat input. This paper couples MGL "
     "thermoelasticity with the dual-phase-lag (DPL) and three-phase-lag (TPL) heat conduction models and studies an "
     "unbounded isotropic plane-strain medium heated by a line source whose strength varies in time (step, rectangular "
     "pulse, exponentially decaying pulse, gamma-type pulse and sinusoidal pulse train) or which translates at constant "
     "speed. The pulsed problem is solved in closed form in the Laplace domain through a displacement potential and "
     "modified Bessel functions $K_0$ and $K_1$. The moving problem is solved by a Fourier transform in the plane and a "
     "Laplace transform in time, with the transverse integral evaluated analytically and the remaining Fourier integral "
     "evaluated by the trapezoidal rule. Large-transform-parameter asymptotics classify the models: the second-order DPL "
     "and TPL laws with $\\tau_T>\\tau_q/2$ keep one finite-speed thermal wave ($c_w=%s$ for the chosen data, against "
     "%s for the Lord–Shulman type MGL law) together with a diffusive branch, whereas first-order DPL is parabolic, and a "
     "second-order law with $\\tau_T<\\tau_q/2$ is shown numerically to be unstable. Results are inverted with Durbin's Fourier-series "
     "method accelerated by the Wynn epsilon algorithm. An independent finite-difference solver reproduces the Laplace "
     "solution to 0.2 per cent in temperature and 2 to 3 per cent in stress, the moving-source code reproduces the "
     "axisymmetric solution at zero speed to about 2×10⁻⁴, and the global heat-content identity is satisfied to better than 0.7 per cent. Parametric studies "
     "quantify the influence of the phase lags, the thermal-displacement lag, the conductivity rate, the strain-rate "
     "parameter, the pulse width and period and the source speed. The strain-rate parameter dominates the mechanical "
     "response behind the front, the phase lags dominate the arrival time and the temperature near the front, "
     "and a source moving faster than the thermal wave produces a Mach-type front with a "
     "stress peak several times larger than the stationary value." % ("%.2f" % cD, "%.2f" % cLS)))
add(("kw", "modified Green–Lindsay thermoelasticity; dual-phase-lag; three-phase-lag; pulsed line heat source; moving heat source; Laplace transform; wave speed; strain rate"))

H1("1. Introduction")
P("Heat conduction in solids that are heated on very short time scales or by very localized sources departs from the "
  "Fourier law, which predicts an infinite speed of thermal disturbance. The Lord–Shulman model introduced one "
  "relaxation time into the flux law, the Green–Lindsay model introduced two relaxation times into the constitutive "
  "and energy equations, and the Green–Naghdi models introduced thermal displacement. These theories restored finite "
  "propagation speeds but brought their own difficulties, in particular jumps in displacement at the wavefront in the "
  "Green–Lindsay case. Reviews of the generalized thermoelasticity family and of its modifications can be found in [9]. "
  "A modification that has attracted attention is the modified Green–Lindsay (MGL) theory of Yu, Xue and Tian [14], which adds "
  "a strain-rate term with the same relaxation time that multiplies the temperature rate. The additional term eliminates the "
  "discontinuity of the displacement, and the qualitative properties of the resulting system were examined by Quintanilla [15]. "
  "Subsequent work has treated fundamental solutions [3], a Galerkin-type representation [4], a finite element "
  "formulation for a functionally graded hollow disk [5], infinite-speed behaviour [2] and photothermal problems in semiconductors [6].")
P("The closest antecedent of the present work is the study of Singh and Mukhopadhyay [1], who solved the line heat source "
  "problem for an unbounded MGL medium with a Lord–Shulman type heat conduction law and a heat input switched on at "
  "time zero. By a Laplace transform and a thermoelastic potential they found one finite-speed wave and a "
  "diffusive part, with a continuous displacement and a jump confined to the hoop stress, in contrast with Lord–Shulman, "
  "Green–Lindsay and Moore–Gibson–Thompson solutions that show two wavefronts. Line source problems under "
  "Moore–Gibson–Thompson thermoelasticity were examined in [7] and [8]. Those analyses used a single relaxation time in the "
  "flux law and a Heaviside time dependence of the source.")
P("Two features of practical heating are not covered by that setting. First, real sources are pulsed: laser or electron "
  "beam heating has a finite duration, a rapid rise and a decay, and may be repeated periodically. The response then "
  "depends on how the pulse width and period compare with the phase lags of the material. Second, sources move: a focused beam scanned "
  "over a surface, a welding arc or a travelling hot spot has a position that changes with time, and when the source speed "
  "exceeds the thermal wave speed the field acquires a conical front. Both features interact with the heat conduction law "
  "because the lag times determine how fast the material can follow the source.")
P("The heat conduction law is the second ingredient. The dual-phase-lag (DPL) model of Tzou introduces a lag $\\tau_q$ "
  "in the heat flux and a lag $\\tau_T$ in the temperature gradient, so that it contains the Fourier and Lord–Shulman laws "
  "as special cases. The three-phase-lag (TPL) model of Roychoudhuri adds a lag $\\tau_v$ in the thermal displacement gradient "
  "weighted by a conductivity rate $K^*$, which restores the thermal displacement of Green–Naghdi theory within a lag framework. "
  "These laws are normally studied with Taylor expansions in the lags, and the order of the expansion decides the mathematical "
  "type of the heat equation. First-order expansions in both lags give a parabolic equation, whereas an expansion that is of "
  "second order in $\\tau_q$ gives a hyperbolic one provided a stability condition on the ratio of the lags holds. "
  "Because the order of the expansion decides the wave structure, a careful asymptotic analysis is needed before any "
  "numerical result is trusted, and this paper devotes a full section to it.")
P("The aims of the paper are therefore: (i) to formulate MGL thermoelasticity with DPL and TPL heat conduction in a "
  "form that contains the Lord–Shulman MGL model of [1] and the Fourier model as limits; (ii) to solve the pulsed line "
  "source problem exactly in the Laplace domain for several temporal profiles; (iii) to solve a rigorously defined moving "
  "line source problem; (iv) to classify the wave structure by large-parameter asymptotics and to check the "
  "stability of the second-order lag laws; (v) to invert the transforms numerically and to validate the inversion by "
  "independent means; and (vi) to quantify the sensitivity of the response to the lag times, the conductivity rate, the "
  "strain-rate parameter, the pulse parameters and the source speed.")
P("The paper makes a specific and limited claim. All results use the nondimensional copper data and lag times of [1], which "
  "are chosen to make wave effects visible and correspond to sub-picosecond physical times, and the lag values for the "
  "DPL and TPL models are illustrative choices that satisfy the stability condition rather than measured values. The moving "
  "source is a line parallel to the $z$ axis that translates at constant speed in plane strain; it is not a "
  "three-dimensional point source or a finite-diameter beam. The classical foundational models (Lord–Shulman, Green–Lindsay, Tzou, "
  "Roychoudhuri, Chandrasekharaiah) are cited here by author and model name only, because they predate 2013 and the reference "
  "list of this manuscript is restricted to the 2013 to 2026 window.")
P("The remainder of the paper is organised as follows. Section 2 states the governing equations and the nondimensional form. "
  "Section 3 derives the pulsed-source solution and the temporal profiles. Section 4 treats the moving source. Section 5 gives the large-parameter "
  "asymptotics and the stability analysis. Section 6 describes the numerical inversion and the validation tools. Section 7 "
  "presents the results and Section 8 lists limitations. Section 9 summarises the conclusions.")

H1("2. Governing equations")
H2("2.1 Dimensional MGL thermoelasticity")
P("Consider a homogeneous, isotropic, linearly thermoelastic solid with Lamé constants $\\lambda$ and $\\mu$, mass density $\\rho$, "
  "specific heat at constant strain $c_E$, thermal conductivity $k$ and coupling constant $\\gamma=(3\\lambda+2\\mu)\\alpha_t$, where "
  "$\\alpha_t$ is the linear thermal expansion coefficient. Let $\\theta$ be the temperature increment over the reference "
  "temperature $T_0$, $\\varepsilon_{ij}$ the strain tensor, $e$ its trace and $Q$ the volumetric heat source. In the MGL theory [14] the "
  "stress is")
EQ(r"\sigma_{ij}=\left(1+\tau_1\partial_t\right)\left[\lambda e\delta_{ij}+2\mu\varepsilon_{ij}-\gamma\theta\delta_{ij}\right]")
P("where $\\tau_1$ is the relaxation time that multiplies both the temperature rate (as in the Green–Lindsay model) and, in the "
  "MGL modification, the strain rate. The equation of motion without body force and the energy balance are")
EQ(r"\rho\,\partial_t^2 u_i=\sigma_{ij,j}")
EQ(r"\rho c_E\,\partial_t\theta+\gamma T_0\,\partial_t e=-\nabla\cdot q+Q")
P("The heat flux $q$ is closed by a constitutive law. Four members of the family are used. The Fourier and Lord–Shulman laws are")
EQ(r"q=-k\nabla\theta")
EQ(r"\left(1+\tau_0\partial_t\right)q=-k\nabla\theta")
P("The dual-phase-lag law states that the flux at time $t+\\tau_q$ is produced by the temperature gradient at time $t+\\tau_T$,")
EQ(r"q(x,t+\tau_q)=-k\nabla\theta(x,t+\tau_T)")
P("and its Taylor expansion, taken to second order in $\\tau_q$ and first order in $\\tau_T$, is")
EQ(r"\left(1+\tau_q\partial_t+\tfrac{1}{2}\tau_q^2\partial_t^2\right)q=-k\left(1+\tau_T\partial_t\right)\nabla\theta")
P("The three-phase-lag law of Roychoudhuri adds the gradient of the thermal displacement $v$, defined by "
  "$\\partial_t v=\\theta$, with a lag $\\tau_v$ and the conductivity rate $K^*$:")
EQ(r"q(x,t+\tau_q)=-\left[k\nabla\theta(x,t+\tau_T)+K^{*}\nabla v(x,t+\tau_v)\right]")
P("Expanding to second order in $\\tau_q$ and first order in $\\tau_T$ and $\\tau_v$ gives")
EQ(r"\left(1+\tau_q\partial_t+\tfrac{1}{2}\tau_q^2\partial_t^2\right)q=-k\left(1+\tau_T\partial_t\right)\nabla\theta-K^{*}\left(1+\tau_v\partial_t\right)\nabla v")
P("These expansions are standard; the truncation order is a modelling decision and is discussed in Section 5. When only the "
  "first-order term in $\\tau_q$ is retained and $\\tau_T=0$, $K^*=0$, the Lord–Shulman law is recovered with $\\tau_0=\\tau_q$, and "
  "this is the role that $\\tau_0$ of [1] plays below. When $\\tau_q=\\tau_T$ at first order the flux law reduces to the Fourier law "
  "after both sides are divided by the common factor.")

H2("2.2 Nondimensional form")
P("The nondimensional variables are those of [1]. With $c_1^2=(\\lambda+2\\mu)/\\rho$ and $\\eta=\\rho c_E/k$ the scalings are")
EQ(r"x^{\prime}=\eta c_1 x,\quad t^{\prime}=\eta c_1^2 t,\quad u^{\prime}=\eta c_1 u,\quad \theta^{\prime}=\theta/T_0,\quad \sigma_{ij}^{\prime}=\sigma_{ij}/(\lambda+2\mu)")
P("and the lag times scale like time, $\\tau^{\\prime}=\\eta c_1^2\\tau$. The conductivity rate, which has the dimension of $k$ per unit time, "
  "becomes $K=K^*/(\\eta c_1^2 k)$. The dimensionless coupling constants are")
EQ(r"\delta_1=\frac{\gamma T_0}{\lambda+2\mu},\quad \delta_2=\frac{\gamma}{\rho c_E},\quad \lambda_1=\frac{\lambda}{\lambda+2\mu},\quad \epsilon=\delta_1\delta_2,\quad \kappa=1-\lambda_1")
P("Primes are dropped from here on. For the copper data used in [1] these constants are listed in Table 2. The scaling "
  "implies that one nondimensional length unit is %s m and one time unit is %s s, so that the nondimensional lag "
  "times quoted below correspond to sub-picosecond physical lags." % (g(1/(8886.73*C['v']), 3), g(1/(8886.73*C['v']**2), 3)))
P("In the Laplace domain with zero initial data and a transform parameter $s$ the flux laws above take the common form")
EQ(r"\Phi(s)\,\bar q=-\Psi(s)\nabla\bar\theta")
P("with the operators")
EQ(r"\Phi(s)=1+\tau_q s+\tfrac{1}{2}\tau_q^2 s^2")
EQ(r"\Psi(s)=1+\tau_T s+\frac{K\left(1+\tau_v s\right)}{s}")
P("The Fourier model has $\\Phi=\\Psi=1$, the Lord–Shulman model has $\\Phi=1+\\tau_0 s$ (first-order truncation) and $\\Psi=1$, the "
  "first-order DPL model has $\\Phi=1+\\tau_q s$ and $\\Psi=1+\\tau_T s$, the second-order DPL model has the full $\\Phi$ above with $K=0$, and "
  "the TPL model has all terms. The parameter $K$ appears in $\\Psi$ with a pole at $s=0$: it makes the long-time behaviour "
  "of the TPL model wave-like instead of diffusive, as shown in Section 5.")
H2("2.3 Axisymmetric plane-strain equations")
P("For a line source along the $z$ axis the medium is in plane strain and all fields depend on the radial distance $r$ and time. The "
  "radial displacement $u(r,t)$ is the only displacement component. The nondimensional equation of motion, the dilatation and the stresses are")
EQ(r"\partial_t^2 u=\left(1+\tau_1\partial_t\right)\left(\partial_r e-\delta_1\partial_r\theta\right)")
EQ(r"e=\partial_r u+\frac{u}{r}")
EQ(r"\sigma_{rr}=\left(1+\tau_1\partial_t\right)\left[\partial_r u+\lambda_1\frac{u}{r}-\delta_1\theta\right]")
EQ(r"\sigma_{\phi\phi}=\left(1+\tau_1\partial_t\right)\left[\lambda_1\partial_r u+\frac{u}{r}-\delta_1\theta\right]")
P("The heat source is a line source of strength $Q_0$ per unit length with an arbitrary temporal profile $f(t)$,")
EQ(r"Q(r,t)=\frac{Q_0}{2\pi r}\,\delta(r)\,f(t)")
P("so that $Q_0$ is the total source integrated over the plane. In the energy equation the source enters in the convention of "
  "[1], in which the Laplace-domain combined equation reads")
EQ(r"\Psi(s)\nabla^2\bar\theta=\Phi(s)\,s\left(\bar\theta+\delta_2\bar e\right)-\bar Q")
P("with $\\nabla^2=\\partial_r^2+r^{-1}\\partial_r$. This convention (called the effective-source convention below) reduces exactly to the "
  "equation of [1] for the Lord–Shulman limit, which makes the comparison with that paper meaningful. A physically "
  "equivalent alternative in which the source is carried through the lag operator, $-\\Phi(s)\\bar Q$, was also implemented; it differs by the "
  "operator $\\Phi(\\partial_t)$ acting on $f$, which for a step creates impulsive terms at $t=0$. The alternative is used only for the "
  "limit check $\\tau_q=\\tau_T\\to$ Fourier, where it gives exact agreement. The Laplace transform of the momentum "
  "equation is")
EQ(r"s^2\bar u=\left(1+\tau_1 s\right)\left(\partial_r\bar e-\delta_1\partial_r\bar\theta\right)")
P("The thermoelastic displacement potential $\\varphi$ is defined by")
EQ(r"u=\partial_r\varphi,\qquad e=\nabla^2\varphi")
P("so that, after integrating the momentum equation once and imposing decay at infinity, with $p=1+\\tau_1 s$,")
EQ(r"\bar\theta=\frac{1}{\delta_1}\left(\nabla^2\bar\varphi-\frac{s^2}{p}\bar\varphi\right)")
P("Substituting into the energy equation gives a fourth-order equation for the potential,")
EQ(r"\left(\nabla^4-B\nabla^2+C\right)\bar\varphi=-\frac{\delta_1\bar Q}{\Psi}")
EQ(r"B=\frac{s^2}{p}+\left(1+\epsilon\right)\frac{\Phi s}{\Psi},\qquad C=\frac{\Phi s^3}{\Psi p}")
P("For the Lord–Shulman limit these coefficients are $B=(b_1s^3+b_2s^2+b_3s)/p$ and $C=s^3(1+\\tau_0 s)/p$ with $b_1=(1+\\epsilon)\\tau_1\\tau_0$, "
  "$b_2=(1+\\epsilon)(\\tau_1+\\tau_0)+1$ and $b_3=1+\\epsilon$, the form quoted in [1]. The same derivation with the temperature-rate "
  "coupling of the original Green–Lindsay theory (no strain-rate term) was also coded as a comparison model and is labelled GL.")

FIG("Figure_1.png", "Schematic of the two source configurations in the unbounded plane-strain medium: (a) the pulsed axisymmetric line source with its thermal wavefront and diffusive tail; (b) the line source translating at speed $V$ with the Mach-type envelope that exists when $V>c_w$. Geometry schematic, not computed.")

P("It is useful to interpret the operators $\\Phi$ and $\\Psi$ physically before the solution is constructed. The operator $\\Phi$ describes the delay with which the heat "
  "flux responds to a change of the driving gradient, so that it controls how fast thermal information can travel; a vanishing $\\tau_q$ removes the delay and the front disappears. The operator $\\Psi$ "
  "describes the delay with which the gradient itself is felt, and a positive $\\tau_T$ gives the medium a memory of the gradient that acts against the flux delay. When the two "
  "act together the net behaviour depends on their ratio, which is why the stability condition of Section 5 involves $\\tau_T/\\tau_q$. In the TPL model the factor $K(1+\\tau_vs)/s$ adds a contribution "
  "proportional to the history of the temperature, which gives the medium a restoring character at long times.")
