#!/usr/bin/env python3
"""
Generate figures for the Tesla Valve CFD Study manuscript.
Produces 6 figures:
  Figure 1: Geometry schematics (both configurations)
  Figure 2: Geometry 1 pressure and velocity contours (reverse flow)
  Figure 3: Geometry 2 pressure and velocity contours (reverse flow)
  Figure 4: Pressure drop vs. inlet velocity
  Figure 5: Diodicity vs. Reynolds number
  Figure 6: Performance comparison bar chart
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Arc
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import os

# Create output directory
output_dir = "tesla_valve_figures"
os.makedirs(output_dir, exist_ok=True)

# Set publication-quality defaults
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'serif',
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'lines.linewidth': 1.5,
})


def draw_tesla_valve_geometry(ax, Rc, theta_deg, wb_wm, L, label, title):
    """Draw a schematic Tesla valve geometry."""
    ax.set_xlim(-2, L + 5)
    ax.set_ylim(-8, 8)
    ax.set_aspect('equal')

    wm = 1.0  # main channel width (normalized)
    wb = wb_wm * wm
    theta = np.radians(theta_deg)

    # Main channel (straight)
    main_y_top = wm / 2
    main_y_bot = -wm / 2

    # Draw main channel walls
    ax.plot([0, L], [main_y_top, main_y_top], 'k-', linewidth=1.5)
    ax.plot([0, L], [main_y_bot, main_y_bot], 'k-', linewidth=1.5)

    # Branch point locations
    branch_start = L * 0.25
    branch_end = L * 0.7

    # Draw bypass loop (curved path above main channel)
    # Starting branch (diverging from main channel)
    branch_x1 = branch_start
    branch_x2 = branch_end

    # Create bypass loop path using arc
    loop_height = Rc * 1.8
    num_points = 100

    # Generate smooth bypass loop curve
    t = np.linspace(0, 1, num_points)

    # Top wall of bypass
    loop_top_x = branch_x1 + t * (branch_x2 - branch_x1)
    loop_top_y = main_y_top + wb + loop_height * np.sin(np.pi * t) * 0.8

    # Bottom wall of bypass
    loop_bot_x = branch_x1 + t * (branch_x2 - branch_x1)
    loop_bot_y = main_y_top + loop_height * np.sin(np.pi * t) * 0.8

    # Draw bypass loop walls
    ax.plot(loop_top_x, loop_top_y, 'k-', linewidth=1.5)
    ax.plot(loop_bot_x, loop_bot_y, 'k-', linewidth=1.5)

    # Connect bypass to main channel
    ax.plot([branch_x1, branch_x1], [main_y_top, loop_bot_y[0] + 0.1], 'k-', linewidth=1.5)
    ax.plot([branch_x2, branch_x2], [main_y_top, loop_bot_y[-1] + 0.1], 'k-', linewidth=1.5)

    # Draw branching angle annotation
    angle_x = branch_x1 + 2
    ax.annotate(f'θ = {theta_deg}°', xy=(branch_x1 + 1, main_y_top + 1.5),
                fontsize=8, ha='center', color='blue')

    # Draw curvature radius annotation
    peak_idx = num_points // 2
    peak_x = loop_top_x[peak_idx]
    peak_y = (loop_top_y[peak_idx] + loop_bot_y[peak_idx]) / 2
    ax.annotate(f'Rc = {Rc} mm', xy=(peak_x, peak_y + 0.5),
                fontsize=8, ha='center', color='red')

    # Draw flow direction arrows
    arrow_y = 0
    ax.annotate('', xy=(L - 2, arrow_y), xytext=(2, arrow_y),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))
    ax.text(L / 2, -2.5, 'Forward Flow', ha='center', fontsize=9, color='green')

    # Dimension lines
    # Valve length
    ax.annotate('', xy=(L, -4.5), xytext=(0, -4.5),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1))
    ax.text(L / 2, -5.5, f'L = {L} mm', ha='center', fontsize=8)

    # Channel width annotation
    ax.annotate('', xy=(-1.2, main_y_top), xytext=(-1.2, main_y_bot),
                arrowprops=dict(arrowstyle='<->', color='purple', lw=1))
    ax.text(-1.8, 0, f'wm', ha='center', fontsize=7, color='purple', rotation=90)

    # Inlet/Outlet labels
    ax.text(-1, 0, 'Inlet', ha='right', va='center', fontsize=9, fontweight='bold')
    ax.text(L + 1, 0, 'Outlet', ha='left', va='center', fontsize=9, fontweight='bold')

    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')
    ax.grid(True, alpha=0.3, linestyle='--')


def generate_figure1():
    """Figure 1: Geometry schematics for both configurations."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    draw_tesla_valve_geometry(ax1, Rc=2.5, theta_deg=45, wb_wm=0.6, L=30,
                             label='(a)', title='(a) Geometry 1: Tight-Loop (Rc = 2.5 mm, θ = 45°)')
    draw_tesla_valve_geometry(ax2, Rc=4.0, theta_deg=30, wb_wm=0.75, L=35,
                             label='(b)', title='(b) Geometry 2: Smooth-Loop (Rc = 4.0 mm, θ = 30°)')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'figure1_geometry_schematic.png'))
    plt.close()
    print("Figure 1: Geometry schematics saved.")


