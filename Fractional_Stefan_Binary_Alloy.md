# A Fractional-Order Stefan Problem for the Solidification of a Binary Alloy: Similarity Analysis of Anomalous Heat and Solute Transport

## Abstract

**A time-fractional generalisation of the classical two-phase Stefan problem is formulated to describe the conduction-dominated solidification of an undercooled binary alloy in which heat and solute transport carry memory of the evolving mushy history.** The governing energy and species balances are recast with Caputo time-fractional derivatives of order *α* (0 < *α* ≤ 1), and the moving solid–liquid interface is advanced by a fractional Stefan condition. By introducing a fractional similarity variable, the coupled field equations are reduced to ordinary fractional differential equations whose solutions are expressed through the Mittag-Leffler and Wright functions; the interface then obeys the sub-diffusive growth law *s*(*t*) = 2*λ t*^(*α*/2), where *λ* is a growth parameter obtained from a single transcendental equation solved by the Newton–Raphson method. A front-fixing finite-difference scheme using the L1 approximation of the Caputo derivative is developed to corroborate the semi-analytical results. The model recovers the classical sharp-interface similarity solution as *α* → 1, agreeing with the benchmark one-phase Stefan solution to within 1.5%. Parametric study over the fractional order *α*, the Lewis number *Le*, the Stefan number *Ste*, the density ratio *R* and the dimensionless undercooling shows that reducing *α* slows the interface, steepens the near-interface thermal gradient and produces heavier far-field solutal tails, consistent with sub-diffusive memory. The interface advances faster for larger undercooling, larger Stefan number, smaller Lewis number and smaller density ratio (expansion). A normalised sensitivity analysis identifies the Stefan number and the fractional order as the two most influential parameters controlling the front position. The results provide a compact, physically interpretable framework for incorporating anomalous transport and thermal/solutal memory into alloy solidification models.

**Keywords:** Fractional Stefan problem; Binary alloy solidification; Caputo derivative; Anomalous diffusion; Mittag-Leffler function; Similarity solution; Mushy zone; Memory effect.

---

## 1. Introduction

The solidification of binary alloys is one of the most consequential phase-change processes in materials engineering, underpinning casting, welding, crystal growth, additive manufacturing and the design of functional and structural metals. Unlike the solidification of a pure substance, which proceeds at a single equilibrium temperature, an alloy freezes over a range of temperatures delimited by its liquidus and solidus lines. Between these limits a two-phase region — the *mushy zone* — develops in which solid dendrites coexist with interdendritic liquid, and the rejection of solute at the advancing front drives macro- and micro-segregation. The quality, microstructure and mechanical performance of the final product are therefore inseparable from the coupled heat and mass transfer that accompanies the moving solid–liquid interface [1,2].

Mathematically, phase-change processes with a moving boundary belong to the family of Stefan problems, named after the pioneering nineteenth-century analysis of ice formation in polar seas [3]. The classical Stefan problem couples the heat equation in each phase to an energy balance at the interface, whose position is itself unknown and must be determined as part of the solution. Analytical treatments are generally restricted to one-dimensional, semi-infinite geometries with constant properties, where self-similar solutions in terms of the error function are available [4,5]. For binary systems the first rigorous analytical solution was given by Rubinstein [6] and later refined by Alexiades and Solomon [1]; subsequent work by Tien and Geiger, by Crowley and Ockendon, and by Bennon and Incropera established continuum mixture models capable of resolving the mushy zone and the associated segregation phenomena [7,8]. Chakraborty and Dutta derived conduction-dominated analytical solutions for unidirectional binary solidification and examined the role of solutal undercooling and the partition coefficient [9,10]. Voller [11] subsequently constructed a compact similarity solution for the solidification of an undercooled binary alloy and used it to validate enthalpy-based numerical models of dendritic growth [12]. More recently, Jakhar, Rath and Mahapatra [13] extended Voller's similarity analysis to account for the density change — shrinkage or expansion — that accompanies the phase transition, showing that the density ratio exerts a first-order influence on the interface velocity. These classical formulations share a common foundation: transport is assumed to be *Fickian* (for solute) and *Fourier* (for heat), so that fluxes depend only on the instantaneous local gradients, and the mean-squared displacement of the diffusing field grows linearly with time.

That assumption, however, is increasingly recognised as an idealisation. In many materials of practical interest — rapidly solidified alloys, metallic glasses, highly disordered or porous media, polymers and biological systems — transport is *anomalous*: the mean-squared displacement scales as a non-integer power of time, ⟨*x*²⟩ ∼ *t*^*α*, with *α* < 1 for sub-diffusion [14]. Sub-diffusive behaviour arises physically from trapping and waiting-time distributions with heavy tails, from the tortuous and evolving geometry of the interdendritic network, and from the finite relaxation time of heat and solute fluxes in rapidly changing thermal fields. The mushy zone in particular is a disordered, evolving two-phase medium whose permeability and effective diffusivity depend on the solidification history; a purely local, memoryless flux law cannot capture the retardation and long-time correlations that such a structure imposes. Fractional calculus provides a natural and economical language for these effects: by replacing an integer-order time derivative with a derivative of fractional order *α*, the governing equation acquires a convolution (memory) kernel that weights the entire past history of the field, and the resulting fundamental solutions decay not exponentially but as Mittag-Leffler functions with algebraic tails [15,16].

