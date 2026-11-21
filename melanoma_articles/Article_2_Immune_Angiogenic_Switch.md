# Immune-Derived Angiogenic Signalling Sets the Duration of Melanoma Dormancy: Bottleneck Dynamics, Phase Structure and Anti-VEGF Scheduling in a Tumour–Immune Model

**[Author names]**

[Affiliations]

*Corresponding author: [e-mail]

---

## Abstract

Tumour-associated macrophages and other activated immune cells secrete VEGF and related angiogenic factors. In the melanoma model of Eikenberry, Thalhauser and Kuang, this immune-derived angiogenic signal produced a two-phase pattern: an epidermal tumour held at a steady state for about 300 days, followed by angiogenesis and aggressive invasion. We studied this phenomenon systematically in a reduced, radially symmetric version of that model. The production rate of tumour angiogenic factor (TAF) by activated immune cells, γ_vm, was the control parameter. Without immune TAF, the primary tumour stayed at an avascular steady state indefinitely. Above a critical value γ_vm,c ≈ 883 (in scaled units), the tumour went through a dormant phase and then underwent an angiogenic switch. The duration of dormancy diverged as γ_vm approached the critical value from above. It ranged from 72 days at γ_vm = 1283 to 2762 days at γ_vm = 883.6, and fitted a power law with exponent −0.50. This is the scaling expected when a stable state has just disappeared in a saddle-node bifurcation. In this regime, long dormancy does not require a slow biological process: it arises from slow passage through a state that no longer exists. Phase diagrams over immune recruitment and immune TAF production showed that immune TAF shrinks the region of immune control. The minimum immune recruitment for avascular control rose from Q = 0.04 without immune TAF to 0.09 at γ_vm = 900 and 0.12 at γ_vm = 1600. A strongly recruited immune response could also hold a vascularised tumour at small size. Neutralising 50% of bioavailable TAF continuously from the start prevented the switch. A 180-day course delayed it by 124–150 days, and a course given during dormancy delayed it by 330–350 days. Continuous neutralisation of 50% or more, started after the switch, reverted established vascularised tumours to the avascular controlled state. These results identify immune-derived TAF as a parameter that sets dormancy duration and suggest that anti-angiogenic therapy acts in this model by restoring the immune-controlled state.

**Keywords:** Melanoma; Angiogenic switch; Tumour dormancy; Tumour-associated macrophages; VEGF; Saddle-node bifurcation; Anti-angiogenic therapy

---

## 1. Introduction

Most solid tumours can grow to only about 1–2 mm without new blood vessels. The transition from an avascular, slowly growing lesion to a vascularised, invasive one is called the angiogenic switch [1,2]. In cutaneous melanoma the switch is closely associated with the change from radial to vertical growth [3,4]. Experiments in human melanoma xenografts showed that constitutive VEGF expression matters more than hypoxia-induced VEGF up-regulation [5]. Eikenberry, Thalhauser and Kuang (hereafter EKT) reproduced this result in a spatial model of melanoma invasion [6].

Tumour cells are not the only source of angiogenic factors. Tumour-associated macrophages produce VEGF, bFGF, TNF-α and IL-8 [7,8]. In a mouse model of breast cancer, macrophage infiltration regulated the timing of the angiogenic switch [9]. Nesbit and colleagues showed that low-level MCP-1 expression by melanoma cells attracted macrophages that promoted tumour formation, while high expression led to tumour destruction [10]. The immune response can therefore act on both sides. EKT included this effect by letting activated immune cells produce tumour angiogenic factor (TAF) at a rate γ_vm. In one simulation they observed an immune-controlled steady state lasting about 300 days, followed by immune-induced angiogenesis and unchecked growth (EKT Fig. 6) [6].

Long periods of tumour dormancy followed by sudden progression are common clinically. Mathematical models have attributed dormancy to angiogenic balance [11], immune equilibrium [12,13] and cell kinetics [14]. EKT reported the two-phase pattern for a single parameter set and did not examine what determines the length of the dormant phase, how the pattern depends on the strength of the immune response, or how it responds to anti-angiogenic therapy. We address these questions here with a reduced version of the EKT model. Anti-angiogenic therapy has had limited success in melanoma. Bevacizumab added to chemotherapy did not significantly improve progression-free survival in advanced melanoma [15], and adjuvant bevacizumab did not improve overall survival in high-risk resected melanoma [16]. A model that separates tumour-derived from immune-derived angiogenic signals may help explain when such therapy can be effective.

