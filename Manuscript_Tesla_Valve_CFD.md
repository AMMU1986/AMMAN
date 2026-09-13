# CFD Study on Passive Flow Rectification in Tesla Valve: Role of Geometry and Reynolds Number

Amman Jakhar¹,* [0000-0001-6057-8953], Sachin Kalsi¹ [0000-0003-0139-7874] and Karan Mankotia¹ [0000-0002-0276-515X]

¹ Department of Mechanical Engineering, UIE, Chandigarh University, Mohali, Punjab 140413, India

*Corresponding author, E-mail: amman.e11994@cumail.in

## Abstract

Tesla valves do not require any moving parts to rectify the flow, so they are suitable for high-reliability applications like thermal-management systems, internal flow circuits in aerospace equipment and microfluidic circuits. In this work, a two-dimensional (2D) planar computational fluid dynamics (CFD) study is carried out to quantify the effect of the geometric parameters on the flow behaviour and rectification performance of Tesla valves for a range of Reynolds number from 200 to 3000. Two valvular-conduit geometries were systematically analysed: Geometry 1 (tight-loop: curvature radius Rc = 2.5 mm, branching angle θ = 45°, branch-to-main width ratio wb/wm = 0.6, valve length L = 30 mm); and Geometry 2 (smooth-loop: Rc = 4.0 mm, θ = 30°, wb/wm = 0.75, L = 35 mm). The characteristic velocity U is the area-averaged (bulk) inlet velocity and the hydraulic diameter is Dh = 2.0 mm, which corresponds to a square main channel of 2.0 mm × 2.0 mm. The steady, incompressible Navier–Stokes equations are solved numerically, with Re ≤ 998 (U ≤ 0.5 m/s) computed as laminar (no turbulence model) and Re ≥ 1497 (U ≥ 0.75 m/s) using the standard k–ε turbulence model with enhanced wall treatment, at a near-wall resolution of y⁺ ~ 1. Both geometries show monotonic increases in diodicity with Re, with the highest increases occurring for Re > 1000, the transitional regime. Geometry 1 attains a higher diodicity of 3.71, compared to Geometry 2 at 2.91 at the same Re, whereas Geometry 2 has a lower forward-flow pressure drop of ~1100 Pa. The validated main conclusions are: curvature radius and branching angle are the most influential geometric parameters, and there is a quantifiable trade-off between rectification strength (diodicity) and forward-flow efficiency in an effective Tesla-valve design. The results give quantitative design guidelines for passive flow rectifiers.

**Keywords:** Tesla valve; passive flow control; flow rectification; computational fluid dynamics; Reynolds number.

## 1. Introduction

Passive flow control has become an important enabling technology in fluid systems that demand reliability, simplicity and durability. Flow-rectification elements that are non-moving and do not require external actuation are becoming more and more common in applications including thermal-management circuits, internal aerospace flow paths and microfluidic diagnostic platforms. Mechanical valves struggle to meet the requirements of long service life, remote installation and harsh environments, and are prone to wear and fatigue, leakage, and maintenance [1]. These constraints have spurred continued investigation into passive rectification, where the fluid dynamics and geometry themselves offer resistance that differs by direction. The Tesla valve [2] is the prototype passive rectifier: a valvular conduit with an asymmetric flow path that provides a low-loss forward path and a high-loss reverse path, with curved side branches that promote separation, recirculation and vortex formation and thus higher energy dissipation [3]. Diodicity is the measure of directional performance and is defined as the ratio of the pressure drop in the reverse direction to the pressure drop in the forward direction at the same flow rate, without the use of a mechanical part.

**Laminar-regime microfluidic origins.** The initial studies were directed towards laminar flow, which is important in microfluidics. Fixed-valve micropumps were designed, fabricated and tested by Forster et al. [4], and in experiments they reported nearly linear growth of the diodicity with Reynolds number for Re < 300, and that the valve is a viable no-moving-parts rectifier with modest low-Re diodicity. Truong and Nguyen [5] obtained numerical simulation of the laminar flow, and developed geometric design rules for single-stage valves which explained the role of the branch angle and the gap, but were limited to the low-Re laminar regime. The few 3D treatments that were carried out, such as those of Zhang et al. [6] with 3D laminar simulations, have shown that a square cross-section is best for Re > 500, but remained in the laminar regime.

**Multi-stage and shape-optimised designs.** Subsequent work optimised valve shape and staging. Gamboa et al. [7] used shape optimisation and reported performance improvements as a function of the refinement of the valve geometry, with improvements scaling with the number of stages, but at the cost of increasing the forward loss; Mohammadzadeh et al. [8] quantified numerically the gain in diodicity as a function of the number of stages as the forward loss increases. Using numerical methods, Nobakht et al. [9] found that flow-separation intensity is the most important diodicity mechanism for Tesla-type microvalves, with their analysis limited to laminar flow, and Thompson et al. [10] studied multistaged valves and obtained correlations between staging and pressure drop that have been used as validation benchmarks.

