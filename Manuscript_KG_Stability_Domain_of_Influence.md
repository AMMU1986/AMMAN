# Energy, Dissipation-Induced Instability and Domain of Influence in Klein–Gordon Nonlocal Thermoelasticity: A Unified Analysis of Six Non-Fourier Heat Conduction Models

**Draft manuscript (Paper B)**, prepared as a follow-up to Mondal and Mukhopadhyay, *Mechanics of Materials* 222 (2026) 105834.

---

## Abstract

Klein–Gordon (KG) nonlocal elasticity, (1 − ε₁²∇² + τ₁²∂ₜ²)σ = C:e − γΘI, is now widely combined with generalized heat conduction. Its well-posedness and stability have not been examined. We study the linear problem on ℝ³ for six heat laws: Lord–Shulman (LS), Green–Naghdi II and III (GN-II, GN-III), dual-phase-lag (DPL-1), hyperbolic dual-phase-lag (HDPL) and Moore–Gibson–Thompson (MGT). We obtain five results.

(i) The purely elastic KG equation conserves a family of energies E_b. For τ₁² < b < ε₁²/c_d², E_b is positive definite, so the elastic problem is stable and has unique solutions whenever τ₁c_d < ε₁. If τ₁c > ε₁ for c = c_d or c_s, there is an explicit band of wavenumbers, (τ₁c ± √(τ₁²c² − ε₁²))/ε₁², in which solutions grow exponentially. For shear waves this criterion is exact for every heat law, because they decouple from temperature.

(ii) The physical energy, the one whose decrease thermodynamics guarantees, is the member b = 0. It is indefinite, and it is negative on the optical branch that KG nonlocality creates near frequency 1/τ₁.

(iii) Consequently, every dissipative heat law destabilizes KG thermoelasticity, even when τ₁c_d < ε₁. For small wavenumbers the optical branch grows at the rate Re s = −(ε k⁴ τ₁/2) Im[a(i/τ₁)/b(i/τ₁)], where a and b are the heat-law polynomials. This is positive for LS, GN-III and DPL-1, and for MGT and HDPL exactly when their own stability conditions hold. Only the non-dissipative GN-II model remains stable, and only for weak coupling. For the copper data used in the literature the e-folding time is 0.2–1.2 ns. Adding Kelvin–Voigt viscosity, or a damping term in the KG operator, makes the instability worse.

(iv) If the heat equation is coupled to ∇·(u̇ + b u⃛) instead of ∇·u̇, the cross terms cancel against E_b, and the system is stable for τ₁² ≤ b ≤ ε₁²/c_d². This is proved for the Fourier, LS, GN-II and GN-III laws and verified numerically for MGT, DPL-1 and HDPL.

(v) By Gårding's theorem, disturbances stay within |x| ≤ V∗t with V∗ = max(ε₁/τ₁, v_θ), where v_θ = 1/√τ_q for LS and MGT, C_T for GN-II and √(2τ_T)/τ_q for HDPL. Speeds are infinite for GN-III, DPL-1 and for Eringen's model (τ₁ = 0).

KG nonlocality therefore restores a finite speed of propagation that Eringen's differential model lacks, but only at the price of a negative-energy branch that is incompatible with dissipation unless the coupling is modified.

**Keywords:** Klein–Gordon nonlocal elasticity; well-posedness; energy method; dissipation-induced instability; negative-energy waves; domain of influence; Gårding hyperbolicity; Moore–Gibson–Thompson; dual-phase-lag

---

## 1. Introduction

Nonlocal elasticity of Klein–Gordon type [1,2] adds an internal time τ₁ to Eringen's internal length ε₁ [3]. The constitutive operator becomes 1 − ε₁²∇² + τ₁²∂ₜ². The time term produces an optical-like dispersion branch and a frequency gap, which makes the model attractive for metamaterials and lattice-like media [1,2]. Since 2024 the operator has been coupled with MGT heat conduction [4], with memory-dependent and fractional variants [5–7], and, most recently, with six non-Fourier heat laws in one framework [8].

These studies compute plane-wave dispersion or Laplace-domain transient responses, but none examines whether the coupled initial-value problem is well-posed or stable. This matters for two reasons.

- The displacement equation becomes fourth order in time (ρτ₁² ∂ₜ⁴u). Its natural energy contains the indefinite term −½ρτ₁²|ü|².
- For constant-coefficient problems, the propagation speeds of a well-posed system are fixed by its principal part [9,10]. For the GN-type heat laws there are domain-of-influence results [11]; their KG analogues are unknown.