---

## 2. Methods

### 2.1 Model

We use the reduced EKT model described in full in a companion study (Article 1 of this series). The domain is radially symmetric, 0 ≤ r ≤ 12 mm, and represents a thin skin layer above a dermal vascular bed. The variables are tumour cell density p, cytotoxic immune cell density m, vascular density e (0 ≤ e ≤ 1), and quasi-steady fields of immune-attracting factor a and TAF v. All densities are scaled by the tumour carrying capacity K_C. No satellites are seeded in this study. With T = p, Γ = T/(ξ + T) and k = (τ_c0 + τ_cA Γ) m/(λ_c + T):

∂p/∂t = D_c ∇·(p∇p) + r_c p (1 − p/K_p) − k p,      K_p = K_0 + (1 − K_0) e

∂m/∂t = D_m ∇²m − χ ∇·(m∇a) + Q a/(a + φ_a) − β_K p m/(λ_m + m) − β_m m

∂e/∂t = D_e ∇²e + α_e [S(v)(1 − e) − (1 − S(v)) e],      S(v) = 1/(1 + exp(−(v − V_T)/V_w))

0 = D_a ∇²a + γ_ac p + γ_am m Γ − β_a a

0 = f(t) · [solution of 0 = D_v ∇²v + γ_v p + γ_vm m Γ − β_v v]

Here f(t) ≤ 1 is the fraction of TAF left bioavailable by anti-VEGF therapy (f = 1 without therapy). The tumour's carrying capacity rises from the avascular value K_0 = 0.25 to 1 as vasculature forms. This stands in for the release from oxygen limitation and the penetration of the basement membrane that EKT model explicitly. Vasculature grows when TAF exceeds the threshold V_T = 0.5 and regresses when it falls below, following EKT's assumption that endothelial cells undergo apoptosis when VEGF is low [6].

Parameters are as in Table 1 of Article 1, with r_c = 0.30 day⁻¹, K_0 = 0.25, D_m = 0.01 mm² day⁻¹, Q = 0.05 day⁻¹, τ_c0 = 0.02 day⁻¹, τ_cA = 2.027 day⁻¹, ξ = 0.1, D_v = 0.5 mm² day⁻¹, β_v = 20 day⁻¹, constitutive TAF production γ_v = 20, V_T = 0.5, V_w = 0.05 and α_e = 0.05 day⁻¹. The immune TAF production rate γ_vm, the immune influx Q and the constitutive rate γ_v are varied. In the reduced model, γ_vm has units of scaled TAF per immune cell per day. Its magnitude relative to γ_v reflects the fact that immune cells sit at lower density than tumour cells and mostly at the tumour margin, where activation Γ is lower.

### 2.2 Numerics and outcome measures

The numerical scheme is as in Article 1: a finite-volume grid with Δr = 0.1 mm, forward Euler with Δt = 0.05 day, and exact tridiagonal solves for the quasi-steady fields. The tumour starts as a disc of density 0.2 and radius 0.5 mm. The angiogenic switch time is the first day on which the integrated vascular mass ∫2πr e dr exceeds 1. In the controlled avascular state this mass is about 0.02, and after a switch it approaches the domain total of 452. At day 1500 each run is classified as one of the following:
- eradicated (tumour mass below 10⁻³);
- controlled, avascular (no switch, mass below 2);
- avascular escape (no switch, mass at least 2);
- vascularised, controlled (switch, mass below 2);
- angiogenic escape (switch, mass at least 2).

The critical value γ_vm,c was located by bisection to a precision of 0.05, using runs of 4000 days.

### 2.3 Experiments

1. Time courses for γ_vm = 0, 900, 1000 and 1500 over 2000 days, with radial profiles at selected times for γ_vm = 900.
2. Dormancy duration for γ_vm = γ_vm,c + Δ, with Δ from 0.2 to 400.
3. Phase diagrams over Q ∈ [0.03, 0.15] (13 values) and γ_vm ∈ [0, 1600] (17 values), for γ_v = 20 and γ_v = 15 (442 runs).
4. Anti-VEGF therapy for γ_vm = 900, 1000 and 1500, with f ∈ {0.9, 0.7, 0.5, 0.3} and five schedules: continuous from day 0; days 0–180; days 200–380; continuous from day 200; and continuous from 30 days after the untreated switch time, which we call "from detection" (72 runs plus controls).

