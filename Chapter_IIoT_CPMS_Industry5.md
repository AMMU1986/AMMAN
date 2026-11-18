# INDUSTRIAL INTERNET OF THINGS AND CYBER-PHYSICAL MANUFACTURING SYSTEMS: FOUNDATIONS, ARCHITECTURES AND PATHWAYS FOR INDUSTRY 5.0

**Book:** Robotics and Adaptive Manufacturing Systems in Industry 5.0: Integrating Intelligence, Connectivity, and Automation (Apple Academic Press)

**Series:** AAP Advances in Materials, Manufacturing and Computational Intelligence Techniques

**Authors:** Amman Jakhar¹,* and Sachin Kalsi¹

¹ Department of Mechanical Engineering, Chandigarh University, Mohali, Punjab-140301, India

*Corresponding author: Amman Jakhar, Email: ammanjakhar5000734@gmail.com

## Abstract

This chapter presents a comprehensive exploration of the Industrial Internet of Things (IIoT) and Cyber-Physical Manufacturing Systems (CPMS) as foundational pillars of Industry 5.0. The chapter systematically examines the architectural, technological, and operational dimensions that enable seamless convergence of physical manufacturing processes with digital intelligence. Beginning with foundational concepts, the chapter progresses through enabling technologies, architectural frameworks, real-world applications, and emerging challenges. Particular emphasis is placed on how IIoT-enabled cyber-physical systems facilitate adaptive, human-centric, and sustainable manufacturing paradigms characteristic of Industry 5.0.

**Keywords:** Industrial Internet of Things; Cyber-physical manufacturing systems; Industry 5.0; Edge computing; Digital twin; Human-centric manufacturing

## Introduction

Manufacturing is changing from a sequence of isolated machines into a network of connected, sensing and computing assets. Sensors now report the condition of spindles, motors and robots many times per second. Controllers exchange data with plant software and with cloud platforms. Software models of machines and processes run alongside the physical equipment and suggest, or even execute, corrective actions. The Industrial Internet of Things (IIoT) provides the connectivity and data layer for this change, while Cyber-Physical Manufacturing Systems (CPMS) provide the control logic that closes the loop between data and physical action.

These technologies were first promoted under the banner of Industry 4.0, with a strong focus on efficiency, automation and cost. The European Commission's concept of Industry 5.0 adds three further goals: production should be human-centric, sustainable and resilient [1]. Industry 5.0 does not replace Industry 4.0 technologies. It changes the purpose for which they are deployed and the values against which their success is judged [2]. A connected factory is no longer judged only by output per hour but also by how well it supports its workers, how much energy and material it uses, and how quickly it recovers from disruption [3].

This chapter explains how IIoT and CPMS support these goals. Section 1 sets out the concepts and architectures. Section 2 describes the enabling technologies for communication, edge computing, data management and security. Section 3 discusses applications in adaptive, human-centric and sustainable production. Section 4 examines implementation challenges, standards and maturity models, and then outlines emerging trends and research needs. The chapter closes with conclusions for engineers, managers and researchers. Four figures and four tables summarise the main frameworks.

## 1. Foundations of Industrial Internet of Things and Cyber-Physical Systems

### 1.1 Conceptual Evolution: From IoT to IIoT in Manufacturing Contexts

#### 1.1.1 Definitions and scope

The Internet of Things describes a world in which everyday objects carry identifiers, sensors and network connections so that they can exchange data and be controlled remotely [4]. Consumer IoT applications, such as smart thermostats, wearables and home assistants, typically value convenience, low unit cost and ease of setup. A delayed message or a dropped connection is an inconvenience but rarely a safety hazard.

The Industrial Internet of Things applies the same principles to production machinery, process plants, energy systems and logistics. Its requirements are very different. Industrial deployments need deterministic timing, high availability, long equipment lifetimes, functional safety and protection against cyberattacks that could damage equipment or injure people [5]. Boyes and colleagues define IIoT as a system of networked smart objects, cyber-physical assets, generic information technologies and optional cloud or edge platforms that enable real-time, intelligent and autonomous access, collection, analysis, communication and exchange of process, product and service information within the industrial environment [6]. Enterprise IoT lies between the two. It covers connected assets in offices, buildings and fleets, where reliability matters but hard real-time control is uncommon.

#### 1.1.2 Historical development

IIoT did not emerge from nothing. From the 1970s onwards, supervisory control and data acquisition (SCADA) systems and distributed control systems (DCS) collected data from remote terminal units and programmable logic controllers (PLCs) and presented it to operators. These systems were proprietary, closed and organised in strict hierarchies. During the 1990s and 2000s, fieldbuses and industrial Ethernet replaced point-to-point wiring, and manufacturing execution systems (MES) linked shop-floor data with business planning. Survey work on IoT in industry traces how radio-frequency identification, wireless sensor networks and service-oriented architectures gradually opened these hierarchies and allowed devices to publish data more freely [7]. IIoT is the result of this convergence: industrial devices that speak open, internet-compatible protocols, while still meeting the timing and safety requirements of automation.

#### 1.1.3 The transition from Industry 4.0 to Industry 5.0

The German Industrie 4.0 initiative, launched in 2011 and formalised in 2013, described a smart factory in which cyber-physical systems communicate across the value chain and production becomes flexible enough to make individualised products at mass-production cost [8]. Early implementations emphasised automation and efficiency. Critics noted that this focus risked treating workers as a cost to be minimised rather than as a source of creativity and judgement. Nahavandi argued that the next stage would bring humans and machines back together, with robots and intelligent systems taking over repetitive and dangerous tasks while people focus on customisation, problem-solving and oversight [9]. The European Commission's Industry 5.0 policy document made this human-centric orientation explicit and added sustainability and resilience as equal goals [1]. In this framing, IIoT provides the data that allows factories to measure worker wellbeing, energy use and supply-chain risk, as well as throughput.

#### 1.1.4 Key characteristics

Hermann, Pentek and Otto identified a set of design principles that remain useful for describing IIoT systems [10]. Interoperability allows machines, devices, sensors and people to communicate through shared standards. Virtualisation creates a digital copy of the factory by linking sensor data with simulation models. Decentralisation lets individual cyber-physical systems make decisions locally. Real-time capability allows data to be collected and analysed quickly enough to react to failures or changing orders. Service orientation exposes functions of machines and software as services that other systems can call. Modularity allows production systems to be reconfigured by adding or replacing modules. Table 1 compares how these characteristics differ between consumer IoT, enterprise IoT and IIoT.

Table 1. Comparison of consumer IoT, enterprise IoT and Industrial IoT

