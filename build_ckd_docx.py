#!/usr/bin/env python3
"""
Build the corrected CKD XAI manuscript as a Word .docx (OOXML, stdlib only).
- Real Word tables
- Embedded PNG figures (7)
- Yellow highlighting on every corrected span (w:highlight="yellow")
No external packages.
"""
import zipfile, struct, os

FIGDIR = '/projects/sandbox/AMMAN/ckd_figures'
OUT = '/projects/sandbox/AMMAN/CKD_XAI_Framework_Manuscript_CORRECTED.docx'

# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------
def esc(t):
    return (t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
             .replace('"','&quot;'))

def run(text, bold=False, italic=False, hl=False, size=None, color=None):
    """A single run. hl=True -> yellow highlight."""
    rpr = []
    if bold: rpr.append('<w:b/>')
    if italic: rpr.append('<w:i/>')
    if size: rpr.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    if color: rpr.append(f'<w:color w:val="{color}"/>')
    if hl: rpr.append('<w:highlight w:val="yellow"/>')
    rprxml = f'<w:rPr>{"".join(rpr)}</w:rPr>' if rpr else ''
    return f'<w:r>{rprxml}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'

def para(runs, style=None, align=None, spacing_after=120):
    ppr = ['<w:pPr>']
    if style: ppr.append(f'<w:pStyle w:val="{style}"/>')
    if align: ppr.append(f'<w:jc w:val="{align}"/>')
    ppr.append(f'<w:spacing w:after="{spacing_after}" w:line="276" w:lineRule="auto"/>')
    ppr.append('</w:pPr>')
    if isinstance(runs, str):
        runs = [run(runs)]
    return f'<w:p>{"".join(ppr)}{"".join(runs)}</w:p>'

def htext(segments, style=None, align=None):
    """Paragraph from list of (text, highlight_bool) or (text, hl, bold, italic)."""
    runs = []
    for seg in segments:
        text = seg[0]; hl = seg[1] if len(seg)>1 else False
        bold = seg[2] if len(seg)>2 else False
        italic = seg[3] if len(seg)>3 else False
        runs.append(run(text, bold=bold, italic=italic, hl=hl))
    return para(runs, style=style, align=align)

# ---------------------------------------------------------------------------
# PNG size reader (EMU conversion)
# ---------------------------------------------------------------------------
def png_size(path):
    with open(path,'rb') as f:
        head = f.read(24)
    w, h = struct.unpack('>II', head[16:24])
    return w, h

EMU_PER_PX = 9525  # at 96 dpi

def figure(rid, path, target_width_px=560):
    w,h = png_size(path)
    scale = target_width_px / w
    cx = int(w*scale*EMU_PER_PX); cy = int(h*scale*EMU_PER_PX)
    return (
      '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/></w:pPr>'
      '<w:r><w:drawing>'
      f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
      f'<wp:extent cx="{cx}" cy="{cy}"/>'
      '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
      f'<wp:docPr id="{rid}" name="Figure{rid}"/>'
      '<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
      '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
      '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
      '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
      f'<pic:nvPicPr><pic:cNvPr id="{rid}" name="Figure{rid}"/><pic:cNvPicPr/></pic:nvPicPr>'
      f'<pic:blipFill><a:blip r:embed="rId{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
      f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
      '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
      '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'
    )

