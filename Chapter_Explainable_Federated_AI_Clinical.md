# EXPLAINABLE AND FEDERATED ARTIFICIAL INTELLIGENCE FOR SECURE CLINICAL DECISION SUPPORT IN NEXT-GENERATION HEALTHCARE SYSTEMS

## Abstract

Artificial intelligence is reshaping clinical decision support, yet its adoption in healthcare is constrained by the sensitivity of patient data, the opacity of high-performing models, and the need for demonstrable trust. This chapter examines how the convergence of federated learning and explainable artificial intelligence can deliver secure, transparent, and reliable clinical decision support for next-generation healthcare systems. It begins by tracing the evolution of intelligent clinical decision support and articulating the intertwined challenges of data privacy, cybersecurity, and clinician trust. The chapter then presents federated learning as a privacy-preserving paradigm that enables multiple institutions to train shared models collaboratively without exchanging raw patient records, detailing distributed architectures, secure model aggregation, and defences against adversarial and inference-based cyber threats such as differential privacy, homomorphic encryption, and secure multi-party computation. Complementing this, it surveys explainable artificial intelligence techniques—both interpretable-by-design models and post-hoc methods—that render predictions intelligible to clinicians, and it proposes an integrated explainable-federated framework that unites privacy preservation with transparency for trustworthy clinical decision-making. Finally, the chapter reviews real-world clinical applications, system evaluation strategies, and implementation considerations, and it critically analyses the ethical, regulatory, and technical obstacles that remain, outlining future research directions toward responsible, accountable, and scalable intelligent healthcare.

**Keywords:** Federated learning; explainable artificial intelligence; clinical decision support; data privacy; healthcare security; trustworthy artificial intelligence

## 1. Introduction to Secure and Intelligent Healthcare Systems

### 1.1 Evolution of Artificial Intelligence in Clinical Decision Support

Clinical decision support has evolved from simple reminder systems into sophisticated analytical engines capable of informing diagnosis, prognosis, and treatment selection across virtually every medical specialty [1]. The earliest intelligent clinical systems emerged in the 1970s and 1980s as rule-based expert systems that encoded medical knowledge as explicit if-then rules; pioneering programs such as MYCIN demonstrated that a machine could reason about infectious disease and recommend antimicrobial therapy with expert-level competence within a narrow domain [2]. Although transparent and auditable, these systems were brittle, labour-intensive to maintain, and unable to learn from new data, which limited their scalability and real-world deployment.

The subsequent era was defined by statistical machine learning, in which models learned predictive patterns directly from structured clinical data rather than relying on hand-coded rules. Logistic regression, support vector machines, and ensemble methods became staples of risk stratification and outcome prediction, while careful feature engineering translated heterogeneous clinical variables into model inputs [1]. The most recent and transformative phase has been driven by deep learning, in which multilayer neural networks automatically learn hierarchical representations from raw data such as medical images, waveforms, and free-text notes [3]. Deep models have matched or exceeded specialist performance in tasks ranging from diabetic retinopathy screening to skin cancer classification, catalysing a wave of translational research into machine learning for medicine [4]. This progression—from transparent but limited rule-based systems through data-driven statistical learning to highly accurate but opaque deep networks—is summarized in Figure 1.

[Insert Figure 1 here]
Figure 1. Evolution of artificial intelligence in clinical decision support, from rule-based expert systems through statistical machine learning and deep learning to federated and explainable AI.

As clinical decision support systems have grown more capable, they have also become more deeply embedded in care delivery, integrating with electronic health records to provide alerts, risk scores, and recommendations at the point of care [5]. This integration amplifies both the potential benefits and the potential harms of automated inference: accurate, well-calibrated support can improve outcomes and efficiency, whereas unreliable or poorly understood predictions can propagate errors at scale. The trajectory depicted in Figure 1 therefore reflects not only increasing predictive power but also an expanding need for the privacy, security, and transparency safeguards that the remainder of this chapter addresses. The defining tension of contemporary healthcare AI is that the most accurate models are often the least interpretable and the most data-hungry, precisely when clinical data is most sensitive and most fragmented across institutions [1].

### 1.2 Challenges of Data Privacy, Security, and Trust in Healthcare AI

