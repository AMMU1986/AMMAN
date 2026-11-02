#!/usr/bin/env python3
"""
Build the Word .docx for "AI-Powered Digital Marketing for Sustainability"
(Chapter ID ADSM-2), embedding the four figures.

Reuses the raw-OOXML builder in create_agentic_docx.py by pointing its
module-level settings at this chapter's files.

Usage:
    python3 generate_sustainable_marketing_figures.py
    python3 create_sustainable_marketing_docx.py
"""

import create_agentic_docx as builder

BASE = '/projects/sandbox/AMMAN'
MD_FILE = f'{BASE}/Chapter_AI_Powered_Digital_Marketing_Sustainability.md'
DOCX_FILE = f'{BASE}/Chapter_AI_Powered_Digital_Marketing_Sustainability.docx'

builder.FIG_DIR = f'{BASE}/sustainable_marketing_figures'
builder.FIGURE_FILES = {
    1: 'Figure_1_Conceptual_Model.png',
    2: 'Figure_2_AI_Technology_Pipeline.png',
    3: 'Figure_3_Double_Edged_Sword.png',
    4: 'Figure_4_Governance_Cycle.png',
}

if __name__ == '__main__':
    builder.create_docx(MD_FILE, DOCX_FILE)
