# Entropy Generation and Irreversibility Analysis of Unsteady EMHD Squeezing Flow of a Carreau Hybrid Nanofluid (AA7072–AA7075/Methanol) Between Parallel Porous Plates

## Abstract

The present investigation reports a comprehensive mathematical and numerical study of the second-law behaviour of an unsteady, two-dimensional, electro-magneto-hydrodynamic (EMHD) squeezing flow of a Carreau hybrid nanofluid confined between two parallel porous plates. Aluminium-alloy nanoparticles AA7072 and AA7075 are suspended in methanol to synthesise the hybrid working fluid, a combination selected for its superior effective thermal conductivity and electrical response. The physical model incorporates a transverse magnetic field, an aligned electric field, Darcy–Forchheimer porous drag, nonlinear thermal radiation, viscous dissipation, Joule heating, Soret and Dufour cross-diffusion, and a first-order homogeneous chemical reaction. Realistic transport phenomena are captured through velocity, thermal (Biot-type) and solutal slip boundary conditions. The coupled nonlinear partial differential equations governing momentum, energy and species transport are reduced to a system of ordinary differential equations by appropriate similarity transformations and solved with the MATLAB `bvp4c` collocation solver. Beyond the conventional field analysis, the local volumetric entropy generation rate is formulated from the four dominant irreversibility sources—heat conduction, fluid friction, Joule dissipation and mass diffusion—and recast into a dimensionless entropy generation number, together with the Bejan number that measures the relative dominance of thermal irreversibility. A detailed parametric study establishes that the squeezing parameter, Weissenberg number, magnetic parameter, radiation parameter, Brinkman number and diffusive-irreversibility parameter exert first-order control over the entropy production. It is shown that entropy generation attains its maximum near the plates where velocity and temperature gradients are steepest, and that the Bejan number distribution reveals a transition from friction-dominated irreversibility in the core to conduction-dominated irreversibility at the walls. The findings offer design guidance for squeeze-film dampers, micro-electromechanical cooling channels and hydraulic actuators employing engineered hybrid coolants.

**Keywords:** Carreau hybrid nanofluid; Entropy generation; Bejan number; EMHD squeezing flow; Darcy–Forchheimer; Soret–Dufour; bvp4c

---

## Nomenclature

| Symbol | Description | Symbol | Description |
|--------|-------------|--------|-------------|
| a, γ | dimensional constants (s⁻¹) | Br | Brinkman number |
| B(t) | time-dependent magnetic field | Be | Bejan number |
| C | concentration (mol m⁻³) | Da | Darcy number |
| cₚ | specific heat (J kg⁻¹ K⁻¹) | Df | Dufour number |
| D_B | Brownian diffusion coefficient | Ec | Eckert number |
| E₀ | electric field strength | Fr | Forchheimer parameter |
| f | dimensionless stream function | Ha, M | magnetic parameter |
| h(t) | plate separation (m) | K | chemical reaction parameter |
| n | Carreau power-law index | N_G, N_s | entropy generation number |
| Pr | Prandtl number | Rd | radiation parameter |
| Sc | Schmidt number | Sq | squeezing parameter |
| Sr | Soret number | We | Weissenberg number |
| T | temperature (K) | u, v | velocity components (m s⁻¹) |
| **Greek** | | | |
| β₁ | temperature difference parameter | η | similarity variable |
| θ | dimensionless temperature | φ | dimensionless concentration |
| Γ | Carreau material time constant | κ | thermal conductivity |
| μ | dynamic viscosity | ρ | density |
| σ | electrical conductivity | Ω | diffusive irreversibility parameter |
| φ₁, φ₂ | nanoparticle volume fractions | | |
| **Subscripts** | | | |
| f | base fluid (methanol) | hnf | hybrid nanofluid |
| s1 | AA7072 nanoparticle | s2 | AA7075 nanoparticle |

---

## 1. Introduction

The relentless drive toward compact, high-flux thermal-management devices has placed the intensification of convective heat transfer at the centre of contemporary engineering research. Conventional heat-transfer liquids such as water, ethylene glycol and light alcohols possess intrinsically modest thermal conductivities, which restricts their usefulness in the miniaturised cooling passages of power electronics, microreactors and precision machine tools. The pioneering proposal of Choi and Eastman [1] to disperse metallic and oxide nanoparticles within a base liquid—thereby producing a *nanofluid*—triggered a sustained research effort to exploit the anomalously high effective conductivity of such suspensions. Subsequent experimental and theoretical work demonstrated that the thermal, rheological and electrical properties of nanofluids can be tuned by adjusting particle material, size, shape and loading [2, 3]. A natural extension of the single-particle nanofluid is the *hybrid nanofluid*, in which two chemically distinct nanoparticle species are co-dispersed in the same carrier so that the composite inherits complementary advantages of each constituent [4, 5]. Hybrid suspensions have been shown to deliver a more favourable trade-off between thermal enhancement and pumping penalty than their mono-particle counterparts [6, 7].

Among candidate nanoparticles, the aluminium alloys AA7072 and AA7075 are particularly attractive because they combine a high electrical conductivity with excellent corrosion resistance and low density. Tlili et al. [8] investigated a three-dimensional magnetohydrodynamic flow of an AA7072–AA7075/methanol hybrid nanofluid over a surface of variable thickness and reported a pronounced enhancement of the heat-transfer coefficient relative to methanol alone. The same alloy pairing has since been adopted in a variety of boundary-layer and channel-flow studies [9, 10], and it is the working combination retained in the present analysis. Methanol is selected as the base liquid owing to its low freezing point, low viscosity and compatibility with electronic-cooling applications [11].

The rheological response of many industrially relevant suspensions departs markedly from the Newtonian idealisation. Polymeric coolants, biofluids, paints and particle-laden liquids exhibit shear-thinning or shear-thickening behaviour that must be represented by a generalised constitutive law. The Carreau model, introduced by Pierre Carreau, is especially versatile because it recovers Newtonian behaviour at both vanishing and infinite shear rates while describing a power-law region at intermediate shear [12]. Shah et al. [13] examined chemically reacting magnetised Carreau flow over a nonlinear stretching surface, whereas Wahab et al. [14] analysed an inclined magnetised Carreau fluid with an infinite-shear-rate viscosity correction. Mkhatshwa and Khumalo [15] specifically addressed irreversibility in an EMHD Darcy–Forchheimer Carreau hybrid nanofluid over a stretchable surface, underscoring the growing interest in coupling non-Newtonian rheology with second-law analysis. Additional treatments of Carreau transport under thermal radiation and mixed convection appear in [16, 17].

Squeezing flows—generated when two surfaces approach or separate while a viscous fluid occupies the intervening gap—are ubiquitous in lubrication systems, squeeze-film dampers, polymer moulding, hydraulic machinery and biomechanical joints [18, 19]. The unsteady, moving-boundary character of squeezing flow renders its analysis considerably richer than that of steady boundary layers. Sobamowo and Akinshilo [20] applied the homotopy perturbation method to squeezing Casson flow, while Ahmad et al. [21, 22] explored squeezed Sutterby and slip-affected flows between parallel plates. The combined influence of magnetic fields, porous media and cross-diffusion on unsteady squeezing Casson flow was reported by Bhaskar and Sharma [23], who employed the optimal homotopy analysis method and highlighted the reversed roles of Soret and Dufour effects. The present study builds directly upon this squeezing-channel configuration but replaces the single-particle Casson fluid with a Carreau hybrid nanofluid and, crucially, introduces a full second-law treatment.

The simultaneous transport of heat and mass under coupled gradients gives rise to the Soret (thermo-diffusion) and Dufour (diffusion-thermo) effects. Since Charles Soret's nineteenth-century observations, these cross-diffusion mechanisms have been recognised as significant whenever temperature and concentration differences are comparable [24, 25]. Their treatment in non-Newtonian and nanofluid contexts has been advanced by numerous authors [26, 27, 28], with Soret and Dufour numbers shown to modify the Nusselt and Sherwood numbers in opposite senses. Nonlinear thermal radiation, viscous dissipation and Joule heating further complicate the energy balance and are indispensable in high-temperature or electrically driven systems [29, 30, 31]. The role of Darcy–Forchheimer porous resistance, comprising both viscous and inertial drag contributions, has likewise been established as a governing factor in porous-channel flows [32, 33].

Although the first-law (energy-conservation) analysis quantifies *how much* heat is transferred, it is silent about the thermodynamic *quality* of the process. The second law of thermodynamics, expressed through entropy generation, identifies and ranks the irreversibilities that degrade available work. Following the seminal framework of Bejan [34, 35], entropy-generation minimisation has become a standard design paradigm for thermal systems. Entropy analyses of nanofluid and hybrid-nanofluid flows have been reported for stretching sheets, cavities, microchannels and rotating systems [36, 37, 38, 39], consistently revealing that magnetic, radiative and frictional effects are the principal contributors to irreversibility. Recent studies have extended entropy analysis to Carreau and other generalised-Newtonian fluids [40, 41], and to squeezing configurations [42, 43]. Nonetheless, a careful survey of the literature discloses a distinct gap: no previous work has performed a coupled first- and second-law analysis of an *unsteady EMHD squeezing flow of an AA7072–AA7075/methanol Carreau hybrid nanofluid* through a Darcy–Forchheimer porous channel with Soret–Dufour cross-diffusion, nonlinear radiation, Joule heating and multi-mode slip.

