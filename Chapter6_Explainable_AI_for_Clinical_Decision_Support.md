# Chapter 6

# Explainable Artificial Intelligence for Clinical Decision Support

**Amman Jakhar¹,\*** and **Sachin Kalsi¹**

¹ Department of Mechanical Engineering, Chandigarh University, Mohali, Punjab-140301

\* Corresponding Email: ammanjakhar5000734@gmail.com

---

## Abstract

This chapter offers a rigorous and practice-oriented examination of Explainable Artificial Intelligence (XAI) within the domain of clinical decision support systems (CDSS), addressing the pivotal challenge of reconciling algorithmic performance with the transparency demands of high-stakes medical environments. As AI models—particularly deep learning architectures—achieve remarkable accuracy in tasks ranging from radiological image interpretation to predictive risk stratification, their inherent opacity poses significant barriers to clinical adoption, undermining trust, accountability, and regulatory compliance. The chapter systematically reviews the landscape of XAI methodologies applicable to healthcare, distinguishing between intrinsic interpretable models such as decision trees and rule-based systems, and post-hoc explanation techniques including SHapley Additive Explanations (SHAP), Local Interpretable Model-agnostic Explanations (LIME), Integrated Gradients, and attention-based visualization methods. Specific emphasis is placed on the unique requirements of clinical contexts, where explanations must not only be technically faithful but also cognitively aligned with clinical reasoning, diagnostically actionable, and sensitive to the temporal and multimodal nature of patient data. The discussion critically examines the tension between model complexity and explainability, the evaluation of explanation quality through both computational metrics and clinician-user studies, and the emerging frameworks for regulatory certification of XAI systems under standards such as the EU AI Act and FDA guidelines for software as a medical device. Through illustrative case studies spanning emergency triage, oncology treatment planning, and intensive care unit (ICU) early warning systems, the chapter demonstrates practical XAI implementation strategies that enhance clinician-AI collaboration. The chapter concludes with forward-looking perspectives on personalised explanations tailored to diverse user groups, the integration of causal reasoning with associative learning, and the role of interactive and counterfactual explanations in fostering iterative human-AI dialogue for improved patient outcomes.

**Keywords:** Explainable Artificial Intelligence, Clinical Decision Support Systems, Interpretability, Trustworthy AI, Healthcare Informatics

---

## 6.1 Introduction

The integration of artificial intelligence (AI) into clinical medicine represents one of the most consequential technological transitions in the history of healthcare delivery. Over the past decade, machine learning (ML) systems—and deep neural networks in particular—have demonstrated diagnostic and prognostic performance that rivals, and in narrow tasks occasionally surpasses, that of experienced clinicians [1]. Convolutional neural networks now classify diabetic retinopathy from fundus photographs, detect malignant lesions on mammograms, and segment tumours on magnetic resonance imaging with sensitivity and specificity that would have seemed implausible only fifteen years ago [2]. Recurrent and transformer-based architectures ingest longitudinal electronic health record (EHR) streams to forecast sepsis, acute kidney injury, and in-hospital deterioration hours before conventional scoring systems raise an alarm [3]. Yet despite this remarkable accuracy, the translation of such models from retrospective validation studies into routine bedside practice has been strikingly slow [4].

A central reason for this translational gap is the *opacity* of high-performing models. The very architectural properties that grant deep networks their expressive power—millions of nonlinearly interacting parameters distributed across dozens of layers—render their internal decision logic inscrutable to the humans who must act on their outputs [5]. A clinician confronted with a recommendation to escalate care, withhold a therapy, or order an invasive procedure cannot responsibly defer to a numerical score whose derivation is hidden. Medicine is a domain in which decisions carry existential consequences, in which accountability is legally and ethically mandated, and in which the norms of professional practice demand that a practitioner be able to articulate the reasoning behind an intervention [6]. An unexplained prediction, however accurate on aggregate, is therefore of limited clinical utility and may even be dangerous when it is silently miscalibrated for a particular patient subgroup [7].

Explainable Artificial Intelligence (XAI) has emerged as the research programme dedicated to closing this gap. Broadly, XAI encompasses the collection of methods, models, and evaluation practices that render the behaviour of AI systems intelligible to human stakeholders without unacceptable sacrifice of predictive performance [8]. In the clinical setting, the ambitions of XAI extend well beyond technical curiosity. Explanations are expected to support four interlocking objectives: to *build appropriate trust* so that clinicians neither over-rely nor under-rely on the system; to *enable verification* so that errors and spurious correlations can be caught before they harm patients; to *satisfy regulatory and legal requirements* for transparency and the right to explanation; and to *facilitate learning* so that the human-AI partnership improves over time [9]. These objectives are not always mutually reinforcing, and a recurring theme of this chapter is that "explainability" is not a single property but a family of context-dependent requirements that must be negotiated against the concrete demands of a clinical workflow [10].

This chapter is structured to move from foundations to practice. Section 6.2 establishes conceptual foundations, defining interpretability and explainability and situating them within a taxonomy of approaches. Section 6.3 surveys the principal methodological families—intrinsically interpretable models and post-hoc explanation techniques including SHAP, LIME, Integrated Gradients, attention visualisation, and counterfactual methods. Section 6.4 articulates the distinctive requirements that clinical contexts impose on explanations. Section 6.5 examines the enduring tension between model complexity and explainability. Section 6.6 addresses the difficult problem of evaluating explanation quality through both computational metrics and human studies. Section 6.7 reviews the regulatory landscape. Section 6.8 grounds the discussion in three case studies. Section 6.9 offers forward-looking perspectives, and Section 6.10 concludes.

## 6.2 Conceptual Foundations of Explainability in Healthcare

### 6.2.1 Interpretability, Explainability, and Related Constructs

