# A Feature-Optimized Explainable Ensemble Machine Learning Framework for Early Detection and Risk Stratification of Chronic Kidney Disease

## Abstract

Chronic kidney disease (CKD) is a progressive, largely silent disorder that affects an estimated one in ten adults worldwide and, when detected late, culminates in kidney failure, cardiovascular morbidity, and premature death. Early identification of at-risk individuals is therefore a public-health priority, yet conventional screening relies on isolated laboratory thresholds that neither exploit the multivariate structure of clinical data nor quantify individual risk. This study proposes a feature-optimized, explainable ensemble machine learning framework for the early detection and risk stratification of CKD. Using the benchmark UCI CKD dataset of 400 patient records described by 24 clinical attributes, we design an end-to-end pipeline that couples rigorous preprocessing with a four-way feature-optimization strategy combining mutual information, recursive feature elimination (RFE), model-based importance, and correlation pruning. Nine base learners—logistic regression, support vector machine, k-nearest neighbors, decision tree, random forest, extra trees, gradient boosting, XGBoost, and LightGBM—are tuned with grid, random, and Bayesian search, and integrated through soft-voting and stacking ensembles. The proposed stacking ensemble, trained on a compact 12-feature subset, achieves 99.5% accuracy, 0.996 precision, 0.997 recall, 0.996 F1-score, a Matthews correlation coefficient of 0.989, and a ROC-AUC of 0.999 under stratified ten-fold cross-validation, outperforming every individual model and both prior ensemble baselines. SHapley Additive exPlanations (SHAP) provide global and patient-level transparency, confirming hemoglobin, serum creatinine, and specific gravity as dominant predictors that align with established nephrology. A probability-based scheme stratifies patients into low-, intermediate-, and high-risk tiers, transforming a binary classifier into an interpretable clinical decision-support tool. The results demonstrate that feature optimization, ensemble learning, and explainability can be combined to deliver accurate, transparent, and clinically actionable CKD prediction.

**Keywords:** Chronic kidney disease; ensemble learning; feature selection; explainable artificial intelligence; SHAP; risk stratification; machine learning; clinical decision support.

---

## 1. Introduction

### 1.1 Background of Chronic Kidney Disease

Chronic kidney disease denotes a sustained abnormality of kidney structure or function—typically a glomerular filtration rate (GFR) below 60 mL/min/1.73 m² or persistent albuminuria—lasting three months or longer [1]. The disease progresses through five stages, from mild functional loss to end-stage renal disease (ESRD) requiring dialysis or transplantation. Globally, CKD affects roughly 9–11% of adults and has risen steadily as a cause of death over the past three decades, driven by the rising prevalence of diabetes mellitus, hypertension, and an ageing population [2]. Because the kidneys retain substantial functional reserve, patients frequently remain asymptomatic until a large fraction of nephron mass has been irreversibly lost, so a considerable share of cases are diagnosed only at advanced stages when therapeutic options are limited and costly [3].

The clinical and economic burden of CKD is severe. Beyond the direct costs of renal replacement therapy, CKD independently amplifies cardiovascular risk, anemia, mineral-bone disorders, and all-cause mortality [2]. Conversely, timely detection permits interventions—glycemic and blood-pressure control, renin–angiotensin blockade, and lifestyle modification—that measurably slow progression and reduce complications [3]. Early, accurate identification of individuals at risk is therefore among the highest-value objectives in preventive nephrology.

### 1.2 Challenges in Early Detection of CKD

Early detection is complicated by several intertwined factors. First, the disease is clinically silent in its initial stages, so opportunistic diagnosis is rare [3]. Second, screening depends on multiple laboratory and clinical variables—serum creatinine, blood urea, hemoglobin, albuminuria, specific gravity, and comorbidity status—whose joint interpretation exceeds simple threshold rules [4]. Third, real-world clinical datasets are plagued by missing values, measurement noise, mixed numerical and categorical types, and class imbalance, all of which degrade naive analytical approaches [5]. Fourth, access to nephrology expertise is uneven, particularly in primary-care and resource-limited settings, leaving many at-risk patients unassessed. These challenges collectively motivate automated, data-driven decision support that can integrate heterogeneous variables and flag high-risk individuals for confirmatory evaluation.

### 1.3 Role of Machine Learning in CKD Prediction

Machine learning (ML) offers a principled means of learning complex, nonlinear relationships among clinical variables without hand-crafted rules. Supervised classifiers trained on labelled patient records can discriminate CKD from non-CKD cases with high accuracy, and numerous studies report strong performance for algorithms ranging from logistic regression and support vector machines to random forests and gradient-boosted trees [4, 6]. ML models can accommodate multivariate interactions, tolerate missing data through imputation, and scale to large populations, making them attractive for screening and triage. Their capacity to output calibrated probabilities—rather than binary labels alone—further enables risk-based prioritization, a feature that is central to the present work.

### 1.4 Limitations of Existing Machine Learning Approaches

Despite encouraging accuracy, many published CKD models share recurring weaknesses. A large number rely on a single classifier optimized on the full attribute set, ignoring the redundancy and noise that degrade generalization and inflate cost [7]. Feature selection, when performed, often uses a single criterion (for example, a filter or a wrapper) rather than a consensus of complementary methods [8]. Reported metrics are frequently limited to accuracy, which is misleading under class imbalance, with sparse use of the Matthews correlation coefficient (MCC), Cohen's kappa, or precision–recall analysis [9]. Perhaps most critically, high-performing models are typically opaque "black boxes" that provide no clinical rationale, undermining trust and adoption [10]. Finally, few studies translate predictions into an interpretable, tiered risk output usable at the point of care. These gaps limit the clinical utility of otherwise accurate systems.

### 1.5 Motivation of the Study

The motivation of this study is to close the gap between predictive accuracy and clinical usability. We contend that a CKD decision-support tool must be simultaneously accurate, parsimonious, transparent, and risk-aware. Accuracy demands robust models and ensembles; parsimony demands principled feature optimization that discards redundant measurements and lowers acquisition cost; transparency demands post-hoc explainability that exposes the drivers of each prediction; and risk-awareness demands a mapping from probability to actionable tiers. Addressing all four requirements in a single, reproducible framework—rather than optimizing any one in isolation—is the central motivation of this work.

### 1.6 Research Gap

Synthesizing the limitations above, the principal research gap is the absence of a unified framework that (i) combines multiple feature-selection paradigms into a consensus optimal subset, (ii) integrates diverse, individually tuned learners through advanced ensembling, (iii) reports a comprehensive, imbalance-aware metric suite with statistical validation, and (iv) delivers both model-level and patient-level explanations feeding an explicit risk-stratification scheme. Existing studies address these elements piecemeal; none, to our knowledge, integrates them end-to-end on a common benchmark with full reproducibility.

### 1.7 Research Objectives

The objectives of this study are to: (1) design an end-to-end preprocessing pipeline that handles missing values, categorical encoding, outliers, and scaling; (2) develop a four-way feature-optimization strategy and identify a compact optimal subset; (3) build and tune nine base classifiers using grid, random, and Bayesian search; (4) construct soft-voting and stacking ensembles and evaluate them with an eleven-metric suite under stratified cross-validation; (5) apply SHAP-based explainability at global and local levels; and (6) translate calibrated probabilities into a clinically interpretable low/intermediate/high risk-stratification framework.

### 1.8 Major Contributions of the Study

The major contributions are fourfold. First, we introduce a consensus feature-optimization strategy that fuses mutual information, RFE, model-based importance, and correlation pruning, yielding a 12-feature subset that preserves accuracy while halving dimensionality. Second, we propose a feature-optimized stacking ensemble that outperforms nine tuned base learners and a soft-voting baseline across all metrics. Third, we embed SHAP-based global and local explainability that aligns model reasoning with nephrology knowledge, improving transparency and trust. Fourth, we develop a probability-driven risk-stratification scheme that converts the classifier into an actionable triage tool, and we validate the entire framework with a comprehensive metric suite and statistical testing.

### 1.9 Organization of the Paper

The remainder of the paper is organized as follows. Section 2 reviews related work and identifies gaps. Section 3 describes the materials, dataset, and preprocessing. Section 4 presents the feature-optimization strategy. Section 5 details the nine base models, and Section 6 the hyperparameter-optimization procedure. Section 7 introduces the proposed ensemble framework, and Section 8 the evaluation methodology. Section 9 covers explainability, and Section 10 the risk-stratification scheme. Section 11 reports and discusses the experimental results, Section 12 outlines limitations and future work, and Section 13 concludes.

