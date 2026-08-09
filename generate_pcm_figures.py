#!/usr/bin/env python3
"""
Generate 6 figures for the PCM chapter using pure Python with struct/zlib for PNG creation.
No external dependencies needed.
"""
import struct
import zlib
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pcm_figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_png(width, height, pixels):
    """Create a PNG file from raw pixel data (list of rows, each row is list of (R,G,B) tuples)."""
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



def fill_rect(pixels, x1, y1, x2, y2, color):
    """Fill a rectangle in the pixel buffer."""
    for y in range(max(0, y1), min(len(pixels), y2)):
        for x in range(max(0, x1), min(len(pixels[0]), x2)):
            pixels[y][x] = color


def draw_hline(pixels, x1, x2, y, color, thickness=1):
    for t in range(thickness):
        if 0 <= y+t < len(pixels):
            for x in range(max(0, x1), min(len(pixels[0]), x2)):
                pixels[y+t][x] = color


def draw_vline(pixels, x, y1, y2, color, thickness=1):
    for t in range(thickness):
        if 0 <= x+t < len(pixels[0]):
            for y in range(max(0, y1), min(len(pixels), y2)):
                pixels[y][x+t] = color


def draw_text_block(pixels, x, y, text, color, scale=1):
    """Draw a simple text representation as a colored block with label indicator."""
    # Simple block representation for labels
    bw = len(text) * 6 * scale
    bh = 10 * scale
    for dy in range(bh):
        for dx in range(bw):
            if 0 <= y+dy < len(pixels) and 0 <= x+dx < len(pixels[0]):
                pixels[y+dy][x+dx] = color



def create_figure1_classification():
    """Figure 1: Classification of Phase Change Materials (PCMs) - Hierarchy diagram."""
    w, h = 800, 500
    pixels = [[(255, 255, 255) for _ in range(w)] for _ in range(h)]
    
    # Title bar
    fill_rect(pixels, 0, 0, w, 40, (25, 60, 120))
    
    # Main PCM box at top
    fill_rect(pixels, 300, 55, 500, 95, (41, 128, 185))
    
    # Three main category boxes
    # Organic
    fill_rect(pixels, 50, 140, 250, 180, (39, 174, 96))
    # Inorganic
    fill_rect(pixels, 310, 140, 510, 180, (231, 76, 60))
    # Eutectic
    fill_rect(pixels, 570, 140, 750, 180, (142, 68, 173))
    
    # Connecting lines from top
    draw_vline(pixels, 400, 95, 140, (80, 80, 80), 2)
    draw_hline(pixels, 150, 660, 120, (80, 80, 80), 2)
    draw_vline(pixels, 150, 120, 140, (80, 80, 80), 2)
    draw_vline(pixels, 410, 120, 140, (80, 80, 80), 2)
    draw_vline(pixels, 660, 120, 140, (80, 80, 80), 2)
    
    # Sub-categories for Organic
    fill_rect(pixels, 20, 220, 140, 255, (46, 204, 113))
    fill_rect(pixels, 155, 220, 275, 255, (46, 204, 113))
    draw_vline(pixels, 80, 180, 220, (80, 80, 80), 1)
    draw_vline(pixels, 215, 180, 220, (80, 80, 80), 1)
    draw_hline(pixels, 80, 215, 200, (80, 80, 80), 1)
    draw_vline(pixels, 150, 180, 200, (80, 80, 80), 1)
    
    # Sub-sub for Organic
    fill_rect(pixels, 10, 280, 90, 310, (171, 235, 198))
    fill_rect(pixels, 100, 280, 180, 310, (171, 235, 198))
    fill_rect(pixels, 190, 280, 270, 310, (171, 235, 198))
    
    # Sub-categories for Inorganic
    fill_rect(pixels, 290, 220, 410, 255, (236, 112, 99))
    fill_rect(pixels, 420, 220, 540, 255, (236, 112, 99))
    draw_vline(pixels, 350, 180, 220, (80, 80, 80), 1)
    draw_vline(pixels, 480, 180, 220, (80, 80, 80), 1)
    draw_hline(pixels, 350, 480, 200, (80, 80, 80), 1)
    draw_vline(pixels, 410, 180, 200, (80, 80, 80), 1)
    
    # Sub-categories for Eutectic
    fill_rect(pixels, 560, 220, 680, 255, (165, 105, 189))
    fill_rect(pixels, 690, 220, 780, 255, (165, 105, 189))
    draw_vline(pixels, 620, 180, 220, (80, 80, 80), 1)
    draw_vline(pixels, 735, 180, 220, (80, 80, 80), 1)
    draw_hline(pixels, 620, 735, 200, (80, 80, 80), 1)
    draw_vline(pixels, 660, 180, 200, (80, 80, 80), 1)
    
    # Legend area
    fill_rect(pixels, 50, 380, 750, 480, (245, 245, 245))
    # Legend items
    fill_rect(pixels, 70, 395, 100, 415, (41, 128, 185))
    fill_rect(pixels, 70, 425, 100, 445, (39, 174, 96))
    fill_rect(pixels, 300, 395, 330, 415, (231, 76, 60))
    fill_rect(pixels, 300, 425, 330, 445, (142, 68, 173))
    fill_rect(pixels, 550, 395, 580, 415, (171, 235, 198))
    fill_rect(pixels, 550, 425, 580, 445, (165, 105, 189))
    
    png_data = create_png(w, h, pixels)
    path = os.path.join(OUTPUT_DIR, "Figure_1_PCM_Classification.png")
    with open(path, 'wb') as f:
        f.write(png_data)
    print(f"Created: {path}")