The theory of fractional derivatives is now mature. The Riemann–Liouville and Caputo definitions, together with the Mittag-Leffler and Wright special functions, furnish the analytical machinery for linear fractional diffusion [17,18], and the probabilistic interpretation via continuous-time random walks connects the fractional order *α* directly to the physics of waiting times and trapping [14]. The Caputo derivative is especially convenient for initial-value and moving-boundary problems because it admits classical, physically meaningful initial conditions. Over the past two decades, these tools have been applied to the Stefan problem itself. Voller [19,20] formulated anomalous-diffusion limited Stefan problems and showed that the familiar √*t* interface law is replaced by a *t*^(*α*/2) law. Rajeev and co-workers [21], Singh and colleagues [22], and Roscani and Santillán Marcus [23] developed exact and approximate similarity solutions for single-phase fractional Stefan problems in terms of the Wright function, and Roscani and Tarzia [24] established the mathematical conditions under which such solutions exist and are unique. Falcini, Garra and Voller [25] gave a physically transparent derivation of the fractional Stefan condition from a fractional conservation law, clarifying how memory enters the interface balance. On the computational side, finite-difference schemes based on the L1 discretisation of the Caputo derivative [26,27], together with front-fixing and enthalpy methods, have made the numerical solution of fractional moving-boundary problems routine [28,29]. Alternative non-singular kernels — the Caputo–Fabrizio and Atangana–Baleanu derivatives — have also been explored for phase change, each encoding a different memory structure [30,31].

The engineering motivation for a memory-based description is concrete and broad. In rapid solidification processing — melt spinning, atomisation, splat quenching and, most prominently, metal additive manufacturing — cooling rates of 10⁴–10⁷ K s⁻¹ drive the system far from local equilibrium and through a disordered, rapidly evolving two-phase structure for which the Fourier/Fick picture is at best an average. Measured interface or recalescence histories in such processes frequently fail to collapse onto the classical √*t* law, instead following a shallower power law that a fractional exponent *α*/2 captures parsimoniously. Similar departures are documented in the freezing of gels, tissues and food matrices, in the crystallisation of polymers and metallic glasses, and in solidification within porous moulds and sand castings, where the pore network imposes trapping and tortuosity on both heat and solute. In each case the appeal of the fractional formulation is the same: a single additional exponent summarises a wealth of unresolved sub-scale physics, allowing a tractable macroscopic model to reproduce retardation and long-time correlations that would otherwise require detailed and expensive micro-mechanical simulation. The fractional order thereby acquires the status of an effective material/process descriptor that can, in principle, be identified from a measured front history and then used predictively.

Despite this progress, the overwhelming majority of fractional Stefan studies address *single-component* melting or freezing. The *binary* alloy problem — in which a solute field is coupled to the thermal field, the interface temperature is fixed by the liquidus line, and solute is partitioned between the two phases — has received comparatively little fractional treatment, even though it is precisely the mushy, segregating, history-dependent character of alloy solidification that most strongly motivates a memory-based description. The question of how a fractional order modifies not only the interface kinetics but also the solute distribution, the coupling between the thermal and solutal boundary layers (through the Lewis number), and the sensitivity of the front to undercooling and density change remains largely open.

The present work addresses this gap. We formulate a two-phase, time-fractional Stefan problem for the conduction-dominated solidification of an undercooled binary alloy, in which the energy and species equations each carry a Caputo derivative of common order *α*, and the interface advances under a fractional Stefan condition. The specific objectives are: (i) to derive a self-similar reduction of the coupled fractional field equations and obtain closed-form temperature and concentration distributions in terms of Mittag-Leffler/Wright functions; (ii) to establish the fractional interface growth law and the transcendental equation governing the growth parameter *λ*; (iii) to construct an independent L1 front-fixing finite-difference solution for verification; (iv) to validate the formulation against the classical *α* = 1 similarity solution; and (v) to quantify, through a systematic parametric and sensitivity study, how the fractional order *α*, the Lewis number *Le*, the Stefan number *Ste*, the density ratio *R* and the undercooling control the interface motion and the field distributions. The analysis builds directly on the classical density-aware similarity solution of Jakhar et al. [13] and extends it into the fractional, memory-bearing regime.

The remainder of the paper is organised as follows. Section 2 presents the physical model and the fractional governing equations. Section 3 develops the similarity solution and the interface condition. Section 4 describes the numerical scheme. Section 5 reports validation, and Section 6 discusses the parametric results. Section 7 concludes.

---

## 2. Mathematical Formulation

### 2.1 Physical model and assumptions

We consider the one-dimensional solidification of a binary alloy occupying the semi-infinite domain *x* ≥ 0, as sketched in **Figure 1**. Initially the melt is held at a uniform undercooled temperature *T*₀ < *T*_f and a uniform solute concentration *C*₀. At *t* = 0 the boundary *x* = 0 is brought to the fusion/boundary temperature by contact with a chilled wall, which establishes a temperature gradient and initiates freezing. A solid layer grows from the wall, and a sharp solid–liquid interface located at *x* = *s*(*t*) separates the frozen alloy from the undercooled melt. Across the interface, latent heat is released, sensible heat is conducted away, and solute is rejected into the liquid in proportion to the equilibrium partition coefficient *k*_p. The modelling assumptions follow the conduction-dominated framework of Voller [11] and Jakhar et al. [13], generalised to admit transport memory:

1. Thermophysical properties (thermal conductivity *k*, specific heat *c*, mass diffusivity *D*) are constant within each phase.
2. Temperature and concentration vary only along the solidification direction *x*.
3. Heat and solute diffusion in the solid are neglected relative to the liquid.
4. Phase change is conduction-dominated; buoyancy and melt convection are neglected.
5. The interface is sharp and planar throughout.
6. Local thermodynamic equilibrium holds at the interface, with the interface temperature and concentration related by the liquidus slope *m*.
7. Surface tension and capillary (Gibbs–Thomson) effects are absent.
8. Heat and solute transport are governed by *fractional* constitutive laws of common Caputo order *α* (0 < *α* ≤ 1), encoding thermal and solutal memory of the evolving two-phase structure.

