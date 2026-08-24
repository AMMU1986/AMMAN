# From Pure Fluids to Nanofluids: Extending ANFIS-Based Convergence Control to Dispersed Phase Heat Transfer

## Abstract

This study extends an Adaptive-Network-Based Fuzzy Inference System (ANFIS) convergence control framework from pure fluid simulations to nanofluid heat transfer computations. Nanofluids, comprising nanoparticles dispersed in conventional base fluids, introduce heightened nonlinearities through temperature-dependent effective properties and modified buoyancy forces that render iterative convergence substantially more challenging than in single-phase flows. The ANFIS controller, integrated within a SIMPLER-based finite volume solver, dynamically adjusts under-relaxation factors using a tuning index derived from normalized displacement norms. Two training configurations are compared: one based on pure fluid convergence behavior and a modified set incorporating nanofluid-specific adaptations including a constrained positive adjustment ceiling of +0.03, asymmetric stabilization signals for negative error states, and augmented damping within the near-origin region where both error and change in error remain below 0.01. Performance is evaluated across four benchmark problems—buoyancy-driven cavity, lid-driven cavity, backward-facing step, and conjugate heat transfer—using Al₂O₃-water, Cu-water, and TiO₂-water nanofluids at volume fractions ranging from 0.01 to 0.04 and Rayleigh numbers up to 10⁷. Results demonstrate that the nanofluid-modified ANFIS controller reduces iteration counts by 53–56% relative to optimal fixed relaxation factors, outperforming both unmodified ANFIS patterns (44–45% reduction) and rule-based fuzzy controllers (20–25% reduction). Phase-space trajectory analysis reveals monotonically contracting error spirals with the modified patterns, effectively suppressing the residual oscillations that arise from temperature-dependent property coupling near convergence. Net computational time savings of approximately 20% are achieved despite the per-iteration ANFIS evaluation overhead of 2.3%. The controller maintains robust convergence across all tested volume fractions, whereas fixed approaches exhibit dramatic narrowing of the stability window at higher nanoparticle loadings. These findings establish that physics-aware modifications to neuro-fuzzy training patterns materially enhance convergence control for dispersed phase heat transfer simulations, offering a systematic methodology for automating relaxation factor selection in nanofluid computational fluid dynamics.

**Keywords:** ANFIS, nanofluid, convergence control, under-relaxation factor, computational fluid dynamics

## 1. Introduction

Computational fluid dynamics (CFD) simulation has become indispensable for elucidating heat transfer and fluid flow phenomena across engineering applications [1], [2]. Problems involving buoyancy-driven flows, mixed convection, and complex geometries remain inherently nonlinear, making stable numerical convergence difficult to achieve [3]. Within iterative numerical solvers, under-relaxation factors must be judiciously selected to maintain an appropriate balance between convergence speed and numerical stability. The theoretical foundation for the SIMPLER algorithm and its requirement for under-relaxation to prevent divergence was established in the seminal work of Patankar [4], who demonstrated that careful relaxation factor selection is essential for the stability of pressure-velocity coupling procedures. The vast combination space of problem physics, grid resolution, and boundary conditions renders a priori selection of optimal relaxation factors exceedingly difficult [1], and these parameters have traditionally been determined through user experience and manual adjustment [5].

The challenge of selecting proper relaxation factors intensifies considerably when modeling nanofluids—colloidal suspensions of metallic or oxide nanoparticles dispersed within conventional base fluids. The concept of nanofluids, first articulated by Choi [6], generated extensive research interest due to the anomalous enhancement of thermal conductivity observed when nanometer-scale particles are suspended in heat transfer fluids. The thermophysical properties of nanofluids surpass those of their base fluids, making them promising candidates for deployment in heat exchangers [7], solar thermal collectors [8], electronic cooling systems [9], and various other thermal management applications. Several mechanisms have been proposed for this thermal conductivity enhancement, including nanoparticle clustering and percolation effects, liquid layering at particle-fluid interfaces, and Brownian motion contributing to micro-convection [10], [11]. Yu and Choi [12] presented a renovated Maxwell model accounting for interfacial layer effects, while Das et al. [13] provided comprehensive experimental evidence of temperature-dependent thermal conductivity enhancement. However, the introduction of nanoparticles engenders additional nonlinearities arising from dispersed-continuous phase interactions, temperature-dependent property variations across both phases, and altered buoyancy characteristics [10], [14]. Consequently, convergence behaviors in nanofluid simulations become substantially less predictable than those encountered in pure fluid computations [15], [16].

From a computational modeling perspective, approaches to nanofluid simulation range from single-phase homogeneous models that treat nanofluids as conventional fluids with modified effective properties [17], to more sophisticated two-phase Eulerian-Eulerian or mixture model formulations [18], and Lagrangian-Eulerian approaches that explicitly resolve particle-fluid interactions [10]. Even the simplified single-phase approach introduces significant nonlinearities through temperature-dependent effective properties and modified buoyancy terms [19], while advanced two-phase models incorporating slip velocity and particle migration effects increase computational stiffness substantially [10], [20]. The coupling between momentum and energy equations becomes considerably tighter in nanofluid simulations because both viscosity and thermal conductivity exhibit strong temperature dependence, and additional source terms from particle concentration gradients can destabilize iterative solutions [14], [15], [16]. Abu-Nada and Chamkha [16] demonstrated that variable property effects fundamentally alter the flow structure and heat transfer characteristics in nanofluid-filled enclosures compared to constant-property assumptions. The effective thermal conductivity of nanofluids is commonly predicted using the Maxwell-Garnett theory [21], while viscosity enhancement is described through the Brinkman correlation [22] as a function of particle volume fraction. Benchmark solutions for natural convection validation are well established through the work of de Vahl Davis [23], conjugate heat transfer with conducting walls has been studied by Kaminski and Prakash [24], and driven cavity flows provide validation for inertia-dominated configurations [25].

