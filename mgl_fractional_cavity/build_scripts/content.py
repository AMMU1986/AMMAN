# -*- coding: utf-8 -*-
"""Manuscript content. Block types:
('title', text) ('authors', text) ('h1', text) ('h2', text) ('p', text) ('abstract', text)
('kw', text) ('eq', latex, number) ('fig', file, caption) ('table', caption, rows, widths)
('ref', text, doi) ('note', text)
Inline math in paragraphs: $...$ (LaTeX subset)."""
import math
import mgl

C = mgl.constants()
VW = 1.0 / math.sqrt((1 + C["eps"]) * 0.02)

B = []
add = B.append

add(("title", "MGL Thermoelasticity of a Spherical Cavity and a Cylindrical Hole under Thermal Shock with Fractional-Order Heat Conduction"))
add(("authors", "[Author names, affiliations and corresponding-author e-mail to be inserted]"))

add(("h1u", "Abstract"))
add(("abstract",
     "Modified Green–Lindsay (MGL) thermoelasticity adds a strain-rate term to the temperature-rate-dependent "
     "Green–Lindsay (GL) theory and thereby removes the displacement discontinuity that GL theory predicts at a "
     "propagating wavefront. Most boundary-value problems solved so far within MGL theory use an integer-order law of "
     "heat conduction. This work formulates the response of an unbounded isotropic medium that contains either a "
     "spherical cavity or a cylindrical hole whose wall is subjected to a sudden temperature rise, using a Caputo-type "
     "fractional extension of the MGL energy equation of order $0<\\alpha\\le 1$. A displacement potential and the "
     "Laplace transform reduce each geometry to a fourth-order operator equation. The spherical case is solved in closed "
     "form with the kernel $e^{-mr}/r$, and the cylindrical case with modified Bessel functions of the second kind. "
     "Large-parameter asymptotics show that for $\\alpha=1$ the solution consists of one finite-speed wave plus a "
     "diffusive part, whereas for $0<\\alpha<1$ both parts are diffusive at leading order, so that the sharp wavefront is "
     "lost. Time-domain fields are obtained by Fourier-series (Durbin) numerical Laplace inversion with Wynn-epsilon "
     "acceleration and are cross-checked against an independent finite-difference solution. For copper with "
     "$\\tau_0=0.02$ and $\\tau_1=0.05$, the computations for $\\alpha=1$ show a finite jump in temperature, radial "
     "stress and hoop stress at $r=a+v_w t$ with $v_w\\approx 7.01$, while the displacement remains continuous. For "
     "$\\alpha=0.5$, $0.75$ and $0.9$ no jump is found; the hoop-stress front is replaced by a continuous compressive "
     "layer that becomes steeper as $\\alpha$ approaches 1. The strain-rate relaxation time $\\tau_1$ leaves the "
     "wavefront position unchanged but alters the hoop stress at the cavity wall, which changes sign between "
     "$\\tau_1=0.05$ and $\\tau_1=0.08$ in the computed case."))
add(("kw", "modified Green–Lindsay theory; fractional heat conduction; spherical cavity; cylindrical hole; "
     "thermal shock; Laplace transform; Caputo derivative"))

# ---------------------------------------------------------------- 1
add(("h1", "1  Introduction"))
add(("h2", "1.1  Background"))
add(("p", "Classical coupled thermoelasticity rests on Fourier's law of heat conduction. Combined with the energy "
     "balance, Fourier's law gives a parabolic heat equation, so a thermal disturbance applied at one point is felt "
     "instantaneously everywhere in the body. For most engineering time scales this idealization is harmless, but it "
     "fails when the heat flux is very high or the time scale of interest is very short. Typical examples are pulsed "
     "laser heating, welding arcs, the heat released at the tip of a fast-running crack and ultrafast heating of thin "
     "films. In these situations the finite time that the heat flux needs to respond to a change in the temperature "
     "gradient is comparable to the time scale of loading, and the thermal response acquires a wave-like character."))
add(("p", "Generalized thermoelasticity addresses this deficiency by introducing one or more relaxation times, or by "
     "phase-lag constitutive relations, into the heat-conduction law, the constitutive equations, or both. A broad "
     "review of the resulting family of models, including the Lord–Shulman (LS), Green–Lindsay (GL), Green–Naghdi and "
     "Moore–Gibson–Thompson (MGT) theories and their modified versions, is given in [9]. Each model resolves the "
     "paradox of infinite propagation speed in a different way, and each carries characteristic predictions about how "
     "discontinuities propagate. These predictions matter for applications, because a jump in stress at a wavefront "
     "may initiate damage even when the peak value of a smooth stress field would not."))
add(("p", "The GL theory introduces two relaxation times, one in the energy equation and one in the "
     "stress–strain–temperature relation, and it is a temperature-rate-dependent theory. A well-known feature of GL "
     "theory is that the displacement field may be discontinuous across a propagating wavefront. A discontinuous "
     "displacement implies that material either separates or interpenetrates, which conflicts with the continuum "
     "hypothesis on which the theory is built. The modified Green–Lindsay (MGL) theory adds a strain-rate term to the "
     "constitutive relation [2]. With this term the displacement becomes continuous at the wavefront and the conflict "
     "with the continuum hypothesis disappears, while the temperature-rate dependence and therefore the finite-speed "
     "character of thermal propagation are retained."))
add(("p", "Since its introduction, the MGL theory has been examined from several angles. Fundamental solutions for "
     "the strain- and temperature-rate-dependent theory were derived in [3], and a Galerkin-type representation of the "
     "general solution was given in [4]. The theory has been applied with a Galerkin-type finite element approach to "
     "a functionally graded hollow disk [5] and to photothermal processes in semiconductors excited by surface "
     "absorption of laser radiation [6]. For the problem of a line heat source in an unbounded medium, Singh and "
     "Mukhopadhyay [1] showed that the MGL solution consists of one wave travelling with finite speed together with a "
     "diffusive part, so that some disturbance is present at every point for every positive time. In that problem the "
     "temperature, the displacement and the radial stress are continuous, and only the circumferential (hoop) stress "
     "jumps at the wavefront. The same authors analyzed the corresponding line-source problem within MGT "
     "thermoelasticity [7], and an MGT analysis of a continuous line heat source in an infinite solid is given in [8]. "
     "Together, [1], [7] and [8] provide a reference picture of how the different generalized theories behave for a "
     "simple excitation in an unbounded medium."))
add(("h2", "1.2  Open questions"))
add(("p", "Two aspects of this picture have not been addressed. The first concerns geometry. The line-source analysis "
     "of [1] deals with an unbounded medium without any internal boundary. In engineering structures, however, thermal "
     "shocks are very often applied to the surface of a cavity or a hole: pressure vessels and pipes, nuclear "
     "components, cryogenic tanks and cooled thin-walled parts all contain such boundaries [11,12]. A traction-free "
     "cavity wall reflects and converts waves and couples the thermal and mechanical parts of the solution through the "
     "boundary conditions. Whether the qualitative conclusions drawn for the line source, in particular which field "
     "quantities jump at the wavefront, carry over to a problem with an internal boundary is not obvious."))
add(("p", "The second aspect concerns the heat-conduction law itself. Heat transport in heterogeneous, porous, "
     "composite and functionally graded media frequently deviates from both the classical diffusive law and the "
     "single-relaxation-time wave law [10,11]. Fractional-order heat conduction provides a compact way of describing "
     "such anomalous transport: the order $\\alpha$ of a time-fractional derivative acts as a continuous parameter "
     "between diffusion and wave-like transport. How a fractional energy equation interacts with the strain-rate term "
     "that defines MGL theory has not been analyzed. In particular, it is not known whether the single finite-speed "
     "wave found in [1] survives when the time derivative of order two in the energy equation is replaced by one of "
     "order $1+\\alpha$ with $\\alpha<1$."))
add(("p", "The MGT line-source studies [7,8] serve as a natural comparison for the present work. They show that the "
     "number of wavefronts and the nature of the jumps depend sensitively on the structure of the heat-conduction law. "
     "It is therefore reasonable to expect that a change of the order of the time derivative in the energy equation "
     "changes the wavefront structure of MGL theory as well, and the purpose of this paper is to quantify that change "
     "for two canonical cavity geometries."))