For thermoelasticity with GN-III, DPL and MGT heat laws, well-posedness and stability have been settled in the local case [12–15]. This paper does the same for KG nonlocality. The main finding is negative: dissipation destabilizes the KG optical branch. This is the dissipation-induced instability of negative-energy modes familiar from fluid and plasma physics [16–18]. We also identify a modified coupling that removes it.

Section 2 states the model. Section 3 treats the purely elastic KG equation. Section 4 derives the physical energy identity and the instability. Section 5 presents the energy-consistent coupling. Section 6 gives the domain of influence. Section 7 presents numerical verification, and Section 8 discusses consequences.

## 2. Model

We use the notation of [8] and of Paper A. In dimensional form,

ρ(1 − ε₁²∇² + τ₁²∂ₜ²) ü = div(C∇u) − γ∇Θ,                                                   (1)

ρcΘ̇ + γT₀ ∇·u̇ + div q = 0,                                                                (2)

where C is the isotropic elasticity tensor (λ, μ) and q obeys one of the following laws:

- Fourier: q = −k∇Θ
- LS: (1 + τ_q∂ₜ)q = −k∇Θ
- GN-II: q = −k∗∇ν, with ν̇ = Θ
- GN-III: q = −k∇Θ − k∗∇ν
- MGT: (1 + τ_q∂ₜ)q = −k∇Θ − k∗∇ν
- DPL-1 and HDPL: (1 + τ_q∂ₜ [+ τ_q²∂ₜ²/2])q = −k(1 + τ_T∂ₜ)∇Θ

We assume μ > 0 and λ + μ ≥ 0 (true for copper), so that, for fields decaying at infinity,

μ‖∇v‖² ≤ ⟨C∇v, ∇v⟩ ≤ (λ + 2μ)‖∇v‖²,                                                       (3)

where ⟨C∇v, ∇v⟩ = ∫(λ+2μ)(div v)² + μ|curl v|² dx and ‖·‖ is the L²(ℝ³) norm.

For the Fourier-mode analysis we use the non-dimensional form of Paper A. Write c_d = 1, s for the temporal exponent (fields ∝ exp(st + ik·x)), coupling ε = γ²T₀/(ρc(λ+2μ)), and the heat polynomials a(s), b(s) of Table 1. The P-wave and S-wave characteristic polynomials are

D_P(s, k) = [b(s) + k²a(s)] E(s, k) − ε k² b(s),   E = −k² − (1 + ε₁²k²)s² − τ₁²s⁴,             (4)

D_S(s, k) = τ₁²s⁴ + (1 + ε₁²k²)s² + c_s²k².                                                   (5)

Table 1. Heat-law polynomials (non-dimensional; κ = k/k_ref, C_T² = k∗/(ρcV²)).

| Model | a(s) | b(s) |
|---|---|---|
| LS | κ | s(1 + τ_q s) |
| GN-II | C_T² | s² |
| GN-III | C_T² + κ s | s² |
| MGT | C_T² + κ s | s²(1 + τ_q s) |
| DPL-1 | κ(1 + τ_T s) | s(1 + τ_q s) |
| HDPL | κ(1 + τ_T s) | s(1 + τ_q s + τ_q²s²/2) |

The data are those of [8]: ε₁ = 0.01, τ₁ = 0.006, τ_q = 0.01 and τ_T = 0.015. For copper, C_T² = 1.000 and c_s = 0.4994. We take α_t = 1.78 × 10⁻⁵ K⁻¹, giving ε = 0.0168. The value printed in [8], 1.78 × 10⁻⁴ K⁻¹, gives ε = 1.68, and we report it for comparison. The reference frequency is ω∗ = 1.536 × 10¹¹ s⁻¹.

## 3. The purely elastic KG equation

### 3.1 A family of conserved energies

**Theorem B1.** Let γ = 0, and let u be a smooth solution of Eq. (1) decaying with its derivatives at infinity. For every real b, the quantity

E_b(t) = ½ ∫ { ρ|u̇|² + 2ρτ₁² u̇·u⃛ + ρbτ₁²|u⃛|² + ρ(b − τ₁²)|ü|² + ρε₁²|∇u̇|² − b C∇u̇:∇u̇ + ρbε₁²|∇ü|² + C∇u:∇u + 2b C∇u:∇ü } dx      (6)

is conserved. If

τ₁² < b < ε₁²ρ/(λ + 2μ) = ε₁²/c_d²,                                                              (7)