Healthcare data is among the most sensitive categories of personal information, and its use in machine learning raises acute privacy concerns [6]. Training high-performing models conventionally requires aggregating large volumes of patient records into centralized repositories, a practice that increases exposure to breaches and conflicts with the data-minimization principles embedded in regulatory frameworks [7]. In many jurisdictions, legal instruments such as the Health Insurance Portability and Accountability Act and the General Data Protection Regulation impose strict constraints on how patient data may be collected, transferred, and processed, and they establish rights and obligations that centralized data pooling struggles to satisfy [8]. These constraints, combined with institutional and national boundaries, leave clinical data siloed and underutilized, as highlighted by the fragmentation illustrated in the final stage of Figure 1.

Beyond regulatory compliance, machine learning models themselves can leak sensitive information. Membership inference attacks can determine whether a particular individual's record was part of a model's training set, while model inversion and gradient-based attacks can reconstruct features of the underlying data [9]. Such vulnerabilities mean that even models trained and shared without direct access to raw records can compromise patient confidentiality, motivating privacy-preserving training techniques discussed later in this chapter. Security threats extend further to the integrity of the models themselves, including data poisoning and adversarial manipulation that can degrade performance or introduce hidden malicious behaviour.

Equally important is the challenge of trust. Clinicians are professionally and ethically accountable for the decisions they make, and they are understandably reluctant to act on recommendations they cannot scrutinize or understand [10]. The opacity of deep learning models—their "black box" character—undermines accountability, complicates error analysis, and may obscure the spurious correlations or biases that models can inadvertently learn. Trust in healthcare AI is thus multidimensional, encompassing technical reliability, fairness across patient subgroups, privacy protection, and interpretability [10]. Addressing these intertwined challenges of privacy, security, and trust requires more than incremental improvements to individual models; it demands architectural paradigms that protect data by design and that make model behaviour transparent to the humans who remain responsible for patient care. The two complementary paradigms that form the core of this chapter—federated artificial intelligence and explainable artificial intelligence—respond directly to these needs.

## 2. Federated Artificial Intelligence for Privacy-Preserving Healthcare

### 2.1 Federated Learning Architectures and Distributed Clinical Data Integration

Federated learning is a distributed machine learning paradigm in which multiple participants collaboratively train a shared model while keeping their data local, exchanging only model parameters or updates rather than raw records [11]. Introduced as a method for learning from decentralized data on mobile devices, the canonical federated averaging algorithm iteratively trains local models at each participant, transmits the resulting updates to a coordinating server, and aggregates them into an improved global model that is then redistributed [11]. Applied to healthcare, this architecture allows hospitals, clinics, and research laboratories to contribute to a collective model without their patient data ever leaving the institution, directly reconciling the need for large, diverse training sets with the imperative to preserve privacy [12]. Figure 2 depicts this architecture, showing distributed clinical sites performing local training and sharing only encrypted updates through a secure aggregation and privacy layer with a central server.

[Insert Figure 2 here]
Figure 2. Federated learning architecture for privacy-preserving healthcare, in which distributed clinical sites train local models and exchange only encrypted updates through a secure aggregation and privacy layer, so that raw patient data never leaves the institution.

Federated learning in medicine is commonly organized as cross-silo collaboration, in which a modest number of reliable institutional participants—each holding substantial local datasets—jointly train a model, in contrast to the cross-device setting involving vast numbers of intermittently available clients [13]. This distinction matters because healthcare participants are relatively few, persistently available, and governed by formal agreements, which simplifies orchestration but introduces its own challenges around data heterogeneity and governance. A landmark multi-institutional study demonstrated that federated learning could train a tumour-segmentation model across geographically distributed centres and achieve performance comparable to a model trained on centrally pooled data, without any site sharing its patient images [14]. Such results establish federated learning as a credible route to the statistical power that rare diseases and underrepresented populations require.

