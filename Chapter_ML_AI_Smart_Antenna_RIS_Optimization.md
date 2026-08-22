# Machine Learning and AI for Smart Antenna and RIS Optimization

## Abstract

The rapid evolution of wireless communication systems toward sixth-generation (6G) and beyond has necessitated the development of intelligent, adaptive antenna systems and reconfigurable intelligent surfaces (RIS) capable of meeting unprecedented demands for data throughput, spectral efficiency, and energy performance. This chapter presents a comprehensive examination of machine learning (ML) and artificial intelligence (AI) techniques applied to the optimization of smart antenna systems and RIS configurations. Beginning with foundational concepts of smart antennas, beamforming, and RIS architectures, the chapter systematically explores AI-driven design frameworks, data-driven antenna modeling, adaptive beamforming optimization, terahertz antenna design, RIS phase configuration, deep reinforcement learning for dynamic RIS control, and joint optimization of communication resources. Emerging applications in 6G networks, challenges in implementation, and future research directions involving federated learning, explainable AI, and intelligent metasurfaces are discussed. The integration of AI methodologies into antenna and RIS design represents a paradigm shift from conventional optimization approaches, enabling real-time adaptation, enhanced network performance, and intelligent wireless environments for next-generation communication systems.

**Keywords:** Smart antennas, reconfigurable intelligent surfaces, machine learning, deep learning, beamforming, 6G communications, reinforcement learning, terahertz antennas, phase optimization, intelligent wireless environments

---

## Section 1: Fundamentals of AI-Enabled Smart Antennas and Reconfigurable Intelligent Surfaces

### 1.1 Smart Antenna Systems and RIS for Next-Generation Communication Networks

The evolution of wireless communication systems from first-generation analog networks to the emerging sixth-generation (6G) infrastructure has been characterized by exponential increases in data rates, connectivity density, and spectral efficiency requirements. Smart antenna systems, which incorporate signal processing capabilities to adaptively control radiation patterns, have emerged as fundamental enabling technologies for meeting these demands (Björnson et al., 2019). Unlike conventional antenna systems with fixed radiation characteristics, smart antennas employ adaptive algorithms to dynamically adjust beam directions, null placements, and spatial multiplexing configurations based on real-time channel conditions and user requirements.

Smart antenna architectures can be broadly classified into switched-beam systems and adaptive array systems. Switched-beam systems select from a predetermined set of radiation patterns based on signal strength measurements, while adaptive arrays continuously adjust element weights to optimize performance metrics such as signal-to-interference-plus-noise ratio (SINR) and capacity (Rappaport et al., 2019). The transition to massive multiple-input multiple-output (MIMO) systems, incorporating hundreds or thousands of antenna elements, has dramatically increased the degrees of freedom available for spatial signal processing, enabling simultaneous service to numerous users through spatial multiplexing and beamforming techniques.

Reconfigurable intelligent surfaces represent a revolutionary paradigm in wireless communications, offering the ability to intelligently control the propagation environment rather than merely adapting to it (Wu & Zhang, 2020). A RIS consists of a planar surface comprising numerous passive reflecting elements, each capable of independently adjusting the phase shift applied to incident electromagnetic waves. By coordinating the phase shifts across all elements, a RIS can constructively combine reflected signals at desired locations, effectively creating programmable wireless channels. This capability transforms the wireless propagation environment from an uncontrollable factor into an optimizable design parameter, as illustrated in Figure 1.

**[Figure 1: Architecture of a RIS-assisted smart antenna communication system showing the base station with adaptive antenna array, RIS panel with configurable reflecting elements, and multiple user equipment in a multi-path propagation environment. The figure depicts the direct path, reflected paths through RIS, and the phase-shift control mechanism.]**

The integration of RIS with smart antenna systems creates synergistic benefits for next-generation networks. While smart antennas optimize the transmitted signal characteristics, RIS elements shape the propagation channel itself, providing complementary control over the end-to-end communication link (Di Renzo et al., 2020). This combined approach is particularly valuable for terahertz (THz) communication systems envisioned for 6G, where severe path loss and atmospheric absorption limit coverage. RIS deployments can establish virtual line-of-sight paths, extend coverage to obstructed areas, and enhance signal strength at user locations that would otherwise experience inadequate service quality.

The configuration space for joint antenna-RIS systems is extraordinarily large. A RIS with N elements, each supporting B-bit phase resolution, presents 2^(NB) possible configurations, rendering exhaustive search computationally infeasible for practical deployments with hundreds or thousands of elements (Huang et al., 2019). This computational challenge, combined with the dynamic nature of wireless channels and user mobility, motivates the application of machine learning and artificial intelligence techniques for efficient optimization. As shown in Figure 1, the complexity of managing multiple signal paths simultaneously through both antenna beamforming and RIS phase configuration demands intelligent algorithms capable of real-time decision-making in high-dimensional spaces.

### 1.2 Machine Learning and Artificial Intelligence Fundamentals for Wireless Optimization

Machine learning encompasses a broad family of computational methods that enable systems to improve performance on specific tasks through experience, without being explicitly programmed for each scenario (Goodfellow et al., 2016). In the context of wireless communication optimization, ML techniques provide powerful tools for learning complex relationships between system parameters and performance metrics, adapting to dynamic environments, and discovering optimization strategies that exceed the capabilities of conventional approaches.

Supervised learning algorithms learn mappings from input features to output labels using labeled training data. For antenna and RIS optimization, supervised learning enables the development of surrogate models that predict electromagnetic performance characteristics from design parameters, dramatically reducing the computational cost compared to full-wave electromagnetic simulations (Chen et al., 2020). Neural networks, support vector machines, random forests, and Gaussian process regression represent commonly employed supervised learning methods, each offering distinct advantages in terms of accuracy, computational efficiency, and interpretability.

Unsupervised learning techniques discover hidden structures and patterns in unlabeled data. Clustering algorithms identify natural groupings in antenna design spaces or wireless channel characteristics, while dimensionality reduction methods extract compact representations of high-dimensional electromagnetic data. These capabilities are particularly valuable for analyzing large datasets generated by antenna measurement campaigns or channel sounding experiments, revealing underlying patterns that inform optimization strategies.

Reinforcement learning (RL) represents a fundamentally different paradigm, where an agent learns optimal decision-making policies through interaction with an environment, receiving reward signals that guide behavior toward desired outcomes (Sutton & Barto, 2018). For dynamic wireless systems, RL enables real-time adaptation of antenna configurations and RIS phase shifts in response to changing channel conditions, user mobility, and traffic demands. Deep reinforcement learning (DRL), which combines deep neural networks with RL algorithms, has demonstrated remarkable success in handling the high-dimensional state and action spaces characteristic of modern wireless systems.

