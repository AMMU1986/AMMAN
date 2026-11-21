# How Far Does Tumour-Directed Immunity Reach? Stochastic Satellite Seeding, an Immune Halo and Excision Margins in a Spatial Melanoma Model

**[Author names]**

[Affiliations]

*Corresponding author: [e-mail]

---

## Abstract

Eikenberry, Thalhauser and Kuang modelled local metastatic seeding from a primary melanoma as a Poisson process with exponentially distributed dispersal distances. They reported that moderately metastatic tumours suppress satellite disease best, because they activate a widespread local immune response. We revisited this question with a reduced, radially symmetric version of their tumour–immune model, using deterministic single-satellite experiments and stochastic Monte Carlo simulations (840 runs over seeding rate and dispersal distance, and 1080 runs over excision margin). Single-satellite experiments showed an immune "halo" around the primary tumour. Satellites seeded within about 1.4–1.7 mm of the primary edge were held at a stable sub-detectable density, while those farther out escaped. The halo reach changed little as immune recruitment rose from Q = 0.04 to 0.09 and increased to 2.5 mm at Q = 0.10. Recruitment also determined whether dormant satellites recurred after the primary was removed. They recurred for Q ≤ 0.08, but at Q ≥ 0.09 the post-surgical immune response kept them dormant. In stochastic simulations, the probability of recurrence after resection rose monotonically with the seeding rate for every dispersal distance. We did not reproduce an intermediate optimum. The fraction of runs in which recurrence was triggered by surgery, rather than present before it, did peak at intermediate seeding rates: 0.63 at 0.01–0.03 seeds per day for a mean dispersal of 0.5 mm, 0.95 at 0.1 per day for 0.25 mm, and 1.0 at 1 per day for 0.125 mm. Higher seeding raised local immune-cell mass up to 6.9-fold but did not prevent escape. The excision margin needed to keep recurrence probability below 10% was about 1 mm for short dispersal and 1.5–2 mm for intermediate dispersal. For long dispersal it was not reached within 3 mm. These results suggest that the intermediate optimum reported for the original model depends on mechanisms absent from our reduction, such as debris-driven immune activation. They also suggest that the spatial reach of peritumoral immunity, together with the dispersal distance of micrometastases, sets the margin at which surgery stops triggering recurrence.

**Keywords:** Melanoma; Satellite metastasis; Monte Carlo simulation; Poisson seeding; Immune surveillance; Excision margin; Reaction–diffusion model

---

## 1. Introduction

Satellite and in-transit metastases are lymphatic deposits of melanoma in the skin between the primary tumour and the regional lymph nodes. They carry a poor prognosis [1,2]. Local recurrence after excision is often caused by satellites that were present but undetected at surgery, rather than by residual primary tumour [3]. Melanoma excision margins are therefore set to remove both the visible tumour and any occult deposits. Randomised trials support margins of 1–2 cm depending on tumour thickness [4–6].

Eikenberry, Thalhauser and Kuang (hereafter EKT) proposed a model of local seeding in which satellites are created by a Poisson process with rate λ_seed. Each satellite lodges at a distance from the primary edge drawn from an exponential distribution with rate λ_distance [7]. Satellites close to the primary were suppressed by the immune response directed against it. When the primary was removed, the satellites grew. EKT also reported a non-intuitive result (their Fig. 10). A low seeding rate produced a single escaping satellite. Moderate to high rates produced many satellites that were all eliminated by the immune response. Very high rates overwhelmed it. They concluded that moderately metastatic tumours induce the local immune activation that is best for suppressing metastatic disease.

That result was based on a small number of realisations of a stochastic process. It also depends on how far the immune response around the primary reaches. Here we measure this reach directly in a reduced version of the EKT model and then repeat the seeding experiment as a Monte Carlo study with 40 realisations per parameter pair. We ask three questions:

1. How far from the primary edge can a satellite be held dormant, and how does this distance depend on immune strength?
2. Does recurrence probability vary non-monotonically with seeding rate?
3. What excision margin is needed to make surgery-triggered recurrence unlikely?

---

## 2. Methods

### 2.1 Model

We use the reduced EKT model described in full in Article 1 of this series. It is a radially symmetric domain of radius 12 mm with primary tumour cells p, satellite cells s, cytotoxic immune cells m, a vascular density e, and quasi-steady immune-attracting factor a and tumour angiogenic factor v. Densities are scaled by the tumour carrying capacity. With T = p + s, activation Γ = T/(ξ + T) and kill rate k = (τ_c0 + τ_cA Γ) m/(λ_c + T):

∂p/∂t = D_c ∇·(p∇p) + r_c p (1 − T/K_p) − k p,      K_p = K_0 + (1 − K_0) e

∂s/∂t = D_c ∇·(s∇s) + r_c s (1 − T/K_s) − k s

∂m/∂t = D_m ∇²m − χ ∇·(m∇a) + Q a/(a + φ_a) − β_K T m/(λ_m + m) − β_m m

with quasi-steady a and v and vascular dynamics as in Article 1. Parameters are those of Article 1, Table 1, with immune recruitment Q = 0.05 day⁻¹ unless varied. Immune-angiogenic production is off (γ_vm = 0), so the primary does not vascularise. Densities below 10⁻⁵, roughly 0.1 cell per grid ring, are set to zero.

### 2.2 Stochastic seeding

From day 180 until surgery on day 540, satellites are seeded by a Poisson process with rate λ_seed (per day). At each time step of 0.05 day, the number of new satellites is drawn from a Poisson distribution with mean λ_seed Δt. Each satellite is placed at radius r = r_edge + d, where r_edge is the current primary edge (outermost radius with p > 0.01) and d is drawn from an exponential distribution with rate λ_dist (per mm). The mean dispersal distance is therefore 1/λ_dist. A satellite adds density 0.002 to the grid ring containing r. As in EKT, radial symmetry means each satellite is a ring. Surgery removes all tissue within r_edge + margin. Each run uses its own seed for a pseudo-random number generator (Mulberry32), so all results are reproducible.

### 2.3 Outcome measures

Satellite burden is the integrated mass ∫2πr s dr. Burden is detectable when it exceeds 0.1, about one quarter of the mass of the controlled primary. For each run we record:
- whether satellite burden was detectable before surgery (day 539);
- whether it was detectable at the end of the simulation (day 1200), which we call recurrence;
- whether recurrence was triggered by surgery, meaning detectable at the end but not before surgery;
- the mean immune-cell mass during the seeding period.

### 2.4 Experiments

1. **Halo map (deterministic).** A single satellite is seeded on day 180 at r = 1.0–5.0 mm (step 0.1), for Q = 0.04–0.10 (step 0.01). This is run with and without surgery on day 540 (0.5 mm margin), giving 574 runs.
2. **Seeding Monte Carlo.** λ_seed ∈ {0.003, 0.01, 0.03, 0.1, 0.3, 1, 3} per day, λ_dist ∈ {2, 4, 8} per mm, 40 realisations each, surgery with 0.5 mm margin: 840 runs.
3. **Margin study.** λ_seed ∈ {0.03, 0.3}, λ_dist ∈ {2, 4, 8}, margin ∈ {0, 0.5, 1.0, 1.5, 2.0, 3.0} mm, 30 realisations each: 1080 runs.

---

## 3. Results

### 3.1 The primary tumour is surrounded by an immune halo

Figure 1A maps the fate of a single satellite with the primary left in place. At every immune strength we tested, satellites close to the primary were held at a stable density below detection, and satellites beyond a sharp outer limit escaped. With baseline recruitment (Q = 0.05; primary edge 0.9 mm), satellites seeded at 1.0–2.5 mm were dormant and those at 2.6 mm or more escaped. At the weakest recruitment (Q = 0.04), the primary was larger (edge 1.4 mm). Satellites at 1.0–1.7 mm merged with it or were eliminated, those at 1.8–3.1 mm were dormant, and those beyond escaped. For Q = 0.06–0.09, the primary shrank to an edge of 0.4–0.6 mm and the dormant band ended at 1.9–2.1 mm.