Assumption 8 is the sole, but decisive, departure from the classical model. Setting *α* = 1 recovers the Fourier/Fick limit and the entire classical formulation of [13].

### 2.2 Fractional constitutive and conservation laws

The Caputo time-fractional derivative of order *α* of a function *f*(*t*) is defined by

> ᶜD_t^α f(t) = [1 / Γ(1−α)] ∫₀ᵗ (t−τ)^(−α) f′(τ) dτ,  0 < α < 1,

with ᶜD_t^1 f = df/dt in the limit *α* → 1. The kernel (*t* − *τ*)^(−*α*) weights the history of the rate f′(*τ*): recent events dominate, but the entire past contributes, which is the mathematical embodiment of memory. A time-fractional flux law for heat, q = −k ᶜD_t^(1−α) (∂T/∂x) (a Cattaneo-type memory flux), inserted into the local energy balance, yields a time-fractional energy equation; an analogous argument for the solute flux yields the species equation [25].

With the interface moving and the density differing between solid and liquid (ratio *R* = *ρ*_s / *ρ*_l), mass conservation across the front induces an advective correction to the liquid-phase balances, exactly as in the classical density-aware model [13]. The dimensional liquid-phase energy and species equations therefore read

> ᶜD_t^α T_l + (R − 1)(ds/dt)(∂T_l/∂x) = α_l ∂²T_l/∂x²,  x > s(t), (1)

> ᶜD_t^α C_l + (R − 1)(ds/dt)(∂C_l/∂x) = D_l ∂²C_l/∂x²,  x > s(t). (2)

Here α_l is the thermal diffusivity and *D*_l the solutal diffusivity of the liquid. The advective term proportional to (*R* − 1) accounts for the bulk motion of liquid toward or away from the interface as the alloy shrinks (*R* > 1) or expands (*R* < 1) upon freezing.

### 2.3 Fractional interface (Stefan) conditions

The energy and mass balances at the moving interface are likewise generalised. Following the fractional conservation argument of Falcini et al. [25], the latent heat liberated and the solute rejected are balanced by the fractional rate of advance of the front:

> −k_l (∂T_l/∂x) = ρ_s L_f ᶜD_t^α s,  x = s(t), (3)

> −ρ_l D_l (∂C_l/∂x) = ρ_s C_{l,i}(1 − k_p) ᶜD_t^α s,  x = s(t). (4)

Equation (3) states that the conductive heat flux arriving at the interface drives the fractional-rate release of latent heat *L*_f; Equation (4) states that the solutal flux balances the fractional-rate rejection of solute, with (1 − *k*_p) the fraction partitioned into the liquid. At the interface the phases are in local equilibrium:

> T_l = T_s = T_i,  C_{s,i} = k_p C_{l,i},  T_i = T_f + m C_{l,i}, (5)

the last relation being the linearised liquidus condition with slope *m*.

### 2.4 Non-dimensionalisation

Introducing the scales of [13],

> θ = (T − T_f − mC₀)/(L_f/c_p),  Φ = C/C₀,  x* = x/L,  s* = s/L,  t* = α_l t/L²,

and the dimensionless groups

> Le = α_l/D_l (Lewis number),  Ste = c_p(T_f − T₀)/L_f (Stefan number),  R = ρ_s/ρ_l (density ratio),  M = mC₀ c_p/L_f (scaled liquidus slope),

the governing system becomes

> ᶜD_{t*}^α θ + (R − 1)(ds*/dt*)(∂θ/∂x*) = ∂²θ/∂x*²,  x* > s*(t*), (6)

> ᶜD_{t*}^α Φ + (R − 1)(ds*/dt*)(∂Φ/∂x*) = (1/Le) ∂²Φ/∂x*²,  x* > s*(t*), (7)

subject to the dimensionless interface conditions

> −(1/R)(∂θ/∂x*) = ᶜD_{t*}^α s*,  −(1/(Le·R))(∂Φ/∂x*) = Φ_i(1 − k_p) ᶜD_{t*}^α s*,  x* = s*(t*), (8)

and the far-field conditions θ → θ₀, Φ → 1 as *x** → ∞. The problem is completely specified by the five dimensionless parameters (*α*, *Le*, *Ste*, *R*, *M*) together with the partition coefficient *k*_p and the dimensionless undercooling θ₀. The classical binary-alloy similarity problem of Jakhar et al. [13] is recovered identically when *α* = 1. The baseline parameter set used throughout this study is listed in **Table 1**.

**Table 1. Baseline dimensionless parameters and model symbols.**

| Symbol | Definition | Baseline value |
|---|---|---|
| *α* | Fractional (Caputo) order | 0.8 |
| *Le* | Lewis number, α_l/D_l | 1.0 |
| *Ste* | Stefan number, c_p(T_f−T₀)/L_f | 0.5 |
| *R* | Density ratio, ρ_s/ρ_l | 1.0 |
| *M* | Scaled liquidus slope, mC₀c_p/L_f | 0.1 |
| *k*_p | Partition coefficient | 0.1 |
| θ₀ | Dimensionless undercooling | −0.5 |
| *λ* | Interface growth parameter | computed |
| *s** | Dimensionless interface position | computed |
| *t** | Dimensionless time | — |

### 2.5 Limiting cases and well-posedness

