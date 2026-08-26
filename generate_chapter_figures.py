"""
Generate 4 professional figures for the book chapter.
Optimized for speed with smaller dimensions and efficient drawing.
"""

import struct
import zlib
import math
import os

def create_png(width, height, pixels, filename):
    """Create PNG from flat pixel array. pixels[y][x] = (R,G,B)"""
    def make_chunk(chunk_type, data):
        chunk = chunk_type + data
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', zlib.crc32(chunk) & 0xffffffff)
    
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # filter byte
        for x in range(width):
            r, g, b = pixels[y][x]
            raw.append(min(255, max(0, r)))
            raw.append(min(255, max(0, g)))
            raw.append(min(255, max(0, b)))
    
    signature = b'\x89PNG\r\n\x1a\n'
    ihdr = make_chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    idat = make_chunk(b'IDAT', zlib.compress(bytes(raw), 6))
    iend = make_chunk(b'IEND', b'')
    
    with open(filename, 'wb') as f:
        f.write(signature + ihdr + idat + iend)

def fill_rect(pixels, x1, y1, x2, y2, color, W, H):
    for y in range(max(0, y1), min(H, y2)):
        for x in range(max(0, x1), min(W, x2)):
            pixels[y][x] = color

def draw_hline(pixels, x1, x2, y, color, W, H, th=1):
    for dy in range(th):
        yy = y + dy
        if 0 <= yy < H:
            for x in range(max(0, x1), min(W, x2)):
                pixels[yy][x] = color

def draw_vline(pixels, x, y1, y2, color, W, H, th=1):
    for dx in range(th):
        xx = x + dx
        if 0 <= xx < W:
            for y in range(max(0, y1), min(H, y2)):
                pixels[y][xx] = color

def fill_circle(pixels, cx, cy, r, color, W, H):
    r2 = r * r
    for y in range(max(0, cy - r), min(H, cy + r + 1)):
        dy = y - cy
        dx_max = int(math.sqrt(max(0, r2 - dy*dy)))
        for x in range(max(0, cx - dx_max), min(W, cx + dx_max + 1)):
            pixels[y][x] = color