def create_figure2_thermal_conductivity():
    """Figure 2: Thermal Conductivity Enhancement - Bar chart comparison."""
    w, h = 800, 500
    pixels = [[(255, 255, 255) for _ in range(w)] for _ in range(h)]
    
    # Title bar
    fill_rect(pixels, 0, 0, w, 40, (25, 60, 120))
    
    # Axes
    draw_hline(pixels, 80, 750, 420, (40, 40, 40), 2)
    draw_vline(pixels, 80, 50, 420, (40, 40, 40), 2)
    
    # Y-axis grid lines
    for i in range(5):
        y = 420 - i * 80
        draw_hline(pixels, 80, 750, y, (220, 220, 220), 1)
    
    # Bars representing thermal conductivity values
    # Pure Paraffin: 0.2 -> very short bar
    # Nanoparticles: 0.4 -> short
    # CNT: 0.8 -> medium-short
    # Graphene: 1.5 -> medium
    # EG: 25 -> tall
    # Metal Foam: 15 -> tall
    # Fins: 10 -> medium-tall
    # Hybrid: 35 -> tallest
    
    bar_data = [
        (0.2, (189, 195, 199)),   # Pure Paraffin
        (0.5, (52, 152, 219)),    # Nanoparticles
        (1.0, (46, 204, 113)),    # CNT
        (2.0, (155, 89, 182)),    # Graphene
        (25, (230, 126, 34)),     # Expanded Graphite
        (15, (231, 76, 60)),      # Metal Foam
        (10, (241, 196, 15)),     # Fins
        (35, (26, 188, 156)),     # Hybrid
    ]
    
    max_val = 40
    bar_width = 70
    gap = 12
    start_x = 110
    
    for i, (val, color) in enumerate(bar_data):
        x = start_x + i * (bar_width + gap)
        bar_height = int((val / max_val) * 350)
        y_top = 420 - bar_height
        fill_rect(pixels, x, y_top, x + bar_width, 420, color)
        # Bar outline
        draw_hline(pixels, x, x + bar_width, y_top, (40, 40, 40), 1)
        draw_vline(pixels, x, y_top, 420, (40, 40, 40), 1)
        draw_vline(pixels, x + bar_width, y_top, 420, (40, 40, 40), 1)
    
    # Legend area
    fill_rect(pixels, 100, 440, 750, 490, (248, 248, 248))
    colors_legend = [(189,195,199),(52,152,219),(46,204,113),(155,89,182),
                     (230,126,34),(231,76,60),(241,196,15),(26,188,156)]
    for i, c in enumerate(colors_legend):
        fill_rect(pixels, 110 + i*80, 450, 130 + i*80, 470, c)
    
    png_data = create_png(w, h, pixels)
    path = os.path.join(OUTPUT_DIR, "Figure_2_Thermal_Conductivity_Enhancement.png")
    with open(path, 'wb') as f:
        f.write(png_data)
    print(f"Created: {path}")



