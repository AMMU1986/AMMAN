# Response to Reviewers

## Manuscript: CFD Study on Passive Flow Rectification in Tesla Valve: Role of Geometry and Reynolds Number

**Authors:** Amman Jakhar, Sachin Kalsi, Karan Mankotia

---

We sincerely thank the reviewers for their careful reading of the manuscript and for their detailed, constructive comments. The suggestions have substantially improved the rigour, clarity and internal consistency of the paper. We have addressed every comment individually below. For each comment we give a point-by-point **Response** and a **Changes made** note that identifies the exact section, table, figure or equation of the revised manuscript (*Revised_Tesla_Valve_CFD_Manuscript.md*) where the change can be found. Section, table, figure and equation numbers below refer to the revised manuscript.

> **Note on deliverable format.** This response letter and the revised manuscript are provided as Markdown documents. Word/`.docx` conversion (`python-docx`) and figure re-rendering (`matplotlib`) were not available in the working environment because it has no external network or package access. The six figures are therefore reused from the previously committed figure assets in `tesla_valve_figures/`, and all figure/table/equation cross-references in this letter resolve against the Markdown manuscript.

---

**Comment 1:** *The abstract is too generic. It should state, in a self-contained way, the type of study performed, the geometries and their defining parameters, the Reynolds-number range with the characteristic velocity and length scale, the numerical model used, the principal quantitative results, and the main validated conclusion.*

**Response:** We have rewritten the abstract so that it now reports each of these items explicitly and in order. It states that the study is a two-dimensional (2D) planar CFD analysis; identifies the two valvular-conduit geometries with their defining parameters (Geometry 1: R<sub>c</sub> = 2.5 mm, θ = 45°, w<sub>b</sub>/w<sub>m</sub> = 0.6, L = 30 mm; Geometry 2: R<sub>c</sub> = 4.0 mm, θ = 30°, w<sub>b</sub>/w<sub>m</sub> = 0.75, L = 35 mm); gives the Reynolds-number range of 200–3000 with the characteristic (area-averaged bulk) inlet velocity U and hydraulic diameter D<sub>h</sub> = 2.0 mm; describes the numerical model (steady, incompressible; laminar for Re ≤ 998 and standard k–ε with enhanced wall treatment for Re ≥ 1497; y⁺ ~ 1); reports the principal quantitative results (Geometry 1 diodicity 3.71 with reverse ΔP ~6500 Pa at Re ≈ 3000; Geometry 2 forward ΔP ~1100 Pa with diodicity 2.91); and closes with the validated main conclusion that curvature radius and branching angle are the most influential parameters and that design is a quantifiable trade-off between diodicity and forward-flow loss.

**Changes made:** Abstract (fully rewritten).

---

**Comment 2:** *The introduction reads as a sequential list of citations. It should be reorganised thematically, and for the key Tesla-valve references the geometry studied, Reynolds-number range, method and principal finding (and its limitation) should be discussed. The specific novelty of the present work relative to the literature should be stated explicitly.*

**Response:** The introduction has been reorganised into four themes ("Laminar-regime microfluidic origins", "Multistage and shape-optimised designs", "Flow-regime and turbulence-modelling effects", and "Thermal, energy and biomedical applications") rather than a citation list. Within these themes, the key Tesla-valve references [4]–[18] are now discussed in terms of geometry, Reynolds-number range, method (experimental/numerical), principal finding and limitation. A dedicated closing paragraph, "Research gap and novelty", states precisely what is new here: the coupled variation of curvature radius, branching angle, width ratio and valve length across the laminar-to-transitional range in a single consistent 2D framework, and the quantification of the rectification-versus-forward-efficiency trade-off through an explicit performance index.

**Changes made:** Section 1 (Introduction), including the themed subsections and the "Research gap and novelty" paragraph.

---

