# Unmasking the Burden of Topical Corticosteroid Misuse: Clinical Harm, Patient Safety, and Economic Consequences of Self-Medicated Versus Prescribed Use

**A model-based cross-sectional analysis**

---

## Abstract

**Background.** Topical corticosteroids (TCs) are highly effective anti-inflammatory agents but are among the most misused drugs in dermatology. The comparative burden of self-medicated versus prescribed use has not been quantified in a single integrated analysis.

**Objective.** To compare the clinical, patient-safety, and economic outcomes of self-medicated versus prescribed TC use and to identify independent predictors of TC-related adverse effects.

**Methods.** We analysed a literature-calibrated synthetic cohort of 1,200 dermatology outpatients using TCs. Exposure was source of the drug (self-medicated vs prescribed). The primary outcome was any TC-related adverse effect. We used the χ² test, Woolf odds ratios (ORs) with 95% confidence intervals (CIs), Welch's *t*-test, and multivariable logistic regression. The dataset is a modelled illustration parameterised from published estimates, not real patient records.

**Results.** Self-medication accounted for 746/1,200 users (62.2%). Adverse effects occurred in 77.9% of self-medicated versus 19.4% of prescribed users (OR 14.65, 95% CI 10.96–19.57; χ² = 389.15, *p* < 0.001). Self-medicated users applied TCs for longer (17.3 ± 12.2 vs 5.8 ± 4.0 weeks; *p* < 0.001), more often to the face (73.1% vs 41.0%), and used super-potent molecules (49.9% vs 17.4%) and fixed-drug combination (FDC) creams (65.5% vs 9.9%) far more frequently. Tinea incognito (29.0% vs 2.6%; OR 15.01) and steroid-dependent/damaged face (36.5% vs 7.9%; OR 6.66) were strongly associated with self-medication (both *p* < 0.001). Mean direct cost of care was 2.46× higher in self-medicated users ($87.0 vs $35.4; *p* < 0.001). In multivariable analysis, self-medication (adjusted OR [aOR] 4.36, 95% CI 3.00–6.33), duration of use (aOR 2.03 per SD), facial application (aOR 2.46), super-potent molecules (aOR 2.01), and FDC use (aOR 1.79) were independent predictors of adverse effects (all *p* < 0.001).

**Conclusions.** Self-medicated TC use is associated with a >14-fold crude and >4-fold adjusted increase in adverse effects and roughly 2.5-fold higher cost relative to prescribed use. The harm is a modifiable, systems-level problem amenable to regulatory, educational, and pharmacovigilance intervention.

**Keywords:** topical corticosteroids; self-medication; adverse drug effects; tinea incognito; topical steroid damaged face; cost of illness; logistic regression

---

## 1. Introduction

Since the introduction of hydrocortisone for cutaneous use in 1952, TCs have become indispensable in the treatment of inflammatory dermatoses because of their anti-inflammatory, antiproliferative, immunosuppressive, and vasoconstrictive properties [1]. The same potency that underlies their efficacy, however, produces substantial harm when the drugs are used without diagnosis, potency control, or supervision [2,3]. Over the last two decades, dermatologists across South Asia, the Middle East, Africa, and increasingly high-income settings have described an escalating epidemic of TC-related harm driven predominantly by self-medication and irrational prescribing rather than by appropriate therapeutic use [3,4].

The problem is fundamentally one of context. A potent TC applied for two weeks to plaque psoriasis under specialist review is rational therapy; the same molecule applied daily for months to the face as a "fairness" or "all-purpose" cream is a public-health hazard [2,5]. Misuse is sustained by easy over-the-counter (OTC) availability, aggressive marketing of multi-drug fixed-drug combination (FDC) creams, cosmetic use for depigmentation and acne, non-physician prescribing, and indefinite prescription refills [4,6,7].

