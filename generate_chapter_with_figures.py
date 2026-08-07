#!/usr/bin/env python3
"""
Generate the complete book chapter .docx with embedded tables and figures.
"Accreditation as Accountability, Learning, and Institutional Renewal"

Creates 3 clear figures and 3 tables, one per section.
Uses only standard library modules.
"""

import zipfile
import os
import struct
import zlib
import math
import io
from xml.etree.ElementTree import Element, SubElement, tostring

# ============================================================
# FIGURE GENERATION - Pure Python PNG creation
# ============================================================

def create_png(width, height, pixels):
    """Create a PNG file from raw pixel data (list of rows, each row is list of (R,G,B) tuples)"""
    def make_chunk(chunk_type, data):
        chunk = chunk_type + data
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', zlib.crc32(chunk) & 0xffffffff)

    # PNG signature
    signature = b'\x89PNG\r\n\x1a\n'

    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    ihdr = make_chunk(b'IHDR', ihdr_data)

    # IDAT
    raw_data = b''
    for row in pixels:
        raw_data += b'\x00'  # filter byte
        for r, g, b in row:
            raw_data += struct.pack('BBB', r, g, b)
    compressed = zlib.compress(raw_data)
    idat = make_chunk(b'IDAT', compressed)

    # IEND
    iend = make_chunk(b'IEND', b'')

    return signature + ihdr + idat + iend


def draw_filled_rect(pixels, x1, y1, x2, y2, color):
    """Draw a filled rectangle"""
    for y in range(max(0, y1), min(len(pixels), y2)):
        for x in range(max(0, x1), min(len(pixels[0]), x2)):
            pixels[y][x] = color


def draw_rect_border(pixels, x1, y1, x2, y2, color, thickness=2):
    """Draw a rectangle border"""
    for t in range(thickness):
        for x in range(x1, x2):
            if y1 + t < len(pixels):
                pixels[y1 + t][x] = color
            if y2 - 1 - t >= 0 and y2 - 1 - t < len(pixels):
                pixels[y2 - 1 - t][x] = color
        for y in range(y1, y2):
            if x1 + t < len(pixels[0]):
                pixels[y][x1 + t] = color
            if x2 - 1 - t >= 0 and x2 - 1 - t < len(pixels[0]):
                pixels[y][x2 - 1 - t] = color


def draw_rounded_rect(pixels, x1, y1, x2, y2, fill_color, border_color, thickness=2):
    """Draw a rounded rectangle with fill and border"""
    draw_filled_rect(pixels, x1 + 4, y1, x2 - 4, y2, fill_color)
    draw_filled_rect(pixels, x1, y1 + 4, x2, y2 - 4, fill_color)
    draw_filled_rect(pixels, x1 + 2, y1 + 1, x2 - 2, y2 - 1, fill_color)
    draw_filled_rect(pixels, x1 + 1, y1 + 2, x2 - 1, y2 - 2, fill_color)
    draw_rect_border(pixels, x1 + 4, y1, x2 - 4, y2, border_color, thickness)
    draw_rect_border(pixels, x1, y1 + 4, x2, y2 - 4, border_color, thickness)


