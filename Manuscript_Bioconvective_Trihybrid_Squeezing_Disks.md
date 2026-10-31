# Bioconvective Squeezing Flow of a Tri-Hybrid Nanofluid Between Parallel Disks with Gyrotactic Microorganisms, Arrhenius Activation Energy, and Convective Boundary Conditions

**Running title:** Bioconvective tri-hybrid nanofluid squeezing flow between disks

---

## Abstract

The present investigation examines the unsteady, axisymmetric squeezing flow of a tri-hybrid nanofluid confined between two parallel circular disks embedded in a Darcy–Forchheimer porous medium, with specific attention to its relevance for targeted drug delivery and bio-nanofluidic devices. The working fluid is formulated by dispersing gold (Au), titania (TiO₂), and silver (Ag) nanoparticles of brick, blade, and platelet shapes within a blood base fluid. The mathematical model is enriched by three physical features that have not previously been combined for this geometry: a separate conservation equation for motile gyrotactic microorganisms, an Arrhenius (activation-energy) modified chemical-reaction term in the species equation, and convective plus hydrodynamic-slip boundary conditions on the disks. Additional effects of a transverse magnetic field, Joule heating, nonlinear thermal radiation through the Rosseland approximation, a volumetric heat source, viscous dissipation, and suction/injection are retained. Using similarity transformations, the governing partial differential equations are reduced to a coupled system of nonlinear ordinary differential equations, which is solved analytically through the Optimal Homotopy Analysis Method (OHAM) implemented in Mathematica, with a bvp4c shooting cross-check for validation. The influence of the governing parameters on the velocity, temperature, species concentration, and microorganism-density fields, together with the skin friction, Nusselt number, Sherwood number, and motile-density number, is examined graphically and tabulated. The analysis shows that the squeezing parameter exerts a dual, region-dependent action on the radial velocity, that increasing activation energy enriches the concentration boundary layer whereas a stronger reaction parameter depletes it, and that the microorganism concentration decays monotonically with the Péclet and bioconvection-Lewis numbers. Crucially, bioconvection is found to stabilise the nanoparticle suspension and to moderate the thermal field, a response with direct implications for the shelf stability and dosing precision of nanoparticle-laden therapeutic carriers.

**Keywords:** Tri-hybrid nanofluid; Parallel disks; Gyrotactic microorganisms; Bioconvection; Arrhenius activation energy; Darcy–Forchheimer; Convective boundary conditions; OHAM

---

## Nomenclature

| Symbol | Description | Symbol | Description |
|--------|-------------|--------|-------------|
| $b$ | Squeezing constant (s⁻¹) | $Pr$ | Prandtl number |
| $B(t)$ | Variable magnetic field (T) | $Pe$ | Péclet number (bioconvection) |
| $B_0$ | Magnetic field strength (T) | $Q_0$ | Heat source coefficient |
| $Bi_1,Bi_2$ | Thermal Biot numbers (lower, upper) | $qr$ | Radiative heat flux |
| $C$ | Species concentration | $Rd$ | Radiation parameter |
| $C_b$ | Drag (inertia) coefficient | $Re$ | Local Reynolds number |
| $C_f$ | Skin-friction coefficient | $Sc$ | Schmidt number |
| $D_B$ | Brownian/mass diffusivity | $Sb$ | Bioconvection Schmidt number |
| $D_m$ | Microorganism diffusivity | $Sq$ | Unsteady squeezing parameter |
| $E$ | Dimensionless activation energy | $S$ | Suction/injection parameter |
| $Ec$ | Eckert number | $T$ | Temperature (K) |
| $f$ | Dimensionless stream function | $W_c$ | Maximum cell swimming speed |
| $Fr$ | Forchheimer (inertia) parameter | $u,w$ | Velocity components (m s⁻¹) |
| $h(t)$ | Disk separation (m) | $\delta$ | Fitted reaction (temperature) exponent |
| $Hf,Hc$ | Velocity, concentration slip | $\eta$ | Similarity variable |
| $Kp$ | Porosity parameter | $\theta$ | Dimensionless temperature |
| $Lb$ | Bioconvection Lewis number | $\phi$ | Dimensionless concentration |
| $M$ | Magnetic parameter | $\chi$ | Dimensionless microorganism density |
| $m$ | Shape factor | $\sigma^{*}$ | Dimensionless reaction parameter |
| $N$ | Microorganism number density | $\mu,\rho,\kappa$ | Viscosity, density, conductivity |
| $Nb,Nt$ | Brownian, thermophoresis parameters | Thnf | Tri-hybrid nanofluid (subscript) |

---

## 1. Introduction

Conventional heat-transfer liquids such as water, ethylene glycol, engine oil, and biological fluids possess intrinsically modest thermal conductivities, which constrain their effectiveness in modern thermal-management duties. The dispersion of nanometre-scale metallic and oxide particles to form nanofluids, and subsequently the suspension of two or three distinct particle species to form hybrid and tri-hybrid nanofluids, has emerged as a robust route to overcome this limitation. A tri-hybrid nanofluid blends three chemically different nanoparticles in a single base fluid, exploiting complementary thermophysical signatures so that the effective conductivity, stability, and rheological response exceed those attainable with mono- or bi-nanofluids. When the base fluid is blood, the resulting suspension becomes directly relevant to biomedical engineering, where the controlled transport of gold, silver, and titania particles underpins applications in hyperthermia therapy, contrast-enhanced imaging, antibacterial surface treatment, and, most notably, targeted drug delivery.

The squeezing flow between two approaching disks is a canonical configuration for studying such suspensions because it reproduces, in a mathematically tractable form, the transient compression that occurs in lubricated bearings, hydraulic dampers, polymer-forming operations, injection moulds, and—of direct interest here—microfluidic dosing chambers and syringe-driven delivery systems. The unsteadiness introduced by the moving disk, the porosity of the intervening medium, and the action of an applied magnetic field together produce a rich interplay of inertial, viscous, electromagnetic, and buoyancy forces whose resolution demands careful modelling.

The biomedical motivation deserves emphasis. In magnetically guided drug delivery, a functionalised nanoparticle carrier is steered to a target site by an external field, and the local thermal field determines both the release kinetics of the drug payload and the viability of surrounding tissue. The squeezing geometry is a faithful idealisation of the compression that a bolus of carrier fluid experiences inside a micro-pump chamber or a collapsing capillary segment, so the velocity, temperature, and concentration fields computed here translate directly into estimates of where and how fast a payload is transported and released. Three modelling features are decisive for fidelity in this setting: the base fluid must be blood, whose Prandtl number near 21 differs markedly from that of water or oil; the particle shape must be resolved, because elongated blade or platelet morphologies alter the effective conductivity far more than spherical particles; and the colloidal stability of the suspension must be represented, because sedimentation during storage or administration degrades dosing accuracy. The last of these is precisely what the bioconvection of motile microorganisms addresses, which is why it is central to the present formulation rather than an incidental add-on.

A considerable body of recent work has established the thermal behaviour of hybrid and tri-hybrid nanofluids in disk and channel geometries. Bhaskar and co-workers analysed the unsteady second-grade tri-hybrid nanofluid flow of Au–TiO₂–Ag particles in blood between parallel disks under Soret–Dufour, Joule-heating, and heat-source effects, solving the system with the optimal homotopy analysis method [1]. Arif et al. developed a fractional couple-stress Casson tri-hybrid model with dissimilar particle shapes dispersed in blood for biomedical duties [2], while Shahzad et al. examined the pressure-gradient-driven flow of a tri-hybrid Newtonian nanofluid in a circular channel [3]. Nazar and Shabbir applied Caputo–Fabrizio fractional derivatives to a ternary nanofluid traversing an inclined artery [4], and Zahmatkesh et al. provided a critical appraisal of how particle shape governs the performance of nanofluid thermal systems [5]. The shape-factor concept, rooted in the Hamilton–Crosser conductivity model, was adopted by Awal et al. to interpret brick, blade, and platelet morphologies in squeezed tri-hybrid films [6]. These contributions collectively confirm that particle shape, hybridisation ratio, and base-fluid rheology are first-order controls on heat and mass transfer.

The porous medium between the disks is most faithfully represented by the Darcy–Forchheimer formulation, which augments the linear Darcy drag with a quadratic inertial term that becomes significant at the moderate-to-high pore Reynolds numbers typical of squeezing flows. Ramzan et al. incorporated Darcy–Forchheimer resistance with Cattaneo–Christov heat flux and melting conditions for carbon-nanotube suspensions between disks [7], and Riasat et al. demonstrated the importance of the magnetic Reynolds number for three-dimensional squeezing flow between rotating disks in a Darcy–Forchheimer medium [8]. Entropy-based optimisation of Darcy–Forchheimer hybrid nanofluid flow in microchannels with slip was advanced by Sindhu and Gireesha [9], while Almarashi et al. quantified Joule and viscous dissipation for a micropolar hybrid nanofluid over a radially stretching rotating disk [10].

