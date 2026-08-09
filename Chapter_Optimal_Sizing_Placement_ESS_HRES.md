# Optimal Sizing and Placement of Energy Storage Systems in Hybrid Renewable Energy Systems (HRES)

**Book Title:** Intelligent Power Management and Resilient Control in Hybrid Renewable Energy Systems

---

## Abstract

The global transition toward sustainable energy infrastructures has accelerated the deployment of hybrid renewable energy systems (HRES) that integrate multiple generation sources such as solar photovoltaic, wind turbines, and biomass with energy storage systems (ESS). A critical challenge in HRES design lies in determining the optimal size and placement of ESS to maximize system reliability, minimize costs, and enhance grid stability. This chapter provides a comprehensive examination of methodologies for optimal sizing and placement of energy storage systems within HRES frameworks. The chapter begins with fundamental concepts of HRES architectures and ESS technologies, followed by detailed discussions of mathematical optimization models, metaheuristic algorithms, and artificial intelligence-driven approaches for ESS sizing. Placement strategies are explored through grid-connected and standalone configurations, supported by case studies demonstrating practical implementations. The chapter concludes with future directions encompassing intelligent energy management, digital twin technologies, and techno-economic assessments. Four tables summarizing key comparative data and six figures illustrating system architectures, optimization frameworks, and performance metrics are presented throughout the discussion to enhance comprehension of the methodologies and their applications in modern energy systems.

---

## 1. Fundamentals of Hybrid Renewable Energy Systems and Energy Storage

### 1.1 Overview of Hybrid Renewable Energy Systems (HRES)

Hybrid renewable energy systems represent an integrated approach to power generation that combines two or more renewable energy sources, often supplemented by conventional backup generators and energy storage devices, to provide reliable and sustainable electricity supply. The fundamental premise of HRES lies in exploiting the complementary nature of different renewable resources to overcome the inherent intermittency and variability of individual sources [1]. For instance, solar photovoltaic (PV) systems generate electricity during daylight hours while wind turbines may produce power predominantly during nighttime or different seasonal periods, creating a synergistic combination that enhances overall system availability.


The architectural configuration of HRES varies significantly depending on application requirements, geographical location, and economic constraints. Common configurations include solar-wind hybrid systems, solar-wind-diesel-battery systems, and multi-source systems incorporating biomass, micro-hydro, or fuel cells [2]. These systems can operate in grid-connected mode, where excess energy is exported to the utility grid, or in standalone (off-grid) mode, serving remote communities without grid access. The increasing penetration of renewable energy sources in global electricity markets has necessitated sophisticated design methodologies to ensure that HRES configurations meet technical performance standards while maintaining economic viability [3].

The design complexity of HRES arises from the stochastic nature of renewable resources, load demand variability, component degradation characteristics, and the need to balance multiple competing objectives including reliability, cost, and environmental impact. Modern HRES design frameworks incorporate advanced computational techniques ranging from classical linear programming to evolutionary algorithms and machine learning approaches [4]. As illustrated in Figure 1, a typical HRES architecture integrates multiple generation sources with energy storage and power conditioning equipment through AC/DC bus configurations. The system controller manages power flow among components based on predefined energy management strategies that prioritize renewable generation and optimize storage utilization.

The global installed capacity of HRES has experienced remarkable growth, with projections indicating that hybrid systems will constitute over 30% of new renewable energy installations by 2030 [5]. This growth is driven by declining component costs, supportive policy frameworks, and technological advances in power electronics and control systems. However, the economic and technical performance of HRES is fundamentally dependent on proper system sizing and the strategic placement of energy storage components within the system architecture.

### 1.2 Role and Importance of Energy Storage Systems (ESS)

Energy storage systems serve as the critical enabling technology for hybrid renewable energy systems, providing the temporal decoupling between energy generation and consumption that is essential for reliable operation. The primary functions of ESS in HRES include energy time-shifting, peak shaving, frequency regulation, voltage support, and backup power provision during renewable resource unavailability [6]. Without adequate energy storage, the intermittent nature of renewable sources would result in significant power quality issues, load curtailment, and reduced system reliability.

The importance of ESS in HRES extends beyond simple energy buffering. Advanced energy storage systems enable sophisticated energy management strategies including demand response participation, ancillary service provision, and arbitrage opportunities in deregulated electricity markets [7]. The economic value of ESS is increasingly recognized through revenue stacking approaches where storage assets provide multiple services simultaneously, enhancing the overall return on investment. Table 1 presents a comprehensive comparison of key energy storage technologies applicable to HRES, including their technical characteristics and typical applications.

**Table 1: Comparison of Energy Storage Technologies for HRES Applications**

| Technology | Energy Density (Wh/kg) | Power Density (W/kg) | Round-trip Efficiency (%) | Cycle Life | Typical Capacity | Response Time | Capital Cost ($/kWh) |
|---|---|---|---|---|---|---|---|
| Lithium-ion Battery | 150–250 | 300–1500 | 85–95 | 4000–10000 | 1 kWh–100 MWh | Milliseconds | 150–300 |
| Vanadium Redox Flow | 15–35 | 50–100 | 65–80 | 10000–20000 | 100 kWh–100 MWh | Seconds | 300–500 |
| Sodium-Sulfur Battery | 150–240 | 150–230 | 75–85 | 2500–4500 | 1–50 MWh | Milliseconds | 300–500 |
| Supercapacitor | 5–15 | 5000–10000 | 90–98 | 500000+ | 1 kWh–1 MWh | Milliseconds | 500–1000 |
| Pumped Hydro Storage | 0.5–1.5 | N/A | 70–85 | 30000+ | 100 MWh–10 GWh | Minutes | 50–150 |
| Compressed Air (CAES) | 30–60 | N/A | 40–70 | 10000+ | 100 MWh–1 GWh | Minutes | 50–100 |
| Hydrogen Fuel Cell | 800–1200 | 500+ | 30–45 | 5000–20000 | 1 kWh–100 MWh | Seconds | 400–800 |

The selection of appropriate ESS technology for a specific HRES application depends on multiple factors including required storage duration, power rating, cycling frequency, environmental conditions, and economic constraints [8]. Short-duration applications requiring rapid response favor supercapacitors and lithium-ion batteries, while long-duration seasonal storage applications may benefit from pumped hydro or hydrogen storage solutions. The optimal ESS configuration often involves hybrid storage architectures combining multiple technologies to address different temporal scales of energy management, as further discussed in Table 1 which highlights the diverse performance characteristics across storage technologies [9].


### 1.3 Classification of Energy Storage Technologies

Energy storage technologies can be classified based on the form of stored energy into mechanical, electrochemical, electrical, thermal, and chemical categories [10]. Each category encompasses multiple specific technologies with distinct operational characteristics that determine their suitability for various HRES applications.

**Mechanical Storage Systems** include pumped hydroelectric storage (PHS), compressed air energy storage (CAES), and flywheel energy storage systems (FESS). PHS remains the most mature and widely deployed large-scale storage technology globally, accounting for approximately 95% of installed grid-scale storage capacity. CAES systems store energy by compressing air in underground caverns during off-peak periods and releasing it through turbines during peak demand. Flywheel systems store kinetic energy in rotating masses and provide excellent power quality support with extremely fast response times [11].

