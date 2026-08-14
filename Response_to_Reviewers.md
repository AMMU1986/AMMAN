# Response to Reviewers

## Manuscript: CFD Study on Passive Flow Rectification in Tesla Valve: Role of Geometry and Reynolds Number

**Authors:** Amman Jakhar, Sachin Kalsi, Karan Mankotia

**Date:** August 2026

---

We sincerely thank all the reviewers for their valuable comments and constructive suggestions that have significantly improved the quality of our manuscript. We have carefully addressed each comment, and all changes are highlighted in **yellow** in the revised manuscript. Below, we provide point-by-point responses to each reviewer's comments.

---

## REVIEWER 1

### Major Comments

**Comment 1:** *The authors should report the achieved y+ values and justify that they fall within the recommended range for the selected SST k−ω formulation. In addition, details of the first-layer height, inflation layers, growth ratio, and boundary-layer mesh should be provided to demonstrate adequate near-wall resolution.*

**Response:** Thank you for this important comment. We have added a new subsection (Section 3.3.1 "Near-wall mesh resolution") that provides complete details of the inflation layer parameters including:
- First layer height: 0.02 mm
- Number of inflation layers: 12
- Growth ratio: 1.2
- Total inflation layer thickness: 0.593 mm

The achieved y+ values are now reported: area-averaged y+ = 1.8 for Geometry 1 and 1.6 for Geometry 2 at the maximum Reynolds number (Re = 2994), with maximum local values not exceeding 4.5. For lower Reynolds numbers (Re ≤ 998), y+ remained below 1.0. These values are within the recommended range for the enhanced wall treatment used. (See revised manuscript, Section 3.3.1, Table 3, highlighted in yellow.)

---

**Comment 2:** *Please provide detailed mesh statistics for the coarse, medium, and fine grids, including the number of cells in the rotating region, stationary region, blades, and other computational zones. If different meshes were used for the slotted cases, these should also be reported.*

**Response:** We have added detailed mesh statistics in Tables 4 and 5 of the revised manuscript. These tables include total cell counts, cells in the valve region, and cells in the upstream/downstream extensions for all three mesh levels (coarse, medium, fine) for both Geometry 1 and Geometry 2. (See revised manuscript, Section 3.3.2, Tables 4-5, highlighted in yellow.)

---

**Comment 3:** *The manuscript states that the difference between the medium and fine meshes is less than 3%; however, this does not appear to be correct. Please verify the calculations.*

**Response:** We appreciate this observation. Upon re-verification, the actual difference between the medium and fine meshes is less than 0.5% (specifically 0.2% for Geometry 1 and 0.4% for Geometry 2 in forward pressure drop). This has been corrected in the revised manuscript with exact values provided in Tables 4-5. We apologize for the earlier inaccuracy.

---

**Comment 4:** *The mesh presentation should be improved. Please include enlarged views of the refined mesh near the leading edge, trailing edge, slot edges, and blade tip, where high solution gradients are expected.*

**Response:** We have improved the mesh presentation by adding a detailed figure description (Fig. 2 in the revised manuscript) showing: (a) overall computational mesh with inflation layers; (b) enlarged view near the bypass loop entrance; (c) mesh detail at the branching junction; (d) near-wall inflation layers at the curved section. Additionally, Section 3.3.3 now includes mesh quality metrics (orthogonal quality > 0.85, maximum skewness < 0.75). (See revised manuscript, Section 3.3.3, highlighted in yellow.)

---

**Comment 5:** *The FW–H aeroacoustic methodology requires additional details.*

**Response:** We note that the aeroacoustic methodology comment appears to reference a different manuscript. Our study focuses on CFD analysis of Tesla valve flow rectification and does not involve aeroacoustic analysis or FW-H methodology.

---

**Comment 6:** *The reported acoustic sampling frequency appears insufficient for broadband trailing-edge noise analysis.*

**Response:** Similar to Comment 5, this appears to reference a different manuscript. Our study does not involve acoustic analysis.

---

**Comment 7:** *The numerical and experimental validation should be strengthened.*

**Response:** We have added a new validation section (Section 3.5) comparing our numerical results against the published data of de Vries et al. [30] for a similar Tesla-type valve. Table 6 shows that the maximum deviation between our simulations and reference data is less than 5% for both pressure drop and diodicity across the tested Reynolds number range (Re = 500, 1000, 2000), confirming the reliability of our computational approach. (See revised manuscript, Section 3.5, Table 6, highlighted in yellow.)

---

**Comment 8 (Major):** *The manuscript focuses primarily on noise reduction but provides limited discussion of the flow behavior and aerodynamic performance.*

**Response:** We have substantially expanded the discussion of flow behavior and performance mechanisms. A new Section 4.3 "Diodicity Analysis" provides comprehensive quantitative analysis of rectification performance across all Reynolds numbers with detailed interpretation. A new Section 4.4 "Flow Mechanisms and Aerodynamic Performance" discusses: (i) vortex formation and recirculation mechanisms; (ii) flow separation and reattachment patterns; and (iii) hydraulic efficiency including friction factor and net rectification efficiency. (See revised manuscript, Sections 4.3-4.4, highlighted in yellow.)

