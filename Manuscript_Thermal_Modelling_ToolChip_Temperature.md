# Thermal Modelling of Tool–Chip Interfacial Temperature in Interrupted Orthogonal Machining in the Presence of Cutting Fluids

**Authors:** Gyanendra Singh Goindi¹, Anshu Dhar Jayal¹, Prabir Sarkar¹\*

¹Department of Mechanical Engineering, Indian Institute of Technology Ropar, Rupnagar 140001, Punjab, India

\*Corresponding author. E-mail: prabir@iitrpr.ac.in

---

## Abstract

Minimum quantity lubrication (MQL) machining has emerged as a practical and sustainable alternative to conventional flood cooling, but the mechanism by which a metal-working fluid (MWF) acts in the cutting zone is governed strongly by the prevailing temperature. The tool–chip interfacial temperature, in particular, dictates whether an applied lubricant continues to function in the liquid phase, evaporates, or undergoes thermal decomposition that releases tribo-active elements. Knowledge of this temperature is therefore central to interpreting and optimizing cutting-fluid performance, yet it is difficult to measure directly during MQL machining because the atomized jet and mist obscure the cutting zone and preclude conventional infrared or tool–work thermocouple techniques. This paper presents a two-dimensional finite difference (FD) model coupled with an inverse heat-transfer solution procedure for estimating transient temperatures in the shear zone and on the cutting-tool rake face during interrupted orthogonal machining (peripheral down milling) of a plain medium carbon steel under dry and MQL conditions. Unlike classical analytical treatments, the method makes no a priori assumption about either the tool–chip friction coefficient or the heat-partition ratios at the various heat-generation zones, since both are variable outcomes of the applied MWF's effectiveness and can be predicted analytically only under steady-state continuous cutting. Temperatures recorded by a fine-wire K-type thermocouple embedded beneath the workpiece are used as input data, and a simple genetic algorithm minimizes the squared error between measured and predicted temperature histories to recover the unknown heat flux. The FD estimates were validated against the analytical model of Loewen and Shaw (1954) for dry cutting; rake-face temperatures and shear-zone heat-partition fractions agreed reasonably, while FD shear-zone temperatures were consistently higher because the FD model additionally captures flank–workpiece contact heating. Estimated temperatures were compared with the thermal decomposition temperatures of six MQL fluids, including fluorine-containing imidazolium ionic liquids, an oil-miscible phosphonium ionic liquid, and polyethylene glycol. The results confirm that at low speeds and light loads, where temperatures stay below decomposition, lubricant viscosity governs friction reduction, whereas at higher speeds and loads the fluids decompose and chemical action (notably fluorine liberation from BMIMPF6) dominates. Strong correlations between estimated rake-face temperatures and cutting forces were observed across most conditions, demonstrating that thermal modelling provides direct, physically meaningful insight into cutting-fluid action mechanisms.

**Keywords:** Interrupted orthogonal machining; Tool–chip interface temperature; Finite difference method; Inverse heat transfer; Minimum quantity lubrication; Ionic liquids

---

## 1. Introduction

Machining remains one of the most important and widely used manufacturing processes for producing engineering components with the required dimensional accuracy, surface finish, and surface integrity. Because the process directly influences the surface and sub-surface characteristics of a part, it has a decisive effect on the service life and reliability of critical components used in the automotive, aerospace, biomedical, and general engineering sectors. Machining is fundamentally a process of controlled material removal accomplished by severe, localized plastic deformation of the workpiece material ahead of a wedge-shaped cutting tool. According to widely accepted estimates, almost all of the mechanical energy supplied to accomplish this deformation and the subsequent sliding of the chip over the tool is ultimately converted into heat. The heat so generated raises the temperature of the chip, the workpiece, and, most critically, the cutting tool, and it is this thermal loading that limits attainable cutting speeds, accelerates tool wear, and constrains productivity.

To manage the heat generated in cutting, conventional practice relies on the copious application of flood cutting fluids, typically water-based emulsions or neat cutting oils delivered at flow rates of the order of tens of litres per minute. These fluids cool the tool and workpiece, lubricate the tool–chip and tool–workpiece interfaces, and flush chips from the cutting zone. However, the economic and ecological burdens associated with cutting fluids are large and growing. The fluids are susceptible to microbial contamination, require dedicated filtration and recirculation systems, occupy valuable shop-floor space, and must eventually be treated and disposed of at significant cost. Skin contact and inhalation of mist expose machine operators to well-documented health hazards. Together, the procurement, maintenance, and disposal of cutting fluids can account for a substantial fraction of the total manufacturing cost of a machined part, in some estimates rivalling or exceeding the cost of the cutting tools themselves.

These concerns have driven sustained research into dry machining and near-dry or minimum quantity lubrication (MQL) machining. In MQL, a very small volume of lubricant, typically in the range of 10–100 ml/h, is atomized in a jet of compressed air and directed at the cutting zone, where it is largely consumed within the process itself so that there is essentially no fluid to collect, recycle, or dispose of. Because MQL and dry machining eliminate the bulk convective cooling provided by flood coolant, heat accumulates in the machining zone to a greater extent, and it becomes essential to understand how the resulting temperatures affect the tool, the workpiece, and the lubricant. Modelling the tribological and thermal conditions of the cutting process is therefore a prerequisite for the rational selection and optimization of MQL fluids.

Among the various thermal criteria that influence cutting-fluid action, the tool–chip interfacial temperature distribution is arguably the most important. This temperature determines whether an applied fluid can perform its intended lubricating function without undergoing an unwanted change of phase or thermal degradation. Depending on the interface temperature, a lubricant may remain a liquid, evaporate to a vapour, or decompose chemically; each of these states implies a different mode of action. Thermal degradation beyond a critical temperature can either destroy the lubricating capability of a fluid or, conversely, activate it by liberating reactive species that form low-shear-strength films on the freshly generated chip and workpiece surfaces. The action mechanism of a given fluid thus varies with both the fluid chemistry and the prevailing thermal conditions, which makes accurate knowledge of the machining-zone temperatures indispensable to interpreting experimental cutting-force and surface-finish data.

