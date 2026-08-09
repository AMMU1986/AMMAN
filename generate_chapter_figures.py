"""
Generate 4 professional figures for the book chapter on
Generative AI for Sustainable Business Intelligence and Human Capital
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# Set style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11

output_dir = '/projects/sandbox/AMMAN/chapter_figures'
os.makedirs(output_dir, exist_ok=True)

# ============================================================
# FIGURE 1: Conceptual Framework - Generative AI Integration
# with Sustainable Business Intelligence
# ============================================================
def create_figure1():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Figure 1: Conceptual Framework for Generative AI Integration\nwith Sustainable Business Intelligence', 
                 fontsize=13, fontweight='bold', pad=20)

    # Central circle - Generative AI
    center_circle = plt.Circle((5, 5), 1.2, color='#2E86AB', alpha=0.85)
    ax.add_patch(center_circle)
    ax.text(5, 5, 'Generative\nAI', ha='center', va='center', fontsize=12, 
            fontweight='bold', color='white')

    # Three pillars of sustainability
    pillars = [
        (2, 8, '#27AE60', 'Economic\nSustainability'),
        (5, 8.5, '#E67E22', 'Environmental\nSustainability'),
        (8, 8, '#8E44AD', 'Social\nSustainability'),
    ]
    for x, y, color, label in pillars:
        box = FancyBboxPatch((x-0.9, y-0.5), 1.8, 1.0, 
                             boxstyle="round,pad=0.1", facecolor=color, alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, 
                fontweight='bold', color='white')
        ax.annotate('', xy=(5, 6.2), xytext=(x, y-0.5),
                   arrowprops=dict(arrowstyle='->', color=color, lw=2))

    # Business Intelligence components
    bi_components = [
        (1.5, 3.5, '#3498DB', 'Predictive\nAnalytics'),
        (3.5, 2, '#1ABC9C', 'Data-Driven\nDecision Making'),
        (6.5, 2, '#E74C3C', 'Real-Time\nInsights'),
        (8.5, 3.5, '#F39C12', 'Strategic\nForecasting'),
    ]
    for x, y, color, label in bi_components:
        box = FancyBboxPatch((x-0.85, y-0.45), 1.7, 0.9, 
                             boxstyle="round,pad=0.1", facecolor=color, alpha=0.75)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, 
                fontweight='bold', color='white')
        ax.annotate('', xy=(x, y+0.45), xytext=(5, 3.8),
                   arrowprops=dict(arrowstyle='<->', color='gray', lw=1.5, 
                                  connectionstyle='arc3,rad=0.1'))

    # Human Capital layer
    hc_box = FancyBboxPatch((2, 0.3), 6, 0.9, boxstyle="round,pad=0.15", 
                            facecolor='#34495E', alpha=0.85)
    ax.add_patch(hc_box)
    ax.text(5, 0.75, 'Human Capital Development & Future of Work', 
            ha='center', va='center', fontsize=11, fontweight='bold', color='white')

    # Connecting arrows from bottom
    ax.annotate('', xy=(5, 3.8), xytext=(5, 1.2),
               arrowprops=dict(arrowstyle='<->', color='#34495E', lw=2.5))

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_1_Conceptual_Framework.png', dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 1 created.")

# ============================================================
# FIGURE 2: AI-Driven Human Capital Management Ecosystem
# ============================================================
def create_figure2():
    fig, ax = plt.subplots(1, 1, figsize=(11, 7))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('Figure 2: AI-Driven Human Capital Management Ecosystem', 
                 fontsize=13, fontweight='bold', pad=15)

    # Left side - AI Technologies
    ai_techs = [
        (1.5, 5.5, 'NLP & Text\nGeneration'),
        (1.5, 4.2, 'Computer\nVision'),
        (1.5, 2.9, 'Reinforcement\nLearning'),
        (1.5, 1.6, 'Generative\nAdversarial\nNetworks'),
    ]
    
    # Header box
    header_box = FancyBboxPatch((0.3, 6.0), 2.4, 0.6, boxstyle="round,pad=0.1",
                                facecolor='#2C3E50', alpha=0.9)
    ax.add_patch(header_box)
    ax.text(1.5, 6.3, 'AI Technologies', ha='center', va='center', 
            fontsize=10, fontweight='bold', color='white')

    for x, y, label in ai_techs:
        box = FancyBboxPatch((x-0.9, y-0.4), 1.8, 0.8, boxstyle="round,pad=0.08",
                             facecolor='#3498DB', alpha=0.75)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, color='white', fontweight='bold')

    # Center - HCM Processes
    hcm_processes = [
        (5.5, 5.5, 'Talent\nAcquisition'),
        (5.5, 4.2, 'Performance\nManagement'),
        (5.5, 2.9, 'Learning &\nDevelopment'),
        (5.5, 1.6, 'Workforce\nPlanning'),
    ]

    header_box2 = FancyBboxPatch((4.3, 6.0), 2.4, 0.6, boxstyle="round,pad=0.1",
                                 facecolor='#2C3E50', alpha=0.9)
    ax.add_patch(header_box2)
    ax.text(5.5, 6.3, 'HCM Processes', ha='center', va='center', 
            fontsize=10, fontweight='bold', color='white')

    for x, y, label in hcm_processes:
        box = FancyBboxPatch((x-0.9, y-0.4), 1.8, 0.8, boxstyle="round,pad=0.08",
                             facecolor='#27AE60', alpha=0.75)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, color='white', fontweight='bold')

    # Right side - Sustainability Outcomes
    outcomes = [
        (9.5, 5.5, 'Reduced\nTurnover'),
        (9.5, 4.2, 'Inclusive\nWorkplace'),
        (9.5, 2.9, 'Green Skill\nDevelopment'),
        (9.5, 1.6, 'Sustainable\nProductivity'),
    ]

    header_box3 = FancyBboxPatch((8.3, 6.0), 2.4, 0.6, boxstyle="round,pad=0.1",
                                 facecolor='#2C3E50', alpha=0.9)
    ax.add_patch(header_box3)
    ax.text(9.5, 6.3, 'Sustainability\nOutcomes', ha='center', va='center', 
            fontsize=9, fontweight='bold', color='white')

    for x, y, label in outcomes:
        box = FancyBboxPatch((x-0.9, y-0.4), 1.8, 0.8, boxstyle="round,pad=0.08",
                             facecolor='#E67E22', alpha=0.75)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, color='white', fontweight='bold')

    # Arrows connecting sections
    for i in range(4):
        y_pos = 5.5 - i * 1.3
        ax.annotate('', xy=(4.6, y_pos), xytext=(2.4, y_pos),
                   arrowprops=dict(arrowstyle='->', color='#7F8C8D', lw=2))
        ax.annotate('', xy=(8.6, y_pos), xytext=(6.4, y_pos),
                   arrowprops=dict(arrowstyle='->', color='#7F8C8D', lw=2))

    # Feedback loop at bottom
    ax.annotate('', xy=(2.4, 0.8), xytext=(8.6, 0.8),
               arrowprops=dict(arrowstyle='<->', color='#E74C3C', lw=2.5,
                              connectionstyle='arc3,rad=-0.3'))
    ax.text(5.5, 0.3, 'Continuous Feedback & Optimization Loop', 
            ha='center', va='center', fontsize=9, fontstyle='italic', color='#E74C3C')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_2_HCM_Ecosystem.png', dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 2 created.")

# ============================================================
# FIGURE 3: Risk and Challenge Matrix for GenAI Implementation
# ============================================================
def create_figure3():
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    
    categories = ['Data Privacy', 'Algorithmic\nBias', 'Workforce\nResistance', 
                  'Governance\nGaps', 'Skill\nDeficiency', 'Transparency\nDeficit']
    
    # Impact scores (1-10)
    likelihood = [8.5, 7.8, 7.2, 6.5, 8.0, 7.0]
    impact = [9.0, 8.5, 6.8, 7.5, 7.0, 8.2]
    
    colors = ['#E74C3C', '#E67E22', '#F1C40F', '#3498DB', '#9B59B6', '#1ABC9C']
    sizes = [s * 80 for s in [9.0, 8.5, 7.0, 7.0, 7.5, 7.6]]

    scatter = ax.scatter(likelihood, impact, c=colors, s=sizes, alpha=0.75, edgecolors='black', linewidth=1.5)
    
    for i, cat in enumerate(categories):
        ax.annotate(cat, (likelihood[i], impact[i]), textcoords="offset points", 
                   xytext=(12, 5), fontsize=9, fontweight='bold')

    ax.set_xlabel('Likelihood of Occurrence', fontsize=12, fontweight='bold')
    ax.set_ylabel('Severity of Impact', fontsize=12, fontweight='bold')
    ax.set_title('Figure 3: Risk Assessment Matrix for Generative AI\nImplementation in Organizations', 
                 fontsize=13, fontweight='bold')
    ax.set_xlim(5.5, 9.5)
    ax.set_ylim(5.5, 10)
    ax.grid(True, alpha=0.3, linestyle='--')

    # Quadrant labels
    ax.axhline(y=7.75, color='gray', linestyle=':', alpha=0.5)
    ax.axvline(x=7.5, color='gray', linestyle=':', alpha=0.5)
    ax.text(6.3, 9.5, 'Monitor Closely', fontsize=9, fontstyle='italic', alpha=0.6)
    ax.text(8.2, 9.5, 'Critical Risk Zone', fontsize=9, fontstyle='italic', color='red', alpha=0.7)
    ax.text(6.3, 6.0, 'Low Priority', fontsize=9, fontstyle='italic', alpha=0.6)
    ax.text(8.2, 6.0, 'Proactive Mitigation', fontsize=9, fontstyle='italic', alpha=0.6)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_3_Risk_Matrix.png', dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 3 created.")

# ============================================================
# FIGURE 4: Future Roadmap - AI, Sustainability & Human Capital
# ============================================================
def create_figure4():
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('Figure 4: Future Roadmap for Integrated AI, Sustainability,\nand Human Capital Development', 
                 fontsize=13, fontweight='bold', pad=15)

    # Timeline arrow
    ax.annotate('', xy=(11.5, 3), xytext=(0.5, 3),
               arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=3))

    # Time periods
    periods = [
        (2, 'Short-term\n(2024-2026)', '#3498DB'),
        (5, 'Medium-term\n(2027-2029)', '#27AE60'),
        (8, 'Long-term\n(2030-2035)', '#E67E22'),
        (11, 'Visionary\n(2035+)', '#8E44AD'),
    ]

    for x, label, color in periods:
        # Marker on timeline
        ax.plot(x, 3, 'o', markersize=15, color=color, zorder=5)
        ax.text(x, 2.3, label, ha='center', va='center', fontsize=9, fontweight='bold')
        
    # Items above timeline
    above_items = [
        (2, 4.5, 'AI-Augmented\nAnalytics Adoption', '#3498DB'),
        (5, 4.5, 'Autonomous\nDecision Systems', '#27AE60'),
        (8, 4.5, 'Self-Sustaining\nAI Ecosystems', '#E67E22'),
        (11, 4.5, 'Fully Integrated\nHuman-AI Symbiosis', '#8E44AD'),
    ]

    for x, y, label, color in above_items:
        box = FancyBboxPatch((x-1.1, y-0.4), 2.2, 0.8, boxstyle="round,pad=0.1",
                             facecolor=color, alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, 
                fontweight='bold', color='white')
        ax.annotate('', xy=(x, 3.15), xytext=(x, y-0.4),
                   arrowprops=dict(arrowstyle='->', color=color, lw=1.5, linestyle='--'))

    # Items below timeline
    below_items = [
        (2, 1.3, 'Basic AI Literacy\nPrograms', '#3498DB'),
        (5, 1.3, 'Advanced Human-AI\nCollaboration', '#27AE60'),
        (8, 1.3, 'Sustainable AI\nGovernance Maturity', '#E67E22'),
        (11, 1.3, 'Universal AI\nEthics Standards', '#8E44AD'),
    ]

    for x, y, label, color in below_items:
        box = FancyBboxPatch((x-1.1, y-0.4), 2.2, 0.8, boxstyle="round,pad=0.1",
                             facecolor=color, alpha=0.5)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold')
        ax.annotate('', xy=(x, 2.85), xytext=(x, y+0.4),
                   arrowprops=dict(arrowstyle='->', color=color, lw=1.5, linestyle='--'))

    # Legend labels
    ax.text(6, 5.6, 'Technology Milestones (Above) | Human Capital Milestones (Below)', 
            ha='center', fontsize=10, fontstyle='italic', color='#2C3E50')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_4_Future_Roadmap.png', dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 4 created.")


if __name__ == '__main__':
    create_figure1()
    create_figure2()
    create_figure3()
    create_figure4()
    print("\nAll 4 figures generated successfully!")
