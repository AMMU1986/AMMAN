# Chapter 4: Experimentation

## 4.1 Selection of Suitable Minerals Used as Fluxes for Submerged Arc Welding

Submerged arc welding (SAW) is one of the most widely used welding processes in shipbuilding, offshore structures, pressure vessels, pipeline construction, and automotive manufacturing due to its high deposition rate, deep penetration, and stable arc. The performance of SAW fluxes directly influences weld metal mechanical properties, corrosion resistance, and slag detachability. These factors are critical for components subjected to cyclic loading in corrosive marine environments. The design of the welding fluxes plays an important role in the fulfilment of these properties, in particular regarding the behaviour of the arc, slag formation and heat transfer during the submerged arc welding operation. Traditionally, the flux design has relied on trial-and-error techniques leading to improper arc stability and slag detachability. Introducing more systematic and scientific models, however, on the basis of the Design of Experiments (DoE) methodology allows optimized flux formulations to be used for challenging industrial applications.

The present research work aims to systematically design and characterize twenty-five submerged arc welding fluxes using controlled mineral blends that are optimized for harsh and saltwater conditions developed into fluxes to be used in marine and offshore welding applications. The main mineral ingredients selected for flux formulation include silica (SiO₂), titanium dioxide (TiO₂), calcium fluoride (CaF₂), barium oxide (BaO), manganese oxide (MnO), and calcium oxide (CaO). These constituents were mixed in controlled ratios with CaO kept constant to stabilize slag chemistry. The purity of mineral powders used was 99%, and the composition of each batch was checked through X-ray fluorescence (XRF) analysis to guarantee reproducibility and quality control of the composition.

The selection of each mineral constituent was guided by its specific metallurgical contribution to the welding process:

**Silica (SiO₂):** Silica was adjusted in the range of 5.0 to 10.0 g per 100 g batch, which offers fluxing activity and slag fluidity. Silica serves as an acidic oxide that forms the backbone of the silicate network in the slag, controlling its viscosity and flow characteristics during welding.

**Titanium Dioxide (TiO₂):** The titanium dioxide level was varied between 10.0 and 20.0 g per 100 g batch in order to enhance the arc stability and slag detachability. TiO₂ is a well-known arc stabilizer that contributes to smooth arc characteristics and facilitates easy removal of the solidified slag from the weld bead surface.

**Calcium Fluoride (CaF₂):** Calcium fluoride was added to reduce the melting point of the slag; the amount of CaF₂ ranged from 20.0 to 35.0 g per 100 g batch to create well-suited offshore welding conditions. CaF₂ is a powerful fluxing agent that dramatically lowers the liquidus temperature of the slag system, reduces viscosity, and enhances the fluidity necessary for proper weld pool coverage.

**Barium Oxide (BaO):** Barium oxide was loaded in the range of 5.0 to 10.0 g per 100 g batch to stabilize the arc effectiveness and help in the formation of slag. BaO acts as a strong basic oxide that contributes to the overall basicity of the flux system, improves desulfurization capability, and provides radiation shielding benefits.

**Manganese Oxide (MnO):** Manganese oxide was loaded in the range of 10.0 to 25.0 g per 100 g batch, serving as a deoxidizer and refining the weld-metal microstructure. MnO plays a dual role in the welding process — it provides manganese to the weld metal through slag-metal reactions while simultaneously acting as a deoxidizer.

**Calcium Oxide (CaO):** In each formulation, 8.0 g calcium oxide was incorporated as a baseline basic condition and to ensure control of slag viscosity. CaO was kept constant across all 25 formulations to eliminate it as a variable and maintain consistent baseline slag chemistry.

Table 4.1 summarizes the mineral constituent composition ranges used for the flux formulation design matrix.

**Table 4.1: Mineral constituent composition ranges for flux formulation**

| S. No | Mineral Constituent | Denoting Symbol | Range (g/100g batch) |
|-------|-------------------|-----------------|---------------------|
| 1 | SiO₂ | A | 5.0 – 10.0 |
| 2 | TiO₂ | B | 10.0 – 20.0 |
| 3 | CaF₂ | C | 20.0 – 35.0 |
| 4 | BaO | D | 5.0 – 10.0 |
| 5 | MnO | E | 10.0 – 25.0 |
| 6 | CaO | F | 8.0 (constant in all compositions) |

As an innovative additive, red ochre, which is an iron-edible by-product of iron-ore extraction in Rajasthan, India, was used. Being red ochre, it was dried in the oven at 110°C for a period of 24 hours and milled to less than 45 μm before mixing. Inclusion levels were between 5.0 and 15.0 g per 100 g batch to substitute an equal fraction of silica to maintain total batch mass. With high iron levels, red ochre increases electrical conductivity, arc stability and adjusts weld-metal chemistry and microstructure to provide better corrosion resistance. The use of red ochre as a sustainable arc-stabilizing additive in SAW fluxes represents a novel contribution of this research, as such application has not been previously investigated in the literature.

### 4.1.1 Design of Experimentation for Flux Formulation

The traditional trial-and-error method was replaced by a systematic Design of Experiments (DoE) approach to develop the twenty-five submerged arc welding fluxes. Since mineral constituents (SiO₂, TiO₂, CaF₂, BaO, MnO and fixed CaO) are interdependent and an increase in one component necessarily requires a decrease in one or more other components, the mixture technique of Design of Experiments was employed. Design-Expert software (version 13, Stat-Ease Inc., Minneapolis, MN, USA) was used to design an experimental flux design matrix for SiO₂, TiO₂, CaF₂, BaO, MnO and fixed CaO ingredients.

The D-optimal design was selected because the lower and upper bound constraints for the variables (Table 4.1) are not possible in standard simplex-lattice or simplex-centroid designs. To minimize systematic bias, the replicates were randomly positioned in the design space. The mixture formulation was designed according to the following mathematical constraints:

**Equation 4.1:**
$$0 \leq \alpha_i \leq x_i \leq \beta_i \leq 100$$

**Equation 4.2:**
$$\sum_{i=1}^{6} x_i = 100$$

where x is the mass in grams of every mineral constituent in every batch of 100 g, while α_i and β_i serve as the lower and upper specifications of each element, as detailed in Table 4.1. Equation 4.1 ensures that the amount of each single element is within a given range. The scale is able to adapt the mass variations brought by adding red ochre and binder materials.

The compositional range is analyzed based on a number of basic ternary systems as illustrated in Figure 4.1. The CaF₂ addition to the SiO₂-CaO-CaF₂ diagram (Figure 4.1a) reduces the liquidus temperature and creates two-liquid zones, which are important in regulating the fluidity of slag. The SiO₂-MnO-TiO₂ system (Figure 4.1b) plotted under controlled oxygen potential shows the effect of Mn and Ti in the formation and stability of silicate and titanate phases, and hence, the stability of the arc as well as the slag release. The BaO-SiO₂-CaF₂ system (Figure 4.1c) also indicates a low-melting dual liquid phase near the SiO₂-CaF₂ interface, which means that the flux is easier to melt than the others. These ternary combinations are then further extended to a quaternary model SiO₂-CaF₂-MnO-BaO (Figure 4.1d), whose polyhedral zone represents the scope of composition that is viable, based on the results of the liquidus and phase-stability criteria observed in the target systems. It is used as an umbrella design guide to designing flux compositions to provide stable melting characteristics and controlled slag properties.

**Figure 4.1:** Representation of ternary and quaternary phase relationships used in flux formulation and compositional optimization. (a) The SiO₂–CaO–CaF₂ system showing liquid phase formation regions, (b) The SiO₂–MnO–TiO₂ equilibrium diagram under a controlled pCO/pCO₂ ratio of unity, (c) The BaO–SiO₂–CaF₂ diagram depicting liquidus surfaces and phase stability zones, (d) The quaternary compositional framework (SiO₂–CaF₂–MnO–BaO) defining the feasible design region selected for flux development studies.

The basicity index (BI) of 25 fluxes was calculated using Equation 4.3 given by Tulliani:

**Equation 4.3:**
$$Basicity\ Index = \frac{(CaO + CaF_2 + MgO + BaO + SrO + Na_2O) + 0.5(MnO + Fe)}{SiO_2 + 0.5(TiO_2 + Al_2O_3 + ZrO_2)}$$

This index was developed with an improved description of the fluxing and deoxidizing effect of CaF₂ and MnO, in addition to the conventional basic oxides. The resulting values of the basicity index ranged between 2.100 and 4.622, virtually grouping the fluxes between acidic and strongly basic as indicated in Table 4.2. CaF₂ and MnO rich blends (e.g., Run 2) had the highest basicity and those with high levels of SiO₂ and TiO₂ had the lowest basicity.

The experimental stability was ensured since repeated compositions in such manner of intentional repetition gave the same values of the basicity index, which proved the methodological solution of the process of flux formulation and screening. A high level of SiO₂ and TiO₂ reduced the basicity index, which is generally responsible for producing liquid slags. In contrast, BaO and the constant 8% CaO increased the index, which correlates with improved desulfurization potential and better slag detachability from the weld metal.

The use of the basicity index proved to be useful as a comparative screening index. Using the CaF₂ and MnO in the flux mixture computation, the basicity index measure was more performance reflective, with high index values corresponding to greater fluxing capacity and deoxidation capacity. This can be observed in the high basicity index blends such as Runs 13, 21 and 22, blending oxides with maximum benefit and minimum harm on the content of MnO and CaF₂.

**Table 4.2: Design matrix of flux composition**

