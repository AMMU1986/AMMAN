# Chapter 5

# Human-in-the-Loop and Explainable AI in Mission Control Systems

Amman Jakhar^1,* and Sachin Kalsi^1

^1 Department of Mechanical Engineering, Chandigarh University, Mohali, Punjab-140301, India

*Corresponding author: ammanjakhar5000734@gmail.com

## Abstract

Integrating artificial intelligence into space mission control raises a central tension: how to exploit machine speed and scale while keeping human authority intact. As missions move beyond Earth orbit, communication delays make real-time ground control impractical and force decision authority onboard. Human-in-the-loop (HITL) and explainable AI (XAI) frameworks reconcile this tension by augmenting autonomy while preserving oversight for judgment-laden decisions. Evidence from human-autonomy teaming shows that agents which justify their recommendations improve operator trust, situation awareness, workload, and diagnostic accuracy, and that detailed justifications help most under high uncertainty. However, excessive explanation causes information overload, so depth must be calibrated. This chapter surveys HITL-XAI paradigms, presents a layered reference architecture combining hierarchical planning, truth maintenance, and case-based reasoning, reviews onboard large-language-model deployments aboard the International Space Station, and outlines open problems in verification, human factors, and accountability for autonomous virtual flight controllers.

**Keywords:** human-in-the-loop, explainable AI, mission control systems, space autonomy, human-AI teaming, trust calibration, situation awareness, virtual flight controller

## 5.1. Introduction

The operation of spacecraft has, since the earliest crewed and robotic missions, rested on a tightly coupled partnership between vehicles in flight and large teams of specialists on the ground. Mission control rooms institutionalise this partnership: telemetry flows down to the ground, expert flight controllers interpret it against procedures and hard-won experience, and validated commands flow back up to the vehicle. This arrangement has served remarkably well for missions in low Earth orbit (LEO) and cislunar space, where the round-trip communication delay is small enough that a human remains, in practice, inside every meaningful control loop. Yet the same arrangement becomes progressively untenable as vehicles venture farther from Earth, as the number of tracked objects and simultaneous operations grows, and as the cadence of decisions outpaces the ability of ground teams to respond. Artificial intelligence (AI) is increasingly proposed as the means of closing this gap, and a growing body of work has mapped how learning and reasoning methods can support spacecraft guidance, navigation, and control [1], space situational awareness and collision avoidance [2], and onboard data processing under the severe power, radiation, and computational constraints of the space environment [3].

The motivation for autonomy is therefore not novelty for its own sake but operational necessity. A satellite operator facing hundreds of conjunction warnings per week, or a crewed vehicle on a trans-Mars trajectory, cannot rely on a model in which every decision is adjudicated on the ground [4]. At the same time, spaceflight is unforgiving of error, and the consequences of a misjudged manoeuvre or a mishandled anomaly can be catastrophic and irreversible. This combination—strong pressure toward autonomy coupled with an intolerance of failure—defines the design problem addressed in this chapter. The resolution advocated here is not to replace human controllers with opaque automation, but to construct systems in which AI and humans form an effective team, with authority allocated according to the demands of the situation and with the machine's reasoning rendered legible to the people who remain accountable for the mission.

Two complementary ideas structure this approach. The first is keeping a human in, or on, the loop: designing the division of labour so that humans retain the ability to understand, question, and override automated action. The second is explainability: ensuring that when an AI system recommends or takes an action, it can convey why, in terms a human operator can absorb and act upon. Explanation is not a cosmetic addition. Work in the cognitive and social sciences has long held that useful explanations are contrastive, selective, and social—shaped by what the recipient already expects rather than by an exhaustive dump of internal state [5]. In high-stakes settings, some scholars argue that interpretability should be designed into models from the outset rather than retrofitted onto black boxes [6], while broad surveys have catalogued the concepts, taxonomies, and open challenges of the field now widely known as explainable AI (XAI) [7]. The chapter takes both ideas seriously and treats them as inseparable: autonomy without explanation forfeits oversight, and explanation without a principled allocation of authority is merely decoration.

### 5.1.1. The shifting locus of control in space operations

Historically, the locus of control in space operations has sat firmly on the ground. Flight controllers, organised by subsystem discipline—propulsion, power, thermal, communications, guidance—monitor telemetry and exercise authority through validated command procedures. Automation existed, but largely as scripted command sequences and alarm thresholds rather than as an independent decision-maker. The shift now under way is a migration of decision authority from the ground toward the vehicle, driven by three forces. First, communication latency grows inexorably with distance: negligible in LEO, roughly a second each way to the Moon, and several to tens of minutes to Mars. Second, the scale of operations has exploded, with mega-constellations and a congested orbital environment generating decision volumes that exceed human throughput [2], [4]. Third, the capability of onboard computing and AI has matured to the point where meaningful reasoning can occur aboard the vehicle rather than only on the ground [3].

This migration does not eliminate the human; it changes the human's role from continuous controller to supervisor, collaborator, and final authority. The design challenge is to manage that transition without sacrificing the qualities—judgment, accountability, and the capacity to confront genuine novelty—that human controllers uniquely provide. A poorly managed transition risks the worst of both worlds: automation that acts faster than humans can follow, coupled with humans who no longer understand the system well enough to intervene when it errs. Avoiding that outcome is the practical purpose of the human-in-the-loop and explainability principles developed in the remainder of this chapter.

### 5.1.2. Scope and contributions of this chapter

This chapter examines how HITL and XAI principles can be combined into mission control systems that are simultaneously more autonomous and more trustworthy. Section 5.2 establishes the conceptual foundations of human-in-the-loop control, introducing the autonomy spectrum and its dependence on communication latency, and formalising when authority must move onboard. Section 5.3 surveys explainable AI for human-AI teaming, presenting a taxonomy of explanation types and reviewing the empirical evidence on their effects on operators. Section 5.4 develops a layered reference architecture for HITL-XAI mission control, treating hierarchical planning, truth maintenance, case-based reasoning, explanation generation, and trust calibration as interacting components, and expressing several of the key trade-offs as simple models. Section 5.5 examines emerging deployments, most notably onboard large-language-model systems aboard the International Space Station (ISS) and autonomous collision-avoidance capabilities. Section 5.6 sets out open problems in verification, human factors, and accountability, and Section 5.7 concludes.

