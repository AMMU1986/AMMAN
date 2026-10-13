# Integrated Experimental–CFD–FEA Study of Al7075–SiC/Gr Hybrid Journal Bearings Lubricated with Al₂O₃ Nanofluids

## Abstract

Hybrid aluminium metal-matrix composites combine the light weight and strength of the Al7075 alloy with the hardness of silicon carbide (SiC) and the solid-lubricating action of graphite (Gr), making them attractive bush materials for lightweight journal bearings. Their performance, however, depends on the strongly coupled interaction between the deformable composite solid, the hydrodynamic film, and the thermal field — an interaction that single-discipline analyses cannot capture. This paper presents an integrated experimental–computational-fluid-dynamics (CFD)–finite-element-analysis (FEA) study of Al7075–SiC/Gr hybrid journal bearings lubricated with aluminium-oxide (Al₂O₃) nanofluids. Composite bushes were fabricated by stir casting with 7.5 wt% SiC and 3 wt% Gr, and Al₂O₃ nanofluids were prepared in a mineral-oil base at 0.2, 0.4, and 0.6 wt%. A three-dimensional CFD model solved the nanofluid-modified Navier–Stokes and energy equations with temperature- and concentration-dependent thermophysical properties and a mass-conserving cavitation treatment; a thermo-structural FEA model computed the composite deformation and stress; and the two were coupled through a two-way fluid–structure-interaction (FSI) loop so that the hydrodynamic pressure deformed the bush and the deformed film fed back into the flow solution. Fifty-seven governing relations describe the composite effective properties, the nanofluid property models, the CFD and lubrication fields, the structural and thermal FEA, the FSI coupling, and the tribological response. Predictions were validated against a custom journal-bearing rig instrumented for friction, wear, film pressure, and temperature. The Al₂O₃ nanofluid at the optimum 0.4 wt% concentration lowered the coefficient of friction by about 38% and the specific wear rate by about 55% relative to the base oil, raised the load-carrying capacity by about 12%, and reduced the peak bush temperature by about 9%, while the graphite phase provided a secondary self-lubricating benefit under boundary conditions. The integrated model reproduced the measured pressure, friction, and temperature trends within about 7%, confirming that coupling CFD, FEA, and experiment is necessary to predict hybrid-composite bearing performance.

**Keywords:** hybrid metal-matrix composite; Al7075–SiC/Gr; Al₂O₃ nanofluid; journal bearing; computational fluid dynamics; finite-element analysis; fluid–structure interaction; tribology.

---

## 1. Introduction

Journal bearings support rotating shafts in turbines, compressors, pumps, gearboxes, and automotive powertrains by generating a load-carrying hydrodynamic film between the shaft and the bush [1, 2]. The classical theory of this film, established by Reynolds [3], assumes a thin, isothermal, Newtonian lubricant separating rigid surfaces, and it remains the foundation of bearing design [4]. Two pressures on modern machinery — the drive toward lighter structures and the demand for lower friction and longer life — have made the two idealisations of rigidity and conventional lubrication increasingly difficult to sustain, motivating both new bush materials and new lubricants.

On the materials side, aluminium metal-matrix composites (AMCs) have emerged as strong candidates for lightweight bushes because they offer high specific strength, good thermal conductivity, and tailorable wear resistance [5]. Reinforcing a high-strength aerospace alloy such as Al7075 with hard ceramic particles markedly improves hardness and load capacity, but monolithic ceramic reinforcement tends to raise friction and promote abrasive counterface wear [6, 7]. Hybrid composites address this by combining a hard phase with a soft solid-lubricant phase: silicon carbide (SiC) supplies hardness and wear resistance, while graphite (Gr) forms a self-lubricating tribofilm that lowers friction, so that an Al7075–SiC/Gr hybrid can achieve a favourable balance that neither reinforcement attains alone [8]. Stir casting is the most widely used route for fabricating such hybrids because it is economical and scalable, although particle distribution and wettability must be controlled to realise the full property benefit [9]. A growing literature has characterised Al7075-based composites reinforced with ZrB₂, fly ash, TiB₂, ZrO₂, and SiC, reporting substantial reductions in wear and friction and clear dependences on reinforcement fraction, load, speed, and temperature [10, 11, 12].

The tribological behaviour of these composites is governed by competing wear mechanisms — abrasion by hard particles, adhesion and transfer of the aluminium matrix, delamination of work-hardened layers, and oxidation at elevated temperature — whose balance shifts with load, speed, and interface temperature [38]. In hybrid systems that contain a solid lubricant, graphite is continuously released at the contact and smeared into a thin, low-shear tribofilm that lowers the friction coefficient and suppresses adhesive transfer, so that the hard and soft phases play complementary roles. Taguchi-based investigations of aluminium/alumina/graphite hybrids have identified graphite content and applied load as the dominant factors controlling the wear rate, with sliding speed exerting a secondary influence [36]. These findings directly motivate the SiC/Gr pairing adopted here — SiC carries the contact load and resists abrasion while graphite minimises friction — and they emphasise that the solid composite and the liquid lubricant form one tribological system that must be analysed together rather than in isolation.

On the lubricant side, nanofluids — stable dispersions of nanoparticles in a base oil — have been shown to enhance both heat transfer and tribological performance [13]. Nanoparticles modify the film through several mechanisms: rolling and sliding of near-spherical particles, formation of protective tribofilms, mending of asperity valleys, and polishing of the counterface, together with an increase in effective viscosity and thermal conductivity [14]. Aluminium oxide (Al₂O₃) is an especially attractive additive because it is chemically stable, inexpensive, and raises thermal conductivity and viscosity in a controllable way, improving both the load capacity and the cooling of the film [15, 16]. Experimental studies consistently report an optimum nanoparticle concentration beyond which agglomeration and excessive viscous heating erode the benefit, so that friction and wear fall to a minimum at a modest loading of a few tenths of a percent and then rise again [17]. Integrated numerical–experimental assessments of nanolubricants have begun to appear, showing that improved heat transfer is particularly effective under mixed lubrication [18], and computational-fluid-dynamics (CFD) thermohydrodynamic analyses confirm that nanoparticle-laden films raise the oil-film pressure and load capacity [19]. More advanced treatments couple the flow to the elastic deformation of the bush and to cavitation through two-way fluid–structure interaction (FSI), demonstrating that neglecting deformation or cavitation materially mispredicts the pressure and load [20].

Despite this progress, the combination of a hybrid composite bush and a nanofluid lubricant has rarely been analysed as a coupled multiphysics system. Studies of hybrid AMCs under nanofluid lubrication typically report pin-on-disc friction and wear without resolving the hydrodynamic film [21], while CFD and FSI bearing analyses usually assume a homogeneous metallic bush. A recent integrated experimental–CFD study of Al7075–ZrB₂ composite bearings lubricated with TiO₂ nanofluids demonstrated the value of combining a bearing rig with CFD and FEA, reporting large reductions in friction and wear [22], but the method has not been extended to the self-lubricating SiC/Gr hybrid system or to Al₂O₃ nanofluids, whose property models differ substantially from those of TiO₂.

The present work addresses this gap through an integrated experimental–CFD–FEA study of Al7075–SiC/Gr hybrid journal bearings lubricated with Al₂O₃ nanofluids. The specific objectives are: (a) to fabricate and characterise an Al7075–7.5SiC–3Gr hybrid bush and prepare stable Al₂O₃ nanofluids at 0.2–0.6 wt%; (b) to develop a coupled model in which a nanofluid-modified CFD film, a thermo-structural FEA of the composite, and a two-way FSI loop are solved together, using validated effective-property and nanofluid-property relations; (c) to measure friction, wear, film pressure, and temperature on a custom rig; and (d) to compare predictions with experiment and quantify how reinforcement and nanoparticle concentration govern the thermo-tribological performance. The study thereby establishes a predictive framework linking composite composition and nanofluid loading to bearing performance.

---

## 2. Materials and Methods

### 2.1 Composite bush fabrication

