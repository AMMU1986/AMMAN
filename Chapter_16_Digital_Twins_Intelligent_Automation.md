# DIGITAL TWINS AND INTELLIGENT AUTOMATION FOR INDUSTRY 5.0

@AUTHORS Rajanish Kumar Kaushal, Amman Jakhar, and Sachin Kalsi

## Abstract

The convergence of digital twin technology and intelligent automation is reshaping the industrial landscape as manufacturing transitions from the efficiency-driven paradigm of Industry 4.0 towards the human-centric, resilient, and sustainable vision of Industry 5.0. A digital twin is a high-fidelity virtual representation of a physical asset, process, or system that is synchronised with its physical counterpart through continuous bidirectional data exchange, enabling real-time monitoring, simulation, prediction, and optimisation across the asset lifecycle. Intelligent automation extends conventional automation by embedding artificial intelligence, machine learning, and autonomous decision-making into cyber-physical systems, allowing them to sense, reason, and act with limited human intervention. This chapter provides a structured examination of how these two technologies jointly underpin the Industry 5.0 agenda. It begins by tracing the conceptual origins and reference architecture of digital twins, then surveys the enabling technologies of intelligent automation, including the industrial Internet of Things, edge and cloud computing, and data-driven modelling. The chapter articulates the defining principles of Industry 5.0—human-centricity, resilience, and sustainability—and contrasts them with the preceding paradigm. It then analyses the integration of digital twins with intelligent automation as a closed-loop system that couples perception, cognition, and action, and reviews representative applications spanning smart manufacturing, predictive maintenance, supply-chain resilience, healthcare, and energy. Finally, the chapter addresses the principal technical, organisational, and ethical challenges—interoperability, data governance, cybersecurity, trust, and workforce transformation—and outlines future research directions. The discussion offers scholars and practitioners a coherent framework for understanding how synchronised virtual models and autonomous intelligence are enabling a more humane and adaptive industrial future.

**Keywords:** Digital twin; intelligent automation; Industry 5.0; human-centric manufacturing; cyber-physical systems; industrial Internet of Things; predictive maintenance; artificial intelligence; resilience; sustainability

## 1. Introduction

Manufacturing and the broader industrial economy are undergoing a profound transformation driven by the fusion of physical production systems with advanced digital capabilities. Central to this transformation is the digital twin, a concept first articulated as a virtual, digital equivalent of a physical product that mirrors its state and behaviour throughout the product lifecycle [1]. The idea was subsequently elaborated as a mechanism for mitigating unpredictable and undesirable emergent behaviour in complex systems by maintaining a continuously updated virtual counterpart that can be interrogated, simulated, and optimised without disturbing the physical asset [2]. Over the past decade, the digital twin has matured from an aerospace and product-lifecycle-management aspiration into a mainstream industrial technology adopted across sectors as diverse as manufacturing, energy, mobility, and healthcare [3].

The distinguishing feature of a genuine digital twin, as opposed to a static digital model, is the automated flow of data between the physical and virtual entities. A widely cited classification distinguishes the digital model, in which no automated data exchange exists; the digital shadow, in which data flow automatically from the physical to the virtual entity only; and the digital twin proper, in which data flow automatically in both directions so that changes in the virtual model can act back upon the physical system [4]. This bidirectional coupling is what allows a digital twin to move beyond passive visualisation towards active control and autonomous optimisation, and it is precisely this capability that connects digital twins to the agenda of intelligent automation.

Intelligent automation denotes the augmentation of traditional automation with artificial intelligence, enabling systems not merely to execute predetermined instructions but to perceive their environment, reason about alternatives, and adapt their behaviour to changing conditions. When a digital twin is coupled with intelligent automation, the resulting system can detect deviations, predict future states, evaluate candidate interventions in simulation, and enact the most favourable action, closing the loop between sensing and actuation. Realising such systems at scale, however, demands substantial enabling infrastructure, including pervasive sensing, high-bandwidth connectivity, scalable computation, and robust modelling techniques [5].

While Industry 4.0 emphasised automation, connectivity, and data-driven efficiency, a subsequent vision—Industry 5.0—has emerged that reorients technological progress around human well-being, societal resilience, and environmental sustainability. This chapter examines the intersection of digital twins and intelligent automation within this emerging paradigm. The remainder of the chapter is organised as follows. Section 2 establishes the conceptual foundations and reference architecture of digital twins. Section 3 characterises the transition from Industry 4.0 to Industry 5.0. Section 4 discusses human-centricity and the human-cyber-physical perspective. Section 5 analyses the enabling technologies and the integration of digital twins with intelligent automation. Section 6 reviews applications, and Section 7 addresses challenges and future directions before the chapter concludes.