## 5.2. Foundations of Human-in-the-Loop Mission Control

Human-in-the-loop control is best understood not as a single design but as a family of arrangements distinguished by how authority and initiative are shared between human and machine. To reason about these arrangements it is useful to place them on a spectrum and to connect that spectrum to the physical constraint that most strongly shapes space operations: the finite speed of light.

### 5.2.1. The autonomy spectrum

At one extreme of the spectrum lies fully manual, ground-controlled operation, in which the vehicle executes explicit commands and exercises no independent judgment. At the other lies full autonomy, in which an onboard system perceives, decides, and acts, with human involvement reduced to after-the-fact review. Between these poles lie the two configurations of greatest practical interest. In a human-in-the-loop configuration, the AI proposes actions but a human must approve each one before it is executed; the human is a mandatory gate in the control loop. In a human-on-the-loop configuration, the AI acts on its own initiative while a human supervises and retains the ability to intervene or veto; the human is a monitor with an override, not a gate. Figure 5.1 depicts this spectrum and, crucially, aligns it with the communication latency that determines which configurations are feasible for a given mission.

[[FIGURE 5.1]]
Figure 5.1. The autonomy spectrum in mission control, aligned with one-way communication latency. As distance from Earth grows, the feasible operating point shifts from ground control toward onboard autonomy, while human authority and real-time oversight necessarily decline.

The spectrum is not merely descriptive. Empirical studies of human-machine teams show that the level of autonomy (LOA) materially affects coordination, performance, trust, and operator workload, and that neither extreme is uniformly best; intermediate, well-designed teaming arrangements often outperform both fully manual and fully automatic modes [8]. The design task is therefore to select, and to be able to shift between, points on this spectrum as circumstances demand—a capability sometimes called adaptive or adjustable autonomy. Crucially, the appropriate point is not fixed for a mission but varies with the phase of flight, the criticality of the subsystem, and the health of the vehicle: a controller may keep tight per-action authority during a docking manoeuvre yet delegate routine thermal management to the onboard system. Table 5.1 summarises the principal loop configurations and the operational regimes to which each is suited, together with the human role and authority model that each entails.

Table 5.1. Loop configurations across the autonomy spectrum, with the associated human role, authority model, latency regime, and representative mission contexts.

| Configuration | Human role | Authority | Latency regime | Representative context |
| --- | --- | --- | --- | --- |
| Manual / ground control | Controller issues every command | Human total | Sub-second (LEO/GEO) | Crewed LEO, early commissioning |
| Human-in-the-loop | Approves each AI-proposed action | Human per-action gate | Seconds (cislunar) | Lunar operations, high-risk manoeuvres |
| Human-on-the-loop | Supervises; can veto or intervene | Human override | Minutes (Mars) | Deep-space cruise, routine station-keeping |
| Full autonomy | Reviews outcomes after the fact | Onboard, human post-hoc | Tens of minutes and beyond | Time-critical safing, deep-space anomalies |

### 5.2.2. Communication latency and the case for onboard autonomy

The dominant physical driver of the autonomy spectrum is one-way light time. In LEO the delay is on the order of milliseconds, so a controller can react to telemetry essentially in real time and a human-in-the-loop arrangement imposes no penalty. In cislunar space the one-way delay approaches 1.3 seconds—still tolerable for supervisory control but already awkward for tasks requiring tight closed-loop timing. For Mars the one-way delay ranges from roughly four to twenty-four minutes depending on the relative positions of the planets, which makes real-time ground control physically impossible: by the time a warning reaches Earth and a considered response returns, the moment for effective action has often passed. As Figure 5.1 makes explicit, missions beyond cislunar space must place time-critical decision authority onboard, retaining the human as a supervisor who sets goals, reviews behaviour, and intervenes on the slower cadence that latency permits.

This constraint has been studied concretely for Mars surface operations, where the formulation of safe, valid activity plans must reconcile high-level science objectives with the practical impossibility of interactive ground supervision, and where operator trust in the autonomous planner becomes a precondition for delegating authority at all [9]. More generally, for a human to supervise an autonomous system across such a gap, the system must be able to make its state and reasoning legible despite the delay; situation awareness, transparency, and explainability are therefore not separable concerns but facets of a single design problem, a point argued forcefully in the human-factors literature on human-AI teams [10]. The difficulty is sharpened for crewed deep-space missions by the isolated, confined, and extreme (ICE) nature of the environment, which amplifies every difficulty of human-AI interaction—trust, transparency, autonomy, and the social attribution of competence to the machine—and turns these settings into a demanding stress test for the very design principles this chapter advocates [11].

### 5.2.3. Allocating authority as a function of latency and urgency

Table 5.1 pairs each loop configuration with a latency regime, but latency alone does not determine the appropriate allocation of authority; the urgency of the decision matters just as much. A useful way to formalise this is to compare the time available to act with the time required to consult a human. Let t_deadline denote the time from detection of a situation to the last moment at which an effective action can still be taken, and let t_human denote the expected time to route the situation to a human and receive an authorised response, which for ground-based supervision is dominated by round-trip light time. A simple decision rule for whether authority must reside onboard is

(5.1)   A_onboard = 1 if t_human ≥ γ · t_deadline, else 0,

where γ ∈ (0,1] is a safety margin reflecting how much of the available window may prudently be consumed by consultation. Equation (5.1) captures the intuition behind Figure 5.1: as t_human grows with distance, an increasing fraction of decisions—those with short t_deadline, such as collision avoidance or subsystem safing—cross the threshold and must be delegated onboard, while decisions with long deadlines can safely remain with the human. The design of a HITL-XAI system is, in large part, the design of this allocation together with the explanation machinery that lets humans supervise the decisions that fall on the autonomous side of it. Notably, the same mission may occupy several of these configurations at once, delegating short-deadline safety functions while retaining per-action authority over strategic or scientific choices, so that the allocation is best thought of as decision-by-decision rather than mission-wide.

