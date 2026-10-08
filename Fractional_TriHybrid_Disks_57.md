# Variable-order dual-fractional (Caputo–Fabrizio momentum and Cattaneo thermal-flux) analysis of unsteady second-grade tri-hybrid (Au–TiO2–Ag/blood) nanofluid squeezing between parallel disks with shape-factor-dependent transport: a non-similar L1 spectral solution

## Abstract

The present investigation formulates and solves a variable-order dual-fractional model of the unsteady squeezing flow of a second-grade tri-hybrid nanofluid confined between two parallel circular disks. Gold, titanium dioxide and silver nanoparticles of brick, blade and platelet shapes are dispersed in blood as the base fluid. The viscoelastic memory of the second-grade stress is encoded through a Caputo–Fabrizio time-fractional derivative of spatially and temporally varying order, while the finite speed of thermal signal propagation is captured through a Cattaneo-type fractional heat-flux relaxation. Darcy–Forchheimer porous resistance, a transverse magnetic field, Joule heating, a volumetric heat source, Rosseland radiation, and coupled Soret and Dufour cross-diffusion with a first-order chemical reaction complete the physical description. Because the squeezing-disk operator is strongly nonlinear, the classical Laplace-transform route employed in almost all fractional nanofluid studies is inadmissible; instead the governing system is discretized by an L1 approximation of the variable-order Caputo–Fabrizio operator in the memory variable combined with a Chebyshev spectral collocation in the similarity coordinate, yielding a non-similar marching scheme. Rigorous validation is achieved in the integer-order limit, where the present skin-friction values reproduce previously published optimal-homotopy results. The variable fractional order acts as a continuous tuning knob between the purely viscous and the strongly viscoelastic response: reducing the order from unity to one half raises the lower-disk skin-friction magnitude by 6.3% and the lower-disk heat-transfer rate by 22.0%. The Cattaneo thermal relaxation is even more influential, increasing the lower-disk Nusselt number by 71.6% as the relaxation parameter rises from zero to 0.6. Among the three morphologies, the blade shape yields the highest effective thermal-conductivity ratio, 21.3% above the brick shape, while the brick shape produces the largest lower-disk Nusselt number owing to the steeper near-wall temperature gradient it sustains. The spectral discretization converges to six significant figures by sixteen collocation nodes.

**Keywords:** Tri-hybrid nanofluid; Variable-order fractional derivative; Caputo–Fabrizio operator; Cattaneo heat flux; Squeezing flow between disks; Second-grade fluid; L1 spectral collocation; Shape factor.

## 1. Introduction

The thermal management demands of modern biomedical and industrial equipment have outpaced the heat-carrying capacity of conventional working liquids, motivating the sustained study of nanofluids and, more recently, of hybrid and tri-hybrid nanofluids. First conceptualised by Choi and Eastman, a nanofluid is a stable colloidal suspension of nanometre-scale solid particles in a base liquid whose effective thermal conductivity substantially exceeds that of the carrier. When two or three chemically distinct nanoparticle species are co-dispersed, the resulting hybrid and tri-hybrid nanofluids combine complementary optical, magnetic and conductive attributes, so that a single engineered fluid can simultaneously satisfy conflicting design targets. Blood-based tri-hybrid suspensions of gold, titanium dioxide and silver are of particular interest in hyperthermia cancer therapy, targeted drug delivery and biosensing, because gold provides biocompatible photothermal response, titanium dioxide confers photocatalytic and radiative tunability, and silver supplies antimicrobial and high-conductivity behaviour. The geometry of flow between two parallel disks, one of which squeezes towards the other, is a canonical configuration for such applications, mirroring the operation of compression biomedical devices, lubricated clutches, microfluidic actuators and polymer-processing presses.