The present work is motivated by a broader program of research into the use of ionic liquids as green lubricant additives in MQL machining. Ionic liquids are salts that are molten at or near room temperature owing to the large, asymmetric organic cations that lower their lattice energy; they exhibit negligible volatility, high thermal stability over a wide temperature range, and, crucially, physical and chemical properties that can be tailored by the choice of cation–anion pair. Prior experimental studies by the present authors and others have shown that small additions of fluorine-containing imidazolium ionic liquids to a vegetable base oil can markedly reduce cutting forces at elevated cutting speeds, where the interface temperature rises above the decomposition temperature of the ionic liquid and liberated fluorine binds to the fresh chip surface to reduce tool–chip adhesion. Oil-miscible phosphonium ionic liquids and polyethylene glycol, by contrast, tend to perform best at lower speeds where the interface temperature remains below their decomposition temperatures and the lubricating action is dominated by fluid viscosity. Distinguishing between these physically and chemically dominated regimes for any given fluid requires a reliable estimate of the temperature at the tool–chip interface under the specific cutting conditions employed.

Direct measurement of tool–chip interface temperature during MQL machining is, however, exceptionally difficult. Infrared thermography and tool–work thermocouple techniques, which are serviceable in dry cutting, are frustrated by the atomized lubricant jet and mist that envelop the cutting zone and obscure the tool from view. This practical obstacle motivates an inverse approach, in which readily accessible temperature measurements at a location remote from the cutting edge are combined with a validated heat-conduction model to reconstruct the inaccessible interface temperature.

This paper presents such an approach: a two-dimensional finite difference model of transient heat conduction in the workpiece, coupled with a genetic-algorithm-based inverse heat-transfer solution procedure, applied to interrupted orthogonal machining (peripheral down milling) of a plain medium carbon steel under dry and MQL conditions. In contrast to analytical and finite element treatments, the method deliberately avoids assuming values for the tool–chip friction coefficient or the heat-partition ratios, treating the unknown heat flux entering the workpiece as the quantity to be determined by matching measured and predicted temperature histories. The recovered heat flux is then used, together with an estimated shear-plane angle, to obtain average temperatures in the shear zone and on the tool rake face. The estimated temperatures are compared with the analytical predictions of Loewen and Shaw for validation in dry cutting and with the measured thermal decomposition temperatures of a set of candidate MQL fluids in order to illuminate the mechanisms by which different fluids influence the tribology of the process. Comparison with corresponding cutting-force measurements completes the picture.

The remainder of the paper is organized as follows. Section 2 reviews heat generation in machining and the principal analytical and numerical modelling approaches. Section 3 develops the finite difference formulation and the inverse solution procedure. Section 4 describes the experimental setup, materials, and the plan of experiments. Section 5 presents and discusses the validation results, the estimated temperatures under various MWF conditions, and the correlations with cutting forces and surface roughness. Section 6 summarizes the principal conclusions.

---

## 2. Heat generation and its modelling in machining

### 2.1 Heat-generation zones

In metal cutting, the great majority of the mechanical work expended is converted into heat, and this conversion is concentrated in three well-recognized zones. The **primary heat zone** coincides with the idealized shear plane, where incoming workpiece material is plastically deformed within a narrow shear band during chip formation; the plastic work of shear is almost entirely dissipated as heat here. The **secondary heat zone** lies along the tool rake face immediately behind the cutting edge, where the newly formed chip slides over the rake surface under high normal pressure; the frictional and further plastic work in this zone is likewise converted mostly to heat. The **tertiary heat zone** arises at the tool flank, where the freshly machined workpiece surface rubs against the flank face of the tool. The relative importance of these zones depends on the cutting conditions, tool geometry, tool wear state, and the presence or absence of a lubricant.

Accurate estimation of the heat generated in cutting, and of how it partitions between the chip, the tool, and the workpiece, is an inherently difficult task. The process combines very high strains and strain rates with high temperatures, and these conditions substantially alter the local flow stress of the workpiece and the properties of the tool. The geometry of realistic operations, the temperature dependence of thermal and mechanical properties, and the transient nature of interrupted cutting all add to the complexity. A large body of work has nevertheless been devoted to modelling machining heat, and the models can broadly be classified as analytical or numerical.

### 2.2 Analytical models

The classical analytical treatments of cutting temperatures trace back to the moving-heat-source and heat-partition concepts of Blok and the friction-slider analysis of Jaeger, and to their application to machining by Trigger and Chao, Hahn, Loewen and Shaw, Rapier, and Weiner. In these approaches the total cutting energy is divided between primary shear-zone heat generation and secondary tool–chip interface heat generation, with the tertiary flank zone usually neglected for simplicity. A fraction of the shear-zone heat flows into the workpiece while the remainder is carried away in the chip; as the heated chip subsequently slides over the rake face, additional frictional heat is generated, part of which conducts into the tool and part of which remains in the chip. Refinements such as the volumetric (rather than planar) rake-face heat source proposed by Boothroyd have improved the fidelity of these models.

The analytical models are elegant and computationally inexpensive, but they rest on two assumptions that are problematic for interrupted MQL cutting. First, they assume a uniform heat source and steady-state conditions, which are appropriate only for continuous cutting after long times and not for the intrinsically transient, intermittent engagement of a milling insert. Second, and more importantly for the present purpose, they require the tool–chip friction coefficient and the heat-partition ratios to be specified as inputs. Under MQL these quantities are precisely what the applied fluid alters, in a manner that varies with fluid chemistry, cutting speed, and load; treating them as known inputs would defeat the purpose of the analysis.

### 2.3 Numerical models

Numerical models fall into two families: the finite element method (FEM) and the finite difference (FD) method. In both, the machining domain is discretized into small elements and the governing energy-balance equations are solved element by element for the temperature field. FEM was first applied to machining by Tay and co-workers and subsequently by many others; FD models for heat conduction in cutting have been used by Smith and Armarego, Lin, Chen, Obikawa, Lazoglu and Altintas, and others. Numerical models can accommodate temperature-dependent material properties and complex geometries far more readily than analytical models. However, FEM in particular can demand very large computational resources, with detailed simulations requiring hours or days of run time on powerful hardware, and, like analytical models, numerical models generally require the user to supply several sensitive input parameters, including friction and heat-partition data.

The approach adopted in this work uses a deliberately simple and computationally light explicit FD scheme for the forward heat-conduction problem, so that it can be evaluated many thousands of times inside an optimization loop, and pairs it with an inverse solution that recovers the unknown heat input from measured temperatures rather than requiring it as an assumption. This combination is well suited to MQL machining precisely because it does not presuppose the friction coefficient or heat-partition ratios.