## 5.3. Explainable AI for Human-AI Teaming in Space

If autonomy is the answer to latency, explainability is the answer to the loss of oversight that autonomy entails. When a human can no longer adjudicate each action, the human's ability to supervise depends on being able to understand, after or alongside the fact, what the machine did and why. This section reviews why explainability matters in safety-critical operations, offers a taxonomy of explanation types, and surveys the empirical evidence on how explanation affects human operators.

### 5.3.1. Why explainability matters in safety-critical operations

The case for explainability in mission control rests on three linked claims. The first is epistemic: an operator who understands the basis of a recommendation can judge whether it genuinely applies to the situation at hand, catching cases where the model is confidently wrong because the situation falls outside its competence. The second concerns trust calibration: explanations, when well designed, help operators trust the system when it is right and distrust it when it is wrong, rather than trusting it uniformly or not at all. The third is about accountability: humans who remain legally and organisationally responsible for a mission must be able to give an account of why decisions were made, which is impossible if the decision process is opaque. These motivations are not specific to space; they animate the broader programme of building explainable agents and robots that can articulate the reasons for their behaviour [12]. Design guidance for human-AI interaction has consistently emphasised making system behaviour and confidence legible and supporting graceful correction of errors [13], and user-centred methods have been proposed for deriving explanation requirements from the questions people actually ask rather than from what a model can conveniently expose [14].

The counsel here is not that more explanation is always better. As later subsections make clear, explanation carries a cognitive cost, and the goal is calibrated understanding, not maximal disclosure. But the baseline claim—that opaque automation is ill-suited to safety-critical supervision by accountable humans—is now widely accepted, and it motivates the taxonomy that follows.

### 5.3.2. A taxonomy of explanation types

Explanations differ along several dimensions, and choosing among them is a central design decision. Figure 5.3 organises the space along three axes: scope, form, and timing. By scope, an explanation may be global, describing the model's overall behaviour, or local, justifying a single decision. By timing, it may be ante-hoc (intrinsic to a transparent model) or post-hoc (generated after the fact to explain a black box). By form, explanations include contrastive ("why A rather than B?"), feature-attribution (which inputs mattered most), example- or case-based (this decision resembles these prior cases), and rule-based (an if-then account of the logic). Surveys of the field have proposed broadly compatible taxonomies and have stressed that evaluation must be tied to the explanation's purpose rather than to generic notions of fidelity [15], and dedicated reviews of XAI taxonomies show how these dimensions can be organised into a coherent design vocabulary [16].

[[FIGURE 5.3]]
Figure 5.3. A taxonomy of explanation types for mission-control XAI, organised by scope (global vs. local), form (contrastive, feature-attribution, example/case-based, rule-based), and timing (ante-hoc vs. post-hoc). The reported combination of contrastive and global explanations is highlighted as particularly effective for user preference and performance.

Two forms deserve emphasis in the mission-control context. Contrastive explanations align with how people naturally seek explanation—by asking why one outcome occurred instead of an expected alternative—and have been studied as a way to make rule-based and example-based justifications more useful to non-specialists [17]. Case-based explanation, in which a decision is justified by reference to similar past situations, is attractive precisely because flight operations already rely heavily on precedent and validated procedures. Explanations of automated planning and scheduling—the reasoning most relevant to mission operations—form their own emerging subfield, in which the challenge is to explain not a classification but a plan: why this sequence of actions, why not an alternative, and what would have to change for the plan to differ [18]. Table 5.2 collects the principal explanation types with a mission-control example and the primary benefit and cost of each, and it is this cost-benefit structure, rather than any single "best" explanation, that should guide design.

Table 5.2. Explanation types with mission-control examples, primary benefits, and principal costs.

| Explanation type | Mission-control example | Primary benefit | Principal cost |
| --- | --- | --- | --- |
| Global | Overview of how the anomaly classifier weighs subsystems | Builds an accurate mental model; low workload | May not justify a specific action |
| Local | Why this specific telemetry pattern was flagged | Directly relevant to the decision at hand | Can be dominated by spurious features |
| Contrastive | Why safe-mode rather than continued operation | Matches human question-asking; aids trust | Higher cognitive effort to process |
| Feature-attribution | Which sensors drove a collision-risk estimate | Pinpoints the evidence quickly | Risk of reading correlation as cause |
| Example / case-based | This fault resembles three prior on-orbit events | Leverages operator precedent knowledge | Requires a curated, relevant case base |
| Rule-based | The if-then logic that triggered the manoeuvre | Auditable and verifiable | Brittle for complex, learned behaviour |

### 5.3.3. Empirical effects on trust, situation awareness, and workload

A substantial experimental literature now examines what explanation actually does for human-AI teams, and the picture is more nuanced than early enthusiasm suggested. Explainable interfaces have been argued to enhance shared situation awareness and mental-model formation, which are the defining characteristics of effective teaming [19], and dedicated surveys of explainable interfaces for human-autonomy teaming have begun to consolidate design knowledge specific to this setting [20]. Studies that pair AI advice with confidence information and explanation find that these cues can improve the accuracy of human-AI decisions and help calibrate trust, though the effect depends heavily on how the information is presented [21]. Critically, several studies show that explanations do not automatically produce complementary team performance—teams that outperform either the human or the AI alone—and that poorly designed explanation can induce over-reliance, in which operators accept incorrect advice because an explanation lends it a veneer of legitimacy [22]. The distinction between warranted and unwarranted reliance has been sharpened into the notion of appropriate reliance, in which the goal is not to maximise agreement with the AI but to accept correct advice and reject incorrect advice, a distinction that explanations sometimes help and sometimes hinder [23]. A recent meta-analysis of XAI-based decision support concludes that while such support tends to improve task performance overall, the explanations themselves are frequently not the decisive factor, underscoring that explanation is necessary but far from sufficient [24].