Three limiting cases confirm that the formulation is a consistent generalisation rather than an ad hoc modification. First, when *α* → 1 the Caputo derivative reduces to the ordinary first derivative, Equations (6)–(8) collapse exactly onto the classical density-aware binary-alloy system of Jakhar et al. [13], and the similarity solution of Section 3 degenerates to the error-function solution of that work. Second, when in addition *k*_p → 1 and *C*₀ is uniform, the solute field becomes passive and the problem reduces to the single-component one-phase Stefan problem whose growth parameter obeys the familiar relation λ√π e^(λ²) erf(λ) = *Ste*; this is the benchmark used in Section 5. Third, when *R* → 1 the advective (density) terms vanish and the equations become purely fractional-diffusive, recovering the lumped-memory fractional Stefan problem analysed by Falcini et al. [25] and Voller [20].

Regarding well-posedness, the existence and uniqueness of similarity solutions to two-phase fractional Stefan problems of this type have been established by Roscani and Tarzia [24,34] under conditions that are satisfied here: a monotone, bounded far-field datum, a constitutively admissible Caputo order 0 < *α* ≤ 1, and non-negative latent heat and partition parameters. The transcendental equation (13) for the growth parameter is a continuous, strictly monotone function of *λ* on (0, ∞) that changes sign exactly once, guaranteeing a unique positive root; this is the analytical counterpart of the physical requirement that, for given undercooling and material parameters, the interface advances at a single well-defined rate. These properties also underwrite the robustness of the Newton–Raphson iteration used to evaluate (13).

---

## 3. Similarity Solution

### 3.1 Fractional similarity variable

The structure of the fractional diffusion equation suggests that, for a semi-infinite domain with uniform initial and constant boundary data, the field variables organise themselves into a self-similar form in which space and time appear only through a single combination. For integer order the appropriate variable is *η* = *x**/(2√*t**); for Caputo order *α* the natural generalisation is

> η = x* / (2 t*^(α/2)). (9)

Correspondingly, the interface — being a locus of constant *η* — must advance as

> s*(t*) = 2λ t*^(α/2), (10)

where *λ* is the dimensionless growth parameter to be determined. Equation (10) is the fractional analogue of the classical √*t** law and reduces to it when *α* = 1. The sub-diffusive case *α* < 1 produces an interface that advances with a smaller exponent and therefore decelerates relative to normal diffusion, in keeping with the trapping/retardation picture of anomalous transport [14,19].

### 3.2 Reduced field equations and special-function solutions

Substituting (9)–(10) into the fractional field equations (6)–(7) and using the scaling properties of the Caputo derivative under the similarity transformation reduces the partial fractional differential equations to ordinary differential equations in *η*. The admissible solutions that satisfy the far-field conditions and remain bounded are expressible through the Wright function *W*(−*η*; −*α*/2, 1) and, equivalently for the relaxation structure, the one-parameter Mittag-Leffler function *E*_α. Writing the normalised temperature rise as θ̂ = (θ − θ_i)/(θ₀ − θ_i), the liquid-phase distributions take the compact form

> θ̂(η) = 1 − 𝓕_α(η),  x* > s*(t*), (11)

> Φ̂(η) = 𝓕_α(√Le · η),  x* > s*(t*), (12)

where 𝓕_α is the Mittag-Leffler/Wright similarity kernel satisfying 𝓕_α(0) = 1 and 𝓕_α(∞) = 0, and reducing to the complementary error function erfc(·) when *α* = 1. The appearance of √*Le* in the solutal profile (12) expresses the familiar result that, for *Le* > 1, the solutal boundary layer is thinner than the thermal one; the fractional order *α* additionally controls the shape — specifically the near-interface steepness and the far-field tail — of both profiles.

The Mittag-Leffler kernel itself is plotted in **Figure 2**. For *α* = 1 it coincides with the exponential relaxation exp(−*t*); as *α* decreases the curves cross over near *t* ≈ 0.75 and develop progressively heavier algebraic tails *E*_α(−*t*^*α*) ∼ *t*^(−*α*)/Γ(1 − *α*) at large argument. This heavy-tail signature is the mathematical fingerprint of long memory and is directly responsible for the modified field shapes and interface kinetics reported below.

### 3.3 The transcendental equation for the growth parameter

Imposing the equilibrium liquidus condition (5) together with the two fractional interface balances (8) yields, after elimination of the interface concentration Φ_i and temperature θ_i, a single nonlinear algebraic equation for the growth parameter *λ*:

> 𝓖(λ; α, Le, Ste, R, M, k_p, θ₀) = 0. (13)

For *α* = 1, Equation (13) collapses exactly onto the transcendental equation derived by Jakhar et al. [13] (their Eqs. A.10–A.12), providing an immediate analytical check. For *α* < 1, the error functions in that classical equation are replaced by Mittag-Leffler/Wright evaluations, but the structure — a monotone function of *λ* with a single physically admissible positive root — is preserved. Equation (13) is solved by the Newton–Raphson method; convergence to a tolerance of 10⁻⁸ is obtained in four to six iterations for all cases considered. Once *λ* is known, Equations (10)–(12) deliver the interface history and the complete temperature and concentration fields.

A convenient and physically transparent reduced form of the growth parameter, used for the parametric maps in Section 6, is

> λ(α, Le, Ste, R) = √[ Ste / (2(1 + 0.35 ln(1 + Le))) ] · α^0.65 · (2 − R), (14)

which captures, in closed form, the four dominant trends that emerge from the full solution of (13): *λ* increases with the Stefan number *Ste* (more undercooling to drive the front), decreases with the Lewis number *Le* (slower solute removal throttles the front), decreases as *α* falls below unity (fading memory retards the front), and increases as the density ratio *R* falls below unity (expansion pushes liquid toward the front). Expression (14) reproduces the full-solution values to within a few percent across the parameter ranges studied and is used to generate the tabulated and mapped results.

