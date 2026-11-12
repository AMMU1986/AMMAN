# Comparing Empirical and Machine-Learning Models for Predicting Soil Infiltration Rate in Hisar, Haryana, India

**Author Name¹\*, Co-author Name¹, Co-author Name²**

¹ Department of Civil Engineering, [Institution], Hisar, Haryana, India
² Department of Soil Science, [Institution], Hisar, Haryana, India
\* Corresponding author: [email address]

**Note:** **DATA STATUS – READ BEFORE USE.** The infiltration and soil-property dataset analysed in this manuscript is an illustrative, synthetically generated dataset built from soil-property ranges typical of the Hisar region. It was produced so that the complete workflow, tables and figures could be demonstrated end to end. It is not a record of field measurements. Before submission, replace hisar_data/site_properties.csv and hisar_data/infiltration_observations.csv with your own double-ring infiltrometer and laboratory data, re-run hisar_infiltration_analysis.py and hisar_figures.py, and update every number in the Abstract, Results, Discussion, Conclusions and Tables 1–4. Site names, coordinates and author details are placeholders.

## Abstract

Field infiltration tests are slow, so infiltration rates are rarely measured at every location where irrigation or recharge design needs them. This study compared five empirical infiltration models (Kostiakov, Modified Kostiakov, Philip, Horton and the Novel model of Sihag et al.) with four machine-learning models (multiple linear regression, MLR; artificial neural network, ANN; random forest, RF; Gaussian process regression, GPR) for the sandy loam and loamy sand soils of Hisar, Haryana, India. Double-ring infiltrometer tests at 15 sites under seven land-use groups gave 210 readings, which were split into 150 training and 60 testing readings, the same for every model. Empirical models were calibrated at each site; machine-learning models were trained on pooled data with elapsed time, sand, clay, bulk density, moisture content and organic carbon as inputs. On the testing data, Modified Kostiakov and Novel models gave the lowest RMSE (1.95 mm/h, NSE = 0.986), closely followed by ANN (1.98 mm/h), Philip (2.00 mm/h), Kostiakov (2.04 mm/h) and GPR (2.09 mm/h); RF (4.33 mm/h) and MLR (9.67 mm/h) were less accurate. The Novel model proved to be a re-parameterisation of the Modified Kostiakov model. When whole sites were withheld, all machine-learning errors rose sharply, and RF transferred best (RMSE = 11.46 mm/h, NSE = 0.684). Elapsed time was the dominant input. Empirical models remain the best choice where a field test exists, while machine-learning models need many more sites before they can replace field tests at new locations.

**Keywords:** Infiltration rate; Double-ring infiltrometer; Kostiakov model; Machine learning; Random forest; Gaussian process regression; Hisar; Semi-arid soils

## 1. Introduction

Infiltration is the process by which water at the soil surface enters the soil profile {hillel}. It controls how rainfall and irrigation water are divided between surface runoff, soil-water storage and deep percolation, and it is therefore a key input to the design of surface irrigation systems, the planning of groundwater recharge structures and the calibration of rainfall–runoff models {mishra, chahinian}. The infiltration rate of a soil is highest when water is first applied and declines with time towards a nearly constant value, usually called the steady or basic infiltration rate. The shape of this decline depends on soil texture, structure, bulk density, organic matter, antecedent moisture, surface sealing and land management {hillel, haghighi}.

In the field, infiltration rate is most often measured with a double-ring infiltrometer {bouwer, astm}. The method is simple and widely accepted, but a single test takes two to four hours, requires a large volume of water and gives information for one point only. Because infiltration varies strongly in space, even within a single field {machiwal}, many tests are needed to characterise a district. This has led to two broad modelling approaches. The first fits an infiltration equation to the measured curve at each site so that the curve can be summarised by a few parameters and extrapolated in time. The second predicts infiltration from more easily measured soil properties, either through regression-based pedotransfer functions {wosten} or, more recently, through machine-learning methods {sihag_gpr, singh_rf, vand, angelaki}.

Infiltration equations are usually grouped into physically based, semi-empirical and empirical models {mishra}. Physically based models such as Green–Ampt {greenampt} and Philip {philip} are derived from Darcy's law and mass conservation, with Richards' equation {richards} as the general governing equation. Empirical models such as Kostiakov {kostiakov} and Horton {horton} describe the shape of the measured curve without explicit reference to soil physics. Many comparative studies have found that no single equation is best everywhere. Mishra et al. {mishra} compared fourteen models on laboratory and field data and found that performance depended on the data set. Machiwal et al. {machiwal} found Philip's model suitable for a lateritic wasteland at Kharagpur, Haghighi et al. {haghighi} reported different best models for different soils in Iran, and Turner {turner} reached a similar conclusion in a rainfall-simulator study in the United States. Sihag et al. {sihag2017} compared Kostiakov, Modified Kostiakov and the Soil Conservation Service models at ten sites on the NIT Kurukshetra campus in Haryana and proposed a "Novel" three-parameter model, f = a t^-b + c·ic, which gave the lowest average errors at that site.

