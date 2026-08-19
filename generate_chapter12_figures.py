"""
Generate all 4 figures for Chapter 12: Industrial Translation, Scale-Up, 
Regulatory Aspects, AI Integration, Market Potential, and Future Perspectives
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np
import os

# Create output directory
output_dir = "chapter12_figures"
os.makedirs(output_dir, exist_ok=True)

# Set global style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.2


def figure1_scaleup_pathway():
    """
    Figure 1: Schematic of scale-up pathway from lab to industrial production
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    # Title
    ax.text(7, 8.6, 'Scale-Up Pathway for Microbial-Derived Bio-Nanomaterial Production',
            fontsize=14, fontweight='bold', ha='center', va='center')
    
    # Three main stages - boxes
    stages = [
        (2.2, 5.5, 'Laboratory Scale\n(0.1–5 L)', '#E3F2FD'),
        (7, 5.5, 'Pilot Scale\n(50–500 L)', '#FFF3E0'),
        (11.8, 5.5, 'Industrial Scale\n(500–50,000 L)', '#E8F5E9')
    ]
    
    for x, y, text, color in stages:
        box = FancyBboxPatch((x-1.6, y-0.8), 3.2, 1.6, 
                            boxstyle="round,pad=0.1", 
                            facecolor=color, edgecolor='#333333', linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=11, fontweight='bold', ha='center', va='center')
    
    # Arrows between stages
    arrow_style = "Simple,tail_width=1.5,head_width=10,head_length=8"
    ax.annotate('', xy=(5.1, 5.5), xytext=(3.9, 5.5),
                arrowprops=dict(arrowstyle='->', lw=2.5, color='#1565C0'))
    ax.annotate('', xy=(9.9, 5.5), xytext=(8.7, 5.5),
                arrowprops=dict(arrowstyle='->', lw=2.5, color='#E65100'))
    
    # Lab scale details
    lab_items = [
        'Strain screening & selection',
        'Parameter optimization (DoE)',
        'Proof-of-concept synthesis',
        'Initial characterization'
    ]
    for i, item in enumerate(lab_items):
        ax.text(2.2, 4.2 - i*0.45, f'• {item}', fontsize=8.5, ha='center', va='center')
    
    # Pilot scale details
    pilot_items = [
        'Bioreactor adaptation',
        'Process validation & PAT',
        'Downstream optimization',
        'Batch consistency testing'
    ]
    for i, item in enumerate(pilot_items):
        ax.text(7, 4.2 - i*0.45, f'• {item}', fontsize=8.5, ha='center', va='center')
    
    # Industrial scale details
    industrial_items = [
        'Full-scale manufacturing',
        'Automated process control',
        'GMP compliance & QC',
        'Continuous production'
    ]
    for i, item in enumerate(industrial_items):
        ax.text(11.8, 4.2 - i*0.45, f'• {item}', fontsize=8.5, ha='center', va='center')
    
    # Bottom section - Key parameters
    ax.plot([0.5, 13.5], [2.2, 2.2], 'k-', lw=1)
    ax.text(7, 1.9, 'Critical Scale-Up Parameters', fontsize=11, fontweight='bold', ha='center')
    
    params = [
        (2.2, 1.3, 'Mixing &\nMass Transfer', '#BBDEFB'),
        (5.1, 1.3, 'Heat Transfer\n& Temperature', '#FFCCBC'),
        (8, 1.3, 'Sterility &\nContamination', '#C8E6C9'),
        (10.9, 1.3, 'Yield &\nReproducibility', '#E1BEE7')
    ]
    
    for x, y, text, color in params:
        box = FancyBboxPatch((x-1.2, y-0.6), 2.4, 1.2, 
                            boxstyle="round,pad=0.05", 
                            facecolor=color, edgecolor='#555555', linewidth=1.2)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=9, ha='center', va='center', fontweight='bold')
    
    # Top section - Process flow indicators
    ax.text(3.5, 7.5, 'Process\nOptimization', fontsize=9, ha='center', 
            style='italic', color='#1565C0')
    ax.text(8.3, 7.5, 'Validation &\nScaling Rules', fontsize=9, ha='center', 
            style='italic', color='#E65100')
    ax.text(11.8, 7.5, 'Commercial\nManufacturing', fontsize=9, ha='center', 
            style='italic', color='#2E7D32')
    
    # Volume indicators
    ax.annotate('', xy=(12.5, 7.0), xytext=(1.5, 7.0),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='gray', linestyle='--'))
    ax.text(7, 7.2, 'Increasing Volume, Complexity, and Regulatory Requirements →',
            fontsize=9, ha='center', color='gray', style='italic')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_1_ScaleUp_Pathway.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 1 saved successfully.")