[Insert Figure 1 here]

Figure 1. The immune halo. Fate of a single satellite seeded on day 180 at radius r (horizontal axis) for immune recruitment Q (vertical axis). (A) Primary left in place; outcome at day 1200. (B) Primary resected on day 540 with a 0.5 mm margin. Green: eliminated or excised. Yellow: dormant (present but below detection). Red: escaped while the primary was present. Orange: recurred after surgery. Primary edge radii are 1.4, 0.9, 0.6, 0.5, 0.4, 0.4 and 0.4 mm for Q = 0.04 to 0.10.

Measured from the primary edge, the halo reach was 1.7, 1.6, 1.5, 1.4, 1.5 and 1.5 mm for Q = 0.04 to 0.09. Stronger recruitment shrank the primary but barely changed how far beyond its edge the halo extended. At Q = 0.10 the reach increased to 2.5 mm. We did not identify the cause of this jump and treat it as an observation within the range tested.

Figure 1B shows the same experiment with surgery. For Q ≤ 0.08, almost every dormant satellite outside the excision boundary recurred after surgery. The one exception was a satellite at 2.0 mm with Q = 0.04, just outside the 1.9 mm boundary, which the remaining infiltrate eliminated. At Q = 0.09, satellites at 1.0–1.9 mm stayed dormant after surgery. At Q = 0.10, satellites up to 2.8 mm stayed dormant, and only the outermost position (2.9 mm) recurred. At high recruitment, the immune cells that the satellite attracts on its own are enough to keep it dormant once the primary is gone. This is the "low-level metastatic persistence" state of EKT Fig. 9 [7]. The response that was keeping the satellite dormant comes from the satellite itself, not from the primary.

### 3.2 Recurrence probability rises monotonically with seeding rate

Table 1 and Figure 2 summarise the seeding Monte Carlo. For every dispersal distance, the probability of recurrence rose monotonically with seeding rate. With long dispersal (λ_dist = 2 per mm, mean 0.5 mm), recurrence probability was 0.43 at λ_seed = 0.003 per day, when on average fewer than one satellite was seeded. It reached 1.0 at λ_seed = 0.03 per day. Short dispersal shifted the curve to higher seeding rates. Recurrence probability reached 0.5 between 0.01 and 0.03 per day for λ_dist = 4, and at about 0.1 per day for λ_dist = 8. We found no intermediate seeding rate at which recurrence probability fell.

[Insert Figure 2 here]

Figure 2. Monte Carlo seeding experiment (40 realisations per point). (A) Probability that satellite burden is detectable before surgery (dashed) and at day 1200 (solid). (B) Fraction of runs in which recurrence was triggered by surgery: detectable at day 1200 but not before surgery.

Table 1. Seeding Monte Carlo results (40 realisations each; surgery on day 540 with a 0.5 mm margin). "Seeds" is the mean number of satellites; "pre" and "recurrence" are the probabilities of detectable burden before surgery and at day 1200; "triggered" is the fraction with recurrence that was not detectable before surgery; "immune mass" is the mean immune-cell mass between days 180 and 540; "primary lost" is the fraction of runs in which the primary was eliminated before surgery.