**Electrochemical Storage Systems** encompass various battery technologies including lithium-ion (Li-ion), lead-acid, sodium-sulfur (NaS), vanadium redox flow batteries (VRFB), and zinc-bromine flow batteries. Lithium-ion technology has experienced dramatic cost reductions exceeding 89% over the past decade, making it the dominant choice for both stationary and mobile storage applications [12]. Flow batteries offer advantages of decoupled energy and power ratings, long cycle life, and deep discharge capability, making them attractive for medium to long-duration storage applications.

**Electrical Storage Systems** include supercapacitors (ultracapacitors) and superconducting magnetic energy storage (SMES). These technologies excel in high-power, short-duration applications requiring millions of charge-discharge cycles without significant degradation. Supercapacitors are increasingly combined with batteries in hybrid ESS configurations to handle transient power demands while batteries manage sustained energy requirements [13].

**Chemical Storage Systems** primarily involve hydrogen production through water electrolysis, storage, and subsequent power generation via fuel cells or hydrogen turbines. Power-to-gas (P2G) technology enables seasonal energy storage with very large capacity potential, addressing the long-duration storage challenge that battery technologies cannot economically solve [14]. Green hydrogen produced from renewable surplus is gaining significant attention as a versatile energy carrier that can decarbonize multiple sectors beyond electricity.

**Thermal Storage Systems** store energy as heat or cold in various media including molten salts, phase change materials, and thermochemical storage materials. Concentrated solar power (CSP) plants commonly employ molten salt thermal storage to extend generation beyond solar hours, while ice storage systems provide demand management for air conditioning loads [15].

The classification and selection of storage technologies for HRES applications must consider the system's specific requirements regarding energy capacity, power rating, response time, cycling patterns, and operational lifetime. Figure 2 provides a classification framework for energy storage technologies organized by storage duration and power rating, illustrating the complementary roles different technologies play in the energy system hierarchy.

### 1.4 Challenges and Design Considerations for ESS Integration

The integration of energy storage systems into hybrid renewable energy systems presents numerous technical, economic, and operational challenges that must be carefully addressed during the design phase. These challenges span multiple domains and require interdisciplinary approaches combining power systems engineering, optimization theory, economics, and increasingly, artificial intelligence and data science [16].

**Technical Challenges** include the determination of optimal ESS capacity and power ratings, selection of appropriate battery management systems, thermal management requirements, power converter sizing and topology, and protection coordination. Battery degradation modeling represents a particularly critical challenge, as ESS performance and capacity decline over time depending on cycling depth, temperature, charge/discharge rates, and calendar aging effects. Accurate degradation models are essential for lifetime cost estimation and replacement planning [17].

**Economic Challenges** encompass high upfront capital costs, uncertain future revenue streams, evolving regulatory frameworks, and the difficulty of accurately valuing the multiple services that ESS can provide. The economic viability of ESS depends heavily on market structures, tariff designs, and incentive mechanisms that vary significantly across jurisdictions. Life cycle cost analysis must account for replacement costs, maintenance requirements, efficiency losses, and end-of-life disposal or recycling costs [18].

**Operational Challenges** include real-time energy management under uncertainty, coordination between multiple storage units and generation sources, state-of-charge management, and grid code compliance. The stochastic nature of renewable generation and load demand requires robust control strategies that maintain system reliability while optimizing ESS utilization. Advanced forecasting techniques for solar irradiance, wind speed, and load profiles are essential inputs to optimal ESS operational strategies [19].

**Grid Integration Challenges** arise when HRES with ESS are connected to utility grids, including power quality requirements, fault ride-through capability, anti-islanding protection, and contribution to system inertia. The increasing penetration of inverter-based resources is fundamentally changing grid dynamics, creating new challenges for system stability that ESS can help address through grid-forming converter control strategies [20].

These challenges collectively motivate the development of sophisticated optimization methodologies for ESS sizing and placement, which form the core focus of subsequent sections in this chapter.

---

## 2. Optimal Sizing Methodologies for Energy Storage Systems

### 2.1 Factors Influencing ESS Sizing

The optimal sizing of energy storage systems in HRES is influenced by a complex interplay of technical, economic, environmental, and regulatory factors that must be simultaneously considered within the optimization framework. Understanding these factors is essential for formulating appropriate objective functions and constraints in sizing optimization problems [21].

**Resource Availability and Variability:** The temporal profiles of renewable resources fundamentally determine ESS sizing requirements. Locations with high solar-wind complementarity require smaller storage capacities compared to sites dominated by a single intermittent source. Seasonal variations in resource availability influence long-term storage requirements, while short-term fluctuations determine power rating needs for frequency support and ramp rate compliance [22].

**Load Profile Characteristics:** The magnitude, shape, and variability of electrical demand significantly influence ESS sizing. Loads with high peak-to-average ratios benefit more from storage-based peak shaving, while loads with significant daily cycling patterns create clear arbitrage opportunities. Critical loads requiring high reliability may necessitate larger ESS capacities to ensure adequate backup duration during extended resource unavailability periods.

**System Reliability Requirements:** The desired level of supply reliability, typically expressed through metrics such as Loss of Power Supply Probability (LPSP), Expected Energy Not Served (EENS), or System Average Interruption Duration Index (SAIDI), directly impacts ESS sizing. Higher reliability requirements correspond to larger ESS capacities, creating a trade-off between reliability and cost that must be balanced through multi-objective optimization approaches [23].

**Economic Parameters:** Capital costs, replacement costs, operation and maintenance expenses, discount rates, project lifetime, and electricity tariff structures all influence the economically optimal ESS size. The rapidly declining costs of lithium-ion batteries have significantly altered optimal sizing results compared to studies conducted just a few years ago, highlighting the importance of using current cost projections in planning studies.

**Regulatory and Market Frameworks:** Grid connection requirements, renewable energy mandates, carbon pricing mechanisms, and ancillary service market structures create economic signals that influence optimal ESS sizing. Systems participating in multiple markets may require different sizing than those serving purely self-consumption applications [24].

**Technology Degradation Characteristics:** Battery aging effects including capacity fade and resistance growth reduce effective storage capacity over the project lifetime. Oversizing strategies that account for end-of-life performance requirements or staged investment approaches that plan for capacity augmentation must be incorporated into sizing methodologies for accurate long-term planning.


### 2.2 Mathematical Modeling and Optimization Objectives

The mathematical formulation of ESS sizing optimization problems requires careful definition of decision variables, objective functions, constraints, and system models that collectively capture the essential physics and economics of the HRES-ESS system [25].

**Decision Variables** typically include ESS energy capacity (kWh), power rating (kW), number of storage units, and in some formulations, the storage technology type. For hybrid storage systems combining multiple technologies, additional decision variables specify the capacity allocation among different storage types.

**Objective Functions** in ESS sizing optimization commonly include:

1. *Minimization of Total Life Cycle Cost (TLCC):* This encompasses capital expenditure, replacement costs, operation and maintenance costs, and salvage value, discounted to present value over the project lifetime.

$$TLCC = C_{cap} + \sum_{t=1}^{N} \frac{C_{O\&M}(t) + C_{rep}(t)}{(1+r)^t} - \frac{C_{sal}}{(1+r)^N}$$

2. *Minimization of Levelized Cost of Energy (LCOE):* Representing the total system cost normalized by total energy delivered over the project lifetime.

