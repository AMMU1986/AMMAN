#!/usr/bin/env python3
"""
Build Word (.docx) files for the two Klein-Gordon thermoelasticity manuscripts,
embedding their figures.  Reuses the raw-OOXML converter in
create_agentic_docx.py (python-docx is not available in this sandbox).

Usage:
    python3 create_kg_manuscripts_docx.py
"""

import create_agentic_docx as conv

BASE = '/projects/sandbox/AMMAN'

JOBS = [
    {
        'md': f'{BASE}/Manuscript_KG_Stop_Bands_Thermoelastic_Waves.md',
        'docx': f'{BASE}/Manuscript_KG_Stop_Bands_Thermoelastic_Waves.docx',
        'fig_dir': f'{BASE}/kg_stopband_figures',
        'figures': {
            1: 'Figure_1_Regime_Map.png',
            2: 'Figure_2_Elastic_P_Wave.png',
            3: 'Figure_3_Shear_Wave.png',
            4: 'Figure_4_Phase_Group_Velocity.png',
            5: 'Figure_5_Thermal_Mode.png',
            6: 'Figure_6_Elastic_Mode_Decay_and_Gain.png',
            7: 'Figure_7_Tau1_Parametric.png',
            8: 'Figure_8_Asymptotic_Validation.png',
        },
    },
    {
        'md': f'{BASE}/Manuscript_KG_Stability_Domain_of_Influence.md',
        'docx': f'{BASE}/Manuscript_KG_Stability_Domain_of_Influence.docx',
        'fig_dir': f'{BASE}/kg_stability_figures',
        'figures': {
            1: 'Figure_1_Elastic_Spectrum_and_Growth_Band.png',
            2: 'Figure_2_First_Order_Growth_Law.png',
            3: 'Figure_3_Growth_vs_Coupling_and_Tau1.png',
            4: 'Figure_4_Growth_Rate_vs_k.png',
            5: 'Figure_5_Energy_Consistent_Window.png',
        },
    },
]


def main():
    for job in JOBS:
        conv.FIG_DIR = job['fig_dir']
        conv.FIGURE_FILES = job['figures']
        conv.create_docx(job['md'], job['docx'])


if __name__ == '__main__':
    main()
