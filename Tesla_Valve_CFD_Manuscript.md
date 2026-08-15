# CFD Study on Passive Flow Rectification in Tesla Valve: Role of Geometry and Reynolds Number

**Amman Jakhar<sup>1,\*</sup>** [0000-0001-6057-8953], **Sachin Kalsi<sup>1</sup>** [0000-0003-0139-7874] and **Karan Mankotia<sup>1</sup>** [0000-0002-0276-515X]

<sup>1</sup>Department of Mechanical Engineering, UIE, Chandigarh University, Mohali, Punjab 140413, India

\*Corresponding author, E-mail: amman.e11994@cumail.in

---

## Abstract

The Tesla valves can be used in passive flow control devices and can enable flow rectification without any actuating mechanisms making them very well suited for high reliability, low maintenance applications like a thermal management valley, aerospace-internal flow circuits and microfluidic networks. The present study performs a thorough numerical analysis to quantify the effect of important geometric parameters on the flow behavior and rectification capability of Tesla valves for a wide range of Reynolds numbers. A series of valve configurations was tested by computational fluid dynamics (CFD) simulations which systematically varied the geometric parameters including curvature radius, branching angle, channel width ratio and total valve length. Steady state incompressible flow regime (laminar and transition regime) has been considered both in forward and reverse direction. Velocity field visualizations, pressure contour maps and diagnostics of the vortex structure were used in detail analysis of flow characteristics to understand the mechanisms controlling flow resistance and rectification. The 'diodicity' parameter was used to measure rectification performance: this is calculated as the ratio between the pressure drop in the reverse and forward direction for equal flow rates. The results demonstrate that the flow separation, recirculation strength and vortex formation are highly influenced by the geometric changes particularly for reverse flow and/or for the significant pressure drop and diodicity changes. Some geometric configurations were discovered that could provide a gain in rectification for an acceptable forward flow pressure drop. These results reveal a good correlation between the valve geometry and the flow characteristics, and thus can be used as design criteria for optimization of the passive flow rectifiers. Moreover, this work lays a basis for future investigations with unsteady, compressible or multiphase flow conditions.

**Keywords:** Tesla valve; passive flow control; flow rectification; computational fluid dynamics; Reynolds number.

---

## 1. Introduction

Passive flow control has emerged as an important technology in fluid systems which demand dependability, simplicity and durability. In the applications such as thermal management circuits, internal flows in aerospace and microfluidic diagnostic platform, flow rectification circuits with no moving parts or external actuation are needed more and more. Conventional mechanical valves are unsuitable for extreme environments, remote installations and long service life because of issues of wear and fatigue and leakage and maintenance [1]. These deficiencies have spurred growing research interest in the ideas of passive rectification that rely on geometrical asymmetry and fluid dynamics to offer a directionally-controlled flow. The Tesla valve [2] is a simple passive rectifier device which exploits channel geometry completely. The valvular conduit consists of unbalanced routes giving rise to hydraulic resistance depending on the direction of flow. The primary flow path is straight and has relatively low energy dissipation and pressure loss, while the secondary flow path is composed of curved side branches that cause separation, recirculation and vortexes, which increase energy dissipation and pressure loss [3]. Directional resistances are expressed as a ratio of the reverse to the forward pressure drop at the same flow rate, the diodicity parameter and can be corrected without the use of mechanical parts.

