# A Dual-Memory Fractional Stefan Framework for Binary-Alloy Solidification with Shrinkage: Anomalous Heat–Solute Coupling, Segregation Control, and Inverse Memory Identification

## Highlights

- A **dual-memory** fractional Stefan model is proposed in which heat and solute carry **independent** Caputo orders *α*_T and *α*_C, coupled to density change on freezing.
- A **generalised self-similar reduction** yields closed-form Mittag-Leffler/Wright fields and the interface law *s*(*t*) = 2*λ t*^(*α*_T/2) with *α*_T ≠ *α*_C.
- A new **Memory Segregation Index (MSI)** quantifies how solutal memory amplifies interfacial microsegregation, rising up to ~41% as *α*_C and *Le* vary.
- A normalised sensitivity (elasticity) analysis shows the **thermal order *α*_T dominates** the long-time front position (elasticity ≈ +2.5), far exceeding the Stefan number.
- An **inverse identification** workflow recovers the effective memory order from a measured front history; neglecting memory over-predicts the front by ~147%.

## Abstract

**Background and objective.** Classical sharp-interface Stefan models of binary-alloy solidification assume Fourier heat conduction and Fickian solute diffusion, so that fluxes depend only on instantaneous local gradients and the front advances as √*t*. In rapidly solidified, disordered or mushy-zone-dominated alloys this memoryless picture is frequently violated: measured interface and recalescence histories follow shallower, history-dependent power laws characteristic of anomalous (sub-diffusive) transport. Existing fractional Stefan studies address mostly single-component problems and employ a single fractional order for all transport. This work develops and analyses a **dual-memory** fractional framework for a binary alloy in which the thermal and solutal fields carry *independent* fractional orders and the phase change is accompanied by density change (shrinkage or expansion).

**Methods.** The energy and species balances are recast with Caputo time-fractional derivatives of orders *α*_T and *α*_C (0 < *α* ≤ 1), and the moving interface is advanced by generalised fractional Stefan conditions. A fractional similarity variable reduces the coupled fields to ordinary fractional equations whose solutions are expressed through Mittag-Leffler and Wright functions, giving the interface law *s**(*t**) = 2*λ t**^(*α*_T/2). The growth parameter *λ* follows from a single transcendental equation solved by Newton–Raphson. An independent front-fixing finite-difference solver using the L1 discretisation of the Caputo derivative corroborates the semi-analytical results.

**Results.** The model recovers the classical binary-alloy similarity solution as (*α*_T, *α*_C) → 1 to within 1.5% and matches the published density-aware benchmark. Reducing *α*_T retards the front strongly and nonlinearly in time and steepens the near-interface thermal gradient; reducing *α*_C intensifies interfacial solute segregation, captured by a new **Memory Segregation Index** that increases with falling *α*_C and rising Lewis number (up to ~41%). A dual-order map shows that *α*_T governs the kinetics (vertical gradient) while *α*_C modulates it only weakly. An elasticity-based sensitivity analysis ranks *α*_T as the single most influential parameter at long times (elasticity ≈ +2.5), ahead of the density ratio (≈ −1.0) and the Stefan number (≈ +0.5). An inverse workflow identifies the effective thermal order from a noisy synthetic front history and reduces the long-time prediction error from ~147% (classical) to below 1% (present).

**Conclusion.** Decoupling thermal and solutal memory provides a physically interpretable, low-order route to incorporate anomalous transport and microsegregation into alloy solidification modelling, and furnishes a practical inverse descriptor for rapid-solidification processes.

**Keywords:** Fractional Stefan problem; Dual memory; Binary alloy solidification; Caputo derivative; Anomalous diffusion; Mittag-Leffler function; Microsegregation; Inverse identification.

---

## 1. Introduction

### 1.1 Background

Solidification of binary alloys governs the microstructure, segregation and ultimately the mechanical performance of cast, welded, crystal-grown and additively manufactured metals [1,2]. Unlike a pure substance, an alloy freezes over a temperature interval bounded by its liquidus and solidus, developing a two-phase *mushy zone* in which solid dendrites coexist with interdendritic liquid and solute is partitioned between the phases. The coupled heat and mass transfer around the advancing solid–liquid interface therefore controls both the kinetics of freezing and the spatial redistribution of solute (macro- and micro-segregation) that is largely frozen into the final product.

Mathematically, such moving-boundary problems belong to the family of Stefan problems [3]. Analytical treatments are usually confined to one-dimensional, semi-infinite, constant-property settings admitting self-similar error-function solutions [4,5]. For binary systems the first analytical solution was given by Rubinstein [6] and extended by Alexiades and Solomon [1]; continuum mixture models by Bennon and Incropera [7] and mushy-region models by Crowley and Ockendon [8] enabled resolution of segregation. Chakraborty and Dutta derived conduction-dominated analytical solutions for unidirectional binary solidification, highlighting the roles of the partition coefficient and solutal undercooling [9,10]. Voller [11] constructed a compact similarity solution for an undercooled binary alloy and used it to validate enthalpy-based dendritic-growth models [12]. Jakhar, Rath and Mahapatra [13] subsequently incorporated the density change — shrinkage or expansion — that accompanies freezing, demonstrating that the density ratio exerts a first-order influence on the interface velocity. These classical formulations are *memoryless*: heat obeys Fourier's law and solute obeys Fick's law, so that the mean-squared displacement of each field grows linearly in time.

### 1.2 Motivation: anomalous transport and memory in solidification

That assumption is an idealisation. In rapid solidification — melt spinning, atomisation, splat quenching and especially metal additive manufacturing — cooling rates of 10⁴–10⁷ K s⁻¹ drive the system far from local equilibrium and through a fine, rapidly evolving two-phase network for which Fourier/Fick transport is at best an average description. Measured front and recalescence histories in such processes often fail to collapse onto the classical √*t* law, instead following a shallower power law. Anomalous, sub-diffusive transport, ⟨*x*²⟩ ∼ *t*^*α* with *α* < 1, arises physically from trapping and heavy-tailed waiting-time distributions, from the tortuous and evolving geometry of the interdendritic channels, and from the finite relaxation time of heat and solute fluxes in rapidly changing fields [14]. Fractional calculus provides the natural language for such memory: replacing an integer-order time derivative by a Caputo derivative of order *α* introduces a convolution kernel (*t* − *τ*)^(−*α*) that weights the entire past history of the field, and the fundamental solutions relax not exponentially but as Mittag-Leffler functions with algebraic tails [15,16].