Deep learning, employing neural networks with multiple layers of abstraction, has achieved unprecedented performance in pattern recognition, function approximation, and sequential decision-making tasks. Convolutional neural networks (CNNs) process spatial data structures relevant to antenna arrays and RIS configurations, recurrent neural networks (RNNs) capture temporal dependencies in wireless channels, and generative adversarial networks (GANs) synthesize realistic channel data for training and evaluation purposes. Table 1 summarizes the primary ML categories and their applications in antenna and RIS optimization.

**[Table 1: Machine Learning Categories and Applications in Smart Antenna and RIS Optimization]**

| ML Category | Key Algorithms | Antenna Applications | RIS Applications |
|---|---|---|---|
| Supervised Learning | Neural Networks, SVM, Random Forest, Gaussian Process | Antenna parameter prediction, radiation pattern modeling, impedance matching | Phase shift prediction, channel estimation, beam direction classification |
| Unsupervised Learning | K-means, PCA, Autoencoders, DBSCAN | Design space exploration, channel clustering, feature extraction | RIS element grouping, environmental classification, anomaly detection |
| Reinforcement Learning | Q-learning, DQN, PPO, A3C | Adaptive beamforming, beam tracking, power control | Dynamic phase configuration, user association, resource allocation |
| Deep Learning | CNN, RNN, GAN, Transformer | Near-field pattern prediction, array synthesis, mutual coupling compensation | Large-scale RIS optimization, channel prediction, generative channel modeling |

The application of ML to wireless optimization involves several key considerations. Training data acquisition requires either extensive measurements, electromagnetic simulations, or system-level simulations that accurately capture the phenomena of interest. The computational cost of training must be amortized over multiple inference operations to justify the initial investment. Additionally, the deployment environment must provide sufficient computational resources for real-time inference, and the ML models must generalize effectively to conditions not represented in the training data. As summarized in Table 1, different ML categories offer complementary capabilities that collectively address the diverse optimization challenges in smart antenna and RIS systems.

### 1.3 AI-Driven Antenna and RIS Design Frameworks

The conventional antenna design process relies heavily on experienced engineers iterating between electromagnetic simulation tools and geometric modifications, guided by physical intuition and established design rules. This process is time-consuming, may not explore the full design space, and often converges to local optima rather than globally optimal solutions (Koziel & Bandler, 2022). AI-driven design frameworks fundamentally transform this process by automating design space exploration, learning from accumulated simulation data, and discovering novel configurations that may not be intuitively apparent to human designers.

AI-based antenna design frameworks typically incorporate three primary components: a design space representation module, a performance prediction engine, and an optimization algorithm. The design space representation encodes antenna geometries, material properties, and excitation configurations in formats amenable to ML processing (Sharma et al., 2022). Parameterized representations describe antenna structures through a set of continuous or discrete variables, while image-based representations capture arbitrary geometries through pixel maps or occupancy grids. The performance prediction engine, trained on electromagnetic simulation data, rapidly evaluates candidate designs without requiring full-wave simulations, enabling exploration of millions of configurations within practical time constraints.

For RIS design optimization, AI frameworks must address the configuration of individual element phase shifts, the physical design of unit cells, the overall surface geometry, and the control architecture (Pan et al., 2021). The phase shift optimization problem involves finding the optimal set of reflection coefficients that maximize a given performance metric, subject to hardware constraints such as discrete phase quantization and element coupling. AI approaches can efficiently navigate this discrete, high-dimensional optimization landscape by learning the mapping between channel conditions and optimal phase configurations.

Transfer learning represents a particularly valuable technique for antenna and RIS design, enabling knowledge gained from one design problem to accelerate solutions for related problems. A neural network trained to predict the performance of one antenna type can be fine-tuned for a related structure with significantly less additional training data. Similarly, RIS optimization policies learned for one deployment scenario can be adapted to new environments with minimal retraining, reducing the computational burden of site-specific optimization.

Multi-objective optimization frameworks employ AI techniques to simultaneously optimize multiple conflicting performance metrics. Antenna designs must balance gain, bandwidth, efficiency, size, and manufacturing complexity, while RIS configurations must trade off spectral efficiency, energy consumption, fairness among users, and computational overhead. Multi-objective evolutionary algorithms guided by neural network surrogate models efficiently generate Pareto-optimal solution sets, providing designers with a comprehensive view of achievable performance trade-offs.

---

## Section 2: Machine Learning-Based Smart Antenna Optimization

### 2.1 Data-Driven Antenna Modeling and Performance Prediction

Data-driven modeling approaches leverage machine learning algorithms to construct accurate predictive models of antenna performance from training data generated through electromagnetic simulations or physical measurements. These surrogate models serve as computationally efficient alternatives to full-wave simulation tools, enabling rapid design exploration, real-time optimization, and sensitivity analysis that would be impractical with conventional methods.

The development of ML-based antenna models follows a systematic workflow comprising data generation, feature engineering, model selection, training, validation, and deployment. Data generation involves executing electromagnetic simulations across a carefully designed set of input parameter combinations, capturing the relationship between design variables and performance metrics. Design of experiments techniques, including Latin hypercube sampling and orthogonal arrays, ensure efficient coverage of the design space while minimizing the required number of simulations.

Neural network-based surrogate models have demonstrated exceptional accuracy in predicting antenna parameters including return loss, gain, radiation patterns, impedance, and efficiency across multi-dimensional design spaces. Deep neural networks with multiple hidden layers capture the nonlinear relationships between geometric parameters and electromagnetic performance, achieving prediction errors below 1% for well-trained models (Wu et al., 2021). Gaussian process regression provides probabilistic predictions with uncertainty estimates, enabling active learning strategies that intelligently select new simulation points to maximally improve model accuracy.

The prediction of mutual coupling between antenna elements in array configurations represents a particularly challenging modeling task due to the complex electromagnetic interactions that depend on element spacing, orientation, and the surrounding structure (Yao et al., 2022). ML models trained on coupling data enable rapid array optimization by providing instant evaluations of coupling characteristics for candidate configurations, facilitating the design of arrays with reduced mutual coupling and improved isolation between elements.

Table 2 presents a comparison of ML techniques for antenna performance prediction, highlighting their respective strengths and limitations for different application scenarios.

**[Table 2: Comparison of Machine Learning Techniques for Antenna Performance Prediction]**

