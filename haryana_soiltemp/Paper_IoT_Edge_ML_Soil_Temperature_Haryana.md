# Low-Cost IoT Sensor Network with Edge Machine Learning for Real-Time Multi-Depth Soil Temperature Forecasting in the Rice–Wheat System of Haryana, India

**Author(s):** [Full Name(s)], [Department, Institution, City, Haryana, India], [Email Address], ORCID: [0000-0000-0000-0000]

## Abstract

Soil temperature controls seed germination, root growth, and nutrient turnover, yet weather stations in Haryana rarely measure it below the surface. This paper presents the design and evaluation of a low-cost Internet of Things (IoT) network that measures soil temperature at 5, 10, 20, and 50 cm and forecasts it on the sensor node using a compressed machine learning model. Each node combines an ESP32 microcontroller, four DS18B20 probes, air temperature, humidity, light and soil moisture sensors, and a LoRa radio, at an indicative cost of about ₹4,700. Because the field deployment is still at the design stage, the system was evaluated with a digital twin. A stochastic weather generator tuned to Karnal and Hisar drove a Crank–Nicolson heat-conduction model with a coupled water balance and a rice–wheat crop calendar, and a sensor error model converted the simulated temperatures into realistic probe readings. Persistence, ridge regression, random forest, gradient-boosted trees, and a multi-output multilayer perceptron were trained on two years and tested on a third. One-day-ahead errors at 5 cm were 1.14–1.26 °C at Karnal and 1.30–1.51 °C at Hisar. At seven days, learned models reduced persistence error by 14–29%. Quantising the perceptron to 8-bit integers cut its size from 1,024 to 320 bytes with no loss of accuracy at 5 cm. The estimated battery life of a node is about one year without solar charging. Simulated residue retention lowered 5 cm temperature during the wheat sowing window by 1.55 °C. The results show that on-node forecasting is technically feasible and define the baseline that field data must now test.

**Keywords:** Soil temperature forecasting; Internet of Things; edge machine learning; TinyML; LoRa; rice–wheat system; Haryana; precision agriculture

## 1. Introduction

Soil temperature governs most of the physical, chemical, and biological processes that take place in the root zone. It controls the rate of seed imbibition and germination, root elongation, microbial respiration, nitrogen mineralisation, and the movement of water and heat between the land surface and the atmosphere [1]. Because soil has a much larger heat capacity than air, its temperature lags and damps the daily and seasonal cycles of air temperature, and the size of this lag and damping depends on soil moisture, texture, cover, and depth [2]. Air temperature alone is therefore a poor guide to the thermal conditions that a seed or root actually experiences, particularly in the top 10 cm of soil where most sowing decisions are made.

These relationships matter in Haryana, a state of north-western India where the rice–wheat rotation occupies most of the irrigated cropland. The system has supported national food security for decades, but long-term experiments across the Indo-Gangetic Plains show stagnating or declining yields and growing concern about the sustainability of conventional management [3]. Conservation agriculture, which combines reduced tillage, residue retention, and crop diversification, has been promoted as a way to sustain productivity in South Asia while cutting costs and emissions [4]. Each of these practices changes the soil thermal regime. A layer of rice residue shades the soil surface, slows heating in autumn, and alters the conditions under which wheat is sown in November.

Sowing date is one of the main levers that farmers in Haryana can use to manage heat risk. Satellite analysis has shown that extreme heat above 34 °C accelerates the senescence of wheat in northern India and reduces yield [5], and crop-model ensembles project that each degree of global warming will reduce world wheat production by about 6% [6]. Wheat sown late after rice is especially exposed to heat during grain filling in March. Machines such as the Happy Seeder allow wheat to be drilled directly into rice stubble, which saves time and avoids burning [7]. Residue burning remains a serious source of air pollution in the region [8], and the need to clear fields quickly is one reason it persists. Meanwhile, intensive irrigation of rice has caused rapid depletion of groundwater across north-western India [9], which increases interest in practices such as direct-seeded rice and deficit irrigation that further modify soil temperature and moisture. Reliable, local, depth-resolved soil temperature information would therefore support decisions on sowing, irrigation, and residue management.

Such information is scarce. Most India Meteorological Department stations record air temperature, humidity, wind, and sunshine, but few report soil temperature at several depths, and many records contain gaps. Researchers have responded by estimating soil temperature from routine weather data with statistical and machine learning (ML) models. Bilgili showed that artificial neural networks (ANNs) estimated soil temperature in Adana, Turkey, more accurately than linear regression [10]. Kisi and colleagues compared generalised regression, radial basis function, and multilayer perceptron (MLP) networks at several depths [11], and Talaee applied a co-active neuro-fuzzy inference system to arid and semi-arid sites in Iran [12]. Citakoglu compared ANN, adaptive neuro-fuzzy inference system (ANFIS), and multiple linear regression models across Turkey [13]. Feng and colleagues evaluated extreme learning machines, gradient boosting, random forests, and backpropagation networks in China and found that tree-based models were both accurate and efficient [14]. Sihag and colleagues estimated daily soil temperature at 5 cm in East Azerbaijan, Iran, using an MLP, Gaussian process regression, random forest, and the M5P model tree, and reported that the MLP gave the lowest error [15]. Alizamir and colleagues compared extreme learning machines, ANNs, classification and regression trees, and the group method of data handling for monthly soil temperatures at four depths [16]. More recently, recurrent networks such as the long short-term memory (LSTM) network [17] have been applied to hydrological and land-surface variables, where they learn long-range dependencies directly from time series [18].

This literature has three common limitations. First, nearly all studies rely on archived station records, so the models cannot respond in real time and cannot be used where no station exists. Second, most studies estimate soil temperature at the same time as the weather inputs rather than forecasting it days ahead, which limits their value for planning. Third, models are usually evaluated with a single random split of the data from one or two stations, which can overstate accuracy because neighbouring days are strongly correlated. In the study by Sihag and colleagues, for example, the Gaussian process models fitted the training data almost perfectly but had much larger errors on the test data [15].

The IoT offers a route around the first limitation. Big-data and smart-farming frameworks describe how networks of connected sensors can feed continuous field observations into decision support [19]. Reviews of agricultural IoT have catalogued sensors, communication protocols, and platforms suitable for farms [20], [21], and have identified cost, power supply, connectivity, and data interpretation as the main barriers to adoption in developing regions [22]. Low-power wide-area networks such as LoRa and LoRaWAN can carry small sensor packets over several kilometres of open farmland with very low energy use [23], and they suit rural areas with weak cellular coverage [24]. Edge computing moves processing from the cloud to devices close to the data source, reducing latency, bandwidth, and dependence on continuous connectivity [25]. The emerging field of tiny machine learning (TinyML) applies this idea to microcontrollers with only kilobytes of memory [26], and frameworks such as TensorFlow Lite for Microcontrollers make it practical to run quantised neural networks on such devices [27].

Despite these developments, we found no study that combines low-cost multi-depth soil temperature sensing, LoRa networking, and on-device ML forecasting for the rice–wheat system of Haryana, or that tests whether compressed models running on a microcontroller can match cloud models for this task. This paper addresses that gap. Its objectives are to:

1. design a low-cost, solar-powered sensor node and network architecture for multi-depth soil temperature monitoring in Haryana;
2. build a physically based digital twin of the network at two contrasting sites, Karnal and Hisar, to generate realistic training and testing data before field deployment;
3. compare persistence, ridge regression, random forest, gradient-boosted trees, and a multi-output MLP for forecasting soil temperature 1, 3, and 7 days ahead at four depths, using time-ordered and cross-site validation;
4. quantify the accuracy, memory, and energy cost of running an 8-bit quantised model on the node; and
5. estimate how residue retention changes the soil thermal regime during the wheat sowing window.

The paper is a design and simulation study. All numerical results come from the digital twin, and they should be read as a baseline that the planned field deployment will test, not as field measurements.

## 2. Materials and Methods

### 2.1 Study Region and the Rice–Wheat System

