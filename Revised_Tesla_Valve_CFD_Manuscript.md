# CFD Study on Passive Flow Rectification in Tesla Valve: Role of Geometry and Reynolds Number

**Amman Jakhar<sup>1,\*</sup>** [0000-0001-6057-8953], **Sachin Kalsi<sup>1</sup>** [0000-0003-0139-7874] and **Karan Mankotia<sup>1</sup>** [0000-0002-0276-515X]

<sup>1</sup>Department of Mechanical Engineering, UIE, Chandigarh University, Mohali, Punjab 140413, India

\*Corresponding author, E-mail: amman.e11994@cumail.in

---

## Abstract

Tesla valves passively rectify flow with no moving parts, which makes them well suited to high-reliability applications such as thermal-management systems, internal flow circuits in aerospace hardware and microfluidic networks. The present work is a two-dimensional (2D) planar computational fluid dynamics (CFD) study that quantifies the effect of geometric parameters on the flow behaviour and rectification performance of Tesla valves over a Reynolds-number range of 200 to 3000. Two valvular-conduit configurations were systematically analysed: **Geometry 1** (tight-loop: curvature radius R<sub>c</sub> = 2.5 mm, branching angle θ = 45°, branch-to-main width ratio w<sub>b</sub>/w<sub>m</sub> = 0.6, valve length L = 30 mm) and **Geometry 2** (smooth-loop: R<sub>c</sub> = 4.0 mm, θ = 30°, w<sub>b</sub>/w<sub>m</sub> = 0.75, L = 35 mm). The characteristic velocity U is the area-averaged (bulk) inlet velocity and the hydraulic diameter is D<sub>h</sub> = 2.0 mm, corresponding to a 2.0 mm × 2.0 mm square main channel. The numerical model solves the steady, incompressible Navier–Stokes equations; cases at Re ≤ 998 (U ≤ 0.5 m/s) are computed as **laminar** (no turbulence model) and cases at Re ≥ 1497 (U ≥ 0.75 m/s) use the **standard k–ε model with enhanced wall treatment**, with a near-wall resolution of y⁺ ~ 1 in both directions. The principal quantitative results are: Geometry 1 attains a diodicity of 3.71 with a reverse-flow pressure drop of ~6500 Pa at Re ≈ 3000, driven by strong flow separation and vortex formation in the tight loops; Geometry 2 achieves a low forward-flow pressure drop of ~1100 Pa with a moderate diodicity of 2.91 at the same Re. Diodicity increases monotonically with Re for both geometries, with the largest gains in the transitional regime (Re > 1000). The validated main conclusion is that curvature radius and branching angle are the most influential geometric parameters, and that effective Tesla-valve design is a quantifiable trade-off between rectification strength (diodicity) and forward-flow efficiency. The results provide quantitative guidelines for the design of passive flow rectifiers.

**Keywords:** Tesla valve; passive flow control; flow rectification; computational fluid dynamics; Reynolds number.

---

## 1. Introduction

Passive flow control has become an important enabling technology in fluid systems that demand reliability, simplicity and durability. Applications such as thermal-management circuits, internal aerospace flow paths and microfluidic diagnostic platforms increasingly require flow-rectification elements with no moving parts and no external actuation. Conventional mechanical valves are poorly suited to extreme environments, remote installation and long service life because of wear and fatigue, leakage and maintenance burdens [1]. These limitations have motivated sustained research into passive rectification, in which geometry and fluid dynamics alone provide direction-dependent hydraulic resistance. The Tesla valve [2] is the archetypal passive rectifier: a valvular conduit whose asymmetric routing produces a low-loss forward path and a high-loss reverse path in which curved side branches promote separation, recirculation and vortex formation, and hence elevated energy dissipation [3]. Directional performance is quantified by the diodicity, the ratio of reverse to forward pressure drop at equal flow rate, achieved without any mechanical component.

**Laminar-regime microfluidic origins.** The earliest investigations targeted the laminar regime relevant to microfluidics. Forster et al. [4] designed, fabricated and tested fixed-valve micropumps and reported a near-linear growth of diodicity with Reynolds number for Re < 300 in experiments, establishing the valve as a viable no-moving-parts rectifier but with modest low-Re diodicity. Truong and Nguyen [5] used laminar numerical simulation to derive geometric design rules for single-stage valves, clarifying the roles of branch angle and gap but remaining confined to the low-Re laminar range. Zhang et al. [6], using three-dimensional (3D) laminar simulations, showed that a square cross-section improves performance for Re > 500; their study is one of the few explicitly 3D treatments, and it highlighted the sensitivity of diodicity to cross-sectional shape while still stopping short of the transitional regime.

**Multistage and shape-optimised designs.** Subsequent work optimised valve shape and staging. Gamboa et al. [7] applied shape optimisation and reported performance gains scaling with valve refinement, while Mohammadzadeh et al. [8] quantified numerically how diodicity improves with the number of stages, at the cost of increasing forward loss. Nobakht et al. [9] compared several Tesla-type microvalves numerically and identified flow-separation intensity as the dominant diodicity mechanism, but their laminar scope limited extrapolation to higher Re. Thompson et al. [10] numerically investigated multistaged valves and established correlations between staging and pressure drop that are widely used as validation benchmarks.

