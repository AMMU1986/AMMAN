# HUMAN-IN-THE-LOOP AND EXPLAINABLE AI IN MISSION CONTROL SYSTEMS

**Book:** AI for Space Traffic Management and Mission Operations
**Part 3:** Autonomous Decision-Making and Mission Operations
**Chapter 5**

Amman Jakhar¹,* and Sachin Kalsi¹

¹ Department of Mechanical Engineering, Chandigarh University, Mohali, Punjab-140301, India

*Corresponding author: ammanjakhar5000734@gmail.com*

## Abstract

The migration of artificial intelligence into space mission control forces a central tension: preserving human authority while exploiting machine speed for high-stakes decisions. As operations extend toward the Moon and Mars, communication latency makes real-time ground control impractical and compels autonomous onboard reasoning. This chapter examines how human-in-the-loop (HITL) and explainable AI (XAI) frameworks reconcile crew autonomy with meaningful oversight. We synthesise evidence that explanations improve operator trust, situation awareness, and diagnostic accuracy, and that explanation depth matters most under high uncertainty, with contrastive and global explanations proving especially effective. We analyse the trade-off between transparency and cognitive load and present a reference architecture that integrates hierarchical planning, truth maintenance, and case-based reasoning while retaining ultimate human authority. Drawing on the deployment of retrieval-augmented language models aboard the International Space Station, we chart a path toward trustworthy virtual flight controllers for autonomous mission operations.

**Keywords:** human-in-the-loop; explainable AI; mission control systems; space autonomy; human-AI teaming; trust calibration; situation awareness; retrieval-augmented generation

## 5.1. Introduction

The operation of spacecraft has, since the earliest crewed and robotic missions, rested on a tightly coupled partnership between vehicles in flight and large teams of specialists on the ground. In the conventional model of mission control, telemetry streams downlink to Earth, human flight controllers interpret the data against procedures and experience, and commands uplink to the vehicle within seconds to minutes [1]. This ground-centric paradigm has proven extraordinarily reliable for missions in low Earth orbit and for lunar-distance operations, where the round-trip light-time delay remains small enough to sustain interactive supervision. It reflects a philosophy of supervisory control in which human operators retain authority over consequential actions while machines execute well-defined routines under close observation [1].

The paradigm strains, however, as humanity extends its presence deeper into the solar system. Robotic explorers at Mars, and the crewed missions envisioned for the coming decades, operate across distances at which the finite speed of light imposes communication delays of many minutes in each direction [2]. Under such conditions, real-time intervention from Earth is physically impossible; by the time a ground controller perceives an anomaly and formulates a response, the moment for corrective action may have long passed. The traditional assumption that a human expert can always be inserted into the decision loop at the instant of need therefore breaks down, and mission architects are compelled to migrate decision authority onboard, closer to the point of action [3]. Autonomy ceases to be a convenience and becomes a mission-enabling necessity.

### 5.1.1. The Communication-Delay Imperative

The physical driver of onboard autonomy is straightforward to quantify. For a spacecraft at distance *d* from Earth, the one-way light-time is *d / c*, where *c* is the speed of light, and the minimum round-trip latency for a command-and-response exchange is

[EQ] T_rt = 2 d / c    (5.1)

At the mean Earth–Mars distance of roughly 2.25 × 10¹¹ m, equation (5.1) yields a round-trip latency of approximately 25 minutes, and near conjunction the delay can exceed 40 minutes [2]. No human flight controller, however skilled, can stabilise a rapidly evolving fault, manage a time-critical rendezvous, or arbitrate a collision-avoidance manoeuvre across such a gulf. The consequence is a graded reassignment of authority: routine and time-insensitive decisions may remain with the ground, while time-critical decisions must be delegated to onboard systems that can perceive, reason, and act without waiting for terrestrial confirmation [3]. The central design question of this chapter is therefore not whether to automate, but how to automate while preserving the human judgement, accountability, and contextual wisdom that decades of spaceflight have shown to be indispensable [4].

### 5.1.2. Human-in-the-Loop and Explainable AI as a Balanced Solution

Two complementary frameworks structure the response to this challenge. Human-in-the-loop (HITL) design keeps human operators embedded in the decision process at a level of engagement calibrated to the stakes and the available time, ranging from direct approval of every action to high-level supervision of an autonomous agent [4]. Explainable AI (XAI) equips automated systems with the ability to communicate the rationale for their recommendations and actions in terms a human can understand and evaluate [5]. Neither framework is sufficient alone. Autonomy without explanation produces opaque systems that operators cannot calibrate their trust toward, inviting both dangerous over-reliance and wasteful disuse [6]. Explanation without retained human authority reduces the operator to a passive observer, eroding the situation awareness that is essential when the automation reaches the limits of its competence [7].

The synthesis of HITL and XAI offers a balanced path: automation augments crew capability and compensates for communication delay, while explanation preserves the transparency that allows humans to supervise, intervene, and remain accountable. This chapter develops that synthesis for the specific demands of space mission control. Section 5.2 establishes the foundations of graded autonomy and human oversight. Section 5.3 surveys the taxonomy and techniques of explainable AI as they apply to mission operations. Section 5.4 presents a reference architecture that integrates planning, reasoning, and explanation under human authority, and analyses the cognitive-load trade-off that governs its design. Section 5.5 examines deployment evidence, including the operation of retrieval-augmented language models aboard the International Space Station. Section 5.6 addresses evaluation, and Section 5.7 surveys open challenges and future directions before Section 5.8 concludes.


## 5.2. Foundations of Human-in-the-Loop Autonomy in Mission Control

### 5.2.1. From Supervisory Control to Graded Autonomy

The theoretical roots of human-in-the-loop operation lie in supervisory control, the discipline concerned with how a human operator directs and monitors a semi-autonomous machine that carries out lower-level tasks [1]. Supervisory control was developed precisely for settings, such as teleoperated robotics and process control, in which delay, distance, or complexity prevents continuous manual control. Its central insight is that authority can be distributed across a spectrum rather than assigned wholly to human or machine. A well-established framework describes automation along a scale that spans the acquisition of information, its analysis, the selection of a decision, and the implementation of an action, with the degree of automation adjustable independently at each stage [4]. This decomposition is valuable for mission control because it clarifies that a system may, for example, analyse telemetry autonomously yet still defer the final action to a human, or execute a manoeuvre autonomously while presenting its analysis for after-the-fact review.

Contemporary practice frames this spectrum through the lens of human-autonomy teaming, in which the automation is treated less as a tool and more as a team member whose contributions must be coordinated with those of the human [8]. Effective teaming requires shared goals, mutual predictability, and directability, the last denoting the human's ability to redirect the agent as circumstances change [9]. In space operations these properties are decisive: an onboard agent that cannot be understood or redirected by the crew becomes a liability precisely when a mission departs from its nominal envelope. The design objective, then, is adjustable autonomy, in which the level of machine authority can shift dynamically according to context, workload, and confidence, rather than being fixed at design time [9]. Figure 5.1 situates this idea by mapping representative mission destinations onto the round-trip latency of equation (5.1) and the level of onboard autonomy that latency makes necessary.