Haryana lies between about 27.6° and 30.9° N and 74.5° and 77.6° E in the Indo-Gangetic Plains. Its climate grades from sub-humid in the north-east to semi-arid in the south-west, and two sites were chosen to represent this gradient. Karnal (29.69° N, 76.99° E) lies in the eastern zone, which receives most of its rainfall from the south-west monsoon between late June and September and has a dense network of canals and tube wells. Hisar (29.15° N, 75.72° E) lies in the western zone, which is drier and hotter in summer, with sandier soils and lower rainfall. Both sites have deep alluvial soils of sandy loam to loam texture, and both are dominated by the rice–wheat or cotton–wheat rotation [3]. For simplicity, the same soil hydraulic and thermal parameters were used at both sites, so differences between the sites in this study arise from climate and not from soil properties.

In the rice–wheat system modelled here, rice is transplanted in late June, kept ponded until late September, and harvested in mid-October. Wheat is sown in the first half of November and harvested in mid-April. Two management practices were represented: conventional tillage (CT), in which rice residue is removed or burned and the soil is tilled before sowing, and zero tillage with residue retention (ZT-R), in which wheat is drilled into standing or chopped rice residue [7], [4].

### 2.2 Sensor Node and Network Architecture

The network follows a three-tier architecture of field, gateway, and cloud layers, with an advisory layer for users (Figure 1). Each field node measures soil temperature at four depths and the main weather variables every 15 minutes, computes a forecast on the device, and transmits both the readings and the forecast over LoRa. A single gateway can serve all nodes within a few kilometres [23]. The gateway forwards packets over a 4G or Wi-Fi link to a cloud database, where data are quality-controlled, models are retrained, and updated model weights are sent back to the nodes. Because each node computes its own forecast, it can keep supplying forecasts to a local display or a nearby farmer's phone even when the backhaul link fails, which is common in rural areas [24], [25].

[Insert Figure 1 here]
Figure 1. Three-Tier IoT–Edge Architecture of the Proposed Soil Temperature Forecasting Network

Figure 2 shows the node hardware. An ESP32-WROOM-32 module with a 240 MHz dual-core processor and 520 KB of static memory acts as the controller. Four waterproof DS18B20 digital probes on a shared 1-Wire bus measure soil temperature at 5, 10, 20, and 50 cm. The manufacturer specifies an accuracy of ±0.5 °C between −10 and +85 °C and a maximum resolution of 0.0625 °C [28]. A BME280 sensor measures air temperature, humidity, and pressure inside a radiation shield. A BH1750 light sensor provides a proxy for incoming solar radiation, and a capacitive sensor measures volumetric soil moisture in the top 10 cm. An SX1276 LoRa transceiver transmits in the 865–867 MHz band that is licence-exempt in India. A 6 W solar panel charges two 18650 lithium-ion cells through a maximum-power-point charger, and a low-quiescent-current regulator supplies 3.3 V. Between measurements the controller and radio enter deep sleep. One node in each cluster also carries a tipping-bucket rain gauge.

[Insert Figure 2 here]
Figure 2. Sensor Node Hardware and Installation Depths of the Soil Temperature Probes

*Installation and calibration.* At each plot the probes are installed in the crop row by augering a 7 cm hole to 55 cm, inserting the probes horizontally into the undisturbed side wall at the four target depths, and backfilling in the original order of soil layers so that bulk density and heat flow are disturbed as little as possible. The cables run to the mast in a shallow trench so that they do not act as heat conductors along the probe line. Because DS18B20 sensors differ by up to a few tenths of a degree, every probe is first placed in a stirred water bath with a reference thermometer at three temperatures (about 5, 25, and 45 °C), and a linear correction is stored in the node's flash memory. One node at each site is installed within 10 m of a reference soil thermometer, such as those operated by CCS Haryana Agricultural University at Hisar or by the ICAR institutes at Karnal, so that drift can be detected during the season. Probes must be removed before deep tillage and reinstalled afterwards; in ZT-R plots they can stay in place for the whole rotation.

*Data handling.* Each 15-minute packet contains the four soil temperatures, the air measurements, the battery voltage, and the current one-, three-, and seven-day forecasts, which fits in a 32-byte LoRa payload. In the cloud layer, readings outside physically plausible limits (below −5 °C or above 70 °C for soil), readings that change by more than 5 °C in 15 minutes at 20 cm or deeper, and runs of identical values longer than six hours are flagged. Daily means are computed only when at least 80% of the readings for that day are valid, and short gaps are filled by linear interpolation. These daily means are the inputs and targets of the forecasting models described in Section 2.4.

Table 1 lists the components and their indicative prices. A complete node costs about ₹4,740, which is a small fraction of the price of a research-grade automatic weather station with soil temperature profiling. The gateway is a shared cost and is not included.

Table 1. Bill of Materials for One Sensor Node (Indicative Online Retail Prices in India, 2026)

| Component | Function | Quantity | Approx. cost (₹) |
|---|---|---|---|
| ESP32-WROOM-32 module | Control, edge inference | 1 | 450 |
| DS18B20 waterproof probe | Soil temperature at 5, 10, 20, 50 cm | 4 | 720 |
| BME280 sensor | Air temperature, humidity, pressure | 1 | 350 |
| BH1750 light sensor | Proxy for solar radiation | 1 | 120 |
| Capacitive soil moisture sensor | Volumetric moisture, 0–10 cm | 1 | 150 |
| SX1276 LoRa module and 865 MHz antenna | Long-range radio link | 1 | 700 |
| 6 W solar panel | Energy harvesting | 1 | 650 |
| CN3791 MPPT charger | Battery charging | 1 | 250 |
| 2 × 18650 cells (6,000 mAh) with holder | Energy storage | 1 set | 600 |
| Low-Iq regulator, PCB, passives | Power supply and wiring | 1 set | 300 |
| IP65 enclosure, radiation shield, PVC mast | Weather protection and mounting | 1 set | 450 |
| **Total per node** | | | **4,740** |

### 2.3 Digital Twin for Data Generation

Field data from the network are not yet available. To develop and test the forecasting pipeline before deployment, a digital twin was built that reproduces the main physical processes at each site and the behaviour of the sensors. The twin has four parts: a weather generator, a soil water balance, a soil heat-conduction model, and a sensor observation model. Its parameters were set from published climate normals for Karnal and Hisar and from standard soil physics values; reanalysis products such as ERA5-Land [29] can be used to refine these settings and to check simulated soil temperatures once the network is installed.

*Solar geometry and radiation.* Extraterrestrial radiation was computed with the FAO-56 procedure [30]. For day of year J, the inverse relative Earth–Sun distance and the solar declination are

$$ d_r = 1 + 0.033\,\cos(2\pi J / 365) $$ (1)

$$ \delta = 0.409\,\sin(2\pi J / 365 - 1.39) $$ (2)

and the sunset hour angle for latitude φ is

$$ \omega_s = \arccos[-\tan(\varphi)\,\tan(\delta)] $$ (3)

Daily extraterrestrial radiation R_a (MJ m⁻² d⁻¹) is then

$$ R_a = (24 \cdot 60 / \pi)\, G_{sc}\, d_r\, [\omega_s \sin\varphi \sin\delta + \cos\varphi \cos\delta \sin\omega_s] $$ (4)

where G_sc = 0.0820 MJ m⁻² min⁻¹ is the solar constant. Incoming solar radiation R_s follows the Ångström relation [31]

$$ R_s = (a_s + b_s\, n/N)\, R_a, \qquad N = 24\,\omega_s / \pi $$ (5)

with a_s = 0.25 and b_s = 0.50, where n is the actual sunshine duration and N the maximum possible duration. The relative sunshine n/N was generated from a seasonal mean that falls during the monsoon, on rainy days, and on foggy winter days, plus random noise.

*Weather generator.* Daily mean air temperature combines a seasonal harmonic, a monsoon cooling term, and a first-order autoregressive anomaly:

$$ T_{a,clim}(J) = A_0 + A_1 \cos[2\pi (J - J_{max})/365] - 1.5\, M(J) $$ (6)