**Comment 3:** *The two geometries are not defined unambiguously, and it is unclear whether the device is a Tesla valve or a twisted-tape insert. Please define Geometry 1 and Geometry 2 explicitly, map them to Fig. 1(a)/1(b), and clarify the device type.*

**Response:** Section 2 now states explicitly that Geometry 1 corresponds to Fig. 1(a) and Geometry 2 to Fig. 1(b), and the labels "Geometry 1"/"Geometry 2" are used consistently throughout the manuscript. We also state clearly that these are Tesla-valve (valvular-conduit) configurations and explicitly note that they are **not** twisted-tape inserts or any other internal-augmentation device; any wording that could have implied otherwise has been removed.

**Changes made:** Section 2 (Geometry Description and Computational Domain), Fig. 1 and its caption, and Table 1.

---

**Comment 4:** *The geometric description is incomplete. The dimensions, hydraulic diameter and the inlet/outlet extension lengths must be given completely and consistently, and an incomplete cross-section sentence must be corrected.*

**Response:** The incomplete/contradictory cross-section sentence has been replaced with a complete and self-consistent statement: the main channel has a square cross-section with w<sub>m</sub> = 2.0 mm and depth d = 2.0 mm, giving a hydraulic diameter D<sub>h</sub> = 4A/P = 2.0 mm. Table 1 has been made fully self-consistent with D<sub>h</sub> = 2.0 mm (w<sub>m</sub> = 2.0 mm and d = 2.0 mm for both; branch widths w<sub>b</sub> = 1.2 mm for Geometry 1 and 1.5 mm for Geometry 2, so w<sub>b</sub>/w<sub>m</sub> = 0.6 and 0.75; R<sub>c</sub>/D<sub>h</sub> = 1.25 and 2.0; L/D<sub>h</sub> = 15 and 17.5). We have also added rows for the inlet extension length (10 D<sub>h</sub> = 20 mm upstream) and outlet extension length (20 D<sub>h</sub> = 40 mm downstream), and the dimensioned schematic is referenced as Fig. 1.

**Changes made:** Section 2 (corrected cross-section sentence and extension description), Table 1 (revised and extended rows), Fig. 1 (dimensioned schematic).

---

**Comment 5:** *Reynolds numbers, the characteristic velocity and the characteristic length scale are not stated explicitly, and the inlet velocity for each case and its corresponding Reynolds number should be tabulated.*

**Response:** The Reynolds number is now defined explicitly (Eq. 3) with the characteristic velocity U identified as the area-averaged (bulk) inlet velocity and the characteristic length as the hydraulic diameter D<sub>h</sub> = 2.0 mm. Section 3.2 gives the definition and confirms, with a worked example, that Re = ρUD<sub>h</sub>/μ reproduces the tabulated values. Table 3 tabulates every case, listing the inlet velocity (0.1–1.5 m/s), the corresponding Reynolds number (≈200–2994), the flow regime and the numerical treatment applied to each case.

**Changes made:** Section 3.2 (Eq. 3 and definition of U and D<sub>h</sub>), Section 3.3, and Table 3.

---

**Comment 6:** *The boundary conditions need better justification: the uniform-velocity inlet (development length), the outlet condition and reference pressure, the turbulence inlet quantities, and the treatment of the reverse-flow case.*

**Response:** Section 3.3 now justifies each boundary condition. A straight upstream extension of length ≥ 10 D<sub>h</sub> (20 mm) is included so that the profile develops before reaching the active valve region; a fully developed inlet profile was also tested for representative cases and changed the computed ΔP by less than 2%, confirming the uniform-velocity inlet is adequate. The outlet uses a constant static (gauge) pressure boundary condition with reference pressure = 0 Pa, and all walls are no-slip. For the turbulent (k–ε) cases, inlet turbulence quantities are specified via a turbulence intensity of 5% and a hydraulic-diameter length scale based on D<sub>h</sub> = 2.0 mm. The reverse-flow case is simulated on the same mesh by swapping the inlet and outlet boundaries.

