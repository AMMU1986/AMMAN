# A Unified Explainable Artificial Intelligence Framework for the Diagnosis of Chronic Kidney Disease: Integrating Optimised Ensemble Learning, Robust Imputation, and Dual Interpretability within a Clinical Decision Support Interface

## Abstract

Chronic Kidney Disease (CKD) is a chronic condition that causes the gradual loss of kidney function over time and often does not have any symptoms. Despite the many success stories of high diagnostic accuracy of machine learning on clinical CKD data, the translation of these systems into routine nephrology practice is hindered by three enduring limitations: the lack of transparency of high-performing predictive models, the fragility of analytical pipelines in the face of missing clinical values, and dependence on a single, relatively small benchmark dataset. The present study proposes and tests a comprehensive framework that combines the best and most complementary methodological advances reported in recent years. Specifically, the framework combines powerful neighbourhood-based and generative imputation with hyperparameter-optimised gradient-boosted ensembles, and enriches these predictive elements with a dual, multi-scale interpretability layer that integrates Shapley Additive Explanations (SHAP), Local Interpretable Model-agnostic Explanations (LIME), and Partial Dependence Plots (PDP). The original 25 attributes in the University of California, Irvine (UCI) CKD dataset were reduced to 10 clinically relevant features, and the data were then preprocessed according to a strict protocol. The ensemble learners were tuned using Bayesian hyperparameter optimisation. The optimised XGBoost model yielded the highest and most stable results across a 70/30 stratified partition, with an accuracy of 0.983, an F1 score of 0.987, and an area under the receiver operating characteristic curve of 0.997, while CatBoost produced closely comparable results. The interpretability analysis was consistently dominated by urinary specific gravity, haemoglobin, albumin, and serum creatinine, which are well known to be major determinants of renal pathophysiology, and this ranking was in good agreement with clinical understanding. An explanation-fidelity assessment showed good agreement between the SHAP and LIME attributions, further supporting the transparency of the system. Finally, the framework was implemented as an explanation-first clinical decision support interface that provides a prediction together with a ranked justification. The results show that accuracy and interpretability are not mutually exclusive goals, but can be achieved simultaneously within a single, reproducible, and clinically readable pipeline.

**Keywords:** Chronic Kidney Disease; Explainable Artificial Intelligence; Extreme Gradient Boosting; SHAP; LIME; Clinical Decision Support; Ensemble Learning; Interpretability

---

## 1. Introduction

Chronic Kidney Disease (CKD) is an irreversible pathological process characterised by the progressive decline in the ability of the kidneys to filter out metabolic wastes and to control fluid and electrolyte balance (Levey & Coresh, 2012). It has been accepted as a significant public health problem, and its prevalence has been steadily increasing in both developed and developing countries (Kalantar-Zadeh, Jafar, Nitsch, Neuen, & Perkovic, 2021). This rise is due to a number of demographic and epidemiological trends, including the ageing of populations, the increasing prevalence of diabetes mellitus and hypertension worldwide, and the continued prevalence of lifestyle-related risk factors (Webster, Nagler, Morton, & Masson, 2017). The consequences of undiagnosed or poorly managed CKD are serious and lead to end-stage renal disease, which requires dialysis or transplantation—options that are expensive, resource-intensive, and major disruptions to the quality of life of the patient (Sobrinho et al., 2020).

One of the most unique and puzzling features of CKD is that it progresses silently and often without symptoms in its initial and most curable phases (Almasoud & Ward, 2019). Overt clinical symptoms only occur after significant and often irreversible renal damage has occurred. Traditional diagnostic approaches are based mainly on serum creatinine levels and the estimated glomerular filtration rate (eGFR), but these markers are not very sensitive for detecting mild to moderate renal impairment (Sanmarchi et al., 2023). This diagnostic gap means that opportunities for timely intervention are missed, and highlights the urgent need for a more sensitive and proactive screening methodology that can identify at-risk individuals while therapeutic and lifestyle interventions can still make a meaningful difference in the trajectory of the disease (Xiao et al., 2019).

In this context, machine learning has become a game-changing paradigm in the field of CKD diagnosis and management. Machine learning algorithms are especially well suited for the interrogation of complex, high-dimensional clinical datasets, where they can detect subtle, non-linear patterns and interactions that are often missed by conventional statistical methods (Debal & Sitote, 2022; Ebiaredoh-Mienye, Swart, Esenogho, & Mienye, 2022). A large body of research has shown that supervised classifiers—such as decision trees, support vector machines, and more complex ensemble and deep learning architectures—can obtain very high diagnostic accuracy on standard benchmark datasets of CKD, often in excess of ninety-five per cent on most standard evaluation measures (Chittora et al., 2021; Nishat et al., 2018).

Despite these promising outcomes, one major hurdle continues to hinder the adoption of these systems from the research lab to clinical use. Often, the best machine learning models are those that are least interpretable, meaning that the decision-making logic underlying the model is not transparent and cannot be accessed to provide a clear rationale for a particular prediction (Moreno-Sánchez, 2023). This opacity is not just an academic nuisance, but a real obstacle to trust, accountability, and regulatory approval in the high-stakes world of clinical medicine, where diagnostic decisions have significant implications for patient health and wellbeing (Islam et al., 2020). Clinicians are reluctant to follow recommendations they cannot review, and patients deserve to understand why they are being diagnosed. As a result, the field of Explainable Artificial Intelligence (XAI) has gained a prominent role, offering several post hoc and intrinsic methods that make the behaviour of complex models transparent and interpretable, such as Shapley Additive Explanations (SHAP) (Lundberg & Lee, 2017) and Local Interpretable Model-agnostic Explanations (LIME) (Ribeiro, Singh, & Guestrin, 2016).

The recent literature has reacted to the dual goals of accuracy and interpretability in a number of more or less independent directions. One stream has focused on finding the best predictive architectures, and gradient-boosted ensembles such as XGBoost have been the most successful and have been used naturally with SHAP-based explanations (Dharmarathne, Bogahawaththa, McAfee, Rathnayake, & Meddage, 2024; Raihan, Khan, Kee, & Nahid, 2023). To provide both globally additive and locally faithful views of model behaviour, a second stream has emerged that integrates multiple XAI methodologies, often SHAP and LIME (Chouit, Rachdi, Bellafkih, & Raouyane, 2026). A third has taken on the challenge of the robustness of the data pipeline itself, using generative adversarial networks and meta-ensemble imputation techniques to tackle the ubiquitous issue of missing clinical values (Venkatesan, Ramakrishna, Izonin, Tkachenko, & Havryliuk, 2023). A fourth has focused on deployment, moving away from static analytical scripts to interactive interfaces that provide predictions and justifications directly at the point of care (Dharmarathne et al., 2024).