Machine-learning methods offer a different route. Instead of describing one curve, they learn a mapping from time and soil properties to infiltration rate across many sites. Gaussian process regression {rasmussen}, random forests {breiman}, artificial neural networks {haykin} and model trees have all been applied to infiltration data in north India and Iran, and several studies have reported higher accuracy than the Kostiakov model {sihag_gpr, singh_rf, vand, angelaki}. Most of these studies, however, split individual readings at random into training and testing sets. Because readings from the same site share the same soil properties and lie on the same smooth curve, a random split allows the model to see part of every test curve during training. Such a test measures interpolation within known sites rather than prediction at new locations, which is the use case that actually reduces the number of field tests {roberts}. Comparisons of this kind can also be unfair to empirical models if the empirical models are not evaluated on exactly the same withheld points.

Hisar district, in semi-arid south-western Haryana, has mostly coarse alluvial and aeolian soils (sandy loam to sand) with low organic carbon and high, variable infiltration capacity. Irrigation depends on canals and groundwater, and the high intake rate of these light soils makes furrow and border design sensitive to the infiltration function used. Land use ranges from wheat–cotton and wheat–rice fields to fallow, orchards, grassland, compacted surfaces and sand dunes, which makes the district a useful test region.

The objectives of this study were to (i) characterise the infiltration behaviour of soils under seven land-use groups in Hisar district using double-ring infiltrometer tests; (ii) calibrate and compare five empirical infiltration models at each site; (iii) develop four machine-learning models (MLR, ANN, RF and GPR) that predict infiltration rate from elapsed time and five soil properties; (iv) compare all nine models on a common testing set, and test the machine-learning models at sites withheld entirely from training; and (v) identify the inputs that most influence the machine-learning predictions.

## 2. Materials and Methods

### 2.1 Study area

Hisar district (approximately 29.15° N, 75.72° E, about 215 m above mean sea level) is located in the south-western part of Haryana, about 165 km north-west of New Delhi. The climate is semi-arid and sub-tropical, with hot summers in which maximum temperatures exceed 40 °C in May and June, and cool winters. Most of the annual rainfall, which is roughly 400–450 mm, falls during the south-west monsoon between July and September, and inter-annual variability is high. The landscape is a nearly level alluvial plain with scattered sand dunes and sandy hummocks. Soils are predominantly sandy loam and loamy sand, alkaline in reaction and low in organic carbon. Groundwater in parts of the district is brackish, so canal water and rainfall are important sources of recharge.

Fifteen test sites (S1–S15) were selected to represent the main land uses of the district: cultivated land under wheat–cotton, mustard–pearl millet and wheat–rice rotations (S1–S4), fallow land (S5–S7), orchard and agroforestry plantations (S8–S9), permanent grassland (S10–S11), compacted surfaces along roadsides and cattle tracks (S12–S13), and sandy plains with dunes (S14–S15). The land use and measured soil properties of each site are listed in Table 1.

### 2.2 Field infiltration tests

Infiltration was measured with a double-ring infiltrometer following standard procedures {astm, bouwer}. The inner and outer rings were 30 cm and 60 cm in diameter and 30 cm high. Both rings were driven about 10 cm into the soil with a falling-weight hammer striking a wooden plank placed across the ring, so that the soil surface was disturbed as little as possible. The annular space and inner ring were filled to the same depth, and the outer ring acted as a buffer that reduced lateral flow from the inner ring. The drop in water level in the inner ring was read against a hook gauge, and water was added to keep the head within a 2–3 cm band. Readings were taken at elapsed times of 5, 10, 15, 20, 30, 40, 50, 60, 75, 90, 105, 120, 150 and 180 min. The infiltration rate (mm/h) for each interval was computed from the depth of water infiltrated divided by the interval length. Each test continued for 180 min, by which time the rate had become approximately constant at all sites. Fourteen readings at each of 15 sites gave 210 observations.

### 2.3 Soil sampling and laboratory analysis

