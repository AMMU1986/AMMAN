#!/usr/bin/env python3
"""
Create a Word .docx file for the chapter
"Sequence Analysis, Motif Discovery, and Functional Annotation".

Reuses the raw-OOXML builder and figure-embedding logic from
create_agentic_docx.py (python-docx is not available in this sandbox) and
embeds the five generated figures inline at the "[Insert Figure N here]"
placeholders.

Usage:
    python3 create_sequence_annotation_docx.py
"""

import create_agentic_docx as base

MD_FILE = '/projects/sandbox/AMMAN/Chapter_Sequence_Analysis_Motif_Annotation.md'
DOCX_FILE = '/projects/sandbox/AMMAN/Chapter_Sequence_Analysis_Motif_Annotation.docx'
FIG_DIR = '/projects/sandbox/AMMAN/sequence_figures'

FIGURE_FILES = {
    1: 'Figure_1_Orthology_Paralogy.png',
    2: 'Figure_2_Conservation_Profile.png',
    3: 'Figure_3_Template_Matching.png',
    4: 'Figure_4_Pathway_Context.png',
    5: 'Figure_5_Prioritization.png',
}


if __name__ == '__main__':
    base.MD_FILE = MD_FILE
    base.DOCX_FILE = DOCX_FILE
    base.FIG_DIR = FIG_DIR
    base.FIGURE_FILES = FIGURE_FILES
    base.create_docx(MD_FILE, DOCX_FILE)