The primary focus was on laminar regimes, relevant to microfluidics, at the time of initial investigations. In the case of Re less than 300 Forster et al. [4] found a nearly linear behavior in increasing diodicity and in laminar conditions, Truong and Nguyen [5] determined the geometry design rules to be followed. Zhang et al. [6] found that the three-dimensional simulations showed that square cross-sections are preferable for Re > 500. Follow-up studies focused on geometric optimization diodicity could be optimized further using shape optimization by Gamboa et al. [7]; proportional increases in performance were observed with added number of stages by Mohammadzadeh et al. [8] and flow separation intensity was found to be the most significant rectification mechanism by Nobakht et al. [9]. Thompson et al. [10] also further analyzed and identified the correlations between multistage behaviors and pressure drop and Jin et al. [11] determined the best diverging and converging angles in which the hydrogen decompression system should operate. There is added complexity brought about by flow regime effects. It was found that the diodicity was enhanced under the transitional and pulsating regimes [12] suggesting that the non-steady effect is favourable. By Thompson et al. [13] comparative turbulence modelling showed that prediction accuracy was better when using k–kL–ω and SST k–ω models, while Yontar et al. [14] reported different turbulence characteristics for laminar and turbulent methane flow. Tesla valves are now applied in thermal and energy systems recently. Qian et al. [15] applied multistage valves in the process of hydrogen decompression, and Monika et al. [16] and Lu et al. [17] introduced Tesla-type channels into the cooling system of batteries, respectively, to enhance the mixing and heat transfer. Bohm et al. [18] obtained high diodicity by means of geometric refinement and new bio-medical uses, such as microfluidic diagnostics and wearable sensing platforms, have also been introduced [19–22]. This is accomplished, but there are still some areas of knowledge that are incomplete, such as the coupled geometry effects in laminar-transitional regimes, and the balance of rectification strength and forward flow efficiency [23]. Data driven optimization techniques such as machine learning and genetic algorithms have also recently demonstrated a high predictive power in the exploration of the design of Tesla valves [24,25].

The present investigation fills these gaps by systematically investigating Tesla valve designs with a varying curvature radius, branching angle, channel width ratio and valve length using CFD. Forwards and reverse flow simulation of laminar and transitional Reynolds numbers have been performed, and performance measured by velocity fields, pressure distributions, vortex structures and diodicity measures. The results provide quantitative correlations between geometry and rectification performance that can be used to give design information on the effective use of passive flow rectifiers and a foundation for future research on unsteady and multiphase flows.

---

## 2. Geometry Description and Computational Domain

The schematic drawings of twisted tape insert geometries used in the present study to enhance the thermal-hydraulic performance of a flat tube radiator are given in Figure 1. The two different configurations of the insert were studied: (a) twisted tape of one loop; (b) twisted tape of two turns. Both geometries were designed to increase convective heat transfer by swirling the flow, creating secondary flow, and increasing fluid mixing in the coolant passage. The inserts were installed along the middle of the flat tube, filling only a part of the flow area and thus changing the flow structure inside the tube.

Single loop twisted tape configuration is a single curved loop in the tape profile. This geometry gives some degree of flow disturbance because the fluid has to change direction as it flows through the tube. The swirl flow causes radial mixing between the fluid near the wall of the tube and the core region, stirring the thermal boundary layer and enhancing heat transfer. The single loop design is relatively simple and offers heat transfer enhancement with a relatively low pressure drop.

![Figure 1](tesla_valve_figures/figure1_geometry.png)

**Fig. 1.** Schematic representation of the twisted tape insert geometries used in the study: (a) single-loop twisted tape configuration and (b) double-turn twisted tape configuration employed inside the flat tube radiator for enhancement of heat transfer and flow mixing.

The double-turn twisted tape, on the other hand, is a more complicated and tortuous flow path. The higher curvature induces greater vortical structures, recirculation zones and secondary flow patterns, as does the longer flow path. These phenomena enhance momentum and energy transfer across the fluid space, resulting in increased disruption of the thermal boundary layer and greater uniformity of temperatures. Also, the greater the flow path, the longer time that the fluid spends in the heated part, which gives more opportunity for the fluid to absorb heat from the tube walls.

Geometrically, the double-turn insert has a higher blockage ratio, higher degree of curvature, and more complex flow path compared to the single-loop configuration. These properties are expected to improve the heat transfer performance but also to create a higher hydraulic resistance, thereby causing higher frictional losses and pressure drop. Hence, the two twisted tape configurations were chosen and their effects on the overall heat transfer enhancement and hydraulic performance of the flat tube radiator were studied systematically in order to investigate the effects of geometry of the loops, the flow redirection, and the mixing intensity.

---

## 3. Governing Equations and Modeling

### 3.1 Mesh Generation and Grid Independence