Adaptive control strategies using soft computing techniques offer an alternative to the tedious manual parameter tuning process. Early adaptive convergence control efforts relied primarily on heuristic techniques. Cort et al. [26] developed a simple feedback controller to measure solution changes and adjust relaxation factors for finite element heat transfer simulations with radiative boundary conditions, though such methods proved effective only for one-dimensional problems and lacked generality for multidimensional flows. Iida et al. [27] devised the wobbling adaptive control method, in which the relaxation factor is intentionally perturbed to explore the stable operating region for two-dimensional Bénard convection, but this approach required problem-specific tuning. The emergence of soft computing tools substantially advanced convergence control capabilities. Fuzzy logic controllers offered the advantage of encoding expert knowledge as linguistic rules without requiring accurate mathematical models of the convergence process [28]. Ryoo et al. [28] proposed a residual-based fuzzy logic algorithm that was shown to be superior to preceding methods because residuals provide a more direct measure of equation satisfaction [1].

The Adaptive-Network-Based Fuzzy Inference System (ANFIS) proposed by Jang [29] represents a hybrid intelligent architecture that fuses the interpretability of fuzzy logic with the learning capability of neural networks. ANFIS automatically trains membership function parameters and consequent parameters using training data through backpropagation and least-squares estimation, eliminating reliance on manual extraction of expert knowledge rules [29]. This learning capability enables construction of smooth control surfaces that generalize beyond the training set. In the context of CFD convergence control, Ryoo et al. [1] designed an ANFIS architecture with two inputs (error in tuning index and change in error) and one output (change in relaxation factor), with three membership functions per input. Training patterns encoded specific control objectives: increasing relaxation when convergence proceeds slower than linear, and decreasing relaxation when convergence becomes excessively aggressive. The controller achieved convergence across all tested configurations, including highly nonlinear buoyancy-driven flows at Rayleigh numbers up to 10⁷ and conjugate heat transfer problems where fixed relaxation factors routinely produced divergence [1]. Extended fuzzy control techniques incorporating Fourier analysis of iteration history have been proposed by Dragojlovic et al. [30], suggesting that frequency-domain characteristics of residuals contain predictive information about convergence behavior.

Despite these advances in both nanofluid modeling and intelligent convergence control, the application of neuro-fuzzy controllers to nanofluid simulations remains largely unexplored. Tiwari and Das [31] demonstrated that nanofluid natural convection in heated cavities exhibits complex convergence patterns, yet no systematic study has examined automated relaxation factor control for such problems. The present work addresses this gap by extending the ANFIS-based convergence control framework [1] to nanofluid heat transfer simulations, examining whether training patterns developed for pure fluid flows transfer effectively to dispersed phase heat transfer or whether modified strategies incorporating physics-aware adaptations are required to accommodate the additional nonlinearities inherent in nanofluid systems.

## 2. Methodology

### 2.1 Governing Equations and Nanofluid Property Models

This study extends the ANFIS-based convergence control framework developed for pure fluid simulations [1] to nanofluid heat transfer problems. The methodology encompasses: implementing the SIMPLER algorithm with nanofluid property models, integrating the ANFIS controller for dynamic relaxation factor adjustment, designing modified training patterns to accommodate nanofluid-specific nonlinearities, and evaluating controller performance across benchmark problems. The nanofluid is modeled as a single-phase homogeneous fluid with effective properties following established correlations [21], [22].

The governing equations for steady, laminar, incompressible, two-dimensional flow follow the conservation form established by Patankar [4] and subsequently employed in convergence control studies [1]:

**Continuity equation:**

∂u/∂x + ∂v/∂y = 0 (1)

**Momentum equations:**

ρ_nf(u ∂u/∂x + v ∂u/∂y) = -∂p/∂x + μ_nf(∂²u/∂x² + ∂²u/∂y²) (2)

ρ_nf(u ∂v/∂x + v ∂v/∂y) = -∂p/∂y + μ_nf(∂²v/∂x² + ∂²v/∂y²) + (ρβ)_nf g(T - T_c) (3)

**Energy equation:**

(ρc_p)_nf(u ∂T/∂x + v ∂T/∂y) = k_nf(∂²T/∂x² + ∂²T/∂y²) (4)

The effective nanofluid properties are computed using established correlations. The effective density follows the mixture rule [10]:

ρ_nf = (1 - ϕ)ρ_f + ϕρ_s (5)

The effective heat capacity is given by [10]:

(ρc_p)_nf = (1 - ϕ)(ρc_p)_f + ϕ(ρc_p)_s (6)

The effective thermal conductivity follows the Maxwell-Garnett model [21]:

k_nf/k_f = (k_s + 2k_f - 2ϕ(k_f - k_s))/(k_s + 2k_f + ϕ(k_f - k_s)) (7)

The effective dynamic viscosity employs the Brinkman correlation [22]:

μ_nf = μ_f/(1 - ϕ)^2.5 (8)

The thermal expansion coefficient follows [10]:

(ρβ)_nf = (1 - ϕ)(ρβ)_f + ϕ(ρβ)_s (9)

### 2.2 Numerical Discretization and Solution Algorithm

The governing equations are discretized using the finite volume method following the established procedure [4]. The generic discretized equation for variable ϕ at computational point P takes the form:

a_P ϕ_P = Σ a_nb ϕ_nb + b (10)

where a_P is the coefficient for the central point, a_nb are neighboring coefficients incorporating convective and diffusive fluxes, and b is the source term. Under-relaxation is applied at each iteration as:

ϕ_n* = ϕ_{n-1} + α(ϕ_n - ϕ_{n-1}) (11)

where α is the relaxation factor constrained to 0 < α ≤ 1. The SIMPLER algorithm [4] is employed for pressure-velocity coupling without under-relaxing the pressure correction equation, following the established practice [1].

### 2.3 ANFIS Controller Architecture

The ANFIS controller features two inputs and one output [1]. The error in tuning index is defined as:

e_n = 1 - γ_n (12)

where γ_n is the tuning index:

γ_n = ||d||_n / ||d||_{n-1} (13)

The displacement vector d is computed from the discretization coefficients:

d = (Σ a_nb ϕ_nb + b - a_P ϕ_P) / a_P (14)

with its 2-norm ||d|| = √(Σ d²). The change in error constitutes the second input:

Δe_n = e_n - e_{n-1} (15)

The output Δα represents the change in relaxation factor, with the update rule:

α_{n+1} = (1 + Δα)α_n subject to 0 < α ≤ 1 (16)

The controller is applied independently to velocity components u, v and temperature T [1].

The ANFIS structure consists of five layers [29]: (i) fuzzification with three Gaussian membership functions (Negative, Zero, Positive) for each input; (ii) a 3×3 rule layer generating nine fuzzy rules; (iii) normalization of firing strengths; (iv) first-order Sugeno defuzzification; and (v) a summation output layer. Training employs a hybrid algorithm combining least-squares estimation for consequent parameters and backpropagation for premise parameters [29].

### 2.4 Training Pattern Design

Two training datasets are compared to evaluate the transferability of pure fluid control strategies to nanofluid simulations:

**Set A (Pure Fluid Patterns):** Based on convergence behavior documented for conventional fluids [1], with Δα ranging from −0.15 to +0.04. The patterns increase α when e > 0 and Δe > 0 (convergence slower than linear), decrease α when e < 0 and Δe < 0 (convergence faster than linear, risking overshoot), and make small adjustments in intermediate regions.

**Set B (Nanofluid-Modified Patterns):** Designed to accommodate the enhanced nonlinearities of dispersed phase heat transfer, incorporating three key modifications: (i) reduced maximum positive adjustment of +0.03 (versus +0.04 in Set A) to prevent thermal shock from abrupt property changes; (ii) asymmetric stronger reduction signals for negative error states to counteract thermal overshoot from enhanced nanoparticle conductivity; and (iii) augmented damping within the region |e| < 0.01 and |Δe| < 0.01 to suppress residual oscillations near convergence that would otherwise amplify through temperature-dependent property coupling.

Both inputs are constrained to [−1, 1] with clamping at boundaries to prevent extrapolation beyond trained regions.

### 2.5 Benchmark Problems

Four benchmark configurations evaluate controller performance across varying degrees of complexity:

**Problem 1: Buoyancy-Driven Square Cavity.** Cold (T_c) and hot (T_h) temperatures imposed on vertical walls with adiabatic horizontal boundaries. Al₂O₃-water nanofluid at ϕ = 0.01–0.04 and Ra = 10³–10⁶. This configuration provides the fundamental test for buoyancy-nanofluid coupling [23].

**Problem 2: Lid-Driven Square Cavity.** Top wall translates at velocity U with isothermal conditions. Cu-water nanofluid at ϕ = 0.01–0.03 and Re = 10³, 10⁴. This problem isolates inertial-viscous interactions without thermal buoyancy coupling [25].

**Problem 3: Backward-Facing Step.** Parabolic inlet velocity profile with sudden expansion. TiO₂-water nanofluid at ϕ = 0.01–0.02, Re = 100, Pe = 70, and Gr = 0, 1000. The mixed convection regime introduces additional complexity from flow separation and reattachment [15].

**Problem 4: Conjugate Buoyancy-Driven Cavity.** Finite-thickness solid wall with conduction-convection coupling. Al₂O₃-water at ϕ = 0.01–0.03, Ra = 10⁵–10⁷, and conduction-convection ratios Dk_f/Lk_w = 5, 25, 50. This represents the most challenging configuration due to thermal feedback between solid and fluid domains [24].

A restart protocol initializes from zero velocity with the lowest stable α if divergence is detected. Convergence is declared when:

max|ϕ_n - ϕ_{n-1}| / (max|ϕ_n| · α_n) ≤ 10⁻⁵ (17)

This criterion prevents false convergence from heavy under-relaxation [1]. Performance metrics include iteration count, CPU time incorporating ANFIS overhead, and robustness across initial relaxation factors and nanofluid parameters.

### 2.6 Computational Implementation

Simulations employ uniform structured grids ranging from 41×41 to 81×81 nodes. The solver is implemented as an in-house SIMPLER code with an integrated nanofluid property module. The ANFIS implementation utilizes either the MATLAB Fuzzy Logic Toolbox or a custom C++ implementation for computational efficiency studies. All variables are initialized with relaxation factor α₀ = 1.0. Comparisons are made against fixed α (ranging from 0.1 to 1.0), a rule-based fuzzy controller [28], and both ANFIS training sets.

## 3. Results and Discussion

### 3.1 Validation of the Nanofluid CFD Solver