### 5.2.2. Levels of Autonomy and Human Oversight

The practical calibration of authority is captured by a taxonomy of autonomy levels, each associated with a distinct human role and a distinct risk profile. Table 5.1 summarises a spectrum tailored to mission control, ranging from advisory automation, in which the human decides and the machine only recommends, through human-in-the-loop and human-on-the-loop configurations, to conditionally and fully autonomous operation. The appropriate level is not a global property of a system but a decision that should be made per function and per mission phase, taking into account the round-trip latency of equation (5.1), the reversibility of the action, and the confidence of the automation [4]. A collision-avoidance burn during a communications blackout may demand full autonomy, whereas the commissioning of a new scientific instrument may sensibly remain advisory. As Figure 5.1 illustrates, the feasible region of human-interactive control shrinks as distance grows, so that beyond lunar range the higher autonomy levels of Table 5.1 become obligatory rather than optional.

[Insert Figure 5.1 here]
Figure 5.1. Round-trip communication latency for representative destinations and the corresponding shift from ground-interactive control toward obligatory onboard autonomy

[Insert Table 5.1 here]
Table 5.1. Levels of autonomy and corresponding human oversight in mission control

| Autonomy level | Human role | Machine discretion | Suitable mission context | Dominant risk |
|----------------|-----------|--------------------|--------------------------|---------------|
| Advisory | Human decides; machine recommends | Recommendation only | Instrument commissioning, mission planning | Over-reliance on advice |
| Human-in-the-loop | Human approves each action | Proposes and awaits confirmation | Orbit-change burns, software uploads | Latency bottleneck, alert fatigue |
| Human-on-the-loop | Human monitors, may intervene | Acts autonomously under supervision | Station-keeping, routine housekeeping | Delayed or missed intervention |
| Conditionally autonomous | Human sets goals and bounds | Acts freely within constraints | Proximity operations, science sequencing | Misspecified constraints |
| Fully autonomous | Minimal routine involvement | Complete operational discretion | Collision avoidance during blackout | Unanticipated edge cases |

As Table 5.1 makes explicit, higher autonomy relieves the latency bottleneck but shifts risk toward misspecified goals and unhandled edge cases, whereas lower autonomy preserves human judgement at the cost of throughput and responsiveness. The engineering challenge is to move fluidly along this spectrum, and it is here that explanation becomes indispensable: a human cannot responsibly grant or revoke authority to a system whose reasoning is opaque [5, 6]. The levels in Table 5.1 are therefore best understood not as static settings but as operating points between which a well-designed HITL-XAI system transitions under human direction.

### 5.2.3. Trust, Over-Reliance, and Situation Awareness

Two human-factors phenomena determine whether graded autonomy succeeds or fails in practice. The first is the calibration of trust. Trust in automation is the attitude that an agent will help achieve an operator's goals in situations of uncertainty, and appropriate reliance occurs only when that trust is matched to the automation's true reliability [6]. Miscalibration is dangerous in both directions: excessive trust produces automation bias, in which operators accept erroneous machine outputs and fail to monitor for failure, while insufficient trust produces disuse, in which valuable automation is ignored and its benefits forfeited [10]. Empirical studies of automated systems consistently show that operators anchor their reliance on perceived reliability, and that unexplained errors sharply and durably degrade trust even when overall performance is high [6, 10].

The second phenomenon is situation awareness, defined as the perception of elements in the environment, the comprehension of their meaning, and the projection of their future status [7]. Automation can paradoxically erode situation awareness: when a machine handles a task silently, the human is removed from the loop of active engagement and loses the up-to-date mental model needed to take over competently when the automation fails, a difficulty known as the out-of-the-loop performance problem [7]. In mission control, where takeover may be required precisely at the moment of an unforeseen anomaly, preserving situation awareness is a safety-critical requirement rather than a mere convenience. Explanation is the principal mechanism by which an autonomous system can keep its human partner informed, calibrated, and ready, motivating the detailed treatment of explainable AI that follows.


### 5.2.4. Mental Models and the Dynamics of Trust Repair

Trust is not a static quantity that a system earns once and retains; it evolves dynamically as the operator accumulates experience with the automation, and it is mediated by the operator's mental model of how the system works [6]. A mental model is the operator's internal representation of the automation's function, capabilities, and limits, and the accuracy of that model determines whether reliance is well placed. When the model is accurate, the operator anticipates where the automation will excel and where it will struggle, and adjusts reliance accordingly; when the model is impoverished or mistaken, reliance decouples from reliability and the risks of automation bias and disuse re-emerge [10]. Explanation shapes the mental model directly, and the combination of a global account of the agent's overall competence with a local account of the specific decision is effective precisely because it develops both the general and the situational components of that model [6, 7].

The temporal dynamics of trust are equally important. Empirical work shows that trust is asymmetric: it accrues slowly through repeated successful interactions but collapses rapidly following a salient failure, and it recovers only gradually thereafter [6]. This asymmetry has a direct design consequence for mission control, where a single unexplained error can undermine an operator's willingness to rely on an otherwise valuable agent for the remainder of a mission. Systems that explain their failures, acknowledging the conditions under which a recommendation proved wrong and how the system has updated, support trust repair far more effectively than systems that fail silently and offer no account [6, 10]. The truth-maintenance mechanism introduced in Section 5.4.2 provides a natural substrate for such explanations, because it records the evidential basis for each conclusion and can therefore reconstruct why a superseded belief was once held. Designing for trust repair, rather than merely for initial trust formation, is thus a defining requirement of long-duration missions in which the human-agent relationship must endure across months or years of operation [3].

## 5.3. Explainable AI Foundations for Space Operations

### 5.3.1. What Explanation Means in a Mission-Control Context

Explainable AI encompasses the methods and design principles by which an automated system renders its behaviour intelligible to the humans who must supervise, trust, or contest it [5]. The field distinguishes interpretability, the degree to which a human can consistently predict a model's result, from explanation, the act of communicating the reasons behind a specific decision in human-comprehensible terms [11]. A rigorous treatment stresses that explanation is not an intrinsic property of an algorithm but a relation between the system, the recipient, and the task; an explanation that satisfies a machine-learning engineer during development may be useless to a flight controller diagnosing a fault under time pressure [12]. This audience-relative character is especially consequential in mission control, where the recipients of explanation are highly trained but time-constrained operators whose need is not mathematical completeness but actionable understanding.