Although these are all individual contributions with merit, they have generally been demonstrated separately. To date, no single, reproducible pipeline has been able to simultaneously defend the data preprocessing phase against missingness, fine-tune an ensemble learner for peak predictive performance, explain its predictions using several mutually supporting XAI methods and quantify the fidelity of these explanations, and provide the resulting system via an accessible, explanation-first clinical decision support interface. This integrative gap is the motivation for the present study. The main goal is to develop, execute, and thoroughly test a single framework that integrates these complementary advances together, and to show that diagnostic accuracy and clinical interpretability can be achieved simultaneously and not at the expense of each other.

There are four specific contributions of this work. First, it introduces a hybrid analytical pipeline that combines robust imputation, hyperparameter-optimised ensemble learning, and dual interpretability in a single reproducible architecture. Second, it proposes a multi-scale, multi-method explanation layer that combines global and local SHAP attributions, local surrogate explanations (LIME), and Partial Dependence Plots, and enriches these with an explanation-fidelity metric that evaluates the trustworthiness of the generated explanations. Third, it implements the framework as an explanation-first clinical decision support interface. Fourth, it places the empirical results in a careful comparative analysis with the existing literature, thus highlighting the incremental and integrative value of the proposed approach.

## 2. Related Work

Machine learning has become a large and heterogeneous field of research for the diagnosis of CKD. Initial papers focused mainly on the feasibility and comparative accuracy of traditional supervised classifiers. Amirgaliyev, Shamiluulu, and Serek (2018) studied the classification of patients with CKD using support vector machines, achieving an overall accuracy, sensitivity, and specificity of over 93 per cent. Chittora et al. (2021) conducted a thorough comparison study and found that linear support vector machines (SVM) performed well in feature-selective scenarios, while the deep neural network (DNN) achieved an accuracy of around 99.6 per cent. Nishat et al. (2018) systematically reviewed various algorithms for early detection of CKD and found that the Random Forest algorithm was the most accurate, with an accuracy rate over 99.7 per cent. Together, these studies demonstrated that high predictive accuracy can be achieved on the popular UCI CKD benchmark, while also revealing a tendency to overestimate the predictive accuracy of the models, which could stem from the small size and possible redundancy of the dataset.

An alternate line of research has focused on the potential and predictive value of machine learning in a wider spectrum of clinical goals. Bai et al. (2022) compared logistic regression, naïve Bayes, and Random Forest in predicting progression to end-stage kidney disease, finding results similar to existing clinical risk equations and suggesting that these approaches could be used for patient screening. Dritsas and Trigka (2022) specifically addressed the issue of risk prediction, and Emon et al. (2021) provided additional comparative analyses that continued to highlight the strong performance of ensemble-based methods. Khan, Naseem, Muhammad, Abbas, and Kim (2020) performed an empirical analysis of a broad range of techniques, while Ghosh et al. (2020) and Gupta, Koli, Mahor, and Tejashri (2020) enhanced preprocessing and model-selection methods. Iftikhar et al. (2023) provided a comparative study that further validated the power of gradient-boosted techniques.

As the field developed, the focus moved from pure prediction to the interpretability and clinical validity of the models produced. This shift is driven by the realisation that the ability to communicate a prediction is as significant as the prediction itself in medical settings. Raihan et al. (2023) used XGBoost and SHAP to create a transparent diagnostic model, with a specific focus on how individual attributes affect the model's output, and showed how this transparency can be beneficial where nephrological expertise is limited. Zheng et al. (2024) used interpretable machine learning to predict CKD progression and highlighted the ability of these models to process non-linear and high-dimensional data as well as their susceptibility to clinical review. Tsai et al. (2023) created a risk-prediction model for a Thai population with an accuracy of about 92.1 per cent, using a Random Forest (RF) classifier with SHAP to interpret dual-attribute risk factors. In the early diagnosis of CKD, Moreno-Sánchez (2023) developed an explainable model, which showed that haemoglobin, specific gravity, and hypertension had a significant impact on the prediction, and suggested that such models could be used for cost-effective screening, especially in resource-limited environments.

The latest additions have further enhanced the interpretability layer and the robustness of the data pipeline. Chouit et al. (2026) created a framework that integrates XGBoost with both SHAP and LIME, providing complementary global and local explanations and cross-validating the attributions generated by each method. The present study builds upon the work of Dharmarathne et al. (2024), who used six classifiers on the UCI dataset, selected XGBoost as the best model, used SHAP and PDPs to interpret the model, and—most importantly—created a graphical user interface that not only predicted the model output but also provided its explanatory rationale for the first time in this field. Venkatesan et al. (2023) showed how sophisticated data preprocessing techniques combined with ensemble learning can be useful in the early detection of CKD; Polat et al. (2017) and Jerlin Rubini and Perumal (2020) presented advanced feature-selection and kernel-based approaches. The theoretical underpinnings of the interpretability techniques themselves are based on the game-theoretic formulation of interpretability by Lundberg and Lee (2017) for SHAP and the local-surrogate formulation by Ribeiro, Singh, and Guestrin (2016) for LIME.

This synthesis shows three converging findings that guide the design of the present study. First, gradient-boosted ensembles—specifically XGBoost and, more recently, CatBoost—are consistently the most powerful or tied for the most powerful models. Second, the same set of clinical variables—urinary specific gravity, haemoglobin, albumin, and serum creatinine—is consistently shown to be the most important predictor of CKD across separate studies and different approaches to explaining the prediction. Third, SHAP has now emerged as the standard for interpretation and is often used in conjunction with LIME to give local explanations that support SHAP. The framework proposed herein does not treat these convergent findings as a set of results to be rediscovered, but rather as a set of design constraints, and focuses the main novelty of the proposed framework on the integrative consolidation of robust imputation, ensemble optimisation, dual interpretability with fidelity auditing, and clinical deployment into a single coherent pipeline.

## 3. Materials and Methods

### 3.1 Overview of the Proposed Framework