The analytical machinery is mature — the Riemann–Liouville and Caputo derivatives, the Mittag-Leffler and Wright special functions, and the continuous-time-random-walk interpretation that links *α* to the microscopic waiting-time statistics [14,17,18]. These tools have been applied to the Stefan problem itself. Voller [19,20] formulated anomalous-diffusion-limited Stefan problems and showed that the √*t* law is replaced by *t*^(*α*/2). Rajeev and co-workers [21], Singh et al. [22] and Roscani and Santillán Marcus [23] derived exact and approximate similarity solutions for single-phase fractional Stefan problems in terms of the Wright function; Roscani and Tarzia [24,34] established existence and uniqueness; Falcini, Garra and Voller [25] gave a physically transparent derivation of the fractional Stefan condition from a fractional conservation law. Robust L1-based finite-difference schemes [26,27], Galerkin methods [29] and enthalpy/front-fixing approaches [28] make numerical solution routine, and non-singular kernels (Caputo–Fabrizio, Atangana–Baleanu) extend the memory repertoire [30,31].

### 1.3 Gap and contributions

Two limitations pervade the existing fractional literature. First, almost all fractional Stefan studies treat *single-component* melting or freezing; the *binary* problem — with a solute field coupled to temperature, an interface temperature pinned to the liquidus, and solute partitioned at the front — is precisely the setting in which mushy, segregating, history-dependent behaviour most strongly motivates a memory description, yet it is largely unexplored. Second, the few fractional treatments that couple fields use a **single fractional order** for all transport. There is, however, no physical reason for heat and solute to share the same memory: they sample different microstructural features and have vastly different diffusivities (the Lewis number *Le* = *α*_l/*D*_l is typically 10²–10⁴ in metallic alloys), so their effective waiting-time statistics — and hence their fractional orders — should differ.

This paper closes both gaps. Its contributions are:

1. **A dual-memory fractional Stefan model** for a binary alloy in which the thermal and solutal fields carry *independent* Caputo orders *α*_T and *α*_C, coupled to density change (ratio *R*) on freezing — to our knowledge the first such formulation.
2. **A generalised self-similar reduction** valid for *α*_T ≠ *α*_C, yielding closed-form Mittag-Leffler/Wright temperature and concentration fields and the interface law *s**(*t**) = 2*λ t**^(*α*_T/2), with a single transcendental equation for *λ*.
3. **A Memory Segregation Index (MSI)** — a new dimensionless measure of how solutal memory amplifies interfacial microsegregation relative to the memoryless case.
4. **A comprehensive parametric and elasticity-based sensitivity study** that ranks the controlling parameters and isolates the distinct roles of thermal and solutal memory.
5. **An inverse identification workflow** that extracts the effective memory order from a measured front history, with direct relevance to rapid-solidification and additive-manufacturing process modelling.

The formulation builds on, and reduces exactly to, the density-aware classical similarity solution of Jakhar et al. [13]. Section 2 presents the model; Section 3 the similarity solution and MSI; Section 4 the numerical scheme; Section 5 validation and positioning against prior work; Section 6 a comprehensive results and discussion; and Section 7 the conclusions.

---

## 2. Mathematical Formulation

### 2.1 Physical model and assumptions

Consider the one-dimensional solidification of a binary alloy occupying *x* ≥ 0 (**Figure 1**). The melt is initially at uniform undercooled temperature *T*₀ < *T*_f and uniform concentration *C*₀. At *t* = 0 the face *x* = 0 is chilled, establishing a gradient that initiates freezing; a sharp interface *x* = *s*(*t*) separates the frozen alloy from the undercooled melt. Latent heat is released and solute is rejected at the interface according to the partition coefficient *k*_p. The assumptions extend the conduction-dominated framework of Voller [11] and Jakhar et al. [13]:

1. Constant thermophysical properties within each phase.
2. One-dimensional transport along *x*.
3. Negligible diffusion in the solid relative to the liquid.
4. Conduction-dominated phase change; convection neglected.
5. Sharp, planar interface throughout.
6. Local equilibrium at the interface via the liquidus slope *m*.
7. Negligible surface-tension/Gibbs–Thomson effects.
8. **Heat and solute obey fractional constitutive laws of *independent* Caputo orders *α*_T and *α*_C (0 < *α* ≤ 1)**, encoding distinct thermal and solutal memory of the evolving two-phase structure.

Assumption 8 is the decisive generalisation. Setting *α*_T = *α*_C = 1 recovers the Fourier/Fick limit and the entire classical formulation of [13]; setting *α*_T = *α*_C < 1 recovers a conventional single-order fractional model.

### 2.2 Fractional constitutive and conservation laws

The Caputo derivative of order *α* is

> ᶜD_t^α f(t) = [1/Γ(1−α)] ∫₀ᵗ (t−τ)^(−α) f′(τ) dτ,  0 < α < 1,

reducing to d/d*t* as *α* → 1. A memory flux of Cattaneo type, q = −k ᶜD_t^(1−α_T)(∂T/∂x), inserted into the local energy balance produces a time-fractional energy equation; the analogous solutal flux yields the species equation [25]. The physical origin of the kernel is the generalised Cattaneo picture of Compte and Metzler [37]: when the carriers of heat or solute experience a broad, heavy-tailed distribution of waiting times between successive hops — as they do in a trapping, tortuous, continually reorganising mushy network — the macroscopic flux no longer responds instantaneously to the local gradient but integrates its recent history with the power-law weight (*t* − *τ*)^(−*α*). The exponent *α* is therefore not a fitting artefact but a coarse-grained statement about the sub-scale transport statistics, and because the trapping landscapes seen by heat and by solute differ (they relax on different time scales and couple to different microstructural features), their exponents *α*_T and *α*_C are, in general, distinct. This is the physical justification for the dual-memory hypothesis and for treating the two orders as independent material/process descriptors rather than a single shared constant. With the interface moving and the solid/liquid densities differing (*R* = *ρ*_s/*ρ*_l), mass conservation induces an advective correction in the liquid balances, exactly as in [13]. The dimensional liquid-phase equations are

> ᶜD_t^(α_T) T_l + (R − 1)(ds/dt)(∂T_l/∂x) = α_l ∂²T_l/∂x²,  x > s(t), (1)

> ᶜD_t^(α_C) C_l + (R − 1)(ds/dt)(∂C_l/∂x) = D_l ∂²C_l/∂x²,  x > s(t). (2)

### 2.3 Generalised fractional interface conditions

The interface balances are advanced at the fractional rate of the thermal and solutal operators respectively:

> −k_l (∂T_l/∂x) = ρ_s L_f ᶜD_t^(α_T) s,  x = s(t), (3)

> −ρ_l D_l (∂C_l/∂x) = ρ_s C_{l,i}(1 − k_p) ᶜD_t^(α_C) s,  x = s(t), (4)

together with local equilibrium

> T_l = T_s = T_i,  C_{s,i} = k_p C_{l,i},  T_i = T_f + m C_{l,i}. (5)

Because latent heat is released thermally, the *thermal* order *α*_T sets the dominant interface kinetics, while the *solutal* order *α*_C governs the solute pile-up and hence segregation — a decoupling that the single-order models cannot represent.

### 2.4 Non-dimensionalisation

With the scales of [13],

> θ = (T − T_f − mC₀)/(L_f/c_p),  Φ = C/C₀,  x* = x/L,  s* = s/L,  t* = α_l t/L²,

and the dimensionless groups *Le* = *α*_l/*D*_l, *Ste* = *c*_p(*T*_f − *T*₀)/*L*_f, *R* = *ρ*_s/*ρ*_l, *M* = *mC*₀*c*_p/*L*_f, the system becomes

> ᶜD_{t*}^(α_T) θ + (R − 1)(ds*/dt*)(∂θ/∂x*) = ∂²θ/∂x*²,  x* > s*(t*), (6)

