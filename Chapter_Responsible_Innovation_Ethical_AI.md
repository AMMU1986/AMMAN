# Responsible Innovation and Ethical AI Governance

**Amman Jakhar** (Corresponding author). Department of Mechanical Engineering, Chandigarh University, Mohali, Punjab-140301, India. Email: ammanjakhar5000734@gmail.com. ORCID: 0009-0004-1234-5678.

**Sachin Kalsi.** Department of Mechanical Engineering, Chandigarh University, Mohali, Punjab-140301, India. Email: sachin.kalsi@cumail.in. ORCID: 0000-0002-2345-6789.

**Abstract.** Artificial intelligence is reshaping how organisations create value, make decisions, and compete, yet the same capabilities that drive innovation can amplify bias, erode privacy, and obscure accountability. This chapter examines how responsible innovation and ethical governance can be embedded throughout the AI innovation process so that technological progress remains aligned with societal values and public trust. Building on the responsible innovation tradition, we argue that anticipation, reflexivity, inclusion, and responsiveness provide a durable foundation for governing AI under conditions of uncertainty. We then analyse five interdependent ethical principles that recur across the global policy landscape, namely transparency, fairness, accountability, privacy protection, and human-centricity, and show how each is translated from abstract commitment into concrete organisational practice. The discussion turns to four persistent governance challenges: algorithmic bias, diffuse accountability in complex sociotechnical systems, the need for deliberative governance, and meaningful multi-stakeholder engagement. To address these challenges, we propose an integrated governance model that connects societal values, ethical principles, operational processes, and independent oversight across the design, development, deployment, and monitoring stages of the AI lifecycle. The model is illustrated with reference to leading international frameworks and is intended to guide business leaders, policymakers, and practitioners navigating responsible AI adoption. We conclude that ethical governance of AI is not merely a compliance obligation but a strategic capability that sustains innovation, reduces risk, and secures long-term organisational legitimacy in a rapidly evolving regulatory and social environment.

**JEL Codes:** D63; K24; M14; M15; O31; O33

**Keywords:** Algorithmic accountability; Artificial intelligence; Ethical governance; Multi-stakeholder engagement; Responsible innovation; Transparency

## 1. Introduction

Artificial intelligence (AI) has moved from a specialised research pursuit to a general-purpose capability that permeates products, services, and strategic decisions across virtually every sector. As organisations race to capture the value of prediction, automation, and generative systems, they increasingly confront a parallel imperative: to ensure that innovation is conducted responsibly, ethically, and in a manner that preserves public trust. The central premise of this chapter is that innovation and ethics are not competing objectives but mutually reinforcing dimensions of durable value creation. Responsible innovation offers a mature intellectual foundation for reconciling the two, directing attention not only to what technologies can do but to whether, for whom, and under what conditions they ought to be deployed [1]. Its guiding aspiration is to align the trajectory of technological development with widely shared societal values and expectations [2].

The responsible innovation literature emerged in response to a recurring pattern in which powerful technologies advanced faster than the institutions meant to govern them, producing harms that became visible only after deployment [3]. AI intensifies this dynamic because its systems learn from data, operate at scale, adapt over time, and often function opaquely, making their consequences difficult to anticipate and to reverse. A substantial body of work has translated broad ethical aspirations into principles intended to steer AI toward socially beneficial outcomes [4]. Yet a comparative analysis of dozens of guidelines documents revealed a striking convergence on high-level principles alongside persistent divergence in how those principles are interpreted and implemented [5]. The recognition that principles alone cannot guarantee ethical AI has shifted scholarly and practical attention from articulating values to designing the governance mechanisms through which values are enacted [6].

This chapter contributes to that shift. It connects the theory of responsible innovation to the practice of ethical AI governance, and it argues that governance must be woven through the entire innovation process rather than appended as a final compliance check. The remainder proceeds as follows. Section 2 develops the responsible innovation foundations and their translation to AI. Section 3 examines five core ethical principles and their practical manifestations. Section 4 analyses four major governance challenges. Section 5 proposes an integrated governance model and situates it within leading international frameworks. Section 6 draws out implications for business leaders and policymakers, and Section 7 concludes.

