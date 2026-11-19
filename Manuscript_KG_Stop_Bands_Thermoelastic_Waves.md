# Stop Bands, Evanescent Regimes and Amplifying Pass Bands of Thermoelastic Waves in Klein–Gordon Nonlocal Solids under Six Non-Fourier Heat Conduction Models

**Draft manuscript (Paper A)**, prepared as a follow-up to Mondal and Mukhopadhyay, *Mechanics of Materials* 222 (2026) 105834.

---

## Abstract

Klein–Gordon (KG) nonlocal elasticity adds an internal length ε₁ and an internal time τ₁ to the stress–strain relation. Recent plane-wave studies combining it with generalized heat conduction report phase velocity, attenuation and specific loss over a frequency window, but they do not treat the frequencies at which the KG dispersion relation becomes singular or changes sign. This paper maps those frequencies exactly. For a KG medium with wave speed c the purely elastic wavenumber is k² = β²(1 − τ₁²β²)/(c² − ε₁²β²), so every bulk wave has two critical frequencies, Ω_ε = c/ε₁ and Ω_τ = 1/τ₁. Between them the wave is evanescent (a stop band). Above both it propagates again on an "optical" branch whose phase and group velocities tend to ε₁/τ₁. When ε₁ = cτ₁ the stop band closes and the wave is exactly non-dispersive. Eringen's differential model (τ₁ = 0) has no second pass band. We then solve the coupled longitudinal problem for the Lord–Shulman (LS), Green–Naghdi II and III (GN-II, GN-III), dual-phase-lag (DPL-1), hyperbolic dual-phase-lag (HDPL) and Moore–Gibson–Thompson (MGT) models. We use one scaling that remains valid when k = 0 (GN-II), and a branch rule based on propagation direction rather than on the sign of Im W. Three results are new. (i) In the P stop band (2.4–4.1 THz for the copper data used) the elastic mode decays within about 0.2–0.8 nm (for 120 ≤ β ≤ 160) for all six heat models. (ii) Above 1/τ₁ the optical elastic branch has Im W < 0 for every dissipative heat model, so it is spatially amplified, while for GN-II it is neutral. (iii) Because KG and Eringen nonlocality drive the effective coupling ε/(1 − ε₁²β²) to zero, the thermal mode tends exactly to the uncoupled limits: speed 1/√τ_q and attenuation 1/(2√τ_q) for LS; attenuation (1 − τ_q C_T²/κ)/(2√(τ_q κ)) for MGT; speed √(2τ_T)/τ_q and attenuation (1 − τ_q/2τ_T)/√(2τ_T) for HDPL. The MGT and HDPL attenuation limits are positive exactly when the known stability conditions of those heat laws hold. We also note that the thermal expansion coefficient printed in the source study (1.78 × 10⁻⁴ K⁻¹) is ten times the copper value and raises the coupling constant from 0.0168 to 1.68.

**Keywords:** Klein–Gordon nonlocal elasticity; stop band; evanescent wave; group velocity; generalized thermoelasticity; Moore–Gibson–Thompson; dual-phase-lag; spatial amplification

---

## 1. Introduction

Nonlocal elasticity of Klein–Gordon type was introduced by Lazar and Agiasofitou [1,2] as an extension of Eringen's Helmholtz-type model [3]. It adds a characteristic time τ₁ to the characteristic length ε₁, so the constitutive operator becomes 1 − ε₁²∇² + τ₁²∂ₜ². Lazar and Agiasofitou showed that the resulting dispersion relation has acoustic- and optical-like branches separated by a frequency gap [1,2]. Since then the operator has been combined with many heat conduction laws, most often MGT [4] and its fractional or memory-dependent variants [5–7].

Mondal and Mukhopadhyay [8] recently gave a unified plane-wave analysis of KG nonlocal thermoelasticity under six heat conduction models (LS [9], GN-II [10], GN-III [11], DPL-1 [12], HDPL [13,14] and MGT [15]). They computed phase velocity, attenuation and specific loss for the thermal, elastic and shear modes. Three aspects of that analysis motivate the present work.

