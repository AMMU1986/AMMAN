"""
Generate 4 figures for the AI-Driven Consumer Behavior Analytics chapter
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# Create output directory
os.makedirs('/projects/sandbox/AMMAN/ai_chapter_figures', exist_ok=True)

# Set global style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11

# ============================================================
# FIGURE 1: Evolution of AI in Consumer Analytics (Timeline)
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))

periods = ['1990-2000\nTraditional\nMarket Research', 
           '2000-2010\nDigital Analytics\n& CRM',
           '2010-2018\nMachine Learning\n& Big Data',
           '2018-2023\nDeep Learning\n& NLP',
           '2023-Present\nGenerative AI\n& LLMs']

technologies = [
    'Surveys, Focus Groups,\nStatistical Sampling',
    'Web Analytics, Email\nMarketing, Basic CRM',
    'Predictive Models,\nRecommendation Engines',
    'Sentiment Analysis,\nChatbots, Personalization',
    'LLMs, Autonomous Marketing,\nHyper-Personalization'
]

capabilities = [
    'Descriptive\nAnalytics',
    'Diagnostic\nAnalytics',
    'Predictive\nAnalytics',
    'Prescriptive\nAnalytics',
    'Autonomous\nAnalytics'
]

colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#F44336']

x_positions = np.linspace(0.1, 0.9, 5)

# Draw timeline arrow
ax.annotate('', xy=(0.95, 0.5), xytext=(0.05, 0.5),
            arrowprops=dict(arrowstyle='->', lw=2, color='gray'))

for i, (x, period, tech, cap, color) in enumerate(zip(x_positions, periods, technologies, capabilities, colors)):
    # Draw circle on timeline
    circle = plt.Circle((x, 0.5), 0.025, color=color, zorder=5, transform=ax.transAxes)
    ax.add_patch(circle)
    
    # Period label above
    ax.text(x, 0.72, period, ha='center', va='center', fontsize=8.5, fontweight='bold',
            transform=ax.transAxes,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.15, edgecolor=color))
    
    # Technology below
    ax.text(x, 0.30, tech, ha='center', va='center', fontsize=7.5,
            transform=ax.transAxes,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='gray', alpha=0.8))
    
    # Capability label
    ax.text(x, 0.12, cap, ha='center', va='center', fontsize=7.5, fontweight='bold',
            color=color, transform=ax.transAxes)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
ax.set_title('Figure 1: Evolution of Artificial Intelligence in Consumer and Marketing Analytics', 
             fontsize=11, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/ai_chapter_figures/Figure_1_AI_Evolution_Consumer_Analytics.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# FIGURE 2: AI-Based Consumer Segmentation Framework
# ============================================================
fig, ax = plt.subplots(figsize=(11, 8))

# Central element
center_circle = plt.Circle((0.5, 0.5), 0.12, color='#1565C0', alpha=0.9, zorder=5)
ax.add_patch(center_circle)
ax.text(0.5, 0.5, 'AI-Driven\nConsumer\nSegmentation', ha='center', va='center', 
        fontsize=10, fontweight='bold', color='white', zorder=6)

# Surrounding segments
segments = [
    {'pos': (0.5, 0.88), 'label': 'Data Sources', 'color': '#2196F3',
     'items': 'Social Media\nTransactions\nBrowsing Data\nIoT Sensors'},
    {'pos': (0.85, 0.7), 'label': 'ML Techniques', 'color': '#4CAF50',
     'items': 'Clustering\nClassification\nDeep Learning\nNLP'},
    {'pos': (0.85, 0.3), 'label': 'Segmentation Types', 'color': '#FF9800',
     'items': 'Behavioral\nDemographic\nPsychographic\nValue-Based'},
    {'pos': (0.5, 0.12), 'label': 'Predictions', 'color': '#9C27B0',
     'items': 'Purchase Intent\nChurn Risk\nLifetime Value\nPreferences'},
    {'pos': (0.15, 0.3), 'label': 'Personalization', 'color': '#F44336',
     'items': 'Recommendations\nContent\nPricing\nCommunication'},
    {'pos': (0.15, 0.7), 'label': 'Outcomes', 'color': '#009688',
     'items': 'Conversion\nRetention\nSatisfaction\nRevenue'}
]

for seg in segments:
    # Draw connecting line
    ax.plot([0.5, seg['pos'][0]], [0.5, seg['pos'][1]], 
            color='gray', lw=1.5, alpha=0.5, zorder=1)
    
    # Draw segment box
    bbox = mpatches.FancyBboxPatch(
        (seg['pos'][0]-0.1, seg['pos'][1]-0.08), 0.2, 0.16,
        boxstyle="round,pad=0.01", facecolor=seg['color'], alpha=0.15,
        edgecolor=seg['color'], linewidth=2)
    ax.add_patch(bbox)
    
    # Label
    ax.text(seg['pos'][0], seg['pos'][1]+0.04, seg['label'], ha='center', va='center',
            fontsize=9, fontweight='bold', color=seg['color'])
    # Items
    ax.text(seg['pos'][0], seg['pos'][1]-0.03, seg['items'], ha='center', va='center',
            fontsize=7, color='#333333')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
ax.set_title('Figure 2: AI-Based Consumer Segmentation and Behavioral Prediction Framework', 
             fontsize=11, fontweight='bold', pad=15)

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/ai_chapter_figures/Figure_2_AI_Consumer_Segmentation_Framework.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# FIGURE 3: Personalized Customer Engagement Ecosystem
# ============================================================
fig, ax = plt.subplots(figsize=(12, 7))

# Layers (bottom to top)
layers = [
    {'y': 0.08, 'height': 0.14, 'color': '#1565C0', 'label': 'DATA LAYER',
     'items': ['Customer Data Platform', 'IoT & Sensor Data', 'Social Listening', 'Transaction History', 'Behavioral Logs']},
    {'y': 0.24, 'height': 0.14, 'color': '#2E7D32', 'label': 'ANALYTICS LAYER',
     'items': ['Machine Learning', 'Deep Learning', 'NLP & Sentiment', 'Predictive Models', 'Real-time Processing']},
    {'y': 0.40, 'height': 0.14, 'color': '#E65100', 'label': 'INTELLIGENCE LAYER',
     'items': ['Customer Insights', 'Segmentation', 'Journey Analytics', 'Propensity Scoring', 'Churn Prediction']},
    {'y': 0.56, 'height': 0.14, 'color': '#6A1B9A', 'label': 'PERSONALIZATION LAYER',
     'items': ['Recommendations', 'Dynamic Content', 'Adaptive Pricing', 'Next-Best-Action', 'A/B Optimization']},
    {'y': 0.72, 'height': 0.14, 'color': '#C62828', 'label': 'ENGAGEMENT LAYER',
     'items': ['Omnichannel Delivery', 'Chatbots & VA', 'Email & Push', 'Social & Web', 'In-Store Experience']}
]

for layer in layers:
    # Draw layer rectangle
    rect = mpatches.FancyBboxPatch(
        (0.05, layer['y']), 0.9, layer['height'],
        boxstyle="round,pad=0.01", facecolor=layer['color'], alpha=0.12,
        edgecolor=layer['color'], linewidth=2)
    ax.add_patch(rect)
    
    # Layer label
    ax.text(0.08, layer['y'] + layer['height']/2, layer['label'], 
            ha='left', va='center', fontsize=9, fontweight='bold', color=layer['color'])
    
    # Items
    x_positions_items = np.linspace(0.28, 0.92, 5)
    for x, item in zip(x_positions_items, layer['items']):
        ax.text(x, layer['y'] + layer['height']/2, item, ha='center', va='center',
                fontsize=7.5, color='#333',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=layer['color'], alpha=0.7))

# Arrows between layers
for i in range(len(layers)-1):
    y_start = layers[i]['y'] + layers[i]['height']
    y_end = layers[i+1]['y']
    ax.annotate('', xy=(0.5, y_end), xytext=(0.5, y_start),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='gray'))

# Side annotation
ax.text(0.99, 0.5, 'Feedback Loop\n& Continuous\nLearning', ha='center', va='center',
        fontsize=8, fontweight='bold', color='#555', rotation=90,
        transform=ax.transAxes)

ax.set_xlim(0, 1)
ax.set_ylim(0, 0.92)
ax.axis('off')
ax.set_title('Figure 3: AI-Enabled Personalized Customer Engagement Ecosystem', 
             fontsize=11, fontweight='bold', pad=15)

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/ai_chapter_figures/Figure_3_Personalized_Engagement_Ecosystem.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# FIGURE 4: Strategic Framework for AI-Driven Engagement
# ============================================================
fig, ax = plt.subplots(figsize=(12, 8))

# Main framework boxes
framework_elements = [
    # Top row - Strategy
    {'pos': (0.5, 0.88), 'size': (0.85, 0.1), 'color': '#1565C0',
     'title': 'STRATEGIC VISION: Customer-Centric AI-Driven Engagement',
     'items': ''},
    # Second row
    {'pos': (0.18, 0.72), 'size': (0.28, 0.1), 'color': '#2E7D32',
     'title': 'Data Foundation',
     'items': 'Quality | Integration | Governance'},
    {'pos': (0.5, 0.72), 'size': (0.28, 0.1), 'color': '#E65100',
     'title': 'AI & Analytics Engine',
     'items': 'ML | DL | NLP | GenAI'},
    {'pos': (0.82, 0.72), 'size': (0.28, 0.1), 'color': '#6A1B9A',
     'title': 'Personalization Platform',
     'items': 'Real-time | Contextual | Adaptive'},
    # Third row
    {'pos': (0.25, 0.52), 'size': (0.42, 0.1), 'color': '#00695C',
     'title': 'Customer Intelligence',
     'items': 'Segmentation | Prediction | Sentiment | CLV'},
    {'pos': (0.75, 0.52), 'size': (0.42, 0.1), 'color': '#AD1457',
     'title': 'Engagement Orchestration',
     'items': 'Omnichannel | Journey | Experience | Retention'},
    # Fourth row
    {'pos': (0.5, 0.34), 'size': (0.85, 0.1), 'color': '#F57F17',
     'title': 'Ethical & Responsible AI Framework',
     'items': 'Privacy | Transparency | Fairness | Consent | Compliance'},
    # Bottom row
    {'pos': (0.25, 0.16), 'size': (0.42, 0.1), 'color': '#37474F',
     'title': 'Organizational Readiness',
     'items': 'Skills | Culture | Change Management'},
    {'pos': (0.75, 0.16), 'size': (0.42, 0.1), 'color': '#4E342E',
     'title': 'Technology Infrastructure',
     'items': 'Cloud | Edge | APIs | Security'},
]

for elem in framework_elements:
    x, y = elem['pos']
    w, h = elem['size']
    
    rect = mpatches.FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.01", facecolor=elem['color'], alpha=0.15,
        edgecolor=elem['color'], linewidth=2)
    ax.add_patch(rect)
    
    if elem['items']:
        ax.text(x, y + 0.02, elem['title'], ha='center', va='center',
                fontsize=9, fontweight='bold', color=elem['color'])
        ax.text(x, y - 0.02, elem['items'], ha='center', va='center',
                fontsize=7.5, color='#444')
    else:
        ax.text(x, y, elem['title'], ha='center', va='center',
                fontsize=10, fontweight='bold', color=elem['color'])

# Connecting arrows
connections = [
    ((0.5, 0.83), (0.18, 0.77)), ((0.5, 0.83), (0.5, 0.77)), ((0.5, 0.83), (0.82, 0.77)),
    ((0.18, 0.67), (0.25, 0.57)), ((0.5, 0.67), (0.25, 0.57)), ((0.5, 0.67), (0.75, 0.57)),
    ((0.82, 0.67), (0.75, 0.57)),
    ((0.25, 0.47), (0.5, 0.39)), ((0.75, 0.47), (0.5, 0.39)),
    ((0.5, 0.29), (0.25, 0.21)), ((0.5, 0.29), (0.75, 0.21)),
]

for start, end in connections:
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', lw=1, color='gray', alpha=0.6))

# Outcome box at very bottom
ax.text(0.5, 0.04, 'OUTCOMES: Enhanced Customer Experience | Increased Revenue | Sustainable Growth | Trust',
        ha='center', va='center', fontsize=9, fontweight='bold', color='#1B5E20',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=2))

ax.set_xlim(0, 1)
ax.set_ylim(0, 0.97)
ax.axis('off')
ax.set_title('Figure 4: Strategic Framework for AI-Driven Personalized Customer Engagement', 
             fontsize=11, fontweight='bold', pad=10)

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/ai_chapter_figures/Figure_4_Strategic_Framework.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("All 4 figures generated successfully!")
print(os.listdir('/projects/sandbox/AMMAN/ai_chapter_figures'))