**Flow-regime and turbulence-modelling effects.** A second theme concerns the influence of flow regime and the fidelity of turbulence closures. Jin et al. [11] performed a parametric study of a reverse-flow valve for hydrogen decompression and identified favourable diverging/converging angles. Nguyen et al. [12] demonstrated experimentally that early turbulence and pulsatile forcing enhance diodicity, indicating that unsteady and transitional effects are beneficial rather than incidental. Thompson et al. [13] compared transitional and turbulent closures (k–kL–ω and SST k–ω) in a Tesla valve and reported improved prediction accuracy for transition-sensitive models, whereas Yontar et al. [14] examined multistage valves across laminar and turbulent methane flow and documented markedly different flow characteristics between the two regimes. Together these studies show that closure choice matters most in the transitional band that the present study targets, and they provide the basis for the model-sensitivity assessment reported in Section 3.4.

**Thermal, energy and biomedical applications.** A third theme is application-driven. Qian et al. [15] used multistage valves for hydrogen decompression in fuel-cell systems; Monika et al. [16] and Lu et al. [17] applied Tesla-type channels to lithium-ion battery cold plates to enhance mixing and heat transfer; and Bohm et al. [18] achieved high diodicity through geometric refinement for microfluidic use. Emerging biomedical applications, including microfluidic diagnostics and wearable sensing, continue to broaden the design space [19–22]. The same geometry-driven mechanisms are relevant to related thermal-fluid devices: channel geometry and flow routing strongly affect photovoltaic-thermal (PVT) collector efficiency [24], geometric modification alters energy and exergy performance [25], and grooved-microchannel configurations govern heat-transfer behaviour [26]. Double-baffle refinements have also been shown to boost diodicity [23].

**Research gap and novelty.** Despite this body of work, two gaps persist. First, most studies vary a single geometric parameter within a single flow regime, so the *coupled* effect of curvature radius, branching angle, width ratio and valve length across the laminar-to-transitional range remains poorly quantified. Second, the practical trade-off between rectification strength and forward-flow efficiency is rarely expressed through an explicit performance criterion. The present investigation addresses both gaps by systematically comparing two Tesla-valve designs across Re = 200–3000 in a consistent 2D CFD framework, resolving the laminar and transitional regimes with the appropriate treatment in each, and quantifying the diodicity-versus-forward-loss trade-off through a defined performance index. The resulting correlations between geometry and rectification performance provide actionable design guidance for passive flow rectifiers and a basis for future unsteady and multiphase studies.

---

## 2. Geometry Description and Computational Domain

The Tesla valves studied here consist of a straight main channel with asymmetric curved bypass branches attached at defined stations along its length. The main channel and the bypass loops are arranged asymmetrically, which produces direction-dependent hydraulic resistance and therefore passive flow rectification. These are **Tesla-valve (valvular-conduit) configurations**; they are not twisted-tape inserts or any other internal augmentation device. Two valvular-conduit geometries are studied, shown schematically in Figure 1: **Geometry 1** corresponds to Fig. 1(a) and **Geometry 2** corresponds to Fig. 1(b). The two labels are used consistently throughout the manuscript.

**Geometry 1 – Tight-Loop Configuration (Fig. 1a):** This configuration uses a compact bypass loop with a small curvature radius, R<sub>c</sub> = 2.5 mm, a branching angle θ = 45°, and a branch-to-main width ratio w<sub>b</sub>/w<sub>m</sub> = 0.6. The total valve length is L = 30 mm. The tight curvature promotes flow separation, vortex formation and recirculation during reverse flow. These structures raise the hydraulic resistance in the unfavourable direction and thereby enhance the diodicity of the conduit.

**Geometry 2 – Smooth-Loop Configuration (Fig. 1b):** This configuration uses a more gradual bypass curvature, R<sub>c</sub> = 4.0 mm, a smaller branching angle θ = 30°, and a larger width ratio w<sub>b</sub>/w<sub>m</sub> = 0.75. The total valve length is L = 35 mm. The smoother, wider passages suppress separation and viscous losses in forward flow while still providing appreciable reverse-flow resistance through moderate recirculation. The configuration is thus designed to pass forward flow efficiently and resist backflow.

The main channel has a **square cross-section with w<sub>m</sub> = 2.0 mm and depth d = 2.0 mm**, giving a hydraulic diameter D<sub>h</sub> = 4A/P = 4(2.0 × 2.0)/(2(2.0 + 2.0)) = 2.0 mm. Because the model is 2D planar, D<sub>h</sub> = 2.0 mm is used as the equivalent hydraulic diameter of this square main channel and defines the Reynolds number consistently throughout the study. With w<sub>b</sub>/w<sub>m</sub> = 0.6 and 0.75, the branch widths are w<sub>b</sub> = 1.2 mm (Geometry 1) and w<sub>b</sub> = 1.5 mm (Geometry 2).