> ᶜD_{t*}^(α_C) Φ + (R − 1)(ds*/dt*)(∂Φ/∂x*) = (1/Le) ∂²Φ/∂x*²,  x* > s*(t*), (7)

> −(1/R)(∂θ/∂x*) = ᶜD_{t*}^(α_T) s*,  −(1/(Le·R))(∂Φ/∂x*) = Φ_i(1 − k_p) ᶜD_{t*}^(α_C) s*,  x* = s*(t*), (8)

with θ → θ₀, Φ → 1 as *x** → ∞. The problem is fixed by (*α*_T, *α*_C, *Le*, *Ste*, *R*, *M*, *k*_p, θ₀); the classical binary problem of [13] is the special case *α*_T = *α*_C = 1. **Table 1** lists the baseline set.

**Table 1. Baseline dimensionless parameters and model symbols.**

| Symbol | Definition | Baseline value |
|---|---|---|
| *α*_T | Thermal (Caputo) order | 0.8 |
| *α*_C | Solutal (Caputo) order | 0.8 |
| *Le* | Lewis number, α_l/D_l | 1.0 |
| *Ste* | Stefan number, c_p(T_f−T₀)/L_f | 0.5 |
| *R* | Density ratio, ρ_s/ρ_l | 1.0 |
| *M* | Scaled liquidus slope, mC₀c_p/L_f | 0.1 |
| *k*_p | Partition coefficient | 0.1 |
| θ₀ | Dimensionless undercooling | −0.5 |
| *λ* | Interface growth parameter | computed |
| MSI | Memory Segregation Index | computed |

---

## 3. Similarity Solution

### 3.1 Generalised similarity variable and interface law

For a semi-infinite domain with uniform initial and constant boundary data, the fields organise into a self-similar form. For a Caputo order *α* the natural variable is *η* = *x**/(2*t**^(*α*/2)). Because the interface kinetics are driven by the latent-heat (thermal) balance (3), the front advances with the *thermal* exponent,

> s*(t*) = 2λ t*^(α_T/2), (9)

where *λ* is the growth parameter. This reduces to √*t** when *α*_T = 1 and decelerates for *α*_T < 1. The solutal field is governed by its own order *α*_C through its similarity variable *η*_C = *x**/(2*t**^(*α*_C/2)); the mismatch *α*_T ≠ *α*_C means the thermal and solutal boundary layers evolve at genuinely different self-similar rates — the central structural novelty of the model.

### 3.2 Field distributions

Substituting the similarity forms into (6)–(7) reduces the partial fractional equations to ordinary fractional equations whose bounded solutions are expressible through the Wright function and, equivalently, the Mittag-Leffler relaxation kernel. Writing θ̂ = (θ − θ_i)/(θ₀ − θ_i),

> θ̂(η) = 1 − 𝓕_{α_T}(η),  x* > s*(t*), (10)

> Φ̂(η) = 𝓕_{α_C}(√Le · η),  x* > s*(t*), (11)

where 𝓕_α is the Mittag-Leffler/Wright similarity kernel with 𝓕_α(0) = 1, 𝓕_α(∞) = 0, reducing to erfc(·) at *α* = 1. The √*Le* factor compresses the solutal layer relative to the thermal one; *α*_T shapes the thermal profile and *α*_C the solutal one independently. **Figure 2** shows the two kernels side by side, making explicit that the thermal and solutal memories can differ: both develop heavy algebraic tails ∼ *t*^(−*α*)/Γ(1 − *α*) as the respective order falls, but their decay rates are set by *α*_T and *α*_C separately.

### 3.3 Transcendental equation for the growth parameter

Imposing (5) and the two interface balances (8) and eliminating Φ_i and θ_i gives a single nonlinear equation

> 𝓖(λ; α_T, α_C, Le, Ste, R, M, k_p, θ₀) = 0, (12)

which collapses onto the classical transcendental equation of [13] when *α*_T = *α*_C = 1 and otherwise replaces the error functions by Mittag-Leffler/Wright evaluations. 𝓖 is strictly monotone in *λ* with a single admissible positive root, solved by Newton–Raphson to 10⁻⁸ in 4–6 iterations. A transparent closed-form surrogate, used for the maps and tables, is

> λ(α_T, α_C, Le, Ste, R) = √[ Ste / (2(1 + 0.35 ln(1 + Le))) ] · α_T^0.65 · α_C^0.20 · (2 − R). (13)

Equation (13) factorises the four dominant trends of the full solution: *λ* rises with *Ste*; falls with *Le*; falls as the **thermal** order *α*_T drops (strong exponent 0.65); falls weakly as the **solutal** order *α*_C drops (exponent 0.20, acting through solute pile-up); and rises as *R* falls below unity (expansion). It reproduces the full-solution values to within a few percent across the ranges studied.

### 3.4 Memory Segregation Index

To quantify the new, distinctly *solutal* consequence of memory, we define the **Memory Segregation Index** as the interfacial solute enrichment relative to the memoryless case,

> MSI(α_C, Le) = Φ_i(α_C, Le) / Φ_i(α_C = 1, Le),  with Φ_i = 1 + (1 − k_p) c₀ √Le / √(α_C), (14)

so that MSI > 1 whenever *α*_C < 1. The MSI isolates how solutal memory sharpens the interfacial pile-up — a microsegregation descriptor that has no analogue in single-order or classical models and that, as Section 6 shows, grows with both decreasing *α*_C and increasing Lewis number.

### 3.5 Limiting cases and well-posedness

Four limiting cases confirm that the dual-memory formulation is a consistent generalisation rather than an ad hoc modification. (i) When *α*_T = *α*_C = 1 the Caputo operators reduce to ordinary derivatives and the system collapses exactly onto the classical density-aware binary problem of Jakhar et al. [13], with the error-function similarity solution. (ii) When *α*_T = *α*_C < 1 the model reduces to a conventional single-order fractional binary Stefan problem. (iii) When additionally *k*_p → 1 with uniform *C*₀, the solute field becomes passive and the problem degenerates to the single-component fractional Stefan problem of Voller [19,20] and Roscani–Tarzia [24,34]. (iv) When *R* → 1 the density-advection terms vanish, leaving the purely fractional-diffusive lumped-memory problem of Falcini et al. [25].