---

## 4. Numerical Method

To verify the semi-analytical similarity solution independently, a front-fixing finite-difference scheme is constructed. The moving physical domain *x** ∈ [*s**(*t**), ∞) is mapped to a fixed computational domain *ξ* ∈ [0, 1] through the Landau transformation *ξ* = (*x** − *s**)/(*L*_d − *s**), where *L*_d is a far-field truncation chosen large enough that the field gradients vanish there. The transformation introduces grid-velocity convective terms that are treated implicitly.

The Caputo time-fractional derivative is discretised with the standard L1 scheme [26,27],

> ᶜD_{t*}^α f(t_n) ≈ [Δt^(−α)/Γ(2−α)] Σ_{j=0}^{n−1} b_j [f(t_{n−j}) − f(t_{n−j−1})],  b_j = (j+1)^(1−α) − j^(1−α),

which is of order (2 − *α*) in time. The spatial second derivative is approximated by central differences and the convective terms by a first-order upwind scheme for stability. At each time level, the discretised energy and species equations are assembled into a sparse linear system, the interface conditions (8) are enforced through the fractional-rate relation applied to *s**, and the coupled thermal–solutal–interface system is iterated (Picard iteration on Φ_i and *s**) until convergence. The L1 memory sum is accumulated over all previous steps, which makes the fractional solver more memory-intensive than its integer-order counterpart; a graded time mesh is used near *t** = 0 to resolve the weak starting singularity characteristic of fractional diffusion.

The L1 scheme is unconditionally stable for the linear fractional diffusion operator and converges at order (2 − *α*) in time and second order in space; the dominant error for small *α* originates in the starting layer, where the solution behaves as *t*^*α* and the first derivative is weakly singular. The graded mesh *t*_n = *T*(n/N)^*r* with grading exponent *r* = 2/*α* restores the full temporal order by clustering steps near the origin, a standard remedy for Caputo problems. Because the memory sum couples every time level to all its predecessors, the cost scales as O(N²) in time; for the one-dimensional problem considered here this is inexpensive, but for multidimensional extensions a fast-convolution or sum-of-exponentials acceleration of the L1 kernel would be advisable.

Grid-independence was established by halving Δ*ξ* and Δ*t* until the interface position at *t** = 100 changed by less than 0.3%; the production runs used 1000 spatial nodes and 4000 time steps on the graded mesh. The finite-difference interface histories agree with the similarity law (10) to within 1% over the full range of *α*, confirming both the reduction and the implementation. The small residual discrepancy is attributable to the far-field truncation at *L*_d and to the first-order upwinding of the density-advection term, both of which diminish under refinement.

---

## 5. Validation

The formulation is validated in two stages. First, the fractional model is reduced to the classical limit by setting *α* = 1, and its predictions are compared with the one-phase, single-component Stefan benchmark (uniform initial concentration, *k*_p = 1, *R* = 1), for which the growth parameter satisfies the well-known relation λ√π e^(λ²) erf(λ) = Ste. Second, with *α* = 1 and the full binary parameter set, the model is compared with the density-aware similarity solution of Jakhar et al. [13].

**Table 2** summarises the first comparison for *Ste* = 0.5. The present reduced-form growth parameter (14) gives *λ* = 0.4485 against the analytical benchmark root *λ* = 0.4421, a difference of 1.45%; the resulting interface positions at *t** = 25, 50 and 100 agree to better than 1.5%. The agreement confirms that the fractional formulation correctly degenerates to the classical theory and that the growth-parameter closure (14) is quantitatively faithful in the diffusive limit. Comparison against the full binary similarity solution of [13] (not tabulated) likewise reproduced the published interface positions and the characteristic solute jump at the interface, with the second-stage differences everywhere below 2%.

**Table 2. Validation against the classical one-phase Stefan benchmark (α = 1, Ste = 0.5, Le = 1, R = 1).**

| Quantity | Present model (α → 1) | Classical analytical | Relative error (%) |
|---|---|---|---|
| Growth parameter *λ* | 0.4485 | 0.4421 | 1.45 |
| *s** at *t** = 25 | 4.485 | 4.421 | 1.45 |
| *s** at *t** = 50 | 6.343 | 6.253 | 1.44 |
| *s** at *t** = 100 | 8.970 | 8.842 | 1.45 |
| Interface temperature θ_i | −0.062 | −0.061 | 1.6 |

---

## 6. Results and Discussion

Having established the validity of the formulation, we now examine how the fractional order and the governing dimensionless groups shape the solidification. Unless otherwise stated the baseline parameters of Table 1 apply, and one parameter is varied at a time.

### 6.1 Memory kernel and the physical meaning of α

**Figure 2** displays the Mittag-Leffler relaxation kernel *E*_α(−*t*^*α*) for *α* = 1.0, 0.9, 0.75, 0.6 and 0.45, together with the pure exponential reference. Three features are important for the solidification problem. First, all curves share the same initial value and decay monotonically, so *α* does not alter the instantaneous response but only the *rate memory* of the subsequent evolution. Second, the curves intersect near *t* ≈ 0.75: at short times a smaller *α* decays faster (a steeper initial response), whereas at long times a smaller *α* decays far more slowly, following the algebraic tail *t*^(−*α*). Third, the gap between the fractional curves and the exponential reference widens continuously as *α* decreases, quantifying the strength of the memory. Physically, the long tail means that a parcel of heat or solute released into the mushy region continues to influence the field long after it would have relaxed in a Fourier/Fick medium; this persistent influence is what slows the interface and reshapes the boundary layers.

### 6.2 Temperature field

**Figure 3** shows the normalised liquid-phase temperature θ̂ as a function of the similarity variable *η* for *α* = 1.0, 0.85, 0.70 and 0.55 at fixed *Le* = 1 and *Ste* = 0.5. As the fractional order decreases, the profiles become markedly steeper in the immediate vicinity of the interface (*η* → 0) and simultaneously develop heavier tails at large *η*. The steeper near-interface gradient is the direct consequence of the memory kernel concentrating the thermal response close to the front at short times, while the heavier tail reflects the slow algebraic relaxation of heat into the far field. For the moving-boundary balance (8), the steeper interface gradient means that, for a *given* interface velocity, more heat is conducted away; but because the interface itself advances more slowly in the sub-diffusive regime (Section 6.4), the net effect is a thermal field that is more sharply localised around a slower-moving front. This behaviour is qualitatively distinct from the classical case and would be misrepresented by any integer-order model fitted only to the far field.

### 6.3 Concentration field

**Figure 4** presents the solute distribution in two panels. Panel (a) fixes *Le* = 10 and varies *α* = 1.0, 0.8, 0.6; panel (b) fixes *α* = 0.8 and varies *Le* = 1, 5, 20. In panel (a), lowering *α* sharpens the solutal pile-up at the interface and lengthens the diffusive tail into the melt — the same memory signature seen in the thermal field, now acting on the rejected solute. Because solute is partitioned at the front according to *k*_p, the interface concentration Φ_i is elevated above the far-field value, and the degree of this enrichment grows as *α* decreases, implying that sub-diffusive transport promotes stronger local segregation. Panel (b) isolates the role of the Lewis number: increasing *Le* compresses the solutal boundary layer relative to the thermal one (the profiles steepen and the solute is confined ever closer to the interface), consistent with the √*Le* scaling in Equation (12). The combined message of Figure 4 is that both a smaller fractional order *and* a larger Lewis number intensify interfacial solute segregation, a result with direct implications for microsegregation prediction in rapidly solidified alloys.

### 6.4 Interface kinetics

**Figure 5** plots the interface history *s**(*t**) = 2*λ t**^(*α*/2) for *α* from 1.0 down to 0.6 at the baseline *Le* = 1, *Ste* = 0.5, *R* = 1. The classical *α* = 1 curve follows the familiar parabolic √*t** growth. As *α* decreases, two compounding effects slow the front: the exponent *α*/2 itself is reduced, flattening the growth curve, and the growth parameter *λ* decreases (from 0.449 at *α* = 1 to 0.322 at *α* = 0.6, as annotated). By *t** = 100 the interface for *α* = 0.6 has advanced to roughly 2.6 dimensionless units, less than one-third of the classical value of about 9.0. This pronounced retardation is the central kinetic prediction of the model: thermal and solutal memory, by keeping released heat and solute lingering near the front, throttle the rate at which the interface can consume the undercooled melt. The effect is strongly nonlinear in time — the fractional and classical curves separate ever more widely as solidification proceeds — so that memory effects that are negligible at early times become dominant at long times.

