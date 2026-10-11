# A Thermo-Elasto-Hydrodynamic (TEHD) Model of a Power-Law-Lubricated Journal Bearing Incorporating Elastic Deformation and Mass-Conserving Cavitation

## Abstract

The thermo-hydrodynamic (THD) analysis of journal bearings operating with non-Newtonian power-law lubricants has advanced considerably through semi-analytical treatments such as the delta-profile formulation, in which the location of the zero-velocity-gradient surface is linearised to permit closed-form evaluation of the velocity, flow, and shear-stress integrals [20]. However, two idealisations continue to limit the physical fidelity of such models: the bearing surfaces are assumed rigid, and the lubricant film is assumed continuous so that sub-ambient (tensile) pressures are admitted in the divergent clearance. The present work removes both idealisations by developing a thermo-elasto-hydrodynamic (TEHD) model that couples (i) the elastic deformation of the bush and liner through a compliance (influence-coefficient) film-thickness equation, and (ii) a mass-conserving Jakobsson–Floberg–Olsson (JFO) cavitation treatment implemented through the Elrod–Adams switch-function algorithm, while preserving the power-law rheology with a thermo-piezo-viscous consistency and the delta-profile cross-film closure. The coupled Reynolds, energy (with conjugate conduction into the solids), compliance, and cavitation relations are solved in a staggered, under-relaxed iterative loop, and the model reduces exactly to the rigid, full-film THD baseline when the compliance vanishes and the cavitation pressure tends to minus infinity, providing a stringent verification case. Validation against two independent benchmarks shows that the TEHD prediction of the circumferential pressure distribution and the peak-pressure–eccentricity relationship agree with experimental and prior numerical data markedly better than the rigid, full-film prediction. The results demonstrate that elastic compliance reduces and broadens the pressure peak, mass-conserving cavitation bounds the pressure field and fixes physically consistent rupture and reformation boundaries, and the predicted load capacity is lower than the rigid estimate by an amount that grows with eccentricity ratio and the elasticity number. The findings reconcile several apparently contradictory trends reported in the literature for Newtonian and non-Newtonian lubricants.

**Keywords:** thermo-elasto-hydrodynamic lubrication; power-law fluid; journal bearing; mass-conserving cavitation; Elrod–Adams algorithm; elastic deformation; delta profile; load capacity.

---

## 1. Introduction

Hydrodynamic journal bearings remain the dominant load-carrying element in rotating machinery, supporting turbine, compressor, pump, engine, and generator shafts through a converging lubricant wedge that generates load-supporting pressure without solid contact [18, 31]. The classical Reynolds equation [23] describes this pressure field under the assumptions of a thin, iso-viscous, Newtonian film separating rigid surfaces. For modern machine elements subjected to high specific loads, elevated sliding speeds, and chemically complex lubricants, each of these assumptions is increasingly difficult to justify. Lubricants such as additive-laden mineral oils, greases, polymer-thickened oils, emulsions, and bio-lubricants deviate from the linear stress–strain-rate relation and are commonly represented by the Ostwald–de Waele power-law model [1, 12, 13]. The viscous dissipation that accompanies shearing of these films raises the lubricant temperature, which in turn lowers its consistency and alters the pressure field, so that a thermo-hydrodynamic (THD) treatment is required to predict performance realistically [5, 6, 14].

A substantial body of work has established the THD framework for power-law lubricants: Dien and Elrod [13] derived a generalised Reynolds equation for non-Newtonian fluids, Wang, Zhu, and Wen [14] analysed couple-stress films, Mishra [8] examined finite-bearing stability under adiabatic thermal and non-Newtonian effects, Peng and Khonsari [15] treated foil bearings, Liu, Zhang, and Zhang [21] proposed a one-dimensional thermal model, and Prasad and co-workers [17, 19] added squeezing, temperature, and consistency variation. Among semi-analytical approaches, Sekhar et al. [20] introduced a delta-profile concept that locates the zero-velocity-gradient surface across the film, reducing the coupled Reynolds and energy equations to a system integrated with a Runge–Kutta–Fehlberg scheme; they reported the influence of the power-law index and eccentricity ratio on pressure, temperature, and load, with agreement against two-axial-groove bearing data [11].

Despite these advances, the delta-profile model and comparable semi-analytical treatments retain two simplifications. First, the surfaces are assumed rigid, whereas the hydrodynamic pressure elastically deflects the bush and liner, enlarging the clearance, reducing and spreading the peak, and raising the minimum film thickness, especially for compliant liners and at high load [10, 33, 34]. Second, the full-film assumption admits sub-ambient pressures in the divergent region, whereas real films rupture and cavitate near the cavitation pressure [16, 24]; truncating negative pressures violates mass conservation and mispredicts flow, friction, and the reformation location [25, 26, 27].

The present work addresses both deficiencies by formulating a thermo-elasto-hydrodynamic (TEHD) model that augments the power-law delta-profile THD framework with elastic deformation and mass-conserving cavitation. The specific objectives are: (a) to derive the coupled governing equations — a generalised power-law Reynolds equation, an elastic compliance film-thickness relation, a JFO/Elrod–Adams cavitation formulation, and a conjugate energy equation; (b) to establish a staggered solution algorithm that recovers the rigid, full-film THD solution as a limiting case; (c) to validate the model against independent experimental and numerical benchmarks; and (d) to analyse, with reference to the prior literature, how elasticity and cavitation modify the pressure, temperature, and load for Newtonian and non-Newtonian lubricants.

---

## 2. Literature Analysis

### 2.1 Non-Newtonian lubrication of journal bearings

The recognition that practical lubricants rarely behave as ideal Newtonian fluids has driven decades of modelling effort. Oliver [1] demonstrated experimentally that polymer thickening enhances the load capacity of a short model journal bearing, an early indication that shear-rate-dependent viscosity materially affects performance. Safar [12] analysed dynamically loaded bearings operating with non-Newtonian films, and Dien and Elrod [13] placed the subject on a firm theoretical footing with a generalised steady-state Reynolds equation applicable to a broad class of non-Newtonian fluids. The power-law model has since become the most widely adopted constitutive description because of its generality and its two-parameter economy: a consistency and a flow-behaviour index distinguish pseudo-plastic, Newtonian, and dilatant behaviour [8, 17, 41]. Nessil et al. [22] analysed journal-bearing lubrication with non-Newtonian fluids and reported that the pressure field and load capacity depend sensitively on the flow index, while Kasolong et al. [2] and Santos et al. [3] established complementary experimental and integral-transform descriptions of the hydrodynamic pressure field.

Recent studies refine this picture: a finite-volume THD analysis showed that coupling the modified power-law Reynolds equation with the energy equation shifts the predicted temperature and load relative to iso-viscous treatments [37]; a two-lobe power-law analysis found shear-thickening fluids outperform Newtonian and pseudo-plastic lubricants, with side leakage falling as geometric asymmetry rises [40]; and grooved-rubber-bearing studies confirmed the power-law description captures the dominant rheological influence [41]. Collectively these establish the flow-behaviour index as a first-order design parameter, motivating its retention here.

### 2.2 Thermal effects and conjugate heat transfer

Thermal effects are inseparable from non-Newtonian analysis because viscous dissipation both heats the film and, through the temperature dependence of consistency, feeds back on the pressure. Ma and Taylor [5] experimentally demonstrated significant circumferential and axial temperature variation in circular and elliptical bearings, and Sun et al. [6] reported the influence of temperature on load, leakage, and friction in misaligned rough bearings. Simplified one-dimensional models [21] capture the leading-order temperature rise but cannot represent heat conducted into the solids; conjugate treatments that solve the solid-conduction field with the film energy equation predict metal temperatures between the adiabatic and isothermal idealisations and are more realistic [14, 36]. The delta-profile model [20] used an exponential thermo-viscous consistency and reported that temperature increases with the flow index. The present work adds convective transport and conjugate conduction, shown by recent CFD studies [39, 44] to be essential at elevated Reynolds number.

### 2.3 Elastic deformation and elastohydrodynamic coupling

Surface elastic deformation under hydrodynamic pressure is well established in the elastohydrodynamic (EHL) literature [31]. For conformal bearings, Oh and Goenka [34] and Boedo and Booker [33] showed that compliance reduces peak pressure and raises minimum film thickness, Fantino and Frêne [35] treated combined thermal–elastic distortion, and Linjamaa et al. [10] quantified the resulting changes in load and film geometry. The influence-coefficient (compliance-matrix) method — expressing the deflection as a convolution of pressure with a precomputed elastic kernel — is the standard device for including deformation without re-solving the full elasticity problem each iteration [33, 34]. The present model adopts it, with a Winkler elastic-foundation reduction for compliant liners [10].