then E_b is equivalent to the squared norm N(t) = ‖u̇‖² + ‖ü‖² + ‖u⃛‖² + ‖∇u‖² + ‖∇u̇‖² + ‖∇ü‖². Such a b exists if and only if τ₁c_d < ε₁.

*Proof.* Take the L² inner product of Eq. (1) with u̇ + b u⃛ and integrate by parts. The four groups of terms are:

- ρ∫ü·(u̇ + bu⃛) = d/dt ρ∫(½|u̇|² + ½b|ü|²);
- −ρε₁²∫∇²ü·(u̇ + bu⃛) = d/dt ρε₁²∫(½|∇u̇|² + ½b|∇ü|²);
- ρτ₁²∫u⁗·(u̇ + bu⃛) = d/dt ρτ₁²∫(u⃛·u̇ − ½|ü|² + ½b|u⃛|²);
- −∫div(C∇u)·(u̇ + bu⃛) = d/dt ∫(½C∇u:∇u + bC∇u:∇ü − ½bC∇u̇:∇u̇).

Their sum is dE_b/dt = 0.

For positivity, examine the terms in groups:

- The pair (u̇, u⃛) forms the quadratic form ρ(|u̇|² + 2τ₁²u̇·u⃛ + bτ₁²|u⃛|²). It is positive definite if and only if τ₁⁴ < bτ₁², that is, b > τ₁².
- The coefficient of |ü|² is ρ(b − τ₁²) > 0.
- By Eq. (3), ρε₁²‖∇u̇‖² − b⟨C∇u̇, ∇u̇⟩ ≥ (ρε₁² − b(λ+2μ))‖∇u̇‖² > 0.
- For the pair (∇u, ∇ü), Young's inequality in the C-inner product gives 2b⟨C∇u, ∇ü⟩ ≥ −θ⟨C∇u, ∇u⟩ − (b²/θ)(λ+2μ)‖∇ü‖² for any θ ∈ (0, 1). The remainder is positive if b < θε₁²ρ/(λ+2μ). Since b < ε₁²/c_d², such a θ < 1 exists.

Finally, Eq. (3) bounds ⟨C∇u, ∇u⟩ below by μ‖∇u‖². ∎

**Corollary B1.** If τ₁c_d < ε₁, the elastic KG Cauchy problem has at most one solution in the energy space, and N(t) ≤ K N(0) for all t, with K depending only on the material constants.

Theorem B1 holds for any b. Only the choice b = 0 corresponds to the classical multiplier u̇, and therefore to the power expended by external forces:

E₀ = ½∫{ ρ|u̇|² − ρτ₁²|ü|² + 2ρτ₁² u̇·u⃛ + ρε₁²|∇u̇|² + C∇u:∇u } dx.                       (8)

E₀ is indefinite. For the spatially uniform optical oscillation u = A cos(t/τ₁), the density of E₀ is −ρ|A|²/(2τ₁²) < 0. The optical branch is therefore a negative-energy mode with respect to the physical energy.

### 3.2 Instability when τ₁c > ε₁

**Proposition B2.** For a KG wave with speed c (c_d for P, c_s for S), real wavenumbers in the band

k₋ < k < k₊,   k± = (τ₁c ± √(τ₁²c² − ε₁²)) / ε₁²,                                             (9)

give complex s², and therefore one root of D_S (or of D_P at γ = 0) with Re s > 0. The band is empty if τ₁c ≤ ε₁.

*Proof.* s² solves τ₁²s⁴ + (1 + ε₁²k²)s² + c²k² = 0. The discriminant (1 + ε₁²k²)² − 4τ₁²c²k² is a quadratic in k² whose roots are k±². ∎

Shear waves are uncoupled from Θ in all six heat laws. The condition τ₁c_s ≤ ε₁ is therefore necessary for stability of KG thermoelasticity, independently of the heat law. For the data of [8] (τ₁ = 0.006), both τ₁c_d < ε₁ and τ₁c_s < ε₁ hold. For τ₁ = 0.015 the P band is 38.2 < k < 261.8, which matches the numerical roots to four digits (Fig. 1b).

[Insert Figure 1 here]

Figure 1. Purely elastic KG P wave. (a) Temporal frequencies |Im s| of the acoustic and optical branches for τ₁ = 0.006. The optical branch starts at 1/τ₁ ≈ 166.7 and approaches slope ε₁/τ₁; the acoustic branch saturates at 1/ε₁ = 100. (b) Growth rate Re s for τ₁ = 0.012, 0.015 and 0.02 (all with τ₁c_d > ε₁). Dotted lines are the band edges of Eq. (9).

