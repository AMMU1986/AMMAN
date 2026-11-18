# Do Machine-Learning Models of Silica-Fume Self-Compacting Concrete Generalize Across Laboratories? Leakage-Free, Physics-Constrained Prediction of Compressive Strength with Calibrated Uncertainty

**Manuscript type:** Original research article (draft)

**Draft status note:** This draft gives the full study design, methods and analysis plan. Every numerical result that depends on the compiled dataset is marked **[TBD]**. No values have been invented. Fill them in after running the analysis pipeline described in Section 4.

---

## Abstract

Machine-learning (ML) models for the compressive strength of self-compacting concrete (SCC) modified with silica fume (SF) often report coefficients of determination above 0.95. Most of these models are trained and tested on mixes split at random from a database compiled from published studies. Mixes from the same laboratory share cement, aggregates, specimen geometry, testing machines and operators, so a random split places near-duplicate information on both sides of the split and overstates accuracy. Many published regression equations also violate basic physics, for example predicting that strength falls with curing age, and almost none report prediction uncertainty. This study addresses these three problems together. We compile an open, source-tagged database of [TBD] SF-modified SCC mixes from [TBD] independent studies, with harmonized specimen geometry, binder chemistry and curing temperature. We compare random K-fold cross-validation with leave-one-study-out (LOSO) cross-validation for eight models: linear, power-law and pure-quadratic regression, an M5P model tree, random forest, Gaussian process regression, extreme gradient boosting (XGBoost), a monotonicity-constrained XGBoost, and a hybrid model in which XGBoost predicts the parameters of the *fib* Model Code 2010 strength-development law. Prediction intervals are produced with split conformal prediction and conformalized quantile regression calibrated at the study level. Under random splitting the best model reaches R² = [TBD]; under LOSO validation the same model reaches R² = [TBD], a drop of [TBD]. Physical constraints reduce LOSO RMSE by [TBD] MPa and remove all [TBD] physically inconsistent predictions. Study-level conformal intervals reach [TBD]% empirical coverage at a 90% target, with a mean width of [TBD] MPa. Accumulated local effect analysis gives an optimum SF dosage of [TBD] kg/m³ (95% bootstrap interval [TBD]), which shifts with water-to-binder ratio. We argue that LOSO validation, physical consistency checks and calibrated intervals should become minimum reporting standards for data-driven concrete strength models.

**Keywords:** self-compacting concrete; silica fume; compressive strength; data leakage; grouped cross-validation; physics-informed machine learning; monotonic constraints; conformal prediction; uncertainty quantification

---

## 1. Introduction

Self-compacting concrete (SCC) flows under its own weight, fills formwork and passes through congested reinforcement without vibration or segregation [1]. Its fresh-state requirements are codified in terms of slump-flow, viscosity, passing ability and segregation resistance classes [2]. To achieve these properties, SCC uses a high powder content, a low water-to-binder ratio (w/b) and a high-range water-reducing admixture. Silica fume (SF) is a common supplementary cementitious material in SCC. Its sub-micron particles fill voids between cement grains, and its amorphous silica reacts with calcium hydroxide to form additional calcium silicate hydrate. Together these effects densify the paste and the interfacial transition zone [3,4]. SF also raises water demand and paste viscosity, so its benefit to strength depends on how the mix is rebalanced. Experimental studies therefore report a range of optimum SF dosages, and the optimum is expected to depend on w/b, superplasticizer dosage and curing age [3].

Because mix design involves many interacting variables, researchers have turned to data-driven models that learn the relationship between mix proportions and compressive strength from published experiments [5]. For SF-modified SCC, recent studies have compared linear, power-law, quadratic and model-tree regressions [6], and earlier work used neural-network surrogate models [7]. These studies typically compile a few hundred mixes from twenty or more papers, split the mixes at random into training and testing sets, and report R², RMSE and related metrics. For example, Abdulrahman et al. [6] compiled 240 mixes from 20 sources and reported a training R² of 0.98 and a testing R² of 0.83 for an M5P model tree.

Three methodological problems limit how far such results can be trusted.

The first problem is data leakage through study structure. Mixes from the same study share materials, laboratory procedures, specimen geometry and testing equipment. They often differ only in one or two variables, such as SF dosage or curing age. When these mixes are split at random, the test set contains near-copies of training mixes, and the model is evaluated on interpolation within known laboratories rather than prediction for a new laboratory. Leakage of this kind is a recognised cause of inflated performance in applied ML [8,9]. In ecology and other fields with grouped data, blocked or grouped cross-validation is the standard remedy [10]. To our knowledge, no study of SF-modified SCC has reported performance on studies that were entirely withheld from training.

The second problem is physical inconsistency. Concrete strength increases monotonically with curing age under normal moist curing and decreases with w/b at a fixed binder type, following Abrams' law. Unconstrained regressions can violate these relationships. In Abdulrahman et al. [6], the pure-quadratic equation contains a negative coefficient on both curing age and its square. The power-law equation multiplies a power of SF content into the prediction, so it predicts zero strength for every mix without SF. Flexible models such as gradient-boosted trees can also produce non-monotone predictions where data are sparse. A model that predicts lower strength at 90 days than at 28 days for the same mix should not be used for design, whatever its average error. Physics-informed ML offers ways to encode such knowledge as constraints or as model structure [11].

The third problem is the lack of uncertainty estimates. A structural engineer needs to know not only the expected strength but also how far the true strength may fall below it. Point predictions with an average error say little about the error for a particular mix. Conformal prediction produces prediction intervals with a guaranteed coverage rate under an exchangeability assumption, without assuming a distribution for the errors [12,13]. Its use in concrete materials research is still rare, and its guarantees depend on how calibration data are grouped, which matters here because of the study structure described above.