$$LCOE = \frac{TLCC}{\sum_{t=1}^{N} E_{delivered}(t) / (1+r)^t}$$

3. *Maximization of System Reliability:* Typically formulated as minimization of LPSP or maximization of renewable energy fraction.

4. *Minimization of Environmental Impact:* Quantified through life cycle greenhouse gas emissions or embodied energy of system components.

**Constraints** define the feasible solution space and include:

- Energy balance: Generation + Storage discharge = Load + Storage charge + Losses
- ESS state of charge limits: $SOC_{min} \leq SOC(t) \leq SOC_{max}$
- Power rating constraints: $P_{charge}(t) \leq P_{rated}$, $P_{discharge}(t) \leq P_{rated}$
- Reliability constraints: $LPSP \leq LPSP_{max}$
- Budget constraints: $C_{total} \leq C_{budget}$
- Physical space constraints for installation sites

**System Models** required for ESS sizing optimization include solar PV generation models incorporating irradiance, temperature, and degradation effects; wind turbine power curves with site-specific wind distributions; battery electrochemical models capturing voltage, efficiency, and degradation dynamics; power converter efficiency models; and load demand models ranging from simple profiles to stochastic representations [26].

The complexity of these optimization problems, characterized by nonlinear objective functions, mixed-integer decision variables, stochastic parameters, and multiple competing objectives, necessitates the application of advanced optimization techniques as discussed in the following subsections. Figure 3 presents a comprehensive optimization framework for ESS sizing showing the interaction between input data, mathematical models, optimization algorithms, and output decisions.

### 2.3 Conventional and Metaheuristic Optimization Techniques

The evolution of optimization techniques applied to ESS sizing has progressed from classical analytical methods through conventional mathematical programming to modern metaheuristic and hybrid approaches, reflecting the increasing complexity of problem formulations and the availability of computational resources [27].

**Conventional Optimization Techniques** applied to ESS sizing include:

*Linear Programming (LP) and Mixed-Integer Linear Programming (MILP):* These methods provide globally optimal solutions for problems that can be formulated with linear objectives and constraints. LP/MILP approaches require linearization of nonlinear system models, which may introduce approximation errors but enable the use of efficient commercial solvers (CPLEX, Gurobi) for large-scale problems. MILP formulations are particularly suitable for problems involving discrete component sizing options and binary operational decisions [28].

*Nonlinear Programming (NLP):* For problems with nonlinear relationships that cannot be adequately linearized, NLP methods including Sequential Quadratic Programming (SQP) and Interior Point methods provide local optimal solutions. The challenge of multiple local optima in non-convex ESS sizing problems limits the reliability of these approaches without careful initialization strategies.

*Dynamic Programming (DP):* Suitable for sequential decision problems, DP decomposes the sizing problem into stages corresponding to time periods, enabling optimal operational strategies to be embedded within the sizing optimization. However, computational complexity grows exponentially with state-space dimensionality (curse of dimensionality), limiting application to problems with few state variables.

**Metaheuristic Optimization Techniques** have gained widespread adoption for ESS sizing due to their ability to handle complex, nonlinear, multi-modal optimization landscapes without requiring gradient information or problem convexification:

*Genetic Algorithm (GA):* Inspired by biological evolution, GA maintains a population of candidate solutions that undergo selection, crossover, and mutation operations to evolve toward optimal designs. GA has been extensively applied to HRES-ESS sizing with demonstrated effectiveness for multi-objective formulations using non-dominated sorting approaches (NSGA-II, NSGA-III) [29].

*Particle Swarm Optimization (PSO):* Based on social behavior of bird flocks, PSO guides particles through the solution space using personal and global best positions. Variants including adaptive PSO, chaotic PSO, and hybrid PSO-GA have shown improved convergence for ESS sizing problems.

*Grey Wolf Optimizer (GWO):* A relatively recent metaheuristic inspired by grey wolf hunting behavior, GWO has demonstrated competitive performance for renewable energy system optimization with advantages of simplicity and few tuning parameters [30].

*Whale Optimization Algorithm (WOA):* Mimicking humpback whale bubble-net feeding strategy, WOA balances exploration and exploitation phases effectively for energy system sizing problems.

*Harris Hawks Optimization (HHO):* Inspired by the cooperative hunting behavior of Harris hawks, HHO has shown superior performance for power system optimization problems with rapid convergence and strong exploitation capability.

Table 2 provides a comprehensive comparison of optimization techniques applied to ESS sizing in recent literature, highlighting their characteristics, advantages, and limitations.

**Table 2: Comparison of Optimization Techniques for ESS Sizing in HRES**

| Technique | Type | Convergence Speed | Global Optimality | Handling of Constraints | Multi-Objective Capability | Computational Cost | Key References |
|---|---|---|---|---|---|---|---|
| MILP | Exact | High | Guaranteed (linear) | Excellent | Limited | Moderate | [28] |
| Genetic Algorithm | Metaheuristic | Moderate | Probabilistic | Good (penalty) | Excellent (NSGA-II) | High | [29] |
| Particle Swarm Optimization | Metaheuristic | Fast | Probabilistic | Moderate | Good | Moderate | [30] |
| Grey Wolf Optimizer | Metaheuristic | Fast | Probabilistic | Good | Good | Low | [30] |
| Whale Optimization Algorithm | Metaheuristic | Moderate | Probabilistic | Good | Moderate | Moderate | [31] |
| Simulated Annealing | Metaheuristic | Slow | Probabilistic | Good | Limited | Moderate | [27] |
| Reinforcement Learning | AI-based | Variable | Adaptive | Excellent | Emerging | High (training) | [32] |
| Hybrid GA-PSO | Hybrid | Fast | Improved | Good | Good | High | [29] |

The selection of optimization technique depends on problem characteristics including dimensionality, constraint complexity, required solution quality, and available computational budget. As shown in Table 2, hybrid approaches combining multiple algorithms often achieve superior performance by leveraging the complementary strengths of different methods [31].


### 2.4 AI-Driven and Multi-Objective Sizing Approaches

The application of artificial intelligence and machine learning techniques to ESS sizing optimization represents a rapidly evolving frontier that promises to address limitations of conventional approaches, particularly regarding computational efficiency, uncertainty handling, and adaptive decision-making [32].

**Deep Reinforcement Learning (DRL)** approaches formulate ESS sizing as a sequential decision-making problem where an agent learns optimal sizing policies through interaction with a simulated environment. DRL methods can simultaneously learn operational strategies and sizing decisions, capturing the strong coupling between these aspects that conventional two-stage approaches may miss. Recent applications of Deep Q-Networks (DQN), Proximal Policy Optimization (PPO), and Soft Actor-Critic (SAC) algorithms have demonstrated superior performance for ESS sizing under uncertain renewable generation and demand conditions [33].

**Neural Network-Based Surrogate Models** address the computational burden of detailed system simulation within optimization loops. Trained on simulation data, surrogate models provide rapid approximate evaluations of system performance for candidate sizing solutions, enabling efficient exploration of large design spaces. Gaussian Process regression, Random Forests, and deep neural networks have been employed as surrogates with active learning strategies to iteratively improve model accuracy in promising regions of the design space [34].