## 4. Dissipation-induced instability

### 4.1 Physical energy identity

**Theorem B3.** For the original system (1)–(2) with heat law Fourier, LS, GN-II or GN-III,

d/dt [E₀ + E_θ] = −𝒟 ≤ 0,                                                                       (10)

where E_θ and 𝒟 are:

- Fourier: E_θ = ∫ρcΘ²/(2T₀), 𝒟 = ∫k|∇Θ|²/T₀;
- LS: E_θ = ∫[ρcΘ²/(2T₀) + τ_q|q|²/(2kT₀)], 𝒟 = ∫|q|²/(kT₀);
- GN-II: E_θ = ∫[ρcΘ²/(2T₀) + k∗|∇ν|²/(2T₀)], 𝒟 = 0;
- GN-III: E_θ = ∫[ρcΘ²/(2T₀) + k∗|∇ν|²/(2T₀)], 𝒟 = ∫k|∇Θ|²/T₀.

*Proof.* Multiply Eq. (1) by u̇ and Eq. (2) by Θ/T₀, integrate, and add. The coupling terms ±γ∫Θ ∇·u̇ cancel. What remains is (1/T₀)∫q·∇Θ. Substitute each heat law:

- LS: q·∇Θ = −|q|²/k − (τ_q/2k) d/dt|q|².
- GN-II: q·∇Θ = −(k∗/2) d/dt|∇ν|².
- GN-III: −k|∇Θ|² − (k∗/2) d/dt|∇ν|². ∎

Eq. (10) is the usual thermodynamic statement: dissipation decreases the physical energy. Because E₀ is indefinite (Eq. (8)), this does not imply stability. A mode with E₀ < 0 that loses energy grows in amplitude [16–18].

### 4.2 Growth rate of the optical branch

**Theorem B4.** Let τ₁ > 0 and b(i/τ₁) ≠ 0. The optical root of D_P that equals s₀ = i/τ₁ at k = 0 is analytic in k² near k = 0, and

Re s(k) = −(ε τ₁ k⁴ / 2) · Im[ a(i/τ₁) / b(i/τ₁) ] + O(k⁶).                                       (11)

*Proof.* Since D_P = b(1 + k²a/b)E − εk²b, near s₀ the equation D_P = 0 is equivalent to E(s, k) = εk²/(1 + k²a/b) = εk² − εk⁴ a(s)/b(s) + O(k⁶). At k = 0, E = −s²(1 + τ₁²s²) has a simple root at s₀, with ∂E/∂s(s₀) = 2s₀. By the implicit function theorem s = s₀ + σ₁k² + σ₂k⁴ + O(k⁶).

E is even in s with real coefficients, so E(iy, k) is real for real y. Hence every term generated by E alone is purely imaginary. This includes σ₁ = −iτ₁(1 + ε − ε₁²/τ₁²)/2 and the E-generated part of σ₂.

The only real contribution comes from εk⁴a/b. It gives Re σ₂ = −Re[ε(a/b)(s₀)/(2s₀)] = −(ετ₁/2) Im[(a/b)(s₀)]. ∎

Evaluating Im[a(i/τ₁)/b(i/τ₁)] with Ω = 1/τ₁ gives closed forms for each model:

- LS: −κ / [Ω(1 + τ_q²Ω²)]
- GN-II: 0
- GN-III: −κ/Ω
- MGT: −(κ − τ_qC_T²) / [Ω(1 + τ_q²Ω²)]
- DPL-1: −κ(1 + τ_Tτ_qΩ²) / [Ω(1 + τ_q²Ω²)]
- HDPL: −κ[1 + Ω²τ_q(τ_T − τ_q/2)] / [Ω|1 − τ_q²Ω²/2 + iτ_qΩ|²]

**Corollary B4.** For τ₁ > 0, KG thermoelasticity is unstable (sup over k of Re s > 0) under LS, GN-III (κ > 0) and DPL-1 for all admissible parameters. It is unstable under MGT whenever κ > τ_qC_T², and under HDPL whenever 2τ_T > τ_q. These are exactly the conditions under which those heat laws are themselves stable [14,15].

For GN-II, Eq. (11) gives zero. Numerically the GN-II system is neutrally stable for ε = 0.0168. For ε = 1.68 it is unstable near k ≈ 128, where the optical elastic branch collides with the thermal branch (a Krein collision).

The paradox stated in Corollary B4 is that the better-behaved the heat law, the more certainly the KG model grows.

