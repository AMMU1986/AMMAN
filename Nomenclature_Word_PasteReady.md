# Nomenclature — Word-Ready (paste directly)

**Two ways to use this:**
1. **Best:** open `Nomenclature_Word.docx` and copy the whole block (the symbol
   list is a native Word table; subscripts/abbreviations are formatted
   paragraphs). Paste into the manuscript — formatting and Unicode symbols
   carry over.
2. **Plain paste:** copy the Unicode text below straight into Word. The
   superscripts (⁻¹, ², ³), subscripts (ₚ, ₕ), the over-dot ṁ, and Greek
   letters (φ, ρ, ε, μ, Δ) are real Unicode characters, so they display
   correctly without using Word's superscript/subscript buttons.

---

## Nomenclature

| Symbol | Description | Unit |
|--------|-------------|------|
| *A* | heat transfer surface area | m² |
| *c*ₚ | specific heat | J kg⁻¹ K⁻¹ |
| *D*ₕ | hydraulic diameter | m |
| *h* | heat transfer coefficient | W m⁻² K⁻¹ |
| *k* | thermal conductivity | W m⁻¹ K⁻¹ |
| *ṁ* | mass flow rate | kg s⁻¹ |
| *N* | number of samples | – |
| *Nu* | Nusselt number | – |
| *Pr* | Prandtl number | – |
| *Q* | heat transfer rate | W |
| *Re* | Reynolds number | – |
| *T* | temperature | K |
| *U* | velocity | m s⁻¹ |
| *ε* | radiator effectiveness | – |
| *φ* | nanoparticle volume concentration | % |
| *μ* | dynamic viscosity | kg m⁻¹ s⁻¹ |
| *ρ* | density | kg m⁻³ |
| *ΔT*_LMTD_ | log-mean temperature difference | K |

**Subscripts:** nf = nanofluid;  p = particles;  w = base fluid (water);  in = inlet;  out = outlet;  a = air;  c = coolant;  max = maximum;  min = minimum.

**Abbreviations:** DIW = deionized water;  NF = nanofluid;  HNF = hybrid nanofluid;  ML = machine learning;  MLRR = Multiple Linear Ridge Regression;  PLSR = Partial Least Squares Regression;  MLP = Multi-Layer Perceptron;  SVR = Support Vector Regression;  AdaBoost (AB) = Adaptive Boosting;  RFR = Random Forest Regression.

---

### Unicode reference (for manual retyping if needed)
- Superscripts: ⁻ (U+207B), ¹ (U+00B9), ² (U+00B2), ³ (U+00B3)
- Subscripts: ₚ (U+209A), ₕ (U+2095)
- Over-dot (ṁ): m + U+0307, or the precomposed ṁ (U+1E45)
- Greek: φ (U+03C6), ρ (U+03C1), ε (U+03B5), μ (U+03BC), Δ (U+0394)
- En dash for "no unit": – (U+2013)

> Note on subscripts: in `Nomenclature_Word.docx`, the symbols *c*ₚ, *D*ₕ and
> Δ*T*_LMTD use **true Word subscripts** (vertAlign), so "p", "h" and "LMTD"
> appear as proper lowered subscript text — the journal-standard look — and copy
> cleanly into the manuscript. In this markdown preview they are shown with an
> underscore (e.g. ΔT_LMTD) only because plain markdown has no subscript syntax.
