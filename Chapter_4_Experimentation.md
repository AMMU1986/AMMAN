# CHAPTER 4: EXPERIMENTATION

## 4.1 Selection of Suitable Minerals Used as Fluxes for Submerged Arc Welding

The development of submerged arc welding (SAW) fluxes for marine and offshore pipeline applications requires a careful selection of mineral constituents that can collectively provide arc stability, adequate slag coverage, controlled element transfer, and desirable weld metal properties. In the present research, the mineral constituents were selected based on their individual contributions to slag behavior, thermophysical characteristics, and weld metal metallurgy.

The primary mineral constituents selected for the flux formulation system are:

1. **Silica (SiO₂):** Selected as an acidic constituent providing fluxing activity and slag fluidity. SiO₂ forms the backbone of silicate networks in the slag and influences the viscosity and melting characteristics.

2. **Titanium Dioxide (TiO₂):** Included to enhance arc stability and slag detachability. TiO₂ also contributes to inclusion modification in the weld metal, promoting acicular ferrite nucleation.

3. **Calcium Fluoride (CaF₂):** Added as a fluxing agent to reduce the melting point of the slag, control viscosity, and improve basicity. CaF₂ also aids in hydrogen removal and desulfurization.

4. **Barium Oxide (BaO):** Incorporated to stabilize arc effectiveness, contribute to slag formation, and increase the basicity index of the flux system.

5. **Manganese Oxide (MnO):** Included as a deoxidizer and for refining the weld-metal microstructure through controlled manganese transfer to the weld pool.

6. **Calcium Oxide (CaO):** Maintained at a constant level (8.0 g per 100 g batch) to provide baseline basic conditions and ensure consistent slag viscosity control across all formulations.

Additionally, **red ochre**, an iron-rich by-product of iron-ore extraction from Rajasthan, India, was used as an innovative additive. Red ochre was dried at 110°C for 24 hours and milled to less than 45 µm before incorporation. Inclusion levels ranged between 5.0 and 15.0 g per 100 g batch to substitute an equal fraction of silica, maintaining total batch mass. The high iron content of red ochre increases electrical conductivity, enhances arc stability, and adjusts weld-metal chemistry for improved corrosion resistance.

The purity of all mineral powders used was 99%, and the composition of each batch was verified through X-ray fluorescence (XRF) analysis to guarantee reproducibility and quality control.

### 4.1.1 Design of Experimentation for Flux Formulation

The traditional trial-and-error method was replaced by a systematic Design of Experiments (DoE) approach to develop twenty-five submerged arc welding fluxes. Since the mineral constituents (SiO₂, TiO₂, CaF₂, BaO, MnO, and fixed CaO) are interdependent—an increase in one component necessarily requires a decrease in one or more other components—the mixture technique of Design of Experiments was employed.

**Design-Expert software (version 13, Stat-Ease Inc., Minneapolis, MN, USA)** was used to generate the experimental flux design matrix. The D-optimal design was selected because the lower and upper bound constraints for the variables (Table 4.1) are not achievable in standard simplex-lattice or simplex-centroid designs. To minimize systematic bias, the replicates were randomly positioned in the design space.

**Table 4.1:** Mineral constituent composition ranges for flux formulation

| S. No | Mineral Constituent | Denoting Symbol | Range (g/100g batch) |
|-------|-------------------|-----------------|---------------------|
| 1 | SiO₂ | A | 5.0 – 10.0 |
| 2 | TiO₂ | B | 10.0 – 20.0 |
| 3 | CaF₂ | C | 20.0 – 35.0 |
| 4 | BaO | D | 5.0 – 10.0 |
| 5 | MnO | E | 10.0 – 25.0 |
| 6 | CaO | F | 8.0 (constant) |

The mixture formulation was designed according to the following mathematical constraints:

**Equation 4.1:**
$$0 \leq \alpha_i \leq x_i \leq \beta_i \leq 100$$

**Equation 4.2:**
$$\sum_{i=1}^{6} x_i = 100$$

where x is the mass in grams of every mineral constituent in every batch of 100 g, while α_i and β_i serve as the lower and upper specifications of each element.

