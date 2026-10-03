# Equations in Word Equation-Editor Form (UnicodeMath Linear Format)

**How to use:** In Microsoft Word, place the cursor where you want the equation,
press **Alt + =** (inserts an equation field), then **copy one line below and paste
it into the equation field** and press **Enter** (or Space). Word's equation editor
auto-converts the linear text into the professionally stacked/fraction form.

- The format used is **UnicodeMath** (Word's native linear math format).
- `/` builds a fraction, `^` a superscript, `_` a subscript, `√()` a radical.
- Greek names (`\rho`, `\phi`, `\mu`, `\varepsilon`, `\Delta`, `\Sigma`) auto-convert
  to the Greek symbol on the next space.
- Parentheses after a subscript/superscript group terms, e.g. `\rho_(nf)`.

> A ready-made Word file where every equation is already a live, editable Word
> equation object is also provided: **Equations_Word_Editor.docx**.

---

## Section 2.4 — Governing and property equations

**Eq. (1) — Nanofluid density**
```
\rho_nf=\phi \rho_p+(1-\phi) \rho_w
```

**Eq. (2) — Nanofluid heat capacity (volumetric)**
```
(\rho c_p )_nf=\phi (\rho c_p )_p+(1-\phi)(\rho c_p )_w
```

**Eq. (3) — Nanofluid specific heat**
```
c_(p,nf)=(\phi (\rho c_p )_p+(1-\phi)(\rho c_p )_w)/\rho_nf
```

**Eq. (4) — Nanofluid dynamic viscosity (Einstein)**
```
\mu_nf=(1+2.5\phi) \mu_w
```

**Eq. (5) — Nanofluid thermal conductivity (Maxwell)**
```
k_nf=((k_p+2k_w-2\phi(k_w-k_p))/(k_p+2k_w+\phi(k_w-k_p))) k_w
```

**Eq. (6) — Hybrid equivalent particle density**
```
\rho_p=x \rho_(Al₂O₃ )+(1-x) \rho_CuO
```

**Eq. (7) — Hybrid equivalent particle heat capacity**
```
(\rho c_p )_p=x (\rho c_p )_(Al₂O₃ )+(1-x)(\rho c_p )_CuO
```

**Eq. (8) — Hybrid equivalent particle conductivity**
```
k_p=x k_(Al₂O₃ )+(1-x) k_CuO
```

**Eq. (9) — Coolant mean velocity**
```
U=\dot(m)_nf/(\rho_nf A_c )
```

**Eq. (10) — Hydraulic diameter**
```
D_h=(4A_c)/P
```

**Eq. (11) — Reynolds number**
```
Re=(\rho_nf U D_h)/\mu_nf
```

**Eq. (12) — Prandtl number**
```
Pr=(\mu_nf c_(p,nf))/k_nf
```

**Eq. (13) — Coolant mass flow rate**
```
\dot(m)_nf=\rho_nf \dot(V)_nf
```

**Eq. (14) — Heat rejected (coolant side)**
```
Q_c=\dot(m)_nf c_(p,nf) (T_in-T_out )_nf
```

**Eq. (15) — Heat gained (air side)**
```
Q_a=\dot(m)_a c_(p,a) (T_out-T_in )_a
```

**Eq. (16) — Energy balance**
```
Q=Q_c≈Q_a
```

**Eq. (17) — Log-mean temperature difference**
```
\Delta T_LMTD=((T_s-T_(in,nf) )-(T_s-T_(out,nf) ))/ln⁡[(T_s-T_(in,nf) )/(T_s-T_(out,nf) )] 
```

**Eq. (18) — Coolant-side convective coefficient**
```
h=Q/(A_s \Delta T_LMTD )
```

**Eq. (19) — Nusselt number**
```
Nu=(h D_h)/k_nf
```

**Eq. (20) — Minimum heat-capacity rate**
```
C_min=(\dot(m) c_p )_min
```

**Eq. (21) — Maximum possible heat transfer**
```
Q_max=C_min (T_(in,c)-T_(in,a) )
```

**Eq. (22) — Radiator effectiveness**
```
\varepsilon=Q/Q_max 
```

**Eq. (23) — Power-law Nusselt correlation**
```
Nu=a Re^0.5 Pr^(1/3)
```

---

## Section 3.5 — Machine-learning performance metrics

**Eq. (24) — Pearson correlation coefficient**
```
r=cov(a,p)/√(cov(a,a) cov(p,p))
```

**Eq. (25) — Mean square error**
```
MSE=1/N \Sigma_(i=1)^N (a_i-p_i )^2 
```

**Eq. (26) — Root mean square error**
```
RMSE=√MSE
```

**Eq. (27) — Mean absolute error**
```
MAE=1/N \Sigma_(i=1)^N |a_i-p_i | 
```

---

### Tips if a line doesn't auto-format
- Make sure you are **inside an equation field** (Alt + =) before pasting — otherwise
  Word treats it as plain text.
- After pasting, press **Space** once at the end of the line to trigger the build-up.
- If a Greek backslash name stays as text, add a trailing space after it (e.g. type
  `\rho ` → ρ). You can also switch the field to **Professional** via the Equation
  Tools ▸ Design ▸ "Professional" button.
- `\dot(m)` renders an over-dot (ṁ); `_( ... )` and `^( ... )` group multi-character
  sub/superscripts.