---

## 3. Results

### 3.1 Immune-derived TAF produces two-phase growth

Without immune TAF (γ_vm = 0), the tumour reached a steady mass of 0.41 within about 100 days and stayed there for the whole 2000-day simulation (Figure 1A). Peak TAF in this state was 0.23, less than half the angiogenic threshold. Values of γ_vm up to 800 changed the steady mass by less than 12%. At γ_vm = 900 the tumour reached a quasi-steady mass of about 0.5, which drifted upward slowly over 400 days. The angiogenic switch occurred on day 420. Tumour mass then rose from 0.75 on day 400 to 12.4 on day 600 and 387 on day 2000 (Figure 1B). Immune cell mass rose at the same time, from 2.2 on day 300 to 9.3 on day 600, but did not control the vascularised tumour. At γ_vm = 1000 and 1500, the switch came on days 143 and 54, and the dormant phase became short or absent.

[Insert Figure 1 here]

Figure 1. Immune-derived TAF produces two-phase growth. (A) Primary tumour mass for four values of the immune TAF production rate γ_vm. (B) Tumour, immune-cell and vascular masses for γ_vm = 900; the dashed line marks the angiogenic switch (vascular mass greater than 1) on day 420.

The radial profiles show how the switch happens (Figure 2). On day 300, peak TAF was 0.43, below the threshold of 0.5, and vascular density was below 0.1. Peak TAF reached 0.77 on day 450 and 1.04 on day 520. Vascular density reached 0.99 by day 520, raising the local carrying capacity, and peak tumour density rose from 0.30 on day 300 to 0.98 on day 520. A positive feedback loop drives the switch. Vasculature allows a denser tumour. A denser tumour produces more TAF and activates more immune cells, which produce more TAF.

[Insert Figure 2 here]

Figure 2. Radial structure of the angiogenic switch at γ_vm = 900. (A) TAF profiles on days 300, 450, 520 and 600, with the switch threshold V_T. (B) Tumour density (solid) and vascular density (dashed) on the same days.

### 3.2 Dormancy duration diverges at a critical immune TAF production rate

Bisection placed the critical value between γ_vm = 883.32 and 883.36. Below it, the tumour stayed avascular for 4000 days. Above it, the time to the switch fell steeply with distance from the critical value (Figure 3): 2762 days at Δ = 0.22, 1207 days at Δ = 2.0, 380 days at Δ = 20 and 72 days at Δ = 400. A log–log regression over all 11 points gave a slope of −0.50. Over the six points closest to the critical value, the slope was −0.43, which is slightly shallower because the switch time includes a fixed delay after the vascular threshold is crossed.

[Insert Figure 3 here]

Figure 3. Time to the angiogenic switch as a function of distance from the critical immune TAF production rate, γ_vm − γ_vm,c, on log–log axes. The dashed line has slope −1/2.

An exponent of −1/2 is the signature of a saddle-node bifurcation [17]. For γ_vm below the critical value, the controlled avascular state is a stable equilibrium. At the critical value it merges with an unstable equilibrium and disappears. Just above it, the system still passes slowly through the region where the equilibrium used to be, and the passage time scales as (γ_vm − γ_vm,c)^(−1/2). In the model, therefore, a dormant phase of hundreds to thousands of days does not need a slow underlying process such as gradual mutation or slow immune exhaustion. It arises when a parameter sits just past the point where a stable state disappears. Small differences in immune TAF production between patients or lesions would then produce very large differences in dormancy duration.

### 3.3 Immune TAF shrinks the region of immune control

Figure 4A shows outcomes over immune recruitment Q and immune TAF production γ_vm with baseline constitutive TAF (γ_v = 20). At the weakest recruitment, Q = 0.03, the tumour escaped through angiogenesis at every γ_vm. For γ_vm ≤ 600, any Q ≥ 0.04 controlled the tumour in the avascular state. At Q = 0.04 and γ_vm = 700–800, the tumour escaped without vasculature. From γ_vm = 900 upward, a region of angiogenic escape appeared for Q = 0.03–0.06. Next to it was a region in which the tumour vascularised but stayed small (mass below 2). This region covered Q = 0.07–0.08 at γ_vm = 900 and widened to Q = 0.07–0.11 at γ_vm = 1400–1600. Only higher recruitment kept the tumour avascular. The minimum Q for avascular control was 0.04 for γ_vm ≤ 600, 0.05 at 700–800, 0.09 at 900, 0.10 at 1000–1100, 0.11 at 1200–1300 and 0.12 at 1400–1600. No combination in this range led to eradication within 1500 days.