A central obstacle to federated clinical learning is statistical heterogeneity: data distributions differ across institutions because of divergent patient populations, acquisition devices, labelling conventions, and care practices, violating the independent-and-identically-distributed assumption underlying many algorithms [15]. These non-identical distributions can slow convergence and bias the global model toward dominant sites, motivating algorithmic refinements such as personalization, proximal regularization, and adaptive aggregation. The practical value of overcoming these obstacles was dramatically illustrated during the COVID-19 pandemic, when a federated model trained across dozens of hospitals worldwide predicted clinical outcomes for patients more accurately and generalizably than models trained at any single site [16]. Table 1 contrasts centralized and federated learning across the dimensions most relevant to healthcare deployment, clarifying why the distributed approach shown in Figure 2 has gained traction despite its added complexity.

Table 1. Comparison of Centralized and Federated Learning for Healthcare

| Dimension | Centralized Learning | Federated Learning |
|-----------|----------------------|--------------------|
| Data location | Raw data pooled in one repository | Data remains at each institution |
| Privacy exposure | High; single point of breach | Reduced; only model updates shared |
| Regulatory burden | Complex cross-border data transfer | Aligns with data-minimization principles |
| Data diversity | Limited by what can be legally pooled | Broad, multi-institutional populations |
| Communication cost | One-time data upload | Repeated model-update exchange |
| Key challenge | Data governance and consent | Statistical heterogeneity and coordination |

As Table 1 indicates, the federated approach trades the one-time cost of centralizing data for the recurring cost of exchanging model updates, while substantially lowering privacy exposure and regulatory friction. This trade-off is generally favourable in healthcare, where the legal and ethical barriers to pooling data are often prohibitive [12]. Integrating distributed clinical data in this manner, however, presupposes that the model updates exchanged during training do not themselves leak sensitive information—an assumption that the next subsection examines and that the privacy-preserving layer is designed to enforce.

### 2.2 Privacy Preservation, Secure Model Aggregation, and Protection Against Cyber Threats

Although federated learning keeps raw data local, the model updates that participants share can still reveal private information, necessitating explicit privacy-preserving mechanisms within the secure aggregation pipeline. Differential privacy provides a rigorous mathematical framework for bounding the information that any single individual's data contributes to a released output, typically by adding calibrated noise to gradients or parameters during training [17]. Applied to deep learning, differentially private stochastic gradient descent clips per-example gradients and injects noise to furnish formal privacy guarantees, albeit at some cost to model accuracy that must be balanced against the privacy budget [18]. In the federated setting, differential privacy can be applied locally at each site or centrally during aggregation, offering tunable protection against inference attacks.

Secure aggregation complements differential privacy by ensuring that the coordinating server observes only the sum of participants' updates and never any individual contribution, using cryptographic protocols that mask updates in a way that cancels out when combined [19]. Homomorphic encryption offers an alternative or additional safeguard by allowing computations to be performed directly on encrypted updates, so that aggregation occurs without ever decrypting individual contributions [20]. Secure multi-party computation generalizes this idea, enabling multiple parties to jointly compute a function over their private inputs while revealing nothing beyond the result. These mechanisms, summarized in Table 2, can be layered to achieve defence in depth, each addressing a distinct part of the threat surface at a distinct computational cost.

Table 2. Privacy-Preserving and Security Mechanisms for Federated Clinical Learning

| Mechanism | Protection Provided | Principal Limitation |
|-----------|---------------------|----------------------|
| Differential privacy | Formal bound on individual data leakage | Accuracy loss as privacy budget tightens |
| Secure aggregation | Server sees only aggregate, not individual updates | Coordination overhead; dropout handling |
| Homomorphic encryption | Computation on encrypted updates | High computational and communication cost |
| Secure multi-party computation | Joint computation without revealing inputs | Protocol complexity; communication rounds |
| Robust aggregation | Resistance to poisoned or outlier updates | May discard legitimate heterogeneous updates |

The threats that these mechanisms counter are not hypothetical. Gradient-based reconstruction attacks have shown that shared gradients can be inverted to recover training images with striking fidelity, confirming that update sharing alone is insufficient for privacy [21]. Federated systems are also vulnerable to integrity attacks: malicious participants can poison the global model or implant backdoors by submitting carefully crafted updates, degrading performance or triggering targeted misbehaviour under specific conditions [22]. A broad analysis of federated learning threats distinguishes privacy attacks, which seek to extract information, from robustness attacks, which seek to corrupt the model, and emphasizes that realistic deployments must defend against both simultaneously [23]. Robust aggregation rules, anomaly detection on updates, and client authentication therefore complement the confidentiality mechanisms in Table 2.