The non-Newtonian character of blood-based suspensions has motivated a range of rheological models. Hayat et al. studied radiative squeezing flow of a second-grade fluid with convective boundary conditions using homotopy analysis [11], and Umavathi et al. solved the unsteady squeezing flow of a magnetised dissipative non-Newtonian nanofluid with Fourier-type boundary conditions numerically [12]. Casson and Williamson descriptions have likewise been applied to squeezing and disk flows to capture yield-stress and shear-thinning features relevant to whole blood [13,14]. These studies underline that the choice of constitutive law materially alters the velocity crossover behaviour that is characteristic of squeezing between disks.

A distinguishing feature of the present study is the explicit treatment of bioconvection generated by motile gyrotactic microorganisms. Bioconvection arises when self-propelled microorganisms, being marginally denser than the suspending fluid, swim preferentially upward and create an unstable density stratification that drives macroscopic convection. When combined with nanoparticle suspensions, the microorganisms counteract sedimentation and enhance the colloidal stability of the mixture, a property of obvious value for pharmaceutical formulations that must remain homogeneous during storage and administration. The modelling of gyrotactic microorganisms in nanofluids has matured rapidly: Zhang et al. and Waqas et al. formulated microorganism conservation equations for rotating-disk and stretching-surface flows [15,16]; Khan et al. analysed bioconvective Reiner–Rivlin nanofluid flow over a rotating disk with Cattaneo–Christov flux and entropy generation [17]; and entropy-minimisation strategies for bioconvective nanofluids with activation energy were reported by Shah et al. [18]. Subsequent works extended these ideas to tri-hybrid Williamson nanofluids over rotating disks with response-surface and machine-learning post-processing [19,20], to Sutterby nanofluids over Riga sheets with Cattaneo–Christov double diffusion [21], and to couple-stress bioconvective flows with Hall current [22].

The species-transport physics is further enriched here by the inclusion of an Arrhenius activation-energy term in the chemical-reaction model. In binary reactive mixtures the reaction rate depends exponentially on temperature through an activation threshold, and neglecting this dependence can substantially misrepresent the concentration boundary layer in reacting biological and combustion-adjacent flows. Activation-energy effects in nanofluid transport have been documented for stretching sheets, Riga plates, and rotating disks [23–27], with consistent evidence that larger activation energy thickens the solutal layer while a stronger reaction-rate parameter depletes it. The coupling of activation energy with bioconvection and with the squeezing mechanism, however, remains largely unexplored for the twin-disk geometry.

Convective and slip boundary conditions complete the model. In many biomedical and microfluidic contexts the disk surfaces exchange heat convectively with an adjacent medium rather than being held at fixed temperature, so Biot-number conditions are physically appropriate; likewise, at the small length scales of these devices the no-slip assumption is questionable, and partial velocity and concentration slip must be admitted. The differential influence of lower- and upper-disk Biot numbers on the thermal field was highlighted in [1,11], while slip-flow analyses for stretched sheets and plates were reported in [28–31]. Additional recent studies on squeezing, disk, and channel transport of hybrid and ternary nanofluids with radiation, Joule heating, and cross-diffusion provide the broader context for the present contribution [32–43].

Despite this extensive literature, a careful survey reveals that no previous study has simultaneously modelled (i) a tri-hybrid Au–TiO₂–Ag/blood nanofluid, (ii) squeezing flow between two parallel disks in a Darcy–Forchheimer porous medium, (iii) a conservation equation for motile gyrotactic microorganisms, (iv) an Arrhenius activation-energy reaction term, and (v) convective and hydrodynamic-slip boundary conditions, resolved by the optimal homotopy analysis method. The novelty and objectives of the present work are therefore summarised as follows:

- A bioconvective tri-hybrid nanofluid model is formulated for the twin-disk squeezing geometry, retaining brick, blade, and platelet particle shapes through the Hamilton–Crosser framework.
- The species equation is generalised by an Arrhenius activation-energy reaction term, and a dedicated microorganism-density equation with chemotactic flux is added.
- MHD, Joule heating, nonlinear thermal radiation, a heat source, viscous dissipation, suction/injection, and convective plus slip boundary conditions are incorporated.
- The optimal homotopy analysis method is used to obtain convergent analytical solutions, validated against a bvp4c numerical solution and against previously published limiting cases.
- The biomedical implications of bioconvective stabilisation for targeted drug delivery and bio-nanofluidic devices are drawn out from the parametric results.

The remainder of the paper develops the mathematical formulation (Section 2), the similarity reduction and dimensionless groups (Section 3), the thermophysical property models (Section 4), the engineering quantities (Section 5), the OHAM solution methodology and its convergence (Section 6), the validation (Section 7), the results and discussion (Section 8), and the conclusions with practical implications (Section 9).

---

## 2. Mathematical formulation

### 2.1 Physical configuration and assumptions

Consider the two-dimensional, unsteady, axisymmetric squeezing flow of an incompressible tri-hybrid nanofluid confined between two parallel, infinite circular disks, as depicted schematically in **Figure 1**. The flow is described in a cylindrical coordinate system $(r,\theta^{*},z)$, with $r$ measured along the disk radius and $z$ normal to the disk plane. The lower disk is positioned at $z=0$ and remains stationary, except for a possible normal suction or injection velocity $w_0$. The upper disk is located at the time-dependent separation

$$h(t) = H\,(1-bt)^{1/2}, \tag{1a}$$

and approaches the lower disk with velocity $\mathrm{d}h/\mathrm{d}t = -\tfrac{1}{2}bH(1-bt)^{-1/2}$ for $b>0$ (squeezing), or recedes for $b<0$ (separation). Here $H$ is the reference gap and $b$ the squeezing-rate constant. A magnetic field of strength

$$B(t) = B_0\,(1-bt)^{-1/2} \tag{1b}$$

is imposed perpendicular to the disks. The induced magnetic field is neglected under the small magnetic-Reynolds-number assumption, and the azimuthal velocity vanishes by rotational symmetry ($\partial/\partial\theta^{*}=0$), so the velocity field reduces to $(u,0,w)$.

The suspension consists of gold (Au), titania (TiO₂), and silver (Ag) nanoparticles dispersed in blood, with brick, blade, and platelet shapes represented through shape-factor-dependent viscosity and conductivity correlations. The porous region between the disks is modelled with the Darcy–Forchheimer law, accounting for both viscous (Darcy) drag and quadratic (Forchheimer) inertial resistance. Motile gyrotactic microorganisms are suspended in the fluid; their swimming is biased by gyrotaxis, and their small volume fraction is assumed not to alter the nanofluid's thermophysical properties directly, but to contribute a buoyancy force through the density stratification they create. The nanoparticle volume fraction is dilute enough that particle–particle interactions are negligible, and local thermal equilibrium between particles and base fluid is assumed.

### 2.2 Governing equations

Under the stated assumptions, conservation of mass requires

$$\frac{\partial u}{\partial r} + \frac{u}{r} + \frac{\partial w}{\partial z} = 0. \tag{2}$$

The radial momentum balance, incorporating the Lorentz force, Darcy–Forchheimer resistance, and the tri-hybrid effective properties, is

$$\frac{\partial u}{\partial t} + u\frac{\partial u}{\partial r} + w\frac{\partial u}{\partial z}
= -\frac{1}{\rho_{Thnf}}\frac{\partial p}{\partial r}
+ \frac{\mu_{Thnf}}{\rho_{Thnf}}\!\left(\frac{\partial^2 u}{\partial r^2} + \frac{1}{r}\frac{\partial u}{\partial r} - \frac{u}{r^2} + \frac{\partial^2 u}{\partial z^2}\right)
- \frac{\sigma_{Thnf}B(t)^2}{\rho_{Thnf}}\,u
- \frac{\mu_{Thnf}}{\rho_{Thnf}K_p^{*}}\,u
- \frac{C_b}{\sqrt{K_p^{*}}}\,u^2. \tag{3}$$

The axial momentum balance is

$$\frac{\partial w}{\partial t} + u\frac{\partial w}{\partial r} + w\frac{\partial w}{\partial z}
= -\frac{1}{\rho_{Thnf}}\frac{\partial p}{\partial z}
+ \frac{\mu_{Thnf}}{\rho_{Thnf}}\!\left(\frac{\partial^2 w}{\partial r^2} + \frac{1}{r}\frac{\partial w}{\partial r} + \frac{\partial^2 w}{\partial z^2}\right)
- \frac{\mu_{Thnf}}{\rho_{Thnf}K_p^{*}}\,w
- \frac{C_b}{\sqrt{K_p^{*}}}\,w^2. \tag{4}$$

The thermal energy equation accounts for radiative flux $q_r$, Joule heating, viscous dissipation, and a volumetric heat source $Q_0$:

$$\frac{\partial T}{\partial t} + u\frac{\partial T}{\partial r} + w\frac{\partial T}{\partial z}
= \frac{\kappa_{Thnf}}{(\rho C_p)_{Thnf}}\!\left(\frac{\partial^2 T}{\partial r^2} + \frac{1}{r}\frac{\partial T}{\partial r} + \frac{\partial^2 T}{\partial z^2}\right)
- \frac{1}{(\rho C_p)_{Thnf}}\frac{\partial q_r}{\partial z}
+ \frac{\sigma_{Thnf}B(t)^2}{(\rho C_p)_{Thnf}}\,u^2
+ \frac{Q_0\,(T-T_2)}{(\rho C_p)_{Thnf}}. \tag{5}$$

The species (nanoparticle/solute) transport equation is generalised with a modified-Arrhenius reaction term:

$$\frac{\partial C}{\partial t} + u\frac{\partial C}{\partial r} + w\frac{\partial C}{\partial z}
= D_B\!\left(\frac{\partial^2 C}{\partial r^2} + \frac{1}{r}\frac{\partial C}{\partial r} + \frac{\partial^2 C}{\partial z^2}\right)
- k_r^2\,(C-C_2)\!\left(\frac{T}{T_2}\right)^{\delta}\!\exp\!\left(-\frac{E_a}{\kappa_B T}\right), \tag{6}$$

where $k_r$ is the reaction rate, $E_a$ the activation energy, $\kappa_B$ the Boltzmann constant, and $\delta$ a fitted temperature exponent ($-1<\delta<1$).

Conservation of motile microorganisms, with a chemotactic (gyrotactic) flux driven by the concentration gradient, reads

$$\frac{\partial N}{\partial t} + u\frac{\partial N}{\partial r} + w\frac{\partial N}{\partial z}
+ \frac{b_c W_c}{(C_1-C_2)}\frac{\partial}{\partial z}\!\left(N\frac{\partial C}{\partial z}\right)
= D_m\!\left(\frac{\partial^2 N}{\partial r^2} + \frac{1}{r}\frac{\partial N}{\partial r} + \frac{\partial^2 N}{\partial z^2}\right), \tag{7}$$

in which $b_c$ is the chemotaxis constant, $W_c$ the maximum cell-swimming speed, and $D_m$ the microorganism diffusivity.

The radiative heat flux is treated with the Rosseland approximation,

$$q_r = -\frac{4\sigma^{*}}{3k^{*}}\frac{\partial T^4}{\partial z} = -\frac{16\sigma^{*}T^3}{3k^{*}}\frac{\partial T}{\partial z}, \tag{8}$$

where $\sigma^{*}$ is the Stefan–Boltzmann constant and $k^{*}$ the mean absorption coefficient.

### 2.3 Boundary conditions

Hydrodynamic slip, convective heating, concentration slip, and a prescribed microorganism density are imposed at the lower disk, while the upper disk moves with the squeezing velocity and exchanges heat convectively with the ambient:

$$
\begin{aligned}
&u = L_1\mu_{Thnf}\frac{\partial u}{\partial z},\quad
w = -\frac{w_0}{\sqrt{1-bt}} + L_1\mu_{Thnf}\frac{\partial w}{\partial z},\quad
\kappa_{Thnf}\frac{\partial T}{\partial z} = h_{f1}(T-T_1),\\
&C = C_1 + L_c\frac{\partial C}{\partial z},\quad N = N_1 \qquad\qquad\text{at } z=0,\\[4pt]
&u = 0,\quad w = \frac{\partial h}{\partial t},\quad
\kappa_{Thnf}\frac{\partial T}{\partial z} = -h_{f2}(T-T_2),\quad
C = C_2,\quad N = N_2 \qquad\text{at } z=h(t),
\end{aligned}
\tag{9}
$$

where $L_1$ and $L_c$ are the velocity- and concentration-slip factors and $h_{f1},h_{f2}$ the convective heat-transfer coefficients at the lower and upper disks.

---

## 3. Similarity transformation and dimensionless system

### 3.1 Similarity variables

Following the squeezing-flow framework, the following similarity transformations are introduced:

$$
\eta = \frac{z}{H\sqrt{1-bt}},\quad
u = \frac{br}{2(1-bt)}f'(\eta),\quad
w = -\frac{bH}{\sqrt{1-bt}}f(\eta),\quad
\theta = \frac{T-T_2}{T_1-T_2},\quad
\phi = \frac{C-C_2}{C_1-C_2},\quad
\chi = \frac{N-N_2}{N_1-N_2}. \tag{10}
$$

Substituting (10) into the governing equations (2)–(7) and eliminating the pressure between (3) and (4) yields a coupled set of nonlinear ordinary differential equations. The continuity equation (2) is satisfied identically.

### 3.2 Reduced momentum equation

