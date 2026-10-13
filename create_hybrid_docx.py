#!/usr/bin/env python3
"""
Build the Word (.docx) for the Al7075-SiC/Gr + Al2O3 nanofluid bearing paper,
reusing the native-OMML docx builder from create_tehd_docx.py.
"""

import create_tehd_docx as b

b.SRC = '/projects/sandbox/AMMAN/Research_Article_Al7075_SiC_Gr_Al2O3_Bearing.md'
b.OUT = '/projects/sandbox/AMMAN/Research_Article_Al7075_SiC_Gr_Al2O3_Bearing.docx'
b.FIGDIR = '/projects/sandbox/AMMAN/hybrid_figures'
b.FIGS = {
    1: 'Fig1_schematic.png',
    2: 'Fig2_methodology_flowchart.png',
    3: 'Fig3_nanofluid_properties.png',
    4: 'Fig4_pressure_distribution.png',
    5: 'Fig5_friction_wear.png',
    6: 'Fig6_temperature.png',
    7: 'Fig7_fea_stress.png',
}

if __name__ == '__main__':
    b.build_docx()
