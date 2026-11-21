# Surgery-Triggered Recurrence of Dormant Satellite Melanoma and the Timing of Adjuvant Immune Stimulation: A Reaction–Diffusion Modelling Study

**[Author names]**

[Affiliations]

*Corresponding author: [e-mail]

---

## Abstract

Local recurrence of cutaneous melanoma after complete excision often arises from satellite micrometastases rather than from residual primary tumour. Eikenberry, Thalhauser and Kuang proposed that the immune response directed against a primary melanoma suppresses nearby satellites "in passing", and that removing the primary together with its immune infiltrate releases them. Here we use a reduced, radially symmetric version of their tumour–immune model to ask two follow-on questions: which satellites are released by surgery, and when should immune stimulation be given to prevent the resulting recurrence. The model tracks primary tumour cells, satellite cells, cytotoxic immune cells, tumour vasculature, and quasi-steady fields of immune-attracting factor and tumour angiogenic factor. With baseline parameters the primary reaches an immune-controlled steady state of radius 0.9 mm. A satellite seeded 1.1 mm beyond its edge stays at a stable, sub-detectable mass of 2.8 × 10⁻³ (dimensionless units) for more than three years if the primary is left in place. After resection with a 0.5 mm margin, the immune cell mass falls by 65% within 44 days, the satellite crosses the detection threshold 44 days after surgery, and it settles at a mass 18 times that of the original primary. Satellites are released only from a band about 0.6–1.6 mm beyond the primary edge; satellites farther away escape even with the primary present, and a margin of 1.75 mm removes every released satellite in this geometry. Short courses (30–120 days) of increased immune-cell recruitment given in the 80 days after surgery did not prevent recurrence, because dormant satellites are too small to activate immune cells. Courses given four or more months before surgery eliminated the primary tumour and released the satellite before surgery, as resection does. The same courses eradicated the recurrence when started 80–100 days or more after surgery, once the satellite burden had grown. Continuous post-operative stimulation at twice the baseline recruitment held the recurrence below detection. Relief of tumour-induced immune-cell killing alone was ineffective. The eradication result held for numerical extinction thresholds from 3 × 10⁻⁶ to 3 × 10⁻⁴ but failed at a threshold of 10⁻⁶ or below, which corresponds to fractions of a cell. These results suggest that, under the immune-disruption hypothesis, the benefit of adjuvant immune stimulation depends on antigen burden at the time of treatment, and that the immune state of the peritumoral tissue is as relevant to margin choice as the visible tumour edge.

**Keywords:** Melanoma; Satellite metastasis; Tumour dormancy; Surgical excision; Immunotherapy timing; Reaction–diffusion model; Tumour–immune interaction

---

## 1. Introduction

Cutaneous melanoma is usually treated by wide local excision of the primary lesion. Local and in-transit recurrence still occurs in a minority of patients, and a substantial fraction of these recurrences arise from satellite micrometastases in the surrounding skin rather than from incomplete removal of the primary tumour [1,2]. In some cases, recurrence appears soon after surgery in lesions that had been clinically silent. De Giorgi and colleagues described a patient whose slowly growing polypoid melanoma was excised and who then developed multiple satellite lesions within 5–7 cm of the scar within weeks [3]. Observations of this kind are part of a broader literature suggesting that removal of a primary tumour can accelerate the growth of dormant disseminated disease [4,5].

Several mechanisms have been proposed. Primary tumours can release systemic inhibitors of angiogenesis or growth, whose removal frees distant lesions [3,6]. Surgery and wound healing trigger a systemic inflammatory response that can promote outgrowth of immune-controlled tumours, as shown directly in mouse models by Krall and colleagues [7,8]. A third mechanism was proposed by Eikenberry, Thalhauser and Kuang (hereafter EKT) using a spatial partial differential equation model of melanoma invasion with a cellular immune response [9]. In their simulations, immune cells recruited by the primary tumour also suppressed nearby satellites. Excision removed the primary and most of these immune cells, and the satellites then grew to a total mass larger than the primary had reached.

