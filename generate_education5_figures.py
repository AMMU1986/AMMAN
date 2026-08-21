"""
Generate all 4 figures for Chapter: Advancing Education 5.0 through AI Readiness and Acceptance
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

output_dir = "education5_figures"
os.makedirs(output_dir, exist_ok=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.2


def figure1_ai_readiness_framework():
    """
    Figure 1: Multi-Layered AI Readiness Assessment Framework for Higher Education 5.0
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(7, 9.5, 'Multi-Layered AI Readiness Assessment Framework for Higher Education 5.0',
            fontsize=13, fontweight='bold', ha='center', va='center')

    # Four layers from bottom to top
    layers = [
        (1.2, '#E3F2FD', '#1565C0', 'INPUT LAYER', 'Institutional & Stakeholder Data',
         ['Infrastructure data', 'AI investments', 'Training records', 'Surveys & interviews', 'Usage analytics']),
        (3.4, '#E8F5E9', '#2E7D32', 'READINESS LAYER', 'Multi-Dimensional Capability Assessment',
         ['Technological', 'Human', 'Organizational', 'Ethical/Governance', 'Cultural']),
        (5.6, '#FFF3E0', '#E65100', 'ACCEPTANCE LAYER', 'Stakeholder Willingness & Preparedness',
         ['Perceived usefulness', 'Ease of use', 'Trust', 'Self-efficacy', 'Behavioral intention']),
        (7.8, '#F3E5F5', '#6A1B9A', 'TRANSFORMATION LAYER', 'Education 5.0 Outcomes',
         ['Teaching quality', 'Personalized learning', 'Research productivity', 'Admin efficiency', 'Innovation']),
    ]

    for y, fcolor, ecolor, title, subtitle, items in layers:
        box = FancyBboxPatch((0.5, y), 13, 1.8, boxstyle="round,pad=0.1",
                            facecolor=fcolor, edgecolor=ecolor, linewidth=2)
        ax.add_patch(box)
        ax.text(1.5, y+1.4, title, fontsize=11, fontweight='bold', color=ecolor)
        ax.text(1.5, y+1.0, subtitle, fontsize=9, color=ecolor, style='italic')
        for i, item in enumerate(items):
            x_pos = 2.0 + i * 2.4
            box_item = FancyBboxPatch((x_pos-0.9, y+0.15), 1.8, 0.6, boxstyle="round,pad=0.03",
                                     facecolor='white', edgecolor=ecolor, linewidth=0.8)
            ax.add_patch(box_item)
            ax.text(x_pos, y+0.45, item, fontsize=7.5, ha='center', va='center')

    # Arrows between layers
    for i in range(3):
        y_start = layers[i][0] + 1.8
        y_end = layers[i+1][0]
        ax.annotate('', xy=(7, y_end), xytext=(7, y_start),
                    arrowprops=dict(arrowstyle='->', lw=2, color='#555'))

    # Formula box
    ax.text(12.5, 0.5, 'AIR = \u03A3(w\u1d62 \u00d7 R\u1d62)', fontsize=10,
            ha='center', va='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFFDE7', edgecolor='#F9A825', lw=1.5))

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_1_AI_Readiness_Framework.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 1 saved.")


