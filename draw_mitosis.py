#!/usr/bin/env python3
"""
Draw a hand-drawn style labeled diagram of mitosis stages.
Uses pure Python to generate a PNG file without external dependencies.
Optimized for speed using bytearray for pixel buffer.
"""

import struct
import zlib
import math
import random

# Image dimensions
WIDTH = 1200
HEIGHT = 850

# Create pixel buffer as flat bytearray (much faster than list of tuples)
# 3 bytes per pixel (RGB)
buf = bytearray(b'\xff' * (WIDTH * HEIGHT * 3))

def set_pixel(x, y, r, g, b):
    """Set a pixel with bounds checking."""
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        idx = (y * WIDTH + x) * 3
        buf[idx] = r
        buf[idx+1] = g
        buf[idx+2] = b

def draw_line(x0, y0, x1, y1, r, g, b, thickness=2):
    """Draw a line with thickness."""
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy), 1)
    x_inc = dx / steps
    y_inc = dy / steps
    
    t = thickness // 2
    for i in range(steps + 1):
        cx = int(x0 + i * x_inc)
        cy = int(y0 + i * y_inc)
        for tx in range(-t, t + 1):
            for ty in range(-t, t + 1):
                set_pixel(cx + tx, cy + ty, r, g, b)

def draw_circle(cx, cy, radius, r, g, b, thickness=2):
    """Draw circle outline."""
    num_points = max(40, int(radius * 2))
    random.seed(hash((cx, cy, radius)))
    prev_x = cx + radius
    prev_y = cy
    for i in range(1, num_points + 1):
        angle = 2 * math.pi * i / num_points
        wobble = random.uniform(-1.5, 1.5)
        nx = int(cx + (radius + wobble) * math.cos(angle))
        ny = int(cy + (radius + wobble) * math.sin(angle))
        draw_line(prev_x, prev_y, nx, ny, r, g, b, thickness)
        prev_x, prev_y = nx, ny

def draw_ellipse(cx, cy, rx, ry, r, g, b, thickness=2):
    """Draw ellipse outline with hand-drawn wobble."""
    num_points = max(40, int((rx + ry)))
    random.seed(hash((cx, cy, rx, ry)))
    prev_x = int(cx + rx)
    prev_y = cy
    for i in range(1, num_points + 1):
        angle = 2 * math.pi * i / num_points
        wobble = random.uniform(-1.2, 1.2)
        nx = int(cx + (rx + wobble) * math.cos(angle))
        ny = int(cy + (ry + wobble) * math.sin(angle))
        draw_line(prev_x, prev_y, nx, ny, r, g, b, thickness)
        prev_x, prev_y = nx, ny

def fill_ellipse(cx, cy, rx, ry, r, g, b):
    """Fill an ellipse."""
    for y in range(max(0, cy - ry), min(HEIGHT, cy + ry + 1)):
        dy = y - cy
        if abs(dy) <= ry:
            half_w = int(rx * math.sqrt(1 - (dy/ry)**2))
            for x in range(max(0, cx - half_w), min(WIDTH, cx + half_w + 1)):
                idx = (y * WIDTH + x) * 3
                buf[idx] = r
                buf[idx+1] = g
                buf[idx+2] = b

def fill_circle(cx, cy, radius, r, g, b):
    """Fill a circle."""
    fill_ellipse(cx, cy, radius, radius, r, g, b)

def draw_arrow(x0, y0, x1, y1, r, g, b, thickness=2):
    """Draw an arrow."""
    draw_line(x0, y0, x1, y1, r, g, b, thickness)
    angle = math.atan2(y1 - y0, x1 - x0)
    al = 10
    for da in [2.5, -2.5]:
        ax = int(x1 - al * math.cos(angle + da * 0.3))
        ay = int(y1 - al * math.sin(angle + da * 0.3))
        draw_line(x1, y1, ax, ay, r, g, b, thickness)