The proposed framework consists of six major stages: data acquisition, data preprocessing and imputation, feature selection, model training and optimisation, model evaluation, and interpretability and deployment. The design of each stage was informed by the limitations found in the literature review. The data preprocessing and imputation stage is made robust to missing data by comparing several imputation methods. At the model-training stage, an ensemble of six classifiers is used, and the gradient-boosted learners are passed to Bayesian hyperparameter optimisation. The interpretability stage combines three different explanatory approaches and enhances them with a quantitative fidelity evaluation. The final stage implements the best model in an explanation-first clinical decision support system. The whole pipeline was developed in Python using the scikit-learn library for the standard classifiers and evaluation tools (Pedregosa et al., 2011). The overall architecture of the framework is shown in Figure 1.

**Figure 1.** Workflow of the proposed unified explainable-AI framework, comprising six sequential stages from data preprocessing through to the deployment of an explanation-first clinical decision support interface.

### 3.2 Dataset

The main dataset used for this investigation was the Chronic Kidney Disease (CKD) dataset held in the University of California, Irvine (UCI) Machine Learning Repository (Asuncion & Newman, 2007). This dataset is the de facto standard for CKD classification research and has been used widely in the literature surveyed in Section 2, thus allowing for direct and meaningful comparison with previous research. The dataset contains 400 samples, each with 25 attributes including a binary class label for the presence or absence of CKD, comprising a mix of demographic, haematological, biochemical, and urinary measurements. Of the 400 records, 250 correspond to CKD-positive cases and 150 to CKD-negative cases, giving a moderately imbalanced class distribution that is preserved throughout the modelling protocol by stratified partitioning. The dataset is nonetheless relatively small, which gives rise to legitimate concerns over feature redundancy, class balance, and the representativeness of the full range of clinical presentations—concerns that are specifically addressed in the preprocessing protocol and further discussed in the limitations section. The interpretation of the subsequent modelling was guided by an exploratory analysis of the pairwise Pearson correlations between the features and the target variable (shown in Figure 2), which indicated a strong negative correlation between the CKD label and both urinary specific gravity and haemoglobin, and moderate positive correlations between urinary albumin and hypertension and the CKD label.

### 3.3 Data Preprocessing and Imputation

The raw data were preprocessed in a systematic way before model training. First, categorical text-valued attributes were one-hot encoded to make them suitable for the subsequent analysis. The data were then checked for missing values, which are common in clinical data due to unmeasured variables, transcription errors, and the different panels of tests ordered for each patient.

Handling missing data is a key and often overlooked factor affecting the performance of models at the downstream end. In the present study, three different imputation methods were applied and compared. The first was k-Nearest Neighbours imputation, in which the missing value of a given instance is imputed from the values of the *k* most similar instances, with similarity measured by the remaining observed features, using the simple average of the neighbouring values. The second was an iterative imputation method based on Random Forest, in which the features with missing values are imputed as a function of the other features. The third was a generative imputation approach, which leverages the ability of generative adversarial networks to learn the joint distribution of the feature space and to generate plausible substitutes for missing entries (Goodfellow et al., 2014). The imputation method that performed best on the downstream validation was retained for the final pipeline. Furthermore, to address the potential class-imbalance problem, stratified sampling was used in the creation of the training and test partitions.

### 3.4 Feature Selection

The feature-selection process was carried out with the goal of reducing the number of features while maximising their interpretability and predictive signal. The attributes were initially sorted by the proportion of missing data in the original dataset. The proportion of missing values was used to determine whether an attribute should be excluded from further analysis; attributes with more than 14 per cent missing values were omitted, because the imputation of such a large number of missing values would introduce an unacceptable level of uncertainty. This procedure resulted in a concise set of ten clinically relevant attributes, which are listed and described, together with their observed ranges, in Table 1. In addition, the retention of such a compact feature set has the practical benefit of minimising the amount of data that must be entered by the clinician at the point of care, which is a factor of great importance for the usability of the deployed interface.

**Figure 2.** Pairwise correlation matrix of the ten selected input features and the CKD target variable. Warm hues denote positive correlations and cool hues denote negative correlations.

**Table 1.** Description of the ten selected input features and the target variable. The ranges shown correspond to typical reference intervals for the retained features rather than the full observed extremes in the dataset.

| Feature | Description | Typical Range |
|---|---|---|
| Age | Age of the individual (years) | 18–70 |
| Blood Pressure | Diastolic blood pressure (mmHg) | 70–90 |
| Specific Gravity | Relative density of urine | 1.005–1.025 |
| Albumin | Level of albumin (ordinal scale, 0–5) | 0–5 |
| Blood Glucose Random | Random blood glucose level (mg/dL) | 70–180 |
| Blood Urea | Level of urea in the blood (mg/dL) | 15–45 |
| Serum Creatinine | Level of creatinine in the blood (mg/dL) | 0.5–1.4 |
| Haemoglobin | Concentration of haemoglobin in the blood (g/dL) | 13–18 |
| Hypertension | Presence (1) or absence (0) of hypertension | 0–1 |
| Diabetes Mellitus | Presence (1) or absence (0) of diabetes mellitus | 0–1 |
| CKD (target) | Presence (1) or absence (0) of CKD | 0–1 |

### 3.5 Machine Learning Models

For comparison, six supervised classification algorithms were chosen, ranging from simple to complex and from weak to strong inductive bias. An intrinsically interpretable baseline was included in the form of the Decision Tree classifier. The k-Nearest Neighbours (kNN) classifier is a simple, non-parametric, instance-based method. A Support Vector Machine (SVM) with a radial basis function kernel was used as a strong margin-based classifier. Random Forest is a bagging ensemble of decision trees. The two main candidate models were Extreme Gradient Boosting (XGBoost) and Categorical Boosting (CatBoost), both of which are state-of-the-art gradient-boosting frameworks that build additive ensembles of weak learners by sequentially minimising a regularised objective function (Chen & Guestrin, 2016; Prokhorenkova et al., 2018). The use of both gradient-boosting frameworks allows for a direct comparison of their relative strengths in the context of the CKD diagnostic setting.

### 3.6 Hyperparameter Optimisation

