#!/usr/bin/env python3
"""
Generate 4 professional figures for Chapter 2:
AI-Driven Data Analytics in Cancer Precision Medicine

Creates PNG figures using pure Python (no external dependencies).
"""

import struct
import zlib
import math
import os

OUTPUT_DIR = "/projects/sandbox/AMMAN/chapter2_figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_png(width, height, pixels, filename):
    """Create a PNG file from RGB pixel data."""
    def write_chunk(chunk_type, data):
        chunk = chunk_type + data
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', zlib.crc32(chunk) & 0xffffffff)

    sig = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = write_chunk(b'IHDR', ihdr_data)

    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0)  # filter byte
        for x in range(width):
            idx = (y * width + x) * 3
            raw_data.extend(pixels[idx:idx+3])

    compressed = zlib.compress(bytes(raw_data), 9)
    idat = write_chunk(b'IDAT', compressed)
    iend = write_chunk(b'IEND', b'')

    with open(filename, 'wb') as f:
        f.write(sig + ihdr + idat + iend)


def blend_color(c1, c2, t):
    """Blend two colors."""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def draw_rect(pixels, width, height, x1, y1, x2, y2, color):
    """Draw a filled rectangle."""
    for y in range(max(0, y1), min(height, y2)):
        for x in range(max(0, x1), min(width, x2)):
            idx = (y * width + x) * 3
            pixels[idx] = color[0]
            pixels[idx+1] = color[1]
            pixels[idx+2] = color[2]


def draw_circle(pixels, width, height, cx, cy, r, color):
    """Draw a filled circle."""
    for y in range(max(0, cy - r), min(height, cy + r + 1)):
        for x in range(max(0, cx - r), min(width, cx + r + 1)):
            if (x - cx)**2 + (y - cy)**2 <= r**2:
                idx = (y * width + x) * 3
                pixels[idx] = color[0]
                pixels[idx+1] = color[1]
                pixels[idx+2] = color[2]