def figure2_dimensions_readiness():
    """
    Figure 2: Five Dimensions of AI Readiness in Higher Education
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(6, 9.5, 'Five Dimensions of AI Readiness in Higher Education',
            fontsize=13, fontweight='bold', ha='center', va='center')

    # Central hub
    circle = plt.Circle((6, 5), 1.3, facecolor='#E8EAF6', edgecolor='#283593', linewidth=2.5)
    ax.add_patch(circle)
    ax.text(6, 5.2, 'AI', fontsize=14, fontweight='bold', ha='center', color='#283593')
    ax.text(6, 4.7, 'Readiness', fontsize=11, fontweight='bold', ha='center', color='#283593')

    # Five dimensions around the center
    dimensions = [
        (6, 8.5, 'Technological\nReadiness', '#E3F2FD', '#1565C0',
         'Infrastructure, cloud,\ndata platforms, security'),
        (10, 6.8, 'Human\nReadiness', '#E8F5E9', '#2E7D32',
         'AI literacy, data skills,\nprompt engineering'),
        (9.5, 2.5, 'Organizational\nReadiness', '#FFF3E0', '#E65100',
         'Leadership, strategy,\nfunding, support'),
        (2.5, 2.5, 'Ethical &\nGovernance', '#F3E5F5', '#6A1B9A',
         'Privacy, bias, transparency,\naccountability'),
        (2, 6.8, 'Cultural\nReadiness', '#FFEBEE', '#C62828',
         'Innovation mindset,\nexperimentation culture'),
    ]

    for x, y, title, fcolor, ecolor, desc in dimensions:
        box = FancyBboxPatch((x-1.4, y-0.9), 2.8, 1.8, boxstyle="round,pad=0.08",
                            facecolor=fcolor, edgecolor=ecolor, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y+0.3, title, fontsize=9.5, fontweight='bold', ha='center', va='center', color=ecolor)
        ax.text(x, y-0.4, desc, fontsize=7.5, ha='center', va='center')

        # Line to center
        dx = 6 - x
        dy = 5 - y
        dist = np.sqrt(dx**2 + dy**2)
        sx = x + dx/dist*1.5
        sy = y + dy/dist*1.0
        ex = 6 - dx/dist*1.4
        ey = 5 - dy/dist*1.4
        ax.plot([sx, ex], [sy, ey], '-', lw=1.5, color='#555', alpha=0.6)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_2_Dimensions_Readiness.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 2 saved.")


def figure3_acceptance_model():
    """
    Figure 3: Academic Community AI Acceptance Model
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(7, 8.6, 'Academic Community AI Acceptance Model',
            fontsize=13, fontweight='bold', ha='center', va='center')

    # External factors (left)
    ext_factors = [
        (1.8, 7.0, 'Institutional\nSupport'),
        (1.8, 5.5, 'Training &\nDevelopment'),
        (1.8, 4.0, 'AI Literacy\nLevel'),
        (1.8, 2.5, 'Social\nInfluence'),
    ]

    for x, y, text in ext_factors:
        box = FancyBboxPatch((x-1.1, y-0.4), 2.2, 0.8, boxstyle="round,pad=0.05",
                            facecolor='#ECEFF1', edgecolor='#455A64', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=8.5, ha='center', va='center', fontweight='bold')

    # Core constructs (middle)
    core = [
        (5.5, 6.5, 'Perceived\nUsefulness', '#E3F2FD', '#1565C0'),
        (5.5, 4.5, 'Perceived\nEase of Use', '#E8F5E9', '#2E7D32'),
        (5.5, 2.5, 'Trust in\nAI Systems', '#FFF3E0', '#E65100'),
    ]

    for x, y, text, fcolor, ecolor in core:
        box = FancyBboxPatch((x-1.2, y-0.5), 2.4, 1.0, boxstyle="round,pad=0.08",
                            facecolor=fcolor, edgecolor=ecolor, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=9, ha='center', va='center', fontweight='bold', color=ecolor)

    # Mediator
    med_box = FancyBboxPatch((8.3, 4.0), 2.4, 1.0, boxstyle="round,pad=0.08",
                            facecolor='#F3E5F5', edgecolor='#6A1B9A', linewidth=2)
    ax.add_patch(med_box)
    ax.text(9.5, 4.5, 'Behavioral\nIntention', fontsize=9, ha='center', va='center',
            fontweight='bold', color='#6A1B9A')

    # Outcome (right)
    out_box = FancyBboxPatch((11.3, 4.0), 2.2, 1.0, boxstyle="round,pad=0.08",
                            facecolor='#FFEBEE', edgecolor='#C62828', linewidth=2)
    ax.add_patch(out_box)
    ax.text(12.4, 4.5, 'Actual AI\nUse', fontsize=9, ha='center', va='center',
            fontweight='bold', color='#C62828')

    # Arrows: external -> core
    for i, (ex, ey, _) in enumerate(ext_factors):
        targets = [(5.5, 6.5), (5.5, 4.5), (5.5, 2.5)]
        closest = min(targets, key=lambda t: abs(t[1] - ey))
        ax.annotate('', xy=(closest[0]-1.2, closest[1]), xytext=(ex+1.1, ey),
                    arrowprops=dict(arrowstyle='->', lw=1, color='#777'))

    # Arrows: core -> mediator
    for x, y, _, _, _ in core:
        ax.annotate('', xy=(8.3, 4.5), xytext=(x+1.2, y),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color='#555'))

    # Arrow: mediator -> outcome
    ax.annotate('', xy=(11.3, 4.5), xytext=(10.7, 4.5),
                arrowprops=dict(arrowstyle='->', lw=2, color='#333'))

    # Moderators (bottom)
    ax.text(7, 1.2, 'Moderators: Discipline | Experience | Gender | Institution Type | Country',
            fontsize=9, ha='center', style='italic', color='#555',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF9C4', edgecolor='#F9A825', lw=1))

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_3_Acceptance_Model.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 3 saved.")


def figure4_transformation_roadmap():
    """
    Figure 4: Strategic Pathway from AI Readiness to Education 5.0 Transformation
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(7, 8.6, 'Strategic Pathway: From AI Readiness to Education 5.0 Transformation',
            fontsize=13, fontweight='bold', ha='center', va='center')

    # Six-phase cycle
    phases = [
        (2.3, 6.5, 'ASSESS', 'Readiness audit,\ngap analysis', '#E3F2FD', '#1565C0'),
        (5.0, 6.5, 'PREPARE', 'Strategy, training,\ninfrastructure', '#E8F5E9', '#2E7D32'),
        (7.7, 6.5, 'PILOT', 'Controlled AI\nexperiments', '#FFF3E0', '#E65100'),
        (10.4, 6.5, 'EVALUATE', 'Impact assessment,\nfeedback', '#F3E5F5', '#6A1B9A'),
        (12.0, 4.0, 'SCALE', 'Institutional\nrollout', '#FFEBEE', '#C62828'),
        (9.5, 4.0, 'MONITOR', 'Continuous tracking,\nadaptation', '#E0F7FA', '#00695C'),
    ]

    for x, y, title, desc, fcolor, ecolor in phases:
        box = FancyBboxPatch((x-1.1, y-0.7), 2.2, 1.4, boxstyle="round,pad=0.08",
                            facecolor=fcolor, edgecolor=ecolor, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y+0.25, title, fontsize=10, fontweight='bold', ha='center', color=ecolor)
        ax.text(x, y-0.3, desc, fontsize=7.5, ha='center', va='center')

    # Arrows between top phases
    for i in range(3):
        ax.annotate('', xy=(phases[i+1][0]-1.1, 6.5),
                    xytext=(phases[i][0]+1.1, 6.5),
                    arrowprops=dict(arrowstyle='->', lw=2, color='#555'))

    # Arrow from EVALUATE down to SCALE
    ax.annotate('', xy=(12.0, 5.4), xytext=(10.4, 5.8),
                arrowprops=dict(arrowstyle='->', lw=2, color='#555'))

    # Arrow from SCALE to MONITOR
    ax.annotate('', xy=(9.5+1.1, 4.0), xytext=(12.0-1.1, 4.0),
                arrowprops=dict(arrowstyle='<-', lw=2, color='#555'))

    # Feedback loop from MONITOR back to ASSESS
    ax.annotate('', xy=(2.3, 5.7), xytext=(9.5, 3.3),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='#00695C',
                               connectionstyle='arc3,rad=-0.4', linestyle='--'))
    ax.text(5.5, 3.0, 'Continuous Improvement Loop', fontsize=9, ha='center',
            style='italic', color='#00695C')

    # Readiness levels at bottom
    ax.text(7, 1.8, 'Institutional Readiness Levels', fontsize=11, fontweight='bold', ha='center')
    levels = [
        (1.8, 'Level 1\nInitial', '#FFCDD2'),
        (4.3, 'Level 2\nEmerging', '#FFE0B2'),
        (6.8, 'Level 3\nDeveloping', '#FFF9C4'),
        (9.3, 'Level 4\nAdvanced', '#C8E6C9'),
        (11.8, 'Level 5\nTransformative', '#B2EBF2'),
    ]

    for x, text, color in levels:
        box = FancyBboxPatch((x-0.9, 0.5), 1.8, 0.9, boxstyle="round,pad=0.05",
                            facecolor=color, edgecolor='#555', linewidth=1)
        ax.add_patch(box)
        ax.text(x, 0.95, text, fontsize=8, ha='center', va='center', fontweight='bold')

    # Arrow across levels
    ax.annotate('', xy=(12.5, 0.95), xytext=(1.0, 0.95),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='#333', linestyle='--'))

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_4_Transformation_Roadmap.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 4 saved.")


if __name__ == '__main__':
    print("Generating Education 5.0 Chapter figures...")
    figure1_ai_readiness_framework()
    figure2_dimensions_readiness()
    figure3_acceptance_model()
    figure4_transformation_roadmap()
    print(f"\nAll figures saved to '{output_dir}/'")
    for f in sorted(os.listdir(output_dir)):
        size = os.path.getsize(os.path.join(output_dir, f)) / 1024
        print(f"  - {f} ({size:.0f} KB)")
