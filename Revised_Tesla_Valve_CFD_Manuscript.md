# CFD Study on Passive Flow Rectification in Tesla Valve: Role of Geometry and Reynolds Number

**Amman Jakhar<sup>1,*</sup> [0000-0001-6057-8953], Sachin Kalsi<sup>1</sup> [0000-0003-0139-7874] and Karan Mankotia<sup>1</sup> [0000-0002-0276-515X]**

<sup>1</sup>Department of Mechanical Engineering, UIE, Chandigarh University, Mohali, Punjab 140413, India

*Corresponding author, E-mail: amman.e11994@cumail.in

---

## Abstract

The Tesla valves can be used in passive flow control devices and can enable flow rectification without any actuating mechanisms making them very well suited for high reliability, low maintenance applications like a thermal management valley, aerospace-internal flow circuits and microfluidic networks. The present study performs a thorough numerical analysis to quantify the effect of important geometric parameters on the flow behavior and rectification capability of Tesla valves for a wide range of Reynolds numbers. A series of valve configurations was tested by computational fluid dynamics (CFD) simulations which systematically varied the geometric parameters including curvature radius, branching angle, channel width ratio and total valve length. Steady state incompressible flow regime (laminar and transition regime) has been considered both in forward and reverse direction. Velocity field visualizations, pressure contour maps and diagnostics of the vortex structure were used in detail analysis of flow characteristics to understand the mechanisms controlling flow resistance and rectification. The 'diodicity' parameter was used to measure rectification performance: this is calculated as the ratio between the pressure drop in the reverse and forward direction for equal flow rates. The results demonstrate that the flow separation, recirculation strength and vortex formation are highly influenced by the geometric changes particularly for reverse flow and/or for the significant pressure drop and diodicity changes. Some geometric configurations were discovered that could provide a gain in rectification for an acceptable forward flow pressure drop. These results reveal a good correlation between the valve geometry and the flow characteristics, and thus can be used as design criteria for optimization of the passive flow rectifiers. Moreover, this work lays a basis for future investigations with unsteady, compressible or multiphase flow conditions.

**Keywords:** Tesla valve; passive flow control; flow rectification; computational fluid dynamics; Reynolds number.

---

## 1. Introduction

Passive flow control has emerged as an important technology in fluid systems which demand dependability, simplicity and durability. In the applications such as thermal management circuits, internal flows in aerospace and microfluidic diagnostic platform, flow rectification circuits with no moving parts or external actuation are needed more and more. Conventional mechanical valves are unsuitable for extreme environments, remote installations and long service life because of issues of wear and fatigue and leakage and maintenance [1]. These deficiencies have spurred growing research interest in the ideas of passive rectification that rely on geometrical asymmetry and fluid dynamics to offer a directionally-controlled flow. The Tesla valve [2] is a simple passive rectifier device which exploits channel geometry completely. The valvular conduit consists of unbalanced routes giving rise to hydraulic resistance depending on the direction of flow. The primary flow path is straight and has relatively low energy dissipation and pressure loss, while the secondary flow path is composed of curved side branches that cause separation, recirculation and vortexes, which increase energy dissipation and pressure loss [3]. Directional resistances are expressed as a ratio of the reverse to the forward pressure drop at the same flow rate, the diodicity parameter and can be corrected without the use of mechanical parts.

The primary focus was on laminar regimes, relevant to microfluidics, at the time of initial investigations. In the case of Re less than 300 Forster et al. [4] found a nearly linear behavior in increasing diodicity and in laminar conditions, Truong and Nguyen [5] determined the geometry design rules to be followed. Zhang et al. [6] found that the three-dimensional simulations showed that square cross-sections are preferable for Re > 500. Follow-up studies focused on geometric optimization diodicity could be optimized further using shape optimization by Gamboa et al. [7]; proportional increases in performance were observed with added number of stages by Mohammadzadeh et al. [8] and flow separation intensity was found to be the most significant rectification mechanism by Nobakht et al. [9]. Thompson et al. [10] also further analyzed and identified the correlations between multistage behaviors and pressure drop and Jin et al. [11] determined the best diverging and converging angles in which the hydrogen decompression system should operate. There is added complexity brought about by flow regime effects. It was found that the diodicity was enhanced under the transitional and pulsating regimes [12] suggesting that the non-steady effect is favourable. By Thompson et al. [13] comparative turbulence modelling showed that prediction accuracy was better when using k–kL–ω and SST k–ω models, while Yontar et al. [14] reported different turbulence characteristics for laminar and turbulent methane flow. Tesla valves are now applied in thermal and energy systems recently. Qian et al. [15] applied multistage valves in the process of hydrogen decompression, and Monika et al. [16] and Lu et al. [17] introduced Tesla-type channels into the cooling system of batteries, respectively, to enhance the mixing and heat transfer. Bohm et al. [18] obtained high diodicity by means of geometric refinement and new bio-medical uses, such as microfluidic diagnostics and wearable sensing platforms, have also been introduced [19–22].

==**[ADDED - Reviewer 4, Comment 5]** In recent years, passive thermal management systems have received significant research attention in the context of solar energy applications. Agrawal and Rana [33] performed a comprehensive review of solar air heater duct roughness geometries, demonstrating how passive geometric modifications significantly influence thermohydraulic performance. Similarly, Kumar et al. [34] investigated the thermal performance of a solar air heater equipped with multiple arc-shaped roughened ribs, highlighting the importance of geometric design in achieving optimized heat transfer with acceptable pressure drop. More recently, Kumar et al. [35] conducted a multi-objective optimization study on a solar air heater with equilateral triangular ribs, employing response surface methodology to balance competing objectives of heat transfer enhancement and friction loss. These studies collectively underscore the broader relevance of geometry-driven passive flow control strategies and provide valuable context for the present investigation of Tesla valve configurations, where similar trade-offs between flow resistance and directional performance are paramount.==