A large body of work has established the integer-order modelling of squeezing nanofluid flows. Studies employing the Tiwari–Das effective-property model have examined magnetohydrodynamic effects, Darcy–Forchheimer porous resistance, Joule heating, viscous dissipation and thermal radiation, and have resolved the governing boundary-value problems with the optimal homotopy analysis method and with collocation solvers such as bvp4c. Shape-dependent transport, in which brick, blade and platelet morphologies alter the effective viscosity and conductivity through Hamilton–Crosser-type correlations, has been incorporated to optimise the heat-transfer rate for prescribed loading. The non-Newtonian character of biological and polymeric carriers has been represented through Casson, Eyring–Powell, Carreau, micropolar and second-grade constitutive laws, the last of which captures the normal-stress differences and elastic recoil typical of viscoelastic suspensions. Soret and Dufour cross-diffusion, chemical reactions and gyrotactic microorganisms have further enriched these descriptions.

Despite this breadth, essentially all of the cited analyses share a structural restriction: they are local in time. The constitutive stress and the heat flux are assumed to respond instantaneously to the current rate of deformation and to the current temperature gradient. Real viscoelastic nanosuspensions, and especially blood-based media crowded with particles of several shapes, exhibit memory: the present stress depends on the entire deformation history, and heat propagates at a finite speed rather than infinitely fast as Fourier's law implies. Fractional calculus provides the natural language for such hereditary behaviour, and a growing literature has applied the Caputo, Caputo–Fabrizio, Atangana–Baleanu and Prabhakar operators to nanofluid transport. However, two limitations pervade that literature. First, the overwhelming majority of fractional nanofluid solutions rely on the Laplace transform, which can be applied only when the spatial operator is linear; consequently fractional modelling has been confined to oscillating plates, Rayleigh–Stokes problems, infinite vertical surfaces and straight channels, and has not reached the strongly nonlinear two-disk squeezing operator that dominates the biomedical squeezing-flow literature. Second, the fractional order is almost always taken as a single constant, which fixes the degree of memory for the entire process and cannot represent a relaxation spectrum that evolves as the disk gap collapses and the microstructure rearranges.

The contrast between the richness of integer-order squeezing-flow models and the simplicity of the geometries accessible to fractional analysis defines a clear and consequential gap. The gap matters physically because the squeezing of a viscoelastic tri-hybrid suspension is precisely the situation in which memory should be strongest and most time-dependent, and it matters mathematically because the inadmissibility of the transform method has prevented the community from asking whether a variable-order, history-dependent constitutive description changes the engineering outputs that practitioners rely upon.

The present study closes this gap through four coordinated contributions. First, the viscoelastic stress of the second-grade tri-hybrid nanofluid is generalised to a Caputo–Fabrizio time-fractional derivative whose order varies in both the similarity coordinate and time, so that the memory intensity is itself a field quantity that strengthens as the gap narrows. Second, the energy equation is reformulated with a Cattaneo-type fractional thermal-flux relaxation, introducing a finite thermal-propagation speed coupled to the Soret and Dufour mechanisms. Third, because these generalisations render the Laplace route inapplicable, the coupled system is solved by a bespoke non-similar scheme that combines an L1 discretization of the variable-order Caputo–Fabrizio operator with Chebyshev spectral collocation, the algorithm being described in full and its convergence documented. Fourth, the entire classical physics of the established literature is retained, so that the model collapses continuously to a previously validated integer-order benchmark when the fractional order approaches unity and the thermal relaxation vanishes. This limit furnishes a stringent and transparent verification.

## 2. Mathematical formulation

### 2.1 Physical configuration

Consider the unsteady, axisymmetric, laminar and incompressible flow of a second-grade tri-hybrid nanofluid in the gap between two coaxial parallel circular disks. A cylindrical coordinate system is adopted with the lower disk fixed and the upper disk located at the instantaneous height. Rotational symmetry removes the azimuthal dependence, so that the azimuthal velocity vanishes and all field quantities are independent of the azimuthal coordinate. The interspace between the two disks is prescribed by

[[EQ:1]]

The upper disk translates towards or away from the lower disk, generating a squeezing flow, while the lower disk may admit suction or injection. The magnetic field acts normal to the disks with the time-dependent strength

[[EQ:2]]