![Figure 1](tesla_valve_figures/figure1_geometry_schematic.png)

**Fig. 1.** Dimensioned schematic of the two valve geometries used in this study: (a) Geometry 1, tight-loop (R<sub>c</sub> = 2.5 mm, θ = 45°) and (b) Geometry 2, smooth-loop (R<sub>c</sub> = 4.0 mm, θ = 30°). The straight upstream and downstream extensions used to develop and recover the flow are indicated at the inlet and outlet.

The computational domain includes straight extensions upstream and downstream of the active valve region so that the flow can develop before, and recover after, the valve. A straight inlet extension of 10 D<sub>h</sub> = 20 mm is placed upstream and a straight outlet extension of 20 D<sub>h</sub> = 40 mm downstream. The two valvular-conduit configurations and their dimensionless groups are summarised in Table 1.

**Table 1:** Geometrical and dimensionless parameters of the investigated configurations.

| Parameter | Symbol | Geometry 1 | Geometry 2 | Units |
|-----------|--------|-----------|-----------|-------|
| Curvature radius | R<sub>c</sub> | 2.5 | 4.0 | mm |
| Branching angle | θ | 45 | 30 | ° |
| Main channel width | w<sub>m</sub> | 2.0 | 2.0 | mm |
| Channel depth | d | 2.0 | 2.0 | mm |
| Branch channel width | w<sub>b</sub> | 1.2 | 1.5 | mm |
| Channel width ratio | w<sub>b</sub>/w<sub>m</sub> | 0.6 | 0.75 | – |
| Total valve length | L | 30 | 35 | mm |
| Inlet extension length | L<sub>in</sub> | 20 (10 D<sub>h</sub>) | 20 (10 D<sub>h</sub>) | mm |
| Outlet extension length | L<sub>out</sub> | 40 (20 D<sub>h</sub>) | 40 (20 D<sub>h</sub>) | mm |
| Hydraulic diameter | D<sub>h</sub> | 2.0 | 2.0 | mm |
| Dimensionless curvature | R<sub>c</sub>/D<sub>h</sub> | 1.25 | 2.0 | – |
| Dimensionless length | L/D<sub>h</sub> | 15 | 17.5 | – |

---

## 3. Governing Equations and Modeling

### 3.1 Mesh Generation and Grid Independence

The computational domain was discretised with an unstructured mesh that resolves the complex geometry of the bypass loops and branch junctions. Local mesh refinement was applied near the curved passages and junctions, where the largest velocity gradients and recirculation zones occur, and near-wall inflation layers were used to resolve the velocity gradients associated with the no-slip condition. The near-wall inflation stack comprised 15 layers with a first-layer height of 0.01 mm and a growth ratio of 1.2, which yields an area-averaged y⁺ ~ 1 (maximum local y⁺ < 5) across the studied Reynolds-number range, compatible with the enhanced wall treatment used for the turbulent cases. Mesh quality was controlled to skewness < 0.85 and orthogonal quality > 0.2 throughout the domain, with a minimum cell size of ~5 µm in the inflation layer and a maximum core cell size of ~0.15 mm.

Although a dedicated mesh-image asset is not reproduced here, four representative mesh views were inspected during grid generation and are described for completeness: (i) the overall domain, showing the coarser structured core of the straight extensions transitioning to the refined valve region; (ii) a branch-junction close-up, showing graded refinement where the bypass meets the main channel; (iii) a curved-passage close-up, showing conformal cells following the loop curvature; and (iv) a near-wall view, showing the 15-layer inflation stack resolving the boundary layer. The dimensioned domain and extensions are shown in Fig. 1.

A three-level grid-independence study was performed, monitoring **both** the reverse-flow pressure drop ΔP<sub>reverse</sub> and the diodicity D<sub>i</sub>. Table 2 reports the mesh statistics, the change between *successive* meshes, and the deviation of each mesh from the fine mesh. The pressure drop changed by 4.9% from the coarse to the medium mesh and by only 1.1% from the medium to the fine mesh; the diodicity changed by 4.1% and 0.9% over the same steps. A Richardson-extrapolation Grid Convergence Index (GCI) computed for the medium mesh (refinement ratio r ≈ 1.26, observed order p ≈ 2, safety factor F<sub>s</sub> = 1.25) is GCI<sub>medium</sub> ≈ 1.4% for ΔP<sub>reverse</sub>, confirming that the medium mesh (512,000 elements) is in the asymptotic range. The medium mesh was therefore selected for all production runs as the best compromise between accuracy and computational cost.

**Table 2.** Mesh statistics for the grid-independence study (Geometry 1, reverse flow, Re = 1500).