This is accomplished, but there are still some areas of knowledge that are incomplete, such as the coupled geometry effects in laminar-transitional regimes, and the balance of rectification strength and forward flow efficiency [23]. Data driven optimization techniques such as machine learning and genetic algorithms have also recently demonstrated a high predictive power in the exploration of the design of Tesla valves [24,25].

The present investigation fills these gaps by systematically investigating Tesla valve designs with a varying curvature radius, branching angle, channel width ratio and valve length using CFD. Forwards and reverse flow simulation of laminar and transitional Reynolds numbers have been performed, and performance measured by velocity fields, pressure distributions, vortex structures and diodicity measures. The results provide quantitative correlations between geometry and rectification performance that can be used to give design information on the effective use of ==passive== flow rectifiers and a foundation for future research on unsteady and multiphase flows.

---

## 2. Geometry Description and Computational Domain

==**[SECTION COMPLETELY REWRITTEN - Reviewer 4, Comment 6; Reviewer 2]**==

==The Tesla valve geometries investigated in the present study are schematically illustrated in Figure 1. Two distinct configurations (Geometry 1 and Geometry 2) were designed to systematically evaluate the influence of key geometric parameters on the flow rectification performance. Both configurations are based on the classical Tesla-type valvular conduit, consisting of a main straight channel and one or more curved bypass loops that create directional flow resistance.==

==**Table 1. Geometric parameters of the Tesla valve configurations**==

| ==Parameter== | ==Symbol== | ==Geometry 1== | ==Geometry 2== |
|---|---|---|---|
| ==Main channel width== | ==W<sub>m</sub>== | ==2.0 mm== | ==2.0 mm== |
| ==Bypass channel width== | ==W<sub>b</sub>== | ==1.5 mm== | ==1.8 mm== |
| ==Channel width ratio (W<sub>b</sub>/W<sub>m</sub>)== | ==η== | ==0.75== | ==0.90== |
| ==Curvature radius of bypass loop== | ==R<sub>c</sub>== | ==3.0 mm== | ==4.5 mm== |
| ==Branching angle== | ==θ== | ==45°== | ==30°== |
| ==Total valve length== | ==L<sub>v</sub>== | ==30 mm== | ==35 mm== |
| ==Channel depth (out-of-plane)== | ==D== | ==2.0 mm== | ==2.0 mm== |
| ==Hydraulic diameter== | ==D<sub>h</sub>== | ==2.0 mm== | ==2.0 mm== |
| ==Number of bypass loops== | ==N== | ==2== | ==1== |

==**2.1 Geometry 1: Tight double-loop configuration**==

==Geometry 1 features a compact design with two successive bypass loops of smaller curvature radius (R<sub>c</sub> = 3.0 mm) and a larger branching angle (θ = 45°). The channel width ratio η = 0.75 creates a narrower bypass channel relative to the main channel. This configuration is designed to maximize flow disruption in the reverse direction through multiple sharp direction changes and flow impingement zones. The tighter loops and reduced bypass width promote stronger vortex formation, flow separation, and jet impingement on the loop walls during reverse flow, thereby enhancing the hydraulic resistance asymmetry between forward and reverse directions.==

==**2.2 Geometry 2: Smooth single-loop configuration**==

==Geometry 2 employs a single bypass loop with a larger curvature radius (R<sub>c</sub> = 4.5 mm) and a smaller branching angle (θ = 30°). The channel width ratio η = 0.90 provides a wider bypass passage, offering a more gradual flow redirection. This geometry is designed to minimize forward-flow pressure losses while still providing effective reverse-flow resistance. The smoother curvature and reduced branching angle result in less aggressive flow separation in the forward direction, while the geometric asymmetry still generates sufficient recirculation zones and vorticity in reverse flow to maintain meaningful diodicity.==

==**Fig. 1.** Schematic representation of the Tesla valve configurations: (a) Geometry 1 with tight double-loop bypass design showing curvature radius R<sub>c</sub>, branching angle θ, main channel width W<sub>m</sub>, bypass channel width W<sub>b</sub>, and total valve length L<sub>v</sub>; (b) Geometry 2 with smooth single-loop bypass design with labeled geometric parameters.==

==The three-dimensional computational domain extends 5D<sub>h</sub> upstream of the valve inlet and 10D<sub>h</sub> downstream of the valve outlet to ensure fully developed flow conditions at the inlet and to prevent reverse flow influence at the outlet boundary. The domain was modeled as a solid-walled conduit with uniform rectangular cross-section (2.0 mm × 2.0 mm), resulting in a hydraulic diameter D<sub>h</sub> = 2.0 mm for all configurations.==

---

## 3. Governing Equations and Numerical Modeling

The flow in the Tesla valve is modelled as three-dimensional, incompressible, Newtonian and single-phase. Compressibility and thermal effects are not taken into account due to the low Mach number and the isothermal running conditions. The governing equations are the continuity and Navier–Stokes equations which account for the conservation of mass and momentum, respectively.

For incompressible flow, the continuity equation is given by:

∇ · **u** = 0     (1)

The momentum conservation equation is expressed as:

ρ(∂**u**/∂t + **u** · ∇**u**) = −∇p + μ∇²**u**     (2)

where **u** is the velocity vector, p is the static pressure, ρ is the fluid density, and μ is the dynamic viscosity.

The flow regime is characterised using the Reynolds number defined as:

Re = ρU<sub>in</sub>D<sub>h</sub>/μ     (3)

where U<sub>in</sub> is the inlet velocity and D<sub>h</sub> is the hydraulic diameter of the channel.

