# Energy, Dissipation-Induced Instability and Domain of Influence in Klein–Gordon Nonlocal Thermoelasticity: A Unified Analysis of Six Non-Fourier Heat Conduction Models

---

## Abstract

Klein–Gordon (KG) nonlocal elasticity, (1 − ε₁²∇² + τ₁²∂ₜ²)σ = C:e − γΘI, adds a characteristic time τ₁ to the characteristic length ε₁ of Eringen's model. It is now widely combined with non-Fourier heat conduction, but the well-posedness and stability of the resulting initial-value problem have not been examined. We study the linear problem on ℝ³ for six heat laws: Lord–Shulman (LS), Green–Naghdi types II and III (GN-II, GN-III), dual-phase-lag (DPL-1), hyperbolic dual-phase-lag (HDPL) and Moore–Gibson–Thompson (MGT).

First, the purely elastic KG equation conserves a one-parameter family of energies E_b. For τ₁² < b < ε₁²/c_d², E_b is positive definite. The elastic problem is therefore stable, and its solutions are unique, whenever τ₁c_d < ε₁. If τ₁c > ε₁ for c = c_d or c_s, there is an explicit band of wavenumbers in which solutions grow exponentially. For shear waves this criterion holds for every heat law, because shear waves decouple from temperature.

Second, the physical energy E₀, the one whose decrease thermodynamics guarantees, is indefinite. For a plane mode its average is ½|A|²ω² ∂D/∂(ω²), which is positive on the acoustic branch and negative on the optical branch that KG nonlocality creates above frequency 1/τ₁.

Third, as a consequence, every dissipative heat law destabilizes KG thermoelasticity, even when τ₁c_d < ε₁. We derive the growth rate to first order in the coupling ε at all wavenumbers: Re s = εk⁴ Im q²/(2ω_o√Δ|k² − q²|²), where ω_o is the optical frequency, Δ the elastic discriminant and q the thermal wavenumber. The formula matches the exact roots to within 0.12% for k ≥ 0.1. The growth rate is positive for LS, GN-III and DPL-1, and for MGT and HDPL exactly when their own stability conditions hold. It decays like k⁻² at large k and resonates when ε₁/τ₁ equals the thermal front speed. For copper the e-folding time is 0.2–1.2 ns. GN-II is neutral at the physical coupling, but becomes unstable when the optical branch crosses the thermal branch. Kelvin–Voigt viscosity, or a damping term in the KG operator, makes the instability worse.

Fourth, coupling the heat equation to ∇·(u̇ + bu⃛) instead of ∇·u̇ makes the cross terms cancel against E_b, and the system becomes stable for τ₁² ≤ b ≤ ε₁²/c_d². We prove this for the Fourier, LS, GN-II and GN-III laws and verify it numerically for MGT, DPL-1 and HDPL.

Fifth, Gårding's theorem confines disturbances to |x| ≤ V∗t with V∗ = max(ε₁/τ₁, v_θ), where v_θ is the thermal front speed. The speed is infinite for GN-III, DPL-1 and Eringen's model.

**Keywords:** Klein–Gordon nonlocal elasticity; well-posedness; energy method; dissipation-induced instability; negative-energy waves; Krein collision; domain of influence; Gårding hyperbolicity; Moore–Gibson–Thompson; dual-phase-lag

---

## 1. Introduction

The theory of thermoelasticity began with Duhamel, who added a thermal stress to the equations of elasticity [1]. Biot gave the coupled theory a basis in irreversible thermodynamics [2]. Because it uses Fourier's law, the classical theory predicts an infinite speed for heat. Cattaneo [3] and Vernotte [4] removed this by adding a relaxation time to the flux. Lord and Shulman (LS) built a generalized dynamic thermoelasticity on that idea [5], and Green and Lindsay proposed a variant with two relaxation times [6]. Green and Naghdi introduced the thermal displacement and three theories of type I–III [7–9]. Type II has no dissipation; type III contains both a conductive and a wave-like flux. Tzou's dual-phase-lag (DPL) law separates the lags of the heat flux and of the temperature gradient [10]. These hyperbolic theories were reviewed by Chandrasekharaiah [11].

Quintanilla added a flux relaxation to GN-III to obtain Moore–Gibson–Thompson (MGT) thermoelasticity [12]. Extensions with history dependence [13] and numerical analysis [14] followed. Stability is not automatic for these heat laws. The MGT equation decays exponentially only if the diffusive coefficient exceeds the relaxed wave coefficient [15]. The second-order DPL law requires 2τ_T > τ_q [16], and DPL thermoelasticity has its own well-posedness conditions [17]. Thermodynamic restrictions on delayed models were discussed by Fabrizio and Franchi [18].

For classical thermoelasticity, existence and asymptotic stability were established by Dafermos [19]. The energy method and uniqueness theorems are summarized by Carlson [20] and by Ieşan [21]. Domain-of-influence theorems, which state that disturbances travel at finite speed, are a second standard requirement; for MGT thermoelasticity such a theorem was proved by Jangid and Mukhopadhyay [22]. Plane-wave analyses of the same theory were given by Jangid, Gupta and Mukhopadhyay [23].

Nonlocal elasticity adds a length scale. In Eringen's integral theory the stress at a point depends on the strain in a neighbourhood [24]. For one kernel the integral law reduces to the differential form (1 − ε₁²∇²)σ = C:e [25,26]. Its dispersion relation has a cut-off frequency [27], and its relation to gradient elasticity and to length-scale identification is reviewed in [28].

Lazar and Agiasofitou added a characteristic time, arriving at nonlocal elasticity of Klein–Gordon type [29,30]. The constitutive operator becomes 1 − ε₁²∇² + τ₁²∂ₜ². The time term produces an optical-like branch and a frequency gap, which makes the model attractive for structured media. Singh combined the KG operator with MGT heat conduction [31]. Mondal and Mukhopadhyay recently analysed plane waves under KG nonlocality and six heat laws in one framework [32]. These works compute dispersion relations or transient responses, but none examines whether the initial-value problem is well-posed or stable.

There are two reasons to expect a problem.

- **Fourth-order time derivative.** The displacement equation contains ρτ₁²∂ₜ⁴u. The natural energy, obtained with the multiplier u̇, then contains the indefinite term −½ρτ₁²|ü|².
- **Nonlocality and propagation speed.** For constant-coefficient systems the speed of propagation is set by the principal part of the operator. Gårding's theorem states that a forward fundamental solution supported in a cone exists if and only if the operator is hyperbolic [33,34]. Eringen's differential model fails this test, so its speed is infinite. KG nonlocality changes the principal part, and its domain of influence is unknown.

This paper analyses both questions with the energy method [20,21,35], semigroup arguments [36] and Fourier analysis. The main result is that dissipation destabilizes the KG optical branch, because that branch carries negative physical energy. Such dissipation-induced instabilities of negative-energy modes are well known in fluid mechanics [37], in Hamiltonian systems [38,39] and more generally in non-conservative mechanics [40,41]. They had not been identified in nonlocal thermoelasticity. The result has a practical consequence for Laplace-domain transient solutions, whose numerical inversion assumes no singularities to the right of the Bromwich contour [42].

The contributions are:

1. a one-parameter family of conserved energies for elastic KG, a stability window τ₁² < b < ε₁²/c_d², and an explicit growth band when τ₁c > ε₁;
2. the modal energy ½|A|²ω²∂D/∂(ω²), which shows that the optical branch carries negative physical energy for all wavenumbers;
3. the physical energy identity for KG thermoelasticity, and a first-order growth law, valid at all wavenumbers, for every heat law;
4. closed-form small-k and large-k limits of the growth rate, including a resonance when ε₁/τ₁ equals the thermal front speed;
5. a modified coupling with a positive, non-increasing energy;
6. the domain of influence for all six heat laws.

Section 2 states the model. Section 3 treats elastic KG and the modal energy. Section 4 analyses dissipation-induced instability. Section 5 presents the energy-consistent coupling. Section 6 gives the domain of influence. Section 7 discusses the consequences, and Section 8 summarizes the conclusions.

## 2. Model

### 2.1 Field equations

Let u be the displacement, Θ = T − T₀ the temperature increment and q the heat flux in a homogeneous, isotropic solid occupying ℝ³. The KG constitutive law [29,32] is