add(("h2", "1.3  Contributions and outline"))
add(("p", "The contributions of the paper are as follows. (i) A fractional-order MGL formulation is set up for an "
     "unbounded medium containing a spherical cavity or a cylindrical hole whose wall is subjected to a thermal shock "
     "and is free of traction. (ii) Closed-form Laplace-domain solutions are derived for both geometries, with explicit "
     "expressions for the temperature, displacement and stresses. (iii) A large-parameter asymptotic analysis "
     "classifies the solution into wave-like and diffusive parts as a function of $\\alpha$ and predicts the loss of the "
     "sharp wavefront for $\\alpha<1$. (iv) A numerical inversion strategy is described and validated: Laplace-inversion "
     "tests on known transforms, enforcement of the boundary conditions in the time domain and a comparison with an "
     "independent finite-difference solution for $\\alpha=1$. (v) Time-domain results for copper are presented for "
     "both geometries, for four values of $\\alpha$ and for three values of the strain-rate relaxation time "
     "$\\tau_1$."))
add(("p", "Section 2 states the governing equations, the boundary and initial conditions and the nondimensional "
     "form. Sections 3 and 4 give the Laplace-domain solutions for the spherical cavity and the cylindrical hole. "
     "Section 5 contains the asymptotic analysis, and Section 6 describes the numerical inversion and its validation. "
     "Section 7 presents the numerical results, Section 8 discusses them together with the limitations of the model, "
     "and Section 9 concludes the paper."))

# ---------------------------------------------------------------- 2
add(("h1", "2  Problem formulation"))
add(("h2", "2.1  Governing equations"))
add(("p", "Consider a homogeneous, isotropic thermoelastic medium of infinite extent that contains either a spherical "
     "cavity of radius $a$ or an infinitely long circular cylindrical hole of radius $a$ (Fig. 1). The medium is "
     "initially at rest at the uniform reference temperature $T_0$. Because of the symmetry of the geometry and of the "
     "loading, the only nonzero displacement component is the radial displacement $u(r,t)$, and the temperature "
     "increment $\\theta=T-T_0$ depends only on $r$ and $t$. In the cylindrical case plane-strain conditions are assumed. "
     "The volumetric strain is"))
add(("eq", r"e=\frac{\partial u}{\partial r}+\frac{2u}{r}\quad\text{(sphere)},\qquad e=\frac{\partial u}{\partial r}+\frac{u}{r}\quad\text{(cylinder)}", 1))
add(("fig", "Figure_1.png", "Figure 1. Geometry of the problem: (a) spherical cavity and (b) cylindrical hole of radius $a$ "
     "in an unbounded isotropic MGL medium. A thermal shock $\\theta(a,t)=\\theta_0H(t)$ is applied on the traction-free "
     "wall $r=a$; all fields vanish in the far field, condition (10). The dashed circle indicates the position "
     "$r=a+v_wt$ of the thermal wavefront predicted for $\\alpha=1$ (Section 5)."))
add(("p", "In MGL theory the strain-rate relaxation time $\\tau_1$ enters the constitutive relation through the "
     "operator $1+\\tau_1\\partial/\\partial t$ acting on both the elastic and the thermal parts of the stress. For "
     "radial motion the equation of motion then reads"))
add(("eq", r"\rho\frac{\partial^{2}u}{\partial t^{2}}=\left(1+\tau_{1}\frac{\partial}{\partial t}\right)\left[(\lambda+2\mu)\frac{\partial e}{\partial r}-\gamma\frac{\partial\theta}{\partial r}\right]", 2))
add(("p", "where $\\rho$ is the mass density, $\\lambda$ and $\\mu$ are the Lamé constants and $\\gamma=(3\\lambda+2\\mu)\\alpha_t$ "
     "with $\\alpha_t$ the coefficient of linear thermal expansion. The fractional extension of the MGL energy equation "
     "adopted here is"))
add(("eq", r"k\nabla^{2}\theta=\left(\frac{\partial}{\partial t}+\frac{\tau_{0}^{\alpha}}{\Gamma(\alpha+1)}\frac{\partial^{1+\alpha}}{\partial t^{1+\alpha}}\right)(\rho c_{E}\theta+\gamma T_{0}e),\qquad 0<\alpha\le 1", 3))
add(("p", "where $k$ is the thermal conductivity, $c_E$ the specific heat at constant strain and $\\tau_0$ the thermal "
     "relaxation time. For $\\alpha=1$, Eq. (3) reduces to $k\\nabla^2\\theta=\\rho c_E(\\theta_t+\\tau_0\\theta_{tt})+"
     "\\gamma T_0(e_t+\\tau_0e_{tt})$, which coincides with the integer-order MGL energy equation of [1] up to the form "
     "of the coupling term. The fractional derivative is understood in the Caputo sense; for an order "
     "$\\beta=1+\\alpha$ with $1<\\beta\\le 2$,"))
add(("eq", r"\frac{\partial^{\beta}f}{\partial t^{\beta}}=\frac{1}{\Gamma(2-\beta)}\int_{0}^{t}{\left(t-s\right)^{1-\beta}f''(s)\,ds},\qquad 1<\beta\le 2", 4))
add(("p", "The Caputo form is chosen because its Laplace transform involves only the initial values of the function and "
     "its first derivative, which have a direct physical meaning and vanish for the problem considered here. For the "
     "spherical cavity, the radial and hoop stresses are"))
add(("eq", r"\sigma_{rr}=\left(1+\tau_{1}\frac{\partial}{\partial t}\right)\left[(\lambda+2\mu)\frac{\partial u}{\partial r}+2\lambda\frac{u}{r}-\gamma\theta\right]", 5))
add(("eq", r"\sigma_{\phi\phi}=\left(1+\tau_{1}\frac{\partial}{\partial t}\right)\left[2(\lambda+\mu)\frac{u}{r}+\lambda\frac{\partial u}{\partial r}-\gamma\theta\right]", 6))
add(("p", "with $\\tau_1\\ge\\tau_0>0$. Equations (5) and (6) hold for the sphere, in which the two hoop stresses "
     "$\\sigma_{\\phi\\phi}$ and $\\sigma_{\\vartheta\\vartheta}$ coincide. For the cylindrical hole the corresponding plane-strain "
     "forms of [1] are used: $\\sigma_{rr}$ contains $\\lambda u/r$ instead of $2\\lambda u/r$, and the hoop stress is "
     "$(1+\\tau_1\\partial_t)[\\lambda\\partial u/\\partial r+(\\lambda+2\\mu)u/r-\\gamma\\theta]$."))
add(("h2", "2.2  Initial and boundary conditions"))
add(("p", "The medium is initially undisturbed:"))
add(("eq", r"\theta=\frac{\partial\theta}{\partial t}=u=\frac{\partial u}{\partial t}=\sigma_{rr}=\sigma_{\phi\phi}=0\qquad\text{at }t=0", 7))
add(("p", "At $t=0$ the cavity wall is subjected to a sudden temperature rise of magnitude $\\theta_0$ and is kept free of "
     "traction:"))
add(("eq", r"\theta(a,t)=\theta_{0}H(t)", 8))
add(("eq", r"\sigma_{rr}(a,t)=0", 9))
add(("p", "where $H(t)$ is the Heaviside step function. Finally, all field quantities vanish far from the cavity:"))
add(("eq", r"(\theta,u,\sigma_{rr},\sigma_{\phi\phi})\to 0\qquad\text{as }r\to\infty", 10))
add(("p", "The step boundary datum (8) is a deliberately severe idealization of a thermal shock. Because it contains a "
     "discontinuity at $t=0$, any finite-speed wave generated at the wall carries a discontinuity as well, and the "
     "question of which field quantities jump at the wavefront becomes a sharp test of the model."))
add(("h2", "2.3  Nondimensionalization"))
add(("p", "Let $v=\\sqrt{(\\lambda+2\\mu)/\\rho}$ denote the speed of dilatational waves and $\\eta=\\rho c_E/k$. The "
     "following nondimensional variables are introduced:"))
add(("eq", r"r^{*}=v\eta r,\quad t^{*}=v^{2}\eta t,\quad u^{*}=v\eta u,\quad \theta^{*}=\frac{\theta}{T_{0}},\quad \sigma^{*}=\frac{\sigma}{\lambda+2\mu}", 11))
add(("p", "The relaxation times and the cavity radius are scaled in the same way as $t$ and $r$. Dropping the asterisks, "
     "the governing equations become"))