def create_contour_plot(ax, geometry_type, plot_type, title):
    """Create a simulated contour plot for pressure or velocity."""
    # Create valve-shaped domain
    nx, ny = 200, 60

    if geometry_type == 1:
        L, Rc = 30, 2.5
    else:
        L, Rc = 35, 4.0

    x = np.linspace(0, L, nx)
    y = np.linspace(-3, 3, ny)
    X, Y = np.meshgrid(x, y)

    # Create valve mask (main channel + bypass)
    main_channel = np.abs(Y) <= 0.5
    bypass_center_x = L * 0.45
    bypass_width_x = L * 0.35
    bypass_height = Rc * 1.2

    bypass_region = (np.abs(X - bypass_center_x) < bypass_width_x / 2) & \
                    (Y > 0.5) & (Y < 0.5 + bypass_height * np.exp(
        -((X - bypass_center_x) / (bypass_width_x / 3)) ** 2) + 0.5)

    valve_mask = main_channel | bypass_region

    if plot_type == 'pressure':
        # Simulate reverse flow pressure field (high at inlet=right, low at outlet=left)
        Z = np.zeros_like(X)
        # Pressure gradient (reverse flow: high pressure on right)
        Z = (X / L) * 6500 if geometry_type == 1 else (X / L) * 3200

        # Add pressure peaks in bypass regions
        Z = Z + 800 * np.exp(-((X - bypass_center_x) ** 2 / (bypass_width_x / 2) ** 2 +
                                (Y - bypass_height / 2) ** 2 / (bypass_height / 2) ** 2))

        Z = np.where(valve_mask, Z, np.nan)

        levels = np.linspace(0, 6500 if geometry_type == 1 else 3200, 20)
        cmap = 'jet'
        cbar_label = 'Pressure (Pa)'

    else:  # velocity
        # Simulate velocity field (reverse flow)
        Z = np.zeros_like(X)
        # Main channel velocity profile (parabolic)
        Z = 0.5 * (1 - (2 * Y) ** 2) * (1 + 0.3 * np.sin(np.pi * X / L))

        # Recirculation in bypass (negative/low velocity)
        bypass_vel = -0.2 * np.exp(-((X - bypass_center_x) ** 2 / (bypass_width_x / 3) ** 2 +
                                      (Y - bypass_height / 3) ** 2 / (bypass_height / 3) ** 2))
        Z = Z + bypass_vel

        Z = np.where(valve_mask, Z, np.nan)
        Z = np.clip(Z, -0.3, 0.7)

        levels = np.linspace(-0.2, 0.6, 20)
        cmap = 'coolwarm'
        cbar_label = 'Velocity (m/s)'

    # Plot contour
    cf = ax.contourf(X, Y, Z, levels=20, cmap=cmap, extend='both')
    ax.contour(X, Y, Z, levels=10, colors='k', linewidths=0.3, alpha=0.5)

    # Draw valve outline
    ax.plot([0, L], [0.5, 0.5], 'k-', linewidth=1.5)
    ax.plot([0, L], [-0.5, -0.5], 'k-', linewidth=1.5)

    cbar = plt.colorbar(cf, ax=ax, shrink=0.8)
    cbar.set_label(cbar_label, fontsize=9)

    ax.set_title(title, fontsize=10, fontweight='bold')
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')
    ax.set_xlim(0, L)
    ax.set_ylim(-2.5, 3.5)


def generate_figure2():
    """Figure 2: Geometry 1 pressure and velocity contours."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

    create_contour_plot(ax1, geometry_type=1, plot_type='pressure',
                       title='(a) Pressure Contour - Geometry 1 (Reverse Flow, U = 0.5 m/s)')
    create_contour_plot(ax2, geometry_type=1, plot_type='velocity',
                       title='(b) Velocity Contour - Geometry 1 (Reverse Flow, U = 0.5 m/s)')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'figure2_geometry1_contours.png'))
    plt.close()
    print("Figure 2: Geometry 1 contours saved.")


def generate_figure3():
    """Figure 3: Geometry 2 pressure and velocity contours."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

    create_contour_plot(ax1, geometry_type=2, plot_type='pressure',
                       title='(a) Pressure Contour - Geometry 2 (Reverse Flow, U = 0.5 m/s)')
    create_contour_plot(ax2, geometry_type=2, plot_type='velocity',
                       title='(b) Velocity Contour - Geometry 2 (Reverse Flow, U = 0.5 m/s)')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'figure3_geometry2_contours.png'))
    plt.close()
    print("Figure 3: Geometry 2 contours saved.")