(1 − ε₁²∇² + τ₁²∂ₜ²) σ = C∇u − γΘ I,                                                                   (1)

where C is the isotropic elasticity tensor with Lamé constants λ and μ, and γ = α_t(3λ + 2μ). With the equation of motion

div σ = ρ ü,                                                                                              (2)

and the nonlocal operator applied to both sides, the displacement satisfies

ρ (1 − ε₁²∇² + τ₁²∂ₜ²) ü = div(C∇u) − γ ∇Θ.                                                            (3)

The linearized energy balance is

ρ c Θ̇ + γ T₀ ∇·u̇ + div q = 0.                                                                           (4)

### 2.2 Heat conduction laws

The six heat laws of [32] are, for Fourier conduction,

q = −k ∇Θ;                                                                                                (5)

for LS [3–5],

(1 + τ_q∂ₜ) q = −k ∇Θ;                                                                                   (6)

for GN-II [8], with the thermal displacement ν̇ = Θ,

q = −k∗ ∇ν;                                                                                               (7)

for GN-III [9],

q = −k ∇Θ − k∗ ∇ν;                                                                                        (8)

for MGT [12],

(1 + τ_q∂ₜ) q = −k ∇Θ − k∗ ∇ν;                                                                            (9)

and for DPL-1 (n₁ = 0) and HDPL (n₁ = 1) [10,11],

(1 + τ_q∂ₜ + n₁τ_q²∂ₜ²/2) q = −k (1 + τ_T∂ₜ) ∇Θ.                                                         (10)

### 2.3 Assumptions on the elastic moduli

We assume μ > 0 and λ + μ ≥ 0, which holds for copper and for most isotropic solids. For fields v decaying at infinity, integration by parts gives the identity

⟨C∇v, ∇v⟩ = ∫ [(λ + 2μ)(div v)² + μ|curl v|²] dx,                                                      (11)

and, because ‖∇v‖² = ‖div v‖² + ‖curl v‖², the bounds

μ ‖∇v‖² ≤ ⟨C∇v, ∇v⟩ ≤ (λ + 2μ) ‖∇v‖²,                                                                   (12)

where ‖·‖ is the L²(ℝ³) norm.

### 2.4 Non-dimensional form and Fourier symbols

We use the scaling of the companion wave-propagation study (Paper A), which coincides with [23,32] when k > 0 and stays valid for GN-II. The reference frequency is ω∗ = ρcV²/k_ref with V = √((λ+2μ)/ρ), and the dimensionless groups are

c_d = 1,   c_s² = μ/(λ + 2μ),   ε = γ²T₀/(ρc(λ + 2μ)),   C_T² = k∗/(ρcV²),   κ = k/k_ref.                   (13)

For the stability analysis we use Fourier–Laplace modes

(u, Θ) ∝ exp(st + ik·x),   k ∈ ℝ³,   s ∈ ℂ,                                                                (14)

so a mode grows if Re s > 0. Writing k = |k|, the longitudinal (P) characteristic polynomial is

D_P(s, k) = [b(s) + k²a(s)] E(s, k) − ε k² b(s),                                                             (15)

where a and b are the heat-law polynomials of Table 2 and

E(s, k) = −k² − (1 + ε₁²k²) s² − τ₁²s⁴                                                                     (16)

is the KG elastic symbol. The transverse (S) polynomial is independent of the heat law:

D_S(s, k) = τ₁²s⁴ + (1 + ε₁²k²) s² + c_s²k².                                                                (17)

For the frequency-domain quantities we use the uncoupled thermal wavenumber of Paper A,

q²(ω) = −b(−iω) / a(−iω),                                                                                    (18)

evaluated at real frequency ω > 0.

### 2.5 Relation to earlier formulations

Eqs. (3)–(10) are the equations of [32], written in dimensional form and with the standard sign convention −div q for heat supplied by conduction. The thermal stress −γΘI enters the right-hand side of Eq. (1), so it is not acted on by the nonlocal operator. This choice follows [29,31,32] and is essential for the analysis below. If the operator acted on the thermal stress as well, the coupling term in Eq. (15) would carry the factor (1 + ε₁²k² + τ₁²s²). The structure of the instability would not change, but the closed forms of Section 4 would. All results are stated for the formulation in use in the literature.

The Fourier-mode convention exp(st + ik·x) of Eq. (14) is related to the harmonic convention exp{i(Wx − βt)} of Paper A by s = −iβ and k = W. Temporal stability (Re s ≤ 0 for real k) and spatial attenuation (Im W ≥ 0 for real β) are different questions. For a negative-energy branch they give answers of opposite sign: temporal growth in this paper and spatial amplification in Paper A.

Table 1. Data (copper [23,32]) and model parameters.

| Quantity | Value | Quantity | Value |
|---|---|---|---|
| ρ | 8954 kg m⁻³ | λ, μ | 7.76 × 10¹⁰ Pa, 3.86 × 10¹⁰ Pa |
| c | 383.1 J kg⁻¹ K⁻¹ | k | 386 W m⁻¹ K⁻¹ |
| k∗ | 5930.38 × 10¹⁰ W m⁻¹ K⁻¹ s⁻¹ | T₀ | 293 K |
| α_t (physical) | 1.78 × 10⁻⁵ K⁻¹ | α_t (as printed in [32]) | 1.78 × 10⁻⁴ K⁻¹ |
| ε (physical) | 0.0168 | ε (from [32]) | 1.680 |
| ω∗ | 1.536 × 10¹¹ s⁻¹ | l∗ = V/ω∗ | 27.06 nm |
| c_s | 0.4994 | C_T² | 1.000 |
| ε₁ | 0.01 | τ₁ | 0.006 |
| τ_q | 0.01 | τ_T | 0.015 |

Table 2. Heat-law polynomials (non-dimensional).

| Model | a(s) | b(s) | Stability condition of the heat law |
|---|---|---|---|
| LS | κ | s(1 + τ_q s) | none |
| GN-II | C_T² | s² | conservative |
| GN-III | C_T² + κs | s² | κ > 0 |
| MGT | C_T² + κs | s²(1 + τ_q s) | κ > τ_qC_T² [12,15] |
| DPL-1 | κ(1 + τ_T s) | s(1 + τ_q s) | none |
| HDPL | κ(1 + τ_T s) | s(1 + τ_q s + τ_q²s²/2) | 2τ_T > τ_q [16] |

## 3. The purely elastic KG equation

### 3.1 A family of conserved energies

Let γ = 0 and consider the multiplier

v = u̇ + b u⃛,   b ∈ ℝ.                                                                                     (19)

Taking the L² product of Eq. (3) with v and integrating by parts for fields decaying at infinity gives four identities. The inertial term gives

ρ ∫ ü·(u̇ + b u⃛) dx = d/dt ρ ∫ (½|u̇|² + ½b|ü|²) dx.                                                      (20)

The spatially nonlocal term gives

−ρε₁² ∫ ∇²ü·(u̇ + b u⃛) dx = d/dt ρε₁² ∫ (½|∇u̇|² + ½b|∇ü|²) dx.                                         (21)

The temporally nonlocal term gives

ρτ₁² ∫ u⁗·(u̇ + b u⃛) dx = d/dt ρτ₁² ∫ (u̇·u⃛ − ½|ü|² + ½b|u⃛|²) dx.                                       (22)

The elastic term gives

−∫ div(C∇u)·(u̇ + b u⃛) dx = d/dt ∫ (½C∇u:∇u + bC∇u:∇ü − ½bC∇u̇:∇u̇) dx.                                   (23)

Adding Eqs. (20)–(23) defines

E_b(t) = ½∫ { ρ|u̇|² + 2ρτ₁² u̇·u⃛ + ρbτ₁²|u⃛|² + ρ(b − τ₁²)|ü|² + ρε₁²|∇u̇|² − bC∇u̇:∇u̇ + ρbε₁²|∇ü|² + C∇u:∇u + 2bC∇u:∇ü } dx,      (24)

and proves the conservation law

dE_b/dt = 0   for every b ∈ ℝ.                                                                             (25)

**Theorem 1 (positivity).** E_b is equivalent to the squared norm N(t) defined below if and only if τ₁² < b < ε₁²ρ/(λ + 2μ). Such a b exists if and only if τ₁c_d < ε₁.

*Proof.* Consider first the pair (u̇, u⃛). The quadratic form

