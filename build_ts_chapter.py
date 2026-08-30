# -*- coding: utf-8 -*-
"""
Builds the full Word chapter:
  "Time-Series Analysis for Crop Growth Monitoring"
~8300 words, 43 references (serial order), 4 tables, 4 figures (each cited twice).
No external libraries (uses ts_docx.py).
"""
import os
from ts_docx import DocxBuilder

FIG = "ts_figures"
d = DocxBuilder()

# ============================ FRONT MATTER =================================
d.subtitle("Advances in Agricultural Remote Sensing for Deltas")
d.subtitle("Part II: Intelligent Monitoring Techniques")
d.title("Chapter 7")
d.title("Time-Series Analysis for Crop Growth Monitoring")
d.spacer()

# ------------------------------- ABSTRACT (no references) ------------------
d.heading("Abstract", 1)
d.paragraph(
    "Time-series analysis has become one of the most powerful paradigms in agricultural "
    "remote sensing, transforming isolated snapshots of the land surface into continuous "
    "narratives of crop development. In deltaic regions, where intensive multiple cropping, "
    "fragmented smallholder fields, monsoonal cloud cover and recurrent hydrological extremes "
    "coexist, the temporal dimension of Earth observation is not merely useful but essential. "
    "This chapter presents a comprehensive treatment of temporal remote sensing for crop "
    "growth monitoring, beginning with the physical and phenological principles that make "
    "repeated observation informative, and progressing through the diverse data sources, "
    "vegetation indices and biophysical indicators that populate a time series. It examines "
    "the persistent challenges of cloud contamination, atmospheric perturbation, sensor "
    "inconsistency and the trade-offs among temporal, spatial and spectral resolution that "
    "shape every operational monitoring system. Building on these foundations, the chapter "
    "explores how phenological metrics are extracted from index trajectories, how curve "
    "fitting and smoothing reconstruct clean seasonal signals, and how multi-temporal "
    "signatures enable robust crop classification and yield estimation. A substantial "
    "portion is devoted to intelligent analytics, including classical machine learning, "
    "deep spatiotemporal architectures, multi-source data fusion and the automated detection "
    "of crop stress and disturbance. The discussion then turns to concrete delta applications, "
    "climate and extreme-event impact assessment, decision support for precision and "
    "sustainable agriculture, and emerging trends such as near-real-time monitoring and "
    "agricultural digital twins. Throughout, the emphasis is on how the temporal dimension, "
    "when analysed intelligently, converts vast streams of satellite, airborne and in-situ "
    "data into actionable knowledge for food security and climate resilience in the world's "
    "most vulnerable and productive landscapes.",
    spacing_after=160,
)

d.page_break()

# ========================= SECTION 1 =======================================
d.heading("Section 1: Fundamentals of Time-Series Crop Monitoring", 1)

d.heading("1.1 Principles of Temporal Remote Sensing", 2)
d.heading("Concept and importance of temporal observations in agriculture", 3)
d.paragraph(
    "Agriculture is, by its very nature, a temporal process. A single image of a field, however "
    "sharp or spectrally rich, captures only one instant in a continuous cycle of germination, "
    "growth, senescence and harvest. Temporal remote sensing exploits the fact that repeated "
    "observations of the same location reveal patterns that no single acquisition can convey. "
    "By stacking measurements acquired at intervals of days to weeks, analysts reconstruct the "
    "trajectory of a crop through its life cycle and interpret deviations from the expected "
    "pattern as evidence of stress, management action or environmental disturbance [1]. This "
    "shift from static mapping to dynamic monitoring is the conceptual heart of time-series "
    "analysis. Where early remote sensing sought to answer the question 'what is here?', "
    "temporal analysis answers the more agronomically meaningful question 'how is this changing, "
    "and why?' [2]. In deltaic agricultural systems, where two or even three crops may be grown "
    "on the same parcel within a single year, the temporal signal is often the only reliable "
    "means of distinguishing cropping practices that appear identical in any individual scene.",
)
d.paragraph(
    "The importance of temporal observation is amplified by the intensification of global "
    "agriculture and the growing demand for timely, field-scale information. National statistical "
    "surveys and periodic ground campaigns cannot match the frequency, spatial coverage or "
    "objectivity of a well-designed satellite time series [3]. Consequently, temporal remote "
    "sensing underpins operational services ranging from crop-area estimation and yield "
    "forecasting to drought early warning and insurance verification. The credibility of these "
    "services rests on the assumption that the temporal signal is both physically interpretable "
    "and consistently measured, an assumption that motivates much of the methodological "
    "discussion in later sections.",
)
d.paragraph(
    "The delta context sharpens each of these motivations. Deltas such as those of the Ganges-"
    "Brahmaputra, the Mekong, the Nile and the Irrawaddy are simultaneously among the most "
    "agriculturally productive and most physically dynamic environments on the planet, supporting "
    "dense populations that depend directly on the land for food and livelihood. Their fields are "
    "small and irregular, their cropping is intensive and rapidly changing, and their exposure to "
    "flooding, cyclones, drought and salinity intrusion is acute and increasing under a shifting "
    "climate [3]. In such settings, an annual or even seasonal snapshot is inadequate; only a "
    "dense, intelligently analysed time series can capture the pace of change and the diversity of "
    "practice that characterize delta agriculture. This chapter therefore treats the temporal "
    "dimension not as an enhancement of conventional mapping but as the organizing principle of "
    "modern agricultural monitoring in these landscapes.",
)

d.heading("Seasonal crop dynamics and phenological development", 3)
d.paragraph(
    "The observable temporal signal of a crop is a direct expression of its phenology, the timing "
    "of recurring biological events such as emergence, canopy closure, flowering, grain filling "
    "and senescence. As a crop develops, the amount and vigour of green vegetation change in a "
    "characteristic manner, producing a rise-and-fall pattern in vegetation indices that is often "
    "described as a growth curve or seasonal trajectory [4]. The greening phase reflects "
    "increasing leaf area and chlorophyll content, the plateau corresponds to peak canopy "
    "development, and the browning phase marks maturation and harvest. Because different crops "
    "reach these milestones at different times and at different rates, their trajectories differ "
    "in amplitude, timing and shape, providing a temporal fingerprint that supports both "
    "phenological interpretation and crop discrimination [5].",
)
d.paragraph(
    "In delta environments, phenological development is strongly modulated by water availability, "
    "photoperiod and temperature, all of which vary seasonally with the monsoon. Rice, the "
    "dominant delta crop, exhibits a distinctive flooding-transplanting-greening sequence that is "
    "visible even under partial cloud cover when radar observations are incorporated [6]. "
    "Understanding these seasonal dynamics is a prerequisite for interpreting any time series, "
    "because an anomaly can only be identified relative to an expected phenological baseline.",
)