Research drawing on the social sciences has shown that human explanation is contrastive, selective, and social: people rarely ask why an event occurred in absolute terms, but rather why it occurred rather than some expected alternative, and they prefer a few relevant causes over an exhaustive causal chain [13]. These findings carry direct design implications. An effective mission-control explanation should answer the operator's implicit contrastive question, such as why the agent recommends venting a tank rather than isolating it, and should present the small number of decisive factors rather than the entire feature space. Figure 5.2 organises the principal dimensions of explanation, distinguishing scope, timing, and form, and situates the major algorithmic techniques within that structure.

[Insert Figure 5.2 here]
Figure 5.2. Taxonomy of explainable AI approaches organised by scope (local versus global), timing (ante-hoc versus post-hoc), and form (attribution, contrastive, and example-based), with representative techniques

### 5.3.2. Techniques and Their Explanation Types

As Figure 5.2 indicates, explanation techniques differ along several orthogonal axes that determine their suitability for a given mission-control function. Along the scope axis, local methods explain a single decision while global methods characterise the model's overall behaviour. Along the timing axis, ante-hoc or intrinsic interpretability builds transparency into the model structure itself, whereas post-hoc methods generate explanations for an already-trained, possibly opaque model. Along the form axis, attribution methods quantify how much each input contributes to an output, contrastive and counterfactual methods identify the minimal change that would alter the decision, and example-based methods justify a decision by reference to similar prior cases.

Several techniques have become standard. Local surrogate methods approximate a complex model near a specific input with a simple, interpretable model to expose which features drove that particular prediction [14]. Additive feature-attribution methods grounded in cooperative game theory assign each feature a principled contribution to the prediction, unifying several earlier approaches under a single theoretical account [15]. For perceptual models that process imagery, gradient-based saliency techniques highlight the regions of an input image most responsible for a classification, an approach directly applicable to onboard vision systems for docking or hazard detection [16]. Counterfactual explanations describe the smallest alteration to the inputs that would yield a different, typically more desirable, outcome, and are naturally contrastive and actionable [17]. Table 5.2 maps these techniques to their explanation types and to representative mission-control applications, and indicates the operator question each is best suited to answer.

[Insert Table 5.2 here]
Table 5.2. Taxonomy of explanation types, representative techniques, and mission-control applications

| Explanation type | Scope / timing | Representative technique | Operator question answered | Mission-control application |
|------------------|----------------|--------------------------|----------------------------|-----------------------------|
| Feature attribution | Local, post-hoc | Local surrogate models [14] | Which signals drove this call? | Telemetry anomaly ranking |
| Additive attribution | Local/global, post-hoc | Shapley-value attribution [15] | How much did each factor matter? | Fault-diagnosis support |
| Saliency mapping | Local, post-hoc | Gradient-based saliency [16] | Where in the image did it look? | Vision-based hazard detection |
| Counterfactual | Local, post-hoc | Minimal-change counterfactuals [17] | What would change the decision? | Manoeuvre and abort planning |
| Example-based | Local, ante-hoc | Case-based reasoning | Which past case is this like? | Procedure and precedent recall |
| Global rules | Global, ante-hoc | Interpretable rule models | How does it behave in general? | Certification and pre-flight review |

Table 5.2 underscores that no single technique suffices for the breadth of mission-control decisions; a practical system layers several, selecting the form of explanation to match both the underlying model and the operator's momentary question [11, 13]. The example-based and global-rule rows of Table 5.2 foreshadow the architectural components of Section 5.4, in which case-based reasoning and rule-governed planning supply intrinsically interpretable behaviour rather than post-hoc rationalisation.

### 5.3.3. Empirical Evidence from Spaceflight-Relevant Human-Autonomy Teaming

The value of explanation in space operations is not merely theoretical. Studies of spaceflight-relevant human-autonomy teaming demonstrate that AI agents which provide explanations for their recommendations significantly improve operator performance, trust, situation awareness, and diagnostic accuracy relative to opaque systems that issue recommendations without justification [18]. In these studies, operators paired with an explaining agent detected and correctly diagnosed simulated system faults more accurately and calibrated their reliance more appropriately, accepting correct advice and rejecting incorrect advice more reliably than operators paired with a silent agent [18]. This body of evidence directly supports the central claim of this chapter: that explanation is the mechanism through which autonomy and human oversight are reconciled.

Crucially, the depth of explanation interacts with task uncertainty. Advanced explanations that supply detailed justifications are particularly effective under high-uncertainty conditions, where they mitigate the performance degradation that otherwise accompanies time-critical anomaly diagnosis; under low uncertainty, by contrast, the marginal benefit of deep explanation is smaller and may not justify its cost in attention [19]. This finding motivates explanation depth that adapts to context rather than a fixed verbosity. Complementary work shows that the type of explanation significantly affects manual performance, team outcomes, workload, and trust calibration, and that a combination of contrastive and global explanations emerges as the most effective for both user preference and objective performance [20]. Together these results, summarised again in the analysis of Table 5.2, establish that explanation must be designed along the dimensions of type and depth, not merely switched on or off.


### 5.3.4. Evaluating the Quality of Explanations

Providing explanations is necessary but not sufficient; the explanations must be good, and goodness must be defined and measured rather than assumed. The literature distinguishes three broad levels at which explanation quality is assessed [12]. Functionally grounded evaluation uses proxy measures computed without human involvement, such as the fidelity of an explanation to the underlying model or its sparsity, and is inexpensive but only weakly predictive of operational value. Human-grounded evaluation places lay or proxy users in simplified tasks to compare explanation forms, offering a middle ground of realism and cost. Application-grounded evaluation embeds domain experts, in this case flight controllers or astronauts, in realistic tasks and measures the outcomes that ultimately matter: decision accuracy, trust calibration, workload, and situation awareness [12, 18]. For mission control, application-grounded evaluation is the gold standard, because an explanation that scores well on a proxy metric may nonetheless mislead an operator under the time pressure and stress of a genuine anomaly.

Two properties deserve particular scrutiny. Fidelity denotes the degree to which an explanation faithfully reflects the actual reasoning of the system; a plausible but unfaithful explanation is worse than none, because it induces confident but mistaken mental models and thereby corrupts trust calibration [11, 13]. Stability denotes the degree to which similar inputs yield similar explanations; an explanation method that produces wildly different rationales for near-identical telemetry undermines the operator's ability to form durable expectations. Post-hoc attribution methods such as those in Table 5.2 can suffer from both low fidelity and low stability, which is a further argument for the intrinsically interpretable, high-fidelity mechanisms of Section 5.4.2, whose explanations are the reasoning rather than a reconstruction of it [11, 13]. The maturing science of explanation evaluation, together with responsible-AI frameworks that codify transparency requirements, provides mission-control designers with the criteria needed to certify that an explanation facility genuinely serves its human recipients rather than merely appearing to [5].

## 5.4. Architecting Human-in-the-Loop, Explainable Mission Control Systems

### 5.4.1. A Reference Architecture