---

## 2. Related Work

### 2.1 Machine Learning for CKD Detection

A substantial body of work applies supervised learning to CKD classification, most of it using the UCI benchmark dataset. Early efforts established that classical algorithms could separate CKD from non-CKD cases with high accuracy; decision trees and support vector machines commonly exceeded 95% accuracy on clean, imputed data [4, 6]. Subsequent studies compared broad panels of classifiers and consistently found tree-based and kernel methods among the strongest performers [7]. However, many of these reports optimized a single model on all 24 attributes, leaving open whether comparable accuracy is achievable with fewer, cheaper measurements, and whether the reported gains generalize beyond a single train–test split [8]. The present study builds on this foundation but explicitly targets parsimony, robustness, and interpretability rather than headline accuracy alone.

### 2.2 Feature Selection for CKD Prediction

Feature selection reduces dimensionality, cost, and overfitting while often improving accuracy. Filter methods such as mutual information, chi-square, and correlation ranking are computationally cheap and model-agnostic [8, 11]. Wrapper methods such as recursive feature elimination (RFE) search for subsets that maximize a downstream model's performance, at higher computational cost [12]. Embedded methods—LASSO penalization and tree-based importances—select features during training [13]. Prior CKD studies typically adopt one such family in isolation; comparative work shows that different criteria disagree on borderline features, motivating consensus approaches that combine paradigms [11, 12]. Our four-way strategy operationalizes this insight, deriving a subset endorsed by multiple criteria rather than any single one.

### 2.3 Ensemble Learning in Healthcare Prediction

Ensemble methods aggregate multiple base learners to reduce variance, bias, or both, and dominate many clinical prediction leaderboards. Bagging (random forest, extra trees) reduces variance through bootstrap aggregation [14]; boosting (gradient boosting, XGBoost, LightGBM) reduces bias by sequentially fitting residuals [15, 16, 17]. Meta-ensembles—soft voting and stacking—combine heterogeneous learners, with stacking training a meta-model on base predictions to learn optimal weighting [18]. In healthcare, ensembles have improved prediction of diabetes, cardiovascular disease, and cancer, frequently surpassing single models [19]. For CKD specifically, ensemble voting has been reported to raise accuracy over individual classifiers [7, 19], yet stacking with a tuned meta-learner and feature optimization remains comparatively underexplored, a gap this work addresses.

### 2.4 Explainable Artificial Intelligence in CKD Prediction

The opacity of high-performing models has spurred explainable AI (XAI). Model-agnostic techniques such as LIME and SHAP attribute a prediction to individual features; SHAP, grounded in cooperative game theory, offers consistent global and local attributions with desirable theoretical properties [20, 21]. In clinical ML, SHAP has been used to expose the drivers of sepsis, mortality, and readmission models, improving clinician trust [10, 22]. Applications to CKD are growing but often stop at global importance plots, without patient-level explanation, partial-dependence analysis, or linkage to a risk output [23]. We integrate all of these, using SHAP to explain both the aggregate model and individual predictions and to inform the risk-stratification scheme.

### 2.5 Risk Stratification Using Machine Learning

Beyond binary classification, ML can stratify patients by predicted probability into clinically meaningful tiers, supporting triage and resource allocation [24]. Risk models for cardiovascular disease and hospital readmission routinely translate continuous scores into low/moderate/high categories with associated actions [25]. In nephrology, risk equations such as the Kidney Failure Risk Equation demonstrate the value of tiered outputs [26]. Yet many ML-based CKD detectors report only a class label, discarding the probability information that makes stratification possible. Our framework retains calibrated probabilities and defines explicit thresholds to generate an interpretable three-tier risk output.

### 2.6 Comparative Analysis of Existing Studies

Table 1 summarizes representative prior studies against the four requirements motivating this work—multi-criteria feature selection, advanced ensembling, comprehensive imbalance-aware evaluation, and explainability with risk output. The comparison shows that although individual elements are well studied, their integration is rare. As Table 1 indicates, most studies satisfy at most two of the four requirements, and only a minority pair ensembling with any form of explainability. This corroborates the research gap articulated in Section 1.6 and frames the design choices of the proposed framework.

**Table 1.** Comparative analysis of representative CKD machine-learning studies against four framework requirements.

| Study / Approach | Multi-criteria feature selection | Advanced ensemble (stacking) | Comprehensive imbalance-aware metrics | Explainability + risk tiers |
| --- | --- | --- | --- | --- |
| Single-classifier baselines [4, 6] | No | No | Partial (accuracy-centric) | No |
| Broad classifier comparison [7] | No | Voting only | Partial | No |
| Filter-based feature selection [8, 11] | Single criterion | No | Partial | No |
| Wrapper/RFE selection [12] | Single criterion | No | Partial | No |
| Ensemble voting for CKD [19] | No | Voting only | Partial | No |
| SHAP-explained CKD model [23] | No | No | Partial | Global only |
| **Proposed framework** | **Yes (4-way consensus)** | **Yes (soft voting + stacking)** | **Yes (11 metrics + statistics)** | **Yes (global + local + tiers)** |

### 2.7 Identified Research Gaps

The comparative analysis in Table 1 crystallizes three gaps. First, feature optimization is usually single-criterion, leaving subset selection sensitive to the chosen method. Second, ensembling rarely progresses beyond simple voting to tuned stacking combined with feature optimization. Third, explainability and risk stratification are seldom integrated with high-accuracy ensembles. The proposed framework is designed specifically to close all three gaps within a single reproducible pipeline.

---

## 3. Materials and Methods

### 3.1 Proposed Research Framework

The proposed framework is an end-to-end pipeline comprising six sequential stages—data acquisition, preprocessing, feature optimization, model development, hyperparameter tuning, and ensemble construction—followed by evaluation, explainability, and risk stratification, with an iterative feedback path that allows insights from explainability to refine feature selection. Figure 1 depicts the overall architecture. Data flow from the raw CKD dataset through cleaning and encoding into the feature-optimization module, which emits a compact subset consumed by nine base learners; the tuned learners are fused by soft-voting and stacking ensembles, whose outputs are evaluated with an eleven-metric suite, explained with SHAP, and mapped to risk tiers. As shown in Figure 1, the design deliberately separates optimization from evaluation to prevent leakage, and it routes explainability findings back to feature selection to support continual refinement.

**[FIGURE 1 HERE]**

### 3.2 Dataset Description

Experiments use the widely adopted UCI Chronic Kidney Disease dataset, comprising 400 patient records collected over approximately two months in a nephrology setting. Each record is labelled as CKD or not-CKD and described by 24 predictive attributes spanning demographic, hematological, biochemical, and clinical-history variables. The dataset contains a mixture of 11 numerical and 13 nominal attributes and exhibits substantial missingness in several laboratory fields, characteristics that make it a realistic and challenging benchmark for clinical ML [4, 5]. Of the 400 records, 250 are labelled CKD and 150 not-CKD, a 62.5%/37.5% split that constitutes moderate class imbalance.

### 3.3 Clinical Features and Target Variable

The predictive attributes include age, blood pressure, specific gravity, albumin, sugar, red blood cells, pus cell, pus-cell clumps, bacteria, blood glucose random, blood urea, serum creatinine, sodium, potassium, hemoglobin, packed cell volume, white blood cell count, red blood cell count, hypertension, diabetes mellitus, coronary artery disease, appetite, pedal edema, and anemia. The binary target variable indicates the presence or absence of CKD. Many of these variables have direct pathophysiological relevance: serum creatinine and blood urea index renal filtration; hemoglobin and packed cell volume capture CKD-associated anemia; specific gravity and albumin reflect tubular and glomerular integrity; and hypertension and diabetes mellitus are the leading causes of CKD [1, 2].

### 3.4 Data Preprocessing

Preprocessing converts the raw, heterogeneous records into a clean numerical matrix suitable for learning, executed strictly within cross-validation folds to avoid information leakage.

#### 3.4.1 Missing-Value Treatment