For the specific choice among explanation forms, the evidence increasingly favours a combination rather than a single winner. A controlled study of explanation strategy in human-AI collaborative decision-making found that global explanations incurred the lowest mental workload and yielded the highest understandability, whereas contrastive explanations demanded the most effort but produced the highest perceived competence, affect-based trust, and sense of collaboration [25]. This dissociation—global explanations for economical understanding, contrastive explanations for trust and engagement—explains why the pairing of contrastive and global explanations highlighted in Figure 5.3 is attractive: the two forms address different operator needs and, used together, cover both the workload and the trust dimensions catalogued in Table 5.2. Findings from reinforcement-learning settings temper this optimism, showing that contrastive explanations are not always sufficient on their own and may need to be complete to be genuinely helpful [26], and a mixed-methods study of human-AI teams reported the counter-intuitive result that a lower-explainability agent was sometimes perceived as more trustworthy and competent, a reminder that more explanation is not monotonically better [27]. Consistent with this, comparative work on how different explanation classes affect trust calibration in decision-support settings finds that the same explanation can improve calibration for some users while degrading it for others, so explanation design must account for individual differences and expertise [28].

### 5.3.4. Explanation depth under uncertainty

The dependence of explanation value on context is nowhere sharper than under uncertainty. When a situation is routine and the AI's confidence is high, a terse explanation suffices and elaborate justification merely wastes attention. When the situation is uncertain—an ambiguous anomaly, conflicting sensor evidence, an off-nominal state not covered by procedure—operators benefit from deeper, more detailed justifications that expose the underlying evidence and reasoning, particularly in time-critical diagnosis where a wrong call is costly. Figure 5.4 sketches this relationship: operator performance rises with explanation depth, but the slope and the location of the useful maximum depend on the level of uncertainty, and beyond a certain depth additional detail degrades performance by overloading the operator.

[[FIGURE 5.4]]
Figure 5.4. Explanation depth versus operator performance and cognitive load. Under high uncertainty, deeper justifications yield substantial gains before plateauing; under low uncertainty, benefits saturate early and excessive depth pushes operators into an information-overload regime where added detail reduces performance.

The two curves encode a design principle: explanation depth should be adaptive, expanding under uncertainty and contracting when the situation is clear. This is consistent with uncertainty-aware perspectives on explanation that attach a confidence estimate to the explanation itself, not merely to the prediction, so that operators can tell a well-supported justification from a speculative one [29]. It also reflects a hard limit on the human side: attention and working memory are finite, and explanations compete with the primary task for these scarce resources. Studies of how practitioners use interpretability tools have found that the mere availability of explanation can breed over-confidence and misuse, with users reading structure into noise and trusting tools they do not understand [30], and controlled experiments have documented anchoring effects in which an initial explanation biases all subsequent judgment [31]. Trust research further cautions that perfect calibration is not always the right target; some principled distrust is healthy, and a degree of deliberate miscalibration can be protective when the system's competence boundary is unknown [32]. Quasi-experimental work in diagnostic decision support shows the positive side of the same coin: explanation designed explicitly to support calibration can measurably improve the accuracy with which experts accept or reject machine advice [33]. The quantitative management of this depth-versus-load trade-off is taken up in Section 5.4.4.

## 5.4. Architecting HITL-XAI Mission Control Systems

The foregoing principles must be embodied in an architecture. This section presents a layered reference design, describes the reasoning and explanation components that populate it, and formalises the trust-calibration and cognitive-load trade-offs that govern its human-facing behaviour.

### 5.4.1. A layered reference architecture

Figure 5.2 presents a reference architecture organised as five layers, with information rising and authority descending. At the base, the telemetry and sensor layer (L1) ingests spacecraft subsystem data, guidance and navigation state, life-support parameters, and space-domain awareness inputs such as conjunction data. Above it, the AI reasoning core (L2) performs the substantive work—planning, diagnosis, and prediction—using the heterogeneous methods described below. The explanation-generation layer (L3) transforms the reasoning core's internal state into the explanation forms of the taxonomy, attaching confidence, provenance, and uncertainty. The operator interface layer (L4) presents recommendations, alerts, and explanations, and critically allows the human to adjust explanation depth in line with the depth-adaptivity principle developed below. At the top, the human decision and authority layer (L5) is where crew or ground controllers approve, override, delegate, or abort, retaining ultimate authority over the vehicle.

[[FIGURE 5.2]]
Figure 5.2. Reference architecture of a human-in-the-loop, explainable-AI mission control system. Telemetry and reasoning rise through explanation generation to the operator, while authority descends from the human decision layer; the design supports disconnected operation via a self-contained onboard reasoning core.

The essential property of this architecture is the deliberate separation of the reasoning core (L2) from the explanation layer (L3). This separation, advocated in work on deploying explainable machine learning in real settings [34] and in the broader programme of human-centred XAI that moves the emphasis from algorithms to user experiences [35], allows the explanation machinery to be designed, evaluated, and improved against human needs independently of the underlying models. It also enables the same reasoning to be explained in different forms and depths for different operators and situations—precisely the adaptivity that Table 5.2 calls for. Surveys of user studies of model explanations reinforce the point that the value of any explanation is realised only at this human-facing boundary, in changed human understanding and behaviour, rather than in the model internals themselves [36]. A practical corollary is that the explanation layer should be treated as a first-class engineering artefact with its own requirements, tests, and acceptance criteria, not as a reporting afterthought bolted onto a finished model.

### 5.4.2. Hierarchical planning, truth maintenance, and case-based reasoning

The reasoning core (L2) is deliberately heterogeneous, because no single technique satisfies all of the demands of mission operations: the core must plan over long horizons, maintain a consistent picture of a changing world, and behave predictably enough to be trusted. Three complementary mechanisms address these demands. Hierarchical task planning decomposes high-level mission goals into sub-goals and primitive actions, producing plans that are themselves explainable because their structure mirrors the goal decomposition an operator already understands; the explainable-planning literature shows how such plans can be interrogated contrastively—why this action, why not another—and how a system can reconcile its plan with the operator's differing expectations [18]. A truth-maintenance capability records the dependencies among beliefs and conclusions so that when new telemetry contradicts an earlier inference, the system can retract exactly what depended on the stale belief and, equally important, can trace and report why it now believes what it does. Case-based reasoning grounds decisions in a library of prior situations, delivering both predictable behaviour and a naturally case-based form of explanation that resonates with the precedent-driven culture of flight operations, as reflected in the example/case-based entry of the explanation taxonomy.