add(("eq", r"\frac{\partial^{2}u}{\partial t^{2}}=\left(1+\tau_{1}\frac{\partial}{\partial t}\right)\left(\frac{\partial e}{\partial r}-d_{1}\frac{\partial\theta}{\partial r}\right)", 12))
add(("eq", r"\nabla^{2}\theta=\left(\frac{\partial}{\partial t}+\frac{\tau_{0}^{\alpha}}{\Gamma(\alpha+1)}\frac{\partial^{1+\alpha}}{\partial t^{1+\alpha}}\right)(\theta+d_{2}e)", 13))
add(("eq", r"\sigma_{rr}=\left(1+\tau_{1}\frac{\partial}{\partial t}\right)\left[\frac{\partial u}{\partial r}+2\lambda_{1}\frac{u}{r}-d_{1}\theta\right]", 14))
add(("eq", r"\sigma_{\phi\phi}=\left(1+\tau_{1}\frac{\partial}{\partial t}\right)\left[(1+\lambda_{1})\frac{u}{r}+\lambda_{1}\frac{\partial u}{\partial r}-d_{1}\theta\right]", 15))
add(("p", "with the dimensionless constants"))
add(("eq", r"d_{1}=\frac{\gamma T_{0}}{\lambda+2\mu},\qquad d_{2}=\frac{\gamma}{\rho c_{E}},\qquad \lambda_{1}=\frac{\lambda}{\lambda+2\mu}", 16))
add(("p", "The coupling parameter is $\\varepsilon=d_1d_2$. The material data used in this work are those of copper "
     "adopted in [1] and are listed in Table 1. The derived constants of Eq. (16) were first estimated by hand and then "
     "recomputed in the code used for the numerical results; both sets of values are given in Table 2 and agree to the "
     "digits quoted."))
add(("table", "Table 1. Physical data for copper (from [1]).",
     [["Quantity", "Symbol", "Value", "Unit"],
      ["Lamé constant", "$\\lambda$", "7.76 × 10¹⁰", "N/m²"],
      ["Lamé constant (shear modulus)", "$\\mu$", "3.86 × 10¹⁰", "N/m²"],
      ["Coefficient of linear thermal expansion", "$\\alpha_t$", "1.78 × 10⁻⁵", "1/K"],
      ["Specific heat at constant strain", "$c_E$", "383.1", "J/(kg K)"],
      ["Thermal conductivity", "$k$", "386", "W/(m K)"],
      ["Mass density", "$\\rho$", "8954", "kg/m³"],
      ["Reference temperature", "$T_0$", "293", "K"],
      ["$\\eta=\\rho c_E/k$", "$\\eta$", "8886.73", "s/m²"]],
     [3600, 1300, 2100, 1600]))
add(("table", "Table 2. Derived dimensionless constants: hand estimate and value recomputed in the code.",
     [["Constant", "Definition", "Hand estimate", "Computed"],
      ["$d_1$", "$\\gamma T_0/(\\lambda+2\\mu)$", "≈ 0.0104", "%.5f" % C["d1"]],
      ["$d_2$", "$\\gamma/(\\rho c_E)$", "≈ 1.61", "%.4f" % C["d2"]],
      ["$\\varepsilon$", "$d_1d_2$", "≈ 0.0168", "%.5f" % C["eps"]],
      ["$\\lambda_1$", "$\\lambda/(\\lambda+2\\mu)$", "≈ 0.501", "%.4f" % C["lambda1"]],
      ["$\\kappa$", "$1-\\lambda_1=2\\mu/(\\lambda+2\\mu)$", "≈ 0.499", "%.4f" % C["kappa"]],
      ["$v_w$ ($\\alpha=1$, $\\tau_0=0.02$)", "$1/\\sqrt{(1+\\varepsilon)\\tau_0}$", "≈ 7.0", "%.3f" % VW]],
     [2300, 3000, 1800, 1500]))
add(("p", "With $\\gamma=%.4g$ N/(m² K) the constants are $d_1=%.5f$, $d_2=%.4f$ and $\\varepsilon=%.5f$. The small value "
     "of $\\varepsilon$ indicates weak thermomechanical coupling, as is typical for metals; the mechanical response "
     "is driven by the temperature field, while the feedback of the deformation on the temperature is small but not "
     "negligible near the wavefront." % (C["gamma"], C["d1"], C["d2"], C["eps"])))
add(("h2", "2.4  Displacement potential"))
add(("p", "Because the motion is irrotational, the displacement can be written in terms of a scalar potential $\\phi(r,t)$:"))
add(("eq", r"u=\frac{\partial\phi}{\partial r},\qquad \nabla^{2}=\frac{\partial^{2}}{\partial r^{2}}+\frac{2}{r}\frac{\partial}{\partial r}\;\text{(sphere)},\quad \nabla^{2}=\frac{\partial^{2}}{\partial r^{2}}+\frac{1}{r}\frac{\partial}{\partial r}\;\text{(cylinder)}", 17))
add(("p", "so that $e=\\nabla^2\\phi$ in both geometries. Substituting into Eqs. (12) and (13), integrating the equation of "
     "motion once with respect to $r$ and using the far-field condition (10) gives"))
add(("eq", r"\frac{\partial^{2}\phi}{\partial t^{2}}=\left(1+\tau_{1}\frac{\partial}{\partial t}\right)\left(\nabla^{2}\phi-d_{1}\theta\right)", 18))
add(("eq", r"\nabla^{2}\theta=\left(\frac{\partial}{\partial t}+\frac{\tau_{0}^{\alpha}}{\Gamma(\alpha+1)}\frac{\partial^{1+\alpha}}{\partial t^{1+\alpha}}\right)\left(\theta+d_{2}\nabla^{2}\phi\right)", 19))

# ---------------------------------------------------------------- 3
add(("h1", "3  Laplace-domain solution for the spherical cavity"))
add(("h2", "3.1  Transformed equations"))
add(("p", "The Laplace transform of a function $f(t)$ is denoted by $\\bar{f}(r,s)=\\int_0^\\infty{f(r,t)e^{-st}dt}$. For "
     "the Caputo derivative of order $1+\\alpha$ and the zero initial data (7),"))
add(("eq", r"\mathcal{L}\left\{\frac{\partial^{1+\alpha}f}{\partial t^{1+\alpha}}\right\}=s^{1+\alpha}\bar{f}", 20))
add(("p", "Introducing the abbreviations $p=1+\\tau_1s$ and $g(s)=1+\\tau_0^{\\alpha}s^{\\alpha}/\\Gamma(\\alpha+1)$, "
     "the transforms of Eqs. (18) and (19) are"))
add(("eq", r"s^{2}\bar{\phi}=p\left(\nabla^{2}\bar{\phi}-d_{1}\bar{\theta}\right)", 21))
add(("eq", r"\nabla^{2}\bar{\theta}=sg\left(\bar{\theta}+d_{2}\nabla^{2}\bar{\phi}\right)", 22))
add(("p", "Equation (21) gives $d_1\\bar\\theta=\\nabla^2\\bar\\phi-s^2\\bar\\phi/p$. Applying $\\nabla^2$, inserting the "
     "result into Eq. (22) and collecting terms eliminates the temperature and yields the fourth-order equation"))
add(("eq", r"\left[\nabla^{4}-\left(\frac{s^{2}}{p}+(1+\varepsilon)sg\right)\nabla^{2}+\frac{s^{3}g}{p}\right]\bar{\phi}=0,\qquad \varepsilon=d_{1}d_{2}", 23))
add(("p", "For $\\alpha=1$ the coefficients are rational functions of $s$ and Eq. (23) reduces to the polynomial form of "
     "[1]. For $\\alpha<1$ the coefficients contain the fractional power $s^{\\alpha}$, which is the only change "
     "introduced by the fractional law at the level of the transformed equations. Equation (23) factorizes as"))