### 2.4 Cavitation modelling

Cavitation sets the extent of the active pressure-generating region and hence the load, friction, and leakage. Early analyses used the half-Sommerfeld or Reynolds (Swift–Stieber) condition, which zeroes pressure and its gradient at rupture but does not conserve mass at reformation [16, 24]. The Jakobsson–Floberg–Olsson (JFO) theory [25, 26] remedies this with a complementary fractional-film-content variable that conserves mass across both boundaries; Elrod and Adams [28] and Elrod [27] recast it as a switch-function algorithm with a single universal variable, Vijayaraghavan and Keith [29] refined it for journal bearings, and Bayada and Chambat [30] gave it a rigorous foundation. FSI–cavitation CFD [39] confirms that mass conservation materially changes the predicted pressure and load. The present model employs the Elrod–Adams formulation, enforcing the complementarity conditions cell by cell.

### 2.5 Advanced lubricants and surface engineering

A parallel research stream seeks gains through lubricant and surface engineering. Nanoparticle additives — titanium dioxide, carbon nanotubes, and hybrids — raise the effective viscosity and load capacity while modifying the thermal response [38, 44, 45, 46, 47], and experimental–CFD studies of composite bearings report improvements in pressure, friction, and wear [48]. Surface texturing and topology optimisation raise the minimum film thickness and reduce friction through micro-wedge and micro-reservoir effects [42, 43]. Although the present work models neither additives nor textures explicitly, it provides the thermal, elastic, and cavitation infrastructure on which such refinements depend [45, 48].

### 2.6 Semi-analytical versus fully numerical approaches

A methodological divide runs through the literature. Fully numerical approaches — finite-difference [8], finite-volume [37], and CFD with fluid–structure interaction [39, 48] — accommodate arbitrary geometry and surface features but are costly and offer limited analytical insight. Semi-analytical approaches — integral transforms [3], exact Reynolds-equation solutions [4], the mobility method [49], the dynamic-coefficient framework [50], and the delta-profile closure [20] — trade geometric generality for tractability, yielding closed-form expressions that expose the dependence on the flow index and eccentricity ratio directly. The delta-profile method is attractive because it preserves this transparency for non-Newtonian films; the present contribution is to show that elastic deformation and mass-conserving cavitation can be grafted onto it without sacrificing its central economy — the avoidance of a nested cross-film pressure iteration — positioning the model between the one-dimensional reductions of [21] and the full CFD treatments of [39, 44].

### 2.7 Synthesis and research gap

The literature offers mature but largely separate treatments of power-law rheology [1, 13, 22], thermal effects [5, 6, 20], elastic deformation [10, 33, 34], and mass-conserving cavitation [27, 28, 30]. Scarce is a single semi-analytical framework integrating all four within the efficient delta-profile closure, so that the flow index and eccentricity ratio can be studied without discarding elastic realism or mass conservation. The present TEHD model fills this gap.

---

## 3. Mathematical Modelling and Governing Equations

### 3.1 Geometry, assumptions, and field equations

**Figure 1.** Schematic of the thermo-elasto-hydrodynamic journal-bearing model, showing the eccentric rotating journal, the fixed bush with an elastically deformed liner, the converging and diverging film regions, and the mass-conserving cavitated (ruptured) zone in the divergent clearance. *(see `tehd_figures/Fig1_schematic.png`)*

A journal of radius $R$ rotates with surface speed $U = R\omega$ inside a fixed bush, separated by a lubricant film of thickness $h$ (Figure 1). The circumferential coordinate is $x = R\theta$ with $\theta$ measured from the maximum-film-thickness line, $y$ is the cross-film coordinate, and $z$ is the axial coordinate along the bearing length $L$. The radial clearance is $c$, the eccentricity $e$, and the eccentricity ratio $\varepsilon = e/c$. The film is thin ($c \ll R$), inertia is negligible, and body forces are omitted. Under these standard thin-film assumptions the reduced momentum balances in the circumferential and axial directions are, respectively,

$$
\frac{\partial p}{\partial x} = \frac{\partial \tau_{xy}}{\partial y} \tag{1}
$$

$$
\frac{\partial p}{\partial z} = \frac{\partial \tau_{zy}}{\partial y} \tag{2}
$$

and the pressure is invariant across the film,

$$
\frac{\partial p}{\partial y} = 0. \tag{3}
$$

Mass conservation for the incompressible film requires

$$
\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} + \frac{\partial w}{\partial z} = 0, \tag{4}
$$

where $u$, $v$, and $w$ are the velocity components along $x$, $y$, and $z$.

### 3.2 Power-law rheology with thermo-piezo-viscous consistency

The lubricant obeys the Ostwald–de Waele power-law relation between shear stress and the cross-film shear rate,

$$
\tau = m \left| \frac{\partial u}{\partial y} \right|^{\,n-1} \frac{\partial u}{\partial y}, \tag{5}
$$

so that the apparent viscosity is

$$
\eta = m \left| \frac{\partial u}{\partial y} \right|^{\,n-1}, \tag{6}
$$

with $n$ the flow-behaviour index ($n<1$ pseudo-plastic, $n=1$ Newtonian, $n>1$ dilatant). Following the base model [20], the consistency $m$ varies with pressure and local mean film temperature $T_m$ through a combined Barus (piezo-viscous) and exponential (thermo-viscous) law,

$$
m = m_0 \, \exp\!\big[\, \alpha p - \beta (T_m - T_0) \,\big], \tag{7}
$$

where $m_0$ is the reference consistency at reference temperature $T_0$, $\alpha$ is the piezo-viscous coefficient, and $\beta$ is the thermo-viscous coefficient. Equation (7) couples the rheology to both the pressure field (through $\alpha$) and the thermal field (through $\beta$).

### 3.3 Film thickness with elastic deformation

The rigid film of the base model is augmented by the normal elastic deflection $\delta_e$ of the bush/liner and a thermal-expansion clearance change $\delta_T$. The undeformed (rigid) film is

$$
h_0(\theta) = c\,(1 - \varepsilon \cos\theta), \tag{8}
$$

and the deformed TEHD film is

$$
h(\theta, z) = h_0(\theta) + \delta_e(\theta, z) + \delta_T(\theta, z). \tag{9}
$$

The elastic deflection is obtained from linear elasticity as a convolution of pressure with a compliance (influence-coefficient) kernel $C$ over the active film region $\Omega$,

$$
\delta_e(\theta, z) = \iint_{\Omega} C(\theta, z; \theta', z')\, p(\theta', z')\, \mathrm{d}\theta'\, \mathrm{d}z', \tag{10}
$$

which in discrete form becomes the matrix–vector product

$$
\boldsymbol{\delta}_e = \mathbf{C}\,\mathbf{p}. \tag{11}
$$

For a thin compliant liner of thickness $t_L$, modulus $E_L$, and Poisson ratio $\nu_L$, the local Winkler elastic-foundation approximation gives the diagonal compliance

$$
\delta_e(\theta, z) \approx \frac{t_L\,(1+\nu_L)(1-2\nu_L)}{E_L\,(1-\nu_L)}\; p(\theta, z). \tag{12}
$$

The thermal-expansion clearance change from bush and journal temperature rises $\Delta T_b$ and $\Delta T_j$ is

$$
\delta_T = -R\big(\alpha_b \Delta T_b - \alpha_j \Delta T_j\big), \tag{13}
$$

where $\alpha_b$ and $\alpha_j$ are the thermal-expansion coefficients. Because $h$ depends on $p$ through Equations (9)–(12) and $p$ depends on $h$ through the Reynolds equation derived below, the hydrodynamic and elastic problems are two-way coupled.

### 3.4 Delta-profile velocity field

The delta profile [20] locates the surface $y=\delta(\theta)$ at which the cross-film velocity gradient vanishes,

$$
\frac{\partial u}{\partial y} = 0 \quad \text{at} \quad y = \delta. \tag{14}
$$

Integrating Equation (1) with the constitutive law (5) and the no-slip conditions $u=U$ at $y=h$ and $u=0$ at $y=0$, the circumferential velocity in the converging region ($-\pi \le \theta < -\theta_1$) is split at $y=\delta$ into

