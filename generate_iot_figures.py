"""
Generate 4 figures for the IoT & Smart Cities chapter
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

os.makedirs('/projects/sandbox/AMMAN/iot_figures', exist_ok=True)

# Figure 1: IoT Architecture - Layered Model (Sensors → Edge → Fog → Cloud)
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Figure 1: Multi-Layer IoT Architecture for Smart City Infrastructure', fontsize=14, fontweight='bold', pad=20)

# Layers
layers = [
    (1.0, 'Perception Layer\n(Sensors & Actuators)', '#E8F5E9', 
     'Temperature, Humidity, Air Quality,\nTraffic Sensors, Smart Meters, CCTV'),
    (3.0, 'Edge Computing Layer\n(Local Processing)', '#E3F2FD',
     'Real-time Analytics, Data Filtering,\nLocal Decision Making, Latency < 10ms'),
    (5.0, 'Fog Computing Layer\n(Regional Processing)', '#FFF3E0',
     'Data Aggregation, Pattern Recognition,\nRegional Coordination, Load Balancing'),
    (7.0, 'Cloud Computing Layer\n(Global Analytics)', '#F3E5F5',
     'Big Data Analytics, AI/ML Training,\nDigital Twins, Long-term Storage'),
    (9.0, 'Application Layer\n(Smart City Services)', '#FFEBEE',
     'Traffic Management, Energy Optimization,\nPublic Safety, Healthcare, Governance')
]

for y, label, color, desc in layers:
    rect = FancyBboxPatch((0.5, y-0.4), 9, 1.4, boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor='#333333', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(2.5, y+0.3, label, fontsize=11, fontweight='bold', va='center', ha='center')
    ax.text(6.5, y+0.3, desc, fontsize=9, va='center', ha='center', style='italic')

# Arrows between layers
for i in range(len(layers)-1):
    ax.annotate('', xy=(5, layers[i+1][0]-0.4), xytext=(5, layers[i][0]+1.0),
                arrowprops=dict(arrowstyle='->', lw=2, color='#1565C0'))

# Side labels
ax.text(0.1, 5, 'Data Flow ↑', fontsize=10, rotation=90, va='center', ha='center', color='#1565C0', fontweight='bold')
ax.text(9.9, 5, 'Control Flow ↓', fontsize=10, rotation=270, va='center', ha='center', color='#C62828', fontweight='bold')

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/iot_figures/Figure_1_IoT_Architecture.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 2: Smart City Communication Networks
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Figure 2: Communication Technologies and Network Topology\nfor Smart City IoT Ecosystems', fontsize=13, fontweight='bold', pad=15)

# Network categories
categories = {
    'LPWAN\n(Long Range)': (2, 7.5, '#C8E6C9', ['LoRaWAN', 'NB-IoT', 'Sigfox', 'LTE-M']),
    '5G/6G\n(High Speed)': (6, 7.5, '#BBDEFB', ['eMBB', 'URLLC', 'mMTC', 'THz Comm']),
    'Mesh Networks\n(Local)': (10, 7.5, '#FFE0B2', ['Zigbee', 'Thread', 'Wi-Fi 6E', 'Bluetooth 5']),
    'TSN\n(Time-Sensitive)': (2, 3, '#E1BEE7', ['IEEE 802.1', 'DetNet', 'OPC UA', 'Profinet']),
    'Satellite\n(Global)': (6, 3, '#B2DFDB', ['LEO Sat', 'Starlink', 'OneWeb', 'IoT NTN']),
    'Edge Network\n(Computing)': (10, 3, '#FFCDD2', ['MEC', 'Cloudlet', 'Micro DC', 'CDN'])
}

for label, (x, y, color, items) in categories.items():
    rect = FancyBboxPatch((x-1.5, y-1.2), 3, 2.8, boxstyle="round,pad=0.15",
                          facecolor=color, edgecolor='#333', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x, y+1.0, label, fontsize=10, fontweight='bold', ha='center', va='center')
    for i, item in enumerate(items):
        ax.text(x, y - 0.1 - i*0.4, f'• {item}', fontsize=8, ha='center', va='center')

# Central hub
circle = plt.Circle((6, 5.3), 0.6, color='#FDD835', ec='#F57F17', linewidth=2)
ax.add_patch(circle)
ax.text(6, 5.3, 'Smart\nCity\nHub', fontsize=8, ha='center', va='center', fontweight='bold')

# Connections
for label, (x, y, color, items) in categories.items():
    ax.annotate('', xy=(6, 5.3), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='#555', connectionstyle='arc3,rad=0.1'))

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/iot_figures/Figure_2_Communication_Networks.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 3: Smart City Applications Framework
fig, ax = plt.subplots(1, 1, figsize=(12, 9))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Figure 3: IoT Applications Framework for Sustainable Urban Infrastructure', fontsize=13, fontweight='bold', pad=15)

# Central circle
circle = plt.Circle((6, 5), 1.2, color='#1976D2', ec='#0D47A1', linewidth=2.5)
ax.add_patch(circle)
ax.text(6, 5, 'IoT-Enabled\nSmart City\nPlatform', fontsize=10, ha='center', va='center', 
        fontweight='bold', color='white')

# Application domains around the center
domains = [
    (6, 9, 'Smart Transportation', '#4CAF50', ['Connected Vehicles', 'Traffic AI', 'MaaS', 'EV Charging']),
    (10.5, 7, 'Smart Energy', '#FF9800', ['Smart Grids', 'Microgrids', 'Demand Response', 'Solar/Wind']),
    (10.5, 3, 'Smart Water &\nWaste', '#00BCD4', ['Leak Detection', 'Quality Monitor', 'Smart Bins', 'Recycling']),
    (6, 1, 'Environmental\nMonitoring', '#8BC34A', ['Air Quality', 'Noise Mapping', 'Green Spaces', 'Climate']),
    (1.5, 3, 'Public Safety &\nHealth', '#F44336', ['Surveillance', 'Emergency', 'Telemedicine', 'Pandemic']),
    (1.5, 7, 'Smart Governance', '#9C27B0', ['e-Services', 'Open Data', 'Participation', 'Digital ID'])
]

for x, y, label, color, items in domains:
    rect = FancyBboxPatch((x-1.4, y-0.9), 2.8, 1.8, boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor='#333', linewidth=1.5, alpha=0.8)
    ax.add_patch(rect)
    ax.text(x, y+0.4, label, fontsize=9, fontweight='bold', ha='center', va='center', color='white')
    items_text = ' | '.join(items[:2]) + '\n' + ' | '.join(items[2:])
    ax.text(x, y-0.3, items_text, fontsize=7, ha='center', va='center', color='white')
    
    # Connection line
    ax.annotate('', xy=(6 + 1.2*(x-6)/max(abs(x-6),abs(y-5),0.01)*0.8 if abs(x-6)>0.1 else 6, 
                        5 + 1.2*(y-5)/max(abs(x-6),abs(y-5),0.01)*0.8 if abs(y-5)>0.1 else 5),
                xytext=(x, y),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=color, connectionstyle='arc3,rad=0'))

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/iot_figures/Figure_3_Applications_Framework.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 4: Future Vision - AI-Driven Autonomous Smart City
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Figure 4: Strategic Roadmap for AI-Driven Autonomous Smart Cities', fontsize=13, fontweight='bold', pad=15)

# Timeline phases
phases = [
    (1.5, 'Phase 1\n(2024-2026)', 'Connected\nCity', '#E8F5E9', '#4CAF50',
     ['Basic IoT Deploy', 'Data Collection', '5G Rollout', 'Pilot Projects']),
    (4.5, 'Phase 2\n(2026-2028)', 'Intelligent\nCity', '#E3F2FD', '#1976D2',
     ['AI Analytics', 'Digital Twins', 'Predictive Mgmt', 'Edge Computing']),
    (7.5, 'Phase 3\n(2028-2031)', 'Autonomous\nCity', '#FFF3E0', '#FF9800',
     ['Self-Healing Infra', 'Autonomous Traffic', 'AI Governance', '6G Networks']),
    (10.5, 'Phase 4\n(2031-2035)', 'Cognitive\nCity', '#F3E5F5', '#9C27B0',
     ['AGI Systems', 'Full Automation', 'Quantum IoT', 'Neural Cities'])
]

# Draw timeline arrow
ax.annotate('', xy=(11.5, 5), xytext=(0.5, 5),
            arrowprops=dict(arrowstyle='->', lw=3, color='#333'))

for x, phase, title, bg_color, border_color, items in phases:
    # Upper box
    rect = FancyBboxPatch((x-1.2, 5.5), 2.4, 3.5, boxstyle="round,pad=0.1",
                          facecolor=bg_color, edgecolor=border_color, linewidth=2)
    ax.add_patch(rect)
    ax.text(x, 8.5, phase, fontsize=9, fontweight='bold', ha='center', va='center', color=border_color)
    ax.text(x, 7.5, title, fontsize=10, fontweight='bold', ha='center', va='center')
    for i, item in enumerate(items):
        ax.text(x, 6.8-i*0.4, f'• {item}', fontsize=8, ha='center', va='center')
    
    # Timeline dot
    circle = plt.Circle((x, 5), 0.2, color=border_color, ec='#333', linewidth=1.5)
    ax.add_patch(circle)
    
    # Lower metrics
    rect2 = FancyBboxPatch((x-1.2, 1.5), 2.4, 2.8, boxstyle="round,pad=0.1",
                           facecolor='#FAFAFA', edgecolor=border_color, linewidth=1.5, linestyle='--')
    ax.add_patch(rect2)

metrics = [
    (1.5, ['ROI: 15-25%', 'Coverage: 40%', 'Sensors: 1M']),
    (4.5, ['ROI: 30-45%', 'Coverage: 70%', 'Sensors: 10M']),
    (7.5, ['ROI: 50-80%', 'Coverage: 90%', 'Sensors: 50M']),
    (10.5, ['ROI: 100%+', 'Coverage: 99%', 'Sensors: 500M'])
]

for x, items in metrics:
    ax.text(x, 4.0, 'Key Metrics', fontsize=8, fontweight='bold', ha='center', va='center')
    for i, item in enumerate(items):
        ax.text(x, 3.3-i*0.5, item, fontsize=8, ha='center', va='center')

ax.text(6, 0.8, 'Maturity Level →', fontsize=11, ha='center', va='center', fontweight='bold', color='#333')

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/iot_figures/Figure_4_Strategic_Roadmap.png', dpi=150, bbox_inches='tight')
plt.close()

print("All 4 figures generated successfully!")
print(os.listdir('/projects/sandbox/AMMAN/iot_figures'))