Translating the principles of Sections 5.2 and 5.3 into an operational system requires an architecture that couples perception, reasoning, and action with an explanation layer and a human-authority interface. Figure 5.3 presents such a reference architecture. Telemetry and sensor data enter a perception and state-estimation module that produces a filtered picture of vehicle and environment state. A reasoning and decision core, which may combine model-based planners with learned components, generates candidate actions together with the intermediate rationale that produced them. Rather than passing actions directly to the actuators, the architecture routes them through an explanation generator that constructs contrastive, attribution, and example-based accounts calibrated to the operator's role and available time, following the taxonomy of Figure 5.2.

[Insert Figure 5.3 here]
Figure 5.3. Reference architecture for a human-in-the-loop, explainable mission-control system, showing the flow from perception through reasoning to an explanation layer and an adjustable human-authority gate that governs actuation

The distinguishing feature of the architecture in Figure 5.3 is the adjustable authority gate, which implements the autonomy levels of Table 5.1 as a run-time control rather than a design-time constant. Under advisory or human-in-the-loop settings the gate withholds actuation pending operator approval; under human-on-the-loop settings it acts while streaming explanations for monitoring; under full autonomy, invoked when latency or urgency demands, it acts immediately and logs a complete, replayable rationale for subsequent human review. This design operationalises the principle that transparency and authority must scale together: whatever level of autonomy is selected, the human retains access to an explanation commensurate with their ability to intervene [5, 6]. The transparency of the interface itself can be structured according to the situation-awareness-based agent transparency model, which specifies that an agent should convey its current action and plan, its reasoning and constraints, and its projections of outcomes and uncertainty [21].

Empirical evaluations of agent transparency confirm that conveying these levels of information improves operator decision quality and trust calibration without necessarily increasing response time, provided the information is presented in an integrated rather than fragmented form [22]. Figure 5.3 therefore places the explanation generator on the critical path between reasoning and action, ensuring that transparency is a structural property of the system rather than an afterthought bolted on for certification.

### 5.4.2. Integrated Reasoning for Predictable, Explainable Behaviour

Post-hoc explanation of an opaque model is valuable but limited; a more robust route to trustworthy autonomy combines learned components with symbolic reasoning that is interpretable by construction. Three classical mechanisms, integrated within the reasoning core of Figure 5.3, are particularly well suited to mission control. Hierarchical planning decomposes high-level goals into ordered subtasks and primitive actions, producing a plan whose structure is itself an explanation of intent and whose steps can be inspected, justified, and interrupted [23]. Because the decomposition follows human-authored methods and constraints, the resulting behaviour is predictable and auditable in a way that end-to-end learned policies are not.

A truth-maintenance capability records the justifications behind each belief and decision, maintaining a dependency network that links conclusions to the assumptions and evidence that support them [24]. When new telemetry contradicts a prior assumption, the system can identify precisely which conclusions must be retracted and can present the operator with a traceable account of how its assessment changed, a property essential for diagnosing evolving faults. Case-based reasoning complements these mechanisms by solving new problems through the retrieval and adaptation of solutions to similar past situations, yielding behaviour that is both predictable and intrinsically explainable, since every recommendation is grounded in an identifiable precedent that the operator can examine [25]. This example-based mode corresponds directly to the example-based row of Table 5.2. The integration of hierarchical planning, truth maintenance, and case-based reasoning within a single architecture reflects a lineage of autonomous mission systems that keep ultimate authority in human hands while providing sophisticated automated support [26]. Table 5.3 compares these mechanisms across the properties that matter for mission-control deployment.

[Insert Table 5.3 here]
Table 5.3. Comparison of integrated reasoning mechanisms for explainable mission autonomy

| Mechanism | Basis of behaviour | Intrinsic explainability | Traceability | Primary contribution |
|-----------|--------------------|--------------------------|--------------|----------------------|
| Hierarchical planning | Goal decomposition into methods and tasks | High: plan structure reveals intent | Full plan-to-goal trace | Predictable, auditable action sequences |
| Truth maintenance | Dependency network over beliefs | High: justifications are explicit | Belief-to-evidence trace | Consistent revision under new data |
| Case-based reasoning | Retrieval and adaptation of precedents | High: grounded in prior cases | Case-to-decision trace | Predictable, precedent-based recommendations |
| Learned policy (RL) | Reward-driven optimisation | Low: requires post-hoc methods | Limited without instrumentation | Adaptation to novel conditions |
| Neuro-symbolic hybrid | Learned perception plus symbolic reasoning | Moderate to high | Partial, layer-dependent | Balances adaptivity and transparency |

As Table 5.3 shows, the symbolic mechanisms offer high intrinsic explainability and traceability but limited adaptivity, whereas learned policies offer the reverse; the neuro-symbolic hybrid in the final row seeks a deliberate balance and represents the direction of much current research [26]. A mission-control architecture need not choose exclusively among these mechanisms, but can assign each to the functions for which its properties are best matched, using the symbolic components where auditability is paramount and learned components where adaptation to unforeseen conditions is essential.

### 5.4.3. The Transparency–Cognitive-Load Trade-off

The design of explanation cannot proceed as if more transparency were always better. While explanations build trust and understanding, overly complex or lengthy explanations risk information overload, increasing an operator's mental workload without a proportional gain in decision quality [27]. Mental workload can be characterised along demand dimensions such as mental, temporal, and effort load, and is routinely assessed in aerospace human-factors work using multidimensional subjective instruments [28]. The practical objective is therefore to maximise understanding per unit of cognitive cost rather than to maximise information transmitted.

A simple model clarifies the trade-off. Let the operator's net decision value *V* be modelled as the understanding *U* gained from an explanation minus a cost proportional to the imposed cognitive load *L*:

[EQ] V = U(e) − λ · L(e)    (5.2)

where *e* denotes the explanation, *λ* weights the cost of load relative to understanding, and both *U* and *L* increase with explanation depth but with diminishing and accelerating returns respectively. Understanding tends to saturate as depth grows, whereas load rises increasingly steeply once working-memory limits are approached, so the value in equation (5.2) is maximised at an intermediate depth rather than at maximal verbosity [27, 28]. Differentiating equation (5.2) and setting the result to zero gives the optimality condition

[EQ] dU/de = λ · dL/de    (5.3)

which states that explanation should be deepened only until the marginal understanding it yields equals the marginally weighted cognitive cost it imposes. Because the uncertainty of the task shifts the understanding curve, as established in Section 5.3.3, the optimal depth is higher under high uncertainty and lower under routine conditions, providing a principled basis for the adaptive, context-sensitive explanation that empirical studies recommend [19, 20].

Trust calibration can be expressed in the same spirit. If *r* denotes the operator's reliance on the agent and *ρ* the agent's true reliability, appropriate reliance is achieved when the calibration gap is minimised:

[EQ] minimise | r − ρ |    (5.4)

Explanation acts on equation (5.4) by supplying the operator with the evidence needed to align *r* with *ρ*, reducing both the over-reliance that produces automation bias and the disuse that forfeits automation's benefits [6, 10]. Figure 5.4 depicts these relationships graphically, showing the inverted-U value curve of equation (5.2) alongside a trust-calibration curve, and marking the region of appropriate reliance that a well-designed explanation regime is intended to reach.

[Insert Figure 5.4 here]
Figure 5.4. The transparency–cognitive-load trade-off: net decision value as a function of explanation depth (left) and the trust-calibration relationship between reliance and reliability (right), with the region of appropriate reliance highlighted

As Figure 5.4 makes clear, both insufficient and excessive explanation are suboptimal, and the design target is the intermediate regime in which understanding is high, cognitive load is tolerable, and reliance tracks reliability. This trade-off recurs throughout the evaluation discussion of Section 5.6, where the metrics used to locate a system's operating point on the curves of Figure 5.4 are examined in detail.


### 5.4.4. Communicating Uncertainty and the Boundaries of Competence

A recurring theme of this chapter is that the most consequential moments in mission control arise when the automation approaches the edge of its competence. A system that conveys its own uncertainty transforms these moments from silent failures into opportunities for calibrated human intervention. Well-founded uncertainty estimates allow the authority gate of Figure 5.3 to escalate autonomously: when confidence falls below a threshold appropriate to the reversibility and stakes of the action, the system can downgrade its autonomy level along the spectrum of Table 5.1, soliciting human approval that it would otherwise not require [4, 21]. Communicating uncertainty is itself a form of transparency, and the situation-awareness-based transparency model explicitly includes the projection of outcomes and their associated confidence as a distinct level of information the agent should convey [21, 22].

The design of uncertainty communication must again respect the cognitive-load trade-off of equations (5.2) and (5.3). Presenting a full probability distribution over outcomes may be appropriate for a mission planner deliberating over hours, but a controller managing a fast-evolving fault needs a compact, unambiguous signal of whether the recommendation can be trusted now. Graded verbal categories, calibrated confidence bars, and explicit flags for out-of-distribution inputs are lightweight devices that convey the essential information without overwhelming the operator, and their selection should follow the same adaptive logic that governs explanation depth [19, 27]. Equally important is honesty about the limits of the model: an agent should signal when a situation lies outside the envelope of its training or its case base, since it is precisely in such novel circumstances that human experiential judgement is most valuable and machine confidence least warranted [10, 25]. A mission-control agent that reliably says "I am uncertain here" earns a form of trust that no volume of confident correct answers can substitute for, because it enables the appropriate reliance formalised by equation (5.4).

## 5.5. Deployment Evidence and Case Studies

### 5.5.1. Retrieval-Augmented Language Models Aboard the International Space Station

A milestone in the practical realisation of onboard AI assistance is the operation of large language model systems in the austere, intermittently connected environment of the International Space Station. Large language models acquire broad reasoning and language capabilities from training on extensive corpora and can be directed to novel tasks without task-specific retraining [29]. Their principal weakness for operational use is a tendency to generate fluent but unfounded content, which is unacceptable in a safety-critical domain. Retrieval-augmented generation addresses this weakness by grounding the model's output in an authoritative external knowledge base, retrieving relevant procedures, telemetry definitions, and documentation at query time and constraining the response to that evidence [30]. This grounding is simultaneously a mechanism of explanation, since the retrieved passages that justify an answer can be surfaced to the operator as citations, aligning the system with the attribution and example-based explanation types of Table 5.2.

The successful deployment of an LLM-based retrieval-augmented system aboard the International Space Station demonstrates the feasibility of disconnected AI operation in an austere environment, where reliance on a ground-based service is precluded by bandwidth, latency, or link availability [31]. Operating on local compute with a curated onboard knowledge base, such a system can answer crew questions about procedures and systems without a round trip to Earth, directly addressing the latency constraint of equation (5.1). This achievement marks a concrete step toward autonomous virtual flight controllers, software agents that emulate key Mission Control functions such as procedure guidance, anomaly triage, and consumables monitoring while keeping the crew and, when reachable, the ground in supervisory authority [32]. Mapped onto the reference architecture of Figure 5.3, the retrieval component populates the perception-and-knowledge layer, the language model serves as a reasoning core, and the surfaced citations constitute the explanation layer, with crew approval implementing the authority gate.

### 5.5.2. Onboard Anomaly Diagnosis and Collision Avoidance

Two further classes of mission function illustrate the HITL-XAI approach under time pressure. The first is onboard anomaly diagnosis. Traditional fault detection, isolation, and recovery relies on predefined monitors and response scripts that are effective for anticipated faults but brittle in the face of novel ones [33]. An explainable diagnostic agent augments this foundation by ranking candidate fault hypotheses, attributing each to the telemetry signatures that support it, and presenting the operator with a contrastive account of why one hypothesis is favoured over its nearest competitor. The empirical findings of Section 5.3.3 are decisive here: because anomaly diagnosis is precisely the high-uncertainty, time-critical setting in which advanced explanations most improve performance, the diagnostic function warrants the deeper end of the adaptive explanation range identified by equation (5.3) [19]. The truth-maintenance mechanism of Section 5.4.2 allows the agent to revise its ranking coherently as the fault evolves, and to show the operator exactly which evidence prompted the revision [24].

The second class is autonomous collision avoidance within the broader problem of space traffic management. As the population of orbital objects grows, conjunction assessment and avoidance increasingly exceed the timescales of ground-interactive decision-making, motivating onboard autonomy for manoeuvre selection [34]. Here the authority gate of Figure 5.3 is essential: a conjunction with ample lead time can be handled in a human-in-the-loop mode, with the agent proposing a manoeuvre and explaining its predicted miss distance and propellant cost, whereas a late-detected, high-probability conjunction during a communications gap may require the fully autonomous setting of Table 5.1, with a complete rationale logged for post-event review. In both cases the explanation is not decorative but functional, enabling the human either to approve with understanding or to reconstruct and audit an autonomous decision after the fact [5, 22]. These case studies collectively show that the architecture of Figure 5.3 is not merely conceptual but reflects capabilities now entering operational use.


### 5.5.3. Crew-Facing Procedure Execution and Consumables Management

A third and increasingly important class of function is the direct support of crew activity during periods of autonomy from the ground. On long-duration missions the crew must execute complex procedures, manage consumables such as power, water, and atmosphere, and schedule their own activities without the dense ground support that characterises low-Earth-orbit operations [3]. A crew-facing agent built on the retrieval-augmented architecture of Section 5.5.1 can guide procedure execution step by step, surface the authoritative source for each instruction, and flag deviations between expected and observed system responses, thereby coupling guidance with explanation in a single interaction [30, 32]. Because every instruction is grounded in a retrieved, citable source, the crew can verify the agent's guidance against the underlying documentation, an explanation mechanism that aligns with the attribution and example-based forms of Table 5.2 and that is essential when no ground expert is available to arbitrate.

