# -*- coding: utf-8 -*-
from cb import *
import fem
from tables import *
CE = fem.CER
q0 = fem.Props(n=1.0, phi0=0.2).ratios(1e-6)
q0n = fem.Props(n=1.0).ratios(1e-6)
qfar = fem.Props(n=1.0, phi0=0.2).ratios(2.0)
PR = R["prof"]

H1("3. Property models for graded and porous media")
H2("3.1 Radial grading")
P("The medium is a mixture of two constituents. The first, called the reference phase, has the copper data of Table 1 and all its property ratios equal to one. The second, called the contrast phase, has fixed ratios $\\chi_Y$ to the reference phase. "
  "The contrast phase is a hypothetical stiff, poorly conducting, light ceramic-like constituent; its ratios in Table 2 are illustrative and are not calibrated to a specific material, because the aim is a controlled test of the numerical method with a clear contrast, not a prediction for a named compound. "
  "The volume fraction of the reference phase is $V_m(r)$. A power-law grading over a zone of thickness $L_g$ is")
EQ(r"V_m(r)=\begin{cases}\end{cases}".replace(r"\begin{cases}\end{cases}", r"\left(\frac{r}{L_g}\right)^{n}\ (r<L_g),\qquad V_m=1\ (r\ge L_g)"), "vm")
P("so that the contrast phase is concentrated at the source and the medium is homogeneous reference material beyond $L_g$. The exponent $n\\ge 0$ is the grading exponent: $n=0$ gives $V_m\\equiv 1$ and recovers the homogeneous medium, whereas a large $n$ keeps the contrast phase dominant over most of the zone. "
  "An exponential alternative with a shape parameter $\\beta>0$, which is also continuous at $r=L_g$, is")
EQ(r"V_m(r)=\frac{e^{\beta r/L_g}-1}{e^{\beta}-1}\quad(r<L_g)")
P("The linear rule of mixtures gives each property ratio as a weighted average of the two phases,")
EQ(r"\hat Y(r)=V_m(r)+\left[1-V_m(r)\right]\chi_Y,\qquad Y\in\{\lambda,\mu,k,\rho,\alpha,c\}", "mix")
P("The rule of mixtures is the simplest estimate and it is known to be crude for strongly contrasting phases; it was chosen for transparency. Self-consistent or Mori–Tanaka estimates, which are classical, could be substituted without changing the finite element formulation, since the scheme only needs point values of the ratios. "
  "In this study $\\chi_\\lambda=\\chi_\\mu=" + g(CE["lam"], 2) + "$, $\\chi_k=" + g(CE["k"], 2) + "$, $\\chi_\\rho=" + g(CE["rho"], 2) + "$, $\\chi_\\alpha=" + g(CE["alpha"], 2) + "$ and $\\chi_c=" + g(CE["c"], 2) + "$, and $L_g=1$. The grading zone is long enough that the front crosses it in the observed time window, and the transition at $r=L_g$ is a node of every mesh used.")
H2("3.2 Porosity")
P("A porosity $\\phi(r)$ is the volume fraction of voids. It is written as a peak value $\\phi_0$ times a profile $w(r)$, with $w=1$ for uniform porosity and $w=1-V_m$ for porosity that is concentrated in the graded zone and vanishes outside it:")
EQ(r"\phi(r)=\phi_0\,w(r),\qquad w(r)=1\ \ \text{or}\ \ w(r)=1-V_m(r)")
P("The effective properties use three simple, widely used power-law reductions that are stated here as modelling assumptions. The elastic moduli follow a squared dependence, the conductivity a three-halves power that corresponds to the Bruggeman estimate for non-conducting spherical voids, and the density decreases linearly. The mass-specific heat and the thermal expansion coefficient are left unchanged:")
EQ(r"\hat\lambda\to(1-\phi)^2\hat\lambda,\quad \hat\mu\to(1-\phi)^2\hat\mu,\quad \hat k\to(1-\phi)^{3/2}\hat k,\quad \hat\rho\to(1-\phi)\hat\rho,\quad \hat c\to\hat c,\quad \hat\alpha\to\hat\alpha", "por")
P("The exponents are inputs; other published exponents change the numbers but not the method. The combination $\\hat\\rho\\hat c$ that multiplies $\\partial_t\\theta$ is the volumetric heat capacity, and it falls linearly with $1-\\phi$. "
  "The coefficients that enter the equations are then")