---

## 3. Finite difference model and inverse solution

### 3.1 Modelling strategy

The objective of the model is to estimate the heat partition, the heat flux in the shear zone, and the tool–chip interfacial temperature, using a finite difference method for transient heat conduction in combination with an inverse heat-transfer solution. The essential idea is that the heat generated in the various zones, and the fractions of that heat entering the workpiece and the tool, are not prescribed from assumed or analytically estimated values. Instead they are left as unknowns and are estimated as part of the solution by requiring the model to reproduce the temperature history actually measured by a thermocouple embedded in the workpiece. Because the friction coefficient at the tool–chip interface is itself a variable outcome of the applied MWF's effectiveness, and because heat-partition ratios can be estimated analytically only under steady-state continuous cutting, this inverse strategy is the natural way to gain insight into the thermal phenomena that both influence, and result from, the action of the lubricant.

The physical configuration modelled is peripheral down milling of a slab-like workpiece, in which the moving cutting edge delivers a heat influx to the workpiece near the tool–workpiece contact zone. In the model this appears as a moving heat source that traverses the top surface of the workpiece at a fixed rate along the feed (X) direction. The workpiece cross-section is discretized into a two-dimensional grid of nodes; heat is conducted between neighbouring nodes, convective heat loss occurs from the exposed top surface, and the remaining boundaries are held at ambient temperature.

**[Figure 1 near here.]**

### 3.2 Governing finite difference equations

For an interior node located within the workpiece and having no internal heat generation, an energy balance over the control volume associated with the node yields the explicit finite difference form of the transient heat-conduction equation. Following the standard treatment (Incropera and DeWitt), the temperature of node (i, j) at time step p is advanced to time step p + 1 according to

$$
\frac{1}{\alpha}\,\frac{T_{i,j}^{\,p+1}-T_{i,j}^{\,p}}{\Delta t}
=\frac{T_{i+1,j}^{\,p}+T_{i-1,j}^{\,p}-2T_{i,j}^{\,p}}{(\Delta x)^2}
+\frac{T_{i,j+1}^{\,p}+T_{i,j-1}^{\,p}-2T_{i,j}^{\,p}}{(\Delta y)^2}
\tag{1}
$$

where α = K/(ρc_p) is the thermal diffusivity of the workpiece material (m²/s), K is the thermal conductivity (W/m·K), ρ is the density (kg/m³), c_p is the specific heat capacity (J/kg·K), Δt is the time step (s), Δx and Δy are the node spacings in the X and Y directions, T_{i,j}^{p} is the temperature of node (i, j) at time p, and T_{i,j}^{p+1} is its temperature at time p + Δt.

**[Figure 2 near here.]**

Setting Δx = Δy and solving Equation (1) for the future nodal temperature gives the compact update rule

$$
T_{i,j}^{\,p+1}= Fo\left(T_{i+1,j}^{\,p}+T_{i-1,j}^{\,p}+T_{i,j+1}^{\,p}+T_{i,j-1}^{\,p}\right)+(1-4\,Fo)\,T_{i,j}^{\,p}
\tag{2}
$$

in which Fo is the dimensionless Fourier number,

$$
Fo=\frac{\alpha\,\Delta t}{(\Delta x)^2}.
\tag{3}
$$

The explicit scheme is only conditionally stable. Stability of the interior-node update requires the coefficient of the current nodal temperature to remain non-negative, i.e. (1 − 4Fo) ≥ 0, which restricts the time step to

$$
\Delta t \le \frac{(\Delta x)^2}{4\alpha}.
\tag{4}
$$

**[Figure 3 near here.]**

Nodes on the left, right, and bottom boundaries of the modelled domain are sufficiently far from the moving heat source that they remain at the ambient temperature throughout, so that

$$
T_{i,j}^{\,p+1}=T_{i,j}^{\,p}=T_\infty \quad\text{(ambient temperature).}
$$

Nodes on the exposed top face of the workpiece lose heat by convection to the surroundings. Applying an energy balance that includes the convective term gives the update rule for a top-surface (non-contact) node,

$$
T_{i,j}^{\,p+1}=Fo\left(T_{i+1,j}^{\,p}+T_{i-1,j}^{\,p}+2T_{i,j-1}^{\,p}\right)+\left(1-2\,Bi\,Fo-4\,Fo\right)T_{i,j}^{\,p}+2\,Bi\,Fo\,T_\infty
\tag{5}
$$

where Bi is the dimensionless Biot number,

$$
Bi=\frac{h\,\Delta x}{K},
\tag{6}
$$

h is the convective heat-transfer coefficient at the top face (W/m²·K), and T_∞ is the ambient temperature. Stability of the convective-surface node requires (1 − 2Bi·Fo − 4Fo) ≥ 0, i.e.

$$
\Delta t \le \frac{\rho\,c_p\,(\Delta x)^2}{4K+2h\,\Delta x}.
\tag{7}
$$

Finally, for the node on the top surface that is instantaneously in contact with the cutting tool, and onto which the moving heat source imposes a heat flux q̇ (W/m²), the update rule becomes

$$
T_{i,j}^{\,p+1}=Fo\left(T_{i+1,j}^{\,p}+T_{i-1,j}^{\,p}+2T_{i,j-1}^{\,p}\right)+(1-4\,Fo)\,T_{i,j}^{\,p}+\frac{2\,\dot q\,\Delta t}{\rho\,c_p\,\Delta x}.
\tag{8}
$$

The additional term in Equation (8) represents the heat delivered to the surface node by the moving source over the time step. The magnitude of q̇, the heat flux entering the workpiece through the tool–workpiece contact zone, is left as the principal unknown to be recovered by the inverse procedure.

### 3.3 Material properties

The thermophysical properties required by the model were taken from materials-handbook data for plain medium carbon steel. The thermal conductivity of the workpiece material was taken as 54 W/m·K, with a rate of change with temperature of 0.003 W/m·K²; the specific heat capacity was taken as 425 J/kg·K, with a rate of change of 0.733 J/kg·K²; and the density was taken as 7850 kg/m³. Incorporating the temperature dependence of conductivity and specific heat allows the model to reflect, at least approximately, the softening of thermal response at the elevated temperatures reached near the cutting edge.

### 3.4 Inverse heat-transfer solution using a genetic algorithm