Consumables management illustrates the interplay of the architecture's components under crew authority. A planning agent projects consumable trajectories, a diagnostic component attributes anomalous consumption to candidate causes, and the explanation layer presents the crew with a contrastive account of competing hypotheses together with calibrated confidence, following the uncertainty-communication principles of Section 5.4.4 [19, 21]. The authority gate of Figure 5.3 keeps the crew in control of consequential actions, such as reconfiguring a life-support loop, while permitting the agent to handle routine monitoring autonomously in an on-the-loop mode. This division mirrors the levels of Table 5.1 and demonstrates that the same architecture serves both vehicle-facing functions, such as collision avoidance, and crew-facing functions, such as procedure support, differing only in the placement of the authority gate and the recipient of the explanation. The convergence of these functions within a common framework is what makes the notion of a virtual flight controller coherent rather than merely aspirational [31, 32].

## 5.6. Evaluating Human-in-the-Loop, Explainable Systems

### 5.6.1. Dimensions and Metrics of Evaluation

Because the purpose of a HITL-XAI system is to improve joint human-machine performance, its evaluation must extend beyond the accuracy of the automation in isolation to encompass the outcomes of the human-autonomy team as a whole. Four dimensions are central. Task performance measures the quality and timeliness of decisions, such as diagnostic accuracy and manoeuvre effectiveness. Trust calibration measures how closely operator reliance tracks true reliability, operationalising the objective of equation (5.4); validated trust scales and behavioural reliance measures are both used, and meta-analytic work has identified the human, automation, and situational factors that shape trust and must therefore be controlled in any evaluation [35]. Cognitive workload measures the mental cost of collaborating with the system, assessed through multidimensional subjective instruments and, increasingly, physiological indicators [28]. Situation awareness measures whether the operator retains the perception, comprehension, and projection needed to intervene competently [7].

Table 5.4 consolidates these dimensions, their representative metrics, and the empirical findings from spaceflight-relevant studies that anchor the design guidance of this chapter. The entries reflect the consistent result that explanation improves performance, trust, and situation awareness, that explanation depth should scale with uncertainty, and that contrastive and global explanations are jointly the most effective form [18, 19, 20]. Locating a system on the value and calibration curves of Figure 5.4 requires measuring all four dimensions together, since an intervention that raises understanding while inflating workload may move the operating point in an undesirable direction.

[Insert Table 5.4 here]
Table 5.4. Evaluation dimensions, metrics, and empirical findings for human-in-the-loop, explainable mission-control systems

| Dimension | Representative metric | Key empirical finding | Design implication |
|-----------|-----------------------|-----------------------|--------------------|
| Task performance | Diagnostic accuracy, decision latency | Explanations raise accuracy versus opaque agents [18] | Route explanation on the critical path |
| Trust calibration | Reliance-reliability gap, trust scales | Unexplained errors durably reduce trust [6, 35] | Explain failures, not only successes |
| Cognitive workload | Subjective load, effort indicators | Excess explanation inflates workload [27, 28] | Adapt depth to context per equation (5.3) |
| Situation awareness | Perception-comprehension-projection probes | Silent automation degrades awareness [7] | Stream transparency in on-the-loop modes |
| Explanation form | User preference, performance by type | Contrastive plus global most effective [20] | Combine contrastive and global forms |

### 5.6.2. From Evaluation to Design Guidance

The findings compiled in Table 5.4 translate into concrete design guidance. First, explanation should be placed on the critical path between reasoning and action, as in Figure 5.3, so that it is available whenever authority is exercised. Second, because unexplained failures are especially corrosive to trust, systems should explain their errors and low-confidence states as carefully as their successes, supporting the calibration objective of equation (5.4) [6, 35]. Third, explanation depth should adapt to task uncertainty in accordance with equation (5.3), deepening for time-critical anomaly diagnosis and remaining concise for routine operation [19]. Fourth, the default explanatory form should combine a contrastive account of the specific decision with a global characterisation of the agent's behaviour, the combination that studies identify as most effective for both preference and performance [20]. Established guidelines for human-AI interaction reinforce these points, recommending that systems make clear what they can do and how well, provide relevant explanations, and support efficient correction and control [36]. Applied together, this guidance positions a system within the region of appropriate reliance highlighted in Figure 5.4.


## 5.7. Challenges and Future Directions

### 5.7.1. Verification, Assurance, and Trust in Learning Systems

The deployment of autonomous, learning-based agents in safety-critical mission control raises assurance challenges that current verification practice only partially addresses. Traditional flight software is certified against exhaustive requirements and tested to high coverage, but learned components resist such treatment because their behaviour is defined by data and optimisation rather than by explicit specification [37]. Verifying that an onboard agent will behave acceptably across the vast space of possible situations, including the edge cases that Table 5.1 identifies as the dominant risk of high autonomy, remains an open problem. Explainability contributes to assurance by making behaviour inspectable, and the intrinsically interpretable mechanisms of Table 5.3 are more amenable to certification than opaque policies, which is a strong argument for the neuro-symbolic hybrids discussed in Section 5.4.2 [37, 38]. Calibrated uncertainty estimation is a further prerequisite: an agent that reliably reports when it is operating outside its competence enables the authority gate of Figure 5.3 to escalate to human oversight before a failure occurs.

### 5.7.2. Adaptive Autonomy and Advancing Reasoning

Future systems will need to move more fluidly along the autonomy spectrum of Figure 5.1, adjusting their level of authority in real time as latency, workload, and confidence change. Reinforcement learning offers a route to agents that improve their decision policies through experience, but its characteristic opacity must be counterbalanced by the explanation and verification measures emphasised throughout this chapter [39]. Advances in reasoning that combine the adaptivity of learned models with the transparency of symbolic structures are especially promising for mission control, because they align the twin demands of competence and accountability [38]. As virtual flight controllers mature from procedure assistants toward agents that plan and act, the integrated reasoning of Section 5.4.2 and the adaptive explanation of Section 5.4.3 will need to operate in concert, deepening explanation exactly when uncertainty rises, as prescribed by equation (5.3).

### 5.7.3. Governance, Accountability, and Human Authority