The compositional design space was guided by established ternary and quaternary phase diagrams:

- **SiO₂–CaO–CaF₂ system (Fig. 4.1a):** The CaF₂ addition reduces the liquidus temperature and creates two-liquid zones, important for regulating slag fluidity.
- **SiO₂–MnO–TiO₂ system (Fig. 4.1b):** Plotted under controlled oxygen potential (pCO/pCO₂ = 1), showing the effect of Mn and Ti on silicate and titanate phase formation and stability.
- **BaO–SiO₂–CaF₂ system (Fig. 4.1c):** Indicates a low-melting dual liquid phase near the SiO₂–CaF₂ interface, facilitating easier flux melting.
- **Quaternary SiO₂–CaF₂–MnO–BaO model (Fig. 4.1d):** The polyhedral design space represents the scope of viable composition based on liquidus and phase-stability criteria.

**Fig. 4.1:** Representation of ternary and quaternary phase relationships used in flux formulation and compositional optimization. (a) The SiO₂–CaO–CaF₂ system showing liquid phase formation regions, (b) The SiO₂–MnO–TiO₂ equilibrium diagram under a controlled pCO/pCO₂ ratio of unity, (c) The BaO–SiO₂–CaF₂ diagram depicting liquidus surfaces and phase stability zones, (d) The quaternary compositional framework (SiO₂–CaF₂–MnO–BaO) defining the feasible design region selected for flux development studies.

The resulting twenty-five experimental flux compositions are presented in the design matrix (Table 4.2), which includes vertex points, centre edge points, plane centre points, and an overall centroid to ensure comprehensive coverage of the design space.

**Table 4.2:** Design matrix of flux composition

| Run | SiO₂ | TiO₂ | CaF₂ | BaO | MnO | CaO | Basicity Index | Point Type |
|-----|------|------|------|-----|-----|-----|---------------|------------|
| 1 | 10.00 | 18.59 | 21.42 | 9.99 | 25.00 | 8.00 | 2.253 | Vertex |
| 2 | 6.37 | 10.17 | 35.00 | 8.46 | 25.00 | 8.00 | 4.622 | Vertex |
| 3 | 8.15 | 13.98 | 35.00 | 10.00 | 17.86 | 8.00 | 3.201 | Vertex |
| 4 | 7.94 | 15.42 | 30.09 | 6.55 | 25.00 | 8.00 | 2.981 | Vertex |
| 5 | 8.15 | 13.98 | 35.00 | 10.00 | 17.86 | 8.00 | 3.201 | Vertex |
| 6 | 5.29 | 20.00 | 27.44 | 7.28 | 25.00 | 8.00 | 2.677 | Vertex |
| 7 | 10.00 | 14.37 | 25.63 | 10.00 | 25.00 | 8.00 | 2.816 | Centre Edge |
| 8 | 7.94 | 15.42 | 30.09 | 6.55 | 25.00 | 8.00 | 2.981 | Centre Edge |
| 9 | 7.94 | 15.42 | 30.09 | 6.55 | 25.00 | 8.00 | 2.981 | Centre Edge |
| 10 | 7.99 | 20.00 | 28.17 | 10.00 | 18.84 | 8.00 | 2.322 | Centre Edge |
| 11 | 10.00 | 20.00 | 26.73 | 5.00 | 23.27 | 8.00 | 2.100 | Centre Edge |
| 12 | 5.02 | 20.00 | 33.18 | 6.31 | 20.48 | 8.00 | 2.717 | Centre Edge |
| 13 | 5.00 | 14.38 | 30.62 | 10.00 | 25.00 | 8.00 | 3.799 | Centre Edge |
| 14 | 7.99 | 20.00 | 28.17 | 10.00 | 18.84 | 8.00 | 2.322 | Centre Edge |
| 15 | 8.79 | 15.54 | 35.00 | 5.35 | 20.32 | 8.00 | 2.823 | Centre Edge |
| 16 | 10.00 | 11.45 | 35.00 | 5.00 | 23.55 | 8.00 | 3.337 | Plane Centre |
| 17 | 10.00 | 19.37 | 31.71 | 9.51 | 14.41 | 8.00 | 2.166 | Plane Centre |
| 18 | 10.00 | 20.00 | 35.00 | 10.00 | 10.00 | 8.00 | 2.100 | Plane Centre |
| 19 | 10.00 | 16.88 | 31.33 | 7.89 | 18.90 | 8.00 | 2.461 | Plane Centre |
| 20 | 10.00 | 16.88 | 31.33 | 7.89 | 18.90 | 8.00 | 2.461 | Plane Centre |
| 21 | 10.00 | 10.00 | 30.00 | 10.00 | 25.00 | 8.00 | 3.650 | Plane Centre |
| 22 | 10.00 | 10.00 | 34.07 | 10.00 | 20.93 | 8.00 | 3.650 | Plane Centre |
| 23 | 7.97 | 20.00 | 35.00 | 6.01 | 16.02 | 8.00 | 2.326 | Plane Centre |
| 24 | 5.00 | 16.16 | 35.00 | 5.00 | 23.84 | 8.00 | 3.395 | Plane Centre |
| 25 | 5.00 | 20.00 | 35.00 | 9.30 | 15.70 | 8.00 | 2.720 | Overall Centroid |

