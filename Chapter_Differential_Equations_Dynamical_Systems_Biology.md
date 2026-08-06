# Differential Equations and Dynamical Systems in Biology

**Book: Biomathematics: A New Horizon of Science and Engineering**

---

## Abstract

One of the most fruitful areas of collaboration between mathematics and the life sciences is that between differential equations and dynamical systems theory and biology. This chapter gives a detailed account of the recent developments in mathematical methods developed under the foundation of ordinary and partial differential equations, stability and bifurcation analysis, and computational simulation, that have revolutionized the study of biological phenomena. Basic theory and current applications fundamental to understanding modern biomathematics are explored including population dynamics, epidemiological modeling, pattern formation and cell signaling. The chapter also ends with a discussion on new computational tools, multiscale modeling problems, and prospects for the future of mathematical biology in a new era of data intensive science and personalized medicine.

---

## Section 1: Foundations of Mathematical Biology

### 1.1 Introduction to Biomathematics and Its Scope

#### Role of Mathematics in Understanding Biological Systems

Nature, as Biology is, is complex and complicated [1]! Despite this vast range of scale, all living systems exhibit an ability to function continually at multiple scales that spans from molecular interactions over nanoseconds to evolutionary changes over millions of years [8]. These phenomena can be precisely described, analyzed and predicted using Mathematical terms [2, 3] as a language that is universal in its nature. Mathematical modeling of biological systems can be used to state the hypotheses in a mathematical way, to discover principles which are dominant, and to predict quantitatively in a way that will inform experiments [9]. Mathematics and biology are not only contentedly applied to one another, but they enrich each other too [10]. Mathematical ideas have given rise to new fields of biology, and biological problems have theirs provided new insights into mathematics. New fields of biological science have emerged as new fields of mathematics and new insights into the biology have emerged as a result of mathematics. Differential equations feature in particular as the key mathematical tools for describing the continuous temporal and spatial dynamics of biological quantities [11]. In all sorts of phenomena, ranging from growth of a bacterial population, the spread of a contagious disease, to propagation of electrical signals along nerve fibers, there is a formal connection between mechanism and observation presented by a differential equation [12].


#### Historical Development and Interdisciplinary Significance

The earliest roots of mathematical biology can be traced back to the eighteenth century, when Daniel Bernoulli used mathematics to investigate the study of inoculation strategies for smallpox disease in 1760 [13]. The field started to develop significantly however in the early 1900's with the work of two mathematicians, Alfred Lotka and Vito Volterra, who developed independently population models of predator prey interactions [14, 15]. They worked out their network of coupled ODEs, and found that complex oscillatory phenomena, such as those of real world ecosystems, could be produced by simple mathematical rules [16]. Alan Turing's paper on 'morphogenesis' from 1952 [17] and Alan Hodgkin and Andrew Huxley's mathematical model of nerve impulse propagation [18], both of whom won the Nobel Prize, were other important contributions in the mid-20th century. These results proved that mathematical modelling was not simply a description game, but a truly predictive modelling technique that could explain mechanisms, which were not directly accessible by experimental means [19]. Biomathematics is now a well-established interdisciplinary field, which covers mathematical ecology, epidemiology, systems biology, bioinformatics and computational medicine [5, 20]. Mathematical approaches are not only valuable but also necessary with regard to the exponential growth in biological data, the rise of an increased computational power, and the questions of growing complexity which global biology is meeting nowadays [21].

#### Examples of Biological Phenomena Modeled Mathematically

The variety of phenomena of biological origin that can be described mathematically is remarkable [1, 2]. Logistic growth equations and Lotka-Volterra systems are used in population ecology to better understand the interactions between species and predict the dynamics of the ecosystems [22, 23]. Compartmental models have been used for forecasting disease outbreaks and assessment of intervention strategies [24, 25]. In cell biology, Michaelis-Menten model and coupled systems of ODEs are used to model metabolic and signalling networks [26, 27]. Reaction-diffusion equations are used by developmental biologists to find the mechanisms by which cells in an embryo first differentiate to form organized tissues and organs [17, 28]. To study brain functions from single neuron to large-scale dynamics of neural networks neuroscientists rely on conductance-based models and neural field equations [18, 29]. All these applications are built mostly on differential equations and the theory of dynamical systems [4]. The theory of differential equations plays a vital role in solving these applications.


### 1.2 Basics of Differential Equations in Biology

#### Ordinary and Partial Differential Equations (ODEs & PDEs)

One of the mathematical pillars of biological modelling of dynamics is the set of equations known as differential equations [11, 30]. The differential equation of an ordinary variable y, which changes with respect of one independent variable, x, usually time [3]. In biology, the ODEs model well-mixed systems in which the spatial dimension is not relevant, for example, the concentrations in a homogenously mixed bioreactor when modeling the growth of a substrate, or the number of people who are infected in a population. A general first order ordinary differential equation (ODE) is given by:

$$\frac{dx}{dt} = f(x, t) \tag{1}$$

where $x$ is the state variable (population size, chemical concentration, membrane voltage) and the biological mechanism governing the change is encoded by the function $f(x, t)$ [4]. A combination of multiple interacting components requires multiple components to be tracked simultaneously, leading to systems of coupled ODEs of the form:

$$\frac{dx_i}{dt} = f_i(x_1, x_2, \ldots, x_n, t), \quad i = 1, 2, \ldots, n \tag{2}$$

These occur naturally in metabolic networks or multi-species ecological communities [32]. There are situations in which the spatial variation is relevant, for which PDEs extend the framework [2, 33]. A PDE has partial derivatives with respect to a spatial coordinate(s) and time. When considering diffusive transport, as well as local reaction kinetics, the general reaction-diffusion equation is:

$$\frac{\partial u}{\partial t} = D \nabla^2 u + R(u) \tag{3}$$

where the diffusion coefficient $D$ indicates the diffusive transport properties and $R(u)$ represents local reaction kinetics [34]. Some physical phenomena, like the formation of a morphogen gradient during embryonic development, the propagation of epidemics through space, or the propagation of calcium waves in cardiac tissue [35, 36] require the modelling by PDEs.


#### Initial and Boundary Conditions in Biological Contexts

Without the specification of suitable auxiliary conditions there will not be a unique solution of a differential equation [11]. Initial conditions for ODEs are those conditions at the initial time ($t = 0$) that indicate the starting condition of the biological system that is being studied [30]. An example of initial conditions is provided by the modelling of epidemics where they represent the number of susceptible, infected and recovered individuals at the beginning of an outbreak [24]. In addition, PDEs must also include boundary conditions which specify the response of the system at the edges of the spatial domain [33]. Biological applications might involve impermeable membranes in cells (no-flux or Neumann conditions), concentrations fixed by sources outside the solution (Dirichlet conditions) and periodic conditions for ring shaped or toroidal geometries [34]. Several different possible boundary conditions drastically affect the models generated by the system and are governed by its biological validity [2].

#### Analytical vs Numerical Solution Approaches

Close mathematical solutions give a total description of the dependence of the parameter and the system behavior [3]. However, they can only be used for relatively simple equations. The general solution of the exponential growth equation is:

$$N(t) = N_0 e^{rt} \tag{4}$$

and hence this equation clearly shows dependence on growth rate $r$ and initial condition $N_0$ [22]. Likewise, the logistic equation has a solution in closed form:

$$N(t) = \frac{K N_0}{N_0 + (K - N_0)e^{-rt}} \tag{5}$$

which is formulated with the carrying capacity $K$ and intrinsic growth rate $r$ [37]. However, most of the biologically realistic models are too complicated to be treated analytically [38]. In most cases standard nonlinearities, multiple variable couplings and spatial heterogeneity require numerical solutions. There are various methods available for solving ODEs and PDEs, such as Euler's method, Runge-Kutta schemes, and adaptive step-size algorithms to solve ODEs and finite difference, finite element, and spectral methods for PDEs [39, 40]. The option of using either analytical or numerical method will be determined by the model complexity, the question(s) being asked, and the quantitative precision that is desired [41].


### 1.3 Modeling Biological Systems: Principles and Assumptions

#### Deterministic vs Stochastic Models

Deterministic models – those governed by ordinary or partial differential equations – assume that the state of a system is fully determined by its current state and the equations that govern the system [42]. If random fluctuations average out as in large populations and/or high molecular concentrations, this framework is suitable. Most models of chemical kinetics receive as input the parameters that describe the chemical process and initial conditions including the initial reactants. These kinetic models are intrinsically deterministic and yield reproducible evolutions of the initial conditions for the same input parameters. But there are many systems in which stochasticity is important in the biological world [44]. The contributions from individual molecules in gene expression of a cell are small enough that random deviation (noise) is a major phenomenon, instead of a minor deviation [45]. This intrinsic variability can be modeled using stochastic models, usually in the form of a continuous-time Markov chain controlled by a master equation. The chemical master equation for the probability $P(\mathbf{x}, t)$ of being in state $\mathbf{x}$ at time $t$ is given by:

$$\frac{dP(\mathbf{x}, t)}{dt} = \sum_{j=1}^{M} \left[ a_j(\mathbf{x} - \boldsymbol{\nu}_j) P(\mathbf{x} - \boldsymbol{\nu}_j, t) - a_j(\mathbf{x}) P(\mathbf{x}, t) \right] \tag{6}$$

where $a_j$ are the propensity functions and $\boldsymbol{\nu}_j$ are the stoichiometric change vectors for each of the $M$ reaction channels [46]. An alternative approximation for large molecule numbers is provided by the Langevin equation:

$$dx = f(x)dt + g(x)dW(t) \tag{7}$$

where $dW(t)$ represents a Wiener process capturing the stochastic fluctuations [46]. The Gillespie algorithm is able to simulate chemical reaction networks exactly at a stochastic level, and could be used to show phenomena such as bistable behavior, noise induced switching, variation from cell to cell, etc., which deterministic models are unable to capture [47].


#### Scaling, Simplification, and Parameter Estimation

Generally biological systems have many interacting components at many scales [8]. Smarter mathematical modeling involves modeling without loss of information (dimensional analysis), scaling the variables without losing information (non-dimensionalization) and recognizing slow and fast timescales [48]. To solve the many dimensions of enzyme kinetic models, quasi-steady state approximations are used and singular perturbation theory is applied to isolate the fast transients and the slow manifold dynamics [49]. One of the most significant challenges in biological modelling is the parameter estimation [50]. A number of model parameters are seldom measured directly and are inferred from indirect observations [51]. Systematic parameter identification is possible through techniques such as least-squares fitting or maximum-likelihood estimation or by means of Bayesian inference and Markov chain Monte Carlo methods [52, 53]. The problem of identifiability deals with the question of whether or not the available data allows for the determination of the possible values of the parameters and is a fundamental theoretical issue that can guide experimental design [54]. Mathematical biology problems require the development and use of models based on mathematical equations.

#### Model Validation Using Experimental Data

No matter how elegant and beautiful the mathematical model, science value can be applied only as long as the model is realistic and reflects the biological reality [9]. A systematic comparison of model prediction and independent experimental data which were not used in model parameter estimation constitutes model validation [55]. During this process, the model is tested for its ability to include the necessary biological mechanisms and for its ability to properly predict results when applied to a situation beyond the scope or range of the previously mentioned use cases. Examples among validation strategies are comparison of predicted steady-state results with measured concentrations of equilibrium results, testing whether the model output of the dynamic trajectory is in good agreement with the time series data, and testing whether the model accurately reproduces the results of perturbation experiments [50, 57]. The failure of the models during validation is information itself and the omission of mechanisms, or incorrect assumptions, is responsible for this failure, and so refinement of the model is instructed by it [55]. Mathematical biology follows an iterative process of model-building, prediction, experimental checking and adjustment, known as the scientific method [1, 9].

**Table 1: Summary of Key Concepts in Foundations of Mathematical Biology**

| Topic | Key Equation/Concept | Biological Application | Mathematical Framework |
|-------|---------------------|----------------------|----------------------|
| Exponential Growth | dN/dt = rN | Microbial cultures, early colonization | First-order linear ODE |
| Logistic Growth | dN/dt = rN(1 - N/K) | Density-regulated populations | Nonlinear ODE with carrying capacity |
| Reaction-Diffusion | ∂u/∂t = D∇²u + R(u) | Morphogen gradients, spatial spread | Partial differential equation |
| Deterministic Modeling | dx/dt = f(x, t) | Large populations, well-mixed systems | Ordinary differential equations |
| Stochastic Modeling | Master equation / Langevin | Gene expression, small molecule counts | Markov chains, SDEs |
| Parameter Estimation | Least-squares, MLE, Bayesian | Inferring rate constants from data | Statistical inference |
| Model Validation | Prediction vs. experiment | Testing mechanistic hypotheses | Iterative refinement cycle |
| Quasi-Steady-State | Fast variable elimination | Enzyme kinetics simplification | Singular perturbation theory |


---

## Section 2: Dynamical Systems Theory in Biological Modeling

### 2.1 Introduction to Dynamical Systems

#### Definition of Dynamical Systems in Biology

Dynamical systems are mathematical models that describe the evolution of a system over time following certain rules [4, 58]. Formally, a continuous time dynamical system is defined by a system of ODEs:

$$\frac{d\mathbf{x}}{dt} = \mathbf{F}(\mathbf{x}) \tag{8}$$

where $\mathbf{x} \in \mathbb{R}^n$ is a vector of state variables characterizing the state of the system, and $\mathbf{F}: \mathbb{R}^n \rightarrow \mathbb{R}^n$ is the vector field determining its evolution [59]. In a biological sense, the theory of dynamical systems gives the concepts and tools needed for understanding the way the living system changes, maintains homeostasis, reacts to disturbances and switches between qualitatively different behaviors [60]. For a dynamical systems theory one of its most important assets is the ability to describe the qualitative aspects of such systems without solving the underlying equations explicitly [58]. Questions like whether a system might reach a steady state, be periodic, or produce chaotic behavior can frequently be answered by doing a geometric and topological analysis of the structure of the phase space [4]. This qualitative method is of special relevance in biology where the values of the parameters are often poorly known but suitable qualitative features of the behavior can be observed experimentally [61].

#### State Variables, Phase Space, and Trajectories

State variables characterize a state of a biological system at a given time—these include population densities, chemical concentrations, membrane potentials, or levels of gene expression [59]. All the states together comprise the entire collection of states, the so-called phase space (also state space): each point in the phase space represents a specific state of the system. The phase space is $n$-dimensional for a system with $n$ state variables [58]. As a system passes through time, it takes a path through phase space known as a trajectory or orbit [60]. The set of all possible trajectories is called the phase portrait and gives the complete qualitative description of the behaviour of a system [4]. The structure of the dynamics, or attractors towards which the trajectories converge, repellers from which they diverge, and separatrices that separate phase space into basins, is revealed in phase portraits [62]. Biologically speaking, these attractors can represent different cell fates, different stable states of an ecosystem or endemic/disease-free states for diseases [63, 64].


#### Continuous vs Discrete Dynamical Systems

For biological processes that change smoothly over time, represented by what are called continuous dynamical systems, these are described by equations that are made up of derivatives of functions. Many physiological and biochemical processes are well described by the continuous models: Neuronal membrane behavior, enzyme catalysis, hormone secretion, etc. [5]. The mathematical theory of continuous systems is based on topology, differential geometry and functional analysis that describe the behavior [58]. When biological events arrive at fixed, but separate, time steps, then these are usually modelled as a discrete dynamical system, given by a difference equation or an iterated map of the form:

$$x_{n+1} = G(x_n) \tag{9}$$

Naturally occurring systems such as organisms with non-overlapping generations, annual census data in ecology, and cell division cycles are modelled in terms of discrete time [22]. Even in a one-dimensional map a system can display rich dynamical behavior, such as period-doubling cascades and chaos, as Robert May's seminal paper on the discrete logistic equation illustrated [66]:

$$x_{n+1} = r x_n (1 - x_n) \tag{10}$$

where $r$ is the growth parameter that controls the qualitative dynamics of the system [66]. A continuous vs. discrete formulation choice is based on the time resolution of interest and the type of biological processes to be modeled [3].

### 2.2 Stability Analysis and Equilibrium Points

#### Fixed Points and Steady States

An equilibrium point (also called a fixed point or steady state) of a dynamical system $d\mathbf{x}/dt = \mathbf{F}(\mathbf{x})$ is a point $\mathbf{x}^*$ where:

$$\mathbf{F}(\mathbf{x}^*) = \mathbf{0} \tag{11}$$

At those locations all rates of change are equal to zero, and the system may remain stationary if it is at exactly that location [4, 58]. Steady states occur in biological systems, such as the resting membrane potential of a neuron, the carrying capacity of a population, the disease-free equilibrium of an epidemic model or the basal expression level of a gene, etc. [60, 67]. The algebraic system $\mathbf{F}(\mathbf{x}) = \mathbf{0}$ may have one or multiple solutions depending on the parameters of the system [4]. The occurrence of multiple equilibria is also of biological interest because it also means the potential for alternative stable states, seen in the clear versus turbid water balances of lakes, differentiation and nondifferentiation of cells in gene regulatory networks, or disease-free status versus endemic steady states in the dynamics of infectious diseases [63, 68]. The number and type of equilibria may change with varying parameters, leading to bifurcation phenomena [69].


#### Linearization and Jacobian Matrices

The linearization consists of approximating the nonlinear vector field $\mathbf{F}(\mathbf{x})$ by its first order Taylor expansion about $\mathbf{x}^*$ [58] that gives an indication of the behavior of trajectories near equilibrium points. This results in the linearized equation:

$$\frac{d\mathbf{y}}{dt} = \mathbf{J} \mathbf{y} \tag{12}$$