def draw_line(pixels, width, height, x1, y1, x2, y2, color, thickness=2):
    """Draw a line with given thickness."""
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy), 1)
    for i in range(steps + 1):
        t = i / steps
        x = int(x1 + dx * t)
        y = int(y1 + dy * t)
        for ty in range(-thickness//2, thickness//2 + 1):
            for tx in range(-thickness//2, thickness//2 + 1):
                nx, ny = x + tx, y + ty
                if 0 <= nx < width and 0 <= ny < height:
                    idx = (ny * width + nx) * 3
                    pixels[idx] = color[0]
                    pixels[idx+1] = color[1]
                    pixels[idx+2] = color[2]


def draw_gradient_rect(pixels, width, height, x1, y1, x2, y2, color1, color2, vertical=True):
    """Draw a gradient-filled rectangle."""
    for y in range(max(0, y1), min(height, y2)):
        for x in range(max(0, x1), min(width, x2)):
            if vertical:
                t = (y - y1) / max(1, (y2 - y1 - 1))
            else:
                t = (x - x1) / max(1, (x2 - x1 - 1))
            color = blend_color(color1, color2, t)
            idx = (y * width + x) * 3
            pixels[idx] = color[0]
            pixels[idx+1] = color[1]
            pixels[idx+2] = color[2]


def draw_rounded_rect(pixels, width, height, x1, y1, x2, y2, r, color):
    """Draw a rounded rectangle."""
    draw_rect(pixels, width, height, x1 + r, y1, x2 - r, y2, color)
    draw_rect(pixels, width, height, x1, y1 + r, x2, y2 - r, color)
    draw_circle(pixels, width, height, x1 + r, y1 + r, r, color)
    draw_circle(pixels, width, height, x2 - r, y1 + r, r, color)
    draw_circle(pixels, width, height, x1 + r, y2 - r, r, color)
    draw_circle(pixels, width, height, x2 - r, y2 - r, r, color)


def draw_arrow(pixels, width, height, x1, y1, x2, y2, color, thickness=2):
    """Draw an arrow from (x1,y1) to (x2,y2)."""
    draw_line(pixels, width, height, x1, y1, x2, y2, color, thickness)
    # Arrowhead
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 10
    a1 = angle + math.pi * 0.8
    a2 = angle - math.pi * 0.8
    ax1 = int(x2 + arrow_len * math.cos(a1))
    ay1 = int(y2 + arrow_len * math.sin(a1))
    ax2 = int(x2 + arrow_len * math.cos(a2))
    ay2 = int(y2 + arrow_len * math.sin(a2))
    draw_line(pixels, width, height, x2, y2, ax1, ay1, color, thickness)
    draw_line(pixels, width, height, x2, y2, ax2, ay2, color, thickness)


# ============================================================
# FIGURE 1: AI-Driven Cancer Precision Medicine Framework
# Shows multimodal data sources flowing into AI/ML pipeline
# ============================================================
def generate_figure1():
    W, H = 800, 600
    pixels = bytearray([255, 255, 255] * W * H)

    # Title area - light blue header
    draw_rect(pixels, W, H, 0, 0, W, 50, (41, 98, 255))

    # Data sources (left side) - colored boxes
    sources = [
        ((50, 80, 200, 140), (52, 152, 219), "Genomics"),
        ((50, 160, 200, 220), (46, 204, 113), "Imaging"),
        ((50, 240, 200, 300), (155, 89, 182), "EHR"),
        ((50, 320, 200, 380), (230, 126, 34), "Proteomics"),
        ((50, 400, 200, 460), (231, 76, 60), "Wearables"),
    ]

    for (x1, y1, x2, y2), color, _ in sources:
        draw_rounded_rect(pixels, W, H, x1, y1, x2, y2, 8, color)

    # Central AI Processing box
    draw_gradient_rect(pixels, W, H, 300, 120, 520, 420, (41, 98, 255), (108, 52, 235))
    # Inner lighter area
    draw_rect(pixels, W, H, 310, 130, 510, 410, (60, 120, 255))

    # Sub-modules inside
    modules = [
        (320, 150, 500, 190, (72, 145, 255)),
        (320, 210, 500, 250, (90, 160, 255)),
        (320, 270, 500, 310, (108, 175, 255)),
        (320, 330, 500, 370, (126, 190, 255)),
    ]
    for x1, y1, x2, y2, color in modules:
        draw_rounded_rect(pixels, W, H, x1, y1, x2, y2, 5, color)

    # Output (right side)
    outputs = [
        ((600, 120, 750, 180), (39, 174, 96)),
        ((600, 210, 750, 270), (41, 128, 185)),
        ((600, 300, 750, 360), (142, 68, 173)),
        ((600, 390, 750, 450), (211, 84, 0)),
    ]
    for (x1, y1, x2, y2), color, in outputs:
        draw_rounded_rect(pixels, W, H, x1, y1, x2, y2, 8, color)

    # Arrows from sources to center
    for (x1, y1, x2, y2), _, _ in sources:
        mid_y = (y1 + y2) // 2
        draw_arrow(pixels, W, H, x2 + 5, mid_y, 295, mid_y, (100, 100, 100), 2)

    # Arrows from center to outputs
    for (x1, y1, x2, y2), _ in outputs:
        mid_y = (y1 + y2) // 2
        draw_arrow(pixels, W, H, 525, mid_y, x1 - 5, mid_y, (100, 100, 100), 2)

    # Legend dots at bottom
    legend_colors = [(52, 152, 219), (46, 204, 113), (155, 89, 182), (230, 126, 34), (231, 76, 60)]
    for i, color in enumerate(legend_colors):
        draw_circle(pixels, W, H, 150 + i * 120, 550, 8, color)

    # Border
    draw_rect(pixels, W, H, 0, 0, W, 2, (200, 200, 200))
    draw_rect(pixels, W, H, 0, H-2, W, H, (200, 200, 200))
    draw_rect(pixels, W, H, 0, 0, 2, H, (200, 200, 200))
    draw_rect(pixels, W, H, W-2, 0, W, H, (200, 200, 200))

    filename = os.path.join(OUTPUT_DIR, "Figure_1_AI_Cancer_Framework.png")
    create_png(W, H, bytes(pixels), filename)
    print(f"Generated: {filename}")


# ============================================================
# FIGURE 2: Data Mining Techniques Taxonomy
# Hierarchical diagram showing classification/clustering/feature selection
# ============================================================
def generate_figure2():
    W, H = 800, 600
    pixels = bytearray([255, 255, 255] * W * H)

    # Top level node
    draw_rounded_rect(pixels, W, H, 280, 30, 520, 80, 10, (41, 98, 255))

    # Second level nodes
    level2 = [
        (60, 140, 260, 200, (52, 152, 219)),
        (300, 140, 500, 200, (46, 204, 113)),
        (540, 140, 740, 200, (155, 89, 182)),
    ]
    for x1, y1, x2, y2, color in level2:
        draw_rounded_rect(pixels, W, H, x1, y1, x2, y2, 8, color)

    # Arrows from top to level 2
    draw_line(pixels, W, H, 400, 80, 160, 140, (80, 80, 80), 2)
    draw_line(pixels, W, H, 400, 80, 400, 140, (80, 80, 80), 2)
    draw_line(pixels, W, H, 400, 80, 640, 140, (80, 80, 80), 2)

    # Third level - Classification subtypes
    class_nodes = [
        (30, 260, 150, 310, (93, 173, 226)),
        (170, 260, 290, 310, (93, 173, 226)),
    ]
    for x1, y1, x2, y2, color in class_nodes:
        draw_rounded_rect(pixels, W, H, x1, y1, x2, y2, 6, color)
        draw_line(pixels, W, H, (x1+x2)//2, 260, 160, 200, (80, 80, 80), 1)

    # Third level - Clustering subtypes
    clust_nodes = [
        (280, 260, 400, 310, (88, 214, 141)),
        (420, 260, 540, 310, (88, 214, 141)),
    ]
    for x1, y1, x2, y2, color in clust_nodes:
        draw_rounded_rect(pixels, W, H, x1, y1, x2, y2, 6, color)
        draw_line(pixels, W, H, (x1+x2)//2, 260, 400, 200, (80, 80, 80), 1)

    # Third level - Feature selection subtypes
    feat_nodes = [
        (540, 260, 660, 310, (187, 143, 206)),
        (680, 260, 790, 310, (187, 143, 206)),
    ]
    for x1, y1, x2, y2, color in feat_nodes:
        draw_rounded_rect(pixels, W, H, x1, y1, x2, y2, 6, color)
        draw_line(pixels, W, H, (x1+x2)//2, 260, 640, 200, (80, 80, 80), 1)

    # Fourth level - technique examples (small boxes)
    fourth_level = [
        # Under classification
        (20, 360, 130, 400, (174, 214, 241)),
        (140, 360, 250, 400, (174, 214, 241)),
        (20, 420, 130, 460, (174, 214, 241)),
        (140, 420, 250, 460, (174, 214, 241)),
        # Under clustering
        (270, 360, 380, 400, (171, 235, 198)),
        (390, 360, 500, 400, (171, 235, 198)),
        (270, 420, 380, 460, (171, 235, 198)),
        (390, 420, 500, 460, (171, 235, 198)),
        # Under feature selection
        (530, 360, 650, 400, (215, 189, 226)),
        (660, 360, 780, 400, (215, 189, 226)),
        (530, 420, 650, 460, (215, 189, 226)),
        (660, 420, 780, 460, (215, 189, 226)),
    ]
    for x1, y1, x2, y2, color in fourth_level:
        draw_rounded_rect(pixels, W, H, x1, y1, x2, y2, 4, color)

    # Connect level 3 to level 4
    for i in range(4):
        if i < 2:
            draw_line(pixels, W, H, fourth_level[i*2][0]+55, 360, 90, 310, (150, 150, 150), 1)
            draw_line(pixels, W, H, fourth_level[i*2+1][0]+55, 360, 230, 310, (150, 150, 150), 1)

    # Bottom performance comparison bars
    bar_y = 500
    bar_colors = [(52, 152, 219), (46, 204, 113), (155, 89, 182), (230, 126, 34), (231, 76, 60)]
    bar_widths = [580, 520, 490, 450, 400]
    for i, (color, bw) in enumerate(zip(bar_colors, bar_widths)):
        by = bar_y + i * 18
        draw_rect(pixels, W, H, 100, by, 100 + bw, by + 14, color)

    filename = os.path.join(OUTPUT_DIR, "Figure_2_Data_Mining_Taxonomy.png")
    create_png(W, H, bytes(pixels), filename)
    print(f"Generated: {filename}")


# ============================================================
# FIGURE 3: Data Preprocessing Pipeline
# Flowchart showing data cleaning -> transformation -> balancing -> model
# ============================================================
def generate_figure3():
    W, H = 800, 600
    pixels = bytearray([255, 255, 255] * W * H)

    # Background gradient effect
    for y in range(H):
        t = y / H * 0.05
        gray = int(255 - t * 255)
        for x in range(W):
            idx = (y * W + x) * 3
            pixels[idx] = gray
            pixels[idx+1] = gray
            pixels[idx+2] = gray

    # Pipeline stages (horizontal flow)
    stages = [
        (30, 80, 180, 200, (231, 76, 60), "Raw Data"),
        (220, 80, 370, 200, (230, 126, 34), "Cleaning"),
        (410, 80, 560, 200, (241, 196, 15), "Transform"),
        (600, 80, 750, 200, (46, 204, 113), "Balanced"),
    ]

    for x1, y1, x2, y2, color, _ in stages:
        draw_rounded_rect(pixels, W, H, x1, y1, x2, y2, 10, color)
        # Add inner highlight
        draw_rect(pixels, W, H, x1+5, y1+5, x2-5, y1+20, 
                  tuple(min(255, c+40) for c in color))

    # Arrows between stages
    arrow_y = 140
    draw_arrow(pixels, W, H, 185, arrow_y, 215, arrow_y, (60, 60, 60), 3)
    draw_arrow(pixels, W, H, 375, arrow_y, 405, arrow_y, (60, 60, 60), 3)
    draw_arrow(pixels, W, H, 565, arrow_y, 595, arrow_y, (60, 60, 60), 3)

    # Sub-processes below each stage
    sub_colors = [
        [(192, 57, 43), (192, 57, 43), (192, 57, 43)],
        [(211, 84, 0), (211, 84, 0), (211, 84, 0)],
        [(243, 156, 18), (243, 156, 18), (243, 156, 18)],
        [(39, 174, 96), (39, 174, 96), (39, 174, 96)],
    ]

    for stage_idx, (x1, y1, x2, y2, color, _) in enumerate(stages):
        center_x = (x1 + x2) // 2
        draw_line(pixels, W, H, center_x, y2, center_x, y2 + 30, (100, 100, 100), 2)
        
        for sub_idx in range(3):
            sx1 = x1 - 10
            sy1 = y2 + 40 + sub_idx * 55
            sx2 = x2 + 10
            sy2 = sy1 + 45
            sub_color = tuple(min(255, c + 60) for c in color)
            draw_rounded_rect(pixels, W, H, sx1, sy1, sx2, sy2, 5, sub_color)
            if sub_idx < 2:
                draw_line(pixels, W, H, center_x, sy2, center_x, sy2 + 10, (150, 150, 150), 1)

    # Bottom output arrow
    draw_arrow(pixels, W, H, 400, 550, 400, 580, (41, 98, 255), 3)
    draw_rounded_rect(pixels, W, H, 300, 560, 500, 590, 8, (41, 98, 255))

    filename = os.path.join(OUTPUT_DIR, "Figure_3_Preprocessing_Pipeline.png")
    create_png(W, H, bytes(pixels), filename)
    print(f"Generated: {filename}")


# ============================================================
# FIGURE 4: Emerging AI Architectures for Cancer Healthcare
# Shows multimodal fusion, federated learning, and future directions
# ============================================================
def generate_figure4():
    W, H = 800, 600
    pixels = bytearray([255, 255, 255] * W * H)

    # Three main sections
    # Section 1: Multimodal Fusion (left)
    draw_gradient_rect(pixels, W, H, 20, 40, 260, 350, (52, 152, 219), (41, 98, 255))
    # Inner boxes representing modalities
    modality_boxes = [
        (35, 70, 125, 120, (93, 173, 226)),
        (140, 70, 245, 120, (93, 173, 226)),
        (35, 135, 125, 185, (93, 173, 226)),
        (140, 135, 245, 185, (93, 173, 226)),
    ]
    for x1, y1, x2, y2, color in modality_boxes:
        draw_rounded_rect(pixels, W, H, x1, y1, x2, y2, 5, color)

    # Fusion indicator
    draw_rounded_rect(pixels, W, H, 60, 210, 230, 260, 8, (26, 82, 170))
    draw_rounded_rect(pixels, W, H, 60, 280, 230, 330, 8, (20, 60, 140))

    # Arrows connecting modalities to fusion
    draw_arrow(pixels, W, H, 80, 185, 100, 210, (255, 255, 255), 1)
    draw_arrow(pixels, W, H, 190, 185, 170, 210, (255, 255, 255), 1)

    # Section 2: Federated Learning (center)
    draw_gradient_rect(pixels, W, H, 280, 40, 520, 350, (46, 204, 113), (39, 174, 96))
    
    # Central server
    draw_circle(pixels, W, H, 400, 120, 30, (34, 153, 84))
    
    # Client nodes
    client_positions = [(330, 220), (400, 250), (470, 220), (350, 290), (450, 290)]
    for cx, cy in client_positions:
        draw_circle(pixels, W, H, cx, cy, 15, (88, 214, 141))
        draw_line(pixels, W, H, cx, cy - 15, 400, 150, (255, 255, 255), 1)

    # Privacy shield representation
    draw_rounded_rect(pixels, W, H, 310, 310, 490, 340, 6, (34, 153, 84))

    # Section 3: Future Directions (right)
    draw_gradient_rect(pixels, W, H, 540, 40, 780, 350, (155, 89, 182), (142, 68, 173))
    
    # Layers representing future tech
    future_layers = [
        (560, 70, 760, 120, (187, 143, 206)),
        (560, 140, 760, 190, (175, 122, 197)),
        (560, 210, 760, 260, (163, 101, 188)),
        (560, 280, 760, 330, (151, 80, 179)),
    ]
    for x1, y1, x2, y2, color in future_layers:
        draw_rounded_rect(pixels, W, H, x1, y1, x2, y2, 6, color)

    # Bottom integration bar
    draw_rounded_rect(pixels, W, H, 20, 380, 780, 440, 10, (44, 62, 80))
    
    # Integration sub-sections
    int_sections = [
        (40, 395, 200, 425, (52, 73, 94)),
        (220, 395, 390, 425, (52, 73, 94)),
        (410, 395, 580, 425, (52, 73, 94)),
        (600, 395, 760, 425, (52, 73, 94)),
    ]
    for x1, y1, x2, y2, color in int_sections:
        draw_rounded_rect(pixels, W, H, x1, y1, x2, y2, 4, color)

    # Bottom outcome boxes
    outcomes = [
        (50, 470, 230, 560, (39, 174, 96)),
        (260, 470, 440, 560, (41, 128, 185)),
        (470, 470, 650, 560, (142, 68, 173)),
    ]
    for x1, y1, x2, y2, color in outcomes:
        draw_rounded_rect(pixels, W, H, x1, y1, x2, y2, 8, color)
        # Inner detail
        draw_rect(pixels, W, H, x1+10, y1+10, x2-10, y1+30, 
                  tuple(min(255, c+40) for c in color))

    # Arrows from integration bar to outcomes
    for x1, y1, x2, y2, color in outcomes:
        cx = (x1 + x2) // 2
        draw_arrow(pixels, W, H, cx, 440, cx, 465, (100, 100, 100), 2)

    filename = os.path.join(OUTPUT_DIR, "Figure_4_Emerging_AI_Architectures.png")
    create_png(W, H, bytes(pixels), filename)
    print(f"Generated: {filename}")


if __name__ == "__main__":
    print("Generating figures for Chapter 2...")
    generate_figure1()
    generate_figure2()
    generate_figure3()
    generate_figure4()
    print(f"\nAll figures generated in: {OUTPUT_DIR}")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        fpath = os.path.join(OUTPUT_DIR, f)
        print(f"  {f} ({os.path.getsize(fpath):,} bytes)")
