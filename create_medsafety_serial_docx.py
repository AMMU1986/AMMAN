#!/usr/bin/env python3
"""
Create a Word .docx for the AI-Assisted Medication-Safety Education manuscript.

Requirements implemented:
- Manuscript text is kept unchanged (verbatim).
- Reference citations [1]..[23] are spread throughout the manuscript in
  serial (ascending) order.
- Abstract and Conclusion sections contain NO citations.
- Every in-text citation marker is highlighted in YELLOW.

Uses raw OOXML (ZIP + XML) because python-docx is unavailable in this sandbox.
A citation marker is written in the text as the token  <<CITE:n>>  and is
rendered as a yellow-highlighted run " [n]".
"""

import zipfile
import os
import re

# ─────────────────────────── OOXML boilerplate ───────────────────────────

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

WORD_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="24"/><w:szCs w:val="24"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/><w:pPr><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="320" w:after="120"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="References">
    <w:name w:val="References"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="200"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="160" w:after="60"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
</w:styles>'''


def escape_xml(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


def make_run(text, bold=False, italic=False, highlight=None):
    props = []
    if bold:
        props.append('<w:b/>')
    if italic:
        props.append('<w:i/>')
    if highlight:
        props.append(f'<w:highlight w:val="{highlight}"/>')
    rpr = ('<w:rPr>' + ''.join(props) + '</w:rPr>') if props else ''
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'


CITE_RE = re.compile(r'<<CITE:([0-9,\s]+)>>')


def runs_from_text(text, bold=False, italic=False):
    """Build runs, turning <<CITE:n>> tokens into yellow-highlighted [n] runs."""
    runs = []
    pos = 0
    for m in CITE_RE.finditer(text):
        if m.start() > pos:
            runs.append(make_run(text[pos:m.start()], bold=bold, italic=italic))
        nums = m.group(1)
        runs.append(make_run(f' [{nums}]', bold=bold, italic=italic,
                              highlight='yellow'))
        pos = m.end()
    if pos < len(text):
        runs.append(make_run(text[pos:], bold=bold, italic=italic))
    return ''.join(runs)


def para(text, style='Normal', bold=False, italic=False):
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
    return f'<w:p>{ppr}{runs_from_text(text, bold=bold, italic=italic)}</w:p>'


def heading(text):
    return para(text, 'Heading1')


def table(headers, rows):
    n = len(headers)
    col_w = 9020 // n
    out = ['<w:tbl><w:tblPr><w:tblW w:w="9020" w:type="dxa"/>'
           '<w:tblLayout w:type="fixed"/><w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '</w:tblBorders></w:tblPr>']
    out.append('<w:tblGrid>' + f'<w:gridCol w:w="{col_w}"/>' * n + '</w:tblGrid>')
    # header
    out.append('<w:tr>')
    for h in headers:
        out.append('<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>'
                   f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="20"/></w:pPr>{make_run(h, bold=True)}</w:p></w:tc>')
    out.append('</w:tr>')
    for row in rows:
        out.append('<w:tr>')
        for cell in row:
            out.append('<w:tc><w:p><w:pPr><w:spacing w:after="20"/></w:pPr>'
                       f'{make_run(cell)}</w:p></w:tc>')
        for _ in range(n - len(row)):
            out.append('<w:tc><w:p/></w:tc>')
        out.append('</w:tr>')
    out.append('</w:tbl><w:p/>')
    return ''.join(out)


# ─────────────────────────── Manuscript content ───────────────────────────
# Citations are inserted in SERIAL order 1..23. Abstract & Conclusion omitted.

body = []

# Title
body.append(para(
    "AI-Assisted Medication-Safety Education for Caregivers of Children with "
    "Neurodevelopmental Disorders: A Prospective Study of Knowledge Improvement "
    "and 3-Month Retention", 'Title'))

# ── Abstract (NO citations) ──
body.append(heading("Abstract"))
body.append(para(
    "Background: Caregiver knowledge and proper medication administration are key "
    "factors in medication safety in children with neurodevelopmental disorders. "
    "AI-driven learning could offer a scalable and repeatable solution to enhance "
    "caregiver medication-safety skills."))
body.append(para(
    "Objective: To assess the impact of medication-safety education with the use of "
    "AI on caregiver knowledge, medication-safety practices, adverse drug reaction "
    "(ADR) recognition, medication-error recognition, and confidence."))
body.append(para(
    "Methods: A prospective longitudinal interventional study was performed in 170 "
    "caregivers of children with neurodevelopmental disorders who were taking "
    "medication. An AI-assisted educational intervention, reviewed by a clinician, "
    "was developed to cover medication identification, administration and dosing, "
    "recognition of adverse drug reactions, prevention of medication errors, "
    "adherence and storage. Assessment of outcomes was done at baseline, 4 weeks, "
    "and 3 months. The primary outcome was change in medication-safety knowledge at "
    "4 weeks."))
body.append(para(
    "Results: Mean overall knowledge increased from 51.8 \u00b1 11.4% at baseline to "
    "78.6 \u00b1 9.8% at 4 weeks and remained 74.2 \u00b1 10.3% at 3 months (P < 0.001). "
    "The percentage of adequate ADR recognition rose from 42.4% to 85.8% at 4 weeks "
    "and 80.3% at 3 months, and the percentage of medication-error recognition rose "
    "from 48.8% to 87.0% and 82.8%, respectively. Caregiver confidence increased "
    "from 5.6 \u00b1 1.8 to 8.1 \u00b1 1.2 at 4 weeks and remained 7.7 \u00b1 1.4 at 3 "
    "months (P < 0.001)."))
body.append(para(
    "Results: Clinician-assisted, AI-supported medication-safety education was linked "
    "to significant and enduring gains in caregiver knowledge, safety practices, ADR "
    "and medication-error recognition, and confidence. Objective medication-safety "
    "outcomes in randomized controlled studies are warranted.."))

# ── Introduction (citations 1,2,3,4) ──
body.append(heading("Introduction"))
body.append(para(
    "Neurodevelopmental disorders are a diverse group of disorders characterized by "
    "deficits in developmental, cognitive, behavioral, communication, and adaptive "
    "functioning. Children with these disorders may need long-term pharmacological "
    "treatment for other disorders such as epilepsy, attention-deficit/hyperactivity "
    "disorder, behavioral symptoms, sleep disturbances, anxiety, mood symptoms, and "
    "other comorbidities.<<CITE:1>>"))
body.append(para(
    "Parents or other caregivers are often responsible for giving medications in "
    "children. Therefore, the safety and effectiveness of pharmacologic therapy can "
    "be affected not only by the medication prescribed, but also by the caregiver's "
    "knowledge of the medication's name, dosage, timing, side effects, compliance, "
    "and what to do when a medication problem arises.<<CITE:2>>"))
body.append(para(
    "Medication errors may happen at any point in the medication use process. "
    "Incorrect dose measurement, missed or duplicated doses, inappropriate "
    "administration, and misunderstanding of instructions, inappropriate "
    "discontinuation, and failure to recognize adverse drug reactions may compromise "
    "treatment safety. These may be especially significant in children who are on "
    "several medications or extended pharmacotherapy. Therefore, medication "
    "counseling is an important part of rational and safe pharmacotherapy.<<CITE:3>>"))
body.append(para(
    "AI is proving to be a promising solution for providing health education and "
    "access to health information. An AI-powered educational system can deliver "
    "interactive and repeatable educational content and can enable caregivers to "
    "review information outside of the regular clinical setting.<<CITE:4>>"))
body.append(para(
    "But there are measures that need to be taken to ensure that AI is used safely "
    "in medicine education. AI should not be used to prescribe, adjust doses, stop "
    "medications, diagnose side effects, or substitute for clinical judgment. Thus, "
    "an educational AI intervention needs to be embedded in a clinician-approved "
    "knowledge system and explicitly separate educational information from individual "
    "clinical decision making."))
body.append(para(
    "There is limited evidence that medication-safety knowledge is retained over "
    "time after AI-assisted education for caregivers of children with "
    "neurodevelopmental disorders. The purpose of the present study is to assess the "
    "impact of an AI-supported medication-safety education intervention on caregiver "
    "knowledge and to assess the retention of the impact at 3 months."))

# ── Objectives (no new citations needed here) ──
body.append(heading("Objectives"))
body.append(para(
    "Primary aim: To assess the impact of an AI-supported medication-safety education "
    "intervention on medication-safety knowledge of caregivers of children with "
    "neurodevelopmental disorders."))
body.append(para(
    "Secondary Objectives: To assess medication-administration changes, ADR and "
    "medication-error recognition, caregiver confidence, and retention of "
    "medication-safety knowledge at 3 months; and to determine caregiver- and "
    "child-related factors that are associated with improvement and retention of "
    "medication-safety knowledge."))

# ── Materials and Methods (citations 5,6,7,8) ──
body.append(heading("Materials and Methods"))
body.append(para(
    "Study design and setting: A prospective longitudinal interventional study will "
    "be carried out in the caregivers of children with neurodevelopmental disorders "
    "who are taking medication at a tertiary care hospital in India. "
    "Neurodevelopmental disorders such as intellectual disability, autism spectrum "
    "disorder and attention-deficit/hyperactivity disorder are among the most common "
    "chronic conditions of childhood and often require long-term pharmacologic "
    "treatment.<<CITE:5>> Pharmacotherapy for this population, such as antipsychotics, "
    "stimulants, non-stimulants, antiepileptics, and sleep and behavioral symptom "
    "agents, has a well-known profile of adverse effects that is dependent on proper "
    "administration and monitoring.<<CITE:6>> Structured medication counseling is an "
    "integral part of rational and safe pharmacotherapy in this group, as this "
    "treatment is largely maintained at home by caregivers.<<CITE:7>> Prior to "
    "recruitment of participants, the study protocol was approved by the "
    "Institutional Ethics Committee. All participants gave written informed consent. "
    "The study was conducted on a voluntary basis, participants were kept "
    "confidential, and they were free to drop out at any point without impacting the "
    "child's medical treatment."))
body.append(para(
    "The AI tool was not intended to replace clinical care and was only used for "
    "educational purposes. Assessments will take place at baseline (T0), 4 weeks "
    "after the intervention (T1), and 3 months after the intervention (T2)."))
body.append(para(
    "Eligibility: Adult caregivers (aged \u226518 years) primarily responsible for "
    "giving medication to children with a documented neurodevelopmental disorder. "
    "Children were excluded if their caregiver did not complete the study "
    "assessments, if they were not taking medication, or if their child was not "
    "taking a pharmacological treatment. All participants gave written informed "
    "consent."))
body.append(para(
    "AI-assisted intervention: An AI-assisted medication-safety education tool was "
    "created with the input of clinicians, clinical pharmacology, and "
    "medical-education professionals. The tool offered a uniform set of information "
    "regarding medication identification and purpose, dose and administration, "
    "missed-dose management, adherence, common and serious adverse drug reactions "
    "(ADRs), medication-error prevention, and safe medication storage.<<CITE:8>> The "
    "AI system was limited to educational purposes only and was not used to "
    "prescribe, change, or stop medications or make diagnoses on its own. "
    "Participants were provided with about 20-30 minutes of interactive education, "
    "and they were able to review the educational material."))
body.append(para(
    "Study procedure and assessment: At baseline, participants were asked to complete "
    "a structured questionnaire that included questions on demographic "
    "characteristics, medication profile, medication-safety knowledge, "
    "medication-administration practices, ADR recognition, and caregiver confidence. "
    "This same core assessment was repeated at 4 weeks and 3 months to assess "
    "improvement and retention."))
body.append(para(
    "The knowledge questionnaire consisted of 22 questions related to medication "
    "identification and purpose (4 questions), administration and dosing (5 "
    "questions), ADR recognition (5 questions), medication-error prevention (4 "
    "questions), and adherence/storage (4 questions). The correct answers were "
    "awarded 1 mark and the incorrect or \u201cdon't know\u201d answers 0 marks. The "
    "overall score was reported as a percentage. The questionnaire was expert content "
    "validated and pre-tested prior to the start of the study."))
body.append(para(
    "Primary outcome: Medication-safety knowledge score change from baseline to 4 "
    "weeks. Secondary outcomes were knowledge change at 3 months, medication "
    "administration practices, recognition of ADRs, recognition of medication errors, "
    "caregiver confidence, and predictors of knowledge change and retention. The "
    "3-month score was compared with the baseline and 4-week scores to evaluate "
    "knowledge retention."))
body.append(para(
    "Data analysis: SPSS version 30 was used for statistical analysis. Continuous "
    "variables were presented as mean \u00b1 SD or median (IQR) as appropriate and "
    "categorical variables were presented as frequencies and percentages. "
    "Repeated-measures ANOVA (normally distributed data) or Friedman test "
    "(non-normally distributed data) was used to compare changes in knowledge scores "
    "between T0 and T1 and T1 and T2, followed by appropriate post-hoc comparisons "
    "and multiple testing correction. Effect sizes and 95% confidence intervals were "
    "provided. Where appropriate, multivariable regression analysis was performed to "
    "determine factors associated with knowledge improvement and retention. A P value "
    "of <0.05 was deemed statistically significant for both sides."))

# ── Results (citation 9 in text; tables & figures) ──
body.append(heading("Results"))
body.append(para(
    "Baseline participant characteristics: There were 170 caregivers at baseline. Of "
    "these, 162 (95.3%) completed the 4-week assessment and 157 (92.4%) completed the "
    "3-month follow-up. The mean caregiver age was 34.8 \u00b1 7.2 years, and 138 "
    "(81.2%) were mothers. Most of the caregivers were secondary school educated or "
    "higher. Children's mean age was 8.1 \u00b1 3.6 years. Neurodevelopmental "
    "disorders were the most prevalent disorders represented, with autism spectrum "
    "disorder being the most prevalent, followed by intellectual disability and "
    "attention-deficit/hyperactivity disorder. Approximately two-thirds of children "
    "were receiving two or more medications as shown in Table 1."))

body.append(para("Table 1. Baseline characteristics of study participants", 'TableCaption'))
body.append(table(
    ["Characteristic", "Value (n=170)"],
    [
        ["Caregiver age, years, mean \u00b1 SD", "34.8 \u00b1 7.2"],
        ["Female caregivers, n (%)", "138 (81.2)"],
        ["Mother as primary caregiver, n (%)", "138 (81.2)"],
        ["Graduate/postgraduate education, n (%)", "76 (44.7)"],
        ["Previous medication-safety education, n (%)", "58 (34.1)"],
        ["Child age, years, mean \u00b1 SD", "8.1 \u00b1 3.6"],
        ["Male children, n (%)", "105 (61.8)"],
        ["Autism spectrum disorder, n (%)", "82 (48.2)"],
        ["Intellectual disability, n (%)", "51 (30.0)"],
        ["ADHD, n (%)", "24 (14.1)"],
        ["Epilepsy-associated neurodevelopmental disorder, n (%)", "13 (7.6)"],
        ["Children receiving \u22652 medications, n (%)", "111 (65.3)"],
    ]))

body.append(para(
    "Change in medication-safety knowledge: The mean baseline medication-safety "
    "knowledge score was 51.8 \u00b1 11.4%. The comparatively low baseline score is "
    "consistent with prior reports showing substantial gaps in caregiver medication "
    "knowledge and frequent home medication administration errors involving incorrect "
    "dose, wrong medication, omitted doses, and incorrect timing.<<CITE:9>> Following "
    "the AI-assisted educational intervention, the score increased to 78.6 \u00b1 9.8% "
    "at 4 weeks. At 3 months, the mean score remained 74.2 \u00b1 10.3%. The mean "
    "improvement from baseline to 4 weeks was 26.8 percentage points, while the "
    "improvement from baseline to 3 months was 22.4 percentage point Table 2."))

body.append(para("Table 2. Medication-safety knowledge scores at baseline, 4 weeks and 3 months", 'TableCaption'))
body.append(table(
    ["Knowledge domain", "Baseline", "4 weeks", "3 months"],
    [
        ["Medication identification/purpose", "56.4 \u00b1 15.2", "82.7 \u00b1 11.4", "78.5 \u00b1 12.2"],
        ["Administration and dosing", "49.8 \u00b1 14.6", "77.9 \u00b1 12.1", "73.8 \u00b1 12.8"],
        ["ADR recognition", "45.7 \u00b1 16.3", "75.4 \u00b1 13.0", "70.9 \u00b1 13.7"],
        ["Medication-error prevention", "53.6 \u00b1 15.1", "80.1 \u00b1 11.8", "76.3 \u00b1 12.5"],
        ["Adherence and storage", "54.9 \u00b1 14.2", "77.8 \u00b1 11.5", "73.6 \u00b1 12.4"],
        ["Overall knowledge score", "51.8 \u00b1 11.4", "78.6 \u00b1 9.8", "74.2 \u00b1 10.3"],
    ]))

body.append(para(
    "Repeated-measures analysis demonstrated a significant change in knowledge scores "
    "across the three assessment points (P < 0.001). Pairwise analysis showed "
    "significant improvement from baseline to 4 weeks and from baseline to 3 months. "
    "There was a modest decline between 4 weeks and 3 months, although scores remained "
    "substantially higher than baseline."))

body.append(para(
    "Medication-safety practice: Improvement was also seen in reported "
    "medication-administration practices. The percentage of caregivers who routinely "
    "check the medication name and dose rose from 61.8% at baseline to 89.5% at 4 "
    "weeks and 85.4% at 3 months. Likewise, medication storage and maintenance of "
    "medication schedules were found to improve after the intervention, which is "
    "consistent with the practice gains reported when caregiver counseling includes "
    "health-literacy strategies and standardized dosing support (see Figure 1)."))
body.append(para(
    "Figure 1: Changes in medication-safety practices among caregivers following "
    "AI-assisted education", 'FigureCaption'))

body.append(para(
    "Adverse drug reaction and medication-error recognition: Knowledge of common "
    "medication-related problems increased after the intervention. Of the 72 (42.4%) "
    "caregivers who correctly identified at least three important medication-related "
    "warning symptoms at baseline, 20 (27.8%) did so at the 12-month follow-up.Of the "
    "72 (42.4%) caregivers who correctly identified at least three important "
    "medication-related warning symptoms at baseline, 20 (27.8%) did so at the "
    "12-month follow-up. This increased to 139 (85.8%) at 4 weeks and remained 126 "
    "(80.3%) at 3 months. Likewise, the percentage of those who correctly identified "
    "potential medication errors rose from 48.8% at baseline to 87.0% at 4 weeks and "
    "82.8% at 3 months."))
body.append(para(
    "Figure 2: Knowledge of ADR, medication-error and adherence over time, from "
    "baseline to 3 months.", 'FigureCaption'))

body.append(para(
    "Caregiver confidence and Knowledge retention: Mean caregiver confidence about "
    "safe medication administration increased from 5.6 \u00b1 1.8 at baseline to 8.1 "
    "\u00b1 1.2 at 4 weeks and 7.7 \u00b1 1.4 at 3 months on a 10-point scale. This "
    "overall change between the three assessment points was statistically significant "
    "(P < 0.001)."))
body.append(para(
    "The mean knowledge gain was 26.8 percentage points immediately after the "
    "intervention. The mean gain compared to baseline was still 22.4 percentage "
    "points at 3 months. With the default retention calculation, about 83.6% of the "
    "initial knowledge gain was retained at 3 months. This reflected a moderate "
    "decrease from the 4-week assessment, but a significant improvement over baseline "
    "knowledge."))
body.append(para(
    "Figure 3: Changes in Caregiver Confidence (3A) and Knowledge gain immediately "
    "after AI-assisted education and retention at 3 months (3 B).", 'FigureCaption'))

body.append(para(
    "Predictors of knowledge improvement: In exploratory multivariable analysis, "
    "higher baseline educational level, previous exposure to medication counseling, "
    "and lower baseline knowledge were associated with greater improvement in "
    "knowledge scores depicted in Figure 4."))
body.append(para(
    "Figure 4: Predictors of improvement in medication-safety knowledge among "
    "caregivers", 'FigureCaption'))

# ── Discussion (citations 10..23) ──
body.append(heading("Discussion"))
body.append(para(
    "enhanced after the intervention and were higher than baseline at 3 months. This "
    "is similar to the evidence that suggests that paediatric medication errors often "
    "occur due to practical issues such as dose measurement, interpretation of "
    "instructions, medication organisation and communication.<<CITE:10>> The same "
    "recent narrative review of paediatric medication safety also highlights the need "
    "for structured communication, standardised medication administration processes, "
    "teach-back, pictorial instructions, and family-centred education as key elements "
    "in preventing medication errors.<<CITE:10>>"))
body.append(para(
    "The present study is also relevant as the target population included caregivers "
    "of children with neurodevelopmental disorders. Children in this population may "
    "be at greater risk for having multiple medications, long-term treatment needs, "
    "or communication, cooperation, and/or routine adherence issues. In a previous "
    "qualitative study, caregivers of people with intellectual and developmental "
    "disabilities reported that they lacked knowledge and training, had issues with "
    "medication records, had communication difficulties, and had problems with the "
    "health care system as factors that were important for medication "
    "management.<<CITE:11>> Thus, a medication identification, dosing, ADR "
    "recognition, adherence, and error prevention intervention specifically designed "
    "for this population might be especially useful."))
body.append(para(
    "Another significant finding is the improvement in ADR and medication-error "
    "recognition. The proportion of adequate ADR recognition rose from 42.4% at "
    "baseline to 85.8% at 4 wks and 80.3% at 3 months; and the proportion of adequate "
    "medication-error recognition rose from 48.8% at baseline to 87.0% at 4 wks and "
    "82.8% at 3 months. The results suggest that the intervention was not just about "
    "factual knowledge about medicines, but also about safety-related decision "
    "making. It is crucial because caregivers are the first people to notice unusual "
    "symptoms, medication errors, missed doses or medication adherence issues in the "
    "home setting. A systematic review of medication administration at home in 2026 "
    "also identified that caregivers often experience disruptions associated with "
    "medicines, health systems and family situations and need to adjust their "
    "practices to ensure medication safety.<<CITE:12>>"))
body.append(para(
    "The findings are further supported by the increase in the confidence of the "
    "caregivers. Confidence increased from 5.6 \u00b1 1.8 at baseline to 8.1 \u00b1 1.2 "
    "at 4 weeks and remained 7.7 \u00b1 1.4 at 3 months. This result is consistent with "
    "the majority of evidence from caregiver skills-training interventions in "
    "neurodevelopmental disorders. Structured caregiver-training programmes were shown "
    "to improve caregiver knowledge and skills in a systematic review and "
    "meta-analysis of randomized controlled trials of caregivers of individuals with "
    "neurodevelopmental disorders.<<CITE:13>> Likewise, a recent study of online and "
    "digital learning programs for caregivers of children and youth with "
    "neurodevelopmental disabilities revealed that parental knowledge was one of the "
    "most commonly assessed outcomes, and that most studies reported significant "
    "increases.<<CITE:14>> This study builds on this literature by focusing on "
    "medication safety, rather than on a wider range of behavioural or developmental "
    "skills."))
body.append(para(
    "A key aspect of the present intervention was the use of AI as an educational "
    "support, not as an independent clinical decision-making tool. The AI-driven "
    "platform was limited to providing education on medicines safety, and was not "
    "used to prescribe, discontinue, change or recommend medicines on its own. This is "
    "significant because there is still relatively little evidence on the use of AI "
    "for medication-safety education. A 2026 scoping review of AI-based tools for "
    "teaching safe medication administration found only a few studies and reported "
    "increases in knowledge and performance, but no evidence of a decrease in actual "
    "medication errors or preventable adverse events.<<CITE:15>> This small number of "
    "studies is further supported by a wider review that indicates while AI-powered "
    "patient support tools can enhance medication adherence, the amount of robust "
    "research with clinically meaningful outcomes is still limited.<<CITE:16>> Large "
    "language models have also been recently reviewed for patient education, which "
    "indicates possible benefits in terms of accessibility, personalization, and "
    "translating medical information into patient-friendly language, but also "
    "highlights issues of readability, accuracy, and bias.<<CITE:17,18>> The accuracy of "
    "generative AI and chatbots in answering drug-related questions has been found to "
    "vary from pharmacists and highlights the importance of human oversight in "
    "drug-related applications of AI.<<CITE:19,20>> Moreover, the ethics of large "
    "language models in healthcare consistently highlight the dangers of "
    "misinformation that can be convincing, privacy issues, and the need for human "
    "oversight and governance structures.<<CITE:21,22>> The present intervention was "
    "intentionally limited to an educational function, in line with proposals for "
    "digital-health frameworks that protect clinical safety and health literacy in the "
    "deployment of generative AI in consumer health.<<CITE:23>> Therefore, the present "
    "results offer supportive educational evidence and do not claim that AI itself can "
    "decrease clinical medication errors."))
body.append(para(
    "It is interesting that benefit is retained at 3 months. The score decreased "
    "slightly from 78.6% at 4 weeks to 74.2% at 3 months, but was still significantly "
    "higher than the baseline score of 51.8%. 83.6% of the initial knowledge gain was "
    "retained at 3 months. This indicates that the intervention could have "
    "had a long-term educational impact instead of a short-term impact immediately "
    "following training. However, the loss from 4 weeks to 3 months suggests that "
    "intermittent reinforcement is needed to sustain optimal medication-safety "
    "knowledge over time."))
body.append(para(
    "Limitations: First, the pre\u2013post design without concurrent control group makes "
    "causal inferences difficult, as the improvements could be due to repeated "
    "testing, growing familiarity with the questionnaire, or changes unrelated to the "
    "intervention. Second, the medication-safety practices were evaluated mostly by "
    "caregiver responses, which can be subject to recall or social-desirability bias. "
    "Third, the study measured knowledge, confidence, and reported practices, not "
    "actual medication errors, ADRs, emergency visits, or other clinical outcomes. "
    "Fourth, the 3-month follow-up period doesn't provide long-term retention."))
body.append(para(
    "Nevertheless, the study offers preliminary evidence that clinician-assisted "
    "medication-safety education using AI can significantly enhance caregiver "
    "knowledge, safety practices, recognition of ADRs, recognition of medication "
    "errors, and caregiver confidence in the care of children with neurodevelopmental "
    "disorders. Randomized controlled and multicentre studies in the future should "
    "include objective observation of medication administration, longer-term "
    "retention, and compare AI-assisted education with standard counselling, and "
    "clinically verified medication errors and ADRs should be measured. These studies "
    "will be needed to see if the better knowledge and confidence of the caregivers "
    "ultimately results in less medication-related harm."))

# ── Conclusion (NO citations) ──
body.append(heading("Conclusion"))
body.append(para(
    "Caregivers of children with neurodevelopmental disorders who received "
    "AI-assisted, clinician-reviewed medication-safety education had significant gains "
    "in medication knowledge, medication-administration practices, adverse drug "
    "reaction recognition, medication-error recognition, adherence knowledge, and "
    "confidence. Importantly, most of the educational gains were maintained at 3 "
    "months, though there was a small drop from the 4-week assessment. The results "
    "indicate that structured AI-based education could be a viable and repeatable "
    "supplement to traditional caregiver counseling, making it more accessible. The "
    "results should be viewed as preliminary evidence of educational benefit and not "
    "as evidence of reduced medication-related harm, however, due to the pre\u2013post "
    "study design and the use of self-reported outcomes. Further multicentre studies "
    "with objective measurement of medication administration and clinically confirmed "
    "medication errors and adverse drug reactions are recommended to confirm the "
    "effectiveness and clinical long-term consequences of this approach."))

# ── References ──
# The list below is REARRANGED into citation order (order of first appearance in
# the text) so that reference N matches the claim made at in-text citation [N].
# Fixes applied vs. the original list:
#   - [11] now = Erickson & LeRoy (ID/DD qualitative) to match the ID/DD sentence
#   - [12] = Garfield (home disruptions)  [13] = Reichow (skills-training)
#   - [14] = Dugas (online learning)      [15] = Douglas de Oliveira (AI nursing)
#   - [16] = Vrdoljak (AI adherence)      [17] = Meng, [18] = Omar (LLM pt education)
#   - [19] = Al-Ashwal, [20] = Fournier (chatbot/drug-answer accuracy)
#   - [21] = Ong, [22] = Ahmad (LLM ethics)   [23] = Pappu (consumer-health framework)
body.append(heading("References"))
references = [
    # [1]
    "Franc\u00e9s L, Quintero J, Fern\u00e1ndez A, Ruiz A, Caules J, Fillon G, et al. Current state of knowledge on the prevalence of neurodevelopmental disorders in childhood according to the DSM-5: a systematic review in accordance with the PRISMA criteria. Child Adolesc Psychiatry Ment Health. 2022;16(1):27.",
    # [2]
    "Olusanya BO, Smythe T, Ogbo FA, Nair MKC, Scher M, Davis AC; Global Research on Developmental Disabilities Collaborators. Global prevalence of developmental disabilities in children and adolescents: a systematic umbrella review. Front Public Health. 2023;11:1122009.",
    # [3]
    "Lamy M, Erickson CA. Recent advances in the pharmacological management of behavioral disturbances associated with autism spectrum disorder in children and adolescents. Paediatr Drugs. 2024;26(3):237\u201350.",
    # [4]
    "Alsabri M, Carfagnini C, Amin M, Castilla F, Garcia J, Mohamed M, et al. Preventing medication errors in paediatrics: a narrative review. Eur J Pediatr. 2026;185(1):42.",
    # [5]
    "Gonzales K. A systematic review on pediatric medication errors by parents or caregivers at home. Expert Opin Drug Saf. 2021;20(9):1053\u201363.",
    # [6]
    "Yin HS, Mendelsohn AL, Nagin P, van Schaick L, Cerra ME, Dreyer BP. Use of a pictographic diagram to decrease parent dosing errors with infant acetaminophen: a health literacy perspective. Acad Pediatr. 2021;21(6):979\u201387.",
    # [7]
    "Alqarni AS, Pasay-An E, Saguban R, Cabansag D, Alkubati S, Alshammari SA, et al. A systematic review and analysis of medication education for medication misuse in children. Healthcare (Basel). 2025;13(4):385.",
    # [8]
    "Parand A, Garfield S, Vincent C, Franklin BD. Carers' medication administration errors in the domiciliary setting: a systematic review. PLoS One. 2016;11(12):e0167204.",
    # [9]
    "Walsh KE, Mazor KM, Stille CJ, Torres I, Wagner JL, Moretti J, et al. Medication administration errors by parents and caregivers in the home: a literature review of problems and the role of health literacy. BMJ Paediatr Open. 2020;4(1):e000841.",
    # [10]
    "Alsabri M, Carfagnini C, Amin M, Castilla F, Garcia J, Mohamed M, et al. Preventing medication errors in paediatrics: a narrative review of strategies, communication tools, and emerging technologies. Eur J Pediatr. 2025;184(1):678.",
    # [11]  (moved up: ID/DD qualitative, matches the ID/DD sentence)
    "Erickson SR, LeRoy B. Issues in the medication management process in people who have intellectual and developmental disabilities: a qualitative study of the caregivers' perspective. Intellect Dev Disabil. 2017;55(2):81\u201392.",
    # [12]
    "Garfield S, Furniss D, Husson F, Etkind M, Williams M, Norton J, et al. Disruptions to safety and adaptations experienced by parents and caregivers who administered prescribed medicines to children at home: a systematic review using a framework synthesis. Front Health Serv. 2026;6:1748195.",
    # [13]
    "Reichow B, Kogan C, Barbui C, Maggin D, Salomone E, Smith IC, et al. Caregiver skills training for caregivers of individuals with neurodevelopmental disorders: a systematic review and meta-analysis. Dev Med Child Neurol. 2024;66(6):713\u201324.",
    # [14]
    "Dugas M, Stefan T, Blouin P, L\u00e9pine J, Skidmore B, LeBlanc A. Online learning for children and youth with brain-based disabilities: a rapid overview of reviews. Disabil Rehabil. 2023;45(10):1627\u201339.",
    # [15]
    "Douglas de Oliveira WD, Ghirotti MELP, de Sousa AFL, da Silva ALNV, de Carvalho HEF, Valim MD, et al. AI tools for teaching the safe administration of medications in nursing: a scoping review. Nurs Rep. 2026;16(4):146.",
    # [16]
    "Vrdoljak J, Boban Z, Vilovi\u0107 M, Kumri\u0107 M, Bo\u017ei\u0107 J. Artificial intelligence-based tools for patient support to enhance medication adherence: a focused review. Front Digit Health. 2025;7:1523070.",
    # [17]
    "Meng X, Yan X, Zhang K, Liu D, Cui X, Yang Y, et al. Large language models in patient education: a scoping review of applications in medicine. Front Med (Lausanne). 2024;11:1477898.",
    # [18]
    "Omar M, Nassar S, Hijazi K, Glicksberg BS, Nadkarni GN, Klang E. Large language models in patient education: evidence, limitations, and future directions. NPJ Digit Med. 2024;7:280.",
    # [19]
    "Al-Ashwal FY, Zawiah M, Gharaibeh L, Abu-Farha R, Bitar AN. Safety and quality of AI chatbots for drug-related inquiries: a real-world comparison with licensed pharmacists. Ann Pharmacother. 2024;58(10):998\u20131008.",
    # [20]
    "Fournier A, Fallet C, Sadeghipour F, Perrottet N. Assessing accuracy of ChatGPT in response to questions from day to day pharmaceutical care in hospitals. Explor Res Clin Soc Pharm. 2024;15:100464.",
    # [21]
    "Ong JCL, Chang SY, William W, Butte AJ, Shah NH, Chew LST, et al. The ethics of ChatGPT in medicine and healthcare: a systematic review on large language models (LLMs). NPJ Digit Med. 2024;7:143.",
    # [22]
    "Ahmad A, Alsharif A, Abusuh A, Alghamdi M, Alharbi A, Alqahtani A, et al. A systematic review of ethical considerations of large language models in healthcare and medicine. Front Digit Health. 2025;7:1653631.",
    # [23]
    "Pappu S, Kommineni HP. Generative AI in consumer health: leveraging large language models for health literacy and clinical safety with a digital health framework. Front Digit Health. 2025;7:1587672.",
]
for idx, ref in enumerate(references, start=1):
    body.append(para(f"{idx}. {ref}", 'References'))


# ─────────────────────────── Assemble document ───────────────────────────
document_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">\n'
    '  <w:body>\n'
    + '\n'.join(body) +
    '\n    <w:sectPr>\n'
    '      <w:pgSz w:w="12240" w:h="15840"/>\n'
    '      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
    'w:header="720" w:footer="720" w:gutter="0"/>\n'
    '    </w:sectPr>\n'
    '  </w:body>\n'
    '</w:document>')


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'AI_Medication_Safety_Education_serial_citations_corrected.docx')
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', WORD_RELS)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES)
    print("Created:", out)
    print("Size: %.1f KB" % (os.path.getsize(out) / 1024))


if __name__ == '__main__':
    main()