| ML Technique | Prediction Accuracy | Training Data Required | Computational Cost (Inference) | Handling of High Dimensionality | Uncertainty Quantification |
|---|---|---|---|---|---|
| Artificial Neural Networks | High (RMSE < 2%) | Moderate (500–5000 samples) | Very Low (ms) | Excellent | Limited |
| Gaussian Process Regression | Very High (RMSE < 1%) | Low (100–500 samples) | Moderate (scales with N³) | Poor (curse of dimensionality) | Excellent |
| Support Vector Regression | High (RMSE < 3%) | Moderate (200–2000 samples) | Low (ms) | Good | Limited |
| Random Forest | Moderate (RMSE < 5%) | Low (100–1000 samples) | Low (ms) | Good | Moderate (via ensemble variance) |
| Deep Learning (CNN/DNN) | Very High (RMSE < 1%) | High (5000–50000 samples) | Very Low (ms) | Excellent | Limited (without Bayesian extensions) |

As detailed in Table 2, the choice of ML technique depends on the specific requirements regarding prediction accuracy, available training data, computational resources, and the need for uncertainty quantification. For initial design exploration with limited simulation budgets, Gaussian process regression provides excellent accuracy with uncertainty estimates. For production optimization systems requiring instantaneous predictions across high-dimensional design spaces, deep neural networks offer the best combination of accuracy and computational efficiency.

Convolutional neural networks have been applied to predict antenna performance directly from geometric representations encoded as images, eliminating the need for explicit parameterization of antenna structures. This approach enables the modeling of arbitrarily complex geometries, including fractal structures, defected ground planes, and metamaterial-inspired designs that resist compact parametric description. The CNN learns relevant geometric features automatically from training data, identifying patterns that correlate with specific electromagnetic behaviors.

The integration of physics-informed constraints into ML models represents an emerging approach that combines data-driven learning with electromagnetic theory. Physics-informed neural networks incorporate Maxwell's equations and boundary conditions as regularization terms during training, ensuring that predictions satisfy fundamental physical laws even when extrapolating beyond training data distributions. This approach reduces training data requirements while improving model reliability for antenna parameter prediction across diverse operating conditions and geometric configurations.

Transfer learning strategies further enhance the efficiency of data-driven antenna modeling by leveraging knowledge from related design problems. A surrogate model trained for one antenna type can be adapted to predict the performance of structurally similar antennas with minimal additional training data. This capability is particularly valuable for design families where systematic variations in geometry produce predictable changes in electromagnetic performance, enabling rapid evaluation of design variants without independent model development for each configuration.

### 2.2 AI-Based Beamforming and Beam-Steering Optimization

Beamforming constitutes a fundamental signal processing technique in smart antenna systems, where the complex weights applied to individual antenna elements are optimized to shape the array radiation pattern according to desired objectives. Traditional beamforming approaches, including minimum variance distortionless response (MVDR), maximum signal-to-noise ratio (Max-SNR), and zero-forcing methods, rely on accurate channel state information and involve matrix operations whose complexity scales with the number of antenna elements and users.

AI-based beamforming methods address several limitations of conventional approaches, including sensitivity to channel estimation errors, computational complexity in massive MIMO systems, and inability to optimize non-convex objectives. Deep learning-based beamforming networks learn to generate near-optimal beam weights from available channel observations, achieving performance comparable to iterative optimization algorithms at a fraction of the computational cost (Xia et al., 2020). These networks can be trained to operate under imperfect channel conditions, providing robustness to estimation errors that degrade conventional methods.

The beam management problem in millimeter-wave (mmWave) and sub-THz systems involves selecting appropriate beam directions from a codebook, tracking beam orientations as users move, and performing beam recovery when links are interrupted by blockages. Deep learning approaches to beam management exploit spatial and temporal correlations in channel measurements, enabling faster beam alignment with reduced overhead compared to exhaustive beam sweeping procedures. Recurrent neural networks and long short-term memory (LSTM) networks capture the temporal evolution of optimal beam directions, enabling predictive beam tracking that anticipates user movement.

Figure 2 illustrates the architecture of an AI-based adaptive beamforming system, showing the integration of neural network processing with conventional array signal processing components.

**[Figure 2: AI-based adaptive beamforming architecture showing input channel measurements, neural network processing pipeline (feature extraction CNN, temporal modeling LSTM, beam weight prediction fully-connected layers), and output beamforming weight vectors applied to the antenna array elements for spatial signal processing.]**

Hybrid beamforming architectures, which combine analog phase shifters with digital baseband processing, present unique optimization challenges due to the constant-modulus constraint on analog weights and the coupled nature of analog and digital processing stages. AI methods decompose this problem into learnable sub-problems, jointly optimizing analog and digital precoding matrices to approach the performance of fully digital systems while maintaining the hardware efficiency of hybrid architectures. As depicted in Figure 2, the neural network architecture processes channel information through successive stages of feature extraction, temporal modeling, and weight prediction, enabling end-to-end optimization of the complete beamforming pipeline.

Multi-user beamforming optimization in massive MIMO systems involves determining precoding vectors that simultaneously serve multiple users while managing inter-user interference. Deep learning approaches learn interference management strategies from training data, discovering beamforming solutions that balance sum-rate maximization with fairness constraints. Graph neural networks (GNNs) have shown particular promise for this application, as they naturally model the interaction topology between base stations, users, and interference links.

### 2.3 Optimization of THz Antennas Using Intelligent Algorithms

Terahertz communication systems, operating in the frequency range from 0.1 to 10 THz, represent a promising technology for achieving terabit-per-second data rates envisioned for 6G networks (Akyildiz et al., 2022). However, the unique propagation characteristics at THz frequencies, including severe free-space path loss, atmospheric molecular absorption, and limited diffraction, impose stringent requirements on antenna performance. THz antennas must achieve high gain and directivity to overcome path loss, while maintaining sufficient bandwidth to support ultra-wideband modulation schemes.

AI-assisted optimization of THz antenna designs addresses the complex multi-parameter design space that characterizes high-frequency antenna structures. At THz frequencies, antenna dimensions approach the scale of manufacturing tolerances, making performance highly sensitive to geometric variations. Machine learning models capture these sensitivities, enabling robust design optimization that accounts for fabrication uncertainties and ensures reliable performance across manufacturing variations.

Evolutionary algorithms enhanced by neural network surrogate models efficiently optimize THz antenna geometries, including patch dimensions, slot configurations, substrate properties, and feeding mechanisms. The surrogate model provides rapid performance evaluations that guide the evolutionary search, while periodic full-wave simulations update and validate the surrogate model. This co-evolutionary approach achieves near-optimal designs with computational budgets reduced by factors of 10 to 100 compared to simulation-only optimization.