The basicity index (BI) of all twenty-five fluxes was calculated using the modified Tulliani equation:

**Equation 4.3:**
$$BI = \frac{(CaO + CaF_2 + MgO + BaO + SrO + Na_2O) + 0.5(MnO + Fe)}{SiO_2 + 0.5(TiO_2 + Al_2O_3 + ZrO_2)}$$

The basicity index values ranged from 2.100 to 4.622, spanning from mildly acidic to strongly basic compositions.

### 4.1.2 Selection of SAW Process Parameters

For the multi-pass bead-on-plate experimentation, a single-wire submerged arc welding (SAW) machine was utilized with the following parameters:

- **Welding current:** 230 A (for bead-on-plate); 440 A (for butt joint welding)
- **Arc voltage:** 25 V (for bead-on-plate); 28 V (for butt joint welding)
- **Welding speed:** 8 inches/min (3.39 mm/s) for bead-on-plate; 13 inches/min for butt joints
- **Polarity:** Direct Current Electrode Positive (DCEP)
- **Electrode:** EA2TiB filler wire, 2.4 mm diameter
- **Arc efficiency (η):** 0.75

The heat input was calculated using the standard formula:

**Equation 4.4:**
$$HI = \frac{V \times I \times 60}{S} \times \eta$$

where V is the welding voltage, I is the welding current, S is the welding speed, and η is the arc efficiency.

For bead-on-plate experiments, the calculated heat input was approximately 1.02 kJ/mm, which is within the recommended range of 0.8–2.5 kJ/mm for X70 pipeline steel welding. This range prevents excessive coarsening of the heat-affected zone while ensuring full flux melting and sufficient slag-metal reaction time.

The interpass temperature was rigorously maintained at 120°C to 150°C, monitored at 25 mm from the weld bead centerline using a contact thermocouple sensor. This relatively low interpass temperature ensured that no coarse grains or martensite would form in the multipass weld metal, promoting acicular ferrite microstructure formation.

---

## 4.2 SAW Flux Preparation

The preparation of the agglomerated fluxes was performed in the laboratory following a systematic protocol:

**Step 1: Mineral Powder Preparation**
Each mineral constituent was individually milled to a particle size less than 45 µm (passing through a 325-mesh sieve). This particle size was selected to maximize the contact surface area, ensure uniform distribution of binder, achieve ideal agglomeration, and eliminate segregation of high-density oxides (BaO, MnO) during handling and welding.

**Step 2: Weighing and Mixing**
Mineral components were weighed accurately using a digital weighing balance (precision ±1 mg) based on the design matrix (Table 4.2). The powders were then combined in a turbula mixer for 30 minutes to obtain a homogeneous mixture.

**Step 3: Binder Addition**
Potassium silicate solution (K₂SiO₃) at 5 wt.% of the total batch mass was used as the inorganic binder. The binder was diluted in distilled water at a 1:3 ratio to lower viscosity and was gradually poured into the powdered mixture while continually stirring to ensure complete homogenization.