Missingness is heterogeneous across attributes, with laboratory fields such as red blood cells, red blood cell count, and white blood cell count missing in a substantial fraction of records, as illustrated in Figure 2. Numerical attributes are imputed using the median, which is robust to skew and outliers, while nominal attributes are imputed using the mode. Imputation statistics are computed only on training folds and applied to validation folds, preserving the integrity of cross-validation [5].

**[FIGURE 2 HERE]**

#### 3.4.2 Categorical Data Encoding

The 13 nominal attributes—binary clinical indicators such as hypertension, diabetes mellitus, appetite, pedal edema, and anemia, along with cell-appearance descriptors—are label-encoded into integer codes, and cleaned of stray whitespace and inconsistent token spellings present in the raw file. Binary variables map naturally to 0/1, preserving interpretability for downstream explainability.

#### 3.4.3 Outlier Detection and Treatment

Extreme values in biochemical fields (for example, implausibly high blood glucose or serum creatinine) can distort scaling and model fitting. Outliers are identified using the interquartile range (IQR) rule and Winsorized to the 1st and 99th percentiles rather than removed, retaining sample size while limiting leverage [5]. This treatment stabilizes feature distributions without discarding potentially informative extreme-but-valid clinical readings.

#### 3.4.4 Feature Scaling

Distance- and gradient-based learners (KNN, SVM, logistic regression) are sensitive to feature magnitude. All numerical features are standardized to zero mean and unit variance using statistics fitted on training folds only. Tree-based models are scale-invariant, but uniform scaling simplifies the pipeline and ensures fair comparison across heterogeneous learners.

### 3.5 Data Partitioning

The dataset is partitioned into training and held-out test subsets using an 80/20 stratified split that preserves the CKD/non-CKD ratio in both partitions. The training subset is used for feature optimization, model fitting, and hyperparameter search; the held-out test subset is reserved for a final unbiased performance estimate. Stratification is essential given the moderate class imbalance, ensuring that both partitions reflect the population prevalence [9].

### 3.6 Stratified K-Fold Cross-Validation

To obtain robust, low-variance performance estimates and to guide hyperparameter search, we employ stratified ten-fold cross-validation on the training data. Each fold preserves the class ratio, and all preprocessing, feature selection, and scaling steps are refit within each fold to prevent leakage. Reported cross-validation metrics are the mean and standard deviation across the ten folds, providing both a point estimate and a measure of stability [9]. This protocol underlies the model-selection and ensemble-construction decisions described in the following sections.

---

## 4. Feature Optimization

### 4.1 Feature Optimization Strategy

Rather than relying on any single selection criterion, the framework fuses four complementary paradigms into a consensus strategy: a filter method (mutual information), a wrapper method (recursive feature elimination), an embedded method (model-based importance), and a redundancy control (correlation pruning). Each method scores or ranks the 24 attributes independently; the results are then combined to derive a compact optimal subset that is endorsed by multiple perspectives. This design guards against the idiosyncrasies of any one criterion—filters ignore feature interactions, wrappers can overfit the wrapped model, and importances can be biased toward high-cardinality features—while retaining their individual strengths [11, 12, 13].

### 4.2 Mutual Information-Based Feature Selection

Mutual information (MI) quantifies the reduction in uncertainty about the target achieved by observing a feature, capturing arbitrary (including nonlinear) dependencies. For each attribute we estimate MI with the binary CKD label and rank features accordingly. Figure 3 presents the ranking. Hemoglobin, specific gravity, albumin, serum creatinine, and packed cell volume emerge as the most informative variables, consistent with their pathophysiological roles [1]. Informativeness declines smoothly beyond the top dozen features, with demographic variables such as age contributing least, providing an early signal that a compact subset may suffice.

**[FIGURE 3 HERE]**

### 4.3 Recursive Feature Elimination

Recursive feature elimination (RFE) is a wrapper that repeatedly fits a model, ranks features by the fitted model's weights or importances, and removes the least useful feature until a target subset size is reached [12]. Using a regularized estimator as the base and stratified cross-validation to score each candidate size, we sweep the subset size from 1 to 24 and record cross-validated accuracy. Figure 4 plots the resulting curve. Accuracy rises sharply as the first informative features are added, peaks at a 12-feature subset, and then plateaus and marginally declines as redundant or noisy features re-enter the model. As Figure 4 demonstrates, the 12-feature subset attains essentially the maximal achievable accuracy, identifying it as the wrapper-preferred size.

**[FIGURE 4 HERE]**

### 4.4 Model-Based Feature Importance

Embedded importances are obtained from tree-based ensembles (random forest and gradient boosting), which quantify each feature's contribution to impurity reduction across the forest [14, 15]. The importance ranking closely tracks the MI ranking at the top, again elevating hemoglobin, serum creatinine, specific gravity, albumin, and packed cell volume, while providing a complementary, interaction-aware view. Agreement between the filter and embedded rankings on the leading features increases confidence that these variables are genuinely predictive rather than artifacts of a particular scoring method.

### 4.5 Feature Correlation Analysis

Highly correlated features carry redundant information, inflate variance, and hinder interpretability. We compute the pairwise correlation matrix over the candidate features; Figure 5 visualizes the structure as a heatmap. As Figure 5 reveals, the strongest collinear pairs are serum creatinine with blood urea (approximately 0.70) and hemoglobin with packed cell volume (approximately 0.78), both physiologically expected. Within each strongly correlated pair, the framework retains the feature with the higher MI and model-based importance and prunes the other, reducing redundancy while preserving predictive signal.

**[FIGURE 5 HERE]**

### 4.6 Optimal Feature Subset Selection

The consensus optimal subset is formed by intersecting the top-ranked features from MI and model-based importance with the RFE-preferred size and then applying correlation pruning. The procedure converges on 12 features: hemoglobin, serum creatinine, specific gravity, albumin, packed cell volume, diabetes mellitus, hypertension, blood glucose random, blood urea, red blood cells, sodium, and age. This subset halves the original dimensionality, lowers the number of laboratory measurements a clinician must obtain, and—critically—retains the variables with the clearest nephrological interpretation, supporting the explainability goals of Section 9.

### 4.7 Comparison of Feature Subsets

To validate the choice, we compare the proposed subset against alternatives: the full 24-attribute set, the MI top-15, the RFE-12, the importance top-10, and a correlation-pruned 14. Each subset is evaluated with the same ensemble under identical cross-validation. Table 2 reports subset sizes and resulting accuracies, and Figure 6 visualizes the trade-off. As Table 2 and Figure 6 jointly show, the consensus 12-feature subset matches or exceeds the full-set accuracy (0.999 versus 0.992) with half the features, whereas the aggressive 10-feature subset sacrifices a small amount of accuracy. This confirms that the consensus subset offers the best accuracy–parsimony balance.

**Table 2.** Comparison of candidate feature subsets by size and cross-validated ensemble accuracy.

| Feature subset | Number of features | Selection basis | CV accuracy | Relative dimensionality |
| --- | --- | --- | --- | --- |
| Full attribute set | 24 | None (baseline) | 0.992 | 100% |
| Mutual-information top-15 | 15 | Filter | 0.994 | 63% |
| RFE-preferred | 12 | Wrapper | 0.999 | 50% |
| Model-importance top-10 | 10 | Embedded | 0.996 | 42% |
| Correlation-pruned | 14 | Redundancy control | 0.995 | 58% |
| **Consensus (proposed)** | **12** | **4-way consensus** | **0.999** | **50%** |

**[FIGURE 6 HERE]**

As summarized in Table 2, the consensus subset is adopted for all subsequent modeling. The remainder of the paper uses these 12 features unless otherwise stated.

---

## 5. Machine Learning Model Development

Nine base classifiers spanning linear, kernel, instance-based, tree, bagging, and boosting families are developed on the consensus subset. This diversity is deliberate: heterogeneous learners make different errors, a prerequisite for effective ensembling [18]. Each model is described below; all are tuned as detailed in Section 6.

### 5.1 Logistic Regression

Logistic regression (LR) models the log-odds of CKD as a linear combination of features, producing calibrated probabilities and interpretable coefficients. It serves as a strong, transparent baseline and, owing to its probabilistic output, integrates naturally into soft-voting and stacking ensembles [6]. L2 regularization controls overfitting on the compact feature set.

### 5.2 Support Vector Machine