First, the denominators c_s² − ε₁²β² and c_d² − ε₁²β² of their Eqs. (42), (43), (47) and (48) are stated to be non-zero for all admissible parameters. With their data (ε₁ = 0.01, c_d = 1, c_s ≈ 0.4994) they vanish at β ≈ 49.9 and β = 100. The factor 1 − τ₁²β² vanishes at β ≈ 166.7. The shear-wave velocity reaching zero near β = 50 in their Fig. 7(a), and the abrupt drops in their Fig. 1(a), lie at these points, but the regimes on either side were not identified.

Second, all roots were selected by requiring Im W > 0. On a branch whose energy runs opposite to its natural damping direction, this rule picks the wave travelling the wrong way.

Third, their non-dimensional length l = k/(ρc_vV) is zero for GN-II (k = 0). The factor L/V in their Eq. (19) is not defined.

This paper addresses all three points. Section 2 restates the model with a scaling that is valid for all six heat laws. Section 3 classifies the purely elastic KG regimes exactly. Section 4 treats the coupled problem, defines a physical branch rule, and gives closed-form high-frequency limits. Section 5 presents numerical results for copper. Section 6 discusses physical scales, the coupling constant, and the link to the companion stability analysis (Paper B).

## 2. Governing equations and a uniform scaling

### 2.1 Field equations

We follow [8]. The KG constitutive law is

(1 − ε₁²∇² + τ₁²∂ₜ²) σ = 2μ e + λ tr(e) I − γ Θ I,                                  (1)

with γ = α_t(3λ + 2μ). Combined with div σ = ρü it gives

μ∇²u + (λ + μ)∇(∇·u) − γ∇Θ = ρ(1 − ε₁²∇² + τ₁²∂ₜ²) ü.                              (2)

The six heat models are written as one equation. We use polynomials a(s) and b(s) in the time-derivative operator s = ∂ₜ:

a(∂ₜ) ∇²Θ = b(∂ₜ) (Θ + ε ∇·u),                                                        (3)

with the entries of Table 1. Table 1 is Eq. (16) of [8] in operator form. For LS and DPL a common factor ∂ₜ has been cancelled, which assumes quiescent past states.

Table 1. Heat conduction polynomials a(s), b(s) in Eq. (3) (non-dimensional; κ = k/k_ref, C_T² = k∗/(ρcV²)).

| Model | a(s) | b(s) |
|---|---|---|
| LS | κ | s(1 + τ_q s) |
| GN-II | C_T² | s² |
| GN-III | C_T² + κ s | s² |
| MGT | C_T² + κ s | s²(1 + τ_q s) |
| DPL-1 | κ(1 + τ_T s) | s(1 + τ_q s) |
| HDPL | κ(1 + τ_T s) | s(1 + τ_q s + τ_q² s²/2) |

### 2.2 Scaling

Let V = √((λ+2μ)/ρ) and let ω∗ = ρcV²/k_ref be a reference frequency, where k_ref is the thermal conductivity of the material. We set x′ = ω∗x/V, t′ = ω∗t, u′ = ω∗u/V and Θ′ = γΘ/(λ+2μ), and we use the same k_ref for every model. GN-II is then obtained by setting κ = 0 rather than through a scaling that degenerates. Dropping primes, c_d = 1, c_s² = μ/(λ+2μ), and

ε = γ²T₀ / (ρc(λ+2μ)),   C_T² = k∗/(ρcV²),   κ = k/k_ref.                                 (4)

For the copper data of [8,16] (ρ = 8954 kg m⁻³, c = 383.1 J kg⁻¹ K⁻¹, k = 386 W m⁻¹ K⁻¹, k∗ = 5930.38 × 10¹⁰ W m⁻¹ K⁻¹ s⁻¹, λ = 7.76 × 10¹⁰ Pa, μ = 3.86 × 10¹⁰ Pa, T₀ = 293 K) we get V = 4158 m s⁻¹, ω∗ = 1.536 × 10¹¹ s⁻¹, l∗ = V/ω∗ = 27.1 nm, c_s = 0.4994 and C_T² = 1.000.