## 2. Foundations and Architecture of Digital Twins

### 2.1 Concept, Definitions, and Evolution

Although the intuition behind the digital twin predates the term, its modern formulation is attributed to early product-lifecycle-management work that envisioned a virtual counterpart mirroring a physical product across its entire lifecycle [1, 2]. Since then, the research community has produced numerous definitions that, despite differences in emphasis, converge on a small set of essential attributes: a physical entity, a virtual counterpart, and the data and information connections that bind them [6]. A systematic characterisation of the digital twin identifies these connections, together with the fidelity of the virtual model and the frequency of synchronisation, as the parameters that determine how faithfully the twin represents its physical origin [6]. From a modelling perspective, the value of a digital twin derives from its ability to integrate physics-based simulation with data-driven learning, yielding hybrid models that are both interpretable and adaptive [7].

Comprehensive surveys have mapped the definitions, characteristics, and design implications of digital twins across domains, noting that the concept is applied at widely varying scopes, from a single component to an entire factory or city [8]. Systematic literature reviews further reveal that the term is often used loosely, encompassing everything from detailed engineering simulations to lightweight dashboards, which has prompted calls for clearer terminology and maturity criteria [9]. A generalised characterisation frames the digital twin as comprising a physical reality, a virtual representation, and the bidirectional information flows connecting them, applicable across engineering and non-engineering disciplines alike [10]. This diversity of interpretation motivates the maturity-based classification summarised later in this section.

### 2.2 Reference Architecture

A widely adopted conceptual model describes the digital twin in terms of several interacting dimensions: the physical entity, the virtual entity, the services built upon the twin, the data that fuel it, and the connections that integrate these elements. Fig. 16-1 presents a layered reference architecture that organises these ideas into five tiers—physical, data-acquisition, communication, digital-modelling, and application—linked by bidirectional flows. At the physical layer reside the assets, machines, and processes instrumented with sensors and actuators. The data-acquisition layer captures signals and converts them into structured streams, while the communication layer transports data securely between the edge and higher tiers. The digital-modelling layer hosts the virtual counterpart together with simulation, analytics, and machine-learning services, and the application layer delivers monitoring, prediction, optimisation, and control functions to end users.

[[FIG:1]]
Fig. 16-1. Five-layer reference architecture of a digital twin, showing bidirectional data flow between the physical asset and the virtual model.

The architecture depicted in Fig. 16-1 emphasises the closed-loop nature of a mature digital twin: insights generated in the digital-modelling layer are not merely visualised but are fed back as control decisions to the physical layer. This feedback path is the technical basis for intelligent automation and is revisited in Section 5. The extent to which a given implementation realises this loop varies considerably, which is why practitioners find it useful to distinguish levels of digital-twin maturity.

### 2.3 Types and Maturity Levels

Digital twins can be classified by the degree of integration between the physical and virtual entities, ranging from disconnected digital models through one-way digital shadows to fully coupled digital twins [4]. They can also be classified by scope—product, process, or system—and by lifecycle stage, from design and manufacturing to operation and service. Table 16-1 organises these distinctions into a maturity framework that spans descriptive, diagnostic, predictive, and prescriptive capabilities, culminating in the autonomous twin that can act upon its physical counterpart without routine human intervention. This progression parallels the broader analytics maturity ladder and provides a practical vocabulary for assessing where a given deployment sits.

Table 16-1. Maturity levels of digital twins and their defining capabilities.

| Maturity Level | Data Integration | Core Capability | Human Role | Representative Example |
|----------------|------------------|-----------------|-----------|------------------------|
| Digital model | Manual, no automatic link | Static representation and documentation | Full manual control | As-designed CAD model |
| Digital shadow | One-way, physical to virtual | Real-time monitoring and visualisation | Human interprets data | Live condition dashboard |
| Predictive twin | One-way with analytics | Forecasting of future states | Human decides on alerts | Remaining-useful-life estimation |
| Prescriptive twin | Bidirectional, advisory | Recommends optimal interventions | Human approves actions | Optimised maintenance scheduling |
| Autonomous twin | Bidirectional, closed-loop | Self-optimising control | Human sets goals and bounds | Self-adjusting production cell |

As Table 16-1 indicates, the transition from a digital shadow to an autonomous twin corresponds to a progressive delegation of decision authority from humans to the system, mirroring the closed-loop architecture introduced above. The higher maturity levels are unattainable without the analytical and control capabilities supplied by intelligent automation, underscoring the interdependence of the two technologies that this chapter addresses. Contemporary reviews confirm that most industrial deployments remain at the digital-shadow or predictive stage, with fully autonomous twins still comparatively rare [3, 5].

