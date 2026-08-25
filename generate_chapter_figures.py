#!/usr/bin/env python3
"""
Generate 4 figures for the Sustainable Manufacturing chapter as PNG files.
Uses only Python standard library (struct, zlib) to create PNG images.
"""

import struct
import zlib
import os

def create_png(width, height, pixels, filename):
    """Create a PNG file from pixel data (list of rows, each row is list of (R,G,B) tuples)."""
    def make_chunk(chunk_type, data):
        chunk = chunk_type + data
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', zlib.crc32(chunk) & 0xFFFFFFFF)
    
    # PNG signature
    signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = make_chunk(b'IHDR', ihdr_data)
    
    # IDAT chunk - image data
    raw_data = b''
    for row in pixels:
        raw_data += b'\x00'  # filter type: None
        for r, g, b in row:
            raw_data += struct.pack('BBB', r, g, b)
    
    compressed = zlib.compress(raw_data)
    idat = make_chunk(b'IDAT', compressed)
    
    # IEND chunk
    iend = make_chunk(b'IEND', b'')
    
    with open(filename, 'wb') as f:
        f.write(signature + ihdr + idat + iend)

def draw_rect(pixels, x1, y1, x2, y2, color):
    """Draw a filled rectangle."""
    for y in range(max(0, y1), min(len(pixels), y2)):
        for x in range(max(0, x1), min(len(pixels[0]), x2)):
            pixels[y][x] = color

def draw_border(pixels, x1, y1, x2, y2, color, thickness=2):
    """Draw a rectangle border."""
    for t in range(thickness):
        for x in range(x1, x2):
            if y1+t < len(pixels):
                pixels[y1+t][x] = color
            if y2-1-t >= 0 and y2-1-t < len(pixels):
                pixels[y2-1-t][x] = color
        for y in range(y1, y2):
            if x1+t < len(pixels[0]):
                pixels[y][x1+t] = color
            if x2-1-t >= 0 and x2-1-t < len(pixels[0]):
                pixels[y][x2-1-t] = color

def draw_bar(pixels, x, y, width, height, color):
    """Draw a bar (for bar charts)."""
    draw_rect(pixels, x, y - height, x + width, y, color)