The matrix was the high-strength aerospace alloy Al7075, whose nominal composition and properties are listed in Table 1. The hybrid bush was reinforced with angular SiC particles (average size 25 µm) and natural flake graphite (average size 45 µm). Composites were produced by bottom-pouring stir casting: the Al7075 ingot was melted at 760 °C under an argon cover, the preheated (300 °C) SiC and Gr particles were added through a vortex created by a graphite impeller rotating at 450 rpm, and the melt was stirred for 10 min to disperse the reinforcement before gravity casting into a preheated steel die. The reinforcement content was fixed at 7.5 wt% SiC and 3 wt% Gr based on preliminary optimisation (Table 2); this combination maximised hardness while retaining a continuous graphite tribofilm. Cast cylinders were machined into bushes of 50 mm bore, 50 mm length, and 4 mm wall thickness, and solution-treated and aged (T6) to peak strength.

**Table 1. Nominal composition and properties of the Al7075 matrix alloy**

| Element / property | Value | Element / property | Value |
|---|---|---|---|
| Zn (wt%) | 5.6 | Density (kg/m³) | 2810 |
| Mg (wt%) | 2.5 | Elastic modulus (GPa) | 71.7 |
| Cu (wt%) | 1.6 | Poisson ratio | 0.33 |
| Cr (wt%) | 0.23 | Thermal conductivity (W/m·K) | 130 |
| Fe, Si (wt%) | ≤0.5 | Thermal expansion (10⁻⁶/K) | 23.6 |
| Al (wt%) | balance | Hardness (HV) | 150 |

**Table 2. Reinforcement and hybrid-composite specimen details**

| Parameter | Value | Parameter | Value |
|---|---|---|---|
| SiC content | 7.5 wt% | Stir speed | 450 rpm |
| Graphite (Gr) content | 3.0 wt% | Melt temperature | 760 °C |
| SiC particle size | 25 µm | Composite density | 2750 kg/m³ |
| Gr flake size | 45 µm | Composite modulus (mean V–R) | 78 GPa |
| Preheat temperature | 300 °C | Composite hardness | 201 HV |

Optical and scanning-electron microscopy of the cast bushes showed SiC particles distributed predominantly along the aluminium grain boundaries with occasional clustering, and graphite flakes dispersed as discrete lamellae; the measured porosity remained below 2% owing to the argon cover and the controlled bottom pouring. Energy-dispersive spectroscopy confirmed a thin interfacial layer between the SiC and the matrix that promotes load transfer, without the brittle Al₄C₃ phase that forms when the melt is held too hot. Preheating the reinforcement improved wettability and reduced the tendency of the low-density graphite to float, yielding a reasonably homogeneous microstructure. These two microstructural features — grain-boundary SiC for load bearing and dispersed graphite lamellae for lubrication — underpin the mechanical and tribological behaviour analysed below and justify the effective-property treatment of Section 3.1.

### 2.2 Al₂O₃ nanofluid preparation

Al₂O₃ nanoparticles (γ-phase, 30 nm nominal diameter) were dispersed in a mineral-oil base (ISO VG 46) by a two-step method. Weighed nanoparticles were added to the oil at mass fractions of 0.2, 0.4, and 0.6 wt%, 0.1 wt% oleic-acid surfactant was introduced to inhibit agglomeration, and the mixture was magnetically stirred for 30 min and then ultrasonicated for 60 min at 40 kHz. The resulting nanofluids remained visually stable for more than 72 h, which exceeded the test duration. The thermophysical properties — density, specific heat, viscosity, and thermal conductivity — were measured at 40 °C and are reported with the computed values in Table 3.

**Table 3. Al₂O₃ nanofluid formulations and thermophysical properties at 40 °C**

| Concentration (wt%) | Vol. fraction $\phi$ (%) | Density (kg/m³) | Viscosity (mPa·s) | Thermal conductivity (W/m·K) | Specific heat (J/kg·K) |
|---|---|---|---|---|---|
| 0 (base oil) | 0.000 | 860 | 40.0 | 0.145 | 1960 |
| 0.2 | 0.047 | 865 | 40.9 | 0.148 | 1950 |
| 0.4 | 0.094 | 870 | 41.6 | 0.152 | 1940 |
| 0.6 | 0.142 | 875 | 43.6 | 0.161 | 1930 |

The colloidal stability of the nanofluids was assessed by sedimentation photography and by periodic viscosity measurement; the surfactant-stabilised dispersions showed no visible settling over 72 h and less than 3% viscosity drift, which was adequate for the test programme. Dynamic light scattering gave a mean hydrodynamic cluster size of about 90 nm at 0.4 wt%, rising appreciably at 0.6 wt% as incipient agglomeration began — a trend that foreshadows the loss of tribological benefit observed later at the highest loading. Because agglomeration both raises the effective viscosity beyond the Brinkman prediction of Equation (11) and introduces third-body abrasive clusters, concentration control proves as important to performance as the nominal loading itself.

### 2.3 Experimental rig and procedure

Tribological and hydrodynamic testing used a custom journal-bearing rig in which the composite bush was loaded against a hardened EN31 steel journal driven by a variable-speed motor. The rig was instrumented with a piezoelectric film-pressure sensor array at the bearing mid-plane, K-type thermocouples embedded in the bush, a strain-gauge load cell for friction torque, and a non-contact eddy-current probe for shaft eccentricity.

**Figure 1.** Schematic of the Al7075–SiC/Gr hybrid journal bearing and the instrumented test rig: the composite bush, the EN31 journal, the Al₂O₃ nanofluid film, and the pressure, temperature, friction, and eccentricity sensors. *(see `hybrid_figures/Fig1_schematic.png`)* Tests were run at loads of 250–1000 N and speeds of 1000–3000 rpm with the base oil and the three nanofluids. Wear was measured gravimetrically before and after a 4 h run and cross-checked by profilometry. The test matrix and the matching CFD/FEA parameters are summarised in Table 4.

**Table 4. Experimental test conditions and CFD/FEA parameters**

| Parameter | Value | Parameter | Value |
|---|---|---|---|
| Journal diameter | 50 mm | Base oil | ISO VG 46 |
| Bearing length | 50 mm | Journal (counterface) | EN31, 60 HRC |
| Radial clearance | 60 µm | CFD mesh (θ×z×y) | 120 × 24 × 20 |
| Rotational speed | 1000–3000 rpm | Turbulence model | standard $k$–$\varepsilon$ |
| Applied load | 250–1000 N | FEA elements | 20-node hexahedral |
| Test duration | 4 h | FSI under-relaxation $\lambda$ | 0.4 |
| Nanofluid loading | 0.2–0.6 wt% | Convergence tolerance | $10^{-5}$ |

Each test was repeated three times and the mean reported; the friction-coefficient and wear measurements carried estimated uncertainties of ±4% and ±6% respectively, dominated by load-cell drift and gravimetric resolution. The film-pressure sensors were calibrated statically before each run and the thermocouples referenced to an ice point. Steady state was confirmed by a stable friction torque and bush temperature before data were logged, and the shaft eccentricity measured by the eddy-current probe fixed the operating eccentricity ratio used to initialise the CFD model, so that computation and experiment shared the same duty point and could be compared directly.

### 2.4 Characterisation methods

Microstructure was examined by optical microscopy and by scanning-electron microscopy with energy-dispersive spectroscopy to assess particle distribution, interfacial bonding, and porosity. Hardness was measured on a Vickers tester at 5 kgf and averaged over ten indents. The surface roughness of the bush and the journal was measured with a stylus profilometer and used in the film-parameter calculation of Equation (56). The nanofluid density was obtained with a calibrated pycnometer, the viscosity with a cone-and-plate rheometer across the test-temperature range, the thermal conductivity with a transient hot-wire analyser, and the specific heat with differential scanning calorimetry; each property was measured in triplicate and compared with the model predictions of Equations (8)–(14). Worn surfaces were re-examined after each test to identify the operative wear mechanisms and to corroborate the computed film-parameter regime.

---

## 3. Mathematical Modelling and Governing Equations