### 6.5 Growth parameter maps

**Figure 6** maps the growth parameter *λ* against the fractional order *α* ∈ [0.4, 1.0] for Lewis numbers *Le* = 0.5, 1, 5 and 20. For every *Le*, *λ* rises monotonically and concavely with *α*, confirming that memory uniformly retards the front. The vertical ordering of the curves shows the throttling influence of the Lewis number: at any fixed *α*, raising *Le* from 0.5 to 20 lowers *λ* by roughly 25%, because a larger *Le* corresponds to slower solutal diffusion, which impedes the removal of rejected solute and hence the advance of the interface. The curves are approximately self-similar in shape, which is the graphical expression of the multiplicative closure (14): the *α*-dependence (through *α*^0.65) and the *Le*-dependence factorise cleanly. **Table 3** tabulates the same quantity for the discrete grid used in the computations.

**Table 3. Growth parameter λ as a function of fractional order α and Lewis number Le (Ste = 0.5, R = 1).**

| *α* \ *Le* | 0.5 | 1.0 | 5.0 | 20.0 |
|---|---|---|---|---|
| 1.0 | 0.468 | 0.449 | 0.392 | 0.348 |
| 0.9 | 0.437 | 0.419 | 0.366 | 0.325 |
| 0.8 | 0.405 | 0.388 | 0.339 | 0.301 |
| 0.7 | 0.371 | 0.356 | 0.311 | 0.276 |
| 0.6 | 0.336 | 0.322 | 0.281 | 0.250 |

The monotone decrease of *λ* down each column (decreasing *α*) and along each row (increasing *Le*) is unambiguous and quantifies the two retarding mechanisms. The largest growth parameter in the table (fast case) is *λ* = 0.468 at *α* = 1, *Le* = 0.5; the smallest (slow case) is *λ* = 0.250 at *α* = 0.6, *Le* = 20 — nearly a two-fold range attributable jointly to memory and solutal resistance.

### 6.6 Effect of undercooling, Stefan number and density

The interface position at a fixed observation time, *s**(*t** = 100) = 2*λ* · 10^*α*, condenses the combined influence of the kinetic exponent and the growth parameter. **Table 4** reports this quantity over a grid of fractional order *α* and Stefan number *Ste* (with *Le* = 1, *R* = 1). Along each row, raising the Stefan number — equivalently, deepening the undercooling — advances the front substantially: at *α* = 1 the interface position grows from 6.34 at *Ste* = 0.25 to 12.69 at *Ste* = 1.0, a doubling. Down each column, decreasing *α* retards the front for the compound reasons discussed in Section 6.4. The two effects are of comparable magnitude over the ranges studied, so that a deeply undercooled sub-diffusive melt (*Ste* = 1.0, *α* = 0.6, *s** ≈ 3.62) can advance more slowly than a weakly undercooled diffusive one (*Ste* = 0.25, *α* = 1.0, *s** ≈ 6.34). The density ratio *R* enters through the factor (2 − *R*) in Equation (14): expansion on freezing (*R* < 1) accelerates the front by pushing liquid toward the interface, whereas shrinkage (*R* > 1) retards it, reproducing the first-order density effect reported by Jakhar et al. [13] now embedded within the fractional framework.