d.heading("Advantages of repeated satellite and airborne observations", 3)
d.paragraph(
    "Repeated observation confers several distinct advantages. First, it enables the separation of "
    "persistent land-cover characteristics from transient conditions, so that a temporarily flooded "
    "rice paddy is not confused with a permanent water body [7]. Second, frequent revisits increase "
    "the probability of obtaining cloud-free views during critical growth windows, a decisive "
    "benefit in the humid tropics. Third, dense time series allow statistical noise to be averaged "
    "out and outliers to be detected, improving the reliability of derived products [8]. Finally, "
    "the combination of satellite constellations with airborne and unmanned platforms provides a "
    "multiscale temporal record in which coarse, frequent observations are complemented by "
    "occasional high-resolution acquisitions. Together these advantages explain why the modern "
    "monitoring community treats the time series, rather than the individual image, as the "
    "fundamental unit of analysis. The principal data sources that populate such a time series, "
    "together with their characteristic revisit interval, spatial detail and weather independence, "
    "are compared in Table 1.",
)

# ---- Figure 1 (first citation) ----
fig1 = os.path.join(FIG, "Figure_1_NDVI_Profiles.png")
d.paragraph(
    "The characteristic seasonal trajectories of the principal delta crops are illustrated in "
    "Figure 1, which contrasts the single-peak profile of a transplanted rice crop with the "
    "double-peak pattern produced by a wheat-maize rotation and the sharper profile of a "
    "single maize crop [9].",
)
d.image(fig1, "Figure 1. Idealized NDVI temporal profiles for representative delta crops, "
              "showing crop-specific timing, amplitude and shape of the seasonal growth curve.")
d.paragraph(
    "It is worth emphasising that the temporal advantage is cumulative rather than additive. A "
    "single cloud-free scene acquired at the peak of the growing season may correctly locate a "
    "field of dense vegetation, but it cannot indicate whether that vegetation is a vigorous rice "
    "crop approaching harvest or a weed-choked field that will yield little. Only the sequence of "
    "observations, read together, resolves this ambiguity, because the rate at which the canopy "
    "developed, the date on which it peaked and the manner in which it declined are collectively "
    "diagnostic of both crop type and crop condition [5]. This is why practitioners increasingly "
    "speak of the time series as a signal to be processed rather than a set of images to be "
    "interpreted individually, and why the analytical techniques of subsequent sections are framed "
    "in the language of signal reconstruction, feature extraction and sequence modelling.",
)

d.heading("1.2 Remote Sensing Data Sources for Time-Series Analysis", 2)
d.heading("Optical satellite missions and multispectral observations", 3)
d.paragraph(
    "Optical satellites remain the backbone of agricultural time-series analysis because their "
    "multispectral measurements are directly sensitive to the pigments and structure of green "
    "vegetation. Coarse-resolution sensors provide daily global coverage that captures rapid "
    "phenological change, while medium-resolution missions such as the Landsat series and the "
    "Sentinel-2 constellation deliver field-scale detail at revisit intervals of a few days to "
    "a fortnight [10]. The complementary strengths of these missions have motivated harmonized "
    "products that blend their observations into a single consistent record, dramatically "
    "increasing the density of usable optical data over any given field [11]. For delta "
    "monitoring, the red-edge bands introduced by newer missions are particularly valuable "
    "because they improve sensitivity to chlorophyll and leaf area during the dense-canopy "
    "stages when traditional indices saturate [12].",
)
d.heading("Synthetic Aperture Radar (SAR) and complementary datasets", 3)
d.paragraph(
    "Synthetic Aperture Radar is indispensable in cloud-prone delta regions because microwave "
    "signals penetrate cloud and are largely independent of solar illumination, guaranteeing "
    "observations regardless of weather [13]. SAR backscatter responds to the geometry, "
    "moisture and structure of the canopy and the underlying surface, making it especially "
    "effective for detecting the flooding and transplanting stages of rice and for tracking "
    "biomass accumulation [14]. Dual-polarization and interferometric measurements add further "
    "structural information. When combined with optical time series, SAR fills the temporal gaps "
    "left by cloud and provides an orthogonal view of crop condition, an approach examined in "
    "detail in the fusion discussion of Section 3 [15].",
)
d.heading("UAV and ground-based observations for high-resolution monitoring", 3)
d.paragraph(
    "Unmanned aerial vehicles and ground-based sensors occupy the fine end of the observational "
    "spectrum. UAVs deliver centimetre-scale imagery on demand, enabling detailed characterization "
    "of within-field variability, calibration of satellite products and rapid response to "
    "localized events [16]. Fixed field spectrometers, phenocams and networks of low-cost "
    "internet-connected soil and canopy sensors contribute continuous point observations that "
    "anchor and validate the larger-scale time series [17]. Although their spatial coverage is "
    "limited, these platforms provide the temporal density and ground truth that satellite "
    "analysis alone cannot supply, and they are increasingly integrated into operational "
    "monitoring frameworks.",
)

# ---- Table 1: data sources ----
d.table(
    "Table 1. Comparison of principal remote-sensing data sources used in agricultural "
    "time-series analysis for delta regions.",
    ["Data source", "Typical revisit", "Spatial detail", "Cloud independence", "Primary strength"],
    [
        ["Coarse optical (daily)", "Sub-daily to daily", "Coarse", "No", "High temporal density"],
        ["Medium optical (Landsat/Sentinel-2)", "5-16 days", "Field scale", "No", "Balanced detail and frequency"],
        ["SAR (C-band)", "6-12 days", "Field scale", "Yes", "All-weather observation"],
        ["UAV imagery", "On demand", "Very fine", "Partial", "Within-field variability"],
        ["Field / IoT sensors", "Continuous", "Point", "Yes", "Ground truth and calibration"],
    ],
    col_widths=[2600, 1700, 1500, 1700, 1860],
)

d.heading("1.3 Vegetation Indices and Biophysical Indicators", 2)
d.heading("NDVI, EVI, SAVI, and related vegetation indices", 3)
d.paragraph(
    "Vegetation indices distil multispectral reflectance into scalar quantities that track the "
    "abundance and vigour of green vegetation. The Normalized Difference Vegetation Index remains "
    "the most widely used because of its simplicity and long heritage, but it saturates over "
    "dense canopies and is sensitive to soil background and atmospheric effects [18]. The Enhanced "
    "Vegetation Index mitigates saturation and atmospheric influence by incorporating the blue "
    "band and a canopy-background adjustment, while the Soil-Adjusted Vegetation Index reduces the "
    "influence of exposed soil during early growth stages, a common condition in newly planted "
    "delta fields [19]. Additional indices exploiting the red edge and shortwave infrared provide "
    "complementary sensitivity to chlorophyll, water content and stress, and the choice among them "
    "is dictated by the crop, the growth stage and the sensor available [20].",
)
d.heading("Canopy cover, biomass, and chlorophyll estimation", 3)
d.paragraph(
    "Beyond simple indices, quantitative biophysical variables provide a more physically grounded "
    "description of crop state. Fractional canopy cover, leaf area index, above-ground biomass and "
    "canopy chlorophyll content can be retrieved from time series through empirical relationships "
    "or radiative-transfer inversion [21]. These variables are more directly linked to "
    "photosynthetic capacity and yield than indices alone, and their temporal evolution offers a "
    "robust basis for growth monitoring and productivity estimation. Retrieval accuracy depends on "
    "careful calibration and on the availability of ground measurements, reinforcing the role of "
    "the in-situ observations described earlier [22].",
)
d.heading("Selection of indicators for different crops and growth stages", 3)
d.paragraph(
    "No single indicator is optimal across all crops and phenological phases. Early-season "
    "monitoring, when soil dominates the signal, benefits from soil-adjusted formulations; the "
    "dense-canopy period requires indices that resist saturation; and stress detection may demand "
    "specialized water or pigment indices [23]. Effective time-series analysis therefore selects "
    "indicators purposefully, often combining several into a multivariate feature set that is "
    "later exploited by the machine-learning methods discussed in Section 3. This deliberate "
    "matching of indicator to purpose is one of the practical hallmarks of a well-designed "
    "monitoring system.",
)