## 3. From Industry 4.0 to Industry 5.0

### 3.1 The Industry 4.0 Paradigm

The fourth industrial revolution, commonly termed Industry 4.0, was conceived as the pervasive digitalisation and interconnection of manufacturing through cyber-physical systems, the Internet of Things, and data analytics [11]. It built upon a set of enabling technologies—autonomous robots, simulation, horizontal and vertical system integration, the industrial Internet of Things, cloud computing, additive manufacturing, augmented reality, big data, and cybersecurity—that together promised substantial gains in productivity and flexibility [12]. A foundational architectural principle was the five-level structure for cyber-physical systems, progressing from smart connection through data-to-information conversion, cyber modelling, cognition, and configuration, which provided an implementation blueprint for connected factories [13].

Industry 4.0 reframed manufacturing as an intelligent, data-rich activity in which physical processes are continuously monitored and optimised through their digital representations [14]. The economic case was compelling, and consultancy analyses forecast significant improvements in productivity, revenue growth, and employment associated with the adoption of the nine enabling technologies [15]. Nevertheless, as implementation matured, observers noted that the paradigm's emphasis on efficiency and automation tended to marginalise the human operator and paid limited attention to environmental and social sustainability, prompting a re-examination of industrial priorities [16].

### 3.2 The Emergence of Industry 5.0

Industry 5.0 emerged as a complementary and corrective vision that retains the technological capabilities of Industry 4.0 while explicitly foregrounding three values: human-centricity, resilience, and sustainability [16]. Rather than positioning technology as an end in itself, Industry 5.0 treats it as a means to serve human well-being and societal goals, restoring the human operator to a central role alongside intelligent machines [17]. Policy formulations have articulated this vision as an industry that is sustainable, human-centric, and resilient, capable of respecting planetary boundaries while placing worker well-being at the heart of the production process [18].

Scholarly treatments have examined both the prospects and the retrospective lessons of this transition, situating Industry 5.0 as an evolution rather than a replacement of its predecessor [19]. Surveys of enabling technologies identify collaborative robots, the digital twin, edge computing, 6G and beyond, and human-machine collaboration frameworks as the technical pillars that will realise the Industry 5.0 vision [20]. Fig. 16-2 summarises the conceptual shift, depicting the three pillars of Industry 5.0 rising from the technological foundation established by Industry 4.0. The figure highlights that the new paradigm does not discard automation and connectivity but augments them with human values and systemic robustness.

[[FIG:2]]
Fig. 16-2. Conceptual transition from Industry 4.0 to Industry 5.0, showing the three defining pillars of human-centricity, resilience, and sustainability built upon the Industry 4.0 technological base.

The relationship between the two paradigms is one of co-existence and hybridisation rather than abrupt succession, a point emphasised by comparative analyses of the two models [21]. A viability-oriented framework integrates resilience, sustainability, and human-centricity into a unified perspective, arguing that these dimensions are mutually reinforcing rather than competing objectives [22]. Complementary work frames Industry 5.0 as a humanisation and greening of Industry 4.0, and stresses the ethical and value-oriented engineering practices required to design the factory of the future responsibly [23, 24]. Table 16-2 contrasts the salient characteristics of the two paradigms across several dimensions to make the distinction concrete.

Table 16-2. Comparison of Industry 4.0 and Industry 5.0 across key dimensions.

| Dimension | Industry 4.0 | Industry 5.0 |
|-----------|--------------|--------------|
| Primary driver | Efficiency and automation | Human well-being and value |
| Human role | Operator supervised by systems | Collaborator empowered by systems |
| Core objective | Productivity and flexibility | Human-centricity, resilience, sustainability |
| Technology focus | Connectivity and data analytics | Human-machine collaboration and cognition |
| Sustainability | Implicit, secondary | Explicit, central |
| Robots | Autonomous industrial robots | Collaborative robots working with people |
| Success metric | Cost and throughput | Well-being, adaptability, environmental impact |

The contrasts in Table 16-2 show that Industry 5.0 does not abandon the digital infrastructure of Industry 4.0 but reorients its purpose. Notably, the digital twin appears in both paradigms, yet its role expands under Industry 5.0 from an efficiency instrument to an enabler of human-centred decision support and sustainable operation, a theme developed in the following sections. This reorientation is consistent with the human-centric emphasis of the comparison above and motivates the human-cyber-physical perspective discussed next.