ρ(|u̇|² + 2τ₁² u̇·u⃛ + bτ₁²|u⃛|²) > 0   for (u̇, u⃛) ≠ 0   ⇔   b > τ₁²                                       (26)

controls both variables. The coefficient ρ(b − τ₁²) of |ü|² is then positive. By Eq. (12), ρε₁²‖∇u̇‖² − b⟨C∇u̇, ∇u̇⟩ ≥ (ρε₁² − b(λ + 2μ))‖∇u̇‖², which is positive if b < ε₁²/c_d².

For the pair (∇u, ∇ü), Young's inequality in the C-inner product gives, for any θ ∈ (0, 1),

2b⟨C∇u, ∇ü⟩ ≥ −θ⟨C∇u, ∇u⟩ − (b²/θ)(λ + 2μ)‖∇ü‖².                                                           (27)

The remainder ρbε₁² − (b²/θ)(λ + 2μ) is positive if b < θε₁²/c_d². Such a θ < 1 exists precisely when

τ₁² < b < ε₁²/c_d².                                                                                         (28)

With the lower bound of Eq. (12), E_b then controls

N(t) = ‖u̇‖² + ‖ü‖² + ‖u⃛‖² + ‖∇u‖² + ‖∇u̇‖² + ‖∇ü‖².                                                     (29)

Conversely, if b lies outside the interval (28), one of the forms above is indefinite. ∎

**Corollary 1 (stability and uniqueness).** If τ₁c_d < ε₁, there are constants 0 < m₁ ≤ m₂ depending only on the material such that

m₁ N(t) ≤ E_b(t) ≤ m₂ N(t),                                                                                 (30)

and hence every solution satisfies

N(t) ≤ (m₂/m₁) N(0)   for all t ≥ 0.                                                                       (31)

In particular, a solution with zero data vanishes identically. With the Hille–Yosida theorem [36], Eq. (31) gives a contraction semigroup in the energy norm.

### 3.2 The physical energy and the modal energy

Only the member b = 0 of the family corresponds to the multiplier u̇, and therefore to the power expended by external forces. It is

E₀ = ½∫ { ρ|u̇|² − ρτ₁²|ü|² + 2ρτ₁² u̇·u⃛ + ρε₁²|∇u̇|² + C∇u:∇u } dx.                                     (32)

E₀ is indefinite. For the spatially uniform optical oscillation u = A cos(t/τ₁), its density is

e₀ = −ρ|A|² / (2τ₁²) < 0.                                                                                   (33)

The sign of E₀ holds on the whole optical branch, not only at k = 0. Write the elastic dispersion function (non-dimensional, with c the local speed) as

D(ω², k) = ω²(1 + ε₁²k²) − τ₁²ω⁴ − c²k².                                                                   (34)

**Proposition 1 (modal energy).** For a plane mode u = A cos(ωt − k·x) satisfying D(ω², k) = 0, the time-averaged density of E₀ is

⟨e₀⟩ = ½ |A|² ω² ∂D/∂(ω²).                                                                                  (35)

At the two roots ω² = [(1 + ε₁²k²) ∓ √Δ]/(2τ₁²), where Δ = (1 + ε₁²k²)² − 4τ₁²c²k², this gives

∂D/∂(ω²) = ±√Δ:  positive on the acoustic branch, negative on the optical branch.                         (36)

*Proof.* Average the integrand of Eq. (32) over a period. This gives ¼|A|²[ω²(1 + ε₁²k²) − 3τ₁²ω⁴ + c²k²]. Eliminate c²k² using D = 0 and compare with ∂D/∂(ω²) = (1 + ε₁²k²) − 2τ₁²ω². ∎

Eq. (35) is the classical wave-energy formula of Cairns [37] for a dispersion function that depends on ω². For a single mode u⃛ = −ω²u̇, so the energy obtained with the multiplier (19) is

⟨e_b⟩ = (1 − bω²) ⟨e₀⟩.                                                                                     (37)

The acoustic frequencies satisfy ω < c/ε₁ and the optical frequencies satisfy ω > 1/τ₁. Eq. (37) is therefore positive on both branches exactly when τ₁² ≤ b ≤ ε₁²/c². This independently confirms the window of Theorem 1, mode by mode.

### 3.3 Instability for τ₁c > ε₁

The temporal roots of a KG wave of local speed c solve

τ₁²s⁴ + (1 + ε₁²k²) s² + c²k² = 0.                                                                         (38)

The discriminant of Eq. (38) in s² is Δ(k²) = (1 + ε₁²k²)² − 4τ₁²c²k². It is negative, and s² is complex, exactly when k² lies between the roots of Δ.

**Proposition 2 (growth band).** If τ₁c > ε₁, Eq. (38) has a root with Re s > 0 for

k₋ < k < k₊,   k± = [τ₁c ± √(τ₁²c² − ε₁²)] / ε₁².                                                          (39)

In this band

s² = [−(1 + ε₁²k²) ± i√(−Δ)] / (2τ₁²),                                                                     (40)

and, since |s²| = ck/τ₁, the growth rate is

Re s = √{ [ck/τ₁ − (1 + ε₁²k²)/(2τ₁²)] / 2 }.                                                              (41)

If τ₁c ≤ ε₁ the band is empty.

*Proof.* Δ is a quadratic in k² with roots k±², and Δ < 0 between them. Eq. (41) follows from Re √z = √((|z| + Re z)/2). ∎

Shear waves are uncoupled from Θ for every heat law. The condition τ₁c_s ≤ ε₁ is therefore necessary for the stability of KG thermoelasticity, whatever the heat law. For the data of Table 1, τ₁c_d = 0.006 < ε₁ = 0.01, so both elastic conditions hold. For τ₁ = 0.015, Eq. (39) gives 38.2 < k < 261.8 for P waves, and Eq. (41) gives a peak growth rate of 37.3 near k = 150. Both match the numerical roots to three digits (Fig. 1b).

[Insert Figure 1 here]

Figure 1. Purely elastic KG P wave. (a) Temporal frequencies |Im s| of the acoustic and optical branches for τ₁ = 0.006. The optical branch starts at 1/τ₁ ≈ 166.7 and approaches slope ε₁/τ₁; the acoustic branch saturates at 1/ε₁ = 100. (b) Growth rate Re s for τ₁ = 0.012, 0.015 and 0.02 (all with τ₁c_d > ε₁). Dotted lines are the band edges of Eq. (39).

### 3.4 The matched case and marginal stability

At the boundary τ₁c = ε₁ of the window (28), the discriminant becomes Δ = (1 + ε₁²k²)² − 4ε₁²k² = (1 − ε₁²k²)². It is non-negative for every k and vanishes at the single wavenumber k = 1/ε₁. There the two roots in s² coincide, so the acoustic and optical branches touch at the frequency ω = 1/τ₁. For all other k the roots are distinct and purely imaginary.

At the touching point the polynomial (38) has a double pair of imaginary roots. If the corresponding eigenvectors coalesce, as they generically do, solutions grow linearly in time rather than exponentially. The matched case τ₁c_d = ε₁ is therefore marginally stable. It is the case in which the P wave of Paper A is non-dispersive. Its energy E_b with b = τ₁² = ε₁²/c_d² is non-negative but not positive definite, in agreement with Theorem 1, which requires a strict inequality.

The modal energy (37) gives the same picture. For b = τ₁², ⟨e_b⟩ vanishes at ω = 1/τ₁, the cut-on frequency of the optical branch. For b = ε₁²/c², it vanishes in the limit ω → c/ε₁, the saturation frequency of the acoustic branch. When τ₁c = ε₁ the two frequencies coincide, and no admissible b remains strictly inside the window.

## 4. Dissipation-induced instability

### 4.1 Physical energy identity

Multiply Eq. (3) by u̇ and Eq. (4) by Θ/T₀, integrate and add. The coupling terms ±γ∫Θ ∇·u̇ cancel, which gives

d/dt [E₀ + ∫ ρcΘ²/(2T₀) dx] = (1/T₀) ∫ q·∇Θ dx.                                                          (42)

For the LS law (6),

q·∇Θ = −|q|²/k − (τ_q/(2k)) d/dt |q|²;                                                                    (43)

for GN-II (7),

q·∇Θ = −(k∗/2) d/dt |∇ν|²;                                                                                (44)