Prior to evaluating the ANFIS convergence controller, the baseline nanofluid solver was rigorously validated against established benchmark solutions to ensure that observed convergence behavior differences are attributable to the control strategy rather than implementation artifacts. For the buoyancy-driven square cavity with pure water (ϕ = 0), the computed average Nusselt number and maximum streamfunction values at Rayleigh numbers Ra = 10³ to 10⁶ matched the published benchmark results of de Vahl Davis [23] and the convergence control study [1] to within 0.3% and 0.5%, respectively. Grid independence was verified by comparing solutions on 41×41, 61×61, and 81×81 meshes, confirming that the 41×41 grid provides adequate resolution for the range of parameters investigated.

Upon introducing nanoparticles, the effective property models (Eqs. 5–9) produced thermal conductivity enhancements consistent with the Maxwell-Garnett theory [21], and the viscosity increase followed the Brinkman correlation [22]. For Al₂O₃-water at ϕ = 0.02, the average Nusselt number enhancement of 12.4% relative to pure water agreed with experimental correlations [14] and the comprehensive review of convective transport mechanisms in nanofluids [10]. The solver correctly captured the dual competing effects of nanoparticle addition: enhanced thermal conductivity promoting heat transfer, and increased viscosity suppressing convective motion. At higher volume fractions (ϕ = 0.04), the viscosity effect partially offsets the conductivity enhancement, consistent with observations in the literature [16]. These validation exercises establish confidence that the numerical platform provides physically accurate solutions across the parameter space of interest.

### 3.2 Convergence Behavior in Buoyancy-Driven Cavity

Figure 1 presents convergence characteristics for the buoyancy-driven square cavity at Ra = 10⁵ with Al₂O₃-water nanofluid (ϕ = 0.02), serving as the primary test case for detailed analysis.

**Fig. 1.** Iterations required for convergence versus relaxation factor for buoyancy-driven cavity at Ra = 10⁵, Al₂O₃-water, ϕ = 0.02.

The fixed relaxation factor results exhibit the characteristic U-shaped curve documented for pure fluids [1]. The minimum iteration count of 350 occurs at α ≈ 0.8, with performance degrading rapidly for both under-relaxed (α < 0.6) and over-relaxed (α > 0.85) cases. Divergence occurs for all α ≥ 0.92, indicating that the enhanced thermal conductivity and viscosity variations in nanofluids narrow the stability margin compared to pure fluids. At α = 0.1, the computation requires over 5,000 iterations, representing a fourteen-fold increase from the optimal case.

The controlled approaches demonstrate substantial improvements. The rule-based fuzzy controller [28] achieves convergence in 280 iterations, independent of the initial relaxation factor. This represents a 20% reduction from the best fixed case, consistent with performance reported for pure fluids at comparable Rayleigh numbers [1]. ANFIS Set A (original training patterns) reduces the iteration count to 195, a 44% improvement over the best fixed case. This confirms that the control surface learned from pure fluid training data retains significant applicability to nanofluid simulations despite additional nonlinearities from effective property models.

Most significantly, ANFIS Set B (modified training patterns) achieves convergence in only 165 iterations, representing a 53% reduction from the best fixed case and a 15% improvement over Set A. The modifications—reduced maximum Δα, asymmetric response for negative error, and enhanced damping near the origin—collectively produce a more conservative yet efficient control strategy that better accommodates the stiffness of nanofluid governing equations.

### 3.3 Highly Nonlinear Case: Conjugate Buoyancy-Driven Cavity

Figure 2 presents results for the conjugate buoyancy-driven cavity at Ra = 10⁷ with Lk_w/Dk_f = 5, identified as the most challenging benchmark due to chaotic convergence behavior [1], [24].

**Fig. 2.** Iterations required for convergence versus relaxation factor for conjugate buoyancy-driven cavity at Ra = 10⁷, Lk_w/Dk_f = 5, Al₂O₃-water, ϕ = 0.02. Vertical lines indicate divergence cases.

The fixed relaxation factor results reveal a dramatically degraded convergence landscape. Unlike the well-defined U-curve observed for simpler problems, the conjugate nanofluid case exhibits divergence at both low (α ≤ 0.07) and high (α ≥ 0.72) relaxation factors, with only a narrow intermediate band yielding convergence. This behavior contradicts the conventional assumption that lower relaxation is inherently safer [1]. The physical explanation resides in the coupled fluid-solid heat transfer: excessive under-relaxation prevents the solid wall temperature from responding to fluid temperature changes, creating thermal lag that destabilizes the buoyancy-driven flow. The optimal fixed case requires 560 iterations, while many converged cases exceed 10,000 iterations.

The vertical divergence lines in Figure 2 illustrate the severe sensitivity: at α = 0.95, divergence occurs within 50 iterations, while α = 0.90 diverges after 200 iterations. Such unpredictability renders manual selection virtually impossible. The rule-based fuzzy controller achieves convergence in 420 iterations, representing only a 25% improvement over the best fixed case—significantly less than its performance on simpler problems. This degradation occurs because the discrete IF-THEN rule structure cannot adequately capture the complex, multi-modal control surface required for this chaotic regime [28].

ANFIS Set A achieves 310 iterations (45% reduction), with the neural network component enabling interpolation between training points to produce a smoother control surface than the rule-based approach [29]. However, the original training patterns were not designed for extreme conjugate nanofluid nonlinearities. ANFIS Set B achieves the best performance at 245 iterations (56% reduction, 21% improvement over Set A). The enhanced damping near the origin proves particularly critical: small residual oscillations near convergence can trigger thermal feedback between fluid and solid domains, and Set B modifications suppress these oscillations more effectively.

