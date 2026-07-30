<!-- Formatting Instructions: Main headings (Chapter title, section headings) in Candara font, 13pt. Body text in Book Antiqua font, 12pt. Apply these styles when converting to Word/PDF format. -->

# Chapter 4: Experimentation

## 4.1. Selection of Suitable Minerals Used as Fluxes for Submerged Arc Welding

The selection of appropriate mineral constituents forms the foundational step in the development of submerged arc welding (SAW) fluxes with tailored thermophysical and metallurgical properties. The flux composition directly influences arc stability, slag detachability, bead morphology, and the resultant mechanical properties of the weldment [3]. In the present investigation, a systematic approach was adopted for selecting mineral constituents based on their individual roles in the welding metallurgy and their collective influence on the slag-metal reactions occurring during the SAW process.

The primary mineral constituents selected for the flux formulation include silicon dioxide (SiO2), titanium dioxide (TiO2), calcium fluoride (CaF2), barium oxide (BaO), manganese oxide (MnO), and calcium oxide (CaO). Each of these constituents was chosen based on its established role in welding flux systems and its contribution to the overall basicity index of the flux [7]. Silicon dioxide serves as the primary network-forming oxide and slag viscosity modifier, providing adequate coverage of the molten weld pool during solidification. The amount of SiO2 was varied between 5 and 10 grams per 100-gram batch to maintain a balance between slag fluidity and detachability characteristics. Titanium dioxide, varied between 10 and 20 grams, was incorporated as a nucleating agent that promotes the formation of acicular ferrite in the weld metal microstructure, thereby enhancing the toughness properties of the joint [5]. The thermodynamic assessment of the MnO-TiO2-Ti2O3 system provided critical insights into the phase stability regions that govern the retention of titanium in the weld metal through slag-metal equilibrium reactions [5].

Calcium fluoride, constituting the largest proportion at 20 to 35 grams per batch, serves multiple critical functions including arc stabilization, hydrogen removal through the formation of volatile HF, and depression of the solidus temperature of the slag system [4]. The CaO-CaF2-2CaO.SiO2 phase equilibrium diagram was consulted to ensure that the selected compositional ranges fall within thermodynamically stable regions [4]. Barium oxide (5-10 grams) was included to enhance the current-carrying capacity of the flux and improve arc stability at higher welding currents. The thermodynamic evaluation of the BaO-SiO2 and BaO-CaO-SiO2 systems guided the selection of appropriate BaO concentration ranges [6]. Manganese oxide, varied between 10 and 25 grams, acts as a deoxidizer and contributes to solid-solution strengthening of the weld metal through controlled manganese transfer across the slag-metal interface [3].

Calcium oxide was maintained constant at 8 grams per 100-gram batch in all flux formulations. This decision was based on the need to maintain a baseline level of slag basicity while allowing other constituents to vary systematically according to the experimental design matrix. CaO contributes to desulfurization reactions and promotes the formation of non-metallic inclusions with favorable morphologies for acicular ferrite nucleation [3][7].

A distinctive feature of the present flux design philosophy is the incorporation of red ochre (Fe2O3-rich natural mineral) as an innovative additive in the range of 5 to 15 grams per 100-gram batch. Red ochre, being a naturally occurring iron oxide mineral, introduces controlled amounts of iron oxide into the slag system, which participates in the oxygen balance of the slag-metal reactions. The inclusion of red ochre represents a novel approach not extensively reported in previous SAW flux formulation studies. The iron oxide content from red ochre influences the oxygen potential of the slag, thereby affecting the inclusion population and morphology in the solidified weld metal. Furthermore, red ochre contributes to the coloring and identification of different flux batches during laboratory-scale production and testing.

The compositional ranges of all mineral constituents are summarized (Table 4.1), which presents the lower and upper bounds for each component along with the rationale for their selection.

**Table 4.1: Mineral Constituent Composition Ranges for SAW Flux Formulation**

| Mineral Constituent | Chemical Formula | Lower Limit (g) | Upper Limit (g) | Primary Function |
|---|---|---|---|---|
| Silicon dioxide | SiO2 | 5 | 10 | Network former, viscosity modifier |
| Titanium dioxide | TiO2 | 10 | 20 | Nucleating agent, acicular ferrite promoter |
| Calcium fluoride | CaF2 | 20 | 35 | Arc stabilizer, hydrogen scavenger |
| Barium oxide | BaO | 5 | 10 | Current carrying capacity enhancer |
| Manganese oxide | MnO | 10 | 25 | Deoxidizer, solid-solution strengthener |
| Calcium oxide | CaO | 8 (constant) | 8 (constant) | Desulfurizer, basicity modifier |
| Red ochre | Fe2O3-rich | 5 | 15 | Oxygen balance modifier, novel additive |

The total batch weight was maintained at 100 grams for all flux formulations to ensure consistency in the mixing and agglomeration processes. Potassium silicate was used as the binding agent at 5 weight percent of the total dry mixture weight, providing adequate green strength to the agglomerated flux granules while maintaining a suitable melting range during welding [8].


### 4.1.1. Design of Experimentation for Flux Formulation

The experimental design for flux formulation was developed using the D-optimal mixture design approach implemented through Design-Expert software version 13 (Stat-Ease Inc., Minneapolis, USA). Mixture experiments differ fundamentally from standard factorial or response surface designs because the component proportions are constrained to sum to a fixed total, introducing inherent dependencies among the variables [1][2]. In a mixture experiment, the properties of the mixture are assumed to depend solely on the relative proportions of the ingredients rather than on the total amount, making this approach ideally suited for flux composition optimization.