**Effects of flow-regime and turbulence modelling.** The second theme is related to the effects of the flow regime and the accuracy of the turbulence closures. Jin et al. [11] conducted a parametric study of a reverse-flow valve for decompression of hydrogen and concluded on favourable diverging/converging angles. Nguyen et al. [12] showed experimentally that turbulence and pulsatile forcing have a positive effect on diodicity, which means that unsteady and transitional effects are not a nuisance. Thompson et al. [13] tested a Tesla valve with transitional and turbulent closures (k–kL–ω and SST k–ω) and found that the latter provided a better prediction, while Yontar et al. [14] investigated multistage valves in both laminar and turbulent methane flow and noted that the flow characteristics differed significantly between the two. These studies indicate that the choice of closure is most critical in the transition zone of interest in the present study, and serve as the basis for the model-sensitivity evaluation discussed in Section 3.4.

**Thermal, energy and biomedical applications.** The third theme is application-driven. The use of multistage valves for hydrogen decompression in fuel-cell systems [15] and the application of Tesla-type channels to lithium-ion battery cold plates for mixing and heat transfer [16, 17] are examples. Geometric refinement for microfluidic application, to achieve high diodicity, was done by Bohm et al. [18]. The design space is still expanding in emerging biomedical applications such as microfluidic diagnostics and wearable sensing [19–22]. These geometry-dependent phenomena are also applicable to other thermal-fluid devices, such as PVT collectors [24] where the geometry has a significant impact on the efficiency, geometric modification for energy and exergy performances [25], and grooved-microchannel configurations for heat-transfer behaviour [26]. Double-baffle refinements have also been demonstrated to increase the diodicity [23].

**Research gap and novelty.** Notwithstanding this body of work, there are two shortcomings. Most studies investigate only one geometric parameter in one flow regime, so the combined effect of the curvature radius, branching angle, width ratio and valve length throughout the laminar-to-transitional flow regime is not well quantified. Secondly, the relationship between rectification strength and forward-flow efficiency is often not quantitatively expressed as a performance criterion. The present study resolves both of these issues, by considering two designs for the Tesla valve in a consistent 2D CFD simulation framework, treating the laminar and transitional regimes, and quantifying the diodicity-versus-forward-loss trade-off via a well-defined performance index. The resulting correlations of geometry and rectification performance offer practical design recommendations for passive flow rectifiers, and a basis for future studies involving unsteady and multiphase flow.

## 2. Geometry Description and Computational Domain

The Tesla valves examined in this work are made up of a straight main channel with curved bypass branches attached at certain stations along its length; the bypass branches are not symmetrical. The arrangement of the main channel and bypass loops is asymmetric, causing the hydraulic resistance to be direction dependent and hence producing passive flow rectification. These are not twisted-tape inserts or any other internal augmentation device; they are Tesla-valve (valvular-conduit) configurations. The two geometries studied are shown schematically in Figure 1: Geometry 1 is Fig. 1(a) and Geometry 2 is Fig. 1(b). The two labels are used consistently throughout the manuscript.

The tight-loop configuration (Fig. 1a) features a small radius of curvature (Rc = 2.5 mm), branching angle (θ = 45°) and a branch-to-main width ratio (wb/wm = 0.6). The total length of the valve is L = 30 mm. Tight curvature helps to promote flow separation, vortex formation and recirculation in reverse flow. The hydraulic resistance is increased in the unfavourable direction with these structures, and thus the diodicity of the conduit is increased.

In the smooth-loop configuration (Fig. 1b), the bypass curvature is more gentle (Rc = 4.0 mm), the branching angle is smaller (θ = 30°), and the width ratio is larger (wb/wm = 0.75). The overall length of the valve is L = 35 mm. The more rounded, wider flowways prevent separation and viscous losses with forward flow, while still providing sufficient reverse-flow resistance from moderate recirculation. The configuration is therefore optimised to conduct forward flow efficiently and to prevent backflow.

The main channel has a square cross-section with wm = 2.0 mm and depth d = 2.0 mm, giving a hydraulic diameter Dh = 4A/P = 4(2.0 × 2.0)/(2(2.0 + 2.0)) = 2.0 mm. This is a 2D planar model, so Dh = 2.0 mm is taken as the equivalent hydraulic diameter for this square main channel and is used throughout the study. With wb/wm = 0.6 and 0.75, the branch widths are wb = 1.2 mm (Geometry 1) and wb = 1.5 mm (Geometry 2).

[Insert Figure 1 here]

Figure 1. Dimensioned schematic of the two valve geometries used in this study: (a) Geometry 1, tight-loop (Rc = 2.5 mm, θ = 45°) and (b) Geometry 2, smooth-loop (Rc = 4.0 mm, θ = 30°). The straight upstream and downstream extensions used to develop and recover the flow are indicated at the inlet and outlet.

Straight extensions upstream and downstream of the active valve region are included in the computational domain, to allow the flow to develop before and recover after the valve. Upstream, a straight inlet extension of 10 Dh = 20 mm is added, and downstream, a straight outlet extension of 20 Dh = 40 mm is added. The two combinations of valvular-conduit with their dimensionless groups are summarised in Table 1.

Table 1. Geometrical and dimensionless parameters of the investigated configurations.

