"""
Generate 4 figures for Chapter 3: Comparative and Structural Bioinformatics of Enzymes
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# Create output directory
os.makedirs('/projects/sandbox/AMMAN/chapter3_figures', exist_ok=True)

# Set global style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.2

# ============================================================
# FIGURE 1: Workflow for Comparative Bioinformatics of Enzymes
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Figure 1: Integrated Workflow for Comparative Bioinformatics\nAnalysis of Enzyme Targets', 
             fontsize=13, fontweight='bold', pad=20)

# Define workflow boxes
boxes = [
    (1, 8.5, 'Sequence Retrieval\n& Curation', '#4CAF50'),
    (4.5, 8.5, 'Multiple Sequence\nAlignment (MSA)', '#2196F3'),
    (8, 8.5, 'Phylogenetic\nAnalysis', '#9C27B0'),
    (1, 6.0, 'Conserved Motif\nIdentification', '#FF9800'),
    (4.5, 6.0, 'Homology\nModelling', '#E91E63'),
    (8, 6.0, 'Structure\nPrediction', '#00BCD4'),
    (1, 3.5, 'Structural\nAlignment', '#795548'),
    (4.5, 3.5, 'Active-Site\nMapping', '#607D8B'),
    (8, 3.5, 'Binding-Pocket\nAnalysis', '#FF5722'),
    (2.75, 1.2, 'Molecular Docking &\nInteraction Profiling', '#3F51B5'),
    (6.25, 1.2, 'MD Simulations &\nDrug Target Selection', '#009688'),
]

for (x, y, label, color) in boxes:
    rect = FancyBboxPatch((x, y), 2.8, 1.3, boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor='black', alpha=0.8, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + 1.4, y + 0.65, label, ha='center', va='center',
            fontsize=9, fontweight='bold', color='white')

# Add arrows between rows
arrow_style = "Simple,tail_width=0.5,head_width=6,head_length=4"
for i in range(3):
    # Row 1 to Row 2
    ax.annotate('', xy=(boxes[i+3][0]+1.4, boxes[i+3][1]+1.3), 
                xytext=(boxes[i][0]+1.4, boxes[i][1]),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
    # Row 2 to Row 3
    ax.annotate('', xy=(boxes[i+6][0]+1.4, boxes[i+6][1]+1.3), 
                xytext=(boxes[i+3][0]+1.4, boxes[i+3][1]),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))

# Row 3 to Row 4
ax.annotate('', xy=(boxes[9][0]+1.4, boxes[9][1]+1.3), 
            xytext=(boxes[6][0]+1.4, boxes[6][1]),
            arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
ax.annotate('', xy=(boxes[10][0]+1.4, boxes[10][1]+1.3), 
            xytext=(boxes[8][0]+1.4, boxes[8][1]),
            arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))

# Horizontal arrows
for i in range(2):
    ax.annotate('', xy=(boxes[i+1][0], boxes[i+1][1]+0.65), 
                xytext=(boxes[i][0]+2.8, boxes[i][1]+0.65),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
    ax.annotate('', xy=(boxes[i+4][0], boxes[i+4][1]+0.65), 
                xytext=(boxes[i+3][0]+2.8, boxes[i+3][1]+0.65),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
    ax.annotate('', xy=(boxes[i+7][0], boxes[i+7][1]+0.65), 
                xytext=(boxes[i+6][0]+2.8, boxes[i+6][1]+0.65),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/chapter3_figures/Figure_1_Comparative_Bioinformatics_Workflow.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# FIGURE 2: Structural Bioinformatics Pipeline
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Figure 2: Structural Bioinformatics Analysis of Enzyme Targets', 
             fontsize=13, fontweight='bold')

# Panel A: Homology Modelling Quality Assessment
ax = axes[0, 0]
models = ['Template\nIdentification', 'Alignment\nBuilding', 'Model\nConstruction', 'Loop\nModelling', 'Energy\nMinimization', 'Validation']
quality_scores = [0.95, 0.88, 0.82, 0.75, 0.90, 0.92]
colors = ['#4CAF50', '#8BC34A', '#CDDC39', '#FFC107', '#4CAF50', '#4CAF50']
bars = ax.bar(range(len(models)), quality_scores, color=colors, edgecolor='black', linewidth=0.8)
ax.set_xticks(range(len(models)))
ax.set_xticklabels(models, fontsize=8)
ax.set_ylabel('Quality Score', fontsize=10)
ax.set_title('A) Homology Modelling Pipeline Scores', fontsize=10, fontweight='bold')
ax.set_ylim(0, 1.1)
ax.axhline(y=0.8, color='red', linestyle='--', alpha=0.7, label='Threshold')
ax.legend(fontsize=8)

# Panel B: RMSD comparison of structural alignments
ax = axes[0, 1]
enzymes = ['DHFR', 'HIV-PR', 'CDK2', 'COX-2', 'ACE', 'PTP1B', 'EGFR', 'Neuraminidase']
rmsd_values = [0.45, 0.78, 1.12, 0.95, 1.35, 0.62, 0.89, 0.55]
colors_rmsd = ['#2196F3' if r < 1.0 else '#FF5722' for r in rmsd_values]
ax.barh(range(len(enzymes)), rmsd_values, color=colors_rmsd, edgecolor='black', linewidth=0.8)
ax.set_yticks(range(len(enzymes)))
ax.set_yticklabels(enzymes, fontsize=9)
ax.set_xlabel('RMSD (Å)', fontsize=10)
ax.set_title('B) Structural Alignment RMSD Values', fontsize=10, fontweight='bold')
ax.axvline(x=1.0, color='red', linestyle='--', alpha=0.7, label='1.0 Å cutoff')
ax.legend(fontsize=8)

# Panel C: Druggability scores of binding pockets
ax = axes[1, 0]
pockets = ['Pocket 1\n(Active Site)', 'Pocket 2\n(Allosteric)', 'Pocket 3\n(Interface)', 
           'Pocket 4\n(Cryptic)', 'Pocket 5\n(Surface)']
druggability = [0.92, 0.78, 0.65, 0.45, 0.22]
volume = [450, 320, 280, 180, 120]
scatter = ax.scatter(volume, druggability, s=[d*300 for d in druggability], 
                     c=druggability, cmap='RdYlGn', edgecolors='black', linewidth=1.2,
                     vmin=0, vmax=1)
for i, txt in enumerate(pockets):
    ax.annotate(txt, (volume[i], druggability[i]), fontsize=7, ha='center', 
                va='bottom', xytext=(0, 10), textcoords='offset points')
ax.set_xlabel('Pocket Volume (Å³)', fontsize=10)
ax.set_ylabel('Druggability Score', fontsize=10)
ax.set_title('C) Binding-Pocket Druggability Analysis', fontsize=10, fontweight='bold')
plt.colorbar(scatter, ax=ax, label='Druggability')

# Panel D: B-factor / flexibility profile
ax = axes[1, 1]
residues = np.arange(1, 201)
np.random.seed(42)
bfactor = 20 + 10*np.sin(residues/20) + np.random.normal(0, 3, 200)
# Mark active site residues
active_site = [45, 46, 47, 95, 96, 97, 145, 146, 147]
ax.plot(residues, bfactor, color='#2196F3', linewidth=0.8, alpha=0.8)
ax.fill_between(residues, bfactor, alpha=0.3, color='#2196F3')
for res in active_site:
    ax.axvline(x=res, color='red', alpha=0.3, linewidth=2)
ax.set_xlabel('Residue Number', fontsize=10)
ax.set_ylabel('B-factor (Å²)', fontsize=10)
ax.set_title('D) Flexibility Profile with Active-Site Residues', fontsize=10, fontweight='bold')
ax.legend(['B-factor', 'Active site'], fontsize=8)

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/chapter3_figures/Figure_2_Structural_Bioinformatics_Pipeline.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# FIGURE 3: Enzyme-Ligand Interaction Analysis
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Figure 3: Integrative Analysis of Enzyme–Ligand Interactions', 
             fontsize=13, fontweight='bold')

# Panel A: Docking scores comparison
ax = axes[0, 0]
compounds = ['Compound A', 'Compound B', 'Compound C', 'Compound D', 'Compound E',
             'Compound F', 'Compound G', 'Compound H']
dock_scores = [-9.8, -8.5, -7.9, -10.2, -6.8, -8.1, -9.3, -7.2]
colors_dock = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(compounds)))
ax.barh(range(len(compounds)), dock_scores, color=colors_dock, edgecolor='black', linewidth=0.8)
ax.set_yticks(range(len(compounds)))
ax.set_yticklabels(compounds, fontsize=9)
ax.set_xlabel('Docking Score (kcal/mol)', fontsize=10)
ax.set_title('A) Molecular Docking Scores', fontsize=10, fontweight='bold')
ax.axvline(x=-8.0, color='blue', linestyle='--', alpha=0.7, label='Threshold (-8.0)')
ax.legend(fontsize=8)

# Panel B: Interaction types distribution
ax = axes[0, 1]
interaction_types = ['H-bonds', 'Hydrophobic', 'π-π Stacking', 'Salt Bridge', 
                     'Van der Waals', 'Cation-π']
counts = [12, 8, 5, 3, 15, 2]
colors_int = ['#E91E63', '#9C27B0', '#3F51B5', '#009688', '#FF9800', '#795548']
wedges, texts, autotexts = ax.pie(counts, labels=interaction_types, colors=colors_int,
                                   autopct='%1.1f%%', startangle=90, 
                                   textprops={'fontsize': 8})
ax.set_title('B) Distribution of Interaction Types', fontsize=10, fontweight='bold')

# Panel C: MD simulation RMSD over time
ax = axes[1, 0]
time = np.linspace(0, 100, 1000)
np.random.seed(123)
rmsd_apo = 1.2 + 0.3*np.log(time+1) + np.random.normal(0, 0.1, 1000)
rmsd_holo = 0.8 + 0.15*np.log(time+1) + np.random.normal(0, 0.08, 1000)
ax.plot(time, rmsd_apo, color='#F44336', alpha=0.8, linewidth=1, label='Apo (unbound)')
ax.plot(time, rmsd_holo, color='#4CAF50', alpha=0.8, linewidth=1, label='Holo (ligand-bound)')
ax.set_xlabel('Time (ns)', fontsize=10)
ax.set_ylabel('RMSD (Å)', fontsize=10)
ax.set_title('C) MD Simulation RMSD Trajectories', fontsize=10, fontweight='bold')
ax.legend(fontsize=9)
ax.set_ylim(0, 3.5)

# Panel D: Binding free energy decomposition
ax = axes[1, 1]
energy_components = ['ΔG_vdW', 'ΔG_elec', 'ΔG_polar\nsolv', 'ΔG_nonpolar\nsolv', 'ΔG_total']
values = [-35.2, -18.5, 28.3, -4.8, -30.2]
colors_energy = ['#4CAF50' if v < 0 else '#F44336' for v in values]
ax.bar(range(len(energy_components)), values, color=colors_energy, edgecolor='black', linewidth=0.8)
ax.set_xticks(range(len(energy_components)))
ax.set_xticklabels(energy_components, fontsize=9)
ax.set_ylabel('Energy (kcal/mol)', fontsize=10)
ax.set_title('D) MM-PBSA Binding Free Energy\nDecomposition', fontsize=10, fontweight='bold')
ax.axhline(y=0, color='black', linewidth=0.8)

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/chapter3_figures/Figure_3_Enzyme_Ligand_Interactions.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# FIGURE 4: Bioinformatics-Guided Drug Design Framework
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(13, 9))
ax.set_xlim(0, 13)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Figure 4: Bioinformatics-Guided Enzyme Targeting Framework\nfor Drug Discovery', 
             fontsize=13, fontweight='bold', pad=20)

# Central pipeline stages
stages = [
    (1.5, 8.0, 'Target\nIdentification', '#1565C0', 
     'Comparative genomics\nPathway analysis\nEssentiality prediction'),
    (5.0, 8.0, 'Target\nValidation', '#2E7D32',
     'Conservation analysis\nDruggability assessment\nSelectivity profiling'),
    (8.5, 8.0, 'Hit\nDiscovery', '#E65100',
     'Virtual screening\nPharmacophore modelling\nFragment-based design'),
    (1.5, 4.5, 'Lead\nOptimization', '#6A1B9A',
     'SAR analysis\nADMET prediction\nBinding mode analysis'),
    (5.0, 4.5, 'Preclinical\nAssessment', '#C62828',
     'Selectivity validation\nOff-target prediction\nToxicity profiling'),
    (8.5, 4.5, 'Experimental\nValidation', '#00695C',
     'In vitro assays\nX-ray crystallography\nSPR binding studies'),
]

for (x, y, title, color, desc) in stages:
    # Main box
    rect = FancyBboxPatch((x, y), 3.0, 2.0, boxstyle="round,pad=0.15",
                          facecolor=color, edgecolor='black', alpha=0.85, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + 1.5, y + 1.5, title, ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')
    ax.text(x + 1.5, y + 0.5, desc, ha='center', va='center',
            fontsize=7, color='white', style='italic')

# Arrows between stages (top row)
for i in range(2):
    ax.annotate('', xy=(stages[i+1][0], stages[i+1][1]+1.0), 
                xytext=(stages[i][0]+3.0, stages[i][1]+1.0),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))

# Arrows between stages (bottom row)
for i in range(2):
    ax.annotate('', xy=(stages[i+4][0], stages[i+4][1]+1.0), 
                xytext=(stages[i+3][0]+3.0, stages[i+3][1]+1.0),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))

# Arrows from top to bottom row
ax.annotate('', xy=(stages[3][0]+1.5, stages[3][1]+2.0), 
            xytext=(stages[0][0]+1.5, stages[0][1]),
            arrowprops=dict(arrowstyle='->', color='#333', lw=2, connectionstyle='arc3,rad=0'))
ax.annotate('', xy=(stages[5][0]+1.5, stages[5][1]+2.0), 
            xytext=(stages[2][0]+1.5, stages[2][1]),
            arrowprops=dict(arrowstyle='->', color='#333', lw=2, connectionstyle='arc3,rad=0'))

# Add feedback loop
ax.annotate('', xy=(stages[2][0]+3.0, stages[2][1]+0.5), 
            xytext=(stages[5][0]+3.0, stages[5][1]+1.5),
            arrowprops=dict(arrowstyle='->', color='#FF5722', lw=1.5, 
                          connectionstyle='arc3,rad=-0.3', linestyle='dashed'))
ax.text(12.0, 6.5, 'Feedback\nLoop', fontsize=8, color='#FF5722', 
        fontweight='bold', ha='center')

# Add bottom annotation
ax.text(6.5, 1.5, 'Bioinformatics Tools: BLAST, Clustal Omega, MEGA, MODELLER, AutoDock,\n'
        'GROMACS, SwissDock, PyMOL, VMD, Schrödinger Suite, MOE, Discovery Studio',
        ha='center', va='center', fontsize=9, style='italic',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='gray', alpha=0.8))

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/chapter3_figures/Figure_4_Drug_Design_Framework.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("All 4 figures generated successfully!")
print("Files saved in /projects/sandbox/AMMAN/chapter3_figures/")
for f in os.listdir('/projects/sandbox/AMMAN/chapter3_figures/'):
    print(f"  - {f}")