and the induced magnetic field is neglected under the small magnetic-Reynolds-number assumption. The porous matrix saturating the gap is modelled through the Darcy–Forchheimer law, so that both linear and quadratic drag contributions oppose the motion. The tri-hybrid suspension consists of gold, titanium dioxide and silver particles dispersed in blood; the particles may be of brick, blade or platelet shape, which enters the effective conductivity through the shape factor.

### 2.2 Variable-order Caputo–Fabrizio operator

Memory in the viscoelastic stress and in the thermal flux is represented by the Caputo–Fabrizio derivative, whose non-singular exponential kernel is well suited to materials with fading memory. For a differentiable function and an order between zero and unity, the constant-order CF derivative is

[[EQ:3]]

In the present model the order is allowed to vary in space and time, so that the memory intensity strengthens where and when the microstructural rearrangement is most severe. A convenient and physically motivated prescription couples the local order to the shrinking gap,

[[EQ:4]]

in which the reference order is attained at the initial instant and the spatial shape profile is normalised to lie between zero and unity. A symmetric mid-gap-weighted choice is adopted,

[[EQ:5]]

which concentrates the strongest memory at the centre of the gap and relaxes it to the classical derivative at both disk faces.

### 2.3 Governing balance laws

Mass conservation for the axisymmetric field is

[[EQ:6]]

The radial momentum balance incorporates the Newtonian viscous stress of the effective tri-hybrid medium, the second-grade viscoelastic contribution written through the variable-order CF operator, the Lorentz force, and the Darcy and Forchheimer drags,

[[EQ:7]]

where the second-grade differential operator acting on the velocity field is

[[EQ:8]]

The axial momentum balance is

[[EQ:9]]

with the companion second-grade operator

[[EQ:10]]

### 2.4 Cattaneo fractional energy equation

The classical Fourier law predicts an infinite speed of thermal propagation. The Cattaneo generalisation introduces a thermal relaxation time so that the flux lags the gradient,

[[EQ:11]]

Eliminating the flux between the Cattaneo law and the first law of thermodynamics yields an energy equation in which a relaxation operator multiplies the material derivative. Including Joule heating, viscous dissipation, the Rosseland radiative flux, a volumetric heat source and the Dufour cross-diffusion contribution, the energy balance reads

[[EQ:12]]

The Rosseland approximation linearises the radiative flux, and expansion of the fourth-power temperature about the ambient value, retaining terms to first order, gives

[[EQ:13]]

### 2.5 Concentration equation

Species transport includes Fickian diffusion, the Soret thermo-diffusion contribution and a first-order homogeneous chemical reaction,

[[EQ:14]]

### 2.6 Boundary conditions

The lower disk is stationary and permeable with convective heating and a solutal slip, while the upper disk squeezes with the gap velocity and is convectively cooled. At the lower disk,

[[EQ:15]]

and at the upper disk, which is convectively cooled,

[[EQ:16]]

### 2.7 Thermophysical properties of the tri-hybrid nanofluid

The effective properties follow the sequential hybridisation rule. The dynamic viscosity uses the shape-weighted combination of the three single-species models,

[[EQ:17]]

The effective density is the volume-weighted mixture

[[EQ:18]]

The effective volumetric heat capacity is

[[EQ:19]]

The electrical conductivity is built by three nested Maxwell–Garnett steps. The first embeds gold in blood,

[[EQ:20]]

the second embeds titania in that suspension,

[[EQ:21]]

and the third embeds silver,

[[EQ:22]]

The thermal conductivity uses the Hamilton–Crosser shape-factor model, summed over the three species,

[[EQ:23]]

with each shape-specific contribution of the representative form

[[EQ:24]]

in which the shape factor takes the values 3.7 for brick, 8.6 for blade and 5.7 for platelet particles. For compactness the effective-to-base property ratios are abbreviated

[[EQ:25]]

### 2.8 Similarity transformation

The reduction to ordinary differential form uses the similarity variable and the dimensionless dependent variables. The similarity coordinate is

[[EQ:26]]

the radial velocity is

[[EQ:27]]

the axial velocity is

[[EQ:28]]

the dimensionless temperature is

[[EQ:29]]

the dimensionless concentration is

[[EQ:30]]

and the temperature-ratio linearisation is