Table 2. Small-k growth law, Eq. (11), against numerical roots of D_P (ε = 0.0168).

| Model | Im[a/b](i/τ₁) | Re s at k = 0.05: numeric / Eq. (11) | Re s at k = 0.2: numeric / Eq. (11) |
|---|---|---|---|
| LS | −1.588e−3 | 5.000e−13 / 5.003e−13 | 1.281e−10 / 1.281e−10 |
| GN-II | 0 | ≈ 0 / 0 | ≈ 0 / 0 |
| GN-III | −6.000e−3 | 1.890e−12 / 1.890e−12 | 4.839e−10 / 4.839e−10 |
| DPL-1 | −8.206e−3 | 2.583e−12 / 2.585e−12 | 6.617e−10 / 6.618e−10 |
| HDPL | −7.739e−3 | 2.438e−12 / 2.438e−12 | 6.244e−10 / 6.241e−10 |
| MGT | −1.572e−3 | 5.048e−13 / 4.953e−13 | 1.268e−10 / 1.268e−10 |

The relative difference for MGT at k = 0.05 (2%) is round-off: the growth rate there is 10⁻¹³ against frequencies of order 10².

### 4.3 Size of the growth rate

Table 3 and Fig. 2 give sup over k of Re s for the original coupling. The peak lies at k ≈ 14–35 (wavelengths 5–12 nm) and the rate decays like k⁻² for large k. In physical units the e-folding time is 0.20–1.18 ns, about 800–4800 periods of the optical oscillation (2π/(ω∗Ω) ≈ 0.25 ps). Nanosecond laser heating of nanostructures, the application targeted by several KG studies, therefore falls directly in the range where the spurious growth matters. With the source coupling ε = 1.68 the rates are about 100 times larger. For Eringen's model (τ₁ = 0) and for classical elasticity, sup over k of Re s ≤ 0 for all six heat laws.

Table 3. Peak growth rate of KG thermoelasticity, original coupling.

| Model | sup Re s (ε = 0.0168) | at k | rate (s⁻¹) | e-folding time | sup Re s (ε = 1.68) |
|---|---|---|---|---|---|
| LS | 3.19e−2 | 19.8 | 4.90e9 | 0.20 ns | 3.06 |
| GN-II | 0 (neutral) | – | – | – | 38.3 (k ≈ 128) |
| GN-III | 7.93e−3 | 34.7 | 1.22e9 | 0.82 ns | 0.79 |
| DPL-1 | 5.50e−3 | 34.7 | 8.44e8 | 1.18 ns | 0.55 |
| HDPL | 6.52e−3 | 13.7 | 1.00e9 | 1.00 ns | 0.65 |
| MGT | 3.22e−2 | 19.8 | 4.95e9 | 0.20 ns | 3.08 |

[Insert Figure 2 here]

Figure 2. Maximum growth rate Re s versus wavenumber for the original coupling: (a) ε = 0.0168, (b) ε = 1.68. The dotted grey line in (a) is the LS small-k law, Eq. (11), with slope k⁴. GN-II is neutral in (a) and unstable near k ≈ 128 in (b).

### 4.4 Damping does not cure the instability

Two natural regularizations make the instability worse:

- **Damping in the KG operator**, 1 − ε₁²∇² + τ_d∂ₜ + τ₁²∂ₜ². With τ_d = 10⁻⁵, sup Re s = 1.2–1.7 × 10⁻² for every heat law, including GN-II and γ = 0. The term acts as negative viscosity on the acoustic branch.
- **Kelvin–Voigt viscosity**, Lσ = (1 + η∂ₜ)C:e − γΘI. The optical branch then grows at the rate η/(2ε₁²) as k → ∞. For η = 10⁻⁵ the numerical value is 0.0500 for all models, equal to the formula.

Both results follow from the same mechanism: any dissipation acting on the physical energy E₀ feeds the negative-energy branch.

## 5. An energy-consistent coupling

Theorem B1 suggests replacing ∇·u̇ in Eq. (2) by ∇·(u̇ + b u⃛):

ρcΘ̇ + γT₀ ∇·(u̇ + b u⃛) + div q = 0.                                                            (12)

**Theorem B5.** For Eqs. (1) and (12) with heat law Fourier, LS, GN-II or GN-III,

d/dt [E_b + E_θ] = −𝒟 ≤ 0,                                                                        (13)

with E_θ and 𝒟 as in Theorem B3. If τ₁² < b < ε₁²/c_d², then E_b + E_θ is positive definite and the system is Lyapunov stable.