The forward FD model, given a value of the heat flux q̇ (and the associated heat-generation parameters), predicts the complete transient temperature field in the workpiece, and in particular the temperature history at the node corresponding to the physical location of the embedded thermocouple. The inverse problem is to find the value(s) of the unknown heat input that make the predicted temperature history at that location match the measured history as closely as possible.

This is posed as a minimization problem: the objective function is the sum of squared errors between the measured temperature history and the predicted temperature history at the thermocouple location, and the design variables are the unknown heat-generation and heat-input terms. A simple genetic algorithm (GA) is used to perform the minimization. The GA maintains a population of candidate solutions (values of the unknown flux), evaluates the objective function for each candidate by calling the forward FD subroutine, and evolves the population over successive generations through selection, crossover, and mutation so as to drive the squared error toward its minimum. Because the forward subroutine must be invoked many thousands of times during the optimization, the explicit FD scheme was chosen for its speed and simplicity; each forward solution is inexpensive, so the overall inverse solution remains tractable on ordinary computing hardware. The approach follows the methodology previously described by Jayal for inverse estimation of machining heat.

Once the optimal heat flux that minimizes the measurement–prediction error has been identified, it is substituted back into the forward FD model to compute the full temperature field under those conditions. The heat flux recovered for the shear zone, together with an estimated shear-plane angle, is then supplied to the analytical framework of Loewen and Shaw to obtain the average temperature at the tool–chip contact zone on the rake face. In this way the inverse FD procedure yields three quantities of primary interest for each experimental condition: the average shear-zone temperature, the shear-zone heat-partition fraction (the fraction of shear-zone heat carried away by the chip), and the average tool–chip interface (rake-face) temperature.

---

## 4. Experimental setup and plan

### 4.1 Machining arrangement and temperature measurement

Machining experiments were carried out as peripheral down-milling (interrupted orthogonal) operations on the side face of a slab-like workpiece, using a CNC vertical machining centre. Interrupted orthogonal milling was chosen for two reasons. First, orthogonal cutting geometry is comparatively easy to model and is therefore well suited to fundamental studies. Second, and importantly for MQL, the interrupted nature of milling is favourable to lubricant action: during each revolution the single cutting insert engages the workpiece for only a short arc and then rotates idly through air, during which it passes in front of the MQL nozzle and receives a fresh coat of lubricant before the next cut. Interrupted cutting is thus an effective condition in which to assess the efficacy of a candidate fluid.

The workpiece was mounted horizontally and the cutter axis kept vertical, with the feed direction corresponding to down milling. Only one pocket of the milling cutter was fitted with an insert, the other pockets being intentionally left blank, so that a single, well-defined cutting edge engaged the work once per revolution. A fresh cutting edge was used for each experiment, and each experiment was replicated three times.

For temperature measurement, a fine-wire K-type (chromel–alumel) thermocouple of 0.25 mm diameter was embedded in the fixture immediately below the workpiece, at a known location relative to the machined surface. This indirect, sub-surface measurement was adopted deliberately, because the alternative techniques normally used to sense cutting-zone temperature — infrared thermal imaging and the tool–work thermocouple — are impractical during MQL machining, where the atomized jet and mist cover the cutting area and obscure the tool. The thermocouple output was acquired through an NI cDAQ-9188 thermal module and a LabVIEW-based data-acquisition system. The recorded sub-surface temperature history is precisely the input required by the inverse FD procedure. Machining forces were recorded simultaneously with a piezoelectric dynamometer and charge amplifier; the resultant of the force components in the feed and normal (X and Y) directions was used as the machining-force value, the axial (Z) component being negligible for the orthogonal arrangement.

**[Table 1 near here.]**

### 4.2 Workpiece material

The workpiece was a plain medium carbon steel, equivalent to AISI 1055, of the type used in many general-purpose engineering applications. The material was annealed before machining to an average hardness of about 190 BHN. Its measured chemical composition is summarized in Table 1.

### 4.3 Lubricants

Six MQL fluid formulations were investigated, spanning three lubricant systems: a vegetable base oil with fluorine-containing hydrophilic (oil-immiscible) ionic liquids; the same vegetable oil with an oil-miscible hydrophobic phosphonium ionic liquid; and polyethylene glycol (PEG) alone and with a hydrophilic ionic liquid dissolved in it. Canola oil served as the vegetable base oil. The fluorine-containing ionic liquid designated IL1 was 1-methyl-3-butyl-imidazolium hexafluorophosphate (BMIMPF6), added to the oil at 3 wt %; a second, oil-miscible phosphonium ionic liquid, tributyl(nonyl)phosphonium bis(2-ethylhexyl) phosphate (designated IL308), was added at 1 wt % and 0.5 wt %. PEG of average molecular weight 400 was used neat and with 3 wt % BMIMPF6 (PEG + IL1). The viscosities of the preparations were measured with a rotational microviscometer, densities with a portable density meter, and thermal decomposition temperatures by thermogravimetric analysis (TGA) in an inert nitrogen atmosphere, the decomposition temperature being defined as the temperature at 5 % weight loss.

### 4.4 Cutting conditions and plan of experiments

To span a useful range of process intensities, two sets of feed and radial depth of cut were used, corresponding to light and relatively heavy machining, and each was run at three cutting speeds. Light machining used a feed of 0.1 mm/tooth and a depth of cut of 0.3 mm; heavy machining used a feed of 0.3 mm/tooth and a depth of cut of 0.8 mm. Cutting speeds of 150, 200, and 250 m/min were investigated in each case; speeds beyond 250 m/min were not feasible with the uncoated carbide insert, and the machine-tool and fixture rigidity limited the depth of cut to 0.8 mm. The fixed and variable parameters of the experimental plan are collected in Table 2. The complete matrix combined the two machining intensities and three cutting speeds with dry cutting and the several MQL conditions, with three replicates each.

**[Table 2 near here.]**

---

## 5. Results and discussion

The inverse FD procedure was applied to the measured sub-surface temperature histories to estimate, for each experimental condition, the average shear-zone temperature, the shear-zone heat-partition fraction, and the average tool–chip interface temperature on the rake face. These estimates were first validated against the analytical model of Loewen and Shaw for dry cutting, and were then used, together with the thermal decomposition data of the fluids and the measured cutting forces, to interpret the mechanisms of cutting-fluid action under MQL.

### 5.1 Validation against the analytical model (dry cutting)

#### 5.1.1 Shear-zone temperatures

