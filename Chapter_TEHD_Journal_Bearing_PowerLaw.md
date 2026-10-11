# Thermo-Elasto-Hydrodynamic (TEHD) Analysis of a Power-Law-Lubricated Journal Bearing with Elastic Deformation and Mass-Conserving Cavitation

## Abstract

**Background.** A recent semi-analytical study modelled the thermo-hydrodynamic (THD) lubrication of a journal bearing operating with a non-Newtonian power-law fluid, introducing a "delta (δ) profile" to locate the zero-velocity-gradient surface and so couple the Reynolds and energy equations [1]. That model assumes rigid bearing surfaces and treats the lubricant film as continuous (no rupture). Both assumptions limit physical realism: at high load and eccentricity the bush and liner deform elastically, and in the divergent (downstream) region the film ruptures and cavitates.

**Objective.** To extend the rigid-surface, full-film THD model into a thermo-elasto-hydrodynamic (TEHD) model by (i) adding elastic deformation of the bearing surface to the film-thickness equation through a compliance (influence-coefficient) formulation, and (ii) replacing the full-film assumption with a mass-conserving Jakobsson–Floberg–Olsson (JFO) cavitation treatment implemented through the Elrod–Adams switch-function algorithm, while retaining the power-law rheology with temperature- and pressure-dependent consistency.

**Methods.** The modified power-law Reynolds equation, a 3-D energy equation with conjugate heat conduction into the solids, a linear-elasticity compliance relation, and the Elrod–Adams cavitation algorithm are solved in a staggered (segregated) iterative loop until the pressure, temperature, deformation, and cavity-fraction fields are mutually converged. The δ-profile concept of the base paper is retained to simplify the cross-film velocity and shear-stress integrals.

**Expected outcomes.** Relative to the rigid, full-film THD baseline, the TEHD model is expected to predict lower and broader peak pressures, a physically bounded (non-negative) pressure field with a well-defined film-rupture boundary, higher peak temperatures localised near minimum film thickness, and a modified load capacity whose sign of change depends on the power-law index *n* and the eccentricity ratio ε.

**Keywords:** thermo-elasto-hydrodynamic lubrication (TEHD); power-law fluid; journal bearing; mass-conserving cavitation; JFO/Elrod–Adams; elastic deformation; delta profile.

---

## 1. Introduction

Hydrodynamic journal bearings separate the rotating journal from the stationary bush by a converging-wedge lubricant film that generates load-supporting pressure. For heavily loaded and high-speed machinery the lubricant is frequently non-Newtonian — additive-laden mineral oils, greases, polymer-thickened oils, and bio-lubricants all deviate from the linear stress–strain-rate relation and are commonly represented by the power-law (Ostwald–de Waele) model, in which the apparent viscosity varies with shear rate through an index *n* and a consistency *m*.

The base study [1] developed a semi-analytical THD solution for a power-law-lubricated bearing in which the journal rotates and the bush is fixed. Its principal contributions were (a) a *delta profile* that linearises the location of the zero-velocity-gradient surface across the film, allowing the velocity, flow, and shear-stress integrals to be evaluated in closed form, and (b) a coupled treatment of the Reynolds and energy equations with a consistency that depends on both pressure and mean film temperature. The resulting ordinary differential equations were integrated with a Runge–Kutta–Fehlberg scheme, and the influence of *n* and ε on pressure, temperature, and load was reported.

Two idealisations in that model restrict its applicability to real bearings:

1. **Rigid surfaces.** The film thickness is prescribed purely by the rigid geometry, `h = c(1 − ε cos θ)`. In practice the hydrodynamic pressure elastically deforms the bush and liner, enlarging the effective clearance in the high-pressure zone, lowering and spreading the pressure peak, and increasing the minimum film thickness. This elasto-hydrodynamic coupling becomes significant for compliant liners (polymer, white-metal, rubber) and at high specific load.