The EKT model raises practical questions that the original paper did not address. First, which satellites are released by surgery, and how does this depend on the excision margin? Second, the EKT discussion pointed to adjuvant therapy scheduling as a natural use of the model [9]. Immune checkpoint inhibitors are now standard adjuvant treatment for resected high-risk melanoma [10,11], and neoadjuvant immunotherapy given while the tumour is still in place has shown higher pathological response rates and improved event-free survival compared with adjuvant-only treatment [12–14]. Preclinical work attributes the neoadjuvant advantage to stronger priming of tumour-specific T cells by antigen from the intact tumour [15]. A spatial model can ask a complementary question: if satellites are held dormant by the primary's immune infiltrate, when does a period of immune stimulation have a lasting effect?

We address these questions with a reduced version of the EKT model that keeps its central immune terms but simplifies its geometry and oxygen dynamics. We do not attempt quantitative prediction. Our aim is to identify which qualitative outcomes follow from the immune-disruption mechanism and how they depend on margin and treatment timing.

---

## 2. Methods

### 2.1 Model overview

We consider a radially symmetric domain 0 ≤ r ≤ R (mm) centred on the primary tumour, which represents a thin layer of skin viewed from above. Each point of the domain is assumed to lie above a dermal vascular bed from which immune cells can enter. This geometry keeps the EKT model's radial structure but collapses its vertical dimension. The depth-dependent oxygen field and the basement membrane are replaced by a vascular density e(r,t) that raises the local carrying capacity of the primary tumour. Densities are scaled by the tumour-cell carrying capacity K_C, so they are dimensionless. Time is in days.

The variables are primary tumour cells p, satellite cells s, cytotoxic immune cells m, tumour vasculature e (0 ≤ e ≤ 1), immune-attracting factor a, and tumour angiogenic factor v. The two soluble factors diffuse and decay far faster than cells move (their decay rates are 8 and 20 per day). We therefore treat them as quasi-steady and solve an elliptic problem for each at every time step.

### 2.2 Governing equations

With total tumour density T = p + s, the immune activation level and the per-cell kill rate follow the EKT formulation [9]:

Γ = T / (ξ + T),      k = (τ_c0 + τ_cA Γ) m / (λ_c + T)

The cell equations are:

∂p/∂t = D_c ∇·(p∇p) + r_c p (1 − T/K_p) − k p,      with K_p = K_0 + (1 − K_0) e

∂s/∂t = D_c ∇·(s∇s) + r_c s (1 − T/K_s) − k s

∂m/∂t = D_m ∇²m − χ ∇·(m∇a) + Q a/(a + φ_a) − β_K T m/(λ_m + m) − β_m m

∂e/∂t = D_e ∇²e + α_e [S(v)(1 − e) − (1 − S(v)) e],      with S(v) = 1/(1 + exp(−(v − V_T)/V_w))

The quasi-steady factor equations are:

0 = D_a ∇²a + γ_ac T + γ_am m Γ − β_a a

0 = D_v ∇²v + γ_v T + γ_vm m Γ − β_v v

Tumour motility uses the density-dependent (porous-medium) diffusion of EKT Eq. 1, which gives sharp tumour borders. The primary is confined to a low avascular capacity K_0 until vasculature forms. Satellites are assumed to lodge at the dermal vascular level, as in EKT, and so have a higher capacity K_s. Immune cells enter wherever immune-attracting factor is present, at a saturating rate Q a/(a + φ_a). This is the spatially distributed analogue of EKT's boundary influx from the vascular bed. They move by diffusion and chemotaxis and are killed in proportion to local tumour density, which represents the immunosuppressive microenvironment. The vascular switch S(v) replaces the EKT Heaviside thresholds with a smooth sigmoid. All boundaries have zero flux.

The kill term has an important property. When T is much smaller than ξ and λ_c, the per-cell kill rate is approximately (τ_c0 + τ_cA T/ξ) m/λ_c. Because activation grows with tumour density, very small lesions are only weakly attacked. Larger ones are attacked more strongly until the denominator λ_c + T saturates the effect. With inactivated cytotoxicity τ_c0 set an order of magnitude below the EKT upper bound, this allows a stable low-density equilibrium, which we interpret as immune-mediated dormancy [16,17].

### 2.3 Parameters

Parameters are listed in Table 1. Where EKT gave a dimensional value or range, we used it directly or scaled it by K_C (for half-saturation densities). Parameters without a direct empirical basis in the reduced geometry (K_0, K_s, χ, Q, β_K) were calibrated so that the baseline primary tumour reaches an immune-controlled steady state, as in EKT Fig. 7, rather than being destroyed or escaping. Without immune cells (Q = 0), the same primary vascularises and fills the 12 mm domain within about 400 days.