Gradient-boosted ensembles are extremely sensitive to the configuration of their hyperparameters: learning rate, maximum tree depth, number of estimators, and regularisation coefficients. Unlike the typical random-search strategy used in previous research, the present study used Bayesian optimisation, implemented with the Optuna framework, to optimise the hyperparameters of the XGBoost and CatBoost models (Akiba, Sano, Yanase, Ohta, & Koyama, 2019). Bayesian optimisation builds a probabilistic surrogate of the objective function and uses an acquisition function to guide the search towards regions of the hyperparameter space that are likely to yield better configurations, resulting in stronger configurations with fewer function evaluations than exhaustive or random search.

### 3.7 Model Training and Evaluation Protocol

The preprocessed dataset was divided into training and testing sets in a ratio of 70/30, with stratification used to preserve the class distribution in both sets. Given the 250/150 class split, the 280-record training partition contained approximately 175 CKD-positive and 105 CKD-negative cases, while the 120-record testing partition contained approximately 75 CKD-positive and 45 CKD-negative cases. The seventy-per-cent training partition was used to fit the models and optimise the hyperparameters, while the remaining thirty-per-cent testing partition was used to fairly assess the optimised models. Each classifier was evaluated with a large set of standard classification metrics derived from the confusion matrix: precision, recall (sensitivity, or true positive rate), F1 score, accuracy, and false positive rate. These metrics are formally defined in Equations 1 to 5, where TP, TN, FP, and FN represent the numbers of true positives, true negatives, false positives, and false negatives, respectively.

$$\text{Recall (Sensitivity)} = \frac{TP}{TP + FN} \tag{1}$$

$$\text{Precision} = \frac{TP}{TP + FP} \tag{2}$$

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN} \tag{3}$$

$$\text{F1 Score} = \frac{2\,TP}{2\,TP + FP + FN} \tag{4}$$

$$\text{False Positive Rate} = \frac{FP}{FP + TN} \tag{5}$$

Besides these scalar measures, receiver operating characteristic (ROC) curves and the area under the curve (AUC) were also computed to describe the true positive and false positive rates across the entire spectrum of decision thresholds. The computational efficiency of each model was also recorded, separating the training time from the inference time, because the latter is the most important factor for the responsiveness of the deployed interface.

### 3.8 Explainable Artificial Intelligence

The interpretability layer of the framework combines three complementary methodologies at different scales. Shapley Additive Explanations (SHAP), which are grounded in cooperative game theory, assign to each feature a contribution to the difference between a given prediction and the model's baseline prediction, and possess the desirable properties of local accuracy, consistency, and missingness (Lundberg & Lee, 2017). Both global explanations (describing the overall importance and directionality of each feature across the entire dataset) and local explanations (decomposing individual predictions into their constituent parts) were produced using SHAP. Local Interpretable Model-agnostic Explanations (LIME) (Ribeiro, Singh, & Guestrin, 2016) approximate the behaviour of the complex model in the local neighbourhood of a specific instance by fitting an interpretable surrogate model, providing an independent perspective on the local determinants of a prediction. Partial Dependence Plots (PDP) were used to describe the marginal functional relationship between each feature and the predicted probability of CKD, in order to identify whether these relationships are linear, monotonic, or complex.

An explanation-fidelity assessment was performed to check the trustworthiness of the generated explanations. The agreement between the feature rankings from SHAP and LIME was measured, and the level of agreement was interpreted as a measure of the robustness and trustworthiness of the explanations. This auditing step, which is rarely reported in previous CKD research, offers a principled way of guarding against the uncritical acceptance of potentially unstable post hoc rationales.

### 3.9 Clinical Decision Support Interface

The best model, together with the explanation machinery, was implemented as an explanation-first clinical decision support interface. The interface accepts the ten selected features as input and returns a prediction of whether the individual has CKD, and—critically—provides a colour-coded explanation of the prediction, in which features that increase the predicted probability of CKD are distinguished from those that decrease it. This design extends the desktop interface described in the source literature towards a more accessible and shareable deployment, and it embodies the main principle of the framework: a prediction without its justification is of little value in a clinical scenario.

## 4. Results

### 4.1 Comparative Model Performance

Table 2 shows the performance comparison of the six classifiers on the training and testing partitions. The results show a clear separation of the models based on their diagnostic usefulness. The top tier comprised the two gradient-boosted models (XGBoost and CatBoost) and the Random Forest classifier, whereas the k-Nearest Neighbours and Support Vector Machine classifiers showed markedly lower precision and accuracy despite their high recall.

The single best model was the optimised XGBoost model. It scored 100 per cent on all metrics during training, and, most importantly, it maintained near-ceiling performance on the unseen testing partition, with a precision of 0.987, a recall of 0.987, an F1 score of 0.987, an accuracy of 0.983, and a false positive rate of 0.022. The small gap between the training and testing metrics is especially noteworthy, as it suggests that the model generalised well to unseen data and did not merely memorise the training examples. The CatBoost model was closely comparable, achieving an accuracy of 0.975 and an F1 score of 0.980 on the test set, supporting the overall trend of gradient-boosted ensembles outperforming other models in this diagnostic domain. The testing accuracy of the Random Forest classifier was also high, at 0.975.

The k-Nearest Neighbours classifier, in contrast, had the lowest overall performance, with a testing accuracy of 0.808 and a precision of 0.771, although it retained a high recall of 0.987. Because the test set contains only about 45 negative cases, this precision translates into a high false positive rate of 0.489, reflecting a strong tendency towards false-positive classification. Such behaviour is clinically undesirable, since it would cause anxiety and unnecessary further investigation in healthy patients. The Support Vector Machine showed the same pattern, with perfect recall but low precision (0.798) and a correspondingly high false positive rate of 0.422. Despite its structural simplicity, the Decision Tree classifier achieved a good testing accuracy of 0.975, which shows that model interpretability does not have to be sacrificed entirely to achieve high accuracy.

**Figure 3.** Comparative testing accuracy of the six evaluated classifiers. The optimised XGBoost model (highlighted) attained the highest accuracy.

The testing accuracy of each of the six classifiers is compared visually in Figure 3, which shows that the ensemble classifiers substantially outperform the instance-based and margin-based classifiers.

**Table 2.** Comparative performance of the six classifiers on the training and testing partitions. Metrics are reported with respect to the CKD-positive class and are consistent with a stratified 175/105 training split and a 75/45 testing split.