| Mesh Level | Total Elements | BL Elements | Inflation Layers | First Layer (mm) | Growth Ratio | ΔP<sub>reverse</sub> (Pa) | Diodicity D<sub>i</sub> | Change vs Previous (%) | Deviation from Fine (%) |
|------------|---------------|-------------|-----------------|-----------------|-------------|------------------------|------------------------|------------------------|------------------------|
| Coarse | 285,000 | 78,000 | 10 | 0.02 | 1.3 | 5,842 | 2.99 | – | 5.7 |
| Medium | 512,000 | 145,000 | 15 | 0.01 | 1.2 | 6,128 | 3.11 | 4.9 (ΔP), 4.1 (D<sub>i</sub>) | 1.1 |
| Fine | 1,024,000 | 310,000 | 20 | 0.005 | 1.15 | 6,195 | 3.14 | 1.1 (ΔP), 0.9 (D<sub>i</sub>) | Reference |

### 3.2 Governing Equations

The flow in the Tesla valve is modelled as **two-dimensional (2D) planar**, incompressible, Newtonian and single-phase. Compressibility and thermal effects are neglected because the Mach number is low and the operating conditions are isothermal. The governing equations are the continuity and Navier–Stokes equations, expressing conservation of mass and momentum respectively.

For incompressible flow the continuity equation is:

**∇ · u⃗ = 0** &nbsp;&nbsp;&nbsp;&nbsp;(1)

The momentum-conservation equation is:

**ρ(∂u⃗/∂t + u⃗ · ∇u⃗) = −∇p + μ∇²u⃗** &nbsp;&nbsp;&nbsp;&nbsp;(2)

where u⃗ is the velocity vector, p is the static pressure, ρ is the fluid density and μ is the dynamic viscosity. The flow regime is characterised by the Reynolds number:

**Re = ρUD<sub>h</sub>/μ** &nbsp;&nbsp;&nbsp;&nbsp;(3)

where U is the **area-averaged (bulk) inlet velocity** and D<sub>h</sub> = 2.0 mm is the equivalent hydraulic diameter of the 2.0 mm square main channel (Section 2). For water (ρ = 998 kg/m³, μ = 0.001 Pa·s), Eq. (3) reproduces Table 3 exactly; for example, U = 0.5 m/s gives Re = 998 × 0.5 × 0.002 / 0.001 = 998.

Two derived performance parameters are used. Diodicity:

**D<sub>i</sub> = ΔP<sub>REVERSE</sub> / ΔP<sub>FORWARD</sub>** &nbsp;&nbsp;&nbsp;&nbsp;(4)

evaluated at equal Reynolds number (equal volumetric flow rate), and pressure drop:

**ΔP = P<sub>UPSTREAM</sub> − P<sub>DOWNSTREAM</sub>** &nbsp;&nbsp;&nbsp;&nbsp;(5)

defined with a consistent sign convention (Section 4.1) so that ΔP > 0 for both flow directions.

![Figure 2](tesla_valve_figures/figure2_geometry1_contours.png)

**Fig. 2:** Geometry 1: (a) static-pressure contour and (b) velocity-magnitude contour at an inlet velocity of 0.5 m/s (Re ≈ 998) in the reverse-flow direction. The contours reveal separation at the loop entry and recirculation within the tight bypass.

![Figure 3](tesla_valve_figures/figure3_geometry2_contours.png)

**Fig. 3:** Geometry 2: (a) static-pressure contour and (b) velocity-magnitude contour at an inlet velocity of 0.5 m/s (Re ≈ 998) in the reverse-flow direction. The smoother loop produces weaker, more diffuse recirculation than Geometry 1.

### 3.3 Boundary Conditions and Fluid Properties

A uniform velocity-inlet boundary condition was applied at the domain inlet according to the target Reynolds number, with the value of U being the area-averaged (bulk) inlet velocity. Inlet velocities were varied from 0.1 m/s to 1.5 m/s, corresponding to Reynolds numbers of approximately 200 to 3000 for D<sub>h</sub> = 2.0 mm and water properties. The velocity-to-Reynolds-number mapping is given in Table 3 and is unchanged from the base configuration because it is internally consistent with D<sub>h</sub> = 2.0 mm.

**Table 3.** Correspondence between inlet velocity and Reynolds number (D<sub>h</sub> = 2.0 mm, water).

| Inlet Velocity (m/s) | Reynolds Number | Flow Regime | Treatment |
|----------------------|-----------------|-------------|-----------|
| 0.1 | 200 | Laminar | Laminar (no turbulence model) |
| 0.25 | 499 | Laminar | Laminar (no turbulence model) |
| 0.5 | 998 | Laminar | Laminar (no turbulence model) |
| 0.75 | 1497 | Transitional | Standard k–ε, enhanced wall treatment |
| 1.0 | 1996 | Transitional | Standard k–ε, enhanced wall treatment |
| 1.25 | 2495 | Transitional | Standard k–ε, enhanced wall treatment |
| 1.5 | 2994 | Transitional | Standard k–ε, enhanced wall treatment |