2. **Full (continuous) film.** The base energy/Reynolds coupling admits negative pressures in the divergent region. Real films cannot sustain tension; they rupture and cavitate, forming a striated two-phase (liquid + vapour/gas) zone at (or near) the lubricant's cavitation pressure. Simply truncating negative pressures (the half-Sommerfeld or Reynolds/Swift–Stieber boundary condition) violates mass conservation across the rupture and reformation boundaries and mispredicts flow, friction, and the reformation location.

A thermo-elasto-hydrodynamic (TEHD) model removes both idealisations by solving, simultaneously, the hydrodynamics of the film, the elastic deformation of the solids, the thermal field (with temperature-dependent rheology and conjugate conduction into the solids), and a mass-conserving cavitation model. Recent literature confirms the value of this coupling: finite-volume THD solutions for power-law oils [2], TEHD studies with nano- and bio-lubricants following the power law [3], and CFD/FSI analyses incorporating cavitation [4] all report that elasticity and cavitation materially change the predicted pressure, temperature, and load.

This chapter formulates such a TEHD extension while **retaining the power-law rheology and the δ-profile machinery of the base paper**, so that the present model is a strict superset of [1]: setting the elastic compliance to zero and the cavitation pressure to −∞ recovers the original rigid, full-film THD solution as a limiting case.

---

## 2. Governing Equations

The coordinate system follows the base paper: `x = Rθ` is the circumferential coordinate (θ measured from the maximum-film-thickness line), `y` is the cross-film coordinate, and `z` is the axial coordinate along the bearing length `L`. The journal of radius `R` rotates with surface speed `U = Rω`; the bush is fixed. The radial clearance is `c` and the eccentricity ratio is `ε = e/c`.

### 2.1 Power-law rheology with thermo-piezo-viscous consistency

The lubricant obeys the Ostwald–de Waele model, with the shear stress related to the cross-film velocity gradient by

$$
\tau = m \left| \frac{\partial u}{\partial y} \right|^{\,n-1} \frac{\partial u}{\partial y},
$$

where `n` is the power-law (flow-behaviour) index — `n = 1` Newtonian, `n < 1` pseudo-plastic (shear-thinning), `n > 1` dilatant (shear-thickening). As in [1] the consistency `m` varies with pressure `p` and local mean film temperature `T_m` through a combined Barus (piezo-viscous) / exponential (thermo-viscous) law,

$$
m = m_0 \, \exp\!\big[\, \alpha p - \beta (T_m - T_0) \,\big],
$$

with `α` the piezo-viscous coefficient, `β` the thermo-viscous coefficient, `m_0` the reference consistency at reference temperature `T_0`. This is the key TEHD feedback on rheology: pressure stiffens the fluid, temperature thins it.

### 2.2 Film-thickness equation with elastic deformation (the elasto-coupling)

The rigid film of the base paper is augmented by the normal elastic deflection `δ_e(θ, z)` of the bush/liner surface and, optionally, a thermal-expansion clearance change `δ_T(θ, z)`:

$$
h(\theta, z) = c\,(1 - \varepsilon \cos\theta) + \delta_e(\theta, z) + \delta_T(\theta, z).
$$

The elastic deflection is obtained from linear elasticity as a convolution of the hydrodynamic pressure with a **compliance (influence-coefficient) matrix** `C`, precomputed once from a finite-element model of the bush (or from the elastic half-space / thin-shell approximation for a compliant liner):

$$
\delta_e(\theta, z) = \iint_{\Omega} C(\theta, z;\, \theta', z')\, p(\theta', z')\, \mathrm{d}\theta'\,\mathrm{d}z'
\quad\Longrightarrow\quad
\boldsymbol{\delta}_e = \mathbf{C}\, \mathbf{p},
$$

where `Ω` is the active (pressurised) film region and the discrete form `δ_e = C p` is used in computation. For a thin compliant liner of thickness `t_L`, Young's modulus `E_L`, and Poisson's ratio `ν_L`, the simple-elastic-foundation (Winkler) approximation gives a local, diagonal compliance

$$
\delta_e(\theta, z) \approx \frac{t_L\,(1+\nu_L)(1-2\nu_L)}{E_L\,(1-\nu_L)}\; p(\theta, z),
$$

