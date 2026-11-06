# -*- coding: utf-8 -*-
from cb import *

H1("3. Pulsed line source: exact Laplace-domain solution")
H2("3.1 Potential, temperature, displacement and stresses")
P("With $\\bar Q=Q_0\\bar F(s)\\delta(r)/(2\\pi r)$, where $\\bar F$ is the Laplace transform of the temporal profile, the right-hand side "
  "of the fourth-order equation is a two-dimensional delta function. The operator factorises, since $m_1^2$ and $m_2^2$ are the roots of "
  "$x^2-Bx+C=0$:")
EQ(r"\left(\nabla^2-m_1^2\right)\left(\nabla^2-m_2^2\right)\bar\varphi=-\frac{\delta_1 Q_0\bar F}{\Psi}\,\delta^{(2)}(x)")
EQ(r"m_{1,2}^2=\frac{1}{2}\left[B\pm\sqrt{B^2-4C}\right]")
P("The roots are labelled so that $|m_1|\\ge|m_2|$ and the branch with a positive real part is taken, which guarantees decay in $r$ for real $s>0$ "
  "and, by analytic continuation, for the complex values of $s$ used in the inversion. A two-dimensional Fourier transform with wave number "
  "$\\xi$ gives")
EQ(r"\tilde\varphi(\xi)=-\frac{\delta_1 Q_0\bar F}{\Psi\left(\xi^2+m_1^2\right)\left(\xi^2+m_2^2\right)}")
P("The partial fraction decomposition $1/[(\\xi^2+m_1^2)(\\xi^2+m_2^2)]=[1/(\\xi^2+m_2^2)-1/(\\xi^2+m_1^2)]/(m_1^2-m_2^2)$ and the "
  "transform pair $1/(\\xi^2+m^2)\\leftrightarrow K_0(mr)/2\\pi$ give")
EQ(r"\bar\varphi=G\left[K_0(m_1 r)-K_0(m_2 r)\right],\qquad G=\frac{\delta_1 Q_0\bar F(s)}{2\pi\,\Psi(s)\left(m_1^2-m_2^2\right)}")
P("The potential is finite at $r=0$ because the logarithmic singularities of the two Bessel functions have the same coefficient. Using "
  "$K_0'=-K_1$ and the identity $\\nabla^2K_0(mr)=m^2K_0(mr)$ for $r>0$ the other fields follow. The temperature and displacement are")
EQ(r"\bar\theta=\frac{G}{\delta_1}\left[\left(m_1^2-\frac{s^2}{p}\right)K_0(m_1 r)-\left(m_2^2-\frac{s^2}{p}\right)K_0(m_2 r)\right]")
EQ(r"\bar u=-G\left[m_1K_1(m_1 r)-m_2K_1(m_2 r)\right]")
P("The stress transforms are obtained from the constitutive relations and the potential equation. Writing "
  "$\\partial_r\\bar u+\\lambda_1\\bar u/r=\\nabla^2\\bar\\varphi-\\kappa\\bar u/r$ and using the relation between $\\bar\\theta$ and $\\bar\\varphi$:")
EQ(r"\bar\sigma_{rr}=s^2\bar\varphi-p\kappa\frac{\bar u}{r}")
EQ(r"\bar\sigma_{\phi\phi}=s^2\bar\varphi+p\kappa\left(\frac{\bar u}{r}-\nabla^2\bar\varphi\right)")
P("where $\\nabla^2\\bar\\varphi=G[m_1^2K_0(m_1r)-m_2^2K_0(m_2r)]$. These expressions have the same structure as those obtained "
  "in [1] for the Lord–Shulman limit, with the lag operators entering only through $m_1$, $m_2$ and the prefactor $G$. "
  "All fields decay exponentially in $r$ for $\\mathrm{Re}\\,s>0$, which is the far-field condition used in the validation.")
H2("3.2 Singular behaviour and global energy identity")
P("Near the source the temperature has the logarithmic singularity familiar from the Fourier line source. Expanding $K_0$ for small argument "
  "in the temperature transform, the logarithmic terms combine through the identity $m_1^2-m_2^2$ to give")
EQ(r"\bar\theta\simeq-\frac{Q_0\bar F(s)}{2\pi\Psi(s)}\ln r,\qquad r\to0")
P("The factor $\\Psi$ shows that the lag in the temperature gradient, not the lag in the flux, controls the strength of the singularity. The "
  "heat flux through a small circle satisfies, in the Laplace domain,")