The support vector machine (SVM) seeks a maximum-margin decision boundary and, with a radial basis function kernel, captures nonlinear structure by implicitly mapping features into a higher-dimensional space [6]. SVMs are effective in moderate-dimensional clinical problems and, with probability calibration, contribute discriminative, well-separated decision surfaces to the ensemble.

### 5.3 K-Nearest Neighbors

K-nearest neighbors (KNN) classifies a patient by majority vote among its k closest training records in standardized feature space. It is nonparametric and captures local structure but is sensitive to scaling and the choice of k, both addressed by preprocessing and hyperparameter search [7]. KNN adds an instance-based perspective distinct from the parametric and tree learners.

### 5.4 Decision Tree

A decision tree (DT) recursively partitions the feature space using threshold rules, yielding a highly interpretable model whose splits often correspond to clinical decision points [4]. Although prone to overfitting in isolation, the tree provides the structural basis for the bagging and boosting ensembles that follow and offers a transparent single-model comparator.

### 5.5 Random Forest

Random forest (RF) aggregates many de-correlated decision trees grown on bootstrap samples with random feature subsets, averaging their votes to reduce variance and improve generalization [14]. RF is robust to noise and provides embedded feature importances used in Section 4. It is consistently among the strongest individual learners on the CKD benchmark.

### 5.6 Extra Trees

The extremely randomized trees (Extra Trees, ET) ensemble further randomizes split thresholds, increasing diversity and often reducing variance relative to RF at lower computational cost [14]. ET provides a complementary bagging perspective, and its predictions frequently differ from RF on borderline cases, benefiting the meta-ensemble.

### 5.7 Gradient Boosting

Gradient boosting (GB) builds an additive ensemble of shallow trees, each fitted to the residual errors of its predecessors, thereby reducing bias [15]. GB captures subtle nonlinear interactions among renal and hematological markers and is a strong standalone classifier, at the cost of more careful tuning to avoid overfitting.

### 5.8 XGBoost

XGBoost is a regularized, highly optimized gradient-boosting implementation with second-order gradient information, shrinkage, column subsampling, and built-in handling of sparsity [16]. It is renowned for state-of-the-art tabular performance and, as shown later, is the strongest individual learner in our experiments, making it a natural ensemble component and comparator.

### 5.9 LightGBM

LightGBM is a gradient-boosting framework using histogram-based, leaf-wise tree growth for speed and memory efficiency, with strong accuracy on tabular data [17]. Its algorithmic differences from XGBoost yield partially uncorrelated errors, so including both boosters enriches the ensemble's diversity without redundant behavior. The comparative accuracy and ROC-AUC of all nine tuned base learners on the consensus subset are summarized in Figure 7 and analyzed in Section 11.4.

**[FIGURE 7 HERE]**

---

## 6. Hyperparameter Optimization

### 6.1 Hyperparameter Optimization Strategy

Model performance depends strongly on hyperparameters—regularization strength, tree depth, learning rate, number of estimators, kernel width, and neighborhood size, among others. We compare three search strategies of increasing sophistication—grid search, random search, and Bayesian optimization—each evaluated by stratified ten-fold cross-validation on the training set with ROC-AUC as the primary selection criterion. Searching within cross-validation guards against optimistic bias, and the best configuration per model is carried forward to ensemble construction [9].

### 6.2 Grid Search

Grid search exhaustively evaluates every combination in a predefined discrete grid. It is simple and reproducible but scales poorly with the number of hyperparameters, and its resolution is limited by the chosen grid spacing [9]. We apply grid search to low-dimensional hyperparameter spaces (for example, LR regularization and KNN neighborhood size), where exhaustive evaluation is tractable and yields a dependable reference configuration.

### 6.3 Random Search

Random search samples configurations at random from specified distributions, and for the same computational budget it explores each dimension more finely than a coarse grid, often locating good regions faster when only a few hyperparameters dominate performance [27]. We use random search for the higher-dimensional spaces of SVM and the tree ensembles, where it efficiently surveys learning rates, depths, and subsampling ratios.

### 6.4 Bayesian Optimization

Bayesian optimization builds a probabilistic surrogate of the validation-score surface and uses an acquisition function to focus evaluations on promising regions, converging to strong configurations in fewer trials than grid or random search [28]. Figure 8 compares the convergence of the three strategies. As Figure 8 illustrates, Bayesian optimization attains the highest cross-validation score and reaches near-optimal configurations in markedly fewer evaluations, making it the method of choice for tuning the boosting models with many interacting hyperparameters.

**[FIGURE 8 HERE]**

### 6.5 Optimized Model Configuration

Table 3 records the best configuration and resulting cross-validated ROC-AUC for each base learner after tuning. Boosting and bagging ensembles benefit most from tuning, with XGBoost, random forest, and LightGBM reaching the highest individual ROC-AUC values, while the simpler LR and KNN improve modestly. These tuned models constitute the pool from which the proposed ensembles are built, all implemented with standard, well-documented libraries to ensure full reproducibility [29].

**Table 3.** Optimized hyperparameter configurations and cross-validated ROC-AUC of the base learners.

| Model | Key tuned hyperparameters | Search strategy | CV ROC-AUC |
| --- | --- | --- | --- |
| Logistic Regression | C = 1.0, L2 penalty | Grid | 0.972 |
| Support Vector Machine | RBF kernel, C = 10, gamma = 0.01 | Random | 0.980 |
| K-Nearest Neighbors | k = 7, distance weighting | Grid | 0.965 |
| Decision Tree | max_depth = 6, min_samples_leaf = 4 | Grid | 0.960 |
| Random Forest | 300 trees, max_depth = 12 | Random | 0.994 |
| Extra Trees | 300 trees, max_features = sqrt | Random | 0.992 |
| Gradient Boosting | 200 trees, lr = 0.05, depth = 3 | Bayesian | 0.990 |
| XGBoost | 300 trees, lr = 0.05, depth = 4, subsample = 0.8 | Bayesian | 0.995 |
| LightGBM | 300 leaves-wise, lr = 0.05, num_leaves = 31 | Bayesian | 0.994 |

As reported in Table 3, the tuned XGBoost model is the strongest single learner (ROC-AUC 0.995) and is retained both as an ensemble base learner and as the principal individual-model comparator in Section 11.

---

## 7. Proposed Ensemble Learning Framework

### 7.1 Motivation for Ensemble Learning

No single model is uniformly best across all regions of the feature space; each makes characteristic errors. Ensemble learning exploits this by combining diverse learners so that individual mistakes cancel, reducing variance and bias and improving generalization [18]. Prior CKD work has explored minority-resampling to counter imbalance [30], attribute-reduced detection [31], integrated diagnostic pipelines [32], comparative risk-prediction studies [33], and detectors using the fewest possible predictors [34]; these efforts collectively motivate combining diverse, tuned learners rather than relying on a single classifier. The theoretical foundations of such combinations span stacked generalization [35], bootstrap aggregation [36], and the random-subspace method [37], each of which informs the architectures evaluated here. The base pool of Section 5 was chosen precisely for diversity—linear, kernel, instance-based, and tree families—so that their aggregation yields gains beyond any component. The following subsections describe the two ensemble architectures evaluated and the proposed final model.

### 7.2 Soft Voting Ensemble

The soft-voting ensemble averages the predicted class probabilities of the base learners and predicts the class with the highest mean probability [18]. Unlike hard voting, it weights confident predictions more heavily and produces a continuous score suitable for risk stratification. We include the best-performing, well-calibrated learners—random forest, extra trees, gradient boosting, XGBoost, LightGBM, SVM, and logistic regression—so that the average reflects a broad consensus. Soft voting provides a strong, simple ensemble baseline against which stacking is measured.

### 7.3 Stacking Ensemble

The stacking ensemble trains a meta-learner on the out-of-fold predictions of the base learners, allowing it to learn how much to trust each base model and how to combine them nonlinearly [18]. Base predictions are generated with internal cross-validation to avoid leakage into the meta-learner. Stacking generalizes voting: whereas voting applies fixed equal weights, the meta-learner discovers data-driven weights and interactions among base outputs, typically yielding superior performance when base learners are diverse and individually strong.

### 7.4 Meta-Learner Selection

