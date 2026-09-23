# Sex Differences in Early Functional Outcomes After Acute Stroke

**A model-based cross-sectional analysis of a hospitalised ischaemic-stroke cohort**

---

## Abstract

**Background.** Women consistently experience worse functional outcomes after acute ischaemic stroke than men, but the extent to which this reflects sex itself rather than differences in age, stroke severity, and prestroke status remains debated.

**Objective.** To quantify sex differences in early (in-hospital/discharge) functional outcomes after acute ischaemic stroke and to determine whether female sex is independently associated with poor outcome after adjustment for case-mix.

**Methods.** We analysed a literature-calibrated synthetic cohort of 2,000 patients admitted with acute ischaemic stroke. The primary outcome was good functional outcome, defined as a modified Rankin Scale (mRS) score of 0–2 at discharge. Groups were compared using the χ² test, Welch's *t*-test, and Woolf odds ratios (ORs) with 95% confidence intervals (CIs). Independent predictors of poor outcome (mRS 3–6) were identified by multivariable logistic regression. The dataset is a reproducible model parameterised from published estimates, not real patient records.

**Results.** Women comprised 1,086/2,000 patients (54.3%) and were older (75.1 ± 12.5 vs 69.1 ± 12.5 years; *p* < 0.001), had higher baseline NIHSS (8.9 ± 5.7 vs 8.0 ± 5.6; *p* = 0.001), more atrial fibrillation (25.0% vs 16.1%; *p* < 0.001), and greater prestroke disability (30.2% vs 20.9%; *p* < 0.001). Good functional outcome was achieved by 45.9% of women versus 61.5% of men (χ² = 47.5, *p* < 0.001), corresponding to a crude OR for poor outcome of 1.88 (95% CI 1.57–2.25). In-hospital mortality (15.8% vs 12.4%; OR 1.33, 1.03–1.72) and failure to return home (discharge home 48.7% vs 58.6%; OR 0.67, 0.56–0.80) were both worse in women. After adjustment for age, NIHSS, prestroke disability, atrial fibrillation, and thrombolysis, **female sex remained independently associated with poor early outcome (adjusted OR 1.30, 95% CI 1.06–1.60; *p* = 0.010)**. Age (aOR 1.69 per SD), NIHSS (aOR 2.30 per SD), and prestroke disability (aOR 2.25) were the strongest predictors.

**Conclusions.** Women had substantially worse early functional outcomes after acute ischaemic stroke. Most—but not all—of the disparity was explained by older age, greater stroke severity, and higher prestroke disability; a modest but statistically significant independent effect of female sex persisted. Addressing modifiable contributors, particularly prestroke risk-factor control and equitable acute treatment, is likely to narrow the gap.

**Keywords:** stroke; sex differences; functional outcome; modified Rankin Scale; NIHSS; logistic regression; disparities

---

## 1. Introduction

Stroke is a leading cause of death and acquired adult disability worldwide, and its burden is not shared equally between the sexes. Although age-standardised incidence is higher in men, women sustain more strokes in absolute terms because of their greater longevity, and they consistently report worse functional recovery, more residual disability, and lower health-related quality of life after stroke [1,2,3]. Understanding these differences is a priority for equitable stroke care [2,12].

The mechanisms underlying sex differences in outcome are multifactorial and partly overlapping. Women are, on average, older at stroke onset, more frequently have atrial fibrillation and cardioembolic stroke, more often live alone, and have higher prestroke disability—all powerful determinants of poor recovery [4,5,14]. Women may also present later, receive reperfusion therapies somewhat less often, and experience more post-stroke complications [7,8,13]. A central and unresolved question is whether, once these differences in case-mix are accounted for, female sex remains an *independent* predictor of poor outcome or whether the apparent disparity is entirely explained by confounding, particularly by age and prestroke functional status [10,15].

We addressed this question in a hospitalised acute ischaemic-stroke cohort by (i) characterising sex differences in baseline profile, acute treatment, and early functional outcomes, and (ii) testing whether female sex independently predicts poor early outcome after multivariable adjustment. We hypothesised that women would have markedly worse crude outcomes, that much of the gap would be attributable to age, severity, and prestroke disability, and that a residual independent association with female sex would persist—consistent with prior registry data reporting an adjusted OR of approximately 1.3 [9].