EQ(r"P=\lambda_1\hat\lambda+\kappa\hat\mu,\qquad L=\lambda_1\hat\lambda")
EQ(r"g=\hat\alpha\,\frac{3\lambda_0\hat\lambda+2\mu_0\hat\mu}{3\lambda_0+2\mu_0}")
TAB(*T2())
P("Table 2 lists the ratios at the source ($r\\to 0$) and in the far field for the grading law with $n=1$ and for the combination with a uniform porosity $\\phi_0=0.2$, evaluated by the program that produces all the results.")
H2("3.3 Local wave speed")
P("The speed of the thermal wave in a locally uniform medium follows from the large-$s$ behaviour of the Laplace-domain dispersion relation derived in Section 4, which is dominated by the leading terms of the quadratic in $m^2$. The result is")
EQ(r"c(r)^2=\frac{\hat k\,P}{\tau_0\left(\hat\rho\hat c\,P+\epsilon\,g^2\right)}", "wave")
P("For the reference medium $P=g=\\hat k=\\hat\\rho\\hat c=1$ and Eq. (@wave@) gives $c=1/\\sqrt{(1+\\epsilon)\\tau_0}=" + g(R["prof"]["hom"]["c"][0], 4) + "$, the value in [1]. Eq. (@wave@) does not contain $\\tau_1$, which governs damping but not the speed of the leading front. "
  "In the graded medium with $n=1$ the local speed rises from " + g(PR["n1"]["c"][0], 3) + " at the source to " + g(PR["n1"]["c"][49], 3) + " at $r=0.5$ and to " + g(PR["n1"]["c"][99], 4) + " at $r=L_g$ (Figure 2). Uniform porosity of 0.2 and 0.3 lowers the speed to " + g(PR["p0.2"]["c"][0], 4) + " and " + g(PR["p0.3"]["c"][0], 4) + ", because the conductivity and the stiffness fall faster than the heat capacity. "
  "In a medium that varies with $r$, a front that starts at $r_0$ is expected to arrive at $r$ after the travel time")
EQ(r"t_a(r)=\int_{r_0}^{r}\frac{dr'}{c(r')}", "travel")
P("This is a ray-theory estimate that ignores reflections caused by the property gradient; it is compared with the computed arrival times in Table 3. The elastic dilatational speed of the medium without the strain-rate effect is also of interest, because the Lord–Shulman-type and classical limits $\\tau_1\\to 0$ retain an elastic wavefront with that speed:")
EQ(r"c_e(r)^2=\frac{P}{\hat\rho}")
P("In the reference medium $c_e=1$, so that an elastic front reaches $r=0.3$ only at $t=0.3$, the end of the computed window. In the graded media the elastic speed in the contrast core is " + g(math.sqrt(q0n["P"] / q0n["rho"]), 3) + " times the reference value, so that the elastic front crosses the zone earlier, a fact that is visible in the results for $\\tau_1=0$ below.")

TAB(*T3())
FIG("Figure_2.png", "Local wave speed $c(r)$ from Eq. (@wave@) for (a) power-law grading, (b) porosity models and (c) the conductivity and P-modulus ratios. Computed from the property model.")
H1("4. Exact solution for uniform media")
P("The finite element results are verified against an exact solution that is derived here for a uniform medium whose properties are the reference data multiplied by the constant ratios $P$, $L$, $\\hat k$, $\\hat\\rho$, $\\hat\\rho\\hat c$ and $g$. For unit ratios it reduces to the solution of [1]. "
  "After a Laplace transform with parameter $s$ (overbars) the displacement is represented by a potential $\\varphi$, and $p=1+\\tau_1 s$ and $\\Psi=1+\\tau_0 s$ are the transform-domain forms of the two operators:")
