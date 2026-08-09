#!/usr/bin/env python3
"""Generate 4 figures for AI-Driven Contract Analytics chapter using pure Python PNG creation."""

import struct
import zlib
import os

def create_png(width, height, pixels):
    """Create a PNG file from raw pixel data. pixels is list of rows, each row is list of (R,G,B) tuples."""
    def make_chunk(chunk_type, data):
        chunk = chunk_type + data
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', zlib.crc32(chunk) & 0xffffffff)
    
    header = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = make_chunk(b'IHDR', ihdr_data)
    
    raw_data = b''
    for row in pixels:
        raw_data += b'\x00'  # filter byte
        for r, g, b in row:
            raw_data += struct.pack('BBB', r, g, b)
    
    compressed = zlib.compress(raw_data)
    idat = make_chunk(b'IDAT', compressed)
    iend = make_chunk(b'IEND', b'')
    
    return header + ihdr + idat + iend

def draw_rect(pixels, x1, y1, x2, y2, color):
    """Draw a filled rectangle."""
    for y in range(max(0, y1), min(len(pixels), y2)):
        for x in range(max(0, x1), min(len(pixels[0]), x2)):
            pixels[y][x] = color

def draw_text_block(pixels, x, y, w, h, color):
    """Draw a text-like block (solid rectangle representing text area)."""
    draw_rect(pixels, x, y, x+w, y+h, color)


def draw_horizontal_line(pixels, x1, x2, y, color, thickness=2):
    """Draw a horizontal line."""
    for t in range(thickness):
        if y+t < len(pixels):
            for x in range(max(0, x1), min(len(pixels[0]), x2)):
                pixels[y+t][x] = color

def draw_vertical_line(pixels, x, y1, y2, color, thickness=2):
    """Draw a vertical line."""
    for t in range(thickness):
        if x+t < len(pixels[0]):
            for y in range(max(0, y1), min(len(pixels), y2)):
                pixels[y][x+t] = color

def draw_arrow_right(pixels, x1, x2, y, color, thickness=2):
    """Draw a right-pointing arrow."""
    draw_horizontal_line(pixels, x1, x2, y, color, thickness)
    # Arrowhead
    for i in range(8):
        if y-i >= 0 and x2-i < len(pixels[0]):
            pixels[y-i][x2-i] = color
        if y+i < len(pixels) and x2-i < len(pixels[0]):
            pixels[y+i][x2-i] = color

def draw_arrow_down(pixels, x, y1, y2, color, thickness=2):
    """Draw a downward-pointing arrow."""
    draw_vertical_line(pixels, x, y1, y2, color, thickness)
    for i in range(8):
        if x-i >= 0 and y2-i < len(pixels):
            pixels[y2-i][x-i] = color
        if x+i < len(pixels[0]) and y2-i < len(pixels):
            pixels[y2-i][x+i] = color

def create_blank(width, height, bg_color=(255, 255, 255)):
    """Create blank pixel grid."""
    return [[bg_color for _ in range(width)] for _ in range(height)]