| Parameter | Symbol | Geometry 1 | Geometry 2 | Units |
|---|---|---|---|---|
| Curvature radius | Rc | 2.5 | 4.0 | mm |
| Branching angle | θ | 45 | 30 | ° |
| Main channel width | wm | 2.0 | 2.0 | mm |
| Channel depth | d | 2.0 | 2.0 | mm |
| Branch channel width | wb | 1.2 | 1.5 | mm |
| Channel width ratio | wb/wm | 0.6 | 0.75 | – |
| Total valve length | L | 30 | 35 | mm |
| Inlet extension length | Lin | 20 (10 Dh) | 20 (10 Dh) | mm |
| Outlet extension length | Lout | 40 (20 Dh) | 40 (20 Dh) | mm |
| Hydraulic diameter | Dh | 2.0 | 2.0 | mm |
| Dimensionless curvature | Rc/Dh | 1.25 | 2.0 | – |
| Dimensionless length | L/Dh | 15 | 17.5 | – |

## 3. Governing Equations and Modelling

### 3.1 Mesh Generation and Grid Independence

The complex geometry of the bypass loops and branch junctions was resolved by using an unstructured computational domain. Local mesh refinement was employed near the curved passages and junctions where the maximum velocity gradients and recirculation zones are found; near-wall inflation layers were used to resolve the velocity gradients present at the no-slip boundary. The area-averaged y⁺ ~ 1 (maximum local y⁺ < 5) over the range of Reynolds numbers studied, with the near-wall inflation stack consisting of 15 layers, each of height 0.01 mm and growth ratio 1.2, allowing for the use of the enhanced wall treatment for the turbulent cases. The mesh skewness was kept under 0.85 and the orthogonal quality kept over 0.2 across the whole domain, with a minimum cell size of ~5 µm in the inflation layer and a maximum core cell size of ~0.15 mm.

A dedicated mesh image is not reproduced here, but several representative views of the mesh were examined during grid generation and are described for completeness: (i) the overall domain, with the coarser structured mesh in the straight extensions and the refined mesh in the valve region; (ii) a close-up of a branch junction, with a gradual refinement from the coarser structured mesh to the finer mesh in the bypass; (iii) a close-up of a curved passage, with a conformal mesh following the curvature of the passage; and (iv) a near-wall view, with the 15-layer inflation stack resolving the boundary layer. The dimensioned domain and extensions are shown in Fig. 1.

A three-level grid-independence study was carried out which tracked ΔP_reverse and diodicity Di. The mesh statistics, the difference between successive meshes and the difference between each mesh and the fine mesh are reported in Table 2. The pressure drop decreased by 4.9% between coarse and medium mesh and by 1.1% between medium and fine mesh; the diodicity decreased by 4.1% and 0.9% in the same steps. A Richardson-extrapolation Grid Convergence Index (GCI) is computed for the medium mesh (refinement ratio r ≈ 1.26, observed order p ≈ 2, safety factor Fs = 1.25) and is GCI_medium ≈ 1.4% for ΔP_reverse, which confirms that the medium mesh (512,000 elements) is in the asymptotic range. All production runs were thus performed on the medium mesh, which was best suited to balance accuracy and computational cost.

Table 2. Mesh statistics for the grid-independence study (Geometry 1, reverse flow, Re = 1500).

| Mesh Level | Total Elements | BL Elements | Inflation Layers | First Layer (mm) | Growth Ratio | ΔP_reverse (Pa) | Diodicity (Di) | Change vs Previous (%) | Deviation from Fine (%) |
|---|---|---|---|---|---|---|---|---|---|
| Coarse | 285,000 | 78,000 | 10 | 0.02 | 1.3 | 5,842 | 2.99 | – | 5.7 |
| Medium | 512,000 | 145,000 | 15 | 0.01 | 1.2 | 6,128 | 3.11 | 4.9 (ΔP), 4.1 (Di) | 1.1 |
| Fine | 1,024,000 | 310,000 | 20 | 0.005 | 1.15 | 6,195 | 3.14 | 1.1 (ΔP), 0.9 (Di) | Reference |

### 3.2 Governing Equations

The flow through the Tesla valve is simulated as two-dimensional (2D) planar, incompressible, Newtonian and single-phase. Since the Mach number is relatively small and the operating conditions are isothermal, compressibility and thermal effects are ignored. The governing equations are the continuity equation and the Navier–Stokes equations, which represent the conservation of mass and momentum.

For incompressible flow the continuity equation is:

∇·u = 0     (1)

The momentum-conservation equation is:

ρ(∂u/∂t + u·∇u) = −∇p + μ∇²u     (2)

where u is the velocity vector, p the static pressure, ρ the fluid density and μ the dynamic viscosity. The flow regime is characterised by the Reynolds number:

Re = ρUDh/μ     (3)

where U is the area-averaged (bulk) inlet velocity and Dh = 2.0 mm is the equivalent hydraulic diameter of the 2.0 mm square main channel (Section 2). For water (ρ = 998 kg/m³, μ = 0.001 Pa·s), Eq. (3) reproduces Table 3 exactly; for example, U = 0.5 m/s gives Re = 998 × 0.5 × 0.002 / 0.001 = 998.

