#!/usr/bin/env python3
"""
Create a Word .docx file for the manuscript
"Leakage-Free, Physics-Constrained Prediction of Silica-Fume SCC Strength".

Reuses the raw-OOXML converter in create_agentic_docx.py (python-docx is not
available in this sandbox). The manuscript has no figures, so no images are
embedded.

Usage:
    python3 create_sf_scc_docx.py
"""

import os

import create_agentic_docx as conv

HERE = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(HERE, 'Manuscript_LeakageFree_SF_SCC_Strength.md')
DOCX_FILE = os.path.join(HERE, 'Manuscript_LeakageFree_SF_SCC_Strength.docx')

if __name__ == '__main__':
    conv.FIGURE_FILES = {}
    conv.create_docx(MD_FILE, DOCX_FILE)
