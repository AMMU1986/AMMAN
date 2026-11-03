#!/usr/bin/env python3
"""
Create a Word .docx file for the chapter
"Comparative and Structural Bioinformatics of Enzymes".

Reuses the raw-OOXML builder and figure-embedding logic from
create_agentic_docx.py (python-docx is not available in this sandbox) and
embeds the five generated figures inline at the "[Insert Figure N here]"
placeholders.

Usage:
    python3 create_structural_bioinformatics_docx.py
"""

import os

import create_agentic_docx as base

MD_FILE = '/projects/sandbox/AMMAN/Chapter_Structural_Bioinformatics_Enzymes.md'
DOCX_FILE = '/projects/sandbox/AMMAN/Chapter_Structural_Bioinformatics_Enzymes.docx'
FIG_DIR = '/projects/sandbox/AMMAN/structural_figures'

FIGURE_FILES = {
    1: 'Figure_1_Comparative_Workflow.png',
    2: 'Figure_2_Structure_Routes.png',
    3: 'Figure_3_Druggability.png',
    4: 'Figure_4_Dynamics.png',
    5: 'Figure_5_Integrated_Pipeline.png',
}


if __name__ == '__main__':
    # Point the shared builder at this chapter's figures and output.
    base.MD_FILE = MD_FILE
    base.DOCX_FILE = DOCX_FILE
    base.FIG_DIR = FIG_DIR
    base.FIGURE_FILES = FIGURE_FILES
    base.create_docx(MD_FILE, DOCX_FILE)
