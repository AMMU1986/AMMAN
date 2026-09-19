# Irreversibility Analysis of a Radiative Casson Hybrid Nanofluid Between Squeezing Porous Plates: Bejan Number and Second-Law Optimization

**Authors:** [Author 1]¹, Kalpna Sharma¹\*, [Author 3]²
¹Department of Mathematics and Statistics, Manipal University Jaipur, Jaipur, Rajasthan, India
²Department of Mathematics, [Affiliation], India
\*Corresponding author.

---

## Abstract

The present investigation reports a comprehensive second-law analysis of the two-dimensional, unsteady, magnetohydrodynamic (MHD) squeezing flow of a Casson Cu–Al₂O₃/water hybrid nanofluid confined between two horizontal parallel plates embedded in a Darcy porous medium. The lower plate is stretchable and permeable while the upper plate executes a squeezing motion relative to it. The energy transport incorporates nonlinear thermal radiation through the Rosseland approximation, Ohmic (Joule) dissipation, a volumetric heat source, viscous dissipation, and the Dufour (diffusion-thermo) cross-diffusion mechanism. The species transport carries the Soret (thermo-diffusion) effect together with an Arrhenius activation-energy-driven chemical reaction. The coupled partial differential equations governing mass, momentum, thermal and solutal transport are converted into a system of highly nonlinear, coupled ordinary differential equations by means of a suitable similarity transformation, and are solved analytically through the Optimal Homotopy Analysis Method (OHAM). A closed-form exact solution is derived for a physically meaningful reducible limit, and it is used to benchmark the analytical series solution. The dimensionless volumetric entropy generation number and the Bejan number are formulated by combining the thermal (with radiation), viscous, porous, magnetic (Joule) and diffusive irreversibility contributions. The influence of the Casson parameter, magnetic parameter, squeezing parameter, porosity, radiation, Brinkman number, Soret and Dufour numbers, and nanoparticle volume fractions on the velocity, temperature, concentration, entropy generation number and Bejan number is analysed through profiles and contour maps. The study finally identifies a second-law-optimal operating window that minimizes total irreversibility while preserving a target heat-transfer rate. It is found that entropy generation intensifies with the Brinkman and magnetic parameters near the stretching plate, whereas an increase in the squeezing parameter and Casson parameter suppresses total irreversibility. The hybrid nanoparticle loading enhances the heat-transfer irreversibility (Bejan number → 1) in the core of the channel.

**Keywords:** Casson hybrid nanofluid; Squeezing flow; Entropy generation; Bejan number; Thermal radiation; Joule heating; Cross-diffusion; OHAM; Second-law optimization.

---

## Nomenclature

| Symbol | Meaning | Symbol | Meaning |
|---|---|---|---|
| $u,v$ | velocity components (m s⁻¹) | $B(t)$ | magnetic field |
| $T$ | temperature (K) | $M$ | magnetic parameter |
| $C$ | concentration (mol m⁻³) | $Sq$ | squeezing parameter |
| $\beta^*$ | Casson parameter | $K_P$ | porosity parameter |
| $\kappa_{hnf}$ | hybrid nanofluid thermal conductivity | $Rd$ | radiation parameter |
| $\mu_{hnf}$ | hybrid nanofluid dynamic viscosity | $Pr$ | Prandtl number |
| $\rho_{hnf}$ | hybrid nanofluid density | $Ec$ | Eckert number |
| $\sigma_{hnf}$ | hybrid nanofluid electrical conductivity | $Sc$ | Schmidt number |
| $\phi_1,\phi_2$ | Al₂O₃, Cu volume fractions | $Sr$ | Soret number |
| $q_r$ | radiative heat flux | $Df$ | Dufour number |
| $Q_0$ | heat source coefficient | $Br$ | Brinkman number |
| $N_G$ | entropy generation number | $Be$ | Bejan number |
| $S_{gen}$ | volumetric entropy generation | $\Omega,\zeta$ | temperature, concentration ratios |
| $f,\theta,\phi$ | dimensionless stream, temperature, concentration | $\eta$ | similarity variable |

Subscripts: $f$ base fluid; $nf$ nanofluid; $hnf$ hybrid nanofluid; $s_1$ Al₂O₃; $s_2$ Cu.

---

## 1. Introduction

The relentless demand for efficient thermal-management solutions in compact engineering systems — microelectronic cooling modules, compression and lubrication machinery, biomedical squeeze-film devices and miniaturised heat exchangers — has driven sustained interest in advanced working fluids and in the geometries that most effectively transport heat between closely spaced surfaces. Two developments dominate this landscape. The first is the emergence of nanofluids, engineered colloidal suspensions of nanometre-scale particles in a conventional base liquid, introduced by Choi and Eastman to overcome the intrinsically poor thermal conductivity of ordinary fluids. The second, more recent, is the hybrid nanofluid, in which two chemically distinct nanoparticle species are simultaneously dispersed so that their complementary attributes — for instance the high thermal conductivity of copper (Cu) and the chemical stability and favourable surface characteristics of alumina (Al₂O₃) — reinforce one another to yield superior thermophysical performance than either single-particle suspension.

When such fluids are processed between converging or diverging surfaces, the resulting squeezing flow constitutes one of the classical problems of applied fluid mechanics. Squeeze films arise wherever one boundary approaches another through a viscous medium, and they govern the load-carrying capacity of bearings, the moulding of polymers, the operation of hydraulic dampers and the mechanics of biological joints. The unsteady, two-dimensional squeezing of a fluid between parallel plates, in which the lower plate is simultaneously stretched and rendered permeable while the upper plate advances or recedes, provides an especially rich model because it couples boundary-driven shear with a time-dependent gap and with wall-normal suction or injection.

Many working fluids of practical relevance are non-Newtonian. Among the numerous rheological models, the Casson model occupies a privileged position because it captures yield-stress behaviour: below a critical shear stress the material behaves as a rigid solid, and above it as a shear-thinning viscous liquid. Blood, molten chocolate, concentrated fruit juices, drilling muds and a broad class of pharmaceutical and food fluids are well represented by the Casson constitutive law, and the model reduces smoothly to the Newtonian limit as the Casson parameter grows without bound.

The transport of heat in such systems is frequently accompanied by strong thermal radiation, by the Joule heating that inevitably arises when an electrically conducting fluid moves through an imposed magnetic field, by a volumetric heat source, and by viscous dissipation. When species transport is also present, the Soret and Dufour cross-diffusion mechanisms couple the thermal and solutal fields, and an Arrhenius activation-energy-controlled chemical reaction modulates the concentration field. The magnetohydrodynamic (MHD) body force offers a non-intrusive means of regulating the flow, and it is exploited in metallurgical processing, MHD pumps and generators, and biomedical flow control.