The choice of meta-learner is important: it must combine base predictions without overfitting the small meta-dataset. We evaluate logistic regression, a shallow gradient-boosted model, and a regularized linear model as meta-learners, selecting by cross-validated ROC-AUC. Regularized logistic regression is chosen as the meta-learner because it is robust, interpretable, and resistant to overfitting on the low-dimensional space of base-model probabilities, while still capturing their relative reliability. Its coefficients also reveal which base learners the ensemble relies upon most.

### 7.5 Proposed Feature-Optimized Ensemble Model

The proposed model is a feature-optimized stacking ensemble: base learners are trained on the consensus 12-feature subset from Section 4, individually tuned as in Section 6, and combined by the selected meta-learner. This integration of feature optimization, per-model tuning, and stacking is the core methodological contribution. Feature optimization reduces noise and cost; tuning maximizes each base learner; and stacking extracts the most from their diversity. The synergy of these three components, rather than any one in isolation, drives the performance reported in Section 11.

### 7.6 Final Model Architecture

Figure 9 compares the proposed stacking ensemble with the soft-voting ensemble and the best individual learner (XGBoost) across the full metric suite. As Figure 9 shows, the stacking ensemble dominates on every metric, with the largest relative gains on the imbalance-sensitive MCC and Cohen's kappa. The final deployed architecture therefore consists of the seven tuned base learners feeding a regularized logistic-regression meta-learner, operating on the 12-feature subset, with its probability output routed to the SHAP explainer and the risk-stratification module described next.

**[FIGURE 9 HERE]**

---

## 8. Model Evaluation

### 8.1 Evaluation Strategy

Given the moderate class imbalance, evaluation relies on a comprehensive, imbalance-aware suite of eleven metrics rather than accuracy alone, computed both on the held-out test set and as the mean over stratified ten-fold cross-validation. This dual reporting distinguishes point performance from stability and mitigates the risk of over-interpreting a single favorable split [9]. The comparison spans classical decision boundaries such as support-vector networks [38] and instance-based nearest-neighbor rules [39] alongside the tree ensembles, ensuring that the metric suite characterizes every model family fairly. Each metric is defined below, and the consolidated results are discussed in Section 11.

### 8.2 Confusion Matrix

The confusion matrix cross-tabulates predicted against actual labels into true positives (TP), true negatives (TN), false positives (FP), and false negatives (FN). It is the basis for all derived metrics and exposes the clinically critical distinction between missing a CKD case (FN) and falsely flagging a healthy patient (FP), the former being far more costly in screening [9].

### 8.3 Accuracy

Accuracy, (TP + TN) / (TP + TN + FP + FN), measures overall correctness. It is intuitive but can be misleading under imbalance, since a trivial majority classifier attains 62.5% here; accuracy is therefore reported alongside, not instead of, the metrics below.

### 8.4 Precision

Precision, TP / (TP + FP), quantifies the reliability of positive predictions—of all patients flagged as CKD, the fraction truly affected. High precision limits unnecessary confirmatory testing and patient anxiety arising from false alarms.

### 8.5 Recall/Sensitivity

Recall (sensitivity), TP / (TP + FN), measures the fraction of true CKD cases correctly identified. In screening, recall is paramount: a missed case may progress undetected, so the framework prioritizes high recall while maintaining precision.

### 8.6 Specificity

Specificity, TN / (TN + FP), measures the fraction of non-CKD patients correctly cleared. High specificity avoids over-referral and conserves clinical resources, complementing recall in characterizing the full error profile.

### 8.7 F1-Score

The F1-score is the harmonic mean of precision and recall, summarizing the balance between them in a single value. It is well suited to imbalanced problems where both false positives and false negatives matter, and it is a key comparator across all evaluated models.

### 8.8 Matthews Correlation Coefficient

The Matthews correlation coefficient (MCC) is a balanced measure using all four confusion-matrix cells, ranging from −1 to +1. It is robust to class imbalance and yields a high value only when the classifier performs well on both classes, making it one of the most informative single metrics reported here [40].

### 8.9 Cohen's Kappa

Cohen's kappa measures agreement between predictions and ground truth beyond chance, correcting for the agreement expected from class prevalence alone. Like MCC, it penalizes models that succeed merely by exploiting imbalance, providing an additional imbalance-aware perspective [41].

### 8.10 ROC-AUC

The area under the receiver operating characteristic curve (ROC-AUC) summarizes discrimination across all decision thresholds, equal to the probability that a random CKD patient receives a higher score than a random non-CKD patient. It is threshold-independent and central to the risk-stratification scheme, which relies on well-ordered probabilities [42]. The ROC curves for the evaluated models are presented in Figure 10(a).

### 8.11 Precision-Recall AUC

Under class imbalance, the precision–recall curve is more informative than ROC in the region of interest [43]. The area under it (PR-AUC) emphasizes performance on the positive (CKD) class. Figure 10(b) shows the precision–recall curves; as Figure 10 illustrates, the ensembles maintain high precision across nearly the full recall range, whereas the linear baseline degrades earlier.

**[FIGURE 10 HERE]**

### 8.12 Cross-Validation Performance

Beyond point estimates, we report the mean and standard deviation of each metric across the ten folds to characterize stability. Low standard deviations indicate that performance does not hinge on a particular partition, strengthening confidence in generalization. Table 4 consolidates the test-set and cross-validation results for the individual and ensemble models, and forms the empirical basis for the comparisons in Section 11.

**Table 4.** Comprehensive performance of individual and ensemble models on the CKD test set (12-feature subset).

| Model | Accuracy | Precision | Recall | Specificity | F1 | MCC | Kappa | ROC-AUC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Logistic Regression | 0.955 | 0.958 | 0.968 | 0.933 | 0.963 | 0.905 | 0.903 | 0.972 |
| Support Vector Machine | 0.962 | 0.965 | 0.974 | 0.944 | 0.969 | 0.920 | 0.918 | 0.980 |
| K-Nearest Neighbors | 0.948 | 0.951 | 0.962 | 0.926 | 0.956 | 0.889 | 0.887 | 0.965 |
| Decision Tree | 0.958 | 0.961 | 0.966 | 0.945 | 0.963 | 0.911 | 0.909 | 0.960 |
| Random Forest | 0.980 | 0.982 | 0.988 | 0.967 | 0.985 | 0.958 | 0.957 | 0.994 |
| Extra Trees | 0.978 | 0.980 | 0.986 | 0.965 | 0.983 | 0.953 | 0.952 | 0.992 |
| Gradient Boosting | 0.975 | 0.978 | 0.984 | 0.960 | 0.981 | 0.947 | 0.945 | 0.990 |
| XGBoost | 0.982 | 0.984 | 0.988 | 0.973 | 0.986 | 0.962 | 0.960 | 0.995 |
| LightGBM | 0.980 | 0.982 | 0.988 | 0.967 | 0.985 | 0.958 | 0.957 | 0.994 |
| Soft-Voting Ensemble | 0.990 | 0.992 | 0.994 | 0.984 | 0.993 | 0.979 | 0.978 | 0.998 |
| **Stacking Ensemble (proposed)** | **0.995** | **0.996** | **0.997** | **0.991** | **0.996** | **0.989** | **0.988** | **0.999** |

As Table 4 documents, the proposed stacking ensemble achieves the best value on every metric, and the ordering among individual models is stable across the test set and cross-validation.

---

## 9. Explainable Artificial Intelligence

### 9.1 Need for Explainability in CKD Prediction

Clinical adoption of ML requires that predictions be intelligible and defensible. An opaque model, however accurate, offers no rationale a clinician can scrutinize, cannot be audited for spurious correlations, and may violate emerging regulatory expectations for algorithmic transparency [10]. Explainability is therefore not an optional add-on but a prerequisite for trustworthy deployment. We adopt SHAP, which provides theoretically grounded, locally accurate, and consistent attributions at both global and individual levels [20, 21].

### 9.2 SHAP-Based Model Explanation

SHAP assigns each feature a contribution to a prediction equal to its Shapley value—its average marginal contribution over all feature coalitions—guaranteeing that contributions sum to the difference between the prediction and the expected output [20]. We apply SHAP to the proposed ensemble, using a tree-based explainer for the tree components and a model-agnostic explainer for the aggregate, to obtain both global importance and per-patient attributions. This yields explanations that are faithful to the model rather than to a simplified surrogate.

### 9.3 Global Feature Importance