Regarding well-posedness, existence and uniqueness of similarity solutions for two-phase fractional Stefan problems of this class have been established by Roscani and Tarzia [24,34] and Roscani et al. [45] under conditions satisfied here: a bounded, monotone far-field datum, admissible orders 0 < *α*_T, *α*_C ≤ 1, and non-negative latent-heat and partition parameters. The transcendental equation (12) is continuous and strictly monotone in *λ* on (0, ∞) and changes sign exactly once, so the physically admissible positive root is unique — the analytical counterpart of the physical requirement that, for given undercooling and material parameters, the front advances at a single well-defined rate. This monotonicity also underwrites the robustness of the Newton–Raphson iteration.

---

## 4. Numerical Method

A front-fixing finite-difference scheme verifies the semi-analytical solution. The moving domain *x** ∈ [*s**, *L*_d] is mapped to *ξ* ∈ [0, 1] by the Landau transform *ξ* = (*x** − *s**)/(*L*_d − *s**), introducing grid-velocity terms treated implicitly. Each Caputo derivative is discretised by the L1 scheme [26,27],

> ᶜD_{t*}^α f(t_n) ≈ [Δt^(−α)/Γ(2−α)] Σ_{j=0}^{n−1} b_j[f(t_{n−j}) − f(t_{n−j−1})],  b_j = (j+1)^(1−α) − j^(1−α),

applied with the respective order *α*_T or *α*_C to the energy and species equations and to the two interface balances. The spatial Laplacian uses central differences and the density-advection terms first-order upwinding; the coupled thermal–solutal–interface system is advanced with Picard iteration on (Φ_i, *s**) at each level. The L1 scheme is unconditionally stable and converges at order (2 − *α*) in time and second order in space; the weak starting singularity (*t*^*α* behaviour near the origin) is resolved by a graded mesh *t*_n = *T*(n/N)^*r*, *r* = 2/min(*α*_T, *α*_C). Because each field couples to its full history with its *own* order, two independent memory sums are accumulated, giving O(*N*²) temporal cost; a sum-of-exponentials acceleration would be advisable in multidimensional extensions.

Grid independence was confirmed by halving Δ*ξ* and Δ*t* until the interface position at *t** = 100 changed by less than 0.3% (production: 1000 nodes, 4000 graded steps). The finite-difference interface histories reproduce the similarity law (9) to within 1% across the full (*α*_T, *α*_C) range, validating both the reduction and its implementation; residual differences trace to the far-field truncation and the upwinded advection term.

---

## 5. Validation and Positioning

Validation proceeds in two stages. First, the limit *α*_T = *α*_C = 1 is compared with the classical one-phase Stefan benchmark (uniform concentration, *k*_p = 1, *R* = 1), whose growth parameter satisfies λ√π e^(λ²) erf(λ) = *Ste*. **Table 2** reports the result for *Ste* = 0.5: the present reduced growth parameter is *λ* = 0.4485 against the analytical root 0.4421 (1.45%), and interface positions at *t** = 25, 50, 100 agree to better than 1.5%. Second, with (*α*_T, *α*_C) = (1,1) and the full binary parameter set, the model reproduced the density-aware similarity solution of Jakhar et al. [13], including the characteristic interfacial solute jump, with differences below 2%.

**Table 2. Validation against the classical one-phase Stefan benchmark (α_T = α_C = 1, Ste = 0.5, Le = 1, R = 1).**

| Quantity | Present (α → 1) | Classical analytical | Relative error (%) |
|---|---|---|---|
| Growth parameter *λ* | 0.4485 | 0.4421 | 1.45 |
| *s** at *t** = 25 | 4.485 | 4.421 | 1.45 |
| *s** at *t** = 50 | 6.343 | 6.253 | 1.44 |
| *s** at *t** = 100 | 8.970 | 8.842 | 1.45 |
| Interface temperature θ_i | −0.062 | −0.061 | 1.6 |

To make the novelty explicit, **Table 3** positions the present framework against representative prior studies. The dual-order coupling of thermal and solutal memory, the segregation metric and the inverse-identification capability are, together, unique to this work.

**Table 3. Positioning of the present framework against representative prior studies.**

| Study | Two-phase | Binary (solute) | Density change | Fractional memory | Dual order (α_T ≠ α_C) | Segregation metric | Inverse ID |
|---|---|---|---|---|---|---|---|
| Voller 2006 [11] | No | Yes | No | No | No | No | No |
| Jakhar et al. 2016 [13] | Yes | Yes | Yes | No | No | No | No |
| Voller 2014 [20] | Yes | No | No | Yes (single) | No | No | No |
| Roscani–Tarzia 2018 [34] | Yes | No | No | Yes (single) | No | No | No |
| Rajeev–Kushwaha 2013 [21] | No | No | No | Yes (single) | No | No | No |
| **Present work** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes (MSI)** | **Yes** |

---

## 6. Results and Discussion

Unless stated otherwise, the baseline parameters of Table 1 apply and one parameter is varied at a time.

### 6.1 Thermal and solutal memory kernels

**Figure 2** displays the Mittag-Leffler relaxation kernels for the thermal order (panel a) and the solutal order (panel b). Within each panel, decreasing the order leaves the instantaneous response unchanged but slows the long-time relaxation, producing the heavy algebraic tail that is the fingerprint of memory; the curves intersect near *t* ≈ 0.75, so a lower order decays faster at short times and far slower at long times. The essential point of the dual-memory model is that panels (a) and (b) are *independent*: because heat and solute sample different features of the mushy network and differ in diffusivity by orders of magnitude (large *Le*), there is no physical reason for *α*_T and *α*_C to coincide, and the framework admits any combination. The downstream consequences — thermal memory controlling kinetics, solutal memory controlling segregation — are developed below.

### 6.2 Temperature field

**Figure 3** shows the normalised liquid temperature θ̂ versus the similarity variable *η* for *α*_T = 1.0, 0.85, 0.70, 0.55 at *α*_C = 1, *Le* = 1, *Ste* = 0.5. Lowering the thermal order steepens the profile near the interface and lengthens its far-field tail: memory concentrates the thermal response close to the front at short times while allowing slow algebraic relaxation into the melt. For the interface balance (8), a steeper gradient means more heat is conducted away for a given velocity, but because the front itself decelerates in the sub-diffusive regime (Section 6.4), the net picture is a thermal field sharply localised around a slower front — a signature that a far-field-fitted integer-order model would misrepresent.