| λ_dist (mm⁻¹) | λ_seed (day⁻¹) | Seeds | Pre | Recurrence | Triggered | Immune mass | Primary lost |
|---|---|---|---|---|---|---|---|
| 2 | 0.003 | 0.8 | 0.08 | 0.43 | 0.35 | 2.29 | 0.05 |
| 2 | 0.01 | 3.4 | 0.13 | 0.75 | 0.63 | 2.30 | 0.05 |
| 2 | 0.03 | 10.8 | 0.38 | 1.00 | 0.63 | 3.36 | 0.23 |
| 2 | 0.1 | 36.2 | 0.78 | 1.00 | 0.23 | 7.24 | 0.55 |
| 2 | 0.3 | 107 | 1.00 | 1.00 | 0.00 | 11.0 | 0.70 |
| 2 | 3 | 1085 | 1.00 | 1.00 | 0.00 | 15.8 | 0.93 |
| 4 | 0.003 | 0.8 | 0.00 | 0.23 | 0.23 | 1.76 | 0.00 |
| 4 | 0.03 | 10.8 | 0.00 | 0.78 | 0.78 | 1.77 | 0.00 |
| 4 | 0.1 | 36.2 | 0.03 | 0.98 | 0.95 | 1.78 | 0.00 |
| 4 | 1 | 364 | 0.40 | 1.00 | 0.60 | 3.38 | 0.23 |
| 4 | 3 | 1085 | 0.68 | 1.00 | 0.33 | 5.07 | 0.55 |
| 8 | 0.003 | 0.8 | 0.00 | 0.08 | 0.08 | 1.76 | 0.00 |
| 8 | 0.1 | 36.2 | 0.00 | 0.53 | 0.53 | 1.77 | 0.00 |
| 8 | 0.3 | 107 | 0.00 | 0.90 | 0.90 | 1.78 | 0.00 |
| 8 | 3 | 1085 | 0.03 | 1.00 | 0.98 | 1.88 | 0.00 |

Two features help explain why higher seeding did not improve control. First, higher seeding did raise immune activity, as EKT proposed. With λ_dist = 2, mean immune-cell mass rose from 2.3 to 15.8 as the seeding rate rose from 0.003 to 3 per day, a 6.9-fold increase. Immune mass rose only in parameter sets where satellites escaped before surgery. With λ_dist = 8, where escape before surgery was rare, it stayed at 1.76–1.88 at every seeding rate, even with over 1000 satellites seeded. The increase was therefore a response to escaped disease rather than a cause of suppression. Dormant satellites are held at densities where immune activation Γ is low (Article 1), so they recruit few additional immune cells. A cloud of dormant satellites therefore does not broaden the halo. Second, at high seeding rates with long dispersal, the primary itself was frequently eliminated before surgery (up to 93% of runs). In these runs, escaped satellites crowded the primary and attracted immune cells that also attacked it. We did not separate the contributions of these two effects.

The fraction of recurrences triggered by surgery did peak at intermediate seeding rates (Figure 2B). It reached 0.63 at 0.01–0.03 per day for λ_dist = 2, 0.95 at 0.1 per day for λ_dist = 4, and 1.0 at 1 per day for λ_dist = 8. At low seeding rates most runs produced no satellite inside the halo. At high rates at least one satellite landed beyond the halo and escaped before surgery. At intermediate rates, satellites accumulated inside the halo, stayed dormant, and were released by surgery. A clinically silent satellite population that surgery then releases is therefore most likely for moderately metastatic tumours.

### 3.3 A single realisation

Figure 3 shows one realisation with λ_seed = 0.1 per day and λ_dist = 4 per mm. Thirty-seven satellites were seeded between days 180 and 540, at radii of 0.91–1.89 mm, which is within 1.0 mm of the primary edge at 0.9 mm (Figure 3B). Total satellite mass stayed at 4.5 × 10⁻³ until surgery, below detection. Surgery removed satellites within 1.4 mm of the centre. The rest recurred, became detectable 39 days after surgery, and reached a steady mass of 7.0, 17 times the primary.

[Insert Figure 3 here]

Figure 3. One stochastic realisation (λ_seed = 0.1 per day, λ_dist = 4 per mm). (A) Masses of the primary, satellites and immune cells; surgery on day 540. (B) Seeding time and radius of each satellite; the dashed line is the excision boundary.