| Attribute | Consumer IoT | Enterprise IoT | Industrial IoT (IIoT) |
|---|---|---|---|
| Typical assets | Wearables, home appliances, personal devices | Building systems, fleets, office equipment | Machine tools, robots, PLCs, process plant, drives |
| Timing requirements | Best effort; seconds acceptable | Near real time; sub-second desirable | Deterministic; often under 1 ms for motion control |
| Availability target | Moderate; restarts tolerated | High during business hours | Very high; continuous operation, planned downtime only |
| Lifetime of devices | 2 to 5 years | 5 to 10 years | 15 to 30 years, with legacy equipment in service |
| Safety implications | Low | Moderate | High; failures can injure people or damage equipment |
| Security priority | Confidentiality and privacy | Confidentiality and integrity | Availability and integrity first, then confidentiality |
| Typical protocols | Wi-Fi, Bluetooth, HTTP | Wi-Fi, LTE, MQTT, HTTP | EtherCAT, PROFINET, TSN, OPC UA, MQTT, 5G |
| Governing standards | Consumer product regulations | IT management frameworks | IEC 62443, IEC 61508, ISA-95, RAMI 4.0 |

#### 1.1.5 Convergence with operational technology

Information technology (IT) and operational technology (OT) grew up separately. IT manages data, applications and business processes. OT monitors and controls physical equipment. The two domains differ in culture as well as technology. IT updates software frequently and accepts restarts, while OT values stability and may run the same controller software for decades. IT security puts confidentiality first, while OT puts availability and safety first. IIoT forces these domains together, because data must flow from field devices to enterprise analytics and decisions must flow back to the shop floor. Wollschlaeger, Sauter and Jasperneite describe how this convergence is replacing the strict automation pyramid with flatter, service-based networks in which field devices can communicate directly with higher-level systems [11]. The opportunity is better use of data. The challenge is that every new connection is also a potential path for faults and attacks.

### 1.2 Cyber-Physical Manufacturing Systems: Architecture and Core Principles

#### 1.2.1 Definition and taxonomy

Lee defined cyber-physical systems as integrations of computation with physical processes, in which embedded computers and networks monitor and control physical processes, usually with feedback loops where physical processes affect computations and vice versa [12]. In manufacturing, a CPMS links machines, products, materials and people with computational models and communication networks. Monostori and colleagues describe cyber-physical production systems as autonomous and cooperative elements and subsystems that are connected with each other across all levels of production, from processes through machines up to production and logistics networks [13].

CPMS can be classified along several dimensions. By scope, they range from a single smart machine, through a production cell or line, to a whole factory and a networked supply chain. By function, they include monitoring systems, control systems, optimisation systems and self-organising systems. By the degree of human involvement, they range from systems that only inform operators to systems that act without human approval. These dimensions are useful when designing or comparing implementations.

#### 1.2.2 The 5C architecture

Lee, Bagheri and Kao proposed a five-level architecture that has become a widely used guide for building CPMS [14]. Figure 1 shows the five levels. At the Connection level, data are acquired reliably from machines, controllers and enterprise systems. At the Conversion level, raw signals are turned into meaningful information, for example by extracting features that indicate machine health. At the Cyber level, a digital model of each machine is built, and machines are compared with each other to detect unusual behaviour. At the Cognition level, the combined information is presented to experts and decision support is provided. At the Configuration level, decisions are fed back to the physical system so that it can adjust, reconfigure or optimise itself.

The 5C model is useful because it separates concerns. A plant can achieve a solid Connection level without advanced analytics, and it can add higher levels step by step. It also makes clear that value increases towards the top of the pyramid, while data volume decreases as raw signals are condensed into decisions.

[Insert Figure 1 here]

Figure 1. The 5C architecture for cyber-physical manufacturing systems, showing the five levels from Connection to Configuration and the main function at each level. Adapted from the concept of Lee, Bagheri and Kao [14]; drawn by the authors.

#### 1.2.3 Feedback control loops and latency

A CPMS is built around feedback loops. Sensors measure a physical quantity, such as temperature, vibration or position. The measurement is transmitted, processed and compared with a target. A controller then sends a command to an actuator, which changes the physical process. The time taken for this cycle determines what the loop can control. Servo motion control may need cycle times below one millisecond, with very small variation known as jitter. Process temperature control may tolerate cycles of seconds. Production scheduling may run every few minutes or hours.

The placement of computation therefore follows the timing requirement. Loops that require hard real-time behaviour must stay close to the machine, usually in PLCs, motion controllers or edge devices. Loops that optimise over longer horizons can run in plant servers or in the cloud. A common design error is to route time-critical decisions through networks or platforms that cannot guarantee delivery times. Good CPMS design treats latency, jitter and reliability as explicit requirements for each loop.

#### 1.2.4 Digital-physical synchronisation

The cyber part of a CPMS is only useful if it reflects the current state of the physical system. A digital twin is a virtual representation of a physical asset, process or system that is kept up to date with data from its physical counterpart [15]. Kritzinger and colleagues distinguish three levels of integration [16]. In a digital model, data are exchanged manually between physical and digital objects. In a digital shadow, data flow automatically from the physical object to the digital one, but not back. In a digital twin, data flow automatically in both directions, so that changes in the model can change the physical system. Synchronisation requires consistent identifiers for assets, time stamps that can be compared across systems, and data models that describe what each value means. Without these, a twin gradually drifts from reality and its predictions become unreliable.

#### 1.2.5 Reference architectures

Reference architectures help organisations structure complex systems and use a common vocabulary. The Reference Architecture Model Industrie 4.0 (RAMI 4.0) describes an asset in a three-dimensional space [17]. The first axis covers six layers, from the physical asset through integration, communication, information and functional layers up to the business layer. The second axis follows the life cycle of a product type and its individual instances, from development to maintenance and recycling. The third axis represents the hierarchy levels of the factory, from product and field device to the connected world. The Industrial Internet Reference Architecture (IIRA) of the Industry IoT Consortium takes a more general, cross-industry perspective [18]. It describes IIoT systems through business, usage, functional and implementation viewpoints, and divides functions into control, operations, information, application and business domains. RAMI 4.0 is more detailed for manufacturing assets, while IIRA is broader and easier to apply across sectors. Both are compatible, and many projects use RAMI 4.0 to model assets and IIRA to structure system-level concerns.

#### 1.2.6 Levels of autonomy

The autonomy of a CPMS can be described as a sequence of levels. At the lowest level, the system monitors and displays data, and all decisions are made by people. At the next level, it diagnoses problems and recommends actions. A higher level allows it to execute actions within limits that people have set, for example by adjusting feed rates within an approved range. At the highest level, the system configures and optimises itself, coordinating with other systems to reach goals. Leitão, Colombo and Karnouskos review prototypes that show how multi-agent and service-oriented approaches allow distributed CPS components to cooperate and adapt [19]. In Industry 5.0, the aim is not maximum autonomy in every case but appropriate autonomy, in which humans retain oversight of decisions that affect safety, quality and working conditions.

