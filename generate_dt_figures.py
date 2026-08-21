import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

# Set global style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

# ============================================================
# FIGURE 1: Digital Twin Architecture for Physiological Modeling
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_title('Figure 1: AI-Augmented Digital Twin Architecture for Multiscale Physiological Modeling', 
             fontsize=12, fontweight='bold', pad=20)

# Patient Data Layer (bottom)
rect1 = FancyBboxPatch((0.5, 0.5), 11, 1.2, boxstyle="round,pad=0.1", 
                        facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=2)
ax.add_patch(rect1)
ax.text(6, 1.1, 'Patient Data Layer\n(Medical Imaging | EHR | Wearable Sensors | Genomics | Lab Results)', 
        ha='center', va='center', fontsize=9, fontweight='bold')

# Computational Engine Layer (middle)
rect2 = FancyBboxPatch((0.5, 2.2), 5, 2.2, boxstyle="round,pad=0.1", 
                        facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=2)
ax.add_patch(rect2)
ax.text(3, 3.3, 'Computational Engine\n─────────────────\n• FEM/CFD Solvers\n• Multi-physics Coupling\n• Multiscale Integration', 
        ha='center', va='center', fontsize=8.5, fontweight='bold')

rect3 = FancyBboxPatch((6.5, 2.2), 5, 2.2, boxstyle="round,pad=0.1", 
                        facecolor='#FFF3E0', edgecolor='#E65100', linewidth=2)
ax.add_patch(rect3)
ax.text(9, 3.3, 'AI/ML Engine\n─────────────────\n• Deep Learning Models\n• Physics-Informed NNs\n• Reinforcement Learning', 
        ha='center', va='center', fontsize=8.5, fontweight='bold')

# Digital Twin Core (upper middle)
rect4 = FancyBboxPatch((2, 5), 8, 1.5, boxstyle="round,pad=0.1", 
                        facecolor='#F3E5F5', edgecolor='#6A1B9A', linewidth=2)
ax.add_patch(rect4)
ax.text(6, 5.75, 'Digital Twin Core: Patient-Specific Physiological Model\n(Cardiac | Respiratory | Neurological | Musculoskeletal | Metabolic)', 
        ha='center', va='center', fontsize=9.5, fontweight='bold')

# Clinical Application Layer (top)
rect5 = FancyBboxPatch((1.5, 7), 9, 0.8, boxstyle="round,pad=0.1", 
                        facecolor='#FFEBEE', edgecolor='#C62828', linewidth=2)
ax.add_patch(rect5)
ax.text(6, 7.4, 'Clinical Applications: Diagnosis | Treatment Planning | Prognosis | Precision Medicine', 
        ha='center', va='center', fontsize=9, fontweight='bold')

# Arrows
arrow_style = "Simple,tail_width=1,head_width=6,head_length=4"
ax.annotate('', xy=(6, 2.2), xytext=(6, 1.7),
            arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
ax.annotate('', xy=(6, 5.0), xytext=(6, 4.4),
            arrowprops=dict(arrowstyle='->', color='#4A148C', lw=2))
ax.annotate('', xy=(6, 7.0), xytext=(6, 6.5),
            arrowprops=dict(arrowstyle='->', color='#C62828', lw=2))

# Feedback arrows
ax.annotate('', xy=(1.0, 5.0), xytext=(1.0, 7.4),
            arrowprops=dict(arrowstyle='->', color='gray', lw=1.5, linestyle='dashed'))
ax.text(0.4, 6.2, 'Feedback\nLoop', ha='center', va='center', fontsize=7, color='gray')

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/dt_figures/Figure_1_DT_Architecture.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# FIGURE 2: Cardiovascular Digital Twin Workflow
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')
ax.set_title('Figure 2: Cardiovascular Digital Twin – From Imaging to Clinical Decision Support', 
             fontsize=12, fontweight='bold', pad=15)

# Step boxes
steps = [
    (0.5, 4.5, 2.2, 2, '#BBDEFB', '#1565C0', 'Step 1:\nMedical Imaging\n────────\n• CT/MRI\n• Echocardiography\n• Angiography'),
    (3.2, 4.5, 2.2, 2, '#C8E6C9', '#2E7D32', 'Step 2:\n3D Reconstruction\n────────\n• Segmentation\n• Mesh Generation\n• Patient-Specific\n  Geometry'),
    (5.9, 4.5, 2.2, 2, '#FFE0B2', '#E65100', 'Step 3:\nSimulation\n────────\n• Hemodynamics\n• Electrophysiology\n• Fluid-Structure\n  Interaction'),
    (8.6, 4.5, 2.8, 2, '#E1BEE7', '#6A1B9A', 'Step 4:\nAI-Driven Analysis\n────────\n• Risk Prediction\n• Treatment Optimization\n• Real-time Monitoring'),
]

for x, y, w, h, fc, ec, text in steps:
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", 
                          facecolor=fc, edgecolor=ec, linewidth=2)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=8, fontweight='bold')

# Arrows between steps
for i in range(3):
    x_start = steps[i][0] + steps[i][2]
    x_end = steps[i+1][0]
    y_mid = 5.5
    ax.annotate('', xy=(x_end, y_mid), xytext=(x_start, y_mid),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))

# Output box
rect_out = FancyBboxPatch((2, 1), 8, 2.5, boxstyle="round,pad=0.1", 
                           facecolor='#FFF9C4', edgecolor='#F57F17', linewidth=2)
ax.add_patch(rect_out)
ax.text(6, 2.25, 'Clinical Outcomes\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
        '• Personalized Cardiac Risk Score    • Virtual Surgery Planning\n'
        '• Hemodynamic Optimization           • Drug Response Prediction\n'
        '• Arrhythmia Forecasting              • Device Placement Simulation', 
        ha='center', va='center', fontsize=9)