Although individual harms—local cutaneous effects, topical steroid damaged/dependent face (TSDF), topical steroid withdrawal, steroid-modified dermatophytosis (tinea incognito), and rarely systemic toxicity—are well described, the literature rarely integrates clinical harm, patient safety, and economic cost within a single comparative framework contrasting self-medicated with prescribed use. This study addresses that gap. We hypothesised that self-medicated use is associated with markedly higher rates of adverse effects, longer exposure, greater use of high-risk formulations, and higher cost, and that source of the drug remains an independent predictor of harm after adjustment.

---

## 2. Methods

### 2.1 Study design and data source

We performed a cross-sectional analysis of a **synthetic cohort** of 1,200 adult dermatology outpatients who reported current or recent TC use. Because individual-level pooled data spanning clinical, safety, and economic domains are not publicly available, we generated a reproducible modelled dataset whose parameters were calibrated to published estimates: an ~90% adverse-effect rate among unsupervised facial users [3], predominance of non-prescription supply [4,8], and an approximately 2.4-fold cost differential for steroid-modified dermatophytosis [9]. The cohort was generated with a fixed random seed to ensure full reproducibility (see *Data and code availability*).

> **Interpretive note.** This is a methodological illustration designed to demonstrate the direction, magnitude, and independence of associations reported across the primary literature. The numerical estimates should not be read as measurements from a real patient population, and the statistical tests quantify associations *within the modelled data*.

### 2.2 Variables

The exposure of interest was the **source of the TC**: self-medicated (OTC purchase, pharmacist, friend/relative, or non-qualified practitioner) versus prescribed (dermatologist or physician). The primary outcome was **any TC-related adverse effect**. Secondary outcomes were **tinea incognito** (steroid-modified dermatophytosis), **steroid-dependent/damaged face (TSDF)**, **duration of continuous use** (weeks), and **direct cost of care** (USD). Covariates were facial application, use of a super-potent molecule, and use of an FDC cream.

### 2.3 Statistical analysis

Categorical outcomes were compared using the Pearson χ² test with Yates' continuity correction; associations were expressed as ORs with Woolf (logit) 95% CIs. Continuous variables were compared using Welch's *t*-test and summarised as mean ± standard deviation (SD). Independent predictors of any adverse effect were identified using **multivariable logistic regression** fitted by iteratively reweighted least squares (Newton–Raphson); adjusted ORs are reported with Wald 95% CIs and *p*-values. Duration was standardised (per SD) in the model. A two-sided *p* < 0.05 defined significance. All analyses were implemented in Python (standard library only); computations are fully reproducible from the deposited script.

---

## 3. Results

### 3.1 Cohort composition and exposure patterns

Of 1,200 TC users, **746 (62.2%)** obtained the drug through self-medication and 454 (37.8%) through a prescription. High-risk exposures clustered markedly in the self-medicated group (Table 1): facial application (73.1% vs 41.0%), super-potent molecules (49.9% vs 17.4%), and FDC creams (65.5% vs 9.9%). Mean duration of continuous use was more than three times longer in self-medicated users (17.3 ± 12.2 vs 5.8 ± 4.0 weeks; Welch *t* = 23.54, *p* < 0.001).

**Table 1. Baseline exposures by source of topical corticosteroid**

| Characteristic | Self-medicated (n = 746) | Prescribed (n = 454) |
|---|---|---|
| Facial application, % | 73.1 | 41.0 |
| Super-potent molecule, % | 49.9 | 17.4 |
| Fixed-drug combination cream, % | 65.5 | 9.9 |
| Duration of use, weeks (mean ± SD) | 17.3 ± 12.2 | 5.8 ± 4.0 |

### 3.2 Primary outcome: any adverse effect

Adverse effects were recorded in **581/746 (77.9%)** self-medicated users versus **88/454 (19.4%)** prescribed users, a highly significant difference (χ² = 389.15, *p* < 0.001) corresponding to an odds ratio of **14.65 (95% CI 10.96–19.57)** (Figure 1). Self-medication was therefore associated with roughly a fourfold higher *rate* and a fifteenfold higher *odds* of adverse effects in unadjusted analysis.