Figure 4 compares the average shear-zone temperatures estimated by the FD model with those calculated by the analytical Loewen–Shaw method for light and heavy dry cutting at the three cutting speeds. Two features stand out. First, the two methods track one another qualitatively: shear-zone temperature rises with cutting speed in light cutting and remains high across the speed range in heavy cutting. Second, and consistently, the FD estimates lie substantially above the analytical values.

**[Figure 4 near here.]**

This systematic offset has a physical explanation. The FD model is driven by the temperature actually measured beneath the workpiece during machining, and that measured sub-surface temperature reflects the combined heating of the workpiece by two sources: the primary shear zone and the tertiary tool-flank–workpiece contact zone. The analytical model, by construction, neglects the flank–workpiece heat generation. Because the FD model attributes all of the measured sub-surface heating to the workpiece heat input it solves for, it effectively lumps the shear-zone and flank-contact contributions together, which raises its shear-zone temperature estimate relative to the flank-free analytical value. The discrepancy is therefore not an error so much as a reflection of a real heat source that the analytical model omits, and it is largest where flank rubbing is proportionally more significant.

#### 5.1.2 Tool–chip interface (rake-face) temperatures

Figure 5 presents the corresponding comparison for the average tool rake-face temperature in the tool–chip contact zone, again for light and heavy dry cutting at the three speeds. Here the agreement between the FD estimates and the analytical predictions is considerably better than for the shear zone, and the two methods are in reasonable accord. The match is closer for heavy cutting than for light cutting, which is consistent with the analytical model's steady-state assumptions being better approximated when the cut is heavier and the thermal field more fully developed. The reasonable agreement in rake-face temperature is significant, because it is this temperature that governs lubricant phase behaviour and decomposition, and its reliable estimation is the central objective of the model.

**[Figure 5 near here.]**

#### 5.1.3 Heat partition in the shear zone

Part of the heat generated in the shear zone is convected away in the chip and the remainder conducts into the workpiece. Figure 6 compares the shear-zone heat-partition fraction (the fraction of shear-zone heat carried by the chip) estimated by the FD model with the analytical values for light and heavy dry cutting. The FD and analytical partition fractions are in approximate agreement, again with better matching under heavy machining. The heat-partition fraction generally lies in the range of roughly 0.4–0.6 across the conditions examined, indicating that a little over half of the shear-zone heat leaves with the chip. The reasonable reproduction of both rake-face temperature and heat partition, using only measured sub-surface temperatures and no assumed friction or partition data, provides confidence that the inverse FD approach captures the essential thermal physics of the process.

**[Figure 6 near here.]**

### 5.2 Thermal decomposition temperatures of the fluids

To connect the estimated temperatures to lubricant behaviour, the thermal decomposition temperatures and viscosities of the six MQL fluids were determined; these are summarized in Table 3. Two groupings are apparent. The PEG-based lubricants have relatively low decomposition temperatures, in the range of about 270–280 °C, whereas the vegetable-oil-based lubricants decompose at higher temperatures, in the range of about 330–380 °C. In terms of viscosity, neat PEG and the oil + IL308(1 %) preparation are the most viscous of the set, while the remaining fluids cluster in the range of about 60–70 mPa·s at 25 °C. These two properties — decomposition temperature and viscosity — are the levers through which a fluid's performance is expected to depend on the machining-zone temperature: below decomposition, the more viscous fluids should reduce friction more effectively (a physically dominated regime), whereas above decomposition, the chemistry of the decomposition products should govern behaviour (a chemically dominated regime).

**[Table 3 near here.]**

### 5.3 Estimated temperatures and mechanisms under MQL — light machining

Figure 7 shows the average shear-zone and rake-face temperatures estimated by the FD model for machining under the various MWF conditions in light cutting, as functions of cutting speed. At the lowest cutting speed in light machining, the estimated shear-zone temperatures — and hence, by association, the temperatures in the workpiece–tool-flank contact region — lie well below the decomposition temperatures of all the lubricants. In this regime the fluids remain intact and their lubricating action is governed principally by viscosity. Consistently, the more viscous fluids PEG and oil + IL308(1 %) gave the lowest machining forces at low speed in light cutting, because a more viscous film is better able to separate the sliding surfaces and reduce friction at the tool flank and rake.

**[Figure 7 near here.]**

As cutting speed increases in light machining, the estimated temperatures rise and begin to exceed the decomposition thresholds of the fluids. The behaviour then changes character. The rake-face temperatures for machining with neat oil, oil + IL308(1 %), and oil + IL308(0.5 %) remain below the decomposition temperatures of those preparations at low speed, so their forces are correspondingly low; but as speed increases and decomposition sets in, the phosphonium-ionic-liquid preparations lose their advantage, in contrast to the fluorine-containing IL1. At the highest speed, IL1 decomposes and liberates fluorine, which readily bonds with the chemically reactive freshly cut surface and reduces the adhesion of the chip to the tool, so that machining forces fall most sharply for IL1. This is precisely the chemically dominated regime, and its onset is signalled by the estimated rake-face temperature crossing the fluid's decomposition temperature. The temperature model therefore does more than report a number: it predicts which mechanism — viscous or chemical — should be operative for a given fluid at a given condition, and the force data corroborate that prediction.

### 5.4 Estimated temperatures and mechanisms under MQL — heavy machining

Under heavy machining the picture shifts because the higher feed and depth of cut raise the temperatures throughout the speed range. The estimated rake-face temperatures in heavy cutting lie well above the decomposition temperatures of the fluids at all three speeds. Consequently the chemically dominated regime is accessible even at the lowest speed. At low speed in heavy cutting, the lowest forces and temperatures were observed for IL1 and PEG + IL1: because the interface temperature already exceeds the decomposition temperature, IL1 decomposes and liberates fluorine, which bonds to the fresh iron surface, reduces tool–workpiece adhesion, and lowers cutting forces. At intermediate speed, the oil + IL308(1 %) preparation gave the best results, consistent with its effectiveness up to medium speeds. At the highest speed, however, the effect of the ionic liquids diminished and neat vegetable oil (followed by IL1 and IL308(0.5 %)) gave the lowest forces and temperatures. The estimated shear-zone temperatures in heavy cutting behaved analogously, being uniformly high and lying above the fluids' decomposition temperatures across the speed range. The consistent inference is that, for heavy cutting, the thermal conditions push essentially all of the fluids into the decomposition regime, so that differences in performance are governed by the nature of the decomposition products rather than by viscosity.