## 2. Enabling Technologies and Architectural Frameworks

### 2.1 Communication Protocols, Networking, and Edge Intelligence

#### 2.1.1 Industrial communication protocols

No single protocol meets every industrial requirement, so IIoT systems combine several. Modbus, introduced in 1979, remains common because it is simple and widely supported, but it has no built-in security and a limited data model. PROFINET and EtherCAT are industrial Ethernet protocols designed for real-time control. EtherCAT processes frames on the fly as they pass through each device, which allows very short cycle times for motion control. PROFINET offers several performance classes, including isochronous real-time communication for demanding applications.

OPC Unified Architecture (OPC UA) addresses a different need. It is a platform-independent, service-oriented framework that combines data transport with a rich information model and built-in security functions such as authentication, signing and encryption [20]. OPC UA allows a machine to describe not only a value but also what the value means, its units and its relationship to other data. Message Queuing Telemetry Transport (MQTT) is a lightweight publish-subscribe protocol that moves data efficiently from many devices to central brokers, which makes it popular for edge-to-cloud communication. The OPC UA PubSub extension can use MQTT as a transport, combining semantic richness with efficient distribution.

Time-sensitive networking (TSN) is a set of IEEE 802.1 standards that adds deterministic timing to standard Ethernet [21]. TSN provides time synchronisation, traffic scheduling and frame pre-emption, so that time-critical control traffic and ordinary IT traffic can share the same network without interfering. Combined with OPC UA, TSN could reduce the need for separate proprietary fieldbuses. Table 2 compares the main protocols.

Table 2. Comparison of major industrial communication protocols for IIoT and CPMS

| Protocol | Communication model | Typical latency or cycle time | Built-in security | Typical role in IIoT |
|---|---|---|---|---|
| Modbus (RTU/TCP) | Master-slave, request-response | Milliseconds to tens of milliseconds | None in original specification | Legacy device access, simple sensors and meters |
| PROFINET | Provider-consumer, real-time Ethernet | About 1 ms (IRT classes below 1 ms) | Security classes being added | Field-level control in factory automation |
| EtherCAT | Master-slave, on-the-fly frame processing | Below 100 µs possible | Limited; relies on network segmentation | High-speed motion control, robotics |
| OPC UA (client-server) | Service-oriented, request-response | Tens of milliseconds | Authentication, signing, encryption | Semantic data exchange between machines, MES and edge |
| OPC UA PubSub over TSN | Publish-subscribe, deterministic | Sub-millisecond with TSN scheduling | As OPC UA, with network-level guarantees | Converged field-to-cloud communication |
| MQTT | Publish-subscribe via broker | Tens to hundreds of milliseconds | TLS transport encryption; broker authentication | Telemetry from devices and edge to cloud |
| 5G (URLLC, mMTC) | Cellular wireless | Target 1 ms air interface for URLLC | 3GPP security architecture | Mobile robots, AGVs, wireless sensors, flexible layouts |

#### 2.1.2 Network architecture considerations

Industrial networks are organised in layers. At the field level, sensors, actuators and controllers communicate over deterministic networks. At the edge level, gateways and edge servers collect data from many devices, translate protocols and run local analytics. At the plant level, MES, historians and site-level twins coordinate production. At the cloud level, enterprise systems, large-scale analytics and model training take place. Figure 2 shows this layered architecture together with typical latencies and protocols. The general trade-off is that higher layers offer more computing power, storage and context, while lower layers offer lower latency, more deterministic behaviour and better data locality.

[Insert Figure 2 here]

Figure 2. Layered IIoT architecture across the edge-cloud continuum, showing typical functions, protocols and latency ranges at the field, edge, fog (plant) and cloud levels. Drawn by the authors based on [11], [20], [21] and [22].

#### 2.1.3 5G and beyond in manufacturing

Wireless communication allows flexible factory layouts in which machines and mobile robots can be moved without rewiring. Fifth-generation (5G) mobile networks were designed with industrial use cases in mind. Ultra-reliable low-latency communication (URLLC) targets air-interface latencies of about one millisecond with very high reliability, which makes wireless control of some machines feasible. Massive machine-type communication (mMTC) supports very large numbers of low-power devices per square kilometre, suitable for dense sensor networks. Private 5G networks allow manufacturers to control coverage, capacity and security on their own sites. Varga and colleagues review the challenges of using 5G for IIoT, including integration with existing industrial networks, guaranteed end-to-end latency and the cost and complexity of deployment [22]. Research on sixth-generation (6G) networks aims at even lower latency, integrated sensing and communication, and native support for artificial intelligence.

#### 2.1.4 Edge computing paradigms

Edge computing moves computation close to where data are produced [23]. In manufacturing, this reduces latency for time-critical analytics, saves network bandwidth by sending only processed results upward, and keeps sensitive process data on site. Fog computing, introduced by Bonomi and colleagues, describes a layer of distributed computing resources between devices and the cloud that can host applications across many locations [24]. Mist computing pushes very light processing into sensors and controllers themselves. In practice, these terms describe points on a continuum rather than sharply separated layers.

#### 2.1.5 The edge-cloud continuum

Deciding where to run each workload is a design task. Workloads that require responses within a few milliseconds, such as vision-based quality inspection on a fast line, belong at the edge. Workloads that require large data sets and heavy computation, such as training a machine-learning model on data from several plants, belong in the cloud. Many workloads are split: a model is trained in the cloud, deployed to the edge for inference, and retrained when its performance drifts. Privacy and data sovereignty also matter. Some manufacturers do not allow raw process data to leave their premises, which favours edge processing and federated learning, in which models are trained locally and only model updates are shared.

#### 2.1.6 Interoperability and semantic integration

Connecting devices is not enough. Systems must also agree on what data mean. The Asset Administration Shell (AAS) is the Industrie 4.0 approach to this problem [25]. It is a standardised digital representation of an asset that contains submodels describing different aspects, such as technical data, documentation, operational data and maintenance information. A digital nameplate submodel, for example, holds the manufacturer, type, serial number and certifications of a device in a machine-readable form. OPC UA companion specifications define common information models for particular machine types, such as robots or machine tools, so that a client can understand any compliant machine without custom programming. Semantic integration reduces the cost of connecting new equipment and is a precondition for plug-and-produce systems.

### 2.2 Data Management, Analytics, and Security in Cyber-Physical Manufacturing

#### 2.2.1 Industrial data acquisition

Manufacturing data come from many sources: vibration, temperature, current and acoustic sensors on machines; controller variables such as positions, speeds and alarms; vision systems; energy meters; and enterprise systems that record orders, materials and quality results. Sampling rates vary from several kilohertz for vibration analysis to once per shift for some quality records. Data acquisition design must decide what to measure, how often, and with what accuracy. Retrofitting legacy machines with external sensors and edge gateways is often the most economical way to begin, because it avoids changes to certified control systems.