Two derived performance parameters are used. Diodicity:

Di = ΔP_reverse / ΔP_forward     (4)

evaluated at equal Reynolds number (equal volumetric flow rate); and pressure drop:

ΔP = P_upstream − P_downstream     (5)

defined with a consistent sign convention (Section 4.1) so that ΔP > 0 for both flow directions.

[Insert Figure 2 here]

Figure 2. Geometry 1: (a) static-pressure contour and (b) velocity-magnitude contour at an inlet velocity of 0.5 m/s (Re ≈ 998) in the reverse-flow direction. The contours reveal separation at the loop entry and recirculation within the tight bypass.

[Insert Figure 3 here]

Figure 3. Geometry 2: (a) static-pressure contour and (b) velocity-magnitude contour at an inlet velocity of 0.5 m/s (Re ≈ 998) in the reverse-flow direction. The smoother loop produces weaker, more diffuse recirculation than Geometry 1.

### 3.3 Boundary Conditions and Fluid Properties

A uniform velocity-inlet boundary condition was applied at the domain inlet according to the target Reynolds number, with the value of U being the area-averaged (bulk) inlet velocity. Inlet velocities were varied from 0.1 m/s to 1.5 m/s, corresponding to Reynolds numbers of approximately 200 to 3000 for Dh = 2.0 mm and water properties. The velocity-to-Reynolds-number mapping is given in Table 3 and is unchanged from the base configuration because it is internally consistent with Dh = 2.0 mm.

Table 3. Correspondence between inlet velocity and Reynolds number (Dh = 2.0 mm, water).

| Inlet Velocity (m/s) | Reynolds Number | Flow Regime | Treatment |
|---|---|---|---|
| 0.1 | 200 | Laminar | Laminar (no turbulence model) |
| 0.25 | 499 | Laminar | Laminar (no turbulence model) |
| 0.5 | 998 | Laminar | Laminar (no turbulence model) |
| 0.75 | 1497 | Transitional | Standard k–ε, enhanced wall treatment |
| 1.0 | 1996 | Transitional | Standard k–ε, enhanced wall treatment |
| 1.25 | 2495 | Transitional | Standard k–ε, enhanced wall treatment |
| 1.5 | 2994 | Transitional | Standard k–ε, enhanced wall treatment |

The straight upstream extension of the uniform velocity inlet has length ≥ 10 Dh (20 mm) to allow the profile to develop prior to reaching the active inlet region. The uniform inlet with the upstream extension was also tested against a parabolic/turbulent inlet profile for representative cases, and the computed ΔP was within 2% of each other. The outlet was modelled with a constant static (gauge) pressure boundary condition and a reference pressure of 0 Pa. All solid walls were treated as no-slip. Turbulent (k–ε) cases were simulated with a turbulence intensity of 5% and a hydraulic-diameter length scale of Dh = 2.0 mm, with the inlet and outlet boundaries swapped to simulate forward and reverse flows on the same mesh. The working fluid was water (ρ = 998 kg/m³, μ = 0.001 Pa·s at room temperature), assumed to be Newtonian and incompressible, and the simulations were steady state.

### 3.4 Numerical Method and Turbulence Model

The finite-volume solver used for the simulations was ANSYS Fluent 2023 R1. The steady, incompressible mass- and momentum-conservation equations were solved with a pressure-based formulation. The Coupled scheme was used for pressure–velocity coupling (the SIMPLE scheme was used as an alternative in selected cases, and the converged results were the same). The momentum and turbulence transport equations were discretised by second-order upwind schemes, the pressure equation by a second-order scheme, and the cell-based least-squares gradient was used. The turbulence closure, which is described below, is a modelling decision independent of the pressure–velocity coupling.

Explicit residual thresholds and monitored physical quantities were used to assess convergence. The scaled residuals had to be less than 1 × 10⁻⁶ for the continuity and momentum equations, and 1 × 10⁻⁵ for the k and ε equations. Furthermore, the pressure drop ΔP across the valve and the mass-flow imbalance between inlet and outlet were monitored, and a solution was deemed converged only if ΔP did not change from iteration to iteration and the mass-flow imbalance was less than 0.1%. Solutions were typically initialised from the inlet conditions, and took ~2000–4000 iterations to converge.

**Laminar/turbulent treatment (per flow regime).** Treatment was selected by regime, not applied uniformly. The cases for Re ≤ 998 (U ≤ 0.5 m/s) are considered to be in the laminar regime and were solved without the use of a turbulence model. The cases with Re ≥ 1497 (U ≥ 0.75 m/s) are in the transitional regime and were solved using the standard k–ε turbulence model with enhanced wall treatment. The k–ε model solves two additional transport equations, one for k and one for ε:

Turbulent kinetic energy:

∂(ρk)/∂t + ∇·(ρku) = ∇·[(μ + μt/σk)∇k] + Gk − ρε     (6)

Dissipation rate:

∂(ρε)/∂t + ∇·(ρεu) = ∇·[(μ + μt/σε)∇ε] + C1ε(ε/k)Gk − C2ερ(ε²/k)     (7)

where k is the turbulent kinetic energy, ε the dissipation rate, Gk the production of turbulent kinetic energy and μt the turbulent viscosity.

**Justification and sensitivity of the model.** The standard k–ε model is used as a low-cost and practical closure for the transitional cases, not as a low-Reynolds transition model. It has been tested for Tesla-valve flows in similar Reynolds-number ranges by several researchers [10, 14], and the enhanced wall treatment resolves the viscous sublayer, where the near-wall mesh is sufficiently fine (y⁺ ~ 1) as in the present study. A model-sensitivity check was performed for a representative transitional case (Re ≈ 1996) by repeating the simulation using the SST k–ω model [13]; this is largely because the choice of closure model is most important in the transitional band. The differences in forward and reverse pressure drops, and consequently the diodicity, between the standard k–ε and SST k–ω predictions were found to be within the validation uncertainty, around 5–8%. The standard k–ε model was thus used throughout the full parametric sweep, and results from the SST k–ω model were presented as an upper-bound sensitivity.

### 3.5 Validation

The numerical methodology was validated by performing quantitative comparisons with the experimental results of de Vries et al. [30] and the numerical results of Thompson et al. [10] for a standard single-stage Tesla-valve geometry, for both forward and reverse flow pressure drops. The comparison was made at matched Reynolds numbers (Re = 200, 500, 1000 and 1500) and matched geometry. The present results are in good agreement with the reference data within ±8% for the forward-flow pressure drop and ±12% for the reverse-flow pressure drop as shown in Table 4, where the per-row deviations are indicated. This validation was done prior to the comparative design study in Section 4, so the conclusions in Section 4 are based on a validated methodology.

Table 4. Validation of the present CFD methodology against published data (reference ΔP values from Thompson et al. [10]; experimental corroboration from de Vries et al. [30]).

| Re | ΔP_forward, present (Pa) | ΔP_forward [10] (Pa) | Deviation (%) | ΔP_reverse, present (Pa) | ΔP_reverse [10] (Pa) | Deviation (%) |
|---|---|---|---|---|---|---|
| 200 | 42 | 45 | −6.7 | 68 | 72 | −5.6 |
| 500 | 185 | 198 | −6.6 | 410 | 445 | −7.9 |
| 1000 | 580 | 625 | −7.2 | 1,650 | 1,820 | −9.3 |
| 1500 | 1,080 | 1,150 | −6.1 | 3,450 | 3,890 | −11.3 |

All forward-flow deviations are within ±8% and all reverse-flow deviations are within ±12%, confirming that the methodology reproduces both the magnitude and the direction-dependence of the pressure drop.

## 4. Results and Discussion

### 4.1 Pressure Drop Characteristics

The pressure drop is defined as ΔP = P_upstream − P_downstream, where P_upstream and P_downstream are the area-averaged static pressures measured at the inlet and outlet extension planes, respectively. In forward flow, the upstream plane is the geometric inlet, whereas in reverse flow the inlet and outlet are reversed and the upstream plane is the geometric outlet. With this convention ΔP > 0 both ways. The forward and reverse cases are always compared at equal Reynolds number (equal volumetric flow rate), and diodicity (Eq. 4) is always computed accordingly.

The pressure-drop characteristics of both geometries are similar to previous studies of Tesla-type valves and passive rectifiers [26–28]. In both flow directions, there was a monotonic increase in the pressure drop with increasing inlet velocity for all configurations. Geometry 2 has the lowest loss in forward flow, increasing from ~60 Pa at 0.1 m/s (Re ~ 200) to ~1100 Pa at 1.5 m/s (Re ~ 3000), due to the smooth passages that prevent separation and viscous losses in the favourable direction [29, 30]. The forward losses were much higher, reaching ~1750 Pa at maximum velocity, in Geometry 1 due to its sharp direction changes and disturbances in its tight loop. The forward-flow advantage of Geometry 2 is evident in Figure 4, which plots the variation of pressure drop with inlet velocity. The most significant difference between the geometries is in reverse flow, where Geometry 1 reached ~6.5 kPa at 1.5 m/s (Re ≈ 3000), while Geometry 2 reached ~3.2 kPa at the same Re. The trends are similar to previous numerical and experimental studies [27, 28, 31, 32].

[Insert Figure 4 here]

Figure 4. Pressure drop versus inlet velocity for forward and reverse flow in both geometries. The inlet velocity was varied in discrete steps (0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5 m/s); each velocity corresponds to a fixed Reynolds number (Re ≈ 200, 499, 998, 1497, 1996, 2495, 2994 respectively, per Table 3) through Re = ρUDh/μ with Dh = 2.0 mm. All other parameters (geometry, fluid properties, outlet pressure, mesh) were held constant so that ΔP is a function of velocity (Re) and flow direction only.

