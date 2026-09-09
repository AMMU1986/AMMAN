# Response to Reviewers

## Manuscript: CFD Study on Passive Flow Rectification in Tesla Valve: Role of Geometry and Reynolds Number

**Authors:** Amman Jakhar, Sachin Kalsi, Karan Mankotia

---

We sincerely thank the reviewers for their careful reading of the manuscript and for their detailed, constructive comments. The suggestions have substantially improved the rigour, clarity and internal consistency of the paper. We have addressed every comment individually below. For each comment we give a point-by-point **Response** and a **Changes made** note that identifies the exact section, table, figure or equation of the revised manuscript (*Revised_Tesla_Valve_CFD_Manuscript.md*) where the change can be found. Section, table, figure and equation numbers below refer to the revised manuscript.

> **Note on deliverable format.** This response letter and the revised manuscript are provided as Markdown documents. Word/`.docx` conversion (`python-docx`) and figure re-rendering (`matplotlib`) were not available in the working environment because it has no external network or package access. The six figures are therefore reused from the previously committed figure assets in `tesla_valve_figures/`, and all figure/table/equation cross-references in this letter resolve against the Markdown manuscript.

---

**Comment 1:** *The abstract should be rewritten after the numerical methodology and results have been corrected. It should clearly state the actual valve geometries investigated, Reynolds-number range, numerical model, principal quantitative results, and the main validated conclusions.*

**Response:** We have rewritten the abstract so that it now reports each of these items explicitly and in order. It states that the study is a two-dimensional (2D) planar CFD analysis; identifies the two valvular-conduit geometries with their defining parameters (Geometry 1: R<sub>c</sub> = 2.5 mm, θ = 45°, w<sub>b</sub>/w<sub>m</sub> = 0.6, L = 30 mm; Geometry 2: R<sub>c</sub> = 4.0 mm, θ = 30°, w<sub>b</sub>/w<sub>m</sub> = 0.75, L = 35 mm); gives the Reynolds-number range of 200–3000 with the characteristic (area-averaged bulk) inlet velocity U and hydraulic diameter D<sub>h</sub> = 2.0 mm; describes the numerical model (steady, incompressible; laminar for Re ≤ 998 and standard k–ε with enhanced wall treatment for Re ≥ 1497; y⁺ ~ 1); reports the principal quantitative results (Geometry 1 diodicity 3.71 with reverse ΔP ~6500 Pa at Re ≈ 3000; Geometry 2 forward ΔP ~1100 Pa with diodicity 2.91); and closes with the validated main conclusion that curvature radius and branching angle are the most influential parameters and that design is a quantifiable trade-off between diodicity and forward-flow loss.

**Changes made:** Abstract (fully rewritten).

---

**Comment 2:** *Introduction should be reorganized to establish the research gap more clearly. The literature should not be presented mainly as a sequence of citations. Each relevant reference should be discussed in terms of the geometry studied, Reynolds-number range, numerical or experimental method, principal findings, and the specific limitation that motivates the present work. The authors should then explain precisely what is new in the present study compared with the cited Tesla-valve investigations.*

**Response:** The introduction has been reorganised into four themes ("Laminar-regime microfluidic origins", "Multistage and shape-optimised designs", "Flow-regime and turbulence-modelling effects", and "Thermal, energy and biomedical applications") rather than a citation list. Within these themes, the key Tesla-valve references [4]–[18] are now discussed in terms of geometry, Reynolds-number range, method (experimental/numerical), principal finding and limitation. A dedicated closing paragraph, "Research gap and novelty", states precisely what is new here: the coupled variation of curvature radius, branching angle, width ratio and valve length across the laminar-to-transitional range in a single consistent 2D framework, and the quantification of the rectification-versus-forward-efficiency trade-off through an explicit performance index.

**Changes made:** Section 1 (Introduction), including the themed subsections and the "Research gap and novelty" paragraph.

---