With the copper thermal expansion coefficient α_t = 1.78 × 10⁻⁵ K⁻¹, the coupling constant is ε = 0.0168. This is the standard value for copper in generalized thermoelasticity. The value α_t = 1.78 × 10⁻⁴ K⁻¹ printed in [8] gives ε = 1.68, which is 100 times larger. We use ε = 0.0168 throughout and report ε = 1.68 for comparison only. The parameters τ_q = 0.01, τ_T = 0.015, ε₁ = 0.01 and τ₁ = 0.006 are those of [8].

### 2.3 Potentials and plane waves

With u = ∇φ + ∇×Ψ and Ψ = (0, ψ, 0), Eqs. (2)–(3) give

∇²φ − (1 − ε₁²∇² + τ₁²∂ₜ²) φ̈ = Θ,     a(∂ₜ)∇²Θ = b(∂ₜ)(Θ + ε∇²φ),                         (5)

c_s²∇²ψ − (1 − ε₁²∇² + τ₁²∂ₜ²) ψ̈ = 0.                                                        (6)

For time-harmonic waves exp{i(Wx − βt)} with real β, define

S(β) = 1 − ε₁²β²,   R(β) = 1 − τ₁²β²,   q²(β) = −b(−iβ)/a(−iβ).                               (7)

Here q² is the squared wavenumber of the uncoupled thermal wave. Eliminating Θ gives the coupled longitudinal dispersion relation

S W⁴ − [β²R + q²(S + ε)] W² + q² β² R = 0,                                                   (8)

which is algebraically identical to Eq. (45) of [8]. The shear wave satisfies

W₃² = β² R / (c_s² − ε₁²β²).                                                                    (9)

## 3. Exact regimes of the purely elastic KG wave

For a KG wave of local speed c (c = c_d for P, c = c_s for S), Eqs. (5) with γ = 0 and (6) give

k²(β) = β²(1 − τ₁²β²) / (c² − ε₁²β²).                                                         (10)

**Proposition A1 (critical frequencies).** Let Ω_ε = c/ε₁ and Ω_τ = 1/τ₁, both assumed finite and positive. Then k² > 0 (propagation) for β < min(Ω_ε, Ω_τ) and for β > max(Ω_ε, Ω_τ). k² < 0 (evanescence) for β strictly between them. At β = Ω_ε the wavenumber diverges (zero phase and group velocity). At β = Ω_τ it vanishes (cut-on of the upper branch).

*Proof.* The sign of k² is the sign of the ratio (1 − β²/Ω_τ²)/(1 − β²/Ω_ε²). ∎

**Proposition A2 (matched case).** If ε₁ = cτ₁, then Ω_ε = Ω_τ, the stop band closes and k = β/c for all β ≠ Ω_τ. The KG wave is then exactly non-dispersive.

*Proof.* Substitute ε₁ = cτ₁ in Eq. (10). The factor 1 − τ₁²β² cancels. ∎

**Proposition A3 (group velocity and high-frequency limit).** On a propagating branch,

v_g = dβ/dk = k(c² − ε₁²β²) / [β(1 + ε₁²k² − 2τ₁²β²)].                                    (11)

On the upper branch, k → (τ₁/ε₁)β as β → ∞, so the phase and group velocities both tend to ε₁/τ₁, independently of c. On the lower branch, v_g → 0 as β → Ω_ε.

*Proof.* Differentiate F = k²(c² − ε₁²β²) − β²(1 − τ₁²β²) = 0 implicitly. The limits follow from Eq. (10). ∎

**Remark A1 (Eringen limit).** For τ₁ = 0, k² → −1/ε₁² as β → ∞. Eringen's model therefore has a single cut-off at c/ε₁ and no upper pass band. The decay rate tends to Im k = 1/ε₁ = 100.