*Proof.* Multiply Eq. (1) by u̇ + b u⃛ and Eq. (12) by Θ/T₀. The coupling terms are γ∫Θ ∇·(u̇ + bu⃛) and −γ∫Θ ∇·(u̇ + bu⃛), and they cancel. The rest follows from Theorems B1 and B3. ∎

For MGT, DPL-1 and HDPL the energy argument requires additional multipliers, as in the local theory [12–14]. We have not carried it out; instead we computed sup over k of Re s numerically for 33 values of b (Fig. 3). For all five dissipative laws, sup Re s ≤ 10⁻¹⁵ (round-off) for 4.0 × 10⁻⁵ ≤ b ≤ 1.0 × 10⁻⁴. It is positive (2 × 10⁻⁴ to 3 × 10⁻²) for b ≤ 3.5 × 10⁻⁵ and for b ≥ 1.05 × 10⁻⁴. The numerical window therefore coincides with the theoretical window [τ₁², ε₁²] = [3.6 × 10⁻⁵, 10⁻⁴]. We conjecture that Theorem B5 extends to MGT under κ > τ_qC_T², and to HDPL under 2τ_T > τ_q.

[Insert Figure 3 here]

Figure 3. Energy-consistent coupling, Eq. (12): sup over k ∈ [0.1, 10⁴] of Re s versus b, for the five dissipative heat laws. The shaded window τ₁² ≤ b ≤ ε₁²/c_d² is stable; the system is unstable outside it.

*Interpretation.* Eq. (12) states that the heat balance sees the strain rate filtered by the same kind of temporal operator that appears in the KG stress law. It is the minimal change that makes the coupling consistent with a positive energy. Whether it can be derived from a nonlocal Clausius–Duhem inequality, for example in the framework of [1], is an open question. Until it is answered, we recommend treating KG thermoelasticity with the original coupling as an effective theory valid only well below 1/τ₁, the cut-on frequency of the optical branch.

## 6. Domain of influence

For constant-coefficient operators, Gårding's theorem [9,10] states two things. A forward fundamental solution supported in a proper closed cone exists if and only if the operator is hyperbolic with respect to t. When it exists, its support lies in the dual of the hyperbolicity cone of the principal part. For systems one applies the theorem to the determinant, here D_P·D_S.

Hyperbolicity requires two conditions:

(H1) the principal part p does not vanish at the time direction (s ≠ 0, k = 0), and its roots in s are purely imaginary for real k;