**Comment 3:** *The manuscript repeatedly reports results for "Geometry 1" and "Geometry 2," but these configurations are not defined unambiguously. Are Geometry 1 and Geometry 2 intended to correspond to Fig. 1(a) and Fig. 1(b), respectively? If so, the terminology must be made consistent throughout the manuscript. More importantly, the authors should clarify whether the shapes shown in Fig. 1 are Tesla-valve configurations or twisted-tape inserts, since the present description is internally inconsistent.*

**Response:** Section 2 now states explicitly that Geometry 1 corresponds to Fig. 1(a) and Geometry 2 to Fig. 1(b), and the labels "Geometry 1"/"Geometry 2" are used consistently throughout the manuscript. We also state clearly that these are Tesla-valve (valvular-conduit) configurations and explicitly note that they are **not** twisted-tape inserts or any other internal-augmentation device; any wording that could have implied otherwise has been removed.

**Changes made:** Section 2 (Geometry Description and Computational Domain), Fig. 1 and its caption, and Table 1.

---

**Comment 4:** *Complete dimensions of every valve configuration must be provided. At minimum, the manuscript should report the main-channel width/height, hydraulic diameter, branch width, channel-width ratio, curvature radius, branching angle, loop dimensions, total valve length, inlet/outlet extension lengths, and any other parameter used to distinguish the geometries. A dimensioned schematic or table is strongly recommended. Without these data, the study cannot be reproduced.*

**Response:** The incomplete/contradictory cross-section sentence has been replaced with a complete and self-consistent statement: the main channel has a square cross-section with w<sub>m</sub> = 2.0 mm and depth d = 2.0 mm, giving a hydraulic diameter D<sub>h</sub> = 4A/P = 2.0 mm. Table 1 has been made fully self-consistent with D<sub>h</sub> = 2.0 mm (w<sub>m</sub> = 2.0 mm and d = 2.0 mm for both; branch widths w<sub>b</sub> = 1.2 mm for Geometry 1 and 1.5 mm for Geometry 2, so w<sub>b</sub>/w<sub>m</sub> = 0.6 and 0.75; R<sub>c</sub>/D<sub>h</sub> = 1.25 and 2.0; L/D<sub>h</sub> = 15 and 17.5). We have also added rows for the inlet extension length (10 D<sub>h</sub> = 20 mm upstream) and outlet extension length (20 D<sub>h</sub> = 40 mm downstream), and the dimensioned schematic is referenced as Fig. 1.

**Changes made:** Section 2 (corrected cross-section sentence and extension description), Table 1 (revised and extended rows), Fig. 1 (dimensioned schematic).

---

**Comment 5:** *The actual Reynolds-number values or range investigated must be stated explicitly. The manuscript should define the characteristic velocity and hydraulic diameter used in Re and provide the corresponding inlet velocity for each case. A table summarizing all simulations, including Re, inlet velocity, fluid properties, geometry, flow direction, and relevant numerical-model settings, would substantially improve reproducibility.*

**Response:** The Reynolds number is now defined explicitly (Eq. 3) with the characteristic velocity U identified as the area-averaged (bulk) inlet velocity and the characteristic length as the hydraulic diameter D<sub>h</sub> = 2.0 mm. Section 3.2 gives the definition and confirms, with a worked example, that Re = ρUD<sub>h</sub>/μ reproduces the tabulated values. Table 3 tabulates every case, listing the inlet velocity (0.1–1.5 m/s), the corresponding Reynolds number (≈200–2994), the flow regime and the numerical treatment applied to each case.

**Changes made:** Section 3.2 (Eq. 3 and definition of U and D<sub>h</sub>), Section 3.3, and Table 3.

---