$$ T_a(J) = T_{a,clim}(J) + \varepsilon_J, \qquad \varepsilon_J = \rho\, \varepsilon_{J-1} + \sigma\, \eta_J, \quad \eta_J \sim N(0,1) $$ (7)

Here A_0 and A_1 are the annual mean and amplitude (24.0 and 11.0 °C at Karnal; 24.5 and 12.0 °C at Hisar), J_max is the day of peak temperature, M(J) is a Gaussian monsoon index centred on early August, ρ = 0.75, and σ = 1.4 °C at Karnal and 1.6 °C at Hisar. Rainfall occurrence followed a seasonally varying probability, and rainfall amounts followed an exponential distribution with a larger mean in the monsoon. Relative humidity was modelled as a seasonal function that rises in the monsoon and in winter fog, increases on wet days, and falls when temperature anomalies are positive. Wind speed followed a log-normal distribution with a pre-monsoon maximum. Four years were simulated for each site with a fixed random seed.

*Soil water balance.* Reference evapotranspiration was estimated with the Hargreaves–Samani equation [32]:

$$ ET_0 = 0.0023 \cdot 0.408\, R_a\, (T_a + 17.8)\, \sqrt{\Delta T} $$ (8)

where ΔT is the diurnal temperature range, which was linked to relative sunshine. Volumetric water content θ of the 0–30 cm root zone was updated daily:

$$ \theta_J = \theta_{J-1} + (P_J + I_J - K_c K_s ET_{0,J}) / (1000\, Z_r) - D_J $$ (9)

where P is rainfall (mm), I is irrigation (mm), K_c is a crop coefficient that rises with crop cover f_c and with ponding in rice, K_s is a water stress factor that declines linearly as θ approaches wilting point, Z_r = 0.30 m, and D is drainage of half of any water above field capacity. Rice fields were held at saturation during ponding, and wheat received a 60 mm irrigation whenever θ fell below 0.18 m³ m⁻³, plus a pre-sowing irrigation.

*Upper boundary condition.* The soil surface temperature was set by air temperature plus a radiative heating term that is reduced by crop cover, residue, and surface wetness:

$$ T_0(J) = T_a(J) + \beta\, R_s(J)\, (1 - f_c)(1 - 0.6 f_r)(1 - 0.5 S_e) $$ (10)

where β = 0.30 °C per MJ m⁻² d⁻¹, f_c is the crop cover fraction, f_r is the residue cover fraction (0.7 after rice harvest in ZT-R plots, decaying over the wheat season), and S_e is the effective saturation of the surface soil. This formulation captures the main effects reported for mulched and cropped soils, in which shading and evaporation reduce surface heating [1], [2].

*Heat conduction.* Below the surface, soil temperature T(z, t) obeys the one-dimensional heat-conduction equation

$$ \partial T / \partial t = \partial / \partial z\, (\alpha\, \partial T / \partial z) $$ (11)

The volumetric heat capacity C (J m⁻³ K⁻¹) depends on the bulk density ρ_b, the specific heat of the solids c_s, and the water content [33]:

$$ C(\theta) = \rho_b\, c_s + \theta\, C_w $$ (12)

with ρ_b = 1,450 kg m⁻³, c_s = 800 J kg⁻¹ K⁻¹, and C_w = 4.18 × 10⁶ J m⁻³ K⁻¹. Thermal conductivity λ was computed with the Johansen approach [34], in which the Kersten number K_e interpolates between dry and saturated conductivities as a function of the degree of saturation S_r:

$$ K_e = \log_{10}(S_r) + 1, \qquad S_r > 0.1 $$ (13)

$$ \lambda(\theta) = \lambda_{dry} + (\lambda_{sat} - \lambda_{dry})\, K_e $$ (14)

with λ_dry = 0.35 and λ_sat = 1.60 W m⁻¹ K⁻¹, typical of sandy loam. The thermal diffusivity is then

$$ \alpha = \lambda / C $$ (15)

Equation (11) was solved on a 2 m profile with a 2.5 cm grid using the Crank–Nicolson scheme [35], which is unconditionally stable and second-order accurate in time and space. For node i and time level n,

$$ -\tfrac{r}{2} T_{i-1}^{n+1} + (1 + r)\, T_i^{n+1} - \tfrac{r}{2} T_{i+1}^{n+1} = \tfrac{r}{2} T_{i-1}^{n} + (1 - r)\, T_i^{n} + \tfrac{r}{2} T_{i+1}^{n}, \qquad r = \alpha \Delta t / \Delta z^2 $$ (16)

The resulting tridiagonal system was solved with the Thomas algorithm at four 6-hour sub-steps per day. The lower boundary at 2 m was held at the annual mean air temperature plus 1.5 °C, and the first simulated year was discarded as spin-up.

*Analytical check.* For a homogeneous soil with sinusoidal surface forcing of amplitude A_0 and angular frequency ω, Eq. (11) has the classical solution [36]

$$ T(z, t) = \bar{T} + A_0\, e^{-z/d} \sin(\omega t - z/d) $$ (17)

where the damping depth is

$$ d = \sqrt{2\alpha / \omega} $$ (18)

For the annual cycle and a typical moist-soil diffusivity of α ≈ 0.05 m² d⁻¹ from Eq. (15), Eq. (18) gives d ≈ 2.4 m, so the annual amplitude should fall by about 19% between the surface and 50 cm, with a phase lag of about 12 days. In the numerical model, a harmonic fit to the test-year series gave an annual amplitude of 12.35 °C at 5 cm and 9.47 °C at 50 cm, a reduction of 23%, and a lag of about 5 days. The damping agrees reasonably with theory. The shorter lag is expected because the model differs from the idealised case in three ways: the surface forcing is not sinusoidal, the ponded rice period holds the whole profile near air temperature for several months, and the fixed lower boundary at 2 m is shallower than the semi-infinite soil assumed by Eq. (17).

*Sensor observation model.* Simulated "true" temperatures at each probe depth k were converted into sensor readings using

$$ T_{obs} = Q_{0.0625}\,[\, T_{true} + b_k + \epsilon \,], \qquad \epsilon \sim N(0,\, 0.15^2) $$ (19)

where b_k is a fixed probe bias drawn uniformly from ±0.3 °C, ε is random noise, and Q_0.0625 rounds to the 0.0625 °C resolution of the DS18B20 [28]. In addition, 2% of daily values were removed at random to mimic packet loss and were filled by linear interpolation, as the cloud quality-control routine would do. Only these observed values, never the true temperatures, were used as model inputs and targets.

### 2.4 Forecasting Models

*Inputs and targets.* All inputs were standardised with the mean μ_j and standard deviation s_j of the training data:

$$ \tilde{x}_j = (x_j - \mu_j) / s_j $$ (20)

The input vector for day t contained 16 features:

$$ \mathbf{x}_t = [T_{a,t}, T_{a,t-1}, T_{a,t-2}, RH_t, u_t, n_t, R_{s,t}, P_t, \theta_t, T_{5,t}, T_{10,t}, T_{20,t}, T_{50,t}, T_{5,t-1}, \sin(2\pi J/365), \cos(2\pi J/365)] $$ (21)

where T_a is air temperature, RH relative humidity, u wind speed, n sunshine hours, R_s solar radiation, P rainfall, θ soil moisture, and T_z the observed soil temperature at depth z cm. The two harmonic terms encode the season. The targets were the observed soil temperatures at all four depths h days ahead, with h = 1, 3, and 7. Including current soil temperatures is a key difference from studies that estimate soil temperature from weather alone [10], [15]; an IoT node measures soil temperature directly, so the forecasting task is to predict how it will change.

*Persistence.* The simplest benchmark assumes that soil temperature will not change:

$$ \hat{T}_{z,t+h} = T_{z,t} $$ (22)

Any useful model must beat this benchmark, especially at longer horizons.

*Ridge regression.* Multiple linear regression with an L2 penalty [37] estimates the weight vector as