[Insert Figure 4 here]

Figure 4. Outcome at day 1500 over immune influx Q and immune TAF production γ_vm. (A) Constitutive TAF production γ_v = 20. (B) γ_v = 15. Categories are defined in Section 2.2.

Immune recruitment therefore does two things that oppose each other. More immune cells mean more immune TAF. But stronger recruitment also holds the tumour at a lower density, which lowers both tumour-derived TAF and the activation Γ that drives immune TAF production. Across the range we tested, the second effect dominated, and stronger recruitment never made outcomes worse at fixed γ_vm. Immune TAF instead raises the level of recruitment needed for avascular control.

With weaker constitutive TAF (γ_v = 15, Figure 4B), angiogenic escape needed more immune TAF. At Q = 0.05, the onset moved from γ_vm = 900 to about 1100. At the weakest recruitment (Q = 0.03), the tumour escaped without vasculature for γ_vm ≤ 600, growing laterally at the avascular capacity. Constitutive and immune-derived TAF add together in the model. A tumour line with low constitutive VEGF expression, which EKT and Danielsen and Rofstad found to be insufficient for angiogenesis on its own [5,6], can still switch when immune TAF supplies the shortfall.

The vascularised-but-controlled state is notable. In this state the angiogenic switch has occurred, yet strong immune recruitment holds the tumour at a mass close to the avascular steady state. Under the model's assumptions, vascularisation alone does not imply progression when immune pressure is high.

### 3.4 Anti-VEGF therapy delays, prevents, or reverses the switch

Figure 5 shows tumour mass under five anti-VEGF schedules with 50% TAF neutralisation (f = 0.5). Table 1 summarises all doses.

[Insert Figure 5 here]

Figure 5. Anti-VEGF schedules with 50% of TAF neutralised. (A) γ_vm = 900 (untreated switch on day 420). (B) γ_vm = 1000 (untreated switch on day 143). "From detection" starts 30 days after the untreated switch.

Table 1. Effect of anti-VEGF schedules. Entries are the angiogenic switch day (or "none") and, in parentheses, tumour mass on day 2000. Untreated values: γ_vm = 900, switch day 420 (387); γ_vm = 1000, day 143 (449); γ_vm = 1500, day 54 (449). f is the fraction of TAF left bioavailable.

| Schedule | γ_vm 900, f 0.5 | γ_vm 1000, f 0.5 | γ_vm 1500, f 0.5 | γ_vm 1500, f 0.9 |
|---|---|---|---|---|
| Continuous from day 0 | none (0.41) | none (0.41) | none (0.42) | 76 (449) |
| Days 0–180 | 566 (339) | 288 (449) | 203 (449) | 76 (449) |
| Days 200–380 | 767 (260) | 143 (381) | 54 (449) | 54 (449) |
| Continuous from day 200 | none (0.41) | 143 (0.42) | 54 (0.47) | 54 (449) |
| From detection, continuous | 420 (0.34) | 143 (0.41) | 54 (0.42) | 54 (449) |

Continuous neutralisation from day 0 prevented the switch for every γ_vm tested with f ≤ 0.7. For γ_vm = 900 and 1000 it also worked at f = 0.9, but at γ_vm = 1500 the 10% dose only delayed the switch from day 54 to day 76. A 180-day course from day 0 delayed the switch by 124–147 days for γ_vm = 900 and 1000, and by 144–150 days for γ_vm = 1500 at f ≤ 0.7. The tumour then progressed as in the untreated case. Results were almost independent of dose between f = 0.7 and f = 0.3, because any dose that pushes TAF below the threshold has the same effect on vascular growth. For γ_vm = 900, a course during the dormant phase (days 200–380) delayed the switch by 327–348 days, to day 747–768. This is longer than the 180 days of treatment. We interpret this as the course pushing the system back from the edge of the bottleneck, so that the slow region had to be traversed again.

Continuous neutralisation started after the switch reverted established vascularised tumours to the avascular controlled state. With f ≤ 0.5, tumour mass returned to 0.34–0.47 by day 2000 for all three γ_vm values. At f = 0.7, reversion occurred for γ_vm = 900 but not for γ_vm = 1000 or 1500. At f = 0.9 it never occurred. Reversion requires a dose large enough to hold TAF below the threshold despite the higher tumour density and immune activation of the vascularised state. This is higher than the dose needed for prevention, which reflects the hysteresis of the positive feedback loop.