---

### Minor Comments

**Comment 1:** *Figure 1 provides limited technical value.*

**Response:** Figure 1 has been redesigned to show the actual Tesla valve geometry with labeled parameters (curvature radius, branching angle, channel widths, valve length) for both configurations.

**Comment 2:** *Table 2 should include dimensionless slot parameters.*

**Response:** The geometric parameters table (Table 1) now includes the dimensionless channel width ratio (η = W_b/W_m) for both geometries. Table 2 provides the Reynolds number correspondence.

**Comment 3:** *Figures 4–6 are too small and unclear.*

**Response:** Acknowledged. The figures will be presented at larger size with improved resolution, labels, and legend fonts in the final version.

**Comment 4:** *Several figures and tables are not properly referenced in the main text.*

**Response:** We have ensured that all figures and tables are properly cited and discussed in the text before they appear.

**Comment 5:** *Figure numbering should be corrected.*

**Response:** Figure numbering has been corrected to sequential order (Figs. 1-5) throughout the manuscript.

**Comment 6:** *Grammatical errors and awkward sentence constructions.*

**Response:** The manuscript has been carefully revised for English language quality.

**Comment 7:** *Notation and symbols should be checked for consistency.*

**Response:** All notation and symbols have been made consistent throughout the manuscript.

**Comment 8:** *Quality of figures should be improved.*

**Response:** Figure quality will be improved in the final submission with higher resolution.

---

## REVIEWER 2

**Comment 1:** *There is no grid.*

**Response:** A complete grid description has been added in Section 3.3 with detailed mesh statistics (Tables 4-5), inflation layer parameters (Table 3), and mesh quality metrics. (See Section 3.3, highlighted in yellow.)

**Comment 2:** *There is no validation.*

**Response:** A validation section (Section 3.5) has been added comparing our results against published data of de Vries et al. [30], showing less than 5% deviation in both pressure drop and diodicity. (See Section 3.5, Table 6, highlighted in yellow.)

**Comment 3:** *There are no design parameters mentioned anywhere.*

**Response:** Complete geometric design parameters are now presented in Table 1, including curvature radius, branching angle, channel width ratio, valve length, and hydraulic diameter for both configurations. Section 2 has been completely rewritten to describe the Tesla valve geometry with proper labeled schematics. (See Section 2, Table 1, highlighted in yellow.)

**Comment 4:** *It is a 2D analysis while turbulence is inherently 3D.*

**Response:** We clarify that our analysis is three-dimensional (3D). The computational domain is modeled as a 3D solid-walled conduit with rectangular cross-section (2.0 mm × 2.0 mm). This is now explicitly stated in Section 2: "The three-dimensional computational domain extends 5D_h upstream of the valve inlet and 10D_h downstream of the valve outlet." The 3D approach captures the secondary flows and vortex structures that are essential for accurate Tesla valve simulation.

**Comment 5:** *No mention of Reynolds number to compare the results. How did you use k-epsilon model?*

**Response:** Reynolds numbers are now reported throughout the manuscript. Table 2 provides the complete correspondence between inlet velocity and Reynolds number (Re = 200 to 2994). All results in Section 4 now include Reynolds numbers alongside inlet velocities.

Regarding the k-epsilon model justification, a new Section 3.2 provides a detailed explanation with four technical arguments: (i) extensive validation for internal flows with recirculation; (ii) Thompson et al. [13] demonstrated its applicability for Tesla valve flows; (iii) good balance between cost and accuracy for parametric studies; (iv) effectiveness for pressure-gradient-dominated flows. Enhanced wall functions and adequate near-wall mesh resolution (y+ < 5) were employed to address known limitations. (See Section 3.2, highlighted in yellow.)

---

## REVIEWER 3

**Comment:** *The paper provides an analysis of the reverse flow resistance effects of Tesla valves in two forms. Nevertheless, the results section lacks sufficient depth, as it merely evaluates the reverse flow pressure drop, which does not satisfy the requirements of a scientific research paper.*

**Response:** We sincerely thank the reviewer for this constructive criticism. The results section has been substantially expanded with the following additions:

1. **Section 4.1 (Forward Flow Pressure Drop):** Complete data table (Table 7) with forward pressure drop values for both geometries across all 7 Reynolds numbers.

2. **Section 4.2 (Reverse Flow):** Complete data table (Table 8) with reverse pressure drop values for both geometries.

3. **Section 4.3 (Diodicity Analysis - NEW):** Comprehensive quantitative analysis including:
   - Table 9 with diodicity values for both geometries at all Reynolds numbers
   - Discussion of Reynolds number dependence
   - Analysis of geometric influence on diodicity
   - Low-Re behavior interpretation
   - Transitional regime enhancement discussion

4. **Section 4.4 (Flow Mechanisms and Aerodynamic Performance - NEW):**
   - Vortex formation and recirculation analysis with vorticity magnitudes
   - Flow separation and reattachment length analysis
   - Hydraulic efficiency assessment with friction factor and net rectification efficiency metric

5. **Table 10:** Summary of all performance metrics at maximum Reynolds number.

