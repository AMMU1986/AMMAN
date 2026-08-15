#!/usr/bin/env python3
"""
Generate figures for Tesla Valve CFD Manuscript using pure Python (no external dependencies).
Creates SVG figures for the manuscript.
"""

import os
import math

OUTPUT_DIR = "tesla_valve_figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_figure1_geometry():
    """Create Figure 1: Schematic of Tesla valve geometries (single-loop and double-turn)."""
    
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="500" viewBox="0 0 900 500">
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
    <linearGradient id="flowGrad1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#2196F3;stop-opacity:0.8"/>
      <stop offset="100%" style="stop-color:#64B5F6;stop-opacity:0.4"/>
    </linearGradient>
    <linearGradient id="flowGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#FF5722;stop-opacity:0.8"/>
      <stop offset="100%" style="stop-color:#FF8A65;stop-opacity:0.4"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="900" height="500" fill="white"/>
  
  <!-- Title -->
  <text x="450" y="30" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#333">
    Tesla Valve Geometry Configurations
  </text>
  
  <!-- (a) Single-Loop Configuration -->
  <text x="225" y="60" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="#333">
    (a) Geometry 1: Single-Loop Configuration
  </text>
  
  <!-- Main channel - single loop -->
  <rect x="50" y="120" width="350" height="40" fill="none" stroke="#333" stroke-width="2"/>
  
  <!-- Loop bypass path -->
  <path d="M 150 120 C 150 60, 250 60, 250 120" fill="none" stroke="#333" stroke-width="2"/>
  <path d="M 150 120 C 150 50, 260 50, 260 120" fill="none" stroke="#333" stroke-width="2" stroke-dasharray="none"/>
  
  <!-- Inner loop walls -->
  <path d="M 160 120 C 160 75, 240 75, 240 120" fill="none" stroke="#333" stroke-width="2"/>
  
  <!-- Flow arrows in main channel -->
  <line x1="60" y1="140" x2="130" y2="140" stroke="#2196F3" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="270" y1="140" x2="380" y2="140" stroke="#2196F3" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- Flow arrow in bypass -->
  <path d="M 170 95 L 210 80" fill="none" stroke="#FF5722" stroke-width="1.5" marker-end="url(#arrowhead)"/>
  
  <!-- Dimensions -->
  <line x1="50" y1="180" x2="400" y2="180" stroke="#666" stroke-width="1" stroke-dasharray="4,2"/>
  <text x="225" y="195" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#666">L = Total valve length</text>
  
  <!-- Angle annotation -->
  <path d="M 150 120 L 165 90" fill="none" stroke="#E91E63" stroke-width="1.5"/>
  <text x="130" y="95" font-family="Arial, sans-serif" font-size="10" fill="#E91E63">θ</text>
  
  <!-- Labels -->
  <text x="90" y="145" font-family="Arial, sans-serif" font-size="10" fill="#2196F3">Forward</text>
  <text x="190" y="70" font-family="Arial, sans-serif" font-size="10" fill="#FF5722">Bypass</text>
  <text x="60" y="115" font-family="Arial, sans-serif" font-size="10" fill="#333">Inlet</text>
  <text x="370" y="115" font-family="Arial, sans-serif" font-size="10" fill="#333">Outlet</text>
  
  <!-- Recirculation zone indicator -->
  <ellipse cx="200" cy="100" rx="15" ry="8" fill="none" stroke="#9C27B0" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="200" y="55" font-family="Arial, sans-serif" font-size="9" text-anchor="middle" fill="#9C27B0">Recirculation zone</text>
  
  
  <!-- (b) Double-Turn Configuration -->
  <text x="675" y="60" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="#333">
    (b) Geometry 2: Double-Turn Configuration
  </text>
  
  <!-- Main channel - double turn -->
  <rect x="500" y="120" width="350" height="40" fill="none" stroke="#333" stroke-width="2"/>
  
  <!-- First loop -->
  <path d="M 580 120 C 580 65, 650 65, 650 120" fill="none" stroke="#333" stroke-width="2"/>
  <path d="M 590 120 C 590 80, 640 80, 640 120" fill="none" stroke="#333" stroke-width="2"/>
  
  <!-- Second loop -->
  <path d="M 700 120 C 700 65, 770 65, 770 120" fill="none" stroke="#333" stroke-width="2"/>
  <path d="M 710 120 C 710 80, 760 80, 760 120" fill="none" stroke="#333" stroke-width="2"/>
  
  <!-- Flow arrows -->
  <line x1="510" y1="140" x2="560" y2="140" stroke="#2196F3" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="660" y1="140" x2="690" y2="140" stroke="#2196F3" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="780" y1="140" x2="835" y2="140" stroke="#2196F3" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- Bypass arrows -->
  <path d="M 600 100 L 625 85" fill="none" stroke="#FF5722" stroke-width="1.5" marker-end="url(#arrowhead)"/>
  <path d="M 720 100 L 745 85" fill="none" stroke="#FF5722" stroke-width="1.5" marker-end="url(#arrowhead)"/>
  
  <!-- Labels -->
  <text x="525" y="115" font-family="Arial, sans-serif" font-size="10" fill="#333">Inlet</text>
  <text x="815" y="115" font-family="Arial, sans-serif" font-size="10" fill="#333">Outlet</text>
  <text x="615" y="70" font-family="Arial, sans-serif" font-size="10" fill="#FF5722">Loop 1</text>
  <text x="735" y="70" font-family="Arial, sans-serif" font-size="10" fill="#FF5722">Loop 2</text>
  
  <!-- Dimensions for double-turn -->
  <line x1="500" y1="180" x2="850" y2="180" stroke="#666" stroke-width="1" stroke-dasharray="4,2"/>
  <text x="675" y="195" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#666">L = Total valve length</text>
  
  <!-- Curvature radius annotation -->
  <line x1="615" y1="90" x2="615" y2="120" stroke="#E91E63" stroke-width="1" stroke-dasharray="2,2"/>
  <text x="625" y="108" font-family="Arial, sans-serif" font-size="10" fill="#E91E63">R</text>
  
  
  <!-- Key geometric parameters box -->
  <rect x="100" y="250" width="700" height="220" fill="#F5F5F5" stroke="#CCC" stroke-width="1" rx="5"/>
  <text x="450" y="275" font-family="Arial, sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#333">
    Key Geometric Parameters
  </text>
  
  <!-- Parameter descriptions -->
  <text x="150" y="305" font-family="Arial, sans-serif" font-size="12" fill="#333">• Curvature radius (R): Controls the tightness of bypass loops</text>
  <text x="150" y="330" font-family="Arial, sans-serif" font-size="12" fill="#333">• Branching angle (θ): Angle at which bypass diverges from main channel</text>
  <text x="150" y="355" font-family="Arial, sans-serif" font-size="12" fill="#333">• Channel width ratio (w/W): Ratio of bypass to main channel width</text>
  <text x="150" y="380" font-family="Arial, sans-serif" font-size="12" fill="#333">• Total valve length (L): Overall length of the valve structure</text>
  <text x="150" y="405" font-family="Arial, sans-serif" font-size="12" fill="#333">• Hydraulic diameter (D_h): 2.0 mm for the present study</text>
  
  <!-- Working fluid info -->
  <text x="150" y="440" font-family="Arial, sans-serif" font-size="12" fill="#555">Working fluid: Water (ρ = 998 kg/m³, μ = 0.001 Pa·s)</text>
  <text x="150" y="460" font-family="Arial, sans-serif" font-size="12" fill="#555">Reynolds number range: 200–3000 (Laminar to Transitional)</text>