---

## 4. Discussion

We studied the two-phase growth pattern that EKT attributed to angiogenic factors released by activated immune cells [6]. In a reduced version of their model, the pattern comes from a saddle-node bifurcation. The duration of dormancy is controlled by how far immune TAF production lies above a critical value, with the scaling exponent of −1/2 expected for this bifurcation. A slow passage near a vanished equilibrium is a general mechanism for long transients in nonlinear systems [17]. To our knowledge it has not previously been proposed as the source of immune-associated angiogenic dormancy in melanoma models. It has a practical implication. Near the critical point, dormancy duration is extremely sensitive to parameters, so similar tumours could remain dormant for very different times, and their dormancy durations would vary widely.

The phase diagrams clarify the dual role of the immune response that EKT and Nesbit and colleagues described [6,10]. In our model, stronger immune recruitment does not make outcomes worse at fixed immune TAF production. Immune TAF raises the recruitment level needed for avascular control and opens a band of intermediate recruitment where the tumour escapes. The model therefore suggests that the clinical effect of macrophage infiltration depends on the ratio of their cytotoxic to their angiogenic output rather than on their number alone, consistent with the view that macrophage phenotype determines whether infiltration is protective [7,8]. We also found a vascularised but immune-controlled state, which suggests that vascularisation and progression can be separated when immune pressure is high.

The anti-VEGF simulations give three predictions. First, prevention needs only modest neutralisation if it is continuous, and dormancy-phase treatment buys more time than the same treatment given earlier. The reason is that treatment pushes the system back from the bottleneck, which the tumour must then traverse again. Second, finite courses only delay the switch, consistent with the absence of a durable survival benefit from anti-angiogenic therapy in melanoma trials [15,16]. Third, continuous high-dose neutralisation can revert vascularised tumours to the controlled avascular state, because vascular regression lowers tumour density and immune activation together. This reversion depends on the model's assumptions that vasculature regresses completely when TAF is withdrawn and that the immune response remains intact. Experimental anti-angiogenic therapy has instead shown evasive resistance, increased invasiveness and accelerated metastasis [18–20], none of which our model includes. Vascular normalisation, which may improve immune-cell delivery [21,22], is also absent. Adding these mechanisms would test whether the reversion prediction survives.

### 4.1 Limitations

The model shares the limitations of the reduced EKT framework described in Article 1. These include the absence of an explicit oxygen field, basement membrane, necrosis and vertical geometry, the use of dimensionless densities, and calibrated values for several immune parameters. The critical value γ_vm,c ≈ 883 is specific to these calibrated values and has no direct experimental counterpart. The exponent of −1/2, the existence of a critical value and the qualitative phase structure are the robust results. Anti-VEGF therapy is modelled as a uniform fractional reduction of bioavailable TAF with no pharmacokinetics, no effect on immune cells and no resistance. All immune cells are lumped into one population, so the model cannot separate angiogenic M2-like macrophages from cytotoxic cells.

### 4.2 Conclusions

In a reduced EKT model, immune-derived angiogenic factor sets the duration of melanoma dormancy through a saddle-node bottleneck, raises the immune recruitment needed for avascular control, and creates a vascularised but controlled state. Continuous anti-VEGF therapy prevents the switch at modest doses and reverses it at higher doses. Finite courses only delay it, and a course given during dormancy delays it longest.

---

## Data and Code Availability

Code and raw results are in the `melanoma_articles/` directory of this repository. `node run_experiments.js a2` regenerates the results and `python3 make_figures.py` regenerates the figures.

## Competing Interests

The authors declare no competing interests.

---

## References

[1] Hanahan D, Folkman J. Patterns and emerging mechanisms of the angiogenic switch during tumorigenesis. Cell. 1996;86(3):353–364.

[2] Naumov GN, Akslen LA, Folkman J. Role of angiogenesis in human tumor dormancy: animal models of the angiogenic switch. Cell Cycle. 2006;5(16):1779–1787.

[3] Marcoval J, Moreno A, Graells J, Vidal A, Escribà JM, Garcia-Ramírez M, et al. Angiogenesis and malignant melanoma. Angiogenesis is related to the development of vertical (tumorigenic) growth phase. J Cutan Pathol. 1997;24(4):212–218.