Table 1. Model parameters (densities scaled by K_C; lengths in mm; time in days).

| Symbol | Meaning | Value | Basis |
|---|---|---|---|
| r_c | Maximum tumour growth rate | 0.30 day⁻¹ | EKT range 0.17–0.69 |
| D_c | Density-dependent tumour motility | 0.01 mm² day⁻¹ | Calibrated |
| K_0 | Avascular carrying capacity of primary | 0.25 | Calibrated |
| K_s | Carrying capacity of dermal satellites | 0.5 | Assumed |
| D_m | Immune cell diffusion | 0.01 mm² day⁻¹ | EKT range 0.000864–0.071 |
| χ | Immune chemotaxis coefficient | 0.25 | Calibrated |
| Q | Maximum immune cell influx | 0.05 day⁻¹ | Calibrated |
| φ_a | Half-saturation of influx | 0.02 | Assumed |
| β_m | Immune cell turnover | 0.02 day⁻¹ | EKT range 0–0.05 |
| β_K | Tumour-induced immune cell death | 0.5 day⁻¹ | Calibrated |
| λ_m | Half-saturation of immune death | 0.01 | EKT 10²–10³ cells mm⁻³, scaled |
| τ_c0 | Kill rate, non-activated immune cell | 0.02 day⁻¹ | Below EKT bound of 0.218 |
| τ_cA | Additional kill rate, activated cell | 2.027 day⁻¹ | EKT |
| λ_c | Half-saturation of killing | 0.01 | EKT, scaled |
| ξ | Half-maximal activation density | 0.1 | EKT range, scaled |
| D_a, β_a | IAF diffusion and decay | 2.0 mm² day⁻¹, 8.0 day⁻¹ | EKT ranges |
| D_v, β_v | TAF diffusion and decay | 0.5 mm² day⁻¹, 20 day⁻¹ | EKT ranges |
| γ_ac, γ_am | IAF production by tumour, immune cells | 1.0, 1.0 | Scaling |
| γ_v, γ_vm | TAF production by tumour, immune cells | 20, 0 | Scaling; γ_vm studied in companion work |
| V_T, V_w | Angiogenic switch threshold and width | 0.5, 0.05 | Scaling |
| α_e, D_e | Vascular growth/regression rate, spread | 0.05 day⁻¹, 0.002 mm² day⁻¹ | Assumed |
| R, Δr, Δt | Domain radius, grid spacing, time step | 12 mm, 0.1 mm, 0.05 day | Numerical |

### 2.4 Numerical method

Equations are discretised with a conservative finite-volume scheme on a uniform radial grid. Diffusion and chemotaxis fluxes are evaluated at cell faces, and chemotaxis uses first-order upwinding. Cell equations are advanced with forward Euler. At every step, the two quasi-steady factor equations are solved exactly with a pre-factorised tridiagonal (Thomas) solver. Simulations run for 1500 days. The simulator is written in plain JavaScript (Node.js) without external libraries.

A continuum model can recover from densities that correspond to far less than one cell, which is a known artefact of deterministic population models [18]. We therefore set tumour densities below an extinction threshold of 10⁻⁵ to zero. As a reference point, assume K_C = 10⁵ cells mm⁻³ and a layer thickness of 0.1 mm. A grid ring at r = 2 mm then holds about 1.3 × 10⁴ cells at density 1, so the threshold corresponds to roughly 0.1 cell per ring. Section 3.5 tests the sensitivity of all conclusions to this threshold.

### 2.5 Experiments

The primary tumour starts as a disc of density 0.2 and radius 0.5 mm. In all experiments, a single satellite ring of density 0.002 is seeded at radius r on day 180. Because the domain is radially symmetric, a satellite is necessarily a ring, as in EKT. Surgery on day 540 sets every variable to zero for r < R_ex, where R_ex is the primary edge (outermost radius with p > 0.01) plus the margin. The baseline margin is 0.5 mm. A lesion is called detectable when its integrated mass ∫2πr s dr exceeds 0.1, about one quarter of the primary steady-state mass.