For the source parameters, the P stop band is 100 < β < 166.7 and the S stop band is 49.9 < β < 166.7. In physical units these are 2.45–4.08 THz and 1.22–4.08 THz (f = βω∗/2π). Both bands lie inside the acoustic phonon range of copper, which matters when interpreting them (Section 6). Fig. 1 shows the regime map in the (τ₁, β) plane. The stop bands close at τ₁ = ε₁/c_d = 0.01 for P waves and at τ₁ = ε₁/c_s = 0.02 for S waves. For τ₁ larger than these values the order of the critical frequencies reverses. Paper B shows that the elastic KG model is then also temporally unstable.

[Insert Figure 1 here]

Figure 1. Regime map of KG nonlocal elasticity for ε₁ = 0.01. The black curve is β = 1/τ₁; dashed lines are the cut-offs c_d/ε₁ = 100 and c_s/ε₁ = 49.9. Pink regions are stop bands of both P and S waves; blue regions are S-only stop bands. The green line marks τ₁ = 0.006 used in [8]; dotted lines mark τ₁ = ε₁/c_d and τ₁ = ε₁/c_s, where the bands close.

[Insert Figure 2 here]

Figure 2. Purely elastic P wave (γ = 0): (a) Re W and (b) Im W versus β for KG (ε₁ = 0.01, τ₁ = 0.006), Eringen (τ₁ = 0) and classical elasticity. The shaded band 100 < β < 166.7 is the KG stop band. Above it KG propagates again, while Eringen remains evanescent with Im W → 100.

[Insert Figure 3 here]

Figure 3. Transverse shear wave: (a) Re W₃ and (b) Im W₃. The S stop band 49.9 < β < 166.7 explains the zero phase velocity near β = 50 reported in Fig. 7(a) of [8]. The attenuation there is evanescent decay, not thermal damping.

[Insert Figure 4 here]

Figure 4. Purely elastic P wave: (a) phase velocity and (b) group velocity. For the matched case τ₁ = ε₁/c_d = 0.01 the wave is non-dispersive (Proposition A2). On the upper KG branch both velocities approach ε₁/τ₁ = 1.667 (dotted line).

## 4. Coupled longitudinal waves

### 4.1 Root selection

Eq. (8) gives two values of W² at each β. Each value has two square roots ±W. Ref. [8] keeps the root with Im W > 0. That rule is correct when a wave loses energy as it travels, but it is not a law: what is required is that the wave carries energy away from the source. We use the following rule.

- **Pass band** (|Re W| ≥ |Im W|): choose Re W > 0. On every branch considered here the group velocity is positive (Eq. (11) and Fig. 4), so this wave carries energy towards +x. The sign of Im W is then a result, not an input. Im W < 0 means spatial amplification.
- **Stop band** (|Im W| > |Re W|): choose Im W > 0 (decay away from the source).

The two modes are labelled at the highest frequency computed (β = 3000). There, KG and Eringen nonlocality decouple the fields (Section 4.2), so the thermal mode is the root closest to q². The labels are then carried to lower frequencies by minimum-relative-distance continuation. In classical GN-II the uncoupled thermal and elastic speeds coincide (C_T = c_d = 1); we then call the faster root "thermal".

### 4.2 High-frequency decoupling and exact limits

Divide Eq. (8) by S. The coupling enters only through ε/S. Under KG or Eringen nonlocality S = 1 − ε₁²β² → −∞, so

ε_eff(β) = ε / (1 − ε₁²β²) → 0   (β → ∞).                                                  (12)

The thermal mode therefore tends to the uncoupled thermal wavenumber q(β), and the elastic mode to the KG elastic branch, Eq. (10). Expanding q(β) for large β gives the exact high-frequency limits.

**Proposition A4 (thermal-mode limits under KG/Eringen nonlocality).** As β → ∞, the thermal phase velocity V₁ and attenuation Q₁ satisfy:

- LS: V₁ → 1/√τ_q, Q₁ → 1/(2√(τ_q κ));
- MGT: V₁ → √(κ/τ_q), Q₁ → (1 − τ_q C_T²/κ)/(2√(τ_q κ));
- HDPL: V₁ → √(2κτ_T)/τ_q, Q₁ → (1 − τ_q/(2τ_T))/√(2κτ_T);
- GN-II: V₁ → C_T, Q₁ = 0;
- GN-III and DPL-1: V₁ and Q₁ grow like √β (diffusive, unbounded).

*Proof (MGT; the other cases are analogous).* q² = −b/a = β²(1 − iβτ_q)/(C_T² − iβκ) = (τ_q/κ)β²[1 + (i/β)(1/τ_q − C_T²/κ) + O(β⁻²)]. Hence q = β√(τ_q/κ) + (i/2)(1/τ_q − C_T²/κ)√(τ_q/κ) + O(β⁻¹). ∎

For the data used, these limits are V₁ → 10, Q₁ → 5 (LS); V₁ → 10, Q₁ → 4.95 (MGT); and V₁ → 17.32, Q₁ → 3.849 (HDPL). The MGT limit is positive if and only if κ > τ_q C_T², which is the known stability condition of MGT heat conduction [17]. The HDPL limit is positive if and only if 2τ_T > τ_q, which is the stability condition of the second-order dual-phase-lag law [18]. Proposition A4 thus links the high-frequency attenuation of the thermal front directly to the well-posedness of the heat law.

Proposition A4 also explains why LS and MGT give nearly identical results in [8]. Their leading terms are identical (both principal parts are τ_q∂ₜ² − κ∇² up to a factor ∂ₜ). They differ only through the lower-order term C_T², which enters the attenuation with weight τ_q C_T²/κ = 0.01.

In the classical case (S ≡ 1) the coupling never vanishes and the limits are shifted by O(ε). For LS, solving Eq. (8) asymptotically gives V₁ → 10.0008 at ε = 0.0168.

## 5. Numerical results for copper

Eq. (8) was solved in closed form (quadratic in W²) on 2500 logarithmically spaced frequencies in 0.05 ≤ β ≤ 3000, using the root selection of Section 4.1. All scripts use the Python standard library only and are listed in Appendix A.

### 5.1 Thermal mode

Fig. 5 and Table 2 show that the thermal-mode phase velocity and attenuation are almost independent of the elasticity framework. For the five dissipative models, KG and classical values differ by at most 0.8% in V₁ and 2.9% in Q₁ over 0.05 ≤ β ≤ 3000; the largest differences occur just above β = 1/τ₁, where the optical elastic branch is cut on. This agrees with the conclusion of [8] that the thermal mode is governed by the heat law. GN-II is the exception: its classical thermal speed stays at 1.067 at all frequencies, because the coupling never vanishes, whereas under KG it tends to C_T = 1 (a 6.7% difference at β = 3000). The limits of Proposition A4 are reached to four digits at β = 3000. The HDPL velocity peak (V₁ ≈ 18.3 near β ≈ 160) followed by relaxation to 17.32 is a property of the heat law itself; it also appears for classical elasticity.

Table 2. Thermal mode (V₁, Q₁) under KG nonlocality, physical coupling ε = 0.0168.

| Model | β = 10 | β = 50 | β = 200 | β = 3000 | Limit (Prop. A4) |
|---|---|---|---|---|---|
| LS | 4.247, 2.123 | 7.861, 3.929 | 9.716, 4.862 | 9.999, 4.999 | 10, 5 |
| GN-II | 1.065, 0 | 1.038, 0 | 1.003, 0 | 1.000, 0 | 1, 0 |
| GN-III | 4.268, 2.112 | 9.900, 4.948 | 19.96, 9.978 | 77.45, 38.72 | unbounded |
| DPL-1 | 4.591, 2.280 | 11.67, 5.134 | 25.68, 8.986 | 95.38, 31.80 | unbounded |
| HDPL | 4.601, 2.273 | 11.90, 4.759 | 18.20, 4.551 | 17.33, 3.853 | 17.32, 3.849 |
| MGT | 4.079, 1.998 | 7.814, 3.865 | 9.710, 4.811 | 9.999, 4.949 | 10, 4.95 |

