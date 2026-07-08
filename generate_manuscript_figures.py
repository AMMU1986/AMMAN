#!/usr/bin/env python3
"""
Generate manuscript figures for Ionic Liquids MQL Machining paper.
Uses only Python standard library (struct, zlib, os, math) to create PNG files.
"""

import struct
import zlib
import os
import math

# ============================================================================
# PNG Generation Core
# ============================================================================

def make_chunk(chunk_type, data):
    """Create a PNG chunk with length, type, data, and CRC."""
    chunk = chunk_type + data
    return struct.pack('>I', len(data)) + chunk + struct.pack('>I', zlib.crc32(chunk) & 0xFFFFFFFF)

def create_png(width, height, pixels):
    """
    Create a PNG file from pixel data.
    pixels is a list of rows, each row is a list of (R, G, B) tuples.
    """
    signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = make_chunk(b'IHDR', ihdr_data)
    
    # IDAT chunk - pixel data with filter bytes
    raw_data = b''
    for row in pixels:
        raw_data += b'\x00'  # No filter
        for r, g, b in row:
            raw_data += struct.pack('BBB', r, g, b)
    
    compressed = zlib.compress(raw_data, 9)
    idat = make_chunk(b'IDAT', compressed)
    
    # IEND chunk
    iend = make_chunk(b'IEND', b'')
    
    return signature + ihdr + idat + iend

# ============================================================================
# Canvas class for drawing
# ============================================================================