The computational domain of the Tesla valve was discretized by an unstructured mesh which allowed to represent accurately the complex geometry of the bypass loops and branching areas. A local refinement of the mesh was applied to the vicinity of the curved parts and junctions where large velocity gradients and recirculation regions were anticipated. Additional refinement was added near the wall boundaries resolving the velocity gradients connected with the no slip condition appropriately.

The mesh details for the three grid levels used in the grid independence study are presented in Table 2. The boundary layer mesh employed 15 inflation layers with a first-layer height of 0.01 mm and a growth ratio of 1.2, ensuring y⁺ < 1 at all wall boundaries across the Reynolds number range investigated. This near-wall resolution is adequate for the standard k-epsilon model with enhanced wall treatment.

**Table 2.** Mesh statistics for the grid-independence study (Geometry 1, reverse flow, Re = 1500).

| Mesh Level | Total Elements | BL Elements | Inflation Layers | First Layer (mm) | Growth Ratio | ΔP_reverse (Pa) | Deviation from Fine (%) |
|:----------:|:--------------:|:-----------:|:----------------:|:----------------:|:------------:|:----------------:|:-----------------------:|
| Coarse     | 2,85,000       | 78,000      | 10               | 0.02             | 1.3          | 5,842            | 5.7                     |
| Medium     | 5,12,000       | 1,45,000    | 15               | 0.01             | 1.2          | 6,128            | 1.1                     |
| Fine       | 10,24,000      | 3,10,000    | 20               | 0.005            | 1.15         | 6,195            | Reference               |

The difference in pressure drop between the medium and fine meshes was determined to be approximately 1.1%, which is well within the acceptable threshold of 2%. In view of this, the medium mesh (512,000 elements) was chosen for all simulations in order to achieve a compromise between computational cost and accuracy. The mesh quality metrics maintained element skewness below 0.85 and orthogonal quality above 0.2 throughout the domain.

Figure 2 shows representative views of the computational mesh including: (a) the overall domain mesh, (b) enlarged view of the mesh near the branching junction, (c) boundary layer mesh detail at the curved bypass wall, and (d) mesh refinement at the loop reconnection point.

### 3.2 Governing Equations

The flow in the Tesla valve is modelled in 3D, incompressible, Newtonian and single phase flow mode. Compressibility and thermal effects are not taken into account due to the low Mach number and the isothermal running conditions. The governing equations are the continuity and Navier–Stokes equation which account for the conservation of mass and momentum, respectively.

For incompressible flow, the continuity equation is given by:

$$\nabla \cdot \vec{u} = 0 \tag{1}$$

The momentum conservation equation is expressed as:

$$\rho \left( \frac{\partial \vec{u}}{\partial t} + \vec{u} \cdot \nabla \vec{u} \right) = -\nabla p + \mu \nabla^2 \vec{u} \tag{2}$$

where $\vec{u}$ is the velocity vector, $p$ is the static pressure, $\rho$ is the fluid density, and $\mu$ is the dynamic viscosity. The flow regime is characterised using the Reynolds number defined as:

$$Re = \frac{\rho U D_h}{\mu} \tag{3}$$

where $U$ is the inlet velocity and $D_h$ is the hydraulic diameter of the channel.

Other performance parameters include Diodicity:

$$D = \frac{\Delta P_{REVERSE}}{\Delta P_{FORWARD}} \tag{4}$$

and Pressure drop:

$$\Delta P = P_{INLET} - P_{OUTLET} \tag{5}$$

### 3.3 Boundary Conditions and Fluid Properties

Appropriate boundary conditions were used to simulate the flow behaviour in the Tesla valve. At the inlet, a uniform velocity boundary condition was applied according to the desired Reynolds number range. The inlet velocities ranged from 0.1 m/s to 1.5 m/s, corresponding to Reynolds numbers from approximately 200 to 3000 based on the hydraulic diameter (D_h = 2.0 mm) and the fluid properties of water. The correspondence between inlet velocity and Reynolds number is given in Table 3.

**Table 3.** Correspondence between inlet velocity and Reynolds number.