This paper addresses the three problems in one framework. Its contributions are as follows:

1. An open, source-tagged database of SF-modified SCC mixes with harmonized specimen geometry, binder composition, SF properties and curing temperature, released under the FAIR data principles.
2. A direct measurement of the performance gap between random and leave-one-study-out (LOSO) cross-validation for eight model classes, including a replication of the four models in Abdulrahman et al. [6].
3. Two physics-constrained models: a monotonicity-constrained gradient-boosting model and a hybrid model in which ML predicts the parameters of the *fib* Model Code 2010 strength-development function.
4. Study-level conformal prediction intervals, with coverage checked on withheld laboratories.
5. An estimate of the optimum SF dosage with a bootstrap confidence interval, and a test of whether the optimum depends on w/b.

Section 2 reviews the relevant background. Section 3 states the research questions and hypotheses. Section 4 describes the data and methods. Section 5 reports the results, Section 6 discusses them, and Section 7 concludes.

## 2. Background and Related Work

### 2.1 Strength development in silica-fume SCC

The compressive strength of hardened concrete depends mainly on the porosity of the cement paste and the quality of the interfacial transition zone between paste and aggregate [4]. Abrams' law expresses the dominant effect of w/b as f_c = A / B^(w/b), where A and B are empirical constants for a given set of materials and test conditions [14]. Strength increases with age as hydration proceeds. The *fib* Model Code 2010 describes this with the coefficient β_cc(t) = exp{s[1 − (28/t)^0.5]}, so that f_cm(t) = β_cc(t) · f_cm,28. The coefficient s depends on the strength class of the cement and ranges from about 0.20 for rapid-hardening, high-strength cements to 0.38 for slow-hardening cements [15]. Curing temperature changes the rate of hydration. Model Code 2010 accounts for this through a temperature-adjusted age, t_T = Σ Δt_i · exp[13.65 − 4000/(273 + T(Δt_i))], where T is the curing temperature in °C [15].

Silica fume affects strength through three mechanisms: filling of voids between cement particles, nucleation of hydration products, and pozzolanic reaction with calcium hydroxide [3]. The pozzolanic reaction is slower than cement hydration, so SF contributes more to strength at later ages, especially beyond 28 days. At high dosages, SF raises water demand and can cause agglomeration if dispersion is poor. If the superplasticizer dosage is not increased, the mix may need more water or may contain more entrapped air, and strength falls. The net effect is a dosage-response curve that typically rises, peaks and then flattens or declines. Reported optima vary across studies, commonly between about 5% and 15% of binder mass [3,4]. This dependence on other mix variables is why a single study cannot fix the optimum, and why a pooled, multi-study analysis with uncertainty estimates is useful.

### 2.2 Machine learning for concrete strength and evaluation practice

Data-driven prediction of concrete strength dates back at least to the neural-network study of Yeh [16], whose high-performance concrete dataset remains a common benchmark. Reviews describe a steady growth of studies using neural networks, support vector regression, tree ensembles, model trees and hybrid metaheuristic models [5]. The M5 model tree [17], implemented as M5P in the Weka toolkit [18], fits a decision tree whose leaves hold linear regression models. It is popular in concrete research because it yields readable piecewise-linear equations. Ensemble methods such as gradient-boosted trees, particularly XGBoost [19], and random forests [20] usually achieve lower error on tabular data. Gaussian process regression provides predictive variances in addition to point predictions [21].

Ben Chaabene et al. [5] noted that many concrete ML studies share weaknesses: small datasets, random train/test splits, limited hyperparameter tuning reported without nested validation, and few comparisons with simple baselines. Selecting hyperparameters and estimating performance on the same data leads to optimistic estimates, a problem formally analysed by Cawley and Talbot [22]. Nested cross-validation separates the two tasks.

### 2.3 Data leakage and grouped validation

Leakage occurs when information that would not be available at prediction time is present during training or model selection [8]. Kapoor and Narayanan [9] reviewed leakage across ML-based science and listed "non-independence between training and test samples" as a frequent cause of inflated results. In compiled concrete databases the dependence comes from the study. Mixes in one study usually share cement source, aggregate type and grading, specimen size and shape, curing regime, loading rate and operator. The model can therefore learn a study's "signature" from its fixed variables and use it to predict test mixes from the same study.

Roberts et al. [10] showed that when data have hierarchical or spatial structure, random cross-validation underestimates prediction error for new groups, and they recommended blocked or grouped cross-validation that matches the intended use. For a model intended to predict the strength of a new mix made by a different producer or laboratory, the relevant test is performance on studies the model has never seen. Leave-one-study-out cross-validation is the most direct form of this test.

### 2.4 Physics-informed and monotone machine learning

Physics-informed ML includes several ways of combining domain knowledge with learning from data: adding physics-based loss terms, constraining the hypothesis space, and building hybrid models in which a learned component sets the parameters of a mechanistic equation [11]. For tabular regression, monotonic constraints are a simple and effective form of prior knowledge. Monotonic neural networks were introduced by Sill [23], and modern gradient-boosting libraries, including XGBoost, support monotone constraints on chosen input variables [19]. A monotone constraint guarantees that the prediction never decreases (or never increases) as the constrained variable increases, with all other inputs held fixed.

For concrete strength, the most defensible constraints are a non-decreasing response to curing age under moist curing and a non-increasing response to w/b at fixed binder composition. The response to SF content should not be constrained, because a rise-and-fall curve is expected (Section 2.1).

### 2.5 Conformal prediction