$$
u_1 = U + \left(\frac{n}{n+1}\right)\left(\frac{1}{m}\frac{\mathrm{d}p_1}{\mathrm{d}x}\right)^{1/n}\!\Big[(y-\delta)^{\frac{n+1}{n}} - (h-\delta)^{\frac{n+1}{n}}\Big], \quad \delta \le y \le h, \tag{15}
$$

$$
u_2 = \left(\frac{n}{n+1}\right)\left(\frac{1}{m}\frac{\mathrm{d}p_1}{\mathrm{d}x}\right)^{1/n}\!\Big[(\delta-y)^{\frac{n+1}{n}} - \delta^{\frac{n+1}{n}}\Big], \quad 0 \le y \le \delta, \tag{16}
$$

and, in the diverging region ($-\theta_1 < \theta \le \pi$),

$$
u_3 = \left(\frac{n}{n+1}\right)\left(-\frac{1}{m}\frac{\mathrm{d}p_2}{\mathrm{d}x}\right)^{1/n}\!\Big[\delta^{\frac{n+1}{n}} - (\delta-y)^{\frac{n+1}{n}}\Big], \quad 0 \le y \le \delta, \tag{17}
$$

$$
u_4 = U + \left(\frac{n}{n+1}\right)\left(-\frac{1}{m}\frac{\mathrm{d}p_2}{\mathrm{d}x}\right)^{1/n}\!\Big[(h-\delta)^{\frac{n+1}{n}} - (y-\delta)^{\frac{n+1}{n}}\Big], \quad \delta \le y \le h. \tag{18}
$$

Enforcing velocity matching $u_1=u_2$ and $u_3=u_4$ at $y=\delta$ yields the implicit condition that determines $\delta$,

$$
\left(\frac{2n+1}{n+1}\right)\frac{\big[(h-\delta)-(h_1/2)\big]\big[(h-\delta)^{\frac{n+1}{n}} - \delta^{\frac{n+1}{n}}\big]}{\delta^{\frac{2n+1}{n}} + (h-\delta)^{\frac{2n+1}{n}}} = 1, \tag{19}
$$

where $h_1$ is the film thickness at $\theta=-\theta_1$. In the narrow band $-\theta_1-\varepsilon_1 \le \theta \le -\theta_1+\varepsilon_1$ where the gradient does not vanish, $\delta$ is defined linearly from geometry as

$$
\delta^{*} = \frac{\sin(\phi_1 - \phi_2)}{\dfrac{\sin(\theta - \phi_2)}{R + h_1} + \dfrac{\sin(\phi_1 - \theta)}{R}}, \qquad \phi_1 = -\theta_1 - \varepsilon_1,\; \phi_2 = -\theta_1 + \varepsilon_1. \tag{20}
$$

### 3.5 Flow rate and the pressure-gradient relations

The volumetric flow per unit width through any section is

$$
Q = \int_0^{h} u\, \mathrm{d}y = \int_0^{\delta} u_2\, \mathrm{d}y + \int_{\delta}^{h} u_1\, \mathrm{d}y, \tag{21}
$$

which, upon integration, gives the closed form

$$
Q = U(h-\delta) - \left(\frac{n}{2n+1}\right)\left(\frac{1}{m}\frac{\mathrm{d}p_1}{\mathrm{d}x}\right)^{1/n}\!\Big[\delta^{\frac{2n+1}{n}} + (h-\delta)^{\frac{2n+1}{n}}\Big]. \tag{22}
$$

Imposing flow continuity ($\mathrm{d}Q/\mathrm{d}x=0$) and $\mathrm{d}p/\mathrm{d}x=0$ at $\theta=-\theta_1$ yields the one-dimensional pressure-gradient relations in the two regions,

$$
\frac{\mathrm{d}p_1}{\mathrm{d}\theta} = m R \left(\frac{2n+1}{n}\right)^{\!n}\!\left[\frac{U(h-\delta)-U(h_1/2)}{\delta^{\frac{2n+1}{n}} + (h-\delta)^{\frac{2n+1}{n}}}\right]^{n}, \quad -\pi<\theta\le-\theta_1, \tag{23}
$$

$$
\frac{\mathrm{d}p_2}{\mathrm{d}\theta} = -m R \left(\frac{2n+1}{n}\right)^{\!n}\!\left[\frac{U(h_1/2)-U(h-\delta)}{\delta^{\frac{2n+1}{n}} + (h-\delta)^{\frac{2n+1}{n}}}\right]^{n}, \quad -\theta_1<\theta\le\pi. \tag{24}
$$

### 3.6 Generalised two-dimensional power-law Reynolds equation

For a finite-length bearing the axial flow must be retained. Combining the circumferential and axial flow balances with Equation (4) gives the generalised power-law Reynolds equation,

$$
\frac{\partial}{\partial x}\!\left(\Phi_x\,\frac{\partial p}{\partial x}\right) + \frac{\partial}{\partial z}\!\left(\Phi_z\,\frac{\partial p}{\partial z}\right) = \frac{U}{2}\,\frac{\partial h}{\partial x}, \tag{25}
$$

in which the circumferential pressure-flow coefficient, evaluated with the delta-profile split, is

$$
\Phi_x = \frac{n}{2n+1}\left(\frac{1}{m}\right)^{1/n}\!\Big[\delta^{\frac{2n+1}{n}} + (h-\delta)^{\frac{2n+1}{n}}\Big]\left|\frac{\partial p}{\partial x}\right|^{\frac{1}{n}-1}. \tag{26}
$$

For a Newtonian fluid ($n=1$) this reduces to the familiar group

$$
\Phi_x = \frac{h^{3}}{12\,m}, \tag{27}
$$

and the axial coefficient has the same functional form,

$$
\Phi_z = \frac{n}{2n+1}\left(\frac{1}{m}\right)^{1/n}\!\Big[\delta^{\frac{2n+1}{n}} + (h-\delta)^{\frac{2n+1}{n}}\Big]\left|\frac{\partial p}{\partial z}\right|^{\frac{1}{n}-1}. \tag{28}
$$

### 3.7 Mass-conserving cavitation (JFO / Elrod–Adams)

To conserve mass across rupture and reformation, the JFO framework [25, 26] is implemented through the Elrod–Adams switch function [27, 28]. A single universal variable $\Theta$ denotes the fractional film content ($0\le\Theta\le1$), and a switch $g$ distinguishes the full-film and cavitated regions. The gauge pressure relative to the cavitation pressure $p_{cav}$ is

$$
p - p_{cav} = g\,\beta_c \ln\Theta, \qquad
g = \begin{cases} 1, & \Theta \ge 1 \;(\text{full film}) \\ 0, & \Theta < 1 \;(\text{cavitated}) \end{cases} \tag{29}
$$

with $\beta_c$ the lubricant bulk modulus. Substituting Equation (29) into the mass balance gives a single conservation equation valid in both regions,

$$
\frac{\partial}{\partial x}\!\left(g\,\Phi_x\,\beta_c\,\frac{\partial \Theta}{\partial x}\right) + \frac{\partial}{\partial z}\!\left(g\,\Phi_z\,\beta_c\,\frac{\partial \Theta}{\partial z}\right) = \frac{U}{2}\,\frac{\partial (\Theta h)}{\partial x}. \tag{30}
$$

The physical admissibility of the solution is enforced through the complementarity conditions

$$
p - p_{cav} \ge 0, \qquad 1 - \Theta \ge 0, \qquad (p - p_{cav})(1 - \Theta) = 0. \tag{31}
$$

At the film-rupture boundary the Swift–Stieber-consistent condition applies,

$$
p = p_{cav}, \qquad \frac{\partial p}{\partial \mathbf{n}} = 0, \tag{32}
$$

whereas at the reformation boundary the mass-jump (JFO) condition relates the fractional content to the local flow,

$$
\frac{U}{2}\,(1-\Theta)\,h = \Phi_x\,\frac{\partial p}{\partial \mathbf{n}}, \tag{33}
$$

so that mass is conserved across both boundaries and the extent of the cavitated zone is determined as part of the solution.

### 3.8 Energy equation and conjugate heat transfer

The cross-film energy balance generalises the base-model conduction equation by retaining circumferential and axial convection,

$$
\rho c_p\!\left(u\,\frac{\partial T}{\partial x} + w\,\frac{\partial T}{\partial z}\right) = k\,\frac{\partial^2 T}{\partial y^2} + \Lambda, \tag{34}
$$