The terminology surrounding XAI is used inconsistently across the literature, and a degree of conceptual discipline is essential before methods can be meaningfully compared. Following the influential formulation of Doshi-Velez and Kim [8], *interpretability* may be understood as the degree to which a human can consistently predict a model's result, while *explainability* refers to the extent to which the internal mechanics of a system can be articulated in human terms. A closely related construct is *transparency*, which concerns whether the model's mechanism is inspectable at the level of the whole model (simulatability), its individual components (decomposability), or its training algorithm [5]. *Fidelity*, by contrast, measures how accurately an explanation reflects the true behaviour of the model it purports to describe, and *plausibility* captures whether an explanation is convincing to a human—two properties that, crucially, can diverge, since a plausible explanation may be unfaithful and a faithful explanation may be implausible [11].

For clinical purposes it is useful to add the notion of *actionability*: an explanation is actionable when it identifies factors that a clinician can, in principle, intervene upon or verify against independent evidence [12]. A saliency map that highlights an anatomically implausible region, or a feature attribution that credits an administrative artefact such as the identity of the ordering department, is neither actionable nor trustworthy even if it faithfully reflects what the model learned. This last observation motivates one of the field's most important cautionary findings: models frequently achieve high accuracy by exploiting confounders and shortcuts, and a faithful explanation is precisely the instrument that exposes such behaviour [7].

### 6.2.2 A Taxonomy of Approaches

XAI methods can be organised along several orthogonal axes, summarised conceptually in **Figure 1**. The first and most fundamental axis distinguishes *intrinsic* interpretability—achieved by constraining the model to a transparent functional form such as a shallow decision tree, a linear model, or a rule list—from *post-hoc* explanation, in which a separate procedure is applied after training to approximate or probe an already-trained black-box model [13]. A second axis separates *model-specific* techniques, which exploit the internal structure of a particular architecture (for example, gradient-based attributions for differentiable networks), from *model-agnostic* techniques that treat the model as an opaque function and perturb its inputs [14]. A third axis distinguishes *global* explanations, which characterise the model's behaviour across the entire input space, from *local* explanations, which account for a single prediction about a single patient [8]. As **Figure 1** indicates, these axes are not independent: intrinsic models tend to offer global transparency, whereas the most widely deployed post-hoc methods in healthcare are local and model-agnostic.

The relevance of this taxonomy to clinical practice cannot be overstated. A hospital quality-improvement committee auditing a readmission model for systematic bias needs *global* explanations of population-level behaviour, whereas a bedside physician evaluating a single deterioration alert needs a *local* explanation specific to that patient's physiology [15]. The organising scheme in **Figure 1** thus serves not merely as an academic classification but as a decision aid for selecting the appropriate explanatory tool for a given clinical question, a mapping developed further in the case studies of Section 6.8.


## 6.3 A Landscape of XAI Methodologies for Healthcare

### 6.3.1 Intrinsically Interpretable Models

The most direct route to interpretability is to restrict the hypothesis class to models whose structure is transparent by construction. Decision trees express their logic as a sequence of human-readable if-then splits; linear and logistic regression models attach a signed coefficient to each covariate; rule lists and rule sets encode knowledge as compact Boolean conditions; and generalised additive models (GAMs) express the prediction as a sum of one-dimensional shape functions that can be plotted and inspected feature by feature [16]. Such models have a long and successful history in medicine: the CHA₂DS₂-VASc score for stroke risk in atrial fibrillation, the CURB-65 score for pneumonia severity, and the Wells criteria for pulmonary embolism are all, in effect, intrinsically interpretable predictive models that clinicians trust precisely because they can trace every point in the score to a physiological rationale [17].

A persistent assumption in the field held that intrinsic interpretability necessarily costs accuracy—the so-called accuracy-interpretability trade-off. Rudin has forcefully challenged this assumption, arguing that for many structured, tabular clinical prediction problems, a carefully engineered interpretable model matches the performance of an opaque one, and that the reflexive deployment of black boxes in high-stakes settings is therefore both unnecessary and irresponsible [13]. The work of Caruana and colleagues on GAMs applied to pneumonia mortality prediction is emblematic: their interpretable model not only achieved competitive accuracy but revealed a dangerous learned pattern—that asthmatic patients were assigned *lower* risk—an artefact of more aggressive treatment that would have been invisible in a black box and lethal if deployed naively [7]. This example illustrates that intrinsic interpretability is not merely a convenience but a mechanism of clinical safety.

### 6.3.2 Post-hoc Feature Attribution: SHAP and LIME

When the deployment of a complex model is justified—most notably for unstructured data such as images, waveforms, and free text where deep networks decisively outperform interpretable alternatives—post-hoc explanation becomes necessary. The two most widely adopted model-agnostic attribution methods are LIME and SHAP.

Local Interpretable Model-agnostic Explanations (LIME) explains an individual prediction by fitting a simple, interpretable surrogate model—typically sparse linear regression—to the black box's behaviour in the local neighbourhood of the instance of interest, generated by perturbing the input and weighting the perturbed samples by their proximity to the original [14]. The result is a set of locally faithful feature weights that indicate which features pushed the prediction toward or away from a given outcome. LIME is attractive for its intuitive formulation and its applicability to tabular, text, and image data, but it suffers from instability: because the explanation depends on stochastic sampling and neighbourhood definition, repeated applications to the same instance can yield materially different attributions, a property that undermines clinician confidence [18].

SHapley Additive exPlanations (SHAP) places feature attribution on a firmer theoretical footing by drawing on cooperative game theory [19]. Treating each feature as a "player" in a game whose "payoff" is the model's prediction, SHAP assigns to each feature its Shapley value—the average marginal contribution of that feature across all possible orderings of feature inclusion. This construction uniquely satisfies a set of desirable axioms (local accuracy, missingness, and consistency) that competing methods violate, and it unifies several earlier attribution schemes as special cases [19]. Practical variants such as KernelSHAP (model-agnostic) and TreeSHAP (an exact, efficient algorithm for tree ensembles) have made SHAP the de facto standard for explaining tabular clinical models, and its additive force-plot and summary-plot visualisations have become familiar sights in the medical ML literature [3]. The principal comparison of these and other methods is presented in **Table 1**, which contrasts them along the dimensions of scope, model dependence, output form, computational cost, and known limitations.

