#!/usr/bin/env python3
"""
Create a Word .docx file for the chapter
"AI-Powered Digital Marketing for Sustainability".

Reuses the raw-OOXML builder established in create_intersectionality_docx.py
(python-docx is not available in this sandbox). Markdown pipe tables are
rendered as native Word tables and the generated figures are embedded inline
where the "[Insert Figure N here]" placeholders appear.

Usage:
    python3 create_ai_marketing_docx.py
"""

import create_intersectionality_docx as base

MD_FILE = '/projects/sandbox/AMMAN/Chapter_AI_Digital_Marketing_Sustainability.md'
DOCX_FILE = '/projects/sandbox/AMMAN/Chapter_AI_Digital_Marketing_Sustainability.docx'
FIG_DIR = '/projects/sandbox/AMMAN/ai_marketing_figures'

FIGURE_FILES = {
    1: 'Figure_1_Convergence.png',
    2: 'Figure_2_Consumer_Journey.png',
    3: 'Figure_3_Footprint_Paradox.png',
    4: 'Figure_4_Responsible_Framework.png',
}

# Redirect the shared builder's module-level paths to this chapter's assets.
base.MD_FILE = MD_FILE
base.DOCX_FILE = DOCX_FILE
base.FIG_DIR = FIG_DIR
base.FIGURE_FILES = FIGURE_FILES


if __name__ == '__main__':
    base.create_docx(MD_FILE, DOCX_FILE)