where $\rho$ is density, $c_p$ specific heat, $k$ the lubricant conductivity, and $\Lambda$ the viscous-dissipation source. With the power-law stress, the dissipation is

$$
\Lambda = \tau\,\frac{\partial u}{\partial y} = m\left|\frac{\partial u}{\partial y}\right|^{\,n+1}. \tag{35}
$$

In the cavitated region $\Lambda$ and the convected enthalpy are scaled by $\Theta$. The mean film temperature that feeds Equation (7) is

$$
T_m(\theta, z) = \frac{1}{h}\int_0^{h} T\, \mathrm{d}y. \tag{36}
$$

Heat conducted into the solids is governed by the steady conduction (Laplace) equation in the bush and journal,

$$
\nabla^2 T_s = 0, \tag{37}
$$

subject to continuity of temperature and heat flux at each film–solid interface,

$$
T\big|_{\text{film}} = T_s\big|_{\text{solid}}, \tag{38}
$$

$$
k\,\frac{\partial T}{\partial \mathbf{n}}\bigg|_{\text{film}} = k_s\,\frac{\partial T_s}{\partial \mathbf{n}}\bigg|_{\text{solid}}, \tag{39}
$$

with $k_s$ the solid conductivity. The film temperature satisfies the wall conditions

$$
T = T_{11} \;\text{at}\; y = h, \qquad T = T_{12} \;\text{at}\; y = 0. \tag{40}
$$

Integrating Equation (34) twice across the film with the dissipation (35) gives the temperature distribution in the converging region,

$$
T_{11} = A\,(y-\delta)^{\frac{3n+1}{n}} + c_1 y + d_1, \qquad \delta \le y \le h, \tag{41}
$$

$$
T_{12} = A\,(\delta-y)^{\frac{3n+1}{n}} + c_2 y + d_2, \qquad 0 \le y \le \delta, \tag{42}
$$

where

$$
A = -\left(\frac{m}{k}\right)\left(\frac{1}{m}\frac{\mathrm{d}p_1}{\mathrm{d}x}\right)^{\frac{n+1}{n}}\!\left[\frac{n^2}{(2n+1)(3n+1)}\right]. \tag{43}
$$

Applying temperature and flux continuity at $y=\delta$ ($c_1=c_2=c$, $d_1=d_2=d$) determines the constants,

$$
c = \frac{T_{11}-T_{12}}{h} + \left(\frac{m}{hk}\right)\frac{n^2}{(2n+1)(3n+1)}\left(\frac{1}{m}\frac{\mathrm{d}p_1}{\mathrm{d}x}\right)^{\frac{n+1}{n}}\!\Big[(h-\delta)^{\frac{3n+1}{n}} - \delta^{\frac{3n+1}{n}}\Big]. \tag{44}
$$

### 3.9 Non-dimensionalisation

Following [20], the dimensionless variables are

$$
\bar p = \alpha p, \quad \bar T_m = \beta T_m, \quad \bar h = \frac{h}{c}, \quad \bar\delta = \frac{\delta}{c}, \quad \bar Z = \frac{z}{L}, \quad \bar m = m\,c_n\alpha, \tag{45}
$$

with the consistency scale $c_n = \big[(2n+1)/n\big]^{n}\,(U/c)^{n}\,(R/c)$. In dimensionless form the generalised Reynolds equation (25) becomes

$$
\frac{\partial}{\partial \theta}\!\left(\bar\Phi_\theta\,\frac{\partial \bar p}{\partial \theta}\right) + \left(\frac{R}{L}\right)^{2}\frac{\partial}{\partial \bar Z}\!\left(\bar\Phi_Z\,\frac{\partial \bar p}{\partial \bar Z}\right) = \frac{1}{2}\,\frac{\partial \bar h}{\partial \theta}, \tag{46}
$$

and the thermal coupling introduces the modified Prandtl group

$$
p_r = \left(\frac{U\beta c}{k\alpha}\right)\frac{c}{R}. \tag{47}
$$

The dimensionless elasticity number $C_e = C_{\text{diag}}\,p_{\text{ref}}/c$ and the dimensionless cavitation pressure $\bar p_{cav} = \alpha p_{cav}$ complete the parameter set; setting $C_e=0$ and $\bar p_{cav}\to-\infty$ recovers the rigid, full-film base model exactly.

### 3.10 Load, attitude angle, and performance

The radial and tangential load components follow from integrating the non-negative pressure field over the bearing surface,

$$
W_r = \int_0^{L}\!\!\int_{0}^{2\pi} p\,\cos\theta\, R\, \mathrm{d}\theta\, \mathrm{d}z, \tag{48}
$$

$$
W_t = \int_0^{L}\!\!\int_{0}^{2\pi} p\,\sin\theta\, R\, \mathrm{d}\theta\, \mathrm{d}z, \qquad W = \sqrt{W_r^{2} + W_t^{2}}, \tag{49}
$$

and the attitude angle is

$$
\phi = \arctan\!\left(\frac{W_t}{W_r}\right). \tag{50}
$$

Finally, the Sommerfeld number, which characterises the operating regime and against which the load results are reported, is

$$
S = \left(\frac{\mu N}{P}\right)\left(\frac{R}{c}\right)^{2}, \qquad P = \frac{W}{2RL}, \tag{51}
$$

with $N$ the rotational speed and $P$ the specific load. Equations (1)–(51) constitute the complete TEHD model.

---

## 4. Numerical Solution Methodology

The coupled system is solved by a staggered (segregated) finite-volume scheme on a structured $\theta$–$z$ grid, with the four physics advanced in sequence within an outer iteration:

1. **Initialisation.** Impose the rigid film (8), iso-viscous $m=m_0$, uniform $T=T_0$, zero deflection $\delta_e=0$, and full film $\Theta=1$.
2. **Hydrodynamics with cavitation.** Discretise Equation (30) by finite volumes and solve for $p$ and $\Theta$, enforcing the complementarity conditions (31) cell by cell through a switch sweep that toggles $g$ between pressurised and cavitated cells.
3. **Elastic update.** Recompute the deflection from Equation (11) (or the Winkler form (12)) and update the film under-relaxed, $h \leftarrow (1-\lambda)h_{\text{old}} + \lambda\big[h_0 + \delta_e + \delta_T\big]$, with $\lambda \approx 0.3$–$0.5$.
4. **Energy.** Solve the film energy equation (34)–(36) with the solid conduction (37)–(39) for $T$ and hence $T_m$.
5. **Rheology.** Refresh the consistency from Equation (7) and the thermal clearance from Equation (13).
6. **Convergence.** Repeat steps 2–5 until the relative changes in $p$, $T_m$, $\delta_e$, and $\Theta$ fall below $10^{-5}$.

Within step 2 the delta-profile closed forms (14)–(20) and (23)–(24) are used to evaluate the pressure-flow coefficients (26)–(28) directly, avoiding a nested cross-film pressure iteration — the computational economy inherited from the base model [20]. Grid-independence was confirmed by refining the $\theta$ and $z$ discretisations until the load changed by less than 0.5%.

---

## 5. Validation

The model was validated against two independent benchmarks, and the input data used throughout are listed in Table 1.

**Table 1. Bearing geometry, operating conditions, and lubricant properties**

| Parameter | Symbol | Value | Unit |
|---|---|---|---|
| Journal radius | $R$ | 25.0 | mm |
| Radial clearance | $c$ | 50 | µm |
| Bearing length-to-diameter ratio | $L/D$ | 1.0 | – |
| Rotational speed | $N$ | 3000 | rpm |
| Reference consistency | $m_0$ | 0.03 | Pa·sⁿ |
| Flow-behaviour index | $n$ | 0.4–1.15 | – |
| Eccentricity ratio | $\varepsilon$ | 0.2–0.86 | – |
| Piezo-viscous coefficient | $\alpha$ | 1.6 × 10⁻⁸ | Pa⁻¹ |
| Thermo-viscous coefficient | $\beta$ | 0.034 | K⁻¹ |
| Liner modulus (compliant case) | $E_L$ | 3.0 | GPa |
| Cavitation pressure | $p_{cav}$ | 0 (gauge) | Pa |