Immune stimulation is modelled in two ways. The first multiplies the recruitment rate Q by a factor F, representing therapies that increase immune-cell trafficking or expansion. The second multiplies the tumour-induced immune-cell killing rate β_K by a factor below one, representing relief of local immunosuppression in the spirit of checkpoint blockade. Each is applied for a window of D days starting at a chosen offset from surgery. Table 2 lists the experiments.

Table 2. Numerical experiments.

| Experiment | Varied quantities | Runs |
|---|---|---|
| Baseline resection | Surgery vs. no surgery vs. no immunity | 3 |
| Fate map | Seed radius 1.0–4.0 mm (step 0.1) × margin 0–3 mm (step 0.25) | 403 |
| Timing | 8 schedules × start offsets −240 to +360 days (step 20) | 248 |
| Continuous adjuvant | Q × 1.25, 1.5, 2, 3 from surgery onward | 4 |
| Robustness | 12 parameter or numerical variants × 4 scenarios | 52 |

---

## 3. Results

### 3.1 Resection releases an immune-suppressed satellite

With baseline parameters, the primary tumour stops growing within about 60 days. It reaches a steady state of mass 0.41 and edge radius 0.9 mm, surrounded by an immune infiltrate of mass 1.76 (Figure 1A). A satellite seeded at r = 2.0 mm (1.1 mm beyond the edge) on day 180 settles within days at a mass of 2.8 × 10⁻³, a factor of 35 below detection. If the primary is left in place, it stays at this mass to the end of the simulation, 1320 days after seeding.

Resection on day 540 removes all tissue within 1.4 mm of the centre, including the densest part of the immune infiltrate (Figure 1B). Immune cell mass falls from 1.76 to 1.33 immediately and continues to fall to a minimum of 0.61 on day 584, as immune-attracting factor decays. Released from immune control, the satellite grows with a doubling time of 8.3 days. It becomes detectable 44 days after surgery, exceeds the mass of the original primary by day 51, and settles at a new steady state of mass 7.49, 18 times the primary. Immune mass rises again in response, to 11.4, but this immune response now controls a much larger lesion. The sequence agrees with EKT Fig. 7: recurrence is faster than primary growth and ends at a larger tumour burden.

[Insert Figure 1 here]

Figure 1. Resection of an immune-controlled primary tumour releases a dormant satellite. (A) Integrated masses of the primary tumour, a satellite seeded at r = 2.0 mm on day 180, and immune cells; surgery (0.5 mm margin) on day 540. The dotted red curve shows the satellite when the primary is not removed. The grey dashed line marks the detection threshold. (B) Radial immune-cell density just before surgery (day 530) and 5, 30 and 60 days after it. The vertical lines mark the excision boundary (1.4 mm) and the satellite position.

Without immunity, the same primary vascularises, and by day 540 primary and satellite together occupy most of the domain (combined mass 212). The immune response is therefore responsible for both the controlled primary and the dormant satellite.

### 3.2 Only satellites within a band around the primary are released

The fate map in Figure 2A shows what happens to a satellite as a function of its seeding radius and the excision margin. Three regions appear. Satellites seeded at r ≥ 2.6 mm (1.7 mm or more beyond the primary edge) escape immune control and become detectable before surgery. They are outside the range of the primary's immune infiltrate, and no margin we tested (up to 3 mm) changes their fate. Satellites inside the excision boundary are removed. Between these regions lies the band of released satellites. These lesions are dormant while the primary is present and recur after surgery.

[Insert Figure 2 here]

Figure 2. Satellite fate depends on seeding radius and excision margin. (A) Outcome at day 1500 for a satellite seeded on day 180 at radius r (horizontal axis) with surgery on day 540 using the margin on the vertical axis. Red: escaped before surgery. Orange: dormant before surgery, recurrent after it. Green: no recurrence. (B) Days from surgery to detectable recurrence for released satellites, 0.5 mm margin.

The lower edge of the band has a feature that pure geometry does not explain. With a zero margin (cutting at the visible edge, R_ex = 0.9 mm), satellites at 1.0–1.4 mm do not recur. With a 0.25 mm margin, satellites at 1.1–1.4 mm do recur, although they lie outside both excision boundaries. The difference is the immune infiltrate. Cutting at the visible edge leaves the densest part of the peritumoral immune ring in place (Figure 1B). Those immune cells, together with the immune-attracting factor that the satellite itself produces, are enough to eliminate a satellite next to the scar. A slightly wider margin removes the infiltrate but not the satellite. Wider margins of 0.75–1.5 mm progressively remove the released band. A margin of 1.75 mm (R_ex = 2.65 mm) removes every satellite that would otherwise recur.