The novelty and objectives of the present study are therefore:

1. To formulate, for the first time, the coupled momentum, energy and species equations for an unsteady EMHD squeezing Carreau hybrid nanofluid in a porous channel and to reduce them to a similarity ODE system.
2. To derive the local volumetric entropy generation rate incorporating heat-conduction, fluid-friction, Joule-heating and mass-diffusion irreversibilities, and to express it as a dimensionless entropy generation number together with the Bejan number.
3. To obtain accurate numerical solutions via `bvp4c` and validate them against limiting cases available in the literature.
4. To quantify, through an extensive parametric campaign presented in seven figures and six tables, the influence of the squeezing parameter, Weissenberg number, power-law index, magnetic and electric parameters, radiation, Eckert, Brinkman, Soret, Dufour and chemical-reaction parameters on the flow, thermal, solutal and irreversibility fields.

---

## 2. Mathematical Formulation

### 2.1 Physical configuration and assumptions

Consider the unsteady, two-dimensional, laminar and incompressible flow of a Carreau hybrid nanofluid squeezed between two infinite parallel porous plates separated by a time-dependent distance

$$
h(t) = \left[\frac{\nu_f (1 - \gamma t)}{a}\right]^{1/2}. \tag{1}
$$

The Cartesian coordinates $x$ and $y$ are aligned along and normal to the lower plate, respectively. The lower plate is stretched with velocity $U_w(x,t)$, while the upper plate moves with the normal squeezing velocity $v_h = \mathrm{d}h/\mathrm{d}t$. The plates approach one another for $\gamma > 0$ (squeezing) and separate for $\gamma < 0$. A transverse, time-dependent magnetic field

$$
B(t) = \frac{B_0}{(1-\gamma t)^{1/2}} \tag{2}
$$

is imposed in the $y$-direction, together with an aligned electric field $E(t)=E_0 (1-\gamma t)^{-1/2}$. The induced magnetic field is neglected under the small magnetic Reynolds number assumption. The channel is saturated by a homogeneous, isotropic Darcy–Forchheimer porous medium. AA7072 and AA7075 nanoparticles are assumed to be uniformly dispersed in methanol and in thermal equilibrium with the base fluid, with no slip between phases.

### 2.2 Carreau hybrid nanofluid constitutive model

For the Carreau fluid the extra-stress tensor is expressed through an apparent viscosity that depends on the shear rate. The Cauchy stress tensor reads

$$
\boldsymbol{\tau} = -p\,\mathbf{I} + \mu(\dot{\gamma})\,\mathbf{A}_1, \tag{3}
$$

where $\mathbf{A}_1 = \nabla\mathbf{V} + (\nabla\mathbf{V})^{\mathrm{T}}$ is the first Rivlin–Ericksen tensor and the shear-dependent viscosity obeys

$$
\mu(\dot{\gamma}) = \mu_\infty + (\mu_0 - \mu_\infty)\left[1 + (\Gamma\dot{\gamma})^2\right]^{\frac{n-1}{2}}. \tag{4}
$$

Here $\Gamma$ is the material time constant, $n$ the power-law index, and $\mu_0,\mu_\infty$ the zero- and infinite-shear-rate viscosities. The scalar shear rate is

$$
\dot{\gamma} = \sqrt{\tfrac{1}{2}\,\mathrm{tr}(\mathbf{A}_1^2)}. \tag{5}
$$

Taking the customary limit $\mu_\infty \to 0$, the effective viscosity becomes

$$
\mu(\dot{\gamma}) = \mu_0\left[1 + (\Gamma\dot{\gamma})^2\right]^{\frac{n-1}{2}}. \tag{6}
$$

The model recovers pseudoplastic (shear-thinning) behaviour for $0<n<1$ and dilatant (shear-thickening) behaviour for $n>1$, while $n=1$ or $\Gamma\to 0$ returns the Newtonian limit.

### 2.3 Governing equations

Invoking the boundary-layer approximation appropriate to the thin squeezing gap, the conservation equations of mass, momentum, energy and species for the Carreau hybrid nanofluid are:

**Continuity:**

$$
\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0. \tag{7}
$$

**x-Momentum:**

$$
\begin{aligned}
\frac{\partial u}{\partial t} + u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y}
= &\; \frac{\mu_{hnf}}{\rho_{hnf}}\frac{\partial^2 u}{\partial y^2}\left[1 + \Gamma^2\left(\frac{\partial u}{\partial y}\right)^2\right]^{\frac{n-1}{2}} \\
& + \frac{\mu_{hnf}}{\rho_{hnf}}(n-1)\Gamma^2\frac{\partial^2 u}{\partial y^2}\left(\frac{\partial u}{\partial y}\right)^2\left[1 + \Gamma^2\left(\frac{\partial u}{\partial y}\right)^2\right]^{\frac{n-3}{2}} \\
& + \frac{\sigma_{hnf}}{\rho_{hnf}}\left(E_0 B_0 - B(t)^2 u\right) - \frac{\mu_{hnf}}{\rho_{hnf}}\frac{u}{K_p^*} - \frac{C_b}{\sqrt{K_p^*}}u^2 .
\end{aligned} \tag{8}
$$

**y-Momentum:**

$$
\frac{\partial v}{\partial t} + u\frac{\partial v}{\partial x} + v\frac{\partial v}{\partial y}
= -\frac{1}{\rho_{hnf}}\frac{\partial p}{\partial y} + \frac{\mu_{hnf}}{\rho_{hnf}}\frac{\partial^2 v}{\partial y^2}. \tag{9}
$$

**Energy:**

$$
\begin{aligned}
\frac{\partial T}{\partial t} + u\frac{\partial T}{\partial x} + v\frac{\partial T}{\partial y}
= &\; \frac{\kappa_{hnf}}{(\rho c_p)_{hnf}}\frac{\partial^2 T}{\partial y^2}
- \frac{1}{(\rho c_p)_{hnf}}\frac{\partial q_r}{\partial y}
+ \frac{\mu_{hnf}}{(\rho c_p)_{hnf}}\left(\frac{\partial u}{\partial y}\right)^2\left[1 + \Gamma^2\left(\frac{\partial u}{\partial y}\right)^2\right]^{\frac{n-1}{2}} \\
& + \frac{\sigma_{hnf}}{(\rho c_p)_{hnf}}\left(uB_0 - E_0\right)^2
+ \frac{D_B K_T}{c_s (c_p)_{hnf}}\frac{\partial^2 C}{\partial y^2}.
\end{aligned} \tag{10}
$$

**Concentration:**

$$
\frac{\partial C}{\partial t} + u\frac{\partial C}{\partial x} + v\frac{\partial C}{\partial y}
= D_B\frac{\partial^2 C}{\partial y^2} + \frac{D_B K_T}{T_m}\frac{\partial^2 T}{\partial y^2} - k_1(C - C_h). \tag{11}
$$

In Eqs. (8)–(11) $u,v$ are the velocity components, $T$ the temperature, $C$ the species concentration, $C_b$ the Forchheimer drag coefficient, $K_p^*$ the permeability, $q_r$ the radiative flux, $k_1$ the reaction rate, $K_T$ the thermal-diffusion ratio, $c_s$ the concentration susceptibility, and $T_m$ the mean fluid temperature.

### 2.4 Nonlinear thermal radiation

Using the Rosseland diffusion approximation, the radiative heat flux is

$$
q_r = -\frac{4\sigma^*}{3k^*}\frac{\partial T^4}{\partial y} = -\frac{16\sigma^*}{3k^*}T^3\frac{\partial T}{\partial y}, \tag{12}
$$

so that its divergence becomes

$$
\frac{\partial q_r}{\partial y} = -\frac{16\sigma^*}{3k^*}\left[3T^2\left(\frac{\partial T}{\partial y}\right)^2 + T^3\frac{\partial^2 T}{\partial y^2}\right], \tag{13}
$$

where $\sigma^*$ is the Stefan–Boltzmann constant and $k^*$ the mean absorption coefficient. The temperature is written as $T = T_0\left[1 + (\theta_r - 1)\theta\right]$ with $\theta_r = T_w/T_0$ the temperature-ratio parameter, retaining the full nonlinearity of radiation.

### 2.5 Thermophysical properties of the hybrid nanofluid

The effective properties of the AA7072–AA7075/methanol suspension are modelled with well-established mixture correlations. The dynamic viscosity follows the Brinkman relation,

$$
\mu_{hnf} = \frac{\mu_f}{(1-\phi_1)^{2.5}(1-\phi_2)^{2.5}}, \tag{14}
$$

the effective density is

$$
\rho_{hnf} = (1-\phi_2)\left[(1-\phi_1)\rho_f + \phi_1\rho_{s1}\right] + \phi_2\rho_{s2}, \tag{15}
$$

and the heat capacity is

$$
(\rho c_p)_{hnf} = (1-\phi_2)\left[(1-\phi_1)(\rho c_p)_f + \phi_1(\rho c_p)_{s1}\right] + \phi_2(\rho c_p)_{s2}. \tag{16}
$$

The thermal conductivity is evaluated through the two-step Maxwell model,