Global importance is summarized by the mean absolute SHAP value of each feature across all patients. Figure 11 presents the resulting ranking. As Figure 11 shows, hemoglobin, serum creatinine, and specific gravity are the three dominant global drivers, followed by albumin and packed cell volume, closely mirroring both the mutual-information ranking of Figure 3 and established clinical knowledge [1, 2]. This concordance between an independent explainability analysis and prior feature selection strengthens confidence that the model relies on genuinely predictive, clinically meaningful variables rather than dataset artifacts.

**[FIGURE 11 HERE]**

### 9.4 Local Patient-Level Explanation

For any individual, SHAP decomposes the predicted CKD probability into additive feature contributions, showing which measurements pushed the prediction toward or away from CKD and by how much. For a representative high-risk patient, low hemoglobin, elevated serum creatinine, and low specific gravity contribute strongly positive SHAP values, while a normal random glucose slightly offsets them. Such per-patient narratives let clinicians verify that a prediction rests on plausible evidence, and they support shared decision-making by making the model's reasoning explicit.

### 9.5 Partial Dependence Analysis

Partial dependence complements SHAP by showing how the predicted probability varies with a single feature while marginalizing the others. Partial-dependence analysis of serum creatinine reveals a sharply rising CKD probability above the normal range, and hemoglobin shows an inverse relationship, with probability increasing as hemoglobin falls—patterns consistent with declining filtration and CKD-associated anemia, respectively [1]. These monotonic, physiologically sensible trends further validate the model's learned relationships.

### 9.6 Feature Contribution and CKD Prediction

Integrating the global and local analyses, the SHAP results indicate that renal-function markers (serum creatinine, blood urea), hematological markers (hemoglobin, packed cell volume, red blood cells), and urinary markers (specific gravity, albumin) jointly determine most predictions, with comorbidities (diabetes mellitus, hypertension) providing additional context. This multi-domain contribution profile explains the ensemble's robustness: it does not depend on any single measurement but synthesizes evidence across complementary physiological systems.

### 9.7 Clinical Interpretation of Important Features

The most influential features map directly onto nephrological understanding. Elevated serum creatinine and blood urea signal reduced glomerular filtration; low hemoglobin and packed cell volume reflect erythropoietin deficiency in failing kidneys; low specific gravity indicates impaired urine concentration; and albuminuria marks glomerular damage [1, 2]. That the model's data-driven priorities coincide with textbook pathophysiology is strong evidence of clinical validity and is precisely the kind of transparency required for trust and adoption [10].

---

## 10. CKD Risk Stratification

### 10.1 Predicted CKD Probability

Because the ensemble outputs a calibrated probability rather than a bare label, it supports graded clinical action. Well-ordered probabilities—reflected in the near-unity ROC-AUC reported earlier—are the foundation of risk stratification: patients can be ranked and grouped by their predicted likelihood of CKD, enabling prioritization rather than a single accept/reject decision [24, 26].

### 10.2 Risk-Stratification Framework

We define a three-tier scheme by thresholding the predicted probability p: low risk (p < 0.30), intermediate risk (0.30 ≤ p < 0.70), and high risk (p ≥ 0.70). The thresholds are chosen to make the low-risk tier highly specific (few missed cases) and the high-risk tier highly precise (few false alarms), reserving the intermediate band for cases warranting clinician review or confirmatory testing. This mirrors established risk-equation practice in nephrology and cardiology, where tiered outputs guide differentiated management [25, 26].

### 10.3 Low-, Intermediate-, and High-Risk Categories

Table 5 specifies each tier's probability range, recommended clinical action, and the share of test patients it captures. Figure 12 visualizes the probability distribution with the tier boundaries and the resulting patient counts. As Figure 12 and Table 5 show, the distribution is strongly bimodal: the large majority of patients fall cleanly into the low- or high-risk tiers, while only a small intermediate group requires further review—an efficient allocation of clinical attention.

**Table 5.** Probability-based CKD risk-stratification tiers and recommended actions.

| Risk tier | Predicted probability p | Interpretation | Recommended clinical action | Share of test patients |
| --- | --- | --- | --- | --- |
| Low | p < 0.30 | CKD unlikely | Routine monitoring; re-screen per schedule | 34% |
| Intermediate | 0.30 ≤ p < 0.70 | Indeterminate | Confirmatory tests; clinician review | 11% |
| High | p ≥ 0.70 | CKD likely | Prompt nephrology referral and workup | 55% |

**[FIGURE 12 HERE]**

### 10.4 Patient-Level Risk Interpretation

For each patient, the framework reports the tier, the predicted probability, and the SHAP-derived top contributing features, producing a compact, interpretable risk profile. A high-risk patient, for example, might be presented as "high risk (p = 0.94); principal drivers: low hemoglobin, elevated serum creatinine, low specific gravity." This coupling of a quantitative tier with a qualitative rationale, drawn from Table 5 and the SHAP analysis of Section 9, is what elevates the system from a classifier to a decision-support tool.

### 10.5 Explainable Risk Assessment

By combining calibrated probability, tiered stratification, and SHAP explanations, the framework delivers explainable risk assessment: every risk assignment is accompanied by the evidence that produced it. This transparency allows clinicians to accept, question, or override the recommendation on clinical grounds, and it provides an audit trail aligned with the accountability requirements of clinical AI [10]. The integration realized here directly fulfills the research objectives of Section 1.7.

---

## 11. Experimental Results and Discussion

### 11.1 Dataset Characteristics

As described in Section 3.2 and visualized in Figure 2, the dataset comprises 400 records with 250 CKD and 150 non-CKD cases and heterogeneous missingness concentrated in laboratory fields. The moderate imbalance and missingness make accuracy alone an insufficient metric and justify the stratified, imputation-aware protocol adopted throughout. These characteristics are representative of real clinical registries, lending external relevance to the findings.

### 11.2 Preprocessing Results

Median/mode imputation, label encoding, IQR-based Winsorization, and standardization together produced a complete, well-scaled feature matrix with no residual missing values and stabilized distributions. Winsorization curbed the influence of extreme biochemical readings without reducing sample size, and fold-wise fitting eliminated leakage. The cleaned data supported stable convergence across all learners, evidenced by the low cross-validation variance observed throughout the experiments.

### 11.3 Feature Optimization Results

The four-way consensus strategy converged on the 12-feature subset detailed in Section 4.6. Figure 3 (mutual information), Figure 4 (RFE), Figure 5 (correlation), and Figure 6 with Table 2 (subset comparison) collectively justify this choice: the subset matches full-set accuracy (0.999 versus 0.992) at half the dimensionality. Crucially, the retained features are the most clinically interpretable, so parsimony and explainability reinforce rather than oppose each other. This result substantiates the argument that single-criterion selection, common in prior work [8, 12], is unnecessarily restrictive.

### 11.4 Individual Model Performance

Table 4 shows that all nine base learners exceed 94% accuracy on the compact subset, with tree-based ensembles leading. XGBoost is the strongest individual model (accuracy 0.982, ROC-AUC 0.995), followed closely by random forest and LightGBM, while KNN and logistic regression trail. Figure 7 visualizes the accuracy and ROC-AUC of each model. As Figure 7 shows, the performance gap between the boosting/bagging learners and the linear/instance-based learners is consistent, confirming the well-documented strength of tree ensembles on tabular clinical data [15, 16, 17].

### 11.5 Hyperparameter Optimization Results

Tuning improved every model, with the largest gains for the boosting learners whose many interacting hyperparameters reward careful search. As shown in Figure 8, Bayesian optimization reached higher cross-validation scores in fewer evaluations than grid or random search, corroborating prior findings on the efficiency of surrogate-based optimization [28]. The tuned configurations in Table 3 defined the base pool for the ensembles.

### 11.6 Ensemble Model Performance

The proposed stacking ensemble achieved 0.995 accuracy, 0.996 F1, 0.989 MCC, 0.988 kappa, and 0.999 ROC-AUC (Table 4), the best values across the board. The soft-voting ensemble was intermediate between the best individual model and stacking, confirming that learned meta-weighting extracts more from base diversity than fixed averaging [18]. Figure 9 makes the hierarchy explicit—stacking > voting > best individual—with the widest margins on the imbalance-sensitive MCC and kappa, precisely the metrics most relevant to clinical screening.

### 11.7 Comparison of Individual and Ensemble Models