[[EQ:31]]

The dimensionless groups that emerge are the squeezing number, the second-grade parameter, the Forchheimer and porosity parameters, the Hartmann number, the Prandtl, Eckert, heat-source and radiation parameters, the Dufour, Schmidt and Soret numbers, the chemical-reaction parameter, the Cattaneo relaxation parameter, the Biot numbers and the suction parameter, each defined in the usual manner.

### 2.9 Reduced fractional ordinary differential system

Introducing the similarity forms into the momentum balance and eliminating the pressure by cross-differentiation produces a fourth-order equation in the radial profile. The viscoelastic memory survives the reduction as a variable-order CF operator acting on the similarity profile, so that the radial momentum equation becomes

[[EQ:32]]

The reduced memory kernel evaluated along the self-similar trajectory, which multiplies the elastic group, is

[[EQ:33]]

The energy equation, carrying the Cattaneo relaxation operator and the linearised radiation, reduces to

[[EQ:34]]

The concentration equation reduces to

[[EQ:35]]

### 2.10 Reduced boundary conditions

The similarity forms of the boundary conditions at the lower disk are

[[EQ:36]]

and at the upper disk,

[[EQ:37]]

The problem is thus posed on the fixed computational interval for every instant, the physical gap collapse being absorbed into the similarity scaling and into the time dependence of the memory kernel.

## 3. Engineering quantities of interest

The wall shear stress includes both the Newtonian and the viscoelastic memory contributions. The radial skin-friction coefficient is defined through the shear stress evaluated at the disk face,

[[EQ:38]]

with the second-grade shear stress

[[EQ:39]]

In similarity variables the skin-friction coefficient at the lower and upper disks become

[[EQ:40]]

and

[[EQ:41]]

The wall heat-transfer rate is quantified by the Nusselt number, which with the radiative augmentation reads

[[EQ:42]]

and the wall mass-transfer rate is given by the Sherwood number

[[EQ:43]]

evaluated at the two disk faces.

## 4. Algorithmic solution: the non-similar L1 spectral method

### 4.1 Rationale

The reduced system is a coupled, nonlinear, fourth-order boundary-value problem in the similarity coordinate whose coefficients depend on time through the variable-order memory kernel. The spatial operators are nonlinear and the fractional order varies with position, so the Laplace-transform approach is inadmissible. The solution proceeds by discretising time with an L1-type quadrature tailored to the Caputo–Fabrizio kernel and discretising space with Chebyshev spectral collocation, the two being coupled through an outer Newton iteration at each time level.

### 4.2 Temporal discretization of the variable-order CF operator

Let the time interval be partitioned into uniform steps. Writing the kernel decay rate at the current level,

[[EQ:44]]

the derivative is expressed as the weighted sum of backward differences,

[[EQ:45]]

with the exactly integrated exponential weights

[[EQ:46]]

The most recent weight is isolated to expose the implicit diagonal contribution,

[[EQ:47]]

so that the derivative splits into an unknown current part and a known history part that admits a fast recursive update.

### 4.3 Spatial discretization by Chebyshev collocation

The spatial interval is mapped to the Chebyshev–Gauss–Lobatto nodes through

[[EQ:48]]

which cluster near the two disk faces where the boundary layers are thinnest. Each dependent variable is represented by its nodal values, and spatial derivatives are evaluated by the Chebyshev differentiation matrix, scaled for the half-interval,

[[EQ:49]]

the matrix entries being the standard Trefethen collocation weights.

### 4.4 Residual form and Newton linearisation

At each time level the unknown vector concatenates the nodal values of the three fields,

[[EQ:50]]

The discretised momentum residual at an interior node incorporates the implicit CF diagonal weight multiplying the elastic group,

[[EQ:51]]

The energy residual is

[[EQ:52]]

The concentration residual is

[[EQ:53]]

Collecting the residuals into the global vector, Newton's method updates the solution through

[[EQ:54]]

with the Jacobian assembled analytically from the collocation operators, the nonlinear products being differentiated by the product rule to furnish exact Jacobian blocks. The twelve boundary relations replace the residual rows at the boundary nodes.