and for GN-III (8),

q·∇Θ = −k|∇Θ|² − (k∗/2) d/dt |∇ν|².                                                                      (45)

**Theorem 2 (physical energy identity).** For the Fourier, LS, GN-II and GN-III laws,

d/dt [E₀ + E_θ] = −𝒟 ≤ 0,                                                                                 (46)

where E_θ = ∫ρcΘ²/(2T₀) is augmented by ∫τ_q|q|²/(2kT₀) for LS and by ∫k∗|∇ν|²/(2T₀) for GN-II and GN-III. The dissipation is 𝒟 = ∫k|∇Θ|²/T₀ (Fourier, GN-III), ∫|q|²/(kT₀) (LS), or 0 (GN-II).

Eq. (46) is the usual thermodynamic statement that dissipation reduces the physical energy. Because E₀ is indefinite (Proposition 1), it does not imply stability. A mode with negative E₀ that loses energy grows in amplitude [37–41].

### 4.2 Growth law at small wavenumber

**Theorem 3 (small-k growth).** Let τ₁ > 0 and b(i/τ₁) ≠ 0. The optical root of D_P that equals s₀ = i/τ₁ at k = 0 is analytic in k² near k = 0. Its real part is

Re s(k) = −(ε τ₁ k⁴ / 2) · Im[a(i/τ₁) / b(i/τ₁)] + O(k⁶).                                                   (47)

*Proof.* Near s₀, D_P = 0 is equivalent to

E(s, k) = εk² / (1 + k²a/b) = εk² − εk⁴ a(s)/b(s) + O(k⁶).                                                 (48)

At k = 0, E = −s²(1 + τ₁²s²) has a simple root at s₀, with ∂E/∂s(s₀) = 2s₀. By the implicit function theorem,

s = s₀ + σ₁k² + σ₂k⁴ + O(k⁶).                                                                              (49)

E is even in s with real coefficients, so E(iy, k) is real for real y. All terms generated by E alone are therefore purely imaginary, including

σ₁ = −(iτ₁/2)(1 + ε − ε₁²/τ₁²).                                                                            (50)

The only real contribution comes from the term εk⁴a/b in Eq. (48). It gives Re σ₂ = −Re[ε(a/b)(s₀)/(2s₀)], which is Eq. (47). ∎

With Ω = 1/τ₁ the bracket of Eq. (47) has the following closed forms:

LS:      Im[a/b](iΩ) = −κ / [Ω(1 + τ_q²Ω²)];                                                                (51)

GN-II:   Im[a/b](iΩ) = 0;                                                                                    (52)

GN-III:  Im[a/b](iΩ) = −κ/Ω;                                                                                 (53)

MGT:     Im[a/b](iΩ) = −(κ − τ_qC_T²) / [Ω(1 + τ_q²Ω²)];                                                     (54)

DPL-1:   Im[a/b](iΩ) = −κ(1 + τ_Tτ_qΩ²) / [Ω(1 + τ_q²Ω²)];                                                   (55)

HDPL:    Im[a/b](iΩ) = −κ[1 + Ω²τ_q(τ_T − τ_q/2)] / [Ω |1 − τ_q²Ω²/2 + iτ_qΩ|²].                             (56)

**Corollary 2.** For τ₁ > 0 the optical branch grows at small k under LS, GN-III (κ > 0) and DPL-1 for all admissible parameters. It grows under MGT whenever κ > τ_qC_T², and under HDPL whenever 2τ_T > τ_q:

sign Re s = sign(−Im[a/b](iΩ)) > 0   whenever the heat law is itself stable.                                (57)

For GN-II the leading term vanishes.

Table 3 compares Eq. (47) with the numerical roots of D_P. The agreement is four digits for all dissipative models. The 2% difference for MGT at k = 0.05 is round-off, because the growth rate there is about 10⁻¹³ while the frequencies are of order 10².

Table 3. Small-k growth law (47) against numerical roots (ε = 0.0168).

| Model | Im[a/b](i/τ₁) | Re s, k = 0.05: numeric / Eq. (47) | Re s, k = 0.2: numeric / Eq. (47) |
|---|---|---|---|
| LS | −1.588e−3 | 5.000e−13 / 5.003e−13 | 1.281e−10 / 1.281e−10 |
| GN-II | 0 | ≈ 0 / 0 | ≈ 0 / 0 |
| GN-III | −6.000e−3 | 1.890e−12 / 1.890e−12 | 4.839e−10 / 4.839e−10 |
| DPL-1 | −8.206e−3 | 2.583e−12 / 2.585e−12 | 6.617e−10 / 6.618e−10 |
| HDPL | −7.739e−3 | 2.438e−12 / 2.438e−12 | 6.244e−10 / 6.241e−10 |
| MGT | −1.572e−3 | 5.048e−13 / 4.953e−13 | 1.268e−10 / 1.268e−10 |

### 4.3 Growth law at all wavenumbers

Theorem 3 can be extended to all k at first order in ε. Let ω_o(k) > 0 be the optical frequency of the uncoupled elastic equation, so that E(iω_o, k) = 0. Define the real function

F(y, k) = E(iy, k) = −k² + y²(1 + ε₁²k²) − τ₁²y⁴,                                                         (58)

and the thermal transfer function G(s) = b(s)/(b(s) + k²a(s)). The coupled equation D_P = 0 reads E = εk²G. To first order in ε, the optical root is shifted by δs = εk²G(iω_o)/E_s(iω_o), with E_s = −iF_y. Hence

Re δs = −ε k² Im G(iω_o) / F_y(ω_o, k).                                                                    (59)

Since a and b have real coefficients, G(iω) is the complex conjugate of G(−iω) = q²/(q² − k²). By the identity of Paper A,

Im G(iω) = k² Im q²(ω) / |k² − q²(ω)|².                                                                    (60)

On the optical branch F_y = 2ω_o ∂D/∂(ω²) = −2ω_o√Δ by Eq. (36). This gives the main result of this section.

**Theorem 4 (first-order growth law).** For small ε, the optical branch of KG thermoelasticity has

Re s_o(k) = ε k⁴ Im q²(ω_o) / [2 ω_o √Δ |k² − q²(ω_o)|²] + O(ε²),                                          (61)

and the acoustic branch has

Re s_a(k) = −ε k⁴ Im q²(ω_a) / [2 ω_a √Δ |k² − q²(ω_a)|²] + O(ε²).                                         (62)

By Lemma 1 of Paper A, Im q² > 0 at every frequency exactly when the heat law is dissipative and stable. Under that condition the optical branch grows and the acoustic branch decays, at every wavenumber.

The sign difference between Eqs. (61) and (62) is the sign of the modal energy (36). Dissipation always removes physical energy, so it damps positive-energy modes and amplifies negative-energy ones. Theorem 4 is the time-domain counterpart of the spatial amplification of the optical elastic wave found in Paper A. Fig. 2 shows that Eq. (61) reproduces the exact growth rate to within 0.12% for all k ≥ 0.1 and all five dissipative laws. At the peak, for example, the LS values are 3.1901 × 10⁻² (exact) and 3.1915 × 10⁻² (Eq. (61)) at k = 19.8.

[Insert Figure 2 here]

Figure 2. First-order growth law. (a) Exact max Re s (dots) against Eq. (61) (lines) for the five dissipative heat laws, ε = 0.0168. (b) Ratio of exact to first-order values for k ≥ 0.1.

### 4.4 Large-wavenumber behaviour and resonance

For large k the optical frequency is ω_o ≈ v_n k, with nonlocal speed v_n = ε₁/τ₁, and √Δ ≈ ε₁²k². For heat laws with a finite front speed v_θ (LS, MGT, HDPL), Im q² ≈ Λ_θ ω and q² ≈ ω²/v_θ². Substituting into Eq. (61) gives

Re s_o ≈ ε Λ_θ / [2 ε₁² k² (1 − v_n²/v_θ²)²],                                                              (63)

with the coefficient

Λ_θ = 1/κ (LS);  (1 − τ_qC_T²/κ)/κ (MGT);  (τ_q/τ_T)(1 − τ_q/(2τ_T))/κ (HDPL).                             (64)

For the diffusive laws (GN-III and DPL-1) the factor (1 − v_n²/v_θ²) is replaced by 1, with Λ_θ = 1/κ (GN-III) and τ_q/(κτ_T) (DPL-1). Table 4 shows that Eq. (63) reproduces the exact values at k = 10⁴ to four digits.