$$ \hat{\mathbf{w}} = \arg\min_{\mathbf{w}} \sum_t (y_t - \mathbf{w}^{\top} \mathbf{x}_t)^2 + \lambda \lVert \mathbf{w} \rVert^2 = (\mathbf{X}^{\top}\mathbf{X} + \lambda \mathbf{I})^{-1} \mathbf{X}^{\top} \mathbf{y} $$ (23)

with λ = 0.01. One model was fitted for each depth.

*Random forest.* A random forest [38] averages B regression trees, each grown on a bootstrap sample of the training data with a random subset of features considered at each split:

$$ \hat{f}_{RF}(\mathbf{x}) = \frac{1}{B} \sum_{b=1}^{B} f_b(\mathbf{x}) $$ (24)

Each split was chosen to maximise the reduction in squared error, which for a candidate split of node data into left (L) and right (R) subsets is

$$ \Delta SSE = \frac{(\sum_{L} y_i)^2}{n_L} + \frac{(\sum_{R} y_i)^2}{n_R} - \frac{(\sum y_i)^2}{n} $$ (25)

The forest used B = 60 trees, a maximum depth of 12, at least five samples per leaf, five candidate features per split, and 32 quantile bins per feature.

*Gradient-boosted trees.* Gradient boosting [39] builds an additive model in which each new shallow tree h_m is fitted to the residuals of the current ensemble:

$$ F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \nu\, h_m(\mathbf{x}), \qquad h_m \leftarrow r_i = y_i - F_{m-1}(\mathbf{x}_i) $$ (26)

The ensemble used 120 trees of depth 3, a learning rate ν = 0.1, at least ten samples per leaf, and 80% row subsampling.

*Multi-output multilayer perceptron.* The MLP has one hidden layer of 12 rectified linear units and four linear outputs, one per depth:

$$ \mathbf{h} = \mathrm{ReLU}(\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1) $$ (27)

$$ \hat{\mathbf{y}} = \mathbf{W}_2 \mathbf{h} + \mathbf{b}_2, \qquad \mathcal{L} = \frac{1}{4N} \sum_{t=1}^{N} \sum_{k=1}^{4} (\hat{y}_{t,k} - y_{t,k})^2 $$ (28)

Targets were standardised for training. Weights were initialised with He scaling and optimised with Adam [40] at a learning rate of 0.005 and a batch size of 32. The last 15% of the training period was held out for early stopping with a patience of 20 epochs. With 16 inputs, the network has 256 parameters and needs 240 multiply–accumulate operations per forecast, small enough for any modern microcontroller. A single network forecasting all four depths was chosen over four separate networks because it shares the hidden layer and so uses a quarter of the memory.

Hyperparameters were chosen once from common defaults in the literature and kept the same at both sites and all horizons. This avoids tuning on the test year, which would make the comparison optimistic. All models were implemented from first principles in Python using only the standard library, so that the code runs without external dependencies and every reported number can be reproduced exactly. The training set for each site and horizon contained 728 daily samples, and the test sets contained 364, 362, and 358 samples for the one-, three-, and seven-day horizons, because the last days of the record have no future target.

### 2.5 Edge Deployment and Quantisation

To run on the ESP32, the trained MLP was converted to 8-bit integers by post-training quantisation [41]. Weights, inputs, and hidden activations were mapped to signed integers with per-tensor symmetric scale factors:

$$ q = \mathrm{clip}(\mathrm{round}(w / s),\, -127,\, 127), \qquad s = \max |w| / 127 $$ (29)

Biases were stored as 32-bit integers in the accumulator scale, following the integer-arithmetic-only inference scheme used in TensorFlow Lite [41], [27]. Inference in the quantised model uses only integer multiplication and addition until the final rescaling, which suits microcontrollers without fast floating-point hardware [26]. The quantised model was evaluated on the same test data as the full-precision model.

### 2.6 Validation Design and Evaluation Metrics

Two validation designs were used. In the *time-ordered* design, the second and third simulated years (after spin-up) were used for training and the fourth for testing at each site, so the models never saw data from the test period. In the *leave-one-site-out* design, models were trained at Karnal and tested on the Hisar test year without retraining, which simulates deploying a model at a new location. A third test applied the model trained on the Karnal CT plot to the Karnal ZT-R plot to measure the effect of a change in management.

Accuracy was measured with the root mean square error (RMSE), the Nash–Sutcliffe efficiency (NSE) [42], and the Kling–Gupta efficiency (KGE) [43]. For observations O_i, predictions P_i, and n test days,

$$ RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (O_i - P_i)^2} $$ (30)

$$ NSE = 1 - \frac{\sum_{i}(O_i - P_i)^2}{\sum_{i}(O_i - \bar{O})^2} $$ (31)

$$ KGE = 1 - \sqrt{(r - 1)^2 + (\sigma_P / \sigma_O - 1)^2 + (\mu_P / \mu_O - 1)^2} $$ (32)

where r is the Pearson correlation, σ the standard deviation, and μ the mean. NSE and KGE equal 1 for a perfect model. KGE was included because it separates errors in correlation, variability, and bias, which NSE combines [43].

To identify which inputs drive the forecasts, permutation importance [38] was computed for the MLP at 5 cm. The importance of feature j is the increase in test RMSE when its values are randomly shuffled, averaged over five shuffles:

$$ I_j = \frac{1}{5} \sum_{s=1}^{5} RMSE(\mathbf{X}^{(j,s)}) - RMSE(\mathbf{X}) $$ (33)

### 2.7 Energy Budget

The node operates on a 15-minute cycle. In each cycle it wakes, reads the sensors, runs the forecast, and transmits, then returns to deep sleep. The average current and the battery life without solar input are

$$ \bar{I} = \frac{\sum_k t_k I_k}{T_{cyc}}, \qquad L_{batt} = \frac{\eta\, C_{batt}}{24\, \bar{I}} $$ (34)

where t_k and I_k are the duration and current of each phase, T_cyc = 900 s, C_batt = 6,000 mAh, and η = 0.8 is the usable fraction of capacity. The phases were an active period of 4.0 s at 80 mA (sensor conversion, which takes up to 750 ms per DS18B20 at full resolution [28], plus processing), a LoRa transmission of 0.2 s at 120 mA, and deep sleep at 0.15 mA for the remainder, which allows for regulator and sensor leakage. These are datasheet-based estimates, not measurements.

## 3. Results

### 3.1 Simulated Thermal Regime

Table 2 summarises the simulated weather and soil variables for the three analysis years. Mean air temperature was 23.5 °C at Karnal and 24.3 °C at Hisar, and Hisar had the wider range, reaching 43.0 °C in summer. Annual rainfall from the weather generator averaged 578 mm at Karnal and 394 mm at Hisar, which reproduces the east–west gradient across Haryana but is somewhat below long-term normals at both sites. Mean soil temperature at 5 cm was about 3 °C above mean air temperature at both sites, and the standard deviation of soil temperature decreased with depth, from 9.1 °C at 5 cm to 6.8 °C at 50 cm at Karnal.

Table 2. Descriptive Statistics of Simulated Daily Variables (Three Analysis Years, CT Plots)

| Variable | Karnal mean | Karnal min | Karnal max | Karnal SD | Hisar mean | Hisar min | Hisar max | Hisar SD |
|---|---|---|---|---|---|---|---|---|
| Air temperature (°C) | 23.47 | 7.15 | 39.16 | 7.94 | 24.32 | 6.81 | 43.04 | 8.59 |
| Relative humidity (%) | 51.26 | 20.83 | 94.59 | 14.94 | 44.76 | 18.09 | 86.73 | 14.00 |
| Wind speed (m s⁻¹) | 1.52 | 0.38 | 6.25 | 0.65 | 1.66 | 0.50 | 5.33 | 0.64 |
| Sunshine duration (h) | 8.29 | 1.02 | 13.08 | 2.17 | 8.56 | 0.64 | 12.91 | 1.90 |
| Solar radiation (MJ m⁻² d⁻¹) | 18.71 | 7.84 | 29.60 | 4.83 | 19.13 | 9.18 | 29.29 | 4.52 |
| Soil moisture (m³ m⁻³) | 0.28 | 0.12 | 0.45 | 0.11 | 0.27 | 0.12 | 0.45 | 0.12 |
| Soil temperature 5 cm (°C) | 26.30 | 10.19 | 44.94 | 9.06 | 27.21 | 9.31 | 49.75 | 9.73 |
| Soil temperature 10 cm (°C) | 26.31 | 10.88 | 44.00 | 8.80 | 26.87 | 9.62 | 48.31 | 9.43 |
| Soil temperature 20 cm (°C) | 25.90 | 12.12 | 42.19 | 8.29 | 26.99 | 11.44 | 46.50 | 8.88 |
| Soil temperature 50 cm (°C) | 26.28 | 15.81 | 39.50 | 6.82 | 26.67 | 14.75 | 41.88 | 7.31 |