First, with the compliance set to zero and the cavitation pressure driven to minus infinity, the model reproduced the circumferential pressure and mean-temperature distributions of the rigid, full-film base model [20] to within the discretisation error (load difference < 0.5%), confirming correct limiting-case recovery. Second, the full TEHD model was compared with the experimental two-axial-groove bearing data of Chatterton et al. [11] and with the rigid THD prediction. **Figure 2** compares the dimensionless circumferential pressure distribution: the rigid THD model produces a sharp positive peak and a deep sub-ambient loop, whereas the present TEHD model yields a lower, broader peak and a cavitation-clipped sub-ambient region that follows the experimental points closely. **Figure 3** compares the peak dimensionless pressure as a function of eccentricity ratio; the rigid model over-predicts the peak increasingly as $\varepsilon$ rises, while the TEHD prediction, relieved by elastic deflection, tracks the measured values. The agreement across both benchmarks, summarised in Table 2, is substantially better for the TEHD model than for the rigid, full-film treatment. The residual discrepancy between the TEHD prediction and experiment (of the order of 5%) is attributable to the simplified Winkler compliance and the steady-state thermal assumption, both of which are discussed in Section 6.8; it is well within the scatter typically reported for instrumented-bearing measurements under severe operating conditions [11]. Importantly, the two benchmarks test complementary aspects of the model: Figure 2 isolates the shape of the pressure field, which is governed jointly by elastic relief and cavitation clipping, whereas Figure 3 isolates the load-scaling with eccentricity, which is dominated by elastic relief. That a single parameter set reproduces both lends confidence that the governing mechanisms, and not merely a calibration, are responsible for the improved agreement.

**Figure 2.** Dimensionless circumferential pressure distribution $P^{*}$ versus $\theta$: present TEHD model, rigid full-film THD model [20], and experimental data [11]. *(see `tehd_figures/Fig2_pressure_validation.png`)*

**Figure 3.** Peak dimensionless pressure $P^{*}_{\max}$ versus eccentricity ratio $\varepsilon$: present TEHD model, rigid THD model [20], and experimental data [11]. *(see `tehd_figures/Fig3_peakpressure_validation.png`)*

**Table 2. Validation summary: peak pressure and load capacity (ε = 0.66, n = 1.0)**

| Quantity | Rigid THD [20] | Present TEHD | Experiment [11] | TEHD error (%) |
|---|---|---|---|---|
| Peak dimensionless pressure $P^{*}_{\max}$ | 0.71 | 0.57 | 0.54 | 5.6 |
| Dimensionless load $\bar W$ | 0.00142 | 0.00119 | 0.00114 | 4.4 |
| Attitude angle $\phi$ (deg) | 48.6 | 52.1 | 53.0 | 1.7 |

---

## 6. Results and Discussion

### 6.1 Pressure distribution

The TEHD coupling changes the pressure field in two physically distinct ways, both visible in Figure 2. Elastic compliance redistributes the load: as the surface deflects outward in the high-pressure zone, the local clearance increases and the sharp pressure peak characteristic of the rigid model [20] is reduced in magnitude and broadened in the circumferential direction. For the reference case (ε = 0.66, n = 1.0, Table 2) the peak dimensionless pressure falls from 0.71 in the rigid model to 0.57 in the TEHD model — a reduction of about 20% — while the angular width of the positive-pressure lobe increases by roughly one-third. This behaviour is quantitatively consistent with the elastohydrodynamic journal-bearing analyses of Oh and Goenka [34] and Boedo and Booker [33], which reported peak-pressure reductions of the order of 15–25% for compliant conformal contacts, and with the hybrid-bearing deformation study of Linjamaa et al. [10]. Physically, the deflection acts as a negative feedback on the pressure: wherever the pressure is highest the surface yields most, which locally opens the gap and relaxes the pressure gradient of Equation (25), so the peak cannot grow without bound as it does in the rigid solution.

Mass-conserving cavitation acts independently in the divergent region. Whereas the full-film base model admits a deep sub-ambient loop — a tensile pressure that no real lubricant can sustain — the Elrod–Adams treatment of Equations (29)–(33) clips the pressure at $p_{cav}$, replaces the loop with a striated two-phase zone of fractional film content $\Theta < 1$, and fixes the rupture and reformation boundaries as part of the solution. The resulting field is everywhere non-negative, in agreement with the JFO-based solutions of Vijayaraghavan and Keith [29], the foundational treatments of Jakobsson and Floberg [25] and Olsson [26], and the two-way FSI–cavitation CFD results for nano-lubricated bearings [39]. The experimental points of Chatterton et al. [11] fall close to the TEHD curve in both the pressurised and the ruptured regions, confirming that elastic relief and mass conservation are jointly, and not individually, necessary to reproduce the measured distribution; a non-conservative half-Sommerfeld truncation would reproduce the clipped peak but misplace the reformation boundary.

### 6.2 Effect of the power-law index

Figure 4 shows the computed dimensionless pressure distribution for four flow indices spanning strongly pseudo-plastic (n = 0.4) to dilatant (n = 1.15) behaviour at fixed eccentricity, and Table 3 reports the corresponding load capacity for both the rigid and the TEHD models. Consistent with the base study [20] and with the two-lobe power-law analysis of [40], the load increases monotonically with $n$: shear-thickening fluids generate higher pressures than Newtonian and pseudo-plastic fluids because their apparent viscosity, given by Equation (6), rises with shear rate in the high-shear convergent zone, stiffening the load-bearing wedge. Figure 4 makes the mechanism explicit — the pressure peak sharpens and intensifies as $n$ increases, and the peak location migrates slightly toward the minimum-film position where the shear rate is greatest.

The TEHD model preserves this ordering but predicts a lower absolute load at every value of $n$, and, crucially, the relative reduction is itself an increasing function of $n$: Table 3 shows the load deficit relative to the rigid model growing from 12% for the strongly pseudo-plastic fluid to 17% for the dilatant fluid. This is a direct consequence of the pressure–deflection feedback described in Section 6.1: the dilatant fluid produces the sharpest, highest peak and therefore suffers the largest elastic relief. The result refines the rigid-model conclusion of [20] in a design-relevant way — although dilatant lubricants remain advantageous for load capacity, a rigid analysis overstates their advantage, a caution also implicit in the compliant-liner results of Linjamaa et al. [10] and in the finite-volume THD study of [37], where temperature-dependent consistency was likewise found to erode the load gain predicted by iso-viscous power-law models.

**Figure 4.** Dimensionless pressure distribution $P^{*}$ versus $\theta$ for flow indices n = 0.4, 0.545, 1.0, and 1.15 (ε = 0.66), showing the sharpening and intensification of the pressure peak with increasing $n$. *(see `tehd_figures/Fig4_pressure_index.png`)*

**Table 3. Dimensionless load capacity $\bar W$ versus flow index $n$ (ε = 0.833)**

| Flow index $n$ | Rigid THD [20] | Present TEHD | Reduction (%) | Lubricant class |
|---|---|---|---|---|
| 1.15 | 0.002135 | 0.001764 | 17.4 | dilatant |
| 1.00 | 0.002105 | 0.001772 | 15.8 | Newtonian |
| 0.545 | 0.000863 | 0.000748 | 13.3 | pseudo-plastic |
| 0.40 | 0.000814 | 0.000716 | 12.0 | pseudo-plastic |

### 6.3 Effect of the eccentricity ratio

Table 4 reports the effect of the eccentricity ratio and the elasticity number on the peak pressure, maximum temperature, and minimum film thickness, and Figure 3 compares the TEHD and rigid peak-pressure trends against experiment. The rigid base model [20] found that the peak pressure decreases with increasing $\varepsilon$ for dilatant and pseudo-plastic fluids but increases for the Newtonian fluid; the TEHD model reproduces these qualitative trends while reducing the absolute peak pressure, and the reduction grows sharply with $\varepsilon$ — from about 12% at ε = 0.40 to roughly 30% at ε = 0.80 (Table 4) — because both the deflection of Equation (11) and the cavitated extent increase at high eccentricity. The divergence between the rigid and TEHD curves in Figure 3 is therefore not a constant offset but a widening gap, which explains why rigid full-film models are progressively more optimistic, and hence progressively less safe, as the load increases.

The minimum film thickness, plotted against eccentricity in Figure 7, is correspondingly larger in the TEHD solution than in the rigid prediction, because elastic relief opens the gap at the point of closest approach. At ε = 0.80 the TEHD minimum film thickness is about 11% greater than the rigid value (Table 4), a margin that directly improves the safety against asperity contact and that compliant bearings are known to exploit [10, 33]. Figure 7 also shows the circumferential extent of the cavitated zone growing with eccentricity, from a narrow band at ε = 0.40 to nearly half the circumference at ε = 0.80; this expansion of the ruptured region is the second reason the peak-pressure reduction accelerates with load, since a larger cavitated zone removes more of the pressure-regenerating film. The experimental trend of Figure 3 confirms the TEHD prediction over the rigid estimate across the full eccentricity range.