Eq. (63) predicts a resonance when the nonlocal speed matches the thermal front speed:

v_n = v_θ   ⇔   τ₁ = ε₁ / v_θ.                                                                             (65)

For ε₁ = 0.01, this gives τ₁ = 0.001 for LS and MGT (v_θ = 10) and τ₁ = 5.77 × 10⁻⁴ for HDPL (v_θ = 17.32). Fig. 3(b) shows sharp peaks of the growth rate at exactly these values, reaching sup Re s = 2.05 (LS) and 0.62 (HDPL). Phase matching between the optical elastic branch and the thermal front therefore maximizes the transfer of energy from the negative-energy mode into dissipation.

Table 4. Large-k growth law (63) against exact roots at k = 10⁴ (ε = 0.0168).

| Model | v_θ | Λ_θ | Eq. (63) | Exact |
|---|---|---|---|---|
| LS | 10 | 1 | 8.887e−7 | 8.887e−7 |
| GN-III | ∞ | 1 | 8.400e−7 | 8.400e−7 |
| DPL-1 | ∞ | 0.6667 | 5.600e−7 | 5.600e−7 |
| HDPL | 17.32 | 0.4444 | 3.803e−7 | 3.804e−7 |
| MGT | 10 | 0.99 | 8.798e−7 | 8.798e−7 |

[Insert Figure 3 here]

Figure 3. (a) sup over k of Re s versus the coupling constant ε (log–log; dotted lines mark ε = 0.0168 and 1.68). The slope is 1, as predicted by Theorem 4. (b) sup over k of Re s versus τ₁ for ε₁ = 0.01. The peaks at τ₁ = 0.001 (LS, MGT) and 5.77 × 10⁻⁴ (HDPL) are the resonances of Eq. (65). GN-II becomes unstable for τ₁ ≥ 0.0094 (Krein collision), and every model is unstable beyond τ₁ = ε₁/c_d (dotted black line).

### 4.5 Size of the growth rate

Table 5 and Fig. 4 give sup over k of Re s for the original coupling. The peak lies at k ≈ 14–35, which corresponds to wavelengths of 5–12 nm. In physical units the e-folding time is

t_e = 1 / (ω∗ sup_k Re s),                                                                                  (66)

which is 0.20 ns for LS and MGT and 0.82–1.18 ns for GN-III, HDPL and DPL-1. This is 800–4800 periods of the optical oscillation (2π/(ω∗Ω) ≈ 0.25 ps). Nanosecond heating of nanostructures, the application targeted by several KG studies, is therefore directly affected. Fig. 3(a) shows that sup Re s is proportional to ε over four decades, as Theorem 4 predicts. The coupling implied by the value of α_t printed in [32] (ε = 1.68) therefore produces rates 100 times larger. For Eringen's model (τ₁ = 0) and for classical elasticity, sup over k of Re s ≤ 0 for all six laws.

Table 5. Peak growth rate, original coupling.

| Model | sup Re s (ε = 0.0168) | at k | rate (s⁻¹) | t_e | sup Re s (ε = 1.68) |
|---|---|---|---|---|---|
| LS | 3.19e−2 | 19.8 | 4.90e9 | 0.20 ns | 3.06 |
| GN-II | 0 (neutral) | – | – | – | 38.3 (k ≈ 128) |
| GN-III | 7.93e−3 | 34.7 | 1.22e9 | 0.82 ns | 0.79 |
| DPL-1 | 5.50e−3 | 34.7 | 8.44e8 | 1.18 ns | 0.55 |
| HDPL | 6.52e−3 | 13.7 | 1.00e9 | 1.00 ns | 0.65 |
| MGT | 3.22e−2 | 19.8 | 4.95e9 | 0.20 ns | 3.08 |

[Insert Figure 4 here]

Figure 4. Maximum growth rate Re s versus wavenumber for the original coupling: (a) ε = 0.0168, (b) ε = 1.68. The dotted grey line in (a) is the LS small-k law, Eq. (47), with slope k⁴. GN-II is neutral in (a) and unstable near k ≈ 128 in (b).

### 4.6 Dependence on τ₁ and the Eringen limit

Fig. 3(b) shows sup Re s as a function of τ₁ for fixed ε₁ = 0.01. Away from the resonances (65), the growth rate of LS, MGT and HDPL decreases rapidly as τ₁ → 0. For LS it falls from 3.2 × 10⁻² at τ₁ = 0.006 to 1.3 × 10⁻⁷ at τ₁ = 10⁻⁴, close to the scaling τ₁⁴ that follows from Eq. (47) with q² ≈ τ_qΩ² + iΩ. GN-III is the exception: its growth rate decreases only slowly, to 1.6 × 10⁻³ at τ₁ = 10⁻⁴, so the limit τ₁ → 0 is singular for that law. At τ₁ = ε₁/c_d = 0.01 all models jump to rates of order 0.1–0.5, and beyond it the purely elastic instability of Proposition 2 takes over.

GN-II is neutral for τ₁ ≤ 0.0092. For τ₁ ≥ 0.0094 it becomes strongly unstable (sup Re s = 2.5 at τ₁ = 0.0094 and k ≈ 138). At these values the optical elastic branch crosses the GN-II thermal branch, whose speed is C_T = 1. Two branches of opposite energy sign then collide and form a complex-conjugate pair: a Krein collision [38,41]. The same mechanism produces the GN-II instability at ε = 1.68 in Table 5.

### 4.7 Damping does not cure the instability

Two natural regularizations make the instability worse. The first adds damping to the KG operator:

(1 − ε₁²∇² + τ_d∂ₜ + τ₁²∂ₜ²) σ = C∇u − γΘI.                                                               (67)

With τ_d = 10⁻⁵, sup Re s = 1.2–1.7 × 10⁻² for every heat law, including GN-II and the purely elastic case. The term τ_d∂ₜ acts as a negative viscosity on the acoustic branch.

The second adds Kelvin–Voigt viscosity to the local stress:

(1 − ε₁²∇² + τ₁²∂ₜ²) σ = (1 + η∂ₜ)C∇u − γΘI.                                                             (68)

At large k, Eq. (68) replaces −k² in Eq. (16) by −k²(1 + ηs). Perturbing the optical root s ≈ i v_n k gives the growth rate

Re s → η / (2ε₁²)   (k → ∞).                                                                                (69)

For η = 10⁻⁵, Eq. (69) gives 0.0500, equal to the numerical value for all six heat laws and for γ = 0. Both results follow from the mechanism of Section 4.3: dissipation acting on E₀ feeds the negative-energy branch.

Table 6. Regularizations (sup over k of Re s).

| Variant | LS | GN-II | GN-III | DPL-1 | HDPL | MGT | γ = 0 |
|---|---|---|---|---|---|---|---|
| none (τ₁ = 0.006) | 3.2e−2 | 0 | 7.9e−3 | 5.5e−3 | 6.5e−3 | 3.2e−2 | 0 |
| KG damping, τ_d = 10⁻⁵ | 1.24e−2 | 1.61e−2 | 1.24e−2 | 1.33e−2 | 1.39e−2 | 1.24e−2 | 1.74e−2 |
| Kelvin–Voigt, η = 10⁻⁵ | 5.00e−2 | 5.00e−2 | 5.00e−2 | 5.00e−2 | 5.00e−2 | 5.00e−2 | 5.00e−2 |

### 4.8 A two-oscillator picture

The instability can be understood without Fourier analysis. Eq. (1) is an equation for the stress, of the form τ₁²σ̈ + σ − ε₁²∇²σ = C∇u − γΘI. In time, each point of the solid carries a stress oscillator of natural frequency 1/τ₁, driven by the local elastic stress. Spatially, neighbouring oscillators are connected by the term ε₁²∇²σ.

On the acoustic branch the oscillator is driven below resonance, and the stress follows the strain in phase. This is ordinary elasticity with a softened, dispersive stiffness. On the optical branch the oscillator is driven above resonance, and the stress is in antiphase with the strain. The mechanical power σ:ė then has the opposite sign to the kinetic and strain energies it would supply in a classical solid. Proposition 1 makes this sign change precise.

