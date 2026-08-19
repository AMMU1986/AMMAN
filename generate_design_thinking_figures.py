"""
Generate all 4 figures for Chapter: Operational Excellence through Human-Centered Systems
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge
import numpy as np
import os

# Create output directory
output_dir = "design_thinking_figures"
os.makedirs(output_dir, exist_ok=True)

# Set global style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.2


def figure1_design_thinking_operations():
    """
    Figure 1: The Five Stages of Design Thinking Mapped to Operational Contexts
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    # Title
    ax.text(7, 8.6, 'The Five Stages of Design Thinking in Operational Excellence',
            fontsize=14, fontweight='bold', ha='center', va='center')
    
    # Five stages as connected hexagons/circles
    stages = [
        (1.8, 5.5, 'EMPATHIZE', '#E3F2FD', '#1565C0'),
        (4.6, 5.5, 'DEFINE', '#E8F5E9', '#2E7D32'),
        (7.4, 5.5, 'IDEATE', '#FFF3E0', '#E65100'),
        (10.2, 5.5, 'PROTOTYPE', '#F3E5F5', '#6A1B9A'),
        (13.0, 5.5, 'TEST', '#FFEBEE', '#C62828'),
    ]
    
    for x, y, text, fcolor, ecolor in stages:
        circle = plt.Circle((x, y), 1.1, facecolor=fcolor, edgecolor=ecolor, linewidth=2.5)
        ax.add_patch(circle)
        ax.text(x, y + 0.1, text, fontsize=10, fontweight='bold', ha='center', va='center', color=ecolor)
    
    # Arrows between stages
    for i in range(4):
        x1 = stages[i][0] + 1.15
        x2 = stages[i+1][0] - 1.15
        ax.annotate('', xy=(x2, 5.5), xytext=(x1, 5.5),
                    arrowprops=dict(arrowstyle='->', lw=2, color='#555'))
    
    # Feedback loop arrow (from Test back to Empathize)
    from matplotlib.patches import FancyArrowPatch
    ax.annotate('', xy=(1.8, 4.2), xytext=(13.0, 4.2),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='#888', 
                               connectionstyle='arc3,rad=0.3', linestyle='--'))
    ax.text(7.4, 3.4, 'Iterative Feedback Loop', fontsize=9, ha='center', 
            style='italic', color='#666')
    
    # Operational context for each stage (below)
    op_contexts = [
        (1.8, 7.5, 'Observe warehouse\nassociates, logistics\ncoordinators, customers'),
        (4.6, 7.5, 'Reframe operational\nproblems beyond\nsurface symptoms'),
        (7.4, 7.5, 'Cross-functional\nbrainstorming &\ncreative solutions'),
        (10.2, 7.5, 'Process simulations\n& digital twins for\ntesting changes'),
        (13.0, 7.5, 'Real-world pilot\nruns with iterative\nrefinement'),
    ]
    
    for x, y, text in op_contexts:
        box = FancyBboxPatch((x-1.1, y-0.55), 2.2, 1.1, boxstyle="round,pad=0.05",
                            facecolor='#FAFAFA', edgecolor='#999', linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=8, ha='center', va='center')
        ax.plot([x, x], [y-0.55, 6.6], 'k--', lw=0.8, alpha=0.5)
    
    # Bottom row - Traditional vs Human-Centered comparison
    ax.plot([0.5, 13.5], [2.5, 2.5], 'k-', lw=0.8)
    ax.text(7, 2.2, 'Paradigm Shift: From Efficiency-First to Experience-First Operations',
            fontsize=11, fontweight='bold', ha='center')
    
    comparisons = [
        (3.5, 1.4, 'Traditional Ops:\nWaste reduction\nVariance elimination\nPeople as variables', '#FFCDD2'),
        (10.5, 1.4, 'Human-Centered Ops:\nExperience optimization\nEmpathy-driven insight\nPeople as innovators', '#C8E6C9'),
    ]
    
    for x, y, text, color in comparisons:
        box = FancyBboxPatch((x-2.2, y-0.7), 4.4, 1.4, boxstyle="round,pad=0.1",
                            facecolor=color, edgecolor='#555', linewidth=1.2)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=9, ha='center', va='center')
    
    # Arrow between comparisons
    ax.annotate('', xy=(8.0, 1.4), xytext=(6.0, 1.4),
                arrowprops=dict(arrowstyle='->', lw=2.5, color='#2E7D32'))
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_1_Design_Thinking_Operations.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 1 saved successfully.")