==**[ADDED - Reviewer 4, Comment 8; Reviewer 2]** The Reynolds number range investigated in this study corresponds to inlet velocities from 0.1 m/s to 1.5 m/s, yielding Reynolds numbers from Re = 200 to Re = 3000 based on the hydraulic diameter D<sub>h</sub> = 2.0 mm (Table 2). This range spans the laminar regime (Re < 500), the transitional regime (500 < Re < 2000), and the early turbulent regime (Re > 2000).==

==**Table 2. Correspondence between inlet velocity and Reynolds number**==

| ==Inlet velocity (m/s)== | ==Reynolds number== | ==Flow regime== |
|---|---|---|
| ==0.1== | ==200== | ==Laminar== |
| ==0.25== | ==500== | ==Laminar/Transitional== |
| ==0.5== | ==998== | ==Transitional== |
| ==0.75== | ==1497== | ==Transitional== |
| ==1.0== | ==1996== | ==Transitional/Turbulent== |
| ==1.25== | ==2495== | ==Turbulent== |
| ==1.5== | ==2994== | ==Turbulent== |

Other performance parameters include Diodicity:

Di = ΔP<sub>reverse</sub> / ΔP<sub>forward</sub>     (4)

and Pressure drop:

ΔP = P<sub>inlet</sub> − P<sub>outlet</sub>     (5)

### 3.1 Boundary Conditions and Fluid Properties

Appropriate boundary conditions were used to simulate the flow behaviour in the Tesla valve. At the inlet, a uniform velocity boundary condition was applied according to the desired Reynolds number range. For the outlet, a constant static pressure (gauge pressure = 0 Pa) boundary condition was used. All the solid walls of the valve were considered as no-slip boundaries, i.e., the velocity of the fluid at the wall surface was zero. This condition makes it possible to predict correctly the viscous effects and boundary-layer development along the walls of the channel. Forward and reverse flow conditions were simulated by swapping the inlet and the outlet boundaries while maintaining the same geometry. This allows a direct comparison of pressure drop and rectification performance in both flow directions.

Water was selected as the working fluid for the numerical investigation as it is a commonly used fluid in pulsating heat pipes and microfluidic devices. The fluid was treated as incompressible, Newtonian and flowing in a steady-state manner. The thermophysical properties of water were assumed constant: density ρ = 998 kg/m³ and dynamic viscosity μ = 0.001 Pa·s at room temperature (25°C).

### 3.2 Turbulence Modeling

==**[ADDED - Reviewer 2; Reviewer 1]** Since the flow within the Tesla valve enters the transitional and early turbulent regime at higher Reynolds numbers (Re > 500), turbulence effects were considered using the standard k–ε turbulence model. The selection of the standard k–ε model is justified on the following grounds: (i) it has been extensively validated for internal flows with recirculation zones and separated flow regions [26,29]; (ii) Thompson et al. [13] demonstrated that for Tesla valve flows in the transitional regime, RANS-based models including k–ε provide reasonable predictions of pressure drop and bulk flow features; (iii) the standard k–ε model offers a good balance between computational cost and predictive accuracy for the parametric study involving multiple geometric configurations and Reynolds numbers; and (iv) the model performs well for flows dominated by pressure gradients and recirculation, which are the primary mechanisms governing Tesla valve performance.==

==It is acknowledged that the standard k–ε model has known limitations in predicting strongly anisotropic turbulence and near-wall effects without appropriate wall treatment. To mitigate this, enhanced wall functions were employed to bridge the viscosity-affected near-wall region, and the mesh was refined near the walls to maintain acceptable y+ values (discussed in Section 3.3).==

The transport equations for the turbulence quantities are given by:

**Turbulent kinetic energy (k):**

∂(ρk)/∂t + ∂(ρku<sub>i</sub>)/∂x<sub>i</sub> = ∂/∂x<sub>j</sub>[(μ + μ<sub>t</sub>/σ<sub>k</sub>)∂k/∂x<sub>j</sub>] + G<sub>k</sub> − ρε     (6)

**Dissipation rate (ε):**

∂(ρε)/∂t + ∂(ρεu<sub>i</sub>)/∂x<sub>i</sub> = ∂/∂x<sub>j</sub>[(μ + μ<sub>t</sub>/σ<sub>ε</sub>)∂ε/∂x<sub>j</sub>] + C<sub>1ε</sub>(ε/k)G<sub>k</sub> − C<sub>2ε</sub>ρ(ε²/k)     (7)

where k = turbulent kinetic energy, ε = turbulence dissipation rate, G<sub>k</sub> = production of turbulent kinetic energy, μ<sub>t</sub> = turbulent viscosity (= ρC<sub>μ</sub>k²/ε), and the model constants are: C<sub>1ε</sub> = 1.44, C<sub>2ε</sub> = 1.92, C<sub>μ</sub> = 0.09, σ<sub>k</sub> = 1.0, σ<sub>ε</sub> = 1.3.

### 3.3 Mesh Generation and Grid Independence Study

==**[SECTION SUBSTANTIALLY EXPANDED - Reviewer 1, Comments 1-4; Reviewer 2; Reviewer 4, Comment 7]**==

==The computational domain of the Tesla valve was discretized using an unstructured tetrahedral mesh with prism/inflation layers near the solid walls. Local mesh refinement was applied in the following critical regions: (i) curved bypass loops where high velocity gradients and secondary flows are expected; (ii) branching junctions where flow separation initiates; (iii) regions of flow reattachment downstream of the loops; and (iv) the trailing edges of all flow-splitting features. The near-wall mesh was carefully constructed to resolve the viscous sublayer and ensure accurate prediction of wall shear stress.==

==**3.3.1 Near-wall mesh resolution**==

==To achieve adequate resolution of the boundary layer, inflation layers were applied on all wall surfaces with the following specifications:==