## 4. Human-Centricity and the Human-Cyber-Physical Perspective

A defining commitment of Industry 5.0 is the elevation of the human operator from a supervised resource to an empowered collaborator whose skills, creativity, and judgement are amplified by intelligent systems [17]. This commitment is formalised in the concept of human-cyber-physical systems, which extends the cyber-physical systems of Industry 4.0 by explicitly incorporating the human as an integral element of the system rather than an external supervisor [25]. In this view, the human, the cyber component, and the physical component form a tightly coupled triad in which cognitive tasks are shared and dynamically allocated according to their respective strengths.

The human-cyber-physical framework distinguishes between the physical execution of tasks, the cyber processing of information, and the human provision of insight, intuition, and ethical judgement [26]. Digital twins occupy a natural place within this framework as the cyber medium through which humans perceive and influence physical processes. By presenting an intuitive, continuously updated representation of a physical system, a digital twin enhances situational awareness and enables operators to explore the consequences of decisions in simulation before committing them to the physical world. As illustrated earlier in Fig. 16-2, human-centricity is not opposed to automation; rather, it repositions automation as a partner that offloads repetitive or hazardous work while reserving high-value cognitive and creative tasks for people.

This human-centred orientation has direct implications for the design of intelligent automation. Systems must be transparent, explaining their reasoning in terms that operators can understand and trust; they must be controllable, allowing humans to intervene and override; and they must be inclusive, accommodating the diverse capabilities of the workforce. The ethical dimension is equally important, requiring that value-sensitive considerations be embedded into engineering decisions from the outset rather than retrofitted [24]. These requirements shape the integration architecture presented in the next section.

## 5. Enabling Technologies and the Integration of Digital Twins with Intelligent Automation

### 5.1 Enabling Technologies

Realising digital twins coupled with intelligent automation depends on a stack of mutually reinforcing technologies. Big-data infrastructure provides the capacity to store and process the high-velocity streams generated by instrumented assets, and a comparative analysis of digital twins and big data in the context of smart manufacturing highlights their complementary roles in achieving closed-loop optimisation [27]. Data-driven smart manufacturing frameworks demonstrate how the digital twin serves as the integrating hub that unifies design, production, and service data [28]. A systematic account of the enabling technologies and tools for digital twins identifies modelling, simulation, data management, connectivity, and services as the principal building blocks that must be orchestrated [29].

Connectivity is provided by the industrial Internet of Things, and a survey of digital twins in the Internet-of-Things context details the technical features, scenarios, and architectural models that arise when twins are embedded in pervasively connected environments [30]. Simulation is a further cornerstone, and the simulation aspect of the digital twin has been analysed as the means by which virtual models reproduce and anticipate physical behaviour [31]. In design and production engineering, the digital twin has been shaped into a comprehensive representation that supports both geometric and behavioural fidelity [32]. Table 16-3 organises the principal enabling technologies and their specific contributions to the digital-twin-plus-automation stack.

Table 16-3. Principal enabling technologies for digital twins and intelligent automation.

| Technology | Function in the Stack | Contribution to Intelligent Automation |
|------------|-----------------------|----------------------------------------|
| Industrial Internet of Things | Sensing and connectivity | Supplies real-time data for perception |
| Edge and cloud computing | Distributed computation | Balances latency and scalability of analytics |
| Artificial intelligence and machine learning | Modelling and inference | Enables prediction and autonomous decisions |
| Physics-based simulation | Virtual experimentation | Evaluates interventions before actuation |
| Big-data platforms | Storage and processing | Handles high-velocity heterogeneous streams |
| Digital-twin middleware | Synchronisation and services | Maintains fidelity and exposes control interfaces |
| Collaborative robotics | Physical actuation | Executes decisions safely alongside humans |

As Table 16-3 makes clear, no single technology is sufficient in isolation; the value emerges from their integration. Artificial intelligence and machine learning supply the inferential capacity that transforms a monitoring twin into a decision-making one, while edge and cloud computing furnish the computational substrate that allows analytics to run at appropriate latencies. Together these technologies populate the digital-modelling and application layers on which the integration loop depends.

### 5.2 The Integration Loop

The integration of digital twins with intelligent automation is best understood as a perception-cognition-action loop that continuously synchronises the physical and virtual worlds. Fig. 16-3 depicts this closed loop: sensors on the physical asset feed data to the virtual model, which maintains an up-to-date estimate of the asset's state; analytical and machine-learning services within the twin interpret this state, predict its evolution, and evaluate candidate actions in simulation; and the selected action is transmitted back to the physical asset through actuators, whereupon the cycle repeats. Human operators supervise the loop, setting goals and constraints and intervening when necessary, consistent with the human-centric principles discussed in Section 4.