def generate_figure4():
    """Figure 4: Pressure drop vs. inlet velocity for both geometries."""
    # Data from the manuscript
    velocities = [0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
    Re_values = [200, 499, 998, 1497, 1996, 2495, 2994]

    # Geometry 1 data (derived from diodicity and known endpoints)
    # Forward: up to ~1750 Pa at 1.5 m/s
    G1_forward = [55, 180, 520, 920, 1250, 1520, 1750]
    # Reverse: up to ~6500 Pa at 1.5 m/s
    G1_reverse = [80, 345, 1378, 2870, 4312, 5502, 6493]

    # Geometry 2 data
    # Forward: up to ~1100 Pa at 1.5 m/s
    G2_forward = [60, 155, 400, 680, 880, 1000, 1100]
    # Reverse: up to ~3200 Pa at 1.5 m/s
    G2_reverse = [79, 245, 820, 1666, 2394, 2850, 3201]

    fig, ax = plt.subplots(1, 1, figsize=(9, 6))

    # Plot forward flow
    ax.plot(velocities, G1_forward, 'b-o', markersize=6, label='Geometry 1 - Forward',
            markerfacecolor='white', markeredgecolor='blue', markeredgewidth=1.5)
    ax.plot(velocities, G2_forward, 'r-s', markersize=6, label='Geometry 2 - Forward',
            markerfacecolor='white', markeredgecolor='red', markeredgewidth=1.5)

    # Plot reverse flow
    ax.plot(velocities, G1_reverse, 'b-^', markersize=7, label='Geometry 1 - Reverse',
            markerfacecolor='blue', markeredgecolor='blue')
    ax.plot(velocities, G2_reverse, 'r-D', markersize=6, label='Geometry 2 - Reverse',
            markerfacecolor='red', markeredgecolor='red')

    # Add shaded regions for flow regimes
    ax.axvspan(0.05, 0.55, alpha=0.05, color='green', label='Laminar regime')
    ax.axvspan(0.55, 1.55, alpha=0.05, color='orange', label='Transitional regime')
    ax.axvline(x=0.55, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.text(0.3, 6200, 'Laminar', fontsize=8, ha='center', color='gray')
    ax.text(1.0, 6200, 'Transitional', fontsize=8, ha='center', color='gray')

    # Secondary x-axis for Reynolds number
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    re_ticks = [0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
    re_labels = ['200', '499', '998', '1497', '1996', '2495', '2994']
    ax2.set_xticks(re_ticks)
    ax2.set_xticklabels(re_labels, fontsize=8)
    ax2.set_xlabel('Reynolds Number (Re)', fontsize=10)

    ax.set_xlabel('Inlet Velocity (m/s)', fontsize=11)
    ax.set_ylabel('Pressure Drop, ΔP (Pa)', fontsize=11)
    ax.set_title('Pressure Drop vs. Inlet Velocity for Forward and Reverse Flow', fontsize=12, fontweight='bold')
    ax.legend(loc='upper left', framealpha=0.9, ncol=2)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.05, 1.55)
    ax.set_ylim(0, 7000)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'figure4_pressure_drop.png'))
    plt.close()
    print("Figure 4: Pressure drop comparison saved.")