def generate_figure1():
    """Figure 1: Architecture of AI-Driven Contract Analytics Platform."""
    w, h = 800, 600
    pixels = create_blank(w, h, (248, 249, 250))
    
    # Title area
    draw_rect(pixels, 200, 10, 600, 40, (33, 37, 41))
    
    # Layer 1: Data Sources (top)
    colors_l1 = [(52, 152, 219), (41, 128, 185), (52, 152, 219), (41, 128, 185)]
    labels_x = [50, 230, 410, 590]
    for i, x in enumerate(labels_x):
        draw_rect(pixels, x, 60, x+160, 110, colors_l1[i])
        draw_rect(pixels, x+10, 70, x+150, 100, (255, 255, 255))
    
    # Arrows down from layer 1
    for x in [130, 310, 490, 670]:
        draw_arrow_down(pixels, x, 112, 140, (100, 100, 100))
    
    # Layer 2: Processing Engine
    draw_rect(pixels, 50, 145, 750, 230, (46, 204, 113))
    draw_rect(pixels, 70, 160, 250, 215, (255, 255, 255))
    draw_rect(pixels, 270, 160, 450, 215, (255, 255, 255))
    draw_rect(pixels, 470, 160, 650, 215, (255, 255, 255))
    
    # Arrow down
    draw_arrow_down(pixels, 400, 232, 260, (100, 100, 100))
    
    # Layer 3: AI/ML Engine
    draw_rect(pixels, 50, 265, 750, 370, (155, 89, 182))
    draw_rect(pixels, 70, 280, 220, 355, (255, 255, 255))
    draw_rect(pixels, 240, 280, 390, 355, (255, 255, 255))
    draw_rect(pixels, 410, 280, 560, 355, (255, 255, 255))
    draw_rect(pixels, 580, 280, 730, 355, (255, 255, 255))
    
    # Arrow down
    draw_arrow_down(pixels, 400, 372, 400, (100, 100, 100))
    
    # Layer 4: Knowledge Repository
    draw_rect(pixels, 150, 405, 650, 470, (230, 126, 34))
    draw_rect(pixels, 170, 420, 350, 455, (255, 255, 255))
    draw_rect(pixels, 370, 420, 550, 455, (255, 255, 255))
    
    # Arrow down
    draw_arrow_down(pixels, 400, 472, 500, (100, 100, 100))
    
    # Layer 5: Decision Support Interface
    draw_rect(pixels, 100, 505, 700, 580, (231, 76, 60))
    draw_rect(pixels, 120, 520, 300, 565, (255, 255, 255))
    draw_rect(pixels, 320, 520, 500, 565, (255, 255, 255))
    draw_rect(pixels, 520, 520, 680, 565, (255, 255, 255))
    
    return create_png(w, h, pixels)


def generate_figure2():
    """Figure 2: AI-Driven Contract Lifecycle Management Workflow."""
    w, h = 800, 500
    pixels = create_blank(w, h, (248, 249, 250))
    
    # Title bar
    draw_rect(pixels, 150, 10, 650, 40, (33, 37, 41))
    
    # Workflow stages (horizontal flow)
    stage_colors = [(52, 152, 219), (46, 204, 113), (155, 89, 182), 
                    (230, 126, 34), (231, 76, 60)]
    stage_x = [30, 180, 330, 480, 630]
    
    for i, x in enumerate(stage_x):
        # Main box
        draw_rect(pixels, x, 60, x+130, 160, stage_colors[i])
        # Inner white area
        draw_rect(pixels, x+10, 75, x+120, 145, (255, 255, 255))
        # Arrow to next
        if i < 4:
            draw_arrow_right(pixels, x+132, x+178, 110, (100, 100, 100))
    
    # AI components below (connected to each stage)
    ai_color = (44, 62, 80)
    for i, x in enumerate(stage_x):
        draw_arrow_down(pixels, x+65, 162, 190, (150, 150, 150))
        draw_rect(pixels, x, 195, x+130, 270, ai_color)
        draw_rect(pixels, x+8, 208, x+122, 258, (200, 220, 240))
    
    # Feedback loop (bottom)
    draw_rect(pixels, 30, 300, 760, 310, (192, 57, 43))
    draw_rect(pixels, 375, 310, 425, 340, (192, 57, 43))
    
    # Analytics Dashboard area
    draw_rect(pixels, 100, 360, 700, 480, (236, 240, 241))
    # Dashboard elements
    draw_rect(pixels, 120, 375, 280, 460, (52, 152, 219))
    draw_rect(pixels, 300, 375, 460, 460, (46, 204, 113))
    draw_rect(pixels, 480, 375, 680, 460, (155, 89, 182))
    
    return create_png(w, h, pixels)


