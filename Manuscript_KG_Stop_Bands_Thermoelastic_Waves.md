# Stop Bands, Evanescent Regimes and Amplifying Pass Bands of Thermoelastic Waves in Klein–Gordon Nonlocal Solids under Six Non-Fourier Heat Conduction Models

---

## Abstract

Klein–Gordon (KG) nonlocal elasticity adds a characteristic length ε₁ and a characteristic time τ₁ to the stress–strain relation of a solid. Plane-wave studies that combine it with generalized heat conduction report phase velocity, attenuation and specific loss over a chosen frequency window. They do not, however, analyse the frequencies at which the KG dispersion relation becomes singular or changes sign. This paper gives an exact account of those frequencies and of the wave regimes they separate.

For a KG medium with local wave speed c, the purely elastic wavenumber satisfies k² = β²(1 − τ₁²β²)/(c² − ε₁²β²). Every bulk wave therefore has two critical frequencies, Ω_ε = c/ε₁ and Ω_τ = 1/τ₁. Between them the wave is evanescent (a stop band). Above both it propagates again on an optical branch whose phase and group velocities tend to ε₁/τ₁. When ε₁ = cτ₁ the stop band closes and the wave is exactly non-dispersive. Eringen's differential model (τ₁ = 0) has a cut-off but no second pass band.

We then solve the coupled longitudinal problem for six heat conduction laws: Lord–Shulman (LS), Green–Naghdi types II and III (GN-II, GN-III), dual-phase-lag (DPL-1), hyperbolic dual-phase-lag (HDPL) and Moore–Gibson–Thompson (MGT). We use a scaling that remains valid when the Fourier conductivity is zero (GN-II), and a root-selection rule based on the direction of energy flow rather than on the sign of the imaginary part of the wavenumber. The coupled dispersion relation factorizes as S(W² − k_e²)(W² − q²) = εq²W², where S = 1 − ε₁²β², k_e is the KG elastic wavenumber and q the thermal wavenumber.

A first-order expansion in the coupling ε gives the elastic-mode attenuation in closed form, Im W₂ ≈ εk_e³ Im q²/(2S|k_e² − q²|²). Away from the cut-off and from frequencies where the two uncoupled modes nearly coincide, it agrees with the exact roots to four or five digits. We show that Im q² > 0 at all frequencies exactly when the heat law is dissipative and stable. Consequently, the elastic wave is damped below c/ε₁ and amplified on the optical branch for LS, GN-III, DPL-1, HDPL and MGT, and it is neutral for GN-II. The usual rule Im W > 0 hides this amplification by selecting a wave that travels towards its source.

KG and Eringen nonlocality drive the effective coupling ε/S to zero at high frequency. The thermal mode therefore tends exactly to closed-form limits, and the MGT and HDPL attenuation limits are positive exactly when the stability conditions κ > τ_qC_T² and 2τ_T > τ_q hold. LS and MGT share their leading high-frequency terms, which explains why they give nearly identical results in earlier studies.

For copper, the P-wave stop band lies between 2.45 and 4.08 THz and the S-wave stop band between 1.22 and 4.08 THz. In the P stop band the elastic wave decays within 0.2–0.8 nm. The thermal expansion coefficient used in a recent study (1.78 × 10⁻⁴ K⁻¹) is ten times the copper value and raises the coupling constant from 0.0168 to 1.68. We give results for both values.

**Keywords:** Klein–Gordon nonlocal elasticity; stop band; evanescent wave; group velocity; generalized thermoelasticity; Moore–Gibson–Thompson heat conduction; dual-phase-lag; spatial amplification; negative-energy wave

---

## 1. Introduction

Thermoelasticity couples the deformation of a solid to its temperature. Duhamel first wrote down the coupling by adding a thermal stress to Navier's equations [1]. Biot later placed the coupled theory on a thermodynamic basis [2]. Both theories use Fourier's law, under which a thermal disturbance is felt instantly at every point. That prediction is acceptable for slow processes but not for short-pulse heating or for phenomena at the nanoscale. Cattaneo [3] and Vernotte [4] removed the paradox by adding a relaxation time to the heat-flux law. Lord and Shulman (LS) built a thermoelastic theory on that law [5], and Green and Lindsay proposed an alternative with two relaxation times [6].

Green and Naghdi took a different route. They introduced a thermal displacement ν with ν̇ = T and derived three theories [7–9]. Type II (GN-II) has no dissipation and supports undamped thermal waves; type III (GN-III) contains both a conductive and a wave-like flux. Tzou's dual-phase-lag (DPL) model introduced separate lags for the heat flux and the temperature gradient [10,11]. Its first-order and hyperbolic (second-order in τ_q) Taylor expansions became known as DPL-1 and HDPL. Chandrasekharaiah reviewed these hyperbolic theories [12]. More recently, Quintanilla added a flux relaxation to GN-III, obtaining Moore–Gibson–Thompson (MGT) thermoelasticity [13]. Its well-posedness, history-dependent extensions and numerical analysis have been studied since [14,15].

These heat laws are not all stable for every parameter choice. The MGT equation is exponentially stable only if the diffusive coefficient dominates the relaxed wave term [16]. The second-order DPL law requires 2τ_T > τ_q [17,18]. Thermodynamic restrictions on delayed heat-conduction models were discussed by Fabrizio and Franchi [19]. These conditions will reappear below in the attenuation of thermoelastic waves.

Plane harmonic waves are the standard test bed for any thermoelastic theory. Deresiewicz [20] and Chadwick and Sneddon [21] analysed them in the classical theory. Puri studied them under generalized theories [22]. Chandrasekharaiah computed wave speeds under GN-II [23], and Puri and Jordan treated type-III media [24]. Prasad, Kumar and Mukhopadhyay analysed plane waves under DPL [25], and Jangid, Gupta and Mukhopadhyay did the same under MGT [26]. A domain-of-influence theorem for MGT thermoelasticity was proved by Jangid and Mukhopadhyay [27]. In each case the wave picture consists of a predominantly thermal and a predominantly elastic longitudinal mode, plus an uncoupled shear wave. The theory is characterized by their dispersion and attenuation.

Nonlocal elasticity adds a material length scale. In Eringen's integral theory the stress at a point depends on the strain in a neighbourhood [28]. The thermoelastic extension came soon after [29]. For a particular kernel the integral law reduces to the differential form (1 − ε₁²∇²)σ = C:e [30,31], which has become the workhorse of size-dependent mechanics. Challamel and co-workers showed that this differential law yields a dispersive wave equation with a cut-off frequency [32]. Askes and Aifantis reviewed the wider family of gradient and nonlocal models and their dispersion [33]. Plane waves and their reflection in Eringen-type nonlocal thermoelastic solids were studied by Sarkar and Tomar [34] and by Das, Sarkar and Lahiri [35], among many others. Dispersion-engineered media such as phononic crystals and metamaterials, where band gaps are designed rather than incidental, are reviewed by Hussein, Leamy and Ruzzene [36].

Lazar and Agiasofitou added a characteristic time to Eringen's length, arriving at a nonlocal elasticity of Klein–Gordon type [37,38]. The constitutive operator becomes 1 − ε₁²∇² + τ₁²∂ₜ², and the dispersion relation acquires an optical-like branch and a frequency gap. Singh combined the KG operator with MGT heat conduction [39]. Mondal and Mukhopadhyay recently analysed plane waves in a unified framework of KG nonlocality and six heat laws [40]. They computed phase velocity, attenuation and specific loss for the thermal, elastic and shear modes, and compared them with Eringen and classical elasticity.

Three features of that analysis leave room for further work.