# Bitmap font 5x7
FONT = {
    'A': ["01110","10001","10001","11111","10001","10001","10001"],
    'B': ["11110","10001","10001","11110","10001","10001","11110"],
    'C': ["01110","10001","10000","10000","10000","10001","01110"],
    'D': ["11100","10010","10001","10001","10001","10010","11100"],
    'E': ["11111","10000","10000","11110","10000","10000","11111"],
    'F': ["11111","10000","10000","11110","10000","10000","10000"],
    'G': ["01110","10001","10000","10111","10001","10001","01110"],
    'H': ["10001","10001","10001","11111","10001","10001","10001"],
    'I': ["01110","00100","00100","00100","00100","00100","01110"],
    'J': ["00111","00010","00010","00010","00010","10010","01100"],
    'K': ["10001","10010","10100","11000","10100","10010","10001"],
    'L': ["10000","10000","10000","10000","10000","10000","11111"],
    'M': ["10001","11011","10101","10101","10001","10001","10001"],
    'N': ["10001","11001","10101","10011","10001","10001","10001"],
    'O': ["01110","10001","10001","10001","10001","10001","01110"],
    'P': ["11110","10001","10001","11110","10000","10000","10000"],
    'Q': ["01110","10001","10001","10001","10101","10010","01101"],
    'R': ["11110","10001","10001","11110","10100","10010","10001"],
    'S': ["01111","10000","10000","01110","00001","00001","11110"],
    'T': ["11111","00100","00100","00100","00100","00100","00100"],
    'U': ["10001","10001","10001","10001","10001","10001","01110"],
    'V': ["10001","10001","10001","10001","01010","01010","00100"],
    'W': ["10001","10001","10001","10101","10101","10101","01010"],
    'X': ["10001","10001","01010","00100","01010","10001","10001"],
    'Y': ["10001","10001","01010","00100","00100","00100","00100"],
    'Z': ["11111","00001","00010","00100","01000","10000","11111"],
    ' ': ["00000","00000","00000","00000","00000","00000","00000"],
    '0': ["01110","10001","10011","10101","11001","10001","01110"],
    '1': ["00100","01100","00100","00100","00100","00100","01110"],
    '2': ["01110","10001","00001","00110","01000","10000","11111"],
    '-': ["00000","00000","00000","11111","00000","00000","00000"],
    '.': ["00000","00000","00000","00000","00000","00000","00100"],
    ',': ["00000","00000","00000","00000","00000","00100","01000"],
    ':': ["00000","00100","00100","00000","00100","00100","00000"],
    '(': ["00010","00100","01000","01000","01000","00100","00010"],
    ')': ["01000","00100","00010","00010","00010","00100","01000"],
    '/': ["00001","00010","00010","00100","01000","01000","10000"],
}

def draw_text(x, y, text, r, g, b, scale=2):
    """Draw text."""
    cursor_x = x
    for char in text.upper():
        if char in FONT:
            bitmap = FONT[char]
            for row_idx, row in enumerate(bitmap):
                for col_idx in range(5):
                    if row[col_idx] == '1':
                        for sx in range(scale):
                            for sy in range(scale):
                                set_pixel(cursor_x + col_idx*scale + sx,
                                         y + row_idx*scale + sy, r, g, b)
            cursor_x += 6 * scale
        else:
            cursor_x += 6 * scale

def draw_dashed_circle(cx, cy, radius, r, g, b):
    """Draw dashed circle for nuclear envelope."""
    for i in range(0, 30, 2):
        a1 = 2 * math.pi * i / 30
        a2 = 2 * math.pi * (i + 1) / 30
        x1 = int(cx + radius * math.cos(a1))
        y1 = int(cy + radius * math.sin(a1))
        x2 = int(cx + radius * math.cos(a2))
        y2 = int(cy + radius * math.sin(a2))
        draw_line(x1, y1, x2, y2, r, g, b, 1)