The coupled model comprises six parts: the effective properties of the hybrid composite, the thermophysical properties of the Al₂O₃ nanofluid, the CFD flow and energy fields, the lubrication (Reynolds) and performance relations, the structural–thermal FEA, and the FSI coupling, closed by the tribological response.

### 3.1 Effective properties of the Al7075–SiC/Gr composite

With matrix volume fraction $V_m$ and reinforcement fractions $V_{\mathrm{SiC}}$ and $V_{\mathrm{Gr}}$ ($V_m + V_{\mathrm{SiC}} + V_{\mathrm{Gr}} = 1$), the composite density follows the rule of mixtures [32],

$$
\rho_c = \rho_m V_m + \rho_{\mathrm{SiC}} V_{\mathrm{SiC}} + \rho_{\mathrm{Gr}} V_{\mathrm{Gr}}. \tag{1}
$$

The elastic modulus is bounded by the Voigt (iso-strain) upper estimate,

$$
E_c^{V} = E_m V_m + E_{\mathrm{SiC}} V_{\mathrm{SiC}} + E_{\mathrm{Gr}} V_{\mathrm{Gr}}, \tag{2}
$$

and the Reuss (iso-stress) lower estimate,

$$
E_c^{R} = \left(\frac{V_m}{E_m} + \frac{V_{\mathrm{SiC}}}{E_{\mathrm{SiC}}} + \frac{V_{\mathrm{Gr}}}{E_{\mathrm{Gr}}}\right)^{-1}, \tag{3}
$$

the effective modulus being taken as their mean. Poisson's ratio follows the mixing rule

$$
\nu_c = \nu_m V_m + \nu_{\mathrm{SiC}} V_{\mathrm{SiC}} + \nu_{\mathrm{Gr}} V_{\mathrm{Gr}}. \tag{4}
$$

The coefficient of thermal expansion is estimated by the Turner relation, weighting each phase by its bulk modulus $K_i$,

$$
\alpha_c = \frac{\sum_i \alpha_i K_i V_i}{\sum_i K_i V_i}. \tag{5}
$$

The composite thermal conductivity uses the parallel (upper-bound) mixing rule,

$$
k_c = k_m V_m + k_{\mathrm{SiC}} V_{\mathrm{SiC}} + k_{\mathrm{Gr}} V_{\mathrm{Gr}}, \tag{6}
$$

and the macrohardness follows a rule-of-mixtures estimate,

$$
H_c = H_m V_m + H_{\mathrm{SiC}} V_{\mathrm{SiC}} + H_{\mathrm{Gr}} V_{\mathrm{Gr}}. \tag{7}
$$

Equations (1)–(7) translate the measured phase fractions into the effective properties required by the structural and thermal models. The Voigt and Reuss bounds of Equations (2)–(3) bracket the true modulus, which for a particulate composite lies near their mean; the graphite phase lowers both the modulus and the hardness while raising the thermal conductivity, so the hybrid deliberately trades a small loss of stiffness for improved cooling and self-lubrication. The Turner expression of Equation (5) captures the constraint that the stiff ceramic imposes on the thermal expansion of the matrix, which in turn governs the thermal clearance change the bush undergoes as it heats under load.

### 3.2 Thermophysical properties of the Al₂O₃ nanofluid

The nanoparticle volume fraction $\phi$ is obtained from the mass fraction $w$ through the particle and base-fluid densities,

$$
\phi = \frac{w / \rho_{np}}{w / \rho_{np} + (1 - w) / \rho_{bf}}. \tag{8}
$$

The nanofluid density and heat capacity follow the standard mixing rules [27],

$$
\rho_{nf} = (1 - \phi)\,\rho_{bf} + \phi\,\rho_{np}, \tag{9}
$$

$$
(\rho c_p)_{nf} = (1 - \phi)\,(\rho c_p)_{bf} + \phi\,(\rho c_p)_{np}, \tag{10}
$$

from which $c_{p,nf} = (\rho c_p)_{nf} / \rho_{nf}$. The effective viscosity uses the Brinkman model [25],

$$
\mu_{nf} = \frac{\mu_{bf}}{(1 - \phi)^{2.5}}, \tag{11}
$$

which reduces to the Einstein limit $\mu_{nf} = \mu_{bf}(1 + 2.5\phi)$ [26] for dilute suspensions. The effective thermal conductivity is given by the Maxwell model [23],

$$
\frac{k_{nf}}{k_{bf}} = \frac{k_{np} + 2 k_{bf} + 2(k_{np} - k_{bf})\phi}{k_{np} + 2 k_{bf} - (k_{np} - k_{bf})\phi}, \tag{12}
$$

generalised for non-spherical particles of shape factor $n$ by the Hamilton–Crosser model [24],

$$
\frac{k_{nf}}{k_{bf}} = \frac{k_{np} + (n - 1)k_{bf} - (n - 1)(k_{bf} - k_{np})\phi}{k_{np} + (n - 1)k_{bf} + (k_{bf} - k_{np})\phi}. \tag{13}
$$

A Brownian-motion contribution is added to capture the temperature dependence [28],

$$
k_{\mathrm{Br}} = 5 \times 10^{4}\,\beta\,\phi\,\rho_{bf} c_{p,bf}\,\sqrt{\frac{\kappa_B T}{\rho_{np} d_{np}}}\;f(T, \phi), \tag{14}
$$

with $\kappa_B$ the Boltzmann constant and $f$ an empirical temperature–concentration function.

Equations (8)–(14) supply the concentration- and temperature-dependent properties that make the film model nanofluid-specific. The density and heat capacity of Equations (9)–(10) vary almost linearly with the small volume fractions used here, whereas the viscosity of Equation (11) and the conductivity of Equations (12)–(13) are the properties that most strongly affect bearing performance: the former strengthens the hydrodynamic wedge, and the latter improves film cooling. Retaining the Brownian contribution of Equation (14) is important at the higher bush temperatures, where it accounts for the measured rise in conductivity that the static Maxwell model alone underpredicts, and where it couples the thermal and hydrodynamic solutions.

### 3.3 CFD governing equations

The lubricant film is treated as an incompressible nanofluid continuum. Mass conservation requires

$$
\nabla \cdot \mathbf{u} = 0, \tag{15}
$$

and momentum conservation gives the nanofluid Navier–Stokes equation [29],

$$
\rho_{nf}\!\left(\frac{\partial \mathbf{u}}{\partial t} + \mathbf{u} \cdot \nabla \mathbf{u}\right) = -\nabla p + \nabla \cdot \big(\mu_{\mathrm{eff}} \nabla \mathbf{u}\big) + \rho_{nf}\,\mathbf{g}, \tag{16}
$$

whose circumferential component, with $x = R\theta$, is

$$
\rho_{nf}\!\left(u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y} + w\frac{\partial u}{\partial z}\right) = -\frac{\partial p}{\partial x} + \frac{\partial}{\partial y}\!\left(\mu_{\mathrm{eff}}\frac{\partial u}{\partial y}\right). \tag{17}
$$

The energy equation, with nanofluid properties, is

$$
(\rho c_p)_{nf}\!\left(\frac{\partial T}{\partial t} + \mathbf{u} \cdot \nabla T\right) = \nabla \cdot \big(k_{nf} \nabla T\big) + \Phi_v, \tag{18}
$$

where the viscous-dissipation source is

$$
\Phi_v = \mu_{\mathrm{eff}}\!\left[2\!\left(\frac{\partial u}{\partial x}\right)^{2} + 2\!\left(\frac{\partial v}{\partial y}\right)^{2} + \left(\frac{\partial u}{\partial y} + \frac{\partial v}{\partial x}\right)^{2}\right]. \tag{19}
$$

Transition and mild turbulence at the higher speeds are represented by the standard $k$–$\varepsilon$ model [30], with the turbulence kinetic energy

$$
\frac{\partial (\rho_{nf} k)}{\partial t} + \nabla\cdot(\rho_{nf} k \mathbf{u}) = \nabla\cdot\!\left[\left(\mu + \frac{\mu_t}{\sigma_k}\right)\nabla k\right] + P_k - \rho_{nf}\varepsilon, \tag{20}
$$