[Insert Figure 5 here]

Figure 5. Thermal mode under the six heat models: (a) phase velocity V₁ and (b) attenuation Q₁ versus β (log scale). Solid or dashed lines are KG; dotted lines are classical elasticity, which nearly coincide with KG. Grey dotted lines mark the limits of Proposition A4.

### 5.2 Elastic mode: stop band and optical pass band

The elastic mode is where the elasticity framework matters (Table 3, Fig. 6).

- **Lower pass band (β < 100).** The elastic mode slows from V₂ ≈ 1 to V₂ ≈ 0.18 at β = 99, with a small attenuation of order 10⁻² for the five dissipative models. GN-II gives zero attenuation.
- **Stop band (100 < β < 166.7).** Re W₂ is nearly zero and Im W₂ is large: Im W₂ ≈ 125 at β = 120 and 36 at β = 160. The decay length 1/Im W₂ is 0.008–0.03 in units of l∗, which is 0.2–0.8 nm. It agrees within 1% across all six heat models (Table 3). Fig. 6(a) shows a sharp minimum at the pole β = c_d/ε₁, where W₂ diverges.
- **Optical pass band (β > 166.7).** The wave propagates again with V₂ → ε₁/τ₁ = 1.667. With the root choice of Section 4.1, **Im W₂ is negative for LS, GN-III, DPL-1, HDPL and MGT and zero for GN-II.** The optical elastic wave grows in its direction of travel, although by a small amount: the most negative Im W₂ is −0.15 (LS, MGT) just above β = 1/τ₁, and Im W₂ ≈ −0.008 at β = 200. Choosing Im W > 0 instead, as in [8], gives Re W₂ < 0, which is a wave travelling towards the source.
- **Eringen.** There is no optical band. Above β = 100, Im W₂ decreases monotonically to 1/ε₁ = 100.
- **Classical.** The elastic mode is non-dispersive with Q₂ ≈ 0.0084–0.0086 (LS, GN-III, MGT) or slowly decreasing Q₂ (DPL-1, HDPL).

Table 3. Elastic mode (V₂, Q₂), physical coupling ε = 0.0168. "–" means evanescent (Re W₂ ≈ 0).

| Model | KG β = 50 | KG β = 120 | KG β = 200 | KG β = 500 | Eringen β = 200 | Classical β = 200 |
|---|---|---|---|---|---|---|
| LS | 0.9078, 0.0103 | –, 125.3 | 2.609, −0.0084 | 1.732, −6.4e−4 | –, 115.5 | 0.9999, 0.0086 |
| GN-II | 0.8743, 0 | –, 126.4 | 2.600, 0 | 1.731, 0 | –, 115.7 | 0.9373, 0 |
| GN-III | 0.9079, 0.0102 | –, 125.3 | 2.609, −0.0073 | 1.732, −6.1e−4 | –, 115.5 | 1.000, 0.0084 |
| DPL-1 | 0.9079, 0.0089 | –, 125.3 | 2.609, −0.0051 | 1.732, −4.1e−4 | –, 115.5 | 1.000, 0.0059 |
| HDPL | 0.9079, 0.0081 | –, 125.3 | 2.609, −0.0038 | 1.732, −2.8e−4 | –, 115.5 | 1.000, 0.0042 |
| MGT | 0.9078, 0.0102 | –, 125.3 | 2.609, −0.0083 | 1.732, −6.4e−4 | –, 115.5 | 0.9999, 0.0085 |

[Insert Figure 6 here]

Figure 6. Elastic mode under KG nonlocality. (a) Decay length 1/|Im W₂| on a log scale; the shaded region is the P stop band. GN-II is absent outside the band because its attenuation is zero. (b) Signed specific loss SL₂ = 4π Im W₂/|Re W₂| (× 10³) in the optical pass band. Negative values are spatial gain; GN-II is neutral.

### 5.3 Effect of the coupling constant

