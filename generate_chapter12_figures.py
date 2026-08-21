"""
Generate 4 figures for Chapter 12: Industrial Translation, AI Integration, and Market Potential
of Microbial-Derived Bio-Nanomaterials
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# Create output directory
output_dir = '/projects/sandbox/AMMAN/chapter12_figures'
os.makedirs(output_dir, exist_ok=True)

# Set global style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.2

# =============================================================================
# FIGURE 1: Scale-up pathway from laboratory to industrial production
# =============================================================================
def create_figure1():
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Figure 1: Scale-Up Pathway from Laboratory to Industrial Production\nof Microbial-Derived Bio-Nanomaterials', 
            ha='center', va='center', fontsize=13, fontweight='bold')
    
    # Define stages
    stages = [
        {'x': 1.5, 'y': 6.5, 'w': 2.5, 'h': 2.0, 'color': '#E8F5E9', 'edge': '#4CAF50',
         'title': 'Stage 1\nLaboratory Scale', 
         'details': '• Flask experiments\n• Strain screening\n• Parameter optimization\n• Proof of concept\n• Volume: 0.1-1 L'},
        {'x': 4.5, 'y': 6.5, 'w': 2.5, 'h': 2.0, 'color': '#E3F2FD', 'edge': '#2196F3',
         'title': 'Stage 2\nBench Scale', 
         'details': '• Small bioreactors\n• Process standardization\n• DOE optimization\n• Reproducibility studies\n• Volume: 1-10 L'},
        {'x': 7.5, 'y': 6.5, 'w': 2.5, 'h': 2.0, 'color': '#FFF3E0', 'edge': '#FF9800',
         'title': 'Stage 3\nPilot Scale', 
         'details': '• Pilot bioreactors\n• Process validation\n• Scale-up correlations\n• Quality testing\n• Volume: 10-1000 L'},
        {'x': 10.5, 'y': 6.5, 'w': 2.5, 'h': 2.0, 'color': '#FCE4EC', 'edge': '#E91E63',
         'title': 'Stage 4\nIndustrial Scale', 
         'details': '• Production bioreactors\n• Continuous operation\n• Full QC/QA systems\n• Commercial output\n• Volume: >1000 L'},
    ]
    
    for stage in stages:
        rect = FancyBboxPatch((stage['x'], stage['y']), stage['w'], stage['h'],
                              boxstyle="round,pad=0.1", facecolor=stage['color'], 
                              edgecolor=stage['edge'], linewidth=2)
        ax.add_patch(rect)
        ax.text(stage['x'] + stage['w']/2, stage['y'] + stage['h'] - 0.3, stage['title'],
                ha='center', va='top', fontsize=9, fontweight='bold')
        ax.text(stage['x'] + stage['w']/2, stage['y'] + stage['h'] - 0.9, stage['details'],
                ha='center', va='top', fontsize=7.5)
    
    # Arrows between stages
    for i in range(3):
        x_start = stages[i]['x'] + stages[i]['w']
        x_end = stages[i+1]['x']
        y_mid = stages[i]['y'] + stages[i]['h']/2
        ax.annotate('', xy=(x_end, y_mid), xytext=(x_start, y_mid),
                   arrowprops=dict(arrowstyle='->', lw=2.5, color='#424242'))
    
    # Bottom section - Key considerations
    considerations = [
        {'x': 1.5, 'y': 2.0, 'w': 2.5, 'h': 1.8, 'color': '#F3E5F5', 'edge': '#9C27B0',
         'title': 'Critical Process\nParameters',
         'details': '• Temperature, pH\n• Agitation, aeration\n• Metal precursor conc.\n• Incubation time'},
        {'x': 4.5, 'y': 2.0, 'w': 2.5, 'h': 1.8, 'color': '#E0F7FA', 'edge': '#00BCD4',
         'title': 'Quality\nAttributes',
         'details': '• Particle size & PDI\n• Morphology\n• Zeta potential\n• Crystallinity'},
        {'x': 7.5, 'y': 2.0, 'w': 2.5, 'h': 1.8, 'color': '#FFF9C4', 'edge': '#FFC107',
         'title': 'Downstream\nProcessing',
         'details': '• Centrifugation\n• Ultrafiltration\n• Stabilization\n• Formulation'},
        {'x': 10.5, 'y': 2.0, 'w': 2.5, 'h': 1.8, 'color': '#EFEBE9', 'edge': '#795548',
         'title': 'Economic\nFactors',
         'details': '• Capital costs\n• Operating costs\n• Yield optimization\n• Waste reduction'},
    ]
    
    for cons in considerations:
        rect = FancyBboxPatch((cons['x'], cons['y']), cons['w'], cons['h'],
                              boxstyle="round,pad=0.1", facecolor=cons['color'],
                              edgecolor=cons['edge'], linewidth=1.5)
        ax.add_patch(rect)
        ax.text(cons['x'] + cons['w']/2, cons['y'] + cons['h'] - 0.2, cons['title'],
                ha='center', va='top', fontsize=8.5, fontweight='bold')
        ax.text(cons['x'] + cons['w']/2, cons['y'] + cons['h'] - 0.8, cons['details'],
                ha='center', va='top', fontsize=7.5)
    
    # Connecting arrows from top to bottom
    for i in range(4):
        x_mid = stages[i]['x'] + stages[i]['w']/2
        ax.annotate('', xy=(x_mid, considerations[i]['y'] + considerations[i]['h']),
                   xytext=(x_mid, stages[i]['y']),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='#757575', linestyle='dashed'))
    
    # Label for bottom section
    ax.text(7, 4.2, 'Key Considerations at Each Stage', ha='center', fontsize=11, 
            fontweight='bold', style='italic', color='#424242')
    
    # Scale indicator
    ax.annotate('', xy=(12.5, 5.2), xytext=(1.5, 5.2),
               arrowprops=dict(arrowstyle='->', lw=2, color='#D32F2F'))
    ax.text(7, 5.5, 'Increasing Scale, Complexity, and Investment →', ha='center', 
            fontsize=10, color='#D32F2F', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Figure_1_Scaleup_Pathway.png'), dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 1 saved successfully.")


# =============================================================================
# FIGURE 2: Integrated risk assessment and regulatory decision framework
# =============================================================================
def create_figure2():
    fig, ax = plt.subplots(1, 1, figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title
    ax.text(7, 10.5, 'Figure 2: Integrated Risk Assessment and Regulatory Decision Framework\nfor Microbial-Derived Bio-Nanomaterials',
            ha='center', va='center', fontsize=13, fontweight='bold')
    
    # Central framework - 4 main components
    # Hazard Identification
    box1 = FancyBboxPatch((0.5, 7.0), 3.0, 2.5, boxstyle="round,pad=0.15",
                          facecolor='#FFCDD2', edgecolor='#D32F2F', linewidth=2)
    ax.add_patch(box1)
    ax.text(2.0, 9.2, 'HAZARD\nIDENTIFICATION', ha='center', va='center', 
            fontsize=9, fontweight='bold', color='#B71C1C')
    ax.text(2.0, 8.0, '• Cytotoxicity screening\n• Genotoxicity assessment\n• Immunotoxicity evaluation\n• Microbial contaminants\n• Endotoxin testing',
            ha='center', va='center', fontsize=7.5)
    
    # Exposure Assessment
    box2 = FancyBboxPatch((4.0, 7.0), 3.0, 2.5, boxstyle="round,pad=0.15",
                          facecolor='#C8E6C9', edgecolor='#388E3C', linewidth=2)
    ax.add_patch(box2)
    ax.text(5.5, 9.2, 'EXPOSURE\nASSESSMENT', ha='center', va='center',
            fontsize=9, fontweight='bold', color='#1B5E20')
    ax.text(5.5, 8.0, '• Route of exposure\n• Duration & frequency\n• Concentration levels\n• Environmental fate\n• Bioaccumulation potential',
            ha='center', va='center', fontsize=7.5)
    
    # Dose-Response
    box3 = FancyBboxPatch((7.5, 7.0), 3.0, 2.5, boxstyle="round,pad=0.15",
                          facecolor='#BBDEFB', edgecolor='#1976D2', linewidth=2)
    ax.add_patch(box3)
    ax.text(9.0, 9.2, 'DOSE-RESPONSE\nCHARACTERIZATION', ha='center', va='center',
            fontsize=9, fontweight='bold', color='#0D47A1')
    ax.text(9.0, 8.0, '• IC50/LC50 determination\n• NOAEL/LOAEL values\n• Chronic vs. acute effects\n• Species extrapolation\n• Safety factors',
            ha='center', va='center', fontsize=7.5)
    
    # Risk Characterization
    box4 = FancyBboxPatch((11.0, 7.0), 2.5, 2.5, boxstyle="round,pad=0.15",
                          facecolor='#FFE0B2', edgecolor='#F57C00', linewidth=2)
    ax.add_patch(box4)
    ax.text(12.25, 9.2, 'RISK\nCHARACTERIZATION', ha='center', va='center',
            fontsize=9, fontweight='bold', color='#E65100')
    ax.text(12.25, 8.0, '• Risk quantification\n• Uncertainty analysis\n• Margin of safety\n• Risk classification\n• Communication',
            ha='center', va='center', fontsize=7.5)
    
    # Arrows between boxes
    ax.annotate('', xy=(4.0, 8.25), xytext=(3.5, 8.25),
               arrowprops=dict(arrowstyle='->', lw=2, color='#424242'))
    ax.annotate('', xy=(7.5, 8.25), xytext=(7.0, 8.25),
               arrowprops=dict(arrowstyle='->', lw=2, color='#424242'))
    ax.annotate('', xy=(11.0, 8.25), xytext=(10.5, 8.25),
               arrowprops=dict(arrowstyle='->', lw=2, color='#424242'))
    
    # Regulatory Decision Box (center bottom)
    decision_box = FancyBboxPatch((3.5, 4.0), 7.0, 2.2, boxstyle="round,pad=0.2",
                                  facecolor='#E8EAF6', edgecolor='#303F9F', linewidth=2.5)
    ax.add_patch(decision_box)
    ax.text(7.0, 5.8, 'REGULATORY DECISION & RISK MANAGEMENT', ha='center', va='center',
            fontsize=11, fontweight='bold', color='#1A237E')
    ax.text(7.0, 4.8, '• Product classification (Drug/Device/Cosmetic/Environmental)\n'
            '• Approval pathway selection (FDA/EMA/EPA/REACH)\n'
            '• Required documentation & testing protocols\n'
            '• Post-market surveillance & pharmacovigilance',
            ha='center', va='center', fontsize=8.5)
    
    # Arrow from risk assessment to decision
    ax.annotate('', xy=(7.0, 6.2), xytext=(7.0, 7.0),
               arrowprops=dict(arrowstyle='->', lw=2.5, color='#303F9F'))
    
    # Bottom outcomes
    outcomes = [
        {'x': 1.0, 'y': 1.0, 'w': 3.5, 'h': 2.2, 'color': '#F1F8E9', 'edge': '#689F38',
         'title': 'BIOMEDICAL\nAPPLICATIONS',
         'details': '• IND/NDA pathway\n• Clinical trials (I-III)\n• GMP manufacturing\n• Biocompatibility (ISO 10993)'},
        {'x': 5.25, 'y': 1.0, 'w': 3.5, 'h': 2.2, 'color': '#E0F2F1', 'edge': '#00796B',
         'title': 'ENVIRONMENTAL\nAPPLICATIONS',
         'details': '• EPA/TSCA review\n• Ecotoxicity testing\n• Environmental monitoring\n• Contained use protocols'},
        {'x': 9.5, 'y': 1.0, 'w': 3.5, 'h': 2.2, 'color': '#FBE9E7', 'edge': '#E64A19',
         'title': 'CONSUMER\nPRODUCTS',
         'details': '• REACH registration\n• Safety data sheets\n• Labeling requirements\n• Market surveillance'},
    ]
    
    for out in outcomes:
        rect = FancyBboxPatch((out['x'], out['y']), out['w'], out['h'],
                              boxstyle="round,pad=0.1", facecolor=out['color'],
                              edgecolor=out['edge'], linewidth=1.5)
        ax.add_patch(rect)
        ax.text(out['x'] + out['w']/2, out['y'] + out['h'] - 0.25, out['title'],
                ha='center', va='top', fontsize=8.5, fontweight='bold')
        ax.text(out['x'] + out['w']/2, out['y'] + out['h'] - 0.85, out['details'],
                ha='center', va='top', fontsize=7.5)
    
    # Arrows from decision to outcomes
    ax.annotate('', xy=(2.75, 3.2), xytext=(5.5, 4.0),
               arrowprops=dict(arrowstyle='->', lw=1.8, color='#689F38'))
    ax.annotate('', xy=(7.0, 3.2), xytext=(7.0, 4.0),
               arrowprops=dict(arrowstyle='->', lw=1.8, color='#00796B'))
    ax.annotate('', xy=(11.25, 3.2), xytext=(8.5, 4.0),
               arrowprops=dict(arrowstyle='->', lw=1.8, color='#E64A19'))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Figure_2_Risk_Assessment_Framework.png'), dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 2 saved successfully.")


# =============================================================================
# FIGURE 3: AI-driven closed-loop workflow for bio-nanomaterial design
# =============================================================================
def create_figure3():
    fig, ax = plt.subplots(1, 1, figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Figure 3: AI-Driven Closed-Loop Workflow for Design and Optimization\nof Microbial-Derived Bio-Nanomaterials',
            ha='center', va='center', fontsize=13, fontweight='bold')
    
    # Central cycle - 6 components arranged in a circle
    center_x, center_y = 7, 5
    radius = 3.2
    angles = [90, 30, -30, -90, -150, 150]  # positions around circle
    
    components = [
        {'title': 'DATA\nCOLLECTION', 'color': '#E8F5E9', 'edge': '#4CAF50',
         'details': 'Experimental data,\nliterature mining,\ndatabases'},
        {'title': 'ML MODEL\nTRAINING', 'color': '#E3F2FD', 'edge': '#2196F3',
         'details': 'Random forests, DNNs,\nGaussian processes,\nensemble methods'},
        {'title': 'PREDICTIVE\nDESIGN', 'color': '#F3E5F5', 'edge': '#9C27B0',
         'details': 'Property prediction,\noptimal conditions,\ninverse design'},
        {'title': 'AUTOMATED\nSYNTHESIS', 'color': '#FFF3E0', 'edge': '#FF9800',
         'details': 'Robotic platforms,\nhigh-throughput,\nmicrobioreactors'},
        {'title': 'CHARACTERIZATION\n& ANALYSIS', 'color': '#FCE4EC', 'edge': '#E91E63',
         'details': 'Computer vision,\nautomated TEM/SEM,\nspectroscopy'},
        {'title': 'BAYESIAN\nOPTIMIZATION', 'color': '#E0F7FA', 'edge': '#00BCD4',
         'details': 'Active learning,\nacquisition functions,\nuncertainty sampling'},
    ]
    
    box_w, box_h = 2.4, 1.8
    positions = []
    
    for i, (angle, comp) in enumerate(zip(angles, components)):
        rad = np.radians(angle)
        x = center_x + radius * np.cos(rad) - box_w/2
        y = center_y + radius * np.sin(rad) - box_h/2
        positions.append((x + box_w/2, y + box_h/2))
        
        rect = FancyBboxPatch((x, y), box_w, box_h, boxstyle="round,pad=0.1",
                              facecolor=comp['color'], edgecolor=comp['edge'], linewidth=2)
        ax.add_patch(rect)
        ax.text(x + box_w/2, y + box_h - 0.3, comp['title'],
                ha='center', va='top', fontsize=8.5, fontweight='bold')
        ax.text(x + box_w/2, y + box_h - 1.0, comp['details'],
                ha='center', va='top', fontsize=7)
    
    # Draw circular arrows connecting components
    for i in range(6):
        start = positions[i]
        end = positions[(i+1) % 6]
        # Calculate midpoint and offset for curved arrow
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        # Offset toward center
        offset_x = (center_x - mid_x) * 0.3
        offset_y = (center_y - mid_y) * 0.3
        
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=2, color='#424242',
                                  connectionstyle=f'arc3,rad=0.3'))
    
    # Central hub
    circle = plt.Circle((center_x, center_y), 1.0, facecolor='#FFFDE7', 
                        edgecolor='#F9A825', linewidth=2.5)
    ax.add_patch(circle)
    ax.text(center_x, center_y + 0.2, 'AI-DRIVEN', ha='center', va='center',
            fontsize=10, fontweight='bold', color='#F57F17')
    ax.text(center_x, center_y - 0.3, 'CLOSED LOOP', ha='center', va='center',
            fontsize=9, fontweight='bold', color='#F57F17')
    
    # Side annotations
    # Digital Twin box
    dt_box = FancyBboxPatch((0.3, 0.3), 3.5, 1.5, boxstyle="round,pad=0.1",
                            facecolor='#ECEFF1', edgecolor='#546E7A', linewidth=1.5)
    ax.add_patch(dt_box)
    ax.text(2.05, 1.5, 'DIGITAL TWIN', ha='center', va='top', fontsize=8.5, fontweight='bold')
    ax.text(2.05, 1.0, '• Process simulation\n• Virtual experiments\n• Scenario analysis',
            ha='center', va='top', fontsize=7.5)
    
    # Outcomes box
    out_box = FancyBboxPatch((10.2, 0.3), 3.5, 1.5, boxstyle="round,pad=0.1",
                             facecolor='#ECEFF1', edgecolor='#546E7A', linewidth=1.5)
    ax.add_patch(out_box)
    ax.text(11.95, 1.5, 'OUTCOMES', ha='center', va='top', fontsize=8.5, fontweight='bold')
    ax.text(11.95, 1.0, '• Optimized nanoparticles\n• Reduced development time\n• Predictive quality control',
            ha='center', va='top', fontsize=7.5)
    
    # Dashed connections to side boxes
    ax.annotate('', xy=(2.05, 1.8), xytext=(4.5, 3.5),
               arrowprops=dict(arrowstyle='->', lw=1.5, color='#546E7A', linestyle='dashed'))
    ax.annotate('', xy=(11.95, 1.8), xytext=(9.5, 3.5),
               arrowprops=dict(arrowstyle='->', lw=1.5, color='#546E7A', linestyle='dashed'))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Figure_3_AI_Workflow.png'), dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 3 saved successfully.")


# =============================================================================
# FIGURE 4: Research roadmap and technology convergence framework
# =============================================================================
def create_figure4():
    fig, ax = plt.subplots(1, 1, figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Figure 4: Comprehensive Research Roadmap and Technology Convergence Framework\nfor Next-Generation Microbial Bio-Nanomaterials',
            ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Timeline arrow at top
    ax.annotate('', xy=(13, 8.5), xytext=(1, 8.5),
               arrowprops=dict(arrowstyle='->', lw=3, color='#1565C0'))
    
    # Time periods
    periods = [
        {'x': 2.5, 'label': 'Near-term\n(1-3 years)', 'color': '#4CAF50'},
        {'x': 6.0, 'label': 'Mid-term\n(3-7 years)', 'color': '#FF9800'},
        {'x': 9.5, 'label': 'Long-term\n(7-15 years)', 'color': '#E91E63'},
        {'x': 12.5, 'label': 'Visionary\n(>15 years)', 'color': '#9C27B0'},
    ]
    
    for p in periods:
        ax.plot(p['x'], 8.5, 'o', markersize=12, color=p['color'], zorder=5)
        ax.text(p['x'], 8.9, p['label'], ha='center', va='bottom', fontsize=8, 
                fontweight='bold', color=p['color'])
    
    # Research areas - stacked rows
    # Row 1: Biotechnology advances
    row1_y = 6.8
    ax.text(0.5, row1_y, 'BIOTECHNOLOGY', ha='left', va='center', fontsize=9, 
            fontweight='bold', color='#2E7D32', rotation=0)
    
    biotech_items = [
        {'x': 2.0, 'w': 2.5, 'text': 'Optimized wild-type\nstrain libraries'},
        {'x': 4.8, 'w': 3.0, 'text': 'CRISPR-engineered\nproduction strains'},
        {'x': 8.1, 'w': 2.8, 'text': 'Synthetic microbial\nconsortia'},
        {'x': 11.2, 'w': 2.3, 'text': 'Autonomous\nbiosystems'},
    ]
    
    for item in biotech_items:
        rect = FancyBboxPatch((item['x'], row1_y - 0.5), item['w'], 0.9,
                              boxstyle="round,pad=0.05", facecolor='#E8F5E9', 
                              edgecolor='#4CAF50', linewidth=1.2)
        ax.add_patch(rect)
        ax.text(item['x'] + item['w']/2, row1_y, item['text'],
                ha='center', va='center', fontsize=7)
    
    # Row 2: AI/Computing
    row2_y = 5.6
    ax.text(0.5, row2_y, 'AI & COMPUTING', ha='left', va='center', fontsize=9,
            fontweight='bold', color='#1565C0')
    
    ai_items = [
        {'x': 2.0, 'w': 2.5, 'text': 'ML prediction\nmodels'},
        {'x': 4.8, 'w': 3.0, 'text': 'Self-driving\nlaboratories'},
        {'x': 8.1, 'w': 2.8, 'text': 'Autonomous material\ndiscovery platforms'},
        {'x': 11.2, 'w': 2.3, 'text': 'AGI-guided\nresearch'},
    ]
    
    for item in ai_items:
        rect = FancyBboxPatch((item['x'], row2_y - 0.5), item['w'], 0.9,
                              boxstyle="round,pad=0.05", facecolor='#E3F2FD',
                              edgecolor='#2196F3', linewidth=1.2)
        ax.add_patch(rect)
        ax.text(item['x'] + item['w']/2, row2_y, item['text'],
                ha='center', va='center', fontsize=7)
    
    # Row 3: Manufacturing
    row3_y = 4.4
    ax.text(0.5, row3_y, 'MANUFACTURING', ha='left', va='center', fontsize=9,
            fontweight='bold', color='#E65100')
    
    mfg_items = [
        {'x': 2.0, 'w': 2.5, 'text': 'Pilot-scale\nvalidation'},
        {'x': 4.8, 'w': 3.0, 'text': 'Continuous\nbiomanufacturing'},
        {'x': 8.1, 'w': 2.8, 'text': 'Smart factory\nintegration'},
        {'x': 11.2, 'w': 2.3, 'text': 'Distributed\nbioproduction'},
    ]
    
    for item in mfg_items:
        rect = FancyBboxPatch((item['x'], row3_y - 0.5), item['w'], 0.9,
                              boxstyle="round,pad=0.05", facecolor='#FFF3E0',
                              edgecolor='#FF9800', linewidth=1.2)
        ax.add_patch(rect)
        ax.text(item['x'] + item['w']/2, row3_y, item['text'],
                ha='center', va='center', fontsize=7)
    
    # Row 4: Applications
    row4_y = 3.2
    ax.text(0.5, row4_y, 'APPLICATIONS', ha='left', va='center', fontsize=9,
            fontweight='bold', color='#AD1457')
    
    app_items = [
        {'x': 2.0, 'w': 2.5, 'text': 'Antimicrobials &\nbiosensors'},
        {'x': 4.8, 'w': 3.0, 'text': 'Targeted drug delivery\n& remediation'},
        {'x': 8.1, 'w': 2.8, 'text': 'Personalized medicine\n& smart systems'},
        {'x': 11.2, 'w': 2.3, 'text': 'Autonomous\ntheranostics'},
    ]
    
    for item in app_items:
        rect = FancyBboxPatch((item['x'], row4_y - 0.5), item['w'], 0.9,
                              boxstyle="round,pad=0.05", facecolor='#FCE4EC',
                              edgecolor='#E91E63', linewidth=1.2)
        ax.add_patch(rect)
        ax.text(item['x'] + item['w']/2, row4_y, item['text'],
                ha='center', va='center', fontsize=7)
    
    # Convergence zone at bottom
    conv_box = FancyBboxPatch((1.5, 0.5), 11, 1.8, boxstyle="round,pad=0.15",
                              facecolor='#FFFDE7', edgecolor='#F9A825', linewidth=2.5)
    ax.add_patch(conv_box)
    ax.text(7, 1.9, 'TECHNOLOGY CONVERGENCE: Bio-Nano-AI-Digital Integration',
            ha='center', va='center', fontsize=10, fontweight='bold', color='#F57F17')
    ax.text(7, 1.15, 'Circular Bioeconomy  •  Sustainable Manufacturing  •  Personalized Solutions  •  Autonomous Systems  •  Global Impact',
            ha='center', va='center', fontsize=8.5, color='#5D4037')
    
    # Vertical arrows from rows to convergence
    for x_pos in [3.25, 6.3, 9.5, 12.35]:
        ax.annotate('', xy=(x_pos, 2.3), xytext=(x_pos, 2.7),
                   arrowprops=dict(arrowstyle='->', lw=1.2, color='#F9A825'))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Figure_4_Research_Roadmap.png'), dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 4 saved successfully.")


# Generate all figures
if __name__ == '__main__':
    create_figure1()
    create_figure2()
    create_figure3()
    create_figure4()
    print("\nAll 4 figures generated successfully in:", output_dir)