Conformal prediction converts any point predictor into a prediction-interval method [12,13]. In split conformal regression, the model is trained on one subset of data, and absolute residuals are computed on a separate calibration subset. If the calibration and test points are exchangeable, an interval of the form [ŷ − q, ŷ + q] covers the true value with probability at least 1 − α. Here q is the ⌈(n + 1)(1 − α)⌉-th smallest calibration residual [24]. Conformalized quantile regression (CQR) uses lower and upper quantile models instead of a symmetric band, so the interval width can vary across the input space [25]. The jackknife+ method extends these guarantees to leave-one-out schemes [26]. When the test distribution differs from the calibration distribution, standard coverage guarantees can fail, and weighted conformal methods have been proposed for covariate shift [27].

For grouped data, the exchangeability assumption should be placed at the level of the group. If whole studies are exchangeable, then calibrating on withheld studies gives valid coverage for a new study. Calibrating on random mixes from studies already in the training set does not give this guarantee.

### 2.6 Interpretation of fitted models

SHAP values attribute each prediction to the input features using Shapley values from cooperative game theory [28]. Accumulated local effect (ALE) plots show how the prediction changes as one feature varies, averaged over the conditional distribution of the other features [29]. ALE plots are preferred over partial dependence plots when inputs are correlated, as they are in concrete mix design: cement content, w/b and superplasticizer dosage are strongly related, as are fine and coarse aggregate contents.

## 3. Research Questions and Hypotheses

The study addresses four research questions (RQ), each with a testable hypothesis (H).

**RQ1. How much does reported accuracy depend on the validation scheme?**
H1: For every model class, LOSO cross-validation gives a higher RMSE and a lower R² than random 10-fold cross-validation. The gap is largest for the most flexible models (M5P, random forest, XGBoost).

**RQ2. Do physical constraints improve prediction for unseen studies?**
H2: Monotone-constrained XGBoost and the hybrid Model Code 2010 model have a LOSO RMSE no worse than unconstrained XGBoost, and they produce zero physically inconsistent predictions on a dense evaluation grid.

**RQ3. Can calibrated prediction intervals be obtained for new laboratories?**
H3: Study-level conformal intervals reach empirical LOSO coverage within ±3 percentage points of the 90% target. Conformal intervals calibrated on random mixes under-cover on withheld studies.

**RQ4. Is there a consistent optimum SF dosage?**
H4: The ALE curve for SF content has an interior maximum. The location of the maximum moves to higher dosages as w/b decreases, provided superplasticizer dosage is sufficient.

## 4. Materials and Methods

### 4.1 Database compilation

**Search protocol.** We search Scopus and Web of Science using the query ("self-compacting concrete" OR "self-consolidating concrete" OR SCC) AND ("silica fume" OR microsilica) AND ("compressive strength"), covering publications from 1995 to 2026. The search is supplemented by backward citation tracking from the reference lists of Abdulrahman et al. [6], Asteris and Kolovos [7], and the review of Siddique [3]. Screening and inclusion follow a PRISMA-style flow diagram, with two independent reviewers and disagreements resolved by discussion.

**Inclusion criteria.** A study is included if it (a) reports SCC that meets at least one EFNARC slump-flow class [2]; (b) includes at least one mix with SF; (c) reports full mix proportions in kg/m³ or values convertible to them; (d) reports compressive strength at a stated age with specimen geometry; and (e) uses standard moist or water curing, or reports the curing temperature. Studies using fibres, recycled aggregates, lightweight aggregates or nanomaterials are recorded but excluded from the main analysis, and they form a separate out-of-distribution test set (Section 4.4).

**Recorded variables.** Table 1 lists the variables recorded for each mix. Each record carries a study identifier, which is the grouping variable for validation.

Table 1. Variables recorded for each mix in the database.

| Group | Variable | Unit | Role |
|---|---|---|---|
| Identification | Study ID, mix ID, publication year, country | – | Grouping and metadata |
| Binder | Cement content, cement strength class (32.5/42.5/52.5, N/R) | kg/m³, – | Input |
| Binder | SF content, SF SiO₂ content, SF specific surface area | kg/m³, %, m²/g | Input |
| Binder | Fly ash, slag and limestone powder contents | kg/m³ | Input |
| Water | Total water, w/b ratio | kg/m³, – | Input |
| Aggregate | Fine and coarse aggregate contents, maximum aggregate size | kg/m³, mm | Input |
| Admixtures | Superplasticizer dosage and type (PCE/SNF), VMA dosage | kg/m³, – | Input |
| Curing | Age at test, curing type, curing temperature | days, –, °C | Input |
| Specimen | Shape (cube/cylinder), size | mm | Harmonization |
| Fresh state | Slump flow, T500, V-funnel time | mm, s, s | Secondary output |
| Hardened | Compressive strength | MPa | Target |

### 4.2 Harmonization

**Specimen geometry.** Strength measured on cubes is higher than strength measured on cylinders of the same concrete, and smaller specimens give higher strength than larger ones [30]. All values are converted to an equivalent 150 × 300 mm cylinder strength. For normal-strength concrete we use the cube-to-cylinder relationships implied by the strength classes in Model Code 2010 [15]. For high-strength concrete, where the ratio approaches 1, we use a strength-dependent conversion. As a sensitivity check, models are also fitted on the subset of mixes tested on 100 mm or 150 mm cubes without conversion, with specimen geometry included as an input.

**Binder composition.** The total binder is the sum of cement, SF and other supplementary materials. We compute w/b from total water, including water from admixtures where reported, and we express SF both in kg/m³ and as a percentage of binder mass. Where SF chemistry is not reported, the SiO₂ content is imputed with the median for the reported product type. An indicator records that the value was imputed.

**Curing temperature.** The temperature-adjusted age t_T is computed with the Model Code 2010 expression given in Section 2.1 [15]. Where curing temperature is not reported for standard water curing, 20 °C is assumed, and an indicator records the assumption. The ASTM C1074 maturity method provides an alternative check for studies with variable temperatures [31].