def figure2_human_centered_process_mapping():
    """
    Figure 2: Human-Centered Process Mapping Framework
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Human-Centered Process Mapping: Integrating User Journey with Operations',
            fontsize=13, fontweight='bold', ha='center', va='center')
    
    # Two parallel tracks
    # Top track: Operational Process Flow
    ax.text(7, 8.7, 'Operational Process Flow', fontsize=11, fontweight='bold', 
            ha='center', color='#1565C0')
    
    process_steps = [
        (1.5, 7.8, 'Order\nReceived'),
        (4.0, 7.8, 'Warehouse\nPick & Pack'),
        (6.5, 7.8, 'Quality\nCheck'),
        (9.0, 7.8, 'Shipping &\nLogistics'),
        (11.5, 7.8, 'Last Mile\nDelivery'),
    ]
    
    for x, y, text in process_steps:
        box = FancyBboxPatch((x-0.9, y-0.45), 1.8, 0.9, boxstyle="round,pad=0.05",
                            facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=8.5, ha='center', va='center', fontweight='bold')
    
    for i in range(4):
        ax.annotate('', xy=(process_steps[i+1][0]-0.95, 7.8), 
                    xytext=(process_steps[i][0]+0.95, 7.8),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color='#1565C0'))
    
    # Middle: Emotional Journey / Pain Points
    ax.text(7, 6.6, 'User Emotional Journey & Pain Points', fontsize=11, fontweight='bold',
            ha='center', color='#E65100')
    
    emotions = [
        (1.5, 5.9, 'Anticipation\n(Positive)', '#C8E6C9'),
        (4.0, 5.9, 'Frustration\n(Pain Point)', '#FFCDD2'),
        (6.5, 5.9, 'Anxiety\n(Uncertainty)', '#FFF9C4'),
        (9.0, 5.9, 'Impatience\n(Pain Point)', '#FFCDD2'),
        (11.5, 5.9, 'Satisfaction\n(Positive)', '#C8E6C9'),
    ]
    
    for x, y, text, color in emotions:
        box = FancyBboxPatch((x-0.9, y-0.45), 1.8, 0.9, boxstyle="round,pad=0.05",
                            facecolor=color, edgecolor='#E65100', linewidth=1.2)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=8.5, ha='center', va='center')
    
    # Connecting lines between process and emotion
    for step in process_steps:
        ax.plot([step[0], step[0]], [step[1]-0.5, 6.35], 'k:', lw=0.8, alpha=0.6)
    
    # Bottom track: Design Thinking Interventions
    ax.text(7, 4.7, 'Design Thinking Interventions', fontsize=11, fontweight='bold',
            ha='center', color='#6A1B9A')
    
    interventions = [
        (1.5, 3.9, 'Persona\nDevelopment'),
        (4.0, 3.9, 'Ergonomic\nRedesign'),
        (6.5, 3.9, 'Visual\nManagement'),
        (9.0, 3.9, 'Real-time\nTracking'),
        (11.5, 3.9, 'Feedback\nLoop'),
    ]
    
    for x, y, text in interventions:
        box = FancyBboxPatch((x-0.9, y-0.45), 1.8, 0.9, boxstyle="round,pad=0.05",
                            facecolor='#F3E5F5', edgecolor='#6A1B9A', linewidth=1.2)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=8.5, ha='center', va='center')
    
    # Connecting lines from emotions to interventions
    for em in emotions:
        ax.plot([em[0], em[0]], [em[1]-0.5, 4.35], 'k:', lw=0.8, alpha=0.6)
    
    # Bottom section - Key Principles
    ax.plot([0.5, 13.5], [2.8, 2.8], 'k-', lw=0.8)
    ax.text(7, 2.5, 'Key Principles of Human-Centered Process Mapping', fontsize=10, 
            fontweight='bold', ha='center')
    
    principles = [
        (2.5, 1.5, 'Document\nEmotional States', '#BBDEFB'),
        (5.5, 1.5, 'Identify\nFriction Points', '#FFCCBC'),
        (8.5, 1.5, 'Validate with\nObservation', '#C8E6C9'),
        (11.5, 1.5, 'Evidence-Based\nPrioritization', '#E1BEE7'),
    ]
    
    for x, y, text, color in principles:
        box = FancyBboxPatch((x-1.2, y-0.5), 2.4, 1.0, boxstyle="round,pad=0.05",
                            facecolor=color, edgecolor='#555', linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=9, ha='center', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_2_Process_Mapping_Framework.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 2 saved successfully.")


def figure3_supply_chain_resilience():
    """
    Figure 3: Supply Chain Resilience through Human-Centered Design & AI Integration
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Supply Chain Resilience: Integrating Design Thinking with AI Adoption',
            fontsize=13, fontweight='bold', ha='center', va='center')
    
    # Central framework - three concentric rings concept
    # Outer ring: Supply Chain Ecosystem
    outer = plt.Circle((7, 5.2), 3.8, facecolor='#E8F5E9', edgecolor='#2E7D32', 
                       linewidth=2, alpha=0.3)
    ax.add_patch(outer)
    ax.text(7, 8.8, 'Supply Chain Ecosystem', fontsize=10, fontweight='bold',
            ha='center', color='#2E7D32')
    
    # Middle ring: Design Thinking Layer
    middle = plt.Circle((7, 5.2), 2.5, facecolor='#E3F2FD', edgecolor='#1565C0',
                        linewidth=2, alpha=0.4)
    ax.add_patch(middle)
    ax.text(7, 7.5, 'Design Thinking Layer', fontsize=9, fontweight='bold',
            ha='center', color='#1565C0')
    
    # Inner core: AI & Technology
    inner = plt.Circle((7, 5.2), 1.3, facecolor='#F3E5F5', edgecolor='#6A1B9A',
                       linewidth=2.5)
    ax.add_patch(inner)
    ax.text(7, 5.5, 'AI &', fontsize=10, fontweight='bold', ha='center', color='#6A1B9A')
    ax.text(7, 5.0, 'Technology', fontsize=10, fontweight='bold', ha='center', color='#6A1B9A')
    ax.text(7, 4.5, 'Core', fontsize=9, ha='center', color='#6A1B9A')
    
    # Stakeholders around the outer ring
    stakeholders = [
        (2.5, 8.5, 'Suppliers &\nManufacturers'),
        (11.5, 8.5, 'Logistics\nPartners'),
        (2.0, 2.0, 'Frontline\nWorkers'),
        (12.0, 2.0, 'End\nCustomers'),
    ]
    
    for x, y, text in stakeholders:
        box = FancyBboxPatch((x-1.0, y-0.4), 2.0, 0.8, boxstyle="round,pad=0.05",
                            facecolor='white', edgecolor='#2E7D32', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=8.5, ha='center', va='center', fontweight='bold')
    
    # Design Thinking elements in middle ring
    dt_elements = [
        (4.8, 6.8, 'Empathy\nInterviews'),
        (9.2, 6.8, 'Problem\nReframing'),
        (4.5, 3.6, 'Rapid\nPrototyping'),
        (9.5, 3.6, 'Iterative\nTesting'),
    ]
    
    for x, y, text in dt_elements:
        box = FancyBboxPatch((x-0.8, y-0.35), 1.6, 0.7, boxstyle="round,pad=0.03",
                            facecolor='white', edgecolor='#1565C0', linewidth=1.2)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=8, ha='center', va='center', color='#1565C0')
    
    # Right side panel: AI Adoption Framework
    ax.plot([13.2, 13.2], [1.0, 8.5], 'k-', lw=0.5, alpha=0.3)
    
    # Bottom section - Risk Assessment
    ax.text(7, 1.0, 'Empathy-Driven Risk Assessment: Surfacing vulnerabilities that quantitative models miss',
            fontsize=9, ha='center', style='italic', color='#555')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_3_Supply_Chain_Resilience.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 3 saved successfully.")