Figure 3 shows the simulated test year at Karnal. Soil temperature at 5 cm tracks air temperature closely in winter, when crop cover and low radiation limit surface heating, and exceeds it by 5–8 °C in May and June, when the soil is bare and dry before rice transplanting. Once the rice field is flooded in July, the soil profile becomes almost isothermal and closely follows air temperature. Temperature at 50 cm is damped and lags the surface, remaining warmer than the surface from October to February. This pattern agrees with the analytical behaviour described by Eqs. (17) and (18) and with the general behaviour of irrigated alluvial soils [1].

[Insert Figure 3 here]
Figure 3. Simulated Daily Air Temperature and Soil Temperature at 5, 20, and 50 cm, Karnal Test Year (CT Plot)

### 3.2 Forecast Accuracy by Model, Depth, and Horizon

Table 3 reports the test-year RMSE of every model at every depth and horizon. Errors increased with forecast horizon and decreased with depth for all models, because deeper soil changes more slowly. For one-day forecasts at Karnal, RMSE at 5 cm ranged from 1.14 °C for ridge regression to 1.26 °C for gradient-boosted trees, and at 50 cm it ranged from 0.20 to 0.36 °C. At this horizon, persistence was already a strong benchmark (1.16 °C at 5 cm), because soil temperature changes little from one day to the next.

Table 3. Test-Year RMSE (°C) of Soil Temperature Forecasts by Model, Horizon, and Depth

| Model | Horizon (days) | Karnal 5 cm | Karnal 10 cm | Karnal 20 cm | Karnal 50 cm | Hisar 5 cm | Hisar 10 cm | Hisar 20 cm | Hisar 50 cm |
|---|---|---|---|---|---|---|---|---|---|
| Persistence | 1 | 1.16 | 0.93 | 0.64 | 0.36 | 1.35 | 1.06 | 0.72 | 0.39 |
| Ridge (MLR) | 1 | 1.14 | 0.87 | 0.50 | 0.20 | 1.30 | 1.01 | 0.55 | 0.20 |
| Random forest | 1 | 1.20 | 0.92 | 0.56 | 0.29 | 1.48 | 1.16 | 0.70 | 0.38 |
| Gradient-boosted trees | 1 | 1.26 | 0.97 | 0.59 | 0.29 | 1.51 | 1.21 | 0.71 | 0.34 |
| MLP | 1 | 1.25 | 0.97 | 0.60 | 0.29 | 1.39 | 1.06 | 0.66 | 0.38 |
| Persistence | 3 | 1.95 | 1.71 | 1.33 | 0.75 | 2.31 | 2.01 | 1.59 | 0.93 |
| Ridge (MLR) | 3 | 1.74 | 1.52 | 1.16 | 0.50 | 2.03 | 1.78 | 1.35 | 0.57 |
| Random forest | 3 | 1.77 | 1.56 | 1.19 | 0.54 | 2.11 | 1.89 | 1.43 | 0.66 |
| Gradient-boosted trees | 3 | 1.86 | 1.63 | 1.27 | 0.57 | 2.24 | 1.98 | 1.52 | 0.69 |
| MLP | 3 | 1.88 | 1.75 | 1.37 | 0.76 | 2.17 | 1.94 | 1.48 | 0.65 |
| Persistence | 7 | 2.54 | 2.32 | 1.96 | 1.31 | 3.46 | 3.16 | 2.67 | 1.75 |
| Ridge (MLR) | 7 | 1.97 | 1.80 | 1.51 | 0.90 | 2.47 | 2.26 | 1.90 | 1.14 |
| Random forest | 7 | 2.11 | 1.91 | 1.60 | 0.96 | 2.67 | 2.44 | 2.03 | 1.19 |
| Gradient-boosted trees | 7 | 2.15 | 1.97 | 1.66 | 1.00 | 2.66 | 2.43 | 2.02 | 1.21 |
| MLP | 7 | 2.19 | 2.05 | 1.79 | 1.24 | 2.64 | 2.52 | 2.12 | 1.40 |

The advantage of learned models grew with horizon (Figure 4). At seven days and 5 cm, ridge regression reduced RMSE relative to persistence by 22% at Karnal (from 2.54 to 1.97 °C) and by 29% at Hisar (from 3.46 to 2.47 °C). The MLP reduced it by 14% and 24%, and the tree ensembles by 15–23%. Gains were larger at Hisar, where higher temperature variability makes persistence less reliable. Ridge regression was the most accurate model at every site, depth, and horizon. The MLP and random forest were usually within 0.2 °C of it, and the largest gap was 0.34 °C, for the MLP at 50 cm seven days ahead at Karnal. Every learned model had an NSE above 0.91 and a KGE above 0.92 at every depth and horizon.

The pattern of error with depth also has practical meaning. At 5 cm, a seven-day RMSE of 2.0–2.7 °C is comparable to the day-to-day variability of soil temperature in spring and autumn, so forecasts at this depth are most useful for one to three days. At 50 cm, even seven-day forecasts have errors of about 1 °C, which is adequate for planning decisions that depend on deeper soil warmth, such as the timing of root-zone irrigation in summer or the assessment of conditions for tuber crops grown in rotation.

[Insert Figure 4 here]
Figure 4. Test-Year RMSE of Soil Temperature Forecasts at 5 cm by Model and Forecast Horizon, Karnal and Hisar

Figure 5 compares observed and forecast values for the MLP at 5 cm one day ahead at Karnal. Points cluster tightly around the 1:1 line across the full range from about 10 to 45 °C (NSE = 0.981, KGE = 0.987). The largest errors occurred on days with abrupt changes, such as the first heavy monsoon rain or the onset of a winter cold wave, which cannot be anticipated from the previous day's conditions without a weather forecast.

[Insert Figure 5 here]
Figure 5. Agreement Between Observed and Forecast Soil Temperature at 5 cm, One-Day MLP Forecast, Karnal Test Year

### 3.3 Generalisation Across Sites and Management

In the leave-one-site-out test, models trained only on Karnal were applied to the Hisar test year. One-day RMSE at 5 cm was 1.33 °C for ridge regression, 1.48 °C for the MLP, 1.61 °C for gradient-boosted trees, and 1.62 °C for random forest. Compared with models trained at Hisar itself (Table 3), the penalty was 0.03 °C for ridge regression, 0.09 °C for the MLP, and about 0.10–0.14 °C for the tree ensembles. The tree models degraded more because Hisar's summer temperatures exceeded the range seen at Karnal, and trees cannot extrapolate beyond the range of their training targets. At 50 cm, the cross-site RMSE of random forest (0.56 °C) was 47% higher than its within-site value (0.38 °C), while the MLP increased by only 0.03 °C.

The management test produced two findings. First, residue retention changed the thermal regime. During the wheat sowing window (mid-October to late November), mean simulated temperature at 5 cm was 20.85 °C under CT and 19.30 °C under ZT-R, a reduction of 1.55 °C; at 10 cm the reduction was 1.49 °C. Over the whole wheat growing period from mid-November to the end of February the difference shrank to 0.48 °C as the residue decomposed and the crop canopy closed. Second, a model trained on the CT plot still forecast the ZT-R plot well, with one-day RMSE at 5 cm of 1.32 °C compared with 1.25 °C on the CT plot itself. The small penalty arises because the model uses current soil temperature as an input, which already carries the effect of the residue.