| Run | SiO₂ | TiO₂ | CaF₂ | BaO | MnO | CaO | Basicity Index | Polyhedron Points |
|-----|------|------|------|-----|-----|-----|----------------|-------------------|
| 1 | 10.0000 | 18.5875 | 21.4218 | 9.9907 | 25.0000 | 8.0000 | 2.253 | Vertex |
| 2 | 6.3710 | 10.1721 | 35.0000 | 8.4569 | 25.0000 | 8.0000 | 4.622 | Vertex |
| 3 | 8.1508 | 13.9845 | 35.0000 | 10.0000 | 17.8647 | 8.0000 | 3.201 | Vertex |
| 4 | 7.9403 | 15.4216 | 30.0875 | 6.5505 | 25.0000 | 8.0000 | 2.981 | Vertex |
| 5 | 8.1508 | 13.9845 | 35.0000 | 10.0000 | 17.8647 | 8.0000 | 3.201 | Vertex |
| 6 | 5.2878 | 20.0000 | 27.4372 | 7.2750 | 25.0000 | 8.0000 | 2.677 | Vertex |
| 7 | 10.0000 | 14.3697 | 25.6303 | 10.0000 | 25.0000 | 8.0000 | 2.816 | Centre Edge |
| 8 | 7.9403 | 15.4216 | 30.0875 | 6.5505 | 25.0000 | 8.0000 | 2.981 | Centre Edge |
| 9 | 7.9403 | 15.4216 | 30.0875 | 6.5505 | 25.0000 | 8.0000 | 2.981 | Centre Edge |
| 10 | 7.9942 | 20.0000 | 28.1671 | 10.0000 | 18.8387 | 8.0000 | 2.322 | Centre Edge |
| 11 | 10.0000 | 20.0000 | 26.7320 | 5.0000 | 23.2680 | 8.0000 | 2.100 | Centre Edge |
| 12 | 5.0225 | 20.0000 | 33.1834 | 6.3129 | 20.4812 | 8.0000 | 2.717 | Centre Edge |
| 13 | 5.0000 | 14.3807 | 30.6193 | 10.0000 | 25.0000 | 8.0000 | 3.799 | Centre Edge |
| 14 | 7.9942 | 20.0000 | 28.1671 | 10.0000 | 18.8387 | 8.0000 | 2.322 | Centre Edge |
| 15 | 8.7884 | 15.5402 | 35.0000 | 5.3529 | 20.3186 | 8.0000 | 2.823 | Centre Edge |
| 16 | 10.0000 | 11.4468 | 35.0000 | 5.0000 | 23.5532 | 8.0000 | 3.337 | Centre Edge |
| 17 | 10.0000 | 19.3687 | 31.7112 | 9.5128 | 14.4072 | 8.0000 | 2.166 | Plane Centre |
| 18 | 10.0000 | 20.0000 | 35.0000 | 10.0000 | 10.0000 | 8.0000 | 2.100 | Plane Centre |
| 19 | 10.0000 | 16.8752 | 31.3320 | 7.8940 | 18.8989 | 8.0000 | 2.461 | Plane Centre |
| 20 | 10.0000 | 16.8752 | 31.3320 | 7.8940 | 18.8989 | 8.0000 | 2.461 | Plane Centre |
| 21 | 10.0000 | 10.0000 | 30.0000 | 10.0000 | 25.0000 | 8.0000 | 3.650 | Plane Centre |
| 22 | 10.0000 | 10.0000 | 34.0733 | 10.0000 | 20.9267 | 8.0000 | 3.650 | Plane Centre |
| 23 | 7.9677 | 20.0000 | 35.0000 | 6.0136 | 16.0186 | 8.0000 | 2.326 | Plane Centre |
| 24 | 5.0000 | 16.1588 | 35.0000 | 5.0000 | 23.8412 | 8.0000 | 3.395 | Plane Centre |
| 25 | 5.0000 | 20.0000 | 35.0000 | 9.3000 | 15.7000 | 8.0000 | 2.720 | Overall Centroid |

The extreme vertices design methodology, following the original proposal of McLean and Anderson, was used to develop the total of twenty-five agglomerated submerged arc welding fluxes. The resulting three-dimensional design space for the mixture system is a polyhedron with five vertices. To sweep this design region in a thorough manner, twenty-five experimental flux compositions were systematically formulated as shown in Table 4.2. The design points include vertices (V), centre edges (CE), plane centres (PC), and an overall centroid (OC), ensuring comprehensive coverage of the feasible compositional space.

For the multipass bead-on-plate experimentation and subsequent butt weld joint fabrication, the flux component constraints were expressed as:

**Equation 4.4:**
$$5 \leq SiO_2(t_1) \leq 10$$
$$10 \leq TiO_2(t_2) \leq 20$$
$$20 \leq CaF_2(t_3) \leq 35$$
$$10 \leq MnO(t_4) \leq 25$$
$$5 \leq BaO(t_5) \leq 10$$
$$\sum_{i=1}^{4} t_i = 85$$

### 4.1.2 Selection of SAW Process Parameters

The selection of appropriate submerged arc welding process parameters was critical to ensuring consistent weld quality across all twenty-five flux formulations. Parameters were selected based on pre-trial tests to determine bead profile consistency, slag detachability, and absence of surface defects such as undercut or over-reinforcement.

**For Multi-Pass Bead-on-Plate Experimentation:**

A single-wire submerged arc welding (SAW) machine was utilized with the following parameters:
- Welding current: 230 A
- Arc voltage: 25 V
- Welding speed: 8 inches/min (3.39 mm/s)
- Filler wire: EA2TiB with 2.4 mm diameter
- Wire feed: constant rate (no extra cold feed wire)
- Polarity: Direct Current Electrode Positive (DCEP)

The heat input was calculated using the standard formula:

**Equation 4.5:**
$$Heat\ Input\ (HI) = \frac{V \times I \times 60}{S} \times \eta$$

where V is the welding voltage, I is the welding current, S is the welding speed (mm/min), and η is the arc efficiency (η = 0.75 for SAW).

A heat input value of approximately 1.02 kJ/mm was obtained from Equation 4.5, which is within the recommended range of 0.8–2.5 kJ/mm for X70 pipeline steel welding to prevent excessive coarsening of the heat-affected zone and to guarantee full flux melting and sufficient reaction time of slag-metal interactions.

**For Butt Weld Joint Fabrication:**

For the final butt weld joints with selected fluxes, the welding parameters were adjusted based on plate thickness and joint geometry:
- Welding current: 440 A
- Arc voltage: 28 V
- Welding speed: 13 inches/min
- Contact tip-to-work distance: 20 mm
- Polarity: DCEP
- Base plate dimensions: 140 mm × 140 mm × 22 mm

These parameters were determined after preliminary test welds conducted to qualitatively assess bead profile, porosity, and slag detachability on a low, medium, or high scale.

## 4.2 SAW Flux Preparation

The preparation of the agglomerated fluxes was performed in the laboratory following a systematic multi-step procedure to ensure homogeneity, proper bonding, and consistent performance during welding.

**Step 1: Mineral Powder Preparation**

Each mineral constituent was individually milled to a particle size of less than 45 μm (passing through a 325-mesh sieve). This was done to develop a homogeneous flux mixture and to ensure consistent melting during submerged arc welding. This particle size was selected due to its maximum contact surface area of individual flux constituents, uniform distribution of binder, and ideal agglomeration, thus eliminating segregation of high-density oxides like BaO and MnO throughout handling and welding processes.

**Step 2: Weighing and Dry Mixing**

Following the weighing of the mineral components based on the design matrix (Table 4.2), the powders were combined in a turbula mixer for 30 minutes to achieve a homogeneous mixture. The mineral constituents were weighed accurately using a digital weighing balance (precision ±1 mg).

**Step 3: Binder Addition**

Potassium silicate solution (K₂SiO₃) at 5 wt.% of the total batch mass was added as an inorganic binder so that the mineral powders would adhere to form agglomerates. The role of the potassium silicate is to serve as a binding agent to hold together the separate flux constituents and to enhance arc stability during welding. The binder was diluted in distilled water at a 1:3 ratio to lower the viscosity and was then gradually poured into the powdered mixture while being continually stirred to homogenize the whole flux mixture.

**Step 4: Agglomeration**

After uniformly homogenizing the flux mixture, a 1.0 mm sieve was used to form the wet mixture into green agglomerates, which were then dried in an oven at 100°C for 2 hours to dry out the agglomerates and remove absorbed moisture before cracking.

**Step 5: Crushing and Sieving**

The agglomerates were then dried and crushed and sieved to reach a final particle size distribution of 0.5 mm to 1.4 mm (ASTM 14-35 mesh). This particle size range is optimal for submerged arc welding as it provides adequate flux coverage over the weld pool while allowing uniform melting.

**Step 6: Final Drying and Storage**

The sieved fluxes were placed in sealed jars at 120°C overnight before welding to remove all remaining hydroxyl groups, thus reducing the chances of the multipass welded SAW beads cracking as a result of hydrogen pickup. For the butt weld joint experiments, an additional high-temperature baking step was employed: after initial air drying for twenty-four hours, the flux was baked in an oven at 200°C to remove all remaining moisture, followed by heating in a muffle furnace at a temperature of 900°C. The flux was then crushed after being allowed to cool in air, sieved to the required particle size, and finally packed in airtight bags to avoid absorption of moisture before welding.

The entire flux preparation process is summarized as follows:

1. Individual mineral powders milled to <45 μm
2. Accurate weighing per design matrix
3. Dry mixing in turbula mixer (30 minutes)
4. Addition of diluted potassium silicate binder (5 wt.%)
5. Wet mixing until homogeneous
6. Sieving through 1.0 mm mesh for agglomeration
7. Drying at 100°C for 2 hours
8. Crushing and sieving to 0.5–1.4 mm (ASTM 14-35 mesh)
9. Final baking at 120°C overnight (or 200°C + 900°C for butt weld fluxes)
10. Storage in airtight containers




## 4.3 Characterization of Physicochemical and Thermophysical Properties of SAW Fluxes

A comprehensive characterization of the physicochemical and thermophysical properties of the twenty-five formulated SAW fluxes was undertaken to establish correlations between composition, structure, and anticipated welding performance. The characterization program included bulk density measurement, thermal property determination (thermal conductivity, thermal diffusivity, and specific heat capacity), phase analysis via X-ray diffraction (XRD), and structural analysis via Fourier Transform Infrared (FTIR) spectroscopy. These measurements provide the scientific foundation for understanding how the mineral composition of fluxes influences their thermal behavior during welding and, consequently, the quality of the resultant weld.

### 4.3.1 Measurement of Density of Fluxes

The bulk density of each of the twenty-five flux formulations was measured using the tapped-density methodology. In this method, the flux powders were placed into known cylindrical flasks (10 mL) and subjected to a known set of tapping cycles, which ensures the uniformity of particle distribution. The samples were then weighed using precise analytical balances. This method characterizes the packing nature and characteristics of the particles, which directly influence the bulk properties and welding performance parameters of granular welding materials.

Density calculation followed Equation 4.6:

**Equation 4.6:**
$$\rho = \frac{Mass}{Volume}$$

where ρ represents the bulk density in g/cm³, Mass is the total mass of the tapped flux sample in grams, and Volume is the occupied volume in cm³ after tapping.

The entire thermophysical characterization of the 25 different submerged arc welding flux formulations showed a density range of 1.40 to 1.54 g/cm³ (Figure 4.2a), which shows good correlation with the literature values of such multicomponent flux systems. A similar range of density of 1.35–1.58 g/cm³ was reported by Sharma and Chhibber in the system of CaO-SiO₂-CaF₂ flux and was reported in the 1.42–1.56 g/cm³ range of TiO₂-SiO₂-MgO systems by Kowalski and Nowak.

Formulations enriched in high-density oxides such as BaO (ρ = 5.72 g/cm³) and MnO (ρ = 5.03 g/cm³) exhibited maximum density values (Flux 14–Flux 16 and Flux 23–Flux 25), consistent with theoretical predictions based on rule-of-mixtures calculations. Conversely, silica-dominated (SiO₂, ρ = 2.65 g/cm³) and fluorspar-rich (CaF₂, ρ = 3.18 g/cm³) compositions displayed lower bulk densities (Flux 1–Flux 6). This compositional-density relationship aligns with established principles in flux metallurgy, where Singh et al. demonstrated similar trends with R² correlation coefficients exceeding 0.85 between oxide density and flux bulk density.

The mean density of 1.48 ± 0.04 g/cm³ is an optimal value with regards to compaction properties that can be successfully used in SAW with appropriate performance measures such as flourishing flux flow and arc coverage. This value lies in the optimal range determined by Kumar et al., who found that SAW fluxes with the density of 1.4–1.6 g/cm³ possess the best arc stability and the ability of slag to detach. The rather close density structure (coefficient of variation = 2.7%) points towards low porosity and high manufacturing reproducibility, owed to the uniform addition of CaO binder (8%) when undergoing agglomeration.