Together these mechanisms give the reasoning core the three properties that supervision across a latency gap requires: foresight, consistency, and traceability. The truth-maintenance layer in particular is what allows the explanation layer above it to answer the operator's most important question during an evolving anomaly—not merely what the system concluded, but what would change its mind. Within the reasoning core, these mechanisms are not alternatives but collaborators: the planner proposes, the truth-maintenance system keeps the proposal consistent with incoming evidence, and the case base supplies precedent that both constrains behaviour and furnishes ready-made explanatory material.

### 5.4.3. Explanation generation and interface design

The explanation layer (L3) and interface (L4) turn internal reasoning into calibrated understanding, and their design follows directly from the empirical findings of Section 5.3. Because global explanations minimise workload while contrastive explanations maximise trust and engagement [25], the interface should offer a layered presentation: a concise global or summary explanation by default, expandable on demand into contrastive and case-based detail. This directly operationalises the depth-adaptivity principle and the type trade-offs catalogued in Table 5.2. Explanations should carry explicit confidence and, wherever possible, an indication of the uncertainty in the explanation itself, following uncertainty-aware approaches [29], because an operator who cannot distinguish a confident recommendation from a guess cannot calibrate trust. The interface must also guard against the failure modes documented earlier—over-reliance and anchoring—for example by prompting the operator to consider disconfirming evidence rather than presenting only the system's preferred conclusion, and by varying the framing so that repeated interactions do not entrench a single anchor. Work connecting explanation design explicitly to trust calibration provides concrete interaction patterns for these safeguards, including the timing and granularity at which confidence and rationale should be surfaced [37].

### 5.4.4. Trust calibration and cognitive-load management

The human-facing behaviour of the architecture can be made precise with a few simple models that formalise the qualitative curves of Figure 5.4. Trust calibration is the alignment between an operator's reliance on the system and the system's actual reliability. If we let r(x) ∈ [0,1] denote the operator's propensity to accept the system's recommendation on instance x, and c(x) ∈ [0,1] denote the system's true probability of being correct on x, then a natural measure of miscalibration over a set of N instances is

(5.2)   M = (1/N) · Σ | r(x_i) − c(x_i) |,

where perfect calibration corresponds to M = 0. Good explanation reduces M by making c(x) legible: it should raise reliance where the system is likely correct and lower it where the system is likely wrong, rather than raising reliance uniformly. Over-reliance corresponds to r(x) > c(x) precisely where c(x) is low—the operator accepting bad advice—and is exactly what adaptive, uncertainty-bearing explanation is meant to prevent. Conceptual toolkits for measuring trust in human-autonomy teams provide operational instruments for estimating quantities like r(x) in realistic settings, including behavioural and self-report measures that can be combined into a running estimate of team trust [38].

The value of explanation must be weighed against its cost. Let b(d) be the performance benefit of an explanation of depth d and let k(d) be its cognitive cost, both increasing in d but with b(d) eventually saturating while k(d) continues to grow. The net utility of explanation depth is

(5.3)   U(d) = b(d) − λ · k(d),

where λ scales the operator's sensitivity to workload. The useful depth is the value d_opt that maximises U(d); beyond it, added detail costs more than it returns and the operator slides into the information-overload regime. Because b(d) is steeper under uncertainty—detailed justification helps more when the situation is ambiguous—the optimum d_opt shifts to the right as uncertainty rises, which is the formal content of the two curves. Finally, since workload, trust, and situation awareness co-vary and can now be estimated in near real time from operator physiological and behavioural signals [39], an advanced interface can in principle adjust d toward d_opt dynamically, expanding explanation when the operator has spare capacity and contracting it when they are saturated. Closing this loop reliably—measuring operator state accurately enough to drive an adaptive interface without itself becoming a distraction—remains an active and demanding research problem [39].

## 5.5. Emerging Deployments and Case Studies

The architecture of Section 5.4 is not merely notional. Several recent deployments demonstrate that its key ingredients—onboard reasoning, disconnected operation, and human-facing explanation—are now feasible in flight-relevant settings. This section reviews the most significant of these and synthesises them in Table 5.3.

### 5.5.1. Onboard language models and the virtual flight controller

The most striking recent milestone is the deployment of large-language-model (LLM) capability aboard the ISS. In a demonstration using an onboard supercomputer, an LLM was run entirely on the station, establishing that disconnected AI operation in an austere, radiation-exposed environment is feasible and that inference need not depend on a live link to the ground [40]. This matters for the architecture of Figure 5.2 because it validates the disconnected-operation property: the reasoning and explanation layers can, in principle, reside onboard and continue to function when communication with Earth is unavailable, which is the defining condition of deep-space operation identified in Section 5.2.2. Table 5.3 records this and the other deployments discussed here against the architectural properties they exercise.

Complementary work has focused on retrieval-augmented generation (RAG) for procedure support. A representative assistant combines knowledge graphs, retrieval-augmented generation, and augmented-reality cues to help astronauts execute procedures reliably and offline aboard the ISS and future lunar platforms, explicitly targeting the reliability and offline-availability requirements that a naive language model cannot meet [41]. Related efforts have extended LLM-driven, immersive interfaces to spacewalk and robotics support in NASA-sponsored analog studies, illustrating how the operator-interface layer might look in practice and how natural-language interaction can lower the workload of consulting complex procedures under time pressure [42]. Taken together, these deployments trace a credible path toward a "virtual flight controller": an onboard system that emulates key mission-control functions—monitoring, procedure execution, and first-line anomaly response—while surfacing its reasoning to crew in natural language. Retrieval augmentation is particularly significant for explainability, because grounding responses in an auditable corpus of procedures and prior cases provides exactly the provenance that the explanation layer requires, converting an otherwise opaque generative model into one whose assertions can be traced to source documents.