def create_figure3_temperature_profile():
    """Figure 3: Temperature Profile During PCM Charging and Discharging."""
    w, h = 800, 500
    pixels = [[(255, 255, 255) for _ in range(w)] for _ in range(h)]
    
    # Title bar
    fill_rect(pixels, 0, 0, w, 40, (25, 60, 120))
    
    # Axes
    draw_hline(pixels, 80, 750, 420, (40, 40, 40), 2)
    draw_vline(pixels, 80, 50, 422, (40, 40, 40), 2)
    
    # Draw charging curve (S-shaped with plateau)
    # Phase 1: Sensible heating (solid) - steep rise
    # Phase 2: Latent heat (melting) - plateau
    # Phase 3: Sensible heating (liquid) - steep rise
    
    # Charging curve points
    charge_color = (231, 76, 60)  # Red
    discharge_color = (41, 128, 185)  # Blue
    
    # Melting temperature line (dashed)
    melt_y = 230
    for x in range(80, 750, 8):
        draw_hline(pixels, x, min(x+4, 750), melt_y, (150, 150, 150), 1)
    
    # Draw charging curve
    for x in range(100, 700):
        if x < 250:
            # Sensible heating solid phase (steep)
            y = 400 - int((x - 100) * 1.1)
            thickness = 3
        elif x < 470:
            # Melting plateau
            y = melt_y + int(3 * ((x - 360) / 220) ** 2) if x > 360 else melt_y - int(3 * ((360 - x) / 110) ** 2)
            y = melt_y
            thickness = 3
        else:
            # Sensible heating liquid phase
            y = melt_y - int((x - 470) * 0.6)
            thickness = 3
        
        for t in range(thickness):
            if 0 <= y+t < h and 0 <= x < w:
                pixels[y+t][x] = charge_color
    
    # Draw discharging curve (shifted right/down)
    for x in range(100, 700):
        if x < 230:
            # Sensible cooling liquid phase (steep decline)
            y = 80 + int((x - 100) * 1.15)
            thickness = 3
        elif x < 480:
            # Solidification plateau
            y = melt_y + 15
            thickness = 3
        else:
            # Sensible cooling solid phase
            y = melt_y + 15 + int((x - 480) * 0.8)
            thickness = 3
        
        for t in range(thickness):
            if 0 <= y+t < h and 0 <= x < w:
                pixels[y+t][x] = discharge_color
    
    # Phase region shading
    fill_rect(pixels, 81, 421, 250, 440, (255, 200, 200))  # Solid region
    fill_rect(pixels, 250, 421, 470, 440, (255, 255, 200))  # Melting region
    fill_rect(pixels, 470, 421, 700, 440, (200, 200, 255))  # Liquid region
    
    # Legend
    fill_rect(pixels, 550, 60, 740, 120, (248, 248, 248))
    fill_rect(pixels, 560, 70, 590, 85, charge_color)
    fill_rect(pixels, 560, 95, 590, 110, discharge_color)
    
    png_data = create_png(w, h, pixels)
    path = os.path.join(OUTPUT_DIR, "Figure_3_Temperature_Profile.png")
    with open(path, 'wb') as f:
        f.write(png_data)
    print(f"Created: {path}")



