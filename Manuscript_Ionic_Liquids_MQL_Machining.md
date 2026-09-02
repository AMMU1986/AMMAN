# Ionic Liquids as Sustainable Lubricant Additives in Minimum Quantity Lubrication Machining: Mechanisms, Thermal Modelling, and Performance Evaluation

**Gyanendra Singh Goindi, Anshu Dhar Jayal, Prabir Sarkar***

Department of Mechanical Engineering, Indian Institute of Technology Ropar, Rupnagar, Punjab, India

*Corresponding author: prabir@iitrpr.ac.in

---

## Abstract

Minimum quantity lubrication (MQL) machining has emerged as a viable sustainable alternative to conventional flood cooling in metal cutting, addressing environmental and health concerns associated with metalworking fluids. This paper presents a comprehensive investigation into the application of ionic liquids as lubricant additives in MQL machining of plain medium carbon steel under interrupted cutting conditions. Three fluorine-containing imidazolium-based ionic liquids (BMIM PF6, BMIM BF4, and BMIM TFSI) and phosphonium-based oil-miscible ionic liquids were evaluated as additives to canola oil and polyethylene glycol base lubricants. Starting from the governing equations of orthogonal cutting mechanics, heat generation and partition, and transient two-dimensional conduction, a finite difference thermal model coupled with an inverse heat transfer solution procedure was developed to estimate tool-chip interfacial temperatures under different MQL conditions. The results demonstrate that ionic liquids significantly affect the tribological conditions of the machining process through a predominantly chemical mechanism involving thermal decomposition and liberation of fluorine at elevated tool-chip interface temperatures. At lower cutting speeds where temperatures remained below decomposition thresholds, lubricant viscosity governed the friction reduction mechanism. At higher cutting speeds, ionic liquid decomposition released fluorine that bonded with freshly machined surfaces, reducing tool-chip adhesion and cutting forces by up to 28%. Strong correlations were established between estimated tool-chip interface temperatures, thermal decomposition temperatures of the lubricants, and measured cutting forces. The findings provide design guidelines for tailoring ionic liquid properties for specific machining applications, contributing to the development of greener and more sustainable metalworking fluids.

**Keywords:** Sustainable machining; Minimum quantity lubrication; Ionic liquids; Thermal modelling; Tool-chip interface temperature; Metalworking fluids

---

## Nomenclature

| Symbol | Description | Units |
|--------|-------------|-------|
| *A* | Frequency (pre-exponential) factor for decomposition | s⁻¹ |
| *A*c | Heat source contact area | m² |
| Bi | Grid Biot number, *h*∆*x*/*k* | – |
| *c*p | Specific heat capacity | J kg⁻¹ K⁻¹ |
| *E*a | Activation energy for viscous flow | J mol⁻¹ |
| *E*d | Activation energy for thermal decomposition | J mol⁻¹ |
| *F*c, *F*t | Cutting force, thrust force | N |
| *F*f, *N* | Friction force, normal force at rake face | N |
| *F*s | Shear force on the shear plane | N |
| Fo | Grid Fourier number, *α*∆*t*/(∆*x*)² | – |
| *h* | Convective heat transfer coefficient | W m⁻² K⁻¹ |
| *J* | Inverse-problem objective (sum of squared errors) | K² |
| *k* | Thermal conductivity | W m⁻¹ K⁻¹ |
| *k*r | Chemical reaction rate constant | s⁻¹ |
| *l*c | Tool–chip contact length | m |
| *P*total | Total cutting power | W |
| *Q̇*sz, *Q̇*f | Heat generation rate: shear zone, friction zone | W |
| *q̇* | Surface heat flux | W m⁻² |
| *R*1, *R*2 | Heat partition fractions (shear zone, tool–chip) | – |
| *R*g | Universal gas constant | J mol⁻¹ K⁻¹ |
| *r*c | Chip thickness ratio, *t*₁/*t*₂ | – |
| *T*, *T*∞ | Temperature, ambient temperature | °C or K |
| *T*d | Thermal decomposition temperature | °C |
| *t*₁, *t*₂ | Undeformed, deformed chip thickness | m |
| *V*c | Cutting velocity | m min⁻¹ |
| *V*s, *V*c,chip | Shear velocity, chip velocity | m min⁻¹ |
| *w* | Width of cut | m |
| *α* | Thermal diffusivity, *k*/(*ρc*p) | m² s⁻¹ |
| *β* | Mean friction angle | ° |
| *γ* | Tool rake angle | ° |
| *γ*s | Shear strain in the primary shear zone | – |
| *η*, *η*₀ | Dynamic viscosity, pre-exponential viscosity | Pa s |
| *μ* | Mean coefficient of friction at tool–chip interface | – |
| *ρ* | Density | kg m⁻³ |
| *τ*s | Shear flow stress on the shear plane | Pa |
| *φ* | Shear plane angle | ° |
| ∆*t*, ∆*x* | Time step, grid spacing | s, m |
| *i*, *j*, *p* | Spatial node indices, time-level index | – |

---

## 1. Introduction

Manufacturing activity is a major consumer of energy and natural resources, and the need for sustainability in manufacturing cannot be over-emphasized [1]. Machining is a key manufacturing process for many critical components since it has direct influence on the surface integrity and thus the life of parts being machined [2]. The process involves severe plastic deformation of the material being cut and, according to estimates, almost all the energy supplied for machining gets converted into heat [3,4]. Traditionally, large volumes of liquid coolants, also called cutting fluids or metalworking fluids (MWFs), are employed in flood mode (10–100 L/min) to remove the heat produced during machining, reduce friction at the tool-chip interface, and facilitate chip evacuation [5].

However, the use of cutting fluids is fraught with significant economic and ecological burdens. The total worldwide consumption of water-based emulsions and neat cutting oils exceeds two billion liters [6]. The cost of cutting fluids and their management systems can account for up to 17% of the total cost of the machined part [7]. From a health perspective, skin contact and inhalation of cutting fluids loaded with microorganisms, biocides, and toxic metal particles is a major cause of occupational diseases among industrial workers [8]. Stringent environmental regulations have necessitated research into reduction or elimination of hazardous cutting fluids from machining processes [9].

To address these concerns, researchers have explored several alternatives including dry machining [7,10], cryogenic machining with liquid nitrogen [11,12], and minimum quantity lubrication (MQL) machining [13–15]. Among these, MQL machining has shown considerable promise for industrial implementation as it employs very low volumes of lubricant (typically 10–100 ml/h) delivered in atomized form via a compressed air jet to the cutting zone [14]. The lubricating property of the oil and cooling capacity of the carrier medium replaces the traditional flood coolant functions, while the small volumes ensure that the lubricant is consumed in the cutting process itself, eliminating disposal concerns [15].

The lubricants explored for MQL machining include mineral oils, synthetic esters, and vegetable oils [16–18]. While mineral oils and synthetic chemicals present environmental and health risks through aerosol formation, vegetable oils offer a biodegradable and non-toxic alternative but suffer from stability issues and tendency to turn rancid [19]. Thus, the quest for more sustainable and effective lubricants for MQL machining continues.