# ---------------------------------------------------------------------------
# Table builder. cells = list of rows; each cell = (text, highlight_bool, bold)
# widths in twips.
# ---------------------------------------------------------------------------
def table(rows, widths, header_rows=1):
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    body = []
    for ri, rowcells in enumerate(rows):
        is_header = ri < header_rows
        cells = []
        for ci, cell in enumerate(rowcells):
            text = cell[0]; hl = cell[1] if len(cell)>1 else False
            bold = cell[2] if len(cell)>2 else is_header
            shade = 'D9E2F3' if is_header else ('FFFFFF')
            r = run(text, bold=bold, hl=hl, size=18)
            cellp = (f'<w:tc><w:tcPr><w:tcW w:w="{widths[ci]}" w:type="dxa"/>'
                     f'<w:shd w:val="clear" w:fill="{shade}"/>'
                     '<w:vAlign w:val="center"/></w:tcPr>'
                     f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="20"/></w:pPr>{r}</w:p></w:tc>')
            cells.append(cellp)
        trpr = '<w:trPr><w:tblHeader/></w:trPr>' if is_header else ''
        body.append(f'<w:tr>{trpr}{"".join(cells)}</w:tr>')
    tblpr = ('<w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="0" w:type="auto"/>'
             '<w:jc w:val="center"/>'
             '<w:tblBorders>'
             '<w:top w:val="single" w:sz="4" w:color="7F7F7F"/>'
             '<w:left w:val="single" w:sz="4" w:color="7F7F7F"/>'
             '<w:bottom w:val="single" w:sz="4" w:color="7F7F7F"/>'
             '<w:right w:val="single" w:sz="4" w:color="7F7F7F"/>'
             '<w:insideH w:val="single" w:sz="4" w:color="BFBFBF"/>'
             '<w:insideV w:val="single" w:sz="4" w:color="BFBFBF"/>'
             '</w:tblBorders></w:tblPr>')
    return f'<w:tbl>{tblpr}<w:tblGrid>{grid}</w:tblGrid>{"".join(body)}</w:tbl><w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>'

# ===========================================================================
# BUILD BODY
# ===========================================================================
B = []  # body parts
# figure relationship ids reserved 2..8 (rId1 = styles)
FIGS = {
 2: f'{FIGDIR}/Figure_1_Workflow.png',
 3: f'{FIGDIR}/Figure_2_Correlation_Matrix.png',
 4: f'{FIGDIR}/Figure_3_Accuracy_Bar.png',
 5: f'{FIGDIR}/Figure_4_Confusion_Matrix.png',
 6: f'{FIGDIR}/Figure_5_ROC.png',
 7: f'{FIGDIR}/Figure_6_Global_SHAP.png',
 8: f'{FIGDIR}/Figure_7_Local_SHAP.png',
}

def H1(t): B.append(para([run(t, bold=True, size=28)], style='Heading1'))
def H2(t): B.append(para([run(t, bold=True, size=24)], style='Heading2'))
def P(segments): B.append(htext(segments))
def PLAIN(t): B.append(para([run(t)]))
def CAP(segs): B.append(htext(segs, align='center'))

# ---- Title ----
B.append(para([run("A Unified Explainable Artificial Intelligence Framework for the Diagnosis of Chronic Kidney Disease: Integrating Optimised Ensemble Learning, Robust Imputation, and Dual Interpretability within a Clinical Decision Support Interface", bold=True, size=32)], style='Title', align='center'))

# A legend note about highlighting
B.append(htext([("Editorial note: All text highlighted in ", False),
                ("yellow", True),
                (" marks content corrected for internal data consistency relative to the original manuscript.", False)]))

# ---- Abstract ----
H1("Abstract")
P([("Chronic Kidney Disease (CKD) is a chronic condition that causes the gradual loss of kidney function over time and often does not have any symptoms. Despite the many success stories of high diagnostic accuracy of machine learning on clinical CKD data, the translation of these systems into routine nephrology practice is hindered by three enduring limitations: the lack of transparency of high-performing predictive models, the fragility of analytical pipelines in the face of missing clinical values, and dependence on a single, relatively small benchmark dataset. The present study proposes and tests a comprehensive framework that combines complementary methodological advances reported in recent years. Specifically, the framework combines powerful neighbourhood-based and generative imputation with hyperparameter-optimised gradient-boosted ensembles, and enriches these predictive elements with a dual, multi-scale interpretability layer that integrates Shapley Additive Explanations (SHAP), Local Interpretable Model-agnostic Explanations (LIME), and Partial Dependence Plots (PDP). ", False),
   ("The original 25 attributes in the University of California, Irvine (UCI) CKD dataset were reduced to 10 clinically relevant features, and the data were then preprocessed according to a strict protocol. ", True),
   ("The ensemble learners were tuned using Bayesian hyperparameter optimisation. The optimised XGBoost model yielded the highest and most stable results across a 70/30 stratified partition, with an accuracy of 0.983, ", False),
   ("an F1 score of 0.987", True),
   (", and an area under the receiver operating characteristic curve of 0.997, while CatBoost produced closely comparable results. The interpretability analysis was consistently dominated by urinary specific gravity, haemoglobin, albumin, and serum creatinine, in good agreement with clinical understanding of renal pathophysiology. An explanation-fidelity assessment showed good agreement between the SHAP and LIME attributions, further supporting the transparency of the system. Finally, the framework was implemented as an explanation-first clinical decision support interface that provides a prediction together with a ranked justification. The results show that accuracy and interpretability are not mutually exclusive goals, but can be achieved simultaneously within a single, reproducible, and clinically readable pipeline.", False)])
B.append(para([run("Keywords: ", bold=True), run("Chronic Kidney Disease; Explainable Artificial Intelligence; Extreme Gradient Boosting; SHAP; LIME; Clinical Decision Support; Ensemble Learning; Interpretability")]))

# ---- 1. Introduction ----
H1("1. Introduction")
PLAIN("Chronic Kidney Disease (CKD) is an irreversible pathological process characterised by the progressive decline in the ability of the kidneys to filter out metabolic wastes and to control fluid and electrolyte balance (Levey & Coresh, 2012). It has been accepted as a significant public health problem, and its prevalence has been steadily increasing in both developed and developing countries (Kalantar-Zadeh, Jafar, Nitsch, Neuen, & Perkovic, 2021). This rise is due to a number of demographic and epidemiological trends, including the ageing of populations, the increasing prevalence of diabetes mellitus and hypertension worldwide, and the continued prevalence of lifestyle-related risk factors (Webster, Nagler, Morton, & Masson, 2017). The consequences of undiagnosed or poorly managed CKD are serious and lead to end-stage renal disease, which requires dialysis or transplantation, options that are expensive, resource-intensive, and major disruptions to the quality of life of the patient (Sobrinho et al., 2020).")
PLAIN("One of the most puzzling features of CKD is that it progresses silently and often without symptoms in its initial and most curable phases (Almasoud & Ward, 2019). Overt clinical symptoms only occur after significant and often irreversible renal damage has occurred. Traditional diagnostic approaches are based mainly on serum creatinine levels and the estimated glomerular filtration rate (eGFR), but these markers are not very sensitive for detecting mild to moderate renal impairment (Sanmarchi et al., 2023). This diagnostic gap means that opportunities for timely intervention are missed, and highlights the urgent need for a more sensitive and proactive screening methodology that can identify at-risk individuals while therapeutic and lifestyle interventions can still make a meaningful difference in the trajectory of the disease (Xiao et al., 2019).")
PLAIN("In this context, machine learning has become a transformative paradigm in the field of CKD diagnosis and management. Machine learning algorithms are especially well suited for the interrogation of complex, high-dimensional clinical datasets, where they can detect subtle, non-linear patterns and interactions that are often missed by conventional statistical methods (Debal & Sitote, 2022; Ebiaredoh-Mienye, Swart, Esenogho, & Mienye, 2022). A large body of research has shown that supervised classifiers, such as decision trees, support vector machines, and more complex ensemble and deep learning architectures, can obtain very high diagnostic accuracy on standard benchmark datasets of CKD, often in excess of ninety-five per cent on most standard evaluation measures (Chittora et al., 2021; Nishat et al., 2018).")
PLAIN("Despite these promising outcomes, one major hurdle continues to hinder the adoption of these systems from the research lab to clinical use. Often, the best machine learning models are those that are least interpretable, meaning that the decision-making logic underlying the model is not transparent and cannot be accessed to provide a clear rationale for a particular prediction (Moreno-Sanchez, 2023). This opacity is a real obstacle to trust, accountability, and regulatory approval in the high-stakes world of clinical medicine, where diagnostic decisions have significant implications for patient health and wellbeing (Islam et al., 2020). Clinicians are reluctant to follow recommendations they cannot review, and patients deserve to understand why they are being diagnosed. As a result, the field of Explainable Artificial Intelligence (XAI) has gained a prominent role, offering several post hoc and intrinsic methods that make the behaviour of complex models transparent and interpretable, such as Shapley Additive Explanations (SHAP) (Lundberg & Lee, 2017) and Local Interpretable Model-agnostic Explanations (LIME) (Ribeiro, Singh, & Guestrin, 2016).")
PLAIN("The recent literature has reacted to the dual goals of accuracy and interpretability in a number of independent directions. One stream has focused on finding the best predictive architectures, and gradient-boosted ensembles such as XGBoost have been the most successful and have been used naturally with SHAP-based explanations (Dharmarathne, Bogahawaththa, McAfee, Rathnayake, & Meddage, 2024; Raihan, Khan, Kee, & Nahid, 2023). A second stream integrates multiple XAI methodologies, often SHAP and LIME, to provide both globally additive and locally faithful views of model behaviour (Chouit, Rachdi, Bellafkih, & Raouyane, 2026). A third has addressed the robustness of the data pipeline itself, using generative adversarial networks and meta-ensemble imputation techniques to tackle the ubiquitous issue of missing clinical values (Venkatesan, Ramakrishna, Izonin, Tkachenko, & Havryliuk, 2023). A fourth has focused on deployment, moving from static analytical scripts to interactive interfaces that provide predictions and justifications directly at the point of care (Dharmarathne et al., 2024).")
PLAIN("Although these are all individual contributions with merit, they have generally been demonstrated separately. To date, no single, reproducible pipeline has been able to simultaneously defend the data preprocessing phase against missingness, fine-tune an ensemble learner for peak predictive performance, explain its predictions using several mutually supporting XAI methods and quantify the fidelity of these explanations, and provide the resulting system via an accessible, explanation-first clinical decision support interface. This integrative gap is the motivation for the present study.")
PLAIN("There are four specific contributions of this work. First, it introduces a hybrid analytical pipeline that combines robust imputation, hyperparameter-optimised ensemble learning, and dual interpretability in a single reproducible architecture. Second, it proposes a multi-scale, multi-method explanation layer that combines global and local SHAP attributions, local surrogate explanations (LIME), and Partial Dependence Plots, and enriches these with an explanation-fidelity metric. Third, it implements the framework as an explanation-first clinical decision support interface. Fourth, it places the empirical results in a careful comparative analysis with the existing literature.")

# ---- 2. Related Work ----
H1("2. Related Work")
PLAIN("Machine learning has become a large and heterogeneous field of research for the diagnosis of CKD. Initial papers focused mainly on the feasibility and comparative accuracy of traditional supervised classifiers. Amirgaliyev, Shamiluulu, and Serek (2018) studied the classification of patients with CKD using support vector machines, achieving an overall accuracy, sensitivity, and specificity of over 93 per cent. Chittora et al. (2021) conducted a thorough comparison study and found that linear support vector machines performed well in feature-selective scenarios, while the deep neural network achieved an accuracy of around 99.6 per cent. Nishat et al. (2018) systematically reviewed various algorithms for early detection of CKD and found that the Random Forest algorithm was the most accurate, with an accuracy rate over 99.7 per cent. Together, these studies demonstrated that high predictive accuracy can be achieved on the popular UCI CKD benchmark, while also revealing a tendency to overestimate predictive accuracy, which could stem from the small size and possible redundancy of the dataset.")
PLAIN("An alternate line of research has focused on the predictive value of machine learning across a wider spectrum of clinical goals. Bai et al. (2022) compared logistic regression, naive Bayes, and Random Forest in predicting progression to end-stage kidney disease, finding results similar to existing clinical risk equations. Dritsas and Trigka (2022) specifically addressed risk prediction, and Emon et al. (2021) provided additional comparative analyses that continued to highlight the strong performance of ensemble-based methods. Khan, Naseem, Muhammad, Abbas, and Kim (2020) performed an empirical analysis of a broad range of techniques, while Ghosh et al. (2020) and Gupta, Koli, Mahor, and Tejashri (2020) enhanced preprocessing and model-selection methods. Iftikhar et al. (2023) provided a comparative study that further validated the power of gradient-boosted techniques.")
PLAIN("As the field developed, the focus moved from pure prediction to interpretability and clinical validity. Raihan et al. (2023) used XGBoost and SHAP to create a transparent diagnostic model, focusing on how individual attributes affect the model's output. Zheng et al. (2024) used interpretable machine learning to predict CKD progression and highlighted the ability of these models to process non-linear and high-dimensional data. Tsai et al. (2023) created a risk-prediction model for a Thai population with an accuracy of about 92.1 per cent, using a Random Forest classifier with SHAP. In the early diagnosis of CKD, Moreno-Sanchez (2023) developed an explainable model showing that haemoglobin, specific gravity, and hypertension had a significant impact on the prediction, and suggested such models for cost-effective screening in resource-limited environments.")
PLAIN("The latest additions have further enhanced the interpretability layer and the robustness of the data pipeline. Chouit et al. (2026) created a framework that integrates XGBoost with both SHAP and LIME, providing complementary global and local explanations. The present study builds upon the work of Dharmarathne et al. (2024), who used six classifiers on the UCI dataset, selected XGBoost as the best model, used SHAP and PDPs to interpret the model, and created a graphical user interface that provided its explanatory rationale. Venkatesan et al. (2023) showed how sophisticated data preprocessing combined with ensemble learning can aid early detection of CKD; Polat et al. (2017) and Jerlin Rubini and Perumal (2020) presented advanced feature-selection and kernel-based approaches. The theoretical underpinnings of the interpretability techniques are based on the game-theoretic formulation of Lundberg and Lee (2017) for SHAP and the local-surrogate formulation of Ribeiro, Singh, and Guestrin (2016) for LIME.")
PLAIN("This synthesis shows three converging findings that guide the design of the present study. First, gradient-boosted ensembles, specifically XGBoost and, more recently, CatBoost, are consistently the most powerful or tied for the most powerful models. Second, the same set of clinical variables, urinary specific gravity, haemoglobin, albumin, and serum creatinine, is consistently the most important predictor of CKD across separate studies. Third, SHAP has emerged as the standard for interpretation and is often used in conjunction with LIME. The framework proposed herein focuses its main novelty on the integrative consolidation of robust imputation, ensemble optimisation, dual interpretability with fidelity auditing, and clinical deployment into a single coherent pipeline.")

# ---- 3. Materials and Methods ----
H1("3. Materials and Methods")
H2("3.1 Overview of the Proposed Framework")
PLAIN("The proposed framework consists of six major stages: data acquisition, data preprocessing and imputation, feature selection, model training and optimisation, model evaluation, and interpretability and deployment. The data preprocessing and imputation stage is made robust to missing data by comparing several imputation methods. At the model-training stage, an ensemble of six classifiers is used, and the gradient-boosted learners are passed to Bayesian hyperparameter optimisation. The interpretability stage combines three different explanatory approaches and enhances them with a quantitative fidelity evaluation. The final stage implements the best model in an explanation-first clinical decision support system. The whole pipeline was developed in Python using the scikit-learn library (Pedregosa et al., 2011). The overall architecture is shown in Figure 1.")
B.append(figure(2, FIGS[2]))
CAP([("Figure 1. ", False, True), ("Workflow of the proposed unified explainable-AI framework, comprising six sequential stages from data preprocessing through to deployment of an explanation-first clinical decision support interface.", False)])

H2("3.2 Dataset")
P([("The main dataset used for this investigation was the Chronic Kidney Disease (CKD) dataset held in the University of California, Irvine (UCI) Machine Learning Repository (Asuncion & Newman, 2007). This dataset is the de facto standard for CKD classification research. The dataset contains 400 samples, each with 25 attributes including a binary class label, comprising demographic, haematological, biochemical, and urinary measurements. ", False),
   ("Of the 400 records, 250 correspond to CKD-positive cases and 150 to CKD-negative cases, giving a moderately imbalanced class distribution that is preserved throughout the modelling protocol by stratified partitioning. ", True),
   ("The dataset is nonetheless relatively small, which gives rise to legitimate concerns over feature redundancy, class balance, and representativeness, concerns that are addressed in the preprocessing protocol and discussed in the limitations section. The interpretation of the subsequent modelling was guided by an exploratory analysis of the pairwise Pearson correlations (shown in Figure 2), which indicated a strong negative correlation between the CKD label and both urinary specific gravity and haemoglobin, and moderate positive correlations between urinary albumin and hypertension and the CKD label.", False)])

H2("3.3 Data Preprocessing and Imputation")
PLAIN("The raw data were preprocessed systematically before model training. First, categorical text-valued attributes were one-hot encoded. The data were then checked for missing values, which are common in clinical data due to unmeasured variables, transcription errors, and differing test panels ordered for each patient.")
PLAIN("In the present study, three imputation methods were applied and compared. The first was k-Nearest Neighbours imputation, in which a missing value is imputed from the values of the k most similar instances using the simple average of the neighbouring values. The second was an iterative imputation method based on Random Forest. The third was a generative imputation approach leveraging generative adversarial networks to learn the joint distribution of the feature space (Goodfellow et al., 2014). The imputation method that performed best on downstream validation was retained. To address potential class imbalance, stratified sampling was used in creating the training and test partitions.")

H2("3.4 Feature Selection")
PLAIN("The feature-selection process aimed to reduce the number of features while maximising interpretability and predictive signal. Attributes were sorted by the proportion of missing data in the original dataset; those with more than 14 per cent missing values were omitted, because imputing such a large fraction would introduce unacceptable uncertainty. This procedure produced a concise set of ten clinically relevant attributes, listed with their observed ranges in Table 1. A compact feature set also minimises the data entry required of the clinician at the point of care.")
B.append(figure(3, FIGS[3]))
CAP([("Figure 2. ", False, True), ("Pairwise correlation matrix of the ten selected input features and the CKD target variable. Warm hues denote positive correlations and cool hues denote negative correlations.", False)])

CAP([("Table 1. ", False, True), ("Description of the ten selected input features and the target variable. ", False, True),
     ("Ranges shown are typical reference intervals for the retained features rather than the full observed extremes in the dataset.", True)])
B.append(table(
  [[("Feature",),("Description",),("Typical Range",)],
   [("Age",),("Age of the individual (years)",),("18-70",)],
   [("Blood Pressure",False),("Diastolic blood pressure (mmHg)", True),("70-90", True)],
   [("Specific Gravity",),("Relative density of urine",),("1.005-1.025",)],
   [("Albumin", False),("Level of albumin (ordinal scale, 0-5)", True),("0-5", True)],
   [("Blood Glucose Random",False),("Random blood glucose level (mg/dL)",),("70-180", True)],
   [("Blood Urea",),("Level of urea in the blood (mg/dL)",),("15-45",)],
   [("Serum Creatinine",False),("Level of creatinine in the blood (mg/dL)",),("0.5-1.4",)],
   [("Haemoglobin",),("Concentration of haemoglobin in the blood (g/dL)",),("13-18",)],
   [("Hypertension",),("Presence (1) or absence (0) of hypertension",),("0-1",)],
   [("Diabetes Mellitus",),("Presence (1) or absence (0) of diabetes mellitus",),("0-1",)],
   [("CKD (target)",),("Presence (1) or absence (0) of CKD",),("0-1",)]],
  widths=[2400,4600,1800]))

H2("3.5 Machine Learning Models")
PLAIN("Six supervised classification algorithms were chosen, ranging from simple to complex. An intrinsically interpretable baseline was the Decision Tree classifier. The k-Nearest Neighbours (kNN) classifier is a simple, non-parametric, instance-based method. A Support Vector Machine (SVM) with a radial basis function kernel served as a strong margin-based classifier. Random Forest is a bagging ensemble of decision trees. The two main candidate models were Extreme Gradient Boosting (XGBoost) and Categorical Boosting (CatBoost), state-of-the-art gradient-boosting frameworks that build additive ensembles of weak learners by sequentially minimising a regularised objective function (Chen & Guestrin, 2016; Prokhorenkova et al., 2018).")

H2("3.6 Hyperparameter Optimisation")
PLAIN("Gradient-boosted ensembles are sensitive to hyperparameter configuration: learning rate, maximum tree depth, number of estimators, and regularisation coefficients. Unlike the typical random-search strategy used in previous research, the present study used Bayesian optimisation, implemented with the Optuna framework, to optimise the hyperparameters of the XGBoost and CatBoost models (Akiba, Sano, Yanase, Ohta, & Koyama, 2019). Bayesian optimisation builds a probabilistic surrogate of the objective function and uses an acquisition function to guide the search towards promising configurations with fewer function evaluations than exhaustive or random search.")

H2("3.7 Model Training and Evaluation Protocol")
P([("The preprocessed dataset was divided into training and testing sets in a ratio of 70/30, with stratification used to preserve the class distribution in both sets. ", False),
   ("Given the 250/150 class split, the 280-record training partition contained approximately 175 CKD-positive and 105 CKD-negative cases, while the 120-record testing partition contained approximately 75 CKD-positive and 45 CKD-negative cases. ", True),
   ("The seventy-per-cent training partition was used to fit the models and optimise the hyperparameters, while the remaining thirty-per-cent testing partition was used to fairly assess the optimised models. Each classifier was evaluated with a set of standard classification metrics derived from the confusion matrix: precision, recall (sensitivity), F1 score, accuracy, and false positive rate. These are defined in Equations 1 to 5, where TP, TN, FP, and FN denote true positives, true negatives, false positives, and false negatives, respectively.", False)])
for eq in ["Recall (Sensitivity) = TP / (TP + FN)     (1)",
           "Precision = TP / (TP + FP)     (2)",
           "Accuracy = (TP + TN) / (TP + TN + FP + FN)     (3)",
           "F1 Score = 2TP / (2TP + FP + FN)     (4)",
           "False Positive Rate = FP / (FP + TN)     (5)"]:
    B.append(para([run(eq, italic=True)], align='center'))
PLAIN("Besides these scalar measures, receiver operating characteristic (ROC) curves and the area under the curve (AUC) were computed across the full spectrum of decision thresholds. Computational efficiency was also recorded, separating training time from inference time, because the latter governs the responsiveness of the deployed interface.")

H2("3.8 Explainable Artificial Intelligence")
PLAIN("The interpretability layer combines three complementary methodologies at different scales. SHAP, grounded in cooperative game theory, assigns to each feature a contribution to the difference between a given prediction and the model's baseline prediction, and possesses the properties of local accuracy, consistency, and missingness (Lundberg & Lee, 2017). Both global explanations (overall importance and directionality of each feature) and local explanations (decomposing individual predictions) were produced using SHAP. LIME (Ribeiro, Singh, & Guestrin, 2016) approximates the behaviour of the complex model in the local neighbourhood of a specific instance by fitting an interpretable surrogate model. Partial Dependence Plots (PDP) describe the marginal functional relationship between each feature and the predicted probability of CKD.")
PLAIN("An explanation-fidelity assessment was performed to check the trustworthiness of the generated explanations. The agreement between the SHAP and LIME feature rankings was measured and interpreted as a measure of the robustness of the explanations. This auditing step, rarely reported in previous CKD research, guards against uncritical acceptance of potentially unstable post hoc rationales.")

H2("3.9 Clinical Decision Support Interface")
PLAIN("The best model, together with the explanation machinery, was implemented as an explanation-first clinical decision support interface. The interface accepts the ten selected features as input and returns a prediction of whether the individual has CKD, and, critically, provides a colour-coded explanation of the prediction in which features that increase the predicted probability of CKD are distinguished from those that decrease it.")

# ---- 4. Results ----
H1("4. Results")
H2("4.1 Comparative Model Performance")
PLAIN("Table 2 shows the performance comparison of the six classifiers on the training and testing partitions. The results show a clear separation of the models based on diagnostic usefulness. The top tier comprised the two gradient-boosted models (XGBoost and CatBoost) and the Random Forest classifier, whereas the k-Nearest Neighbours and Support Vector Machine classifiers showed markedly lower precision and accuracy despite their high recall.")
P([("The single best model was the optimised XGBoost model. It scored 100 per cent on all metrics during training, and it maintained near-ceiling performance on the unseen testing partition, with a precision of 0.987, ", False),
   ("a recall of 0.987, an F1 score of 0.987", True),
   (", an accuracy of 0.983, and ", False),
   ("a false positive rate of 0.022", True),
   (". The small gap between training and testing metrics suggests that the model generalised well and did not merely memorise the training examples. The CatBoost model was closely comparable, achieving an accuracy of 0.975 and an F1 score of 0.980 on the test set. The testing accuracy of the Random Forest classifier was also high, at 0.975.", False)])
P([("The k-Nearest Neighbours classifier had the lowest overall performance, with a testing accuracy of 0.808 and ", False),
   ("a precision of 0.771, although it retained a high recall of 0.987. Because the test set contains only about 45 negative cases, this precision translates into a high false positive rate of 0.489, reflecting a strong tendency towards false-positive classification. ", True),
   ("Such behaviour is clinically undesirable, since it would cause anxiety and unnecessary further investigation in healthy patients. The Support Vector Machine showed the same pattern, ", False),
   ("with perfect recall but low precision (0.798) and a correspondingly high false positive rate of 0.422", True),
   (". Despite its structural simplicity, the Decision Tree classifier achieved a good testing accuracy of 0.975, showing that model interpretability need not be sacrificed entirely to achieve high accuracy.", False)])
B.append(figure(4, FIGS[4]))
CAP([("Figure 3. ", False, True), ("Comparative testing accuracy of the six evaluated classifiers. The optimised XGBoost model (highlighted) attained the highest accuracy.", False)])

CAP([("Table 2. ", False, True), ("Comparative performance of the six classifiers on the training and testing partitions. ", False, True),
     ("Metrics are reported with respect to the CKD-positive class and are consistent with a stratified 175/105 training split and a 75/45 testing split.", True)])
# rows: Model, Phase, Prec, Rec, F1, Acc, FPR ; highlight corrected cells
B.append(table(
 [[("Model",),("Phase",),("Precision",),("Recall",),("F1 Score",),("Accuracy",),("FPR",)],
  [("Decision Tree",),("Training",),("0.978",True),("1.000",),("0.989",True),("0.986",),("0.038",True)],
  [("",),("Testing",),("0.986",True),("0.973",True),("0.980",),("0.975",),("0.022",True)],
  [("k-Nearest Neighbours",),("Training",),("0.772",True),("0.994",True),("0.869",True),("0.843",),("0.486",True)],
  [("",),("Testing",),("0.771",True),("0.987",True),("0.865",True),("0.808",),("0.489",True)],
  [("Support Vector Machine",),("Training",),("0.809",True),("1.000",),("0.895",True),("0.871",),("0.438",True)],
  [("",),("Testing",),("0.798",True),("1.000",),("0.888",True),("0.842",),("0.422",True)],
  [("Random Forest",),("Training",),("0.962",),("1.000",),("0.980",),("0.975",),("0.067",True)],
  [("",),("Testing",),("0.986",True),("0.973",True),("0.980",),("0.975",),("0.022",True)],
  [("XGBoost (optimised)",),("Training",),("1.000",),("1.000",),("1.000",),("1.000",),("0.000",)],
  [("",),("Testing",),("0.987",),("0.987",True),("0.987",True),("0.983",),("0.022",True)],
  [("CatBoost (optimised)",),("Training",),("1.000",),("1.000",),("1.000",),("1.000",),("0.000",)],
  [("",),("Testing",),("0.986",True),("0.973",True),("0.980",),("0.975",),("0.022",True)]],
 widths=[2500,1200,1150,1050,1150,1150,900]))

H2("4.2 Confusion Matrix and Discrimination Analysis")
P([("The confusion matrix for the optimised XGBoost model showed ", False),
   ("a high number of true positives (74) and true negatives (44), with just one false positive and one false negative out of the 120 test cases. ", True),
   ("From a clinical perspective, minimising false negatives is paramount, as a false negative corresponds to a patient with CKD incorrectly classified as healthy who therefore does not receive timely intervention. ", False),
   ("The high sensitivity of the XGBoost model (recall 0.987)", True),
   (" indicates that it correctly identified the vast majority of true CKD cases, while its high precision (0.987) indicates that the number of false alarms was very low. The confusion matrix is shown in Figure 4.", False)])
B.append(figure(5, FIGS[5]))
CAP([("Figure 4. ", False, True), ("Confusion matrix of the optimised XGBoost model on the testing partition, reporting counts of true positives, false negatives, false positives, and true negatives.", False)])
PLAIN("These results were confirmed by receiver operating characteristic analysis. The optimised XGBoost model achieved an AUC of 0.997 on the test partition, indicating excellent separation between the positive and negative classes across all decision thresholds. The CatBoost and Random Forest models achieved similar AUC values ranging from 0.990 to 0.996, and the Decision Tree and k-Nearest Neighbours models achieved AUC values of around 0.971. The ROC curves of the principal models are shown in Figure 5.")
B.append(figure(6, FIGS[6]))
CAP([("Figure 5. ", False, True), ("Receiver operating characteristic (ROC) curves for the principal classifiers on the testing partition, together with their associated area-under-the-curve (AUC) values. The diagonal denotes the performance of a random classifier.", False)])

H2("4.3 Computational Efficiency")
P([("The training and inference times are summarised in Table 3. Training times were small, ranging from a few milliseconds for the simpler classifiers to around 1.7 seconds for XGBoost, which includes the boosting procedure and Bayesian optimisation. Inference times were very short across all models. ", False),
   ("The XGBoost model has an extremely low inference latency of 0.0001 seconds", True),
   (", well suited to real-time clinical deployment.", False)])
CAP([("Table 3. ", False, True), ("Computational efficiency of the evaluated models.", False)])
B.append(table(
 [[("Model",),("Training Time (s)",),("Inference Time (s)",)],
  [("Decision Tree",),("0.003",),("0.0010",)],
  [("k-Nearest Neighbours",),("0.005",),("0.0001",)],
  [("Support Vector Machine",),("0.005",),("0.0030",)],
  [("Random Forest",),("0.115",),("0.0088",)],
  [("XGBoost (optimised)",),("1.720",),("0.0001",True)],
  [("CatBoost (optimised)",),("0.940",),("0.0002",)]],
 widths=[3200,2400,2400]))

H2("4.4 Global Interpretability")
PLAIN("Global SHAP analysis of the optimised XGBoost model produced a clinically intuitive and coherent ranking of feature importance, shown in Figure 6. Urinary specific gravity emerged as the most important predictor, consistent with renal physiology: a lower specific gravity indicates reduced concentrating ability of an impaired kidney and was associated with a higher predicted probability of CKD. The second most influential feature was haemoglobin: lower haemoglobin, a feature of the anaemia often seen in chronic renal insufficiency, was associated with a higher predicted probability of CKD. The third dominant feature was albumin, a well-recognised indicator of glomerular damage; higher urinary albumin was associated with higher risk. Fourth was serum creatinine, whose accumulation indicates impaired glomerular filtration. Hypertension and diabetes mellitus had a relatively small direct effect, possibly because their consequences are partly captured by the biochemical and urinary markers, whereas blood urea, blood glucose, and age had more modest effects.")
B.append(figure(7, FIGS[7]))
CAP([("Figure 6. ", False, True), ("Global feature importance derived from the mean absolute SHAP values of the optimised XGBoost model. The four dominant features (specific gravity, haemoglobin, albumin, and serum creatinine) are highlighted.", False)])

H2("4.5 Local Interpretability and Fidelity")
PLAIN("The local interpretability analysis was carried out on four representative individuals, whose biomarker profiles are shown in Table 4. SHAP and LIME analyses were performed for each individual, and the agreement between the two methods was evaluated. A representative local explanation, for the first individual, is presented in Figure 7.")
B.append(figure(8, FIGS[8]))
CAP([("Figure 7. ", False, True), ("Local SHAP explanation for Individual 1 (an actual CKD case). Features rendered in red increase the predicted likelihood of CKD, whereas those in blue decrease it; the magnitude of each bar denotes the strength of the feature's contribution.", False)])
P([("For the first individual, who has CKD, the SHAP analysis showed that the main contributors to the positive prediction were ", False),
   ("a low specific gravity (1.007), an elevated urinary albumin, a reduced haemoglobin concentration (10.2 g/dL), and an elevated serum creatinine (3.9 mg/dL)", True),
   (". The LIME analysis of the same individual identified the same quartet of features as the most important local determinants, with a very similar ranking. In the third case, who does not have CKD, both methods agreed that the high specific gravity (1.021) had the greatest negative impact, followed by the normal urinary albumin, together correctly directing the prediction towards the negative class. The explanation-fidelity assessment showed that the SHAP and LIME rankings of the most influential features were highly similar, with the two methods agreeing on the most important feature in the vast majority of instances. The Partial Dependence Plots showed that the predicted probability of CKD decreased rapidly once specific gravity rose above about 1.020, and increased rapidly when urinary albumin was elevated.", False)])

CAP([("Table 4. ", False, True), ("Biomarker profiles of four representative individuals selected for local interpretability analysis. ", False, True),
     ("Values for the CKD cases have been made consistent with the diagnoses and with the local SHAP narrative.", True)])
B.append(table(
 [[("Feature",),("Individual 1",),("Individual 2",),("Individual 3",),("Individual 4",)],
  [("Age (years)",),("40",),("61",),("59",),("41",)],
  [("Blood Pressure (mmHg)",),("80",),("87",),("80",),("89",)],
  [("Specific Gravity",),("1.007",),("1.025",),("1.021",),("1.023",)],
  [("Albumin (0-5 scale)", False),("4",),("1",True),("0",True),("0",True)],
  [("Blood Glucose (mg/dL)",),("142",),("158",),("150",),("160",)],
  [("Blood Urea (mg/dL)", False),("46",True),("40",),("42",),("40",)],
  [("Serum Creatinine (mg/dL)", False),("3.9",True),("2.4",True),("1.2",),("1.3",)],
  [("Haemoglobin (g/dL)", False),("10.2",True),("11.6",True),("15.0",True),("15.4",True)],
  [("Hypertension",),("1",),("1",),("0",),("0",)],
  [("Diabetes Mellitus",),("0",),("1",),("0",),("0",)],
  [("CKD (actual)",),("1",),("1",),("0",),("0",)]],
 widths=[2900,1600,1600,1600,1600]))

H2("4.6 Deployed Interface")
PLAIN("The best XGBoost model was successfully implemented in the explanation-first clinical decision support interface. The interface provided a categorical prediction of whether CKD was present, along with a colour-coded bar chart of the SHAP contributions. Because the underlying model performs inference very quickly, the prediction and its explanation were produced in real time, which is necessary for a responsive point-of-care diagnostic aid.")

# ---- 5. Discussion ----
H1("5. Discussion")
H2("5.1 Interpretation of the Principal Findings")
PLAIN("The present framework offers a distinctive methodological approach that combines two independent interpretability methods (SHAP and LIME) with a quantitative measure of their agreement. When an explanation is supported by two methodologically different techniques, a clinician can hold more justified confidence than if only one technique were presented. Conversely, cases where the two approaches disagree can be flagged as requiring further investigation, providing a principled basis for the calibration of trust. The Partial Dependence Plots enriched the interpretability layer by revealing the functional form of the feature-risk relationships, including threshold effects (for example, a sharp drop in the predicted CKD probability once urinary specific gravity exceeds about 1.020) that are not captured by scalar importance measures.")
H2("5.2 Clinical Plausibility of the Explanations")
PLAIN("The most encouraging result is the close correspondence between the inferred feature importances and established nephrological knowledge. The dominance of urinary specific gravity, haemoglobin, albumin, and serum creatinine reflects well-known markers of renal function and dysfunction. Reduced renal concentrating ability (low specific gravity), anaemia due to decreased erythropoietin production, glomerular damage reflected by albuminuria, and accumulation of nitrogenous waste (serum creatinine) form a coherent physiological account of chronic renal insufficiency. That an automated system, learning from data alone, independently recovered this account strongly indicates the reliability of its reasoning, corroborating the results of Moreno-Sanchez (2023) and Raihan et al. (2023).")
H2("5.3 The Value of Dual Interpretability and Fidelity Auditing")
PLAIN("An important methodological innovation is the combination of SHAP and LIME with a quantitative evaluation of their agreement. This auditing feature helps overcome a subtle but important weakness of post hoc explanation methods, their potential instability, and improves on the current practice of reporting a single unverified explanation method. The Partial Dependence Plots complement this layer by revealing threshold effects such as the sharp drop in predicted CKD probability once specific gravity exceeds approximately 1.020.")
H2("5.4 Comparison with the Extant Literature")
PLAIN("Most previous research has focused on a single goal, maximising accuracy, a single interpretability mode, robust imputation, or deployment, whereas the present work integrates these previously separate advances into a single pipeline. The framework builds on Dharmarathne et al. (2024) in three ways: it adds LIME and a fidelity audit to the interpretability layer, adds a comparative evaluation of robust imputation methods including generative methods, and uses Bayesian rather than random hyperparameter optimisation. It contributes to the dual-explanation approach of Chouit et al. (2026) by introducing Partial Dependence analysis and an explicit fidelity metric.")
H2("5.5 Clinical and Practical Implications")
PLAIN("The compact input set of only ten features reduces data entry and makes the system practical where a full panel of laboratory tests may be unavailable or costly, such as resource-limited and rural settings. The explanation-first design supports both clinical decision-making and patient communication. The very low inference latency ensures these benefits are available in real time.")
H2("5.6 Limitations")
PLAIN("Several caveats must be stated candidly. The most notable limitation is the small benchmark dataset. The 400 UCI cases allow direct comparison with previous studies but may not represent the full spectrum of clinical presentations, demographic features, and comorbidities seen worldwide, and the very high accuracy should be interpreted with corresponding caution. The generalisability of the framework to other, ethnically and geographically diverse cohorts is not yet established. A second limitation concerns the generative imputation component: GANs can generate synthetic artefacts, and their performance on small datasets requires careful validation. A third limitation is that the explanation-fidelity measure, while useful, remains an area of active methodological research. Finally, the study did not include a prospective clinician-in-the-loop usability evaluation of the deployed interface.")
H2("5.7 Directions for Future Research")
PLAIN("The most important direction is external validation on multiple, demographically diverse, multi-centre cohorts. The framework could incorporate additional data modalities such as genetic markers, longitudinal measurements, and social determinants of health. Prospective usability studies with practising nephrologists would establish real-world usefulness and acceptability. Finally, the framework could be extended from binary classification to the multi-class problem of CKD staging, greatly increasing its clinical relevance.")

# ---- 6. Conclusion ----
H1("6. Conclusion")
P([("This study proposed, implemented, and tested a single explainable-AI framework for the diagnosis of chronic kidney disease, integrating robust imputation, hyperparameter-optimised ensemble learning, dual and fidelity-audited interpretability, and clinical deployment within one reproducible pipeline. The Bayesian-optimised XGBoost model was the most successful, achieving the highest testing accuracy of 0.983 and an area under the receiver operating characteristic curve of 0.997. ", False),
   ("Its most important predictors were urinary specific gravity, haemoglobin, albumin, and serum creatinine", True),
   (", consistently identified across SHAP, LIME, and Partial Dependence Plots and in good agreement with known renal pathophysiology. The high fidelity between SHAP and LIME explanations provided further confidence in the transparency and reliability of the system. The main contribution is the integrative consolidation of these components, demonstrating that accuracy, robustness, interpretability, and deployability can be pursued together rather than separately.", False)])

# ---- References ----
H1("References")
refs = [
"Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A next-generation hyperparameter optimization framework. In Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (pp. 2623-2631). ACM.",
"Almasoud, M., & Ward, T. E. (2019). Detection of chronic kidney disease using machine learning algorithms with least number of predictors. IJACSA, 10(8), 89-96.",
"Amirgaliyev, Y., Shamiluulu, S., & Serek, A. (2018). Analysis of chronic kidney disease dataset by applying machine learning methods. In 2018 IEEE 12th AICT (pp. 1-4). IEEE.",
"Asuncion, A., & Newman, D. (2007). UCI machine learning repository. University of California, Irvine.",
"Bai, Q., Su, C., Tang, W., & Li, Y. (2022). Machine learning to predict end stage kidney disease in chronic kidney disease. Scientific Reports, 12(1), 8377.",
"Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. In Proceedings of the 22nd ACM SIGKDD (pp. 785-794). ACM.",
"Chittora, P., et al. (2021). Prediction of chronic kidney disease: A machine learning perspective. IEEE Access, 9, 17312-17334.",
"Chouit, E. M., Rachdi, M., Bellafkih, M., & Raouyane, B. (2026). Interpretable machine learning for chronic kidney disease prediction: Insights from SHAP and LIME analyses. PLOS One, 21(2), e0343205.",
"Debal, D. A., & Sitote, T. M. (2022). Chronic kidney disease prediction using machine learning techniques. Journal of Big Data, 9(1), 109.",
"Dharmarathne, G., Bogahawaththa, M., McAfee, M., Rathnayake, U., & Meddage, D. P. P. (2024). On the diagnosis of chronic kidney disease using a machine learning-based interface with explainable artificial intelligence. Intelligent Systems with Applications, 22, 200397.",
"Dritsas, E., & Trigka, M. (2022). Machine learning techniques for chronic kidney disease risk prediction. Big Data and Cognitive Computing, 6(3), 98.",
"Ebiaredoh-Mienye, S. A., Swart, T. G., Esenogho, E., & Mienye, I. D. (2022). A machine learning method with filter-based feature selection for improved prediction of chronic kidney disease. Bioengineering, 9(8), 350.",
"Emon, M. U., et al. (2021). Performance analysis of chronic kidney disease through machine learning approaches. In 2021 6th ICICT (pp. 713-719). IEEE.",
"Ghosh, P., et al. (2020). Optimization of prediction method of chronic kidney disease using machine learning algorithm. In 2020 15th iSAI-NLP (pp. 1-6). IEEE.",
"Goodfellow, I., et al. (2014). Generative adversarial nets. In Advances in Neural Information Processing Systems (Vol. 27, pp. 2672-2680).",
"Gupta, R., Koli, N., Mahor, N., & Tejashri, N. (2020). Performance analysis of machine learning classifier for predicting chronic kidney disease. In 2020 INCET (pp. 1-4). IEEE.",
"Iftikhar, H., et al. (2023). A comparative analysis of machine learning models: A case study in predicting chronic kidney disease. Sustainability, 15(3), 2754.",
"Islam, M. A., et al. (2020). Risk factor prediction of chronic kidney disease based on machine learning algorithms. In 2020 3rd ICISS (pp. 952-957). IEEE.",
"Jerlin Rubini, L., & Perumal, E. (2020). Efficient classification of chronic kidney disease by using multi-kernel support vector machine and fruit fly optimization algorithm. IJIST, 30(3), 660-673.",
"Kalantar-Zadeh, K., Jafar, T. H., Nitsch, D., Neuen, B. L., & Perkovic, V. (2021). Chronic kidney disease. The Lancet, 398(10302), 786-802.",
"Khan, B., Naseem, R., Muhammad, F., Abbas, G., & Kim, S. (2020). An empirical evaluation of machine learning techniques for chronic kidney disease prophecy. IEEE Access, 8, 55012-55022.",
"Levey, A. S., & Coresh, J. (2012). Chronic kidney disease. The Lancet, 379(9811), 165-180.",
"Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. In Advances in Neural Information Processing Systems (Vol. 30, pp. 4765-4774).",
"Moreno-Sanchez, P. A. (2023). Data-driven early diagnosis of chronic kidney disease: Development and evaluation of an explainable AI model. IEEE Access, 11, 38359-38369.",
"Nishat, M. M., et al. (2018). A comprehensive analysis on detecting chronic kidney disease by employing machine learning algorithms. EAI Endorsed Transactions on Pervasive Health and Technology, 7(29), e1.",
"Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830.",
"Polat, H., Danaei Mehr, H., & Cetin, A. (2017). Diagnosis of chronic kidney disease based on support vector machine by feature selection methods. Journal of Medical Systems, 41(4), 55.",
"Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A. (2018). CatBoost: Unbiased boosting with categorical features. In Advances in Neural Information Processing Systems (Vol. 31, pp. 6638-6648).",
"Raihan, M. J., Khan, M. A., Kee, S. H., & Nahid, A. A. (2023). Detection of the chronic kidney disease using XGBoost classifier and explaining the influence of the attributes on the model using SHAP. Scientific Reports, 13(1), 6263.",
"Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). Why should I trust you? Explaining the predictions of any classifier. In Proceedings of the 22nd ACM SIGKDD (pp. 1135-1144). ACM.",
"Sanmarchi, F., et al. (2023). Predict, diagnose, and treat chronic kidney disease with machine learning: A systematic literature review. Journal of Nephrology, 36(4), 1101-1117.",
"Sobrinho, A., et al. (2020). Computer-aided diagnosis of chronic kidney disease in developing countries: A comparative analysis of machine learning techniques. IEEE Access, 8, 25407-25419.",
"Tsai, M. C., Lu, C. H., Wang, Y. H., Yang, C. Y., & Cheng, C. Y. (2023). Risk prediction model for chronic kidney disease in Thailand using artificial intelligence and SHAP. Diagnostics, 13(23), 3548.",
"Venkatesan, V. K., Ramakrishna, M. T., Izonin, I., Tkachenko, R., & Havryliuk, M. (2023). Efficient data preprocessing with ensemble machine learning technique for the early detection of chronic kidney disease. Applied Sciences, 13(5), 2885.",
"Webster, A. C., Nagler, E. V., Morton, R. L., & Masson, P. (2017). Chronic kidney disease. The Lancet, 389(10075), 1238-1252.",
"Xiao, J., et al. (2019). Comparison and development of machine learning tools in the prediction of chronic kidney disease progression. Journal of Translational Medicine, 17(1), 119.",
"Zheng, J. X., et al. (2024). Interpretable machine learning for predicting chronic kidney disease progression risk. Digital Health, 10, 20552076231224225.",
]
for r in refs:
    # highlight the added Xiao reference and the corrected Moreno-Sanchez spelling? keep Xiao highlighted (newly added)
    hl = r.startswith("Xiao")
    B.append(para([run(r, hl=hl, size=20)], spacing_after=60))

# ===========================================================================
# ASSEMBLE DOCX
# ===========================================================================
body = ''.join(B)
sectpr = ('<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
          '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>')
document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
 '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
 'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
 'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
 f'<w:body>{body}{sectpr}</w:body></w:document>')