EQ(r"\lim_{r\to0}2\pi r\,\bar q_r=\frac{Q_0\bar F(s)}{\Phi(s)}")
P("so that the source strength appears through the flux operator, which is the expected consequence of the effective-source convention. "
  "Integrating the energy equation over the plane, the Laplacian term vanishes because the flux decays at infinity, and the integral of "
  "the dilatation vanishes because the displacement decays. This gives a global identity that is independent of the "
  "thermoelastic coupling and of $\\Psi$,")
EQ(r"\int_0^\infty{\theta\,2\pi r\,dr}=Q_0\,\mathcal{L}^{-1}\left[\frac{\bar F(s)}{s\,\Phi(s)}\right]")
P("This identity provides a stringent test of the numerical solution because it involves all the radii and depends only on the flux "
  "operator $\\Phi$. For the step source with $\\Phi=1$ it gives $Q_0t$, the total heat injected.")
H2("3.3 Temporal profiles")
P("Five profiles are used; their definitions are collected in Table 5 and Figure 3. A profile is normalised to a maximum value of one "
  "(or to one for the step). The step (Heaviside) profile corresponds to the problem of [1]. In the Laplace domain:")
EQ(r"f=H(t):\qquad \bar F(s)=\frac{1}{s}")
EQ(r"f=H(t)-H(t-t_p):\qquad \bar F(s)=\frac{1-e^{-st_p}}{s}")
EQ(r"f=e^{-t/t_d}:\qquad \bar F(s)=\frac{1}{s+1/t_d}")
EQ(r"f=\frac{t}{t_m}e^{1-t/t_m}:\qquad \bar F(s)=\frac{e\,t_m}{\left(1+t_ms\right)^2}")
EQ(r"f=\sin^2\left(\frac{\pi t}{P}\right):\qquad \bar F(s)=\frac{\omega_0^2}{2s\left(s^2+\omega_0^2\right)},\quad\omega_0=\frac{2\pi}{P}")
P("The gamma-type profile rises from zero with a finite rate, peaks at $t=t_m$ with value one and decays slowly; it is a common idealisation "
  "of a laser pulse. The squared sine is a periodic train of non-negative pulses with period $P$ and a mean value of one half; it keeps the "
  "source non-negative, which a plain sine would not. The rectangular pulse is evaluated by superposition of two shifted step solutions, which avoids "
  "the Gibbs oscillations that a direct inversion of the discontinuous profile would produce:")
EQ(r"\mathcal{R}_{\mathrm{rect}}(r,t)=\mathcal{R}_{\mathrm{step}}(r,t)-H(t-t_p)\,\mathcal{R}_{\mathrm{step}}(r,t-t_p)")
P("where $\\mathcal{R}$ stands for any field. The transforms of all five profiles were inverted separately with the same numerical "
  "method used for the field problem; the maximum error against the exact time functions was %s for the step, %s for the exponential, %s for the gamma "
  "profile and %s for the squared sine, and %s for the rectangle away from the discontinuity." % (
      g(X["profile_inversion"]["step"], 2), g(X["profile_inversion"]["exp_0.05"], 2), g(X["profile_inversion"]["gamma_0.03"], 2),
      g(X["profile_inversion"]["sin2_0.08"], 2), g(X["profile_inversion"]["rect_0.04"], 2)))

H1("4. Moving line source")
H2("4.1 Formulation and its limitations")
P("The moving-source problem is formulated for a line parallel to the $z$ axis that passes through the point $(Vt,0)$ of the $xy$ plane at time $t$, "
  "so that it translates at the constant speed $V$ in the $x$ direction in plane strain. The source is")
EQ(r"Q(x,y,t)=Q_0\,\delta(x-Vt)\,\delta(y)\,f(t)")
P("This is the formulation that was implemented; it is not the radially moving ring source that would be a fallback if the Cartesian problem "
  "were intractable. The medium is unbounded, the source starts at the origin at $t=0$, and no boundary or edge is present, so the problem has "
  "no reflected field. The source is a mathematical line, so that the temperature is logarithmically singular on its path. Since the only "
  "source of disturbance is a thermal one, the solenoidal part of the displacement satisfies a homogeneous wave equation with zero data and "
  "vanishes, which gives an irrotational displacement field $u_i=\\partial_i\\varphi$ that satisfies the same potential equation as in Section 2 with $\\nabla^2$ "
  "now the two-dimensional Cartesian Laplacian.")
