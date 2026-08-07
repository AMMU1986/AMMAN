#!/usr/bin/env python3
"""
Generate SVG figures for: Design Thinking Across Core Business Functions
Then convert to PNG using pure Python bitmap rendering.
"""

import os
import struct
import zlib
import math

os.makedirs('dt_figures', exist_ok=True)


###############################################################################
# PNG Creation utilities
###############################################################################

def create_png(width, height, pixels, filename):
    """Create PNG from pixel array. pixels[y][x] = (r, g, b)"""
    def make_chunk(chunk_type, data):
        chunk = chunk_type + data
        crc = zlib.crc32(chunk) & 0xffffffff
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', crc)
    
    header = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    
    raw_data = bytearray()
    for row in pixels:
        raw_data += b'\x00'
        for r, g, b in row:
            raw_data += bytes([r, g, b])
    
    compressed = zlib.compress(bytes(raw_data), 9)
    
    with open(filename, 'wb') as f:
        f.write(header)
        f.write(make_chunk(b'IHDR', ihdr))
        f.write(make_chunk(b'IDAT', compressed))
        f.write(make_chunk(b'IEND', b''))


def new_canvas(width, height, bg=(255, 255, 255)):
    """Create blank canvas"""
    return [[bg for _ in range(width)] for _ in range(height)]


def draw_filled_circle(pixels, cx, cy, r, color, width, height):
    """Draw a filled circle"""
    for y in range(max(0, cy - r), min(height, cy + r + 1)):
        for x in range(max(0, cx - r), min(width, cx + r + 1)):
            if (x - cx)**2 + (y - cy)**2 <= r**2:
                pixels[y][x] = color


def draw_circle_outline(pixels, cx, cy, r, color, thickness, width, height):
    """Draw a circle outline"""
    for y in range(max(0, cy - r - thickness), min(height, cy + r + thickness + 1)):
        for x in range(max(0, cx - r - thickness), min(width, cx + r + thickness + 1)):
            dist_sq = (x - cx)**2 + (y - cy)**2
            if (r - thickness)**2 <= dist_sq <= (r + thickness)**2:
                pixels[y][x] = color


def draw_rect(pixels, x1, y1, x2, y2, color, width, height):
    """Draw filled rectangle"""
    for y in range(max(0, y1), min(height, y2)):
        for x in range(max(0, x1), min(width, x2)):
            pixels[y][x] = color


def draw_rounded_rect(pixels, x1, y1, x2, y2, radius, fill_color, border_color, width, height):
    """Draw rounded rectangle with fill and border"""
    # Fill
    for y in range(max(0, y1), min(height, y2)):
        for x in range(max(0, x1), min(width, x2)):
            # Check corners
            in_rect = True
            if x < x1 + radius and y < y1 + radius:
                if (x - (x1 + radius))**2 + (y - (y1 + radius))**2 > radius**2:
                    in_rect = False
            elif x > x2 - radius and y < y1 + radius:
                if (x - (x2 - radius))**2 + (y - (y1 + radius))**2 > radius**2:
                    in_rect = False
            elif x < x1 + radius and y > y2 - radius:
                if (x - (x1 + radius))**2 + (y - (y2 - radius))**2 > radius**2:
                    in_rect = False
            elif x > x2 - radius and y > y2 - radius:
                if (x - (x2 - radius))**2 + (y - (y2 - radius))**2 > radius**2:
                    in_rect = False
            if in_rect:
                pixels[y][x] = fill_color


def draw_line(pixels, x1, y1, x2, y2, color, thickness, width, height):
    """Draw a line with given thickness"""
    dx = x2 - x1
    dy = y2 - y1
    length = max(1, int(math.sqrt(dx*dx + dy*dy)))
    for i in range(length + 1):
        t = i / length
        cx = int(x1 + t * dx)
        cy = int(y1 + t * dy)
        for ty in range(-thickness, thickness + 1):
            for tx in range(-thickness, thickness + 1):
                px, py = cx + tx, cy + ty
                if 0 <= px < width and 0 <= py < height:
                    if tx*tx + ty*ty <= thickness*thickness:
                        pixels[py][px] = color


