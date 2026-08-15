"""
Generate 4 figures for Chapter 5: AI-Powered Digital Marketing for Sustainability
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs('/projects/sandbox/AMMAN/ch5_figures', exist_ok=True)

# Set global style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11

# ============================================================
# Figure 1: Framework for AI-Driven Sustainable Digital Marketing
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(10, 7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
ax.text(5, 9.5, 'Framework for AI-Driven Sustainable Digital Marketing', 
        ha='center', va='center', fontsize=14, fontweight='bold')

# Central circle
circle_center = plt.Circle((5, 5), 1.2, color='#2E86AB', alpha=0.3)
ax.add_patch(circle_center)
ax.text(5, 5, 'AI-Powered\nSustainable\nMarketing', ha='center', va='center', fontsize=10, fontweight='bold')

# Surrounding components
components = [
    (2, 8, 'Predictive\nAnalytics', '#A23B72'),
    (8, 8, 'NLP &\nGenerative AI', '#F18F01'),
    (1.5, 5, 'Consumer\nSegmentation', '#C73E1D'),
    (8.5, 5, 'Recommendation\nEngines', '#3B1F2B'),
    (2, 2, 'Ethical AI\nGovernance', '#44AF69'),
    (8, 2, 'Impact\nMeasurement', '#2196F3'),
]

colors_light = ['#E8D5E0', '#FFF0D5', '#F5D5CF', '#D5C8C4', '#D5F0DC', '#D5E8F5']

for i, (x, y, label, color) in enumerate(components):
    rect = mpatches.FancyBboxPatch((x-0.9, y-0.6), 1.8, 1.2, 
                                     boxstyle="round,pad=0.1", 
                                     facecolor=colors_light[i], edgecolor=color, linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', color=color)
    # Draw arrows to center
    dx = 5 - x
    dy = 5 - y
    dist = np.sqrt(dx**2 + dy**2)
    ax.annotate('', xy=(5 - dx/dist*1.3, 5 - dy/dist*1.3), 
                xytext=(x + dx/dist*1.0, y + dy/dist*0.7),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

# Add outer ring labels
ax.text(5, 0.5, 'Sustainability Outcomes: Reduced Carbon Footprint • Green Consumer Behavior • Ethical Brand Trust', 
        ha='center', va='center', fontsize=9, style='italic', color='#555555')

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/ch5_figures/Figure_1_AI_Sustainable_Marketing_Framework.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# Figure 2: Consumer Engagement Lifecycle with AI Integration
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(11, 6))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')

ax.text(6, 6.5, 'AI-Enhanced Consumer Engagement Lifecycle for Sustainability', 
        ha='center', va='center', fontsize=13, fontweight='bold')

stages = [
    (1.5, 4, 'Awareness', '#1976D2', 'AI Content\nGeneration'),
    (4, 4, 'Interest', '#388E3C', 'Personalized\nRecommendations'),
    (6.5, 4, 'Evaluation', '#F57C00', 'Sentiment\nAnalysis'),
    (9, 4, 'Purchase', '#7B1FA2', 'Dynamic\nPricing'),
    (11, 4, 'Advocacy', '#C62828', 'Loyalty\nAI Programs'),
]

for i, (x, y, label, color, ai_tool) in enumerate(stages):
    # Main stage box
    rect = mpatches.FancyBboxPatch((x-0.8, y-0.5), 1.6, 1.0, 
                                     boxstyle="round,pad=0.1", 
                                     facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.8)
    ax.add_patch(rect)
    ax.text(x, y, label, ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    
    # AI tool below
    rect2 = mpatches.FancyBboxPatch((x-0.8, y-2.2), 1.6, 1.2, 
                                      boxstyle="round,pad=0.1", 
                                      facecolor='#E8F5E9', edgecolor=color, linewidth=1.5)
    ax.add_patch(rect2)
    ax.text(x, y-1.6, ai_tool, ha='center', va='center', fontsize=8, color=color)
    
    # Arrow from stage to AI tool
    ax.annotate('', xy=(x, y-1.0), xytext=(x, y-0.55),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
    
    # Arrow to next stage
    if i < len(stages) - 1:
        next_x = stages[i+1][0]
        ax.annotate('', xy=(next_x-0.85, y), xytext=(x+0.85, y),
                    arrowprops=dict(arrowstyle='->', color='#333333', lw=2))

# Sustainability bar at bottom
rect_bottom = mpatches.FancyBboxPatch((0.5, 0.3), 11, 0.8, 
                                        boxstyle="round,pad=0.1", 
                                        facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=2)
ax.add_patch(rect_bottom)
ax.text(6, 0.7, 'Sustainability Integration Layer: Carbon Tracking • Eco-Labeling • Circular Economy Nudges', 
        ha='center', va='center', fontsize=9, fontweight='bold', color='#1B5E20')

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/ch5_figures/Figure_2_Consumer_Engagement_Lifecycle.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# Figure 3: Environmental Footprint of AI Marketing Systems
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))

# Left: Bar chart - Carbon emissions by AI marketing activity
activities = ['Model\nTraining', 'Real-time\nInference', 'Data\nStorage', 'Content\nGeneration', 'A/B\nTesting']
emissions = [45, 25, 15, 10, 5]
colors_bar = ['#D32F2F', '#F57C00', '#FBC02D', '#388E3C', '#1976D2']

axes[0].barh(activities, emissions, color=colors_bar, edgecolor='black', linewidth=0.8)
axes[0].set_xlabel('% of Total Carbon Emissions')
axes[0].set_title('Carbon Emissions by AI Marketing Activity', fontweight='bold')
axes[0].set_xlim(0, 55)
for i, v in enumerate(emissions):
    axes[0].text(v + 1, i, f'{v}%', va='center', fontweight='bold')

# Right: Line chart - Projected carbon reduction with responsible AI
years = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028]
traditional = [100, 110, 122, 135, 150, 167, 185, 205, 228]
responsible_ai = [100, 105, 108, 106, 100, 92, 82, 70, 58]

axes[1].plot(years, traditional, 'r-o', linewidth=2, markersize=6, label='Traditional AI Marketing')
axes[1].plot(years, responsible_ai, 'g-s', linewidth=2, markersize=6, label='Responsible AI Marketing')
axes[1].fill_between(years, responsible_ai, traditional, alpha=0.1, color='green')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Relative Carbon Footprint (Index)')
axes[1].set_title('Carbon Footprint Trajectories', fontweight='bold')
axes[1].legend(loc='upper left')
axes[1].grid(True, alpha=0.3)
axes[1].set_ylim(0, 250)

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/ch5_figures/Figure_3_Environmental_Footprint_AI.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# Figure 4: Industry Applications Matrix - AI for Sustainability
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(11, 7))
ax.set_xlim(0, 11)
ax.set_ylim(0, 8)
ax.axis('off')

ax.text(5.5, 7.5, 'Industry Applications: AI-Driven Sustainability Marketing Matrix', 
        ha='center', va='center', fontsize=13, fontweight='bold')

# Headers
industries = ['Fashion & Apparel', 'Food & Beverage', 'E-Commerce & Retail']
ai_apps = ['Predictive\nAnalytics', 'NLP/Content\nOptimization', 'Personalization\nEngines', 'Impact\nMeasurement']

# Draw grid
header_color = '#1565C0'
for i, ind in enumerate(industries):
    x = 3.5 + i * 2.5
    rect = mpatches.FancyBboxPatch((x-1.0, 6.2), 2.0, 0.8, 
                                     boxstyle="round,pad=0.05", 
                                     facecolor=header_color, edgecolor='black', linewidth=1)
    ax.add_patch(rect)
    ax.text(x, 6.6, ind, ha='center', va='center', fontsize=9, fontweight='bold', color='white')

for j, app in enumerate(ai_apps):
    y = 5.2 - j * 1.5
    rect = mpatches.FancyBboxPatch((0.3, y-0.4), 2.2, 0.8, 
                                     boxstyle="round,pad=0.05", 
                                     facecolor='#E8EAF6', edgecolor='#3F51B5', linewidth=1)
    ax.add_patch(rect)
    ax.text(1.4, y, app, ha='center', va='center', fontsize=8, fontweight='bold', color='#1A237E')

# Fill matrix cells
cell_data = [
    ['Demand\nForecasting', 'Waste\nReduction', 'Inventory\nOptimization'],
    ['Eco-Label\nMessaging', 'Origin\nStorytelling', 'Green\nDescriptions'],
    ['Sustainable\nAlternatives', 'Diet\nNudges', 'Carbon-Score\nRanking'],
    ['Circularity\nMetrics', 'Supply Chain\nTransparency', 'Packaging\nReduction'],
]

cell_colors = ['#E3F2FD', '#E8F5E9', '#FFF3E0']

for i in range(3):
    for j in range(4):
        x = 3.5 + i * 2.5
        y = 5.2 - j * 1.5
        rect = mpatches.FancyBboxPatch((x-0.9, y-0.35), 1.8, 0.7, 
                                         boxstyle="round,pad=0.05", 
                                         facecolor=cell_colors[i], edgecolor='#999999', linewidth=0.8)
        ax.add_patch(rect)
        ax.text(x, y, cell_data[j][i], ha='center', va='center', fontsize=7.5)

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/ch5_figures/Figure_4_Industry_Applications_Matrix.png', dpi=150, bbox_inches='tight')
plt.close()

print("All 4 figures generated successfully!")
print(os.listdir('/projects/sandbox/AMMAN/ch5_figures'))