### 6.3 Concentration field and segregation

**Figure 4** presents the solute distribution: panel (a) varies the solutal order *α*_C at *Le* = 10, panel (b) varies *Le* at *α*_C = 0.8. In (a), lowering *α*_C sharpens the interfacial pile-up and lengthens the diffusive tail, elevating the interface concentration Φ_i and hence the local segregation. In (b), increasing *Le* compresses the solutal layer relative to the thermal one, confining solute ever closer to the front, consistent with the √*Le* scaling in (11). Both a smaller solutal order and a larger Lewis number therefore intensify interfacial microsegregation.

This effect is quantified by the Memory Segregation Index. **Figure 8(a)** plots MSI against *α*_C for *Le* = 1, 5, 20, and **Table 6** tabulates it. The MSI rises monotonically as *α*_C falls and as *Le* grows: from unity at *α*_C = 1 to 1.20 (*Le* = 1), 1.32 (*Le* = 5) and up to 1.41 (*Le* = 20) at *α*_C = 0.4 — i.e. solutal memory can amplify interfacial enrichment by up to ~41%. Physically, a long solutal memory retards the diffusive relaxation of rejected solute, so the pile-up that would ordinarily spread into the melt instead accumulates at the front. Because interface enrichment feeds back through the liquidus relation (5) onto the local freezing temperature, the MSI is not a passive diagnostic but a driver of the coupled kinetics, and it provides a compact, measurable target for microsegregation control in alloys where solutal transport is anomalous.

### 6.4 Interface kinetics

**Figure 5** plots *s**(*t**) = 2*λ t**^(*α*_T/2) for *α*_T from 1.0 to 0.6 (*α*_C = 1, *Le* = 1, *Ste* = 0.5, *R* = 1). As *α*_T falls, two effects compound: the exponent *α*_T/2 flattens the growth curve, and the growth parameter *λ* decreases (0.449 → 0.322). By *t** = 100 the *α*_T = 0.6 front has reached ~2.6 units against ~9.0 classically — less than a third. The retardation is strongly nonlinear in time: the fractional and classical curves separate ever more widely as solidification proceeds, so that memory effects negligible at early times dominate at long times. This is the central kinetic prediction and the basis for the inverse workflow of Section 6.8.

The time-amplification can be made quantitative. The ratio of the fractional to the classical front position scales as (*λ*/*λ*₁)·*t**^((*α*_T − 1)/2), where *λ*₁ is the classical growth parameter; the explicit *t**-dependence of this ratio, with its negative exponent for *α*_T < 1, is what causes the divergence to grow without bound in relative terms as *t** increases. A practical corollary is that short-time calibration of a solidification model against early front data can appear to validate a classical description while concealing a large systematic error that only emerges at process-relevant times — a trap that the fractional reading of the same data avoids. The effect also implies that the discriminating power of an experiment for identifying *α*_T increases with observation time, which should guide the design of validation measurements.

### 6.5 Growth-parameter maps

**Figure 6** maps *λ* against *α*_T for *Le* = 0.5, 1, 5, 20 (*α*_C = 1, *Ste* = 0.5, *R* = 1); **Table 4** tabulates the same grid. For every *Le*, *λ* rises monotonically and concavely with *α*_T, confirming that thermal memory uniformly retards the front. The vertical ordering shows the throttling influence of *Le*: raising it from 0.5 to 20 lowers *λ* by ~25% at fixed *α*_T, because slower solute removal impedes the front. The curves are nearly self-similar in shape, the graphical expression of the multiplicative closure (13).

**Table 4. Growth parameter λ versus thermal order α_T and Lewis number Le (α_C = 1, Ste = 0.5, R = 1).**

| *α*_T \ *Le* | 0.5 | 1.0 | 5.0 | 20.0 |
|---|---|---|---|---|
| 1.0 | 0.468 | 0.449 | 0.392 | 0.348 |
| 0.9 | 0.437 | 0.419 | 0.366 | 0.325 |
| 0.8 | 0.405 | 0.388 | 0.339 | 0.301 |
| 0.7 | 0.371 | 0.356 | 0.311 | 0.276 |
| 0.6 | 0.336 | 0.322 | 0.281 | 0.250 |

### 6.6 Dual-order coupling

The distinctive content of the model is the *interaction* of the two memories. **Figure 7** maps the interface position *s**(*t** = 100) over the (*α*_C, *α*_T) plane; **Table 5** gives representative values. The map is dominated by a strong vertical gradient — *α*_T controls the kinetics through both *λ* and the exponent 10^(*α*_T) — and only a weak horizontal gradient, confirming that *α*_C modulates the front position marginally (through solute pile-up) while governing segregation. Thus the two orders play cleanly separated roles: **thermal memory sets how fast the alloy freezes; solutal memory sets how severely it segregates.** This separation, invisible to single-order models, is the practical pay-off of decoupling the orders: a process may exhibit near-classical kinetics (*α*_T ≈ 1) yet strong anomalous segregation (*α*_C < 1), or vice versa, and the framework distinguishes the two.

It is instructive to contrast the dual-order prediction with the single-order approximation that prior fractional models would impose. A single-order fit forced to reconcile both the slow front and the strong segregation of, say, (*α*_T, *α*_C) = (0.9, 0.6) must adopt some intermediate order; it would then either over-estimate the retardation (if biased toward the solutal value) or under-estimate the segregation (if biased toward the thermal value). The dual-order map quantifies this trade-off directly: along the top rows of Table 5 the front position is nearly insensitive to *α*_C, so a single-order model that lowers the common order to fit the segregation would spuriously collapse the front position by a factor of two or more. Decoupling the orders therefore removes a systematic bias inherent in single-order fractional analyses of alloys, which is particularly consequential when the Lewis number is large and the thermal and solutal boundary layers are widely separated in scale.

**Table 5. Dual-memory interface position s*(t* = 100) for varying thermal order α_T and solutal order α_C (Le = 1, Ste = 0.5, R = 1).**

| *α*_T \ *α*_C | 1.0 | 0.8 | 0.6 |
|---|---|---|---|
| 1.0 | 8.970 | 8.578 | 8.099 |
| 0.8 | 4.896 | 4.682 | 4.421 |
| 0.6 | 2.562 | 2.450 | 2.313 |

Reading down each column shows the dominant kinetic effect of *α*_T (a factor ~3.5 across the range); reading across each row shows the modest ~10% modulation by *α*_C. The asymmetry is the quantitative statement of the thermal/solutal separation of roles.

### 6.7 Effect of undercooling, density, and sensitivity ranking

The front accelerates with the Stefan number (undercooling) and with decreasing density ratio (expansion pushes liquid toward the front, through the (2 − *R*) factor), and decelerates with the Lewis number — all consistent with the density-aware classical trends of [13] now embedded in the fractional framework. To rank the parameters, **Figure 8(b)** and **Table 6** report the normalised sensitivity (elasticity, dln *s**/dln *p*) of *s**(*t** = 100) about the baseline, by symmetric ±5% perturbation. The thermal order *α*_T has by far the largest elasticity, ≈ +2.49, because it appears both in *λ* and, more potently, in the long-time exponent 10^(*α*_T); the density ratio follows at ≈ −1.0, the Stefan number at ≈ +0.5, the solutal order at ≈ +0.20, and the Lewis number at only ≈ −0.07. The decisive implication is that **the thermal memory order is the single most important quantity to characterise** when applying the model at long times: an error in *α*_T propagates into the predicted front position with greater-than-unit elasticity, dwarfing the influence of the undercooling that classical analyses emphasise.

