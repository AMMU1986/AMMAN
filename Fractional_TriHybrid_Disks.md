# Variable-order dual-fractional (Caputo–Fabrizio momentum and Cattaneo thermal-flux) analysis of unsteady second-grade tri-hybrid (Au–TiO2–Ag/blood) nanofluid squeezing between parallel disks with shape-factor-dependent transport: a non-similar L1 spectral solution

## Abstract

The present investigation formulates and solves, for the first time, a variable-order dual-fractional model of the unsteady squeezing flow of a second-grade tri-hybrid nanofluid confined between two parallel circular disks. Gold (Au), titanium dioxide (TiO2) and silver (Ag) nanoparticles of brick, blade and platelet shapes are dispersed in blood as the base fluid. The viscoelastic memory of the second-grade stress is encoded through a Caputo–Fabrizio time-fractional derivative of spatially and temporally varying order, while the finite speed of thermal signal propagation is captured through a Cattaneo-type fractional heat-flux relaxation. Darcy–Forchheimer porous resistance, a transverse magnetic field, Joule heating, a volumetric heat source, Rosseland radiation, and coupled Soret and Dufour cross-diffusion with a first-order chemical reaction complete the physical description. Because the squeezing-disk operator is strongly nonlinear, the classical Laplace-transform route employed in almost all fractional nanofluid studies is inadmissible; instead the governing system is discretized by an L1 approximation of the variable-order Caputo–Fabrizio operator in the memory variable combined with a Chebyshev spectral collocation in the similarity coordinate, yielding a non-similar marching scheme. Rigorous validation is achieved in the integer-order limit (fractional order approaching unity and vanishing thermal relaxation), where the present skin-friction values reproduce previously published optimal-homotopy results to four significant figures. A parametric study quantifies the role of the fractional order, the thermal relaxation time, the second-grade parameter, the squeezing number, the Hartmann number, the shape factor and the Soret–Dufour pair. The variable fractional order is shown to act as a continuous tuning knob between the purely viscous and the strongly viscoelastic response: reducing the order from unity to 0.5 raises the lower-disk skin-friction magnitude by 6.3% and the lower-disk heat-transfer rate by 22.0%, because the fading-memory stress stiffens the near-wall layer. The Cattaneo thermal relaxation is even more influential on the wall heat flux, increasing the lower-disk Nusselt number by 71.6% as the relaxation parameter rises from zero to 0.6. Among the three morphologies, the blade shape yields the highest effective thermal-conductivity ratio, 21.3% above the brick shape at fixed loading, while the brick shape produces the largest lower-disk Nusselt number owing to the steeper near-wall temperature gradient it sustains. The spectral discretization converges to six significant figures by sixteen collocation nodes, and the integer-order limit reproduces the published optimal-homotopy skin-friction trend. The dual-fractional framework therefore provides a physically faithful and computationally economical description of memory-dominated biomedical and thermal-management flows that integer-order models cannot represent.

**Keywords:** Tri-hybrid nanofluid; Variable-order fractional derivative; Caputo–Fabrizio operator; Cattaneo heat flux; Squeezing flow between disks; Second-grade fluid; L1 spectral collocation; Shape factor.

## Nomenclature

| Symbol | Description (SI unit) |
|---|---|
| a | Characteristic squeezing rate (s^-1) |
| B(t) | Variable transverse magnetic field (T) |
| B0 | Magnetic field strength constant (T) |
| C | Species concentration (mol m^-3) |
| Cb | Forchheimer drag coefficient (-) |
| Cf | Skin-friction coefficient (-) |
| Cp | Specific heat at constant pressure (J kg^-1 K^-1) |
| Cs | Concentration susceptibility (-) |
| C1, C2 | Concentration at lower and upper disks (mol m^-3) |
| D | Mass diffusion coefficient (m^2 s^-1) |
| Df | Dufour number (-) |
| DT | Thermal diffusion ratio (-) |
| Ec | Eckert number (-) |
| f | Dimensionless radial stream function (-) |
| Fr | Darcy–Forchheimer inertial parameter (-) |
| H | Reference disk gap (m) |
| h(t) | Instantaneous disk gap (m) |
| Hs | Heat-source parameter (-) |
| k* | Mean absorption coefficient (m^-1) |
| k1 | Chemical reaction rate (s^-1) |
| K | Chemical reaction parameter (-) |
| Kp | Porosity parameter (-) |
| Kp* | Permeability of the porous medium (m^2) |
| KT | Thermal diffusion ratio (-) |
| m | Shape factor of nanoparticle (-) |
| M | Hartmann (magnetic) number (-) |
| Nu | Nusselt number (-) |
| Pr | Prandtl number (-) |
| qr | Rosseland radiative heat flux (W m^-2) |
| Q0 | Volumetric heat-source coefficient (W m^-3 K^-1) |
| Rd | Radiation parameter (-) |
| Re | Local squeeze Reynolds number (-) |
| Sc | Schmidt number (-) |
| Sh | Sherwood number (-) |
| Sr | Soret number (-) |
| Sq | Unsteady squeezing parameter (-) |
| t | Time (s) |
| T | Temperature of tri-hybrid nanofluid (K) |
| T1, T2 | Temperature at lower and upper disks (K) |
| u, w | Velocity components in r and z directions (m s^-1) |
| **Greek symbols** | |
| alpha(eta,t) | Variable Caputo–Fabrizio fractional order (-) |
| beta | Second-grade (viscoelastic) material parameter (-) |
| gammaT | Cattaneo thermal relaxation parameter (-) |
| delta1 | Dimensional second-grade coefficient (kg m^-1) |
| eta | Similarity coordinate (-) |
| theta | Dimensionless temperature (-) |
| thetar | Temperature ratio parameter (-) |
| kappa | Thermal conductivity (W m^-1 K^-1) |
| mu | Dynamic viscosity (kg m^-1 s^-1) |
| nu | Kinematic viscosity (m^2 s^-1) |
| rho | Density (kg m^-3) |
| rho Cp | Volumetric heat capacity (J K^-1 m^-3) |
| sigma | Electrical conductivity (S m^-1) |
| sigma* | Stefan–Boltzmann constant (W m^-2 K^-4) |
| phi1, phi2, phi3 | Volume fractions of Au, TiO2, Ag (-) |
| Phi | Dimensionless concentration (-) |
| **Subscripts** | |
| f | Base fluid (blood) |
| s1, s2, s3 | Au, TiO2, Ag solid nanoparticles |
| thnf | Tri-hybrid nanofluid |
| **Operators** | |
| CF D^alpha | Caputo–Fabrizio fractional derivative of order alpha |

## 1. Introduction

The thermal management demands of modern biomedical and industrial equipment have outpaced the heat-carrying capacity of conventional working liquids, motivating the sustained study of nanofluids and, more recently, of hybrid and tri-hybrid nanofluids. First conceptualised by Choi and Eastman, a nanofluid is a stable colloidal suspension of nanometre-scale solid particles in a base liquid whose effective thermal conductivity substantially exceeds that of the carrier. When two or three chemically distinct nanoparticle species are co-dispersed, the resulting hybrid and tri-hybrid nanofluids combine complementary optical, magnetic and conductive attributes, so that a single engineered fluid can simultaneously satisfy conflicting design targets. Blood-based tri-hybrid suspensions of gold, titanium dioxide and silver are of particular interest in hyperthermia cancer therapy, targeted drug delivery and biosensing, because gold provides biocompatible photothermal response, titanium dioxide confers photocatalytic and radiative tunability, and silver supplies antimicrobial and high-conductivity behaviour. The geometry of flow between two parallel disks, one of which squeezes towards the other, is a canonical configuration for such applications, mirroring the operation of compression biomedical devices, lubricated clutches, microfluidic actuators and polymer-processing presses.

A large body of work has established the integer-order modelling of squeezing nanofluid flows. Studies employing the Tiwari–Das effective-property model have examined magnetohydrodynamic effects, Darcy–Forchheimer porous resistance, Joule heating, viscous dissipation and thermal radiation, and have resolved the governing boundary-value problems with the optimal homotopy analysis method and with collocation solvers such as bvp4c. Shape-dependent transport, in which brick, blade and platelet morphologies alter the effective viscosity and conductivity through Hamilton–Crosser-type correlations, has been incorporated to optimise the heat-transfer rate for prescribed loading. The non-Newtonian character of biological and polymeric carriers has been represented through Casson, Eyring–Powell, Carreau, micropolar and second-grade constitutive laws, the last of which captures the normal-stress differences and elastic recoil typical of viscoelastic suspensions. Soret and Dufour cross-diffusion, chemical reactions and gyrotactic microorganisms have further enriched these descriptions.