d.heading("1.4 Challenges in Agricultural Time-Series Data", 2)
d.heading("Cloud contamination and missing observations", 3)
d.paragraph(
    "The single greatest obstacle to optical time-series analysis in delta regions is cloud. "
    "During the monsoon, weeks may pass without a usable optical observation, leaving critical "
    "growth stages unrecorded and producing irregular, gap-riddled time series [24]. Cloud "
    "shadow and thin cirrus further contaminate apparently clear pixels, introducing spurious "
    "drops in vegetation indices that can be mistaken for stress. Robust cloud masking, gap "
    "filling and reconstruction are therefore not optional refinements but core components of "
    "any operational pipeline, as reflected in Figure 2 [25].",
)
d.heading("Atmospheric effects and sensor inconsistencies", 3)
d.paragraph(
    "Even under clear skies, the atmosphere scatters and absorbs radiation, altering measured "
    "reflectance in ways that vary with aerosol load, water vapour and viewing geometry [26]. "
    "Rigorous atmospheric correction is essential to produce surface reflectance that is "
    "comparable across dates. Compounding this, time series assembled from multiple sensors "
    "inherit differences in spectral response, calibration and spatial sampling, which must be "
    "reconciled through cross-calibration and harmonization before the data can be interpreted "
    "as a single coherent record [27].",
)
d.heading("Temporal resolution, spatial resolution, and data harmonization", 3)
d.paragraph(
    "A fundamental tension pervades sensor design: high spatial detail, frequent revisit and broad "
    "coverage cannot all be maximized simultaneously, as the source comparison in Table 1 makes "
    "clear. Coarse sensors observe often but blur "
    "smallholder fields, whereas fine sensors resolve individual parcels but revisit infrequently "
    "[28]. Delta agriculture, characterized by tiny, heterogeneous fields and rapid phenological "
    "change, sits precisely where this trade-off bites hardest. Data harmonization and fusion, "
    "which blend the temporal richness of coarse sensors with the spatial precision of fine ones, "
    "are the principal strategies for resolving this tension and are treated at length in "
    "Section 3 [29].",
)

# ---- Figure 2 (first citation) ----
fig2 = os.path.join(FIG, "Figure_2_Curve_Fitting.png")
d.paragraph(
    "The combined impact of these challenges is visible in Figure 2, where raw cloud-affected "
    "observations scatter widely below the true seasonal signal and a fitted trajectory is "
    "required to recover an interpretable growth curve [30].",
)
d.image(fig2, "Figure 2. Curve fitting and gap filling applied to a noisy, cloud-affected NDVI "
              "series, illustrating the reconstruction of a smooth seasonal trajectory from "
              "irregular observations.")

d.page_break()

# ========================= SECTION 2 =======================================
d.heading("Section 2: Crop Phenology and Growth Dynamics", 1)

d.heading("2.1 Detection of Crop Growth Stages", 2)
d.heading("Emergence, vegetative growth, flowering, and maturity", 3)
d.paragraph(
    "The detection of discrete growth stages from a continuous time series translates a smooth "
    "curve into agronomically meaningful events. Emergence corresponds to the initial departure "
    "of the vegetation index from its bare-soil baseline; the vegetative phase is marked by rapid "
    "greening; flowering typically coincides with or shortly follows the seasonal maximum; and "
    "maturity is signalled by the onset of senescence and the decline toward harvest [31]. "
    "Accurate identification of these stages allows monitoring systems to time interventions, "
    "assess development relative to the expected calendar and flag crops that are advancing "
    "unusually quickly or slowly.",
)
d.heading("Phenological metrics derived from vegetation-index curves", 3)
d.paragraph(
    "A rich set of phenological metrics can be derived from a fitted index curve, as summarized in "
    "Table 2, including the "
    "start, peak and end of the growing season, the length of the season, the maximum index "
    "value, the rate of greening and the integrated index over the season, which serves as a "
    "proxy for cumulative productivity [32]. These metrics compress the temporal signal into a "
    "compact, interpretable feature vector that is highly informative for both classification and "
    "yield estimation. Their reliability depends critically on the quality of the underlying curve "
    "fitting, underscoring the importance of the smoothing methods discussed below.",
)
d.heading("Identification of crop-specific growth patterns", 3)
d.paragraph(
    "Because each crop possesses a characteristic phenological signature, the pattern of "
    "derived metrics can itself identify the crop. Rice, wheat, maize and jute, for example, "
    "differ systematically in season length, greening rate and the presence or absence of an "
    "early flooding signal [33]. Recognizing these crop-specific patterns is the conceptual "
    "bridge between phenological analysis and the classification methods of Section 2.3, and it "
    "is especially powerful in delta systems where multiple crops share the same landscape.",
)

d.heading("2.2 Time-Series Curve Fitting and Smoothing", 2)
d.heading("Moving averages and noise-reduction techniques", 3)
d.paragraph(
    "The simplest approach to noise reduction is the moving average, which replaces each "
    "observation with a local mean and thereby suppresses high-frequency fluctuations [34]. "
    "Weighted and adaptive variants, together with median filters that resist outliers, offer "
    "improved performance when cloud-induced drops are present. While computationally trivial, "
    "these techniques can blur genuine phenological transitions if applied too aggressively, so "
    "the window size must be chosen with care relative to the temporal sampling and the sharpness "
    "of the crop's development.",
)
d.heading("Polynomial, spline, and harmonic fitting methods", 3)
d.paragraph(
    "More sophisticated smoothing fits an explicit functional form to the time series. Piecewise "
    "polynomial and spline fits provide flexible local approximations, asymmetric logistic "
    "functions capture the sigmoidal greening and senescence phases, and harmonic (Fourier) "
    "models represent the seasonal cycle as a sum of sinusoids well suited to long, multi-year "
    "records [35]. The Savitzky-Golay filter, which fits successive local polynomials, is "
    "particularly popular because it preserves the shape and timing of phenological features "
    "while removing noise [36]. The appropriate method depends on the density and regularity of "
    "the observations and on whether the objective is per-season metric extraction or long-term "
    "trend analysis.",
)
d.heading("Extraction of seasonal growth trajectories", 3)
d.paragraph(
    "The product of curve fitting is a clean seasonal trajectory from which phenological metrics "
    "and biophysical proxies are read. As illustrated earlier in Figure 2, the fitted curve "
    "bridges cloud gaps and rejects contaminated observations, yielding a continuous signal "
    "suitable for downstream analysis [37]. In delta regions with two or three cropping cycles "
    "per year, the fitting procedure must be capable of resolving multiple distinct peaks within a "
    "single annual record, a requirement that favours flexible local methods over rigid global "
    "models.",
)