(H2) sup over real k of Re s < ∞ (Gårding's condition on lower-order terms).

Instability with a bounded growth rate does not violate (H2).

**Theorem B6.** Let τ₁ > 0.

(a) For LS, MGT, GN-II and HDPL, the principal part of D_P·D_S is, up to sign, s⁴(τ₁²s² + ε₁²k²)²·p_θ(s, k), where p_θ is τ_q s² + κk² (LS), s(τ_q s² + κk²) (MGT), s² + C_T²k² (GN-II) or s(τ_q²s²/2 + κτ_T k²) (HDPL). Condition (H1) holds. Condition (H2) holds because Re s is bounded and decays like k⁻² (Fig. 2). Hence solutions with compactly supported data in a ball of radius R vanish outside the ball of radius R + V∗t, where

V∗ = max(ε₁/τ₁, v_θ),   v_θ = 1/√τ_q (LS), √(κ/τ_q) (MGT), C_T (GN-II), √(2κτ_T)/τ_q (HDPL).          (14)

(b) For GN-III and DPL-1, the principal part of the heat factor is κk²s and κτ_T k²s respectively. These vanish at k = 0, so (H1) fails and the speed of propagation is infinite.

(c) For Eringen's model (τ₁ = 0, ε₁ > 0), the elastic factor of the principal part is ε₁²k²s². It vanishes at k = 0, so (H1) fails and the speed is infinite for every heat law. The same conclusion follows directly from ü = c²Δ(I − ε₁²Δ)⁻¹u, whose kernel e^(−|x|/ε₁)/(4πε₁²|x|) is positive everywhere.

*Proof.* Count degrees in Eq. (4). The coupling term εk²b has degree at least two less than (b + k²a)E for every model in Table 1, so it does not enter the principal part. Products of hyperbolic polynomials are hyperbolic, and their hyperbolicity cone is the intersection of the individual cones. A factor with characteristic speeds 0 and v has a cone whose dual is {|x| ≤ vt}; the intersection of the cones is dual to the ball of the largest speed, giving the maximum in Eq. (14). ∎

For the data used, V∗ = 10 (LS, MGT), 1.667 (GN-II, where ε₁/τ₁ > C_T = 1) and 17.32 (HDPL), all in units of c_d. Table 4 compares these bounds with max |Im s|/k at k = 10⁶. The two agree to four digits whenever the bound is finite. For GN-III and DPL-1 the numerical ratio is 1.667, because their phase speeds are finite. Their diffusive roots, however, have Re s ∝ −k², which is the source of the infinite speed. LS and MGT have the same principal part and so the same front speed. This is the structural reason why the two models give nearly identical wave results in [8].

Table 4. Wavefront speed: Gårding bound, Eq. (14), versus the numerical ratio max(abs Im s)/k at k = 10⁶.

| Model | KG bound | KG numeric | Eringen bound | Eringen numeric |
|---|---|---|---|---|
| LS | 10.000 | 10.000 | ∞ | 10.000 |
| GN-II | 1.6667 | 1.6667 | ∞ | 1.0000 |
| GN-III | ∞ | 1.6667 | ∞ | 0.0001 |
| DPL-1 | ∞ | 1.6667 | ∞ | 0.0001 |
| HDPL | 17.321 | 17.321 | ∞ | 17.321 |
| MGT | 10.000 | 10.000 | ∞ | 10.000 |

For the energy-consistent coupling, Eq. (12), the coupling term reaches the principal order in LS and MGT. The front speeds then shift slightly: for b = 6 × 10⁻⁵ the LS speeds solve τ_qτ₁²v⁴ − (τ_qε₁² + κτ₁² + εbτ_q)v² + κε₁² = 0, which gives v = 10.0014 and 1.6662, in agreement with the numerical value 10.0014. The domain of influence remains bounded.

## 7. Numerical method

The roots of D_P (degree 6–7 in s) and D_S (degree 4) were computed by Aberth–Ehrlich iteration on a rescaled polynomial, followed by Newton polishing. The method uses the Python standard library only. The maximum relative backward error over all models and wavenumbers was 3.8 × 10⁻¹⁶. Every analytical result was checked against these roots:

- the band edges, Eq. (9), to four digits;
- the small-k law, Eq. (11), to four digits (Table 2);
- the Kelvin–Voigt rate η/(2ε₁²) exactly;
- the front speeds, Eq. (14), to four digits (Table 4).

The scripts are listed in Appendix A.

## 8. Discussion and conclusions

1. **Elastic KG is well-posed and stable if and only if τ₁c_d < ε₁.** The "if" direction comes from the conserved energies E_b; the "only if" direction from the explicit growth band (9). For shear waves the condition τ₁c_s ≤ ε₁ is necessary for every thermoelastic variant. Parameter choices in the literature should be checked against this condition: for ε₁ = 0.01, any τ₁ > 0.01 (in units where c_d = 1) is unstable.

2. **Dissipation makes KG thermoelasticity unstable.** The optical branch carries negative physical energy, so every dissipative heat law (LS, GN-III, DPL-1, HDPL, MGT) makes it grow. The growth rate follows Eq. (11), and for copper the e-folding time is 0.2–1.2 ns. Only GN-II is neutral, and only for weak coupling. Viscous regularization makes things worse. This is the time-domain counterpart of the spatial amplification of the optical elastic wave found in Paper A.

3. **Implications for published work.** Laplace-domain transient solutions are correct only if the Bromwich contour lies to the right of all singularities. With poles in Re s > 0, a fixed inversion abscissa can hide the growth or give spurious results, and finite-time simulations can be contaminated by the growing mode. We have not re-examined specific published studies, but we recommend that KG transient results be checked for poles with Re s > 0.

4. **A stable alternative.** Coupling the heat equation to ∇·(u̇ + bu⃛) with τ₁² ≤ b ≤ ε₁²/c_d² gives a positive, non-increasing energy. Stability is proved for Fourier, LS, GN-II and GN-III and verified numerically for MGT, DPL-1 and HDPL. A thermodynamic derivation of this coupling is the main open problem raised here.

5. **Finite speed.** With τ₁ > 0 and an LS, MGT, GN-II or HDPL heat law, disturbances travel at most at V∗ = max(ε₁/τ₁, v_θ). GN-III, DPL-1 and Eringen's model (τ₁ = 0) have infinite speed. LS and MGT share their principal part and therefore their front speed.

Natural extensions are the energy proof of Theorem B5 for MGT and the dual-phase-lag laws, bounded domains with boundary conditions suited to differential nonlocal models, and calibration of (ε₁, τ₁) against phonon dispersion so that the window τ₁c_d < ε₁ can be checked for real materials.

## Appendix A. Reproducibility

The following scripts in this repository use the Python 3 standard library only:

- `kg_thermoelastic_core.py`: polynomials of Eqs. (4)–(5), root finder, growth bands, wavefront speeds;
- `kg_plot.py`: plotting helper;
- `generate_kg_stability_figures.py`: Figs. 1–3 and `kg_stability_figures/numerical_summary.txt`, from which Tables 2–4 are taken.

## References

[1] Lazar M, Agiasofitou E. Nonlocal elasticity of Klein–Gordon type: fundamentals and wave propagation. Wave Motion. 2022;114:103038.

[2] Lazar M, Agiasofitou E. Nonlocal elasticity of Klein–Gordon type with internal length and time scales: constitutive modelling and dispersion relations. KIT Open Repository, https://publikationen.bibliothek.kit.edu/1000165899 (verify journal version before submission).

[3] Eringen AC. On differential equations of nonlocal elasticity and solutions of screw dislocation and surface waves. J Appl Phys. 1983;54:4703–4710.

[4] Singh B. Wave propagation in context of Moore–Gibson–Thompson thermoelasticity with Klein–Gordon nonlocality. Vietnam J Mech. 2024;46(2):104–118.

[5] Memory-dependent wave dynamics in micropolar thermoelastic solid with Klein–Gordon nonlocal effect. Contin Mech Thermodyn. 2025. https://doi.org/10.1007/s00161-025-01447-z (complete author list before submission).

[6] Nonlocal thermoelastic analysis of axially moving nanobeams with external loading via modified Klein–Gordon elasticity. Contin Mech Thermodyn. 2025. https://doi.org/10.1007/s00161-025-01423-7 (complete author list before submission).

[7] Viscoelastic Pasternak foundation analysis of a thermoelastic microbeam using Moore–Gibson–Thompson heat conduction under Klein–Gordon nonlocality. AIMS Math. 2025. https://doi.org/10.3934/math.2025471 (complete author list before submission).

[8] Mondal S, Mukhopadhyay S. Modeling and analysis of wave propagation under generalized Klein–Gordon nonlocal thermoelasticity theories. Mech Mater. 2026;222:105834.

[9] Gårding L. Linear hyperbolic partial differential equations with constant coefficients. Acta Math. 1951;85:1–62.

[10] Hörmander L. The Analysis of Linear Partial Differential Operators II: Differential Operators with Constant Coefficients. Berlin: Springer; 1983. Chapter 12.

[11] Jangid K, Mukhopadhyay S. A domain of influence theorem under MGT thermoelasticity theory. Math Mech Solids. 2021;26:285–295.

[12] Quintanilla R. Moore–Gibson–Thompson thermoelasticity. Math Mech Solids. 2019;24(12):4020–4031.

[13] Quintanilla R, Racke R. Qualitative aspects in dual-phase-lag thermoelasticity. SIAM J Appl Math. 2006;66(3):977–1001.

[14] Quintanilla R, Racke R. A note on stability in dual-phase-lag heat conduction. Int J Heat Mass Transfer. 2006;49:1209–1213.

[15] Kaltenbacher B, Lasiecka I, Marchand R. Wellposedness and exponential decay rates for the Moore–Gibson–Thompson equation arising in high intensity ultrasound. Control Cybern. 2011;40(4):971–988.

[16] Cairns RA. The role of negative energy waves in some instabilities of parallel flows. J Fluid Mech. 1979;92:1–14.

[17] MacKay RS. Movement of eigenvalues of Hamiltonian equilibria under non-Hamiltonian perturbation. Phys Lett A. 1991;155:266–268.

[18] Krechetnikov R, Marsden JE. Dissipation-induced instabilities in finite dimensions. Rev Mod Phys. 2007;79:519–553.

[19] Lord HW, Shulman Y. A generalized dynamical theory of thermoelasticity. J Mech Phys Solids. 1967;15:299–309.

[20] Green AE, Naghdi PM. On undamped heat waves in an elastic solid. J Therm Stress. 1992;15(2):253–264.

[21] Green AE, Naghdi PM. Thermoelasticity without energy dissipation. J Elasticity. 1993;31(3):189–208.

[22] Tzou DY. A unified field approach for heat conduction from macro- to microscales. J Heat Transfer. 1995;117(1):8–16.

[23] Chandrasekharaiah DS. Hyperbolic thermoelasticity: a review of recent literature. Appl Mech Rev. 1998;51:705–729.