## 2. From Responsible Innovation to Responsible AI

Responsible innovation is commonly articulated through four interrelated dimensions, often summarised by the acronym AREA: anticipation, reflexivity, inclusion, and responsiveness [1]. Anticipation involves systematically imagining the plausible impacts, risks, and futures associated with a technology before they materialise, using foresight, scenario analysis, and impact assessment to surface concerns early. Reflexivity requires developers and organisations to hold a mirror to their own assumptions, values, and limitations, acknowledging that technical choices encode normative commitments. Inclusion opens the innovation process to a plurality of voices, especially those of communities likely to be affected, so that design is informed by diverse perspectives rather than the priorities of a narrow group. Responsiveness is the capacity to act on what anticipation, reflexivity, and inclusion reveal, adapting the direction and shape of innovation in response to emerging knowledge and public values. Figure 1 depicts how these four dimensions surround and inform responsible AI innovation while being applied iteratively across the lifecycle.

[Insert Figure 1 here]

Figure 1. The AREA dimensions of responsible innovation integrated across the AI lifecycle. Source: Authors' own elaboration, based on Stilgoe et al. (2013) [1] and Dignum (2019) [7].

Translating these dimensions to AI requires attention to the specific properties that make AI systems ethically consequential. Because AI systems are sociotechnical, embedding data, models, and human institutions, the ethics of algorithms cannot be reduced to code quality alone but must address how systems interact with organisational and social contexts [8]. Responsible AI, understood as the practice of developing and deploying AI in ways that are accountable to human values, provides an organising concept that links the abstract dimensions of responsible innovation to concrete engineering and management decisions [7]. The pressing question for practitioners is one of translation, namely how to move from what ethical AI requires to how it is achieved in daily development work [9]. Table 1 maps each responsible innovation dimension to representative AI governance practices, illustrating how anticipation, reflexivity, inclusion, and responsiveness can be operationalised.

Table 1. Mapping of responsible innovation dimensions to concrete AI governance practices. Source: Authors' own elaboration, adapted from Stilgoe et al. (2013) [1], Dignum (2019) [7], and Morley et al. (2020) [9].

| RI Dimension | Guiding Question | Representative AI Practices |
| --- | --- | --- |
| Anticipation | What could go wrong, and for whom? | Algorithmic impact assessment, scenario analysis, red-teaming, risk classification |
| Reflexivity | Whose values are embedded in the system? | Value elicitation, model and data documentation, ethics review of design choices |
| Inclusion | Who should have a voice in design? | Participatory design, stakeholder consultation, community advisory panels |
| Responsiveness | How will we adapt when harms emerge? | Monitoring, incident response, model updating, redress and appeal mechanisms |

As Table 1 makes clear, the four dimensions are not sequential stages but continuous commitments that must be revisited as a system evolves. The lifecycle strip in Figure 1 reinforces this point: anticipation is most valuable at design, inclusion shapes both design and deployment, and responsiveness depends on monitoring that feeds back into subsequent iterations. Responsible AI, in this reading, is less a destination than a disciplined practice of ongoing reflection and adjustment [9].

## 3. Core Ethical Principles for AI

Across the many AI ethics frameworks published by governments, companies, and civil society, a recurring set of principles has crystallised [4] [5]. This chapter concentrates on five that are especially salient for governance because each generates concrete obligations and measurable practices: transparency, fairness, accountability, privacy protection, and human-centricity. Figure 2 presents these principles as interdependent pillars that together support trustworthy and responsible AI, resting on a foundation of societal values, human rights, and the rule of law.

[Insert Figure 2 here]

Figure 2. Five interdependent ethical principles as pillars of trustworthy AI. Source: Authors' own elaboration, informed by Floridi et al. (2018) [4] and Jobin et al. (2019) [5].

### 3.1 Transparency and Explainability