with $\mathbf{y} = \mathbf{x} - \mathbf{x}^*$ being the perturbation from equilibrium, and $\mathbf{J}$ being the Jacobian matrix evaluated at $\mathbf{x}^*$ [4]. The elements of the Jacobian are the partial derivatives:

$$J_{ij} = \frac{\partial F_i}{\partial x_j} \bigg|_{\mathbf{x}=\mathbf{x}^*} \tag{13}$$

evaluated at the equilibrium point [59]. The Jacobian matrix contains the dynamics of the sensitivity of the rate of change of the state variables to the changes in a state variable [60]. In ecological models, the elements of the Jacobian illustrate the strengths of interaction between the species [70]. They measure the sensitivity of reaction rates in biochemical networks to changes in the concentrations of its metabolites [27]. The linearized system is generally used to describe the dynamics near an equilibrium state and can be used to predict whether these dynamics are growing or decaying over time [4, 71].

#### Stability Criteria and Biological Interpretation

The eigenvalues of the Jacobian matrix are used to test an equilibrium point for stability [58, 59]. The characteristic equation for determining eigenvalues is:

$$\det(\mathbf{J} - \lambda \mathbf{I}) = 0 \tag{14}$$

When the real parts of all the eigenvalues are negative ($\text{Re}(\lambda_i) < 0$ for all $i$), the equilibrium is asymptotically stable; that is, exponential decay of small perturbations allows the system to return to the steady state [4]. If there is any eigenvalue with a positive real component the equilibrium is unstable and the perturbations grow [60]. For the case of complex eigenvalues with negative real values, damped oscillations occur toward the equilibrium, and for the case of purely imaginary eigenvalues, the boundary between stability and instability is established [71]. From a biological perspective, stability analysis shows the stability of the homeostatic state [67]. For a population model, a stable equilibrium would mean that after the environmental perturbations the population would return to its carrying capacity [22]. An unstable disease-free equilibrium in an epidemiological model indicates that a pathogen may be able to invade the population as an endemic infection [24, 25]. In epidemiology, the basic reproduction number $R_0$ is directly linked to the stability of the disease-free equilibrium: if $R_0 > 1$, the disease-free state becomes unstable [72]. However, the Routh-Hurwitz criteria [58] give algebraic conditions on the roots of the characteristic polynomial that ensure that the system is stable, without actually evaluating the roots. For two-dimensional systems, the stability conditions require:

$$\text{tr}(\mathbf{J}) < 0 \quad \text{and} \quad \det(\mathbf{J}) > 0 \tag{15}$$

That is, the trace (sum of eigenvalues) must be negative and the determinant (product of eigenvalues) must be positive [59].


### 2.3 Nonlinear Dynamics and Bifurcation Analysis

#### Nonlinearity in Biological Systems

Most natural systems are nonlinear [4, 60]. These appear as nonlinear terms in the governing equations, such as saturating enzyme kinetics (Michaelis-Menten) [26, 27], density-dependent growth and cooperative binding (Hill functions). The rich dynamical behaviour of living systems – multistability, oscillations, excitability, chaos – which are impossible for purely linear systems [58, 73] are produced by these nonlinearities. The implications of the nonlinearity for mathematics are significant [69]. Superposition is violated: response is NOT the sum of the individual responses [4]. Qualitative changes in the behaviour can result from small changes in the parameters [71]. There are multiple attractors and the behaviour of the system is history dependent [63]. Such features make mathematical modelling difficult but are indeed biological processes. Nonlinear dynamics, such as those mentioned above, all play a role in the creation of cellular memory, developmental switches and critical transition points in ecosystems [64, 68].

#### Limit Cycles, Oscillations, and Chaos

Circadian rhythms, cardiac pacemaker activity, calcium oscillations in signaling cells, population cycles of prey and predator, or oscillations in yeast glycolysis are examples of periodic oscillations that occur in biology everywhere. From a mathematical point of view, sustained oscillations are represented by limit cycles: isolated, closed orbits of phase space to which other orbits tend nearby [4, 58]. The Poincaré-Bendixson theorem proves that for bounded planar systems where convergence to an equilibrium is impossible, a limit cycle must exist, providing a powerful existence result for two-dimensional biological oscillators [59]. Oscillations most commonly emerge via the Hopf bifurcation [69, 76]. A stable equilibrium loses its stability when a parameter passes through a critical value, and a pair of complex conjugate eigenvalues cross the imaginary axis; the condition for Hopf bifurcation at parameter $\mu = \mu_c$ is:

$$\text{Re}(\lambda(\mu_c)) = 0, \quad \frac{d}{d\mu}\text{Re}(\lambda(\mu))\bigg|_{\mu=\mu_c} \neq 0 \tag{16}$$

resulting in the birth of a limit cycle [4]. It is this mechanism which is responsible for the onset of oscillations in neural systems and for the initiation of calcium spiking in stimulated cells [29, 77]. Chaos—deterministic, yet unpredictable dynamics—shows sensitive dependence on initial conditions and has been found in different biological situations [66, 78]. Cardiac arrhythmias, irregular firing patterns of the nervous system and insect populations have been found to be associated with chaotic dynamics [79]. Chaos serves to remind us that apparently random, complex behavior can emerge from simple deterministic rules, and thus undermines naive distinctions between order and randomness in living systems [66, 80].


#### Bifurcation Theory and Transitions in System Behavior

In bifurcation theory, the qualitative behavior of a dynamical system changes with changes in the parameters of the system [69, 76]. A bifurcation takes place at a value of the parameter at which the number, type and/or the stability of equilibria and/or periodic orbits changes [4]. Bifurcations are critical thresholds or transitions that occur in a biological system, where beyond a threshold, system behavior switches. Saddle-node bifurcations occur when two equilibria near one another merge and then disappear, with one being stable and one unstable—a phenomenon that drives critical fluctuations or processes in ecosystems, such as the collapse of a fishery or irreversible eutrophication of a lake [68, 81]. In the case of an epidemiological model, a transcritical bifurcation corresponds to the invasion threshold ($R_0 = 1$) [72]. Systems exhibiting symmetry give rise to pitchfork bifurcations which model spontaneous symmetry-breaking phenomena including cell polarization and pattern formation [69, 76]. Bifurcation is summarized graphically in the form of a bifurcation diagram, a graph in which the equilibrium values of an observable quantity or the oscillation amplitude are plotted against a control parameter [4, 58]. These diagrams reveal hysteresis (history-dependence), bistability (coexisting attractors) and thresholds, providing a roadmap for biologists to grasp the ways in which slow environmental and/or physiological changes can cause rapid behavioural change [63, 81].

**Table 2: Summary of Dynamical Systems Concepts and Their Biological Significance**

| Dynamical Systems Concept | Mathematical Characterization | Biological Example | Significance |
|--------------------------|------------------------------|-------------------|-------------|
| Stable Equilibrium | All eigenvalues Re(λ) < 0 | Population at carrying capacity | Homeostasis, robustness |
| Unstable Equilibrium | Any eigenvalue Re(λ) > 0 | Disease-free state when R₀ > 1 | Pathogen invasion threshold |
| Limit Cycle | Isolated closed orbit in phase space | Circadian rhythms, cardiac pacemaker | Sustained biological oscillations |
| Hopf Bifurcation | Complex eigenvalues cross imaginary axis | Onset of calcium spiking | Emergence of rhythmic behavior |
| Saddle-Node Bifurcation | Two equilibria collide and annihilate | Ecosystem collapse, lake eutrophication | Critical transitions, tipping points |
| Transcritical Bifurcation | Stability exchange between equilibria | Epidemic threshold (R₀ = 1) | Invasion/extinction boundaries |
| Chaos | Sensitive dependence on initial conditions | Cardiac arrhythmias, insect populations | Deterministic unpredictability |
| Bistability | Two coexisting stable attractors | Cell fate decisions, genetic switches | Cellular memory, irreversible transitions |


---

## Section 3: Applications in Biological Systems

### 3.1 Population Dynamics and Ecology Models

#### Exponential and Logistic Growth Models

The most basic model of population growth is the exponential growth law:

$$\frac{dN}{dt} = rN \tag{17}$$

where $N$ is the size (or number) of the population and $r$ is the intrinsic rate of natural increase [22, 37]. The first phase of growth in unlimited ecosystems is represented by this model, and has the analytical solution $N(t) = N_0 e^{rt}$ [3]. Although physiologically unattainable over long time periods (any population cannot grow indefinitely), in the early-colonisation phase of microbial cultures and establishment of an invasive species, exponential growth can be considered a very good approximation [23]. A density dependent feedback mechanism that accounts for the environmental carrying capacity $K$ is introduced by the logistic equation:

$$\frac{dN}{dt} = rN\left(1 - \frac{N}{K}\right) \tag{18}$$