**Step 4: Agglomeration**
After uniform homogenization, a 1.0 mm sieve was used to form the wet mixture into green agglomerates.

**Step 5: Drying**
The green agglomerates were dried in an oven at 100°C for 2 hours to remove absorbed moisture and prevent cracking.

**Step 6: Crushing and Sieving**
The dried agglomerates were crushed and sieved to achieve a final particle size distribution of 0.5 mm to 1.4 mm (ASTM 14–35 mesh).

**Step 7: Final Baking**
The sieved fluxes were placed in sealed jars at 120°C overnight before welding to remove all remaining hydroxyl groups, thus reducing the probability of hydrogen-induced cracking in the multipass SAW beads.

For the butt joint welding experiments (Paper 3), an additional high-temperature treatment was employed: the mixed flux was baked at 200°C, followed by heating in a muffle furnace at 900°C, then cooled in air, crushed, and sieved to the required particle size before final packaging in airtight bags.

---

## 4.3 Characterization of Physicochemical and Thermophysical Properties of SAW Fluxes

### 4.3.1 Measurement of Density of Fluxes

Bulk density measurements were performed using the tapped-density methodology. The flux powders were placed into known cylindrical flasks (10 mL) with a standardized number of taps to ensure uniformity of particle distribution, then weighed using precise analytical balances.

The density calculation followed:

**Equation 4.5:**
$$\rho = \frac{Mass}{Volume}$$

This method determines the bulk properties and packing characteristics of the granular welding materials, which directly influence welding performance parameters such as flux flow and arc coverage.

### 4.3.2 Thermal Properties Measurement (Thermal Conductivity, Thermal Diffusivity, and Specific Heat)

Thermal conductivity, specific heat capacity, and thermal diffusivity measurements were made simultaneously using the **Hot Disk Transient Plane Source (TPS-2500S)** instrument, which follows the international standard method **ISO 22007-2**.

The TPS technique utilizes a nickel sensor enclosed in two thin insulating coatings, acting both as a heat source and resistance thermometer. The symmetric testing setup, with sensors placed between identical flux samples, eliminates the effect of thermal contact resistance and provides true bulk property results.

Measurement uncertainties are typically less than ±3% for thermal conductivity and ±5% for thermal diffusivity.

The thermal diffusivity was calculated using the fundamental relationship:

**Equation 4.6:**
$$\alpha = \frac{k}{\rho \cdot C_p}$$

where α is thermal diffusivity, k is thermal conductivity, ρ is density, and C_p is specific heat capacity.

The effective thermal conductivity follows the rule-of-mixtures expression:

**Equation 4.7:**
$$k_{eff} = \sum \varphi_i \cdot k_i$$

where k_eff represents effective thermal conductivity, φ_i denotes volume fraction, and k_i represents individual phase conductivity.

### 4.3.3 Phase Analysis of Fluxes

X-ray diffraction (XRD) analysis was performed on representative flux mixtures to identify crystalline phase assemblages and determine their relative proportions. The XRD patterns were recorded over the 2θ range of 15° to 65° using Cu-Kα radiation. Crystalline phases including fluorite (CaF₂), rutile (TiO₂), MnO, SiO₂, BaO, and CaO were identified by matching diffraction peaks with standard reference patterns.

The crystallite size and degree of crystallinity were qualitatively assessed from the sharpness and intensity of diffraction peaks, with full width at half maximum (FWHM) values used as indicators of crystallite size.

### 4.3.4 Structural Analysis of Fluxes

Fourier Transform Infrared (FTIR) spectroscopy was employed to study the molecular-level structural features of the flux samples. FTIR spectra were recorded in the wavenumber range of 4000–400 cm⁻¹ using the KBr pellet technique.

The FTIR analysis focused on:
- Si–O–Si asymmetric stretching vibrations (1070–1120 cm⁻¹)
- Non-bridging oxygen (Si–O) stretching vibrations (~950 cm⁻¹)
- O–H stretching bands (~3400 cm⁻¹)
- Ti–O lattice vibration bands (400–800 cm⁻¹)
- Si–O–Si bending modes (400–600 cm⁻¹)