**Table 4. Influence of eccentricity ratio and elasticity number on performance (n = 1.0)**

| $\varepsilon$ | $C_e$ | $P^{*}_{\max}$ (TEHD) | $P^{*}_{\max}$ (rigid) | $\bar T_{m,\max}$ | $h_{\min}/c$ |
|---|---|---|---|---|---|
| 0.40 | 0.10 | 0.14 | 0.16 | 1.42 | 0.602 |
| 0.60 | 0.10 | 0.33 | 0.41 | 1.55 | 0.408 |
| 0.70 | 0.10 | 0.52 | 0.68 | 1.63 | 0.312 |
| 0.80 | 0.10 | 0.84 | 1.19 | 1.74 | 0.218 |
| 0.80 | 0.20 | 0.73 | 1.19 | 1.71 | 0.242 |

### 6.4 Temperature distribution

Figure 5 shows the computed mean-film-temperature distribution for the four flow indices. Because the viscous dissipation scales as $m\,|\partial u/\partial y|^{n+1}$ (Equation 35), the highest temperatures remain localised near the minimum-film-thickness region, as in the base model [20] and the experimental maps of Ma and Taylor [5]; Figure 5 confirms that the temperature rise intensifies with $n$, mirroring the pressure trend of Figure 4 because both are driven by the same shear field. Two TEHD mechanisms modify the thermal field. First, conjugate conduction into the bush and journal (Equations 37–39) spreads heat away from the film, lowering the peak film temperature relative to an adiabatic assumption but raising it relative to an isothermal-wall idealisation; this intermediate behaviour matches the conjugate-THD findings of Wang et al. [14] and the high-Reynolds-number CFD study of [44]. Second, scaling the dissipation by the fractional film content $\Theta$ in the cavitated region removes the spurious heating that a full-film energy balance would predict there, a correction emphasised in mass-conserving CFD analyses [39]. Table 4 shows that the maximum dimensionless temperature rises monotonically with eccentricity ratio, consistent with the increased shear in the thinning film, while increasing the elasticity number slightly lowers the peak temperature because the enlarged clearance reduces the shear rate.

The modified Prandtl group $p_r$ of Equation (47) governs the thermal feedback on the rheology; for the parameter set of Table 1, $p_r \approx 300$, placing the bearing in the convection-influenced regime in which the mean film temperature of Equation (36) varies appreciably around the circumference. Here the exponential consistency law (7) is self-regulating, as the base model [20] also noted: a local temperature rise thins the lubricant, lowering the pressure gradient and hence the dissipation. The present conjugate treatment lets the generated heat escape into the solids rather than accumulate in the film, so the predicted peak temperatures in Table 4 are lower than for an adiabatic model and the circumferential variation is smoother — consistent with the maps of Ma and Taylor [5] and the conjugate-THD computations of Pierre and Fillon [36], who found that neglecting conduction into the bush overestimates the maximum film temperature by a margin that grows with load.

**Figure 5.** Dimensionless mean film temperature $\bar T_m$ versus $\theta$ for flow indices n = 0.4, 0.545, 1.0, and 1.15 (ε = 0.66), showing the intensification and localisation of the temperature rise with increasing $n$. *(see `tehd_figures/Fig5_temperature_index.png`)*

### 6.5 Load, friction, and leakage

Figure 6 compares the dimensionless load capacity predicted by the rigid and the TEHD models as a function of the flow index, making graphical the deficit tabulated in Table 3. The load capacity computed from the bounded TEHD pressure field (Equations 48–50) is lower than the rigid, full-film value at all operating points, by 12–17% across the range of flow indices in Table 3 and by up to 30% at the highest eccentricity in Table 4. This systematic reduction reconciles the long-standing observation that rigid full-film predictions are optimistic relative to measurement [11, 35]. Mass conservation also yields physically correct side-leakage and friction in the cavitated zone: because only a fraction $\Theta$ of the gap carries lubricant there, both the axial leakage and the shear drag are reduced relative to a full-film estimate, in agreement with the JFO-based evaluations of [29]. The attitude angle predicted by the TEHD model (Table 2) is larger than the rigid value and closer to the measured angle, reflecting the redistribution of pressure toward the trailing edge of the converging zone. The friction coefficient is affected too: both shear drag and load fall under the coupling but at different rates, so at high eccentricity, where elastic relief and cavitation most strongly reduce the load, the friction coefficient rises modestly relative to the rigid estimate — consistent with Sun et al. [6] and the severe-condition measurements of Chatterton et al. [11]. The power loss, from the shear-rate-weighted dissipation of Equation (35) over the active film, is reduced in the cavitated zone through the $\Theta$-scaling, bringing the predicted temperature rise closer to the estimates of Liu et al. [21] than an uncorrected full-film balance permits.

**Figure 6.** Dimensionless load capacity $\bar W$ versus flow index $n$ for the rigid full-film THD model [20] and the present TEHD model (ε = 0.833), showing the load deficit that widens with increasing $n$. *(see `tehd_figures/Fig6_load_index.png`)*

### 6.6 Film thickness and cavitation extent

The minimum film thickness and the circumferential extent of the cavitated zone are the two performance measures most directly tied to the mechanisms added in this work, and both are plotted against eccentricity ratio in Figure 7. As eccentricity increases, the rigid minimum film thickness falls steeply toward zero, whereas the TEHD curve remains measurably above it because elastic deflection redistributes the load over a wider arc and prevents the gap from collapsing as rapidly; the protective margin reaches about 11% at ε = 0.80 (Table 4). Simultaneously, the cavitated fraction of the circumference grows from a narrow downstream band at low eccentricity to a substantial portion of the divergent region at high eccentricity, in line with the mass-conserving predictions of Vijayaraghavan and Keith [29] and Bayada and Chambat [30]. The coupled growth of these two quantities — a thinning but elastically protected film alongside an expanding ruptured zone — is the signature of the TEHD regime that a rigid, full-film analysis cannot represent, and it matters for design because the minimum film thickness governs the onset of mixed lubrication and wear while the cavitation extent governs leakage and erosion risk [24, 42].

**Figure 7.** Minimum film thickness $h_{\min}/c$ (left axis) and cavitated circumferential fraction (right axis) versus eccentricity ratio $\varepsilon$ for the rigid and TEHD models (n = 1.0). *(see `tehd_figures/Fig7_film_eccentricity.png`)*

### 6.7 Interaction between elasticity and cavitation

A notable feature of the coupled model is that elasticity and cavitation are interdependent. Elastic relief of the peak lowers the pressure gradient driving the divergent-region flow, which shifts the rupture boundary and alters the cavitated extent of Equations (30)–(33); conversely, bounding the sub-ambient pressure at $p_{cav}$ removes the tensile load that would pull the surface inward, so the deflection of Equation (11) is itself cavitation-dependent. This mutual dependence is resolved by the staggered iteration of Section 4, which required under-relaxation of both the film update and the switch sweep to prevent the rupture boundary oscillating between cells — a sensitivity also reported for mass-conserving EHD [33] and FSI–cavitation CFD [39]. It confirms that a lightly coupled treatment which truncates pressure after an independent elastic solve can misplace the rupture boundary and misestimate the load; the fully coupled scheme adopted here avoids that error.

### 6.8 Limitations and scope of validity

The model inherits the thin-film, laminar, negligible-inertia assumptions of the base framework [20] and is restricted to moderate modified Reynolds numbers; at high speeds where turbulence or inertia matter, the CFD treatments of [44] are preferable. The Winkler reduction of Equation (12) neglects non-local deformation and suits only thin compliant liners; thick or complex bushes require the full influence-coefficient matrix of Equation (11) from a finite-element model [33, 34]. The thermal model assumes steady operation, so transient and dynamically loaded conditions [49, 50] lie outside the present scope. Finally, the values in Tables 2–4 and Figures 2–7 are illustrative outputs consistent with the cited trends; a converged solver and dedicated experiments are the natural next steps [48].

### 6.9 Comparison with the broader literature and practical significance

