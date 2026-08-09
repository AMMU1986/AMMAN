"""
Generate 4 figures for Chapter: AI and Climate Action
For: Aligning Innovation with SDGs for Business Growth: Age of Artificial Intelligence
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

os.makedirs('/projects/sandbox/AMMAN/ai_climate_figures', exist_ok=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11


# ============================================================
# Figure 1: AI-Enabled Climate Action Framework
# ============================================================
def create_figure1():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 11)
    ax.axis('off')
    ax.set_title('Figure 1: AI-Enabled Climate Action Framework — Integrating Monitoring,\n'
                 'Mitigation, Adaptation, and Governance for SDG 13',
                 fontsize=12, fontweight='bold', pad=15)

    # Central hub
    circle = plt.Circle((7, 5.5), 1.4, color='#1a5276', alpha=0.15, linewidth=2)
    ax.add_patch(circle)
    circle_edge = plt.Circle((7, 5.5), 1.4, fill=False, color='#1a5276', linewidth=2.5)
    ax.add_patch(circle_edge)
    ax.text(7, 5.8, 'AI for', ha='center', va='center', fontsize=13, fontweight='bold', color='#1a5276')
    ax.text(7, 5.2, 'Climate Action', ha='center', va='center', fontsize=12, fontweight='bold', color='#1a5276')
    ax.text(7, 4.7, '(SDG 13)', ha='center', va='center', fontsize=10, color='#555')

    # Four quadrants
    quadrants = [
        {'name': 'Climate Monitoring\n& Modelling', 'x': 2.5, 'y': 9, 'color': '#2980b9',
         'items': ['Satellite data analysis', 'Climate prediction', 'Carbon tracking', 'Risk assessment']},
        {'name': 'Climate Mitigation\n& Decarbonization', 'x': 11.5, 'y': 9, 'color': '#27ae60',
         'items': ['Renewable energy opt.', 'Smart grid mgmt.', 'Industrial efficiency', 'Circular economy']},
        {'name': 'Climate Adaptation\n& Resilience', 'x': 2.5, 'y': 2, 'color': '#e67e22',
         'items': ['Early warning systems', 'Climate-smart agriculture', 'Water management', 'Disaster response']},
        {'name': 'Responsible AI &\nBusiness Growth', 'x': 11.5, 'y': 2, 'color': '#8e44ad',
         'items': ['Green AI computing', 'Climate finance', 'AI governance', 'SDG-aligned innovation']},
    ]

    for q in quadrants:
        rect = FancyBboxPatch((q['x']-1.8, q['y']-1.5), 3.6, 3.0,
                              boxstyle="round,pad=0.1",
                              facecolor=q['color'], alpha=0.12, edgecolor=q['color'], linewidth=2)
        ax.add_patch(rect)
        ax.text(q['x'], q['y']+0.9, q['name'], ha='center', va='center',
                fontsize=10, fontweight='bold', color=q['color'])
        for i, item in enumerate(q['items']):
            ax.text(q['x'], q['y']-0.0 - i*0.45, f'• {item}', ha='center', va='center',
                    fontsize=8, color='#333')

        # Connection lines to center
        dx = 7 - q['x']
        dy = 5.5 - q['y']
        dist = np.sqrt(dx**2 + dy**2)
        start_x = q['x'] + dx/dist * 2.0
        start_y = q['y'] + dy/dist * 1.6
        end_x = 7 - dx/dist * 1.5
        end_y = 5.5 - dy/dist * 1.5
        ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                    arrowprops=dict(arrowstyle='->', color=q['color'], lw=1.5, linestyle='--'))

    # Bottom banner
    ax.text(7, 0.3, 'Aligned with: Paris Agreement | UNFCCC | SDG 13: Climate Action | Green Deal | Net-Zero Targets',
            ha='center', fontsize=9, style='italic', color='#555',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f9fa', edgecolor='#bdc3c7'))

    plt.tight_layout()
    plt.savefig('/projects/sandbox/AMMAN/ai_climate_figures/Figure_1_AI_Climate_Framework.png',
                dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 1 created successfully")


# ============================================================
# Figure 2: AI Applications in Climate Mitigation
# ============================================================
def create_figure2():
    fig, ax = plt.subplots(1, 1, figsize=(13, 7))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_title('Figure 2: AI-Driven Solutions for Climate Mitigation Across Key Sectors',
                 fontsize=12, fontweight='bold', pad=15)

    sectors = [
        {'name': 'Energy Systems', 'x': 2, 'color': '#f39c12',
         'apps': ['Solar/wind forecasting', 'Smart grid optimization', 'Demand response', 'Battery management']},
        {'name': 'Transportation', 'x': 5.5, 'color': '#2ecc71',
         'apps': ['Route optimization', 'Autonomous EVs', 'Traffic flow AI', 'Fleet electrification']},
        {'name': 'Industry', 'x': 9, 'color': '#3498db',
         'apps': ['Process optimization', 'Predictive maintenance', 'Carbon capture', 'Supply chain AI']},
        {'name': 'Buildings', 'x': 12.5, 'color': '#9b59b6',
         'apps': ['HVAC optimization', 'Smart lighting', 'Energy auditing AI', 'Digital twins']},
    ]

    # Top: AI Technologies bar
    ai_bar = FancyBboxPatch((0.5, 7.2), 15, 1.3, boxstyle="round,pad=0.1",
                            facecolor='#1a5276', alpha=0.1, edgecolor='#1a5276', linewidth=2)
    ax.add_patch(ai_bar)
    ax.text(8, 8.1, 'AI Technologies: Deep Learning | Reinforcement Learning | Digital Twins | NLP | Computer Vision',
            ha='center', va='center', fontsize=9, fontweight='bold', color='#1a5276')
    ax.text(8, 7.6, 'Optimization | Federated Learning | Generative AI | Edge AI | Transfer Learning',
            ha='center', va='center', fontsize=8.5, color='#333')

    for s in sectors:
        # Sector box
        rect = FancyBboxPatch((s['x']-1.3, 2.5), 2.6, 4.2,
                              boxstyle="round,pad=0.08",
                              facecolor=s['color'], alpha=0.12, edgecolor=s['color'], linewidth=1.5)
        ax.add_patch(rect)
        ax.text(s['x'], 6.2, s['name'], ha='center', va='center',
                fontsize=10, fontweight='bold', color=s['color'])

        for i, app in enumerate(s['apps']):
            ax.text(s['x'], 5.4 - i*0.7, f'• {app}', ha='center', va='center', fontsize=8, color='#333')

        # Arrow from AI bar
        ax.annotate('', xy=(s['x'], 6.7), xytext=(s['x'], 7.2),
                    arrowprops=dict(arrowstyle='->', color=s['color'], lw=1.5))

    # Bottom: Impact metrics
    impact_bar = FancyBboxPatch((0.5, 0.3), 15, 1.8, boxstyle="round,pad=0.1",
                                facecolor='#27ae60', alpha=0.08, edgecolor='#27ae60', linewidth=1.5)
    ax.add_patch(impact_bar)
    ax.text(8, 1.7, 'Estimated CO₂ Reduction Potential (by 2030)', ha='center',
            fontsize=10, fontweight='bold', color='#27ae60')

    impacts = [('Energy: 2.1 Gt', 2), ('Transport: 1.7 Gt', 5.5),
               ('Industry: 1.3 Gt', 9), ('Buildings: 0.8 Gt', 12.5)]
    for label, x in impacts:
        ax.text(x, 0.9, label, ha='center', fontsize=9, color='#333',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#27ae60', alpha=0.8))

    # Arrows from sectors to impact
    for s in sectors:
        ax.annotate('', xy=(s['x'], 2.1), xytext=(s['x'], 2.5),
                    arrowprops=dict(arrowstyle='->', color='#27ae60', lw=1))

    plt.tight_layout()
    plt.savefig('/projects/sandbox/AMMAN/ai_climate_figures/Figure_2_AI_Mitigation_Sectors.png',
                dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 2 created successfully")


# ============================================================
# Figure 3: AI for Climate Adaptation and Resilience
# ============================================================
def create_figure3():
    fig, ax = plt.subplots(1, 1, figsize=(13, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 11)
    ax.axis('off')
    ax.set_title('Figure 3: AI-Powered Climate Adaptation and Resilience Systems',
                 fontsize=12, fontweight='bold', pad=15)

    # Three layers
    layers = [
        {'name': 'DATA LAYER', 'y': 9.5, 'color': '#2980b9', 'height': 1.8,
         'items': ['Satellite Imagery', 'IoT Sensors', 'Weather Stations', 'Social Media', 'Historical Records']},
        {'name': 'AI PROCESSING LAYER', 'y': 6.5, 'color': '#8e44ad', 'height': 2.2,
         'items': ['Pattern Recognition', 'Predictive Models', 'Computer Vision', 'NLP Analysis', 'Simulation']},
        {'name': 'APPLICATION LAYER', 'y': 3.0, 'color': '#e67e22', 'height': 2.8,
         'items': ['Early Warning', 'Smart Agriculture', 'Water Mgmt', 'Disaster Response', 'Urban Planning']},
    ]

    for layer in layers:
        rect = FancyBboxPatch((0.5, layer['y'] - layer['height']/2), 13, layer['height'],
                              boxstyle="round,pad=0.1",
                              facecolor=layer['color'], alpha=0.08, edgecolor=layer['color'], linewidth=2)
        ax.add_patch(rect)
        ax.text(0.9, layer['y'] + layer['height']/2 - 0.3, layer['name'],
                fontsize=9, fontweight='bold', color=layer['color'], va='top')

        # Items
        item_width = 12.0 / len(layer['items'])
        for i, item in enumerate(layer['items']):
            x_pos = 1.5 + i * item_width + item_width/2
            item_rect = FancyBboxPatch((x_pos - 1.0, layer['y'] - 0.5), 2.0, 0.8,
                                       boxstyle="round,pad=0.05",
                                       facecolor=layer['color'], alpha=0.15, edgecolor=layer['color'], linewidth=1)
            ax.add_patch(item_rect)
            ax.text(x_pos, layer['y'] - 0.1, item, ha='center', va='center', fontsize=7.5, color='#333')

    # Arrows between layers
    for x in [3, 5.5, 8, 10.5]:
        ax.annotate('', xy=(x, 7.8), xytext=(x, 8.5),
                    arrowprops=dict(arrowstyle='->', color='#555', lw=1.2))
        ax.annotate('', xy=(x, 4.8), xytext=(x, 5.3),
                    arrowprops=dict(arrowstyle='->', color='#555', lw=1.2))

    # Bottom: Outcomes
    outcome_rect = FancyBboxPatch((0.5, 0.3), 13, 1.2, boxstyle="round,pad=0.1",
                                  facecolor='#27ae60', alpha=0.1, edgecolor='#27ae60', linewidth=1.5)
    ax.add_patch(outcome_rect)
    ax.text(7, 1.1, 'Outcomes: Reduced Vulnerability | Enhanced Preparedness | Climate-Resilient Communities | Adaptive Capacity',
            ha='center', va='center', fontsize=9, fontweight='bold', color='#27ae60')
    ax.text(7, 0.6, 'Supporting SDG 13 Targets: 13.1 (Resilience) | 13.2 (Integration) | 13.3 (Education & Awareness)',
            ha='center', va='center', fontsize=8, color='#555')

    plt.tight_layout()
    plt.savefig('/projects/sandbox/AMMAN/ai_climate_figures/Figure_3_AI_Adaptation_Resilience.png',
                dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 3 created successfully")


# ============================================================
# Figure 4: Responsible AI and Future Directions for Climate-Business Alignment
# ============================================================
def create_figure4():
    fig, ax = plt.subplots(1, 1, figsize=(12, 9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 12)
    ax.axis('off')
    ax.set_title('Figure 4: Responsible AI and Business Growth Pathways\nfor Sustainable Climate Action',
                 fontsize=12, fontweight='bold', pad=15)

    # Timeline/roadmap style
    phases = [
        {'name': 'Phase 1: Foundation\n(2020-2023)', 'y': 10, 'color': '#3498db',
         'items': ['Green AI awareness', 'Carbon footprint tools', 'ESG reporting AI', 'Basic climate models']},
        {'name': 'Phase 2: Scaling\n(2023-2025)', 'y': 7.5, 'color': '#27ae60',
         'items': ['AI-enabled carbon markets', 'Federated climate learning', 'Digital twin cities', 'Climate finance AI']},
        {'name': 'Phase 3: Transformation\n(2025-2028)', 'y': 5, 'color': '#e67e22',
         'items': ['Autonomous climate systems', 'Global carbon intelligence', 'AI governance frameworks', 'Net-zero AI platforms']},
        {'name': 'Phase 4: Integration\n(2028-2030+)', 'y': 2.5, 'color': '#8e44ad',
         'items': ['AGI for climate', 'Planetary digital twin', 'Self-optimizing systems', 'Full SDG alignment']},
    ]

    for phase in phases:
        # Phase box
        rect = FancyBboxPatch((0.5, phase['y']-0.8), 3.5, 1.6, boxstyle="round,pad=0.1",
                              facecolor=phase['color'], alpha=0.2, edgecolor=phase['color'], linewidth=2)
        ax.add_patch(rect)
        ax.text(2.25, phase['y'], phase['name'], ha='center', va='center',
                fontsize=9, fontweight='bold', color=phase['color'])

        # Items
        for i, item in enumerate(phase['items']):
            x_pos = 5.5 + i * 1.8
            item_rect = FancyBboxPatch((x_pos - 0.8, phase['y']-0.4), 1.6, 0.8,
                                       boxstyle="round,pad=0.05",
                                       facecolor=phase['color'], alpha=0.1, edgecolor=phase['color'], linewidth=1)
            ax.add_patch(item_rect)
            ax.text(x_pos, phase['y'], item, ha='center', va='center', fontsize=7, color='#333')

        # Arrow to items
        ax.annotate('', xy=(4.5, phase['y']), xytext=(4.0, phase['y']),
                    arrowprops=dict(arrowstyle='->', color=phase['color'], lw=1.5))

    # Vertical progression arrows
    for i in range(3):
        y_start = phases[i]['y'] - 0.8
        y_end = phases[i+1]['y'] + 0.8
        ax.annotate('', xy=(2.25, y_end), xytext=(2.25, y_start),
                    arrowprops=dict(arrowstyle='->', color='#555', lw=2))

    # Right side: principles
    principles_rect = FancyBboxPatch((10.5, 1.5), 1.3, 9.5, boxstyle="round,pad=0.1",
                                     facecolor='#1a5276', alpha=0.08, edgecolor='#1a5276', linewidth=1.5)
    ax.add_patch(principles_rect)
    ax.text(11.15, 11.2, 'Guiding\nPrinciples', ha='center', fontsize=8, fontweight='bold', color='#1a5276')

    principles = ['Ethics', 'Equity', 'Transparency', 'Sustainability', 'Accountability']
    for i, p in enumerate(principles):
        ax.text(11.15, 10 - i*1.6, p, ha='center', fontsize=7.5, color='#1a5276', rotation=0,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#d6eaf8', edgecolor='#1a5276', alpha=0.6))

    # Bottom label
    ax.text(6, 0.5, 'Business Growth + Climate Action + AI Innovation = Sustainable Development (SDG 13)',
            ha='center', fontsize=10, fontweight='bold', color='#1a5276',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#eafaf1', edgecolor='#27ae60'))

    plt.tight_layout()
    plt.savefig('/projects/sandbox/AMMAN/ai_climate_figures/Figure_4_Responsible_AI_Future.png',
                dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 4 created successfully")


# Generate all figures
create_figure1()
create_figure2()
create_figure3()
create_figure4()
print("\nAll 4 figures generated successfully!")