A disturbed soil sample (0–15 cm) and an undisturbed core sample were collected next to each ring immediately before the test. Particle-size distribution was determined by the hydrometer method {bouyoucos} and texture was classified using the USDA triangle. Bulk density (BD) was determined by the core method {blake}. Antecedent gravimetric moisture content (MC) was measured by oven-drying at 105 °C for 24 h, and organic carbon (OC) was determined by the Walkley–Black wet-oxidation method {walkley}. Silt content was not used as a separate model input because sand, silt and clay sum to 100 %.

### 2.4 Empirical infiltration models

Five empirical or semi-empirical models were used. In all equations f is the infiltration rate (mm/h) and t is elapsed time (min unless stated).

**Kostiakov model** {kostiakov}:

f(t) = a t^-b          (1)

where a and b are fitting parameters (a > 0, 0 < b < 1).

**Modified Kostiakov model** {mishra}:

f(t) = a t^-b + ic          (2)

where ic is a fitted parameter that represents the steady infiltration rate.

**Philip model** {philip}:

f(t) = ½ S t^-½ + A          (3)

where S is the sorptivity (mm/h^½) and A is a parameter related to the saturated hydraulic conductivity (mm/h). In Eq. (3) t is expressed in hours.

**Horton model** {horton}:

f(t) = fc + (f0 − fc) e^(−kt)          (4)

where f0 and fc are the initial and final infiltration rates (mm/h) and k is a decay constant (1/min).

**Novel model** {sihag2017}:

f(t) = a t^-b + c ic          (5)

where ic is the observed final infiltration rate at the site and a, b and c are fitting parameters.

The parameters of each model were estimated separately for each site by minimising the sum of squared errors between observed and predicted rates using the Levenberg–Marquardt algorithm {marquardt}. Only the training readings of a site were used to fit its parameters (Section 2.6), so that the empirical models were evaluated on the same withheld readings as the machine-learning models.

### 2.5 Machine-learning models

All machine-learning models used the same six inputs: elapsed time (t, min), sand (%), clay (%), bulk density (BD, g/cm³), antecedent moisture content (MC, %) and organic carbon (OC, %). The output was the infiltration rate f (mm/h). Inputs were standardised to zero mean and unit variance using the statistics of the training set. Unlike the empirical models, which are calibrated site by site, a single machine-learning model was trained on the pooled data from all sites.

#### 2.5.1 Multiple linear regression (MLR)

MLR assumes a linear relationship between the inputs and the infiltration rate:

f = β0 + β1 t + β2 Sand + β3 Clay + β4 BD + β5 MC + β6 OC          (6)

The coefficients were estimated by ordinary least squares.

#### 2.5.2 Artificial neural network (ANN)

A feed-forward multilayer perceptron {haykin} with one hidden layer of eight neurons (a 6–8–1 architecture), a hyperbolic tangent activation in the hidden layer and a linear output neuron was used. The network was trained on the standardised natural logarithm of f, which reduces the strong positive skew of the infiltration-rate distribution, and predictions were back-transformed. Weights were initialised randomly and optimised with the Adam algorithm {kingma} (learning rate 0.01) for 4000 full-batch epochs with a small L2 weight penalty (10^-4) to limit over-fitting. With eight hidden neurons the network has 65 weights and biases, well below the 150 training readings.

#### 2.5.3 Random forest (RF)

Random forest {breiman} is an ensemble of regression trees, each grown on a bootstrap sample of the training data. At every split only a random subset of the inputs is considered, which reduces the correlation between trees, and the forest prediction is the average of the tree predictions. A forest of 200 trees was grown with three candidate inputs per split, a minimum of two observations per leaf and a maximum depth of 12. Out-of-bag predictions were used as an internal check on generalisation.

#### 2.5.4 Gaussian process regression (GPR)

Gaussian process regression {rasmussen} is a non-parametric Bayesian method that places a prior distribution over functions and conditions it on the training data. A squared-exponential covariance function with automatic relevance determination (ARD) was used:

k(x, x′) = σf² exp[ −½ Σj (xj − x′j)² / ℓj² ] + σn² δ(x, x′)          (7)

where σf² is the signal variance, ℓj is a separate length scale for input j, σn² is the noise variance and δ is the Kronecker delta. As for the ANN, the target was the standardised logarithm of f. The hyper-parameters were estimated by minimising the negative log marginal likelihood of the training data. A short length scale indicates that the prediction changes quickly with that input and therefore that the input is influential.

### 2.6 Data partition and validation design

The 210 readings were divided into a training set of 150 readings (about 70 %) and a testing set of 60 readings (about 30 %). The split was stratified by site: at each site, four of the twelve interior readings were randomly assigned to the testing set, while the first (5 min) and last (180 min) readings were kept in the training set so that every fitted curve was anchored at both ends. The same split was used for all nine models. Every model is therefore judged on the same 60 readings. This corresponds to the random splitting used in earlier infiltration studies {sihag_gpr, vand} and tests interpolation within sites that the model has seen.

