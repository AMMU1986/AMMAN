#!/usr/bin/env python3
"""
Build an Excel (.xlsx) workbook of faculty publications (1 Jul 2025 - 30 Jun 2026)
with DOI and Link columns filled in where a confident match was found via web search.

Uses ONLY the Python standard library (zipfile) to emit a minimal, valid .xlsx --
no external packages (the sandbox has no network/pip access).

Entries whose DOI could not be verified with high confidence are left BLANK and
flagged in a "Status" column, per the user's instruction ("leave blank + flagged").
"""

import html
import json
import os
import zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_JSON = os.path.join(BASE, "publications_doi_data.json")
OUT_XLSX = os.path.join(BASE, "Publications_By_Faculty_2025-2026.xlsx")

# ---------------------------------------------------------------------------
# Source rows: (S.No, Institute, Department, Authors, Title, Journal/Conf, Q)
# Publisher column is left blank in the source, so we keep it blank.
# ---------------------------------------------------------------------------
ROWS = [
    (1, "UIE", "EF 3", "Ritesh Kumar Kushwaha & Meenakshi", "Multiple crop disease detection using EfficientNetB0 – a CNN model", "Journal of Optical Communications", "Q1"),
    (2, "UIE", "EF 3", "Gurpreet Singh & Gyanendra Singh", "Internal Surface Finish Analysis of Inconel 625 Tube Using MAF and CMAF Processes", "Material and Mechanical Engineering Technology", "Q4"),
    (3, "UIE", "EF 3", "Yogendra Narayan & Rajeev Ranjan", "Exploring the Performance of Brain-Computer Interfaces in Assistive Technology", "Lecture Notes in Networks and Systems", "Q4"),
    (4, "UIE", "EF 3", "Meenakshi Munjal", "Performance Analysis of DS-CDMA Using GIG Orthogonal Codes Under AWGN and Rayleigh Fading Channel", "Lecture Notes in Networks and Systems", "Q4"),
    (5, "UIE", "EF 3", "Meenakshi Munjal", "QoS and QoE-Based Network Selection in Heterogenous Wireless Network", "Lecture Notes in Networks and Systems", "Q4"),
    (6, "UIE", "EF 3", "Meenakshi Munjal", "User-Oriented Approach for Network Selection in Heterogeneous Environments", "Lecture Notes in Networks and Systems", "Q4"),
    (7, "UIE", "EF 3", "Rajeev Ranjan & Yogendra", "Isolated Word Recognition and Feature Extraction Using Machine Learning", "Lecture Notes in Networks and Systems", "Q4"),
    (8, "UIE", "EF 3", "Garima Chandel & Saweta", "A Personal Health Assistant: Chatbot Design for Exercise and Nutrition Support", "Lecture Notes in Networks and Systems", "Q4"),
    (9, "UIE", "EF 3", "Sonia Bajaj", "Effect of Nonlocal Micropolar Thermoelasticity with Initial Stress in the Context of Dual Phase Lag in Thermodynamical Interactions", "2024 International Conference on Control, Computing, Communication and Materials, ICCCCM 2024", "Q4"),
    (10, "UIE", "EF 3", "Sandeep Kumar Saini", "Supervised Machine Learning-Based Models for Heart Disease Detection", "Lecture Notes in Networks and Systems", "Q4"),
    (11, "UIE", "EF 3", "Yogendra Narayan", "A Comprehensive Study on Deep Learning Models for the Detection of Diabetic Retinopathy using Pathological Images", "Archives of Computational Methods in Engineering", "Q1"),
    (12, "UIE", "EF 3", "Amman Jakhar", "Investigation on mechanical and microstructural behavior of API X70 and SA 516 dissimilar MIG welded joint", "International Journal of Materials Research", "Q3"),
    (13, "UIE", "EF 3", "Garima Chandel", "Advancements in the applications of organic light emitting diode", "Main Group Chemistry", "Q3"),
    (14, "UIE", "EF 3", "Simarpreet Kaur", "Photonic crystal based finer surface plasmonic sensor for detecting cancer", "Optoelectronics and Advanced Materials, Rapid Communications", "Q4"),
    (15, "UIE", "EF 3", "Rajeev Ranjan", "Simulation-based modeling of quantum key distribution in a Li-Fi system using free-space optics and polarization modulation", "Journal of Optical Communications", "Q1"),
    (16, "UIE", "EF 3", "Yogendra Narayan", "Motor imagery feature selection using modified whale optimization algorithm for brain–computer interface", "Iran Journal of Computer Science", "Q2"),
    (17, "UIE", "EF 3", "Saruchi", "Machine Learning Algorithm for Detecting and Predicting Chronic Kidney Disease", "Biomedical and Pharmacology Journal", "Q4"),
    (18, "UIE", "EF 3", "Amman Jakhar", "Heat transfer and the pressure drop properties of the mono and hybrid nanofluids on the flat tube", "AIP Conference Proceedings", "Q4"),
    (19, "UIE", "EF 3", "Shalinder Chopra & Gyanendra Singh", "Effectiveness of MQL turning for SS-316 under different cutting speed and feed rates", "AIP Conference Proceedings", "Q4"),
    (20, "UIE", "EF 3", "Amman Jakhar", "Experimental study on microstructural and corrosion behaviour of pipeline steel", "AIP Conference Proceedings", "Q4"),
    (21, "UIE", "EF 3", "Gyanendra Singh Goindi", "Influence of textured/un-textured tools while turning of medium carbon steel under Mql/dry environments", "AIP Conference Proceedings", "Q4"),
    (22, "UIE", "EF 3", "Shalinder Chopra & Gyanendra Singh", "Impact of MQL delivery parameters on SS-316 machining performance", "AIP Conference Proceedings", "Q4"),
    (23, "UIE", "EF 3", "Gyanendra Goindi", "Effect of cutting oil viscosity on surface roughness and cutting forces during MQL turning of aluminium alloy Al6061", "AIP Conference Proceedings", "Q4"),
    (24, "UIE", "EF 3", "Gyanendra Goindi", "Influence of tool surface texturing on machining performance during turning of aluminium alloy Al6061 under dry conditions", "AIP Conference Proceedings", "Q4"),
    (25, "UIE", "EF 3", "Amman Jakhar", "Design and manufacturing system for plastic tiles and analysis of waste plastic tiles and ceramic tiles", "AIP Conference Proceedings", "Q4"),
    (26, "UIE", "EF 3", "Amman Jakhar", "Experimental investigation on cutting temperature during near dry machining of AISI-202 steel using vegetable base oil", "AIP Conference Proceedings", "Q4"),
    (27, "UIE", "EF 3", "Yogendra Narayan & Rajeev Ranjan", "Advancing Emotion Recognition through Innovative EEG Feature Extraction Techniques using S-Transform", "2025 4th OPJU International Technology Conference on Smart Computing for Innovation and Advancement in Industry 5.0, OTCON 2025", "Q4"),
    (28, "UIE", "EF 3", "Rajanish Kumar Kaushal", "Automatic and Efficient Sound-Based Early Fault Detection for Vehicles based on GCN-A and LSTM Model", "3rd International Conference on Data Science and Information System, ICDSIS 2025", "Q4"),
    (29, "UIE", "EF 3", "Amman Jakhar", "Study on the Microstructural Behaviour of API X70 and 2205 DSS Dissimilar MIG Weld", "National Academy Science Letters", "Q1"),
    (30, "UIE", "EF 3", "Yogendra Narayan, Harpreet Singh Saghra, Mandeep Kaur Ghumman", "Assessing the Role of Intelligent BCI for Disabled Individuals - A Real-Time Approach and Standard BCI Architecture", "Proceedings of the 2025 12th International Conference on Computing for Sustainable Global Development, INDIACom 2025", "Q4"),
    (31, "UIE", "EF 3", "Akshaya Kubba", "Smart Agriculture: Identifying Plant Leaf Diseases with Machine Learning", "International Conference on Electronics, AI, and Computing: Innovating for a Sustainable and Connected Future, EAIC 2025", "Q4"),
    (32, "UIE", "EF 3", "Garima Chandel", "Enhancing Space Communication with DPSK-OFDM Modulation in Li-Fi and Free-Space Optics", "International Conference on Electronics, AI, and Computing: Innovating for a Sustainable and Connected Future, EAIC 2025", "Q4"),
    (33, "UIE", "EF 3", "Sonia Bajaj", "An Evaluation of Efficiency for Schools in Punjab Utilizing the DEA Technique", "International Conference on Electronics, AI, and Computing: Innovating for a Sustainable and Connected Future, EAIC 2025", "Q4"),
    (34, "UIE", "EF 3", "Yogendra Narayan,Rajanish Kumar Kaushal", "A Comparative Evaluation of Deep Learning Architectures for Prostate Cancer Segmentation: Introducing TrionixNet with N-Core Multi-Attention Mechanism", "Archives of Computational Methods in Engineering", "Q1"),
    (35, "UIE", "EF 3", "Yogendra Narayan,Rajanish Kumar Kaushal", "A Comprehensive Study of Enhanced Computational Approaches for Breast Cancer Classification: Comparative Analysis with Existing State of the Art Methods", "Archives of Computational Methods in Engineering", "Q1"),
    (36, "UIE", "EF 3", "Kamaldeep Kaur", "Nanomaterial-Powered Biosensors: A Cutting-Edge Review of Their Versatile Applications", "Micromachines", "Q1"),
    (37, "UIE", "EF 3", "Amman Jakhar", "Electrochemical Corrosion Study on Heat-Treated API X70 Steel Used for Pressure Vessel Applications", "National Academy Science Letters", "Q2"),
    (38, "UIE", "EF 3", "Himanshu", "A comprehensive review on graphene/CdS nanocomposites: From synthesis to multifunctional applications", "Next Materials", "Q3"),
    (39, "UIE", "EF 3", "Himanshu", "Numerical Simulation of Pb Free MGeI3 (M = Cs and Rb) Based Perovskite Solar Cells: Theoretical Insights into Performance Optimization by SCAPS-1D", "Springer Proceedings in Physics", "Q4"),
    (40, "UIE", "EF 3", "Rajanish Kumar Kaushal", "Earthquake Risk Severity Prediction and Disaster Management using a Hybrid ARIMA-LSTM Model", "Proceedings of 8th International Conference on Computing Methodologies and Communication, ICCMC 2025", "Q4"),
    (41, "UIE", "EF 3", "Mandeep Singh", "Middleware architecture performance analysis for vehicular ad hoc network", "Eurasip Journal on Wireless Communications and Networking", "Q1"),
    (42, "UIE", "EF 3", "Amman Jakhar", "Investigating the Effect of S4-C504 Filler on Mechanical and Microstructural Behavior of Similar API X70 MIG Welded Joint", "National Academy Science Letters", "Q2"),
    (43, "UIE", "EF 3", "Yogendra Narayan", "The Role of Artificial Intelligence in Predicting Intrauterine Fetal Demise: A Case-Control Study", "Vascular and Endovascular Review", "Q2"),
    (44, "UIE", "EF 3", "Rajeev Ranjan", "Lightweight Convolutional Neural Network for Automated Histopathology Image Classification on the Path MNIST Dataset", "Proceedings of the 4th International Conference on Innovative Mechanisms for Industry Applications, ICIMIA 2025", "Q4"),
    (45, "UIE", "EF 3", "Shalinder Chopra, Gyanendra Singh", "Influence of Oil Viscosity on Surface and Cutting Forces During MQL Turning Process of SS-316", "Lecture Notes in Mechanical Engineering", "Q4"),
    (46, "UIE", "EF 3", "Rajeev Ranjan", "Deep Learning based Early Detection of Cardiovascular Anomalies in IoT-Enabled Smart Hospitals", "Proceedings of the 4th International Conference on Innovative Mechanisms for Industry Applications, ICIMIA 2025", "Q4"),
    (47, "UIE", "EF 3", "Rajanish Kumar Kaushal , Yogendra Narayan", "A Comprehensive Study of Various Hybrid Deep Learning Models for Automated and Explainable Pneumonia Detection in the Pulmonary Alveolar Region: Current Insights and Future Directions", "Archives of Computational Methods in Engineering", "Q1"),
    (48, "UIE", "EF 3", "Meenakshi", "Analysis of Vehicular Communications in Heterogeneous Small Cell", "Wireless Personal Communications", "Q1"),
    (49, "UIE", "EF 3", "Ritesh Kumar Kushwaha, Rajeev Ranjan", "Enhancing Q-factor and BER in optical wireless systems using cryogenic Li-Fi architecture", "Journal of Optical Communications", "Q1"),
    (50, "UIE", "EF 3", "Sonia Bajaj, Sangeeta Kumari", "EFFECT OF INCLINED LOAD ON PLANE WAVE IN NONLOCAL THERMOELASTIC THREE-PHASE LAG MODEL", "Palestine Journal of Mathematics", "Q3"),
    (51, "UIE", "EF 3", "Sandeep Kumar Saini, Garima Chandel", "Evaluating Machine Learning Models for Chronic Kidney Disease Detection", "2025 International Conference on Smart and Sustainable Technology, INCSST 2025", "Q4"),
    (52, "UIE", "EF 3", "Rajanish Kumar Kaushal", "Advanced Anomaly Detection in E-Commerce Fraud Prevention Using a Hybrid XGBoost-DNN Model", "2025 International Conference on Smart and Sustainable Technology, INCSST 2025", "Q4"),
    (53, "UIE", "EF 3", "Sandeep Kumar Saini, Garima Chandel", "Time-Domain EEG Feature Analysis for Seizure Detection with Machine Learning", "2026 International Conference on Smart and Sustainable Technology, INCSST 2025", "Q4"),
    (54, "UIE", "EF 3", "Rohan Gupta , Gyanendra Singh, Garima Chandel", "Integrating Machine Learning and MediaPipe for Gym Management System Using AI", "2025 2nd International Conference on Computing and Data Science, ICCDS 2025", "Q4"),
    (55, "UIE", "EF 3", "Sandeep Kumar Saini, Garima Chandel", "Automated Onset Seizure Detection Using EEG Signals by Machine Learning", "Lecture Notes in Electrical Engineering", "Q4"),
    (56, "UIE", "EF 3", "Sandeep Kumar Saini, Garima Chandel", "Deepfake Detection Using AI and Machine Learning Algorithms", "2025 IEEE International Conference on Computer, Electronics, Electrical Engineering and their Applications, IC2E3 2025", "Q4"),
    (57, "UIE", "EF 3", "Kamaldeep Kaur", "4D PRINTING: FUNDAMENTALS, MATERIALS, APPLICATIONS AND CHALLENGES", "Smart Materials and Applications", "Q4"),
    (58, "UIE", "EF 3", "Sonia Bajaj", "TRENDS IN ROBOTICS TECHNOLOGY: SOLUTION FOR MATERIALS TO MANUFACTURING", "Smart Materials and Applications", "Q4"),
    (59, "UIE", "EF 3", "Saweta Verma, Garima Chandel", "IMPACT OF SMART MATERIALS ON DIGITAL TWIN", "Smart Materials and Applications", "Q4"),
    (60, "UIE", "EF 3", "Anupam Mittal", "AI-Driven Chatbots: Enhancing Educational Experiences Through Data Analytics", "Chatbots and Beyond: Exploring the Future of Conversational Technology in Education", "Q4"),
    (61, "UIE", "EF 3", "Yogendra Narayan", "Automated segmentation of gastrointestinal organs using the TATIMPA network: a novel robust comparative deep learning approach with integrated multi-pyramidal attention", "Network Modeling Analysis in Health Informatics and Bioinformatics", "Q1"),
    (62, "UIE", "EF 3", "Ruby Priya", "Waste plastic upcycling: MoO2/C nanocomposites supported on Ni foam for efficient oxygen evolution reaction", "Chemical Physics", "Q2"),
    (63, "UIE", "EF 3", "Richa Sharma", "Results on Coupled Coincidence Point with Y-Cone Metric Spaces", "Trends in Mathematics", "Q4"),
    (64, "UIE", "EF 3", "Sonia Bajaj", "Effect of gravity and variable thermal conductivity in a thermoelastic half space with dual phase lag model", "Scientific Reports", "Q1"),
    (65, "UIE", "EF 3", "Ruby Priya", "Unveiling the Effect of Surfactant: Aminoglycoside Interactions with Noble Metal Nanoparticles", "Journal of Physics: Conference Series", "Q3"),
    (66, "UIE", "EF 3", "Kavita Saini", "On Zweier I-Convergent Triple Sequence Spaces", "Boletim da Sociedade Paranaense de Matematica", "Q3"),
    (67, "UIE", "EF 3", "Yogendra Narayan,Mandeep Kaur Ghumman", "Strengthening Network Security through the Implementation of AI-Driven Automated Incident Response Systems", "Proceedings - 2025 IEEE International Conference on Compute, Control, Network and Photonics, ICCCNP 2025", "Q4"),
    (68, "UIE", "EF 3", "Yogendra Narayan", "Machine Learning-Based Weather Prediction for Agricultural Planning", "2025 2nd International Conference on New Frontiers in Communication, Automation, Management and Security, ICCAMS 2025", "Q4"),
    (69, "UIE", "EF 3", "Rajanish Kumar Kaushal", "Optimized quantum cryptography for secure blockchain transaction", "2025 2nd International Conference on New Frontiers in Communication, Automation, Management and Security, ICCAMS 2025", "Q4"),
    (70, "UIE", "EF 3", "Rajanish Kumar Kaushal", "Deep Learning-Driven Fault Detection in EV Powertrain Components", "2025 2nd International Conference on New Frontiers in Communication, Automation, Management and Security, ICCAMS 2025", "Q4"),
    (71, "UIE", "EF 3", "Rajanish Kumar Kaushal", "Optimized fuzzy-MPPT approach for superior solar power management in EV battery charging systems", "Energy Reports", "Q1"),
    (72, "UIE", "EF 3", "Gyanendra Singh Goindi", "Enhancing Al6061 alloy machinability in turning operations through RHVT, MQL and textured tool integration", "World Journal of Engineering", "Q2"),
    (73, "UIE", "EF 3", "Gurpreet Singh", "Introduction to the Fabrication of Materials Using Microwave Routes in View of Green Technology – Fundamentals and Applications", "Microwave Processing of Metallic Materials: Revolutionizing Surface Engineering for Green Manufacturing", "Q4"),
    (74, "UIE", "EF 3", "Kamaldeep Kaur", "Revolutionizing Material Science: A Thorough Introduction to the Properties and Innovations of Rare-Earth-Doped Metal Oxide Nanostructures", "Engineering Materials", "Q4"),
    (75, "UIE", "EF 3", "Ruby Priya", "Free surface unconfined melt electrospinning: an emergent approach", "Journal of Materials Science", "Q1"),
    (76, "UIE", "EF 3", "Amman Jakhar", "To Study the Effect of S4-C504 and S4-I504 Fillers on the Microstructural and Mechanical Behavior of Similar SA 516 MIG Weldments", "National Academy Science Letters", "Q2"),
    (77, "UIE", "EF 3", "Saruchi", "ADVANCED PREDICTION MODEL FOR EARLY DETECTION OF LUMPY SKIN DISEASE USING DEEP LEARNING AND IMAGE PROCESSING", "Journal of Mechanics of Continua and Mathematical Sciences", "Q4"),
    (78, "UIE", "EF 3", "Geetika Malik Ahlawat", "A Review on Carbon Dioxide Mitigation and Sustainable Energy Production Through Algal Biorefineries", "Bioenergy Research", "Q1"),
    (79, "UIE", "EF 3", "Yogendra Narayan", "Comparison of Properties of Recycled and River Sand Fine Aggregate on Concrete: A Smart Inverters Application", "Lecture Notes in Electrical Engineering", "Q4"),
    (80, "UIE", "EF 3", "Meenakshi Munjal", "Adaboost Learning Algorithm for Face Recognition", "2025 International Conference on Intelligent and Secure Engineering Solutions, CISES 2025", "Q4"),
    (81, "UIE", "EF 3", "Rajanish Kumar Kaushal", "Geothermal Energy in India: Present Developments and Global Comparisons", "2025 International Conference on Intelligent and Secure Engineering Solutions, CISES 2025", "Q4"),
    (82, "UIE", "EF 3", "Rajanish Kumar Kaushal", "Advanced Heart Disease Prediction Through Feature Selection-Driven Machine Learning Techniques", "2025 International Conference on Intelligent and Secure Engineering Solutions, CISES 2025", "Q4"),
    (83, "UIE", "EF 3", "Rajanish Kumar Kaushal", "Quality of Wine Prediction Using Machine Learning Algorithms", "2025 International Conference on Intelligent and Secure Engineering Solutions, CISES 2025", "Q4"),
    (84, "UIE", "EF 3", "Rajeev Ranjan", "Detection and Classification of ADHD using Deep Learning", "2025 International Conference on Intelligent and Secure Engineering Solutions, CISES 2025", "Q4"),
    (85, "UIE", "EF 3", "Meenakshi Munjal", "Non-Invasive Bioactive Bio patch for Astronauts Gut Health Monitoring", "2025 International Conference on Intelligent and Secure Engineering Solutions, CISES 2025", "Q4"),
    (86, "UIE", "EF 3", "Ritesh Kumar Kushwaha", "Cyber-attack Prediction on IIoT Devices Using Machine Learning", "2025 International Conference on Intelligent and Secure Engineering Solutions, CISES 2025", "Q4"),
    (87, "UIE", "EF 3", "Rajeev Ranjan", "Early Detection and Classification of ECG Arrhythmia using Machine learning and Ensemble learning", "2025 International Conference on Intelligent and Secure Engineering Solutions, CISES 2025", "Q4"),
    (88, "UIE", "EF 3", "Anupam Mittal", "Deep Learning-Based Detection of Skin and Oral Cancer: Advancing Diagnostic Accuracy and Early Intervention", "Lecture Notes in Electrical Engineering", "Q4"),
    (89, "UIE", "EF 3", "Mandeep Singh Devgan", "Attention-Guided Lightweight CNN-Transformer Fusion for Real-Time Traffic Sign Recognition in Adverse Environments: HACTNet", "IET Intelligent Transport Systems", "Q1"),
    (90, "UIE", "EF 3", "Anupam Mittal", "Optimizing Landslide Prediction Using Stacking Ensemble Learning and Remote Sensing Data", "Lecture Notes in Electrical Engineering", "Q4"),
    (91, "UIE", "EF 3", "Saweta Verma", "Artificial Intelligence and Smart Technology in the Evolution of Healthcare", "AIP Conference Proceedings", "Q4"),
    (92, "UIE", "EF 3", "Sandeep Kumar Saini", "Examining the Role of Chatbots in Online Learning and Student Engagement", "AIP Conference Proceedings", "Q4"),
    (93, "UIE", "EF 3", "Rajeev Ranjan", "Global Trends in Speaker Identification Under Voice Disguise: A 25-Year Review", "Sakarya University Journal of Computer and Information Sciences", "Q3"),
    (94, "UIE", "EF 3", "Richa Sharma", "A Note on Eigenvalues Significance in Digital Image Processing", "Boletim da Sociedade Paranaense de Matematica", "Q3"),
    (95, "UIE", "EF 3", "Sandeep Kumar Saini", "Analyzing and Implementation of Time Domain Features from Long-Duration EEG Signal for Seizure Detection using Machine Learning", "AIP Conference Proceedings", "Q4"),
    (96, "UIE", "EF 3", "Geetika Sharma", "Enhancing Power System Reliability with a Hybrid LSTM-Isolation Forest-Autoencoder Model", "Arabian Journal for Science and Engineering", "Q1"),
    (97, "UIE", "EF 3", "Amman Jakhar", "Optimization of Drilling Parameters for Aluminium 7075 Using Taguchi Method", "National Academy Science Letters", "Q2"),
    (98, "UIE", "EF 3", "Yogendra Narayan", "A Comprehensive Study of Various Hybrid Deep Learning Models for Leukaemia Classification: Comparative Analysis with Existing Studies", "Archives of Computational Methods in Engineering", "Q1"),
    (99, "UIE", "EF 3", "Gurpreet Singh", "Enhancing Inconel 625 tube finishing via magnetic abrasive brushes using RSM and GA-ANFIS optimization approach", "Proceedings of the Indian National Science Academy", "Q2"),
    (100, "UIE", "EF 3", "Richa Sharma", "An Adaptive Hybrid Method for Numerical Integration with Error Control", "Boletim da Sociedade Paranaense de Matematica", "Q3"),
    (101, "UIE", "EF 3", "Sonia Bajaj", "Effect of Variable Thermal Conductivity and Nonlocality in Pre-Stressed Thermoelastic Medium", "Mechanics of Solids", "Q3"),
    (102, "UIE", "EF 3", "Meenakshi Munjal", "The Impact of Flex Fuel in India: Financially and Environmentally", "2025 IEEE 2nd International Conference on Green Industrial Electronics and Sustainable Technologies, GIEST 2025", "Q4"),
    (103, "UIE", "EF 3", "Mandeep Singh", "Comparative Study of Face Recognition on Grayscale Images Using PCA, Eigenfaces, CNN, and Traditional Machine Learning Models", "Proceedings - 2025 5th International Conference on Internet of Things: Smart Innovation and Usage, IoT-SIU 2025", "Q4"),
    (104, "UIE", "EF 3", "Ritesh Kumar", "Modeling Avian Flu Risk using Predictive Modeling with Multi-Modal Data Sources", "2025 Global Conference on Information Technology and Communication Networks, GITCON 2025", "Q4"),
    (105, "UIE", "EF 3", "Ritesh Kumar", "Classification and Detection of ADHD using Deep Machine Learning Model", "2025 Global Conference on Information Technology and Communication Networks, GITCON 2025", "Q4"),
    (106, "UIE", "EF 3", "Mandeep Singh", "Explainable and Privacy-Preserving Multi-Class Network Intrusion Detection Using SHAP and LightGBM", "2025 5th International Conference on Advancement in Electronics and Communication Engineering, AECE 2025", "Q4"),
    (107, "UIE", "EF 3", "Rajeev Ranjan", "Air Quality Prediction Using Ensemble Gradient Boosting Model", "2025 Global Conference on Information Technology and Communication Networks, GITCON 2025", "Q4"),
    (108, "UIE", "EF 3", "Ritesh Kumar Kushwaha", "Air Quality Forecasting Using Generative AI and Ensemble Learning", "2025 Global Conference on Information Technology and Communication Networks, GITCON 2025", "Q4"),
    (109, "UIE", "EF 3", "Sandeep Kumar Saini", "Advancements in AIML and IoT Technologies for Real-Time Heart Rate Monitoring and Patient Care", "2025 Global Conference on Information Technology and Communication Networks, GITCON 2025", "Q4"),
    (110, "UIE", "EF 3", "Rajanish Kumar Kaushal", "Predictive Modeling of Diabetes Mellitus: Early Detection and Risk Stratification with Machine Learning", "2025 5th International Conference on Advancement in Electronics and Communication Engineering, AECE 2025", "Q4"),
    (111, "UIE", "EF 3", "Sandeep Kumar Saini", "Advanced Deep Learning Architecture for EEG-Based Onset Seizure Detection", "2025 Global Conference on Information Technology and Communication Networks, GITCON 2025", "Q4"),
    (112, "UIE", "EF 3", "Kavita Jindal", "A Fuzzy Logic-Based Model for Early Detection of Dementia Using Cognitive and EEG Parameters", "Proceedings - 2025 IEEE 3rd International Symposium on Sustainable Energy, Signal Processing and Cybersecurity, iSSSC 2025", "Q4"),
    (113, "UIE", "EF 3", "Garima Chandel", "IoT Based Failure Response System and Autonomous UAV Recovery", "Proceedings of the International Conference on Electrical, Electronics, and Computer Science with Advance Power Technologies - A Future Trends, ICE2CPT 2025", "Q4"),
    (114, "UIE", "EF 3", "Rajanish Kumar Kaushal", "SecureSmart: Blockchain-Assisted Adaptive Graph Neural Network for Intelligent Data Protection in Smart Cities", "Proceedings of the 9th International Conference on Electronics, Communication and Aerospace Technology, ICECA 2025", "Q4"),
    (115, "UIE", "EF 3", "Rajeev Ranjan", "A FREQUENCY-AWARE CNN–VISION TRANSFORMER WITH ADAPTIVE MULTI-STREAM FEATURE FUSION AND UNCERTAINTY ESTIMATION FOR EEG SEIZURE DETECTION", "Journal of Mechanics of Continua and Mathematical Sciences", "Q4"),
    (116, "UIE", "EF 3", "Richa Sharma", "Computational performance of classical and hybrid root-finding methods for real-world nonlinear models", "Discover Computing", "Q2"),
    (117, "UIE", "EF 3", "Apurva Thakur", "Deep Feature-Based Image Retrieval Using YOLOv8 and K-Nearest Neighbour Classifier", "Lecture Notes in Networks and Systems", "Q4"),
    (118, "UIE", "EF 3", "Mandeep Kaur Ghumman", "5G-Driven Telehealth Systems for High-Fidelity Remote Diagnostics", "Proceedings of the 4th IEEE International Conference on Interdisciplinary Approaches in Technology and Management for Social Innovation, IATMSI 2026", "Q4"),
    (119, "UIE", "EF 3", "Yogendra Narayan", "Deep Learning-Based EEG Signal Classification for Enhancing Brain-Computer Interface Accuracy", "Proceedings of the 4th IEEE International Conference on Interdisciplinary Approaches in Technology and Management for Social Innovation, IATMSI 2026", "Q4"),
    (120, "UIE", "EF 3", "Yogendra Narayan", "Machine Learning Approaches for EMG Signal Classification to Predict Hand Gesture", "Proceedings of the 4th IEEE International Conference on Interdisciplinary Approaches in Technology and Management for Social Innovation, IATMSI 2026", "Q4"),
    (121, "UIE", "EF 3", "Ritesh Kumar Kushwaha", "Performance Analysis of Li-Fi under Cryogenic Temperature Conditions", "IETACS 2025 - 2025 International Conference on Innovations and Emerging Technologies in AI and Communication Systems", "Q4"),
    (122, "UIE", "EF 3", "Rajanish Kumar Kaushal", "A Comprehensive Analysis and Classification of Municipal Waste: Trends, Challenges, and Management Strategies", "International Conference on Emerging Technologies in Electronics and Green Energy, ICETEG 2025", "Q4"),
    (123, "UIE", "EF 3", "Sandeep Kumar Saini", "Analysis of Time Domain Feature Extraction Method from Long-Duration EEG Signals for Seizure Detection", "Proceedings of 1st IEEE Uttar Pradesh Section Women in Engineering International Conference on Electrical, Electronics and Computer Engineering, UPWIECON 2025", "Q4"),
    (124, "UIE", "EF 3", "Ritesh Kumar Kushwaha", "Enhancing Fake News Detection Using a Hybrid RoBERTa and DCNN Architecture", "2025 2nd IEEE International Conference for Women in Computing, InCoWoCo 2025", "Q4"),
    (125, "UIE", "EF 3", "Rajanish Kumar Kaushal", "Efficient Breast Cancer Detection using a Dilated Convolutional Network with Walk-Spread-based Optimization", "Proceedings of the 4th International Conference on Intelligent Computing, Information and Control Systems, ICOIICS 2025", "Q4"),
    (126, "UIE", "EF 3", "Rajanish Kumar Kaushal", "Hybrid Random Forest-based Waste Classification System for Smart City Management", "Proceedings of the 6th International Conference on Smart Electronics and Communication, ICOSEC 2025", "Q4"),
    (127, "UIE", "EF 3", "Ruby Priya", "Deconvoluting capacitive and diffusive contributions in Cu-doped SnO2 nanoparticles for enhanced double-layer capacitance and oxygen evolution reaction", "Materials Today Communications", "Q1"),
    (128, "UIE", "EF 3", "Rajeev Ranjan", "A novel local optimal oriented pattern for image splicing detection leveraging deep learning and SVM", "Franklin Open", "Q2"),
    (129, "UIE", "EF 3", "Rajeev Ranjan", "Feature extraction and classification technique based speaker identification system of Indian regional accent", "Franklin Open", "Q2"),
    (130, "UIE", "EF 3", "Nibedita Banik", "Bioactive Xylan/Cellulose Nanocomposites: Catechol Crosslinking and Lecithin Stabilization", "Journal of Bio- and Tribo-Corrosion", "Q1"),
    (131, "UIE", "EF 3", "Yogendra Narayan, Rajeev Ranjan", "A Frequency-Aware CNN-Vision Transformer with Adaptive Multi-Scale Feature Fusion Framework for Real-Time EEG-Based Epileptic Seizure Detection", "2026 International Conference on Emerging Smart Computing and Informatics, ESCI 2026", "Q4"),
    (132, "UIE", "EF 3", "Ritesh Kumar Kushwaha", "Cryo-tunable graphene terahertz antenna with electrostatic reconfigurability and Q-factor enhancement", "Results in Optics", "Q2"),
    (133, "UIE", "EF 3", "Kavita Jindal", "AI-Driven Potato Disease Detection and Yield Optimization Through Leaf Image Analysis", "Proceedings - IEEE Madhya Pradesh Section Conference, MPCON 2026", "Q4"),
    (134, "UIE", "EF 3", "Manikanika", "Concluding Overviews of Metal Ions Dispersed Nanoparticles for Nanotechtonics Future Prospects", "Engineering Materials", "Q3"),
    (135, "UIE", "EF 3", "Sandeep Kumar Saini, Garima Chandel", "Comparative Analysis of Linear Regression, Polynomial Regression, and LSTM for Population Growth Prediction", "International Conference on Intelligent Processing, Hardware, Electronics, and Radio Systems, CIPHER 2026", "Q4"),
    (136, "UIE", "EF 3", "Meenakshi Munjal", "Machine Learning and Optimization for Future Healthcare Devices", "International Conference on Intelligent Processing, Hardware, Electronics, and Radio Systems, CIPHER 2026", "Q4"),
    (137, "UIE", "EF 3", "Meenakshi Munjal", "Digital Twins Framework for Modeling Human Decision-Making", "International Conference on Intelligent Processing, Hardware, Electronics, and Radio Systems, CIPHER 2026", "Q4"),
    (138, "UIE", "EF 3", "Gurmeet Kaur", "AIDS Infection Prediction from Clinical and Demographic Data Using Ensemble and Linear Models", "Proceedings of the 2026 International Conference on Intelligent and Innovative Technologies in Computing, Electrical and Electronics, IITCEE 2026", "Q4"),
    (139, "UIE", "EF 3", "Meenakshi Munjal", "Evaluating the Robustness of LLM Against Data Poisoning Attacks in Cybersecurity Datasets", "7th International Conference on Innovative Trends in Information Technology, ICITIIT 2026", "Q4"),
    (140, "UIE", "EF 3", "Meenakshi Munjal", "Federated LLMs for Collaborative Cyber Threat Intelligence without Data Sharing", "7th International Conference on Innovative Trends in Information Technology, ICITIIT 2026", "Q4"),
    (141, "UIE", "EF 3", "Yogendra Narayan", "A Comprehensive Study to Enhance Colorectal Cancer Diagnosis Using Hybrid Deep Learning Approaches: Comparative Analysis with Existing State of the Art Techniques", "Archives of Computational Methods in Engineering", "Q1"),
    (142, "UIE", "EF 3", "Akshaya Kubba,Vikas Wasson", "Enhanced Plant Leaf Disease Detection Using Optimized Machine Learning Models", "IETACS 2025 - 2025 International Conference on Innovations and Emerging Technologies in AI and Communication Systems", "Q4"),
    (143, "UIE", "EF 3", "Rajeev Ranjan", "AI for Mental Health Assessment: Opportunities, Challenge and Ethical Consideration", "IETACS 2025 - 2025 International Conference on Innovations and Emerging Technologies in AI and Communication Systems", "Q4"),
    (144, "UIE", "EF 3", "Meenakshi Munjal", "Federated Learning-Based LLMs for Privacy-Aware Cyber Threat Intelligence", "2026 1st International Conference on Artificial Intelligence and Machine Learning in Communication and Power Systems, AIMLCPS 2026", "Q4"),
    (145, "UIE", "EF 3", "Meenakshi Munjal", "Network Selection in Device-to-Device Communication Using Genetic AI", "2026 1st International Conference on Artificial Intelligence and Machine Learning in Communication and Power Systems, AIMLCPS 2026", "Q4"),
    (146, "UIE", "EF 3", "Meenakshi Munjal", "Evaluating Data Poisoning Resilience of Large Language Models for Cybersecurity Applications", "2026 1st International Conference on Artificial Intelligence and Machine Learning in Communication and Power Systems, AIMLCPS 2026", "Q4"),
    (147, "UIE", "EF 3", "Rajeev Ranjan", "Underwater Low Cost Subaqueous Acoustic Communication System", "Proceedings of IEEE International Conference on Emerging Engineering Technologies and Applications, IC-EETA 2025", "Q4"),
    (148, "UIE", "EF 3", "Kavita Jindal", "AI-Driven Heart Disease Prediction Using the XGBoost Ensemble Learning Technique", "Proceedings of IEEE International Conference on Emerging Engineering Technologies and Applications, IC-EETA 2025", "Q4"),
    (149, "UIE", "EF 3", "Rajeev Ranjan", "IoT based Automatic detection and classification of Smart Waste Segregation Bin for smart City", "Proceedings of IEEE International Conference on Emerging Engineering Technologies and Applications, IC-EETA 2025", "Q4"),
    (150, "UIE", "EF 3", "Rajeev Ranjan", "Lung Nodule Detection and Segmentation using Linear Kernel SVM", "Proceedings of IEEE International Conference on Emerging Engineering Technologies and Applications, IC-EETA 2025", "Q4"),
]