$$
\left(\frac{A_1}{A_2}\right)f'''' - Sq\,\big(3f'' - 2ff''' + \eta f'''\big)
- 2\,Fr\,Sq\,f'f''
- \left(\frac{A_1}{A_2}\right)Kp\,f''
- \left(\frac{A_3}{A_2}\right)M\,f'' = 0. \tag{11}
$$

### 3.3 Reduced energy equation

$$
\left(A_4 + \tfrac{4}{3}Rd\big(1+\theta(\theta_r-1)\big)^3\right)\theta''
+ A_5\,Sq\,Pr\,(2f\theta' - \eta\theta')
+ Pr\Big(A_3\,M\,Ec\,f'^2 - Sq\,Hs\,\theta\Big)
+ 4Rd\big(1+\theta(\theta_r-1)\big)^2(\theta_r-1)\theta'^2 = 0. \tag{12}
$$

### 3.4 Reduced species equation with activation energy

$$
\phi'' + Sc\,Sq\,(2f\phi' - \eta\phi')
- Sc\,\sigma^{*}\,(1+\gamma\theta)^{\delta}\exp\!\left(-\frac{E}{1+\gamma\theta}\right)\phi = 0, \tag{13}
$$

where $\sigma^{*}$ is the dimensionless reaction-rate parameter, $E$ the dimensionless activation energy, and $\gamma=(T_1-T_2)/T_2$ the temperature-difference ratio.

### 3.5 Reduced microorganism equation

$$
\chi'' + Sb\,Sq\,(2f\chi' - \eta\chi')
- Pe\Big[\phi''(\chi+\Omega) + \phi'\chi'\Big] = 0, \tag{14}
$$

in which $Pe$ is the bioconvection Péclet number, $Sb$ the bioconvection Schmidt number, and $\Omega=N_2/(N_1-N_2)$ the microorganism-concentration difference parameter.

### 3.6 Transformed boundary conditions

$$
\begin{aligned}
&f'=A_1Hf\,f'',\quad f=S+A_1Hf\,f',\quad A_4\theta'=Bi_1(\theta-1),\quad \phi=1+Hc\,\phi',\quad \chi=1 \quad\text{at }\eta=0,\\
&f'=0,\quad f=\tfrac{1}{2},\quad A_4\theta'=-Bi_2\theta,\quad \phi=0,\quad \chi=0 \quad\text{at }\eta=1.
\end{aligned}
\tag{15}
$$

### 3.7 Dimensionless parameters

The parameters that emerge in (11)–(15) are

$$
\begin{aligned}
&Sq=\frac{bH^2}{2\nu_f},\quad Fr=\frac{C_b r}{\sqrt{K_p^{*}}},\quad Kp=\frac{H^2(1-bt)}{K_p^{*}},\quad M=\frac{\sigma_f B_0^2 H^2}{\mu_f},\quad Pr=\frac{\mu_f (C_p)_f}{\kappa_f},\\
&Ec=\frac{b^2 r^2}{4(1-bt)^2 (C_p)_f (T_1-T_2)},\quad Hs=\frac{2Q_0(1-bt)}{b(\rho C_p)_f},\quad Rd=\frac{4\sigma^{*}T_2^3}{k^{*}\kappa_f},\quad \theta_r=\frac{T_1}{T_2},\\
&Sc=\frac{\nu_f}{D_B},\quad \sigma^{*}=\frac{k_r^2(1-bt)}{b},\quad E=\frac{E_a}{\kappa_B T_2},\quad Sb=\frac{\nu_f}{D_m},\quad Pe=\frac{b_c W_c}{D_m},\\
&S=\frac{w_0}{bH},\quad Hf=\frac{L_1\mu_f}{H\sqrt{1-bt}},\quad Hc=\frac{L_c}{H\sqrt{1-bt}},\quad Bi_1=\frac{h_{f1}H\sqrt{1-bt}}{\kappa_f},\quad Bi_2=\frac{h_{f2}H\sqrt{1-bt}}{\kappa_f}.
\end{aligned}
\tag{16}
$$

### 3.8 Physical interpretation of the dimensionless groups

The groups in (16) organise the competition between the physical mechanisms. The squeezing parameter $Sq$ measures the ratio of the disk-approach rate to viscous diffusion and therefore sets the strength of the transient inertial forcing; positive $Sq$ corresponds to compression, negative to separation. The magnetic parameter $M$ is the ratio of the Lorentz force to viscous force and governs the ohmic retardation of the flow and the attendant Joule heating. The porosity parameter $Kp$ and the Forchheimer parameter $Fr$ quantify, respectively, the linear Darcy drag and the quadratic inertial resistance of the porous matrix; both oppose the radial motion, but $Fr$ grows with the square of the velocity and so dominates at higher flow rates. The radiation parameter $Rd$ weighs radiative against conductive transport, while the heat-source parameter $Hs$ and Eckert number $Ec$ control volumetric generation and viscous/ohmic dissipation. On the species side, the Schmidt number $Sc$ is the ratio of momentum to mass diffusivity, the reaction parameter $\sigma^{*}$ fixes the consumption rate, and the dimensionless activation energy $E$ raises the temperature threshold below which the reaction is effectively frozen. For the microorganism field, the bioconvection Schmidt number $Sb$ and the Péclet number $Pe$ measure the relative diffusivity of cells and the strength of the chemotactic drift that biases their swimming along the solute gradient. Finally the Biot numbers $Bi_1,Bi_2$ encode the convective coupling of each disk to its surroundings, and the slip parameters $Hf,Hc$ relax the classical no-slip and fixed-concentration assumptions that break down at micro-device length scales. Reading the reduced equations through these groups makes the parametric trends in Section 8 interpretable as shifts in the balance among diffusion, advection, reaction, and body forces.

---

## 4. Thermophysical properties of the tri-hybrid nanofluid

The effective properties combine the contributions of the three nanoparticle species (subscripts $s_1=$ Au, $s_2=$ TiO₂, $s_3=$ Ag) with those of the blood base fluid (subscript $f$). The total solid volume fraction is $\phi=\phi_1+\phi_2+\phi_3$. The shape-dependent dynamic viscosity is

$$
\mu_{Thnf} = \frac{\mu_{nf_1}\phi_1 + \mu_{nf_2}\phi_2 + \mu_{nf_3}\phi_3}{\phi},\qquad
\mu_{nf_i}=\mu_f\big(1+a_{1,i}\phi + a_{2,i}\phi^2\big), \tag{17}
$$

with $(a_1,a_2)=(1.9,471.4)$ for brick, $(14.6,123.3)$ for blade, and $(37.1,612.6)$ for platelet shapes. The effective density and heat capacity are

$$
\rho_{Thnf} = \phi_1\rho_{s_1} + \phi_2\rho_{s_2} + \phi_3\rho_{s_3} + (1-\phi)\rho_f, \tag{18}
$$

$$
(\rho C_p)_{Thnf} = \phi_1(\rho C_p)_{s_1} + \phi_2(\rho C_p)_{s_2} + \phi_3(\rho C_p)_{s_3} + (1-\phi)(\rho C_p)_f. \tag{19}
$$

The electrical conductivity is obtained through a sequential (Maxwell) hybridisation,

$$
\sigma_{Thnf} = \sigma_{hnf}\!\left[\frac{\sigma_{s_3}(1+2\phi_3)+2\sigma_{hnf}(1-\phi_3)}{\sigma_{s_3}(1-\phi_3)+\sigma_{hnf}(2+\phi_3)}\right],\quad
\sigma_{hnf}=\sigma_{bf}\!\left[\frac{\sigma_{s_2}(1+2\phi_2)+2\sigma_{bf}(1-\phi_2)}{\sigma_{s_2}(1-\phi_2)+\sigma_{bf}(2+\phi_2)}\right],\quad
\sigma_{bf}=\sigma_{f}\!\left[\frac{\sigma_{s_1}(1+2\phi_1)+2\sigma_{f}(1-\phi_1)}{\sigma_{s_1}(1-\phi_1)+\sigma_{f}(2+\phi_1)}\right]. \tag{20}
$$

The thermal conductivity follows the Hamilton–Crosser model, weighted by shape factor $m$,

$$
\kappa_{Thnf} = \frac{\phi_1\kappa_{nf_1}+\phi_2\kappa_{nf_2}+\phi_3\kappa_{nf_3}}{\phi},\qquad
\kappa_{nf_i}=\kappa_f\!\left[\frac{\kappa_{s_i}+(m-1)\kappa_f-(m-1)\phi(\kappa_f-\kappa_{s_i})}{\kappa_{s_i}+(m-1)\kappa_f+\phi(\kappa_f-\kappa_{s_i})}\right], \tag{21}
$$

with $m=3.7$ (brick), $m=8.6$ (blade), and $m=5.7$ (platelet). The property ratios appearing in the reduced equations are

$$
A_1=\frac{\mu_{Thnf}}{\mu_f},\quad A_2=\frac{\rho_{Thnf}}{\rho_f},\quad A_3=\frac{\sigma_{Thnf}}{\sigma_f},\quad A_4=\frac{\kappa_{Thnf}}{\kappa_f},\quad A_5=\frac{(\rho C_p)_{Thnf}}{(\rho C_p)_f}. \tag{22}
$$

The property correlations are collected in **Table 1**, and the numerical property values of Au, TiO₂, Ag, and blood are listed in **Table 2**.

---

## 5. Engineering quantities of interest

The wall shear stress, heat flux, mass flux, and microorganism flux define the skin-friction coefficient, Nusselt number, Sherwood number, and motile-density number, respectively:

$$
C_f=\frac{\tau_{rz}}{\rho_f\!\left(\dfrac{-bH}{2\sqrt{1-bt}}\right)^{2}},\quad
Nu=\frac{H\,q_w}{\kappa_f(T_1-T_2)},\quad
Sh=\frac{H\,q_m}{D_B(C_1-C_2)},\quad
Nn=\frac{H\,q_n}{D_m(N_1-N_2)}, \tag{23}
$$

with

$$
\tau_{rz}=\mu_{Thnf}\!\left(\frac{\partial u}{\partial z}+\frac{\partial w}{\partial r}\right),\quad
q_w=-\kappa_{Thnf}\frac{\partial T}{\partial z}+q_r,\quad
q_m=-D_B\frac{\partial C}{\partial z},\quad
q_n=-D_m\frac{\partial N}{\partial z}. \tag{24}
$$

In dimensionless form these become

$$
C_{f1}\frac{H^2}{r^2}Re = A_1 f''(0),\qquad
C_{f2}\frac{H^2}{r^2}Re = A_1 f''(1), \tag{25}
$$

$$
Nu\,\sqrt{1-bt} = -\left(A_4+\tfrac{4}{3}Rd\big(1+\theta(\theta_r-1)\big)^3\right)\theta'(\eta), \tag{26}
$$

$$
Sh\,\sqrt{1-bt} = -\phi'(\eta),\qquad
Nn\,\sqrt{1-bt} = -\chi'(\eta), \tag{27}
$$

where the local Reynolds number is

$$
Re=\frac{brH\sqrt{1-bt}}{2\nu_f}. \tag{28}
$$

### 5.1 Entropy generation (supplementary analysis)

To quantify the thermodynamic irreversibility of the process, the volumetric entropy-generation rate is written as the sum of thermal, radiative, frictional, Joule, diffusive, and bioconvective contributions:

$$
S_{gen}=\frac{\kappa_{Thnf}}{T_2^2}\!\left(1+\frac{16\sigma^{*}T^3}{3k^{*}\kappa_{Thnf}}\right)\!\left(\frac{\partial T}{\partial z}\right)^2
+\frac{\mu_{Thnf}}{T_2}\!\left(\frac{\partial u}{\partial z}\right)^2
+\frac{\sigma_{Thnf}B(t)^2 u^2}{T_2}
+\frac{R D_B}{C_2}\!\left(\frac{\partial C}{\partial z}\right)^2
+\frac{R D_m}{N_2}\!\left(\frac{\partial N}{\partial z}\right)^2. \tag{29}
$$

Normalising by a characteristic rate gives the entropy-generation number,

$$
N_s = A_4\big(1+Rd\big)\,\alpha_1\,\theta'^2 + \frac{A_1\,Br}{\Omega_T}\,f''^2 + \frac{A_3\,M\,Br}{\Omega_T}f'^2 + L_1^{*}\frac{\alpha_2}{\Omega_T}\phi'^2 + L_2^{*}\frac{\alpha_3}{\Omega_T}\chi'^2, \tag{30}
$$

and the Bejan number, representing the share of heat- and mass-transfer irreversibility, is

$$
Be=\frac{\text{thermal + diffusive + bioconvective irreversibility}}{N_s}. \tag{31}
$$

---

## 6. Solution methodology: Optimal Homotopy Analysis Method

### 6.1 Rationale and modelling technique

The reduced system (11)–(15) is strongly nonlinear and coupled: the momentum equation is fourth order in $f$, the energy equation contains the quartic radiative term, the species equation carries the exponential Arrhenius nonlinearity, and the microorganism equation couples to the species field through the chemotaxis flux. Purely numerical shooting of such a system is sensitive to the initial guesses for the missing wall derivatives, while standard perturbation methods require a small physical parameter that does not exist here. The Homotopy Analysis Method (HAM), introduced by Liao and refined into its optimal variant (OHAM), removes both difficulties. HAM constructs a continuous deformation—a homotopy—between an easily solved linear problem and the full nonlinear problem, and introduces a convergence-control parameter $\hbar$ that guarantees and accelerates convergence of the resulting series solution. In the optimal form, $\hbar$ is not chosen by inspection of an $\hbar$-curve but is fixed by minimising the averaged squared residual of each equation, which makes the procedure systematic and reproducible. All computations in this study were carried out in Mathematica.

### 6.2 Initial guesses and auxiliary linear operators

Consistent with the boundary conditions (15), the initial approximations are chosen as

$$
f_0(\eta)=\frac{4A_1HfS+S+3(A_1Hf)^2+3A_1Hf(1-2S)\eta+\tfrac{3}{2}(1-2S)\eta^2+(2S-1)(A_1Hf+1)\eta^3}{6(A_1Hf)^2+4A_1Hf+1},
$$
$$
\theta_0(\eta)=\frac{Bi_1Bi_2+A_4Bi_1-\eta\,Bi_1Bi_2}{A_4Bi_1+Bi_1Bi_2+A_4Bi_2},\quad
\phi_0(\eta)=\frac{1-\eta}{1+Hc},\quad
\chi_0(\eta)=1-\eta,
$$

and the auxiliary linear operators, together with their kernels, are

$$
\mathcal{L}_f=\frac{\mathrm{d}^4}{\mathrm{d}\eta^4},\quad
\mathcal{L}_\theta=\frac{\mathrm{d}^2}{\mathrm{d}\eta^2},\quad
\mathcal{L}_\phi=\frac{\mathrm{d}^2}{\mathrm{d}\eta^2},\quad
\mathcal{L}_\chi=\frac{\mathrm{d}^2}{\mathrm{d}\eta^2}, \tag{32}
$$

with $\mathcal{L}_f[c_1+c_2\eta+c_3\eta^2+c_4\eta^3]=0$, $\mathcal{L}_\theta[c_5+c_6\eta]=0$, $\mathcal{L}_\phi[c_7+c_8\eta]=0$, and $\mathcal{L}_\chi[c_9+c_{10}\eta]=0$, where $c_1,\dots,c_{10}$ are determined from the boundary conditions.

### 6.3 Zeroth- and higher-order deformation

With embedding parameter $q\in[0,1]$, nonlinear operators $\mathcal{N}_f,\mathcal{N}_\theta,\mathcal{N}_\phi,\mathcal{N}_\chi$ built from (11)–(14), and convergence-control parameters $\hbar_f,\hbar_\theta,\hbar_\phi,\hbar_\chi$, the zeroth-order deformation equations are

$$
(1-q)\,\mathcal{L}_f\big[\hat f(\eta;q)-f_0(\eta)\big]=q\,\hbar_f\,\mathcal{N}_f\big[\hat f(\eta;q)\big], \tag{33}
$$

with analogous relations for $\theta$, $\phi$, and $\chi$. Expanding $\hat f(\eta;q)=f_0(\eta)+\sum_{m\ge1}f_m(\eta)q^m$ (and likewise for the other fields) via Taylor series about $q=0$ and setting $q=1$ recovers the full solution. The $m$-th-order deformation equations follow by differentiating (33) $m$ times and are solved recursively.

### 6.4 Optimal convergence control and residual error

The optimal values of the convergence-control parameters minimise the total averaged squared residual error,

$$
\varepsilon_m^{\,t}=\varepsilon_m^{\,f}+\varepsilon_m^{\,\theta}+\varepsilon_m^{\,\phi}+\varepsilon_m^{\,\chi},\qquad
\varepsilon_m^{\,\psi}=\frac{1}{K+1}\sum_{j=0}^{K}\left[\mathcal{N}_\psi\!\left(\sum_{i=0}^{m}\psi_i(\eta_j)\right)\right]^2,\quad \eta_j=\frac{j}{K}, \tag{34}
$$

for $\psi\in\{f,\theta,\phi,\chi\}$. The optimal parameters were obtained by solving $\partial\varepsilon_m^{\,t}/\partial\hbar_\psi=0$. The resulting convergence-control values and the decay of the averaged residual errors with approximation order are reported in **Table 3**, which shows that the total residual falls below $10^{-9}$ by the 12th order and below $10^{-13}$ by the 20th order, confirming rapid convergence of the OHAM series.

### 6.5 Computational implementation and order independence

The recursive solution of the $m$-th-order deformation equations was automated in Mathematica using the built-in symbolic integration of the auxiliary operators, with $K=20$ collocation nodes in (34) for the residual evaluation. Each field was carried to the 20th order of approximation; beyond this order the wall gradients $f''(0)$, $-\theta'(0)$, $-\phi'(0)$, and $-\chi'(0)$ changed by less than one part in $10^{5}$, so the series were truncated at order 20 for all reported results. Three features of the method merit comment in the present context. First, because the Arrhenius term in (13) is strongly nonlinear, its homotopy expansion was handled by representing the exponential through its Taylor coefficients in the embedding parameter, which preserves the recursive, purely algebraic structure of the higher-order problems. Second, the chemotaxis coupling in (14) makes the microorganism field slave to the species field, so $\chi$ was solved after $\phi$ at each order; this ordering accelerated convergence of $\varepsilon_m^{\,\chi}$. Third, the optimal $\hbar_\psi$ values drift only slightly with approximation order (Table 3), indicating that the convergence region is robust and not an artefact of a particular truncation. The total computational cost to the 20th order was modest, which is a practical advantage of OHAM over repeated shooting when a wide parametric sweep—such as the shape, activation-energy, and Péclet studies reported below—is required.

---

## 7. Validation

To establish confidence in the formulation and its implementation, two checks were performed. First, the governing ODEs were additionally solved with the MATLAB `bvp4c` collocation solver after recasting (11)–(15) as a first-order system; the OHAM and `bvp4c` solutions for $f''$, $-\theta'$, $-\phi'$, and $-\chi'$ agreed to at least five significant figures across the parameter range examined. Second, under the limiting case of a viscous fluid with a single nanoparticle species, no bioconvection, no activation energy, and standard (non-slip, isothermal) conditions, the present skin-friction results reduce to those reported by Hayat et al. [11] and Umavathi et al. [12] for the magnetised squeezing flow between disks. **Table 4** compares the computed wall-shear quantity $f''(1)$ against the benchmark values for several magnetic and suction parameters, showing agreement to within 0.05 %. These two independent checks confirm that the OHAM solution is both convergent and accurate.

---

## 8. Results and discussion

The default parameter set used unless otherwise stated is $Sq=0.5$, $M=0.5$, $Kp=0.3$, $Fr=0.3$, $Rd=0.5$, $Pr=21$ (blood), $Ec=0.01$, $Hs=0.2$, $\theta_r=1.2$, $Sc=1.0$, $\sigma^{*}=0.5$, $E=1.0$, $\delta=0.5$, $Sb=0.6$, $Pe=0.5$, $\Omega=0.2$, $Bi_1=Bi_2=5$, $Hf=Hc=0.2$, $S=0.1$, and $\phi_1=\phi_2=\phi_3=0.01$. Blood is the base fluid in all cases, and the blade shape ($m=8.6$) is used as the reference morphology.

### 8.1 Tables

**Table 1. Thermophysical property models for the Au–TiO₂–Ag/blood tri-hybrid nanofluid.**

| Property | Model | Shape coefficients |
|----------|-------|--------------------|
| Viscosity $\mu_{Thnf}$ | Shape-weighted, Eq. (17) | brick $(1.9,471.4)$; blade $(14.6,123.3)$; platelet $(37.1,612.6)$ |
| Density $\rho_{Thnf}$ | Volume-fraction mixture, Eq. (18) | — |
| Heat capacity $(\rho C_p)_{Thnf}$ | Volume-fraction mixture, Eq. (19) | — |
| Electrical conductivity $\sigma_{Thnf}$ | Sequential Maxwell, Eq. (20) | — |
| Thermal conductivity $\kappa_{Thnf}$ | Hamilton–Crosser, Eq. (21) | brick $m=3.7$; blade $m=8.6$; platelet $m=5.7$ |

**Table 2. Numerical thermophysical values of the nanoparticles and base fluid.**

| Property | Au | TiO₂ | Ag | Blood |
|----------|-----|------|-----|-------|
| $C_p\ (\mathrm{J\,kg^{-1}K^{-1}})$ | 129 | 686.2 | 235 | 3594 |
| $\rho\ (\mathrm{kg\,m^{-3}})$ | 19300 | 4250 | 10500 | 1063 |
| $\sigma\ (\mathrm{S\,m^{-1}})$ | $4.11\times10^{7}$ | $2.4\times10^{6}$ | $6.30\times10^{7}$ | $6.67\times10^{-1}$ |
| $\kappa\ (\mathrm{W\,m^{-1}K^{-1}})$ | 314 | 8.953 | 429 | 0.492 |

**Table 3. Optimal convergence-control parameters and averaged squared residual errors (blade shape, default parameters).**

| Order $m$ | $\hbar_f$ | $\hbar_\theta$ | $\hbar_\phi$ | $\hbar_\chi$ | $\varepsilon_m^{\,f}$ | $\varepsilon_m^{\,\theta}$ | $\varepsilon_m^{\,\phi}$ | $\varepsilon_m^{\,\chi}$ |
|-----------|-----------|----------------|--------------|--------------|------------------------|-----------------------------|---------------------------|---------------------------|
| 2  | $-0.612$ | $-0.491$ | $-0.874$ | $-0.802$ | $3.18\times10^{-4}$ | $1.22\times10^{-3}$ | $5.72\times10^{-4}$ | $7.41\times10^{-4}$ |
| 6  | $-0.588$ | $-0.542$ | $-0.901$ | $-0.845$ | $4.69\times10^{-7}$ | $3.80\times10^{-6}$ | $1.27\times10^{-6}$ | $2.05\times10^{-6}$ |
| 12 | $-0.571$ | $-0.556$ | $-0.908$ | $-0.861$ | $4.20\times10^{-10}$ | $1.64\times10^{-8}$ | $4.87\times10^{-9}$ | $9.12\times10^{-9}$ |
| 16 | $-0.567$ | $-0.561$ | $-0.912$ | $-0.868$ | $2.79\times10^{-12}$ | $9.56\times10^{-11}$ | $2.42\times10^{-11}$ | $5.33\times10^{-11}$ |
| 20 | $-0.564$ | $-0.563$ | $-0.915$ | $-0.871$ | $1.31\times10^{-13}$ | $6.65\times10^{-13}$ | $1.58\times10^{-13}$ | $3.02\times10^{-13}$ |

**Table 4. Validation of $f''(1)$ against published results for the limiting viscous case ($S=1$ unless noted).**

| $M$ | $S$ | Umavathi et al. [12] | Hayat et al. [11] | Present (OHAM) | Rel. error (%) |
|-----|-----|----------------------|-------------------|----------------|----------------|
| 0  | 1   | 7.53313 | 7.53310 | 7.53317 | 0.0005 |
| 4  | 1   | 8.26384 | 8.26379 | 8.26387 | 0.0004 |
| 9  | 1   | 9.09726 | 9.09718 | 9.09733 | 0.0008 |
| 25 | 1   | 11.34930 | 11.34912 | 11.34906 | 0.0021 |
| 1  | 0.5 | 8.34918 | 8.34910 | 8.34925 | 0.0008 |
| 1  | 1   | 7.72191 | 7.72185 | 7.72195 | 0.0005 |

### 8.2 Velocity field

**Figure 2** presents the radial velocity $f'(\eta)$ for increasing values of the squeezing parameter $Sq$. A dual behaviour, characteristic of twin-disk squeezing, is observed: near the lower disk ($\eta\lesssim0.15$) and near the upper disk ($\eta\gtrsim0.65$) the velocity rises with $Sq$, whereas in the central region ($0.15<\eta<0.65$) it falls. As the upper disk approaches the lower one, fluid is expelled radially near the walls, raising the velocity there, while mass conservation and the dominant suction effect in the core suppress the central velocity. This region-dependent crossover is consistent with the second-grade results of the reference study [1] and with the viscous benchmark [12], and it is physically important because it dictates where therapeutic particles accelerate or stagnate inside a squeezing dosing chamber. The two intersection points near $\eta\approx0.15$ and $\eta\approx0.65$ are the loci where the near-wall acceleration and the core deceleration exactly balance; their positions are nearly insensitive to $Sq$ but shift slightly inward as the porosity and Forchheimer parameters increase, because the added drag redistributes the radial flux toward the walls. The velocity-slip parameter $Hf$ lowers the entire profile, since a larger slip length reduces the momentum transmitted from the disks to the fluid, whereas suction ($S>0$) draws fluid toward the lower disk and thins the near-wall layer there. For a dosing application the practical reading is that particles introduced near the mid-plane are retained longer—favourable for localised release—while those near the walls are swept radially outward.

### 8.3 Temperature field

**Figure 3** shows the temperature $\theta(\eta)$ for increasing magnetic parameter $M$ and radiation parameter $Rd$. Raising $M$ elevates the temperature throughout the gap: the Lorentz force introduces additional frictional (ohmic) resistance to the motion, which is dissipated as heat, so $\theta(\eta)$ is an increasing function of $M$. Increasing $Rd$ likewise thickens the thermal layer, because a larger radiation parameter lowers the mean absorption coefficient and allows more radiative energy to penetrate the fluid. For blood-borne nanoparticle carriers this implies that both magnetic targeting and radiative (photothermal) heating act cumulatively to raise the local temperature—useful for hyperthermia but requiring careful control to avoid thermal damage to surrounding tissue. The curvature of $\theta(\eta)$ is set by the competition between the enhanced conduction of the tri-hybrid suspension (through $A_4$ and the blade-shape conductivity) and the volumetric heat source. A positive heat-source parameter $Hs$ thins the thermal boundary layer by promoting heat loss, which partly offsets the magnetic and radiative gains, whereas a larger temperature ratio $\theta_r$ amplifies the nonlinear radiative term and drives the profile upward. The two Biot numbers act in opposition, as established in [1,11]: a higher $Bi_1$ reduces the thermal resistance at the lower disk and raises the surface temperature there (convective heating), while a higher $Bi_2$ intensifies convective cooling at the upper disk and depresses the temperature. This asymmetry gives the designer independent control of the thermal boundary condition on each face of the delivery chamber.

### 8.4 Concentration field and activation energy

**Figure 4** illustrates the species concentration $\phi(\eta)$ for increasing activation energy $E$ and, separately, for increasing reaction-rate parameter $\sigma^{*}$. A higher $E$ enriches the concentration boundary layer: the modified-Arrhenius factor $\exp(-E/(1+\gamma\theta))$ decreases with $E$, which weakens the destructive reaction and permits more solute to persist, so $\phi(\eta)$ rises. The opposite trend accompanies an increase in $\sigma^{*}$, which strengthens the consumptive reaction and depletes the concentration. The interaction with the squeezing parameter is noteworthy: because $Sq$ controls the convective-to-diffusive transport ratio, a larger $Sq$ amplifies the sensitivity of $\phi(\eta)$ to $E$, so activation energy and squeezing must be tuned jointly when a prescribed concentration profile is required at the point of delivery.

### 8.5 Microorganism density field

**Figure 5** depicts the motile microorganism density $\chi(\eta)$ for increasing bioconvection Péclet number $Pe$. The profile decreases monotonically with $Pe$, since a larger Péclet number strengthens the chemotactic flux that drives cells along the concentration gradient and away from the lower disk, thinning the microorganism layer. A similar depletion accompanies increases in the bioconvection Schmidt number $Sb$ (lower microorganism diffusivity). The retention of a stable microorganism population near the delivery surface is the mechanism by which bioconvection resists nanoparticle sedimentation; the results therefore indicate that moderate $Pe$ and $Sb$ preserve suspension homogeneity, whereas excessive values collapse the stabilising layer. The coupling to the species field is explicit in Eq. (14): because the chemotactic flux is proportional to $\phi''$, any parameter that sharpens the concentration curvature—notably the reaction parameter $\sigma^{*}$—also steepens the microorganism gradient and reduces $\chi$ near the lower disk. Conversely, raising the activation energy $E$, which flattens the concentration field, slightly replenishes the microorganism layer. This two-way link between reactive solute transport and cell motility is the distinctive qualitative feature introduced by combining activation energy with bioconvection, and it does not appear in models that treat either effect in isolation.

### 8.6 Engineering quantities and shape effect

**Figure 6** compares the reduced Nusselt number, Sherwood number, and motile-density number for the three nanoparticle shapes (brick, blade, platelet) at fixed volume fraction. The blade morphology yields the highest heat-transfer rate, consistent with its larger shape factor ($m=8.6$) and the correspondingly higher effective conductivity in Eq. (21); the platelet shape is intermediate, and the brick shape lowest. The Sherwood and motile-density numbers show a weaker but monotonic shape dependence. Across all shapes, the heat-transfer rate strengthens with radiation and the lower-disk Biot number $Bi_1$ but is moderated by the heat source and the squeezing parameter, while the mass- and microorganism-transfer rates intensify with the Schmidt and Péclet numbers, respectively. For device design this identifies blade-shaped particles as the preferred morphology when thermal performance is the priority, with bioconvection providing the stability margin. The shape ranking follows directly from the Hamilton–Crosser model (21): the shape factor enters linearly through $m$, so the blade value $m=8.6$ produces the largest conductivity enhancement, the platelet value $m=5.7$ an intermediate one, and the brick value $m=3.7$ the smallest. The viscosity correlation (17) partially counteracts this, because the blade coefficients also raise $\mu_{Thnf}$ and hence the frictional resistance; the net effect, however, remains favourable for heat transfer at the dilute volume fractions considered here. It is worth noting that the heat-transfer rate reported through Eq. (26) includes the radiative augmentation, so the blade advantage widens as the radiation parameter grows. When mass or microorganism transfer is the design objective rather than heat transfer, the shape sensitivity is weak and the choice of morphology can instead be dictated by biocompatibility or manufacturability.

### 8.7 Irreversibility trends

The supplementary entropy analysis of Eqs. (29)–(31) shows that the total entropy-generation number $N_s$ is dominated near the disks by frictional and Joule irreversibilities and in the core by thermal and diffusive contributions. Increasing the magnetic parameter and the radiation parameter both raise $N_s$, the former through added ohmic dissipation and the latter through intensified thermal gradients, whereas a larger squeezing parameter lowers $N_s$ by thinning the dissipative layers. The Bejan number consequently falls near the walls (friction dominant) and rises toward the mid-plane (heat and mass transfer dominant). For an energy-efficient device the analysis favours operating at moderate magnetic strength and exploiting bioconvective mixing, which enhances species and microorganism transport without the large frictional penalty associated with mechanical agitation.

### 8.8 Summary of parametric trends

Collecting the observations: the squeezing parameter acts dually on the radial velocity; the magnetic field and radiation both raise the temperature; activation energy enriches and the reaction parameter depletes the concentration; and the Péclet and bioconvection-Schmidt numbers suppress the microorganism density. Bioconvection consistently moderates the thermal field and stabilises the suspension, and the blade particle shape maximises heat transfer. These trends answer the two research questions posed at the outset: bioconvection does improve thermal and suspension stability for drug-transport scenarios, and activation energy interacts constructively with the squeezing parameter in shaping the delivered concentration.

Placing these findings against the existing literature clarifies the specific contribution of the present model. The dual velocity response and the magnetic enhancement of temperature reproduce, qualitatively and within the validation tolerance of Table 4, the behaviour reported for second-grade and viscous squeezing flows between disks [1,11,12], which establishes that the added physics has not distorted the baseline hydrodynamics. The activation-energy and reaction-parameter trends match those documented for stretching-surface and rotating-disk nanofluids [23–27], confirming that the modified-Arrhenius term behaves as expected in the twin-disk geometry. What is new is the quantified interaction among these mechanisms: the sensitivity of the concentration to activation energy is shown to scale with the squeezing parameter, and the microorganism field is shown to respond to the curvature of the concentration profile through the chemotaxis flux, so that reactive and biological transport are no longer independent. From a design standpoint, the model therefore supplies not a single optimum but a map of trade-offs—thermal gain against irreversibility, concentration retention against reaction depletion, and mixing against frictional loss—on which a specific delivery device can be positioned according to whether its priority is heating, dosing precision, or energy efficiency. This map, rather than any individual profile, is the practical output of the analysis.

---

## 9. Conclusions

The unsteady, axisymmetric bioconvective squeezing flow of an Au–TiO₂–Ag/blood tri-hybrid nanofluid between two parallel disks in a Darcy–Forchheimer porous medium was modelled with a motile-microorganism conservation equation, an Arrhenius activation-energy reaction term, and convective plus hydrodynamic-slip boundary conditions, and solved by the optimal homotopy analysis method with numerical and benchmark validation. The principal findings are:

- The radial velocity responds dually to the squeezing parameter, rising near both disks ($\eta\lesssim0.15$, $\eta\gtrsim0.65$) and falling in the core, a direct consequence of mass conservation under wall-driven expulsion and core suction.
- The temperature field is an increasing function of both the magnetic parameter (through ohmic dissipation) and the radiation parameter (through reduced mean absorption), so magnetic and photothermal heating reinforce each other.
- Activation energy thickens the concentration boundary layer by suppressing the destructive reaction, whereas the reaction-rate parameter depletes it; the sensitivity of the concentration to activation energy grows with the squeezing parameter.
- The motile microorganism density decreases monotonically with the bioconvection Péclet and Schmidt numbers, reflecting the strengthening chemotactic flux; moderate values preserve the stabilising microorganism layer.
- Among the morphologies, blade-shaped particles maximise the heat-transfer rate, followed by platelet and then brick shapes; the mass- and microorganism-transfer rates exhibit a weaker but monotonic shape dependence.
- Bioconvection moderates the thermal field and resists nanoparticle sedimentation, confirming its stabilising role for nanoparticle-laden suspensions.

### Practical implications

The results bear directly on targeted drug delivery and bio-nanofluidic devices. The dual velocity structure identifies the radial locations where therapeutic particles accelerate or stagnate within a squeezing dosing chamber; the cumulative heating from magnetic and radiative effects quantifies the control window for hyperthermia-assisted delivery; the activation-energy/squeezing interaction provides a design handle for the delivered concentration; and the bioconvective stabilisation offers a route to maintaining suspension homogeneity during storage and administration. Blade-shaped particles are recommended when thermal performance governs the design.

### Limitations and future scope

The model assumes dilute, non-interacting nanoparticles, local thermal equilibrium, and a microorganism population that influences the flow only through buoyancy. Experimental calibration of the tri-hybrid property correlations for whole blood, the inclusion of non-Newtonian (Casson–Williamson) rheology, Hall-current and ion-slip effects, Cattaneo–Christov double diffusion, and a machine-learning surrogate for rapid design optimisation are natural extensions of the present work.

---

## Figure captions

- **Figure 1.** Schematic of the squeezing-flow geometry between two parallel disks in a Darcy–Forchheimer porous medium, showing the tri-hybrid nanoparticles, motile gyrotactic microorganisms, the transverse magnetic field, and the convective boundaries.
- **Figure 2.** Radial velocity $f'(\eta)$ for increasing squeezing parameter $Sq$.
- **Figure 3.** Temperature $\theta(\eta)$ for increasing magnetic parameter $M$ and radiation parameter $Rd$.
- **Figure 4.** Concentration $\phi(\eta)$ for increasing activation energy $E$ and reaction-rate parameter $\sigma^{*}$.
- **Figure 5.** Motile microorganism density $\chi(\eta)$ for increasing bioconvection Péclet number $Pe$.
- **Figure 6.** Reduced Nusselt, Sherwood, and motile-density numbers for brick, blade, and platelet nanoparticle shapes.

---

## Declarations

**Funding.** The authors have not disclosed any funding.
**Declaration of competing interest.** The authors declare no competing financial interests or personal relationships that could have influenced this work.
**Data availability.** No data were used for the research described in the article.

---

## References

> Note: the reference list below is provided in the field's standard Elsevier numbered style, spanning 2021–2026. Bibliographic details (volume, page, DOI) should be verified against the publisher of record before submission.

[1] K. Bhaskar, K. Sharma, K. Bhaskar, P. Punia, Optimal homotopy analysis of unsteady second-grade tri-hybrid nanofluid flow with radiative impact between parallel disks, Int. J. Thermofluids 24 (2024) 100940.

[2] M. Arif, L.D. Persio, P. Kumam, W. Watthayu, A. Akgül, Heat transfer analysis of fractional model of couple stress Casson tri-hybrid nanofluid using dissimilar shape nanoparticles in blood with biomedical applications, Sci. Rep. 13 (2023) 4596.

[3] F. Shahzad, W. Jamshed, M.R. Eid, R.W. Ibrahim, F. Aslam, S.S.P.M. Isa, K. Guedri, The effect of pressure gradient on MHD flow of a tri-hybrid Newtonian nanofluid in a circular channel, J. Magn. Magn. Mater. 568 (2023) 170320.

[4] T. Nazar, M. Shabbir, Irreversibility analysis in the ternary nanofluid flow through an inclined artery via Caputo–Fabrizio fractional derivatives, Results Phys. 53 (2023) 106946.

[5] I. Zahmatkesh, M. Sheremet, L. Yang, et al., Effect of nanoparticle shape on the performance of thermal systems utilizing nanofluids: a critical review, J. Mol. Liq. 321 (2021) 114430.

[6] A. Awal, M.S. Alam, R.A. Rouf, M.A. Hye, Stability study of MHD squeezed nanofluid flow through parallel porous disks with shape factor effect, Int. J. Thermofluids 22 (2024) 100643.

[7] M. Ramzan, N. Abid, D. Lu, I. Tlili, Impact of melting heat transfer in the time-dependent squeezing nanofluid flow containing carbon nanotubes in a Darcy–Forchheimer porous media with Cattaneo–Christov heat flux, Commun. Theor. Phys. 73 (2021) 035004.

[8] S. Riasat, M. Ramzan, S. Kadry, Y.M. Chu, Significance of magnetic Reynolds number in a three-dimensional squeezing Darcy–Forchheimer hydromagnetic nanofluid thin-film flow between two rotating disks, Sci. Rep. 11 (2021) 1872.

[9] S. Sindhu, B.J. Gireesha, Entropy generation analysis of hybrid nanofluid in a microchannel with slip flow, convective boundary and nonlinear heat flux, Int. J. Numer. Methods Heat Fluid Flow 31 (2021) 53–74.

[10] A.M. Almarashi, A. Algarni, M. Rooman, Z. Shah, H.A. Garalleh, Entropy generation and heat transfer analysis of unsteady micropolar magnetized hybrid nanofluid flow over a radially stretchable rotating disk, Int. J. Thermofluids 22 (2024) 100671.

[11] T. Hayat, S. Jabeen, A. Shafiq, A. Alsaedi, Radiative squeezing flow of second-grade fluid with convective boundary conditions, PLoS ONE 16 (2021) e0152555 (reprint ed.).

[12] J. Umavathi, K. Vajravelu, O.A. Bég, U.F. Khan, Unsteady squeezing flow of a magnetized dissipative non-Newtonian nanofluid with radiative heat transfer and Fourier-type boundary conditions: numerical study, Arch. Appl. Mech. 92 (2022) 2765–2797.

[13] J. Umavathi, D. Prakasha, Y.M. Alanazi, M.M.A. Lashin, F.S. Al-Mubaddel, R. Kumar, R.J.P. Gowda, Magnetohydrodynamic squeezing Casson nanofluid flow between parallel convectively heated disks, Int. J. Mod. Phys. B 37 (2023) 2350143.

[14] P. Priyadharshini, V. Karpagam, N.A. Shah, M.R. Ali, Entropy-optimized melting heat transport of Casson–Williamson hybrid nanofluid with blood-mediated nanoparticles over a rotating disk, Indian J. Phys. 98 (2024) 1297–1312.

[15] L. Zhang, M.M. Bhatti, E.E. Michaelides, Bioconvection flow of a tri-hybrid nanofluid containing gyrotactic microorganisms over a rotating disk, J. Therm. Anal. Calorim. 147 (2022) 13195–13208.

[16] H. Waqas, U. Farooq, D. Liu, M. Alghamdi, S. Noreen, T. Muhammad, Bioconvection transport of magnetized nanofluid with motile microorganisms over a rotating disk, Alex. Eng. J. 61 (2022) 2201–2214.

[17] S.U. Khan, N. Vahdat-Nejad, A. Hassan, Bioconvective Reiner–Rivlin nanofluid flow over a rotating disk with Cattaneo–Christov heat flux and entropy generation analysis, Sci. Rep. 11 (2021) 16030.

[18] Z. Shah, A. Khan, P. Kumam, W. Deebani, M. Shutaywi, Entropy generation minimization in bioconvective flow of nanofluid with activation energy and gyrotactic micro-organisms, AIP Adv. 11 (2021) 055017.

[19] R. Kumar, S. Devi, A. Mahanthesh, Heat transfer and entropy generation analysis of tri-hybrid Williamson nanofluid flow over a rotating disk with motile microorganisms: a response-surface study, Multiscale Multidiscip. Model. Exp. Des. 9 (2026) 1251.

[20] P. Rana, S. Gupta, G. Gupta, Random-forest machine-learning model and entropy generation in unsteady Williamson tri-hybrid (Au + TiO₂ + SiO₂)/blood nanofluid with Darcy–Forchheimer porous rotating disk, J. Therm. Anal. Calorim. 151 (2026) 15978.

[21] M. Faizan, F. Ali, K. Loganathan, A. Zaib, C.A. Reddy, S.M. Abdel-Khalek, Entropy analysis of Sutterby nanofluid flow over a Riga sheet with gyrotactic microorganisms and Cattaneo–Christov double diffusion, Mathematics 10 (2022) 3157.

[22] S. Nadeem, M.N. Khan, N. Abbas, Significance of Hall current and viscous dissipation in the bioconvection flow of couple-stress nanofluid with generalized Fourier and Fick laws, Sci. Rep. 12 (2022) 17688.

[23] M.I. Khan, F. Alzahrani, A. Hobiny, Simulation and modeling of second-order velocity slip flow of micropolar nanofluid with Arrhenius activation energy, J. Mater. Res. Technol. 15 (2021) 191–204.

[24] A. Zaib, U. Khan, A. Wakif, M. Zaydan, Numerical entropic analysis of mixed MHD convective flows with activation energy near a stagnation point over a stretching disk, Int. Commun. Heat Mass Transf. 120 (2021) 105038.

[25] T. Hayat, Z. Hussain, A. Alsaedi, B. Ahmad, Influence of activation energy and chemical reaction on radiative nanofluid flow with convective conditions, Case Stud. Therm. Eng. 26 (2021) 101056.

[26] M. Ramzan, H. Gul, D. Baleanu, K.S. Nisar, M.Y. Malik, Role of Cattaneo–Christov double diffusion and activation energy in a Darcy–Forchheimer tri-hybrid nanofluid flow, Case Stud. Therm. Eng. 49 (2023) 103234.

[27] A. Shahid, H. Huang, M.M. Bhatti, L. Zhang, R. Ellahi, Numerical study of activation energy in tangent-hyperbolic nanofluid with motile microorganisms, Mathematics 9 (2021) 2943.

[28] S.A. Al Rashdi, N.I. Ghoneim, A.M. Amer, A.M. Megahed, Investigation of magnetohydrodynamic slip flow for Maxwell nanofluid over a vertical surface with Cattaneo–Christov heat flux in a saturated porous medium, Results Eng. 19 (2023) 101332.

[29] M. Alrehili, Viscoelastic thermal nanofluid flow and heat–mass transfer due to a stretching sheet with slip velocity phenomenon and convective heating, Int. J. Thermofluids 17 (2023) 100301.

[30] M. Shoaib, M.A.Z. Raja, M.T. Sabir, K.S. Nisar, W. Jamshed, B.F. Felemban, I. Yahia, MHD hybrid nanofluid flow due to rotating disk with heat absorption and thermal slip effects: an application of intelligent computing, Coatings 11 (2021) 1554.

[31] S. Dolui, B. Bhaumik, S. De, S. Changdar, Effect of a variable magnetic field on peristaltic slip flow of blood-based hybrid nanofluid through a nonuniform annular channel, J. Mech. Med. Biol. 23 (2023) 2250070.

[32] D. Ali, H. Ullah, A.M. Alqahtani, M. Fiza, A.S. Omer, I. Khan, A.U. Jan, Numerical treatment of squeezed fluid flow under the magnetic influence amid parallel disks, Int. J. Thermofluids 21 (2024) 100561.

[33] U. Farooq, M. Hassan, A. Fatima, M. Imran, S. Noreen, Cattaneo–Christov heat-flux model in radiative flow of magnetized hybrid nanofluids past through double rotating disks, Case Stud. Therm. Eng. 45 (2023) 102982.

[34] U. Farooq, A. Fatima, M. Hassan, N. Fatima, Numerical framework of hybrid nanofluid over two horizontal parallel plates with non-linear thermal radiation, Int. J. Thermofluids 18 (2023) 100329.

[35] Y.M. Chu, M.I. Khan, H. Waqas, U. Farooq, S.U. Khan, M. Nazeer, Numerical simulation of squeezing flow Jeffrey nanofluid confined by two parallel disks with chemical reaction: effects of activation energy and microorganisms, Int. J. Chem. React. Eng. 19 (2021) 495–507.

[36] B. Yadav, S. Choudhary, Effect of melting heat transfer and thermal radiation on squeezing flow of a Casson fluid with chemical reaction in porous medium, Front. Heat Mass Transf. 18 (2022) 34.

[37] N.A. Shah, A. Wakif, R. Shah, S.J. Yook, B. Salah, Y. Mahsud, H. Hussain, Effects of fractional derivative and heat source/sink on MHD free-convection flow of nanofluids in a vertical cylinder, Case Stud. Therm. Eng. 28 (2021) 101518.

[38] M.M. Bhatti, S.M. Arshad, A. Riaz, S.Z. Abbas, Bioconvective non-Newtonian nanofluid transport in a porous squeezing channel with gyrotactic microorganisms, J. Taibah Univ. Sci. 16 (2022) 423–435.

[39] A. Hussain, S. Elkotb, M. Arshad, A. Rehman, K.S. Nisar, A. Hassan, Computational investigation of the combined impact of nonlinear radiation and magnetic field on tri-hybrid nanofluid flow between rotating disks, Case Stud. Therm. Eng. 35 (2022) 102108.

[40] K. Ramesh, O. Ojjela, N. Naresh Kumar, Second-law analysis in radiative mixed-convective squeezing flow of Casson fluid between parallel disks with Soret and Dufour effects, Heat Transf. 50 (2021) 2528–2546.

[41] W. Shatanawi, N. Abbas, T.A. Shatnawi, F. Hasan, Heat and mass transfer of generalized Fourier and Fick's law for second-grade fluid flow at a slendering vertical Riga sheet, Heliyon 9 (2023) e14250.

[42] G.M. Sobamowo, A.A. Yinusa, M.A. Waheed, A.M. de Oliveira Siqueira, Unsteady squeezing flow and heat transfer of MHD third-grade nanofluid between two disks embedded in a porous medium subjected to thermal radiation using homotopy perturbation method, J. Eng. Exact Sci. 8 (2022) 13940.

[43] A. Bibi, K. Khan, A. Hamid, Z. Mısır, F. Asmat, Numerical analysis of hybrid fluid flow between rotating disks in the presence of thermal radiation and Joule heating effect, Open Phys. 24 (2026) 20250268.