which is convenient for a first implementation and is replaced by the full `C` matrix when non-local deformation matters. Because `h` now depends on `p` (through `δ_e`) and `p` depends on `h` (through the Reynolds equation), the hydrodynamic and elastic problems are **two-way coupled**.

### 2.3 Modified power-law Reynolds equation

Integrating the momentum balance across the film with the power-law constitutive law and the δ-profile boundary treatment of [1] yields the generalised (2-D, finite-length) Reynolds equation for a power-law fluid,

$$
\frac{\partial}{\partial x}\!\left( \Phi_x\, \frac{\partial p}{\partial x} \right)
+ \frac{\partial}{\partial z}\!\left( \Phi_z\, \frac{\partial p}{\partial z} \right)
= \frac{U}{2}\,\frac{\partial h}{\partial x},
$$

where the pressure-flow coefficients `Φ_x`, `Φ_z` carry the non-Newtonian dependence. Using the δ-profile to split the film at the zero-shear surface `y = δ`, these coefficients take the form

$$
\Phi \;=\; \frac{n}{2n+1}\left(\frac{1}{m}\right)^{1/n}
\left[\, \delta^{\frac{2n+1}{n}} + (h-\delta)^{\frac{2n+1}{n}} \,\right]
\left|\frac{\partial p}{\partial x}\right|^{\frac{1}{n}-1},
$$

reducing, for `n = 1`, to the familiar Newtonian group `h^3/(12 m)`. The explicit single-coordinate forms `dp₁/dθ` and `dp₂/dθ` of equations (14)–(15) in [1], together with the δ-matching condition (their equation 16) and the linear δ* definition (their equation 17), are retained to evaluate `Φ` semi-analytically within each control volume.

### 2.4 Mass-conserving cavitation (JFO via the Elrod–Adams switch)

To respect mass conservation across film rupture and reformation, the JFO framework is adopted and implemented with the Elrod–Adams switch function. A single universal variable `Θ` (the fractional film content, `0 ≤ Θ ≤ 1`) and a switch `g` distinguish the two regions:

- **Full-film (pressurised) region:** `g = 1`, `Θ = 1`, pressure `p ≥ p_cav` is the unknown.
- **Cavitated (ruptured) region:** `g = 0`, `p = p_cav` (constant), fractional film content `Θ < 1` is the unknown.

The gauge pressure relative to cavitation is written as `p − p_cav = g·β_c·ln Θ` with bulk modulus `β_c`, so that a single conservation equation governs both regions:

$$
\frac{\partial}{\partial x}\!\left( g\,\Phi_x\, \beta_c\, \frac{\partial \Theta}{\partial x} \right)
+ \frac{\partial}{\partial z}\!\left( g\,\Phi_z\, \beta_c\, \frac{\partial \Theta}{\partial z} \right)
= \frac{U}{2}\,\frac{\partial (\Theta h)}{\partial x}.
$$

The complementarity conditions
$$
p - p_{cav} \geq 0,\qquad 1-\Theta \geq 0,\qquad (p-p_{cav})(1-\Theta) = 0
$$
are enforced cell-by-cell, which automatically locates the rupture boundary (Swift–Stieber-consistent, `p = dp/dn = 0`) and the reformation boundary (a jump condition conserving mass). This replaces the base paper's implicit full-film assumption and guarantees `p ≥ p_cav` everywhere.

### 2.5 Energy equation with conjugate heat transfer

The cross-film energy balance generalises equation (18) of [1] to include convection and axial conduction, and is coupled to heat conduction in the solids. In the film,

$$
\rho c_p\!\left( u\,\frac{\partial T}{\partial x} + w\,\frac{\partial T}{\partial z} \right)
= k\,\frac{\partial^2 T}{\partial y^2} \;+\; \underbrace{\tau\,\frac{\partial u}{\partial y}}_{\text{viscous dissipation}} ,
$$

where the dissipation term, with the power-law stress, is `τ ∂u/∂y = m |∂u/∂y|^{n+1}`. In the cavitated region the dissipation and transported enthalpy are scaled by the film fraction `Θ`. The mean film temperature feeding the consistency law is, as in [1],