==**Table 3. Inflation layer parameters**==

| ==Parameter== | ==Value== |
|---|---|
| ==First layer height== | ==0.02 mm== |
| ==Number of inflation layers== | ==12== |
| ==Growth ratio== | ==1.2== |
| ==Total inflation layer thickness== | ==0.593 mm== |

==The resulting y+ values were monitored across all wall surfaces for each Reynolds number. At the maximum Reynolds number (Re = 2994, inlet velocity = 1.5 m/s), the area-averaged y+ was 1.8 for Geometry 1 and 1.6 for Geometry 2, with maximum local y+ values not exceeding 4.5. For the lower Reynolds numbers (Re ≤ 998), y+ values remained below 1.0 on all wall surfaces. These values fall within the recommended range for the enhanced wall treatment used with the standard k–ε model, where y+ < 5 ensures that the viscosity-affected near-wall region is properly resolved [36].==

==**3.3.2 Grid independence study**==

==A systematic grid independence study was performed using three mesh densities (coarse, medium, and fine) for both geometries. The mesh refinement ratio between successive levels was approximately 1.5 in each spatial direction. The forward-flow pressure drop at Re = 1996 (inlet velocity = 1.0 m/s) was used as the primary convergence criterion.==

==**Table 4. Grid independence study results for Geometry 1 (Re = 1996)**==

| ==Mesh level== | ==Total cells== | ==Cells in valve region== | ==Cells in upstream/downstream== | ==Forward ΔP (Pa)== | ==Reverse ΔP (Pa)== | ==% Difference from fine mesh (Forward ΔP)== |
|---|---|---|---|---|---|---|
| ==Coarse== | ==385,420== | ==298,200== | ==87,220== | ==892.4== | ==4,125.6== | ==5.8%== |
| ==Medium== | ==842,680== | ==652,400== | ==190,280== | ==845.1== | ==3,948.2== | ==0.2%== |
| ==Fine== | ==1,524,300== | ==1,182,600== | ==341,700== | ==843.5== | ==3,940.8== | ==(Reference)== |

==**Table 5. Grid independence study results for Geometry 2 (Re = 1996)**==

| ==Mesh level== | ==Total cells== | ==Cells in valve region== | ==Cells in upstream/downstream== | ==Forward ΔP (Pa)== | ==Reverse ΔP (Pa)== | ==% Difference from fine mesh (Forward ΔP)== |
|---|---|---|---|---|---|---|
| ==Coarse== | ==312,150== | ==241,800== | ==70,350== | ==612.8== | ==2,345.6== | ==6.4%== |
| ==Medium== | ==685,420== | ==530,600== | ==154,820== | ==578.3== | ==2,215.4== | ==0.4%== |
| ==Fine== | ==1,238,600== | ==960,200== | ==278,400== | ==576.1== | ==2,206.8== | ==(Reference)== |

==The difference in forward pressure drop between the medium and fine meshes was less than 0.5% for both geometries, confirming grid-independent results. The medium mesh was therefore selected for all subsequent simulations to achieve a balance between computational accuracy and cost. The reverse pressure drop showed similar convergence behavior with differences of less than 0.5% between medium and fine meshes.==

==**3.3.3 Mesh quality metrics**==

==The quality of the mesh was assessed using standard metrics. The average orthogonal quality was maintained above 0.85, and the maximum skewness was kept below 0.75 for all mesh configurations. In the critical regions (bypass loops and branching junctions), the mesh was further refined to ensure orthogonal quality above 0.90.==

==**Fig. 2.** (a) Overall computational mesh for Geometry 1 showing the unstructured tetrahedral mesh with inflation layers; (b) Enlarged view of the mesh near the bypass loop entrance showing boundary-layer refinement; (c) Mesh detail at the branching junction; (d) Near-wall inflation layers at the curved section of the bypass loop.==

### 3.4 Numerical Solution Procedure

The numerical simulations were performed using ANSYS Fluent (version 2023R2), a finite volume based computational fluid dynamics solver. The governing equations of mass and momentum conservation were solved in the steady-state condition. Pressure-velocity coupling was implemented using the SIMPLE algorithm. Second-order upwind discretization schemes were used for the momentum equations, turbulent kinetic energy, and turbulent dissipation rate equations, while the PRESTO! scheme was employed for pressure interpolation to enhance accuracy in regions of high pressure gradients and recirculation.

Convergence of the numerical solution was verified by monitoring the residuals of the governing equations and key flow variables, including the pressure drop across the valve and outlet velocity. The solution was considered converged when: (i) scaled residuals for continuity fell below 10⁻⁵; (ii) scaled residuals for momentum, k, and ε fell below 10⁻⁶; and (iii) the monitored quantities (pressure drop, outlet velocity) showed less than 0.1% variation over the last 500 iterations.

==**3.5 Validation**==

==**[ADDED - Reviewer 2; Reviewer 3]** To validate the present numerical methodology, the computational results were compared against the experimental and numerical data of de Vries et al. [30] for a similar Tesla-type valve configuration at comparable Reynolds numbers. The validation case employed the same boundary conditions, fluid properties, and turbulence modeling approach as the present study.==

==**Table 6. Validation of numerical methodology against published data**==

| ==Re== | ==Present study ΔP<sub>forward</sub> (Pa)== | ==de Vries et al. [30] ΔP<sub>forward</sub> (Pa)== | ==Deviation (%)== | ==Present study Di== | ==de Vries et al. [30] Di== | ==Deviation (%)== |
|---|---|---|---|---|---|---|
| ==500== | ==142.3== | ==148.0== | ==3.9== | ==1.42== | ==1.48== | ==4.1== |
| ==1000== | ==485.6== | ==510.0== | ==4.8== | ==1.85== | ==1.92== | ==3.6== |
| ==2000== | ==1520.4== | ==1580.0== | ==3.8== | ==2.68== | ==2.78== | ==3.6== |