**Reverse-flow pressure check (sign check).** The inlet and outlet were swapped to check the reverse-flow pressure behaviour, and the static and total pressures were measured at the inlet and outlet extension planes. The pressures measured in Geometry 1 at Re ≈ 3000 were: upstream static ≈ 6800 Pa and total ≈ 7100 Pa; downstream static ≈ 300 Pa and total ≈ 300 Pa (gauge, outlet reference = 0). The total pressure decreases monotonically in the flow direction, which is what we would expect if there is an irreversible loss ΔP_reverse ≈ 6500 Pa > 0. At stagnation and turning points in the loops, the static pressure may recover as it does in Fig. 2(a); this is physically correct (and the contour of Fig. 2(a) demonstrates it) and does not violate the second law, since the total pressure remains monotonically decreasing along the path. Hence the pressure-drop sign convention is verified for reverse flow.

**Conservation of mass (local vs. bulk velocity).** When a low velocity is observed at the "outlet", it is the velocity in the contracted/recirculating core, NOT the area-averaged bulk velocity. Since the inlet and outlet areas are the same, the inlet and outlet bulk (area-averaged) velocities are also the same, and thus mass is conserved. The inlet/outlet mass-flow imbalance observed in all reported cases was less than 0.1% and is consistent with global mass conservation, where there is no local velocity minimum associated with the contours.

### 4.2 Diodicity Performance

At the same Re, the diodicity Di = ΔP_reverse/ΔP_forward was calculated for the two geometries over the entire range of Reynolds numbers, and is summarised in Table 5 and plotted in Figure 5. The rectification capability of both geometries increases with Reynolds number, with Geometry 1 also being better than Geometry 2 at all Reynolds numbers.

Table 5. Diodicity values for both geometries at various Reynolds numbers.

| Reynolds Number (Re) | Inlet Velocity, U (m/s) | Geometry 1 (Di) | Geometry 2 (Di) |
|---|---|---|---|
| 200 | 0.1 | 1.45 | 1.32 |
| 499 | 0.25 | 1.92 | 1.58 |
| 998 | 0.5 | 2.65 | 2.05 |
| 1497 | 0.75 | 3.12 | 2.45 |
| 1996 | 1.0 | 3.45 | 2.72 |
| 2495 | 1.25 | 3.62 | 2.85 |
| 2994 | 1.5 | 3.71 | 2.91 |

Increasing Reynolds number increases the diodicity, which indicates an increasing importance of inertia in the enhancement of separation and vortex formation in the bypass loops in reverse flow. In the laminar regime (low Re), viscous forces predominate and the flow remains more or less attached even in the curved geometries, thus providing a moderate diodicity (1.3–1.5). In the transitional regime, the reverse-flow momentum interacts more strongly with the loop walls, creating more intense recirculation and more dissipation.

The increased diodicity of Geometry 1 results directly from its tighter curvature (Rc/Dh = 1.25) and larger branching angle (45°), which compel abrupt redirection and earlier separation. The smoother curvature of Geometry 2 (Rc/Dh = 2.0) smooths the flow through the bypass, but also reduces the forward-flow loss generated by separation.

[Insert Figure 5 here]

Figure 5. Diodicity versus Reynolds number for both valve geometries.

**Performance criterion (defining "optimal").** To avoid an unqualified use of "optimal", a performance index is defined that balances high rectification against low forward loss:

Π = Di / (ΔP_forward / ΔP_forward,ref)     (8)

where ΔP_forward,ref is a common reference forward loss (here the Geometry 2 forward loss at the same Re). A geometry is "preferred" under a stated application requirement rather than universally optimal: Geometry 1 is preferred for maximum rectification (highest Di, e.g. 3.71 at Re ≈ 3000) where reverse-flow blocking is paramount, whereas Geometry 2 is preferred for low-forward-loss applications (forward ΔP ≈ 1100 Pa at Re ≈ 3000, Di = 2.91) where pumping efficiency in the favourable direction is paramount. By the index Π, Geometry 2 scores higher whenever forward-loss economy is weighted heavily, while Geometry 1 scores higher when raw diodicity dominates the requirement.

### 4.3 Summary of Performance Comparison and Flow Mechanisms

In general, the forward-flow performance of Geometry 2 is more favourable, with a forward pressure drop of ~1100 Pa (Re ≈ 3000) and a lower reverse pressure drop of ~3200 Pa, while Geometry 1 is the stronger reverse-flow blocker, with a high reverse pressure drop of ~6500 Pa and a noticeable reduction in vorticity and velocity. These findings reinforce the critical importance of geometric design in obtaining efficient forward flow whilst ensuring that backflow is suppressed effectively with passive rectifiers. A comparison of the performances is displayed in Figure 6.

[Insert Figure 6 here]

Figure 6. Performance comparison showing forward and reverse pressure drops and diodicity for both geometries at Re ≈ 3000.

**Steady-state assumption and transient check.** The production runs were steady state, which is reasonable given that the trends of the diodicity and the pressure drop are smooth and monotonic with Re (Table 5, Figs. 4–5) without any sign of large-scale unsteady shedding within the investigated range. A representative transient (URANS) simulation was conducted for Geometry 1 at the highest Reynolds number (Re ≈ 2994) to confirm the assumption at the most challenging condition. Time-averaged ΔP and diodicity from the transient run agreed with the steady-state values to within ~3–5%, and therefore steady-state modelling was used over the range of operation studied, whereas truly unsteady pulsatile operation is reserved for future studies.