d.heading("2.3 Crop Classification Using Temporal Signatures", 2)
d.heading("Phenology-based crop identification", 3)
d.paragraph(
    "Phenology-based classification assigns crop types on the basis of the shape and timing of "
    "their temporal signatures rather than the spectral values of any single date [38]. Because "
    "the temporal pattern is far more distinctive than instantaneous reflectance, this approach "
    "dramatically reduces the confusion that plagues single-date classification, particularly "
    "among spectrally similar crops. Simple rule-based schemes keyed to characteristic events, "
    "such as the flooding signal of rice, can be remarkably effective and transparent.",
)
d.heading("Multi-temporal classification approaches", 3)
d.paragraph(
    "More general approaches treat the entire stacked time series, or a set of derived phenological "
    "and statistical features, as the input to a classifier [39]. Multi-temporal classification "
    "leverages the full seasonal record and naturally accommodates the fusion of optical and radar "
    "observations. The dimensionality of a dense time series, however, demands careful feature "
    "engineering or dimensionality reduction to avoid overfitting, a concern that motivates the "
    "learned feature extraction of deep models discussed in Section 3.",
)
d.heading("Machine-learning methods for crop-type discrimination", 3)
d.paragraph(
    "Supervised machine-learning classifiers, notably random forests and support vector machines, "
    "have become the workhorses of temporal crop mapping because they handle high-dimensional, "
    "non-linear feature spaces and provide measures of feature importance [40]. Their accuracy "
    "depends on representative training data and on the informativeness of the temporal features "
    "supplied. Reported accuracies for these and more advanced methods are summarized in Figure 3, "
    "which shows a consistent improvement as models become better able to exploit temporal "
    "structure [41].",
)

# ---- Figure 3 (first citation) ----
fig3 = os.path.join(FIG, "Figure_3_Accuracy_Bars.png")
d.image(fig3, "Figure 3. Representative overall accuracies reported for temporal crop-classification "
              "methods, illustrating the general improvement from classical machine learning toward "
              "deep and attention-based architectures.")

# ---- Table 2: phenological metrics ----
d.table(
    "Table 2. Common phenological metrics derived from a fitted vegetation-index time series and "
    "their agronomic interpretation.",
    ["Metric", "Definition", "Agronomic interpretation"],
    [
        ["Start of season", "Onset of sustained greening", "Planting / emergence timing"],
        ["Peak value", "Maximum index of the season", "Maximum canopy vigour"],
        ["Time of peak", "Date of the seasonal maximum", "Approx. flowering / heading"],
        ["Length of season", "Duration from start to end", "Crop cycle length"],
        ["Rate of greening", "Slope of the rising limb", "Vigour of vegetative growth"],
        ["Seasonal integral", "Area under the curve", "Cumulative productivity proxy"],
    ],
    col_widths=[2200, 3400, 3760],
)

d.paragraph(
    "A further practical consideration in delta classification is the treatment of mixed and "
    "transitional pixels. Because delta fields are frequently smaller than the ground sampling "
    "distance of medium-resolution sensors, a single pixel may straddle two crops, a field "
    "boundary or the interface between cropland and water. Such mixed pixels blur the temporal "
    "signature and can bias both classification and area estimation. Strategies to mitigate this "
    "include the use of finer-resolution imagery where available, sub-pixel unmixing that "
    "decomposes the observed signal into component fractions, and object-based analysis that "
    "aggregates pixels into homogeneous field objects before extracting temporal features [38]. "
    "The choice among these strategies depends on the sensor, the landscape and the accuracy "
    "requirements of the intended product, and it is a decision that materially affects the "
    "credibility of downstream statistics.",
)

d.heading("2.4 Crop Growth and Yield Estimation", 2)
d.heading("Linking temporal remote-sensing indicators with biomass", 3)
d.paragraph(
    "The temporal accumulation of a vegetation index over the growing season is closely related to "
    "the amount of photosynthetically active radiation intercepted by the canopy, and hence to the "
    "biomass produced [42]. This physical link, formalized in light-use-efficiency frameworks, "
    "underpins the use of the seasonal integral and related metrics as predictors of biomass and, "
    "ultimately, yield. The strength of the relationship depends on the crop, the growth stage and "
    "the environmental limitations on productivity, so calibration against field measurements "
    "remains essential.",
)
d.heading("Estimation of crop productivity and yield", 3)
d.paragraph(
    "Yield estimation models range from simple empirical regressions between seasonal metrics and "
    "measured yield to sophisticated schemes that assimilate remote-sensing observations into "
    "process-based crop growth models [43]. Empirical approaches are transparent and easily "
    "operationalized but may not transfer well across regions or seasons, whereas assimilation "
    "approaches are more physically consistent but demand greater data and computational "
    "resources. In practice, hybrid strategies that constrain a crop model with remotely sensed "
    "phenology and biophysical variables offer an attractive balance for delta applications.",
)
d.heading("Early-season yield forecasting and uncertainty assessment", 3)
d.paragraph(
    "Forecasting yield before harvest is among the most valuable products of time-series analysis, "
    "informing markets, food-security planning and policy. Early-season forecasts rely on the "
    "partial trajectory observed to date, extrapolated using climatological expectations and "
    "historical relationships. Because such forecasts are inherently uncertain, rigorous "
    "quantification of confidence, propagating errors from observation, retrieval and model, is "
    "indispensable for responsible decision-making. As the season progresses and the observed "
    "trajectory lengthens, forecast uncertainty narrows, a behaviour that operational systems "
    "communicate explicitly to their users.",
)

d.page_break()

# ========================= SECTION 3 =======================================
d.heading("Section 3: Intelligent Time-Series Analytics for Delta Agriculture", 1)

d.heading("3.1 Machine Learning for Temporal Crop Monitoring", 2)
d.heading("Random forests, support vector machines, and ensemble learning", 3)
d.paragraph(
    "Classical machine learning transformed temporal crop monitoring by providing flexible, "
    "data-driven mappings from feature vectors to crop type, condition or yield. Random forests "
    "aggregate many decision trees to achieve robust, high-accuracy classification while resisting "
    "overfitting and offering interpretable measures of feature importance. Support vector "
    "machines construct optimal separating boundaries in high-dimensional feature spaces and "
    "perform well even with modest training samples. Ensemble strategies, including gradient "
    "boosting and stacking, combine multiple learners to squeeze additional performance from the "
    "temporal features. These methods, whose comparative accuracies appear in Figure 3, remain "
    "the pragmatic default for many operational systems because they are efficient, well "
    "understood and readily deployed.",
)
d.heading("Feature extraction from multi-date imagery", 3)
d.paragraph(
    "The performance of classical learners hinges on the features presented to them. Effective "
    "feature extraction condenses a dense, noisy time series into a compact set of informative "
    "descriptors, typically combining phenological metrics, statistical summaries such as means "
    "and variances, spectral indices at key dates and textural or contextual measures. Thoughtful "
    "feature engineering both reduces dimensionality and injects domain knowledge, often "
    "yielding accuracy comparable to more complex models at a fraction of the computational cost. "
    "This step is where agronomic understanding and statistical learning meet most directly.",
)
d.heading("Automated detection of crop growth anomalies", 3)
d.paragraph(
    "Machine learning also enables the automatic detection of anomalies, deviations of an observed "
    "trajectory from its expected phenological baseline. By learning the normal range of behaviour "
    "for a crop and region, models can flag fields that are greening too slowly, senescing "
    "prematurely or otherwise departing from the norm. Such anomalies frequently signal water "
    "stress, nutrient deficiency, pest infestation or damage from extreme events, and their timely "
    "detection is the foundation of the early-warning systems discussed in Section 3.4.",
)
d.paragraph(
    "A recurring practical question is how much labelled training data these methods require. "
    "Classical learners such as random forests and support vector machines are attractive in "
    "data-scarce delta settings precisely because they perform respectably with a few hundred "
    "well-distributed field samples, provided the temporal features are informative. Where field "
    "reference data are especially limited, transfer of knowledge from data-rich regions or "
    "seasons, together with careful stratification of the available samples across crop types and "
    "management practices, can substantially improve generalization [40]. The interpretability of "
    "these models is a further operational asset: feature-importance rankings reveal which dates "
    "and indices drive a classification, allowing analysts to sanity-check results against "
    "agronomic expectation and to detect subtle problems such as mislabelled training polygons or "
    "residual cloud contamination.",
)