EQ(r"\bar u=\partial_r\bar\varphi,\qquad \bar e=\nabla^2\bar\varphi,\qquad \nabla^2=\partial_r^2+\frac{1}{r}\partial_r")
P("Eq. (@e1@) integrated once in $r$ gives the temperature in terms of the potential,")
EQ(r"\bar\theta=\frac{1}{\delta_1 g}\left(P\nabla^2\bar\varphi-\frac{\hat\rho s^2}{p}\bar\varphi\right)")
P("and substitution in the transformed energy equation leads to a fourth-order equation that factorises as")
EQ(r"\left(\nabla^2-m_1^2\right)\left(\nabla^2-m_2^2\right)\bar\varphi=-\frac{\delta_1 g}{P\hat k}\,\bar Q,\qquad \bar Q=\frac{1}{s}\,\frac{\delta(r)}{2\pi r}")
P("The squared roots $m_{1,2}^2$ solve a quadratic whose coefficients follow from the preceding steps:")
EQ(r"m_{1,2}^2=\frac{B\pm\sqrt{B^2-4AC}}{2A},\qquad A=P\hat k", "roots")
EQ(r"B=\frac{\hat k\hat\rho s^2}{p}+\Psi s\left(\hat\rho\hat c\,P+\epsilon g^2\right),\qquad C=\frac{\Psi\,\hat\rho\hat\rho\hat c\,s^3}{p}")
P("The large-$s$ limit of this quadratic, in which $B\\sim\\Psi s\\left(\\hat\\rho\\hat c P+\\epsilon g^2\\right)$ dominates through $\\tau_0 s^2$ and $C$ is of lower order, gives the fast root $m_1^2\\sim s^2/c^2$ with $c$ from Eq. (@wave@); the slow root grows like $s$ and corresponds to the diffusive part. "
  "A Hankel transform of the source and a partial-fraction expansion, together with $\\nabla^2K_0(mr)=m^2K_0(mr)$ away from the origin, give the potential")
EQ(r"\bar\varphi=G\left[K_0(m_1 r)-K_0(m_2 r)\right],\qquad G=\frac{\delta_1 g}{2\pi s\,P\hat k\left(m_1^2-m_2^2\right)}")
P("where $K_0$ and $K_1$ are the modified Bessel functions of the second kind. The temperature, the displacement and the transformed stresses are")
EQ(r"\bar\theta=\frac{G}{\delta_1 g}\sum_{j=1}^{2}(-1)^{j+1}\left(Pm_j^2-\frac{\hat\rho s^2}{p}\right)K_0(m_j r),\qquad \bar u=-G\sum_{j=1}^{2}(-1)^{j+1}m_jK_1(m_j r)")
EQ(r"\bar\sigma_{rr}=\hat\rho s^2\bar\varphi-p\,(P-L)\frac{\bar u}{r},\qquad \bar\sigma_{\phi\phi}=\hat\rho s^2\bar\varphi+p\,(P-L)\left(\frac{\bar u}{r}-\nabla^2\bar\varphi\right)")
P("The stress formulas follow from the relation $\\bar\\sigma=p\\bar S$ and Eq. (@e1@). The time-domain solution is obtained with the Fourier-series inversion of Durbin with the epsilon-algorithm of Wynn applied to the last partial sums. With $T$ the period and $c_0$ the abscissa of convergence,")
EQ(r"f(t)\approx\frac{e^{c_0t}}{T}\left[\frac{1}{2}\bar f(c_0)+\sum_{k=1}^{N}\mathrm{Re}\left\{\bar f\!\left(c_0+\frac{ik\pi}{T}\right)e^{ik\pi t/T}\right\}\right]", "durbin")
P("with $T=2t$, $c_0t=6$ and $N=1200$. The program that implements this solution was first compared with the independent implementation of the previous homogeneous studies, and the two agree to all printed digits for the reference medium. "
  "A weakness of the exact solution must be recorded: the singular logarithmic behaviour of $K_0$ at $r\\to 0$ means that it cannot represent the regularised source, which is why the verification is limited to $r\\ge 0.1$ and the effect of the regularisation is measured separately in Section 8.2.")
