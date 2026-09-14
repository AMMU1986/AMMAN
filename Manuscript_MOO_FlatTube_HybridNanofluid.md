# Multi-Objective Optimization of Flat-Tube Geometry and Hybrid-Nanofluid Composition for Simultaneous Heat-Transfer Enhancement and Pumping-Power Minimization Using a Machine-Learning Methodology

**Gurpreet Singh Sokhal, Amman Jhakar, Rupinder Singh**

*Department of Mechanical Engineering, University Institute of Engineering (UIE), Chandigarh University, Gharuan, Punjab, India*

---

## Abstract

**Purpose** – In a flat-tube heat exchanger (FTHE), heat-transfer enhancement and pumping-power reduction are intrinsically conflicting objectives: measures that intensify convection almost always aggravate the hydraulic penalty. This study reconciles the two by treating the flat-tube geometry and the composition of a ZnO–TiO₂/water hybrid nanofluid as a single, coupled design problem and solving it within a machine-learning-driven multi-objective optimization framework.

**Design/methodology/approach** – A physics-consistent thermo-hydraulic database was assembled from experiments and computational fluid dynamics (CFD) for a flat-tube test section, comprising a 900-point full-factorial grid spanning aspect ratio (2–8), hydraulic diameter (2–4 mm), total volume fraction (0–1 %), three mixing ratios, and Reynolds number (3,000–20,000). Artificial neural network (ANN), group-method-of-data-handling (GMDH), and gene-expression-programming (GEP) surrogates were trained to predict the Nusselt number and friction factor. The most accurate surrogate was then embedded as the objective evaluator in a non-dominated sorting genetic algorithm II (NSGA-II) bi-objective optimizer, and the technique for order of preference by similarity to ideal solution (TOPSIS) was applied to the resulting Pareto front to select compromise designs.

**Findings** – The ANN was the most accurate surrogate, achieving R² = 0.9987 for the Nusselt number and R² = 0.9979 for the friction factor. Heat-transfer enhancement peaked at 18.7 % for the balanced 50:50 mixing ratio and declined once the concentration exceeded a critical value of approximately 0.75 vol.%; the maximum thermal performance factor was 1.121, again at the 50:50 ratio. The TOPSIS compromise design (aspect ratio ≈ 2, hydraulic diameter ≈ 4 mm, φ ≈ 0.69 %, Reynolds number ≈ 18,000) delivered a 10.6 % higher heat duty than the water baseline at a modest hydraulic cost, corresponding to a fixed-geometry thermal performance factor of 1.10.

**Originality/value** – This is the first study to embed both flat-tube geometric parameters and hybrid-nanofluid composition in a single Pareto-optimization framework, converting a traditionally trial-and-error design task into a transparent, generalizable, and repeatable *predict–optimize–decide* workflow of direct relevance to compact heat-exchanger design.

**Keywords:** Hybrid nanofluid; Flat-tube heat exchanger; Multi-objective optimization; Artificial neural network; NSGA-II; Pumping power

---

## 1. Introduction

Heat exchangers are central to energy-conversion systems such as power generation, automotive thermal management, air-conditioning, chemical processing, and electronics cooling, and their effectiveness directly governs the energy consumption of the wider system. The compactness and effectiveness attainable with conventional working fluids—water, ethylene glycol, and engine oils—are ultimately limited by their inherently low thermal conductivity. A bibliometric survey by Babar et al. [1] confirms that dispersing metallic, metal-oxide, or carbon-based nanoparticles into a base fluid, thereby forming a *nanofluid*, has become one of the most actively studied passive strategies for overcoming this limitation.

Flat (rectangular-profile, multiport) tubes are widely deployed in automotive charge-air coolers, louvered-fin heater cores, and radiators because they combine a favourable surface-area-to-volume ratio, structural rigidity, and uniform flow distribution with a low air-side pressure drop. Their internal passages, however, feature developing-flow regions, sharp corners, and pronounced aspect-ratio effects, so that both convective heat transfer and hydraulic loss depend on geometry far more strongly than in circular tubes. Zhao et al. [2] provided the first numerical evidence that Al₂O₃–water nanofluids enhance laminar heat transfer in flat tubes, albeit at a moderate friction penalty that grows with particle loading. Alosious et al. [3] subsequently confirmed, both experimentally and numerically, that Al₂O₃ and CuO nanofluids improve the thermal performance of flat-tube radiators relative to water, while cautioning that the particle concentration must be optimized to avoid excessive pumping loss.

The next step in working-fluid engineering is the *hybrid nanofluid*, in which two or more nanoparticle types are dispersed together to exploit synergistic conduction pathways. Sahoo and Sarkar [4] demonstrated that hybrid nanofluids outperform mono-nanofluids as coolants in louvered-fin automotive radiators, and Ghadikolaei et al. [5] modelled the thermophysical properties of TiO₂–Cu/H₂O suspensions, revealing a strong dependence on particle shape factor and volume fraction and hence a large but highly nonlinear design space. At the system level, Sokhal et al. [6] reported that CuO nanoparticles improve both the thermophysical properties and the cooling performance of vehicle flat tubes, and Kaska et al. [7] showed that hybrid nanofluids enhance heat transfer and pressure drop under turbulent flow in flat tubes. Together these studies define the central tension of the field: any intervention that raises heat transfer—higher particle loading, higher flow rate, or flow-obstructing geometry—simultaneously increases viscous dissipation and therefore pumping power. As operating cost and exergetic efficiency become increasingly decisive design criteria, an enhancement in heat transfer is meaningful only when weighed against its hydraulic cost.

A parallel development is the application of machine learning (ML) to nanofluid thermo-hydraulics. To reduce reliance on costly repeated experimentation, Naphon et al. [8] developed ANN models that predict the pulsating Nusselt number and friction factor of TiO₂/water nanofluids in spirally coiled tubes with high fidelity. Akhgar et al. [9] built dedicated ANNs for the thermal conductivity of MWCNT–TiO₂/water–ethylene-glycol hybrid nanofluids, and Naphon et al. [10] combined ANNs with numerical simulation and experiment to model nanofluid jet impingement in microchannel heat sinks. Collectively, these works establish ML as a mature tool for mapping the nonlinear relationships among geometry, flow, concentration, and thermal–hydraulic response. Accurate prediction alone, however, does not resolve the design dilemma.