### 4.3 Data quality control

1. **Unit and transcription checks.** Mix proportions are checked against an absolute-volume balance using reported or typical specific gravities. Records whose total volume deviates from 1 m³ by more than 3% are re-read from the source and corrected or excluded. This step would catch errors such as a cement content entered as 0.455 instead of 455 kg/m³.
2. **Duplicates.** Mixes that appear in more than one publication by the same group are identified by matching proportions and strengths, and only one copy is retained. Duplicates across studies would otherwise leak information even under LOSO validation.
3. **Outliers.** Outliers are flagged with a robust Mahalanobis distance on the inputs and with study-level residuals from a simple baseline model. Flagged records are re-checked against the source but are not removed only because they are extreme.
4. **Reporting completeness.** Each study is scored for reporting completeness (0–10). The score is used in a sensitivity analysis that excludes the least complete studies.

### 4.4 Validation design

Three validation schemes are compared for every model.

**Scheme A: random 10-fold cross-validation**, repeated five times with different random seeds. This mirrors common practice in the literature, including the random two-thirds/one-third split in Abdulrahman et al. [6].

**Scheme B: leave-one-study-out (LOSO) cross-validation.** In each fold, all mixes from one study form the test set and all other studies form the training set. Performance is computed on the pooled out-of-fold predictions and also as the median over studies, so that large studies do not dominate.

**Scheme C: grouped 5-fold cross-validation**, with whole studies assigned to folds and fold sizes balanced by number of mixes. Scheme C gives lower-variance estimates than LOSO when some studies are very small.

**Nested tuning.** In all schemes, hyperparameters are tuned in an inner loop that follows the same grouping as the outer loop. For example, under LOSO the inner loop uses grouped 5-fold cross-validation over the training studies. This prevents optimistic bias from model selection [22]. Tuning uses Bayesian optimization with the tree-structured Parzen estimator in Optuna [32], with 100 trials per outer fold.

**Out-of-distribution test.** Models trained on the full main dataset are also applied to the separate set of fibre-reinforced and recycled-aggregate SF-SCC mixes (Section 4.1). This measures how performance degrades outside the training domain and tests whether the conformal intervals widen or under-cover in that setting.

**Leakage gap.** For each model and metric, the leakage gap is defined as Δ = metric(Scheme B) − metric(Scheme A). The uncertainty of Δ is estimated by a study-level bootstrap with 2,000 resamples of studies.

### 4.5 Models

Eight models are compared. All use the same inputs: cement, SF, other supplementary materials, w/b, fine aggregate, coarse aggregate, maximum aggregate size, superplasticizer and temperature-adjusted age (log-transformed). Cement class and SF SiO₂ content are included where the reporting allows. Inputs are scaled with min–max scaling fitted inside each training fold only.

**M1. Linear regression (LR)**, as in Equation 2 of [6].

**M2. Power-law regression**, the model called "MLR" in [6]. To avoid the zero-SF singularity, SF enters as (1 + SF), and all other inputs are strictly positive in raw units.

**M3. Pure-quadratic regression (PQ)**, with ridge regularization tuned in the inner loop.

**M4. M5P model tree** [17,18], with the minimum number of instances per leaf tuned.

**M5. Random forest** [20].

**M6. Gaussian process regression** [21] with an automatic relevance determination Matérn-5/2 kernel plus a white-noise term.

**M7. XGBoost** [19], unconstrained.

**M8a. Monotone XGBoost.** This is M7 with monotone constraints: non-decreasing in temperature-adjusted age and non-increasing in w/b. No constraint is placed on SF content.

**M8b. Hybrid Model Code 2010 model.** Strength is written as

f_c(x, t_T) = f_28(x) · exp{ s(x) · [1 − (28 / t_T)^0.5] },

where x is the vector of mix inputs without age. Two XGBoost regressors predict log f_28(x) and the logit-scaled parameter s(x). The parameter s is bounded to the interval [0.10, 0.50], which contains the Model Code values for all cement classes [15]. The f_28 regressor is monotone non-increasing in w/b. The two regressors are trained jointly by gradient boosting on the custom loss L = Σ (f_c,obs − f_c,pred)², using the analytical gradients of the expression above. Because s(x) > 0, the predicted strength is guaranteed to increase with age for every mix. The model also extrapolates sensibly beyond the ages in the training data, and its learned s(x) can be compared with the Model Code values as a physical check.

In the hybrid model, the age effect of SF is captured by s(x). This allows the model to learn that mixes with more SF gain a larger share of their strength after 28 days, which is the expected effect of the slower pozzolanic reaction.

**Baseline.** A study-mean baseline predicts, for each test mix, the mean strength of the training mixes with the nearest w/b and age. It sets a floor for useful performance.

### 4.6 Uncertainty quantification

Prediction intervals with a nominal coverage of 1 − α = 0.90 are constructed in four ways.

**U1. Random split conformal.** Calibration mixes are drawn at random from the training studies. This method is included to show what happens when the calibration set has the same leakage as a random test split.

**U2. Study-level split conformal.** Calibration uses all mixes from a random 20% of the training studies. Each calibration study contributes the maximum absolute residual over its mixes, a conservative choice that treats the study as the exchangeable unit. The interval half-width q is the ⌈(m + 1)(1 − α)⌉-th smallest of the m study scores.

**U3. Study-level conformalized quantile regression (CQR).** Lower and upper quantile XGBoost models (α/2 and 1 − α/2), trained with the monotone constraints of M8a, are calibrated with the CQR score [25] on held-out studies. Intervals can then be wider where data are sparse or noisy.

**U4. Gaussian process intervals** from M6, used without conformal correction as a model-based comparison.