d.heading("3.2 Deep Learning and Spatiotemporal Modeling", 2)
d.heading("Convolutional neural networks for temporal imagery", 3)
d.paragraph(
    "Deep learning has reshaped temporal crop analysis by learning features directly from data "
    "rather than relying on hand-crafted descriptors. Convolutional neural networks excel at "
    "capturing spatial patterns and textures within imagery, and when applied across a temporal "
    "stack, they extract spatiotemporal features that encode both the appearance of a field and "
    "its evolution. One-dimensional convolutions applied along the time axis are particularly "
    "effective at recognizing characteristic phenological shapes, providing a powerful alternative "
    "to explicit metric extraction.",
)
d.heading("Recurrent neural networks and Long Short-Term Memory models", 3)
d.paragraph(
    "Recurrent architectures are designed explicitly for sequential data and are therefore natural "
    "candidates for time-series analysis. Long Short-Term Memory networks maintain an internal "
    "memory that captures long-range temporal dependencies while mitigating the vanishing-gradient "
    "problem that afflicts simple recurrent networks. Applied to crop time series, they learn the "
    "ordered progression of growth stages and achieve strong classification and forecasting "
    "performance, especially when observations are irregularly spaced, as is typical under cloudy "
    "delta skies. Their advantage over classical learners is most pronounced when the temporal "
    "ordering of observations carries decisive information.",
)
d.heading("Transformer-based approaches for long-term crop monitoring", 3)
d.paragraph(
    "Transformer architectures, built on self-attention, have recently achieved state-of-the-art "
    "results in sequence modelling and are increasingly applied to satellite time series. By "
    "attending to all observations simultaneously, they capture long-range dependencies and "
    "assign importance to the most informative dates without the sequential bottleneck of "
    "recurrent models. Attention weights also offer a degree of interpretability, revealing which "
    "acquisitions drive a given decision. As indicated in Figure 3, attention-based models often "
    "achieve the highest reported accuracies, though at the cost of greater data and computational "
    "demands that must be weighed against operational constraints.",
)

d.paragraph(
    "The choice between classical and deep approaches is ultimately governed by the operational "
    "context rather than by accuracy alone. Deep architectures reward abundant training data and "
    "computational resources with superior accuracy and the ability to learn features that human "
    "analysts might overlook, but they can be opaque and data-hungry in ways that ill suit "
    "under-resourced monitoring programmes. Classical learners, conversely, offer transparency, "
    "modest data requirements and rapid deployment at some cost in peak performance [41]. Many "
    "successful delta monitoring systems therefore adopt a pragmatic middle path, using deep models "
    "to distil rich features or to handle the most difficult discrimination tasks while relying on "
    "interpretable classical learners for routine, auditable production. The comparative accuracies "
    "of Figure 3 should thus be read alongside the practical trade-offs summarized in Table 3 rather "
    "than as a simple ranking of methods.",
)

d.heading("3.3 Data Fusion for Continuous Crop Monitoring", 2)
d.heading("Integration of optical and SAR observations", 3)
d.paragraph(
    "The complementary nature of optical and radar observations makes their fusion one of the most "
    "productive strategies in delta monitoring. Optical data provide direct information on pigments "
    "and canopy state but are blocked by cloud, whereas radar guarantees observation regardless of "
    "weather but is harder to interpret physiologically. By combining the two, analysts obtain a "
    "denser, more reliable time series in which radar fills the gaps left by cloud and reinforces "
    "the optical signal during clear periods. This integration, depicted in Figure 4, is now "
    "standard practice in operational rice-monitoring systems.",
)
d.heading("Fusion of satellite, UAV, and field sensor data", 3)
d.paragraph(
    "Fusion extends beyond satellite platforms to embrace the full observational hierarchy. UAV "
    "imagery calibrates and downscales satellite products, field and internet-connected sensors "
    "supply continuous ground truth, and satellite constellations provide synoptic coverage. "
    "Multiscale fusion reconciles these heterogeneous streams into a coherent picture that is "
    "simultaneously detailed, frequent and broad in coverage. The resulting product supports "
    "field-scale decisions while retaining the regional context essential for planning, and it "
    "exemplifies the end-to-end pipeline summarized in Figure 4.",
)
d.paragraph(
    "The practical design of a fusion pipeline involves several consequential choices. Fusion may "
    "be performed at the level of raw or corrected observations, at the level of derived features "
    "such as indices and phenological metrics, or at the level of decisions, where separate "
    "classifiers trained on each data source are combined. Feature-level and decision-level fusion "
    "are often more robust to the differing physical meanings of optical and radar measurements, "
    "whereas observation-level fusion can maximize temporal density when the sources are carefully "
    "harmonized. Regardless of the level chosen, rigorous geometric co-registration and consistent "
    "temporal referencing are prerequisites, because even small misalignments between sources "
    "propagate into spurious anomalies. The workflow of Figure 4 therefore places preprocessing "
    "and harmonization deliberately upstream of the fusion and modelling stages.",
)
d.heading("Filling temporal gaps through data assimilation and reconstruction", 3)
d.paragraph(
    "Where observations are missing, gap filling and data assimilation reconstruct the continuous "
    "signal. Statistical reconstruction interpolates across gaps using temporal and spatial "
    "correlations, while data assimilation blends observations with the predictions of a crop "
    "growth model, producing an estimate that is consistent with both the data and the underlying "
    "physiology. Assimilation is especially valuable in delta regions, where long cloudy periods "
    "would otherwise leave critical stages unobserved, and it forms the analytical core of the "
    "continuous-monitoring workflow.",
)

# ---- Figure 4 (first citation) ----
fig4 = os.path.join(FIG, "Figure_4_Fusion_Workflow.png")
d.image(fig4, "Figure 4. End-to-end multi-source data-fusion workflow integrating optical, SAR, "
              "UAV and in-situ observations through preprocessing, assimilation and machine-learning "
              "fusion to generate crop maps, yield forecasts and stress alerts.")