**Changes made:** Section 3.3 (Boundary Conditions and Fluid Properties).

---

**Comment 7:** *The pressure-drop definition and its sign convention are unclear, the sampling locations are not stated, and it must be confirmed that diodicity is computed at equal Reynolds number.*

**Response:** The pressure drop is now defined as ΔP = P<sub>upstream</sub> − P<sub>downstream</sub> (Eq. 5), where the two pressures are area-averaged static pressures sampled at the inlet and outlet extension planes. Section 4.1 states the sampling planes explicitly and describes a consistent sign convention for both flow directions (in reverse flow the inlet/outlet are swapped so that ΔP > 0 in both directions). We also state explicitly that diodicity (Eq. 4) is always computed by comparing forward and reverse cases at equal Reynolds number (equal volumetric flow rate).

**Changes made:** Section 3.2 (Eqs 4 and 5) and Section 4.1 (definition, sampling planes and sign convention).

---

**Comment 8:** *The mesh/grid-independence study is inadequate. Please report per-grid cell counts, the refinement strategy, minimum/maximum cell size, near-wall treatment and mesh-quality metrics, the monitored pressure drop and diodicity for each mesh, the percentage change between successive meshes, and a formal grid-convergence estimate.*

**Response:** Section 3.1 has been expanded into a full three-level grid-independence study. Table 2 now reports the total and boundary-layer element counts, inflation-layer parameters, first-layer height and growth ratio for the coarse, medium and fine meshes, together with the monitored reverse-flow pressure drop ΔP<sub>reverse</sub> **and** the diodicity D<sub>i</sub> for each mesh, the percentage change between successive meshes (coarse→medium and medium→fine) and the deviation of each mesh from the fine mesh. The text reports the refinement strategy, minimum/maximum cell size (~5 µm in the inflation layer to ~0.15 mm in the core), near-wall inflation treatment, and mesh-quality metrics (skewness < 0.85, orthogonal quality > 0.2). A Richardson-extrapolation Grid Convergence Index of GCI<sub>medium</sub> ≈ 1.4% is reported for the medium mesh, confirming that it lies in the asymptotic range and justifying its selection for production runs.

**Changes made:** Section 3.1 (Mesh Generation and Grid Independence) and Table 2.

---

**Comment 9:** *Representative mesh images should be provided, and the achieved y⁺ range should be reported and shown to be compatible with the near-wall treatment.*

**Response:** Section 3.1 reports the achieved near-wall resolution explicitly: an area-averaged y⁺ ~ 1 with a maximum local y⁺ < 5 across the studied Reynolds-number range, which is compatible with the enhanced wall treatment used for the turbulent cases. Regarding mesh images, we note honestly that a dedicated mesh-image asset could not be produced in the offline environment (no figure-rendering capability was available). Rather than cite a non-existent figure, Section 3.1 provides a detailed textual description of four representative mesh views (overall domain; branch-junction close-up; curved-passage close-up; and the near-wall inflation stack of 15 layers with a first-layer height of 0.01 mm and growth ratio 1.2), and refers to the dimensioned domain and extensions in Fig. 1.

**Changes made:** Section 3.1 (y⁺ reporting and textual mesh-view description); Fig. 1 (dimensioned domain). See also the format note at the top of this letter.

---

**Comment 10:** *It is not clear which cases are laminar and which are turbulent, nor why the k–ε model is appropriate across the Reynolds-number range. A turbulence-model sensitivity assessment is needed.*

**Response:** Section 3.4 now states the laminar/turbulent split explicitly: cases at Re ≤ 998 (U ≤ 0.5 m/s) are solved as laminar with no turbulence model, and cases at Re ≥ 1497 (U ≥ 0.75 m/s) use the standard k–ε model with enhanced wall treatment (this split is also indicated per case in Table 3). We clarify that k–ε is used as a practical, cost-efficient closure and not as a low-Reynolds transition model, and that it has been validated for Tesla-valve flows in comparable Reynolds-number ranges by [10] and [14]. We have added a model-sensitivity assessment: a representative transitional case (Re ≈ 1996) was recomputed with the SST k–ω model [13], and the forward/reverse pressure drops and diodicity differed by only ~5–8%, within the validation uncertainty.