Taken together, the mechanisms in Table 2 transform the generic federated architecture of Figure 2 into a system that is secure as well as collaborative. The appropriate combination depends on the threat model, the sensitivity of the data, the number and trustworthiness of participants, and the tolerance for computational overhead and accuracy degradation [23]. In practice, healthcare deployments frequently pair secure aggregation with a modest amount of differential privacy, achieving meaningful protection while preserving clinical utility. Yet privacy and security, however well engineered, do not by themselves make a model trustworthy to the clinicians who must act on its outputs; that requires the transparency provided by explainable artificial intelligence, to which the chapter now turns.

## 3. Explainable Artificial Intelligence for Transparent and Reliable Clinical Decision Support

### 3.1 Explainable AI Techniques for Interpretable Clinical Predictions

Explainable artificial intelligence encompasses methods that make the behaviour and predictions of machine learning models intelligible to humans, a capability that is indispensable when models inform decisions affecting patient health. As organized in Figure 3, explanation techniques fall into two broad families: models that are interpretable by design and post-hoc methods that explain already-trained models. Interpretable-by-design approaches include linear and logistic models, decision trees, rule lists, and generalized additive models, whose structure permits direct inspection of how inputs influence outputs. A compelling demonstration showed that an intelligible generalized additive model for pneumonia risk not only matched the accuracy of opaque models but also exposed a dangerous pattern the data had encoded, which a black-box model would have silently propagated [24].

[Insert Figure 3 here]
Figure 3. Taxonomy of explainable AI techniques for clinical predictions, distinguishing intrinsic interpretable-by-design models from post-hoc explanation methods that together yield human-interpretable evidence supporting clinician trust and accountability.

Post-hoc techniques explain models that are themselves opaque, and they dominate contemporary practice because the highest-performing clinical models are frequently deep networks. Local interpretable model-agnostic explanations approximate a complex model's behaviour near a specific prediction with a simple surrogate, highlighting which features drove that individual decision [25]. Shapley additive explanations draw on cooperative game theory to assign each feature a principled contribution to a prediction, providing both local and globally consistent attributions that have become widely adopted in clinical machine learning [26]. For imaging models, gradient-weighted class activation mapping produces saliency heatmaps that localize the regions of an image most responsible for a prediction, allowing clinicians to verify that a model attends to clinically relevant anatomy rather than artefacts [27]. Counterfactual explanations describe the minimal changes to inputs that would alter a prediction, offering actionable "what-if" reasoning that aligns naturally with clinical thinking [28]. Table 3 compares these techniques across the properties that matter for clinical use.

Table 3. Comparison of Explainable AI Techniques for Clinical Predictions

| Technique | Type | Explanation Output | Clinical Strength |
|-----------|------|--------------------|-------------------|
| Logistic / GAM | Intrinsic | Transparent feature weights | Directly auditable, trusted by clinicians |
| Decision tree / rules | Intrinsic | Explicit decision path | Mirrors clinical reasoning |
| LIME | Post-hoc, local | Local feature importance | Model-agnostic, intuitive |
| SHAP | Post-hoc, local/global | Consistent feature attributions | Theoretically grounded, widely used |
| Grad-CAM | Post-hoc, imaging | Saliency heatmap | Visual verification of image regions |
| Counterfactual | Post-hoc, example-based | Minimal actionable input change | Supports what-if clinical reasoning |

The choice among the techniques in Table 3 depends on the data modality, the model architecture, and the clinical question. Some scholars argue that for high-stakes healthcare decisions, inherently interpretable models should be preferred wherever they can match the accuracy of opaque alternatives, because post-hoc explanations may be unfaithful to the underlying model's true reasoning [29]. A survey of explainability in medicine echoes this caution while cataloguing the rapid growth of medical XAI and the diversity of techniques now available [30]. As Figure 3 emphasizes, the ultimate purpose of all these methods is the same: to convert an opaque prediction into human-interpretable evidence that supports clinician verification, accountability, and trust. The techniques in Table 3 are not mutually exclusive, and clinical systems increasingly combine several to serve different stakeholders and audit requirements.