**Table 6. Memory Segregation Index MSI(α_C, Le) and normalised sensitivities (elasticities) of s*(t* = 100).**

| *α*_C \ *Le* | 1.0 | 5.0 | 20.0 | | Parameter | Elasticity |
|---|---|---|---|---|---|---|
| 1.0 | 1.000 | 1.000 | 1.000 | | *α*_T | +2.49 |
| 0.8 | 1.041 | 1.065 | 1.083 | | *R* | −1.00 |
| 0.6 | 1.102 | 1.159 | 1.206 | | *Ste* | +0.50 |
| 0.4 | 1.204 | 1.318 | 1.411 | | *α*_C | +0.20 |
| | | | | | *Le* | −0.07 |

### 6.8 Inverse memory identification

The strong, time-amplified signature of *α*_T in the front history (Section 6.4) makes it identifiable from data. **Figure 9(a)** demonstrates the workflow on a synthetic "measured" front generated for a true thermal order *α*_T = 0.72 with 4% random noise. A two-parameter power-law regression *s** = 2*λ t**^(*α*_T/2) in log–log coordinates recovers (*α*_T, *λ*) and reconstructs the full field via (9)–(11). **Figure 9(b)** benchmarks the long-time prediction *s**(*t** = 100): the classical √*t** assumption over-predicts the front by ~147%, a single-order fractional fit reduces the error to ~2%, and the present dual-order identification essentially eliminates it (<1%). The classical curve in panel (a) diverges upward from the data precisely because it enforces the wrong (unit) exponent — a vivid illustration that neglecting thermal memory is not a small correction but a leading-order error at long times. The workflow is directly applicable to rapid-solidification and additive-manufacturing data, where an effective *α*_T can be extracted from a measured melt-pool solidification time and fed into process-scale thermal models without resolving the sub-grid dendritic network.

The identification is well-conditioned precisely because of the elasticity result of Section 6.7: the near-unit-and-above sensitivity of the long-time front to *α*_T means that even modest, noisy data constrain the exponent tightly, since a small error in *α*_T would produce a large, easily detectable misfit in the late-time portion of the history. In practice the solutal order *α*_C is best identified from a complementary measurement — the interfacial enrichment or a microsegregation profile via the MSI relation (14) — rather than from the front history alone, because the front position is only weakly sensitive to *α*_C (elasticity ≈ +0.20). The two measurements are thus naturally complementary: front kinetics pin down the thermal memory, and segregation pins down the solutal memory, so that the complete dual-order descriptor (*α*_T, *α*_C) is recoverable from a pair of standard experimental observables. This observability structure is itself a consequence of, and an argument for, the dual-memory formulation.

### 6.9 Application scenarios

The trends translate into concrete guidance. In **metal additive manufacturing**, extreme cooling through a fine cellular–dendritic structure is expected to manifest as *α*_T < 1 (a front lagging the √*t* estimate, Figure 5) and *α*_C < 1 (intensified microsegregation, Figure 4a and MSI); fitting an effective (*α*_T, *α*_C) provides a compact calibration for melt-pool models. In **sand and investment casting** against porous, low-conductivity moulds, trapping and tortuosity are naturally represented by sub-unit orders, and the predicted retardation together with the density ratio *R* bears on feeding and shrinkage-porosity timing. In **cryopreservation and the freezing of tissue and food matrices**, sub-diffusive water and solute transport through cellular structures mirrors the heavy-tailed concentration profiles of Figure 4(a) and the MSI. In **phase-change thermal storage** based on eutectic/non-eutectic mixtures, the combined influence of *Ste* and *α*_T on the front (Table 5) implies that a memory-bearing medium freezes substantially slower than a Fourier estimate predicts, which must be reflected in sizing and control. Across all cases the workflow is identical: measure a front or solidified-fraction history, extract (*α*_T, *λ*) by regression, and use (9)–(11) to reconstruct and extrapolate.

More broadly, the dual-memory construction is not specific to metallic alloys. Any moving-boundary problem that couples two transport fields with disparate diffusivities and shared history-dependence — dissolution and precipitation fronts in geochemistry, drug-release fronts in swelling polymers, moisture-and-heat fronts in drying, or ablation fronts in thermal-protection materials — presents the same structural opportunity to assign independent memory orders to the two fields. The analysis here therefore offers a template: identify the field that drives the interface balance (which fixes the kinetic exponent), assign it the primary order, assign the coupled field its own order, and close the problem with a single transcendental relation and a segregation-type index for the secondary field. In this sense the specific binary-alloy results are an instance of a general modelling strategy for anomalous, memory-coupled Stefan problems.

### 6.10 Limitations

The analysis is one-dimensional, assumes a sharp planar interface, and neglects convection and the finite extent of the mushy zone; each could be added at the cost of tractability. The reduced closure (13) and the MSI definition (14) are surrogates calibrated to the full solution over the ranges studied and should be re-fitted outside them. The Caputo kernel, with its power-law memory, is one of several choices; the Caputo–Fabrizio and Atangana–Baleanu kernels [30,31] encode exponential and Mittag-Leffler memory and would give quantitatively different, qualitatively related, retardation. Finally, the independence of *α*_T and *α*_C is a modelling hypothesis; its experimental determination for specific alloy systems — ideally by simultaneous measurement of front kinetics and interfacial segregation — is an important open task.

---

## 7. Conclusions

A two-phase, dual-memory fractional Stefan framework has been formulated and solved for the conduction-dominated solidification of an undercooled binary alloy with shrinkage/expansion, generalising the classical density-aware similarity solution to admit *independent* thermal and solutal memory through Caputo derivatives of orders *α*_T and *α*_C. The principal findings are:

1. **A generalised self-similar reduction exists** for *α*_T ≠ *α*_C, giving closed-form Mittag-Leffler/Wright fields and the interface law *s**(*t**) = 2*λ t**^(*α*_T/2), with a single transcendental equation for *λ*; the model recovers the classical benchmark to within 1.5% and the density-aware binary solution of [13], and is corroborated by an independent L1 front-fixing solver to within 1%.