def draw_arrow(pixels, x1, y1, x2, y2, color, thickness, width, height):
    """Draw an arrow from (x1,y1) to (x2,y2)"""
    draw_line(pixels, x1, y1, x2, y2, color, thickness, width, height)
    # Arrowhead
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 12
    a1 = angle + math.pi * 0.8
    a2 = angle - math.pi * 0.8
    ax1 = int(x2 + arrow_len * math.cos(a1))
    ay1 = int(y2 + arrow_len * math.sin(a1))
    ax2 = int(x2 + arrow_len * math.cos(a2))
    ay2 = int(y2 + arrow_len * math.sin(a2))
    draw_line(pixels, x2, y2, ax1, ay1, color, thickness, width, height)
    draw_line(pixels, x2, y2, ax2, ay2, color, thickness, width, height)


def blend_color(bg, fg, alpha):
    """Blend foreground onto background with alpha (0.0-1.0)"""
    return (
        int(bg[0] * (1 - alpha) + fg[0] * alpha),
        int(bg[1] * (1 - alpha) + fg[1] * alpha),
        int(bg[2] * (1 - alpha) + fg[2] * alpha),
    )


def lighten(color, factor=0.7):
    """Create lighter version of color"""
    return (
        min(255, int(color[0] + (255 - color[0]) * factor)),
        min(255, int(color[1] + (255 - color[1]) * factor)),
        min(255, int(color[2] + (255 - color[2]) * factor)),
    )


###############################################################################
# Simple bitmap font (5x7 pixel characters)
###############################################################################

FONT_5X7 = {
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
    '2': ["01110","10001","00001","00010","00100","01000","11111"],
    '3': ["11111","00010","00100","00010","00001","10001","01110"],
    '4': ["00010","00110","01010","10010","11111","00010","00010"],
    '5': ["11111","10000","11110","00001","00001","10001","01110"],
    '6': ["00110","01000","10000","11110","10001","10001","01110"],
    '7': ["11111","00001","00010","00100","01000","01000","01000"],
    '8': ["01110","10001","10001","01110","10001","10001","01110"],
    '9': ["01110","10001","10001","01111","00001","00010","01100"],
    '-': ["00000","00000","00000","11111","00000","00000","00000"],
    '.': ["00000","00000","00000","00000","00000","01100","01100"],
    ',': ["00000","00000","00000","00000","00000","00100","01000"],
    ':': ["00000","01100","01100","00000","01100","01100","00000"],
    '/': ["00001","00010","00010","00100","01000","01000","10000"],
    '(': ["00010","00100","01000","01000","01000","00100","00010"],
    ')': ["01000","00100","00010","00010","00010","00100","01000"],
    '&': ["01100","10010","10100","01000","10101","10010","01101"],
    '+': ["00000","00100","00100","11111","00100","00100","00000"],
    '=': ["00000","00000","11111","00000","11111","00000","00000"],
    '>': ["01000","00100","00010","00001","00010","00100","01000"],
    '<': ["00010","00100","01000","10000","01000","00100","00010"],
}


def draw_text(pixels, text, x, y, color, scale, width, height):
    """Draw text at position (x,y) with given scale. Returns text width."""
    cursor_x = x
    for ch in text.upper():
        glyph = FONT_5X7.get(ch)
        if glyph is None:
            cursor_x += 4 * scale
            continue
        for row_idx, row in enumerate(glyph):
            for col_idx, bit in enumerate(row):
                if bit == '1':
                    px = cursor_x + col_idx * scale
                    py = y + row_idx * scale
                    for sy in range(scale):
                        for sx in range(scale):
                            fx, fy = px + sx, py + sy
                            if 0 <= fx < width and 0 <= fy < height:
                                pixels[fy][fx] = color
        cursor_x += 6 * scale
    return cursor_x - x


def draw_text_centered(pixels, text, cx, cy, color, scale, width, height):
    """Draw text centered at (cx, cy)"""
    text_width = len(text) * 6 * scale
    text_height = 7 * scale
    x = cx - text_width // 2
    y = cy - text_height // 2
    draw_text(pixels, text, x, y, color, scale, width, height)


def draw_multiline_centered(pixels, lines, cx, cy, color, scale, width, height, line_spacing=2):
    """Draw multiple lines of text centered"""
    total_height = len(lines) * (7 * scale + line_spacing) - line_spacing
    start_y = cy - total_height // 2
    for i, line in enumerate(lines):
        line_y = start_y + i * (7 * scale + line_spacing)
        draw_text_centered(pixels, line, cx, line_y, color, scale, width, height)