Heat conduction removes energy at a rate proportional to the square of the temperature gradient. On the optical branch, the energy removed comes from a reservoir whose physical energy is already negative, so the amplitude grows. The same reasoning explains why the Kelvin–Voigt and KG-damping regularizations of Section 4.7 fail. Any dissipation that acts on the physical energy E₀ feeds the optical branch, and the only remedy is to change what the dissipation acts on. This is what the coupling of Section 5 does.

This picture also explains the resonance (65). Heat is removed most efficiently from an elastic wave whose phase speed matches the thermal front speed, because the temperature and strain fields then stay in step over many wavelengths. When the optical branch has the thermal front speed, the transfer of energy from the negative-energy mode to dissipation is largest.

## 5. An energy-consistent coupling

Theorem 1 and Eq. (37) show that E_b, not E₀, is the positive energy of elastic KG. A coupling consistent with it replaces the energy balance (4) by

ρ c Θ̇ + γ T₀ ∇·(u̇ + b u⃛) + div q = 0.                                                                   (70)

Multiplying Eq. (3) by u̇ + bu⃛ and Eq. (70) by Θ/T₀, the coupling terms γ∫Θ ∇·(u̇ + bu⃛) cancel exactly, and

d/dt [E_b + E_θ] = (1/T₀) ∫ q·∇Θ dx.                                                                      (71)

**Theorem 5 (stability of the modified coupling).** For Eqs. (3) and (70) with the Fourier, LS, GN-II or GN-III law, d/dt[E_b + E_θ] = −𝒟 ≤ 0, with E_θ and 𝒟 as in Theorem 2. If τ₁² < b < ε₁²/c_d², then E_b + E_θ is positive definite and the system is Lyapunov stable.

*Proof.* Combine Eq. (71) with Eqs. (43)–(45) and Theorem 1. ∎

In Fourier variables the modified coupling replaces εk²b(s) in Eq. (15) by εk²(1 + bs²)b(s):

D_P^b(s, k) = [b(s) + k²a(s)] E(s, k) − ε k² (1 + b s²) b(s).                                               (72)

For MGT, DPL-1 and HDPL an energy proof requires additional multipliers, as in the local theory [12,17]; we have not carried it out. Instead we computed sup over k ∈ [0.1, 10⁴] of Re s for 33 values of b (Fig. 5 and Table 7). For all five dissipative laws the system is stable (sup Re s ≤ 10⁻¹⁵, round-off) for 4.0 × 10⁻⁵ ≤ b ≤ 1.0 × 10⁻⁴. It is unstable for b ≤ 3.5 × 10⁻⁵ and for b ≥ 1.05 × 10⁻⁴. The numerical window therefore coincides with the theoretical window [τ₁², ε₁²] = [3.6 × 10⁻⁵, 10⁻⁴]. We conjecture that Theorem 5 extends to MGT under κ > τ_qC_T² and to HDPL under 2τ_T > τ_q.

Table 7. Energy-consistent coupling: sup over k of Re s versus b.

| b | LS | GN-III | DPL-1 | HDPL | MGT |
|---|---|---|---|---|---|
| 0 (original) | 3.2e−2 | 7.9e−3 | 5.5e−3 | 6.5e−3 | 3.2e−2 |
| 2.0e−5 | 1.4e−2 | 3.3e−3 | 2.3e−3 | 2.9e−3 | 1.4e−2 |
| 3.5e−5 | 2.3e−4 | 7.5e−5 | 5.9e−5 | 1.2e−4 | 2.3e−4 |
| 4.0e−5 to 1.0e−4 | ≤ 1e−15 | ≤ 1e−15 | ≤ 1e−15 | ≤ 1e−15 | ≤ 1e−15 |
| 1.05e−4 | 7.8e−6 | 7.8e−6 | 6.0e−6 | 4.8e−6 | 7.7e−6 |
| 1.6e−4 | 7.3e−4 | 7.2e−4 | 5.7e−4 | 4.6e−4 | 7.2e−4 |

[Insert Figure 5 here]

Figure 5. Energy-consistent coupling, Eq. (70): sup over k ∈ [0.1, 10⁴] of Re s versus b, for the five dissipative heat laws. The shaded window τ₁² ≤ b ≤ ε₁²/c_d² is stable; outside it the system is unstable.

Eq. (70) states that the heat balance sees the strain rate filtered by a temporal operator of the same kind as the one in the KG stress law. It is the minimal change that makes the coupling consistent with a positive energy. Whether it can be derived from a nonlocal Clausius–Duhem inequality is an open question.

The modification also changes the principal part for LS and MGT, because the coupling term εbk²s²b(s) then reaches the highest order. For LS the characteristic speeds v solve

τ_qτ₁² v⁴ − (τ_qε₁² + κτ₁² + εbτ_q) v² + κε₁² = 0.                                                         (73)

For b = 6 × 10⁻⁵ this gives v = 10.0014 and 1.6662, in agreement with the numerical value 10.0014. The shift relative to the original coupling is O(εb), so the domain of influence of Section 6 is essentially unchanged.

## 6. Domain of influence

A constant-coefficient operator P(∂ₜ, ∇) is hyperbolic with respect to t in Gårding's sense [33,34] if its principal part p satisfies p(1, 0) ≠ 0, the roots of p in s are purely imaginary for real k, and

sup { Re s : P(s, ik) = 0, k ∈ ℝ³ } < ∞.                                                                   (74)

Gårding's theorem states that P then has a unique forward fundamental solution, supported in the dual cone of the hyperbolicity cone of p. It also states the converse: if P is not hyperbolic, no forward fundamental solution supported in a proper cone exists. For systems the theorem is applied to the determinant, here D_P·D_S [34,35]. Condition (74) allows a bounded instability, so it is satisfied by the original KG coupling: Section 4 shows that Re s is bounded and decays like k⁻².

**Theorem 6 (domain of influence).** Let τ₁ > 0.

(a) For LS, MGT, GN-II and HDPL, the principal part of D_P·D_S is, up to sign,

p(s, k) = s⁴ (τ₁²s² + ε₁²k²)² p_θ(s, k),                                                                  (75)

where p_θ = τ_qs² + κk² (LS), s(τ_qs² + κk²) (MGT), s² + C_T²k² (GN-II) or s(τ_q²s²/2 + κτ_Tk²) (HDPL). Solutions with data supported in a ball of radius R then vanish outside the ball of radius R + V∗t, where

V∗ = max(ε₁/τ₁, v_θ),   v_θ = 1/√τ_q (LS), √(κ/τ_q) (MGT), C_T (GN-II), √(2κτ_T)/τ_q (HDPL).                (76)

(b) For GN-III and DPL-1 the principal part of the heat factor is κk²s and κτ_Tk²s, respectively. It vanishes at (s, k) = (1, 0), so P is not hyperbolic and the speed of propagation is infinite.

(c) For Eringen's model (τ₁ = 0, ε₁ > 0), the elastic factor of the principal part is ε₁²k²s². It also vanishes at (1, 0), so the speed is infinite for every heat law. Directly, the elastic Eringen equation can be written as

ü = c² Δ (I − ε₁²Δ)⁻¹ u,   (I − ε₁²Δ)⁻¹ f = ∫ e^(−|x−y|/ε₁) f(y) dy / (4πε₁²|x − y|),                      (77)

whose kernel is positive everywhere. A disturbance at one point is felt instantly at every other point.

*Proof.* Count degrees in Eq. (15). The coupling term εk²b has degree at least two less than (b + k²a)E for every model in Table 2, so it does not enter the principal part. A product of hyperbolic polynomials is hyperbolic, and its hyperbolicity cone is the intersection of the individual cones. A factor with characteristic speeds 0 and v has a cone whose dual is {|x| ≤ vt}. The intersection is dual to the ball of the largest speed, which gives Eq. (76). Parts (b) and (c) follow because p(1, 0) = 0. ∎

For the data used, V∗ = 10 (LS, MGT), 1.667 (GN-II, where ε₁/τ₁ > C_T = 1) and 17.32 (HDPL), in units of c_d. Table 8 compares these bounds with the ratio max |Im s|/k at k = 10⁶. They agree to four digits whenever the bound is finite. For GN-III and DPL-1 the ratio is 1.667, because their phase speeds are finite. Their diffusive roots, however, have Re s ∝ −k², and this is what makes the speed infinite. LS and MGT share the same principal part and so the same front speed, which is the structural reason why they give nearly identical wave results in [32].