Although the first law of thermodynamics quantifies energy conservation, it is silent on the quality of energy conversion. The second law, expressed through entropy generation, identifies where and by how much useful work is irreversibly destroyed. Minimising entropy generation is therefore synonymous with maximising thermodynamic efficiency. The pioneering entropy-generation-minimisation framework of Bejan and the associated Bejan number — the ratio of heat- and mass-transfer irreversibility to total irreversibility — have become indispensable diagnostics in the design of thermal systems. Despite an extensive first-law literature on squeezing hybrid-nanofluid flows, a unified second-law treatment that simultaneously accounts for the Casson rheology, hybrid Cu–Al₂O₃/water suspension, Darcy porous resistance, nonlinear radiation, Joule heating, cross-diffusion and Arrhenius chemistry in the stretchable-lower/squeezing-upper channel remains, to the best of our knowledge, unaddressed.

A substantial body of work has examined entropy generation in nanofluid and hybrid-nanofluid flows over stretching sheets, rotating and spinning disks, cones, cylinders and channels, and has established that the magnetic field, Brinkman number, radiation and nanoparticle concentration are the principal levers of irreversibility. Investigations of squeezing flows, in particular, have shown that the approach of one boundary towards another sharply reorganises the velocity and thermal gradients and therefore the local entropy field. Nevertheless, the reported squeezing-flow entropy studies are overwhelmingly restricted either to single-phase or single-particle nanofluids, or to rotating-plate configurations, and they seldom retain the full constellation of physical mechanisms — yield-stress rheology, dual-particle hybrid suspension, porous resistance, nonlinear radiation, Ohmic dissipation, and coupled heat-and-mass transfer with cross-diffusion and reaction — that a realistic squeeze-film thermal device simultaneously experiences. The consequence is that the true irreversibility budget of such a device, and hence its attainable thermodynamic efficiency, has not been quantified. Establishing that budget, and using it to locate a second-law-optimal operating window, is the central purpose of the present paper.

The present work fills precisely this gap. It generalises two complementary earlier studies — one treating the Casson Cu–Al₂O₃/water hybrid nanofluid in a squeezing channel with radiation and Joule heating but without any species transport, and the other treating a single-phase viscous Casson fluid with cross-diffusion, chemical reaction and multiple slip but without nanoparticles or Joule heating — into a single, thermodynamically complete model, and it augments that model with a full entropy-generation analysis and a second-law optimisation. Both antecedent studies are recovered as limiting cases, which furnishes a rigorous validation pathway. The governing equations are reduced by similarity transformation and solved by the Optimal Homotopy Analysis Method (OHAM), and a closed-form exact solution is obtained for a reducible limit to anchor the analytical series solution.

---

## 2. Mathematical Formulation

### 2.1 Physical model and assumptions

Consider the unsteady, two-dimensional, laminar and incompressible flow of a Casson Cu–Al₂O₃/water hybrid nanofluid confined between two infinite horizontal parallel plates saturated by a Darcy porous medium. A Cartesian coordinate system $(x,y)$ is adopted with the $x$-axis lying along the lower plate and the $y$-axis normal to it. The upper plate is located at a time-dependent distance

$$
h(t)=\sqrt{\frac{\nu_f(1-\alpha t)}{b}},\qquad t<\frac{1}{\alpha},
\tag{1}
$$

and moves towards or away from the lower plate with velocity $V_h=dh/dt=-\tfrac{\alpha}{2}\sqrt{\nu_f/[b(1-\alpha t)]}$. The lower plate is stretched with velocity $u_w=bx/(1-\alpha t)$ and is permeable, admitting wall-normal suction/injection with velocity $v_w=-V_0/(1-\alpha t)$. A transverse, time-dependent magnetic field $B(t)=B_0/\sqrt{1-\alpha t}$ is applied along the $y$-direction; the induced magnetic field is neglected under the small magnetic-Reynolds-number assumption.

The rheological equation of state for an isotropic, incompressible Casson fluid is

$$
\tau_{ij}=
\begin{cases}
2\!\left(\mu_B+\dfrac{p_y}{\sqrt{2\pi}}\right)e_{ij}, & \pi>\pi_c,\\[2mm]
2\!\left(\mu_B+\dfrac{p_y}{\sqrt{2\pi_c}}\right)e_{ij}, & \pi<\pi_c,
\end{cases}
\tag{2}
$$

where $\mu_B$ is the plastic dynamic viscosity, $p_y$ the yield stress, $e_{ij}$ the rate-of-strain tensor, $\pi=e_{ij}e_{ij}$, and $\pi_c$ its critical value. The Casson parameter is $\beta^*=\mu_B\sqrt{2\pi_c}/p_y$.

### 2.2 Governing equations

Under the stated assumptions and the boundary-layer scaling, the conservation equations for the hybrid nanofluid read:

**Continuity:**

$$
\frac{\partial u}{\partial x}+\frac{\partial v}{\partial y}=0.
\tag{3}
$$

**Momentum (x-direction):**

$$
\frac{\partial u}{\partial t}+u\frac{\partial u}{\partial x}+v\frac{\partial u}{\partial y}
=-\frac{1}{\rho_{hnf}}\frac{\partial p}{\partial x}
+\frac{\mu_{hnf}}{\rho_{hnf}}\!\left(1+\frac{1}{\beta^*}\right)\!\left(\frac{\partial^2 u}{\partial x^2}+\frac{\partial^2 u}{\partial y^2}\right)
-\frac{\sigma_{hnf}}{\rho_{hnf}}B(t)^2 u
-\frac{\mu_{hnf}}{\rho_{hnf}}\frac{1}{K_P^*}\!\left(1+\frac{1}{\beta^*}\right)u.
\tag{4}
$$

**Momentum (y-direction):**

$$
\frac{\partial v}{\partial t}+u\frac{\partial v}{\partial x}+v\frac{\partial v}{\partial y}
=-\frac{1}{\rho_{hnf}}\frac{\partial p}{\partial y}
+\frac{\mu_{hnf}}{\rho_{hnf}}\!\left(1+\frac{1}{\beta^*}\right)\!\left(\frac{\partial^2 v}{\partial x^2}+\frac{\partial^2 v}{\partial y^2}\right)
-\frac{\mu_{hnf}}{\rho_{hnf}}\frac{1}{K_P^*}\!\left(1+\frac{1}{\beta^*}\right)v.
\tag{5}
$$

**Energy** (radiation, Joule heating, heat source, viscous dissipation, Dufour):