### 4.3.2 Thermal Properties (Thermal Conductivity, Thermal Diffusivity, and Specific Heat) Measurement

Specific heat capacity, thermal diffusivity, and thermal conductivity measurements were made using the Hot Disk Transient Plane Source (TPS-2500S), which is the international standard method (ISO 22007-2) for simultaneous determination of thermal properties. The TPS technique utilizes a nickel sensor that is enclosed in two thin insulating coatings to act both as a specialized heat source and resistance thermometer. The arrangement allows accurate determination of thermal transport characteristics by examining manifested transient temperature variations in response to controlled heat pulse application.

Compared to traditional methods, the TPS method is more accurate with the measurement uncertainties usually less than ±3 percent and ±5 percent of thermal conductivity and thermal diffusivity, respectively. TPS measurements were compared by White and Collocott to reference materials and found to agree very well with known values across a variety of material classes. The symmetric testing setup used in this experiment, with sensors between the same flux samples, has removed the effect of thermal contact resistance and given real bulk property results.

**Thermal Conductivity:**

The outcome of the thermal conductivity measurements (Figure 4.2b) showed that the range of materials was 0.34 to 0.52 W/m·K, with an indication of compositional dependence apparent, and in line with the known structure-property relationships within ceramic flux systems. These values are consistent with values reported in literature: Sharma and Chhibber found that similar agglomerated flux composites had thermal conductivities of 0.31–0.48 W/m·K, whereas Kumar et al. reported a thermal conductivity of 0.38–0.55 W/m·K for TiO₂-SiO₂-based systems.

The strong dependence between the density of the flux and thermal conductivity indicates the underlying heat transfer processes in heterogeneous oxides. High concentrations of the metallic oxides (MnO, BaO, and TiO₂) in dense fluxes always had high thermal conduction properties, with thermal conductivity values enhanced by a maximum of 53% over silicate-based formulations. This improvement is caused by improved phonon transport properties of crystalline metallic oxide phases compared to amorphous silicate networks.

On the other hand, silica-based compositions (Flux 1–Flux 6) were found to have insulating properties with smaller values of thermal conductivity, which is in line with known lower values of thermal conductivity of amorphous SiO₂ (0.1–0.2 W/m·K). This is a compositional effect that Kang and Morita have studied extensively and shown that values of thermal conductivity reduce drastically with increases in SiO₂ content, especially when the ratio of CaO/SiO₂ decreases below one.

The relationship follows the expression:

**Equation 4.7:**
$$k_{eff} = \sum \phi_i k_i$$

where k_eff represents effective thermal conductivity, φ_i denotes volume fraction, and k_i represents individual phase conductivity.

**Specific Heat Capacity:**

Measurements of specific heat capacity ranged between 0.902 and 1.192 MJ/m³·K across the flux formulations (Figure 4.2c), of which Flux 25 had the highest specific heat capacity of 1.28 MJ/m³·K, which was the highest in the CaF₂ and MnO concentration range. These values indicate splendid consistency with previously reported data: Kumar et al. received specific heat values of 0.85–1.15 MJ/m³ produced by electrode coating of CaF₂, whereas Sharma and Chhibber acquired the values of 0.91–1.21 MJ/m³ produced by electrode coating of the same flux.

SAW applications with high specific heat capacity have high metallurgical benefits in that it helps in greater thermal energy capture prior to an increase in temperature. This property keeps the arc under control and regulates the rate of cooling in weld pools — key considerations in the elimination of thermal shock and the endurance of uniform slag layer structure. The dependence of the specific heat on CaF₂ is governed by the general thermodynamic laws whereby addition of fluoride increases the heat capacity by increasing the vibrational modes of the lattice.

**Thermal Diffusivity:**

Thermal diffusivity measurements varied between 0.202 and 0.351 mm²/s (Figure 4.2d), calculated using the fundamental relationship:

**Equation 4.8:**
$$\alpha = \frac{k}{\rho C_p}$$

where α represents thermal diffusivity, k denotes thermal conductivity, ρ is density, and C_p represents specific heat capacity.

Flux 3 and Flux 22 fluxes with high concentration of silica and fluorspar had the lowest thermal diffusivity values (0.202–0.215 mm²/s), and this represents the best thermal insulation capacity necessary to sustain the weld pool protection. These values are comparable with experiments conducted by Negi and Chattopadhyaya who found thermal diffusivities of 0.18–0.23 mm²/s for silicate-dominated SAW fluxes. Compositions with high content of BaO or MnO (Flux 8 and Flux 20), possessing better thermal transport properties, exhibited a higher rate of heat propagation (0.335–0.351 mm²/s).

The results of thermal diffusivity investigations lead to basic conclusions on thermal management of a weld pool: the controlled heat transfer rates define the cooling and microstructural change. Low thermal diffusivity fosters slow cooling and high ductility, whereas high thermal diffusivity fosters fast cooling and smooth grain structures.

**Figure 4.2:** Variation of thermophysical properties of flux number with (a) density, (b) thermal conductivity, (c) specific heat, and (d) thermal diffusivity.

### 4.3.3 Phase Analysis of Fluxes

X-ray diffraction (XRD) analysis was performed on selected flux mixtures to identify the crystalline phase assemblage, which provides in-depth information on thermal conduct and metallurgical workability during the welding process. XRD patterns were obtained for four representative flux compositions: Flux 2, Flux 12, Flux 16, and Flux 20, selected to represent the range of compositions in the design matrix.

**XRD Analysis of Flux 2 (Figure 4.3a):**

Flux 2, containing 35% CaF₂ and 25% MnO (Table 4.2), exhibits strong, sharp fluorite reflections at 2θ = 28.3°, 32.2°, and 47.0°, corresponding to the (111), (200) and (220) planes respectively. High intensity and categorically small full width at half maximum (FWHM) indicates the high crystallinity and a large crystallite size, indicating that the thermal treatment during flux preparation was adequate to encourage good formation of fluorite crystal growth.

**XRD Analysis of Flux 20 (Figure 4.3d):**

In contrast, lower CaF₂ content (31.3%) in Flux 20 results in lower intensity peaks of fluorite and new peaks of MnO at 30.1° and 50.5°. The negative correlation between the intensity of the peak of fluorite and MnO indicates a crystallization effect, in which the addition of MnO to the specimens may also have favoured the growth of other crystal phases.

**XRD Analysis of Flux 12 (Figure 4.3b):**

Flux 12 displays an intermediate phase assemblage with strong fluorite reflections accompanied by well-defined rutile peaks at 27.4°, 36.1°, and 54.4°, as well as discrete MnO signatures. The enhanced rutile-to-fluorite intensity ratio in Flux 12 compared to Flux 2 indicates improved titania retention in crystalline form, which is relevant for arc stabilization.

**XRD Analysis of Flux 16 (Figure 4.3c):**

Flux 16, with 35% CaF₂ and relatively high TiO₂ content, shows both strong fluorite and rutile peaks, indicating coexistence of these crystalline phases with well-defined peak intensities.

**Structure–Property Correlations from XRD:**

Results of XRD analysis can be correlated with the thermophysical properties described in Section 4.3.1 and 4.3.2. Specifically, higher degree of crystallinity in fluorite (Flux 2 and 16) resulted in lower values of thermal diffusivity (0.215–0.245 mm²/s) than the MnO-rich Flux 20 (0.335 mm²/s). This is consistent with the known phonon scattering effect of fluorite-structured compounds, where the presence of fluorine vacancies disrupts heat-carrying phonon propagation. On the other hand, the higher thermal diffusivity of the MnO-rich compositions can be explained due to the metallic nature of the oxidation state of MnO that enables electronic thermal conduction.

In addition, the qualitative assessment of degree of crystallinity made from the sharpness and intensity of peaks in the XRD profiles is inversely proportional to the basicity index. The studies indicated that diffraction peaks were typically more intense and sharp for higher basicity fluxes (as in Flux 2 and 13) as compared to lower basicity fluxes (such as Flux 11 and 18), which typically had broader and weaker diffraction peak intensities, reflecting higher amorphous content. This relationship is mechanistically plausible due to the fact that basic oxides (CaO, BaO) and CaF₂ have a tendency to be present in the form of unique crystalline phases, while SiO₂ is capable of forming amorphous glassy networks.

**Figure 4.3:** X-ray diffraction patterns of flux samples showing intensity (arbitrary units) versus 2θ (degrees) for four different compositions: (a) Intensity vs 2θ value for Flux 2, (b) Intensity vs 2θ value for Flux 12, (c) Intensity vs 2θ value for Flux 16, and (d) Intensity vs 2θ value for Flux 20.

### 4.3.4 Structural Analysis of Fluxes

Fourier Transform Infrared (FTIR) spectroscopy was employed to understand the molecular-level structural features of the flux formulations. FTIR spectra were obtained for eight flux samples divided into two sets: Set A (Flux 1, Flux 6, Flux 7, Flux 11) and Set B (Flux 14, Flux 19, Flux 21, Flux 25), as shown in Figure 4.4. The spectra are similar to the interpretation of oxide-based welding flux systems. Typical absorption bands characteristic of the vibrations in the silicate network, hydroxyl groups, and metal-oxygen bonds are found for all of the samples.

**Si-O-Si Asymmetric Stretching (1070–1120 cm⁻¹):**

In all the spectra, the most striking feature is a wide, strong signal in the 1070 to 1120 cm⁻¹ range, characteristic of asymmetric Si-O-Si stretching in silicate tetrahedra. It is observed that a systematic shift of this band towards lower wavenumbers takes place in Flux 14, 19, 21, 25 (Set B) compared with the other fluxes (Set A, Flux 1, 6, 7, 11). There was an average shift in peak position from 1105 cm⁻¹ for Set A to 1085 cm⁻¹ for Set B.

This red shift is quantitatively analysed in terms of increased depolymerization of silicate network, which is described by the fact that the number of Si-O-Si bonds is proportional to the degree of polymerization. Lower wavenumbers indicate a higher concentration of non-bridging oxygen atoms (NBOs), which are the effect of the network modification embedded by the basic oxides (BaO, MnO, CaO).

**Non-Bridging Oxygen Species (950 cm⁻¹):**

The Si-O (non-bridging oxygen) stretching vibrations are assigned to a shoulder near 950 cm⁻¹ that is stronger in Set B samples. The intensity ratio I₉₅₀/I₁₁₀₀ can be used as a semi-quantitative measure to quantify network depolymerization. The average calculated ratio is in the range 0.15–0.25 in Set A, and 0.30–0.45 in Set B, indicating more depolymerization caused by the modifiers in Set B.

**Correlation with Thermal and Anticipated Slag Behavior:**

The depolymerization index obtained from FTIR confirms the trend of positive correlation with the specific heat capacity values obtained from Section 4.3.2. The specific heat capacities of Set B with higher ratio of I₉₅₀/I₁₁₀₀ were in the range of 1.05–1.19 MJ/m³·K, and Set A were in the range 0.90–0.98 MJ/m³·K. The correlation makes good sense on a mechanical ground since the depolymerised silicate networks seem to have more vibration modes and higher configurational entropy than do more polymerised species, thereby providing a better capacity for absorbing heat.