Transparency concerns the extent to which the existence, purpose, data, and logic of an AI system can be understood by those who build, use, and are affected by it. In consequential domains, affected individuals have a legitimate interest in understanding decisions that shape their lives, and debates about a right to explanation have highlighted both its promise and its legal ambiguity [10]. Because interpretability is used to mean many different things, researchers have called for greater rigour in defining what explanation is for and how it should be evaluated [11]. A prominent argument holds that for high-stakes decisions, inherently interpretable models are often preferable to opaque models supplemented by post hoc explanations, which can be unstable or misleading [12]. The field of explainable AI has nonetheless produced a rich taxonomy of methods for rendering complex models more intelligible [13], and sustained programmes of research have advanced techniques that help users understand, trust, and appropriately rely on machine outputs [14].

### 3.2 Fairness and Non-Discrimination

Fairness addresses the risk that AI systems reproduce or amplify unjust patterns present in data or design. Data-driven systems can generate discriminatory outcomes even without discriminatory intent, because historical data encode past inequities and proxy variables correlate with protected attributes [15]. Surveys of bias and fairness in machine learning catalogue numerous sources of bias across the pipeline and a corresponding proliferation of formal fairness definitions, several of which cannot be satisfied simultaneously [16]. Empirical audits have made these risks concrete: an evaluation of commercial facial analysis systems found substantially higher error rates for darker-skinned women than for lighter-skinned men [17], and analysis of a widely used health algorithm revealed that reliance on healthcare cost as a proxy for need systematically disadvantaged Black patients [18]. Scholars caution that fairness cannot be fully resolved within the model alone, since abstracting a system from its social context can obscure the very harms it produces [19]. Achieving fairness in practice therefore demands sociotechnical attention to context, deployment, and the availability of sensitive attributes needed to detect disparities [20].

### 3.3 Accountability

Accountability concerns who is answerable for the behaviour and consequences of an AI system, and through what mechanisms. Algorithmic decision-making can diffuse responsibility across data providers, developers, deployers, and users, creating gaps in which no actor is clearly accountable [21]. Closing these gaps requires structured practices such as internal auditing conducted before deployment to surface risks while they can still be addressed [22]. Technical and procedural tools can render algorithms accountable to oversight bodies even when full transparency is infeasible, for example through logging, testing, and cryptographic assurances [23]. Recent work distinguishes multiple senses of accountability, clarifying that it functions both as a backward-looking mechanism for attributing responsibility and as a forward-looking driver of better governance [24]. Designing systems to be reviewable, so that their decisions can be reconstructed and contested after the fact, offers a practical route to meaningful accountability in complex pipelines [25].

### 3.4 Privacy Protection

Privacy protection addresses how AI systems collect, infer, and use personal information. The theory of contextual integrity holds that privacy is not simply secrecy but the appropriate flow of information according to the norms of the context in which it was shared, a lens well suited to AI systems that repurpose data across contexts [26]. Regulatory regimes have codified many of these expectations, and the General Data Protection Regulation in particular establishes obligations around lawful basis, purpose limitation, data minimisation, and data subject rights that directly constrain AI development [27]. For AI, privacy risk extends beyond raw data to inferences drawn about individuals, requiring safeguards throughout the data lifecycle.

### 3.5 Human-Centricity

Human-centricity insists that AI augment rather than diminish human agency, keeping people meaningfully in control of consequential decisions. Human-centred AI frames the goal as systems that are simultaneously highly automated and subject to high levels of human control, rejecting the assumption that autonomy and oversight are inversely related [28]. Practical guidelines for human-AI interaction translate this commitment into design recommendations governing how systems communicate capabilities, handle errors, and support user control [29]. Table 2 summarises the five principles alongside their practical manifestations and characteristic risks when the principle is neglected.

Table 2. Core ethical principles, their practical manifestation, and risks of neglect. Source: Authors' own elaboration, synthesised from Jobin et al. (2019) [5], Mittelstadt et al. (2016) [8], and Shneiderman (2020) [28].

| Principle | Practical Manifestation | Risk if Neglected |
| --- | --- | --- |
| Transparency | Documentation, disclosure, explanations | Unaccountable, unchallengeable decisions |
| Fairness | Bias testing, representative data, audits | Discrimination and reputational harm |
| Accountability | Audits, logging, clear ownership, redress | Responsibility gaps and impunity |
| Privacy | Minimisation, consent, purpose limitation | Surveillance and loss of trust |
| Human-centricity | Human oversight, contestability, control | Loss of agency and automation harm |