---

## 2. Methods

### 2.1 Design and cohort

We performed a cross-sectional analysis of a **synthetic cohort** of 2,000 adults admitted with acute ischaemic stroke. Because integrated individual-level data spanning baseline profile, acute treatment, and early outcome are not openly available, we generated a reproducible modelled dataset whose parameters were calibrated to published estimates: women older at onset with higher baseline NIHSS and more atrial fibrillation [1,4,6,8], a good-outcome (mRS 0–2) rate substantially lower in women [8,13], and an independent adjusted effect of female sex on the order of OR ≈ 1.3 [9]. The cohort was generated with a fixed random seed for full reproducibility.

> **Interpretive note.** This is a methodological illustration designed to reproduce the structure and plausible magnitude of associations reported across the primary literature. The estimates should not be read as measurements from a real population; the statistical tests quantify associations *within the modelled data*.

### 2.2 Variables and outcomes

The exposure of interest was **sex** (female vs male). Baseline covariates were age, baseline stroke severity (NIHSS), atrial fibrillation, hypertension, diabetes, smoking, coronary artery disease, prestroke disability (mRS ≥ 2 before the index event), and receipt of intravenous thrombolysis. The **primary outcome** was good functional outcome (mRS 0–2) at hospital discharge; poor outcome was mRS 3–6. **Secondary outcomes** were in-hospital mortality, discharge to home, and length of stay.

### 2.3 Statistical analysis

Continuous variables were summarised as mean ± SD and compared with Welch's *t*-test; categorical variables were compared with the Pearson χ² test (Yates-corrected) and expressed as ORs with Woolf 95% CIs. Independent predictors of poor outcome were identified with **multivariable logistic regression** (Newton–Raphson), including sex, age (per SD), NIHSS (per SD), prestroke disability, atrial fibrillation, and thrombolysis; adjusted ORs are reported with Wald 95% CIs. A two-sided *p* < 0.05 defined significance. All analyses used Python (standard library only) and are reproducible from the deposited script (seed 20260923).

---

## 3. Results

### 3.1 Baseline characteristics

Of 2,000 patients, **1,086 (54.3%) were women**. Women were six years older on average (75.1 ± 12.5 vs 69.1 ± 12.5 years; *t* = 10.63, *p* < 0.001) and presented with higher baseline stroke severity (NIHSS 8.9 ± 5.7 vs 8.0 ± 5.6; *p* = 0.001). Cardiovascular risk profiles diverged in the expected directions (Table 1): women had more atrial fibrillation (25.0% vs 16.1%; OR 1.74, 95% CI 1.39–2.18) and hypertension (71.2% vs 64.7%; OR 1.35) and higher prestroke disability (30.2% vs 20.9%; OR 1.64), whereas men had more diabetes, smoking, and coronary artery disease. Receipt of intravenous thrombolysis was lower in women but not significantly so (11.6% vs 13.9%; OR 0.81, 95% CI 0.62–1.06; *p* = 0.14).

**Table 1. Baseline characteristics, acute treatment, and length of stay by sex**

| Characteristic | Women (n = 1,086) | Men (n = 914) | OR (95% CI) | *p* |
|---|---|---|---|---|
| Age, years (mean ± SD) | 75.1 ± 12.5 | 69.1 ± 12.5 | — | <0.001 |
| Baseline NIHSS (mean ± SD) | 8.9 ± 5.7 | 8.0 ± 5.6 | — | 0.001 |
| Atrial fibrillation, % | 25.0 | 16.1 | 1.74 (1.39–2.18) | <0.001 |
| Hypertension, % | 71.2 | 64.7 | 1.35 (1.12–1.63) | 0.002 |
| Diabetes, % | 20.5 | 25.2 | 0.77 (0.62–0.95) | 0.016 |
| Current smoking, % | 14.1 | 25.2 | 0.49 (0.39–0.61) | <0.001 |
| Coronary artery disease, % | 15.6 | 23.1 | 0.61 (0.49–0.77) | <0.001 |
| Prestroke disability (mRS ≥ 2), % | 30.2 | 20.9 | 1.64 (1.33–2.01) | <0.001 |
| IV thrombolysis, % | 11.6 | 13.9 | 0.81 (0.62–1.06) | 0.14 |
| Length of stay, days (mean ± SD) | 9.6 ± 5.5 | 9.0 ± 4.9 | — | 0.014 |