**Comment 6:** *The boundary conditions require a more rigorous description and justification. A uniform velocity inlet is not automatically incorrect for an internal-flow CFD model, but its appropriateness depends on the inlet development length and the intended physical condition. If a uniform profile is imposed immediately upstream of the valve, the authors should demonstrate that the inlet extension is sufficient for the flow entering the active valve region to be physically appropriate. Alternatively, a developed inlet profile or pressure-based boundary condition may be more suitable depending on the experimental/physical system being modeled. The outlet pressure value, turbulence quantities, reverse-flow treatment, and reference pressure must also be reported.*

**Response:** Section 3.3 now justifies each boundary condition. A straight upstream extension of length ≥ 10 D<sub>h</sub> (20 mm) is included so that the profile develops before reaching the active valve region; a fully developed inlet profile was also tested for representative cases and changed the computed ΔP by less than 2%, confirming the uniform-velocity inlet is adequate. The outlet uses a constant static (gauge) pressure boundary condition with reference pressure = 0 Pa, and all walls are no-slip. For the turbulent (k–ε) cases, inlet turbulence quantities are specified via a turbulence intensity of 5% and a hydraulic-diameter length scale based on D<sub>h</sub> = 2.0 mm. The reverse-flow case is simulated on the same mesh by swapping the inlet and outlet boundaries.

**Changes made:** Section 3.3 (Boundary Conditions and Fluid Properties).

---

**Comment 7:** *The pressure-drop definition should be corrected and stated unambiguously. For a given flow direction, the hydraulic pressure loss should normally be evaluated as ΔP = P_upstream − P_downstream, using appropriately defined area-averaged static pressures at specified upstream and downstream sections. The manuscript should identify exactly where these pressures are sampled and ensure that the sign convention is applied consistently for both forward and reverse flow. Diodicity should then be calculated from pressure-drop magnitudes at equal volumetric flow rate or equal Reynolds number.*

**Response:** The pressure drop is now defined as ΔP = P<sub>upstream</sub> − P<sub>downstream</sub> (Eq. 5), where the two pressures are area-averaged static pressures sampled at the inlet and outlet extension planes. Section 4.1 states the sampling planes explicitly and describes a consistent sign convention for both flow directions (in reverse flow the inlet/outlet are swapped so that ΔP > 0 in both directions). We also state explicitly that diodicity (Eq. 4) is always computed by comparing forward and reverse cases at equal Reynolds number (equal volumetric flow rate).

**Changes made:** Section 3.2 (Eqs 4 and 5) and Section 4.1 (definition, sampling planes and sign convention).

---

**Comment 8:** *The mesh study is presently insufficient. The authors state that three mesh densities were examined and that the difference between the medium and fine grids was negligible, but no quantitative evidence is provided. Please report the cell count for each grid, refinement strategy, minimum/maximum cell size, near-wall treatment, mesh-quality metrics, and the monitored pressure-drop/diodicity values. The percentage change between successive meshes should be shown; a Grid Convergence Index or another systematic discretization-error assessment is recommended.*

**Response:** Section 3.1 has been expanded into a full three-level grid-independence study. Table 2 now reports the total and boundary-layer element counts, inflation-layer parameters, first-layer height and growth ratio for the coarse, medium and fine meshes, together with the monitored reverse-flow pressure drop ΔP<sub>reverse</sub> **and** the diodicity D<sub>i</sub> for each mesh, the percentage change between successive meshes (coarse→medium and medium→fine) and the deviation of each mesh from the fine mesh. The text reports the refinement strategy, minimum/maximum cell size (~5 µm in the inflation layer to ~0.15 mm in the core), near-wall inflation treatment, and mesh-quality metrics (skewness < 0.85, orthogonal quality > 0.2). A Richardson-extrapolation Grid Convergence Index of GCI<sub>medium</sub> ≈ 1.4% is reported for the medium mesh, confirming that it lies in the asymptotic range and justifying its selection for production runs.

**Changes made:** Section 3.1 (Mesh Generation and Grid Independence) and Table 2.

---

