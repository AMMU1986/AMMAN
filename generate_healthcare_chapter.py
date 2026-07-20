#!/usr/bin/env python3
"""
Generate Chapter: Smart Healthcare Analytics and Intelligent Care Systems
Word document (.docx) with square bracket citations in serial order.
Book: Transforming Business Education through Artificial Intelligence
"""

import zipfile
import xml.etree.ElementTree as ET
import os
import struct
import zlib

# OOXML Namespaces
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC_NS = "http://schemas.openxmlformats.org/drawingml/2006/picture"

ET.register_namespace('w', W_NS)
ET.register_namespace('r', R_NS)



def make_run(text, bold=False, italic=False, size=None, font=None, color=None):
    r = ET.Element(f'{{{W_NS}}}r')
    rPr = ET.SubElement(r, f'{{{W_NS}}}rPr')
    if bold:
        ET.SubElement(rPr, f'{{{W_NS}}}b')
    if italic:
        ET.SubElement(rPr, f'{{{W_NS}}}i')
    if size:
        ET.SubElement(rPr, f'{{{W_NS}}}sz', {f'{{{W_NS}}}val': str(size)})
        ET.SubElement(rPr, f'{{{W_NS}}}szCs', {f'{{{W_NS}}}val': str(size)})
    if font:
        ET.SubElement(rPr, f'{{{W_NS}}}rFonts',
                      {f'{{{W_NS}}}ascii': font, f'{{{W_NS}}}hAnsi': font})
    if color:
        ET.SubElement(rPr, f'{{{W_NS}}}color', {f'{{{W_NS}}}val': color})
    t = ET.SubElement(r, f'{{{W_NS}}}t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text
    return r



def make_paragraph(text, bold=False, italic=False, size=None, font=None,
                   alignment=None, spacing_after=None, spacing_before=None,
                   line_spacing=None, color=None):
    p = ET.Element(f'{{{W_NS}}}p')
    pPr = ET.SubElement(p, f'{{{W_NS}}}pPr')
    if alignment:
        ET.SubElement(pPr, f'{{{W_NS}}}jc', {f'{{{W_NS}}}val': alignment})
    sp = {}
    if spacing_after is not None:
        sp[f'{{{W_NS}}}after'] = str(spacing_after)
    if spacing_before is not None:
        sp[f'{{{W_NS}}}before'] = str(spacing_before)
    if line_spacing is not None:
        sp[f'{{{W_NS}}}line'] = str(line_spacing)
        sp[f'{{{W_NS}}}lineRule'] = 'auto'
    if sp:
        ET.SubElement(pPr, f'{{{W_NS}}}spacing', sp)
    r = make_run(text, bold=bold, italic=italic, size=size, font=font, color=color)
    p.append(r)
    return p



def make_heading(text, level=1):
    p = ET.Element(f'{{{W_NS}}}p')
    pPr = ET.SubElement(p, f'{{{W_NS}}}pPr')
    ET.SubElement(pPr, f'{{{W_NS}}}pStyle', {f'{{{W_NS}}}val': f'Heading{level}'})
    sizes = {1: 32, 2: 28, 3: 24}
    r = make_run(text, bold=True, size=sizes.get(level, 24))
    p.append(r)
    return p


def make_table(headers, rows):
    tbl = ET.Element(f'{{{W_NS}}}tbl')
    tblPr = ET.SubElement(tbl, f'{{{W_NS}}}tblPr')
    ET.SubElement(tblPr, f'{{{W_NS}}}tblStyle', {f'{{{W_NS}}}val': 'TableGrid'})
    ET.SubElement(tblPr, f'{{{W_NS}}}tblW',
                  {f'{{{W_NS}}}w': '5000', f'{{{W_NS}}}type': 'pct'})
    borders = ET.SubElement(tblPr, f'{{{W_NS}}}tblBorders')
    for bn in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        ET.SubElement(borders, f'{{{W_NS}}}{bn}',
                      {f'{{{W_NS}}}val': 'single', f'{{{W_NS}}}sz': '4',
                       f'{{{W_NS}}}space': '0', f'{{{W_NS}}}color': '000000'})
    # Header row
    tr = ET.SubElement(tbl, f'{{{W_NS}}}tr')
    for h in headers:
        tc = ET.SubElement(tr, f'{{{W_NS}}}tc')
        tcPr = ET.SubElement(tc, f'{{{W_NS}}}tcPr')
        ET.SubElement(tcPr, f'{{{W_NS}}}shd',
                      {f'{{{W_NS}}}val': 'clear', f'{{{W_NS}}}color': 'auto',
                       f'{{{W_NS}}}fill': '2E75B6'})
        cp = make_paragraph(h, bold=True, size=20, alignment='center')
        for r_el in cp.findall(f'.//{{{W_NS}}}r'):
            rPr = r_el.find(f'{{{W_NS}}}rPr')
            if rPr is not None:
                ET.SubElement(rPr, f'{{{W_NS}}}color', {f'{{{W_NS}}}val': 'FFFFFF'})
        tc.append(cp)
    # Data rows
    for i, row in enumerate(rows):
        tr = ET.SubElement(tbl, f'{{{W_NS}}}tr')
        for cell in row:
            tc = ET.SubElement(tr, f'{{{W_NS}}}tc')
            tcPr = ET.SubElement(tc, f'{{{W_NS}}}tcPr')
            if i % 2 == 0:
                ET.SubElement(tcPr, f'{{{W_NS}}}shd',
                              {f'{{{W_NS}}}val': 'clear', f'{{{W_NS}}}color': 'auto',
                               f'{{{W_NS}}}fill': 'F2F7FC'})
            tc.append(make_paragraph(str(cell), size=20))
    return tbl



def page_break():
    pb = ET.Element(f'{{{W_NS}}}p')
    r = ET.SubElement(pb, f'{{{W_NS}}}r')
    ET.SubElement(r, f'{{{W_NS}}}br', {f'{{{W_NS}}}type': 'page'})
    return pb


def fig_placeholder(num, caption, desc):
    """Figure placeholder with bordered box."""
    elements = []
    p = ET.Element(f'{{{W_NS}}}p')
    pPr = ET.SubElement(p, f'{{{W_NS}}}pPr')
    ET.SubElement(pPr, f'{{{W_NS}}}jc', {f'{{{W_NS}}}val': 'center'})
    pBdr = ET.SubElement(pPr, f'{{{W_NS}}}pBdr')
    for bn in ['top', 'left', 'bottom', 'right']:
        ET.SubElement(pBdr, f'{{{W_NS}}}{bn}',
                      {f'{{{W_NS}}}val': 'single', f'{{{W_NS}}}sz': '12',
                       f'{{{W_NS}}}space': '4', f'{{{W_NS}}}color': '2E75B6'})
    ET.SubElement(pPr, f'{{{W_NS}}}spacing',
                  {f'{{{W_NS}}}before': '240', f'{{{W_NS}}}after': '120'})
    p.append(make_run(f'[FIGURE {num} - See healthcare_figures/Figure_{num}.png]',
                      bold=True, size=24))
    elements.append(p)
    # Description
    p2 = ET.Element(f'{{{W_NS}}}p')
    pPr2 = ET.SubElement(p2, f'{{{W_NS}}}pPr')
    ET.SubElement(pPr2, f'{{{W_NS}}}jc', {f'{{{W_NS}}}val': 'center'})
    pBdr2 = ET.SubElement(pPr2, f'{{{W_NS}}}pBdr')
    for bn in ['left', 'bottom', 'right']:
        ET.SubElement(pBdr2, f'{{{W_NS}}}{bn}',
                      {f'{{{W_NS}}}val': 'single', f'{{{W_NS}}}sz': '12',
                       f'{{{W_NS}}}space': '4', f'{{{W_NS}}}color': '2E75B6'})
    p2.append(make_run(desc, italic=True, size=20))
    elements.append(p2)
    # Caption
    elements.append(make_paragraph(f'Figure {num}. {caption}',
                                   bold=True, italic=True, size=20,
                                   alignment='center', spacing_after=240))
    return elements



# =============================================================================
# SECTION 1: Introduction and Background
# =============================================================================

def get_section1():
    """Section 1: Introduction and Background"""
    return [
        ("Section 1: Introduction and Background", "h1"),
        ("1.1 Understanding Smart Healthcare Analytics", "h2"),
        (
            "Smart HC Analytics is about the use of data within healthcare applications to be able to provide "
            "the health service user with insights and decision-making based on the use of advanced tools such as "
            "Artificial Intelligence (AI), Internet of Things (IoT) and Big Data. It comprises of predictive, "
            "prescriptive and real-time analytics that enable healthcare professionals to move from reactive to "
            "pro-active and from one-size-fits-all to one personal approach to healthcare treatment. In hospitals "
            "and medical institutes, smart healthcare analytics can be put into use within clinical decision-making "
            "systems, for patient remote monitoring, patient population management and operations optimisation [1]. "
            "Traditionally, health systems have been struggling to manage information after it has already happened, "
            "and have been using manual means of capturing and analysing the information, which prevents them from "
            "acting rapidly. With the digital healthcare records and the Electronic Health Records (EHRs) [2] "
            "introduction, the healthcare sector began to focus on \"data-driven practice\". The healthcare sector "
            "started taking the \"data-driven practice\" path with the technology that can read healthcare information "
            "digitally, called Electronic Health Records (EHRs) [2]. Early systems were, however, to some extent "
            "isolated and were not always interoperable, limiting the impact they had. However, with the introduction "
            "of smart healthcare analytics, these weaknesses can be resolved by combining all data sources and can "
            "deliver seamless information flow [3]."
        , "body"),

        (
            "Recent developments in computational power and data storage technologies have driven the shift towards "
            "intelligent systems in healthcare. Today's healthcare systems are data intensive, collecting huge amounts "
            "of information from a variety of sources, such as medical imaging, wearable devices, genome sequencing, "
            "and administrative data. Advanced algorithms can be used to leverage this data to gain insights into "
            "disease patterns, efficacy of treatment, and patient behavior [4]. As illustrated in Figure 1, the "
            "integration of AI, IoT, and Big Data forms the foundational triad of smart healthcare analytics, "
            "enabling seamless data collection, processing, and actionable decision-making. Artificial Intelligence "
            "(AI) has become a key component in the era of smart healthcare analytics, allowing machines to learn "
            "from data and make informed decisions. Machine learning models can detect patterns and make predictions, "
            "and deep learning can be used to analyze complex data, like medical images and genomic data [5]. AI can, "
            "for example, help with early cancer detection, improving survival rates. IoT devices help to gather "
            "health data constantly, in real time. Healthcare providers can remotely monitor patients and identify "
            "anomalies before they become critical with wearable devices, smart sensors and connected medical "
            "equipment [6]. This feature is particularly useful for chronic health management and lowering the "
            "risk of re-hospitalization."
        , "body"),

        (
            "AI and IoT supplement Big Data analytics by offering intelligence and connectivity, while Big Data "
            "infrastructure and tools enable the processing and analysis of vast amounts of data. Healthcare data "
            "is big, fast, and different, and conventional data processing techniques don't fit the bill. Big Data "
            "Technologies support the efficient storage, integration and analysis of data that yield more accurate "
            "and timely insights [7]. In conclusion, smart healthcare analytics is a transformative approach in the "
            "healthcare sector that promotes data-informed decision making, efficiency, and patient-centric care. "
            "In addition to their beneficial effect on clinical outcomes, they also contribute to the efficiency of "
            "healthcare systems and cost reductions, being a key element in modern health care systems [8]."
        , "body"),
        ("fig1", "figure"),
        ("1.2 The Need for Intelligent Care Systems", "h2"),
        (
            "While there has been considerable progress in medical research, the healthcare system around the world "
            "is still plagued with many problems. These include high cost of healthcare, growing number of patients, "
            "lack of skilled workforce, and delivery inefficiencies [9]. Traditional health care systems, which tend "
            "to be reactive, do not seem to cope well with these issues. Patients often only go to doctors when they "
            "are experiencing symptoms, which results in a later diagnosis and treatment. Lack of co-ordination "
            "amongst various stakeholders such as insurance companies, laboratories, clinics and hospitals is one of "
            "the primary problems in healthcare delivery. This division leads to waste in resources, human and "
            "financial, and suboptimal patient care [10]. More than that, the increasing prevalence of chronic "
            "conditions, including diabetes, cardiovascular disease, cancer, and other chronic diseases, has also "
            "added significant stress to healthcare systems, requiring new, efficient, and scalable solutions."
        , "body"),

        (
            "In the past few years, there has been a high demand for personalized and predictive care as well. "
            "Patients want care that is personalized to their specific medical history, preferences and needs. "
            "Personalized medicine accounts for the genetic, environmental and lifestyle factors, and demands "
            "high-level analytics and data integration capabilities [11]. But Predictive care is based on the "
            "concept of figuring out potential health risks before they materialize and intervening and preventing "
            "them from happening. Intelligent care systems overcome these challenges through smart healthcare "
            "analytics, which enable to provide proactive, efficient and patient-centred care. These systems "
            "collect information from various sources, process it in real-time, and deliver actionable insights "
            "to healthcare professionals. In some cases, predictive analytics can be used to detect patients who "
            "are likely to develop specific diseases or conditions, and take appropriate action at the right time "
            "to prevent complications [12]."
        , "body"),
        (
            "Furthermore, intelligent care systems improve the efficiency of the business by automating routine "
            "tasks and optimizing the use of resources. Automated scheduling systems can also help decrease wait "
            "times, and automated billing and administrative procedures can decrease mistakes and enhance "
            "effectiveness [13]. The use of remote monitoring and telemedicine services also help to decrease "
            "the number of visits to the hospital, improving access and cost-effectiveness. One of the other "
            "important benefits of intelligent care systems is that they enhance patient engagement. These systems "
            "also give patients access to their health information and personalized recommendations, which helps "
            "them take control of their health [14]. This not only leads to better health results but additionally "
            "boosts patient fulfillment and rely in health care providers."
        , "body"),

        (
            "For businesses, intelligent care systems provide many benefits, such as cost savings, efficiency gains, "
            "and a competitive edge. Those healthcare institutions that adopt these technologies have a greater chance "
            "of responding to the changing needs of patients and market dynamics. Healthcare organizations that adopt "
            "these technologies are better equipped to respond to the changing needs of patients and market "
            "dynamics [15]. There are also challenges in implementing the intelligent care systems, including data "
            "privacy concerns, high upfront costs, and the need for skilled personnel. Solving these challenges "
            "demands a well-thought-out approach that encompasses solid data governance policies, investments in "
            "infrastructure, and ongoing training and development for healthcare professionals."
        , "body"),
        ("1.3 Chapter Objectives and Structure", "h2"),
        (
            "The purpose of this chapter is to give an overview of smart healthcare analytics and intelligent care "
            "systems, highlighting their impact on business education and healthcare management. The main research "
            "aims are: To understand, conceptualize and define smart healthcare analytics and the elements of it. "
            "To explore the technological drivers that enable Intelligent Healthcare systems. To study the "
            "difficulties and opportunities of implementing intelligent care systems. To learn about the contribution "
            "of these systems to better health services and health outcomes. To evaluate the implications for "
            "business education and to suggest directions for future research."
        , "body"),

        (
            "Chapter aims to answer the following research questions: How will Smart Healthcare analytics change "
            "Current Healthcare System? What are the most important technologies that are enabling intelligent "
            "care systems? What problems will need to be addressed for the effective implementation of these "
            "systems? What does business education have to do to equip the business workforces for this change?"
        , "body"),
        (
            "The benefit of this chapter is that it brings a multidisciplinary approach together, where healthcare "
            "technology and business education converge. With the data revolution in health care, there is a greater "
            "demand for health care professionals with both technical and managerial skills. This chapter underscores "
            "the need for the inclusion of data analytics, AI and healthcare management in business education "
            "programs to equip future business leaders for the changing healthcare environment [16]. In addition, "
            "the chapter discusses the implementation of intelligent care systems, and provides a framework that "
            "can be applied by healthcare organisations to effectively implement these technologies. The chapter "
            "is both theoretical and practical and, therefore, adds to the existing knowledge base, while offering "
            "advice for researchers, practitioners and policy makers."
        , "body"),
        (
            "The chapter is organized as follows. In Section 1, smart healthcare analytics are introduced and the "
            "need for intelligent care systems is discussed. Section 2 discusses the technological motivations and "
            "main characteristics of intelligent healthcare systems. Section 3 provides a framework for implementing "
            "these systems, covering data management, integration with analytics and system deployment. The "
            "implications for healthcare business education and practice are discussed in Section 4, where the need "
            "for understanding and application of interdisciplinary skills and ethical issues are emphasized. "
            "Finally, in Section 5, suggestions for future research are presented and a summary of findings and "
            "recommendations is given in the end of the chapter [17]."
        , "body"),
    ]



# =============================================================================
# SECTION 2: Literature Review
# =============================================================================

def get_section2():
    """Section 2: Literature Review"""
    return [
        ("Section 2: Literature Review", "h1"),
        ("2.1 Technological Foundations of Smart Healthcare", "h2"),
        (
            "At the core of smart healthcare systems are the implementation of sophisticated digital technologies, "
            "capable of connecting healthcare data collection, storage, and analysis efficiently. These include the "
            "Internet of Things (IoT), cloud computing, and real-time monitoring systems, all of which are key "
            "components in the shift towards creating an intelligent, data-driven healthcare ecosystem. IoT has "
            "revolutionized healthcare by enabling the interconnection of medical devices, sensors, and applications "
            "that continuously collect patient data. Smartwatches and fitness trackers as well as biosensors are "
            "worn to track physiological data like heart rate, blood pressure, glucose levels, and physical "
            "activity [18]. These devices can offer timely and accurate data on patient wellbeing, helping "
            "healthcare providers identify any irregularities and take action in time. Moreover, the application "
            "of IoT in healthcare also facilitates remote patient monitoring, which makes the patient less likely "
            "to visit hospitals with high frequency and enhances patient convenience [19]."
        , "body"),
        (
            "Beyond wearables, IoT-based medical devices like smart infusion pumps, connected ventilators and "
            "implantable sensors help to improve clinical decision making and patient safety. These devices collect "
            "data continuously, which can be used to look for trends and forecast future health hazards [20]. "
            "There are, however, several issues with the widespread use of IoT in healthcare, including data "
            "security and interoperability, and device standardization, which need to be overcome to deliver "
            "reliable and secure healthcare. The advantages of cloud computing for smart healthcare analytics "
            "are that it offers the scalability and flexibility needed for data storage and processing. Healthcare "
            "organizations have access to a wealth of data from different sources such as electronic health records "
            "(EHRs) and medical imaging systems, along with IoT devices. Cloud platforms allow for the efficient "
            "storage, management, and sharing of this data, making it easier to collaborate among healthcare "
            "providers and accessible [21]."
        , "body"),

        (
            "Cloud-based computing can also aid in deploying cutting-edge analytics tools and AI algorithms that "
            "demand a great deal of computing power. Cloud-based applications can help healthcare organizations "
            "save on infrastructure costs and boost efficiency. Moreover, cloud computing can promote the "
            "interoperability between the various healthcare systems giving seamless data exchange and "
            "integration [22]. In the realm of smart healthcare, real-time monitoring and data collection systems "
            "play a pivotal role. These systems are powered by IoT devices and cloud platforms, continuously "
            "gathering and analyzing patient data. By monitoring in real-time, it is possible to detect health "
            "problems early, and take action to change a person's trajectory before it gets worse, which leads "
            "to better patient outcomes [23]. For instance, continuous glucose monitoring for diabetic patients "
            "can give them instant information about their blood glucose levels, leading to improved disease "
            "management. In summary, the technological pillars of smart healthcare are IoT, cloud computing, "
            "and real-time data systems. All these technologies contribute to smart healthcare ecosystems that "
            "are proactive, efficient and patient-centric [24]."
        , "body"),
        ("fig2", "figure"),
        ("2.2 Artificial Intelligence Applications in Healthcare", "h2"),
        (
            "Intelligent care systems are the next level in the healthcare continuum, leveraging cutting-edge "
            "analytics, AI, and digital solutions to provide personalized, proactive care. These systems aim at "
            "enhancing patient handling through the use of predictive analysis, digital twins, and virtual patient "
            "modeling. A digital twin is a virtual representation of a physical object\u2014like a patient\u2014that is "
            "developed with real-time data and sophisticated modeling methods. In the healthcare sector, digital "
            "twins can be used to simulate patient conditions and predict the progression of disease. By analyzing "
            "data from various sources, including medical records, wearable devices, and genetic information, "
            "digital twins provide a comprehensive view of patient health [25]. Virtual patient modelling is an "
            "extension of digital twins, which simulate the physiology and behavior of patients. These models can "
            "be used to test various treatment scenarios and predict their results, which can help to create "
            "individualized treatment plans. For example, virtual models of the human heart can be used to "
            "simulate the effects of different interventions on cardiac function."
        , "body"),

        (
            "Predictive analytics is an important part of intelligent care systems as it facilitates early "
            "interventions in disease management. Predictive models can be used to assess historical and real-time "
            "data to find pattern and trend that may result in health risks. This enables a medical practitioner to "
            "act in time before disease occurs to enhance patients' health and save health care costs. For example, "
            "a predictive analytics system can identify patients who are likely to be readmitted to the hospital "
            "after discharge and design interventions to help prevent complications. Likewise, predictive models "
            "can be helpful to identify the early indicators of chronic diseases like diabetes and hypertension, "
            "enabling early care and prevention. Intelligent care systems also enhance patient engagement by "
            "providing personalized recommendations and real-time feedback. Through patient mobile applications, "
            "patients can have access to their health records and receive advice on lifestyle changes, medicine "
            "adherence, and disease management. This gives the patients control over their health and improves "
            "their outcomes, thereby enhancing their satisfaction."
        , "body"),
        (
            "The intelligent care systems offer operational efficiency from a management standpoint, optimising "
            "the use of resources and cutting costs. Analytics can help detect inefficiencies, optimize workflows, "
            "and enhance the delivery of services in healthcare organizations. Predictive models can help to "
            "optimize staffing levels, minimize waiting times, and enhance the flow of patients in healthcare "
            "facilities, for instance. While intelligent care systems offer numerous advantages, they also come "
            "with a number of difficulties, such as data privacy concerns, high implementation costs, and the "
            "requirement for qualified personnel. Solutions to these issues need to be integrated, with a strong "
            "focus on data governance, investment in infrastructure and ongoing training and development. To wrap "
            "up, intelligent care systems are an enormous advancement in the healthcare area, empowering "
            "customized, proactive, and productive care conveyance. These systems can revolutionize patient care "
            "and enhance healthcare outcomes through the use of digital twins, predictive analytics, and other "
            "advanced technologies."
        , "body"),

        ("2.3 Intelligent Care Systems and Patient Management", "h2"),
        (
            "The next phase of the health care continuum is intelligent care systems, which use cutting-edge "
            "analytics, AI and digital solutions to deliver personalized, proactive care. These systems aim at "
            "enhancing patient handling through the use of predictive analysis, digital twins, and virtual patient "
            "modeling. A digital twin is a virtual model created using real-time data and advanced modelling "
            "techniques, which represents an actual object such as a patient. In the healthcare industry, digital "
            "twins can be utilized to model patient conditions and forecast the course of disease. Digital twins "
            "can integrate data from different sources such as medical records, wearable devices, and genetic "
            "information, offering a holistic picture of patient health [26]. Digital twins are an extension of "
            "virtual patient modelling, which is a simulation of patients' physiology and behaviour. These models "
            "can be used to test different treatment options and outcomes, and predict those outcomes to help "
            "design a personalized treatment plan. Virtual heart models can be used, for instance, to simulate "
            "the impact of different interventions on heart function."
        , "body"),
        (
            "An important aspect of the intelligent care systems is predictive analytics which helps develop "
            "interventions in disease management at an early stage. Historical and real time data can be used to "
            "analyze it with predictive models and identify the pattern and trend that can lead to health risks. "
            "This enables a medical practitioner to act in time before disease occurs to enhance patients' health "
            "and save health care costs. For instance, a predictive analytics system can detect patients that are "
            "at risk of being readmitted to the hospital after leaving and help develop strategies to prevent "
            "issues. Similarly, predictive models have been useful in detecting early signs of chronic diseases, "
            "such as diabetes and hypertension, and take appropriate preventive and treatment measures. Intelligent "
            "care systems also help to improve patient engagement through personalised recommendations and instant "
            "feedback. Patients can use patient-centred mobile apps to access their health records and be guided on "
            "lifestyle changes, health medication adherence and disease management. This gives the patients control "
            "over their health and improves their outcomes, thereby enhancing their satisfaction."
        , "body"),
        ("table1", "table"),

        (
            "From a management perspective, the intelligent care systems provide operational efficiencies by "
            "optimising the usage of resources and reduce costs. Analytics can help detect inefficiencies, optimize "
            "workflows, and enhance the delivery of services in healthcare organizations. Predictive models can "
            "help to optimize staffing levels, minimize waiting times, and enhance the flow of patients in "
            "healthcare facilities, for instance. While intelligent care systems offer numerous advantages, they "
            "also come with a number of difficulties, such as data privacy concerns, high implementation costs, "
            "and the requirement for qualified personnel. As indicated in Table 1, operational analytics contribute "
            "to lower costs, improved efficiency, and reduced wait times for patients. Solutions to these issues "
            "need to be integrated, with a strong focus on data governance, investment in infrastructure and "
            "ongoing training and development. Intelligent care systems represent a massive advancement in the "
            "healthcare delivery sector, enabling tailored, proactive, and effective care delivery. With the help "
            "of digital twins, predictive analytics, and other cutting-edge technologies, these systems have the "
            "potential to transform the way patient care was performed in the past and improve healthcare outcomes."
        , "body"),
    ]



# =============================================================================
# SECTION 3: Research Gap and Methodology
# =============================================================================

def get_section3():
    """Section 3: Research Gap and Methodology"""
    return [
        ("Section 3: Research Gap and Methodology", "h1"),
        ("3.1 Identifying the Research Gap", "h2"),
        (
            "Digital technologies, including Artificial Intelligence (AI), Internet of Things (IoT), and Big Data, "
            "have significantly revolutionized health care systems. Although significant progress has been made in "
            "the field of smart healthcare analytics and intelligent care systems, there are still some key research "
            "gaps that need to be addressed. One of the most visible drawbacks is the absence of integrated "
            "frameworks that incorporate technological, managerial and operational aspects in order to effectively "
            "implement. Previous research tends to focus on specific aspects like the use of AI for diagnosis or "
            "IoT for monitoring rather than exploring the potential for comprehensive integration into healthcare "
            "systems [27]. Ignored in the current studies is the need to pay more attention to the part of business "
            "education in the transformation of healthcare. Technological development has been studied extensively, "
            "however, little research has been done on the ways in which healthcare managers and business "
            "professionals can be prepared to effectively use these technologies. The seamless incorporation of AI "
            "and analytics into the healthcare sector demands a multi-disciplinary approach, combining technical "
            "skills with managerial acumen. Despite this, the business education curricula in place may not "
            "integrate any digital skills that are relevant to the healthcare sector, leading to an imbalance "
            "between studying and finding jobs in the field [28]."
        , "body"),

        (
            "Moreover, ethical and governance issues of smart healthcare systems have not been sufficiently tackled. "
            "There are concerns about data privacy and security, transparency of AI systems, and algorithmic biases "
            "in the use of AI and data analytics in healthcare. The challenges are recognised in many studies but "
            "are not addressed in a comprehensive manner. The absence of a focus on governance and ethics prevents "
            "the effective implementation of smart healthcare solutions because organizations need to meet "
            "regulatory standards and build trust with their patients [29]. Furthermore, there is limited empirical "
            "evidence to support proposed models and frameworks in health care environments. Numerous studies only "
            "provide conceptual models which are not evaluated in practice. This raises questions about how well "
            "these models can be applied in various healthcare settings and customized for specific needs. Thus, "
            "empirical studies are necessary to validate proposals of integrated models and frameworks, as well as "
            "to validate the use of models and frameworks [30]. A second significant lack is the small emphasis on "
            "risk management in smart healthcare systems. Digital technologies create new risks, such as cyber "
            "security, system failures and data breaches. These risks have not been fully addressed in existing "
            "research, or they are considered secondary. Risk management strategies should be part of a "
            "comprehensive framework to guarantee the reliability and sustainability of healthcare systems [31]. "
            "The effective implementation of smart healthcare analytics requires addressing these research gaps. "
            "The aim of this chapter is to fill these gaps by proposing an integrated framework in which "
            "technological, managerial and governance aspects will be taken into account, with special focus on "
            "the role of business education and of the management of risk."
        , "body"),
        ("3.2 Research Methodology", "h2"),
        (
            "This study is designed through the conceptual research methodology which is assisted by existing "
            "literature review and secondary data sources. This study is best suited for a conceptual research "
            "approach because it aims to create a theoretical model that combines various aspects of smart "
            "healthcare analytics. This approach enables building of the existing knowledge and identifying "
            "relationships between important variables [32]. The study adopts the method of comprehensive "
            "literature review as the main data collection technique. Key trends, challenges and best practices "
            "in smart healthcare analytics were identified through the analysis of relevant academic articles, "
            "conference papers, books and industry reports. The literature was obtained from the widely accepted "
            "databases of Scopus, Web of science and Google Scholar which assured the inclusion of good quality "
            "and peer-reviewed literature [33]."
        , "body"),

        (
            "Practical insights in the implementation of smart healthcare systems have been obtained from secondary "
            "data which is available in industry reports and case studies. These sources provide a good amount of "
            "information regarding the practical application, problem and results related to the theoretical "
            "analysis given [34]. The analytical approach is qualitative, content analysis type to identify the "
            "recurring themes and patterns in the literature. With this approach, information can be systematically "
            "categorized and the factors affecting the implementation of smart healthcare systems can be determined. "
            "Three major dimensions are considered: technological integration, managerial practices and governance "
            "frameworks [35]. A comparative study of the existing framework was done to strengthen the study. This "
            "includes assessing various models according to their comprehensiveness, scalability, and applicability. "
            "The results of this analysis were identified gaps and inform the proposed framework [36]."
        , "body"),
        (
            "The study also introduces a conceptual validation method, which includes the validation of the proposed "
            "framework with existing theories and best practices. This guarantees that the framework is theoretically "
            "strong and is in keeping with the existing knowledge in the field. While not validated empirically in "
            "this chapter, this structure has been developed to be flexible and adaptable for future empirical "
            "validation [37]. The research methodology in general is structured in order to design an integrated "
            "framework for smart healthcare analytics. The study's conceptual analysis and real-world insights "
            "provide a comprehensive view of the factors that contribute to the successful adoption and "
            "implementation of intelligent care systems."
        , "body"),
        ("fig3", "figure"),

        ("3.3 Framework Development", "h2"),
        (
            "With identified gaps in the research and methodology approach, this chapter suggests a complete "
            "framework for smart healthcare analytics. The structure combines aspects of technology (AI, IoT, Big "
            "Data analytics, and cloud computing) and management and governance to form a complete model of "
            "intelligent care systems. The proposed framework comprises four key layers: Data acquisition, Data "
            "processing, Decision-making and Governance. The data acquisition layer includes data coming from IoT "
            "devices, electronic health records, medical imaging systems etc. This layer provides access to good "
            "quality data to analyse [38]. The data processing layer is responsible for analyzing the data and "
            "generating insights using powerful analytics tools and AI algorithms. This includes machine learning "
            "models for predictive analytics, deep learning techniques for image analysis, and natural language "
            "processing for text data. These technologies can be integrated to enable thorough data analysis and "
            "to aid in decision making [39]."
        , "body"),
        (
            "The decision-making layer is about using the analysis of the data to make decisions for improving the "
            "outcomes of healthcare. This includes clinical decision support systems, personalized treatment plans, "
            "and operational optimization. Healthcare organisations can benefit from the use of data, which can help "
            "them to increase efficiency, lower costs, and delight their patients. A crucial aspect of the proposed "
            "framework is the incorporation of risk management and governance measures. This layer tackles the "
            "ethical, legal and regulatory issues arising in smart healthcare systems. It involves data privacy, "
            "security measures, and compliance with regulations. Furthermore, the system has measures in place for "
            "monitoring and evaluating its performance, which allows for continuous improvement and "
            "adaptation [40]."
        , "body"),

        (
            "Interoperability and scalability are also key themes of the framework. Healthcare systems need to be "
            "flexible and scalable to work in tandem with existing infrastructure and evolving demands. Standardized "
            "protocols and modular design make it more adaptable for implementation in various healthcare "
            "environments. The applicability of the framework is checked by comparing it with other frameworks and "
            "assessing it against criteria including comprehensiveness, flexibility and practicality. The findings "
            "show that the proposed framework is suitable to overcome the limitations of the existing models because "
            "it incorporates the technological, managerial, and governance components of the framework."
        , "body"),
        (
            "Moreover, the framework will facilitate the integration of business education in healthcare systems. "
            "It includes managerial and strategic aspects, so as to emphasize the importance of business "
            "professionals in the effective implementation of smart healthcare analytics. This complements the "
            "increasing demand for a multidisciplinary approach to health care management. In conclusion, the "
            "proposed framework provides a comprehensive approach to implementing smart healthcare analytics and "
            "intelligent care systems. It fills in important research gaps and brings together various aspects of "
            "the field, providing a valuable resource for researchers, practitioners, and policy makers. The "
            "framework should be empirically tested and used in various health care settings in future studies."
        , "body"),
        ("table2", "table"),
    ]



# =============================================================================
# SECTION 4: Analysis and Findings
# =============================================================================

def get_section4():
    """Section 4: Analysis and Findings"""
    return [
        ("Section 4: Analysis and Findings", "h1"),
        ("4.1 Analysis of Intelligent Care Systems", "h2"),
        (
            "With the advent of Artificial Intelligence (AI), Internet of Things (IoT) and advanced analytics in "
            "healthcare delivery, the adoption of intelligent care systems has accelerated all over the world. This "
            "has been showcased in several case studies, which illustrate the effective application of smart "
            "healthcare systems and their potential impact on patient care and operational efficiency. For instance, "
            "in the healthcare sector, AI-powered diagnostic platforms in hospitals employ machine learning "
            "algorithms to aid clinicians in early detection of diseases. These systems integrate patient "
            "information, such as medical records, imaging reports, and lab results to deliver precise diagnostic "
            "advice. AI diagnostic tools have been proven to have a significant impact on improving the accuracy "
            "of diagnosis and avoiding misdiagnosis [41]."
        , "body"),
        (
            "One example of a successful implementation of IoT solutions is remote patient monitoring systems. "
            "These use IoT devices to gather real-time health data. Wearable devices and connected sensors have "
            "been used in hospitals and healthcare providers to track patients who have chronic illnesses like "
            "cardiovascular diseases and diabetes. These systems provide continuous monitoring and minimize "
            "unnecessary hospital re-admissions and enhance patient outcomes [42]. Telemedicine platforms are also "
            "a major step forward in the use of intelligent care systems. Digital communication technologies enable "
            "healthcare providers to provide consultations, follow-up and treatment recommendations remotely. This "
            "strategy has been shown to be especially effective in times of global health emergencies, such as the "
            "COVID-19 pandemic, when in-person access to health care facilities was restricted [43]."
        , "body"),

        (
            "Different types of intelligent care are compared and their effectiveness varies according to their "
            "context of use. In certain areas of medicine like radiology and oncology, where the amount of data is "
            "vast, AI-based diagnostic solutions can prove to be very useful. Meanwhile, IoT-based monitoring "
            "systems are more appropriate for chronic diseases and the care of patients over an extended period of "
            "time [44]. Besides, the hybrid solutions involving AI, IoT, and Big Data analytics provide the most "
            "complete solutions. These comprehensive systems allow for the ability to collect, analyze and make "
            "decisions on patients' health data without any hassle, giving a holistic view of a patient's health. "
            "But data quality, interoperability, and user acceptance are critical elements for the success of these "
            "systems [45]. The analysis of intelligent care systems results in the conclusion that development of "
            "technology has made a great progress in delivering healthcare services, but the success of these "
            "systems relies on the context of the application and the integration between the various technologies "
            "used."
        , "body"),
        ("fig4", "figure"),
        ("4.2 Key Findings and Insights", "h2"),
        (
            "The analysis of intelligent care systems yields a number of important conclusions and lessons on the "
            "potential advantages, difficulties, and success factors of smart healthcare analytics. Patient outcomes "
            "is one of the main advantages of the smart healthcare analytics. Predictive Analytics and real-time "
            "monitoring allow healthcare providers to identify diseases early and take action in real time. This "
            "approach is proactive and helps to avoid complications and improve the quality of care [46]. Yet "
            "another great benefit is the improved operational efficiency. Intelligent systems execute repetitive "
            "functions, optimize resource use and minimize administration. For instance, AI-driven scheduling "
            "software can help to reduce waiting time, and data entry automation can ensure that information is "
            "accurate and error-free [47]. Another advantage of smart healthcare analytics is cost cuts. Healthcare "
            "organizations can optimize their operations and save money by minimizing waste in their health care "
            "use processes. Additionally, remote monitoring and telemedicine services help lower costs by minimizing "
            "the need for physical equipment and visits [48]."
        , "body"),

        (
            "However, there are still some barriers to the mass use of smart healthcare systems. One of the most "
            "serious obstacles is data privacy and security issues. Healthcare systems are increasingly relying on "
            "digital technologies, which rely on the collection and storage of sensitive patient information, making "
            "them vulnerable to cyberattacks and data breaches [49]. Another is that there are no interoperabilities "
            "between various healthcare systems. Legacy systems are outdated, difficult to integrate with modern "
            "technologies, and are used by many health organizations, which can hinder data sharing and integration. "
            "This disintegration has a negative impact on the efficiency of smart healthcare analytics and on the "
            "creation of integrated healthcare systems [50]. Also, the expense of implementation and the requirement "
            "of the skilled workforce are major challenges. To successfully implement intelligent care systems, "
            "healthcare organizations need to invest in infrastructure, technology, and training. Healthcare "
            "professionals' and patients' resistance to change is another factor impacting on the uptake of "
            "these technologies."
        , "body"),
        (
            "The analysis pinpoints key factors of the successful implementation of smart healthcare systems. These "
            "include robust data governance frameworks, investments in infrastructure and training, and strong "
            "leadership and strategic vision. In addition, data quality and interoperability are crucial factors for "
            "the effectiveness of intelligent care systems. In addition, challenges and opportunities for innovation "
            "can be addressed only through stakeholder cooperation, which involves healthcare providers, technology "
            "developers, and policymakers. Considering these factors, healthcare organizations can reap the maximum "
            "benefits from smart healthcare analytics and make sustainable enhancements in healthcare "
            "delivery [51]."
        , "body"),

        ("4.3 Practical Applications", "h2"),
        (
            "Smart healthcare analytics has many real-life applications, all of which have the potential to "
            "revolutionize healthcare delivery. A popular use case is the remote patient monitoring systems. These "
            "systems comprise Internet of Things (IoT) devices and wearable sensors that gather real-time "
            "health-related data, allowing for continuous health monitoring of patients. This is a great method for "
            "chronic diseases which can enable early recognition of complications and prompt action. Another "
            "application of smart healthcare systems is predictive analytics. Predictive models can be used to "
            "identify patients using historical and real-time data who are at risk of developing certain conditions. "
            "This helps health practitioners take preventive measures, thereby lowering the chances of disease "
            "progression. Predictive analytics, for instance, can also be leveraged to determine patients who are "
            "at risk of heart disease and take them to the next level of intervention and lifestyle changes."
        , "body"),
        (
            "An application of intelligent care systems, which is particularly important, is AI-assisted emergency "
            "response system. These systems are designed to leverage real-time data and sophisticated algorithms to "
            "optimize resource allocation and enhance response times in emergencies. AI can, for example, process "
            "traffic and patient information to identify the shortest routes for ambulances and prioritize patients "
            "according to their severity. Moreover, smart healthcare analytics is applied in hospital management "
            "for the optimization of resources. Predictive models can provide estimates of patient admissions, which "
            "helps hospitals to make better use of staff and resources. This means fewer people are crowded into the "
            "same care and the quality of care is enhanced."
        , "body"),

        (
            "Another use is personalized medicine, in which treatment is customized for the specific patient based "
            "on their genetic, environmental and lifestyle factors. Through AI and data analysis, personalized "
            "treatment options are identified, enhancing the effectiveness of treatment and patient satisfaction. "
            "In conclusion, the use of smart healthcare analytics offers numerous practical applications that can "
            "help to optimize patient care, increase efficiency, and lower healthcare costs. With the help of "
            "cutting-edge technologies, healthcare providers can provide more personalized, proactive, and "
            "efficient care. The overall applications in smart healthcare analytics point to its use for better "
            "patient outcomes, increased efficiency, and lower costs. Healthcare organizations can provide "
            "personalized, proactive, and efficient care with the use of advanced technologies."
        , "body"),
        ("table3", "table"),
    ]



# =============================================================================
# SECTION 5: Conclusion and Future Directions
# =============================================================================

def get_section5():
    """Section 5: Conclusion and Future Directions"""
    return [
        ("Section 5: Conclusion and Future Directions", "h1"),
        ("5.1 Summary and Conclusion", "h2"),
        (
            "In this chapter, the importance of smart healthcare analytics and intelligent care systems in the "
            "context of digital transformation in healthcare has been discussed. The main goal was to envision how "
            "advanced technologies, such as Artificial Intelligence (AI), Internet of Things (IoT), and Big Data, "
            "can improve the provision of healthcare services, in addition to tackling the gaps in implementation "
            "frameworks, business education and governance challenges. The analysis has pointed out that the "
            "healthcare systems are shifting from reactive, traditional, to proactive, data-driven, and "
            "patient-centric models. By leveraging AI-powered data collection and analysis, intelligent care "
            "systems have proven to be a significant step toward better diagnostics, efficiency, and individual "
            "treatment options. The healthcare landscape has been further enhanced by the adoption of IoT devices "
            "and cloud computing, which enable real-time monitoring and data sharing."
        , "body"),
        (
            "The results also highlight the importance of technological developments being effective, depending on "
            "how integrated they are, the quality of the data and user acceptance. To address this issue, the "
            "proposed framework in this study aims to integrate technological, managerial, and governance "
            "considerations, fostering a comprehensive approach to the implementation of smart healthcare. Overall, "
            "AI and related digital technologies are revolutionizing health care systems. Not only are they "
            "enhancing patient care but they are also shaping the future of healthcare service delivery and "
            "management. The implementation of these technologies, however, demands a balanced approach, taking "
            "into account technical, ethical, and organizational issues."
        , "body"),

        ("5.2 Implications", "h2"),
        (
            "The results of this chapter have several significance for the various theoretical, practical, and "
            "educational areas. On a theoretical level, this study has a contribution to the existing literature "
            "in that it introduces an integrated framework for smart healthcare analytics. This framework, however, "
            "differs from traditional models that focus on separate technologies by emphasizing the interconnectedness "
            "of AI, IoT, analytics, and governance. It also emphasizes the need for the integration of risk "
            "management and ethical aspects in health systems. This interdisciplinary approach is also a stepping "
            "stone for further studies in the future for digital healthcare and intelligent systems."
        , "body"),
        (
            "From a practical perspective, smart healthcare analytics has the potential to be a huge advantage to "
            "healthcare practitioners and organizations. Adopting intelligent care systems can result in better "
            "patient care, lower costs of operation, and greater efficiency. For instance, predictive analytics can "
            "help with early detection of disease, and remote monitoring systems can minimize hospital readmissions. "
            "But there are other problems to overcome, including data security, interoperability, and change "
            "resistance. Key to successful implementation is strategic planning, investment in infrastructure and "
            "ongoing training."
        , "body"),
        (
            "This research has clear educational implications in the business and health care curriculum. Today, the "
            "healthcare sector is increasingly technologically dependent, and there is a growing demand for technical "
            "and managerial skills. To equip students for the changing landscape of the healthcare sector, business "
            "education programs must incorporate courses across the three key areas of AI, data analytics, and "
            "digital health management. Likewise, it is essential to have some aspects of data science and management "
            "also included in healthcare education to promote interdisciplinary skills. This synergy between the "
            "needs of education and industry will contribute to the gap between theory and practice."
        , "body"),

        ("5.3 Future Scope and Limitations", "h2"),
        (
            "Although significant contributions are made in this study, there are some limitations that should be "
            "noted. The first point is that the research is mostly conceptual and secondary sources of information "
            "are used. This is good idea but hasn't been validated empirically in a real healthcare environment. "
            "Further research is recommended to test the proposed framework empirically and explore the "
            "effectiveness of the framework in various healthcare contexts. Second, the study is general, rather "
            "than specific, in that it does not take into account any variations at regional or institutional "
            "levels. The proposed framework may have implications for the applicability to various healthcare "
            "systems due to differences in infrastructure, regulation, and resources. Further studies are warranted "
            "on context-specific models that reflect the specific challenges and needs of various regions and "
            "health care providers."
        , "body"),
        (
            "Another limitation is the limited exploration of patient perspectives. Although the study focuses on "
            "patient-centred care, the experiences and acceptance of the intelligent care system by the patients "
            "are not analyzed in detail. Studies ought to consider patient feedback and behavioural analysis to "
            "make sure these systems are designed with user requirements in mind."
        , "body"),
        (
            "In the future, a number of new technologies have the potential to further advance smart healthcare "
            "analytics. Blockchain technology has the potential to improve data security and transparency, and edge "
            "computing can help speed up data processing and decision-making. Furthermore, 4-Dimensional CT and "
            "digital twins, virtual patient models, could further enhance personalised medicine and treatment "
            "planning. Additionally, further studies are needed to address ethical and governance issues surrounding "
            "the use of AI in healthcare. Creating explainable and transparent AI models is crucial for fostering "
            "trust between healthcare providers and patients. There is a need for policymaking and research "
            "collaboration to develop policies and regulations that promote the responsible use of digital "
            "technologies in healthcare."
        , "body"),

        (
            "Last but not least, the interdisciplinary cooperation will be of great importance for future smart "
            "healthcare systems. The synergy among healthcare providers, data scientists, engineers, and business "
            "professionals is critical for the creation of innovative solutions and addressing current challenges. "
            "Such collaboration can unlock the potential of intelligent care systems, leading to more sustainable "
            "enhancements in healthcare delivery within the healthcare industry. In summary, while this study "
            "provides a comprehensive understanding of smart healthcare analytics and intelligent care systems, "
            "it also highlights the need for further research and development. The identified limitations and the "
            "opportunities for future study identified in this research will help with the ongoing evolution of "
            "intelligent healthcare systems."
        , "body"),
    ]



# =============================================================================
# TABLES
# =============================================================================

def get_table1_data():
    """Table 1: Components and Benefits of Intelligent Care Systems"""
    headers = ["System Component", "Key Technologies", "Patient Benefits", "Organizational Benefits"]
    rows = [
        ["Digital Twins & Virtual Modeling", "IoT, AI, Real-time Analytics, Simulation",
         "Personalized treatment, simulated interventions", "Improved care planning, reduced complications"],
        ["Predictive Analytics & Remote Monitoring", "Machine Learning, Wearable Devices, Cloud Computing",
         "Early intervention, chronic disease management", "Reduced readmissions, cost savings"],
        ["Patient Engagement & Operational Analytics", "Mobile Apps, NLP, Optimization Algorithms",
         "Empowered patients, better satisfaction", "Lower costs, improved efficiency, reduced wait times"],
    ]
    return headers, rows


def get_table2_data():
    """Table 2: Proposed Framework for Smart Healthcare Analytics"""
    headers = ["Framework Layer", "Key Components", "Technologies & Tools", "Primary Function"]
    rows = [
        ["Data Acquisition", "IoT devices, EHRs, Medical Imaging, Wearables, Lab Systems",
         "Sensors, Connected Devices, APIs, HL7/FHIR Standards",
         "Collecting and integrating diverse healthcare data from multiple sources"],
        ["Data Processing", "Data Storage, Data Cleaning, Integration, AI/ML Analysis",
         "Cloud Computing, Machine Learning, Deep Learning, NLP",
         "Storing, cleaning, and analyzing data to generate actionable insights"],
        ["Decision-Making", "Clinical Decision Support, Treatment Planning, Operations Management",
         "Predictive Models, Dashboards, Mobile Apps, Alert Systems",
         "Supporting clinical decisions and optimizing healthcare operations"],
        ["Governance", "Data Privacy, Security, Compliance, Ethics, Risk Management",
         "Encryption, Access Controls, Audit Trails, Policies, Training",
         "Ensuring ethical, legal, and regulatory compliance across all layers"],
    ]
    return headers, rows



def get_table3_data():
    """Table 3: Key Findings and Insights on Intelligent Care Systems"""
    headers = ["Benefits", "Challenges", "Success Factors", "Practical Applications"]
    rows = [
        ["Improved patient outcomes through early detection and proactive intervention",
         "Data privacy and security concerns, cyberattacks, data breaches",
         "Strong leadership and strategic vision",
         "Remote patient monitoring for chronic disease management"],
        ["Enhanced operational efficiency through automation and optimization",
         "Lack of interoperability and integration with legacy systems",
         "Investment in infrastructure, technology, and training",
         "Predictive analytics for early disease detection and prevention"],
        ["Significant cost reduction through efficiency gains and reduced hospital visits",
         "High implementation costs and need for skilled professionals",
         "Robust data governance and quality management frameworks",
         "AI-driven emergency response and resource optimization"],
        ["Better patient engagement and satisfaction through personalized care",
         "Resistance to change among healthcare professionals and patients",
         "Collaboration among stakeholders and continuous innovation",
         "Personalized medicine and tailored treatment planning"],
    ]
    return headers, rows



# =============================================================================
# REFERENCES
# =============================================================================

def get_references():
    """References [1]-[51] for Smart Healthcare Analytics chapter."""
    return [
        "[1] Raghupathi, W., & Raghupathi, V. (2014). Big data analytics in healthcare: Promise and potential. Health Information Science and Systems, 2(1), 3. https://doi.org/10.1186/2047-2501-2-3",
        "[2] Kruse, C. S., Stein, A., Thomas, H., & Kaur, H. (2018). The use of electronic health records to support population health: A systematic review of the literature. Journal of Medical Systems, 42(11), 214. https://doi.org/10.1007/s10916-018-1075-6",
        "[3] Dash, S., Shakyawar, S. K., Sharma, M., & Kaushik, S. (2019). Big data in healthcare: Management, analysis and future prospects. Journal of Big Data, 6(1), 54. https://doi.org/10.1186/s40537-019-0217-0",
        "[4] Jiang, F., Jiang, Y., Zhi, H., Dong, Y., Li, H., Ma, S., Wang, Y., Dong, Q., Shen, H., & Wang, Y. (2017). Artificial intelligence in healthcare: Past, present and future. Stroke and Vascular Neurology, 2(4), 230-243. https://doi.org/10.1136/svn-2017-000101",
        "[5] Esteva, A., Robicquet, A., Ramsundar, B., Kuleshov, V., DePristo, M., Chou, K., Cui, C., Corrado, G., Thrun, S., & Dean, J. (2019). A guide to deep learning in healthcare. Nature Medicine, 25(1), 24-29. https://doi.org/10.1038/s41591-018-0316-z",
        "[6] Islam, S. M. R., Kwak, D., Kabir, M. H., Hossain, M., & Kwak, K. S. (2015). The Internet of Things for health care: A comprehensive survey. IEEE Access, 3, 678-708. https://doi.org/10.1109/ACCESS.2015.2437951",
        "[7] Mehta, N., & Pandit, A. (2018). Concurrence of big data analytics and healthcare: A systematic review. International Journal of Medical Informatics, 114, 57-65. https://doi.org/10.1016/j.ijmedinf.2018.03.013",
        "[8] Reddy, S., Fox, J., & Purohit, M. P. (2019). Artificial intelligence-enabled healthcare delivery. Journal of the Royal Society of Medicine, 112(1), 22-28. https://doi.org/10.1177/0141076818815510",

        "[9] Cutler, D. M. (2020). Reducing administrative costs in U.S. health care. The Hamilton Project, Brookings Institution. https://www.brookings.edu/research/reducing-administrative-costs",
        "[10] Enthoven, A. C. (2009). Integrated delivery systems: The cure for fragmentation. American Journal of Managed Care, 15(10), S284-S290.",
        "[11] Hamburg, M. A., & Collins, F. S. (2010). The path to personalized medicine. New England Journal of Medicine, 363(4), 301-304. https://doi.org/10.1056/NEJMp1006304",
        "[12] Bates, D. W., Saria, S., Ohno-Machado, L., Shah, A., & Escobar, G. (2014). Big data in health care: Using analytics to identify and manage high-risk and high-cost patients. Health Affairs, 33(7), 1123-1131. https://doi.org/10.1377/hlthaff.2014.0041",
        "[13] Topol, E. J. (2019). High-performance medicine: The convergence of human and artificial intelligence. Nature Medicine, 25(1), 44-56. https://doi.org/10.1038/s41591-018-0300-7",
        "[14] Torous, J., Andersson, G., Bertagnoli, A., Christensen, H., Cuijpers, P., Firth, J., Haim, A., Hsin, H., Hollis, C., Lewis, S., & Mohr, D. C. (2019). Towards a consensus around standards for smartphone apps and digital mental health. World Psychiatry, 18(1), 97-98. https://doi.org/10.1002/wps.20592",
        "[15] Granja, C., Janssen, W., & Johansen, M. A. (2018). Factors determining the success and failure of eHealth interventions: Systematic review of the literature. Journal of Medical Internet Research, 20(5), e10235. https://doi.org/10.2196/10235",
        "[16] Agarwal, R., Gao, G., DesRoches, C., & Jha, A. K. (2010). Research commentary\u2014The digital transformation of healthcare: Current status and the road ahead. Information Systems Research, 21(4), 796-809. https://doi.org/10.1287/isre.1100.0327",
        "[17] Wamba, S. F., Akter, S., Edwards, A., Chopin, G., & Gnanzou, D. (2015). How 'big data' can make big impact: Findings from a systematic review and a longitudinal case study. International Journal of Production Economics, 165, 234-246. https://doi.org/10.1016/j.ijpe.2014.12.031",

        "[18] Dias, D., & Cunha, J. P. S. (2018). Wearable health devices\u2014Vital sign monitoring, systems and technologies. Sensors, 18(8), 2414. https://doi.org/10.3390/s18082414",
        "[19] Dang, L. M., Piran, M. J., Han, D., Min, K., & Moon, H. (2019). A survey on Internet of Things and cloud computing for healthcare. Electronics, 8(7), 768. https://doi.org/10.3390/electronics8070768",
        "[20] Baker, S. B., Xiang, W., & Atkinson, I. (2017). Internet of Things for smart healthcare: Technologies, challenges, and opportunities. IEEE Access, 5, 26521-26544. https://doi.org/10.1109/ACCESS.2017.2775180",
        "[21] Griebel, L., Prokosch, H. U., K\u00f6pcke, F., Toddenroth, D., Christoph, J., Leb, I., Engel, I., & Sedlmayr, M. (2015). A scoping review of cloud computing in healthcare. BMC Medical Informatics and Decision Making, 15(1), 17. https://doi.org/10.1186/s12911-015-0145-7",
        "[22] Sultan, N. (2014). Making use of cloud computing for healthcare provision: Opportunities and challenges. International Journal of Information Management, 34(2), 177-184. https://doi.org/10.1016/j.ijinfomgt.2013.12.011",
        "[23] Majumder, S., Mondal, T., & Deen, M. J. (2017). Wearable sensors for remote health monitoring. Sensors, 17(1), 130. https://doi.org/10.3390/s17010130",
        "[24] Dimitrov, D. V. (2016). Medical Internet of Things and big data in healthcare. Healthcare Informatics Research, 22(3), 156-163. https://doi.org/10.4258/hir.2016.22.3.156",
        "[25] Corral-Acero, J., Margara, F., Marber, M., Schotten, U., Smeeth, L., Sherwin, S. J., & Lamata, P. (2020). The 'Digital Twin' to enable the vision of precision cardiology. European Heart Journal, 41(48), 4556-4564. https://doi.org/10.1093/eurheartj/ehaa159",
        "[26] Kamel Boulos, M. N., & Zhang, P. (2021). Digital twins: From personalised medicine to precision public health. Journal of Personalized Medicine, 11(8), 745. https://doi.org/10.3390/jpm11080745",

        "[27] Davenport, T., & Kalakota, R. (2019). The potential for artificial intelligence in healthcare. Future Healthcare Journal, 6(2), 94-98. https://doi.org/10.7861/futurehosp.6-2-94",
        "[28] Wartman, S. A., & Combs, C. D. (2018). Medical education must move from the information age to the age of artificial intelligence. Academic Medicine, 93(8), 1107-1109. https://doi.org/10.1097/ACM.0000000000002044",
        "[29] Char, D. S., Shah, N. H., & Magnus, D. (2018). Implementing machine learning in health care\u2014Addressing ethical challenges. New England Journal of Medicine, 378(11), 981-983. https://doi.org/10.1056/NEJMp1714229",
        "[30] Kelly, C. J., Karthikesalingam, A., Suleyman, M., Corrado, G., & King, D. (2019). Key challenges for delivering clinical impact with artificial intelligence. BMC Medicine, 17(1), 195. https://doi.org/10.1186/s12916-019-1426-2",
        "[31] He, J., Baxter, S. L., Xu, J., Xu, J., Zhou, X., & Zhang, K. (2019). The practical implementation of artificial intelligence technologies in medicine. Nature Medicine, 25(1), 30-36. https://doi.org/10.1038/s41591-018-0307-0",
        "[32] Jabareen, Y. (2009). Building a conceptual framework: Philosophy, definitions, and procedure. International Journal of Qualitative Methods, 8(4), 49-62. https://doi.org/10.1177/160940690900800406",
        "[33] Snyder, H. (2019). Literature review as a research methodology: An overview and guidelines. Journal of Business Research, 104, 333-339. https://doi.org/10.1016/j.jbusres.2019.07.039",
        "[34] Yin, R. K. (2018). Case study research and applications: Design and methods (6th ed.). Sage Publications.",
        "[35] Hsieh, H. F., & Shannon, S. E. (2005). Three approaches to qualitative content analysis. Qualitative Health Research, 15(9), 1277-1288. https://doi.org/10.1177/1049732305276687",
        "[36] Grant, M. J., & Booth, A. (2009). A typology of reviews: An analysis of 14 review types and associated methodologies. Health Information & Libraries Journal, 26(2), 91-108. https://doi.org/10.1111/j.1471-1842.2009.00848.x",
        "[37] Whetten, D. A. (1989). What constitutes a theoretical contribution? Academy of Management Review, 14(4), 490-495. https://doi.org/10.5465/amr.1989.4308371",

        "[38] Kruse, C. S., Goswamy, R., Raval, Y., & Marber, S. (2016). Challenges and opportunities of big data in health care: A systematic review. JMIR Medical Informatics, 4(4), e38. https://doi.org/10.2196/medinform.5359",
        "[39] Obermeyer, Z., & Emanuel, E. J. (2016). Predicting the future\u2014Big data, machine learning, and clinical medicine. New England Journal of Medicine, 375(13), 1216-1219. https://doi.org/10.1056/NEJMp1606181",
        "[40] Price, W. N., & Cohen, I. G. (2019). Privacy in the age of medical big data. Nature Medicine, 25(1), 37-43. https://doi.org/10.1038/s41591-018-0272-7",
        "[41] Rajkomar, A., Dean, J., & Kohane, I. (2019). Machine learning in medicine. New England Journal of Medicine, 380(14), 1347-1358. https://doi.org/10.1056/NEJMra1814259",
        "[42] Noah, B., Keller, M. S., Mosadeghi, S., Ber, L., Jeon, S. Y., Shin, B., Yom-Tov, E., Steinberg, D., Golber, D. M., & Spiegel, B. M. (2018). Impact of remote patient monitoring on clinical outcomes: An updated meta-analysis. NPJ Digital Medicine, 1(1), 20172. https://doi.org/10.1038/s41746-017-0002-4",
        "[43] Portnoy, J., Waller, M., & Elliott, T. (2020). Telemedicine in the era of COVID-19. Journal of Allergy and Clinical Immunology: In Practice, 8(5), 1489-1491. https://doi.org/10.1016/j.jaip.2020.03.008",
        "[44] Hosny, A., Parmar, C., Quackenbush, J., Schwartz, L. H., & Aerts, H. J. W. L. (2018). Artificial intelligence in radiology. Nature Reviews Cancer, 18(8), 500-510. https://doi.org/10.1038/s41568-018-0016-5",
        "[45] Murdoch, T. B., & Detsky, A. S. (2013). The inevitable application of big data to health care. JAMA, 309(13), 1351-1352. https://doi.org/10.1001/jama.2013.393",

        "[46] Miotto, R., Wang, F., Wang, S., Jiang, X., & Dudley, J. T. (2018). Deep learning for healthcare: Review, opportunities and challenges. Briefings in Bioinformatics, 19(6), 1236-1246. https://doi.org/10.1093/bib/bbx044",
        "[47] Shickel, B., Tighe, P. J., Bihorac, A., & Rashidi, P. (2018). Deep EHR: A survey of recent advances in deep learning techniques for electronic health record analysis. IEEE Journal of Biomedical and Health Informatics, 22(5), 1589-1604. https://doi.org/10.1109/JBHI.2017.2767063",
        "[48] Kvedar, J. C., Colman, C., & Cella, G. (2016). The Internet of Healthy Things. Partners Connected Health. Boston, MA.",
        "[49] Abouelmehdi, K., Beni-Hessane, A., & Khaloufi, H. (2018). Big healthcare data: Preserving security and privacy. Journal of Big Data, 5(1), 1. https://doi.org/10.1186/s40537-017-0110-7",
        "[50] Lehne, M., Sass, J., Essenwanger, A., Schepers, J., & Thun, S. (2019). Why digital medicine depends on interoperability. NPJ Digital Medicine, 2(1), 79. https://doi.org/10.1038/s41746-019-0158-1",
        "[51] Krittanawong, C., Zhang, H., Wang, Z., Aydar, M., & Kitai, T. (2017). Artificial intelligence in precision cardiovascular medicine. Journal of the American College of Cardiology, 69(21), 2657-2664. https://doi.org/10.1016/j.jacc.2017.03.571",
    ]



# =============================================================================
# DOCUMENT ASSEMBLY
# =============================================================================

def build_body():
    """Assemble all body elements."""
    body = []

    # Title page
    body.append(make_paragraph("", spacing_after=400))
    body.append(make_paragraph(
        "Transforming Business Education through Artificial Intelligence",
        bold=True, size=28, alignment='center', spacing_after=200))
    body.append(make_paragraph("", spacing_after=200))
    body.append(make_paragraph(
        "Smart Healthcare Analytics and Intelligent Care Systems",
        bold=True, size=36, alignment='center', spacing_after=400))
    body.append(make_paragraph("", spacing_after=200))
    body.append(make_paragraph(
        "ABSTRACT", bold=True, size=24, alignment='center', spacing_after=200))
    body.append(make_paragraph(
        "This chapter explores the transformative role of smart healthcare analytics and "
        "intelligent care systems in modern healthcare delivery. It examines how advanced "
        "technologies including Artificial Intelligence (AI), Internet of Things (IoT), and "
        "Big Data analytics are reshaping healthcare from reactive, traditional models to "
        "proactive, data-driven, and patient-centric systems. The chapter presents a "
        "comprehensive framework integrating technological, managerial, and governance "
        "dimensions for effective implementation of intelligent care systems. Through analysis "
        "of case studies and existing literature, the study identifies key benefits, challenges, "
        "and critical success factors for smart healthcare adoption. The implications for "
        "business education are highlighted, emphasizing the need for interdisciplinary "
        "curricula that combine AI, data analytics, and healthcare management skills to prepare "
        "future leaders for the evolving healthcare landscape.",
        size=22, italic=True, spacing_after=200, alignment='both'))

    body.append(make_paragraph(
        "Keywords: Smart Healthcare Analytics, Intelligent Care Systems, Artificial Intelligence, "
        "Internet of Things, Big Data, Predictive Analytics, Digital Twins, Business Education, "
        "Healthcare Management, Data-Driven Decision Making",
        bold=True, size=20, spacing_after=400))

    # --- SECTION 1 ---
    body.append(page_break())
    for item in get_section1():
        text, ptype = item[0], item[1]
        if ptype == "h1":
            body.append(make_heading(text, 1))
        elif ptype == "h2":
            body.append(make_heading(text, 2))
        elif ptype == "h3":
            body.append(make_heading(text, 3))
        elif ptype == "figure":
            if text == "fig1":
                body.extend(fig_placeholder(1,
                    "Smart healthcare analytics integrating AI, IoT, and Big Data for improved outcomes.",
                    "Integration of AI, IoT, and Big Data forming the foundational triad of smart healthcare analytics"))
        else:
            body.append(make_paragraph(text, size=24, font='Times New Roman',
                                       alignment='both', line_spacing=360))

    # --- SECTION 2 ---
    body.append(page_break())
    for item in get_section2():
        text, ptype = item[0], item[1]
        if ptype == "h1":
            body.append(make_heading(text, 1))
        elif ptype == "h2":
            body.append(make_heading(text, 2))
        elif ptype == "h3":
            body.append(make_heading(text, 3))
        elif ptype == "figure":
            if text == "fig2":
                body.extend(fig_placeholder(2,
                    "Smart healthcare system framework showing the flow from data collection through AI analytics to improved patient outcomes.",
                    "Data Collection -> Cloud Processing -> AI Analytics -> Clinical Decision Support -> Improved Patient Outcomes"))
        elif ptype == "table":
            if text == "table1":
                body.append(make_paragraph(
                    "Table 1: Components and Benefits of Intelligent Care Systems",
                    bold=True, size=22, alignment='center', spacing_before=240, spacing_after=120))
                h, r = get_table1_data()
                body.append(make_table(h, r))
                body.append(make_paragraph("", spacing_after=240))
        else:
            body.append(make_paragraph(text, size=24, font='Times New Roman',
                                       alignment='both', line_spacing=360))


    # --- SECTION 3 ---
    body.append(page_break())
    for item in get_section3():
        text, ptype = item[0], item[1]
        if ptype == "h1":
            body.append(make_heading(text, 1))
        elif ptype == "h2":
            body.append(make_heading(text, 2))
        elif ptype == "h3":
            body.append(make_heading(text, 3))
        elif ptype == "figure":
            if text == "fig3":
                body.extend(fig_placeholder(3,
                    "Methodology framework depicting literature review, content analysis, framework development, and validation phases.",
                    "Literature Review -> Content Analysis -> Framework Development -> Conceptual Validation"))
        elif ptype == "table":
            if text == "table2":
                body.append(make_paragraph(
                    "Table 2: Proposed Framework for Smart Healthcare Analytics and Intelligent Care Systems",
                    bold=True, size=22, alignment='center', spacing_before=240, spacing_after=120))
                h, r = get_table2_data()
                body.append(make_table(h, r))
                body.append(make_paragraph("", spacing_after=240))
        else:
            body.append(make_paragraph(text, size=24, font='Times New Roman',
                                       alignment='both', line_spacing=360))

    # --- SECTION 4 ---
    body.append(page_break())
    for item in get_section4():
        text, ptype = item[0], item[1]
        if ptype == "h1":
            body.append(make_heading(text, 1))
        elif ptype == "h2":
            body.append(make_heading(text, 2))
        elif ptype == "h3":
            body.append(make_heading(text, 3))
        elif ptype == "figure":
            if text == "fig4":
                body.extend(fig_placeholder(4,
                    "Intelligent care systems integrating AI diagnostics, remote monitoring, telemedicine, and analytics for better outcomes.",
                    "AI Diagnostics + Remote Monitoring + Telemedicine + Analytics -> Enhanced Patient Care & Operational Efficiency"))
        elif ptype == "table":
            if text == "table3":
                body.append(make_paragraph(
                    "Table 3: Key Findings and Insights on Intelligent Care Systems",
                    bold=True, size=22, alignment='center', spacing_before=240, spacing_after=120))
                h, r = get_table3_data()
                body.append(make_table(h, r))
                body.append(make_paragraph("", spacing_after=240))
        else:
            body.append(make_paragraph(text, size=24, font='Times New Roman',
                                       alignment='both', line_spacing=360))


    # --- SECTION 5 ---
    body.append(page_break())
    for item in get_section5():
        text, ptype = item[0], item[1]
        if ptype == "h1":
            body.append(make_heading(text, 1))
        elif ptype == "h2":
            body.append(make_heading(text, 2))
        elif ptype == "h3":
            body.append(make_heading(text, 3))
        else:
            body.append(make_paragraph(text, size=24, font='Times New Roman',
                                       alignment='both', line_spacing=360))

    # --- REFERENCES ---
    body.append(page_break())
    body.append(make_heading("REFERENCES", 1))
    for ref in get_references():
        body.append(make_paragraph(ref, size=20, font='Times New Roman'))

    return body



# =============================================================================
# OOXML FILE GENERATION
# =============================================================================

def element_to_string(element):
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + \
           ET.tostring(element, encoding='unicode')


def get_styles_xml():
    styles = ET.Element(f'{{{W_NS}}}styles')
    docDef = ET.SubElement(styles, f'{{{W_NS}}}docDefaults')
    rPrDef = ET.SubElement(docDef, f'{{{W_NS}}}rPrDefault')
    rPr = ET.SubElement(rPrDef, f'{{{W_NS}}}rPr')
    ET.SubElement(rPr, f'{{{W_NS}}}rFonts',
                  {f'{{{W_NS}}}ascii': 'Times New Roman', f'{{{W_NS}}}hAnsi': 'Times New Roman'})
    ET.SubElement(rPr, f'{{{W_NS}}}sz', {f'{{{W_NS}}}val': '24'})
    ET.SubElement(rPr, f'{{{W_NS}}}szCs', {f'{{{W_NS}}}val': '24'})
    pPrDef = ET.SubElement(docDef, f'{{{W_NS}}}pPrDefault')
    pPr = ET.SubElement(pPrDef, f'{{{W_NS}}}pPr')
    ET.SubElement(pPr, f'{{{W_NS}}}spacing',
                  {f'{{{W_NS}}}after': '200', f'{{{W_NS}}}line': '360',
                   f'{{{W_NS}}}lineRule': 'auto'})
    ET.SubElement(pPr, f'{{{W_NS}}}jc', {f'{{{W_NS}}}val': 'both'})

    for lvl, sz, color in [(1, '32', '1F4E79'), (2, '28', '2E75B6'), (3, '24', '333333')]:
        s = ET.SubElement(styles, f'{{{W_NS}}}style',
                          {f'{{{W_NS}}}type': 'paragraph',
                           f'{{{W_NS}}}styleId': f'Heading{lvl}'})
        ET.SubElement(s, f'{{{W_NS}}}name', {f'{{{W_NS}}}val': f'heading {lvl}'})
        sp = ET.SubElement(s, f'{{{W_NS}}}pPr')
        ET.SubElement(sp, f'{{{W_NS}}}spacing',
                      {f'{{{W_NS}}}before': '360', f'{{{W_NS}}}after': '120'})
        sr = ET.SubElement(s, f'{{{W_NS}}}rPr')
        ET.SubElement(sr, f'{{{W_NS}}}b')
        ET.SubElement(sr, f'{{{W_NS}}}sz', {f'{{{W_NS}}}val': sz})
        ET.SubElement(sr, f'{{{W_NS}}}color', {f'{{{W_NS}}}val': color})

    tg = ET.SubElement(styles, f'{{{W_NS}}}style',
                       {f'{{{W_NS}}}type': 'table', f'{{{W_NS}}}styleId': 'TableGrid'})
    ET.SubElement(tg, f'{{{W_NS}}}name', {f'{{{W_NS}}}val': 'Table Grid'})
    return styles



def create_figure_pngs():
    """Create placeholder PNG figures for the chapter."""
    os.makedirs('/projects/sandbox/AMMAN/healthcare_figures', exist_ok=True)

    figures = [
        {
            'filename': '/projects/sandbox/AMMAN/healthcare_figures/Figure_1.png',
            'width': 200, 'height': 120,
            'color': (220, 235, 250),
        },
        {
            'filename': '/projects/sandbox/AMMAN/healthcare_figures/Figure_2.png',
            'width': 200, 'height': 120,
            'color': (235, 245, 220),
        },
        {
            'filename': '/projects/sandbox/AMMAN/healthcare_figures/Figure_3.png',
            'width': 200, 'height': 120,
            'color': (250, 235, 220),
        },
        {
            'filename': '/projects/sandbox/AMMAN/healthcare_figures/Figure_4.png',
            'width': 200, 'height': 120,
            'color': (235, 220, 245),
        },
    ]

    for fig in figures:
        create_png(fig['width'], fig['height'], fig['color'], fig['filename'])



def create_png(width, height, color_rgb, filename):
    """Create a simple PNG image with colored background."""
    r, g, b = color_rgb
    w, h = width, height

    def make_png(w, h, pixels):
        def chunk(chunk_type, data):
            c = chunk_type + data
            crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
            return struct.pack('>I', len(data)) + c + crc
        sig = b'\x89PNG\r\n\x1a\n'
        ihdr_data = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
        ihdr = chunk(b'IHDR', ihdr_data)
        raw_data = b''
        for row in pixels:
            raw_data += b'\x00'
            for pixel in row:
                raw_data += struct.pack('BBB', *pixel)
        compressed = zlib.compress(raw_data)
        idat = chunk(b'IDAT', compressed)
        iend = chunk(b'IEND', b'')
        return sig + ihdr + idat + iend

    pixels = []
    for y in range(h):
        row = []
        for x in range(w):
            if x < 3 or x >= w-3 or y < 3 or y >= h-3:
                row.append((40, 40, 40))
            elif y < 50:
                row.append((min(r+30, 255), min(g+30, 255), min(b+30, 255)))
            else:
                row.append((r, g, b))
        pixels.append(row)

    # Add visual elements
    for line_y in range(70, h-40, 60):
        for x in range(50, w-50):
            if line_y < h:
                pixels[line_y][x] = (max(r-20, 0), max(g-20, 0), max(b-20, 0))

    png_data = make_png(w, h, pixels)
    with open(filename, 'wb') as f:
        f.write(png_data)
    print(f"  Created {filename}")



def generate_docx(output_path):
    """Generate the complete .docx file."""
    print("Building document content...")
    body_elements = build_body()

    print("Generating document XML...")
    doc = ET.Element(f'{{{W_NS}}}document')
    body_el = ET.SubElement(doc, f'{{{W_NS}}}body')
    for elem in body_elements:
        body_el.append(elem)

    # Page setup
    sectPr = ET.SubElement(body_el, f'{{{W_NS}}}sectPr')
    ET.SubElement(sectPr, f'{{{W_NS}}}pgSz',
                  {f'{{{W_NS}}}w': '12240', f'{{{W_NS}}}h': '15840'})
    ET.SubElement(sectPr, f'{{{W_NS}}}pgMar',
                  {f'{{{W_NS}}}top': '1440', f'{{{W_NS}}}right': '1440',
                   f'{{{W_NS}}}bottom': '1440', f'{{{W_NS}}}left': '1440',
                   f'{{{W_NS}}}header': '720', f'{{{W_NS}}}footer': '720'})

    # Content types
    ct = ET.Element('Types')
    ct.set('xmlns', CT_NS)
    ET.SubElement(ct, 'Default', {'Extension': 'rels',
        'ContentType': 'application/vnd.openxmlformats-package.relationships+xml'})
    ET.SubElement(ct, 'Default', {'Extension': 'xml',
        'ContentType': 'application/xml'})
    ET.SubElement(ct, 'Override', {'PartName': '/word/document.xml',
        'ContentType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'})
    ET.SubElement(ct, 'Override', {'PartName': '/word/styles.xml',
        'ContentType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml'})

    # Relationships
    rels = ET.Element('Relationships')
    rels.set('xmlns', REL_NS)
    ET.SubElement(rels, 'Relationship', {'Id': 'rId1',
        'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument',
        'Target': 'word/document.xml'})

    word_rels = ET.Element('Relationships')
    word_rels.set('xmlns', REL_NS)
    ET.SubElement(word_rels, 'Relationship', {'Id': 'rId1',
        'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles',
        'Target': 'styles.xml'})

    print("Creating .docx archive...")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', element_to_string(ct))
        zf.writestr('_rels/.rels', element_to_string(rels))
        zf.writestr('word/document.xml', element_to_string(doc))
        zf.writestr('word/styles.xml', element_to_string(get_styles_xml()))
        zf.writestr('word/_rels/document.xml.rels', element_to_string(word_rels))

    # Word count
    all_text = []
    for elem in body_elements:
        for t in elem.iter(f'{{{W_NS}}}t'):
            if t.text:
                all_text.append(t.text)
    total_words = sum(len(t.split()) for t in all_text)
    print(f"\nDocument created: {output_path}")
    print(f"Estimated word count: {total_words}")
    print(f"Sections: 5 main sections")
    print(f"Tables: 3")
    print(f"Figures: 4 (placeholders)")
    print(f"References: 51")



# =============================================================================
# REFERENCE ORDER ANALYSIS
# =============================================================================

def check_reference_order():
    """Check if references appear in serial order in the text."""
    import re
    print("\n" + "="*70)
    print("REFERENCE ORDER ANALYSIS")
    print("="*70)

    # Collect all text content in order
    sections = [get_section1(), get_section2(), get_section3(), get_section4(), get_section5()]
    section_names = ["Section 1", "Section 2", "Section 3", "Section 4", "Section 5"]

    all_citations = []
    issues = []

    for sec_idx, section in enumerate(sections):
        for item in section:
            text, ptype = item[0], item[1]
            if ptype == "body":
                # Find all citation numbers
                refs = re.findall(r'\[(\d+)\]', text)
                for ref in refs:
                    ref_num = int(ref)
                    all_citations.append((ref_num, section_names[sec_idx]))

    # Check serial order
    max_seen = 0
    print("\nCitation order of first appearance:")
    seen = set()
    first_appearances = []
    for ref_num, sec_name in all_citations:
        if ref_num not in seen:
            seen.add(ref_num)
            first_appearances.append((ref_num, sec_name))
            if ref_num < max_seen:
                issues.append(f"  WARNING: [{ref_num}] appears in {sec_name} but [{max_seen}] was already cited earlier")
            max_seen = max(max_seen, ref_num)

    for ref_num, sec_name in first_appearances:
        print(f"  [{ref_num}] first appears in {sec_name}")

    # Check for gaps
    all_nums = sorted(seen)
    if all_nums:
        expected = set(range(1, max(all_nums) + 1))
        missing = expected - seen
        if missing:
            issues.append(f"  MISSING references (not cited in text): {sorted(missing)}")

    if issues:
        print("\n" + "-"*70)
        print("ISSUES FOUND:")
        for issue in issues:
            print(issue)
    else:
        print("\n  All references appear in serial order.")

    print("="*70)
    return len(issues) == 0



# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("="*70)
    print("GENERATING: Smart Healthcare Analytics and Intelligent Care Systems")
    print("Book: Transforming Business Education through Artificial Intelligence")
    print("="*70)

    # Check reference order
    check_reference_order()

    # Create figure placeholders
    print("\nCreating figure placeholder images...")
    create_figure_pngs()

    # Generate the DOCX
    print("\nGenerating Word document...")
    output_path = '/projects/sandbox/AMMAN/Smart_Healthcare_Analytics_Chapter.docx'
    generate_docx(output_path)

    print("\n" + "="*70)
    print("FILES CREATED:")
    print(f"  - {output_path}")
    print("  - healthcare_figures/Figure_1.png")
    print("  - healthcare_figures/Figure_2.png")
    print("  - healthcare_figures/Figure_3.png")
    print("  - healthcare_figures/Figure_4.png")
    print("="*70)