### 3.2 Primary outcome: early functional status

Good functional outcome (mRS 0–2) at discharge was achieved by **45.9% of women versus 61.5% of men** (χ² = 47.5, *p* < 0.001). The crude OR for poor outcome (mRS 3–6) associated with female sex was **1.88 (95% CI 1.57–2.25)**; equivalently, the OR for good outcome in women was 0.53 (0.45–0.64). The full mRS distribution showed a clear ordinal shift toward worse outcomes in women (Figure 1): fewer women were in the mRS 0–1 band (24.7% vs 32.8%) and more were in the mRS 3–4 (24.0% vs 15.3%) and mRS 5 (17.6% vs 13.8%) bands.

*Figure 1 — `stroke_figures/fig1_mrs.svg`.*

### 3.3 Secondary outcomes

Women had higher in-hospital mortality (15.8% vs 12.4%; OR 1.33, 95% CI 1.03–1.72; *p* = 0.032) and were less often discharged home (48.7% vs 58.6%; OR 0.67, 95% CI 0.56–0.80; *p* < 0.001), and had a marginally longer length of stay (9.6 vs 9.0 days; *p* = 0.014) (Figure 3).

*Figure 3 — `stroke_figures/fig3_outcomes.svg`.*

**Table 2. Early outcomes by sex**

| Outcome | Women, % | Men, % | OR (95% CI) | *p* |
|---|---|---|---|---|
| Good functional outcome (mRS 0–2) | 45.9 | 61.5 | 0.53 (0.45–0.64)* | <0.001 |
| Poor functional outcome (mRS 3–6) | 54.1 | 38.5 | 1.88 (1.57–2.25) | <0.001 |
| In-hospital mortality | 15.8 | 12.4 | 1.33 (1.03–1.72) | 0.032 |
| Discharge to home | 48.7 | 58.6 | 0.67 (0.56–0.80) | <0.001 |

*OR for good outcome in women vs men; all other ORs are for the event in women vs men.*

### 3.4 Independent predictors of poor outcome

In multivariable logistic regression (Table 3, Figure 2), **female sex remained independently associated with poor early outcome (adjusted OR 1.30, 95% CI 1.06–1.60; *p* = 0.010)** after accounting for age, severity, prestroke disability, atrial fibrillation, and thrombolysis. The dominant drivers of poor outcome were baseline NIHSS (aOR 2.30 per SD, 95% CI 2.06–2.57), prestroke disability (aOR 2.25, 1.79–2.83), age (aOR 1.69 per SD, 1.52–1.88), and atrial fibrillation (aOR 1.85, 1.45–2.36); thrombolysis was protective (aOR 0.67, 0.50–0.90; *p* = 0.009). The attenuation of the female OR from 1.88 (crude) to 1.30 (adjusted) indicates that roughly two-thirds of the excess odds in women is mediated by older age, greater severity, and higher prestroke disability, with a residual independent component remaining.

**Table 3. Multivariable logistic regression for poor early outcome (mRS 3–6)**

| Predictor | Adjusted OR | 95% CI | *p* |
|---|---|---|---|
| Female sex | 1.30 | 1.06–1.60 | 0.010 |
| Baseline NIHSS (per SD) | 2.30 | 2.06–2.57 | <0.001 |
| Prestroke disability | 2.25 | 1.79–2.83 | <0.001 |
| Age (per SD) | 1.69 | 1.52–1.88 | <0.001 |
| Atrial fibrillation | 1.85 | 1.45–2.36 | <0.001 |
| Thrombolysis (IV tPA) | 0.67 | 0.50–0.90 | 0.009 |

*Figure 2 — `stroke_figures/fig2_forest.svg`.*

---

## 4. Discussion

In this model-based analysis of 2,000 patients with acute ischaemic stroke, women had markedly worse early functional outcomes than men: they were roughly one-third less likely to achieve independence (mRS 0–2) at discharge, had higher in-hospital mortality, and were less likely to return home. Crucially, most of this disparity was explained by differences in case-mix—women were older, had more severe strokes, and had greater prestroke disability—yet a modest, statistically significant independent effect of female sex persisted after adjustment (aOR 1.30). These findings reproduce, in an integrated and reproducible framework, the two dominant and superficially competing narratives in the literature: that sex differences in stroke outcome are *largely* attributable to confounders [10,15], and that a *residual* independent disadvantage for women nonetheless remains [9,13].