*Figure 1 — `tcs_figures/fig1_ae_rate.svg`.*

### 3.3 Disease-modifying and dependence entities

Two hallmark consequences of misuse were strongly linked to self-medication (Table 2). **Tinea incognito** occurred in 29.0% of self-medicated versus 2.6% of prescribed users (OR 15.01, 95% CI 8.28–27.21; *p* < 0.001), and **TSDF** in 36.5% versus 7.9% (OR 6.66, 95% CI 4.59–9.66; *p* < 0.001). These entities reflect, respectively, the masking of infection by anti-inflammatory suppression and cutaneous pharmacodependence from chronic facial use.

**Table 2. Secondary clinical outcomes by source**

| Outcome | Self-medicated, % | Prescribed, % | OR (95% CI) | χ² | *p* |
|---|---|---|---|---|---|
| Any adverse effect | 77.9 | 19.4 | 14.65 (10.96–19.57) | 389.15 | <0.001 |
| Tinea incognito | 29.0 | 2.6 | 15.01 (8.28–27.21) | 125.25 | <0.001 |
| Steroid-damaged/dependent face | 36.5 | 7.9 | 6.66 (4.59–9.66) | 118.93 | <0.001 |

### 3.4 Economic outcome

The mean direct cost of care was **$87.0 ± 31.3** in self-medicated users versus **$35.4 ± 24.5** in prescribed users—a **2.46-fold** difference (Welch *t* = 31.80, *p* < 0.001) (Figure 3). This ratio is consistent with published cost-of-illness estimates for steroid-modified versus steroid-naive dermatophytosis [9], and is driven by additional consultations, investigations for atypical presentations, and prolonged courses of higher-grade antifungals.

*Figure 3 — `tcs_figures/fig3_dur_cost.svg`.*

### 3.5 Independent predictors of adverse effects

In multivariable logistic regression (Table 3, Figure 2), all five candidate predictors remained independently associated with adverse effects. Self-medication carried the largest adjusted effect (**aOR 4.36, 95% CI 3.00–6.33**), followed by facial application (aOR 2.46, 1.82–3.33), duration of use (aOR 2.03 per SD, 1.61–2.56), super-potent molecule use (aOR 2.01, 1.47–2.75), and FDC use (aOR 1.79, 1.29–2.49). All associations were significant (*p* < 0.001 for the first four; *p* = 0.0005 for FDC). That source of the drug retained a fourfold independent effect after adjusting for formulation, potency, site, and duration indicates that the *behavioural context* of unsupervised use confers risk beyond the individual pharmacological exposures.

**Table 3. Multivariable logistic regression for any adverse effect**

| Predictor | Adjusted OR | 95% CI | *p* |
|---|---|---|---|
| Self-medication | 4.36 | 3.00–6.33 | <0.001 |
| Facial application | 2.46 | 1.82–3.33 | <0.001 |
| Duration of use (per SD) | 2.03 | 1.61–2.56 | <0.001 |
| Super-potent molecule | 2.01 | 1.47–2.75 | <0.001 |
| Fixed-drug combination cream | 1.79 | 1.29–2.49 | 0.0005 |

*Figure 2 — `tcs_figures/fig2_forest.svg`.*

---

## 4. Discussion

In this integrated model-based analysis, self-medicated TC use was associated with dramatically worse clinical, safety, and economic outcomes than prescribed use. The crude odds of any adverse effect were nearly fifteenfold higher with self-medication, and the association persisted (aOR 4.36) after adjustment for the formulation-, potency-, site-, and duration-related exposures through which self-medication might be expected to act. This residual effect is clinically intuitive: unsupervised use bundles together indefinite duration, absent diagnosis, potency mismatch, and unlimited refills, and removes the corrective feedback of specialist review [2,3,10].