$$
T_m(\theta, z) = \frac{1}{h}\int_0^{h} T \, \mathrm{d}y .
$$

Conjugate conduction in the bush and journal,
$$
\nabla^2 T_{\text{solid}} = 0,
$$
is solved with continuity of temperature and heat flux at the film–solid interfaces, so the model predicts realistic metal temperatures rather than assuming adiabatic or isothermal walls. The thermal field also drives the thermal-expansion clearance change `δ_T` in §2.2.

### 2.6 Load and performance

The load components and attitude angle follow from integrating the (now non-negative) pressure field over the bearing surface,

$$
W_r = \iint p \cos\theta \, R\, \mathrm{d}\theta\, \mathrm{d}z, \qquad
W_t = \iint p \sin\theta \, R\, \mathrm{d}\theta\, \mathrm{d}z, \qquad
W = \sqrt{W_r^2 + W_t^2}, \qquad
\phi = \arctan\!\frac{W_t}{W_r}.
$$

Friction torque, power loss, and side-leakage flow are obtained from the shear stress at the journal surface and the axial pressure-driven flow, each scaled by the film fraction `Θ` in the cavitated zone.

---

## 3. Non-Dimensionalisation

Following [1], define

$$
\bar p = \alpha p,\quad \bar T_m = \beta T_m,\quad \bar h = h/c,\quad \bar\delta = \delta/c,\quad
\bar m = m\, c_n \alpha,\quad c_n = \left(\frac{2n+1}{n}\right)^{\!n}\!\left(\frac{U}{c}\right)^{\!n}\frac{R}{c},
$$

and the modified Prandtl group `p_r = (U β c / k α)(c/R)`. The additional TEHD groups are an **elasticity (compliance) number**

$$
C_e = \frac{\alpha\,\bar p_{\text{ref}}\, c}{c} \;\sim\; \frac{\text{elastic deflection}}{\text{clearance}}
= \frac{C_{\text{diag}}\, p_{\text{ref}}}{c},
$$

a dimensionless **cavitation pressure** `\bar p_{cav} = \alpha p_{cav}`, and a solid-to-fluid **conductivity ratio** `k_r = k_{\text{solid}}/k`. Setting `C_e = 0`, `\bar p_{cav} \to -\infty`, and `k_r \to \infty` (isothermal walls) recovers the base-paper equations exactly.

---

## 4. Solution Algorithm (Staggered TEHD Coupling)

The four physics are solved in a segregated outer loop; each sub-problem uses the latest available fields:

1. **Initialise** rigid film `h = c(1 − ε cos θ)`, isoviscous `m = m_0`, `T = T_0`, `δ_e = 0`, `Θ = 1`.
2. **Hydrodynamics + cavitation.** With current `h`, `m`, solve the Elrod–Adams conservation equation (§2.4) by finite volumes, enforcing the complementarity conditions (e.g. by a Fischer–Burmeister / PJacobi switch sweep) to obtain `p` and `Θ`.
3. **Elastic deformation.** Update `δ_e = C p`; apply under-relaxation `h ← (1−λ)h_old + λ[c(1 − ε cos θ) + δ_e + δ_T]`.
4. **Energy + conjugate conduction.** With current `p`, `u`, solve the film energy equation and solid conduction (§2.5) for `T`, hence `T_m`.
5. **Rheology update.** Recompute `m = m_0 exp[α p − β(T_m − T_0)]` and the thermal clearance `δ_T`.
6. **Convergence check.** Repeat 2–5 until the relative changes in `p`, `T_m`, `δ_e`, and `Θ` all fall below tolerance (typically 1e−5). Under-relaxation of pressure, film, and temperature stabilises the strongly coupled iteration.
7. **Post-process** load, attitude angle, friction, power loss, leakage, minimum film thickness, maximum pressure and temperature.

The δ-profile closed forms of [1] are evaluated inside step 2 to obtain the pressure-flow coefficients `Φ` without a nested cross-film pressure iteration, which is the computational economy inherited from the base model.

---

## 5. Verification and Validation Plan