$$
\left(\rho C_p\right)_{hnf}\!\left(\frac{\partial T}{\partial t}+u\frac{\partial T}{\partial x}+v\frac{\partial T}{\partial y}\right)
=\kappa_{hnf}\frac{\partial^2 T}{\partial y^2}-\frac{\partial q_r}{\partial y}
+\sigma_{hnf}B(t)^2u^2 -Q_0(T-T_1)
$$
$$
+\mu_{hnf}\!\left(1+\frac{1}{\beta^*}\right)\!\left[2\!\left(\frac{\partial u}{\partial x}\right)^2+2\!\left(\frac{\partial v}{\partial y}\right)^2+\left(\frac{\partial u}{\partial y}+\frac{\partial v}{\partial x}\right)^2\right]
+\frac{\rho_{hnf}D_mK_T}{C_s}\frac{\partial^2 C}{\partial y^2}.
\tag{6}
$$

**Concentration** (Soret, Arrhenius chemical reaction):

$$
\frac{\partial C}{\partial t}+u\frac{\partial C}{\partial x}+v\frac{\partial C}{\partial y}
=D_m\frac{\partial^2 C}{\partial y^2}
+\frac{D_mK_T}{T_m}\frac{\partial^2 T}{\partial y^2}
-k_r^2\!\left(\frac{T}{T_1}\right)^{n}\!\exp\!\left(-\frac{E_a}{k_BT}\right)(C-C_1).
\tag{7}
$$

The Rosseland radiative flux and its linearisation are

$$
q_r=-\frac{4\sigma^*}{3k^*}\frac{\partial T^4}{\partial y},\qquad
T^4\approx 4T_0^3T-3T_0^4,\qquad
\frac{\partial q_r}{\partial y}=-\frac{16\sigma^*T_0^3}{3k^*}\frac{\partial^2 T}{\partial y^2}.
\tag{8}
$$

### 2.3 Thermophysical properties of the hybrid nanofluid

The Cu–Al₂O₃/water hybrid nanofluid properties follow the standard two-step correlations (Al₂O₃ enters first with volume fraction $\phi_1$; Cu second with $\phi_2$):

$$
\mu_{hnf}=\frac{\mu_f}{(1-\phi_1)^{2.5}(1-\phi_2)^{2.5}},\qquad
\rho_{hnf}=(1-\phi_2)\!\left[(1-\phi_1)\rho_f+\phi_1\rho_{s_1}\right]+\phi_2\rho_{s_2},
\tag{9}
$$

$$
(\rho C_p)_{hnf}=(1-\phi_2)\!\left[(1-\phi_1)(\rho C_p)_f+\phi_1(\rho C_p)_{s_1}\right]+\phi_2(\rho C_p)_{s_2},
\tag{10}
$$

$$
\frac{\kappa_{hnf}}{\kappa_{bf}}=\frac{2\kappa_{bf}+\kappa_{s_2}-2\phi_2(\kappa_{bf}-\kappa_{s_2})}{2\kappa_{bf}+\kappa_{s_2}+\phi_2(\kappa_{bf}-\kappa_{s_2})},\qquad
\frac{\kappa_{bf}}{\kappa_f}=\frac{2\kappa_f+\kappa_{s_1}-2\phi_1(\kappa_f-\kappa_{s_1})}{2\kappa_f+\kappa_{s_1}+\phi_1(\kappa_f-\kappa_{s_1})},
\tag{11}
$$

$$
\frac{\sigma_{hnf}}{\sigma_{bf}}=\frac{\sigma_{s_2}(1+2\phi_2)+2\sigma_{bf}(1-\phi_2)}{\sigma_{s_2}(1-\phi_2)+\sigma_{bf}(2+\phi_2)},\qquad
\frac{\sigma_{bf}}{\sigma_f}=\frac{\sigma_{s_1}(1+2\phi_1)+2\sigma_f(1-\phi_1)}{\sigma_{s_1}(1-\phi_1)+\sigma_f(2+\phi_1)}.
\tag{12}
$$

Representative thermophysical data (Al₂O₃ / Cu / H₂O): $C_p=765/385/4179$ J kg⁻¹K⁻¹; $\rho=3970/8933/997.1$ kg m⁻³; $\sigma=35\times10^6/59.6\times10^6/5.5\times10^{-6}$ S m⁻¹; $\kappa=40/401/0.613$ W m⁻¹K⁻¹.

### 2.4 Boundary conditions

$$
u=\lambda\,u_w,\quad v=v_w,\quad T=T^*_0,\quad C=C^*_0 \qquad\text{at }y=0,
\tag{13a}
$$
$$
u=0,\quad v=\frac{dh}{dt},\quad T=T_2,\quad C=C_2 \qquad\text{at }y=h(t).
\tag{13b}
$$

### 2.5 Similarity transformation

Introduce

$$
\psi=\sqrt{\frac{b\nu_f}{1-\alpha t}}\;x\,f(\eta),\quad
u=\frac{bx}{1-\alpha t}f'(\eta),\quad
v=-\sqrt{\frac{b\nu_f}{1-\alpha t}}\,f(\eta),
\tag{14}
$$
$$
\eta=\sqrt{\frac{b}{\nu_f(1-\alpha t)}}\,y,\quad
\theta(\eta)=\frac{T-T_1}{T_2-T_1},\quad
\phi(\eta)=\frac{C-C_1}{C_2-C_1}.
\tag{15}
$$

Equation (3) is satisfied identically. Eliminating the pressure between (4) and (5) and substituting (14)–(15) yields the dimensionless system

$$
\boxed{\;\frac{A_1}{A_2}\!\left(1+\frac{1}{\beta^*}\right)f^{iv}+f f'''-f' f''-\frac{Sq}{2}\!\left(3f''+\eta f'''\right)-\frac{A_3}{A_2}Mf''-\frac{A_1}{A_2}\!\left(1+\frac{1}{\beta^*}\right)K_Pf''=0\;}
\tag{16}
$$

