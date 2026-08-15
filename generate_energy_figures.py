"""
Generate 4 figures for Chapter: AI-Based System Modeling and Simulation Techniques in Energy Systems
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs('/projects/sandbox/AMMAN/energy_figures', exist_ok=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11

# ============================================================
# Figure 1: Taxonomy of AI-Based Energy System Modeling Approaches
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(11, 7.5))
ax.set_xlim(0, 11)
ax.set_ylim(0, 8)
ax.axis('off')

ax.text(5.5, 7.5, 'Taxonomy of AI-Based Energy System Modeling Approaches', 
        ha='center', va='center', fontsize=14, fontweight='bold')

# Top-level box
rect_top = mpatches.FancyBboxPatch((3.5, 6.3), 4.0, 0.8,
                                    boxstyle="round,pad=0.1",
                                    facecolor='#1565C0', edgecolor='black', linewidth=1.5)
ax.add_patch(rect_top)
ax.text(5.5, 6.7, 'AI-Based Energy\nSystem Modeling', ha='center', va='center', 
        fontsize=11, fontweight='bold', color='white')

# Level 2 boxes
level2 = [
    (1.5, 4.8, 'Physics-Based\nModels', '#E53935'),
    (4.0, 4.8, 'Data-Driven\nModels', '#43A047'),
    (6.5, 4.8, 'Hybrid AI-Physics\nModels', '#FB8C00'),
    (9.0, 4.8, 'Optimization &\nControl', '#7B1FA2'),
]

for x, y, label, color in level2:
    rect = mpatches.FancyBboxPatch((x-0.9, y-0.4), 1.8, 0.8,
                                    boxstyle="round,pad=0.08",
                                    facecolor=color, edgecolor='black', linewidth=1.2, alpha=0.85)
    ax.add_patch(rect)
    ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    # Arrow from top
    ax.annotate('', xy=(x, y+0.4), xytext=(5.5, 6.3),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))

# Level 3 boxes
level3_data = [
    # Under Physics-Based
    [(1.5, 3.4, 'Thermodynamic\nModels'), (1.5, 2.4, 'Electrical Circuit\nModels')],
    # Under Data-Driven
    [(4.0, 3.4, 'ML: SVR, RF,\nGBM, XGBoost'), (4.0, 2.4, 'DL: ANN, CNN,\nLSTM, GRU')],
    # Under Hybrid
    [(6.5, 3.4, 'Physics-Informed\nNeural Networks'), (6.5, 2.4, 'Digital Twins &\nSurrogates')],
    # Under Optimization
    [(9.0, 3.4, 'RL & Multi-Agent\nOptimization'), (9.0, 2.4, 'Metaheuristic &\nEvolutionary')],
]

level2_colors = ['#FFCDD2', '#C8E6C9', '#FFE0B2', '#E1BEE7']
level2_edge = ['#E53935', '#43A047', '#FB8C00', '#7B1FA2']

for i, group in enumerate(level3_data):
    for x, y, label in group:
        rect = mpatches.FancyBboxPatch((x-0.85, y-0.35), 1.7, 0.7,
                                        boxstyle="round,pad=0.06",
                                        facecolor=level2_colors[i], edgecolor=level2_edge[i], linewidth=1)
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center', fontsize=7.5, color='#222')
        # Arrow from level2
        parent_y = 4.8
        ax.annotate('', xy=(x, y+0.35), xytext=(x, parent_y-0.4),
                    arrowprops=dict(arrowstyle='->', color=level2_edge[i], lw=1.2))

# Bottom bar
rect_bottom = mpatches.FancyBboxPatch((0.5, 0.8), 10.0, 0.8,
                                       boxstyle="round,pad=0.1",
                                       facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=2)
ax.add_patch(rect_bottom)
ax.text(5.5, 1.2, 'Applications: Load Forecasting • Renewable Prediction • Battery Modeling • Smart Grid • Energy Management',
        ha='center', va='center', fontsize=9, fontweight='bold', color='#0D47A1')

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/energy_figures/Figure_1_AI_Energy_Modeling_Taxonomy.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# Figure 2: Deep Learning Architectures for Energy Time-Series Forecasting
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(13, 5))

# Left panel: LSTM architecture schematic
ax = axes[0]
ax.set_xlim(0, 6)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_title('LSTM Network', fontweight='bold', fontsize=11)

# Input layer
for i in range(4):
    circle = plt.Circle((1, 1.5 + i*1.5), 0.3, color='#42A5F5', ec='black')
    ax.add_patch(circle)
    ax.text(1, 1.5 + i*1.5, f'x{i+1}', ha='center', va='center', fontsize=8, color='white')

# Hidden LSTM cells
for i in range(3):
    rect = mpatches.FancyBboxPatch((2.5, 2.0 + i*1.8), 1.2, 0.8,
                                    boxstyle="round,pad=0.05",
                                    facecolor='#66BB6A', edgecolor='black', linewidth=1)
    ax.add_patch(rect)
    ax.text(3.1, 2.4 + i*1.8, 'LSTM', ha='center', va='center', fontsize=8, fontweight='bold', color='white')

# Output
circle_out = plt.Circle((5, 4.5), 0.4, color='#EF5350', ec='black')
ax.add_patch(circle_out)
ax.text(5, 4.5, 'ŷ', ha='center', va='center', fontsize=10, color='white', fontweight='bold')

# Arrows
for i in range(4):
    ax.annotate('', xy=(2.5, 2.4 + min(i,2)*1.8), xytext=(1.3, 1.5 + i*1.5),
                arrowprops=dict(arrowstyle='->', color='#333', lw=0.8))
for i in range(3):
    ax.annotate('', xy=(4.6, 4.5), xytext=(3.7, 2.4 + i*1.8),
                arrowprops=dict(arrowstyle='->', color='#333', lw=0.8))

# Middle panel: CNN for spatial energy features
ax = axes[1]
ax.set_xlim(0, 6)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_title('CNN Architecture', fontweight='bold', fontsize=11)

layers = [
    (0.8, 'Input\nLayer', '#42A5F5', 3.5),
    (1.8, 'Conv1D\n+ReLU', '#FFA726', 3.0),
    (2.8, 'Conv1D\n+ReLU', '#FFA726', 2.5),
    (3.8, 'Pooling', '#AB47BC', 2.0),
    (4.8, 'Dense', '#66BB6A', 1.5),
    (5.5, 'Output', '#EF5350', 1.0),
]

for x, label, color, height in layers:
    rect = mpatches.FancyBboxPatch((x-0.3, 4-height/2), 0.6, height,
                                    boxstyle="round,pad=0.03",
                                    facecolor=color, edgecolor='black', linewidth=1, alpha=0.8)
    ax.add_patch(rect)
    ax.text(x, 4, label, ha='center', va='center', fontsize=7, color='white', fontweight='bold')

for i in range(len(layers)-1):
    ax.annotate('', xy=(layers[i+1][0]-0.3, 4), xytext=(layers[i][0]+0.3, 4),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1))

# Right panel: Transformer architecture
ax = axes[2]
ax.set_xlim(0, 6)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_title('Transformer Model', fontweight='bold', fontsize=11)

blocks = [
    (3, 1.5, 'Positional\nEncoding', '#42A5F5'),
    (3, 3.0, 'Multi-Head\nSelf-Attention', '#FF7043'),
    (3, 4.5, 'Feed-Forward\nNetwork', '#FFA726'),
    (3, 6.0, 'Layer Norm\n+ Residual', '#AB47BC'),
    (3, 7.2, 'Output\nProjection', '#EF5350'),
]

for x, y, label, color in blocks:
    rect = mpatches.FancyBboxPatch((x-1.0, y-0.45), 2.0, 0.9,
                                    boxstyle="round,pad=0.05",
                                    facecolor=color, edgecolor='black', linewidth=1, alpha=0.85)
    ax.add_patch(rect)
    ax.text(x, y, label, ha='center', va='center', fontsize=8, color='white', fontweight='bold')

for i in range(len(blocks)-1):
    ax.annotate('', xy=(3, blocks[i+1][1]-0.45), xytext=(3, blocks[i][1]+0.45),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.2))

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/energy_figures/Figure_2_Deep_Learning_Architectures.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# Figure 3: Performance Comparison of AI Models for Energy Forecasting
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))

# Left: Bar chart - RMSE comparison across methods
methods = ['Linear\nRegression', 'SVR', 'Random\nForest', 'ANN', 'LSTM', 'Transformer', 'Hybrid\nPINN']
rmse_values = [8.5, 6.2, 5.4, 4.1, 3.2, 2.8, 2.3]
colors_bar = ['#90A4AE', '#78909C', '#546E7A', '#42A5F5', '#26A69A', '#AB47BC', '#EF5350']

bars = axes[0].bar(methods, rmse_values, color=colors_bar, edgecolor='black', linewidth=0.8, width=0.65)
axes[0].set_ylabel('RMSE (MW)')
axes[0].set_title('Prediction Accuracy Comparison', fontweight='bold')
axes[0].set_ylim(0, 10)
axes[0].grid(axis='y', alpha=0.3)
for bar, val in zip(bars, rmse_values):
    axes[0].text(bar.get_x() + bar.get_width()/2, val + 0.2, f'{val}', 
                ha='center', va='bottom', fontsize=9, fontweight='bold')

# Right: Line chart - Training time vs accuracy trade-off
models_x = ['LR', 'SVR', 'RF', 'ANN', 'LSTM', 'Trans.', 'PINN']
accuracy = [78, 84, 87, 91, 94, 96, 97]
train_time = [0.1, 2, 5, 15, 45, 120, 180]

ax2 = axes[1]
color1 = '#1976D2'
color2 = '#E53935'

ln1 = ax2.plot(models_x, accuracy, 'o-', color=color1, linewidth=2, markersize=8, label='Accuracy (R²×100)')
ax2.set_ylabel('Accuracy (%)', color=color1)
ax2.set_ylim(70, 100)
ax2.tick_params(axis='y', labelcolor=color1)

ax2_twin = ax2.twinx()
ln2 = ax2_twin.plot(models_x, train_time, 's--', color=color2, linewidth=2, markersize=8, label='Training Time')
ax2_twin.set_ylabel('Training Time (min)', color=color2)
ax2_twin.set_ylim(0, 200)
ax2_twin.tick_params(axis='y', labelcolor=color2)

lines = ln1 + ln2
labels = [l.get_label() for l in lines]
ax2.legend(lines, labels, loc='center right')
ax2.set_title('Accuracy vs. Computational Cost', fontweight='bold')
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/energy_figures/Figure_3_Performance_Comparison.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# Figure 4: AI-Enabled Smart Grid and Energy Management Architecture
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(11, 7.5))
ax.set_xlim(0, 11)
ax.set_ylim(0, 8.5)
ax.axis('off')

ax.text(5.5, 8.1, 'AI-Enabled Smart Grid and Integrated Energy Management Architecture',
        ha='center', va='center', fontsize=13, fontweight='bold')

# Layer 1: Energy Sources (top)
sources = [
    (1.5, 7.0, 'Solar PV', '#FFA000'),
    (3.5, 7.0, 'Wind', '#0288D1'),
    (5.5, 7.0, 'Grid', '#455A64'),
    (7.5, 7.0, 'Battery\nStorage', '#7B1FA2'),
    (9.5, 7.0, 'EV\nCharging', '#2E7D32'),
]

for x, y, label, color in sources:
    rect = mpatches.FancyBboxPatch((x-0.7, y-0.35), 1.4, 0.7,
                                    boxstyle="round,pad=0.06",
                                    facecolor=color, edgecolor='black', linewidth=1.2, alpha=0.85)
    ax.add_patch(rect)
    ax.text(x, y, label, ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')

# Layer 2: Data & Communication
rect_data = mpatches.FancyBboxPatch((0.5, 5.3), 10.0, 0.7,
                                     boxstyle="round,pad=0.08",
                                     facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=1.5)
ax.add_patch(rect_data)
ax.text(5.5, 5.65, 'IoT Sensors • Smart Meters • SCADA • Communication Network • Data Lake',
        ha='center', va='center', fontsize=9, fontweight='bold', color='#0D47A1')

# Arrows from sources to data layer
for x, y, _, _ in sources:
    ax.annotate('', xy=(x, 5.95), xytext=(x, y-0.35),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1))

# Layer 3: AI Engine (center)
rect_ai = mpatches.FancyBboxPatch((1.5, 3.3), 8.0, 1.5,
                                   boxstyle="round,pad=0.1",
                                   facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=2)
ax.add_patch(rect_ai)
ax.text(5.5, 4.4, 'AI-Based Decision Engine', ha='center', va='center', 
        fontsize=11, fontweight='bold', color='#1B5E20')

ai_modules = [
    (2.8, 3.7, 'Load\nForecasting'),
    (4.5, 3.7, 'Generation\nPrediction'),
    (6.2, 3.7, 'Optimal\nScheduling'),
    (8.0, 3.7, 'Fault\nDetection'),
]

for x, y, label in ai_modules:
    rect = mpatches.FancyBboxPatch((x-0.65, y-0.3), 1.3, 0.6,
                                    boxstyle="round,pad=0.04",
                                    facecolor='#A5D6A7', edgecolor='#388E3C', linewidth=1)
    ax.add_patch(rect)
    ax.text(x, y, label, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#1B5E20')

# Arrow data -> AI
ax.annotate('', xy=(5.5, 4.8), xytext=(5.5, 5.3),
            arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))

# Layer 4: Outputs / Applications
rect_out = mpatches.FancyBboxPatch((0.5, 1.3), 10.0, 1.2,
                                    boxstyle="round,pad=0.1",
                                    facecolor='#FFF3E0', edgecolor='#E65100', linewidth=1.5)
ax.add_patch(rect_out)

outputs = [
    (2.0, 1.9, 'Demand\nResponse'),
    (4.0, 1.9, 'Energy\nTrading'),
    (6.0, 1.9, 'Grid\nStability'),
    (8.0, 1.9, 'Cost\nMinimization'),
    (10.0, 1.9, 'Carbon\nReduction'),
]

for x, y, label in outputs:
    ax.text(x, y, label, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#BF360C')

# Arrow AI -> Outputs
ax.annotate('', xy=(5.5, 2.5), xytext=(5.5, 3.3),
            arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2))

# Bottom feedback
ax.annotate('', xy=(0.8, 5.65), xytext=(0.8, 1.9),
            arrowprops=dict(arrowstyle='->', color='#9E9E9E', lw=1.5, linestyle='dashed'))
ax.text(0.4, 3.8, 'Feedback\nLoop', ha='center', va='center', fontsize=7, color='#616161', style='italic')

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/energy_figures/Figure_4_Smart_Grid_Architecture.png', dpi=150, bbox_inches='tight')
plt.close()

print("All 4 energy system figures generated successfully!")
print(os.listdir('/projects/sandbox/AMMAN/energy_figures'))
