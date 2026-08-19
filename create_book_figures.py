#!/usr/bin/env python3
"""
Generate 4 PNG figures for the Cultivating Tomorrow book.
Optimized pure Python implementation - no external dependencies.
"""
import struct
import zlib
import math
import os

def create_png(width, height, pixels, filename):
    """Create a PNG file from RGB pixel data (bytearray)."""
    def make_chunk(chunk_type, data):
        chunk = chunk_type + data
        crc = zlib.crc32(chunk) & 0xffffffff
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', crc)
    
    signature = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = make_chunk(b'IHDR', ihdr_data)
    
    # Build raw data with filter bytes
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0)  # filter byte
        offset = y * width * 3
        raw_data.extend(pixels[offset:offset + width * 3])
    
    compressed = zlib.compress(bytes(raw_data), 6)
    idat = make_chunk(b'IDAT', compressed)
    iend = make_chunk(b'IEND', b'')
    
    with open(filename, 'wb') as f:
        f.write(signature + ihdr + idat + iend)


class Canvas:
    def __init__(self, width, height, bg=(255, 255, 255)):
        self.width = width
        self.height = height
        self.pixels = bytearray(bg * (width * height))
    
    def set_pixel(self, x, y, r, g, b):
        if 0 <= x < self.width and 0 <= y < self.height:
            idx = (y * self.width + x) * 3
            self.pixels[idx] = r
            self.pixels[idx+1] = g
            self.pixels[idx+2] = b
    
    def fill_rect(self, x0, y0, x1, y1, r, g, b):
        x0, x1 = max(0, min(x0, x1)), min(self.width-1, max(x0, x1))
        y0, y1 = max(0, min(y0, y1)), min(self.height-1, max(y0, y1))
        row = bytes([r, g, b]) * (x1 - x0 + 1)
        for y in range(y0, y1 + 1):
            offset = (y * self.width + x0) * 3
            self.pixels[offset:offset + len(row)] = row
    
    def draw_line(self, x0, y0, x1, y1, r, g, b, thickness=1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        half = thickness // 2
        
        while True:
            for t in range(-half, half + 1):
                self.set_pixel(x0 + t, y0, r, g, b)
                self.set_pixel(x0, y0 + t, r, g, b)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
    
    def draw_rect(self, x0, y0, x1, y1, r, g, b, thickness=2):
        self.draw_line(x0, y0, x1, y0, r, g, b, thickness)
        self.draw_line(x1, y0, x1, y1, r, g, b, thickness)
        self.draw_line(x1, y1, x0, y1, r, g, b, thickness)
        self.draw_line(x0, y1, x0, y0, r, g, b, thickness)
    
    def fill_circle(self, cx, cy, radius, r, g, b):
        r2 = radius * radius
        for dy in range(-radius, radius + 1):
            y = cy + dy
            if 0 <= y < self.height:
                dx_max = int(math.sqrt(max(0, r2 - dy*dy)))
                x_start = max(0, cx - dx_max)
                x_end = min(self.width - 1, cx + dx_max)
                if x_start <= x_end:
                    row = bytes([r, g, b]) * (x_end - x_start + 1)
                    offset = (y * self.width + x_start) * 3
                    self.pixels[offset:offset + len(row)] = row
    
    def draw_circle(self, cx, cy, radius, r, g, b, thickness=2):
        for angle in range(0, 360):
            a = math.radians(angle)
            for t in range(thickness):
                rad = radius - thickness//2 + t
                x = int(cx + rad * math.cos(a))
                y = int(cy + rad * math.sin(a))
                self.set_pixel(x, y, r, g, b)
            # Half angles for smoother circle
            a = math.radians(angle + 0.5)
            for t in range(thickness):
                rad = radius - thickness//2 + t
                x = int(cx + rad * math.cos(a))
                y = int(cy + rad * math.sin(a))
                self.set_pixel(x, y, r, g, b)
    
    def save(self, filename):
        create_png(self.width, self.height, self.pixels, filename)


# ============================================================================
# FIGURE 1: Conceptual Framework
# ============================================================================
def create_figure1(output_dir):
    c = Canvas(800, 600)
    
    # Background gradient effect (light)
    c.fill_rect(0, 0, 799, 599, 250, 255, 250)
    
    # Title bar
    c.fill_rect(0, 0, 799, 50, 34, 87, 34)
    
    # Left circle fill (Regenerative Ag - green)
    cx1, cy1, r = 300, 310, 140
    c.fill_circle(cx1, cy1, r, 180, 238, 180)
    
    # Right circle fill (Agritourism - blue)
    cx2, cy2 = 500, 310
    c.fill_circle(cx2, cy2, r, 180, 210, 240)
    
    # Overlap area (gold) - fill where both circles overlap
    for dy in range(-r, r+1):
        y = cy1 + dy
        if 0 <= y < 600:
            dx_max1 = int(math.sqrt(max(0, r*r - dy*dy)))
            x_start1 = cx1 - dx_max1
            x_end1 = cx1 + dx_max1
            
            dy2 = y - cy2
            if abs(dy2) <= r:
                dx_max2 = int(math.sqrt(max(0, r*r - dy2*dy2)))
                x_start2 = cx2 - dx_max2
                x_end2 = cx2 + dx_max2
                
                # Overlap
                x_start = max(x_start1, x_start2)
                x_end = min(x_end1, x_end2)
                if x_start <= x_end:
                    row = bytes([240, 200, 80]) * (x_end - x_start + 1)
                    offset = (y * 800 + x_start) * 3
                    c.pixels[offset:offset+len(row)] = row
    
    # Circle outlines
    c.draw_circle(cx1, cy1, r, 0, 100, 0, 3)
    c.draw_circle(cx2, cy2, r, 0, 0, 139, 3)
    
    # Small dots in left circle (principles)
    for dx, dy in [(-60, -40), (-70, 20), (-40, 60), (-80, -10), (-30, -70)]:
        c.fill_circle(cx1+dx, cy1+dy, 6, 0, 80, 0)
    
    # Small dots in right circle (tourism elements)
    for dx, dy in [(60, -40), (70, 20), (40, 60), (80, -10), (30, -70)]:
        c.fill_circle(cx2+dx, cy2+dy, 6, 0, 0, 120)
    
    # Central synergy symbol
    c.fill_circle(400, 310, 15, 200, 120, 0)
    
    # Arrow pointing down from overlap
    c.draw_line(400, 450, 400, 550, 139, 69, 19, 3)
    c.draw_line(390, 540, 400, 555, 139, 69, 19, 3)
    c.draw_line(410, 540, 400, 555, 139, 69, 19, 3)
    
    # Legend
    c.fill_rect(50, 565, 75, 585, 180, 238, 180)
    c.draw_rect(50, 565, 75, 585, 0, 0, 0, 1)
    c.fill_rect(250, 565, 275, 585, 240, 200, 80)
    c.draw_rect(250, 565, 275, 585, 0, 0, 0, 1)
    c.fill_rect(500, 565, 525, 585, 180, 210, 240)
    c.draw_rect(500, 565, 525, 585, 0, 0, 0, 1)
    
    c.save(os.path.join(output_dir, "Figure_1_Conceptual_Framework.png"))
    print("  Created: Figure_1_Conceptual_Framework.png")


# ============================================================================
# FIGURE 2: Farm Design Layout
# ============================================================================
def create_figure2(output_dir):
    c = Canvas(800, 600)
    c.fill_rect(0, 0, 799, 599, 248, 255, 248)
    
    # Title bar
    c.fill_rect(0, 0, 799, 40, 85, 107, 47)
    
    # Zone 1: Visitor Center (bottom left)
    c.fill_rect(50, 430, 200, 550, 220, 190, 150)
    c.draw_rect(50, 430, 200, 550, 139, 69, 19, 2)
    # Building icon
    c.fill_rect(90, 460, 160, 530, 180, 140, 100)
    c.draw_line(90, 460, 125, 440, 100, 60, 20, 2)
    c.draw_line(125, 440, 160, 460, 100, 60, 20, 2)
    
    # Zone 2: Polyculture fields (center)
    c.fill_rect(230, 180, 550, 380, 144, 215, 144)
    c.draw_rect(230, 180, 550, 380, 0, 100, 0, 2)
    # Crop rows with variety
    for i, y in enumerate(range(200, 370, 18)):
        color = [(34, 139, 34), (60, 160, 60), (80, 180, 80), (34, 139, 34)][i % 4]
        c.draw_line(250, y, 530, y, *color, 2)
    
    # Zone 3: Grazing paddocks (top right)
    c.fill_rect(580, 70, 750, 230, 170, 215, 70)
    c.draw_rect(580, 70, 750, 230, 85, 107, 47, 2)
    # Fence posts
    for x in range(600, 740, 30):
        c.draw_line(x, 70, x, 230, 139, 119, 101, 1)
        c.fill_rect(x-2, 140, x+2, 150, 80, 50, 20)
    
    # Zone 4: Composting area (top left)
    c.fill_rect(50, 70, 200, 160, 160, 110, 60)
    c.draw_rect(50, 70, 200, 160, 101, 67, 33, 2)
    # Compost mound shapes
    for cx_off in [90, 140]:
        for dy in range(-20, 21):
            dx = int(math.sqrt(max(0, 400 - dy*dy)))
            y = 120 + dy
            c.draw_line(cx_off - dx//2, y, cx_off + dx//2, y, 120, 80, 40, 1)
    
    # Zone 5: Water features (center-right)
    c.fill_rect(580, 270, 750, 390, 160, 210, 240)
    c.draw_rect(580, 270, 750, 390, 0, 0, 139, 2)
    # Wavy lines
    for y in range(280, 380, 12):
        for x in range(590, 740, 2):
            ny = y + int(4 * math.sin(x * 0.08))
            c.set_pixel(x, ny, 30, 80, 200)
            c.set_pixel(x, ny+1, 30, 80, 200)
    
    # Nature trails (curved path)
    for i in range(200):
        t = i / 199
        x = int(220 + 350 * t)
        y = int(410 + 30 * math.sin(t * 4))
        c.fill_circle(x, y, 2, 194, 178, 128)
    
    # Hedgerow (top)
    for x in range(50, 760, 30):
        c.fill_circle(x, 55, 8, 34, 120, 34)
    
    # Legend
    legend_items = [
        (50, 220, 190, 150), (180, 144, 215, 144), (310, 170, 215, 70),
        (440, 160, 110, 60), (570, 160, 210, 240), (700, 194, 178, 128)
    ]
    for x, r, g, b in legend_items:
        c.fill_rect(x, 570, x+20, 590, r, g, b)
        c.draw_rect(x, 570, x+20, 590, 0, 0, 0, 1)
    
    c.save(os.path.join(output_dir, "Figure_2_Farm_Design_Layout.png"))
    print("  Created: Figure_2_Farm_Design_Layout.png")


# ============================================================================
# FIGURE 3: Revenue Diversification Bar Chart
# ============================================================================
def create_figure3(output_dir):
    c = Canvas(800, 600)
    c.fill_rect(0, 0, 799, 599, 255, 255, 255)
    
    # Title bar
    c.fill_rect(0, 0, 799, 45, 0, 100, 0)
    
    # Axes
    c.draw_line(100, 500, 720, 500, 0, 0, 0, 2)
    c.draw_line(100, 500, 100, 70, 0, 0, 0, 2)
    
    # Grid lines
    for i in range(1, 6):
        y = 500 - i * 80
        c.draw_line(100, y, 720, y, 220, 220, 220, 1)
    
    # Bars
    categories = [
        (160, 180, 300),   # Crop Sales
        (300, 140, 260),   # Livestock
        (440, 40, 340),    # Tourism Experiences
        (580, 20, 220),    # Education Programs
    ]
    
    bw = 50
    for x, trad_h, regen_h in categories:
        # Traditional (gray)
        c.fill_rect(x, 500-trad_h, x+bw, 500, 180, 180, 180)
        c.draw_rect(x, 500-trad_h, x+bw, 500, 120, 120, 120, 1)
        # Regenerative (green)
        c.fill_rect(x+bw+8, 500-regen_h, x+2*bw+8, 500, 34, 160, 34)
        c.draw_rect(x+bw+8, 500-regen_h, x+2*bw+8, 500, 0, 100, 0, 1)
    
    # Trend line
    pts = [(130, 460), (260, 380), (400, 280), (540, 200), (680, 140)]
    for i in range(len(pts)-1):
        c.draw_line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], 220, 50, 0, 3)
    # Arrowhead
    c.draw_line(680, 140, 668, 152, 220, 50, 0, 3)
    c.draw_line(680, 140, 670, 135, 220, 50, 0, 3)
    
    # Legend
    c.fill_rect(550, 65, 580, 85, 180, 180, 180)
    c.draw_rect(550, 65, 580, 85, 0, 0, 0, 1)
    c.fill_rect(550, 95, 580, 115, 34, 160, 34)
    c.draw_rect(550, 95, 580, 115, 0, 0, 0, 1)
    c.fill_rect(550, 125, 580, 145, 220, 50, 0)
    c.draw_rect(550, 125, 580, 145, 0, 0, 0, 1)
    
    # Y-axis markers
    for i in range(6):
        y = 500 - i * 80
        c.draw_line(95, y, 100, y, 0, 0, 0, 2)
    
    c.save(os.path.join(output_dir, "Figure_3_Revenue_Diversification.png"))
    print("  Created: Figure_3_Revenue_Diversification.png")