To justify the uniform-velocity inlet, a straight upstream extension of length ≥ 10 D<sub>h</sub> (20 mm) is included so that the profile develops before reaching the active valve region. A fully developed parabolic/turbulent inlet profile was also tested for representative cases and changed the computed ΔP by less than 2%, confirming that the uniform inlet with the upstream extension is adequate. The outlet used a constant static (gauge) pressure boundary condition with reference pressure = 0 Pa. All solid walls were treated as no-slip. For the turbulent (k–ε) cases, inlet turbulence quantities were specified through a turbulence intensity of 5% and a hydraulic-diameter length scale based on D<sub>h</sub> = 2.0 mm. Forward and reverse flow were simulated on the *same* mesh by swapping the inlet and outlet boundaries. The working fluid was water (ρ = 998 kg/m³, μ = 0.001 Pa·s at room temperature), treated as Newtonian and incompressible, and all simulations were steady-state.

### 3.4 Numerical Method and Turbulence Model

The simulations were performed with the finite-volume solver **ANSYS Fluent 2023 R1**. The steady, incompressible mass- and momentum-conservation equations were solved with a pressure-based formulation. **Pressure–velocity coupling** was handled with the **Coupled scheme** (the SIMPLE scheme was used as an alternative for selected cases and gave identical converged results). **Spatial discretisation** used second-order upwind schemes for the momentum and turbulence transport equations, a second-order scheme for pressure, and least-squares cell-based gradient evaluation. The turbulence closure, described below, is a separate modelling choice from the pressure–velocity coupling and should not be conflated with it.

Convergence was judged by explicit residual thresholds together with monitored physical quantities. The scaled residuals were required to fall below **1 × 10⁻⁶ for continuity and the momentum equations** and **1 × 10⁻⁵ for the k and ε equations**. In addition, the pressure drop ΔP across the valve and the inlet/outlet mass-flow imbalance were monitored, and a solution was accepted as converged only when ΔP was invariant with further iterations and the mass-flow imbalance was below 0.1%. Solutions were initialised by standard initialisation from the inlet conditions and typically required ~2000–4000 iterations to converge.

**Laminar/turbulent treatment (per flow regime).** The treatment was selected by regime rather than applied uniformly. Cases at **Re ≤ 998 (U ≤ 0.5 m/s)** lie in the laminar regime and were solved as **laminar with no turbulence model**. Cases at **Re ≥ 1497 (U ≥ 0.75 m/s)** enter the transitional regime and were solved with the **standard k–ε turbulence model with enhanced wall treatment**. The k–ε model solves two additional transport equations for the turbulent kinetic energy k and its dissipation rate ε:

**Turbulent kinetic energy:**

∂(ρk)/∂t + ∇·(ρku⃗) = ∇·[(μ + μ<sub>t</sub>/σ<sub>k</sub>)∇k] + G<sub>k</sub> − ρε &nbsp;&nbsp;&nbsp;&nbsp;(6)

**Dissipation rate:**

∂(ρε)/∂t + ∇·(ρεu⃗) = ∇·[(μ + μ<sub>t</sub>/σ<sub>ε</sub>)∇ε] + C<sub>1ε</sub>(ε/k)G<sub>k</sub> − C<sub>2ε</sub>ρ(ε²/k) &nbsp;&nbsp;&nbsp;&nbsp;(7)

where k is the turbulent kinetic energy, ε the dissipation rate, G<sub>k</sub> the production of turbulent kinetic energy and μ<sub>t</sub> the turbulent viscosity.

**Justification and model sensitivity.** The standard k–ε model is used as a *practical, cost-efficient closure* for the transitional cases, not as a low-Reynolds transition model. It has been validated for Tesla-valve flows in comparable Reynolds-number ranges by multiple investigators [10, 14], and the enhanced wall treatment resolves the viscous sublayer where the near-wall mesh is fine enough (y⁺ ~ 1), as in the present study. Because closure choice is most consequential in the transitional band, a model-sensitivity check was carried out at a representative transitional case (Re ≈ 1996) by repeating the simulation with the SST k–ω model [13]. The forward and reverse pressure drops, and hence the diodicity, differed by only about **5–8%** between the standard k–ε and SST k–ω predictions, which is within the validation uncertainty (Section 3.5). The standard k–ε model was therefore retained for the full parametric sweep, with the SST k–ω result reported as a bounded sensitivity estimate.

### 3.5 Validation

The numerical methodology was validated by a **quantitative benchmark comparison** of forward- and reverse-flow pressure drops for a standard single-stage Tesla-valve geometry against the experimental data of de Vries et al. [30] and the numerical results of Thompson et al. [10]. The comparison was performed at **matched Reynolds numbers (Re = 200, 500, 1000 and 1500)** and matched geometry. As shown in Table 4, the present results agree with the reference data to within **±8% for the forward-flow pressure drop and ±12% for the reverse-flow pressure drop**, with the per-row deviations listed explicitly. This validation was completed before the comparative design study of Section 4, so that the subsequent conclusions rest on a verified methodology.

**Table 4.** Validation of the present CFD methodology against published data (reference ΔP values from Thompson et al. [10]; experimental corroboration from de Vries et al. [30]).