Table 2 underscores that the five principles are interdependent rather than separable checkboxes. Transparency, for instance, is a precondition for accountability, and human-centricity depends on the contestability that fairness and transparency make possible. This interdependence, also visible in the pillar structure of Figure 2, means that governance must address the principles as a coherent system rather than optimising each in isolation [8].

## 4. Governance Challenges in Complex AI Systems

Even where organisations endorse ethical principles, translating them into reliable outcomes confronts structural challenges. Four are particularly consequential: algorithmic bias, accountability in complex systems, the need for deliberative governance, and meaningful multi-stakeholder engagement. Table 3 summarises each challenge, its underlying cause, and promising governance responses.

Table 3. Major governance challenges, their causes, and governance responses. Source: Authors' own elaboration, drawing on Mehrabi et al. (2021) [16], Raji et al. (2020) [22], and Cath (2018) [30].

| Challenge | Underlying Cause | Governance Response |
| --- | --- | --- |
| Algorithmic bias | Skewed data, proxy variables, design choices | Bias audits, diverse data, fairness metrics, monitoring |
| Diffuse accountability | Complex supply chains and opaque models | Reviewability, impact assessment, clear responsibility |
| Governance deficit | Fast innovation outpacing oversight | Deliberative and anticipatory governance mechanisms |
| Weak stakeholder voice | Exclusion of affected communities | Structured, meaningful multi-stakeholder engagement |

### 4.1 Algorithmic Bias

Algorithmic bias remains among the most visible governance challenges because its harms fall unevenly on already marginalised groups. As Table 3 indicates, bias arises not from a single fault but from an accumulation of choices about data, features, objectives, and thresholds [16]. Mitigation is complicated by the incompatibility of competing fairness criteria and by the risk that inferences about individuals extend beyond what they disclosed, raising the question of whether people hold a right to reasonable inferences drawn by algorithms [31]. Effective governance therefore combines technical measures with organisational accountability and continuous monitoring rather than treating bias as a one-time correction.

### 4.2 Accountability in Complex Systems

As AI systems are assembled from pre-trained components, third-party models, and automated pipelines, tracing responsibility for a given outcome becomes difficult. This diffusion is the practical core of the accountability challenge introduced in Section 3.3 and summarised in Table 3, and it is compounded when systems adapt after deployment. Governance responses emphasise auditability, documentation, and reviewability so that decisions can be reconstructed and contested [22] [25].

### 4.3 The Need for Deliberative Governance

Because AI raises value-laden questions on which reasonable people disagree, governance cannot be reduced to technical optimisation and instead requires deliberation about ends as well as means. The society-in-the-loop framing argues that embedding a social contract into AI governance requires mechanisms for negotiating and encoding collective values, not merely aggregating individual preferences [32]. Complementing this, the argument that ethical governance is essential to building justified public trust holds that transparent processes of standard-setting and oversight are themselves constitutive of trustworthiness [33].

### 4.4 Multi-Stakeholder Engagement

Meaningful governance depends on including those who develop, deploy, use, and are affected by AI. Yet participation can be tokenistic, and scholars warn that participation is not a design fix for structural problems unless it genuinely shares power with affected communities [34]. Framing AI governance as a shared responsibility distributed across technical, ethical, legal, and political domains clarifies why no single actor can secure responsible outcomes alone [30]. Figure 4 depicts the resulting ecosystem, in which developers, business leaders, regulators, affected communities, civil society, and end users engage in bidirectional deliberation and feedback around an AI system.

[Insert Figure 4 here]

Figure 4. Deliberative, multi-stakeholder ecosystem surrounding an AI system. Source: Authors' own elaboration, informed by Rahwan (2018) [32] and Sloane et al. (2022) [34].

As Figure 4 suggests, the value of multi-stakeholder engagement lies not in consultation for its own sake but in creating durable channels through which concerns can shape design and through which affected parties can contest outcomes. When such channels are absent, the governance deficit identified in Table 3 widens, and trust erodes.

## 5. An Integrated Governance Model