# ============================================================================
# FIGURE 4: Holistic Model - Hub and Spoke Diagram
# ============================================================================
def create_figure4(output_dir):
    c = Canvas(800, 600)
    c.fill_rect(0, 0, 799, 599, 252, 252, 255)
    
    # Title bar
    c.fill_rect(0, 0, 799, 40, 70, 130, 180)
    
    # Central hub
    c.fill_circle(400, 300, 50, 240, 190, 60)
    c.draw_circle(400, 300, 50, 160, 100, 0, 3)
    
    # 6 surrounding nodes
    colors = [
        (34, 139, 34),    # Ecological Restoration
        (0, 0, 160),      # Economic Viability
        (160, 30, 30),    # Social/Cultural
        (128, 0, 128),    # Policy Framework
        (220, 140, 0),    # Education
        (0, 130, 130),    # Community
    ]
    
    nodes = []
    for i in range(6):
        angle = math.radians(60 * i - 90)
        nx = int(400 + 180 * math.cos(angle))
        ny = int(300 + 180 * math.sin(angle))
        nodes.append((nx, ny))
    
    # Draw connecting lines first
    for nx, ny in nodes:
        c.draw_line(400, 300, nx, ny, 150, 150, 150, 2)
    
    # Draw outer connections
    for i in range(6):
        x1, y1 = nodes[i]
        x2, y2 = nodes[(i+1) % 6]
        c.draw_line(x1, y1, x2, y2, 200, 200, 200, 1)
    
    # Draw nodes on top
    for i, (nx, ny) in enumerate(nodes):
        r, g, b = colors[i]
        c.fill_circle(nx, ny, 35, r, g, b)
        c.draw_circle(nx, ny, 35, 0, 0, 0, 2)
    
    # Direction arrows on spokes
    for i, (nx, ny) in enumerate(nodes):
        # Midpoint arrow indicator
        mx = (400 + nx) // 2
        my = (300 + ny) // 2
        c.fill_circle(mx, my, 4, 100, 100, 100)
    
    # Outer ring (dashed)
    for angle in range(0, 360, 3):
        if angle % 6 < 3:
            a = math.radians(angle)
            x = int(400 + 230 * math.cos(a))
            y = int(300 + 230 * math.sin(a))
            c.set_pixel(x, y, 150, 150, 150)
            c.set_pixel(x+1, y, 150, 150, 150)
            c.set_pixel(x, y+1, 150, 150, 150)
    
    # Legend at bottom
    for i, (r, g, b) in enumerate(colors):
        x = 60 + i * 120
        c.fill_rect(x, 555, x+22, 577, r, g, b)
        c.draw_rect(x, 555, x+22, 577, 0, 0, 0, 1)
    
    c.save(os.path.join(output_dir, "Figure_4_Holistic_Model.png"))
    print("  Created: Figure_4_Holistic_Model.png")


def main():
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "book_figures")
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating book figures...")
    create_figure1(output_dir)
    create_figure2(output_dir)
    create_figure3(output_dir)
    create_figure4(output_dir)
    print("All 4 figures generated successfully!")


if __name__ == "__main__":
    main()