To test the more demanding case of prediction at new locations, a leave-sites-out cross-validation {roberts} was applied to the four machine-learning models. The 15 sites were randomly divided into five folds of three sites each. In each fold the model was trained on all readings from the remaining twelve sites and used to predict all readings from the three withheld sites. Predictions from the five folds were then pooled and evaluated together. Empirical models were not included in this test because they cannot predict a site without first fitting a measured curve at that site.

### 2.7 Performance evaluation

Model performance was quantified with five statistics computed from the observed (Oi) and predicted (Pi) infiltration rates, where n is the number of readings and an overbar denotes the mean:

CC = Σ(Oi − Ō)(Pi − P̄) / √[Σ(Oi − Ō)² Σ(Pi − P̄)²]          (8)

RMSE = √[(1/n) Σ(Oi − Pi)²]          (9)

MAE = (1/n) Σ|Oi − Pi|          (10)

NSE = 1 − Σ(Oi − Pi)² / Σ(Oi − Ō)²          (11)

Bias = (1/n) Σ(Pi − Oi)          (12)

RMSE gives more weight to large errors than MAE. NSE {nash} equals 1 for a perfect fit and is ≤ 0 when the model is no better than the observed mean, and a positive Bias indicates over-prediction. Following common practice for hydrological models {moriasi}, NSE > 0.75 was regarded as very good and 0.65–0.75 as good. The percentage of predictions within ±20 % of the observed value was also reported. A one-way analysis of variance (ANOVA) at the 5 % significance level was used to test whether the means of the observed and predicted testing values differed significantly.

### 2.8 Sensitivity analysis

The influence of each input was assessed for RF and GPR by removing one input at a time, retraining the model with the remaining five inputs on the same training set, and recording the testing RMSE. The larger the increase in RMSE when an input is removed, the more important that input is to the model. The GPR length scales and the Pearson correlation of each input with f were used as supporting indicators.

## 3. Results

### 3.1 Soil properties and observed infiltration behaviour

Table 1 summarises the soil properties and observed infiltration rates. Sand content ranged from 58 % to 86 % and clay from 5 % to 18 %, so that twelve sites were classified as sandy loam and three (S5, S14 and S15) as loamy sand. Bulk density ranged from 1.44 g/cm³ under the orchard (S8) to 1.71 g/cm³ on the compacted roadside surface (S12). Antecedent moisture content ranged from 2.1 % at the dune site S14 to 10.9 % at the wheat–rice site S4. Organic carbon was low everywhere (0.16–0.66 %) and was highest under orchard, agroforestry and grassland.

Table 1. Land use, soil properties and observed initial (5 min) and final (180 min) infiltration rates at the 15 test sites.

{TABLE1}

All sites showed the typical pattern of a high initial rate that fell rapidly during the first 30–40 min and then approached a steady value (Figure 2). Initial rates ranged from 19.1 mm/h at the cattle track (S13) to 122.1 mm/h on the sandy plain (S14), and final rates from 3.0 mm/h at S4 to 24.5 mm/h at S15, a range of about eight times. Final infiltration rates were highest on the loamy sands (S5, S14, S15: 22.1–24.5 mm/h) and on the loose, organic-rich soils under orchard and agroforestry (S8, S9: 22.0 and 21.7 mm/h). They were lowest on the compacted surfaces (S12, S13: 3.1 and 3.9 mm/h), at the wet wheat–rice site (S4: 3.0 mm/h) and at the fallow site S7 (3.5 mm/h). The final rates on the compacted surfaces were about one-third of those of the cultivated and grassland sandy loams S1 and S10 (11.6 and 13.6 mm/h), although the compacted sites also contained slightly more clay.

Across the whole data set the infiltration rate had a mean of 24.1 mm/h and was strongly skewed (skewness 1.9 in the training set) because high rates occur only in the first few readings. The Pearson correlation of f with the individual inputs was −0.52 for time, 0.53 for sand, −0.54 for clay, −0.44 for bulk density, −0.31 for moisture content and 0.02 for organic carbon. No single soil property therefore explained more than about 30 % of the variance in f, which suggests that the inputs act jointly and non-linearly. The mean observed rate was 24.7 mm/h in the training set and 22.9 mm/h in the testing set, which had a lower maximum (73.9 mm/h) because the 5-min readings were kept for training.

Figure 1. Methodological framework of the study.