add(("eq", r"\left(\nabla^{2}-m_{1}^{2}\right)\left(\nabla^{2}-m_{2}^{2}\right)\bar{\phi}=0", 24))
add(("p", "where $m_1^2$ and $m_2^2$ are the roots of the characteristic quadratic,"))
add(("eq", r"m_{1}^{2}+m_{2}^{2}=\frac{s^{2}}{p}+(1+\varepsilon)sg", 25))
add(("eq", r"m_{1}^{2}m_{2}^{2}=\frac{s^{3}g}{p}", 26))
add(("h2", "3.2  Decaying solutions and field expressions"))
add(("p", "For the spherical Laplacian, $\\nabla^2(e^{-mr}/r)=m^2e^{-mr}/r$. Choosing the roots with $\\mathrm{Re}\\,m_i>0$ "
     "ensures that the solution decays as $r\\to\\infty$, as required by Eq. (10). The bounded solution is therefore"))
add(("eq", r"\bar{\phi}=\frac{A_{1}e^{-m_{1}r}+A_{2}e^{-m_{2}r}}{r}", 27))
add(("p", "where $A_1$ and $A_2$ depend on $s$ only. Differentiation gives the displacement, and Eq. (21) the temperature:"))
add(("eq", r"\bar{u}=-\sum_{i=1}^{2}{A_{i}\frac{(1+m_{i}r)e^{-m_{i}r}}{r^{2}}}", 28))
add(("eq", r"\bar{\theta}=\frac{1}{d_{1}}\sum_{i=1}^{2}{\left(m_{i}^{2}-\frac{s^{2}}{p}\right)A_{i}\frac{e^{-m_{i}r}}{r}}", 29))
add(("p", "To obtain the stresses, the identity $\\phi_{rr}=\\nabla^2\\phi-(2/r)\\phi_r$ is used in the transformed Eqs. (14) "
     "and (15), and $d_1\\bar\\theta$ is replaced by $\\nabla^2\\bar\\phi-s^2\\bar\\phi/p$. The terms in $\\nabla^2\\bar\\phi$ cancel "
     "in the radial stress, and one finds"))
add(("eq", r"\bar{\sigma}_{rr}=s^{2}\bar{\phi}-2p\kappa\frac{\bar{u}}{r}", 30))
add(("eq", r"\bar{\sigma}_{\phi\phi}=s^{2}\bar{\phi}+p\kappa\left(\frac{\bar{u}}{r}-\nabla^{2}\bar{\phi}\right),\qquad \kappa=1-\lambda_{1}=\frac{2\mu}{\lambda+2\mu}", 31))
add(("p", "Equations (30) and (31) were derived by hand in the first draft of this work and have been re-derived "
     "independently for the present version. In detail, $\\bar\\sigma_{rr}/p=(\\nabla^2\\bar\\phi-2\\bar u/r)+2\\lambda_1\\bar u/r-"
     "(\\nabla^2\\bar\\phi-s^2\\bar\\phi/p)=s^2\\bar\\phi/p-2\\kappa\\bar u/r$, and $\\bar\\sigma_{\\phi\\phi}/p=(1+\\lambda_1)\\bar u/r+"
     "\\lambda_1(\\nabla^2\\bar\\phi-2\\bar u/r)-(\\nabla^2\\bar\\phi-s^2\\bar\\phi/p)=s^2\\bar\\phi/p+\\kappa(\\bar u/r-\\nabla^2\\bar\\phi)$. "
     "Both expressions are therefore confirmed and no correction was required. They were further checked numerically: "
     "the time-domain radial stress computed from Eq. (30) vanishes at $r=a$ to round-off accuracy, and the stresses "
     "agree with those of the independent finite-difference solution described in Section 6.3."))
add(("h2", "3.3  Integration constants"))
add(("p", "The thermal condition (8) transforms to $\\bar\\theta(a,s)=\\theta_0/s$ and the mechanical condition (9) to "
     "$\\bar\\sigma_{rr}(a,s)=0$. With Eqs. (28)–(30) these give the linear system"))
add(("eq", r"\sum_{i=1}^{2}{\left(m_{i}^{2}-\frac{s^{2}}{p}\right)A_{i}\frac{e^{-m_{i}a}}{a}}=\frac{d_{1}\theta_{0}}{s}", 32))
add(("eq", r"\sum_{i=1}^{2}{A_{i}\left[s^{2}+\frac{2p\kappa(1+m_{i}a)}{a^{2}}\right]\frac{e^{-m_{i}a}}{a}}=0", 33))
add(("p", "Defining $c_{1i}=(m_i^2-s^2/p)e^{-m_ia}/a$, $c_{2i}=[s^2+2p\\kappa(1+m_ia)/a^2]e^{-m_ia}/a$ and "
     "$\\Delta=c_{11}c_{22}-c_{12}c_{21}$, Cramer's rule gives"))
add(("eq", r"A_{1}=\frac{d_{1}\theta_{0}}{s}\frac{c_{22}}{\Delta}", 34))
add(("eq", r"A_{2}=-\frac{d_{1}\theta_{0}}{s}\frac{c_{21}}{\Delta}", 35))
add(("p", "In the numerical implementation the exponentially large factors $e^{m_ia}$ hidden in $A_i$ are never formed. "
     "Instead the scaled constants $B_i=A_ie^{-m_ia}/a$ are computed from Eqs. (32)–(35), and the fields are evaluated "
     "with the bounded factors $e^{-m_i(r-a)}$, which is stable for all $s$ on the inversion contour."))

# ---------------------------------------------------------------- 4
add(("h1", "4  Laplace-domain solution for the cylindrical hole"))
add(("p", "For the cylindrical Laplacian the decaying solutions of $(\\nabla^2-m^2)\\bar\\phi=0$ are $K_0(mr)$, where $K_n$ "
     "denotes the modified Bessel function of the second kind of order $n$. The roots $m_1$ and $m_2$ are the same as "
     "in Eqs. (25) and (26), again with $\\mathrm{Re}\\,m_i>0$. Thus"))
add(("eq", r"\bar{\phi}=A_{1}K_{0}(m_{1}r)+A_{2}K_{0}(m_{2}r)", 36))
add(("p", "Using $K_0'(z)=-K_1(z)$ and $\\nabla^2K_0(mr)=m^2K_0(mr)$,"))
add(("eq", r"\bar{u}=-\sum_{i=1}^{2}{A_{i}m_{i}K_{1}(m_{i}r)}", 37))
add(("eq", r"\bar{\theta}=\frac{1}{d_{1}}\sum_{i=1}^{2}{\left(m_{i}^{2}-\frac{s^{2}}{p}\right)A_{i}K_{0}(m_{i}r)}", 38))
add(("p", "In plane strain the transformed radial stress is $\\bar\\sigma_{rr}=p[\\bar u_r+\\lambda_1\\bar u/r-d_1\\bar\\theta]$. "
     "With $\\phi_{rr}=\\nabla^2\\phi-\\phi_r/r$ for the cylindrical Laplacian this becomes, following [1],"))
add(("eq", r"\bar{\sigma}_{rr}=s^{2}\bar{\phi}-p\kappa\frac{\bar{u}}{r}", 39))
add(("p", "Equation (39) was also re-derived for this version and is confirmed: $\\bar\\sigma_{rr}/p=(\\nabla^2\\bar\\phi-\\bar u/r)+"
     "\\lambda_1\\bar u/r-(\\nabla^2\\bar\\phi-s^2\\bar\\phi/p)=s^2\\bar\\phi/p-\\kappa\\bar u/r$. The same steps applied to the "
     "plane-strain hoop stress give $\\bar\\sigma_{\\phi\\phi}=s^2\\bar\\phi+p\\kappa(\\bar u/r-\\nabla^2\\bar\\phi)$, which has the "
     "same form as Eq. (31) and is used for the cylindrical results in Section 7. The traction-free and thermal "
     "conditions at $r=a$ give"))
add(("eq", r"\sum_{i=1}^{2}{A_{i}\left[s^{2}K_{0}(m_{i}a)+\frac{p\kappa m_{i}K_{1}(m_{i}a)}{a}\right]}=0", 40))
add(("eq", r"\sum_{i=1}^{2}{\left(m_{i}^{2}-\frac{s^{2}}{p}\right)A_{i}K_{0}(m_{i}a)}=\frac{d_{1}\theta_{0}}{s}", 41))
add(("p", "Let $b_i=(m_i^2-s^2/p)K_0(m_ia)$ denote the coefficient of $A_i$ in Eq. (41) and $C_i$ the coefficient of $A_i$ "
     "in Eq. (40), and let $\\Delta_c=b_1C_2-b_2C_1$ be the determinant of the system. Then"))
