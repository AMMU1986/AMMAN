"""
Generate high-quality figures for the Industry 5.0 chapter:
'Evidences from Advanced and Emerging Economies: A Qualitative Comparative Analysis'

Figures:
1. Configurational Framework - Five causal conditions and equifinal pathways
2. Firm-Level Outcomes Comparison (Advanced vs Emerging Economies)
3. Fuzzy-Set Membership Radar Charts for Six Economies
4. Comparative Matrix - Technology, Policy, Workforce, Scalability
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np
import seaborn as sns
import os

# Set publication-quality defaults
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Color palette
COLORS = {
    'advanced': '#2C5F8A',      # Deep blue for advanced economies
    'emerging': '#D4763A',      # Warm orange for emerging economies
    'highlight': '#4CAF50',     # Green for positive outcomes
    'warning': '#E74C3C',       # Red for challenges
    'neutral': '#7F8C8D',       # Gray for neutral
    'germany': '#1B4F72',
    'japan': '#6C3483',
    'usa': '#1E8449',
    'india': '#D35400',
    'brazil': '#C0392B',
    'sea': '#2980B9',
    'bg_light': '#F8F9FA',
}

output_dir = 'industry5_figures'
os.makedirs(output_dir, exist_ok=True)


def figure1_configurational_framework():
    """
    Figure 1: Configurational Framework for Industry 5.0 Adoption
    Shows five causal conditions, their configurational interactions,
    and equifinal pathways across advanced and emerging economies.
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_facecolor('#FAFBFC')

    # Title
    ax.text(6, 8.7, 'Configurational Framework for Industry 5.0 Adoption',
            ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(6, 8.35, 'Five Causal Conditions and Equifinal Pathways',
            ha='center', va='center', fontsize=11, style='italic', color='#555555')

    # --- Five Causal Conditions (top row) ---
    conditions = [
        ('TECH', 'Technological\nInfrastructure', '#2C5F8A'),
        ('WORK', 'Workforce\nReadiness', '#27AE60'),
        ('POL', 'Policy\nEnvironment', '#8E44AD'),
        ('INNOV', 'Innovation\nCapacity', '#D35400'),
        ('SUST', 'Sustainability\nOrientation', '#16A085'),
    ]

    cond_y = 7.2
    cond_xs = [1.5, 3.5, 5.5, 7.5, 9.5]
    
    for i, (abbr, label, color) in enumerate(conditions):
        x = cond_xs[i]
        # Draw hexagon-like box
        box = FancyBboxPatch((x - 0.7, cond_y - 0.45), 1.4, 0.9,
                             boxstyle="round,pad=0.05", facecolor=color,
                             edgecolor='white', linewidth=1.5, alpha=0.9)
        ax.add_patch(box)
        ax.text(x, cond_y + 0.05, abbr, ha='center', va='center',
                fontsize=9, fontweight='bold', color='white')
        ax.text(x, cond_y - 0.55, label, ha='center', va='top',
                fontsize=8, color='#333333')

    # --- Configurational Logic Box ---
    logic_y = 5.5
    logic_box = FancyBboxPatch((2.5, logic_y - 0.5), 7, 1.0,
                               boxstyle="round,pad=0.1", facecolor='#ECF0F1',
                               edgecolor='#BDC3C7', linewidth=1.5)
    ax.add_patch(logic_box)
    ax.text(6, logic_y + 0.15, 'CONFIGURATIONAL LOGIC', ha='center', va='center',
            fontsize=10, fontweight='bold', color='#2C3E50')
    ax.text(6, logic_y - 0.2, 'Conjunctural Causation  |  Equifinality  |  Asymmetric Causation',
            ha='center', va='center', fontsize=8.5, color='#555555')

    # Arrows from conditions to logic box
    for x in cond_xs:
        ax.annotate('', xy=(x, logic_y + 0.5), xytext=(x, cond_y - 0.9),
                    arrowprops=dict(arrowstyle='->', color='#7F8C8D', lw=1.2))

    # --- Three Equifinal Pathways (bottom section) ---
    pathway_y = 3.2
    pathways = [
        ('PATH 1', 'Advanced Economy\nPathway', 'TECH * INNOV * WORK',
         'Germany, Japan, USA', COLORS['advanced']),
        ('PATH 2', 'Policy-Innovation\nPathway', 'POL * INNOV * ~TECH',
         'India', COLORS['emerging']),
        ('PATH 3', 'Workforce-Policy\nPathway', 'WORK * POL * ~TECH * ~INNOV',
         'Southeast Asia', '#2980B9'),
    ]

    path_xs = [2.5, 6.0, 9.5]
    
    for i, (path_id, title, formula, cases, color) in enumerate(pathways):
        x = path_xs[i]
        # Pathway box
        box = FancyBboxPatch((x - 1.3, pathway_y - 0.9), 2.6, 1.8,
                             boxstyle="round,pad=0.08", facecolor='white',
                             edgecolor=color, linewidth=2.0)
        ax.add_patch(box)
        ax.text(x, pathway_y + 0.55, path_id, ha='center', va='center',
                fontsize=9, fontweight='bold', color=color)
        ax.text(x, pathway_y + 0.15, title, ha='center', va='center',
                fontsize=8.5, color='#333333')
        ax.text(x, pathway_y - 0.25, formula, ha='center', va='center',
                fontsize=7.5, fontfamily='monospace', color='#555555')
        ax.text(x, pathway_y - 0.6, cases, ha='center', va='center',
                fontsize=7.5, style='italic', color='#777777')

    # Arrows from logic to pathways
    for x in path_xs:
        ax.annotate('', xy=(x, pathway_y + 0.9), xytext=(6, logic_y - 0.5),
                    arrowprops=dict(arrowstyle='->', color='#7F8C8D', lw=1.0,
                                    connectionstyle='arc3,rad=0.0'))

    # --- Outcome Box ---
    outcome_y = 1.3
    outcome_box = FancyBboxPatch((3.5, outcome_y - 0.5), 5.0, 1.0,
                                  boxstyle="round,pad=0.1", facecolor=COLORS['highlight'],
                                  edgecolor='#27AE60', linewidth=2.0, alpha=0.15)
    ax.add_patch(outcome_box)
    ax.text(6, outcome_y + 0.15, 'INDUSTRY 5.0 SUCCESS', ha='center', va='center',
            fontsize=11, fontweight='bold', color='#1E8449')
    ax.text(6, outcome_y - 0.2, 'Human-Centric  •  Sustainable  •  Resilient',
            ha='center', va='center', fontsize=9, color='#27AE60')

    # Arrows from pathways to outcome
    for x in path_xs:
        ax.annotate('', xy=(6, outcome_y + 0.5), xytext=(x, pathway_y - 0.9),
                    arrowprops=dict(arrowstyle='->', color='#27AE60', lw=1.2,
                                    connectionstyle='arc3,rad=0.0'))

    # Equifinality annotation
    ax.text(11, 2.2, 'EQUIFINALITY:\nMultiple pathways\n→ same outcome',
            ha='center', va='center', fontsize=8, style='italic',
            color='#7F8C8D',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#F5F5F5', edgecolor='#CCCCCC'))

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_1_Configurational_Framework.png',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✓ Figure 1: Configurational Framework generated")


def figure2_firm_outcomes():
    """
    Figure 2: Firm-Level Outcomes Comparison
    Bar chart comparing productivity gains, injury reduction, and waste reduction
    across configurations.
    """
    fig, axes = plt.subplots(1, 3, figsize=(13, 5))

    categories = ['TECH+INNOV+WORK\n(Advanced, N=18)',
                  'POL+INNOV\n(India, N=7)',
                  'WORK+POL\n(SE Asia, N=6)',
                  'Partial Config.\n(Brazil, N=5)']
    
    colors = [COLORS['advanced'], COLORS['emerging'], COLORS['sea'], COLORS['neutral']]

    # Data
    productivity = [22.4, 14.8, 11.2, 6.4]
    prod_err = [6.8, 5.2, 4.8, 3.1]
    
    safety = [38.2, 25.3, 19.7, 10.2]
    safety_err = [9.4, 8.7, 7.1, 5.4]
    
    # Scalability (1-5 scale) and cost data for third panel
    scalability = [3.2, 3.8, 4.2, 2.5]
    cost_mid = [85, 23.5, 11.5, 32.5]  # thousands USD midpoint

    # Panel 1: Productivity Gains
    ax = axes[0]
    bars = ax.bar(range(4), productivity, yerr=prod_err, capsize=4,
                  color=colors, edgecolor='white', linewidth=0.8, alpha=0.85)
    ax.set_xticks(range(4))
    ax.set_xticklabels(categories, fontsize=8)
    ax.set_ylabel('Mean Productivity Gain (%)')
    ax.set_title('(a) Productivity Gains from HRC', fontweight='bold', fontsize=10)
    ax.set_ylim(0, 35)
    ax.axhline(y=0, color='black', linewidth=0.5)
    # Add value labels
    for i, (v, e) in enumerate(zip(productivity, prod_err)):
        ax.text(i, v + e + 0.8, f'{v}%', ha='center', va='bottom', fontsize=8, fontweight='bold')

    # Panel 2: Safety Improvement
    ax = axes[1]
    bars = ax.bar(range(4), safety, yerr=safety_err, capsize=4,
                  color=colors, edgecolor='white', linewidth=0.8, alpha=0.85)
    ax.set_xticks(range(4))
    ax.set_xticklabels(categories, fontsize=8)
    ax.set_ylabel('Mean Safety Improvement (%)')
    ax.set_title('(b) Injury/Safety Improvement', fontweight='bold', fontsize=10)
    ax.set_ylim(0, 55)
    ax.axhline(y=0, color='black', linewidth=0.5)
    for i, (v, e) in enumerate(zip(safety, safety_err)):
        ax.text(i, v + e + 0.8, f'{v}%', ha='center', va='bottom', fontsize=8, fontweight='bold')

    # Panel 3: Cost-Scalability Trade-off (scatter)
    ax = axes[2]
    scatter_sizes = [180, 70, 60, 50]  # proportional to N
    for i in range(4):
        ax.scatter(cost_mid[i], scalability[i], s=scatter_sizes[i],
                   c=colors[i], edgecolor='white', linewidth=1.5, zorder=3, alpha=0.85)
        ax.annotate(categories[i].split('\n')[0], (cost_mid[i], scalability[i]),
                    textcoords="offset points", xytext=(10, 5), fontsize=7.5)
    ax.set_xlabel('Implementation Cost (USD thousands, midpoint)')
    ax.set_ylabel('Scalability Score (1-5)')
    ax.set_title('(c) Cost vs. Scalability', fontweight='bold', fontsize=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(1.5, 5)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=3.5, color='#27AE60', linestyle='--', alpha=0.4, linewidth=1)
    ax.axvline(x=40, color='#E74C3C', linestyle='--', alpha=0.4, linewidth=1)
    ax.text(20, 4.8, 'Low-cost &\nHigh-scalability', fontsize=7, ha='center',
            color='#27AE60', alpha=0.7)
    ax.text(75, 2.0, 'High-cost &\nLow-scalability', fontsize=7, ha='center',
            color='#E74C3C', alpha=0.7)

    plt.suptitle('Figure 2: Firm-Level Industry 5.0 Outcomes by Configurational Pathway',
                 fontsize=12, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_2_Firm_Level_Outcomes.png',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✓ Figure 2: Firm-Level Outcomes generated")


def figure3_radar_charts():
    """
    Figure 3: Fuzzy-Set Membership Radar Charts for Six Economies
    Shows the calibrated scores across five conditions for each economy.
    """
    # Data from Table 3
    categories = ['TECH', 'WORK', 'POL', 'INNOV', 'SUST']
    
    economies = {
        'Germany': [0.92, 0.85, 0.90, 0.88, 0.87],
        'Japan': [0.95, 0.78, 0.82, 0.85, 0.72],
        'United States': [0.88, 0.80, 0.70, 0.95, 0.60],
        'India': [0.30, 0.45, 0.55, 0.50, 0.35],
        'Brazil': [0.35, 0.40, 0.45, 0.40, 0.50],
        'Southeast Asia': [0.40, 0.50, 0.50, 0.45, 0.40],
    }
    
    economy_colors = [COLORS['germany'], COLORS['japan'], COLORS['usa'],
                      COLORS['india'], COLORS['brazil'], COLORS['sea']]

    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # close the polygon

    fig, axes = plt.subplots(2, 3, figsize=(13, 9), subplot_kw=dict(polar=True))
    axes_flat = axes.flatten()

    for idx, (economy, values) in enumerate(economies.items()):
        ax = axes_flat[idx]
        values_closed = values + values[:1]
        
        # Plot
        ax.plot(angles, values_closed, 'o-', linewidth=2.0,
                color=economy_colors[idx], markersize=5)
        ax.fill(angles, values_closed, alpha=0.2, color=economy_colors[idx])
        
        # Crossover line at 0.5
        crossover = [0.5] * (N + 1)
        ax.plot(angles, crossover, '--', linewidth=1.0, color='#E74C3C', alpha=0.5)
        
        # Labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=9)
        ax.set_ylim(0, 1.0)
        ax.set_yticks([0.25, 0.50, 0.75, 1.0])
        ax.set_yticklabels(['0.25', '0.50', '0.75', '1.0'], fontsize=7, color='gray')
        ax.set_title(economy, fontsize=11, fontweight='bold', pad=15,
                     color=economy_colors[idx])
        
        # Add score annotations
        for i, (angle, value) in enumerate(zip(angles[:-1], values)):
            ax.annotate(f'{value:.2f}', xy=(angle, value),
                       textcoords="offset points", xytext=(5, 5),
                       fontsize=7, color='#555555')

    plt.suptitle('Figure 3: Fuzzy-Set Membership Scores Across Five Causal Conditions\n'
                 '(Red dashed line = 0.5 crossover threshold)',
                 fontsize=12, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_3_Radar_FuzzySet_Scores.png',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✓ Figure 3: Radar Charts generated")


def figure4_comparative_matrix():
    """
    Figure 4: Comparative Matrix - Technology, Policy, Workforce, Scalability
    Heatmap-style comparison across dimensions for all six economies.
    """
    fig, ax = plt.subplots(1, 1, figsize=(11, 7))

    # Dimensions and economies
    dimensions = ['Technological\nInfrastructure', 'Workforce\nReadiness',
                  'Policy\nEnvironment', 'Innovation\nCapacity',
                  'Sustainability\nOrientation', 'Industry 5.0\nOutcome']
    economies = ['Germany', 'Japan', 'United States', 'India', 'Brazil', 'SE Asia']

    # Data matrix (rows = economies, cols = dimensions)
    data = np.array([
        [0.92, 0.85, 0.90, 0.88, 0.87, 0.90],  # Germany
        [0.95, 0.78, 0.82, 0.85, 0.72, 0.85],  # Japan
        [0.88, 0.80, 0.70, 0.95, 0.60, 0.82],  # USA
        [0.30, 0.45, 0.55, 0.50, 0.35, 0.55],  # India
        [0.35, 0.40, 0.45, 0.40, 0.50, 0.48],  # Brazil
        [0.40, 0.50, 0.50, 0.45, 0.40, 0.52],  # SE Asia
    ])

    # Custom colormap: diverging from red (low) to blue (high) with white at 0.5
    cmap = sns.diverging_palette(10, 220, as_cmap=True)

    # Plot heatmap
    im = ax.imshow(data, cmap=cmap, aspect='auto', vmin=0, vmax=1)

    # Add text annotations
    for i in range(len(economies)):
        for j in range(len(dimensions)):
            val = data[i, j]
            text_color = 'white' if val > 0.75 or val < 0.25 else 'black'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                    fontsize=10, fontweight='bold', color=text_color)

    # Axis configuration
    ax.set_xticks(range(len(dimensions)))
    ax.set_xticklabels(dimensions, fontsize=10, ha='center')
    ax.set_yticks(range(len(economies)))
    ax.set_yticklabels(economies, fontsize=10)
    
    # Add dividing line between advanced and emerging
    ax.axhline(y=2.5, color='white', linewidth=3)
    ax.text(-0.8, 1, 'ADVANCED', rotation=90, va='center', ha='center',
            fontsize=9, fontweight='bold', color=COLORS['advanced'])
    ax.text(-0.8, 4, 'EMERGING', rotation=90, va='center', ha='center',
            fontsize=9, fontweight='bold', color=COLORS['emerging'])

    # Crossover threshold indicator
    cbar = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label('Fuzzy-Set Membership Score', fontsize=10)
    cbar.ax.axhline(y=0.5, color='red', linewidth=1.5, linestyle='--')
    cbar.ax.text(1.5, 0.5, '← Crossover\n    (0.50)', fontsize=7,
                 color='red', va='center', transform=cbar.ax.get_yaxis_transform())

    # Add pathway annotations on the right
    ax.text(6.3, 0.5, 'Path 1:\nTECH*INNOV*WORK',
            fontsize=8, ha='left', va='center', color=COLORS['advanced'],
            fontfamily='monospace', style='italic')
    ax.text(6.3, 3.0, 'Path 2: POL*INNOV',
            fontsize=8, ha='left', va='center', color=COLORS['india'],
            fontfamily='monospace', style='italic')
    ax.text(6.3, 4.5, 'Path 3: WORK*POL',
            fontsize=8, ha='left', va='center', color=COLORS['sea'],
            fontfamily='monospace', style='italic')

    ax.set_title('Figure 4: Comparative Matrix—Divergent Pathways to Industry 5.0 Outcomes\n'
                 'Fuzzy-Set Scores Across Five Conditions and Outcome',
                 fontsize=12, fontweight='bold', pad=15)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_4_Comparative_Matrix.png',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✓ Figure 4: Comparative Matrix generated")


if __name__ == '__main__':
    print("Generating figures for Industry 5.0 chapter...")
    print("=" * 55)
    figure1_configurational_framework()
    figure2_firm_outcomes()
    figure3_radar_charts()
    figure4_comparative_matrix()
    print("=" * 55)
    print(f"All figures saved to '{output_dir}/' directory")