### 5.5 Correlations between temperatures, forces, and surface roughness

To quantify the interdependence of the thermal and mechanical outputs, Pearson correlation coefficients were computed among the mean machining forces, the workpiece surface roughness (Ra), the estimated shear-zone temperature, and the estimated rake-face temperature, separately for light and heavy machining at each cutting speed. Representative results are collected in Table 4, in which coefficients exceeding the significance threshold (|r| > 0.669 at p = 0.1 for the light-machining data set) are treated as strong.

**[Table 4 near here.]**

In light machining at low cutting speed, strong correlations were found among all four quantities — forces, roughness, shear-zone temperature, and rake-face temperature — indicating that in this benign, physically dominated regime the mechanical and thermal responses move together and are jointly governed by the lubricant's viscous action. As speed increased to the medium value, the web of correlations thinned: significant correlation persisted between surface roughness and shear-zone temperature, and between rake-face temperature and cutting forces, but the fuller inter-linkage was lost. At the highest speed in light machining, the only strong correlation that remained was between rake-face temperature and cutting forces. This progressive simplification is consistent with the transition from a viscosity-governed to a chemistry-governed regime as temperature rises: at high speed, the rake-face temperature (and the associated decomposition chemistry) becomes the dominant determinant of force, while surface roughness decouples from the thermal field.

In heavy machining, strong correlations were observed between machining forces and shear-zone temperature, and between machining forces and rake-face temperature, at low and medium speeds; at the highest speed, the only visible correlation was between machining forces and rake-face temperature. Notably, workpiece surface roughness showed no significant correlation with either forces or temperatures under heavy machining. The persistence, across almost all conditions, of a strong force–rake-face-temperature correlation is the single most robust finding of the correlation analysis, and it underscores the central role of the tool–chip interface temperature — the very quantity the inverse FD model is designed to estimate — in governing the tribological outcome of the process.

### 5.6 Discussion: mechanism of cutting-fluid action

Taken together, the results support a coherent, temperature-centred picture of MQL fluid action. The controlling variable is the temperature at the tool–chip interface (and, to a lesser degree, in the shear and flank-contact zones). When this temperature remains below a fluid's thermal decomposition temperature, the fluid persists as a liquid and its physical properties, chiefly viscosity, govern its ability to reduce friction; more viscous fluids such as PEG and oil + IL308(1 %) then perform best, and improvements in surface finish track lubricant viscosity. When the temperature exceeds the decomposition temperature, the fluid breaks down and the identity of its decomposition products determines behaviour. For the fluorine-bearing imidazolium ionic liquid IL1, decomposition liberates fluorine that reacts with the freshly generated, highly reactive chip surface to form low-shear-strength films that reduce tool–chip adhesion, yielding the sharpest reductions in cutting force at high speed and heavy load. For PEG, by contrast, decomposition simply destroys the lubricating film without releasing an effective tribo-active species, so its advantage is lost at high speed.

The value of the inverse FD model is that it makes this mechanistic distinction operational. By estimating the interface temperature for each condition and comparing it against the measured decomposition temperature of each fluid, one can predict a priori whether a given fluid will act physically or chemically under a given set of cutting parameters, and the accompanying force and roughness data confirm those predictions. This is achieved without assuming the friction coefficient or heat-partition ratios — which is essential, because those quantities are themselves altered by the very fluid action under study — and with a computational scheme light enough to be embedded in a genetic-algorithm optimization loop. The method thus provides a practical route to the rational, temperature-informed design and selection of MQL fluids, including the tailoring of ionic-liquid chemistries whose decomposition temperatures are matched to the thermal conditions of a target application.

### 5.7 Limitations and future work

Several simplifications temper the interpretation of the results. The heat-conduction model is two-dimensional and treats the workpiece as the primary conduction domain, so three-dimensional effects and heat flow into the tool and chip are represented only implicitly through the recovered surface flux and the coupling to the Loewen–Shaw framework for the rake-face temperature. The material properties, though made temperature-dependent, are handbook values rather than measurements on the specific heat lot, and the convective boundary condition at the top surface uses a single effective heat-transfer coefficient that cannot fully capture the spatially and temporally varying cooling produced by an atomized MQL jet. The inverse solution recovers an effective heat flux that best explains the sub-surface temperature history; distinguishing rigorously between the shear-zone and flank-contact contributions to that flux would require additional measurements or a more elaborate multi-source model. Future work could extend the model to three dimensions, incorporate explicit tool and chip domains with contact conductance, measure the effective convective coefficient of the MQL spray, and instrument the workpiece with multiple thermocouples to better resolve the individual heat sources. Broadening the fluid set and the range of tool–workpiece pairs, and studying the effect of ionic-liquid concentration and cation–anion combinations, would further test the generality of the temperature-centred mechanism proposed here.

---

## 6. Conclusions

A two-dimensional finite difference model, coupled with a genetic-algorithm-based inverse heat-transfer solution, has been developed and applied to estimate transient temperatures on the cutting-tool flank and rake faces from temperatures measured by a thermocouple embedded in the workpiece during interrupted orthogonal machining (peripheral down milling) of a plain medium carbon steel under dry and MQL conditions. The principal conclusions are as follows.

1. The inverse FD approach recovers the shear-zone heat flux, the shear-zone heat-partition fraction, and the tool–chip interface temperature without assuming the tool–chip friction coefficient or the heat-partition ratios. This is essential for MQL analysis, because those quantities are variable outcomes of the applied fluid's action and can be estimated analytically only under steady-state continuous cutting.

2. Validated against the analytical model of Loewen and Shaw for dry cutting, the FD estimates of rake-face temperature and of shear-zone heat partition agreed reasonably, with better agreement under heavy cutting. The FD shear-zone temperatures were systematically higher than the analytical values because the FD model, being driven by measured sub-surface temperatures, additionally captures the flank–workpiece contact heating that the analytical model neglects.

3. The estimated temperatures, compared with the measured thermal decomposition temperatures of the fluids, define two regimes of lubricant action. Where the temperature stays below decomposition — as in light machining at low speed — the fluids remain intact and lubricating action is dominated by viscosity; the more viscous fluids (PEG and oil + IL308(1 %)) then gave the lowest forces. Where the temperature exceeds decomposition — as at higher speeds and in heavy machining throughout the speed range — the fluids decompose and their decomposition chemistry governs behaviour; the fluorine-containing ionic liquid IL1 gave the sharpest force reductions through fluorine liberation and reduced tool–chip adhesion.