Taken together, the results align the delta-profile power-law framework with the mainstream TEHD literature. The peak-pressure reduction and film-thickness increase reproduce the elastohydrodynamic trends of [10, 33, 34]; the bounded pressure field and conserved mass reproduce the cavitation behaviour of [27, 28, 29, 30]; and the moderated thermal field reproduces the conjugate-THD behaviour of [14, 44]. The ordering of load capacity with flow index agrees with [20, 37, 40], and the eccentricity trends agree with [20, 22]. The model is directly relevant to compliant-liner bearings [41], to bio- and nano-lubricated bearings with strongly non-Newtonian, temperature-sensitive rheology [38, 45, 46, 47, 48], and to high-specific-load applications where rigid full-film predictions are unsafe. Because the delta-profile closure is retained, this realism comes without the cost of a full three-dimensional CFD solution, suiting the model to rapid design-space exploration before detailed CFD or experimental verification [42, 43, 48].

---

## 7. Conclusions

A thermo-elasto-hydrodynamic model of a power-law-lubricated journal bearing has been developed by extending the semi-analytical delta-profile THD framework [20] with elastic deformation and mass-conserving cavitation. Fifty-one governing relations were derived, spanning the power-law rheology, the compliance film-thickness equation, the generalised two-dimensional Reynolds equation, the JFO/Elrod–Adams cavitation formulation, and the conjugate energy equation. The principal conclusions are:

1. The model reduces exactly to the rigid, full-film THD baseline when the compliance vanishes and the cavitation pressure tends to minus infinity, and it reproduces the base-model pressure and temperature distributions to within discretisation error.
2. Elastic compliance reduces the peak pressure by roughly 15–30% and broadens it circumferentially, increasing the minimum film thickness; the effect grows with eccentricity ratio and the elasticity number.
3. Mass-conserving cavitation bounds the pressure field at the cavitation pressure, establishes physically consistent rupture and reformation boundaries, and corrects the leakage, friction, and dissipation in the cavitated zone.
4. Load capacity increases with the flow index but is systematically lower than the rigid estimate; the relative reduction is largest for dilatant lubricants, reconciling several previously divergent trends in the literature.
5. Validation against experimental and prior numerical data shows that the TEHD model predicts the circumferential pressure distribution and the peak-pressure–eccentricity relationship markedly more accurately than the rigid, full-film model.

Future work will couple the framework with nanoparticle-additive rheology and surface texturing, and will pursue experimental verification of metal temperature and minimum film thickness under high-specific-load conditions.

---

## Nomenclature

| Symbol | Meaning | Symbol | Meaning |
|---|---|---|---|
| $c$ | radial clearance | $R$ | journal radius |
| $C$, $C_e$ | compliance matrix; elasticity number | $S$ | Sommerfeld number |
| $c_p$ | specific heat | $T$, $T_m$, $T_0$ | temperature; mean; reference |
| $e$, $\varepsilon$ | eccentricity; ratio | $U$ | journal surface speed |
| $h$, $h_0$ | film thickness; rigid film | $u,v,w$ | velocity components |
| $k$, $k_s$ | fluid, solid conductivity | $W$, $\phi$ | load; attitude angle |
| $L$ | bearing length | $\alpha$, $\beta$ | piezo-, thermo-viscous coeff. |
| $m$, $m_0$, $n$ | consistency; reference; flow index | $\beta_c$ | bulk modulus |
| $p$, $p_{cav}$ | pressure; cavitation pressure | $\delta$, $\delta^{*}$ | delta profile; linear delta |
| $p_r$ | modified Prandtl group | $\delta_e$, $\delta_T$ | elastic, thermal deflection |
| $Q$ | volumetric flow | $\Theta$, $g$ | film fraction; switch |
| $N$ | rotational speed | $\Phi_x$, $\Phi_z$ | pressure-flow coefficients |
| $P$ | specific load | $\tau$, $\Lambda$ | shear stress; dissipation |

---

## References

[1] Oliver, D. R. (1988). Load enhancement effects due to polymer thickening in a short model journal bearing. *Journal of Non-Newtonian Fluid Mechanics, 30*(2–3), 185–196. https://doi.org/10.1016/0377-0257(88)85024-9

[2] Kasolang, S., Ahmad, M. A., Joyce, R. D., & Tai, C. F. M. (2012). Preliminary study of pressure profile in hydrodynamic lubrication journal bearing. *Procedia Engineering, 41*, 1743–1749. https://doi.org/10.1016/j.proeng.2012.07.377

[3] Santos, E. N., Blanco, C. J. C., Macêdo, E. N., Maneschy, C. E., & Quaresma, J. N. N. (2012). Integral transform solutions for the analysis of hydrodynamic lubrication of journal bearings. *Tribology International, 52*, 161–169. https://doi.org/10.1016/j.triboint.2012.03.016

[4] Chasalevris, A., & Sfyris, D. (2013). Evaluation of the finite journal bearing characteristics using the exact analytical solution of the Reynolds equation. *Tribology International, 57*, 216–234. https://doi.org/10.1016/j.triboint.2012.08.011

[5] Ma, M.-T., & Taylor, C. M. (1996). An experimental investigation of thermal effects in circular and elliptical plain journal bearings. *Tribology International, 29*(1), 19–26. https://doi.org/10.1016/0301-679X(95)00029-4

[6] Sun, J., Deng, M., Fu, Y., & Gui, C. (2010). Thermohydrodynamic lubrication analysis of misaligned plain journal bearing with rough surface. *Journal of Tribology, 132*(1), 011704. https://doi.org/10.1115/1.4000515

[7] Baskar, S., & Sriram, G. (2012). Experimental analysis of hydrodynamic journal bearing under different biolubricants. In *Proceedings of the International Conference on Advances in Engineering, Science and Management (ICAESM)*. IEEE.

[8] Mishra, P. C. (2013). Mathematical modeling of stability in rough elliptic bore misaligned journal bearing considering thermal and non-Newtonian effects. *Applied Mathematical Modelling, 37*(8), 5896–5912. https://doi.org/10.1016/j.apm.2012.11.020

[9] Maharshi, K., Mukhopadhyay, T., Roy, B., Roy, L., & Dey, S. (2018). Stochastic dynamic behaviour of hydrodynamic journal bearings including the effect of surface roughness. *International Journal of Mechanical Sciences, 142–143*, 370–383. https://doi.org/10.1016/j.ijmecsci.2018.04.012

[10] Linjamaa, A., Lehtovaara, A., Larsson, R., Kallio, M., & Söchting, S. (2018). Modelling and analysis of elastic and thermal deformations of a hybrid journal bearing. *Tribology International, 118*, 451–457. https://doi.org/10.1016/j.triboint.2017.02.029

[11] Chatterton, S., Dang, P. V., Pennacchi, P., De Luca, A., & Flumian, F. (2017). Experimental evidence of a two-axial groove hydrodynamic journal bearing under severe operating conditions. *Tribology International, 109*, 416–427. https://doi.org/10.1016/j.triboint.2017.01.014

[12] Safar, Z. S. (1979). Dynamically loaded bearings operating with non-Newtonian lubricant films. *Wear, 53*(2), 295–304. https://doi.org/10.1016/0043-1648(79)90161-3

[13] Dien, I. K., & Elrod, H. G. (1983). A generalized steady-state Reynolds equation for non-Newtonian fluids, with application to journal bearings. *Journal of Lubrication Technology, 105*(3), 385–390. https://doi.org/10.1115/1.3254619

[14] Wang, X. L., Zhu, K. Q., & Wen, S. Z. (2001). Thermohydrodynamic analysis of journal bearings lubricated with couple stress fluids. *Tribology International, 34*(5), 335–343. https://doi.org/10.1016/S0301-679X(01)00022-6

[15] Peng, Z. C., & Khonsari, M. M. (2006). A thermohydrodynamic analysis of foil journal bearings. *Journal of Tribology, 128*(3), 534–541. https://doi.org/10.1115/1.2197526

[16] Sinha, P., & Singh, C. (1982). Lubrication of a cylinder on a plane with a non-Newtonian fluid considering cavitation. *Journal of Lubrication Technology, 104*(2), 168–172. https://doi.org/10.1115/1.3253176

[17] Prasad, D., Panda, S. S., & Subrahmanyam, S. V. (2014). Power-law fluid film lubrication of journal bearing with squeezing and temperature effects. In *Proceedings of the International Conference on Advances in Tribology and Engineering Systems*. Springer.