def figure4_culture_excellence():
    """
    Figure 4: Building a Culture of Human-Centered Operational Excellence (KANO Model Integration)
    """
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.3)
    
    # Panel A: KANO Model
    ax1 = fig.add_subplot(gs[0, 0])
    
    # KANO model curves
    x = np.linspace(-3, 3, 100)
    
    # Delighters (exponential upper)
    y_delight = 0.3 * np.exp(0.5 * x) - 0.5
    # Basic needs (lower curve)
    y_basic = 1.5 * (1 / (1 + np.exp(-2*x))) - 1.2
    # Performance (linear)
    y_perf = 0.5 * x
    
    ax1.plot(x, y_delight, 'g-', lw=2.5, label='Delighters (Excitement)')
    ax1.plot(x, y_perf, 'b-', lw=2.5, label='Performance (One-dimensional)')
    ax1.plot(x, y_basic, 'r-', lw=2.5, label='Basic Needs (Must-be)')
    
    ax1.axhline(y=0, color='k', lw=0.8, alpha=0.5)
    ax1.axvline(x=0, color='k', lw=0.8, alpha=0.5)
    ax1.set_xlabel('Degree of Achievement →', fontsize=9)
    ax1.set_ylabel('← Dissatisfaction | Satisfaction →', fontsize=9)
    ax1.set_title('(A) KANO Model for Operational Excellence', fontsize=11, fontweight='bold')
    ax1.legend(fontsize=8, loc='lower right')
    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-2, 3)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # Panel B: Culture Transformation Stages
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 8)
    ax2.axis('off')
    ax2.set_title('(B) Culture Transformation Journey', fontsize=11, fontweight='bold')
    
    # Staircase of transformation
    stairs = [
        (1.5, 1.5, 'Foundation:\nAlign Mission\n& Values', '#BBDEFB'),
        (3.5, 3.0, 'Process:\nRedesign with\nEmpathy', '#C8E6C9'),
        (5.5, 4.5, 'Training:\nDeploy DT\nCapabilities', '#FFE0B2'),
        (7.5, 6.0, 'Sustain:\nContinuous\nImprovement', '#E1BEE7'),
    ]
    
    for x, y, text, color in stairs:
        box = FancyBboxPatch((x-0.9, y-0.7), 1.8, 1.4, boxstyle="round,pad=0.05",
                            facecolor=color, edgecolor='#555', linewidth=1.2)
        ax2.add_patch(box)
        ax2.text(x, y, text, fontsize=8, ha='center', va='center', fontweight='bold')
    
    # Arrows connecting stairs
    for i in range(3):
        ax2.annotate('', xy=(stairs[i+1][0]-0.9, stairs[i+1][1]-0.3),
                    xytext=(stairs[i][0]+0.9, stairs[i][1]+0.3),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color='#555'))
    
    # Panel C: Quality Prevention vs Correction
    ax3 = fig.add_subplot(gs[1, 0])
    
    categories = ['Planning\n(Cheap Time)', 'Design\nPhase', 'Implementation', 'Post-Launch\n(Expensive Time)']
    prevention_costs = [10, 20, 35, 15]
    correction_costs = [5, 10, 25, 60]
    
    x_pos = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax3.bar(x_pos - width/2, prevention_costs, width, label='Prevention (QA)', 
                    color='#4CAF50', edgecolor='white')
    bars2 = ax3.bar(x_pos + width/2, correction_costs, width, label='Correction (QC)',
                    color='#F44336', edgecolor='white')
    
    ax3.set_xlabel('Project Phase', fontsize=9)
    ax3.set_ylabel('Relative Cost (%)', fontsize=9)
    ax3.set_title('(C) Quality Assurance vs. Quality Control Costs', fontsize=11, fontweight='bold')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(categories, fontsize=8)
    ax3.legend(fontsize=8)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    
    # Panel D: Continuous Improvement Loop
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_xlim(0, 10)
    ax4.set_ylim(0, 8)
    ax4.axis('off')
    ax4.set_title('(D) Continuous Improvement Loop (Plus/Delta)', fontsize=11, fontweight='bold')
    
    # Circular loop
    theta = np.linspace(0, 2*np.pi, 100)
    r = 2.5
    cx, cy = 5, 4
    
    ax4.plot(cx + r*np.cos(theta), cy + r*np.sin(theta), 'b-', lw=2, alpha=0.3)
    
    loop_stages = [
        (cx + r*np.cos(np.pi/2), cy + r*np.sin(np.pi/2), 'Observe &\nEmpathize', '#E3F2FD'),
        (cx + r*np.cos(0), cy + r*np.sin(0), 'Analyze &\nDefine', '#E8F5E9'),
        (cx + r*np.cos(-np.pi/2), cy + r*np.sin(-np.pi/2), 'Implement\n& Test', '#FFF3E0'),
        (cx + r*np.cos(np.pi), cy + r*np.sin(np.pi), 'Reflect\n(Plus/Delta)', '#F3E5F5'),
    ]
    
    for x, y, text, color in loop_stages:
        box = FancyBboxPatch((x-0.8, y-0.45), 1.6, 0.9, boxstyle="round,pad=0.05",
                            facecolor=color, edgecolor='#333', linewidth=1.2)
        ax4.add_patch(box)
        ax4.text(x, y, text, fontsize=8, ha='center', va='center', fontweight='bold')
    
    # Arrows around the loop
    for i in range(4):
        angle_start = np.pi/2 - i*np.pi/2
        angle_end = np.pi/2 - (i+1)*np.pi/2
        mid_angle = (angle_start + angle_end) / 2
        ax4.annotate('', 
                    xy=(cx + (r-0.3)*np.cos(angle_end + 0.3), cy + (r-0.3)*np.sin(angle_end + 0.3)),
                    xytext=(cx + (r-0.3)*np.cos(angle_start - 0.3), cy + (r-0.3)*np.sin(angle_start - 0.3)),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color='#1565C0',
                                   connectionstyle='arc3,rad=0.3'))
    
    plt.savefig(f'{output_dir}/Figure_4_Culture_Excellence.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 4 saved successfully.")


# Generate all figures
if __name__ == '__main__':
    print("Generating Design Thinking Chapter figures...")
    figure1_design_thinking_operations()
    figure2_human_centered_process_mapping()
    figure3_supply_chain_resilience()
    figure4_culture_excellence()
    print(f"\nAll figures saved to '{output_dir}/' directory.")
    for f in sorted(os.listdir(output_dir)):
        filepath = os.path.join(output_dir, f)
        size_kb = os.path.getsize(filepath) / 1024
        print(f"  - {f} ({size_kb:.1f} KB)")