H2("4.2 Transform solution")
P("Taking the Laplace transform in time, the source becomes a distribution along the positive $x$ axis,")
EQ(r"\bar Q(x,y,s)=\frac{Q_0}{V}\,f\!\left(\frac{x}{V}\right)e^{-sx/V}\,H(x)\,\delta(y)")
P("The spatial Fourier transform pair is defined by")
EQ(r"\tilde g(\xi,\eta)=\int_{-\infty}^{\infty}\int_{-\infty}^{\infty}{g(x,y)\,e^{-i(\xi x+\eta y)}\,dx\,dy}")
P("For a source that moves at speed $V$ the transform of $\\bar Q$ is the transform of the profile with a Doppler-shifted Laplace variable, "
  "which can be verified directly from the definition of the Laplace transform of $\\delta(x-Vt)f(t)$:")
EQ(r"\tilde Q(\xi,\eta,s)=Q_0\,\bar F\!\left(s+i\xi V\right)")
P("Because $\\mathrm{Re}\\,s>0$ the shifted argument remains in the half plane of analyticity of $\\bar F$ for every real $\\xi$. The transformed potential is")
EQ(r"\tilde\varphi=-\frac{\delta_1Q_0\bar F(s+i\xi V)}{\Psi(s)\left(k^2+m_1^2\right)\left(k^2+m_2^2\right)},\qquad k^2=\xi^2+\eta^2")
P("The roots $m_1$ and $m_2$ depend only on $s$, not on $\\xi$, because the medium is homogeneous. The inverse transform in $\\eta$ is "
  "performed analytically using the partial fractions of Section 3.1 and the standard result that the inverse transform of $1/(\\eta^2+a^2)$ with respect to $\\eta$ is $e^{-a|y|}/(2a)$:")
EQ(r"a_j=\sqrt{\xi^2+m_j^2},\qquad g_j(\xi,y)=\frac{e^{-a_jy}}{2a_j},\qquad j=1,2")
P("with the branch $\\mathrm{Re}\\,a_j>0$. By symmetry the field is even in $y$, and the formulas below are for $y>0$. The potential and the "
  "transformed fields are single Fourier integrals,")
EQ(r"\bar\varphi(x,y,s)=\frac{1}{2\pi}\int_{-\infty}^{\infty}{e^{i\xi x}\,\Lambda(\xi)\left[g_1-g_2\right]}d\xi")
EQ(r"\Lambda(\xi)=\frac{\delta_1Q_0\bar F(s+i\xi V)}{\Psi(s)\left(m_1^2-m_2^2\right)}")
P("The temperature, the two displacement components and the three in-plane stresses are given by the same integral with the integrand "
  "modified as follows (for $y>0$ and $\\kappa p$ as in Section 3). The temperature is")
EQ(r"\bar\theta=\frac{1}{2\pi\delta_1}\int{e^{i\xi x}\Lambda\left[\left(m_1^2-\frac{s^2}{p}\right)g_1-\left(m_2^2-\frac{s^2}{p}\right)g_2\right]}d\xi")
EQ(r"\bar u_x=\frac{1}{2\pi}\int{i\xi\,e^{i\xi x}\Lambda\left[g_1-g_2\right]}d\xi")
EQ(r"\bar u_y=\frac{1}{2\pi}\int{e^{i\xi x}\Lambda\left[-a_1g_1+a_2g_2\right]}d\xi")
P("For the stresses the Fourier-space expressions $\\tilde\\sigma_{xx}=\\tilde\\varphi(s^2+p\\kappa\\eta^2)$, $\\tilde\\sigma_{yy}=\\tilde\\varphi(s^2+p\\kappa\\xi^2)$ and "
  "$\\tilde\\sigma_{xy}=-p\\kappa\\xi\\eta\\tilde\\varphi$ follow from the relation between $\\theta$ and $\\varphi$, and the $\\eta$ factors are "
  "removed by differentiation in $y$, which is legitimate for $y\\ne0$. The results are")