Graphene-based THz antennas exploit the unique electromagnetic properties of graphene, including tunable surface conductivity and support for surface plasmon polariton modes, to achieve reconfigurable radiation characteristics. AI optimization frameworks for graphene antennas must account for the frequency-dependent and bias-dependent material properties, the quantum mechanical effects at nanoscale dimensions, and the coupling between electrical and electromagnetic domains. Neural networks trained on multi-physics simulation data enable efficient exploration of the expanded design space introduced by graphene tunability. These multi-physics models bridge the gap between idealized electromagnetic analysis and real-world device behavior, accounting for thermal effects, mechanical stress, and material aging.

THz antenna array optimization involves the joint determination of element geometries, inter-element spacings, and feeding network configurations to achieve desired radiation characteristics. The array factor computation at THz frequencies must account for mutual coupling effects that become significant when elements are closely spaced relative to the wavelength. AI-based optimization handles these coupled design variables simultaneously, discovering array configurations that achieve superior performance compared to independent optimization of individual parameters.

---

## Section 3: AI-Enabled RIS Optimization and Intelligent Wireless Environments

### 3.1 Machine Learning for RIS Phase Configuration and Beam Management

The optimization of RIS phase configurations constitutes a central challenge in RIS-assisted communication systems, requiring the determination of optimal reflection coefficients for each element to maximize system performance metrics (Wu & Zhang, 2020). For a RIS with N elements, each supporting continuous phase shifts in [0, 2π), the optimization space is N-dimensional and generally non-convex, with performance landscapes that exhibit numerous local optima due to the periodic nature of phase parameters (Guo et al., 2020).

Machine learning approaches to RIS phase optimization can be categorized into offline learning methods, which train models to predict optimal configurations from channel state information, and online learning methods, which adapt phase configurations in real-time through interaction with the wireless environment. Offline methods employ deep neural networks trained on datasets of channel realizations paired with corresponding optimal phase configurations obtained through conventional optimization (Taha et al., 2021). Once trained, these networks generate near-optimal phase configurations in milliseconds, enabling practical real-time operation.

The channel estimation problem for RIS-assisted systems presents unique challenges due to the passive nature of RIS elements, which cannot transmit or process pilot signals independently. ML-based channel estimation methods exploit the structural properties of RIS channels, including sparsity in angular domains and correlation between adjacent elements, to achieve accurate estimation with reduced pilot overhead. Deep learning architectures such as deep image prior and convolutional sparse coding have been applied to reconstruct full channel matrices from limited measurements, leveraging the inherent structure of RIS-assisted channels.

Codebook-based RIS beam management employs AI techniques to design optimal phase shift codebooks and select appropriate codewords based on real-time measurements. Unlike antenna beamforming codebooks that are typically designed offline using geometric criteria, RIS codebooks must account for the specific deployment geometry, surrounding environment, and distribution of user locations (Alexandropoulos et al., 2020). ML-based codebook design learns from deployment-specific data to create customized codebooks that outperform universal designs, adapting to the unique characteristics of each installation.

Figure 3 presents the operational framework for ML-based RIS phase optimization, illustrating the data flow from channel measurements through the neural network prediction system to the RIS controller.

**[Figure 3: Machine learning framework for RIS phase optimization showing the complete pipeline: (a) channel measurement acquisition from base station and users, (b) feature extraction and preprocessing, (c) deep neural network prediction of optimal phase configurations, (d) RIS controller implementing predicted phase shifts, and (e) feedback loop for online model refinement.]**

The scalability of ML-based RIS optimization to large surfaces with thousands of elements requires architectural innovations in the neural network design. Convolutional neural networks exploit the spatial locality of RIS element interactions, reducing parameter counts and improving generalization (Huang et al., 2020). Attention mechanisms identify the most critical elements for performance optimization, enabling efficient computation even for very large surfaces. As shown in Figure 3, the complete optimization pipeline integrates measurement acquisition, intelligent processing, and controller implementation in a closed-loop architecture that enables continuous performance improvement through online learning.

### 3.2 Deep Reinforcement Learning for Dynamic RIS Control

Dynamic wireless environments, characterized by user mobility, temporal traffic variations, and time-varying channel conditions, demand RIS configurations that adapt continuously to maintain optimal performance. Deep reinforcement learning provides a natural framework for this sequential decision-making problem, where the RIS controller agent observes the current system state, selects phase configurations (actions), and receives performance feedback (rewards) that guide learning toward optimal policies (Feng et al., 2020).

The formulation of RIS control as a Markov decision process (MDP) involves defining appropriate state representations, action spaces, reward functions, and transition dynamics. The state typically encompasses available channel measurements, current phase configurations, user locations, and quality-of-service metrics (Yang et al., 2021). The action space corresponds to the set of achievable phase configurations, which may be discretized to reduce complexity or parameterized using continuous action spaces. The reward function encodes the optimization objective, such as sum-rate maximization, minimum-rate guarantee, or energy efficiency.

Deep Q-Networks (DQN) and their variants, including Double DQN, Dueling DQN, and Prioritized Experience Replay, have been applied to discrete RIS phase optimization problems where elements support a limited number of phase states. These algorithms learn action-value functions that estimate the expected cumulative reward for each phase configuration in each system state, enabling greedy action selection that maximizes long-term performance. However, the exponential growth of the action space with the number of elements limits the applicability of DQN to relatively small RIS deployments.

Policy gradient methods, including Proximal Policy Optimization (PPO) and Advantage Actor-Critic (A2C), address the scalability limitations of value-based methods by directly parameterizing and optimizing the policy network (Nguyen et al., 2022). These algorithms output continuous phase shift values or probabilities over discrete options, scaling more gracefully to large action spaces. The actor-critic architecture separates the policy (actor) from the value estimation (critic), enabling stable training with reduced variance in gradient estimates.

Table 3 presents a comparative analysis of DRL algorithms for RIS control, evaluating their performance characteristics across relevant metrics.

**[Table 3: Comparative Analysis of Deep Reinforcement Learning Algorithms for Dynamic RIS Control]**

| DRL Algorithm | Action Space | Scalability (Elements) | Convergence Speed | Sample Efficiency | Real-Time Capability | Performance vs. Optimal |
|---|---|---|---|---|---|---|
| DQN | Discrete | Limited (<64 elements) | Moderate | Low | High (after training) | 90–95% |
| Double DQN | Discrete | Limited (<64 elements) | Moderate | Moderate | High (after training) | 92–96% |
| PPO | Continuous/Discrete | Good (<256 elements) | Fast | Moderate | High (after training) | 93–97% |
| A3C | Continuous/Discrete | Good (<256 elements) | Fast | Moderate | High (after training) | 92–96% |
| SAC | Continuous | Excellent (<1024 elements) | Moderate | High | Moderate | 95–98% |
| Multi-Agent DRL | Continuous/Discrete | Excellent (>1024 elements) | Slow | Low | Moderate | 90–95% |