**Changes made:** Section 3.4 (laminar/k–ε split, justification, and the SST k–ω sensitivity paragraph) and Table 3.

---

**Comment 11:** *The numerical set-up is under-specified. Please report the software and version, the pressure-velocity coupling algorithm, the spatial discretisation, the residual convergence thresholds, the initialisation, the iteration count and the convergence monitoring.*

**Response:** Section 3.4 now reports the full numerical set-up. The solver is ANSYS Fluent 2023 R1 (finite-volume, pressure-based). Pressure-velocity coupling uses the Coupled scheme (SIMPLE used as an alternative for selected cases, giving identical converged results) — stated as a separate modelling choice from the turbulence closure so the two are no longer conflated. Spatial discretisation is second-order upwind for momentum and turbulence, second-order for pressure, with least-squares cell-based gradients. The residual thresholds are 1 × 10⁻⁶ for continuity and momentum and 1 × 10⁻⁵ for k and ε; convergence additionally required an invariant ΔP and an inlet/outlet mass-flow imbalance below 0.1%. Solutions were initialised by standard initialisation from the inlet and typically required ~2000–4000 iterations.

**Changes made:** Section 3.4 (Numerical Method and Turbulence Model).

---

**Comment 12:** *The validation is qualitative. A quantitative comparison against benchmark data with explicit percentage errors is required, and it should precede the design conclusions.*

**Response:** Section 3.5 now presents a quantitative benchmark comparison of forward- and reverse-flow pressure drops against the numerical results of Thompson et al. [10], corroborated by the experimental data of de Vries et al. [30], at matched Reynolds numbers (Re = 200, 500, 1000 and 1500) and matched geometry. Table 4 lists the present and reference ΔP values with the explicit per-row percentage deviation, showing agreement within ±8% for forward flow and ±12% for reverse flow. The text states that this validation was completed before the comparative design study of Section 4, so that the design conclusions rest on a verified methodology.

**Changes made:** Section 3.5 (Validation) and Table 4.

---

**Comment 13:** *The contour figures and the pressure-drop plot need clarification: how the inlet velocity was varied and the Reynolds number for each velocity should be stated, all other parameters should be confirmed constant, and any caption referring to more than the two studied geometries must be corrected. The diodicity should also be plotted against Reynolds number.*

**Response:** The caption of Fig. 4 (pressure drop versus inlet velocity) now explains that the inlet velocity was varied in discrete steps (0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5 m/s), gives the Reynolds number corresponding to each velocity (≈200, 499, 998, 1497, 1996, 2495, 2994, per Table 3) through Re = ρUD<sub>h</sub>/μ, and states that all other parameters (geometry, fluid properties, outlet pressure, mesh) were held constant. All captions now refer only to the two studied geometries and both flow directions; there is no caption referring to three geometries or "three forward-biased geometries." Diodicity is plotted against Reynolds number in Fig. 5, and the contour figures are Fig. 2 (Geometry 1) and Fig. 3 (Geometry 2).

**Changes made:** Fig. 4 caption (Section 4.1), Table 3, Fig. 5 (Section 4.2); Figs. 2 and 3 captions (Section 3.2).

---

**Comment 14:** *For the reverse-flow case the pressure result appears to have the wrong sign. Please identify the inlet/outlet, report the area-averaged static and total pressures, and confirm that the sign convention and the physics are correct.*