#### 2.2.2 Data architecture and storage

Time-series databases store sensor data efficiently and support fast queries over time ranges. Data lakes store large volumes of raw and processed data in many formats for later analysis. Data warehouses hold structured data for reporting. Federated data architectures allow data to remain in separate systems, or with separate organisations, while still being queried or used for model training through common interfaces. Tao and colleagues describe how data-driven smart manufacturing depends on managing the full life cycle of manufacturing data, from collection and storage through processing, visualisation and application [26].

#### 2.2.3 Real-time stream processing

Many manufacturing decisions must be made while data are still arriving. Stream processing frameworks analyse data continuously as events, rather than storing them first and analysing them later. Typical tasks include filtering, aggregation over sliding time windows, detection of threshold violations and correlation of events from different sources. Stream processing can run on edge devices for local decisions and in the cloud for plant-wide or fleet-wide views.

#### 2.2.4 Machine learning for manufacturing intelligence

Machine learning has become a core tool for turning manufacturing data into decisions [27]. Supervised learning uses labelled examples to predict outcomes such as product quality, tool wear or remaining useful life. Unsupervised learning finds patterns without labels and is widely used for anomaly detection, where a model learns normal behaviour and flags deviations. Reinforcement learning learns control policies by trial and reward and is being explored for robot motion, process parameter tuning and scheduling. Deep learning methods are well suited to images, sound and high-frequency signals. Practical challenges include the scarcity of labelled failure data, changes in process conditions that make models drift, and the need to explain model decisions to engineers and operators.

#### 2.2.5 Cybersecurity frameworks

Connecting OT to IT networks exposes industrial systems to attacks. The Stuxnet worm, which damaged uranium enrichment centrifuges by manipulating PLC code while showing operators normal values, demonstrated that cyberattacks can cause physical damage [28]. The NIST guide to operational technology security describes how to protect industrial control systems while respecting their performance, reliability and safety requirements [29]. A central principle is defence in depth: several layers of protection, including network segmentation, firewalls, access control, device hardening, monitoring and incident response, so that the failure of one layer does not compromise the whole system.

The IEC 62443 series is the main international standard family for industrial automation and control system security [30]. It divides systems into zones of equal security requirements, connected by conduits through which communication is controlled. It defines security levels from protection against casual violation up to protection against sophisticated, well-resourced attackers, and it sets requirements for asset owners, system integrators and product suppliers. Zero-trust architecture adds the principle that no device or user is trusted by default, even inside the network perimeter, and that every access request must be authenticated and authorised [31]. Applying zero trust in OT is challenging because legacy devices often cannot support modern authentication, but it can be implemented at gateways and conduits.

#### 2.2.6 Safety-security co-engineering

Functional safety and cybersecurity were traditionally handled by separate teams and standards. Functional safety, governed by standards such as IEC 61508, protects against hazards caused by random hardware failures and systematic faults. Cybersecurity protects against intentional attacks. In connected systems, a cyberattack can disable a safety function, and a security measure, such as a forced software update, can interfere with safe operation. Safety-security co-engineering analyses both kinds of risk together, so that hazard analyses consider attack scenarios and security measures are checked for safety effects.

#### 2.2.7 Data governance and privacy

IIoT raises questions about who owns machine data. A machine builder may want data from its machines in customer plants to improve its products, while the plant operator may regard the same data as revealing its production secrets. Contracts and data-sharing frameworks must define ownership, access and use. Human-centric applications add privacy concerns, because wearables and cameras can collect personal data about workers. Data protection laws require a lawful basis, purpose limitation, data minimisation and transparency. Good practice is to anonymise or aggregate worker data where possible, involve workers' representatives in design, and use such data to improve safety and wellbeing rather than for surveillance.

## 3. Applications and Implementation in Industry 5.0 Manufacturing

### 3.1 IIoT-Enabled Adaptive Manufacturing and Human-Centric Production

#### 3.1.1 Adaptive production systems

Customers increasingly expect personalised products delivered quickly. Adaptive production systems respond to this demand by changing what they make, how they make it and in what order, without long changeovers. IIoT supports adaptation by providing current information about orders, machine availability, tool condition and material stocks. Kusiak describes smart manufacturing as the use of data, models and connectivity to make production more responsive, with decisions informed by real-time information rather than fixed plans [32]. Reconfigurable machines, modular lines and mobile robots provide the physical flexibility, while IIoT and CPMS provide the information and control needed to use it.

#### 3.1.2 Real-time process optimisation

Closed-loop optimisation uses IIoT data to adjust process parameters during production. In machining, cutting forces and vibration can be monitored to adjust feed rates, avoiding chatter and tool breakage while maintaining productivity. In injection moulding, pressure and temperature profiles can be adjusted to compensate for changes in material batches. In welding, sensors can detect deviations in the seam and adjust the torch path. These applications move quality control from inspection after the fact to prevention during production.

#### 3.1.3 Predictive maintenance integration

Predictive maintenance uses condition data to estimate when equipment is likely to fail, so that maintenance can be scheduled before failure but not unnecessarily early. Prognostics and health management methods extract health indicators from signals, model degradation and estimate remaining useful life [33]. The full value of predictive maintenance appears only when predictions are integrated with production planning. A maintenance task that is predicted for next week can be scheduled during a planned changeover, and orders can be routed to other machines in the meantime. This integration requires that maintenance systems, MES and scheduling tools share data through common interfaces.

#### 3.1.4 Human-in-the-loop systems

Industry 5.0 places workers at the centre of production. Romero and colleagues introduced the concept of the Operator 4.0, a worker whose physical, sensory and cognitive abilities are enhanced by technology [34]. Their typology includes the augmented operator supported by augmented reality, the strong operator supported by exoskeletons, the smarter operator supported by intelligent personal assistants, the healthy operator supported by wearable trackers, and the collaborative operator working with robots. IIoT links these technologies to production data. An augmented reality headset can show the next assembly step for the specific product variant on the line. An exoskeleton can adapt its support to the task. Cognitive load can be estimated from interaction patterns or physiological signals, and the system can adjust the pace or the amount of information shown.

#### 3.1.5 Worker safety and wellbeing

IIoT can improve safety by detecting hazardous conditions and alerting workers before harm occurs. Wearable sensors can monitor heart rate, skin temperature and posture to detect heat stress, fatigue or ergonomic risk. Environmental sensors can monitor noise, air quality and temperature. Location systems can warn workers who approach moving machinery or restricted zones. These applications must be designed with workers' consent and with clear limits on how data are used, as discussed in Section 2.2.7.

#### 3.1.6 Collaborative robotics integration