[4] Srivastava A, Ralhan R, Kaur J. Angiogenesis in cutaneous melanoma: pathogenesis and clinical implications. Microsc Res Tech. 2003;60(2):208–224.

[5] Danielsen T, Rofstad EK. The constitutive level of vascular endothelial growth factor (VEGF) is more important than hypoxia-induced VEGF up-regulation in the angiogenesis of human melanoma xenografts. Br J Cancer. 2000;82(9):1528–1534.

[6] Eikenberry S, Thalhauser C, Kuang Y. Tumor-immune interaction, surgical treatment, and cancer recurrence in a mathematical model of melanoma. PLoS Comput Biol. 2009;5(4):e1000362.

[7] Mantovani A, Allavena P, Sica A, Balkwill F. Cancer-related inflammation. Nature. 2008;454(7203):436–444.

[8] De Palma M, Biziato D, Petrova TV. Microenvironmental regulation of tumour angiogenesis. Nat Rev Cancer. 2017;17(8):457–474.

[9] Lin EY, Li JF, Gnatovskiy L, Deng Y, Zhu L, Grzesik DA, et al. Macrophages regulate the angiogenic switch in a mouse model of breast cancer. Cancer Res. 2006;66(23):11238–11246.

[10] Nesbit M, Schaider H, Miller TH, Herlyn M. Low-level monocyte chemoattractant protein-1 stimulation of monocytes leads to tumor formation in nontumorigenic melanoma cells. J Immunol. 2001;166(11):6483–6490.

[11] Hahnfeldt P, Panigrahy D, Folkman J, Hlatky L. Tumor development under angiogenic signaling: a dynamical theory of tumor growth, treatment response, and postvascular dormancy. Cancer Res. 1999;59(19):4770–4775.

[12] Kuznetsov VA, Makalkin IA, Taylor MA, Perelson AS. Nonlinear dynamics of immunogenic tumors: parameter estimation and global bifurcation analysis. Bull Math Biol. 1994;56(2):295–321.

[13] Wilkie KP, Hahnfeldt P. Tumor–immune dynamics regulated in the microenvironment inform the transient nature of immune-induced tumor dormancy. Cancer Res. 2013;73(12):3534–3544.

[14] Enderling H, Anderson ARA, Chaplain MAJ, Beheshti A, Hlatky L, Hahnfeldt P. Paradoxical dependencies of tumor dormancy and progression on basic cell kinetics. Cancer Res. 2009;69(22):8814–8821.

[15] Kim KB, Sosman JA, Fruehauf JP, Linette GP, Markovic SN, McDermott DF, et al. BEAM: a randomized phase II study evaluating the activity of bevacizumab in combination with carboplatin plus paclitaxel in patients with previously untreated advanced melanoma. J Clin Oncol. 2012;30(1):34–41.

[16] Corrie PG, Marshall A, Dunn JA, Middleton MR, Nathan PD, Gore M, et al. Adjuvant bevacizumab in patients with melanoma at high risk of recurrence (AVAST-M): preplanned interim results from a multicentre, open-label, randomised controlled phase 3 study. Lancet Oncol. 2014;15(6):620–630.

[17] Strogatz SH. Nonlinear Dynamics and Chaos: With Applications to Physics, Biology, Chemistry, and Engineering. Reading (MA): Addison-Wesley; 1994.

[18] Bergers G, Hanahan D. Modes of resistance to anti-angiogenic therapy. Nat Rev Cancer. 2008;8(8):592–603.

[19] Ebos JML, Lee CR, Cruz-Munoz W, Bjarnason GA, Christensen JG, Kerbel RS. Accelerated metastasis after short-term treatment with a potent inhibitor of tumor angiogenesis. Cancer Cell. 2009;15(3):232–239.

[20] Pàez-Ribes M, Allen E, Hudock J, Takeda T, Okuyama H, Viñals F, et al. Antiangiogenic therapy elicits malignant progression of tumors to increased local invasion and distant metastasis. Cancer Cell. 2009;15(3):220–231.

[21] Jain RK. Normalization of tumor vasculature: an emerging concept in antiangiogenic therapy. Science. 2005;307(5706):58–62.

[22] Huang Y, Goel S, Duda DG, Fukumura D, Jain RK. Vascular normalization as an emerging strategy to enhance cancer immunotherapy. Cancer Res. 2013;73(10):2943–2948.
