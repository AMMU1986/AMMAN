#!/usr/bin/env python3
"""
Create a Word .docx for the chapter
"Explainable and Federated Artificial Intelligence for Secure Clinical
 Decision Support in Next-Generation Healthcare Systems".

Reuses the raw-OOXML builder from create_agentic_docx.py (python-docx is not
available in this sandbox) and embeds the generated 300-dpi figures inline at
the "[Insert Figure N here]" placeholders.

Usage:
    python3 create_xfl_docx.py
"""

import create_agentic_docx as base

MD_FILE = '/projects/sandbox/AMMAN/Chapter_Explainable_Federated_AI_Clinical.md'
DOCX_FILE = '/projects/sandbox/AMMAN/Chapter_Explainable_Federated_AI_Clinical.docx'
FIG_DIR = '/projects/sandbox/AMMAN/xfl_figures'

FIGURE_FILES = {
    1: 'Figure_1_Evolution_AI_CDS.png',
    2: 'Figure_2_Federated_Architecture.png',
    3: 'Figure_3_XAI_Taxonomy.png',
    4: 'Figure_4_XFL_Framework.png',
}

# Point the shared builder at this chapter's figure assets.
base.FIG_DIR = FIG_DIR
base.FIGURE_FILES = FIGURE_FILES

if __name__ == '__main__':
    base.create_docx(MD_FILE, DOCX_FILE)