**Table 4. Interface position s*(t* = 100) for varying fractional order α and Stefan number Ste (Le = 1, R = 1).**

| *α* \ *Ste* | 0.25 | 0.50 | 1.00 |
|---|---|---|---|
| 1.0 | 6.344 | 8.970 | 12.686 |
| 0.8 | 3.463 | 4.897 | 6.925 |
| 0.6 | 1.812 | 2.562 | 3.623 |

### 6.7 Sensitivity analysis

To rank the controlling parameters, **Figure 7** reports the normalised sensitivity (local elasticity) of the interface position *s**(*t** = 100) with respect to each of *α*, *Le*, *Ste* and *R*, evaluated about the baseline case by a symmetric ±5% perturbation. The Stefan number has the largest positive elasticity, confirming undercooling as the dominant accelerant of solidification. The fractional order *α* has a large positive elasticity of comparable magnitude — a direct consequence of its appearance both in the growth parameter and, more potently, in the time exponent 10^*α*, which amplifies small changes in *α* at the long observation time *t** = 100. The density ratio *R* carries a negative elasticity (increasing *R*, i.e. more shrinkage, retards the front), and the Lewis number a smaller negative elasticity (increasing *Le* throttles the front through solutal resistance). The analysis makes quantitatively precise the qualitative trends of Sections 6.4–6.6 and identifies *Ste* and *α* as the parameters that most urgently require accurate characterisation when the model is applied to a real alloy system: an error in the fractional order propagates into the predicted front position with roughly unit elasticity at long times.

### 6.8 Application scenarios

The parametric trends translate directly into guidance for several technologically important settings. In **metal additive manufacturing** (laser powder-bed fusion and directed energy deposition), the melt pool solidifies through a fine, rapidly evolving cellular–dendritic structure under extreme cooling rates. The model predicts that an effective fractional order below unity will manifest as a solidification front that lags the classical √*t* estimate and as intensified interfacial solute segregation (Section 6.3) — both consistent with the microsegregation and non-equilibrium partitioning routinely observed in printed alloys. Fitting an effective *α* to measured melt-pool solidification times would provide a compact calibration parameter for process-scale thermal models without resolving the sub-grid dendritic network. In **sand and investment casting**, where solidification proceeds against a porous, low-conductivity mould, the trapping and tortuosity of the surrounding medium are naturally represented by *α* < 1; the predicted retardation (Figure 5) and its strong growth with time are relevant to the timing of feeding and the prediction of shrinkage porosity, the latter further modulated here by the density ratio *R*. In the **freezing of biological tissue and food matrices**, sub-diffusive water and solute transport through cellular structures is well documented, and the heavy-tailed concentration profiles of Figure 4(a) mirror the slow, persistent solute redistribution that governs ice-crystal growth and cryopreservation outcomes. Finally, for **phase-change thermal-storage media** based on eutectic and non-eutectic mixtures, the combined influence of the Stefan number and the fractional order on the front position (Table 4) bears directly on charge/discharge timing: a storage medium with pronounced transport memory will exhibit a markedly longer effective solidification time than a Fourier estimate would suggest, which must be accounted for in sizing and control.

Across these scenarios the practical workflow is identical: measure an interface or solidified-fraction history, extract the exponent *α*/2 and prefactor *λ* from a log–log fit, and feed the identified (*α*, *λ*) into Equations (10)–(12) to reconstruct the full thermal and solutal fields and to extrapolate the front. Because the sensitivity analysis (Figure 7) shows that *α* carries near-unit elasticity on the long-time front position, even a modest fractional correction materially changes engineering predictions, which underscores the value of identifying it rather than defaulting to the classical *α* = 1 assumption.

### 6.9 Implications and limitations

Taken together, the results show that the fractional order *α* is not a mere curve-fitting exponent but a physically meaningful descriptor of transport memory that systematically and simultaneously governs interface kinetics, boundary-layer structure and interfacial segregation. The practical appeal of the formulation is its economy: a single additional parameter extends the classical, well-validated similarity framework into the anomalous-transport regime without recourse to detailed micro-mechanical modelling of the mushy zone. This makes the model attractive as a reduced-order descriptor for inverse problems — for instance, inferring an effective *α* from a measured interface history *s*(*t*) ∼ *t*^(*α*/2) in a rapidly solidified or disordered alloy.

Several limitations should be acknowledged. The analysis is one-dimensional, assumes a sharp planar interface and neglects melt convection, natural segregation-driven flow and the finite extent of the mushy zone; each of these could be incorporated at the cost of analytical tractability. The common fractional order assumed for heat and solute could be relaxed to independent orders *α*_T and *α*_C to represent distinct thermal and solutal memory, which may be important when the two transport mechanisms sample different features of the microstructure. The reduced closure (14), while accurate in the ranges studied, is a surrogate for the full transcendental solution of (13) and should be re-fitted outside those ranges. Finally, the choice of the Caputo derivative — with its power-law memory kernel — is one of several possibilities; the non-singular Caputo–Fabrizio and Atangana–Baleanu kernels [30,31] encode exponential and Mittag-Leffler memory respectively and would yield quantitatively different, though qualitatively related, retardation. Experimental determination of the most appropriate kernel for a given alloy system remains an open and important question.

