#!/usr/bin/env python3
"""
Generate professional figures for the book chapter:
Optimal Sizing and Placement of Energy Storage Systems in HRES
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, ArrowStyle
import numpy as np
import os

# Create output directory
output_dir = "ESS_chapter_figures"
os.makedirs(output_dir, exist_ok=True)

# Set global style
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
    'savefig.bbox': 'tight'
})


# ============================================================
# FIGURE 1: Typical HRES Architecture with ESS Integration
# ============================================================
def create_figure1():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Figure 1: Typical HRES Architecture with Energy Storage Integration',
                 fontsize=13, fontweight='bold', pad=15)

    # Color scheme
    colors = {
        'solar': '#FFB300', 'wind': '#1E88E5', 'diesel': '#757575',
        'battery': '#43A047', 'bus_dc': '#E53935', 'bus_ac': '#8E24AA',
        'load': '#FF6F00', 'grid': '#00695C', 'converter': '#5D4037'
    }

    # DC Bus
    ax.plot([4.5, 4.5], [1.5, 6.5], color=colors['bus_dc'], linewidth=4, solid_capstyle='round')
    ax.text(4.5, 6.8, 'DC Bus', ha='center', fontsize=10, fontweight='bold', color=colors['bus_dc'])

    # AC Bus
    ax.plot([8.5, 8.5], [1.5, 6.5], color=colors['bus_ac'], linewidth=4, solid_capstyle='round')
    ax.text(8.5, 6.8, 'AC Bus', ha='center', fontsize=10, fontweight='bold', color=colors['bus_ac'])

    # Solar PV
    box = FancyBboxPatch((0.5, 5.5), 2.5, 1.2, boxstyle="round,pad=0.1",
                         facecolor=colors['solar'], alpha=0.3, edgecolor=colors['solar'], linewidth=2)
    ax.add_patch(box)
    ax.text(1.75, 6.1, 'Solar PV\nArray', ha='center', va='center', fontsize=9, fontweight='bold')
    ax.annotate('', xy=(4.3, 6.1), xytext=(3.1, 6.1),
                arrowprops=dict(arrowstyle='->', color=colors['solar'], lw=2))

    # Wind Turbine
    box = FancyBboxPatch((0.5, 3.8), 2.5, 1.2, boxstyle="round,pad=0.1",
                         facecolor=colors['wind'], alpha=0.3, edgecolor=colors['wind'], linewidth=2)
    ax.add_patch(box)
    ax.text(1.75, 4.4, 'Wind\nTurbine', ha='center', va='center', fontsize=9, fontweight='bold')
    ax.annotate('', xy=(4.3, 4.4), xytext=(3.1, 4.4),
                arrowprops=dict(arrowstyle='->', color=colors['wind'], lw=2))

    # Battery ESS
    box = FancyBboxPatch((0.5, 2.0), 2.5, 1.2, boxstyle="round,pad=0.1",
                         facecolor=colors['battery'], alpha=0.3, edgecolor=colors['battery'], linewidth=2)
    ax.add_patch(box)
    ax.text(1.75, 2.6, 'Battery\nESS', ha='center', va='center', fontsize=9, fontweight='bold')
    ax.annotate('', xy=(4.3, 2.6), xytext=(3.1, 2.6),
                arrowprops=dict(arrowstyle='<->', color=colors['battery'], lw=2))

    # Bidirectional Converter (DC-AC)
    box = FancyBboxPatch((5.8, 3.5), 1.8, 1.5, boxstyle="round,pad=0.1",
                         facecolor=colors['converter'], alpha=0.2, edgecolor=colors['converter'], linewidth=2)
    ax.add_patch(box)
    ax.text(6.7, 4.25, 'Bi-directional\nDC/AC\nConverter', ha='center', va='center', fontsize=8, fontweight='bold')
    ax.annotate('', xy=(5.7, 4.25), xytext=(4.7, 4.25),
                arrowprops=dict(arrowstyle='<->', color=colors['converter'], lw=2))
    ax.annotate('', xy=(8.3, 4.25), xytext=(7.7, 4.25),
                arrowprops=dict(arrowstyle='<->', color=colors['converter'], lw=2))

    # AC Loads
    box = FancyBboxPatch((9.8, 5.2), 2.0, 1.2, boxstyle="round,pad=0.1",
                         facecolor=colors['load'], alpha=0.3, edgecolor=colors['load'], linewidth=2)
    ax.add_patch(box)
    ax.text(10.8, 5.8, 'AC Loads\n(Residential/\nIndustrial)', ha='center', va='center', fontsize=8, fontweight='bold')
    ax.annotate('', xy=(9.7, 5.8), xytext=(8.7, 5.8),
                arrowprops=dict(arrowstyle='->', color=colors['load'], lw=2))

    # Utility Grid
    box = FancyBboxPatch((9.8, 3.3), 2.0, 1.2, boxstyle="round,pad=0.1",
                         facecolor=colors['grid'], alpha=0.3, edgecolor=colors['grid'], linewidth=2)
    ax.add_patch(box)
    ax.text(10.8, 3.9, 'Utility\nGrid', ha='center', va='center', fontsize=9, fontweight='bold')
    ax.annotate('', xy=(9.7, 3.9), xytext=(8.7, 3.9),
                arrowprops=dict(arrowstyle='<->', color=colors['grid'], lw=2))

    # Diesel Generator
    box = FancyBboxPatch((9.8, 1.5), 2.0, 1.2, boxstyle="round,pad=0.1",
                         facecolor=colors['diesel'], alpha=0.3, edgecolor=colors['diesel'], linewidth=2)
    ax.add_patch(box)
    ax.text(10.8, 2.1, 'Diesel\nGenerator', ha='center', va='center', fontsize=9, fontweight='bold')
    ax.annotate('', xy=(8.7, 2.1), xytext=(9.7, 2.1),
                arrowprops=dict(arrowstyle='->', color=colors['diesel'], lw=2))

    # EMS Controller
    box = FancyBboxPatch((5.5, 0.3), 2.2, 1.0, boxstyle="round,pad=0.1",
                         facecolor='#BBDEFB', alpha=0.5, edgecolor='#1565C0', linewidth=2, linestyle='--')
    ax.add_patch(box)
    ax.text(6.6, 0.8, 'Energy Management\nSystem (EMS)', ha='center', va='center', fontsize=8, fontweight='bold', color='#1565C0')

    # Dashed control lines from EMS
    for target_y in [2.6, 4.25, 5.8]:
        ax.plot([6.6, 6.6], [1.3, target_y - 0.3], color='#1565C0', linewidth=0.8, linestyle=':', alpha=0.5)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_1_HRES_Architecture.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 1 created: HRES Architecture")


# ============================================================
# FIGURE 2: Classification of Energy Storage Technologies
# ============================================================
def create_figure2():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    # Data for storage technologies (Power MW vs Discharge Duration hours)
    technologies = {
        'Supercapacitors': {'power': (0.001, 1), 'duration': (0.001, 0.05), 'color': '#E91E63'},
        'Flywheels': {'power': (0.01, 10), 'duration': (0.01, 0.25), 'color': '#9C27B0'},
        'Li-ion Batteries': {'power': (0.01, 100), 'duration': (0.5, 6), 'color': '#2196F3'},
        'Lead-Acid': {'power': (0.01, 50), 'duration': (0.5, 4), 'color': '#607D8B'},
        'Flow Batteries': {'power': (0.1, 100), 'duration': (2, 12), 'color': '#4CAF50'},
        'NaS Batteries': {'power': (1, 100), 'duration': (4, 8), 'color': '#FF9800'},
        'CAES': {'power': (10, 1000), 'duration': (4, 24), 'color': '#795548'},
        'Pumped Hydro': {'power': (100, 10000), 'duration': (6, 24), 'color': '#00BCD4'},
        'Hydrogen': {'power': (0.1, 1000), 'duration': (24, 500), 'color': '#CDDC39'},
    }

    ax.set_xscale('log')
    ax.set_yscale('log')

    for tech, params in technologies.items():
        x_min, x_max = params['power']
        y_min, y_max = params['duration']
        width = x_max - x_min
        height = y_max - y_min

        rect = plt.Rectangle((x_min, y_min), width, height,
                            alpha=0.35, facecolor=params['color'],
                            edgecolor=params['color'], linewidth=2)
        ax.add_patch(rect)

        # Label position
        x_label = np.sqrt(x_min * x_max)
        y_label = np.sqrt(y_min * y_max)
        ax.text(x_label, y_label, tech, ha='center', va='center',
                fontsize=8, fontweight='bold', color='black',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7))

    # Application zones
    ax.axhspan(0.001, 0.1, alpha=0.05, color='red')
    ax.axhspan(0.1, 4, alpha=0.05, color='yellow')
    ax.axhspan(4, 600, alpha=0.05, color='green')

    ax.text(0.0015, 0.02, 'Power Quality\n(seconds-minutes)', fontsize=8, fontstyle='italic', color='red', alpha=0.8)
    ax.text(0.0015, 1, 'Energy Management\n(minutes-hours)', fontsize=8, fontstyle='italic', color='#B8860B', alpha=0.8)
    ax.text(0.0015, 50, 'Bulk Storage\n(hours-days)', fontsize=8, fontstyle='italic', color='green', alpha=0.8)

    ax.set_xlim(0.001, 15000)
    ax.set_ylim(0.001, 600)
    ax.set_xlabel('Rated Power (MW)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Discharge Duration (hours)', fontsize=11, fontweight='bold')
    ax.set_title('Figure 2: Classification of Energy Storage Technologies by Power Rating and Duration',
                 fontsize=12, fontweight='bold', pad=15)
    ax.grid(True, which='both', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_2_ESS_Classification.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 2 created: ESS Classification")


# ============================================================
# FIGURE 3: Optimization Framework for ESS Sizing
# ============================================================
def create_figure3():
    fig, ax = plt.subplots(1, 1, figsize=(13, 9))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_title('Figure 3: Comprehensive Optimization Framework for ESS Sizing in HRES',
                 fontsize=13, fontweight='bold', pad=15)

    def draw_box(ax, x, y, w, h, text, color, fontsize=8):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                            facecolor=color, alpha=0.3, edgecolor=color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', wrap=True)

    # Input Data Layer (top)
    ax.text(6.5, 8.5, 'INPUT DATA', ha='center', fontsize=11, fontweight='bold', color='#1565C0')
    inputs = [('Solar\nIrradiance', 0.5), ('Wind\nSpeed', 2.5), ('Load\nDemand', 4.5),
              ('Economic\nParameters', 6.5), ('Component\nSpecs', 8.5), ('Grid\nTariffs', 10.5)]
    for text, x in inputs:
        draw_box(ax, x, 7.5, 1.6, 0.9, text, '#1E88E5', 7)

    # Arrows down
    for x in [1.3, 3.3, 5.3, 7.3, 9.3, 11.3]:
        ax.annotate('', xy=(x, 7.3), xytext=(x, 7.5),
                    arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))

    # System Models Layer
    ax.text(6.5, 7.0, 'SYSTEM MODELS', ha='center', fontsize=11, fontweight='bold', color='#2E7D32')
    models = [('PV Generation\nModel', 1.0), ('Wind Power\nModel', 3.5),
              ('Battery\nDegradation\nModel', 6.0), ('Power Flow\nModel', 8.5), ('Economic\nModel', 11.0)]
    for text, x in models:
        draw_box(ax, x, 5.8, 2.0, 1.0, text, '#43A047', 7)

    # Arrows down
    for x in [2.0, 4.5, 7.0, 9.5, 12.0]:
        ax.annotate('', xy=(x, 5.5), xytext=(x, 5.8),
                    arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))

    # Optimization Engine (center)
    ax.text(6.5, 5.3, 'OPTIMIZATION ENGINE', ha='center', fontsize=11, fontweight='bold', color='#BF360C')
    box = FancyBboxPatch((1.5, 3.5), 10.0, 1.6, boxstyle="round,pad=0.15",
                         facecolor='#FF5722', alpha=0.15, edgecolor='#BF360C', linewidth=2.5)
    ax.add_patch(box)

    opt_methods = ['MILP/NLP', 'GA/NSGA-II', 'PSO/GWO', 'DRL/ML', 'Hybrid\nMethods']
    for i, method in enumerate(opt_methods):
        x = 2.0 + i * 2.0
        ax.text(x, 4.3, method, ha='center', va='center', fontsize=8, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFCCBC', edgecolor='#BF360C', linewidth=1))

    # Arrows down
    ax.annotate('', xy=(6.5, 3.2), xytext=(6.5, 3.5),
                arrowprops=dict(arrowstyle='->', color='gray', lw=2))

    # Objective Functions & Constraints
    ax.text(3.5, 2.8, 'OBJECTIVES', ha='center', fontsize=10, fontweight='bold', color='#4A148C')
    objectives = ['Min LCOE', 'Min LPSP', 'Min Emissions', 'Max NPV']
    for i, obj in enumerate(objectives):
        draw_box(ax, 0.8 + i * 1.7, 1.8, 1.5, 0.8, obj, '#7B1FA2', 7)

    ax.text(10.0, 2.8, 'CONSTRAINTS', ha='center', fontsize=10, fontweight='bold', color='#E65100')
    constraints = ['Energy\nBalance', 'SOC\nLimits', 'Budget']
    for i, con in enumerate(constraints):
        draw_box(ax, 8.0 + i * 1.7, 1.8, 1.5, 0.8, con, '#E65100', 7)

    # Output Layer (bottom)
    ax.text(6.5, 1.3, 'OPTIMAL DESIGN OUTPUTS', ha='center', fontsize=11, fontweight='bold', color='#1B5E20')
    outputs = ['ESS\nCapacity\n(kWh)', 'Power\nRating\n(kW)', 'Technology\nSelection', 'Placement\nLocation']
    for i, out in enumerate(outputs):
        draw_box(ax, 1.5 + i * 2.8, 0.1, 2.2, 1.0, out, '#1B5E20', 7)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_3_Optimization_Framework.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 3 created: Optimization Framework")


# ============================================================
# FIGURE 4: Grid-Connected and Standalone HRES Architectures
# ============================================================
def create_figure4():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # --- Left: Grid-Connected Architecture ---
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('(a) Grid-Connected HRES', fontsize=11, fontweight='bold', pad=10)

    def draw_component(ax, x, y, w, h, text, color):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                            facecolor=color, alpha=0.3, edgecolor=color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=7, fontweight='bold')

    # Grid-connected components
    draw_component(ax1, 0.5, 8.0, 2.0, 1.2, 'Solar PV\n5 MW', '#FFB300')
    draw_component(ax1, 0.5, 6.0, 2.0, 1.2, 'Wind Farm\n3 MW', '#1E88E5')
    draw_component(ax1, 0.5, 4.0, 2.0, 1.2, 'ESS-1\n(Li-ion)\n2 MWh', '#43A047')
    draw_component(ax1, 0.5, 2.0, 2.0, 1.2, 'ESS-2\n(Flow)\n4 MWh', '#009688')

    # Main bus
    ax1.plot([4.0, 4.0], [1.5, 9.0], color='#E53935', linewidth=3)
    ax1.text(4.0, 9.3, 'Distribution\nBus', ha='center', fontsize=8, fontweight='bold', color='#E53935')

    # Connections to bus
    for y in [8.6, 6.6, 4.6, 2.6]:
        ax1.plot([2.6, 3.9], [y, y], color='gray', linewidth=1.5)

    # Substation & Grid
    draw_component(ax1, 5.5, 7.5, 2.2, 1.2, 'Substation\nTransformer', '#5D4037')
    ax1.plot([4.1, 5.4], [8.1, 8.1], color='gray', linewidth=1.5)

    draw_component(ax1, 8.2, 7.5, 1.5, 1.2, 'Utility\nGrid', '#00695C')
    ax1.plot([7.8, 8.1], [8.1, 8.1], color='gray', linewidth=1.5)

    # Loads at different buses
    draw_component(ax1, 5.5, 5.5, 2.0, 1.0, 'Industrial\nLoad (2MW)', '#FF6F00')
    ax1.plot([4.1, 5.4], [6.0, 6.0], color='gray', linewidth=1.5)

    draw_component(ax1, 5.5, 3.8, 2.0, 1.0, 'Residential\nLoad (1MW)', '#FF6F00')
    ax1.plot([4.1, 5.4], [4.3, 4.3], color='gray', linewidth=1.5)

    draw_component(ax1, 5.5, 2.0, 2.0, 1.0, 'ESS-3\n(Behind Meter)\n1 MWh', '#43A047')
    ax1.plot([4.1, 5.4], [2.5, 2.5], color='gray', linewidth=1.5)

    # PCC label
    ax1.plot(4.0, 8.1, 'ro', markersize=8)
    ax1.text(4.4, 8.4, 'PCC', fontsize=8, color='red', fontweight='bold')

    # --- Right: Standalone Architecture ---
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('(b) Standalone (Off-Grid) HRES', fontsize=11, fontweight='bold', pad=10)

    # DC Bus (left side)
    ax2.plot([3.0, 3.0], [2.5, 8.5], color='#E53935', linewidth=3)
    ax2.text(3.0, 8.8, 'DC Bus', ha='center', fontsize=8, fontweight='bold', color='#E53935')

    # AC Bus (right side)
    ax2.plot([7.0, 7.0], [2.5, 8.5], color='#8E24AA', linewidth=3)
    ax2.text(7.0, 8.8, 'AC Bus', ha='center', fontsize=8, fontweight='bold', color='#8E24AA')

    # DC Sources
    draw_component(ax2, 0.3, 7.2, 1.8, 1.0, 'Solar PV\n500 kW', '#FFB300')
    ax2.plot([2.2, 2.9], [7.7, 7.7], color='gray', linewidth=1.5)

    draw_component(ax2, 0.3, 5.5, 1.8, 1.0, 'Battery ESS\n800 kWh', '#43A047')
    ax2.plot([2.2, 2.9], [6.0, 6.0], color='gray', linewidth=1.5)

    draw_component(ax2, 0.3, 3.8, 1.8, 1.0, 'Supercap\n50 kW', '#E91E63')
    ax2.plot([2.2, 2.9], [4.3, 4.3], color='gray', linewidth=1.5)

    # Inverter
    draw_component(ax2, 4.2, 4.8, 1.8, 1.5, 'Bi-directional\nInverter\n(Grid-forming)', '#5D4037')
    ax2.plot([3.1, 4.1], [5.5, 5.5], color='gray', linewidth=1.5)
    ax2.plot([6.1, 6.9], [5.5, 5.5], color='gray', linewidth=1.5)

    # AC Sources & Loads
    draw_component(ax2, 8.0, 7.2, 1.8, 1.0, 'Wind\nTurbine\n350 kW', '#1E88E5')
    ax2.plot([7.1, 7.9], [7.7, 7.7], color='gray', linewidth=1.5)

    draw_component(ax2, 8.0, 5.5, 1.8, 1.0, 'Diesel Gen\n200 kW', '#757575')
    ax2.plot([7.1, 7.9], [6.0, 6.0], color='gray', linewidth=1.5)

    draw_component(ax2, 8.0, 3.8, 1.8, 1.0, 'Critical\nLoad', '#FF6F00')
    ax2.plot([7.1, 7.9], [4.3, 4.3], color='gray', linewidth=1.5)

    draw_component(ax2, 8.0, 2.2, 1.8, 1.0, 'Non-Critical\nLoad', '#FF8F00')
    ax2.plot([7.1, 7.9], [2.7, 2.7], color='gray', linewidth=1.5)

    # EMS
    draw_component(ax2, 3.8, 1.2, 2.5, 0.9, 'Microgrid EMS\nController', '#1565C0')

    fig.suptitle('Figure 4: HRES Architectures with ESS Placement Options',
                 fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_4_HRES_Architectures.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 4 created: HRES Architectures")


# ============================================================
# FIGURE 5: Digital Twin Ecosystem for ESS Deployment
# ============================================================
def create_figure5():
    fig, ax = plt.subplots(1, 1, figsize=(13, 9))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_title('Figure 5: Integrated Digital Ecosystem for ESS Deployment and Management',
                 fontsize=13, fontweight='bold', pad=15)

    def draw_layer_box(ax, x, y, w, h, text, color, fontsize=8):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                            facecolor=color, alpha=0.25, edgecolor=color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center',
                fontsize=fontsize, fontweight='bold')

    # Layer 1: Physical Assets (bottom)
    ax.text(6.5, 0.9, 'PHYSICAL LAYER', ha='center', fontsize=10, fontweight='bold', color='#37474F')
    physical_items = [('Solar PV\nArrays', 1.0), ('Wind\nTurbines', 3.2),
                      ('Battery\nESS', 5.4), ('Power\nConverters', 7.6), ('Grid\nConnection', 9.8)]
    for text, x in physical_items:
        draw_layer_box(ax, x, 0.1, 1.8, 0.7, text, '#607D8B', 7)

    # Layer 2: IoT & Sensing
    ax.text(6.5, 2.3, 'IoT SENSING & COMMUNICATION LAYER', ha='center', fontsize=10, fontweight='bold', color='#1565C0')
    iot_items = [('Voltage/Current\nSensors', 0.5), ('Temperature\nSensors', 2.8),
                 ('Smart\nMeters', 5.1), ('Weather\nStations', 7.4), ('Edge\nComputing', 9.7)]
    for text, x in iot_items:
        draw_layer_box(ax, x, 1.5, 1.9, 0.7, text, '#1E88E5', 7)

    # Arrows between layers
    for x in [1.9, 4.1, 6.3, 8.5, 10.7]:
        ax.annotate('', xy=(x, 1.5), xytext=(x, 0.85),
                    arrowprops=dict(arrowstyle='->', color='gray', lw=1))

    # Layer 3: Digital Twin Platform
    ax.text(6.5, 4.3, 'DIGITAL TWIN PLATFORM', ha='center', fontsize=10, fontweight='bold', color='#2E7D32')
    box = FancyBboxPatch((0.8, 2.7), 11.4, 1.4, boxstyle="round,pad=0.15",
                         facecolor='#43A047', alpha=0.1, edgecolor='#2E7D32', linewidth=2)
    ax.add_patch(box)

    dt_items = [('Electrochemical\nModel', 1.2), ('Thermal\nModel', 3.4),
                ('Degradation\nModel', 5.6), ('Power Flow\nSimulation', 7.8), ('Economic\nModel', 10.0)]
    for text, x in dt_items:
        draw_layer_box(ax, x, 2.9, 1.9, 0.9, text, '#2E7D32', 7)

    # Arrows up
    for x in [2.1, 4.3, 6.5, 8.7, 10.9]:
        ax.annotate('', xy=(x, 2.9), xytext=(x, 2.25),
                    arrowprops=dict(arrowstyle='->', color='gray', lw=1))

    # Layer 4: Analytics & AI
    ax.text(6.5, 6.0, 'PREDICTIVE ANALYTICS & AI LAYER', ha='center', fontsize=10, fontweight='bold', color='#BF360C')
    ai_items = [('SOH\nEstimation', 1.0), ('Remaining\nUseful Life\nPrediction', 3.3),
                ('Renewable\nForecasting', 5.6), ('Anomaly\nDetection', 7.9), ('Optimal\nScheduling', 10.2)]
    for text, x in ai_items:
        draw_layer_box(ax, x, 4.6, 2.0, 1.0, text, '#E65100', 7)

    # Arrows
    for x in [2.0, 4.3, 6.6, 8.9, 11.2]:
        ax.annotate('', xy=(x, 4.6), xytext=(x, 4.15),
                    arrowprops=dict(arrowstyle='->', color='gray', lw=1))

    # Layer 5: Decision & Control
    ax.text(6.5, 7.7, 'INTELLIGENT DECISION & CONTROL LAYER', ha='center', fontsize=10, fontweight='bold', color='#4A148C')
    decision_items = [('Model Predictive\nControl', 1.5), ('Deep RL\nAgent', 4.2),
                      ('Energy\nManagement\nSystem', 6.9), ('Market\nBidding\nStrategy', 9.6)]
    for text, x in decision_items:
        draw_layer_box(ax, x, 6.2, 2.2, 1.2, text, '#7B1FA2', 7)

    # Arrows
    for x in [2.6, 5.3, 8.0, 10.7]:
        ax.annotate('', xy=(x, 6.2), xytext=(x, 5.65),
                    arrowprops=dict(arrowstyle='->', color='gray', lw=1))

    # Feedback loop arrow
    ax.annotate('', xy=(12.2, 0.5), xytext=(12.2, 7.4),
                arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=2, linestyle='dashed'))
    ax.text(12.5, 4.0, 'Feedback\nLoop', ha='center', fontsize=8, color='#D32F2F', rotation=90)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_5_Digital_Ecosystem.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 5 created: Digital Ecosystem")


# ============================================================
# FIGURE 6: Future Research Roadmap for ESS in HRES
# ============================================================
def create_figure6():
    fig, ax = plt.subplots(1, 1, figsize=(13, 8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Figure 6: Research Roadmap and Technology Evolution for ESS in HRES (2024-2035)',
                 fontsize=12, fontweight='bold', pad=15)

    # Timeline
    years = ['2024', '2026', '2028', '2030', '2032', '2035']
    x_positions = [1.5, 3.5, 5.5, 7.5, 9.5, 11.5]

    ax.plot([1.0, 12.0], [4.0, 4.0], color='#37474F', linewidth=3)
    for x, year in zip(x_positions, years):
        ax.plot(x, 4.0, 'o', color='#37474F', markersize=10)
        ax.text(x, 3.5, year, ha='center', fontsize=9, fontweight='bold')

    # Technology Track (top)
    ax.text(0.3, 7.2, 'Technology\nEvolution', ha='center', fontsize=9, fontweight='bold',
            color='#1565C0', rotation=0)
    tech_items = [
        (1.5, 'Li-ion\nDominance'),
        (3.5, 'Solid-State\nBatteries'),
        (5.5, 'Na-ion\nCommercial'),
        (7.5, 'Li-S\nMature'),
        (9.5, 'Quantum\nBatteries'),
        (11.5, 'Multi-Physics\nStorage')
    ]
    for x, text in tech_items:
        box = FancyBboxPatch((x-0.8, 5.8), 1.6, 1.0, boxstyle="round,pad=0.08",
                            facecolor='#1E88E5', alpha=0.2, edgecolor='#1565C0', linewidth=1.2)
        ax.add_patch(box)
        ax.text(x, 6.3, text, ha='center', va='center', fontsize=7, fontweight='bold')
        ax.plot([x, x], [5.0, 5.8], color='#1565C0', linewidth=1, linestyle='--')

    # Methodology Track (upper middle)
    ax.text(0.3, 5.2, 'Methods', ha='center', fontsize=9, fontweight='bold', color='#2E7D32')
    method_items = [
        (1.5, 'Meta-\nheuristics'),
        (3.5, 'Deep RL\nSizing'),
        (5.5, 'Federated\nLearning'),
        (7.5, 'Quantum\nOptimization'),
        (9.5, 'Autonomous\nDesign'),
        (11.5, 'Self-Evolving\nSystems')
    ]
    for x, text in method_items:
        box = FancyBboxPatch((x-0.8, 4.4), 1.6, 0.9, boxstyle="round,pad=0.08",
                            facecolor='#43A047', alpha=0.2, edgecolor='#2E7D32', linewidth=1.2)
        ax.add_patch(box)
        ax.text(x, 4.85, text, ha='center', va='center', fontsize=7, fontweight='bold')

    # Application Track (lower middle)
    app_items = [
        (1.5, 'Behind-\nMeter'),
        (3.5, 'Community\nStorage'),
        (5.5, 'V2G\nIntegration'),
        (7.5, 'Multi-Sector\nCoupling'),
        (9.5, '100% RE\nGrids'),
        (11.5, 'Space-Based\nEnergy')
    ]
    for x, text in app_items:
        box = FancyBboxPatch((x-0.8, 2.5), 1.6, 0.9, boxstyle="round,pad=0.08",
                            facecolor='#FF9800', alpha=0.2, edgecolor='#E65100', linewidth=1.2)
        ax.add_patch(box)
        ax.text(x, 2.95, text, ha='center', va='center', fontsize=7, fontweight='bold')
        ax.plot([x, x], [3.4, 3.5], color='#E65100', linewidth=1, linestyle='--')

    ax.text(0.3, 2.9, 'Applications', ha='center', fontsize=9, fontweight='bold', color='#E65100')

    # Market Track (bottom)
    market_items = [
        (1.5, '$150/kWh'),
        (3.5, '$100/kWh'),
        (5.5, '$70/kWh'),
        (7.5, '$50/kWh'),
        (9.5, '$35/kWh'),
        (11.5, '$20/kWh')
    ]
    for x, text in market_items:
        box = FancyBboxPatch((x-0.7, 1.2), 1.4, 0.7, boxstyle="round,pad=0.08",
                            facecolor='#9C27B0', alpha=0.2, edgecolor='#6A1B9A', linewidth=1.2)
        ax.add_patch(box)
        ax.text(x, 1.55, text, ha='center', va='center', fontsize=7, fontweight='bold')

    ax.text(0.3, 1.5, 'Battery\nCost', ha='center', fontsize=9, fontweight='bold', color='#6A1B9A')

    # Legend
    legend_items = [
        ('Technology Evolution', '#1565C0'),
        ('Optimization Methods', '#2E7D32'),
        ('Applications', '#E65100'),
        ('Cost Trajectory', '#6A1B9A')
    ]
    for i, (label, color) in enumerate(legend_items):
        ax.plot(3.0 + i*2.5, 0.5, 's', color=color, markersize=10, alpha=0.5)
        ax.text(3.3 + i*2.5, 0.5, label, va='center', fontsize=8)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/Figure_6_Research_Roadmap.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Figure 6 created: Research Roadmap")


# ============================================================
# Generate all figures
# ============================================================
if __name__ == "__main__":
    print("Generating figures for ESS Chapter...")
    print("=" * 50)
    create_figure1()
    create_figure2()
    create_figure3()
    create_figure4()
    create_figure5()
    create_figure6()
    print("=" * 50)
    print(f"All figures saved to: {output_dir}/")
    print("Done!")