# ============ COLORS ============
BLACK = (0, 0, 0)
PURPLE = (100, 20, 120)
GREEN = (0, 130, 0)
BLUE = (0, 0, 150)
RED = (180, 0, 0)
BROWN = (150, 80, 0)
GRAY = (80, 80, 80)
LIGHT_BLUE = (230, 240, 255)
DARK_RED = (150, 0, 0)

# ============ DRAW ============

# Title
draw_text(320, 15, "STAGES OF MITOSIS", 0, 0, 100, 3)
# Subtitle (hand-drawn style note)
draw_text(420, 50, "- HAND DRAWN DIAGRAM -", *GRAY, 2)

# Stage positions (5 stages)
stages = [
    (120, 220, "INTERPHASE"),
    (360, 220, "PROPHASE"),
    (600, 220, "METAPHASE"),
    (840, 220, "ANAPHASE"),
    (1080, 220, "TELOPHASE"),
]

cell_r = 70

for i, (cx, cy, name) in enumerate(stages):
    # Label
    text_w = len(name) * 12
    draw_text(cx - text_w//2, cy - 120, name, *BLACK, 2)
    # Stage number
    num_str = str(i+1) + "."
    draw_text(cx - text_w//2 - 20, cy - 120, num_str, *RED, 2)
    
    # Cell body
    fill_ellipse(cx, cy, cell_r, cell_r + 10, *LIGHT_BLUE)
    draw_ellipse(cx, cy, cell_r, cell_r + 10, *BLACK, 2)
    
    if name == "INTERPHASE":
        # Nuclear envelope
        draw_dashed_circle(cx, cy, 40, *BLUE)
        # Chromatin threads (loose)
        random.seed(11)
        for _ in range(6):
            sx = cx + random.randint(-25, 25)
            sy = cy + random.randint(-25, 25)
            for _ in range(2):
                ex = sx + random.randint(-12, 12)
                ey = sy + random.randint(-12, 12)
                draw_line(sx, sy, ex, ey, *PURPLE, 1)
                sx, sy = ex, ey
        # Nucleolus
        fill_circle(cx + 10, cy + 5, 7, 50, 50, 80)
        # Centriole pair
        draw_line(cx+50, cy-30, cx+50, cy-20, *BROWN, 2)
        draw_line(cx+54, cy-30, cx+54, cy-20, *BROWN, 2)
        # Labels below
        draw_text(cx-55, cy+90, "CHROMATIN", *PURPLE, 1)
        draw_text(cx-55, cy+100, "NUCLEOLUS", 50, 50, 80, 1)
        draw_text(cx-55, cy+110, "NUCLEAR ENV.", *BLUE, 1)
        
    elif name == "PROPHASE":
        # Condensed chromosomes (X shapes)
        positions = [(-20,-15),(10,-10),(-10,10),(15,15),(0,-28)]
        for dx, dy in positions:
            x, y = cx+dx, cy+dy
            draw_line(x-4, y-5, x+4, y+5, *PURPLE, 2)
            draw_line(x+4, y-5, x-4, y+5, *PURPLE, 2)
        # Centrioles moving apart
        draw_line(cx-50, cy-40, cx-50, cy-30, *BROWN, 2)
        draw_line(cx-46, cy-40, cx-46, cy-30, *BROWN, 2)
        draw_line(cx+50, cy-40, cx+50, cy-30, *BROWN, 2)
        draw_line(cx+54, cy-40, cx+54, cy-30, *BROWN, 2)
        # Early spindle
        for off in range(-2, 3):
            draw_line(cx-45, cy-35, cx+off*8, cy, *GREEN, 1)
            draw_line(cx+50, cy-35, cx+off*8, cy, *GREEN, 1)
        # Labels
        draw_text(cx-60, cy+90, "CHROMOSOMES", *PURPLE, 1)
        draw_text(cx-60, cy+100, "CONDENSE", *PURPLE, 1)
        draw_text(cx-60, cy+110, "SPINDLE FORMS", *GREEN, 1)
        
    elif name == "METAPHASE":
        # Spindle fibers full
        for off in range(-3, 4):
            draw_line(cx, cy-65, cx+off*9, cy, *GREEN, 1)
            draw_line(cx, cy+65, cx+off*9, cy, *GREEN, 1)
        # Chromosomes aligned at center
        for off in range(-3, 4):
            x = cx + off * 9
            draw_line(x-3, cy-5, x+3, cy+5, *PURPLE, 2)
            draw_line(x+3, cy-5, x-3, cy+5, *PURPLE, 2)
        # Metaphase plate indicator
        draw_line(cx-45, cy, cx-35, cy, *RED, 1)
        draw_line(cx+35, cy, cx+45, cy, *RED, 1)
        # Labels
        draw_text(cx-65, cy+90, "METAPHASE PLATE", *RED, 1)
        draw_text(cx-65, cy+100, "CHROMOSOMES", *PURPLE, 1)
        draw_text(cx-65, cy+110, "ALIGNED", *PURPLE, 1)
        
    elif name == "ANAPHASE":
        # Cell slightly elongated
        # Spindle fibers
        for off in range(-2, 3):
            draw_line(cx+off*10, cy-40, cx+off*10, cy+40, *GREEN, 1)
        # Chromosomes moving to poles
        for off in range(-2, 3):
            x = cx + off * 10
            # Top set
            draw_line(x-2, cy-35, x+2, cy-25, *PURPLE, 2)
            # Bottom set
            draw_line(x-2, cy+25, x+2, cy+35, *PURPLE, 2)
        # Arrows showing movement
        draw_arrow(cx-25, cy-15, cx-25, cy-30, *RED, 1)
        draw_arrow(cx+25, cy+15, cx+25, cy+30, *RED, 1)
        # Labels
        draw_text(cx-65, cy+90, "SISTER", *PURPLE, 1)
        draw_text(cx-65, cy+100, "CHROMATIDS", *PURPLE, 1)
        draw_text(cx-65, cy+110, "MOVE TO POLES", *RED, 1)
        
    elif name == "TELOPHASE":
        # Two forming cells (cleavage furrow)
        # Upper cell
        fill_ellipse(cx, cy-25, 50, 35, *LIGHT_BLUE)
        draw_ellipse(cx, cy-25, 50, 35, *BLACK, 2)
        # Lower cell
        fill_ellipse(cx, cy+25, 50, 35, *LIGHT_BLUE)
        draw_ellipse(cx, cy+25, 50, 35, *BLACK, 2)
        # Cleavage furrow indicators
        draw_line(cx-55, cy, cx-40, cy, *RED, 2)
        draw_line(cx+40, cy, cx+55, cy, *RED, 2)
        # Nuclear envelopes reforming
        draw_dashed_circle(cx, cy-25, 22, *BLUE)
        draw_dashed_circle(cx, cy+25, 22, *BLUE)
        # Decondensing chromatin
        random.seed(77)
        for _ in range(3):
            sx = cx + random.randint(-10, 10)
            sy = cy - 25 + random.randint(-10, 10)
            ex = sx + random.randint(-6, 6)
            ey = sy + random.randint(-6, 6)
            draw_line(sx, sy, ex, ey, *PURPLE, 1)
        random.seed(88)
        for _ in range(3):
            sx = cx + random.randint(-10, 10)
            sy = cy + 25 + random.randint(-10, 10)
            ex = sx + random.randint(-6, 6)
            ey = sy + random.randint(-6, 6)
            draw_line(sx, sy, ex, ey, *PURPLE, 1)
        # Labels
        draw_text(cx-65, cy+90, "CLEAVAGE", *RED, 1)
        draw_text(cx-65, cy+100, "FURROW", *RED, 1)
        draw_text(cx-65, cy+110, "NUCLEI REFORM", *BLUE, 1)

# Arrows between stages
for i in range(len(stages) - 1):
    x1 = stages[i][0] + cell_r + 15
    x2 = stages[i+1][0] - cell_r - 15
    y_mid = stages[i][1]
    draw_arrow(x1, y_mid, x2, y_mid, *GRAY, 2)

# Result: Two daughter cells
draw_text(380, 430, "RESULT: CYTOKINESIS", *BLACK, 2)
# Two cells
for dx in [-80, 80]:
    cx_d = 600 + dx
    cy_d = 510
    fill_ellipse(cx_d, cy_d, 40, 40, *LIGHT_BLUE)
    draw_ellipse(cx_d, cy_d, 40, 40, *BLACK, 2)
    draw_dashed_circle(cx_d, cy_d, 22, *BLUE)
    random.seed(hash(dx)+1)
    for _ in range(3):
        sx = cx_d + random.randint(-10, 10)
        sy = cy_d + random.randint(-10, 10)
        ex = sx + random.randint(-5, 5)
        ey = sy + random.randint(-5, 5)
        draw_line(sx, sy, ex, ey, *PURPLE, 1)

draw_text(420, 570, "2 IDENTICAL DAUGHTER CELLS", *BLACK, 2)

# Arrow from telophase down to result
draw_arrow(1080, 310, 700, 470, *GRAY, 2)

# ============ SIGNIFICANCE BOX ============
box_y = 620
draw_line(80, box_y, 1120, box_y, *BLACK, 2)
draw_line(80, box_y, 80, box_y + 130, *BLACK, 2)
draw_line(1120, box_y, 1120, box_y + 130, *BLACK, 2)
draw_line(80, box_y + 130, 1120, box_y + 130, *BLACK, 2)

draw_text(100, box_y + 15, "SIGNIFICANCE OF MITOSIS:", *DARK_RED, 2)
draw_text(100, box_y + 45, "MITOSIS IS ESSENTIAL FOR GROWTH, REPAIR,", *BLACK, 2)
draw_text(100, box_y + 65, "AND MAINTENANCE OF TISSUES IN LIVING", *BLACK, 2)
draw_text(100, box_y + 85, "ORGANISMS. IT PRODUCES TWO GENETICALLY", *BLACK, 2)
draw_text(100, box_y + 105, "IDENTICAL DAUGHTER CELLS WITH THE SAME", *BLACK, 2)
draw_text(100, box_y + 125, "CHROMOSOME NUMBER AS THE PARENT CELL.", *BLACK, 2)

# Key/Legend
draw_text(100, 790, "KEY:", *BLACK, 2)
draw_line(160, 797, 185, 797, *PURPLE, 2)
draw_text(195, 790, "CHROMOSOMES", *PURPLE, 1)
draw_line(330, 797, 355, 797, *GREEN, 2)
draw_text(365, 790, "SPINDLE FIBERS", *GREEN, 1)
draw_line(510, 797, 535, 797, *BLUE, 2)
draw_text(545, 790, "NUCLEAR ENVELOPE", *BLUE, 1)
draw_line(720, 797, 745, 797, *RED, 2)
draw_text(755, 790, "CLEAVAGE FURROW", *RED, 1)

# ============ SAVE AS PNG ============
def create_png(filename, width, height, pixel_buf):
    """Create PNG from bytearray buffer."""
    def write_chunk(chunk_type, data):
        chunk = chunk_type + data
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', zlib.crc32(chunk) & 0xffffffff)
    
    signature = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = write_chunk(b'IHDR', ihdr_data)
    
    # Build raw data with filter bytes
    raw_data = bytearray()
    row_size = width * 3
    for y in range(height):
        raw_data.append(0)  # Filter: None
        start = y * row_size
        raw_data.extend(pixel_buf[start:start + row_size])
    
    compressed = zlib.compress(bytes(raw_data), 6)
    idat = write_chunk(b'IDAT', compressed)
    iend = write_chunk(b'IEND', b'')
    
    with open(filename, 'wb') as f:
        f.write(signature + ihdr + idat + iend)

output_file = '/projects/sandbox/AMMAN/Mitosis_Diagram_Handdrawn.png'
print("Generating PNG...")
create_png(output_file, WIDTH, HEIGHT, buf)
print(f"Done! Saved to: {output_file}")