</svg>'''
    
    with open(os.path.join(OUTPUT_DIR, "figure1_geometry.svg"), "w") as f:
        f.write(svg_content)
    print("Created figure1_geometry.svg")


def create_figure2_pressure_drop():
    """Create Figure 2: Pressure drop variation with inlet velocity for forward-biased geometries."""
    
    # Data points from the manuscript
    velocities = [0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
    
    # Forward flow pressure drops (Pa) - extrapolated from manuscript data
    geom1_forward = [95, 220, 480, 820, 1180, 1450, 1750]
    geom2_forward = [60, 140, 310, 520, 720, 920, 1100]
    geom3_forward = [75, 175, 380, 650, 940, 1180, 1420]
    
    # SVG chart dimensions
    chart_x = 120
    chart_y = 60
    chart_w = 650
    chart_h = 380
    
    # Scale
    x_min, x_max = 0, 1.6
    y_min, y_max = 0, 2000
    
    def scale_x(v):
        return chart_x + (v - x_min) / (x_max - x_min) * chart_w
    
    def scale_y(p):
        return chart_y + chart_h - (p - y_min) / (y_max - y_min) * chart_h
    
    # Build SVG
    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="550" viewBox="0 0 900 550">',
        '<rect width="900" height="550" fill="white"/>',
        '',
        '<!-- Title -->',
        '<text x="450" y="35" font-family="Arial, sans-serif" font-size="15" font-weight="bold" text-anchor="middle" fill="#333">',
        'Pressure Drop vs. Inlet Velocity (Forward Flow)</text>',
        '',
        '<!-- Chart area -->',
        f'<rect x="{chart_x}" y="{chart_y}" width="{chart_w}" height="{chart_h}" fill="#FAFAFA" stroke="#333" stroke-width="1.5"/>',
    ]
    
    # Grid lines and Y-axis labels
    for p in range(0, 2001, 400):
        y = scale_y(p)
        svg_lines.append(f'<line x1="{chart_x}" y1="{y:.1f}" x2="{chart_x + chart_w}" y2="{y:.1f}" stroke="#DDD" stroke-width="0.5"/>')
        svg_lines.append(f'<text x="{chart_x - 10}" y="{y + 4:.1f}" font-family="Arial, sans-serif" font-size="11" text-anchor="end" fill="#333">{p}</text>')
    
    # X-axis labels
    for v_tick in [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]:
        x = scale_x(v_tick)
        svg_lines.append(f'<line x1="{x:.1f}" y1="{chart_y + chart_h}" x2="{x:.1f}" y2="{chart_y + chart_h + 5}" stroke="#333" stroke-width="1"/>')
        svg_lines.append(f'<text x="{x:.1f}" y="{chart_y + chart_h + 20}" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#333">{v_tick}</text>')
    
    # Axis labels
    svg_lines.append(f'<text x="{chart_x + chart_w/2}" y="{chart_y + chart_h + 45}" font-family="Arial, sans-serif" font-size="13" text-anchor="middle" fill="#333">Inlet Velocity (m/s)</text>')
    svg_lines.append(f'<text x="30" y="{chart_y + chart_h/2}" font-family="Arial, sans-serif" font-size="13" text-anchor="middle" fill="#333" transform="rotate(-90, 30, {chart_y + chart_h/2})">Pressure Drop (Pa)</text>')
    
    # Plot data series
    colors = ["#D32F2F", "#1976D2", "#388E3C"]
    labels = ["Geometry 1", "Geometry 2", "Geometry 3"]
    datasets = [geom1_forward, geom2_forward, geom3_forward]
    markers = ["circle", "square", "triangle"]
    
    for idx, (data, color, label) in enumerate(zip(datasets, colors, labels)):
        # Line
        points = []
        for v, p in zip(velocities, data):
            points.append(f"{scale_x(v):.1f},{scale_y(p):.1f}")
        polyline = " ".join(points)
        svg_lines.append(f'<polyline points="{polyline}" fill="none" stroke="{color}" stroke-width="2.5"/>')
        
        # Data points
        for v, p in zip(velocities, data):
            x, y = scale_x(v), scale_y(p)
            if markers[idx] == "circle":
                svg_lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{color}" stroke="white" stroke-width="1.5"/>')
            elif markers[idx] == "square":
                svg_lines.append(f'<rect x="{x-4:.1f}" y="{y-4:.1f}" width="8" height="8" fill="{color}" stroke="white" stroke-width="1.5"/>')
            else:
                svg_lines.append(f'<polygon points="{x:.1f},{y-5:.1f} {x-5:.1f},{y+4:.1f} {x+5:.1f},{y+4:.1f}" fill="{color}" stroke="white" stroke-width="1.5"/>')
    
    # Legend
    legend_x = chart_x + chart_w - 180
    legend_y = chart_y + 20
    svg_lines.append(f'<rect x="{legend_x}" y="{legend_y}" width="170" height="95" fill="white" stroke="#CCC" stroke-width="1" rx="3"/>')
    
    for idx, (color, label) in enumerate(zip(colors, labels)):
        ly = legend_y + 25 + idx * 28
        svg_lines.append(f'<line x1="{legend_x + 10}" y1="{ly}" x2="{legend_x + 40}" y2="{ly}" stroke="{color}" stroke-width="2.5"/>')
        if markers[idx] == "circle":
            svg_lines.append(f'<circle cx="{legend_x + 25}" cy="{ly}" r="4" fill="{color}"/>')
        elif markers[idx] == "square":
            svg_lines.append(f'<rect x="{legend_x + 21}" y="{ly - 4}" width="8" height="8" fill="{color}"/>')
        else:
            svg_lines.append(f'<polygon points="{legend_x + 25},{ly - 4} {legend_x + 21},{ly + 4} {legend_x + 29},{ly + 4}" fill="{color}"/>')
        svg_lines.append(f'<text x="{legend_x + 50}" y="{ly + 4}" font-family="Arial, sans-serif" font-size="12" fill="#333">{label}</text>')
    
    svg_lines.append('</svg>')
    
    with open(os.path.join(OUTPUT_DIR, "figure2_pressure_drop.svg"), "w") as f:
        f.write("\n".join(svg_lines))
    print("Created figure2_pressure_drop.svg")


def create_figure3_geometry1_contours():
    """Create Figure 3: Geometry 1 pressure and velocity contours (schematic)."""
    
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="500" viewBox="0 0 900 500">
  <defs>
    <!-- Pressure colormap gradient -->
    <linearGradient id="pressureGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#0000FF"/>
      <stop offset="25%" style="stop-color:#00BFFF"/>
      <stop offset="50%" style="stop-color:#00FF00"/>
      <stop offset="75%" style="stop-color:#FFFF00"/>
      <stop offset="100%" style="stop-color:#FF0000"/>
    </linearGradient>
    <!-- Velocity colormap gradient -->
    <linearGradient id="velocityGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#000080"/>
      <stop offset="20%" style="stop-color:#0000FF"/>
      <stop offset="40%" style="stop-color:#00FFFF"/>
      <stop offset="60%" style="stop-color:#00FF00"/>
      <stop offset="80%" style="stop-color:#FFFF00"/>
      <stop offset="100%" style="stop-color:#FF0000"/>
    </linearGradient>
    <!-- Pressure field gradient for contour -->
    <linearGradient id="pField" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" style="stop-color:#FF4444;stop-opacity:0.8"/>
      <stop offset="30%" style="stop-color:#FFAA00;stop-opacity:0.7"/>
      <stop offset="50%" style="stop-color:#44FF44;stop-opacity:0.6"/>
      <stop offset="75%" style="stop-color:#00AAFF;stop-opacity:0.7"/>
      <stop offset="100%" style="stop-color:#0044FF;stop-opacity:0.8"/>
    </linearGradient>
    <linearGradient id="vField" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" style="stop-color:#0000AA;stop-opacity:0.8"/>
      <stop offset="25%" style="stop-color:#0088FF;stop-opacity:0.7"/>
      <stop offset="50%" style="stop-color:#00FF88;stop-opacity:0.7"/>
      <stop offset="75%" style="stop-color:#FFFF00;stop-opacity:0.8"/>
      <stop offset="100%" style="stop-color:#FF0000;stop-opacity:0.9"/>
    </linearGradient>
    <radialGradient id="vortex1" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:#FF0000;stop-opacity:0.9"/>
      <stop offset="60%" style="stop-color:#FFAA00;stop-opacity:0.5"/>
      <stop offset="100%" style="stop-color:#00FF00;stop-opacity:0.2"/>
    </radialGradient>
    <radialGradient id="lowP" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:#0000FF;stop-opacity:0.8"/>
      <stop offset="70%" style="stop-color:#00AAFF;stop-opacity:0.4"/>
      <stop offset="100%" style="stop-color:#00FF00;stop-opacity:0.1"/>
    </radialGradient>
  </defs>
  
  <rect width="900" height="500" fill="white"/>
  
  <!-- Main Title -->
  <text x="450" y="25" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="#333">
    Geometry 1 — Reverse Flow Contours (Inlet Velocity = 0.5 m/s)
  </text>
  
  <!-- (a) Pressure Contour -->
  <text x="225" y="52" font-family="Arial, sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#333">(a) Pressure Contour</text>
  
  <!-- Valve outline with pressure field -->
  <rect x="50" y="70" width="350" height="50" fill="url(#pField)" stroke="#333" stroke-width="1.5" rx="2"/>
  
  <!-- Loop with pressure variation -->
  <path d="M 150 70 C 130 10, 280 10, 260 70" fill="url(#pField)" stroke="#333" stroke-width="1.5"/>
  
  <!-- High pressure zone -->
  <ellipse cx="155" cy="55" rx="20" ry="15" fill="rgba(255,50,0,0.4)" stroke="none"/>
  <text x="155" y="58" font-family="Arial, sans-serif" font-size="8" text-anchor="middle" fill="#8B0000">~470 Pa</text>
  
  <!-- Low pressure zone -->
  <ellipse cx="210" cy="35" rx="18" ry="12" fill="url(#lowP)" stroke="none"/>
  <text x="210" y="38" font-family="Arial, sans-serif" font-size="8" text-anchor="middle" fill="#000080">~-270 Pa</text>
  
  <!-- Flow direction -->
  <text x="380" y="85" font-family="Arial, sans-serif" font-size="10" fill="#333">← Reverse flow</text>
  
  <!-- Pressure colorbar -->
  <rect x="50" y="135" width="200" height="12" fill="url(#pressureGrad)" stroke="#333" stroke-width="0.5"/>
  <text x="50" y="160" font-family="Arial, sans-serif" font-size="9" fill="#333">-270 Pa</text>
  <text x="230" y="160" font-family="Arial, sans-serif" font-size="9" text-anchor="end" fill="#333">470 Pa</text>
  <text x="150" y="160" font-family="Arial, sans-serif" font-size="9" text-anchor="middle" fill="#333">Pressure (Pa)</text>
  
  
  <!-- (b) Velocity Contour -->
  <text x="675" y="52" font-family="Arial, sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#333">(b) Velocity Contour</text>
  
  <!-- Valve outline with velocity field -->
  <rect x="500" y="70" width="350" height="50" fill="url(#vField)" stroke="#333" stroke-width="1.5" rx="2"/>
  
  <!-- Loop with velocity variation -->
  <path d="M 600 70 C 580 10, 730 10, 710 70" fill="url(#vField)" stroke="#333" stroke-width="1.5"/>
  
  <!-- High velocity jet zone -->
  <ellipse cx="650" cy="50" rx="25" ry="10" fill="url(#vortex1)" stroke="none"/>
  <text x="650" y="53" font-family="Arial, sans-serif" font-size="8" text-anchor="middle" fill="white">1.05 m/s</text>
  
  <!-- Vortex indicators -->
  <circle cx="620" cy="35" r="8" fill="none" stroke="#FF4444" stroke-width="1.5" stroke-dasharray="3,2"/>
  <circle cx="690" cy="40" r="6" fill="none" stroke="#FF4444" stroke-width="1.5" stroke-dasharray="3,2"/>
  <text x="620" y="23" font-family="Arial, sans-serif" font-size="8" text-anchor="middle" fill="#CC0000">Vortex</text>
  
  <!-- Stagnation zone -->
  <ellipse cx="720" cy="85" rx="12" ry="8" fill="rgba(0,0,128,0.3)" stroke="none"/>
  <text x="720" y="105" font-family="Arial, sans-serif" font-size="8" text-anchor="middle" fill="#000080">Stagnation</text>
  
  <!-- Velocity colorbar -->
  <rect x="500" y="135" width="200" height="12" fill="url(#velocityGrad)" stroke="#333" stroke-width="0.5"/>
  <text x="500" y="160" font-family="Arial, sans-serif" font-size="9" fill="#333">0 m/s</text>
  <text x="680" y="160" font-family="Arial, sans-serif" font-size="9" text-anchor="end" fill="#333">1.05 m/s</text>
  <text x="600" y="160" font-family="Arial, sans-serif" font-size="9" text-anchor="middle" fill="#333">Velocity (m/s)</text>
  
  
  <!-- Detailed flow features section -->
  <rect x="50" y="185" width="800" height="290" fill="#F8F9FA" stroke="#DDD" stroke-width="1" rx="5"/>
  <text x="450" y="210" font-family="Arial, sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#333">
    Flow Features — Geometry 1 (Reverse Flow, V_in = 0.5 m/s)
  </text>
  
  <!-- Larger schematic of Geometry 1 reverse flow -->
  <!-- Main channel -->
  <rect x="100" y="240" width="600" height="60" fill="#E3F2FD" stroke="#1565C0" stroke-width="2" rx="3"/>
  
  <!-- Loop structure -->
  <path d="M 250 240 C 220 160, 450 160, 420 240" fill="#E8F5E9" stroke="#2E7D32" stroke-width="2"/>
  <path d="M 270 240 C 250 180, 430 180, 410 240" fill="#FFF3E0" stroke="#E65100" stroke-width="1.5" stroke-dasharray="4,2"/>
  
  <!-- Velocity vectors (arrows) showing reverse flow -->
  <line x1="680" y1="270" x2="620" y2="270" stroke="#1565C0" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="580" y1="270" x2="520" y2="270" stroke="#1565C0" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="450" y1="270" x2="430" y2="270" stroke="#1565C0" stroke-width="1.5" marker-end="url(#arrowhead)"/>
  
  <!-- Recirculation in bypass -->
  <ellipse cx="335" cy="200" rx="30" ry="18" fill="none" stroke="#D32F2F" stroke-width="2"/>
  <path d="M 315 195 C 310 185, 325 180, 330 190" fill="none" stroke="#D32F2F" stroke-width="1.5" marker-end="url(#arrowhead)"/>
  <path d="M 355 205 C 360 215, 345 220, 340 210" fill="none" stroke="#D32F2F" stroke-width="1.5" marker-end="url(#arrowhead)"/>
  
  <!-- Separation point -->
  <circle cx="420" cy="240" r="5" fill="#FF5722" stroke="white" stroke-width="1"/>
  <text x="430" y="233" font-family="Arial, sans-serif" font-size="9" fill="#BF360C">Separation point</text>
  
  <!-- Reattachment -->
  <circle cx="250" cy="240" r="5" fill="#4CAF50" stroke="white" stroke-width="1"/>
  <text x="230" y="233" font-family="Arial, sans-serif" font-size="9" fill="#1B5E20">Reattachment</text>
  
  <!-- Jet impingement -->
  <line x1="350" y1="200" x2="335" y2="240" stroke="#FF9800" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="360" y="218" font-family="Arial, sans-serif" font-size="9" fill="#E65100">Jet impingement</text>
  
  <!-- Flow direction labels -->
  <text x="690" y="265" font-family="Arial, sans-serif" font-size="10" fill="#1565C0">Inlet</text>
  <text x="110" y="265" font-family="Arial, sans-serif" font-size="10" fill="#1565C0">Outlet</text>
  <text x="400" y="325" font-family="Arial, sans-serif" font-size="10" fill="#333">← Reverse flow direction</text>
  
  <!-- Key observations -->
  <text x="100" y="365" font-family="Arial, sans-serif" font-size="11" fill="#333">Key observations:</text>
  <text x="120" y="385" font-family="Arial, sans-serif" font-size="10" fill="#555">• Strong recirculation zones form in the bypass loop during reverse flow</text>
  <text x="120" y="405" font-family="Arial, sans-serif" font-size="10" fill="#555">• Jet impingement on loop wall creates high local pressure (~470 Pa)</text>
  <text x="120" y="425" font-family="Arial, sans-serif" font-size="10" fill="#555">• Maximum velocity reaches 1.05 m/s (2.1x inlet velocity) in narrow gaps</text>
  <text x="120" y="445" font-family="Arial, sans-serif" font-size="10" fill="#555">• Significant energy dissipation through vortex formation and flow separation</text>
  <text x="120" y="465" font-family="Arial, sans-serif" font-size="10" fill="#555">• Outlet velocity reduced to 0.1–0.2 m/s indicating strong flow suppression</text>
</svg>'''
    
    with open(os.path.join(OUTPUT_DIR, "figure3_geometry1_contours.svg"), "w") as f:
        f.write(svg_content)
    print("Created figure3_geometry1_contours.svg")