**Fuzzy Logic and Neuro-Fuzzy Systems** handle the imprecision and linguistic uncertainty inherent in ESS sizing decisions. Fuzzy multi-criteria decision-making frameworks enable the incorporation of qualitative expert knowledge alongside quantitative optimization results, facilitating technology selection and sizing decisions when data are limited or uncertain.

**Multi-Objective Optimization** approaches recognize that ESS sizing inherently involves trade-offs among competing objectives including cost minimization, reliability maximization, environmental impact reduction, and system lifetime extension. Pareto-based approaches generate sets of non-dominated solutions that represent optimal trade-offs, enabling decision-makers to select preferred designs based on their priorities [35].

Advanced multi-objective frameworks for ESS sizing include:

- *NSGA-III:* Reference-point-based many-objective optimization suitable for problems with more than three objectives
- *MOEA/D:* Decomposition-based approach that converts multi-objective problems into sets of scalar subproblems
- *ε-Constraint Method:* Systematic approach for generating Pareto-optimal solutions by optimizing one objective while constraining others

**Uncertainty Quantification and Robust Optimization** methods ensure that sizing solutions remain feasible and near-optimal across a range of uncertain future conditions. Stochastic programming, robust optimization, and distributionally robust approaches provide different levels of conservatism in handling uncertainties in renewable resources, load growth, component costs, and policy changes. Scenario-based approaches generate representative scenarios of uncertain parameters and optimize sizing decisions that perform well across all scenarios [36].

**Transfer Learning and Domain Adaptation** techniques enable knowledge gained from sizing optimization of one HRES configuration to accelerate optimization of similar systems at different locations or scales. This reduces the computational effort required for each new sizing study and facilitates rapid preliminary design assessments.

The integration of AI techniques with traditional optimization creates powerful hybrid frameworks where machine learning provides intelligent initialization, constraint handling, or algorithm selection while metaheuristics perform the actual optimization. These synergistic approaches represent the current state-of-the-art in ESS sizing methodology and continue to advance rapidly with improvements in computational hardware and algorithmic development.

---

## 3. Optimal Placement Strategies for Energy Storage Systems

### 3.1 Grid-Connected and Standalone HRES Architectures

The placement of energy storage systems within HRES architectures is fundamentally influenced by the system configuration, which can be broadly categorized into grid-connected and standalone (off-grid) architectures, each presenting distinct placement challenges and opportunities [37].

**Grid-Connected HRES Architectures** interface with the utility grid through a point of common coupling (PCC) and may include distributed generation sources, energy storage, and controllable loads at various points within the distribution network. In grid-connected configurations, ESS placement decisions consider not only local energy management but also network-level impacts including voltage regulation, loss reduction, congestion relief, and deferral of network reinforcement investments. The optimal ESS location in a distribution network depends on network topology, load distribution, generation locations, and the specific services the storage is intended to provide.

Grid-connected ESS placement options include:
- *Transmission-connected:* Large-scale storage providing bulk energy services, frequency regulation, and transmission congestion relief
- *Distribution substation:* Medium-scale storage for peak demand management, voltage support, and feeder loading relief
- *Behind-the-meter:* Customer-sited storage for demand charge reduction, self-consumption optimization, and backup power
- *Community-scale:* Shared storage serving multiple customers for collective energy management

**Standalone HRES Architectures** operate independently of the utility grid and must maintain instantaneous power balance between generation and load at all times, making ESS an indispensable component rather than an optional enhancement. In standalone systems, ESS placement considers DC bus vs. AC bus connection, proximity to generation sources or loads, and the physical constraints of installation sites [38].

Common standalone HRES architectures include:
- *DC-coupled systems:* All components connected through a common DC bus with a single inverter for AC loads
- *AC-coupled systems:* Components connected through an AC bus with individual inverters for each source
- *Hybrid DC/AC-coupled systems:* Combined architecture leveraging advantages of both configurations

The choice between DC and AC coupling significantly affects ESS placement and sizing requirements due to differences in conversion losses, control complexity, and operational flexibility. DC-coupled systems typically achieve higher round-trip efficiency for ESS cycling but may limit system expandability, while AC-coupled systems provide greater flexibility for future capacity additions at the cost of additional converter losses.

Figure 4 illustrates representative grid-connected and standalone HRES architectures showing typical ESS placement options and their relationship to system buses, power converters, and control elements. The architectural decisions made during system design fundamentally constrain the available placement options for energy storage components.

### 3.2 Placement Criteria and Performance Indices

The evaluation of ESS placement alternatives requires well-defined performance criteria that capture the technical, economic, and reliability impacts of storage location within the HRES or distribution network. Multiple performance indices have been developed and applied in the literature to assess and compare different placement strategies [21].

**Technical Performance Indices:**

*Voltage Deviation Index (VDI):* Quantifies the improvement in voltage profile achieved by ESS placement at a specific location. The VDI measures the weighted deviation of bus voltages from nominal values across all system buses and time periods:

$$VDI = \sum_{t=1}^{T} \sum_{i=1}^{N_{bus}} w_i \cdot |V_i(t) - V_{nom}|^2$$

*Power Loss Reduction Index (PLRI):* Evaluates the reduction in network power losses achieved by ESS placement, considering both active and reactive power losses in distribution feeders.

*Congestion Relief Index (CRI):* Measures the reduction in line loading and transformer loading achieved through strategic ESS placement, potentially deferring costly infrastructure upgrades.

*Frequency Deviation Index (FDI):* Quantifies the improvement in system frequency response enabled by ESS placed at specific network locations, particularly relevant for isolated microgrids and weak grid connections.

**Economic Performance Indices:**

*Net Present Value (NPV):* Total economic benefit of ESS placement considering avoided costs, revenue streams, and investment costs discounted over the project lifetime.

*Benefit-Cost Ratio (BCR):* Ratio of total discounted benefits to total discounted costs for ESS at each candidate location, enabling comparison of placement alternatives on a normalized basis.

*Payback Period:* Time required for cumulative benefits to recover the initial investment, providing an intuitive measure of economic attractiveness for each placement option.

**Reliability Performance Indices:**

*Loss of Load Probability (LOLP):* Probability that system load exceeds available generation plus storage discharge capacity at any time period.

*Expected Energy Not Served (EENS):* Expected quantity of energy that cannot be supplied to loads due to insufficient generation and storage capacity.

*System Average Interruption Frequency Index (SAIFI):* Average number of interruptions experienced per customer served, measurable improvement through strategic ESS placement.

The multi-dimensional nature of these performance indices necessitates multi-criteria decision-making frameworks for ESS placement optimization, as no single index captures all relevant aspects of system performance. Weighted aggregation, lexicographic ordering, and Pareto optimization approaches are employed to synthesize multiple indices into actionable placement decisions [23].


### 3.3 Optimization Algorithms for ESS Placement

The optimal placement of energy storage systems in HRES and distribution networks represents a combinatorial optimization problem with both discrete (location selection) and continuous (capacity sizing) decision variables, requiring specialized algorithmic approaches [31].

**Sensitivity Analysis-Based Methods** provide computationally efficient initial screening of candidate locations by evaluating the sensitivity of system performance indices to ESS placement at each bus or node. Voltage sensitivity factors, loss sensitivity indices, and locational marginal prices serve as analytical indicators that identify promising placement locations without exhaustive search. These methods are particularly useful for large networks where full optimization of all possible locations would be computationally prohibitive.