- **Singular frequencies are not analysed.** The denominators c_s² − ε₁²β² and c_d² − ε₁²β² of the dispersion relations are stated to be non-zero for all admissible parameters [40]. For ε₁ = 0.01 they vanish at β ≈ 49.9 (shear) and β = 100 (longitudinal), and the factor 1 − τ₁²β² vanishes at β ≈ 166.7. The shear velocity falling to zero near β = 50, and the abrupt drops in the thermal-mode velocity, occur at these points. The regimes between them were not identified.
- **Root selection.** All roots were chosen by requiring Im W > 0. This is the correct choice for a wave that loses energy as it travels [41,42]. It is not correct in general. The physical requirement is that energy flows away from the source, which in unstable or active media must be settled by a causality analysis of the Briggs–Bers type [43]. Media supporting negative-energy waves are the standard counter-example [44,45].
- **Scaling and data.** The characteristic length l = k/(ρcV) is zero for GN-II (k = 0), and the factor L/V in the unified heat equation is not defined. In addition, the thermal expansion coefficient listed for copper, 1.78 × 10⁻⁴ K⁻¹, is ten times the usual value.

This paper addresses these points and provides closed-form results that the purely numerical treatment of [40] does not. The contributions are:

1. an exact classification of the propagating, evanescent and optical regimes of KG waves, including the matched case ε₁ = cτ₁ and the high-frequency limit ε₁/τ₁;
2. a factorized form of the coupled dispersion relation and a first-order formula for the elastic-mode attenuation, valid for all six heat laws;
3. a lemma linking the sign of Im q² to the stability of each heat law, and a theorem showing that the optical elastic wave is spatially amplified for every dissipative law;
4. low- and high-frequency limits of both longitudinal modes in closed form;
5. numerical results for copper with the physical coupling constant, a parametric study in τ₁, and a direct validation of the asymptotic formulas;
6. an interpretation of the stop bands in physical units, compared with the measured phonon spectrum of copper [46].

Section 2 states the model and the scaling. Section 3 derives the dispersion relations. Section 4 classifies the elastic KG regimes. Section 5 contains the asymptotic analysis of the coupled problem. Section 6 presents numerical results, Section 7 discusses them, and Section 8 summarizes the conclusions.

## 2. Mathematical model

### 2.1 Constitutive law and equation of motion

Consider a homogeneous, isotropic, unbounded thermoelastic solid at reference temperature T₀. Let u be the displacement, e = ½(∇u + ∇uᵀ) the strain, Θ = T − T₀ the temperature increment and σ the stress. Following [37,40], the KG nonlocal constitutive law is

(1 − ε₁²∇² + τ₁²∂ₜ²) σ = 2μ e + λ (tr e) I − γ Θ I,                                                       (1)

where λ and μ are the Lamé constants, γ = α_t(3λ + 2μ) is the thermoelastic modulus and α_t the linear thermal expansion coefficient. Setting τ₁ = 0 recovers Eringen's differential model [30]; setting ε₁ = τ₁ = 0 recovers classical thermoelasticity. In the absence of body forces the equation of motion is

div σ = ρ ü,                                                                                                (2)

with ρ the mass density. Applying the operator of Eq. (1) to Eq. (2) and using the constitutive law gives the displacement equation

μ ∇²u + (λ + μ) ∇(∇·u) − γ ∇Θ = ρ (1 − ε₁²∇² + τ₁²∂ₜ²) ü.                                             (3)

The thermal stress is not multiplied by the nonlocal operator, because it enters the right-hand side of Eq. (1).

### 2.2 Heat conduction laws

The heat flux q obeys one of the following laws. Fourier's law is

q = −k ∇Θ.                                                                                                  (4)

The Cattaneo–Vernotte law underlying LS theory [3–5] is

(1 + τ_q ∂ₜ) q = −k ∇Θ.                                                                                    (5)

The GN-II law [8] uses the thermal displacement ν, with ν̇ = Θ:

q = −k∗ ∇ν,                                                                                                 (6)

where k∗ is the rate of thermal conductivity. The GN-III law [9] combines both mechanisms:

q = −k ∇Θ − k∗ ∇ν.                                                                                          (7)

The MGT law [13] adds a flux relaxation to GN-III:

(1 + τ_q ∂ₜ) q = −k ∇Θ − k∗ ∇ν.                                                                             (8)

The dual-phase-lag law q(t + τ_q) = −k∇Θ(t + τ_T) [10], expanded to first order in τ_T and to first or second order in τ_q [12,25], gives

(1 + τ_q ∂ₜ + n₁ τ_q² ∂ₜ²/2) q = −k (1 + τ_T ∂ₜ) ∇Θ,                                                       (9)

with n₁ = 0 for DPL-1 and n₁ = 1 for HDPL. The linearized energy balance is

ρ c Θ̇ + γ T₀ ∇·u̇ = −div q,                                                                                 (10)

where c is the specific heat. (Ref. [40] writes ∇·q on the left of its Eq. (12). The sign used here is the standard one; the unified equations below agree with those of [40].)

Eliminating q between Eq. (10) and Eqs. (5)–(9) gives the temperature equations. For LS,

k ∇²Θ = (1 + τ_q∂ₜ)(ρcΘ̇ + γT₀ ∇·u̇).                                                                        (11)

For GN-II, GN-III and MGT,

(k∗ + k∂ₜ) ∇²Θ = (1 + τ_q∂ₜ) ∂ₜ (ρcΘ̇ + γT₀ ∇·u̇),                                                          (12)

with k = τ_q = 0 for GN-II and τ_q = 0 for GN-III. For DPL-1 and HDPL,

k (1 + τ_T∂ₜ) ∇²Θ = (1 + τ_q∂ₜ + n₁τ_q²∂ₜ²/2)(ρcΘ̇ + γT₀ ∇·u̇).                                            (13)

### 2.3 Unified operator form

All six laws can be written as

a(∂ₜ) ∇²Θ = b(∂ₜ) (Θ + ε ∇·u),                                                                              (14)

in the non-dimensional variables of Section 2.4, where a and b are the polynomials in s = ∂ₜ listed in Table 2. For LS and DPL a common factor ∂ₜ has been removed, which assumes a quiescent past. The two polynomials are related to the uncoupled thermal wavenumber by

q² = −b(−iβ) / a(−iβ),                                                                                       (15)

which will be used throughout Sections 3–5.

Table 2. Heat-conduction polynomials of Eq. (14) (non-dimensional; κ = k/k_ref and C_T² = k∗/(ρcV²)).

| Model | a(s) | b(s) | Source |
|---|---|---|---|
| LS | κ | s(1 + τ_q s) | [5] |
| GN-II | C_T² | s² | [8] |
| GN-III | C_T² + κs | s² | [9] |
| MGT | C_T² + κs | s²(1 + τ_q s) | [13] |
| DPL-1 | κ(1 + τ_T s) | s(1 + τ_q s) | [10,25] |
| HDPL | κ(1 + τ_T s) | s(1 + τ_q s + τ_q²s²/2) | [11,12] |

### 2.4 Non-dimensional variables

Let k_ref be a reference conductivity, taken as the Fourier conductivity of the material for every model, including GN-II. Define

V = √((λ + 2μ)/ρ),   ω∗ = ρ c V² / k_ref,   l∗ = V/ω∗,                                                       (16)

and the scaled variables

x′ = x/l∗,  t′ = ω∗t,  u′ = u/l∗,  Θ′ = γΘ/(λ + 2μ),  σ′ = σ/(λ + 2μ),  ε₁′ = ε₁/l∗,  τ₁′ = ω∗τ₁,  τ_q′ = ω∗τ_q,  τ_T′ = ω∗τ_T.      (17)

For k > 0 this is the scaling of [26,40]. Using the same k_ref for every model makes GN-II a parameter choice (κ = 0) rather than a degenerate scaling. Dropping primes, the dimensionless groups are

c_d² = 1,   c_s² = μ/(λ + 2μ),   ε = γ²T₀ / (ρc(λ + 2μ)),   C_T² = k∗/(ρcV²),   κ = k/k_ref.                    (18)

The non-dimensional constitutive law is

(1 − ε₁²∇² + τ₁²∂ₜ²) σ = (1 − 2c_s²)(∇·u) I + c_s²(∇u + ∇uᵀ) − Θ I,                                       (19)

and the equation of motion becomes