### 3.2 Integrating Explainable and Federated AI for Trustworthy Clinical Decision-Making

Privacy preservation and interpretability have largely developed as separate research streams, yet trustworthy clinical decision support requires both simultaneously: a model must protect patient data and explain its reasoning. Comprehensive reviews of explainable artificial intelligence frame transparency as a cornerstone of responsible and trustworthy AI, situating the techniques of Figure 3 within broader principles of accountability, fairness, and human oversight [31]. In healthcare specifically, explainability is argued to be essential for establishing the trust that clinicians, patients, and regulators place in automated systems, because it enables error detection, supports informed consent, and clarifies responsibility when decisions are contested [32]. A multidisciplinary analysis further stresses that the adequacy of an explanation is context-dependent and must be evaluated against the needs of its human recipients rather than treated as a purely technical property [33].

Integrating explainability with federated learning introduces both opportunity and difficulty. On one hand, applying explanation methods to a federated global model can surface which features or image regions drive predictions across institutions, revealing site-specific biases and supporting equitable performance. On the other hand, generating explanations in a distributed setting must not reopen the privacy vulnerabilities that federation was designed to close, because explanations themselves can leak information about local data [34]. Research on federated and explainable medical AI has therefore begun to co-design the two paradigms, for example by producing privacy-preserving explanations and by evaluating interpretability consistently across heterogeneous sites [34]. The integrated framework in Figure 4 organizes these concerns into layered stages, from distributed data sources and federated training through a global collaborative model, an explainability engine, and finally clinical decision support delivered to clinicians.

[Insert Figure 4 here]
Figure 4. Integrated explainable-federated AI (XFL) framework for trustworthy clinical decision support, organizing distributed data, privacy-preserving federated training, a global collaborative model, an explainability engine, and clinician-facing decision support within a cross-cutting governance layer and a continual-learning feedback loop.

As Figure 4 illustrates, the explainability engine operates on the global model produced by privacy-preserving federated training, and its interpretable outputs feed into decision support that clinicians can scrutinize and act upon. A feedback loop returns clinician input to the system, enabling continual learning and refinement, while a cross-cutting governance band enforces ethics, regulation, security, and auditing throughout. This architecture makes explicit that trustworthiness is a property of the whole sociotechnical system rather than of any single model: privacy is protected during training, transparency is provided at inference, and human oversight and governance span the entire pipeline. This explainable-federated framework thus synthesizes the privacy mechanisms of Section 2 with the interpretability techniques of Section 3.1 into a coherent approach to trustworthy clinical decision-making.

## 4. Applications, Challenges, and Future Directions

### 4.1 Clinical Applications, System Evaluation, and Real-World Implementation

The explainable-federated approach outlined in Figure 4 is already being realized across diverse clinical domains. In medical imaging, federated models have been trained for tumour segmentation and disease classification across international consortia, and the federated COVID-19 outcome-prediction effort showed that a model aggregated from dozens of hospitals generalized better than locally trained counterparts [16]. Swarm learning, a decentralized variant that removes the central aggregator in favour of blockchain-coordinated peers, has been used to build clinical classifiers for leukaemia, tuberculosis, and COVID-19 from distributed data while preserving confidentiality [35]. Table 4 summarizes representative applications spanning imaging, electronic health record analytics, and genomics, together with the privacy and explainability features they employ.

Table 4. Representative Clinical Applications of Explainable and Federated AI

| Application Domain | Task | Federated / Privacy Feature | Explainability Feature |
|--------------------|------|------------------------------|------------------------|
| Radiology imaging | Tumour segmentation | Cross-silo federation, secure aggregation | Saliency heatmaps |
| Critical care (EHR) | Outcome / mortality prediction | Multi-hospital federation | SHAP feature attributions |
| Oncology / haematology | Disease classification | Swarm / decentralized learning | Attention and saliency |
| Chronic disease | Risk stratification | Differential privacy | Interpretable risk factors |
| Genomics | Variant interpretation | Encrypted aggregation | Counterfactual reasoning |