The preceding analysis motivates an integrated model that connects values, principles, processes, and oversight across the AI lifecycle. Figure 3 presents this model as four governance layers applied to four lifecycle stages. The value layer anchors governance in societal values, human rights, and organisational purpose. The principle layer operationalises those values through transparency, fairness, accountability, and privacy. The process layer supplies the operational machinery of impact assessment, audits, documentation, and testing. The oversight layer provides independent assurance through ethics boards, regulators, redress, and monitoring. Crucially, a continuous feedback loop returns lessons from monitoring to redesign, reflecting the responsiveness dimension introduced in Section 2.

[Insert Figure 3 here]

Figure 3. Layered governance mechanisms applied across each stage of the AI lifecycle. Source: Authors' own elaboration, integrating the EU High-Level Expert Group guidelines [35] and the NIST AI Risk Management Framework [36].

This model is consistent with, and can be instantiated through, leading international frameworks. The European approach to trustworthy AI specifies that systems should be lawful, ethical, and robust, and translates these into concrete requirements and an assessment process [35]. Intergovernmental principles have established shared commitments to inclusive growth, human-centred values, transparency, robustness, and accountability among adopting states [37], while a global standard-setting instrument has articulated the ethics of AI in terms of human rights and dignity [38]. Binding regulation has advanced through a risk-based statute that imposes obligations proportionate to the level of risk a system poses [39]. Voluntary but influential guidance provides a structured process for mapping, measuring, and managing AI risks that organisations can adopt regardless of jurisdiction [36]. Comparative analysis of these and other documents confirms a convergence around a consistent set of thematic commitments, even as implementation details differ [40]. Table 4 compares five prominent frameworks along their core orientation and governance emphasis.

Table 4. Comparison of leading AI governance frameworks. Source: Authors' own elaboration, based on European Commission (2019) [35], OECD (2019) [37], UNESCO (2021) [38], European Parliament and Council (2024) [39], and NIST (2023) [36].

| Framework | Core Orientation | Governance Emphasis |
| --- | --- | --- |
| EU Trustworthy AI Guidelines [35] | Lawful, ethical, robust AI | Requirements and self-assessment |
| OECD AI Principles [37] | Human-centred, inclusive values | Intergovernmental commitments |
| UNESCO Recommendation [38] | Human rights and dignity | Global ethical standard-setting |
| EU AI Act [39] | Risk-based regulation | Binding, proportionate obligations |
| NIST AI RMF [36] | Risk management process | Map, measure, manage, govern |

Table 4 shows that the frameworks are complementary rather than competing: principle-based instruments supply the normative orientation, process-based frameworks supply operational method, and binding regulation supplies enforceable obligations. An organisation implementing the layered model in Figure 3 can therefore draw on international principles for its value and principle layers, on risk-management frameworks for its process layer, and on regulation and independent review for its oversight layer. The integration of these sources into a single coherent architecture is what distinguishes governance as a strategic capability from governance as fragmented compliance.

## 6. Implications for Business Leaders and Policymakers

For business leaders, the central implication is that ethical governance of AI is a source of strategic advantage rather than a constraint on it. Deploying AI as a force for social good depends on deliberate design and governance choices rather than on the technology alone [41]. Concrete mechanisms can support trustworthy AI development and allow organisations to make verifiable claims about their systems, moving beyond aspirational statements to demonstrable practice [42]. Organisations that build governance capabilities early are better positioned to manage regulatory change, avoid costly failures, and earn the trust of customers, employees, and regulators. Because responsibility for AI ultimately rests with the humans and institutions that design and deploy it, leaders cannot delegate ethical judgement to the systems themselves [43].

For policymakers, the analysis underscores the need for governance that is anticipatory, deliberative, and attentive to power. Critical scholarship reminds us that AI is not an abstract or neutral artefact but is embedded in material, economic, and political structures that shape who benefits and who bears the costs [44]. Policy should therefore promote transparency and contestability, resource meaningful participation by affected communities, and ensure that individuals retain avenues to understand and challenge automated decisions, including through explanations that indicate how a different outcome might have been reached [45]. The layered model in Figure 3 and the stakeholder ecosystem in Figure 4 together suggest that effective policy operates at multiple levels simultaneously, combining enforceable rules with softer mechanisms that cultivate a culture of responsibility. Realising fairness and accountability in practice further depends on institutional support for the audits, monitoring, and redress mechanisms summarised in Table 2 and Table 4.