(1 − c_s²) ∇(∇·u) + c_s² ∇²u − ∇Θ = (1 − ε₁²∇² + τ₁²∂ₜ²) ü.                                                (20)

The non-dimensional temperature equation is Eq. (14).

Table 1. Material data (copper [26,40]) and model parameters.

| Quantity | Value | Quantity | Value |
|---|---|---|---|
| ρ | 8954 kg m⁻³ | λ | 7.76 × 10¹⁰ Pa |
| c | 383.1 J kg⁻¹ K⁻¹ | μ | 3.86 × 10¹⁰ Pa |
| k | 386 W m⁻¹ K⁻¹ | k∗ | 5930.38 × 10¹⁰ W m⁻¹ K⁻¹ s⁻¹ |
| T₀ | 293 K | α_t (physical) | 1.78 × 10⁻⁵ K⁻¹ |
| V | 4158 m s⁻¹ | α_t (as printed in [40]) | 1.78 × 10⁻⁴ K⁻¹ |
| ω∗ | 1.536 × 10¹¹ s⁻¹ | l∗ | 27.06 nm |
| c_s | 0.4994 | C_T² | 1.000 |
| ε (physical α_t) | 0.0168 | ε (α_t of [40]) | 1.680 |
| ε₁ | 0.01 | τ₁ | 0.006 |
| τ_q | 0.01 | τ_T | 0.015 |

Two facts in Table 1 matter below. First, C_T² = 1.000, so the GN-type thermal wave speed equals c_d. The thermal and elastic modes of GN-II, GN-III and MGT are therefore nearly degenerate at low frequency. Second, the coupling constant for copper is ε = 0.0168 when the physical α_t is used. We use this value throughout and report ε = 1.68 for comparison only.

### 2.5 Potentials

The Helmholtz decomposition

u = ∇φ + ∇ × Ψ,   ∇·Ψ = 0,                                                                                  (21)

splits Eqs. (14) and (20) into a longitudinal and a transverse part. For plane strain in the xz-plane, Ψ = (0, ψ, 0) and

u₁ = ∂φ/∂x − ∂ψ/∂z,   u₃ = ∂φ/∂z + ∂ψ/∂x.                                                                   (22)

The scalar potential and the temperature satisfy

∇²φ − (1 − ε₁²∇² + τ₁²∂ₜ²) φ̈ = Θ,                                                                          (23)

a(∂ₜ) ∇²Θ = b(∂ₜ)(Θ + ε ∇²φ),                                                                              (24)

and the vector potential satisfies the uncoupled KG wave equation

c_s² ∇²ψ − (1 − ε₁²∇² + τ₁²∂ₜ²) ψ̈ = 0.                                                                    (25)

Substituting Θ from Eq. (23) into Eq. (24) gives a single equation for φ:

[a(∂ₜ)∇² − b(∂ₜ)] [∇²φ − (1 − ε₁²∇² + τ₁²∂ₜ²) φ̈] = ε b(∂ₜ) ∇²φ.                                             (26)

This is the operator form of Eq. (31) of [40]. Setting ε = 0 in Eq. (26), or γ = 0 in Eq. (3), decouples the fields and gives the purely elastic KG equation

∇²φ − (1 − ε₁²∇² + τ₁²∂ₜ²) φ̈ = 0,                                                                          (27)

which is the model of Lazar and Agiasofitou [37].

## 3. Plane waves and dispersion relations

### 3.1 Harmonic solutions

We seek solutions proportional to exp{i(W n·x − βt)}, with real angular frequency β, complex wavenumber W and unit propagation vector n:

(φ, Θ, ψ) = (A_φ, A_Θ, A_ψ) exp{i(W n·x − βt)}.                                                           (28)

On such fields the differential operators reduce to

∇² → −W²,   ∂ₜ → −iβ,   1 − ε₁²∇² + τ₁²∂ₜ² → 1 + ε₁²W² − τ₁²β².                                       (29)

It is convenient to introduce the spatial and temporal nonlocal factors

S(β) = 1 − ε₁²β²,   R(β) = 1 − τ₁²β².                                                                       (30)

S changes sign at β = 1/ε₁, and R at β = 1/τ₁. With c_d = 1, the first is the longitudinal cut-off frequency.

### 3.2 Transverse wave

Substituting Eq. (28) into Eq. (25) gives

W₃² = β² R(β) / (c_s² − ε₁²β²).                                                                              (31)

Eq. (31) is independent of the heat law, as found in [39,40]. With classical elasticity it reduces to W₃ = β/c_s.

### 3.3 Coupled longitudinal waves

Eq. (23) gives the temperature amplitude in terms of the potential amplitude:

A_Θ = (β²R − W²S) A_φ.                                                                                      (32)

Eq. (24), together with the definition (15), gives

(W² − q²) A_Θ = −ε q² W² A_φ.                                                                               (33)

Eliminating A_Θ and introducing the KG elastic wavenumber

k_e² = β² R / S                                                                                             (34)

leads to the coupled dispersion relation in factorized form:

S (W² − k_e²)(W² − q²) = ε q² W².                                                                           (35)

Expanding Eq. (35) gives the biquadratic

S W⁴ − [β²R + q²(S + ε)] W² + q² β² R = 0,                                                                (36)

which coincides with Eq. (45) of [40]. Its roots are

W²₁,₂ = { β²R + q²(S + ε) ± √([β²R + q²(S + ε)]² − 4S q²β²R) } / (2S),                                     (37)

and they satisfy Vieta's relations

W₁² W₂² = q² k_e²,   W₁² + W₂² = k_e² + q² (1 + ε/S).                                                       (38)

The form (35) shows that the coupling acts only through the effective coupling

ε_eff(β) = ε / S(β) = ε / (1 − ε₁²β²).                                                                      (39)

It equals ε in classical elasticity, diverges at β = 1/ε₁, changes sign above it, and tends to zero as β → ∞ when ε₁ > 0.

### 3.4 Wave characteristics

For each root W the phase velocity, attenuation coefficient and specific loss are [40,41]

V = β / Re W,                                                                                               (40)

Q = Im W,                                                                                                   (41)

SL = 4π Im W / |Re W|.                                                                                      (42)

We keep the sign of Im W in Eqs. (41) and (42), so a negative Q or SL means spatial amplification. The decay (or growth) length is

δ = 1 / |Im W|,                                                                                             (43)

and the group velocity, defined for weakly attenuated branches [41,42], is

v_g = [Re (dW/dβ)]⁻¹.                                                                                       (44)

A loss tangent, comparable to the inverse quality factor of resonators, follows from the specific loss:

η_L = 2 Im W / |Re W| = SL / (2π).                                                                          (45)

## 4. Regimes of the purely elastic KG wave

### 4.1 Critical frequencies

For a KG wave with local speed c (c = c_d = 1 for P waves, c = c_s for S waves), Eqs. (27) and (31) give

k²(β) = β²(1 − τ₁²β²) / (c² − ε₁²β²).                                                                       (46)

Define the two critical frequencies

Ω_ε = c/ε₁,   Ω_τ = 1/τ₁.                                                                                   (47)

**Proposition 1 (regimes).** Let ε₁ > 0 and τ₁ > 0. Then

sign k² = sign[(1 − β²/Ω_τ²) / (1 − β²/Ω_ε²)].                                                              (48)

Consequently, the wave propagates (k² > 0) for β < min(Ω_ε, Ω_τ) and for β > max(Ω_ε, Ω_τ). It is evanescent (k² < 0) for min(Ω_ε, Ω_τ) < β < max(Ω_ε, Ω_τ). At β = Ω_ε the wavenumber has a pole; at β = Ω_τ it has a zero.

*Proof.* Write 1 − τ₁²β² = 1 − β²/Ω_τ² and c² − ε₁²β² = c²(1 − β²/Ω_ε²) in Eq. (46). Since β² and c² are positive, Eq. (48) follows. Each factor decreases monotonically in β and changes sign exactly once. ∎

In the stop band the decay rate is