4. Correlation analysis showed a strong, persistent relationship between the estimated tool rake-face temperature and the cutting forces across almost all conditions, confirming the central role of the tool–chip interface temperature in governing the tribological outcome. In light machining at low speed, forces, roughness, and both temperatures were mutually strongly correlated; the correlations progressively simplified as speed rose, consistent with a transition from a viscosity-governed to a chemistry-governed regime. Surface roughness showed no significant correlation with forces or temperatures under heavy machining.

5. Overall, thermal modelling of the tribological conditions in machining is essential to understanding and optimizing cutting-fluid application, because the cutting temperatures determine whether an applied MWF acts physically or chemically. The inverse FD method presented here makes this determination operational and computationally inexpensive, providing a practical basis for the temperature-informed design and selection of MQL fluids, including tailored ionic liquids, for specific machining applications.

---

## Nomenclature

| Symbol | Meaning | Units |
|---|---|---|
| α | thermal diffusivity, K/(ρc_p) | m²/s |
| K | thermal conductivity | W/m·K |
| ρ | density | kg/m³ |
| c_p | specific heat capacity | J/kg·K |
| Δt | time step | s |
| Δx, Δy | node spacing in X, Y | m |
| T_{i,j}^{p} | temperature of node (i, j) at time step p | °C |
| q̇ | surface heat flux from moving source | W/m² |
| h | convective heat-transfer coefficient | W/m²·K |
| T_∞ | ambient temperature | °C |
| Fo | Fourier number, αΔt/(Δx)² | – |
| Bi | Biot number, hΔx/K | – |
| Vc | cutting speed | m/min |
| Ra | arithmetic mean surface roughness | µm |

---

## Tables

**Table 1.** Chemical composition of the workpiece material (plain medium carbon steel, ≈ AISI 1055), wt %.

| Element | C | Si | Mn | P | S | Cu | Cr | Mo | Ni | Al | Sn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| wt % | 0.55 | 0.24 | 0.73 | 0.04 | 0.04 | 0.09 | 0.27 | 0.02 | 0.10 | 0.03 | 0.01 |

**Table 2.** Plan of experiments: fixed and variable parameters.

| Parameter | Value |
|---|---|
| Machining operation | Peripheral down milling (interrupted orthogonal) |
| Machine | CNC vertical machining centre |
| Workpiece material | Plain medium carbon steel (≈ AISI 1055), 190 BHN |
| Cutting tool | Side-and-face milling cutter, dia 50 mm, radial rake 5°, axial rake 0° |
| Cutting insert | Uncoated cemented tungsten carbide (TPUN 160308-P30) |
| Compressed-air pressure | 5 kg/cm² |
| MQL flow rate | 39 ml/h |
| Replicates | 3 per condition |
| Cooling/MQL conditions | DRY; OIL (canola); IL1 (oil + 3 wt % BMIMPF6); PEG; PEG + IL1; IL308(1 %); IL308(0.5 %) |
| Light machining | feed 0.1 mm/tooth, depth 0.3 mm; Vc = 150, 200, 250 m/min |
| Heavy machining | feed 0.3 mm/tooth, depth 0.8 mm; Vc = 150, 200, 250 m/min |

**Table 3.** Viscosity and thermal decomposition temperature (5 % weight loss) of the MQL fluids.

| MQL fluid | Viscosity at 25 °C (mPa·s) | Decomposition temperature (°C) |
|---|---|---|
| Vegetable (canola) oil | 62.05 | 380 |
| Oil + IL1 | 71.36 | 341 |
| Oil + IL308(1 %) | 139.34 | 337 |
| Oil + IL308(0.5 %) | 70.54 | 366 |
| Polyethylene glycol (PEG) | 97.43 | 279 |
| PEG + IL1 | 68.55 | 272 |

**Table 4.** Representative Pearson correlation coefficients among mean machining force (F), surface roughness (Ra), estimated shear-zone temperature (T_sz) and estimated rake-face temperature (T_rf) in light machining. Bold denotes strong correlation (|r| > 0.669, p = 0.1).

| Vc (m/min) | Pair | r |
|---|---|---|
| 150 | F – Ra | **0.58** (moderate) |
| 150 | F – T_rf | **0.85** |
| 150 | Ra – T_sz | **0.76** |
| 150 | T_sz – T_rf | **0.78** |
| 200 | Ra – T_sz | **0.71** |
| 200 | F – T_rf | **0.91** |
| 250 | F – T_rf | **0.68** |
| 250 | Ra – T_sz | 0.31 (not significant) |

---

## Figure captions

**Figure 1.** Schematic of the interrupted orthogonal machining (peripheral down-milling) setup, showing the workpiece, single-insert cutter, MQL nozzle orientation, dynamometer, and the location of the K-type thermocouple embedded beneath the workpiece.

**Figure 2.** Two-dimensional finite difference discretization of the workpiece cross-section, showing the moving surface heat source traversing in the feed (X) direction, convective heat loss from the top face, the ambient-temperature boundaries, and the thermocouple location (approximately 11 mm along and 3 mm below the machined surface, for a 30 mm × 8 mm modelled section).

**Figure 3.** Heat-energy transfer to an interior node (i, j) from its four adjoining nodes (i ± 1, j) and (i, j ± 1), defining the node spacings Δx and Δy used in the explicit finite difference scheme.

**Figure 4.** Average shear-zone temperature versus cutting speed, estimated by the FD model and by the analytical (Loewen–Shaw) method, for (a) light and (b) heavy dry cutting. FD estimates are consistently higher because they include flank-contact heating.

**Figure 5.** Average tool rake-face temperature in the tool–chip contact zone versus cutting speed, estimated by the FD model and the analytical method, for (a) light and (b) heavy dry cutting. Agreement is reasonable and closer for heavy cutting.

**Figure 6.** Shear-zone heat-partition fraction (fraction of shear-zone heat carried by the chip) versus cutting speed, from the FD model and the analytical method, for (a) light and (b) heavy dry cutting.

**Figure 7.** Estimated average shear-zone and rake-face temperatures versus cutting speed under the different MWF conditions (DRY, OIL, IL1, PEG, PEG + IL1, IL308(1 %), IL308(0.5 %)) in light machining, shown relative to the fluids' thermal decomposition temperatures to distinguish viscosity-dominated from chemically dominated regimes.