## 7. Conclusion

This chapter has argued that responsible innovation and ethical governance are essential companions to AI-driven value creation. Beginning from the responsible innovation dimensions of anticipation, reflexivity, inclusion, and responsiveness, it has shown how these commitments can be translated into the practice of responsible AI and operationalised through five interdependent ethical principles. It has analysed four governance challenges that recur across sectors and proposed an integrated model that connects values, principles, processes, and oversight across the AI lifecycle, drawing on leading international frameworks. The overarching message is that ethical governance of AI is not a peripheral compliance exercise but a strategic capability. Organisations that embed governance throughout the innovation process, engage stakeholders meaningfully, and remain responsive to emerging harms will be better equipped to innovate sustainably and to sustain the legitimacy on which long-term success depends. As AI systems grow more capable and pervasive, the discipline of doing innovation responsibly will increasingly distinguish organisations that merely adopt AI from those that adopt it well.

## References

[1] Stilgoe, J., Owen, R., & Macnaghten, P. (2013). Developing a framework for responsible innovation. Research Policy, 42(9), 1568-1580. https://doi.org/10.1016/j.respol.2013.05.008

[2] Von Schomberg, R. (2013). A vision of responsible research and innovation. In R. Owen, J. Bessant, & M. Heintz (Eds.), Responsible innovation (pp. 51-74). Wiley. https://doi.org/10.1002/9781118551424.ch3

[3] Owen, R., Macnaghten, P., & Stilgoe, J. (2012). Responsible research and innovation: From science in society to science for society, with society. Science and Public Policy, 39(6), 751-760. https://doi.org/10.1093/scipol/scs093

[4] Floridi, L., Cowls, J., Beltrametti, M., Chatila, R., Chazerand, P., Dignum, V., Luetge, C., Madelin, R., Pagallo, U., Rossi, F., Schafer, B., Valcke, P., & Vayena, E. (2018). AI4People: An ethical framework for a good AI society. Minds and Machines, 28(4), 689-707. https://doi.org/10.1007/s11023-018-9482-5

[5] Jobin, A., Ienca, M., & Vayena, E. (2019). The global landscape of AI ethics guidelines. Nature Machine Intelligence, 1(9), 389-399. https://doi.org/10.1038/s42256-019-0088-2

[6] Mittelstadt, B. (2019). Principles alone cannot guarantee ethical AI. Nature Machine Intelligence, 1(11), 501-507. https://doi.org/10.1038/s42256-019-0114-4

[7] Dignum, V. (2019). Responsible artificial intelligence: How to develop and use AI in a responsible way. Springer. https://doi.org/10.1007/978-3-030-30371-6

[8] Mittelstadt, B. D., Allo, P., Taddeo, M., Wachter, S., & Floridi, L. (2016). The ethics of algorithms: Mapping the debate. Big Data & Society, 3(2), 1-21. https://doi.org/10.1177/2053951716679679

[9] Morley, J., Floridi, L., Kinsey, L., & Elhalal, A. (2020). From what to how: An initial review of publicly available AI ethics tools, methods and research to translate principles into practices. Science and Engineering Ethics, 26(4), 2141-2168. https://doi.org/10.1007/s11948-019-00165-5

[10] Wachter, S., Mittelstadt, B., & Floridi, L. (2017). Why a right to explanation of automated decision-making does not exist in the General Data Protection Regulation. International Data Privacy Law, 7(2), 76-99. https://doi.org/10.1093/idpl/ipx005

[11] Doshi-Velez, F., & Kim, B. (2017). Towards a rigorous science of interpretable machine learning. arXiv. https://doi.org/10.48550/arXiv.1702.08608

[12] Rudin, C. (2019). Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead. Nature Machine Intelligence, 1(5), 206-215. https://doi.org/10.1038/s42256-019-0048-x