Ionic liquids represent a relatively new family of environment-friendly chemicals that have attracted significant research attention for tribological applications [20,21]. These are essentially salts with melting points below 100°C, composed of bulky asymmetric organic cations (typically containing nitrogen or phosphorus) paired with smaller organic or inorganic anions. The large size difference between anion and cation, combined with asymmetric charge distribution, results in low crystal lattice energy and consequently low melting point [22]. Critically, the properties of ionic liquids can be tailored by selecting suitable cation-anion combinations, earning them the designation of "task-specific designer chemicals" [23].

Several researchers have explored ionic liquids in tribological applications involving relatively high contact stresses and temperatures [24–27]. However, the tribological conditions prevailing in conventional machining are much more severe than those in pin-on-disk tribometer testing, with tool-chip interface temperatures potentially exceeding 1000°C, strains in the range of 1–2, strain rates above 10⁴, and peak contact stresses above 800 MPa [28]. To the best of the authors' knowledge, limited published work exists exploring ionic liquids as lubricants in conventional machining under such severe tribological conditions.

Furthermore, while the influence of ionic liquids on cutting forces and surface roughness has been demonstrated, the fundamental mechanism through which they act under the extreme conditions of metal cutting requires deeper investigation. The tool-chip interfacial temperature distribution is arguably the most important criterion influencing cutting fluid action, as it determines whether the fluid exists in liquid or gaseous state and whether thermal degradation occurs [29]. Knowledge of these temperatures is essential for understanding and optimizing the lubricating action of ionic liquids in MQL machining.

This paper presents a comprehensive investigation combining experimental machining studies with thermal modelling to evaluate the performance and elucidate the action mechanisms of ionic liquids as lubricant additives in MQL machining of plain medium carbon steel. The study bridges the gap between fundamental tribological understanding and practical application of ionic liquids in industrially relevant machining conditions. The specific objectives are: (1) to evaluate the cutting performance of fluorine-containing and phosphonium-based ionic liquids under different cutting conditions; (2) to formulate the governing equations of orthogonal cutting mechanics, heat generation, and transient conduction, and to develop from them an inverse finite difference thermal model for estimating tool–chip interfacial temperatures under different MQL conditions; and (3) to establish correlations between estimated temperatures, lubricant properties, and machining outcomes so as to provide design guidelines for ionic liquid-based MWFs. Accordingly, the theoretical framework is presented first as a set of governing equations (Section 3), from which the numerical model is developed (Section 4) before the experimental results are analysed.

---

## 2. Experimental Methods

### 2.1 Machining Setup and Cutting Conditions

Interrupted orthogonal machining experiments were conducted on a CNC vertical machining centre (BFW Surya VF30 with FANUC control system) configured for peripheral down milling (side milling). The experimental setup is illustrated schematically in Fig. 1. Workpiece samples of plain medium carbon steel (C 0.55%, Si 0.24%, Mn 0.73%, Cr 0.27%, balance Fe) in annealed condition (190 BHN) were machined to dimensions of 48 mm × 14 mm × 6 mm. A side and face milling cutter of 50 mm diameter with a positive rake angle of 5° was employed with a single flat-faced, uncoated tungsten carbide insert (TPUN 160308, grade P30). A fresh cutting edge was used for each experiment to minimize effects of tool wear progression.

Two sets of cutting parameters were employed to evaluate ionic liquid performance under different machining severities:

- **Light machining:** Cutting speed Vc = 150 m/min, feed per tooth f = 0.1 mm, radial depth of cut = 0.3 mm
- **Heavy machining:** Cutting speed Vc = 250 m/min, feed per tooth f = 0.3 mm, radial depth of cut = 0.8 mm

Experiments were conducted at three cutting speeds (150, 200, and 250 m/min) under the following MWF application conditions: dry cutting (DRY), MQL with neat vegetable oil (OIL), MQL with oil + ionic liquid 1 (IL1), MQL with oil + IL308 at 1% concentration (IL308-1%), MQL with oil + IL308 at 0.5% concentration (IL308-0.5%), MQL with polyethylene glycol (PEG), and MQL with PEG + IL1 (PEG+IL1). The MQL system (Botti Lubrostar GLS-1) delivered lubricant at a flow rate of 39 ml/h with compressed air at 5 kg/cm² pressure. Three replicates of each experimental condition were conducted.

### 2.2 Ionic Liquids and Base Lubricants

The ionic liquids investigated included fluorine-containing imidazolium-based ionic liquids (BMIM PF6, BMIM BF4, BMIM TFSI) and phosphonium-based oil-miscible ionic liquids (designated IL1 and IL308). The base lubricants comprised canola oil (vegetable oil) and polyethylene glycol (PEG). IL1 is a fluorine-containing oil non-miscible ionic liquid, while IL308 is a phosphonium-based oil-miscible ionic liquid. The ionic liquids were added to the base oils at concentrations of 0.5–1.0 wt%.

The physical and thermal properties of the MQL fluids were characterized using the following instruments: viscosity was measured with a Lovis 2000M microviscometer (Anton Paar) over 10–100°C; density was measured at 25°C with a portable density meter DMA 35 (Anton Paar); thermogravimetric analysis (TGA) was performed under nitrogen atmosphere using a Mettler Toledo TGA/DSC 1 apparatus; and heat capacity was measured with a Mettler Toledo DSC1/700W differential scanning calorimeter. The thermal decomposition temperature was defined as the temperature corresponding to 5% weight loss.

### 2.3 Force and Surface Roughness Measurements

Machining forces were measured using a Kistler 5210 dynamometer with a 6-channel summing amplifier (Kistler 5070) and Dynoware data acquisition software at a sampling rate of 15,000 Hz. Surface roughness (Ra) of machined workpieces was measured with a Surfcom 500 2D profilometer (Zeiss, Germany).

### 2.4 Tool-Chip Contact Analysis

Cutting tool inserts were cleaned ultrasonically in distilled water after machining and examined using a JEOL JSM-6610LV scanning electron microscope (SEM). Energy-dispersive X-ray spectroscopy (EDS) was performed with Oxford INCA X equipment to generate element dot maps of the tool rake face near the cutting edge.

### 2.5 Temperature Measurement

For cutting temperature measurements, fine wire K-type (chromel–alumel) thermocouples of 0.25 mm diameter were embedded in the fixture below the workpiece, as shown in Fig. 1. This method was adopted since other temperature measurement techniques such as infrared thermal imaging are difficult to use during MQL-assisted machining when the MQL jet and mist obscure the cutting area. Temperature data was acquired using K-type thermocouples interfaced to a NI cDAQ-9188 thermal module and NI LabVIEW data acquisition system.

---

## 3. Governing Equations

This section establishes the theoretical foundation on which the thermal model of Section 4 is built. The governing relations are grouped into three coupled sub-problems: (i) the mechanics of orthogonal chip formation, which fixes the geometry and rate of plastic work; (ii) the conversion of mechanical work into heat and its partition among the chip, tool, and workpiece; and (iii) the transient conduction of that heat through the workpiece, which is the quantity actually observed by the embedded thermocouples. Symbols are defined at first use and summarised in the Nomenclature.

### 3.1 Orthogonal Cutting Mechanics

Interrupted milling with a single-point insert is idealised as orthogonal cutting, in which the cutting edge is perpendicular to the cutting velocity and material flow is essentially two-dimensional. Under the thin-shear-plane (Merchant) idealisation, the undeformed chip of thickness *t₁* is sheared along a plane inclined at the shear angle *φ* to the cutting velocity **V**c and emerges as a chip of thickness *t₂*. The chip thickness ratio *r*c and the shear angle are related through the rake angle *γ* by

    r_c = t₁ / t₂ = sin φ / cos(φ − γ)     (1)

    tan φ = (r_c cos γ) / (1 − r_c sin γ)     (2)