**Conditional coverage by strength class.** Marginal coverage can hide poor coverage in high-strength mixes. We therefore also report coverage within bands of the *predicted* strength (< 40, 40–60, > 60 MPa), and a Mondrian version of U3 that calibrates separately within each predicted band. Binning by the predicted value, rather than the measured value, keeps the procedure usable at prediction time.

All intervals are evaluated under LOSO validation, so that every test study is a laboratory the model has not seen.

### 4.7 Performance metrics

**Point accuracy.** R², RMSE, MAE and the a20-index. The a20-index is defined as the fraction of predictions whose predicted-to-measured ratio lies between 0.8 and 1.2, so it is bounded between 0 and 1. The mean predicted-to-measured ratio is reported separately as a bias measure.

**Interval quality.** Empirical coverage, mean interval width, and the interval score of Gneiting and Raftery [33]:

IS_α(l, u; y) = (u − l) + (2/α)(l − y)·1{y < l} + (2/α)(y − u)·1{y > u}.

The interval score rewards narrow intervals and penalizes misses in proportion to their size.

**Physical consistency.** For each test mix, predictions are computed on a grid of ages (1, 3, 7, 14, 28, 56, 90, 180 and 365 days) and of w/b values (±0.05 around the actual value in steps of 0.01), with other inputs fixed. The violation rate is the fraction of mixes with any decrease in predicted strength with age, or any increase with w/b, larger than 0.1 MPa.

**Characteristic-strength risk.** For design use, the most important error is overprediction of strength. We report the fraction of test mixes whose measured strength falls below the lower bound of the 90% interval, which by construction should be about 5%.

### 4.8 Statistical comparison of models

Differences between models under LOSO are tested with the Wilcoxon signed-rank test on per-study RMSE, with Holm correction for multiple comparisons. Under repeated random cross-validation, the corrected resampled t-test of Nadeau and Bengio [34] is used, because standard t-tests underestimate variance when training sets overlap.

### 4.9 Interpretation and optimum SF dosage

SHAP values [28] are computed for the best-performing model under LOSO and summarized as mean absolute contribution per feature. Because inputs are correlated, ALE curves [29] are used for the effect of SF content. The optimum SF dosage is defined as the location of the maximum of the ALE curve within the range covered by at least 5% of the data. Its uncertainty is estimated with a study-level bootstrap: studies are resampled with replacement 1,000 times, the model is refitted, and the optimum is recomputed each time.

To test H4, two-dimensional ALE surfaces for SF × w/b are computed, and the optimum is located separately within w/b terciles. The interaction is considered supported if the bootstrap intervals for the optimum in the lowest and highest w/b terciles do not overlap.

### 4.10 Replication of earlier results

The four models of Abdulrahman et al. [6] (LR, power-law, PQ and M5P) are refitted on the subset of our database drawn from their 20 source studies. They are evaluated first with a random two-thirds/one-third split, as in the original, and then with LOSO validation. This shows how much of the originally reported accuracy remains under study-level validation, without relying on the original authors' data, which are available only on request.

### 4.11 Implementation and reproducibility

The analysis is implemented in Python with scikit-learn [35], XGBoost [19] and Optuna [32]. M5P is run through the Weka implementation [18] via a Python wrapper. All random seeds are fixed and recorded. The database, its data dictionary, the screening log and the analysis code will be released in a public repository with a persistent identifier, following the FAIR principles [36].

## 5. Results

**Note on this section:** The structure, tables and analyses below are fixed in advance. Values marked [TBD] are filled in from the pipeline output. The text states which result would support or reject each hypothesis, so the conclusions cannot be adjusted after the results are seen.

### 5.1 Database description

The search returned [TBD] records. After screening, [TBD] studies met the inclusion criteria, giving [TBD] mixes in the main dataset and [TBD] mixes in the out-of-distribution set. The number of mixes per study ranges from [TBD] to [TBD] (median [TBD]). Table 2 summarizes the main variables.

Table 2. Summary statistics of the main dataset.

| Variable | Min | Median | Max | Mean | SD |
|---|---|---|---|---|---|
| Cement (kg/m³) | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| SF (kg/m³) | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| SF (% of binder) | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| w/b | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| Fine aggregate (kg/m³) | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| Coarse aggregate (kg/m³) | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| Superplasticizer (kg/m³) | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| Age (days) | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| Equivalent cylinder strength (MPa) | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |

Quality control corrected [TBD] records and removed [TBD] cross-publication duplicates. Between-study variance accounts for [TBD]% of the total variance in strength after adjusting for w/b and age with a mixed-effects baseline. This intraclass correlation measures how much study structure there is to leak.

### 5.2 Effect of the validation scheme (RQ1)

Table 3 compares point accuracy under random 10-fold and LOSO cross-validation.

Table 3. Point accuracy under random and leave-one-study-out cross-validation.

| Model | R² random | R² LOSO | RMSE random (MPa) | RMSE LOSO (MPa) | Leakage gap ΔRMSE (95% CI) |
|---|---|---|---|---|---|
| Baseline | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| M1 LR | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| M2 Power law | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| M3 PQ | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| M4 M5P | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| M5 Random forest | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| M6 GPR | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| M7 XGBoost | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| M8a Monotone XGBoost | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| M8b Hybrid MC2010 | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |

H1 is supported if the leakage gap is positive with a confidence interval above zero for every model, and if the gap for M4, M5 and M7 is larger than for M1–M3. Model rankings under the two schemes are compared with Kendall's τ. A low τ would mean that conclusions about which model is "best", as drawn in earlier studies, depend on the validation scheme.

The replication of Abdulrahman et al. (Section 4.10) gives a random-split testing R² for M5P of [TBD], compared with 0.83 in the original paper. Under LOSO it gives [TBD].