In the previous literature, the action of slag and the dependence of slag viscosity on the extent of network depolymerization is well established, and it is well known that increased network depolymerization will decrease the viscosity of the slag and lower the melting temperature of the slag. Hence, based on the FTIR evidence, it may be reasonably assumed that greater fluidity would be available in the formulations Set B, in particular the formulation Flux 21 and Flux 25, in comparison with the formulations Set A, and thus lower viscosity of the slags would be expected.

**Hydroxyl and Carbonate Species:**

The O-H stretching bands are found in all the spectra and they are of broad band shape with their centre around 3400 cm⁻¹, the intensity of which varies between the different samples (Figure 4.4). These hydroxyl groups are presumably attributable to moisture present on the surface or structural water in the binder (potassium silicate solution) and can affect the weld metal hydrogen content. Higher the hydroxyl band in the Set A samples, the more likely for moisture retention, thus potentially higher the possibility for hydrogen-induced cracking. However, quantitative assessment of hydrogen evolution during welding was beyond the scope of this investigation, and this observation should be considered a qualitative indicator rather than a definitive predictor of weld metal hydrogen content.

**Ti-O and Mn-O Vibrations (400–800 cm⁻¹):**

Titanium dioxide adds characteristic lattice-vibration bands at 400–800 cm⁻¹, whose strength and spectral properties can also be varied depending on which phase is of a lower concentration. The extensive Ti-O vibration envelope is evocative of complex environments of coordination that characterize the multicomponent flux systems. Available literature shows that Ti-O vibration frequencies vary in a systematic way with the decrease in the coordination number when the tetrahedron geometry transforms into an octahedral shape.

The presence of the manganese oxides in the structure adds further lattice modes in the 700–400 cm⁻¹ domain, overlapping Ti-O and Si-O-Si bands; the characteristics increase in proportion to the amount of MnO in the structure, thus indicating changes in the oxidation state. Kim et al. also indicated that the addition of MnO leads to changes in silicate network structure through the provision of free oxygen ions and having a direct effect on thermal and hydrogen dissolution behaviour.

**Si-O-Si Bending Complexes (400–600 cm⁻¹):**

The complementary Si-O-Si bending complexes between 400 and 600 cm⁻¹ indicate the presence of ring structures and three-dimensional network connectivity of the silicate structure; the intensity and structure of these bands are quantitative measures of the extent of polymerization of the network structure, and the influence of the modifier content.

A systematic study of samples Set A (Flux 1, Flux 6, Flux 7, Flux 11) and Set B (Flux 14, Flux 19, Flux 21, Flux 25) showed that there was a strong spectral development which reflects compositional changes in molecular structure. The Si-O-Si asymmetric stretching envelope in Figure 4.4(b) appeared to have systematic shifts to the lower wavenumbers, suggesting that there was more modifier and silicate network depolymerisation. This change in structure is also directly associated with reduced melting temperatures and high slag fluidity.

**Figure 4.4:** FTIR spectra of samples Flux 1, Flux 6, Flux 7, Flux 11 (A) and Flux 14, Flux 19, Flux 21, Flux 25 (B) showing percent transmittance versus wavenumber (4000–500 cm⁻¹). Notable absorption differences observed in fingerprint and functional group regions.




## 4.4 Multi-Pass Bead on Plate Experimentation Using SAW Fluxes

The multi-pass bead-on-plate experimentation represents the critical intermediate step between flux characterization and final butt weld joint fabrication. This stage evaluates the welding performance of all twenty-five laboratory-prepared fluxes under controlled conditions, enabling the assessment of bead morphology, slag detachability, weld metal chemistry, and microhardness prior to selecting the optimal flux compositions for full weldment fabrication.

### 4.4.1 Multi-Pass Bead on Plate Experimentation Using Laboratory Prepared SAW Fluxes

Using the twenty-five laboratory-prepared basic fluxes, multi-pass SAW weld beads were deposited in flat position configuration on API X70 pipeline steel plates having 16 mm thickness. No edge preparation was done for the bead-on-plate experimentation, as the objective was to evaluate flux performance independently of joint geometry effects.

**Filler Wire Selection:**

EA2TiB filler wire with 2.4 mm diameter was utilized without any extra cold feed wire because the rate of wire feed was kept constant to ensure the same amount of metal could be deposited across all 25 flux formulations. This standardization eliminated wire chemistry variation as a confounding factor, allowing the observed differences in weld metal composition to be attributed solely to the slag-metal reactions governed by flux chemistry.

**Welding Parameters:**

A single-wire submerged arc welding (SAW) machine was utilized with the following constant parameters:
- Welding current: 230 A
- Arc voltage: 25 V
- Welding speed: 8 inches/min (3.39 mm/s)
- Heat input: ~1.02 kJ/mm (calculated using Equation 4.5)

The choice of these parameters was based on pre-trial tests to determine bead profile consistency, slag detachability, and absence of surface defects like undercut or over-reinforcement. The heat input value of approximately 1.02 kJ/mm is within the recommended range of 0.8–2.5 kJ/mm for X70 pipeline steel welding to prevent excessive coarsening of the heat-affected zone and to guarantee full flux melting and sufficient reaction time of slag-metal interactions.

**Multi-Pass Deposition Procedure:**

The weld passes were deposited as multipass beads for each flux composition, and in each case, five passes were deposited over the bead. The very first pass was the root/bead-on-plate, and the other four pass depositions were performed following controlled cooling conditions. The interpass temperature was rigorously kept at 120°C to 150°C and monitored at 25 mm distance from the centerline of the weld bead using a contact thermocouple sensor.

This comparatively low level of interpass temperature was maintained to ensure that no coarse grains or martensite would form in the multipass weld metal. Due to this controlled cooling, significant acicular ferrite microstructure was obtained, which is important to achieve the desirable toughness-hardness balance in the multipass welds of API X70 pipeline steel.

Figure 4.5 shows the twenty-five multi-pass SAW beads deposited on the API X70 plate, providing visual evidence of bead morphology variations across the different flux compositions.

**Figure 4.5:** Twenty-five multi-pass SAW beads deposited on API X70 pipeline steel plate using laboratory-prepared fluxes.

**Base Metal and Filler Wire Chemistry:**

Table 4.3 presents the chemical composition of the base metal (API X70 pipeline steel) and filler wire (EA2TiB) used in the SAW bead-on-plate experiments.

**Table 4.3: Chemical composition of base metal and filler wire**

| Material | C | Si | Mn | P | S | Mo | Ni | Cr | Fe |
|----------|------|------|------|-------|-------|-------|-------|-------|------|
| BM (X70) | 0.058 | 0.331 | 1.590 | 0.006 | 0.002 | 0.003 | 0.219 | 0.007 | 98.1 |
| FW (EA2TiB) | 0.03 | 0.078 | 0.781 | 0.020 | 0.005 | 0.317 | 0.090 | 0.042 | 98.8 |

The API X70 steel is a low-carbon (0.058 wt.%) steel with manganese as the primary strengthening element. The filler wire EA2TiB contains titanium and boron additions designed to promote acicular ferrite nucleation in the weld metal through the formation of fine Ti-rich oxide inclusions.

### 4.4.2 Chemical Analysis of Laboratory Prepared SAW Fluxes

To analyze the chemical composition of the weld metal deposited with each flux, atomic absorption spectroscopy (AAS) was employed on each multipass weld bead. The specimen preparation procedure was as follows:

1. An abrasive cut-off wheel was used to make a transverse section (approximately 10 mm thick) of the central area of each bead-on-plate weld without dilution of the base metal or heat-affected zone.
2. The extracted weld metal was ground using SiC abrasive papers (220, 400, 600, 800 and 1200 grit) to remove surface contaminants and any oxide scale.
3. Ultrasonic cleaning was performed using acetone for 10 minutes to ensure complete removal of residual grinding debris.

Table 4.4 presents the complete chemical composition analysis and microhardness measurements for all twenty-five multipass weld beads.

**Table 4.4: Chemical and micro-hardness analysis of multipass beads**

| Flux | C | Si | P | S | Mn | Ni | Cr | Mo | Ti | MH (HV) | CE |
|------|-------|--------|--------|--------|--------|--------|--------|--------|--------|----------|------|
| f1 | 0.0425 | 0.1670 | 0.0121 | 0.0115 | 0.7876 | 0.0100 | 0.0333 | 0.2391 | 0.0025 | 185 | 0.28 |
| f2 | 0.0361 | 0.2325 | 0.0138 | 0.0020 | 0.7854 | 0.0998 | 0.0426 | 0.1923 | 0.0015 | 190 | 0.26 |
| f3 | 0.0412 | 0.2677 | 0.0114 | 0.0020 | 0.6723 | 0.0110 | 0.0304 | 0.2011 | 0.0020 | 200 | 0.24 |
| f4 | 0.0401 | 0.1839 | 0.0112 | 0.0027 | 0.5241 | 0.0896 | 0.0281 | 0.2711 | 0.0021 | 220 | 0.29 |
| f5 | 0.0500 | 0.2120 | 0.0184 | 0.0026 | 0.6729 | 0.0795 | 0.0417 | 0.2042 | 0.0019 | 210 | 0.25 |
| f6 | 0.0503 | 0.1745 | 0.0192 | 0.0036 | 0.6641 | 0.0691 | 0.0336 | 0.2456 | 0.0030 | 178 | 0.19 |
| f7 | 0.0480 | 0.1925 | 0.0174 | 0.0040 | 0.7447 | 0.0688 | 0.0328 | 0.2842 | 0.0022 | 199 | 0.30 |
| f8 | 0.0423 | 0.1554 | 0.0149 | 0.0035 | 0.5448 | 0.0883 | 0.0247 | 0.2225 | 0.0015 | 205 | 0.27 |
| f9 | 0.0483 | 0.1975 | 0.0137 | 0.0022 | 0.6449 | 0.0999 | 0.0267 | 0.2892 | 0.0017 | 195 | 0.25 |
| f10 | 0.0445 | 0.1692 | 0.0116 | 0.0037 | 0.7556 | 0.0105 | 0.0253 | 0.2970 | 0.0012 | 215 | 0.29 |
| f11 | 0.0322 | 0.1571 | 0.0115 | 0.0034 | 0.8813 | 0.0103 | 0.0299 | 0.2151 | 0.0013 | 182 | 0.22 |
| f12 | 0.0456 | 0.1787 | 0.0186 | 0.0030 | 0.8271 | 0.0899 | 0.0230 | 0.2262 | 0.0022 | 191 | 0.24 |
| f13 | 0.0483 | 0.1519 | 0.0108 | 0.0042 | 0.6837 | 0.0103 | 0.0253 | 0.2842 | 0.0024 | 193 | 0.23 |
| f14 | 0.0392 | 0.1517 | 0.0124 | 0.0039 | 0.7608 | 0.0143 | 0.0274 | 0.2183 | 0.0027 | 210 | 0.26 |
| f15 | 0.0462 | 0.1362 | 0.0106 | 0.0024 | 0.6887 | 0.0106 | 0.0276 | 0.2182 | 0.0026 | 226 | 0.31 |
| f16 | 0.0401 | 0.1739 | 0.0119 | 0.0053 | 0.8652 | 0.0107 | 0.0295 | 0.2766 | 0.0011 | 217 | 0.27 |
| f17 | 0.0499 | 0.1327 | 0.0121 | 0.0045 | 0.7110 | 0.0110 | 0.0272 | 0.2923 | 0.0010 | 204 | 0.23 |
| f18 | 0.0488 | 0.1686 | 0.0113 | 0.0057 | 0.8816 | 0.0112 | 0.0218 | 0.2127 | 0.0009 | 200 | 0.22 |
| f19 | 0.0469 | 0.1622 | 0.0130 | 0.0031 | 0.8116 | 0.0106 | 0.0299 | 0.2764 | 0.0023 | 208 | 0.25 |
| f20 | 0.0471 | 0.1480 | 0.0157 | 0.0039 | 0.7590 | 0.0118 | 0.0201 | 0.2610 | 0.0024 | 184 | 0.22 |
| f21 | 0.0416 | 0.1653 | 0.0140 | 0.0040 | 0.8487 | 0.0190 | 0.0218 | 0.2725 | 0.0022 | 210 | 0.28 |
| f22 | 0.0476 | 0.1231 | 0.0120 | 0.0020 | 0.6487 | 0.0170 | 0.0208 | 0.2125 | 0.0025 | 175 | 0.21 |
| f23 | 0.0455 | 0.1453 | 0.0110 | 0.0020 | 0.6587 | 0.0130 | 0.0222 | 0.2223 | 0.0018 | 196 | 0.29 |
| f24 | 0.0483 | 0.1421 | 0.0127 | 0.0118 | 0.9487 | 0.0190 | 0.0238 | 0.2245 | 0.0020 | 189 | 0.25 |
| f25 | 0.0413 | 0.1253 | 0.0152 | 0.0120 | 0.6487 | 0.0193 | 0.0228 | 0.2725 | 0.0019 | 184 | 0.26 |