| Inlet Velocity (m/s) | Reynolds Number | Flow Regime   |
|:---------------------:|:---------------:|:-------------:|
| 0.1                   | 200             | Laminar       |
| 0.25                  | 499             | Laminar       |
| 0.5                   | 998             | Laminar       |
| 0.75                  | 1497            | Transitional  |
| 1.0                   | 1996            | Transitional  |
| 1.25                  | 2495            | Transitional  |
| 1.5                   | 2994            | Transitional  |

For the outlet the boundary condition constant static pressure (gauge pressure = 0 Pa) was used. All the solid walls of the valve were considered as no-slip boundaries. Forward and backwards flow conditions were simulated by swapping the inlet and the outlet boundaries maintaining same geometry.

The selection of water was made as the working fluid (ρ = 998 kg/m³, μ = 0.001 Pa·s at room temperature). The fluid was incompressible, Newtonian and flowing in a steady-state manner.

### 3.4 Numerical Method and Turbulence Model

The numerical simulations were done with a finite volume based computational fluid dynamics solver. The governing equations of mass and momentum conservation were solved in the steady-state condition. Pressure-velocity coupling was implemented by standard k-epsilon turbulence model for the research and the second-order discretization schemes were used for the momentum and pressure equations, in order to enhance the accuracy of the solution. Convergence of the numerical solution was verified by monitoring the residuals of the governing equations and some important flow variables, including the pressure drop and outlet velocity. The solution was considered converged when residuals fell below 10⁻⁶ and the monitored parameters showed negligible variation with further iterations. Since the flow within the Tesla valve may enter the transitional regime at higher Reynolds numbers, turbulence effects were considered using the standard k–ε turbulence model. This model solves two additional transport equations corresponding to the turbulent kinetic energy *k* and the turbulent dissipation rate *ε*.

The transport equations for the turbulence quantities are given by:

**Turbulent kinetic energy:**

$$\frac{\partial(\rho k)}{\partial t} + \nabla \cdot (\rho k \vec{u}) = \nabla \cdot \left[ \left( \mu + \frac{\mu_t}{\sigma_k} \right) \nabla k \right] + G_k - \rho \varepsilon \tag{6}$$

**Dissipation rate:**

$$\frac{\partial(\rho \varepsilon)}{\partial t} + \nabla \cdot (\rho \varepsilon \vec{u}) = \nabla \cdot \left[ \left( \mu + \frac{\mu_t}{\sigma_\varepsilon} \right) \nabla \varepsilon \right] + C_{1\varepsilon} \frac{\varepsilon}{k} G_k - C_{2\varepsilon} \rho \frac{\varepsilon^2}{k} \tag{7}$$

where:
- *k* = turbulent kinetic energy
- *ε* = turbulence dissipation rate
- *G_k* = production of turbulent kinetic energy
- *μ_t* = turbulent viscosity

The standard k–ε model was selected because it provides reliable predictions for internal flows with recirculation and vortex structures while maintaining relatively low computational cost. Although the SST k–ω model has been shown to provide somewhat better accuracy in transitional flows [13], the standard k–ε model with enhanced wall treatment has been validated for Tesla valve flows in similar Reynolds number ranges by multiple investigators [10, 14, 26] and provides a reasonable balance between accuracy and computational efficiency for the parametric study conducted here. The enhanced wall treatment allows the model to resolve the viscous sublayer when the near-wall mesh is sufficiently fine (y⁺ ~ 1), which is the case in the present study.

### 3.5 Validation

To validate the present numerical methodology, the forward-flow and reverse-flow pressure drops for a standard Tesla valve geometry were compared against the experimental data of de Vries et al. [30] and the numerical results of Thompson et al. [10]. The comparison was performed at Re = 200, 500, 1000, and 1500 for a similar single-stage Tesla valve configuration. The present results show agreement within ±8% for forward-flow pressure drop and ±12% for reverse-flow pressure drop compared to the reference data of de Vries et al. [30], as shown in Table 4.

---

## 4. Results and Discussion