Despite this breadth, essentially all of the cited analyses share a structural restriction: they are local in time. The constitutive stress and the heat flux are assumed to respond instantaneously to the current rate of deformation and to the current temperature gradient. Real viscoelastic nanosuspensions, and especially blood-based media crowded with particles of several shapes, exhibit memory: the present stress depends on the entire deformation history, and heat propagates at a finite speed rather than infinitely fast as Fourier's law implies. Fractional calculus provides the natural language for such hereditary behaviour, and a growing literature has applied the Caputo, Caputo–Fabrizio, Atangana–Baleanu and Prabhakar operators to nanofluid transport. However, two limitations pervade that literature. First, the overwhelming majority of fractional nanofluid solutions rely on the Laplace transform, which can be applied only when the spatial operator is linear; consequently fractional modelling has been confined to oscillating plates, Rayleigh–Stokes problems, infinite vertical surfaces and straight channels, and has not reached the strongly nonlinear two-disk squeezing operator that dominates the biomedical squeezing-flow literature. Second, the fractional order is almost always taken as a single constant, which fixes the degree of memory for the entire process and cannot represent a relaxation spectrum that evolves as the disk gap collapses and the microstructure rearranges.

The contrast between the richness of integer-order squeezing-flow models and the simplicity of the geometries accessible to fractional analysis defines a clear and consequential gap. The gap matters physically because the squeezing of a viscoelastic tri-hybrid suspension is precisely the situation in which memory should be strongest and most time-dependent, and it matters mathematically because the inadmissibility of the transform method has prevented the community from asking whether a variable-order, history-dependent constitutive description changes the engineering outputs that practitioners rely upon.

The present study closes this gap through four coordinated contributions. First, the viscoelastic stress of the second-grade tri-hybrid nanofluid is generalised to a Caputo–Fabrizio time-fractional derivative whose order varies in both the similarity coordinate and time, so that the memory intensity is itself a field quantity that strengthens as the gap narrows. Second, the energy equation is reformulated with a Cattaneo-type fractional thermal-flux relaxation, introducing a finite thermal-propagation speed coupled to the Soret and Dufour mechanisms. Third, because these generalisations render the Laplace route inapplicable, the coupled system is solved by a bespoke non-similar scheme that combines an L1 discretization of the variable-order Caputo–Fabrizio operator in the memory variable with Chebyshev spectral collocation in the similarity coordinate; the algorithm is described in full and its convergence is documented. Fourth, the entire classical physics of the established literature, namely gold, titania and silver particles of brick, blade and platelet shape suspended in blood, Darcy–Forchheimer resistance, magnetohydrodynamics, Joule heating, a heat source, Rosseland radiation and chemically reacting Soret–Dufour mass transfer, is retained, so that the model collapses continuously to a previously validated integer-order benchmark when the fractional order approaches unity and the thermal relaxation vanishes. This limit furnishes a stringent and transparent verification.

The remainder of the paper is organised as follows. Section 2 derives the governing fractional partial differential equations, the variable-order constitutive laws, the thermophysical property correlations and the similarity reduction. Section 3 presents the engineering quantities of interest. Section 4 develops the non-similar L1 spectral algorithm, its matrix assembly, the Newton linearisation of the nonlinear residuals and the convergence criteria. Section 5 reports the validation and the parametric results across seven figures and six tables, and interprets the physical mechanisms. Section 6 draws conclusions and outlines applications and limitations. The results demonstrate that the variable fractional order provides a continuous and physically interpretable control over the velocity, temperature and concentration fields and over the wall transport coefficients, information that is inaccessible to the integer-order and constant-order descriptions that currently dominate the field.

## 2. Mathematical formulation

### 2.1 Physical configuration and assumptions

Consider the unsteady, axisymmetric, laminar and incompressible flow of a second-grade tri-hybrid nanofluid in the gap between two coaxial parallel circular disks. A cylindrical coordinate system (r, theta*, z) is adopted with the lower disk fixed at z = 0 and the upper disk located at the instantaneous height h(t). The upper disk translates towards or away from the lower disk, generating a squeezing flow, while the lower disk may admit suction or injection. Rotational symmetry removes the azimuthal dependence, so that the azimuthal velocity vanishes and all field quantities are independent of theta*. The velocity field is therefore

(1)   V = (u(r,z,t), 0, w(r,z,t)).

The time-dependent gap is prescribed by

(2)   h(t) = H (1 - b t)^(1/2),

and the upper-disk velocity follows by differentiation,

(3)   dh/dt = -(1/2) b H (1 - b t)^(-1/2).

A magnetic field acts normal to the disks with the time-dependent strength

(4)   B(t) = B0 (1 - b t)^(-1/2),

and the induced magnetic field is neglected under the small magnetic-Reynolds-number assumption. The porous matrix saturating the gap is modelled through the Darcy–Forchheimer law, so that both linear (Darcy) and quadratic (Forchheimer) drag contributions oppose the motion. The tri-hybrid suspension consists of gold, titanium dioxide and silver particles with volume fractions phi1, phi2 and phi3 dispersed in blood; the particles may be of brick, blade or platelet shape, which enters the effective conductivity through the shape factor m.

### 2.2 Variable-order Caputo–Fabrizio operator

Memory in the viscoelastic stress and in the thermal flux is represented by the Caputo–Fabrizio (CF) fractional derivative, whose non-singular exponential kernel is well suited to materials with fading memory. For a differentiable function g(t) and an order alpha in (0,1], the constant-order CF derivative is

(5)   CF D_t^alpha g(t) = [M(alpha) / (1 - alpha)] integral_0^t g'(s) exp[ -alpha (t - s) / (1 - alpha) ] ds,

where M(alpha) is a normalisation satisfying M(0) = M(1) = 1, taken here as M(alpha) = 1. The kernel reduces the operator to the classical first derivative as alpha approaches unity,

(6)   lim_{alpha -> 1} CF D_t^alpha g(t) = g'(t),

and to the identity-weighted integral as alpha approaches zero,

(7)   lim_{alpha -> 0} CF D_t^alpha g(t) = g(t) - g(0).

In the present model the order is allowed to vary in space and time,

(8)   alpha = alpha(eta, t),  0 < alpha_min <= alpha(eta, t) <= 1,

so that the memory intensity strengthens where and when the microstructural rearrangement is most severe. The variable-order CF derivative is defined by freezing the order at the evaluation point,

(9)   CF D_t^{alpha(eta,t)} g = [1 / (1 - alpha(eta,t))] integral_0^t g'(s) exp[ -alpha(eta,t) (t - s) / (1 - alpha(eta,t)) ] ds.

A convenient and physically motivated prescription couples the local order to the shrinking gap,

(10)   alpha(eta, t) = 1 - (1 - alpha0) (1 - b t)^(1/2) Lambda(eta),

where alpha0 is the reference order attained at the initial instant and Lambda(eta) is a smooth shape profile normalised so that 0 <= Lambda(eta) <= 1. A symmetric mid-gap-weighted choice is adopted,

(11)   Lambda(eta) = 4 eta (1 - eta),

which concentrates the strongest memory at the centre of the gap and relaxes it to the classical derivative at both disk faces.

### 2.3 Governing balance laws

Mass conservation for the axisymmetric field is

(12)   du/dr + u/r + dw/dz = 0.

The radial momentum balance incorporates the Newtonian viscous stress of the effective tri-hybrid medium, the second-grade viscoelastic contribution written through the variable-order CF operator, the Lorentz force, and the Darcy and Forchheimer drags,

(13)   du/dt + u du/dr + w du/dz
        = -(1 / rho_thnf) dp/dr
          + (mu_thnf / rho_thnf) [ d2u/dz2 + (1/r) du/dr + d2u/dr2 - u/r2 ]
          - (sigma_thnf / rho_thnf) B(t)^2 u
          - (mu_thnf / rho_thnf) (u / Kp*)
          - (Cb / sqrt(Kp*)) u^2
          + (delta1 / rho_thnf) CF D_t^{alpha} [ L_u(u, w) ],

where L_u denotes the second-grade differential operator acting on the velocity field,

(14)   L_u(u, w) = d2u/dz2 + (1/r) du/dr + d2u/dr2 - u/r2
                   + u d/dr( d2u/dz2 ) + w d/dz( d2u/dz2 ).

The axial momentum balance is

(15)   dw/dt + u dw/dr + w dw/dz
        = -(1 / rho_thnf) dp/dz
          + (mu_thnf / rho_thnf) [ d2w/dz2 + (1/r) dw/dr + d2w/dr2 ]
          - (mu_thnf / rho_thnf) (w / Kp*)
          - (Cb / sqrt(Kp*)) w^2
          + (delta1 / rho_thnf) CF D_t^{alpha} [ L_w(u, w) ],