With the source value ε = 1.68, the qualitative picture survives, but the magnitudes change by about two orders. At β = 1 the elastic attenuation is Q₂ ≈ 1.0 instead of 0.004. The optical-band gain at β = 200 is Im W₂ ≈ −0.86 for LS. GN-II develops a band of complex-conjugate wavenumbers near β = 200 (W ≈ 116 ± 42i in the two modes), the signature of a collision between the thermal branch and the optical elastic branch. Results that depend on coupling strength should therefore be recomputed with the physical α_t before they are compared with experiment.

## 6. Discussion

**Physical scales.** With ε₁ = 0.01 the internal length is ε₁l∗ = 0.27 nm, about the interatomic spacing of copper (0.256 nm). The P stop band (2.4–4.1 THz) and the optical band above it lie within the phonon spectrum of copper, whose maximum frequency is about 7 THz. The KG continuum is therefore being used at wavelengths of a few lattice spacings, where it is at best a fitted model. A useful next step is to calibrate ε₁ and τ₁ against measured phonon dispersion and to check whether a physical gap exists at all. Copper, a monatomic fcc metal, has no optical phonons.

**Why the optical branch is amplified.** On the optical branch, the mechanical energy defined by the multiplier u̇ (the energy that thermodynamics requires to decrease) is negative (Paper B). Thermal dissipation removes energy from that budget and so increases the wave's amplitude. In the time domain this is the dissipation-induced instability analysed in Paper B. In the frequency domain it appears as Im W₂ < 0 for a wave whose energy travels away from the source. The absence of gain under GN-II, which has no dissipation, supports this interpretation. This mechanism is well known for negative-energy waves in fluids and plasmas [19,20].

**Consequences for reported specific loss.** Specific losses computed with the Im W > 0 rule in the optical band (the region β > 166.7 in Figs. 1, 5 and 6 of [8]) correspond to waves travelling towards the source. In the stop bands, "attenuation" describes evanescent decay and is not dissipation. Neither quantity should be read as thermoelastic damping.

**Limitations.** The analysis is linear and assumes an isotropic, unbounded medium. The branch rule assumes the positive group velocities verified for the purely elastic branches. Near points where branches nearly coincide (classical GN-II, and ε = 1.68 near β = 200), the labels "thermal" and "elastic" are conventions. A full Briggs–Bers analysis [21] of the signaling problem would settle the branch choice rigorously and is left for future work.

## 7. Conclusions

1. Every KG bulk wave has two exact critical frequencies, c/ε₁ and 1/τ₁. The wave is evanescent between them and propagates on an optical branch above both, with phase and group velocities tending to ε₁/τ₁. The stop band closes, and the wave becomes non-dispersive, when ε₁ = cτ₁.
2. Eringen's model has only the lower cut-off and no upper pass band. Its high-frequency decay rate is 1/ε₁.
3. In the P stop band the elastic mode decays within 0.2–0.8 nm for all six heat models. The heat model affects this decay by less than 1%.
4. Above 1/τ₁, the elastic mode is spatially amplified for every dissipative heat model (LS, GN-III, DPL-1, HDPL, MGT) and neutral for GN-II. The usual Im W > 0 rule hides this by selecting a wave travelling towards the source.
5. Nonlocality decouples the thermal mode at high frequency. Its speed and attenuation then tend to closed-form limits, and the MGT and HDPL attenuation limits are positive exactly when the known stability conditions of those heat laws hold. LS and MGT coincide to leading order, which explains their similarity in [8].
6. The thermal expansion coefficient printed in [8] is ten times the copper value and inflates the coupling constant 100-fold.

## Appendix A. Reproducibility

All results come from the following scripts in this repository (Python 3 standard library only):

- `kg_thermoelastic_core.py`: model, dispersion relations, root selection and continuation, closed-form limits.
- `kg_plot.py`: plotting helper built on the repository's PNG canvas.
- `generate_kg_stopband_figures.py`: Figs. 1–6 and `kg_stopband_figures/numerical_summary.txt`, from which Tables 2–3 are taken.