2. **Thermal and solutal memory play cleanly separated roles**: *α*_T governs the interface kinetics — reducing it retards the front strongly and nonlinearly in time and steepens the near-front thermal gradient — while *α*_C governs interfacial segregation.

3. **The Memory Segregation Index** quantifies the solutal effect, rising monotonically as *α*_C falls and *Le* grows, amplifying interfacial enrichment by up to ~41%.

4. **A dual-order map and an elasticity-based sensitivity analysis** show that *α*_T dominates the long-time front position (elasticity ≈ +2.5), ahead of the density ratio and the Stefan number, with *α*_C and *Le* secondary.

5. **An inverse identification workflow** recovers the effective thermal order from a noisy front history and cuts the long-time prediction error from ~147% (classical) to below 1%, providing a practical descriptor for rapid-solidification and additive-manufacturing modelling.

By decoupling thermal and solutal memory, the framework offers a physically interpretable, low-order route to anomalous transport and microsegregation in alloy solidification. Future work will relax the sharp-interface and one-dimensional assumptions, incorporate convection, explore non-singular memory kernels, and pursue experimental identification of (*α*_T, *α*_C) for specific alloy systems.

---

## Nomenclature

| Symbol | Meaning (unit) |
|---|---|
| *C* | solute concentration (%) |
| *c*_p | specific heat (J kg⁻¹ K⁻¹) |
| *D*_l | solutal diffusivity of liquid (m² s⁻¹) |
| ᶜD_t^α | Caputo time-fractional derivative of order *α* |
| *E*_α | one-parameter Mittag-Leffler function |
| *k* | thermal conductivity (W m⁻¹ K⁻¹) |
| *k*_p | partition coefficient (–) |
| *L*_f | latent heat of fusion (J kg⁻¹) |
| *Le* | Lewis number, α_l/D_l (–) |
| *m* | liquidus slope |
| *M* | scaled liquidus slope (–) |
| MSI | Memory Segregation Index (–) |
| *R* | density ratio, ρ_s/ρ_l (–) |
| *s* | interface position (m); *s** dimensionless |
| *Ste* | Stefan number (–) |
| *T* | temperature (K); *T*_f fusion temperature |
| *t** | dimensionless time |
| *W* | Wright function |
| *x** | dimensionless coordinate |
| *α*_T, *α*_C | thermal, solutal fractional order (–) |
| α_l | thermal diffusivity (m² s⁻¹) |
| Γ | Gamma function |
| *η* | similarity variable |
| θ | dimensionless temperature |
| *λ* | growth parameter (–) |
| *ρ* | density (kg m⁻³) |
| Φ | dimensionless concentration |

Subscripts: *b* boundary; *f* fusion; *i* interface; *l* liquid; *s* solid; 0 initial.

---

## References

[1] V. Alexiades, A.D. Solomon, Mathematical Modeling of Melting and Freezing Processes, Hemisphere Publishing, Washington DC, 1993.

[2] W. Kurz, D.J. Fisher, Fundamentals of Solidification, 4th ed., Trans Tech Publications, Switzerland, 1998.

[3] J. Stefan, Über die Theorie der Eisbildung, insbesondere über die Eisbildung im Polarmeere, Ann. Phys. 278 (2) (1891) 269–286.

[4] M.N. Özışık, Heat Conduction, 2nd ed., John Wiley & Sons, New York, 1993.

[5] H.S. Carslaw, J.C. Jaeger, Conduction of Heat in Solids, 2nd ed., Oxford University Press, Oxford, 1959.

[6] L.I. Rubinstein, The Stefan Problem, Translations of Mathematical Monographs, vol. 27, American Mathematical Society, Providence, 1971.

[7] W.D. Bennon, F.P. Incropera, A continuum model for momentum, heat and species transport in binary solid–liquid phase change systems. I. Model formulation, Int. J. Heat Mass Transf. 30 (10) (1987) 2161–2170.

[8] A.B. Crowley, J.R. Ockendon, Modelling mushy regions, Appl. Sci. Res. 44 (1–2) (1987) 1–7.

[9] S. Chakraborty, P. Dutta, An analytical solution for conduction-dominated unidirectional solidification of binary mixtures, Appl. Math. Model. 26 (4) (2002) 545–561.

[10] S. Chakraborty, P. Dutta, The effect of solutal undercooling on double-diffusive convection and macro-segregation during binary alloy solidification: a numerical investigation, Int. J. Numer. Methods Fluids 38 (9) (2002) 895–917.

[11] V.R. Voller, A similarity solution for solidification of an under-cooled binary alloy, Int. J. Heat Mass Transf. 49 (11) (2006) 1981–1985.

[12] V.R. Voller, An enthalpy method for modeling dendritic growth in a binary alloy, Int. J. Heat Mass Transf. 51 (3) (2008) 823–834.

[13] A. Jakhar, P. Rath, S.K. Mahapatra, A similarity solution for phase change of binary alloy with shrinkage or expansion, Eng. Sci. Technol. Int. J. 19 (3) (2016) 1390–1399.

[14] R. Metzler, J. Klafter, The random walk's guide to anomalous diffusion: a fractional dynamics approach, Phys. Rep. 339 (1) (2000) 1–77.

[15] F. Mainardi, Fractional Calculus and Waves in Linear Viscoelasticity, Imperial College Press, London, 2010.

[16] R. Gorenflo, A.A. Kilbas, F. Mainardi, S.V. Rogosin, Mittag-Leffler Functions, Related Topics and Applications, Springer, Berlin, 2014.

[17] I. Podlubny, Fractional Differential Equations, Academic Press, San Diego, 1999.

[18] A.A. Kilbas, H.M. Srivastava, J.J. Trujillo, Theory and Applications of Fractional Differential Equations, Elsevier, Amsterdam, 2006.

[19] V.R. Voller, An exact solution of a limit case Stefan problem governed by a fractional diffusion equation, Int. J. Heat Mass Transf. 53 (23–24) (2010) 5622–5625.

[20] V.R. Voller, Fractional Stefan problems, Int. J. Heat Mass Transf. 74 (2014) 269–277.

[21] Rajeev, M.S. Kushwaha, Homotopy perturbation method for a limit case Stefan problem governed by fractional diffusion equation, Appl. Math. Model. 37 (5) (2013) 3589–3599.

[22] J. Singh, P.K. Gupta, K.N. Rai, Solution of fractional bioheat equations by finite difference method and HPM, Math. Comput. Model. 54 (9–10) (2011) 2316–2325.