$$
\frac{\kappa_{bf}}{\kappa_f} = \frac{\kappa_{s1} + 2\kappa_f - 2\phi_1(\kappa_f - \kappa_{s1})}{\kappa_{s1} + 2\kappa_f + \phi_1(\kappa_f - \kappa_{s1})}, \tag{17}
$$

$$
\frac{\kappa_{hnf}}{\kappa_{bf}} = \frac{\kappa_{s2} + 2\kappa_{bf} - 2\phi_2(\kappa_{bf} - \kappa_{s2})}{\kappa_{s2} + 2\kappa_{bf} + \phi_2(\kappa_{bf} - \kappa_{s2})}. \tag{18}
$$

The electrical conductivity is likewise obtained in two stages,

$$
\frac{\sigma_{bf}}{\sigma_f} = 1 + \frac{3\left(\tfrac{\sigma_{s1}}{\sigma_f}-1\right)\phi_1}{\left(\tfrac{\sigma_{s1}}{\sigma_f}+2\right) - \left(\tfrac{\sigma_{s1}}{\sigma_f}-1\right)\phi_1}, \tag{19}
$$

$$
\frac{\sigma_{hnf}}{\sigma_{bf}} = 1 + \frac{3\left(\tfrac{\sigma_{s2}}{\sigma_{bf}}-1\right)\phi_2}{\left(\tfrac{\sigma_{s2}}{\sigma_{bf}}+2\right) - \left(\tfrac{\sigma_{s2}}{\sigma_{bf}}-1\right)\phi_2}, \tag{20}
$$

and the effective kinematic viscosity is $\nu_{hnf} = \mu_{hnf}/\rho_{hnf}$ (Eq. 21):

$$
\nu_{hnf} = \frac{\mu_{hnf}}{\rho_{hnf}}. \tag{21}
$$

Here $\phi_1$ and $\phi_2$ denote the volume fractions of AA7072 and AA7075, respectively, and subscripts $s1$, $s2$, $f$ identify the two solids and the base fluid.

### 2.6 Similarity transformation

The variable plate spacing motivates the introduction of the similarity variable and dimensionless functions

$$
\eta = \frac{y}{h(t)}, \qquad \psi = \left[\frac{a\nu_f}{1-\gamma t}\right]^{1/2}x\,f(\eta), \tag{22}
$$

$$
u = \frac{ax}{1-\gamma t}f'(\eta), \qquad v = -\left[\frac{a\nu_f}{1-\gamma t}\right]^{1/2}f(\eta), \tag{23}
$$

$$
\theta(\eta) = \frac{T - T_h}{T_w - T_0}, \qquad \phi(\eta) = \frac{C - C_h}{C_w - C_0}, \tag{24}
$$

where the stream function $\psi$ satisfies $u = \partial\psi/\partial y$ and $v = -\partial\psi/\partial x$, thereby identically fulfilling continuity Eq. (7). The wall temperature and concentration are prescribed as

$$
T_w = T_0 + \frac{a x}{1-\gamma t}\, d_1, \qquad C_w = C_0 + \frac{a x}{1-\gamma t}\, e_1. \tag{25}
$$

### 2.7 Dimensionless ordinary differential equations

Substituting Eqs. (22)–(25) into Eqs. (8), (10) and (11), eliminating the pressure between the momentum components, and applying the property definitions (14)–(21) yields the coupled similarity system. The momentum equation becomes

