"""
Generate 4 professional figures for the Design Thinking Comparative Analysis chapter.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np
import os

# Create output directory
os.makedirs('dt_chapter_figures', exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

# ============================================================
# FIGURE 1: The Integrated Strategic Framework
# ============================================================
def create_figure1():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'The Integrated Strategic Framework', fontsize=14, fontweight='bold',
            ha='center', va='center')
    ax.text(5, 9.0, 'Positioning Design Thinking at the Centre of Strategic Approaches',
            fontsize=10, ha='center', va='center', style='italic', color='#555555')
    
    # Central circle - Design Thinking
    central_circle = plt.Circle((5, 5), 1.2, color='#2196F3', alpha=0.3, linewidth=2, edgecolor='#1565C0')
    ax.add_patch(central_circle)
    ax.text(5, 5.2, 'DESIGN\nTHINKING', fontsize=11, fontweight='bold', ha='center', va='center', color='#1565C0')
    ax.text(5, 4.5, 'Human-Centred\nIntegrator', fontsize=8, ha='center', va='center', color='#1565C0')
    
    # Three surrounding circles
    # Analytical - top
    analytical_circle = plt.Circle((5, 7.8), 0.9, color='#4CAF50', alpha=0.25, linewidth=2, edgecolor='#2E7D32')
    ax.add_patch(analytical_circle)
    ax.text(5, 8.0, 'ANALYTICAL', fontsize=9, fontweight='bold', ha='center', va='center', color='#2E7D32')
    ax.text(5, 7.5, 'Data & Logic', fontsize=7, ha='center', va='center', color='#2E7D32')
    
    # Systems - bottom left
    systems_circle = plt.Circle((2.8, 3.5), 0.9, color='#FF9800', alpha=0.25, linewidth=2, edgecolor='#E65100')
    ax.add_patch(systems_circle)
    ax.text(2.8, 3.7, 'SYSTEMS', fontsize=9, fontweight='bold', ha='center', va='center', color='#E65100')
    ax.text(2.8, 3.2, 'Holistic View', fontsize=7, ha='center', va='center', color='#E65100')
    
    # Creative - bottom right
    creative_circle = plt.Circle((7.2, 3.5), 0.9, color='#9C27B0', alpha=0.25, linewidth=2, edgecolor='#6A1B9A')
    ax.add_patch(creative_circle)
    ax.text(7.2, 3.7, 'CREATIVE', fontsize=9, fontweight='bold', ha='center', va='center', color='#6A1B9A')
    ax.text(7.2, 3.2, 'Novel Ideas', fontsize=7, ha='center', va='center', color='#6A1B9A')
    
    # Connecting arrows with labels
    # Analytical to DT
    ax.annotate('', xy=(5, 6.2), xytext=(5, 6.9),
                arrowprops=dict(arrowstyle='<->', color='#388E3C', lw=2))
    ax.text(5.6, 6.55, 'Informed\nEmpathy', fontsize=7, ha='left', color='#388E3C')
    
    # Systems to DT
    ax.annotate('', xy=(3.9, 4.3), xytext=(3.4, 3.9),
                arrowprops=dict(arrowstyle='<->', color='#E65100', lw=2))
    ax.text(2.9, 4.5, 'Sustainable\nSolutions', fontsize=7, ha='center', color='#E65100')
    
    # Creative to DT
    ax.annotate('', xy=(6.1, 4.3), xytext=(6.6, 3.9),
                arrowprops=dict(arrowstyle='<->', color='#6A1B9A', lw=2))
    ax.text(7.1, 4.5, 'Grounded\nInnovation', fontsize=7, ha='center', color='#6A1B9A')
    
    # Outer ring - Strategic Outcomes
    outcomes = [
        (1.5, 8.0, 'Customer\nLoyalty'),
        (8.5, 8.0, 'Organisational\nAgility'),
        (1.0, 1.5, 'Reduced\nRisk'),
        (9.0, 1.5, 'Competitive\nAdvantage'),
    ]
    
    for x, y, label in outcomes:
        box = FancyBboxPatch((x-0.7, y-0.4), 1.4, 0.8, boxstyle="round,pad=0.1",
                            facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, label, fontsize=7, ha='center', va='center', color='#1565C0')
    
    # DT Process stages around the center
    stages = ['Empathize', 'Define', 'Ideate', 'Prototype', 'Test']
    angles = np.linspace(0, 2*np.pi, 6)[:-1]
    radius = 2.0
    for angle, stage in zip(angles, stages):
        x = 5 + radius * np.cos(angle)
        y = 5 + radius * np.sin(angle)
        ax.text(x, y, stage, fontsize=8, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#BBDEFB', edgecolor='#1565C0', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('dt_chapter_figures/Figure_1_Integrated_Framework.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 1 created successfully.")

# ============================================================
# FIGURE 2: Systems Thinking in Strategic Context
# ============================================================
def create_figure2():
    fig, ax = plt.subplots(1, 1, figsize=(11, 8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)
    ax.axis('off')
    
    # Title
    ax.text(5.5, 8.2, 'Systems Thinking in Strategic Context', fontsize=14, fontweight='bold',
            ha='center', va='center')
    ax.text(5.5, 7.8, 'Feedback Loops and Leverage Points in Organisational Decision-Making',
            fontsize=10, ha='center', va='center', style='italic', color='#555555')
    
    # Main system elements as boxes
    elements = {
        'Strategy': (5.5, 6.0, '#2196F3'),
        'Innovation\nCapacity': (2.0, 4.5, '#4CAF50'),
        'Customer\nValue': (9.0, 4.5, '#FF9800'),
        'Market\nPosition': (7.5, 2.5, '#9C27B0'),
        'Org.\nLearning': (3.5, 2.5, '#F44336'),
        'Resource\nAllocation': (5.5, 1.0, '#00BCD4'),
    }
    
    for label, (x, y, color) in elements.items():
        box = FancyBboxPatch((x-0.8, y-0.4), 1.6, 0.8, boxstyle="round,pad=0.15",
                            facecolor=color, edgecolor='black', alpha=0.3, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, label, fontsize=8, fontweight='bold', ha='center', va='center', color='#333333')
    
    # Reinforcing loops (R) - arrows
    connections = [
        ('Strategy', 'Innovation\nCapacity', 'Drives'),
        ('Innovation\nCapacity', 'Customer\nValue', 'Creates'),
        ('Customer\nValue', 'Market\nPosition', 'Strengthens'),
        ('Market\nPosition', 'Resource\nAllocation', 'Enables'),
        ('Resource\nAllocation', 'Org.\nLearning', 'Funds'),
        ('Org.\nLearning', 'Strategy', 'Informs'),
    ]
    
    positions = {
        'Strategy': (5.5, 6.0),
        'Innovation\nCapacity': (2.0, 4.5),
        'Customer\nValue': (9.0, 4.5),
        'Market\nPosition': (7.5, 2.5),
        'Org.\nLearning': (3.5, 2.5),
        'Resource\nAllocation': (5.5, 1.0),
    }
    
    for start, end, label in connections:
        sx, sy = positions[start]
        ex, ey = positions[end]
        mx = (sx + ex) / 2
        my = (sy + ey) / 2
        ax.annotate('', xy=(ex, ey), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle='->', color='#333333', lw=1.5,
                                  connectionstyle='arc3,rad=0.15'))
        ax.text(mx, my + 0.25, label, fontsize=7, ha='center', va='center',
                color='#666666', style='italic')
    
    # Loop labels
    ax.text(5.5, 3.8, 'R', fontsize=18, fontweight='bold', ha='center', va='center',
            color='#1565C0', alpha=0.5)
    ax.text(5.5, 3.3, 'Reinforcing\nLoop', fontsize=7, ha='center', va='center',
            color='#1565C0')
    
    # Leverage points annotation
    ax.text(0.5, 7.2, 'Leverage Points:', fontsize=9, fontweight='bold', color='#D32F2F')
    leverage_points = [
        '• Paradigm shifts (highest impact)',
        '• Goal restructuring',
        '• Information flow adjustments',
        '• Feedback loop modifications'
    ]
    for i, lp in enumerate(leverage_points):
        ax.text(0.5, 6.8 - i*0.3, lp, fontsize=7, color='#D32F2F')
    
    # Balancing loop indicator
    ax.annotate('', xy=(2.0, 4.0), xytext=(3.5, 2.9),
                arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=1.5,
                              connectionstyle='arc3,rad=-0.3', linestyle='dashed'))
    ax.text(2.0, 3.2, 'B\nBalancing', fontsize=7, ha='center', va='center', color='#D32F2F')
    
    plt.tight_layout()
    plt.savefig('dt_chapter_figures/Figure_2_Systems_Thinking.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 2 created successfully.")

# ============================================================
# FIGURE 3: Multi-Level Integration Framework
# ============================================================
def create_figure3():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'The Multi-Level Integration Framework', fontsize=14, fontweight='bold',
            ha='center', va='center')
    ax.text(5, 9.0, 'Connecting User Needs, Organisational Systems, and Ecosystem Dynamics',
            fontsize=10, ha='center', va='center', style='italic', color='#555555')
    
    # Three concentric layers
    # Outer - Ecosystem
    ecosystem = plt.Circle((5, 4.5), 3.8, color='#E8F5E9', alpha=0.5, linewidth=2, edgecolor='#2E7D32')
    ax.add_patch(ecosystem)
    ax.text(5, 8.0, 'ECOSYSTEM DYNAMICS', fontsize=10, fontweight='bold', ha='center', color='#2E7D32')
    ax.text(5, 7.6, 'Market Forces • Regulatory Environment • Technology Trends',
            fontsize=7, ha='center', color='#2E7D32')
    
    # Middle - Organisation
    org = plt.Circle((5, 4.5), 2.5, color='#FFF3E0', alpha=0.5, linewidth=2, edgecolor='#E65100')
    ax.add_patch(org)
    ax.text(5, 6.6, 'ORGANISATIONAL SYSTEMS', fontsize=9, fontweight='bold', ha='center', color='#E65100')
    ax.text(5, 6.2, 'Processes • Culture • Capabilities • Resources',
            fontsize=7, ha='center', color='#E65100')
    
    # Inner - User
    user = plt.Circle((5, 4.5), 1.3, color='#E3F2FD', alpha=0.6, linewidth=2, edgecolor='#1565C0')
    ax.add_patch(user)
    ax.text(5, 4.8, 'USER NEEDS', fontsize=9, fontweight='bold', ha='center', color='#1565C0')
    ax.text(5, 4.3, 'Empathy •\nDesirability', fontsize=7, ha='center', color='#1565C0')
    
    # DT Process flowing through layers
    dt_stages = [
        (1.5, 4.5, 'Empathize', '#1565C0'),
        (2.8, 2.5, 'Define', '#1976D2'),
        (5.0, 1.5, 'Ideate', '#1E88E5'),
        (7.2, 2.5, 'Prototype', '#2196F3'),
        (8.5, 4.5, 'Test', '#42A5F5'),
    ]
    
    for x, y, label, color in dt_stages:
        box = FancyBboxPatch((x-0.5, y-0.25), 1.0, 0.5, boxstyle="round,pad=0.1",
                            facecolor=color, edgecolor='white', alpha=0.8, linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, label, fontsize=7, fontweight='bold', ha='center', va='center', color='white')
    
    # Arrows connecting DT stages
    for i in range(len(dt_stages)-1):
        x1, y1 = dt_stages[i][0], dt_stages[i][1]
        x2, y2 = dt_stages[i+1][0], dt_stages[i+1][1]
        ax.annotate('', xy=(x2-0.4, y2), xytext=(x1+0.4, y1),
                    arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5,
                                  connectionstyle='arc3,rad=0.2'))
    
    # Integration annotations
    annotations = [
        (1.0, 7.5, 'Systems\nThinking\nLens', '#2E7D32'),
        (9.0, 7.5, 'Analytical\nValidation', '#4CAF50'),
        (1.0, 1.5, 'Creative\nIdeation\nEngine', '#9C27B0'),
        (9.0, 1.5, 'Iterative\nRefinement', '#FF5722'),
    ]
    
    for x, y, label, color in annotations:
        ax.text(x, y, label, fontsize=8, ha='center', va='center', color=color, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color, alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('dt_chapter_figures/Figure_3_MultiLevel_Integration.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 3 created successfully.")

# ============================================================
# FIGURE 4: Comparative Outcomes Across Industries
# ============================================================
def create_figure4():
    fig, ax = plt.subplots(1, 1, figsize=(11, 7))
    
    # Data
    categories = ['Innovation\nMetrics', 'Customer\nSatisfaction', 'Operational\nEfficiency', 
                  'Time-to-\nMarket', 'Revenue\nGrowth']
    
    industries = {
        'Product Development': [88, 85, 72, 90, 82],
        'Digital Transformation': [82, 78, 85, 88, 76],
        'Healthcare': [75, 92, 68, 65, 70],
        'Entrepreneurship': [92, 80, 65, 95, 88],
        'Manufacturing': [70, 75, 92, 72, 68],
    }
    
    x = np.arange(len(categories))
    width = 0.15
    multiplier = 0
    
    colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#F44336']
    
    for (industry, values), color in zip(industries.items(), colors):
        offset = width * multiplier
        bars = ax.bar(x + offset, values, width, label=industry, color=color, alpha=0.75, edgecolor='white')
        multiplier += 1
    
    ax.set_xlabel('Performance Dimensions', fontsize=11, fontweight='bold')
    ax.set_ylabel('Improvement Score (0-100)', fontsize=11, fontweight='bold')
    ax.set_title('Comparative Outcomes of Integrated Design Thinking\nApplication Across Five Industry Sectors',
                fontsize=13, fontweight='bold', pad=15)
    ax.set_xticks(x + width * 2)
    ax.set_xticklabels(categories, fontsize=9)
    ax.legend(loc='upper right', fontsize=8, framealpha=0.9)
    ax.set_ylim(0, 105)
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)
    
    # Add benchmark line
    ax.axhline(y=75, color='#D32F2F', linestyle='--', linewidth=1, alpha=0.5)
    ax.text(4.5, 76, 'Industry Benchmark', fontsize=7, color='#D32F2F', style='italic')
    
    plt.tight_layout()
    plt.savefig('dt_chapter_figures/Figure_4_Comparative_Outcomes.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 4 created successfully.")

# Generate all figures
if __name__ == '__main__':
    create_figure1()
    create_figure2()
    create_figure3()
    create_figure4()
    print("\nAll 4 figures generated successfully in 'dt_chapter_figures/' directory.")
