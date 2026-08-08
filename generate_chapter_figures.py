"""
Generate 4 professional figures for the Design Thinking Integration chapter.
Figure 1: Integrated Framework of Design Thinking and Analytical Decision-Making
Figure 2: Integration of Design Thinking and Systems Thinking
Figure 3: Complementarity of Design Thinking and Creative Thinking
Figure 4: AI-Augmented Multimethod Framework for Future Strategic Thinking
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc
import numpy as np
import os

# Create output directory
os.makedirs('/projects/sandbox/AMMAN/chapter_figures', exist_ok=True)

# Color palette - professional academic style
colors = {
    'design': '#2E86AB',       # Blue
    'analytical': '#A23B72',   # Purple
    'systems': '#F18F01',      # Orange
    'creative': '#C73E1D',     # Red
    'integration': '#3B1F2B',  # Dark
    'light_design': '#B8D8E8',
    'light_analytical': '#E0B8D0',
    'light_systems': '#FDDCA0',
    'light_creative': '#F0B8A8',
    'bg': '#FAFAFA',
    'text': '#2C2C2C',
    'arrow': '#555555',
}


def figure_1():
    """Integrated Framework of Design Thinking and Analytical Decision-Making in Strategic Innovation"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    # Title
    ax.text(6, 7.6, 'Integrated Framework: Design Thinking & Analytical Decision-Making',
            ha='center', va='center', fontsize=13, fontweight='bold', color=colors['text'])

    # Design Thinking Process (top row)
    dt_stages = ['Empathize', 'Define', 'Ideate', 'Prototype', 'Test']
    dt_x = [1.5, 3.5, 5.5, 7.5, 9.5]
    for i, (stage, x) in enumerate(zip(dt_stages, dt_x)):
        box = FancyBboxPatch((x-0.7, 6.2), 1.4, 0.8, boxstyle="round,pad=0.1",
                             facecolor=colors['light_design'], edgecolor=colors['design'], linewidth=2)
        ax.add_patch(box)
        ax.text(x, 6.6, stage, ha='center', va='center', fontsize=9, fontweight='bold', color=colors['design'])

    # Arrows between DT stages
    for i in range(len(dt_x)-1):
        ax.annotate('', xy=(dt_x[i+1]-0.7, 6.6), xytext=(dt_x[i]+0.7, 6.6),
                    arrowprops=dict(arrowstyle='->', color=colors['design'], lw=1.5))

    # Analytical Decision-Making Process (bottom row)
    ad_stages = ['Problem\nDefinition', 'Data\nCollection', 'Alternative\nEvaluation', 'Decision\nCriteria', 'Validation']
    ad_x = [1.5, 3.5, 5.5, 7.5, 9.5]
    for i, (stage, x) in enumerate(zip(ad_stages, ad_x)):
        box = FancyBboxPatch((x-0.7, 1.2), 1.4, 0.8, boxstyle="round,pad=0.1",
                             facecolor=colors['light_analytical'], edgecolor=colors['analytical'], linewidth=2)
        ax.add_patch(box)
        ax.text(x, 1.6, stage, ha='center', va='center', fontsize=8, fontweight='bold', color=colors['analytical'])

    # Arrows between AD stages
    for i in range(len(ad_x)-1):
        ax.annotate('', xy=(ad_x[i+1]-0.7, 1.6), xytext=(ad_x[i]+0.7, 1.6),
                    arrowprops=dict(arrowstyle='->', color=colors['analytical'], lw=1.5))

    # Integration zone (middle)
    integration_box = FancyBboxPatch((1.0, 3.0), 9.0, 2.4, boxstyle="round,pad=0.2",
                                     facecolor='#F0F4F8', edgecolor=colors['integration'], linewidth=2, linestyle='--')
    ax.add_patch(integration_box)
    ax.text(5.5, 5.1, 'INTEGRATION ZONE', ha='center', va='center', fontsize=11,
            fontweight='bold', color=colors['integration'])

    # Integration elements
    int_elements = ['Human-Centered\nInsights', 'Thick Data\nSynthesis', 'Creative\nValidation', 'Evidence-Based\nPrototyping', 'Iterative\nDe-risking']
    int_x = [1.5, 3.5, 5.5, 7.5, 9.5]
    for elem, x in zip(int_elements, int_x):
        box = FancyBboxPatch((x-0.65, 3.4), 1.3, 0.9, boxstyle="round,pad=0.05",
                             facecolor='white', edgecolor=colors['integration'], linewidth=1.2)
        ax.add_patch(box)
        ax.text(x, 3.85, elem, ha='center', va='center', fontsize=7.5, color=colors['integration'])

    # Vertical arrows connecting rows
    for x in int_x:
        ax.annotate('', xy=(x, 5.15), xytext=(x, 6.2),
                    arrowprops=dict(arrowstyle='->', color=colors['design'], lw=1, linestyle='--'))
        ax.annotate('', xy=(x, 3.0), xytext=(x, 2.0),
                    arrowprops=dict(arrowstyle='<-', color=colors['analytical'], lw=1, linestyle='--'))

    # Labels
    ax.text(11.2, 6.6, 'DESIGN\nTHINKING', ha='center', va='center', fontsize=9,
            fontweight='bold', color=colors['design'], style='italic')
    ax.text(11.2, 1.6, 'ANALYTICAL\nMETHODS', ha='center', va='center', fontsize=9,
            fontweight='bold', color=colors['analytical'], style='italic')

    # Output arrow
    ax.annotate('', xy=(11.5, 4.2), xytext=(10.0, 4.2),
                arrowprops=dict(arrowstyle='->', color=colors['integration'], lw=2.5))
    ax.text(11.7, 4.2, 'Strategic\nInnovation\nOutcome', ha='left', va='center', fontsize=8,
            fontweight='bold', color=colors['integration'])

    plt.tight_layout()
    plt.savefig('/projects/sandbox/AMMAN/chapter_figures/Figure_1_DT_Analytical_Integration.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 1 saved.")


def figure_2():
    """Integration of Design Thinking and Systems Thinking for Strategic Innovation"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    # Title
    ax.text(6, 7.6, 'Integration of Design Thinking and Systems Thinking for Strategic Innovation',
            ha='center', va='center', fontsize=13, fontweight='bold', color=colors['text'])

    # Left circle - Design Thinking
    circle_dt = plt.Circle((3.2, 4.0), 2.2, facecolor=colors['light_design'], edgecolor=colors['design'],
                           linewidth=2.5, alpha=0.7)
    ax.add_patch(circle_dt)
    ax.text(2.2, 5.5, 'DESIGN THINKING', ha='center', va='center', fontsize=11,
            fontweight='bold', color=colors['design'])
    dt_items = ['Empathy Maps', 'User Journeys', 'Personas', 'Prototypes', 'Co-creation']
    for i, item in enumerate(dt_items):
        ax.text(2.2, 4.8 - i*0.5, f'• {item}', ha='left', va='center', fontsize=8, color=colors['design'])

    # Right circle - Systems Thinking
    circle_st = plt.Circle((8.8, 4.0), 2.2, facecolor=colors['light_systems'], edgecolor=colors['systems'],
                           linewidth=2.5, alpha=0.7)
    ax.add_patch(circle_st)
    ax.text(9.5, 5.5, 'SYSTEMS THINKING', ha='center', va='center', fontsize=11,
            fontweight='bold', color=colors['systems'])
    st_items = ['Causal Loops', 'Feedback Maps', 'Leverage Points', 'Boundaries', 'Emergence']
    for i, item in enumerate(st_items):
        ax.text(9.0, 4.8 - i*0.5, f'• {item}', ha='left', va='center', fontsize=8, color=colors['systems'])

    # Overlap area
    overlap = plt.Circle((6.0, 4.0), 1.5, facecolor='#E8F4E8', edgecolor=colors['integration'],
                         linewidth=2, alpha=0.8, linestyle='--')
    ax.add_patch(overlap)
    ax.text(6.0, 5.0, 'INTEGRATION', ha='center', va='center', fontsize=10,
            fontweight='bold', color=colors['integration'])
    overlap_items = ['Stakeholder\nMapping', 'System-Aware\nDesign', 'Scalable\nSolutions']
    for i, item in enumerate(overlap_items):
        ax.text(6.0, 4.3 - i*0.7, item, ha='center', va='center', fontsize=8, color=colors['integration'])

    # Bottom output box
    output_box = FancyBboxPatch((3.5, 0.5), 5.0, 1.0, boxstyle="round,pad=0.15",
                                facecolor='#E8E0F0', edgecolor=colors['integration'], linewidth=2)
    ax.add_patch(output_box)
    ax.text(6.0, 1.0, 'Solutions addressing root causes with human-centered scalability',
            ha='center', va='center', fontsize=9, fontweight='bold', color=colors['integration'])

    # Arrow from overlap to output
    ax.annotate('', xy=(6.0, 1.5), xytext=(6.0, 2.5),
                arrowprops=dict(arrowstyle='->', color=colors['integration'], lw=2))

    plt.tight_layout()
    plt.savefig('/projects/sandbox/AMMAN/chapter_figures/Figure_2_DT_Systems_Integration.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 2 saved.")


def figure_3():
    """Complementarity of Design Thinking and Creative Thinking in the Innovation Process"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    # Title
    ax.text(6, 7.6, 'Complementarity of Design Thinking and Creative Thinking',
            ha='center', va='center', fontsize=13, fontweight='bold', color=colors['text'])

    # Left column - Creative Thinking (Spontaneous)
    ax.text(2.5, 6.8, 'CREATIVE THINKING', ha='center', va='center', fontsize=11,
            fontweight='bold', color=colors['creative'])
    ax.text(2.5, 6.4, '(Generative Energy)', ha='center', va='center', fontsize=9,
            color=colors['creative'], style='italic')

    creative_items = ['Divergent Thinking', 'Imagination', 'Associative Leaps',
                      'Intuitive Insight', 'Spontaneous Ideas']
    for i, item in enumerate(creative_items):
        box = FancyBboxPatch((1.2, 5.5 - i*0.9), 2.6, 0.6, boxstyle="round,pad=0.08",
                             facecolor=colors['light_creative'], edgecolor=colors['creative'], linewidth=1.5)
        ax.add_patch(box)
        ax.text(2.5, 5.8 - i*0.9, item, ha='center', va='center', fontsize=9, color=colors['creative'])

    # Right column - Design Thinking (Structured)
    ax.text(9.5, 6.8, 'DESIGN THINKING', ha='center', va='center', fontsize=11,
            fontweight='bold', color=colors['design'])
    ax.text(9.5, 6.4, '(Structured Direction)', ha='center', va='center', fontsize=9,
            color=colors['design'], style='italic')

    design_items = ['Empathic Grounding', 'Problem Framing', 'Structured Ideation',
                    'Prototyping & Testing', 'Iterative Refinement']
    for i, item in enumerate(design_items):
        box = FancyBboxPatch((8.2, 5.5 - i*0.9), 2.6, 0.6, boxstyle="round,pad=0.08",
                             facecolor=colors['light_design'], edgecolor=colors['design'], linewidth=1.5)
        ax.add_patch(box)
        ax.text(9.5, 5.8 - i*0.9, item, ha='center', va='center', fontsize=9, color=colors['design'])

    # Center - Innovation Cycle (connecting arrows)
    center_x = 6.0
    ax.text(center_x, 6.8, 'INNOVATION', ha='center', va='center', fontsize=10,
            fontweight='bold', color=colors['integration'])
    ax.text(center_x, 6.4, 'SYNERGY', ha='center', va='center', fontsize=10,
            fontweight='bold', color=colors['integration'])

    # Bidirectional arrows
    synergy_items = ['Novel + Relevant Ideas', 'Directed Exploration', 'Validated Creativity',
                     'Experiential Learning', 'Actionable Innovation']
    for i, item in enumerate(synergy_items):
        y = 5.8 - i*0.9
        # Left arrow
        ax.annotate('', xy=(4.8, y), xytext=(3.8, y),
                    arrowprops=dict(arrowstyle='->', color=colors['arrow'], lw=1.2))
        # Right arrow
        ax.annotate('', xy=(7.2, y), xytext=(8.2, y),
                    arrowprops=dict(arrowstyle='->', color=colors['arrow'], lw=1.2))
        # Center text
        ax.text(center_x, y, item, ha='center', va='center', fontsize=7.5,
                fontweight='bold', color=colors['integration'],
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#F0F0F0', edgecolor='gray', linewidth=0.5))

    # Bottom outcome
    outcome_box = FancyBboxPatch((3.5, 0.5), 5.0, 0.8, boxstyle="round,pad=0.1",
                                  facecolor='#E8F4E8', edgecolor=colors['integration'], linewidth=2)
    ax.add_patch(outcome_box)
    ax.text(6.0, 0.9, 'Creative Confidence → Organizational Innovation Capability',
            ha='center', va='center', fontsize=9.5, fontweight='bold', color=colors['integration'])

    # Arrow to outcome
    ax.annotate('', xy=(6.0, 1.3), xytext=(6.0, 1.9),
                arrowprops=dict(arrowstyle='->', color=colors['integration'], lw=2))

    plt.tight_layout()
    plt.savefig('/projects/sandbox/AMMAN/chapter_figures/Figure_3_DT_Creative_Complementarity.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 3 saved.")


def figure_4():
    """AI-Augmented Multimethod Framework for Future Strategic Thinking"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    # Title
    ax.text(6, 8.6, 'AI-Augmented Multimethod Framework for Strategic Thinking',
            ha='center', va='center', fontsize=13, fontweight='bold', color=colors['text'])

    # Central AI hub
    ai_circle = plt.Circle((6, 4.5), 1.2, facecolor='#E8E0F0', edgecolor=colors['integration'],
                           linewidth=2.5)
    ax.add_patch(ai_circle)
    ax.text(6, 4.8, 'ARTIFICIAL', ha='center', va='center', fontsize=10, fontweight='bold',
            color=colors['integration'])
    ax.text(6, 4.2, 'INTELLIGENCE', ha='center', va='center', fontsize=10, fontweight='bold',
            color=colors['integration'])

    # Four quadrants
    # Top-left: Design Thinking + AI
    box1 = FancyBboxPatch((0.5, 6.5), 4.5, 1.5, boxstyle="round,pad=0.15",
                          facecolor=colors['light_design'], edgecolor=colors['design'], linewidth=2)
    ax.add_patch(box1)
    ax.text(2.75, 7.7, 'AI-Enhanced Design Thinking', ha='center', va='center',
            fontsize=10, fontweight='bold', color=colors['design'])
    ax.text(2.75, 7.2, '• Sentiment analysis at scale', ha='center', va='center', fontsize=8, color=colors['text'])
    ax.text(2.75, 6.85, '• Generative design alternatives', ha='center', va='center', fontsize=8, color=colors['text'])

    # Top-right: Analytical + AI
    box2 = FancyBboxPatch((7.0, 6.5), 4.5, 1.5, boxstyle="round,pad=0.15",
                          facecolor=colors['light_analytical'], edgecolor=colors['analytical'], linewidth=2)
    ax.add_patch(box2)
    ax.text(9.25, 7.7, 'AI-Enhanced Analytics', ha='center', va='center',
            fontsize=10, fontweight='bold', color=colors['analytical'])
    ax.text(9.25, 7.2, '• Predictive modeling', ha='center', va='center', fontsize=8, color=colors['text'])
    ax.text(9.25, 6.85, '• Real-time decision support', ha='center', va='center', fontsize=8, color=colors['text'])

    # Bottom-left: Systems + AI
    box3 = FancyBboxPatch((0.5, 1.0), 4.5, 1.5, boxstyle="round,pad=0.15",
                          facecolor=colors['light_systems'], edgecolor=colors['systems'], linewidth=2)
    ax.add_patch(box3)
    ax.text(2.75, 2.2, 'AI-Enhanced Systems Thinking', ha='center', va='center',
            fontsize=10, fontweight='bold', color=colors['systems'])
    ax.text(2.75, 1.7, '• Agent-based simulation', ha='center', va='center', fontsize=8, color=colors['text'])
    ax.text(2.75, 1.35, '• Digital twin modeling', ha='center', va='center', fontsize=8, color=colors['text'])

    # Bottom-right: Creative + AI
    box4 = FancyBboxPatch((7.0, 1.0), 4.5, 1.5, boxstyle="round,pad=0.15",
                          facecolor=colors['light_creative'], edgecolor=colors['creative'], linewidth=2)
    ax.add_patch(box4)
    ax.text(9.25, 2.2, 'AI-Enhanced Creativity', ha='center', va='center',
            fontsize=10, fontweight='bold', color=colors['creative'])
    ax.text(9.25, 1.7, '• Generative AI ideation', ha='center', va='center', fontsize=8, color=colors['text'])
    ax.text(9.25, 1.35, '• Data-driven inspiration', ha='center', va='center', fontsize=8, color=colors['text'])

    # Connecting lines from AI center to quadrants
    connections = [
        (6, 5.7, 2.75, 6.5),   # to top-left
        (6, 5.7, 9.25, 6.5),   # to top-right
        (6, 3.3, 2.75, 2.5),   # to bottom-left
        (6, 3.3, 9.25, 2.5),   # to bottom-right
    ]
    for x1, y1, x2, y2 in connections:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='<->', color=colors['integration'], lw=1.8,
                                    connectionstyle='arc3,rad=0'))

    # Outer ring labels - Strategic Outcomes
    ax.text(6, 0.3, 'STRATEGIC OUTCOMES: Hybrid Intelligence • Democratized Innovation • Enhanced Foresight • Adaptive Strategy',
            ha='center', va='center', fontsize=9, fontweight='bold', color=colors['integration'],
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#F8F8F8', edgecolor=colors['integration'], linewidth=1.5))

    plt.tight_layout()
    plt.savefig('/projects/sandbox/AMMAN/chapter_figures/Figure_4_AI_Augmented_Framework.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 4 saved.")


# Generate all figures
if __name__ == '__main__':
    figure_1()
    figure_2()
    figure_3()
    figure_4()
    print("\nAll 4 figures generated successfully!")