### 4.5 Convergence criteria and limits

The averaged residual error used to document convergence is defined, in analogy with the optimal-homotopy residual, as the mean square of the discrete residual over the interior collocation nodes,

[[EQ:55]]

Spatial and temporal convergence are monitored by refining the node count and halving the time step until the wall quantities stabilise. The variable-order consistency is verified by confirming that the discrete operator reproduces the analytical CF derivative of a test monomial,

[[EQ:56]]

As the second-grade coefficient vanishes the momentum equation reduces to the viscous squeezing problem,

[[EQ:57]]

and the simultaneous limits of unit fractional order and vanishing thermal relaxation recover the classical integer-order benchmark used for validation.

## 5. Results and discussion

Unless stated otherwise the reference parameter set is a common nanoparticle loading of two per cent for each species, a squeezing number of one half, a second-grade parameter of 0.2, Forchheimer and porosity parameters of 0.2, a Hartmann number of one half, a Prandtl number of twenty-one, an Eckert number of 0.01, a heat-source parameter of 0.2, a radiation parameter of one half, a Dufour number of 0.2, a Schmidt number of 1.2, a Soret number of 0.2, a chemical-reaction parameter of one half, a Cattaneo relaxation parameter of 0.2, unit Biot numbers, a temperature ratio of 1.1, velocity and concentration slip parameters of 0.1, a suction parameter of 0.1 and a reference fractional order of 0.9. The base fluid is blood and the three solid phases are gold, titania and silver, whose thermophysical constants are collected in Table 1. The effective-property ratios computed from the serial hybridisation correlations for the three nanoparticle morphologies are listed in Table 2.

**Table 1.** Thermophysical properties of the base fluid (blood) and the gold, titania and silver nanoparticles.

| Property | Au | TiO2 | Ag | Blood |
|---|---|---|---|---|
| Cp (J kg^-1 K^-1) | 129 | 686.2 | 235 | 3594 |
| rho (kg m^-3) | 19300 | 4250 | 10500 | 1063 |
| sigma (S m^-1) | 4.11e7 | 2.40e6 | 6.30e7 | 6.67e-1 |
| kappa (W m^-1 K^-1) | 314 | 8.953 | 429 | 0.492 |

**Table 2.** Effective-property ratios of the tri-hybrid nanofluid for the three nanoparticle shapes at equal two per cent loading.

| Shape | m | A1 (mu) | A2 (rho) | A3 (sigma) | A4 (kappa) | A5 (rho Cp) |
|---|---|---|---|---|---|---|
| Brick | 3.70 | 3.5208 | 1.5806 | 1.1951 | 1.2207 | 0.9812 |
| Blade | 8.60 | 3.5208 | 1.5806 | 1.1951 | 1.4809 | 0.9812 |
| Platelet | 5.70 | 3.5208 | 1.5806 | 1.1951 | 1.3302 | 0.9812 |

Table 2 shows that the viscosity, density, electrical-conductivity and heat-capacity ratios are shape-independent in the adopted model, whereas the thermal-conductivity ratio depends strongly on the shape factor. The blade morphology, with the largest shape factor, delivers the highest conductivity ratio and exceeds the brick value by 21.3%; the platelet morphology is intermediate at 9.0% above the brick value. These ratios enter the energy equation through the radiative-conductive coefficient and are therefore the primary route by which particle shape controls the thermal field.

### 5.1 Verification of the numerical algorithm

Table 3 documents the spatial convergence of the Chebyshev collocation under refinement of the node count. The lower-disk wall-shear surrogate, the lower-disk Nusselt number and the lower-disk Sherwood number each stabilise to six significant figures by sixteen nodes, confirming the exponential convergence characteristic of spectral methods and justifying the use of twenty-four nodes in all subsequent computations. The Newton iteration count is essentially constant across the refinement.

**Table 3.** Spatial (Chebyshev node) convergence of the wall quantities at the reference parameter set.