### 3.4 Edge Deployment

Table 4 compares the full-precision and quantised MLP. Quantisation reduced the stored model from 1,024 to 320 bytes, a 69% reduction, and left the RMSE at 5 cm unchanged (1.249 versus 1.248 °C). At greater depths, where errors are smaller, quantisation added 0.01–0.03 °C. Both versions fit easily in the memory of the ESP32, and even of much smaller 8-bit microcontrollers. The model needs 240 multiply–accumulate operations per forecast, so inference time is negligible compared with the 750 ms needed for each DS18B20 conversion.

Table 4. Edge Deployment Characteristics of the Multi-Output MLP (Karnal, One-Day Horizon)

| Characteristic | Full precision (float32) | Quantised (int8) |
|---|---|---|
| Parameters | 256 | 256 |
| Multiply–accumulate operations per forecast | 240 | 240 |
| Model storage (bytes) | 1,024 | 320 |
| RMSE at 5 cm (°C) | 1.249 | 1.248 |
| RMSE at 10 cm (°C) | 0.969 | 0.979 |
| RMSE at 20 cm (°C) | 0.597 | 0.620 |
| RMSE at 50 cm (°C) | 0.291 | 0.323 |
| KGE at 5 cm | 0.987 | 0.986 |
| Estimated average node current (mA) | 0.53 | 0.53 |
| Estimated daily charge (mAh) | 12.8 | 12.8 |
| Estimated battery life without solar (days) | 376 | 376 |

The energy budget from Eq. (34) gives an average current of 0.53 mA, or 12.8 mAh per day, which corresponds to about 376 days of operation on the usable battery capacity without any solar input. In practice, battery self-discharge and cold-weather capacity loss will shorten this, but even a fraction of a day of sunshine on the 6 W panel replaces a day's consumption, so the energy budget is not a constraint. The active wake period, most of which is spent waiting for sensor conversions, accounts for about two-thirds of the daily charge and deep sleep for most of the rest; the forecast itself uses a negligible share.

### 3.5 Drivers of the Forecast

Figure 6 shows the permutation importance of each input for the one-day MLP forecast at 5 cm. Current air temperature was the most important input (2.70 °C increase in RMSE when shuffled), followed by current soil temperature at 5 cm (2.56 °C) and the seasonal cosine term (2.25 °C). Soil temperature at 10 cm, the previous day's soil and air temperatures, and soil moisture formed a second group. Relative humidity, rainfall, and wind speed contributed almost nothing. This ranking agrees with earlier findings that air temperature is the dominant predictor of soil temperature [11], [14], and it shows that in an IoT setting, direct soil measurements are nearly as informative as air temperature.

[Insert Figure 6 here]
Figure 6. Permutation Feature Importance for the One-Day MLP Forecast at 5 cm, Karnal

## 4. Discussion

### 4.1 Accuracy in Context

The one-day errors obtained here (1.14–1.51 °C at 5 cm) are lower than those reported for estimation from weather data alone. Sihag and colleagues reported a best testing RMSE of 3.26 °C at Tabriz and 6.33 °C at Ahar for 5 cm soil temperature two days ahead [15], and Feng and colleagues and Alizamir and colleagues reported errors of a similar order at shallow depths [14], [16]. The comparison is not like for like, because our data are simulated and our models also use current soil temperature. It does, however, illustrate the main argument for an IoT approach: once soil temperature is measured directly, forecasting its change over the next few days is a much easier problem than estimating it from air temperature, humidity, and sunshine. The strong performance of the persistence benchmark at one day reinforces this point and shows why every soil temperature forecasting study should report it.

The most notable result is that ridge regression matched or beat the non-linear models in most cases. This differs from much of the published literature, in which ANNs and tree ensembles usually outperform linear regression [10], [13], [15]. Two explanations apply. First, heat conduction is linear in temperature (Eq. 11), so in a soil whose properties change slowly, future temperatures are close to a linear function of current temperatures and forcing. The non-linearities in the digital twin, which come from moisture-dependent conductivity and the crop calendar, were too weak to give flexible models an advantage with only two years of training data. Second, our validation was strictly time-ordered. Random splits, which are common in earlier studies, allow flexible models to interpolate between neighbouring days and can inflate their apparent advantage. The near-perfect training fit and much poorer test fit of the Gaussian process models in Sihag and colleagues [15] is a sign of this effect.

This result should not be over-generalised. Real fields contain processes that the digital twin represents only crudely or not at all, including variable irrigation timing, the shading of individual residue patches, cracking in drying clay, frost, and sensor drift. Such processes may give non-linear models a real advantage, and the field deployment is designed to test this. For edge deployment, the practical lesson is that model choice should be based on measured accuracy and cost rather than complexity. If ridge regression proves as accurate on field data, it would need only 68 parameters for four depths, compared with 256 for the MLP.

### 4.2 Value of Edge Machine Learning

The quantisation results confirm that a soil temperature forecasting model can run on a low-cost microcontroller with no loss of useful accuracy. This agrees with the wider experience of TinyML, in which 8-bit integer models typically lose little accuracy relative to floating-point versions [26], [41]. The model is small enough that memory and computation are not limiting; the real constraints are sensing energy and communication. Computing the forecast on the node has three practical benefits for Haryana. It allows forecasts to continue when the cellular backhaul fails, which is common in rural areas [24]. It allows the node to transmit only alerts or summaries when bandwidth is limited, extending battery life under LoRa duty-cycle limits [23]. And it allows a farmer with a phone to read forecasts directly from a nearby node over Bluetooth without a data plan. A cloud layer remains essential for retraining, for combining information across nodes, and for integrating numerical weather forecasts, which edge models cannot access on their own [25].

### 4.3 Implications for Rice–Wheat Management

The simulated 1.55 °C cooling of the seed zone under residue retention during the sowing window is consistent with the known effects of mulch [1], [2], and it has practical consequences. Wheat germinates over a wide temperature range, but emergence slows as temperature falls, so the cooler seedbed under residue may delay emergence of late-sown wheat. On the other hand, the same cooling effect in March could reduce soil and canopy heating during grain filling, partly offsetting the heat stress that limits wheat yields in northern India [5], [6]. A network that measures and forecasts soil temperature under both practices would let extension staff quantify these trade-offs on farmers' fields rather than infer them. It would also give a direct, local signal of the best sowing window, which could help farmers using the Happy Seeder decide when to sow [7] and reduce the time pressure that encourages residue burning [8].

The finding that a CT-trained model transferred well to the ZT-R plot is encouraging for scaling. It suggests that a model trained at one well-instrumented site could be deployed on nodes in neighbouring fields under different management, provided each node measures soil temperature itself. The cross-site test gave a similar message for transfer from Karnal to Hisar, although the poorer extrapolation of the tree models shows that training data should cover the full range of conditions at the target sites.

### 4.4 Practical Deployment and Adoption in Haryana

Technical feasibility is only one condition for impact. Reviews of agricultural IoT identify cost, maintenance, connectivity, and the difficulty of turning data into decisions as the main reasons that sensor networks fail to scale among smallholders [20], [22]. The design choices in this study respond to each of these. The node cost of about ₹4,740 is low enough for a cluster of nodes to be purchased by a Krishi Vigyan Kendra, a farmer producer organisation, or a village cooperative rather than by individual farmers. One gateway can serve all nodes within several kilometres of open farmland [23], so the network cost per farm falls as more fields join. Solar power and a battery life of months remove the need for regular battery changes, and the absence of moving parts other than the optional rain gauge keeps maintenance to an annual check of probe calibration and enclosure seals.