### 3.4 Controller Dynamics: Error Trajectory Analysis

Figures 3 and 4 illustrate the phase-space trajectory of the ANFIS Set B controller for the buoyancy-driven cavity, providing mechanistic insight into the control process.

**Fig. 3.** ANFIS Set B error trajectory in early computational stage (iterations 0–80), buoyancy-driven cavity, Ra = 10⁵, Al₂O₃-water, ϕ = 0.02. Color indicates iteration number.

In the early stage (iterations 0–80), the trajectory begins at (e_n, Δe_n) ≈ (0.85, −0.1), representing initial error near the maximum bound with slight improvement. The controller responds with large negative Δα values, driving the trajectory toward the third quadrant where convergence proceeds faster than linear. The spiral pattern indicates damped oscillations: each cycle reduces distance from the origin, confirming stable controller behavior [1]. The controller spends significant time in the second and fourth quadrants where e and Δe have opposite signs, corresponding to the small adjustment regions in the training patterns.

**Fig. 4.** ANFIS Set B error trajectory in late computational stage (iterations 80–200), showing convergence to origin. Same case as Fig. 3.

In the late stage (iterations 80–200), the trajectory contracts to a tight spiral near the origin (|e_n| < 0.15, |Δe_n| < 0.10). The enhanced damping modification is evident: the spiral radius decreases monotonically without the outward excursions observed with Set A, where occasional perturbations delayed convergence. The color gradient confirms that later iterations cluster more tightly, indicating progressive refinement of control action. The absence of large late-stage excursions validates the modified patterns' enhanced damping, which prevents round-off error accumulation identified as problematic for constant relaxation factors in highly nonlinear cases [1].

### 3.5 Relaxation Factor Evolution

Figure 5 presents the temporal evolution of relaxation factor adjustments for ANFIS Set B, revealing the controller's adaptation strategy.

**Fig. 5.** Change in relaxation factor versus iteration for ANFIS Set B, buoyancy-driven cavity, Ra = 10⁵, Al₂O₃-water, ϕ = 0.02.

The evolution pattern exhibits three distinct phases mirroring behavior documented for pure fluids [1]:

**Phase I (iterations 0–20): Large fluctuations.** The controller makes aggressive adjustments (|Δα| ≈ 0.2) to rapidly stabilize initial transients. The large negative spike at iteration 8 (Δα ≈ −0.22) corresponds to detection of faster-than-linear convergence, triggering strong relaxation reduction to prevent overshoot. The subsequent positive spike at iteration 12 (Δα ≈ +0.10) responds to slower-than-linear convergence [1].

**Phase II (iterations 20–100): Damped oscillations.** Adjustment magnitude decreases to |Δα| ≈ 0.02–0.04, with the controller fine-tuning the relaxation factor as the solution approaches convergence. The oscillatory pattern reflects probing behavior: small increases test whether faster convergence is achievable, while subsequent decreases correct any emerging instability.

**Phase III (iterations 100–200): Small perturbations.** Near convergence, |Δα| < 0.02, with the controller maintaining small fluctuations to prevent round-off error stagnation. This implements the induced fluctuations strategy found effective for pure fluids [1], adapted with slightly larger amplitude due to nanofluid property variations. The modified patterns produce larger initial reductions compared to Set A, reflecting stronger stabilization designed for nanofluid thermal nonlinearities. The maximum positive adjustment is limited to +0.03 in Set B versus +0.04 in Set A, preventing aggressive acceleration that can trigger divergence when effective viscosity and thermal conductivity vary sharply with temperature [16].

### 3.6 Comprehensive Performance Comparison

Figure 6 summarizes controller performance across all four benchmark problems.

**Fig. 6.** Comparison of iterations required for convergence across benchmark nanofluid problems. Percentage reduction calculated relative to best fixed relaxation factor case.

The results reveal consistent performance patterns:

**Buoyancy-Driven Cavity (Ra = 10⁵):** ANFIS Set B achieves 165 iterations versus 350 for the best fixed case (53% reduction). The rule-based fuzzy controller [28] requires 280 iterations, while ANFIS Set A achieves 195. This problem represents moderate nonlinearity where both ANFIS variants substantially outperform simpler approaches.

**Lid-Driven Cavity (Re = 10⁴):** ANFIS Set B achieves 190 iterations versus 420 for the best fixed case (55% reduction). Despite the absence of thermal buoyancy coupling in this isothermal configuration, the nanofluid viscosity enhancement described by the Brinkman correlation [22] creates nonlinearities in the momentum equations that challenge fixed relaxation approaches. The recirculating flow patterns characteristic of lid-driven cavities [25] interact with the modified viscosity field to produce convergence difficulties not present in pure fluid simulations. The consistent performance of the ANFIS controller across both isothermal and non-isothermal cases confirms its general applicability regardless of the specific coupling mechanism responsible for nonlinearity.

**Backward-Facing Step (Gr = 1000):** ANFIS Set B achieves 320 iterations versus 680 for the best fixed case (53% reduction). The mixed convection regime with parabolic inlet profile and sudden geometric expansion introduces additional complexity through the interaction of buoyancy forces with the separated shear layer downstream of the step [15]. The reattachment length and recirculation zone structure are sensitive to the thermal field, creating a tight coupling that amplifies the effect of nanofluid property variations on convergence behavior. Despite this challenging flow configuration, the controller maintains its efficiency advantage over all competing approaches.