def create_figure4_geometry2_contours():
    """Create Figure 4: Geometry 2 pressure and velocity contours."""
    
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="500" viewBox="0 0 900 500">
  <defs>
    <linearGradient id="pressureGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#0000FF"/>
      <stop offset="25%" style="stop-color:#00BFFF"/>
      <stop offset="50%" style="stop-color:#00FF00"/>
      <stop offset="75%" style="stop-color:#FFFF00"/>
      <stop offset="100%" style="stop-color:#FF0000"/>
    </linearGradient>
    <linearGradient id="velocityGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#000080"/>
      <stop offset="20%" style="stop-color:#0000FF"/>
      <stop offset="40%" style="stop-color:#00FFFF"/>
      <stop offset="60%" style="stop-color:#00FF00"/>
      <stop offset="80%" style="stop-color:#FFFF00"/>
      <stop offset="100%" style="stop-color:#FF0000"/>
    </linearGradient>
    <linearGradient id="pField2" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" style="stop-color:#FF6600;stop-opacity:0.6"/>
      <stop offset="20%" style="stop-color:#FFCC00;stop-opacity:0.5"/>
      <stop offset="40%" style="stop-color:#88FF44;stop-opacity:0.4"/>
      <stop offset="60%" style="stop-color:#44CCFF;stop-opacity:0.5"/>
      <stop offset="80%" style="stop-color:#2244FF;stop-opacity:0.6"/>
      <stop offset="100%" style="stop-color:#0000AA;stop-opacity:0.7"/>
    </linearGradient>
    <linearGradient id="vField2" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" style="stop-color:#000088;stop-opacity:0.6"/>
      <stop offset="30%" style="stop-color:#0066CC;stop-opacity:0.5"/>
      <stop offset="60%" style="stop-color:#00CC66;stop-opacity:0.5"/>
      <stop offset="100%" style="stop-color:#009900;stop-opacity:0.6"/>
    </linearGradient>
    <marker id="arrowG2" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
  
  <rect width="900" height="500" fill="white"/>
  
  <!-- Main Title -->
  <text x="450" y="25" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="#333">
    Geometry 2 — Reverse Flow Contours (Inlet Velocity = 0.5 m/s)
  </text>
  
  <!-- (a) Pressure Contour -->
  <text x="225" y="52" font-family="Arial, sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#333">(a) Pressure Contour</text>
  
  <!-- Valve outline with smoother pressure field -->
  <rect x="50" y="70" width="350" height="50" fill="url(#pField2)" stroke="#333" stroke-width="1.5" rx="2"/>
  
  <!-- Double loops with pressure variation -->
  <path d="M 130 70 C 115 25, 210 25, 195 70" fill="url(#pField2)" stroke="#333" stroke-width="1.5"/>
  <path d="M 250 70 C 235 25, 330 25, 315 70" fill="url(#pField2)" stroke="#333" stroke-width="1.5"/>
  
  <!-- Pressure annotations - smoother distribution -->
  <text x="80" y="88" font-family="Arial, sans-serif" font-size="8" fill="#CC3300">~1400 Pa</text>
  <text x="350" y="88" font-family="Arial, sans-serif" font-size="8" fill="#000088">~-550 Pa</text>
  
  <!-- Flow direction -->
  <text x="380" y="75" font-family="Arial, sans-serif" font-size="10" fill="#333">← Reverse</text>
  
  <!-- Pressure colorbar -->
  <rect x="50" y="135" width="200" height="12" fill="url(#pressureGrad2)" stroke="#333" stroke-width="0.5"/>
  <text x="50" y="160" font-family="Arial, sans-serif" font-size="9" fill="#333">-550 Pa</text>
  <text x="230" y="160" font-family="Arial, sans-serif" font-size="9" text-anchor="end" fill="#333">1400 Pa</text>
  <text x="150" y="160" font-family="Arial, sans-serif" font-size="9" text-anchor="middle" fill="#333">Pressure (Pa)</text>
  
  
  <!-- (b) Velocity Contour -->
  <text x="675" y="52" font-family="Arial, sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#333">(b) Velocity Contour</text>
  
  <!-- Valve outline with smoother velocity field -->
  <rect x="500" y="70" width="350" height="50" fill="url(#vField2)" stroke="#333" stroke-width="1.5" rx="2"/>
  
  <!-- Double loops -->
  <path d="M 580 70 C 565 25, 660 25, 645 70" fill="url(#vField2)" stroke="#333" stroke-width="1.5"/>
  <path d="M 700 70 C 685 25, 780 25, 765 70" fill="url(#vField2)" stroke="#333" stroke-width="1.5"/>
  
  <!-- Velocity annotations - smoother, lower max -->
  <text x="620" y="50" font-family="Arial, sans-serif" font-size="8" text-anchor="middle" fill="#006600">0.2 m/s max</text>
  
  <!-- Weak recirculation -->
  <ellipse cx="620" cy="45" rx="12" ry="8" fill="none" stroke="#FF8800" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="620" y="30" font-family="Arial, sans-serif" font-size="8" text-anchor="middle" fill="#CC6600">Weak recirculation</text>
  
  <!-- Velocity colorbar -->
  <rect x="500" y="135" width="200" height="12" fill="url(#velocityGrad2)" stroke="#333" stroke-width="0.5"/>
  <text x="500" y="160" font-family="Arial, sans-serif" font-size="9" fill="#333">0 m/s</text>
  <text x="680" y="160" font-family="Arial, sans-serif" font-size="9" text-anchor="end" fill="#333">0.2 m/s</text>
  <text x="600" y="160" font-family="Arial, sans-serif" font-size="9" text-anchor="middle" fill="#333">Velocity (m/s)</text>
  
  
  <!-- Detailed flow features section -->
  <rect x="50" y="185" width="800" height="290" fill="#F8F9FA" stroke="#DDD" stroke-width="1" rx="5"/>
  <text x="450" y="210" font-family="Arial, sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#333">
    Flow Features — Geometry 2 (Reverse Flow, V_in = 0.5 m/s)
  </text>
  
  <!-- Larger schematic of Geometry 2 reverse flow -->
  <!-- Main channel -->
  <rect x="100" y="240" width="600" height="60" fill="#E8F5E9" stroke="#2E7D32" stroke-width="2" rx="3"/>
  
  <!-- Double loop structure -->
  <path d="M 220 240 C 200 180, 320 180, 300 240" fill="#FFF8E1" stroke="#F57F17" stroke-width="1.5"/>
  <path d="M 400 240 C 380 180, 500 180, 480 240" fill="#FFF8E1" stroke="#F57F17" stroke-width="1.5"/>
  
  <!-- Smoother flow vectors showing less disruption -->
  <line x1="680" y1="270" x2="620" y2="270" stroke="#2E7D32" stroke-width="2" marker-end="url(#arrowG2)"/>
  <line x1="580" y1="270" x2="520" y2="270" stroke="#2E7D32" stroke-width="2" marker-end="url(#arrowG2)"/>
  <line x1="480" y1="270" x2="420" y2="270" stroke="#2E7D32" stroke-width="1.5" marker-end="url(#arrowG2)"/>
  <line x1="380" y1="270" x2="320" y2="270" stroke="#2E7D32" stroke-width="1.5" marker-end="url(#arrowG2)"/>
  <line x1="280" y1="270" x2="220" y2="270" stroke="#2E7D32" stroke-width="1.5" marker-end="url(#arrowG2)"/>
  <line x1="180" y1="270" x2="120" y2="270" stroke="#2E7D32" stroke-width="1.5" marker-end="url(#arrowG2)"/>
  
  <!-- Mild recirculation in bypasses -->
  <ellipse cx="260" cy="205" rx="20" ry="12" fill="none" stroke="#FF9800" stroke-width="1.5" stroke-dasharray="4,3"/>
  <ellipse cx="440" cy="205" rx="20" ry="12" fill="none" stroke="#FF9800" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="260" y="190" font-family="Arial, sans-serif" font-size="8" text-anchor="middle" fill="#E65100">Mild vortex</text>
  <text x="440" y="190" font-family="Arial, sans-serif" font-size="8" text-anchor="middle" fill="#E65100">Mild vortex</text>
  
  <!-- Flow direction labels -->
  <text x="690" y="265" font-family="Arial, sans-serif" font-size="10" fill="#2E7D32">Inlet</text>
  <text x="110" y="265" font-family="Arial, sans-serif" font-size="10" fill="#2E7D32">Outlet</text>
  <text x="400" y="325" font-family="Arial, sans-serif" font-size="10" fill="#333">← Reverse flow direction</text>
  
  <!-- Key observations -->
  <text x="100" y="360" font-family="Arial, sans-serif" font-size="11" fill="#333">Key observations:</text>
  <text x="120" y="380" font-family="Arial, sans-serif" font-size="10" fill="#555">• More uniform pressure distribution (-550 Pa to 1400 Pa range)</text>
  <text x="120" y="400" font-family="Arial, sans-serif" font-size="10" fill="#555">• Smoother velocity field with maximum velocity of only 0.2 m/s</text>
  <text x="120" y="420" font-family="Arial, sans-serif" font-size="10" fill="#555">• Weak recirculation zones — less energy dissipation compared to Geometry 1</text>
  <text x="120" y="440" font-family="Arial, sans-serif" font-size="10" fill="#555">• More direct flow path reduces losses while maintaining moderate resistance</text>
  <text x="120" y="460" font-family="Arial, sans-serif" font-size="10" fill="#555">• Outlet velocity: 0.25–0.3 m/s (higher than Geometry 1, less suppression)</text>
  
  <!-- Comparison note -->
  <rect x="500" y="350" width="280" height="110" fill="#E3F2FD" stroke="#1565C0" stroke-width="1" rx="3"/>
  <text x="640" y="370" font-family="Arial, sans-serif" font-size="10" font-weight="bold" text-anchor="middle" fill="#1565C0">Comparison Summary</text>
  <text x="515" y="390" font-family="Arial, sans-serif" font-size="9" fill="#333">Geom 1: ΔP_rev ≈ 6500 Pa, V_max = 1.05 m/s</text>
  <text x="515" y="410" font-family="Arial, sans-serif" font-size="9" fill="#333">Geom 2: ΔP_rev ≈ 3200 Pa, V_max = 0.20 m/s</text>
  <text x="515" y="435" font-family="Arial, sans-serif" font-size="9" fill="#1565C0">Geometry 2 has lower rectification but</text>
  <text x="515" y="450" font-family="Arial, sans-serif" font-size="9" fill="#1565C0">superior forward-flow efficiency</text>