def figure2_regulatory_framework():
    """
    Figure 2: Regulatory pathway and safety assessment framework
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.6, 'Regulatory Pathway and Safety Assessment Framework\nfor Microbial-Derived Bio-Nanomaterials',
            fontsize=13, fontweight='bold', ha='center', va='center')
    
    # Main flow - top to bottom
    # Stage 1: Preclinical Assessment
    box1 = FancyBboxPatch((4.5, 8.0), 5, 1.0, boxstyle="round,pad=0.1",
                          facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=2)
    ax.add_patch(box1)
    ax.text(7, 8.5, 'PRECLINICAL ASSESSMENT', fontsize=11, fontweight='bold', 
            ha='center', va='center', color='#1565C0')
    
    # Arrow down
    ax.annotate('', xy=(7, 7.0), xytext=(7, 7.9),
                arrowprops=dict(arrowstyle='->', lw=2, color='#333'))
    
    # Stage 2: Safety Testing (with sub-boxes)
    box2 = FancyBboxPatch((1.0, 5.2), 12, 1.8, boxstyle="round,pad=0.1",
                          facecolor='#FFF8E1', edgecolor='#F57F17', linewidth=2)
    ax.add_patch(box2)
    ax.text(7, 6.8, 'COMPREHENSIVE SAFETY TESTING', fontsize=11, fontweight='bold',
            ha='center', va='center', color='#E65100')
    
    safety_tests = [
        (2.5, 5.8, 'Cytotoxicity\nAssessment'),
        (5.0, 5.8, 'Genotoxicity\nTesting'),
        (7.5, 5.8, 'Immunological\nEvaluation'),
        (10.0, 5.8, 'Ecotoxicity\nAssessment'),
        (12.0, 5.8, 'LCA')
    ]
    
    for x, y, text in safety_tests:
        box = FancyBboxPatch((x-0.9, y-0.4), 1.8, 0.8, boxstyle="round,pad=0.05",
                            facecolor='white', edgecolor='#F57F17', linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=8, ha='center', va='center')
    
    # Arrow down
    ax.annotate('', xy=(7, 4.2), xytext=(7, 5.1),
                arrowprops=dict(arrowstyle='->', lw=2, color='#333'))
    
    # Stage 3: Regulatory Submission
    box3 = FancyBboxPatch((4.0, 3.2), 6, 1.0, boxstyle="round,pad=0.1",
                          facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=2)
    ax.add_patch(box3)
    ax.text(7, 3.7, 'REGULATORY SUBMISSION & REVIEW', fontsize=11, fontweight='bold',
            ha='center', va='center', color='#2E7D32')
    
    # Arrow down
    ax.annotate('', xy=(7, 2.2), xytext=(7, 3.1),
                arrowprops=dict(arrowstyle='->', lw=2, color='#333'))
    
    # Stage 4: Post-market
    box4 = FancyBboxPatch((4.0, 1.2), 6, 1.0, boxstyle="round,pad=0.1",
                          facecolor='#F3E5F5', edgecolor='#6A1B9A', linewidth=2)
    ax.add_patch(box4)
    ax.text(7, 1.7, 'POST-MARKET SURVEILLANCE & MONITORING', fontsize=10, fontweight='bold',
            ha='center', va='center', color='#6A1B9A')
    
    # Side panels - Regulatory Bodies
    # Left side
    left_bodies = ['FDA (USA)', 'EMA (EU)', 'PMDA (Japan)', 'TGA (Australia)']
    ax.text(1.5, 3.7, 'Regulatory\nBodies', fontsize=9, fontweight='bold', 
            ha='center', va='center', color='#2E7D32')
    for i, body in enumerate(left_bodies):
        ax.text(1.5, 3.0 - i*0.4, body, fontsize=8, ha='center', va='center')
    
    # Right side - Standards
    right_std = ['ISO 10993', 'OECD TG', 'ICH Guidelines', 'REACH/CLP']
    ax.text(12.5, 3.7, 'Standards &\nGuidelines', fontsize=9, fontweight='bold',
            ha='center', va='center', color='#2E7D32')
    for i, std in enumerate(right_std):
        ax.text(12.5, 3.0 - i*0.4, std, fontsize=8, ha='center', va='center')
    
    # Connecting lines
    ax.plot([3.9, 3.5], [3.7, 3.7], 'k-', lw=1)
    ax.plot([10.1, 11.0], [3.7, 3.7], 'k-', lw=1)
    
    # Physicochemical characterization box (top left)
    char_box = FancyBboxPatch((0.3, 8.0), 3.5, 1.0, boxstyle="round,pad=0.05",
                              facecolor='#ECEFF1', edgecolor='#455A64', linewidth=1.2)
    ax.add_patch(char_box)
    ax.text(2.05, 8.5, 'Physicochemical\nCharacterization', fontsize=9, 
            fontweight='bold', ha='center', va='center')
    ax.plot([3.8, 4.5], [8.5, 8.5], 'k--', lw=1)
    
    # Risk assessment box (top right)
    risk_box = FancyBboxPatch((10.2, 8.0), 3.5, 1.0, boxstyle="round,pad=0.05",
                              facecolor='#ECEFF1', edgecolor='#455A64', linewidth=1.2)
    ax.add_patch(risk_box)
    ax.text(11.95, 8.5, 'Environmental\nRisk Assessment', fontsize=9,
            fontweight='bold', ha='center', va='center')
    ax.plot([10.2, 9.5], [8.5, 8.5], 'k--', lw=1)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_2_Regulatory_Framework.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 2 saved successfully.")


def figure3_ai_integration():
    """
    Figure 3: AI/ML integration in bio-nanomaterial development
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Integrated AI/ML Framework for Bio-Nanomaterial Development',
            fontsize=13, fontweight='bold', ha='center', va='center')
    
    # Central AI/ML Hub
    circle = plt.Circle((7, 5.2), 1.3, facecolor='#E8EAF6', edgecolor='#283593', linewidth=2.5)
    ax.add_patch(circle)
    ax.text(7, 5.4, 'AI/ML\nEngine', fontsize=12, fontweight='bold', 
            ha='center', va='center', color='#283593')
    ax.text(7, 4.8, '(Deep Learning,\nOptimization)', fontsize=8, ha='center', va='center', color='#3949AB')
    
    # Surrounding components
    components = [
        (2.5, 8.0, 'Data Acquisition\n& Sensors', '#E3F2FD', '#1565C0'),
        (11.5, 8.0, 'Process\nOptimization', '#E8F5E9', '#2E7D32'),
        (2.5, 2.5, 'Characterization\n& Analysis', '#FFF3E0', '#E65100'),
        (11.5, 2.5, 'Prediction &\nDecision Support', '#F3E5F5', '#6A1B9A'),
    ]
    
    for x, y, text, fcolor, ecolor in components:
        box = FancyBboxPatch((x-1.5, y-0.7), 3.0, 1.4, boxstyle="round,pad=0.1",
                            facecolor=fcolor, edgecolor=ecolor, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=10, fontweight='bold', ha='center', va='center', color=ecolor)
    
    # Connecting lines from components to center
    connections = [
        (2.5, 8.0, 7, 5.2),   # Data to center
        (11.5, 8.0, 7, 5.2),  # Process to center
        (2.5, 2.5, 7, 5.2),   # Characterization to center
        (11.5, 2.5, 7, 5.2),  # Prediction to center
    ]
    
    for x1, y1, x2, y2 in connections:
        # Calculate direction
        dx = x2 - x1
        dy = y2 - y1
        dist = np.sqrt(dx**2 + dy**2)
        # Shorten arrows to not overlap with shapes
        start_offset = 1.6
        end_offset = 1.4
        sx = x1 + dx/dist * start_offset
        sy = y1 + dy/dist * start_offset
        ex = x2 - dx/dist * end_offset
        ey = y2 - dy/dist * end_offset
        ax.annotate('', xy=(ex, ey), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle='<->', lw=1.5, color='#555'))
    
    # Sub-items for each component
    # Data Acquisition
    data_items = ['Bioreactor sensors', 'PAT instruments', 'Real-time monitoring']
    for i, item in enumerate(data_items):
        ax.text(2.5, 7.0 - i*0.35, f'• {item}', fontsize=8, ha='center')
    
    # Process Optimization
    proc_items = ['Parameter tuning', 'Yield maximization', 'Quality control']
    for i, item in enumerate(proc_items):
        ax.text(11.5, 7.0 - i*0.35, f'• {item}', fontsize=8, ha='center')
    
    # Characterization
    char_items = ['TEM/SEM image analysis', 'Spectral interpretation', 'Size distribution']
    for i, item in enumerate(char_items):
        ax.text(2.5, 1.5 - i*0.35, f'• {item}', fontsize=8, ha='center')
    
    # Prediction
    pred_items = ['Toxicity prediction', 'Stability forecasting', 'Performance modeling']
    for i, item in enumerate(pred_items):
        ax.text(11.5, 1.5 - i*0.35, f'• {item}', fontsize=8, ha='center')
    
    # ML Methods listed around center
    ml_methods = [
        (4.5, 7.2, 'Neural\nNetworks', '#C5CAE9'),
        (9.5, 7.2, 'Random\nForest', '#C8E6C9'),
        (4.5, 3.3, 'Bayesian\nOptimization', '#FFE0B2'),
        (9.5, 3.3, 'Reinforcement\nLearning', '#E1BEE7'),
    ]
    
    for x, y, text, color in ml_methods:
        box = FancyBboxPatch((x-0.8, y-0.4), 1.6, 0.8, boxstyle="round,pad=0.05",
                            facecolor=color, edgecolor='#666', linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=8, ha='center', va='center', fontweight='bold')
    
    # Digital Twin box at bottom center
    dt_box = FancyBboxPatch((5.0, 0.3), 4.0, 0.9, boxstyle="round,pad=0.1",
                           facecolor='#FFEBEE', edgecolor='#C62828', linewidth=1.5)
    ax.add_patch(dt_box)
    ax.text(7, 0.75, 'Digital Twin & Predictive Maintenance', fontsize=9, 
            fontweight='bold', ha='center', va='center', color='#C62828')
    ax.annotate('', xy=(7, 1.2), xytext=(7, 3.9),
                arrowprops=dict(arrowstyle='<->', lw=1.2, color='#C62828', linestyle='--'))
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_3_AI_ML_Integration.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 3 saved successfully.")