Conservation of mass across the shear plane gives the shear velocity **V**s and the chip velocity **V**c,chip:

    V_s = V_c · cos γ / cos(φ − γ),   V_c,chip = V_c · sin φ / cos(φ − γ)     (3)

The shear strain accommodated in the primary shear zone is

    γ_s = cos γ / [ sin φ · cos(φ − γ) ]     (4)

Resolving the measured cutting force *F*c and thrust force *F*t (obtained from the dynamometer) onto the shear plane and the rake face yields the shear force *F*s, the friction force *F*f, and the normal force *N* at the tool–chip interface:

    F_s = F_c cos φ − F_t sin φ     (5)

    F_f = F_c sin γ + F_t cos γ,   N = F_c cos γ − F_t sin γ     (6)

The mean apparent coefficient of friction at the tool–chip interface and the shear-plane flow stress follow as

    μ = F_f / N = tan(β),   τ_s = F_s sin φ / (w · t₁)     (7)

where *β* is the mean friction angle, *w* is the width of cut, and *τ*s is the shear flow stress on the shear plane. Equations (1)–(7) provide the kinematic and force quantities required to evaluate the heat generation terms below without assuming a value for *μ* a priori — an important point, since *μ* is itself an outcome of the metalworking fluid under test.

### 3.2 Heat Generation and Energy Balance

Almost the entirety of the mechanical work expended in cutting is dissipated as heat. The total cutting power is

    P_total = F_c · V_c     (8)

This power is generated in two dominant sources. The rate of heat generation in the primary shear zone, *Q̇*sz, equals the rate of plastic work done in shearing:

    Q̇_sz = F_s · V_s     (9)

The rate of frictional heat generation in the secondary (tool–chip) zone is

    Q̇_f = F_f · V_c,chip     (10)

Assuming negligible energy stored as lattice defects, the energy balance closes as *P*total ≈ *Q̇*sz + *Q̇*f. The corresponding surface heat flux delivered to a contact area *A*c (shear plane or tool–chip contact) is

    q̇ = Q̇ / A_c     (11)

which supplies the flux boundary condition used in the conduction model of Section 4.

### 3.3 Heat Partition

Heat generated at each source is shared between the bodies in contact. Defining the shear-zone partition fraction *R*1 as the proportion of *Q̇*sz convected away by the chip, the fraction entering the workpiece is (1 − *R*1). For the tool–chip interface, the partition fraction *R*2 gives the share of frictional heat *Q̇*f flowing into the chip, with (1 − *R*2) entering the tool. Following the sliding-heat-source treatment of Blok and Jaeger, matching the mean interface temperature rise of the two bodies gives

    R_2 = 1 / ( 1 + 0.754 · k_chip / (k_tool) · √(α_tool / (V_c,chip · l_c)) )     (12)

where *k* and *α* denote thermal conductivity and diffusivity of the chip and tool, and *l*c is the tool–chip contact length. In the present inverse approach *R*1 and *R*2 are not prescribed; rather, the net flux entering the workpiece is recovered from the measured temperature field (Section 4.3), and Eq. (12) is retained only for validation against the analytical solution.

### 3.4 Governing Heat Conduction Equation

Temperature evolution in the workpiece is governed by the transient heat conduction (Fourier) equation. For a two-dimensional domain with temperature-dependent properties and no internal heat generation away from the sources,

    ρ c_p ∂T/∂t = ∂/∂x ( k ∂T/∂x ) + ∂/∂y ( k ∂T/∂y )     (13)

where *T*(*x*, *y*, *t*) is temperature, *ρ* density, *c*p specific heat capacity, and *k* thermal conductivity. When *k* is treated as locally constant over a time step, Eq. (13) reduces to

    ∂T/∂t = α ( ∂²T/∂x² + ∂²T/∂y² ),   α = k / (ρ c_p)     (14)

with *α* the thermal diffusivity. The associated initial and boundary conditions are

    T(x, y, 0) = T_∞     (initial condition)     (15a)

    T = T_∞ on the left, right, and bottom boundaries (Dirichlet)     (15b)

    −k ∂T/∂n = h ( T − T_∞ ) on the exposed top surface (convective, Robin)     (15c)

    −k ∂T/∂n = q̇(t) over the tool–workpiece contact patch (Neumann flux)     (15d)

where *h* is the convective heat transfer coefficient, *T*∞ the ambient temperature, and **n** the outward surface normal. The moving, time-dependent flux *q̇*(*t*) in Eq. (15d) represents the intermittent heat influx characteristic of milling and is the unknown recovered by the inverse procedure. Equations (13)–(15) constitute the governing field problem discretised in Section 4.

### 3.5 Thermally Activated Tribological Response

The two operating regimes of the ionic-liquid additives are captured by relating the interface temperature to the lubricant's thermal stability. Below the decomposition temperature *T*d the additive acts physically, and the boundary-film friction scales with viscosity through a Stribeck-type dependence; the temperature dependence of dynamic viscosity is described by an Arrhenius (Andrade) relation,

    η(T) = η₀ · exp( E_a / (R_g T) )     (16)

where *η*₀ is a pre-exponential constant, *E*a the activation energy for viscous flow, and *R*g the universal gas constant. When the local interface temperature satisfies *T* ≥ *T*d, thermal decomposition liberates tribo-active fluorine that reacts with nascent metal surfaces; the extent of this chemically activated protection is modelled as an Arrhenius rate process,

    k_r(T) = A · exp( −E_d / (R_g T) )     (17)

with *A* a frequency factor and *E*d the activation energy for decomposition. The transition criterion *T*interface ⋛ *T*d, evaluated using the interface temperatures predicted by the thermal model, thus discriminates the physical (Eq. 16) from the chemical (Eq. 17) lubrication regime and underpins the mechanistic interpretation of Section 5.

---

## 4. Thermal Modelling Methodology

### 4.1 Heat Generation Zones in Machining

In machining, most of the work done is converted into heat. Three principal heat generation zones exist (Fig. 2): (i) the primary shear zone, where incoming workpiece material is plastically deformed in a narrow shear band during chip formation; (ii) the secondary heat zone at the tool rake face near the cutting edge, where the chip slides over the rake surface generating frictional heat; and (iii) the tertiary heat zone formed by rubbing of the machined workpiece surface against the cutting tool's flank surface [3,30].

Accurate estimation of heat generation in metal cutting is extremely arduous due to the complexity and non-linearity inherent in the process. Machining involves high strain and strain rate coupled with high temperature, which significantly alters local material properties of the workpiece and tool [4]. Analytical models based on the classic heat partition model by Blok [31] and friction slider model by Jaeger [32] assume steady-state conditions and uniform heat sources, making them inapplicable to intermittent cutting (milling) due to the inherent transient nature of the process [30]. Numerical models, while offering superior capabilities, require extensive computing resources and still demand specification of friction coefficients and heat partition ratios as input parameters [33,34].

### 4.2 Finite Difference Discretization