Collaborative robots, or cobots, work alongside people without fixed safety fences. Villani and colleagues review the safety requirements, interaction methods and applications of human-robot collaboration in industry [35]. Safe collaboration depends on sensing and communication: the robot must know where people are, how fast it may move, and what force it may apply. IIoT infrastructure supports this by connecting cobots with safety scanners, vision systems and production systems, and by providing the data needed to assign tasks between humans and robots according to their strengths. Figure 3 shows how sensing, analysis, decision, action and human operators are combined into an adaptive loop around a digital twin.

[Insert Figure 3 here]

Figure 3. Human-centric adaptive manufacturing loop enabled by IIoT. Sensing, analysis, decision and action are coordinated through a digital twin and CPMS decision layer, with the human operator as an active participant supported by augmented reality, wearables and exoskeletons. Drawn by the authors based on [14], [32], [34] and [35].

#### 3.1.7 Case studies

The World Economic Forum's Global Lighthouse Network, developed with McKinsey & Company, recognises factories that have deployed Fourth Industrial Revolution technologies at scale and achieved measurable improvements [36]. Lighthouse sites in discrete manufacturing, such as automotive, electronics and machinery, have used IIoT-based monitoring, predictive maintenance, digital twins and advanced analytics to raise productivity, shorten lead times and reduce defects. Sites in process industries, such as chemicals, pharmaceuticals and steel, have used IIoT data and machine learning to optimise process parameters, energy use and yield. A common feature of successful sites is that they combine technology with changes in organisation and skills, so that workers are trained to use the new tools and are involved in designing them. The network's more recent selections also recognise sustainability results, reflecting the Industry 5.0 shift in goals.

### 3.2 Sustainability, Resilience, and Circular Economy Integration

#### 3.2.1 Energy management and optimisation

Energy is a major cost and a major source of emissions in manufacturing. IIoT-based energy monitoring measures consumption at the level of individual machines and processes rather than only at the plant meter. This reveals waste, such as machines left idling, compressed air leaks and inefficient sequencing. Energy data can be combined with production schedules to shift flexible loads to periods of lower prices or lower carbon intensity, a practice known as demand response. Over time, energy data can also inform equipment replacement decisions.

#### 3.2.2 Resource efficiency and waste reduction

Real-time tracking of materials through production reveals where scrap, rework and losses occur. Weighing systems, vision and identification technologies can track material use for each order. Combined with process data, this allows engineers to find the causes of waste and to correct them quickly. Reducing waste lowers both cost and environmental impact.

#### 3.2.3 Carbon footprint monitoring

Companies face growing requirements to report greenhouse gas emissions. Scope 1 emissions come directly from company operations, Scope 2 from purchased energy, and Scope 3 from the rest of the value chain, including suppliers and product use. IIoT data provide measured values for Scope 1 and Scope 2 emissions at the level of products and processes, instead of estimates based on annual averages. For Scope 3, data exchange with suppliers through common data models allows product carbon footprints to be passed along the supply chain.

#### 3.2.4 Circular economy enablement

A circular economy keeps products and materials in use through repair, remanufacturing and recycling. Doing so requires information about each product's materials, condition and history. The digital product passport, a central element of European circular economy policy, provides a structured record of this information throughout the product life cycle [37]. IIoT data can feed the passport with information about how a product was made and how it has been used, and asset administration shells can provide the technical structure for passports of industrial products. At end of life, this information helps decide whether a product should be reused, remanufactured or recycled.

#### 3.2.5 Supply chain resilience

The COVID-19 pandemic, semiconductor shortages and transport disruptions showed how vulnerable global supply chains can be. IIoT improves visibility by tracking shipments, inventory and supplier capacity in real time. Ivanov and Dolgui describe the digital supply chain twin, a model of the supply network that uses real-time data to simulate disruptions and test responses, such as alternative suppliers, routes and inventory policies [38]. With such tools, companies can detect disruptions earlier and react faster.

#### 3.2.6 Predictive quality and zero-defect manufacturing

Zero-defect manufacturing aims to prevent defects rather than detect and scrap them. Psarommatis and colleagues describe four strategies: detection, repair, prediction and prevention [39]. IIoT supports all four. Sensors detect deviations as they occur. Data link defects to their causes so that repairs are targeted. Models predict when a process is drifting towards producing defects. Feedback loops adjust the process before defects appear. Zero-defect manufacturing is also a sustainability strategy, because every defect avoided saves the materials and energy used to make it.

#### 3.2.7 Sustainable operations case studies and resilience frameworks

Table 3 summarises how IIoT and CPMS applications contribute to Industry 5.0 goals, with the main enabling technologies and typical performance indicators. Resilience frameworks combine these applications with architectural choices. Edge computing allows plants to continue operating if cloud connections fail. Modular and reconfigurable lines can switch to alternative products. Remote monitoring and assistance, which expanded during the pandemic, allow experts to support sites without travelling. Digital supply chain twins help plan responses to shocks. Together, these measures help plants absorb disruption and recover quickly.

Table 3. IIoT and CPMS applications supporting the human-centric, sustainable and resilient goals of Industry 5.0

| Application | Industry 5.0 goal | Key enabling technologies | Typical performance indicators |
|---|---|---|---|
| Machine-level energy monitoring and demand response | Sustainability | Smart meters, edge analytics, MES integration | Energy per unit, peak demand, CO2 per unit |
| Real-time material tracking | Sustainability | RFID, vision, weighing systems, MES | Scrap rate, material yield, waste per unit |
| Product carbon footprint tracking | Sustainability | IIoT energy data, AAS, supplier data exchange | Scope 1, 2 and 3 emissions per product |
| Digital product passport | Sustainability (circularity) | AAS, unique identifiers, life-cycle data | Share of products reused, remanufactured or recycled |
| Predictive maintenance integrated with scheduling | Resilience | Condition sensors, PHM models, MES/APS | Unplanned downtime, overall equipment effectiveness |
| Digital supply chain twin | Resilience | Tracking, simulation, cloud analytics | Time to detect and recover from disruption |
| Zero-defect manufacturing | Sustainability and resilience | In-process sensing, ML, closed-loop control | First-pass yield, defects per million |
| AR-guided assembly | Human-centricity | AR headsets, MES, product data | Training time, assembly errors, worker satisfaction |
| Wearable safety and ergonomics monitoring | Human-centricity | Wearables, location systems, privacy-preserving analytics | Incident rate, ergonomic risk score |
| Human-robot collaboration | Human-centricity and resilience | Cobots, safety sensors, task allocation | Cycle time, worker strain, flexibility |

## 4. Challenges, Standards, and Future Directions

### 4.1 Implementation Challenges, Standards, and Maturity Assessment

#### 4.1.1 Technical challenges