add(("eq", r"A_{i}=\frac{d_{1}\theta_{0}}{s}\left(\pm\frac{C_{j}}{\Delta_{c}}\right),\qquad i\neq j", 42))
add(("p", "with the plus sign for $A_1$ and the minus sign for $A_2$. For the numerical evaluation the exponentially "
     "scaled functions $K_n(z)e^{z}$ are used, so that only ratios such as $K_0(m_ir)/K_0(m_ia)$, which remain bounded "
     "for $r\\ge a$, enter the field expressions."))

# ---------------------------------------------------------------- 5
add(("h1", "5  Large-s asymptotics and wavefront structure"))
add(("p", "The behaviour of the solution at short times and near a wavefront is governed by the behaviour of the "
     "transforms for large $|s|$. For large $s$, with $0<\\alpha\\le 1$,"))
add(("eq", r"g(s)\approx\frac{\tau_{0}^{\alpha}s^{\alpha}}{\Gamma(\alpha+1)}=c_{0}s^{\alpha}", 43))
add(("p", "and $s^2/p\\approx s/\\tau_1$. The sum (25) is then dominated by $(1+\\varepsilon)c_0s^{1+\\alpha}$, because "
     "$1+\\alpha>1$, while the product (26) behaves as $c_0s^{2+\\alpha}/\\tau_1$. The two roots therefore separate into "
     "a large root $m_a$ and a small root $m_b$:"))
add(("eq", r"m_{a}^{2}\approx(1+\varepsilon)c_{0}s^{1+\alpha}", 44))
add(("eq", r"m_{b}^{2}\approx\frac{s}{(1+\varepsilon)\tau_{1}}", 45))
add(("h2", "5.1  Integer order, α = 1"))
add(("p", "For $\\alpha=1$ one has $c_0=\\tau_0$ and $m_a\\approx\\sqrt{(1+\\varepsilon)\\tau_0}\\,s$. A factor $e^{-m_ar}$ is "
     "then, to leading order, a pure time delay, and the corresponding contribution is a wavefront that travels with "
     "speed $v_w=1/\\sqrt{(1+\\varepsilon)\\tau_0}$. This is the speed denoted $1/a_{61}$ in [1], since $a_{51}=(1+\\varepsilon)"
     "\\tau_0$ there. For the copper data and $\\tau_0=0.02$, $v_w=%.3f$. The small root satisfies $m_b\\propto\\sqrt{s}$, "
     "which is the signature of diffusion; the corresponding contribution has no front and is felt instantaneously at "
     "every point. Hence the cavity problems have the same structure as the line-source problem of [1]: one "
     "finite-speed wave plus one diffusive part. Note that $v_w$ is independent of $\\tau_1$, whereas $m_b$ depends on "
     "$\\tau_1$ through Eq. (45); the strain-rate term affects the diffusive part but not the speed of the wave." % VW))
add(("h2", "5.2  Fractional order, 0 < α < 1"))
add(("p", "For $0<\\alpha<1$ the large root grows as $m_a\\propto s^{(1+\\alpha)/2}$ with exponent $(1+\\alpha)/2<1$. The "
     "inverse transform of $\\exp(-cs^{\\beta}r)$ with $0<\\beta<1$ is a one-sided stable probability density, which is "
     "positive for all $t>0$ and has no compact support. The contribution of $m_a$ therefore no longer propagates with a "
     "sharp front, and both parts of the solution are diffusive in the leading-order sense. The analysis predicts that "
     "the sharp wavefront of the $\\alpha=1$ solution disappears and that the stress jump is smoothed into a steep but "
     "continuous layer. At the level of the asymptotics this is a conjecture, because the corrections to Eqs. (44) and "
     "(45) are not controlled uniformly in $r$ and $t$; it is tested numerically in Section 7. The classification is "
     "summarized in Table 3, which also records the numerical observation made in this work."))
add(("table", "Table 3. Asymptotic classification of the roots and the resulting wavefront structure.",
     [["Order", "Large root $m_a$", "Small root $m_b$", "Leading-order prediction", "Numerical observation (Section 7)"],
      ["$\\alpha=1$", "$\\propto s$", "$\\propto s^{1/2}$", "One finite-speed wave plus diffusive part",
       "Jump at $r=a+v_wt$, $v_w\\approx 7.01$; diffusive precursor ahead"],
      ["$0<\\alpha<1$", "$\\propto s^{(1+\\alpha)/2}$", "$\\propto s^{1/2}$", "No wavefront (conjectured: smoothed layer)",
       "No jump for $\\alpha=0.5$, $0.75$, $0.9$; continuous layer steepening as $\\alpha\\to 1$"]],
     [1200, 1500, 1400, 2400, 2600]))

# ---------------------------------------------------------------- 6
add(("h1", "6  Numerical Laplace inversion"))
add(("h2", "6.1  Fourier-series (Durbin) inversion"))
add(("p", "The transforms obtained in Sections 3 and 4 are inverted numerically with the Fourier-series method of "
     "Durbin type. For a real constant $c$ to the right of all singularities and a half-period $T$, the inversion "
     "formula, valid for $0<t<2T$, reads"))
add(("eq", r"f(t)\approx\frac{e^{ct}}{T}\left[\frac{1}{2}\bar{f}(c)+\sum_{k=1}^{N}{\left(\mathrm{Re}\,\bar{f}(s_{k})\cos\frac{k\pi t}{T}-\mathrm{Im}\,\bar{f}(s_{k})\sin\frac{k\pi t}{T}\right)}\right],\quad s_{k}=c+\frac{ik\pi}{T}", 46))
add(("p", "The discretization (aliasing) error is of order $e^{-2cT}$ relative to the solution, and the truncation of the "
     "series is controlled by the criterion"))
add(("eq", r"\frac{\left|f_{N}(t)-f_{N/2}(t)\right|}{\left|f_{N}(t)\right|}<10^{-6}", 47))
add(("p", "In this work $ct=6$ and $T=2t$ are used for each output time, so that the aliasing error is of order "
     "$e^{-24}\\approx 4\\times 10^{-11}$. Because the solutions for $\\alpha=1$ contain jumps in $r$ and $t$, the Fourier "
     "series converges slowly. The partial sums are therefore accelerated with the Wynn epsilon algorithm applied to "
     "the last 60 partial sums, with $N=4000$; the comparison required by Eq. (47) is made between $N=4000$ and $N=2000$, "
     "both accelerated. The fractional power $s^{\\alpha}$ is evaluated on the principal branch, which is analytic in "
     "$\\mathrm{Re}\\,s>0$, and the roots are taken with $\\mathrm{Re}\\,m_i>0$. The two values $m_1^2$ and $m_2^2$ are "
     "computed from Eqs. (25) and (26) in a cancellation-free way: the root of larger modulus is taken from the "
     "quadratic formula and the smaller one from the product (26)."))
add(("h2", "6.2  Modified Bessel functions of complex argument"))
add(("p", "The cylindrical solution requires $K_0(z)$ and $K_1(z)$ for complex $z=m_ir$ with $\\mathrm{Re}\\,z>0$. Since "
     "no special-function library was used, both functions were implemented directly in exponentially scaled form "
     "$K_n(z)e^{z}$. For $|z|\\le 2$ the ascending series are used; for $|z|>2$ the integral representation "
     "$K_n(z)e^z=\\sqrt{\\pi/(2z)}\\,\\Gamma(n+1/2)^{-1}\\int_0^\\infty{e^{-u}u^{n-1/2}(1+u/(2z))^{n-1/2}du}$ is evaluated "
     "with the trapezoidal rule after the substitution $u=w^2$, which is spectrally accurate here. The implementation "
     "reproduces tabulated real values to better than $5\\times 10^{-10}$, the two branches agree to about "
     "$10^{-15}$ on $|z|=2$, and the integral branch agrees with the large-argument asymptotic expansion to about "
     "$10^{-14}$ for $|z|\\ge 30$, including arguments close to the imaginary axis."))