Multi-agent reinforcement learning (MARL) frameworks decompose the large-scale RIS optimization problem into smaller sub-problems assigned to individual agents, each controlling a subset of RIS elements (Xu et al., 2022). This distributed approach enables scalability to very large surfaces while maintaining manageable computational requirements for each agent. Cooperative MARL algorithms, such as QMIX and MAPPO, coordinate agent behaviors through shared reward structures and communication mechanisms, achieving collective performance that approaches centralized optimization. As demonstrated in Table 3, different DRL algorithms exhibit distinct trade-offs between scalability, sample efficiency, and optimality gap, necessitating careful algorithm selection based on deployment requirements.

### 3.3 Joint Optimization of Antennas, RIS, and Communication Resources

The full potential of RIS-assisted communication systems is realized through joint optimization of all available degrees of freedom, including transmit beamforming at the base station, RIS phase configurations, power allocation across users and subcarriers, user scheduling, and RIS element activation patterns (Zhang & Dai, 2021). This joint optimization problem is inherently more complex than individual component optimization due to the coupling between decision variables and the resulting non-convex, mixed-integer optimization formulation.

AI-driven joint optimization approaches employ deep learning architectures that simultaneously output multiple optimization variables from shared input features representing the system state. End-to-end learning frameworks train neural networks to directly map from channel observations to jointly optimized configurations, bypassing the need for explicit problem decomposition (Kim et al., 2021). These approaches capture the interdependencies between optimization variables that are often lost in conventional alternating optimization methods.

The resource allocation dimension involves distributing available power, bandwidth, and time resources among users to achieve desired system objectives such as sum-rate maximization, proportional fairness, or minimum quality-of-service guarantees. When combined with RIS phase optimization, resource allocation decisions must account for the RIS-modified channel characteristics, creating a coupled optimization problem where optimal resource allocation depends on the RIS configuration and vice versa. Deep learning methods jointly learn resource allocation and RIS configuration policies, achieving near-optimal performance with polynomial computational complexity.

User scheduling in RIS-assisted systems determines which users are served in each time slot and which RIS configurations are employed for each scheduling decision. The scheduling problem interacts with RIS optimization because different user subsets benefit from different phase configurations (Mu et al., 2022). AI-based scheduling algorithms learn to group users with compatible RIS requirements, maximizing the system throughput while ensuring fairness through long-term reward formulations that penalize persistent service denial.

The integration of sensing and communication functions in RIS-assisted systems introduces additional optimization dimensions, requiring the RIS to simultaneously enhance communication performance and provide environmental sensing capabilities (Liu et al., 2022). Joint communication and sensing optimization employs multi-objective AI frameworks that balance potentially conflicting objectives, generating Pareto-optimal configurations that allow system operators to select appropriate operating points based on current priorities.

The computational architecture for joint optimization must balance optimization quality with latency requirements. Centralized approaches achieve optimal performance but introduce communication overhead and single points of failure, while distributed architectures provide resilience and reduced latency at the cost of potentially suboptimal solutions. Hierarchical optimization frameworks combine centralized strategic planning with distributed tactical execution, allocating long-term resource decisions to centralized processors while delegating rapid phase adjustments to local RIS controllers equipped with lightweight neural network models.

---

## Section 4: Emerging Applications, Challenges, and Future Perspectives

### 4.1 AI-Driven RIS-Assisted THz Networks for 6G and Beyond

The convergence of AI, RIS, and THz technologies creates transformative capabilities for 6G communication systems, enabling applications that are infeasible with current infrastructure. Ultra-high-speed indoor communication systems employ AI-optimized RIS deployments to overcome the severe propagation limitations of THz signals within buildings, creating reliable multi-gigabit links through intelligent reflection management (Sarieddeen et al., 2021). AI algorithms continuously optimize RIS configurations to maintain connectivity as users move and environmental conditions change, compensating for the narrow beams and sensitivity to blockages that characterize THz communications.

Smart factory applications leverage RIS-assisted THz networks to provide ultra-reliable, low-latency communication for industrial automation systems. AI-driven optimization ensures that RIS configurations satisfy strict latency and reliability requirements for machine control applications while maximizing spectral efficiency for concurrent data-intensive monitoring streams (Tariq et al., 2020). The deterministic nature of factory environments enables effective offline optimization supplemented by online adaptation for dynamic elements such as moving robots and personnel.

Vehicular communication networks present extreme challenges for RIS optimization due to high mobility, rapidly changing channel conditions, and stringent latency requirements. AI-based predictive RIS control exploits trajectory information from positioning systems and historical mobility patterns to anticipate optimal configurations before they are needed, eliminating the latency associated with reactive optimization. Deep learning models trained on vehicle trajectory data predict future channel conditions and pre-compute RIS configurations, enabling seamless connectivity for vehicles moving at highway speeds in complex urban and suburban environments.

Figure 4 illustrates the application scenarios for AI-driven RIS-assisted THz networks in future 6G environments, depicting the diverse use cases and their specific optimization requirements.

**[Figure 4: Application scenarios for AI-driven RIS-assisted THz networks in 6G environments showing: (a) indoor high-speed communications with ceiling-mounted RIS panels, (b) smart factory with distributed RIS for robotic control, (c) vehicular network with roadside RIS for V2X communications, and (d) aerial network with UAV-mounted RIS for coverage extension in urban environments.]**

Unmanned aerial vehicle (UAV) mounted RIS platforms introduce three-dimensional mobility to the RIS deployment paradigm, enabling dynamic positioning of reflecting surfaces to optimize coverage and capacity (Li et al., 2021). AI algorithms jointly optimize UAV trajectories and RIS configurations, navigating the coupled spatial-electromagnetic optimization space to maximize network performance over extended service periods. As illustrated in Figure 4, these diverse application scenarios demonstrate the versatility of AI-driven RIS optimization across different environments, mobility conditions, and performance requirements.

Integrated sensing and communication (ISAC) systems employ RIS to simultaneously support wireless data transmission and environmental radar sensing. AI optimization frameworks manage the dual-functional operation, allocating RIS resources between communication and sensing objectives based on real-time demand assessment (Chepuri et al., 2023). Deep learning-based resource allocation dynamically partitions RIS elements between communication-optimal and sensing-optimal configurations, maximizing the joint utility of both functions.

The deployment of RIS in healthcare environments represents another promising application domain, where AI-optimized surfaces can enhance wireless connectivity for medical devices while simultaneously minimizing electromagnetic exposure to patients and staff. Intelligent surface configurations adapt in real-time to maintain reliable communication links for critical patient monitoring equipment while directing radiation away from sensitive areas, demonstrating the potential of AI-driven RIS technology to address domain-specific constraints beyond conventional throughput optimization.