## References

[1] Lazar M, Agiasofitou E. Nonlocal elasticity of Klein–Gordon type: fundamentals and wave propagation. Wave Motion. 2022;114:103038.

[2] Lazar M, Agiasofitou E. Nonlocal elasticity of Klein–Gordon type with internal length and time scales: constitutive modelling and dispersion relations. KIT Open Repository, https://publikationen.bibliothek.kit.edu/1000165899 (verify journal version before submission).

[3] Eringen AC. On differential equations of nonlocal elasticity and solutions of screw dislocation and surface waves. J Appl Phys. 1983;54:4703–4710.

[4] Singh B. Wave propagation in context of Moore–Gibson–Thompson thermoelasticity with Klein–Gordon nonlocality. Vietnam J Mech. 2024;46(2):104–118.

[5] Memory-dependent wave dynamics in micropolar thermoelastic solid with Klein–Gordon nonlocal effect. Contin Mech Thermodyn. 2025. https://doi.org/10.1007/s00161-025-01447-z (complete author list before submission).

[6] Viscoelastic Pasternak foundation analysis of a thermoelastic microbeam using Moore–Gibson–Thompson heat conduction under Klein–Gordon nonlocality. AIMS Math. 2025. https://doi.org/10.3934/math.2025471 (complete author list before submission).

[7] Unified modeling of harmonic waves in rotating piezoelectric semiconductor. Arch Appl Mech. 2026. https://doi.org/10.1007/s00419-026-03121-5 (complete author list before submission).

[8] Mondal S, Mukhopadhyay S. Modeling and analysis of wave propagation under generalized Klein–Gordon nonlocal thermoelasticity theories. Mech Mater. 2026;222:105834.

[9] Lord HW, Shulman Y. A generalized dynamical theory of thermoelasticity. J Mech Phys Solids. 1967;15:299–309.

[10] Green AE, Naghdi PM. On undamped heat waves in an elastic solid. J Therm Stress. 1992;15(2):253–264.

[11] Green AE, Naghdi PM. Thermoelasticity without energy dissipation. J Elasticity. 1993;31(3):189–208.

[12] Tzou DY. A unified field approach for heat conduction from macro- to microscales. J Heat Transfer. 1995;117(1):8–16.

[13] Chandrasekharaiah DS. Hyperbolic thermoelasticity: a review of recent literature. Appl Mech Rev. 1998;51:705–729.

[14] Prasad R, Kumar R, Mukhopadhyay S. Propagation of harmonic plane waves under thermoelasticity with dual-phase-lags. Int J Eng Sci. 2010;48(12):2028–2043.

[15] Quintanilla R. Moore–Gibson–Thompson thermoelasticity. Math Mech Solids. 2019;24(12):4020–4031.

[16] Jangid K, Gupta M, Mukhopadhyay S. On propagation of harmonic plane waves under the Moore–Gibson–Thompson thermoelasticity theory. Waves Random Complex Media. 2024;34(3):1976–1999.

[17] Kaltenbacher B, Lasiecka I, Marchand R. Wellposedness and exponential decay rates for the Moore–Gibson–Thompson equation arising in high intensity ultrasound. Control Cybern. 2011;40(4):971–988.

[18] Quintanilla R, Racke R. A note on stability in dual-phase-lag heat conduction. Int J Heat Mass Transfer. 2006;49:1209–1213.

[19] Cairns RA. The role of negative energy waves in some instabilities of parallel flows. J Fluid Mech. 1979;92:1–14.

[20] Krechetnikov R, Marsden JE. Dissipation-induced instabilities in finite dimensions. Rev Mod Phys. 2007;79:519–553.

[21] Briggs RJ. Electron-Stream Interaction with Plasmas. Cambridge, MA: MIT Press; 1964.

[22] Brillouin L. Wave Propagation and Group Velocity. New York: Academic Press; 1960.

[23] Achenbach JD. Wave Propagation in Elastic Solids. Amsterdam: North-Holland; 1973.