add(("h2", "6.3  Validation"))
add(("p", "Four independent checks were carried out. (a) Inversion of known transforms: for $\\bar f=e^{-k\\sqrt{s}}/s$ "
     "the inverted values at $t=0.007$ agree with $\\mathrm{erfc}(k/(2\\sqrt{t}))$ to seven digits for $k=0.01$ and "
     "$0.03$, and for the delayed step $e^{-t_ds}/s$ with a jump only $10^{-4}$ before or after the output time the "
     "error is below $3\\times 10^{-5}$. (b) Boundary conditions in the time domain: in every computed case "
     "$\\theta(a,t)=\\theta_0$ to ten digits and $|\\sigma_{rr}(a,t)|<2\\times 10^{-13}$. (c) Truncation criterion (47): "
     "for $\\alpha<1$ it is satisfied at 99.9 per cent of the output points (the remaining point is the wall value of "
     "$\\sigma_{rr}$, which is itself of round-off size), with a maximum change between $N=2000$ and $N=4000$ below "
     "$4\\times 10^{-9}$ of the field maximum. For $\\alpha=1$ it is satisfied at 97 to 98 per cent of the points. The "
     "points that fail are concentrated near the wavefront, where the solution is discontinuous and the value at the "
     "jump itself is not defined: in all $\\alpha=1$ cases except $t=0.009$ they lie within $0.004$ of $r=a+v_wt$, and "
     "for $t=0.009$ a few isolated points nearer the wall fail as well. Outside two grid spacings "
     "($\\Delta r=2.5\\times 10^{-4}$) of the front the change between $N=2000$ and $N=4000$ never exceeds "
     "$2\\times 10^{-4}$ of the field maximum, which is far below the resolution of the figures. (d) Comparison with an independent finite-difference solution for "
     "$\\alpha=1$, described next."))
add(("p", "Instead of the short-time asymptotic solution of [1], which applies to the line source and not directly to "
     "the cavity geometry, the $\\alpha=1$ results were compared with an explicit finite-difference solution of the "
     "time-domain equations (12)–(15) with the conditions (7)–(10). The scheme uses a staggered grid with the "
     "temperature at the nodes and the displacement at half-nodes, a ghost node to impose the traction condition, and "
     "the fully coupled energy equation including the term $d_2\\tau_0e_{tt}$. For the sphere at $t=0.007$ and "
     "$\\Delta r=1.25\\times 10^{-4}$, the temperatures at $r=0.02$ and $0.04$ are $0.4840$ and $0.2269$ against $0.4837$ "
     "and $0.2256$ from the Laplace solution; the displacements at $r=0.03$ and $0.07$ are $2.2218\\times 10^{-5}$ and "
     "$2.0287\\times 10^{-6}$ against $2.2267\\times 10^{-5}$ and $2.0295\\times 10^{-6}$; and the radial stress at "
     "$r=0.07$ is $-1.628\\times 10^{-2}$ against $-1.604\\times 10^{-2}$. For the cylinder with $\\Delta r=2.5\\times 10^{-4}$ "
     "the temperatures at $r=0.02$ and $0.03$ are $0.7502$ and $0.6030$ against $0.7545$ and $0.6096$, and the "
     "displacement at $r=0.04$ is $3.2473\\times 10^{-5}$ against $3.2561\\times 10^{-5}$. The finite-difference values "
     "converge towards the Laplace values as the grid is refined. Behind the wavefront the finite-difference stresses "
     "show grid-scale oscillations generated by the discontinuity, so the stress comparison there is qualitative "
     "only; ahead of the front the stresses agree to about 2 per cent."))

# ---------------------------------------------------------------- 7
add(("h1", "7  Numerical results"))
add(("h2", "7.1  Computation plan"))
add(("p", "All results are for the copper data of Table 1 and are given in nondimensional form. The relaxation times "
     "are $\\tau_0=0.02$ and $\\tau_1=0.05$ unless stated otherwise, the shock amplitude is $\\theta_0=1$ and the "
     "nondimensional cavity radius is chosen as $a=0.01$. The output times are $t=0.005$, $0.007$ and $0.009$, at which "
     "the $\\alpha=1$ wavefront is located at $r=a+v_wt=0.0451$, $0.0591$ and $0.0731$. The fractional orders are "
     "$\\alpha=0.5$, $0.75$, $0.9$ and $1.0$. The fields are evaluated on 321 equally spaced points in $0.01\\le r\\le 0.09$ "
     "for the sphere and on 161 points for the cylinder. Vertical dotted lines in the figures mark the predicted "
     "wavefront position $r=a+v_wt$."))
add(("h2", "7.2  Spherical cavity, α = 1"))
add(("fig", "Figure_2.png", "Figure 2. Temperature $\\theta$ versus $r$ for the spherical cavity at $t=0.005$, $0.007$ and "
     "$0.009$ ($\\alpha=1$, $\\tau_0=0.02$, $\\tau_1=0.05$, $a=0.01$). Dotted lines: $r=a+v_wt$."))
add(("p", "Figure 2 shows the temperature. As expected, $\\theta$ attains its maximum $\\theta_0=1$ at the wall and "
     "decreases monotonically with $r$. Behind the wavefront the profile is almost independent of time over the short "
     "interval considered (for example $\\theta(0.03,t)=0.3112$, $0.3116$ and $0.3121$ at the three times), so the main "
     "effect of increasing time is the advance of the front. At the front the temperature drops by a finite amount, "
     "from about $0.143$ to about $0.008$ at $t=0.007$. Ahead of the front a small but nonzero diffusive precursor is "
     "present, e.g. $\\theta(0.07,0.007)\\approx 1.4\\times 10^{-3}$, in agreement with the one-wave-plus-diffusion "
     "structure of Section 5.1. The temperature jump differs from the continuous temperature found in the line-source "
     "problem [1]; it is attributed to the discontinuous boundary datum (8), which is transported by the wave part of "
     "the solution and attenuated by the geometric factor $a/r$ and by damping."))
add(("fig", "Figure_3.png", "Figure 3. Radial displacement $u$ versus $r$ for the spherical cavity at $t=0.005$, $0.007$ and "
     "$0.009$ ($\\alpha=1$). Values are shown multiplied by $10^5$."))
add(("p", "The displacement (Fig. 3) is continuous everywhere, including at the wavefront, where only its slope changes "
     "abruptly. This is the property that distinguishes MGL from GL theory. The cavity wall moves inwards "
     "($u(a,0.007)=-2.26\\times 10^{-5}$): the heated layer next to the wall expands, and since the surrounding cold "
     "material restrains it, the expansion is accommodated partly towards the cavity. Further out the displacement "
     "becomes positive, reaches a maximum of about $2.3\\times 10^{-5}$ near $r\\approx 0.027$ and decays beyond the "
     "front."))
add(("fig", "Figure_4.png", "Figure 4. Radial stress $\\sigma_{rr}$ versus $r$ for the spherical cavity at $t=0.005$, $0.007$ "
     "and $0.009$ ($\\alpha=1$). Values are shown multiplied by $10^2$. The traction-free condition $\\sigma_{rr}(a,t)=0$ is "
     "satisfied to round-off accuracy."))
add(("p", "The radial stress (Fig. 4) vanishes at the wall in accordance with Eq. (9); the computed values are of "
     "order $10^{-14}$. Behind the front $\\sigma_{rr}$ is small ($|\\sigma_{rr}|\\lesssim 1.1\\times 10^{-3}$). At the front "
     "it jumps to a compressive peak of $-0.109$, $-0.077$ and $-0.058$ at $t=0.005$, $0.007$ and $0.009$ and then decays "
     "smoothly ahead of the front. The compressive region ahead of the thermal front is associated with the "
     "diffusive part of the solution, which is present at every point for $t>0$ (Section 5.1); its sensitivity to "
     "$\\tau_1$ is examined in Section 7.5. In contrast to the line-source result of [1], where the radial "
     "stress is continuous, the computed radial stress is discontinuous for the cavity with step heating."))
add(("fig", "Figure_5.png", "Figure 5. Hoop stress $\\sigma_{\\phi\\phi}$ versus $r$ for the spherical cavity at $t=0.005$, "
     "$0.007$ and $0.009$ ($\\alpha=1$). Values are shown multiplied by $10^2$."))
add(("p", "The hoop stress (Fig. 5) is compressive at the cavity wall ($\\sigma_{\\phi\\phi}(a,0.007)=-1.95\\times 10^{-3}$), "
     "becomes weakly tensile in an intermediate zone with a maximum of about $8\\times 10^{-4}$ near $r\\approx 0.029$, and "
     "jumps at the wavefront to a compressive peak of $-0.041$, $-0.032$ and $-0.025$ at the three times. The peak decays "
     "as the front moves outwards, consistent with geometric spreading. The jump in $\\sigma_{\\phi\\phi}$ is the counterpart "
     "of the hoop-stress jump found for the line source [1]."))