- **Limiting-case recovery.** With `C_e = 0` and `\bar p_{cav} → −∞`, reproduce the pressure, temperature, and load curves of [1] (their Figs. 3–10, Table 1) to within discretisation error. This is the primary code-verification check.
- **Newtonian cavitation benchmark.** With `n = 1` and elasticity off, compare the rupture/reformation boundaries and load against classical mass-conserving solutions and experimental cavitation extents.
- **EHD benchmark.** With isoviscous, iso-thermal settings, compare the pressure-peak reduction and film-thickness increase against established elasto-hydrodynamic journal-bearing results for compliant liners.
- **Grid independence** in `θ` and `z`, and sensitivity to the compliance-matrix resolution.
- **Experimental comparison** of metal temperature and minimum film thickness against instrumented-bearing data where available, following the comparison strategy of [1].

---

## 6. Anticipated Results and Discussion

Relative to the rigid, full-film THD baseline of [1], the TEHD coupling is expected to produce the following physically consistent trends.

**Pressure field.** Elastic compliance redistributes the load: the sharp pressure peak near minimum film thickness is reduced in magnitude and broadened circumferentially, because surface deflection locally enlarges the gap and relieves the peak. Mass-conserving cavitation clips the divergent-region sub-ambient loop at `p_cav`, removing the non-physical negative pressures that the base full-film model admits and fixing well-defined rupture and reformation boundaries. The net pressure field is non-negative and smoother.

**Temperature field.** Because viscous dissipation scales with `m |∂u/∂y|^{n+1}`, the highest temperatures remain localised near minimum film thickness. Conjugate conduction spreads heat into the metal, lowering peak film temperature relative to an adiabatic assumption but raising it relative to the isothermal-wall idealisation. In the cavitated zone, scaling dissipation by `Θ` reduces predicted heating, correcting the over-prediction implicit in a full-film energy balance. The thermo-viscous thinning (via `β`) and the piezo-viscous stiffening (via `α`) partially offset one another, as in [1].

**Effect of power-law index `n`.** Consistent with the base paper, increasing `n` (toward dilatant behaviour) is expected to raise pressure and temperature for fixed ε; the TEHD elastic feedback is expected to moderate the pressure rise more strongly for shear-thickening fluids, where peaks are highest and deflection largest. Recent two-lobe power-law results similarly report that shear-thickening lubricants outperform pseudo-plastic ones, especially at higher geometric asymmetry/preload [5].

**Effect of eccentricity `ε`.** The base paper reports that pressure decreases with ε for dilatant and pseudo-plastic fluids but the trend reverses for Newtonian fluid; and that load capacity increases with both `n` and ε. The TEHD model is expected to preserve these qualitative trends while **reducing the absolute load and peak pressure** at high ε (where deformation and cavitation extent are largest), narrowing the gap between the rigid prediction and measured values.

**Load, friction, and leakage.** Load capacity computed from the bounded pressure field will generally be lower than the rigid, full-film value, with the reduction growing with `C_e` and ε. Mass-conserving cavitation yields physically correct side-leakage and friction in the ruptured zone, which a truncated-pressure model mispredicts.

**Practical significance.** The TEHD model is directly relevant to compliant-liner bearings (polymer, rubber, white-metal), bio- and nano-lubricated bearings whose rheology is strongly non-Newtonian and temperature-sensitive, and high-specific-load applications where rigid full-film predictions are known to be optimistic. By retaining the δ-profile semi-analytical core, the extension adds realism without discarding the computational efficiency of the base method.

---

## 7. Conclusion

A thermo-elasto-hydrodynamic extension of the power-law δ-profile THD journal-bearing model of [1] has been formulated. The extension (i) couples hydrodynamic pressure to elastic surface deflection through a compliance-matrix film-thickness equation, (ii) replaces the full-film assumption with a mass-conserving JFO/Elrod–Adams cavitation treatment that guarantees non-negative pressure and conserves mass across rupture and reformation, and (iii) couples a convective film energy equation with conjugate conduction in the solids, feeding a thermo-piezo-viscous consistency law. A staggered iterative algorithm solves the four coupled sub-problems, and the formulation reduces exactly to the base THD model in the rigid, full-film, isothermal-wall limit. The model is expected to predict lower, broader pressure peaks, physically bounded pressures with well-defined cavitation boundaries, localised peak temperatures moderated by conduction, and a load capacity that is reduced relative to the rigid prediction by an amount that grows with the elasticity number and eccentricity ratio. Planned verification against the base-paper limiting case and established EHD/cavitation benchmarks, followed by experimental validation of metal temperature and minimum film thickness, will establish the model's accuracy.