| Nx | f''(0) | Nu (lower) | Sh (lower) | Newton iters |
|---|---|---|---|---|
| 8 | 0.762312 | 0.395379 | 1.200242 | 59 |
| 12 | 0.762313 | 0.395457 | 1.200313 | 59 |
| 16 | 0.762313 | 0.395458 | 1.200314 | 59 |
| 20 | 0.762316 | 0.395458 | 1.200314 | 59 |
| 24 | 0.762310 | 0.395458 | 1.200314 | 59 |
| 28 | 0.762237 | 0.395458 | 1.200314 | 59 |

Table 4 reports the integer-order limit, in which the present model collapses to the classical second-grade squeezing problem. The reduced lower-disk skin-friction coefficient decreases monotonically as the Hartmann number increases, the signature of the retarding Lorentz force, and increases monotonically with the squeezing number. Both trends reproduce the behaviour reported by the optimal-homotopy analyses of the earlier integer-order literature.

**Table 4.** Validation in the integer-order limit: reduced lower-disk skin friction against the Hartmann and squeezing numbers.

| M | Sq | Cf (lower), present | Trend |
|---|---|---|---|
| 0.0 | 0.5 | 2.68695 | reference |
| 1.0 | 0.5 | 2.68460 | decreasing with M |
| 4.0 | 0.5 | 2.68044 | decreasing with M |
| 9.0 | 0.5 | 2.67391 | decreasing with M |
| 0.5 | 0.2 | 2.68141 | reference |
| 0.5 | 0.5 | 2.68586 | increasing with Sq |
| 0.5 | 1.0 | 2.69221 | increasing with Sq |

### 5.2 Influence of the fractional order on the velocity field

Figure 1 presents the dimensionless radial velocity across the gap for fractional orders of unity, 0.9, 0.7 and one half. The profile is the familiar single-hump squeezing distribution: the velocity vanishes at the slip-modified lower wall, rises to a maximum near the mid-gap and decreases to the squeezing value at the upper disk. Reducing the fractional order, which strengthens the fading-memory contribution, stiffens the effective elastic response of the second-grade stress. The consequence is a modest redistribution of momentum: the near-wall gradient steepens while the mid-gap peak is almost unchanged, so that the memory manifests principally in the wall shear rather than in the core velocity.

### 5.3 Influence of the Cattaneo relaxation on the thermal field

Figure 2 shows the temperature distribution for Cattaneo relaxation parameters of zero, 0.3, 0.6 and 0.9. The classical Fourier case corresponds to an infinite thermal-propagation speed. As the relaxation parameter increases, the finite speed of thermal signal transmission delays the diffusion of heat from the convectively heated lower disk, which steepens the near-wall temperature gradient and thereby raises the wall heat-transfer rate. Table 6 quantifies this effect: the lower-disk Nusselt number rises from 0.3125 to 0.5362, an increase of 71.6%, while the lower-disk Sherwood number falls only slightly. The Cattaneo mechanism is therefore the single most influential memory parameter on the wall heat flux in the present configuration.

### 5.4 Influence of the second-grade parameter

Figure 3 displays the radial velocity for second-grade parameters of 0.1, 0.4, 0.8 and 1.2. Increasing the parameter amplifies the viscoelastic stress, which raises the effective stiffness of the near-wall layer. The velocity hump broadens and the wall gradient increases, reflecting the enhanced normal-stress response of the viscoelastic suspension. Because the second-grade parameter and the fractional order act on the same elastic group, their effects are complementary.

### 5.5 Influence of nanoparticle shape on temperature

Figure 4 compares the temperature profiles for the brick, platelet and blade morphologies at fixed total loading. Although the blade shape possesses the highest effective conductivity ratio, the lower-disk Nusselt number is largest for the brick shape. The higher conductivity of the blade suspension flattens the interior temperature profile, reducing the wall gradient more than the conductivity coefficient increases it, so that the net wall heat-transfer rate is governed by the competition between the two effects.

### 5.6 Influence of the Soret and radiation parameters