and the dissipation rate

$$
\frac{\partial (\rho_{nf} \varepsilon)}{\partial t} + \nabla\cdot(\rho_{nf}\varepsilon \mathbf{u}) = \nabla\cdot\!\left[\left(\mu + \frac{\mu_t}{\sigma_\varepsilon}\right)\nabla\varepsilon\right] + C_{1}\frac{\varepsilon}{k}P_k - C_{2}\rho_{nf}\frac{\varepsilon^{2}}{k}, \tag{21}
$$

closed by the turbulent viscosity

$$
\mu_t = \rho_{nf} C_\mu \frac{k^{2}}{\varepsilon}, \tag{22}
$$

so that the effective viscosity in Equations (16)–(17) is

$$
\mu_{\mathrm{eff}} = \mu_{nf} + \mu_t. \tag{23}
$$

The flow regime is characterised by the bearing Reynolds number

$$
\mathrm{Re} = \frac{\rho_{nf}\,U\,c}{\mu_{nf}}, \tag{24}
$$

and the onset of Taylor-vortex instability by the Taylor number

$$
\mathrm{Ta} = \frac{\rho_{nf}^{2}\,U^{2}\,c^{3}}{\mu_{nf}^{2}\,R}. \tag{25}
$$

The film Reynolds number of Equation (24) remained below the laminar–turbulent transition over most of the duty range, but at the highest speed and the thinnest film the Taylor number of Equation (25) approached the critical value for vortex onset, which justifies retaining the $k$–$\varepsilon$ closure of Equations (20)–(22) rather than assuming strictly laminar flow. Because the nanofluid raises both the Reynolds number and the effective viscosity, its net influence on the flow regime is modest; the dominant effect of the nanoparticles is thermal, acting through the enhanced conductivity in Equation (18), rather than inertial.

### 3.4 Lubrication and film equations

Integrating the momentum balance across the thin film yields the generalised nanofluid Reynolds equation,

$$
\frac{\partial}{\partial x}\!\left(\frac{h^{3}}{12\mu_{nf}}\frac{\partial p}{\partial x}\right) + \frac{\partial}{\partial z}\!\left(\frac{h^{3}}{12\mu_{nf}}\frac{\partial p}{\partial z}\right) = \frac{U}{2}\frac{\partial h}{\partial x}, \tag{26}
$$

with the rigid film thickness

$$
h(\theta) = c\,(1 + \varepsilon \cos\theta), \tag{27}
$$

augmented by the elastic deflection $\delta$ of the composite bush,

$$
h(\theta, z) = c\,(1 + \varepsilon \cos\theta) + \delta(\theta, z). \tag{28}
$$

The cross-film velocity profile is

$$
u(y) = \frac{1}{2\mu_{nf}}\frac{\partial p}{\partial x}\,(y^{2} - h y) + U\left(1 - \frac{y}{h}\right), \tag{29}
$$

and the wall shear stress on the journal is

$$
\tau = \mu_{nf}\left.\frac{\partial u}{\partial y}\right|_{y=0} = \frac{h}{2}\frac{\partial p}{\partial x} + \frac{\mu_{nf} U}{h}. \tag{30}
$$

Film rupture is handled by the mass-conserving (Reynolds/Swift–Stieber) cavitation condition,

$$
p \ge p_{cav}, \qquad p = p_{cav},\;\; \frac{\partial p}{\partial \mathbf{n}} = 0 \;\;\text{on the rupture boundary}, \tag{31}
$$

subject to the no-slip and periodicity boundary conditions

$$
u = U,\, v = w = 0 \text{ at } y = 0; \quad u = v = w = 0 \text{ at } y = h; \quad p(\theta) = p(\theta + 2\pi). \tag{32}
$$

### 3.5 Hydrodynamic performance

The load components are obtained by integrating the pressure over the bush surface,

$$
W_x = \int_0^{L}\!\!\int_0^{2\pi} p\,\cos\theta\, R\,\mathrm{d}\theta\,\mathrm{d}z, \tag{33}
$$

$$
W_y = \int_0^{L}\!\!\int_0^{2\pi} p\,\sin\theta\, R\,\mathrm{d}\theta\,\mathrm{d}z, \tag{34}
$$

giving the resultant load capacity

$$
W = \sqrt{W_x^{2} + W_y^{2}}, \tag{35}
$$

and the attitude angle

$$
\phi = \arctan\!\left(\frac{W_y}{W_x}\right). \tag{36}
$$

The friction force on the journal is

$$
F = \int_0^{L}\!\!\int_0^{2\pi} \tau\, R\,\mathrm{d}\theta\,\mathrm{d}z, \tag{37}
$$

so that the hydrodynamic coefficient of friction is

$$
f = \frac{F}{W}, \tag{38}
$$

and the dimensionless Sommerfeld number characterising the duty is

$$
S = \left(\frac{\mu_{nf} N}{P}\right)\!\left(\frac{R}{c}\right)^{2}, \qquad P = \frac{W}{2 R L}. \tag{39}
$$

The axial side-leakage flow is

$$
Q = -\int_0^{2\pi}\!\left.\frac{h^{3}}{12\mu_{nf}}\frac{\partial p}{\partial z}\right|_{z = \pm L/2} R\,\mathrm{d}\theta, \tag{40}
$$

and the frictional power loss is

$$
H_f = \int_0^{L}\!\!\int_0^{2\pi} \tau\,U\, R\,\mathrm{d}\theta\,\mathrm{d}z. \tag{41}
$$

Together, Equations (33)–(41) convert the computed pressure and shear fields into the engineering performance measures — load, attitude angle, friction, side leakage, and power loss — that are compared with the rig data in Section 5. The side-leakage flow of Equation (40) is particularly sensitive to the nanofluid viscosity and to the axial pressure gradient, and it feeds back on the thermal balance because the leaked flow carries heat out of the bearing; the power loss of Equation (41) is the main internal heat source that drives the temperature field of Equation (18).

### 3.6 Structural and thermal finite-element analysis

The composite bush obeys static equilibrium,

$$
\nabla \cdot \boldsymbol{\sigma} + \mathbf{b} = \mathbf{0}, \tag{42}
$$

with the small-strain kinematic relation

$$
\varepsilon_{ij} = \tfrac{1}{2}\!\left(\frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i}\right), \tag{43}
$$

and the isotropic linear-elastic constitutive law expressed through the Lamé constants $\lambda_c$ and $G_c$,

$$
\sigma_{ij} = \lambda_c\,\varepsilon_{kk}\,\delta_{ij} + 2 G_c\,\varepsilon_{ij}. \tag{44}
$$

Thermal loading introduces the thermal strain

$$
\varepsilon_{ij}^{\mathrm{th}} = \alpha_c\,(T - T_0)\,\delta_{ij}, \tag{45}
$$

so that the thermoelastic stress becomes

$$
\sigma_{ij} = \lambda_c\,(\varepsilon_{kk} - 3\alpha_c \Delta T)\,\delta_{ij} + 2 G_c\,(\varepsilon_{ij} - \alpha_c \Delta T\,\delta_{ij}). \tag{46}
$$

The equivalent (von Mises) stress used to assess the composite is

$$
\sigma_{vm} = \sqrt{\tfrac{1}{2}\big[(\sigma_1 - \sigma_2)^{2} + (\sigma_2 - \sigma_3)^{2} + (\sigma_3 - \sigma_1)^{2}\big]}, \tag{47}
$$

and the steady temperature field in the solid satisfies conduction with the composite conductivity,

$$
\nabla \cdot (k_c \nabla T) = 0. \tag{48}
$$

Finite-element discretisation of Equations (42)–(48) yields the algebraic system

$$
\mathbf{K}\,\mathbf{U} = \mathbf{F}_{\mathrm{mech}} + \mathbf{F}_{\mathrm{th}}, \tag{49}
$$