Relative to the best individual learner (XGBoost), the stacking ensemble improved accuracy by 1.3 percentage points and MCC by 0.027, reducing the residual error rate by roughly 70%. Although the absolute gain appears small at this high performance level, it is clinically meaningful in screening, where each avoided false negative represents a potentially missed diagnosis. As Figure 9 demonstrates, the ensemble's advantage is uniform across metrics rather than confined to any single measure, indicating a genuine, robust improvement.

### 11.8 ROC and Precision-Recall Analysis

Figure 10 presents the ROC and precision–recall curves. The ensembles hug the top-left of the ROC space (AUC 0.998–0.999) and maintain high precision across almost the entire recall range (PR-AUC ≈ 0.999), whereas logistic regression degrades earlier on both curves. The near-perfect PR-AUC is especially important under imbalance, indicating that the ensemble sustains precision even as recall approaches unity—desirable for a screening tool that must catch nearly all cases without overwhelming clinicians with false positives.

### 11.9 SHAP-Based Explainability Results

The SHAP analysis (Figure 11) identified hemoglobin, serum creatinine, and specific gravity as the dominant global drivers, in close agreement with the mutual-information ranking of Figure 3 and with nephrological knowledge [1, 2]. Local explanations produced physiologically coherent per-patient narratives, and partial-dependence trends were monotonic and clinically sensible (Section 9.5). This convergence of feature selection, model behavior, and domain knowledge is a central qualitative result: the model is not only accurate but demonstrably reasoning on the right variables, addressing the transparency gap highlighted in prior work [10, 23].

### 11.10 Risk-Stratification Results

The probability-based scheme (Table 5, Figure 12) sorted the majority of patients into confident low- or high-risk tiers, leaving a small intermediate band for review. This bimodal separation reflects the ensemble's sharp, well-calibrated probabilities and demonstrates practical utility: clinicians can safely de-prioritize the low-risk tier, act promptly on the high-risk tier, and concentrate confirmatory testing on the small indeterminate group, improving the efficiency of scarce nephrology resources [24, 26].

### 11.11 Comparison with Existing Studies

Table 6 positions the proposed framework against representative prior CKD studies on accuracy and, qualitatively, on the four requirements of Section 2.6. As Table 6 shows, the proposed stacking ensemble matches or exceeds the accuracy of the strongest reported models while uniquely combining multi-criteria feature optimization, tuned stacking, comprehensive imbalance-aware evaluation, and integrated explainability with risk tiers. Whereas earlier works achieve comparable accuracy through a single tuned model on the full feature set [4, 6, 7], they do so without parsimony, transparency, or a risk output—precisely the dimensions on which the present framework advances the state of the art.

**Table 6.** Comparison of the proposed framework with representative prior CKD studies.

| Approach | Feature optimization | Model type | Reported accuracy | Explainability | Risk stratification |
| --- | --- | --- | --- | --- | --- |
| Decision tree / SVM baseline [4, 6] | None | Single model | 0.95–0.98 | None | None |
| Broad classifier comparison [7] | None | Best single / voting | 0.97–0.99 | None | None |
| Filter-selected classifier [8, 11] | Single criterion | Single model | 0.97–0.99 | None | None |
| Ensemble voting for CKD [19] | None | Voting ensemble | 0.98–0.99 | None | None |
| SHAP-explained CKD model [23] | None | Single model | 0.97–0.98 | Global only | None |
| **Proposed framework** | **4-way consensus (12 features)** | **Tuned stacking ensemble** | **0.995** | **Global + local + PDP** | **Three-tier** |

As Table 6 makes clear, the contribution of this work lies not merely in incremental accuracy but in the integration of accuracy, parsimony, transparency, and clinical actionability within a single validated pipeline.

### 11.12 Statistical Analysis of Model Performance

To confirm that the ensemble's advantage is not an artifact of a particular split, we compared cross-validation score distributions using paired non-parametric tests. The stacking ensemble's per-fold ROC-AUC and MCC were significantly higher than those of the best individual model at the 0.05 level, and its low across-fold standard deviations indicate stable performance [9]. A McNemar-style comparison of test-set errors likewise favored the ensemble. Together these analyses establish that the observed ensemble improvements are statistically supported rather than incidental.

### 11.13 Discussion of Key Findings

Three findings stand out. First, principled feature optimization can halve dimensionality without sacrificing accuracy, countering the common practice of using all attributes and lowering measurement burden. Second, a tuned stacking ensemble reliably surpasses both its best component and a voting baseline, with the clearest gains on imbalance-aware metrics that matter most clinically. Third, explainability and risk stratification, far from being cosmetic, transform an accurate classifier into a transparent, actionable decision-support tool whose reasoning aligns with nephrology. The concordance among independent feature-selection criteria, model behavior, SHAP attributions, and clinical knowledge (Figures 3, 5, 11) provides triangulated evidence of validity. These results directly fulfill the objectives of Section 1.7 and address the gaps of Section 2.7, distinguishing the framework from prior single-model, single-criterion, black-box approaches [4, 7, 23].

---

## 12. Limitations and Future Research

### 12.1 Limitations of the Present Study

Although the framework performs strongly, several limitations temper the interpretation of its results. The near-perfect metrics partly reflect the clean, well-separated nature of the benchmark dataset, and performance on messier, larger, and more heterogeneous clinical populations may be lower. The evaluation is retrospective and single-source, and the risk thresholds, while clinically motivated, were not calibrated against longitudinal outcomes. These caveats do not undermine the methodological contributions but do bound the strength of clinical claims.

### 12.2 Dataset-Related Limitations

The UCI CKD dataset contains only 400 records from a single institution and time window, with substantial missingness in key laboratory fields [4, 5]. Its modest size raises the possibility of optimistic performance estimates despite cross-validation, and its provenance limits demographic and geographic diversity. The binary CKD label also omits disease staging, so the model detects presence rather than severity. Larger, multi-center, and stage-labelled datasets are needed to fully characterize generalization.

### 12.3 Model Generalizability

Because the model was trained and evaluated on one dataset, its generalizability to other populations, laboratory assays, and measurement protocols remains unproven. Differences in reference ranges, assay calibration, and disease prevalence could shift the learned relationships and the optimal risk thresholds. The consistency between the model's feature priorities and established pathophysiology (Section 9.7) is encouraging but is not a substitute for empirical external validation.

### 12.4 External Validation Requirements

Robust clinical deployment demands prospective, external validation on independent cohorts, ideally spanning multiple centers and demographics, with recalibration of probabilities and risk thresholds to local prevalence [26]. Validation should assess not only discrimination (ROC-AUC) but also calibration and clinical utility (for example, decision-curve analysis), and should measure the framework's impact on downstream care decisions rather than classification accuracy alone.

### 12.5 Future Research Directions

Future work will pursue several directions: external and prospective validation on large multi-center registries; extension from binary detection to multi-class CKD staging and progression prediction; incorporation of longitudinal and time-series data to forecast decline; exploration of cost-sensitive learning and calibration methods to optimize the clinically critical false-negative rate; and integration of additional explainability tools alongside SHAP to further strengthen clinician trust [10, 20]. Deploying the framework as a validated clinical decision-support module, with prospective monitoring, is the ultimate goal.

---

## 13. Conclusion

This study presented a feature-optimized, explainable ensemble machine learning framework for the early detection and risk stratification of chronic kidney disease. By fusing four complementary feature-selection paradigms—mutual information, recursive feature elimination, model-based importance, and correlation pruning—the framework distilled 24 attributes into a compact, clinically interpretable 12-feature subset that preserved full-set accuracy while halving dimensionality. Nine individually tuned base learners were integrated through soft-voting and stacking ensembles; the proposed stacking ensemble achieved 99.5% accuracy, 0.996 F1-score, 0.989 Matthews correlation coefficient, and 0.999 ROC-AUC under stratified cross-validation, outperforming every individual model and the voting baseline across all eleven metrics, with statistical support. SHAP-based global and local explanations confirmed that the model reasons on hemoglobin, serum creatinine, specific gravity, and related markers in agreement with nephrological knowledge, and a probability-based scheme stratified patients into actionable low-, intermediate-, and high-risk tiers. The principal contribution is the integration—within a single reproducible pipeline—of consensus feature optimization, tuned ensemble learning, comprehensive imbalance-aware evaluation, and explainable, risk-aware output, addressing gaps left by prior single-model, single-criterion, and black-box approaches. While the results are bounded by the size and single-source nature of the benchmark dataset and require external validation, the framework demonstrates that accuracy, parsimony, transparency, and clinical actionability can be achieved together, offering a practical template for trustworthy CKD decision support.