def draw_line(pixels, x1, y1, x2, y2, color, thickness=2):
    """Draw a line using Bresenham's algorithm with thickness"""
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        for t in range(-thickness//2, thickness//2 + 1):
            if dx > dy:
                py = y1 + t
                if 0 <= py < len(pixels) and 0 <= x1 < len(pixels[0]):
                    pixels[py][x1] = color
            else:
                px = x1 + t
                if 0 <= y1 < len(pixels) and 0 <= px < len(pixels[0]):
                    pixels[y1][px] = color
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def draw_arrow(pixels, x1, y1, x2, y2, color, thickness=2):
    """Draw an arrow from (x1,y1) to (x2,y2)"""
    draw_line(pixels, x1, y1, x2, y2, color, thickness)
    # Arrowhead
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 12
    a1 = angle + math.pi * 0.8
    a2 = angle - math.pi * 0.8
    ax1, ay1 = int(x2 + arrow_len * math.cos(a1)), int(y2 + arrow_len * math.sin(a1))
    ax2, ay2 = int(x2 + arrow_len * math.cos(a2)), int(y2 + arrow_len * math.sin(a2))
    draw_line(pixels, x2, y2, ax1, ay1, color, thickness)
    draw_line(pixels, x2, y2, ax2, ay2, color, thickness)


def draw_circle(pixels, cx, cy, radius, color, thickness=2):
    """Draw a circle outline"""
    for angle_deg in range(360):
        angle = math.radians(angle_deg)
        for t in range(thickness):
            x = int(cx + (radius - t) * math.cos(angle))
            y = int(cy + (radius - t) * math.sin(angle))
            if 0 <= y < len(pixels) and 0 <= x < len(pixels[0]):
                pixels[y][x] = color


def draw_filled_circle(pixels, cx, cy, radius, color):
    """Draw a filled circle"""
    for y in range(cy - radius, cy + radius + 1):
        for x in range(cx - radius, cx + radius + 1):
            if (x - cx)**2 + (y - cy)**2 <= radius**2:
                if 0 <= y < len(pixels) and 0 <= x < len(pixels[0]):
                    pixels[y][x] = color


# 5x7 bitmap font for text rendering
FONT_5X7 = {
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
    '2': ['01110','10001','00001','00110','01000','10000','11111'],
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
    '/': ['00001','00010','00010','00100','01000','01000','10000'],
    '(': ['00010','00100','01000','01000','01000','00100','00010'],
    ')': ['01000','00100','00010','00010','00010','00100','01000'],
    '&': ['01100','10010','10100','01000','10101','10010','01101'],
    '+': ['00000','00100','00100','11111','00100','00100','00000'],
    '=': ['00000','00000','11111','00000','11111','00000','00000'],
    '>': ['10000','01000','00100','00010','00100','01000','10000'],
    '<': ['00010','00100','01000','10000','01000','00100','00010'],
    '?': ['01110','10001','00001','00110','00100','00000','00100'],
    '!': ['00100','00100','00100','00100','00100','00000','00100'],
    "'": ['00100','00100','01000','00000','00000','00000','00000'],
}


def draw_text(pixels, x, y, text, color, scale=2):
    """Draw text on pixels using bitmap font"""
    cursor_x = x
    for char in text.upper():
        if char in FONT_5X7:
            bitmap = FONT_5X7[char]
            for row_idx, row in enumerate(bitmap):
                for col_idx, bit in enumerate(row):
                    if bit == '1':
                        for sy in range(scale):
                            for sx in range(scale):
                                px = cursor_x + col_idx * scale + sx
                                py = y + row_idx * scale + sy
                                if 0 <= py < len(pixels) and 0 <= px < len(pixels[0]):
                                    pixels[py][px] = color
            cursor_x += 6 * scale  # 5 pixels + 1 space, scaled
        else:
            cursor_x += 6 * scale


def text_width(text, scale=2):
    """Calculate text width in pixels"""
    return len(text) * 6 * scale



def create_figure1():
    """Figure 1: Stakeholder Accountability Framework
    Shows the key stakeholders and their expectations flowing into accreditation."""
    W, H = 800, 500
    pixels = [[(255, 255, 255) for _ in range(W)] for _ in range(H)]

    # Colors
    DARK_BLUE = (25, 60, 120)
    MED_BLUE = (50, 100, 170)
    LIGHT_BLUE = (200, 220, 245)
    GOLD = (180, 140, 30)
    LIGHT_GOLD = (255, 240, 200)
    GREEN = (30, 120, 60)
    LIGHT_GREEN = (210, 240, 210)
    RED = (160, 40, 40)
    LIGHT_RED = (255, 220, 220)
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)

    # Title
    title = "STAKEHOLDER ACCOUNTABILITY FRAMEWORK"
    draw_text(pixels, (W - text_width(title, 2)) // 2, 15, title, DARK_BLUE, 2)

    # Central box - Accreditation
    cx, cy = 400, 260
    bw, bh = 160, 60
    draw_filled_rect(pixels, cx - bw//2, cy - bh//2, cx + bw//2, cy + bh//2, LIGHT_BLUE)
    draw_rect_border(pixels, cx - bw//2, cy - bh//2, cx + bw//2, cy + bh//2, DARK_BLUE, 3)
    draw_text(pixels, cx - text_width("ACCREDITATION", 2)//2, cy - 7, "ACCREDITATION", DARK_BLUE, 2)

    # Stakeholder boxes
    boxes = [
        (130, 100, "STUDENTS", "AND FAMILIES", LIGHT_GOLD, GOLD),
        (400, 80, "EMPLOYERS", "AND INDUSTRY", LIGHT_GREEN, GREEN),
        (670, 100, "GOVERNMENT", "AND POLICY", LIGHT_RED, RED),
        (130, 420, "FACULTY", "AND STAFF", LIGHT_BLUE, MED_BLUE),
        (670, 420, "PUBLIC", "AND SOCIETY", LIGHT_GREEN, GREEN),
    ]

    for bx, by, line1, line2, fill, border in boxes:
        draw_filled_rect(pixels, bx - 75, by - 30, bx + 75, by + 30, fill)
        draw_rect_border(pixels, bx - 75, by - 30, bx + 75, by + 30, border, 2)
        draw_text(pixels, bx - text_width(line1, 1)//2, by - 12, line1, border, 1)
        draw_text(pixels, bx - text_width(line2, 1)//2, by + 4, line2, border, 1)

    # Arrows from stakeholders to center
    arrow_targets = [
        (130, 130, cx - bw//2, cy - 10),
        (400, 110, cx, cy - bh//2),
        (670, 130, cx + bw//2, cy - 10),
        (130, 390, cx - bw//2, cy + 10),
        (670, 390, cx + bw//2, cy + 10),
    ]
    for x1, y1, x2, y2 in arrow_targets:
        draw_arrow(pixels, x1, y1, x2, y2, GRAY, 2)

    # Expectation labels along arrows
    labels = [
        (160, 175, "ROI/VALUE"),
        (400, 135, "COMPETENCIES"),
        (580, 175, "FUNDING"),
        (170, 365, "QUALITY"),
        (580, 365, "TRUST"),
    ]
    for lx, ly, txt in labels:
        draw_text(pixels, lx, ly, txt, GRAY, 1)

    # Bottom label
    subtitle = "FIGURE 1: MULTIPLE STAKEHOLDERS DEMAND DEMONSTRABLE PROOF OF INSTITUTIONAL QUALITY"
    draw_text(pixels, (W - text_width(subtitle, 1)) // 2, H - 25, subtitle, BLACK, 1)

    return create_png(W, H, pixels)


def create_figure2():
    """Figure 2: The Organizational Learning Cycle through Accreditation
    Shows the cyclical process: Self-Study -> Data Analysis -> Peer Review -> Action -> loop"""
    W, H = 800, 500
    pixels = [[(255, 255, 255) for _ in range(W)] for _ in range(H)]

    # Colors
    DARK_BLUE = (25, 60, 120)
    MED_BLUE = (50, 100, 170)
    LIGHT_BLUE = (210, 225, 245)
    PURPLE = (90, 40, 130)
    LIGHT_PURPLE = (230, 215, 245)
    TEAL = (20, 120, 120)
    LIGHT_TEAL = (200, 240, 240)
    ORANGE = (180, 90, 20)
    LIGHT_ORANGE = (255, 230, 200)
    BLACK = (0, 0, 0)
    GRAY = (80, 80, 80)

    # Title
    title = "THE ORGANIZATIONAL LEARNING CYCLE"
    draw_text(pixels, (W - text_width(title, 2)) // 2, 15, title, DARK_BLUE, 2)

    # Draw 4 boxes in a cycle
    cx, cy = 400, 275
    radius = 150

    positions = [
        (cx, cy - radius, "SELF-STUDY", "INQUIRY", LIGHT_BLUE, MED_BLUE),
        (cx + radius + 40, cy, "DATA ANALYSIS", "AND EVIDENCE", LIGHT_TEAL, TEAL),
        (cx, cy + radius, "PEER REVIEW", "AND FEEDBACK", LIGHT_PURPLE, PURPLE),
        (cx - radius - 40, cy, "ACTION AND", "IMPROVEMENT", LIGHT_ORANGE, ORANGE),
    ]

    box_w, box_h = 130, 55
    for bx, by, line1, line2, fill, border in positions:
        draw_filled_rect(pixels, bx - box_w//2, by - box_h//2, bx + box_w//2, by + box_h//2, fill)
        draw_rect_border(pixels, bx - box_w//2, by - box_h//2, bx + box_w//2, by + box_h//2, border, 2)
        draw_text(pixels, bx - text_width(line1, 1)//2, by - 10, line1, border, 1)
        draw_text(pixels, bx - text_width(line2, 1)//2, by + 6, line2, border, 1)

    # Draw curved arrows between boxes (simplified as straight arrows)
    # Top -> Right
    draw_arrow(pixels, cx + box_w//2, cy - radius + 10, cx + radius + 40 - box_w//2, cy - box_h//2 + 10, GRAY, 2)
    # Right -> Bottom
    draw_arrow(pixels, cx + radius + 40 - 10, cy + box_h//2, cx + box_w//2, cy + radius - 10, GRAY, 2)
    # Bottom -> Left
    draw_arrow(pixels, cx - box_w//2, cy + radius - 10, cx - radius - 40 + box_w//2, cy + box_h//2 - 10, GRAY, 2)
    # Left -> Top
    draw_arrow(pixels, cx - radius - 40 + 10, cy - box_h//2, cx - box_w//2, cy - radius + 10, GRAY, 2)

    # Center label
    draw_text(pixels, cx - text_width("CONTINUOUS", 1)//2, cy - 8, "CONTINUOUS", DARK_BLUE, 1)
    draw_text(pixels, cx - text_width("LEARNING", 1)//2, cy + 8, "LEARNING", DARK_BLUE, 1)

    # Annotations
    annotations = [
        (cx + 85, cy - radius + 45, "BRIDGING SILOS"),
        (cx + radius + 60, cy + 50, "EVIDENCE-BASED"),
        (cx - 20, cy + radius + 35, "EXTERNAL EYES"),
        (cx - radius - 120, cy - 50, "CLOSE THE LOOP"),
    ]
    for ax, ay, txt in annotations:
        draw_text(pixels, ax, ay, txt, GRAY, 1)

    # Bottom caption
    subtitle = "FIGURE 2: ACCREDITATION AS A CYCLICAL FRAMEWORK FOR INSTITUTIONAL LEARNING"
    draw_text(pixels, (W - text_width(subtitle, 1)) // 2, H - 25, subtitle, BLACK, 1)

    return create_png(W, H, pixels)


def create_figure3():
    """Figure 3: The Virtuous Cycle - Accountability, Learning, Renewal
    Shows the three dimensions as an interconnected triangle/cycle."""
    W, H = 800, 520
    pixels = [[(255, 255, 255) for _ in range(W)] for _ in range(H)]

    # Colors
    DARK_BLUE = (25, 60, 120)
    BLUE = (40, 90, 160)
    LIGHT_BLUE = (210, 225, 245)
    GREEN = (30, 120, 50)
    LIGHT_GREEN = (210, 240, 210)
    PURPLE = (100, 40, 130)
    LIGHT_PURPLE = (235, 215, 250)
    BLACK = (0, 0, 0)
    GRAY = (80, 80, 80)
    GOLD = (170, 130, 20)

    # Title
    title = "THE VIRTUOUS CYCLE: ACCOUNTABILITY"
    title2 = "LEARNING AND RENEWAL"
    draw_text(pixels, (W - text_width(title, 2)) // 2, 10, title, DARK_BLUE, 2)
    draw_text(pixels, (W - text_width(title2, 2)) // 2, 32, title2, DARK_BLUE, 2)

    # Three main nodes in a triangle
    # Top: Accountability
    ax, ay = 400, 130
    # Bottom-left: Learning
    lx, ly = 200, 380
    # Bottom-right: Renewal
    rx, ry = 600, 380

    node_w, node_h = 150, 65

    # Accountability node
    draw_filled_rect(pixels, ax - node_w//2, ay - node_h//2, ax + node_w//2, ay + node_h//2, LIGHT_BLUE)
    draw_rect_border(pixels, ax - node_w//2, ay - node_h//2, ax + node_w//2, ay + node_h//2, BLUE, 3)
    draw_text(pixels, ax - text_width("ACCOUNTABILITY", 2)//2, ay - 7, "ACCOUNTABILITY", BLUE, 2)

    # Learning node
    draw_filled_rect(pixels, lx - node_w//2, ly - node_h//2, lx + node_w//2, ly + node_h//2, LIGHT_GREEN)
    draw_rect_border(pixels, lx - node_w//2, ly - node_h//2, lx + node_w//2, ly + node_h//2, GREEN, 3)
    draw_text(pixels, lx - text_width("LEARNING", 2)//2, ly - 7, "LEARNING", GREEN, 2)

    # Renewal node
    draw_filled_rect(pixels, rx - node_w//2, ry - node_h//2, rx + node_w//2, ry + node_h//2, LIGHT_PURPLE)
    draw_rect_border(pixels, rx - node_w//2, ry - node_h//2, rx + node_w//2, ry + node_h//2, PURPLE, 3)
    draw_text(pixels, rx - text_width("RENEWAL", 2)//2, ry - 7, "RENEWAL", PURPLE, 2)

    # Arrows connecting the three (bidirectional)
    # Accountability -> Learning
    draw_arrow(pixels, ax - node_w//2 + 20, ay + node_h//2, lx + node_w//2 - 20, ly - node_h//2, GRAY, 2)
    # Learning -> Renewal
    draw_arrow(pixels, lx + node_w//2, ly, rx - node_w//2, ry, GRAY, 2)
    # Renewal -> Accountability
    draw_arrow(pixels, rx - 20, ry - node_h//2, ax + node_w//2 - 20, ay + node_h//2, GRAY, 2)

    # Labels on arrows
    draw_text(pixels, 240, 240, "EVIDENCE AND", GRAY, 1)
    draw_text(pixels, 240, 256, "SELF-KNOWLEDGE", GRAY, 1)
    draw_text(pixels, 350, 410, "STRATEGIC", GRAY, 1)
    draw_text(pixels, 350, 426, "ACTION", GRAY, 1)
    draw_text(pixels, 540, 240, "INSTITUTIONAL", GRAY, 1)
    draw_text(pixels, 540, 256, "LEGITIMACY", GRAY, 1)

    # Center - CQI
    draw_filled_circle(pixels, 400, 310, 35, (255, 245, 220))
    draw_circle(pixels, 400, 310, 35, GOLD, 2)
    draw_text(pixels, 400 - text_width("CQI", 2)//2, 303, "CQI", GOLD, 2)

    # Bottom caption
    subtitle = "FIGURE 3: THE THREE DIMENSIONS FORM A VIRTUOUS CYCLE OF CONTINUOUS IMPROVEMENT"
    draw_text(pixels, (W - text_width(subtitle, 1)) // 2, H - 25, subtitle, BLACK, 1)

    return create_png(W, H, pixels)



# ============================================================
# DOCX GENERATION - Tables and Images embedded
# ============================================================

NSMAP = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
}


def ns(prefix, tag):
    return f'{{{NSMAP[prefix]}}}{tag}'


def make_paragraph_el(text, style=None, bold=False, italic=False, indent_first=False, centered=False, font_size=24):
    """Create a paragraph element. font_size is in half-points (24 = 12pt)."""
    p = Element(ns('w', 'p'))
    pPr = SubElement(p, ns('w', 'pPr'))
    if style:
        pStyle = SubElement(pPr, ns('w', 'pStyle'))
        pStyle.set(ns('w', 'val'), style)
    spacing = SubElement(pPr, ns('w', 'spacing'))
    spacing.set(ns('w', 'line'), '480')
    spacing.set(ns('w', 'lineRule'), 'auto')
    if indent_first:
        ind = SubElement(pPr, ns('w', 'ind'))
        ind.set(ns('w', 'firstLine'), '720')
    if centered:
        jc = SubElement(pPr, ns('w', 'jc'))
        jc.set(ns('w', 'val'), 'center')
    if text:
        r = SubElement(p, ns('w', 'r'))
        rPr = SubElement(r, ns('w', 'rPr'))
        rFonts = SubElement(rPr, ns('w', 'rFonts'))
        rFonts.set(ns('w', 'ascii'), 'Times New Roman')
        rFonts.set(ns('w', 'hAnsi'), 'Times New Roman')
        rFonts.set(ns('w', 'cs'), 'Times New Roman')
        sz = SubElement(rPr, ns('w', 'sz'))
        sz.set(ns('w', 'val'), str(font_size))
        szCs = SubElement(rPr, ns('w', 'szCs'))
        szCs.set(ns('w', 'val'), str(font_size))
        if bold:
            SubElement(rPr, ns('w', 'b'))
        if italic:
            SubElement(rPr, ns('w', 'i'))
        t = SubElement(r, ns('w', 't'))
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t.text = text
    return p


def make_table(headers, rows):
    """Create a Word table element with borders."""
    tbl = Element(ns('w', 'tbl'))
    
    # Table properties
    tblPr = SubElement(tbl, ns('w', 'tblPr'))
    tblW = SubElement(tblPr, ns('w', 'tblW'))
    tblW.set(ns('w', 'w'), '9000')
    tblW.set(ns('w', 'type'), 'dxa')
    
    # Table borders
    tblBorders = SubElement(tblPr, ns('w', 'tblBorders'))
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = SubElement(tblBorders, ns('w', border_name))
        border.set(ns('w', 'val'), 'single')
        border.set(ns('w', 'sz'), '4')
        border.set(ns('w', 'space'), '0')
        border.set(ns('w', 'color'), '000000')
    
    # Table layout
    tblLayout = SubElement(tblPr, ns('w', 'tblLayout'))
    tblLayout.set(ns('w', 'type'), 'fixed')
    
    # Column widths
    num_cols = len(headers)
    col_width = 9000 // num_cols
    tblGrid = SubElement(tbl, ns('w', 'tblGrid'))
    for _ in range(num_cols):
        gridCol = SubElement(tblGrid, ns('w', 'gridCol'))
        gridCol.set(ns('w', 'w'), str(col_width))
    
    # Header row
    tr = SubElement(tbl, ns('w', 'tr'))
    for h in headers:
        tc = SubElement(tr, ns('w', 'tc'))
        tcPr = SubElement(tc, ns('w', 'tcPr'))
        tcW = SubElement(tcPr, ns('w', 'tcW'))
        tcW.set(ns('w', 'w'), str(col_width))
        tcW.set(ns('w', 'type'), 'dxa')
        # Shading for header
        shd = SubElement(tcPr, ns('w', 'shd'))
        shd.set(ns('w', 'val'), 'clear')
        shd.set(ns('w', 'color'), 'auto')
        shd.set(ns('w', 'fill'), 'D9E2F3')
        p = make_paragraph_el(h, bold=True, centered=True, font_size=20)
        tc.append(p)
    
    # Data rows
    for row in rows:
        tr = SubElement(tbl, ns('w', 'tr'))
        for cell in row:
            tc = SubElement(tr, ns('w', 'tc'))
            tcPr = SubElement(tc, ns('w', 'tcPr'))
            tcW = SubElement(tcPr, ns('w', 'tcW'))
            tcW.set(ns('w', 'w'), str(col_width))
            tcW.set(ns('w', 'type'), 'dxa')
            p = make_paragraph_el(cell, font_size=20)
            tc.append(p)
    
    return tbl


def make_image_paragraph(rel_id, width_emu, height_emu, alt_text="Figure"):
    """Create a paragraph containing an inline image."""
    p = Element(ns('w', 'p'))
    pPr = SubElement(p, ns('w', 'pPr'))
    jc = SubElement(pPr, ns('w', 'jc'))
    jc.set(ns('w', 'val'), 'center')
    spacing = SubElement(pPr, ns('w', 'spacing'))
    spacing.set(ns('w', 'line'), '480')
    spacing.set(ns('w', 'lineRule'), 'auto')
    
    r = SubElement(p, ns('w', 'r'))
    drawing = SubElement(r, ns('w', 'drawing'))
    
    inline = SubElement(drawing, ns('wp', 'inline'))
    inline.set('distT', '0')
    inline.set('distB', '0')
    inline.set('distL', '0')
    inline.set('distR', '0')
    
    extent = SubElement(inline, ns('wp', 'extent'))
    extent.set('cx', str(width_emu))
    extent.set('cy', str(height_emu))
    
    docPr = SubElement(inline, ns('wp', 'docPr'))
    docPr.set('id', '1')
    docPr.set('name', alt_text)
    
    graphic = SubElement(inline, ns('a', 'graphic'))
    graphicData = SubElement(graphic, ns('a', 'graphicData'))
    graphicData.set('uri', 'http://schemas.openxmlformats.org/drawingml/2006/picture')
    
    pic_el = SubElement(graphicData, ns('pic', 'pic'))
    nvPicPr = SubElement(pic_el, ns('pic', 'nvPicPr'))
    cNvPr = SubElement(nvPicPr, ns('pic', 'cNvPr'))
    cNvPr.set('id', '0')
    cNvPr.set('name', alt_text)
    cNvPicPr = SubElement(nvPicPr, ns('pic', 'cNvPicPr'))
    
    blipFill = SubElement(pic_el, ns('pic', 'blipFill'))
    blip = SubElement(blipFill, ns('a', 'blip'))
    blip.set(ns('r', 'embed'), rel_id)
    stretch = SubElement(blipFill, ns('a', 'stretch'))
    SubElement(stretch, ns('a', 'fillRect'))
    
    spPr = SubElement(pic_el, ns('pic', 'spPr'))
    xfrm = SubElement(spPr, ns('a', 'xfrm'))
    off = SubElement(xfrm, ns('a', 'off'))
    off.set('x', '0')
    off.set('y', '0')
    ext = SubElement(xfrm, ns('a', 'ext'))
    ext.set('cx', str(width_emu))
    ext.set('cy', str(height_emu))
    prstGeom = SubElement(spPr, ns('a', 'prstGeom'))
    prstGeom.set('prst', 'rect')
    
    return p


def make_ref_paragraph(text):
    """Reference paragraph with hanging indent"""
    p = Element(ns('w', 'p'))
    pPr = SubElement(p, ns('w', 'pPr'))
    spacing = SubElement(pPr, ns('w', 'spacing'))
    spacing.set(ns('w', 'line'), '480')
    spacing.set(ns('w', 'lineRule'), 'auto')
    spacing.set(ns('w', 'after'), '0')
    ind = SubElement(pPr, ns('w', 'ind'))
    ind.set(ns('w', 'left'), '720')
    ind.set(ns('w', 'hanging'), '720')
    if text:
        r = SubElement(p, ns('w', 'r'))
        rPr = SubElement(r, ns('w', 'rPr'))
        rFonts = SubElement(rPr, ns('w', 'rFonts'))
        rFonts.set(ns('w', 'ascii'), 'Times New Roman')
        rFonts.set(ns('w', 'hAnsi'), 'Times New Roman')
        rFonts.set(ns('w', 'cs'), 'Times New Roman')
        sz = SubElement(rPr, ns('w', 'sz'))
        sz.set(ns('w', 'val'), '24')
        szCs = SubElement(rPr, ns('w', 'szCs'))
        szCs.set(ns('w', 'val'), '24')
        t = SubElement(r, ns('w', 't'))
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t.text = text
    return p



def build_document():
    """Build the complete document with text, tables, and figures."""
    paragraphs = []
    
    def add_blank():
        paragraphs.append(make_paragraph_el(''))
    
    def add_heading(text, level=1):
        style = 'Heading1' if level == 1 else 'Heading2'
        paragraphs.append(make_paragraph_el(text, style=style, bold=True))
    
    def add_body(text, indent=True):
        paragraphs.append(make_paragraph_el(text, indent_first=indent))
    
    def add_centered(text, bold=False, italic=False):
        paragraphs.append(make_paragraph_el(text, bold=bold, italic=italic, centered=True))

    # ---- TITLE PAGE ----
    add_blank()
    add_blank()
    add_heading('Accreditation as Accountability, Learning, and Institutional Renewal')
    add_blank()
    add_heading('Author Information', level=2)
    add_blank()
    paragraphs.append(make_paragraph_el('[Author Name]'))
    paragraphs.append(make_paragraph_el('ORCID: [0000-0000-0000-0000]'))
    paragraphs.append(make_paragraph_el('Affiliation: [Department, Institution, City, Country]'))
    paragraphs.append(make_paragraph_el('Email: [author.email@institution.edu]'))
    add_blank()
    add_body('Bio: [Author Name] is a [title/position] at [Institution]. With over [X] years of experience in higher education policy and accreditation, [he/she/they] has published extensively on quality assurance, institutional effectiveness, and organizational learning in post-secondary education. [His/Her/Their] research focuses on the intersection of accountability frameworks and institutional transformation in a globalized higher education landscape. [He/She/They] has served on multiple accreditation review teams and advisory boards.', indent=False)
    add_blank()
    add_blank()

    # ---- ABSTRACT ----
    add_heading('Abstract', level=2)
    add_blank()
    add_body('This chapter examines the multifaceted role of accreditation in contemporary higher education, arguing that its true power lies not in any single function but in the dynamic interplay among three essential dimensions: accountability, learning, and institutional renewal. In an era marked by unprecedented skepticism toward the value of higher education, escalating costs, and rapid technological disruption, accreditation has evolved from a collegial peer-review process into a high-stakes mechanism for demonstrating institutional legitimacy. This chapter moves beyond the conventional view of accreditation as merely a compliance exercise. Drawing on organizational learning theory, institutional theory, and quality improvement frameworks, it demonstrates how a strategically approached accreditation process can serve as a powerful catalyst for self-discovery, evidence-based decision-making, and transformative institutional change. The chapter is structured around three interconnected sections: the accountability imperative that establishes the non-negotiable baseline of quality assurance; the learning dimension that repositions the process as a framework for organizational intelligence; and the renewal function that translates self-knowledge into strategic foresight and cultural transformation. The analysis concludes by proposing that institutions that embrace this holistic, cyclical view of accreditation can transform what is often perceived as a bureaucratic burden into their most powerful instrument for thriving in the boundaryless landscape of twenty-first-century higher education.')
    add_blank()
    paragraphs.append(make_paragraph_el('Keywords: accreditation, accountability, institutional learning, quality assurance, continuous improvement, higher education, organizational renewal, self-study, peer review'))
    add_blank()
    add_blank()

    # ---- INTRODUCTION ----
    add_heading('Introduction')
    add_blank()
    add_body('The landscape of higher education is undergoing a period of profound transformation. Traditional boundaries\u2014between disciplines, between institutions, between nations, and between the academy and the world of work\u2014are dissolving at an accelerating pace. In this environment of radical change, the question of how institutions demonstrate their quality, relevance, and fitness for purpose has become one of the most consequential debates in educational policy [1]. At the center of this debate stands accreditation: a process that is simultaneously ancient in its collegial principles and urgently modern in its demands.')
    add_blank()
    add_body('Accreditation in higher education has long functioned as the primary mechanism through which institutions voluntarily submit to external review to demonstrate that they meet established standards of quality [2]. Yet the perception and purpose of this process have shifted dramatically over the past three decades. What was once a largely private conversation among academic peers has become a public instrument of accountability, scrutinized by legislators, journalists, and an increasingly skeptical public demanding evidence that the substantial investment in higher education yields meaningful returns [3, 4].')
    add_blank()
    add_body('This chapter advances a central argument: that accreditation, when approached with intentionality and strategic vision, functions not as a single activity but as a dynamic cycle comprising three interconnected dimensions\u2014accountability, learning, and renewal. Accountability represents the non-negotiable baseline: the demonstration to external stakeholders that an institution is financially viable, ethically governed, and educationally effective. Learning represents the transformative middle ground: the use of systematic self-examination and peer review to build organizational intelligence and foster a culture of evidence-based inquiry. Renewal represents the ultimate aspiration: the translation of institutional self-knowledge into strategic action, adaptive capacity, and cultural transformation that positions the institution for long-term flourishing.')
    add_blank()
    add_body('These three dimensions are not sequential phases but rather simultaneous and mutually reinforcing aspects of a single, virtuous cycle. Accountability without learning becomes mere bureaucratic compliance; learning without renewal is intellectual exercise without consequence; renewal without accountability is unsustainable aspiration without foundation. This chapter explores each dimension in turn, drawing on theoretical frameworks from organizational learning [5, 6], institutional theory [7], and quality management [8], while grounding the analysis in the practical realities of accreditation as experienced by institutions navigating the boundaryless landscape of contemporary higher education.')
    add_blank()
    add_body('The significance of this argument extends beyond the procedural mechanics of accreditation to address fundamental questions about the nature and purpose of quality assurance in post-secondary education. As institutions face existential challenges\u2014demographic shifts that threaten enrollment stability, technological disruptions that challenge traditional pedagogical models, and legitimacy crises that erode public support\u2014the capacity to learn and adapt becomes not merely desirable but essential for institutional survival. Accreditation, reconceived as a catalyst for this adaptive capacity, offers institutions a structured pathway from compliance to transformation\u2014a pathway that honors the legitimate demands of accountability while simultaneously cultivating the organizational intelligence necessary for strategic renewal [9].')
    add_blank()
    add_blank()

    return paragraphs



def build_section1(paragraphs):
    """Section 1 with Table 1 and Figure 1"""
    def add_blank():
        paragraphs.append(make_paragraph_el(''))
    def add_heading(text, level=1):
        style = 'Heading1' if level == 1 else 'Heading2'
        paragraphs.append(make_paragraph_el(text, style=style, bold=True))
    def add_body(text, indent=True):
        paragraphs.append(make_paragraph_el(text, indent_first=indent))
    def add_centered(text, bold=False, italic=False):
        paragraphs.append(make_paragraph_el(text, bold=bold, italic=italic, centered=True))

    add_heading('Section 1: The Face of Accountability: Demonstrating Value in a Skeptical Era')
    add_blank()
    add_heading('1.1 The Stakeholder Mandate: From Public Trust to Public Proof', level=2)
    add_blank()
    add_body('The social contract between higher education and the public has undergone a fundamental renegotiation. For much of the twentieth century, institutions of higher learning operated under a regime of presumptive trust. Society granted universities considerable autonomy\u2014intellectual, financial, and operational\u2014in exchange for the broadly understood social goods of research, teaching, and community service [10]. Accreditation, in this context, functioned primarily as a form of self-regulation among peers, a collegial handshake affirming that a fellow institution met basic standards of respectability.')
    add_blank()
    add_body('That era of presumptive trust has ended. In its place has emerged what might be termed a regime of demonstrable proof [11]. Multiple forces have driven this transformation. The exponential growth of tuition costs has converted higher education from a broadly accessible public good into what many families experience as a high-stakes financial investment demanding quantifiable returns [4]. The proliferation of post-secondary providers\u2014including for-profit institutions, online platforms, and international competitors\u2014has created a marketplace in which the traditional signals of quality are no longer sufficient differentiators. Simultaneously, a series of high-profile institutional failures and predatory practices has eroded public confidence in the capacity of higher education to police itself [12].')
    add_blank()
    add_body('The cost-value equation has become the dominant frame through which students and families assess educational options. In a globalized market with thousands of providers, accreditation serves as the primary quality benchmark\u2014a credible signal that an institution has been externally validated against recognized standards [13]. From the employer\u2019s perspective, accreditation functions as a risk-reduction mechanism, ensuring graduates possess a baseline of knowledge, skills, and professional competencies [14]. The governmental dimension is perhaps the most consequential: institutional accreditation serves as the gateway to federal financial aid\u2014a mechanism that channels over $150 billion annually to students and institutions [15].')
    add_blank()
    add_body('Internationally, this governmental interest in accreditation has intensified as nations recognize the economic implications of higher education quality. The Bologna Process in Europe, the establishment of national quality assurance agencies across Asia and Africa, and the growth of cross-border quality assurance networks all reflect a global convergence toward more systematic accountability mechanisms [16].')
    add_blank()

    # ---- TABLE 1 ----
    add_blank()
    add_centered('Table 1', bold=True)
    add_centered('Stakeholder Expectations and Accreditation Responses', italic=True)
    add_blank()
    table1 = make_table(
        ['Stakeholder', 'Primary Expectation', 'Accreditation Response', 'Key Outcome Metric'],
        [
            ['Students and Families', 'Return on investment; credential portability', 'Quality benchmarking; credit transfer assurance', 'Graduation rates; employment rates'],
            ['Employers and Industry', 'Graduate competency; workforce readiness', 'Program-level learning outcomes; professional standards', 'Licensure pass rates; employer satisfaction'],
            ['Government (Federal/State)', 'Responsible use of public funds; student protection', 'Financial viability review; compliance standards', 'Default rates; completion rates'],
            ['Faculty and Staff', 'Academic freedom; professional development', 'Governance standards; faculty qualifications', 'Faculty retention; scholarly productivity'],
            ['General Public', 'Institutional integrity; social contribution', 'Mission fidelity review; transparency requirements', 'Community engagement; public trust indices'],
        ]
    )
    paragraphs.append(table1)
    add_blank()
    add_blank()

    # ---- Continue Section 1.2 ----
    add_heading('1.2 Compliance and Standards: The Baseline of Quality Assurance', level=2)
    add_blank()
    add_body('If the stakeholder mandate establishes the why of accountability, accreditation standards establish the what. Standards represent the codified expectations against which institutional quality is measured\u2014the \u201chygiene factors\u201d whose absence signals fundamental deficiency but whose presence alone does not guarantee excellence [17]. Financial viability constitutes a primary domain: institutions must demonstrate sound fiscal management and adequate reserves [18]. Student protection requires transparent admissions policies, fair grading practices, and accessible grievance procedures [19, 20]. Mission fidelity ensures that actual operations align with stated purposes [21].')
    add_blank()
    add_body('Beyond these specific domains, accreditation standards collectively establish the infrastructure of educational integrity. They require institutions to maintain qualified faculty, adequate resources, coherent curricula, effective governance, and systematic assessment processes [18]. Their codification creates explicit expectations against which institutional performance can be measured and\u2014when necessary\u2014sanctioned.')
    add_blank()

    # ---- Section 1.3 ----
    add_heading('1.3 Navigating the \u201cAudit Culture\u201d: The Pitfalls and Potentials', level=2)
    add_blank()
    add_body('While accountability serves essential purposes, the concept of \u201caudit culture\u201d [22] provides a critical lens for understanding dysfunctions that emerge when accountability becomes an end in itself. The \u201cbox-checking\u201d mentality\u2014performative compliance focused on satisfying the letter rather than spirit of standards\u2014represents the most pervasive pathology [16]. Mission creep occurs when institutions feel pressure to conform to a singular model of quality that does not align with their unique purposes [23]. The burden of evidence can divert limited personnel from direct educational activities [24].')
    add_blank()

    # ---- FIGURE 1 ----
    add_blank()
    paragraphs.append(make_image_paragraph('rId3', 6096000, 3810000, 'Figure 1'))
    add_blank()
    add_centered('Figure 1. Stakeholder Accountability Framework: Multiple stakeholders demand', italic=True)
    add_centered('demonstrable proof of institutional quality through the accreditation process.', italic=True)
    add_blank()
    add_blank()

    return paragraphs



def build_section2(paragraphs):
    """Section 2 with Table 2 and Figure 2"""
    def add_blank():
        paragraphs.append(make_paragraph_el(''))
    def add_heading(text, level=1):
        style = 'Heading1' if level == 1 else 'Heading2'
        paragraphs.append(make_paragraph_el(text, style=style, bold=True))
    def add_body(text, indent=True):
        paragraphs.append(make_paragraph_el(text, indent_first=indent))
    def add_centered(text, bold=False, italic=False):
        paragraphs.append(make_paragraph_el(text, bold=bold, italic=italic, centered=True))

    add_heading('Section 2: The Pedagogy of Organizations: Accreditation as a Framework for Learning')
    add_blank()
    add_heading('2.1 The Self-Study as a Diagnostic Tool: Uncovering Tacit Knowledge', level=2)
    add_blank()
    add_body('If Section 1 addressed the compliance dimension of accreditation, this section repositions the process as a rich opportunity for institutional self-discovery and organizational learning. The theoretical foundation draws on the concept of the \u201clearning organization\u201d [5]: an entity that continuously enhances its capacity to create its desired future through systematic processes of inquiry, reflection, and adaptive action.')
    add_blank()
    add_body('The self-study functions as a powerful diagnostic tool: a structured occasion for an institution to systematically examine its own assumptions, practices, and outcomes [25]. It creates conditions for both single-loop learning (correcting errors within existing frames) and double-loop learning (questioning the frames themselves) [6]. A well-facilitated self-study creates a \u201clearning space\u201d\u2014a psychologically safe environment for asking difficult questions [26]. The requirement to examine the entire institution forces cross-functional communication [27], revealing \u201cunknown unknowns\u201d that constitute the raw material of organizational learning [28].')
    add_blank()
    add_body('The temporal dimension merits attention: unlike routine operations, the self-study creates intensive, systematic reflection that reveals longitudinal patterns obscured in annual reporting cycles [29].')
    add_blank()

    # ---- TABLE 2 ----
    add_blank()
    add_centered('Table 2', bold=True)
    add_centered('Self-Study Components and Institutional Learning Outcomes', italic=True)
    add_blank()
    table2 = make_table(
        ['Self-Study Component', 'Learning Process', 'Organizational Outcome', 'Theory Base'],
        [
            ['Institutional data collection', 'Single-loop learning: error detection', 'Identification of performance gaps', 'Argyris & Schon [6]'],
            ['Cross-functional dialogue', 'Bridging organizational silos', 'Holistic understanding of student experience', 'Senge [5]'],
            ['Mission alignment review', 'Double-loop learning: frame questioning', 'Strategic clarity and purpose renewal', 'Argyris & Schon [6]'],
            ['Stakeholder surveys', 'Environmental scanning', 'Market responsiveness and relevance', 'Volkwein et al. [30]'],
            ['Outcomes assessment', 'Evidence-based inquiry', 'Pedagogical improvement and innovation', 'Banta & Palomba [33]'],
            ['Resource analysis', 'Systems thinking', 'Efficient allocation and sustainability', 'Senge [5]'],
        ]
    )
    paragraphs.append(table2)
    add_blank()
    add_blank()

    # ---- Section 2.2 ----
    add_heading('2.2 Data, Evidence, and the Culture of Inquiry', level=2)
    add_blank()
    add_body('The shift from \u201cdata for compliance\u201d to \u201cdata for understanding\u201d represents a significant advance in contemporary accreditation practice [30]. The process mandates systematic evidence that challenges anecdotal reasoning [31]. Learning analytics represents an emerging frontier\u2014using accreditation data infrastructure to build predictive models for student success [32]. Closing the assessment loop\u2014implementing changes based on evidence and then re-assessing\u2014is the engine of institutional learning [33]. The cultural shift from autonomous judgment to evidence-based practice requires careful framing of assessment as professional enhancement rather than surveillance [34].')
    add_blank()

    # ---- Section 2.3 ----
    add_heading('2.3 Peer Review: The Transformative Power of External Perspectives', level=2)
    add_blank()
    add_body('The peer review visit operates on the principle that institutions are best evaluated by those who share their fundamental purposes [1]. It challenges organizational groupthink [35], enables best practice exchange [36], provides validation that energizes improvement efforts [37], and catalyzes institutional sense-making that extends beyond the formal evaluation period [38].')
    add_blank()

    # ---- FIGURE 2 ----
    add_blank()
    paragraphs.append(make_image_paragraph('rId4', 6096000, 3810000, 'Figure 2'))
    add_blank()
    add_centered('Figure 2. The Organizational Learning Cycle: Accreditation creates a continuous', italic=True)
    add_centered('cycle of self-study, evidence analysis, peer review, and improvement action.', italic=True)
    add_blank()
    add_blank()

    return paragraphs



def build_section3(paragraphs):
    """Section 3 with Table 3 and Figure 3"""
    def add_blank():
        paragraphs.append(make_paragraph_el(''))
    def add_heading(text, level=1):
        style = 'Heading1' if level == 1 else 'Heading2'
        paragraphs.append(make_paragraph_el(text, style=style, bold=True))
    def add_body(text, indent=True):
        paragraphs.append(make_paragraph_el(text, indent_first=indent))
    def add_centered(text, bold=False, italic=False):
        paragraphs.append(make_paragraph_el(text, bold=bold, italic=italic, centered=True))

    add_heading('Section 3: The Catalyst for Renewal: Reimagining the Institution for the Future')
    add_blank()
    add_heading('3.1 Strategic Foresight: Aligning Accreditation with Institutional Strategy', level=2)
    add_blank()
    add_body('The transition from learning to renewal marks the point at which institutional self-knowledge is translated into strategic action [39]. The concept of the \u201crhythm of renewal\u201d reframes the accreditation cycle as a structured timeline for strategic implementation [40]. Mission serves as compass; self-study findings inform resource allocation decisions [23, 41]. Building institutional capacity\u2014data systems, assessment expertise, communication structures\u2014becomes a strategic investment rather than mere accreditation expense [42].')
    add_blank()

    # ---- Section 3.2 ----
    add_heading('3.2 Enhancing Agility and Responsiveness', level=2)
    add_blank()
    add_body('Critics argue that accreditation\u2019s emphasis on stability can slow institutional adaptation [43]. \u201cInnovation sandboxes\u201d offer a framework for piloting new approaches within enhanced monitoring [44]. Responding to workforce shifts requires ongoing environmental scanning [14]. Serving non-traditional students requires models that differ from the traditional paradigm [45, 46].')
    add_blank()

    # ---- TABLE 3 ----
    add_blank()
    add_centered('Table 3', bold=True)
    add_centered('From Compliance Event to Continuous Quality Improvement Culture', italic=True)
    add_blank()
    table3 = make_table(
        ['Dimension', 'Traditional Approach (Event)', 'CQI Approach (Process)', 'Enabling Factors'],
        [
            ['Timing', 'Decennial preparation cycle', 'Ongoing annual assessment cycles', 'Embedded data systems'],
            ['Leadership', 'Top-down administrative mandate', 'Distributed ownership across institution', 'Faculty empowerment'],
            ['Data use', 'Retrospective reporting for compliance', 'Real-time analytics for decision-making', 'Learning analytics platforms'],
            ['Culture', 'Fear-based compliance mentality', 'Curiosity-driven improvement ethos', 'Psychological safety'],
            ['Scope', 'Document production for site visit', 'Systemic organizational learning', 'Cross-functional teams'],
            ['Outcome', 'Reaffirmation of accreditation status', 'Institutional transformation and renewal', 'Strategic alignment'],
        ]
    )
    paragraphs.append(table3)
    add_blank()
    add_blank()

    # ---- Section 3.3 ----
    add_heading('3.3 Fostering a Culture of Continuous Quality Improvement', level=2)
    add_blank()
    add_body('The ultimate aspiration is institutionalizing CQI as a permanent feature of institutional life [47]. This draws on quality management traditions from Deming [8], Juran [48], Seymour [49], and Freed et al. [50]. The transformation from \u201cevent\u201d to \u201cprocess\u201d requires annual assessment cycles, program reviews, and continuous feedback systems [40]. Faculty empowerment\u2014positioning staff as primary agents of quality\u2014is critical [39]. The \u201clearning organization\u201d concept [5] provides the theoretical capstone. Structural infrastructure (data dashboards, governance mechanisms) must complement cultural values of curiosity and collective responsibility [30, 51]. Technology enables real-time monitoring and rapid response [32, 52].')
    add_blank()

    # ---- FIGURE 3 ----
    add_blank()
    paragraphs.append(make_image_paragraph('rId5', 6096000, 3962400, 'Figure 3'))
    add_blank()
    add_centered('Figure 3. The Virtuous Cycle: Accountability, Learning, and Renewal form an', italic=True)
    add_centered('interconnected system with Continuous Quality Improvement at the center.', italic=True)
    add_blank()
    add_blank()

    return paragraphs



def build_conclusion_and_refs(paragraphs):
    """Add conclusion and references"""
    def add_blank():
        paragraphs.append(make_paragraph_el(''))
    def add_heading(text, level=1):
        style = 'Heading1' if level == 1 else 'Heading2'
        paragraphs.append(make_paragraph_el(text, style=style, bold=True))
    def add_body(text, indent=True):
        paragraphs.append(make_paragraph_el(text, indent_first=indent))

    add_heading('Conclusion')
    add_blank()
    add_body('This chapter has argued that accreditation in higher education is most powerfully understood not as a single function but as a dynamic cycle of three interconnected dimensions: accountability, learning, and institutional renewal. Each dimension is essential, and each depends upon the others for its full realization. Accountability provides the foundation of legitimacy and public trust upon which all else rests. Learning transforms accountability from a defensive posture into genuine inquiry. Renewal translates that learning into strategic action, adaptive capacity, and cultural transformation.')
    add_blank()
    add_body('The virtuous cycle that connects these dimensions can be simply stated: Accountability without learning is bureaucratic; learning without renewal is academic; renewal without accountability is unsustainable. An institution that merely documents its compliance without seeking to understand its performance is engaged in a hollow exercise. An institution that understands its strengths and weaknesses but fails to act wastes the knowledge it has generated. And an institution that implements bold changes without grounding them in evidence builds on sand.')
    add_blank()
    add_body('Achieving this ideal requires institutional leadership that values genuine inquiry over comfortable narratives, that creates psychological safety for honest self-assessment, and that demonstrates the courage to act on difficult findings. It requires a culture of trust in which quality improvement is a shared professional responsibility. It requires accrediting bodies that balance gatekeeping with genuine commitment to institutional development.')
    add_blank()
    add_body('Looking forward, accreditation itself must evolve: developing flexible standards that accommodate innovation, embracing technology-enhanced processes, internationalizing perspectives, and building genuine partnerships with institutions. The evolution of accreditation must mirror the evolution it seeks to catalyze: moving from rigidity to agility, from standardization to contextualization, and from retrospective judgment to prospective partnership.')
    add_blank()
    add_body('The call to action is directed at all participants. Institutional leaders must champion transformation beyond compliance. Faculty must engage as genuine partners in inquiry. Accreditors must reward genuine improvement. Policymakers must create space for innovation alongside accountability. Together, these actors can realize accreditation\u2019s full potential as the powerful instrument of institutional renewal that higher education\u2019s boundaryless future demands.')
    add_blank()
    add_body('Ultimately, the measure of accreditation\u2019s success is whether the process contributes to the creation of institutions that are more effective, more responsive, more equitable, and more capable of serving the diverse learners and complex societies that depend upon them. In the boundaryless landscape of twenty-first-century higher education, this catalytic function has never been more important, nor has the opportunity to realize it been greater.')
    add_blank()
    add_blank()

    # ---- REFERENCES ----
    add_heading('References')
    add_blank()

    references = [
        '[1] Eaton, J. S. (2015). An overview of U.S. accreditation. Council for Higher Education Accreditation.',
        '[2] Brittingham, B. (2009). Accreditation in the United States: How did we get to where we are? New Directions for Higher Education, 2009(145), 7\u201327. https://doi.org/10.1002/he.331',
        '[3] Spellings Commission. (2006). A test of leadership: Charting the future of U.S. higher education. U.S. Department of Education.',
        '[4] Kelchen, R. (2018). Higher education accountability. Johns Hopkins University Press.',
        '[5] Senge, P. M. (2006). The fifth discipline: The art and practice of the learning organization (Rev. ed.). Doubleday.',
        '[6] Argyris, C., & Sch\u00f6n, D. A. (1996). Organizational learning II: Theory, method, and practice. Addison-Wesley.',
        '[7] DiMaggio, P. J., & Powell, W. W. (1983). The iron cage revisited: Institutional isomorphism and collective rationality in organizational fields. American Sociological Review, 48(2), 147\u2013160. https://doi.org/10.2307/2095101',
        '[8] Deming, W. E. (1993). The new economics for industry, government, education. MIT Press.',
        '[9] Kezar, A. (2018). How colleges change: Understanding, leading, and enacting change (2nd ed.). Routledge.',
        '[10] Trow, M. (1996). Trust, markets, and accountability in higher education: A comparative perspective. Higher Education Policy, 9(4), 309\u2013324. https://doi.org/10.1016/S0952-8733(96)00029-3',
        '[11] Ewell, P. T. (2009). Assessment, accountability, and improvement: Revisiting the tension (NILOA Occasional Paper No. 1). National Institute for Learning Outcomes Assessment.',
        '[12] U.S. Government Accountability Office. (2010). For-profit colleges: Undercover testing finds colleges encouraged fraud (GAO-10-948T). U.S. GAO.',
        '[13] Hazelkorn, E. (2015). Rankings and the reshaping of higher education (2nd ed.). Palgrave Macmillan.',
        '[14] Carnevale, A. P., Cheah, B., & Wenzinger, E. (2020). The college payoff: More education doesn\u2019t always mean more earnings. Georgetown University Center on Education and the Workforce.',
        '[15] U.S. Department of Education. (2022). Federal student aid annual report. https://studentaid.gov/data-center/student/portfolio',
        '[16] Stensaker, B., & Harvey, L. (2011). Accountability in higher education: Global perspectives on trust and power. Routledge.',
        '[17] Herzberg, F. (1966). Work and the nature of man. World Publishing Company.',
        '[18] Middle States Commission on Higher Education. (2015). Standards for accreditation and requirements of affiliation (13th ed.). MSCHE.',
        '[19] Cochrane, D., & Szabo-Kubitz, L. (2016). On the verge: Costs and tradeoffs facing community college students. The Institute for College Access & Success.',
        '[20] Council for Higher Education Accreditation. (2019). CHEA at a glance. https://www.chea.org/chea-glance',
        '[21] Higher Learning Commission. (2020). Criteria for accreditation. https://www.hlcommission.org/Policies/criteria-and-core-components.html',
        '[22] Power, M. (1997). The audit society: Rituals of verification. Oxford University Press.',
        '[23] Morphew, C. C., & Hartley, M. (2006). Mission statements: A thematic analysis of rhetoric across institutional type. The Journal of Higher Education, 77(3), 456\u2013471. https://doi.org/10.1353/jhe.2006.0023',
        '[24] Lubinescu, E. S., Ratcliff, J. L., & Gaffney, M. A. (2001). Two continuums collide: Accreditation and assessment. New Directions for Higher Education, 2001(113), 5\u201321. https://doi.org/10.1002/he.1',
        '[25] Kells, H. R. (1995). Self-study processes: A guide to self-evaluation in higher education (4th ed.). American Council on Education/Oryx Press.',
        '[26] Edmondson, A. (1999). Psychological safety and learning behavior in work teams. Administrative Science Quarterly, 44(2), 350\u2013383. https://doi.org/10.2307/2666999',
        '[27] Bresciani, M. J., Gardner, M. M., & Hickmott, J. (2009). Demonstrating student success. Stylus Publishing.',
        '[28] Schein, E. H. (2010). Organizational culture and leadership (4th ed.). Jossey-Bass.',
        '[29] Swing, R. L., & Ross, L. E. (2016). A new vision for institutional research. Change, 48(2), 6\u201313. https://doi.org/10.1080/00091383.2016.1163132',
        '[30] Volkwein, J. F., Liu, Y., & Woodell, J. (2012). The structure and functions of institutional research offices. In The handbook of institutional research (pp. 22\u201339). Jossey-Bass.',
        '[31] Suskie, L. (2018). Assessing student learning: A common sense guide (3rd ed.). Jossey-Bass.',
        '[32] Siemens, G., & Long, P. (2011). Penetrating the fog: Analytics in learning and education. EDUCAUSE Review, 46(5), 30\u201332.',
        '[33] Banta, T. W., & Palomba, C. A. (2015). Assessment essentials (2nd ed.). Jossey-Bass.',
        '[34] Kezar, A., & Eckel, P. D. (2002). The effect of institutional culture on change strategies in higher education. The Journal of Higher Education, 73(4), 435\u2013460. https://doi.org/10.1353/jhe.2002.0038',
        '[35] Janis, I. L. (1982). Groupthink: Psychological studies of policy decisions and fiascoes (2nd ed.). Houghton Mifflin.',
        '[36] Kis, V. (2005). Quality assurance in tertiary education: Current practices in OECD countries. OECD Thematic Review of Tertiary Education.',
        '[37] Harvey, L. (2004). The power of accreditation: Views of academics. Journal of Higher Education Policy and Management, 26(2), 207\u2013223. https://doi.org/10.1080/1360080042000218267',
        '[38] Kinzie, J. (2010). Perspectives from campus leaders on student learning outcomes assessment. Assessment Update, 22(5), 1\u201315. https://doi.org/10.1002/au.225',
        '[39] Welsh, J. F., & Metcalf, J. (2003). Faculty and administrative support for institutional effectiveness activities. The Journal of Higher Education, 74(4), 445\u2013468. https://doi.org/10.1353/jhe.2003.0032',
        '[40] Baker, R. L. (2004). Keystones of regional accreditation. In Revisiting outcomes assessment in higher education (pp. 1\u201325). Libraries Unlimited.',
        '[41] Dickeson, R. C. (2010). Prioritizing academic programs and services (2nd ed.). Jossey-Bass.',
        '[42] Terenzini, P. T. (2013). On the nature of institutional research revisited. Research in Higher Education, 54(2), 137\u2013148. https://doi.org/10.1007/s11162-012-9274-3',
        '[43] Carey, K. (2012). A future of competency-based higher education. EDUCAUSE Review, 47(5), 68\u201369.',
        '[44] Laitinen, A. (2012). Cracking the credit hour. New America Foundation.',
        '[45] Pusser, B., Breneman, D. W., Gansneder, B. M., et al. (2007). Returning to learning: Adults\u2019 success in college is key to America\u2019s future. Lumina Foundation.',
        '[46] Baum, S., Ma, J., & Payea, K. (2013). Education pays 2013. The College Board.',
        '[47] Dill, D. D. (1999). Academic accountability and university adaptation. Higher Education, 38(2), 127\u2013154. https://doi.org/10.1023/A:1003762420723',
        '[48] Juran, J. M. (1989). Juran on leadership for quality: An executive handbook. Free Press.',
        '[49] Seymour, D. T. (1992). On Q: Causing quality in higher education. Macmillan.',
        '[50] Freed, J. E., Klugman, M. R., & Fife, J. D. (1997). A culture for academic excellence. ASHE-ERIC Higher Education Report, 25(1). ERIC Clearinghouse.',
        '[51] Birnbaum, R. (1988). How colleges work: The cybernetics of academic organization and leadership. Jossey-Bass.',
        '[52] Norris, D. M., & Baer, L. L. (2013). Building organizational capacity for analytics. EDUCAUSE.',
    ]

    for ref in references:
        paragraphs.append(make_ref_paragraph(ref))

    return paragraphs



def assemble_docx(output_path):
    """Assemble the complete .docx file with figures and tables."""
    
    # Generate figures
    print("Generating Figure 1...")
    fig1_data = create_figure1()
    print("Generating Figure 2...")
    fig2_data = create_figure2()
    print("Generating Figure 3...")
    fig3_data = create_figure3()
    
    # Build document paragraphs
    print("Building document content...")
    paragraphs = build_document()
    build_section1(paragraphs)
    build_section2(paragraphs)
    build_section3(paragraphs)
    build_conclusion_and_refs(paragraphs)
    
    # Create document.xml
    root = Element(ns('w', 'document'))
    root.set('xmlns:w', NSMAP['w'])
    root.set('xmlns:r', NSMAP['r'])
    root.set('xmlns:wp', NSMAP['wp'])
    root.set('xmlns:a', NSMAP['a'])
    root.set('xmlns:pic', NSMAP['pic'])
    
    body = SubElement(root, ns('w', 'body'))
    for p in paragraphs:
        body.append(p)
    
    # Section properties
    sectPr = SubElement(body, ns('w', 'sectPr'))
    pgSz = SubElement(sectPr, ns('w', 'pgSz'))
    pgSz.set(ns('w', 'w'), '12240')
    pgSz.set(ns('w', 'h'), '15840')
    pgMar = SubElement(sectPr, ns('w', 'pgMar'))
    pgMar.set(ns('w', 'top'), '1440')
    pgMar.set(ns('w', 'right'), '1440')
    pgMar.set(ns('w', 'bottom'), '1440')
    pgMar.set(ns('w', 'left'), '1440')
    pgMar.set(ns('w', 'header'), '720')
    pgMar.set(ns('w', 'footer'), '720')
    
    doc_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + tostring(root, encoding='unicode')
    
    # Create content types
    ct_root = Element('Types')
    ct_root.set('xmlns', 'http://schemas.openxmlformats.org/package/2006/content-types')
    for ext, ctype in [('rels', 'application/vnd.openxmlformats-package.relationships+xml'),
                       ('xml', 'application/xml'),
                       ('png', 'image/png')]:
        d = SubElement(ct_root, 'Default')
        d.set('Extension', ext)
        d.set('ContentType', ctype)
    for pn, ctype in [('/word/document.xml', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'),
                      ('/word/styles.xml', 'application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml'),
                      ('/word/settings.xml', 'application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml')]:
        o = SubElement(ct_root, 'Override')
        o.set('PartName', pn)
        o.set('ContentType', ctype)
    content_types_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + tostring(ct_root, encoding='unicode')
    
    # Create _rels/.rels
    rels_root = Element('Relationships')
    rels_root.set('xmlns', 'http://schemas.openxmlformats.org/package/2006/relationships')
    rel = SubElement(rels_root, 'Relationship')
    rel.set('Id', 'rId1')
    rel.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument')
    rel.set('Target', 'word/document.xml')
    rels_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + tostring(rels_root, encoding='unicode')
    
    # Create word/_rels/document.xml.rels (includes image relationships)
    word_rels_root = Element('Relationships')
    word_rels_root.set('xmlns', 'http://schemas.openxmlformats.org/package/2006/relationships')
    
    r1 = SubElement(word_rels_root, 'Relationship')
    r1.set('Id', 'rId1')
    r1.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles')
    r1.set('Target', 'styles.xml')
    
    r2 = SubElement(word_rels_root, 'Relationship')
    r2.set('Id', 'rId2')
    r2.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings')
    r2.set('Target', 'settings.xml')
    
    r3 = SubElement(word_rels_root, 'Relationship')
    r3.set('Id', 'rId3')
    r3.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image')
    r3.set('Target', 'media/figure1.png')
    
    r4 = SubElement(word_rels_root, 'Relationship')
    r4.set('Id', 'rId4')
    r4.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image')
    r4.set('Target', 'media/figure2.png')
    
    r5 = SubElement(word_rels_root, 'Relationship')
    r5.set('Id', 'rId5')
    r5.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image')
    r5.set('Target', 'media/figure3.png')
    
    word_rels_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + tostring(word_rels_root, encoding='unicode')
    
    # Create styles.xml
    styles_root = Element(ns('w', 'styles'))
    styles_root.set('xmlns:w', NSMAP['w'])
    styles_root.set('xmlns:r', NSMAP['r'])
    docDefaults = SubElement(styles_root, ns('w', 'docDefaults'))
    rPrDefault = SubElement(docDefaults, ns('w', 'rPrDefault'))
    rPr = SubElement(rPrDefault, ns('w', 'rPr'))
    rFonts = SubElement(rPr, ns('w', 'rFonts'))
    rFonts.set(ns('w', 'ascii'), 'Times New Roman')
    rFonts.set(ns('w', 'hAnsi'), 'Times New Roman')
    rFonts.set(ns('w', 'cs'), 'Times New Roman')
    sz = SubElement(rPr, ns('w', 'sz'))
    sz.set(ns('w', 'val'), '24')
    szCs = SubElement(rPr, ns('w', 'szCs'))
    szCs.set(ns('w', 'val'), '24')
    pPrDefault = SubElement(docDefaults, ns('w', 'pPrDefault'))
    pPr = SubElement(pPrDefault, ns('w', 'pPr'))
    spacing = SubElement(pPr, ns('w', 'spacing'))
    spacing.set(ns('w', 'line'), '480')
    spacing.set(ns('w', 'lineRule'), 'auto')
    # Styles
    for sid, sname, is_bold, sz_val, centered in [
        ('Normal', 'Normal', False, '24', False),
        ('Heading1', 'heading 1', True, '28', True),
        ('Heading2', 'heading 2', True, '24', False),
    ]:
        s = SubElement(styles_root, ns('w', 'style'))
        s.set(ns('w', 'type'), 'paragraph')
        s.set(ns('w', 'styleId'), sid)
        n = SubElement(s, ns('w', 'name'))
        n.set(ns('w', 'val'), sname)
        if centered:
            s_pPr = SubElement(s, ns('w', 'pPr'))
            s_jc = SubElement(s_pPr, ns('w', 'jc'))
            s_jc.set(ns('w', 'val'), 'center')
        if is_bold:
            s_rPr = SubElement(s, ns('w', 'rPr'))
            SubElement(s_rPr, ns('w', 'b'))
            s_sz = SubElement(s_rPr, ns('w', 'sz'))
            s_sz.set(ns('w', 'val'), sz_val)
    
    styles_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + tostring(styles_root, encoding='unicode')
    
    # Settings
    settings_root = Element(ns('w', 'settings'))
    settings_root.set('xmlns:w', NSMAP['w'])
    settings_root.set('xmlns:r', NSMAP['r'])
    settings_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + tostring(settings_root, encoding='unicode')
    
    # Write the .docx file
    print("Writing .docx file...")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types_xml)
        zf.writestr('_rels/.rels', rels_xml)
        zf.writestr('word/_rels/document.xml.rels', word_rels_xml)
        zf.writestr('word/document.xml', doc_xml)
        zf.writestr('word/styles.xml', styles_xml)
        zf.writestr('word/settings.xml', settings_xml)
        zf.writestr('word/media/figure1.png', fig1_data)
        zf.writestr('word/media/figure2.png', fig2_data)
        zf.writestr('word/media/figure3.png', fig3_data)
    
    print(f"\nCreated: {output_path}")
    print(f"File size: {os.path.getsize(output_path):,} bytes")
    
    # Verify
    with zipfile.ZipFile(output_path, 'r') as zf:
        print(f"Contents: {len(zf.namelist())} files")
        for name in zf.namelist():
            print(f"  {name} ({zf.getinfo(name).file_size:,} bytes)")


if __name__ == '__main__':
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'Chapter_Accreditation_Accountability_Learning_Renewal.docx')
    assemble_docx(output_file)
    print("\nDone! The document includes:")
    print("  - 3 Tables (one per section)")
    print("  - 3 Figures (one per section)")
    print("  - 52 numbered references in serial order")
    print("  - Times New Roman 12pt, double-spaced")
    print("  - All content in a single .docx file")