The installed base of manufacturing equipment is old. Many machines have controllers that predate open protocols, and some have no network interface at all. Integrating these legacy systems requires retrofitted sensors, protocol converters and careful testing. Protocol heterogeneity adds complexity, because a single plant may use several fieldbuses, industrial Ethernet variants and IT protocols. Real-time guarantees are difficult to maintain when networks carry mixed traffic. Scalability is another concern: an approach that works for one line may fail when extended to thousands of devices across many sites, because of data volumes, device management and security administration.

#### 4.1.2 Organisational barriers

The most difficult barriers are often organisational. IIoT projects require skills in automation, networking, data science and cybersecurity that are rarely found in one team. IT and OT departments may have different priorities and reporting lines. Workers may fear that new technologies will be used to monitor them or replace them. Successful programmes invest in training, create cross-functional teams, involve workers early and communicate clearly about goals.

#### 4.1.3 Economic considerations

IIoT investments must compete for capital with other projects. Costs include sensors, networks, software, integration, security and training, as well as ongoing licences and maintenance. Benefits include reduced downtime, higher quality, lower energy and material use, and faster response to customers, but some benefits, such as resilience and worker wellbeing, are difficult to quantify. Return-on-investment frameworks should start with specific use cases that have measurable value, use pilots to verify assumptions, and include indirect benefits and avoided risks where possible.

#### 4.1.4 Standards landscape

Standards reduce integration costs and risks. IEC 62264, based on ISA-95, defines models and terminology for integrating enterprise and control systems, including the functional hierarchy and the information exchanged between business planning and manufacturing operations. ISO 23247 provides a framework for digital twins in manufacturing, covering principles, reference architecture, digital representation of manufacturing elements and information exchange [40]. RAMI 4.0, IIRA, the AAS specifications, OPC UA, TSN and IEC 62443 complete the core set discussed earlier. Table 4 summarises the main standards and frameworks and their practical uses.

Table 4. Key standards, reference architectures and maturity models for IIoT-CPMS implementation

| Standard or framework | Scope | Practical implication |
|---|---|---|
| RAMI 4.0 (DIN SPEC 91345) [17] | Three-dimensional reference model of layers, life cycle and hierarchy | Common structure for describing Industrie 4.0 assets and components |
| IIRA (Industry IoT Consortium) [18] | Cross-industry IIoT reference architecture with viewpoints | Structures system-level concerns and stakeholder requirements |
| IEC 62264 / ISA-95 | Enterprise-control system integration | Defines interfaces between ERP, MES and control layers |
| OPC UA (IEC 62541) [20] | Secure, semantic, platform-independent communication | Vendor-neutral data exchange and information models |
| IEEE 802.1 TSN [21] | Deterministic Ethernet | Converged networks carrying control and IT traffic |
| Asset Administration Shell [25] | Standardised digital representation of assets | Plug-and-produce integration and digital nameplates |
| IEC 62443 series [30] | Security of industrial automation and control systems | Zones, conduits, security levels and supplier requirements |
| ISO 23247 [40] | Digital twin framework for manufacturing | Reference architecture for twin implementation |
| acatech Industrie 4.0 Maturity Index [41] | Six-stage maturity model across resources, information systems, culture and organisation | Assessment of current state and target capabilities |
| IMPULS Industrie 4.0 Readiness [42] | Six-dimension readiness model with levels 0 to 5 | Quick self-assessment for small and medium-sized firms |

#### 4.1.5 Maturity models

Maturity models help organisations understand where they stand and what to do next. The acatech Industrie 4.0 Maturity Index defines six stages: computerisation, connectivity, visibility, transparency, predictive capacity and adaptability [41]. The first two stages lay the foundations of digitalisation. Visibility answers the question of what is happening, transparency explains why it is happening, predictive capacity forecasts what will happen, and adaptability allows the system to respond autonomously. The model assesses four structural areas: resources, information systems, organisational structure and culture. The IMPULS Industrie 4.0 Readiness model, developed for the German mechanical engineering association, assesses six dimensions, including strategy, smart factory, smart operations, smart products, data-driven services and employees, and assigns companies to readiness levels from outsider to top performer [42]. Other models exist, and the choice matters less than using one consistently to set targets and measure progress.

#### 4.1.6 Implementation roadmaps

A phased approach reduces risk. Figure 4 shows a roadmap aligned with the acatech maturity stages. In the assessment phase, the organisation evaluates its maturity, inventories OT assets and risks, and prioritises use cases by value and feasibility. In the pilot phase, it retrofits sensors and edge gateways on one line, defines data models using OPC UA and MQTT, and establishes IEC 62443 zones and conduits. In the integration phase, it connects the pilot with MES and ERP through ISA-95 interfaces, deploys a plant historian and digital twin, and trains the workforce. In the scaling phase, it rolls out proven solutions across sites, introduces closed-loop and self-optimising control, extends human-robot collaboration and tracks sustainability indicators. Human oversight is retained throughout.

[Insert Figure 4 here]

Figure 4. Phased IIoT-CPMS implementation roadmap aligned with the six stages of the acatech Industrie 4.0 Maturity Index [41], with assessment informed by the IMPULS readiness model [42]. Drawn by the authors.

#### 4.1.7 Risk management

Risks arise at technical, operational and strategic levels. Technical risks include integration failures, poor data quality and cyber vulnerabilities. Operational risks include production disruption during deployment and dependence on a few skilled staff. Strategic risks include vendor lock-in, investments in technologies that become obsolete, and failure to realise expected benefits. Mitigation strategies include pilots with clear success criteria, open standards to avoid lock-in, security by design, documentation and training to spread knowledge, and regular reviews of the programme against business goals.

### 4.2 Emerging Trends and Research Frontiers

#### 4.2.1 AI-native IIoT

Large language models and other foundation models are beginning to appear in manufacturing. They can answer questions about equipment manuals and maintenance records in natural language, generate draft PLC code or test cases, summarise shift reports and help operators diagnose faults. Generative models can also create synthetic data to train other models when real failure data are scarce. In an AI-native IIoT, these capabilities are designed into the architecture rather than added later, with models running at the edge as well as in the cloud. The main challenges are reliability, because generative models can produce plausible but wrong answers, and accountability, because responsibility for decisions must remain clear [3].

#### 4.2.2 Autonomous cyber-physical systems

Research is progressing towards systems that configure, optimise and repair themselves. Self-configuring systems would recognise new modules and integrate them automatically using semantic descriptions such as asset administration shells. Self-optimising systems would continuously adjust parameters to meet goals for quality, cost and energy. Self-healing systems would detect faults and reroute production or switch to backup functions. Multi-agent approaches, in which software agents represent machines, products and orders and negotiate with each other, remain an important route to such autonomy [19].