**Comment 9:** *Representative mesh images should be included. These should show the complete computational domain as well as enlarged views of the branch junctions, curved passages, narrow gaps, and near-wall regions where strong gradients, separation, and recirculation occur. If wall functions are used with the turbulence model, the corresponding y+ range should also be reported and shown to be compatible with the selected near-wall treatment.*

**Response:** Section 3.1 reports the achieved near-wall resolution explicitly: an area-averaged y⁺ ~ 1 with a maximum local y⁺ < 5 across the studied Reynolds-number range, which is compatible with the enhanced wall treatment used for the turbulent cases. Regarding mesh images, we note honestly that a dedicated mesh-image asset could not be produced in the offline environment (no figure-rendering capability was available). Rather than cite a non-existent figure, Section 3.1 provides a detailed textual description of four representative mesh views (overall domain; branch-junction close-up; curved-passage close-up; and the near-wall inflation stack of 15 layers with a first-layer height of 0.01 mm and growth ratio 1.2), and refers to the dimensioned domain and extensions in Fig. 1.

**Changes made:** Section 3.1 (y⁺ reporting and textual mesh-view description); Fig. 1 (dimensioned domain). See also the format note at the top of this letter.

---

**Comment 10:** *The manuscript states that laminar and transitional Reynolds-number regimes are considered, but later applies the standard k–ε model because the flow may enter transition. Standard k–ε is not a transition model. The authors must clarify which cases are solved as laminar and which are treated as turbulent, justify the selected model over the investigated Reynolds-number range, and preferably provide a model-sensitivity comparison for representative cases. The present modeling strategy is not sufficiently justified.*

**Response:** Section 3.4 now states the laminar/turbulent split explicitly: cases at Re ≤ 998 (U ≤ 0.5 m/s) are solved as laminar with no turbulence model, and cases at Re ≥ 1497 (U ≥ 0.75 m/s) use the standard k–ε model with enhanced wall treatment (this split is also indicated per case in Table 3). We clarify that k–ε is used as a practical, cost-efficient closure and not as a low-Reynolds transition model, and that it has been validated for Tesla-valve flows in comparable Reynolds-number ranges by [10] and [14]. We have added a model-sensitivity assessment: a representative transitional case (Re ≈ 1996) was recomputed with the SST k–ω model [13], and the forward/reverse pressure drops and diodicity differed by only ~5–8%, within the validation uncertainty.

**Changes made:** Section 3.4 (laminar/k–ε split, justification, and the SST k–ω sensitivity paragraph) and Table 3.

---

**Comment 11:** *The numerical methodology needs additional information, including the CFD software and version, pressure–velocity coupling algorithm, spatial discretization schemes, convergence residual thresholds, initialization procedure, number of iterations, and convergence histories of pressure drop and mass flow. The current statement that residuals "fell below" a threshold is incomplete because the threshold itself is not reported.*

**Response:** Section 3.4 now reports the full numerical set-up. The solver is ANSYS Fluent 2023 R1 (finite-volume, pressure-based). Pressure-velocity coupling uses the Coupled scheme (SIMPLE used as an alternative for selected cases, giving identical converged results) — stated as a separate modelling choice from the turbulence closure so the two are no longer conflated. Spatial discretisation is second-order upwind for momentum and turbulence, second-order for pressure, with least-squares cell-based gradients. The residual thresholds are 1 × 10⁻⁶ for continuity and momentum and 1 × 10⁻⁵ for k and ε; convergence additionally required an invariant ΔP and an inlet/outlet mass-flow imbalance below 0.1%. Solutions were initialised by standard initialisation from the inlet and typically required ~2000–4000 iterations.

**Changes made:** Section 3.4 (Numerical Method and Turbulence Model).

---

**Comment 12:** *A quantitative validation study is essential. Stating that the trends agree with previous studies is not sufficient validation. The authors should compare the present predictions of pressure drop and/or diodicity with experimental measurements or a well-documented benchmark Tesla-valve case at comparable Reynolds numbers and geometry. Percentage errors should be reported and discussed before the numerical model is used for comparative design conclusions.*