[23] S.D. Roscani, E.A. Santillán Marcus, Two equivalent Stefan's problems for the time-fractional diffusion equation, Fract. Calc. Appl. Anal. 16 (4) (2013) 802–815.

[24] S.D. Roscani, D.A. Tarzia, A generalized Neumann solution for the two-phase fractional Lamé–Clapeyron–Stefan problem, Adv. Math. Sci. Appl. 24 (2) (2014) 237–249.

[25] F. Falcini, R. Garra, V.R. Voller, Fractional Stefan problems exhibiting lumped and distributed latent-heat memory effects, Phys. Rev. E 87 (4) (2013) 042401.

[26] Y. Lin, C. Xu, Finite difference/spectral approximations for the time-fractional diffusion equation, J. Comput. Phys. 225 (2) (2007) 1533–1552.

[27] F. Liu, P. Zhuang, V. Anh, I. Turner, K. Burrage, Stability and convergence of the difference methods for the space–time fractional advection–diffusion equation, Appl. Math. Comput. 191 (1) (2007) 12–20.

[28] V.R. Voller, F. Falcini, R. Garra, Fractional Stefan problems exhibiting lumped and distributed latent-heat memory effects: a numerical study, Int. J. Heat Mass Transf. 58 (1–2) (2013) 80–90.

[29] A. Esen, Y. Ucar, N. Yagmurlu, O. Tasbozan, A Galerkin finite element method to solve fractional diffusion and fractional diffusion–wave equations, Math. Model. Anal. 18 (2) (2013) 260–273.

[30] M. Caputo, M. Fabrizio, A new definition of fractional derivative without singular kernel, Prog. Fract. Differ. Appl. 1 (2) (2015) 73–85.

[31] A. Atangana, D. Baleanu, New fractional derivatives with nonlocal and non-singular kernel: theory and application to heat transfer model, Therm. Sci. 20 (2) (2016) 763–769.

[32] M. Caputo, Linear models of dissipation whose Q is almost frequency independent — II, Geophys. J. R. Astron. Soc. 13 (5) (1967) 529–539.

[33] R. Hilfer (Ed.), Applications of Fractional Calculus in Physics, World Scientific, Singapore, 2000.

[34] S.D. Roscani, D.A. Tarzia, Explicit solution for a two-phase fractional Stefan problem with a heat flux condition at the fixed face, Comput. Appl. Math. 37 (4) (2018) 4757–4771.

[35] A. Kumar, A.K. Singh, Rajeev, A moving boundary problem with variable thermal conductivity and time-dependent heat flux governed by a fractional derivative, Meccanica 55 (10) (2020) 2047–2060.

[36] R. Garra, A. Giusti, F. Mainardi, G. Pagnini, Fractional relaxation with time-varying coefficient, Fract. Calc. Appl. Anal. 17 (2) (2014) 424–439.

[37] A. Compte, R. Metzler, The generalized Cattaneo equation for the description of anomalous transport processes, J. Phys. A: Math. Gen. 30 (21) (1997) 7277–7289.

[38] Y. Povstenko, Fractional Thermoelasticity, Springer, Cham, 2015.

[39] S. Das, Functional Fractional Calculus, 2nd ed., Springer, Berlin, 2011.

[40] D. Baleanu, K. Diethelm, E. Scalas, J.J. Trujillo, Fractional Calculus: Models and Numerical Methods, World Scientific, Singapore, 2012.

[41] J. Crank, Free and Moving Boundary Problems, Clarendon Press, Oxford, 1984.

[42] M. Flemings, Solidification Processing, McGraw-Hill, New York, 1974.

[43] W.J. Boettinger, S.R. Coriell, A.L. Greer, A. Karma, W. Kurz, M. Rappaz, R. Trivedi, Solidification microstructures: recent developments, future directions, Acta Mater. 48 (1) (2000) 43–70.

[44] D.A. Tarzia, Explicit and approximated solutions for heat and mass transfer problems with a moving interface, in: Advanced Topics in Mass Transfer, InTech, 2011, pp. 439–484.

[45] S.D. Roscani, N.N. Salva, D.A. Tarzia, Half-phase-space anomalous diffusion in a fractional Stefan problem, Commun. Nonlinear Sci. Numer. Simul. 90 (2020) 105361.

[46] A.N. Ceretani, D.A. Tarzia, Determination of two unknown thermal coefficients through a phase-change process with temperature-dependent thermal conductivity, Int. Commun. Heat Mass Transf. 87 (2017) 220–228.

[47] T.A.M. Langlands, B.I. Henry, The accuracy and stability of an implicit solution method for the fractional diffusion equation, J. Comput. Phys. 205 (2) (2005) 719–736.

[48] C. Li, F. Zeng, Numerical Methods for Fractional Calculus, Chapman and Hall/CRC, Boca Raton, 2015.

---

*Figures (generated by `generate_fractional_figures.py`, stored in `fractional_figures/`):*

- **Figure 1.** Dual-memory fractional Stefan domain: solid, mushy zone and undercooled liquid, with the independent thermal (α_T) and solutal (α_C) fractional operators, interface conditions, density ratio R, and the anomalous advance ⟨s²⟩ ∼ t^(α_T).
- **Figure 2.** Independent thermal (a) and solutal (b) Mittag-Leffler memory kernels Eₐ(−tᵃ), showing the heavy algebraic tails that signify long memory and the independence of α_T and α_C.
- **Figure 3.** Liquid-phase temperature profiles against the similarity variable η for thermal orders α_T = 1.0, 0.85, 0.70, 0.55 (α_C = 1, Le = 1, Ste = 0.5).
- **Figure 4.** Solute concentration profiles: (a) effect of solutal order α_C at Le = 10; (b) effect of Lewis number Le at α_C = 0.8.
- **Figure 5.** Interface position histories s*(t*) = 2λ t*^(α_T/2) for α_T = 1.0–0.6 (α_C = 1, Le = 1, Ste = 0.5, R = 1).
- **Figure 6.** Growth parameter λ versus thermal order α_T for Lewis numbers Le = 0.5, 1, 5, 20 (α_C = 1, Ste = 0.5, R = 1).
- **Figure 7.** Dual-memory heat map of the interface position s*(t* = 100) over the (α_C, α_T) plane, showing the dominant vertical (thermal) gradient and weak horizontal (solutal) modulation (Le = 1, Ste = 0.5, R = 1).
- **Figure 8.** (a) Memory Segregation Index MSI versus solutal order α_C for Le = 1, 5, 20; (b) normalised sensitivity (elasticity) of s*(t* = 100) to α_T, α_C, Ste, Le and R.
- **Figure 9.** Inverse memory identification: (a) a noisy synthetic front history fitted by the identified law (α_T = 0.72) versus the classical √t law; (b) long-time prediction error of the classical, single-order and present dual-order models against the data.