[[FIG:3]]
Fig. 16-3. The perception-cognition-action loop that integrates a digital twin with intelligent automation, showing continuous synchronisation and human oversight.

The loop illustrated in Fig. 16-3 generalises across application domains and maturity levels. At lower maturity, the action step is advisory and mediated by a human; at higher maturity, it becomes autonomous within predefined bounds, corresponding to the prescriptive and autonomous stages of the maturity ladder. Early demonstrations of realising the cyber-physical production system through a digital twin established the practical feasibility of this coupling [33], and reviews of the roles of the digital twin within cyber-physical production systems confirm that such bidirectional coupling is what enables proactive rather than reactive operation [34]. Surveys of manufacturing applications document how such loops reduce downtime, improve quality, and increase throughput by allowing the system to anticipate and pre-empt problems [35]. Comprehensive reviews of concepts, technologies, and industrial applications reinforce that the maturity of the integration loop is the primary determinant of the value realised [36]. Emerging service-oriented approaches, such as delivering the digital twin as a cloud service, further lower the barrier to implementing the loop by abstracting infrastructure concerns [37]. The realisation of the loop in a manufacturing setting is exemplified by digital-twin-driven smart manufacturing frameworks that connect the connotation, reference model, and applications of the technology [38].

## 6. Applications

Digital twins integrated with intelligent automation have been applied across a broad range of industrial contexts, and the value they deliver depends strongly on the maturity of the integration loop discussed in Section 5. Predictive and preventive maintenance is among the most mature application areas; a dedicated review of digital twins for maintenance documents how synchronised virtual models forecast component degradation and schedule interventions before failures occur [39]. In discrete manufacturing, the integration of part data into a shop-floor digital twin enables fine-grained traceability and adaptive process control [40]. Systematisation studies of the digital-twin concept in industry confirm that manufacturing remains the dominant application domain, followed by energy, mobility, and healthcare [41].

Beyond the factory floor, digital twins support resilience at the scale of entire supply networks. A digital supply-chain twin has been shown to help manage disruption risks and enhance resilience, a capability of heightened importance under the Industry 5.0 emphasis on robustness [42]. Related work frames the digital twin as an instrument for sustainable manufacturing supply chains, proposing implementation frameworks that align operational optimisation with environmental objectives [43]. Fig. 16-4 summarises representative benefits reported across application domains, expressed as indicative improvements in downtime, quality, and resource efficiency. Table 16-4 complements the figure by mapping specific application domains to the digital-twin functions they exploit and the outcomes they target.

[[FIG:4]]
Fig. 16-4. Indicative benefits of integrating digital twins with intelligent automation across representative performance dimensions.

Table 16-4. Application domains for digital twins with intelligent automation.

| Application Domain | Primary Digital-Twin Function | Intelligent-Automation Role | Targeted Outcome |
|--------------------|-------------------------------|-----------------------------|------------------|
| Smart manufacturing | Process modelling and control | Adaptive scheduling and quality control | Higher throughput and quality |
| Predictive maintenance | Condition monitoring and prognosis | Automated intervention scheduling | Reduced unplanned downtime |
| Supply-chain management | Network-level simulation | Disruption detection and re-planning | Improved resilience |
| Energy systems | Asset performance modelling | Load balancing and optimisation | Greater efficiency and lower emissions |
| Healthcare | Patient or device modelling | Decision support and personalisation | Improved safety and outcomes |

As Fig. 16-4 and Table 16-4 together illustrate, the benefits are broad but contingent on domain-specific factors such as data availability, model fidelity, and the acceptable degree of autonomy. Healthcare applications, for instance, typically operate at advisory maturity because of the high stakes involved, whereas maintenance applications more readily support autonomous action. This variation reinforces the maturity perspective introduced earlier and the human-oversight principles of Section 4.

## 7. Challenges and Future Directions

Despite rapid progress, several challenges must be addressed before digital twins coupled with intelligent automation can be deployed pervasively and responsibly. Interoperability remains a persistent obstacle, as heterogeneous assets, protocols, and data formats impede the seamless integration on which the twin depends. The influential call to "make more digital twins" is therefore tempered by the recognition that their proliferation must be matched by rigorous validation and verification if the resulting decisions are to be relied upon [44]. Data governance is equally critical, encompassing data quality, ownership, privacy, and the lineage required to trust model outputs; comprehensive treatments of digital-twin theory and practice identify standardisation and semantic interoperability as persistent open research questions [45].