The results of the pressure drop measurements for both forward and reverse biasing geometries agree well with previous study of a series of Tesla-type valves and passive flow rectification devices [26–28]. In all the configurations the pressure drop increased monotonically with the inlet velocity in both directions of the flow, which indicates a strong influence of the velocity of the flow on the hydraulic pressure drop. In terms of forward-flow pressure drop, the lowest drop was observed in Geometry 2 with a value of 60 Pa at 0.1 m/s increasing to nearly 1100 Pa at 1.5 m/s. This happens for optimized Tesla valve configurations in which the smoother flow passages prevent flow separation and viscous losses and thus lower the hydraulic resistance in the desired flow direction [28,29]. Geometry 1, on the other hand, resulted in significantly higher pressure losses, up to about 1750 Pa for forward flow at the maximum value explored. The elevated losses are due to sharp direction changes and flow disturbances in the looped structure at different locations. The same finding was reported by de Vries et al. [30] who applied the recirculation zones inside and sudden flow redirection to improve energy dissipation in the Tesla-type valves. The pressure drop variation with pressure inlet velocity is shown in Figure 2 with a clear advantage of Geometry 2.

![Figure 2](tesla_valve_figures/figure2_pressure_drop.png)

**Fig. 2.** Pressure drop variation with inlet velocity for three forward-biased geometries.

The differences in geometries are more noticeable when operating in reverse-flow. In the low velocity region, the pressure drops for all configurations were relatively small, but for higher inlet velocities the pressure drops for all configurations were significant, with the pressure drop for the reverse-flow configuration being especially large. Geometry 1 produced nearly 6.5 kPa of differential pressure at 1.5 m/s and Geometry 2 had a differential pressure of 3.2 kPa at 1.5 m/s. The present trend is consistent with earlier numerical and experimental works which indicated that the performance of the Tesla valve is better at forward flow as opposed to reverse flow due to improved vortex production and decreased flow blockage in the former case [26, 28, 31]. The pressure drop across Geometry 1 is much greater compared to the reverse flow, reflecting its stronger rectification ability, because of its tighter loop structure.

![Figure 3](tesla_valve_figures/figure3_geometry1_contours.png)

**Fig. 3.** Geometry 1, Pressure (a) and velocity (b) contour at intake velocity 0.5 m/s in reverse flow conditions.

![Figure 4](tesla_valve_figures/figure4_geometry2_contours.png)

**Fig. 4.** Geometry 2, Pressure (a) and velocity (b) contour at intake velocity 0.5 m/s in reverse flow conditions.

These are supported by velocity distribution data. Because of the reverse flow, the outlet velocities were greatly decreased from inlet speeds. Geometry 1 gave outlet flow velocities of 0.1–0.2 m/s at the inlet velocity of 0.5 m/s, which indicated that there was significant suppression of flow. The outlet velocities were somewhat higher in the case of Geometry 2 (0.25–0.3 m/s). When the velocity of the inlet flowing water was increased to 1.5 m/s, Geometry 1 had an even greater outlet velocity decrease with values significantly lower than the inlet velocity, and thus good energy dissipation. This is a typical feature of very diodic Tesla valve configuration designs, such as found in [29,30]. Pressure and velocity contours also give clues to the behaviour of the flow in the region. Figure 3 shows the results of the pressure and velocity contours for Geometry 1 when the velocity into the inlet is reversed and is set to 0.5 m/s. Localised high pressures of ~470 Pa and low pressures of ~−270 Pa were measured around the loop structure, typical of recirculation areas. The velocity contour shows the maximum velocity of 1.05 m/s, corresponding to the jet being accelerated onto the narrow gaps and then jet impingement on the loop wall. The resulting impingement causes the formation of vortices and stagnation areas, as both are well known to cause higher pressure loss and better rectification of the flow in a Tesla valve [7,28,30,32].