# ---- Table 3: analytical methods ----
d.table(
    "Table 3. Summary of analytical methods for intelligent time-series crop monitoring, with "
    "characteristic strengths and limitations.",
    ["Method family", "Key strength", "Principal limitation"],
    [
        ["Random forest / SVM", "Robust, interpretable, low data need", "Relies on hand-crafted features"],
        ["1D / spatiotemporal CNN", "Learns features automatically", "Needs larger training sets"],
        ["LSTM / recurrent", "Models temporal ordering", "Sequential, slower to train"],
        ["Transformer / attention", "Captures long-range dependencies", "High data and compute demand"],
        ["Data assimilation", "Physically consistent estimates", "Model and parameter complexity"],
    ],
    col_widths=[2600, 3400, 3360],
)

d.heading("3.4 AI-Based Detection of Crop Stress and Disturbances", 2)
d.heading("Detection of drought, flooding, salinity, and nutrient stress", 3)
d.paragraph(
    "Delta agriculture is exposed to a distinctive suite of stressors, and time-series analysis "
    "provides an effective means of detecting each. Drought manifests as suppressed greening and "
    "premature senescence; flooding, a frequent hazard in low-lying deltas, produces abrupt "
    "collapses in the vegetation signal detectable especially by radar; salinity intrusion, "
    "aggravated by sea-level rise and reduced freshwater flow, causes chronic depression of crop "
    "vigour; and nutrient deficiency alters the trajectory in subtler, pigment-related ways. "
    "Artificial-intelligence models trained to recognize these characteristic temporal signatures "
    "can distinguish among stressors and estimate their severity, transforming raw observations "
    "into diagnostic information.",
)
d.heading("Monitoring pest and disease-related vegetation changes", 3)
d.paragraph(
    "Pests and diseases induce changes in canopy structure and pigment content that, while often "
    "subtle at first, produce detectable deviations in a well-characterized time series. "
    "Red-edge and shortwave-infrared indices are particularly sensitive to the early physiological "
    "effects of infestation, and machine-learning models can learn to associate specific temporal "
    "and spectral patterns with particular pests or pathogens. Early detection enables targeted "
    "intervention that limits both crop loss and the environmental burden of blanket pesticide "
    "application.",
)
d.heading("Early warning systems for agricultural disturbances", 3)
d.paragraph(
    "The culmination of stress detection is the operational early-warning system, which "
    "continuously ingests observations, compares them against expected baselines and issues alerts "
    "when significant deviations arise. Such systems integrate the anomaly-detection, "
    "classification and fusion capabilities described throughout this section, delivering "
    "actionable warnings to farmers, extension services and policymakers. In deltaic regions "
    "prone to floods, cyclones and salinity intrusion, timely warning can be the difference "
    "between manageable loss and catastrophic failure, making early-warning systems a central "
    "objective of intelligent monitoring.",
)

d.page_break()

# ========================= SECTION 4 =======================================
d.heading("Section 4: Applications and Future Directions in Delta Regions", 1)

d.heading("4.1 Time-Series Monitoring of Delta Cropping Systems", 2)
d.heading("Rice, wheat, maize, and diversified cropping systems", 3)
d.paragraph(
    "Delta cropping systems are among the most intensive and diverse on Earth, and time-series "
    "monitoring is uniquely suited to characterizing them. Rice dominates most tropical deltas and "
    "presents a distinctive flooding-greening signature that is readily tracked by combined "
    "optical and radar observation, as illustrated in Figure 1. Wheat and maize, often grown in "
    "rotation with rice during the dry season, add further peaks to the annual trajectory, while "
    "diversified systems incorporating pulses, oilseeds and vegetables create complex mosaics that "
    "only dense temporal analysis can disentangle. Mapping these systems accurately is the "
    "foundation for all downstream agricultural intelligence in the delta.",
)
d.heading("Monitoring crop calendars and multiple cropping patterns", 3)
d.paragraph(
    "Beyond identifying crops, time-series analysis reconstructs the crop calendar, the sequence "
    "and timing of planting and harvest across the year. In deltas where double and triple "
    "cropping are common, detecting the number of cropping cycles and their phasing is essential "
    "for estimating cropping intensity and land productivity. The multi-peak trajectories that "
    "encode these patterns, of the kind shown in Figure 1, are resolved through the flexible "
    "curve-fitting and phenological-analysis methods of Section 2, and they reveal shifts in "
    "cropping practice driven by markets, water availability and policy.",
)
d.heading("Assessment of seasonal and interannual agricultural variability", 3)
d.paragraph(
    "Long-term archives allow analysts to characterize not only the average behaviour of a "
    "cropping system but also its variability from season to season and year to year. Comparing "
    "the trajectory of a given year against the historical envelope identifies anomalous seasons, "
    "quantifies the impact of climatic fluctuations and reveals gradual trends such as expanding "
    "or contracting cultivated area. This capacity to place the current season in historical "
    "context is indispensable for food-security assessment and for detecting the slow signatures "
    "of environmental change in the delta.",
)

d.heading("4.2 Climate and Extreme-Event Impact Assessment", 2)
d.heading("Crop responses to floods, cyclones, droughts, and heatwaves", 3)
d.paragraph(
    "Deltas are exceptionally vulnerable to climatic extremes, and time-series analysis provides a "
    "direct means of measuring their agricultural impact. Floods and cyclones produce abrupt, "
    "localized collapses in the vegetation signal that radar can detect even through storm cloud; "
    "droughts and heatwaves generate more gradual, spatially extensive suppression of greening. "
    "By comparing observed trajectories against expected baselines, analysts quantify the extent "
    "and severity of damage rapidly after an event, supporting emergency response and the "
    "administration of relief and insurance. These and the other principal delta applications, "
    "together with the temporal information each exploits and the decisions it supports, are "
    "summarized in Table 4.",
)
d.heading("Long-term assessment of climate-driven productivity changes", 3)
d.paragraph(
    "Multi-decadal time series enable the detection of slow, climate-driven changes in "
    "agricultural productivity that are invisible at shorter timescales. Trends in seasonal "
    "metrics, shifts in the timing of phenological events and gradual changes in maximum canopy "
    "vigour can be attributed to warming, altered precipitation and, in coastal deltas, advancing "
    "salinity. Such long-term assessment informs adaptation planning and provides an evidence base "
    "for climate policy, translating abstract projections into observed agricultural consequences.",
)
d.heading("Recovery monitoring following extreme events", 3)
d.paragraph(
    "The value of time-series analysis extends beyond immediate damage assessment to the "
    "monitoring of recovery. By tracking the return of the vegetation signal toward its normal "
    "trajectory after a flood, cyclone or drought, analysts gauge the resilience of the cropping "
    "system and the effectiveness of rehabilitation efforts. Slow or incomplete recovery may "
    "signal lasting damage such as soil salinization or infrastructure loss, guiding the "
    "allocation of recovery resources and informing longer-term adaptation strategies.",
)

# ---- Table 4: applications ----
d.table(
    "Table 4. Representative applications of time-series remote sensing in delta agriculture and "
    "the decisions they support.",
    ["Application", "Temporal information used", "Decision supported"],
    [
        ["Crop-type mapping", "Full seasonal signature", "Area statistics, planning"],
        ["Crop-calendar monitoring", "Timing of season stages", "Cropping-intensity assessment"],
        ["Yield forecasting", "Seasonal integral and metrics", "Markets, food-security policy"],
        ["Flood / cyclone damage", "Abrupt signal collapse", "Emergency response, relief"],
        ["Drought / salinity stress", "Trajectory suppression", "Irrigation, adaptation planning"],
        ["Recovery monitoring", "Return toward baseline", "Rehabilitation resourcing"],
    ],
    col_widths=[2600, 3400, 3360],
)