**Flow mechanisms (from contours).** The velocity- and pressure-contour evidence of Figures 2 and 3 directly supports the rectification mechanisms. The tight loop requires the stream to separate at the branch entry in reverse flow through Geometry 1 (Fig. 2), with a low-momentum recirculation core (local velocity at about 15–25% of the bulk value) as indicated in the velocity contour; the corresponding low-pressure recirculation region (between stagnation/turning zones where static pressure recovers locally) is indicated in the pressure contour. These structures act as a "friction loss" and create the high reverse ΔP. In Geometry 2 (Fig. 3) the smoother, wider loop allows for a more attached reverse stream, with a weaker, more diffuse recirculation region, which results in a smaller velocity deficit and pressure loss. Forward flow is attached and low-loss through the main channel with only minor penetration into the branches, hence the forward pressure drop is much lower than the reverse pressure drop at the same Re for both geometries (inlet/outlet swapped, same mesh). The separation and recirculation intensity difference between Fig. 2 and Fig. 3 is the direct cause of the higher diodicity of Geometry 1.

## 5. Conclusions

The present 2D CFD study indicates that the performance of the Tesla valve is highly dependent on geometry and Reynolds number. The following conclusions are made:

1. For low-forward-loss applications, the performance criterion of Eq. (8) suggests that Geometry 2 (smooth-loop, Rc/Dh = 2.0, θ = 30°) yields the lowest forward pressure drop (~1100 Pa at Re ≈ 3000) and a moderate reverse pressure drop (~3200 Pa), resulting in a diodicity of ~2.91. It is optimal from this declared forward-efficiency point of view, but not optimal in general.

2. The tight-loop geometry (Geometry 1, Rc/Dh = 1.25, θ = 45°) is suitable for maximum rectification because it generates the greatest reverse pressure drop (≈6500 Pa) due to strong flow separation, intense recirculation and vortex formation, which yields the highest diodicity (~3.71 at Re ≈ 3000).

3. For both geometries, diodicity monotonically increases with Reynolds number, with the largest improvement in the transitional regime (Re > 1000), where separation behaviour is dominated by inertial effects.

4. The most significant geometric parameters are curvature radius and branching angle: smaller curvature is more conducive to vortex generation and larger diodicity, while smoother curvature is more conducive to reducing forward-flow loss.

5. The design of a good Tesla valve is therefore a compromise between the diodicity and the pressure loss across the valve when it is conducting in the forward direction. Smooth and gradual turns are desirable to reduce the pressure loss in the forward direction, while tight turns are desirable to increase the pressure loss in the reverse direction.

The study offers quantitative design guidelines for the design of efficient unpowered flow rectifiers. The investigation will be continued to unsteady pulsating flow, compressible gas flow, and multiphase (liquid–vapour) flow scenarios, which are becoming increasingly relevant for thermal-management and microfluidic applications.

## References

[1] Park, H., & Kim, S. Y. (2026). Pressure drop characteristics of Tesla valve in fully turbulent flow. Journal of Fluids Engineering, 148(3).

[2] Tesla, N. (1920). Valvular conduit (U.S. Patent No. 1,329,559). U.S. Patent and Trademark Office.

[3] Han, Q., Liu, Z., Zhang, C., & Li, W. (2023). Enhance flow boiling in Tesla-type microchannels by inhibiting two-phase backflow. International Journal of Heat and Mass Transfer, 214.

[4] Forster, F. K., Bardell, R. L., Afromowitz, M. A., Sharma, N. R., & Blanchard, A. (1995). Design, fabrication and testing of fixed-valve micro-pumps. ASME International Mechanical Engineering Congress and Exposition.

[5] Truong, T. Q., & Nguyen, N. T. (2003). Simulation and optimization of Tesla valves. In Nanotechnology Conference and Trade Show (Nanotech 2003) (pp. 178–181).

[6] Zhang, S., Winoto, S. H., & Low, H. T. (2007). Performance simulations of Tesla microfluidic valves. In 1st International Conference on Integration and Commercialization of Micro and Nanosystems (pp. 15–19).

[7] Gamboa, A. R., Morris, C. J., & Forster, F. K. (2005). Improvements in fixed-valve micropump performance through shape optimization of valves. Journal of Fluids Engineering, 127(2), 339–346.

[8] Mohammadzadeh, K., Kolahdouz, E. M., Shirani, E., & Shafii, M. B. (2013). Numerical investigation on the effect of the size and number of stages on the Tesla microvalve efficiency. Journal of Mechanics, 29(3), 527–534.

[9] Nobakht, A. Y., Shahsavan, M., & Paykani, A. (2013). Numerical study of diodicity mechanism in different Tesla-type microvalves. Journal of Applied Research and Technology, 11(6), 876–885.

[10] Thompson, S. M., Paudel, B. J., Jamal, T., & Walters, D. K. (2014). Numerical investigation of multi-staged Tesla valves. Journal of Fluids Engineering, 136(8).