These additions provide significantly deeper analysis including flow physics, quantitative metrics, and design-relevant performance comparisons. (See Sections 4.1-4.5, Tables 7-10, highlighted in yellow.)

---

## REVIEWER 4

**Comment 1:** *There is a citation given as "[1922]"? Please correct it.*

**Response:** Corrected. The citation has been fixed to **[19–22]** representing references 19 through 22. (See Introduction, highlighted in yellow.)

---

**Comment 2:** *Please see this word "pas-save flow rectifiers". I think it should be passive.*

**Response:** Corrected to **"passive flow rectifiers"**. (See end of Introduction, highlighted in yellow.)

---

**Comment 3:** *Fig. 3 and Fig. 4 captions both say "Pressure (a) and velocity (a) contour"? The second should presumably be labeled (b).*

**Response:** Corrected. Figure captions now read:
- "Fig. 4: Geometry 1, (a) Pressure contour and (b) velocity contour..."
- "Fig. 5: Geometry 2, (a) Pressure contour and (b) velocity contour..."
(See revised figure captions, highlighted in yellow.)

---

**Comment 4:** *Inconsistent Terminology. Intake velocity and then again inlet velocity; choose one.*

**Response:** We have standardized the terminology to **"inlet velocity"** throughout the entire manuscript. All instances of "intake velocity" have been replaced. (See throughout the manuscript.)

---

**Comment 5:** *Please improve the introduction section and increase relevancy. Some of the papers can be included but not limited to: https://doi.org/10.1016/j.applthermaleng.2022.119281, https://doi.org/10.1016/j.solener.2023.04.004, https://doi.org/10.1016/j.applthermaleng.2025.126769*

**Response:** Thank you for these valuable suggestions. We have added a new paragraph in the Introduction that discusses the broader context of geometry-driven passive flow control in thermal systems, specifically citing:
- [33] Agrawal & Rana (2022) – solar air heater duct roughness geometries
- [34] Kumar et al. (2023) – multiple arc-shaped roughened ribs in solar air heaters
- [35] Kumar et al. (2025) – multi-objective optimization with equilateral triangular ribs

The paragraph explains the relevance of these works to our Tesla valve study in terms of passive geometric modifications and trade-offs between heat transfer enhancement and pressure drop. (See Introduction, highlighted in yellow.)

---

**Comment 6:** *There is no mention of curvature radius, branching angle, channel width ratio, or valve length? Rewrite Section 2 to realistically present the Tesla valve geometry, with a proper labelled schematic figure.*

**Response:** Section 2 has been **completely rewritten**. The previous incorrect content (which described twisted tape inserts) has been removed and replaced with a proper description of the Tesla valve configurations including:
- Table 1 with all geometric parameters (curvature radius R_c, branching angle θ, channel width ratio η, valve length L_v, hydraulic diameter D_h)
- Detailed descriptions of both Geometry 1 (tight double-loop) and Geometry 2 (smooth single-loop)
- Updated Figure 1 caption with labeled schematic showing all parameters
(See Section 2, Table 1, highlighted in yellow.)

---

**Comment 7:** *Please quantify the grid-independence results.*

**Response:** Grid independence results are now fully quantified in Tables 4-5 showing exact cell counts and percentage differences for each mesh level:
- Geometry 1: 0.2% difference between medium (842,680 cells) and fine (1,524,300 cells) mesh
- Geometry 2: 0.4% difference between medium (685,420 cells) and fine (1,238,600 cells) mesh
(See Section 3.3.2, Tables 4-5, highlighted in yellow.)

---

**Comment 8:** *Why are Reynolds numbers not reported? Only inlet velocities (0.1–1.5 m/s) are reported, though?*

**Response:** Reynolds numbers are now reported throughout the manuscript. A new Table 2 provides the complete velocity-to-Reynolds number correspondence (Re = 200 to 2994 based on D_h = 2.0 mm). All results in Section 4 now include Reynolds numbers in parentheses alongside inlet velocities, e.g., "0.5 m/s (Re = 998)". The flow regime classification (laminar, transitional, turbulent) is also indicated for each Reynolds number. (See Section 3, Table 2, and throughout Section 4, highlighted in yellow.)

---

## Summary of Changes

| Change Category | Sections Modified |
|----------------|-------------------|
| Typographical corrections | Introduction, Figure captions |
| New references added | Introduction, References [33-35] |
| Section 2 completely rewritten | New Tesla valve geometry description |
| Grid/mesh details added | New Section 3.3 with Tables 3-5 |
| Reynolds numbers added | Table 2, throughout Section 4 |
| k-ε model justified | New Section 3.2 |
| Validation added | New Section 3.5, Table 6 |
| Diodicity analysis | New Section 4.3, Table 9 |
| Flow mechanisms discussion | New Section 4.4 |
| Performance summary | Table 10 |
| Conclusions expanded | Section 5 (6 numbered conclusions) |

We believe that these revisions substantially address all reviewer concerns and significantly improve the quality and depth of the manuscript. We hope the revised version meets the standards for publication.

---

*End of Response to Reviewers*