### 5.3 Effect of physical constraints (RQ2)

Table 4 reports LOSO accuracy and physical consistency for the flexible models.

Table 4. LOSO accuracy and physical consistency.

| Model | RMSE LOSO (MPa) | MAE LOSO (MPa) | Age violations (% of mixes) | w/b violations (% of mixes) | Out-of-distribution RMSE (MPa) |
|---|---|---|---|---|---|
| M3 PQ | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| M4 M5P | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| M7 XGBoost | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| M8a Monotone XGBoost | [TBD] | [TBD] | 0 (by construction) | 0 (by construction) | [TBD] |
| M8b Hybrid MC2010 | [TBD] | [TBD] | 0 (by construction) | 0 (by construction) | [TBD] |

H2 is supported if the Wilcoxon test finds no significant increase in per-study RMSE for M8a and M8b relative to M7. A significant decrease would be stronger evidence that the constraints help generalization. For the hybrid model, the distribution of learned s(x) values is compared with the Model Code range of 0.20–0.38. Its correlation with SF content is also reported: a positive correlation would show that the model has learned the delayed strength gain from the pozzolanic reaction.

### 5.4 Prediction intervals (RQ3)

Table 5 reports interval performance under LOSO at a nominal coverage of 90%.

Table 5. Prediction interval performance under LOSO validation (nominal coverage 90%).

| Method | Coverage (%) | Mean width (MPa) | Interval score | Coverage < 40 MPa | Coverage 40–60 MPa | Coverage > 60 MPa | Below lower bound (%) |
|---|---|---|---|---|---|---|---|
| U1 Random conformal | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| U2 Study-level conformal | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| U3 Study-level CQR | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| U3 Mondrian CQR | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| U4 GPR intervals | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |

H3 is supported if U2 and U3 achieve coverage between 87% and 93% and U1 shows lower coverage. The out-of-distribution set gives an additional check: coverage is expected to fall there, and the size of the fall shows how far the intervals can be trusted outside the training domain.

### 5.5 Effect of silica fume (RQ4)

The ALE curve for SF content from the best LOSO model peaks at [TBD] kg/m³ ([TBD]% of binder), with a 95% bootstrap interval of [TBD]. The strength gain at the optimum relative to zero SF is [TBD] MPa at 28 days and [TBD] MPa at 90 days. Within w/b terciles, the optimum is [TBD] for w/b ≤ [TBD], [TBD] for the middle tercile and [TBD] for w/b ≥ [TBD]. H4 is supported if the curve has an interior maximum and the intervals for the lowest and highest terciles do not overlap.

The mean absolute SHAP values rank the inputs as follows: [TBD]. Age and w/b are expected to rank highest, consistent with Model Code 2010 and Abrams' law. A high SHAP rank for variables that mainly identify a study, such as fixed aggregate contents, would indicate that the model under random validation was learning study signatures. We test this by comparing SHAP rankings for models fitted under random and LOSO training folds.

## 6. Discussion

### 6.1 What the validation gap means

The central question of this study is not which algorithm is best, but what a reported accuracy figure actually measures. A random split measures how well a model interpolates between mixes from laboratories it has already seen. LOSO measures how well it predicts for a laboratory it has not seen. For practical use, such as a producer checking a new mix design or a designer estimating strength before trial batches, the second figure is the relevant one.

Two features of compiled concrete databases make the gap likely to be large. First, studies are internally homogeneous. Many contribute a grid of SF dosages crossed with ages, using one cement, one aggregate and one specimen type. Second, those fixed variables can act as study identifiers. In the database of Abdulrahman et al. [6], for example, many studies report a single value of fine and coarse aggregate content. A tree model can then use the aggregate contents to identify the study and recover its strength level, without learning anything about how aggregates affect strength. This may explain why that study found coarse aggregate content to have a strong negative correlation with strength (r = −0.61), a stronger relationship than material science would lead one to expect. If the leakage gap is large and the SHAP importance of such variables drops under LOSO training, that would support this explanation.

Whatever the size of the measured gap, the cost of reporting LOSO results is small. It requires only that each mix carry a study identifier, which every compiled database already has implicitly. We recommend that journals ask for grouped validation results alongside random-split results for any model trained on multi-source data.

### 6.2 Value of physical constraints

Physical constraints serve two purposes. The first is credibility: a model that predicts falling strength with age, or rising strength with more water, will not be trusted by engineers, even if its average error is small. Constraints remove these failures by construction. The second purpose is generalization. When a model is applied to a new laboratory, it must extrapolate from patterns in other laboratories. Constraints reduce the set of functions the model can learn and are expected to reduce variance where data are sparse, which is exactly the situation under LOSO.

The hybrid Model Code 2010 model goes further. It separates the question "how strong will this mix be at 28 days?" from "how fast does it gain strength?" The second question has a well-established engineering answer, and the model needs to learn only how mix composition shifts the parameter s. This reduces the amount of data needed to learn the age effect and allows predictions at ages not in the training data, such as 365 days, without the unbounded extrapolation of polynomial models. The learned s(x) values also provide a physical check: if they fall far outside the Model Code range, either the data or the model needs examination.

The constraints chosen here are deliberately limited. We did not constrain the response to cement content, because at fixed w/b more cement means more paste and possibly more shrinkage cracking, and its net effect is not clearly monotonic. We did not constrain the response to SF, because the expected dosage-response curve rises and then falls. Stronger constraints are possible, such as a concave response to SF, but each additional assumption should be justified and tested.

### 6.3 Using prediction intervals in practice

A 90% prediction interval for a new laboratory has a direct engineering interpretation. If the lower bound is below the required mean strength for the target class, the mix should be confirmed by trial batches before use. The lower bound is therefore more useful than the point prediction for screening. Because the characteristic strength in design codes is a lower fractile, a model that reports only the mean cannot support a design decision.