HEADERS = ["S no.", "Institute", "Department", "Name of Authors", "Title of Paper",
           "Name of Journal/ Conference", "Name of Publisher", "Q1/Q2/Q3/Q4",
           "Link", "DOI", "Status"]


def col_letter(idx):
    """0-based column index -> Excel column letter (A, B, ..., Z, AA, ...)."""
    s = ""
    idx += 1
    while idx:
        idx, rem = divmod(idx - 1, 26)
        s = chr(65 + rem) + s
    return s


def cell_xml(ref, value):
    if value is None or value == "":
        return f'<c r="{ref}" t="inlineStr"><is><t/></is></c>'
    esc = html.escape(str(value), quote=True)
    # preserve leading/trailing spaces
    return f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{esc}</t></is></c>'


def build():
    with open(DATA_JSON, encoding="utf-8") as f:
        found = json.load(f)

    # Build the grid: header + 150 data rows
    grid = [HEADERS]
    for (sno, inst, dept, authors, title, venue, q) in ROWS:
        rec = found.get(str(sno))
        if rec:
            link = rec.get("link", "")
            doi = rec.get("doi", "")
            conf = rec.get("confidence", "")
            status = f"Verified ({conf})" if conf else "Verified"
        else:
            link = ""
            doi = ""
            status = "NOT FOUND - verify manually"
        grid.append([sno, inst, dept, authors, title, venue, "", q, link, doi, status])

    # sheet1.xml rows
    rows_xml = []
    for r, rowvals in enumerate(grid, start=1):
        cells = "".join(cell_xml(f"{col_letter(c)}{r}", v) for c, v in enumerate(rowvals))
        rows_xml.append(f'<row r="{r}">{cells}</row>')
    sheet_data = "".join(rows_xml)
    ncols = len(HEADERS)
    dim = f"A1:{col_letter(ncols - 1)}{len(grid)}"

    # column widths (approx)
    widths = [6, 9, 11, 30, 60, 45, 16, 10, 42, 30, 26]
    cols_xml = "".join(
        f'<col min="{i+1}" max="{i+1}" width="{w}" customWidth="1"/>'
        for i, w in enumerate(widths)
    )

    sheet_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<dimension ref="{dim}"/>'
        '<sheetViews><sheetView workbookViewId="0">'
        '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
        '</sheetView></sheetViews>'
        '<sheetFormatPr defaultRowHeight="15"/>'
        f'<cols>{cols_xml}</cols>'
        f'<sheetData>{sheet_data}</sheetData>'
        '</worksheet>'
    )

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '</Types>'
    )

    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '</Relationships>'
    )

    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="Publications" sheetId="1" r:id="rId1"/></sheets>'
        '</workbook>'
    )

    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        '</Relationships>'
    )

    with zipfile.ZipFile(OUT_XLSX, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        z.writestr("xl/worksheets/sheet1.xml", sheet_xml)

    verified = sum(1 for (sno, *_rest) in ROWS if str(sno) in found)
    print(f"Wrote {OUT_XLSX}")
    print(f"Total rows: {len(ROWS)} | Verified DOIs: {verified} | Blank/flagged: {len(ROWS) - verified}")


if __name__ == "__main__":
    build()