Im k = β √[(1 − τ₁²β²) / (ε₁²β² − c²)],   Ω_ε < β < Ω_τ,                                                    (49)

for the ordering Ω_ε < Ω_τ. This ordering holds when τ₁c < ε₁, which is the case for the data of Table 1. The companion stability analysis shows that it is also required for the elastic KG equation to be stable.

### 4.2 The matched case

**Proposition 2 (matched case).** If ε₁ = cτ₁, then Ω_ε = Ω_τ and

k = β/c   for all β ≠ Ω_τ.                                                                                  (50)

The stop band closes and the wave is exactly non-dispersive.

*Proof.* With ε₁ = cτ₁ the denominator of Eq. (46) becomes c²(1 − τ₁²β²), which cancels the numerator. ∎

Proposition 2 explains a feature of Fig. 4: with τ₁ = 0.01 = ε₁/c_d, the P wave behaves classically.

### 4.3 Group velocity and asymptotics

**Proposition 3 (group velocity).** On a propagating branch,

v_g = dβ/dk = k (c² − ε₁²β²) / [β (1 + ε₁²k² − 2τ₁²β²)].                                                   (51)

*Proof.* Differentiate F(k, β) = k²(c² − ε₁²β²) − β²(1 − τ₁²β²) = 0 implicitly and use v_g = −F_k/F_β. ∎

Near the pole β → Ω_ε from below, Eq. (46) gives

k ≈ √[ Ω_ε R(Ω_ε) / (2ε₁²(Ω_ε − β)) ],                                                                     (52)

so k diverges like (Ω_ε − β)^(−1/2). Both the phase velocity and, by Eq. (51), the group velocity tend to zero. On the optical branch, expanding Eq. (46) for large β gives

k = (τ₁/ε₁) β + (τ₁/(2ε₁β)) (c²/ε₁² − 1/τ₁²) + O(β⁻³).                                                    (53)

Hence the phase and group velocities approach the same limit from opposite sides:

V_p = (ε₁/τ₁) [1 − (c²/ε₁² − 1/τ₁²)/(2β²)] + O(β⁻⁴),                                                       (54)

v_g = (ε₁/τ₁) [1 + (c²/ε₁² − 1/τ₁²)/(2β²)] + O(β⁻⁴).                                                       (55)

When Ω_ε < Ω_τ the bracketed coefficient is negative. V_p then decreases towards ε₁/τ₁ from above, and v_g increases towards it from below. The limit ε₁/τ₁ is the same for P and S waves, because it does not depend on c.

### 4.4 The Eringen limit

For τ₁ = 0, Eq. (46) becomes k² = β²/(c² − ε₁²β²). For large β,

k² = −1/ε₁² − c²/(ε₁⁴β²) + O(β⁻⁴),   Im k → 1/ε₁.                                                          (56)

Eringen's differential model therefore has a single cut-off at c/ε₁. Above it the wave is evanescent at every frequency, and its decay rate tends to 1/ε₁ = 100. There is no second pass band. The time scale τ₁ is what reopens propagation above Ω_τ.

Table 3. Critical frequencies for ε₁ = 0.01 (non-dimensional β and physical frequency f = βω∗/2π).

| Wave | Framework | Ω_ε | Ω_τ | Stop band (β) | Stop band (THz) | High-frequency behaviour |
|---|---|---|---|---|---|---|
| P | KG (τ₁ = 0.006) | 100 | 166.7 | 100–166.7 | 2.45–4.08 | propagates, V → 1.667 |
| S | KG (τ₁ = 0.006) | 49.94 | 166.7 | 49.9–166.7 | 1.22–4.08 | propagates, V → 1.667 |
| P | KG (τ₁ = 0.010) | 100 | 100 | none | none | non-dispersive, V = 1 |
| P | Eringen | 100 | ∞ | above 100 | above 2.45 | evanescent, Im k → 100 |
| S | Eringen | 49.94 | ∞ | above 49.9 | above 1.22 | evanescent, Im k → 100 |
| P, S | Classical | ∞ | ∞ | none | none | non-dispersive |

## 5. Asymptotic analysis of the coupled problem

### 5.1 Dissipation and the thermal wavenumber

The sign of Im q² controls the direction of energy exchange between the two longitudinal modes. Evaluating Eq. (15) with the polynomials of Table 2 gives, for β > 0:

LS:      q² = (τ_qβ² + iβ)/κ,   Im q² = β/κ;                                                                (57)

GN-II:   q² = β²/C_T²,   Im q² = 0;                                                                          (58)

GN-III:  Im q² = κβ³ / (C_T⁴ + κ²β²);                                                                        (59)

MGT:     Im q² = β³(κ − τ_qC_T²) / (C_T⁴ + κ²β²);                                                            (60)

DPL-1:   Im q² = β(1 + τ_qτ_Tβ²) / [κ(1 + τ_T²β²)];                                                          (61)

HDPL:    Im q² = β[1 + β²τ_q(τ_T − τ_q/2)] / [κ(1 + τ_T²β²)].                                                (62)

**Lemma 1.** Im q²(β) > 0 for all β > 0 under LS, GN-III (κ > 0) and DPL-1, for all positive relaxation times. Under MGT this holds if and only if κ > τ_qC_T², and under HDPL it holds if 2τ_T ≥ τ_q. For GN-II, Im q² ≡ 0.

*Proof.* Read off the signs of Eqs. (57)–(62). For HDPL, the bracket is positive for all β if τ_T ≥ τ_q/2. ∎

The conditions in Lemma 1 coincide with the known stability conditions of MGT [13,16] and of second-order DPL conduction [17,18]. So "Im q² > 0 at all frequencies" can be read as "the heat law is dissipative and stable". For copper, κ − τ_qC_T² = 0.99 and 2τ_T − τ_q = 0.02, so both conditions hold.

### 5.2 First-order coupling: elastic mode

Because ε is small for real metals, we expand the elastic root of Eq. (35) about the uncoupled KG wavenumber. Write W₂² = k_e² + Δ. Substituting into Eq. (35) and keeping terms of first order in ε gives

Δ = ε q² k_e² / [S (k_e² − q²)] + O(ε²),                                                                     (63)

and, for real k_e > 0,

W₂ = k_e + Δ/(2k_e) + O(ε²).                                                                                (64)

The imaginary part follows from Eq. (63):

Im W₂ = (ε k_e / (2S)) · Im[q² / (k_e² − q²)] + O(ε²).                                                      (65)

For real k_e the identity

Im[q² / (k_e² − q²)] = k_e² Im q² / |k_e² − q²|²                                                             (66)

then gives the main formula of this section:

Im W₂ ≈ ε k_e³ Im q² / [2 S |k_e² − q²|²].                                                                  (67)

The corresponding relative change of the phase velocity is

ΔV₂ / V₂ ≈ −Re Δ / (2k_e²) = −(ε/(2S)) Re[q²/(k_e² − q²)].                                                   (68)

**Theorem 1 (damped and amplified elastic waves).** Let ε₁ > 0, τ₁ > 0 and τ₁c_d < ε₁, and let the heat law satisfy the conditions of Lemma 1. To first order in ε, the elastic mode is

damped (Im W₂ > 0) for 0 < β < 1/ε₁, and amplified (Im W₂ < 0) for β > 1/τ₁.                               (69)

For GN-II, Im W₂ = 0 to first order in ε.

*Proof.* In both pass bands k_e is real and positive (Proposition 1), and Im q² > 0 by Lemma 1. By Eq. (67), sign Im W₂ = sign S. S is positive below 1/ε₁ and negative above it, and the optical band lies above 1/τ₁ > 1/ε₁. ∎

Theorem 1 is valid as long as the correction Δ is small compared with k_e², that is,

ε |q²| ≪ |S| |k_e² − q²|.                                                                                   (70)

Condition (70) fails in two places. It fails near the pole S = 0, where the effective coupling of Eq. (39) diverges. It also fails where k_e² ≈ q². For the data of Table 1 the latter happens for GN-II, GN-III and MGT at low frequency, because C_T = c_d. Section 6.7 shows that elsewhere Eq. (67) reproduces the exact roots to four or five significant digits.