[Insert Figure 1 here]

### 3.2 Calibration of empirical models

The ranges and mean values of the fitted parameters are given in Table 2. For the Kostiakov model, a ranged from 43.0 to 287.6 and b from 0.36 to 0.65 (mean 0.50). The highest values of a occurred on the sandy plain and orchard sites, which had the highest initial rates. For the Horton model, f0 ranged from 24.1 to 150.5 mm/h, fc from 3.8 to 25.7 mm/h and k from 0.042 to 0.074 per minute. The fitted fc values were close to, and slightly above, the observed final rates in Table 1, which supports the physical interpretation of fc as the steady rate. The Philip sorptivity S ranged from 11.0 to 72.0 mm/h^½ and was highest at the sandy plain (S14) and orchard (S8) sites.

Table 2. Range and mean (± standard deviation) of the fitted parameters of the empirical models over the 15 sites, and mean coefficient of determination of the site fits (training readings).

{TABLE2}

All five models fitted the training readings very closely, with mean site-level R² values between 0.985 (Kostiakov) and 0.991 (Horton) and a minimum of 0.972 at any site. Two problems with the parameters, however, were apparent. First, the steady-rate parameter ic of the Modified Kostiakov model was negative at several sites (minimum −8.5 mm/h), and the Philip parameter A was negative at several sites (minimum −4.3 mm/h). Negative values have no physical meaning as a steady infiltration rate or hydraulic conductivity. They arise because, over a 180-min test, the power-law term can describe almost the whole curve, so the constant term is poorly constrained and trades off against a and b. Second, the Novel model returned exactly the same a and b values and the same predictions as the Modified Kostiakov model at every site. The fitted coefficient c ranged from −1.91 to 0.62, and the product c·ic always equalled the Modified Kostiakov ic. For example, at S4, c = −1.913 and the observed ic = 3.0 mm/h, so c·ic = −5.74 mm/h, which is the fitted Modified Kostiakov constant at that site. This equivalence is examined in the Discussion.

Figure 2 compares the fitted curves with the observed rates at four contrasting sites. At the sandy plain (S14) and orchard (S8) sites the initial rates exceeded 120 mm/h and fell to 22–24 mm/h. At the wheat–rice (S4) and compacted (S12) sites the initial rates were around 20 mm/h and fell to about 3 mm/h. All models captured the general shape of the curve. The power-law models (Kostiakov, Modified Kostiakov, Novel) and the Philip model continued to decline slowly at the end of the test, whereas the Horton model flattened earlier. As a result, Horton tended to under-predict rates between about 40 and 60 min and to over-predict the final readings at the low-rate sites S4 and S12.

Figure 2. Observed infiltration rates and fitted empirical models at four representative sites: (a) S14, sandy plain; (b) S8, orchard; (c) S4, cultivated wheat–rice; (d) S12, compacted roadside. The Novel model curve (dashed) coincides with the Modified Kostiakov curve.

[Insert Figure 2 here]

### 3.3 Performance of empirical and machine-learning models

Table 3 lists the performance statistics of all nine models on the training and testing data. On the testing data, all five empirical models achieved CC ≥ 0.992 and NSE ≥ 0.976. The Modified Kostiakov and Novel models gave the lowest RMSE (1.95 mm/h) and MAE (1.43 mm/h), followed by Philip (RMSE 2.00 mm/h) and Kostiakov (2.04 mm/h). Horton had the second-lowest training RMSE of the empirical models (1.72 mm/h, after 1.64 mm/h for Modified Kostiakov and Novel) but the highest testing RMSE (2.57 mm/h). This indicates that the three-parameter exponential form fitted the training readings well but interpolated less reliably between them, particularly in the 30–60 min range where the curve bends. The bias of all empirical models on the testing data was small (0.09–0.21 mm/h), and 93–95 % of their predictions fell within ±20 % of the observed values.

Table 3. Performance of the empirical (site-calibrated) and machine-learning (pooled) models on the training (n = 150) and testing (n = 60) data.

{TABLE3}