d.heading("4.3 Decision Support for Precision and Sustainable Agriculture", 2)
d.heading("Irrigation and fertilizer management using temporal indicators", 3)
d.paragraph(
    "Building on the application overview of Table 4, time-series indicators feed directly into "
    "precision-management decisions. Temporal patterns "
    "of vegetation and water indices reveal spatial and temporal variation in crop water status, "
    "guiding the timing and volume of irrigation, while chlorophyll-sensitive indices inform "
    "nitrogen management by highlighting areas of deficiency. Delivered through farm-management "
    "platforms, this information enables inputs to be applied where and when they are most needed, "
    "improving both productivity and resource-use efficiency, a dual benefit of particular "
    "importance in water-stressed and salinity-affected deltas.",
)
d.heading("Crop health-based intervention strategies", 3)
d.paragraph(
    "The anomaly-detection and stress-diagnosis capabilities described earlier translate naturally "
    "into intervention strategies. When a monitoring system identifies an area of declining "
    "health, it can trigger targeted scouting, treatment or adjustment of management, containing "
    "problems before they spread. This reactive, health-based approach complements routine "
    "management and embodies the shift from calendar-based to condition-based agriculture that "
    "intelligent time-series analysis makes possible.",
)
d.heading("Integration of remote sensing with farm management systems", 3)
d.paragraph(
    "The practical value of time-series analysis is realized only when its products are embedded "
    "in the systems that farmers and advisors actually use. Integration with farm-management "
    "information systems delivers maps, alerts and recommendations through accessible interfaces, "
    "often on mobile devices suited to smallholder contexts. Seamless integration lowers the "
    "barrier to adoption and ensures that the sophisticated analytics described in this chapter "
    "produce tangible improvements in field-level decision-making rather than remaining confined "
    "to research settings.",
)
d.paragraph(
    "Sustainability considerations increasingly shape how these decision-support products are "
    "designed and evaluated. Temporal monitoring not only improves yields but also provides the "
    "evidence needed to reduce the environmental footprint of agriculture, by documenting where "
    "fertilizer and water are being applied inefficiently, by verifying the adoption of "
    "conservation practices and by quantifying the implications of different cropping choices. In "
    "deltas, where agriculture, aquaculture and fragile coastal ecosystems are tightly interwoven, "
    "this capacity to monitor sustainability at scale is becoming as important as the traditional "
    "objectives of production and food security, and it aligns the technical agenda of time-series "
    "analysis with broader societal goals.",
)

d.heading("4.4 Emerging Trends in Time-Series Agricultural Remote Sensing", 2)
d.heading("Near-real-time and automated crop monitoring", 3)
d.paragraph(
    "The trajectory of the field is toward ever more timely and automated monitoring. Growing "
    "satellite constellations, expanding cloud-computing platforms and increasingly automated "
    "processing chains are compressing the interval between observation and actionable information "
    "from weeks to days or hours. Near-real-time monitoring enables genuinely responsive "
    "agriculture, in which management adapts continuously to observed conditions, and it is rapidly "
    "becoming the expectation rather than the exception for operational services.",
)
d.heading("Digital twins and AI-enabled agricultural intelligence", 3)
d.paragraph(
    "A particularly promising development is the agricultural digital twin, a continuously updated "
    "virtual representation of a field or region that fuses remote-sensing time series, process "
    "models and in-situ data. By assimilating observations in real time, a digital twin can "
    "simulate crop development, test management scenarios and forecast outcomes, providing a "
    "powerful platform for decision support. Coupled with advances in artificial intelligence, "
    "digital twins represent a convergence of the observational, analytical and modelling threads "
    "developed throughout this chapter into a unified system of agricultural intelligence.",
)
d.heading("Future opportunities for climate-resilient and sustainable delta agriculture", 3)
d.paragraph(
    "Looking ahead, the intelligent analysis of agricultural time series offers profound "
    "opportunities for building climate-resilient and sustainable delta agriculture. Continuous, "
    "field-scale monitoring can guide the efficient use of scarce water and nutrients, provide "
    "early warning of the extremes to which deltas are increasingly exposed, and supply the "
    "evidence base for adaptation and policy. Realizing this potential will require sustained "
    "investment in data infrastructure, in the harmonization and fusion of heterogeneous "
    "observations, and in the human capacity to interpret and act upon the resulting knowledge. "
    "Overall, the transition toward intelligent, time-series-driven agricultural monitoring "
    "requires a balanced approach in which technological capability, data infrastructure, "
    "institutional capacity, ethical governance and stakeholder acceptance develop together, so "
    "that these tools become genuine enablers of food security, environmental stewardship and "
    "human development in the world's deltas rather than merely another layer of technological "
    "automation.",
    spacing_after=200,
)

d.page_break()

# ========================= REFERENCES ======================================
d.heading("References", 1)