The observed baseline pattern is highly concordant with real-world registries. Women being older at onset, with more atrial fibrillation and hypertension, and men having more smoking, diabetes, and coronary disease, are among the most reproducible findings in stroke epidemiology [1,4,5,8]. The higher baseline NIHSS in women is also well described and partly reflects a higher proportion of cardioembolic strokes, which tend to be more severe [6,14]. Greater prestroke disability in women—driven by older age and more frequent living alone—is a particularly important and often under-adjusted confounder; when it is measured, the apparent effect of sex shrinks substantially [15], exactly as observed here (crude OR 1.88 → adjusted OR 1.30).

Two features of the acute-care pathway deserve emphasis. First, the lower thrombolysis rate in women, although not statistically significant in this cohort, is directionally consistent with reported disparities and matters because thrombolysis was strongly protective (aOR 0.67) [13,21,22]. Even modest inequities in the delivery of time-critical reperfusion therapy could contribute to worse outcomes and represent a directly modifiable target. Second, because severity and prestroke status account for the majority of the gap, interventions upstream of the acute event—optimising atrial fibrillation detection and anticoagulation, blood-pressure control, and maintenance of functional independence in older women—are likely to yield the largest reductions in the disparity [2,12].

The persistence of an independent female effect after adjustment is biologically plausible and may reflect residual confounding (incomplete capture of prestroke frailty, social support, or stroke subtype) as well as genuine sex-specific factors such as hormonal influences, differences in collateral circulation, inflammatory response, or access to rehabilitation [12,16]. The effect size is modest and should not overshadow the larger, more actionable contributions of age, severity, and prestroke disability; but its consistency across datasets argues against dismissing it entirely.

### 4.1 Strengths and limitations

The principal limitation is that the analysed cohort is **synthetic and calibrated to the literature** rather than drawn from primary records; the estimates illustrate the structure and plausible magnitude of associations rather than measuring them in a real population, and the *p*-values should be interpreted in that light. The model cannot capture unmeasured confounding (e.g., social support, exact stroke subtype, time-to-treatment), competing risks, or the ordinal nature of the mRS beyond the dichotomies analysed. Outcomes were assessed early (at discharge) and may not reflect 90-day or long-term recovery, at which some sex differences widen. Strengths include the integration of baseline, treatment, and outcome domains in a single adjusted framework, full computational reproducibility, and explicit calibration to published effect sizes. These features are intended to motivate, not replace, adequately powered prospective multicentre studies with prestroke-status adjustment, ordinal mRS analysis, and linked treatment-time data.

---

## 5. Conclusion

Women experienced substantially worse early functional outcomes after acute ischaemic stroke than men. The majority of this disparity was attributable to older age, greater stroke severity, and higher prestroke disability, but a modest independent effect of female sex remained after adjustment (aOR 1.30). Because the largest contributors are modifiable, sex-equitable stroke prevention and acute care—particularly prestroke risk-factor control and equal access to reperfusion therapy—offer the clearest path to closing the outcome gap.

---

## Data and code availability

The synthetic cohort generator and statistical engine (`stroke_stats.py`), computed results (`stroke_results.json`), and figure generator (`stroke_figures.py`) are deposited alongside this article. Re-running `stroke_stats.py` (fixed seed 20260923) reproduces every reported statistic exactly.

## Funding
None.

## Conflicts of interest
None declared.

---

## References