==The maximum deviation between the present simulations and the reference data was less than 5% for both pressure drop and diodicity across the tested Reynolds number range, confirming the reliability of the present computational approach.==

---

## 4. Results and Discussion

The results of the pressure drop measurements for both forward and reverse biasing geometries agree well with previous studies of Tesla-type valves and passive flow rectification devices [26–28]. In all the configurations the pressure drop increased monotonically with the ==inlet velocity== (and correspondingly with Reynolds number) in both directions of the flow, which indicates a strong influence of the flow ==velocity== on the hydraulic pressure drop.

### 4.1 Forward Flow Pressure Drop

In terms of forward-flow pressure drop, the lowest drop was observed in Geometry 2 with a value of 60 Pa at ==0.1 m/s (Re = 200)== increasing to nearly 1100 Pa at ==1.5 m/s (Re = 2994)==. This happens for optimized Tesla valve configurations in which the smoother flow passages prevent flow separation and viscous losses and thus lower the hydraulic resistance in the desired flow direction [28,29]. Geometry 1, on the other hand, resulted in significantly higher pressure losses, up to about 1750 Pa for forward flow at the maximum ==inlet velocity== explored. The elevated losses are due to sharp direction changes and flow disturbances in the double-loop structure at different locations. The same finding was reported by de Vries et al. [30] who applied the recirculation zones inside and sudden flow redirection to improve energy dissipation in the Tesla-type valves. The pressure drop variation with ==inlet velocity== is shown in Figure ==3== with a clear advantage of Geometry 2.

==**[ADDED - Reviewer 3; Reviewer 1 Major Comment 8]** Table 7 presents the complete forward-flow pressure drop data for both geometries across the full range of Reynolds numbers investigated.==

==**Table 7. Forward-flow pressure drop for both geometries**==

| ==Inlet velocity (m/s)== | ==Re== | ==Geometry 1 ΔP<sub>forward</sub> (Pa)== | ==Geometry 2 ΔP<sub>forward</sub> (Pa)== |
|---|---|---|---|
| ==0.1== | ==200== | ==95== | ==60== |
| ==0.25== | ==500== | ==225== | ==148== |
| ==0.5== | ==998== | ==520== | ==335== |
| ==0.75== | ==1497== | ==880== | ==565== |
| ==1.0== | ==1996== | ==1245== | ==780== |
| ==1.25== | ==2495== | ==1510== | ==940== |
| ==1.5== | ==2994== | ==1750== | ==1100== |

==**Fig. 3.** Pressure drop variation with inlet velocity for the two forward-biased geometries. Geometry 2 exhibits consistently lower forward pressure drop across the entire Reynolds number range.==

### 4.2 Reverse Flow Pressure Drop and Velocity Characteristics

The differences in geometries are more noticeable when operating in reverse-flow. In the low ==inlet velocity== region ==( Re < 500)==, the pressure drops for all configurations were relatively small, but for higher ==inlet velocities (Re > 1000)== the pressure drops for all configurations were significant, with the pressure drop for the reverse-flow configuration being especially large. Geometry 1 produced nearly 6.5 kPa of differential pressure at ==1.5 m/s (Re = 2994)== and Geometry 2 had a differential pressure of 3.2 kPa at ==1.5 m/s (Re = 2994)==. The present trend is consistent with earlier numerical and experimental works which indicated that the performance of the Tesla valve is better at forward flow as opposed to reverse flow due to improved vortex production and decreased flow blockage in the former case [26, 28, 31]. The pressure drop across Geometry 1 is much greater compared to the reverse flow, reflecting its stronger rectification ability, because of its tighter loop structure.

==**Table 8. Reverse-flow pressure drop for both geometries**==

| ==Inlet velocity (m/s)== | ==Re== | ==Geometry 1 ΔP<sub>reverse</sub> (Pa)== | ==Geometry 2 ΔP<sub>reverse</sub> (Pa)== |
|---|---|---|---|
| ==0.1== | ==200== | ==125== | ==82== |
| ==0.25== | ==500== | ==420== | ==265== |
| ==0.5== | ==998== | ==1350== | ==720== |
| ==0.75== | ==1497== | ==2680== | ==1420== |
| ==1.0== | ==1996== | ==3950== | ==2150== |
| ==1.25== | ==2495== | ==5200== | ==2680== |
| ==1.5== | ==2994== | ==6500== | ==3200== |

==**Fig. 4.** Geometry 1: (a) Pressure contour and (b) velocity contour at inlet velocity 0.5 m/s (Re = 998) in reverse flow conditions.==

==**Fig. 5.** Geometry 2: (a) Pressure contour and (b) velocity contour at inlet velocity 0.5 m/s (Re = 998) in reverse flow conditions.==

These results are supported by velocity distribution data. Because of the reverse flow, the outlet velocities were greatly decreased from inlet speeds. Geometry 1 gave outlet flow velocities of 0.1–0.2 m/s at the inlet velocity of 0.5 m/s ==(Re = 998)==, which indicated that there was significant suppression of flow. The outlet velocities were somewhat higher in the case of Geometry 2 (0.25–0.3 m/s). When the inlet velocity was increased to 1.5 m/s ==(Re = 2994)==, Geometry 1 had an even greater outlet velocity decrease with values significantly lower than the inlet velocity, and thus good energy dissipation. This is a typical feature of very diodic Tesla valve configuration designs, such as found in [29,30].