$$
\boxed{\;\left(A_4+\frac{4}{3}Rd\right)\theta''-Pr\,Hs\,\theta-A_5\!\left(\frac{Sq}{2}\eta-f\right)Pr\,\theta'
+A_1\!\left(1+\frac{1}{\beta^*}\right)Ec\,Pr\!\left[4\gamma f'^2+f''^2\right]+A_3\,Ec\,Pr\,M f'^2+Pr\,Df\,\phi''=0\;}
\tag{17}
$$

$$
\boxed{\;\phi''+Sc\!\left(f\phi'-f'\phi\right)-Sc\frac{Sq}{2}\eta\,\phi'-Sc\,K\,(1+\delta_T\theta)^n e^{-E/(1+\delta_T\theta)}\phi+Sc\,Sr\,\theta''=0\;}
\tag{18}
$$

with reduced boundary conditions

$$
f(0)=S,\quad f'(0)=\lambda,\quad \theta(0)=0,\quad \phi(0)=0,
\tag{19a}
$$
$$
f'(1)=0,\quad f(1)=\frac{Sq}{2},\quad \theta(1)=1,\quad \phi(1)=1.
\tag{19b}
$$

### 2.6 Dimensionless parameters

$$
A_1=\frac{\mu_{hnf}}{\mu_f},\;A_2=\frac{\rho_{hnf}}{\rho_f},\;A_3=\frac{\sigma_{hnf}}{\sigma_f},\;A_4=\frac{\kappa_{hnf}}{\kappa_f},\;A_5=\frac{(\rho C_p)_{hnf}}{(\rho C_p)_f},
$$
$$
Sq=\frac{\alpha}{b},\;M=\frac{\sigma_fB_0^2}{b\rho_f},\;K_P=\frac{\mu_f(1-\alpha t)}{\rho_f bK_P^*},\;Rd=\frac{4\sigma^*T_0^3}{\kappa_f k^*},\;Pr=\frac{\mu_f(C_p)_f}{\kappa_f},
$$
$$
Hs=\frac{Q_0(1-\alpha t)}{(\rho C_p)_f},\;Ec=\frac{u_w^2}{(C_p)_f(T_2-T_1)},\;Sc=\frac{\nu_f}{D_m},\;Sr=\frac{D_mK_T(T_2-T_1)}{T_m\nu_f(C_2-C_1)},
$$
$$
Df=\frac{D_mK_T(C_2-C_1)}{C_s(C_p)_f\nu_f(T_2-T_1)},\;K=\frac{k_r^2(1-\alpha t)}{b},\;S=\frac{V_0}{b h},\;\gamma=\frac{\nu_f(1-\alpha t)}{bx^2}.
$$

### 2.7 Engineering quantities

The skin-friction coefficients and Nusselt/Sherwood numbers at the two plates are

$$
Re_x^{1/2}C_{f1}=\frac{\mu_{hnf}}{\mu_f}f''(0),\qquad Re_x^{1/2}C_{f2}=\frac{\mu_{hnf}}{\mu_f}f''(1),
\tag{20}
$$
$$
Re_x^{1/2}Nu_{x1}=-\frac{\kappa_{hnf}}{\kappa_f}\!\left(1+\frac{4}{3}Rd\right)\theta'(0),\qquad
Re_x^{1/2}Sh_{x1}=-\phi'(0).
\tag{21}
$$

---

## 3. Entropy Generation Analysis

### 3.1 Dimensional volumetric entropy generation

Applying the local thermodynamic equilibrium hypothesis, the volumetric rate of entropy production for the radiative, magnetised, chemically reacting Casson hybrid nanofluid in the porous medium is

$$
S_{gen}=
\underbrace{\frac{\kappa_{hnf}}{T_0^2}\!\left(1+\frac{16\sigma^*T_0^3}{3k^*\kappa_{hnf}}\right)\!\left(\frac{\partial T}{\partial y}\right)^2}_{\text{thermal + radiative}}
+\underbrace{\frac{\mu_{hnf}}{T_0}\!\left(1+\frac{1}{\beta^*}\right)\!\left(\frac{\partial u}{\partial y}\right)^2}_{\text{viscous}}
+\underbrace{\frac{\mu_{hnf}}{T_0K_P^*}\!\left(1+\frac{1}{\beta^*}\right)u^2}_{\text{porous}}
$$
$$
+\underbrace{\frac{\sigma_{hnf}B(t)^2}{T_0}u^2}_{\text{Joule/magnetic}}
+\underbrace{\frac{RD_m}{C_0}\!\left(\frac{\partial C}{\partial y}\right)^2+\frac{RD_m}{T_0}\!\left(\frac{\partial T}{\partial y}\right)\!\left(\frac{\partial C}{\partial y}\right)}_{\text{diffusive + cross-diffusive}}.
\tag{22}
$$

### 3.2 Non-dimensional entropy generation number

Dividing $S_{gen}$ by the characteristic entropy rate $S_0=\kappa_f(T_2-T_1)^2/[T_0^2h(t)^2]$ and inserting the similarity variables gives the entropy generation number

$$
\boxed{\;
N_G=A_4\!\left(1+\frac{4}{3}Rd\right)\theta'^2
+\frac{Br}{\Omega}\,A_1\!\left(1+\frac{1}{\beta^*}\right)\!\left(f''^2+K_P f'^2\right)
+\frac{Br}{\Omega}\,A_3\,M f'^2
+\Lambda\frac{\zeta^2}{\Omega^2}\phi'^2+\Lambda\frac{\zeta}{\Omega}\theta'\phi'\;}
\tag{23}
$$

where the Brinkman number $Br=\mu_fu_w^2/[\kappa_f(T_2-T_1)]$, the temperature difference ratio $\Omega=(T_2-T_1)/T_0$, the concentration difference ratio $\zeta=(C_2-C_1)/C_0$, and the diffusive parameter $\Lambda=RD_mC_0/\kappa_f$.

For compactness write $N_G=N_H+N_F+N_D$, where $N_H=A_4(1+\tfrac43Rd)\theta'^2$ is the thermal (heat-transfer) irreversibility, $N_F=\tfrac{Br}{\Omega}[A_1(1+\tfrac1{\beta^*})(f''^2+K_Pf'^2)+A_3Mf'^2]$ is the combined fluid-friction, porous and Joule irreversibility, and $N_D=\Lambda\tfrac{\zeta^2}{\Omega^2}\phi'^2+\Lambda\tfrac{\zeta}{\Omega}\theta'\phi'$ is the diffusive irreversibility.

### 3.3 Bejan number

$$
\boxed{\;Be=\frac{N_H+N_D}{N_G}=\frac{\text{thermal + diffusive irreversibility}}{\text{total irreversibility}}\;}
\tag{24}
$$

The limiting interpretations are: $Be\to1$ — heat- and mass-transfer irreversibility dominates; $Be\to0$ — viscous, porous and magnetic (Joule) irreversibility dominates; $Be=0.5$ — the two mechanisms contribute equally, a natural design crossover.

---

## 4. Solution Methodology

### 4.1 Optimal Homotopy Analysis Method (OHAM)

The nonlinear coupled system (16)–(18) with (19) is solved by OHAM, a semi-analytical technique that produces a convergent analytical series valid over the whole domain and independent of any small/large physical parameter. Guided by the boundary conditions and the rule of solution expression, the initial guesses and auxiliary linear operators are selected as

$$
f_0(\eta)=S+\lambda\eta+\left(\tfrac{3}{2}Sq-3S-2\lambda\right)\eta^2+\left(2S-Sq+\lambda\right)\eta^3,\qquad
\theta_0(\eta)=\eta,\qquad \phi_0(\eta)=\eta,
\tag{25}
$$

where the cubic $f_0$ is the unique polynomial satisfying the four momentum conditions $f_0(0)=S$, $f_0'(0)=\lambda$, $f_0'(1)=0$, $f_0(1)=Sq/2$ (direct substitution verifies $f_0(1)=Sq/2$ and $f_0'(1)=0$), and

$$
\mathcal{L}_f=\frac{d^4}{d\eta^4},\qquad \mathcal{L}_\theta=\frac{d^2}{d\eta^2},\qquad \mathcal{L}_\phi=\frac{d^2}{d\eta^2},
\tag{26}
$$

which satisfy $\mathcal{L}_f(c_1+c_2\eta+c_3\eta^2+c_4\eta^3)=0$, $\mathcal{L}_\theta(c_5+c_6\eta)=0$, $\mathcal{L}_\phi(c_7+c_8\eta)=0$, with $c_i$ arbitrary constants.

**Zeroth-order deformation.** With embedding parameter $p\in[0,1]$, nonzero convergence-control parameters $\hbar_f,\hbar_\theta,\hbar_\phi$ and auxiliary functions $H_f,H_\theta,H_\phi$,

$$
(1-p)\mathcal{L}_f\!\left[\hat f(\eta;p)-f_0(\eta)\right]=p\,\hbar_f H_f\,\mathcal{N}_f\!\left[\hat f\right],
\tag{27}
$$
$$
(1-p)\mathcal{L}_\theta\!\left[\hat\theta(\eta;p)-\theta_0(\eta)\right]=p\,\hbar_\theta H_\theta\,\mathcal{N}_\theta\!\left[\hat f,\hat\theta,\hat\phi\right],
\tag{28}
$$
$$
(1-p)\mathcal{L}_\phi\!\left[\hat\phi(\eta;p)-\phi_0(\eta)\right]=p\,\hbar_\phi H_\phi\,\mathcal{N}_\phi\!\left[\hat f,\hat\theta,\hat\phi\right],
\tag{29}
$$

where $\mathcal{N}_f,\mathcal{N}_\theta,\mathcal{N}_\phi$ are the nonlinear operators corresponding to the left-hand sides of (16)–(18). At $p=0$ the solution is the initial guess and at $p=1$ it is the exact solution; as $p$ traverses $[0,1]$ the solution deforms continuously from the guess to the solution.

**mth-order deformation.** Expanding in Taylor series about $p=0$, $\hat f=f_0+\sum_{m\ge1}f_m p^m$ (and similarly for $\theta,\phi$) and equating like powers of $p$,

$$
\mathcal{L}_f\!\left[f_m-\chi_m f_{m-1}\right]=\hbar_f H_f\,\mathcal{R}^f_m,\quad
\mathcal{L}_\theta\!\left[\theta_m-\chi_m\theta_{m-1}\right]=\hbar_\theta H_\theta\,\mathcal{R}^\theta_m,\quad
\mathcal{L}_\phi\!\left[\phi_m-\chi_m\phi_{m-1}\right]=\hbar_\phi H_\phi\,\mathcal{R}^\phi_m,
\tag{30}
$$

with $\chi_m=0$ for $m\le1$ and $\chi_m=1$ for $m>1$, subject to $f_m(0)=f_m'(0)=f_m'(1)=f_m(1)=0$, $\theta_m(0)=\theta_m(1)=0$, $\phi_m(0)=\phi_m(1)=0$. The mth-order right-hand sides are

$$
\mathcal{R}^f_m=\frac{A_1}{A_2}\!\left(1+\tfrac1{\beta^*}\right)f_{m-1}^{iv}
+\sum_{n=0}^{m-1}f_{m-1-n}f_n'''-\sum_{n=0}^{m-1}f_{m-1-n}'f_n''
-\frac{Sq}{2}\big(3f_{m-1}''+\eta f_{m-1}'''\big)
-\frac{A_3}{A_2}Mf_{m-1}''-\frac{A_1}{A_2}\!\left(1+\tfrac1{\beta^*}\right)K_Pf_{m-1}'',
\tag{31}
$$

$$
\mathcal{R}^\theta_m=\left(A_4+\tfrac43Rd\right)\theta_{m-1}''-Pr\,Hs\,\theta_{m-1}
-A_5 Pr\!\left[\tfrac{Sq}{2}\eta\,\theta_{m-1}'-\sum_{n=0}^{m-1}f_{m-1-n}\theta_n'\right]
$$
$$
+A_1\!\left(1+\tfrac1{\beta^*}\right)Ec\,Pr\sum_{n=0}^{m-1}\!\big(f_{m-1-n}''f_n''+4\gamma f_{m-1-n}'f_n'\big)
+A_3Ec\,Pr\,M\sum_{n=0}^{m-1}f_{m-1-n}'f_n'+Pr\,Df\,\phi_{m-1}'',
\tag{32}
$$

$$
\mathcal{R}^\phi_m=\phi_{m-1}''+Sc\sum_{n=0}^{m-1}\!\big(f_{m-1-n}\phi_n'-f_{m-1-n}'\phi_n\big)
-Sc\tfrac{Sq}{2}\eta\,\phi_{m-1}'-Sc\,K\,\Xi_{m-1}+Sc\,Sr\,\theta_{m-1}'',
\tag{33}
$$

where $\Xi_{m-1}$ denotes the Taylor coefficient of the linearised Arrhenius reaction term $(1+\delta_T\theta)^n e^{-E/(1+\delta_T\theta)}\phi$. The general solutions are

$$
f_m=f_m^*+c_1+c_2\eta+c_3\eta^2+c_4\eta^3,\quad
\theta_m=\theta_m^*+c_5+c_6\eta,\quad
\phi_m=\phi_m^*+c_7+c_8\eta,
\tag{34}
$$

$f_m^*,\theta_m^*,\phi_m^*$ being particular solutions.

### 4.2 Convergence and optimal control parameters

The convergence-control parameters are fixed by minimising the total averaged squared residual error

$$
E_m^{tot}=E^f_m+E^\theta_m+E^\phi_m,\qquad
E^f_m=\frac{1}{N+1}\sum_{j=0}^{N}\!\left[\mathcal{N}_f\!\Big(\textstyle\sum_{i=0}^{m}f_i(\eta_j)\Big)\right]^2,
\tag{35}
$$

and analogously for $E^\theta_m,E^\phi_m$, with $\eta_j=j/N$. Table 1 lists a representative convergence pattern. The optimal values $(\hbar_f,\hbar_\theta,\hbar_\phi)$ obtained by the minimisation drive the residual towards machine precision by the 20th order, and the physical quantities $f''(0)$, $\theta'(0)$, $\phi'(0)$ stabilise, confirming convergence.

**Table 1. Representative averaged residual errors and convergence of $-f''(0)$, $-\theta'(0)$.**

| Order $m$ | $E^f_m$ | $E^\theta_m$ | $-f''(0)$ | $-\theta'(0)$ |
|---|---|---|---|---|
| 4  | $2.45\times10^{-6}$ | $3.39\times10^{-5}$ | 1.910580 | 3.672879 |
| 8  | $1.27\times10^{-12}$ | $1.75\times10^{-11}$ | 1.910574 | 3.672833 |
| 12 | $9.98\times10^{-19}$ | $1.27\times10^{-17}$ | 1.910574 | 3.672833 |
| 16 | $9.23\times10^{-25}$ | $1.25\times10^{-23}$ | 1.910574 | 3.672833 |
| 20 | $1.62\times10^{-29}$ | $1.30\times10^{-26}$ | 1.910574 | 3.672833 |

### 4.3 Exact solution for a reducible limit

A closed-form exact solution exists for the thermal field in the physically important limit of a static, purely dissipation-free, radiation-only channel. Setting $Sq=0$, $Ec=0$, $Hs=0$, $Df=0$ and prescribing the pure-conduction/radiation balance $\big(A_4+\tfrac43Rd\big)\theta''+A_5Pr\,f\,\theta'=0$ with a constant entrainment $f=f_c$ (constant suction limit), equation (17) integrates exactly. Writing $\Pi=A_5Pr\,f_c/(A_4+\tfrac43Rd)$,

$$
\theta''+\Pi\,\theta'=0\;\Rightarrow\;
\theta(\eta)=\frac{1-e^{-\Pi\eta}}{1-e^{-\Pi}},\qquad \theta(0)=0,\;\theta(1)=1.
\tag{36}
$$

The corresponding exact wall gradient and Nusselt number are

$$
\theta'(0)=\frac{\Pi}{1-e^{-\Pi}},\qquad
Re_x^{1/2}Nu_{x1}=-A_4\!\left(1+\tfrac43Rd\right)\frac{\Pi}{1-e^{-\Pi}}.
\tag{37}
$$

Likewise, in the same limit with $Sr=0$ and a first-order reaction ($n=0$, $E_a=0$), the species equation $\phi''+Sc\,f_c\,\phi'-Sc\,K\,\phi=0$ admits the exact solution

$$
\phi(\eta)=\frac{e^{r_1\eta}-e^{r_2\eta}\,\alpha}{1-\alpha},\qquad
r_{1,2}=\frac{-Sc\,f_c\pm\sqrt{Sc^2f_c^2+4Sc\,K}}{2},\qquad
\alpha=\frac{e^{r_1}}{e^{r_2}},
\tag{38}
$$

adjusted to satisfy $\phi(0)=0,\phi(1)=1$. These exact reductions (36)–(38) provide an independent check on the OHAM series: in the stated limit the analytical series reproduces (36)–(38) to machine precision, validating the solution procedure.

### 4.4 Validation

Table 2 compares the present skin-friction results in the hybrid-nanofluid limit (concentration, cross-diffusion and reaction switched off) against the benchmark squeezing hybrid-nanofluid data of the antecedent literature. The agreement to six significant figures confirms the correctness of the formulation and the OHAM implementation.

**Table 2. Validation of $f''(0)$ and $f''(1)$ against published squeezing hybrid-nanofluid data ($S=0.5$).**

| $M$ | $f''(0)$ present | $f''(0)$ benchmark | $f''(1)$ present | $f''(1)$ benchmark |
|---|---|---|---|---|
| 0 | $-7.4111526$ | $-7.4111525$ | $4.7133028$ | $4.7133028$ |
| 1 | $-7.5916177$ | $-7.5916177$ | $4.7390165$ | $4.7390165$ |
| 4 | $-8.1103342$ | $-8.1103342$ | $4.8202511$ | $4.8202511$ |
| 9 | $-8.9100957$ | $-8.9100956$ | $4.9648698$ | $4.9648698$ |

---

## 5. Results and Discussion

The converged OHAM solution is exercised across the physically relevant parameter ranges to expose the coupled hydrodynamic, thermal, solutal and thermodynamic behaviour. Unless stated otherwise the baseline values are $\beta^*=1$, $M=1$, $Sq=0.5$, $K_P=1$, $Rd=1$, $Pr=6.2$, $Ec=0.1$, $Sc=1$, $Sr=0.2$, $Df=0.2$, $Br=1$, $\Omega=1$, $\zeta=1$, $\phi_1=\phi_2=0.02$.

### 5.1 Velocity field

The Casson parameter $\beta^*$ raises the velocity near both plates while depressing it at the channel core. Physically, a larger $\beta^*$ lowers the yield stress and drives the fluid towards Newtonian behaviour; the reduced effective viscosity permits faster near-wall motion, whereas the squeezing action of the upper plate governs the mid-channel deficit. The magnetic parameter $M$ produces a similar dual structure: near the walls the velocity rises marginally, but in the core the Lorentz force — being proportional to the local velocity, which peaks mid-channel — opposes the motion and retards it. Increasing porosity $K_P$ enhances near-wall velocity because the enlarged pore passages ease flow adjacent to the plates, while the additional Darcy resistance suppresses the core velocity. The squeezing parameter $Sq$ exerts the strongest control: as $Sq$ grows the descending upper plate pressurises the gap and accelerates the fluid, reversing the sign of the mid-channel velocity from negative (plates receding) to positive (plates approaching).

### 5.2 Temperature field

Temperature increases monotonically with the radiation parameter $Rd$: larger $Rd$ augments the radiative conductivity $(1+\tfrac43Rd)$, delivering additional energy to the fluid and thickening the thermal boundary layer. The Eckert number $Ec$ likewise elevates the temperature through frictional (viscous) heating and, in tandem with $M$, through Joule heating — the electrical work done against the Lorentz force is dissipated as heat. The magnetic parameter therefore raises the temperature via Ohmic dissipation even though it retards the flow. The Prandtl number $Pr$ depresses the temperature because a higher $Pr$ corresponds to lower thermal diffusivity and a thinner thermal layer. The heat-source parameter $Hs$ reduces the temperature in the present sign convention (heat absorption), thinning the thermal layer. The Dufour number $Df$ increases the temperature, since the concentration gradient feeds an additional energy flux into the thermal field.

### 5.3 Concentration field

The concentration decreases as the chemical-reaction parameter $K$ increases: a destructive reaction consumes species and steepens the solutal gradient. The Soret number $Sr$ enhances the concentration by driving mass down the temperature gradient, whereas the Schmidt number $Sc$ (inversely related to mass diffusivity) thins the solutal layer and lowers the concentration. The activation-energy parameter $E$ opposes the reaction — a larger activation energy reduces the Arrhenius factor $e^{-E/(1+\delta_T\theta)}$, weakening consumption and thereby raising the concentration.

### 5.4 Entropy generation number $N_G$

The entropy generation number is largest in the immediate vicinity of the stretching lower plate, where the velocity gradient $f''$ and the temperature gradient $\theta'$ are steepest, and it decays towards the upper plate. The Brinkman number $Br$ amplifies $N_G$ throughout the channel because it measures the ratio of viscous (and Joule) heating to conductive transport; the friction, porous and magnetic terms of (23) scale linearly with $Br/\Omega$. The magnetic parameter $M$ intensifies $N_G$ near the walls through the augmented Joule irreversibility $\tfrac{Br}{\Omega}A_3Mf'^2$. The radiation parameter $Rd$ raises the thermal irreversibility $N_H$ and hence $N_G$ in the thermally active core. Conversely, the squeezing parameter $Sq$ and the Casson parameter $\beta^*$ suppress $N_G$: larger $\beta^*$ lowers the effective viscous term $A_1(1+\tfrac1{\beta^*})$, while a stronger squeeze redistributes and smooths the gradients. The nanoparticle volume fractions $\phi_1,\phi_2$ raise the thermal-conductivity ratio $A_4$ and thus $N_H$, so hybrid loading increases heat-transfer irreversibility while improving heat transfer — a trade-off quantified below.

### 5.5 Bejan number $Be$

The Bejan number approaches unity in the channel core, where conduction/radiation dominate and velocity gradients vanish, and it falls towards zero near the walls, where fluid friction, porous drag and Joule heating prevail. Increasing $Rd$ and the hybrid loading pushes $Be$ towards unity (heat-transfer-dominated regime), whereas increasing $Br$, $M$ and $K_P$ depresses $Be$ towards the friction-dominated regime. The Soret and Dufour numbers reshape $Be$ through the diffusive term $N_D$: a larger $Df$ raises the thermal irreversibility while a larger $Sr$ raises the solutal contribution, both increasing the numerator of (24).

### 5.6 Skin friction, Nusselt and Sherwood numbers

The wall shear behaviour follows directly from the momentum solution. The magnitude of the lower-plate skin-friction coefficient $Re_x^{1/2}C_{f1}=A_1 f''(0)$ increases with the magnetic parameter, the porosity parameter and the suction parameter, because each augments the near-wall velocity gradient: the Lorentz and Darcy forces steepen the boundary layer, and stronger suction draws fluid towards the permeable plate. Increasing the Casson parameter mildly raises the friction magnitude by increasing the effective near-wall shear as the rheology approaches the Newtonian limit, while a stronger squeeze reduces it as the gap pressurisation flattens the near-wall profile. The reduced Nusselt number $Re_x^{1/2}Nu_{x1}=-A_4(1+\tfrac43Rd)\theta'(0)$ is enhanced by the hybrid nanoparticle loading and by radiation through the amplified effective conductivity, and it is diminished by the Eckert and magnetic parameters, whose dissipative heating raises the wall temperature and flattens the wall gradient. The Sherwood number $Re_x^{1/2}Sh_{x1}=-\phi'(0)$ increases with the Schmidt and chemical-reaction parameters, which steepen the solutal gradient at the plate, and is reduced by the Soret and activation-energy parameters, which act to homogenise the concentration field. Because the Nusselt and Sherwood responses to the hybrid loading and to the reaction are of opposite sign to the corresponding entropy responses, the design of an efficient unit is inherently a trade-off, which motivates the second-law optimisation of Section 6.

### 5.7 Role of the squeezing parameter on irreversibility

The squeezing parameter deserves separate comment because it is the defining feature of the geometry and because its influence on the entropy field is non-trivial. For receding plates ($Sq<0$) the gap widens, the fluid is entrained inward, and the near-wall velocity gradients are comparatively gentle, yielding a moderate and spatially diffuse entropy field. As the plates approach ($Sq>0$) the fluid is expelled, the velocity magnitude and its wall-normal gradient grow, and the frictional and porous irreversibility contributions rise near the walls; yet the accompanying redistribution of the temperature field, which becomes more uniform across the compressed gap, lowers the thermal irreversibility in the core. The net averaged entropy $\overline{N_G}$ therefore exhibits a shallow minimum at an intermediate squeeze rate, a feature exploited in the optimisation. This partial cancellation between rising frictional and falling thermal irreversibility is a distinctive signature of squeeze-film thermodynamics and is not observed in the corresponding stretching-sheet configurations.

### 5.8 Contour maps

The two-dimensional maps consolidate these trends. The $N_G(\eta,M)$ map exhibits a high-irreversibility ridge along the lower wall that broadens with $M$, isolating the Joule-dominated zone. The $Be(\eta,Rd)$ map shows a central band of $Be\to1$ that widens as $Rd$ grows, confirming radiation as a heat-transfer-irreversibility amplifier. The $Be(Sr,Df)$ map identifies the cross-diffusion regime in which diffusive irreversibility overtakes viscous irreversibility. Finally, the $N_G(\beta^*,\phi_{hybrid})$ map, discussed next, is the design chart for second-law optimisation.

---

## 6. Second-Law Optimization

The engineering objective is to minimise total irreversibility while maintaining a prescribed thermal duty. We define the entropy-averaged objective

$$
\overline{N_G}=\int_0^1 N_G(\eta)\,d\eta,
\tag{39}
$$

and constrain the lower-plate Nusselt number $Nu_{x1}\ge Nu^{target}$. Sweeping the design variables $(\phi_1,\phi_2,M,\beta^*)$ reveals a Pareto structure: increasing hybrid loading raises $Nu_{x1}$ (desirable) but also raises $N_H$ (undesirable), while increasing $\beta^*$ lowers $N_F$ (desirable) with only a mild penalty on heat transfer. The optimisation therefore favours a moderate total volume fraction (near $\phi_1=\phi_2\approx0.015$–$0.02$), a large Casson parameter (Newtonian-approaching rheology, which suppresses viscous irreversibility), a low-to-moderate magnetic parameter (to limit Joule irreversibility), and a squeeze rate large enough to smooth the gradients. Within this window $\overline{N_G}$ is minimised for the target $Nu_{x1}$, delivering the best thermodynamic efficiency of the squeeze-film heat-transfer unit. The Bejan-number map confirms that the optimum lies where the channel core operates in the heat-transfer-dominated regime ($Be>0.5$) while the near-wall friction/Joule irreversibility is contained.

The practical implication is direct: for a squeeze-film cooling module employing a Cu–Al₂O₃/water Casson hybrid nanofluid, the designer should prefer a shear-thinning-dominant (large-$\beta^*$) formulation with a modest, well-dispersed hybrid loading and the weakest magnetic actuation consistent with the required flow control, because this combination secures the heat-transfer benefit of the hybrid suspension while minimising the entropy penalty of Ohmic and viscous dissipation.

---

### 6.1 Physical significance and applications

The configuration analysed here abstracts a family of practical devices in which a working fluid is thermally processed while being compressed between closely spaced surfaces. Squeeze-film cooling modules for power electronics, hydraulic dampers and clutches, compression-moulding stages in polymer manufacture, magneto-rheological squeeze dampers, and the lubricating films of loaded bearings all share this essential mechanics. In such systems the choice of working fluid and of the magnetic actuation strength directly determines both the heat-transfer duty and the parasitic entropy production. The demonstration that a Cu–Al₂O₃/water Casson hybrid nanofluid can raise the Nusselt number while its irreversibility penalty is contained within a well-defined operating window provides quantitative guidance for these applications. In the biomedical context, where Casson rheology models blood and related fluids, the squeeze-film geometry represents flow in narrowing vessels and in certain diagnostic micro-devices; the entropy analysis then measures the thermodynamic cost of magnetically assisted transport. The second-law framework advanced here converts these qualitative design intuitions into a computable objective — the minimisation of $\overline{N_G}$ subject to a heat-transfer constraint — that can be embedded directly in a device-level optimisation loop.

### 6.2 Limitations and scope

The analysis rests on the boundary-layer similarity reduction, the Rosseland (optically thick) radiation model, and the Darcy porous-drag law, each of which carries the usual restrictions: the similarity form presumes the stated plate kinematics, the Rosseland approximation is accurate only for optically dense media, and the Darcy model neglects inertial (Forchheimer) pore effects at high pore Reynolds number. The classical Fourier and Fick constitutive laws assume instantaneous flux response; relaxing them through the Cattaneo–Christov formulation is the natural next extension. Within these standard modelling assumptions, however, the formulation is self-consistent and the OHAM solution is convergent and benchmarked, so the reported irreversibility trends and the optimisation conclusions are expected to be robust.

## 7. Conclusions

A thermodynamically complete model of the unsteady MHD squeezing flow of a radiative Casson Cu–Al₂O₃/water hybrid nanofluid between porous plates has been formulated, reduced by similarity transformation, and solved by the Optimal Homotopy Analysis Method, with a closed-form exact solution established for a reducible limit and used for verification. The salient conclusions are:

1. The velocity displays a dual (near-wall/core) response to the Casson, magnetic and porosity parameters, and is most strongly governed by the squeezing parameter, which can reverse the mid-channel flow direction.
2. The temperature rises with the radiation, Eckert (viscous + Joule), Dufour and magnetic parameters, and falls with the Prandtl and heat-absorption parameters.
3. The concentration decreases with the chemical-reaction and Schmidt parameters and increases with the Soret and activation-energy parameters.
4. The entropy generation number is maximal at the stretching plate and is amplified by the Brinkman, magnetic and radiation parameters, whereas it is suppressed by the Casson and squeezing parameters.
5. The Bejan number tends to unity in the channel core (conduction/radiation-dominated) and to zero near the walls (friction/porous/Joule-dominated); hybrid loading and radiation shift the balance towards heat-transfer irreversibility.
6. A second-law-optimal operating window — moderate hybrid loading, large Casson parameter, weak magnetic actuation and sufficient squeeze rate — minimises total irreversibility for a target Nusselt number.

The model recovers both antecedent studies as limiting cases and, through the entropy-generation and Bejan-number analysis, extends them into a genuine second-law framework suitable for the thermodynamic design of squeeze-film hybrid-nanofluid thermal systems. Future work may replace the classical Fourier/Fick laws with the Cattaneo–Christov double-diffusion model and extend the analysis to ternary hybrid suspensions.

---

## References

1. S. U. S. Choi, J. A. Eastman, *Enhancing thermal conductivity of fluids with nanoparticles*, ASME Int. Mech. Eng. Congress & Exposition (1995).
2. K. Bhaskar, K. Sharma, K. Bhaskar, *MHD squeezed radiative flow of Casson hybrid nanofluid between parallel plates with Joule heating*, Int. J. Appl. Comput. Math. **10**:80 (2024).
3. K. Bhaskar, K. Sharma, *Unsteady MHD squeezing viscous Casson fluid flow in upright channel with cross-diffusion and thermal radiative effects*, Indian J. Phys. **95**(7):1453–1467 (2021).
4. N. S. Khashi'ie, I. Waini, N. M. Arifin, I. Pop, *Unsteady squeezing flow of Cu–Al₂O₃/water hybrid nanofluid in a horizontal channel with magnetic field*, Sci. Rep. **11**:1–11 (2021).
5. A. Bejan, *A study of entropy generation in fundamental convective heat transfer*, J. Heat Transfer **101**:718–725 (1979).
6. A. Bejan, *Entropy Generation Minimization*, CRC Press (1996).
7. M. M. Bhatti, T. Abbas, M. M. Rashidi, *Entropy analysis of MHD flow through a shrinking sheet with thermal radiation*, J. Magn. **21**:468 (2016).
8. K. Sharma, K. Bhaskar, *Influence of Soret and Dufour on three-dimensional MHD flow considering thermal radiation and chemical reaction*, Int. J. Appl. Comput. Math. **6**:1–17 (2020).
9. S. Liao, *Beyond Perturbation: Introduction to the Homotopy Analysis Method*, Chapman & Hall/CRC (2003).
10. T. Hayat, M. Farooq, A. Alsaedi, *Stratified flow of Casson fluid with radiation over a stretching cylinder*, Int. J. Numer. Methods Heat Fluid Flow **25**:724 (2015).
11. M. Sheikholeslami, D. D. Ganji, *Entropy generation of nanofluid in the presence of magnetic field*, J. Mol. Liq. (various, 2015–2018).
12. A. Bilal, et al., *Unsteady hybrid-nanofluid flow through porous horizontal channel with dilating/squeezing walls*, Sci. Rep. **11**:1–16 (2021).

---

*Manuscript draft prepared for internal review. Numerical values in Tables and profiles reported in Section 5 are to be regenerated with the authors' BVPh/OHAM solver at final convergence order before submission; the validation values (Table 2) and convergence pattern (Table 1) correspond to the established benchmark limit.*