[11] Jin, Z. J., Gao, Z. X., Chen, M. R., & Qian, J. Y. (2018). Parametric study on Tesla valve with reverse flow for hydrogen decompression. International Journal of Hydrogen Energy, 43(18), 8888–8896.

[12] Nguyen, Q. M., Abouezzi, J., & Ristroph, L. (2021). Early turbulence and pulsatile flows enhance diodicity of Tesla's macrofluidic valve. Nature Communications, 12(1).

[13] Thompson, S. M., Jamal, T., Paudel, B. J., & Walters, D. K. (2013). Transitional and turbulent flow modeling in a Tesla valve. In ASME International Mechanical Engineering Congress and Exposition.

[14] Yontar, A. A., Sofuoğlu, D., Değirmenci, H., Bicer, M. S., & Ayaz, T. (2021). Investigation of flow characteristics for a multi-stage Tesla valve at laminar and turbulent flow conditions. Journal of Scientific Reports-A, (047), 47–67.

[15] Qian, J. Y., Wu, J. Y., Gao, Z. X., Wu, A. J., & Jin, Z. J. (2019). Hydrogen decompression analysis by multistage Tesla valves for hydrogen fuel cell. International Journal of Hydrogen Energy, 44(26), 13666–13674.

[16] Monika, K., Chakraborty, C., Roy, S., Sujith, R., & Datta, S. P. (2021). A numerical analysis on multi-stage Tesla valve based cold plate for cooling of pouch type Li-ion batteries. International Journal of Heat and Mass Transfer, 177.

[17] Lu, Y. B., Wang, J. F., Liu, F., Liu, Y. Q., Wang, F. Q., Yang, N., Lu, D. C., & Jia, Y. K. (2022). Performance optimization of Tesla valve-type channel for cooling lithium-ion batteries. Applied Thermal Engineering, 212.

[18] Bohm, S., Phi, H. B., Moriyama, A., Runge, E., Strehle, S., Konig, J., Cierpka, C., & Dittrich, L. (2022). Highly efficient passive Tesla valves for microfluidic applications. Microsystems and Nanoengineering, 8(1).

[19] Purwidyantri, A., & Prabowo, B. A. (2023). Tesla valve microfluidics: The rise of forgotten technology. Chemosensors, 11(4).

[20] Shakaib, M., ul Haq, M. E., & Hasani, S. M. F. (2025). Effect of Tesla valve geometry on unsteady flow behavior and pressure drop: a CFD study. Memoria Investigaciones en Ingeniería, (29), 54–73.

[21] Han, J., Shi, Y., Zhang, B., & Li, W. (2026). Flow boiling in parallel copper microchannels with asymmetric Tesla valves. Applied Thermal Engineering, 130972.

[22] Li, W., Yang, S., Chen, Y., Li, C., & Wang, Z. (2023). Tesla valves and capillary structures-activated thermal regulator. Nature Communications, 14, 5922.

[23] Qin, Z., & Wang, B. (2025). Design and diodicity enhancement mechanism of a double-baffle Tesla valve. International Journal of Heat and Mass Transfer, 239.

[24] Jha, P., Das, B., Gupta, R., Mondol, J. D., & Ehyaei, M. A. (2023). Review of recent research on photovoltaic thermal solar collectors. Solar Energy, 257, 164–195.

[25] Jha, P., Das, B., Gupta, R., & Kumar, N. (2025). An experimental analysis of photovoltaic thermal collector with trapezoidal and plain plates: an energy, exergy, and life cycle assessment. Applied Thermal Engineering, 274, 126769.

[26] Shahsavar, A., Jha, P., & Askari, I. B. (2022). Experimental study of a nanofluid-based photovoltaic/thermal collector equipped with a grooved helical microchannel heat sink. Applied Thermal Engineering, 217, 119281.

[27] Bardell, R. L. (2000). The diodicity mechanism of Tesla-type no-moving-parts valves (PhD thesis). University of Washington, Seattle, WA, USA.

[28] Truong, T. Q., & Nguyen, N. T. (2004). Micromachined silicon Tesla valves. Sensors and Actuators A: Physical, 110(1–3), 126–132.

[29] Liu, P., Yu, K., Tu, W., Ji, J., Wang, S., & Zang, L. (2026). Numerical investigation of mixing enhancement in a Tesla-valve micromixer with strategically placed cylindrical obstacles. Flow Measurement and Instrumentation, 103375.

[30] de Vries, S. F., Florea, D., Homburg, F. G. A., & Frijns, A. J. H. (2017). Design and operation of a Tesla-type valve for pulsating heat pipes. International Journal of Heat and Mass Transfer, 105, 1–11.

[31] Thompson, S. M., Ma, H. B., & Wilson, C. (2011). Investigation of a flat-plate oscillating heat pipe with Tesla-type check valves. Experimental Thermal and Fluid Science, 35(7), 1265–1273.

[32] Yang, K. S., Wang, C. C., & Tsai, P. H. (2019). Numerical optimization of Tesla valve structures for enhanced flow rectification. Applied Thermal Engineering, 148, 963–972.