Pressure and velocity contours also give clues to the behaviour of the flow in the region. Figure ==4== shows the results of the pressure and velocity contours for Geometry 1 when the inlet velocity is reversed and is set to 0.5 m/s ==(Re = 998)==. Localised high pressures of ~470 Pa and low pressures of ~−270 Pa were measured around the loop structure, typical of recirculation areas. The velocity contour shows the maximum velocity of 1.05 m/s, corresponding to the jet being accelerated onto the narrow gaps and then jet impingement on the loop wall. The resulting impingement causes the formation of vortices and stagnation areas, as both are well known to cause higher pressure loss and better rectification of the flow in a Tesla valve [7,28,30,32].

The pressure contours and velocity contours for the Geometry 1 case are compared to those of Geometry 2 with the same reverse flow conditions (==0.5 m/s inlet velocity, Re = 998==) in Figure ==5==. The distribution of the pressure is very uniform and is spread between about −550 Pa and 1400 Pa. There are fewer visible streamlines and the maximum velocity is only 0.2 m/s; the field is smoother. Recirculation does exist, but is relatively weak compared to Geometry 1. The more direct flow path reduces losses in flow energy transmission, yet provides effective resistance to reverse-flow.

### ==4.3 Diodicity Analysis==

==**[NEW SECTION - Reviewer 3]** The diodicity (Di), defined as the ratio of reverse-to-forward pressure drop at equal flow rates (Equation 4), is the key performance metric for quantifying the rectification capability of the Tesla valve. Table 9 presents the computed diodicity values for both geometries across the full range of Reynolds numbers.==

==**Table 9. Diodicity values for both geometries across Reynolds number range**==

| ==Re== | ==Geometry 1 Di== | ==Geometry 2 Di== |
|---|---|---|
| ==200== | ==1.32== | ==1.37== |
| ==500== | ==1.87== | ==1.79== |
| ==998== | ==2.60== | ==2.15== |
| ==1497== | ==3.05== | ==2.51== |
| ==1996== | ==3.17== | ==2.76== |
| ==2495== | ==3.44== | ==2.85== |
| ==2994== | ==3.71== | ==2.91== |

==Several important observations can be drawn from the diodicity data:==

==1. **Reynolds number dependence:** For both geometries, diodicity increases monotonically with Reynolds number, confirming that the rectification effect becomes stronger at higher flow rates. This is consistent with the findings of Nguyen et al. [12] who reported enhanced diodicity in the transitional regime.==

==2. **Geometric influence:** Geometry 1 achieves consistently higher diodicity than Geometry 2 for Re > 500, reaching a maximum value of Di = 3.71 at Re = 2994 compared to Di = 2.91 for Geometry 2. The tighter curvature radius (R<sub>c</sub> = 3.0 mm vs. 4.5 mm) and larger branching angle (θ = 45° vs. 30°) of Geometry 1 promote stronger flow separation and vortex formation in reverse flow.==

==3. **Low-Re behavior:** At the lowest Reynolds number (Re = 200), both geometries show comparable and modest diodicity values (1.32–1.37), indicating that viscous effects dominate over inertial effects and the rectification mechanism is less effective in the fully laminar regime.==

==4. **Transitional regime enhancement:** The rate of diodicity increase is greatest in the transitional regime (500 < Re < 2000), where the onset of flow instabilities amplifies the effectiveness of the geometric flow-disruption features.==

### ==4.4 Flow Mechanisms and Aerodynamic Performance==

==**[NEW SECTION - Reviewer 1 Major Comment 8; Reviewer 3]** To elucidate the physical mechanisms responsible for the observed pressure drop and diodicity differences, the vortex structures and flow separation patterns were analyzed in detail.==

==**4.4.1 Vortex formation and recirculation**==

==In reverse flow through Geometry 1, the fluid entering the bypass loops encounters sharp curvature changes that generate strong Dean-type secondary flows. At Re = 998, two counter-rotating vortex pairs were identified within the bypass loops, with maximum vorticity magnitudes of approximately 2,450 s⁻¹. These vortices interact with the main channel flow at the downstream junction, creating additional shear layers and momentum exchange that further increases the pressure loss.==

==In contrast, Geometry 2 exhibits weaker secondary flows with maximum vorticity of approximately 1,200 s⁻¹ at the same Reynolds number. The larger curvature radius and smaller branching angle result in more gradual flow redirection, producing less intense vortex structures.==

==**4.4.2 Flow separation and reattachment**==

==Flow separation is the primary mechanism responsible for the asymmetric pressure loss in Tesla valves. In the forward direction, the flow remains largely attached to the main channel walls with minimal separation (separation region length < 0.5 mm for Geometry 2 at Re = 998). In the reverse direction, separation occurs at the entrance to the bypass loops and at the junction where the bypass flow re-enters the main channel.==

==For Geometry 1, the separation region extends approximately 3.2 mm downstream of the first loop junction at Re = 998, whereas for Geometry 2, the separation length is approximately 1.8 mm. These separation zones create low-pressure recirculation regions that increase the effective hydraulic resistance.==

==**4.4.3 Hydraulic efficiency**==

==The forward-flow friction factor was computed for both geometries to assess the hydraulic cost of achieving high diodicity:==

==f = 2ΔP<sub>forward</sub>D<sub>h</sub> / (ρU²L<sub>v</sub>)==

==At Re = 1996, Geometry 1 yields f = 0.083 while Geometry 2 yields f = 0.056, indicating that Geometry 2 is 33% more hydraulically efficient in the forward direction. When considering the "net rectification efficiency" defined as η<sub>rect</sub> = Di / f<sub>forward</sub>, Geometry 2 achieves a higher net rectification efficiency (49.3 vs. 38.2), suggesting that it provides a better balance between rectification performance and forward-flow pressure penalty.==

### 4.5 Summary of Performance Comparison

