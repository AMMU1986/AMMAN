# Nomenclature

**Manuscript:** From Pure Fluids to Nanofluids: Extending ANFIS-Based Convergence Control to Dispersed Phase Heat Transfer

---

## General Symbols (Roman)

| Symbol | Description | Unit |
|--------|-------------|------|
| a_P | Coefficient of the central computational point in the discretized equation | – |
| a_nb | Coefficients of neighbouring nodes | – |
| b | Source term in the discretized equation | – |
| C_p | Specific heat capacity at constant pressure | J kg⁻¹ K⁻¹ |
| **d** | Displacement vector (residual-based correction) | – |
| ‖d‖ | Euclidean (2-)norm of the displacement vector | – |
| D | Fluid domain / gap width (conjugate ratio Dk_f/Lk_w) | m |
| e_n | Error in tuning index at iteration n | – |
| g | Gravitational acceleration | m s⁻² |
| Gr | Grashof number | – |
| k | Thermal conductivity | W m⁻¹ K⁻¹ |
| L | Solid wall thickness (conjugate ratio Dk_f/Lk_w) | m |
| Nu | Nusselt number | – |
| P | Pressure | Pa |
| Pe | Péclet number | – |
| Ra | Rayleigh number | – |
| Re | Reynolds number | – |
| T | Temperature | K |
| T_c | Cold-wall temperature | K |
| T_h | Hot-wall temperature | K |
| u | Velocity component in x-direction | m s⁻¹ |
| U | Lid (top-wall) velocity | m s⁻¹ |
| v | Velocity component in y-direction | m s⁻¹ |
| x, y | Cartesian coordinates | m |

---

## Greek Symbols

| Symbol | Description | Unit |
|--------|-------------|------|
| α | Under-relaxation factor (0 < α ≤ 1) | – |
| α_0 | Initial relaxation factor | – |
| Δα | Change in relaxation factor (ANFIS output) | – |
| β | Thermal expansion coefficient | K⁻¹ |
| γ_n | Tuning index at iteration n | – |
| Δe_n | Change in error at iteration n | – |
| μ | Dynamic viscosity | Pa s |
| ρ | Density | kg m⁻³ |
| ϕ | Nanoparticle volume fraction | – |
| φ_P | Generic transported variable at point P | – |
| φ_nb | Generic transported variable at neighbouring nodes | – |

---

## Subscripts

| Subscript | Description |
|-----------|-------------|
| c | Cold (wall) |
| f | Base fluid |
| h | Hot (wall) |
| n | Current iteration |
| n−1 | Previous iteration |
| n+1 | Next iteration |
| nb | Neighbouring node |
| nf | Nanofluid (effective property) |
| P | Central computational point |
| s | Solid nanoparticle |

---

## Superscripts

| Superscript | Description |
|-------------|-------------|
| * | Updated (under-relaxed) value of a variable |
| 2 | Second-order (used in second derivatives, e.g. ∂²u/∂x²) |

---

## Abbreviations / Acronyms

| Acronym | Definition |
|---------|------------|
| ANFIS | Adaptive-Network-Based Fuzzy Inference System |
| CFD | Computational Fluid Dynamics |
| CHT | Conjugate Heat Transfer |
| CPU | Central Processing Unit |
| SIMPLER | Semi-Implicit Method for Pressure-Linked Equations Revised |
| SOR | Successive Over-Relaxation |

---

**Notes:**
1. The symbol φ (phi) is recommended for the generic transported variable, while ϕ (or φᵥ) is recommended for the nanoparticle volume fraction, to avoid overloading a single glyph across Eqs. (5)–(11).
2. The conjugate conduction–convection ratio appears as both Dk_f/Lk_w (Sec. 2.5) and Lk_w/Dk_f (Sec. 3.3); recommend using one consistent form throughout.