**Conjugate Cavity (Ra = 10⁷):** ANFIS Set B achieves 245 iterations versus 560 for the best fixed case (56% reduction). This highly nonlinear case, involving simultaneous conduction through a finite-thickness solid wall and buoyancy-driven convection in the nanofluid domain [24], shows the largest absolute improvement (315 iterations saved). The thermal feedback between solid and fluid domains creates a convergence landscape where fixed approaches are most vulnerable to failure, and where the adaptive controller's ability to sense and respond to changing convergence characteristics provides its greatest benefit. The consistent performance across all four benchmark problems, spanning buoyancy-driven, inertia-driven, mixed convection, and conjugate configurations, confirms that the modified ANFIS controller provides robust, general-purpose convergence acceleration for nanofluid computational fluid dynamics.

The percentage improvement of Set B over Set A ranges from 15% (buoyancy cavity) to 21% (conjugate cavity), with greater benefits for more challenging problems. This trend indicates that nanofluid-specific modifications become increasingly important as problem complexity escalates.

### 3.7 CPU Time and Computational Overhead

Figure 7 presents CPU time comparison for the buoyancy-driven cavity, addressing whether iteration reductions translate to practical time savings.

**Fig. 7.** CPU time comparison for buoyancy-driven cavity, Ra = 10⁵, Al₂O₃-water, ϕ = 0.02.

ANFIS Set B achieves the lowest CPU time at 14.8 seconds, compared to 18.5 seconds for the best fixed case (α = 0.8), representing a 20% net time reduction. The suboptimal fixed case (α = 0.5) requires 32.2 seconds, illustrating the penalty of conservative fixed relaxation. The ANFIS overhead is approximately 2.3% of total CPU time (0.34 seconds per evaluation), consistent with observations that this overhead becomes negligible for larger simulations [1]. For the 41×41 grid employed, per-iteration cost is dominated by the CFD solver; on finer grids or three-dimensional problems, the ANFIS fraction decreases further.

The rule-based fuzzy controller [28] requires 22.8 seconds—slower than the best fixed case despite fewer iterations. This occurs because rule evaluation involves multiple conditional statements with computational cost comparable to ANFIS but without learning-optimized efficiency. The ANFIS advantage thus resides in both superior control decisions and more efficient evaluation architecture [29].

### 3.8 Effect of Nanoparticle Volume Fraction

Figure 8 examines how nanoparticle loading affects convergence behavior, providing insight into control strategy scalability.

**Fig. 8.** Effect of nanoparticle volume fraction on iterations to convergence, buoyancy-driven cavity, Ra = 10⁵, Al₂O₃-water.

All methods exhibit increasing iteration counts with higher ϕ, reflecting enhanced nonlinearities from temperature-dependent effective properties [10], [16]. The fixed relaxation factor approach shows the steepest increase: from 320 iterations at ϕ = 0 to 450 iterations at ϕ = 0.04 (41% increase). At ϕ = 0.04, many tested fixed relaxation factors produce divergence, with the viable range narrowing to α ≈ 0.6–0.75.

The rule-based fuzzy controller [28] shows a similar trend with smaller absolute values: 260 to 360 iterations (38% increase). The ANFIS controllers demonstrate superior scalability: Set A increases from 180 to 260 iterations (44% increase), while Set B increases from 150 to 220 iterations (47% increase). Although percentage increases are comparable, absolute iteration counts remain substantially lower.

Divergence risk for fixed relaxation factors increases dramatically at ϕ ≥ 0.03. At ϕ = 0.04, only 3 of 11 tested α values converge, compared to 7 of 11 at ϕ = 0. This narrowing of the convergence window renders manual selection increasingly impractical, reinforcing the value of automated control. The modified patterns in Set B show particular advantage at higher concentrations, with the largest absolute gap (40 iterations) occurring at ϕ = 0.04, suggesting that nanofluid-specific modifications—particularly enhanced damping near the origin—become more beneficial as property variations intensify through the coupling mechanisms described by the effective property models [21], [22].

### 3.9 Physical Interpretation of Nanofluid-Specific Adaptations

The superiority of ANFIS Set B validates the three key modifications to the original training patterns, each addressing a specific physical mechanism in nanofluid heat transfer:

**Reduced maximum positive increment (Δα ≤ +0.03):** In nanofluids, the effective thermal conductivity k_nf and viscosity μ_nf vary with temperature through the base fluid properties [16], [21]. A sudden increase in relaxation factor can cause temperature updates that trigger sharp property changes, creating feedback loops that destabilize the iteration process. The reduced maximum prevents this thermal shock while still permitting acceleration when convergence is genuinely slow.

**Asymmetric stronger reduction for negative error:** When e < 0 (faster-than-linear convergence), the nanofluid's enhanced thermal conductivity [12], [21] promotes more rapid heat redistribution, which can overshoot thermal equilibrium and create oscillatory temperature fields. The stronger reduction signals in Set B provide additional stabilization against this thermal overshoot phenomenon.

**Enhanced damping near origin (|e| < 0.01, |Δe| < 0.01):** Near convergence, small residual oscillations in temperature produce property variations that amplify through the coupled governing equations [10], [14]. The Set B modifications suppress these oscillations by reducing controller gain, preventing round-off error accumulation that would otherwise delay final convergence. This mechanism is particularly important for conjugate problems [24] where thermal feedback between solid and fluid domains can sustain oscillations indefinitely under insufficiently damped control.

## 4. Conclusions

This investigation successfully extends an adaptive neuro-fuzzy inference system framework to govern convergence behavior in computational simulations of nanofluid thermal transport, addressing the heightened nonlinearities that arise from temperature-dependent effective properties and modified buoyancy forces. By embedding an intelligent controller within a SIMPLER-based finite volume solver, the study demonstrates that data-driven relaxation factor adjustment offers substantial advantages over both static under-relaxation and conventional rule-based fuzzy strategies across four distinct benchmark configurations.