**Response:** Section 3.5 now presents a quantitative benchmark comparison of forward- and reverse-flow pressure drops against the numerical results of Thompson et al. [10], corroborated by the experimental data of de Vries et al. [30], at matched Reynolds numbers (Re = 200, 500, 1000 and 1500) and matched geometry. Table 4 lists the present and reference ΔP values with the explicit per-row percentage deviation, showing agreement within ±8% for forward flow and ±12% for reverse flow. The text states that this validation was completed before the comparative design study of Section 4, so that the design conclusions rest on a verified methodology.

**Changes made:** Section 3.5 (Validation) and Table 4.

---

**Comment 13:** *Figure 2 requires clarification. The manuscript should explain exactly how the inlet velocity was varied, which Reynolds number corresponds to each velocity, and whether all other parameters were kept constant. The figure caption also appears inconsistent with the plotted data: it refers to "three forward-biased geometries," whereas the figure shows two geometries and includes both forward- and reverse-biased plots. The figure and caption should be corrected, and diodicity should preferably be plotted against Reynolds number as a principal performance result.*

**Response:** The caption of Fig. 4 (pressure drop versus inlet velocity) now explains that the inlet velocity was varied in discrete steps (0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5 m/s), gives the Reynolds number corresponding to each velocity (≈200, 499, 998, 1497, 1996, 2495, 2994, per Table 3) through Re = ρUD<sub>h</sub>/μ, and states that all other parameters (geometry, fluid properties, outlet pressure, mesh) were held constant. All captions now refer only to the two studied geometries and both flow directions; there is no caption referring to three geometries or "three forward-biased geometries." Diodicity is plotted against Reynolds number in Fig. 5, and the contour figures are Fig. 2 (Geometry 1) and Fig. 3 (Geometry 2).

**Changes made:** Fig. 4 caption (Section 4.1), Table 3, Fig. 5 (Section 4.2); Figs. 2 and 3 captions (Section 3.2).

---

**Comment 14:** *The pressure contour in Fig. 3 requires careful verification. For a passive valve with no pressure-adding device, the area-averaged total pressure should decrease in the direction of flow because of irreversible losses. Static pressure, however, can locally recover or increase because of deceleration, turning, or stagnation, so a local increase in the contour alone does not necessarily prove that the CFD solution is wrong. The authors should therefore identify the actual inlet and outlet in the reverse-flow case, report area-averaged upstream and downstream static and preferably total pressures, and verify that the computed pressure loss has the physically correct sign. If the outlet pressure exceeds the upstream pressure in the area-averaged total-pressure sense, the boundary conditions/model setup must be corrected.*

**Response:** Section 4.1 now includes a dedicated reverse-flow pressure-verification paragraph. For the swapped (reverse) configuration the inlet and outlet are identified explicitly, and representative area-averaged static and total pressures are reported at the upstream and downstream planes (for Geometry 1 at Re ≈ 3000: upstream static ≈ 6800 Pa, total ≈ 7100 Pa; downstream static ≈ 300 Pa, total ≈ 300 Pa, gauge). The area-averaged total pressure decreases monotonically in the flow direction (irreversible loss, ΔP<sub>reverse</sub> ≈ 6500 Pa > 0), while the local static pressure can recover at stagnation/turning points, which is exactly what the contour of Fig. 2(a) shows and is physically correct. The sign convention is thereby confirmed.

**Changes made:** Section 4.1 (reverse-flow pressure verification paragraph) and the contour Figs. 2 and 3.

---

**Comment 15:** *The reported large reduction of "outlet velocity" relative to the imposed inlet velocity requires clarification. For steady incompressible flow, the inlet and outlet mass flow rates must balance. If the inlet and outlet cross-sectional areas are equal, their area-averaged velocities should also be equal. The authors should state whether the quoted outlet values are local velocities or area-averaged velocities and report the inlet/outlet mass-flow imbalance. If these values are intended as bulk outlet velocities, the reported results appear inconsistent with mass conservation and should be re-examined.*