The per-capita growth rate decreases linearly to zero as the population gets close to $K$, characteristic of limiting resources, waste buildup, and/or higher competition [22]. The logistic model has one stable equilibrium solution at $N = K$, and one unstable at $N = 0$; if $N$ starts positive it will ultimately converge to $N = K$ [23]. Although the logistic equation is simple, it can account for the basic qualitative traits of density-regulation in growth common to a wide range of taxa including bacteria and mammals [16]. When integrated into the logistic model, time delays represent maturation periods or resource regeneration times, Allee effects represent reduced growth at low densities associated with mate finding issues or cooperative feeding, and environmental stochasticity introduces random perturbations [82, 83]. Biological delays can give rise to oscillations and chaos in time-delayed logistic equations [66]. They also lead to unstable equilibria known as Allee effects and have significant consequences for conservation biology [83].


#### Predator-Prey Models (Lotka-Volterra Systems)

The classical predator-prey model formulated in terms of the ODEs for prey ($H$) and predators ($P$) is [14, 15]:

$$\frac{dH}{dt} = aH - bHP \tag{19}$$

$$\frac{dP}{dt} = cbHP - dP \tag{20}$$

where $a$ is the prey growth rate, $b$ is the predation rate coefficient, $c$ is the conversion efficiency, and $d$ is the predator death rate. The system has neutrally stable periodic orbits as highlighted by the time series of prey and predator populations oscillating out-of-phase with each other, which has been qualitatively observed for the population size of lynx and hares, and also for plankton and predators [16, 23]. The instability of the classical Lotka-Volterra system (neutral stability is lost under any perturbations), however, has led to the construction of more realistic predator-prey models [70]. The Rosenzweig-MacArthur model incorporates logistic prey growth coupled with a saturating (Type II) functional response:

$$\frac{dH}{dt} = rH\left(1 - \frac{H}{K}\right) - \frac{aHP}{1 + ahH} \tag{21}$$

which yields a stable coexistence equilibrium or a stable limit cycle depending on the parameters [84]. This model predicted the paradox of enrichment where the progressive rise of the carrying capacity of prey can lead to the destabilization of ecological coexistence, resulting in the eventual extinction of both populations owing to large amplitude oscillations, and it triggered decades of theoretical and experimental studies [84, 85].

#### Competition and Coexistence Models

Competition between two species is modeled using coupled logistic equations with interaction terms [22, 23]:

$$\frac{dN_1}{dt} = r_1 N_1 \left(1 - \frac{N_1 + \alpha_{12} N_2}{K_1}\right) \tag{22}$$

$$\frac{dN_2}{dt} = r_2 N_2 \left(1 - \frac{N_2 + \alpha_{21} N_1}{K_2}\right) \tag{23}$$

where $\alpha_{ij}$ represents the per-capita effect of species $j$ on species $i$ relative to intraspecific competition [70]. The results of this analysis lead to the competitive exclusion principle; that is, two species that are competitors may not coexist indefinitely when they compete for the same limiting resource unless they have differentiated niches [86]. For stable coexistence it is necessary that intraspecific competition is greater than interspecific competition on both species ($\alpha_{12} < K_1/K_2$ and $\alpha_{21} < K_2/K_1$) [23]. If these conditions are not met, then one species will be competitively driven to extinction while the other is driven to fixation (depending upon the initial conditions when bistability occurs) [86]. Modern extensions include the idea of spatial heterogeneity, time variation, and several resources, which capture mechanisms of coexistence that are not seen in their simple mean-field counterparts [87]. Classical competition theory cannot fully explain the coexistence of species, which is marked by the storage effect, the relative nonlinearity of competition, and spatial niche partitioning [87, 88].


### 3.2 Epidemiological Modeling

#### SIR, SEIR, and Compartmental Models

The compartmental modeling framework divides a population according to disease status [24, 25] and is a starting point for mathematical epidemiology. Kermack and McKendrick proposed the foundational SIR model in 1927, based on the partitioning of the population into Susceptible ($S$), Infected ($I$), and Recovered ($R$) categories with the system [72]:

$$\frac{dS}{dt} = -\frac{\beta SI}{N}, \quad \frac{dI}{dt} = \frac{\beta SI}{N} - \gamma I, \quad \frac{dR}{dt} = \gamma I \tag{24}$$

where $\beta$ is the transmission rate, $\gamma$ is the recovery rate and $N$ is the total population size. The SIR model describes the basic dynamics of an epidemic outbreak: an initial exponential growth in the number of infected people as a result of having a large number of susceptible people, and then the emergence of a peak followed by a decline when almost the entire population had already been infected [24]. It predicts that an epidemic is "self-limiting" in the sense that not everybody has to be infected for the epidemic to wane, which is understood as being driven by herd immunity [25, 72]. Building on this, the SEIR model accounts for the Exposed ($E$) compartment designating individuals that are infected but not yet infectious (latent period) [89]. The incubation period plays an important role in outbreaks of measles, influenza and COVID-19 disease [90]. Other extensions include SEIRS models (incorporating waning immunity), models which include age structure, models which account for more than one strain of pathogen, and models which integrate spatial heterogeneity (metapopulations or networks) [25, 91].

#### Disease Transmission Dynamics

In mathematical epidemiology the pivotal quantity is the basic reproduction number $R_0$, which represents the number of secondary infections expected to arise from an initial infected person in a fully susceptible population [72, 92]. The $R_0$ value for the SIR model is:

$$R_0 = \frac{\beta}{\gamma} \tag{25}$$

If $R_0 > 1$, then the disease-free state is unstable and an epidemic may happen; if $R_0 < 1$, the disease-free state is stable and the infection will become extinct [24]. The effective reproduction number $R_t$ takes into account the reduction in susceptibles throughout an epidemic: $R_t = R_0 S(t)/N$ [25]. The herd immunity threshold, representing the critical fraction of the population that must be immune to prevent sustained transmission, is given by:

$$p_c = 1 - \frac{1}{R_0} \tag{26}$$

This determines the final epidemic size and the vaccination coverage required for disease elimination [72]. Further parameters of transmission dynamics include the generation time distribution, serial interval, and incubation period, which are essential for modeling the dynamics of an epidemic in real-time for forecasting [89, 92]. The force of infection (number of new cases per person who are potential targets for infection) is affected by the prevalence of infection, patterns of contacts, and probability of transmission per contact [24]. The degree of heterogeneity in contact structure measured by contact matrices by age or occupation, or by geographical location, has a significant effect on the dynamics of epidemics as well as on the success of targeted interventions [91, 93].


#### Impact of Vaccination and Control Strategies

Mathematical models are used to quantitatively assess vaccination strategies and public health interventions [25, 90]. The critical level of vaccination coverage needed for achieving herd immunity can be easily obtained from the stability of the disease-free equilibrium in models which include vaccination, namely $p_c = 1 - 1/R_0$ [72]. For measles ($R_0 \sim 12$–$18$), this means that the vaccine coverage needs to be above 92–95%, which has been validated empirically [24]. Models with imperfect vaccine efficacy, vaccines with waning immunity, and age-dependent vaccination with heterogeneous mixing give more fine-grained advice on vaccination programs [91, 93]. The optimal control approach to epidemic models seeks time-varying intervention parameters such as the level of quarantine and social distancing, and the vaccination rate, consistent with resource limitations, to reduce disease costs [89]. Mathematical modelling has paved the way towards providing insights supporting measures taken during the COVID-19 pandemic, including case management, the allocation of vaccines, planning of hospital resources and when to relax lockdown measures in different parts of the world [90, 92].

### 3.3 Cellular and Physiological Systems Modeling

#### Enzyme Kinetics and Biochemical Reactions

Systems biology and metabolic modelling are based on the mathematical description of enzymatically catalysed reactions [26, 27]. The Michaelis-Menten equation describes the rate of an enzymatic reaction as a saturating function of substrate concentration:

$$v = \frac{V_{\max}[S]}{K_m + [S]} \tag{27}$$

where $v$ is the rate of reaction, $V_{\max}$ is the maximum rate at saturation, $[S]$ is the substrate concentration, and $K_m$ is the Michaelis constant [43]. This equation is obtained by a quasi-steady-state approximation to the extensive set of ODEs for enzyme-substrate binding, catalysis and product release [49]. Extensive kinetic frameworks are needed for more complicated enzymatic behaviour (multi-substrate reactions, allosteric regulation, cooperative binding, and substrate inhibition) [27]. Positive cooperativity and ultrasensitive switching behavior are described by the Hill equation:

$$v = \frac{V_{\max}[S]^n}{K^n + [S]^n} \tag{28}$$

where the Hill coefficient $n$ characterizes the degree of cooperativity [73]. Significantly such responses could serve as the paradigm for fundamental components of cellular decision-making of threshold response and bistable switching from graded biochemical interactions [64]. Metabolic flux analysis and metabolic control analysis [32] arise as a result of considering coupled systems of ODEs related to metabolic networks with substrate being the product of one enzyme in the reaction and input for another. Such frameworks enable a quantitative assessment of the control of pathway flux and demonstrate that generally control lies distributed and not in one rate-limited step [27]. Models that include the allosteric feedback regulation of PFK can naturally generate oscillations in glycolysis which were first noted in yeast cell extracts [74, 75].