The value of the data depends on how it is delivered. Most farmers in Haryana use mobile phones, but not all use smartphone applications, so the advisory layer should send short messages in Hindi with a clear recommendation, such as whether the seedbed is warm enough for sowing in the coming days, rather than raw temperatures. Extension staff can use a dashboard that compares plots under different practices. Data from a dense network could also be shared with the India Meteorological Department and with state agricultural agencies to improve the soil temperature component of district-level agro-advisories, which currently rely heavily on air temperature. Data ownership and privacy should be agreed with participating farmers before deployment, and the data should be made openly available in aggregated form so that researchers can extend the analysis.

Finally, the approach can be extended to other variables at little extra cost. The same node already measures soil moisture and could forecast it with the same multi-output network, which would support irrigation scheduling in a state where groundwater is falling rapidly [9]. Adding low-cost leaf wetness or canopy temperature sensors would allow the network to support disease and heat-stress advisories.

### 4.5 Limitations and Future Work

The study has several limitations. The most important is that all results come from a digital twin rather than field measurements. The twin represents the main physical processes, but its parameters are generic, its weather generator produced annual rainfall below long-term normals, and its surface energy balance is simplified to a single radiative heating term (Eq. 10). The accuracies reported here should therefore be treated as a baseline. Field data may show higher errors, especially at 5 cm during irrigation and rainfall events.

Second, the hardware performance figures are estimates. The cost estimates in Table 1 depend on market prices, and the energy budget in Eq. (34) uses typical datasheet values. Probe accuracy, enclosure heating, battery ageing, and LoRa packet loss must all be measured in the field. Third, only daily forecasts were modelled, although the network will record data every 15 minutes, and sub-daily forecasts of frost or heat may be more useful in some seasons. Fourth, the models used only the node's own data. Integrating numerical weather predictions from the India Meteorological Department would likely improve forecasts at three and seven days, when persistence of recent conditions is less informative.

Future work will proceed in three steps. First, a pilot network of six nodes will be installed on paired CT and ZT-R plots at Karnal and Hisar for at least one full rice–wheat cycle, with one node at each site placed next to a reference station for calibration. Second, the models developed here will be retrained and tested on field data, with explainability methods such as SHAP [44] used to compare the drivers of soil temperature in field and simulated data. Third, physics-guided learning, in which the heat-conduction equation is built into the loss function or architecture of the network, will be explored as a way to combine the reliability of the physical model with the flexibility of ML [45]. Such hybrid models could keep the predicted temperature profile physically consistent across depths and may extrapolate better to new sites and to warmer climates.

## 5. Conclusion

This study designed a low-cost IoT network for multi-depth soil temperature monitoring and forecasting in the rice–wheat system of Haryana and evaluated it with a physically based digital twin of two contrasting sites, Karnal and Hisar. A sensor node built from widely available components costs about ₹4,740 and is estimated to run for about a year on its batteries alone, with a small solar panel providing ample margin.

Five forecasting approaches were compared at four depths and three horizons using strictly time-ordered and cross-site validation. One-day forecasts at 5 cm had errors of about 1.1–1.5 °C, and errors fell below 0.4 °C at 50 cm. Persistence was a strong benchmark at one day, but learned models reduced seven-day errors by up to 29%. Ridge regression was as accurate as the random forest, gradient-boosted trees, and multilayer perceptron in most cases, which reflects the near-linear physics of heat conduction and shows the value of testing simple models before complex ones. The multilayer perceptron, quantised to 8-bit integers, occupied 320 bytes and lost no accuracy at 5 cm, which confirms that soil temperature forecasting can run on a low-cost microcontroller.

Simulated residue retention lowered seed-zone temperature during the wheat sowing window by about 1.5 °C, and a model trained under conventional tillage still forecast the residue-covered plot accurately. These results indicate that on-farm networks of this kind could give farmers and extension staff timely, local information for sowing, irrigation, and residue management. Because the findings rest on simulation, the next step is a field deployment at Karnal and Hisar to measure real sensor performance, test the models on observed data, and determine whether non-linear and physics-guided models offer gains that the digital twin could not reveal.

## Data and Code Availability

All data in this paper were generated by the digital twin described in Section 2.3. The complete simulation, modelling, and figure code (`simulate_and_model.py`, `make_figures.py`) runs with the Python standard library and reproduces every reported number from a fixed random seed.

## References

[1] Hillel, D. (1998). *Environmental soil physics*. Academic Press.

[2] Campbell, G. S., & Norman, J. M. (1998). *An introduction to environmental biophysics* (2nd ed.). Springer. https://doi.org/10.1007/978-1-4612-1626-1

[3] Ladha, J. K., Dawe, D., Pathak, H., Padre, A. T., Yadav, R. L., Singh, B., Singh, Y., Singh, Y., Singh, P., Kundu, A. L., Sakal, R., Ram, N., Regmi, A. P., Gami, S. K., Bhandari, A. L., Amin, R., Yadav, C. R., Bhattarai, E. M., Das, S., … Hobbs, P. R. (2003). How extensive are yield declines in long-term rice–wheat experiments in Asia? *Field Crops Research, 81*(2–3), 159–180. https://doi.org/10.1016/S0378-4290(02)00219-8

[4] Jat, M. L., Chakraborty, D., Ladha, J. K., Rana, D. S., Gathala, M. K., McDonald, A., & Gerard, B. (2020). Conservation agriculture for sustainable intensification in South Asia. *Nature Sustainability, 3*(4), 336–343. https://doi.org/10.1038/s41893-020-0500-2

[5] Lobell, D. B., Sibley, A., & Ortiz-Monasterio, J. I. (2012). Extreme heat effects on wheat senescence in India. *Nature Climate Change, 2*(3), 186–189. https://doi.org/10.1038/nclimate1356

[6] Asseng, S., Ewert, F., Martre, P., Rötter, R. P., Lobell, D. B., Cammarano, D., Kimball, B. A., Ottman, M. J., Wall, G. W., White, J. W., Reynolds, M. P., Alderman, P. D., Prasad, P. V. V., Aggarwal, P. K., Anothai, J., Basso, B., Biernath, C., Challinor, A. J., De Sanctis, G., … Zhu, Y. (2015). Rising temperatures reduce global wheat production. *Nature Climate Change, 5*(2), 143–147. https://doi.org/10.1038/nclimate2470

[7] Sidhu, H. S., Manpreet-Singh, Humphreys, E., Yadvinder-Singh, Balwinder-Singh, Dhillon, S. S., Blackwell, J., Bector, V., Malkeet-Singh, & Sarbjeet-Singh. (2007). The Happy Seeder enables direct drilling of wheat into rice stubble. *Australian Journal of Experimental Agriculture, 47*(7), 844–854. https://doi.org/10.1071/EA06225

[8] Jain, N., Bhatia, A., & Pathak, H. (2014). Emission of air pollutants from crop residue burning in India. *Aerosol and Air Quality Research, 14*(1), 422–430. https://doi.org/10.4209/aaqr.2013.01.0031

[9] Rodell, M., Velicogna, I., & Famiglietti, J. S. (2009). Satellite-based estimates of groundwater depletion in India. *Nature, 460*(7258), 999–1002. https://doi.org/10.1038/nature08238

[10] Bilgili, M. (2010). Prediction of soil temperature using regression and artificial neural network models. *Meteorology and Atmospheric Physics, 110*(1–2), 59–70. https://doi.org/10.1007/s00703-010-0104-x

[11] Kisi, O., Tombul, M., & Kermani, M. Z. (2015). Modeling soil temperatures at different depths by using three different neural computing techniques. *Theoretical and Applied Climatology, 121*(1–2), 377–387. https://doi.org/10.1007/s00704-014-1232-x

[12] Talaee, P. H. (2014). Daily soil temperature modeling using neuro-fuzzy approach. *Theoretical and Applied Climatology, 118*(3), 481–489. https://doi.org/10.1007/s00704-013-1084-9

[13] Citakoglu, H. (2017). Comparison of artificial intelligence techniques for prediction of soil temperatures in Turkey. *Theoretical and Applied Climatology, 130*(1–2), 545–556. https://doi.org/10.1007/s00704-016-1914-7