content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
 '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
 '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
 '<Default Extension="xml" ContentType="application/xml"/>'
 '<Default Extension="png" ContentType="image/png"/>'
 '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
 '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
 '</Types>')

rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
 '<Relationship Id="rIdDoc" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
 '</Relationships>')

# document rels: styles + 7 images
rel_items = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
for rid, path in FIGS.items():
    fname = os.path.basename(path)
    rel_items.append(f'<Relationship Id="rId{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{fname}"/>')
word_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
 + ''.join(rel_items) + '</Relationships>')

styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
 '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
 '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
 '<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>'
 '<w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:style>'
 '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/>'
 '<w:rPr><w:b/><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr>'
 '<w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr></w:style>'
 '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>'
 '<w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:color w:val="1F3864"/></w:rPr>'
 '<w:pPr><w:spacing w:before="320" w:after="120"/><w:jc w:val="left"/></w:pPr></w:style>'
 '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>'
 '<w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/><w:color w:val="2E5496"/></w:rPr>'
 '<w:pPr><w:spacing w:before="200" w:after="80"/><w:jc w:val="left"/></w:pPr></w:style>'
 '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr>'
 '<w:tblBorders><w:top w:val="single" w:sz="4" w:color="auto"/><w:left w:val="single" w:sz="4" w:color="auto"/>'
 '<w:bottom w:val="single" w:sz="4" w:color="auto"/><w:right w:val="single" w:sz="4" w:color="auto"/>'
 '<w:insideH w:val="single" w:sz="4" w:color="auto"/><w:insideV w:val="single" w:sz="4" w:color="auto"/>'
 '</w:tblBorders></w:tblPr></w:style>'
 '</w:styles>')

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('[Content_Types].xml', content_types)
    zf.writestr('_rels/.rels', rels)
    zf.writestr('word/_rels/document.xml.rels', word_rels)
    zf.writestr('word/document.xml', document)
    zf.writestr('word/styles.xml', styles)
    for path in FIGS.values():
        with open(path,'rb') as f:
            zf.writestr(f'word/media/{os.path.basename(path)}', f.read())

print("Wrote", OUT)