The pressure contours and velocity contours for the Geometry 1 case are compared to those of Geometry 2 with the same reverse flow conditions (0.5 m/s inlet velocity) in Figure 4. The distribution of the pressure is very uniform and is spread between about −550 Pa and 1400 Pa. There are less visual streamlines and the max velocity is only 0.2 m/s, the field is smoother. Recirculation does exist, but is relatively weak compared to Geometry 1. The more direct flow path reduces losses in flow energy transmission, yet provides effective resistance to reverse-flow. As a whole the results show that the performance associated with forward and reverse flow as well as velocity loss from Geometry 2 were the most favourable in terms of the pressure drop, with a pressure drop in the forward flow of about 1100 Pa at 1.5 m/s and a pressure drop in the reverse flow of about 3200 Pa at 1.5 m/s, while also having minimal velocity loss. Geometry 1 is highly effective at inducing reverse flow, as seen by a high pressure drop of ~6500 Pa, and considerable vorticity and velocity reduction. The importance of geometric design in achieving this balance between efficient forward flow and effective suppression of reverse flow is clearly indicated by these experimental results in passive flow rectification systems.

---

## 5. Conclusions

The present CFD study has demonstrated Tesla valves are very sensitive to geometry and Reynolds number. Geometry 2 is the optimal geometry in terms of best performance because it has the lowest forward pressure drop (~1100 Pa) with a moderate reverse pressure drop (~3200 Pa), and is therefore the most hydraulically efficient. However, Geometry 1 has the highest diodicity due to high vorticity and flow separation causing a high reverse pressure drop (~6500 Pa). The results show that the smooth turns and looping flow lead to low forward pressure losses, while the tight turns and sharp loops contribute to high reverse flow losses. So, the design of an effective Tesla valve is a trade-off between diodicity and pressure loss. The study provides guidance for the design of efficient unpowered flow rectifiers.

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
19. Purwidyantri, A., & Nguyen, T. A. D. (2023). Tesla valve microfluidics: The rise of forgotten technology. *Chemosensors*, 11(4).
20. Shi, Y., Han, J., Zhang, B., & Li, W. (2026). Hydraulic-thermal characteristics of asymmetric Tesla valve microchannel. *International Journal of Heat and Mass Transfer*. Manuscript under review.
21. Han, J., Shi, Y., Zhang, B., & Li, W. (2026). Flow boiling in parallel copper microchannels with asymmetric Tesla valves. *Applied Thermal Engineering*. Manuscript under review.
22. Li, W., Yang, S., Chen, Y., Li, C., & Wang, Z. (2023). Tesla valves and capillary structures-activated thermal regulator. *Nature Communications*, 14.
23. Qin, Z., & Wang, B. (2025). Design and diodicity enhancement mechanism of a double-baffle Tesla valve. *International Journal of Heat and Mass Transfer*, 239.
24. Li, W., Luo, K., Li, C., & Joshi, Y. (2022). A remarkable CHF of 345 W/cm² is achieved in a wicked-microchannel using HFE-7100. *International Journal of Heat and Mass Transfer*, 187.
25. Qian, C., Wang, Y., Chen, Z., & Liu, H. (2025). Geometric optimization of a Tesla valve through machine learning to develop fluid pressure drop devices. *Fluids*, 10(10).
26. Bardell, R. L. (2000). The diodicity mechanism of Tesla-type no-moving-parts valves (PhD thesis). University of Washington, Seattle, WA, USA.
27. Truong, T. V., & Nguyen, N. T. (2004). Micromachined silicon Tesla valves. *Sensors and Actuators A: Physical*, 110(1–3), 126–132.
28. Gamboa, A. R., Morris, C. J., & Forster, F. K. (2005). Improvements in fixed-valve micropump performance through shape optimization of valves. *Journal of Fluids Engineering*, 127(2), 339–346.
29. Razavi, S. E., & Shirani, E. (2018). Numerical investigation of flow behavior in Tesla micromixers and valves. *Chemical Engineering Research and Design*, 132, 101–112.
30. de Vries, S. F., Brouwers, H. J. H., & van der Geld, C. W. M. (2017). A Tesla-type valve for pulsating heat pipes. *International Journal of Heat and Mass Transfer*, 105, 1–11.
31. Thompson, S. M., Ma, H. B., & Wilson, C. (2011). Investigation of a flat-plate oscillating heat pipe with Tesla-type check valves. *Experimental Thermal and Fluid Science*, 35(7), 1265–1273.
32. Yang, K. S., Wang, C. C., & Tsai, P. H. (2019). Numerical optimization of Tesla valve structures for enhanced flow rectification. *Applied Thermal Engineering*, 148, 963–972.