[14] Feng, Y., Cui, N., Hao, W., Gao, L., & Gong, D. (2019). Estimation of soil temperature from meteorological data using different machine learning models. *Geoderma, 338*, 67–77. https://doi.org/10.1016/j.geoderma.2018.11.044

[15] Sihag, P., Esmaeilbeiki, F., Singh, B., & Pandhiani, S. M. (2020). Model-based soil temperature estimation using climatic parameters: The case of Azerbaijan Province, Iran. *Geology, Ecology, and Landscapes, 4*(3), 203–215. https://doi.org/10.1080/24749508.2019.1610841

[16] Alizamir, M., Kisi, O., Ahmed, A. N., Mert, C., Fai, C. M., Kim, S., Kim, N. W., & El-Shafie, A. (2020). Advanced machine learning model for better prediction accuracy of soil temperature at different depths. *PLOS ONE, 15*(4), Article e0231055. https://doi.org/10.1371/journal.pone.0231055

[17] Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation, 9*(8), 1735–1780. https://doi.org/10.1162/neco.1997.9.8.1735

[18] Kratzert, F., Klotz, D., Brenner, C., Schulz, K., & Herrnegger, M. (2018). Rainfall–runoff modelling using long short-term memory (LSTM) networks. *Hydrology and Earth System Sciences, 22*(11), 6005–6022. https://doi.org/10.5194/hess-22-6005-2018

[19] Wolfert, S., Ge, L., Verdouw, C., & Bogaardt, M.-J. (2017). Big data in smart farming – A review. *Agricultural Systems, 153*, 69–80. https://doi.org/10.1016/j.agsy.2017.01.023

[20] Tzounis, A., Katsoulas, N., Bartzanas, T., & Kittas, C. (2017). Internet of Things in agriculture, recent advances and future challenges. *Biosystems Engineering, 164*, 31–48. https://doi.org/10.1016/j.biosystemseng.2017.09.007

[21] Elijah, O., Rahman, T. A., Orikumhi, I., Leow, C. Y., & Hindia, M. N. (2018). An overview of Internet of Things (IoT) and data analytics in agriculture: Benefits and challenges. *IEEE Internet of Things Journal, 5*(5), 3758–3773. https://doi.org/10.1109/JIOT.2018.2844296

[22] Ray, P. P. (2017). Internet of things for smart agriculture: Technologies, practices and future direction. *Journal of Ambient Intelligence and Smart Environments, 9*(4), 395–420. https://doi.org/10.3233/AIS-170440

[23] Augustin, A., Yi, J., Clausen, T., & Townsley, W. M. (2016). A study of LoRa: Long range & low power networks for the Internet of Things. *Sensors, 16*(9), Article 1466. https://doi.org/10.3390/s16091466

[24] Centenaro, M., Vangelista, L., Zanella, A., & Zorzi, M. (2016). Long-range communications in unlicensed bands: The rising stars in the IoT and smart city scenarios. *IEEE Wireless Communications, 23*(5), 60–67. https://doi.org/10.1109/MWC.2016.7721743

[25] Shi, W., Cao, J., Zhang, Q., Li, Y., & Xu, L. (2016). Edge computing: Vision and challenges. *IEEE Internet of Things Journal, 3*(5), 637–646. https://doi.org/10.1109/JIOT.2016.2579198

[26] Warden, P., & Situnayake, D. (2019). *TinyML: Machine learning with TensorFlow Lite on Arduino and ultra-low-power microcontrollers*. O'Reilly Media.

[27] David, R., Duke, J., Jain, A., Janapa Reddi, V., Jeffries, N., Li, J., Kreeger, N., Nappier, I., Natraj, M., Wang, T., Warden, P., & Rhodes, R. (2021). TensorFlow Lite Micro: Embedded machine learning for TinyML systems. *Proceedings of Machine Learning and Systems, 3*, 800–811.

[28] Maxim Integrated. (2019). *DS18B20 programmable resolution 1-Wire digital thermometer* (Datasheet Rev. 6). Maxim Integrated Products.

[29] Muñoz-Sabater, J., Dutra, E., Agustí-Panareda, A., Albergel, C., Arduini, G., Balsamo, G., Boussetta, S., Choulga, M., Harrigan, S., Hersbach, H., Martens, B., Miralles, D. G., Piles, M., Rodríguez-Fernández, N. J., Zsoter, E., Buontempo, C., & Thépaut, J.-N. (2021). ERA5-Land: A state-of-the-art global reanalysis dataset for land applications. *Earth System Science Data, 13*(9), 4349–4383. https://doi.org/10.5194/essd-13-4349-2021

[30] Allen, R. G., Pereira, L. S., Raes, D., & Smith, M. (1998). *Crop evapotranspiration: Guidelines for computing crop water requirements* (FAO Irrigation and Drainage Paper No. 56). Food and Agriculture Organization of the United Nations.

[31] Ångström, A. (1924). Solar and terrestrial radiation. *Quarterly Journal of the Royal Meteorological Society, 50*(210), 121–126. https://doi.org/10.1002/qj.49705021008

[32] Hargreaves, G. H., & Samani, Z. A. (1985). Reference crop evapotranspiration from temperature. *Applied Engineering in Agriculture, 1*(2), 96–99. https://doi.org/10.13031/2013.26773

[33] de Vries, D. A. (1963). Thermal properties of soils. In W. R. van Wijk (Ed.), *Physics of plant environment* (pp. 210–235). North-Holland.

[34] Johansen, O. (1975). *Thermal conductivity of soils* [Doctoral dissertation, Norwegian University of Science and Technology]. (CRREL Draft English Translation 637, 1977).

[35] Crank, J., & Nicolson, P. (1947). A practical method for numerical evaluation of solutions of partial differential equations of the heat-conduction type. *Mathematical Proceedings of the Cambridge Philosophical Society, 43*(1), 50–67. https://doi.org/10.1017/S0305004100023197

[36] Carslaw, H. S., & Jaeger, J. C. (1959). *Conduction of heat in solids* (2nd ed.). Oxford University Press.

[37] Hoerl, A. E., & Kennard, R. W. (1970). Ridge regression: Biased estimation for nonorthogonal problems. *Technometrics, 12*(1), 55–67. https://doi.org/10.1080/00401706.1970.10488634

[38] Breiman, L. (2001). Random forests. *Machine Learning, 45*(1), 5–32. https://doi.org/10.1023/A:1010933404324

[39] Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. *Annals of Statistics, 29*(5), 1189–1232. https://doi.org/10.1214/aos/1013203451

[40] Kingma, D. P., & Ba, J. (2015). Adam: A method for stochastic optimization. In *Proceedings of the 3rd International Conference on Learning Representations (ICLR)*. https://arxiv.org/abs/1412.6980

[41] Jacob, B., Kligys, S., Chen, B., Zhu, M., Tang, M., Howard, A., Adam, H., & Kalenichenko, D. (2018). Quantization and training of neural networks for efficient integer-arithmetic-only inference. In *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition* (pp. 2704–2713). https://doi.org/10.1109/CVPR.2018.00286

[42] Nash, J. E., & Sutcliffe, J. V. (1970). River flow forecasting through conceptual models part I – A discussion of principles. *Journal of Hydrology, 10*(3), 282–290. https://doi.org/10.1016/0022-1694(70)90255-6

[43] Gupta, H. V., Kling, H., Yilmaz, K. K., & Martinez, G. F. (2009). Decomposition of the mean squared error and NSE performance criteria: Implications for improving hydrological modelling. *Journal of Hydrology, 377*(1–2), 80–91. https://doi.org/10.1016/j.jhydrol.2009.08.003

[44] Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In *Advances in Neural Information Processing Systems 30* (pp. 4765–4774).

[45] Karpatne, A., Atluri, G., Faghmous, J. H., Steinbach, M., Banerjee, A., Ganguly, A., Shekhar, S., Samatova, N., & Kumar, V. (2017). Theory-guided data science: A new paradigm for scientific discovery from data. *IEEE Transactions on Knowledge and Data Engineering, 29*(10), 2318–2331. https://doi.org/10.1109/TKDE.2017.2720168