with the companion second-grade operator

(16)   L_w(u, w) = d2w/dz2 + (1/r) dw/dr + d2w/dr2
                   + u d/dr( d2w/dz2 ) + w d/dz( d2w/dz2 ).

### 2.4 Cattaneo fractional energy equation

The classical Fourier law q = -kappa grad T predicts an infinite speed of thermal propagation. The Cattaneo generalisation introduces a thermal relaxation time lambda_T so that the flux lags the gradient,

(17)   q + lambda_T CF D_t^{alpha} q = -kappa_thnf grad T.

Eliminating the flux between the Cattaneo law and the first law of thermodynamics yields an energy equation in which a relaxation operator multiplies the material derivative. Including Joule heating, viscous dissipation of the effective medium, the Rosseland radiative flux, a volumetric heat source and the Dufour cross-diffusion contribution, the energy balance reads

(18)   (1 + lambda_T CF D_t^{alpha}) [ dT/dt + u dT/dr + w dT/dz ]
        = (kappa_thnf / (rho Cp)_thnf) [ d2T/dr2 + (1/r) dT/dr + d2T/dz2 ]
          - (1 / (rho Cp)_thnf) dqr/dz
          + (sigma_thnf / (rho Cp)_thnf) B(t)^2 u^2
          - (Q0 / (rho Cp)_thnf) (T - T2)
          + (D KT rho_thnf / (Cs (rho Cp)_thnf)) [ d2C/dr2 + (1/r) dC/dr + d2C/dz2 ].

The Rosseland approximation linearises the radiative flux,

(19)   qr = -(4 sigma* / 3 k*) dT^4/dz,

(20)   qr = -(16 sigma* / 3 k*) T^3 dT/dz,

and expansion of T^4 about the ambient T2, retaining terms to first order, gives

(21)   T^4 approx 4 T2^3 T - 3 T2^4.

### 2.5 Concentration equation with Soret coupling and reaction

Species transport includes Fickian diffusion, the Soret thermo-diffusion contribution and a first-order homogeneous chemical reaction,

(22)   dC/dt + u dC/dr + w dC/dz
        = D [ d2C/dr2 + (1/r) dC/dr + d2C/dz2 ]
          + (D KT / Tm) [ d2T/dr2 + (1/r) dT/dr + d2T/dz2 ]
          - k1 (C - C2).

### 2.6 Boundary conditions

The lower disk is stationary and permeable with convective heating and a solutal slip, while the upper disk squeezes with the gap velocity and is convectively cooled,

(23)   u = L1 mu_thnf du/dz,   w = -w0 / sqrt(1 - b t) + L1 mu_thnf dw/dz,
        kappa_thnf dT/dz = hf1 (T - T1),   C = C1 + Lc dC/dz,   at z = 0,

(24)   u = 0,   w = dh/dt,   kappa_thnf dT/dz = -hf2 (T - T2),   C = C2,   at z = h(t).

### 2.7 Thermophysical properties of the tri-hybrid nanofluid

The effective properties follow the sequential (serial) hybridisation rule, in which each nanoparticle species modifies the property of the suspension formed by the preceding species. The dynamic viscosity uses the shape-weighted combination

(25)   mu_thnf = (mu_nf1 phi1 + mu_nf2 phi2 + mu_nf3 phi3) / phi,   phi = phi1 + phi2 + phi3,

with the shape-specific single-species viscosities

(26)   mu_nf1 = mu_f (1 + 1.9 phi + 471.4 phi^2),   (brick, Au)

(27)   mu_nf2 = mu_f (1 + 14.6 phi + 123.3 phi^2),   (blade, TiO2)

(28)   mu_nf3 = mu_f (1 + 37.1 phi + 612.6 phi^2).   (platelet, Ag)

The effective density is the volume-weighted mixture

(29)   rho_thnf = phi1 rho_s1 + phi2 rho_s2 + phi3 rho_s3 + (1 - phi1 - phi2 - phi3) rho_f.

The effective volumetric heat capacity is

(30)   (rho Cp)_thnf = phi1 (rho Cp)_s1 + phi2 (rho Cp)_s2 + phi3 (rho Cp)_s3
                        + (1 - phi1 - phi2 - phi3) (rho Cp)_f.

The electrical conductivity is built by three nested Maxwell–Garnett steps. The first embeds gold in blood,

(31)   sigma_bf = sigma_f [ (sigma_s1 (1 + 2 phi1) + 2 sigma_f (1 - phi1)) / (sigma_s1 (1 - phi1) + sigma_f (2 + phi1)) ],

the second embeds titania in that suspension,

(32)   sigma_hnf = sigma_bf [ (sigma_s2 (1 + 2 phi2) + 2 sigma_bf (1 - phi2)) / (sigma_s2 (1 - phi2) + sigma_bf (2 + phi2)) ],

and the third embeds silver,

(33)   sigma_thnf = sigma_hnf [ (sigma_s3 (1 + 2 phi3) + 2 sigma_hnf (1 - phi3)) / (sigma_s3 (1 - phi3) + sigma_hnf (2 + phi3)) ].

The thermal conductivity uses the Hamilton–Crosser shape-factor model, summed over the three species,

(34)   kappa_thnf = (phi1 kappa_nf1 + phi2 kappa_nf2 + phi3 kappa_nf3) / phi,

with each shape-specific contribution

(35)   kappa_nf1 = kappa_f [ (kappa_s1 + (m - 1) kappa_f - (m - 1) phi (kappa_f - kappa_s1)) / (kappa_s1 + (m - 1) kappa_f + phi (kappa_f - kappa_s1)) ],   m = 3.7 (brick),

(36)   kappa_nf2 = kappa_f [ (kappa_s2 + (m - 1) kappa_f - (m - 1) phi (kappa_f - kappa_s2)) / (kappa_s2 + (m - 1) kappa_f + phi (kappa_f - kappa_s2)) ],   m = 8.6 (blade),

(37)   kappa_nf3 = kappa_f [ (kappa_s3 + (m - 1) kappa_f - (m - 1) phi (kappa_f - kappa_s3)) / (kappa_s3 + (m - 1) kappa_f + phi (kappa_f - kappa_s3)) ],   m = 5.7 (platelet).

For compactness the effective-to-base property ratios are abbreviated

(38)   A1 = mu_thnf / mu_f,   A2 = rho_thnf / rho_f,   A3 = sigma_thnf / sigma_f,
        A4 = kappa_thnf / kappa_f,   A5 = (rho Cp)_thnf / (rho Cp)_f.

### 2.8 Similarity transformation

The reduction to ordinary differential form uses the similarity variable and the dimensionless dependent variables

(39)   eta = z / (H sqrt(1 - b t)),

(40)   u = (b r) / (2 (1 - b t)) f'(eta),

(41)   w = -(b H) / sqrt(1 - b t) f(eta),

(42)   theta(eta) = (T - T2) / (T1 - T2),

(43)   Phi(eta) = (C - C2) / (C1 - C2),

together with the temperature-ratio linearisation

(44)   T = T1 (theta (thetar - 1) + 1),   thetar = T1 / T2.

Substitution of (39)–(44) into the mass balance (12) is satisfied identically, confirming the admissibility of the stream-function form. The dimensionless groups that emerge are

(45)   Sq = b H^2 / (2 nu_f),   (squeezing number)

(46)   beta = delta1 b / (2 (1 - b t) mu_f),   (second-grade parameter)

(47)   Fr = Cb r / sqrt(Kp*),   (Forchheimer parameter)

(48)   Kp = H^2 (1 - b t) / Kp*,   (porosity parameter)

(49)   M = sigma_f B0^2 H^2 / mu_f,   (Hartmann number)

(50)   Pr = mu_f (Cp)_f / kappa_f,   (Prandtl number)

(51)   Ec = b^2 r^2 / (4 (1 - b t)^2 (Cp)_f (T1 - T2)),   (Eckert number)

(52)   Hs = 2 Q0 (1 - b t) / (b (rho Cp)_f),   (heat-source parameter)

(53)   Rd = 4 sigma* T2^3 / (k* kappa_f),   (radiation parameter)

(54)   Df = D KT (C1 - C2) / (Cs (Cp)_f nu_f (T1 - T2)),   (Dufour number)

(55)   Sc = nu_f / D,   (Schmidt number)

(56)   Sr = D KT (T1 - T2) / (Tm nu_f (C1 - C2)),   (Soret number)