def create_figure4_encapsulation():
    """Figure 4: PCM Encapsulation Methods - Macro, Micro, and Shape-Stabilized."""
    w, h = 800, 500
    pixels = [[(255, 255, 255) for _ in range(w)] for _ in range(h)]
    
    # Title bar
    fill_rect(pixels, 0, 0, w, 40, (25, 60, 120))
    
    # Three panels for three encapsulation types
    # Panel 1: Macroencapsulation
    fill_rect(pixels, 30, 60, 260, 380, (240, 248, 255))
    draw_vline(pixels, 30, 60, 380, (41, 128, 185), 2)
    draw_vline(pixels, 260, 60, 380, (41, 128, 185), 2)
    draw_hline(pixels, 30, 260, 60, (41, 128, 185), 2)
    draw_hline(pixels, 30, 260, 380, (41, 128, 185), 2)
    
    # Draw macro container (cylinder-like)
    fill_rect(pixels, 80, 120, 210, 340, (189, 195, 199))
    fill_rect(pixels, 95, 135, 195, 325, (52, 152, 219))
    # Inner PCM
    fill_rect(pixels, 105, 150, 185, 310, (41, 128, 185))
    
    # Panel 2: Microencapsulation
    fill_rect(pixels, 285, 60, 515, 380, (255, 248, 240))
    draw_vline(pixels, 285, 60, 380, (230, 126, 34), 2)
    draw_vline(pixels, 515, 60, 380, (230, 126, 34), 2)
    draw_hline(pixels, 285, 515, 60, (230, 126, 34), 2)
    draw_hline(pixels, 285, 515, 380, (230, 126, 34), 2)
    
    # Draw microcapsules (circles approximated with filled squares)
    capsule_positions = [(340, 140), (420, 150), (370, 220), (440, 240),
                         (330, 290), (400, 310), (460, 170), (350, 340)]
    for cx, cy in capsule_positions:
        # Shell
        for dy in range(-18, 19):
            for dx in range(-18, 19):
                if dx*dx + dy*dy <= 18*18:
                    if 0 <= cy+dy < h and 0 <= cx+dx < w:
                        pixels[cy+dy][cx+dx] = (230, 126, 34)
        # Core PCM
        for dy in range(-13, 14):
            for dx in range(-13, 14):
                if dx*dx + dy*dy <= 13*13:
                    if 0 <= cy+dy < h and 0 <= cx+dx < w:
                        pixels[cy+dy][cx+dx] = (241, 196, 15)
    
    # Panel 3: Shape-Stabilized
    fill_rect(pixels, 540, 60, 770, 380, (240, 255, 240))
    draw_vline(pixels, 540, 60, 380, (39, 174, 96), 2)
    draw_vline(pixels, 770, 60, 380, (39, 174, 96), 2)
    draw_hline(pixels, 540, 770, 60, (39, 174, 96), 2)
    draw_hline(pixels, 540, 770, 380, (39, 174, 96), 2)
    
    # Draw porous matrix with PCM
    for y in range(100, 350, 20):
        for x in range(570, 740, 20):
            # Matrix grid
            fill_rect(pixels, x, y, x+8, y+18, (120, 120, 120))
            # PCM in pores
            fill_rect(pixels, x+8, y, x+18, y+18, (46, 204, 113))
    
    # Labels at bottom
    fill_rect(pixels, 30, 400, 260, 430, (41, 128, 185))
    fill_rect(pixels, 285, 400, 515, 430, (230, 126, 34))
    fill_rect(pixels, 540, 400, 770, 430, (39, 174, 96))
    
    # Bottom comparison indicators
    fill_rect(pixels, 30, 450, 260, 480, (200, 220, 240))
    fill_rect(pixels, 285, 450, 515, 480, (255, 230, 200))
    fill_rect(pixels, 540, 450, 770, 480, (200, 240, 200))
    
    png_data = create_png(w, h, pixels)
    path = os.path.join(OUTPUT_DIR, "Figure_4_Encapsulation_Methods.png")
    with open(path, 'wb') as f:
        f.write(png_data)
    print(f"Created: {path}")



def create_figure5_applications():
    """Figure 5: Applications of PCMs in Sustainable Development and Clean Energy."""
    w, h = 800, 550
    pixels = [[(255, 255, 255) for _ in range(w)] for _ in range(h)]
    
    # Title bar
    fill_rect(pixels, 0, 0, w, 40, (25, 60, 120))
    
    # Central hub - PCM Technology
    cx, cy = 400, 275
    for dy in range(-50, 51):
        for dx in range(-50, 51):
            if dx*dx + dy*dy <= 50*50:
                pixels[cy+dy][cx+dx] = (41, 128, 185)
            elif dx*dx + dy*dy <= 55*55:
                pixels[cy+dy][cx+dx] = (25, 60, 120)
    
    # Application boxes around the hub
    apps = [
        (120, 100, 260, 150, (39, 174, 96)),    # Buildings
        (540, 100, 700, 150, (230, 126, 34)),    # Solar Thermal
        (80, 270, 220, 320, (155, 89, 182)),     # Electronics
        (580, 270, 720, 320, (231, 76, 60)),     # Battery TM
        (120, 420, 280, 470, (52, 152, 219)),    # Cold Chain
        (520, 420, 680, 470, (26, 188, 156)),    # Smart Textiles
        (320, 480, 480, 530, (241, 196, 15)),    # Industrial
    ]
    
    for x1, y1, x2, y2, color in apps:
        fill_rect(pixels, x1, y1, x2, y2, color)
        # Draw connecting line to center
        mx = (x1 + x2) // 2
        my = (y1 + y2) // 2
        # Simple line from app center toward hub center
        steps = 30
        for s in range(steps):
            lx = mx + (cx - mx) * s // steps
            ly = my + (cy - my) * s // steps
            dist_sq = (lx - cx)**2 + (ly - cy)**2
            if dist_sq > 55*55:
                for t in range(2):
                    if 0 <= ly+t < h and 0 <= lx+t < w:
                        pixels[ly+t][lx+t] = (100, 100, 100)
    
    # SDG indicators at bottom
    sdg_colors = [(231, 76, 60), (241, 196, 15), (46, 204, 113), (52, 152, 219)]
    for i, c in enumerate(sdg_colors):
        fill_rect(pixels, 200 + i * 110, 540, 280 + i * 110, 548, c)
    
    png_data = create_png(w, h, pixels)
    path = os.path.join(OUTPUT_DIR, "Figure_5_PCM_Applications.png")
    with open(path, 'wb') as f:
        f.write(png_data)
    print(f"Created: {path}")