### 6.3.3 Gradient-Based Attribution and Integrated Gradients

For differentiable models the model's own gradients provide a natural signal of feature importance. The simplest saliency map takes the gradient of the output with respect to the input pixels, but such raw gradients are noisy and suffer from *saturation*, whereby a feature that is important but whose activation has plateaued receives a near-zero gradient [20]. Integrated Gradients addresses this by integrating the gradients along a straight-line path from an uninformative baseline (for instance, a black image) to the actual input, thereby satisfying two axioms—sensitivity and implementation invariance—that raw gradients fail [20]. The method is widely used for explaining medical image classifiers because it attributes a relevance score to every input pixel while remaining computationally tractable and theoretically grounded. Related propagation-based methods such as Layer-wise Relevance Propagation and DeepLIFT pursue similar goals through alternative axiomatic routes [21]. These gradient methods are compared against perturbation-based approaches in **Table 1**, which makes explicit that their model-specific nature is both their strength—efficiency and access to internal structure—and their weakness, since they cannot be applied to non-differentiable or proprietary systems.

### 6.3.4 Attention and Visualisation Methods

For convolutional architectures, class activation mapping techniques—most prominently Gradient-weighted Class Activation Mapping (Grad-CAM)—produce coarse localisation heatmaps that indicate the image regions most responsible for a class prediction, and these have become the standard visual explanation in radiology and pathology applications [22]. In sequence models and transformers, *attention weights*, which quantify how strongly the model attends to each element of an input sequence when producing an output, are frequently repurposed as explanations of which clinical events or words drove a prediction [23]. Attention-based visualisation is intuitive and computationally free, since the weights are a by-product of the forward pass, but its status as a faithful explanation is contested: several studies have shown that attention distributions can be altered substantially without changing model predictions, casting doubt on the claim that "attention is explanation" [24]. The prudent position, reflected in **Table 1**, is to treat attention as a useful hypothesis-generating visualisation that must be corroborated by attribution methods with stronger fidelity guarantees.

### 6.3.5 Example-Based and Counterfactual Explanations

A conceptually distinct family explains a prediction not by attributing importance to features but by reference to examples. *Prototype* and *case-based* methods retrieve training instances that the model deems most similar to the query, mirroring the analogical reasoning clinicians already use when they recall comparable patients [25]. *Counterfactual* explanations, by contrast, answer the question "what minimal change to this patient's features would have altered the recommendation?"—for example, "had the patient's lactate been below 2.0 mmol/L, the sepsis alert would not have fired" [26]. Counterfactuals are especially aligned with clinical cognition because they are inherently actionable and because they map naturally onto the contrastive form of everyday human explanation [10]. Their generation must, however, respect feasibility and plausibility constraints so that the suggested changes are clinically meaningful and, where relevant, causally attainable rather than merely mathematically sufficient [26]. **Table 1** situates these example-based methods alongside feature-attribution approaches, underscoring that no single technique dominates and that clinical deployments increasingly combine complementary methods.

## 6.4 Requirements of Explanations in Clinical Contexts

Explanations that are adequate in a benchmark setting frequently fail at the bedside because clinical practice imposes requirements that generic XAI research rarely foregrounds. **Figure 2** organises these requirements into an integrated framework linking the properties of an explanation to the cognitive, temporal, and organisational realities of care delivery.

### 6.4.1 Cognitive Alignment with Clinical Reasoning

Clinicians reason through a blend of pattern recognition, hypothetico-deductive inference, and probabilistic weighing of evidence, structured by mental models of pathophysiology [27]. An explanation that presents feature attributions in units and idioms foreign to this reasoning—raw pixel relevances, abstract embedding dimensions, or unnormalised log-odds—imposes a heavy translation burden and is likely to be ignored under time pressure. Cognitively aligned explanations instead express themselves in terms of recognised clinical entities (laboratory abnormalities, vital-sign trends, comorbidities) and, ideally, connect them to plausible mechanistic narratives [12]. As **Figure 2** emphasises, alignment is not a property of the algorithm alone but of the fit between the explanation and the recipient's expertise, a point that motivates the personalised explanations discussed in Section 6.9.

### 6.4.2 Diagnostic Actionability

An explanation earns its keep in clinical practice only if it changes what a clinician can do. Actionable explanations distinguish modifiable from non-modifiable factors, surface the evidence a clinician can independently verify, and where possible indicate the direction and magnitude of influence so that an intervention can be prioritised [12]. Counterfactual explanations are the canonical actionable form, but even attribution methods become actionable when their outputs are tied to concrete verification steps—for example, prompting a clinician to re-examine a specific region of an image flagged as decisive.

### 6.4.3 Temporal and Multimodal Sensitivity

Patient data are irreducibly temporal and multimodal: vital signs stream continuously, laboratory values arrive intermittently, imaging is episodic, and clinical notes accumulate asynchronously [3]. An explanation of a deterioration prediction that ignores *when* a risk factor became influential is impoverished; clinicians need to know not only that rising lactate mattered but that its trajectory over the preceding six hours drove the alert [15]. Likewise, explanations for multimodal models must attribute influence across modalities in a commensurable way, indicating whether an oncology recommendation rested primarily on the histopathology, the genomic panel, or the radiological staging [28]. **Table 2** later formalises how these temporal and multimodal properties enter the evaluation of explanation quality.


## 6.5 The Tension Between Model Complexity and Explainability

A recurring dilemma in clinical AI is the apparent conflict between predictive performance and interpretability. The conventional narrative holds that accuracy and explainability sit at opposite ends of a spectrum: simple linear models and shallow trees are transparent but limited, whereas deep ensembles and neural networks are powerful but opaque [8]. This framing, while intuitive, is increasingly recognised as an oversimplification that conflates several distinct issues.