---

## Nomenclature

| Symbol | Meaning |
|---|---|
| `c` | radial clearance |
| `C`, `C_e` | compliance (influence-coefficient) matrix; dimensionless elasticity number |
| `e`, `ε` | eccentricity; eccentricity ratio `e/c` |
| `h` | film thickness |
| `k`, `k_r` | lubricant thermal conductivity; solid-to-fluid conductivity ratio |
| `L` | bearing axial length |
| `m`, `m_0`, `n` | power-law consistency; reference consistency; power-law index |
| `p`, `p_cav` | film pressure; cavitation pressure |
| `R` | journal radius |
| `T`, `T_m`, `T_0` | temperature; mean film temperature; reference temperature |
| `u`, `w` | circumferential, axial film velocity |
| `U = Rω` | journal surface speed |
| `W`, `φ` | load capacity; attitude angle |
| `x = Rθ`, `y`, `z` | circumferential, cross-film, axial coordinates |
| `α`, `β` | piezo-viscous, thermo-viscous coefficients |
| `δ`, `δ*` | zero-shear (delta-profile) location; linearised delta |
| `δ_e`, `δ_T` | elastic deflection; thermal-expansion clearance change |
| `Θ`, `g` | fractional film content; Elrod–Adams switch function |
| `Φ_x`, `Φ_z` | power-law pressure-flow coefficients |
| `ρ`, `c_p` | lubricant density, specific heat |
| `τ` | shear stress |

---

## References

[1] P. S. Sekhar, Dinesh K, P. Patil, A. Dumka, R. Singh, A. S. Kang, A. D. Oza, M. Kumar, A. Kumar. "Temperature analysis of hydrodynamic journal bearing lubrication with a moving journal and a fixed bearing." *Advances in Materials and Processing Technologies*, 2024, 10(4):3517–3530. doi:10.1080/2374068X.2023.2249720

[2] "Thermo-hydrodynamic analysis of journal bearings operating with non-Newtonian oils" (modified power-law Reynolds equation coupled with the energy equation, solved by the finite-volume method), *J. Braz. Soc. Mech. Sci. Eng.*, 2024. doi:10.1007/s40430-024-04804-2

[3] "Thermo-elasto-hydrodynamic (TEHD) study of a journal bearing lubricated with biodegradable nanolubricant" (power-law model), *J. Braz. Soc. Mech. Sci. Eng.*, 2021. doi:10.1007/s40430-021-02801-3

[4] "Thermoelasto-hydrodynamic analysis of nano-lubricated journal bearings using CFD with two-way fluid–structure interaction considering cavitation," *Arab. J. Sci. Eng.*, 2022. doi:10.1007/s13369-022-07024-9

[5] "Steady-state hydrodynamic characteristics of preloaded two-lobe journal bearings under power-law non-Newtonian lubrication," *J. Vib. Eng. Technol.*, 2026. doi:10.1007/s42417-026-02459-y

[6] G. Bayada, M. Chambat. Mass-conserving cavitation models (JFO theory); D. Dowson, C. M. Taylor, "Cavitation in bearings," *Annu. Rev. Fluid Mech.*, 1979. (Foundational cavitation references.)

[7] H. G. Elrod. "A cavitation algorithm." *ASME J. Lubrication Technology*, 1981, 103:350–354. (Elrod–Adams switch-function implementation of JFO cavitation.)

*Note: references [2]–[5] were located via literature search and are cited by title/DOI; the quoted content of [1] is drawn from the manuscript provided. Secondary references [6]–[7] are standard foundational works for the cavitation formulation. Content was rephrased for compliance with licensing restrictions.*