The thermal mode admits the same expansion. With W₁² = q² + Δ₁,

Δ₁ = ε q⁴ / [S (q² − k_e²)] + O(ε²).                                                                         (71)

### 5.3 Low-frequency limits

For LS, DPL-1 and HDPL the thermal wavenumber is diffusive at low frequency:

q² = iβ/κ + O(β²),   so |q²| ≫ β² for β ≪ 1/τ_q.                                                              (72)

In this regime the small root of Eq. (36) can be expanded in powers of β²/q². Using R, S → 1,

W₂² = β²/(1 + ε) − ε β⁴ / [(1 + ε)³ q²] + O(β⁶/q⁴).                                                         (73)

The elastic mode therefore travels at the adiabatic speed and is weakly damped:

V₂ → √(1 + ε),                                                                                              (74)

Q₂ ≈ ε κ β² / [2(1 + ε)^(5/2)].                                                                              (75)

The large root gives the diffusive thermal mode:

W₁² = (1 + ε) q² + O(β²),                                                                                   (76)

V₁ ≈ √(2κβ/(1 + ε)),   Q₁ ≈ √((1 + ε)β/(2κ)).                                                               (77)

For copper, Eq. (74) gives V₂ → 1.0084, and Eq. (75) gives Q₂ = 8.06 × 10⁻⁵ at β = 0.1, against the exact 8.01 × 10⁻⁵. Eq. (77) gives V₁ = 0.1402 and Q₁ = 0.0713 at β = 0.01, both identical to the exact values to four digits.

### 5.4 High-frequency decoupling

When ε₁ > 0, Eq. (39) gives

ε_eff = −ε/(ε₁²β²) + O(β⁻⁴) → 0   (β → ∞).                                                                 (78)

The two longitudinal modes therefore decouple at high frequency. The elastic mode follows the KG optical branch, Eqs. (53)–(55), and the thermal mode tends to the uncoupled thermal wavenumber q(β). Expanding Eq. (15) for large β gives the following leading terms.

LS:     q = β √(τ_q/κ) + i / (2√(τ_qκ)) + O(β⁻¹);                                                           (79)

MGT:    q = β √(τ_q/κ) + i (1 − τ_qC_T²/κ) / (2√(τ_qκ)) + O(β⁻¹);                                            (80)

HDPL:   q = β τ_q / √(2κτ_T) + i (1 − τ_q/(2τ_T)) / √(2κτ_T) + O(β⁻¹);                                         (81)

GN-II:  q = β / C_T   (exactly);                                                                             (82)

GN-III: q = (1 + i) √(β/(2κ)) + O(β^(−1/2));                                                                (83)

DPL-1:  q = (1 + i) √(βτ_q/(2κτ_T)) + O(β^(−1/2)).                                                           (84)

*Derivation of Eq. (80).* q² = β²(1 − iτ_qβ)/(C_T² − iκβ) = (τ_q/κ)β²[1 + (i/β)(1/τ_q − C_T²/κ) + O(β⁻²)]. Taking the square root gives Eq. (80). Eqs. (79) and (81) follow in the same way, and Eqs. (83)–(84) from q² ≈ iβ/κ and q² ≈ iβτ_q/(κτ_T). ∎

**Proposition 4 (thermal-mode limits).** Under KG or Eringen nonlocality, the thermal mode has the high-frequency limits of Table 4. The MGT attenuation limit is positive if and only if κ > τ_qC_T², and the HDPL attenuation limit is positive if and only if 2τ_T > τ_q.

Proposition 4 links the attenuation of the thermal front at high frequency directly to the stability of the heat law. It also explains the close agreement between LS and MGT reported in [40]. Their leading terms in Eqs. (79) and (80) are identical, and they differ only in the attenuation, by the factor τ_qC_T²/κ = 0.01.

In classical elasticity the coupling does not vanish (S ≡ 1). For LS, Eq. (36) with x = W²/β² and q² ≈ τ_qβ²/κ then reduces to

x² − [1 + τ_q(1 + ε)/κ] x + τ_q/κ = 0,                                                                       (85)

whose small root gives V₁ → 10.0008 instead of 10. The difference is O(ε), so for copper the classical and nonlocal thermal limits differ by only 0.008%.

Table 4. Asymptotic limits (data of Table 1, ε = 0.0168). "Unbounded" means growth proportional to √β.

| Model | Low frequency: V₂, Q₂/β² | Low frequency: V₁/√β, Q₁/√β | High frequency (KG): V₁ | High frequency (KG): Q₁ | High frequency (KG): V₂ |
|---|---|---|---|---|---|
| LS | 1.0084, 8.06e−3 | 1.4025, 0.7130 | 10 | 5.000 | 1.667 |
| GN-II | mixed (C_T = c_d) | mixed | 1 | 0 | 1.667 |
| GN-III | mixed (C_T = c_d) | mixed | unbounded | unbounded | 1.667 |
| DPL-1 | 1.0084, 8.06e−3 | 1.4025, 0.7130 | unbounded | unbounded | 1.667 |
| HDPL | 1.0084, 8.06e−3 | 1.4025, 0.7130 | 17.32 | 3.849 | 1.667 |
| MGT | mixed (C_T = c_d) | mixed | 10 | 4.950 | 1.667 |

### 5.5 Decay in the stop band

Inside the P stop band k_e² < 0 and Eq. (63) still applies. To leading order, the elastic mode decays at the KG rate of Eq. (49):

Im W₂ ≈ β √[R / (−S)],   1/ε₁ < β < 1/τ₁.                                                                  (86)

At β = 120 this gives Im W₂ = 125.5, against the exact 125.3 for LS. In physical units the decay length is δ·l∗ = 0.22 nm.

### 5.6 Root selection

Each value of W² in Eq. (37) has two square roots ±W. In the pass bands, |Re W| ≥ |Im W|, and we select the root that carries energy towards +x. On every branch considered here the group velocity of Eq. (51) is positive, so this is the root with

Re W > 0   (pass band; the sign of Im W is then determined, not imposed).                                    (87)

In the stop bands |Im W| > |Re W|, and we select the evanescent root, which decays away from the source:

Im W > 0   (stop band).                                                                                     (88)

For dissipative heat laws, rule (87) gives Im W₂ < 0 on the optical branch, consistent with Theorem 1. The rule Im W > 0 used in [40] instead selects Re W₂ < 0 there, which is a wave travelling towards the source. The rigorous criterion is the Briggs–Bers pinch condition [43]. Rule (87) agrees with it for branches with positive group velocity and small temporal growth, which is the situation here.

## 6. Numerical results

### 6.1 Method

Eq. (36) was solved in closed form on 2500 logarithmically spaced frequencies in 0.05 ≤ β ≤ 3000, using the numerically stable form of the quadratic formula. The modes were identified at β = 3000, where KG nonlocality decouples them (Eq. (78)): the root closest to q² is called thermal. The labels were then carried to lower frequencies by minimum-relative-distance continuation. In classical GN-II, where q² = k_e² exactly, the faster root is called thermal by convention. All computations use the Python standard library only (Appendix A).

### 6.2 Purely elastic waves

Fig. 1 maps the regimes of Proposition 1 in the (τ₁, β) plane for ε₁ = 0.01. The P and S stop bands narrow as τ₁ increases and close at τ₁ = ε₁/c_d = 0.01 and τ₁ = ε₁/c_s = 0.02, respectively. Beyond these values the order of Ω_ε and Ω_τ is reversed.

[Insert Figure 1 here]

Figure 1. Regime map of KG nonlocal elasticity for ε₁ = 0.01. The black curve is β = 1/τ₁; the dashed lines are the cut-offs c_d/ε₁ = 100 and c_s/ε₁ = 49.9. Pink regions are stop bands of both P and S waves; blue regions are S-only stop bands. The green line marks τ₁ = 0.006, used in [40]. Dotted lines mark τ₁ = ε₁/c_d and τ₁ = ε₁/c_s, where the bands close.