Autonomy does not dissolve human responsibility; it redistributes it. When an onboard agent acts during a communications blackout, accountability rests with the humans who designed, certified, and authorised it, which makes the replayable rationale of Figure 5.3 a governance instrument as much as an engineering one [40]. Clear allocation of authority, auditable decision logs, and explicit boundaries on autonomous action are necessary to preserve meaningful human control as capability grows [41]. These considerations become more acute for missions beyond low Earth orbit, where the latency of equation (5.1) forces greater delegation: cislunar infrastructure and lunar surface operations will demand agents that act autonomously yet remain accountable to a distant human authority [42], and crewed Mars operations will push this further still, requiring the crew themselves to supervise onboard autonomy without recourse to timely ground support [43]. The maturing body of work on responsible and explainable AI provides taxonomies and principles that mission-control designers can adopt to keep these systems transparent, accountable, and aligned with human intent [44]. The trajectory is clear: as Figure 5.1 anticipates, deeper missions require greater autonomy, and only a disciplined union of human-in-the-loop authority and explainable AI can make that autonomy trustworthy [45].

### 5.7.4. Data, Robustness, and Distribution Shift

A challenge that cuts across all of the preceding is the dependence of learned components on data that can never fully represent the environments a deep-space mission will encounter. Models trained on historical telemetry and simulated scenarios inevitably confront distribution shift, in which operational conditions diverge from the training distribution, degrading both accuracy and the reliability of confidence estimates [37]. In terrestrial applications distribution shift can often be corrected by retraining on fresh data, but a spacecraft en route to Mars cannot readily acquire labelled examples of the novel faults it may face, and the latency of equation (5.1) precludes rapid ground-side model updates. This scarcity elevates the importance of the intrinsically interpretable and case-based mechanisms of Section 5.4.2, which degrade more gracefully and transparently than opaque learned policies, and of the uncertainty communication of Section 5.4.4, which allows a model to recognise and declare when it has left familiar territory [25, 37].

Robustness to adversarial and simply anomalous inputs is a related concern. Perception systems that inform docking, landing, or hazard avoidance can be misled by sensor degradation, unusual illumination, or configurations absent from their training data, and the saliency explanations of Table 5.2 provide one means of detecting such failures by revealing when a model attends to irrelevant features [16]. The broader lesson is that autonomy for deep space cannot rest on accuracy alone; it requires systems engineered for graceful degradation, self-assessment, and transparency under precisely the unforeseen conditions that motivate their deployment. Meeting this requirement will demand advances in verified and neuro-symbolic AI, in calibrated uncertainty, and in the human-factors design of the interfaces through which fallible autonomy and expert humans collaborate, all bound together by the governance structures that preserve meaningful human control [38, 40, 44].

## 5.8. Conclusion

This chapter has argued that the integration of artificial intelligence into space mission control is best understood not as a contest between human and machine authority but as a problem of principled collaboration. Communication delay, quantified by the round-trip latency of equation (5.1), makes onboard autonomy a necessity for operations beyond lunar distance, yet the experiential judgement, contextual wisdom, and accountability of human operators remain indispensable. Human-in-the-loop design and explainable AI together resolve this tension: graded, adjustable autonomy relieves the latency bottleneck while explanation preserves the transparency that allows humans to calibrate their trust, maintain situation awareness, and intervene when the automation reaches its limits.

The evidence surveyed here is consistent and actionable. Explanations demonstrably improve operator performance, trust, situation awareness, and diagnostic accuracy; explanation depth should scale with task uncertainty, deepening for time-critical anomaly diagnosis; and a combination of contrastive and global explanations is the most effective form. At the same time, the transparency–cognitive-load trade-off of equations (5.2) and (5.3) warns that more explanation is not always better, and that the design target is the intermediate regime of appropriate reliance depicted in Figure 5.4. The reference architecture of Figure 5.3, integrating hierarchical planning, truth maintenance, and case-based reasoning beneath an adjustable human-authority gate, shows how these principles can be embodied in a system that is both capable and auditable. The successful operation of retrieval-augmented language models aboard the International Space Station demonstrates that disconnected, explainable AI assistance is already feasible in the austere environment of spaceflight, marking a concrete step toward the trustworthy virtual flight controllers that future missions will require. As humanity ventures further from Earth, the disciplined union of human authority and machine explanation charted in this chapter offers a foundation for autonomy that mission operators can understand, supervise, and trust.


## References

[1] Sheridan, T. B., "Telerobotics, Automation, and Human Supervisory Control," MIT Press, Cambridge, MA, 1992.

[2] Edwards, C. D., "Relay communications for Mars exploration," International Journal of Satellite Communications and Networking, vol. 25, no. 2, pp. 111–145, 2007.

[3] Frank, J., Spirkovska, L., McCann, R., Wang, L., Pohlkamp, K., and Morin, L., "Autonomous mission operations," Proceedings of the IEEE Aerospace Conference, pp. 1–20, 2013.

[4] Parasuraman, R., Sheridan, T. B., and Wickens, C. D., "A model for types and levels of human interaction with automation," IEEE Transactions on Systems, Man, and Cybernetics—Part A: Systems and Humans, vol. 30, no. 3, pp. 286–297, 2000.

[5] Gunning, D., and Aha, D. W., "DARPA's explainable artificial intelligence (XAI) program," AI Magazine, vol. 40, no. 2, pp. 44–58, 2019.

[6] Lee, J. D., and See, K. A., "Trust in automation: Designing for appropriate reliance," Human Factors, vol. 46, no. 1, pp. 50–80, 2004.

[7] Endsley, M. R., "Toward a theory of situation awareness in dynamic systems," Human Factors, vol. 37, no. 1, pp. 32–64, 1995.

[8] O'Neill, T., McNeese, N., Barron, A., and Schelble, B., "Human–autonomy teaming: A review and analysis of the empirical literature," Human Factors, vol. 64, no. 5, pp. 904–938, 2022.

[9] Johnson, M., Bradshaw, J. M., Feltovich, P. J., Jonker, C. M., van Riemsdijk, M. B., and Sierhuis, M., "Coactive design: Designing support for interdependence in joint activity," Journal of Human-Robot Interaction, vol. 3, no. 1, pp. 43–69, 2014.

[10] Parasuraman, R., and Riley, V., "Humans and automation: Use, misuse, disuse, abuse," Human Factors, vol. 39, no. 2, pp. 230–253, 1997.

[11] Adadi, A., and Berrada, M., "Peeking inside the black-box: A survey on explainable artificial intelligence (XAI)," IEEE Access, vol. 6, pp. 52138–52160, 2018.

[12] Doshi-Velez, F., and Kim, B., "Towards a rigorous science of interpretable machine learning," arXiv preprint arXiv:1702.08608, 2017.

[13] Miller, T., "Explanation in artificial intelligence: Insights from the social sciences," Artificial Intelligence, vol. 267, pp. 1–38, 2019.

[14] Ribeiro, M. T., Singh, S., and Guestrin, C., "'Why should I trust you?': Explaining the predictions of any classifier," Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, pp. 1135–1144, 2016.

[15] Lundberg, S. M., and Lee, S.-I., "A unified approach to interpreting model predictions," Advances in Neural Information Processing Systems, vol. 30, pp. 4765–4774, 2017.

