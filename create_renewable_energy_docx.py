#!/usr/bin/env python3
"""
Create a Word .docx file for the chapter
"Renewable Energy Integration and Forecasting".

Reuses the raw-OOXML builder and figure-embedding logic from
create_agentic_docx.py (python-docx is not available in this sandbox) and
embeds the five generated figures inline at the "[Insert Figure N here]"
placeholders.

Usage:
    python3 create_renewable_energy_docx.py
"""

import create_agentic_docx as base

MD_FILE = '/projects/sandbox/AMMAN/Chapter_Renewable_Energy_Integration_Forecasting.md'
DOCX_FILE = '/projects/sandbox/AMMAN/Chapter_Renewable_Energy_Integration_Forecasting.docx'
FIG_DIR = '/projects/sandbox/AMMAN/renewable_figures'

FIGURE_FILES = {
    1: 'Figure_1_Smart_Grid_Architecture.png',
    2: 'Figure_2_LSTM_Cell.png',
    3: 'Figure_3_Data_Flow.png',
    4: 'Figure_4_Energy_Management_Loop.png',
    5: 'Figure_5_Federated_Learning.png',
}


if __name__ == '__main__':
    base.MD_FILE = MD_FILE
    base.DOCX_FILE = DOCX_FILE
    base.FIG_DIR = FIG_DIR
    base.FIGURE_FILES = FIGURE_FILES
    base.create_docx(MD_FILE, DOCX_FILE)