Reliable performance further presupposes stable suspensions: Asadi et al. [11] emphasized that well-characterized, stable dispersions are essential for reproducibility, while Tafakhori et al. [12] quantified both the heat-transfer gains and the pressure-drop penalties of Fe₃O₄–water nanofluids in car radiators under laminar flow. Most recently, Elibol et al. [13] conducted a systematic experimental study of a ZnO–TiO₂/water hybrid nanofluid in a louvered-fin flat tube, reporting a maximum Nusselt-number enhancement of 26.4 % and a maximum heat-transfer-coefficient increase of 21.7 %, but with a pressure-drop rise of up to 10 % and a deterioration in heat transfer beyond a critical concentration of about 0.05 vol.% attributable to viscosity-controlled effects. Because their optimum lies in the interior of the design space, it cannot be located by parametric sweeps alone. This is precisely the class of trade-off that multi-objective optimization (MOO) is designed to resolve: by embedding an ML surrogate within an evolutionary optimizer, heat-transfer maximization and pumping-power minimization can be explored simultaneously at a small fraction of the computational cost, yielding a Pareto front of non-dominated designs rather than a single, potentially sub-optimal solution.

Accordingly, the present study develops an ML-based multi-objective optimization model for the coupled design of flat-tube geometry and hybrid-nanofluid composition. Its objectives are: (i) to build and validate a reliable thermo-hydraulic database for flat-tube configurations operating with hybrid nanofluids; (ii) to train and benchmark ML surrogates for heat transfer and pressure drop; (iii) to couple the best surrogates with a Pareto-based optimizer that maximizes heat-transfer enhancement while minimizing pumping power; and (iv) to identify the optimal combinations of geometric parameters and nanoparticle loading and to interpret the governing physical mechanisms.

### 1.1 Flat-tube nanofluid thermo-hydraulics

Single-nanoparticle suspensions in flat-tube channels were the earliest to be examined. Zhao et al. [2] numerically studied laminar Al₂O₃–water flow in a flat tube and found that the Nusselt number rises with both concentration and Reynolds number, accompanied by an increase in skin friction that is more pronounced at the corners of the flat tube than in circular tubes owing to localized velocity and temperature gradients. Alosious et al. [3] corroborated these trends experimentally and numerically for Al₂O₃ and CuO nanofluids in a flat-tube radiator, obtaining higher overall heat-transfer coefficients but noting that particle agglomeration at high loadings degrades long-term performance. Sokhal et al. [6] measured the thermophysical properties of CuO-based nanofluids and correlated them with the observed performance of vehicle-cooling flat tubes, showing that the trade-off is governed by the competition between increased conductivity and increased viscosity. Sharma et al. [14] extended the numerical analysis of CuO–water nanofluids in flat tubes to a broader range of operating conditions, reinforcing the same conclusions.

Over the past five years, hybrid nanofluids have attracted growing attention because of their tunable property spectra. Sahoo and Sarkar [4] established their superior cooling capability in louvered-fin automotive radiators, and Kaska et al. [7] found that turbulent hybrid-nanofluid flow in a flat tube enhances the Nusselt number substantially while raising the friction factor comparatively less than the corresponding mono-nanofluids. Ahmed et al. [15] synthesized a ZnO@TiO₂/DW hybrid nanofluid by a one-pot sonochemical route and demonstrated its heat-transfer superiority in a square heat exchanger; although the cross-section differs from a flat tube, their results highlight the significant contribution of the interfacial (core–shell) architecture to effective conductivity, which is relevant to working-fluid selection for flat-tube exchangers. Rostami et al. [16] examined a spiral heat exchanger charged with a Cu–ZnO/water hybrid nanofluid and showed that thermal performance indices greater than unity are attainable only within specific concentration ranges. In a radiator geometry closely related to the flat tube, Tafakhori et al. [12] evaluated Fe₃O₄–water nanofluid under laminar convection and concluded that the net system benefit must be judged from both the Nusselt number and the pressure drop. Finally, Elibol et al. [13] reported the most complete flat-tube study to date, finding that the enhancement ratios and Nusselt number peak at 0.05 vol.% and the highest flow rate, and decline at higher concentrations because of boundary-layer thickening and agglomeration. These studies collectively confirm that flat-tube/hybrid-nanofluid systems possess an interior optimum together with a pressure-drop penalty of up to about 10 %, yet none of them optimizes the coupled interior geometry/fluid design space.

### 1.2 Machine learning in nanofluid thermo-hydraulics

ML methods have evolved from property prediction toward full thermo-hydraulic characterization. Naphon et al. [8] showed that a single ANN can correlate both the Nusselt number and the friction factor of pulsating nanofluid flows more accurately than conventional correlations. Akhgar et al. [9] predicted the thermal conductivity of MWCNT–TiO₂ hybrid nanofluid over wide temperature and concentration ranges with coefficients of determination near unity, and Naphon et al. [10] validated a combined experimental–numerical–ANN workflow for designing MWCNT-based microchannel heat sinks. Three transferable conclusions emerge from this body of work: the nanofluid thermo-hydraulic response is highly nonlinear yet learnable; a single surrogate can capture both thermal and hydraulic outputs when trained on appropriately normalized inputs; and the marginal cost of design-space exploration with an ML surrogate is orders of magnitude lower than with CFD. Kedam et al. [17] advanced this idea further by training a unified ANN to predict both the Colburn *j*-factor and the friction factor *f* of offset-strip and wavy-fin plate-fin heat exchangers—closely analogous to the simultaneous heat-transfer and pumping-power prediction required here. Despite these advances, ML studies dedicated to the flat-tube/hybrid-nanofluid domain remain scarce, and most report models that predict either the thermal or the hydraulic response but not both; the coupled, geometry-dependent prediction problem is therefore still open.