refs = [
    "Reed, B. C., Brown, J. F., VanderZee, D., Loveland, T. R., Merchant, J. W., & Ohlen, D. O. (1994). Measuring phenological variability from satellite imagery. Journal of Vegetation Science, 5(5), 703-714.",
    "Lambin, E. F., & Strahler, A. H. (1994). Change-vector analysis in multitemporal space: a tool to detect and categorize land-cover change processes. Remote Sensing of Environment, 48(2), 231-244.",
    "Atzberger, C. (2013). Advances in remote sensing of agriculture: context description, existing operational monitoring systems and major information needs. Remote Sensing, 5(2), 949-981.",
    "Zhang, X., Friedl, M. A., Schaaf, C. B., et al. (2003). Monitoring vegetation phenology using MODIS. Remote Sensing of Environment, 84(3), 471-475.",
    "Wardlow, B. D., Egbert, S. L., & Kastens, J. H. (2007). Analysis of time-series MODIS 250 m vegetation index data for crop classification in the U.S. Central Great Plains. Remote Sensing of Environment, 108(3), 290-310.",
    "Bouvet, A., & Le Toan, T. (2011). Use of ENVISAT/ASAR wide-swath data for timely rice fields mapping in the Mekong River Delta. Remote Sensing of Environment, 115(4), 1090-1101.",
    "Xiao, X., Boles, S., Liu, J., et al. (2005). Mapping paddy rice agriculture in southern China using multi-temporal MODIS images. Remote Sensing of Environment, 95(4), 480-492.",
    "Jonsson, P., & Eklundh, L. (2004). TIMESAT - a program for analyzing time-series of satellite sensor data. Computers & Geosciences, 30(8), 833-845.",
    "Sakamoto, T., Yokozawa, M., Toritani, H., et al. (2005). A crop phenology detection method using time-series MODIS data. Remote Sensing of Environment, 96(3-4), 366-374.",
    "Wulder, M. A., Loveland, T. R., Roy, D. P., et al. (2019). Current status of Landsat program, science, and applications. Remote Sensing of Environment, 225, 127-147.",
    "Claverie, M., Ju, J., Masek, J. G., et al. (2018). The Harmonized Landsat and Sentinel-2 surface reflectance data set. Remote Sensing of Environment, 219, 145-161.",
    "Drusch, M., Del Bello, U., Carlier, S., et al. (2012). Sentinel-2: ESA's optical high-resolution mission for GMES operational services. Remote Sensing of Environment, 120, 25-36.",
    "Torres, R., Snoeij, P., Geudtner, D., et al. (2012). GMES Sentinel-1 mission. Remote Sensing of Environment, 120, 9-24.",
    "Nguyen, D. B., Gruber, A., & Wagner, W. (2016). Mapping rice extent and cropping scheme in the Mekong Delta using Sentinel-1A data. Remote Sensing Letters, 7(12), 1209-1218.",
    "Veloso, A., Mermoz, S., Bouvet, A., et al. (2017). Understanding the temporal behavior of crops using Sentinel-1 and Sentinel-2-like data for agricultural applications. Remote Sensing of Environment, 199, 415-426.",
    "Zhang, C., Kovacs, J. M. (2012). The application of small unmanned aerial systems for precision agriculture: a review. Precision Agriculture, 13(6), 693-712.",
    "Weiss, M., Jacob, F., & Duveiller, G. (2020). Remote sensing for agricultural applications: a meta-review. Remote Sensing of Environment, 236, 111402.",
    "Tucker, C. J. (1979). Red and photographic infrared linear combinations for monitoring vegetation. Remote Sensing of Environment, 8(2), 127-150.",
    "Huete, A., Didan, K., Miura, T., et al. (2002). Overview of the radiometric and biophysical performance of the MODIS vegetation indices. Remote Sensing of Environment, 83(1-2), 195-213.",
    "Gitelson, A. A. (2004). Wide dynamic range vegetation index for remote quantification of biophysical characteristics of vegetation. Journal of Plant Physiology, 161(2), 165-173.",
    "Baret, F., & Guyot, G. (1991). Potentials and limits of vegetation indices for LAI and APAR assessment. Remote Sensing of Environment, 35(2-3), 161-173.",
    "Jacquemoud, S., Verhoef, W., Baret, F., et al. (2009). PROSPECT+SAIL models: a review of use for vegetation characterization. Remote Sensing of Environment, 113, S56-S66.",
    "Xue, J., & Su, B. (2017). Significant remote sensing vegetation indices: a review of developments and applications. Journal of Sensors, 2017, 1353691.",
    "Whitcraft, A. K., Vermote, E. F., Becker-Reshef, I., & Justice, C. O. (2015). Cloud cover throughout the agricultural growing season: impacts on passive optical Earth observations. Remote Sensing of Environment, 156, 438-447.",
    "Zhu, Z., & Woodcock, C. E. (2012). Object-based cloud and cloud shadow detection in Landsat imagery. Remote Sensing of Environment, 118, 83-94.",
    "Vermote, E. F., Tanre, D., Deuze, J. L., et al. (1997). Second simulation of the satellite signal in the solar spectrum, 6S: an overview. IEEE Transactions on Geoscience and Remote Sensing, 35(3), 675-686.",
    "Roy, D. P., Kovalskyy, V., Zhang, H. K., et al. (2016). Characterization of Landsat-7 to Landsat-8 reflective wavelength and normalized difference vegetation index continuity. Remote Sensing of Environment, 185, 57-70.",
    "Gao, F., Masek, J., Schwaller, M., & Hall, F. (2006). On the blending of the Landsat and MODIS surface reflectance: predicting daily Landsat surface reflectance. IEEE Transactions on Geoscience and Remote Sensing, 44(8), 2207-2218.",
    "Zhu, X., Chen, J., Gao, F., et al. (2010). An enhanced spatial and temporal adaptive reflectance fusion model for complex heterogeneous regions. Remote Sensing of Environment, 114(11), 2610-2623.",
    "Chen, J., Jonsson, P., Tamura, M., et al. (2004). A simple method for reconstructing a high-quality NDVI time-series data set based on the Savitzky-Golay filter. Remote Sensing of Environment, 91(3-4), 332-344.",
    "White, M. A., de Beurs, K. M., Didan, K., et al. (2009). Intercomparison, interpretation, and assessment of spring phenology in North America. Global Change Biology, 15(10), 2335-2359.",
    "Zeng, L., Wardlow, B. D., Xiang, D., et al. (2020). A review of vegetation phenological metrics extraction using time-series, multispectral satellite data. Remote Sensing of Environment, 237, 111511.",
    "Pittman, K., Hansen, M. C., Becker-Reshef, I., et al. (2010). Estimating global cropland extent with multi-year MODIS data. Remote Sensing, 2(7), 1844-1863.",
    "Hird, J. N., & McDermid, G. J. (2009). Noise reduction of NDVI time series: an empirical comparison of selected techniques. Remote Sensing of Environment, 113(1), 248-258.",
    "Verbesselt, J., Hyndman, R., Newnham, G., & Culvenor, D. (2010). Detecting trend and seasonal changes in satellite image time series. Remote Sensing of Environment, 114(1), 106-115.",
    "Savitzky, A., & Golay, M. J. E. (1964). Smoothing and differentiation of data by simplified least squares procedures. Analytical Chemistry, 36(8), 1627-1639.",
    "Beck, P. S. A., Atzberger, C., Hogda, K. A., et al. (2006). Improved monitoring of vegetation dynamics at high latitudes: a new method using MODIS NDVI. Remote Sensing of Environment, 100(3), 321-334.",
    "Pena-Barragan, J. M., Ngugi, M. K., Plant, R. E., & Six, J. (2011). Object-based crop identification using multiple vegetation indices, textural features and crop phenology. Remote Sensing of Environment, 115(6), 1301-1316.",
    "Gomez, C., White, J. C., & Wulder, M. A. (2016). Optical remotely sensed time series data for land cover classification: a review. ISPRS Journal of Photogrammetry and Remote Sensing, 116, 55-72.",
    "Belgiu, M., & Dragut, L. (2016). Random forest in remote sensing: a review of applications and future directions. ISPRS Journal of Photogrammetry and Remote Sensing, 114, 24-31.",
    "Zhong, L., Hu, L., & Zhou, H. (2019). Deep learning based multi-temporal crop classification. Remote Sensing of Environment, 221, 430-443.",
    "Monteith, J. L. (1972). Solar radiation and productivity in tropical ecosystems. Journal of Applied Ecology, 9(3), 747-766.",
    "Lobell, D. B. (2013). The use of satellite data for crop yield gap analysis. Field Crops Research, 143, 56-64.",
]

import html as _html
for i, r in enumerate(refs, 1):
    safe = _html.escape(f"[{i}] {r}", quote=True)
    d.body.append(
        '<w:p><w:pPr><w:spacing w:after="60"/><w:ind w:left="360" w:hanging="360"/>'
        '<w:jc w:val="both"/></w:pPr>'
        f'<w:r><w:rPr><w:sz w:val="20"/></w:rPr>'
        f'<w:t xml:space="preserve">{safe}</w:t></w:r></w:p>'
    )

print(f"Reference count: {len(refs)}")

out = "Chapter_7_Time_Series_Crop_Monitoring.docx"
d.save(out)
print("Saved", out)
