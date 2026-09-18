#!/usr/bin/env python3
"""
make_forms.py - Build the three supporting submission documents (Word .docx):
  1. Structured Table of Contents
  2. AI Disclosure Form
  3. Contributing Authors Agreement Form

Reuses the OOXML helpers from build_docx.py (python-docx is unavailable).
"""

import os
import zipfile

import build_docx as B

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, '..')

CHAPTER_TITLE = 'Human-in-the-Loop and Explainable AI in Mission Control Systems'
BOOK = 'AI for Space Traffic Management and Mission Operations'
PUBLISHER = 'Scrivener Publishing (Wiley)'
AUTHORS = 'Amman Jakhar and Sachin Kalsi'
AFFIL = 'Department of Mechanical Engineering, Chandigarh University, Mohali, Punjab-140301, India'
DRAFT_DATE = '18 September 2026'
FINAL_DATE = '30 September 2026'
PAGES = '24'


def assemble(elements, outpath):
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                '<w:body>%s'
                '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
                '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
                'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
                '</w:body></w:document>' % '\n'.join(elements))
    word_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                 '</Relationships>')
    with zipfile.ZipFile(outpath, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', B.CONTENT_TYPES)
        z.writestr('_rels/.rels', B.RELS)
        z.writestr('word/_rels/document.xml.rels', word_rels)
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', B.STYLES)
    print('Created:', os.path.abspath(outpath),
          '(%.1f KB)' % (os.path.getsize(outpath) / 1024))


def P(text, style='Normal'):
    return B.para(text, style)


def spacer():
    return '<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>'


# ─────────────────────────────────────────────────────────────────────────────
# 1. Structured Table of Contents
# ─────────────────────────────────────────────────────────────────────────────
def toc():
    e = []
    e.append(P('Structured Table of Contents', 'Title'))
    e.append(P('Book: ' + BOOK, 'AuthorLine'))
    e.append(P('Chapter 5: ' + CHAPTER_TITLE, 'AuthorLine'))
    e.append(P(AUTHORS + ' — ' + AFFIL, 'AuthorLine'))
    e.append(spacer())

    entries = [
        ('Abstract', 0),
        ('Keywords', 0),
        ('5.1. Introduction', 0),
        ('5.1.1. The shifting locus of control in space operations', 1),
        ('5.1.2. Scope and contributions of this chapter', 1),
        ('5.2. Foundations of Human-in-the-Loop Mission Control', 0),
        ('5.2.1. The autonomy spectrum', 1),
        ('5.2.2. Communication latency and the case for onboard autonomy', 1),
        ('5.2.3. Allocating authority as a function of latency and urgency', 1),
        ('5.3. Explainable AI for Human-AI Teaming in Space', 0),
        ('5.3.1. Why explainability matters in safety-critical operations', 1),
        ('5.3.2. A taxonomy of explanation types', 1),
        ('5.3.3. Empirical effects on trust, situation awareness, and workload', 1),
        ('5.3.4. Explanation depth under uncertainty', 1),
        ('5.4. Architecting HITL-XAI Mission Control Systems', 0),
        ('5.4.1. A layered reference architecture', 1),
        ('5.4.2. Hierarchical planning, truth maintenance, and case-based reasoning', 1),
        ('5.4.3. Explanation generation and interface design', 1),
        ('5.4.4. Trust calibration and cognitive-load management', 1),
        ('5.5. Emerging Deployments and Case Studies', 0),
        ('5.5.1. Onboard language models and the virtual flight controller', 1),
        ('5.5.2. Autonomous collision avoidance and space traffic management', 1),
        ('5.5.3. Comparative synthesis', 1),
        ('5.6. Challenges, Open Problems, and Research Directions', 0),
        ('5.6.1. Verification, validation, and certification', 1),
        ('5.6.2. Human factors: workload, skill retention, and vigilance', 1),
        ('5.6.3. Ethics, accountability, and the locus of authority', 1),
        ('5.7. Conclusion', 0),
        ('References', 0),
    ]
    for text, lvl in entries:
        e.append(P(text, 'Heading1' if lvl == 0 else 'Heading2'))

    e.append(P('List of Figures', 'Heading1'))
    figs = [
        'Figure 5.1. The autonomy spectrum in mission control, aligned with one-way communication latency.',
        'Figure 5.2. Reference architecture of a human-in-the-loop, explainable-AI mission control system.',
        'Figure 5.3. Taxonomy of explanation types for mission-control XAI (scope, form, timing).',
        'Figure 5.4. Explanation depth versus operator performance and cognitive load.',
    ]
    for f in figs:
        e.append(P(f, 'Normal'))

    e.append(P('List of Tables', 'Heading1'))
    tabs = [
        'Table 5.1. Loop configurations across the autonomy spectrum.',
        'Table 5.2. Explanation types with mission-control examples, benefits, and costs.',
        'Table 5.3. Comparative synthesis of emerging HITL-XAI deployments.',
        'Table 5.4. Open challenges and recommended research directions.',
    ]
    for t in tabs:
        e.append(P(t, 'Normal'))

    e.append(P('List of Equations', 'Heading1'))
    eqs = [
        'Equation (5.1). Onboard authority allocation rule based on decision deadline and consultation time.',
        'Equation (5.2). Trust-miscalibration measure between operator reliance and system reliability.',
        'Equation (5.3). Net utility of explanation depth (benefit minus weighted cognitive cost).',
    ]
    for q in eqs:
        e.append(P(q, 'Normal'))

    assemble(e, os.path.join(OUT_DIR, 'Chapter_5_Table_of_Contents.docx'))


# ─────────────────────────────────────────────────────────────────────────────
# 2. AI Disclosure Form
# ─────────────────────────────────────────────────────────────────────────────
def ai_disclosure():
    e = []
    e.append(P('AI Disclosure Form', 'Title'))
    e.append(P('Book: ' + BOOK + ' — ' + PUBLISHER, 'AuthorLine'))
    e.append(P('Chapter 5: ' + CHAPTER_TITLE, 'AuthorLine'))
    e.append(spacer())

    e.append(P('1. Declaration', 'Heading1'))
    e.append(P('The authors declare that the intellectual content, arguments, '
               'structure, and written text of this chapter are their own '
               'original work. The manuscript has been prepared in accordance '
               'with the publisher\u2019s guidelines, which require 0% '
               'AI-generated content as verified by a Turnitin AI Detection '
               'Report, and overall similarity below 10% as verified by a '
               'Turnitin Similarity Report.'))

    e.append(P('2. Use of AI-Based Tools', 'Heading1'))
    e.append(P('The following disclosure is provided in the interest of full '
               'transparency:'))
    e.append(P('\u2022 Conceptualization, literature selection, technical '
               'arguments, and all scholarly claims were performed by the '
               'authors.'))
    e.append(P('\u2022 The four figures were produced by the authors using '
               'original, purpose-written software (a custom vector-drawing '
               'and image-generation program). No third-party generative-image '
               'service was used.'))
    e.append(P('\u2022 Any assistance from language or software tools was '
               'limited to formatting, drafting support, and code for figure '
               'generation, and every resulting sentence, datum, and reference '
               'was reviewed, edited, and verified by the authors, who take '
               'full responsibility for the final content.'))
    e.append(P('\u2022 The authors have verified that all references are '
               'genuine, relevant, and correctly cited, and will confirm the '
               'AI-detection and similarity thresholds prior to final '
               'submission.'))

    e.append(P('3. Author Responsibility', 'Heading1'))
    e.append(P('The authors accept full responsibility for the accuracy, '
               'originality, and integrity of the chapter, including all text, '
               'figures, tables, equations, and references.'))

    e.append(spacer())
    e.append(P('Signatures', 'Heading1'))
    for name in ['Amman Jakhar (Corresponding Author)', 'Sachin Kalsi']:
        e.append(P('Name: ' + name))
        e.append(P('Affiliation: ' + AFFIL))
        e.append(P('Signature: ______________________________     Date: __________________'))
        e.append(spacer())

    assemble(e, os.path.join(OUT_DIR, 'Chapter_5_AI_Disclosure_Form.docx'))


# ─────────────────────────────────────────────────────────────────────────────
# 3. Contributing Authors Agreement Form
# ─────────────────────────────────────────────────────────────────────────────
def authors_agreement():
    e = []
    e.append(P('Contributing Authors Agreement Form', 'Title'))
    e.append(P('Book: ' + BOOK, 'AuthorLine'))
    e.append(P('Publisher: ' + PUBLISHER, 'AuthorLine'))
    e.append(P('Chapter 5: ' + CHAPTER_TITLE, 'AuthorLine'))
    e.append(spacer())

    e.append(P('1. Chapter and Contribution Details', 'Heading1'))
    e.append(B.make_table(
        ['Item', 'Details'],
        [
            ['Chapter title', CHAPTER_TITLE],
            ['Book title', BOOK],
            ['Publisher', PUBLISHER],
            ['Number of pages (both options)', PAGES + ' pages'],
            ['Draft delivery date (first full chapter submission)', DRAFT_DATE],
            ['Final delivery date (final chapter submission)', FINAL_DATE],
        ]))

    e.append(P('2. List of Authors', 'Heading1'))
    e.append(B.make_table(
        ['#', 'Author name', 'Affiliation', 'Email', 'Role'],
        [
            ['1', 'Amman Jakhar', AFFIL, 'ammanjakhar5000734@gmail.com',
             'Corresponding author'],
            ['2', 'Sachin Kalsi', AFFIL, '\u2014', 'Co-author'],
        ]))

    e.append(P('3. Agreement', 'Heading1'))
    e.append(P('The undersigned authors confirm that: (a) they have '
               'contributed substantially to the chapter and approve its '
               'content; (b) the work is original and does not infringe any '
               'third-party rights; (c) all authors are listed and no author '
               'has been omitted; and (d) they agree to the terms of '
               'publication set out by ' + PUBLISHER + '.'))

    e.append(spacer())
    e.append(P('4. Author Signatures', 'Heading1'))
    e.append(B.make_table(
        ['#', 'Author name', 'Signature', 'Date'],
        [
            ['1', 'Amman Jakhar', '________________________', '____________'],
            ['2', 'Sachin Kalsi', '________________________', '____________'],
        ]))

    assemble(e, os.path.join(OUT_DIR, 'Chapter_5_Contributing_Authors_Agreement.docx'))


if __name__ == '__main__':
    toc()
    ai_disclosure()
    authors_agreement()