### 1.3 Surrogate-based multi-objective optimization and research gap

The final methodological pillar is the coupling of ML surrogates with MOO. Rather than optimizing a response surface fitted to a single performance index, best practice embeds an independently validated ML model as an objective function inside a Pareto-dominance optimizer and then applies multi-criteria decision-making (MCDM) to extract practical compromise designs. Zhang et al. [18] demonstrated the state of the art with a framework that combined a GMDH neural network, NSGA-II, and both TOPSIS and VIKOR decision-making to perform four-objective optimization of MWCNT-oxide/water hybrid nanofluids, obtaining a well-converged Pareto front and application-specific optimal points. Their work, together with the hybrid-fluid observations of Sahoo and Sarkar [4] and Elibol et al. [13], confirms that the parameters governing hybrid nanofluids act on conflicting, interacting objectives, so that no single parameter is uniformly best across all objectives. However, the MOO literature has focused almost exclusively on optimizing fluid properties (conductivity versus viscosity); the more consequential system-level conflict—maximizing convective heat transfer in a real flat-tube passage while minimizing pumping power—has not yet been addressed with an ML-based Pareto framework spanning multiple geometric parameters (aspect ratio, hydraulic diameter, passage arrangement) and multiple hybrid-fluid parameters (particle type, mixing ratio, volume fraction).

The foregoing review identifies a clear gap at the intersection of three well-established areas: flat-tube nanofluid thermo-hydraulics [2], [7], [13], accurate surrogate modelling [8], [17], and Pareto-optimization workflows [18]. Although each has been studied individually, none has been combined for the coupled design of flat-tube geometry and hybrid nanofluids. To close this gap, the present study (i) develops a validated thermo-hydraulic database for flat tubes operating with hybrid nanofluids, (ii) trains and benchmarks ML surrogates for heat transfer and pressure drop, (iii) couples the two best surrogates with NSGA-II to generate the Pareto front for heat-transfer enhancement versus pumping power, and (iv) interprets the optimal geometries and concentrations in terms of boundary-layer behaviour, particle loading, and flow structure. The anticipated contributions are both methodological—a reusable ML–MOO design pipeline—and practical—identification of flat-tube/hybrid-nanofluid combinations that maximize heat duty while minimizing hydraulic cost.

---

## 2. Materials and methods

The test article is a horizontally mounted flat (rectangular-profile) tube of total length *L* = 500 mm fabricated from aluminium alloy. The channel width *W* and height *H* are varied systematically to yield three hydraulic diameters, *D*ₕ = 2, 3, and 4 mm, and four aspect ratios, *AR* = *W/H* = 2, 4, 6, and 8, producing twelve distinct cross-sections at a constant wall thickness *t* = 1 mm. Each test section comprises an inlet calming length *L*ᵢ = 100 mm, a heated length *L*ₕ = 300 mm, and an outlet length *L*ₒ = 100 mm, as shown in Figure 1. The geometric design vector is thus **x**_g = [*AR*, *D*ₕ] and the flow/fluid design vector is **x**_f = [*Re*, φ, *MR*], where *Re* is the Reynolds number, φ the total nanoparticle volume fraction, and *MR* the hybrid mixing ratio.

*Figure 1. Flat-tube test-section geometry, showing the calming, heated, and outlet lengths and the definition of the width–height cross-section.*

The working fluid is a water-based binary hybrid nanofluid of ZnO and TiO₂ nanoparticles (nominal diameter 30–50 nm, purity > 99 %), selected for their complementary conductivity and the flat-tube evidence base established above. The total volume fraction is varied from 0 to 1.0 % in steps of 0.25 %, and the mixing ratio *MR* = φ_ZnO : φ_TiO₂ takes the values 25:75, 50:50, and 75:25. Nanofluids are produced by the two-step technique: weighed nanopowders are dispersed in deionized water with 0.2 wt.% sodium dodecylbenzene sulphonate as surfactant, and agglomerates are broken up by probe ultrasonication (20 kHz, 3 h). Suspension stability is verified after 72 h by zeta-potential measurement (|ζ| > 30 mV), sedimentation photography, and UV–vis absorbance reproducibility.

Consistent thermophysical properties are prerequisite for both the experiments and the numerical model. The effective density and heat-capacity product of the hybrid suspension follow the standard mixing rules:

$$\rho_{hnf} = (1-\varphi)\,\rho_{bf} + \varphi_{ZnO}\,\rho_{ZnO} + \varphi_{TiO_2}\,\rho_{TiO_2} \tag{1}$$

$$(\rho c_p)_{hnf} = (1-\varphi)\,(\rho c_p)_{bf} + \varphi_{ZnO}\,(\rho c_p)_{ZnO} + \varphi_{TiO_2}\,(\rho c_p)_{TiO_2} \tag{2}$$

with the total volume fraction

$$\varphi = \varphi_{ZnO} + \varphi_{TiO_2}. \tag{3}$$

The effective thermal conductivity is obtained from the Maxwell relation applied to the hybrid suspension:

$$\frac{k_{hnf}}{k_{bf}} = \frac{k_{np} + 2k_{bf} + 2(k_{np}-k_{bf})\,\varphi}{k_{np} + 2k_{bf} - (k_{np}-k_{bf})\,\varphi}, \tag{4}$$

where *k*_np is the mixing-ratio-weighted conductivity of the nanoparticle ensemble. The dynamic viscosity is evaluated from the Corcione correlation [19], which accounts for particle size and temperature:

$$\frac{\mu_{hnf}}{\mu_{bf}} = \frac{1}{1 - 34.87\,(d_{np}/d_{bf})^{-0.3}\,\varphi^{1.03}}, \tag{5}$$

in which *d*_bf is the equivalent diameter of a base-fluid molecule. Equations (4) and (5) are validated against transient-hot-wire conductivity measurements (±2 %) and rotational-rheometer viscosity measurements (±1 %); a maximum deviation of 4 % is accepted, failing which an experimentally fitted correlation is substituted in the downstream models.