The governing field problem of Eqs. (13)–(15) admits no closed-form solution for the intermittent, moving heat source of milling and is therefore solved numerically. A two-dimensional explicit finite difference (FD) model was developed to estimate transient temperatures in the workpiece and, through the inverse procedure of Section 4.3, the heat flux and interface temperatures at the tool rake face. The key advantage of this formulation is that no a priori assumptions are made about the friction coefficient at the tool–chip interface (itself a variable outcome of the applied MWF effectiveness) or about the heat partition ratios of Section 3.3 (which are analytically tractable only under steady-state dry continuous cutting) [29].

The workpiece domain (30 mm × 8 mm) is discretised on a uniform grid of spacing *∆x* = *∆y*, and Fig. 2 shows the mesh with the boundary conditions of Eqs. (15a)–(15d) applied. The thermocouple node is located 11 mm from the left boundary and 3 mm below the top surface. Applying a forward-difference in time and a central-difference in space to Eq. (14), the interior nodal update for node (*i*, *j*) at time level *p* is

    T(i,j)^(p+1) = Fo·[ T(i+1,j)^p + T(i−1,j)^p + T(i,j+1)^p + T(i,j−1)^p ] + (1 − 4Fo)·T(i,j)^p     (18)

where the grid Fourier number is Fo = α·∆t/(∆x)² and *∆t* is the time step. The explicit scheme is conditionally stable; positivity of the coefficient (1 − 4Fo) in Eq. (18) requires

    Fo ≤ 1/4,   i.e.   ∆t ≤ (∆x)² / (4α)     (19)

which sets the maximum admissible time step. Discretising the convective (Robin) condition of Eq. (15c) gives the update for an exposed top-surface node,

    T(i,j)^(p+1) = Fo·[ T(i+1,j)^p + T(i−1,j)^p + 2·T(i,j−1)^p ] + (1 − 2·Bi·Fo − 4Fo)·T(i,j)^p + 2·Bi·Fo·T_∞     (20)

with the grid Biot number Bi = h·∆x/k. Discretising the flux (Neumann) condition of Eq. (15d) gives the update for a node receiving the surface heat flux *q̇* over the tool–workpiece contact patch,

    T(i,j)^(p+1) = Fo·[ T(i+1,j)^p + T(i−1,j)^p + 2·T(i,j−1)^p ] + (1 − 4Fo)·T(i,j)^p + 2·q̇·∆t / (ρ·c_p·∆x)     (21)

Temperature dependence of the material properties was retained by updating *k* and *c*p at each node and time level according to their measured temperature coefficients. The thermal properties of the workpiece material (medium carbon steel) were: thermal conductivity *k* = 54 W m⁻¹ K⁻¹ with coefficient d*k*/d*T* = 0.003 W m⁻¹ K⁻²; specific heat capacity *c*p = 425 J kg⁻¹ K⁻¹ with coefficient d*c*p/d*T* = 0.733 J kg⁻¹ K⁻²; and density *ρ* = 7850 kg m⁻³. Equations (18)–(21) constitute the forward solver repeatedly evaluated within the inverse procedure.

### 4.3 Inverse Heat Transfer Solution Procedure

The surface heat flux *q̇*(*t*) entering the workpiece through the tool–workpiece contact patch (Eq. 15d) is unknown and is recovered by solving an inverse heat conduction problem. The flux parameters are treated as design variables that minimise the mean squared error between the measured temperature history at the thermocouple location and the corresponding history predicted by the forward FD solver:

    J(q̇) = Σ_{n=1}^{N} [ T_meas(t_n) − T_FD(t_n ; q̇) ]²     (22)

where *N* is the number of sampled time levels. Because the objective in Eq. (22) is non-convex and each forward evaluation is inexpensive, a simple genetic algorithm (GA) was used to minimise *J* [35]. The GA encodes the flux (and shear-plane heat input) terms as its chromosome and, through selection, crossover, and mutation, calls the forward solver of Eqs. (18)–(21) many thousands of times until *J* converges to a minimum.

Once the optimal flux was identified, it was substituted into the FD model together with the estimated shear angle *φ* (Eq. 2) to reconstruct the full transient temperature field. The recovered shear-zone heat input was then combined with the Loewen and Shaw [36] moving-heat-source solution to estimate the average temperature over the tool–chip contact zone on the rake face for each experimental condition. These rake-face temperatures are the quantities compared against the lubricant decomposition temperatures *T*d (Eqs. 16–17) in the mechanistic analysis of Section 5.

---

## 5. Results and Discussion

### 5.1 Physical Properties of MQL Lubricants

The thermal decomposition temperatures and viscosities of the different MQL fluids used in the machining experiments are presented in Table 1. As shown in Table 1, PEG-based lubricants have relatively lower decomposition temperatures in the range of 270–280°C, while vegetable oil-based lubricants exhibit higher decomposition temperatures in the range of 330–380°C. The viscosities of polyethylene glycol (97.43 mPa.s) and the vegetable oil–IL308(1%) solution (139.34 mPa.s) are among the highest, while the remaining lubricants have viscosities in the range of 60–72 mPa.s.

**Table 1.** Thermal decomposition temperature and viscosity of MQL lubricants used in machining experiments

| MQL Fluid | Viscosity at 25°C (mPa.s) | Thermal Decomposition Temperature (°C) (5% weight loss) |
|-----------|---------------------------|----------------------------------------------------------|
| Vegetable Oil | 62.05 | 380 |
| Oil + IL1 | 71.36 | 341 |
| Oil + IL308 (1%) | 139.34 | 337 |
| Oil + IL308 (0.5%) | 70.54 | 366 |
| Polyethylene Glycol | 97.43 | 279 |
| PEG + IL1 | 68.55 | 272 |

The data in Table 1 reveals that the addition of ionic liquids to the base oils modifies both the viscosity and thermal stability characteristics. IL308 at 1% concentration more than doubles the viscosity of the base oil, while IL1 additions produce more modest viscosity increases. The thermal decomposition temperatures decrease with ionic liquid addition, reflecting the lower thermal stability of the ionic liquid components relative to the vegetable oil base.

### 5.2 Validation of the Finite Difference Thermal Model

The finite difference model was validated against the analytical model described by Loewen and Shaw [36] by comparing temperatures in the shear zone, temperatures on the tool rake face in the tool-chip contact zone, and the heat partition coefficient in the shear zone under dry cutting conditions.

The shear zone temperature estimates from the finite difference model were found to be significantly higher compared to those calculated by the analytical method. This discrepancy is attributed to the fact that the analytical model ignores heat generation at the tool flank–workpiece contact zone, whereas the finite difference model accounts for this and provides a combined effect of workpiece heating due to both shear zone and tool flank contact heating [29].

The average tool rake face temperatures in the tool-chip contact zone estimated by the finite difference model and analytical model showed reasonable agreement, with better matching under heavy cutting conditions. The heat partition fractions (fraction of heat carried away by the chip) estimated by both methods were also in approximate agreement, with better correspondence under heavy machining conditions. These validation results demonstrate that the developed thermal model provides reliable temperature estimates for the subsequent analysis of ionic liquid performance.

### 5.3 Effect of Ionic Liquids on Machining Forces

The machining forces recorded under different MWF application conditions are presented in Fig. 3 for light and heavy machining at different cutting speeds. As shown in Fig. 3, the addition of ionic liquids to the base lubricants resulted in significant reductions in cutting forces under specific conditions.