[13] Barredo Arrieta, A., Diaz-Rodriguez, N., Del Ser, J., Bennetot, A., Tabik, S., Barbado, A., Garcia, S., Gil-Lopez, S., Molina, D., Benjamins, R., Chatila, R., & Herrera, F. (2020). Explainable Artificial Intelligence (XAI): Concepts, taxonomies, opportunities and challenges toward responsible AI. Information Fusion, 58, 82-115. https://doi.org/10.1016/j.inffus.2019.12.012

[14] Gunning, D., Stefik, M., Choi, J., Miller, T., Stumpf, S., & Yang, G. Z. (2019). XAI-Explainable artificial intelligence. Science Robotics, 4(37), eaay7120. https://doi.org/10.1126/scirobotics.aay7120

[15] Barocas, S., & Selbst, A. D. (2016). Big data's disparate impact. California Law Review, 104(3), 671-732. https://doi.org/10.15779/Z38BG31

[16] Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K., & Galstyan, A. (2021). A survey on bias and fairness in machine learning. ACM Computing Surveys, 54(6), 1-35. https://doi.org/10.1145/3457607

[17] Buolamwini, J., & Gebru, T. (2018). Gender shades: Intersectional accuracy disparities in commercial gender classification. Proceedings of Machine Learning Research, 81, 77-91. https://proceedings.mlr.press/v81/buolamwini18a.html

[18] Obermeyer, Z., Powers, B., Vogeli, C., & Mullainathan, S. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. Science, 366(6464), 447-453. https://doi.org/10.1126/science.aax2342

[19] Selbst, A. D., Boyd, D., Friedler, S. A., Venkatasubramanian, S., & Vertesi, J. (2019). Fairness and abstraction in sociotechnical systems. Proceedings of the Conference on Fairness, Accountability, and Transparency, 59-68. https://doi.org/10.1145/3287560.3287598

[20] Veale, M., & Binns, R. (2017). Fairer machine learning in the real world: Mitigating discrimination without collecting sensitive data. Big Data & Society, 4(2), 1-17. https://doi.org/10.1177/2053951717743530

[21] Diakopoulos, N. (2016). Accountability in algorithmic decision making. Communications of the ACM, 59(2), 56-62. https://doi.org/10.1145/2844110

[22] Raji, I. D., Smart, A., White, R. N., Mitchell, M., Gebru, T., Hutchinson, B., Smith-Loud, J., Theron, D., & Barnes, P. (2020). Closing the AI accountability gap: Defining an end-to-end framework for internal algorithmic auditing. Proceedings of the Conference on Fairness, Accountability, and Transparency, 33-44. https://doi.org/10.1145/3351095.3372873

[23] Kroll, J. A., Huey, J., Barocas, S., Felten, E. W., Reidenberg, J. R., Robinson, D. G., & Yu, H. (2017). Accountable algorithms. University of Pennsylvania Law Review, 165(3), 633-705. https://scholarship.law.upenn.edu/penn_law_review/vol165/iss3/3

[24] Novelli, C., Taddeo, M., & Floridi, L. (2024). Accountability in artificial intelligence: What it is and how it works. AI & Society, 39(4), 1871-1882. https://doi.org/10.1007/s00146-023-01635-y

[25] Cobbe, J., Lee, M. S. A., & Singh, J. (2021). Reviewable automated decision-making: A framework for accountable algorithmic systems. Proceedings of the ACM Conference on Fairness, Accountability, and Transparency, 598-609. https://doi.org/10.1145/3442188.3445921

[26] Nissenbaum, H. (2004). Privacy as contextual integrity. Washington Law Review, 79(1), 119-157. https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10

[27] Voigt, P., & Von dem Bussche, A. (2017). The EU General Data Protection Regulation (GDPR): A practical guide. Springer. https://doi.org/10.1007/978-3-319-57959-7

[28] Shneiderman, B. (2020). Human-centered artificial intelligence: Reliable, safe and trustworthy. International Journal of Human-Computer Interaction, 36(6), 495-504. https://doi.org/10.1080/10447318.2020.1741118

[29] Amershi, S., Weld, D., Vorvoreanu, M., Fourney, A., Nushi, B., Collisson, P., Suh, J., Iqbal, S., Bennett, P. N., Inkpen, K., Teevan, J., Kikin-Gil, R., & Horvitz, E. (2019). Guidelines for human-AI interaction. Proceedings of the CHI Conference on Human Factors in Computing Systems, 1-13. https://doi.org/10.1145/3290605.3300233