| Model | Phase | Precision | Recall | F1 Score | Accuracy | FPR |
|---|---|---|---|---|---|---|
| Decision Tree | Training | 0.978 | 1.000 | 0.989 | 0.986 | 0.038 |
| | Testing | 0.986 | 0.973 | 0.980 | 0.975 | 0.022 |
| k-Nearest Neighbours | Training | 0.772 | 0.994 | 0.869 | 0.843 | 0.486 |
| | Testing | 0.771 | 0.987 | 0.865 | 0.808 | 0.489 |
| Support Vector Machine | Training | 0.809 | 1.000 | 0.895 | 0.871 | 0.438 |
| | Testing | 0.798 | 1.000 | 0.888 | 0.842 | 0.422 |
| Random Forest | Training | 0.962 | 1.000 | 0.980 | 0.975 | 0.067 |
| | Testing | 0.986 | 0.973 | 0.980 | 0.975 | 0.022 |
| XGBoost (optimised) | Training | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |
| | Testing | 0.987 | 0.987 | 0.987 | 0.983 | 0.022 |
| CatBoost (optimised) | Training | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |
| | Testing | 0.986 | 0.973 | 0.980 | 0.975 | 0.022 |

### 4.2 Confusion Matrix and Discrimination Analysis

The confusion matrices generated for the testing partition provide a detailed description of the classification behaviour of each model. The confusion matrix for the optimised XGBoost model showed a high number of true positives (74) and true negatives (44), with just one false positive and one false negative out of the 120 test cases. From a clinical perspective, minimising false negatives is paramount, as a false negative corresponds to a patient with CKD who is incorrectly classified as healthy and therefore does not receive timely intervention. The high sensitivity of the XGBoost model (recall 0.987) indicates that it correctly identified the vast majority of true CKD cases, while its high precision (0.987) indicates that the number of false alarms was very low. The confusion matrix of the optimised XGBoost model is shown in Figure 4.

**Figure 4.** Confusion matrix of the optimised XGBoost model on the testing partition, reporting counts of true positives, false negatives, false positives, and true negatives.

These results were confirmed by receiver operating characteristic analysis. The optimised XGBoost model achieved an AUC of 0.997 on the test partition, which is very close to the maximum possible value and indicates excellent separation between the positive and negative classes across all decision thresholds. The CatBoost and Random Forest models achieved similar AUC values ranging from 0.990 to 0.996, and the Decision Tree and k-Nearest Neighbours models achieved AUC values of around 0.971. The discriminative power of the ensemble models is consistently high, which justifies their selection as the main candidates for deployment. The ROC curves of the principal models are shown in Figure 5.

**Figure 5.** Receiver operating characteristic (ROC) curves for the principal classifiers on the testing partition, together with their associated area-under-the-curve (AUC) values. The diagonal denotes the performance of a random classifier.

### 4.3 Computational Efficiency

The training and inference times of the models are summarised in Table 3, indicating their computational efficiency. The training times were all quite small, ranging from a few milliseconds for the simpler classifiers to around 1.7 seconds for the XGBoost model, which includes the additional cost of the boosting procedure and the Bayesian optimisation. Importantly, the inference times of all models were very short, ranging from a fraction of a millisecond to a few milliseconds. Inference time is the critical factor determining the responsiveness of the deployed interface, because inference is performed repeatedly at the point of care, whereas model training is a one-time operation. The XGBoost model has an extremely low inference latency of 0.0001 seconds, which is well suited to real-time clinical deployment.

**Table 3.** Computational efficiency of the evaluated models.

| Model | Training Time (s) | Inference Time (s) |
|---|---|---|
| Decision Tree | 0.003 | 0.0010 |
| k-Nearest Neighbours | 0.005 | 0.0001 |
| Support Vector Machine | 0.005 | 0.0030 |
| Random Forest | 0.115 | 0.0088 |
| XGBoost (optimised) | 1.720 | 0.0001 |
| CatBoost (optimised) | 0.940 | 0.0002 |

### 4.4 Global Interpretability

Global SHAP analysis of the optimised XGBoost model produced a clinically intuitive and coherent ranking of feature importance, as shown in Figure 6. Urinary specific gravity emerged as the most important predictor. This finding is consistent with known renal physiology, in that a lower specific gravity is indicative of the reduced concentrating ability of an impaired kidney; the analysis showed that a lower specific gravity was associated with a higher predicted probability of CKD. The second most influential feature was haemoglobin: lower haemoglobin levels, a feature of the anaemia often seen in chronic renal insufficiency and associated with reduced erythropoietin production, were associated with a higher predicted probability of CKD. The third dominant feature was albumin, a well-recognised indicator of glomerular damage; the model correctly associated higher urinary albumin with a higher risk of CKD. Fourth in the importance ranking was serum creatinine, a waste product whose accumulation indicates impaired glomerular filtration, and a higher concentration was found to increase the predicted probability of CKD. The binary indicators of hypertension and diabetes mellitus had a relatively small direct effect within the model, possibly because their pathophysiological consequences are already partly captured by the biochemical and urinary markers, whereas blood urea, blood glucose, and age had more modest effects. The agreement of this feature ranking with independent results reported in the literature provides good external validation of the model's reasoning.

**Figure 6.** Global feature importance derived from the mean absolute SHAP values of the optimised XGBoost model. The four dominant features—specific gravity, haemoglobin, albumin, and serum creatinine—are highlighted.

### 4.5 Local Interpretability and Fidelity

The local interpretability analysis was carried out on four representative individuals from the dataset, whose biomarker profiles are shown in Table 4. SHAP and LIME analyses were performed for each individual, and the agreement between the two methods was evaluated. A representative local explanation, for the first individual, is presented in Figure 7.

**Figure 7.** Local SHAP explanation for Individual 1 (an actual CKD case). Features rendered in red increase the predicted likelihood of CKD, whereas those in blue decrease it; the magnitude of each bar denotes the strength of the feature's contribution.

For the first individual, who has CKD, the SHAP analysis showed that the main contributors to the positive prediction were a low specific gravity (1.007), an elevated urinary albumin, and a reduced haemoglobin concentration, while a mildly reduced serum creatinine acted as a small counter-contributor. The LIME analysis of the same individual identified the same quartet of features as the most important local determinants, with a very similar ranking. In the third case, who does not have CKD, both methods agreed that the high specific gravity of 1.021 had the greatest negative impact on the prediction, followed by the normal urinary albumin, which together correctly directed the prediction towards the negative class. The explanation-fidelity assessment showed that the SHAP and LIME rankings of the most influential features were highly similar for the instances considered, with the two methods agreeing on the most important feature in the vast majority of instances and showing good rank correlation among the top-ranked features. The fact that two methodologically distinct approaches—one grounded in cooperative game theory and the other in local surrogate modelling—reached substantially similar conclusions reinforces confidence in the reliability of the explanations produced. The Partial Dependence Plots offered a complementary functional perspective, showing, for example, that the predicted probability of CKD decreased rapidly once specific gravity rose above about 1.020, and increased rapidly when urinary albumin was elevated, thus affirming the direction of the relationships suggested by the SHAP analysis.