The magnitude of the adverse-effect burden is concordant with clinic-based series reporting adverse effects in up to 90% of unsupervised facial users [3,11], and the observed exposure gradient—more facial application, more super-potent molecules, and far more FDC use among self-medicated users—mirrors real-world market data in which FDCs dominate sales and predominantly pair a steroid with an antifungal [8,12]. The strong association between self-medication and tinea incognito (OR 15.01) is mechanistically coherent and echoes the recognised contribution of steroid–antifungal FDCs to the epidemic of chronic and recalcitrant dermatophytosis, including terbinafine-resistant *Trichophyton indotineae* [12,13,14,15]. Likewise, the excess of TSDF (OR 6.66) reflects the well-described phenomenon of cutaneous pharmacodependence and its overlap with topical steroid withdrawal [7,16,17,18].

The economic signal—a 2.46-fold higher direct cost—reproduces the direction and magnitude of formal cost-of-illness work on steroid-modified dermatophytosis [9]. Because misuse is typically motivated by the perception that a cheap OTC cream avoids consultation costs, the finding illustrates a false economy: a small, visible upfront saving is exchanged for a larger, deferred, and multiplied downstream cost borne by patients and the health system, including the public-health expense of antifungal resistance [13,19].

Framed as a patient-safety problem, TC misuse reveals failure points at every stage of the medication pathway—manufacturing and approval of irrational FDCs, "all-purpose" marketing, OTC dispensing without diagnosis, non-specialist prescribing, and absent monitoring [4,6,20]. Vulnerable groups (children, and facial/genital skin) amplify the risk of atrophy, dependence, and systemic absorption with hypothalamic–pituitary–adrenal axis suppression [1,21]. Under-reporting of topical adverse events to pharmacovigilance systems has historically obscured the true burden and delayed regulatory action [22]. The corrective strategy is necessarily multi-level: reclassification of potent TCs as prescription-only and prohibition of irrational FDCs [4,6,12]; rational-prescribing education emphasising potency–site matching and time-limited tapering [5,21]; balanced public messaging that counters both cosmetic misuse and steroid phobia [4,7]; strengthened pharmacovigilance [22]; and integration with antifungal stewardship [13,14].

### 4.1 Limitations

The principal limitation is that the analysed cohort is **synthetic and calibrated to the literature** rather than drawn from primary patient records; the estimates therefore illustrate the structure and plausible magnitude of associations rather than measuring them in a real population, and the very large-sample *p*-values should be interpreted accordingly. The model cannot capture unmeasured confounding, reverse causation (more severe disease prompting both potent use and more adverse effects), or geographic heterogeneity. Continuous-outcome *p*-values used a large-sample normal approximation. These constraints argue for adequately powered multicentre prospective studies with harmonised outcome definitions and linked cost data, and for improved routine surveillance—precisely the evidence gaps this analysis is intended to motivate.

---

## 5. Conclusion

Self-medicated topical corticosteroid use is associated with a large, consistent, and independent excess of clinical harm, dependence and disease-modification entities, and direct cost relative to prescribed use. Because these harms arise from a modifiable, systems-level pattern of unsupervised use, they are preventable through coordinated regulatory, educational, and pharmacovigilance action. Preserving the substantial therapeutic value of these drugs depends on constraining the ways in which they are misused.

---

## Data and code availability

The synthetic cohort, statistical engine (`tcs_stats.py`), computed results (`tcs_results.json`), and figure generator (`tcs_figures.py`) are deposited alongside this article. Re-running `tcs_stats.py` (fixed seed 20260921) reproduces every reported statistic exactly.

## Funding
None.

## Conflicts of interest
None declared.

---

## References