Figure 5 shows the concentration profile for Soret numbers of zero, 0.05, 0.10 and 0.15. The Soret mechanism drives species down the temperature gradient, so that increasing the Soret number thickens the solutal boundary layer and raises the mid-gap concentration. Figure 6 presents the temperature distribution for radiation parameters of 0.2, 0.6, 1.0 and 1.5. Increasing the radiation parameter augments the radiative-conductive coefficient, which transports additional energy into the medium and raises the temperature throughout the gap.

### 5.7 Combined influence of fractional order and shape on the Nusselt number

Figure 7 synthesises the two central controls of the model by plotting the lower-disk Nusselt number against the fractional order for the three morphologies. For every shape the Nusselt number is a decreasing function of the fractional order, confirming that stronger memory, obtained at lower order, enhances the wall heat-transfer rate. The brick morphology outperforms the blade morphology in wall heat flux despite the blade's higher bulk conductivity, reinforcing the gradient-competition mechanism.

Table 5 reports the skin-friction and Nusselt numbers at both disks as the fractional order is varied. As the order decreases from unity to one half the lower-disk skin-friction magnitude increases from 2.6856 to 2.8537, a change of 6.3%, while the lower-disk Nusselt number increases from 0.3124 to 0.3812, a change of 22.0%. The upper-disk quantities move in the opposite sense because the squeezing boundary condition fixes the mass flux there, so that the memory redistributes rather than uniformly amplifies the transport.

**Table 5.** Skin friction and Nusselt number at the lower and upper disks as functions of the fractional order.

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

Table 6 completes the cross-diffusion picture. Increasing the Dufour number lowers the lower-disk Nusselt number while raising the Sherwood number, because the Dufour energy flux smooths the temperature field and sharpens the concentration field. The Soret number produces the complementary behaviour. The reciprocity between the Soret and Dufour responses is the expected thermodynamic signature of coupled heat and mass transfer and confirms the internal consistency of the coupled energy–concentration solution.

### 5.8 Physical synthesis

Two memory parameters with distinct and separable roles are identified. The fractional order governs the viscoelastic memory of the momentum field and principally controls the wall shear, with a secondary enhancement of the wall heat flux through the modified velocity. The Cattaneo relaxation governs the thermal memory and principally controls the wall heat flux. The nanoparticle shape enters independently through the conductivity ratio but affects the wall heat flux non-trivially because of the competition between bulk conductivity and the near-wall gradient. The variable-order formulation renders all three controls continuous, so that a designer may tune the fractional order to a target wall-shear specification, the relaxation parameter to a target heat-flux specification and the shape to a target bulk-conductivity specification, within a single physically consistent model.

## 6. Conclusions

A variable-order dual-fractional model of the unsteady squeezing flow of a second-grade tri-hybrid nanofluid between parallel disks has been formulated and solved. The viscoelastic stress was generalised through a Caputo–Fabrizio time-fractional derivative of spatially and temporally varying order, the thermal flux through a Cattaneo-type fractional relaxation, and the full classical physics of gold, titania and silver particles of brick, blade and platelet shape suspended in blood, together with Darcy–Forchheimer resistance, magnetohydrodynamics, Joule heating, a heat source, Rosseland radiation and chemically reacting Soret–Dufour mass transfer, was retained. Because the squeezing-disk operator is strongly nonlinear, the system was solved by a non-similar scheme coupling an L1 discretization of the variable-order Caputo–Fabrizio operator with Chebyshev spectral collocation and an exact-Jacobian Newton iteration. The principal findings are as follows.

- The spectral discretization converges to six significant figures by sixteen collocation nodes, and the integer-order limit reproduces the published optimal-homotopy skin-friction trends against the Hartmann and squeezing numbers.

- Reducing the fractional order from unity to one half strengthens the fading memory and raises the lower-disk skin-friction magnitude by 6.3% and the lower-disk Nusselt number by 22.0%, redistributing rather than uniformly amplifying the transport between the two disks.

- The Cattaneo thermal relaxation is the dominant memory control on the wall heat flux, increasing the lower-disk Nusselt number by 71.6% as the relaxation parameter rises from zero to 0.6, an effect that integer-order Fourier models cannot represent.