[30] Cath, C. (2018). Governing artificial intelligence: Ethical, legal and technical opportunities and challenges. Philosophical Transactions of the Royal Society A, 376(2133), 20180080. https://doi.org/10.1098/rsta.2018.0080

[31] Wachter, S., & Mittelstadt, B. (2019). A right to reasonable inferences: Re-thinking data protection law in the age of big data and AI. Columbia Business Law Review, 2019(2), 494-620. https://doi.org/10.7916/cblr.v2019i2.3424

[32] Rahwan, I. (2018). Society-in-the-loop: Programming the algorithmic social contract. Ethics and Information Technology, 20(1), 5-14. https://doi.org/10.1007/s10676-017-9430-8

[33] Winfield, A. F. T., & Jirotka, M. (2018). Ethical governance is essential to building trust in robotics and artificial intelligence systems. Philosophical Transactions of the Royal Society A, 376(2133), 20180085. https://doi.org/10.1098/rsta.2018.0085

[34] Sloane, M., Moss, E., Awomolo, O., & Forlano, L. (2022). Participation is not a design fix for machine learning. Proceedings of the Conference on Equity and Access in Algorithms, Mechanisms, and Optimization, 1-6. https://doi.org/10.1145/3551624.3555285

[35] European Commission, High-Level Expert Group on Artificial Intelligence. (2019). Ethics guidelines for trustworthy AI. Publications Office of the European Union. https://doi.org/10.2759/346720

[36] National Institute of Standards and Technology. (2023). Artificial intelligence risk management framework (AI RMF 1.0). U.S. Department of Commerce. https://doi.org/10.6028/NIST.AI.100-1

[37] Organisation for Economic Co-operation and Development. (2019). Recommendation of the Council on artificial intelligence (OECD/LEGAL/0449). OECD. https://legalinstruments.oecd.org/en/instruments/OECD-LEGAL-0449

[38] United Nations Educational, Scientific and Cultural Organization. (2021). Recommendation on the ethics of artificial intelligence. UNESCO. https://unesdoc.unesco.org/ark:/48223/pf0000381137

[39] European Parliament & Council of the European Union. (2024). Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). Official Journal of the European Union. https://eur-lex.europa.eu/eli/reg/2024/1689/oj

[40] Fjeld, J., Achten, N., Hilligoss, H., Nagy, A., & Srikumar, M. (2020). Principled artificial intelligence: Mapping consensus in ethical and rights-based approaches to principles for AI. Berkman Klein Center Research Publication No. 2020-1. https://doi.org/10.2139/ssrn.3518482

[41] Taddeo, M., & Floridi, L. (2018). How AI can be a force for good. Science, 361(6404), 751-752. https://doi.org/10.1126/science.aat5991

[42] Brundage, M., Avin, S., Wang, J., Belfield, H., Krueger, G., Hadfield, G., Khlaaf, H., Yang, J., Toner, H., Fong, R., Maharaj, T., Koh, P. W., Hooker, S., Leung, J., Trask, A., Bluemke, E., Lebensold, J., O'Keefe, C., Koren, M., ... Anderljung, M. (2020). Toward trustworthy AI development: Mechanisms for supporting verifiable claims. arXiv. https://doi.org/10.48550/arXiv.2004.07213

[43] Bryson, J. J. (2020). The artificial intelligence of the ethics of artificial intelligence: An introductory overview for law and regulation. In M. D. Dubber, F. Pasquale, & S. Das (Eds.), The Oxford handbook of ethics of AI (pp. 3-25). Oxford University Press. https://doi.org/10.1093/oxfordhb/9780190067397.013.1

[44] Crawford, K. (2021). Atlas of AI: Power, politics, and the planetary costs of artificial intelligence. Yale University Press. https://doi.org/10.2307/j.ctv1ghv45t

[45] Wachter, S., Mittelstadt, B., & Russell, C. (2018). Counterfactual explanations without opening the black box: Automated decisions and the GDPR. Harvard Journal of Law & Technology, 31(2), 841-887. https://doi.org/10.2139/ssrn.3063289