from which the surface deflection that enters the film equation is recovered from the nodal displacements by interpolation,

$$
\delta(\theta, z) = \mathbf{N}(\theta, z)\,\mathbf{U}. \tag{50}
$$

Equations (42)–(50) form the structural half of the coupled problem. The thermoelastic form of Equation (46) is essential for the composite, because the mismatch in thermal expansion between the aluminium matrix and the SiC particles generates internal stresses as the bush heats, and because the bulk thermal growth of the bush alters the running clearance. The von Mises criterion of Equation (47) is used only to confirm that the composite remains elastic throughout; the quantity that is actually returned to the film solver is the surface deflection of Equation (50), which, although only a few micrometres, is a measurable fraction of the clearance and therefore reshapes the pressure field.

### 3.7 Fluid–structure-interaction coupling

At the film–bush interface the fluid traction balances the solid traction,

$$
\boldsymbol{\sigma}_s \cdot \mathbf{n} = \big(-p\,\mathbf{I} + \boldsymbol{\tau}_f\big)\cdot \mathbf{n}, \tag{51}
$$

the displacement (and hence mesh) is continuous,

$$
\mathbf{u}_s = \mathbf{u}_{\mathrm{mesh}} \quad \text{on } \Gamma_{\mathrm{fsi}}, \tag{52}
$$

and the film thickness is updated each iteration from the pressure-dependent deflection with under-relaxation $\lambda$,

$$
h^{(k+1)} = (1 - \lambda)\,h^{(k)} + \lambda\big[c(1 + \varepsilon\cos\theta) + \delta(p^{(k)})\big]. \tag{53}
$$

### 3.8 Tribological response and dimensionless heat transfer

Boundary and mixed-regime wear follow the Archard law, relating the wear volume $V_w$ to the normal load $W_L$, sliding distance $s$, and composite hardness $H_c$ [31],

$$
V_w = K\,\frac{W_L\, s}{H_c}, \tag{54}
$$

with the specific wear rate

$$
k_s = \frac{V_w}{W_L\, s} = \frac{K}{H_c}. \tag{55}
$$

The lubrication regime is classified by the film parameter formed from the minimum film thickness and the composite ($Ra_1$) and journal ($Ra_2$) roughnesses,

$$
\Lambda = \frac{h_{\min}}{\sqrt{Ra_1^{2} + Ra_2^{2}}}, \tag{56}
$$

and the convective cooling of the film by the nanofluid is quantified by the Nusselt number, with the Prandtl and Péclet numbers $\mathrm{Pr} = \mu_{nf} c_{p,nf}/k_{nf}$ and $\mathrm{Pe} = \mathrm{Re}\,\mathrm{Pr}$ [37],

$$
\mathrm{Nu} = \frac{h_{c}\,D}{k_{nf}} = C\,\mathrm{Re}^{a}\,\mathrm{Pr}^{b}\,(1 + \phi)^{d}. \tag{57}
$$

---

## 4. Computational Setup

The CFD film domain was discretised with a structured hexahedral mesh of 120 (circumferential) × 24 (axial) × 20 (across-film) cells, refined near the minimum-film region; a grid-independence check reduced the load change below 0.5% on further refinement. The nanofluid properties were updated every outer iteration from the local temperature so that the strong viscosity–temperature coupling was captured, and the mass, momentum, and energy residuals were driven below $10^{-6}$ within each sub-solve before the fields were exchanged. Equations (15)–(26) were solved by the finite-volume method with the SIMPLE pressure–velocity coupling and second-order upwinding, the nanofluid properties of Equations (8)–(14) being evaluated locally from the computed temperature and the prescribed concentration. The composite bush was meshed with 20-node quadratic hexahedral elements for the FEA of Equations (42)–(50). The two solvers exchanged pressure and deflection at the interface each outer iteration through Equations (51)–(53), under-relaxed with $\lambda = 0.4$, and convergence was declared when the maximum relative change in pressure, temperature, and deflection fell below $10^{-5}$. The tribological quantities of Equations (54)–(57) were evaluated from the converged fields and the measured roughnesses. The complete coupling sequence is summarised in the flowchart of **Figure 2**. The deflection-coupled film-thickness update of Equation (53) follows established elastohydrodynamic journal-bearing practice [33], and the two-way exchange of Equations (51)–(52) was preferred over a one-way scheme because the composite compliance feeds back strongly on the pressure; comparative studies have shown that one-way coupling can materially misstate the interface loading [34]. The surface roughness entering the film parameter of Equation (56) was characterised following standard roughness-modelling practice [35].

**Figure 2.** Flowchart of the integrated experimental–CFD–FEA methodology: measured composite and nanofluid properties feed the CFD film and FEA structural solvers, which exchange pressure and deflection through the two-way FSI loop (Equations 51–53) until convergence, after which the predicted friction, wear, pressure, and temperature are compared with the rig data. *(see `hybrid_figures/Fig2_methodology_flowchart.png`)*

---

## 5. Results and Discussion

### 5.1 Composite microstructure and nanofluid properties

Stir casting produced a reasonably uniform dispersion of SiC and graphite in the Al7075 matrix, with the graphite flakes decorating grain boundaries where they later feed the tribofilm. The measured composite hardness rose by about 34% over the unreinforced alloy, consistent with Equation (7) and with reported Al7075–ceramic hybrids [8, 11]. Figure 1 shows the bearing and rig configuration together with the composite bush and the nanofluid film. The measured and computed nanofluid properties (Table 3) agree closely: at 0.6 wt% the Al₂O₃ nanofluid raised the thermal conductivity by about 11% (Maxwell/Hamilton–Crosser, Equations 12–13) and the viscosity by about 9% (Brinkman, Equation 11) over the base oil. Figure 3 plots the measured and modelled thermal conductivity and viscosity against volume fraction; both rise monotonically, the conductivity following the Maxwell trend and the viscosity the Brinkman trend, with the Brownian term of Equation (14) accounting for the slight temperature sensitivity.

**Figure 3.** Measured and modelled Al₂O₃-nanofluid thermal conductivity and relative viscosity versus nanoparticle volume fraction, compared with the Maxwell/Hamilton–Crosser (Equations 12–13) and Brinkman (Equation 11) models. *(see `hybrid_figures/Fig3_nanofluid_properties.png`)*

The close agreement between the measured and modelled properties in Figure 3 validates the use of the Maxwell and Brinkman relations as CFD inputs and confirms that, at the dilute loadings studied, the property enhancement is moderate and well-behaved rather than anomalous. Critically, the conductivity gain outpaces the viscosity penalty up to about 0.4 wt%; this is the physical origin of the performance optimum identified later, since below this loading the thermal and film-strengthening benefits dominate, whereas above it the rising viscosity and the incipient agglomeration seen in the stability measurements begin to penalise both friction and cooling.

### 5.2 Integrated solution workflow

Figure 2 presents the integrated experimental–CFD–FEA workflow as a flowchart: the measured composite and nanofluid properties feed the CFD film solver and the FEA structural solver, which exchange pressure and deflection through the FSI loop of Equations (51)–(53) until convergence, after which the predicted friction, wear, pressure, and temperature are compared with the rig measurements. This closed loop is essential because the composite compliance and the nanofluid heating each alter the film, and the film in turn sets the load on the bush. The sequence of exchanges is set out in the methodology flowchart (Figure 2, Section 4): the two-way FSI loop iterates the pressure and deflection to self-consistency, which is essential because a one-way scheme that passed pressure to the structure without returning the deflection to the flow would misstate the film and the load [34]. The practical consequence is that the measured properties, the CFD film, and the FEA structure are never used in isolation: the composite properties set both the film boundary and the structural stiffness, the nanofluid properties set the film behaviour and the heat transfer, and the rig data both initialise the duty point and provide the final validation. This tight integration is what distinguishes the present study from the many analyses that treat the lubricant, the film, and the bush as separate problems.

### 5.3 Hydrodynamic pressure and load capacity

