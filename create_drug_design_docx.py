#!/usr/bin/env python3
"""
Create a Word .docx file for Chapter 5 "Machine Learning for Drug Design".

Reuses the raw-OOXML builder from create_agentic_docx.py (python-docx is not
available in this sandbox) and embeds the four generated figures inline where
the "[Insert Figure N here]" placeholders appear.

Usage:
    python3 create_drug_design_docx.py
"""

import os

import create_agentic_docx as base

MD_FILE = '/projects/sandbox/AMMAN/Chapter_ML_Drug_Design.md'
DOCX_FILE = '/projects/sandbox/AMMAN/Chapter_5_ML_Drug_Design.docx'
FIG_DIR = '/projects/sandbox/AMMAN/drug_design_figures'

FIGURE_FILES = {
    1: 'Figure_1_Drug_Design_Workflow.png',
    2: 'Figure_2_Generative_Loop.png',
    3: 'Figure_3_ML_Task_Taxonomy.png',
    4: 'Figure_4_ADMET_Filter.png',
}

if __name__ == '__main__':
    # Point the shared builder at this chapter's figures and paths.
    base.FIG_DIR = FIG_DIR
    base.FIGURE_FILES = FIGURE_FILES
    base.create_docx(MD_FILE, DOCX_FILE)