#### Neural Dynamics and Signaling Pathways

Hodgkin and Huxley's model of nerve impulse propagation was one of the triumphs of mathematical biology [18]. The membrane potential dynamics are governed by:

$$C_m \frac{dV}{dt} = -g_{Na} m^3 h (V - E_{Na}) - g_K n^4 (V - E_K) - g_L (V - E_L) + I_{\text{ext}} \tag{29}$$

where $C_m$ is the membrane capacitance, $g_{Na}$, $g_K$, and $g_L$ are the maximal conductances for sodium, potassium and leak channels, $m$, $h$, and $n$ are gating variables satisfying their own first-order ODEs, $E_{Na}$, $E_K$, and $E_L$ are reversal potentials, and $I_{\text{ext}}$ is the external current [18, 19]. This system of four coupled ODEs captures the shape of the action potential, its threshold, refractoriness, and the ability to fire repetitively, quantitatively and remarkably well [19]. The model is based on the concept of fast positive feedback (sodium channel activation) and slow negative feedback (sodium inactivation and potassium activation) [29]. There have been several attempts to reduce the dimensionality of the spiking response to facilitate the analysis by phase plane using "simplified" neural models such as the FitzHugh-Nagumo and Morris-Lecar models [77]. These simplified models reveal the geometrical structure that underlies excitability, oscillation and bistability in neurons [29]. At the network level, coupled neural oscillator models describe synchronization phenomena, generation of patterns in central pattern generators that regulate locomotion, and collective rhythms of cortical networks [36, 62]. The intracellular signaling pathways, involving cascades of protein phosphorylation, systems of second messengers and gene regulatory networks, are modeled using networks of coupled ODE systems with Michaelis-Menten kinetics, Hill functions and mass-action kinetics [44, 73]. The ultrasensitive behavior of the MAPK signaling pathway is modeled, and oscillatory and amplifying behavior in the cellular response to DNA damage can be outlined through models of the p53-Mdm2 feedback loop [45]. These models have proved vital for understanding of information processing in the cell and as a tool for drug target identification [6, 27].

#### Cardiac and Physiological Rhythm Modeling

The heart's electrical activity is modeled using detailed ionic models of cardiac myocytes, extending the Hodgkin-Huxley framework to include multiple ion channels (calcium, sodium, potassium), intracellular calcium handling, and gap junction coupling [35, 36]. Spatial propagation of the cardiac action potential through tissue is described by the monodomain or bidomain equations, which couple the cellular ionic models with tissue-level electrical conduction. The monodomain equation takes the form:

$$\frac{\partial V}{\partial t} = \frac{1}{C_m}\left[D \nabla^2 V - I_{\text{ion}}(V, \mathbf{w})\right] \tag{30}$$

where $D$ is the effective diffusion coefficient representing gap junction coupling, and $I_{\text{ion}}$ is the total ionic current depending on voltage and gating/concentration variables $\mathbf{w}$ [35]. These models can reproduce normal sinus rhythm, predict conditions for reentrant arrhythmias (spiral waves), and simulate the transition to ventricular fibrillation [36]. Mathematical analysis of cardiac dynamics has direct clinical relevance for understanding mechanisms of arrhythmia, optimizing defibrillation strategies, and planning ablation procedures [7, 57].

**Table 3: Key Mathematical Models in Biological Applications**

| Model | Governing Equations | Key Parameters | Primary Predictions |
|-------|-------------------|----------------|-------------------|
| Lotka-Volterra Predator-Prey | dH/dt = aH - bHP; dP/dt = cbHP - dP | a (prey growth), b (predation), c (efficiency), d (predator death) | Neutrally stable oscillations, phase-lagged cycles |
| Logistic Competition | dN₁/dt = r₁N₁(1 - (N₁ + α₁₂N₂)/K₁) | α₁₂, α₂₁ (competition coefficients) | Competitive exclusion or stable coexistence |
| SIR Epidemic | dS/dt = -βSI/N; dI/dt = βSI/N - γI | β (transmission), γ (recovery), R₀ = β/γ | Epidemic threshold, herd immunity at 1 - 1/R₀ |
| Michaelis-Menten Kinetics | v = V_max[S]/(K_m + [S]) | V_max, K_m | Saturating enzyme response |
| Hodgkin-Huxley Neuron | C dV/dt = -I_ion + I_ext (4 ODEs) | g_Na, g_K, channel gating rates | Action potentials, threshold, refractory period |
| Hill Function | v = V_max[S]ⁿ/(Kⁿ + [S]ⁿ) | n (Hill coefficient), K (half-max) | Ultrasensitivity, cooperative switching |
| Rosenzweig-MacArthur | Logistic prey + Type II functional response | K (carrying capacity), handling time | Paradox of enrichment, limit cycles |
| Beeler-Reuter / Luo-Rudy Cardiac | Multi-channel reaction-diffusion PDE | Ion channel conductances, D (diffusion) | Action potential, reentry, fibrillation |


---

## Section 4: Advanced Topics and Future Perspectives

### 4.1 Spatial Models and Reaction-Diffusion Systems

#### Pattern Formation in Biology

A remarkable use of differential equations in biology is the formation of space-time patterns from initially uniform states [17, 28]. How organisms grow into complex spatial forms (stripes, spots, branching patterns, segmented body plans, etc.) from undifferentiated masses of cells has been a source of interest for both biologists and mathematicians [2]. Reaction-diffusion equations are notable theoretical descriptions of such self-organization and show how a combination of local chemical reactions and spatial diffusion can lead to the generation of stable, reproducible patterns, which do not need any template to begin with [34]. Biology has several types of spatial models, each describing to a different extent [33]. Continuum models are continuous descriptions of morphogen concentrations (or cell densities) described by PDEs [2]. Discrete models trace the behaviour of individual cells and/or molecules on lattices and/or networks [46]. Hybrid models are built by merging continuum models of the diffusible signals with discrete models of cellular behavior [8]. Both approaches have unique advantages; a continuum model can be analyzed and there is easy coupling to physical principles, yet a discrete model can account for stochastic effects, and captures individual scale heterogeneity that may be important at small scales [44].

#### Morphogenesis and Turing Patterns

Alan Turing's seminal 1952 paper showed that a system of two interacting chemicals diffusing at different rates could give rise to stable spatial patterning from a homogeneous steady state on its own, in what is now called diffusion-driven instability [17]. A short-range activator which tends to favour its own production and a long-range inhibitor which suppresses activator production is required in the Turing mechanism [28]. At a sufficient mismatch in the diffusion rates of inhibitor and activator, the homogeneous steady state loses stability against space-periodic variations and the solution ultimately becomes patterned [34]. The two-component reaction-diffusion system governing Turing pattern formation is given by:

$$\frac{\partial u}{\partial t} = D_u \nabla^2 u + f(u, v) \tag{31}$$

$$\frac{\partial v}{\partial t} = D_v \nabla^2 v + g(u, v) \tag{32}$$

where $u$ is the activator concentration, $v$ is the inhibitor concentration, $D_u$ and $D_v$ are the respective diffusion coefficients, and $f$, $g$ are the reaction kinetics [17, 34]. The mathematical conditions for Turing instability require that the homogeneous steady state is stable without diffusion but becomes unstable when diffusion is included, which necessitates specific relationships between the kinetic parameters and a sufficiently large ratio $D_v / D_u$ [28]. Turing patterns are found in many biological systems [10]. Pigmentation patterns formed in the zebrafish skin are due to interactions between melanophores and xanthophores, which fit into the Turing-type conditions [48]. In vertebrate limbs, Turing-like interactions among morphogens like WNT, BMP and SOX9 participate in a process of digit formation [28]. We observe that the regular distribution of hair follicles, feather buds and tooth primordia all show reaction-diffusion-like pattern formation phenomena [2]. More recently, experimental progress in synthetic biology has shown the ability to engineer artificial Turing patterns in bacterial colonies, thereby proving the sufficiency of the mathematical mechanism [10].


#### Applications in Developmental Biology

Reaction-diffusion modelling and its extensions can be used to explain a variety of developmental phenomena besides classic Turing patterns [33, 48]. Production-diffusion-degradation equations model morphogen gradient formation. The steady-state morphogen concentration profile for a source at $x = 0$ with linear degradation is described by:

$$C(x) = C_0 \exp\left(-\frac{x}{\lambda}\right), \quad \text{where} \quad \lambda = \sqrt{\frac{D}{k}} \tag{33}$$

where $C_0$ is the source concentration, $D$ is the diffusion coefficient, and $k$ is the degradation rate constant, giving the characteristic decay length $\lambda$ [61]. The French Flag model in which the fate of a cell depends on the relative concentration of the morphogen to specific thresholds relates the dynamics of the gradient to specification of cell fate [61]. Developmental waves are the sequential activation of the expression of genes along the spatial axes, as observed in developmental biology [34]. The clock and wave-front model of somitogenesis is based on oscillatory gene expression (the segmentation clock) and a traveling front of maturation of the vertebral precursors to account for the periodic occurrence of somitogenesis during embryonic development [75]. By using mathematical analysis, it is found that the combination of the oscillation frequency and the velocity of the wavefronts can be used to predict the segment size numerically, as well as to find possible ranges of segment sizes using genetic perturbation experiments [2]. Directed cell migration along a chemical gradient, also known as chemotaxis, is simulated using Keller-Segel equations for the density of cells $\rho$ and the concentration of the chemoattractant $c$ [33]:

$$\frac{\partial \rho}{\partial t} = D_\rho \nabla^2 \rho - \chi \nabla \cdot (\rho \nabla c) \tag{34}$$

where $D_\rho$ is the cell diffusion coefficient and $\chi$ is the chemotactic sensitivity [33]. These models exhibit blow-up solutions and are applicable to processes such as cell aggregation, colony formation of bacteria, and recruitment of immune cells during inflammatory processes. Extensions incorporating cell proliferation, multiple cell types and mechanical interactions describe tissue morphogenesis and wound healing [8, 48].


### 4.2 Computational Tools and Simulation Techniques

#### Numerical Solvers and Software (MATLAB, Python, etc.)

Numerical solution, visualization and analysis software are essential to the applications of differential equations to biology [38, 39]. The use of MATLAB in mathematical biology has a long history and there are ODE solvers (ode45, ode15s, ode23s) with adaptive step-size control, PDE solvers (pdepe), and a lot of visualization capabilities [40]. The interactive domain allows for fast prototyping and model behaviour exploration with respect to parameter space [41]. In the meantime, Python has gained importance as an alternative approach with the SciPy library's integrate module for solving ODEs, and finite-element PDE solution packages, FEniCS and FiPy [39] have been developed to provide a rich environment for scientific computation and analysis and visualization libraries (NumPy, Matplotlib) too. Because Python is free and open source, has a robust community, and integrates easily with other machine learning applications (such as TensorFlow and PyTorch), it's especially appealing for contemporary methods of data-driven biological modeling [6, 21]. Specialized software packages serve niche needs in biological modeling [40]. For biochemical network modeling, frameworks such as COPASI and BioNetGen automatically convert reaction network definitions into ODEs [32]. NEURON and GENESIS focus on the computational neurosciences and provide efficient solvers for cable equations and compartmental neural models [29]. Spatially resolved simulation environments for cell biological modeling are available in Virtual Cell and CellBlender [41]. XPP-AUTO is a hybrid between numerical simulation and bifurcation analysis that is commonly required in investigations of dynamical systems [38, 69].

#### Data-Driven Modeling and Machine Learning Integration

High throughput technologies, including genomics, proteomics, single cell sequencing, and live imaging, have produced massive amounts of biological data which has sparked the use of data-driven approaches alongside conventional mechanistic modelling [6, 21]. In complex biological systems, machine learning approaches, especially Deep Learning, can provide powerful capabilities for pattern recognition, prediction and dimensionality reduction. An increasingly exciting area is that of combining mechanistic models with machine learning [7]. Physics-informed neural networks (PINNs) solve PDEs by incorporating the physics constraints into the network training process, formulated as:

$$\mathcal{L}_{\text{PINN}} = \mathcal{L}_{\text{data}} + \lambda_{\text{PDE}} \mathcal{L}_{\text{PDE}} + \lambda_{\text{BC}} \mathcal{L}_{\text{BC}} \tag{35}$$

where $\mathcal{L}_{\text{data}}$ enforces agreement with observed data, $\mathcal{L}_{\text{PDE}}$ penalizes violations of the governing PDE, and $\mathcal{L}_{\text{BC}}$ enforces boundary conditions, allowing solution of PDEs in complex geometries as well as inference of model parameters from sparse and noisy data sets [42]. Neural ordinary differential equations (Neural ODEs) use neural networks to represent the vector field of a dynamical system found from time-series data without a priori knowledge of a mechanistic model [51]:

$$\frac{d\mathbf{x}}{dt} = f_\theta(\mathbf{x}, t) \tag{36}$$

where $f_\theta$ is a neural network parameterized by weights $\theta$ [51]. The symbolic regression and sparse identification of nonlinear dynamics (SINDy) algorithms extract governing equations directly from the data determining parsimonious mathematical equations that can be used to explain observed dynamics [80]. These methods fall between the extreme of being purely data-driven and having mechanistic models; they have the benefits of machine learning and also the interpretability of differential equation models [56]. They can be used in studying the dynamics of gene regulatory networks, deriving reduced order models of complex biochemical systems, and inferring spatial dynamics from images [7, 80].


#### Sensitivity Analysis and Optimization

Sensitivity analysis involves quantifying how changes in the values of model parameters affect the model output, allowing identification of which parameters most strongly influence the model output and which ones cannot be determined precisely based on available data [50, 54]. Local sensitivity analysis calculates partial sensitivities of the model's output components with respect to the parameters; global sensitivity analysis methods examine the entire parameter space (Sobol indices, Morris screening, Latin hypercube sampling) and consider parameter interactions [52]. In the field of biological modeling sensitivity analysis can have several purposes: to look for important experimental objectives (such as finding out for which parameters precise measurements are needed in order to get a low prediction uncertainty), to help model reduction (if the model is insensitive to several parameters the values can be rather fixed without the loss of an important part of the prediction accuracy), and to check the robustness of the model (evolutionary selection for robustness is related to the insensitiveness of the biological system to perturbations) [53, 54]. Optimisation techniques, such as gradient-based methods, evolutionary strategies and Bayesian optimisation, enable systematic parameter estimation, optimal experimental design and identification of intervention strategies to optimise biological outcomes and processes [50, 52]. Multi-objective optimization also considers the multi-objective optimization problem which occurs in the biological world when several competing objectives (efficacy and toxicity, speed and accuracy, growth and defense) have to be taken into account at the same time [55, 57].

**Table 4: Computational Tools, Advanced Methods, and Future Directions in Mathematical Biology**

| Category | Tool/Method | Application Domain | Key Capabilities |
|----------|------------|-------------------|-----------------|
| General-Purpose Software | MATLAB (ode45, ode15s) | ODE/PDE numerical solution | Adaptive step-size, stiff solvers, visualization |
| Open-Source Platform | Python (SciPy, FEniCS) | Scientific computing, ML integration | Community support, TensorFlow/PyTorch compatibility |
| Biochemical Modeling | COPASI, BioNetGen | Metabolic/signaling networks | Automatic ODE generation from reactions |
| Neuroscience | NEURON, GENESIS | Neural circuit simulation | Cable equation solvers, compartmental models |
| Machine Learning | PINNs, Neural ODEs | Data-driven dynamics discovery | PDE solution in complex geometries, parameter inference |
| Equation Discovery | SINDy, Symbolic Regression | Governing equation identification | Parsimonious model discovery from time-series |
| Sensitivity Analysis | Sobol indices, Morris screening | Parameter importance ranking | Global exploration, interaction detection |
| Multiscale Modeling | Agent-based models, homogenization | Tissue-level simulation | Cell-level to continuum bridging |
| Personalized Medicine | Digital twins | Patient-specific prediction | Cardiac ablation planning, oncology dosing |
| Pattern Formation | Turing instability analysis | Developmental biology | Stripe/spot prediction, morphogenesis |


### 4.3 Challenges, Limitations, and Future Directions

#### Data Limitations and Model Uncertainty

Although the field of mathematical biology has made great strides, computational opportunities still largely depend on data quality and availability [50, 51]. Biological observations are noisy, unreliable, and rare in comparison to the number of underlying processes one has to capture [54]. However, there are numerous model parameters that can't be observed directly, and can only be inferred through the analysis of limited observations, resulting in a parameter uncertainty that is passed on in model predictions [52]. Evaluating and quantifying to what extent the model adequately captures the studied biological processes (structural uncertainty) is even more challenging [55]. Biological models can be described by uncertainty, which can be quantified and propagated through the model using Bayesian approaches to model inference [53]. Prior distributions incorporate pre-existing knowledge about the parameters, likelihood functions relate model predictions to the observations, while posterior distributions account for new knowledge using data [52]. Systematic analysis of the merit of model complexity—due to model comparison techniques such as the Bayes factors and information criteria—can help guard against overfitting, while still allowing the identification of potentially real biological mechanisms [50, 56]. A critical component in inferring the meaning of the results is the propriety of a model's identifiability, that is, whether there is unique information in the data that can be used to determine the values of the model's parameters [54]. Structural identifiability is concerned about whether the parameters can be theoretically identified based on perfect measurements; practical identifiability requires taking into account the additional limitations resulting from a finite and noisy number of measurements [51]. Unidentifiable parameters in the model suggest either over-parameterization of the model or the requirement for further experimental measurements of certain parts of the model [55].

#### Multiscale Modeling Challenges