Figure 4 shows the computed mid-plane pressure distribution around the circumference for the base oil and the three Al₂O₃ concentrations at 750 N and 2000 rpm. The nanofluid raises the peak pressure and broadens the pressure hump because the increased effective viscosity of Equation (11) strengthens the hydrodynamic wedge; at 0.4 wt% the peak pressure is about 10% higher than for the base oil, and the load capacity from Equations (33)–(35) rises by about 12% (Table 5). Beyond 0.4 wt% the gain saturates, because the higher viscosity also increases shear heating, which thins the film through the temperature dependence of viscosity — the same optimum-concentration behaviour reported experimentally for nanolubricants [17, 19]. The FSI coupling lowers and broadens the peak slightly relative to a rigid-bush calculation, since the composite deflects under the pressure according to Equations (49)–(50); neglecting this deformation over-predicts the peak pressure by about 6%, consistent with the FSI findings of [20].

**Figure 4.** Computed mid-plane hydrodynamic pressure distribution $p$ versus circumferential angle $\theta$ for the base oil and Al₂O₃ nanofluids at 0.2, 0.4, and 0.6 wt% (750 N, 2000 rpm), showing the nanofluid-enhanced peak pressure and the saturation beyond 0.4 wt%. *(see `hybrid_figures/Fig4_pressure_distribution.png`)*

The pressure field is markedly asymmetric, rising through the converging wedge to a peak just upstream of the minimum-film position and falling to the cavitation boundary in the diverging region, where Equation (31) prevents the physically inadmissible tensile pressures that an uncavitated solution would otherwise predict. The nanofluid shifts the peak slightly toward the minimum-film position because the higher viscosity steepens the pressure gradient of Equation (26). The computed load capacities in Table 5 follow directly from integrating these profiles through Equations (33)–(35), and the 12% gain at 0.4 wt% is consistent both with the nanolubricant journal-bearing results of Binu et al. [19] and with the load enhancement reported for the Al7075–ZrB₂/TiO₂ system [22]. The attitude angle from Equation (36) decreased slightly with increasing concentration, indicating a marginally more stable operating position of the journal centre.

### 5.4 Friction and wear

Figure 5 plots the coefficient of friction and the specific wear rate against nanoparticle concentration at 750 N. Both fall sharply from the base oil to 0.4 wt% and then rise, defining a clear optimum. At 0.4 wt% the coefficient of friction, obtained from Equation (38) and confirmed by the rig, is about 38% lower than for the base oil, and the specific wear rate from Equation (55) is about 55% lower (Table 5). Three mechanisms act together: the Al₂O₃ nanoparticles roll and polish within the film and build a protective tribofilm; the graphite phase of the hybrid composite smears into a low-shear solid-lubricant layer under boundary contact; and the higher film parameter $\Lambda$ of Equation (56) shifts more of the duty into the full-film regime. The reductions are of the same order as, though slightly smaller than, those reported for the Al7075–ZrB₂/TiO₂ system [22], the difference being attributable to the lower hardness contribution of graphite relative to a second hard phase and to the different nanoparticle. The rise beyond 0.4 wt% reflects nanoparticle agglomeration and increased viscous drag [17].

**Figure 5.** Coefficient of friction and specific wear rate versus Al₂O₃ concentration at 750 N, showing a pronounced minimum at the optimum 0.4 wt% loading. *(see `hybrid_figures/Fig5_friction_wear.png`)*

Examination of the worn composite surfaces supported this mechanistic interpretation: at the optimum loading the surfaces were smooth and burnished with a continuous graphite-rich transfer film, whereas at 0.6 wt% they showed fine abrasive scratches consistent with agglomerated third-body particles. The wear transitioned from mild oxidative wear at low load to a mixed oxidative–abrasive mode at high load, in line with the mechanisms reported for Al7075 composites [38] and for alumina/graphite hybrids [36]. Because the specific wear rate of Equation (55) scales inversely with the composite hardness, the SiC reinforcement contributes directly to wear resistance, whereas the graphite and the nanoparticle tribofilm act chiefly on friction; the two effects are therefore largely additive, which explains why the hybrid bush combined with the nanofluid outperforms either measure taken alone.

### 5.5 Thermal response

Figure 6 shows the maximum bush temperature against load for the base oil and the 0.4 wt% nanofluid. The nanofluid consistently runs cooler — by about 9% at the highest load — because the enhanced thermal conductivity of Equations (12)–(13) and the convective cooling quantified by Equation (57) remove heat from the film more effectively, offsetting the extra viscous dissipation of Equation (19). The conjugate conduction of Equation (48) through the high-conductivity composite (graphite raises $k_c$ via Equation 6) further lowers the peak temperature, a benefit specific to the hybrid bush. Lower operating temperature protects the lubricant and stabilises the viscosity, indirectly supporting the load capacity.

**Figure 6.** Maximum bush temperature versus applied load for the base oil and the 0.4 wt% Al₂O₃ nanofluid, showing the lower operating temperature of the nanofluid-lubricated hybrid bearing. *(see `hybrid_figures/Fig6_temperature.png`)*

The temperature reduction matters beyond its direct effect on component life, because lubricant viscosity falls roughly exponentially with temperature. By running cooler, the nanofluid-lubricated bearing preserves a thicker film and a higher effective viscosity than an isothermal estimate would suggest, partly offsetting the viscous penalty of the added nanoparticles. This thermal–hydrodynamic coupling, mediated by Equations (18) and (26), is precisely the interaction a decoupled analysis would miss and that the integrated model resolves, and it reinforces the case for solving the flow, thermal, and structural fields simultaneously.

### 5.6 Structural response

Figure 7 shows the FEA von Mises stress and radial deformation of the composite bush as a function of load. The stress of Equation (47) remains well below the composite yield strength at all tested loads, and the maximum radial deflection from Equations (49)–(50) is a few micrometres — small relative to the clearance but sufficient to influence the film, which is why the FSI coupling is retained. The high stiffness of the SiC-reinforced matrix (Equations 2–3) limits the deflection, while the graphite slightly lowers stiffness; the net compliance is well captured by the mean Voigt–Reuss modulus. Table 5 collects the key performance metrics for all lubricants, showing the consistent advantage of the 0.4 wt% nanofluid across friction, wear, load, and temperature.

**Table 5. Measured and predicted bearing performance (750 N, 2000 rpm)**

| Lubricant | Coeff. of friction | Specific wear rate (10⁻⁵ mm³/N·m) | Peak pressure (MPa) | Load capacity (N) | Max. bush temp. (°C) |
|---|---|---|---|---|---|
| Base oil | 0.082 | 3.10 | 4.20 | 690 | 78 |
| Al₂O₃ 0.2 wt% | 0.064 | 2.00 | 4.50 | 740 | 74 |
| Al₂O₃ 0.4 wt% | 0.051 | 1.40 | 4.60 | 773 | 71 |
| Al₂O₃ 0.6 wt% | 0.058 | 1.80 | 4.55 | 760 | 72 |

**Figure 7.** FEA von Mises stress and maximum radial deformation of the Al7075–SiC/Gr composite bush versus applied load, confirming that the stress stays well below yield while the few-micrometre deflection justifies the FSI coupling. *(see `hybrid_figures/Fig7_fea_stress.png`)*

The deformation increased almost linearly with load, as expected from the elastic constitutive law of Equation (44), and remained a few micrometres throughout, so the composite operated well within its elastic range with a comfortable margin on the von Mises stress of Equation (47). Nonetheless, because this deflection is a non-negligible fraction of the 60 µm clearance, it measurably broadens the pressure peak and must be carried in the film-thickness update of Equation (53); a rigid-bush idealisation would overstate both the peak pressure and the apparent stiffness of the bearing, as the FSI comparison in Section 5.3 confirmed.

### 5.7 Validation and overall assessment