First, the trade-off is strongly *data-dependent*. For structured, tabular data with well-engineered features—the setting of most risk-scoring problems—the performance gap between interpretable and black-box models is often negligible, and Rudin's argument that interpretable models should be preferred by default applies with full force [13]. For unstructured, high-dimensional data such as images and raw waveforms, by contrast, deep networks retain a decisive advantage, and post-hoc explanation becomes the only realistic path to transparency [1]. Second, the trade-off can be *reframed as a design choice* rather than an immutable law: hybrid architectures embed interpretable components within otherwise complex systems, concept-bottleneck models force predictions to route through human-defined clinical concepts, and prototype networks build case-based reasoning directly into deep architectures [25]. These designs seek performance and interpretability simultaneously rather than trading one against the other.

A further, under-appreciated consideration is that post-hoc explanations of an opaque model are themselves approximations that may be unfaithful, so a "black box plus explainer" pipeline does not necessarily deliver more trustworthy transparency than a genuinely interpretable model [13]. The decision of where to sit on this spectrum should therefore be made deliberately, informed by the data modality, the stakes of the decision, the regulatory context, and the availability of validated interpretable alternatives. The governance implications of this decision are taken up in the regulatory frameworks summarised in **Table 3**, which links model risk classification to the depth of explanation and validation required.

## 6.6 Evaluating the Quality of Explanations

Perhaps the least mature aspect of clinical XAI is evaluation. It is not enough for a method to *produce* an explanation; the explanation must be shown to be faithful, stable, comprehensible, and clinically useful. Evaluation approaches fall into two broad camps, computational and human-centred, summarised in **Table 2**.

### 6.6.1 Computational (Functionally-Grounded) Metrics

Computational metrics assess properties of an explanation without human involvement, enabling rapid and reproducible comparison [8]. *Faithfulness* (or fidelity) is commonly measured by perturbation tests: features identified as important are removed or masked, and a faithful explanation should produce a correspondingly large drop in the model's confidence [11]. *Stability* (or robustness) quantifies how much an explanation changes under small, semantically irrelevant perturbations of the input; unstable explanations, such as those sometimes produced by LIME, are clinically hazardous because two near-identical patients may receive contradictory rationales [18]. *Sparsity* and *complexity* capture whether an explanation is concise enough to be cognitively manageable, and *sanity checks* verify that an explanation is actually sensitive to the model's parameters and the data labels rather than acting as a mere edge detector [29]. **Table 2** enumerates these metrics together with their operational definitions and the failure modes they are designed to detect.

### 6.6.2 Human-Centred Evaluation

Computational metrics are necessary but not sufficient, because the ultimate criterion of a clinical explanation is its effect on human decision quality [30]. Human-centred evaluation ranges from *application-grounded* studies, in which clinicians use the system in a realistic task and outcomes such as diagnostic accuracy, decision time, and appropriate reliance are measured, to *human-grounded* studies employing simplified proxy tasks [8]. A critical and sobering finding from this literature is that explanations can *increase* inappropriate trust: when an explanation is present, clinicians may follow an incorrect recommendation more readily, a phenomenon of automation bias that well-intentioned XAI can inadvertently worsen [31]. Rigorous human-centred evaluation must therefore measure not only whether users like an explanation—satisfaction is a weak proxy—but whether the explanation improves calibrated reliance, enabling clinicians to accept correct advice and reject incorrect advice [30]. The complementary roles of computational and human-centred evaluation are juxtaposed in **Table 2**, which stresses that a defensible evaluation programme must combine both.

## 6.7 Regulatory and Certification Frameworks

The deployment of XAI in healthcare occurs within a tightening web of regulation that increasingly treats explainability not as an optional virtue but as a compliance obligation. **Table 3** compares the principal frameworks along the dimensions of scope, risk classification, transparency mandates, and their implications for XAI design.

### 6.7.1 The EU AI Act

The European Union's Artificial Intelligence Act establishes a risk-tiered regulatory regime in which most clinical decision support systems, being safety components of medical devices, fall into the *high-risk* category [32]. High-risk systems are subject to obligations including risk management, data governance, technical documentation, human oversight, and—centrally for this chapter—*transparency* provisions requiring that the system's operation be sufficiently interpretable for deployers to understand and appropriately use its output [32]. The Act interacts with the pre-existing right to explanation debated under the General Data Protection Regulation, which grants data subjects meaningful information about the logic of automated decisions with significant effects [33]. Together these instruments make the provision of adequate explanations a legal precondition of deployment in the European market, as summarised in **Table 3**.

### 6.7.2 FDA Regulation of Software as a Medical Device

In the United States, the Food and Drug Administration regulates clinical AI under its framework for Software as a Medical Device (SaMD), and has articulated guiding principles for Good Machine Learning Practice as well as a proposed approach to managing continuously learning ("adaptive") algorithms through predetermined change control plans [34]. FDA guidance emphasises transparency to intended users, robust clinical validation, and lifecycle monitoring for performance drift, and it draws a regulatory distinction between systems that merely inform a clinician who can independently review the basis of a recommendation and those that direct care without such opportunity for review [35]. This distinction places a premium on explanations that genuinely enable independent clinician review, reinforcing the actionability requirement of Section 6.4. The contrast between the EU's rights-based, risk-tiered approach and the FDA's device-lifecycle approach is drawn out in **Table 3**, which also notes the growing convergence around demands for documentation, validation, and post-market surveillance.


## 6.8 Case Studies in Clinical XAI

To move from principle to practice, this section examines three clinical domains in which XAI has been deployed or seriously prototyped. Each illustrates a different combination of data modality, decision stakes, and explanatory need, and each is summarised in **Table 4**. A common reference architecture linking model, explainer, and clinical interface across these settings is depicted in **Figure 3**.

### 6.8.1 Emergency Department Triage