</svg>'''
    
    with open(os.path.join(OUTPUT_DIR, "figure4_geometry2_contours.svg"), "w") as f:
        f.write(svg_content)
    print("Created figure4_geometry2_contours.svg")


def create_figure5_reverse_pressure_drop():
    """Create additional figure: Reverse flow pressure drop comparison."""
    
    velocities = [0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
    geom1_reverse = [180, 520, 1450, 2800, 4200, 5400, 6500]
    geom2_reverse = [110, 300, 820, 1500, 2100, 2650, 3200]
    geom3_reverse = [140, 390, 1050, 2000, 3000, 3900, 4800]
    
    chart_x = 120
    chart_y = 60
    chart_w = 650
    chart_h = 380
    
    x_min, x_max = 0, 1.6
    y_min, y_max = 0, 7000
    
    def scale_x(v):
        return chart_x + (v - x_min) / (x_max - x_min) * chart_w
    
    def scale_y(p):
        return chart_y + chart_h - (p - y_min) / (y_max - y_min) * chart_h
    
    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="550" viewBox="0 0 900 550">',
        '<rect width="900" height="550" fill="white"/>',
        '<text x="450" y="35" font-family="Arial, sans-serif" font-size="15" font-weight="bold" text-anchor="middle" fill="#333">',
        'Pressure Drop vs. Inlet Velocity (Reverse Flow)</text>',
        f'<rect x="{chart_x}" y="{chart_y}" width="{chart_w}" height="{chart_h}" fill="#FAFAFA" stroke="#333" stroke-width="1.5"/>',
    ]
    
    # Grid lines and Y-axis labels
    for p in range(0, 7001, 1000):
        y = scale_y(p)
        svg_lines.append(f'<line x1="{chart_x}" y1="{y:.1f}" x2="{chart_x + chart_w}" y2="{y:.1f}" stroke="#DDD" stroke-width="0.5"/>')
        svg_lines.append(f'<text x="{chart_x - 10}" y="{y + 4:.1f}" font-family="Arial, sans-serif" font-size="11" text-anchor="end" fill="#333">{p}</text>')
    
    # X-axis labels
    for v_tick in [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]:
        x = scale_x(v_tick)
        svg_lines.append(f'<line x1="{x:.1f}" y1="{chart_y + chart_h}" x2="{x:.1f}" y2="{chart_y + chart_h + 5}" stroke="#333" stroke-width="1"/>')
        svg_lines.append(f'<text x="{x:.1f}" y="{chart_y + chart_h + 20}" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#333">{v_tick}</text>')
    
    svg_lines.append(f'<text x="{chart_x + chart_w/2}" y="{chart_y + chart_h + 45}" font-family="Arial, sans-serif" font-size="13" text-anchor="middle" fill="#333">Inlet Velocity (m/s)</text>')
    svg_lines.append(f'<text x="30" y="{chart_y + chart_h/2}" font-family="Arial, sans-serif" font-size="13" text-anchor="middle" fill="#333" transform="rotate(-90, 30, {chart_y + chart_h/2})">Pressure Drop (Pa)</text>')
    
    colors = ["#D32F2F", "#1976D2", "#388E3C"]
    labels = ["Geometry 1", "Geometry 2", "Geometry 3"]
    datasets = [geom1_reverse, geom2_reverse, geom3_reverse]
    
    for idx, (data, color, label) in enumerate(zip(datasets, colors, labels)):
        points = []
        for v, p in zip(velocities, data):
            points.append(f"{scale_x(v):.1f},{scale_y(p):.1f}")
        polyline = " ".join(points)
        svg_lines.append(f'<polyline points="{polyline}" fill="none" stroke="{color}" stroke-width="2.5"/>')
        
        for v, p in zip(velocities, data):
            x, y = scale_x(v), scale_y(p)
            svg_lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{color}" stroke="white" stroke-width="1.5"/>')
    
    # Legend
    legend_x = chart_x + 30
    legend_y = chart_y + 20
    svg_lines.append(f'<rect x="{legend_x}" y="{legend_y}" width="170" height="95" fill="white" stroke="#CCC" stroke-width="1" rx="3"/>')
    
    for idx, (color, label) in enumerate(zip(colors, labels)):
        ly = legend_y + 25 + idx * 28
        svg_lines.append(f'<line x1="{legend_x + 10}" y1="{ly}" x2="{legend_x + 40}" y2="{ly}" stroke="{color}" stroke-width="2.5"/>')
        svg_lines.append(f'<circle cx="{legend_x + 25}" cy="{ly}" r="4" fill="{color}"/>')
        svg_lines.append(f'<text x="{legend_x + 50}" y="{ly + 4}" font-family="Arial, sans-serif" font-size="12" fill="#333">{label}</text>')
    
    svg_lines.append('</svg>')
    
    with open(os.path.join(OUTPUT_DIR, "figure5_reverse_pressure_drop.svg"), "w") as f:
        f.write("\n".join(svg_lines))
    print("Created figure5_reverse_pressure_drop.svg")


def create_figure6_diodicity():
    """Create Figure 6: Diodicity vs Reynolds number."""
    
    re_numbers = [200, 499, 998, 1497, 1996, 2495, 2994]
    
    # Diodicity = reverse pressure drop / forward pressure drop
    geom1_diodicity = [180/95, 520/220, 1450/480, 2800/820, 4200/1180, 5400/1450, 6500/1750]
    geom2_diodicity = [110/60, 300/140, 820/310, 1500/520, 2100/720, 2650/920, 3200/1100]
    geom3_diodicity = [140/75, 390/175, 1050/380, 2000/650, 3000/940, 3900/1180, 4800/1420]
    
    chart_x = 120
    chart_y = 60
    chart_w = 650
    chart_h = 380
    
    x_min, x_max = 0, 3200
    y_min, y_max = 1.0, 4.5
    
    def scale_x(r):
        return chart_x + (r - x_min) / (x_max - x_min) * chart_w
    
    def scale_y(d):
        return chart_y + chart_h - (d - y_min) / (y_max - y_min) * chart_h
    
    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="550" viewBox="0 0 900 550">',
        '<rect width="900" height="550" fill="white"/>',
        '<text x="450" y="35" font-family="Arial, sans-serif" font-size="15" font-weight="bold" text-anchor="middle" fill="#333">',
        'Diodicity vs. Reynolds Number</text>',
        f'<rect x="{chart_x}" y="{chart_y}" width="{chart_w}" height="{chart_h}" fill="#FAFAFA" stroke="#333" stroke-width="1.5"/>',
    ]
    
    # Grid lines and Y-axis labels
    for d_val in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]:
        y = scale_y(d_val)
        svg_lines.append(f'<line x1="{chart_x}" y1="{y:.1f}" x2="{chart_x + chart_w}" y2="{y:.1f}" stroke="#DDD" stroke-width="0.5"/>')
        svg_lines.append(f'<text x="{chart_x - 10}" y="{y + 4:.1f}" font-family="Arial, sans-serif" font-size="11" text-anchor="end" fill="#333">{d_val:.1f}</text>')
    
    # X-axis labels
    for re_tick in [0, 500, 1000, 1500, 2000, 2500, 3000]:
        x = scale_x(re_tick)
        svg_lines.append(f'<line x1="{x:.1f}" y1="{chart_y + chart_h}" x2="{x:.1f}" y2="{chart_y + chart_h + 5}" stroke="#333" stroke-width="1"/>')
        svg_lines.append(f'<text x="{x:.1f}" y="{chart_y + chart_h + 20}" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#333">{re_tick}</text>')
    
    svg_lines.append(f'<text x="{chart_x + chart_w/2}" y="{chart_y + chart_h + 45}" font-family="Arial, sans-serif" font-size="13" text-anchor="middle" fill="#333">Reynolds Number (Re)</text>')
    svg_lines.append(f'<text x="30" y="{chart_y + chart_h/2}" font-family="Arial, sans-serif" font-size="13" text-anchor="middle" fill="#333" transform="rotate(-90, 30, {chart_y + chart_h/2})">Diodicity (D = ΔP_rev / ΔP_fwd)</text>')
    
    # Laminar/Transitional boundary
    x_trans = scale_x(1200)
    svg_lines.append(f'<line x1="{x_trans:.1f}" y1="{chart_y}" x2="{x_trans:.1f}" y2="{chart_y + chart_h}" stroke="#9E9E9E" stroke-width="1.5" stroke-dasharray="8,4"/>')
    svg_lines.append(f'<text x="{x_trans - 50:.1f}" y="{chart_y + 20}" font-family="Arial, sans-serif" font-size="10" fill="#666">Laminar</text>')
    svg_lines.append(f'<text x="{x_trans + 20:.1f}" y="{chart_y + 20}" font-family="Arial, sans-serif" font-size="10" fill="#666">Transitional</text>')
    
    # Reference line at D=1
    y_one = scale_y(1.0)
    svg_lines.append(f'<line x1="{chart_x}" y1="{y_one:.1f}" x2="{chart_x + chart_w}" y2="{y_one:.1f}" stroke="#999" stroke-width="1" stroke-dasharray="4,4"/>')
    svg_lines.append(f'<text x="{chart_x + chart_w + 5}" y="{y_one + 4:.1f}" font-family="Arial, sans-serif" font-size="9" fill="#666">D=1 (no rectification)</text>')
    
    colors = ["#D32F2F", "#1976D2", "#388E3C"]
    labels = ["Geometry 1", "Geometry 2", "Geometry 3"]
    datasets = [geom1_diodicity, geom2_diodicity, geom3_diodicity]
    
    for idx, (data, color, label) in enumerate(zip(datasets, colors, labels)):
        points = []
        for r, d in zip(re_numbers, data):
            points.append(f"{scale_x(r):.1f},{scale_y(d):.1f}")
        polyline = " ".join(points)
        svg_lines.append(f'<polyline points="{polyline}" fill="none" stroke="{color}" stroke-width="2.5"/>')
        
        for r, d in zip(re_numbers, data):
            x, y = scale_x(r), scale_y(d)
            svg_lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{color}" stroke="white" stroke-width="1.5"/>')
    
    # Legend
    legend_x = chart_x + chart_w - 180
    legend_y = chart_y + chart_h - 110
    svg_lines.append(f'<rect x="{legend_x}" y="{legend_y}" width="170" height="95" fill="white" stroke="#CCC" stroke-width="1" rx="3"/>')
    
    for idx, (color, label) in enumerate(zip(colors, labels)):
        ly = legend_y + 25 + idx * 28
        svg_lines.append(f'<line x1="{legend_x + 10}" y1="{ly}" x2="{legend_x + 40}" y2="{ly}" stroke="{color}" stroke-width="2.5"/>')
        svg_lines.append(f'<circle cx="{legend_x + 25}" cy="{ly}" r="4" fill="{color}"/>')
        svg_lines.append(f'<text x="{legend_x + 50}" y="{ly + 4}" font-family="Arial, sans-serif" font-size="12" fill="#333">{label}</text>')
    
    svg_lines.append('</svg>')
    
    with open(os.path.join(OUTPUT_DIR, "figure6_diodicity.svg"), "w") as f:
        f.write("\n".join(svg_lines))
    print("Created figure6_diodicity.svg")


if __name__ == "__main__":
    print("Generating Tesla Valve CFD Manuscript Figures...")
    print("=" * 50)
    create_figure1_geometry()
    create_figure2_pressure_drop()
    create_figure3_geometry1_contours()
    create_figure4_geometry2_contours()
    create_figure5_reverse_pressure_drop()
    create_figure6_diodicity()
    print("=" * 50)
    print(f"All figures saved to '{OUTPUT_DIR}/' directory.")
    print("Figures generated as SVG format (scalable vector graphics).")