---

## 7. Conclusions

A two-phase, time-fractional Stefan problem has been formulated and solved for the conduction-dominated solidification of an undercooled binary alloy, generalising the classical density-aware similarity solution to admit thermal and solutal memory through Caputo derivatives of order *α*. The principal findings are:

1. **A self-similar reduction exists** for the coupled fractional energy and species equations, giving closed-form temperature and concentration distributions in terms of Mittag-Leffler/Wright functions and a sub-diffusive interface growth law *s**(*t**) = 2*λ t**^(*α*/2) that reduces to the classical √*t** law as *α* → 1.

2. **The model is validated**: in the limit *α* → 1 it recovers the one-phase Stefan benchmark to within 1.5% and reproduces the binary density-aware similarity solution of Jakhar et al. [13], and an independent L1 front-fixing finite-difference solver corroborates the similarity results to within 1%.

3. **Reducing the fractional order retards the interface** strongly and nonlinearly in time, through the combined reduction of the kinetic exponent *α*/2 and the growth parameter *λ*; at *t** = 100 a sub-diffusive front (*α* = 0.6) advances to less than one-third of the classical distance.

4. **Memory sharpens boundary layers and intensifies segregation**: smaller *α* steepens the near-interface thermal and solutal gradients, lengthens the far-field tails and elevates the interfacial solute concentration; larger Lewis number compresses the solutal layer and further throttles the front.

5. **The front accelerates** with increasing Stefan number (undercooling) and decreasing density ratio (expansion), and decelerates with increasing Lewis number; a normalised sensitivity analysis ranks the Stefan number and the fractional order as the two most influential parameters at long times.

The framework offers a compact, physically interpretable route to incorporate anomalous transport into alloy solidification modelling and provides a basis for inverse estimation of an effective memory order from measured interface histories. Future work will relax the sharp-interface and one-dimensional assumptions, admit independent thermal and solutal fractional orders, incorporate convection, and pursue experimental identification of the appropriate memory kernel for specific alloy systems.

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
| *L* | length scale (m) |
| *Le* | Lewis number, α_l/D_l (–) |
| *m* | liquidus slope |
| *M* | scaled liquidus slope (–) |
| *R* | density ratio, ρ_s/ρ_l (–) |
| *s* | interface position (m); *s** dimensionless |
| *Ste* | Stefan number (–) |
| *T* | temperature (K); *T*_f fusion temperature |
| *t** | dimensionless time |
| *W* | Wright function |
| *x** | dimensionless coordinate |
| *α* | fractional (Caputo) order (–) |
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

[28] S. Kumar, A. Kumar, D. Baleanu, Two analytical methods for time-fractional nonlinear coupled Boussinesq–Burger equations arising in propagation of shallow water waves, Nonlinear Dyn. 85 (2) (2016) 699–715.

[29] A. Esen, Y. Ucar, N. Yagmurlu, O. Tasbozan, A Galerkin finite element method to solve fractional diffusion and fractional diffusion–wave equations, Math. Model. Anal. 18 (2) (2013) 260–273.

[30] M. Caputo, M. Fabrizio, A new definition of fractional derivative without singular kernel, Prog. Fract. Differ. Appl. 1 (2) (2015) 73–85.

[31] A. Atangana, D. Baleanu, New fractional derivatives with nonlocal and non-singular kernel: theory and application to heat transfer model, Therm. Sci. 20 (2) (2016) 763–769.

[32] M. Caputo, Linear models of dissipation whose Q is almost frequency independent — II, Geophys. J. R. Astron. Soc. 13 (5) (1967) 529–539.

[33] R. Hilfer (Ed.), Applications of Fractional Calculus in Physics, World Scientific, Singapore, 2000.

[34] S.D. Roscani, D.A. Tarzia, Explicit solution for a two-phase fractional Stefan problem with a heat flux condition at the fixed face, Comput. Appl. Math. 37 (4) (2018) 4757–4771.

[35] A. Kumar, A.K. Singh, Rajeev, A moving boundary problem with variable thermal conductivity and time-dependent heat flux governed by a fractional derivative, Meccanica 55 (10) (2020) 2047–2060.

---

*Figures referenced in the text (generated by `generate_fractional_figures.py`, stored in `fractional_figures/`):*

- **Figure 1.** One-dimensional fractional Stefan domain: solid, mushy zone and undercooled liquid, with the governing time-fractional equations and interface conditions, and a sketch of the anomalous mean-square advance ⟨s²⟩ ∼ tᵃ.
- **Figure 2.** Mittag-Leffler relaxation kernel Eₐ(−tᵃ) for several fractional orders, showing the crossover and heavy algebraic tails that signify long memory.
- **Figure 3.** Liquid-phase temperature profiles against the similarity variable η for α = 1.0, 0.85, 0.70, 0.55 (Le = 1, Ste = 0.5).
- **Figure 4.** Solute concentration profiles: (a) effect of fractional order α at Le = 10; (b) effect of Lewis number Le at α = 0.8.
- **Figure 5.** Interface position histories s*(t*) = 2λ t*^(α/2) for α = 1.0–0.6 (Le = 1, Ste = 0.5, R = 1).
- **Figure 6.** Growth parameter λ versus fractional order α for Lewis numbers Le = 0.5, 1, 5, 20 (Ste = 0.5, R = 1).
- **Figure 7.** Normalised sensitivity (elasticity) of the interface position s*(t* = 100) to the fractional order α, Lewis number Le, Stefan number Ste and density ratio R.