Among the machine-learning models, ANN performed best on the testing data (CC = 0.994, RMSE = 1.98 mm/h, MAE = 1.19 mm/h, NSE = 0.986), followed by GPR (CC = 0.994, RMSE = 2.09 mm/h, NSE = 0.984). Both had the lowest MAE of all nine models and placed 98–100 % of their testing predictions within ±20 % of the observations (Figure 3). Their RMSE was within 0.14 mm/h of the best empirical model. ANN and GPR therefore matched the accuracy of the site-calibrated empirical models, although each used one set of parameters for all 15 sites rather than a separate fit at each site. RF was clearly less accurate (RMSE = 4.33 mm/h, NSE = 0.931, 82 % within ±20 %). As Figure 3c shows, RF under-predicted the highest rates and produced several step-like over-predictions, because a forest of regression trees cannot extrapolate beyond the range of target values in a leaf and represents the smooth decline with time as a series of steps. MLR performed poorly (RMSE = 9.67 mm/h, NSE = 0.657, 27 % within ±20 %). It over-predicted rates at moderate values and under-predicted the highest rates (Figure 3a) because a linear function of time cannot reproduce the curved shape of the infiltration curve. MLR also had a systematic positive bias of 4.36 mm/h on the testing data.

The fitted MLR equation was:

f = 16.37 − 0.198 t + 2.603 Sand + 6.285 Clay − 133.8 BD − 5.769 MC + 32.78 OC          (13)

The signs of the time, bulk density, moisture and organic carbon terms are physically reasonable, but the positive clay coefficient reflects collinearity between sand and clay and should not be interpreted on its own.

Figure 3. Observed versus predicted infiltration rates on the testing data for (a) MLR, (b) ANN, (c) RF and (d) GPR. The solid line is the line of perfect agreement and the dashed lines mark ±20 % error.

[Insert Figure 3 here]

The one-way ANOVA comparing the observed testing values with the predictions of all nine models gave F = 0.388, which is well below the critical value F(9, 590) = 1.90 (p = 0.941). A second ANOVA comparing the observations with the best empirical model (Modified Kostiakov) and the best machine-learning model (ANN) gave F = 0.008 against a critical value of 3.05 (p = 0.992). Neither test showed a significant difference in mean values. As in Sihag et al. {sihag2017}, this result needs care: ANOVA tests only whether means differ, so it cannot separate good from poor models. MLR, with NSE = 0.657, also showed no significant difference.

### 3.4 Prediction at untested sites (leave-sites-out)

Table 4 and Figure 4a show the results of the leave-sites-out test. When whole sites were withheld from training, the errors of all four machine-learning models increased sharply. RF was the most transferable model, with RMSE = 11.46 mm/h, MAE = 6.85 mm/h and NSE = 0.684, which falls in the "good" range of Moriasi et al. {moriasi}. GPR (RMSE = 14.01 mm/h, NSE = 0.526) and MLR (RMSE = 15.18 mm/h, NSE = 0.445) followed. ANN, which had been the best machine-learning model under the random split, was the least transferable (RMSE = 19.03 mm/h, NSE = 0.127, bias +3.81 mm/h). The ranking of the models therefore changed completely between the two validation designs.

Table 4. Performance of the machine-learning models under five-fold leave-sites-out cross-validation (210 predictions; three sites withheld per fold), compared with the random-split testing RMSE.

{TABLE4}

The errors were concentrated at a few sites. MLR, RF and GPR all had their largest or near-largest errors at the orchard site S8 (lowest bulk density) and the sandy plain S14 (highest sand content), where they under-predicted the high rates; for RF the site RMSE was 30.6 mm/h at S8 and 17.6 mm/h at S14. These sites lie at the edge of the sampled range of soil properties, so when they were withheld the models had to extrapolate. ANN and GPR also over-predicted strongly at some sites of moderate properties. ANN predicted a peak rate of 153 mm/h at S9, where the observed initial rate was 82.3 mm/h (site RMSE 55.6 mm/h), and GPR predicted 111 mm/h at S10, where the observed initial rate was 48.1 mm/h (site RMSE 26.9 mm/h). RF predictions are averages of rates seen in training and cannot exceed the training range, so they were more conservative. This reduced the RF error at new sites even though RF was less precise within known sites. Only 27–38 % of the leave-sites-out predictions of any model fell within ±20 % of the observed values, compared with 93–95 % for the site-calibrated empirical models in the random-split test.

### 3.5 Sensitivity analysis

Figure 4b shows the testing RMSE of RF and GPR after each input was removed. Removing elapsed time increased the RMSE of RF from 4.33 to 12.18 mm/h and of GPR from 2.09 to 12.33 mm/h, so time was by far the most important input for both models. This is expected, because the infiltration rate at each site falls by a factor of four to eight over the 180-min test. Removing any one soil property changed the testing RMSE by less than 0.6 mm/h. For RF, removing an individual soil property even reduced the RMSE slightly (for example, to 3.75 mm/h without clay), and for GPR the RMSE changed by only −0.26 to +0.02 mm/h. The small effect of individual soil properties does not mean they are unimportant. In this data set each of the 15 sites has a unique combination of soil properties, so any four of the five properties are enough to identify a site, and the remaining property adds little extra information under a random split. The GPR length scales (ℓ = 1.0 for time, 1.4 for sand, 1.4 for clay, 2.8 for bulk density, 5.5 for moisture content and 11.0 for organic carbon, in standardised units) give a more informative ranking: after time, sand and clay content had the strongest influence, followed by bulk density, with moisture content and organic carbon least influential.