#### 4.2.3 Digital twin evolution

Digital twins are evolving from monitoring tools into predictive and autonomous systems. Future twins will combine physics-based and data-driven models, update themselves continuously, and be connected into networks of twins representing machines, lines, factories and supply chains [15]. Standards such as ISO 23247 and the AAS will be important for making twins from different vendors work together [40].

#### 4.2.4 Quantum computing implications

Quantum computing may in future solve some optimisation and simulation problems faster than classical computers. Bayerstadler and colleagues identify industrial applications including production scheduling, logistics optimisation, materials simulation and machine learning [43]. Most of these remain at an early research stage because current quantum hardware is limited. A more immediate implication concerns cryptography. Sufficiently powerful quantum computers could break widely used public-key algorithms, so industrial systems with long lifetimes should plan for migration to post-quantum cryptography.

#### 4.2.5 6G and advanced connectivity

Sixth-generation networks are expected to offer lower latency, higher reliability, integrated sensing and communication, and native support for distributed artificial intelligence. For manufacturing, these features could support wireless control of more demanding processes, precise localisation of tools and workers, and seamless operation of mobile robots across large sites [22].

#### 4.2.6 Cognitive manufacturing

Cognitive manufacturing describes systems that learn, reason and adapt not only at the level of individual machines but across the organisation. Such systems would combine knowledge from engineering, operations and business data, learn from experience across sites, and support people in complex decisions. This vision extends the Cognition and Configuration levels of the 5C architecture from machines to whole enterprises [14].

#### 4.2.7 Societal and ethical dimensions

Industry 5.0 explicitly recognises that technology must serve people and society [1]. IIoT and automation will change jobs. Some tasks will disappear, others will be transformed, and new roles will emerge in data analysis, system integration and human-machine coordination. Equity requires that workers have access to training and that the benefits of productivity gains are shared. Small and medium-sized enterprises need affordable access to technology and skills so that they are not left behind. Responsible innovation frameworks call for transparency about how systems make decisions, protection of worker privacy, involvement of workers in design, and attention to the environmental footprint of digital infrastructure itself [2].

#### 4.2.8 Research roadmap

Several research priorities follow from this review. First, methods are needed to guarantee end-to-end timing and reliability across heterogeneous networks that combine TSN, 5G and edge computing. Second, interoperable, standards-based digital twins must be developed that can be composed across vendors and life-cycle phases. Third, trustworthy artificial intelligence for manufacturing requires methods for explaining, verifying and certifying learning-based controllers. Fourth, human-centric design needs better measures of worker wellbeing and cognitive load, and methods for allocating tasks between humans and machines fairly. Fifth, sustainability requires accurate, product-level measurement of energy, emissions and material flows across supply chains. Sixth, security research must address legacy systems, post-quantum migration and the combined analysis of safety and security. Progress in each of these areas depends on collaboration between universities, technology suppliers, manufacturers and standards bodies.

## 5. Conclusion and Outlook

IIoT and CPMS form the technical foundation of Industry 5.0. IIoT connects machines, products, people and systems, while CPMS close the loop between data and physical action. This chapter traced the evolution from SCADA and DCS to open IIoT architectures, described the 5C architecture and reference models such as RAMI 4.0 and IIRA, and reviewed the protocols, networks, edge computing, data management and security measures on which implementations depend. It showed how these technologies enable adaptive production, predictive maintenance, human-centric work and human-robot collaboration, and how they support sustainability and resilience through energy management, material tracking, carbon accounting, digital product passports, supply chain twins and zero-defect manufacturing.

Three conclusions stand out. First, architecture matters: placing each control loop and workload at the right point in the edge-cloud continuum, and using open, semantic standards, determines whether a system can scale and evolve. Second, security and safety must be designed in from the start, following frameworks such as IEC 62443 and the principles of defence in depth and zero trust. Third, the goals of Industry 5.0 change how success is measured. A connected factory should be judged by its contribution to workers' safety and development, to environmental targets and to resilience, as well as by productivity.

For practitioners, the recommended path is to assess maturity, start with high-value pilots, build on open standards, invest in people as much as in technology, and scale step by step. For researchers, the priorities lie in guaranteed real-time performance across converged networks, interoperable digital twins, trustworthy artificial intelligence, human-centric design methods and accurate sustainability measurement. If these challenges are addressed, IIoT and CPMS can help build manufacturing systems that are not only more efficient but also more humane, sustainable and resilient.

## Declarations

**Funding:** The authors received no specific funding for this work.

**Conflict of interest:** The authors declare no conflict of interest.

**Permissions:** All figures are original works drawn by the authors. Figure 1 adapts a published concept [14] and is redrawn, not reproduced; no copyrighted third-party images are included.