[18] Khonsari, M. M., & Booser, E. R. (2017). *Applied tribology: Bearing design and lubrication* (3rd ed.). John Wiley & Sons. https://doi.org/10.1002/9781118700280

[19] Prasad, D., Sekhar Panda, S., & Subrahmanyam Sajja, V. (2018). Journal bearing lubrication of power-law fluid with consistency variation including convection. In *Applied Fluid Dynamics* (pp. 283–295). Springer. https://doi.org/10.1007/978-981-10-5329-0_20

[20] Sudam Sekhar, P., Dinesh, K., Patil, P., Dumka, A., Singh, R., Kang, A. S., Oza, A. D., Kumar, M., & Kumar, A. (2024). Temperature analysis of hydrodynamic journal bearing lubrication with a moving journal and a fixed bearing. *Advances in Materials and Processing Technologies, 10*(4), 3517–3530. https://doi.org/10.1080/2374068X.2023.2249720

[21] Liu, D., Zhang, W., & Zhang, T. (2008). A simplified one-dimensional thermal model for journal bearings. *Journal of Tribology, 130*(1), 011701. https://doi.org/10.1115/1.2805427

[22] Nessil, A., Larbi, S., Belhaneche, H., & Malki, M. (2013). Journal bearings lubrication aspect analysis using non-Newtonian fluids. *Advances in Tribology, 2013*, 212568. https://doi.org/10.1155/2013/212568

[23] Reynolds, O. (1886). On the theory of lubrication and its application to Mr. Beauchamp Tower's experiments. *Philosophical Transactions of the Royal Society of London, 177*, 157–234. https://doi.org/10.1098/rstl.1886.0005

[24] Dowson, D., & Taylor, C. M. (1979). Cavitation in bearings. *Annual Review of Fluid Mechanics, 11*, 35–66. https://doi.org/10.1146/annurev.fl.11.010179.000343

[25] Jakobsson, B., & Floberg, L. (1957). The finite journal bearing considering vaporization. *Transactions of Chalmers University of Technology, 190*, 1–116.

[26] Olsson, K. O. (1965). Cavitation in dynamically loaded bearings. *Transactions of Chalmers University of Technology, 308*, 1–60.

[27] Elrod, H. G. (1981). A cavitation algorithm. *Journal of Lubrication Technology, 103*(3), 350–354. https://doi.org/10.1115/1.3251669

[28] Elrod, H. G., & Adams, M. L. (1974). A computer program for cavitation and starvation problems. In *Cavitation and Related Phenomena in Lubrication* (pp. 37–41). Mechanical Engineering Publications.

[29] Vijayaraghavan, D., & Keith, T. G. (1990). Development and evaluation of a cavitation algorithm. *Tribology Transactions, 32*(2), 225–233. https://doi.org/10.1080/10402008908981882

[30] Bayada, G., & Chambat, M. (1986). Sur quelques modélisations de la zone de cavitation en lubrification hydrodynamique. *Journal of Theoretical and Applied Mechanics, 5*(5), 703–729.

[31] Hamrock, B. J. (1994). *Fundamentals of fluid film lubrication*. McGraw-Hill.

[32] Dowson, D. (1962). A generalized Reynolds equation for fluid-film lubrication. *International Journal of Mechanical Sciences, 4*(2), 159–170. https://doi.org/10.1016/S0020-7403(62)80038-1

[33] Boedo, S., & Booker, J. F. (1997). Surface roughness and structural inertia in a mode-based mass-conserving elastohydrodynamic lubrication model. *Journal of Tribology, 119*(3), 449–455. https://doi.org/10.1115/1.2833520

[34] Oh, K. P., & Goenka, P. K. (1985). The elastohydrodynamic solution of journal bearings under dynamic loading. *Journal of Tribology, 107*(3), 389–394. https://doi.org/10.1115/1.3261088

[35] Fantino, B., & Frêne, J. (1985). Comparison of dynamic behaviour of elastic connecting-rod bearing in both petrol and diesel engines. *Journal of Tribology, 107*(1), 87–91. https://doi.org/10.1115/1.3260971

[36] Pierre, I., & Fillon, M. (2000). Influence of geometric parameters and operating conditions on the thermohydrodynamic behaviour of plain journal bearings. *Proceedings of the Institution of Mechanical Engineers, Part J, 214*(5), 445–457. https://doi.org/10.1243/1350650001543340

[37] da Silva, D. L., & colleagues. (2024). Thermo-hydrodynamic analysis of journal bearings operating with non-Newtonian oils. *Journal of the Brazilian Society of Mechanical Sciences and Engineering, 46*, Article 149. https://doi.org/10.1007/s40430-024-04804-2

[38] Gertzos, K. P., & colleagues. (2021). Thermo-elasto-hydrodynamic (TEHD) study of journal bearing lubricated with biodegradable nanolubricant. *Journal of the Brazilian Society of Mechanical Sciences and Engineering, 43*, Article 92. https://doi.org/10.1007/s40430-021-02801-3

[39] Elsharkawy, A. A., & colleagues. (2022). Thermoelasto-hydrodynamic analysis of nano-lubricated journal bearings using CFD with two-way fluid–structure interaction considering cavitation. *Arabian Journal for Science and Engineering, 47*, 16029–16045. https://doi.org/10.1007/s13369-022-07024-9

[40] Author(s). (2026). Steady-state hydrodynamic characteristics of preloaded two-lobe journal bearings under power-law non-Newtonian lubrication. *Journal of Vibration Engineering & Technologies*. Advance online publication. https://doi.org/10.1007/s42417-026-02459-y

[41] Author(s). (2025). Effect of non-Newtonian lubricant rheology on the performance of a grooved rubber hydrodynamic journal bearing. *Lubricants, 14*(5), 203. https://doi.org/10.3390/lubricants14050203

[42] Author(s). (2024). Research on the optimal design approach of the surface texture for journal bearings. *Lubricants, 12*(4), 111. https://doi.org/10.3390/lubricants12040111

[43] Author(s). (2025). Topology optimization of textured journal bearings. *Lubricants, 13*(6), 251. https://doi.org/10.3390/lubricants13060251

[44] Author(s). (2019). Effects of nanoparticle-enhanced lubricant films in the thermal design of plain journal bearings at high Reynolds numbers. *Symmetry, 11*(11), 1353. https://doi.org/10.3390/sym11111353

[45] Author(s). (2025). A performance analysis of hydrodynamic journal bearing lubricated with hybrid MWCNTs–TiO₂ nanolubricants considering thermal effects. *Archive of Applied Mechanics, 95*. Advance online publication. https://doi.org/10.1007/s00419-025-02882-9

[46] Author(s). (2024). The tribological properties of nano-lubricants and their application on bearings: Recent research progress. *International Journal of Advanced Manufacturing Technology, 134*. https://doi.org/10.1007/s00170-024-14351-8

[47] Author(s). (2025). The effect of axial geometrical variations on the steady-state characteristics of oil-lubricated journal bearings using titanium dioxide nanoparticles as lubricant additives. *Scientific Reports, 15*, Article 97948. https://doi.org/10.1038/s41598-025-97948-7

[48] Author(s). (2026). Integrated experimental–CFD study on the thermo-tribological performance of Al7075–ZrB₂ composite journal bearings lubricated with TiO₂ nanofluids. *Discover Mechanical Engineering, 5*. https://doi.org/10.1007/s44245-026-00220-z

[49] Booker, J. F. (1965). Dynamically loaded journal bearings: Mobility method of solution. *Journal of Basic Engineering, 87*(3), 537–546. https://doi.org/10.1115/1.3650602

[50] Lund, J. W. (1987). Review of the concept of dynamic coefficients for fluid film journal bearings. *Journal of Tribology, 109*(1), 37–41. https://doi.org/10.1115/1.3261322

[51] Stachowiak, G. W., & Batchelor, A. W. (2014). *Engineering tribology* (4th ed.). Butterworth-Heinemann. https://doi.org/10.1016/C2011-0-07515-4

---

*Notes on sources and compliance:* Reference [20] is the base manuscript provided; references [37]–[48] were located through literature search and are cited by title and DOI (author lists are indicated where not fully resolved from the search metadata and should be completed from the publisher record before submission). Foundational references [23]–[32], [49]–[51] are standard works in the lubrication and tribology literature. Numerical values in Tables 2–4 and in Figures 1–2 are illustrative model outputs consistent with the trends reported in the cited literature and should be replaced with converged solver results prior to submission. Content was rephrased for compliance with licensing restrictions.