Calibration must match the intended use. If intervals are calibrated on random mixes, they inherit the same leakage as random test splits and are expected to be too narrow for new laboratories. Study-level calibration makes the intervals honest about between-laboratory variation, which includes differences in materials, curing and testing that the inputs do not fully capture. The resulting intervals will often be wide. A wide but honest interval is more useful than a narrow one that misses the true value more often than stated, because it shows how much of strength variation cannot yet be explained by reported mix proportions.

Width also points to how the data could be improved. If between-laboratory variation dominates, then better reporting of cement chemistry, SF fineness, aggregate type and testing details would reduce interval width more than collecting more mixes of the same kind. This is a concrete argument for richer reporting standards in experimental papers.

### 6.4 The silica fume optimum

Single studies usually test three to five SF dosages, so they cannot estimate the location of an optimum precisely or test whether it depends on other variables. A pooled analysis can, provided it accounts for the study structure. The study-level bootstrap used here reflects the fact that the information in the database comes from a limited number of laboratories, not from independent mixes. A dependence of the optimum on w/b would be consistent with the mechanism described in Section 2.1: at lower w/b, the increased water demand of SF is compensated by superplasticizer, and the filler and pozzolanic benefits can be exploited at higher dosages.

The analysis also corrects an error in earlier work. In Abdulrahman et al. [6], the quadratic model curves show a shallow maximum near 50–60 kg/m³ followed by a decline, but the text and conclusions report only a decrease with increasing SF. Estimating the optimum with a confidence interval, and testing whether it is an interior maximum, avoids reading a non-monotone curve as monotone.

### 6.5 Limitations

1. **Publication and selection bias.** Compiled databases contain mixes that researchers chose to make and publish. Unusual or failed mixes are under-represented, which narrows the input space and may bias the SF optimum toward dosages that worked well in published studies.
2. **Harmonization error.** Conversion of cube to cylinder strength, and imputation of missing curing temperatures and SF properties, add error that the model cannot separate from real variation. Indicator variables and sensitivity analyses limit, but do not remove, this effect.
3. **Exchangeability of studies.** Study-level conformal guarantees assume that a new laboratory is drawn from the same population as the laboratories in the database. A producer using unusual local materials may fall outside this population. The out-of-distribution test shows how coverage behaves in such cases, and weighted conformal methods for covariate shift [27] are a possible extension.
4. **Unequal study sizes.** A few large studies may dominate training. We report per-study median metrics and grouped 5-fold results to check that conclusions are not driven by a small number of studies.
5. **Missing variables.** Cement chemistry, aggregate mineralogy, air content and testing details such as loading rate are reported inconsistently. Their absence limits achievable accuracy for any model, and part of the between-study variation will remain unexplained.
6. **Causal interpretation.** ALE and SHAP describe the fitted model, not causal effects. The SF optimum should be read as a data-supported hypothesis to be confirmed with designed experiments, such as a dosage series at several w/b ratios in one laboratory.

### 6.6 Recommendations for future data-driven concrete studies

Based on the framework above, we propose a minimum reporting checklist for ML models of concrete strength trained on compiled data:

1. Publish the database with a study identifier for every record, together with a data dictionary and screening log.
2. Report grouped (study-level) validation results alongside any random-split results.
3. Tune hyperparameters with nested validation that follows the same grouping.
4. Compare against simple baselines, including a study-mean or Abrams-law model.
5. Check predictions for physical consistency with age and w/b on a dense grid, and report the violation rate.
6. Report calibrated prediction intervals, with coverage measured on withheld studies.
7. Define metrics correctly. For example, the a20-index is a fraction between 0 and 1. Report bias separately.
8. Interpret correlated inputs with ALE rather than partial dependence, and report bootstrap intervals for derived quantities such as optimum dosages.

## 7. Conclusions

This study set out a framework for testing whether machine-learning models of SF-modified SCC compressive strength generalize to new laboratories, whether physical constraints help them do so, and whether their uncertainty can be stated honestly. The main conclusions are:

1. The validation scheme strongly affects reported accuracy. Under random cross-validation the best model reached R² = [TBD]. Under leave-one-study-out validation it reached R² = [TBD]. Random splitting of compiled databases should not be the only reported evaluation.
2. Monotonic constraints on age and w/b, and a hybrid model built on the *fib* Model Code 2010 strength-development law, removed all physically inconsistent predictions. They changed LOSO RMSE by [TBD] MPa relative to the unconstrained model.
3. Prediction intervals calibrated at the study level reached [TBD]% coverage at a 90% target on withheld laboratories, with a mean width of [TBD] MPa. Intervals calibrated on random mixes reached only [TBD]%.
4. The estimated optimum SF dosage was [TBD] kg/m³ (95% interval [TBD]), and it [TBD: did/did not] shift with w/b.
5. Re-evaluating the four models of Abdulrahman et al. [6] under LOSO reduced the M5P testing R² from [TBD] to [TBD].

The database, code and checklist are released so that other researchers can apply the same evaluation to new SCC datasets. Future work should extend the framework to fresh-state properties and embodied carbon, and should test the predicted optimum SF dosages with designed experiments in independent laboratories.

---

## Data Availability Statement

The compiled database, data dictionary, PRISMA screening log and analysis code will be deposited in a public repository with a persistent identifier on acceptance [TBD: repository and DOI].

## Author Contributions

[TBD: CRediT roles]

## Funding

[TBD]

## Conflict of Interest

The authors declare no competing interests. [TBD: confirm]

---

## References

[1] Okamura H, Ouchi M. Self-compacting concrete. J Adv Concr Technol. 2003;1(1):5–15.