Biological systems are multiply-scaled in nature and processes occur at a wide variety of scales ranging from molecular (nanometer, microsecond) to organismal (meter, year) [8, 20]. Multiscale modeling aims at bridging these hierarchies and accounting for a connection between molecular events and cellular behaviour, cells and tissue level phenomena and tissue interactions and organism level phenomena [6]. Fundamental difficulties include separation of scales, computational complexity, and coupling between models at different resolutions [7]. Three approaches to multiscale modeling are currently being considered: hybrid (interacting models of different scales on a single domain), concurrent (coarse-grained models computed in parallel and coupled at interface scales), and hierarchical (coarse-grained models parameterized by fine-grained models in a separate step) [8, 46]. A highly successful hybrid model approach to tissue-level modelling is agent-based modelling, which involves tracking individual cells as autonomous decision-making entities controlled by internal ODE models, but interacting via mechanical forces and chemical signals [44]. Coarse-grained models retain only the salient aspects of the molecular dynamics [20]. Likewise, relating the characteristics of cellular models to continuum (tissue) descriptions dictates the use of homogenization methods and effective medium theory to map the behavior at the cellular level into continuum models of field equations [33]. Approximations must be considered carefully to be valid when making each transition of scales [8].


#### Emerging Trends in Systems Biology and Personalized Medicine

Medical research and treatment are increasingly moving towards personalized medicine or precision medicine that seeks to shape medical decisions to reflect the individual's biological profile using mathematical modelling, high throughput biological screening and clinical medicine [6, 7]. Patient-specific data, such as genomics data, imaging data and biomarker measurements, are used as input into mathematical models, which are the engine used to derive predictions and treatments for individual patients [57]. Digital twins are computational models of individual patients, tuned by patient-specific information, representing the next frontier in personalized mathematical medicine [7]. Advances in these attempts have included using cardiac digital twins of patient-specific anatomy, electrophysiology, and mechanics for decisions related to ablation and device implantations [35, 36]. Oncological digital twins are used to simulate tumor growth and drug response to inform therapy planning and treatment scheduling [57]. At this early stage the applications show the potential for translation of the mathematical frameworks described throughout this chapter [6]. Systems Biology is grounded in the idea of biological function being a property of an emergent process of interacting elements and networks, and therefore is heavily dependent on dynamical systems theory and differential equations [20, 21]. Genome-scale metabolic models, consisting of thousands of reactions and metabolites, can predict cellular phenotypes from genotypes [32]. The synthesis of all of these in a single computational model of the cell—the so-called whole-cell models—represents the integration of both mathematical and biological knowledge at the cellular level [44, 46]. The future of mathematical biology is in the synergy of mechanistic modelling, data science and experimental biology [6, 7]. Technological developments in single-cell systems, spatial transcriptomics, and live imaging are making more and more datasets available, yet requiring increasingly complex mathematical models to interpret [21]. Combining machine learning with mechanistic models will lead to interpretable, predictive models of biological mechanism at the complexity of real systems [56, 80]. The combination of differential equations, dynamical systems theory and biology will continue to be an important factor in the comprehension of the fundamental principles of life and towards interventions when those principles go awry [1, 5].

---

## Conclusion

The application of differential equations and dynamical systems theory to biology has evolved from isolated mathematical exercises into a comprehensive framework that permeates virtually every subdiscipline of the life sciences. From the elegant simplicity of exponential growth to the computational complexity of patient-specific digital twins, mathematical models provide the quantitative backbone for understanding biological dynamics across all scales of organization. This chapter has traced the arc from foundational principles—the formulation of ODEs and PDEs, the specification of initial and boundary conditions, the distinction between deterministic and stochastic approaches—through the powerful analytical tools of dynamical systems theory—stability analysis, bifurcation theory, and the geometric understanding of phase space—to diverse applications in ecology, epidemiology, cell biology, and physiology. Advanced topics including spatial pattern formation, computational simulation, and data-driven modeling point toward the future directions that will define the field in coming decades. The challenges ahead are substantial: bridging scales, integrating heterogeneous data types, quantifying uncertainty, and translating mathematical insights into clinical practice all require continued innovation at the interface of mathematics, biology, and computation. Yet the trajectory of the field gives cause for optimism. As mathematical biology matures from a specialized niche into an essential component of biological research and medical practice, the differential equations and dynamical systems at its core will continue to illuminate the deep mathematical structures that underlie the complexity of living systems.


---

## References

[1] Murray, J.D. (2002). Mathematical Biology I: An Introduction. 3rd ed. Springer-Verlag, New York.

[2] Murray, J.D. (2003). Mathematical Biology II: Spatial Models and Biomedical Applications. 3rd ed. Springer-Verlag, New York.

[3] Edelstein-Keshet, L. (2005). Mathematical Models in Biology. SIAM, Philadelphia.

[4] Strogatz, S.H. (2015). Nonlinear Dynamics and Chaos: With Applications to Physics, Biology, Chemistry, and Engineering. 2nd ed. Westview Press, Boulder.

[5] Keener, J. and Sneyd, J. (2009). Mathematical Physiology I: Cellular Physiology. 2nd ed. Springer, New York.

[6] Kitano, H. (2002). Systems biology: A brief overview. Science, 295(5560), 1662-1664.

[7] Niederer, S.A., Lumens, J., and Trayanova, N.A. (2019). Computational models in cardiology. Nature Reviews Cardiology, 16(2), 100-111.

[8] Southern, J. et al. (2008). Multi-scale computational modelling in biology and physiology. Progress in Biophysics and Molecular Biology, 96(1-3), 60-89.

[9] Anderson, R.M. and May, R.M. (1991). Infectious Diseases of Humans: Dynamics and Control. Oxford University Press, Oxford.

[10] Kondo, S. and Miura, T. (2010). Reaction-diffusion model as a framework for understanding biological pattern formation. Science, 329(5999), 1616-1620.

[11] Boyce, W.E. and DiPrima, R.C. (2012). Elementary Differential Equations and Boundary Value Problems. 10th ed. John Wiley & Sons, New York.

[12] Fall, C.P. et al. (2002). Computational Cell Biology. Springer-Verlag, New York.

[13] Bernoulli, D. (1760). Essai d'une nouvelle analyse de la mortalité causée par la petite vérole. Mémoires de Mathématiques et de Physique, Académie Royale des Sciences, Paris.

[14] Lotka, A.J. (1925). Elements of Physical Biology. Williams and Wilkins, Baltimore.

[15] Volterra, V. (1926). Fluctuations in the abundance of a species considered mathematically. Nature, 118, 558-560.

[16] Kot, M. (2001). Elements of Mathematical Ecology. Cambridge University Press, Cambridge.

[17] Turing, A.M. (1952). The chemical basis of morphogenesis. Philosophical Transactions of the Royal Society B, 237(641), 37-72.

[18] Hodgkin, A.L. and Huxley, A.F. (1952). A quantitative description of membrane current and its application to conduction and excitation in nerve. Journal of Physiology, 117(4), 500-544.

[19] Koch, C. (1999). Biophysics of Computation: Information Processing in Single Neurons. Oxford University Press, New York.

[20] Ideker, T., Galitski, T., and Hood, L. (2001). A new approach to decoding life: Systems biology. Annual Review of Genomics and Human Genetics, 2, 343-372.

[21] Topol, E.J. (2019). High-performance medicine: The convergence of human and artificial intelligence. Nature Medicine, 25(1), 44-56.

[22] Gotelli, N.J. (2008). A Primer of Ecology. 4th ed. Sinauer Associates, Sunderland.

[23] Hastings, A. (1997). Population Biology: Concepts and Models. Springer-Verlag, New York.

[24] Hethcote, H.W. (2000). The mathematics of infectious diseases. SIAM Review, 42(4), 599-653.

[25] Diekmann, O. and Heesterbeek, J.A.P. (2000). Mathematical Epidemiology of Infectious Diseases: Model Building, Analysis and Interpretation. John Wiley & Sons, Chichester.

[26] Cornish-Bowden, A. (2012). Fundamentals of Enzyme Kinetics. 4th ed. Wiley-Blackwell, Weinheim.

[27] Alon, U. (2019). An Introduction to Systems Biology: Design Principles of Biological Circuits. 2nd ed. CRC Press, Boca Raton.

[28] Maini, P.K., Baker, R.E., and Chuong, C.M. (2006). The Turing model comes of molecular age. Science, 314(5804), 1397-1398.

[29] Izhikevich, E.M. (2007). Dynamical Systems in Neuroscience: The Geometry of Excitability and Bursting. MIT Press, Cambridge.

[30] Hirsch, M.W., Smale, S., and Devaney, R.L. (2013). Differential Equations, Dynamical Systems, and an Introduction to Chaos. 3rd ed. Academic Press, San Diego.

[31] Britton, N.F. (2003). Essential Mathematical Biology. Springer-Verlag, London.

[32] Palsson, B.O. (2015). Systems Biology: Constraint-Based Reconstruction and Analysis. 2nd ed. Cambridge University Press, Cambridge.

[33] Okubo, A. and Levin, S.A. (2001). Diffusion and Ecological Problems: Modern Perspectives. 2nd ed. Springer-Verlag, New York.