def create_figure6_tes_schematic():
    """Figure 6: Schematic of TES System - Operating Principle (Charging, Storing, Discharging)."""
    w, h = 800, 450
    pixels = [[(255, 255, 255) for _ in range(w)] for _ in range(h)]
    
    # Title bar
    fill_rect(pixels, 0, 0, w, 40, (25, 60, 120))
    
    # Three phase boxes
    # Phase 1: Charging
    fill_rect(pixels, 30, 70, 250, 350, (255, 235, 235))
    draw_vline(pixels, 30, 70, 350, (231, 76, 60), 3)
    draw_vline(pixels, 250, 70, 350, (231, 76, 60), 3)
    draw_hline(pixels, 30, 250, 70, (231, 76, 60), 3)
    draw_hline(pixels, 30, 250, 350, (231, 76, 60), 3)
    
    # Heat source arrow into storage
    fill_rect(pixels, 60, 130, 120, 150, (231, 76, 60))
    fill_rect(pixels, 120, 120, 140, 160, (231, 76, 60))
    # Storage tank
    fill_rect(pixels, 80, 180, 200, 300, (189, 195, 199))
    fill_rect(pixels, 90, 190, 190, 290, (241, 196, 15))
    # Temperature indicator (rising)
    for i in range(5):
        fill_rect(pixels, 210, 280 - i*20, 230, 290 - i*20, (231, 76, 60))
    
    # Phase 2: Storing
    fill_rect(pixels, 290, 70, 510, 350, (255, 255, 235))
    draw_vline(pixels, 290, 70, 350, (241, 196, 15), 3)
    draw_vline(pixels, 510, 70, 350, (241, 196, 15), 3)
    draw_hline(pixels, 290, 510, 70, (241, 196, 15), 3)
    draw_hline(pixels, 290, 510, 350, (241, 196, 15), 3)
    
    # Insulated storage tank
    fill_rect(pixels, 340, 150, 460, 300, (150, 150, 150))
    fill_rect(pixels, 350, 160, 450, 290, (241, 196, 15))
    # Insulation lines
    for y in range(150, 300, 15):
        draw_hline(pixels, 340, 350, y, (100, 100, 100), 1)
        draw_hline(pixels, 450, 460, y, (100, 100, 100), 1)
    
    # Phase 3: Discharging
    fill_rect(pixels, 550, 70, 770, 350, (235, 245, 255))
    draw_vline(pixels, 550, 70, 350, (41, 128, 185), 3)
    draw_vline(pixels, 770, 70, 350, (41, 128, 185), 3)
    draw_hline(pixels, 550, 770, 70, (41, 128, 185), 3)
    draw_hline(pixels, 550, 770, 350, (41, 128, 185), 3)
    
    # Storage releasing heat
    fill_rect(pixels, 600, 180, 720, 300, (189, 195, 199))
    fill_rect(pixels, 610, 190, 710, 290, (200, 220, 255))
    # Heat output arrow
    fill_rect(pixels, 660, 130, 720, 150, (41, 128, 185))
    fill_rect(pixels, 720, 120, 740, 160, (41, 128, 185))
    
    # Arrows between phases
    fill_rect(pixels, 255, 200, 285, 210, (100, 100, 100))
    fill_rect(pixels, 515, 200, 545, 210, (100, 100, 100))
    
    # Phase labels at bottom
    fill_rect(pixels, 80, 370, 200, 400, (231, 76, 60))
    fill_rect(pixels, 340, 370, 460, 400, (241, 196, 15))
    fill_rect(pixels, 600, 370, 720, 400, (41, 128, 185))
    
    # Timeline arrow
    draw_hline(pixels, 50, 750, 430, (80, 80, 80), 2)
    fill_rect(pixels, 740, 425, 755, 435, (80, 80, 80))
    
    png_data = create_png(w, h, pixels)
    path = os.path.join(OUTPUT_DIR, "Figure_6_TES_Schematic.png")
    with open(path, 'wb') as f:
        f.write(png_data)
    print(f"Created: {path}")



if __name__ == "__main__":
    print("Generating PCM chapter figures...")
    create_figure1_classification()
    create_figure2_thermal_conductivity()
    create_figure3_temperature_profile()
    create_figure4_encapsulation()
    create_figure5_applications()
    create_figure6_tes_schematic()
    print(f"\nAll figures saved to: {OUTPUT_DIR}")