Emergency triage requires rapid stratification of undifferentiated patients into acuity levels under severe time pressure and incomplete information. Machine learning triage models trained on presenting complaint, vital signs, and demographics can outperform conventional ordinal triage scales in predicting critical outcomes, but their adoption depends on triage nurses trusting and understanding the acuity recommendation within seconds [36]. Here SHAP-based local explanations that surface the two or three features most responsible for an elevated acuity score—for instance, a low oxygen saturation combined with tachycardia and advanced age—map well onto the rapid, feature-focused reasoning of triage staff [3]. The reference architecture in **Figure 3** applies directly: the gradient-boosted model produces a score, TreeSHAP computes attributions in milliseconds, and a compact visual summary is rendered at the point of care. As **Table 4** records, the dominant requirement in this setting is *speed and cognitive economy*, favouring sparse, glanceable explanations over exhaustive ones.

### 6.8.2 Oncology Treatment Planning

Oncology decision support operates on a very different tempo and data profile. Treatment selection integrates histopathology, genomic and molecular panels, radiological staging, and patient preferences, and decisions are deliberated over hours to days, frequently within a multidisciplinary tumour board [28]. The explanatory need is correspondingly richer: clinicians require multimodal attributions that indicate how each data source contributed to a recommendation, together with case-based evidence linking the patient to comparable prior cases and their outcomes [25]. Counterfactual and example-based explanations are particularly valuable here because tumour boards reason contrastively, weighing why one regimen is preferred over another. As shown in **Table 4**, the oncology setting prioritises *depth, multimodality, and traceability to evidence*, and it exposes the limitations of single-modality attribution methods, motivating the integrative interface sketched in **Figure 3**.

### 6.8.3 Intensive Care Unit Early Warning Systems

The ICU generates dense, continuous, multivariate time-series data, and early-warning models for sepsis, deterioration, and organ failure must explain predictions that evolve minute by minute [15]. The explanatory challenge is fundamentally temporal: a static feature-importance list is inadequate when clinicians need to understand which physiological trends over which time windows are driving a rising risk score [3]. Time-aware attribution methods and trajectory visualisations that display the contribution of each variable across the observation window address this need, allowing an intensivist to see, for example, that a sepsis alert reflects a combination of climbing lactate over six hours, worsening tachypnoea, and a falling mean arterial pressure [37]. **Figure 4** presents a representative ICU early-warning explanation workflow, in which streaming vital signs feed a recurrent risk model whose temporally resolved attributions are surfaced alongside the raw trends. This workflow embodies the temporal-sensitivity requirement of Section 6.4.3 and, as **Figure 4** makes clear, integrates the explanation directly into the monitoring display rather than relegating it to a separate report, thereby reducing the interpretive burden on already-saturated ICU staff. **Table 4** summarises how the ICU case differs from triage and oncology in demanding *temporal resolution and continuous updating* above all else.

## 6.9 Future Directions

### 6.9.1 Personalised Explanations for Diverse Stakeholders

A single explanation rarely serves the varied audiences of a clinical AI system. An intensivist, a primary-care physician, a nurse, a hospital administrator, a regulator, and the patient themselves each bring different expertise, goals, and information needs [30]. Future systems will increasingly *personalise* explanations to the recipient's role and expertise—offering a mechanistic, feature-level rationale to a specialist while providing the patient a plain-language, contrastive account of what mattered and what could change [9]. Personalisation raises its own challenges of consistency and manipulation, since audience-tailored explanations must remain mutually faithful to a single underlying model and must not be tuned to persuade rather than to inform [31].

### 6.9.2 From Association to Causation

Most contemporary XAI methods explain *associations* the model has learned, not the *causal* structure of the underlying clinical reality, and this gap is a frequent source of misleading explanations [38]. A feature attribution may correctly report that a model relies on a variable that is merely correlated with, rather than causally related to, the outcome—the asthma-pneumonia artefact being a paradigmatic example [7]. The integration of causal inference with machine learning promises explanations that distinguish genuine drivers from confounders and that support the interventional and counterfactual queries clinicians actually care about [38]. Causal approaches also underpin the feasibility constraints that make counterfactual explanations clinically meaningful, ensuring that suggested changes correspond to attainable interventions rather than statistical artefacts [26].

### 6.9.3 Interactive and Counterfactual Dialogue

The prevailing paradigm treats explanation as a one-shot, static artefact delivered alongside a prediction. A more promising future casts explanation as an *interactive dialogue* in which the clinician interrogates the system—asking why a recommendation was made, what would change it, and how confident the model is—and the system responds with progressively refined, contrastive answers [39]. Such conversational and counterfactual interfaces align explanation with the iterative, question-driven nature of clinical reasoning and can support genuine human-AI collaboration rather than passive consumption of a rationale [10]. Realising this vision will require advances in natural-language generation grounded in faithful model internals, uncertainty communication, and human-computer interaction design attuned to the clinical environment [40].

### 6.9.4 Trustworthiness, Fairness, and Continual Validation

Finally, explainability must be understood as one pillar of a broader trustworthy-AI agenda that includes fairness, robustness, privacy, and continual validation [6]. Explanations are a powerful instrument for auditing fairness, since they can reveal when a model's decisions rest on protected or proxy attributes across demographic subgroups [41]. As models are updated and as patient populations and clinical practices drift, explanations must be re-validated rather than assumed to remain faithful, embedding XAI within the lifecycle-monitoring obligations that regulators increasingly demand [42]. The convergence of secure, federated, and explainable AI—the organising theme of this volume—points toward systems that are simultaneously performant, privacy-preserving, and transparent, and that earn the durable trust of clinicians and patients alike [43].

## 6.10 Conclusion