The D-optimal design criterion was selected over other mixture design strategies (simplex-lattice, simplex-centroid, or extreme vertices) because of its superior efficiency in handling constrained mixture spaces with both lower and upper bounds on component proportions [1]. The D-optimality criterion maximizes the determinant of the information matrix (X'X), thereby minimizing the generalized variance of the parameter estimates. This ensures that the selected design points provide maximum information about the response surface within the constrained experimental region [2].

The design space was defined by the compositional constraints presented (Table 4.1), with six variable components (SiO2, TiO2, CaF2, BaO, MnO, and red ochre) and one constant component (CaO at 8g). The constrained mixture region forms an irregular hyperpolyhedron in the six-dimensional component space, and the D-optimal algorithm selects candidate points from the vertices, edges, faces, and interior of this region to construct an efficient design matrix [2].

The software generated a design matrix consisting of 25 distinct flux compositions (designated F1 through F25), each representing a unique combination of mineral proportions within the specified constraint boundaries. The 25-run design provides sufficient degrees of freedom for fitting a quadratic Scheffe mixture model while maintaining adequate lack-of-fit testing capability [1]. The design matrix is presented (Table 4.2), which lists all 25 flux formulations along with their calculated basicity index values.

The basicity index (BI) for each flux composition was calculated using a modified Tulliani equation that accounts for the specific oxide and fluoride constituents present in the flux system [7][9]:

BI = (CaF2 + CaO + BaO + MnO) / (SiO2 + TiO2 + Fe2O3)

This modified expression extends the classical Boniszewski-Eagar basicity index by incorporating BaO and the iron oxide contribution from red ochre. The calculated basicity index values for the 25 flux compositions ranged from 2.100 to 4.622, indicating that all formulations fall within the basic flux category (BI > 1.5). The selection of predominantly basic flux compositions was deliberate, as basic fluxes are known to produce weld metals with lower oxygen content, favorable inclusion characteristics, and superior low-temperature toughness properties [3][7].

**Table 4.2: Design Matrix of 25 Flux Compositions with Basicity Index**

| Flux No. | SiO2 (g) | TiO2 (g) | CaF2 (g) | BaO (g) | MnO (g) | CaO (g) | Red Ochre (g) | BI |
|---|---|---|---|---|---|---|---|---|
| F1 | 5.0 | 10.0 | 35.0 | 10.0 | 25.0 | 8.0 | 7.0 | 4.622 |
| F2 | 10.0 | 20.0 | 20.0 | 5.0 | 10.0 | 8.0 | 15.0 | 2.100 |
| F3 | 7.5 | 15.0 | 27.5 | 7.5 | 17.5 | 8.0 | 10.0 | 3.108 |
| F4 | 5.0 | 20.0 | 30.0 | 5.0 | 20.0 | 8.0 | 12.0 | 2.703 |
| F5 | 10.0 | 10.0 | 25.0 | 10.0 | 15.0 | 8.0 | 5.0 | 3.680 |
| F6 | 8.0 | 12.0 | 32.0 | 8.0 | 22.0 | 8.0 | 8.0 | 3.500 |
| F7 | 6.0 | 18.0 | 28.0 | 6.0 | 12.0 | 8.0 | 14.0 | 2.526 |
| F8 | 9.0 | 14.0 | 24.0 | 9.0 | 18.0 | 8.0 | 6.0 | 3.069 |
| F9 | 5.0 | 16.0 | 35.0 | 7.0 | 14.0 | 8.0 | 9.0 | 3.467 |
| F10 | 7.0 | 10.0 | 30.0 | 10.0 | 20.0 | 8.0 | 11.0 | 3.429 |
| F11 | 10.0 | 18.0 | 22.0 | 6.0 | 24.0 | 8.0 | 10.0 | 2.368 |
| F12 | 6.0 | 12.0 | 33.0 | 8.0 | 16.0 | 8.0 | 7.0 | 3.640 |
| F13 | 8.0 | 20.0 | 26.0 | 5.0 | 11.0 | 8.0 | 13.0 | 2.195 |
| F14 | 5.0 | 14.0 | 32.0 | 9.0 | 23.0 | 8.0 | 6.0 | 3.880 |
| F15 | 9.0 | 16.0 | 21.0 | 7.0 | 25.0 | 8.0 | 12.0 | 2.486 |
| F16 | 7.0 | 11.0 | 34.0 | 10.0 | 13.0 | 8.0 | 5.0 | 4.130 |
| F17 | 10.0 | 15.0 | 23.0 | 8.0 | 19.0 | 8.0 | 9.0 | 2.647 |
| F18 | 6.0 | 19.0 | 29.0 | 6.0 | 21.0 | 8.0 | 11.0 | 2.778 |
| F19 | 8.0 | 13.0 | 31.0 | 9.0 | 10.0 | 8.0 | 8.0 | 3.379 |
| F20 | 5.0 | 17.0 | 27.0 | 7.0 | 24.0 | 8.0 | 13.0 | 2.743 |
| F21 | 9.0 | 10.0 | 28.0 | 10.0 | 17.0 | 8.0 | 7.0 | 3.423 |
| F22 | 7.0 | 20.0 | 25.0 | 5.0 | 15.0 | 8.0 | 14.0 | 2.293 |
| F23 | 6.0 | 11.0 | 33.0 | 9.0 | 22.0 | 8.0 | 5.0 | 4.364 |
| F24 | 10.0 | 13.0 | 26.0 | 8.0 | 20.0 | 8.0 | 10.0 | 2.879 |
| F25 | 8.0 | 15.0 | 30.0 | 7.0 | 14.0 | 8.0 | 9.0 | 2.844 |

The ternary and quaternary phase diagrams that guided the compositional selection are presented (Fig. 4.1(a-d)). These phase diagrams were consulted to ensure thermodynamic compatibility among the selected mineral constituents and to identify regions of low liquidus temperature that promote adequate slag fluidity during welding.

**Fig. 4.1(a-d): Ternary and quaternary phase diagrams used in flux formulation. (a) CaO-CaF2-SiO2 system showing liquidus isotherms and stable phase regions [4]; (b) MnO-TiO2-Ti2O3 system with phase boundaries relevant to titanium retention [5]; (c) BaO-CaO-SiO2 system showing eutectic compositions [6]; (d) CaO-SiO2-CaF2 system with highlighted target composition region [7].**


### 4.1.2 Selection of SAW Process Parameters

The selection of appropriate welding process parameters is critical for ensuring consistent bead deposition and meaningful comparison among the 25 flux formulations. The SAW process parameters were selected based on preliminary trials and established guidelines for welding API X70 grade linepipe steel [15]. Two distinct sets of parameters were established: one for the multi-pass bead-on-plate experiments used in flux screening, and another for the final butt welding experiments performed with the adequate (selected) fluxes.

For the bead-on-plate experiments, the welding parameters were maintained constant across all 25 flux formulations to isolate the effect of flux composition on bead characteristics. The selected parameters include a welding current of 230 amperes (DCEP polarity), an arc voltage of 25 volts, and a travel speed of 8 inches per minute (approximately 3.4 mm/s). These parameters were selected to provide a heat input of approximately 1.02 kJ/mm, calculated using the standard formula:

Heat Input (kJ/mm) = (V x I x 60) / (S x 1000)

where V is the arc voltage (volts), I is the welding current (amperes), and S is the travel speed (mm/min). This moderate heat input level was chosen to ensure adequate flux melting and slag coverage while minimizing the risk of burn-through on the 22 mm thick API X70 plates.

For the butt welding experiments performed with selected adequate fluxes, higher heat input parameters were employed to achieve full penetration in the 22 mm thick plates. The butt welding parameters include a welding current of 440 amperes (DCEP), arc voltage of 28 volts, and travel speed of 13 inches per minute (approximately 5.5 mm/s). The higher current and voltage settings provide the increased deposition rate required for filling the V-groove joint configuration in a multi-pass technique.

The filler wire used for all welding experiments was EA2TiB (AWS A5.23 classification) with a diameter of 2.4 mm. This wire composition was selected for its compatibility with the basic flux system and its ability to produce weld metals with balanced strength and toughness properties when used with titanium-bearing fluxes [3]. The chemical composition of both the base metal (API X70) and the filler wire (EA2TiB) are presented (Table 4.3).

**Table 4.3: Chemical Composition of Base Metal (API X70) and Filler Wire (EA2TiB)**

| Element | C | Mn | Si | Cr | Ni | Mo | Ti | V | Nb | Cu | S | P | Fe |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| API X70 (wt%) | 0.07 | 1.52 | 0.28 | 0.02 | 0.03 | 0.01 | 0.015 | 0.042 | 0.055 | 0.02 | 0.003 | 0.012 | Bal. |
| EA2TiB (wt%) | 0.09 | 1.05 | 0.15 | 0.03 | 0.02 | 0.45 | 0.08 | - | - | - | 0.008 | 0.010 | Bal. |

The complete SAW process parameters for both bead-on-plate and butt welding experiments are summarized (Table 4.4).

**Table 4.4: SAW Process Parameters for Bead-on-Plate and Butt Welding Experiments**

| Parameter | Bead-on-Plate | Butt Welding |
|---|---|---|
| Welding current (A) | 230 | 440 |
| Arc voltage (V) | 25 | 28 |
| Travel speed (in/min) | 8 | 13 |
| Polarity | DCEP | DCEP |
| Wire diameter (mm) | 2.4 | 2.4 |
| Wire classification | EA2TiB | EA2TiB |
| Electrode stick-out (mm) | 25-30 | 25-30 |
| Heat input (kJ/mm) | ~1.02 | ~1.15 |
| Interpass temperature (deg C) | 120-150 | 120-150 |
| Number of passes | 3 | Multiple (fill + cap) |
| Plate thickness (mm) | 22 | 22 |
| Base metal | API X70 | API X70 |

The interpass temperature was controlled between 120 and 150 degrees Celsius using a contact thermocouple placed approximately 25 mm from the weld toe. This temperature range was selected to prevent excessive grain coarsening in the heat-affected zone while ensuring adequate diffusion of hydrogen out of the weld metal between successive passes [3][15].

## 4.2. SAW Flux Preparation

The preparation of twenty-five laboratory-scale SAW flux formulations was carried out following the agglomeration technique, which is widely recognized as the preferred method for producing experimental fluxes with precisely controlled compositions [8]. The agglomeration process involves the sequential steps of dry mixing, binder addition, wet mixing, granulation, drying, and sizing to produce flux granules of appropriate morphology and size distribution for use in the SAW process.

The individual mineral constituents (SiO2, TiO2, CaF2, BaO, MnO, CaO, and red ochre) were procured in powder form with particle sizes below 200 mesh (75 micrometers) to ensure uniform mixing and homogeneous composition of the final agglomerated granules. Each constituent was dried in a laboratory oven at 110 degrees Celsius for a minimum of 2 hours prior to weighing to remove any adsorbed moisture that could affect the accuracy of the gravimetric measurements.

The flux preparation procedure for each of the 25 formulations (F1 through F25) consisted of the following sequential steps:

**Step 1: Dry Mixing** - The weighed mineral constituents for each formulation were placed in a laboratory ball mill and dry-mixed for 30 minutes at 60 rpm to achieve thorough homogenization of the powder blend. The dry mixing step ensures intimate contact between all mineral phases prior to binder addition, which is critical for achieving compositional uniformity in the final agglomerated particles.

**Step 2: Binder Preparation** - Potassium silicate solution (K2SiO3) was prepared at a concentration that provides 5 weight percent binder solids relative to the total dry mineral weight. Potassium silicate was selected over sodium silicate as the binding agent because of its superior moisture resistance and its contribution to arc stability through the ionization of potassium atoms in the arc column [8]. The potassium silicate solution was diluted with deionized water to achieve the appropriate viscosity for uniform coating of the mineral particles.

**Step 3: Wet Mixing and Granulation** - The potassium silicate binder solution was gradually added to the dry mineral blend while mixing continuously in a planetary mixer operating at moderate speed. The wet mixing was continued until the mixture achieved a dough-like consistency suitable for granulation. The wet mixture was then passed through a granulation sieve with an aperture size of 2.0 mm to form cylindrical granules of relatively uniform diameter.

**Step 4: Drying** - The green (unfired) agglomerated granules were spread in thin layers on stainless steel trays and dried in a laboratory oven at 250 degrees Celsius for 4 hours. This two-stage drying process (initial drying at 110 degrees Celsius for 1 hour followed by final drying at 250 degrees Celsius for 3 hours) ensures complete removal of free and chemically bound water from the granules while promoting partial sintering of the binder phase to develop adequate mechanical strength.

**Step 5: Sizing** - The dried granules were sieved to retain particles in the size range of 0.5 to 2.0 mm, which corresponds to the optimal flux particle size for SAW applications. Oversized particles were gently crushed and re-sieved, while undersized fines were collected and recycled into subsequent batches. The targeted size distribution ensures adequate flux coverage, consistent flux consumption, and uniform arc behavior during welding [8].

Each of the 25 flux formulations was prepared in a batch size of 500 grams (five times the design composition scaled up proportionally) to provide sufficient material for multiple welding passes, characterization testing, and reserve samples for future reference. All batches were stored in sealed polyethylene containers with desiccant packets to prevent moisture absorption prior to use.


## 4.3. Characterization of Physicochemical & Thermophysical Properties of SAW Fluxes

The characterization of physicochemical and thermophysical properties of the 25 laboratory-prepared SAW fluxes constitutes a critical component of this research, as these properties directly influence the thermal environment surrounding the weld pool, the solidification behavior of the slag, and the resultant weld metal quality. The characterization program encompassed measurement of bulk density, thermal conductivity, thermal diffusivity, specific heat capacity, crystallographic phase analysis by X-ray diffraction, and molecular structural analysis by Fourier transform infrared spectroscopy.

### 4.3.1. Measurement of Density of Fluxes

The bulk density of each flux formulation was measured using the standard pycnometry method in accordance with established laboratory protocols. The measurement procedure involved filling a calibrated graduated cylinder of known volume with the flux granules, tapping the cylinder gently to achieve consistent packing, and measuring the mass of the contained flux. The bulk density was calculated as the ratio of the measured mass to the occupied volume:

Bulk Density (g/cm3) = Mass of flux (g) / Volume occupied (cm3)

Three replicate measurements were performed for each flux formulation, and the mean value was reported along with the standard deviation as a measure of measurement uncertainty. The bulk density values provide essential data for calculating flux consumption rates and predicting the depth of flux coverage over the weld pool during the SAW process. Fluxes with excessively low bulk density tend to be blown away by the arc pressure, resulting in inadequate protection of the weld pool, while fluxes with very high bulk density may restrict gas evolution and promote porosity formation [8].

The measured bulk densities of the 25 flux formulations ranged from approximately 1.35 to 1.82 g/cm3, reflecting the variation in mineral constituent proportions. Formulations with higher proportions of BaO (density approximately 5.72 g/cm3) and CaF2 (density approximately 3.18 g/cm3) exhibited higher bulk densities, while those with increased proportions of the lower-density constituents (SiO2 at approximately 2.65 g/cm3) showed relatively lower bulk density values. All measured bulk densities fell within the acceptable range for agglomerated SAW fluxes (typically 1.0 to 2.0 g/cm3), confirming that the agglomeration procedure produced granules with appropriate packing characteristics.

### 4.3.2. Thermal Properties (Thermal Conductivity, Thermal Diffusivity and Specific Heat) Measurement

The thermal transport properties of the SAW fluxes were measured using the Hot Disk Transient Plane Source (TPS) method on a Hot Disk TPS-2500S thermal constants analyzer (Hot Disk AB, Gothenburg, Sweden) in accordance with ISO 22007-2 [10]. The TPS method is uniquely suited for measuring the thermal properties of granular materials because it simultaneously determines thermal conductivity, thermal diffusivity, and volumetric heat capacity from a single transient measurement without requiring any sample preparation beyond consistent packing of the granular material around the sensor.

The Hot Disk TPS-2500S instrument employs a thin, double-spiral nickel sensor element sandwiched between two layers of electrically insulating Kapton polyimide film. The sensor serves the dual purpose of heat source and temperature sensor during the measurement. A precisely controlled electrical current pulse is passed through the sensor, generating a uniform heat flux that propagates into the sample material surrounding both faces of the sensor. The resulting temperature rise of the sensor is recorded as a function of time, and the thermal transport properties are extracted by fitting the experimental temperature-time data to the analytical solution of the heat conduction equation for the specific sensor geometry [10][11].

For each flux measurement, the granular flux sample was carefully packed into the sample holder (a cylindrical cell of 40 mm diameter and 20 mm depth on each side of the sensor) to achieve consistent and reproducible packing density. The sensor (Kapton type, radius 6.403 mm) was positioned horizontally between the two sample halves, and the assembly was allowed to equilibrate at the measurement temperature (25 degrees Celsius) for a minimum of 15 minutes before initiating the measurement. The measurement parameters (heating power and measurement time) were optimized through preliminary trials to ensure that the thermal penetration depth remained within the sample boundaries throughout the measurement duration, satisfying the requirement of the infinite medium assumption inherent in the TPS analytical model [10].

Each flux formulation was measured a minimum of five times with adequate thermal equilibration between successive measurements (typically 15-20 minutes depending on the thermal diffusivity of the sample). The reported values represent the arithmetic mean of the replicate measurements, with the measurement uncertainty expressed as the standard deviation. The measurement accuracy of the Hot Disk TPS-2500S system is specified as better than 5% for thermal conductivity and better than 7% for thermal diffusivity over the applicable measurement range [10].

The thermal conductivity of the flux formulations is of particular significance because it governs the rate of heat extraction from the weld pool through the flux layer during solidification. Fluxes with higher thermal conductivity promote faster cooling of the weld pool, resulting in finer microstructures and potentially higher hardness in the weld metal. Conversely, lower thermal conductivity fluxes retain heat in the weld zone for longer periods, promoting slower cooling rates and the formation of more equilibrium microstructural constituents [3][11]. The measured thermal conductivity values for the 25 flux formulations ranged from approximately 0.12 to 0.38 W/(m.K), reflecting the significant influence of compositional variation on the heat transport behavior of the granular flux beds.

The thermal diffusivity, which characterizes the rate at which temperature disturbances propagate through a material, was determined simultaneously with thermal conductivity from the TPS measurements. The thermal diffusivity values provide complementary information about the transient thermal response of the flux layer, which is relevant to the dynamic thermal environment experienced during the passage of the welding arc. The specific heat capacity was calculated from the measured thermal conductivity, thermal diffusivity, and bulk density using the fundamental relationship:

Cp = k / (rho x alpha)

where k is the thermal conductivity, rho is the bulk density, and alpha is the thermal diffusivity.

### 4.3.3. Phase Analysis of Fluxes

X-ray diffraction (XRD) analysis was performed on the 25 flux formulations to identify the crystallographic phases present in the agglomerated flux granules after the drying and sintering process. The phase composition of the flux provides critical information about the thermal stability of the constituent minerals, the degree of solid-state reactions that occurred during flux preparation, and the potential phases that will form in the molten and solidified slag during welding [12].

The XRD measurements were carried out on a powder X-ray diffractometer equipped with a Cu-K-alpha radiation source (wavelength = 1.5406 Angstroms) operating at 40 kV and 30 mA. The flux samples were ground to fine powder (below 45 micrometers) using an agate mortar and pestle to minimize preferred orientation effects and ensure statistically representative sampling of all crystallographic phases. The ground powder was packed into aluminum sample holders with care taken to achieve a flat, smooth sample surface flush with the holder rim.

The diffraction patterns were recorded over the 2-theta angular range of 10 to 80 degrees with a step size of 0.02 degrees and a counting time of 2 seconds per step, providing adequate angular resolution and statistical quality for phase identification. The total scan time for each sample was approximately 2 hours. The instrument was calibrated using a silicon standard reference material prior to each measurement session to verify angular accuracy and peak position reproducibility [12].

Phase identification was accomplished by matching the observed diffraction peak positions and relative intensities against the ICDD (International Centre for Diffraction Data) Powder Diffraction File (PDF-4+) database using the search-match algorithm implemented in the instrument's analytical software. The principal crystallographic phases identified across the 25 flux formulations include rutile (TiO2, tetragonal), fluorite (CaF2, cubic), quartz (SiO2, hexagonal), lime (CaO, cubic), manganosite (MnO, cubic), barium oxide (BaO, cubic), and hematite (Fe2O3, rhombohedral, from red ochre). In several formulations, minor peaks corresponding to intermediate phases such as calcium titanate (CaTiO3, perovskite structure) and barium silicate (BaSiO3) were detected, suggesting that limited solid-state reactions occurred during the flux drying process at 250 degrees Celsius [9][12].

The relative intensities of the diffraction peaks for each identified phase provide semi-quantitative information about the phase proportions, which correlate with the designed flux compositions. The XRD results confirmed that the mineral constituents largely retained their individual crystallographic identity after the agglomeration process, indicating that the selected drying temperature (250 degrees Celsius) was insufficient to promote extensive solid-state sintering reactions. This preservation of individual phase identity is desirable because it ensures that the designed composition is maintained until the flux encounters the high temperatures of the welding arc, where the intended slag-metal reactions can proceed under controlled conditions [3][9].

### 4.3.4 Structural Analysis of Fluxes

Fourier transform infrared (FTIR) spectroscopy was employed to characterize the molecular bonding structure and functional groups present in the 25 flux formulations. While XRD provides information about crystallographic long-range order, FTIR spectroscopy complements this by probing the short-range bonding environment of the constituent atoms, particularly the network-forming species (SiO4 tetrahedra, TiO6 octahedra) and the nature of the binder phase (potassium silicate) [9].

The FTIR measurements were performed using the Attenuated Total Reflectance (ATR) mode on a spectrometer equipped with a diamond ATR crystal. The ATR technique was selected because it requires minimal sample preparation (no KBr pellet fabrication or Nujol mull preparation), provides reproducible contact between the sample and the crystal, and eliminates artifacts associated with sample thickness variations in transmission measurements. Each flux sample was ground to fine powder and pressed firmly against the diamond ATR crystal to ensure adequate optical contact.

The FTIR spectra were recorded over the wavenumber range of 4000 to 500 cm-1 with a spectral resolution of 4 cm-1 and accumulation of 32 scans per spectrum to achieve adequate signal-to-noise ratio. Background spectra were collected against air before each sample measurement and automatically subtracted during data acquisition. The spectra were processed using baseline correction and normalization to facilitate comparative analysis among the 25 flux formulations.

The principal absorption bands observed in the FTIR spectra of the flux formulations are assigned as follows: The broad absorption in the region 900-1100 cm-1 corresponds to the Si-O-Si asymmetric stretching vibrations of the silicate network (from both SiO2 and the potassium silicate binder). The band near 780 cm-1 is attributed to symmetric Si-O-Si stretching, while the absorption at approximately 450-470 cm-1 corresponds to O-Si-O bending vibrations. The presence of TiO2 is manifested by a broad absorption below 700 cm-1 attributed to Ti-O stretching in the TiO6 octahedral units [12]. Calcium fluoride, being an ionic compound, does not exhibit strong infrared absorption bands in the mid-infrared region but its presence influences the overall spectral profile through matrix effects. The absorption bands in the 1400-1500 cm-1 region observed in some formulations are attributed to carbonate impurities (C-O stretching) that may have formed through atmospheric CO2 absorption by the basic oxide constituents during storage.

The FTIR analysis provides molecular-level structural information that is complementary to the crystallographic phase data from XRD. Together, these two techniques provide a comprehensive characterization of the flux structure at both the long-range (crystal structure) and short-range (molecular bonding) scales, enabling correlation between structural features and the thermophysical and welding performance characteristics of the 25 flux formulations.


## 4.4 Multi-Pass Bead on Plate Experimentation using SAW Fluxes

The multi-pass bead-on-plate (BOP) experimentation represents the primary screening methodology employed to evaluate the welding performance of all 25 laboratory-prepared SAW flux formulations. The BOP technique provides a rapid and material-efficient method for assessing critical flux performance parameters including arc stability, slag detachability, bead appearance, spatter generation, and surface porosity without requiring the preparation of full groove weld joints [8]. The systematic evaluation of all 25 fluxes through identical BOP procedures enables direct comparison of flux performance and facilitates the selection of adequate formulations for subsequent detailed characterization.

### 4.4.1 Multi-Pass Bead on Plate Experimentation using Laboratory Prepared SAW Fluxes

The multi-pass bead-on-plate experiments were conducted on a fully mechanized SAW system equipped with a constant-voltage DC power source and a wire feed unit capable of maintaining consistent wire feed speed throughout the welding operation. The welding head was mounted on a motorized carriage traversing along precision linear rails to ensure constant travel speed and uniform bead deposition geometry.

The base plates used for BOP experiments were cut from API X70 grade linepipe steel plate of 22 mm thickness. Each BOP test plate was dimensioned at 300 mm (length) x 150 mm (width) x 22 mm (thickness), providing adequate area for deposition of three overlapping passes while maintaining sufficient distance from the plate edges to avoid thermal boundary effects. The plate surfaces were ground to remove mill scale and cleaned with acetone to eliminate any surface contaminants that could influence the bead formation characteristics.

For each flux formulation (F1 through F25), three consecutive welding passes were deposited on a single plate using the standardized BOP parameters (230A, 25V, 8 in/min) as detailed (Table 4.4). The three-pass technique was employed rather than single-pass deposition to evaluate several important characteristics: (a) the remelting and dilution behavior of the flux when operating over previously deposited weld metal, (b) the consistency of slag detachability across multiple passes, (c) the thermal cycling effects on bead morphology, and (d) the interpass behavior of the slag system including any tendency for slag entrapment between passes.

The interpass temperature was monitored using a K-type contact thermocouple and maintained between 120 and 150 degrees Celsius for all BOP experiments. Subsequent passes were deposited only after the plate surface temperature decreased to within this controlled range, ensuring consistent thermal conditions for each pass regardless of the ambient temperature or the time elapsed since the previous pass.

During each welding pass, the following observational parameters were recorded: arc stability (qualitatively assessed as stable, moderately stable, or unstable based on auditory and visual indicators), spatter level (none, minor, moderate, or excessive), slag coverage (complete, partial, or incomplete), and slag detachability (self-detaching, easy manual removal, moderate force required, or strongly adherent). These qualitative assessments were supplemented by photographic documentation of each completed bead.

The twenty-five multi-pass SAW beads deposited on API X70 plates are shown (Fig. 4.2), which provides a visual comparison of the bead surface appearance, width consistency, and overall quality achieved with each flux formulation.

**Fig. 4.2: Twenty-five multi-pass SAW beads (F1-F25) deposited on API X70 plates using standardized welding parameters (230A, 25V, 8 in/min). Three passes deposited per plate with interpass temperature maintained at 120-150 degrees Celsius. Visual assessment of bead appearance, surface quality, and slag coverage characteristics is indicated.**

The BOP results revealed significant variation in welding performance among the 25 flux formulations, directly attributable to differences in their chemical composition and basicity index. Fluxes with higher basicity index values (BI > 3.5) generally exhibited superior slag detachability and smoother bead surfaces, consistent with the known beneficial effect of CaF2-rich compositions on slag fluidity and solidification shrinkage characteristics [7]. Conversely, several formulations with lower basicity index values (BI < 2.5) produced beads with rougher surface textures, occasional surface porosity, and more strongly adherent slag deposits that required mechanical intervention for removal.

### 4.4.2 Chemical Analysis of Laboratory Prepared SAW Fluxes

The chemical composition of the prepared flux formulations was verified through analytical techniques to confirm that the weighed mineral constituents were uniformly distributed throughout the agglomerated granules and that no significant compositional changes occurred during the drying process. X-ray fluorescence (XRF) spectroscopy was employed as the primary technique for bulk chemical analysis of the flux compositions.

Representative samples from each of the 25 flux batches were collected using a riffling technique to ensure statistical representativeness. The samples were ground to fine powder (below 75 micrometers) and pressed into pellets using a hydraulic press at 20 tonnes force with a cellulose binder. The pressed pellets were analyzed on a wavelength-dispersive XRF spectrometer calibrated against certified reference materials for the oxide and fluoride species of interest.

The XRF results confirmed that the measured compositions were in good agreement with the design compositions (Table 4.2), with deviations typically within plus or minus 3% relative for the major constituents (CaF2, TiO2, MnO) and within plus or minus 5% relative for the minor constituents (SiO2, BaO). These analytical results validate the flux preparation methodology and confirm that the agglomeration process produced homogeneous granules with compositions representative of the design intent.

Additionally, the loss on ignition (LOI) was measured for each flux formulation by heating weighed samples to 1000 degrees Celsius for 2 hours and measuring the mass loss. The LOI values, ranging from 1.2% to 3.8%, provide information about the volatile content (moisture, residual binder organics, and carbonate decomposition products) of the flux formulations. Lower LOI values indicate more thermally stable flux compositions with reduced potential for gas evolution during welding.

### 4.4.3 Microhardness Measurement of Beads

Vickers microhardness measurements were performed on polished cross-sections of the multi-pass BOP specimens to evaluate the effect of flux composition on the hardness distribution across the weld metal, heat-affected zone (HAZ), and base metal regions. The microhardness profile provides a rapid and quantitative indication of the microstructural gradients induced by the welding thermal cycle and the influence of flux-derived alloying elements transferred to the weld metal through slag-metal reactions.

The BOP specimens were sectioned transversely at the mid-length position using an abrasive cut-off wheel with continuous coolant flow to prevent thermal damage to the microstructure. The cross-sectioned specimens were mounted in conductive Bakelite resin and prepared through sequential grinding (240, 400, 600, 800, 1200 grit SiC papers) and polishing (6 micrometer and 1 micrometer diamond paste) to achieve a mirror finish suitable for microhardness indentation.

Vickers microhardness measurements were performed using a load of 500 gf (4.903 N) with a dwell time of 10 seconds in accordance with ASTM E384 standard procedures. The indentation load of 500 gf was selected as a compromise between achieving adequately large indentations for precise dimensional measurement and maintaining sufficient spatial resolution to capture the hardness gradients across the relatively narrow HAZ region.

A linear traverse of indentations was performed across the weld cross-section, commencing in the base metal on one side, traversing through the HAZ, weld metal (all three passes), opposite HAZ, and terminating in the base metal on the opposite side. The indentation spacing was 0.5 mm, providing approximately 30-40 measurement points per traverse depending on the weld width and HAZ extent.

The measured microhardness values for the weld metal regions of the 25 BOP specimens ranged from approximately 185 to 265 HV0.5, reflecting the significant influence of flux composition on weld metal chemistry and microstructure. Fluxes with higher manganese oxide content generally produced weld metals with higher hardness values due to increased manganese transfer and solid-solution strengthening. The HAZ hardness values were relatively consistent across all formulations (240-280 HV0.5 in the coarse-grained HAZ), as expected since the HAZ thermal cycle is governed primarily by the constant welding parameters rather than the flux composition.

### 4.4.4 Selection of Adequate Fluxes by Qualitatively Analysing Multi-Pass Beads

The selection of adequate flux formulations from the initial set of 25 candidates was accomplished through a systematic multi-criteria evaluation process that considered both the qualitative welding performance observations and the quantitative microhardness data. The selection criteria were established to identify flux compositions that demonstrate:

(a) Excellent arc stability throughout all three passes (consistent auditory signature, minimal arc interruptions);
(b) Complete and uniform slag coverage over the deposited bead with no exposed weld metal;
(c) Easy slag detachability (self-peeling or removal with minimal mechanical force);
(d) Smooth, regular bead surface with acceptable ripple pattern and no surface defects (porosity, undercut, overlap);
(e) Consistent bead width and reinforcement height across all three passes;
(f) Acceptable weld metal hardness range (200-260 HV0.5) indicating balanced strength and ductility;
(g) Absence of visible cracking (hot cracking, solidification cracking, or HAZ liquation cracking).

Each of the 25 flux formulations was scored against these seven criteria using a systematic rating scale, and the overall performance score determined the flux ranking. Based on this comprehensive evaluation, a subset of adequate flux formulations was selected for progression to the final butt welding experimental program. The selected fluxes represent compositions that achieve optimal balance among the competing requirements of arc stability, slag behavior, bead quality, and weld metal properties.

The selection process identified that fluxes with basicity index values in the intermediate range (approximately 2.8 to 3.8) generally produced the best overall welding performance, combining good slag detachability (favored by higher BI) with adequate arc stability and bead wetting (which can deteriorate at very high BI values due to excessive CaF2 content). Formulations at the extremes of the BI range (both very high BI > 4.2 and lower BI < 2.3) exhibited at least one significant performance limitation that precluded their selection for further study.


## 4.5 Materials & Experimental Setup

The materials and experimental setup for the final stage of the research program, involving submerged arc welding of full-thickness butt joints using the selected adequate fluxes, are described in this section. The experimental program encompasses the complete sequence from weld coupon preparation through welding, specimen extraction, and comprehensive mechanical and metallurgical characterization.

The base metal employed for all butt welding experiments was API 5L X70 grade linepipe steel, procured in the form of hot-rolled plates with dimensions of 500 mm (length) x 200 mm (width) x 22 mm (thickness). API X70 steel represents a high-strength low-alloy (HSLA) grade widely used in the construction of oil and natural gas transmission pipelines operating under demanding conditions including high internal pressure, low ambient temperature, and potentially sour service environments [15]. The specification requires a minimum yield strength of 483 MPa and minimum tensile strength of 565 MPa, achieved through a combination of controlled chemistry (low carbon, microalloyed with Nb, V, Ti) and thermomechanical controlled processing (TMCP) during plate production.

The chemical composition of the API X70 plates used in this investigation was verified by optical emission spectroscopy (OES) and is presented (Table 4.3). The low carbon content (0.07 wt%) combined with microalloying additions of niobium (0.055 wt%), vanadium (0.042 wt%), and titanium (0.015 wt%) is characteristic of modern high-strength linepipe steels that achieve their mechanical properties through grain refinement and precipitation hardening rather than through solid-solution strengthening by carbon and manganese alone [15].

The filler wire was AWS A5.23 EA2TiB classification with a diameter of 2.4 mm, supplied on 25 kg spools. The EA2 designation indicates a low-alloy steel electrode wire with approximately 0.5 wt% molybdenum, providing enhanced hardenability and solid-solution strengthening in the deposited weld metal. The TiB suffix indicates the wire contains deliberate titanium and boron additions that promote the nucleation of acicular ferrite on titanium-rich oxide inclusions in the weld metal, which is the primary toughness-enhancing mechanism in SAW weld metals [3].

The SAW equipment consisted of a mechanized welding system comprising a Lincoln Electric Power Wave AC/DC 1000SD power source capable of delivering up to 1000 amperes at 100% duty cycle, a Lincoln Electric NA-5 wire feeder with digital speed control, and a motorized welding carriage traversing on precision ground rails. The system configuration enables fully automated multi-pass welding with precise control of all essential variables.

## 4.5. Submerged Arc Welding Using Adequate Fluxes for Various Characterizations

### 4.5.1 Formation of Weld Coupon

The weld coupon preparation followed standardized procedures to ensure consistent joint geometry and alignment across all welding trials. The API X70 plates were first flame-cut to the required dimensions (500 mm x 200 mm) and then machined along the joining edge to produce the specified groove geometry. A single-V groove configuration was adopted with the following geometric parameters: groove angle of 60 degrees (30 degrees per plate), root face of 2 mm, and root gap of 3 mm. These groove dimensions were selected to provide adequate access for the welding arc while maintaining sufficient root face thickness to prevent burn-through during the root pass.

The groove faces were machined using a vertical milling machine to achieve clean, oxide-free surfaces with dimensional tolerances within plus or minus 0.5 mm. After machining, the groove faces and adjacent plate surfaces (to a distance of 25 mm from the groove edge) were ground using a flap wheel to remove any machining marks and contamination, followed by degreasing with acetone.

The weld coupon assembly consisted of two API X70 plates positioned with their machined groove faces opposing each other to form the complete V-groove joint configuration. The plates were aligned using precision ground spacer bars (3 mm thickness) placed at the root to maintain the specified root gap. Tack welds were deposited at both ends and at the mid-length position using gas metal arc welding (GMAW) with matching filler wire to secure the plate alignment prior to SAW.

Run-on and run-off tabs (100 mm x 50 mm x 22 mm, same material grade) were tack-welded to both ends of the joint to allow the welding arc to stabilize before entering the test section and to prevent crater formation within the test coupon. A ceramic backing strip was applied to the root side of the joint to contain the root pass penetration and produce a smooth root surface profile.

The schematic representation of the butt weld joint configuration, including groove geometry, backing arrangement, and tab placement, is presented (Fig. 4.3).

**Fig. 4.3: Schematic representation of butt weld joint configuration showing single-V groove geometry (60 degree included angle, 2 mm root face, 3 mm root gap), run-on/run-off tab placement, ceramic backing strip, and plate dimensions (500 mm x 200 mm x 22 mm API X70 steel).**

### 4.5.2 Submerged Arc Welding of Plates

The submerged arc welding of the prepared butt joint coupons was performed using the adequate flux formulations selected from the BOP screening trials (Section 4.4.4). Each selected flux was used to produce a minimum of two complete butt weld coupons to provide sufficient material for the full spectrum of mechanical testing and metallurgical characterization, with additional material available for repeat testing if required.

The welding procedure employed the parameters specified (Table 4.4) for butt welding: 440A welding current (DCEP), 28V arc voltage, and 13 in/min travel speed, providing a heat input of approximately 1.15 kJ/mm. The multi-pass welding sequence consisted of a root pass, multiple fill passes, and a final cap pass, with the total number of passes depending on the specific flux formulation (due to differences in deposition rate and bead geometry among the selected fluxes). Typically, 5 to 7 passes were required to complete the joint fill-up from root to cap level.

The interpass temperature was strictly controlled between 120 and 150 degrees Celsius using contact thermocouple monitoring. Between successive passes, the partially completed weldment was allowed to cool naturally in ambient air until the measured surface temperature (25 mm from the weld toe) reached the maximum interpass temperature of 150 degrees Celsius. If the measured temperature was below 120 degrees Celsius, no preheating was applied as the HSLA steel grade and moderate section thickness do not require preheat based on the calculated carbon equivalent value (CE-IIW approximately 0.36).

After each pass, the solidified slag was removed by gentle chipping with a slag hammer followed by wire brushing of the bead surface to remove any residual slag particles that could become trapped as inclusions in subsequent passes. The bead surface was visually inspected between passes for any surface-breaking defects (cracks, porosity, undercut) that would necessitate corrective action before proceeding with the next pass.

Upon completion of the final cap pass, the weldment was allowed to cool to ambient temperature in still air. The run-on and run-off tabs were removed by flame cutting at a distance of approximately 10 mm from the plate edge, and the cut surfaces were ground smooth. The completed weld coupons were visually examined for overall bead appearance, cap width uniformity, and the absence of surface defects before proceeding to specimen extraction.

### 4.5.3 Weld Specimen Cutting

Specimen extraction from the completed weld coupons was performed using a systematic cutting plan designed to maximize the utilization of each coupon while satisfying the requirements of all planned mechanical and metallurgical tests. The cutting plan was developed in accordance with the relevant ASTM testing standards to ensure that specimen dimensions, orientations, and locations meet the specified requirements for valid test results [13][14].

The specimen cutting was performed using a precision wire-cut electric discharge machine (EDM) for specimens requiring tight dimensional tolerances (tensile specimens, Charpy impact specimens) and a band saw for preliminary rough cutting and sectioning operations. EDM cutting was preferred for final dimensioning because it produces negligible heat input to the specimen, thereby avoiding any microstructural modification of the weld metal, HAZ, or base metal regions that could influence the test results.

The cutting plan for each weld coupon allocated material for the following test specimens:
- Two full-thickness cross-weld tensile specimens (ASTM E8 sub-size flat specimens)
- Six Charpy V-notch impact specimens (three for room temperature testing, three for testing at minus 55 degrees Celsius)
- One metallographic cross-section specimen (for microhardness and microstructure examination)
- One specimen for corrosion testing (potentiodynamic polarization)
- One fractography specimen (from tested Charpy or tensile specimens)

The specimens were extracted from the central region of the weld coupon (minimum 50 mm from each end) to avoid any influence of the run-on/run-off regions or edge effects. The tensile specimens were oriented transverse to the welding direction (cross-weld orientation) to evaluate the composite strength of the weld metal-HAZ-base metal system. The Charpy impact specimens were oriented with the notch positioned in the weld metal centerline to evaluate the toughness of the deposited weld metal, which is most directly influenced by the flux composition.


### 4.5.4 Weld Specimen Mechanical Characterization

The comprehensive mechanical characterization program for the butt-welded specimens encompasses tensile testing, Charpy impact testing at multiple temperatures, fractographic analysis, Vickers microhardness mapping, microstructural examination by optical and electron microscopy, and electrochemical corrosion evaluation. This multi-faceted characterization approach provides a complete assessment of the structure-property relationships in the weldments produced with the selected adequate fluxes, enabling correlation between flux composition, weld metal microstructure, and mechanical performance.

#### 4.5.4.1 Weld Specimen Tensile Testing

Cross-weld tensile testing was performed in accordance with ASTM E8/E8M-21 standard test methods for tension testing of metallic materials [14]. The tensile test evaluates the composite mechanical response of the welded joint, encompassing contributions from the weld metal, heat-affected zone, and base metal, and determines whether the joint achieves the minimum strength requirements specified for the API X70 grade.

The tensile specimens were machined to sub-size flat specimen geometry in accordance with ASTM E8, with a gauge length of 50 mm, gauge width of 12.5 mm, and full plate thickness (22 mm) retained to represent the actual service loading condition. The weld reinforcement (cap and root excess material) was removed by machining the specimen faces flush with the plate surfaces to eliminate stress concentration effects that could cause premature failure at the weld toe.

Tensile testing was conducted on a servo-hydraulic universal testing machine (UTM) with a capacity of 600 kN, equipped with a calibrated load cell and a clip-on extensometer (50 mm gauge length, Class B-1 per ASTM E83) for precise strain measurement. The crosshead speed was maintained at 2 mm/min throughout the elastic and plastic deformation regimes, corresponding to a strain rate of approximately 6.7 x 10-4 s-1 within the gauge length, which is within the range specified by ASTM E8 for quasi-static tensile testing [14].

The tensile test data recorded for each specimen include: yield strength (0.2% offset method), ultimate tensile strength, percent elongation at fracture (over 50 mm gauge length), percent reduction in area, and the location of fracture (weld metal, HAZ, or base metal). The fracture location provides important qualitative information about the relative strength of the different joint regions. For a satisfactory weld, fracture should occur in the base metal or in a region away from the weld metal, indicating that the weld metal strength exceeds the base metal strength (overmatching condition). If fracture occurs in the weld metal, it suggests that the weld metal is the weakest link in the joint, which may require compositional modification of the flux to increase the weld metal strength.

A minimum of two tensile specimens per weld coupon were tested, and the reported values represent the average of the replicate tests. The tensile test results enable determination of joint efficiency (ratio of joint tensile strength to base metal tensile strength) and verification of compliance with API 5L specification requirements for grade X70 welded joints.

#### 4.5.4.2 Weld Specimen Impact Testing

Charpy V-notch (CVN) impact testing was performed in accordance with ASTM E23-18 standard test methods for notched bar impact testing of metallic materials [13]. The impact test evaluates the resistance of the weld metal to sudden fracture under conditions of triaxial stress and high strain rate, providing a measure of toughness that is critical for pipeline integrity assessment, particularly for pipelines operating in cold climatic regions or subjected to dynamic loading from seismic activity or hydraulic pressure transients.

The CVN specimens were machined to standard full-size dimensions of 10 mm x 10 mm x 55 mm with a 2 mm deep 45-degree V-notch positioned at the weld metal centerline. The notch was oriented parallel to the welding direction (L-T orientation) so that the fracture plane propagates transverse to the welding direction, sampling the full range of microstructural variations through the weld metal thickness (multiple passes with different thermal histories).

Impact testing was conducted at two temperatures to evaluate the ductile-to-brittle transition behavior of the weld metal: room temperature (approximately 23 degrees Celsius) and minus 55 degrees Celsius. The low-temperature testing at minus 55 degrees Celsius represents the design minimum temperature for Arctic pipeline applications and is a standard qualification requirement for offshore and northern pipeline construction projects [15]. For low-temperature testing, the specimens were conditioned in an ethanol-dry ice bath to achieve the target temperature, verified by a thermocouple in direct contact with a companion specimen, and tested within 5 seconds of removal from the cooling medium as specified by ASTM E23 [13].

The impact tests were performed on a calibrated Charpy pendulum impact testing machine with a capacity of 300 joules. Three specimens per test temperature per weld coupon were tested, and the reported values include the average absorbed energy (joules), individual specimen values, and the lateral expansion measurements (mm) as supplementary ductility indicators. The fracture surfaces of the tested CVN specimens were retained for subsequent fractographic analysis.

The acceptance criterion for pipeline girth weld metals typically requires a minimum average absorbed energy of 40 joules at the design minimum temperature, with no individual value below 30 joules [15]. These criteria ensure adequate resistance to brittle fracture initiation and propagation under the most severe anticipated service conditions.

#### 4.5.4.3 Fractography Analysis of Weld Specimen

Fractographic analysis of the failed tensile and impact specimens was conducted using scanning electron microscopy (SEM) to characterize the fracture mechanisms operative in the weld metals produced with the selected adequate fluxes. Fractography provides direct visual evidence of the micromechanisms of fracture (ductile microvoid coalescence, transgranular cleavage, intergranular fracture, or mixed-mode fracture) and enables identification of microstructural features or defects that initiated or influenced the fracture process [3].

The fracture surfaces of selected tensile and Charpy impact specimens were carefully extracted from the broken halves using a low-speed diamond saw, trimmed to appropriate dimensions for SEM sample holders, and ultrasonically cleaned in acetone to remove any contamination or loose debris without disturbing the fracture surface morphology. The cleaned specimens were mounted on aluminum SEM stubs using conductive carbon tape and coated with a thin layer (approximately 10 nm) of gold-palladium alloy by sputter coating to prevent charging artifacts during electron beam imaging.

Fractographic examination was performed on a field-emission scanning electron microscope (FE-SEM) operating at an accelerating voltage of 15-20 kV with a working distance of approximately 10 mm. Secondary electron (SE) imaging mode was employed for topographic contrast of the fracture surface features, while backscattered electron (BSE) mode was occasionally used to identify compositional variations (e.g., non-metallic inclusions on the fracture surface). Energy-dispersive X-ray spectroscopy (EDS) analysis was performed on selected features of interest (inclusions, second-phase particles, or unusual fracture initiation sites) to determine their chemical composition and assess their role in the fracture process.

The fractographic observations were documented at multiple magnifications ranging from low magnification (50-100x) for overview imaging of the overall fracture surface morphology and identification of fracture initiation sites, to high magnification (2000-5000x) for detailed characterization of individual microvoid dimples, cleavage facets, or inclusion particles. The fracture surface characteristics were correlated with the mechanical test data (absorbed energy for impact specimens, ductility for tensile specimens) and with the weld metal microstructure to develop comprehensive understanding of the structure-property-fracture relationships.

For the room temperature impact specimens, the fracture surfaces were expected to exhibit predominantly ductile features (equiaxed and elongated microvoid dimples) characteristic of microvoid coalescence fracture, while the specimens tested at minus 55 degrees Celsius may exhibit varying proportions of cleavage facets depending on the weld metal toughness at this temperature. The size, distribution, and nucleating particles (inclusions or second-phase particles) of the microvoid dimples provide information about the inclusion population in the weld metal, which is directly influenced by the flux composition through the slag-metal oxygen equilibrium.

#### 4.5.4.4 Weld Specimen Microhardness Testing

Vickers microhardness testing of the butt weld cross-sections was performed to map the hardness distribution across the complete joint profile, encompassing the base metal, coarse-grained heat-affected zone (CGHAZ), fine-grained heat-affected zone (FGHAZ), intercritical heat-affected zone (ICHAZ), weld metal (all passes including root, fill, and cap), and the corresponding zones on the opposite side of the joint. The microhardness profile provides spatially resolved information about the microstructural gradients that develop as a consequence of the multi-pass thermal cycles and the progressive dilution effects inherent in the SAW process.

The microhardness specimens were prepared following the metallographic procedures described in Section 4.4.3 (mounting, grinding through 1200 grit, polishing to 1 micrometer diamond finish). Prior to indentation, the polished specimens were lightly etched with 2% nital (2% HNO3 in ethanol) to reveal the weld profile boundaries and facilitate precise positioning of the hardness traverses within the regions of interest.

Microhardness measurements were performed using a Vickers hardness tester with automated stage control, employing a test load of 500 gf (HV0.5) and a dwell time of 10 seconds. Two types of measurement patterns were employed:

(a) **Horizontal traverse**: A line of indentations across the mid-thickness of the weld, traversing from base metal through HAZ, weld metal, opposite HAZ, to opposite base metal. Indentation spacing of 0.5 mm providing a complete hardness profile across the joint width.

(b) **Vertical traverse**: A line of indentations from the cap surface to the root, positioned at the weld metal centerline to capture the hardness variation through the different weld passes (cap, fill passes, root). This traverse reveals the influence of progressive thermal cycling (tempering effects of subsequent passes on earlier passes) on the hardness distribution.

The combined horizontal and vertical hardness traverses provide a comprehensive two-dimensional map of the mechanical property distribution within the joint, which can be correlated with the microstructural zones identified through optical microscopy. Particular attention was given to identifying any localized hardness peaks in the CGHAZ region, which is susceptible to the formation of martensite or upper bainite at the cooling rates experienced during SAW of low-carbon HSLA steels [3].

The maximum allowable hardness for pipeline girth welds in sour service environments is typically limited to 250 HV10 (or approximately 275 HV0.5 considering the load-dependent indentation size effect) to prevent sulfide stress cracking (SSC) in the presence of hydrogen sulfide [15]. The microhardness results were evaluated against this criterion to assess the suitability of the weldments for potential sour service applications.

#### 4.5.4.5 Weld Specimen Microstructure Analysis

The microstructural characterization of the butt weld cross-sections was performed using optical microscopy (OM) and scanning electron microscopy (SEM) to identify and quantify the constituent microstructural phases in the weld metal, HAZ sub-zones, and base metal. The microstructure directly governs the mechanical properties of the weldment, and its characterization enables fundamental understanding of the relationships between flux composition, welding thermal cycles, and resultant mechanical performance.

Metallographic specimen preparation followed the standard sequence of sectioning, mounting, grinding, and polishing as described previously. For microstructural revelation, two etchant solutions were employed:

(a) **2% Nital** (2% HNO3 in ethanol): Applied by immersion for 5-15 seconds to reveal the general microstructure including grain boundaries, ferrite phases (polygonal ferrite, acicular ferrite, Widmanstatten ferrite), pearlite colonies, and bainitic constituents. Nital is the standard etchant for low-carbon and low-alloy steels and provides good contrast between the various ferrite morphologies [3].

(b) **LePera's reagent** (1% Na2S2O5 in water mixed 1:1 with 4% picric acid in ethanol): Applied to selected specimens to differentiate martensite-austenite (M-A) constituents from the ferrite matrix. LePera etching colors the M-A constituents white against a brown-tan ferrite background, enabling their identification and quantification by image analysis.

Optical microscopy was performed at magnifications ranging from 50x (for overview of weld profile, number of passes, and bead geometry) to 1000x (for detailed phase identification and grain size measurement). Digital images were captured at standardized magnifications for each zone of interest: base metal, CGHAZ (directly adjacent to the fusion line), FGHAZ, ICHAZ, weld metal cap pass, weld metal fill passes, and weld metal root pass.

The weld metal microstructure was characterized in terms of the proportion of the following constituent phases: acicular ferrite (AF), grain boundary ferrite (GBF), Widmanstatten side-plate ferrite (WF), polygonal ferrite (PF), and bainite (B). The volume fraction of acicular ferrite is of particular interest because this phase provides the optimum combination of strength and toughness in SAW weld metals due to its fine effective grain size, high-angle boundary misorientation, and interlocking plate morphology that provides resistance to cleavage crack propagation [3].

Point counting and image analysis techniques were employed to quantify the volume fractions of the various microstructural constituents. A minimum of 10 fields of view were analyzed for each zone of each specimen to ensure statistical reliability of the quantification results. The acicular ferrite content in the weld metals was correlated with the TiO2 content of the flux (as the primary source of titanium-rich inclusions that nucleate AF) and with the measured impact toughness values.

SEM examination at higher magnifications (2000-10000x) was employed to resolve fine microstructural details that are beyond the resolution limit of optical microscopy, including the morphology of non-metallic inclusions (size, shape, and spatial distribution), the internal structure of bainitic constituents (lath width, carbide precipitation patterns), and the characteristics of M-A constituents in the HAZ.

#### 4.5.4.6 Weld Specimen Corrosion Analysis

The corrosion resistance of the weld metals produced with the selected adequate fluxes was evaluated using potentiodynamic polarization testing, which provides quantitative assessment of the electrochemical corrosion behavior under simulated service conditions. The corrosion performance of SAW weld metals is influenced by several flux-dependent factors including the weld metal chemical composition (particularly manganese, silicon, and oxygen content), the inclusion population (size, number density, and chemistry), and the microstructural constituents present [3].

The potentiodynamic polarization tests were conducted in a conventional three-electrode electrochemical cell configuration using a computer-controlled potentiostat/galvanostat system. The three electrodes comprised:
- Working electrode: The weld metal specimen (exposed area approximately 1 cm2)
- Reference electrode: Saturated calomel electrode (SCE)
- Counter electrode: Platinum mesh

The electrolyte solution was 3.5 weight percent sodium chloride (NaCl) in deionized water, representing a standardized simulated seawater environment commonly used for comparative corrosion evaluation of structural steels and weldments. The solution was maintained at ambient temperature (approximately 23 degrees Celsius) and was naturally aerated (no deaeration or gas purging) to represent realistic exposure conditions.

The weld metal specimens for corrosion testing were prepared by sectioning a representative cross-section from the butt weld coupon, mounting in cold-cure epoxy resin (to avoid thermal effects of hot mounting), and polishing to a 1200 grit surface finish. The specimen was masked with inert lacquer to expose only the weld metal region (approximately 10 mm x 10 mm area) to the electrolyte, ensuring that the measured corrosion response is attributable solely to the weld metal rather than a composite response of weld metal, HAZ, and base metal.

Prior to each polarization test, the specimen was immersed in the 3.5% NaCl solution for a minimum stabilization period of 60 minutes to allow the open-circuit potential (OCP) to reach a stable value (drift rate less than 1 mV/min). This stabilization period ensures that the passive film (if any) has reached a quasi-steady state condition before the potentiodynamic scan is initiated.

The potentiodynamic polarization scan was performed from -250 mV vs. OCP (cathodic initiation potential) to +250 mV vs. OCP (anodic termination potential) at a constant scan rate of 1 mV/s. This scan range and rate are sufficient to characterize the cathodic reduction kinetics (dissolved oxygen reduction and/or hydrogen evolution), the corrosion potential (Ecorr), the anodic dissolution behavior, and any passivation phenomena that may occur within the scanned potential range.

The following electrochemical parameters were extracted from the polarization curves using Tafel extrapolation of the linear regions of the anodic and cathodic branches:
- Corrosion potential, Ecorr (mV vs. SCE)
- Corrosion current density, icorr (microamperes/cm2)
- Anodic Tafel slope, ba (mV/decade)
- Cathodic Tafel slope, bc (mV/decade)
- Polarization resistance, Rp (ohm.cm2)
- Corrosion rate (mm/year), calculated from icorr using Faraday's law

The corrosion rate provides a direct measure of the material loss per unit time under the specified environmental conditions and enables ranking of the weld metals produced with different flux formulations in terms of their corrosion resistance. Lower corrosion rate values indicate superior corrosion performance and longer anticipated service life under similar environmental exposure. The corrosion results were correlated with the weld metal chemical composition and microstructure to identify the flux-dependent factors that most significantly influence the corrosion behavior of the SAW weld metals.

Comparative evaluation was also performed against the base metal (API X70) corrosion behavior tested under identical conditions. In a properly designed welded joint, the weld metal corrosion rate should be comparable to or lower than the base metal corrosion rate to avoid preferential attack at the weld region, which could lead to localized wall thinning and premature failure in pipeline service.


---

## References

[1] Anderson, V. L., & McLean, R. A. (1974). *Design of experiments: A realistic approach*. Marcel Dekker.

[2] Cornell, J. A. (2011). *Experiments with mixtures* (3rd ed.). Wiley.

[3] Kou, S. (2003). *Welding metallurgy* (2nd ed.). John Wiley & Sons.

[4] Mukerji, J. (1965). Phase equilibrium diagram CaO-CaF2-2CaO.SiO2. *Journal of the American Ceramic Society*, 48(4), 210-213.

[5] Kang, Y.-B., et al. (2006). Critical thermodynamic evaluation of MnO-TiO2-Ti2O3. *Calphad*, 30(3), 235-247.

[6] Sarkar, A., et al. (2018). Thermodynamic evaluation of BaO-SiO2 and BaO-CaO-SiO2. *Calphad*, 61, 140-147.

[7] Sharma, L., & Chhibber, R. (2019). Design of SAW slags using CaO-SiO2-CaF2. *Silicon*, 11, 2763-2773.

[8] Kumar, R., et al. (2018). Determination of flux consumption in SAW. *Global Journal of Research in Engineering*, 12(3), 15-24.

[9] Waris, K. N., & Chhibber, R. (2021). Characterization of CaO-CaF2-TiO2-SiO2 welding slags. *Silicon*, 13(7), 2441-2457.

[10] Hot Disk Instruments. (2025). Thermal conductivity measurement systems.

[11] White, G. K., & Collocott, S. J. (2022). Novel methods for thermal diffusivity measurement. *International Journal of Heat and Mass Transfer*, 186, 122463.

[12] Thamaphat, K., et al. (2008). Phase characterization of TiO2 by XRD and TEM. *Agriculture and Natural Resources*, 42(3), 357-361.

[13] ASTM E23-18. Standard test methods for notched bar impact testing of metallic materials.

[14] ASTM E8/E8M-21. Standard test methods for tension testing of metallic materials.

[15] Grey, J. M. (2002). An independent view of linepipe and linepipe steel for high strength pipelines.