The intensity ratio I₉₅₀/I₁₁₀₀ was used as a semi-quantitative measure to assess network depolymerization caused by modifier oxides (BaO, MnO, CaO).

---

## 4.4 Multi-Pass Bead-on-Plate Experimentation Using SAW Fluxes

### 4.4.1 Multi-Pass Bead-on-Plate Experimentation Using Laboratory Prepared SAW Fluxes

Using the twenty-five laboratory-prepared basic fluxes, multi-pass SAW weld beads were deposited in flat position configuration on **API X70 pipeline steel plates** of 16 mm thickness. No edge preparation was performed for the bead-on-plate experiments.

Five passes were deposited over each bead for each flux composition. The first pass served as the root/bead-on-plate, and subsequent four passes were deposited under controlled cooling conditions with interpass temperature maintained at 120–150°C.

**Fig. 4.2:** Photograph of twenty-five multi-pass SAW beads deposited on API X70 steel plate.

### 4.4.2 Chemical Analysis of Laboratory Prepared SAW Fluxes

To analyze the chemical composition of each multipass weld bead, **Atomic Absorption Spectroscopy (AAS)** was employed. A transverse section (approximately 10 mm thick) was cut from the central area of each bead-on-plate weld using an abrasive cut-off wheel, avoiding dilution from the base metal or heat-affected zone.

The extracted weld metal was ground (SiC abrasive papers: 220, 400, 600, 800, and 1200 grit) to remove surface contaminants and oxide scale, then ultrasonically cleaned in acetone for 10 minutes before analysis.

**Table 4.3:** Chemical composition of base metal and filler wire

| Material | C | Si | Mn | P | S | Mo | Ni | Cr | Fe |
|----------|------|------|------|-------|-------|------|------|------|------|
| BM (X70) | 0.058 | 0.331 | 1.590 | 0.006 | 0.002 | 0.003 | 0.219 | 0.007 | 98.1 |
| FW (EA2TiB) | 0.03 | 0.078 | 0.781 | 0.020 | 0.005 | 0.317 | 0.090 | 0.042 | 98.8 |

### 4.4.3 Microhardness Measurement of Beads

Microhardness of all twenty-five weld beads was measured using a Vickers microhardness tester under the following conditions:
- Load: 50 kgf
- Dwell time: 10 seconds

The carbon equivalent (CE) was calculated using the IIW formula to assess hardenability and weldability of the weld metal.

### 4.4.4 Selection of Adequate Fluxes by Qualitatively Analysing Multi-Pass Beads

Following multi-pass bead-on-plate experimentation, all twenty-five beads were visually examined to assess:
- Bead morphology (uniformity, smoothness)
- Porosity level (low, medium, high)
- Slag detachability (easy, medium, difficult)

Based on this preliminary screening, three fluxes from the basic flux system—**F6B, F20B, and F22B**—were selected for further investigation based on their exhibiting good bead morphology, minimum porosity, and satisfactory slag detachability characteristics.

---

## 4.5 Materials and Experimental Setup

### 4.5.1 Submerged Arc Welding Using Adequate Fluxes for Various Characterizations

#### 4.5.1.1 Formation of Weld Coupon

API X70 steel base plates of dimension **140 mm × 140 mm × 22 mm** were prepared for butt welding. A single-V groove joint configuration was adopted with:
- Groove angle: 60°
- Root gap: 2 mm
- Root face: 2 mm

**Fig. 4.3:** Schematic representation of butt weld joint configuration showing V-groove geometry with 60° included angle, 2 mm root gap, and 22 mm plate thickness.

#### 4.5.1.2 Submerged Arc Welding of Plates

All experimental welding was conducted with Direct Current Electrode Positive (DCEP) polarity using a single-wire submerged arc welding machine. The final welding parameters, established through pre-trial tests, were:
- Welding current: 440 A
- Arc voltage: 28 V
- Welding speed: 13 inches/min
- Contact tip-to-work distance: 20 mm

Four weld joints were fabricated:
- Three joints using selected laboratory-prepared fluxes (F6B, F20B, F22B)
- One reference joint using a commercial flux (C.F.)

