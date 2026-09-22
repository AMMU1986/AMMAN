# -*- coding: utf-8 -*-
"""Content for the consolidated Call for Book Chapters document."""


def build(doc, add_book):
    # ---- Front matter -----------------------------------------------------
    doc.title('Call for Book Chapters')
    doc.subtitle('A Consolidated Compilation of Open Invitations to Contribute')
    doc.para([('This document compiles the details of ', {}),
              ('18 open Call for Book Chapters', {'bold': True}),
              (' from Elsevier, Springer, CRC Press / Taylor & Francis, '
               'Wiley, ASME Press, Cambridge Scholars Publishing, Bentham '
               'Science and other publishers. Each entry lists the book '
               'title, publisher/indexing, editors, proposed chapters or '
               'topics, important dates and submission details.', {})])
    doc.page_break()

    # ======================================================================
    # 1. Elsevier - Data Driven Approach
    # ======================================================================
    add_book(
        doc, 1,
        'Data Driven Approach for Healthcare, Sustainability, Digital '
        'Transformation, and Global Impact',
        'Elsevier',
        indexing='ISBN: 978-0-443-58244-8',
        about='This book aims to bring together innovative research and '
              'practical insights on how data-driven approaches are '
              'transforming healthcare, sustainability, and digital '
              'transformation while creating a global impact. Key themes '
              'include: Healthcare & AI Applications; Sustainability & '
              'Environmental Impact; Digital Transformation & Smart Systems; '
              'Data Analytics & Decision Support; and Global Impact & Future '
              'Directions.',
        editors=[
            'Dr. Sumit Gupta',
            'Dr. Vineet Pandey',
            'Dr. PCS Reddy',
            'Dr. Seema Rawat',
        ],
        sections=[
            ('Section I - Foundations and Frameworks', [
                'Data-Driven Approaches for a Sustainable and Healthy World',
                'Machine Learning and Data Analytics - Core Concepts and '
                'Engineering Applications',
            ]),
            ('Section II - Data-Driven Healthcare', [
                'AI Applications in Clinical Decision Support, Disease '
                'Prediction, and Advanced Healthcare',
                'Big Data and AI in Pharmaceutical and Biomedical Research',
                'Contactless and IoT-Enabled Healthcare Systems',
            ]),
            ('Section IV - Circular Economy, Food Systems, and Supply Chains', [
                'Circular Economy and Intelligent Solid Waste Management',
                'Data Analytics in Food Systems and Agri-Supply Chains',
                'AI-Driven Supply Chain Management and Logistics Optimization',
            ]),
            ('Section V - Global Impact and Future Directions', [
                'Digital Equity, Global Health, and Emerging Technologies',
                'Future Directions in Data-Driven Systems: Generative AI, '
                'Explainable Intelligence, and Sustainable Global '
                'Transformation',
            ]),
        ],
        dates=[('Last date for complete chapter submission', '22 August 2025')],
        submission=[('Email', 'datadriven.chapter@gmail.com')],
        notes=[
            'Who can contribute: Academicians, researchers, industry '
            'professionals, practitioners, and policy experts working in '
            'relevant areas.',
            'Publication: Selected chapters will undergo rigorous peer '
            'review and be published by Elsevier.',
        ],
    )
    doc.page_break()

    # ======================================================================
    # 2. Elsevier - Sustainable Advanced Energy Storage
    # ======================================================================
    add_book(
        doc, 2,
        'Sustainable Advanced Energy Storage Technologies for Mobility '
        'Solutions',
        'Elsevier',
        indexing='Notification in 10 days',
        editors=['Volume editor: Miadreza Shafie-khah'],
        chapters=[
            'Introduction to Sustainable Advanced Energy Storage '
            'Technologies for Mobility Solutions',
            'Energy Storage Fundamentals, Taxonomy, and Performance Metrics '
            'for Mobility',
            'Lithium-Ion Batteries for Electric Mobility: Chemistries, Pack '
            'Design, and Fast Charging',
            'Emerging Battery Technologies for Next-Generation Mobility',
            'Battery Management Systems, Diagnostics, and Digital Twins for '
            'Mobility Storage',
            'Supercapacitors and Hybrid Energy Storage Systems for '
            'High-Power Mobility Applications',
            'Thermal Management and Thermal Energy Storage in Mobility '
            'Systems',
            'Hydrogen Storage and Fuel-Cell Systems for Sustainable Mobility',
            'Safety, Standards, and Certification of Rechargeable Energy '
            'Storage Systems',
            'Smart Charging, Vehicle-to-Grid, and Grid-Interactive Mobility',
            'Charging Hubs, Depot Electrification, and Integrated '
            'Multi-Energy Infrastructure Planning',
            'Lifecycle Sustainability, Second-Life Batteries, Recycling, and '
            'Digital Battery Passport',
            'Manufacturing Scale-Up, Supply Chains, and Commercialization of '
            'Advanced Storage Technologies',
            'Electric Car-Sharing: Financial Feasibility, Scenario Analysis, '
            'and Public Policy Implications',
            'Markets, Business Models, and Public Policy for Storage-Enabled '
            'Mobility',
            'Future Outlook: Strategic Pathways for Sustainable Mobility '
            'Storage',
            'Review of Battery Thermal Management Systems for Electric '
            'Vehicles: Advances, Challenges, and Role of Machine Learning',
            'MXenes the Cutting-Edge, Multipurpose Material for '
            'Supercapacitors, Energy Storage Devices, and Lithium-Ion '
            'Batteries',
            'Storage-Enabled Electric Mobility: Market Structures, Business '
            'Models, Policy Instruments, and Commercialization Pathways',
            'Emerging Solid-State Batteries: High-Efficiency, Compact, and '
            'Inherently Safe Energy Storage for Next-Generation Mobility',
            'Sustainable solution to support smart mobility in an integrated '
            'rail and grid management system',
        ],
        dates=[
            ('First Decision Notification', '10 days after initial chapter '
             'submission'),
            ('Final Acceptance Notification', '10 days after final chapter '
             'submission'),
        ],
        submission=[('Submit full chapter via',
                     'https://forms.gle/EspFmAGT2d6WVSsy6 (or the QR code on '
                     'the flyer)')],
        notes=['Chapters are listed but not limited to those above.'],
    )
    doc.page_break()

    # ======================================================================
    # 3. CRC Press - AI-Driven Governance
    # ======================================================================
    add_book(
        doc, 3,
        'AI-Driven Governance and Intelligent Enterprises: Concepts, '
        'Technologies, Management, and the Future of Intelligent Economies',
        'CRC Press - Taylor & Francis Group',
        editors=[
            'Dr. Hamed Taherdoost - Professor, University Canada West, Canada',
            'Dr. Deepanjana Varshney - Professor, Abu Dhabi School of '
            'Management, United Arab Emirates',
            'Dr. Mitra Madanchian - Associate Professor, University Canada '
            'West, Canada',
            'Dr. Vishal Jain - Professor, Vivekananda Institute of '
            'Professional Studies, India',
        ],
        sections=[
            ('Part I - Foundations of AI-Driven Governance and Intelligent '
             'Enterprises', [
                'AI-Driven Governance: Concepts, Evolution, and Strategic '
                'Implications',
                'The Rise of Intelligent Enterprises in the Digital Economy',
                'Rethinking Business Management in the Age of Artificial '
                'Intelligence',
                'Digital Transformation and Organizational Intelligence: '
                'From Automation to Augmented Decision-Making',
            ]),
            ('Part II - Emerging Technologies Enabling Intelligent '
             'Enterprises', [
                'Artificial Intelligence in Strategic Decision-Making and '
                'Business Analytics',
                'Blockchain and Decentralized Governance in Digital '
                'Enterprises',
                'Big Data Governance and Data-Driven Organizational '
                'Intelligence',
                'Intelligent Automation, Robotics, and the Future of '
                'Enterprise Operations',
            ]),
            ('Part III - Management, Leadership, and Organizational '
             'Transformation', [
                'Leadership in the Intelligent Enterprise: Managing '
                'AI-Enabled Organizations',
                'Innovation Management and Organizational Agility in the AI '
                'Economy',
                'Digital Risk, Cybersecurity Governance, and Enterprise '
                'Resilience',
                'Ethical AI, Responsible Innovation, and Corporate '
                'Governance',
            ]),
            ('Part IV - Future Governance and the Intelligent Economy', [
                'Regulatory Challenges in AI-Driven Economies',
                'Public-Private Collaboration in AI Governance Ecosystems',
                'The Future of AI-Driven Governance and Intelligent '
                'Enterprises',
            ]),
        ],
        dates=[
            ('Proposal Submission', '30 August 2026'),
            ('Full Chapter Submission', '30 September 2026'),
            ('Acceptance Notification', '30 October 2026'),
        ],
        submission=[('Submit proposal or full chapter to',
                     'bookchapteraidrivengovernance@gmail.com')],
        notes=['Publish with CRC Press (Taylor & Francis Group).'],
    )
    doc.page_break()

    # ======================================================================
    # 4. ASME Press - High-Entropy Alloy MMCs
    # ======================================================================
    add_book(
        doc, 4,
        'Next-Generation High-Entropy Alloy Reinforced Metal Matrix '
        'Composites: Manufacturing Processes, Performance, and Applications',
        'ASME Press',
        indexing='ASME Press Book Series: Next-Generation Manufacturing '
                 'Processes',
        about='This edited volume focuses on the latest advances in '
              'High-Entropy Alloy (HEA) reinforced Metal Matrix Composites. '
              'It covers advanced manufacturing processes, interfacial '
              'engineering, microstructural evolution, mechanical and '
              'functional performance, emerging applications, and future '
              'perspectives, paving the way for next-generation materials '
              'and smart manufacturing solutions.',
        editors=[
            'Dr. K. Harikrishna - Postdoctoral Fellow, IIT Madras, India; '
            'Assistant Professor, SVECW, India',
            'Dr. R. Seetharam - Assistant Professor, IIITDM Kurnool, India',
            'Dr. Radhamanohar Aepuru - Assistant Professor, University of '
            'Chile',
            'Dr. Veera Venkata Nagaraju - Postdoctoral Fellow (ANID), '
            'University of Chile',
            'Dr. Prasad Lokhande - Assistant Professor, IPPT PAN, Poland',
        ],
        sections=[
            ('Part I - Manufacturing Processes and Materials Development', [
                'Introduction & Design Principles of HEA-Reinforced MMCs',
                'Material Selection and Design Considerations',
                'Powder Metallurgy and Liquid-State Processing',
                'Solid-State, Friction Stir & Hybrid Manufacturing',
                'Additive Manufacturing & Hybrid Fabrication',
            ]),
            ('Part II - Microstructure, Interface Engineering, and '
             'Performance', [
                'Interfacial Engineering & Microstructural Evolution',
                'Mechanical Performance & Strengthening Mechanisms',
                'Tribological & Corrosion Performance',
                'Thermal Stability, High-Temperature & Environmental '
                'Performance',
            ]),
            ('Part III - Applications and Future Perspectives', [
                'Aerospace, Automotive & Defense Applications',
                'Energy, Biomedical & Functional Applications',
                'Sustainable Manufacturing & Industry 4.0',
                'Artificial Intelligence & Future Directions',
            ]),
        ],
        dates=[
            ('Chapter Proposal Submission', '15 September 2026'),
            ('Full Chapter Submission', '01 November 2026'),
            ('Final Chapter Submission', '30 November 2026'),
        ],
        submission=[
            ('For more details',
             'https://sites.google.com/view/asme-callforbookchapters'),
            ('For queries', 'katikaharikrishna95@gmail.com'),
        ],
        notes=['No publication fee: there is no publication fee for '
               'submitting or publishing a chapter in this book.'],
    )
    doc.page_break()

    # ======================================================================
    # 5. Elsevier / Scopus / ISTE / Wiley - Computational Mathematics
    # ======================================================================
    add_book(
        doc, 5,
        'Computational Mathematics in Engineering',
        'Elsevier / ISTE Group / Wiley',
        indexing='Scopus',
        chapters=[
            'Introduction to Computational Mathematics in Engineering',
            'Mathematical Foundations for Computational Engineering',
            'Numerical Methods and Computational Algorithms',
            'Computational Modeling and Simulation Techniques',
            'Optimization Techniques in Engineering',
            'Artificial Intelligence and Machine Learning in Engineering '
            'Mathematics',
            'Renewable Energy and Computational Engineering Applications',
            'Computational Software and Programming for Engineers',
            'Emerging Trends and Future Directions',
            'Advanced Computational Methods and Intelligent Engineering '
            'Systems',
        ],
        editors=[
            'Abhishek Kumar - Chandigarh University, Mohali, India',
            'Inam Ul Haq - CGC University, Mohali, India',
            'Priya Batta - Amity University, Mohali, India',
        ],
        dates=[
            ('Abstract Submission', '15 Sep 2026'),
            ('Final Chapter Submission', '25 Sep 2026'),
        ],
        submission=[
            ('All proposals should be submitted on',
             'ai.windenergy.editor@gmail.com'),
            ('Contact Person', 'Inam Ul Haq, +91 9622781525'),
        ],
        notes=['No publication charges.'],
    )
    doc.page_break()

    # ======================================================================
    # 6. CRC Press - Operations Modeling and Optimization
    # ======================================================================
    add_book(
        doc, 6,
        'Operations Modeling and Optimization: Tools for Manufacturing and '
        'Healthcare Systems',
        'Taylor & Francis / CRC Press',
        indexing='Series: Engineering Mathematics and Operations Research - '
                 'Tools, Techniques, Theory, and Applications Used in '
                 'Manufacturing and Management Science',
        about='The book focuses on recent theoretical, computational, and '
              'application-oriented developments in operations modeling, '
              'mathematical optimization, artificial intelligence, decision '
              'science, manufacturing systems, healthcare systems, and '
              'management science.',
        editors=[
            'Prof. Praveen Agarwal - Department of Mathematics, Anand '
            'International College of Engineering, Jaipur, India',
            'Prof. Yassine Sabbar - Department of Mathematics, University '
            'Moulay Ismail de Meknes, Meknes, Morocco',
            'Prof. Shilpi Jain - Department of Mathematics, Poornima College '
            'of Engineering, Jaipur, India',
            'Prof. Fatih Tank - Department of Economics, Atilim University, '
            'Ankara, Turkiye',
        ],
        topics_flat=[
            'Mathematical modeling and optimization',
            'Operations research and decision sciences',
            'Linear, nonlinear, stochastic, and robust optimization',
            'Multi-objective optimization',
            'Artificial intelligence and machine learning for optimization',
            'Neural-network-based modeling and optimization',
            'Supply chain and logistics optimization',
            'Manufacturing and production systems',
            'Scheduling and resource allocation',
            'Healthcare operations and optimization',
            'Healthcare logistics and decision-making',
            'Data-driven and intelligent optimization',
            'Fuzzy and uncertainty modeling',
            'Metaheuristic and evolutionary optimization',
            'Fractional-order modeling and optimization',
            'Sustainable manufacturing and operations',
            'Energy systems optimization',
            'Reliability and maintenance optimization',
            'Simulation and computational methods',
            'Digital twins and intelligent manufacturing',
            'Emerging applications of operations research and mathematical '
            'optimization',
        ],
        guidelines=[
            'Authors should submit: chapter title; abstract; author names; '
            'affiliations and email addresses; 4-6 keywords; and a brief '
            'chapter outline.',
            'Selected proposals will be invited to submit the full book '
            'chapter following the publisher guidelines.',
            'The publisher requires an abstract of approximately 150-200 '
            'words for each chapter.',
        ],
        dates=[
            ('Chapter Proposal / Abstract Submission', '15 September 2026'),
            ('Notification of Acceptance', '30 September 2026'),
            ('Full Chapter Submission', '30 November 2026'),
            ('Revised Chapter Submission', '15 January 2027'),
            ('Final Book Manuscript to Publisher', '30 January 2027'),
        ],
        submission=[
            ('Full chapter (PDF) to', 'shilpi.jain@poornima.org'),
            ('Subject line', 'Book Chapter for Edited Volume on "Operations '
             'Modeling and Optimization: Tools for Manufacturing and '
             'Healthcare Systems"'),
        ],
        notes=[
            'No APC / No chapter processing charge for contributors.',
            'Published by Taylor & Francis / CRC Press.',
        ],
    )
    doc.page_break()

    # ======================================================================
    # 7. CRC Press / Scopus - Smart technologies for Water Sustainability
    # ======================================================================
    add_book(
        doc, 7,
        'Smart Technologies for Water Sustainability and Policy (Volume 2)',
        'CRC Press - Taylor & Francis Group',
        indexing='Scopus',
        chapters=[
            'Fundamentals of AI and Water Sustainability',
            'AI-driven Autonomous Water Distribution Networks',
            'Reinforcement Learning for Water Resource Optimization',
            'AI-driven Water Quality and Pollution Monitoring in Water '
            'Supply Systems',
            'Edge Computing in Smart Water Systems',
            'Digital Twin Framework for Water Infrastructure',
            'Water Data Platforms and Interoperability Standards',
            'API-driven Smart Water Ecosystems',
            'One Water Framework Enabled by Smart Technologies',
            'AI for Climate Impact Assessment on Water Systems',
            'Carbon Accounting in Water Infrastructure',
            'Climate Financing Models for Water Projects',
            'Zero Trust Security for Water Infrastructure',
            'Post-Quantum Security for Critical Water Systems',
            'AI-based Water Pricing and Demand Modeling',
            'Data-Driven Policy Design for Water Systems',
            'Robotics and UAVs in Water Infrastructure Monitoring',
            'Advanced Materials and Nanotechnology in Water Treatment',
            'Blockchain-enabled Water Credit and Trading Systems',
            'Quantum Computing in Hydrological Modeling',
            'Urban Smart Water Grid Implementation - Global case study',
            'Future Research Directions, Policy Gaps, and Commercialization '
            'Opportunities in Smart Water Systems',
        ],
        editors=[
            'Dr. Neha Sharma - Chandigarh University, Punjab',
            'Dr. Abhineet Anand - Bahra University, HP',
            'Dr. Abhishek Kumar - Chandigarh University, Punjab',
            'Dr. Rajeev Tiwari - Bennett University, UP',
            'Dr. Anupam Tiwari - Institution of Electronics and '
            'Telecommunication Engineers, New Delhi',
            'Dr. Prateek Thapar - Quibtstensors, New Delhi',
        ],
        dates=[
            ('Abstract Submission', 'September 14, 2026'),
            ('Abstract Acceptance', 'October 01, 2026'),
            ('Final Chapter Submission', 'November 20, 2026'),
            ('Final Chapter Acceptance', 'December 31, 2026'),
        ],
        submission=[('Authors are invited to send their chapters to',
                     'smartwater367@gmail.com')],
    )
    doc.page_break()

    # ======================================================================
    # 8. Integrity Education - AI-Powered Legal Document Summarization
    # ======================================================================
    add_book(
        doc, 8,
        'AI-Powered Legal Document Summarization: Technologies, Trust, '
        'Governance and the Future of Legal Intelligence',
        'Integrity Education',
        about='The rapid growth of legal information and the complexity of '
              'legal documents create an unprecedented challenge for legal '
              'professionals and researchers. This edited volume explores '
              'how AI, NLP, Machine Learning, LLMs, and Generative AI are '
              'transforming legal document summarization, addressing '
              'accuracy, hallucination, explainability, citation '
              'preservation, bias, confidentiality, accountability, and '
              'ethical governance, and envisioning a future of trustworthy '
              'and human-centric legal intelligence.',
        editors=[
            'Gurpreet Kaur - Assistant Professor, UIC, Chandigarh University',
            'Dr. Kawaljit Kaur - Associate Professor, UIC, Chandigarh '
            'University',
            'Dr. Devinder Singh Anand - Associate Professor, UILS, '
            'Chandigarh University',
        ],
        topics_flat=[
            'Artificial Intelligence and the Evolution of Legal Document '
            'Summarization',
            'NLP, Machine Learning and Deep Learning for Legal Text '
            'Summarization',
            'Extractive, Abstractive and Hybrid Legal Summarization Models',
            'Large Language Models and Generative AI for Legal Summarization',
            'Retrieval-Augmented Generation (RAG) for Reliable Legal '
            'Summarization',
            'Hallucination Detection and Factual Consistency in AI-Generated '
            'Legal Summaries',
            'Citation, Statutory Provision and Precedent Preservation in '
            'Legal Summarization',
            'Legal Domain Datasets, Corpora and Annotation for Summarization',
            'Explainable AI and Transparent Legal Summarization',
            'Legal Reasoning-Aware and Argumentation-Aware Summarization',
            'Evaluation Metrics and Benchmarking of Legal Summarization '
            'Systems',
            'Multilingual and Low-Resource Legal Document Summarization',
            'Ethics, Bias, Privacy and Accountability in AI-Based Legal '
            'Summarization',
            'Human-Centred Legal Summarization and Access to Justice',
            'Future of Trustworthy Legal Intelligence: Agentic AI, '
            'Multimodal Systems and Next-Generation Legal Summarization',
        ],
        guidelines=[
            'Chapter length: 5,000-6,000 words.',
            'Abstract: 200-300 words with 4-6 keywords.',
            'Font: Times New Roman, size 12, line spacing 1.5.',
            'Similarity index should preferably be below 10%.',
            'Footnoting style: all references and footnotes must follow '
            'Bluebook: A Uniform System of Citation (21st Edition).',
        ],
        dates=[
            ('Full Chapter Submission', '5 September 2026'),
            ('Notification of Acceptance', '7 September 2026'),
            ('Tentative Publication', '25 September 2026'),
        ],
        submission=[
            ('Submission email', 'devinderanand1988@gmail.com'),
            ('Chapter processing charges', 'INR 900 (including hard copy '
             'charges), pay via UPI 9855005499'),
        ],
    )
    doc.page_break()

    # ======================================================================
    # 9. Wiley / Scopus - Digital Transformation of Industrial Biotechnology
    # ======================================================================
    add_book(
        doc, 9,
        'Digital Transformation of Industrial Biotechnology',
        'Wiley',
        indexing='Scopus',
        editors=[
            'Dr. Avnish Chauhan - Associate Professor, Graphic Era Hill '
            'University, Dehradun, India',
            'Dr. Prabhat K. Chauhan - Assistant Professor, AKS University '
            'Satna, Madhya Pradesh, India',
        ],
        chapters=[
            'Industrial Biotechnology in the Era of Circular Bioeconomy and '
            'Industry',
            'Microbial Cell Factories for Sustainable Biomanufacturing',
            'Advances in Synthetic Biology and Metabolic Engineering',
            'Precision Fermentation Technologies for High-Value Bioproducts',
            'Enzyme Engineering and Industrial Biocatalysis',
            'Artificial Intelligence and Machine Learning in Bioprocess '
            'Engineering',
            'Digital Twins and Smart Monitoring Systems for Industrial '
            'Bioreactors',
            'Internet of Things and Sensor-Based Process Control in '
            'Biotechnology Industries',
            'Biorefinery Approaches for Biomass Valorization and Resource '
            'Recovery',
            'Agricultural Waste Bioconversion and Waste-to-Wealth '
            'Technologies',
            'Industrial Wastewater Treatment and Resource Recovery Using '
            'Biotechnology',
            'Bioenergy Production: Biohydrogen, Biogas, and Advanced Biofuels',
            'Carbon Capture, Utilization, and Biological Conversion '
            'Technologies',
            'Sustainable Production of Bioplastics, Bio-Based Chemicals, and '
            'Green Materials',
            'Future Perspectives: Net-Zero Manufacturing, Circular '
            'Bioeconomy, and Climate-Smart Industrial Biotechnology',
        ],
        dates=[
            ('Abstract Submission Deadline', '8-15 Aug 2026'),
            ('Abstract Acceptance Notification', '16-20 Sept 2026'),
            ('Full Chapter Submission', '20 Sept 2026'),
            ('Revised Chapter Submission', '25-30 Sept 2026'),
            ('Final Submission', '30 Sept 2026'),
        ],
        submission=[('Submit chapter proposal / full chapters to',
                     'greensentinelbook@gmail.com')],
        notes=[
            'No publication fees for chapters submitted to this book.',
            'All submitted chapters will be peer-reviewed.',
            'Chapters must not have been published previously or be under '
            'consideration elsewhere.',
            'Abstract and chapter plagiarism should not be more than 10%.',
            'AI-generated abstracts and chapters will not be accepted.',
            'Each chapter must contain at least one foreign author.',
            'Chapters should be 8,000-10,000 words, including 3-4 figures '
            'and 2-3 tables.',
            'Reference style: APA.',
        ],
    )
    doc.page_break()

    # ======================================================================
    # 10. Wiley / Scopus - Horticultural Waste Valorization
    # ======================================================================
    add_book(
        doc, 10,
        'Biotechnological Innovations in Horticultural Waste Valorization '
        'and Fermentation Technologies',
        'Wiley',
        indexing='Scopus Indexed',
        chapters=[
            'Horticultural Waste Generation, Characterization, and Circular '
            'Bioeconomy Perspectives',
            'Physicochemical and Biochemical Profiling of Horticultural '
            'Residues for Biotechnological Applications',
            'Microbial Diversity and Functional Biocatalysts for '
            'Horticultural Waste Valorization',
            'Pretreatment Technologies for Enhanced Bioconversion of '
            'Horticultural Biomass',
            'Fermentation Technologies for Sustainable Conversion of '
            'Horticultural Wastes into Value-Added Products',
            'Fermentation and Synthetic Biology Approaches in Horticultural '
            'Waste Biorefineries',
            'Production of Biofuels from Horticultural Residues: Advances, '
            'Challenges, and Future Prospects',
            'Biochar and Carbon-Rich Materials Derived from Horticultural '
            'Wastes: Production and Agricultural Applications',
            'Recovery of Bioactive Compounds, Nutraceuticals, and Functional '
            'Ingredients from Horticultural By-Products',
            'Biotechnological Production of Industrial Enzymes, Organic '
            'Acids, and Microbial Metabolites from Horticultural Wastes',
            'Valorization of Horticultural Waste into Bioplastics, '
            'Biopolymers, and Sustainable Packaging Materials',
            'Artificial Intelligence, Omics Technologies, and Digital '
            'Innovations in Waste-to-Wealth Bioprocesses Systems',
            'Biorefinery Concepts and Cascade Valorization Strategies for '
            'Horticultural Wastes',
        ],
        editors=[
            'Dr. Tanmoy Sarkar - Department of Agriculture, Swami '
            'Vivekananda University, Bengal, India',
            'Dr. Tanmay Sarkar - Department of Food Processing Technology, '
            'Malda Polytechnic, WBSCTE, Bengal, India',
            'Dr. Debasis Mitra - Department of Microbiology, Graphic Era '
            '(Deemed to be University), Dehradun, Uttarakhand, India',
            'Dr. Amir Ali Khoddamzadeh - Department of Earth & Environment, '
            'Florida International University, Florida, U.S.',
        ],
        dates=[
            ('Abstract Submission', '23.08.2026'),
            ('Abstract Acceptance', '01.09.2026'),
            ('Submission Full Chapter', '15.11.2026'),
            ('Final Acceptance', '15.12.2026'),
        ],
        submission=[('Submit abstract', 'tanmoys@svu.ac.in')],
        notes=[
            'No processing fees required.',
            'AI generated content not accepted.',
            'Similarity index (plagiarism) < 10%.',
            'International collaboration highly encouraged.',
        ],
    )
    doc.page_break()

    # ======================================================================
    # 11. Springer - Data-Driven Sustainability
    # ======================================================================
    add_book(
        doc, 11,
        'Data-Driven Sustainability: Machine Learning for Environmental & '
        'Societal Challenges',
        'Springer (Edited Volume)',
        indexing='Scopus / Web of Science (submitted post-publication); '
                 'volume scope: 16 chapters across five sections',
        about='This edited volume brings together computer science, '
              'environmental science and policy studies - from climate '
              'modelling and smart agriculture to digital twins, geospatial '
              'intelligence and responsible AI governance. It surveys how '
              'machine learning and data-driven methods address '
              'environmental and societal challenges to produce novel, '
              'scalable and viable solutions, complemented by real-world '
              'case studies.',
        editors=[
            'Dr. Padmesh Tripathi - Delhi Technical Campus, Greater Noida, '
            'U.P., India',
            'Dr. Mritunjay Rai - Shri Ramswaroop Memorial University, '
            'Barabanki, U.P., India',
            'Dr. Seda Yildirim - Tekirdag Namik Kemal University, Turkiye',
            'Dr. Zahid Akhtar - State University of New York Polytechnic '
            'Institute, NY, USA',
        ],
        sections=[
            ('Section I - Foundations of Data-Driven Sustainability', [
                'Introduction to data-driven sustainability',
                'Sustainability challenges & the role of AI',
                'Machine learning techniques for sustainable systems',
            ]),
            ('Section II - Environmental Sustainability Applications', [
                'Climate change modelling using machine learning',
                'Smart water resource management',
                'Artificial intelligence in sustainable agriculture',
                'Biodiversity conservation & ecological intelligence',
            ]),
            ('Section III - Societal & Urban Sustainability', [
                'Smart cities & sustainable urban systems',
                'Sustainable healthcare systems using AI',
                'Sustainable supply chains & circular economy',
            ]),
            ('Section IV - Advanced Digital & Geospatial Technologies', [
                'Geospatial analytics for sustainability',
                'IoT & edge computing for environmental monitoring',
                'Digital twins for sustainable systems',
            ]),
            ('Section V - Governance, Ethics & Future Directions', [
                'Decision support systems for sustainability policy',
                'Ethics, transparency & responsible AI',
                'Future trends & global case studies',
            ]),
        ],
        guidelines=[
            '500-word proposal via online form (4-6 keywords, not from the '
            'title); author details and affiliations.',
            'Clear headings & subheadings; figures/tables as separate files.',
            'Original, unpublished work only; APA style with numbered '
            'citations.',
            'Submit PDF + MS Word source file; clear, academic, '
            'grammatically correct English.',
            'No Article Processing Charges (APC) - free to publish.',
            'Integrity rules: 0% AI-generated content (breach - author '
            'blacklisted); overall similarity index across the full chapter '
            'less than or equal to 10%; similarity from any single source '
            'less than or equal to 3%.',
        ],
        dates=[
            ('Proposal due (500 words)', '20 September 2026'),
            ('Notification of acceptance', '30 September 2026'),
            ('Full chapter submission', '15 November 2026'),
            ('First decision on chapter', '30 November 2026'),
            ('Second decision on chapter', '15 December 2026'),
            ('Final decision on chapter', '25 December 2026'),
        ],
        submission=[
            ('Submit your proposal', 'https://forms.gle/rF1hhtLDdUgoRMB58'),
            ('Queries', 'springereditedbookchapters@gmail.com (subject line: '
             '"Data-Driven Sustainability")'),
        ],
        notes=['The publisher will submit the volume for Scopus / Web of '
               'Science indexing after publication.'],
    )
    doc.page_break()

    # ======================================================================
    # 12. Cambridge Scholars - Leadership in the Age of Emerging Technologies
    # ======================================================================
    add_book(
        doc, 12,
        'Leadership in the Age of Emerging Technologies: Strategies for '
        'Leading Innovation, People, and Change in a Digital World',
        'Cambridge Scholars Publishing',
        editors=[
            'Mitra Madanchian - University Canada West, Vancouver, Canada',
            'Hamed Taherdoost - University Canada West, Vancouver, Canada',
        ],
        chapters=[
            'Leadership in the Age of Emerging Technologies: Setting the '
            'Context',
            'Emerging Technologies and Digital Transformation',
            'Leadership Competencies for a Digital World',
            'Leading Innovation and Managing Organizational Change',
            'Leading People in Technology-Driven Organizations',
            'Ethical Leadership, Governance, and Responsible Technology',
            'Leadership Across Industries: Cases and Best Practices',
            'The Future of Leadership: Preparing Organizations for '
            'Continuous Technological Change',
        ],
        dates=[
            ('Full Chapter Submission', '15 September 2026'),
            ('Acceptance Notification', '15 October 2026'),
        ],
        submission=[('Submission', 'htm.calls@gmail.com')],
        notes=[
            'Each chapter should be 5000-8000 words.',
            'References should be in APA style.',
            'Proposed chapters are not limited to those listed.',
        ],
    )
    doc.page_break()

    # ======================================================================
    # 13. Cambridge Scholars - Brain Fog
    # ======================================================================
    add_book(
        doc, 13,
        'Brain Fog: Navigating the Artificial Intelligence Era - '
        'Understanding Cognitive Challenges, Digital Overload, and Mental '
        'Well-Being in an AI-Driven World',
        'Cambridge Scholars Publishing',
        about='This book explores how AI and digital technologies influence '
              'human cognition, attention, memory, and mental well-being. It '
              'examines cognitive overload, digital dependency, information '
              'overload, and mental fatigue in an AI-driven world. Drawing '
              'on neuroscience, psychology, cognitive science, and AI, it '
              'highlights both the benefits and risks of AI-assisted living '
              'and provides practical strategies to improve focus, memory, '
              'mental wellness, and cognitive resilience.',
        editors=[
            'Dr. Rajeev Kumar - Dept. of Computer Science and Engg., '
            'Moradabad Institute of Technology, Moradabad, Uttar Pradesh, '
            'India',
            'Dr. Amit Singh - Faculty of Engineering, Teerthanker Mahaveer '
            'University, Moradabad, Uttar Pradesh, India',
            'Dr. Preeti Rani - Faculty of Engineering, Teerthanker Mahaveer '
            'University, Moradabad, Uttar Pradesh, India',
            'Dr. Flora Ferreira - FEP School of Economics and Management, '
            'University of Porto, Portugal',
        ],
        sections=[
            ('Part I - Foundations of Brain Fog and Cognitive Function', [
                'Understanding Brain Fog',
                'The Human Brain in the Information Age',
                'Evolution of Artificial Intelligence',
            ]),
            ('Part II - AI, Digital Technologies, and Cognitive Challenges', [
                'Information Overload and Cognitive Saturation',
                'The Neuroscience of Digital Dependency',
                'AI-Assisted Living and Cognitive Offloading',
                'Brain Fog in Education and Learning',
            ]),
            ('Part III - Brain Fog Across Society', [
                'Workplace Productivity and Cognitive Health',
                'Brain Fog and Mental Health',
                'Brain Fog in Healthcare',
                'Social Relationships and Human Connection',
            ]),
            ('Part IV - Building Cognitive Resilience', [
                'Digital Well-Being and Mindful Technology Use',
                'Enhancing Memory, Attention, and Focus',
                'Human-Centered AI and Ethical Innovation',
            ]),
            ('Part V - The Future of Human Cognition', [
                'Neurotechnology, Brain-Computer Interfaces and AI',
                'The Future of Intelligence',
            ]),
        ],
        dates=[
            ('Abstract Submission', '20 September 2026'),
            ('Notification of Acceptance', '1 October 2026'),
            ('Full Chapter Submission', '10 November 2026'),
            ('Final Acceptance Notification', '30 December 2026'),
        ],
        submission=[
            ('Submit abstract / full-length chapter proposals',
             'https://forms.gle/nRifoJzhpi3P7ckZ8'),
            ('For any query, email us', 'brainfog.publication@gmail.com'),
        ],
        notes=[
            'Submission should include a title, an abstract (maximum 500 '
            'words), keywords, and the name, designation and affiliation of '
            'the submitting author.',
            'No processing and publication charges.',
        ],
    )
    doc.page_break()

    # ======================================================================
    # 14. Elsevier / Scopus - Hybrid Additive Manufacturing of Ceramics
    # ======================================================================
    add_book(
        doc, 14,
        'Hybrid Additive Manufacturing of Ceramics: Advancing Processes, '
        'Materials, Properties and Applications for Next-Generation '
        'Manufacturing',
        'Elsevier',
        indexing='Scopus Indexed',
        about='This book provides a state-of-the-art review of hybrid '
              'additive manufacturing (HAM) of ceramics, covering '
              'fundamental principles, materials, process integration, '
              'modeling, properties, and real-world applications. It '
              'highlights challenges, opportunities, and future directions, '
              'serving as an essential resource for researchers, engineers, '
              'industry professionals, and policymakers.',
        editors=[
            'Prof. Arish Dasan - Institute of Digital and Ecological High '
            'Temperature Materials (I-D-E-M), State Key Laboratory of '
            'Advanced Refractories, Wuhan University of Science and '
            'Technology, Wuhan, China',
            'Prof. Vikas Sharma - University Center for Research and '
            'Development (UCRD), Chandigarh University, Mohali, Punjab, India',
            'Prof. J. Paulo Davim - Department of Mechanical Engineering, '
            'University of Aveiro, Campus Santiago, 3810-193 Aveiro, Portugal',
        ],
        topics_flat=[
            'Fundamentals and evolution of hybrid additive manufacturing of '
            'ceramics',
            'Ceramic materials: powders, feedstocks and composites',
            'Process technologies: AM, machining, joining and surface '
            'engineering',
            'Hybrid process integration and system architectures',
            'Design for AM ceramics and topology optimization',
            'Simulation, modeling and process-structure-property '
            'relationships',
            'Microstructure, mechanical, thermal and functional properties',
            'Non-destructive evaluation and in-situ monitoring',
            'Applications: structural, biomedical, energy and electronic '
            'ceramics',
            'Sustainability, circularity and life-cycle assessment',
            'Industrial case studies, standards and future perspectives',
        ],
        dates=[
            ('Abstract Submission Deadline', '01 September 2026'),
            ('Notification of Acceptance', '10 September 2026'),
            ('Full Chapter Submission Deadline', '30 December 2026'),
        ],
        submission=[
            ('Submit book chapter (Google Form)',
             'https://forms.gle/A8EevsqFJy6ptoNaA'),
            ('Contact', 'arish.dasan@wust.edu.cn; vikas.e17656@cumail.in'),
        ],
        notes=['No publication charges - high-quality contributions welcome '
               'without any publication fees.'],
    )
    doc.page_break()

    # ======================================================================
    # 15. Bentham Science / Scopus - AI in Agriculture
    # ======================================================================
    add_book(
        doc, 15,
        'Artificial Intelligence in Agriculture: A Scientific Analysis of '
        'Its Impact',
        'Bentham Science',
        indexing='Book will be submitted to Scopus for indexing',
        chapters=[
            'Artificial Intelligence in Agriculture: Applications of Machine '
            'Learning, Deep Learning, Internet of Things (IoT), and Digital '
            'Farming',
            'IoT-Enabled Smart Agriculture Systems for Plant Growth '
            'Monitoring and Detection',
            'A Hybrid Internet of Things (IoT) and Machine Learning '
            'Framework for Smart Greenhouse Automation',
            'Machine Learning-Based Decision Support Systems for Crop '
            'Selection, Cultivation, and Yield Optimization',
            'Deep Learning Techniques for Precision and Sustainable '
            'Agriculture',
            'Time-Series Forecasting Techniques (ARIMA, SARIMA, LSTM, GRU, '
            'and Related Models) for Weather, Soil, and Crop Dynamics',
            'Multimodal Data Acquisition and Sensor Fusion Techniques for '
            'Intelligent Plant Growth Monitoring',
            'Reinforcement Learning-Based Intelligent Smart Irrigation '
            'Systems',
            'An IoT and Explainable Artificial Intelligence (XAI)-Driven '
            'Architecture for Intelligent Irrigation Management',
            'Real-World Design, Deployment, and Implementation of Edge AI '
            'Systems for Sustainable Agriculture',
        ],
        editors=[
            'Dr. Suraj Arya (Editor) - Assistant Professor, Central '
            'University of Haryana, India',
            'Dr. Nor Azuana Ramli (Co-Editor) - Senior Lecturer, Universiti '
            'Malaysia Pahang Al-Sultan Abdullah, Malaysia',
            'Dr. Sishu Shankar Muni (Co-Editor) - Assistant Professor, '
            'Digital University Kerala, India',
        ],
        guidelines=[
            'Chapters must be original, unpublished, and not under '
            'consideration for publication elsewhere.',
            'The manuscript should be 15-20 pages in length, with a maximum '
            'of 8,000 words, including references.',
            'The chapter must be prepared strictly in accordance with the '
            'publisher formatting guidelines.',
            'Turnitin similarity index of less than 10% (excluding '
            'references, quotations, and bibliography, where applicable).',
            'AI-generated text, figures, images, tables, or other content '
            'are not permitted.',
        ],
        dates=[
            ('Chapter Proposal Submission Deadline', '20 August 2026'),
            ('Acceptance Notification', '30 August 2026'),
            ('Final Chapter Submission', '10 September 2026'),
        ],
        submission=[
            ('Submission Link', 'https://forms.gle/CZG7rHeiitiVmjSJ7'),
            ('For any queries', 'chaptersubmit26@gmail.com'),
        ],
        notes=['No Article Processing Fee.'],
    )
    doc.page_break()

    # ======================================================================
    # 16. Springer / Scopus - RIS Empowered Terahertz Antenna
    # ======================================================================
    add_book(
        doc, 16,
        'Reconfigurable Intelligent Surfaces Empowered Terahertz Antenna '
        'for Next Generation Communication Networks',
        'Springer',
        indexing='Scopus (approved by Springer, submitted for Scopus '
                 'indexing)',
        about='This book is divided into three major sections: Part 1 - '
              'Fundamentals and Emerging Antenna Technologies; Part 2 - '
              'Modeling, Simulation, and Performance Analysis; and Part 3 - '
              'System Integration and Emerging Applications. The volume is '
              'intended to cover more than 20 invited chapters to provide a '
              'complete solution for modern communication systems with '
              'low-power consumption, combining fundamentals, practical '
              'design techniques, simulation techniques, and practical '
              'applications.',
        editors=[
            'Dr. Brijesh Mishra - Associate Professor, School of Engineering '
            'and Technology, CMR University, Bengaluru, Karnataka',
            'Prof. Ghanshyam Singh - Professor & Director, Centre for Smart '
            'Information and Communication Systems, University of '
            'Johannesburg, South Africa',
        ],
        topics_flat=[
            'Fundamentals and Emerging Antenna Technologies',
            'Introduction to Advanced Antenna Systems',
            'Terahertz Antennas: Design, Materials, and Fabrication '
            'Techniques',
            'Terahertz Wave Propagation and potential Challenges',
            'Overview of Reconfigurable Intelligent Surfaces',
            'RIS-enabled Communication Systems',
            'Programmable Beamforming and Beam Steering in Terahertz and RIS '
            'Antennas',
            'Wireless Information and Power Transfer: Theory and '
            'Technological Evolution',
            'Antenna Architectures for Efficient Wireless Energy Harvesting',
            'Integration of Energy Harvesting with RIS and Terahertz '
            'Antennas',
            'Numerical Modeling Techniques for Terahertz Antennas and RIS',
            'Channel Modeling for Terahertz and RIS-enabled Networks',
            'Link Budget and Efficiency Analysis in Wireless Power Transfer '
            'Systems',
            'Machine Learning and AI for Smart Antenna and RIS Optimization',
            'MIMO antenna for RF energy harvesting applications',
            'Terahertz Antenna Systems for 5G and Beyond',
            'Smart Environments Enabled by RIS and Passive Beamforming',
            'RIS-Assisted Wireless Power Transfer and SWIPT Architectures',
            'Applications in IoT, Biomedical Devices, and Industrial Sensing',
            'Security and Privacy Issues in Advanced Antenna Networks',
            'Artificial intelligence and machine learning driven antenna '
            'system for 5G/6G applications',
            'Future Trends and Research Challenges in Terahertz, RIS, and '
            'Wireless Power Systems',
        ],
        dates=[
            ('Extended deadline', '30 September 2026'),
            ('Notifications', '15 October 2026'),
            ('Submission to Springer', '1 November 2026'),
            ('Online Publication (tentative)', 'February 2027'),
        ],
        submission=[
            ('Chapter submission email',
             'springereditedbookchapter2026@gmail.com'),
            ('Contact', 'springereditedbookchapter2026@gmail.com, Mobile: '
             '+917703004534'),
        ],
        notes=[
            'Permissible similarity and AI score: max. 15%.',
            'Publication fee: Free.',
            'The book chapter should have a minimum of 15 pages and align '
            'with the proposed chapter list.',
        ],
    )
    doc.page_break()

    # ======================================================================
    # 17. Springer - Next-Generation Circular Bio-economy for Agri Waste
    # ======================================================================
    add_book(
        doc, 17,
        'Next-Generation Circular Bio-economy for Agricultural Waste: '
        'Technologies, Digital Innovations, and Sustainable Resource '
        'Recovery',
        'Springer',
        editors=[
            'Dr. Pankaj Kumar - Senior Research Manager, Institute for '
            'Global Environmental Strategies, Japan',
            'Dr. Pawan Kumar Jha - Assistant Professor, University of '
            'Allahabad, Prayagraj, India',
        ],
        chapters=[
            'Circular Bioeconomy and Agricultural Waste: Concepts, Drivers, '
            'and Global Perspectives',
            'Agricultural Waste Streams: Generation, Characterization, and '
            'Resource Mapping',
            'Circular Resource Recovery and Sustainable Biorefinery Systems',
            'Microbial and Enzymatic Conversion of Agricultural Waste',
            'Biofertilizers, Biostimulants, and Soil Health Restoration',
            'Organic Waste Recycling and Nutrient Circularity',
            'Carbon-Negative Technologies for Agricultural Residues',
            'Fungal Biotechnology and Mushroom-Based Circular Systems',
            'Bioenergy and Renewable Fuels from Agricultural Waste',
            'Recovery of Industrial Enzymes, Biochemicals, and Platform '
            'Molecules',
            'Nutraceuticals, Functional Ingredients, and Bioactive Compounds',
            'Bioplastics, Green Packaging, and Sustainable Biomaterials',
            'Advanced Materials and Nanobiotechnology from Agricultural '
            'Residues',
            'Digital Transformation of Circular Bioeconomy Systems',
            'Sustainability Assessment, Policy, Commercialization, and '
            'Future Outlook',
        ],
        dates=[
            ('Abstract Submission Deadline', '04-15 Aug 2026'),
            ('Abstract Acceptance Notification', '15-25 Aug 2026'),
            ('Full Chapter Submission', '20 Oct 2026'),
            ('Revised Chapter Submission', '1-10 Nov 2026'),
            ('Final Acceptance', '25 Nov 2026'),
        ],
        submission=[('Submit chapter proposal / full chapters to',
                     'proposalsspringerbook@gmail.com')],
        notes=[
            'No publication fees for chapters submitted to this book.',
            'All submitted chapters will be peer-reviewed.',
            'Chapters must not have been published previously or be under '
            'consideration elsewhere.',
            'Abstract and chapter plagiarism should not be more than 10%.',
            'AI-generated abstracts and chapters will not be accepted.',
            'Each chapter must contain at least one foreign author.',
            'Chapters should be 8,000-10,000 words, including 3-4 figures '
            'and 2-3 tables.',
            'Reference style: APA.',
        ],
    )
    doc.page_break()

    # ======================================================================
    # 18. CRC / Routledge - AI for Smart Agriculture and Healthcare
    # ======================================================================
    add_book(
        doc, 18,
        'Artificial Intelligence for Smart Agriculture and Healthcare: '
        'Advancing Sustainable Development Goals',
        'Routledge / CRC Press - Taylor & Francis Group',
        indexing='Scopus',
        editors=[
            'Dr. Mithilesh Kumar Dubey - Professor, School of Computer '
            'Science & Engineering (SCOPE), VIT-AP University, Amaravati, '
            'Andhra Pradesh - 522241, India',
            'Khalil Ahmed - Research Scholar, School of Computer Science and '
            'Engineering, Lovely Professional University, Punjab - 144411, '
            'India',
        ],
        chapters=[
            'Introduction to Artificial Intelligence for Sustainable '
            'Development Goals (SDGs) for Smart Agriculture or Healthcare',
            'AI for Precision Agriculture or Healthcare: Concepts and '
            'Applications and Future Trend',
            'Machine Learning Models in Healthcare or Agriculture Data '
            'Analysis and Disease Diagnosis',
            'AI for Precision Agriculture: Enhancing Productivity and '
            'Resource Efficiency',
            'Deep Learning / Computer Vision in Agri-Tech or Healthcare '
            'Imaging',
            'AIoT and Edge Intelligence for Connected Health or Smart '
            'Farming',
            'Big Data Analytics for Sustainable Healthcare or Agricultural '
            'Systems',
            'AI-Driven Decision Support Systems and Predictive Modelling',
            'Integrating Renewable Energy and Green AI Practices for '
            'Sustainable Operations',
            'Emerging Technologies and Future Trends in Advancing AI-Driven '
            'Sustainability for Smart Agriculture or Health Care',
            'AIoT Implementations in Smart Hospitals, Digital Health '
            'Monitoring, or Climate-Smart Agriculture',
            'AI for Personalized Nutrition or Preventive Healthcare',
            'Robotics and Automation in Healthcare or Smart Agriculture',
            'Blockchain and AI for Transparent and Secure Health or Food '
            'Security',
            'AI for Natural or Man Made Disaster Management in Smart '
            'Agriculture or Health Care',
        ],
        dates=[
            ('Full Chapter Submission', '12 October 2026'),
            ('Final Decision', '20 October 2026'),
        ],
        submission=[
            ('Full chapter submission',
             'smartagricultureandhealthcare@gmail.com'),
            ('Contact', '+91 6006254008, +91 6280212568'),
        ],
        notes=[
            'No publication charge.',
            'Publisher: Routledge / Taylor & Francis Group.',
            'Chapter topics are not limited to those listed.',
        ],
    )