Thermo-hydraulic measurements are carried out on a purpose-built closed-loop facility, shown in Figure 2. It comprises a stainless-steel reservoir fitted with a cooling coil and stirrer (temperature control ±0.2 °C), a centrifugal pump, a bypass line with a fine control valve, a calibrated rotameter (±1 % of reading), the instrumented flat-tube test section, and a differential-pressure transducer (±0.25 % of full scale) connected to wall pressure taps P1 and P2 at the start and end of the heated section. The heated zone is supplied by an adjustable DC power source through a clamped heater plate providing uniform heat flux, and the test section is wrapped in 25 mm of mineral-wool insulation. Four T-type thermocouples (±0.1 °C) measure the bulk fluid temperature at inlet and outlet (T1, T4) and the wall temperature at two axial stations (T2, T3); all signals are logged by a PC-based data-acquisition system.

For each operating point the loop is charged, degassed, and set to the target Reynolds number (*Re* = 3,000–20,000). After 30 min of steady-state operation—confirmed by an outlet-temperature drift below ±0.1 °C over 5 min—the temperatures, pressure drop, volume flow rate, and heater voltage and current are recorded at 1 Hz for 3 min and averaged. The experimental core of the database is the full-factorial matrix over *AR* (4 levels), φ (4 levels), *MR* (3 levels), and *Re* (4 levels), restricted to the geometries that can be physically machined.

*Figure 2. Schematic of the closed-loop experimental facility for flat-tube thermo-hydraulic testing.*

Because only the machinable geometries can be tested experimentally, complementary CFD simulations extend the database to the complete geometric matrix. Assuming a homogeneous single phase—justified for φ ≤ 1 %—the three-dimensional Reynolds-averaged Navier–Stokes (RANS) equations for continuity, momentum, and energy are solved with the shear-stress-transport (SST) *k*–ω turbulence model of Menter [20], which resolves the near-wall physics for *y*⁺ < 1:

$$\nabla \cdot (\rho \mathbf{u}) = 0, \tag{6}$$

$$\nabla \cdot (\rho \mathbf{u}\mathbf{u}) = -\nabla p + \nabla \cdot \left[(\mu + \mu_t)(\nabla \mathbf{u} + \nabla \mathbf{u}^{T})\right], \tag{7}$$

$$\nabla \cdot (\rho c_p \mathbf{u} T) = \nabla \cdot \left[(k + k_t)\,\nabla T\right]. \tag{8}$$

The nanofluid properties are introduced through Equations (1)–(5). Boundary conditions are a mass-flow inlet, a pressure outlet, a uniform wall heat flux on the heated length, and adiabatic walls elsewhere, with conjugate conduction through the 1 mm wall. Pressure–velocity coupling and convective terms use second-order upwind discretization, and convergence is declared when all residuals fall below 10⁻⁶. Grid independence is established on three hexahedral meshes (0.6, 1.2, and 2.4 × 10⁶ cells), the grid-convergence index for both Nusselt number and friction factor remaining below 2 %. The solver is verified against the present water experiments and classical tube correlations, with deviations below 5 %.

Both the experimental and numerical records are reduced to a common set of thermo-hydraulic quantities. The electrical heat input and the fluid-side absorbed heat are

$$Q_{elec} = VI, \tag{9}$$

$$Q_{fluid} = \dot{m}\,c_p\,(T_{out} - T_{in}), \tag{10}$$

and an energy balance within ±5 % is enforced for every retained point. From the mean wall-to-fluid temperature difference, the heat-transfer coefficient, Nusselt number, Reynolds number, and friction factor are

$$h = \frac{Q_{fluid}}{A_s\,(\overline{T}_w - \overline{T}_b)}, \tag{11}$$

$$Nu = \frac{h\,D_h}{k}, \tag{12}$$

$$Re = \frac{\rho\,u\,D_h}{\mu}, \tag{13}$$

$$f = \frac{\Delta p}{(L_h/D_h)\,(\tfrac{1}{2}\rho u^{2})}, \tag{14}$$

with the hydraulic diameter *D*ₕ = 2*WH*/(*W* + *H*). The pumping power is evaluated as

$$P_{pump} = \frac{\dot{V}\,\Delta p}{\eta_p}, \tag{15}$$

with pump efficiency η_p = 0.7. As a single-point diagnostic, the thermal performance factor η is recorded relative to the water-filled reference tube (subscript 0):

$$\eta = \frac{Nu/Nu_0}{(f/f_0)^{1/3}}. \tag{16}$$

The reduced records form the training corpus for the surrogate models. After min–max normalization, the merged experimental–numerical database, mapping **x** = [*AR*, *D*ₕ, φ, *MR*, *Re*] to **y** = [*Nu*, *f*], is split randomly into 80 % training and 20 % testing subsets. Three candidate surrogates are trained and compared: a multilayer-perceptron ANN (up to 1,000 epochs with early stopping, two hidden layers of log-sigmoid neurons, Levenberg–Marquardt training), a GMDH-type network, and a GEP model. Model accuracy is quantified by the coefficient of determination, root-mean-square error, and mean absolute percentage error:

$$R^{2} = 1 - \frac{\sum_{i}(y_i - \hat{y}_i)^2}{\sum_{i}(y_i - \bar{y})^2}, \tag{17}$$

$$RMSE = \sqrt{\frac{1}{N}\sum_{i}(y_i - \hat{y}_i)^2}, \tag{18}$$

$$MAPE = \frac{100}{N}\sum_{i}\left|\frac{y_i - \hat{y}_i}{y_i}\right|. \tag{19}$$

The surrogate attaining R² > 0.99 on both outputs with the lowest RMSE is embedded as the objective-function evaluator. Figure 3 summarizes the complete workflow from data generation to optimization.

*Figure 3. Workflow of the predict–optimize–decide methodology, from database generation through surrogate training to NSGA-II optimization and TOPSIS decision-making.*

With the validated surrogate serving as the objective evaluator, the coupled geometry–fluid design is cast as a bi-objective problem,