Fig. 2 shows Re W and Im W for the purely elastic P wave. The KG wavenumber diverges at β = 100, is purely imaginary up to β = 166.7, and then grows linearly with slope τ₁/ε₁ = 0.6 on the optical branch. Eringen's wavenumber stays imaginary above β = 100, with Im W decreasing to 100 as Eq. (56) predicts.

[Insert Figure 2 here]

Figure 2. Purely elastic P wave (γ = 0): (a) Re W and (b) Im W versus β for KG (ε₁ = 0.01, τ₁ = 0.006), Eringen (τ₁ = 0) and classical elasticity. The shaded region is the KG stop band.

### 6.3 Transverse wave

Fig. 3 and Table 5 show the shear wave. Its phase velocity falls from c_s = 0.4994 to 0.10 at β = 49 and vanishes at Ω_ε = 49.94, which is the behaviour reported in Fig. 7(a) of [40]. Between β = 49.94 and 166.7 the shear wave is evanescent, with Im W₃ = 168 at β = 60 and 76 at β = 120. This decay is not thermoelastic damping: Q₃ is zero in every pass band and for every heat law, in agreement with [40], but it is non-zero in the stop band. Above β = 166.7 the KG shear wave propagates again, with V₃ = 8.09 at β = 170 and 1.69 at β = 1000. Eringen's shear wave remains evanescent.

Table 5. Transverse wave (V₃, Im W₃). A dash means evanescent.

| β | KG | Eringen | Classical |
|---|---|---|---|
| 10 | 0.4901, 0 | 0.4892, 0 | 0.4994, 0 |
| 40 | 0.3079, 0 | 0.2989, 0 | 0.4994, 0 |
| 49 | 0.1006, 0 | 0.0962, 0 | 0.4994, 0 |
| 60 | –, 168.3 | –, 180.4 | 0.4994, 0 |
| 120 | –, 76.32 | –, 110.0 | 0.4994, 0 |
| 170 | 8.085, 0 | –, 104.6 | 0.4994, 0 |
| 300 | 1.976, 0 | –, 101.4 | 0.4994, 0 |
| 1000 | 1.688, 0 | –, 100.1 | 0.4994, 0 |

[Insert Figure 3 here]

Figure 3. Transverse wave: (a) Re W₃ and (b) Im W₃ versus β. The shaded region is the S stop band 49.9 < β < 166.7.

Fig. 4 shows the phase and group velocities of the elastic P wave. On the acoustic branch both decrease towards zero at β = 100. On the optical branch the phase velocity decreases from infinity and the group velocity increases from zero, both towards ε₁/τ₁ = 1.667, as Eqs. (54) and (55) predict. At β = 200 the exact values are V_p = 2.61 and v_g = 0.888. For the matched case τ₁ = 0.01, both velocities equal 1 at all frequencies (Proposition 2).

[Insert Figure 4 here]

Figure 4. Elastic P wave: (a) phase velocity and (b) group velocity versus β. The matched case τ₁ = ε₁/c_d = 0.01 is non-dispersive. The dotted line is ε₁/τ₁ = 1.667.

### 6.4 Thermal mode

Fig. 5 and Table 6 show the thermal mode. It depends almost entirely on the heat law. For the five dissipative models, KG and classical values differ by at most 0.8% in V₁ and 2.9% in Q₁ over the whole range; the largest differences occur just above β = 1/τ₁, where the optical elastic branch is cut on.

GN-II is the exception. Its classical thermal velocity stays at 1.067 at all frequencies, whereas under KG it tends to C_T = 1 because the coupling vanishes (Eq. (78)). The limits of Proposition 4 are reached to four digits at β = 3000. The HDPL velocity overshoots to 18.3 near β = 160 before relaxing to 17.32; this overshoot also occurs in the classical case and is therefore a property of the heat law. GN-III and DPL-1 grow without bound, as Eqs. (83)–(84) predict. At β = 3000, Eq. (83) gives V₁ = 77.46 and Q₁ = 38.73 for GN-III, against the exact 77.45 and 38.72.

Table 6. Thermal mode (V₁, Q₁) under KG nonlocality, ε = 0.0168.

| Model | β = 1 | β = 10 | β = 50 | β = 200 | β = 3000 | Limit |
|---|---|---|---|---|---|---|
| LS | 1.394, 0.7029 | 4.247, 2.123 | 7.861, 3.929 | 9.716, 4.862 | 9.999, 4.999 | 10, 5 |
| GN-II | 1.067, 0 | 1.065, 0 | 1.038, 0 | 1.003, 0 | 1.000, 0 | 1, 0 |
| GN-III | 1.282, 0.3143 | 4.268, 2.112 | 9.900, 4.948 | 19.96, 9.978 | 77.45, 38.72 | unbounded |
| DPL-1 | 1.405, 0.7082 | 4.591, 2.280 | 11.67, 5.134 | 25.68, 8.986 | 95.38, 31.80 | unbounded |
| HDPL | 1.405, 0.7082 | 4.601, 2.273 | 11.90, 4.759 | 18.20, 4.551 | 17.33, 3.853 | 17.32, 3.849 |
| MGT | 1.279, 0.3103 | 4.079, 1.998 | 7.814, 3.865 | 9.710, 4.811 | 9.999, 4.949 | 10, 4.95 |

[Insert Figure 5 here]

Figure 5. Thermal mode under the six heat laws: (a) phase velocity V₁ and (b) attenuation Q₁ versus β (logarithmic axis). Solid and dashed lines are KG; dotted lines are classical elasticity and nearly coincide with KG. Grey dotted lines mark the limits of Proposition 4.

### 6.5 Elastic mode

The elastic mode is where the elasticity framework matters (Table 7, Fig. 6).

- **Acoustic pass band (β < 100).** The elastic mode slows from V₂ ≈ 1.004 at β = 1 to V₂ = 0.18 at β = 99. Its attenuation is of order 10⁻² for the five dissipative models and zero for GN-II.
- **P stop band (100 < β < 166.7).** Re W₂ is nearly zero and Im W₂ is large: 125.3 at β = 120 and 36.3 at β = 160. The decay length 1/Im W₂ is 0.008–0.028 in units of l∗, or 0.22–0.75 nm. It agrees within 1% across all six heat laws. Fig. 6(a) shows a sharp minimum of the decay length at the pole β = 100.
- **Optical pass band (β > 166.7).** The elastic mode propagates again, with V₂ = 2.61 at β = 200, 1.73 at β = 500 and 1.668 at β = 3000. With rule (87), Im W₂ is negative for LS, GN-III, DPL-1, HDPL and MGT and zero for GN-II, as Theorem 1 predicts. The gain is small: the most negative value of Im W₂ is −0.15 (LS, MGT) just above β = 1/τ₁; it is −0.0084 at β = 200 and decays like β⁻².
- **Eringen.** There is no optical band. Above β = 100, Im W₂ decreases monotonically towards 1/ε₁ = 100.
- **Classical.** The elastic mode is non-dispersive. Q₂ is constant at 0.0084–0.0086 (LS, GN-III, MGT) or decreases slowly (DPL-1, HDPL).

Table 7. Elastic mode (V₂, Q₂), ε = 0.0168. A dash means evanescent (Re W₂ ≈ 0).

| Model | KG β = 50 | KG β = 120 | KG β = 200 | KG β = 500 | Eringen β = 200 | Classical β = 200 |
|---|---|---|---|---|---|---|
| LS | 0.9078, 0.0103 | –, 125.3 | 2.609, −0.0084 | 1.732, −6.4e−4 | –, 115.5 | 0.9999, 0.0086 |
| GN-II | 0.8743, 0 | –, 126.4 | 2.600, 0 | 1.731, 0 | –, 115.7 | 0.9373, 0 |
| GN-III | 0.9079, 0.0102 | –, 125.3 | 2.609, −0.0073 | 1.732, −6.1e−4 | –, 115.5 | 1.000, 0.0084 |
| DPL-1 | 0.9079, 0.0089 | –, 125.3 | 2.609, −0.0051 | 1.732, −4.1e−4 | –, 115.5 | 1.000, 0.0059 |
| HDPL | 0.9079, 0.0081 | –, 125.3 | 2.609, −0.0038 | 1.732, −2.8e−4 | –, 115.5 | 1.000, 0.0042 |
| MGT | 0.9078, 0.0102 | –, 125.3 | 2.609, −0.0083 | 1.732, −6.4e−4 | –, 115.5 | 0.9999, 0.0085 |