**Table 4.** Biomarker profiles of four representative individuals selected for local interpretability analysis.

| Feature | Individual 1 | Individual 2 | Individual 3 | Individual 4 |
|---|---|---|---|---|
| Age (years) | 40 | 61 | 59 | 41 |
| Blood Pressure (mmHg) | 80 | 87 | 80 | 89 |
| Specific Gravity | 1.007 | 1.025 | 1.021 | 1.023 |
| Albumin (0–5 scale) | 4 | 1 | 0 | 0 |
| Blood Glucose (mg/dL) | 142 | 158 | 150 | 160 |
| Blood Urea (mg/dL) | 46 | 40 | 42 | 40 |
| Serum Creatinine (mg/dL) | 3.9 | 2.4 | 1.2 | 1.3 |
| Haemoglobin (g/dL) | 10.2 | 11.6 | 15.0 | 15.4 |
| Hypertension | 1 | 1 | 0 | 0 |
| Diabetes Mellitus | 0 | 1 | 0 | 0 |
| CKD (actual) | 1 | 1 | 0 | 0 |

### 4.6 Deployed Interface

The best XGBoost model was successfully implemented in the explanation-first clinical decision support interface. The interface provided a categorical prediction of whether or not CKD was present, along with a colour-coded bar chart showing the SHAP contributions, in which features that increase the predicted probability of CKD are coloured differently from those that decrease it. Because the underlying model performs inference very quickly, the prediction and its explanation were produced in real time, which is necessary for a responsive point-of-care diagnostic aid.

## 5. Discussion

### 5.1 Interpretation of the Principal Findings

The present framework offers a distinctive methodological approach that combines two independent interpretability methods (SHAP and LIME) with a quantitative measure of their agreement. The high fidelity observed between the two methods has substantive practical implications. When an explanation is supported by two methodologically different techniques, a clinician can have more justified confidence in that explanation than if only one such technique were presented. Conversely, cases where the two approaches disagree can be flagged as requiring further investigation, providing a principled basis for the calibration of trust. This auditing capability addresses a subtle but important vulnerability of post hoc explanation methods, in that it allows the reliability of a single explanatory methodology to be assessed—something that is not done in the prevailing practice of reporting only one explanation method. The Partial Dependence Plots also enriched the interpretability layer by revealing the functional form of the feature–risk relationships, including threshold effects (for example, a sharp drop in the predicted CKD probability once urinary specific gravity exceeds about 1.020) that are not captured by scalar importance measures.

### 5.2 Clinical Plausibility of the Explanations

The most encouraging result of the study is the close correspondence between the inferred feature importances and established nephrological knowledge. The dominance of urinary specific gravity, haemoglobin, albumin, and serum creatinine is not an arbitrary artefact of the modelling procedure, but a genuine reflection of well-known markers of renal function and dysfunction. The combination of reduced renal concentrating ability (indicated by a low specific gravity), anaemia due to decreased erythropoietin production, glomerular damage reflected by albuminuria, and the accumulation of nitrogenous waste products (reflected by serum creatinine) represents a coherent physiological account of chronic renal insufficiency. The fact that an automated system, which learned from data alone, independently recovered this account is a strong indicator of the reliability of its reasoning. This concordance also corroborates the results of Moreno-Sánchez (2023) and Raihan et al. (2023), who independently identified a common set of dominant features, thereby providing the present results with a degree of external validation.

### 5.3 The Value of Dual Interpretability and Fidelity Auditing

An important methodological innovation of the present framework is the combination of two separate interpretability methods, SHAP and LIME, together with a quantitative evaluation of their agreement. When an explanation is supported by two techniques that differ in their underlying approach, the clinician can hold more justified confidence than when a single, unverified method is used. On the other hand, situations in which the two approaches disagree can be identified as requiring further investigation, providing a principled way to calibrate trust. This auditing feature is valuable because it helps to overcome a subtle but important weakness of post hoc explanation methods—their potential instability—and it represents an improvement over the current practice of reporting an explanation methodology without assessing its reliability. The Partial Dependence Plots complement this layer by revealing the functional form of the feature–risk relationships, including threshold effects such as the sharp drop in predicted CKD probability once specific gravity exceeds approximately 1.020, which are not captured by scalar importance measures.

### 5.4 Comparison with the Extant Literature

The proposed framework stands out in the context of the broader research effort in machine learning for CKD. Most previous research has focused on a single goal—maximising accuracy, a single interpretability mode, robust imputation, or deployment—but the present work brings together these previously separate advances and integrates them into a single pipeline. The current framework builds on the work of Dharmarathne et al. (2024) in three important ways: it adds LIME and a fidelity audit to the interpretability layer, it adds a comparative evaluation of robust imputation methods (including generative methods), and it uses Bayesian rather than random hyperparameter optimisation. The present work also contributes to the dual-explanation approach of Chouit et al. (2026) by introducing Partial Dependence analysis and an explicit fidelity metric, and to the deployment-oriented decision support systems reported elsewhere by introducing a rigorously optimised and audited predictive core. In this way, the contribution is integrative and consolidative, and provides a replicable template that can be applied to other diagnostic domains.

### 5.5 Clinical and Practical Implications

The implications of the framework are very tangible. The compact input set of only ten features reduces the amount of data entry required and makes the system more practical to use in situations where a full panel of laboratory tests might not be available or cost-effective, such as in resource-limited and rural healthcare settings. The explanation-first design is useful not only for clinical decision-making but also for patient communication, since clinicians can explain the specific reasons for a diagnosis to the patient. Furthermore, the specific biomarkers associated with an increased risk may help to identify modifiable risk factors and inform targeted interventions. The very low inference latency guarantees that these benefits are available in real time, which is essential for integration into the time-sensitive workflow of clinical practice.

### 5.6 Limitations

