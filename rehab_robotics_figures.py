"""
Generate 4 professional figures for the Rehabilitation Robotics Book Chapter
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

# Set global style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11

# ============================================================
# FIGURE 1: Timeline/Evolution of Rehabilitation Robotics
# ============================================================
def create_figure1():
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    
    # Timeline data
    years = [1960, 1970, 1980, 1990, 2000, 2010, 2020, 2025]
    milestones = [
        "Early Prosthetics\n& Powered Orthoses",
        "First Robotic Arms\nfor Disabled Users",
        "MIT-Manus\nDevelopment Begins",
        "Clinical Trials of\nRobotic Therapy",
        "Exoskeletons &\nLokomat Introduced",
        "AI & Sensor\nIntegration Era",
        "Soft Robotics &\nBCI Interfaces",
        "Cloud Robotics &\nDigital Twins"
    ]
    
    colors = ['#1a5276', '#1f618d', '#2471a3', '#2e86c1', '#3498db', '#5dade2', '#85c1e9', '#aed6f1']
    
    # Draw timeline
    ax.plot([1955, 2030], [0, 0], 'k-', linewidth=2, zorder=1)
    
    for i, (year, milestone, color) in enumerate(zip(years, milestones, colors)):
        # Alternate above and below
        y_pos = 1.5 if i % 2 == 0 else -1.5
        
        # Draw vertical line
        ax.plot([year, year], [0, y_pos * 0.6], color=color, linewidth=2, zorder=2)
        
        # Draw circle on timeline
        ax.scatter(year, 0, s=120, color=color, zorder=3, edgecolors='black', linewidths=0.5)
        
        # Add text box
        bbox_props = dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.15, edgecolor=color)
        ax.text(year, y_pos, milestone, ha='center', va='center', fontsize=8.5,
                fontweight='bold', bbox=bbox_props, color='#1a1a1a')
        
        # Add year label
        y_label = 0.8 if i % 2 == 0 else -0.8
        ax.text(year, y_label, str(year), ha='center', va='center', fontsize=9, fontweight='bold', color=color)
    
    ax.set_xlim(1955, 2030)
    ax.set_ylim(-3, 3)
    ax.axis('off')
    ax.set_title('Figure 1: Historical Evolution and Major Milestones in Rehabilitation Robotics', 
                 fontsize=13, fontweight='bold', pad=20)
    
    # Add era labels
    ax.annotate('', xy=(1995, -2.7), xytext=(1958, -2.7),
                arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=1.5))
    ax.text(1976, -2.9, 'Early Development Era', ha='center', fontsize=9, style='italic', color='#2c3e50')
    
    ax.annotate('', xy=(2028, -2.7), xytext=(1998, -2.7),
                arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=1.5))
    ax.text(2013, -2.9, 'Modern Intelligent Rehabilitation Era', ha='center', fontsize=9, style='italic', color='#2c3e50')
    
    plt.tight_layout()
    plt.savefig('/projects/sandbox/AMMAN/rehab_figures/Figure_1_Evolution_Timeline.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 1 created successfully.")


# ============================================================
# FIGURE 2: Classification of Rehabilitation Robots
# ============================================================
def create_figure2():
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.axis('off')
    
    # Central node
    central = FancyBboxPatch((5.5, 6.8), 3, 0.8, boxstyle="round,pad=0.1",
                              facecolor='#1a5276', edgecolor='#0d2f4a', linewidth=2)
    ax.add_patch(central)
    ax.text(7, 7.2, 'Rehabilitation\nRobots', ha='center', va='center', fontsize=12,
            fontweight='bold', color='white')
    
    # Category 1: By Function
    categories = {
        'By Function': {
            'pos': (1.5, 4.5), 'color': '#2e86c1',
            'items': ['Therapeutic\nRobots', 'Assistive\nRobots', 'Prosthetic\nDevices']
        },
        'By Anatomy': {
            'pos': (5.5, 4.5), 'color': '#28b463',
            'items': ['Upper Limb', 'Lower Limb', 'Full Body\n/Trunk']
        },
        'By Mechanism': {
            'pos': (9.5, 4.5), 'color': '#d35400',
            'items': ['End-Effector\nBased', 'Exoskeleton\nBased', 'Soft Robotic\nSystems']
        },
        'By Intelligence': {
            'pos': (13, 4.5), 'color': '#8e44ad',
            'items': ['Passive\n(Pre-programmed)', 'Active\n(Adaptive/AI)', 'Hybrid\nSystems']
        }
    }
    
    for cat_name, cat_data in categories.items():
        x, y = cat_data['pos']
        color = cat_data['color']
        
        # Category box
        cat_box = FancyBboxPatch((x - 1.2, y - 0.4), 2.4, 0.8, boxstyle="round,pad=0.1",
                                  facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.85)
        ax.add_patch(cat_box)
        ax.text(x, y, cat_name, ha='center', va='center', fontsize=10,
                fontweight='bold', color='white')
        
        # Connection to central
        ax.annotate('', xy=(x, y + 0.4), xytext=(7, 6.8),
                    arrowprops=dict(arrowstyle='->', color='#555555', lw=1.5,
                                    connectionstyle='arc3,rad=-0.1'))
        
        # Sub-items
        for j, item in enumerate(cat_data['items']):
            item_y = y - 1.2 - j * 1.0
            item_box = FancyBboxPatch((x - 1.0, item_y - 0.35), 2.0, 0.7,
                                       boxstyle="round,pad=0.1",
                                       facecolor=color, edgecolor=color, linewidth=1, alpha=0.2)
            ax.add_patch(item_box)
            ax.text(x, item_y, item, ha='center', va='center', fontsize=8.5, color='#1a1a1a')
            
            # Connection line
            ax.plot([x, x], [y - 0.4, item_y + 0.35], color=color, linewidth=1, alpha=0.5, linestyle='--')
    
    ax.set_xlim(-0.5, 15.5)
    ax.set_ylim(0.5, 8.5)
    ax.set_title('Figure 2: Classification of Rehabilitation Robotic Systems',
                 fontsize=13, fontweight='bold', pad=10)
    
    plt.tight_layout()
    plt.savefig('/projects/sandbox/AMMAN/rehab_figures/Figure_2_Classification.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 2 created successfully.")


# ============================================================
# FIGURE 3: Enabling Technologies Architecture
# ============================================================
def create_figure3():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.axis('off')
    
    # Layer architecture - bottom to top
    layers = [
        {'name': 'Sensing Layer', 'y': 1.0, 'color': '#1a5276',
         'items': ['Force/Torque\nSensors', 'IMU & Motion\nCapture', 'EMG/EEG\nSensors', 'Vision\nSystems']},
        {'name': 'Control Layer', 'y': 2.8, 'color': '#2e86c1',
         'items': ['PID/Impedance\nControl', 'Adaptive\nControl', 'Force\nFeedback', 'Safety\nMonitoring']},
        {'name': 'Intelligence Layer', 'y': 4.6, 'color': '#28b463',
         'items': ['Machine\nLearning', 'Computer\nVision', 'Natural Language\nProcessing', 'Predictive\nAnalytics']},
        {'name': 'Connectivity Layer', 'y': 6.4, 'color': '#d35400',
         'items': ['IoMT\nProtocols', 'Cloud\nComputing', 'Edge\nComputing', '5G/WiFi\nNetworks']},
        {'name': 'Application Layer', 'y': 8.2, 'color': '#8e44ad',
         'items': ['VR/AR\nTherapy', 'Telerehab\nPlatforms', 'Clinical\nDSS', 'Patient\nDashboard']},
    ]
    
    for layer in layers:
        y = layer['y']
        color = layer['color']
        
        # Main layer bar
        bar = FancyBboxPatch((0.5, y - 0.3), 11, 1.4, boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.15)
        ax.add_patch(bar)
        
        # Layer name on left
        ax.text(0.3, y + 0.35, layer['name'], ha='right', va='center', fontsize=10,
                fontweight='bold', color=color, rotation=0,
                transform=ax.transData)
        
        # Sub-items
        x_positions = [2.0, 4.5, 7.0, 9.5]
        for j, (x, item) in enumerate(zip(x_positions, layer['items'])):
            item_box = FancyBboxPatch((x - 0.8, y - 0.1), 1.8, 0.9, boxstyle="round,pad=0.1",
                                       facecolor=color, edgecolor=color, linewidth=1.2, alpha=0.75)
            ax.add_patch(item_box)
            ax.text(x + 0.1, y + 0.35, item, ha='center', va='center', fontsize=8,
                    fontweight='bold', color='white')
    
    # Arrows between layers
    for i in range(len(layers) - 1):
        y_from = layers[i]['y'] + 0.8
        y_to = layers[i+1]['y'] - 0.1
        for x in [3.0, 5.5, 8.0, 10.5]:
            ax.annotate('', xy=(x, y_to), xytext=(x, y_from),
                        arrowprops=dict(arrowstyle='->', color='#666666', lw=1.2))
    
    # Side label
    ax.annotate('', xy=(11.8, 8.5), xytext=(11.8, 1.0),
                arrowprops=dict(arrowstyle='<->', color='#2c3e50', lw=2))
    ax.text(12.2, 4.8, 'Data Flow &\nIntegration', ha='center', va='center', fontsize=9,
            fontweight='bold', color='#2c3e50', rotation=90)
    
    ax.set_xlim(-1.5, 13)
    ax.set_ylim(0.2, 9.5)
    ax.set_title('Figure 3: Layered Architecture of Enabling Technologies for Intelligent Rehabilitation',
                 fontsize=12, fontweight='bold', pad=10)
    
    plt.tight_layout()
    plt.savefig('/projects/sandbox/AMMAN/rehab_figures/Figure_3_Enabling_Technologies.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 3 created successfully.")


# ============================================================
# FIGURE 4: Future Directions and Emerging Trends
# ============================================================
def create_figure4():
    fig, ax = plt.subplots(1, 1, figsize=(11, 9))
    ax.axis('off')
    
    # Central hub
    circle = plt.Circle((5.5, 5), 1.2, color='#1a5276', alpha=0.9, zorder=5)
    ax.add_patch(circle)
    ax.text(5.5, 5, 'Future of\nRehabilitation\nRobotics', ha='center', va='center',
            fontsize=11, fontweight='bold', color='white', zorder=6)
    
    # Surrounding trends
    trends = [
        {'label': 'Soft Robotics &\nBio-inspired\nDesign', 'angle': 90, 'color': '#2e86c1'},
        {'label': 'Digital Twins &\nSimulation\nPlatforms', 'angle': 45, 'color': '#28b463'},
        {'label': 'Cloud &\nEdge Robotic\nSystems', 'angle': 0, 'color': '#d35400'},
        {'label': 'AI-Driven\nPersonalized\nTherapy', 'angle': 315, 'color': '#8e44ad'},
        {'label': 'Home-Based\nAutonomous\nRehabilitation', 'angle': 270, 'color': '#c0392b'},
        {'label': 'Brain-Computer\nInterface\nIntegration', 'angle': 225, 'color': '#16a085'},
        {'label': 'Collaborative\nRobots\n(Cobots)', 'angle': 180, 'color': '#f39c12'},
        {'label': 'Wearable\nSensor\nEcosystems', 'angle': 135, 'color': '#7d3c98'},
    ]
    
    radius = 3.2
    for trend in trends:
        angle_rad = np.radians(trend['angle'])
        x = 5.5 + radius * np.cos(angle_rad)
        y = 5 + radius * np.sin(angle_rad)
        
        # Connection line
        ax.plot([5.5, x], [5, y], color=trend['color'], linewidth=2, alpha=0.6, zorder=2)
        
        # Trend circle
        trend_circle = plt.Circle((x, y), 0.85, color=trend['color'], alpha=0.8, zorder=4)
        ax.add_patch(trend_circle)
        ax.text(x, y, trend['label'], ha='center', va='center', fontsize=7.5,
                fontweight='bold', color='white', zorder=5)
    
    # Outer ring labels for impact areas
    impact_areas = ['Patient Outcomes', 'Cost Reduction', 'Accessibility', 'Clinical Efficiency']
    impact_angles = [60, 150, 240, 330]
    
    for area, angle in zip(impact_areas, impact_angles):
        angle_rad = np.radians(angle)
        x = 5.5 + 4.5 * np.cos(angle_rad)
        y = 5 + 4.0 * np.sin(angle_rad)
        ax.text(x, y, area, ha='center', va='center', fontsize=9,
                style='italic', color='#2c3e50',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#ecf0f1', edgecolor='#bdc3c7'))
    
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 10)
    ax.set_title('Figure 4: Emerging Trends and Future Directions in Rehabilitation Robotics',
                 fontsize=12, fontweight='bold', pad=15)
    
    plt.tight_layout()
    plt.savefig('/projects/sandbox/AMMAN/rehab_figures/Figure_4_Future_Directions.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 4 created successfully.")


# Create output directory and generate all figures
import os
os.makedirs('/projects/sandbox/AMMAN/rehab_figures', exist_ok=True)

create_figure1()
create_figure2()
create_figure3()
create_figure4()
print("\nAll 4 figures generated successfully!")