The comparative assessment of two neuro-fuzzy training configurations reveals that while control surfaces derived from pure fluid convergence trajectories retain meaningful applicability to colloidal suspensions, nanofluid-specific pattern modifications yield superior outcomes. The revised training set, characterized by a constrained positive adjustment ceiling, amplified stabilization signals for negative error states, and augmented damping within the near-origin region, consistently outperformed the original patterns. Quantitatively, the modified controller reduced iteration counts by approximately 53–56% relative to the optimal fixed relaxation factor, whereas the unmodified controller achieved 44–45% reductions. The divergence-prone conjugate buoyancy-driven cavity at the highest Rayleigh number proved most illustrative: fixed relaxation factors failed at both excessive and insufficient values due to thermal lag between coupled solid and fluid domains, yet the modified neuro-fuzzy controller maintained stable convergence.

Phase-space analysis of the controller dynamics indicates that the nanofluid-adapted training patterns produce monotonically contracting error spirals without the outward excursions observed with original patterns. This behavior stems from suppression of residual oscillations near the origin, preventing temperature-dependent property fluctuations from accumulating round-off errors and destabilizing the final approach to convergence. The asymmetric response to negative error values counteracts thermal overshoot phenomena associated with enhanced nanoparticle conductivity, while the reduced maximum positive increment guards against abrupt acceleration that could trigger feedback loops under sharply varying viscosity and thermal conductivity fields.

The practical viability of the intelligent controller is confirmed through computational time measurements demonstrating a net reduction of approximately 20% despite per-iteration overhead of neuro-fuzzy evaluation. This overhead, quantified at roughly 2.3% of total solver time on the grids employed in this study, becomes progressively less significant as problem scale increases, making the approach particularly attractive for large-scale three-dimensional simulations where each unnecessary iteration carries substantial computational cost. The controller exhibits favorable scalability with nanoparticle loading: whereas the stability window for fixed relaxation factors narrows dramatically at volume fractions exceeding 0.03, reducing the number of viable relaxation factors from seven out of eleven tested values at zero concentration to merely three at the highest loading, the adaptive framework maintains robust convergence across the entire investigated concentration range of ϕ = 0.01 to 0.04, with modified patterns delivering their greatest absolute advantage at the highest loading where property nonlinearities are most severe.

These findings establish that intelligent convergence control is not merely transferable from pure to dispersed-phase heat transfer, but can be materially enhanced by incorporating physics-aware modifications into the learning patterns. The proposed methodology offers a systematic pathway for automating relaxation factor selection in nanofluid computational fluid dynamics, eliminating the prohibitive trial-and-error currently required for problems involving strong property nonlinearities and conjugate heat transfer. The three-phase adaptation strategy—constrained acceleration, asymmetric deceleration, and enhanced near-origin damping—provides a template that may be generalized to other classes of multiphysics problems where property coupling introduces additional stiffness beyond that encountered in single-phase simulations.

Future extensions may explore the integration of frequency-domain residual characteristics into the controller inputs, leveraging the spectral information contained in iteration histories to provide earlier warning of impending divergence. Application to Eulerian-Eulerian or Lagrangian-Eulerian multiphase formulations, where slip velocity and particle migration introduce additional stiffness through interphase coupling terms, represents a natural progression of this work. Extension to three-dimensional configurations with turbulent nanofluid flows would test the scalability of the approach under conditions where computational cost makes automated convergence control even more valuable. Additionally, the development of online learning capabilities that allow the ANFIS controller to adapt its control surface during the simulation, rather than relying solely on pre-trained patterns, could further enhance robustness for previously unseen problem configurations.

## References

[1] J. Ryoo, Z. Dragojlovic, and D. A. Kaminski, "Control of convergence in a computational fluid dynamics simulation using ANFIS," *IEEE Trans. Fuzzy Syst.*, vol. 13, no. 1, pp. 42–47, Feb. 2005, doi: 10.1109/TFUZZ.2004.839656.

[2] H. K. Versteeg and W. Malalasekera, *An Introduction to Computational Fluid Dynamics: The Finite Volume Method*, 2nd ed. Harlow, U.K.: Pearson, 2007.

[3] J. H. Ferziger and M. Perić, *Computational Methods for Fluid Dynamics*, 3rd ed. Berlin, Germany: Springer, 2002.

[4] S. V. Patankar, *Numerical Heat Transfer and Fluid Flow*. New York, NY, USA: McGraw-Hill, 1980.

[5] W. Shyy, *Computational Modeling for Fluid Flow and Interfacial Transport*. Amsterdam, Netherlands: Elsevier, 1994.

[6] S. U. S. Choi, "Enhancing thermal conductivity of fluids with nanoparticles," in *Developments and Applications of Non-Newtonian Flows*, D. A. Siginer and H. P. Wang, Eds. New York, NY, USA: ASME, 1995, pp. 99–105.

[7] S. Kakaç and A. Pramuanjaroenkij, "Review of convective heat transfer enhancement with nanofluids," *Int. J. Heat Mass Transfer*, vol. 52, no. 13–14, pp. 3187–3196, Jun. 2009.

[8] T. P. Otanicar, P. E. Phelan, R. S. Prasher, G. Rosengarten, and R. A. Taylor, "Nanofluid-based direct absorption solar collector," *J. Renewable Sustainable Energy*, vol. 2, no. 3, p. 033102, 2010.