Cybersecurity is a further concern, because the bidirectional connectivity that gives a digital twin its power also expands the attack surface of the physical system it controls. The closed-loop coupling between virtual and physical entities implies that a compromised virtual model could issue harmful control actions, making security an intrinsic rather than peripheral requirement. Trust and explainability are prerequisites for human acceptance, consistent with the human-centric commitments of Industry 5.0; operators must understand and be able to override autonomous decisions. Workforce transformation presents an organisational challenge, as the shift towards human-machine collaboration demands new skills and thoughtful change management rather than simple substitution of labour.

Looking ahead, several research directions are prominent. The integration of large-scale artificial-intelligence models with physics-based twins promises hybrid systems that combine broad reasoning with domain fidelity. Federated and edge-based architectures will enable twins to operate under bandwidth and privacy constraints. Standardised reference models and maturity assessments, building on the maturity classifications discussed earlier, will help organisations benchmark and advance their deployments. Above all, the Industry 5.0 agenda calls for research that keeps human well-being, resilience, and sustainability at the centre of technological design, ensuring that increasingly autonomous systems remain aligned with human values [22, 24].

## 8. Conclusion

This chapter has examined the convergence of digital twins and intelligent automation as a cornerstone of the emerging Industry 5.0 paradigm. Beginning from the origins and reference architecture of the digital twin, it showed how the bidirectional coupling between physical and virtual entities, elaborated in the five-layer architecture of Fig. 16-1 and the maturity framework of Table 16-1, provides the foundation for autonomous, self-optimising systems. The transition from Industry 4.0 to Industry 5.0, contrasted in Table 16-2 and depicted in Fig. 16-2, reorients these capabilities around the values of human-centricity, resilience, and sustainability. The integration of digital twins with intelligent automation, formalised as the perception-cognition-action loop of Fig. 16-3 and supported by the enabling technologies of Table 16-3, transforms passive monitoring into proactive and autonomous operation. Applications across manufacturing, maintenance, supply chains, energy, and healthcare, surveyed in Fig. 16-4 and Table 16-4, demonstrate substantial but context-dependent benefits. Realising the full promise of these technologies will require sustained attention to interoperability, data governance, cybersecurity, trust, and workforce transformation, guided throughout by the human-centred ethos of Industry 5.0. As virtual models and autonomous intelligence become ever more capable, their responsible integration offers a path towards an industrial future that is not only more productive but also more resilient, sustainable, and humane.

## References

[1] Grieves, Michael. 2014. "Digital Twin: Manufacturing Excellence through Virtual Factory Replication." White Paper, Florida Institute of Technology.

[2] Grieves, Michael, and John Vickers. 2017. "Digital Twin: Mitigating Unpredictable, Undesirable Emergent Behavior in Complex Systems." In Transdisciplinary Perspectives on Complex Systems, edited by Franz-Josef Kahlen, Shannon Flumerfelt, and Anabela Alves, 85-113. Cham: Springer.

[3] Tao, Fei, He Zhang, Ang Liu, and Andrew Y. C. Nee. 2019. "Digital Twin in Industry: State-of-the-Art." IEEE Transactions on Industrial Informatics 15 (4): 2405-2415.

[4] Kritzinger, Werner, Matthias Karner, Georg Traar, Jan Henjes, and Wilfried Sihn. 2018. "Digital Twin in Manufacturing: A Categorical Literature Review and Classification." IFAC-PapersOnLine 51 (11): 1016-1022.

[5] Fuller, Aidan, Zhong Fan, Charles Day, and Chris Barlow. 2020. "Digital Twin: Enabling Technologies, Challenges and Open Research." IEEE Access 8: 108952-108971.

[6] Jones, David, Chris Snider, Aydin Nassehi, Jason Yon, and Ben Hicks. 2020. "Characterising the Digital Twin: A Systematic Literature Review." CIRP Journal of Manufacturing Science and Technology 29: 36-52.

[7] Rasheed, Adil, Omer San, and Trond Kvamsdal. 2020. "Digital Twin: Values, Challenges and Enablers from a Modeling Perspective." IEEE Access 8: 21980-22012.

[8] Barricelli, Barbara Rita, Elena Casiraghi, and Daniela Fogli. 2019. "A Survey on Digital Twin: Definitions, Characteristics, Applications, and Design Implications." IEEE Access 7: 167653-167671.

[9] Semeraro, Concetta, Mario Lezoche, Hervé Panetto, and Michele Dassisti. 2021. "Digital Twin Paradigm: A Systematic Literature Review." Computers in Industry 130: 103469.