[34] Grindrod, P. (1996). The Theory and Applications of Reaction-Diffusion Equations: Patterns and Waves. 2nd ed. Clarendon Press, Oxford.

[35] Pullan, A.J., Buist, M.L., and Cheng, L.K. (2005). Mathematically Modelling the Electrical Activity of the Heart. World Scientific, Singapore.

[36] Keener, J. and Sneyd, J. (2009). Mathematical Physiology II: Systems Physiology. 2nd ed. Springer, New York.

[37] Verhulst, P.F. (1838). Notice sur la loi que la population suit dans son accroissement. Correspondance Mathématique et Physique, 10, 113-121.

[38] Ermentrout, B. (2002). Simulating, Analyzing, and Animating Dynamical Systems: A Guide to XPPAUT. SIAM, Philadelphia.

[39] Langtangen, H.P. and Pedersen, G.K. (2016). Scaling of Differential Equations. Springer Open, Cham.

[40] Shampine, L.F. and Reichelt, M.W. (1997). The MATLAB ODE suite. SIAM Journal on Scientific Computing, 18(1), 1-22.

[41] Loew, L.M. and Schaff, J.C. (2001). The Virtual Cell: A software environment for computational cell biology. Trends in Biotechnology, 19(10), 401-406.

[42] Raissi, M., Perdikaris, P., and Karniadakis, G.E. (2019). Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations. Journal of Computational Physics, 378, 686-707.

[43] Michaelis, L. and Menten, M.L. (1913). Die Kinetik der Invertinwirkung. Biochemische Zeitschrift, 49, 333-369.

[44] Karr, J.R. et al. (2012). A whole-cell computational model predicts phenotype from genotype. Cell, 150(2), 389-401.

[45] Elowitz, M.B. and Leibler, S. (2000). A synthetic oscillatory network of transcriptional regulators. Nature, 403(6767), 335-338.

[46] Gillespie, D.T. (1977). Exact stochastic simulation of coupled chemical reactions. Journal of Physical Chemistry, 81(25), 2340-2361.

[47] Gillespie, D.T. (2007). Stochastic simulation of chemical kinetics. Annual Review of Physical Chemistry, 58, 35-55.

[48] Green, J.B.A. and Sharpe, J. (2015). Positional information and reaction-diffusion: Two big ideas in developmental biology combine. Development, 142(7), 1203-1211.

[49] Segel, L.A. and Slemrod, M. (1989). The quasi-steady-state assumption: A case study in perturbation. SIAM Review, 31(3), 446-477.

[50] Ashyraliyev, M. et al. (2009). Systems biology: Parameter estimation for biochemical models. FEBS Journal, 276(4), 886-902.

[51] Chen, R.T.Q. et al. (2018). Neural ordinary differential equations. Advances in Neural Information Processing Systems, 31, 6571-6583.

[52] Saltelli, A. et al. (2008). Global Sensitivity Analysis: The Primer. John Wiley & Sons, Chichester.

[53] Gelman, A. et al. (2013). Bayesian Data Analysis. 3rd ed. CRC Press, Boca Raton.

[54] Raue, A. et al. (2009). Structural and practical identifiability analysis of partially observed dynamical models by exploiting the profile likelihood. Bioinformatics, 25(15), 1923-1929.

[55] Kirk, P. et al. (2013). Model selection in systems and synthetic biology. Current Opinion in Biotechnology, 24(4), 767-774.

[56] Baker, R.E. et al. (2018). Mechanistic models versus machine learning, a fight worth fighting for the biological community? Biology Letters, 14(5), 20170660.

[57] Corral-Acero, J. et al. (2020). The 'Digital Twin' to enable the vision of precision cardiology. European Heart Journal, 41(48), 4556-4564.

[58] Perko, L. (2001). Differential Equations and Dynamical Systems. 3rd ed. Springer-Verlag, New York.

[59] Guckenheimer, J. and Holmes, P. (1983). Nonlinear Oscillations, Dynamical Systems, and Bifurcations of Vector Fields. Springer-Verlag, New York.

[60] Kaplan, D. and Glass, L. (1995). Understanding Nonlinear Dynamics. Springer-Verlag, New York.

[61] Wolpert, L. (1969). Positional information and the spatial pattern of cellular differentiation. Journal of Theoretical Biology, 25(1), 1-47.

[62] Pikovsky, A., Rosenblum, M., and Kurths, J. (2001). Synchronization: A Universal Concept in Nonlinear Sciences. Cambridge University Press, Cambridge.

[63] Scheffer, M. et al. (2001). Catastrophic shifts in ecosystems. Nature, 413(6856), 591-596.

[64] Ferrell, J.E. and Xiong, W. (2001). Bistability in cell signaling: How to make continuous processes discontinuous, and reversible processes irreversible. Chaos, 11(1), 227-236.

[65] Elaydi, S.N. (2005). An Introduction to Difference Equations. 3rd ed. Springer-Verlag, New York.

[66] May, R.M. (1976). Simple mathematical models with very complicated dynamics. Nature, 261(5560), 459-467.

[67] Cannon, W.B. (1932). The Wisdom of the Body. W.W. Norton, New York.

[68] Scheffer, M. (2009). Critical Transitions in Nature and Society. Princeton University Press, Princeton.

[69] Kuznetsov, Y.A. (2004). Elements of Applied Bifurcation Theory. 3rd ed. Springer-Verlag, New York.

[70] May, R.M. (1973). Stability and Complexity in Model Ecosystems. Princeton University Press, Princeton.

[71] Wiggins, S. (2003). Introduction to Applied Nonlinear Dynamical Systems and Chaos. 2nd ed. Springer-Verlag, New York.

[72] Kermack, W.O. and McKendrick, A.G. (1927). A contribution to the mathematical theory of epidemics. Proceedings of the Royal Society A, 115(772), 700-721.

[73] Goldbeter, A. and Koshland, D.E. (1981). An amplified sensitivity arising from covalent modification in biological systems. Proceedings of the National Academy of Sciences, 78(11), 6840-6844.

[74] Goldbeter, A. (1996). Biochemical Oscillations and Cellular Rhythms. Cambridge University Press, Cambridge.

[75] Pourquié, O. (2003). The segmentation clock: Converting embryonic time into spatial pattern. Science, 301(5631), 328-330.

[76] Crawford, J.D. (1991). Introduction to bifurcation theory. Reviews of Modern Physics, 63(4), 991-1037.

[77] FitzHugh, R. (1961). Impulses and physiological states in theoretical models of nerve membrane. Biophysical Journal, 1(6), 445-466.

[78] Gleick, J. (1987). Chaos: Making a New Science. Viking Penguin, New York.

[79] Glass, L. (2001). Synchronization and rhythmic processes in physiology. Nature, 410(6825), 277-284.

[80] Brunton, S.L., Proctor, J.L., and Kutz, J.N. (2016). Discovering governing equations from data by sparse identification of nonlinear dynamical systems. Proceedings of the National Academy of Sciences, 113(15), 3932-3937.

[81] Staal, A. et al. (2020). Resilience of tropical tree cover: The roles of climate, fire, and herbivory. Global Change Biology, 26(5), 2952-2965.

[82] Kuang, Y. (1993). Delay Differential Equations with Applications in Population Dynamics. Academic Press, Boston.

[83] Courchamp, F., Berec, L., and Gascoigne, J. (2008). Allee Effects in Ecology and Conservation. Oxford University Press, Oxford.

[84] Rosenzweig, M.L. and MacArthur, R.H. (1963). Graphical representation and stability conditions of predator-prey interactions. American Naturalist, 97(895), 209-223.

[85] Rosenzweig, M.L. (1971). Paradox of enrichment: Destabilization of exploitation ecosystems in ecological time. Science, 171(3969), 385-387.

[86] Hardin, G. (1960). The competitive exclusion principle. Science, 131(3409), 1292-1297.

[87] Chesson, P. (2000). Mechanisms of maintenance of species diversity. Annual Review of Ecology and Systematics, 31, 343-366.

[88] Tilman, D. (1982). Resource Competition and Community Structure. Princeton University Press, Princeton.

[89] Li, M.Y. and Muldowney, J.S. (1995). Global stability for the SEIR model in epidemiology. Mathematical Biosciences, 125(2), 155-164.

[90] Adam, D. (2020). Special report: The simulations driving the world's response to COVID-19. Nature, 580(7803), 316-318.

[91] Keeling, M.J. and Rohani, P. (2008). Modeling Infectious Diseases in Humans and Animals. Princeton University Press, Princeton.

[92] Diekmann, O., Heesterbeek, J.A.P., and Metz, J.A.J. (1990). On the definition and the computation of the basic reproduction ratio R₀ in models for infectious diseases in heterogeneous populations. Journal of Mathematical Biology, 28(4), 365-382.

[93] Mossong, J. et al. (2008). Social contacts and mixing patterns relevant to the spread of infectious diseases. PLoS Medicine, 5(3), e74.