[9] R. Saidur, K. Y. Leong, and H. A. Mohammad, "A review on applications and challenges of nanofluids," *Renewable Sustainable Energy Rev.*, vol. 15, no. 3, pp. 1646–1668, Apr. 2011.

[10] J. Buongiorno, "Convective transport in nanofluids," *J. Heat Transfer*, vol. 128, no. 3, pp. 240–250, Mar. 2006.

[11] J. A. Eastman, S. U. S. Choi, S. Li, W. Yu, and L. J. Thompson, "Anomalously increased effective thermal conductivities of ethylene glycol-based nanofluids containing copper nanoparticles," *Appl. Phys. Lett.*, vol. 78, no. 6, pp. 718–720, Feb. 2001.

[12] W. Yu and S. U. S. Choi, "The role of interfacial layers in the enhanced thermal conductivity of nanofluids: A renovated Maxwell model," *J. Nanoparticle Res.*, vol. 5, no. 1–2, pp. 167–171, 2003.

[13] S. K. Das, N. Putra, P. Thiesen, and W. Roetzel, "Temperature dependence of thermal conductivity enhancement for nanofluids," *J. Heat Transfer*, vol. 125, no. 4, pp. 567–574, Aug. 2003.

[14] S. Mahmud, A. K. M. S. Islam, and R. Saidur, "Thermodynamic analysis of nanofluid flow through a channel with permeable walls," *Int. J. Heat Mass Transfer*, vol. 54, no. 23–24, pp. 5215–5225, Nov. 2011.

[15] K. Khanafer, K. Vafai, and M. Lightstone, "Buoyancy-driven heat transfer enhancement in a two-dimensional enclosure utilizing nanofluids," *Int. J. Heat Mass Transfer*, vol. 46, no. 19, pp. 3639–3653, Sep. 2003.

[16] E. Abu-Nada and A. J. Chamkha, "Effect of nanofluid variable properties on natural convection in enclosures filled with a CuO-EG-water nanofluid," *Int. J. Therm. Sci.*, vol. 49, no. 12, pp. 2339–2352, Dec. 2010.

[17] Y. Xuan and Q. Li, "Heat transfer enhancement of nanofluids," *Int. J. Heat Fluid Flow*, vol. 21, no. 1, pp. 58–64, Feb. 2000.

[18] M. Manninen, V. Taivassalo, and S. Kallio, "On the mixture model for multiphase flow," *VTT Publications*, vol. 288, pp. 1–67, 1996.

[19] A. K. Santra, S. Sen, and N. Chakraborty, "Study of heat transfer due to laminar flow of copper-water nanofluid through two isothermally heated parallel plates," *Int. J. Therm. Sci.*, vol. 48, no. 2, pp. 391–400, Feb. 2009.

[20] M. Corcione, "Empirical correlating equations for predicting the effective thermal conductivity and dynamic viscosity of nanofluids," *Energy Convers. Manage.*, vol. 52, no. 1, pp. 789–793, Jan. 2011.

[21] J. C. Maxwell, *A Treatise on Electricity and Magnetism*, 3rd ed. Oxford, U.K.: Clarendon, 1904.

[22] H. C. Brinkman, "The viscosity of concentrated suspensions and solutions," *J. Chem. Phys.*, vol. 20, no. 4, p. 571, 1952.

[23] G. de Vahl Davis, "Natural convection of air in a square cavity: A bench mark numerical solution," *Int. J. Numer. Methods Fluids*, vol. 3, no. 3, pp. 249–264, May 1983.

[24] D. A. Kaminski and C. Prakash, "Conjugate natural convection in a square enclosure: Effect of conduction in one of the vertical walls," *Int. J. Heat Mass Transfer*, vol. 29, no. 12, pp. 1979–1988, Dec. 1986.

[25] R. Schreiber and H. B. Keller, "Driven cavity flows by efficient numerical techniques," *J. Comput. Phys.*, vol. 49, no. 2, pp. 310–333, Feb. 1983.

[26] G. E. Cort, A. L. Graham, and N. L. Johnson, "Comparison of methods for solving nonlinear finite-element equations in heat transfer," in *Proc. ASME*, 1982, Paper 82-HT-40.

[27] S. Iida, K. Ogawara, S. Furusawa, and N. Ohata, "A fast converging method using wobbling adaptive control of SOR relaxation factor for 2D Bénard convection," *J. Mech. Eng. Soc. Jpn.*, vol. 7, pp. 168–174, 1994.

[28] J. Ryoo, D. Kaminski, and Z. Dragojlovic, "A residual-based fuzzy logic algorithm for control of convergence in a computational fluid dynamics simulation," *J. Heat Transfer*, vol. 121, no. 4, pp. 1076–1078, Nov. 1999.

[29] J.-S. R. Jang, "ANFIS: Adaptive-network-based fuzzy inference system," *IEEE Trans. Syst., Man, Cybern.*, vol. 23, no. 3, pp. 665–685, May/Jun. 1993.

[30] Z. Dragojlovic, D. A. Kaminski, and J. Ryoo, "Control of convergence in convective flow simulation using a fuzzy rule set that stabilizes iterative oscillations," in *Proc. 33rd National Heat Transfer Conf.*, Albuquerque, NM, USA, 1999, Paper NHTC99-229.

[31] R. K. Tiwari and M. K. Das, "Heat transfer augmentation in a two-sided lid-driven differentially heated square cavity utilizing nanofluids," *Int. J. Heat Mass Transfer*, vol. 50, no. 9–10, pp. 2002–2018, May 2007.