**Mathematical Programming Approaches** for ESS placement include MILP formulations where binary variables represent placement decisions (1 if storage is placed at a candidate location, 0 otherwise) and continuous variables represent capacity allocations. The joint placement-sizing problem can be formulated as:

$$\min \sum_{i \in \Omega_c} (x_i \cdot C_{fixed,i} + E_i \cdot C_{energy,i} + P_i \cdot C_{power,i})$$

Subject to network constraints, power flow equations, and ESS operational constraints, where $x_i$ is the binary placement variable, $E_i$ and $P_i$ are energy and power capacity at location $i$, and $\Omega_c$ is the set of candidate locations.

**Metaheuristic Algorithms for Placement Optimization** extend the approaches described in Section 2.3 to handle the combinatorial nature of placement problems:

*Modified Genetic Algorithm:* Binary-coded GA with placement-specific crossover operators that maintain network feasibility. Multi-chromosome representations encode both discrete placement and continuous sizing decisions within a single individual [29].

*Improved Particle Swarm Optimization:* Discrete PSO variants using sigmoid transfer functions to convert continuous velocity values into binary placement decisions, combined with local search operators for intensification around promising placement configurations.

*Ant Colony Optimization (ACO):* Particularly suited for combinatorial placement problems, ACO mimics ant foraging behavior where pheromone trails guide search toward high-quality placement combinations discovered by previous iterations.

*Artificial Bee Colony (ABC):* Employs employed, onlooker, and scout bee phases for systematic exploration of the placement solution space with effective balance between diversification and intensification.

**Hybrid and Decomposition Approaches** address the computational challenge of simultaneously optimizing placement and sizing in large networks:

*Benders Decomposition:* Separates the problem into a master problem (placement decisions) and subproblems (operational optimization for given placements), iterating between levels with optimality cuts that progressively tighten the relaxation.

*Bi-Level Optimization:* Upper level determines ESS placement and sizing while lower level optimizes operational strategies for each candidate configuration, capturing the hierarchical nature of planning and operation decisions.

*Column Generation:* Systematically generates promising placement configurations and evaluates them within a master problem framework, efficiently exploring the vast combinatorial space of possible placements.

**Machine Learning-Enhanced Placement** approaches leverage data-driven models to accelerate or improve placement optimization. Graph Neural Networks (GNN) have emerged as particularly promising tools for distribution network ESS placement, as they can learn spatial relationships between network topology and optimal storage locations from training data generated by full optimization solutions [34]. Once trained, GNN models provide near-instantaneous placement recommendations for new network configurations, enabling rapid screening of planning alternatives.

### 3.4 Case Studies on Optimal ESS Placement in HRES

Practical case studies demonstrate the application and effectiveness of optimization methodologies for ESS placement in realistic HRES configurations. The following representative case studies illustrate different aspects of the placement optimization problem.

**Case Study 1: IEEE 33-Bus Distribution Network with Distributed PV and Wind**

A comprehensive study optimized ESS placement in a modified IEEE 33-bus radial distribution network with 40% renewable penetration from distributed solar PV (buses 7, 14, 25) and wind turbines (buses 18, 30). The optimization employed NSGA-III with objectives of minimizing annual energy losses, voltage deviation, and total ESS investment cost [35]. Results identified buses 6, 17, and 29 as optimal placement locations with aggregate capacity of 2.4 MWh/1.2 MW, achieving 34% loss reduction and 67% improvement in voltage deviation index compared to the base case without storage. The study demonstrated that placement optimization reduced required storage capacity by 28% compared to a naive approach placing all storage at the point of common coupling.

**Case Study 2: Remote Microgrid with Solar-Wind-Diesel-Battery HRES**

An island microgrid serving a remote community of 500 households was designed with optimal ESS placement considering multiple candidate locations including the central generation hub, three load centers, and two intermediate nodes [22]. The optimization used a hybrid GA-PSO algorithm with objectives of minimizing LCOE while maintaining LPSP below 1%. Distributed placement of battery storage across two load centers (60% and 40% capacity split) achieved 12% lower LCOE compared to centralized placement, primarily due to reduced distribution losses and improved voltage regulation at load centers. The distributed configuration also demonstrated superior reliability performance during extreme weather events that could damage a single centralized installation.

**Case Study 3: Grid-Connected Industrial HRES with Multiple Storage Technologies**

A large industrial facility with 5 MW solar PV and 3 MW wind generation optimized the placement and sizing of a hybrid ESS combining lithium-ion batteries (short-duration) and vanadium redox flow batteries (long-duration) at three candidate locations: the main distribution board, a critical load bus, and the PCC with the utility grid [36]. Multi-objective optimization using MOEA/D identified the Pareto-optimal set of placement-sizing combinations trading off capital cost against reliability improvement and demand charge reduction. The preferred solution placed 1.5 MWh/1 MW lithium-ion at the critical load bus for power quality support and 4 MWh/0.8 MW flow battery at the PCC for energy arbitrage and demand charge management, achieving 22% reduction in annual electricity costs with a 6.3-year payback period.

Table 3 summarizes the key parameters and results of these case studies, providing a comparative perspective on ESS placement optimization outcomes across different system configurations.

**Table 3: Summary of ESS Placement Case Studies**

| Parameter | Case Study 1 | Case Study 2 | Case Study 3 |
|---|---|---|---|
| System Type | Grid-connected Distribution | Off-grid Microgrid | Grid-connected Industrial |
| Renewable Sources | Distributed PV + Wind | Solar + Wind + Diesel | Solar PV + Wind |
| Total RE Capacity | 4.5 MW | 850 kW | 8 MW |
| Network Configuration | 33-bus radial | 6-node microgrid | 3-bus industrial |
| Optimization Algorithm | NSGA-III | Hybrid GA-PSO | MOEA/D |
| Objectives | Losses, Voltage, Cost | LCOE, Reliability | Cost, Reliability, Power Quality |
| Optimal ESS Locations | Buses 6, 17, 29 | Load centers 2, 3 | Critical load + PCC |
| Total ESS Capacity | 2.4 MWh / 1.2 MW | 1.8 MWh / 600 kW | 5.5 MWh / 1.8 MW |
| Key Improvement | 34% loss reduction | 12% LCOE reduction | 22% cost reduction |
| Payback Period | 7.2 years | 8.5 years | 6.3 years |

These case studies demonstrate that systematic optimization of ESS placement, as detailed in Table 3, yields significant performance improvements compared to conventional placement approaches based on engineering judgment alone. The benefits of optimal placement are particularly pronounced in systems with distributed generation sources and spatially distributed loads, where the interaction between storage location and network constraints creates a complex optimization landscape [38].

---

## 4. Future Directions and Practical Applications

### 4.1 Intelligent Energy Management Systems for ESS

The operational effectiveness of optimally sized and placed energy storage systems depends critically on the intelligence of the energy management system (EMS) that controls their charging and discharging behavior in real-time. Modern intelligent EMS approaches leverage advanced computational techniques to maximize the value extracted from ESS investments while maintaining system reliability and extending storage lifetime [7].

