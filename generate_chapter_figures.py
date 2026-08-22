"""
Generate 4 scientific figures for the book chapter:
"Differential Equations and Dynamical Systems in Biology"

Figure 1: Lotka-Volterra Predator-Prey Dynamics (Phase Portrait and Time Series)
Figure 2: SIR Epidemic Model Dynamics
Figure 3: Bifurcation Diagram for Bistable Gene Regulatory Network
Figure 4: Reaction-Diffusion Pattern Formation (Turing Patterns)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.gridspec import GridSpec
import matplotlib
matplotlib.use('Agg')

# Set publication-quality defaults
plt.rcParams.update({
    'font.size': 11,
    'font.family': 'serif',
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

output_dir = '/projects/sandbox/AMMAN/chapter_figures/'
import os
os.makedirs(output_dir, exist_ok=True)

# ============================================================
# FIGURE 1: Lotka-Volterra Predator-Prey Dynamics
# ============================================================
def lotka_volterra(y, t, alpha, beta, delta, gamma):
    x, p = y
    dxdt = alpha * x - beta * x * p
    dpdt = delta * x * p - gamma * p
    return [dxdt, dpdt]

# Parameters
alpha, beta, delta, gamma = 1.0, 0.1, 0.075, 1.5
t = np.linspace(0, 50, 2000)

fig = plt.figure(figsize=(12, 5))
gs = GridSpec(1, 2, figure=fig, wspace=0.35)

# Time series
ax1 = fig.add_subplot(gs[0, 0])
y0 = [10, 5]
sol = odeint(lotka_volterra, y0, t, args=(alpha, beta, delta, gamma))
ax1.plot(t, sol[:, 0], 'b-', linewidth=2, label='Prey (x)')
ax1.plot(t, sol[:, 1], 'r-', linewidth=2, label='Predator (y)')
ax1.set_xlabel('Time (t)')
ax1.set_ylabel('Population Density')
ax1.set_title('(a) Population Oscillations Over Time')
ax1.legend(loc='upper right')
ax1.set_xlim(0, 50)
ax1.grid(True, alpha=0.3)

# Phase portrait
ax2 = fig.add_subplot(gs[0, 1])
for y0_i in [[10, 5], [15, 3], [20, 8], [8, 10], [30, 4]]:
    sol_i = odeint(lotka_volterra, y0_i, t, args=(alpha, beta, delta, gamma))
    ax2.plot(sol_i[:, 0], sol_i[:, 1], linewidth=1.5)

# Mark equilibrium point
eq_x, eq_y = gamma/delta, alpha/beta
ax2.plot(eq_x, eq_y, 'k*', markersize=15, label=f'Equilibrium ({eq_x:.1f}, {eq_y:.1f})')
ax2.set_xlabel('Prey Population (x)')
ax2.set_ylabel('Predator Population (y)')
ax2.set_title('(b) Phase Portrait')
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)

plt.suptitle('Figure 1: Lotka-Volterra Predator-Prey Model Dynamics', fontsize=14, fontweight='bold', y=1.02)
plt.savefig(output_dir + 'Figure_1_Predator_Prey_Dynamics.png', bbox_inches='tight', pad_inches=0.2)
plt.close()
print("Figure 1 saved.")

# ============================================================
# FIGURE 2: SIR Epidemic Model Dynamics
# ============================================================
def sir_model(y, t, beta, gamma, mu=0):
    S, I, R = y
    N = S + I + R
    dSdt = -beta * S * I / N + mu * (N - S)
    dIdt = beta * S * I / N - gamma * I - mu * I
    dRdt = gamma * I - mu * R
    return [dSdt, dIdt, dRdt]

fig = plt.figure(figsize=(12, 5))
gs = GridSpec(1, 2, figure=fig, wspace=0.35)

# Basic SIR
ax1 = fig.add_subplot(gs[0, 0])
N = 1000
beta_sir, gamma_sir = 0.3, 0.1
y0_sir = [990/N, 10/N, 0]
t_sir = np.linspace(0, 160, 3000)
sol_sir = odeint(sir_model, y0_sir, t_sir, args=(beta_sir, gamma_sir))

ax1.plot(t_sir, sol_sir[:, 0], 'b-', linewidth=2.5, label='Susceptible (S)')
ax1.plot(t_sir, sol_sir[:, 1], 'r-', linewidth=2.5, label='Infected (I)')
ax1.plot(t_sir, sol_sir[:, 2], 'g-', linewidth=2.5, label='Recovered (R)')
ax1.axhline(y=1/3, color='gray', linestyle='--', alpha=0.5, label=r'$1/R_0$ threshold')
ax1.set_xlabel('Time (days)')
ax1.set_ylabel('Proportion of Population')
ax1.set_title(r'(a) SIR Model ($R_0$ = 3.0)')
ax1.legend(loc='right')
ax1.set_xlim(0, 160)
ax1.grid(True, alpha=0.3)

# Effect of vaccination (varying R0)
ax2 = fig.add_subplot(gs[0, 1])
R0_values = [1.5, 2.5, 3.5, 5.0]
colors = ['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728']
for R0, color in zip(R0_values, colors):
    beta_v = R0 * gamma_sir
    sol_v = odeint(sir_model, y0_sir, t_sir, args=(beta_v, gamma_sir))
    ax2.plot(t_sir, sol_v[:, 1], color=color, linewidth=2, label=f'$R_0$ = {R0}')

ax2.set_xlabel('Time (days)')
ax2.set_ylabel('Proportion Infected')
ax2.set_title('(b) Epidemic Curves for Different $R_0$ Values')
ax2.legend(loc='upper right')
ax2.set_xlim(0, 160)
ax2.grid(True, alpha=0.3)

plt.suptitle('Figure 2: SIR Compartmental Epidemic Model', fontsize=14, fontweight='bold', y=1.02)
plt.savefig(output_dir + 'Figure_2_SIR_Epidemic_Model.png', bbox_inches='tight', pad_inches=0.2)
plt.close()
print("Figure 2 saved.")

# ============================================================
# FIGURE 3: Bifurcation Diagram - Bistable Gene Switch
# ============================================================
fig = plt.figure(figsize=(12, 5))
gs = GridSpec(1, 2, figure=fig, wspace=0.35)

# Gene regulatory toggle switch bifurcation
ax1 = fig.add_subplot(gs[0, 0])

# Hill function-based toggle switch: dx/dt = alpha/(1+y^n) - delta*x
# At steady state with symmetric parameters
n = 4  # Hill coefficient
alpha_vals = np.linspace(0.5, 5.0, 200)
x_ss_high = []
x_ss_low = []
x_ss_unstable = []

for a in alpha_vals:
    # Find steady states: x = a/(1 + x^n) (symmetric case, y=x for simplicity of bifurcation)
    # Actually use: dx/dt = a/(1+x^n) - x
    x_range = np.linspace(0.001, 5, 10000)
    f = a / (1 + x_range**n) - x_range
    # Find zero crossings
    sign_changes = np.where(np.diff(np.sign(f)))[0]
    roots = []
    for sc in sign_changes:
        # Linear interpolation
        x1, x2 = x_range[sc], x_range[sc+1]
        f1, f2 = f[sc], f[sc+1]
        root = x1 - f1 * (x2 - x1) / (f2 - f1)
        roots.append(root)
    
    if len(roots) == 3:
        x_ss_low.append((a, roots[0]))
        x_ss_unstable.append((a, roots[1]))
        x_ss_high.append((a, roots[2]))
    elif len(roots) == 1:
        x_ss_low.append((a, roots[0]))

if x_ss_low:
    xl = np.array(x_ss_low)
    ax1.plot(xl[:, 0], xl[:, 1], 'b-', linewidth=2.5, label='Stable (low)')
if x_ss_high:
    xh = np.array(x_ss_high)
    ax1.plot(xh[:, 0], xh[:, 1], 'r-', linewidth=2.5, label='Stable (high)')
if x_ss_unstable:
    xu = np.array(x_ss_unstable)
    ax1.plot(xu[:, 0], xu[:, 1], 'k--', linewidth=1.5, label='Unstable')

ax1.set_xlabel('Transcription Rate (α)')
ax1.set_ylabel('Steady-State Protein Level (x*)')
ax1.set_title('(a) Saddle-Node Bifurcation Diagram')
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)

# Nullclines and vector field for bistable system
ax2 = fig.add_subplot(gs[0, 1])
a_fixed = 3.0
x_grid = np.linspace(0, 3.5, 20)
y_grid = np.linspace(0, 3.5, 20)
X, Y = np.meshgrid(x_grid, y_grid)

# Toggle switch: dx/dt = a/(1+Y^n) - x, dy/dt = a/(1+X^n) - y
dX = a_fixed / (1 + Y**n) - X
dY = a_fixed / (1 + X**n) - Y

# Normalize arrows
M = np.sqrt(dX**2 + dY**2)
M[M == 0] = 1
dX_norm = dX / M
dY_norm = dY / M

ax2.quiver(X, Y, dX_norm, dY_norm, M, cmap='coolwarm', alpha=0.6)

# Plot nullclines
x_nc = np.linspace(0.01, 3.5, 500)
y_nullcline_x = a_fixed / (1 + x_nc**n)  # x-nullcline: x = a/(1+y^n) => y = ...
x_nullcline_y = a_fixed / (1 + x_nc**n)  # y-nullcline: y = a/(1+x^n)

ax2.plot(x_nc, y_nullcline_x, 'b-', linewidth=2.5, label='x-nullcline')
ax2.plot(x_nullcline_y, x_nc, 'r-', linewidth=2.5, label='y-nullcline')

ax2.set_xlabel('Protein X Concentration')
ax2.set_ylabel('Protein Y Concentration')
ax2.set_title('(b) Nullclines and Phase Portrait')
ax2.legend(loc='upper right')
ax2.set_xlim(0, 3.5)
ax2.set_ylim(0, 3.5)
ax2.grid(True, alpha=0.3)

plt.suptitle('Figure 3: Bistability in Gene Regulatory Toggle Switch', fontsize=14, fontweight='bold', y=1.02)
plt.savefig(output_dir + 'Figure_3_Bifurcation_Gene_Switch.png', bbox_inches='tight', pad_inches=0.2)
plt.close()
print("Figure 3 saved.")

# ============================================================
# FIGURE 4: Reaction-Diffusion Turing Pattern Formation
# ============================================================
fig = plt.figure(figsize=(12, 5))
gs = GridSpec(1, 2, figure=fig, wspace=0.3)

# Simulate a 1D reaction-diffusion system (activator-inhibitor)
# Using Gray-Scott model simplified
np.random.seed(42)

# 2D Turing pattern simulation (simplified)
N_grid = 100
dx = 1.0
dt = 0.1
steps = 5000

# Parameters for Turing instability
Du, Dv = 1.0, 10.0  # Diffusion coefficients
a, b = 0.04, 0.06   # Reaction parameters

# Initialize with small perturbation
u = np.ones((N_grid, N_grid)) * 0.5 + 0.05 * np.random.randn(N_grid, N_grid)
v = np.ones((N_grid, N_grid)) * 0.25 + 0.05 * np.random.randn(N_grid, N_grid)

def laplacian(Z, dx):
    return (np.roll(Z, 1, axis=0) + np.roll(Z, -1, axis=0) +
            np.roll(Z, 1, axis=1) + np.roll(Z, -1, axis=1) - 4*Z) / dx**2

# Schnakenberg kinetics
for step in range(steps):
    Lu = laplacian(u, dx)
    Lv = laplacian(v, dx)
    
    fu = a - u + u**2 * v
    fv = b - u**2 * v
    
    u += dt * (Du * Lu + fu)
    v += dt * (Dv * Lv + fv)
    
    # Clip for stability
    u = np.clip(u, 0, 5)
    v = np.clip(v, 0, 5)

# Plot Turing pattern - Activator
ax1 = fig.add_subplot(gs[0, 0])
im1 = ax1.imshow(u, cmap='viridis', interpolation='bilinear')
ax1.set_title('(a) Activator Concentration (u)')
ax1.set_xlabel('Spatial x')
ax1.set_ylabel('Spatial y')
plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

# Plot Turing pattern - Inhibitor
ax2 = fig.add_subplot(gs[0, 1])
im2 = ax2.imshow(v, cmap='magma', interpolation='bilinear')
ax2.set_title('(b) Inhibitor Concentration (v)')
ax2.set_xlabel('Spatial x')
ax2.set_ylabel('Spatial y')
plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

plt.suptitle('Figure 4: Turing Pattern Formation via Reaction-Diffusion', fontsize=14, fontweight='bold', y=1.02)
plt.savefig(output_dir + 'Figure_4_Turing_Patterns.png', bbox_inches='tight', pad_inches=0.2)
plt.close()
print("Figure 4 saved.")

print("\nAll 4 figures generated successfully!")