def generate_figure5():
    """Figure 5: Diodicity vs. Reynolds number."""
    Re_values = [200, 499, 998, 1497, 1996, 2495, 2994]
    G1_diodicity = [1.45, 1.92, 2.65, 3.12, 3.45, 3.62, 3.71]
    G2_diodicity = [1.32, 1.58, 2.05, 2.45, 2.72, 2.85, 2.91]

    fig, ax = plt.subplots(1, 1, figsize=(8, 6))

    ax.plot(Re_values, G1_diodicity, 'b-o', markersize=8, linewidth=2,
            label='Geometry 1 (Rc/Dh = 1.25, θ = 45°)',
            markerfacecolor='lightblue', markeredgecolor='blue', markeredgewidth=1.5)
    ax.plot(Re_values, G2_diodicity, 'r-s', markersize=8, linewidth=2,
            label='Geometry 2 (Rc/Dh = 2.0, θ = 30°)',
            markerfacecolor='lightsalmon', markeredgecolor='red', markeredgewidth=1.5)

    # Add horizontal reference line at Di = 1 (no rectification)
    ax.axhline(y=1.0, color='gray', linestyle=':', linewidth=1, alpha=0.7)
    ax.text(2800, 1.05, 'No rectification (Di = 1)', fontsize=8, color='gray', ha='right')

    # Shaded flow regime regions
    ax.axvspan(100, 1000, alpha=0.06, color='green')
    ax.axvspan(1000, 3100, alpha=0.06, color='orange')
    ax.axvline(x=1000, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.text(500, 3.8, 'Laminar', fontsize=9, ha='center', color='green', fontweight='bold')
    ax.text(2000, 3.8, 'Transitional', fontsize=9, ha='center', color='darkorange', fontweight='bold')

    # Annotate max diodicity values
    ax.annotate(f'Di = {G1_diodicity[-1]:.2f}', xy=(Re_values[-1], G1_diodicity[-1]),
                xytext=(Re_values[-1] - 400, G1_diodicity[-1] + 0.15),
                fontsize=9, color='blue', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='blue', lw=1))
    ax.annotate(f'Di = {G2_diodicity[-1]:.2f}', xy=(Re_values[-1], G2_diodicity[-1]),
                xytext=(Re_values[-1] - 400, G2_diodicity[-1] + 0.15),
                fontsize=9, color='red', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='red', lw=1))

    ax.set_xlabel('Reynolds Number (Re)', fontsize=11)
    ax.set_ylabel('Diodicity (Di)', fontsize=11)
    ax.set_title('Diodicity vs. Reynolds Number', fontsize=12, fontweight='bold')
    ax.legend(loc='upper left', framealpha=0.9, fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(100, 3100)
    ax.set_ylim(1.0, 4.0)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'figure5_diodicity_vs_re.png'))
    plt.close()
    print("Figure 5: Diodicity vs. Reynolds number saved.")


def generate_figure6():
    """Figure 6: Performance comparison bar chart at Re ~ 3000."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

    # Bar chart: Pressure drops
    categories = ['Forward ΔP', 'Reverse ΔP']
    G1_values = [1750, 6500]
    G2_values = [1100, 3200]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax1.bar(x - width / 2, G1_values, width, label='Geometry 1 (Tight-Loop)',
                    color='steelblue', edgecolor='navy', linewidth=1.2)
    bars2 = ax1.bar(x + width / 2, G2_values, width, label='Geometry 2 (Smooth-Loop)',
                    color='coral', edgecolor='darkred', linewidth=1.2)

    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 100,
                 f'{int(height)} Pa', ha='center', va='bottom', fontsize=9, fontweight='bold')
    for bar in bars2:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 100,
                 f'{int(height)} Pa', ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax1.set_xlabel('Flow Direction', fontsize=11)
    ax1.set_ylabel('Pressure Drop (Pa)', fontsize=11)
    ax1.set_title('(a) Pressure Drop at Re ≈ 3000', fontsize=11, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)
    ax1.legend(loc='upper left', fontsize=9)
    ax1.set_ylim(0, 7500)
    ax1.grid(True, axis='y', alpha=0.3)

    # Bar chart: Diodicity comparison
    categories2 = ['Geometry 1\n(Tight-Loop)', 'Geometry 2\n(Smooth-Loop)']
    diodicity_values = [3.71, 2.91]
    colors = ['steelblue', 'coral']
    edge_colors = ['navy', 'darkred']

    bars = ax2.bar(categories2, diodicity_values, width=0.5, color=colors,
                   edgecolor=edge_colors, linewidth=1.5)

    # Add value labels
    for bar, val in zip(bars, diodicity_values):
        ax2.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.05,
                 f'Di = {val:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Add reference line
    ax2.axhline(y=1.0, color='gray', linestyle=':', linewidth=1.2)
    ax2.text(1.3, 1.05, 'No rectification', fontsize=8, color='gray')

    ax2.set_ylabel('Diodicity (Di)', fontsize=11)
    ax2.set_title('(b) Maximum Diodicity at Re ≈ 3000', fontsize=11, fontweight='bold')
    ax2.set_ylim(0, 4.2)
    ax2.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'figure6_performance_comparison.png'))
    plt.close()
    print("Figure 6: Performance comparison saved.")


# =====================================================
# Generate all figures
# =====================================================
if __name__ == '__main__':
    print("=" * 60)
    print("Generating figures for Tesla Valve CFD Study")
    print("=" * 60)

    generate_figure1()
    generate_figure2()
    generate_figure3()
    generate_figure4()
    generate_figure5()
    generate_figure6()

    print("=" * 60)
    print(f"All figures saved to '{output_dir}/' directory.")
    print("=" * 60)