add(("h2", "7.3  Effect of the fractional order"))
add(("fig", "Figure_6.png", "Figure 6. Effect of the fractional order on (a) the temperature and (b) the hoop stress for "
     "the spherical cavity at $t=0.007$, for $\\alpha=0.5$, $0.75$, $0.9$ and $1.0$ ($\\tau_0=0.02$, $\\tau_1=0.05$). Stresses "
     "are shown multiplied by $10^2$."))
add(("p", "Figure 6 tests the conjecture of Section 5.2. For $\\alpha=1$ the temperature has a jump at $r=0.0591$ and the "
     "steepest gradient of the profile, $|\\partial\\theta/\\partial r|\\approx 540$, occurs at the front. For $\\alpha=0.5$, "
     "$0.75$ and $0.9$ no jump is present: the steepest gradient, about 100 to 105, occurs at the wall, and the "
     "temperature decreases smoothly. The disturbance also extends further: at $r=0.07$ the temperatures are $0.061$, "
     "$0.056$ and $0.027$ for $\\alpha=0.5$, $0.75$ and $0.9$, against $1.4\\times 10^{-3}$ for $\\alpha=1$. The hoop stress in "
     "Fig. 6(b) is more revealing. For $\\alpha=0.9$ the jump is replaced by a steep but continuous compressive layer "
     "with a peak of $-0.024$ near $r\\approx 0.070$. For $\\alpha=0.75$ the layer is broader with a peak of $-0.009$ near "
     "$r\\approx 0.079$, and for $\\alpha=0.5$ the stress is a gentle compressive plateau of about $-0.004$. The "
     "convergence criterion (47) is satisfied for these cases at practically all points, which supports the "
     "conclusion that the profiles are genuinely smooth rather than under-resolved jumps. Within the parameter range "
     "computed, the numerical results thus confirm the leading-order prediction: the sharp front is lost for "
     "$\\alpha<1$, and the stress jump turns into a continuous layer whose steepness increases as $\\alpha$ approaches 1."))
add(("h2", "7.4  Spherical cavity versus cylindrical hole"))
add(("fig", "Figure_7.png", "Figure 7. Comparison of the spherical cavity and the cylindrical hole at $t=0.007$ "
     "($\\alpha=1$, $\\tau_0=0.02$, $\\tau_1=0.05$, $a=0.01$): (a) temperature, (b) hoop stress (multiplied by $10^2$)."))
add(("p", "Figure 7 compares the two geometries. The wavefront is located at the same position in both, as expected, "
     "since $v_w$ depends only on the material and on $\\tau_0$. The temperature behind the front is much higher in the "
     "cylindrical case ($\\theta(0.03)=0.610$ against $0.312$), reflecting the weaker geometric spreading of the "
     "cylindrical kernel $K_0(mr)$ compared with $e^{-mr}/r$. The mechanical response is correspondingly stronger: the "
     "wall displacement is $-7.2\\times 10^{-5}$ against $-2.3\\times 10^{-5}$, the hoop stress at the wall is "
     "$-2.07\\times 10^{-2}$ against $-1.95\\times 10^{-3}$, about ten times larger, and the hoop-stress peak at the front is "
     "$-0.080$ against $-0.032$. The cylindrical geometry is therefore the more severe one for compressive hoop stress "
     "at the wall under the same thermal shock."))
add(("h2", "7.5  Effect of the strain-rate relaxation time"))
add(("fig", "Figure_8.png", "Figure 8. Effect of the strain-rate relaxation time $\\tau_1$ on the hoop stress "
     "$\\sigma_{\\phi\\phi}$ for the spherical cavity at $t=0.007$ ($\\alpha=1$, $\\tau_0=0.02$ fixed; $\\tau_1=0.03$, "
     "$0.05$, $0.08$). Values are shown multiplied by $10^2$."))
add(("p", "Figure 8 isolates the strain-rate effect that distinguishes MGL from GL theory. In agreement with Section "
     "5.1, the position of the wavefront does not depend on $\\tau_1$, and the temperature behind the front is "
     "practically unchanged ($\\theta(0.03)=0.3116$ in all three cases). The hoop stress, however, depends markedly on "
     "$\\tau_1$. At the wall it is $-4.9\\times 10^{-3}$ for $\\tau_1=0.03$, $-1.95\\times 10^{-3}$ for $\\tau_1=0.05$ and "
     "$+8.9\\times 10^{-4}$ for $\\tau_1=0.08$, so in the computed case it changes sign from compression to tension between "
     "$\\tau_1=0.05$ and $\\tau_1=0.08$. The compressive peak at the front decreases in magnitude with increasing $\\tau_1$ "
     "($-0.034$, $-0.032$ and $-0.028$), while the compressive tail ahead of the front becomes broader, consistent with "
     "Eq. (45), according to which a larger $\\tau_1$ slows the diffusive part."))

# ---------------------------------------------------------------- 8
add(("h1", "8  Discussion"))
add(("p", "Table 4 recalls the predictions of the different generalized theories for the line-source problem, as "
     "reported in [1] and [7]. It is included as context; the entries are not new results of this paper."))
add(("table", "Table 4. Predictions of generalized theories for the line-source problem (context from [1,7]; not new results).",
     [["Theory", "Number of wavefronts", "Speed", "Jumps at the wavefront", "Displacement"],
      ["LS", "Two", "Finite", "Infinite jump in temperature and stress", "Continuous"],
      ["GL", "Two", "Finite", "Finite jump", "Discontinuous"],
      ["QMGT", "Two", "Finite", "Infinite jump", "Continuous"],
      ["MGL", "One wave plus diffusive part", "Finite (wave); infinite (diffusive part)", "Continuous except hoop-stress jump", "Continuous"]],
     [1000, 1900, 1900, 2500, 1700]))
add(("h2", "8.1  Effect of the internal boundary"))
add(("p", "In the unbounded line-source problem the two roots of the characteristic equation contribute independently. "
     "In the cavity problems they are coupled through the boundary conditions: the traction-free condition (33) and its "
     "cylindrical counterpart (40) enter the determinants $\\Delta$ and $\\Delta_c$, and therefore both constants $A_1$ and "
     "$A_2$. The cavity wall thus redistributes the energy of the thermal shock between the wave-like and the diffusive "
     "parts of the solution. The computations show one consequence of this coupling, combined with the step datum (8): "
     "in the cavity problems the temperature and the radial stress jump at the front in addition to the hoop stress, "
     "whereas in the line-source problem [1] only the hoop stress jumps. The displacement remains continuous in all "
     "cases, so the essential MGL property is preserved. It should be emphasized that the two problems differ both in "
     "geometry and in excitation, so the difference in jump structure cannot be attributed to the boundary alone; a "
     "cavity problem with a smooth ramp heating would separate the two effects."))
add(("h2", "8.2  Role of the fractional order"))
add(("p", "Table 3 indicates that $\\alpha=1$ is a singular limit for wave behaviour. For every $\\alpha<1$ the large root "
     "grows more slowly than $s$, so no part of the solution propagates as a delayed copy of the boundary datum. The "
     "numerical results of Fig. 6 are consistent with this. Already for $\\alpha=0.9$ the temperature and hoop stress "
     "are continuous, although the hoop stress retains a steep compressive layer. The transition from a jump at "
     "$\\alpha=1$ to a smooth layer at $\\alpha=0.9$ is abrupt in the sense of continuity, but gradual in the sense of "
     "steepness, which is the behaviour expected from a singular limit. From a modelling point of view this implies "
     "that conclusions drawn from an integer-order generalized theory about stress jumps and wavefront-induced damage "
     "may change qualitatively when the heat transport in a real material is better described by a fractional law. "
     "Conversely, experimental evidence of sharp thermal fronts in a given material would constrain $\\alpha$ to be "
     "close to 1."))
add(("p", "A second observation from Fig. 6 is that the disturbance for $\\alpha<1$ reaches further into the medium at a "
     "given time than for $\\alpha=1$. Two factors contribute: the absence of a finite front, and the larger value of the "
     "coefficient $c_0=\\tau_0^{\\alpha}/\\Gamma(\\alpha+1)$ for $\\alpha<1$ at $\\tau_0=0.02$, which changes the balance between "
     "the two terms of $g(s)$. The comparison between different $\\alpha$ at fixed $\\tau_0$ therefore mixes a change in "
     "the order of the law with a change in its effective time scale, and a comparison at matched effective relaxation "
     "time would be a useful complement."))