ax.annotate('', xy=(6, 3.5), xytext=(6, 4.5),
            arrowprops=dict(arrowstyle='->', color='#F57F17', lw=2))

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/dt_figures/Figure_2_Cardiovascular_DT.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# FIGURE 3: Multi-Organ Digital Twin Integration
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(11, 9))
ax.set_xlim(0, 11)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_title('Figure 3: Whole-Body Multi-Organ Digital Twin Integration Framework', 
             fontsize=12, fontweight='bold', pad=15)

# Central hub
circle = plt.Circle((5.5, 4.5), 1.2, color='#F3E5F5', ec='#6A1B9A', linewidth=2.5)
ax.add_patch(circle)
ax.text(5.5, 4.5, 'Whole-Body\nDigital Twin\nIntegration\nHub', 
        ha='center', va='center', fontsize=9, fontweight='bold')

# Organ modules
organs = [
    (5.5, 8.0, '#BBDEFB', '#1565C0', 'Cardiac\nDigital Twin'),
    (9.0, 6.5, '#C8E6C9', '#2E7D32', 'Pulmonary\nDigital Twin'),
    (9.0, 2.5, '#FFE0B2', '#E65100', 'Neurological\nDigital Twin'),
    (5.5, 1.0, '#FFCDD2', '#C62828', 'Musculoskeletal\nDigital Twin'),
    (2.0, 2.5, '#E1BEE7', '#6A1B9A', 'Renal/Hepatic\nDigital Twin'),
    (2.0, 6.5, '#FFF9C4', '#F57F17', 'Metabolic\nDigital Twin'),
]

for x, y, fc, ec, text in organs:
    rect = FancyBboxPatch((x-1.1, y-0.55), 2.2, 1.1, boxstyle="round,pad=0.08", 
                          facecolor=fc, edgecolor=ec, linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=8.5, fontweight='bold')
    # Draw line to center
    ax.plot([x, 5.5], [y, 4.5], color=ec, linewidth=1.5, linestyle='-', alpha=0.6)

# AI layer annotation
rect_ai = FancyBboxPatch((0.3, 0.1), 10.4, 0.6, boxstyle="round,pad=0.05", 
                          facecolor='#ECEFF1', edgecolor='#455A64', linewidth=1.5)
ax.add_patch(rect_ai)
ax.text(5.5, 0.4, 'AI Orchestration Layer: Real-time Data Fusion | Cross-Organ Coupling | Adaptive Model Updates', 
        ha='center', va='center', fontsize=8.5, fontweight='bold', color='#37474F')

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/dt_figures/Figure_3_MultiOrgan_DT.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# FIGURE 4: AI-Driven Predictive Simulation Framework
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')
ax.set_title('Figure 4: AI-Driven Predictive and Scenario-Based Physiological Simulation', 
             fontsize=12, fontweight='bold', pad=15)

# Input layer
inputs = [
    (0.5, 5.5, 1.8, 1, '#E3F2FD', 'Real-time\nSensor Data'),
    (0.5, 4.0, 1.8, 1, '#E8F5E9', 'Electronic\nHealth Records'),
    (0.5, 2.5, 1.8, 1, '#FFF3E0', 'Medical\nImaging'),
    (0.5, 1.0, 1.8, 1, '#FCE4EC', 'Genomic\nData'),
]

for x, y, w, h, fc, text in inputs:
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", 
                          facecolor=fc, edgecolor='#555', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=8, fontweight='bold')

# Data Fusion
rect_fusion = FancyBboxPatch((3.2, 2.5), 2, 3, boxstyle="round,pad=0.08", 
                              facecolor='#E1BEE7', edgecolor='#6A1B9A', linewidth=2)
ax.add_patch(rect_fusion)
ax.text(4.2, 4.0, 'AI-Powered\nData Fusion\n& State\nEstimation', 
        ha='center', va='center', fontsize=9, fontweight='bold')

# Arrows from inputs to fusion
for x, y, w, h, fc, text in inputs:
    ax.annotate('', xy=(3.2, 4.0), xytext=(x+w, y+h/2),
                arrowprops=dict(arrowstyle='->', color='#6A1B9A', lw=1.2))

# Predictive Engine
rect_pred = FancyBboxPatch((6, 2.5), 2.2, 3, boxstyle="round,pad=0.08", 
                            facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=2)
ax.add_patch(rect_pred)
ax.text(7.1, 4.0, 'Predictive\nSimulation\nEngine\n────────\n• What-If\n• Forecasting\n• Scenarios', 
        ha='center', va='center', fontsize=8.5, fontweight='bold')

ax.annotate('', xy=(6, 4.0), xytext=(5.2, 4.0),
            arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2))

# Outputs
outputs = [
    (9, 5.5, 2.5, 1, '#FFEBEE', 'Disease Progression\nPrediction'),
    (9, 4.0, 2.5, 1, '#E3F2FD', 'Treatment Response\nSimulation'),
    (9, 2.5, 2.5, 1, '#FFF9C4', 'Clinical Decision\nSupport'),
    (9, 1.0, 2.5, 1, '#E8F5E9', 'Early Warning\nAlerts'),
]

for x, y, w, h, fc, text in outputs:
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", 
                          facecolor=fc, edgecolor='#555', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=8, fontweight='bold')

# Arrows from predictive to outputs
for x, y, w, h, fc, text in outputs:
    ax.annotate('', xy=(x, y+h/2), xytext=(8.2, 4.0),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.2))

plt.tight_layout()
plt.savefig('/projects/sandbox/AMMAN/dt_figures/Figure_4_Predictive_Simulation.png', dpi=150, bbox_inches='tight')
plt.close()

print("All 4 figures generated successfully!")