### 3.4 Margin needed to prevent surgery-triggered recurrence

Recurrence probability fell with margin, at a rate that depended on dispersal distance (Figure 4, Table 2). With short dispersal (λ_dist = 8, mean 0.125 mm), a 1 mm margin brought the probability to 0.00–0.03 for both seeding rates. With intermediate dispersal (λ_dist = 4), a 1.5 mm margin was needed at λ_seed = 0.03 (probability 0.03), and a 2 mm margin at λ_seed = 0.3 (0.07). With long dispersal (λ_dist = 2), recurrence probability was still 0.27 at a 3 mm margin with λ_seed = 0.03, and 0.93 with λ_seed = 0.3. Many of these satellites lodged beyond the halo and escaped before surgery, so no margin could prevent them.

[Insert Figure 4 here]

Figure 4. Recurrence probability as a function of excision margin (30 realisations per point) for three dispersal rates and two seeding rates (solid 0.03 per day, dashed 0.3 per day).

Table 2. Recurrence probability by margin (30 realisations each).

| λ_dist (mm⁻¹) | λ_seed (day⁻¹) | 0 mm | 0.5 mm | 1.0 mm | 1.5 mm | 2.0 mm | 3.0 mm |
|---|---|---|---|---|---|---|---|
| 2 | 0.03 | 0.90 | 1.00 | 0.77 | 0.43 | 0.40 | 0.27 |
| 2 | 0.3 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.93 |
| 4 | 0.03 | 0.77 | 0.77 | 0.17 | 0.03 | 0.00 | 0.00 |
| 4 | 0.3 | 1.00 | 1.00 | 0.90 | 0.40 | 0.07 | 0.03 |
| 8 | 0.03 | 0.87 | 0.17 | 0.00 | 0.00 | 0.00 | 0.00 |
| 8 | 0.3 | 1.00 | 0.90 | 0.03 | 0.00 | 0.00 | 0.00 |

The required margin follows the halo reach, about 1.5 mm in this geometry. Margins shorter than the halo leave dormant satellites in place and remove the infiltrate that controls them. Margins longer than the halo remove the dormant satellites as well. When the mean dispersal distance is a substantial fraction of the halo reach, margin alone cannot prevent recurrence, because some satellites escape before surgery. Recurrence probability for λ_dist = 2 and λ_seed = 0.03 was slightly higher with a 0.5 mm margin than with no margin (1.00 vs. 0.90). The difference is within sampling error but agrees in direction with the observation in Article 1 that cutting at the visible edge leaves part of the immune infiltrate in place.

---

## 4. Discussion

We measured the spatial reach of tumour-directed immunity in a reduced EKT model and used it to interpret stochastic seeding experiments. The main finding is an immune halo. In a band of fixed width around the primary edge (about 1.4–1.7 mm over most of the range of immune strength we tested), satellites are held dormant. Outside it they escape. The halo has a sharp outer boundary, and its width relative to the primary edge changes little with immune recruitment. Together with the dispersal distance of micrometastases, the halo determines how many satellites are released by surgery and which margins prevent this.

We did not reproduce the intermediate optimum in seeding rate reported by EKT [7]. In our reduction, recurrence probability rises monotonically with seeding rate, and the immune activation generated by many satellites mostly follows escape rather than preventing it. Several differences could explain this. EKT immune cells are also activated by necrotic debris, which accumulates in larger lesions, and this pathway is absent from our model. EKT's results came from a few realisations, so stochastic variation may have contributed. Their geometry was three-dimensional with satellites at the vascular level. Our Monte Carlo does reproduce a related non-monotonic quantity: the fraction of recurrences that surgery triggers is highest for moderately metastatic tumours. This is the population that the EKT mechanism concerns. At low seeding rates no satellite is present, and at high rates disease is already detectable before surgery.