def figure4_market_potential():
    """
    Figure 4: Market potential and future perspectives overview
    """
    fig = plt.figure(figsize=(14, 10))
    
    # Create a grid layout
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.3)
    
    # Panel A: Market size by sector (bar chart)
    ax1 = fig.add_subplot(gs[0, 0])
    sectors = ['Antimicrobial', 'Drug\nDelivery', 'Diagnostics', 'Agriculture', 'Environment', 'Food\nPackaging']
    market_sizes = [2.1, 3.8, 2.6, 1.9, 1.4, 0.8]
    colors = ['#1565C0', '#2E7D32', '#E65100', '#6A1B9A', '#00838F', '#AD1457']
    
    bars = ax1.bar(sectors, market_sizes, color=colors, edgecolor='white', linewidth=0.5)
    ax1.set_ylabel('Market Size ($ Billion)', fontsize=10)
    ax1.set_title('(A) Market Size by Application Sector (2025)', fontsize=11, fontweight='bold')
    ax1.set_ylim(0, 4.5)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # Add value labels on bars
    for bar, val in zip(bars, market_sizes):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'${val}B', ha='center', fontsize=8, fontweight='bold')
    
    # Panel B: Growth projections (CAGR)
    ax2 = fig.add_subplot(gs[0, 1])
    categories = ['Agriculture', 'Antimicrobial', 'Diagnostics', 'Drug Delivery',
                  'Food Packaging', 'Environment']
    cagr_values = [19.3, 18.2, 17.1, 16.5, 15.4, 14.8]
    colors2 = ['#6A1B9A', '#1565C0', '#E65100', '#2E7D32', '#AD1457', '#00838F']
    
    bars2 = ax2.barh(categories, cagr_values, color=colors2, edgecolor='white', linewidth=0.5)
    ax2.set_xlabel('CAGR (%)', fontsize=10)
    ax2.set_title('(B) Projected Growth Rate (CAGR %)', fontsize=11, fontweight='bold')
    ax2.set_xlim(0, 22)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    for bar, val in zip(bars2, cagr_values):
        ax2.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f'{val}%', va='center', fontsize=8, fontweight='bold')
    
    # Panel C: Technology Readiness vs Market Maturity
    ax3 = fig.add_subplot(gs[1, 0])
    trl_values = [6.5, 5.0, 6.0, 5.0, 7.0, 4.5, 5.0]
    market_maturity = [3.5, 2.5, 3.0, 2.0, 4.0, 2.0, 2.5]
    bubble_sizes = [210, 380, 260, 190, 140, 80, 90]
    labels = ['Antimicrobial', 'Drug Delivery', 'Diagnostics', 'Agriculture', 
              'Cosmetics', 'Food Pkg', 'Catalysis']
    colors3 = ['#1565C0', '#2E7D32', '#E65100', '#6A1B9A', '#AD1457', '#00838F', '#FF6F00']
    
    scatter = ax3.scatter(trl_values, market_maturity, s=bubble_sizes, c=colors3, 
                         alpha=0.7, edgecolors='white', linewidth=1.5)
    
    for i, label in enumerate(labels):
        ax3.annotate(label, (trl_values[i], market_maturity[i]), fontsize=7.5,
                    ha='center', va='bottom', xytext=(0, 8), textcoords='offset points')
    
    ax3.set_xlabel('Technology Readiness Level (TRL)', fontsize=10)
    ax3.set_ylabel('Market Maturity', fontsize=10)
    ax3.set_title('(C) TRL vs. Market Maturity (bubble = market size)', fontsize=11, fontweight='bold')
    ax3.set_xlim(3.5, 8)
    ax3.set_ylim(1, 5)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    
    # Panel D: Future roadmap timeline
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_xlim(0, 10)
    ax4.set_ylim(0, 6)
    ax4.axis('off')
    ax4.set_title('(D) Commercialization Roadmap', fontsize=11, fontweight='bold')
    
    # Timeline
    timeline_y = 3.0
    ax4.plot([0.5, 9.5], [timeline_y, timeline_y], 'k-', lw=2)
    
    milestones = [
        (1.5, 'Near-term\n(1-3 yrs)', 'Antimicrobials\nCosmetics', '#2E7D32'),
        (4.0, 'Mid-term\n(3-5 yrs)', 'Diagnostics\nEnvironment', '#E65100'),
        (6.5, 'Long-term\n(5-10 yrs)', 'Drug Delivery\nAgriculture', '#1565C0'),
        (9.0, 'Frontier\n(>10 yrs)', 'Personalized\nMedicine', '#6A1B9A'),
    ]
    
    for x, period, apps, color in milestones:
        ax4.plot(x, timeline_y, 'o', markersize=12, color=color, zorder=5)
        ax4.text(x, timeline_y + 0.8, period, fontsize=8.5, fontweight='bold',
                ha='center', va='center', color=color)
        ax4.text(x, timeline_y - 0.8, apps, fontsize=8, ha='center', va='center')
    
    # Arrow at end
    ax4.annotate('', xy=(9.8, timeline_y), xytext=(9.3, timeline_y),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    # Key drivers text
    ax4.text(5, 0.8, 'Key Drivers: Sustainability demand | AI-driven optimization | Regulatory clarity',
            fontsize=8.5, ha='center', va='center', style='italic', color='#555')
    ax4.text(5, 5.3, 'Investment Requirements: Low → Medium → High → Very High',
            fontsize=8.5, ha='center', va='center', style='italic', color='#555')
    
    plt.savefig(f'{output_dir}/Figure_4_Market_Potential.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 4 saved successfully.")


# Generate all figures
if __name__ == '__main__':
    print("Generating Chapter 12 figures...")
    figure1_scaleup_pathway()
    figure2_regulatory_framework()
    figure3_ai_integration()
    figure4_market_potential()
    print(f"\nAll figures saved to '{output_dir}/' directory.")
    print("Files generated:")
    for f in os.listdir(output_dir):
        filepath = os.path.join(output_dir, f)
        size_kb = os.path.getsize(filepath) / 1024
        print(f"  - {f} ({size_kb:.1f} KB)")