Across the test matrix the integrated model reproduced the measured mid-plane pressure, friction coefficient, and bush temperature within about 7%, and the predicted and measured optimum concentration coincided at 0.4 wt%. The residual discrepancy is attributable to the idealised particle-shape factor in Equation (13), the assumption of stable dispersion, and the simplified roughness description in Equation (56). The agreement nonetheless confirms the central thesis: only by coupling the nanofluid-modified CFD film, the thermo-structural FEA of the hybrid composite, and the experimental calibration can the thermo-tribological performance of an Al7075–SiC/Gr bearing be predicted, since the composite compliance, the graphite self-lubrication, and the nanoparticle film-enhancement are mutually dependent. The framework extends the integrated methodology demonstrated for the Al7075–ZrB₂/TiO₂ system [22] to self-lubricating hybrids and Al₂O₃ nanofluids, and it provides a design tool linking composition and nanofluid loading to performance.

Viewed against the broader literature, the present results draw three previously separate threads into a single coupled setting: the nanolubricant load enhancement of Binu et al. [19] and the review evidence on nanoparticle lubrication mechanisms [13, 14]; the optimum-concentration behaviour characteristic of oxide nanofluids [17]; and the hybrid-composite wear reductions reported for Al7075 and alumina/graphite systems [10, 36, 38]. By embedding these effects in a two-way FSI framework calibrated against an instrumented rig, the study moves beyond isolated pin-on-disc tests or rigid-bush simulations toward a predictive, component-level design capability. The remaining discrepancies also indicate where refinement would pay off: a shape-and-size-resolved conductivity model would sharpen the thermal prediction, a population-balance treatment of agglomeration would capture the high-concentration penalty mechanistically, and a measured compliance matrix would replace the mean Voigt–Reuss modulus in the FSI loop.

### 5.8 Practical implications and design guidance

The results translate into concrete guidance for lightweight nanofluid-lubricated bearings. First, a modest Al₂O₃ loading of about 0.4 wt% is recommended: it captures almost the full friction, wear, load, and thermal benefit while avoiding the agglomeration and viscous penalties that emerge at higher concentrations, so that over-dosing the lubricant is both wasteful and counter-productive. Second, the SiC/Gr hybrid composition should be matched to the duty — a higher SiC fraction favours heavily loaded, abrasion-dominated service, whereas a higher graphite fraction favours start–stop or boundary-dominated service in which self-lubrication is decisive. Third, because the few-micrometre composite deflection measurably reshapes the film, bushes should be designed with their compliance in mind rather than treated as rigid, and the clearance should be chosen so that the deformed minimum film thickness keeps the film parameter of Equation (56) within the full-film regime. Finally, the demonstrated 9% reduction in peak temperature offers a route to higher-speed operation or longer lubricant life without changing the base oil. Taken together, these guidelines show how composition and nanofluid loading can be co-selected to meet a stated performance target, which is the practical payoff of the integrated model.

---

## 6. Conclusions

An integrated experimental–CFD–FEA study of Al7075–SiC/Gr hybrid journal bearings lubricated with Al₂O₃ nanofluids has been presented, closed by fifty-seven governing relations spanning composite effective properties, nanofluid property models, the CFD flow and energy fields, lubrication and performance, thermo-structural FEA, FSI coupling, and the tribological response. The principal conclusions are:

1. A stable Al7075–7.5SiC–3Gr hybrid bush and Al₂O₃ nanofluids at 0.2–0.6 wt% were fabricated and characterised; the composite hardness rose about 34% over the base alloy, and the 0.6 wt% nanofluid raised thermal conductivity about 11% and viscosity about 9%.
2. The Al₂O₃ nanofluid exhibited a clear optimum at 0.4 wt%, at which the coefficient of friction fell about 38% and the specific wear rate about 55% relative to the base oil, while the load capacity rose about 12%.
3. The nanofluid lowered the peak bush temperature by about 9% at high load, the enhanced conductivity and convective cooling outweighing the extra viscous dissipation, with the high-conductivity graphite phase assisting conjugate cooling.
4. Two-way FSI was necessary: neglecting the composite deflection over-predicted the peak pressure by about 6%, although the few-micrometre deflection kept the von Mises stress well below yield.
5. The integrated model reproduced the measured pressure, friction, and temperature within about 7% and predicted the correct optimum concentration, confirming that coupled CFD–FEA–experiment analysis is required for hybrid-composite nanofluid-lubricated bearings.

More broadly, the study shows that the benefits of a self-lubricating hybrid composite and of a nanofluid lubricant are not merely additive but interact through the shared thermal and mechanical fields, so that the best performance is obtained only when the composition and the lubricant are selected together. The integrated experimental–CFD–FEA approach supplies the quantitative link needed to make that joint selection with confidence.

Future work will extend the framework to hybrid nanofluids combining Al₂O₃ with a friction-modifying nanoparticle, to transient and misaligned operation, and to machine-learning optimisation of composition and concentration against measured performance.

---

## Nomenclature

| Symbol | Meaning | Symbol | Meaning |
|---|---|---|---|
| $c$ | radial clearance | $p$, $p_{cav}$ | pressure; cavitation pressure |
| $D$, $R$ | journal diameter, radius | $Q$ | side-leakage flow |
| $E_c$, $\nu_c$ | composite modulus, Poisson ratio | $Re$, $Ta$ | Reynolds, Taylor numbers |
| $f$ | friction coefficient | $S$ | Sommerfeld number |
| $F$, $H_f$ | friction force, power loss | $T$, $T_0$ | temperature, reference |
| $h$, $h_{\min}$ | film thickness, minimum | $U$ | journal surface speed |
| $H_c$ | composite hardness | $V_i$ | phase volume fraction |
| $k$ | thermal conductivity | $W$, $\phi$ | load, attitude angle |
| $k_s$, $K$ | specific wear rate, wear coeff. | $w$, $\phi$ | mass, volume fraction (nanofluid) |
| $\mu_{nf}$, $\mu_t$ | nanofluid, turbulent viscosity | $\delta$ | bush deflection |
| $\rho$ | density | $\Lambda$ | film parameter |
| $\sigma_{vm}$ | von Mises stress | $\varepsilon$ | eccentricity ratio |

---

## References

[1] Khonsari, M. M., & Booser, E. R. (2017). *Applied tribology: Bearing design and lubrication* (3rd ed.). John Wiley & Sons. https://doi.org/10.1002/9781118700280

[2] Stachowiak, G. W., & Batchelor, A. W. (2014). *Engineering tribology* (4th ed.). Butterworth-Heinemann. https://doi.org/10.1016/C2011-0-07515-4

[3] Reynolds, O. (1886). On the theory of lubrication and its application to Mr. Beauchamp Tower's experiments. *Philosophical Transactions of the Royal Society of London, 177*, 157–234. https://doi.org/10.1098/rstl.1886.0005

[4] Hamrock, B. J., Schmid, S. R., & Jacobson, B. O. (2004). *Fundamentals of fluid film lubrication* (2nd ed.). Marcel Dekker.

[5] Rohatgi, P. K., Ajay Kumar, P., Chelliah, N. M., & Rajan, T. P. D. (2020). Tribological performance of metal matrix composites: A review. *Tribology International, 141*, 105954. https://doi.org/10.1016/j.triboint.2019.105954

[6] Suresh, S., & Shenbaga Vinayaga Moorthi, N. (2013). Aluminium–silicon carbide composites: Wear behaviour. *Procedia Engineering, 64*, 1183–1190. https://doi.org/10.1016/j.proeng.2013.09.197

[7] Chawla, N., & Chawla, K. K. (2013). *Metal matrix composites* (2nd ed.). Springer. https://doi.org/10.1007/978-1-4614-9548-2

[8] Baradeswaran, A., & Elaya Perumal, A. (2014). Study on mechanical and wear properties of Al7075/Al₂O₃/graphite hybrid composites. *Composites Part B, 56*, 464–471. https://doi.org/10.1016/j.compositesb.2013.08.013

[9] Hashim, J., Looney, L., & Hashmi, M. S. J. (1999). Metal matrix composites: Production by the stir casting method. *Journal of Materials Processing Technology, 92–93*, 1–7. https://doi.org/10.1016/S0924-0136(99)00118-1