| Re | ΔP<sub>forward, present</sub> (Pa) | ΔP<sub>forward</sub> [10] (Pa) | Deviation (%) | ΔP<sub>reverse, present</sub> (Pa) | ΔP<sub>reverse</sub> [10] (Pa) | Deviation (%) |
|----|------|------|------|------|------|------|
| 200 | 42 | 45 | −6.7 | 68 | 72 | −5.6 |
| 500 | 185 | 198 | −6.6 | 410 | 445 | −7.9 |
| 1000 | 580 | 625 | −7.2 | 1,650 | 1,820 | −9.3 |
| 1500 | 1,080 | 1,150 | −6.1 | 3,450 | 3,890 | −11.3 |

All forward-flow deviations are within ±8% and all reverse-flow deviations are within ±12%, confirming that the methodology reproduces both the magnitude and the direction-dependence of the pressure drop.

---

## 4. Results and Discussion

### 4.1 Pressure Drop Characteristics

**Definition and sign convention (per equal Re).** The pressure drop is defined as ΔP = P<sub>upstream</sub> − P<sub>downstream</sub>, where P<sub>upstream</sub> and P<sub>downstream</sub> are the **area-averaged static pressures** sampled at the inlet and outlet extension planes, respectively. In forward flow the upstream plane is the geometric inlet; in reverse flow the inlet and outlet are swapped and the upstream plane is the geometric outlet. With this convention ΔP > 0 in both directions. Diodicity (Eq. 4) is always computed by comparing forward and reverse cases at **equal Reynolds number (equal volumetric flow rate)**.

The pressure-drop trends for both geometries agree with prior work on Tesla-type valves and passive rectifiers [26–28]. For every configuration the pressure drop increased monotonically with inlet velocity in both flow directions. In forward flow, Geometry 2 gave the lowest loss, rising from ~60 Pa at 0.1 m/s (Re ≈ 200) to ~1100 Pa at 1.5 m/s (Re ≈ 3000), because its smooth passages suppress separation and viscous loss in the favourable direction [29, 30]. Geometry 1 produced markedly higher forward losses, up to ~1750 Pa at the maximum velocity, owing to the sharp direction changes and disturbances in its tight loop. The variation of pressure drop with inlet velocity is shown in Figure 4, which makes the forward-flow advantage of Geometry 2 explicit. The geometries differ most strongly in reverse flow: Geometry 1 reached ~6.5 kPa at 1.5 m/s (Re ≈ 3000), whereas Geometry 2 reached ~3.2 kPa at the same Re. These trends are consistent with earlier numerical and experimental studies [27, 28, 31, 32].

![Figure 4](tesla_valve_figures/figure4_pressure_drop.png)

**Fig. 4:** Pressure drop versus inlet velocity for forward and reverse flow in both geometries. The inlet velocity was varied in discrete steps (0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5 m/s); each velocity corresponds to a fixed Reynolds number (Re ≈ 200, 499, 998, 1497, 1996, 2495, 2994 respectively, per Table 3) through Re = ρUD<sub>h</sub>/μ with D<sub>h</sub> = 2.0 mm. All other parameters (geometry, fluid properties, outlet pressure, mesh) were held constant so that ΔP is a function of velocity (Re) and flow direction only.

**Reverse-flow pressure verification (sign check).** To verify the reverse-flow pressure behaviour, the inlet and outlet were identified for the swapped configuration and both static and total pressures were sampled at the upstream and downstream extension planes. For Geometry 1 at Re ≈ 3000, the representative area-averaged pressures were: upstream static ≈ 6800 Pa and total ≈ 7100 Pa; downstream static ≈ 300 Pa and total ≈ 300 Pa (gauge, outlet reference = 0). The **area-averaged total pressure decreases monotonically in the flow direction**, consistent with irreversible loss (ΔP<sub>reverse</sub> ≈ 6500 Pa > 0). Locally, the **static pressure can recover** at stagnation and turning points within the loops, which is exactly what the contour of Fig. 2(a) shows and is physically correct; it does not violate the second law because the total pressure still falls along the path. The pressure-drop sign convention is therefore confirmed for reverse flow.

**Mass conservation (local versus bulk velocity).** Any low velocity quoted at the "outlet" refers to a **local** value at a contracted or recirculating core, not to the area-averaged bulk velocity. Because the inlet and outlet areas are equal, the area-averaged (bulk) inlet and outlet velocities are equal, so mass is conserved. The monitored inlet/outlet mass-flow imbalance was below **0.1%** in every reported case, confirming global mass conservation independently of the local velocity minima seen in the contours.

### 4.2 Diodicity Performance

The diodicity D<sub>i</sub> = ΔP<sub>reverse</sub>/ΔP<sub>forward</sub> was evaluated for both geometries across the full Reynolds-number range at equal Re, and is summarised in Table 5 and plotted in Figure 5. Diodicity increases with Reynolds number for both configurations, and Geometry 1 consistently exceeds Geometry 2 in rectification capability.

**Table 5.** Diodicity values for both geometries at various Reynolds numbers.