Explainable Artificial Intelligence occupies a pivotal position in the responsible translation of machine learning into clinical practice. This chapter has argued that explainability is not a single technical property but a family of context-dependent requirements—faithfulness, stability, cognitive alignment, actionability, and temporal-multimodal sensitivity—that must be matched to the concrete demands of a clinical task and its stakeholders. It has surveyed the principal methodological families, from intrinsically interpretable models whose transparency is a mechanism of clinical safety, to post-hoc techniques such as SHAP, LIME, Integrated Gradients, attention visualisation, and counterfactual explanation, each with characteristic strengths and documented failure modes. It has challenged the reflexive assumption of an inevitable accuracy-interpretability trade-off, emphasising that the choice of where to sit on that spectrum is a deliberate design decision shaped by data modality, decision stakes, and regulation. It has stressed that evaluation must combine computational metrics with rigorous human-centred studies, because explanations can as easily foster inappropriate trust as calibrated reliance. And it has situated XAI within an intensifying regulatory landscape defined by the EU AI Act and FDA SaMD frameworks, and within three concrete clinical settings—emergency triage, oncology treatment planning, and ICU early warning—that reveal how explanatory needs vary with tempo and modality. Looking forward, personalised explanations, the integration of causal reasoning, and interactive counterfactual dialogue promise to transform explanation from a static disclosure into a genuine medium of human-AI collaboration. The ultimate measure of success will not be the elegance of any attribution algorithm but whether clinicians, equipped with transparent and trustworthy AI, are enabled to make better decisions for the patients in their care [44]. Achieving that goal will require sustained interdisciplinary collaboration among machine-learning researchers, clinicians, human-factors specialists, ethicists, and regulators, working together to ensure that the intelligence we build into healthcare systems is as accountable as it is powerful [45].

---

## Figures

**Figure 1.** A multi-axis taxonomy of Explainable AI methods for clinical decision support, organising techniques by interpretability route (intrinsic vs. post-hoc), model dependence (model-specific vs. model-agnostic), and scope (global vs. local), with representative methods mapped to each region.

**Figure 2.** An integrated framework of clinical explanation requirements, linking explanation properties (fidelity, cognitive alignment, actionability, temporal and multimodal sensitivity) to the cognitive, temporal, and organisational realities of care delivery.

**Figure 3.** A common reference architecture for XAI-enabled clinical decision support, showing the flow from patient data through the predictive model and the explanation engine to a role-adapted clinical interface, shared across the emergency-triage, oncology, and ICU case studies.

**Figure 4.** A representative ICU early-warning explanation workflow in which streaming vital signs and laboratory values feed a recurrent risk model whose temporally resolved feature attributions are surfaced alongside the raw physiological trends within the bedside monitoring display.

---

## Tables

**Table 1.** Comparison of principal XAI methods for healthcare.

| Method | Scope | Model dependence | Output form | Relative cost | Key limitation |
|---|---|---|---|---|---|
| Decision trees / rule lists | Global | Intrinsic | Human-readable rules | Low | Limited capacity for unstructured data |
| Generalised additive models | Global | Intrinsic | Per-feature shape plots | Low–moderate | Assumes limited feature interactions |
| LIME | Local | Agnostic | Local linear weights | Moderate | Instability across runs |
| SHAP (Kernel/Tree) | Local + global | Agnostic / tree-specific | Additive attributions | Moderate–high | Cost for large agnostic models |
| Integrated Gradients | Local | Model-specific (differentiable) | Pixel/feature relevance | Low–moderate | Baseline choice sensitivity |
| Grad-CAM | Local | Model-specific (CNN) | Coarse heatmap | Low | Low spatial resolution |
| Attention visualisation | Local | Model-specific | Attention weights | Negligible | Contested faithfulness |
| Counterfactual / example-based | Local | Agnostic | Contrastive instances | Moderate–high | Feasibility constraints required |

**Table 2.** Evaluation dimensions for explanation quality: computational and human-centred.

| Dimension | Category | Operational definition | Failure mode detected |
|---|---|---|---|
| Faithfulness / fidelity | Computational | Prediction change when important features are perturbed/removed | Explanation misrepresents model logic |
| Stability / robustness | Computational | Sensitivity of explanation to irrelevant input changes | Contradictory rationales for similar patients |
| Sparsity / complexity | Computational | Number of elements in the explanation | Cognitively unmanageable output |
| Sanity checks | Computational | Dependence on model parameters and labels | Explanation acts as data-only artefact |
| Comprehensibility | Human-centred | Clinician understanding in proxy tasks | Misinterpretation of the rationale |
| Calibrated reliance | Human-centred | Correct acceptance/rejection of advice | Automation bias / over-reliance |
| Decision impact | Human-centred | Change in accuracy, time, and outcomes | No clinical utility despite plausibility |

**Table 3.** Comparison of major regulatory frameworks relevant to clinical XAI.

| Dimension | EU AI Act (with GDPR) | FDA SaMD framework |
|---|---|---|
| Regulatory philosophy | Rights-based, risk-tiered | Device lifecycle, safety and effectiveness |
| Risk classification | Unacceptable / high / limited / minimal | Risk categorisation by state of condition and information significance |
| Status of most CDSS | Typically high-risk | Class II/III device software |
| Transparency mandate | Interpretability for deployers; right to explanation | Transparency to intended users; independent review |
| Adaptive models | Documentation and human oversight | Predetermined change control plans |
| Post-market obligations | Monitoring and logging | Real-world performance and drift monitoring |

**Table 4.** Summary of clinical case studies and their distinctive explanatory requirements.

| Setting | Data modality | Decision tempo | Preferred explanation form | Dominant requirement |
|---|---|---|---|---|
| Emergency triage | Vitals, complaint, demographics | Seconds | Sparse SHAP attributions | Speed and cognitive economy |
| Oncology planning | Pathology, genomics, imaging | Hours–days | Multimodal + case-based / counterfactual | Depth, multimodality, traceability |
| ICU early warning | Continuous multivariate time series | Minutes, continuous | Time-resolved trajectory attributions | Temporal resolution and updating |


---

## References

1. Topol, E. J. (2019). High-performance medicine: The convergence of human and artificial intelligence. *Nature Medicine, 25*(1), 44–56. https://doi.org/10.1038/s41591-018-0300-7