#### 4.5.1.3 Weld Specimen Cutting

Following weld fabrication, specimens were extracted from each weld joint for comprehensive mechanical and microstructural characterization using wire-cut EDM and abrasive cutting techniques as per relevant ASTM standards.

#### 4.5.2 Weld Specimen Mechanical Characterization

##### 4.5.2.1 Weld Specimen Tensile Testing

Transverse tensile specimens were prepared and tested in accordance with ASTM E8 standard to determine ultimate tensile strength, yield strength, and elongation of the weld joints.

##### 4.5.2.2 Weld Specimen Impact Testing

Charpy V-notch impact testing was performed at two temperatures:
- Room temperature (~25°C)
- Sub-zero temperature (-55°C)

Specimens were extracted from both the fusion zone (FZ) and the heat-affected zone (HAZ) of each weld joint. Standard 10 mm × 10 mm × 55 mm Charpy specimens with a 2 mm deep, 45° V-notch were used.

##### 4.5.2.3 Fractography Analysis of Weld Specimens

Fracture surfaces of impact-tested specimens were examined using a Scanning Electron Microscope (SEM) operated at 10–15 kV accelerating voltage in secondary electron imaging mode at 1000× magnification. Fractographic features including dimples, cleavage facets, river patterns, microvoids, and fibrous tearing were identified and correlated with the mechanical performance.

##### 4.5.2.4 Weld Specimen Microhardness Testing

Vickers microhardness profiles were obtained across the weld cross-section (base metal → HAZ → fusion zone → HAZ → base metal) using:
- Load: 500 gf (HV0.5)
- Dwell time: 10 seconds
- Spacing: 0.5 mm between indentations

Measurements were taken in both the fusion zone and HAZ regions to map the hardness distribution.

##### 4.5.2.5 Weld Specimen Microstructure Analysis

Metallographic specimens were prepared using standard techniques:
1. Sequential grinding with ascending grits of emery paper (220, 400, 600, 800, 1200 grit)
2. Polishing with diamond paste to achieve a mirror-like surface finish
3. Etching with 2% Nital solution to reveal microstructural features

Optical microscopy was performed at 50× magnification (50 µm scale bar) to identify and characterize:
- Acicular ferrite (AF)
- Polygonal ferrite (PF)
- Grain boundary ferrite (GBF)
- Widmanstätten ferrite (WF)
- Bainite (upper and lower)
- Martensite-austenite (M/A) constituents
- Pearlite (P)

##### 4.5.2.6 Weld Specimen Corrosion Analysis

Electrochemical corrosion testing was performed to evaluate the corrosion resistance of the weld metal in simulated service environments, following standard electrochemical techniques to determine corrosion potential and corrosion rate.

---

## 4.6 Statistical Analysis and Regression Modelling

### 4.6.1 Mixture Regression Modelling

The regression equations for predicting weld metal composition were developed using mixture design methodology with Scheffé canonical mixture models. Due to the summation constraint (∑t_i = 85 wt.%), standard polynomial regression cannot be applied.

The general model forms used were:

**Linear (first-order) mixture model (Equation 4.8):**
$$\hat{y} = \sum_{i=1}^{q} \beta_i t_i$$

**Quadratic (second-order) mixture model (Equation 4.9):**
$$\hat{y} = \sum_{i=1}^{q} \beta_i t_i + \sum_{i<j}^{q} \beta_{ij} t_i t_j$$

**Special cubic (third-order) mixture model (Equation 4.10):**
$$\hat{y} = \sum_{i=1}^{q} \beta_i t_i + \sum_{i<j}^{q} \beta_{ij} t_i t_j + \sum_{i<j<k}^{q} \beta_{ijk} t_i t_j t_k$$

The coefficient vector was obtained using ordinary least squares (OLS):

**Equation 4.11:**
$$\boldsymbol{\beta} = (X^T X)^{-1} X^T y$$

Model selection was performed using ANOVA with terms retained if p < 0.05. Model adequacy was verified using R² values (0.76–0.95), F-tests, lack-of-fit tests, and predicted versus actual plots.

---

*End of Chapter 4*