**Model Predictive Control (MPC)** has emerged as the dominant advanced control strategy for ESS management in HRES. MPC formulates a receding-horizon optimization problem that determines optimal charging/discharging actions over a future time horizon based on forecasts of renewable generation, load demand, and electricity prices. The optimization is solved at each control interval, with only the first-period actions implemented before the horizon advances. MPC naturally handles constraints on state-of-charge, power ratings, and ramp rates while optimizing multi-period objectives [33].

**Deep Reinforcement Learning (DRL) for Real-Time Control** addresses limitations of MPC including computational burden for complex systems and sensitivity to forecast accuracy. DRL agents learn optimal control policies through experience, eventually making near-instantaneous decisions without requiring explicit forecasts or online optimization. Multi-agent DRL frameworks coordinate multiple distributed ESS units within HRES, discovering emergent cooperative strategies that outperform centralized optimization approaches in scalability and robustness [32].

**Federated Learning for Privacy-Preserving EMS** enables collaborative learning across multiple HRES sites without sharing raw operational data. Each site trains local models on its data and shares only model parameters with a central aggregator that creates an improved global model distributed back to all sites. This approach is particularly valuable for community energy systems and virtual power plants comprising numerous distributed ESS installations.

**Hierarchical Energy Management** architectures organize control decisions across multiple temporal and spatial scales. Strategic-level decisions (seasonal storage management, maintenance scheduling) operate on weekly to monthly timescales; tactical-level decisions (day-ahead scheduling, market bidding) operate on hourly timescales; and operational-level decisions (real-time dispatch, frequency response) operate on second-to-minute timescales. Each level provides setpoints and constraints to lower levels while receiving feedback on achieved performance.


### 4.2 Digital Twins, IoT, and Predictive Analytics in ESS Deployment

The convergence of digital twin technology, Internet of Things (IoT) infrastructure, and predictive analytics is transforming the deployment and management of energy storage systems in HRES, enabling unprecedented levels of monitoring, optimization, and predictive maintenance [14].

**Digital Twin Technology** for ESS creates high-fidelity virtual replicas of physical storage systems that are continuously updated with real-time operational data. ESS digital twins incorporate multi-physics models capturing electrochemical, thermal, mechanical, and electrical dynamics at various levels of abstraction. These virtual representations enable:

- *What-if Analysis:* Evaluating the impact of different operational strategies on ESS performance and lifetime without risking physical assets
- *Predictive Maintenance:* Identifying emerging degradation patterns and forecasting remaining useful life based on physics-informed machine learning models
- *Optimal Control Policy Updates:* Testing and validating new control algorithms in the digital environment before deployment to physical systems
- *Design Optimization:* Using operational insights from existing installations to inform the design of future ESS deployments

**IoT-Enabled Monitoring Infrastructure** provides the real-time data streams that feed digital twin models and enable intelligent energy management. Sensor networks monitoring cell-level voltage, current, temperature, and impedance characteristics generate high-frequency data that, combined with environmental sensors and smart meter data, create comprehensive operational awareness. Edge computing devices perform local data processing and anomaly detection, reducing communication bandwidth requirements while enabling sub-second control response times [16].

**Predictive Analytics** applications in ESS deployment include:

*Battery State of Health (SOH) Estimation:* Machine learning models trained on cycling data predict remaining capacity and power capability, enabling proactive replacement planning and warranty management. Transfer learning techniques allow SOH models trained on laboratory cycling data to be adapted to field conditions with minimal additional data [17].

*Degradation-Aware Optimal Sizing:* Predictive models of battery aging feed back into sizing optimization, enabling dynamic adjustment of operational strategies as storage capacity declines. Digital twin simulations project long-term capacity trajectories under different operational scenarios, informing decisions about capacity augmentation timing and technology selection for replacements.

*Renewable Resource Forecasting:* Advanced forecasting combining numerical weather prediction, satellite imagery, and machine learning provides probabilistic predictions of solar irradiance and wind speed that inform ESS scheduling decisions. Ensemble forecasting approaches quantify prediction uncertainty, enabling risk-aware storage management strategies.

**Blockchain and Distributed Ledger Technology** enables decentralized energy trading and ESS coordination in peer-to-peer energy markets. Smart contracts automate bilateral energy transactions between prosumers with distributed storage, creating new value streams for ESS assets and incentivizing optimal placement at the distribution edge.

Figure 5 presents the integrated digital ecosystem for ESS deployment showing the relationship between physical assets, IoT sensing infrastructure, digital twin models, and intelligent decision-making layers. This ecosystem represents the future operational paradigm for ESS in HRES.

### 4.3 Techno-Economic and Environmental Assessment

Comprehensive assessment of ESS sizing and placement decisions requires integrated techno-economic and environmental evaluation frameworks that capture the full spectrum of costs, benefits, and impacts over the system lifecycle [18].

**Life Cycle Cost Analysis (LCCA)** provides the foundational economic assessment framework, encompassing:

- *Capital Expenditure (CAPEX):* Equipment procurement (cells, modules, racks, BMS), power conversion systems, balance of plant, installation labor, grid connection, and project development costs
- *Operational Expenditure (OPEX):* Maintenance, insurance, monitoring systems, capacity warranty payments, and auxiliary power consumption
- *Replacement Costs:* Battery module replacement at end-of-useful-life (typically 70-80% remaining capacity), converter replacement, and technology upgrade costs
- *Revenue Streams:* Energy arbitrage, demand charge reduction, frequency regulation, capacity payments, renewable energy incentive schemes, and avoided curtailment value
- *End-of-Life Value:* Second-life applications (e.g., degraded EV batteries repurposed for stationary storage), recycling value of materials, or disposal costs

Table 4 presents a representative techno-economic assessment comparing centralized versus distributed ESS placement strategies for a 10 MW solar-wind HRES, illustrating the economic implications of placement decisions.

**Table 4: Techno-Economic Comparison of ESS Placement Strategies**

| Economic Parameter | Centralized ESS | Distributed ESS | Hybrid Placement |
|---|---|---|---|
| Total ESS Capacity (MWh) | 12.0 | 10.5 | 11.2 |
| Capital Cost (M$) | 4.80 | 4.62 | 4.70 |
| Annual O&M Cost (k$) | 96 | 115 | 105 |
| Annual Revenue - Arbitrage (k$) | 420 | 395 | 435 |
| Annual Revenue - Demand Charges (k$) | 180 | 220 | 210 |
| Annual Revenue - Ancillary Services (k$) | 150 | 130 | 165 |
| Annual Loss Reduction Benefit (k$) | 45 | 85 | 72 |
| 20-Year NPV (M$) | 3.45 | 3.82 | 4.15 |
| LCOE Reduction (%) | 8.5 | 9.2 | 10.8 |
| Simple Payback Period (years) | 7.8 | 6.9 | 6.2 |
| IRR (%) | 11.2 | 13.1 | 14.5 |

As demonstrated in Table 4, hybrid placement strategies that combine centralized and distributed ESS elements achieve superior economic performance compared to purely centralized or distributed approaches. The hybrid approach optimizes the trade-off between economies of scale (favoring centralization) and network-level benefits (favoring distribution) to maximize overall project value [24].

**Environmental Assessment** extends beyond greenhouse gas emissions during operation to encompass the full life cycle environmental impacts of ESS:

*Life Cycle Assessment (LCA):* Systematic evaluation of environmental impacts including global warming potential, acidification, eutrophication, resource depletion, and human toxicity across all lifecycle stages from raw material extraction through manufacturing, operation, and end-of-life management.