**Key Observations from Chemical Analysis:**

The carbon content in weld beads ranged from 0.032% to 0.050%, representing a decrease from the base metal value of 0.058%. This reduction is attributed to the oxidizing reactions at the slag-metal interface where carbon is oxidized to CO gas. The manganese content in the weld metal ranged from 0.524% to 0.949%, which is significantly lower than the base metal (1.590%) but higher than the filler wire (0.781%), indicating that some manganese transfer occurs from the MnO in the flux through slag-metal reactions.

The titanium content in the weld metal ranged between 0.0009% and 0.0030% (9–30 ppm) for all 25 multipass beads. This is a highly significant range for acicular ferrite microstructure formation. When Ti is present in this optimal low concentration range, it forms fine, dispersed Ti-rich oxide particles (primarily complex MnO-Al₂O₃-SiO₂-TiO₂ oxides containing MnTiO₃) in the molten weld pool during solidification. These inclusions serve as intragranular nucleation sites for acicular ferrite, which is a fine-grained interlocking microstructure known to provide high toughness and strength.

The carbon equivalent (CE) values ranged from 0.19 to 0.31 across the 25 formulations, calculated using the IIW formula. These values fall within acceptable limits for API X70 pipeline steel applications, where CE must remain below 0.43 to ensure adequate weldability and avoid cracking.

**Regression Model Development:**

Using the observed values of chemical composition, regression equations were formed in terms of percentage compositions of flux ingredients. Single, second-order, and third-order regression models were developed in terms of flux mixtures using Scheffé canonical mixture models:

**Equation 4.9 (Linear mixture model):**
$$\hat{y} = \sum_{i=1}^{q} \beta_i t_i$$

**Equation 4.10 (Quadratic mixture model):**
$$\hat{y} = \sum_{i=1}^{q} \beta_i t_i + \sum_{i<j}^{q} \beta_{ij} t_i t_j$$

**Equation 4.11 (Special cubic mixture model):**
$$\hat{y} = \sum_{i=1}^{q} \beta_i t_i + \sum_{i<j}^{q} \beta_{ij} t_i t_j + \sum_{i<j<k}^{q} \beta_{ijk} t_i t_j t_k$$

where ŷ represents the predicted response (such as chemical composition, microhardness, or carbon equivalent), β_i are linear coefficients, β_ij represent binary interaction effects, and β_ijk represent ternary interaction effects among flux components.

The coefficient vector was obtained using:

**Equation 4.12:**
$$\boldsymbol{\beta} = (X^T X)^{-1} X^T y$$

where X is the design matrix and y is the vector of experimental responses.

The adequacy of predicted equations was cross-verified using ANOVA technique. All the flux mixture models in terms of percentage composition and microhardness were verified for respective formed models such as linear, quadratic, and cubic by finding F and P values at 95% confidence level. Statistically significant regression models with R² values ranging from 0.76 to 0.95 (p < 0.05) were developed to predict elemental transfer and mechanical properties.

Table 4.5 presents the ANOVA results for all the responses, confirming the statistical significance of the developed models.

**Table 4.5: Summary of ANOVA results for regression models**

| Response | Model Type | R² | F-value | P-value | Significance |
|----------|-----------|------|---------|---------|--------------|
| C | Special Cubic | 0.88 | 2.02 | 0.0318 | Significant |
| Si | Quadratic | 0.81 | 2.32 | 0.0050 | Significant |
| Mn | Special Cubic | 0.90 | 3.63 | 0.0228 | Significant |
| P | Special Cubic | 0.94 | 1.23 | 0.0123 | Significant |
| S | Quadratic | 0.76 | 2.22 | 0.0310 | Significant |
| Mo | Special Cubic | 0.95 | 3.10 | 0.0030 | Significant |
| Ni | Quadratic | 0.82 | 2.28 | 0.0230 | Significant |
| Cr | Special Cubic | 0.91 | 2.63 | 0.0444 | Significant |
| MH | Quadratic | 0.92 | 2.36 | 0.0452 | Significant |
| CE | Special Cubic | 0.89 | 2.20 | 0.0318 | Significant |

The predicted values agree well with the experimental data, as visually confirmed with the similar location of points to the diagonal in the predicted versus actual plots (Figure 4.6), indicating the existence of a very good goodness of fit.

**Figure 4.6:** Predicted versus actual values for the chemical composition variables and mechanical properties obtained for (a) Carbon (C), (b) Silicon (Si), (c) Phosphorus (P), (d) Sulphur (S), (e) Manganese (Mn), (f) Nickel (Ni), (g) Chromium (Cr), (h) Molybdenum (Mo), (i) Microhardness (MH), and (j) Carbon Equivalent (CE).

**Role of Flux Constituents on Weld Metal Chemistry:**

During the slag-metal reactions of submerged arc welding, free oxygen ions (O²⁻) play a key role in controlling element transfer and elemental chemistry of the weld metal. Basic compounds such as CaO, BaO and MnO of the flux dissociate in the molten slag to produce O²⁻ ions, which are strong electron donors that alter the chemical potential of oxygen at the slag-metal interface. The equilibria of reactions are altered by these free O²⁻ ions by stabilizing the cationic species, transferring them into the weld pool, while simultaneously lowering the oxygen concentration in the metal.

The basic oxidation and alloying reactions occurring in the slag-metal system of submerged arc welding include:

**Equation 4.13:** SiO₂ (slag) ⇌ [Si] (metal) + 2[O] (metal)

**Equation 4.14:** MnO (slag) ⇌ [Mn] (metal) + [O] (metal)

**Equation 4.15:** [S] (metal) + O²⁻ (slag) ⇌ S²⁻ (slag) + [O] (metal)

**Equation 4.16:** CO (gas) + O²⁻ (slag) ⇌ CO₃²⁻ (slag)

Individual flux ingredients such as SiO₂ and MnO were identified as having a positive effect on carbon content, while their interaction effects with other components may produce either negative or positive influences. Elevated CaO (and BaO) contents increase C, Mn, P, and Mo content of weld metal as a result of the availability of free O²⁻ ions to shift equilibria in favor of element recovery. Binary products such as CaO·SiO₂ form stable complexes reducing element transfer, as supported by the negative interaction coefficients.

The sensitivity of each element to individual flux constituents is well illustrated in Trace (Piepel) plots (Figure 4.7). In a mixture design study, a Trace (Piepel) plot illustrates sensitivity of a predicted response to each component in a mixture. Every trace curve represents the path along which the proportion of a single component is varied incrementally along the Piepel direction from the reference blend (overall centroid, Flux F25: SiO₂ = 5.0, TiO₂ = 20.0, CaF₂ = 35.0, BaO = 9.3, MnO = 15.7, CaO = 8.0 wt.%) to the vertex where that component is increased to the maximum allowable proportion.

**Figure 4.7:** Trace (Piepel) plots showing the effect of deviation of individual mixture components from the reference blend on predicted chemical composition and mechanical properties for (a) C, (b) Si, (c) P, (d) S, (e) Mn, (f) Ni, (g) Cr, (h) Mo, (i) microhardness (MH), and (j) carbon equivalent (CE).

The three-dimensional response surface plots (Figure 4.8) provide a comprehensive visualization of the complex multi-variable relationships between flux composition and weld metal properties.

**Figure 4.8:** Three-dimensional mixture surface and contour plots illustrating the effect of components A, B, and C on predicted chemical composition and mechanical responses across the triangular mixture space for (a) C, (b) Si, (c) P, (d) S, (e) Mn, (f) Ni, (g) Cr, (h) Mo, (i) microhardness (MH), and (j) carbon equivalent (CE).

### 4.4.3 Microhardness Measurement of Beads

Microhardness of all twenty-five beads was analysed using a Vickers microhardness tester with 50 kgf load and 10 sec dwell time. The microhardness values ranged from 175 to 226 HV across all formulations (Table 4.4).

The minimum physical requirements for X70 pipeline steel welds typically exhibit a microstructure of acicular ferrite with bainite to provide the best toughness and strength. The microhardness of weld metal and HAZ should be maintained at 180–220 HV to prevent brittleness and maintain weldability while avoiding cracking.

The results showed that:
- F4 optimized flux yielded the highest microhardness of 220 HV with a CE of 0.29 and fine acicular ferrite microstructure
- F15 flux achieved 226 HV, the maximum among all formulations
- F22 flux gave the lowest microhardness value of 175 HV with a CE of 0.21
- The majority of flux formulations produced weld metals within the desired 180–220 HV range

The microhardness results correlate directly with the weld metal chemistry, particularly the manganese and molybdenum content, which influence solid solution strengthening and phase transformation behavior. Higher Mo content (as in Flux 4 and Flux 10) promoted the formation of fine acicular ferrite and bainitic structures contributing to increased hardness.

### 4.4.4 Selection of Adequate Fluxes by Qualitatively Analysing Multi-Pass Beads

Following the multi-pass bead-on-plate experimentation, all twenty-five different beads were visually examined (Figure 4.5) to assess the following criteria:

1. **Bead morphology:** The uniformity, width consistency, and surface appearance of each weld bead
2. **Porosity:** Presence or absence of surface pores and gas entrapment
3. **Slag detachability:** The ease with which the solidified slag could be removed from the weld bead surface