[10] VanDerHorn, Eric, and Sankaran Mahadevan. 2021. "Digital Twin: Generalization, Characterization and Implementation." Decision Support Systems 145: 113524.

[11] Lasi, Heiner, Peter Fettke, Hans-Georg Kemper, Thomas Feld, and Michael Hoffmann. 2014. "Industry 4.0." Business & Information Systems Engineering 6 (4): 239-242.

[12] Xu, Li Da, Eric L. Xu, and Ling Li. 2018. "Industry 4.0: State of the Art and Future Trends." International Journal of Production Research 56 (8): 2941-2962.

[13] Lee, Jay, Behrad Bagheri, and Hung-An Kao. 2015. "A Cyber-Physical Systems Architecture for Industry 4.0-Based Manufacturing Systems." Manufacturing Letters 3: 18-23.

[14] Zhong, Ray Y., Xun Xu, Eberhard Klotz, and Stephen T. Newman. 2017. "Intelligent Manufacturing in the Context of Industry 4.0: A Review." Engineering 3 (5): 616-630.

[15] Rüßmann, Michael, Markus Lorenz, Philipp Gerbert, Manuela Waldner, Jan Justus, Pascal Engel, and Michael Harnisch. 2015. "Industry 4.0: The Future of Productivity and Growth in Manufacturing Industries." Boston Consulting Group.

[16] Xu, Xun, Yuqian Lu, Birgit Vogel-Heuser, and Lihui Wang. 2021. "Industry 4.0 and Industry 5.0-Inception, Conception and Perception." Journal of Manufacturing Systems 61: 530-535.

[17] Nahavandi, Saeid. 2019. "Industry 5.0-A Human-Centric Solution." Sustainability 11 (16): 4371.

[18] Breque, Maija, Lars De Nul, and Athanasios Petridis. 2021. Industry 5.0: Towards a Sustainable, Human-Centric and Resilient European Industry. Luxembourg: Publications Office of the European Union, European Commission, Directorate-General for Research and Innovation.

[19] Leng, Jiewu, Weinan Sha, Baicun Wang, Pai Zheng, Cunbo Zhuang, Qiang Liu, Thorsten Wuest, Dimitris Mourtzis, and Lihui Wang. 2022. "Industry 5.0: Prospect and Retrospect." Journal of Manufacturing Systems 65: 279-295.

[20] Maddikunta, Praveen Kumar Reddy, Quoc-Viet Pham, Prabadevi B, N. Deepa, Kapal Dev, Thippa Reddy Gadekallu, Rukhsana Ruby, and Madhusanka Liyanage. 2022. "Industry 5.0: A Survey on Enabling Technologies and Potential Applications." Journal of Industrial Information Integration 26: 100257.

[21] Golovianko, Mariia, Vagan Terziyan, Vladyslav Branytskyi, and Diana Malyk. 2023. "Industry 4.0 vs. Industry 5.0: Co-Existence, Transition, or a Hybrid." Procedia Computer Science 217: 102-113.

[22] Ivanov, Dmitry. 2023. "The Industry 5.0 Framework: Viability-Based Integration of the Resilience, Sustainability, and Human-Centricity Perspectives." International Journal of Production Research 61 (5): 1683-1695.

[23] Grabowska, Sandra, Sebastian Saniuk, and Bożena Gajdzik. 2022. "Industry 5.0: Improving Humanization and Sustainability of Industry 4.0." Scientometrics 127 (6): 3117-3144.

[24] Longo, Francesco, Antonio Padovano, and Steven Umbrello. 2020. "Value-Oriented and Ethical Technology Engineering in Industry 5.0: A Human-Centric Perspective for the Design of the Factory of the Future." Applied Sciences 10 (12): 4182.

[25] Wang, Baicun, Pai Zheng, Yue Yin, Albert Shan, and Li Zheng. 2022. "Toward Human-Centric Smart Manufacturing: A Human-Cyber-Physical Systems (HCPS) Perspective." Journal of Manufacturing Systems 63: 471-490.

[26] Zhou, Ji, Yinghui Zhou, Baicun Wang, and Jiyuan Zang. 2019. "Human-Cyber-Physical Systems (HCPSs) in the Context of New-Generation Intelligent Manufacturing." Engineering 5 (4): 624-636.

[27] Qi, Qinglin, and Fei Tao. 2018. "Digital Twin and Big Data towards Smart Manufacturing and Industry 4.0: 360 Degree Comparison." IEEE Access 6: 3585-3593.