def draw_line_fast(pixels, x1, y1, x2, y2, color, W, H, th=2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    steps = max(dx, dy, 1)
    for i in range(0, steps + 1, 1):
        t = i / steps
        x = int(x1 + t * (x2 - x1))
        y = int(y1 + t * (y2 - y1))
        for d in range(th):
            if 0 <= y+d < H and 0 <= x < W:
                pixels[y+d][x] = color
            if 0 <= y < H and 0 <= x+d < W:
                pixels[y][x+d] = color

# Colors
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
BLUE1 = (25, 55, 109)
BLUE2 = (41, 98, 168)
BLUE3 = (100, 149, 237)
BLUE4 = (200, 220, 245)
GREEN1 = (34, 112, 67)
GREEN2 = (76, 175, 80)
GREEN3 = (165, 214, 167)
ORANGE1 = (230, 126, 34)
ORANGE2 = (255, 183, 77)
PURPLE1 = (106, 27, 154)
PURPLE2 = (186, 130, 214)
TEAL = (0, 128, 128)
TEAL2 = (128, 203, 196)
RED1 = (211, 47, 47)
GRAY = (158, 158, 158)
LGRAY = (224, 224, 224)
VLIGHT = (245, 245, 245)


def gen_fig1():
    """Digital Transformation Framework - concentric layout"""
    W, H = 500, 400
    pixels = [[WHITE for _ in range(W)] for _ in range(H)]
    
    # Header bar
    fill_rect(pixels, 0, 0, W, 35, BLUE1, W, H)
    
    # Center circle
    fill_circle(pixels, 250, 210, 40, BLUE1, W, H)
    fill_circle(pixels, 250, 210, 35, BLUE2, W, H)
    
    # 6 outer nodes
    nodes = [
        (130, 110, BLUE3), (370, 110, GREEN2),
        (80, 270, PURPLE2), (420, 270, ORANGE1),
        (150, 360, TEAL), (350, 360, RED1),
    ]
    for nx, ny, color in nodes:
        # Connection line
        draw_line_fast(pixels, nx, ny, 250, 210, LGRAY, W, H, 1)
        fill_circle(pixels, nx, ny, 28, color, W, H)
    
    # Bottom boxes
    boxes = [(50, 375, 170, 395, BLUE1), (190, 375, 310, 395, GREEN1), (330, 375, 450, 395, ORANGE1)]
    for x1, y1, x2, y2, c in boxes:
        fill_rect(pixels, x1, y1, x2, y2, c, W, H)
    
    create_png(W, H, pixels, '/projects/sandbox/AMMAN/chapter_figures/Figure_1_Digital_Transformation_Framework.png')
    print("Figure 1 done")


def gen_fig2():
    """Technology Adoption S-Curve"""
    W, H = 500, 380
    pixels = [[WHITE for _ in range(W)] for _ in range(H)]
    
    # Header
    fill_rect(pixels, 0, 0, W, 35, BLUE1, W, H)
    
    # Chart area
    cx1, cy1, cx2, cy2 = 60, 50, 470, 320
    
    # Grid
    for i in range(5):
        y = cy1 + i * (cy2 - cy1) // 4
        draw_hline(pixels, cx1, cx2, y, LGRAY, W, H)
    
    # Axes
    draw_hline(pixels, cx1, cx2, cy2, BLACK, W, H, 2)
    draw_vline(pixels, cx1, cy1, cy2, BLACK, W, H, 2)
    
    # S-curve
    prev_x, prev_y = cx1, cy2 - 10
    for i in range(1, 410):
        x = cx1 + i
        t = (i / 410.0) * 10 - 5
        sig = 1.0 / (1.0 + math.exp(-t))
        y = int(cy2 - 10 - sig * (cy2 - cy1 - 30))
        draw_line_fast(pixels, prev_x, prev_y, x, y, BLUE1, W, H, 2)
        prev_x, prev_y = x, y
    
    # Bell curve (competitive advantage)
    prev_x2, prev_y2 = cx1, cy2 - 10
    for i in range(1, 410):
        x = cx1 + i
        t = i / 410.0
        bell = math.exp(-((t - 0.42)**2) / 0.04) * 0.75
        y = int(cy2 - 10 - bell * (cy2 - cy1 - 30))
        draw_line_fast(pixels, prev_x2, prev_y2, x, y, GREEN1, W, H, 2)
        prev_x2, prev_y2 = x, y
    
    # Phase markers
    for px in [cx1 + 80, cx1 + 170, cx1 + 260, cx1 + 340]:
        draw_vline(pixels, px, cy1 + 10, cy2, LGRAY, W, H, 1)
        fill_circle(pixels, px, cy2 + 12, 4, BLUE2, W, H)
    
    # Legend
    fill_rect(pixels, 330, 55, 465, 100, VLIGHT, W, H)
    draw_hline(pixels, 340, 370, 68, BLUE1, W, H, 3)
    draw_hline(pixels, 340, 370, 88, GREEN1, W, H, 2)
    
    # X-axis label area
    fill_rect(pixels, 200, 340, 330, 360, VLIGHT, W, H)
    
    create_png(W, H, pixels, '/projects/sandbox/AMMAN/chapter_figures/Figure_2_Technology_Adoption_Maturity.png')
    print("Figure 2 done")


def gen_fig3():
    """AI & Emerging Technologies Ecosystem - 3 layer stack"""
    W, H = 500, 420
    pixels = [[WHITE for _ in range(W)] for _ in range(H)]
    
    # Header
    fill_rect(pixels, 0, 0, W, 35, BLUE1, W, H)
    
    # Layer 3 (top): Strategic Outcomes
    fill_rect(pixels, 30, 50, 470, 150, (255, 248, 235), W, H)
    # Outline
    draw_hline(pixels, 30, 470, 50, ORANGE1, W, H, 2)
    draw_hline(pixels, 30, 470, 150, ORANGE1, W, H, 2)
    draw_vline(pixels, 30, 50, 150, ORANGE1, W, H, 2)
    draw_vline(pixels, 470, 50, 150, ORANGE1, W, H, 2)
    # Sub-boxes
    fill_rect(pixels, 50, 70, 170, 135, ORANGE2, W, H)
    fill_rect(pixels, 190, 70, 310, 135, GREEN3, W, H)
    fill_rect(pixels, 330, 70, 450, 135, TEAL2, W, H)
    
    # Layer 2 (middle): Business Capabilities
    fill_rect(pixels, 30, 170, 470, 275, BLUE4, W, H)
    draw_hline(pixels, 30, 470, 170, BLUE2, W, H, 2)
    draw_hline(pixels, 30, 470, 275, BLUE2, W, H, 2)
    draw_vline(pixels, 30, 170, 275, BLUE2, W, H, 2)
    draw_vline(pixels, 470, 170, 275, BLUE2, W, H, 2)
    # Sub-boxes
    fill_rect(pixels, 50, 190, 145, 258, BLUE2, W, H)
    fill_rect(pixels, 160, 190, 255, 258, GREEN2, W, H)
    fill_rect(pixels, 270, 190, 365, 258, ORANGE1, W, H)
    fill_rect(pixels, 380, 190, 450, 258, TEAL, W, H)
    
    # Layer 1 (bottom): Technology Foundation
    fill_rect(pixels, 30, 295, 470, 395, (235, 245, 255), W, H)
    draw_hline(pixels, 30, 470, 295, BLUE1, W, H, 2)
    draw_hline(pixels, 30, 470, 395, BLUE1, W, H, 2)
    draw_vline(pixels, 30, 295, 395, BLUE1, W, H, 2)
    draw_vline(pixels, 470, 295, 395, BLUE1, W, H, 2)
    # Sub-boxes
    fill_rect(pixels, 45, 315, 120, 378, BLUE3, W, H)
    fill_rect(pixels, 130, 315, 205, 378, GREEN2, W, H)
    fill_rect(pixels, 215, 315, 290, 378, PURPLE2, W, H)
    fill_rect(pixels, 300, 315, 375, 378, ORANGE2, W, H)
    fill_rect(pixels, 385, 315, 460, 378, TEAL2, W, H)
    
    # Arrows between layers
    for ax in [110, 230, 350]:
        draw_vline(pixels, ax, 152, 168, BLUE1, W, H, 2)
        draw_vline(pixels, ax, 277, 293, BLUE1, W, H, 2)
    
    # Side labels
    fill_rect(pixels, 475, 80, 495, 130, ORANGE1, W, H)
    fill_rect(pixels, 475, 200, 495, 250, BLUE2, W, H)
    fill_rect(pixels, 475, 330, 495, 375, BLUE1, W, H)
    
    create_png(W, H, pixels, '/projects/sandbox/AMMAN/chapter_figures/Figure_3_Emerging_Tech_Ecosystem.png')
    print("Figure 3 done")


def gen_fig4():
    """Strategic Roadmap - Timeline with phases"""
    W, H = 500, 380
    pixels = [[WHITE for _ in range(W)] for _ in range(H)]
    
    # Header
    fill_rect(pixels, 0, 0, W, 35, BLUE1, W, H)
    
    # Timeline bar
    fill_rect(pixels, 50, 185, 450, 200, BLUE3, W, H)
    # Arrow end
    for d in range(15):
        fill_rect(pixels, 450 + d, 192 - d, 451 + d, 193 + d, GREEN1, W, H)
    
    # Phase markers
    phases_x = [120, 220, 320, 420]
    phase_colors = [BLUE1, BLUE2, GREEN1, ORANGE1]
    
    for i, (px, color) in enumerate(zip(phases_x, phase_colors)):
        # Marker circle
        fill_circle(pixels, px, 192, 8, color, W, H)
        fill_circle(pixels, px, 192, 5, WHITE, W, H)
        fill_circle(pixels, px, 192, 3, color, W, H)
        
        # Upper box
        bx1 = px - 40
        bx2 = px + 40
        fill_rect(pixels, bx1, 55, bx2, 170, VLIGHT, W, H)
        # Top accent
        fill_rect(pixels, bx1, 55, bx2, 65, color, W, H)
        # Border
        draw_hline(pixels, bx1, bx2, 55, color, W, H, 1)
        draw_hline(pixels, bx1, bx2, 170, color, W, H, 1)
        draw_vline(pixels, bx1, 55, 170, color, W, H, 1)
        draw_vline(pixels, bx2, 55, 170, color, W, H, 1)
        # Bullet dots
        for j in range(4):
            fill_circle(pixels, bx1 + 12, 80 + j * 22, 3, color, W, H)
        
        # Lower box
        fill_rect(pixels, bx1, 215, bx2, 330, VLIGHT, W, H)
        fill_rect(pixels, bx1, 215, bx2, 222, color, W, H)
        draw_hline(pixels, bx1, bx2, 215, color, W, H, 1)
        draw_hline(pixels, bx1, bx2, 330, color, W, H, 1)
        draw_vline(pixels, bx1, 215, 330, color, W, H, 1)
        draw_vline(pixels, bx2, 215, 330, color, W, H, 1)
        # Bullet dots
        for j in range(3):
            fill_circle(pixels, bx1 + 12, 238 + j * 28, 3, color, W, H)
        
        # Connect to timeline
        draw_vline(pixels, px, 170, 185, color, W, H, 1)
        draw_vline(pixels, px, 200, 215, color, W, H, 1)
    
    # Bottom summary bar
    fill_rect(pixels, 50, 350, 450, 370, LGRAY, W, H)
    for i, color in enumerate(phase_colors):
        fill_rect(pixels, 60 + i*100, 354, 145 + i*100, 366, color, W, H)
    
    create_png(W, H, pixels, '/projects/sandbox/AMMAN/chapter_figures/Figure_4_Strategic_Roadmap.png')
    print("Figure 4 done")


if __name__ == "__main__":
    os.makedirs('/projects/sandbox/AMMAN/chapter_figures', exist_ok=True)
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print("\nAll figures generated!")
    for f in sorted(os.listdir('/projects/sandbox/AMMAN/chapter_figures')):
        path = f'/projects/sandbox/AMMAN/chapter_figures/{f}'
        print(f"  {f} - {os.path.getsize(path):,} bytes")
