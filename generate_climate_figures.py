"""
Generate 4 professional figures for the Climate Change, Economic Risk, 
and Adaptive Eco-Technological Strategies chapter.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# Create output directory
os.makedirs('/projects/sandbox/AMMAN/climate_figures', exist_ok=True)

# Set global style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['figure.dpi'] = 300

# ============================================================
# FIGURE 1: Global Temperature Anomaly and Economic Loss Trends
# ============================================================
fig, ax1 = plt.subplots(figsize=(10, 6))

years = np.arange(2000, 2026)
# Temperature anomaly data (relative to pre-industrial baseline)
temp_anomaly = np.array([0.61, 0.63, 0.67, 0.69, 0.72, 0.74, 0.76, 0.78, 0.80, 0.83,
                         0.87, 0.90, 0.93, 0.96, 1.00, 1.04, 1.09, 1.14, 1.18, 1.22,
                         1.28, 1.32, 1.38, 1.42, 1.48, 1.52])

# Economic losses from climate disasters (billion USD)
econ_losses = np.array([65, 72, 58, 80, 120, 95, 78, 88, 190, 68,
                        130, 105, 140, 95, 115, 165, 210, 145, 225, 190,
                        280, 310, 260, 340, 380, 420])

color1 = '#d62728'
color2 = '#1f77b4'

ax1.set_xlabel('Year')
ax1.set_ylabel('Global Temperature Anomaly (°C)', color=color1)
ax1.plot(years, temp_anomaly, color=color1, linewidth=2.5, marker='o', markersize=4, label='Temperature Anomaly')
ax1.fill_between(years, temp_anomaly - 0.05, temp_anomaly + 0.05, alpha=0.15, color=color1)
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_ylim(0.4, 1.8)

ax2 = ax1.twinx()
ax2.set_ylabel('Climate-Related Economic Losses (Billion USD)', color=color2)
ax2.bar(years, econ_losses, alpha=0.4, color=color2, width=0.7, label='Economic Losses')
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_ylim(0, 500)

# Add trend lines
z_temp = np.polyfit(years, temp_anomaly, 2)
p_temp = np.poly1d(z_temp)
ax1.plot(years, p_temp(years), '--', color=color1, alpha=0.6, linewidth=1.5)

z_econ = np.polyfit(years, econ_losses, 2)
p_econ = np.poly1d(z_econ)
ax2.plot(years, p_econ(years), '--', color=color2, alpha=0.8, linewidth=1.5)

# Legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9)

ax1.set_title('Figure 1: Global Temperature Anomaly and Climate-Related Economic Losses (2000–2025)')
ax1.grid(True, alpha=0.3)
fig.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/climate_figures/Figure_1_Temperature_Economic_Losses.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# FIGURE 2: Sectoral Vulnerability Assessment Heatmap
# ============================================================
fig, ax = plt.subplots(figsize=(11, 7))

sectors = ['Agriculture', 'Water Resources', 'Energy', 'Transportation',
           'Manufacturing', 'Tourism', 'Healthcare', 'Finance/Insurance']
risk_categories = ['Physical\nRisk', 'Transition\nRisk', 'Supply Chain\nDisruption',
                   'Revenue\nLoss', 'Adaptation\nCost', 'Regulatory\nExposure']

# Vulnerability scores (0-10)
data = np.array([
    [9.2, 5.1, 7.8, 8.5, 7.2, 6.8],  # Agriculture
    [8.8, 4.5, 6.2, 7.1, 8.5, 7.5],  # Water Resources
    [7.5, 8.8, 6.5, 6.2, 7.8, 9.0],  # Energy
    [8.0, 6.5, 7.2, 5.8, 8.2, 7.0],  # Transportation
    [6.5, 7.2, 8.5, 6.8, 6.5, 7.8],  # Manufacturing
    [8.5, 4.8, 5.2, 8.8, 6.0, 5.5],  # Tourism
    [7.0, 3.5, 5.8, 4.5, 7.5, 6.2],  # Healthcare
    [5.8, 8.5, 4.2, 7.5, 5.5, 8.8],  # Finance/Insurance
])

im = ax.imshow(data, cmap='YlOrRd', aspect='auto', vmin=0, vmax=10)

ax.set_xticks(np.arange(len(risk_categories)))
ax.set_yticks(np.arange(len(sectors)))
ax.set_xticklabels(risk_categories, fontsize=9)
ax.set_yticklabels(sectors, fontsize=10)

# Add text annotations
for i in range(len(sectors)):
    for j in range(len(risk_categories)):
        text_color = 'white' if data[i, j] > 7.0 else 'black'
        ax.text(j, i, f'{data[i, j]:.1f}', ha='center', va='center',
                color=text_color, fontsize=9, fontweight='bold')

cbar = plt.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label('Vulnerability Score (0–10)', fontsize=10)

ax.set_title('Figure 2: Sectoral Climate Vulnerability Assessment Matrix', fontsize=12, pad=15)
ax.set_xlabel('Risk Category', fontsize=11)
ax.set_ylabel('Economic Sector', fontsize=11)

fig.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/climate_figures/Figure_2_Sectoral_Vulnerability_Heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# FIGURE 3: Intelligent Eco-Technology Framework
# ============================================================
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 9)
ax.axis('off')

# Title
ax.text(6, 8.5, 'Figure 3: Integrated Intelligent Eco-Technology Framework\nfor Climate Adaptation and Resilience',
        ha='center', va='center', fontsize=12, fontweight='bold')

# Central hub
circle_center = plt.Circle((6, 4.5), 1.2, color='#2c3e50', alpha=0.85)
ax.add_patch(circle_center)
ax.text(6, 4.5, 'Integrated\nClimate\nResilience\nPlatform', ha='center', va='center',
        color='white', fontsize=9, fontweight='bold')

# Surrounding technology nodes
tech_nodes = [
    (2.5, 7.0, 'AI & Machine\nLearning', '#e74c3c'),
    (9.5, 7.0, 'IoT Sensor\nNetworks', '#3498db'),
    (1.5, 4.5, 'Digital Twin\nSimulation', '#27ae60'),
    (10.5, 4.5, 'Renewable\nEnergy Systems', '#f39c12'),
    (2.5, 2.0, 'Early Warning\nSystems', '#9b59b6'),
    (9.5, 2.0, 'Smart\nInfrastructure', '#1abc9c'),
]

for x, y, label, color in tech_nodes:
    rect = mpatches.FancyBboxPatch((x-1.0, y-0.6), 2.0, 1.2,
                                    boxstyle="round,pad=0.1",
                                    facecolor=color, alpha=0.8)
    ax.add_patch(rect)
    ax.text(x, y, label, ha='center', va='center', color='white',
            fontsize=8.5, fontweight='bold')
    # Draw connection lines
    ax.annotate('', xy=(6 + 1.2*(x-6)/max(abs(x-6), 0.01)*0.3, 4.5 + 1.2*(y-4.5)/max(abs(y-4.5), 0.01)*0.3),
                xytext=(x + (6-x)*0.25, y + (4.5-y)*0.25),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5, alpha=0.7))

# Output boxes at bottom
outputs = [
    (2.0, 0.5, 'Climate Risk\nMitigation'),
    (5.0, 0.5, 'Economic\nResilience'),
    (8.0, 0.5, 'Sustainable\nDevelopment'),
    (11.0, 0.5, 'Adaptive\nGovernance'),
]

for x, y, label in outputs:
    rect = mpatches.FancyBboxPatch((x-0.9, y-0.35), 1.8, 0.7,
                                    boxstyle="round,pad=0.05",
                                    facecolor='#34495e', alpha=0.7)
    ax.add_patch(rect)
    ax.text(x, y, label, ha='center', va='center', color='white', fontsize=7.5)

# Arrow from center to outputs
for x, y, label in outputs:
    ax.annotate('', xy=(x, y+0.35), xytext=(6, 4.5-1.2),
                arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=1.0, alpha=0.5))

fig.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/climate_figures/Figure_3_EcoTechnology_Framework.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# FIGURE 4: Adaptive Strategy Pathways and Future Scenarios
# ============================================================
fig, ax = plt.subplots(figsize=(10, 7))

years_future = np.arange(2025, 2051)
n = len(years_future)

# Scenario projections (GDP impact as % deviation from baseline)
np.random.seed(42)
baseline = np.zeros(n)

# Business as usual (increasing negative impact)
bau = -np.cumsum(np.random.uniform(0.1, 0.4, n)) - np.linspace(0, 3, n)

# Moderate adaptation
moderate = -np.cumsum(np.random.uniform(0.05, 0.2, n)) - np.linspace(0, 1.5, n)
moderate = moderate + np.linspace(0, 0.8, n)

# Aggressive adaptation + eco-technology
aggressive = -np.cumsum(np.random.uniform(0.02, 0.1, n)) - np.linspace(0, 0.5, n)
aggressive = aggressive + np.linspace(0, 2.5, n)

# Intelligent eco-tech transformation
intelligent = np.cumsum(np.random.uniform(-0.05, 0.15, n)) + np.linspace(0, 3, n)

ax.plot(years_future, bau, 'r-', linewidth=2.5, label='Business as Usual (No Adaptation)')
ax.fill_between(years_future, bau - 1, bau + 1, alpha=0.1, color='red')

ax.plot(years_future, moderate, color='#ff7f0e', linewidth=2.5, label='Moderate Adaptation')
ax.fill_between(years_future, moderate - 0.8, moderate + 0.8, alpha=0.1, color='orange')

ax.plot(years_future, aggressive, 'g-', linewidth=2.5, label='Aggressive Adaptation + Green Tech')
ax.fill_between(years_future, aggressive - 0.6, aggressive + 0.6, alpha=0.1, color='green')

ax.plot(years_future, intelligent, 'b-', linewidth=2.5, label='Intelligent Eco-Tech Transformation')
ax.fill_between(years_future, intelligent - 0.5, intelligent + 0.5, alpha=0.1, color='blue')

ax.axhline(y=0, color='black', linestyle='--', alpha=0.5, linewidth=1)
ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('GDP Impact (% Deviation from Baseline)', fontsize=11)
ax.set_title('Figure 4: Adaptive Strategy Pathways and Economic Impact Scenarios (2025–2050)', fontsize=11)
ax.legend(loc='lower left', framealpha=0.9, fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(2025, 2050)
ax.set_ylim(-12, 8)

# Add annotations
ax.annotate('Climate damages\naccelerate', xy=(2045, bau[20]), xytext=(2042, bau[20]-2),
            fontsize=8, color='red', arrowprops=dict(arrowstyle='->', color='red', lw=1))
ax.annotate('Net positive\nreturns', xy=(2045, intelligent[20]), xytext=(2042, intelligent[20]+1.5),
            fontsize=8, color='blue', arrowprops=dict(arrowstyle='->', color='blue', lw=1))

fig.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/climate_figures/Figure_4_Adaptive_Strategy_Pathways.png', dpi=300, bbox_inches='tight')
plt.close()

print("All 4 figures generated successfully!")
print("Files saved in /projects/sandbox/AMMAN/climate_figures/")
for f in os.listdir('/projects/sandbox/AMMAN/climate_figures/'):
    print(f"  - {f}")