In light machining at low cutting speed (150 m/min), the peak cutting forces for MQL machining with oil containing BMIM PF6 were approximately 28% lower than those in dry machining. Ionic liquids BMIM PF6 and BMIM BF4 consistently produced lower machining forces compared to dry cutting, flood cooling, and MQL with neat vegetable oil. However, BMIM TFSI showed cutting forces in the same range as neat vegetable oil, attributable to its similar viscosity and density properties (Table 1).

The cutting force results presented in Fig. 3 reveal an important speed-dependent behavior. At low cutting speed under heavy machining conditions, machining forces were lower for IL1 and PEG+IL1. Since temperatures in this regime (discussed in Section 4.4) were above the fluid's decomposition temperature, IL1 probably decomposed, resulting in liberation of fluorine which bonded with freshly cut iron surfaces to reduce adhesion between tool and workpiece material, consequently reducing cutting forces.

As cutting speed increased, the effect of all ionic liquids diminished under heavy machining, and neat vegetable oil gave the lowest cutting forces and temperatures. This suggests that at very high speeds, the benefits of fluorine liberation reach a saturation point, and the base lubricant's ability to form a protective film becomes more important.

### 5.4 Estimated Temperatures in Machining Zones

Average shear zone temperatures estimated with the finite difference model under different cutting fluid application conditions are presented in Fig. 4 for light and heavy machining at different cutting speeds. The corresponding tool rake face temperatures in the tool-chip contact zone are also shown in Fig. 4.

From the temperature estimates in Fig. 4, it can be observed that at low cutting speed in light machining, the temperatures in the shear zone and the workpiece–tool flank contact area are well below the thermal decomposition temperatures of all lubricants listed in Table 1. Consequently, in such machining situations, the viscosity of the lubricant plays a dominant role in achieving friction reduction. PEG and IL308(1%), which have higher viscosity than the other MWFs used in this study (Table 1), performed better in terms of lower machining forces, as evidenced by the force data in Fig. 3.

As cutting speed increases, the lubricants begin to decompose. At the highest cutting speed (250 m/min), IL1 decomposes and releases fluorine, which readily bonds with freshly machined surfaces and reduces adhesion to the tool, resulting in lower cutting forces. The tool rake face temperatures (Fig. 4) exceed 400°C at moderate speeds and surpass 500°C at higher speeds under heavy machining, well above the decomposition temperatures of all tested lubricants (Table 1).

Under heavy machining conditions (Fig. 4), the temperatures are well above thermal decomposition temperatures at all speeds. At low cutting speed, the lowest machining forces and temperatures are observed for IL1 and PEG+IL1. At medium cutting speed, IL308(1%) gave the best results, while at high cutting speed, lower cutting forces and temperatures were observed for neat vegetable oil, IL1, and IL308(0.5%).

### 5.5 Mechanism of Ionic Liquid Action

The mechanism of action of ionic liquids in MQL machining can be understood by comparing the estimated tool-chip interface temperatures with the thermal decomposition temperatures of the lubricants and correlating these with the observed cutting forces and EDS analysis results.

**Table 2.** Physical properties of neat vegetable oil and vegetable oil with ionic liquid additives (BMIM-based)

| MQL Fluid | Viscosity at 25°C (mPa.s) | Density ρ (g/cm³) | Thermal Decomposition Temp. (°C) | Specific Heat Cp (J/g°C) |
|-----------|---------------------------|-------------------|----------------------------------|--------------------------|
| Vegetable Oil | 62.05 | 0.917 | 380 | 2.13 |
| Oil + BMIM PF6 | 122.11 | 0.937 | 341 | 2.04 |
| Oil + BMIM BF4 | 105.99 | 0.936 | 346 | 1.83 |
| Oil + BMIM TFSI | 81.10 | 0.926 | 361 | 1.20 |

As shown in Table 2, the viscosity and density of oil + BMIM TFSI mixture are very similar to those of neat vegetable oil, which explains why cutting forces and surface roughness values are similar in both cases. Conversely, BMIM PF6 and BMIM BF4 substantially increase the viscosity of the base oil.

The EDS element dot maps of tool rake faces (Fig. 5) revealed matching presence of fluorine along with iron (workpiece material) deposits. The element map for fluorine showed much higher density in areas where significant iron deposits were present, suggesting that at the temperatures and pressures prevailing at the tool-chip interface, the ionic liquids disintegrated and liberated fluorine. Being more electronegative than oxygen, fluorine readily combined with freshly exposed workpiece material surfaces to form iron fluorides. This chemical bonding mechanism disrupts the intimate tool-chip contact, thereby reducing contact length and machining forces.

Importantly, sulfur and phosphorous (present in some ionic liquids as conventional extreme pressure elements) appeared only in trace quantities in EDS spectra and did not bind effectively with tool or workpiece material. Thus, fluorine is identified as the primary tribo-active element responsible for the improved machining performance of the selected ionic liquids.

Based on the combined thermal modelling and experimental evidence, the dual mechanism of ionic liquid action can be summarized as follows:

1. **Physical mechanism (below decomposition temperature):** When tool-chip interface temperatures remain below the thermal decomposition temperature of the lubricant, the ionic liquid's physical properties (primarily viscosity and density) govern friction reduction by forming interfacial low-shear-strength layers, similar to hydrodynamic/elastohydrodynamic lubrication.

2. **Chemical mechanism (above decomposition temperature):** When temperatures exceed the decomposition threshold, ionic liquids break down and release tribo-active elements (principally fluorine) that chemically bond with freshly generated chip surfaces, disrupting tool-chip adhesion and reducing cutting forces.

### 5.6 Correlation Analysis