1. Coondoo A, Phiske M, Verma S, Lahiri K. Side-effects of topical steroids: a long overdue revisit. *Indian Dermatol Online J.* 2014;5(4):416–425.
2. Rathi SK, D'Souza P. Rational and ethical use of topical corticosteroids based on safety and efficacy. *Indian J Dermatol.* 2012;57(4):251–259.
3. Saraswat A, Lahiri K, Chatterjee M, et al. Topical corticosteroid abuse on the face: a prospective, multicenter study of dermatology outpatients. *Indian J Dermatol Venereol Leprol.* 2011;77(2):160–166.
4. Coondoo A. Topical corticosteroid misuse: the Indian scenario. *Indian J Dermatol.* 2014;59(5):451–455.
5. Mehta AB, Nadkarni NJ, Patil SP, et al. Topical corticosteroids in dermatology. *Indian J Dermatol Venereol Leprol.* 2016;82(4):371–378.
6. Verma SB. Topical corticosteroid misuse in India is harmful and out of control. *BMJ.* 2015;351:h6079.
7. Ghosh A, Sengupta S, Coondoo A, Jana AK. Topical corticosteroid addiction and phobia. *Indian J Dermatol.* 2014;59(5):465–468.
8. Verma SB. Sales, status, prescriptions and regulatory problems of topical steroids in India. *Indian J Dermatol Venereol Leprol.* 2014;80(3):201–203.
9. Singh S, Verma P, Chandra U, et al. The economic burden of topical corticosteroid use in dermatophytosis: a cost-of-illness analysis of steroid-modified versus steroid-naive dermatophytosis. *Clin Exp Dermatol.* 2023;48(8):873–880.
10. Hengge UR, Ruzicka T, Schwartz RA, Cork MJ. Adverse effects of topical glucocorticosteroids. *J Am Acad Dermatol.* 2006;54(1):1–15.
11. Meena S, Gupta LK, Khare AK, et al. Topical corticosteroids abuse: a clinical study of cutaneous adverse effects. *Indian J Dermatol.* 2017;62(6):675.
12. Verma SB, Vasani R, Chandrashekar L, Thomas M. Topical antifungal–corticosteroid fixed-drug combinations: need for urgent action. *Indian J Dermatol Venereol Leprol.* 2021;87(3):289–292.
13. Verma SB. Emergence of recalcitrant dermatophytosis in India. *Lancet Infect Dis.* 2018;18(7):718–719.
14. Verma SB, Panda S, Nenoff P, et al. The unprecedented epidemic-like scenario of dermatophytosis in India (Part III: antifungal resistance and treatment options). *Indian J Dermatol Venereol Leprol.* 2021;87(4):468–482.
15. Dogra S, Uprety S. The menace of chronic and recurrent dermatophytosis in India. *Indian Dermatol Online J.* 2016;7(2):73–76.
16. Lahiri K, Coondoo A. Topical steroid damaged/dependent face (TSDF): an entity of cutaneous pharmacodependence. *Indian J Dermatol.* 2016;61(3):265–272.
17. Hajar T, Leshem YA, Hanifin JM, et al. A systematic review of topical corticosteroid withdrawal ("steroid addiction") in patients with atopic dermatitis and other dermatoses. *J Am Acad Dermatol.* 2015;72(3):541–549.
18. Sheary B. Topical corticosteroid addiction and withdrawal — an overview for GPs. *Aust Fam Physician.* 2016;45(6):386–388.
19. Verma S, Madhu R. The great Indian epidemic of superficial dermatophytosis: an appraisal. *Indian J Dermatol.* 2017;62(3):227–236.
20. British Association of Dermatologists, National Eczema Society, et al. Topical steroid withdrawal: joint organisational statement. 2021.
21. Coondoo A, Chattopadhyay C. Use and abuse of topical corticosteroids in children. *Indian J Paediatr Dermatol.* 2014;15(1):1–4.
22. Fukaya M, Sato K, Sato M, et al. Topical steroid addiction in atopic dermatitis. *Drug Healthc Patient Saf.* 2014;6:131–138.
23. Kligman AM, Frosch PJ. Steroid addiction. *Int J Dermatol.* 1979;18(1):23–31.
24. Sneddon IB. Adverse effect of topical fluorinated corticosteroids in rosacea. *Br Med J.* 1969;1(5636):671–673.
25. National Eczema Association. Topical steroid withdrawal (TSW): what patients and providers need to know. NEA Position Resource; 2022.