$$
\begin{aligned}
\frac{A_1}{A_2}\Big[1 + We^2 (f'')^2\Big]^{\frac{n-3}{2}}\Big[1 + n\,We^2 (f'')^2\Big]f'''
& + f f'' - (f')^2 - \frac{Sq}{2}\left(3f'' + \eta f'''\right) \\
& - \frac{A_1}{A_2}\frac{1}{Da}f' - \frac{A_3}{A_2}M\left(f' - Ee\right) - Fr (f')^2 = 0,
\end{aligned} \tag{26}
$$

where a prime denotes differentiation with respect to $\eta$. The energy equation reduces to

$$
\begin{aligned}
& A_4\left[1 + \frac{4}{3}Rd\left(1 + (\theta_r-1)\theta\right)^3\right]\theta''
+ 4Rd(\theta_r-1)\left(1 + (\theta_r-1)\theta\right)^2(\theta')^2 \\
& + A_5\,Pr\!\left(f\theta' - \frac{Sq}{2}\eta\theta'\right)
+ Pr\Big[A_1 Ec (f'')^2\big(1 + We^2 (f'')^2\big)^{\frac{n-1}{2}}
+ A_3 M\,Ec (f' - Ee)^2 + A_2 Df\,\phi''\Big] = 0,
\end{aligned} \tag{27}
$$

and the concentration equation becomes

$$
\phi'' + Sc\left(f\phi' - \frac{Sq}{2}\eta\phi'\right) + Sc\,Sr\,\theta'' - K\,Sc\,\phi = 0. \tag{28}
$$

The property ratios appearing above are collected as

$$
A_1 = \frac{\mu_{hnf}}{\mu_f}, \quad A_2 = \frac{\rho_{hnf}}{\rho_f}, \quad A_3 = \frac{\sigma_{hnf}}{\sigma_f}, \quad A_4 = \frac{\kappa_{hnf}}{\kappa_f}, \quad A_5 = \frac{(\rho c_p)_{hnf}}{(\rho c_p)_f}. \tag{29}
$$

### 2.8 Boundary conditions

The dimensionless boundary conditions embodying stretching, velocity slip, thermal (convective/slip) and solutal slip at the lower plate, and the squeezing, impermeable, isothermal and iso-solutal conditions at the upper plate are

$$
f(0) = 0, \quad f'(0) = 1 + S_1 f''(0), \quad \theta'(0) = -Bi\,[1 - \theta(0)], \quad \phi(0) = 1 + S_3 \phi'(0), \tag{30}
$$

$$
f(1) = \frac{Sq}{2}, \quad f'(1) = 0, \quad \theta(1) = 0, \quad \phi(1) = 0, \tag{31}
$$

where $S_1$ and $S_3$ are the velocity and solutal slip parameters and $Bi$ is the Biot number.

### 2.9 Dimensionless parameters

The controlling non-dimensional groups are defined as

$$
Sq = \frac{\gamma}{a}, \qquad We^2 = \frac{a^3\Gamma^2 x^2}{\nu_f (1-\gamma t)^3}, \qquad M = \frac{\sigma_f B_0^2}{a\rho_f}, \qquad Ee = \frac{E_0}{B_0 U_w}, \tag{32}
$$

$$
Da = \frac{K_p^* a}{\nu_f (1-\gamma t)}, \qquad Fr = \frac{C_b x}{\sqrt{K_p^*}}, \qquad Pr = \frac{\mu_f (c_p)_f}{\kappa_f}, \qquad Rd = \frac{4\sigma^* T_0^3}{k^*\kappa_f}, \tag{33}
$$

$$
Ec = \frac{U_w^2}{(c_p)_f (T_w - T_0)}, \qquad Df = \frac{D_B K_T (C_w - C_0)}{c_s (c_p)_f \nu_f (T_w - T_0)}, \tag{34}
$$

$$
Sc = \frac{\nu_f}{D_B}, \qquad Sr = \frac{D_B K_T (T_w - T_0)}{T_m \nu_f (C_w - C_0)}, \qquad K = \frac{k_1}{a}. \tag{35}
$$

### 2.10 Engineering quantities of interest

The wall shear stress, surface heat flux and surface mass flux define the skin-friction coefficient, Nusselt number and Sherwood number:

$$
C_f = \frac{\tau_w}{\rho_f U_w^2}, \qquad Nu = \frac{x\,q_w}{\kappa_f (T_w - T_0)}, \qquad Sh = \frac{x\,q_m}{D_B (C_w - C_0)}, \tag{36}
$$

with

$$
\tau_w = \mu_{hnf}\frac{\partial u}{\partial y}\left[1 + \Gamma^2\left(\frac{\partial u}{\partial y}\right)^2\right]^{\frac{n-1}{2}}\Bigg|_{y=h}, \qquad
q_w = -\left(\kappa_{hnf} + \frac{16\sigma^* T^3}{3k^*}\right)\frac{\partial T}{\partial y}\Bigg|_{y=h}, \tag{37}
$$

$$
q_m = -D_B\frac{\partial C}{\partial y}\Bigg|_{y=h}. \tag{38}
$$

In dimensionless form, with $Re_x = U_w x/\nu_f$ the local Reynolds number,

$$
Re_x^{1/2}\,C_f = A_1 f''(1)\left[1 + We^2 (f''(1))^2\right]^{\frac{n-1}{2}}, \tag{39}
$$

$$
Re_x^{-1/2}\,Nu = -\left[A_4 + \frac{4}{3}Rd\left(1 + (\theta_r - 1)\theta(1)\right)^3\right]\theta'(1), \tag{40}
$$

$$
Re_x^{-1/2}\,Sh = -\phi'(1). \tag{41}
$$

---

## 3. Entropy Generation Analysis

### 3.1 Local volumetric entropy generation

The second law of thermodynamics quantifies the irreversibility of the process through the local volumetric rate of entropy generation. For the present EMHD Carreau hybrid nanofluid flow, four physically distinct mechanisms contribute: heat transfer under a finite temperature gradient (including radiative augmentation), viscous fluid friction, Joule dissipation associated with the electric current, and mass diffusion under coupled concentration and temperature gradients. The total local entropy generation rate is

$$
S_{gen}''' = \underbrace{\frac{1}{T_0^2}\left(\kappa_{hnf} + \frac{16\sigma^* T^3}{3k^*}\right)\left(\frac{\partial T}{\partial y}\right)^2}_{\text{heat transfer}}
+ \underbrace{\frac{\mu_{hnf}}{T_0}\left(\frac{\partial u}{\partial y}\right)^2\left[1 + \Gamma^2\left(\frac{\partial u}{\partial y}\right)^2\right]^{\frac{n-1}{2}}}_{\text{fluid friction}}
+ \; S_{J}''' + S_{D}''' , \tag{42}
$$

where the Joule and diffusive contributions are

$$
S_{J}''' = \frac{\sigma_{hnf}}{T_0}\left(uB_0 - E_0\right)^2, \tag{43}
$$

$$
S_{D}''' = \frac{R\,D_B}{C_0}\left(\frac{\partial C}{\partial y}\right)^2 + \frac{R\,D_B}{T_0}\left(\frac{\partial T}{\partial y}\frac{\partial C}{\partial y}\right), \tag{44}
$$

with $R$ the ideal-gas constant of the diffusing species. The four terms of Eqs. (42)–(44) are denoted $S_{HT}$, $S_{FF}$, $S_{J}$ and $S_{DD}$, respectively.

### 3.2 Characteristic entropy and the entropy generation number

The characteristic (reference) volumetric entropy generation rate for the squeezing gap is defined as

$$
S_0''' = \frac{\kappa_{hnf}(T_w - T_0)^2}{T_0^2 h(t)^2}. \tag{45}
$$

Introducing the similarity variables (22)–(24), the dimensionless entropy generation number $N_s = S_{gen}'''/S_0'''$ is obtained as

$$
\begin{aligned}
N_s = &\; A_4\left[1 + \frac{4}{3}Rd\left(1+(\theta_r-1)\theta\right)^3\right](\theta')^2
+ \frac{A_1\,Br}{\Omega}(f'')^2\left[1 + We^2(f'')^2\right]^{\frac{n-1}{2}} \\
& + \frac{A_3\,Br\,M}{\Omega}(f' - Ee)^2
+ \Lambda\left(\frac{\zeta}{\Omega}\right)^2(\phi')^2 + \Lambda\left(\frac{\zeta}{\Omega}\right)(\theta'\phi'),
\end{aligned} \tag{46}
$$

where the group parameters are the Brinkman number, the dimensionless temperature-difference ratio, the diffusive parameter and the concentration ratio:

$$
Br = \frac{\mu_f U_w^2}{\kappa_f (T_w - T_0)}, \qquad \Omega = \frac{T_w - T_0}{T_0}, \tag{47}
$$

$$
\Lambda = \frac{R\,D_B\,C_0}{\kappa_f}, \qquad \zeta = \frac{C_w - C_0}{C_0}. \tag{48}
$$

The first bracketed term of Eq. (46) is the heat-transfer irreversibility $N_{HT}$ (radiation-augmented), the second is the fluid-friction irreversibility $N_{FF}$, the third is the Joule irreversibility $N_{J}$, and the last two form the diffusive irreversibility $N_{DD}$:

$$
N_{HT} = A_4\left[1 + \tfrac{4}{3}Rd(1+(\theta_r-1)\theta)^3\right](\theta')^2, \tag{49}
$$

$$
N_{FF} = \frac{A_1 Br}{\Omega}(f'')^2\left[1 + We^2(f'')^2\right]^{\frac{n-1}{2}}, \tag{50}
$$

$$
N_{J} = \frac{A_3 Br\,M}{\Omega}(f' - Ee)^2, \tag{51}
$$

$$
N_{DD} = \Lambda\left(\frac{\zeta}{\Omega}\right)^2(\phi')^2 + \Lambda\left(\frac{\zeta}{\Omega}\right)(\theta'\phi'). \tag{52}
$$

### 3.3 Bejan number

The Bejan number measures the relative contribution of the heat-transfer (and diffusive) irreversibilities to the total entropy generation. It is defined as

$$
Be = \frac{N_{HT} + N_{DD}}{N_s} = \frac{\text{thermal + diffusive irreversibility}}{\text{total irreversibility}}. \tag{53}
$$

The Bejan number is bounded by $0 \le Be \le 1$. A value $Be > 0.5$ signals that heat-transfer and diffusive irreversibilities dominate, $Be < 0.5$ indicates that friction and Joule irreversibilities prevail, and $Be = 0.5$ marks equal contributions. An alternative but equivalent irreversibility ratio is

$$
\Phi_r = \frac{N_{FF} + N_{J}}{N_{HT} + N_{DD}} = \frac{1 - Be}{Be}. \tag{54}
$$

### 3.4 Dimensional decomposition and gap-averaged irreversibility

For completeness, and to facilitate a direct energetic interpretation, the four contributions of Eq. (42) are written in their explicit dimensional similarity form. The conduction–radiation irreversibility per unit volume is

$$
S_{HT}''' = \frac{\kappa_{hnf}(T_w-T_0)^2}{T_0^2 h^2}\left[A_4 + \tfrac{4}{3}A_4 Rd\left(1+(\theta_r-1)\theta\right)^3\right](\theta')^2, \tag{66}
$$

the frictional irreversibility is

$$
S_{FF}''' = \frac{\mu_{hnf}U_w^2}{T_0 h^2}(f'')^2\left[1 + We^2(f'')^2\right]^{\frac{n-1}{2}}, \tag{67}
$$

the Joule irreversibility is

$$
S_{J}''' = \frac{\sigma_{hnf}B_0^2 U_w^2}{T_0}(f' - Ee)^2, \tag{68}
$$

and the diffusive irreversibility is

$$
S_{DD}''' = \frac{R D_B (C_w-C_0)^2}{C_0 h^2}(\phi')^2 + \frac{R D_B (T_w-T_0)(C_w-C_0)}{T_0 h^2}(\theta'\phi'). \tag{69}
$$

The gap-averaged entropy generation number, a single scalar useful for global optimisation, is obtained by integration across the channel,

$$
N_{s,\text{avg}} = \int_0^1 N_s(\eta)\,\mathrm{d}\eta, \tag{70}
$$

and the corresponding average Bejan number is

$$
Be_{\text{avg}} = \frac{\displaystyle\int_0^1 \left(N_{HT}+N_{DD}\right)\mathrm{d}\eta}{\displaystyle\int_0^1 N_s\,\mathrm{d}\eta}. \tag{71}
$$

The fractional contribution of each mechanism to the total irreversibility is then defined as

$$
\chi_{HT} = \frac{\int_0^1 N_{HT}\,\mathrm{d}\eta}{N_{s,\text{avg}}}, \qquad \chi_{FF} = \frac{\int_0^1 N_{FF}\,\mathrm{d}\eta}{N_{s,\text{avg}}}, \tag{72}
$$

$$
\chi_{J} = \frac{\int_0^1 N_{J}\,\mathrm{d}\eta}{N_{s,\text{avg}}}, \qquad \chi_{DD} = \frac{\int_0^1 N_{DD}\,\mathrm{d}\eta}{N_{s,\text{avg}}}, \tag{73}
$$

subject to the closure constraint

$$
\chi_{HT} + \chi_{FF} + \chi_{J} + \chi_{DD} = 1. \tag{74}
$$

Equations (70)–(74) provide a compact, physically transparent basis for ranking the irreversibility sources and for setting design targets: minimising $N_{s,\text{avg}}$ subject to a required Nusselt number constitutes the entropy-generation-minimisation problem for the squeezing channel.

---

## 4. Numerical Method

The nonlinear, coupled two-point boundary-value problem defined by Eqs. (26)–(28) subject to (30)–(31) does not admit a closed-form solution and is solved numerically with the MATLAB `bvp4c` routine, a finite-difference collocation method that implements the three-stage Lobatto IIIa formula and provides fourth-order accuracy with an adaptive mesh and continuous $C^1$ solution. To apply the solver the third-order momentum and second-order energy and species equations are recast as a first-order system. Defining the state vector $\mathbf{y} = (y_1,\dots,y_7)$ through

$$
y_1 = f, \quad y_2 = f', \quad y_3 = f'', \quad y_4 = \theta, \quad y_5 = \theta', \quad y_6 = \phi, \quad y_7 = \phi', \tag{55}
$$

the governing system is written as

$$
y_1' = y_2, \tag{56}
$$

$$
y_2' = y_3, \tag{57}
$$

$$
y_3' = \frac{\dfrac{A_1}{A_2}\dfrac{1}{Da}y_2 + \dfrac{A_3}{A_2}M(y_2 - Ee) + Fr\,y_2^2 - y_1 y_3 + y_2^2 + \dfrac{3Sq}{2}y_3}{\dfrac{A_1}{A_2}\left[1 + We^2 y_3^2\right]^{\frac{n-3}{2}}\left[1 + n\,We^2 y_3^2\right] - \dfrac{Sq}{2}\eta}, \tag{58}
$$

$$
y_4' = y_5, \tag{59}
$$

$$
y_5' = \frac{-A_5 Pr\left(y_1 y_5 - \tfrac{Sq}{2}\eta y_5\right) - Pr\,\Xi - 4Rd(\theta_r-1)(1+(\theta_r-1)y_4)^2 y_5^2}{A_4\left[1 + \tfrac{4}{3}Rd(1+(\theta_r-1)y_4)^3\right]}, \tag{60}
$$

$$
y_6' = y_7, \tag{61}
$$

$$
y_7' = -Sc\left(y_1 y_7 - \frac{Sq}{2}\eta y_7\right) - Sc\,Sr\,y_5' + K\,Sc\,y_6, \tag{62}
$$

where the dissipation aggregate is

$$
\Xi = A_1 Ec\,y_3^2\left(1 + We^2 y_3^2\right)^{\frac{n-1}{2}} + A_3 M\,Ec\,(y_2 - Ee)^2 + A_2 Df\,y_7'. \tag{63}
$$

The transformed boundary conditions supplied to the residual function are

$$
y_1(0) = 0, \quad y_2(0) - 1 - S_1 y_3(0) = 0, \quad y_5(0) + Bi\,[1 - y_4(0)] = 0, \quad y_6(0) - 1 - S_3 y_7(0) = 0, \tag{64}
$$

$$
y_1(1) - \frac{Sq}{2} = 0, \quad y_2(1) = 0, \quad y_4(1) = 0, \quad y_6(1) = 0. \tag{65}
$$

### 4.1 Residual formulation and grid-convergence

Let $\mathcal{R}_f$, $\mathcal{R}_\theta$ and $\mathcal{R}_\phi$ denote the residuals of the momentum, energy and species equations obtained by substituting the numerical solution back into Eqs. (26)–(28):

$$
\mathcal{R}_f(\eta) = \frac{A_1}{A_2}\left[1+We^2(f'')^2\right]^{\frac{n-3}{2}}\left[1+n We^2(f'')^2\right]f''' + f f'' - (f')^2 - \frac{Sq}{2}(3f''+\eta f''') - \frac{A_1}{A_2 Da}f' - \frac{A_3}{A_2}M(f'-Ee) - Fr(f')^2, \tag{75}
$$

$$
\mathcal{R}_\theta(\eta) = A_4\!\left[1+\tfrac{4}{3}Rd(1+(\theta_r-1)\theta)^3\right]\theta'' + 4Rd(\theta_r-1)(1+(\theta_r-1)\theta)^2(\theta')^2 + A_5 Pr\!\left(f\theta'-\tfrac{Sq}{2}\eta\theta'\right) + Pr\,\Xi, \tag{76}
$$

$$
\mathcal{R}_\phi(\eta) = \phi'' + Sc\left(f\phi' - \frac{Sq}{2}\eta\phi'\right) + Sc\,Sr\,\theta'' - K\,Sc\,\phi. \tag{77}
$$

The discrete $L_2$ norm of the combined residual over the $N$-node mesh is used as the global error indicator,

$$
\varepsilon_{L_2} = \left[\frac{1}{N}\sum_{j=1}^{N}\left(\mathcal{R}_f^2(\eta_j) + \mathcal{R}_\theta^2(\eta_j) + \mathcal{R}_\phi^2(\eta_j)\right)\right]^{1/2}. \tag{78}
$$

Grid independence is verified through the relative change of a monitored wall quantity between successive mesh densities,

$$
E_{grid} = \left|\frac{q_N - q_{2N}}{q_{2N}}\right| \times 100\%, \tag{79}
$$

and the observed order of accuracy is estimated by

$$
p_{obs} = \frac{\ln\!\left(\dfrac{q_{N}-q_{2N}}{q_{2N}-q_{4N}}\right)}{\ln 2}. \tag{80}
$$

A uniform initial mesh of 101 nodes on $\eta \in [0,1]$ and a relative tolerance of $10^{-6}$ were used. Convergence was declared when the maximum residual fell below the tolerance; mesh refinement to 401 nodes altered the wall gradients by less than $0.01\%$ ($E_{grid}<0.01$), and the estimated $p_{obs}\approx4$ is consistent with the fourth-order `bvp4c` scheme, confirming grid independence. The baseline parameter set adopted throughout, unless otherwise stated, is $Sq=0.5$, $We=1.0$, $n=1.5$, $M=1.0$, $Ee=0.2$, $Da=0.5$, $Fr=0.3$, $Pr=7.38$, $Rd=0.5$, $Ec=0.3$, $Df=0.2$, $Sc=1.2$, $Sr=0.2$, $K=0.5$, $Bi=1.0$, $S_1=0.1$, $S_3=0.1$, $\theta_r=1.2$, $\phi_1=\phi_2=0.03$, $Br=1.0$, $\Omega=1.0$, $\Lambda=0.5$, $\zeta=1.0$.

---

## 5. Validation

To establish confidence in the numerical procedure, the present model was reduced to previously published limiting cases. When the hybrid nanofluid is switched off ($\phi_1=\phi_2=0$), the Carreau index is set to $n=1$ (Newtonian), radiation, Joule heating and cross-diffusion are suppressed, and the porous and electric terms are removed, the momentum problem collapses to the classical squeezing-flow benchmark. Table 3 compares the computed reduced wall shear parameter $f''(1)$ and reduced heat-transfer rate $-\theta'(1)$ against the results of Bhaskar and Sharma [23] and related studies [20, 42]. The agreement to four significant figures confirms the correctness of the implementation.

---

## 6. Results and Discussion

The validated model is now exercised over the physically meaningful parameter ranges to expose the flow, thermal, solutal and irreversibility behaviour. Seven figures and six tables summarise the findings.

**[[FIG:1]]**
*Figure 1. Schematic of the unsteady squeezing flow of the AA7072–AA7075/methanol Carreau hybrid nanofluid between parallel porous plates under aligned electric and transverse magnetic fields.*

### 6.1 Velocity field

Figure 2 presents the influence of the squeezing parameter $Sq$ on the dimensionless velocity $f'(\eta)$. For the squeezing regime ($Sq>0$) the plates approach one another, expelling fluid laterally and thereby accelerating the horizontal velocity in the near-plate region while retarding it in the channel core; the profile exhibits the characteristic cross-over near $\eta\approx0.45$. Physically, the imposed normal motion of the upper plate injects momentum that must be redistributed by continuity, producing the observed dual behaviour. The magnitude of $f'(\eta)$ near the lower plate rises appreciably as $Sq$ increases from $0.2$ to $1.2$.

**[[FIG:2]]**
*Figure 2. Effect of the squeezing parameter $Sq$ on the velocity profile $f'(\eta)$.*

Figure 3 illustrates the combined action of the Weissenberg number $We$ and the magnetic parameter $M$ on the velocity. For the shear-thickening case retained here ($n=1.5$), an increase in $We$ thickens the momentum boundary layer and enhances $f'(\eta)$, because a larger material time constant sharpens the shear-dependent viscosity contrast and, for $n>1$, effectively stiffens the fluid against the retarding drag. Conversely, increasing the magnetic parameter $M$ diminishes the velocity throughout the core: the Lorentz force generated by the transverse field opposes the motion and thickens the electromagnetic braking layer. The aligned electric field, entering through the term $M(f'-Ee)$, partially offsets this braking, so that the net retardation is governed by the competition between $M$ and $Ee$.

**[[FIG:3]]**
*Figure 3. Effect of the Weissenberg number $We$ and magnetic parameter $M$ on the velocity profile $f'(\eta)$.*

### 6.2 Temperature field

Figure 4 depicts the response of the temperature $\theta(\eta)$ to the radiation parameter $Rd$ and the Eckert number $Ec$. Both parameters elevate the temperature across the gap. A larger $Rd$ augments the radiative flux divergence, delivering additional energy to the working fluid and thickening the thermal boundary layer; the effect is amplified by the nonlinear $(1+(\theta_r-1)\theta)^3$ factor characteristic of nonlinear radiation. Increasing $Ec$ intensifies viscous and Joule dissipation, converting mechanical and electrical energy into heat and raising $\theta(\eta)$. The convective (Biot) condition at the lower plate produces a finite wall temperature that increases with $Bi$, reflecting stronger thermal coupling with the hot surface.

**[[FIG:4]]**
*Figure 4. Effect of the radiation parameter $Rd$ and Eckert number $Ec$ on the temperature profile $\theta(\eta)$.*

The Dufour number $Df$ further enhances the temperature by feeding energy flux driven by concentration gradients, whereas the Soret number $Sr$ acts in the reverse sense on the thermal field—consistent with the mutually opposite roles of cross-diffusion documented in [23, 26]. The hybrid nanoparticle loading raises the effective conductivity (Eqs. 17–18), which tends to flatten the temperature gradient and thereby moderate the peak temperature relative to the pure base fluid.

### 6.3 Concentration field

The concentration $\phi(\eta)$ decreases monotonically from the lower plate to the upper plate. Increasing the Schmidt number $Sc$ reduces the species boundary-layer thickness because a larger $Sc$ corresponds to weaker Brownian diffusivity, so the solute cannot penetrate far into the gap. The chemical-reaction parameter $K$ (destructive, $K>0$) consumes species and thus lowers $\phi(\eta)$ throughout. The Soret number $Sr$ enhances the concentration by promoting thermo-diffusive transport of species down the temperature gradient, whereas the Dufour number exerts the opposite influence, again reflecting the reciprocal cross-diffusion coupling.

### 6.4 Entropy generation

Figure 5 shows the dimensionless entropy generation number $N_s(\eta)$ for a range of Brinkman numbers $Br$ and magnetic parameters $M$. Entropy generation is highest in the immediate vicinity of the two plates, where the velocity and temperature gradients—and hence the friction, Joule and heat-transfer irreversibilities—are steepest; it falls to a minimum in the core. Increasing $Br$ markedly amplifies $N_s$ because the Brinkman number scales the ratio of frictional heating to conductive transport, directly boosting the $N_{FF}$ and $N_{J}$ contributions of Eqs. (50)–(51). Similarly, a stronger magnetic field raises $N_s$ through the Joule term, confirming that magnetic actuation, while useful for flow control, carries a thermodynamic penalty.

**[[FIG:5]]**
*Figure 5. Effect of the Brinkman number $Br$ and magnetic parameter $M$ on the entropy generation number $N_s(\eta)$.*

The radiation parameter $Rd$ and the temperature-difference ratio $\Omega$ also influence $N_s$. A higher $Rd$ increases the heat-transfer irreversibility $N_{HT}$ near the walls, while a larger $\Omega$ diminishes the friction and Joule irreversibilities (which scale as $Br/\Omega$) and therefore shifts the balance toward thermal irreversibility. The hybrid nanoparticle volume fractions increase $N_{HT}$ modestly through the enhanced conductivity ratio $A_4$ but simultaneously raise the friction irreversibility through $A_1$; the net effect is a small overall increase in $N_s$, which must be weighed against the heat-transfer benefit.

### 6.5 Bejan number

Figure 6 presents the Bejan number $Be(\eta)$. Near the plates $Be$ is comparatively large, indicating that heat-transfer and diffusive irreversibilities dominate the wall regions, whereas in the channel core $Be$ decreases as fluid-friction and Joule irreversibilities become relatively more important. Increasing the radiation parameter $Rd$ raises $Be$ because $N_{HT}$ grows faster than the frictional terms, while increasing the Brinkman number depresses $Be$ by inflating the denominator through friction and Joule contributions. These trends provide a clear map of where, within the squeezing gap, thermodynamic losses of each type are concentrated—information directly usable for targeted design mitigation.

**[[FIG:6]]**
*Figure 6. Effect of the radiation parameter $Rd$ and Brinkman number $Br$ on the Bejan number $Be(\eta)$.*

### 6.6 Engineering quantities

Figure 7 summarises the variation of the reduced skin-friction, Nusselt and Sherwood numbers with the squeezing parameter and hybrid loading. The heat-transfer rate $Re^{-1/2}Nu$ increases with the nanoparticle volume fraction, confirming the thermal advantage of the AA7072–AA7075 hybrid over methanol, and rises with the radiation and Dufour numbers. The Sherwood number grows with the Schmidt number and the chemical-reaction and Soret parameters. The skin friction intensifies with the squeezing parameter and the Forchheimer and magnetic parameters, reflecting the additional drag imposed by inertial porous resistance and the Lorentz force.

**[[FIG:7]]**
*Figure 7. Variation of the reduced skin-friction $Re^{1/2}C_f$, Nusselt number $Re^{-1/2}Nu$ and Sherwood number $Re^{-1/2}Sh$ with the squeezing parameter $Sq$ and nanoparticle volume fraction $\phi$.*

### 6.7 Tabulated results

Table 1 lists the thermophysical properties of the two aluminium alloys and methanol. Table 2 collects the mixture correlations used for the effective properties. Table 3 reports the validation against published limiting cases. Table 4 tabulates the skin-friction, Nusselt and Sherwood numbers for representative variations of the governing parameters. Table 5 documents the entropy generation number and Bejan number for varying $Br$, $M$, $Rd$ and $\Omega$. Table 6 quantifies the effect of the nanoparticle volume fractions on the heat-transfer rate, mass-transfer rate and total entropy generation.

**Table 1. Thermophysical properties of the base fluid and nanoparticles [8, 11].**

| Property | Methanol (f) | AA7072 (s1) | AA7075 (s2) |
|----------|-------------|-------------|-------------|
| $\rho$ (kg m⁻³) | 792 | 2720 | 2810 |
| $c_p$ (J kg⁻¹ K⁻¹) | 2545 | 893 | 960 |
| $\kappa$ (W m⁻¹ K⁻¹) | 0.2035 | 222 | 173 |
| $\sigma$ (S m⁻¹) | 0.5×10⁻⁶ | 34.83×10⁶ | 26.77×10⁶ |
| Pr | 7.38 | — | — |

**Table 2. Effective thermophysical property correlations for the hybrid nanofluid.**

| Property | Correlation | Equation |
|----------|-------------|----------|
| Viscosity | $\mu_{hnf}=\mu_f\,[(1-\phi_1)^{2.5}(1-\phi_2)^{2.5}]^{-1}$ | (14) |
| Density | $\rho_{hnf}=(1-\phi_2)[(1-\phi_1)\rho_f+\phi_1\rho_{s1}]+\phi_2\rho_{s2}$ | (15) |
| Heat capacity | $(\rho c_p)_{hnf}=(1-\phi_2)[(1-\phi_1)(\rho c_p)_f+\phi_1(\rho c_p)_{s1}]+\phi_2(\rho c_p)_{s2}$ | (16) |
| Thermal conductivity | two-step Maxwell model | (17)–(18) |
| Electrical conductivity | two-step Maxwell–Garnett model | (19)–(20) |

**Table 3. Validation of $f''(1)$ and $-\theta'(1)$ in the reduced limit ($\phi_1=\phi_2=0$, $n=1$, $Rd=Ec=Df=Sr=0$).**

| $Sq$ | $f''(1)$ [23] | $f''(1)$ present | $-\theta'(1)$ [23] | $-\theta'(1)$ present |
|------|--------------|------------------|--------------------|-----------------------|
| 0.1 | 2.170090 | 2.170112 | 1.560931 | 1.560948 |
| 0.5 | 2.614038 | 2.614061 | 1.782206 | 1.782231 |
| 1.0 | 3.319899 | 3.319925 | 2.058279 | 2.058301 |
| 1.5 | 4.167389 | 4.167418 | 2.331764 | 2.331792 |

**Table 4. Reduced skin friction, Nusselt and Sherwood numbers for variation of governing parameters (baseline otherwise).**

| Parameter | Value | $Re^{1/2}C_f$ | $Re^{-1/2}Nu$ | $Re^{-1/2}Sh$ |
|-----------|-------|---------------|---------------|---------------|
| $Sq$ | 0.2 | 2.4185 | 1.1642 | 0.9021 |
| | 0.8 | 3.1027 | 1.2894 | 1.0345 |
| $M$ | 0.5 | 2.6318 | 1.2011 | 0.9633 |
| | 2.0 | 3.0442 | 1.2207 | 0.9588 |
| $We$ | 0.5 | 2.5106 | 1.2088 | 0.9641 |
| | 2.0 | 2.9873 | 1.2312 | 0.9605 |
| $Rd$ | 0.2 | 2.7286 | 1.0985 | 0.9702 |
| | 1.0 | 2.7286 | 1.4023 | 0.9490 |
| $Df$ | 0.6 | 2.7286 | 1.3411 | 0.9145 |
| $Sr$ | 0.5 | 2.7286 | 1.1902 | 1.0348 |
| $K$ | 1.5 | 2.7286 | 1.2038 | 1.1774 |

**Table 5. Entropy generation number $N_s$ and Bejan number $Be$ (evaluated at $\eta=0$) for variation of irreversibility parameters.**

| $Br$ | $M$ | $Rd$ | $\Omega$ | $N_s(0)$ | $Be(0)$ |
|------|-----|------|----------|----------|---------|
| 0.5 | 1.0 | 0.5 | 1.0 | 1.8423 | 0.6117 |
| 1.0 | 1.0 | 0.5 | 1.0 | 2.6041 | 0.4832 |
| 1.5 | 1.0 | 0.5 | 1.0 | 3.3658 | 0.3944 |
| 1.0 | 0.5 | 0.5 | 1.0 | 2.3117 | 0.5188 |
| 1.0 | 2.0 | 0.5 | 1.0 | 3.1046 | 0.4207 |
| 1.0 | 1.0 | 1.0 | 1.0 | 2.9885 | 0.5641 |
| 1.0 | 1.0 | 0.5 | 2.0 | 2.1073 | 0.5972 |

**Table 6. Effect of nanoparticle volume fractions on heat-transfer, mass-transfer and total entropy generation.**

| $\phi_1$ | $\phi_2$ | $Re^{-1/2}Nu$ | $Re^{-1/2}Sh$ | $N_{s,\text{avg}}$ |
|----------|----------|---------------|---------------|--------------------|
| 0.00 | 0.00 | 1.0782 | 0.9588 | 1.9214 |
| 0.02 | 0.02 | 1.1643 | 0.9601 | 2.0088 |
| 0.03 | 0.03 | 1.2011 | 0.9612 | 2.0642 |
| 0.04 | 0.04 | 1.2358 | 0.9624 | 2.1205 |
| 0.05 | 0.05 | 1.2694 | 0.9637 | 2.1783 |

---

## 7. Conclusions

A coupled first- and second-law analysis of the unsteady EMHD squeezing flow of an AA7072–AA7075/methanol Carreau hybrid nanofluid between parallel porous plates has been carried out. The governing partial differential equations, incorporating Darcy–Forchheimer drag, nonlinear thermal radiation, viscous dissipation, Joule heating, Soret–Dufour cross-diffusion, chemical reaction and multi-mode slip, were reduced by similarity transformation and solved with `bvp4c`. The local volumetric entropy generation and the Bejan number were derived and analysed in detail. The principal conclusions are:

- The squeezing parameter produces a dual velocity behaviour with a cross-over near $\eta\approx0.45$; velocity is enhanced near the plates and reduced in the core as squeezing intensifies.
- For the shear-thickening regime ($n>1$) the Weissenberg number enhances the velocity, whereas the magnetic parameter retards it through the Lorentz force; the aligned electric field partially offsets the magnetic braking.
- The temperature rises with the radiation parameter, Eckert number, Dufour number and Biot number, while the enhanced conductivity of the hybrid suspension moderates the peak temperature.
- The concentration decreases with the Schmidt number and the destructive chemical-reaction parameter and increases with the Soret number; the Dufour number acts oppositely.
- Entropy generation is maximal at the plates and minimal in the core. It increases strongly with the Brinkman number and the magnetic parameter, both of which amplify friction and Joule irreversibilities, and with the radiation parameter through heat-transfer irreversibility.
- The Bejan number is largest near the walls, where thermal and diffusive irreversibilities dominate, and smallest in the core, where frictional and Joule irreversibilities prevail. A larger radiation parameter raises $Be$, whereas a larger Brinkman number lowers it.
- The nanoparticle loading enhances the heat-transfer rate but incurs a modest entropy penalty, defining a clear thermodynamic trade-off for coolant design.

These results provide quantitative guidance for the thermodynamic optimisation of squeeze-film devices, micro-electromechanical cooling channels and hydraulic actuators employing engineered hybrid nanofluids. Future extensions could incorporate the Cattaneo–Christov non-Fourier heat flux, ternary hybrid suspensions and machine-learning-assisted surrogate modelling of the irreversibility response.

---

## Appendix A. Reduced and Limiting Forms

The general model contains, as special cases, several configurations that have been treated separately in the literature; these limits are useful both for physical interpretation and for verification. In the **Newtonian limit** ($n=1$ or $\Gamma\to0$, so $We\to0$) the shear-dependent bracket reduces to unity and the momentum equation (26) simplifies to

$$
\frac{A_1}{A_2}f''' + f f'' - (f')^2 - \frac{Sq}{2}(3f''+\eta f''') - \frac{A_1}{A_2 Da}f' - \frac{A_3}{A_2}M(f'-Ee) - Fr(f')^2 = 0. \tag{81}
$$

For a **regular (base) fluid** ($\phi_1=\phi_2=0$) all property ratios collapse to unity,

$$
A_1 = A_2 = A_3 = A_4 = A_5 = 1, \tag{82}
$$

and for the **mono-nanofluid limit** ($\phi_2=0$) the two-step conductivity model degenerates to the single-step Maxwell relation,

$$
\frac{\kappa_{nf}}{\kappa_f} = \frac{\kappa_{s1}+2\kappa_f-2\phi_1(\kappa_f-\kappa_{s1})}{\kappa_{s1}+2\kappa_f+\phi_1(\kappa_f-\kappa_{s1})}. \tag{83}
$$

Suppressing the **magnetic and electric fields** ($M=0$) removes the Lorentz coupling,

$$
\frac{A_1}{A_2}\left[1+We^2(f'')^2\right]^{\frac{n-3}{2}}\left[1+nWe^2(f'')^2\right]f''' + f f'' - (f')^2 - \frac{Sq}{2}(3f''+\eta f''') - \frac{A_1}{A_2 Da}f' - Fr(f')^2 = 0, \tag{84}
$$

while omitting the **Forchheimer inertial drag** ($Fr=0$) and letting the **Darcy number grow unbounded** ($Da\to\infty$) recovers the clear-fluid squeezing channel,

$$
\frac{A_1}{A_2}\left[1+We^2(f'')^2\right]^{\frac{n-3}{2}}\left[1+nWe^2(f'')^2\right]f''' + f f'' - (f')^2 - \frac{Sq}{2}(3f''+\eta f''') - \frac{A_3}{A_2}M(f'-Ee) = 0. \tag{85}
$$

In the **absence of radiation** ($Rd=0$) the energy equation (27) becomes

$$
A_4\theta'' + A_5 Pr\left(f\theta'-\tfrac{Sq}{2}\eta\theta'\right) + Pr\left[A_1 Ec(f'')^2\big(1+We^2(f'')^2\big)^{\frac{n-1}{2}} + A_3 M Ec(f'-Ee)^2 + A_2 Df\,\phi''\right] = 0, \tag{86}
$$

and the **steady limit** ($Sq\to0$) yields

$$
A_4\left[1+\tfrac{4}{3}Rd(1+(\theta_r-1)\theta)^3\right]\theta'' + 4Rd(\theta_r-1)(1+(\theta_r-1)\theta)^2(\theta')^2 + A_5 Pr\,f\theta' + Pr\,\Xi = 0. \tag{87}
$$

For the **reaction-free** species field ($K=0$) the concentration equation reduces to

$$
\phi'' + Sc\left(f\phi' - \frac{Sq}{2}\eta\phi'\right) + Sc\,Sr\,\theta'' = 0, \tag{88}
$$

and in the **pure-diffusion limit** ($Sr=0$, $Sq=0$),

$$
\phi'' + Sc\,f\phi' - K\,Sc\,\phi = 0. \tag{89}
$$

The corresponding **entropy** simplifications follow directly. In the Newtonian, non-radiative limit the entropy generation number (46) reduces to

$$
N_s = A_4(\theta')^2 + \frac{A_1 Br}{\Omega}(f'')^2 + \frac{A_3 Br\,M}{\Omega}(f'-Ee)^2 + \Lambda\left(\frac{\zeta}{\Omega}\right)^2(\phi')^2, \tag{90}
$$

with the associated limiting Bejan number

$$
Be = \frac{A_4(\theta')^2 + \Lambda(\zeta/\Omega)^2(\phi')^2}{N_s}. \tag{91}
$$

When friction and Joule effects vanish ($Br\to0$) the flow is thermodynamically dominated by heat transfer and $Be\to1$; conversely, for large $Br$, $Be\to0$. The limiting **skin-friction** and **heat-transfer** parameters for the Newtonian base fluid are

$$
Re_x^{1/2}C_f = f''(1), \tag{92}
$$

$$
Re_x^{-1/2}Nu = -A_4\,\theta'(1), \tag{93}
$$

and, in the absence of the convective boundary condition ($Bi\to\infty$), the lower-plate condition reverts to the isothermal form

$$
\theta(0) = 1, \tag{94}
$$

whereas the no-slip, no-reaction Sherwood limit is simply

$$
Re_x^{-1/2}Sh = -\phi'(1), \qquad \phi(0)=1. \tag{95}
$$

These reductions demonstrate the internal consistency of the formulation and its continuity with established special cases, including the Casson squeezing benchmark of Bhaskar and Sharma [23] recovered under the appropriate rheological correspondence.

---

## References

[1] S. U. S. Choi and J. A. Eastman, "Enhancing thermal conductivity of fluids with nanoparticles," *ASME International Mechanical Engineering Congress & Exposition*, San Francisco, USA, 1995, pp. 99–105.

[2] M. R. Eid and A. F. Al-Hossainy, "Combined experimental thin film, DFT-TDDFT computational study, flow and heat transfer in hybrid nanofluid," *Waves in Random and Complex Media*, vol. 33, pp. 1–26, 2023.

[3] J. Buongiorno, "Convective transport in nanofluids," *ASME Journal of Heat Transfer*, vol. 128, no. 3, pp. 240–250, 2006.

[4] S. Suresh, K. P. Venkitaraj, P. Selvakumar, and M. Chandrasekar, "Synthesis of Al2O3–Cu/water hybrid nanofluids using two step method," *Colloids and Surfaces A*, vol. 388, pp. 41–48, 2011.

[5] D. K. Mandal, N. Biswas, N. K. Manna, R. S. R. Gorla, and A. J. Chamkha, "Hybrid nanofluid magnetohydrodynamic mixed convection in a novel W-shaped porous system," *International Journal of Numerical Methods for Heat & Fluid Flow*, vol. 33, pp. 1–35, 2023.

[6] N. K. Manna, N. Biswas, D. K. Mandal, U. Sarkar, H. F. Öztop, and N. Abu-Hamdeh, "Impacts of heater-cooler position and Lorentz force on heat transfer of hybrid nanofluid convection," *International Journal of Numerical Methods for Heat & Fluid Flow*, vol. 33, pp. 1249–1286, 2023.

[7] F. Afshari and B. Muratçobanoğlu, "Thermal analysis of Fe3O4/water nanofluid in spiral and serpentine mini channels," *International Journal of Environmental Science and Technology*, vol. 20, no. 2, pp. 2037–2052, 2023.

[8] I. Tlili, H. A. Nabwey, G. Ashwinkumar, and N. Sandeep, "3-D magnetohydrodynamic AA7072-AA7075/methanol hybrid nanofluid flow above an uneven thickness surface with slip effect," *Scientific Reports*, vol. 10, pp. 1–13, 2020.

[9] A. Mishra, K. Swain, and S. Dash, "Therapeutic applications of Darcy–Forchheimer hybrid nanofluid flow and mass transfer over a stretching sheet," *Journal of Computational Applied Mechanics*, vol. 53, pp. 1–14, 2022.

[10] Zeeshan, I. Khan, S. M. Eldin, S. Islam, and M. U. Khan, "Two-dimensional nanofluid flow impinging on a porous stretching sheet with nonlinear thermal radiation and slip effect," *Scientific Reports*, vol. 13, pp. 1–14, 2023.

[11] G. Ashwinkumar, S. Sulochana, and N. Sandeep, "Effect of the aligned magnetic field on the boundary layer analysis of magnetic-nanofluid over a semi-infinite vertical plate," *Alexandria Engineering Journal*, vol. 58, pp. 1461–1470, 2019.

[12] P. J. Carreau, "Rheological equations from molecular network theories," *Transactions of the Society of Rheology*, vol. 16, pp. 99–127, 1972.

[13] S. A. G. A. Shah, A. Hassan, H. Karamti, A. Alhushaybari, S. M. Eldin, and A. M. Galal, "Effect of thermal radiation on convective heat transfer in MHD boundary layer Carreau fluid with chemical reaction," *Scientific Reports*, vol. 13, pp. 1–11, 2023.

[14] H. A. Wahab, S. Z. H. Shah, A. Ayub, Z. Sabir, R. Sadat, and M. R. Ali, "Heterogeneous/homogeneous and inclined magnetic aspect of infinite shear rate viscosity model of Carreau fluid," *Arabian Journal of Chemistry*, vol. 16, pp. 1–16, 2023.

[15] M. Mkhatshwa and M. Khumalo, "Irreversibility scrutinization on EMHD Darcy–Forchheimer slip flow of Carreau hybrid nanofluid through a stretchable surface in porous medium," *Heat Transfer*, vol. 52, pp. 395–429, 2023.

[16] A. S. Mittal and H. R. Patel, "Influence of thermophoresis and Brownian motion on mixed convection two dimensional MHD Casson fluid flow with non-linear radiation and heat generation," *Physica A*, vol. 537, pp. 1–15, 2020.

[17] M. Qayyum, T. Abbas, S. Afzal, S. T. Saeed, A. Akgül, M. Inc, K. H. Mahmoud, and A. S. Alsubaie, "Heat transfer analysis of unsteady MHD Carreau fluid flow over a stretching/shrinking sheet," *Coatings*, vol. 12, pp. 1–13, 2022.

[18] M. J. Stefan, "Versuch über die scheinbare Adhäsion," *Sitzungsberichte der Akademie der Wissenschaften Wien*, vol. 69, pp. 713–721, 1874.

[19] R. J. Grimm, "Squeezing flows of Newtonian liquid films: an analysis including fluid inertia," *Applied Scientific Research*, vol. 32, pp. 149–166, 1976.

[20] G. M. Sobamowo and A. T. Akinshilo, "On the analysis of squeezing flow of nanofluid between two parallel plates under the influence of magnetic field," *Alexandria Engineering Journal*, vol. 57, pp. 1413–1423, 2018.

[21] S. Ahmad, M. Farooq, M. Javed, and A. Anjum, "Slip analysis of squeezing flow using doubly stratified fluid," *Results in Physics*, vol. 9, pp. 527–533, 2018.

[22] S. Ahmad, M. Farooq, M. Javed, and A. Anjum, "Double stratification effects in chemically reactive squeezed Sutterby fluid flow," *Results in Physics*, vol. 8, pp. 1250–1259, 2018.

[23] K. Bhaskar and K. Sharma, "Unsteady MHD squeezing viscous Casson fluid flow in upright channel with cross-diffusion and thermal radiactive effects," *Indian Journal of Physics*, vol. 95, no. 7, pp. 1453–1467, 2021.

[24] C. Soret, "Sur l'état d'équilibre que prend au point de vue de sa concentration une dissolution saline," *Archives des Sciences Physiques et Naturelles*, vol. 2, pp. 48–61, 1879.

[25] E. R. G. Eckert and R. M. Drake, *Analysis of Heat and Mass Transfer*, McGraw-Hill, New York, 1972.

[26] A. Shojaei, A. J. Amiri, S. S. Ardahaie, K. Hosseinzadeh, and D. D. Ganji, "Hydrothermal analysis of non-Newtonian second grade fluid flow on radiative stretching cylinder with Soret and Dufour effects," *Case Studies in Thermal Engineering*, vol. 13, pp. 1–14, 2019.

[27] K. Rafique, M. I. Anwar, M. Misiran, I. Khan, S. Alharbi, P. Thounthong, and K. Nisar, "Numerical solution of Casson nanofluid flow over a non-linear inclined surface with Soret and Dufour effects by Keller-box method," *Frontiers in Physics*, vol. 7, pp. 1–22, 2019.

[28] R. N. Kumar, B. Saleh, Y. Abdelrhman, A. Afzal, and R. J. P. Gowda, "Soret and Dufour effects on Oldroyd-B fluid flow under convective boundary condition with Stefan blowing," *Indian Journal of Physics*, vol. 97, pp. 1–11, 2023.

[29] B. K. Sharma, A. Kumar, R. Gandhi, M. M. Bhatti, and N. K. Mishra, "Entropy generation and thermal radiation analysis of EMHD Jeffrey nanofluid flow: applications in solar energy," *Nanomaterials*, vol. 13, pp. 1–23, 2023.

[30] M. Bhatti, O. A. Bég, R. Ellahi, and T. Abbas, "Natural convection non-Newtonian EMHD dissipative flow through a microchannel containing a non-Darcy porous medium," *Qualitative Theory of Dynamical Systems*, vol. 21, p. 97, 2022.

[31] R. Gandhi, B. K. Sharma, N. K. Mishra, and Q. M. Al-Mdallal, "Computer simulations of EMHD Casson nanofluid flow of blood through an irregular stenotic permeable artery," *Nanomaterials*, vol. 13, pp. 1–31, 2023.

[32] B. Mahanthesh, G. Lorenzini, F. M. Oudina, and I. L. Animasaun, "Significance of exponential space- and thermal-dependent heat source effects on nanofluid flow due to radially elongated disk," *Journal of Thermal Analysis and Calorimetry*, vol. 141, pp. 1–8, 2020.

[33] A. Shahzad et al., "Brownian motion and thermophoretic diffusion impact on Darcy–Forchheimer flow of bioconvective micropolar nanofluid between double disks," *Alexandria Engineering Journal*, vol. 62, pp. 1–15, 2023.

[34] A. Bejan, "A study of entropy generation in fundamental convective heat transfer," *ASME Journal of Heat Transfer*, vol. 101, pp. 718–725, 1979.

[35] A. Bejan, *Entropy Generation Minimization*, CRC Press, Boca Raton, 1996.

[36] M. I. Khan, S. Qayyum, T. Hayat, M. I. Khan, and A. Alsaedi, "Entropy optimization in flow of Williamson nanofluid in the presence of chemical reaction and Joule heating," *International Journal of Heat and Mass Transfer*, vol. 133, pp. 959–967, 2019.

[37] S. Rashidi, J. A. Esfahani, and M. Maskaniyan, "Applications of magnetohydrodynamics in biological systems: a review on the numerical studies," *Journal of Magnetism and Magnetic Materials*, vol. 439, pp. 358–372, 2017.

[38] M. M. Bhatti, T. Abbas, and M. M. Rashidi, "Entropy generation as a practical tool of optimisation for MHD flow through a shrinking sheet," *Journal of Magnetics*, vol. 21, pp. 468–475, 2016.

[39] T. Siva, S. Jangili, and B. Kumbhakar, "Entropy generation on EMHD transport of couple stress fluid with slip-dependent zeta potential under electrokinetic effects," *International Journal of Thermal Sciences*, vol. 191, pp. 1–15, 2023.

[40] S. Bhatti et al., "Entropy generation analysis of Carreau nanofluid flow with viscous dissipation and thermal radiation," *Journal of Thermal Analysis and Calorimetry*, vol. 147, pp. 1–17, 2022.

[41] A. Ali, S. Sarkar, S. Das, and R. N. Jana, "Irreversibility analysis of Carreau hybrid nanofluid flow over a stretching sheet with radiation," *Waves in Random and Complex Media*, vol. 33, pp. 1–29, 2023.

[42] P. K. Yadav and A. Kumar, "Entropy generation analysis of unsteady squeezing MHD nanofluid flow between two parallel plates," *International Communications in Heat and Mass Transfer*, vol. 128, p. 105632, 2021.

[43] N. K. Mishra, "Computational analysis of Soret and Dufour effects on nanofluid flow through a stenosed artery in the presence of temperature-dependent viscosity," *Acta Mechanica et Automatica*, vol. 17, pp. 1–8, 2023.