### 4.2 Challenges in AI-Based Antenna and RIS Optimization

Despite the remarkable progress in AI-based antenna and RIS optimization, numerous challenges remain that limit practical deployment and motivate continued research. Channel estimation accuracy fundamentally constrains the achievable performance of any optimization approach, as both antenna beamforming and RIS phase configuration depend on accurate knowledge of the wireless channel (Zheng & Zhang, 2022). In RIS-assisted systems, the passive nature of reflecting elements prevents direct channel measurement at the RIS, requiring indirect estimation approaches that introduce additional errors. ML-based channel estimation methods partially address this limitation but require sufficient training data that accurately represents the deployment environment.

Computational complexity represents a persistent challenge for real-time AI-based optimization, particularly as system dimensions increase with larger antenna arrays and RIS surfaces. While trained neural networks provide fast inference, the training phase requires substantial computational resources and time, and models may require frequent retraining as environments change (Liu et al., 2021). Edge computing architectures partially mitigate this challenge by providing local computational resources for AI inference, but the limited processing capability of edge devices constrains model complexity and update frequency.

Training data requirements pose practical difficulties for deploying AI-based optimization in new environments. Supervised learning approaches require labeled datasets of channel realizations and corresponding optimal configurations, which are expensive to obtain in real deployments (Elbir et al., 2022). Transfer learning and domain adaptation techniques reduce data requirements but may not fully compensate for significant differences between source and target environments. Synthetic data generation using ray-tracing simulations provides an alternative, but the accuracy of simulated data depends on the fidelity of environmental models.

Hardware limitations of practical RIS implementations constrain the optimization space and introduce non-ideal behaviors that must be accounted for in AI models. Phase quantization limits the achievable phase shifts to discrete values, amplitude-phase coupling introduces unwanted variations in reflection magnitude, and element mutual coupling creates dependencies between adjacent elements (Abeywickrama et al., 2020). AI models must be trained with these hardware impairments to generate configurations that perform well on practical hardware rather than idealized models.

Table 4 summarizes the key challenges in AI-based antenna and RIS optimization along with current mitigation approaches and their effectiveness.

**[Table 4: Key Challenges and Mitigation Approaches in AI-Based Antenna and RIS Optimization]**

| Challenge | Impact on Performance | Current Mitigation Approaches | Effectiveness | Open Research Gaps |
|---|---|---|---|---|
| Channel Estimation Errors | 15–40% throughput degradation | Robust optimization, imperfect CSI training, Bayesian methods | Moderate (60–75% gap recovery) | Ultra-fast estimation for mobile scenarios |
| Computational Complexity | Real-time constraints violated | Model compression, edge computing, pruning | Good (10× speedup with <5% loss) | Sub-millisecond inference for THz systems |
| Training Data Scarcity | Suboptimal generalization | Transfer learning, data augmentation, simulation | Moderate (70–85% of full-data performance) | Zero-shot generalization to new environments |
| Hardware Impairments | 5–20% performance loss | Hardware-aware training, calibration, compensation | Good (80–90% of ideal performance) | Joint hardware-algorithm co-design |
| Energy Consumption | Sustainability concerns | Green AI, efficient architectures, sleep modes | Limited (30–50% reduction) | Near-zero energy RIS with AI optimization |
| Model Generalization | Performance collapse in new scenarios | Meta-learning, continual learning, ensemble methods | Moderate (75–85% cross-domain performance) | Lifelong learning for evolving networks |

Energy consumption of AI-based optimization systems raises sustainability concerns, particularly for always-on RIS configurations that require continuous optimization. The computational energy required for AI inference and the control energy for RIS phase adjustment must be justified by the communication performance improvements achieved (Huang et al., 2019). Green AI approaches that minimize computational footprint while maintaining optimization quality are essential for sustainable deployment. As summarized in Table 4, while significant progress has been made in addressing individual challenges, the simultaneous resolution of all constraints remains an open research problem requiring holistic approaches.

Security vulnerabilities in AI-based wireless optimization systems represent an emerging concern. Adversarial attacks can manipulate channel measurements or training data to cause suboptimal or harmful RIS configurations (Kim & Poor, 2021). Poisoning attacks during the training phase can embed backdoors that activate under specific conditions, compromising system integrity. Robust AI architectures that detect and resist adversarial manipulation are essential for trustworthy deployment in security-sensitive applications.

### 4.3 Future Research Directions and Intelligent RIS Technologies

The future development of AI-based antenna and RIS optimization is shaped by advances in both AI methodology and hardware technology, pointing toward increasingly intelligent, autonomous, and efficient wireless systems. Federated learning offers a privacy-preserving approach to training optimization models across distributed network nodes, enabling collaborative learning without sharing raw channel data (Yang et al., 2020). Multiple base stations and RIS controllers contribute to a shared model while keeping local data private, aggregating learning experiences across diverse environments to improve generalization. This approach is particularly valuable for operators deploying RIS across heterogeneous environments, as the federated model benefits from the collective experience of all installations.

Explainable AI (XAI) techniques address the interpretability challenge of deep learning-based optimization systems, providing insights into why specific antenna configurations or RIS phase shifts are selected (Barredo Arrieta et al., 2020). Understanding the reasoning behind AI decisions enables verification of physical consistency, identification of failure modes, and progressive refinement of optimization strategies. Attention visualization, feature importance analysis, and rule extraction methods reveal the factors driving optimization decisions, building trust among system operators and facilitating regulatory compliance.

Digital twin technology creates virtual replicas of physical wireless environments, enabling AI models to be trained, tested, and refined in simulation before deployment (Kuruvatti et al., 2022). High-fidelity digital twins incorporate detailed environmental models, propagation characteristics, and hardware specifications, providing realistic training environments that reduce the sim-to-real gap. AI-optimized RIS configurations developed in digital twins transfer more effectively to physical deployments when the twin accurately captures relevant environmental characteristics.

Generative AI approaches, including diffusion models and large language models adapted for scientific applications, offer new paradigms for antenna and RIS design (Wang et al., 2023). Generative models learn the distribution of high-performing designs and sample novel configurations that exhibit desired characteristics, potentially discovering structures that lie outside conventional design paradigms. Large language models trained on electromagnetic literature and simulation data may enable natural language specification of antenna requirements, automatically translating high-level performance goals into optimized designs.