Recurrence after surgery is fast throughout the band: 12–63 days to detection across all margins, and 25–47 days for a 0.5 mm margin (Figure 2B). The time is shortest for the outermost satellites, which sit at the edge of immune control and are held at the highest dormant density.

### 3.3 Short immune-stimulation courses work only after the recurrence has grown

We next applied immune stimulation for a fixed window starting at different times relative to surgery (Figure 3A). Increasing recruitment 1.5- or 2-fold for 60 days never prevented recurrence, whenever it was given. A 3-fold increase for 60 days failed when started anywhere from 240 days before surgery to 80 days after it, but for two different reasons, described below. It eradicated the recurrence when started 100 days or more after surgery. The same threshold of 100 days applied to 30-day and 120-day courses. A 5-fold increase moved the threshold earlier, to 80 days. Reducing tumour-induced immune-cell death by 75% for 60 days, or by 90% for 120 days, never prevented recurrence. When given 80 days or more after surgery, it slightly increased the final recurrence mass (8.9–10.2 vs. 7.5). The model does not give a simple reason for this; we report it without a proposed mechanism.

[Insert Figure 3 here]

Figure 3. Timing of immune stimulation relative to surgery. (A) Outcome at day 1500 for eight schedules (rows: "Q xF Dd" multiplies recruitment by F for D days; "bK xF Dd" multiplies tumour-induced immune-cell death by F) as a function of the start day relative to surgery on day 540. Green: satellite eradicated. Orange: recurrence persists. (B) Satellite mass for no therapy and for 3-fold recruitment for 60 days starting 120 days before surgery, at surgery, and 120 days after surgery.

Figure 3B shows the two failure modes. Pre-operative courses act mainly on the primary. A 3-fold boost starting 120 days before surgery reduced the primary to 0.8% of its mass within 20 days. The primary's infiltrate then dissolved, and the satellite escaped 80–100 days after the course began, before the planned surgery. Courses started 160–240 days before surgery eliminated the primary completely, and by day 539 the satellite had already reached a mass of 6.9–7.6. Courses started 20–80 days before surgery left both lesions small at surgery, and the satellite recurred afterwards as in the untreated case. In this model, immunological elimination of the primary releases satellites in the same way as surgical removal.

Courses started at or soon after surgery act on a satellite that is still very small (mass 7 × 10⁻³ to 5 × 10⁻²). The maximum local activation level Γ was 0.02 at the start of a course given at surgery and only 0.2 when the course ended. The extra immune cells therefore killed slowly, and the satellite grew back once the course ended. By contrast, a course started 120 days after surgery acts on a recurrence of mass about 7, where the maximum Γ is 0.83. A 60-day boost then drove the lesion below the extinction threshold within 42 days. Among all eradicating schedules, the recurrence mass when treatment began was 5.0–7.6, far above the detection threshold of 0.1. A 3-fold boost failed at a starting mass of 5.0 and succeeded at 6.4, so the tipping burden lies between these values for that dose. In this model, a short course therefore succeeds only against a recurrence that has become detectable.

### 3.4 Continuous adjuvant stimulation holds the recurrence below detection

When recruitment was raised from the day of surgery onward and never withdrawn, the outcome depended on the dose (Figure 4). A 1.25-fold increase reduced the final recurrence mass from 7.5 to 3.4, and a 1.5-fold increase reduced it to 1.7. A 2-fold increase held the satellite at 0.073, and a 3-fold increase held it at 0.030. Both of these are below the detection threshold. None of these doses eradicated the satellite. Continuous stimulation instead re-creates the dormant state that the primary's infiltrate had maintained, and the lesion remains vulnerable to withdrawal of therapy.

[Insert Figure 4 here]

Figure 4. Continuous post-operative stimulation. Satellite mass after surgery on day 540 with recruitment raised by the indicated factor from surgery onward, compared with no adjuvant therapy.

### 3.5 Robustness