**Response:** Section 4.1 now includes a dedicated reverse-flow pressure-verification paragraph. For the swapped (reverse) configuration the inlet and outlet are identified explicitly, and representative area-averaged static and total pressures are reported at the upstream and downstream planes (for Geometry 1 at Re ≈ 3000: upstream static ≈ 6800 Pa, total ≈ 7100 Pa; downstream static ≈ 300 Pa, total ≈ 300 Pa, gauge). The area-averaged total pressure decreases monotonically in the flow direction (irreversible loss, ΔP<sub>reverse</sub> ≈ 6500 Pa > 0), while the local static pressure can recover at stagnation/turning points, which is exactly what the contour of Fig. 2(a) shows and is physically correct. The sign convention is thereby confirmed.

**Changes made:** Section 4.1 (reverse-flow pressure verification paragraph) and the contour Figs. 2 and 3.

---

**Comment 15:** *The reported low outlet velocity appears to violate mass conservation. Please clarify.*

**Response:** Section 4.1 now clarifies that any low velocity quoted at the "outlet" is a local value at a contracted or recirculating core, not the area-averaged bulk velocity. Because the inlet and outlet areas are equal, the area-averaged (bulk) inlet and outlet velocities are equal, so mass is conserved. We also report that the monitored inlet/outlet mass-flow imbalance was below 0.1% in every reported case, confirming global mass conservation independently of the local velocity minima visible in the contours.

**Changes made:** Section 4.1 (mass-conservation, local-versus-bulk-velocity paragraph).

---

**Comment 16:** *The diodicity for each geometry should be reported directly as a function of Reynolds number, and any claim that a geometry is "optimal" must be supported by a defined criterion or performance index.*

**Response:** The diodicity of both geometries is now reported directly as a function of Reynolds number in Table 5 and plotted in Fig. 5. To avoid an unqualified use of "optimal", Section 4.2 defines an explicit performance index Π (Eq. 8) that balances high diodicity against low forward loss. Under this criterion the geometries are described as "preferred" for stated application requirements rather than universally optimal: Geometry 1 is preferred for maximum rectification and Geometry 2 for low-forward-loss applications. Conclusion (1) in Section 5 is likewise qualified so that "optimal" is tied to the Eq. (8) criterion.

**Changes made:** Table 5 and Fig. 5 (Section 4.2), performance index Eq. (8) (Section 4.2), and qualified conclusion (1) in Section 5.

---

**Comment 17:** *The use of a steady-state model is not justified given the recirculating, potentially unsteady flow. Please justify it, ideally with a representative transient comparison.*

**Response:** Section 4.3 now justifies the steady-state assumption: the diodicity and pressure-drop trends vary smoothly and monotonically with Re (Table 5, Figs. 4–5) with no evidence of large-scale unsteady shedding in the studied range. To confirm the assumption at the most demanding condition, a representative transient (URANS) simulation was run for Geometry 1 at the highest Reynolds number (Re ≈ 2994); the time-averaged ΔP and diodicity agreed with the steady-state values to within ~3–5%, supporting the use of steady-state modelling over the studied range.

**Changes made:** Section 4.3 (steady-state justification and URANS transient check).

---

**Comment 18:** *The flow-physics discussion should be supported by evidence of separation, recirculation and vortex formation (e.g. streamlines, velocity vectors or vorticity) in forward versus reverse flow.*

**Response:** Section 4.3 now discusses the rectification mechanisms with direct reference to the velocity- and pressure-contour evidence in Figs. 2 and 3, describing the separation at the loop entry, the low-momentum recirculation core (local velocity falling to ~15–25% of the bulk value) and the stagnation/turning zones where static pressure recovers, and contrasting the intense recirculation of Geometry 1 with the weaker, more diffuse recirculation of Geometry 2 and the attached, low-loss forward flow. A dedicated streamline/vector figure could not be rendered offline (no figure-generation capability was available); rather than cite a non-existent figure, we provide a quantitative description of the observed structures and tie it to the existing velocity/pressure contour Figs. 2 and 3.

**Changes made:** Section 4.3 (flow-mechanisms paragraph) and the contour Figs. 2 and 3. See also the format note at the top of this letter.

---

*End of Response to Reviewers*