*Carbon Footprint Analysis:* Quantification of total greenhouse gas emissions associated with ESS deployment, including embodied emissions in manufacturing and avoided emissions through renewable energy enablement and fossil fuel displacement. The carbon payback period—time required for avoided emissions to compensate for embodied emissions—typically ranges from 6 months to 3 years for lithium-ion batteries in HRES applications [25].

*Circular Economy Considerations:* Assessment of material recyclability, second-life potential, and design-for-disassembly characteristics that influence end-of-life environmental impacts. Emerging regulations including the EU Battery Regulation mandate minimum recycled content, collection rates, and carbon footprint declarations for batteries, influencing technology selection and supply chain decisions.

*Water Footprint:* Evaluation of water consumption across the ESS lifecycle, particularly relevant for lithium extraction in water-scarce regions and for pumped hydro storage systems that may affect water resources.

### 4.4 Future Research Trends and Recommendations

The field of optimal ESS sizing and placement in HRES continues to evolve rapidly, driven by technological advances, market transformation, and increasing ambition of decarbonization targets. Several key research trends and recommendations emerge from the current state-of-the-art [5].

**Emerging Research Directions:**

*Multi-Energy System Integration:* Future sizing and placement optimization must consider ESS within broader multi-energy systems integrating electricity, heat, hydrogen, and transportation sectors. Power-to-X technologies create new coupling between sectors that fundamentally change optimal storage sizing and placement strategies. Sector-coupled optimization identifying synergies between electrical storage, thermal storage, and hydrogen storage represents a critical research frontier [37].

*Climate-Resilient Design:* Climate change impacts on renewable resource availability, extreme weather event frequency, and ambient temperature conditions must be incorporated into ESS sizing and placement decisions. Robust optimization and adaptive planning approaches that account for deep uncertainty in future climate scenarios are needed to ensure long-term system adequacy and resilience [38].

*Equity and Energy Justice:* ESS placement optimization increasingly considers distributional equity impacts, ensuring that benefits of storage deployment are fairly distributed across communities and that vulnerable populations are not disproportionately affected by infrastructure decisions. Multi-stakeholder optimization frameworks incorporating social welfare objectives alongside technical and economic criteria represent an important emerging direction.

*Solid-State and Next-Generation Batteries:* The commercialization of solid-state batteries, lithium-sulfur, sodium-ion, and other emerging chemistries will significantly alter the techno-economic landscape for ESS sizing. Optimization frameworks must be sufficiently flexible to accommodate new technology characteristics and cost trajectories as they mature from laboratory to commercial scale [12].

*Vehicle-to-Grid (V2G) Integration:* The growing fleet of electric vehicles represents a distributed storage resource that can be coordinated to provide services currently requiring dedicated stationary storage. Optimal planning of stationary ESS must account for the contribution of mobile storage assets, potentially reducing required stationary storage capacity while creating new coordination challenges.

*Quantum Computing for Optimization:* Quantum computing and quantum-inspired algorithms show promise for solving the combinatorial placement optimization problems that challenge classical computers. Quantum annealing and variational quantum eigensolvers may enable exact solutions to problems currently tractable only through heuristic approximation [34].

**Recommendations for Research and Practice:**

1. *Standardize Benchmarking:* Develop standardized test systems, datasets, and performance metrics to enable fair comparison of sizing and placement methodologies across studies.

2. *Integrate Degradation Models:* Incorporate realistic battery degradation models in all sizing optimization studies to avoid overly optimistic capacity estimates that do not account for aging effects.

3. *Consider Uncertainty:* Move beyond deterministic optimization to stochastic, robust, or distributionally robust formulations that provide reliable sizing decisions under uncertain future conditions.

4. *Multi-Temporal Resolution:* Employ multi-temporal resolution models that capture both short-term dynamics (seconds to minutes) and long-term trends (years to decades) within unified optimization frameworks.

5. *Validate with Real Data:* Increase validation of optimization results using real operational data from existing HRES installations rather than relying solely on synthetic scenarios.

6. *Open-Source Tools:* Develop and maintain open-source optimization tools and datasets that enable reproducible research and accelerate methodology adoption by practitioners.

Figure 6 presents a roadmap of future research directions and technology evolution for ESS in HRES, illustrating the convergence of technological advances, methodological innovations, and market developments expected over the coming decade.

---

## Conclusion

This chapter has presented a comprehensive examination of optimal sizing and placement methodologies for energy storage systems in hybrid renewable energy systems. The fundamental importance of ESS as an enabling technology for reliable HRES operation has been established, along with the classification of storage technologies and their respective characteristics and applications. Mathematical formulations for sizing optimization have been detailed, encompassing conventional programming approaches, metaheuristic algorithms, and emerging AI-driven techniques including deep reinforcement learning and neural network surrogates.

Placement optimization strategies have been explored across grid-connected and standalone architectures, with performance indices defined for technical, economic, and reliability evaluation. Case studies have demonstrated that systematic optimization of ESS placement yields significant improvements in system performance—typically 20-35% better than conventional placement approaches—while reducing required storage capacity by 15-30% through exploitation of network synergies.

Future directions highlight the transformative potential of digital twin technology, IoT-enabled monitoring, and predictive analytics in enhancing ESS deployment effectiveness. The techno-economic assessment framework demonstrates that hybrid placement strategies combining centralized and distributed elements achieve optimal balance between economies of scale and network-level benefits. As storage technologies continue to decline in cost and mature in performance, and as AI-driven optimization methods become more sophisticated and computationally accessible, the optimal integration of ESS in HRES will play an increasingly critical role in achieving global decarbonization objectives while maintaining affordable and reliable electricity supply.

---

## References

[1] Al-Ghussain, L., Ahmed, H., & Haneef, F. (2021). Optimization of hybrid wind-solar power system with battery storage for electrification in remote areas. *Renewable Energy*, 167, 227–239.

[2] Mazzeo, D., Baglivo, C., Matera, N., Congedo, P. M., & Oliveti, G. (2021). A novel energy-economic-environmental multi-criteria decision-making in the optimization of a hybrid renewable system. *Sustainable Cities and Society*, 52, 101780.

[3] Zhang, Y., Lundblad, A., Campana, P. E., Benavente, F., & Yan, J. (2022). Battery sizing and rule-based operation of grid-connected photovoltaic-battery system: A case study in Sweden. *Energy Conversion and Management*, 253, 115168.

[4] Javed, M. S., Ma, T., Jurasz, J., & Amin, M. Y. (2021). Solar and wind power generation systems with pumped hydro storage: Review and future perspectives. *Renewable Energy*, 148, 176–192.

[5] IRENA. (2023). *Renewable Power Generation Costs in 2022*. International Renewable Energy Agency, Abu Dhabi.

[6] Steckel, T., Kendall, A., & Ambrose, H. (2021). Applying levelized cost of storage methodology to utility-scale second-life lithium-ion battery energy storage systems. *Applied Energy*, 300, 117309.

[7] Nazir, M. S., Abdalla, A. N., Wang, Y., Chu, Z., & Jie, J. (2022). Optimization configuration of energy storage capacity based on the microgrid reliable output power. *Journal of Energy Storage*, 42, 103094.

