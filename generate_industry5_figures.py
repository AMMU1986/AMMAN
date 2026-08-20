"""
Generate all 4 figures for Chapter: Industry 5.0 - Smart, Sustainable, and Human-Centred Transformation
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np
import os

output_dir = "industry5_figures"
os.makedirs(output_dir, exist_ok=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.2


def figure1_evolution_paradigms():
    """
    Figure 1: Evolution from Industry 4.0 to Industry 5.0 with Three Pillars
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(7, 8.6, 'Evolution from Industry 4.0 to Industry 5.0: The Three Pillars',
            fontsize=14, fontweight='bold', ha='center', va='center')

    # Industry 4.0 box (left)
    box40 = FancyBboxPatch((0.5, 5.5), 4.5, 2.2, boxstyle="round,pad=0.1",
                           facecolor='#ECEFF1', edgecolor='#455A64', linewidth=2)
    ax.add_patch(box40)
    ax.text(2.75, 7.2, 'Industry 4.0', fontsize=12, fontweight='bold',
            ha='center', color='#37474F')
    ax.text(2.75, 6.6, 'Automation-Centric', fontsize=9, ha='center', color='#546E7A')
    items_40 = ['IoT & Cyber-Physical Systems', 'Big Data & Cloud', 'Smart Factories', 'Efficiency Focus']
    for i, item in enumerate(items_40):
        ax.text(2.75, 6.1 - i*0.35, f'• {item}', fontsize=8, ha='center')

    # Arrow
    ax.annotate('', xy=(6.0, 6.6), xytext=(5.2, 6.6),
                arrowprops=dict(arrowstyle='->', lw=3, color='#1565C0'))
    ax.text(5.6, 7.0, 'Evolution', fontsize=8, ha='center', style='italic', color='#1565C0')

    # Industry 5.0 box (right)
    box50 = FancyBboxPatch((6.2, 5.5), 7.3, 2.2, boxstyle="round,pad=0.1",
                           facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=2.5)
    ax.add_patch(box50)
    ax.text(9.85, 7.2, 'Industry 5.0', fontsize=12, fontweight='bold',
            ha='center', color='#1B5E20')
    ax.text(9.85, 6.7, 'Human-Centric, Sustainable, Resilient', fontsize=9,
            ha='center', color='#2E7D32')

    # Three pillars below
    pillars = [
        (3.0, 3.2, 'SUSTAINABILITY', '#E3F2FD', '#1565C0',
         ['Environmental imperative', 'Resource efficiency', 'Circular economy', 'Carbon neutrality']),
        (7.0, 3.2, 'HUMAN-CENTRICITY', '#FFF3E0', '#E65100',
         ['Worker empowerment', 'Human-AI collaboration', 'Skills development', 'Well-being focus']),
        (11.0, 3.2, 'RESILIENCE', '#F3E5F5', '#6A1B9A',
         ['Disruption adaptation', 'Supply chain agility', 'Digital sovereignty', 'Crisis preparedness']),
    ]

    for x, y, title, fcolor, ecolor, items in pillars:
        box = FancyBboxPatch((x-1.6, y-1.5), 3.2, 3.0, boxstyle="round,pad=0.1",
                            facecolor=fcolor, edgecolor=ecolor, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y+1.0, title, fontsize=10, fontweight='bold', ha='center', color=ecolor)
        for i, item in enumerate(items):
            ax.text(x, y+0.3 - i*0.4, f'• {item}', fontsize=8, ha='center')

    # Connecting lines from I5.0 to pillars
    for x, _, _, _, _, _ in pillars:
        ax.plot([x, x], [4.7, 5.4], 'k--', lw=1, alpha=0.5)

    # Bottom label
    ax.text(7, 0.5, 'Circular Economy Integration: Design for Circularity | Resource Loops | Lifecycle Extension',
            fontsize=10, ha='center', style='italic', color='#333',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF9C4', edgecolor='#F9A825', lw=1.5))

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_1_Industry5_Evolution.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 1 saved.")


def figure2_digital_twins_circular():
    """
    Figure 2: Digital Twins and Cognitive Digital Twins for Circular Manufacturing
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(7, 9.5, 'Digital Twins & Cognitive Digital Twins for Circular Process Design',
            fontsize=13, fontweight='bold', ha='center', va='center')

    # Physical Layer (bottom)
    phys_box = FancyBboxPatch((0.5, 0.5), 13, 2.2, boxstyle="round,pad=0.1",
                              facecolor='#ECEFF1', edgecolor='#455A64', linewidth=2)
    ax.add_patch(phys_box)
    ax.text(7, 2.3, 'PHYSICAL LAYER: Manufacturing Systems', fontsize=11, fontweight='bold',
            ha='center', color='#37474F')

    phys_items = [
        (2.0, 1.3, 'Raw Material\nInput'),
        (5.0, 1.3, 'Production\nProcesses'),
        (8.0, 1.3, 'Assembly &\nQuality'),
        (11.0, 1.3, 'End-of-Life\nRecovery'),
    ]
    for x, y, text in phys_items:
        box = FancyBboxPatch((x-0.9, y-0.4), 1.8, 0.8, boxstyle="round,pad=0.03",
                            facecolor='white', edgecolor='#455A64', linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=8, ha='center', va='center')

    # Arrows between physical items
    for i in range(3):
        ax.annotate('', xy=(phys_items[i+1][0]-0.95, 1.3),
                    xytext=(phys_items[i][0]+0.95, 1.3),
                    arrowprops=dict(arrowstyle='->', lw=1.2, color='#455A64'))
    # Circular arrow back
    ax.annotate('', xy=(2.0, 0.7), xytext=(11.0, 0.7),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='#2E7D32',
                               connectionstyle='arc3,rad=0.4', linestyle='--'))
    ax.text(6.5, 0.3, 'Circular Material Flow', fontsize=8, ha='center', color='#2E7D32', style='italic')

    # Digital Twin Layer (middle)
    dt_box = FancyBboxPatch((0.5, 3.5), 13, 2.2, boxstyle="round,pad=0.1",
                            facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=2)
    ax.add_patch(dt_box)
    ax.text(7, 5.3, 'DIGITAL TWIN LAYER: Virtual Simulation & Optimization', fontsize=11,
            fontweight='bold', ha='center', color='#1565C0')

    dt_items = [
        (2.5, 4.3, 'Process\nSimulation'),
        (5.5, 4.3, 'Material Flow\nModelling'),
        (8.5, 4.3, 'Disassembly\nStrategy'),
        (11.5, 4.3, 'Lifecycle\nAssessment'),
    ]
    for x, y, text in dt_items:
        box = FancyBboxPatch((x-0.9, y-0.4), 1.8, 0.8, boxstyle="round,pad=0.03",
                            facecolor='white', edgecolor='#1565C0', linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=8, ha='center', va='center')

    # Cognitive DT Layer (top)
    cdt_box = FancyBboxPatch((0.5, 6.5), 13, 2.2, boxstyle="round,pad=0.1",
                             facecolor='#F3E5F5', edgecolor='#6A1B9A', linewidth=2)
    ax.add_patch(cdt_box)
    ax.text(7, 8.3, 'COGNITIVE DIGITAL TWIN LAYER: AI-Driven Decision Support', fontsize=11,
            fontweight='bold', ha='center', color='#6A1B9A')

    cdt_items = [
        (2.5, 7.3, 'Explainable AI\n(XAI)'),
        (5.5, 7.3, 'Predictive\nMaintenance'),
        (8.5, 7.3, 'Circularity\nOptimization'),
        (11.5, 7.3, 'Digital Product\nPassport'),
    ]
    for x, y, text in cdt_items:
        box = FancyBboxPatch((x-0.9, y-0.4), 1.8, 0.8, boxstyle="round,pad=0.03",
                            facecolor='white', edgecolor='#6A1B9A', linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=8, ha='center', va='center')

    # Vertical connectors
    for x in [2.5, 5.5, 8.5, 11.5]:
        ax.annotate('', xy=(x, 5.7), xytext=(x, 6.45),
                    arrowprops=dict(arrowstyle='<->', lw=1, color='#555'))
    for x in [2.0, 5.0, 8.0, 11.0]:
        ax.annotate('', xy=(x, 2.75), xytext=(x, 3.45),
                    arrowprops=dict(arrowstyle='<->', lw=1, color='#555'))

    # Standards labels on right
    ax.text(13.8, 7.3, 'OPC UA', fontsize=7, ha='right', color='#6A1B9A', style='italic')
    ax.text(13.8, 4.3, 'RAMI4.0', fontsize=7, ha='right', color='#1565C0', style='italic')
    ax.text(13.8, 1.3, 'AutomationML', fontsize=7, ha='right', color='#455A64', style='italic')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_2_Digital_Twins_Circular.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 2 saved.")


def figure3_case_studies():
    """
    Figure 3: Sectoral Applications - PV Manufacturing and FMCG Circular Models
    """
    fig = plt.figure(figsize=(14, 9))
    gs = fig.add_gridspec(1, 2, wspace=0.3)

    # Panel A: PV Manufacturing Circular Design
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('(A) Photovoltaic Manufacturing:\nCircular-by-Design Approach', fontsize=11, fontweight='bold')

    # Circular flow for PV
    phases = [
        (5, 8.5, 'Material\nSelection', '#E3F2FD'),
        (8.5, 6.5, 'Product\nDesign', '#E8F5E9'),
        (8.5, 3.5, 'Manufacturing\nProcess', '#FFF3E0'),
        (5, 1.5, 'Use Phase &\nMaintenance', '#F3E5F5'),
        (1.5, 3.5, 'End-of-Life\nRecovery', '#FFEBEE'),
        (1.5, 6.5, 'Remanufacture\n& Reuse', '#E0F7FA'),
    ]

    for x, y, text, color in phases:
        box = FancyBboxPatch((x-1.2, y-0.6), 2.4, 1.2, boxstyle="round,pad=0.05",
                            facecolor=color, edgecolor='#333', linewidth=1.5)
        ax1.add_patch(box)
        ax1.text(x, y, text, fontsize=8, ha='center', va='center', fontweight='bold')

    # Arrows connecting in circle
    connections = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,0)]
    for s, e in connections:
        sx, sy = phases[s][0], phases[s][1]
        ex, ey = phases[e][0], phases[e][1]
        dx = ex - sx
        dy = ey - sy
        dist = np.sqrt(dx**2 + dy**2)
        ax1.annotate('', xy=(ex - dx/dist*1.3, ey - dy/dist*0.7),
                    xytext=(sx + dx/dist*1.3, sy + dy/dist*0.7),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color='#2E7D32'))

    ax1.text(5, 5, 'Circular\nEconomy', fontsize=10, ha='center', va='center',
            color='#2E7D32', fontweight='bold', style='italic')

    # Panel B: FMCG Decentralized Model (STARHAUS)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('(B) FMCG Decentralized Manufacturing:\nSTARHAUS Framework', fontsize=11, fontweight='bold')

    # Central hub
    circle = plt.Circle((5, 5), 1.5, facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=2)
    ax2.add_patch(circle)
    ax2.text(5, 5.2, 'Community', fontsize=9, ha='center', fontweight='bold', color='#2E7D32')
    ax2.text(5, 4.7, 'Co-Design Hub', fontsize=8, ha='center', color='#2E7D32')

    # Surrounding nodes
    nodes = [
        (5, 8.5, 'Pet Food\nProduction', '#BBDEFB'),
        (8.5, 6.5, 'Fertilizer\nManufacturing', '#C8E6C9'),
        (8.5, 3.5, 'Beverage\nProcessing', '#FFE0B2'),
        (5, 1.5, 'Cereal\nProduction', '#E1BEE7'),
        (1.5, 3.5, 'Local\nSuppliers', '#FFCDD2'),
        (1.5, 6.5, 'Renewable\nEnergy', '#B2EBF2'),
    ]

    for x, y, text, color in nodes:
        box = FancyBboxPatch((x-1.0, y-0.5), 2.0, 1.0, boxstyle="round,pad=0.05",
                            facecolor=color, edgecolor='#555', linewidth=1.2)
        ax2.add_patch(box)
        ax2.text(x, y, text, fontsize=7.5, ha='center', va='center', fontweight='bold')

    # Lines from center to nodes
    for x, y, _, _ in nodes:
        dx = x - 5
        dy = y - 5
        dist = np.sqrt(dx**2 + dy**2)
        ax2.plot([5 + dx/dist*1.6, x - dx/dist*1.1],
                [5 + dy/dist*1.6, y - dy/dist*0.6], 'k--', lw=1, alpha=0.6)

    # SDG alignment note
    ax2.text(5, 0.3, 'Aligned with UN SDGs: 7, 8, 9, 11, 12, 13',
            fontsize=8, ha='center', style='italic', color='#555')

    plt.savefig(f'{output_dir}/Figure_3_Case_Studies.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 3 saved.")


def figure4_implementation_future():
    """
    Figure 4: Strategic Implementation Framework and Future Directions
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(7, 9.5, 'Strategic Implementation Framework for Industry 5.0-Circular Integration',
            fontsize=13, fontweight='bold', ha='center', va='center')

    # Four quadrants
    # Top-left: Barriers
    box1 = FancyBboxPatch((0.3, 5.0), 6.2, 3.8, boxstyle="round,pad=0.1",
                          facecolor='#FFEBEE', edgecolor='#C62828', linewidth=1.5)
    ax.add_patch(box1)
    ax.text(3.4, 8.4, 'Barriers to Integration', fontsize=11, fontweight='bold',
            ha='center', color='#C62828')
    barriers = ['Organizational resistance to change',
                'Technical interoperability gaps',
                'Data standardization challenges',
                'Policy misalignments',
                'Skills & workforce gaps',
                'Investment uncertainty']
    for i, b in enumerate(barriers):
        ax.text(3.4, 7.8 - i*0.45, f'  {i+1}. {b}', fontsize=8.5, ha='center')

    # Top-right: Enablers
    box2 = FancyBboxPatch((7.5, 5.0), 6.2, 3.8, boxstyle="round,pad=0.1",
                          facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=1.5)
    ax.add_patch(box2)
    ax.text(10.6, 8.4, 'Strategic Enablers', fontsize=11, fontweight='bold',
            ha='center', color='#2E7D32')
    enablers = ['Digital twin infrastructure',
                'AI-driven optimization',
                'Policy incentive alignment',
                'Public-private partnerships',
                'Standards harmonization',
                'Workforce upskilling programs']
    for i, e in enumerate(enablers):
        ax.text(10.6, 7.8 - i*0.45, f'  {i+1}. {e}', fontsize=8.5, ha='center')

    # Bottom: Future Directions Timeline
    ax.plot([1, 13], [2.5, 2.5], 'k-', lw=2)
    ax.text(7, 4.2, 'Future Research & Emerging Trends', fontsize=11, fontweight='bold', ha='center')

    milestones = [
        (2.5, 'Short-term\n(2025-2027)', 'Standardized\ncircularity metrics', '#1565C0'),
        (5.5, 'Medium-term\n(2027-2030)', 'Manufacturing\nas a Service', '#E65100'),
        (8.5, 'Long-term\n(2030-2035)', 'Fully autonomous\ncircular systems', '#6A1B9A'),
        (11.5, 'Frontier\n(2035+)', 'Self-healing\nvalue chains', '#C62828'),
    ]

    for x, period, desc, color in milestones:
        ax.plot(x, 2.5, 'o', markersize=12, color=color, zorder=5)
        ax.text(x, 3.2, period, fontsize=8.5, fontweight='bold', ha='center', color=color)
        ax.text(x, 1.6, desc, fontsize=8, ha='center')

    ax.annotate('', xy=(13.3, 2.5), xytext=(12.8, 2.5),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))

    # Arrow connecting barriers to enablers
    ax.annotate('', xy=(7.4, 6.9), xytext=(6.6, 6.9),
                arrowprops=dict(arrowstyle='->', lw=2.5, color='#2E7D32'))
    ax.text(7.0, 7.2, 'Overcome\nwith', fontsize=7, ha='center', color='#2E7D32')

    # Bottom note
    ax.text(7, 0.5, 'EU Policy Frameworks | UN SDG Alignment | Multi-Level Governance | Evidence-Based Design',
            fontsize=9, ha='center', style='italic', color='#555')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_4_Implementation_Future.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 4 saved.")


if __name__ == '__main__':
    print("Generating Industry 5.0 Chapter figures...")
    figure1_evolution_paradigms()
    figure2_digital_twins_circular()
    figure3_case_studies()
    figure4_implementation_future()
    print(f"\nAll figures saved to '{output_dir}/'")
    for f in sorted(os.listdir(output_dir)):
        size = os.path.getsize(os.path.join(output_dir, f)) / 1024
        print(f"  - {f} ({size:.0f} KB)")