def draw_line(pixels, x1, y1, x2, y2, color, thickness=2):
    """Draw a line using Bresenham's algorithm."""
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    
    while True:
        for t in range(-thickness//2, thickness//2 + 1):
            if 0 <= y1+t < len(pixels) and 0 <= x1 < len(pixels[0]):
                pixels[y1+t][x1] = color
            if 0 <= y1 < len(pixels) and 0 <= x1+t < len(pixels[0]):
                pixels[y1][x1+t] = color
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def draw_circle(pixels, cx, cy, r, color, filled=True):
    """Draw a circle."""
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if filled and dist <= r:
                if 0 <= y < len(pixels) and 0 <= x < len(pixels[0]):
                    pixels[y][x] = color
            elif not filled and abs(dist - r) < 1.5:
                if 0 <= y < len(pixels) and 0 <= x < len(pixels[0]):
                    pixels[y][x] = color

def draw_arrow(pixels, x1, y1, x2, y2, color, thickness=2):
    """Draw an arrow from (x1,y1) to (x2,y2)."""
    draw_line(pixels, x1, y1, x2, y2, color, thickness)
    # Arrowhead
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 10
    for a_offset in [-0.4, 0.4]:
        ax = int(x2 - arrow_len * math.cos(angle + a_offset))
        ay = int(y2 - arrow_len * math.sin(angle + a_offset))
        draw_line(pixels, x2, y2, ax, ay, color, thickness)

def create_gradient_bg(width, height, color1, color2):
    """Create gradient background."""
    pixels = []
    for y in range(height):
        row = []
        t = y / height
        r = int(color1[0] * (1-t) + color2[0] * t)
        g = int(color1[1] * (1-t) + color2[1] * t)
        b = int(color1[2] * (1-t) + color2[2] * t)
        for x in range(width):
            row.append((r, g, b))
        pixels.append(row)
    return pixels

# ============================================================
# Figure 1: Bio-Derived Materials Performance Comparison
# ============================================================
def generate_figure1():
    width, height = 800, 500
    bg_color = (255, 255, 255)
    pixels = [[bg_color for _ in range(width)] for _ in range(height)]
    
    # Title area (top)
    draw_rect(pixels, 0, 0, width, 50, (40, 60, 100))
    
    # Chart area
    chart_left = 100
    chart_right = 750
    chart_top = 80
    chart_bottom = 420
    
    # Draw axes
    draw_line(pixels, chart_left, chart_bottom, chart_right, chart_bottom, (50, 50, 50), 2)
    draw_line(pixels, chart_left, chart_top, chart_left, chart_bottom, (50, 50, 50), 2)
    
    # Y-axis grid lines
    for i in range(5):
        y = chart_bottom - int((chart_bottom - chart_top) * (i+1) / 5)
        draw_line(pixels, chart_left, y, chart_right, y, (220, 220, 220), 1)
    
    # Bar data: Performance metrics for different bio-derived materials
    # Categories: Lignin CF, Chitosan, Cellulose NM, Mycelium
    # Metrics: Tensile Strength, Conductivity, Sustainability Score
    colors = [
        (46, 134, 193),   # Blue - Lignin Carbon Fibers
        (39, 174, 96),    # Green - Chitosan Substrates
        (243, 156, 18),   # Orange - Cellulose Nanomaterials
        (155, 89, 182),   # Purple - Mycelium Composites
    ]
    
    bar_groups = 4  # materials
    bars_per_group = 3  # metrics
    group_width = (chart_right - chart_left - 60) // bar_groups
    bar_width = group_width // (bars_per_group + 1)
    
    # Performance data (normalized 0-100)
    data = [
        [85, 92, 78],   # Lignin CF: strength, conductivity, sustainability
        [55, 60, 95],   # Chitosan: strength, conductivity, sustainability
        [90, 45, 88],   # Cellulose NM: strength, conductivity, sustainability
        [40, 30, 97],   # Mycelium: strength, conductivity, sustainability
    ]
    
    max_bar_height = chart_bottom - chart_top - 20
    
    for g in range(bar_groups):
        group_x = chart_left + 30 + g * group_width
        for b in range(bars_per_group):
            bar_x = group_x + b * (bar_width + 3)
            bar_height = int(data[g][b] / 100 * max_bar_height)
            bar_y = chart_bottom - bar_height
            
            # Main bar
            color = colors[g]
            # Vary shade for different metrics
            shade = [1.0, 0.75, 0.55][b]
            bar_color = (int(color[0]*shade), int(color[1]*shade), int(color[2]*shade))
            draw_rect(pixels, bar_x, bar_y, bar_x + bar_width, chart_bottom, bar_color)
            draw_border(pixels, bar_x, bar_y, bar_x + bar_width, chart_bottom, (30, 30, 30), 1)
    
    # Legend area
    legend_y = 455
    legend_items = [
        ("Lignin Carbon Fibers", colors[0]),
        ("Chitosan Substrates", colors[1]),
        ("Cellulose Nanomaterials", colors[2]),
        ("Mycelium Composites", colors[3]),
    ]
    for i, (name, color) in enumerate(legend_items):
        x = 100 + i * 170
        draw_rect(pixels, x, legend_y, x + 20, legend_y + 15, color)
        draw_border(pixels, x, legend_y, x + 20, legend_y + 15, (0, 0, 0), 1)
    
    # Metric legend
    metric_y = 478
    metric_colors_labels = [
        ((80, 80, 80), "Dark=Strength"),
        ((140, 140, 140), "Mid=Conductivity"),
        ((200, 200, 200), "Light=Sustainability"),
    ]
    for i, (c, label) in enumerate(metric_colors_labels):
        x = 180 + i * 200
        draw_rect(pixels, x, metric_y, x + 15, metric_y + 12, c)
    
    create_png(width, height, pixels, os.path.join(output_dir, 'Figure_1_BioMaterials_Performance.png'))
    print("Figure 1 created: Bio-Derived Materials Performance Comparison")

# ============================================================
# Figure 2: Digital Twin Three-Layer Architecture
# ============================================================
def generate_figure2():
    width, height = 800, 550
    bg_color = (248, 249, 250)
    pixels = [[bg_color for _ in range(width)] for _ in range(height)]
    
    # Title bar
    draw_rect(pixels, 0, 0, width, 45, (33, 97, 140))
    
    # Layer 1: Physical Layer (bottom)
    draw_rect(pixels, 80, 380, 720, 480, (214, 234, 248))
    draw_border(pixels, 80, 380, 720, 480, (33, 97, 140), 3)
    # Components inside
    draw_rect(pixels, 120, 405, 230, 455, (174, 214, 241))
    draw_border(pixels, 120, 405, 230, 455, (33, 97, 140), 2)
    draw_rect(pixels, 270, 405, 380, 455, (174, 214, 241))
    draw_border(pixels, 270, 405, 380, 455, (33, 97, 140), 2)
    draw_rect(pixels, 420, 405, 530, 455, (174, 214, 241))
    draw_border(pixels, 420, 405, 530, 455, (33, 97, 140), 2)
    draw_rect(pixels, 570, 405, 680, 455, (174, 214, 241))
    draw_border(pixels, 570, 405, 680, 455, (33, 97, 140), 2)
    
    # Layer 2: DT Engine (middle)
    draw_rect(pixels, 80, 220, 720, 340, (212, 239, 223))
    draw_border(pixels, 80, 220, 720, 340, (30, 132, 73), 3)
    # Sub-components
    draw_rect(pixels, 120, 245, 280, 310, (171, 235, 198))
    draw_border(pixels, 120, 245, 280, 310, (30, 132, 73), 2)
    draw_rect(pixels, 320, 245, 480, 310, (171, 235, 198))
    draw_border(pixels, 320, 245, 480, 310, (30, 132, 73), 2)
    draw_rect(pixels, 520, 245, 680, 310, (171, 235, 198))
    draw_border(pixels, 520, 245, 680, 310, (30, 132, 73), 2)
    
    # Layer 3: Virtual Model (top)
    draw_rect(pixels, 80, 70, 720, 180, (253, 237, 236))
    draw_border(pixels, 80, 70, 720, 180, (176, 58, 46), 3)
    # Sub-components
    draw_rect(pixels, 120, 95, 300, 155, (245, 203, 199))
    draw_border(pixels, 120, 95, 300, 155, (176, 58, 46), 2)
    draw_rect(pixels, 340, 95, 520, 155, (245, 203, 199))
    draw_border(pixels, 340, 95, 520, 155, (176, 58, 46), 2)
    draw_rect(pixels, 560, 95, 700, 155, (245, 203, 199))
    draw_border(pixels, 560, 95, 700, 155, (176, 58, 46), 2)
    
    # Arrows between layers
    # Physical -> DT Engine
    draw_arrow(pixels, 250, 380, 250, 340, (100, 100, 100), 2)
    draw_arrow(pixels, 400, 380, 400, 340, (100, 100, 100), 2)
    draw_arrow(pixels, 550, 380, 550, 340, (100, 100, 100), 2)
    
    # DT Engine -> Virtual Model
    draw_arrow(pixels, 250, 220, 250, 180, (100, 100, 100), 2)
    draw_arrow(pixels, 400, 220, 400, 180, (100, 100, 100), 2)
    draw_arrow(pixels, 550, 220, 550, 180, (100, 100, 100), 2)
    
    # Feedback arrows (right side)
    draw_line(pixels, 730, 125, 730, 430, (200, 50, 50), 2)
    draw_arrow(pixels, 730, 430, 720, 430, (200, 50, 50), 2)
    
    # Side labels represented as colored dots
    draw_circle(pixels, 50, 125, 12, (176, 58, 46))
    draw_circle(pixels, 50, 280, 12, (30, 132, 73))
    draw_circle(pixels, 50, 430, 12, (33, 97, 140))
    
    # AGV/RFID indicators at bottom
    draw_rect(pixels, 80, 500, 250, 535, (253, 237, 236))
    draw_border(pixels, 80, 500, 250, 535, (120, 120, 120), 1)
    draw_rect(pixels, 280, 500, 480, 535, (253, 237, 236))
    draw_border(pixels, 280, 500, 480, 535, (120, 120, 120), 1)
    draw_rect(pixels, 510, 500, 720, 535, (253, 237, 236))
    draw_border(pixels, 510, 500, 720, 535, (120, 120, 120), 1)
    
    create_png(width, height, pixels, os.path.join(output_dir, 'Figure_2_Digital_Twin_Architecture.png'))
    print("Figure 2 created: Digital Twin Three-Layer Architecture")

# ============================================================
# Figure 3: Circular Economy Framework - Multi-Level System
# ============================================================
def generate_figure3():
    width, height = 800, 550
    bg_color = (255, 255, 255)
    pixels = [[bg_color for _ in range(width)] for _ in range(height)]
    
    # Title bar
    draw_rect(pixels, 0, 0, width, 45, (39, 174, 96))
    
    # Three concentric rings representing micro, meso, macro levels
    cx, cy = 400, 300
    
    # Macro level (outer ring)
    draw_circle(pixels, cx, cy, 210, (214, 234, 248), filled=True)
    draw_circle(pixels, cx, cy, 210, (33, 97, 140), filled=False)
    
    # Meso level (middle ring)
    draw_circle(pixels, cx, cy, 150, (212, 239, 223), filled=True)
    draw_circle(pixels, cx, cy, 150, (30, 132, 73), filled=False)
    
    # Micro level (inner ring)
    draw_circle(pixels, cx, cy, 85, (253, 237, 236), filled=True)
    draw_circle(pixels, cx, cy, 85, (176, 58, 46), filled=False)
    
    # Center - product/component
    draw_circle(pixels, cx, cy, 30, (155, 89, 182), filled=True)
    
    # Circular arrows around the center (simplified as arc segments)
    import math
    # Draw flow arrows at micro level
    for angle_deg in [0, 90, 180, 270]:
        angle = math.radians(angle_deg)
        r = 60
        x = int(cx + r * math.cos(angle))
        y = int(cy + r * math.sin(angle))
        draw_circle(pixels, x, y, 5, (176, 58, 46), filled=True)
    
    # Draw flow indicators at meso level
    for angle_deg in [30, 120, 210, 300]:
        angle = math.radians(angle_deg)
        r = 120
        x = int(cx + r * math.cos(angle))
        y = int(cy + r * math.sin(angle))
        draw_circle(pixels, x, y, 8, (30, 132, 73), filled=True)
    
    # Draw policy/market indicators at macro level
    for angle_deg in [15, 75, 135, 195, 255, 315]:
        angle = math.radians(angle_deg)
        r = 180
        x = int(cx + r * math.cos(angle))
        y = int(cy + r * math.sin(angle))
        draw_rect(pixels, x-10, y-10, x+10, y+10, (33, 97, 140))
    
    # Connecting lines from center outward
    for angle_deg in [45, 135, 225, 315]:
        angle = math.radians(angle_deg)
        x1 = int(cx + 35 * math.cos(angle))
        y1 = int(cy + 35 * math.sin(angle))
        x2 = int(cx + 200 * math.cos(angle))
        y2 = int(cy + 200 * math.sin(angle))
        draw_line(pixels, x1, y1, x2, y2, (180, 180, 180), 1)
    
    # Legend boxes (bottom)
    legend_y = 520
    draw_rect(pixels, 100, legend_y, 120, legend_y+20, (253, 237, 236))
    draw_border(pixels, 100, legend_y, 120, legend_y+20, (176, 58, 46), 2)
    
    draw_rect(pixels, 280, legend_y, 300, legend_y+20, (212, 239, 223))
    draw_border(pixels, 280, legend_y, 300, legend_y+20, (30, 132, 73), 2)
    
    draw_rect(pixels, 480, legend_y, 500, legend_y+20, (214, 234, 248))
    draw_border(pixels, 480, legend_y, 500, legend_y+20, (33, 97, 140), 2)
    
    # Side labels
    # Left: enablers
    draw_rect(pixels, 20, 150, 80, 200, (243, 156, 18))
    draw_border(pixels, 20, 150, 80, 200, (200, 120, 0), 2)
    draw_rect(pixels, 20, 220, 80, 270, (243, 156, 18))
    draw_border(pixels, 20, 220, 80, 270, (200, 120, 0), 2)
    draw_rect(pixels, 20, 290, 80, 340, (243, 156, 18))
    draw_border(pixels, 20, 290, 80, 340, (200, 120, 0), 2)
    draw_rect(pixels, 20, 360, 80, 410, (243, 156, 18))
    draw_border(pixels, 20, 360, 80, 410, (200, 120, 0), 2)
    
    # Right: barriers
    draw_rect(pixels, 720, 150, 780, 200, (192, 57, 43))
    draw_rect(pixels, 720, 220, 780, 270, (192, 57, 43))
    draw_rect(pixels, 720, 290, 780, 340, (192, 57, 43))
    draw_rect(pixels, 720, 360, 780, 410, (192, 57, 43))
    
    # Arrows from enablers to circle
    draw_arrow(pixels, 80, 175, 190, 250, (243, 156, 18), 2)
    draw_arrow(pixels, 80, 350, 190, 340, (243, 156, 18), 2)
    
    create_png(width, height, pixels, os.path.join(output_dir, 'Figure_3_Circular_Economy_Framework.png'))
    print("Figure 3 created: Circular Economy Multi-Level Framework")

# ============================================================
# Figure 4: Net-Zero Manufacturing Integration Roadmap
# ============================================================
def generate_figure4():
    width, height = 800, 500
    bg_color = (255, 255, 255)
    pixels = [[bg_color for _ in range(width)] for _ in range(height)]
    
    # Title bar
    draw_rect(pixels, 0, 0, width, 45, (142, 68, 173))
    
    # Timeline arrow
    draw_rect(pixels, 60, 245, 740, 255, (180, 180, 180))
    draw_arrow(pixels, 60, 250, 750, 250, (100, 100, 100), 3)
    
    # Phase boxes along timeline
    phases = [
        (100, "Phase 1", (46, 134, 193)),
        (270, "Phase 2", (39, 174, 96)),
        (440, "Phase 3", (243, 156, 18)),
        (610, "Phase 4", (142, 68, 173)),
    ]
    
    for x, label, color in phases:
        # Main phase box (above timeline)
        draw_rect(pixels, x, 80, x+130, 230, color)
        draw_border(pixels, x, 80, x+130, 230, 
                   (max(0, color[0]-40), max(0, color[1]-40), max(0, color[2]-40)), 2)
        
        # Sub-elements inside box
        inner_color = (min(255, color[0]+60), min(255, color[1]+60), min(255, color[2]+60))
        draw_rect(pixels, x+10, 95, x+120, 125, inner_color)
        draw_rect(pixels, x+10, 135, x+120, 165, inner_color)
        draw_rect(pixels, x+10, 175, x+120, 205, inner_color)
        
        # Connection point to timeline
        draw_circle(pixels, x+65, 250, 8, color, filled=True)
        draw_line(pixels, x+65, 230, x+65, 242, color, 2)
        
        # Below timeline - outcomes
        draw_rect(pixels, x, 270, x+130, 420, 
                 (min(255, color[0]+100), min(255, color[1]+100), min(255, color[2]+100)))
        draw_border(pixels, x, 270, x+130, 420, color, 2)
        
        # Sub-elements below
        for i in range(4):
            y_pos = 285 + i * 33
            draw_rect(pixels, x+10, y_pos, x+120, y_pos+25, 
                     (min(255, color[0]+140), min(255, color[1]+140), min(255, color[2]+140)))
            draw_border(pixels, x+10, y_pos, x+120, y_pos+25, color, 1)
    
    # Connecting arrows between phases
    for i in range(3):
        x1 = phases[i][0] + 130
        x2 = phases[i+1][0]
        draw_arrow(pixels, x1, 155, x2, 155, (100, 100, 100), 2)
    
    # Bottom integration bar
    draw_rect(pixels, 60, 440, 740, 485, (52, 73, 94))
    # Sections within
    section_width = (740 - 60) // 4
    for i in range(4):
        x = 60 + i * section_width
        draw_border(pixels, x, 440, x + section_width, 485, (255, 255, 255), 1)
    
    create_png(width, height, pixels, os.path.join(output_dir, 'Figure_4_NetZero_Integration_Roadmap.png'))
    print("Figure 4 created: Net-Zero Manufacturing Integration Roadmap")

# ============================================================
# Main execution
# ============================================================
if __name__ == '__main__':
    output_dir = '/projects/sandbox/AMMAN/chapter_figures'
    os.makedirs(output_dir, exist_ok=True)
    
    generate_figure1()
    generate_figure2()
    generate_figure3()
    generate_figure4()
    
    print(f"\nAll 4 figures generated in: {output_dir}")
    for f in os.listdir(output_dir):
        print(f"  - {f}")