Rigorous evaluation of the systems in Table 4 must extend beyond conventional accuracy metrics to assess generalization across sites, fairness across patient subgroups, the fidelity and stability of explanations, and the strength of privacy guarantees. Benchmarks designed specifically for cross-silo federated learning in healthcare have begun to standardize such evaluation, providing realistic datasets and tasks that reflect the heterogeneity of real institutions [36]. Systematic reviews of federated healthcare systems propose reference architectures and catalogue the engineering considerations—communication efficiency, participant management, and model versioning—that practical deployments must address [37]. Successful real-world implementation additionally depends on institutional readiness, interoperable data standards, clinician workflow integration, and sustained governance, factors that determine whether the technical promise summarized in Table 4 translates into improved care [38].

### 4.2 Ethical, Regulatory, and Technical Challenges and Future Research Directions

Despite rapid progress, substantial challenges remain before explainable-federated clinical decision support can be deployed at scale. Ethically, automated systems can perpetuate or amplify biases present in training data, raising concerns about fairness and equity that explainability can help surface but not automatically resolve [39]. The federated setting complicates accountability further, because responsibility for a model's behaviour is distributed across participating institutions, and robust governance must therefore assign clear roles for data stewardship, model validation, and incident response [40]. Patients' rights to understand and contest decisions that affect them impose additional obligations that purely technical solutions cannot satisfy.

Regulatory frameworks are still adapting to data-driven and continually learning medical software, and authorities have proposed approaches for overseeing adaptive algorithms that balance innovation with patient safety, including expectations for good machine learning practice and lifecycle monitoring [41]. These evolving requirements interact directly with the privacy-preserving mechanisms and clinical applications discussed above, since regulators increasingly expect demonstrable privacy protection, transparency, and post-deployment surveillance. Technically, open problems persist across the federated learning landscape, including communication efficiency, robustness to heterogeneous and adversarial participants, and formal privacy accounting, all of which remain active areas of research [42]. Security analyses emphasize that federated systems face an expanding attack surface and that defences must evolve in tandem with emerging threats [43].

Future research directions follow directly from these challenges and from the integrated explainable-federated architecture described in this chapter. Co-designing privacy-preserving and explainable methods so that transparency does not compromise confidentiality is a priority, as is developing personalized federated models that respect the statistical heterogeneity of institutions while maintaining global coherence [42]. Standardized, clinically meaningful evaluation of both explanations and privacy guarantees—extending the benchmarking efforts that underpin these clinical applications—will be essential to build the evidence base that regulators and clinicians require [43]. Ultimately, realizing trustworthy intelligent healthcare will depend on close collaboration among computer scientists, clinicians, ethicists, and regulators to ensure that the secure, transparent systems envisioned in this chapter are also equitable, accountable, and genuinely beneficial to patients [40].

## 5. Conclusion

This chapter has argued that the secure and trustworthy deployment of artificial intelligence in clinical decision support depends on uniting two complementary paradigms. Federated learning addresses the privacy and security imperatives of healthcare by enabling institutions to train shared models without exchanging raw patient data, supported by secure aggregation and cryptographic safeguards that defend against inference and integrity attacks. Explainable artificial intelligence addresses the equally vital imperative of trust by rendering model predictions intelligible to the clinicians who remain accountable for patient care. Individually, each paradigm is necessary but insufficient; together, within an integrated and well-governed framework, they offer a credible path toward clinical decision support that is at once accurate, private, transparent, and reliable. Realizing this vision will require continued technical innovation in privacy-preserving explanation, rigorous and clinically meaningful evaluation, adaptive regulation, and sustained interdisciplinary collaboration. As next-generation healthcare systems increasingly rely on distributed intelligence, the explainable-federated approach described here provides a principled foundation for responsible innovation that places patient privacy, clinician trust, and equitable benefit at its centre.

## References

[1] Topol EJ. High-performance medicine: the convergence of human and artificial intelligence. Nature Medicine. 2019;25(1):44-56.

[2] Shortliffe EH. Computer-Based Medical Consultations: MYCIN. New York: Elsevier; 1976.

