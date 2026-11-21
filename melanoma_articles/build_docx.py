#!/usr/bin/env python3
"""Build .docx files for the three melanoma articles, reusing the raw-OOXML
converter in ../create_intersectionality_docx.py (python-docx is unavailable)."""
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import create_intersectionality_docx as conv  # noqa: E402

ARTICLES = [
    ('Article_1_Surgery_Triggered_Recurrence', 'article1_figures', [
        'Figure_1_Resection_Recurrence.png', 'Figure_2_Fate_Map_Margin.png',
        'Figure_3_Immunotherapy_Timing.png', 'Figure_4_Continuous_Adjuvant.png']),
    ('Article_2_Immune_Angiogenic_Switch', 'article2_figures', [
        'Figure_1_Two_Phase_Growth.png', 'Figure_2_TAF_Profiles.png', 'Figure_3_Dormancy_Scaling.png',
        'Figure_4_Phase_Diagram.png', 'Figure_5_Anti_VEGF_Schedules.png']),
    ('Article_3_Immune_Halo_Stochastic_Seeding', 'article3_figures', [
        'Figure_1_Immune_Halo_Map.png', 'Figure_2_Monte_Carlo_Seeding.png',
        'Figure_3_Stochastic_Example.png', 'Figure_4_Margin.png']),
]


def preprocess(md):
    """Adapt markdown features the converter does not handle."""
    md = re.sub(r'^- ', '\u2022 ', md, flags=re.M)   # bullets
    md = md.replace('`', '')                           # inline code
    return md


for stem, figdir, figs in ARTICLES:
    md_path = os.path.join(HERE, stem + '.md')
    conv.FIG_DIR = os.path.join(HERE, figdir)
    conv.FIGURE_FILES = {i + 1: f for i, f in enumerate(figs)}
    with open(md_path, encoding='utf-8') as f:
        text = preprocess(f.read())
    with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8') as tmp:
        tmp.write(text)
    try:
        conv.create_docx(tmp.name, os.path.join(HERE, stem + '.docx'))
    finally:
        os.unlink(tmp.name)