2. Gulshan, V., Peng, L., Coram, M., Stumpe, M. C., Wu, D., Narayanaswamy, A., Venugopalan, S., Widner, K., Madams, T., Cuadros, J., Kim, R., Raman, R., Nelson, P. C., Mega, J. L., & Webster, D. R. (2016). Development and validation of a deep learning algorithm for detection of diabetic retinopathy in retinal fundus photographs. *JAMA, 316*(22), 2402–2410. https://doi.org/10.1001/jama.2016.17216

3. Rajkomar, A., Oren, E., Chen, K., Dai, A. M., Hajaj, N., Hardt, M., Liu, P. J., Liu, X., Marcus, J., Sun, M., Sundberg, P., Yee, H., Zhang, K., Zhang, Y., Flores, G., Duggan, G. E., Irvine, J., Le, Q., Litsch, K., … Dean, J. (2018). Scalable and accurate deep learning with electronic health records. *npj Digital Medicine, 1*, 18. https://doi.org/10.1038/s41746-018-0029-1

4. Kelly, C. J., Karthikesalingam, A., Suleyman, M., Corrado, G., & King, D. (2019). Key challenges for delivering clinical impact with artificial intelligence. *BMC Medicine, 17*, 195. https://doi.org/10.1186/s12916-019-1426-2

5. Lipton, Z. C. (2018). The mythos of model interpretability. *Communications of the ACM, 61*(10), 36–43. https://doi.org/10.1145/3233231

6. Amann, J., Blasimme, A., Vayena, E., Frey, D., & Madai, V. I. (2020). Explainability for artificial intelligence in healthcare: A multidisciplinary perspective. *BMC Medical Informatics and Decision Making, 20*, 310. https://doi.org/10.1186/s12911-020-01332-6

7. Caruana, R., Lou, Y., Gehrke, J., Koch, P., Sturm, M., & Elhadad, N. (2015). Intelligible models for healthcare: Predicting pneumonia risk and hospital 30-day readmission. *Proceedings of the 21st ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 1721–1730. https://doi.org/10.1145/2783258.2788613

8. Doshi-Velez, F., & Kim, B. (2017). *Towards a rigorous science of interpretable machine learning*. arXiv. https://doi.org/10.48550/arXiv.1702.08608

9. Tonekaboni, S., Joshi, S., McCradden, M. D., & Goldenberg, A. (2019). What clinicians want: Contextualizing explainable machine learning for clinical end use. *Proceedings of Machine Learning Research (Machine Learning for Healthcare), 106*, 359–380.

10. Miller, T. (2019). Explanation in artificial intelligence: Insights from the social sciences. *Artificial Intelligence, 267*, 1–38. https://doi.org/10.1016/j.artint.2018.07.007

11. Jacovi, A., & Goldberg, Y. (2020). Towards faithfully interpretable NLP systems: How should we define and evaluate faithfulness? *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4198–4205. https://doi.org/10.18653/v1/2020.acl-main.386

12. Markus, A. F., Kors, J. A., & Rijnbeek, P. R. (2021). The role of explainability in creating trustworthy artificial intelligence for health care: A comprehensive survey of the terminology, design choices, and evaluation strategies. *Journal of Biomedical Informatics, 113*, 103655. https://doi.org/10.1016/j.jbi.2020.103655

13. Rudin, C. (2019). Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead. *Nature Machine Intelligence, 1*(5), 206–215. https://doi.org/10.1038/s42256-019-0048-x

14. Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why should I trust you?": Explaining the predictions of any classifier. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 1135–1144. https://doi.org/10.1145/2939672.2939778

15. Ghassemi, M., Oakden-Rayner, L., & Beam, A. L. (2021). The false hope of current approaches to explainable artificial intelligence in health care. *The Lancet Digital Health, 3*(11), e745–e750. https://doi.org/10.1016/S2589-7500(21)00208-9

16. Molnar, C. (2022). *Interpretable machine learning: A guide for making black box models explainable* (2nd ed.). Independently published. https://christophm.github.io/interpretable-ml-book/

17. Lip, G. Y. H., Nieuwlaat, R., Pisters, R., Lane, D. A., & Crijns, H. J. G. M. (2010). Refining clinical risk stratification for predicting stroke and thromboembolism in atrial fibrillation using a novel risk factor-based approach: The Euro Heart Survey on atrial fibrillation. *Chest, 137*(2), 263–272. https://doi.org/10.1378/chest.09-1584

18. Alvarez-Melis, D., & Jaakkola, T. S. (2018). *On the robustness of interpretability methods*. arXiv. https://doi.org/10.48550/arXiv.1806.08049

19. Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems, 30*, 4765–4774.

20. Sundararajan, M., Taly, A., & Yan, Q. (2017). Axiomatic attribution for deep networks. *Proceedings of the 34th International Conference on Machine Learning (PMLR), 70*, 3319–3328.

21. Bach, S., Binder, A., Montavon, G., Klauschen, F., Müller, K.-R., & Samek, W. (2015). On pixel-wise explanations for non-linear classifier decisions by layer-wise relevance propagation. *PLoS ONE, 10*(7), e0130140. https://doi.org/10.1371/journal.pone.0130140

22. Selvaraju, R. R., Cogswell, M., Das, A., Vedantam, R., Parikh, D., & Batra, D. (2017). Grad-CAM: Visual explanations from deep networks via gradient-based localization. *Proceedings of the IEEE International Conference on Computer Vision*, 618–626. https://doi.org/10.1109/ICCV.2017.74

23. Choi, E., Bahadori, M. T., Sun, J., Kulas, J., Schuetz, A., & Stewart, W. F. (2016). RETAIN: An interpretable predictive model for healthcare using reverse time attention mechanism. *Advances in Neural Information Processing Systems, 29*, 3504–3512.

24. Jain, S., & Wallace, B. C. (2019). Attention is not explanation. *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics*, 3543–3556. https://doi.org/10.18653/v1/N19-1357

25. Chen, C., Li, O., Tao, D., Barnett, A., Rudin, C., & Su, J. (2019). This looks like that: Deep learning for interpretable image recognition. *Advances in Neural Information Processing Systems, 32*, 8930–8941.