**Use of artificial intelligence:** [Authors to complete in line with the publisher's policy. If AI tools were used to assist with drafting, editing or figure generation, state the tool and the purpose here. The authors remain fully responsible for the accuracy, originality and integrity of the content.]

## References

[1] Breque M, De Nul L, Petridis A. Industry 5.0: Towards a Sustainable, Human-Centric and Resilient European Industry. Brussels: European Commission, Directorate-General for Research and Innovation; 2021.

[2] Xu X, Lu Y, Vogel-Heuser B, Wang L. Industry 4.0 and Industry 5.0—Inception, conception and perception. J Manuf Syst. 2021;61:530–535.

[3] Leng J, Sha W, Wang B, Zheng P, Zhuang C, Liu Q, Wuest T, Mourtzis D, Wang L. Industry 5.0: Prospect and retrospect. J Manuf Syst. 2022;65:279–295.

[4] Atzori L, Iera A, Morabito G. The Internet of Things: A survey. Comput Netw. 2010;54(15):2787–2805.

[5] Sisinni E, Saifullah A, Han S, Jennehag U, Gidlund M. Industrial Internet of Things: Challenges, opportunities, and directions. IEEE Trans Ind Inform. 2018;14(11):4724–4734.

[6] Boyes H, Hallaq B, Cunningham J, Watson T. The industrial internet of things (IIoT): An analysis framework. Comput Ind. 2018;101:1–12.

[7] Xu LD, He W, Li S. Internet of Things in industries: A survey. IEEE Trans Ind Inform. 2014;10(4):2233–2243.

[8] Kagermann H, Wahlster W, Helbig J. Recommendations for Implementing the Strategic Initiative INDUSTRIE 4.0: Final Report of the Industrie 4.0 Working Group. Frankfurt am Main: acatech – National Academy of Science and Engineering; 2013.

[9] Nahavandi S. Industry 5.0—A human-centric solution. Sustainability. 2019;11(16):4371.

[10] Hermann M, Pentek T, Otto B. Design principles for Industrie 4.0 scenarios. In: Proceedings of the 49th Hawaii International Conference on System Sciences (HICSS). IEEE; 2016. p. 3928–3937.

[11] Wollschlaeger M, Sauter T, Jasperneite J. The future of industrial communication: Automation networks in the era of the Internet of Things and Industry 4.0. IEEE Ind Electron Mag. 2017;11(1):17–27.

[12] Lee EA. Cyber physical systems: Design challenges. In: Proceedings of the 11th IEEE International Symposium on Object and Component-Oriented Real-Time Distributed Computing (ISORC). IEEE; 2008. p. 363–369.

[13] Monostori L, Kádár B, Bauernhansl T, Kondoh S, Kumara S, Reinhart G, Sauer O, Schuh G, Sihn W, Ueda K. Cyber-physical systems in manufacturing. CIRP Ann. 2016;65(2):621–641.

[14] Lee J, Bagheri B, Kao HA. A cyber-physical systems architecture for Industry 4.0-based manufacturing systems. Manuf Lett. 2015;3:18–23.

[15] Tao F, Zhang H, Liu A, Nee AYC. Digital twin in industry: State-of-the-art. IEEE Trans Ind Inform. 2019;15(4):2405–2415.

[16] Kritzinger W, Karner M, Traar G, Henjes J, Sihn W. Digital twin in manufacturing: A categorical literature review and classification. IFAC-PapersOnLine. 2018;51(11):1016–1022.

[17] Deutsches Institut für Normung (DIN). DIN SPEC 91345:2016-04. Reference Architecture Model Industrie 4.0 (RAMI4.0). Berlin: Beuth Verlag; 2016.

[18] Industrial Internet Consortium. The Industrial Internet of Things, Volume G1: Reference Architecture. Version 1.9. Industrial Internet Consortium; 2019.

[19] Leitão P, Colombo AW, Karnouskos S. Industrial automation based on cyber-physical systems technologies: Prototype implementations and challenges. Comput Ind. 2016;81:11–25.

[20] Mahnke W, Leitner SH, Damm M. OPC Unified Architecture. Berlin: Springer; 2009.

[21] Finn N. Introduction to time-sensitive networking. IEEE Commun Stand Mag. 2018;2(2):22–28.

[22] Varga P, Peto J, Franko A, Balla D, Haja D, Janky F, Soos G, Ficzere D, Maliosz M, Toka L. 5G support for Industrial IoT applications—Challenges, solutions, and research gaps. Sensors. 2020;20(3):828.

[23] Shi W, Cao J, Zhang Q, Li Y, Xu L. Edge computing: Vision and challenges. IEEE Internet Things J. 2016;3(5):637–646.

[24] Bonomi F, Milito R, Zhu J, Addepalli S. Fog computing and its role in the Internet of Things. In: Proceedings of the First Edition of the MCC Workshop on Mobile Cloud Computing. ACM; 2012. p. 13–16.

[25] Plattform Industrie 4.0. Specification: Details of the Asset Administration Shell, Part 1—The Exchange of Information between Partners in the Value Chain of Industrie 4.0. Version 3.0RC02. Berlin: Federal Ministry for Economic Affairs and Climate Action; 2022.

[26] Tao F, Qi Q, Liu A, Kusiak A. Data-driven smart manufacturing. J Manuf Syst. 2018;48:157–169.

[27] Wuest T, Weimer D, Irgens C, Thoben KD. Machine learning in manufacturing: Advantages, challenges, and applications. Prod Manuf Res. 2016;4(1):23–45.

[28] Langner R. Stuxnet: Dissecting a cyberwarfare weapon. IEEE Secur Priv. 2011;9(3):49–51.

[29] Stouffer K, Pease M, Tang C, Zimmerman T, Pillitteri V, Lightman S, et al. Guide to Operational Technology (OT) Security. NIST Special Publication 800-82 Rev. 3. Gaithersburg, MD: National Institute of Standards and Technology; 2023.

[30] International Electrotechnical Commission (IEC). IEC 62443-3-3:2013. Industrial communication networks—Network and system security—Part 3-3: System security requirements and security levels. Geneva: IEC; 2013.

[31] Rose S, Borchert O, Mitchell S, Connelly S. Zero Trust Architecture. NIST Special Publication 800-207. Gaithersburg, MD: National Institute of Standards and Technology; 2020.

[32] Kusiak A. Smart manufacturing. Int J Prod Res. 2018;56(1–2):508–517.

[33] Lee J, Wu F, Zhao W, Ghaffari M, Liao L, Siegel D. Prognostics and health management design for rotary machinery systems—Reviews, methodology and applications. Mech Syst Signal Process. 2014;42(1–2):314–334.

[34] Romero D, Stahre J, Wuest T, Noran O, Bernus P, Fast-Berglund Å, Gorecky D. Towards an Operator 4.0 typology: A human-centric perspective on the fourth industrial revolution technologies. In: Proceedings of the International Conference on Computers and Industrial Engineering (CIE46). Tianjin; 2016. p. 1–11.

[35] Villani V, Pini F, Leali F, Secchi C. Survey on human–robot collaboration in industrial settings: Safety, intuitive interfaces and applications. Mechatronics. 2018;55:248–266.

[36] World Economic Forum, McKinsey & Company. Global Lighthouse Network: Shaping the Next Chapter of the Fourth Industrial Revolution. White paper. Geneva: World Economic Forum; 2023.

[37] Adisorn T, Tholen L, Götz T. Towards a digital product passport fit for contributing to a circular economy. Energies. 2021;14(8):2289.

[38] Ivanov D, Dolgui A. A digital supply chain twin for managing the disruption risks and resilience in the era of Industry 4.0. Prod Plan Control. 2021;32(9):775–788.

[39] Psarommatis F, May G, Dreyfus PA, Kiritsis D. Zero defect manufacturing: State-of-the-art review, shortcomings and future directions in research. Int J Prod Res. 2020;58(1):1–17.

[40] International Organization for Standardization (ISO). ISO 23247-1:2021. Automation systems and integration—Digital twin framework for manufacturing—Part 1: Overview and general principles. Geneva: ISO; 2021.

[41] Schuh G, Anderl R, Gausemeier J, ten Hompel M, Wahlster W, editors. Industrie 4.0 Maturity Index: Managing the Digital Transformation of Companies. acatech STUDY. Munich: Herbert Utz Verlag; 2017.

[42] Lichtblau K, Stich V, Bertenrath R, Blum M, Bleider M, Millack A, Schmitt K, Schmitz E, Schröter M. IMPULS—Industrie 4.0-Readiness. Aachen and Cologne: IMPULS-Stiftung des VDMA; 2015.

[43] Bayerstadler A, Becquin G, Binder J, Botter T, Ehm H, Ehmer T, et al. Industry quantum computing applications. EPJ Quantum Technol. 2021;8(1):25.