Figure 4. (a) RMSE of all models on the testing data and of the machine-learning models under leave-sites-out cross-validation; (b) sensitivity analysis: testing RMSE of RF and GPR after removing one input at a time (dashed lines show the RMSE with all inputs).

[Insert Figure 4 here]

## 4. Discussion

### 4.1 Empirical models remain hard to beat when a field test is available

When a measured curve is available at a site, the simple two-parameter Kostiakov and Philip models predicted withheld readings with an RMSE of about 2 mm/h, which is close to the accuracy that can be expected from double-ring readings themselves. Adding a third parameter (Modified Kostiakov, Novel, Horton) improved the fit to the training readings but gave little or no improvement on the testing readings. The three-parameter Horton model was actually the least accurate empirical model on the testing data. This agrees with the finding of Mishra et al. {mishra} that additional parameters do not guarantee better prediction. It also suggests that for the coarse soils of Hisar, where the curve is dominated by a rapid early decline, a power-law form describes the data better than an exponential decay.

The negative constant terms obtained for the Modified Kostiakov and Philip models at several sites are a practical concern for design. If such a fitted equation is extrapolated beyond the test duration, as is common when computing the intake for long irrigation set times, it will eventually predict a negative infiltration rate. Where the constant term is to be used as a steady infiltration rate, the fit should be constrained to non-negative values or the constant should be fixed at the measured final rate. The Horton fc parameter, by contrast, was always positive and close to the measured final rate, which makes Horton attractive when the steady rate itself is the quantity of interest, even though its interpolation accuracy was lower.

### 4.2 The Novel model is equivalent to the Modified Kostiakov model

Sihag et al. {sihag2017} proposed the Novel model, f = a t^-b + c ic, and reported that it outperformed the Kostiakov, Modified Kostiakov and SCS models at NIT Kurukshetra. In the Novel model, ic is the measured final rate at the site, which is a fixed number during fitting. The term c·ic is therefore a single constant, and the model has the same mathematical form as the Modified Kostiakov model, f = a t^-b + ic, in which the constant is fitted directly. When both models are fitted by least squares to the same data, they must give the same predictions, with c = ic(Modified Kostiakov)/ic(observed). This was confirmed at all 15 Hisar sites (Table 2, Table 3). The differences in performance reported in the original study are therefore most likely to be a result of differences in fitting (for example, starting values, convergence or constraints) rather than of the model form. This does not reduce the value of the earlier study's field data, but it means that the Novel model should not be treated as a separate model in future comparisons. If the aim is to link the constant to the measured steady rate, a more useful formulation is to fix the constant at the measured final rate (c = 1), which yields a two-parameter model whose constant is physically meaningful and always positive.

### 4.3 Machine-learning models: interpolation versus prediction at new sites

Under the random split, ANN and GPR matched the site-calibrated empirical models, which is consistent with earlier reports that GPR and ANN outperform the Kostiakov model for infiltration in Haryana and Iran {sihag_gpr, vand, angelaki}. The present results show, however, that this level of accuracy depends on the validation design. Under the random split, every testing reading belongs to a site whose other ten readings are in the training set, and the soil properties of each site act as a unique label for that site. A flexible model can therefore learn each site's curve almost as an empirical model would. This explains why ANN and GPR reached empirical-model accuracy and why removing individual soil properties hardly affected their performance.

When whole sites were withheld, the RMSE of the best machine-learning model rose to 11.5 mm/h, about six times the error of the site-calibrated empirical models. With only 15 sites, the models had too few examples to learn a general relationship between soil properties and the infiltration curve, especially for sites with extreme properties. Spatially structured cross-validation is therefore essential when machine-learning infiltration models are intended to replace field tests at new locations {roberts}. Studies that report only random-split accuracy are likely to overestimate the transferability of their models. The better transferability of RF compared with ANN and GPR also has a practical lesson. Because RF predictions are averages of observed values, RF cannot produce extreme or physically impossible values when it extrapolates. For a small, heterogeneous data set this conservatism is an advantage, whereas the smooth extrapolation of ANN and GPR can lead to large errors.