Table 8. Wavefront speed: Gårding bound (76) against the numerical ratio max(abs Im s)/k at k = 10⁶.

| Model | KG bound | KG numeric | Eringen bound | Eringen numeric |
|---|---|---|---|---|
| LS | 10.000 | 10.000 | ∞ | 10.000 |
| GN-II | 1.6667 | 1.6667 | ∞ | 1.0000 |
| GN-III | ∞ | 1.6667 | ∞ | 0.0001 |
| DPL-1 | ∞ | 1.6667 | ∞ | 0.0001 |
| HDPL | 17.321 | 17.321 | ∞ | 17.321 |
| MGT | 10.000 | 10.000 | ∞ | 10.000 |

Table 9 collects the results of Sections 3–6.

Table 9. Summary of stability and propagation (data of Table 1, ε = 0.0168).

| Framework | Heat law | Spectrally stable? | Front speed |
|---|---|---|---|
| Classical | all six | yes | finite (LS, MGT, GN-II, HDPL) or infinite (GN-III, DPL-1) |
| Eringen (τ₁ = 0) | all six | yes | infinite |
| KG, original coupling | LS, GN-III, DPL-1, HDPL, MGT | no (t_e = 0.2–1.2 ns) | V∗ of Eq. (76), or infinite (GN-III, DPL-1) |
| KG, original coupling | GN-II | yes for τ₁ ≤ 0.0092; no otherwise | 1.667 |
| KG, modified coupling (70) | all six | yes for τ₁² ≤ b ≤ ε₁²/c_d² | shifted by O(εb) |

## 7. Numerical method

The roots of D_P (degree 6–7 in s), D_P^b and D_S (degree 4) were computed by Aberth–Ehrlich iteration on a rescaled polynomial, followed by Newton polishing, using the Python standard library only. The largest relative backward error over all models and wavenumbers was 3.8 × 10⁻¹⁶. Each analytical result was checked against these roots:

- band edges (39) and growth rate (41): three to four digits;
- small-k law (47): four digits (Table 3);
- first-order law (61): within 0.12% for k ≥ 0.1 (Fig. 2);
- large-k law (63): four digits (Table 4);
- Kelvin–Voigt rate (69): exact;
- front speeds (76): four digits (Table 8).

Wavenumbers were sampled on logarithmic grids of 90–600 points between 10⁻² and 10⁸.

Two further checks were made on the numerical results. First, resolution in k: the peak values in Table 5 changed by less than 0.1% when the grid on 10⁻² ≤ k ≤ 10⁵ was refined from 260 to 600 points, and the peak wavenumbers moved by less than one grid spacing. The resonance peaks of Fig. 3(b) are narrow, so the resonant values of τ₁ given by Eq. (65) were added to the grid explicitly. Without them, a uniform grid can underestimate the peak height by an order of magnitude.

Second, branch identification: every reported growth rate belongs to a root that continues the optical branch of the uncoupled problem. We confirmed this by tracking the roots in ε from 0 to 0.0168 at fixed k, and by checking that |Im s| agrees with the optical frequency ω_o(k) to O(ε). The acoustic and thermal roots have Re s < 0 throughout, in agreement with Eq. (62) and with the dissipativity of the heat laws.

All numerical claims in the text can be reproduced, without modification, by running the scripts listed in Appendix A. Each table entry is written to the numerical summary file with more digits than are quoted here.

## 8. Discussion and conclusions

### 8.1 Interpretation

The KG operator introduces a second oscillator into the stress. On the optical branch that oscillator moves in antiphase with the displacement in a way that makes the physical energy negative (Proposition 1). In a closed, non-dissipative system this is harmless, because a conserved positive energy E_b exists (Theorem 1). Thermodynamics, however, only requires E₀ + E_θ to decrease (Theorem 2). For a negative-energy mode, that decrease means growth. KG thermoelasticity with the original coupling is therefore inconsistent with dissipation: the better a heat law dissipates, the more certainly the optical branch grows (Corollary 2, Theorem 4).

### 8.2 Consequences for published work

Transient KG thermoelastic solutions are usually obtained in the Laplace domain and inverted numerically. Standard inversion algorithms assume that all singularities lie to the left of the Bromwich contour [42]. With poles in Re s > 0, a fixed inversion abscissa can hide the growth or produce spurious results. Finite-time simulations can likewise be contaminated by the growing mode. We have not re-examined any specific published study. We recommend that KG transient results be checked for poles with Re s > 0, and that parameter choices be checked against τ₁c_d < ε₁ and against the resonance (65).

### 8.3 Limitations

The analysis is linear, isotropic and posed on the whole space. Bounded domains require additional boundary conditions in differential nonlocal models. The energy proof of the modified coupling covers four of the six heat laws; for MGT, DPL-1 and HDPL the result is numerical. The coupling (70) is motivated by the energy argument and has not been derived from a thermodynamic principle. The physical parameters (ε₁, τ₁) used here are those of [32]. They place the optical branch in the terahertz range, where a continuum model is at best a fit. All conclusions about the existence of the instability, however, hold for any τ₁ > 0 and any dissipative heat law. Finally, the analysis concerns the linear problem. Nonlinear effects, such as temperature-dependent moduli or large deformations, could saturate the growth, but they cannot remove it at small amplitude: the linear growth rate sets the time scale on which any small perturbation of the optical branch, including numerical round-off, becomes visible. A nonlinear analysis would be needed to determine the amplitude at which the growth saturates.

### 8.4 Comparison with other nonlocal and gradient models

The instability found here is specific to models that make the stress a dynamical variable with its own inertia. Eringen's differential model (τ₁ = 0) has no optical branch, and its energy (32) with τ₁ = 0 is positive. It is stable for every heat law (Table 9), but it pays for this with an infinite speed of propagation (Theorem 6c).

Stable gradient models with a finite propagation speed do exist. Askes and Aifantis [28] discuss gradient-elastic formulations that contain both a stiffness gradient and an inertia gradient. Their energies are positive by construction, and their dispersion relations have one branch per polarization. The KG model differs in that its time scale τ₁ adds a second branch, and that branch carries negative physical energy.

A positive conserved energy can be restored in two ways. One is to restrict the model to the acoustic branch, as an effective theory valid well below 1/τ₁. The other is to change the coupling, as in Section 5. A third possibility, which we have not explored, is to reformulate KG nonlocality with an internal variable that carries its own positive energy, in the spirit of micromorphic models. Any such reformulation should be checked against Proposition 1 before it is coupled to dissipative heat conduction.

### 8.5 Recommendations

For practitioners using KG thermoelasticity, the results suggest the following checks:

- Verify τ₁c_d < ε₁ (P waves) and τ₁c_s ≤ ε₁ (S waves). Otherwise the elastic model itself is unstable (Proposition 2).
- If the heat law is dissipative, estimate the growth rate from Eq. (61), or from Eq. (47) at small wavenumbers, and compare the e-folding time (66) with the time window of the simulation.
- Avoid τ₁ ≈ ε₁/v_θ, the resonance (65), where the growth rate is largest.
- In Laplace-domain solutions, locate all poles of the transformed solution before choosing the inversion abscissa [42].
- Do not add viscosity to suppress the growth (Section 4.7). If a stable model is required, use the modified coupling (70) with τ₁² ≤ b ≤ ε₁²/c_d², or restrict the analysis to frequencies well below 1/τ₁.
- Use the physical thermal expansion coefficient. The value printed in [32] overstates the coupling, and all growth rates, by a factor of 100.

### 8.6 Conclusions