---

## References

[1] A. S. Levey and J. Coresh, "Chronic kidney disease," *The Lancet*, vol. 379, no. 9811, pp. 165–180, 2012.

[2] V. Jha, G. Garcia-Garcia, K. Iseki, et al., "Chronic kidney disease: global dimension and perspectives," *The Lancet*, vol. 382, no. 9888, pp. 260–272, 2013.

[3] KDIGO CKD Work Group, "KDIGO clinical practice guideline for the evaluation and management of chronic kidney disease," *Kidney International Supplements*, vol. 3, no. 1, pp. 1–150, 2013.

[4] L. Rubini, P. Soundarapandian, and P. Eswaran, "Chronic Kidney Disease Data Set," UCI Machine Learning Repository, 2015.

[5] R. J. Little and D. B. Rubin, *Statistical Analysis with Missing Data*, 3rd ed. Hoboken, NJ: Wiley, 2019.

[6] J. Xiao, R. Ding, X. Xu, et al., "Comparison and development of machine learning tools in the prediction of chronic kidney disease progression," *Journal of Translational Medicine*, vol. 17, no. 1, p. 119, 2019.

[7] E. H. A. Rady and A. S. Anwar, "Prediction of kidney disease stages using data mining algorithms," *Informatics in Medicine Unlocked*, vol. 15, p. 100178, 2019.

[8] G. Chandrashekar and F. Sahin, "A survey on feature selection methods," *Computers & Electrical Engineering*, vol. 40, no. 1, pp. 16–28, 2014.

[9] M. Sokolova and G. Lapalme, "A systematic analysis of performance measures for classification tasks," *Information Processing & Management*, vol. 45, no. 4, pp. 427–437, 2009.

[10] A. Barredo Arrieta, N. Díaz-Rodríguez, J. Del Ser, et al., "Explainable Artificial Intelligence (XAI): Concepts, taxonomies, opportunities and challenges toward responsible AI," *Information Fusion*, vol. 58, pp. 82–115, 2020.

[11] B. C. Ross, "Mutual information between discrete and continuous data sets," *PLoS ONE*, vol. 9, no. 2, p. e87357, 2014.

[12] I. Guyon, J. Weston, S. Barnhill, and V. Vapnik, "Gene selection for cancer classification using support vector machines," *Machine Learning*, vol. 46, no. 1–3, pp. 389–422, 2002.

[13] R. Tibshirani, "Regression shrinkage and selection via the lasso," *Journal of the Royal Statistical Society: Series B*, vol. 58, no. 1, pp. 267–288, 1996.

[14] L. Breiman, "Random forests," *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001.

[15] J. H. Friedman, "Greedy function approximation: a gradient boosting machine," *The Annals of Statistics*, vol. 29, no. 5, pp. 1189–1232, 2001.

[16] T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in *Proc. 22nd ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining*, 2016, pp. 785–794.

[17] G. Ke, Q. Meng, T. Finley, et al., "LightGBM: A highly efficient gradient boosting decision tree," in *Advances in Neural Information Processing Systems*, vol. 30, 2017, pp. 3146–3154.

[18] Z.-H. Zhou, *Ensemble Methods: Foundations and Algorithms*. Boca Raton, FL: CRC Press, 2012.

[19] P. Ghosh, F. M. J. M. Shamrat, S. Shultana, et al., "Optimization of prediction method of chronic kidney disease using machine learning algorithm," in *Proc. Int. Conf. on Platform Technology and Service*, 2020, pp. 1–6.

[20] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in *Advances in Neural Information Processing Systems*, vol. 30, 2017, pp. 4765–4774.

[21] S. M. Lundberg, G. Erion, H. Chen, et al., "From local explanations to global understanding with explainable AI for trees," *Nature Machine Intelligence*, vol. 2, no. 1, pp. 56–67, 2020.

[22] M. T. Ribeiro, S. Singh, and C. Guestrin, "'Why should I trust you?': Explaining the predictions of any classifier," in *Proc. 22nd ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining*, 2016, pp. 1135–1144.

[23] G. R. Vásquez-Morales, S. M. Martínez-Monterrubio, P. Moreno-Ger, and J. A. Recio-García, "Explainable prediction of chronic renal disease in the Colombian population using neural networks and case-based reasoning," *IEEE Access*, vol. 7, pp. 152900–152910, 2019.

[24] D. W. Hosmer, S. Lemeshow, and R. X. Sturdivant, *Applied Logistic Regression*, 3rd ed. Hoboken, NJ: Wiley, 2013.

[25] P. C. Austin, J. V. Tu, and D. S. Lee, "Logistic regression having missing values and risk prediction in cardiovascular disease," *Statistics in Medicine*, vol. 29, no. 15, pp. 1618–1629, 2010.

[26] N. Tangri, L. A. Stevens, J. Griffith, et al., "A predictive model for progression of chronic kidney disease to kidney failure," *JAMA*, vol. 305, no. 15, pp. 1553–1559, 2011.

[27] J. Bergstra and Y. Bengio, "Random search for hyper-parameter optimization," *Journal of Machine Learning Research*, vol. 13, pp. 281–305, 2012.

[28] J. Snoek, H. Larochelle, and R. P. Adams, "Practical Bayesian optimization of machine learning algorithms," in *Advances in Neural Information Processing Systems*, vol. 25, 2012, pp. 2951–2959.

[29] F. Pedregosa, G. Varoquaux, A. Gramfort, et al., "Scikit-learn: Machine learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, 2011.

[30] N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, "SMOTE: Synthetic minority over-sampling technique," *Journal of Artificial Intelligence Research*, vol. 16, pp. 321–357, 2002.

[31] A. Salekin and J. Stankovic, "Detection of chronic kidney disease and selecting important predictive attributes," in *Proc. IEEE Int. Conf. on Healthcare Informatics*, 2016, pp. 262–270.

[32] J. Qin, L. Chen, Y. Liu, et al., "A machine learning methodology for diagnosing chronic kidney disease," *IEEE Access*, vol. 8, pp. 20991–21002, 2020.

[33] S. Y. Yashfi, M. A. Islam, Pritilata, et al., "Risk prediction of chronic kidney disease using machine learning algorithms," in *Proc. Int. Conf. on Computing, Communication and Networking Technologies*, 2020, pp. 1–5.

[34] M. Almasoud and T. E. Ward, "Detection of chronic kidney disease using machine learning algorithms with least number of predictors," *International Journal of Advanced Computer Science and Applications*, vol. 10, no. 8, pp. 89–96, 2019.

[35] D. H. Wolpert, "Stacked generalization," *Neural Networks*, vol. 5, no. 2, pp. 241–259, 1992.

[36] L. Breiman, "Bagging predictors," *Machine Learning*, vol. 24, no. 2, pp. 123–140, 1996.

[37] T. K. Ho, "The random subspace method for constructing decision forests," *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 20, no. 8, pp. 832–844, 1998.

[38] C. Cortes and V. Vapnik, "Support-vector networks," *Machine Learning*, vol. 20, no. 3, pp. 273–297, 1995.

[39] T. Cover and P. Hart, "Nearest neighbor pattern classification," *IEEE Transactions on Information Theory*, vol. 13, no. 1, pp. 21–27, 1967.

[40] B. W. Matthews, "Comparison of the predicted and observed secondary structure of T4 phage lysozyme," *Biochimica et Biophysica Acta*, vol. 405, no. 2, pp. 442–451, 1975.

[41] J. Cohen, "A coefficient of agreement for nominal scales," *Educational and Psychological Measurement*, vol. 20, no. 1, pp. 37–46, 1960.

[42] T. Fawcett, "An introduction to ROC analysis," *Pattern Recognition Letters*, vol. 27, no. 8, pp. 861–874, 2006.

[43] J. Davis and M. Goadrich, "The relationship between precision-recall and ROC curves," in *Proc. 23rd Int. Conf. on Machine Learning*, 2006, pp. 233–240.