Table 3 lists the four headline outcomes under parameter and numerical variants: dormancy with the primary in place, recurrence after surgery, failure of a 3-fold boost at surgery, and success of a 3-fold boost 120 days later. Dormancy, recurrence and the failure of the boost at surgery held in every variant except an extinction threshold of 10⁻⁷. At that threshold, sub-cellular tails of the satellite spread beyond the immune infiltrate and escape before surgery. Recurrence time (29–50 days when it occurred) and the failure of the early boost were insensitive to growth rate, immune motility, chemotaxis, grid spacing and time step. Recurrence mass varied 9-fold (5.0 to 45.2) and was most sensitive to immune-cell diffusion.

The success of the late boost was less robust. It held for extinction thresholds from 3 × 10⁻⁶ to 3 × 10⁻⁴ and for every other variant except reduced immunosuppression (β_K = 0.4). It failed at a threshold of 10⁻⁶, where the trough after treatment reached a mass of about 10⁻⁵ but was not counted as extinct. Under the reference conversion in Section 2.4, a mass of 10⁻⁵ is about 0.1 cell. Eradication by a late boost therefore means that the trough falls below one cell. A stochastic model would turn this into a probability of eradication rather than a certainty.

Table 3. Robustness of the main outcomes. "Dormant" is the satellite mass before surgery; "recurrence" is the final satellite mass after surgery and the number of days to detection; the boost columns give the final satellite mass after a 3-fold, 60-day recruitment boost started at surgery or 120 days after it (0 = eradicated).

| Variant | Dormant | Recurrence (days) | Boost at surgery | Boost at +120 d |
|---|---|---|---|---|
| Baseline | 2.8e-3 | 7.49 (44) | 7.07 | 0 |
| Extinction threshold 1e-7 | 9.67 (escaped) | 9.65 (0) | 10.0 | 10.0 |
| Extinction threshold 1e-6 | 2.8e-3 | 7.49 (42) | 7.85 | 7.85 |
| Extinction threshold 3e-6 | 2.8e-3 | 7.49 | n.d. | 0 |
| Extinction threshold 3e-5 | 2.9e-3 | 7.49 | n.d. | 0 |
| Extinction threshold 1e-4 | 2.9e-3 | 7.48 | n.d. | 0 |
| Extinction threshold 3e-4 | 4.1e-3 | 7.04 | n.d. | 0 |
| r_c 0.25 | 4.9e-3 | 5.98 (43) | 5.98 | 0 |
| r_c 0.35 | 2.4e-3 | 14.4 (42) | 14.4 | 0 |
| D_m 0.005 | 3.8e-3 | 4.96 (45) | 4.96 | 0 |
| D_m 0.02 | 2.2e-3 | 45.2 (41) | 43.8 | 0 |
| χ 0.15 | 2.6e-3 | 8.33 (45) | 8.33 | 0 |
| χ 0.35 | 4.1e-3 | 7.03 (41) | 7.03 | 0 |
| β_K 0.4 | 1.3e-2 | 4.20 (29) | 4.20 | 4.40 |
| β_K 0.6 | 1.1e-3 | 32.2 (50) | 32.0 | 0 |
| Δt 0.025 day | 2.8e-3 | 7.49 (45) | 7.07 | 0 |
| Δr 0.05 mm | 1.4e-3 | 12.1 (50) | 12.3 | 0 |

n.d., not determined.

---

## 4. Discussion

We used a reduced version of the EKT tumour–immune model to study the immune-disruption mechanism of post-surgical melanoma recurrence. The model reproduces the core EKT result: a primary tumour held at steady state by its immune infiltrate also keeps a nearby satellite dormant, and resection releases the satellite into rapid growth to a larger burden [9]. We add three observations.

First, release by surgery is spatially selective. Only satellites within a band about 0.6–1.6 mm beyond the primary edge are released. Closer satellites are removed with the primary or eliminated by the infiltrate that remains next to the scar. Farther satellites are never controlled. The band is set by how far the immune infiltrate reaches, not by the visible tumour edge. A margin that removes the infiltrate but not the satellites beside it is the worst choice in the model, because it creates released satellites that a narrower cut would have left under control. The absolute distances are tied to our calibrated millimetre-scale domain and should not be read as clinical margins. Clinical margins are 1–2 cm and are set by trial evidence on survival and local control [19–21]. The qualitative point is that, if immune disruption contributes to satellite recurrence, the reach of peritumoral immunity is a relevant length scale for margin selection.