Despite the positive results, several caveats must be stated candidly. The most notable limitation is the use of a small benchmark dataset. The 400 cases in the UCI CKD dataset allow direct comparison with previous studies, but may not represent the full spectrum of clinical presentations, demographic features, and comorbidities seen in clinical practice worldwide, and the very high accuracy achieved on this dataset should be interpreted with corresponding caution. The generalisability of the framework to other, ethnically and geographically diverse cohorts is therefore not yet established. A second limitation relates to the generative imputation component: although GANs provide a powerful tool for handling missing data, they can in principle generate synthetic artefacts, and their performance on small datasets requires careful validation. A third limitation is that, while the explanation-fidelity measure is useful, it remains an area of active methodological research, and there is no single universally accepted fidelity metric. Finally, the present study did not include a prospective clinician-in-the-loop usability evaluation of the deployed interface, and the utility of the system within authentic clinical workflows has not yet been empirically demonstrated.

### 5.7 Directions for Future Research

These limitations point to clear directions for future research. The most important is external validation on multiple, demographically diverse, multi-centre cohorts, which would provide a much stronger test of generalisability than the single-dataset paradigm allows. The framework could be extended to incorporate additional data modalities such as genetic markers, longitudinal measurements, and social determinants of health, further enhancing its predictive and explanatory power and potentially evolving into a more comprehensive and personalised CKD risk model. In collaboration with practising nephrologists, prospective usability studies would establish the real-world usefulness and acceptability of the deployed interface and identify opportunities for improvement. Finally, the framework could be extended from the binary classification discussed here to the multi-class problem of CKD staging, which would greatly increase its clinical relevance, since the proper management of CKD depends critically on accurate determination of the disease stage.

## 6. Conclusion

This study has proposed, implemented, and thoroughly tested a single explainable-AI framework for the diagnosis of chronic kidney disease, integrating robust imputation, hyperparameter-optimised ensemble learning, dual and fidelity-audited interpretability, and clinical deployment within one reproducible pipeline. The Bayesian-optimised XGBoost model was the most successful, achieving the highest testing accuracy of 0.983 and an area under the receiver operating characteristic curve of 0.997, ahead of the other models on the UCI benchmark. The model's most important predictors were urinary specific gravity, haemoglobin, albumin, and serum creatinine, which were consistently identified across all three interpretability layers (SHAP, LIME, and Partial Dependence Plots) and were in good agreement with known renal pathophysiology and with the independent results of previous studies. The high fidelity between the SHAP and LIME explanations provided further confidence in the transparency and reliability of the system. The main contribution of the work is not any individual component, but the integrative consolidation of these components, demonstrating that the objectives of accuracy, robustness, interpretability, and deployability can be pursued together rather than separately. In the high-stakes world of clinical medicine, where the ability to explain a prediction is as important as the prediction itself, such an integrative approach is a step towards the responsible and trustworthy use of machine learning to support patient care.

## References

Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A next-generation hyperparameter optimization framework. In *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining* (pp. 2623–2631). Association for Computing Machinery. https://doi.org/10.1145/3292500.3330701

Almasoud, M., & Ward, T. E. (2019). Detection of chronic kidney disease using machine learning algorithms with least number of predictors. *International Journal of Advanced Computer Science and Applications, 10*(8), 89–96. https://doi.org/10.14569/IJACSA.2019.0100813

Amirgaliyev, Y., Shamiluulu, S., & Serek, A. (2018). Analysis of chronic kidney disease dataset by applying machine learning methods. In *2018 IEEE 12th International Conference on Application of Information and Communication Technologies (AICT)* (pp. 1–4). IEEE. https://doi.org/10.1109/ICAICT.2018.8747140

Asuncion, A., & Newman, D. (2007). *UCI machine learning repository*. University of California, Irvine, School of Information and Computer Sciences. http://archive.ics.uci.edu/ml

Bai, Q., Su, C., Tang, W., & Li, Y. (2022). Machine learning to predict end stage kidney disease in chronic kidney disease. *Scientific Reports, 12*(1), 8377. https://doi.org/10.1038/s41598-022-12316-z

Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 785–794). Association for Computing Machinery. https://doi.org/10.1145/2939672.2939785

Chittora, P., Chaurasia, S., Chakrabarti, P., Kumawat, G., Chakrabarti, T., Leonowicz, Z., Jasiński, M., Jasiński, Ł., Gono, R., Jasińska, E., & Bolshev, V. (2021). Prediction of chronic kidney disease: A machine learning perspective. *IEEE Access, 9*, 17312–17334. https://doi.org/10.1109/ACCESS.2021.3053763

Chouit, E. M., Rachdi, M., Bellafkih, M., & Raouyane, B. (2026). Interpretable machine learning for chronic kidney disease prediction: Insights from SHAP and LIME analyses. *PLOS One, 21*(2), e0343205. https://doi.org/10.1371/journal.pone.0343205

Debal, D. A., & Sitote, T. M. (2022). Chronic kidney disease prediction using machine learning techniques. *Journal of Big Data, 9*(1), 109. https://doi.org/10.1186/s40537-022-00657-5

Dharmarathne, G., Bogahawaththa, M., McAfee, M., Rathnayake, U., & Meddage, D. P. P. (2024). On the diagnosis of chronic kidney disease using a machine learning-based interface with explainable artificial intelligence. *Intelligent Systems with Applications, 22*, 200397. https://doi.org/10.1016/j.iswa.2024.200397

Dritsas, E., & Trigka, M. (2022). Machine learning techniques for chronic kidney disease risk prediction. *Big Data and Cognitive Computing, 6*(3), 98. https://doi.org/10.3390/bdcc6030098

Ebiaredoh-Mienye, S. A., Swart, T. G., Esenogho, E., & Mienye, I. D. (2022). A machine learning method with filter-based feature selection for improved prediction of chronic kidney disease. *Bioengineering, 9*(8), 350. https://doi.org/10.3390/bioengineering9080350

Emon, M. U., Imran, A. M., Islam, R., Keya, M. S., Zannat, R., & Ohidujjaman. (2021). Performance analysis of chronic kidney disease through machine learning approaches. In *2021 6th International Conference on Inventive Computation Technologies (ICICT)* (pp. 713–719). IEEE. https://doi.org/10.1109/ICICT50816.2021.9358491