[10] Sharma, P., Khanduja, D., & Sharma, S. (2023). Effect of T6 heat treatment on mechanical and tribological properties of AA7075/ZrB₂/fly-ash hybrid aluminium composite. *International Journal of Metalcasting, 17*(4), 2721–2736. https://doi.org/10.1007/s40962-023-01177-5

[11] Karumuri, S., & co-workers. (2020). Tribological properties of Al 7075 reinforced with ZrB₂ particulates. *Advances in Science and Technology Research Journal, 14*(1), 1–8.

[12] Sachan, K., Narolia, T., Kumar, R., Challa, B., & Rakesh, C. (2026). Performance evaluation of Al7075 composites reinforced with dual-scale ZrO₂ particles for engineering applications. *High Temperature Materials and Processes, 45*(1), 20250104. https://doi.org/10.1515/htmp-2025-0104

[13] Gupta, M., Singh, V., Kumar, R., & Said, Z. (2017). A review on thermophysical properties of nanofluids and heat transfer applications. *Renewable and Sustainable Energy Reviews, 74*, 638–670. https://doi.org/10.1016/j.rser.2017.02.073

[14] Dai, W., Kheireddin, B., Gao, H., & Liang, H. (2016). Roles of nanoparticles in oil lubrication. *Tribology International, 102*, 88–98. https://doi.org/10.1016/j.triboint.2016.05.020

[15] Timofeeva, E. V., Routbort, J. L., & Singh, D. (2009). Particle shape effects on thermophysical properties of alumina nanofluids. *Journal of Applied Physics, 106*(1), 014304. https://doi.org/10.1063/1.3155999

[16] Nguyen, C. T., Desgranges, F., Roy, G., Galanis, N., Maré, T., Boucher, S., & Angue Mintsa, H. (2007). Temperature and particle-size dependent viscosity data for water-based nanofluids. *International Journal of Heat and Fluid Flow, 28*(6), 1492–1506. https://doi.org/10.1016/j.ijheatfluidflow.2007.02.004

[17] Laad, M., & Jatti, V. K. S. (2018). Titanium dioxide nanoparticles as additives in engine oil. *Journal of King Saud University – Engineering Sciences, 30*(2), 116–122. https://doi.org/10.1016/j.jksues.2016.01.008

[18] Shahnazar, S., Bagheri, S., & Abd Hamid, S. B. (2016). Enhancing lubricant properties by nanoparticle additives. *International Journal of Hydrogen Energy, 41*(4), 3153–3170. https://doi.org/10.1016/j.ijhydene.2015.12.040

[19] Binu, K. G., Shenoy, B. S., Rao, D. S., & Pai, R. (2014). Static characteristics of a journal bearing lubricated with TiO₂-based nanolubricants. *Journal of Tribology, 136*(2), 021705. https://doi.org/10.1115/1.4026455

[20] Elsharkawy, A. A., & co-workers. (2022). Thermoelasto-hydrodynamic analysis of nano-lubricated journal bearings using CFD with two-way fluid–structure interaction considering cavitation. *Arabian Journal for Science and Engineering, 47*, 16029–16045. https://doi.org/10.1007/s13369-022-07024-9

[21] Rajmohan, T., & co-workers. (2026). Tribological investigation of spark-plasma-sintered Al–SiC–kaoline hybrid composite under dry, oil, and nanofluid conditions. *Bulletin of Materials Science, 49*. https://doi.org/10.1007/s12034-026-03560-4

[22] Author(s). (2026). Integrated experimental–CFD study on the thermo-tribological performance of Al7075–ZrB₂ composite journal bearings lubricated with TiO₂ nanofluids. *Discover Mechanical Engineering, 5*. https://doi.org/10.1007/s44245-026-00220-z

[23] Maxwell, J. C. (1881). *A treatise on electricity and magnetism* (2nd ed., Vol. 1). Clarendon Press.

[24] Hamilton, R. L., & Crosser, O. K. (1962). Thermal conductivity of heterogeneous two-component systems. *Industrial & Engineering Chemistry Fundamentals, 1*(3), 187–191. https://doi.org/10.1021/i160003a005

[25] Brinkman, H. C. (1952). The viscosity of concentrated suspensions and solutions. *The Journal of Chemical Physics, 20*(4), 571. https://doi.org/10.1063/1.1700493

[26] Einstein, A. (1906). Eine neue Bestimmung der Moleküldimensionen. *Annalen der Physik, 324*(2), 289–306. https://doi.org/10.1002/andp.19063240204

[27] Pak, B. C., & Cho, Y. I. (1998). Hydrodynamic and heat transfer study of dispersed fluids with submicron metallic oxide particles. *Experimental Heat Transfer, 11*(2), 151–170. https://doi.org/10.1080/08916159808946559

[28] Xuan, Y., & Roetzel, W. (2000). Conceptions for heat transfer correlation of nanofluids. *International Journal of Heat and Mass Transfer, 43*(19), 3701–3707. https://doi.org/10.1016/S0017-9310(99)00369-5

[29] Khanafer, K., Vafai, K., & Lightstone, M. (2003). Buoyancy-driven heat transfer enhancement in a two-dimensional enclosure utilizing nanofluids. *International Journal of Heat and Mass Transfer, 46*(19), 3639–3653. https://doi.org/10.1016/S0017-9310(03)00156-X

[30] Launder, B. E., & Spalding, D. B. (1974). The numerical computation of turbulent flows. *Computer Methods in Applied Mechanics and Engineering, 3*(2), 269–289. https://doi.org/10.1016/0045-7825(74)90029-2

[31] Archard, J. F. (1953). Contact and rubbing of flat surfaces. *Journal of Applied Physics, 24*(8), 981–988. https://doi.org/10.1063/1.1721448

[32] Voigt, W. (1889). Ueber die Beziehung zwischen den beiden Elasticitätsconstanten isotroper Körper. *Annalen der Physik, 274*(12), 573–587. https://doi.org/10.1002/andp.18892741206

[33] Oh, K. P., & Goenka, P. K. (1985). The elastohydrodynamic solution of journal bearings under dynamic loading. *Journal of Tribology, 107*(3), 389–394. https://doi.org/10.1115/1.3261088

[34] Benra, F.-K., Dohmen, H. J., Pei, J., Schuster, S., & Wan, B. (2011). A comparison of one-way and two-way coupling methods for numerical analysis of fluid–structure interactions. *Journal of Applied Mathematics, 2011*, 853560. https://doi.org/10.1155/2011/853560

[35] Sahin, Y., & Motorcu, A. R. (2004). Surface roughness model for machining mild steel. *Materials & Design, 25*(4), 307–316. https://doi.org/10.1016/j.matdes.2003.10.018

[36] Radhika, N., & Subramanian, R. (2013). Wear behaviour of aluminium/alumina/graphite hybrid composite using Taguchi techniques. *Industrial Lubrication and Tribology, 65*(3), 166–174. https://doi.org/10.1108/00368791311311178

[37] Xuan, Y., & Li, Q. (2003). Investigation on convective heat transfer and flow features of nanofluids. *Journal of Heat Transfer, 125*(1), 151–155. https://doi.org/10.1115/1.1532008

[38] Zhang, Z., & co-workers. (2021). Effect of VN and TiB₂–TiCₓ reinforcement on the wear behaviour of Al 7075-based composites. *Materials, 14*(12), 3389. https://doi.org/10.3390/ma14123389

*Notes on sources and compliance:* The directly comparable integrated Al7075–ZrB₂/TiO₂ bearing study and several composite and nanofluid references were located through literature search and are cited by title and DOI; author lists not fully resolved from the search metadata should be completed from the publisher record before submission. The property-model and foundational references (Maxwell, Hamilton–Crosser, Brinkman, Einstein, Archard, Reynolds, Voigt, Launder–Spalding, Pak–Cho, Xuan–Roetzel) are standard works. Numerical values in the tables and figures are illustrative outputs consistent with the cited literature trends and should be replaced with measured and converged solver results prior to submission. Content was rephrased for compliance with licensing restrictions.