Second, short courses of immune stimulation have a lasting effect only when tumour burden is high enough to activate immune cells. Pre-operative courses strong enough to eliminate the primary released the satellite before surgery, which shows that the release mechanism depends on removing the primary's immune infiltrate, not on surgery itself. This follows from the EKT activation term: killing efficiency rises with local tumour density, so a dormant satellite of mass 10⁻³ is largely ignored even when many immune cells are present. Clinical neoadjuvant immunotherapy studies point the other way: treatment before surgery outperforms treatment after it [12–15]. These two findings do not conflict, because they concern different mechanisms. The neoadjuvant benefit is thought to come from priming and expansion of tumour-specific T-cell clones by antigen from the intact primary, and that systemic memory then acts on micrometastases [15]. Our model has no adaptive memory. Immune cells respond only to local antigen and are lost when stimulation stops. The model result should be read as a statement about local innate-like control. A stimulus that depends on local activation has a lasting effect only when there is enough local antigen, and dormant satellites provide too little. Adding a primed, antigen-specific memory compartment would be the natural next step and could reconcile the two pictures.

Third, continuous post-operative stimulation at twice the baseline recruitment held recurrence below detection but did not eradicate it. In the model, adjuvant therapy restores the control that the primary's infiltrate had provided. Recurrence after withdrawal of adjuvant therapy is then expected, and our model predicts it. This is consistent with continued relapse risk after one year of adjuvant checkpoint inhibition in resected melanoma [10,11], although many other factors contribute in patients.

Reducing tumour-induced immune-cell killing alone was ineffective in all schedules. In this model, immunosuppression limits the immune response mainly inside large tumours. Dormant satellites and small recurrences are limited instead by low activation, which this intervention does not change. This result is specific to how immunosuppression is represented (a density-dependent death term, as in EKT) and should not be read as a statement about checkpoint inhibitors, whose main effects are on T-cell priming and exhaustion.

### 4.1 Limitations

The model is a strong simplification of EKT. It has no vertical dimension, basement membrane, oxygen field or necrotic debris, and the vascular switch only raises the primary's carrying capacity. Several key parameters were calibrated to reproduce an immune-controlled primary rather than measured, and masses are dimensionless. The satellite is a ring because of radial symmetry. This is a worst case, as EKT noted, but it means that the immune response to a satellite is shared around a circle. Surgery is instantaneous and has no wound-healing or systemic inflammatory response, although Krall and colleagues showed that this response can by itself release immune-controlled tumours [7]. The immune compartment has no adaptive memory. Finally, eradication depends on sub-detectable populations becoming extinct, which a deterministic model can only approximate with a threshold. Our robustness analysis shows that the late-boost result depends on this approximation below about 3 × 10⁻⁶, which corresponds to a small fraction of a cell. A stochastic, individual-based treatment of small lesions is needed to turn eradication into a probability.

### 4.2 Conclusions

In a reduced EKT model, surgery releases only satellites in a band set by the reach of the peritumoral immune infiltrate. Short courses of immune stimulation have a lasting effect only once a recurrence has grown large enough to activate immune cells, and continuous stimulation restores dormancy without cure. Spatial models can therefore separate the local immune effects of surgery from systemic priming effects. Testing the timing prediction would require models or experiments that also include adaptive immune memory.

---

## Data and Code Availability

All simulation code, the experiment driver, analysis scripts and raw results are in the `melanoma_articles/` directory of this repository (`melanoma_sim.js`, `run_experiments.js`, `analyze.py`, `make_figures.py`, `results/`). Running `node run_experiments.js a1` followed by `python3 make_figures.py` regenerates every figure.

## Competing Interests

The authors declare no competing interests.

---

## References

[1] MacCormack MA, Cohen LM, Rogers GS. Local melanoma recurrence: a clarification of terminology. Dermatol Surg. 2004;30(12):1533–1538.

[2] Read RL, Haydu L, Saw RPM, Quinn MJ, Shannon K, Spillane AJ, et al. In-transit melanoma metastases: incidence, prognosis, and the role of lymphadenectomy. Ann Surg Oncol. 2015;22(2):475–481.

[3] De Giorgi V, Massai D, Gerlini G, Mannone F, Quercioli E, Carli P. Immediate local and regional recurrence after the excision of a polypoid melanoma: tumor dormancy or tumor activation? Dermatol Surg. 2003;29(6):664–667.