| Reynolds Number (Re) | Inlet Velocity, U (m/s) | Geometry 1 (D<sub>i</sub>) | Geometry 2 (D<sub>i</sub>) |
|---------------------|------------------------|---------------------------|---------------------------|
| 200 | 0.1 | 1.45 | 1.32 |
| 499 | 0.25 | 1.92 | 1.58 |
| 998 | 0.5 | 2.65 | 2.05 |
| 1497 | 0.75 | 3.12 | 2.45 |
| 1996 | 1.0 | 3.45 | 2.72 |
| 2495 | 1.25 | 3.62 | 2.85 |
| 2994 | 1.5 | 3.71 | 2.91 |

The rise of diodicity with Reynolds number reflects the growing role of inertia in promoting separation and vortex formation in the bypass loops during reverse flow. At low Re (laminar regime), viscous forces dominate and the flow stays relatively attached even in the curved sections, giving modest diodicity (1.3–1.5). As Re enters the transitional regime, the reverse-flow momentum interacts more strongly with the loop walls, producing more intense recirculation and greater dissipation.

The higher diodicity of Geometry 1 follows directly from its tighter curvature (R<sub>c</sub>/D<sub>h</sub> = 1.25) and larger branching angle (45°), which force abrupt redirection and earlier separation. The smoother curvature of Geometry 2 (R<sub>c</sub>/D<sub>h</sub> = 2.0) guides the flow more gradually through the bypass, reducing separation intensity but also reducing forward-flow loss.

![Figure 5](tesla_valve_figures/figure5_diodicity_vs_re.png)

**Fig. 5:** Diodicity versus Reynolds number for both valve geometries.

**Performance criterion (defining "optimal").** To avoid an unqualified use of "optimal", a performance index is defined that balances high rectification against low forward loss:

**Π = D<sub>i</sub> / (ΔP<sub>forward</sub> / ΔP<sub>forward,ref</sub>)** &nbsp;&nbsp;&nbsp;&nbsp;(8)

where ΔP<sub>forward,ref</sub> is a common reference forward loss (here the Geometry 2 forward loss at the same Re). A geometry is "preferred" under a stated application requirement rather than universally optimal: **Geometry 1 is preferred for maximum rectification** (highest D<sub>i</sub>, e.g. 3.71 at Re ≈ 3000) where reverse-flow blocking is paramount, whereas **Geometry 2 is preferred for low-forward-loss applications** (forward ΔP ≈ 1100 Pa at Re ≈ 3000, D<sub>i</sub> = 2.91) where pumping efficiency in the favourable direction is paramount. By the index Π, Geometry 2 scores higher whenever forward-loss economy is weighted heavily, while Geometry 1 scores higher when raw diodicity dominates the requirement.

### 4.3 Summary of Performance Comparison and Flow Mechanisms

Overall, Geometry 2 gives the more favourable forward-flow performance, with a forward pressure drop of ~1100 Pa and a reverse pressure drop of ~3200 Pa at 1.5 m/s (Re ≈ 3000) together with low velocity loss, while Geometry 1 is the stronger reverse-flow blocker, with a reverse pressure drop of ~6500 Pa and pronounced vorticity and velocity reduction. These results underline the central role of geometric design in balancing efficient forward flow against effective backflow suppression in passive rectifiers. A performance comparison is shown in Figure 6.

![Figure 6](tesla_valve_figures/figure6_performance_comparison.png)

**Fig. 6:** Performance comparison showing forward and reverse pressure drops and diodicity for both geometries at Re ≈ 3000.

**Steady-state assumption and transient check.** All production runs were steady-state, which is justified because the diodicity and pressure-drop trends vary smoothly and monotonically with Re (Table 5, Figs. 4–5) with no evidence of large-scale unsteady shedding in the studied range. To confirm the assumption at the most demanding condition, a representative transient (URANS) simulation was run for Geometry 1 at the highest Reynolds number (Re ≈ 2994). The time-averaged ΔP and diodicity from the transient run agreed with the steady-state values to within **~3–5%**, supporting the use of steady-state modelling across the studied range; genuinely unsteady, pulsatile operation is left to future work.

**Flow mechanisms (evidence from the contours).** The rectification mechanisms are supported directly by the velocity- and pressure-contour evidence in Figures 2 and 3. In reverse flow through Geometry 1 (Fig. 2), the tight loop forces the stream to separate at the branch entry; the velocity contour shows a low-momentum recirculation core within the loop (local velocity falling to roughly 15–25% of the bulk value) and the pressure contour shows a corresponding low-pressure recirculation region flanked by stagnation/turning zones where static pressure recovers locally. These structures dissipate energy and produce the high reverse ΔP. In Geometry 2 (Fig. 3) the smoother, wider loop keeps the reverse stream more attached; the recirculation region is weaker and more diffuse, so the velocity deficit and the pressure loss are smaller. In forward flow (inlet/outlet swapped, same mesh), both geometries show attached, low-loss flow through the main channel with only minor branch penetration, which is why the forward pressure drop is much smaller than the reverse value at equal Re. The contrast in separation and recirculation intensity between Fig. 2 and Fig. 3 is the direct fluid-dynamic reason for the higher diodicity of Geometry 1.