def generate_figure3():
    """Figure 3: Real-Time Regulatory Compliance Monitoring Framework."""
    w, h = 800, 600
    pixels = create_blank(w, h, (248, 249, 250))
    
    # Title
    draw_rect(pixels, 180, 10, 620, 40, (33, 37, 41))
    
    # Top: Regulatory Sources
    sources_color = (41, 128, 185)
    for i, x in enumerate([80, 250, 420, 590]):
        draw_rect(pixels, x, 55, x+140, 105, sources_color)
        draw_rect(pixels, x+10, 65, x+130, 95, (220, 235, 250))
    
    # Central Processing Hub (circular representation - large square with rounded feel)
    hub_color = (142, 68, 173)
    draw_rect(pixels, 250, 130, 550, 300, hub_color)
    draw_rect(pixels, 270, 150, 530, 280, (240, 230, 250))
    
    # Internal modules
    draw_rect(pixels, 280, 160, 390, 200, (155, 89, 182))
    draw_rect(pixels, 410, 160, 520, 200, (155, 89, 182))
    draw_rect(pixels, 280, 220, 390, 260, (155, 89, 182))
    draw_rect(pixels, 410, 220, 520, 260, (155, 89, 182))
    
    # Arrows from sources to hub
    for x in [150, 320, 490, 660]:
        draw_arrow_down(pixels, x, 107, 128, (100, 100, 100))
    
    # Arrow down from hub
    draw_arrow_down(pixels, 400, 302, 330, (100, 100, 100))
    
    # Risk Assessment Layer
    draw_rect(pixels, 100, 335, 700, 410, (230, 126, 34))
    draw_rect(pixels, 120, 350, 300, 395, (255, 235, 200))
    draw_rect(pixels, 320, 350, 500, 395, (255, 235, 200))
    draw_rect(pixels, 520, 350, 680, 395, (255, 235, 200))
    
    # Arrow down
    draw_arrow_down(pixels, 400, 412, 440, (100, 100, 100))
    
    # Alert & Response System
    draw_rect(pixels, 150, 445, 650, 580, (231, 76, 60))
    draw_rect(pixels, 170, 460, 350, 520, (255, 220, 220))
    draw_rect(pixels, 370, 460, 550, 520, (255, 220, 220))
    draw_rect(pixels, 170, 530, 350, 565, (255, 220, 220))
    draw_rect(pixels, 370, 530, 550, 565, (255, 220, 220))
    
    return create_png(w, h, pixels)


def generate_figure4():
    """Figure 4: Human-AI Collaboration Governance Framework for Legal Analytics."""
    w, h = 800, 600
    pixels = create_blank(w, h, (248, 249, 250))
    
    # Title
    draw_rect(pixels, 150, 10, 650, 40, (33, 37, 41))
    
    # Left side: Human Domain
    draw_rect(pixels, 30, 55, 370, 580, (220, 235, 250))
    # Human roles
    human_color = (52, 152, 219)
    for i, y in enumerate([75, 160, 245, 330, 415, 500]):
        draw_rect(pixels, 50, y, 350, y+65, human_color)
        draw_rect(pixels, 60, y+10, 340, y+55, (255, 255, 255))
    
    # Right side: AI Domain
    draw_rect(pixels, 430, 55, 770, 580, (230, 250, 230))
    # AI capabilities
    ai_color = (46, 204, 113)
    for i, y in enumerate([75, 160, 245, 330, 415, 500]):
        draw_rect(pixels, 450, y, 750, y+65, ai_color)
        draw_rect(pixels, 460, y+10, 740, y+55, (255, 255, 255))
    
    # Center: Governance Bridge (connecting arrows)
    bridge_color = (155, 89, 182)
    for y in [100, 185, 270, 355, 440, 525]:
        draw_rect(pixels, 372, y, 428, y+15, bridge_color)
        # Arrow indicators
        draw_rect(pixels, 380, y+3, 420, y+12, (200, 180, 220))
    
    return create_png(w, h, pixels)

# Main execution
if __name__ == "__main__":
    output_dir = "/projects/sandbox/AMMAN/contract_analytics_figures"
    os.makedirs(output_dir, exist_ok=True)
    
    figures = [
        ("Figure_1_Architecture_AI_Contract_Platform.png", generate_figure1),
        ("Figure_2_Contract_Lifecycle_Management.png", generate_figure2),
        ("Figure_3_Regulatory_Compliance_Monitoring.png", generate_figure3),
        ("Figure_4_Human_AI_Governance_Framework.png", generate_figure4),
    ]
    
    for filename, generator in figures:
        filepath = os.path.join(output_dir, filename)
        png_data = generator()
        with open(filepath, 'wb') as f:
            f.write(png_data)
        print(f"Created: {filepath} ({len(png_data)} bytes)")
    
    print("\nAll 4 figures generated successfully!")