### 5.5.2. Autonomous collision avoidance and space traffic management

A second domain in which HITL-XAI principles are being operationalised is space traffic management (STM) and collision avoidance, where the sheer volume of conjunction events has already outstripped manual handling [4]. Reviews of collision-avoidance manoeuvre design document a clear trajectory from manual, operator-designed manoeuvres toward the autonomous computation of fuel-efficient avoidance actions, motivated by the rising frequency of close approaches [43], and onboard approaches combining machine learning with analytical methods have been proposed to bring at least the initial screening and manoeuvre-design steps aboard the spacecraft [44]. The characteristic HITL question in this domain is the go/no-go manoeuvre decision, which operators have traditionally retained even when the surrounding pipeline is automated—a textbook instance of the authority-allocation problem formalised in Equation (5.1). Here explanation is essential for trust: an operator asked to approve, or to delegate, an autonomous avoidance manoeuvre needs a contrastive, evidence-bearing account of why the manoeuvre is recommended and what the consequences of inaction would be, exactly the pairing of contrastive and global explanation highlighted in Figure 5.3. Without such an account, the operator can neither confidently approve the action nor justify a decision to override it.

### 5.5.3. Comparative synthesis

Table 5.3 synthesises these deployments against the architectural properties introduced above and the autonomy configurations of Table 5.1. The comparison reveals a field advancing on multiple fronts—onboard inference, disconnected operation, procedure grounding, and autonomous manoeuvre design—but not yet integrated into a single system that combines all of them with mature, adaptive explanation. Lessons from human-autonomy teaming in adjacent high-stakes domains, such as tactical operations, reinforce the same conclusion: improvements in situational awareness and decision support are real and measurable, but trust and explainability remain the limiting factors that determine whether operators actually accept and benefit from autonomy [45].

Table 5.3. Comparative synthesis of emerging HITL-XAI deployments against key architectural properties.

| Deployment | Onboard reasoning | Disconnected operation | Explanation form | Autonomy configuration |
| --- | --- | --- | --- | --- |
| Onboard LLM on ISS [40] | Yes (station supercomputer) | Demonstrated | Natural-language, emerging | Human-in-the-loop |
| RAG procedure assistant [41] | Yes | Yes (offline by design) | Retrieval-grounded, case-like | Human-in-the-loop |
| Immersive AR operator interface [42] | Partial | Partial | Natural-language plus AR cues | Human-on-the-loop |
| Autonomous collision avoidance [43], [44] | Partial (onboard screening) | Partial | Contrastive risk rationale | Human-on-the-loop / delegated |

As Table 5.3 indicates, the building blocks of the reference architecture already exist in isolation; the outstanding work is their integration and the maturation of the explanation layer, which is the subject of the challenges discussed next.

## 5.6. Challenges, Open Problems, and Research Directions

Despite rapid progress, significant obstacles stand between the current state of the art and dependable HITL-XAI mission control. Table 5.4 organises these challenges and pairs each with a recommended research direction; the subsections that follow elaborate the most consequential of them.

Table 5.4. Open challenges for HITL-XAI mission control and recommended research directions.

| Challenge | Why it is hard in space operations | Recommended direction |
| --- | --- | --- |
| Verification and certification | Learned components resist exhaustive testing; consequences are irreversible | Hybrid architectures with verifiable rule-based safety envelopes around learned cores |
| Explanation faithfulness | Post-hoc explanations may not reflect the true reasoning | Ante-hoc/intrinsic interpretability; provenance via retrieval and truth maintenance |
| Trust calibration | Both over- and under-reliance degrade outcomes | Uncertainty-bearing, adaptive-depth explanation with calibration metrics |
| Cognitive load and skill retention | Supervisors deskill and are overloaded during rare crises | Adaptive autonomy; training that preserves manual competence |
| Accountability and authority | Responsibility must remain with identifiable humans | Auditable decision logs; explicit authority-allocation policies |

### 5.6.1. Verification, validation, and certification

Spaceflight software is subject to stringent verification and validation, but learned components resist the exhaustive, requirements-based testing that traditional flight software undergoes, because their behaviour is defined by data rather than by inspectable logic. As the first row of Table 5.4 indicates, the most promising response is architectural: wrap learned reasoning cores in verifiable, rule-based safety envelopes that constrain the system to a certified-safe region of behaviour, so that the autonomy of the reasoning core operates within guarantees that can be checked independently of the learned model. This partitioning also aids explanation, since the rule-based envelope is inherently auditable, and it aligns with the long-standing argument that high-stakes decisions benefit from interpretable structure rather than unconstrained black boxes [6]. Surveys of interpretability methods provide a menu of techniques from which the intrinsic, verifiable components of such envelopes can be drawn, spanning inherently interpretable models and post-hoc methods whose outputs can themselves be validated [46]. The certification question—how a safety authority should gain assurance in a system whose behaviour is partly learned—remains largely open and is likely to require new standards as much as new algorithms.

### 5.6.2. Human factors: workload, skill retention, and vigilance

A well-known paradox of automation is that it reduces routine workload while making the residual, rare, high-stakes interventions harder, because supervisors lose situational engagement and practised skill precisely when they most need them. This is the concern behind the cognitive-load and skill-retention challenge noted above. The adaptive-depth explanation formalised in Equation (5.3) and depicted in Figure 5.4 addresses part of the problem by managing moment-to-moment workload, but it does not by itself preserve the deeper competence that lets a controller take over in a genuine crisis. Sustaining that competence requires deliberate design—periodic manual operation, high-fidelity training, and interfaces that keep operators cognitively in the loop even when they are not in the control loop—and the problem is especially acute in the ICE conditions of long-duration crewed missions [11], where crews cannot draw on a large ground team and must retain broad competence across many subsystems. The near-real-time estimation of trust, workload, and situation awareness discussed in Section 5.4.4 offers one route to detecting dangerous disengagement before it matters, by flagging when an operator's state has drifted away from the range in which effective supervision is possible [39].