add(("h2", "8.3  Role of the strain-rate term"))
add(("p", "For $\\alpha=1$ the factor $p=1+\\tau_1s$ appears in Eqs. (21), (25), (26) and (30). It is the feature that "
     "distinguishes MGL from GL theory, and Fig. 8 isolates its effect. Because $v_w$ does not depend on $\\tau_1$, the "
     "strain-rate term does not change where the wavefront is, but it changes the stress distribution behind and ahead "
     "of it, and it can reverse the sign of the hoop stress at the wall. From an engineering point of view this means "
     "that the wall stress, which is often the quantity of interest for failure assessment, is sensitive to a "
     "parameter that has no counterpart in GL theory. Reliable values of $\\tau_1$ for real materials are therefore "
     "important if MGL theory is to be used for quantitative predictions."))
add(("h2", "8.4  Limitations"))
add(("p", "The following limitations should be kept in mind. (i) The fractional law (3) is a modelling choice; its "
     "thermodynamic consistency has not been proven here. (ii) Equations (30), (31) and (39) were originally derived by "
     "hand; they have been re-derived and checked numerically, but an independent symbolic verification is "
     "recommended before publication. (iii) The asymptotic classification is of leading order only. The numerical "
     "confirmation of the loss of the front covers $\\alpha=0.5$, $0.75$ and $0.9$ at a spatial resolution of "
     "$\\Delta r=2.5\\times 10^{-4}$; a layer narrower than this resolution for $\\alpha$ very close to 1 cannot be "
     "excluded. (iv) The validation of the $\\alpha=1$ solution uses an independent finite-difference scheme rather "
     "than the short-time asymptotic solution of [1], which applies to a different problem; no independent time-domain "
     "check was made for $\\alpha<1$. (v) Only one cavity radius ($a=0.01$), one shock amplitude and very short times "
     "($t<\\tau_0$) were considered."))

# ---------------------------------------------------------------- 9
add(("h1", "9  Conclusions"))
add(("p", "A fractional-order modified Green–Lindsay model has been formulated for an unbounded medium containing a "
     "spherical cavity or a cylindrical hole subjected to a thermal shock on a traction-free wall. Closed-form "
     "Laplace-domain solutions were obtained in both geometries, using $e^{-mr}/r$ for the sphere and $K_0(mr)$ for the "
     "cylinder. The stress expressions (30), (31) and (39) were re-derived and confirmed. The main conclusions are:"))
add(("p", "(1) For $\\alpha=1$ the solution consists of one finite-speed wave with $v_w=1/\\sqrt{(1+\\varepsilon)\\tau_0}"
     "\\approx 7.01$ plus a diffusive part, as in the MGL line-source problem. With step heating of the cavity wall, the "
     "temperature, radial stress and hoop stress jump at the front, while the displacement remains continuous."))
add(("p", "(2) For $0<\\alpha<1$ the leading-order analysis predicts that no sharp wavefront exists. The numerical "
     "inversion confirms this for $\\alpha=0.5$, $0.75$ and $0.9$: no jump is found, and the hoop-stress front is "
     "replaced by a continuous compressive layer that steepens as $\\alpha$ approaches 1."))
add(("p", "(3) The cylindrical hole produces higher temperatures and roughly ten times larger compressive hoop stress at "
     "the wall than the spherical cavity under the same shock."))
add(("p", "(4) The strain-rate relaxation time $\\tau_1$ does not affect the wavefront position but strongly affects the "
     "hoop stress; in the computed case the wall hoop stress changes from compression to tension between "
     "$\\tau_1=0.05$ and $0.08$."))
add(("p", "Future work should address smooth (ramp-type) heating to separate the effects of the boundary datum and the "
     "geometry, a study of the limit $\\alpha\\to 1$ at higher resolution, and the thermodynamic consistency of the "
     "fractional MGL energy equation."))

add(("h1u", "Data and code availability"))
add(("p", "The Laplace-domain solution, the numerical inversion, the finite-difference check and the figure scripts "
     "used for this manuscript are pure Python scripts (files mgl.py, fd_check.py, compute_all.py and make_figures.py) "
     "and are available from the authors on request."))

# ---------------------------------------------------------------- refs
add(("h1u", "References"))
REFS = [
    ("R. V. Singh and S. Mukhopadhyay, “Mathematical significance of strain rate and temperature rate on heat conduction in thermoelastic material due to line heat source,” J. Therm. Stresses, vol. 46, no. 11, pp. 1164–1179, 2023.", "10.1080/01495739.2023.2246523"),
    ("R. V. Singh and S. Mukhopadhyay, “An investigation on strain and temperature rate-dependent thermoelasticity and its infinite speed behavior,” J. Therm. Stresses, vol. 43, no. 3, pp. 269–283, 2020.", "10.1080/01495739.2019.1680333"),
    ("B. Singh, M. Gupta and S. Mukhopadhyay, “On the fundamental solutions for the strain and temperature rate-dependent generalized thermoelasticity theory,” J. Therm. Stresses, vol. 43, no. 5, pp. 650–664, 2020.", "10.1080/01495739.2020.1736967"),
    ("M. Gupta and S. Mukhopadhyay, “Galerkin-type solution for the theory of strain and temperature rate-dependent thermoelasticity,” Acta Mech., vol. 230, no. 10, pp. 3633–3643, 2019.", "10.1007/s00707-019-02482-z"),
    ("O. N. Shivay and S. Mukhopadhyay, “A complete Galerkin's type approach of finite element for the solution of a problem on modified Green–Lindsay thermoelasticity for a functionally graded hollow disk,” Eur. J. Mech. A/Solids, vol. 80, p. 103914, 2020.", "10.1016/j.euromechsol.2019.103914"),
    ("I. M. Tayel and K. Lotfy, “Photothermal effects in semiconductors induced by surface absorption of a uniform laser radiation under modified Green–Lindsay theory,” Eur. Phys. J. Plus, vol. 136, no. 9, pp. 1–17, 2021.", "10.1140/epjp/s13360-021-01941-8"),
    ("R. V. Singh and S. Mukhopadhyay, “Study of wave propagation in an infinite solid due to a line heat source under Moore–Gibson–Thompson thermoelasticity,” Acta Mech., vol. 232, no. 12, pp. 4747–4760, 2021.", "10.1007/s00707-021-03073-7"),
    ("A. E. Abouelregal et al., “Thermoelastic processes by a continuous heat source line in an infinite solid via Moore–Gibson–Thompson thermoelasticity,” Materials, vol. 13, no. 19, p. 4463, 2020.", "10.3390/ma13194463"),
    ("F. Shakeriaski, M. Ghodrat, J. Escobedo-Diaz and M. Behnia, “Recent advances in generalized thermoelasticity theory and the modified models: a review,” J. Comput. Des. Eng., vol. 8, no. 1, pp. 15–35, 2021.", "10.1093/jcde/qwaa082"),
    ("A. Krysko, J. Awrejcewicz, S. Pavlov, K. Bodyagina and V. Krysko, “Topological optimization of thermoelastic composites with maximized stiffness and heat transfer,” Compos. Part B: Eng., vol. 158, pp. 319–327, 2019.", "10.1016/j.compositesb.2018.09.047"),
    ("A. Babaee and J. Jelovica, “Nonlinear transient thermoelastic response of FGM plate under sudden cryogenic cooling,” Ocean Eng., vol. 226, p. 108875, 2021.", "10.1016/j.oceaneng.2021.108875"),
    ("A. Babaee and J. Jelovica, “Large amplitude vibration of annular and circular functionally graded composite plates under cooling thermal shocks,” Thin-Walled Struct., vol. 182, p. 110142, 2023.", "10.1016/j.tws.2022.110142"),
]
for i, (t, d) in enumerate(REFS, 1):
    add(("ref", "[%d] %s DOI: " % (i, t), d))
add(("note", "Note to authors: 22 further verified references (2019–2026) must be added to reach the required total of "
     "34. Only the 12 references above have been verified; no additional references or DOIs have been inserted."))