26. Wachter, S., Mittelstadt, B., & Russell, C. (2017). Counterfactual explanations without opening the black box: Automated decisions and the GDPR. *Harvard Journal of Law & Technology, 31*(2), 841–887.

27. Norman, G. (2005). Research in clinical reasoning: Past history and current trends. *Medical Education, 39*(4), 418–427. https://doi.org/10.1111/j.1365-2929.2005.02127.x

28. Huang, S.-C., Pareek, A., Seyyedi, S., Banerjee, I., & Lungren, M. P. (2020). Fusion of medical imaging and electronic health records using deep learning: A systematic review and implementation guidelines. *npj Digital Medicine, 3*, 136. https://doi.org/10.1038/s41746-020-00341-z

29. Adebayo, J., Gilmer, J., Muelly, M., Goodfellow, I., Hardt, M., & Kim, B. (2018). Sanity checks for saliency maps. *Advances in Neural Information Processing Systems, 31*, 9505–9515.

30. Bhatt, U., Xiang, A., Sharma, S., Weller, A., Taly, A., Jia, Y., Ghosh, J., Puri, R., Moura, J. M. F., & Eckersley, P. (2020). Explainable machine learning in deployment. *Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency*, 648–657. https://doi.org/10.1145/3351095.3375624

31. Bansal, G., Wu, T., Zhou, J., Fok, R., Nushi, B., Kamar, E., Ribeiro, M. T., & Weld, D. (2021). Does the whole exceed its parts? The effect of AI explanations on complementary team performance. *Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems*, 81, 1–16. https://doi.org/10.1145/3411764.3445717

32. European Parliament & Council of the European Union. (2024). *Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act)*. Official Journal of the European Union. http://data.europa.eu/eli/reg/2024/1689/oj

33. Goodman, B., & Flaxman, S. (2017). European Union regulations on algorithmic decision-making and a "right to explanation". *AI Magazine, 38*(3), 50–57. https://doi.org/10.1609/aimag.v38i3.2741

34. U.S. Food and Drug Administration, Health Canada, & Medicines and Healthcare products Regulatory Agency. (2021). *Good machine learning practice for medical device development: Guiding principles*. U.S. Food and Drug Administration. https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles

35. U.S. Food and Drug Administration. (2022). *Clinical decision support software: Guidance for industry and Food and Drug Administration staff*. U.S. Food and Drug Administration.

36. Levin, S., Toerper, M., Hamrock, E., Hinson, J. S., Barnes, S., Gardner, H., Dugas, A., Linton, B., Kirsch, T., & Kelen, G. (2018). Machine-learning-based electronic triage more accurately differentiates patients with respect to clinical outcomes compared with the Emergency Severity Index. *Annals of Emergency Medicine, 71*(5), 565–574. https://doi.org/10.1016/j.annemergmed.2017.08.005

37. Lauritsen, S. M., Kristensen, M., Olsen, M. V., Larsen, M. S., Lauritsen, K. M., Jørgensen, M. J., Lange, J., & Thiesson, B. (2020). Explainable artificial intelligence model to predict acute critical illness from electronic health records. *Nature Communications, 11*, 3852. https://doi.org/10.1038/s41467-020-17431-x

38. Pearl, J. (2019). The seven tools of causal inference, with reflections on machine learning. *Communications of the ACM, 62*(3), 54–60. https://doi.org/10.1145/3241036

39. Lakkaraju, H., Slack, D., Chen, Y., Tan, C., & Singh, S. (2022). *Rethinking explainability as a dialogue: A practitioner's perspective*. arXiv. https://doi.org/10.48550/arXiv.2202.01875

40. Holzinger, A., Langs, G., Denk, H., Zatloukal, K., & Müller, H. (2019). Causability and explainability of artificial intelligence in medicine. *WIREs Data Mining and Knowledge Discovery, 9*(4), e1312. https://doi.org/10.1002/widm.1312

41. Rajkomar, A., Hardt, M., Howell, M. D., Corrado, G., & Chin, M. H. (2018). Ensuring fairness in machine learning to advance health equity. *Annals of Internal Medicine, 169*(12), 866–872. https://doi.org/10.7326/M18-1990

42. Finlayson, S. G., Subbaswamy, A., Singh, K., Bowers, J., Kupke, A., Zittrain, J., Kohane, I. S., & Saria, S. (2021). The clinician and dataset shift in artificial intelligence. *New England Journal of Medicine, 385*(3), 283–286. https://doi.org/10.1056/NEJMc2104626

43. Rieke, N., Hancox, J., Li, W., Milletarì, F., Roth, H. R., Albarqouni, S., Bakas, S., Galtier, M. N., Landman, B. A., Maier-Hein, K., Ourselin, S., Sheller, M., Summers, R. M., Trask, A., Xu, D., Baust, M., & Cardoso, M. J. (2020). The future of digital health with federated learning. *npj Digital Medicine, 3*, 119. https://doi.org/10.1038/s41746-020-00323-1

44. Sendak, M. P., D'Arcy, J., Kashyap, S., Gao, M., Nichols, M., Corey, K., Ratliff, W., & Balu, S. (2020). A path for translation of machine learning products into healthcare delivery. *EMJ Innovations, 4*(1), 19–00172. https://doi.org/10.33590/emjinnov/19-00172

45. Vellido, A. (2020). The importance of interpretability and visualization in machine learning for applications in medicine and health care. *Neural Computing and Applications, 32*(24), 18069–18083. https://doi.org/10.1007/s00521-019-04051-w

---

*Note on citation style: In-text citations use bracketed serial numbers [1]–[45] in order of first appearance, with the reference list numbered accordingly; each entry is formatted in APA 7th-edition style. If the publisher requires strict author–date APA in-text citations, the bracketed numbers can be converted to (Author, Year) form using the mapping above.*

*AI Usage Disclosure: This chapter draft was prepared with the assistance of an AI writing tool for drafting, structuring, and reference formatting. All content, citations, and figures should be verified by the authors for accuracy prior to submission.*
