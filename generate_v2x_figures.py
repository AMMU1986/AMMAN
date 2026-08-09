"""
Generate 4 figures for Chapter 2: Communication Protocols for Vehicular Networks
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# Create output directory
os.makedirs('/projects/sandbox/AMMAN/v2x_figures', exist_ok=True)

# Set global style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11

# ============================================================
# Figure 1: Evolution of Vehicular Communication Technologies
# ============================================================
def create_figure1():
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Figure 1: Evolution of Vehicular Communication Technologies\nfrom DSRC to 6G V2X', 
                 fontsize=13, fontweight='bold', pad=20)
    
    # Timeline blocks
    generations = [
        {'name': 'DSRC/WAVE\n(IEEE 802.11p)', 'year': '2010-2016', 'x': 1.5, 'color': '#3498db',
         'features': ['5.9 GHz Band', '10 MHz BW', 'CSMA/CA', '300m Range', '6-27 Mbps']},
        {'name': 'C-V2X\n(LTE Release 14/15)', 'year': '2017-2019', 'x': 4.5, 'color': '#2ecc71',
         'features': ['PC5 Sidelink', 'Uu Interface', 'SC-FDMA', '450m Range', 'Up to 50 Mbps']},
        {'name': '5G NR-V2X\n(Release 16/17)', 'year': '2020-2024', 'x': 7.5, 'color': '#e74c3c',
         'features': ['Sub-6 & mmWave', 'URLLC < 1ms', 'Unicast/Groupcast', '1000m Range', 'Up to 1 Gbps']},
        {'name': '6G V2X\n(Beyond 2028)', 'year': '2025-2030+', 'x': 10.5, 'color': '#9b59b6',
         'features': ['THz & RIS', 'AI-Native', 'ISAC', 'Digital Twin', '> 100 Gbps']},
    ]
    
    for gen in generations:
        # Main box
        rect = FancyBboxPatch((gen['x']-1.2, 4.5), 2.4, 4.5, 
                              boxstyle="round,pad=0.1", 
                              facecolor=gen['color'], alpha=0.15, edgecolor=gen['color'], linewidth=2)
        ax.add_patch(rect)
        
        # Title
        ax.text(gen['x'], 8.5, gen['name'], ha='center', va='center', 
                fontsize=10, fontweight='bold', color=gen['color'])
        
        # Year
        ax.text(gen['x'], 7.5, gen['year'], ha='center', va='center', 
                fontsize=9, style='italic', color='#555555')
        
        # Features
        for i, feat in enumerate(gen['features']):
            ax.text(gen['x'], 6.8 - i*0.45, feat, ha='center', va='center', 
                    fontsize=8, color='#333333')
    
    # Arrow connections
    for i in range(3):
        x_start = generations[i]['x'] + 1.3
        x_end = generations[i+1]['x'] - 1.3
        ax.annotate('', xy=(x_end, 6.5), xytext=(x_start, 6.5),
                    arrowprops=dict(arrowstyle='->', color='#555555', lw=2))
    
    # Bottom: Key metrics progression
    ax.text(7, 3.5, 'Key Performance Progression', ha='center', fontsize=11, fontweight='bold')
    
    metrics = ['Latency:', 'Reliability:', 'Data Rate:', 'V2X Modes:']
    values = [
        ['~100 ms', '~50 ms', '< 1 ms', '< 0.1 ms'],
        ['~90%', '~95%', '99.999%', '99.99999%'],
        ['6-27 Mbps', '~50 Mbps', '~1 Gbps', '> 100 Gbps'],
        ['V2V, V2I', 'V2V, V2I, V2N', 'V2V, V2I, V2N, V2P', 'V2X + Sensing']
    ]
    
    for i, metric in enumerate(metrics):
        ax.text(0.5, 2.8 - i*0.6, metric, ha='left', fontsize=9, fontweight='bold')
        for j, val in enumerate(values[i]):
            ax.text(generations[j]['x'], 2.8 - i*0.6, val, ha='center', fontsize=8,
                    color=generations[j]['color'])
    
    plt.tight_layout()
    plt.savefig('/projects/sandbox/AMMAN/v2x_figures/Figure_1_V2X_Evolution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 1 created successfully")

# ============================================================
# Figure 2: DSRC vs C-V2X Protocol Architecture Comparison
# ============================================================
def create_figure2():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))
    
    fig.suptitle('Figure 2: Protocol Stack Architecture Comparison\nDSRC/WAVE vs C-V2X', 
                 fontsize=13, fontweight='bold', y=0.98)
    
    # DSRC/WAVE Stack
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 12)
    ax1.axis('off')
    ax1.set_title('DSRC/WAVE Protocol Stack', fontsize=11, fontweight='bold', pad=10)
    
    dsrc_layers = [
        {'name': 'Safety Applications\n(BSM, SPaT, MAP)', 'y': 10.5, 'color': '#e74c3c', 'height': 1.2},
        {'name': 'WAVE Short Message Protocol\n(WSMP - IEEE 1609.3)', 'y': 9.0, 'color': '#e67e22', 'height': 1.2},
        {'name': 'IEEE 1609.4\nMulti-Channel Operation', 'y': 7.5, 'color': '#f39c12', 'height': 1.2},
        {'name': 'IEEE 1609.2\nSecurity Services', 'y': 6.0, 'color': '#27ae60', 'height': 1.2},
        {'name': 'IEEE 802.11p MAC\n(EDCA, CSMA/CA)', 'y': 4.5, 'color': '#2980b9', 'height': 1.2},
        {'name': 'IEEE 802.11p PHY\n(OFDM, 5.9 GHz, 10 MHz)', 'y': 3.0, 'color': '#8e44ad', 'height': 1.2},
        {'name': 'DSRC Radio\n(5.850-5.925 GHz)', 'y': 1.5, 'color': '#2c3e50', 'height': 1.2},
    ]
    
    for layer in dsrc_layers:
        rect = FancyBboxPatch((1, layer['y']-0.5), 8, layer['height'], 
                              boxstyle="round,pad=0.05",
                              facecolor=layer['color'], alpha=0.2, edgecolor=layer['color'], linewidth=1.5)
        ax1.add_patch(rect)
        ax1.text(5, layer['y'] + 0.1, layer['name'], ha='center', va='center', fontsize=8.5)
    
    # C-V2X Stack
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 12)
    ax2.axis('off')
    ax2.set_title('C-V2X Protocol Stack', fontsize=11, fontweight='bold', pad=10)
    
    cv2x_layers = [
        {'name': 'V2X Applications\n(BSM, CAM, DENM, CPM)', 'y': 10.5, 'color': '#e74c3c', 'height': 1.2},
        {'name': 'V2X Application Layer\n(SAE J2945, ETSI ITS)', 'y': 9.0, 'color': '#e67e22', 'height': 1.2},
        {'name': 'Transport & Network\n(GeoNetworking / IP)', 'y': 7.5, 'color': '#f39c12', 'height': 1.2},
        {'name': 'V2X Security\n(PKI, Certificates)', 'y': 6.0, 'color': '#27ae60', 'height': 1.2},
        {'name': 'PC5 / Uu RLC/MAC\n(SC-FDMA, Semi-Persistent)', 'y': 4.5, 'color': '#2980b9', 'height': 1.2},
        {'name': 'LTE-V2X PHY\n(SC-FDMA, 10/20 MHz)', 'y': 3.0, 'color': '#8e44ad', 'height': 1.2},
        {'name': 'C-V2X Radio\n(5.9 GHz + Cellular)', 'y': 1.5, 'color': '#2c3e50', 'height': 1.2},
    ]
    
    for layer in cv2x_layers:
        rect = FancyBboxPatch((1, layer['y']-0.5), 8, layer['height'], 
                              boxstyle="round,pad=0.05",
                              facecolor=layer['color'], alpha=0.2, edgecolor=layer['color'], linewidth=1.5)
        ax2.add_patch(rect)
        ax2.text(5, layer['y'] + 0.1, layer['name'], ha='center', va='center', fontsize=8.5)
    
    # Side labels
    for ax in [ax1, ax2]:
        ax.text(0.3, 10.5, 'App', fontsize=7, rotation=0, va='center', fontweight='bold', color='gray')
        ax.text(0.3, 7.5, 'Net', fontsize=7, rotation=0, va='center', fontweight='bold', color='gray')
        ax.text(0.3, 4.5, 'MAC', fontsize=7, rotation=0, va='center', fontweight='bold', color='gray')
        ax.text(0.3, 1.5, 'PHY', fontsize=7, rotation=0, va='center', fontweight='bold', color='gray')
    
    plt.tight_layout()
    plt.savefig('/projects/sandbox/AMMAN/v2x_figures/Figure_2_Protocol_Architecture.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 2 created successfully")

# ============================================================
# Figure 3: 5G NR-V2X Network Architecture and Slicing
# ============================================================
def create_figure3():
    fig, ax = plt.subplots(1, 1, figsize=(13, 8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')
    ax.set_title('Figure 3: 5G NR-V2X Network Architecture with Network Slicing\nand Multi-Access Edge Computing (MEC)', 
                 fontsize=12, fontweight='bold', pad=15)
    
    # Vehicle layer at bottom
    vehicle_rect = FancyBboxPatch((0.5, 0.3), 15, 2, boxstyle="round,pad=0.1",
                                   facecolor='#ecf0f1', edgecolor='#7f8c8d', linewidth=1.5)
    ax.add_patch(vehicle_rect)
    ax.text(8, 1.8, 'Vehicle Layer', ha='center', fontsize=10, fontweight='bold')
    
    vehicles = ['OBU\n(V2V)', 'UE\n(V2I)', 'UE\n(V2N)', 'Sensor\n(V2P)', 'RSU\n(Edge)']
    colors_v = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']
    for i, (v, c) in enumerate(zip(vehicles, colors_v)):
        rect = FancyBboxPatch((1+i*3, 0.5), 2.2, 1.0, boxstyle="round,pad=0.05",
                              facecolor=c, alpha=0.3, edgecolor=c, linewidth=1)
        ax.add_patch(rect)
        ax.text(2.1+i*3, 1.0, v, ha='center', va='center', fontsize=7.5)
    
    # RAN Layer
    ran_rect = FancyBboxPatch((0.5, 2.8), 15, 2, boxstyle="round,pad=0.1",
                               facecolor='#d5f5e3', edgecolor='#27ae60', linewidth=1.5)
    ax.add_patch(ran_rect)
    ax.text(8, 4.3, 'Radio Access Network (RAN)', ha='center', fontsize=10, fontweight='bold')
    
    ran_items = ['gNB\n(Sub-6 GHz)', 'gNB\n(mmWave)', 'PC5\nSidelink', 'MEC\nServer']
    for i, item in enumerate(ran_items):
        rect = FancyBboxPatch((1.5+i*3.5, 3.0), 2.5, 1.0, boxstyle="round,pad=0.05",
                              facecolor='#27ae60', alpha=0.2, edgecolor='#27ae60', linewidth=1)
        ax.add_patch(rect)
        ax.text(2.75+i*3.5, 3.5, item, ha='center', va='center', fontsize=8)
    
    # Core Network with Slicing
    core_rect = FancyBboxPatch((0.5, 5.3), 15, 2.2, boxstyle="round,pad=0.1",
                                facecolor='#fdebd0', edgecolor='#e67e22', linewidth=1.5)
    ax.add_patch(core_rect)
    ax.text(8, 7.0, '5G Core Network (5GC) with Network Slicing', ha='center', fontsize=10, fontweight='bold')
    
    slices = [
        {'name': 'URLLC Slice\n(Autonomous Driving)', 'color': '#e74c3c'},
        {'name': 'eMBB Slice\n(HD Maps, Infotainment)', 'color': '#3498db'},
        {'name': 'mMTC Slice\n(IoT Sensors)', 'color': '#27ae60'},
        {'name': 'V2X Slice\n(Safety Messages)', 'color': '#9b59b6'},
    ]
    for i, s in enumerate(slices):
        rect = FancyBboxPatch((1+i*3.7, 5.5), 3.0, 1.1, boxstyle="round,pad=0.05",
                              facecolor=s['color'], alpha=0.2, edgecolor=s['color'], linewidth=1)
        ax.add_patch(rect)
        ax.text(2.5+i*3.7, 6.05, s['name'], ha='center', va='center', fontsize=7.5)
    
    # Cloud/AI Layer
    cloud_rect = FancyBboxPatch((0.5, 8.0), 15, 2.2, boxstyle="round,pad=0.1",
                                 facecolor='#ebdef0', edgecolor='#8e44ad', linewidth=1.5)
    ax.add_patch(cloud_rect)
    ax.text(8, 9.7, 'Cloud & AI Layer', ha='center', fontsize=10, fontweight='bold')
    
    cloud_items = ['V2X Application\nServer', 'AI/ML\nOrchestrator', 'Digital Twin\nPlatform', 'Traffic Mgmt\nCenter']
    for i, item in enumerate(cloud_items):
        rect = FancyBboxPatch((1.5+i*3.5, 8.2), 2.5, 1.1, boxstyle="round,pad=0.05",
                              facecolor='#8e44ad', alpha=0.15, edgecolor='#8e44ad', linewidth=1)
        ax.add_patch(rect)
        ax.text(2.75+i*3.5, 8.75, item, ha='center', va='center', fontsize=7.5)
    
    # Connection arrows between layers
    for x in [3, 6, 9, 12]:
        ax.annotate('', xy=(x, 2.8), xytext=(x, 2.3),
                    arrowprops=dict(arrowstyle='->', color='#555', lw=1))
        ax.annotate('', xy=(x, 5.3), xytext=(x, 4.8),
                    arrowprops=dict(arrowstyle='->', color='#555', lw=1))
        ax.annotate('', xy=(x, 8.0), xytext=(x, 7.5),
                    arrowprops=dict(arrowstyle='->', color='#555', lw=1))
    
    plt.tight_layout()
    plt.savefig('/projects/sandbox/AMMAN/v2x_figures/Figure_3_5G_NRV2X_Architecture.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 3 created successfully")

# ============================================================
# Figure 4: 6G V2X Vision and Enabling Technologies
# ============================================================
def create_figure4():
    fig, ax = plt.subplots(1, 1, figsize=(12, 9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 12)
    ax.axis('off')
    ax.set_title('Figure 4: 6G V2X Vision — Enabling Technologies and\nIntelligent Transportation Ecosystem', 
                 fontsize=12, fontweight='bold', pad=15)
    
    # Central hub
    circle = plt.Circle((6, 6), 1.5, color='#2c3e50', alpha=0.15, linewidth=2)
    ax.add_patch(circle)
    circle_edge = plt.Circle((6, 6), 1.5, fill=False, color='#2c3e50', linewidth=2)
    ax.add_patch(circle_edge)
    ax.text(6, 6.2, '6G V2X', ha='center', va='center', fontsize=14, fontweight='bold', color='#2c3e50')
    ax.text(6, 5.5, 'Intelligent\nMobility', ha='center', va='center', fontsize=9, color='#555')
    
    # Surrounding technology nodes
    technologies = [
        {'name': 'Terahertz\nCommunication\n(0.1-10 THz)', 'angle': 90, 'color': '#e74c3c'},
        {'name': 'Reconfigurable\nIntelligent\nSurfaces (RIS)', 'angle': 45, 'color': '#3498db'},
        {'name': 'AI-Native\nAir Interface\n& Semantic Comm', 'angle': 0, 'color': '#27ae60'},
        {'name': 'Integrated Sensing\n& Communication\n(ISAC)', 'angle': 315, 'color': '#f39c12'},
        {'name': 'Digital Twin\n& Holographic\nCommunication', 'angle': 270, 'color': '#9b59b6'},
        {'name': 'Cooperative\nIntelligence &\nSwarm V2X', 'angle': 225, 'color': '#e67e22'},
        {'name': 'Non-Terrestrial\nNetworks\n(LEO/HAPs)', 'angle': 180, 'color': '#1abc9c'},
        {'name': 'Sub-ms Latency\n& Extreme\nReliability', 'angle': 135, 'color': '#c0392b'},
    ]
    
    radius = 4.0
    for tech in technologies:
        angle_rad = np.radians(tech['angle'])
        x = 6 + radius * np.cos(angle_rad)
        y = 6 + radius * np.sin(angle_rad)
        
        # Node box
        rect = FancyBboxPatch((x-1.2, y-0.7), 2.4, 1.4, boxstyle="round,pad=0.1",
                              facecolor=tech['color'], alpha=0.15, edgecolor=tech['color'], linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, y, tech['name'], ha='center', va='center', fontsize=7.5, color='#333')
        
        # Connection line to center
        x_end = 6 + 1.6 * np.cos(angle_rad)
        y_end = 6 + 1.6 * np.sin(angle_rad)
        x_start = x - 1.0 * np.cos(angle_rad)
        y_start = y - 0.6 * np.sin(angle_rad)
        ax.plot([x_end, x - (x-6)*0.3], [y_end, y - (y-6)*0.3], 
                color=tech['color'], linewidth=1.5, alpha=0.6, linestyle='--')
    
    # KPIs at corners
    kpis = [
        {'text': 'Peak Rate: > 1 Tbps', 'pos': (1, 11.2)},
        {'text': 'Latency: < 0.1 ms', 'pos': (1, 10.7)},
        {'text': 'Reliability: 99.99999%', 'pos': (8, 11.2)},
        {'text': 'Positioning: < 1 cm', 'pos': (8, 10.7)},
        {'text': 'Connection Density: 10^7/km²', 'pos': (1, 0.8)},
        {'text': 'Mobility: > 1000 km/h', 'pos': (8, 0.8)},
    ]
    
    for kpi in kpis:
        ax.text(kpi['pos'][0], kpi['pos'][1], kpi['text'], fontsize=8.5, 
                fontweight='bold', color='#2c3e50',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#f8f9fa', edgecolor='#bdc3c7'))
    
    plt.tight_layout()
    plt.savefig('/projects/sandbox/AMMAN/v2x_figures/Figure_4_6G_V2X_Vision.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 4 created successfully")

# Generate all figures
create_figure1()
create_figure2()
create_figure3()
create_figure4()
print("\nAll 4 figures generated successfully!")