[28] Tao, Fei, Meng Zhang, and Andrew Y. C. Nee. 2019. Digital Twin Driven Smart Manufacturing. London: Academic Press.

[29] Qi, Qinglin, Fei Tao, Tianliang Hu, Nabil Anwer, Ang Liu, Yongli Wei, Lihui Wang, and Andrew Y. C. Nee. 2021. "Enabling Technologies and Tools for Digital Twin." Journal of Manufacturing Systems 58: 3-21.

[30] Minerva, Roberto, Gyu Myoung Lee, and Noel Crespi. 2020. "Digital Twin in the IoT Context: A Survey on Technical Features, Scenarios, and Architectural Models." Proceedings of the IEEE 108 (10): 1785-1824.

[31] Boschert, Stefan, and Roland Rosen. 2016. "Digital Twin-The Simulation Aspect." In Mechatronic Futures, edited by Peter Hehenberger and David Bradley, 59-74. Cham: Springer.

[32] Schleich, Benjamin, Nabil Anwer, Luc Mathieu, and Sandro Wartzack. 2017. "Shaping the Digital Twin for Design and Production Engineering." CIRP Annals 66 (1): 141-144.

[33] Uhlemann, Thomas H.-J., Christian Lehmann, and Rolf Steinhilper. 2017. "The Digital Twin: Realizing the Cyber-Physical Production System for Industry 4.0." Procedia CIRP 61: 335-340.

[34] Negri, Elisa, Luca Fumagalli, and Marco Macchi. 2017. "A Review of the Roles of Digital Twin in CPS-Based Production Systems." Procedia Manufacturing 11: 939-948.

[35] Cimino, Chiara, Elisa Negri, and Luca Fumagalli. 2019. "Review of Digital Twin Applications in Manufacturing." Computers in Industry 113: 103130.

[36] Liu, Mengnan, Shuiliang Fang, Huiyue Dong, and Cunzhi Xu. 2021. "Review of Digital Twin about Concepts, Technologies, and Industrial Applications." Journal of Manufacturing Systems 58: 346-361.

[37] Aheleroff, Shohin, Xun Xu, Ray Y. Zhong, and Yuqian Lu. 2021. "Digital Twin as a Service (DTaaS) in Industry 4.0: An Architecture Reference Model." Advanced Engineering Informatics 47: 101225.

[38] Lu, Yuqian, Chao Liu, Kevin I-Kai Wang, Huiyue Huang, and Xun Xu. 2020. "Digital Twin-Driven Smart Manufacturing: Connotation, Reference Model, Applications and Research Issues." Robotics and Computer-Integrated Manufacturing 61: 101837.

[39] Errandonea, Itxaro, Sergio Beltrán, and Saioa Arrizabalaga. 2020. "Digital Twin for Maintenance: A Literature Review." Computers in Industry 123: 103316.

[40] Coronado, Pedro Daniel Urbina, Roby Lynn, Wafa Louhichi, Mahmoud Parto, Ethan Wescoat, and Thomas Kurfess. 2018. "Part Data Integration in the Shop Floor Digital Twin: Mobile and Cloud Technologies to Enable a Manufacturing Execution System." Journal of Manufacturing Systems 48: 25-33.

[41] Sjarov, Martin, Tobias Lechler, Jonathan Fuchs, Matthias Brossog, Andreas Selmaier, Florian Faltus, Thorbjörn Donhauser, and Jörg Franke. 2020. "The Digital Twin Concept in Industry-A Review and Systematization." In 2020 25th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA), 1789-1796.

[42] Ivanov, Dmitry, and Alexandre Dolgui. 2021. "A Digital Supply Chain Twin for Managing the Disruption Risks and Resilience in the Era of Industry 4.0." Production Planning & Control 32 (9): 775-788.

[43] Kamble, Sachin S., Angappa Gunasekaran, Harsh Parekh, Venkatesh Mani, Amine Belhadi, and Rohit Sharma. 2022. "Digital Twin for Sustainable Manufacturing Supply Chains: Current Trends, Future Perspectives, and an Implementation Framework." Technological Forecasting and Social Change 176: 121448.

[44] Tao, Fei, and Qinglin Qi. 2019. "Make More Digital Twins." Nature 573 (7775): 490-491.

[45] Sharma, Ashutosh, Elias Kosasih, Jie Zhang, Alexandra Brintrup, and Anisoara Calinescu. 2022. "Digital Twins: State of the Art Theory and Practice, Challenges, and Open Research Questions." Journal of Industrial Information Integration 30: 100383.