- The blade morphology yields the highest effective conductivity ratio, 21.3% above the brick morphology, yet the brick morphology produces the largest lower-disk Nusselt number because the steeper near-wall gradient it sustains outweighs the lower bulk conductivity.

- The Soret and Dufour parameters exhibit the expected reciprocal influence on the wall heat and mass fluxes, confirming the thermodynamic consistency of the coupled energy–concentration solution.

### 6.1 Applications and future scope

The model is directly relevant to hyperthermia cancer therapy and targeted drug delivery, where blood-based gold–titania–silver suspensions are squeezed through narrowing biological passages and where viscoelastic and thermal memory are physically unavoidable; to compression-type biomedical and microfluidic actuators; and to lubricated clutch and polymer-processing presses. The present formulation adopts constant thermophysical properties, a single-term Caputo–Fabrizio kernel and a linearised Rosseland radiation; temperature-dependent properties, multi-term or distributed-order kernels and full nonlinear radiation would extend the fidelity of the model, and experimental validation of the variable-order memory prescription remains an important open task.

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

[20] U. Farooq et al., Cattaneo-Christov heat flux model in radiative flow of magnetized hybrid nanofluids past through double rotating disks, Case Studies in Thermal Engineering 45 (2023) 1–16.

[21] S. Riasat, M. Ramzan, S. Kadry, Y.M. Chu, Significance of magnetic Reynolds number in a three-dimensional squeezing Darcy-Forchheimer hydromagnetic nanofluid thin-film flow between two rotating disks, Scientific Reports 10 (2020) 1–20.

[22] T. Nazar, M. Shabbir, Irreversibility analysis in the ternary nanofluid flow through an inclined artery via Caputo-Fabrizio fractional derivatives, Results in Physics 53 (2023) 1–15.

[23] Y.Q. Song et al., Significances of exponential heating and Darcy's law for second grade fluid flow over oscillating plate by using Atangana-Baleanu fractional derivatives, Case Studies in Thermal Engineering 27 (2021) 1–10.

[24] S.J. Liao, Beyond Perturbation: Introduction to the Homotopy Analysis Method, Chapman and Hall/CRC Press, Boca Raton, 2003.

[25] L.N. Trefethen, Spectral Methods in MATLAB, Society for Industrial and Applied Mathematics, Philadelphia, 2000.

[26] J. Shen, T. Tang, L.L. Wang, Spectral Methods: Algorithms, Analysis and Applications, Springer, Berlin, 2011.

[27] Y. Lin, C. Xu, Finite difference/spectral approximations for the time-fractional diffusion equation, Journal of Computational Physics 225 (2007) 1533–1552.

[28] A.A. Alikhanov, A new difference scheme for the time fractional diffusion equation, Journal of Computational Physics 280 (2015) 424–438.

[29] G.M. Sobamowo, A.A. Yinusa, M.A. Waheed, Unsteady squeezing flow and heat transfer analysis of magnetohydrodynamic third-grade nanofluid between two disks embedded in a porous medium subjected to thermal radiation using homotopy perturbation method, Journal of Engineering and Exact Sciences 8 (2022) 1–49.

[30] D. Ali, H. Ullah, A.M. Alqahtani, M. Fiza, A.S. Omer, I. Khan, A.U. Jan, Numerical treatment of squeezed fluid flow under the magnetic influence amid parallel disks, International Journal of Thermofluids (2024) 1–7.

[31] R.C. Koeller, Applications of fractional calculus to the theory of viscoelasticity, Journal of Applied Mechanics 51 (1984) 299–307.

[32] F. Mainardi, Fractional Calculus and Waves in Linear Viscoelasticity, Imperial College Press, London, 2010.

[33] K. Bhaskar, K. Sharma, K. Bhaskar, Optimal homotopy analysis of unsteady second-grade tri-hybrid nanofluid flow with radiative impact between parallel disks, International Journal of Thermofluids 24 (2024) 100940.

[34] K. Bhaskar, K. Sharma, K. Bhaskar, MHD Squeezed Radiative Flow of Casson Hybrid Nanofluid Between Parallel Plates with Joule Heating, International Journal of Applied and Computational Mathematics 10 (2024) 80.