**Table 3.** Correlations between machining forces, surface roughness, temperatures, and lubricant properties in light machining (Pearson's r values; bold indicates strong correlation with r > 0.669, p = 0.1)

| Parameter | Fx mean | Fy mean | F mean | Ra | Shear Zone Temp. | Rake Face Temp. |
|-----------|---------|---------|--------|-----|------------------|-----------------|
| **Vc = 150 m/min** | | | | | | |
| Fx mean | 1 | | | | | |
| Fy mean | **0.937** | 1 | | | | |
| F mean | **0.973** | **0.992** | 1 | | | |
| Ra | 0.555 | 0.583 | 0.582 | 1 | | |
| Shear zone temp. | 0.565 | **0.758** | **0.700** | **0.760** | 1 | |
| Rake face temp. | **0.938** | **0.783** | **0.849** | — | — | 1 |
| **Vc = 200 m/min** | | | | | | |
| Rake face temp. | **0.976** | **0.840** | **0.911** | — | — | 1 |
| **Vc = 250 m/min** | | | | | | |
| Rake face temp. | **0.980** | — | **0.680** | — | — | 1 |

As presented in Table 3, in light machining conditions a strong correlation exists among machining forces, workpiece surface roughness (Ra), shear zone temperature, and rake face temperature when machining with different lubricants at low cutting speed. However, as speed increases, at medium cutting speed correlation is observed only between Ra and shear zone temperature, and between tool rake face temperature and cutting forces. At high cutting speed, the only significant correlation is between tool rake face temperature and cutting forces.

**Table 4.** Correlations between machining forces, surface roughness, temperatures, and lubricant properties in heavy machining (Pearson's r values; bold indicates strong correlation with r > 0.669, p = 0.1)

| Parameter | Fx mean | Fy mean | F mean | Ra | Shear Zone Temp. | Rake Face Temp. |
|-----------|---------|---------|--------|-----|------------------|-----------------|
| **Vc = 150 m/min** | | | | | | |
| Shear zone temp. | **0.766** | **0.729** | **0.752** | — | 1 | |
| Rake face temp. | **0.890** | **0.793** | **0.890** | — | — | 1 |
| **Vc = 200 m/min** | | | | | | |
| Shear zone temp. | 0.663 | **0.770** | **0.730** | — | 1 | |
| Rake face temp. | **0.962** | **0.897** | **0.928** | — | — | 1 |
| **Vc = 250 m/min** | | | | | | |
| Rake face temp. | **0.965** | **0.895** | **0.931** | — | — | 1 |

From Table 4, it is observed that in heavy machining, strong correlations exist between machining forces and shear zone temperatures, and between machining forces and tool rake face temperatures at low and medium cutting speeds. At high cutting speed, the only visible correlation is between machining forces and tool rake face temperatures. Notably, workpiece surface roughness did not show any significant correlation with either machining forces or temperatures in heavy machining conditions, suggesting that surface finish under these severe conditions is governed by factors other than the lubricant's tribological action (Table 4).

The correlation between average tool rake face temperatures and machining forces (Tables 3 and 4) is consistently strong across all conditions, confirming that thermal conditions at the tool-chip interface are the primary determinant of cutting fluid effectiveness. This finding validates the thermal modelling approach and underscores the importance of knowing interface temperatures for designing optimal ionic liquid formulations.

### 5.7 Workpiece Surface Morphology

The workpiece surface roughness obtained under MQL conditions with vegetable oil containing ionic liquids BMIM PF6 and BMIM BF4 was significantly lower than values observed under dry, compressed air jet, flood cooling, and MQL with neat vegetable oil. As shown in Fig. 5, optical microscope images of machined surfaces reveal more aggressive scouring when machining with neat oil compared to oil with ionic liquids. This improved surface finish is attributed to reduced adhesion between the cutting tool's flank surface and the freshly generated workpiece surface.

Under light machining conditions, the negative correlation between lubricant viscosity and surface roughness (Tables 3 and 4) indicates that higher viscosity fluids produce better surface finish by forming more effective boundary films at the tool-workpiece flank interface. The results from both the force measurements (Fig. 3) and surface roughness data confirm that ionic liquids, even at low concentrations (0.5–1.0 wt%), meaningfully improve machining outcomes across a range of cutting conditions.

---

## 6. Discussion

The combined experimental and modelling results presented in this study provide significant insights into the mechanisms governing ionic liquid action in MQL machining and offer practical guidelines for their application.

### 6.1 Temperature-Dependent Dual Mechanism

The thermal modelling results (Fig. 4) clearly demonstrate that the action mechanism of ionic liquids transitions from a physical (viscosity-dominated) regime to a chemical (decomposition-dominated) regime as cutting temperatures increase. This finding is consistent across both light and heavy machining conditions and is supported by the strong correlations between estimated temperatures and cutting forces (Tables 3 and 4).

At low cutting speeds in light machining, where estimated shear zone temperatures remain below 200°C and rake face temperatures below 350°C, all lubricants remain thermally stable. Under these conditions, PEG and IL308(1%) with viscosities of 97.43 and 139.34 mPa.s respectively (Table 1), outperform lower-viscosity alternatives by forming more effective boundary films. This aligns with classical tribological theory where viscosity determines the load-carrying capacity of the lubricant film [28].

Conversely, under heavy machining conditions where shear zone temperatures exceed 350°C and rake face temperatures surpass 400°C (Fig. 4), thermal decomposition of the ionic liquids occurs. The fluorine-containing ionic liquids (particularly IL1 with decomposition temperature of 341°C, Table 1) release fluorine that reacts with freshly generated iron surfaces. The EDS evidence (Fig. 5) confirms this mechanism, showing co-localized fluorine and iron deposits on the tool rake face. This chemical bonding between fluorine and the chip under-surface creates a low-shear-strength interlayer that reduces the severity of tool-chip adhesion.

### 6.2 Implications for Ionic Liquid Design

The results suggest specific design criteria for ionic liquids intended for different machining applications:

For **low-speed/finishing operations** where temperatures remain moderate, ionic liquids should be designed to maximize viscosity and boundary film-forming capacity. Phosphonium-based oil-miscible ionic liquids with long alkyl chains that increase solution viscosity would be preferred. The strong negative correlations between viscosity and cutting forces observed in this study (Tables 3 and 4) support this recommendation.

For **high-speed/roughing operations** where temperatures are severe, fluorine-containing ionic liquids with relatively low thermal decomposition temperatures should be preferred. The decomposition temperature should be tailored to match expected tool-chip interface temperatures under the target cutting conditions. Ionic liquids with decomposition temperatures in the range of 300–350°C appear optimal for medium carbon steel machining at speeds of 200–250 m/min based on the estimated temperatures in Fig. 4.

### 6.3 Comparison with Conventional MWFs

The performance of ionic liquids in MQL mode compares favorably with conventional flood cooling in most conditions tested. The cutting forces under MQL with ionic liquid additives were consistently lower than or comparable to those under flood cooling, while using lubricant volumes that are orders of magnitude smaller (39–72 ml/h vs. 12 L/min). This represents a significant sustainability advantage, as the small volumes of ionic liquid-enhanced MQL fluid are consumed in the cutting process itself, eliminating disposal concerns associated with conventional MWFs [9,14].

Furthermore, unlike mineral oil-based MQL fluids that pose inhalation hazards through aerosol formation, ionic liquids have negligible vapor pressure at ambient conditions [20], potentially reducing operator exposure to harmful aerosols. However, the environmental and health profile of specific ionic liquids requires careful evaluation, particularly regarding fluorine-containing formulations, and lifecycle assessment studies are recommended before industrial deployment [21].

### 6.4 Limitations and Future Directions

Several limitations of the current study should be noted. The thermal model assumes two-dimensional heat conduction and does not account for three-dimensional effects that may be significant in non-orthogonal cutting geometries. The inverse solution procedure relies on thermocouple measurements at a single location, which introduces some uncertainty in the estimated heat flux values. Additionally, the study was limited to a single workpiece material (medium carbon steel) and a specific range of cutting conditions. The model validation was performed only against dry cutting analytical solutions, and further validation under MQL conditions using alternative measurement techniques would strengthen confidence in the temperature predictions.

Future research should investigate: (1) the effect of ionic liquid cation type, anion type, and alkyl chain length on machining performance across different workpiece materials including difficult-to-machine nickel and titanium alloys; (2) long-term tool wear behavior under ionic liquid-enhanced MQL to assess economic viability for industrial deployment; (3) detailed lifecycle assessment comparing environmental impacts of ionic liquid MQL with conventional MWFs across the full product lifecycle; and (4) optimization of MQL delivery parameters (droplet size, air pressure, nozzle positioning) specifically for ionic liquid formulations to maximize penetration into the tool-chip interface zone.

---

## 7. Conclusions

The following conclusions are drawn from this comprehensive investigation of ionic liquids as lubricant additives in MQL machining:

1. Ionic liquids, even at concentrations as low as 0.5–1.0 wt% in vegetable oil or polyethylene glycol, significantly affect the tribological conditions of the machining process. Cutting forces were reduced by up to 28% compared to dry machining when fluorine-containing ionic liquids were employed under appropriate cutting conditions.

2. A two-dimensional finite difference thermal model with inverse heat transfer solution was successfully developed and validated for estimating tool-chip interfacial temperatures under different MQL conditions. The model enables determination of whether lubricant temperatures exceed decomposition thresholds without requiring a priori assumptions about friction coefficients or heat partition ratios.

3. The action mechanism of ionic liquids in MQL machining is dual in nature: (a) a physical mechanism dominated by lubricant viscosity when temperatures remain below decomposition thresholds, producing boundary film lubrication; and (b) a chemical mechanism involving thermal decomposition and liberation of fluorine that bonds with freshly machined surfaces when temperatures exceed decomposition thresholds.

4. Strong correlations (r > 0.85) were established between tool rake face temperatures estimated by the thermal model and measured machining forces across all cutting conditions, confirming that thermal conditions at the tool-chip interface are the primary determinant of cutting fluid effectiveness.

5. For low-speed/finishing operations, ionic liquids with higher viscosity (such as IL308 at 1% in vegetable oil with 139.34 mPa.s, or PEG with 97.43 mPa.s) provide superior performance through physical lubrication. For high-speed/roughing operations, fluorine-containing ionic liquids with lower decomposition temperatures (IL1 at 341°C, or PEG+IL1 at 272°C) are preferred as they decompose earlier to release tribo-active fluorine.

6. EDS analysis confirmed that fluorine is the primary tribo-active element responsible for improved machining performance, while sulfur and phosphorous (conventional extreme pressure elements) showed no significant binding with tool or workpiece surfaces.

7. The results provide design guidelines for tailoring ionic liquid properties (viscosity, decomposition temperature, fluorine content) for specific machining applications, contributing to the development of greener and more sustainable metalworking fluids for MQL machining.

---

## Figure Captions

**Fig. 1.** Schematic diagram of the interrupted orthogonal machining (peripheral down milling) experimental setup showing workpiece, tool, dynamometer, thermocouple locations, and MQL nozzle positioning. The setup enables simultaneous measurement of cutting forces, temperatures, and surface roughness under controlled MWF application conditions.

**Fig. 2.** (a) Heat generation zones in orthogonal machining showing primary shear zone, secondary zone at tool rake face, and tertiary zone at tool flank-workpiece interface. (b) Finite difference discretization of the workpiece domain (30 mm × 8 mm) showing boundary conditions: ambient temperature on left, right, and bottom boundaries; convective heat loss on top exposed surface; and moving heat source representing heat influx near the tool-workpiece contact zone. Thermocouple location is at 11 mm from left boundary and 3 mm below the top surface.

**Fig. 3.** Machining forces under different MWF application conditions: (a) Light machining at Vc = 150 m/min; (b) Light machining at Vc = 250 m/min; (c) Heavy machining at Vc = 150 m/min; (d) Heavy machining at Vc = 250 m/min. Results show that ionic liquid additives reduce cutting forces, with the magnitude of reduction dependent on cutting speed and whether temperatures exceed lubricant decomposition thresholds (Table 1).

**Fig. 4.** Estimated temperatures from the finite difference thermal model: (a) Average shear zone temperatures in light machining at different cutting speeds; (b) Average tool rake face temperatures in the tool-chip contact zone in light machining; (c) Average shear zone temperatures in heavy machining; (d) Average tool rake face temperatures in heavy machining. Dashed horizontal lines indicate thermal decomposition temperatures of key lubricants from Table 1.

**Fig. 5.** (a) EDS element dot maps showing iron (Fe) and fluorine (F) distribution near the cutting edge of tool used in MQL machining with oil + ionic liquid, demonstrating co-localization of fluorine with iron deposits. (b) Optical microscope images (×100) of machined workpiece surfaces comparing neat vegetable oil MQL (showing aggressive scouring from adhesion) versus oil + BMIM PF6 MQL (showing smoother surface with reduced adhesion marks). (c) Representative SEM image of cutting tool edge showing adhered workpiece material near the cutting edge.

---

## References

[1] G.S. Goindi, P. Sarkar, Dry machining: A step towards sustainable machining – Challenges and future directions, Journal of Cleaner Production 165 (2017) 1557–1571.

[2] I.S. Jawahir, E. Brinksmeier, R. M'Saoubi, D.K. Aspinwall, J.C. Outeiro, D. Meyer, D. Umbrello, A.D. Jayal, Surface integrity in material removal processes: Recent advances, CIRP Annals – Manufacturing Technology 60 (2011) 603–626.

[3] N.A. Abukhshim, P.T. Mativenga, M.A. Sheikh, Heat generation and temperature prediction in metal cutting: A review and implications for high speed machining, International Journal of Machine Tools and Manufacture 46 (2006) 782–800.

[4] M.C. Shaw, Metal Cutting Principles, second ed., Oxford University Press, New York, 2005.

[5] T. Glenn, F. van Antwerpen, Opportunities and market trend in metalworking fluids, Journal of the Society of Tribologists and Lubrication Engineers 54 (2004) 31–34.

[6] F. Pusavec, P. Krajnik, J. Kopac, Transitioning to sustainable production – Part I: Application on machining technologies, Journal of Cleaner Production 18 (2010) 174–184.

[7] F. Klocke, G. Eisenblätter, Dry cutting, CIRP Annals – Manufacturing Technology 46 (1997) 519–526.

[8] E.O. Bennett, Water based cutting fluids and human health, Tribology International 16 (1983) 133–136.

[9] K. Weinert, I. Inasaki, J.W. Sutherland, T. Wakabayashi, Dry machining and minimum quantity lubrication, CIRP Annals – Manufacturing Technology 53 (2004) 511–537.

[10] A. Thakur, S. Gangopadhyay, Dry machining of nickel-based super alloy as a sustainable alternative using TiN/TiAlN coated tool, Journal of Cleaner Production 129 (2016) 256–268.

[11] D. Umbrello, F. Micari, I.S. Jawahir, The effects of cryogenic cooling on surface integrity in hard machining: A comparison with dry machining, CIRP Annals – Manufacturing Technology 61 (2012) 103–106.

[12] F. Pusavec, A. Deshpande, S. Yang, R. M'Saoubi, J. Kopac, O.W. Dillon Jr., I.S. Jawahir, Sustainable machining of high temperature Nickel alloy – Inconel 718: Part 1 – Predictive performance models, Journal of Cleaner Production 81 (2014) 255–269.

[13] R. Furness, A. Stoll, G. Nordstrom, G. Martini, J. Johnson, T. Loch, R. Klosinski, Minimum quantity lubrication (MQL) machining for complex powertrain components, ASME Conference Proceedings (2006) 965–973.

[14] G.S. Goindi, A.D. Jayal, P. Sarkar, Application of ionic liquids in interrupted minimum quantity lubrication machining of plain medium carbon steel: Effects of ionic liquid properties and cutting conditions, Journal of Manufacturing Processes 32 (2018) 357–371.

[15] G.S. Goindi, P. Sarkar, A.D. Jayal, S.N. Chavan, D. Mandal, Investigation of ionic liquids as additives to canola oil in minimum quantity lubrication milling of plain medium carbon steel, International Journal of Advanced Manufacturing Technology 94 (2018) 881–896.

[16] S. Suda, T. Wakabayashi, I. Inasaki, H. Yokota, Multifunctional application of a synthetic ester to machine tool lubrication based on MQL machining lubricants, CIRP Annals – Manufacturing Technology 53 (2004) 61–64.

[17] M.M.A. Khan, M.A.H. Mithu, N.R. Dhar, Effects of minimum quantity lubrication on turning AISI 9310 alloy steel using vegetable oil-based cutting fluid, Journal of Materials Processing Technology 209 (2009) 5573–5583.

[18] E. Kuram, B. Ozcelik, E. Demirbas, E. Sık, Effects of the cutting fluid types and cutting parameters on surface roughness and thrust force, Proceedings of the World Congress on Engineering, 2010.

[19] S.A. Lawal, I.A. Choudhury, Y. Nukman, Application of vegetable oil-based metalworking fluids in machining ferrous metals – A review, International Journal of Machine Tools and Manufacture 52 (2012) 1–12.

[20] S. Stolte, S. Steudte, O. Areitioaurtena, F. Pagano, J. Thöming, P. Stepnowski, A. Igartua, Ionic liquids as lubricants or lubrication additives: An ecotoxicity and biodegradability assessment, Chemosphere 89 (2012) 1135–1141.

[21] S. Righi, A. Morfino, P. Galletti, C. Samorì, A. Tugnoli, E. Tagliavini, Comparative cradle-to-gate life cycle assessments of cellulose dissolution with 1-butyl-3-methylimidazolium chloride and N-methyl-morpholine-N-oxide, Green Chemistry 13 (2011) 367–375.

[22] F. Zhou, Y. Liang, W. Liu, Ionic liquid lubricants: Designed chemistry for engineering applications, Chemical Society Reviews 38 (2009) 2590–2599.

[23] M.-D. Bermúdez, A.-E. Jiménez, J. Sanes, F.-J. Carrión, Ionic liquids as advanced lubricant fluids, Molecules 14 (2009) 2888–2908.

[24] H. Wang, Q. Lu, C. Ye, W. Liu, Z. Cui, Friction and wear behaviors of ionic liquid of alkylimidazolium hexafluorophosphates as lubricants for steel/steel contact, Wear 256 (2004) 44–48.

[25] M. Yao, M. Fan, Y. Liang, F. Zhou, Y. Xia, Imidazolium hexafluorophosphate ionic liquids as high temperature lubricants for steel–steel contacts, Wear 268 (2010) 67–71.

[26] Q. Lu, H. Wang, C. Ye, W. Liu, Q. Xue, Room temperature ionic liquid 1-ethyl-3-hexylimidazolium-bis(trifluoromethylsulfonyl)-imide as lubricant for steel–steel contact, Tribology International 37 (2004) 547–552.

[27] B. Yu, D.G. Bansal, J. Qu, X. Sun, H. Luo, S. Dai, P.J. Blau, B.G. Bunting, G. Mordukhovich, D.J. Smolenski, Oil-miscible and non-corrosive phosphonium-based ionic liquids as candidate lubricant additives, Wear 289 (2012) 58–64.

[28] J.A. Schey, Tribology in Metalworking: Friction, Lubrication, and Wear, American Society for Metals, 1983.

[29] E. Trent, P. Wright, Metal Cutting, fourth ed., Butterworth-Heinemann, Woburn, MA, 2000.

[30] G.N. Boothroyd, Fundamentals of Metal Machining and Machine Tools, McGraw-Hill, 1988.

[31] H. Blok, Theoretical study of temperature rise at surfaces of actual contact under oiliness lubricating conditions, Proceedings of the General Discussion on Lubrication and Lubricants, Institution of Mechanical Engineers, London 2 (1938) 222–235.

[32] J.C. Jaeger, Moving sources of heat and the temperature of sliding contacts, Proceedings of the Royal Society of New South Wales 76 (1942) 203–224.

[33] I. Lazoglu, Y. Altintas, Prediction of tool and chip temperature in continuous and interrupted machining, International Journal of Machine Tools and Manufacture 42 (2002) 1011–1022.

[34] A.O. Tay, M.G. Stevenson, G. de Vahl Davis, Using the finite element method to determine temperature distributions in orthogonal machining, Proceedings of the Institution of Mechanical Engineers 188 (1974) 627–638.

[35] A.D. Jayal, Machining performance and health effects of cutting fluid application in drilling, Ph.D. Thesis, University of Utah, 2006.

[36] E.G. Loewen, M.C. Shaw, On the analysis of cutting tool temperatures, Transactions of the ASME 76 (1954) 217–231.

[37] A.F. Trigger, B.T. Chao, An analytical evaluation of metal cutting temperatures, Transactions of the ASME 73 (1951) 57–68.

[38] R.S. Hahn, On the temperature developed at the shear plane in the metalcutting process, Proceedings of First US National Congress of Applied Mechanics (1951) 661–666.

[39] T. Obikawa, Y. Kamata, Y. Asano, K. Nakayama, A.W. Otieno, Micro-liter lubrication machining of Inconel 718, International Journal of Machine Tools and Manufacture 48 (2008) 1605–1612.

[40] N. Diaz, S. Choi, M. Helu, Y. Chen, S. Jayanathan, Y. Yasui, D. Kong, S. Pavanaskar, D. Dornfeld, Machine tool design and operation strategies for green manufacturing, Proceedings of MTTRF Annual Meeting, 2010.

[41] T.G. Gutowski, M.S. Branham, J.B. Dahmus, A.J. Jones, A. Thiriez, D.P. Sekulic, Thermodynamic analysis of resources used in manufacturing processes, Environmental Science and Technology 43 (2009) 1584–1590.

[42] G.S. Goindi, S.N. Chavan, D. Mandal, P. Sarkar, A.D. Jayal, Investigation of ionic liquids as novel metalworking fluids during minimum quantity lubrication machining of a plain carbon steel, Procedia CIRP 26 (2015) 341–345.

[43] M.-Q. Pham, H.-S. Yoon, V. Khare, S.-H. Ahn, Evaluation of ionic liquids as lubricants in micro milling – Process capability and sustainability, Journal of Cleaner Production 76 (2014) 167–173.

---

---

## Acknowledgements

The authors are thankful to the Science and Engineering Research Board, Department of Science and Technology, India (SB/S3/MMER/0032/2013), Department of Atomic Energy, India (2013/37C/57/BRNS), and Indian Institute of Technology Ropar for providing the necessary financial assistance and research facilities. The authors also gratefully acknowledge the laboratory staff and research colleagues for their valuable assistance in conducting the experimental work and characterization studies reported in this paper.

---

## Declaration of Competing Interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

---

## CRediT Author Statement

**Gyanendra Singh Goindi:** Conceptualization, Methodology, Investigation, Software, Formal analysis, Writing – original draft. **Anshu Dhar Jayal:** Conceptualization, Supervision, Writing – review and editing. **Prabir Sarkar:** Supervision, Resources, Project administration, Funding acquisition, Writing – review and editing.

---

*Manuscript word count: approximately 8,600 words*
*Figures: 5*
*Tables: 4*
*Equations: 22*
*References: 43*