Based on this preliminary screening combined with the quantitative analysis of microhardness, carbon equivalent, and microstructural evaluation, three fluxes from the present basic flux system were selected for further investigation. The selection criteria were:
- Good bead morphology (uniform, consistent width, smooth surface)
- Minimum porosity (no visible pores or gas pockets)
- Satisfactory slag detachability characteristics (easy, complete slag removal)
- Microhardness within the acceptable range (180–220 HV)
- Carbon equivalent within pipeline steel specifications (CE < 0.43)
- Evidence of desirable acicular ferrite microstructure

Consequently, fluxes with the designation F6B, F20B, and F22B belonging to the basic system were selected for preparing final submerged arc weld joints. The performance and characteristics of these three selected laboratory-prepared fluxes were then evaluated by comparing the weld joints made with them against a reference weld joint fabricated using a commercial flux (designated as C.F.).

**Microstructural Evaluation of Selected Beads:**

The microstructure of selected weld beads was examined using standard metallographic techniques, which involved sequential grinding with ascending grits of emery paper, followed by polishing with diamond paste to achieve a mirror-like surface finish. The polished specimens were etched with 2% Nital solution for microstructural revelation.

Figure 4.9 shows the microstructure of multi-pass beads for selected flux compositions:

- **Flux 4 (Figure 4.9a):** Shows predominantly acicular ferrite microstructure with uniformly distributed carbide inclusions, indicating optimal flux chemistry for nucleation of intragranular ferrite
- **Flux 10 (Figure 4.9b):** Displays ferrite matrix with carbide precipitates and dendritic skeleton structures
- **Flux 11 (Figure 4.9c):** Exhibits ferrite with distributed carbide particles throughout the matrix
- **Flux 20 (Figure 4.9d):** Shows ferrite with acicular ferrite regions and carbide inclusions
- **Flux 22 (Figure 4.9e):** Demonstrates acicular ferrite (AF) with carbide inclusions distributed throughout the weld metal

**Figure 4.9:** Microstructure of multi-pass beads in SAW; (a) Flux no.4; (b) Flux no.10; (c) Flux no.11; (d) Flux no.20; (e) Flux no.22.

The control of flux chemistry can be translated directly into microstructural changes. Higher basicity because of the CaO and MnO additions favours the formation of a fine acicular ferrite with dispersed carbide and oxide inclusions that have a high Mn, Cr and Ti content. TiO₂ in particular has been known to produce fine Ti-bearing inclusions which strongly nucleate acicular ferrite. The present welds have acicular ferrite matrices and carbide inclusions which are uniformly distributed, consistent with previous work in which the chemistry of the inclusions is correlated with acicular ferrite fraction.

In contrast, flux combinations that are rich in SiO₂ and CaF₂ produce more cementitic (coarser ferrite/bainitic structure) weld metal with less effectual inclusions and higher levels of retained impurities (P, S), trends as expected from previous submerged arc research where more acidic slags resulted in reduced acicular ferrite content.




## 4.5 Materials and Experimental Setup

### 4.5.1 Submerged Arc Welding Using Adequate Fluxes for Various Characterizations

Following the systematic screening process described in Section 4.4.4, three laboratory-prepared basic fluxes (F6B, F20B, and F22B) were selected for the fabrication of full butt weld joints on API X70 pipeline steel. These fluxes were chosen based on their demonstrated performance in the bead-on-plate experiments, specifically their good bead morphology, minimum porosity, satisfactory slag detachability, and acceptable microhardness and carbon equivalent values. A commercial flux (designated as C.F.) was used as a reference standard for comparison purposes.

**Base Material Specification:**

The base material used for all weld joint fabrication was API 5L X70 pipeline steel, which is a high-strength low-alloy (HSLA) steel specifically designed for high-pressure transmission pipelines. API X70 provides a specified minimum yield strength of 485 MPa and an excellent combination of strength, ductility, and weldability. The selection of API X70 for this research is justified by its extensive use in modern pipeline infrastructure for demanding applications including deep-water offshore pipelines, seismically active regions, and arctic environments.

The characteristics of API X70 steel are attained by a complex metallurgical design, which in most cases consists of ultra-low carbon content and a complex microstructure of acicular ferrite, bainitic-ferritic phases, and finely dispersed martensite-austenite (MA) constituents. The thermo-mechanical controlled processing (TMCP) method employed in its manufacture guarantees a fine-grained structure with both strength and sufficient deformability. The presence of micro-alloying elements like Nb, Ti, and V in API X70 helps to refine the austenite grain size and induce the formation of acicular ferrite, which increases both the strength and the low-temperature toughness.

**Filler Wire Specification:**

EA2TiB filler wire with 2.4 mm diameter was used for all weld joint fabrication. This wire contains controlled amounts of titanium and boron, which are added to promote fine Ti-bearing oxide inclusions that serve as heterogeneous nucleation sites for acicular ferrite in the weld metal. The wire composition is given in Table 4.6.

Table 4.6 presents the complete chemical analysis of the parent metal, filler wire, and weld metal compositions for all four weld joints.

**Table 4.6: Chemical analysis of parent metal, filler wire, and weld metal**

| S.No | %C | %Si | %Mn | %P | %S | %Cr | %Mo | %Ni | %Cu | %Nb | %Ti | %Fe | %CE |
|------|-------|-------|------|--------|--------|-------|-------|-------|--------|-------|------|-------|------|
| X70 | 0.059 | 0.331 | 1.70 | 0.0068 | 0.0032 | 0.007 | 0.002 | 0.299 | 0.0061 | 0.062 | 0.02 | 97.50 | 0.33 |
| FW | 0.028 | 0.089 | 0.92 | 0.0112 | 0.0080 | 0.042 | 0.312 | 0.091 | 0.1501 | 0.025 | 0.01 | 98.31 | 0.25 |
| C.F | 0.059 | 0.374 | 1.62 | 0.0164 | 0.0070 | 0.039 | 0.412 | 0.068 | 0.0810 | 0.008 | 0.02 | 97.29 | 0.38 |
| F6B | 0.042 | 0.397 | 0.80 | 0.0119 | 0.0024 | 0.029 | 0.392 | 0.052 | 0.0701 | 0.006 | 0.02 | 98.17 | 0.31 |
| F20B | 0.051 | 0.441 | 0.67 | 0.0211 | 0.0019 | 0.030 | 0.401 | 0.049 | 0.0699 | 0.012 | 0.03 | 98.22 | 0.28 |
| F22B | 0.061 | 0.451 | 0.71 | 0.0222 | 0.0011 | 0.022 | 0.355 | 0.050 | 0.0555 | 0.018 | 0.02 | 98.23 | 0.27 |

Key observations from Table 4.6:
- The sulfur content in all weld joints was reduced considerably compared to the base material, filler wire, and commercial flux, indicating effective desulfurization by the basic flux constituents
- Maximum carbon equivalent (CE = 0.38 wt.%) was observed for the weld joint fabricated using the commercial flux
- Specimen F6B's CE (0.31) was closest to the base metal CE (0.33)
- Lower CE values in F20B (0.28) and F22B (0.27) fluxes indicate improved weldability
- Ni and Nb content in the weld metal was reduced compared to the parent metal, while substantial amounts of Ti, B, Cu, and Cr (carbide formers) were gained from the filler wire

### 4.5.2 Formation of Weld Coupon

API X70 steel base plates of dimension 140 mm × 140 mm × 22 mm were prepared for butt welding. The joint configuration was a single-V groove with the following specifications:
- Groove angle: 60°
- Root gap: 2 mm
- Root face: 2 mm
- Plate thickness: 22 mm

Figure 4.10 shows the schematic representation of the butt weld joint configuration used for all welding experiments.

**Figure 4.10:** Schematic representation of butt weld joint configuration showing 60° groove angle, 2 mm root gap, and 2 mm root face on 22 mm thick API X70 plates.

The plates were cleaned of mill scale, rust, and surface contaminants prior to welding using grinding and solvent degreasing. Tack welds were placed at both ends of the plates to maintain alignment and root gap during welding. Run-on and run-off tabs were attached to ensure steady-state welding conditions throughout the entire joint length.

### 4.5.3 Submerged Arc Welding of Plates

All experimental welding was conducted with direct current electrode positive (DCEP) polarity using a single-wire submerged arc welding machine. The welding parameters for the butt joint fabrication were:
- Welding current: 440 A
- Arc voltage: 28 V
- Welding speed: 13 inches/min
- Contact tip-to-work distance (CTWD): 20 mm
- Polarity: DCEP
- Electrode: EA2TiB, 2.4 mm diameter

These parameters were determined after preliminary test welds conducted to qualitatively test the bead profile, porosity, and slag detachability, with each parameter rated on a low, medium, or high scale. The selected parameters ensured complete joint penetration, adequate fusion, and acceptable bead geometry for all flux compositions.

A total of four weld joints were fabricated:
1. Weld joint using F6B flux (laboratory-prepared basic flux no. 6)
2. Weld joint using F20B flux (laboratory-prepared basic flux no. 20)
3. Weld joint using F22B flux (laboratory-prepared basic flux no. 22)
4. Weld joint using C.F. (commercial flux — reference standard)

Multiple passes were required to fill the V-groove joint, with interpass temperature monitored and controlled between 120°C and 150°C using contact thermocouple measurements. Slag was completely removed between passes using chipping hammer and wire brush to prevent slag entrapment. Each successive pass was deposited only after confirming that the previous pass was free from visible defects such as cracks, porosity, or undercut.

### 4.5.4 Weld Specimen Cutting

Following weld fabrication, the comprehensive mechanical and microstructural characterization was conducted on all four weld joints. Specimens were extracted from the welded plates using wire electrical discharge machining (EDM) or abrasive cut-off wheels to minimize heat-affected distortion of the specimens during cutting. The following specimens were extracted from each weld joint:

1. **Tensile test specimens:** Transverse tensile specimens machined according to ASTM E8 standard
2. **Impact test specimens:** Standard Charpy V-notch specimens (10 mm × 10 mm × 55 mm) extracted from both the fusion zone and heat-affected zone
3. **Microhardness specimens:** Cross-sectional specimens polished to mirror finish
4. **Metallographic specimens:** Cross-sectional samples for optical microscopy
5. **Fractography specimens:** Broken halves of impact specimens for SEM analysis
6. **Corrosion specimens:** Samples prepared for electrochemical testing

All specimens were identified with flux designation and zone location (fusion zone, HAZ, or base metal) to enable systematic comparison of results across the four weld joints.

### 4.5.5 Weld Specimen Mechanical Characterization

#### 4.5.4.1 Weld Specimen Tensile Testing

Transverse tensile testing was conducted to evaluate the overall joint strength and determine whether the weld joints met the minimum mechanical requirements specified for API X70 pipeline steel. The minimum physical requirements for X70 pipeline steel welds include:
- Yield strength (or 0.2% proof stress): ≥ 485 MPa
- Ultimate tensile strength: ≥ 570 MPa

Tensile specimens were machined from the welded plates in the transverse direction (perpendicular to the welding direction) so that the gauge length encompasses the weld metal, both HAZ regions, and parent metal. Testing was performed on a universal testing machine at a constant crosshead speed in accordance with ASTM E8 standard specifications.

The fracture location, yield strength, ultimate tensile strength, percentage elongation, and reduction in area were recorded for each specimen. Specimens that fractured in the weld metal or HAZ were noted as these indicate potential weak regions requiring further investigation.