1. Elastic KG is stable, with unique solutions, if and only if τ₁c_d < ε₁. The "if" direction follows from the conserved energies E_b; the "only if" direction from the explicit growth band (39)–(41). For shear waves, τ₁c_s ≤ ε₁ is necessary for every thermoelastic variant.
2. The physical energy of a plane mode is ½|A|²ω²∂D/∂(ω²): positive on the acoustic branch and negative on the optical branch.
3. Every dissipative heat law makes the optical branch grow. The growth rate is given at all wavenumbers by Eq. (61) to within 0.12%. It scales like k⁴ at small k and like k⁻² at large k, and it resonates when ε₁/τ₁ equals the thermal front speed. For copper the e-folding time is 0.2–1.2 ns.
4. GN-II is neutral at the physical coupling for τ₁ ≤ 0.0092. It becomes unstable through a Krein collision when the optical and thermal branches cross.
5. Viscous damping, whether added to the KG operator or as Kelvin–Voigt viscosity, increases the instability.
6. Coupling the heat equation to ∇·(u̇ + bu⃛) with τ₁² ≤ b ≤ ε₁²/c_d² gives a positive, non-increasing energy. Stability is proved for Fourier, LS, GN-II and GN-III and verified numerically for MGT, DPL-1 and HDPL.
7. With τ₁ > 0 and an LS, MGT, GN-II or HDPL heat law, disturbances travel at most at V∗ = max(ε₁/τ₁, v_θ). GN-III, DPL-1 and Eringen's model have infinite speed. LS and MGT share their principal part and front speed.

Open problems are a thermodynamic derivation of the coupling (70), energy proofs for MGT and the dual-phase-lag laws, bounded domains, and calibration of (ε₁, τ₁) against measured dispersion, so that the conditions found here can be checked for real materials.

To convert the non-dimensional results of this paper to physical units, use

t_phys = t/ω∗,   x_phys = x l∗,   (Re s)_phys = ω∗ Re s.                                                    (78)

## Appendix A. Reproducibility

The following scripts in this repository use the Python 3 standard library only:

- `kg_thermoelastic_core.py`: polynomials (15)–(17), root finder, growth bands, wavefront speeds;
- `kg_plot.py`: plotting helper;
- `generate_kg_stability_figures.py`: Figs. 1–5 and `kg_stability_figures/numerical_summary.txt`, from which Tables 3–8 are taken.

## References

[1] Duhamel JMC. Second mémoire sur les phénomènes thermo-mécaniques. J Éc Polytech. 1837;15(25):1–57.

[2] Biot MA. Thermoelasticity and irreversible thermodynamics. J Appl Phys. 1956;27(3):240–253.

[3] Cattaneo C. Sur une forme de l'équation de la chaleur éliminant le paradoxe d'une propagation instantanée. C R Acad Sci Paris. 1958;247:431–433.

[4] Vernotte P. Les paradoxes de la théorie continue de l'équation de la chaleur. C R Acad Sci Paris. 1958;246:3154–3155.

[5] Lord HW, Shulman Y. A generalized dynamical theory of thermoelasticity. J Mech Phys Solids. 1967;15:299–309.

[6] Green AE, Lindsay KA. Thermoelasticity. J Elasticity. 1972;2(1):1–7.

[7] Green AE, Naghdi PM. A re-examination of the basic postulates of thermomechanics. Proc R Soc Lond A. 1991;432:171–194.

[8] Green AE, Naghdi PM. On undamped heat waves in an elastic solid. J Therm Stresses. 1992;15(2):253–264.

[9] Green AE, Naghdi PM. Thermoelasticity without energy dissipation. J Elasticity. 1993;31(3):189–208.

[10] Tzou DY. A unified field approach for heat conduction from macro- to micro-scales. J Heat Transfer. 1995;117(1):8–16.

[11] Chandrasekharaiah DS. Hyperbolic thermoelasticity: a review of recent literature. Appl Mech Rev. 1998;51(12):705–729.

[12] Quintanilla R. Moore–Gibson–Thompson thermoelasticity. Math Mech Solids. 2019;24(12):4020–4031.

[13] Conti M, Pata V, Quintanilla R. Thermoelasticity of Moore–Gibson–Thompson type with history dependence in the temperature. Asymptot Anal. 2020;120(1–2):1–21.

[14] Bazarra N, Fernández JR, Quintanilla R. Analysis of a Moore–Gibson–Thompson thermoelastic problem. J Comput Appl Math. 2021;382:113058.

[15] Kaltenbacher B, Lasiecka I, Marchand R. Wellposedness and exponential decay rates for the Moore–Gibson–Thompson equation arising in high intensity ultrasound. Control Cybern. 2011;40(4):971–988.

[16] Quintanilla R, Racke R. A note on stability in dual-phase-lag heat conduction. Int J Heat Mass Transfer. 2006;49(7–8):1209–1213.

[17] Quintanilla R, Racke R. Qualitative aspects in dual-phase-lag thermoelasticity. SIAM J Appl Math. 2006;66(3):977–1001.

[18] Fabrizio M, Franchi F. Delayed thermal models: stability and thermodynamics. J Therm Stresses. 2014;37(2):160–173.

[19] Dafermos CM. On the existence and the asymptotic stability of solutions to the equations of linear thermoelasticity. Arch Ration Mech Anal. 1968;29(4):241–271.

[20] Carlson DE. Linear thermoelasticity. In: Truesdell C, editor. Handbuch der Physik, Vol. VIa/2. Berlin: Springer; 1972. p. 297–345.

[21] Ieşan D. Thermoelastic Models of Continua. Dordrecht: Kluwer; 2004.

[22] Jangid K, Mukhopadhyay S. A domain of influence theorem under MGT thermoelasticity theory. Math Mech Solids. 2021;26(2):285–295.

[23] Jangid K, Gupta M, Mukhopadhyay S. On propagation of harmonic plane waves under the Moore–Gibson–Thompson thermoelasticity theory. Waves Random Complex Media. 2024;34(3):1976–1999.

[24] Eringen AC. Linear theory of nonlocal elasticity and dispersion of plane waves. Int J Eng Sci. 1972;10(5):425–435.

[25] Eringen AC. On differential equations of nonlocal elasticity and solutions of screw dislocation and surface waves. J Appl Phys. 1983;54(9):4703–4710.

[26] Eringen AC. Nonlocal Continuum Field Theories. New York: Springer; 2002.

[27] Challamel N, Rakotomanana L, Le Marrec L. A dispersive wave equation using nonlocal elasticity. C R Mécanique. 2009;337(8):591–595.

[28] Askes H, Aifantis EC. Gradient elasticity in statics and dynamics: an overview of formulations, length scale identification procedures, finite element implementations and new results. Int J Solids Struct. 2011;48(13):1962–1990.

[29] Lazar M, Agiasofitou E. Nonlocal elasticity of Klein–Gordon type: fundamentals and wave propagation. Wave Motion. 2022;114:103038.

[30] Lazar M, Agiasofitou E. Nonlocal elasticity of Klein–Gordon type with internal length and time scales: constitutive modelling and dispersion relations. KIT Open Repository; https://publikationen.bibliothek.kit.edu/1000165899 (journal version to be confirmed before submission).

[31] Singh B. Wave propagation in context of Moore–Gibson–Thompson thermoelasticity with Klein–Gordon nonlocality. Vietnam J Mech. 2024;46(2):104–118.

[32] Mondal S, Mukhopadhyay S. Modeling and analysis of wave propagation under generalized Klein–Gordon nonlocal thermoelasticity theories. Mech Mater. 2026;222:105834.

[33] Gårding L. Linear hyperbolic partial differential equations with constant coefficients. Acta Math. 1951;85:1–62.

[34] Hörmander L. The Analysis of Linear Partial Differential Operators II: Differential Operators with Constant Coefficients. Berlin: Springer; 1983.

[35] Courant R, Hilbert D. Methods of Mathematical Physics, Vol. II: Partial Differential Equations. New York: Interscience; 1962.

[36] Pazy A. Semigroups of Linear Operators and Applications to Partial Differential Equations. New York: Springer; 1983.

[37] Cairns RA. The role of negative energy waves in some instabilities of parallel flows. J Fluid Mech. 1979;92(1):1–14.

[38] MacKay RS. Movement of eigenvalues of Hamiltonian equilibria under non-Hamiltonian perturbation. Phys Lett A. 1991;155(4–5):266–268.

[39] Bloch AM, Krishnaprasad PS, Marsden JE, Ratiu TS. Dissipation induced instabilities. Ann Inst H Poincaré Anal Non Linéaire. 1994;11(1):37–90.

[40] Krechetnikov R, Marsden JE. Dissipation-induced instabilities in finite dimensions. Rev Mod Phys. 2007;79(2):519–553.

[41] Kirillov ON. Nonconservative Stability Problems of Modern Physics. Berlin: De Gruyter; 2013.

[42] Abate J, Whitt W. A unified framework for numerically inverting Laplace transforms. INFORMS J Comput. 2006;18(4):408–421.