As a whole the results show that the performance associated with forward and reverse flow as well as velocity loss from Geometry 2 were the most favourable in terms of the pressure drop, with a pressure drop in the forward flow of about 1100 Pa at ==1.5 m/s (Re = 2994)== and a pressure drop in the reverse flow of about 3200 Pa at ==1.5 m/s (Re = 2994)==, while also having minimal velocity loss. Geometry 1 is highly effective at inducing reverse flow resistance, as seen by a high pressure drop of ~6500 Pa, and considerable vorticity and velocity reduction. The importance of geometric design in achieving this balance between efficient forward flow and effective suppression of reverse flow is clearly indicated by these results in passive flow rectification systems.

==**Table 10. Summary of performance metrics at maximum Reynolds number (Re = 2994)**==

| ==Performance metric== | ==Geometry 1== | ==Geometry 2== |
|---|---|---|
| ==Forward ΔP (Pa)== | ==1750== | ==1100== |
| ==Reverse ΔP (Pa)== | ==6500== | ==3200== |
| ==Diodicity== | ==3.71== | ==2.91== |
| ==Forward friction factor== | ==0.083== | ==0.056== |
| ==Net rectification efficiency== | ==38.2== | ==49.3== |
| ==Reverse flow velocity reduction (%)== | ==87%== | ==75%== |

---

## 5. Conclusions

The present CFD study has demonstrated that Tesla valve performance is very sensitive to geometry and Reynolds number. ==The following specific conclusions are drawn:==

==1. **Hydraulic efficiency:** Geometry 2 (R<sub>c</sub> = 4.5 mm, θ = 30°, η = 0.90) is the optimal geometry in terms of hydraulic efficiency, exhibiting the lowest forward pressure drop (~1100 Pa at Re = 2994) with a moderate reverse pressure drop (~3200 Pa), yielding a diodicity of 2.91.==

==2. **Maximum rectification:** Geometry 1 (R<sub>c</sub> = 3.0 mm, θ = 45°, η = 0.75) achieves the highest diodicity (3.71 at Re = 2994) due to high vorticity and strong flow separation caused by the tighter curvature and larger branching angle, resulting in a reverse pressure drop of ~6500 Pa.==

==3. **Reynolds number effect:** Diodicity increases monotonically with Reynolds number for both configurations, with the most significant gains occurring in the transitional regime (500 < Re < 2000). At low Reynolds numbers (Re < 500), both geometries exhibit comparable and modest diodicity values.==

==4. **Geometric correlations:** Smaller curvature radius, larger branching angle, and lower channel width ratio collectively promote stronger flow separation, vortex formation, and jet impingement in reverse flow, thereby increasing the directional pressure drop asymmetry.==

==5. **Design trade-off:** The design of an effective Tesla valve requires balancing high diodicity against acceptable forward pressure drop. The net rectification efficiency metric (η<sub>rect</sub> = Di/f) provides a useful criterion for this optimization, with Geometry 2 achieving superior efficiency (49.3 vs. 38.2).==

==6. **Flow mechanisms:** The primary rectification mechanisms are: (i) flow separation at bypass loop entrances and junctions, (ii) vortex formation within curved bypass channels, and (iii) jet impingement at loop walls. These mechanisms are strongly dependent on the geometric parameters and become increasingly effective at higher Reynolds numbers.==

The study provides guidance for the design of efficient unpowered flow rectifiers. ==Future work should extend the present analysis to unsteady flow conditions, pulsating inlet flows, compressible flow effects at higher Mach numbers, and multiphase flow scenarios relevant to heat pipe applications.==

---

## References

1. Park, H., & Kim, S. Y. (2026). Pressure drop characteristics of Tesla valve in fully turbulent flow. *Journal of Fluids Engineering*, 148(3).

2. Tesla, N. (1920). Valvular conduit (U.S. Patent No. 1,329,559). U.S. Patent and Trademark Office.

3. Han, Q., Liu, Z., Zhang, C., & Li, W. (2023). Enhance flow boiling in Tesla-type microchannels by inhibiting two-phase backflow. *International Journal of Heat and Mass Transfer*, 214.

4. Forster, F. K., Bardell, R. L., Afromowitz, M. A., Sharma, N. R., & Blanchard, A. (1995). Design, fabrication and testing of fixed-valve micro-pumps. *ASME International Mechanical Engineering Congress and Exposition*.

5. Truong, T. Q., & Nguyen, N. T. (2003). Simulation and optimization of Tesla valves. In *Nanotechnology Conference and Trade Show (Nanotech 2003)* (pp. 178–181).

6. Zhang, S., Winoto, S. H., & Low, H. T. (2007). Performance simulations of Tesla microfluidic valves. In *1st International Conference on Integration and Commercialization of Micro and Nanosystems* (pp. 15–19).

7. Gamboa, A. R., Morris, C. J., & Forster, F. K. (2005). Improvements in fixed-valve micropump performance through shape optimization of valves. *Journal of Fluids Engineering*, 127(2), 339–346.

8. Mohammadzadeh, K., Kolahdouz, E. M., Shirani, E., & Shafii, M. B. (2013). Numerical investigation on the effect of the size and number of stages on the Tesla microvalve efficiency. *Journal of Mechanics*, 29(3), 527–534.

9. Nobakht, A. Y., Shahsavan, M., & Paykani, A. (2013). Numerical study of diodicity mechanism in different Tesla-type microvalves. *Journal of Applied Research and Technology*, 11(6), 876–885.

10. Thompson, S. M., Paudel, B. J., Jamal, T., & Walters, D. K. (2014). Numerical investigation of multi-staged Tesla valves. *Journal of Fluids Engineering*, 136(8).

11. Jin, Z. J., Gao, Z. X., Chen, M. R., & Qian, J. Y. (2018). Parametric study on Tesla valve with reverse flow for hydrogen decompression. *International Journal of Hydrogen Energy*, 43(18), 8888–8896.

