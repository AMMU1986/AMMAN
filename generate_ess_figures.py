#!/usr/bin/env python3
"""
Generate SVG figures for Chapter: Optimal Sizing and Placement of ESS in HRES
Uses only Python standard library (no matplotlib needed)
"""
import math
import os

OUTPUT_DIR = "/projects/sandbox/AMMAN/ESS_chapter_figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def svg_header(width=800, height=500, title=""):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<title>{title}</title>
<defs>
  <style>
    .title {{ font: bold 16px Arial, sans-serif; fill: #1a1a2e; }}
    .label {{ font: 12px Arial, sans-serif; fill: #333; }}
    .axis-label {{ font: bold 13px Arial, sans-serif; fill: #333; }}
    .legend {{ font: 12px Arial, sans-serif; fill: #333; }}
    .small {{ font: 10px Arial, sans-serif; fill: #555; }}
  </style>
</defs>
<rect width="{width}" height="{height}" fill="white"/>
'''



def svg_footer():
    return '</svg>\n'


def figure1_ess_technology_comparison():
    """Figure 1: Comparison of ESS Technologies - Energy Density vs Power Density"""
    w, h = 850, 550
    svg = svg_header(w, h, "ESS Technology Comparison")

    # Title
    svg += '<text x="425" y="30" class="title" text-anchor="middle">Figure 1: Energy Storage Technology Comparison (Power Density vs Energy Density)</text>\n'

    # Plot area
    px, py, pw, ph = 100, 60, 650, 420
    svg += f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="#f8f9fa" stroke="#ccc"/>\n'

    # Axis labels
    svg += f'<text x="{px + pw//2}" y="{py + ph + 45}" class="axis-label" text-anchor="middle">Specific Energy (Wh/kg)</text>\n'
    svg += f'<text x="{px - 55}" y="{py + ph//2}" class="axis-label" text-anchor="middle" transform="rotate(-90,{px-55},{py+ph//2})">Specific Power (W/kg)</text>\n'

    # Technologies data: (name, energy_wh_kg, power_w_kg, color, size)
    techs = [
        ("Li-ion (NMC)", 200, 1500, "#e63946", 22),
        ("Li-ion (LFP)", 140, 1200, "#f4845f", 20),
        ("Lead-Acid", 40, 300, "#6c757d", 18),
        ("Flow Battery\n(VRFB)", 25, 100, "#457b9d", 20),
        ("Supercapacitor", 8, 10000, "#2a9d8f", 18),
        ("NaS Battery", 120, 200, "#e9c46a", 17),
        ("Flywheel", 10, 5000, "#264653", 16),
        ("Hydrogen\nFuel Cell", 500, 50, "#8338ec", 19),
        ("Compressed\nAir (CAES)", 15, 20, "#06d6a0", 16),
    ]

    # Log scale mapping
    x_min, x_max = 5, 600  # Wh/kg
    y_min, y_max = 10, 15000  # W/kg

    def map_x(val):
        return px + (math.log10(val) - math.log10(x_min)) / (math.log10(x_max) - math.log10(x_min)) * pw

    def map_y(val):
        return py + ph - (math.log10(val) - math.log10(y_min)) / (math.log10(y_max) - math.log10(y_min)) * ph

    # Grid lines
    for xv in [10, 50, 100, 200, 500]:
        xx = map_x(xv)
        svg += f'<line x1="{xx}" y1="{py}" x2="{xx}" y2="{py+ph}" stroke="#ddd" stroke-dasharray="3,3"/>\n'
        svg += f'<text x="{xx}" y="{py+ph+15}" class="small" text-anchor="middle">{xv}</text>\n'

    for yv in [10, 100, 1000, 10000]:
        yy = map_y(yv)
        svg += f'<line x1="{px}" y1="{yy}" x2="{px+pw}" y2="{yy}" stroke="#ddd" stroke-dasharray="3,3"/>\n'
        svg += f'<text x="{px-10}" y="{yy+4}" class="small" text-anchor="end">{yv}</text>\n'

    # Plot bubbles
    for name, energy, power, color, size in techs:
        cx = map_x(energy)
        cy = map_y(power)
        svg += f'<circle cx="{cx}" cy="{cy}" r="{size}" fill="{color}" fill-opacity="0.7" stroke="{color}" stroke-width="2"/>\n'
        lines = name.split('\n')
        for i, line in enumerate(lines):
            svg += f'<text x="{cx}" y="{cy + size + 14 + i*13}" class="small" text-anchor="middle">{line}</text>\n'

    svg += svg_footer()
    with open(f"{OUTPUT_DIR}/Figure_1_ESS_Technology_Comparison.svg", 'w') as f:
        f.write(svg)
    print("Figure 1 generated.")



def figure2_optimization_framework():
    """Figure 2: ESS Sizing Optimization Framework Flowchart"""
    w, h = 900, 600
    svg = svg_header(w, h, "ESS Sizing Optimization Framework")
    svg += '<text x="450" y="30" class="title" text-anchor="middle">Figure 2: Multi-Objective ESS Sizing Optimization Framework</text>\n'

    # Define boxes
    boxes = [
        (450, 70, 220, 40, "Input Data Collection", "#264653"),
        (200, 150, 180, 35, "Renewable Resource\nData (Solar, Wind)", "#2a9d8f"),
        (450, 150, 180, 35, "Load Demand\nProfiles", "#2a9d8f"),
        (700, 150, 180, 35, "Economic\nParameters", "#2a9d8f"),
        (450, 225, 250, 40, "System Modeling & Constraints", "#457b9d"),
        (450, 305, 250, 40, "Optimization Algorithm Selection", "#e9c46a"),
        (180, 385, 160, 35, "Metaheuristic\n(GA, PSO, DE)", "#f4845f"),
        (420, 385, 160, 35, "AI-Driven\n(DRL, BO)", "#f4845f"),
        (660, 385, 160, 35, "Mathematical\n(MILP, NLP)", "#f4845f"),
        (450, 460, 250, 40, "Multi-Objective Evaluation", "#e63946"),
        (450, 540, 250, 40, "Pareto-Optimal ESS Design", "#264653"),
    ]

    for (cx, cy, bw, bh, text, color) in boxes:
        x = cx - bw/2
        y = cy - bh/2
        svg += f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="8" fill="{color}" fill-opacity="0.15" stroke="{color}" stroke-width="2"/>\n'
        lines = text.split('\n')
        for i, line in enumerate(lines):
            ty = cy + (i - (len(lines)-1)/2) * 14
            svg += f'<text x="{cx}" y="{ty + 5}" class="label" text-anchor="middle" font-weight="bold">{line}</text>\n'

    # Arrows
    arrows = [
        (450, 90, 450, 130), (200, 167, 360, 225), (450, 167, 450, 205),
        (700, 167, 540, 225), (450, 245, 450, 285),
        (450, 325, 450, 365), (450, 325, 260, 367), (450, 325, 660, 367),
        (260, 402, 350, 440), (450, 402, 450, 440), (660, 402, 550, 440),
        (450, 480, 450, 520),
    ]
    for (x1, y1, x2, y2) in arrows:
        svg += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#333" stroke-width="1.5" marker-end="url(#arrowhead)"/>\n'

    svg += '<defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#333"/></marker></defs>\n'
    svg += svg_footer()
    with open(f"{OUTPUT_DIR}/Figure_2_Optimization_Framework.svg", 'w') as f:
        f.write(svg)
    print("Figure 2 generated.")



def figure3_pareto_front():
    """Figure 3: Pareto Front - LCOE vs LPSP Trade-off"""
    w, h = 800, 520
    svg = svg_header(w, h, "Pareto Front LCOE vs LPSP")
    svg += '<text x="400" y="30" class="title" text-anchor="middle">Figure 3: Pareto Front - LCOE vs Reliability (LPSP) Trade-off</text>\n'

    px, py, pw, ph = 100, 55, 600, 380
    svg += f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="#f8f9fa" stroke="#aaa"/>\n'

    svg += f'<text x="{px + pw//2}" y="{py + ph + 45}" class="axis-label" text-anchor="middle">Loss of Power Supply Probability (LPSP) [%]</text>\n'
    svg += f'<text x="{px - 55}" y="{py + ph//2}" class="axis-label" text-anchor="middle" transform="rotate(-90,{px-55},{py+ph//2})">LCOE ($/kWh)</text>\n'

    # LPSP range: 0-5%, LCOE range: 0.10-0.35
    x_min, x_max = 0, 5
    y_min, y_max = 0.10, 0.35

    def mx(v): return px + (v - x_min)/(x_max - x_min) * pw
    def my(v): return py + ph - (v - y_min)/(y_max - y_min) * ph

    # Grid
    for xv in [0, 1, 2, 3, 4, 5]:
        xx = mx(xv)
        svg += f'<line x1="{xx}" y1="{py}" x2="{xx}" y2="{py+ph}" stroke="#e0e0e0"/>\n'
        svg += f'<text x="{xx}" y="{py+ph+15}" class="small" text-anchor="middle">{xv}</text>\n'
    for yv in [0.10, 0.15, 0.20, 0.25, 0.30, 0.35]:
        yy = my(yv)
        svg += f'<line x1="{px}" y1="{yy}" x2="{px+pw}" y2="{yy}" stroke="#e0e0e0"/>\n'
        svg += f'<text x="{px-8}" y="{yy+4}" class="small" text-anchor="end">{yv:.2f}</text>\n'

    # Pareto front points (LPSP%, LCOE)
    pareto = [(0.2, 0.32), (0.5, 0.28), (0.8, 0.24), (1.2, 0.21), (1.5, 0.19),
              (2.0, 0.17), (2.5, 0.155), (3.0, 0.145), (3.5, 0.138), (4.0, 0.132), (4.5, 0.128)]

    # Draw Pareto curve
    points_str = " ".join([f"{mx(x)},{my(y)}" for x, y in pareto])
    svg += f'<polyline points="{points_str}" fill="none" stroke="#e63946" stroke-width="2.5"/>\n'
    for x, y in pareto:
        svg += f'<circle cx="{mx(x)}" cy="{my(y)}" r="5" fill="#e63946"/>\n'

    # Non-dominated solutions (scattered above Pareto)
    import random
    random.seed(42)
    for _ in range(30):
        lpsp = random.uniform(0.3, 4.8)
        lcoe = random.uniform(0.16, 0.34)
        # Ensure above Pareto
        pareto_lcoe = 0.32 - 0.045 * lpsp + 0.003 * lpsp**2
        if lcoe > pareto_lcoe + 0.01:
            svg += f'<circle cx="{mx(lpsp)}" cy="{my(lcoe)}" r="4" fill="#457b9d" fill-opacity="0.5"/>\n'

    # Highlight optimal region
    svg += f'<rect x="{mx(1.0)}" y="{my(0.22)}" width="{mx(2.5)-mx(1.0)}" height="{my(0.155)-my(0.22)}" fill="#2a9d8f" fill-opacity="0.15" stroke="#2a9d8f" stroke-dasharray="5,3" stroke-width="1.5"/>\n'
    svg += f'<text x="{mx(1.75)}" y="{my(0.23)}" class="label" text-anchor="middle" fill="#2a9d8f">Preferred Region</text>\n'

    # Legend
    svg += f'<circle cx="{px+pw-130}" cy="{py+20}" r="5" fill="#e63946"/>\n'
    svg += f'<text x="{px+pw-118}" y="{py+24}" class="legend">Pareto Front</text>\n'
    svg += f'<circle cx="{px+pw-130}" cy="{py+40}" r="4" fill="#457b9d" fill-opacity="0.5"/>\n'
    svg += f'<text x="{px+pw-118}" y="{py+44}" class="legend">Dominated Solutions</text>\n'

    svg += svg_footer()
    with open(f"{OUTPUT_DIR}/Figure_3_Pareto_Front.svg", 'w') as f:
        f.write(svg)
    print("Figure 3 generated.")



def figure4_placement_network():
    """Figure 4: ESS Placement in Distribution Network"""
    w, h = 900, 600
    svg = svg_header(w, h, "ESS Placement in Distribution Network")
    svg += '<text x="450" y="30" class="title" text-anchor="middle">Figure 4: Optimal ESS Placement in IEEE 33-Bus Distribution Network with HRES</text>\n'

    # Simplified 33-bus-like network
    nodes = [
        (100, 300, "Sub", "#264653", 14),  # Substation
        (180, 300, "1", "#457b9d", 8), (240, 300, "2", "#457b9d", 8),
        (300, 300, "3", "#457b9d", 8), (360, 300, "4", "#457b9d", 8),
        (420, 300, "5", "#457b9d", 8), (480, 300, "6", "#e63946", 12),  # ESS here
        (540, 300, "7", "#457b9d", 8), (600, 300, "8", "#457b9d", 8),
        (660, 300, "9", "#457b9d", 8), (720, 300, "10", "#457b9d", 8),
        (780, 300, "11", "#457b9d", 8),
        # Branch 1 (upward from node 3)
        (300, 220, "12", "#457b9d", 8), (300, 150, "13", "#457b9d", 8),
        (360, 150, "14", "#457b9d", 8),
        # Branch 2 (downward from node 6)
        (480, 380, "15", "#457b9d", 8), (480, 440, "16", "#457b9d", 8),
        (540, 440, "17", "#457b9d", 8), (540, 500, "18", "#e63946", 12),  # ESS here
        # Branch 3 (upward from node 9)
        (660, 220, "19", "#457b9d", 8), (660, 150, "20", "#457b9d", 8),
        (720, 150, "21", "#457b9d", 8),
        # Branch 4 (downward from node 10)
        (720, 380, "22", "#457b9d", 8), (720, 440, "23", "#457b9d", 8),
        (780, 440, "24", "#457b9d", 8), (780, 500, "25", "#e63946", 12),  # ESS here
    ]

    # Draw connections (edges)
    edges = [
        (0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,11),
        (3,12),(12,13),(13,14),
        (6,15),(15,16),(16,17),(17,18),
        (9,19),(19,20),(20,21),
        (10,22),(22,23),(23,24),(24,25),
    ]
    for i, j in edges:
        x1, y1 = nodes[i][0], nodes[i][1]
        x2, y2 = nodes[j][0], nodes[j][1]
        svg += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#888" stroke-width="2"/>\n'

    # Draw nodes
    for x, y, label, color, r in nodes:
        svg += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" stroke="white" stroke-width="1.5"/>\n'
        if r > 10:
            svg += f'<text x="{x}" y="{y+4}" class="small" text-anchor="middle" fill="white" font-weight="bold">{label}</text>\n'

    # Add PV symbols (yellow sun icons)
    pv_nodes = [(300, 150), (660, 150)]  # Nodes 13, 20
    for px_n, py_n in pv_nodes:
        svg += f'<circle cx="{px_n+25}" cy="{py_n-15}" r="12" fill="#f4a261" stroke="#e76f51" stroke-width="1.5"/>\n'
        svg += f'<text x="{px_n+25}" y="{py_n-11}" class="small" text-anchor="middle" fill="white" font-weight="bold">PV</text>\n'

    # Add Wind symbols
    wind_nodes = [(360, 150), (720, 150)]  # Nodes 14, 21
    for wx, wy in wind_nodes:
        svg += f'<rect x="{wx+15}" y="{wy-28}" width="24" height="18" rx="4" fill="#2a9d8f" stroke="#264653"/>\n'
        svg += f'<text x="{wx+27}" y="{wy-16}" class="small" text-anchor="middle" fill="white" font-weight="bold">W</text>\n'

    # ESS labels
    ess_positions = [(480, 300, "6"), (540, 500, "18"), (780, 500, "25")]
    for ex, ey, lbl in ess_positions:
        svg += f'<rect x="{ex-18}" y="{ey+16}" width="36" height="16" rx="3" fill="#e63946" stroke="#c1121f"/>\n'
        svg += f'<text x="{ex}" y="{ey+27}" class="small" text-anchor="middle" fill="white" font-weight="bold">ESS</text>\n'

    # Legend
    ly = 560
    svg += f'<circle cx="150" cy="{ly}" r="8" fill="#457b9d"/>\n'
    svg += f'<text x="165" y="{ly+4}" class="legend">Load Bus</text>\n'
    svg += f'<circle cx="280" cy="{ly}" r="10" fill="#e63946"/>\n'
    svg += f'<text x="297" y="{ly+4}" class="legend">Optimal ESS Location</text>\n'
    svg += f'<circle cx="450" cy="{ly}" r="10" fill="#f4a261"/>\n'
    svg += f'<text x="467" y="{ly+4}" class="legend">Solar PV</text>\n'
    svg += f'<rect x="560" y="{ly-9}" width="20" height="18" rx="3" fill="#2a9d8f"/>\n'
    svg += f'<text x="587" y="{ly+4}" class="legend">Wind Turbine</text>\n'
    svg += f'<rect x="700" y="{ly-7}" width="14" height="14" fill="#264653"/>\n'
    svg += f'<text x="720" y="{ly+4}" class="legend">Substation</text>\n'

    svg += svg_footer()
    with open(f"{OUTPUT_DIR}/Figure_4_Placement_Network.svg", 'w') as f:
        f.write(svg)
    print("Figure 4 generated.")



def figure5_cost_trends():
    """Figure 5: ESS Cost Reduction Trajectories"""
    w, h = 800, 500
    svg = svg_header(w, h, "ESS Cost Trajectories")
    svg += '<text x="400" y="30" class="title" text-anchor="middle">Figure 5: Energy Storage Cost Trajectories and Projections (2015-2035)</text>\n'

    px, py, pw, ph = 100, 55, 620, 370
    svg += f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="#f8f9fa" stroke="#aaa"/>\n'

    svg += f'<text x="{px + pw//2}" y="{py + ph + 45}" class="axis-label" text-anchor="middle">Year</text>\n'
    svg += f'<text x="{px - 55}" y="{py + ph//2}" class="axis-label" text-anchor="middle" transform="rotate(-90,{px-55},{py+ph//2})">Cost ($/kWh)</text>\n'

    years = list(range(2015, 2036))
    y_min, y_max = 0, 700

    def mx(yr): return px + (yr - 2015) / 20 * pw
    def my(cost): return py + ph - (cost - y_min) / (y_max - y_min) * ph

    # Grid
    for yr in range(2015, 2036, 5):
        xx = mx(yr)
        svg += f'<line x1="{xx}" y1="{py}" x2="{xx}" y2="{py+ph}" stroke="#e0e0e0"/>\n'
        svg += f'<text x="{xx}" y="{py+ph+15}" class="small" text-anchor="middle">{yr}</text>\n'
    for cv in range(0, 701, 100):
        yy = my(cv)
        svg += f'<line x1="{px}" y1="{yy}" x2="{px+pw}" y2="{yy}" stroke="#e0e0e0"/>\n'
        svg += f'<text x="{px-8}" y="{yy+4}" class="small" text-anchor="end">{cv}</text>\n'

    # Projection region
    svg += f'<rect x="{mx(2025)}" y="{py}" width="{mx(2035)-mx(2025)}" height="{ph}" fill="#f0f0f0" fill-opacity="0.5"/>\n'
    svg += f'<text x="{mx(2030)}" y="{py+15}" class="small" text-anchor="middle" fill="#888">Projected</text>\n'

    # Li-ion data
    liion = [(2015, 600), (2016, 520), (2017, 450), (2018, 380), (2019, 320),
             (2020, 270), (2021, 230), (2022, 200), (2023, 170), (2024, 150), (2025, 135),
             (2026, 120), (2027, 108), (2028, 97), (2029, 88), (2030, 80),
             (2031, 74), (2032, 68), (2033, 63), (2034, 59), (2035, 55)]
    pts = " ".join([f"{mx(yr)},{my(c)}" for yr, c in liion])
    svg += f'<polyline points="{pts}" fill="none" stroke="#e63946" stroke-width="2.5"/>\n'

    # Flow battery
    flow = [(2015, 450), (2016, 420), (2017, 395), (2018, 370), (2019, 350),
            (2020, 320), (2021, 300), (2022, 280), (2023, 260), (2024, 240), (2025, 225),
            (2026, 210), (2027, 195), (2028, 182), (2029, 170), (2030, 160),
            (2031, 150), (2032, 142), (2033, 135), (2034, 128), (2035, 122)]
    pts = " ".join([f"{mx(yr)},{my(c)}" for yr, c in flow])
    svg += f'<polyline points="{pts}" fill="none" stroke="#457b9d" stroke-width="2.5"/>\n'

    # Sodium-ion
    nai = [(2020, 350), (2021, 310), (2022, 270), (2023, 220), (2024, 180), (2025, 155),
           (2026, 135), (2027, 118), (2028, 103), (2029, 92), (2030, 82),
           (2031, 74), (2032, 67), (2033, 61), (2034, 56), (2035, 52)]
    pts = " ".join([f"{mx(yr)},{my(c)}" for yr, c in nai])
    svg += f'<polyline points="{pts}" fill="none" stroke="#2a9d8f" stroke-width="2.5" stroke-dasharray="6,3"/>\n'

    # Legend
    lx, ly = px + pw - 180, py + 30
    svg += f'<line x1="{lx}" y1="{ly}" x2="{lx+30}" y2="{ly}" stroke="#e63946" stroke-width="2.5"/>\n'
    svg += f'<text x="{lx+35}" y="{ly+4}" class="legend">Lithium-ion</text>\n'
    svg += f'<line x1="{lx}" y1="{ly+20}" x2="{lx+30}" y2="{ly+20}" stroke="#457b9d" stroke-width="2.5"/>\n'
    svg += f'<text x="{lx+35}" y="{ly+24}" class="legend">Flow Battery (VRFB)</text>\n'
    svg += f'<line x1="{lx}" y1="{ly+40}" x2="{lx+30}" y2="{ly+40}" stroke="#2a9d8f" stroke-width="2.5" stroke-dasharray="6,3"/>\n'
    svg += f'<text x="{lx+35}" y="{ly+44}" class="legend">Sodium-ion</text>\n'

    svg += svg_footer()
    with open(f"{OUTPUT_DIR}/Figure_5_Cost_Trajectories.svg", 'w') as f:
        f.write(svg)
    print("Figure 5 generated.")



def figure6_digital_twin():
    """Figure 6: Digital Twin Architecture for ESS Management"""
    w, h = 900, 550
    svg = svg_header(w, h, "Digital Twin Architecture")
    svg += '<text x="450" y="30" class="title" text-anchor="middle">Figure 6: Digital Twin and IoT Architecture for Intelligent ESS Management</text>\n'

    # Physical Layer
    svg += '<rect x="30" y="60" width="840" height="120" rx="10" fill="#e8f4f8" stroke="#457b9d" stroke-width="1.5"/>\n'
    svg += '<text x="60" y="82" class="axis-label" fill="#264653">Physical Layer</text>\n'

    phys_items = [("Solar PV\nArray", 120, 130), ("Wind\nTurbines", 260, 130),
                  ("Battery\nESS", 400, 130), ("Power\nElectronics", 540, 130),
                  ("Load\nCenters", 680, 130), ("Grid\nConnection", 800, 130)]
    for label, cx, cy in phys_items:
        svg += f'<rect x="{cx-45}" y="{cy-22}" width="90" height="44" rx="6" fill="#457b9d" fill-opacity="0.2" stroke="#457b9d"/>\n'
        lines = label.split('\n')
        for i, line in enumerate(lines):
            svg += f'<text x="{cx}" y="{cy + (i-0.5)*13 + 3}" class="small" text-anchor="middle">{line}</text>\n'

    # IoT/Communication Layer
    svg += '<rect x="30" y="200" width="840" height="80" rx="10" fill="#fff3e0" stroke="#e9c46a" stroke-width="1.5"/>\n'
    svg += '<text x="60" y="222" class="axis-label" fill="#e76f51">IoT & Communication Layer</text>\n'
    iot_items = ["Sensors &\nMeters", "Edge\nComputing", "MQTT/OPC-UA\nProtocols", "5G/WiFi\nNetwork", "Data\nAggregation"]
    for i, item in enumerate(iot_items):
        cx = 150 + i * 160
        lines = item.split('\n')
        for j, line in enumerate(lines):
            svg += f'<text x="{cx}" y="{247 + j*13}" class="small" text-anchor="middle">{line}</text>\n'

    # Digital Twin Layer
    svg += '<rect x="30" y="300" width="840" height="120" rx="10" fill="#e8f8e8" stroke="#2a9d8f" stroke-width="1.5"/>\n'
    svg += '<text x="60" y="322" class="axis-label" fill="#264653">Digital Twin Layer</text>\n'
    dt_items = [("Electrochemical\nModel", 150, 365), ("Thermal\nModel", 310, 365),
                ("Degradation\nModel", 470, 365), ("Power Flow\nSimulation", 630, 365),
                ("State\nEstimation", 790, 365)]
    for label, cx, cy in dt_items:
        svg += f'<rect x="{cx-55}" y="{cy-22}" width="110" height="44" rx="6" fill="#2a9d8f" fill-opacity="0.2" stroke="#2a9d8f"/>\n'
        lines = label.split('\n')
        for i, line in enumerate(lines):
            svg += f'<text x="{cx}" y="{cy + (i-0.5)*13 + 3}" class="small" text-anchor="middle">{line}</text>\n'

    # Intelligence Layer
    svg += '<rect x="30" y="440" width="840" height="90" rx="10" fill="#f3e8ff" stroke="#8338ec" stroke-width="1.5"/>\n'
    svg += '<text x="60" y="462" class="axis-label" fill="#8338ec">Intelligence & Decision Layer</text>\n'
    intel_items = [("Predictive\nMaintenance", 150, 495), ("Optimal\nDispatch (MPC)", 320, 495),
                   ("SOH/RUL\nPrediction", 490, 495), ("Anomaly\nDetection", 650, 495),
                   ("Fleet\nManagement", 800, 495)]
    for label, cx, cy in intel_items:
        svg += f'<rect x="{cx-55}" y="{cy-20}" width="110" height="40" rx="6" fill="#8338ec" fill-opacity="0.15" stroke="#8338ec"/>\n'
        lines = label.split('\n')
        for i, line in enumerate(lines):
            svg += f'<text x="{cx}" y="{cy + (i-0.5)*13 + 2}" class="small" text-anchor="middle">{line}</text>\n'

    # Vertical arrows between layers
    for cx in [200, 400, 600, 750]:
        svg += f'<line x1="{cx}" y1="180" x2="{cx}" y2="200" stroke="#888" stroke-width="1.5" marker-end="url(#arrowhead)"/>\n'
        svg += f'<line x1="{cx}" y1="280" x2="{cx}" y2="300" stroke="#888" stroke-width="1.5" marker-end="url(#arrowhead)"/>\n'
        svg += f'<line x1="{cx}" y1="420" x2="{cx}" y2="440" stroke="#888" stroke-width="1.5" marker-end="url(#arrowhead)"/>\n'

    svg += '<defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#888"/></marker></defs>\n'
    svg += svg_footer()
    with open(f"{OUTPUT_DIR}/Figure_6_Digital_Twin_Architecture.svg", 'w') as f:
        f.write(svg)
    print("Figure 6 generated.")


# Generate all figures
if __name__ == "__main__":
    figure1_ess_technology_comparison()
    figure2_optimization_framework()
    figure3_pareto_front()
    figure4_placement_network()
    figure5_cost_trends()
    figure6_digital_twin()
    print("\nAll 6 figures generated in:", OUTPUT_DIR)