[3] Esteva A, Robicquet A, Ramsundar B, Kuleshov V, DePristo M, Chou K, et al. A guide to deep learning in healthcare. Nature Medicine. 2019;25(1):24-29.

[4] Rajkomar A, Dean J, Kohane I. Machine learning in medicine. New England Journal of Medicine. 2019;380(14):1347-1358.

[5] Sutton RT, Pincock D, Baumgart DC, Sadowski DC, Fedorak RN, Kroeker KI. An overview of clinical decision support systems: benefits, risks, and strategies for success. npj Digital Medicine. 2020;3:17.

[6] Price WN, Cohen IG. Privacy in the age of medical big data. Nature Medicine. 2019;25(1):37-43.

[7] Kaissis GA, Makowski MR, Ruckert D, Braren RF. Secure, privacy-preserving and federated machine learning in medical imaging. Nature Machine Intelligence. 2020;2(6):305-311.

[8] Voigt P, von dem Bussche A. The EU General Data Protection Regulation (GDPR): A Practical Guide. Cham: Springer; 2017.

[9] Shokri R, Stronati M, Song C, Shmatikov V. Membership inference attacks against machine learning models. In: IEEE Symposium on Security and Privacy; 2017. p. 3-18.

[10] Vayena E, Blasimme A, Cohen IG. Machine learning in medicine: addressing ethical challenges. PLoS Medicine. 2018;15(11):e1002689.

[11] McMahan B, Moore E, Ramage D, Hampson S, Aguera y Arcas B. Communication-efficient learning of deep networks from decentralized data. In: Proceedings of AISTATS; 2017. p. 1273-1282.

[12] Rieke N, Hancox J, Li W, Milletari F, Roth HR, Albarqouni S, et al. The future of digital health with federated learning. npj Digital Medicine. 2020;3:119.

[13] Yang Q, Liu Y, Chen T, Tong Y. Federated machine learning: concept and applications. ACM Transactions on Intelligent Systems and Technology. 2019;10(2):12.

[14] Sheller MJ, Edwards B, Reina GA, Martin J, Pati S, Kotrotsou A, et al. Federated learning in medicine: facilitating multi-institutional collaborations without sharing patient data. Scientific Reports. 2020;10:12598.

[15] Li T, Sahu AK, Talwalkar A, Smith V. Federated learning: challenges, methods, and future directions. IEEE Signal Processing Magazine. 2020;37(3):50-60.

[16] Dayan I, Roth HR, Zhong A, Harouni A, Gentili A, Abidin AZ, et al. Federated learning for predicting clinical outcomes in patients with COVID-19. Nature Medicine. 2021;27(10):1735-1743.

[17] Dwork C, Roth A. The algorithmic foundations of differential privacy. Foundations and Trends in Theoretical Computer Science. 2014;9(3-4):211-407.

[18] Abadi M, Chu A, Goodfellow I, McMahan HB, Mironov I, Talwar K, et al. Deep learning with differential privacy. In: Proceedings of the ACM SIGSAC Conference on Computer and Communications Security; 2016. p. 308-318.

[19] Bonawitz K, Ivanov V, Kreuter B, Marcedone A, McMahan HB, Patel S, et al. Practical secure aggregation for privacy-preserving machine learning. In: Proceedings of the ACM SIGSAC Conference on Computer and Communications Security; 2017. p. 1175-1191.

[20] Acar A, Aksu H, Uluagac AS, Conti M. A survey on homomorphic encryption schemes: theory and implementation. ACM Computing Surveys. 2018;51(4):79.

[21] Zhu L, Liu Z, Han S. Deep leakage from gradients. In: Advances in Neural Information Processing Systems; 2019. p. 14774-14784.

[22] Bagdasaryan E, Veit A, Hua Y, Estrin D, Shmatikov V. How to backdoor federated learning. In: Proceedings of AISTATS; 2020. p. 2938-2948.

[23] Lyu L, Yu H, Yang Q. Threats to federated learning: a survey. arXiv preprint arXiv:2003.02133. 2020.

[24] Caruana R, Lou Y, Gehrke J, Koch P, Sturm M, Elhadad N. Intelligible models for healthcare: predicting pneumonia risk and hospital 30-day readmission. In: Proceedings of the ACM SIGKDD International Conference on Knowledge Discovery and Data Mining; 2015. p. 1721-1730.