[16] Selvaraju, R. R., Cogswell, M., Das, A., Vedantam, R., Parikh, D., and Batra, D., "Grad-CAM: Visual explanations from deep networks via gradient-based localization," Proceedings of the IEEE International Conference on Computer Vision, pp. 618–626, 2017.

[17] Wachter, S., Mittelstadt, B., and Russell, C., "Counterfactual explanations without opening the black box: Automated decisions and the GDPR," Harvard Journal of Law & Technology, vol. 31, no. 2, pp. 841–887, 2018.

[18] Stowers, K., Kasdaglis, N., Rupp, M. A., Newton, O. B., Chen, J. Y. C., and Barnes, M. J., "The impact of agent transparency on human performance, trust, and situation awareness in human–autonomy teams," IEEE Transactions on Human-Machine Systems, vol. 50, no. 3, pp. 245–253, 2020.

[19] Sadler, G., Ho, N., Hoffmann, L., Zemlicka, K., Lyons, J., Fergueson, W., and Wilkins, M., "Effects of explanation depth on operator performance and trust during time-critical anomaly diagnosis," Proceedings of the Human Factors and Ergonomics Society Annual Meeting, vol. 63, no. 1, pp. 176–180, 2019.

[20] van der Waa, J., Nieuwburg, E., Cremers, A., and Neerincx, M., "Evaluating XAI: A comparison of rule-based and example-based explanations," Artificial Intelligence, vol. 291, art. 103404, 2021.

[21] Chen, J. Y. C., Procci, K., Boyce, M., Wright, J., Garcia, A., and Barnes, M., "Situation awareness-based agent transparency," U.S. Army Research Laboratory Technical Report ARL-TR-6905, 2014.

[22] Mercado, J. E., Rupp, M. A., Chen, J. Y. C., Barnes, M. J., Barber, D., and Procci, K., "Intelligent agent transparency in human–agent teaming for multi-UxV management," Human Factors, vol. 58, no. 3, pp. 401–415, 2016.

[23] Nau, D., Ghallab, M., and Traverso, P., "Automated Planning and Acting," Cambridge University Press, Cambridge, UK, 2016.

[24] Doyle, J., "A truth maintenance system," Artificial Intelligence, vol. 12, no. 3, pp. 231–272, 1979.

[25] Aamodt, A., and Plaza, E., "Case-based reasoning: Foundational issues, methodological variations, and system approaches," AI Communications, vol. 7, no. 1, pp. 39–59, 1994.

[26] Muscettola, N., Nayak, P. P., Pell, B., and Williams, B. C., "Remote Agent: To boldly go where no AI system has gone before," Artificial Intelligence, vol. 103, no. 1–2, pp. 5–47, 1998.

[27] Sweller, J., "Cognitive load during problem solving: Effects on learning," Cognitive Science, vol. 12, no. 2, pp. 257–285, 1988.

[28] Hart, S. G., and Staveland, L. E., "Development of NASA-TLX (Task Load Index): Results of empirical and theoretical research," Advances in Psychology, vol. 52, pp. 139–183, 1988.

[29] Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., et al., "Language models are few-shot learners," Advances in Neural Information Processing Systems, vol. 33, pp. 1877–1901, 2020.

[30] Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., et al., "Retrieval-augmented generation for knowledge-intensive NLP tasks," Advances in Neural Information Processing Systems, vol. 33, pp. 9459–9474, 2020.

[31] Meza, D., Berndt, J., and Trenchard, M., "Deploying a retrieval-augmented large language model assistant in a disconnected space environment," Proceedings of the AIAA ASCEND Conference, pp. 1–12, 2024.

[32] Marquez, J. J., Hillenius, S., Deliz, I., Kanefsky, B., Zheng, J., and Reagan, M., "Enabling communication and autonomy between astronauts and ground teams for future deep-space operations," Proceedings of the IEEE Aerospace Conference, pp. 1–10, 2019.

[33] Zolghadri, A., "Advanced model-based FDIR techniques for aerospace systems: Today challenges and opportunities," Progress in Aerospace Sciences, vol. 53, pp. 18–29, 2012.

[34] Uriot, T., Izzo, D., Simões, L. F., Abay, R., Einecke, N., Rebhan, S., et al., "Spacecraft collision avoidance challenge: Design and results of a machine learning competition," Astrodynamics, vol. 6, no. 2, pp. 121–140, 2022.

[35] Hoff, K. A., and Bashir, M., "Trust in automation: Integrating empirical evidence on factors that influence trust," Human Factors, vol. 57, no. 3, pp. 407–434, 2015.

[36] Amershi, S., Weld, D., Vorvoreanu, M., Fourney, A., Nushi, B., Collisson, P., et al., "Guidelines for human-AI interaction," Proceedings of the CHI Conference on Human Factors in Computing Systems, pp. 1–13, 2019.

[37] Seshia, S. A., Sadigh, D., and Sastry, S. S., "Toward verified artificial intelligence," Communications of the ACM, vol. 65, no. 7, pp. 46–55, 2022.

[38] Garcez, A. d'Avila, and Lamb, L. C., "Neurosymbolic AI: The third wave," Artificial Intelligence Review, vol. 56, no. 11, pp. 12387–12406, 2023.

[39] Sutton, R. S., and Barto, A. G., "Reinforcement Learning: An Introduction," 2nd ed., MIT Press, Cambridge, MA, 2018.

[40] Santoni de Sio, F., and van den Hoven, J., "Meaningful human control over autonomous systems: A philosophical account," Frontiers in Robotics and AI, vol. 5, art. 15, 2018.

[41] Cummings, M. L., "Automation and accountability in decision support system interface design," Journal of Technology Studies, vol. 32, no. 1, pp. 23–31, 2006.

[42] Crusan, J. C., Smith, R. M., Craig, D. A., Caram, J. M., Guidi, J., Gates, M., et al., "Deep space gateway concept: Extending human presence into cislunar space," Proceedings of the IEEE Aerospace Conference, pp. 1–10, 2018.

[43] Frank, J. D., Iatauro, M., Boddy, M., Dungan, K., Kurklu, E., and Lee, R., "Autonomous mission operations for crewed deep-space missions," Journal of Aerospace Information Systems, vol. 16, no. 10, pp. 447–463, 2019.

[44] Arrieta, A. B., Díaz-Rodríguez, N., Del Ser, J., Bennetot, A., Tabik, S., Barbado, A., et al., "Explainable Artificial Intelligence (XAI): Concepts, taxonomies, opportunities and challenges toward responsible AI," Information Fusion, vol. 58, pp. 82–115, 2020.

[45] Truszkowski, W., Hinchey, M., Rash, J., and Rouff, C., "Autonomous and autonomic systems: A paradigm for future space exploration missions," IEEE Transactions on Systems, Man, and Cybernetics—Part C: Applications and Reviews, vol. 36, no. 3, pp. 279–291, 2006.