---

## References

1. Incropera, F.P., DeWitt, D.P. *Fundamentals of Heat and Mass Transfer*. John Wiley & Sons, 1985.
2. Shaw, M.C. *Metal Cutting Principles*, 2nd ed. Oxford University Press, 2005.
3. Trent, E.M., Wright, P.K. *Metal Cutting*, 4th ed. Butterworth-Heinemann, Woburn, MA, 2000.
4. Boothroyd, G. *Fundamentals of Metal Machining and Machine Tools*. McGraw-Hill, 1988.
5. Childs, T., Maekawa, K., Obikawa, T., Yamane, Y. *Metal Machining: Theory and Applications*. Arnold, 2000.
6. Astakhov, V.P. *Tribology of Metal Cutting*. Elsevier, 2006.
7. Blok, H. Theoretical study of temperature rise at surfaces of actual contact under oiliness lubricating conditions. *Proc. Inst. Mech. Eng. General Discussion on Lubrication*, 1938.
8. Jaeger, J.C. Moving sources of heat and the temperature at sliding contacts. *Proc. R. Soc. NSW* 76 (1942) 203–224.
9. Trigger, K.J., Chao, B.T. An analytical evaluation of metal-cutting temperatures. *Trans. ASME* 73 (1951) 57–68.
10. Hahn, R.S. On the temperature developed at the shear plane in the metal-cutting process. *Proc. First US National Congress of Applied Mechanics*, 1951, 661–666.
11. Loewen, E.G., Shaw, M.C. On the analysis of cutting-tool temperatures. *Trans. ASME* 76 (1954) 217–231.
12. Rapier, A.C. A theoretical investigation of the temperature distribution in the metal cutting process. *Br. J. Appl. Phys.* 5 (1954) 400–405.
13. Weiner, J.H. Shear-plane temperature distribution in orthogonal cutting. *Trans. ASME* 77 (1955) 1331–1341.
14. Boothroyd, G. Temperatures in orthogonal metal cutting. *Proc. Inst. Mech. Eng.* 177 (1963) 789–810.
15. Tay, A.O., Stevenson, M.G., de Vahl Davis, G. Using the finite element method to determine temperature distributions in orthogonal machining. *Proc. Inst. Mech. Eng.* 188 (1974) 627–638.
16. Muraka, P.D., Barrow, G., Hinduja, S. Influence of the process variables on the temperature distribution in orthogonal machining using the finite element method. *Int. J. Mech. Sci.* 21 (1979) 445–456.
17. Strenkowski, J.S., Moon, K.-J. Finite element prediction of chip geometry and tool/workpiece temperature distributions in orthogonal metal cutting. *J. Eng. Ind.* 112 (1990) 313–318.
18. Stephenson, D.A., Jen, T.-C., Lavine, A.S. Cutting tool temperatures in contour turning: transient analysis and experimental verification. *J. Manuf. Sci. Eng.* 119 (1997) 494–501.
19. Komanduri, R., Hou, Z.B. Thermal modeling of the metal cutting process — Part II. *Int. J. Mech. Sci.* 43 (2001) 57–88.
20. Smith, A.J.R., Armarego, E.J.A. Temperature prediction in orthogonal cutting with a finite difference approach. *Ann. CIRP* 30 (1981) 9–13.
21. Lin, J. Inverse estimation of the tool-work interface temperature in end milling. *Int. J. Mach. Tools Manuf.* 35 (1995) 751–760.
22. Chen, W.C., Tsao, C.C., Liang, P.W. Determination of temperature distributions on the rake face of cutting tools using a remote method. *Int. Commun. Heat Mass Transfer* 24 (1997) 161–170.
23. Obikawa, T., Matsumura, T., Shirakashi, T., Usui, E. Wear characteristic of alumina coated and alumina ceramic tools. *J. Mater. Process. Technol.* 63 (1997) 211–216.
24. Lazoglu, I., Altintas, Y. Prediction of tool and chip temperature in continuous and interrupted machining. *Int. J. Mach. Tools Manuf.* 42 (2002) 1011–1022.
25. Abukhshim, N.A., Mativenga, P.T., Sheikh, M.A. Heat generation and temperature prediction in metal cutting: a review and implications for high speed machining. *Int. J. Mach. Tools Manuf.* 46 (2006) 782–800.
26. Goindi, G.S., Jayal, A.D., Sarkar, P. Application of ionic liquids in interrupted minimum quantity lubrication machining of plain medium carbon steel: effects of ionic liquid properties and cutting conditions. *J. Manuf. Process.* 32 (2018) 357–371.
27. Goindi, G.S., Sarkar, P. Dry machining: a step towards sustainable machining — challenges and future directions. *J. Clean. Prod.* 165 (2017) 1557–1571.
28. Goindi, G.S., Chavan, S.N., Mandal, D., Sarkar, P., Jayal, A.D. Investigation of ionic liquids as novel metalworking fluids during minimum quantity lubrication machining of a plain carbon steel. *Procedia CIRP* 26 (2015) 341–345.
29. Jayal, A.D. *Investigations into the mechanisms of cutting fluid action and effects on tool wear in machining* (Ph.D. dissertation), 2006.
30. Bermúdez, M.-D., Jiménez, A.-E., Sanes, J., Carrión, F.-J. Ionic liquids as advanced lubricant fluids. *Molecules* 14 (2009) 2888–2908.
31. Zhou, F., Liang, Y., Liu, W. Ionic liquid lubricants: designed chemistry for engineering applications. *Chem. Soc. Rev.* 38 (2009) 2590–2599.
32. Cai, M., Liang, Y., Zhou, F., Liu, W. A novel imidazolium salt with antioxidation and anticorrosion dual functionalities as the additive in poly(ethylene glycol) for steel/steel contacts. *Wear* 306 (2013) 197–208.
33. Sanes, J., Carrión, F.J., Bermúdez, M.D., Martínez-Nicolás, G. Ionic liquids as lubricants of polystyrene and polyamide 6-steel contacts. *Tribol. Lett.* 21 (2006) 121–133.
34. Weinert, K., Inasaki, I., Sutherland, J.W., Wakabayashi, T. Dry machining and minimum quantity lubrication. *Ann. CIRP* 53 (2004) 511–537.