###############################################################################
# Color definitions
###############################################################################

PRIMARY = (44, 62, 80)
SECONDARY = (52, 152, 219)
ACCENT1 = (231, 76, 60)      # Red
ACCENT2 = (39, 174, 96)      # Green
ACCENT3 = (243, 156, 18)     # Orange
ACCENT4 = (155, 89, 182)     # Purple
ACCENT5 = (26, 188, 156)     # Teal
DARK_TEXT = (44, 62, 80)
MID_GRAY = (127, 140, 141)
LIGHT_BG = (236, 240, 241)
WHITE = (255, 255, 255)


###############################################################################
# Figure 1: Design Thinking Process Model
###############################################################################

def generate_figure1():
    W, H = 1200, 600
    pixels = new_canvas(W, H, WHITE)
    
    # Title
    draw_text_centered(pixels, "THE DESIGN THINKING PROCESS MODEL", W//2, 30, PRIMARY, 3, W, H)
    draw_text_centered(pixels, "FIVE STAGES OF HUMAN-CENTERED INNOVATION", W//2, 62, MID_GRAY, 2, W, H)
    
    # Five stages as circles with labels
    stages = [
        ("EMPATHIZE", ACCENT1, "UNDERSTAND"),
        ("DEFINE", ACCENT3, "SYNTHESIZE"),
        ("IDEATE", SECONDARY, "GENERATE"),
        ("PROTOTYPE", ACCENT2, "BUILD"),
        ("TEST", ACCENT4, "VALIDATE"),
    ]
    
    stage_y = 260
    stage_radius = 70
    start_x = 130
    spacing = 240
    
    for i, (name, color, subtitle) in enumerate(stages):
        cx = start_x + i * spacing
        # Draw filled circle (light)
        draw_filled_circle(pixels, cx, stage_y, stage_radius, lighten(color, 0.75), W, H)
        # Draw circle outline
        draw_circle_outline(pixels, cx, stage_y, stage_radius, color, 3, W, H)
        # Stage name
        draw_text_centered(pixels, name, cx, stage_y - 12, color, 2, W, H)
        # Subtitle
        draw_text_centered(pixels, subtitle, cx, stage_y + 14, DARK_TEXT, 2, W, H)
        
        # Arrow to next stage
        if i < 4:
            arrow_x1 = cx + stage_radius + 10
            arrow_x2 = cx + spacing - stage_radius - 10
            draw_arrow(pixels, arrow_x1, stage_y, arrow_x2, stage_y, MID_GRAY, 2, W, H)
    
    # Iteration feedback arrow (bottom arc)
    # Draw a dashed line from TEST back to EMPATHIZE
    test_x = start_x + 4 * spacing
    emp_x = start_x
    arc_y = stage_y + 130
    # Left horizontal
    draw_line(pixels, emp_x, arc_y, test_x, arc_y, ACCENT1, 2, W, H)
    # Vertical connectors
    draw_line(pixels, test_x, stage_y + stage_radius + 5, test_x, arc_y, ACCENT1, 2, W, H)
    draw_arrow(pixels, emp_x, arc_y, emp_x, stage_y + stage_radius + 5, ACCENT1, 2, W, H)
    
    draw_text_centered(pixels, "ITERATIVE FEEDBACK LOOPS", W//2, arc_y + 25, ACCENT1, 2, W, H)
    
    # Core principles at bottom
    principles = [("HUMAN-CENTERED", ACCENT1), ("ITERATIVE", SECONDARY), 
                  ("COLLABORATIVE", ACCENT2), ("EXPERIMENTAL", ACCENT3), ("OPTIMISTIC", ACCENT4)]
    
    draw_text_centered(pixels, "CORE PRINCIPLES:", W//2, 490, PRIMARY, 2, W, H)
    
    princ_y = 525
    princ_spacing = 230
    princ_start = 140
    for i, (p, color) in enumerate(principles):
        px = princ_start + i * princ_spacing
        # Small colored box
        bw = len(p) * 6 * 2 + 16
        bx1 = px - bw // 2
        draw_rounded_rect(pixels, bx1, princ_y - 12, bx1 + bw, princ_y + 14, 5, lighten(color, 0.7), color, W, H)
        draw_text_centered(pixels, p, px, princ_y - 5, color, 2, W, H)
    
    create_png(W, H, pixels, 'dt_figures/Figure_1_Design_Thinking_Process.png')
    print("Figure 1 generated.")


###############################################################################
# Figure 2: Customer Experience Framework
###############################################################################

def generate_figure2():
    W, H = 1200, 700
    pixels = new_canvas(W, H, WHITE)
    
    # Title
    draw_text_centered(pixels, "DESIGN THINKING-ENABLED CUSTOMER EXPERIENCE FRAMEWORK", W//2, 30, PRIMARY, 2, W, H)
    draw_text_centered(pixels, "FROM EMPATHY TO INTEGRATED EXPERIENCE DELIVERY", W//2, 55, MID_GRAY, 2, W, H)
    
    # Central hub
    cx, cy = W//2, 320
    hub_r = 70
    draw_filled_circle(pixels, cx, cy, hub_r, lighten(SECONDARY, 0.8), W, H)
    draw_circle_outline(pixels, cx, cy, hub_r, SECONDARY, 3, W, H)
    draw_text_centered(pixels, "CUSTOMER", cx, cy - 10, SECONDARY, 2, W, H)
    draw_text_centered(pixels, "EXPERIENCE", cx, cy + 10, SECONDARY, 2, W, H)
    
    # Four surrounding functions
    functions = [
        ("MARKETING", "AND BRAND", 250, 150, ACCENT1),
        ("OPERATIONS", "AND DELIVERY", 950, 150, ACCENT2),
        ("TECHNOLOGY", "AND DIGITAL", 950, 490, ACCENT4),
        ("SERVICE", "AND SUPPORT", 250, 490, ACCENT3),
    ]
    
    for name, sub, fx, fy, color in functions:
        # Rounded rect
        bw, bh = 180, 70
        draw_rounded_rect(pixels, fx - bw//2, fy - bh//2, fx + bw//2, fy + bh//2, 
                         10, lighten(color, 0.75), color, W, H)
        draw_text_centered(pixels, name, fx, fy - 8, color, 2, W, H)
        draw_text_centered(pixels, sub, fx, fy + 12, DARK_TEXT, 2, W, H)
        
        # Draw connecting line to center
        dx = cx - fx
        dy = cy - fy
        dist = math.sqrt(dx*dx + dy*dy)
        # Start from edge of box, end at edge of circle
        start_frac = 100 / dist
        end_frac = 1 - hub_r / dist
        lx1 = int(fx + dx * start_frac)
        ly1 = int(fy + dy * start_frac)
        lx2 = int(fx + dx * end_frac)
        ly2 = int(fy + dy * end_frac)
        draw_line(pixels, lx1, ly1, lx2, ly2, color, 2, W, H)
    
    # Design thinking process steps at top
    dt_steps = ["EMPATHIZE", "DEFINE", "IDEATE", "PROTOTYPE", "TEST"]
    step_y = 90
    step_spacing = 220
    step_start = 160
    for i, step in enumerate(dt_steps):
        sx = step_start + i * step_spacing
        bw = len(step) * 6 * 2 + 16
        draw_rounded_rect(pixels, sx - bw//2, step_y - 12, sx + bw//2, step_y + 12,
                         5, PRIMARY, PRIMARY, W, H)
        draw_text_centered(pixels, step, sx, step_y - 5, WHITE, 2, W, H)
        # Arrow to next
        if i < 4:
            draw_arrow(pixels, sx + bw//2 + 5, step_y, sx + step_spacing - bw//2 - 5, step_y,
                      MID_GRAY, 1, W, H)
    
    # Customer journey stages at bottom
    draw_text_centered(pixels, "CUSTOMER JOURNEY STAGES", W//2, 600, PRIMARY, 2, W, H)
    journey = [("AWARENESS", ACCENT1), ("CONSIDERATION", ACCENT3), ("PURCHASE", SECONDARY),
               ("USAGE", ACCENT2), ("ADVOCACY", ACCENT4)]
    j_y = 640
    j_spacing = 220
    j_start = 160
    for i, (stage, color) in enumerate(journey):
        jx = j_start + i * j_spacing
        bw = len(stage) * 6 * 2 + 16
        draw_rounded_rect(pixels, jx - bw//2, j_y - 12, jx + bw//2, j_y + 12,
                         5, lighten(color, 0.7), color, W, H)
        draw_text_centered(pixels, stage, jx, j_y - 5, color, 2, W, H)
        if i < 4:
            draw_arrow(pixels, jx + bw//2 + 5, j_y, jx + j_spacing - bw//2 - 5, j_y,
                      MID_GRAY, 1, W, H)
    
    create_png(W, H, pixels, 'dt_figures/Figure_2_Customer_Experience_Framework.png')
    print("Figure 2 generated.")


###############################################################################
# Figure 3: Business Model Innovation Process
###############################################################################

def generate_figure3():
    W, H = 1200, 700
    pixels = new_canvas(W, H, WHITE)
    
    # Title
    draw_text_centered(pixels, "DESIGN THINKING-ENABLED BUSINESS MODEL INNOVATION PROCESS", W//2, 30, PRIMARY, 2, W, H)
    
    # Three main phases
    phases = [
        ("DISCOVER", 200, ACCENT1, ["CUSTOMER EMPATHY", "MARKET ANALYSIS", "PAIN POINTS"]),
        ("DESIGN", 600, SECONDARY, ["VALUE PROPOSITION", "REVENUE MODEL", "ECOSYSTEM DESIGN"]),
        ("DELIVER", 1000, ACCENT2, ["PILOT TESTING", "REFINEMENT", "SCALE-UP"]),
    ]
    
    phase_y = 250
    phase_w = 300
    phase_h = 300
    
    for name, px, color, items in phases:
        # Phase box
        x1 = px - phase_w // 2
        y1 = phase_y - 50
        x2 = px + phase_w // 2
        y2 = phase_y + phase_h - 50
        draw_rounded_rect(pixels, x1, y1, x2, y2, 12, lighten(color, 0.85), color, W, H)
        
        # Phase title
        draw_text_centered(pixels, name, px, phase_y - 20, color, 3, W, H)
        
        # Items
        for i, item in enumerate(items):
            iy = phase_y + 40 + i * 60
            iw = 250
            ix1 = px - iw // 2
            draw_rounded_rect(pixels, ix1, iy - 15, ix1 + iw, iy + 15, 5,
                            lighten(color, 0.6), color, W, H)
            draw_text_centered(pixels, item, px, iy - 5, DARK_TEXT, 2, W, H)
    
    # Arrows between phases
    draw_arrow(pixels, 350 + 10, phase_y + 80, 450 - 10, phase_y + 80, PRIMARY, 3, W, H)
    draw_arrow(pixels, 750 + 10, phase_y + 80, 850 - 10, phase_y + 80, PRIMARY, 3, W, H)
    
    # Feedback loop at bottom
    loop_y = phase_y + phase_h + 30
    draw_line(pixels, 200, loop_y, 1000, loop_y, ACCENT3, 2, W, H)
    draw_line(pixels, 1000, phase_y + phase_h - 55, 1000, loop_y, ACCENT3, 2, W, H)
    draw_arrow(pixels, 200, loop_y, 200, phase_y + phase_h - 55, ACCENT3, 2, W, H)
    draw_text_centered(pixels, "CONTINUOUS LEARNING AND ITERATION", W//2, loop_y + 25, ACCENT3, 2, W, H)
    
    # Three lenses at bottom
    draw_text_centered(pixels, "INNOVATION LENSES", W//2, 580, PRIMARY, 2, W, H)
    
    lenses = [
        ("DESIRABILITY", "HUMAN NEEDS", ACCENT1, 250),
        ("FEASIBILITY", "TECHNICAL", SECONDARY, 600),
        ("VIABILITY", "BUSINESS VALUE", ACCENT2, 950),
    ]
    
    lens_y = 635
    for name, sub, color, lx in lenses:
        r = 45
        draw_filled_circle(pixels, lx, lens_y, r, lighten(color, 0.7), W, H)
        draw_circle_outline(pixels, lx, lens_y, r, color, 2, W, H)
        draw_text_centered(pixels, name, lx, lens_y - 8, color, 2, W, H)
        draw_text_centered(pixels, sub, lx, lens_y + 12, DARK_TEXT, 1, W, H)
    
    create_png(W, H, pixels, 'dt_figures/Figure_3_Business_Model_Innovation.png')
    print("Figure 3 generated.")


###############################################################################
# Figure 4: Organizational Readiness Framework
###############################################################################

def generate_figure4():
    W, H = 1200, 700
    pixels = new_canvas(W, H, WHITE)
    
    # Title
    draw_text_centered(pixels, "ORGANIZATIONAL READINESS FRAMEWORK", W//2, 30, PRIMARY, 3, W, H)
    draw_text_centered(pixels, "FOR DESIGN THINKING IMPLEMENTATION", W//2, 60, MID_GRAY, 2, W, H)
    
    # Four quadrants
    quad_w = 520
    quad_h = 240
    gap = 30
    
    quads = [
        ("CULTURE AND MINDSET", 300, 210, ACCENT1,
         ["PSYCHOLOGICAL SAFETY", "TOLERANCE FOR AMBIGUITY", "OPENNESS TO EXPERIMENT", "CROSS-FUNCTIONAL COLLAB"]),
        ("STRUCTURE AND GOVERNANCE", 900, 210, SECONDARY,
         ["CROSS-FUNCTIONAL TEAMS", "AGILE DECISION-MAKING", "INNOVATION LABS", "DESIGN LEADERSHIP"]),
        ("CAPABILITIES AND SKILLS", 300, 500, ACCENT2,
         ["EMPATHETIC RESEARCH", "CREATIVE FACILITATION", "PROTOTYPING SKILLS", "SYSTEMS THINKING"]),
        ("RESOURCES AND INFRA", 900, 500, ACCENT3,
         ["DEDICATED BUDGETS", "PHYSICAL SPACES", "TOOLS AND PLATFORMS", "EXTERNAL PARTNERSHIPS"]),
    ]
    
    for title, qx, qy, color, items in quads:
        x1 = qx - quad_w // 2
        y1 = qy - quad_h // 2
        x2 = qx + quad_w // 2
        y2 = qy + quad_h // 2
        draw_rounded_rect(pixels, x1, y1, x2, y2, 12, lighten(color, 0.85), color, W, H)
        draw_text_centered(pixels, title, qx, y1 + 25, color, 2, W, H)
        
        for i, item in enumerate(items):
            iy = y1 + 55 + i * 40
            draw_text(pixels, "- " + item, x1 + 30, iy, DARK_TEXT, 2, W, H)
    
    # Central element
    center_r = 40
    draw_filled_circle(pixels, W//2, H//2 - 20, center_r, PRIMARY, W, H)
    draw_text_centered(pixels, "DT", W//2, H//2 - 28, WHITE, 2, W, H)
    draw_text_centered(pixels, "READY", W//2, H//2 - 12, WHITE, 2, W, H)
    
    # Connecting lines from center to quadrants
    for _, qx, qy, color, _ in quads:
        dx = qx - W//2
        dy = qy - (H//2 - 20)
        dist = math.sqrt(dx*dx + dy*dy)
        frac = center_r / dist
        lx1 = int(W//2 + dx * frac)
        ly1 = int(H//2 - 20 + dy * frac)
        end_frac = 1 - 120 / dist
        lx2 = int(W//2 + dx * end_frac)
        ly2 = int(H//2 - 20 + dy * end_frac)
        draw_line(pixels, lx1, ly1, lx2, ly2, color, 2, W, H)
    
    # Maturity levels at bottom
    draw_text_centered(pixels, "MATURITY LEVELS:", W//2, 645, PRIMARY, 2, W, H)
    levels = [("EMERGING", ACCENT1), ("DEVELOPING", ACCENT3), ("ESTABLISHED", SECONDARY), ("LEADING", ACCENT2)]
    lev_y = 675
    lev_spacing = 250
    lev_start = 225
    for i, (level, color) in enumerate(levels):
        lx = lev_start + i * lev_spacing
        bw = len(level) * 6 * 2 + 20
        draw_rounded_rect(pixels, lx - bw//2, lev_y - 12, lx + bw//2, lev_y + 12,
                         5, lighten(color, 0.5), color, W, H)
        draw_text_centered(pixels, level, lx, lev_y - 5, WHITE, 2, W, H)
    
    create_png(W, H, pixels, 'dt_figures/Figure_4_Organizational_Readiness.png')
    print("Figure 4 generated.")


###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    print("Generating figures for Design Thinking chapter...")
    generate_figure1()
    generate_figure2()
    generate_figure3()
    generate_figure4()
    print("\nAll figures generated in 'dt_figures/' directory.")