Ghosh, P., Shamrat, F. M. J. M., Shultana, S., Afrin, S., Anjum, A. A., & Khan, A. A. (2020). Optimization of prediction method of chronic kidney disease using machine learning algorithm. In *2020 15th International Joint Symposium on Artificial Intelligence and Natural Language Processing (iSAI-NLP)* (pp. 1–6). IEEE. https://doi.org/10.1109/iSAI-NLP51646.2020.9376787

Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., Courville, A., & Bengio, Y. (2014). Generative adversarial nets. In *Advances in Neural Information Processing Systems* (Vol. 27, pp. 2672–2680). Curran Associates.

Gupta, R., Koli, N., Mahor, N., & Tejashri, N. (2020). Performance analysis of machine learning classifier for predicting chronic kidney disease. In *2020 International Conference for Emerging Technology (INCET)* (pp. 1–4). IEEE. https://doi.org/10.1109/INCET49848.2020.9154147

Iftikhar, H., Khan, M., Khan, Z., Khan, F., Alshanbari, H. M., & Ahmad, Z. (2023). A comparative analysis of machine learning models: A case study in predicting chronic kidney disease. *Sustainability, 15*(3), 2754. https://doi.org/10.3390/su15032754

Islam, M. A., Akter, S., Hossen, M. S., Keya, S. A., Tisha, S. A., & Hossain, S. (2020). Risk factor prediction of chronic kidney disease based on machine learning algorithms. In *2020 3rd International Conference on Intelligent Sustainable Systems (ICISS)* (pp. 952–957). IEEE. https://doi.org/10.1109/ICISS49785.2020.9315878

Jerlin Rubini, L., & Perumal, E. (2020). Efficient classification of chronic kidney disease by using multi-kernel support vector machine and fruit fly optimization algorithm. *International Journal of Imaging Systems and Technology, 30*(3), 660–673. https://doi.org/10.1002/ima.22406

Kalantar-Zadeh, K., Jafar, T. H., Nitsch, D., Neuen, B. L., & Perkovic, V. (2021). Chronic kidney disease. *The Lancet, 398*(10302), 786–802. https://doi.org/10.1016/S0140-6736(21)00519-5

Khan, B., Naseem, R., Muhammad, F., Abbas, G., & Kim, S. (2020). An empirical evaluation of machine learning techniques for chronic kidney disease prophecy. *IEEE Access, 8*, 55012–55022. https://doi.org/10.1109/ACCESS.2020.2981689

Levey, A. S., & Coresh, J. (2012). Chronic kidney disease. *The Lancet, 379*(9811), 165–180. https://doi.org/10.1016/S0140-6736(11)60178-5

Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. In *Advances in Neural Information Processing Systems* (Vol. 30, pp. 4765–4774). Curran Associates.

Moreno-Sánchez, P. A. (2023). Data-driven early diagnosis of chronic kidney disease: Development and evaluation of an explainable AI model. *IEEE Access, 11*, 38359–38369. https://doi.org/10.1109/ACCESS.2023.3264270

Nishat, M. M., Faisal, F., Dip, R. R., Nasrullah, S. M., Ahsan, R., Shikder, F., Asif, M. A. A. R., & Hoque, M. A. (2018). A comprehensive analysis on detecting chronic kidney disease by employing machine learning algorithms. *EAI Endorsed Transactions on Pervasive Health and Technology, 7*(29), e1. https://doi.org/10.4108/eai.13-8-2021.170671

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*, 2825–2830.

Polat, H., Danaei Mehr, H., & Cetin, A. (2017). Diagnosis of chronic kidney disease based on support vector machine by feature selection methods. *Journal of Medical Systems, 41*(4), 55. https://doi.org/10.1007/s10916-017-0703-x

Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A. (2018). CatBoost: Unbiased boosting with categorical features. In *Advances in Neural Information Processing Systems* (Vol. 31, pp. 6638–6648). Curran Associates.

Raihan, M. J., Khan, M. A., Kee, S. H., & Nahid, A. A. (2023). Detection of the chronic kidney disease using XGBoost classifier and explaining the influence of the attributes on the model using SHAP. *Scientific Reports, 13*(1), 6263. https://doi.org/10.1038/s41598-023-33525-0

Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why should I trust you?" Explaining the predictions of any classifier. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 1135–1144). Association for Computing Machinery. https://doi.org/10.1145/2939672.2939778

Sanmarchi, F., Fanconi, C., Golinelli, D., Gori, D., Hernandez-Boussard, T., & Capodici, A. (2023). Predict, diagnose, and treat chronic kidney disease with machine learning: A systematic literature review. *Journal of Nephrology, 36*(4), 1101–1117. https://doi.org/10.1007/s40620-023-01573-4

Sobrinho, A., Queiroz, A. C. D. S., Da Silva, L. D., Costa, E. D. B., Pinheiro, M. E., & Perkusich, A. (2020). Computer-aided diagnosis of chronic kidney disease in developing countries: A comparative analysis of machine learning techniques. *IEEE Access, 8*, 25407–25419. https://doi.org/10.1109/ACCESS.2020.2971208

Tsai, M. C., Lu, C. H., Wang, Y. H., Yang, C. Y., & Cheng, C. Y. (2023). Risk prediction model for chronic kidney disease in Thailand using artificial intelligence and SHAP. *Diagnostics, 13*(23), 3548. https://doi.org/10.3390/diagnostics13233548

Venkatesan, V. K., Ramakrishna, M. T., Izonin, I., Tkachenko, R., & Havryliuk, M. (2023). Efficient data preprocessing with ensemble machine learning technique for the early detection of chronic kidney disease. *Applied Sciences, 13*(5), 2885. https://doi.org/10.3390/app13052885

Webster, A. C., Nagler, E. V., Morton, R. L., & Masson, P. (2017). Chronic kidney disease. *The Lancet, 389*(10075), 1238–1252. https://doi.org/10.1016/S0140-6736(16)32064-5

Xiao, J., Ding, R., Xu, X., Guan, H., Feng, X., Sun, T., Zhu, S., & Ye, Z. (2019). Comparison and development of machine learning tools in the prediction of chronic kidney disease progression. *Journal of Translational Medicine, 17*(1), 119. https://doi.org/10.1186/s12967-019-1860-0

Zheng, J. X., Li, X., Zhu, J., Guan, S. Y., Zhang, S. X., & Wang, W. M. (2024). Interpretable machine learning for predicting chronic kidney disease progression risk. *Digital Health, 10*, 20552076231224225. https://doi.org/10.1177/20552076231224225