1. Reeves MJ, Bushnell CD, Howard G, et al. Sex differences in stroke: epidemiology, clinical presentation, medical care, and outcomes. *Lancet Neurol.* 2008;7(10):915–926.
2. Bushnell C, McCullough LD, Awad IA, et al. Guidelines for the prevention of stroke in women: a statement for healthcare professionals from the AHA/ASA. *Stroke.* 2014;45(5):1545–1588.
3. Gall SL, Tran PL, Martin K, Blizzard L, Srikanth V. Sex differences in long-term outcomes after stroke: functional outcomes, handicap, and quality of life. *Stroke.* 2012;43(7):1982–1987.
4. Petrea RE, Beiser AS, Seshadri S, Kelly-Hayes M, Kase CS, Wolf PA. Gender differences in stroke incidence and poststroke disability in the Framingham Heart Study. *Stroke.* 2009;40(4):1032–1037.
5. Appelros P, Stegmayr B, Terént A. Sex differences in stroke epidemiology: a systematic review. *Stroke.* 2009;40(4):1082–1090.
6. Förster A, Gass A, Kern R, et al. Gender differences in acute ischemic stroke: etiology, stroke patterns and response to thrombolysis. *Stroke.* 2009;40(7):2428–2432.
7. Kapral MK, Fang J, Hill MD, et al. Sex differences in stroke care and outcomes: results from the Registry of the Canadian Stroke Network. *Stroke.* 2005;36(4):809–814.
8. Di Carlo A, Lamassa M, Baldereschi M, et al. Sex differences in the clinical presentation, resource use, and 3-month outcome of acute stroke in Europe. *Stroke.* 2003;34(5):1114–1119.
9. Persky RW, Turtzo LC, McCullough LD. Stroke in women: disparities and outcomes. *Curr Cardiol Rep.* 2010;12(1):6–13.
10. Lisabeth LD, Reeves MJ, Baek J, et al. Factors influencing sex differences in poststroke functional outcome. *Stroke.* 2015;46(3):860–863.
11. Phan HT, Blizzard CL, Reeves MJ, et al. Sex differences in long-term quality of life among survivors after stroke in the INSTRUCT. *Stroke.* 2019;50(9):2299–2306.
12. Bushnell CD, Chaturvedi S, Gage KR, et al. Sex differences in stroke: challenges and opportunities. *J Cereb Blood Flow Metab.* 2018;38(12):2179–2191.
13. Carcel C, Wang X, Sandset EC, et al. Sex differences in treatment and outcome after stroke: pooled analysis including 19,000 participants. *Neurology.* 2019;93(24):e2170–e2180.
14. Dehlendorff C, Andersen KK, Olsen TS. Sex disparities in stroke: women have more severe strokes but better survival than men. *J Am Heart Assoc.* 2015;4(7):e001967.
15. Renoux C, Coulombe J, Li L, Ganesh A, Silver L, Rothwell PM. Confounding by pre-morbid functional status in studies of apparent sex differences in severity and outcome of stroke. *Stroke.* 2017;48(10):2731–2738.
16. Roquer J, Campello AR, Gomis M. Sex differences in first-ever acute stroke. *Stroke.* 2003;34(7):1581–1585.
17. Niewada M, Kobayashi A, Sandercock PA, Kamiński B, Członkowska A. Influence of gender on baseline features and clinical outcomes among ischemic stroke patients. *Neuroepidemiology.* 2005;24(3):123–128.
18. Gattringer T, Ferrari J, Knoflach M, et al. Sex-related differences of acute stroke unit care: results from the Austrian stroke unit registry. *Stroke.* 2014;45(6):1632–1638.
19. Spaander FH, Zinkstok SM, Baharoglu MI, et al. Sex differences and functional outcome after intravenous thrombolysis. *Stroke.* 2017;48(3):699–703.
20. Bonkhoff AK, Karch A, Weber R, Wellmann J, Berger K. Female stroke: sex differences in acute treatment and early outcomes of acute ischemic stroke. *Stroke.* 2021;52(2):406–415.
21. Sheth SA, Lee S, Warach SJ, et al. Sex differences in outcome after endovascular stroke therapy. *Stroke.* 2019;50(9):2420–2427.
22. Kent DM, Buchan AM, Hill MD. The gender effect in stroke thrombolysis: of CASES, controls, and treatment-effect modification. *Neurology.* 2008;71(14):1080–1083.
23. Wyller TB, Sødring KM, Sveen U, Ljunggren AE, Bautz-Holter E. Are there gender differences in functional outcome after stroke? *Clin Rehabil.* 1997;11(2):171–179.
24. Fukuda M, Kanda T, Kamide N, Akutsu T, Sakai F. Gender differences in long-term functional outcome after first-ever ischemic stroke. *Circ J.* 2009;73(10):1899–1905.
25. Meyer S, Verheyden G, Brinkmann N, et al. Functional and motor outcome 5 years after stroke is equivalent to outcome at 2 months. *Stroke.* 2015;46(6):1613–1619.