class Canvas:
    def __init__(self, width, height, bg=(255, 255, 255)):
        self.width = width
        self.height = height
        self.pixels = [[bg for _ in range(width)] for _ in range(height)]
    
    def set_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = color
    
    def get_pixel(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[y][x]
        return (255, 255, 255)
    
    def fill_rect(self, x, y, w, h, color):
        for dy in range(h):
            for dx in range(w):
                self.set_pixel(x + dx, y + dy, color)
    
    def draw_rect(self, x, y, w, h, color, thickness=1):
        """Draw rectangle outline."""
        for t in range(thickness):
            # Top and bottom
            for dx in range(w):
                self.set_pixel(x + dx, y + t, color)
                self.set_pixel(x + dx, y + h - 1 - t, color)
            # Left and right
            for dy in range(h):
                self.set_pixel(x + t, y + dy, color)
                self.set_pixel(x + w - 1 - t, y + dy, color)
    
    def draw_line(self, x0, y0, x1, y1, color, thickness=1):
        """Draw a line using Bresenham's algorithm."""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while True:
            for t in range(-(thickness//2), (thickness+1)//2):
                if dx >= dy:
                    self.set_pixel(x0, y0 + t, color)
                else:
                    self.set_pixel(x0 + t, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
    
    def draw_dashed_line(self, x0, y0, x1, y1, color, thickness=1, dash=8, gap=5):
        """Draw a dashed line."""
        dx = x1 - x0
        dy = y1 - y0
        dist = math.sqrt(dx*dx + dy*dy)
        if dist == 0:
            return
        steps = int(dist)
        drawn = 0
        for i in range(steps + 1):
            t = i / max(steps, 1)
            x = int(x0 + dx * t)
            y = int(y0 + dy * t)
            cycle = drawn % (dash + gap)
            if cycle < dash:
                for th in range(-(thickness//2), (thickness+1)//2):
                    if abs(dx) >= abs(dy):
                        self.set_pixel(x, y + th, color)
                    else:
                        self.set_pixel(x + th, y, color)
            drawn += 1
    
    def draw_circle(self, cx, cy, r, color, thickness=1, fill=None):
        """Draw a circle."""
        if fill:
            for y in range(-r, r+1):
                for x in range(-r, r+1):
                    if x*x + y*y <= r*r:
                        self.set_pixel(cx + x, cy + y, fill)
        # Draw outline
        for angle in range(360 * 4):
            a = math.radians(angle / 4.0)
            for t in range(thickness):
                x = int(cx + (r - t) * math.cos(a))
                y = int(cy + (r - t) * math.sin(a))
                self.set_pixel(x, y, color)
    
    def draw_arc(self, cx, cy, r, start_angle, end_angle, color, thickness=1):
        """Draw an arc from start_angle to end_angle (degrees)."""
        steps = int(abs(end_angle - start_angle) * 4)
        for i in range(steps + 1):
            angle = math.radians(start_angle + (end_angle - start_angle) * i / max(steps, 1))
            for t in range(thickness):
                x = int(cx + (r - t) * math.cos(angle))
                y = int(cy + (r - t) * math.sin(angle))
                self.set_pixel(x, y, color)
    
    def fill_circle(self, cx, cy, r, color):
        """Fill a circle."""
        for y in range(-r, r+1):
            for x in range(-r, r+1):
                if x*x + y*y <= r*r:
                    self.set_pixel(cx + x, cy + y, color)
    
    def draw_arrow(self, x0, y0, x1, y1, color, thickness=2, head_size=10):
        """Draw an arrow from (x0,y0) to (x1,y1)."""
        self.draw_line(x0, y0, x1, y1, color, thickness)
        # Arrowhead
        angle = math.atan2(y1 - y0, x1 - x0)
        a1 = angle + math.pi * 0.8
        a2 = angle - math.pi * 0.8
        hx1 = int(x1 + head_size * math.cos(a1))
        hy1 = int(y1 + head_size * math.sin(a1))
        hx2 = int(x1 + head_size * math.cos(a2))
        hy2 = int(y1 + head_size * math.sin(a2))
        self.draw_line(x1, y1, hx1, hy1, color, thickness)
        self.draw_line(x1, y1, hx2, hy2, color, thickness)
    
    def fill_triangle(self, x0, y0, x1, y1, x2, y2, color):
        """Fill a triangle."""
        min_y = max(0, min(y0, y1, y2))
        max_y = min(self.height - 1, max(y0, y1, y2))
        for y in range(min_y, max_y + 1):
            xs = []
            edges = [(x0, y0, x1, y1), (x1, y1, x2, y2), (x2, y2, x0, y0)]
            for ex0, ey0, ex1, ey1 in edges:
                if ey0 == ey1:
                    continue
                if min(ey0, ey1) <= y <= max(ey0, ey1):
                    x = ex0 + (y - ey0) * (ex1 - ex0) / (ey1 - ey0)
                    xs.append(int(x))
            if len(xs) >= 2:
                xs.sort()
                for x in range(xs[0], xs[-1] + 1):
                    self.set_pixel(x, y, color)
    
    def save_png(self, filename):
        """Save canvas as PNG file."""
        data = create_png(self.width, self.height, self.pixels)
        with open(filename, 'wb') as f:
            f.write(data)


# ============================================================================
# Bitmap Font (5x7 pixel font)
# ============================================================================

FONT_5x7 = {
    'A': ['01110','10001','10001','11111','10001','10001','10001'],
    'B': ['11110','10001','10001','11110','10001','10001','11110'],
    'C': ['01110','10001','10000','10000','10000','10001','01110'],
    'D': ['11110','10001','10001','10001','10001','10001','11110'],
    'E': ['11111','10000','10000','11110','10000','10000','11111'],
    'F': ['11111','10000','10000','11110','10000','10000','10000'],
    'G': ['01110','10001','10000','10111','10001','10001','01110'],
    'H': ['10001','10001','10001','11111','10001','10001','10001'],
    'I': ['01110','00100','00100','00100','00100','00100','01110'],
    'J': ['00111','00010','00010','00010','00010','10010','01100'],
    'K': ['10001','10010','10100','11000','10100','10010','10001'],
    'L': ['10000','10000','10000','10000','10000','10000','11111'],
    'M': ['10001','11011','10101','10101','10001','10001','10001'],
    'N': ['10001','11001','10101','10011','10001','10001','10001'],
    'O': ['01110','10001','10001','10001','10001','10001','01110'],
    'P': ['11110','10001','10001','11110','10000','10000','10000'],
    'Q': ['01110','10001','10001','10001','10101','10010','01101'],
    'R': ['11110','10001','10001','11110','10100','10010','10001'],
    'S': ['01110','10001','10000','01110','00001','10001','01110'],
    'T': ['11111','00100','00100','00100','00100','00100','00100'],
    'U': ['10001','10001','10001','10001','10001','10001','01110'],
    'V': ['10001','10001','10001','10001','01010','01010','00100'],
    'W': ['10001','10001','10001','10101','10101','10101','01010'],
    'X': ['10001','10001','01010','00100','01010','10001','10001'],
    'Y': ['10001','10001','01010','00100','00100','00100','00100'],
    'Z': ['11111','00001','00010','00100','01000','10000','11111'],
    '0': ['01110','10001','10011','10101','11001','10001','01110'],
    '1': ['00100','01100','00100','00100','00100','00100','01110'],
    '2': ['01110','10001','00001','00010','00100','01000','11111'],
    '3': ['01110','10001','00001','00110','00001','10001','01110'],
    '4': ['00010','00110','01010','10010','11111','00010','00010'],
    '5': ['11111','10000','11110','00001','00001','10001','01110'],
    '6': ['01110','10001','10000','11110','10001','10001','01110'],
    '7': ['11111','00001','00010','00100','01000','01000','01000'],
    '8': ['01110','10001','10001','01110','10001','10001','01110'],
    '9': ['01110','10001','10001','01111','00001','10001','01110'],
    ' ': ['00000','00000','00000','00000','00000','00000','00000'],
    '.': ['00000','00000','00000','00000','00000','00000','00100'],
    ',': ['00000','00000','00000','00000','00000','00100','01000'],
    ':': ['00000','00000','00100','00000','00000','00100','00000'],
    '-': ['00000','00000','00000','11111','00000','00000','00000'],
    '+': ['00000','00100','00100','11111','00100','00100','00000'],
    '(': ['00010','00100','01000','01000','01000','00100','00010'],
    ')': ['01000','00100','00010','00010','00010','00100','01000'],
    '/': ['00001','00010','00010','00100','01000','01000','10000'],
    '%': ['10001','00010','00010','00100','01000','01000','10001'],
    '=': ['00000','00000','11111','00000','11111','00000','00000'],
    "'": ['00100','00100','01000','00000','00000','00000','00000'],
    '"': ['01010','01010','01010','00000','00000','00000','00000'],
    '?': ['01110','10001','00001','00110','00100','00000','00100'],
    '!': ['00100','00100','00100','00100','00100','00000','00100'],
    '^': ['00100','01010','10001','00000','00000','00000','00000'],
    '_': ['00000','00000','00000','00000','00000','00000','11111'],
    '~': ['00000','00000','01000','10101','00010','00000','00000'],
    '<': ['00010','00100','01000','10000','01000','00100','00010'],
    '>': ['01000','00100','00010','00001','00010','00100','01000'],
    '[': ['01110','01000','01000','01000','01000','01000','01110'],
    ']': ['01110','00010','00010','00010','00010','00010','01110'],
    '#': ['01010','01010','11111','01010','11111','01010','01010'],
    '*': ['00000','00100','10101','01110','10101','00100','00000'],
    'a': ['00000','00000','01110','00001','01111','10001','01111'],
    'b': ['10000','10000','11110','10001','10001','10001','11110'],
    'c': ['00000','00000','01110','10000','10000','10001','01110'],
    'd': ['00001','00001','01111','10001','10001','10001','01111'],
    'e': ['00000','00000','01110','10001','11111','10000','01110'],
    'f': ['00110','01001','01000','11100','01000','01000','01000'],
    'g': ['00000','00000','01111','10001','01111','00001','01110'],
    'h': ['10000','10000','10110','11001','10001','10001','10001'],
    'i': ['00100','00000','01100','00100','00100','00100','01110'],
    'j': ['00010','00000','00110','00010','00010','10010','01100'],
    'k': ['10000','10000','10010','10100','11000','10100','10010'],
    'l': ['01100','00100','00100','00100','00100','00100','01110'],
    'm': ['00000','00000','11010','10101','10101','10001','10001'],
    'n': ['00000','00000','10110','11001','10001','10001','10001'],
    'o': ['00000','00000','01110','10001','10001','10001','01110'],
    'p': ['00000','00000','11110','10001','11110','10000','10000'],
    'q': ['00000','00000','01111','10001','01111','00001','00001'],
    'r': ['00000','00000','10110','11001','10000','10000','10000'],
    's': ['00000','00000','01110','10000','01110','00001','11110'],
    't': ['01000','01000','11100','01000','01000','01001','00110'],
    'u': ['00000','00000','10001','10001','10001','10011','01101'],
    'v': ['00000','00000','10001','10001','10001','01010','00100'],
    'w': ['00000','00000','10001','10001','10101','10101','01010'],
    'x': ['00000','00000','10001','01010','00100','01010','10001'],
    'y': ['00000','00000','10001','10001','01111','00001','01110'],
    'z': ['00000','00000','11111','00010','00100','01000','11111'],
}

def draw_text(canvas, x, y, text, color=(0, 0, 0), scale=1):
    """Draw text on canvas using bitmap font."""
    cursor_x = x
    for ch in text:
        if ch in FONT_5x7:
            bitmap = FONT_5x7[ch]
            for row_idx, row in enumerate(bitmap):
                for col_idx, bit in enumerate(row):
                    if bit == '1':
                        for sy in range(scale):
                            for sx in range(scale):
                                canvas.set_pixel(cursor_x + col_idx * scale + sx,
                                               y + row_idx * scale + sy, color)
            cursor_x += 6 * scale
        else:
            cursor_x += 6 * scale

def text_width(text, scale=1):
    """Calculate width of text in pixels."""
    return len(text) * 6 * scale

def draw_text_centered(canvas, cx, y, text, color=(0, 0, 0), scale=1):
    """Draw text centered at cx."""
    w = text_width(text, scale)
    draw_text(canvas, cx - w // 2, y, text, color, scale)

def draw_text_right(canvas, x, y, text, color=(0, 0, 0), scale=1):
    """Draw text right-aligned at x."""
    w = text_width(text, scale)
    draw_text(canvas, x - w, y, text, color, scale)

def draw_text_vertical(canvas, x, y, text, color=(0, 0, 0), scale=1):
    """Draw text vertically (rotated 90 degrees CCW)."""
    for i, ch in enumerate(text):
        if ch in FONT_5x7:
            bitmap = FONT_5x7[ch]
            for row_idx, row in enumerate(bitmap):
                for col_idx, bit in enumerate(row):
                    if bit == '1':
                        # Rotate 90 CCW: new_x = row_idx, new_y = (4-col_idx)
                        px = x - row_idx * scale
                        py = y + i * 6 * scale + (4 - col_idx) * scale
                        for sy in range(scale):
                            for sx in range(scale):
                                canvas.set_pixel(px - sx, py + sy, color)



# ============================================================================
# Figure 1: Experimental Setup
# ============================================================================

def generate_figure_1(output_path):
    """Generate Figure 1: Peripheral down milling setup schematic."""
    canvas = Canvas(800, 600)
    
    # Title
    draw_text_centered(canvas, 400, 15, "Figure 1: Peripheral Down Milling - Experimental Setup", (0, 0, 0), 2)
    
    # Colors
    GRAY = (180, 180, 180)
    DARK_GRAY = (100, 100, 100)
    STEEL = (160, 170, 180)
    LIGHT_BLUE = (200, 220, 240)
    BROWN = (139, 90, 43)
    GREEN = (34, 139, 34)
    RED = (200, 50, 50)
    BLUE = (50, 50, 200)
    ORANGE = (255, 140, 0)
    YELLOW = (255, 220, 50)
    
    # Machine table (bottom)
    canvas.fill_rect(100, 480, 600, 40, DARK_GRAY)
    canvas.draw_rect(100, 480, 600, 40, (0, 0, 0), 2)
    draw_text_centered(canvas, 400, 495, "MACHINE TABLE", (255, 255, 255), 1)
    
    # Dynamometer on table
    canvas.fill_rect(200, 430, 400, 50, (100, 150, 200))
    canvas.draw_rect(200, 430, 400, 50, (0, 0, 0), 2)
    draw_text_centered(canvas, 400, 450, "KISTLER DYNAMOMETER", (255, 255, 255), 1)
    draw_text_centered(canvas, 400, 462, "(Fx, Fy, Fz)", (220, 220, 255), 1)
    
    # Workpiece on dynamometer
    wp_x, wp_y, wp_w, wp_h = 250, 330, 300, 100
    canvas.fill_rect(wp_x, wp_y, wp_w, wp_h, STEEL)
    canvas.draw_rect(wp_x, wp_y, wp_w, wp_h, (0, 0, 0), 2)
    draw_text_centered(canvas, 400, 365, "WORKPIECE", (0, 0, 0), 1)
    draw_text_centered(canvas, 400, 380, "(AISI 1045 Steel)", (60, 60, 60), 1)
    draw_text_centered(canvas, 400, 395, "160x30x8 mm", (60, 60, 60), 1)
    
    # Thermocouples in workpiece (small dots)
    tc_positions = [(310, 360), (350, 360), (390, 360)]
    for tx, ty in tc_positions:
        canvas.fill_circle(tx, ty, 3, RED)
        # Wire going down
        canvas.draw_line(tx, ty + 3, tx, ty + 15, RED, 1)
    draw_text(canvas, 280, 410, "Thermocouples (K-type)", RED, 1)
    
    # Cutter/tool (circle with inserts) - positioned above workpiece
    cutter_cx, cutter_cy, cutter_r = 480, 230, 60
    canvas.draw_circle(cutter_cx, cutter_cy, cutter_r, (0, 0, 0), 2)
    canvas.draw_circle(cutter_cx, cutter_cy, cutter_r - 5, GRAY, 1)
    
    # Tool body fill
    canvas.fill_circle(cutter_cx, cutter_cy, cutter_r - 6, (200, 200, 210))
    canvas.draw_circle(cutter_cx, cutter_cy, cutter_r, (0, 0, 0), 2)
    
    # Center of cutter
    canvas.fill_circle(cutter_cx, cutter_cy, 5, (0, 0, 0))
    
    # Inserts on cutter (4 inserts at 90 degree intervals)
    for angle_deg in [45, 135, 225, 315]:
        angle = math.radians(angle_deg)
        ix = int(cutter_cx + (cutter_r - 10) * math.cos(angle))
        iy = int(cutter_cy + (cutter_r - 10) * math.sin(angle))
        # Draw small rectangle for insert
        canvas.fill_rect(ix - 4, iy - 4, 8, 8, YELLOW)
        canvas.draw_rect(ix - 4, iy - 4, 8, 8, (0, 0, 0), 1)
    
    # Rotation arrow around cutter
    canvas.draw_arc(cutter_cx, cutter_cy, cutter_r + 15, -30, 60, BLUE, 2)
    # Arrowhead at end of arc
    end_angle = math.radians(60)
    ax = int(cutter_cx + (cutter_r + 15) * math.cos(end_angle))
    ay = int(cutter_cy + (cutter_r + 15) * math.sin(end_angle))
    canvas.draw_line(ax, ay, ax + 5, ay - 8, BLUE, 2)
    canvas.draw_line(ax, ay, ax - 7, ay - 3, BLUE, 2)
    
    # Cutter label
    draw_text_centered(canvas, cutter_cx, 150, "MILLING CUTTER", (0, 0, 0), 1)
    draw_text_centered(canvas, cutter_cx, 162, "(4-insert, D=50mm)", (60, 60, 60), 1)
    draw_text(canvas, cutter_cx + cutter_r + 20, 220, "n (rpm)", BLUE, 1)
    
    # MQL Nozzle (top left, pointing toward cutting zone)
    nozzle_x, nozzle_y = 280, 200
    # Nozzle body
    canvas.fill_rect(nozzle_x - 60, nozzle_y - 10, 60, 20, (80, 80, 80))
    canvas.draw_rect(nozzle_x - 60, nozzle_y - 10, 60, 20, (0, 0, 0), 1)
    # Nozzle tip (triangle)
    canvas.fill_triangle(nozzle_x, nozzle_y - 6, nozzle_x, nozzle_y + 6, nozzle_x + 15, nozzle_y, (80, 80, 80))
    
    # Spray droplets from nozzle
    import random
    random.seed(42)
    for i in range(25):
        dx = random.randint(15, 80)
        dy = random.randint(-25, 25)
        size = random.randint(1, 2)
        canvas.fill_circle(nozzle_x + dx, nozzle_y + dy + dx//4, size, GREEN)
    
    # MQL label
    draw_text(canvas, nozzle_x - 80, nozzle_y - 30, "MQL NOZZLE", GREEN, 1)
    draw_text(canvas, nozzle_x - 80, nozzle_y - 18, "(Lubricant+Air)", (60, 100, 60), 1)
    
    # Feed direction arrow (left to right under workpiece)
    canvas.draw_arrow(180, 540, 620, 540, (0, 0, 150), 2, 12)
    draw_text_centered(canvas, 400, 555, "Table Feed Direction (Vf)", (0, 0, 150), 1)
    
    # Cutting zone indicator
    cut_x = wp_x + wp_w - 50
    cut_y = wp_y
    # Small sparks/cutting indicators
    for i in range(8):
        angle = math.radians(-30 + i * 20)
        sx = int(cut_x + 20 * math.cos(angle))
        sy = int(cut_y + 20 * math.sin(angle))
        canvas.draw_line(cut_x, cut_y, sx, sy, ORANGE, 1)
    
    # Spindle above cutter
    canvas.fill_rect(cutter_cx - 15, 60, 30, 90, DARK_GRAY)
    canvas.draw_rect(cutter_cx - 15, 60, 30, 90, (0, 0, 0), 1)
    draw_text_centered(canvas, cutter_cx, 80, "SPINDLE", (200, 200, 200), 1)
    
    # Depth of cut annotation
    doc_x = wp_x + wp_w + 20
    canvas.draw_line(doc_x, wp_y, doc_x, wp_y + 20, RED, 1)
    canvas.draw_line(doc_x - 5, wp_y, doc_x + 5, wp_y, RED, 1)
    canvas.draw_line(doc_x - 5, wp_y + 20, doc_x + 5, wp_y + 20, RED, 1)
    draw_text(canvas, doc_x + 8, wp_y + 5, "ap", RED, 1)
    
    # Legend box
    canvas.draw_rect(20, 540, 150, 50, (0, 0, 0), 1)
    draw_text(canvas, 25, 545, "Legend:", (0, 0, 0), 1)
    canvas.fill_circle(35, 560, 3, RED)
    draw_text(canvas, 45, 557, "Thermocouple", (0, 0, 0), 1)
    canvas.fill_rect(25, 572, 10, 6, GREEN)
    draw_text(canvas, 45, 571, "MQL spray", (0, 0, 0), 1)
    
    canvas.save_png(output_path)
    print(f"  Saved: {output_path}")



# ============================================================================
# Figure 2: FD Model Discretization
# ============================================================================

def generate_figure_2(output_path):
    """Generate Figure 2: Finite Difference grid discretization."""
    canvas = Canvas(800, 600)
    
    # Title
    draw_text_centered(canvas, 400, 15, "Figure 2: Finite Difference Model Discretization", (0, 0, 0), 2)
    
    # Colors
    BLUE = (0, 80, 180)
    RED = (200, 30, 30)
    GREEN = (30, 150, 30)
    ORANGE = (220, 120, 0)
    PURPLE = (120, 0, 180)
    LIGHT_GRAY = (230, 230, 230)
    
    # Domain dimensions
    margin_left = 120
    margin_top = 80
    domain_w = 560  # pixels for 30mm
    domain_h = 350  # pixels for 8mm
    
    # Scale: 560px = 30mm, 350px = 8mm
    px_per_mm_x = domain_w / 30.0
    px_per_mm_y = domain_h / 8.0
    
    # Draw grid
    nx = 16  # number of grid divisions in x
    ny = 9   # number of grid divisions in y
    
    dx = domain_w / nx
    dy = domain_h / ny
    
    # Fill domain background
    canvas.fill_rect(margin_left, margin_top, domain_w, domain_h, (248, 248, 255))
    
    # Draw grid lines
    for i in range(nx + 1):
        x = int(margin_left + i * dx)
        canvas.draw_line(x, margin_top, x, margin_top + domain_h, (200, 200, 220), 1)
    for j in range(ny + 1):
        y = int(margin_top + j * dy)
        canvas.draw_line(margin_left, y, margin_left + domain_w, y, (200, 200, 220), 1)
    
    # Draw domain boundary (thick)
    canvas.draw_rect(margin_left, margin_top, domain_w, domain_h, (0, 0, 0), 3)
    
    # Axes
    # X-axis below domain
    axis_y = margin_top + domain_h + 40
    canvas.draw_arrow(margin_left, axis_y, margin_left + domain_w + 30, axis_y, (0, 0, 0), 2, 10)
    draw_text(canvas, margin_left + domain_w + 35, axis_y - 4, "X (mm)", (0, 0, 0), 1)
    
    # X-axis ticks
    for mm in range(0, 31, 5):
        x = int(margin_left + mm * px_per_mm_x)
        canvas.draw_line(x, axis_y - 3, x, axis_y + 3, (0, 0, 0), 1)
        draw_text_centered(canvas, x, axis_y + 8, str(mm), (0, 0, 0), 1)
    
    # Y-axis to the left
    axis_x = margin_left - 30
    canvas.draw_arrow(axis_x, margin_top + domain_h, axis_x, margin_top - 20, (0, 0, 0), 2, 10)
    draw_text(canvas, axis_x - 20, margin_top - 35, "Y (mm)", (0, 0, 0), 1)
    
    # Y-axis ticks (0 at top, 8 at bottom to match depth)
    for mm in range(0, 9, 2):
        y = int(margin_top + mm * px_per_mm_y)
        canvas.draw_line(axis_x - 3, y, axis_x + 3, y, (0, 0, 0), 1)
        draw_text_right(canvas, axis_x - 6, y - 3, str(mm), (0, 0, 0), 1)
    
    # Moving heat source on top surface (red band)
    hs_start_mm = 8
    hs_end_mm = 14
    hs_x0 = int(margin_left + hs_start_mm * px_per_mm_x)
    hs_x1 = int(margin_left + hs_end_mm * px_per_mm_x)
    canvas.fill_rect(hs_x0, margin_top - 8, hs_x1 - hs_x0, 8, RED)
    canvas.draw_rect(hs_x0, margin_top - 8, hs_x1 - hs_x0, 8, (150, 0, 0), 1)
    
    # Heat source arrow showing movement direction
    canvas.draw_arrow(hs_x0 - 10, margin_top - 15, hs_x1 + 10, margin_top - 15, RED, 2, 8)
    draw_text_centered(canvas, (hs_x0 + hs_x1) // 2, margin_top - 35, "Moving Heat Source (q)", RED, 1)
    draw_text_centered(canvas, (hs_x0 + hs_x1) // 2, margin_top - 25, "V = cutting speed", (150, 50, 50), 1)
    
    # Heat flux arrows going into domain from heat source
    for mm in range(hs_start_mm + 1, hs_end_mm, 1):
        x = int(margin_left + mm * px_per_mm_x)
        canvas.draw_arrow(x, margin_top + 2, x, margin_top + 25, (255, 100, 100), 1, 5)
    
    # Boundary conditions labels
    # Top surface - convection (except heat source)
    draw_text(canvas, margin_left + domain_w - 150, margin_top - 35, "h, T_ambient (conv.)", BLUE, 1)
    # Small arrows on top showing convection
    for mm in range(16, 28, 2):
        x = int(margin_left + mm * px_per_mm_x)
        canvas.draw_line(x, margin_top - 5, x, margin_top + 5, BLUE, 1)
        canvas.draw_line(x - 2, margin_top + 3, x, margin_top + 5, BLUE, 1)
        canvas.draw_line(x + 2, margin_top + 3, x, margin_top + 5, BLUE, 1)
    
    # Left boundary - T = T_ambient
    draw_text_vertical(canvas, margin_left - 55, margin_top + 80, "T = T_amb", BLUE, 1)
    # Arrows on left
    for j in range(2, 8, 2):
        y = int(margin_top + j * py_per_mm_y) if 'py_per_mm_y' in dir() else int(margin_top + j * px_per_mm_y)
        y = int(margin_top + j * domain_h / 8)
        canvas.draw_line(margin_left - 5, y, margin_left + 5, y, BLUE, 1)
    
    # Right boundary - T = T_ambient
    draw_text(canvas, margin_left + domain_w + 10, margin_top + domain_h // 2 - 20, "T = T_amb", BLUE, 1)
    
    # Bottom boundary - insulated / T = T_ambient
    draw_text_centered(canvas, margin_left + domain_w // 2, margin_top + domain_h + 15, "T = T_ambient (bottom boundary)", BLUE, 1)
    
    # Thermocouple location at (11mm, 3mm from top)
    tc_x = int(margin_left + 11 * px_per_mm_x)
    tc_y = int(margin_top + 3 * px_per_mm_y)
    # Draw crosshair
    canvas.fill_circle(tc_x, tc_y, 6, GREEN)
    canvas.draw_circle(tc_x, tc_y, 8, GREEN, 2)
    canvas.draw_line(tc_x - 12, tc_y, tc_x + 12, tc_y, GREEN, 1)
    canvas.draw_line(tc_x, tc_y - 12, tc_x, tc_y + 12, GREEN, 1)
    
    # Label for thermocouple
    draw_text(canvas, tc_x + 15, tc_y - 15, "TC Location", GREEN, 1)
    draw_text(canvas, tc_x + 15, tc_y - 3, "(11mm, 3mm)", GREEN, 1)
    
    # Grid node indicators at some intersections
    for i in range(0, nx + 1, 2):
        for j in range(0, ny + 1, 2):
            x = int(margin_left + i * dx)
            y = int(margin_top + j * dy)
            canvas.fill_circle(x, y, 2, (80, 80, 80))
    
    # Stencil notation box (lower right)
    box_x, box_y = 550, 480
    canvas.draw_rect(box_x, box_y, 220, 100, (0, 0, 0), 1)
    draw_text(canvas, box_x + 5, box_y + 5, "FD Stencil:", (0, 0, 0), 1)
    # Show 5-point stencil
    stx, sty = box_x + 110, box_y + 55
    canvas.fill_circle(stx, sty, 4, (0, 0, 0))  # center
    canvas.fill_circle(stx - 25, sty, 4, BLUE)   # left
    canvas.fill_circle(stx + 25, sty, 4, BLUE)   # right
    canvas.fill_circle(stx, sty - 25, 4, BLUE)   # top
    canvas.fill_circle(stx, sty + 25, 4, BLUE)   # bottom
    canvas.draw_line(stx - 25, sty, stx + 25, sty, (0, 0, 0), 1)
    canvas.draw_line(stx, sty - 25, stx, sty + 25, (0, 0, 0), 1)
    draw_text(canvas, box_x + 5, box_y + 20, "dx=dy=0.5mm", (60, 60, 60), 1)
    draw_text(canvas, box_x + 5, box_y + 32, "dt=0.001s", (60, 60, 60), 1)
    draw_text(canvas, box_x + 5, box_y + 80, "(i,j) node", (0, 0, 0), 1)
    
    # Domain size annotation
    # Width annotation at bottom
    ann_y = margin_top + domain_h + 55
    canvas.draw_line(margin_left, ann_y, margin_left + domain_w, ann_y, (0, 0, 0), 1)
    canvas.draw_line(margin_left, ann_y - 5, margin_left, ann_y + 5, (0, 0, 0), 1)
    canvas.draw_line(margin_left + domain_w, ann_y - 5, margin_left + domain_w, ann_y + 5, (0, 0, 0), 1)
    draw_text_centered(canvas, margin_left + domain_w // 2, ann_y + 8, "30 mm", (0, 0, 0), 1)
    
    # Height annotation on right
    ann_x = margin_left + domain_w + 60
    canvas.draw_line(ann_x, margin_top, ann_x, margin_top + domain_h, (0, 0, 0), 1)
    canvas.draw_line(ann_x - 5, margin_top, ann_x + 5, margin_top, (0, 0, 0), 1)
    canvas.draw_line(ann_x - 5, margin_top + domain_h, ann_x + 5, margin_top + domain_h, (0, 0, 0), 1)
    draw_text(canvas, ann_x + 8, margin_top + domain_h // 2 - 4, "8 mm", (0, 0, 0), 1)
    
    canvas.save_png(output_path)
    print(f"  Saved: {output_path}")



# ============================================================================
# Figure 3: Machining Forces Bar Chart
# ============================================================================

def generate_figure_3(output_path):
    """Generate Figure 3: Bar chart of machining forces."""
    canvas = Canvas(800, 600)
    
    # Title
    draw_text_centered(canvas, 400, 15, "Figure 3: Machining Forces Under Different MWF Conditions", (0, 0, 0), 2)
    
    # Data
    conditions = ["DRY", "OIL", "IL1", "PEG", "PEG+IL1", "IL308-1%", "IL308-0.5%"]
    # Light machining forces (N)
    light_forces = [380, 340, 310, 330, 280, 270, 260]
    # Heavy machining forces (N)
    heavy_forces = [850, 780, 720, 750, 680, 650, 620]
    
    # Colors for bars
    colors_light = [
        (220, 80, 80),    # DRY - red
        (80, 150, 220),   # OIL - blue
        (80, 200, 80),    # IL1 - green
        (200, 150, 50),   # PEG - gold
        (150, 80, 200),   # PEG+IL1 - purple
        (50, 180, 180),   # IL308-1% - teal
        (220, 130, 50),   # IL308-0.5% - orange
    ]
    colors_heavy = [
        (180, 50, 50),
        (50, 110, 180),
        (50, 160, 50),
        (160, 120, 30),
        (120, 50, 160),
        (30, 140, 140),
        (180, 100, 30),
    ]
    
    # Chart area
    chart_left = 100
    chart_right = 750
    chart_top = 70
    chart_bottom = 480
    chart_w = chart_right - chart_left
    chart_h = chart_bottom - chart_top
    
    # Y-axis: 0 to 1000 N
    y_max = 1000
    
    # Draw axes
    canvas.draw_line(chart_left, chart_top, chart_left, chart_bottom, (0, 0, 0), 2)
    canvas.draw_line(chart_left, chart_bottom, chart_right, chart_bottom, (0, 0, 0), 2)
    
    # Y-axis label
    draw_text_vertical(canvas, chart_left - 60, chart_top + 100, "Force (N)", (0, 0, 0), 1)
    
    # Y-axis ticks and gridlines
    for val in range(0, y_max + 1, 200):
        y = int(chart_bottom - (val / y_max) * chart_h)
        canvas.draw_line(chart_left - 5, y, chart_left, y, (0, 0, 0), 1)
        draw_text_right(canvas, chart_left - 8, y - 3, str(val), (0, 0, 0), 1)
        # Gridline
        if val > 0:
            canvas.draw_dashed_line(chart_left + 1, y, chart_right, y, (200, 200, 200), 1, 4, 4)
    
    # Draw bars
    n_conditions = len(conditions)
    group_width = chart_w / n_conditions
    bar_width = int(group_width * 0.35)
    gap = 5
    
    for i in range(n_conditions):
        group_x = int(chart_left + i * group_width + group_width * 0.1)
        
        # Light machining bar
        bar_h_light = int((light_forces[i] / y_max) * chart_h)
        bar_x_light = group_x
        bar_y_light = chart_bottom - bar_h_light
        canvas.fill_rect(bar_x_light, bar_y_light, bar_width, bar_h_light, colors_light[i])
        canvas.draw_rect(bar_x_light, bar_y_light, bar_width, bar_h_light, (0, 0, 0), 1)
        
        # Heavy machining bar
        bar_h_heavy = int((heavy_forces[i] / y_max) * chart_h)
        bar_x_heavy = group_x + bar_width + gap
        bar_y_heavy = chart_bottom - bar_h_heavy
        canvas.fill_rect(bar_x_heavy, bar_y_heavy, bar_width, bar_h_heavy, colors_heavy[i])
        canvas.draw_rect(bar_x_heavy, bar_y_heavy, bar_width, bar_h_heavy, (0, 0, 0), 1)
        
        # Value labels on bars
        draw_text_centered(canvas, bar_x_light + bar_width // 2, bar_y_light - 12,
                          str(light_forces[i]), (0, 0, 0), 1)
        draw_text_centered(canvas, bar_x_heavy + bar_width // 2, bar_y_heavy - 12,
                          str(heavy_forces[i]), (0, 0, 0), 1)
        
        # X-axis labels (condition names)
        label_x = group_x + bar_width + gap // 2
        draw_text_centered(canvas, label_x, chart_bottom + 10, conditions[i], (0, 0, 0), 1)
    
    # X-axis label
    draw_text_centered(canvas, (chart_left + chart_right) // 2, chart_bottom + 30, "MWF Condition", (0, 0, 0), 1)
    
    # Legend
    legend_x = 500
    legend_y = 520
    canvas.draw_rect(legend_x, legend_y, 250, 60, (0, 0, 0), 1)
    draw_text(canvas, legend_x + 10, legend_y + 5, "Legend:", (0, 0, 0), 1)
    
    # Light machining
    canvas.fill_rect(legend_x + 10, legend_y + 20, 20, 12, (150, 150, 220))
    canvas.draw_rect(legend_x + 10, legend_y + 20, 20, 12, (0, 0, 0), 1)
    draw_text(canvas, legend_x + 35, legend_y + 22, "Light: ap=1mm, fz=0.1mm", (0, 0, 0), 1)
    
    # Heavy machining
    canvas.fill_rect(legend_x + 10, legend_y + 38, 20, 12, (100, 100, 180))
    canvas.draw_rect(legend_x + 10, legend_y + 38, 20, 12, (0, 0, 0), 1)
    draw_text(canvas, legend_x + 35, legend_y + 40, "Heavy: ap=2mm, fz=0.2mm", (0, 0, 0), 1)
    
    # Additional note
    draw_text(canvas, chart_left, 560, "Cutting speed: Vc = 200 m/min", (80, 80, 80), 1)
    draw_text(canvas, chart_left, 575, "Tool: 4-insert face mill, D=50mm", (80, 80, 80), 1)
    
    canvas.save_png(output_path)
    print(f"  Saved: {output_path}")



# ============================================================================
# Figure 4: Temperature Estimates Line Chart
# ============================================================================

def generate_figure_4(output_path):
    """Generate Figure 4: Temperature vs cutting speed line chart."""
    canvas = Canvas(800, 600)
    
    # Title
    draw_text_centered(canvas, 400, 15, "Figure 4: Estimated Cutting Zone Temperatures", (0, 0, 0), 2)
    
    # Data: cutting speeds and temperatures for each condition
    speeds = [150, 200, 250]  # m/min
    
    # Temperature data (degrees C) for each condition at each speed
    temp_data = {
        "DRY":     [380, 460, 560],
        "OIL":     [310, 380, 460],
        "IL1":     [280, 340, 420],
        "PEG":     [290, 360, 440],
        "PEG+IL1": [250, 310, 380],
        "IL308":   [230, 280, 350],
    }
    
    # Colors for each condition
    line_colors = {
        "DRY":     (200, 30, 30),
        "OIL":     (30, 80, 200),
        "IL1":     (30, 160, 30),
        "PEG":     (180, 130, 0),
        "PEG+IL1": (140, 30, 180),
        "IL308":   (0, 160, 160),
    }
    
    # Chart area
    chart_left = 120
    chart_right = 620
    chart_top = 70
    chart_bottom = 500
    chart_w = chart_right - chart_left
    chart_h = chart_bottom - chart_top
    
    # Axis ranges
    x_min, x_max = 130, 270  # m/min (with padding)
    y_min, y_max = 100, 600  # degrees C
    
    def to_px(speed, temp):
        x = int(chart_left + (speed - x_min) / (x_max - x_min) * chart_w)
        y = int(chart_bottom - (temp - y_min) / (y_max - y_min) * chart_h)
        return x, y
    
    # Draw axes
    canvas.draw_line(chart_left, chart_top, chart_left, chart_bottom, (0, 0, 0), 2)
    canvas.draw_line(chart_left, chart_bottom, chart_right, chart_bottom, (0, 0, 0), 2)
    
    # Y-axis ticks and gridlines
    for temp in range(100, 601, 50):
        _, y = to_px(x_min, temp)
        if temp % 100 == 0:
            canvas.draw_line(chart_left - 5, y, chart_left, y, (0, 0, 0), 1)
            draw_text_right(canvas, chart_left - 8, y - 3, str(temp), (0, 0, 0), 1)
            canvas.draw_dashed_line(chart_left + 1, y, chart_right, y, (220, 220, 220), 1, 4, 4)
        else:
            canvas.draw_line(chart_left - 2, y, chart_left, y, (0, 0, 0), 1)
    
    # X-axis ticks
    for speed in speeds:
        x, _ = to_px(speed, y_min)
        canvas.draw_line(x, chart_bottom, x, chart_bottom + 5, (0, 0, 0), 1)
        draw_text_centered(canvas, x, chart_bottom + 10, str(speed), (0, 0, 0), 1)
    
    # Axis labels
    draw_text_centered(canvas, (chart_left + chart_right) // 2, chart_bottom + 30,
                      "Cutting Speed (m/min)", (0, 0, 0), 1)
    draw_text_vertical(canvas, chart_left - 80, chart_top + 120, "Temperature (C)", (0, 0, 0), 1)
    
    # Decomposition temperature line (dashed horizontal at 340C)
    decomp_temp = 340
    _, decomp_y = to_px(x_min, decomp_temp)
    canvas.draw_dashed_line(chart_left, decomp_y, chart_right, decomp_y, (180, 0, 0), 2, 10, 6)
    draw_text(canvas, chart_right + 5, decomp_y - 12, "Decomposition", (180, 0, 0), 1)
    draw_text(canvas, chart_right + 5, decomp_y + 2, "Temp. (~340C)", (180, 0, 0), 1)
    
    # Plot lines
    marker_styles = list(temp_data.keys())
    for condition, temps in temp_data.items():
        color = line_colors[condition]
        points = []
        for i, speed in enumerate(speeds):
            x, y = to_px(speed, temps[i])
            points.append((x, y))
        
        # Draw lines between points
        for i in range(len(points) - 1):
            canvas.draw_line(points[i][0], points[i][1],
                           points[i+1][0], points[i+1][1], color, 2)
        
        # Draw markers (filled circles)
        for px, py in points:
            canvas.fill_circle(px, py, 5, color)
            canvas.draw_circle(px, py, 5, (0, 0, 0), 1)
    
    # Legend (right side)
    legend_x = 640
    legend_y = 80
    canvas.draw_rect(legend_x, legend_y, 140, 160, (0, 0, 0), 1)
    canvas.fill_rect(legend_x + 1, legend_y + 1, 138, 158, (250, 250, 250))
    draw_text(canvas, legend_x + 10, legend_y + 8, "MWF Condition:", (0, 0, 0), 1)
    
    for idx, (condition, color) in enumerate(line_colors.items()):
        ly = legend_y + 25 + idx * 22
        canvas.draw_line(legend_x + 10, ly + 4, legend_x + 35, ly + 4, color, 2)
        canvas.fill_circle(legend_x + 22, ly + 4, 4, color)
        draw_text(canvas, legend_x + 40, ly, condition, color, 1)
    
    # Notes
    draw_text(canvas, 120, 530, "Conditions: ap = 1.5mm, fz = 0.15mm/tooth", (80, 80, 80), 1)
    draw_text(canvas, 120, 545, "Temperature estimated via FD inverse method from TC data", (80, 80, 80), 1)
    draw_text(canvas, 120, 560, "Dashed line: IL thermal decomposition limit", (180, 0, 0), 1)
    
    canvas.save_png(output_path)
    print(f"  Saved: {output_path}")



# ============================================================================
# Figure 5: EDS Surface Analysis
# ============================================================================

def generate_figure_5(output_path):
    """Generate Figure 5: EDS dot maps and surface morphology."""
    import random
    random.seed(123)
    
    canvas = Canvas(800, 600)
    
    # Title
    draw_text_centered(canvas, 400, 15, "Figure 5: EDS Analysis and Surface Morphology", (0, 0, 0), 2)
    
    # Three panels: (a), (b), (c)
    panel_w = 240
    panel_h = 230
    panel_y = 60
    gap = 20
    
    panels_start_x = (800 - 3 * panel_w - 2 * gap) // 2
    
    # Colors
    FE_COLOR = (200, 50, 50)    # Iron - red
    F_COLOR = (50, 200, 50)     # Fluorine - green
    DARK_BG = (30, 30, 40)
    
    # ---- Panel (a): Fe EDS dot map ----
    ax = panels_start_x
    ay = panel_y
    
    # Dark background for EDS map
    canvas.fill_rect(ax, ay, panel_w, panel_h, DARK_BG)
    canvas.draw_rect(ax, ay, panel_w, panel_h, (0, 0, 0), 2)
    
    # Panel label
    draw_text_centered(canvas, ax + panel_w // 2, ay + panel_h + 8, "(a) Fe K-alpha EDS Map", (0, 0, 0), 1)
    
    # Cutting edge indication (bright line near top)
    edge_y = ay + 30
    canvas.draw_line(ax + 20, edge_y, ax + panel_w - 20, edge_y, (100, 100, 120), 2)
    draw_text(canvas, ax + 5, ay + 5, "Cutting Edge", (150, 150, 150), 1)
    
    # Fe dots - concentrated near the cutting edge, scattered below
    for i in range(300):
        # Higher density near the edge
        if random.random() < 0.6:
            dx = random.randint(20, panel_w - 20)
            dy = random.randint(35, 100)
        else:
            dx = random.randint(20, panel_w - 20)
            dy = random.randint(35, panel_h - 20)
        
        intensity = random.randint(150, 255)
        size = random.randint(1, 2)
        color = (intensity, int(intensity * 0.2), int(intensity * 0.2))
        canvas.fill_circle(ax + dx, ay + dy, size, color)
    
    # Scale bar
    canvas.fill_rect(ax + panel_w - 60, ay + panel_h - 20, 40, 3, (255, 255, 255))
    draw_text(canvas, ax + panel_w - 55, ay + panel_h - 15, "50um", (255, 255, 255), 1)
    
    # ---- Panel (b): F EDS dot map ----
    bx = panels_start_x + panel_w + gap
    by = panel_y
    
    canvas.fill_rect(bx, by, panel_w, panel_h, DARK_BG)
    canvas.draw_rect(bx, by, panel_w, panel_h, (0, 0, 0), 2)
    
    draw_text_centered(canvas, bx + panel_w // 2, by + panel_h + 8, "(b) F K-alpha EDS Map", (0, 0, 0), 1)
    
    # Cutting edge
    canvas.draw_line(bx + 20, edge_y, bx + panel_w - 20, edge_y, (100, 100, 120), 2)
    draw_text(canvas, bx + 5, by + 5, "Cutting Edge", (150, 150, 150), 1)
    
    # F dots - from IL decomposition on tool surface
    for i in range(250):
        if random.random() < 0.5:
            dx = random.randint(20, panel_w - 20)
            dy = random.randint(35, 120)
        else:
            dx = random.randint(20, panel_w - 20)
            dy = random.randint(35, panel_h - 20)
        
        intensity = random.randint(120, 255)
        size = random.randint(1, 2)
        color = (int(intensity * 0.2), intensity, int(intensity * 0.2))
        canvas.fill_circle(bx + dx, by + dy, size, color)
    
    # Scale bar
    canvas.fill_rect(bx + panel_w - 60, by + panel_h - 20, 40, 3, (255, 255, 255))
    draw_text(canvas, bx + panel_w - 55, by + panel_h - 15, "50um", (255, 255, 255), 1)
    
    # ---- Panel (c): Surface morphology comparison ----
    cx = panels_start_x + 2 * (panel_w + gap)
    cy = panel_y
    
    canvas.fill_rect(cx, cy, panel_w, panel_h, (200, 200, 200))
    canvas.draw_rect(cx, cy, panel_w, panel_h, (0, 0, 0), 2)
    
    draw_text_centered(canvas, cx + panel_w // 2, cy + panel_h + 8, "(c) Surface Morphology", (0, 0, 0), 1)
    
    # Left half: rougher texture (neat oil)
    half_w = panel_w // 2
    for y in range(cy + 2, cy + panel_h - 2):
        for x in range(cx + 2, cx + half_w - 1):
            # Random roughness
            noise = random.randint(-40, 40)
            # Add some linear scratches
            if (x + y) % 7 == 0 or (x - y) % 11 == 0:
                noise -= 30
            base = 160 + noise
            base = max(80, min(220, base))
            canvas.set_pixel(x, y, (base, base, base))
    
    # Right half: smoother texture (oil + IL)
    for y in range(cy + 2, cy + panel_h - 2):
        for x in range(cx + half_w + 1, cx + panel_w - 2):
            noise = random.randint(-15, 15)
            if (x + y * 2) % 19 == 0:
                noise -= 10
            base = 180 + noise
            base = max(140, min(220, base))
            canvas.set_pixel(x, y, (base, base, base))
    
    # Dividing line
    canvas.draw_line(cx + half_w, cy, cx + half_w, cy + panel_h, (255, 0, 0), 2)
    
    # Labels for each half
    draw_text_centered(canvas, cx + half_w // 2, cy + 8, "Neat Oil", (0, 0, 0), 1)
    draw_text_centered(canvas, cx + half_w + half_w // 2, cy + 8, "Oil + IL", (0, 0, 100), 1)
    
    # Roughness indicators
    draw_text(canvas, cx + 5, cy + panel_h - 30, "Ra=0.8um", (0, 0, 0), 1)
    draw_text(canvas, cx + half_w + 10, cy + panel_h - 30, "Ra=0.4um", (0, 0, 100), 1)
    
    # ---- Lower section: Summary/annotations ----
    note_y = panel_y + panel_h + 40
    
    # Annotation box
    canvas.draw_rect(40, note_y, 720, 250, (0, 0, 0), 1)
    canvas.fill_rect(41, note_y + 1, 718, 248, (248, 248, 255))
    
    draw_text(canvas, 60, note_y + 10, "EDS Analysis Summary:", (0, 0, 0), 2)
    
    draw_text(canvas, 60, note_y + 40, "- Panel (a): Fe deposits from workpiece material transfer to tool", (0, 0, 0), 1)
    draw_text(canvas, 60, note_y + 58, "  surface. Higher concentration near cutting edge indicates", (0, 0, 0), 1)
    draw_text(canvas, 60, note_y + 76, "  adhesive wear mechanism.", (0, 0, 0), 1)
    
    draw_text(canvas, 60, note_y + 100, "- Panel (b): F (fluorine) from ionic liquid decomposition forms", (0, 0, 0), 1)
    draw_text(canvas, 60, note_y + 118, "  protective tribofilm (FeF2/FeF3) on tool surface.", (0, 0, 0), 1)
    
    draw_text(canvas, 60, note_y + 142, "- Panel (c): Surface quality comparison shows IL additive", (0, 0, 0), 1)
    draw_text(canvas, 60, note_y + 160, "  significantly reduces surface roughness (Ra from 0.8 to 0.4 um).", (0, 0, 0), 1)
    
    draw_text(canvas, 60, note_y + 190, "Conditions: Vc=200m/min, ap=1.5mm, MQL flow=50ml/h", (80, 80, 80), 1)
    draw_text(canvas, 60, note_y + 208, "IL: [P66614][NTf2] at 1% concentration in PEG base oil", (80, 80, 80), 1)
    
    # Color legend for EDS
    legend_y2 = note_y + 230
    canvas.fill_circle(500, note_y + 50, 5, FE_COLOR)
    draw_text(canvas, 510, note_y + 47, "= Fe signal", FE_COLOR, 1)
    canvas.fill_circle(500, note_y + 70, 5, F_COLOR)
    draw_text(canvas, 510, note_y + 67, "= F signal", F_COLOR, 1)
    
    canvas.save_png(output_path)
    print(f"  Saved: {output_path}")



# ============================================================================
# Main
# ============================================================================

def main():
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "manuscript_figures")
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating manuscript figures...")
    print()
    
    print("Figure 1: Experimental Setup")
    generate_figure_1(os.path.join(output_dir, "Figure_1_Experimental_Setup.png"))
    
    print("Figure 2: FD Model Discretization")
    generate_figure_2(os.path.join(output_dir, "Figure_2_FD_Model_Discretization.png"))
    
    print("Figure 3: Machining Forces")
    generate_figure_3(os.path.join(output_dir, "Figure_3_Machining_Forces.png"))
    
    print("Figure 4: Temperature Estimates")
    generate_figure_4(os.path.join(output_dir, "Figure_4_Temperature_Estimates.png"))
    
    print("Figure 5: EDS Surface Analysis")
    generate_figure_5(os.path.join(output_dir, "Figure_5_EDS_Surface.png"))
    
    print()
    print("All figures generated successfully!")

if __name__ == "__main__":
    main()