EQ(r"\bar\sigma_{xx}=\frac{1}{2\pi}\int{e^{i\xi x}\Lambda\left[\left(s^2-p\kappa a_1^2\right)g_1-\left(s^2-p\kappa a_2^2\right)g_2\right]}d\xi")
EQ(r"\bar\sigma_{yy}=\frac{1}{2\pi}\int{e^{i\xi x}\Lambda\left(s^2+p\kappa\xi^2\right)\left[g_1-g_2\right]}d\xi")
EQ(r"\bar\sigma_{xy}=\frac{p\kappa}{2\pi}\int{i\xi\,e^{i\xi x}\Lambda\left[-a_1g_1+a_2g_2\right]}d\xi")
H2("4.3 Evaluation, consistency and the Mach condition")
P("The integrals are evaluated by the trapezoidal rule with step $h$ and truncation $|\\xi|\\le\\xi_{\\max}$,")
EQ(r"\int_{-\infty}^{\infty}{F(\xi)\,d\xi}\approx h\sum_{j=-J}^{J}{F(jh)},\qquad J=\xi_{\max}/h")
P("For an integrand that is analytic in a strip of half-width $d$ about the real axis the trapezoidal error decays like $e^{-2\\pi d/h}$ plus the "
  "truncation error, which is exponentially small for $y>0$ because $g_j\\sim e^{-|\\xi|y}$. The nearest singularities are the branch points of $a_j$ at "
  "$\\xi=\\pm im_j$ and the pole of $\\bar F(s+i\\xi V)$ at $\\xi=is/V$. In the computations $y=0.2$, $h=0.25$ and $\\xi_{\\max}=100$ are used, so that the "
  "truncation factor is about $e^{-20}$. A necessary check is that the code reproduces the axisymmetric solution of Section 3 when $V=0$. In that "
  "case the integrand is independent of $V$ and the known identity")
EQ(r"\frac{1}{2\pi}\int_{-\infty}^{\infty}{e^{i\xi x}\,\frac{e^{-y\sqrt{\xi^2+m^2}}}{2\sqrt{\xi^2+m^2}}\,d\xi}=\frac{1}{2\pi}K_0\!\left(m\sqrt{x^2+y^2}\right)")
P("shows that the two solutions coincide. The Cartesian stress components are related to the polar ones, with $\\varphi$ the polar angle, by")
EQ(r"\sigma_{xx}=\sigma_{rr}\cos^2\varphi+\sigma_{\phi\phi}\sin^2\varphi")
P("which is used in the $V=0$ comparison. The wave structure of Section 5 implies a characteristic thermal wave speed $c_w$. When $V>c_w$ the "
  "source outruns its own disturbance and the wavefronts, being circles centred at earlier source positions, have a conical envelope with half-angle")
EQ(r"\sin\beta=\frac{c_w}{V}")
P("The numerical results of Section 7 show the corresponding rise of the stress peak. For $V<c_w$ the front is a distorted circle whose "
  "forward part is compressed in the direction of motion, and the temperature maximum is displaced toward the moving source. The moving-source "
  "solution describes the transient stage and not a quasi-steady state: the source is switched on at $t=0$ and the fields at $t=0.1$ still contain the "
  "initial front.")

FIG("Figure_2.png", "Solution procedure: transform, potential, closed-form transform-domain solution, asymptotic classification, numerical inversion and validation. Flow chart, not computed.")
FIG("Figure_3.png", "Temporal source profiles (a) and the modulus of their Laplace transforms on the imaginary axis (b). Profiles are those of Table 5; curves are computed from the defining functions; the sinusoidal spectrum has a pole at $\\omega_0=2\\pi/P$ and is clipped.")

P("The Doppler-shifted argument of $\\bar F$ has a direct interpretation. A Fourier component of wave number $\\xi$ along the direction of motion sees the source, in the frame of the medium, as "
  "a time dependence $e^{-i\\xi Vt}f(t)$, so that its effective complex frequency is $s+i\\xi V$. For a step profile the source of that component is $1/(s+i\\xi V)$, which has a pole at "
  "$s=-i\\xi V$ and therefore describes a harmonic forcing. The response is obtained by integrating all components with the weight $e^{i\\xi x}$, and the thermal wave appears as a "
  "singularity in the transform variable $s$ that is shifted by $\\xi V$ for each component. This is the origin of the Mach-type structure when $V$ exceeds the wave speed: components "
  "with $|\\xi|V$ larger than the wave frequency are forced faster than the medium can propagate them, and their contributions add coherently along the cone.")