[25] Ribeiro MT, Singh S, Guestrin C. "Why should I trust you?": explaining the predictions of any classifier. In: Proceedings of the ACM SIGKDD International Conference on Knowledge Discovery and Data Mining; 2016. p. 1135-1144.

[26] Lundberg SM, Lee SI. A unified approach to interpreting model predictions. In: Advances in Neural Information Processing Systems; 2017. p. 4765-4774.

[27] Selvaraju RR, Cogswell M, Das A, Vedantam R, Parikh D, Batra D. Grad-CAM: visual explanations from deep networks via gradient-based localization. In: Proceedings of the IEEE International Conference on Computer Vision; 2017. p. 618-626.

[28] Wachter S, Mittelstadt B, Russell C. Counterfactual explanations without opening the black box: automated decisions and the GDPR. Harvard Journal of Law and Technology. 2017;31(2):841-887.

[29] Rudin C. Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead. Nature Machine Intelligence. 2019;1(5):206-215.

[30] Tjoa E, Guan C. A survey on explainable artificial intelligence (XAI): toward medical XAI. IEEE Transactions on Neural Networks and Learning Systems. 2021;32(11):4793-4813.

[31] Arrieta AB, Diaz-Rodriguez N, Del Ser J, Bennetot A, Tabik S, Barbado A, et al. Explainable artificial intelligence (XAI): concepts, taxonomies, opportunities and challenges toward responsible AI. Information Fusion. 2020;58:82-115.

[32] Markus AF, Kors JA, Rijnbeek PR. The role of explainability in creating trustworthy artificial intelligence for health care: a comprehensive survey of the terminology, design choices, and evaluation strategies. Journal of Biomedical Informatics. 2021;113:103655.

[33] Amann J, Blasimme A, Vayena E, Frey D, Madai VI. Explainability for artificial intelligence in healthcare: a multidisciplinary perspective. BMC Medical Informatics and Decision Making. 2020;20:310.

[34] Chaddad A, Peng J, Xu J, Bouridane A. Survey of explainable AI techniques in healthcare. Sensors. 2023;23(2):634.

[35] Warnat-Herresthal S, Schultze H, Shastry KL, Manamohan S, Mukherjee S, Garg V, et al. Swarm learning for decentralized and confidential clinical machine learning. Nature. 2021;594(7862):265-270.

[36] Ogier du Terrail J, Ayed SS, Cyffers E, Grimberg F, He C, Loeb R, et al. FLamby: datasets and benchmarks for cross-silo federated learning in healthcare. In: Advances in Neural Information Processing Systems; 2022.

[37] Antunes RS, Andre da Costa C, Kuderle A, Yari IA, Eskofier B. Federated learning for healthcare: systematic review and architecture proposal. ACM Transactions on Intelligent Systems and Technology. 2022;13(4):54.

[38] Nguyen DC, Pham QV, Pathirana PN, Ding M, Seneviratne A, Lin Z, et al. Federated learning for smart healthcare: a survey. ACM Computing Surveys. 2022;55(3):60.

[39] Gerke S, Minssen T, Cohen G. Ethical and legal challenges of artificial intelligence-driven healthcare. In: Artificial Intelligence in Healthcare. London: Academic Press; 2020. p. 295-336.

[40] Reddy S, Allan S, Coghlan S, Cooper P. A governance model for the application of AI in health care. Journal of the American Medical Informatics Association. 2020;27(3):491-497.

[41] U.S. Food and Drug Administration. Artificial Intelligence/Machine Learning (AI/ML)-Based Software as a Medical Device (SaMD) Action Plan. Silver Spring, MD: FDA; 2021.

[42] Kairouz P, McMahan HB, Avent B, Bellet A, Bennis M, Bhagoji AN, et al. Advances and open problems in federated learning. Foundations and Trends in Machine Learning. 2021;14(1-2):1-210.

[43] Mothukuri V, Parizi RM, Pouriyeh S, Huang Y, Dehghantanha A, Srivastava G. A survey on security and privacy of federated learning. Future Generation Computer Systems. 2021;115:619-640.