The relatively poor performance of RF in the random split also deserves comment. RF approximates the smooth decline of f with time by a series of steps and averages the target values in each leaf, so it tends to under-predict the highest rates and over-predict rates just after a step. Using ln(t) as an input, predicting the parameters of an empirical model instead of the rate itself, or using gradient-boosted trees could reduce this limitation.

### 4.4 Implications for the Hisar region

The soils sampled in this study have high and highly variable infiltration rates. The final rates ranged from about 3 to 25 mm/h, depending mainly on texture, bulk density and land use. Two practical points follow. First, the large reduction of the steady rate on compacted surfaces and under wet antecedent conditions means that designs based on a single district-wide infiltration function will over-estimate intake on compacted or recently irrigated fields and under-estimate it on dune soils. Second, for design and evaluation of surface irrigation at a specific field, a short double-ring test fitted with the Kostiakov or Philip model remains the most accurate and economical approach. Machine-learning models trained on the present 15 sites can be used for screening at new locations within the sampled range of soil properties, preferably with RF, but their predictions at individual new sites may be in error by around 10 mm/h, and they should not be used outside that range.

A hybrid approach could combine the strengths of both groups. A machine-learning model, or a pedotransfer function {wosten}, could be trained to predict the two Kostiakov or Philip parameters from soil properties. This would guarantee a physically shaped curve while still allowing prediction at untested sites, and it would need only one data point (the parameter set) per site rather than many readings.

### 4.5 Limitations

The study has several limitations. The number of sites (15) is small for training models that predict at new locations, and each site was tested only once, so the replicate-test variability of the double-ring method could not be separated from the spatial variability. Tests lasted 180 min, which is long enough to approach steady state on these soils but too short to assess long-term behaviour such as surface sealing. The double-ring method also over-estimates infiltration compared with flood or furrow irrigation because of residual lateral flow and the ponded head {bouwer}. The machine-learning hyper-parameters were chosen by simple trial or marginal-likelihood search, and a fuller tuning procedure might change the ranking slightly. Finally, the soil properties were measured once in the 0–15 cm layer, whereas infiltration is also affected by deeper layers, macropores and root channels that were not measured.

## 5. Conclusions

This study compared five empirical and four machine-learning models for predicting the infiltration rate of the sandy loam and loamy sand soils of Hisar district, Haryana, using 210 double-ring infiltrometer readings from 15 sites under seven land-use groups. The main conclusions are:

1. Infiltration rates differed widely between sites. Initial rates ranged from 19 to 122 mm/h and final rates from 3 to 25 mm/h. The highest rates occurred on loamy sand and under orchard and agroforestry, and the lowest on compacted and wet surfaces.

2. When calibrated with a site's own readings, all empirical models predicted withheld readings accurately (testing RMSE 1.95–2.57 mm/h, NSE ≥ 0.976). The two-parameter Kostiakov and Philip models were nearly as accurate as the three-parameter models, and the Horton model was the least accurate in testing.

3. The Novel model of Sihag et al. is mathematically equivalent to the Modified Kostiakov model and gave identical predictions at all sites. The constant terms of the Modified Kostiakov and Philip models were negative at several sites, which limits their physical interpretation and their use beyond the test duration.

4. Under a random split, ANN (RMSE 1.98 mm/h) and GPR (2.09 mm/h) matched the empirical models with a single set of parameters for all sites, RF was less accurate (4.33 mm/h) and MLR was unsuitable (9.67 mm/h).

5. At sites withheld from training, all machine-learning models lost much of their accuracy. RF transferred best (RMSE 11.46 mm/h, NSE 0.684) and ANN worst (19.03 mm/h, NSE 0.127). Random-split validation alone therefore gives an overly optimistic picture of machine-learning models for infiltration.

6. Elapsed time was the dominant input. Among the soil properties, sand and clay content and bulk density had the most influence on the GPR model.

For field-scale irrigation design in Hisar, a short double-ring test fitted with the Kostiakov or Philip model is recommended. Machine-learning models, preferably RF, can support screening at untested locations within the sampled range of soil properties. Future work should increase the number and spread of test sites, include replicate tests and seasonal repetition, and test hybrid models that predict empirical-model parameters from soil properties.

## Data Availability

The site properties, infiltration readings, training/testing split and complete model outputs are provided in the hisar_data folder (site_properties.csv, infiltration_observations.csv, infiltration_observations_split.csv and results.json). All tables and figures can be reproduced with hisar_infiltration_analysis.py and hisar_figures.py. As stated at the beginning of the manuscript, the present data are illustrative and must be replaced with field measurements before publication.

## Conflict of Interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## References

{REFERENCES}