[2] EFNARC. The European guidelines for self-compacting concrete: specification, production and use. Farnham, UK: EFNARC; 2005.

[3] Siddique R. Utilization of silica fume in concrete: review of hardened properties. Resour Conserv Recycl. 2011;55(11):923–32.

[4] Mehta PK, Monteiro PJM. Concrete: microstructure, properties, and materials. 4th ed. New York: McGraw-Hill Education; 2014.

[5] Ben Chaabene W, Flah M, Nehdi ML. Machine learning prediction of mechanical properties of concrete: critical review. Constr Build Mater. 2020;260:119889.

[6] Abdulrahman PI, Jaf DKI, Malla SK, Mohammed AS, Kurda R, Asteris PG, et al. Predictive modeling of compressive strength in silica fume-modified self-compacted concrete: a soft computing approach. Struct Concr. 2025;26(3):2340–65.

[7] Asteris PG, Kolovos KG. Self-compacting concrete strength prediction using surrogate models. Neural Comput Appl. 2019;31(Suppl 1):409–24.

[8] Kaufman S, Rosset S, Perlich C, Stitelman O. Leakage in data mining: formulation, detection, and avoidance. ACM Trans Knowl Discov Data. 2012;6(4):15.

[9] Kapoor S, Narayanan A. Leakage and the reproducibility crisis in machine-learning-based science. Patterns. 2023;4(9):100804.

[10] Roberts DR, Bahn V, Ciuti S, Boyce MS, Elith J, Guillera-Arroita G, et al. Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography. 2017;40(8):913–29.

[11] Karniadakis GE, Kevrekidis IG, Lu L, Perdikaris P, Wang S, Yang L. Physics-informed machine learning. Nat Rev Phys. 2021;3(6):422–40.

[12] Vovk V, Gammerman A, Shafer G. Algorithmic learning in a random world. New York: Springer; 2005.

[13] Angelopoulos AN, Bates S. Conformal prediction: a gentle introduction. Found Trends Mach Learn. 2023;16(4):494–591.

[14] Abrams DA. Design of concrete mixtures. Bulletin 1. Chicago: Structural Materials Research Laboratory, Lewis Institute; 1919.

[15] Fédération internationale du béton (fib). fib Model Code for Concrete Structures 2010. Berlin: Ernst & Sohn; 2013.

[16] Yeh IC. Modeling of strength of high-performance concrete using artificial neural networks. Cem Concr Res. 1998;28(12):1797–808.

[17] Quinlan JR. Learning with continuous classes. In: Proceedings of the 5th Australian Joint Conference on Artificial Intelligence. Singapore: World Scientific; 1992. p. 343–8.

[18] Wang Y, Witten IH. Inducing model trees for continuous classes. In: Proceedings of the 9th European Conference on Machine Learning, Poster Papers. Prague; 1997. p. 128–37.

[19] Chen T, Guestrin C. XGBoost: a scalable tree boosting system. In: Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining. New York: ACM; 2016. p. 785–94.

[20] Breiman L. Random forests. Mach Learn. 2001;45(1):5–32.

[21] Rasmussen CE, Williams CKI. Gaussian processes for machine learning. Cambridge, MA: MIT Press; 2006.

[22] Cawley GC, Talbot NLC. On over-fitting in model selection and subsequent selection bias in performance evaluation. J Mach Learn Res. 2010;11:2079–107.

[23] Sill J. Monotonic networks. In: Advances in Neural Information Processing Systems 10. Cambridge, MA: MIT Press; 1998. p. 661–7.

[24] Lei J, G'Sell M, Rinaldo A, Tibshirani RJ, Wasserman L. Distribution-free predictive inference for regression. J Am Stat Assoc. 2018;113(523):1094–111.

[25] Romano Y, Patterson E, Candès E. Conformalized quantile regression. In: Advances in Neural Information Processing Systems 32. 2019. p. 3543–53.

[26] Barber RF, Candès EJ, Ramdas A, Tibshirani RJ. Predictive inference with the jackknife+. Ann Stat. 2021;49(1):486–507.

[27] Tibshirani RJ, Barber RF, Candès EJ, Ramdas A. Conformal prediction under covariate shift. In: Advances in Neural Information Processing Systems 32. 2019. p. 2530–40.

[28] Lundberg SM, Lee SI. A unified approach to interpreting model predictions. In: Advances in Neural Information Processing Systems 30. 2017. p. 4765–74.

[29] Apley DW, Zhu J. Visualizing the effects of predictor variables in black box supervised learning models. J R Stat Soc Series B Stat Methodol. 2020;82(4):1059–86.

[30] Neville AM. Properties of concrete. 5th ed. Harlow, UK: Pearson Education; 2011.

[31] ASTM International. ASTM C1074-19: Standard practice for estimating concrete strength by the maturity method. West Conshohocken, PA: ASTM International; 2019.

[32] Akiba T, Sano S, Yanase T, Ohta T, Koyama M. Optuna: a next-generation hyperparameter optimization framework. In: Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining. New York: ACM; 2019. p. 2623–31.

[33] Gneiting T, Raftery AE. Strictly proper scoring rules, prediction, and estimation. J Am Stat Assoc. 2007;102(477):359–78.

[34] Nadeau C, Bengio Y. Inference for the generalization error. Mach Learn. 2003;52(3):239–81.

[35] Pedregosa F, Varoquaux G, Gramfort A, Michel V, Thirion B, Grisel O, et al. Scikit-learn: machine learning in Python. J Mach Learn Res. 2011;12:2825–30.

[36] Wilkinson MD, Dumontier M, Aalbersberg IJ, Appleton G, Axton M, Baak A, et al. The FAIR Guiding Principles for scientific data management and stewardship. Sci Data. 2016;3:160018.