#### 4.5.4.2 Weld Specimen Impact Testing

Impact toughness testing was performed using the Charpy V-notch (CVN) method to evaluate the resistance of the weld joints to sudden fracture under dynamic loading conditions. This is a critical property for pipeline applications where resistance to brittle fracture at low temperatures is essential for safe operation.

Standard Charpy V-notch specimens (10 mm × 10 mm × 55 mm with a 2 mm deep, 45° V-notch) were extracted from both the fusion zone (FZ) and heat-affected zone (HAZ) of each weld joint. Testing was conducted at two temperatures:
- Room temperature (~25°C)
- Low temperature (-55°C)

The low-temperature testing at -55°C is particularly relevant for pipeline applications in arctic environments and for sour gas service conditions where low-temperature toughness is a critical design requirement.

Table 4.7 presents the impact toughness measurements for the parent metal and all four weld joints at both testing temperatures.

**Table 4.7: Impact toughness values**

| S.No | Specimen | Weld Metal Impact Toughness (J) | | HAZ Impact Toughness (J) | |
|------|----------|------|------|------|------|
| | | Room temp. | -55°C | Room temp. | -55°C |
| 1 | Parent metal | 350 | 35 | — | — |
| 2 | F6B | 171 | 21 | 385 | 28 |
| 3 | F20B | 125 | 11 | 355 | 19 |
| 4 | F22B | 131 | 14 | 360 | 20 |
| 5 | CF | 159 | 18 | 390 | 30 |

Key observations from Table 4.7:
- The base metal exhibited the highest impact toughness at both room temperature (350 J) and -55°C (35 J)
- The F6B flux weld joint exhibited greater impact toughness (171 J at room temperature and 21 J at -55°C) than other laboratory flux weld joints and also exceeded the commercial flux (159 J at room temperature and 18 J at -55°C)
- Weld joints fabricated using F20B and F22B fluxes showed moderate impact toughness values, but lesser than the parent metal and commercial flux
- All weld specimens showed increased impact strength in the HAZ at room temperature compared to the fusion zone, which is attributed to grain refinement effects in the fine-grained HAZ
- The F6B flux specimen experienced the highest impact strength in the HAZ at both room temperature (385 J) and -55°C (28 J)

Figure 4.11 illustrates the variation of impact energy of different weld joints at room temperature and -55°C for both the fusion zone and HAZ regions.

**Figure 4.11:** Impact toughness values for various fluxes showing weld metal and HAZ impact energy at room temperature and -55°C.

The flux constituents play a major role in the impact strength of the weld metal depending on the nature of the flux (acidic, basic, or neutral). The amount of oxygen in the weld metal is based on the kind of flux applied and hence affects the final mechanical properties. High impurities of weld metal oxygen that may be caused by a mixture of acidic flux constituents (such as SiO₂ and Al₂O₃) or by the atmosphere grossly interfere with impact toughness. Basic fluxes offer better impact properties than acidic fluxes through the addition of fluorides or strong oxides, which decrease the oxygen content in weld metal.

The excellent performance of the F6B flux weld joint resulting from its basic characteristics is supported by the fundamental understanding that optimized basic flux design, in particular those containing TiO₂, can maximize the Charpy impact energy due to increased formation of acicular ferrite and control of inclusion characteristics. The laboratory-prepared fluxes (F6B, F20B, and F22B) encourage lower oxygen pickup, finer inclusions, and acicular ferrite formation, which improves toughness even at sub-zero temperatures.

#### 4.5.4.3 Fractography Analysis of Weld Specimen

Fractography analysis of impact-tested specimens was performed using scanning electron microscopy (SEM) to characterize the fracture mechanisms operating in the parent metal, heat-affected zone, and fusion zone. SEM examination was conducted at 15.0 kV accelerating voltage with working distances of 11–15 mm at 1,000× magnification.

The fractography of impact-tested specimens indicates the complex interaction of welding flux chemistry, microstructure, and fracture mechanisms within the parent metal (PM), heat-affected zone (HAZ), and fusion zone (FZ). Systematic fractographic analysis proves that these regions show different failure modes under impact loading, which is directly related to their specific microstructural features and to the welding flux used.

**Parent Metal Fractography (Figure 4.12a):**

The parent metal fracture surface revealed ductile fracture features including microvoid coalescence and well-developed dimple structures. The parent metal has the highest impact toughness, and the fracture surface exhibited extensive plastic deformation before failure, with deep equiaxed dimples indicative of high energy absorption capacity. Evidence of ductile rupture, voids, facet tearing, and micro voids were all observed, confirming the high toughness of the TMCP-processed base material.

**Fusion Zone Fractography:**

The fusion zone had the most complicated fractographic features and had the lowest impact toughness compared to the parent metal and HAZ region.

*F6B Flux — Room Temperature (Figure 4.12b):* The F6B basic flux demonstrated excellent performance with 171 J impact toughness in the weld zone at room temperature. Fractography revealed a mixture of ductile features including ductile fracture zones, facets, sharp tearing, and fibrous dimples, indicating a combined ductile-brittle failure mode with predominantly ductile character.

*F6B Flux — -55°C (Figure 4.12c):* At -55°C, brittle fracture with some facet tore surfaces was observed. Facets ridges, fibrous rupture, brittle rupture zones, and uneven tearing were identified, consistent with the transition from ductile to brittle behavior at reduced temperatures.

*F20B Flux — Room Temperature (Figure 4.12d):* The F20B flux produced fusion zone fracture surfaces with sharp dendrites, ductile fraction regions, and fibrous rupture areas, showing mixed-mode fracture.

*F20B Flux — -55°C (Figure 4.12e):* At low temperature, larger facet tearing, river patterns, uneven ridges, and brittle surfaces were observed, indicating lower fracture resistance.

*F22B Flux — Room Temperature (Figure 4.12f):* F22B showed facets, micro voids, small dimples, and cleavage facets at room temperature, indicating a transition behavior.

*F22B Flux — -55°C (Figure 4.12g):* At -55°C, ridges, facets, brittle rupture, and cleavage facets dominated, indicating predominantly brittle failure.

*Commercial Flux — Room Temperature (Figure 4.12h):* The commercial flux showed ductile rupture, voids, uneven surface, micro void, and fibrous dimples, demonstrating good ductile fracture characteristics.

*Commercial Flux — -55°C (Figure 4.12i):* At -55°C, river patterns, uneven ridges, facets, and dimples were observed in the commercial flux weld zone.

**HAZ Fractography:**

The HAZ exhibited transitional fractographic behaviour between the parent metal and fusion zone. The coarse-grained HAZ (CGHAZ) adjacent to the fusion line had the most brittle characteristics related to cleavage fracture with martensite-austenite (M-A) constituents and large multi-austenite grains.

*F6B HAZ — Room Temperature (Figure 4.12j):* Fractographic analysis showed facets, sharp ridges, brittle rupture, void, and irregular surface features, indicating mixed-mode fracture with some brittle regions.

*F6B HAZ — -55°C (Figure 4.12k):* At -55°C, cleavage crack, macro void, facets, and brittle rupture were observed, but with more ductile features compared to other fluxes at the same temperature.

*Commercial Flux HAZ — Room Temperature (Figure 4.12l):* River pattern, fibrous dimples, ductile rupture, uneven surface, and facet ridges were identified.

*Commercial Flux HAZ — -55°C (Figure 4.12m):* Facets, voids, ductile tearing, cleavage crack, and micro voids were observed.

Fractographic analysis of HAZ specimens from welds made with basic fluxes (F6B) and commercial fluxes (CF) showed an improvement in toughness with an increased ductile fracture area compared to other fluxes. The F6B flux gave 385 J impact energy in the HAZ at room temperature while 28 J at -55°C, with fractography demonstrating intense microvoid coalescence. The effect of inclusions on the HAZ fractography depends significantly on the nature of the inclusions: fine-sized, well-dispersed inclusions refine the HAZ microstructure and favour ductile fracture, whereas large-sized clustered inclusions lead to grain coarsening and cleavage-dominated failure.

**Figure 4.12:** Fractographs of API X70 SAW weldments in parent, fusion zone and HAZ region: (a) Parent metal, (b) F6B fusion zone at room temperature, (c) F6B fusion zone at -55°C, (d) F20B fusion zone at room temperature, (e) F20B fusion zone at -55°C, (f) F22B fusion zone at room temperature, (g) F22B fusion zone at -55°C, (h) CF fusion zone at room temperature, (i) CF fusion zone at -55°C, (j) F6B HAZ at room temperature, (k) F6B HAZ at -55°C, (l) CF HAZ at room temperature, (m) CF HAZ at -55°C.

#### 4.5.4.4 Weld Specimen Microhardness Testing

Assessment of microhardness of API X70 SAW joints using different fluxes identifies a complex interaction of flux basicity and other factors such as weld-metal composition and the effect of thermal cycles on microstructural modifications in parent material, weld metal, and heat-affected zone (HAZ). Microhardness measurements were performed using a Vickers microhardness tester across the weld cross-section, traversing from base metal through the HAZ to the fusion zone center and then back through the HAZ to the base metal on the opposite side.

The testing parameters were:
- Load: 500 gf (HV0.5) for cross-sectional profiles
- Dwell time: 10 seconds
- Spacing between indentations: 0.5 mm
- Standard: ASTM E384

The as-received API X70 steel has a fine-grained ferrite-pearlite microstructure with a microhardness range of 190–220 HV, giving it a balanced strength-toughness relationship suitable for high-pressure applications.

Table 4.8 presents the microhardness values of the fusion zone and heat-affected zone of SAW weldments using laboratory-prepared and commercial fluxes.

**Table 4.8: Microhardness of SAW weldments in FZ and HAZ regions**

| Flux | Max./Min. | Fusion Zone (FZ) | HAZ |
|------|-----------|------------------|-----|
| F6B | Max. value | 224 | 251 |
| | Min. value | 205 | 208 |
| F20B | Max. value | 215 | 229 |
| | Min. value | 195 | 201 |
| F22B | Max. value | 202 | 225 |
| | Min. value | 184 | 205 |
| CF | Max. value | 233 | 257 |
| | Min. value | 210 | 211 |

Key observations from Table 4.8:
- The commercial flux (CF) shows the highest hardness values in both the fusion zone (210–233 HV) and HAZ (211–257 HV)
- F6B welded joints generally have a medium but steady distribution of microhardness in the weld metal (205–224 HV), which can be explained by the prevailing presence of acicular ferrite and fine-dispersed bainitic constituents
- F20B and F22B, which contain more CaO/CaF₂-rich formulations, form more averagely lower weld-metal hardness (195–215 HV for F20B and 184–202 HV for F22B), as a result of enhanced deoxidation and microstructural refinement
- All flux compositions show a slight increase in hardness in the HAZ region compared to the fusion zone, due to excessive thermal cycling of this region during welding
- The maximum HAZ hardness values (225–257 HV) remain below the critical threshold of 350 HV that would indicate susceptibility to hydrogen-induced cracking