[4] Demicheli R, Retsky MW, Hrushesky WJM, Baum M, Gukas ID. The effects of surgery on tumor growth: a century of investigations. Ann Oncol. 2008;19(11):1821–1828.

[5] Retsky MW, Demicheli R, Hrushesky WJM, Baum M, Gukas ID. Dormancy and surgery-driven escape from dormancy help explain some clinical features of breast cancer. APMIS. 2008;116(7–8):730–741.

[6] Boushaba K, Levine H, Nilsen-Hamilton M. A mathematical model for the regulation of tumor dormancy based on enzyme kinetics. Bull Math Biol. 2006;68(7):1495–1526.

[7] Krall JA, Reinhardt F, Mercury OA, Pattabiraman DR, Brooks MW, Dougan M, et al. The systemic response to surgery triggers the outgrowth of distant immune-controlled tumors in mouse models of dormancy. Sci Transl Med. 2018;10(436):eaan3464.

[8] Ceelen W, Pattyn P, Mareel M. Surgery, wound healing, and metastasis: recent insights and clinical implications. Crit Rev Oncol Hematol. 2014;89(1):16–26.

[9] Eikenberry S, Thalhauser C, Kuang Y. Tumor-immune interaction, surgical treatment, and cancer recurrence in a mathematical model of melanoma. PLoS Comput Biol. 2009;5(4):e1000362.

[10] Weber J, Mandala M, Del Vecchio M, Gogas HJ, Arance AM, Cowey CL, et al. Adjuvant nivolumab versus ipilimumab in resected stage III or IV melanoma. N Engl J Med. 2017;377(19):1824–1835.

[11] Eggermont AMM, Blank CU, Mandala M, Long GV, Atkinson V, Dalle S, et al. Adjuvant pembrolizumab versus placebo in resected stage III melanoma. N Engl J Med. 2018;378(19):1789–1801.

[12] Amaria RN, Reddy SM, Tawbi HA, Davies MA, Ross MI, Glitza IC, et al. Neoadjuvant immune checkpoint blockade in high-risk resectable melanoma. Nat Med. 2018;24(11):1649–1654.

[13] Blank CU, Rozeman EA, Fanchi LF, Sikorska K, van de Wiel B, Kvistborg P, et al. Neoadjuvant versus adjuvant ipilimumab plus nivolumab in macroscopic stage III melanoma. Nat Med. 2018;24(11):1655–1661.

[14] Patel SP, Othus M, Chen Y, Wright GP Jr, Yost KJ, Hyngstrom JR, et al. Neoadjuvant–adjuvant or adjuvant-only pembrolizumab in advanced melanoma. N Engl J Med. 2023;388(9):813–823.

[15] Liu J, Blake SJ, Yong MCR, Harjunpää H, Ngiow SF, Takeda K, et al. Improved efficacy of neoadjuvant compared to adjuvant immunotherapy to eradicate metastatic disease. Cancer Discov. 2016;6(12):1382–1399.

[16] Koebel CM, Vermi W, Swann JB, Zerafa N, Rodig SJ, Old LJ, et al. Adaptive immunity maintains occult cancer in an equilibrium state. Nature. 2007;450(7171):903–907.

[17] Dunn GP, Old LJ, Schreiber RD. The three Es of cancer immunoediting. Annu Rev Immunol. 2004;22:329–360.

[18] Mollison D. Dependence of epidemic and population velocities on basic parameters. Math Biosci. 1991;107(2):255–287.

[19] Thomas JM, Newton-Bishop J, A'Hern R, Coombes G, Timmons M, Evans J, et al. Excision margins in high-risk malignant melanoma. N Engl J Med. 2004;350(8):757–766.

[20] Hayes AJ, Maynard L, Coombes G, Newton-Bishop J, Timmons M, Cook M, et al. Wide versus narrow excision margins for high-risk, primary cutaneous melanomas: long-term follow-up of survival in a randomised trial. Lancet Oncol. 2016;17(2):184–192.

[21] Swetter SM, Tsao H, Bichakjian CK, Curiel-Lewandrowski C, Elder DE, Gershenwald JE, et al. Guidelines of care for the management of primary cutaneous melanoma. J Am Acad Dermatol. 2019;80(1):208–250.