### 5.6.3. Ethics, accountability, and the locus of authority

Finally, the migration of decision authority described in Section 5.1.1 raises questions of accountability that technology alone cannot resolve. If an autonomous system takes an irreversible action, responsibility must still rest with identifiable humans and organisations, which requires that authority allocation be explicit and that decisions be logged in an auditable, explainable form—the accountability row of Table 5.4. Equation (5.1) offers a principled basis for deciding which decisions may be delegated, but the choice of the safety margin γ, and the residual authority retained by humans, are governance decisions as much as engineering ones. The explanation layer of Figure 5.2 is thus not only a usability feature but an accountability mechanism: it produces the record and the rationale by which humans can answer, after the fact, for what an autonomous system did on their behalf. Ensuring that this record is faithful—that the explanation reflects the actual reasoning rather than a plausible reconstruction—remains one of the field's central open problems, and it is why the truth-maintenance and retrieval-grounding mechanisms of Sections 5.4.2 and 5.5.1 are so important: they make faithful explanation a structural property of the system rather than an aspiration.

## 5.7. Conclusion

The integration of AI into space mission control is best understood not as a contest between human and machine authority but as the design of a partnership in which each contributes what it does best. Communication latency, formalised in Equation (5.1) and illustrated in Figure 5.1, makes onboard autonomy a physical necessity for missions beyond cislunar space; the loss of real-time oversight that autonomy entails, catalogued across the configurations of Table 5.1, makes explainability a corresponding necessity rather than a luxury. The empirical literature reviewed in Section 5.3 shows that explanation, when well designed, improves trust calibration, situation awareness, and diagnostic accuracy; that the combination of contrastive and global explanations is especially effective; and that explanation depth must be adapted to uncertainty to avoid the information overload depicted in Figure 5.4. The layered reference architecture of Figure 5.2, combining hierarchical planning, truth maintenance, and case-based reasoning beneath a dedicated explanation layer, offers a way to keep ultimate authority with humans while delegating time-critical action to the machine. Emerging deployments—onboard language models and retrieval-augmented assistants aboard the ISS, and increasingly autonomous collision avoidance—demonstrate that the necessary ingredients exist, and the remaining work set out in Table 5.4 is to integrate them into verifiable, accountable systems and to mature the explanation layer that turns raw autonomy into a trustworthy virtual flight controller. The destination is a mission control in which humans supervise rather than operate, understand rather than merely command, and remain, always, the final authority.

## References

[1] D. Izzo, M. Märtens, and B. Pan, "A survey on artificial intelligence trends in spacecraft guidance dynamics and control," Astrodynamics, vol. 3, no. 4, pp. 287–299, 2019.

[2] L. Mashiku and D. Hall, "Recommended methods for improving space situational awareness and collision avoidance using artificial intelligence and machine learning," in Proc. AAS/AIAA Astrodynamics Specialist Conference, 2019.

[3] V. Kothari, E. Liberis, and N. D. Lane, "The final frontier: Deep learning in space," in Proc. 21st Int. Workshop on Mobile Computing Systems and Applications (HotMobile), 2020, pp. 45–49.

[4] R. Furfaro et al., "Artificial intelligence in computational astrodynamics: Application to space sustainability and space traffic management," Advances in Space Research, 2024.

[5] T. Miller, "Explanation in artificial intelligence: Insights from the social sciences," Artificial Intelligence, vol. 267, pp. 1–38, 2019.

[6] C. Rudin, "Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead," Nature Machine Intelligence, vol. 1, no. 5, pp. 206–215, 2019.

[7] A. Barredo Arrieta et al., "Explainable Artificial Intelligence (XAI): Concepts, taxonomies, opportunities and challenges toward responsible AI," Information Fusion, vol. 58, pp. 82–115, 2020.

[8] A. R. Wasser et al., "Teammates instead of tools: The impacts of level of autonomy on mission performance and human–agent teaming dynamics in multi-agent distributed teams," Frontiers in Robotics and AI, vol. 9, 782134, 2022.

[9] J. Marshall et al., "Examining operational trust and intention toward Mars autonomous systems," arXiv preprint arXiv:2110.15460, 2021.

[10] M. R. Endsley, "Supporting human-AI teams: Transparency, explainability, and situation awareness," Computers in Human Behavior, vol. 140, 107574, 2023.

[11] A. Casini et al., "Human–AI interaction in isolated, confined, and extreme environments: Psychological, ethical, and design perspectives," Frontiers in Human Dynamics, vol. 8, 2026.

[12] S. Anjomshoae, A. Najjar, D. Calvaresi, and K. Främling, "Explainable agents and robots: Results from a systematic literature review," in Proc. 18th Int. Conf. on Autonomous Agents and Multiagent Systems (AAMAS), 2019, pp. 1078–1088.

[13] S. Amershi et al., "Guidelines for human-AI interaction," in Proc. CHI Conf. on Human Factors in Computing Systems, 2019, pp. 1–13.

[14] D. Wang, Q. Yang, A. Abdul, and B. Y. Lim, "Designing theory-driven user-centric explainable AI," in Proc. CHI Conf. on Human Factors in Computing Systems, 2019, pp. 1–15.

[15] G. Vilone and L. Longo, "Notions of explainability and evaluation approaches for explainable artificial intelligence," Information Fusion, vol. 76, pp. 89–106, 2021.

[16] T. Speith, "A review of taxonomies of explainable artificial intelligence (XAI) methods," in Proc. ACM Conf. on Fairness, Accountability, and Transparency (FAccT), 2022, pp. 2239–2250.

[17] J. van der Waa, E. Nieuwburg, A. Cremers, and M. Neerincx, "Evaluating XAI: A comparison of rule-based and example-based explanations," Artificial Intelligence, vol. 291, 103404, 2021.