Laboratory-prepared basic fluxes such as F6B, F20B, and F22B tend to deposit more basic weld metal that encourages slag-metal interactions to minimize oxygen and hydrogen atoms in the weld and refine the weld-metal microstructure while inhibiting coarse martensite and fresh bainite development in the fusion zone. The microhardness profile in the HAZ is highly determined by the highest temperature and the rate of cooling that is predetermined by the heat input of the SAW and the stability of the flux arc. A slight increase in hardness of the coarse-grained HAZ (CGHAZ) near the fusion line is often moderate because of martensite-austenite (M-A) constituents and fine bainite formed by rapid cooling.

#### 4.5.4.5 Weld Specimen Microstructure Analysis

The microstructural behavior of API X70 submerged arc welding (SAW) weldments, especially in the fusion zone (FZ) and the heat-affected zone (HAZ), is critically controlled by the flux system used. High-basicity fluxes such as F6B, F20B, and F22B yield a much evolved and desirable microstructural evolution compared to neutral or acidic commercial SAW fluxes.

**Specimen Preparation:**

Metallographic specimens were prepared by standard techniques involving:
1. Mounting in epoxy resin for handling convenience
2. Sequential grinding with SiC abrasive papers (220, 400, 600, 800, 1200, and 2000 grit)
3. Polishing with diamond paste (6 μm followed by 1 μm) to achieve mirror-like surface finish
4. Etching with 2% Nital (2% nitric acid in ethanol) for 5–10 seconds to reveal the microstructure
5. Optical microscopy examination at 50× magnification

**Parent Metal Microstructure (Figure 4.13a):**

The as-received API X70 parent metal exhibits a fine-grained ferrite-pearlite microstructure characteristic of TMCP-processed pipeline steel. The ferrite grains are equiaxed with an average grain size of approximately 5–10 μm, and the pearlite colonies are uniformly distributed at grain boundaries. This microstructure provides the balanced combination of strength and toughness required for pipeline applications.

**Fusion Zone Microstructure:**

In the fusion zone, where welding metal solidifies directly from the molten state, the basicity of the flux determines the oxygen potential and the inclusion population. High-basicity fluxes containing high fractions of basic oxides (CaO, BaO) relative to acidic oxides (SiO₂, TiO₂) create a low-oxygen atmosphere that causes a decrease in the fraction of oxide inclusions and favours the development of finely dispersed complex inclusions rich in titanium. These inclusions become preferable nucleation centres for acicular ferrite (AF), an intergranular microstructure composed of fine non-aligned laths of ferrite, having exceptional resistance to cleavage fracture.

*F6B Fusion Zone (Figure 4.13b):* The fusion zone produced with F6B flux shows predominantly acicular ferrite (AF) with polygonal ferrite (PF) and minor pearlite (P) constituents. The acicular ferrite laths are fine, interlocking, and randomly oriented, providing excellent crack arrest capability. This microstructure is responsible for the high impact toughness observed (171 J at room temperature).

*F20B Fusion Zone (Figure 4.13d):* The F20B flux produced a fusion zone containing acicular ferrite (AF), Widmanstätten ferrite (WF), martensite-austenite (M/A) constituents, and lower bainite (LB). The presence of M/A constituents indicates somewhat higher hardenability compared to F6B.

*F22B Fusion Zone (Figure 4.13f):* The F22B flux fusion zone displays acicular ferrite (AF), polygonal ferrite (PF), pearlite (P), and side-plate ferrite (SF). This more diverse phase distribution contributes to the slightly lower but still acceptable hardness values.

*Commercial Flux Fusion Zone (Figure 4.13h):* The commercial flux produced a fusion zone with polygonal ferrite (PF), pearlite (P), and lath ferrite (LF). The presence of larger polygonal ferrite grains indicates less grain refinement compared to the laboratory basic fluxes, though the overall mechanical properties remained acceptable.

**Heat-Affected Zone Microstructure:**

The HAZ undergoes a complex thermal cycle without melting and shows microstructural changes with similar sensitivity to the choice of flux but through indirect mechanisms. The HAZ for API X70 steel is normally composed of several sub-regions: the coarse-grained HAZ (CGHAZ) adjacent to the fusion line experiencing peak temperatures and austenite grain coarsening, and the fine-grained HAZ (FGHAZ) experiencing normalizing temperatures.

*F6B HAZ (Figure 4.13c):* The HAZ of F6B weldment shows grain boundary ferrite (GBF), quenched polygonal ferrite (QPF), and martensite-austenite (M/A) constituents. The M/A phase appears as small islands at grain boundaries and triple points, which contribute to the increased hardness observed in the HAZ (up to 251 HV).

*F20B HAZ (Figure 4.13e):* The F20B HAZ exhibits Widmanstätten ferrite (WF), martensite-austenite (M/A), and lower bainite (LB). The presence of WF indicates higher peak temperatures experienced in this region.

*F22B HAZ (Figure 4.13g):* The F22B HAZ shows grain boundary ferrite (GBF), Widmanstätten ferrite (WF), and quenched polygonal ferrite (QPF). The coarser microstructural features correlate with the lower hardness values observed.

*Commercial Flux HAZ (Figure 4.13i):* The commercial flux HAZ displays quenched polygonal ferrite (QPF), martensite-austenite (M/A), upper bainite (UB), Widmanstätten ferrite (WF), and additional M/A islands. The presence of upper bainite and multiple M/A islands contributes to the highest HAZ hardness among all specimens (257 HV maximum).

Weldments produced with basic fluxes (F6B, F20B, F22B, and CF) have fusion zones made up mostly of acicular ferrite with small amounts of polygonal ferrite and bainite. It has been observed that fluxes with lower basicity indices or with rutile-based compositions give higher weld metal oxygen concentration, which causes a coarser inclusion distribution and the formation of less desirable microstructures such as grain boundary ferrite (GBF) and Widmanstätten ferrite (WF).

The CGHAZ of API X70 welds produced with basic fluxes typically shows a microstructure of bainite and acicular ferrite. These are undesirable phases developed during solidification of SAW weldments and can be reduced by using highly basic fluxes with controlled heat input.

**Figure 4.13:** Microstructure analysis of API X70 SAW welds fabricated using different fluxes: (a) Parent metal showing ferrite and pearlite, (b) F6B fusion zone showing PF, AF, and P, (c) F6B HAZ showing GBF, QPF, and M/A, (d) F20B fusion zone showing AF, WF, M/A, and LB, (e) F20B HAZ showing WF, M/A, and LB, (f) F22B fusion zone showing AF, PF, P, and SF, (g) F22B HAZ showing GBF, WF, and QPF, (h) CF fusion zone showing PF, P, and LF, (i) CF HAZ showing QPF, M/A, UB, and WF. (Note: PF = polygonal ferrite; P = pearlite; AF = acicular ferrite; LB = lower bainite; UB = upper bainite; QPF = quenched polygonal ferrite; M/A = martensite-austenite; WF = Widmanstätten ferrite; GBF = grain boundary ferrite; LF = lath ferrite; SF = side-plate ferrite)

#### 4.5.4.6 Weld Specimen Corrosion Analysis

Electrochemical corrosion analysis was performed on the weld specimens to evaluate the corrosion resistance of the weld metal produced with different flux compositions. This is particularly important for pipeline applications in marine and offshore environments where the weld joints are exposed to corrosive media including seawater, CO₂, and H₂S.

**Specimen Preparation for Corrosion Testing:**

Corrosion test specimens were extracted from the fusion zone of each weld joint. The specimens were prepared as follows:
1. Specimens were cut to expose a defined surface area (typically 1 cm²)
2. Electrical connection was established by soldering a copper wire to the back surface
3. The specimens were mounted in cold-setting epoxy resin, leaving only the test surface exposed
4. The exposed surface was ground sequentially with SiC papers (up to 1200 grit)
5. Final polishing was performed with diamond paste (1 μm)
6. Specimens were ultrasonically cleaned in acetone and dried before testing

**Electrochemical Testing Setup:**

Electrochemical measurements were conducted using a three-electrode cell configuration:
- Working electrode: Weld metal specimen
- Reference electrode: Saturated Calomel Electrode (SCE)
- Counter electrode: Platinum plate

The electrolyte used was a solution simulating the pipeline service environment (typically 3.5% NaCl solution representing seawater conditions). The following electrochemical techniques were employed:

1. **Open Circuit Potential (OCP) measurement:** The specimens were immersed in the electrolyte for a stabilization period (typically 30–60 minutes) until a steady-state potential was achieved.

2. **Potentiodynamic Polarization:** Linear sweep voltammetry was performed from -250 mV vs. OCP to +250 mV vs. OCP at a scan rate of 1 mV/s. From the polarization curves, the following corrosion parameters were extracted using Tafel extrapolation method:
   - Corrosion potential (E_corr)
   - Corrosion current density (i_corr)
   - Anodic and cathodic Tafel slopes (β_a, β_c)
   - Corrosion rate (calculated from i_corr using Faraday's law)

3. **Electrochemical Impedance Spectroscopy (EIS):** Measurements were performed at OCP with an AC perturbation amplitude of 10 mV over a frequency range of 100 kHz to 10 mHz. The impedance data were analyzed by fitting to equivalent electrical circuits to determine:
   - Solution resistance (R_s)
   - Charge transfer resistance (R_ct)
   - Double-layer capacitance (C_dl)

**Corrosion Behavior Assessment:**

The corrosion behavior of the weld metal is influenced by several factors related to the flux composition:
- The silicon content in the weld metal (higher Si promotes formation of protective SiO₂ films)
- The manganese content (Mn can form MnS inclusions that act as pitting initiation sites)
- The chromium and molybdenum content (both promote passive film formation)
- The microstructural homogeneity (galvanic coupling between different phases)
- The inclusion content and distribution (inclusions can act as preferential corrosion sites)

The weld metal chemistry resulting from the basic flux compositions (particularly the lower sulfur content and controlled oxygen potential) is expected to provide improved corrosion resistance compared to weld metals produced with acidic or neutral flux systems. The basic fluxes promote cleaner weld metal with fewer non-metallic inclusions, which reduces the number of potential pit initiation sites.

The electrochemical corrosion behavior was systematically compared across all four weld joints to establish the relationship between flux composition, weld metal chemistry, microstructure, and corrosion performance. This integrated approach provides a complete picture of the suitability of the developed fluxes for marine and offshore pipeline applications where both mechanical performance and corrosion resistance are critical design requirements.

## Summary of Experimental Program

The complete experimental program described in this chapter encompasses a systematic progression from flux design through characterization to final weldment evaluation:

1. **Flux Design (Section 4.1):** Twenty-five SAW fluxes were designed using DoE methodology with ternary phase diagram guidance
2. **Flux Preparation (Section 4.2):** Laboratory agglomeration process with controlled particle size and moisture content
3. **Flux Characterization (Section 4.3):** Comprehensive physicochemical and thermophysical property measurement including density, thermal properties, XRD, and FTIR
4. **Bead-on-Plate Screening (Section 4.4):** Multipass welding with all 25 fluxes, chemical analysis, microhardness measurement, and flux selection
5. **Full Weldment Fabrication and Testing (Section 4.5):** Butt weld joints with three selected fluxes plus commercial reference, followed by complete mechanical and microstructural characterization

This methodical approach replaces traditional trial-and-error flux development with a science-based, predictable framework for designing SAW fluxes optimized for high-strength pipeline steel applications in marine and offshore environments.