[Insert Figure 6 here]

Figure 6. Elastic mode under KG nonlocality. (a) Decay length 1/|Im W₂| on a logarithmic scale; the shaded region is the P stop band. GN-II is absent outside the band because its attenuation is zero. (b) Signed specific loss SL₂ = 4π Im W₂/|Re W₂| (× 10³) in the optical pass band; negative values are spatial gain.

### 6.6 Effect of the characteristic time

Fig. 7 shows the LS elastic mode for τ₁ = 0.004, 0.006, 0.008 and 0.0095. The lower band edge stays at β = 100. The upper edge moves to 1/τ₁ = 250, 166.7, 125 and 105.3, so the stop band shrinks from 150 to 5.3 units of β. The optical-branch velocity at β = 300 decreases from 4.26 to 1.06, approaching ε₁/τ₁ in each case. The gain at β = 300 decreases in magnitude from 6.6 × 10⁻³ to 1.1 × 10⁻³ as τ₁ increases. As τ₁ → ε₁/c_d the response approaches the non-dispersive matched case of Proposition 2.

[Insert Figure 7 here]

Figure 7. Effect of τ₁ on the LS elastic mode (ε₁ = 0.01): (a) phase velocity V₂ and (b) |Im W₂| versus β. The upper band edge is β = 1/τ₁.

### 6.7 Validation of the asymptotic formulas

Fig. 8(a) compares Eq. (67) with the exact elastic-mode attenuation for LS, GN-III and HDPL. For LS and HDPL, the two agree to within 0.5% at β = 1 and to four or five digits at β = 50, 300 and 3000. Examples are 1.0334 × 10⁻² against 1.0335 × 10⁻² for LS at β = 50, and 7.0630 × 10⁻⁶ in both cases for HDPL at β = 3000. For GN-III the formula fails below β ≈ 3, where k_e² ≈ q² and condition (70) is violated, but it matches the exact values to five digits above β = 10. Fig. 8(b) confirms the low-frequency thermal limits of Eq. (77) for LS.

[Insert Figure 8 here]

Figure 8. Validation of the asymptotic results. (a) Elastic-mode |Im W₂| from Eq. (67) (lines) against exact roots (dots) for LS, GN-III and HDPL under KG nonlocality. (b) Low-frequency LS thermal mode: exact V₁ and Q₁ against Eq. (77).

### 6.8 Effect of the coupling constant

Table 8 compares the physical coupling ε = 0.0168 with the value ε = 1.68 implied by the expansion coefficient printed in [40]. Thermal-mode velocities change by a few per cent, but the elastic-mode attenuation increases by two orders of magnitude, from 0.0042 to 1.00 at β = 1 for LS. The optical-band gain increases in the same proportion. For GN-II with ε = 1.68 a band of complex-conjugate wavenumbers appears near β = 200 (W ≈ 116 ± 42i in the two modes). This is the signature of a collision between the thermal branch and the optical elastic branch, which cannot occur at the physical coupling. Coupling-dependent results should therefore be recomputed with the physical α_t before any comparison with experiment.

Table 8. Effect of the coupling constant (KG, LS and GN-II).

| Quantity | ε = 0.0168 | ε = 1.68 |
|---|---|---|
| LS: V₂, Q₂ at β = 1 | 1.004, 0.0042 | 0.773, 1.002 |
| LS: V₂, Q₂ at β = 50 | 0.908, 0.0103 | 0.900, 1.024 |
| LS: Im W₂ at β = 200 | −0.0084 | −0.863 |
| LS: V₁, Q₁ at β = 10 | 4.247, 2.123 | 3.988, 1.901 |
| GN-II: V₁, V₂ at β = 1 | 1.067, 0.937 | 0.544, 1.840 |
| GN-II near β = 200 | real wavenumbers | complex-conjugate pair: V = 1.719, Q = ±42.3 |

## 7. Discussion

### 7.1 Physical scales

The physical frequency and length associated with non-dimensional values are

f = β ω∗ / (2π),   δ_phys = l∗ / |Im W|.                                                                        (89)

With ε₁ = 0.01, the internal length is ε₁l∗ = 0.27 nm, close to the nearest-neighbour distance of copper (0.256 nm). The P stop band (2.45–4.08 THz) and the optical band above it lie inside the measured phonon spectrum of copper, whose highest frequency is about 7 THz [46]. Copper is a monatomic fcc metal and has no optical phonons. The KG gap at these parameters therefore has no counterpart in the real lattice dynamics of copper.

The KG continuum, as parametrized in [40], is thus being used at wavelengths of a few lattice spacings, where it can at best be a fitted model. Before the stop bands are interpreted physically, ε₁ and τ₁ should be calibrated against measured phonon dispersion, as is customary for gradient models [33]. For metamaterials and phononic crystals [36], where gaps are designed and length scales are much larger than atomic, the KG regimes of Section 4 may be directly useful.

### 7.2 Why the optical wave is amplified

Theorem 1 has a simple energetic interpretation. With the multiplier u̇, the mechanical energy of KG elasticity contains the term −½ρτ₁²|ü|², and it is negative for the optical oscillation at frequency 1/τ₁. Thermal dissipation removes energy from this budget, so on the optical branch it increases the wave amplitude rather than decreasing it. This is the mechanism of negative-energy waves in fluids and plasmas [44,45]. In the frequency domain it appears as Im W₂ < 0 for a wave whose energy travels away from the source. The neutrality of GN-II, which has no dissipation, supports this interpretation.

### 7.3 Comparison with the source study

Table 9 compares the present results with the corresponding statements in [40].

Table 9. Comparison with Mondal and Mukhopadhyay [40].

| Topic | Ref. [40] | Present study |
|---|---|---|
| Denominators c² − ε₁²β² | stated non-zero for all admissible parameters | vanish at β = c/ε₁ (49.9 for S, 100 for P) |
| Shear velocity near β = 50 | decreases to zero | exact cut-off Ω_ε = c_s/ε₁; stop band 49.9–166.7 |
| Behaviour above 1/τ₁ | sudden drops in V₁ | cut-on of the optical branch, with V → ε₁/τ₁ |
| Root selection | Im W > 0 | Re W > 0 in pass bands, Im W > 0 in stop bands |
| Optical-band specific loss | positive | negative (gain) for dissipative laws, zero for GN-II |
| LS–MGT similarity | observed numerically | identical leading terms, Eqs. (79)–(80) |
| Scaling | l = k/(ρcV), degenerate for GN-II | k_ref used for all models |
| Coupling constant | α_t = 1.78 × 10⁻⁴ K⁻¹, ε = 1.68 | α_t = 1.78 × 10⁻⁵ K⁻¹, ε = 0.0168 |

We could not reproduce the numerical values in the figures of [40], for instance the thermal-mode velocity limit of about 9.66 for LS. The present value is 10 under KG and 10.0008 in the classical case. Because the factor L/V in [40] is undefined, we could not trace the cause of the difference.

### 7.4 Limitations

The analysis is linear and restricted to isotropic, unbounded media. Rule (87) relies on the positive group velocities of the elastic branches. A full Briggs–Bers treatment of the signaling problem [43] would make the branch choice rigorous, including near the GN-II branch collision at strong coupling. The modes are labelled "thermal" and "elastic" by convention; where they nearly coincide (classical GN-II, and GN-III and MGT at low frequency, because C_T = c_d), these labels have no physical meaning.

## 8. Conclusions