The model has clinical implications only at the level of mechanism. Our domain is a few millimetres across, while clinical margins are measured in centimetres and are justified by trial outcomes [4–6]. Satellite and in-transit metastases also travel through dermal lymphatics over centimetres [1,2], whereas our dispersal distances are fractions of a millimetre. The general point does transfer. If peritumoral immunity keeps nearby micrometastases dormant, margin choice involves a trade-off between removing dormant disease and leaving its immune control intact. Information on peritumoral immune infiltration, which is already recognised as prognostic in melanoma [8], could therefore be relevant to surgical planning. This hypothesis would need testing in models with realistic lymphatic transport and in clinical data that relate infiltrate pattern to local recurrence.

### 4.1 Limitations

The limitations of the reduced EKT framework (Article 1) apply. These include radial symmetry, which makes every satellite a ring, as well as the lack of explicit oxygen, necrosis, basement membrane and adaptive immunity, and dimensionless masses. Seeding is uniform in time from day 180 to surgery and independent of primary size. Satellites are deterministic once seeded, and the extinction of small populations is approximated by a density threshold. The Monte Carlo sample sizes (30–40 per point) give probability estimates with standard errors up to about 0.09. The cause of the larger halo at Q = 0.10 was not identified.

### 4.2 Conclusions

In a reduced EKT model, the primary melanoma is surrounded by an immune halo about 1.5 mm wide in which satellites remain dormant. Recurrence probability after resection rises monotonically with seeding rate. The fraction of recurrences that surgery triggers is highest at intermediate rates. Margins that extend beyond the halo prevent surgery-triggered recurrence when micrometastases disperse over short distances, but not when they disperse over distances comparable to the halo.

---

## Data and Code Availability

Code and raw results are in the `melanoma_articles/` directory of this repository. `node run_experiments.js a3` regenerates the Monte Carlo results; random seeds are fixed in the driver.

## Competing Interests

The authors declare no competing interests.

---

## References

[1] Read RL, Haydu L, Saw RPM, Quinn MJ, Shannon K, Spillane AJ, et al. In-transit melanoma metastases: incidence, prognosis, and the role of lymphadenectomy. Ann Surg Oncol. 2015;22(2):475–481.

[2] Gershenwald JE, Scolyer RA, Hess KR, Sondak VK, Long GV, Ross MI, et al. Melanoma staging: evidence-based changes in the American Joint Committee on Cancer eighth edition cancer staging manual. CA Cancer J Clin. 2017;67(6):472–492.

[3] MacCormack MA, Cohen LM, Rogers GS. Local melanoma recurrence: a clarification of terminology. Dermatol Surg. 2004;30(12):1533–1538.

[4] Thomas JM, Newton-Bishop J, A'Hern R, Coombes G, Timmons M, Evans J, et al. Excision margins in high-risk malignant melanoma. N Engl J Med. 2004;350(8):757–766.

[5] Hayes AJ, Maynard L, Coombes G, Newton-Bishop J, Timmons M, Cook M, et al. Wide versus narrow excision margins for high-risk, primary cutaneous melanomas: long-term follow-up of survival in a randomised trial. Lancet Oncol. 2016;17(2):184–192.

[6] Swetter SM, Tsao H, Bichakjian CK, Curiel-Lewandrowski C, Elder DE, Gershenwald JE, et al. Guidelines of care for the management of primary cutaneous melanoma. J Am Acad Dermatol. 2019;80(1):208–250.

[7] Eikenberry S, Thalhauser C, Kuang Y. Tumor-immune interaction, surgical treatment, and cancer recurrence in a mathematical model of melanoma. PLoS Comput Biol. 2009;5(4):e1000362.

[8] Azimi F, Scolyer RA, Rumcheva P, Moncrieff M, Murali R, McCarthy SW, et al. Tumor-infiltrating lymphocyte grade is an independent predictor of sentinel lymph node status and survival in patients with cutaneous melanoma. J Clin Oncol. 2012;30(21):2678–2683.