Autonomous RIS control systems leverage hierarchical AI architectures that operate at multiple time scales, combining fast reactive optimization with slower strategic planning (Dai et al., 2022). Low-level controllers handle rapid phase adjustments in response to channel fluctuations, while high-level planners manage resource allocation, user scheduling, and RIS deployment strategies over longer horizons. This hierarchical approach mirrors the structure of modern communication protocol stacks, enabling seamless integration of AI optimization at all appropriate abstraction levels.

Intelligent metasurfaces represent the next evolution beyond current RIS technology, incorporating sensing, computing, and communication capabilities directly into the surface elements (Di Renzo et al., 2022). These active intelligent surfaces can autonomously sense their electromagnetic environment, compute optimal configurations locally, and coordinate with network infrastructure, reducing the dependence on external computing and control signaling infrastructure. AI algorithms embedded in metasurface controllers enable truly autonomous operation, with the surface adapting its behavior without external intervention.

The convergence toward AI-native 6G and 7G communication architectures envisions networks designed from inception around AI capabilities, where antenna systems, RIS elements, and network functions are jointly conceived as components of an intelligent system (Letaief et al., 2022). In these architectures, AI is not an add-on optimization tool but a fundamental design principle that shapes network topology, protocol design, resource management, and physical layer operation. The tight integration of AI with antenna and RIS hardware enables performance levels that approach theoretical bounds while maintaining practical implementability and deployment feasibility.

The development of standardized benchmarks and evaluation frameworks for AI-based antenna and RIS optimization represents a critical need for the research community. Current studies employ diverse simulation environments, channel models, and performance metrics, making direct comparison between approaches difficult. Establishing common evaluation protocols, reference datasets, and performance baselines would accelerate progress by enabling objective assessment of algorithmic innovations and facilitating reproducible research across institutions and research groups worldwide.

---

## Conclusion

This chapter has presented a comprehensive overview of machine learning and artificial intelligence techniques for the optimization of smart antenna systems and reconfigurable intelligent surfaces, addressing the full spectrum from fundamental concepts to cutting-edge research directions. The integration of AI methodologies into antenna and RIS design represents a transformative paradigm that enables capabilities beyond the reach of conventional optimization approaches, including real-time adaptation to dynamic environments, efficient navigation of vast configuration spaces, and discovery of novel designs that transcend human intuition.

The progression from data-driven antenna modeling through adaptive beamforming optimization to joint antenna-RIS-resource management illustrates the expanding scope of AI applications in wireless systems. Each layer of optimization adds complexity but also unlocks additional performance gains, motivating the development of increasingly sophisticated AI frameworks. Deep reinforcement learning emerges as a particularly powerful tool for dynamic RIS control, enabling autonomous adaptation without explicit environmental models, while supervised learning provides efficient mapping from channel observations to optimal configurations for scenarios amenable to offline training.

The challenges identified—including channel estimation errors, computational complexity, training data requirements, hardware limitations, and security vulnerabilities—define the current frontiers of the field and guide future research priorities. Addressing these challenges requires not only advances in AI algorithms but also innovations in hardware design, system architecture, and deployment methodology. The future directions discussed, encompassing federated learning, explainable AI, digital twins, generative models, and intelligent metasurfaces, point toward a future where AI and electromagnetic engineering are inseparably intertwined, jointly delivering the intelligent wireless environments envisioned for 6G and beyond.

---

## References

Abeywickrama, S., Zhang, R., Wu, Q., & Yuen, C. (2020). Intelligent reflecting surface: Practical phase shift model and beamforming optimization. *IEEE Transactions on Communications*, 68(9), 5849–5863.

Akyildiz, I. F., Kak, A., & Nie, S. (2022). 6G and beyond: The future of wireless communications systems. *IEEE Access*, 8, 133995–134030.

Alexandropoulos, G. C., Stylianopoulos, K., Huang, C., Yuen, C., Bennis, M., & Debbah, M. (2020). Pervasive machine learning for smart radio environments enabled by reconfigurable intelligent surfaces. *Proceedings of the IEEE*, 110(9), 1494–1525.

Barredo Arrieta, A., Díaz-Rodríguez, N., Del Ser, J., Bennetot, A., Tabik, S., Barbado, A., ... & Herrera, F. (2020). Explainable artificial intelligence (XAI): Concepts, taxonomies, opportunities and challenges toward responsible AI. *Information Fusion*, 58, 82–115.

Björnson, E., Hoydis, J., & Sanguinetti, L. (2019). Massive MIMO networks: Spectral, energy, and hardware efficiency. *Foundations and Trends in Signal Processing*, 11(3-4), 154–655.

Chen, M., Challita, U., Saad, W., Yin, C., & Debbah, M. (2020). Artificial neural networks-based machine learning for wireless networks: A tutorial. *IEEE Communications Surveys & Tutorials*, 21(4), 3039–3071.

Chepuri, S. P., Saha, S., Mishra, D., & Alexandropoulos, G. C. (2023). Integrated sensing and communication with reconfigurable intelligent surfaces: Opportunities, applications, and future directions. *IEEE Wireless Communications*, 30(1), 84–91.

Dai, L., Wang, B., Wang, M., Yang, X., Tan, J., Bi, S., ... & Di Renzo, M. (2022). Reconfigurable intelligent surface-based wireless communications: Antenna design, prototyping, and experimental results. *IEEE Access*, 8, 45913–45923.

Di Renzo, M., Debbah, M., Phan-Huy, D. T., Zappone, A., Alouini, M. S., Yuen, C., ... & Tretyakov, S. A. (2020). Smart radio environments empowered by reconfigurable AI meta-surfaces: An idea whose time has come. *EURASIP Journal on Wireless Communications and Networking*, 2020(1), 1–20.

Di Renzo, M., Ntontin, K., Song, J., Danufane, F. H., Qian, X., Lazarakis, F., ... & Phan-Huy, D. T. (2022). Reconfigurable intelligent surfaces vs. relaying: Differences, similarities, and performance comparison. *IEEE Open Journal of the Communications Society*, 1, 798–807.

Elbir, A. M., Chatzinotas, S., Song, K., & Mishra, K. V. (2022). Federated learning for channel estimation in conventional and IRS-assisted massive MIMO. *IEEE Transactions on Wireless Communications*, 21(6), 4431–4444.

Feng, K., Wang, Q., Li, X., & Wen, C. K. (2020). Deep reinforcement learning based intelligent reflecting surface optimization for MISO communication systems. *IEEE Wireless Communications Letters*, 9(5), 745–749.

Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep learning*. MIT Press.

Guo, H., Liang, Y. C., Chen, J., & Larsson, E. G. (2020). Weighted sum-rate maximization for reconfigurable intelligent surface aided wireless networks. *IEEE Transactions on Wireless Communications*, 19(5), 3064–3076.