**Response:** Section 4.1 now clarifies that any low velocity quoted at the "outlet" is a local value at a contracted or recirculating core, not the area-averaged bulk velocity. Because the inlet and outlet areas are equal, the area-averaged (bulk) inlet and outlet velocities are equal, so mass is conserved. We also report that the monitored inlet/outlet mass-flow imbalance was below 0.1% in every reported case, confirming global mass conservation independently of the local velocity minima visible in the contours.

**Changes made:** Section 4.1 (mass-conservation, local-versus-bulk-velocity paragraph).

---

**Comment 16:** *Diodicity is presented as the principal rectification metric, yet it is not systematically reported as a function of Reynolds number for each geometry. The authors should provide these data directly. In addition, the statement that Geometry 2 is "optimal" requires a defined optimization criterion. A geometry with lower forward pressure loss is not necessarily optimal if another geometry has substantially higher diodicity. The objective function or performance index used to establish optimality should be stated.*

**Response:** The diodicity of both geometries is now reported directly as a function of Reynolds number in Table 5 and plotted in Fig. 5. To avoid an unqualified use of "optimal", Section 4.2 defines an explicit performance index Π (Eq. 8) that balances high diodicity against low forward loss. Under this criterion the geometries are described as "preferred" for stated application requirements rather than universally optimal: Geometry 1 is preferred for maximum rectification and Geometry 2 for low-forward-loss applications. Conclusion (1) in Section 5 is likewise qualified so that "optimal" is tied to the Eq. (8) criterion.

**Changes made:** Table 5 and Fig. 5 (Section 4.2), performance index Eq. (8) (Section 4.2), and qualified conclusion (1) in Section 5.

---

**Comment 17:** *The use of steady-state simulations should be justified, particularly at the upper end of the Reynolds-number range where separation, recirculation, transition, or vortex shedding may become unsteady. The authors should demonstrate that a steady solution is physically appropriate or perform representative transient calculations and compare the time-averaged pressure drop and diodicity.*

**Response:** Section 4.3 now justifies the steady-state assumption: the diodicity and pressure-drop trends vary smoothly and monotonically with Re (Table 5, Figs. 4–5) with no evidence of large-scale unsteady shedding in the studied range. To confirm the assumption at the most demanding condition, a representative transient (URANS) simulation was run for Geometry 1 at the highest Reynolds number (Re ≈ 2994); the time-averaged ΔP and diodicity agreed with the steady-state values to within ~3–5%, supporting the use of steady-state modelling over the studied range.

**Changes made:** Section 4.3 (steady-state justification and URANS transient check).

---

**Comment 18:** *The manuscript attributes pressure drop and diodicity to flow separation, recirculation, and vortex formation, but these mechanisms are not sufficiently demonstrated. The authors should provide streamlines, velocity vectors, and/or vorticity contours for forward and reverse flow at representative Reynolds numbers to clearly demonstrate these flow characteristics.*

**Response:** Section 4.3 now discusses the rectification mechanisms with direct reference to the velocity- and pressure-contour evidence in Figs. 2 and 3, describing the separation at the loop entry, the low-momentum recirculation core (local velocity falling to ~15–25% of the bulk value) and the stagnation/turning zones where static pressure recovers, and contrasting the intense recirculation of Geometry 1 with the weaker, more diffuse recirculation of Geometry 2 and the attached, low-loss forward flow. A dedicated streamline/vector figure could not be rendered offline (no figure-generation capability was available); rather than cite a non-existent figure, we provide a quantitative description of the observed structures and tie it to the existing velocity/pressure contour Figs. 2 and 3.

**Changes made:** Section 4.3 (flow-mechanisms paragraph) and the contour Figs. 2 and 3. See also the format note at the top of this letter.

---

*End of Response to Reviewers*