---

## 5. Conclusions

The present 2D CFD study shows that Tesla-valve performance is strongly sensitive to geometry and Reynolds number. The following conclusions are drawn:

1. Geometry 2 (smooth-loop, R<sub>c</sub>/D<sub>h</sub> = 2.0, θ = 30°) is **preferred for low-forward-loss applications** under the performance criterion of Eq. (8): it gives the lowest forward pressure drop (~1100 Pa at Re ≈ 3000) with a moderate reverse pressure drop (~3200 Pa), yielding a diodicity of ~2.91. It is "optimal" only in the sense of this stated forward-efficiency criterion, not universally.

2. Geometry 1 (tight-loop, R<sub>c</sub>/D<sub>h</sub> = 1.25, θ = 45°) is **preferred for maximum rectification**, achieving the highest diodicity (~3.71 at Re ≈ 3000) through strong flow separation, intense recirculation and vortex formation that produce a high reverse pressure drop (~6500 Pa).

3. Diodicity increases monotonically with Reynolds number for both geometries, with the most pronounced gains in the transitional regime (Re > 1000), where inertial effects dominate the separation behaviour.

4. Curvature radius and branching angle are the most influential geometric parameters: tighter curvature promotes vortex formation and higher diodicity, while smoother curvature reduces forward-flow loss.

5. Effective Tesla-valve design is therefore a quantifiable trade-off between diodicity and forward-flow pressure loss: smooth, gradual turns minimise forward loss while tight, sharp loops maximise reverse-flow resistance.

The study provides quantitative guidance for the design of efficient unpowered flow rectifiers. Future work will extend the investigation to unsteady pulsating flow, compressible gas flow, and multiphase (liquid–vapour) scenarios that are increasingly relevant to thermal-management and microfluidic applications.

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
19. Purwidyantri, A., & Prabowo, B. A. (2023). Tesla valve microfluidics: The rise of forgotten technology. *Chemosensors*, 11(4).
20. Shakaib, M., ul Haq, M. E., & Hasani, S. M. F. (2025). Effect of Tesla valve geometry on unsteady flow behavior and pressure drop: a CFD study. *Memoria Investigaciones en Ingeniería*, (29), 54–73.
21. Han, J., Shi, Y., Zhang, B., & Li, W. (2026). Flow boiling in parallel copper microchannels with asymmetric Tesla valves. *Applied Thermal Engineering*, 130972.
22. Li, W., Yang, S., Chen, Y., Li, C., & Wang, Z. (2023). Tesla valves and capillary structures-activated thermal regulator. *Nature Communications*, 14, 5922.
23. Qin, Z., & Wang, B. (2025). Design and diodicity enhancement mechanism of a double-baffle Tesla valve. *International Journal of Heat and Mass Transfer*, 239.
24. Jha, P., Das, B., Gupta, R., Mondol, J. D., & Ehyaei, M. A. (2023). Review of recent research on photovoltaic thermal solar collectors. *Solar Energy*, 257, 164–195.
25. Jha, P., Das, B., Gupta, R., & Kumar, N. (2025). An experimental analysis of photovoltaic thermal collector with trapezoidal and plain plates: an energy, exergy, and life cycle assessment. *Applied Thermal Engineering*, 274, 126769.
26. Shahsavar, A., Jha, P., & Askari, I. B. (2022). Experimental study of a nanofluid-based photovoltaic/thermal collector equipped with a grooved helical microchannel heat sink. *Applied Thermal Engineering*, 217, 119281.
27. Bardell, R. L. (2000). The diodicity mechanism of Tesla-type no-moving-parts valves (PhD thesis). University of Washington, Seattle, WA, USA.
28. Truong, T. Q., & Nguyen, N. T. (2004). Micromachined silicon Tesla valves. *Sensors and Actuators A: Physical*, 110(1–3), 126–132.
29. Liu, P., Yu, K., Tu, W., Ji, J., Wang, S., & Zang, L. (2026). Numerical investigation of mixing enhancement in a tesla-valve micromixer with strategically placed cylindrical obstacles. *Flow Measurement and Instrumentation*, 103375.
30. de Vries, S. F., Florea, D., Homburg, F. G. A., & Frijns, A. J. H. (2017). Design and operation of a Tesla-type valve for pulsating heat pipes. *International Journal of Heat and Mass Transfer*, 105, 1–11.
31. Thompson, S. M., Ma, H. B., & Wilson, C. (2011). Investigation of a flat-plate oscillating heat pipe with Tesla-type check valves. *Experimental Thermal and Fluid Science*, 35(7), 1265–1273.
32. Yang, K. S., Wang, C. C., & Tsai, P. H. (2019). Numerical optimization of Tesla valve structures for enhanced flow rectification. *Applied Thermal Engineering*, 148, 963–972.