[18] T. Chakraborti, S. Sreedharan, and S. Kambhampati, "The emerging landscape of explainable automated planning and decision making," in Proc. 29th Int. Joint Conf. on Artificial Intelligence (IJCAI), 2020, pp. 4803–4811.

[19] M. Paleja et al., "The utility of explainable AI in ad hoc human-machine teaming," in Advances in Neural Information Processing Systems (NeurIPS), 2021.

[20] X. Wang et al., "Explainable interface for human-autonomy teaming: A survey," arXiv preprint arXiv:2405.02583, 2024.

[21] Y. Zhang, Q. V. Liao, and R. K. E. Bellamy, "Effect of confidence and explanation on accuracy and trust calibration in AI-assisted decision making," in Proc. ACM Conf. on Fairness, Accountability, and Transparency (FAT*), 2020, pp. 295–305.

[22] G. Bansal et al., "Does the whole exceed its parts? The effect of AI explanations on complementary team performance," in Proc. CHI Conf. on Human Factors in Computing Systems, 2021, pp. 1–16.

[23] P. Schemmer, N. Kühl, C. Benz, A. Bartos, and G. Satzger, "Appropriate reliance on AI advice: Conceptualization and the effect of explanations," in Proc. 28th Int. Conf. on Intelligent User Interfaces (IUI), 2023, pp. 410–422.

[24] F. Fügener et al., "The effect of explainable AI-based decision support on human task performance: A meta-analysis," arXiv preprint arXiv:2504.13858, 2025.

[25] Y. Wang, M. Zhang, and J. Chen, "Effects of explanation strategy and autonomy of explainable AI on human–AI collaborative decision-making," International Journal of Social Robotics, vol. 16, pp. 791–810, 2024.

[26] S. Lin et al., "(When) are contrastive explanations of reinforcement learning helpful?," arXiv preprint arXiv:2211.07719, 2022.

[27] S. Bhaskara et al., "Understanding the influence of AI autonomy on AI explainability levels in human-AI teams using a mixed methods approach," Cognition, Technology & Work, vol. 26, pp. 435–455, 2024.

[28] M. Naiseh, D. Al-Thani, N. Jiang, and R. Ali, "How the different explanation classes impact trust calibration: The case of clinical decision support systems," International Journal of Human-Computer Studies, vol. 169, 102941, 2023.

[29] C. Marx, Y. Park, H. Hasson, Y. Wang, S. Ermon, and L. Huan, "But are you sure? An uncertainty-aware perspective on explainable AI," in Proc. 26th Int. Conf. on Artificial Intelligence and Statistics (AISTATS), PMLR vol. 206, 2023.

[30] H. Kaur, H. Nori, S. Jenkins, R. Caruana, H. Wallach, and J. Wortman Vaughan, "Interpreting interpretability: Understanding data scientists' use of interpretability tools for machine learning," in Proc. CHI Conf. on Human Factors in Computing Systems, 2020, pp. 1–14.

[31] M. Nourani, C. Roy, J. E. Block, D. R. Honeycutt, T. Rahman, E. D. Ragan, and V. Gogate, "Anchoring bias affects mental model formation and user reliance in explainable AI systems," in Proc. 26th Int. Conf. on Intelligent User Interfaces (IUI), 2021, pp. 340–350.

[32] X. Zhang and P. Robinette, "Trust miscalibration is sometimes necessary: An empirical study and a computational model," Frontiers in Psychology, vol. 12, 690089, 2021.

[33] R. El-Assady et al., "Facilitating trust calibration in artificial intelligence-driven diagnostic decision support systems for determining physicians' diagnostic accuracy: Quasi-experimental study," JMIR Formative Research, vol. 8, e58666, 2024.

[34] U. Bhatt et al., "Explainable machine learning in deployment," in Proc. ACM Conf. on Fairness, Accountability, and Transparency (FAT*), 2020, pp. 648–657.

[35] Q. V. Liao and K. R. Varshney, "Human-centered explainable AI (XAI): From algorithms to user experiences," arXiv preprint arXiv:2110.10790, 2021.

[36] Y. Rong et al., "Towards human-centered explainable AI: A survey of user studies for model explanations," IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 46, no. 4, pp. 2104–2122, 2024.

[37] M. Naiseh, D. Al-Thani, N. Jiang, and R. Ali, "Explainable recommendation: When design meets trust calibration," World Wide Web, vol. 24, pp. 1857–1884, 2021.

[38] A. R. Panganiban, G. Matthews, and M. D. Long, "Transparency in autonomous teammates: Intention to support as teaming information," Journal of Cognitive Engineering and Decision Making, vol. 14, no. 2, pp. 174–190, 2020.

[39] T. Grushin et al., "Operator-agnostic and real-time usable psychophysiological models of trust, workload, and situation awareness," Frontiers in Computer Science, vol. 7, 1549399, 2025.

[40] Booz Allen Hamilton, "Large language models in space—and beyond: Deploying an LLM aboard the International Space Station," Technical report, 2024.

[41] O. Bensch et al., "Enhancing procedure management for the International Space Station using retrieval-augmented generation and knowledge graphs," in Proc. SPAICE: AI in and for Space (ESA/DLR), 2024.

[42] K. Zhuang et al., "2024 NASA SUITS report: LLM-driven immersive augmented reality user interface for robotics and space exploration," arXiv preprint arXiv:2507.01206, 2025.

[43] N. Sánchez-Ortiz et al., "A review of spacecraft collision avoidance manoeuvre design methods," arXiv preprint arXiv:2503.22555, 2025.

[44] J. L. Gonzalo and C. Colombo, "On-board collision avoidance applications based on machine learning and analytical methods," in Proc. 8th European Conference on Space Debris (ESA), 2021.

[45] D. Shmueli et al., "AI-driven human-autonomy teaming in tactical operations: Proposed framework and future directions," arXiv preprint arXiv:2411.09788, 2024.

[46] P. Linardatos, V. Papastefanopoulos, and S. Kotsiantis, "Explainable AI: A review of machine learning interpretability methods," Entropy, vol. 23, no. 1, 18, 2021.