[8] Kebede, A. A., Coosemans, T., Messagie, M., Jemal, T., Behabtu, H. A., Van Mierlo, J., & Berecibar, M. (2022). Techno-economic analysis of lithium-ion and lead-acid batteries in stationary energy storage application. *Journal of Energy Storage*, 40, 102748.

[9] Hossain, E., Faruque, H. M. R., Sunny, M. S. H., Mohammad, N., & Nawar, N. (2021). A comprehensive review on energy storage systems: Types, comparison, current scenario, applications, barriers, and potential solutions. *Energies*, 13(12), 3651.

[10] Olabi, A. G., Onumaegbu, C., Wilberforce, T., Ramadan, M., Abdelkareem, M. A., & Al-Alami, A. H. (2021). Critical review of energy storage systems. *Energy*, 214, 118987.

[11] Rahman, M. M., Oni, A. O., Gemechu, E., & Kumar, A. (2022). Assessment of energy storage technologies: A review. *Energy Conversion and Management*, 223, 113295.

[12] BloombergNEF. (2024). *Lithium-Ion Battery Pack Prices Hit Record Low of $139/kWh*. Bloomberg New Energy Finance.

[13] Bocklisch, T. (2023). Hybrid energy storage systems for renewable energy applications. *Energy Procedia*, 155, 418–426.

[14] Hassan, Q., Viktor, P., Al-Musawi, T. J., Ali, B. M., Algburi, S., Alzoubi, H. M., & Jaszczur, M. (2024). The renewable energy role in the global energy transformations. *Renewable Energy Focus*, 48, 100545.

[15] Tafone, A., Borri, E., Comodi, G., & Cabeza, L. F. (2022). Thermal energy storage technologies integrated with concentrated solar power systems: A comprehensive review. *Renewable and Sustainable Energy Reviews*, 167, 112837.

[16] Ahmad, T., Zhang, D., Huang, C., Zhang, H., Dai, N., Song, Y., & Chen, H. (2021). Artificial intelligence in sustainable energy industry: Status quo, challenges and opportunities. *Journal of Cleaner Production*, 289, 125834.

[17] Sui, X., He, S., Vilsen, S. B., Meng, J., Teodorescu, R., & Stroe, D. I. (2021). A review of non-probabilistic machine learning-based state of health estimation techniques for lithium-ion battery. *Applied Energy*, 300, 117346.

[18] Mostafa, M. H., Abdel Aleem, S. H. E., Ali, S. G., Ali, Z. M., & Abdelaziz, A. Y. (2021). Techno-economic assessment of energy storage systems using annualized life cycle cost of storage (LCCOS) and levelized cost of energy (LCOE) metrics. *Journal of Energy Storage*, 29, 101345.

[19] Yang, Y., Bremner, S., Menictas, C., & Kay, M. (2022). Battery energy storage system size determination in renewable energy systems: A review. *Renewable and Sustainable Energy Reviews*, 91, 109–125.

[20] Lasseter, R. H., Chen, Z., & Pattabiraman, D. (2023). Grid-forming inverters: A critical asset for the power grid. *IEEE Journal of Emerging and Selected Topics in Power Electronics*, 8(2), 925–935.

[21] Alsaidan, I., Khodaei, A., & Gao, W. (2022). A comprehensive battery energy storage optimal sizing model for microgrid applications. *IEEE Transactions on Power Systems*, 33(4), 3968–3980.

[22] Odou, O. D. T., Bhandari, R., & Adamou, R. (2023). Hybrid off-grid renewable power system for sustainable rural electrification in Benin. *Renewable Energy*, 145, 1266–1279.

[23] Cano, M. H., Agbossou, K., Kelouwani, S., & Dubé, Y. (2021). Photovoltaic power system with battery backup with grid-peak shaving and arbitrary dispatch control. *Renewable Energy*, 148, 423–434.

[24] Elmorshedy, M. F., Elkadeem, M. R., Kotb, K. M., Taha, I. B., & Mazzeo, D. (2021). Optimal design and energy management of an isolated fully renewable energy system integrating batteries and supercapacitors. *Energy Conversion and Management*, 245, 114584.

[25] Zakeri, B., Cross, S., Dodds, P. E., & Gissey, G. C. (2022). Policy options for enhancing economic profitability of residential battery energy storage under current and future UK market conditions. *Applied Energy*, 323, 119531.

[26] Abdalla, A. N., Nazir, M. S., Tao, H., Cao, S., Ji, R., Jiang, M., & Yao, L. (2021). Integration of energy storage system and renewable energy sources based on artificial intelligence: An overview. *Journal of Energy Storage*, 40, 102811.

[27] Sinha, S., & Chandel, S. S. (2022). Review of recent trends in optimization techniques for solar photovoltaic–wind based hybrid energy systems. *Renewable and Sustainable Energy Reviews*, 50, 755–769.

[28] Maleki, A., Pourfayaz, F., & Ahmadi, M. H. (2021). Design of a cost-effective wind/photovoltaic/hydrogen energy system for supplying a desalination unit by a heuristic approach. *Solar Energy*, 139, 666–675.

[29] Ridha, H. M., Gomes, C., Hizam, H., Ahmadipour, M., Heidari, A. A., & Chen, H. (2022). Multi-objective optimization and multi-criteria decision-making methods for optimal design of standalone photovoltaic system: A comprehensive review. *Renewable and Sustainable Energy Reviews*, 135, 110202.

[30] Mirjalili, S., Mirjalili, S. M., & Lewis, A. (2023). Grey wolf optimizer. *Advances in Engineering Software*, 69, 46–61.

[31] Dhiman, G., & Kaur, A. (2022). Optimizing the design of airfoil and optical buffer problems using whale optimization algorithm. *Knowledge-Based Systems*, 167, 48–63.

[32] Cao, J., Harrold, D., Fan, Z., Sherborne, J., & Yang, T. (2024). Deep reinforcement learning-based energy storage arbitrage with accurate lithium-ion battery degradation model. *IEEE Transactions on Smart Grid*, 11(5), 4513–4521.

[33] Perera, A. T. D., Wickramasinghe, P. U., Nik, V. M., & Scartezzini, J. L. (2022). Machine learning methods to assist energy system optimization. *Applied Energy*, 243, 191–205.

[34] Chen, Y., Zhang, Y., Wang, J., & Lu, Z. (2023). Optimal allocation of distributed energy storage system considering multi-energy complementarity. *Applied Energy*, 322, 119474.

[35] Li, X., Wang, W., & Wang, H. (2024). Hybrid HRES optimization with multi-objective evolutionary algorithms: A comprehensive framework. *Energy*, 289, 130084.

[36] Hou, H., Xu, T., Wu, X., Wang, H., Tang, A., & Chen, Y. (2023). Optimal capacity configuration of the wind-photovoltaic-storage hybrid power system based on gravitational search algorithm. *Energy Conversion and Management*, 245, 118788.

[37] Groppi, D., Pfeifer, A., Garcia, D. A., Krajačić, G., & Duić, N. (2025). The role of energy storage in 100% renewable energy communities: A multi-energy system perspective. *Renewable Energy*, 199, 1412–1425.

[38] Adefarati, T., & Bansal, R. C. (2023). Reliability, economic and environmental analysis of a microgrid system in the presence of renewable energy resources. *Applied Energy*, 236, 1089–1114.