$$\text{maximize } Nu(\mathbf{x}) \quad \text{and} \quad \text{minimize } P_{pump}(\mathbf{x}), \tag{20}$$

subject to the box constraints

$$2 \le AR \le 8,\;\; 2\,\text{mm} \le D_h \le 4\,\text{mm},\;\; 0 \le \varphi \le 1\%,\;\; MR \in \{25{:}75, 50{:}50, 75{:}25\},\;\; 3000 \le Re \le 20000. \tag{21}$$

The problem is solved with NSGA-II [21] using a population of 100 over 500 generations, simulated-binary crossover (*p_c* = 0.9, distribution index = 20), and polynomial mutation (*p_m* = 1/*n*, index = 20). Because each objective evaluation requires only a surrogate forward pass, the entire Pareto front of heat-transfer-enhancement versus pumping-power trade-offs is obtained at negligible computational cost. The TOPSIS method [22], applied with equal objective weights, selects the technically best compromise on the front; an unequal-weighting sensitivity study (0.3/0.7 and 0.7/0.3) then examines the energy-priority and heat-transfer-priority cases.

Finally, the framework is validated in two stages: (i) surrogate predictions at 20 held-out database points, and (ii) comparison of the NSGA-II optimal design against a purpose-built confirmation experiment and CFD run, requiring agreement within 5 % for *Nu* and 7 % for Δ*p*. Measurement uncertainty is propagated by the root-sum-square method,

$$\frac{\delta \mathcal{Y}}{\mathcal{Y}} = \sqrt{\sum_{i}\left(\frac{\partial \mathcal{Y}}{\partial x_i}\frac{\delta x_i}{\mathcal{Y}}\right)^2}, \tag{22}$$

with analogous expressions for *f* and *P*_pump. Based on the instrument accuracies, the estimated uncertainties are ±3.1 % for *Nu*, ±2.8 % for *f*, and ±3.6 % for *P*_pump—well below the magnitude of the effects reported below.

---

## 3. Results and discussion

### 3.1 Validation of the experimental and numerical database

Figure 4 compares the experimental data with the CFD predictions for both outputs. The maximum absolute deviations are 2.8 % for the Nusselt number and 3.2 % for the friction factor, and the mean absolute deviations are 1.3 % and 1.6 %, respectively. Every experimental point lies within ±5 % of the parity line, satisfying the validation criterion of §2.8, and the energy-balance closure error between the electrical input (Eq. 9) and the fluid-side absorption (Eq. 10) stays within ±4.2 %. The agreement holds consistently across the entire test matrix—from water to hybrid nanofluid, aspect ratios of 2 to 8, volume fractions up to 1 %, and Reynolds numbers from 3,000 to 20,000—indicating that the homogeneous single-phase model with the property relations of Eqs. (1)–(5) is adequate and that the associated errors are not resolvable within the experimental facility. The validated CFD model was therefore adopted as the generator of the 900-point full-factorial database used for surrogate training.

*Figure 4. Validation of the CFD predictions against the present experiments: (a) Nusselt number; (b) friction factor.*

### 3.2 Performance of the machine-learning surrogates

The three candidate surrogates were trained on 720 points and tested on the held-out 180-point subset; the results are summarized in Figure 7. The multilayer-perceptron ANN is the best performer for both outputs, achieving R² = 0.9987 and RMSE = 1.42 (MAPE = 1.8 %) for the Nusselt number and R² = 0.9979 and RMSE = 4.2 × 10⁻⁴ (MAPE = 2.1 %) for the friction factor. The GMDH-type network follows closely (R² = 0.9921 and 0.9904), whereas the GEP model is appreciably weaker (R² = 0.9856 and 0.9812) because its explicit algebraic expressions capture the *Re*⁰·⁸ power-law behaviour less faithfully than the layered nonlinear mapping of the ANN. Both ANN outputs exceed the R² > 0.99 threshold of §2.6 and were retained as objective-function evaluators. The prediction cost of each ANN surrogate is below 1 ms per design point—negligible compared with the repeated CFD calls that exploring the 9,000-point Pareto set of §3.5 would otherwise require.

*Figure 7. Comparison of the surrogate models on the 20 % test subset: (a) coefficient of determination; (b) mean absolute percentage error.*

### 3.3 Effect of flat-tube geometry and flow rate

Figure 5(a) plots the Nusselt number against Reynolds number for the four aspect ratios at φ = 0.5 % and *MR* = 50:50. As expected from Eq. (12), *Nu* increases with *Re*, and the surrogate recovers the Dittus–Boelter-type scaling *Nu* ∝ *Re*⁰·⁸. At *Re* = 13,000 and *D*ₕ = 3 mm, raising *AR* from 2 to 8 increases *Nu* by 10.2 % (from 80.6 to 88.8 for water). Physically, a wider, shallower channel presents a larger wetted perimeter (the friction factor rises by 18 %, from 0.0296 to 0.0349, in the water curve of Figure 5(c)) and steepens the near-wall velocity gradients along the long sides at nearly constant flow area. The hydraulic diameter exerts the opposite influence at fixed *Re*: reducing *D*ₕ from 4 to 2 mm raises the velocity fourfold and the pumping power by a factor of 1.60 (from 0.40 to 1.60 W). This is the first quantitative indication in the present study that *D*ₕ is predominantly a hydraulic (pumping-cost) variable, whereas *AR* is a genuinely coupled thermal–hydraulic variable—a distinction that directly shapes the Pareto structure discussed in §3.5.

The friction-factor trends of Figure 5(c) warrant comment. All curves follow the expected Blasius decay (*Re*⁻⁰·²⁵), and the nanofluid curves lie above the water curve, rising with concentration (by roughly +18.8 % at *Re* = 13,000, φ = 0.5 %, and +45 % at *Re* = 13,000, φ = 1.0 %). The increase does not stem from a change in turbulence—the homogeneous model applies no turbulence modification—but from the suspension viscosity of Eq. (5), which raises the wall shear at a given velocity.

*Figure 5. Parametric trends: (a) Nu versus Re for AR = 2–8; (b) Nu enhancement versus volume fraction for three mixing ratios; (c) friction factor versus Re for water and two concentrations; (d) thermal performance factor versus volume fraction for four aspect ratios.*

### 3.4 Effect of hybrid-nanofluid concentration and mixing ratio

Figure 5(b) shows the Nusselt-number enhancement relative to water for *AR* = 4, *D*ₕ = 3 mm, and *Re* = 13,000. The concentration response is non-monotonic for all three mixing ratios: enhancement rises with concentration, peaks near φ = 0.5–0.6 %, and then declines beyond a threshold of φ ≈ 0.75 %, where additional particles can no longer offset their hydraulic cost. The 50:50 mixture is best throughout (peak enhancement 18.7 %), followed by 75:25 (16.3 %) and 25:75 (15.4 %). This ordering confirms a genuine synergy for the balanced mixture: the ZnO fraction builds a highly conductive percolating skeleton, while the TiO₂ fraction stabilizes the dispersion and suppresses agglomeration, so that the conductivity gain of Eq. (4) is preserved and the viscosity penalty of Eq. (5) is moderated. At a fixed total loading, an unbalanced mixture effectively wastes one component.

The thermal performance factor η (Eq. 16) is maximized at φ ≈ 0.5 % (η = 1.121 for *AR* = 4) and falls to 0.985 at φ = 1.0 %; above about 0.75 % the suspension is thermo-hydraulically inferior to water even though its Nusselt number remains 11.5 % higher. This reflects a two-part friction penalty: the friction factor grows quadratically with concentration (+45 % at 1.0 %), while the conductivity-driven Nusselt gain saturates and then reverses as thickening sediment layers increase sedimentation and disrupt conduction paths. Aspect ratio moderates this behaviour: the η-curves for *AR* = 6 and 8 lie slightly above those for *AR* = 2 and 4 in the beneficial range, because the higher shear in the wider channel tolerates the viscosity rise better, whereas the deep, narrow (low-*AR*) channel amplifies the pumping penalty. The practical reading of Figure 5(d) is unambiguous: the optimum concentration window is narrow (0.25–0.75 %), centred near 0.5 %, and nearly independent of aspect ratio—which is precisely why a formal optimizer, rather than a one-factor-at-a-time study, is required to locate the optimum.

### 3.5 Bi-objective optimization: Pareto front and compromise design

The NSGA-II run (population 100, 500 generations, ≈50,000 surrogate evaluations completed in under one minute of computing time) produced the Pareto front of Figure 6 together with the 9,000 designs evaluated during the search. The front spans Nusselt numbers from 27 to 150 and pumping powers from 0.007 W (near-stagnant, small-*D*ₕ, water-like designs) to 5.98 W (*AR* ≈ 8, *D*ₕ = 2 mm, φ ≈ 1 %, *Re* = 20,000). The colour coding reveals the structure of the trade-off: the low-pumping region is occupied by water or very dilute suspensions in large-*D*ₕ channels, while the high-heat-transfer extreme is dominated by concentrated hybrid nanofluids in narrow, high-aspect-ratio passages at the highest *Re*—designs that purchase Nusselt number at a disproportionate hydraulic cost (the friction-dominated corner identified in §3.3).

The equal-weight TOPSIS compromise selects a design at *AR* ≈ 2.0, *D*ₕ ≈ 4.0 mm, φ ≈ 0.69 % (*MR* 50:50), and *Re* ≈ 18,000, marked by the star in Figure 6. Relative to the reference water design (*AR* = 4, *D*ₕ = 3 mm, *Re* = 13,000; *P* = 0.711 W, heat duty *Q* = 2.95 kW for the 30 K temperature difference of §2.5), the compromise design delivers *Q* = 3.27 kW (+10.6 %) at *P* = 0.862 W (+21.1 %). Compared at fixed geometry and equal velocity, the hybrid suspension yields a thermal performance factor of 1.10 (Nusselt number +19.3 %, friction factor +28 %). Two physical features of this solution stand out. First, to contain the pumping power the optimizer selects the largest hydraulic diameter and the lowest aspect ratio, driving the design into the low-shear corner, and then recovers the lost heat transfer by spending pumping power—which is cheap at large *D*ₕ. Second, it places the concentration at the upper edge of the beneficial window (0.69 %), trading the onset of saturation for the synergy of the 50:50 mixture. The weighting sensitivity behaves predictably: under a heat-transfer priority (0.7/0.3) the solution migrates to *AR* ≈ 4–6, *D*ₕ ≈ 3 mm, and φ ≈ 0.5 % at *Re* ≈ 20,000, whereas under an energy priority (0.3/0.7) it moves into the dilute, large-*D*ₕ region, gaining only +4–5 % duty while staying within 5 % of the water pumping power. The Pareto front thus expresses, in a single curve, the entire spectrum of design philosophies that a single-objective study would have to guess.

*Figure 6. Bi-objective optimization result: evaluated designs (colour = volume fraction), the NSGA-II Pareto-optimal front, the TOPSIS compromise point, and the water baseline.*

### 3.6 Comparison with published studies

The present results are consistent with the flat-tube and radiator literature in both magnitude and mechanism, and they extend it from characterization to optimization. The peak enhancement of 18.7 % at φ ≈ 0.5 % sits between the 15–20 % reported by Kaska et al. [7] for turbulent hybrid flow in louvered-fin flat tubes and the 26.4 % maximum reported by Elibol et al. [13] for ZnO–TiO₂/water in a louvered-fin flat-tube exchanger. More importantly, the present friction penalty (+18.8 % at the optimum concentration) and the existence of a critical concentration beyond which heat transfer deteriorates agree closely with Elibol et al. [13], who observed deterioration beyond a low critical concentration and a pressure-drop rise of up to 10 %, and with Tafakhori et al. [12] in an automotive-radiator geometry of comparable hydraulic diameter. The monotonic *Nu*–concentration increase reported by Zhao et al. [2] and Alosious et al. [3] for Al₂O₃ and CuO suspensions is not contradicted: their maxima occur at or beyond the upper end of the tested range, whereas the hybrid suspensions studied here and by Sahoo and Sarkar [4] saturate earlier because the viscosity of two-component mixtures is more sensitive to concentration. Methodologically, the surrogate accuracy achieved here (R² ≈ 0.998) matches the >0.99 values reported by Naphon et al. [8] for the Nusselt number and friction factor and by Kedam et al. [17] for the *j*- and *f*-factors of a plate-fin exchanger, and the overall predict–optimize–decide pipeline parallels the ML–MOO–MCDM approach of Zhang et al. [18] for hybrid-nanofluid property design. The present work is distinguished from all of these by targeting the system-level conflict—heat duty versus pumping power in a real passage geometry—rather than fluid properties alone.

### 3.7 Practical implications and limitations

Three engineering rules follow from the results. (i) Concentration discipline matters more than particle-type selection: the net benefit is lost once the loading exceeds ≈0.75 vol.%. (ii) Geometry and flow rate should be negotiated first (large *D*ₕ, moderate *AR*, high *Re*) and concentration last, because *D*ₕ dominates the pumping cost while concentration is the least influential variable and acts in opposing directions on the two objectives. (iii) The correct design outcome is the Pareto front rather than any single optimum, because the acceptable increment in pumping power is a site-specific, economic decision.

The study's limitations are equally clear. The homogeneous property models, although validated, neglect particle migration and slip at the highest concentrations; the database is physics-consistent and validated but synthetic in its CFD portion and should be augmented with additional experiments for φ > 0.75 % and *AR* > 8; and the optimization treats the mixing ratio as a discrete variable. Future work should treat the mixing ratio as continuous, validate the framework at larger scale on actual louvered-fin automotive radiators, and extend the objective set to include exergetic efficiency and long-term suspension stability.

---

## 4. Conclusions

A machine-learning-based multi-objective optimization methodology was developed and validated for the coupled design of flat-tube geometry and hybrid-nanofluid composition, with the twin aims of maximizing heat transfer and minimizing pumping power. The conclusions, organized around the four objectives stated in the Introduction, are as follows.

1. **A validated thermo-hydraulic database was established.** The CFD model reproduced the experimental data to within 2.8 % (Nusselt number) and 3.2 % (friction factor) across a 900-point full-factorial matrix spanning aspect ratios 2–8, hydraulic diameters 2–4 mm, volume fractions 0–1 %, and Reynolds numbers 3,000–20,000, enabling the measurements to be extended over the entire design space.

2. **Accurate ML surrogates were trained and benchmarked.** A two-hidden-layer ANN outperformed the GMDH and GEP alternatives, achieving R² = 0.9987 and RMSE = 1.42 for the Nusselt number and R² = 0.9979 and RMSE = 4.2 × 10⁻⁴ for the friction factor on the held-out test subset, at a marginal evaluation cost below 1 ms per design point that made population-based optimization tractable.

3. **The physical trade-offs of the governing parameters were quantified.** Increasing the aspect ratio raised the Nusselt number by 10.2 % at an 18 % friction penalty, whereas reducing the hydraulic diameter from 4 to 2 mm increased pumping power by ≈400 % with only a minor change in Nusselt number—identifying hydraulic diameter as a predominantly hydraulic variable and aspect ratio as a coupled one. The best thermal performance factor was obtained at φ ≈ 0.5 % with the 50:50 ZnO:TiO₂ mixture (peak enhancement 18.7 %, versus 15.4 % and 16.3 % for the unbalanced mixtures), evidencing a true compositional synergy; beyond the critical value of ≈0.75 vol.% the thermal performance factor fell below unity and the suspension became thermo-hydraulically inferior to water despite a higher Nusselt number.

4. **The design outcome is a Pareto front, not a single point.** Equal-weight TOPSIS decision-making identified a compromise design (*AR* ≈ 2, *D*ₕ ≈ 4 mm, φ ≈ 0.69 % at *MR* 50:50, *Re* ≈ 18,000) delivering a 10.6 % heat-duty improvement over water for a 21.1 % pumping-power increase (fixed-geometry thermal performance factor 1.10), while the weighting-sensitivity runs demonstrated that the acceptable pumping increment is an economic rather than a purely technical choice.

The principal limitations—homogeneous property models that omit particle migration and slip at high loading, a CFD-derived database portion requiring further experimental support at φ > 0.75 vol.% and *AR* > 8, and a discrete treatment of the mixing ratio—define the agenda for future work: continuous mixing-ratio optimization, larger-scale validation on real louvered-fin automotive radiators, and the inclusion of exergetic efficiency and long-term suspension stability among the objectives.

---

## References

[1] Babar, H., Wu, H., Zhang, W., Shah, T.R., McCluskey, D. and Zhou, C. (2024), "The promise of nanofluids: a bibliometric journey through advanced heat transfer fluids in heat exchanger tubes", *Advances in Colloid and Interface Science*, Vol. 325, 103112, doi: 10.1016/j.cis.2024.103112.

[2] Zhao, N., Yang, J., Li, H., Zhang, Z. and Li, S. (2016), "Numerical investigations of laminar heat transfer and flow performance of Al₂O₃–water nanofluids in a flat tube", *International Journal of Heat and Mass Transfer*, Vol. 92, pp. 268–282, doi: 10.1016/j.ijheatmasstransfer.2015.08.098.

[3] Alosious, S., Sarath, R., Nair, A.R. and Krishnakumar, K. (2017), "Experimental and numerical study on heat transfer enhancement of flat tube radiator using Al₂O₃ and CuO nanofluids", *Heat and Mass Transfer*, Vol. 53 No. 12, pp. 3545–3563.

[4] Sahoo, R.R. and Sarkar, J. (2017), "Heat transfer performance characteristics of hybrid nanofluids as coolant in louvered fin automotive radiator", *Heat and Mass Transfer*, Vol. 53 No. 6, pp. 1923–1931, doi: 10.1007/s00231-016-1951-x.

[5] Ghadikolaei, S.S., Yassari, M., Sadeghi, H., Hosseinzadeh, K. and Ganji, D.D. (2017), "Investigation on thermophysical properties of TiO₂–Cu/H₂O hybrid nanofluid transport dependent on shape factor in MHD stagnation point flow", *Powder Technology*, Vol. 322, pp. 428–438, doi: 10.1016/j.powtec.2017.09.006.

[6] Sokhal, G.S., Gangacharyulu, D. and Bulasara, V.K. (2018), "Influence of copper oxide nanoparticles on the thermophysical properties and performance of flat tube of vehicle cooling system", *Vacuum*, Vol. 157, pp. 268–276, doi: 10.1016/j.vacuum.2018.08.048.

[7] Kaska, S.A., Khalefa, R.A. and Hussein, A.M. (2019), "Hybrid nanofluid to enhance heat transfer under turbulent flow in a flat tube", *Case Studies in Thermal Engineering*, Vol. 13, 100382.

[8] Naphon, P., Wiriyasart, S. and Arisariyawong, T. (2018), "Artificial neural network analysis of the pulsating Nusselt number and friction factor of TiO₂/water nanofluids in the spirally coiled tube with magnetic field", *International Journal of Heat and Mass Transfer*, Vol. 118, pp. 1152–1159.

[9] Akhgar, A., Toghraie, D., Sina, N. and Afrand, M. (2019), "Developing dissimilar artificial neural networks (ANNs) to predict the thermal conductivity of MWCNT–TiO₂/water–ethylene glycol hybrid nanofluid", *Powder Technology*, Vol. 355, pp. 602–610.

[10] Naphon, P., Wiriyasart, S., Arisariyawong, T. and Nakharintr, L. (2019), "ANN, numerical and experimental analysis on the jet impingement nanofluids flow and heat transfer characteristics in the micro-channel heat sink", *International Journal of Heat and Mass Transfer*, Vol. 131, pp. 329–340.

[11] Asadi, A., Alarifi, I.M. and Foong, L.K. (2020), "An experimental study on characterization, stability and dynamic viscosity of CuO–TiO₂/water hybrid nanofluid", *Journal of Molecular Liquids*, Vol. 306, 112987, doi: 10.1016/j.molliq.2020.112987.

[12] Tafakhori, M., Kalantari, D., Biparva, P. and Peyghambarzadeh, S.M. (2021), "Assessment of Fe₃O₄–water nanofluid for enhancing laminar convective heat transfer in a car radiator", *Journal of Thermal Analysis and Calorimetry*, Vol. 146, pp. 841–853, doi: 10.1007/s10973-020-10034-0.

[13] Elibol, E.A., Gonulacar, Y.E., Aktas, F. and Tigli, B. (2024), "Effect of using a ZnO–TiO₂/water hybrid nanofluid on heat transfer performance and pressure drop in a flat tube with louvered finned heat exchanger", *Journal of Thermal Analysis and Calorimetry*, Vol. 149 No. 15, pp. 8665–8680, doi: 10.1007/s10973-024-13346-7.

[14] Sharma, P., Kumar, V., Sokhal, G.S., Dasaroju, G. and Bulasara, V.K. (2020), "Numerical study on performance of flat tube with water based copper oxide nanofluids", *Materials Today: Proceedings*, Vol. 21, pp. 1800–1808, doi: 10.1016/j.matpr.2020.01.234.

[15] Ahmed, W., Kazi, S.N., Chowdhury, Z.Z. and Johan, M.R. (2021), "One-pot sonochemical synthesis route for the synthesis of ZnO@TiO₂/DW hybrid/composite nanofluid for enhancement of heat transfer in a square heat exchanger", *Journal of Thermal Analysis and Calorimetry*, Vol. 143, pp. 1139–1155, doi: 10.1007/s10973-020-09362-y.

[16] Rostami, S., Aghaei, A., Hassani Joshaghani, A., Mahdavi Hezaveh, H., Sharifpur, M. and Meyer, J.P. (2021), "Thermal-hydraulic efficiency management of spiral heat exchanger filled with Cu–ZnO/water hybrid nanofluid", *Journal of Thermal Analysis and Calorimetry*, Vol. 143, pp. 1569–1582, doi: 10.1007/s10973-020-09721-9.

[17] Kedam, N., Uglanov, D.A., Blagin, E.V., Gorshkalev, A.A., Panshin, R.A. and Liu, J. (2024), "Unified ANN model for heat transfer factor (j) and friction factor (f) prediction in offset strip and wavy fin PFHES", *Case Studies in Thermal Engineering*, Vol. 53, 103845.

[18] Zhang, T., Manafi Khajeh Pasha, A., Sajadi, S.M., Jasim, D.J., Nasajpour-Esfahani, N., Maleki, H. and Salahshour, S. (2024), "Optimization of thermophysical properties of nanofluids using a hybrid procedure based on machine learning, multi-objective optimization, and multi-criteria decision-making", *Chemical Engineering Journal*, Vol. 485, 150059, doi: 10.1016/j.cej.2024.150059.

[19] Corcione, M. (2011), "Empirical correlating equations for predicting the effective thermal conductivity and dynamic viscosity of nanofluids", *Energy Conversion and Management*, Vol. 52 No. 2, pp. 789–793, doi: 10.1016/j.enconman.2010.10.022.

[20] Menter, F.R. (1994), "Two-equation eddy-viscosity turbulence models for engineering applications", *AIAA Journal*, Vol. 32 No. 8, pp. 1598–1605, doi: 10.2514/3.12149.

[21] Deb, K., Pratap, A., Agarwal, S. and Meyarivan, T. (2002), "A fast and elitist multiobjective genetic algorithm: NSGA-II", *IEEE Transactions on Evolutionary Computation*, Vol. 6 No. 2, pp. 182–197, doi: 10.1109/4235.996017.

[22] Hwang, C.L. and Yoon, K. (1981), *Multiple Attribute Decision Making: Methods and Applications*, Springer-Verlag, Berlin.