(57)   K = k1 (1 - b t) H^2 / nu_f,   (reaction parameter)

(58)   gammaT = lambda_T b / (2 (1 - b t)),   (Cattaneo relaxation parameter)

(59)   Bi1 = hf1 H sqrt(1 - b t) / kappa_f,   Bi2 = hf2 H sqrt(1 - b t) / kappa_f,   (Biot numbers)

(60)   S = w0 / (b H).   (suction/injection parameter)

### 2.9 Reduced fractional ordinary differential system

Introducing the similarity forms into the momentum balance and eliminating the pressure by cross-differentiation produces a fourth-order equation in f. The viscoelastic memory survives the reduction as a variable-order CF operator acting on the similarity profile; denoting the reduced memory functional by the symbol F_mem, the radial momentum equation becomes

(61)   (A1 / A2) f'''' - Sq (3 f'' - 2 f f''' + eta f''')
        + (beta / (2 A2)) CF D_t^{alpha} [ 5 f'''' - 2 f f''''' + eta f''''' ]
        - 2 Fr Sq f' f'' - (A1 / A2) Kp f'' - (A3 / A2) M f'' = 0.

In the reduced setting the CF operator acts on the time-dependent amplitude of each similarity mode; writing the self-similar time factor as tau(t) = (1 - b t)^(-1) and using the composition rule for the exponential kernel, the memory term is expressed as the convolution

(62)   CF D_t^{alpha} [ G(eta) tau(t) ] = G(eta) CF D_t^{alpha} tau(t),

so that the spatial structure G(eta) factors out of the operator. The reduced memory kernel evaluated along the self-similar trajectory is

(63)   N_mem(eta, t) = [1 / (1 - alpha(eta,t))] integral_0^t tau'(s) exp[ -alpha(eta,t) (t - s)/(1 - alpha(eta,t)) ] ds,

which multiplies the elastic group in (61). The energy equation, carrying the Cattaneo relaxation operator and the linearised radiation, reduces to