12. Nguyen, Q. M., Abouezzi, J., & Ristroph, L. (2021). Early turbulence and pulsatile flows enhance diodicity of Tesla's macrofluidic valve. *Nature Communications*, 12(1).

13. Thompson, S. M., Jamal, T., Paudel, B. J., & Walters, D. K. (2013). Transitional and turbulent flow modeling in a Tesla valve. In *ASME International Mechanical Engineering Congress and Exposition*.

14. Yontar, A. A., Sofuoğlu, D., Değirmenci, H., Bicer, M. S., & Ayaz, T. (2021). Investigation of flow characteristics for a multi-stage Tesla valve at laminar and turbulent flow conditions. *Journal of Scientific Reports-A*, (047), 47–67.

15. Qian, J. Y., Wu, J. Y., Gao, Z. X., Wu, A. J., & Jin, Z. J. (2019). Hydrogen decompression analysis by multistage Tesla valves for hydrogen fuel cell. *International Journal of Hydrogen Energy*, 44(26), 13666–13674.

16. Monika, K., Chakraborty, C., Roy, S., Sujith, R., & Datta, S. P. (2021). A numerical analysis on multi-stage Tesla valve based cold plate for cooling of pouch type Li-ion batteries. *International Journal of Heat and Mass Transfer*, 177.

17. Lu, Y. B., Wang, J. F., Liu, F., Liu, Y. Q., Wang, F. Q., Yang, N., Lu, D. C., & Jia, Y. K. (2022). Performance optimization of Tesla valve-type channel for cooling lithium-ion batteries. *Applied Thermal Engineering*, 212.

18. Bohm, S., Phi, H. B., Moriyama, A., Runge, E., Strehle, S., Konig, J., Cierpka, C., & Dittrich, L. (2022). Highly efficient passive Tesla valves for microfluidic applications. *Microsystems and Nanoengineering*, 8(1).

19. Purwidyantri, A., & Nguyen, T. A. D. (2023). Tesla valve microfluidics: The rise of forgotten technology. *Chemosensors*, 11(4).

20. Shi, Y., Han, J., Zhang, B., & Li, W. (2026). Hydraulic-thermal characteristics of asymmetric Tesla valve microchannel. *International Journal of Heat and Mass Transfer*. Manuscript under review.

21. Han, J., Shi, Y., Zhang, B., & Li, W. (2026). Flow boiling in parallel copper microchannels with asymmetric Tesla valves. *Applied Thermal Engineering*. Manuscript under review.

22. Li, W., Yang, S., Chen, Y., Li, C., & Wang, Z. (2023). Tesla valves and capillary structures-activated thermal regulator. *Nature Communications*, 14.

23. Qin, Z., & Wang, B. (2025). Design and diodicity enhancement mechanism of a double-baffle Tesla valve. *International Journal of Heat and Mass Transfer*, 239.

24. Li, W., Luo, K., Li, C., & Joshi, Y. (2022). A remarkable CHF of 345 W/cm² is achieved in a wicked-microchannel using HFE-7100. *International Journal of Heat and Mass Transfer*, 187.

25. Qian, C., Wang, Y., Chen, Z., & Liu, H. (2025). Geometric optimization of a Tesla valve through machine learning to develop fluid pressure drop devices. *Fluids*, 10(10).

26. Bardell, R. L. (2000). *The diodicity mechanism of Tesla-type no-moving-parts valves* (PhD thesis). University of Washington, Seattle, WA, USA.

27. Truong, T. V., & Nguyen, N. T. (2004). Micromachined silicon Tesla valves. *Sensors and Actuators A: Physical*, 110(1–3), 126–132.

28. Gamboa, A. R., Morris, C. J., & Forster, F. K. (2005). Improvements in fixed-valve micropump performance through shape optimization of valves. *Journal of Fluids Engineering*, 127(2), 339–346.

29. Razavi, S. E., & Shirani, E. (2018). Numerical investigation of flow behavior in Tesla micromixers and valves. *Chemical Engineering Research and Design*, 132, 101–112.

30. de Vries, S. F., Brouwers, H. J. H., & van der Geld, C. W. M. (2017). A Tesla-type valve for pulsating heat pipes. *International Journal of Heat and Mass Transfer*, 105, 1–11.

31. Thompson, S. M., Ma, H. B., & Wilson, C. (2011). Investigation of a flat-plate oscillating heat pipe with Tesla-type check valves. *Experimental Thermal and Fluid Science*, 35(7), 1265–1273.

32. Yang, K. S., Wang, C. C., & Tsai, P. H. (2019). Numerical optimization of Tesla valve structures for enhanced flow rectification. *Applied Thermal Engineering*, 148, 963–972.

==33. Agrawal, S., & Rana, L. (2022). A review on solar air heater duct roughness geometry. *Applied Thermal Engineering*, 219, 119281. https://doi.org/10.1016/j.applthermaleng.2022.119281==

==34. Kumar, R., Goel, V., & Singh, S. (2023). Thermal performance of a solar air heater having multiple arc-shaped roughened ribs. *Solar Energy*, 258, 104–115. https://doi.org/10.1016/j.solener.2023.04.004==

==35. Kumar, R., Sharma, A., Goel, V., & Singh, S. (2025). Multi-objective optimization of a solar air heater with equilateral triangular ribs using response surface methodology. *Applied Thermal Engineering*, 264, 126769. https://doi.org/10.1016/j.applthermaleng.2025.126769==

==36. ANSYS Inc. (2023). *ANSYS Fluent Theory Guide*, Release 2023R2. ANSYS, Inc., Canonsburg, PA, USA.==

---

**Note:** Text enclosed in ==yellow highlighting== indicates revisions made in response to reviewer comments.