1. Every KG bulk wave has two exact critical frequencies, c/ε₁ and 1/τ₁. The wave is evanescent between them and propagates on an optical branch above both, with phase and group velocities tending to ε₁/τ₁ from above and below. For copper data the stop bands are 2.45–4.08 THz (P) and 1.22–4.08 THz (S).
2. When ε₁ = cτ₁ the stop band closes and the KG wave is exactly non-dispersive. Eringen's model has only the lower cut-off and no upper pass band, and its decay rate tends to 1/ε₁.
3. The coupled dispersion relation factorizes as S(W² − k_e²)(W² − q²) = εq²W². Coupling acts only through ε/S, which vanishes at high frequency under KG and Eringen nonlocality.
4. Im q² > 0 at all frequencies exactly when the heat law is dissipative and stable. To first order in ε, the elastic mode is damped below c/ε₁ and amplified above 1/τ₁ for LS, GN-III, DPL-1, HDPL and MGT, and neutral for GN-II. Eq. (67) gives the attenuation and agrees with the exact roots to four or five digits.
5. The usual rule Im W > 0 hides the amplification by selecting, in the optical band, a wave that travels towards its source.
6. The thermal mode tends to closed-form limits at high frequency. The MGT and HDPL attenuation limits are positive exactly when κ > τ_qC_T² and 2τ_T > τ_q. LS and MGT share their leading terms, which explains their similarity in [40]. At low frequency the elastic mode travels at the adiabatic speed √(1 + ε) and the thermal mode is diffusive.
7. The thermal expansion coefficient printed in [40] is ten times the copper value and inflates the coupling constant 100-fold. With the physical value, coupling effects on the elastic mode are about 100 times smaller.

## Appendix A. Reproducibility

All results come from the following scripts in this repository, which use the Python 3 standard library only:

- `kg_thermoelastic_core.py`: model polynomials, dispersion relations, root selection, continuation and closed-form limits;
- `kg_plot.py`: plotting helper built on the repository's PNG canvas;
- `generate_kg_stopband_figures.py`: Figs. 1–8 and `kg_stopband_figures/numerical_summary.txt`, from which Tables 4–8 are taken.

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

[11] Tzou DY. The generalized lagging response in small-scale and high-rate heating. Int J Heat Mass Transfer. 1995;38(17):3231–3240.

[12] Chandrasekharaiah DS. Hyperbolic thermoelasticity: a review of recent literature. Appl Mech Rev. 1998;51(12):705–729.

[13] Quintanilla R. Moore–Gibson–Thompson thermoelasticity. Math Mech Solids. 2019;24(12):4020–4031.

[14] Conti M, Pata V, Quintanilla R. Thermoelasticity of Moore–Gibson–Thompson type with history dependence in the temperature. Asymptot Anal. 2020;120(1–2):1–21.

[15] Bazarra N, Fernández JR, Quintanilla R. Analysis of a Moore–Gibson–Thompson thermoelastic problem. J Comput Appl Math. 2021;382:113058.

[16] Kaltenbacher B, Lasiecka I, Marchand R. Wellposedness and exponential decay rates for the Moore–Gibson–Thompson equation arising in high intensity ultrasound. Control Cybern. 2011;40(4):971–988.

[17] Quintanilla R, Racke R. A note on stability in dual-phase-lag heat conduction. Int J Heat Mass Transfer. 2006;49(7–8):1209–1213.

[18] Quintanilla R, Racke R. Qualitative aspects in dual-phase-lag thermoelasticity. SIAM J Appl Math. 2006;66(3):977–1001.

[19] Fabrizio M, Franchi F. Delayed thermal models: stability and thermodynamics. J Therm Stresses. 2014;37(2):160–173.

[20] Deresiewicz H. Plane waves in a thermoelastic solid. J Acoust Soc Am. 1957;29(2):204–209.

[21] Chadwick P, Sneddon IN. Plane waves in an elastic solid conducting heat. J Mech Phys Solids. 1958;6:223–230.

[22] Puri P. Plane waves in generalized thermoelasticity. Int J Eng Sci. 1973;11(7):735–744.

[23] Chandrasekharaiah DS. Thermoelastic plane waves without energy dissipation. Mech Res Commun. 1996;23(5):549–555.

[24] Puri P, Jordan PM. On the propagation of plane waves in type-III thermoelastic media. Proc R Soc Lond A. 2004;460:3203–3221.

[25] Prasad R, Kumar R, Mukhopadhyay S. Propagation of harmonic plane waves under thermoelasticity with dual-phase-lags. Int J Eng Sci. 2010;48(12):2028–2043.

[26] Jangid K, Gupta M, Mukhopadhyay S. On propagation of harmonic plane waves under the Moore–Gibson–Thompson thermoelasticity theory. Waves Random Complex Media. 2024;34(3):1976–1999.

[27] Jangid K, Mukhopadhyay S. A domain of influence theorem under MGT thermoelasticity theory. Math Mech Solids. 2021;26(2):285–295.

[28] Eringen AC. Linear theory of nonlocal elasticity and dispersion of plane waves. Int J Eng Sci. 1972;10(5):425–435.

[29] Eringen AC. Theory of nonlocal thermoelasticity. Int J Eng Sci. 1974;12(12):1063–1077.

[30] Eringen AC. On differential equations of nonlocal elasticity and solutions of screw dislocation and surface waves. J Appl Phys. 1983;54(9):4703–4710.

[31] Eringen AC. Nonlocal Continuum Field Theories. New York: Springer; 2002.

[32] Challamel N, Rakotomanana L, Le Marrec L. A dispersive wave equation using nonlocal elasticity. C R Mécanique. 2009;337(8):591–595.

[33] Askes H, Aifantis EC. Gradient elasticity in statics and dynamics: an overview of formulations, length scale identification procedures, finite element implementations and new results. Int J Solids Struct. 2011;48(13):1962–1990.

[34] Sarkar N, Tomar SK. Plane waves in nonlocal thermoelastic solid with voids. J Therm Stresses. 2019;42(5):580–606.

[35] Das N, Sarkar N, Lahiri A. Reflection of plane waves from the stress-free isothermal and insulated boundaries of a nonlocal thermoelastic solid. Appl Math Model. 2019;73:526–544.

[36] Hussein MI, Leamy MJ, Ruzzene M. Dynamics of phononic materials and structures: historical origins, recent progress, and future outlook. Appl Mech Rev. 2014;66(4):040802.

[37] Lazar M, Agiasofitou E. Nonlocal elasticity of Klein–Gordon type: fundamentals and wave propagation. Wave Motion. 2022;114:103038.

[38] Lazar M, Agiasofitou E. Nonlocal elasticity of Klein–Gordon type with internal length and time scales: constitutive modelling and dispersion relations. KIT Open Repository; https://publikationen.bibliothek.kit.edu/1000165899 (journal version to be confirmed before submission).

[39] Singh B. Wave propagation in context of Moore–Gibson–Thompson thermoelasticity with Klein–Gordon nonlocality. Vietnam J Mech. 2024;46(2):104–118.

[40] Mondal S, Mukhopadhyay S. Modeling and analysis of wave propagation under generalized Klein–Gordon nonlocal thermoelasticity theories. Mech Mater. 2026;222:105834.

[41] Brillouin L. Wave Propagation and Group Velocity. New York: Academic Press; 1960.

[42] Achenbach JD. Wave Propagation in Elastic Solids. Amsterdam: North-Holland; 1973.

[43] Briggs RJ. Electron-Stream Interaction with Plasmas. Cambridge, MA: MIT Press; 1964.

[44] Cairns RA. The role of negative energy waves in some instabilities of parallel flows. J Fluid Mech. 1979;92(1):1–14.

[45] Krechetnikov R, Marsden JE. Dissipation-induced instabilities in finite dimensions. Rev Mod Phys. 2007;79(2):519–553.

[46] Svensson EC, Brockhouse BN, Rowe JM. Crystal dynamics of copper. Phys Rev. 1967;155(3):619–632.