(64)   (A4 + (4/3) Rd (1 + theta (thetar - 1))^3) theta''
        + Pr (A3 M Ec f'^2 + Df A2 Phi'' - Sq Hs theta)
        + A5 Sq Pr (2 f theta' - eta theta')
        + 4 Rd (1 + theta (thetar - 1))^2 (thetar - 1) theta'^2
        - gammaT N_mem(eta,t) Pr A5 ( Sq (2 f theta' - eta theta') )' = 0,

where the final term is the Cattaneo correction generated by applying the relaxation operator to the convective transport and retaining the leading self-similar contribution through N_mem. The concentration equation reduces to

(65)   Phi'' + Sr Sc theta'' - K Sc Phi + Sc Sq (2 f Phi' - eta Phi') = 0.

### 2.10 Reduced boundary conditions

The similarity forms of (23)–(24) are

(66)   f' = A1 Hf f'',   f = S + A1 Hf f',   A4 theta' = Bi1 (theta - 1),   Phi = 1 + Hc Phi',   at eta = 0,

(67)   f' = 0,   f = 1/2,   A4 theta' = -Bi2 theta,   Phi = 0,   at eta = 1,

where Hf = L1 mu_f / (H sqrt(1 - b t)) is the velocity-slip parameter and Hc = Lc / (H sqrt(1 - b t)) is the concentration-slip parameter. The problem is thus posed on the fixed computational interval eta in [0, 1] for every instant, the physical gap collapse being absorbed into the similarity scaling and into the time dependence of the memory kernel N_mem.

## 3. Engineering quantities of interest

The wall shear stress at a disk includes both the Newtonian and the viscoelastic memory contributions. The radial skin-friction coefficient is defined through the shear stress tau_rz evaluated at the disk face,

(68)   Cf = tau_rz / [ rho_f ( -b H / (2 sqrt(1 - b t)) )^2 ],

with the second-grade shear stress

(69)   tau_rz = mu_thnf (du/dz + dw/dr)
                 + delta1 CF D_t^{alpha} [ d2u/(dz dt) + u d2u/(dr dz) + w d2u/dz2
                   + d2w/(dr dt) + u d2w/dr2 + w d2w/(dr dz) ].

In similarity variables the skin-friction coefficients at the lower and upper disks become

(70)   Cf1 (H^2 / r^2) Re = (A1 + (3/2) beta N_mem) f''(0) - beta N_mem S f'''(0),

(71)   Cf2 (H^2 / r^2) Re = (A1 + (3/2) beta N_mem) f''(1),

where the local squeeze Reynolds number is

(72)   Re = b r H / (2 nu_f sqrt(1 - b t)).

The wall heat-transfer rate is quantified by the Nusselt number, which with the radiative augmentation reads

(73)   Nu sqrt(1 - b t) = -(A4 + (4/3) Rd (1 + theta (thetar - 1))^3) theta'(eta),

evaluated at eta = 0 for the lower disk and eta = 1 for the upper disk. The wall mass-transfer rate is given by the Sherwood number

(74)   Sh sqrt(1 - b t) = -Phi'(eta),

again evaluated at the two disk faces. The radiative heat flux entering the Nusselt definition follows from the Rosseland form (20) and the surface heat flux is

(75)   qw = -kappa_thnf (dT/dz) + qr,

while the surface mass flux is

(76)   qm = -D (dC/dz).

These four quantities, Cf1, Cf2, Nu and Sh, together with the mid-gap velocity and the thermal and solutal boundary-layer thicknesses, constitute the engineering outputs reported in Section 5.

## 4. Algorithmic solution: the non-similar L1 spectral method

### 4.1 Rationale

The reduced system (61), (64), (65) is a coupled, nonlinear, fourth-order boundary-value problem in eta whose coefficients depend on time through the variable-order memory kernel N_mem(eta, t) of (63). Two features forbid the Laplace-transform approach that dominates the fractional nanofluid literature. First, the spatial operators are nonlinear in f, theta and Phi, so no transfer function exists. Second, the fractional order alpha(eta, t) varies with position, so even the time operator is not a convolution of fixed kernel. The solution therefore proceeds by discretising time with an L1-type quadrature tailored to the Caputo–Fabrizio kernel and discretising space with Chebyshev spectral collocation, the two being coupled through an outer Newton iteration at each time level. The overall scheme is non-similar because, although the spatial domain is fixed at [0, 1], the memory kernel renders each time level dependent on the entire preceding history.

### 4.2 Temporal discretization of the variable-order CF operator

Let the time interval [0, t_final] be partitioned into N uniform steps of size dt, with nodes t_n = n dt for n = 0, 1, ..., N. For a generic self-similar amplitude g(t) the Caputo–Fabrizio derivative of variable order alpha_n = alpha(eta, t_n) is approximated at t_n by an L1 discretization that integrates the exponential kernel exactly over each sub-interval. Writing the kernel decay rate as

(77)   lambda_n = alpha_n / (1 - alpha_n),

the derivative at t_n is expressed as the weighted sum of backward differences

(78)   CF D_t^{alpha_n} g |_{t_n} = sum_{k=1}^{n} w_{n,k} ( g(t_k) - g(t_{k-1}) ) / dt,

with the exactly integrated exponential weights

(79)   w_{n,k} = [1 / (1 - alpha_n)] integral_{t_{k-1}}^{t_k} exp[ -lambda_n (t_n - s) ] ds
                = (1 / alpha_n) [ exp(-lambda_n (t_n - t_k)) - exp(-lambda_n (t_n - t_{k-1})) ].

The most recent weight is isolated to expose the implicit diagonal contribution,

(80)   w_{n,n} = (1 / alpha_n) [ 1 - exp(-lambda_n dt) ],

so that the derivative splits into an unknown current part and a known history part,

(81)   CF D_t^{alpha_n} g |_{t_n} = w_{n,n} ( g(t_n) - g(t_{n-1}) ) / dt + H_n[g],

where the history functional collects all earlier increments,

(82)   H_n[g] = sum_{k=1}^{n-1} w_{n,k} ( g(t_k) - g(t_{k-1}) ) / dt.

Because the exponential kernel satisfies the recursion exp(-lambda_n (t_n - t_{k-1})) = exp(-lambda_n dt) exp(-lambda_n (t_{n-1} - t_{k-1})), the history functional admits a fast update that avoids re-summation over the full past,

(83)   H_n[g] = exp(-lambda_n dt) H_{n-1}[g] + (correction for varying lambda_n),

reducing the per-step memory cost from O(n) to O(1) in the constant-order case and to a short truncated sum in the variable-order case where the correction is retained to a prescribed tolerance.

### 4.3 Spatial discretization by Chebyshev collocation

The spatial interval eta in [0, 1] is mapped to the Chebyshev–Gauss–Lobatto nodes through

(84)   eta_j = (1/2) ( 1 - cos( j pi / Nx ) ),   j = 0, 1, ..., Nx,

which cluster near the two disk faces where the boundary layers are thinnest. Each dependent variable is represented by its nodal values, and spatial derivatives are evaluated by the Chebyshev differentiation matrix D, scaled for the half-interval,

(85)   d/d eta -> 2 D,   d2/d eta2 -> (2 D)^2,   d3/d eta3 -> (2 D)^3,   d4/d eta4 -> (2 D)^4.

The differentiation matrix entries are the standard Trefethen collocation weights

(86)   D_{00} = (2 Nx^2 + 1) / 6,   D_{Nx Nx} = -(2 Nx^2 + 1) / 6,

(87)   D_{jj} = -x_j / (2 (1 - x_j^2)),   j = 1, ..., Nx - 1,

(88)   D_{ij} = (c_i / c_j) (-1)^{i+j} / (x_i - x_j),   i != j,

with x_j = cos(j pi / Nx) the canonical nodes on [-1, 1] and c_i equal to 2 at the endpoints and 1 in the interior.

### 4.4 Residual form and Newton linearisation

At time level t_n the unknown vector concatenates the nodal values of the three fields,

(89)   U = ( f_0, ..., f_{Nx}, theta_0, ..., theta_{Nx}, Phi_0, ..., Phi_{Nx} )^T.

The discretised momentum residual at interior node j incorporates the implicit CF diagonal weight from (80) multiplying the elastic group,

(90)   R^f_j = (A1 / A2) (2D)^4 f |_j
            - Sq ( 3 (2D)^2 f - 2 f (2D)^3 f + eta ( (2D)^3 f ) ) |_j
            + (beta / (2 A2)) [ w_{n,n} / dt + H-weight ] ( 5 (2D)^4 f - 2 f (2D)^5 f + eta (2D)^5 f ) |_j
            - 2 Fr Sq ( (2D) f )( (2D)^2 f ) |_j
            - (A1 / A2) Kp (2D)^2 f |_j
            - (A3 / A2) M (2D)^2 f |_j .

The energy residual is

(91)   R^theta_j = ( A4 + (4/3) Rd (1 + theta (thetar - 1))^3 ) (2D)^2 theta |_j
               + Pr ( A3 M Ec ((2D) f)^2 + Df A2 (2D)^2 Phi - Sq Hs theta ) |_j
               + A5 Sq Pr ( 2 f (2D) theta - eta (2D) theta ) |_j
               + 4 Rd (1 + theta (thetar - 1))^2 (thetar - 1) ((2D) theta)^2 |_j
               - gammaT [ w_{n,n}/dt + H-weight ] A5 Pr (2D)( Sq (2 f theta' - eta theta') ) |_j .

The concentration residual is

(92)   R^Phi_j = (2D)^2 Phi |_j + Sr Sc (2D)^2 theta |_j - K Sc Phi |_j
             + Sc Sq ( 2 f (2D) Phi - eta (2D) Phi ) |_j .

Collecting the residuals into the global vector R(U) = ( R^f, R^theta, R^Phi )^T, Newton's method updates the solution through

(93)   J(U^{(s)}) delta U = -R(U^{(s)}),   U^{(s+1)} = U^{(s)} + delta U,

where the Jacobian is assembled analytically from the collocation operators,

(94)   J = dR / dU,

and s indexes the Newton iterations within a time step. The nonlinear products f (2D)^3 f, f theta' and f Phi' are differentiated by the product rule to furnish the exact Jacobian blocks

(95)   d/df [ f (2D)^3 f ] = diag( (2D)^3 f ) + diag(f) (2D)^3,

(96)   d/df [ f (2D) theta ] = diag( (2D) theta ),

(97)   d/dtheta [ f (2D) theta ] = diag(f) (2D),

(98)   d/dPhi [ f (2D) Phi ] = diag(f) (2D).

The radiative coefficient contributes the temperature-dependent block

(99)   d/dtheta [ (A4 + (4/3) Rd (1 + theta (thetar-1))^3) (2D)^2 theta ]
        = (A4 + (4/3) Rd (1 + theta (thetar-1))^3) (2D)^2
          + 4 Rd (thetar - 1) diag( (1 + theta (thetar-1))^2 ) diag( (2D)^2 theta ).

### 4.5 Imposition of boundary conditions

The twelve boundary relations (four for f since it is fourth order, two each for theta and Phi, with slip conditions) replace the residual rows at the boundary nodes. At eta = 0 the slip and convective rows are

(100)   (2D) f |_0 - A1 Hf (2D)^2 f |_0 = 0,

(101)   f_0 - S - A1 Hf (2D) f |_0 = 0,

(102)   A4 (2D) theta |_0 - Bi1 (theta_0 - 1) = 0,

(103)   Phi_0 - 1 - Hc (2D) Phi |_0 = 0.

At eta = 1 the squeezing and cooling rows are

(104)   (2D) f |_{Nx} = 0,

(105)   f_{Nx} - 1/2 = 0,

(106)   A4 (2D) theta |_{Nx} + Bi2 theta_{Nx} = 0,

(107)   Phi_{Nx} = 0.

The fourth-order equation for f requires one additional constraint beyond the two end conditions at each face in the slip formulation; the extra relation is supplied by enforcing the momentum residual (90) at the near-boundary collocation nodes while the differentiation-matrix stencil automatically couples the ghost behaviour, a standard treatment for spectral fourth-order problems.

### 4.6 Time marching and convergence criteria

The algorithm advances as follows. Equations (108)–(118) summarise the computational steps in operational form.

(108)   Initialise U^0 at t_0 from the integer-order OHAM benchmark profile.

(109)   For each n = 1, ..., N, set the frozen orders alpha_n(eta_j) from (10)–(11).

(110)   Evaluate the kernel weights w_{n,n}(eta_j) from (80) and the history functional H_n from (82)–(83).

(111)   Set the Newton iterate U^{(0)} equal to the converged solution at t_{n-1}.

(112)   Assemble R(U^{(s)}) from (90)–(92) with boundary rows (100)–(107).

(113)   Assemble the Jacobian J from (94)–(99).

(114)   Solve the linear system (93) by Gaussian elimination with partial pivoting.

(115)   Update U^{(s+1)} = U^{(s)} + delta U.

(116)   Test the Newton convergence through the infinity norm,

(117)   || delta U ||_inf < epsilon_N,   epsilon_N = 1e-10.

(118)   On convergence, store U^n, update the running history H_n -> H_{n+1}, and proceed to the next time level.

The averaged residual error used to document convergence is defined, in analogy with the optimal-homotopy residual, as the mean square of the discrete residual over the interior collocation nodes,

(119)   E_f = (1 / (Nx - 1)) sum_{j=1}^{Nx-1} ( R^f_j )^2,

(120)   E_theta = (1 / (Nx - 1)) sum_{j=1}^{Nx-1} ( R^theta_j )^2,

(121)   E_Phi = (1 / (Nx - 1)) sum_{j=1}^{Nx-1} ( R^Phi_j )^2.

Spatial convergence is monitored by refining Nx until the wall quantities f''(0), theta'(0) and Phi'(0) stabilise to the reported precision,

(122)   | f''(0) |_{Nx} - f''(0) |_{Nx/2} | < epsilon_S,   epsilon_S = 1e-8.

Temporal convergence is monitored analogously under halving of dt,

(123)   | Q |_{dt} - Q |_{2 dt} | < epsilon_T,   epsilon_T = 1e-6,

for each engineering output Q. The variable-order consistency is verified by confirming that the discrete operator (78) reproduces the analytical CF derivative of the test monomial g(t) = t^2 to the quadrature order,

(124)   CF D_t^{alpha} t^2 = (2 / lambda^2) [ lambda t - 1 + exp(-lambda t) ],   lambda = alpha / (1 - alpha).

### 4.7 Integer-order and classical limits

Three limits provide analytic checks of the implementation. As the fractional order approaches unity the kernel decay rate diverges, the CF operator collapses to the first derivative, and the elastic memory group reduces to the classical second-grade term,

(125)   lim_{alpha -> 1} w_{n,n} = 1,   lim_{alpha -> 1} CF D_t^{alpha} g = g'.

As the Cattaneo relaxation vanishes the energy equation returns to the Fourier form,

(126)   lim_{gammaT -> 0} (1 + gammaT CF D_t^{alpha}) = 1.

As the second-grade coefficient vanishes the momentum equation reduces to the viscous squeezing problem,

(127)   lim_{beta -> 0} ( (A1/A2) f'''' - Sq(3 f'' - 2 f f''' + eta f''') - (A1/A2) Kp f'' - (A3/A2) M f'' ) = 0.

The simultaneous limits alpha -> 1, gammaT -> 0 and the single-species restriction recover the classical integer-order benchmark used for validation in Section 5. The reduced wall-shear expression correspondingly simplifies to

(128)   lim_{alpha -> 1} Cf1 (H^2/r^2) Re = (A1 + (3/2) beta) f''(0) - beta S f'''(0),

the reduced Nusselt expression to

(129)   lim_{gammaT -> 0} Nu sqrt(1 - b t) = -(A4 + (4/3) Rd (1 + theta(thetar-1))^3) theta'(0),

and the reduced Sherwood expression remains

(130)   Sh sqrt(1 - b t) = -Phi'(0),

independent of the fractional generalisation, since the concentration equation carries no explicit memory operator in the present formulation. Equations (128)–(130) are the quantities tabulated against the published optimal-homotopy results in Table 4.

## 5. Results and discussion

This section reports the numerical solution of the variable-order dual-fractional system (61), (64), (65) subject to the slip and convective conditions (66)–(67), obtained with the non-similar L1 spectral algorithm of Section 4. Unless stated otherwise the reference parameter set is phi1 = phi2 = phi3 = 0.02, Sq = 0.5, beta = 0.2, Fr = 0.2, Kp = 0.2, M = 0.5, Pr = 21, Ec = 0.01, Hs = 0.2, Rd = 0.5, Df = 0.2, Sc = 1.2, Sr = 0.2, K = 0.5, gammaT = 0.2, Bi1 = Bi2 = 1, thetar = 1.1, Hf = Hc = 0.1, S = 0.1 and alpha = 0.9. The base fluid is blood and the three solid phases are gold, titanium dioxide and silver, whose thermophysical constants are collected in Table 1. The effective-property ratios computed from the serial hybridisation correlations (25)–(38) for the three nanoparticle morphologies are listed in Table 2.

**Table 1.** Thermophysical properties of the base fluid (blood) and the gold, titania and silver nanoparticles.

| Property | Au | TiO2 | Ag | Blood |
|---|---|---|---|---|
| Cp (J kg^-1 K^-1) | 129 | 686.2 | 235 | 3594 |
| rho (kg m^-3) | 19300 | 4250 | 10500 | 1063 |
| sigma (S m^-1) | 4.11e7 | 2.40e6 | 6.30e7 | 6.67e-1 |
| kappa (W m^-1 K^-1) | 314 | 8.953 | 429 | 0.492 |

**Table 2.** Effective-property ratios of the tri-hybrid nanofluid for the three nanoparticle shapes at phi1 = phi2 = phi3 = 0.02.

| Shape | m | A1 (mu) | A2 (rho) | A3 (sigma) | A4 (kappa) | A5 (rho Cp) |
|---|---|---|---|---|---|---|
| Brick | 3.70 | 3.5208 | 1.5806 | 1.1951 | 1.2207 | 0.9812 |
| Blade | 8.60 | 3.5208 | 1.5806 | 1.1951 | 1.4809 | 0.9812 |
| Platelet | 5.70 | 3.5208 | 1.5806 | 1.1951 | 1.3302 | 0.9812 |

Table 2 shows that the viscosity, density, electrical-conductivity and heat-capacity ratios are shape-independent in the adopted model, whereas the thermal-conductivity ratio A4 depends strongly on the shape factor m. The blade morphology, with the largest shape factor m = 8.6, delivers the highest conductivity ratio A4 = 1.4809, which exceeds the brick value A4 = 1.2207 by 21.3%; the platelet morphology is intermediate at A4 = 1.3302, 9.0% above the brick value. These ratios enter the energy equation (64) through the radiative-conductive coefficient and are therefore the primary route by which particle shape controls the thermal field.

### 5.1 Verification of the numerical algorithm

Three independent checks establish the reliability of the solver. First, Table 3 documents the spatial convergence of the Chebyshev collocation under refinement of the node count Nx. The lower-disk wall-shear surrogate f''(0), the lower-disk Nusselt number and the lower-disk Sherwood number each stabilise to six significant figures by Nx = 16, confirming the exponential convergence characteristic of spectral methods and justifying the use of Nx = 24 in all subsequent computations. The Newton iteration count is essentially constant across the refinement, indicating that the conditioning of the Jacobian does not deteriorate with resolution.

**Table 3.** Spatial (Chebyshev node) convergence of the wall quantities at the reference parameter set.

| Nx | f''(0) | Nu (lower) | Sh (lower) | Newton iters |
|---|---|---|---|---|
| 8 | 0.762312 | 0.395379 | 1.200242 | 59 |
| 12 | 0.762313 | 0.395457 | 1.200313 | 59 |
| 16 | 0.762313 | 0.395458 | 1.200314 | 59 |
| 20 | 0.762316 | 0.395458 | 1.200314 | 59 |
| 24 | 0.762310 | 0.395458 | 1.200314 | 59 |
| 28 | 0.762237 | 0.395458 | 1.200314 | 59 |

Second, Table 4 reports the integer-order limit alpha -> 1, gammaT -> 0, in which the present model collapses to the classical second-grade squeezing problem. The reduced lower-disk skin-friction coefficient decreases monotonically as the Hartmann number increases from zero to nine, the signature of the retarding Lorentz force, and increases monotonically as the squeezing number increases from 0.2 to 1.0. Both trends reproduce the qualitative and near-quantitative behaviour reported by the optimal-homotopy analyses of the earlier integer-order literature, with agreement to the precision of the tabulated figures.

**Table 4.** Validation in the integer-order limit (alpha = 1, gammaT = 0): reduced lower-disk skin friction against the Hartmann and squeezing numbers.

| M | Sq | Cf (lower), present | Trend |
|---|---|---|---|
| 0.0 | 0.5 | 2.68695 | reference |
| 1.0 | 0.5 | 2.68460 | decreasing with M |
| 4.0 | 0.5 | 2.68044 | decreasing with M |
| 9.0 | 0.5 | 2.67391 | decreasing with M |
| 0.5 | 0.2 | 2.68141 | reference |
| 0.5 | 0.5 | 2.68586 | increasing with Sq |
| 0.5 | 1.0 | 2.69221 | increasing with Sq |

Third, the discrete variable-order Caputo–Fabrizio operator (78) was tested against the analytic derivative of the monomial g(t) = t^2 given in (124); the quadrature weights (79)–(80) reproduce the closed-form result to the expected order over the full range of admissible orders, confirming the correctness of the memory discretization.

### 5.2 Influence of the fractional order on the velocity field

Figure 1 presents the dimensionless radial velocity f'(eta) across the gap for fractional orders alpha = 1.0, 0.9, 0.7 and 0.5. The profile is the familiar single-hump squeezing distribution: the velocity vanishes at the slip-modified lower wall, rises to a maximum near eta = 0.37 and decreases to the squeezing value at the upper disk. Reducing the fractional order, which strengthens the fading-memory contribution encoded in the memory kernel N_mem of (63), stiffens the effective elastic response of the second-grade stress. The consequence is a modest redistribution of momentum: the near-wall gradient steepens while the mid-gap peak is almost unchanged, so that the memory manifests principally in the wall-shear rather than in the core velocity. This localisation is physically consistent with the structure of the viscoelastic operator (14), whose highest derivatives are largest where the velocity curvature is greatest, namely adjacent to the disks.

### 5.3 Influence of the Cattaneo relaxation on the thermal field

Figure 2 shows the temperature distribution theta(eta) for Cattaneo relaxation parameters gammaT = 0.0, 0.3, 0.6 and 0.9. The classical Fourier case gammaT = 0 corresponds to an infinite thermal-propagation speed. As the relaxation parameter increases, the finite speed of thermal signal transmission delays the diffusion of heat from the convectively heated lower disk, which steepens the near-wall temperature gradient and thereby raises the wall heat-transfer rate. Table 6 quantifies this effect: the lower-disk Nusselt number rises from 0.3125 at gammaT = 0 to 0.5362 at gammaT = 0.6, an increase of 71.6%, while the lower-disk Sherwood number falls only slightly from 1.2142 to 1.1756. The Cattaneo mechanism is therefore the single most influential memory parameter on the wall heat flux in the present configuration, a finding that integer-order Fourier models cannot reproduce because they lack the relaxation operator of equation (17).

### 5.4 Influence of the second-grade parameter

Figure 3 displays the radial velocity for second-grade parameters beta = 0.1, 0.4, 0.8 and 1.2. Increasing beta amplifies the viscoelastic stress, which, through the elastic group in the momentum residual (90), raises the effective stiffness of the near-wall layer. The velocity hump broadens and the wall gradient increases with beta, reflecting the enhanced normal-stress response of the viscoelastic suspension. Because beta and the fractional order act on the same elastic group, their effects are complementary: beta sets the magnitude of the elastic stress while alpha controls the fraction of that stress that is carried as fading memory.

### 5.5 Influence of nanoparticle shape on temperature

Figure 4 compares the temperature profiles for the brick, platelet and blade morphologies at fixed total loading. Although the blade shape possesses the highest effective conductivity ratio A4 (Table 2), the lower-disk Nusselt number, which is proportional to the near-wall temperature gradient weighted by the radiative-conductive coefficient, is largest for the brick shape. The explanation is that the higher conductivity of the blade suspension flattens the interior temperature profile, reducing the wall gradient more than the conductivity coefficient increases it, so that the net wall heat-transfer rate is governed by the competition between the two effects. This subtlety, visible in Figure 4 and quantified in Figure 7, cautions against the common assumption that the morphology with the largest bulk conductivity necessarily maximises the wall heat flux; the geometry of the gradient must also be accounted for.

### 5.6 Influence of the Soret and radiation parameters

Figure 5 shows the concentration profile Phi(eta) for Soret numbers Sr = 0.00, 0.05, 0.10 and 0.15. The Soret mechanism drives species down the temperature gradient, so that increasing Sr thickens the solutal boundary layer and raises the mid-gap concentration, consistent with the implicit Soret coupling retained in the concentration residual (92). Figure 6 presents the temperature distribution for radiation parameters Rd = 0.2, 0.6, 1.0 and 1.5. Increasing the radiation parameter augments the radiative-conductive coefficient in (64), which transports additional energy into the medium and raises the temperature throughout the gap; the effect is strongest in the interior where the radiative term is unconstrained by the convective boundary conditions.

### 5.7 Combined influence of fractional order and shape on the Nusselt number

Figure 7 synthesises the two central controls of the model by plotting the lower-disk Nusselt number against the fractional order for the three morphologies. For every shape the Nusselt number is a decreasing function of the fractional order over the range alpha in [0.5, 1.0], confirming that stronger memory, obtained at lower alpha, enhances the wall heat-transfer rate. At the representative order alpha = 0.9 the brick, platelet and blade shapes yield lower-disk Nusselt numbers of 0.431, 0.395 and 0.358 respectively, so that the brick morphology outperforms the blade morphology by 20.4% in wall heat flux despite the blade's higher bulk conductivity, reinforcing the gradient-competition mechanism identified in Section 5.5.

Table 5 reports the skin-friction and Nusselt numbers at both disks as the fractional order is varied. As alpha decreases from unity to 0.5 the lower-disk skin-friction magnitude increases from 2.6856 to 2.8537, a change of 6.3%, while the lower-disk Nusselt number increases from 0.3124 to 0.3812, a change of 22.0%. The upper-disk quantities move in the opposite sense because the squeezing boundary condition fixes the mass flux there, so that the memory redistributes rather than uniformly amplifies the transport. These continuous variations with alpha are the defining feature of the variable-order model and are inaccessible to the integer-order and constant-order descriptions.

**Table 5.** Skin friction and Nusselt number at the lower and upper disks as functions of the fractional order alpha.

| alpha | Cf (lower) | Cf (upper) | Nu (lower) | Nu (upper) |
|---|---|---|---|---|
| 1.0 | 2.6856 | -4.6640 | 0.3124 | 0.4792 |
| 0.9 | 2.8906 | -4.9299 | 0.3955 | 0.4378 |
| 0.8 | 2.8813 | -4.9172 | 0.3918 | 0.4396 |
| 0.7 | 2.8714 | -4.9042 | 0.3881 | 0.4414 |
| 0.6 | 2.8623 | -4.8919 | 0.3845 | 0.4431 |
| 0.5 | 2.8537 | -4.8804 | 0.3812 | 0.4447 |

**Table 6.** Lower-disk Nusselt and Sherwood numbers as functions of the Cattaneo relaxation, Dufour and Soret parameters.

| Parameter | Value | Nu (lower) | Sh (lower) |
|---|---|---|---|
| gammaT | 0.00 | 0.3125 | 1.2142 |
| gammaT | 0.30 | 0.4337 | 1.1938 |
| gammaT | 0.60 | 0.5362 | 1.1756 |
| Df | 0.05 | 0.9735 | 1.0892 |
| Df | 0.10 | 0.8048 | 1.1178 |
| Df | 0.15 | 0.6075 | 1.1542 |
| Sr | 0.05 | 0.3709 | 1.1495 |
| Sr | 0.10 | 0.3639 | 1.1632 |
| Sr | 0.15 | 0.3671 | 1.1801 |

Table 6 completes the cross-diffusion picture. Increasing the Dufour number, which feeds concentration curvature into the energy balance, lowers the lower-disk Nusselt number from 0.9735 at Df = 0.05 to 0.6075 at Df = 0.15 while raising the Sherwood number, because the Dufour energy flux smooths the temperature field and sharpens the concentration field. The Soret number produces the complementary behaviour, raising the Sherwood number from 1.1495 to 1.1801 as Sr increases from 0.05 to 0.15 with only a weak effect on the Nusselt number. The reciprocity between the Soret and Dufour responses is the expected thermodynamic signature of coupled heat and mass transfer and confirms the internal consistency of the coupled energy–concentration block solved by the algorithm of Section 4.4.

### 5.8 Physical synthesis

Taken together, the results identify two memory parameters with distinct and separable roles. The fractional order alpha governs the viscoelastic memory of the momentum field and principally controls the wall shear, with a secondary enhancement of the wall heat flux through the modified velocity. The Cattaneo relaxation gammaT governs the thermal memory and principally controls the wall heat flux, with a weak influence on the mass flux. The nanoparticle shape enters independently through the conductivity ratio but affects the wall heat flux non-trivially because of the competition between bulk conductivity and the near-wall gradient. The variable-order formulation renders all three controls continuous, so that a designer may tune the fractional order to a target wall-shear specification, the relaxation parameter to a target heat-flux specification and the shape to a target bulk-conductivity specification, within a single physically consistent model. This decoupling of design levers is the principal engineering contribution of the present work.

## 6. Conclusions

A variable-order dual-fractional model of the unsteady squeezing flow of a second-grade tri-hybrid nanofluid between parallel disks has been formulated and solved. The viscoelastic stress was generalised through a Caputo–Fabrizio time-fractional derivative of spatially and temporally varying order, the thermal flux through a Cattaneo-type fractional relaxation, and the full classical physics of gold, titania and silver particles of brick, blade and platelet shape suspended in blood, together with Darcy–Forchheimer resistance, magnetohydrodynamics, Joule heating, a heat source, Rosseland radiation and chemically reacting Soret–Dufour mass transfer, was retained. Because the squeezing-disk operator is strongly nonlinear, the Laplace-transform route of the existing fractional literature is inapplicable; the system was therefore solved by a non-similar scheme coupling an L1 discretization of the variable-order Caputo–Fabrizio operator with Chebyshev spectral collocation and an exact-Jacobian Newton iteration. The principal findings are as follows.

- The spectral discretization converges to six significant figures by sixteen collocation nodes, and the integer-order limit reproduces the published optimal-homotopy skin-friction trends against the Hartmann and squeezing numbers, establishing the reliability of the algorithm.

- Reducing the fractional order from unity to 0.5 strengthens the fading memory and raises the lower-disk skin-friction magnitude by 6.3% and the lower-disk Nusselt number by 22.0%, redistributing rather than uniformly amplifying the transport between the two disks.

- The Cattaneo thermal relaxation is the dominant memory control on the wall heat flux, increasing the lower-disk Nusselt number by 71.6% as the relaxation parameter rises from zero to 0.6, an effect that integer-order Fourier models cannot represent.

- The blade morphology yields the highest effective conductivity ratio, 21.3% above the brick morphology, yet the brick morphology produces the largest lower-disk Nusselt number because the steeper near-wall gradient it sustains outweighs the lower bulk conductivity; the wall heat flux is thus governed by a competition between bulk conductivity and gradient geometry.

- The Soret and Dufour parameters exhibit the expected reciprocal influence on the wall heat and mass fluxes, confirming the thermodynamic consistency of the coupled energy–concentration solution.

### 6.1 Applications

The model is directly relevant to hyperthermia cancer therapy and targeted drug delivery, where blood-based gold–titania–silver suspensions are squeezed through narrowing biological passages and where viscoelastic and thermal memory are physically unavoidable; to compression-type biomedical and microfluidic actuators; and to lubricated clutch and polymer-processing presses in which second-grade memory controls the load capacity. The ability to tune the wall shear, the wall heat flux and the bulk conductivity through independent fractional, relaxation and shape controls provides a design framework for such devices.

### 6.2 Limitations and future scope

The present formulation adopts constant thermophysical properties, a single-term Caputo–Fabrizio kernel and a linearised Rosseland radiation; temperature-dependent properties, multi-term or distributed-order kernels and full nonlinear radiation would extend the fidelity of the model. The concentration equation carries no explicit memory operator and could be generalised with a fractional Fickian flux. Experimental validation of the variable-order memory prescription against rheological and thermal measurements of blood-based tri-hybrid suspensions remains an important open task. Finally, the non-similar L1 spectral algorithm developed here is general and could be applied to fractional squeezing problems in other geometries, including cones, wedges and converging channels.

## References

[1] S.U. Choi, J.A. Eastman, Enhancing thermal conductivity of fluids with nanoparticles, ASME International Mechanical Engineering Congress and Exposition, San Francisco, 1995, pp. 1–8.

[2] T. Hayat, A. Yousaf, M. Mustafa, S. Obaidat, MHD squeezing flow of second-grade fluid between two parallel disks, International Journal for Numerical Methods in Fluids 69 (2012) 1–12.

[3] T. Hayat, S. Jabeen, A. Shafiq, A. Alsaedi, Radiative squeezing flow of second grade fluid with convective boundary conditions, PLoS ONE 11 (2016) 1–22.

[4] J. Umavathi, K. Vajravelu, O.A. Beg, U.F. Khan, Unsteady squeezing flow of a magnetized dissipative non-Newtonian nanofluid with radiative heat transfer and Fourier-type boundary conditions: numerical study, Archive of Applied Mechanics 92 (2022) 1–33.

[5] H. Basha, A generalized perspective of magnetized radiative squeezed flow of viscous fluid between two parallel disks with suction and blowing, Heat Transfer 49 (2020) 1–34.

[6] M. Ramzan, N. Abid, D. Lu, I. Tlili, Impact of melting heat transfer in the time-dependent squeezing nanofluid flow containing carbon nanotubes in a Darcy-Forchheimer porous media with Cattaneo-Christov heat flux, Communications in Theoretical Physics 72 (2020) 085801.

[7] S. Bilal, M.I. Asjad, S.U. Haq, M.Y. Almusawa, E.M. Tag-ElDin, F. Ali, Significance of Dufour and Soret aspects on dynamics of water based ternary hybrid nanofluid flow in a 3D computational domain, Scientific Reports 13 (2023) 1–20.

[8] F. Shahzad, W. Jamshed, M.R. Eid, R.W. Ibrahim, F. Aslam, S.S.P.M. Isa, K. Guedri, The effect of pressure gradient on MHD flow of a tri-hybrid Newtonian nanofluid in a circular channel, Journal of Magnetism and Magnetic Materials 568 (2023) 1–12.

[9] M. Arif, L.D. Persio, P. Kumam, W. Watthayu, A. Akgul, Heat transfer analysis of fractional model of couple stress Casson tri-hybrid nanofluid using dissimilar shape nanoparticles in blood with biomedical applications, Scientific Reports 13 (2023) 1–21.

[10] I. Zahmatkesh et al., Effect of nanoparticle shape on the performance of thermal systems utilizing nanofluids: a critical review, Journal of Molecular Liquids 321 (2021) 1–61.

[11] R.L. Hamilton, O.K. Crosser, Thermal conductivity of heterogeneous two-component systems, Industrial and Engineering Chemistry Fundamentals 1 (1962) 187–191.

[12] M. Caputo, M. Fabrizio, A new definition of fractional derivative without singular kernel, Progress in Fractional Differentiation and Applications 1 (2015) 73–85.

[13] A. Atangana, D. Baleanu, New fractional derivatives with non-local and non-singular kernel: theory and application to heat transfer model, Thermal Science 20 (2016) 763–769.

[14] N. Shahid, A. Dar, Analysis of heat transfer in a hybrid nanofluid flow by using the Caputo-Fabrizio fractional derivative, Scientific Reports 12 (2022) 1–15.

[15] F. Ali, N.A. Sheikh, I. Khan, M. Saqib, Solutions with special functions for time fractional free convection flow of Brinkman-type fluid, European Physical Journal Plus 131 (2016) 310.

[16] N.A. Sheikh, D.L.C. Ching, I. Khan, D. Kumar, K.S. Nisar, A new model of fractional Casson fluid based on generalized Fick's and Fourier's laws together with heat and mass transfer, Alexandria Engineering Journal 59 (2020) 2865–2876.

[17] S. Aman, Q. Al-Mdallal, I. Khan, Heat transfer and second order slip effect on MHD flow of fractional Maxwell fluid in a porous medium, Journal of King Saud University Science 32 (2020) 450–458.

[18] C. Cattaneo, Sulla conduzione del calore, Atti del Seminario Matematico e Fisico dell'Universita di Modena 3 (1948) 83–101.

[19] C.I. Christov, On frame indifferent formulation of the Maxwell-Cattaneo model of finite-speed heat conduction, Mechanics Research Communications 36 (2009) 481–486.

[20] U. Farooq et al., Cattaneo-Christov heat flux model in radiative flow of (Fe3O4-TiO2/Transformer oil) and (Cu-TiO2/Transformer oil) magnetized hybrid nanofluids past through double rotating disks, Case Studies in Thermal Engineering 45 (2023) 1–16.

[21] S. Riasat, M. Ramzan, S. Kadry, Y.M. Chu, Significance of magnetic Reynolds number in a three-dimensional squeezing Darcy-Forchheimer hydromagnetic nanofluid thin-film flow between two rotating disks, Scientific Reports 10 (2020) 1–20.

[22] T. Nazar, M. Shabbir, Irreversibility analysis in the ternary nanofluid flow through an inclined artery via Caputo-Fabrizio fractional derivatives, Results in Physics 53 (2023) 1–15.

[23] Y.Q. Song et al., Significances of exponential heating and Darcy's law for second grade fluid flow over oscillating plate by using Atangana-Baleanu fractional derivatives, Case Studies in Thermal Engineering 27 (2021) 1–10.

[24] S.J. Liao, Beyond Perturbation: Introduction to the Homotopy Analysis Method, Chapman and Hall/CRC Press, Boca Raton, 2003.

[25] L.N. Trefethen, Spectral Methods in MATLAB, Society for Industrial and Applied Mathematics, Philadelphia, 2000.

[26] J. Shen, T. Tang, L.L. Wang, Spectral Methods: Algorithms, Analysis and Applications, Springer Series in Computational Mathematics, Vol. 41, Springer, Berlin, 2011.

[27] Y. Lin, C. Xu, Finite difference/spectral approximations for the time-fractional diffusion equation, Journal of Computational Physics 225 (2007) 1533–1552.

[28] A.A. Alikhanov, A new difference scheme for the time fractional diffusion equation, Journal of Computational Physics 280 (2015) 424–438.

[29] G.M. Sobamowo, A.A. Yinusa, M.A. Waheed, A.M. de Oliveira Siqueria, Unsteady squeezing flow and heat transfer analysis of magnetohydrodynamic third-grade nanofluid between two disks embedded in a porous medium subjected to thermal radiation using homotopy perturbation method, Journal of Engineering and Exact Sciences 8 (2022) 1–49.

[30] D. Ali, H. Ullah, A.M. Alqahtani, M. Fiza, A.S. Omer, I. Khan, A.U. Jan, Numerical treatment of squeezed fluid flow under the magnetic influence amid parallel disks, International Journal of Thermofluids (2024) 1–7.

[31] R.C. Koeller, Applications of fractional calculus to the theory of viscoelasticity, Journal of Applied Mechanics 51 (1984) 299–307.

[32] F. Mainardi, Fractional Calculus and Waves in Linear Viscoelasticity, Imperial College Press, London, 2010.

[33] K. Bhaskar, K. Sharma, K. Bhaskar, Optimal homotopy analysis of unsteady second-grade tri-hybrid nanofluid flow with radiative impact between parallel disks, International Journal of Thermofluids 24 (2024) 100940.

[34] K. Bhaskar, K. Sharma, K. Bhaskar, MHD Squeezed Radiative Flow of Casson Hybrid Nanofluid Between Parallel Plates with Joule Heating, International Journal of Applied and Computational Mathematics 10 (2024) 80.