Huang, C., Zappone, A., Alexandropoulos, G. C., Debbah, M., & Yuen, C. (2019). Reconfigurable intelligent surfaces for energy efficiency in wireless communication. *IEEE Transactions on Wireless Communications*, 18(8), 4157–4170.

Huang, C., Mo, R., & Yuen, C. (2020). Reconfigurable intelligent surface assisted multi-user MISO systems exploiting deep reinforcement learning. *IEEE Journal on Selected Areas in Communications*, 38(8), 1839–1850.

Kim, J., & Poor, H. V. (2021). Physical layer security for RIS-assisted communications: Threats, countermeasures, and future directions. *IEEE Wireless Communications*, 28(6), 86–93.

Kim, S., Shim, B., & Lee, J. (2021). Deep learning-based joint optimization of beamforming and RIS phase shifts. *IEEE Transactions on Communications*, 69(11), 7450–7463.

Koziel, S., & Bandler, J. W. (2022). Machine learning for accelerated antenna design and optimization. *IEEE Antennas and Propagation Magazine*, 64(4), 60–72.

Kuruvatti, N. P., Habibi, M. A., Partani, S., Han, B., Fellan, A., & Schotten, H. D. (2022). Empowering 6G communication systems with digital twin technology. *IEEE Access*, 10, 112158–112170.

Letaief, K. B., Shi, Y., Lu, J., & Lu, J. (2022). Edge artificial intelligence for 6G: Vision, enabling technologies, and applications. *IEEE Journal on Selected Areas in Communications*, 40(1), 5–36.

Li, S., Duo, B., Yuan, X., Liang, Y. C., & Di Renzo, M. (2021). Reconfigurable intelligent surface assisted UAV communication: Joint trajectory design and passive beamforming. *IEEE Wireless Communications Letters*, 9(5), 716–720.

Liu, F., Cui, Y., Masouros, C., Xu, J., Han, T. X., Eldar, Y. C., & Buzzi, S. (2022). Integrated sensing and communications: Toward dual-functional wireless networks for 6G and beyond. *IEEE Journal on Selected Areas in Communications*, 40(6), 1728–1767.

Liu, Y., Liu, X., Mu, X., Hou, T., Xu, J., Di Renzo, M., & Al-Dhahir, N. (2021). Reconfigurable intelligent surfaces: Principles and opportunities. *IEEE Communications Surveys & Tutorials*, 23(3), 1546–1577.

Mu, X., Liu, Y., Xu, L., Schober, R., & Poor, H. V. (2022). Simultaneously transmitting and reflecting (STAR) RIS aided wireless communications. *IEEE Transactions on Wireless Communications*, 21(5), 3083–3098.

Nguyen, K. K., Duong, T. Q., Vien, N. A., Le-Khac, N. A., & Nguyen, M. N. (2022). Real-time optimized clustering and caching for 6G intelligent reflecting surface-assisted communications. *IEEE Transactions on Wireless Communications*, 21(7), 5089–5103.

Pan, C., Ren, H., Wang, K., Xu, W., Elkashlan, M., Nallanathan, A., & Hanzo, L. (2021). Multicell MIMO communications relying on intelligent reflecting surfaces. *IEEE Transactions on Wireless Communications*, 19(8), 5218–5233.

Rappaport, T. S., Xing, Y., Kanhere, O., Ju, S., Madanayake, A., Mandal, S., ... & Trichopoulos, G. C. (2019). Wireless communications and applications above 100 GHz: Opportunities and challenges for 6G and beyond. *IEEE Access*, 7, 78729–78757.

Sarieddeen, H., Saeed, N., Al-Naffouri, T. Y., & Alouini, M. S. (2021). Next generation terahertz communications: A rendezvous of sensing, imaging, and localization. *IEEE Communications Magazine*, 58(5), 69–75.

Sharma, P., Tiwari, R. N., Singh, P., Kumar, P., & Kanaujia, B. K. (2022). MIMO antennas: Design approaches, techniques, and applications. *Sensors*, 22(20), 7813.

Sutton, R. S., & Barto, A. G. (2018). *Reinforcement learning: An introduction* (2nd ed.). MIT Press.

Taha, A., Alrabeiah, M., & Alkhateeb, A. (2021). Enabling large intelligent surfaces with compressive sensing and deep learning. *IEEE Access*, 9, 44304–44321.

Tariq, F., Khandaker, M. R., Wong, K. K., Imran, M. A., Bennis, M., & Debbah, M. (2020). A speculative study on 6G. *IEEE Wireless Communications*, 27(4), 118–125.

Wang, S., Li, T., Zhao, J., Liu, Y., & Li, G. Y. (2023). Generative AI for wireless communications: Technologies, applications, and opportunities. *IEEE Network*, 37(5), 116–123.

Wu, Q., & Zhang, R. (2020). Towards smart and reconfigurable environment: Intelligent reflecting surface aided wireless network. *IEEE Communications Magazine*, 58(1), 106–112.

Wu, Y., Lin, Y., Li, M., & Li, E. P. (2021). Deep learning-based antenna design and optimization: A review. *IEEE Antennas and Propagation Magazine*, 63(5), 72–85.

Xia, W., Zheng, G., Zhu, Y., Zhang, J., Wang, J., & Petropulu, A. P. (2020). A deep learning framework for optimization of MISO downlink beamforming. *IEEE Transactions on Communications*, 68(3), 1866–1880.

Xu, J., Kang, Y., & Tao, X. (2022). Multi-agent deep reinforcement learning for RIS-assisted multi-user MISO systems. *IEEE Transactions on Cognitive Communications and Networking*, 8(4), 1872–1885.

Yang, H., Xiong, Z., Zhao, J., Niyato, D., Xiao, L., & Wu, Q. (2021). Deep reinforcement learning-based intelligent reflecting surface for secure wireless communications. *IEEE Transactions on Wireless Communications*, 20(1), 375–388.

Yang, Q., Liu, Y., Chen, T., & Tong, Y. (2020). Federated machine learning: Concept and applications. *ACM Transactions on Intelligent Systems and Technology*, 10(2), 1–19.

Yao, H. M., Sha, W. E. I., & Jiang, L. (2022). Machine learning for antenna design: Methods and applications. *Applied Sciences*, 12(4), 2076.

Zhang, S., & Dai, L. (2021). Joint beamforming optimization for intelligent reflecting surface-aided communications. *IEEE Transactions on Communications*, 69(3), 2020–2033.

Zheng, B., & Zhang, R. (2022). Intelligent reflecting surface-enhanced OFDM: Channel estimation and reflection optimization. *IEEE Wireless Communications Letters*, 9(4), 518–522.
