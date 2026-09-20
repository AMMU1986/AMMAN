# A New Research Problem — Combining the Two Casson MHD Squeezing-Flow Papers

**Prepared as a research-gap / problem-formulation note.**

This note fuses the two papers below into a single, more general physical model and identifies a **genuinely new problem** that neither paper solves and that the recent literature has not yet reported for this specific squeezing-channel geometry.

- **Paper A** — *MHD Squeezed Radiative Flow of Casson Hybrid Nanofluid Between Parallel Plates with Joule Heating*, Bhaskar, Sharma & Bhaskar, *Int. J. Appl. Comput. Math* **10**:80 (2024). [DOI](https://doi.org/10.1007/s40819-024-01720-w)
- **Paper B** — *Unsteady MHD squeezing viscous Casson fluid flow in upright channel with cross-diffusion and thermal radiactive effects*, Bhaskar & Sharma, *Indian J. Phys.* **95**(7):1453–1467 (2021). [DOI](https://doi.org/10.1007/s12648-020-01805-4)

---

## 1. What each paper already does (and does not)

| Physics / feature | Paper A (2024) | Paper B (2021) |
|---|---|---|
| Geometry | Unsteady squeezing between parallel plates; **stretchable + permeable** lower plate, squeezing upper plate | Unsteady squeezing porous channel; stretching lower plate, squeezing upper plate |
| Fluid | **Casson Cu–Al₂O₃/water hybrid nanofluid** | Viscous (single-phase) **Casson** fluid |
| Porous medium | ✔ | ✔ |
| MHD | ✔ | ✔ |
| Thermal radiation (Rosseland) | ✔ | ✔ |
| Joule heating | ✔ | ✘ (not included) |
| Heat source/sink | ✔ | ✘ |
| Viscous dissipation | ✔ | ✔ |
| Suction/injection | ✔ | ✘ |
| **Species / concentration field** | ✘ (energy only) | ✔ |
| **Cross-diffusion (Soret / Dufour)** | ✘ | ✔ |
| **Chemical reaction** | ✘ | ✔ (first order, constant rate) |
| **Activation energy (Arrhenius)** | ✘ | ✘ |
| **Double stratification (thermal + solutal)** | ✘ | ✔ |
| **Triple slip (velocity/thermal/solutal)** | ✘ | ✔ |
| **Entropy generation / Bejan number** | ✘ | ✘ |
| Solver | OHAM | OHAM (BVPh 2.0) |

**Key observation.** The two papers are complementary halves:

- Paper A has the **rich thermo-magnetic transport of a *hybrid nanofluid*** (Joule heating, heat source, suction/injection) but **no mass transfer at all** — there is no concentration equation.
- Paper B has the full **heat-*and*-mass transport machinery** (Soret/Dufour cross-diffusion, chemical reaction, double stratification, triple slip) but only for a **plain viscous Casson fluid** — no nanoparticles, no Joule heating.

Neither paper contains a **second-law (entropy generation) analysis**, and neither includes **Arrhenius activation energy**.

---

## 2. The research gap (verified against recent literature)

A scan of 2022–2026 work shows the individual ingredients are well studied, but always in *other* geometries or with *subsets* of the physics:

- Entropy generation in squeezing flow exists mainly for **rotating** plates or **plain Casson nanofluid**, not the Cu–Al₂O₃ Casson **hybrid** stretch/squeeze channel — e.g. *Entropy Generation and Statistical Analysis of MHD Hybrid Nanofluid Unsteady Squeezing Flow between Two Parallel Rotating Plates with Activation Energy* ([MDPI, Nanomaterials 2022](https://www.mdpi.com/2079-4991/12/14/2381)); *Entropy Generation Optimization in Squeezing MHD Flow of Casson Nanofluid with Viscous Dissipation and Joule Heating* ([MDPI, Entropy 2019](https://www.mdpi.com/1099-4300/21/8/747)).
- Cu–Al₂O₃ Casson hybrid with chemical reaction / slip / porous medium has been done on **stretching sheets**, e.g. *Heat and mass transfer analysis of chemically reacted Cu/Al₂O₃ Casson hybrid nanofluid via porous medium under MHD and slip conditions* ([Nanotechnology Reviews 2026](https://www.degruyterbrill.com/document/doi/10.1515/ntrev-2025-0283/html)); *Entropy Generation of Cu–Al₂O₃/Water Flow ... through a Porous Stretching Sheet with Slip, Joule Heating and Chemical Reaction* ([MDPI, MCA 2023](https://www.mdpi.com/2297-8747/28/1/18)).
- Cattaneo–Christov / activation energy / cross-diffusion for Casson hybrid nanofluids appears mostly over **disks, cones, cylinders and stretching sheets**, not the squeezing channel — e.g. *Bioconvection and entropy generation in Cattaneo–Christov Casson ternary hybrid nanofluid over a Riga plate with activation energy* ([Springer 2026](https://link.springer.com/article/10.1007/s42452-026-09225-5)); *FD and ANN modeling of cross-diffusive free convection in Casson MoS₂–MXene/PAW hybrid nanofluid over a vertical cone* ([Springer 2026](https://link.springer.com/article/10.1186/s40712-026-00536-4)).

> *Content above was rephrased/summarized for compliance with licensing restrictions.*

**Gap statement.** *No single study unifies the Cu–Al₂O₃/water **Casson hybrid nanofluid** in the **stretchable-lower-plate / squeezing-upper-plate porous channel** (Paper A geometry and thermal physics: MHD + Joule heating + radiation + heat source + viscous dissipation + suction/injection) **together with** a full species field carrying **Soret–Dufour cross-diffusion + Arrhenius-activation-energy chemical reaction + triple slip + double stratification** (Paper B machinery), analysed through a **second-law entropy-generation / Bejan-number** framework.*

---

## 3. Proposed new problem (recommended title)

> **"Entropy generation in the unsteady MHD squeezing flow of a Casson Cu–Al₂O₃/water hybrid nanofluid through a porous channel with Arrhenius activation energy, Soret–Dufour cross-diffusion, multiple slip and double stratification."**

This is the *superset* of both papers plus two new mechanisms (activation energy + irreversibility analysis). Both original papers become **validation limiting cases** (Paper A ⇒ drop the concentration equation, slip, stratification, cross-diffusion; Paper B ⇒ set nanoparticle volume fractions φ₁ = φ₂ = 0 and remove Joule heating), which is a strong credibility feature.

### 3.1 Governing equations (2-D, unsteady)

Continuity:

$$\frac{\partial u}{\partial x}+\frac{\partial v}{\partial y}=0$$

Momentum (Casson + hybrid + MHD + Darcy porous drag), keeping Paper A's `hnf` property model:

$$\frac{\partial u}{\partial t}+u\frac{\partial u}{\partial x}+v\frac{\partial u}{\partial y}
=-\frac{1}{\rho_{hnf}}\frac{\partial p}{\partial x}
+\frac{\mu_{hnf}}{\rho_{hnf}}\Big(1+\tfrac{1}{\beta^{*}}\Big)\Big(\tfrac{\partial^2u}{\partial x^2}+\tfrac{\partial^2u}{\partial y^2}\Big)
-\frac{\sigma_{hnf}}{\rho_{hnf}}B(t)^2u
-\frac{\mu_{hnf}}{\rho_{hnf}}\frac{1}{K_P^{*}}\Big(1+\tfrac{1}{\beta^{*}}\Big)u$$

Energy (radiation + Joule heating + heat source + viscous dissipation + **Dufour** cross-diffusion — *new coupling for the hybrid case*):

$$\big(\rho C_p\big)_{hnf}\!\Big(\tfrac{\partial T}{\partial t}+u\tfrac{\partial T}{\partial x}+v\tfrac{\partial T}{\partial y}\Big)
=\kappa_{hnf}\tfrac{\partial^2T}{\partial y^2}-\tfrac{\partial q_r}{\partial y}
+\sigma_{hnf}B(t)^2u^2+Q_0(T-T_1)
+\mu_{hnf}\Big(1+\tfrac{1}{\beta^{*}}\Big)\Phi
+\frac{\rho_{hnf}D_m K_T}{C_s}\tfrac{\partial^2C}{\partial y^2}$$

Concentration (**new to the hybrid problem**: Soret + chemical reaction with **Arrhenius activation energy**):

$$\frac{\partial C}{\partial t}+u\frac{\partial C}{\partial x}+v\frac{\partial C}{\partial y}
=D_m\frac{\partial^2C}{\partial y^2}
+\frac{D_m K_T}{T_m}\frac{\partial^2T}{\partial y^2}
-k_r^2\Big(\frac{T}{T_1}\Big)^{n}\exp\!\Big(-\frac{E_a}{k_BT}\Big)(C-C_1)$$

where the last term is the **Arrhenius-modified reaction** (this is the mechanism absent from *both* papers).

Rosseland radiation (as in both papers): $q_r=-\dfrac{4\sigma^{*}}{3k^{*}}\dfrac{\partial T^4}{\partial y}$, $T^4\approx4T_0^3T-3T_0^4$.

### 3.2 Boundary conditions — triple slip + double stratification (from Paper B, new for the hybrid fluid)

At the lower plate $y=0$:

$$u=\lambda u_w+L\,\frac{\partial u}{\partial y},\quad v=v_w,\quad
T=T_w+K_{11}\frac{\partial T}{\partial y},\quad
C=C_w+K_{12}\frac{\partial C}{\partial y}$$

At the upper (squeezing) plate $y=h(t)$:

$$u=0,\quad v=\frac{dh}{dt},\quad T=T_h,\quad C=C_h$$

with linearly stratified plate temperature/concentration $T_w=T_0+\ldots$, $T_h=T_0+\ldots$, etc. (Paper B, Eq. 7).

### 3.3 Similarity reduction

Use Paper A / B transforms $\eta=\sqrt{\tfrac{b}{\nu_f(1-\alpha t)}}\,y$, $u=\tfrac{bx}{1-\alpha t}f'(\eta)$, $\theta$, and add $\phi(\eta)=\dfrac{C-C_h}{C_w-C_0}$. The system reduces to coupled ODEs of the schematic form:

$$\Big(\tfrac{A_1}{A_2}\Big)\Big(1+\tfrac1{\beta^{*}}\Big)f^{iv}+ff'''-f'f''-\tfrac{Sq}{2}(3f''+\eta f''')-\Big(\tfrac{A_3}{A_2}\Big)Mf''-\Big(\tfrac{A_1}{A_2}\Big)\Big(1+\tfrac1{\beta^{*}}\Big)K_Pf''=0$$

$$\Big(A_4+\tfrac43Rd\Big)\theta''-\Pr Hs\,\theta-A_5\Big(\tfrac{Sq}{2}\eta-f\Big)\Pr\theta'+A_1\Big(1+\tfrac1{\beta^{*}}\Big)Ec\Pr[\,\cdots\,]+A_3Ec\Pr M f'^{2}+\Pr Df\,\phi''=0$$

$$\phi''+Sc\Big(f\phi'-f'\phi\Big)-Sc\,\tfrac{Sq}{2}\big(\eta\phi'+\varepsilon_2 f'\big)-Sc\,K(1+\delta_T\theta)^{n}e^{-E/(1+\delta_T\theta)}\phi+Sc\,Sr\,\theta''=0$$

(the θ″ and φ″ cross-terms are the Dufour/Soret couplings; the exponential term is activation energy).

### 3.4 New quantity — entropy generation (second law)

$$S_{gen}=\underbrace{\frac{\kappa_{hnf}}{T_0^2}\Big(1+\tfrac43Rd\Big)\Big(\tfrac{\partial T}{\partial y}\Big)^2}_{\text{heat transfer}}
+\underbrace{\frac{\mu_{hnf}}{T_0}\Big(1+\tfrac1{\beta^{*}}\Big)\Big(\tfrac{\partial u}{\partial y}\Big)^2+\frac{\mu_{hnf}}{T_0K_P^{*}}u^2+\frac{\sigma_{hnf}B^2}{T_0}u^2}_{\text{friction + porous + Joule}}
+\underbrace{\frac{R D_m}{C_0}\Big(\tfrac{\partial C}{\partial y}\Big)^2+\frac{R D_m}{T_0}\Big(\tfrac{\partial T}{\partial y}\Big)\Big(\tfrac{\partial C}{\partial y}\Big)}_{\text{diffusive}}$$

Non-dimensionalise to $N_G$ and report the **Bejan number** $Be=\dfrac{\text{thermal+diffusive irreversibility}}{N_G}$. This entire block is new relative to both papers.

### 3.5 Solution method

Keep **OHAM** (the group's signature method in both papers) for continuity and cross-validation; optionally cross-check with `bvp4c`/spectral collocation. **Validate** by recovering:
- Paper A tables (f″(0), f″(1), −θ′(0)) when φ (concentration), slip, stratification, Soret/Dufour, activation energy are switched off;
- Paper B when φ₁ = φ₂ = 0 (base viscous Casson fluid) and Joule heating removed.

---

## 4. Alternative / adjustable novelty knobs

If reviewers judge the superset above "too incremental," any **one** of these makes a cleaner standalone contribution on the same geometry:

1. **Cattaneo–Christov double diffusion** — replace classical Fourier/Fick with thermal + solutal relaxation times (non-Fourier). Rarely done for the *squeezing hybrid* channel.
2. **Ternary / tri-hybrid nanofluid** (e.g. Cu–Al₂O₃–TiO₂/water or Cu–Al₂O₃–GO) — extend the property model to three nanoparticles and compare nanofluid vs hybrid vs ternary in the same squeezing channel.
3. **Shape-factor study** (spherical / platelet / cylindrical / lamina nanoparticles) coupled with entropy optimisation.
4. **Response-surface methodology (RSM) / sensitivity analysis** on Nusselt & Sherwood numbers — adds a statistical-optimisation dimension neither paper has.

**Recommended primary target:** Section 3 (superset + activation energy + entropy). **Highest-novelty single-add:** Section 4.1 (Cattaneo–Christov double diffusion).

---

## 5. Why this is publishable and defensible

- **Clear gap:** unifies two of the authors' own complementary models and adds two mechanisms (activation energy + irreversibility) absent from both.
- **Built-in validation:** both prior papers are exact limiting cases, giving immediate benchmark tables.
- **Application pull:** hybrid-nanofluid squeezing channels model lubrication/compression systems, biomedical squeeze films and heat-exchanger cores; entropy minimisation ties directly to energy-efficiency design.
- **Method continuity:** OHAM reuse means the existing solver/codebase can be extended rather than rebuilt.
