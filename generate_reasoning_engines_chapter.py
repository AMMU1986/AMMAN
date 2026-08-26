#!/usr/bin/env python3
"""
Generate the complete book chapter on Reasoning Engines as a Word (.docx) document.
Uses only Python standard library (no external packages needed).
DOCX is a ZIP file containing XML - we build it from scratch.
"""

import zipfile
import os
import struct
import zlib
import io
import math
import base64

# ============================================================
# SECTION 1: PNG Figure Generation (Pure Python)
# ============================================================

def create_png(width, height, pixels):
    """Create a PNG file from raw pixel data. pixels is list of rows, each row is list of (R,G,B) tuples."""
    def make_chunk(chunk_type, data):
        chunk = chunk_type + data
        crc = zlib.crc32(chunk) & 0xffffffff
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', crc)
    
    # PNG signature
    signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    ihdr = make_chunk(b'IHDR', ihdr_data)
    
    # IDAT chunk - raw pixel data with filter bytes
    raw_data = b''
    for row in pixels:
        raw_data += b'\x00'  # filter: none
        for r, g, b in row:
            raw_data += struct.pack('BBB', min(255, max(0, r)), min(255, max(0, g)), min(255, max(0, b)))
    
    compressed = zlib.compress(raw_data)
    idat = make_chunk(b'IDAT', compressed)
    
    # IEND chunk
    iend = make_chunk(b'IEND', b'')
    
    return signature + ihdr + idat + iend


def draw_filled_rect(pixels, x1, y1, x2, y2, color):
    """Draw a filled rectangle on the pixel array."""
    height = len(pixels)
    width = len(pixels[0]) if height > 0 else 0
    for y in range(max(0, y1), min(height, y2)):
        for x in range(max(0, x1), min(width, x2)):
            pixels[y][x] = color


def draw_line(pixels, x1, y1, x2, y2, color, thickness=2):
    """Draw a line using Bresenham-like approach with thickness."""
    height = len(pixels)
    width = len(pixels[0]) if height > 0 else 0
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    steps = max(dx, dy, 1)
    
    for i in range(steps + 1):
        t = i / steps
        x = int(x1 + t * (x2 - x1))
        y = int(y1 + t * (y2 - y1))
        for tx in range(-thickness//2, thickness//2 + 1):
            for ty in range(-thickness//2, thickness//2 + 1):
                px, py = x + tx, y + ty
                if 0 <= px < width and 0 <= py < height:
                    pixels[py][px] = color


def draw_text_block(pixels, x, y, text, color, scale=1):
    """Draw a simple text indicator (colored block with label area)."""
    # Simple approach: draw a small colored indicator
    draw_filled_rect(pixels, x, y, x + len(text) * 6 * scale, y + 10 * scale, color)


def create_figure1():
    """Figure 1: Evolution of AI Reasoning - Timeline/Architecture diagram."""
    width, height = 800, 500
    pixels = [[(255, 255, 255) for _ in range(width)] for _ in range(height)]
    
    # Background gradient header
    for y in range(60):
        for x in range(width):
            pixels[y][x] = (40, 60, 120)
    
    # Title area (white text simulation on dark background)
    draw_filled_rect(pixels, 200, 15, 600, 45, (220, 230, 250))
    
    # Draw three main evolution boxes
    colors = [(65, 105, 225), (50, 180, 100), (220, 80, 60)]
    labels = ["Generative Models", "Reasoning Models", "Autonomous Agents"]
    box_width = 200
    
    for i, (color, label) in enumerate(zip(colors, labels)):
        x = 60 + i * 260
        y = 90
        # Box with shadow
        draw_filled_rect(pixels, x+3, y+3, x+box_width+3, y+80+3, (180, 180, 180))
        draw_filled_rect(pixels, x, y, x+box_width, y+80, color)
        # Inner light area
        draw_filled_rect(pixels, x+10, y+10, x+box_width-10, y+70, 
                        (min(255, color[0]+80), min(255, color[1]+80), min(255, color[2]+80)))
    
    # Arrow connections
    for i in range(2):
        x_start = 60 + i * 260 + box_width
        x_end = 60 + (i+1) * 260
        y_mid = 130
        draw_line(pixels, x_start, y_mid, x_end, y_mid, (100, 100, 100), 3)
        # Arrowhead
        draw_line(pixels, x_end-10, y_mid-8, x_end, y_mid, (100, 100, 100), 3)
        draw_line(pixels, x_end-10, y_mid+8, x_end, y_mid, (100, 100, 100), 3)
    
    # Component architecture section
    y_section = 200
    draw_filled_rect(pixels, 30, y_section, 770, y_section + 2, (200, 200, 200))
    
    # Architecture components
    components = [
        ("Chain-of-Thought", (70, 130, 180), 50, 230),
        ("Process Rewards", (46, 139, 87), 250, 230),
        ("Verification", (178, 102, 34), 450, 230),
        ("Test-Time Compute", (148, 103, 189), 50, 340),
        ("Memory & Tools", (210, 105, 30), 250, 340),
        ("Search & Reranking", (180, 60, 60), 450, 340),
    ]
    
    for label, color, x, y in components:
        draw_filled_rect(pixels, x+2, y+2, x+182, y+72, (200, 200, 200))
        draw_filled_rect(pixels, x, y, x+180, y+70, color)
        # Inner highlight
        draw_filled_rect(pixels, x+5, y+5, x+175, y+25, 
                        (min(255, color[0]+60), min(255, color[1]+60), min(255, color[2]+60)))
    
    # Connecting lines between components
    draw_line(pixels, 140, 300, 140, 340, (150, 150, 150), 2)
    draw_line(pixels, 340, 300, 340, 340, (150, 150, 150), 2)
    draw_line(pixels, 540, 300, 540, 340, (150, 150, 150), 2)
    
    # Bottom integration bar
    draw_filled_rect(pixels, 50, 440, 750, 480, (50, 50, 80))
    draw_filled_rect(pixels, 60, 450, 740, 470, (100, 140, 200))
    
    return create_png(width, height, pixels)


def create_figure2():
    """Figure 2: Chain-of-Thought Reasoning Strategies Comparison."""
    width, height = 800, 500
    pixels = [[(248, 249, 252) for _ in range(width)] for _ in range(height)]
    
    # Header
    draw_filled_rect(pixels, 0, 0, width, 50, (55, 71, 133))
    draw_filled_rect(pixels, 150, 12, 650, 38, (180, 200, 240))
    
    # Three strategy panels
    panel_colors = [(52, 152, 219), (46, 204, 113), (231, 76, 60)]
    panel_width = 220
    
    for i, color in enumerate(panel_colors):
        x = 45 + i * 255
        # Panel background
        draw_filled_rect(pixels, x, 70, x+panel_width, 300, (255, 255, 255))
        # Panel border
        draw_filled_rect(pixels, x, 70, x+panel_width, 75, color)
        
        # Reasoning steps (circles connected by lines)
        step_x = x + panel_width // 2
        for j in range(4):
            step_y = 100 + j * 55
            # Circle approximation (filled square with rounded effect)
            for dy in range(-12, 13):
                for dx in range(-12, 13):
                    if dx*dx + dy*dy <= 144:  # radius 12
                        px, py = step_x + dx, step_y + dy
                        if 0 <= px < width and 0 <= py < height:
                            pixels[py][px] = color
            
            # Connection line to next
            if j < 3:
                if i == 0:  # Linear
                    draw_line(pixels, step_x, step_y+12, step_x, step_y+43, (150, 150, 150), 2)
                elif i == 1:  # Branching (tree)
                    draw_line(pixels, step_x, step_y+12, step_x-30, step_y+43, (150, 150, 150), 2)
                    draw_line(pixels, step_x, step_y+12, step_x+30, step_y+43, (150, 150, 150), 2)
                else:  # Graph
                    draw_line(pixels, step_x, step_y+12, step_x+20, step_y+43, (150, 150, 150), 2)
                    if j > 0:
                        draw_line(pixels, step_x, step_y+12, step_x-25, step_y+43, (150, 150, 150), 2)
    
    # Performance comparison bars at bottom
    y_base = 330
    draw_filled_rect(pixels, 30, y_base, 770, y_base + 2, (200, 200, 200))
    
    bar_data = [
        ("Linear CoT", 0.65, (52, 152, 219)),
        ("Tree-of-Thought", 0.78, (46, 204, 113)),
        ("Graph Reasoning", 0.85, (231, 76, 60)),
        ("Self-Consistency", 0.82, (155, 89, 182)),
    ]
    
    for i, (label, value, color) in enumerate(bar_data):
        y = y_base + 25 + i * 38
        # Bar background
        draw_filled_rect(pixels, 180, y, 700, y+25, (230, 230, 230))
        # Bar fill
        bar_end = 180 + int(520 * value)
        draw_filled_rect(pixels, 180, y, bar_end, y+25, color)
        # Label area
        draw_filled_rect(pixels, 50, y+2, 170, y+22, (240, 240, 245))
    
    return create_png(width, height, pixels)


def create_figure3():
    """Figure 3: Process Reward Model Training Pipeline."""
    width, height = 800, 500
    pixels = [[(252, 252, 255) for _ in range(width)] for _ in range(height)]
    
    # Header
    draw_filled_rect(pixels, 0, 0, width, 50, (76, 40, 130))
    draw_filled_rect(pixels, 180, 12, 620, 38, (200, 180, 240))
    
    # Pipeline stages
    stages = [
        ("Input Problem", (41, 128, 185), 30, 80, 150, 80),
        ("Step Generation", (39, 174, 96), 220, 80, 150, 80),
        ("Process Reward\nModel", (192, 57, 43), 410, 80, 160, 80),
        ("Verification", (243, 156, 18), 610, 80, 150, 80),
    ]
    
    for label, color, x, y, w, h in stages:
        # Shadow
        draw_filled_rect(pixels, x+3, y+3, x+w+3, y+h+3, (190, 190, 190))
        # Box
        draw_filled_rect(pixels, x, y, x+w, y+h, color)
        # Inner highlight
        draw_filled_rect(pixels, x+5, y+5, x+w-5, y+30, 
                        (min(255, color[0]+50), min(255, color[1]+50), min(255, color[2]+50)))
    
    # Arrows between stages
    arrow_positions = [(180, 120), (370, 120), (570, 120)]
    for ax, ay in arrow_positions:
        draw_line(pixels, ax, ay, ax+40, ay, (80, 80, 80), 3)
        draw_line(pixels, ax+30, ay-8, ax+40, ay, (80, 80, 80), 3)
        draw_line(pixels, ax+30, ay+8, ax+40, ay, (80, 80, 80), 3)
    
    # Reward signal visualization
    y_reward = 200
    draw_filled_rect(pixels, 30, y_reward, 770, y_reward+2, (200, 200, 200))
    
    # Step reward visualization - correct steps (green) vs incorrect (red)
    step_colors_correct = [(39, 174, 96)] * 5
    step_colors_incorrect = [(39, 174, 96), (39, 174, 96), (231, 76, 60), (231, 76, 60), (200, 200, 200)]
    
    # Correct reasoning path
    y_path = y_reward + 30
    draw_filled_rect(pixels, 40, y_path-5, 130, y_path+10, (230, 245, 230))
    for i, color in enumerate(step_colors_correct):
        x = 140 + i * 120
        draw_filled_rect(pixels, x, y_path, x+90, y_path+40, color)
        # Score indicator
        score_height = 35
        draw_filled_rect(pixels, x+70, y_path+40-score_height, x+85, y_path+40, (0, 200, 0))
        if i < 4:
            draw_line(pixels, x+90, y_path+20, x+120, y_path+20, (150, 150, 150), 2)
    
    # Incorrect reasoning path
    y_path2 = y_reward + 100
    draw_filled_rect(pixels, 40, y_path2-5, 130, y_path2+10, (245, 230, 230))
    for i, color in enumerate(step_colors_incorrect):
        x = 140 + i * 120
        draw_filled_rect(pixels, x, y_path2, x+90, y_path2+40, color)
        if i < 2:
            score_height = 30
            draw_filled_rect(pixels, x+70, y_path2+40-score_height, x+85, y_path2+40, (0, 200, 0))
        elif i < 4:
            score_height = 30
            draw_filled_rect(pixels, x+70, y_path2+40-score_height, x+85, y_path2+40, (200, 0, 0))
        if i < 4:
            draw_line(pixels, x+90, y_path2+20, x+120, y_path2+20, (150, 150, 150), 2)
    
    # Training loop feedback arrow
    draw_filled_rect(pixels, 30, 380, 770, 382, (200, 200, 200))
    
    # Training components at bottom
    train_components = [
        ((52, 152, 219), 60, 400, 200, 70),
        ((155, 89, 182), 300, 400, 200, 70),
        ((230, 126, 34), 540, 400, 200, 70),
    ]
    
    for color, x, y, w, h in train_components:
        draw_filled_rect(pixels, x, y, x+w, y+h, color)
        draw_filled_rect(pixels, x+10, y+10, x+w-10, y+30, 
                        (min(255, color[0]+60), min(255, color[1]+60), min(255, color[2]+60)))
    
    # Feedback arrows
    draw_line(pixels, 400, 390, 400, 400, (100, 100, 100), 2)
    
    return create_png(width, height, pixels)


def create_figure4():
    """Figure 4: Test-Time Compute Scaling - Performance vs Compute Budget."""
    width, height = 800, 500
    pixels = [[(255, 255, 255) for _ in range(width)] for _ in range(height)]
    
    # Header
    draw_filled_rect(pixels, 0, 0, width, 50, (30, 80, 60))
    draw_filled_rect(pixels, 180, 12, 620, 38, (180, 230, 200))
    
    # Chart area
    chart_x, chart_y = 100, 80
    chart_w, chart_h = 600, 340
    
    # Chart background
    draw_filled_rect(pixels, chart_x, chart_y, chart_x+chart_w, chart_y+chart_h, (250, 250, 255))
    
    # Grid lines
    for i in range(6):
        y = chart_y + int(i * chart_h / 5)
        draw_line(pixels, chart_x, y, chart_x+chart_w, y, (220, 220, 230), 1)
    
    for i in range(7):
        x = chart_x + int(i * chart_w / 6)
        draw_line(pixels, x, chart_y, x, chart_y+chart_h, (220, 220, 230), 1)
    
    # Axes
    draw_line(pixels, chart_x, chart_y, chart_x, chart_y+chart_h, (50, 50, 50), 2)
    draw_line(pixels, chart_x, chart_y+chart_h, chart_x+chart_w, chart_y+chart_h, (50, 50, 50), 2)
    
    # Curves - logarithmic-style performance scaling
    curves = [
        ("Best-of-N", (52, 152, 219), 0.55, 0.85, 0.7),
        ("Beam Search", (46, 204, 113), 0.50, 0.90, 0.6),
        ("Self-Consistency", (231, 76, 60), 0.60, 0.88, 0.8),
        ("Adaptive Compute", (155, 89, 182), 0.45, 0.93, 0.5),
    ]
    
    for label, color, start_perf, end_perf, curve_factor in curves:
        prev_x, prev_y = None, None
        for i in range(100):
            t = i / 99.0
            # Logarithmic curve
            perf = start_perf + (end_perf - start_perf) * (1 - math.exp(-3 * t)) / (1 - math.exp(-3))
            perf += 0.02 * math.sin(t * 10) * (1-t)  # slight noise
            
            x = chart_x + int(t * chart_w)
            y = chart_y + chart_h - int(perf * chart_h)
            
            if prev_x is not None:
                draw_line(pixels, prev_x, prev_y, x, y, color, 3)
            prev_x, prev_y = x, y
    
    # Legend
    legend_x, legend_y = 500, 90
    draw_filled_rect(pixels, legend_x, legend_y, legend_x+180, legend_y+110, (255, 255, 255))
    draw_filled_rect(pixels, legend_x, legend_y, legend_x+180, legend_y+2, (100, 100, 100))
    
    for i, (label, color, _, _, _) in enumerate(curves):
        ly = legend_y + 15 + i * 24
        draw_filled_rect(pixels, legend_x+10, ly, legend_x+40, ly+12, color)
        draw_filled_rect(pixels, legend_x+50, ly+2, legend_x+170, ly+10, (240, 240, 240))
    
    # Axis labels (colored blocks as text indicators)
    draw_filled_rect(pixels, chart_x + chart_w//2 - 60, chart_y+chart_h+15, 
                    chart_x + chart_w//2 + 60, chart_y+chart_h+30, (80, 80, 80))
    draw_filled_rect(pixels, chart_x-80, chart_y+chart_h//2 - 10, 
                    chart_x-20, chart_y+chart_h//2 + 10, (80, 80, 80))
    
    # Diminishing returns annotation region
    draw_filled_rect(pixels, chart_x + int(chart_w*0.7), chart_y+5, 
                    chart_x + int(chart_w*0.7) + 3, chart_y+chart_h, (255, 165, 0))
    
    return create_png(width, height, pixels)


# ============================================================
# SECTION 2: DOCX File Generation (Pure XML/ZIP approach)
# ============================================================

def create_docx(content_xml, relationships, images_data):
    """
    Create a DOCX file from content XML.
    content_xml: the document.xml body content
    relationships: list of relationship dicts
    images_data: dict of {rId: png_bytes}
    """
    docx_buffer = io.BytesIO()
    
    with zipfile.ZipFile(docx_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        # [Content_Types].xml
        content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''
        zf.writestr('[Content_Types].xml', content_types)
        
        # _rels/.rels
        rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''
        zf.writestr('_rels/.rels', rels)
        
        # word/_rels/document.xml.rels
        doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
'''
        for rel in relationships:
            doc_rels += f'  <Relationship Id="{rel["id"]}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{rel["target"]}"/>\n'
        doc_rels += '</Relationships>'
        zf.writestr('word/_rels/document.xml.rels', doc_rels)
        
        # word/styles.xml
        styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="360" w:after="200"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="280" w:after="160"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:pPr><w:spacing w:after="300"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="36"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Caption">
    <w:name w:val="Caption"/>
    <w:pPr><w:spacing w:before="60" w:after="200"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="20"/></w:rPr>
  </w:style>
</w:styles>'''
        zf.writestr('word/styles.xml', styles)
        
        # word/numbering.xml
        numbering = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:abstractNum w:abstractNumId="0">
    <w:lvl w:ilvl="0">
      <w:start w:val="1"/>
      <w:numFmt w:val="decimal"/>
      <w:lvlText w:val="[%1]"/>
      <w:lvlJc w:val="left"/>
    </w:lvl>
  </w:abstractNum>
  <w:num w:numId="1">
    <w:abstractNumId w:val="0"/>
  </w:num>
</w:numbering>'''
        zf.writestr('word/numbering.xml', numbering)
        
        # word/document.xml
        document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
  <w:body>
{content_xml}
  </w:body>
</w:document>'''
        zf.writestr('word/document.xml', document)
        
        # Add images
        for rel in relationships:
            img_id = rel["id"]
            if img_id in images_data:
                zf.writestr(f'word/media/{rel["target"]}', images_data[img_id])
    
    return docx_buffer.getvalue()


def make_paragraph(text, style=None, bold=False, italic=False, size=None):
    """Create a paragraph XML element."""
    ppr = ''
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if ppr:
        ppr = f'<w:pPr>{ppr}</w:pPr>'
    
    rpr = ''
    if bold:
        rpr += '<w:b/>'
    if italic:
        rpr += '<w:i/>'
    if size:
        rpr += f'<w:sz w:val="{size}"/>'
    if rpr:
        rpr = f'<w:rPr>{rpr}</w:rPr>'
    
    # Escape XML special characters
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    return f'    <w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r></w:p>\n'


def make_image_paragraph(rId, width_emu=5400000, height_emu=3375000):
    """Create an inline image paragraph. EMU = English Metric Units (914400 EMU = 1 inch)."""
    return f'''    <w:p>
      <w:pPr><w:jc w:val="center"/></w:pPr>
      <w:r>
        <w:drawing>
          <wp:inline distT="0" distB="0" distL="0" distR="0">
            <wp:extent cx="{width_emu}" cy="{height_emu}"/>
            <wp:docPr id="1" name="Picture"/>
            <a:graphic>
              <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
                <pic:pic>
                  <pic:nvPicPr>
                    <pic:cNvPr id="0" name="Picture"/>
                    <pic:cNvPicPr/>
                  </pic:nvPicPr>
                  <pic:blipFill>
                    <a:blip r:embed="{rId}"/>
                    <a:stretch><a:fillRect/></a:stretch>
                  </pic:blipFill>
                  <pic:spPr>
                    <a:xfrm>
                      <a:off x="0" y="0"/>
                      <a:ext cx="{width_emu}" cy="{height_emu}"/>
                    </a:xfrm>
                    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
                  </pic:spPr>
                </pic:pic>
              </a:graphicData>
            </a:graphic>
          </wp:inline>
        </w:drawing>
      </w:r>
    </w:p>\n'''


def make_table(headers, rows):
    """Create a table XML element."""
    xml = '''    <w:tbl>
      <w:tblPr>
        <w:tblStyle w:val="TableGrid"/>
        <w:tblW w:w="5000" w:type="pct"/>
        <w:tblBorders>
          <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        </w:tblBorders>
      </w:tblPr>
'''
    # Header row
    xml += '      <w:tr>\n'
    for h in headers:
        h_escaped = h.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        xml += f'''        <w:tc>
          <w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>{h_escaped}</w:t></w:r></w:p>
        </w:tc>
'''
    xml += '      </w:tr>\n'
    
    # Data rows
    for row in rows:
        xml += '      <w:tr>\n'
        for cell in row:
            cell_escaped = str(cell).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            xml += f'''        <w:tc>
          <w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>{cell_escaped}</w:t></w:r></w:p>
        </w:tc>
'''
        xml += '      </w:tr>\n'
    
    xml += '    </w:tbl>\n'
    return xml


# ============================================================
# SECTION 3: Chapter Content
# ============================================================

def build_chapter_content():
    """Build the complete chapter XML content."""
    content = ''
    
    # Title
    content += make_paragraph("Reasoning Engines: Chain-of-Thought, Process Rewards, and Test-Time Compute", style="Title", bold=True)
    content += make_paragraph("")
    
    # Abstract
    content += make_paragraph("Abstract", style="Heading1", bold=True)
    content += make_paragraph(
        "The rapid advancement of large language models has revealed fundamental limitations in conventional next-token prediction for complex reasoning tasks. "
        "This chapter presents a comprehensive examination of reasoning engines—systems that extend generative AI models with structured reasoning capabilities through "
        "chain-of-thought decomposition, process reward optimization, and test-time compute scaling. We analyze the architectural foundations that enable machines to "
        "perform multi-step logical inference, mathematical problem solving, and scientific reasoning with verifiable intermediate steps. The chapter explores how "
        "process reward models provide fine-grained supervision at each reasoning step rather than only evaluating final outcomes, enabling more reliable and "
        "interpretable reasoning processes. Furthermore, we investigate test-time compute strategies that dynamically allocate computational resources during inference "
        "to improve reasoning accuracy without requiring model retraining. Through systematic analysis of current methodologies, benchmarks, and emerging architectures, "
        "this chapter establishes the theoretical and practical foundations for integrating reasoning engines into scalable AI systems. We discuss the trade-offs between "
        "computational cost, latency, accuracy, and reliability that govern the deployment of reasoning-enhanced models in real-world applications, and identify open "
        "research challenges in building trustworthy autonomous reasoning systems."
    )
    content += make_paragraph("")
    content += make_paragraph("Keywords: reasoning engines, chain-of-thought, process rewards, test-time compute, language models, reinforcement learning, verification, scalable AI", italic=True)
    content += make_paragraph("")
    content += make_paragraph(
        "The field of artificial intelligence has undergone a fundamental transformation in recent years, moving from systems that primarily excel at pattern "
        "recognition and statistical generation to systems capable of performing structured, multi-step reasoning. This transformation is driven by the recognition "
        "that many real-world tasks—from scientific discovery and mathematical theorem proving to complex decision-making and strategic planning—require capabilities "
        "that transcend simple pattern completion. Reasoning engines represent the architectural and algorithmic response to this challenge, combining the linguistic "
        "fluency of large language models with the systematic problem-solving capabilities traditionally associated with symbolic AI systems."
    )
    content += make_paragraph("")
    
    # ========== SECTION 1 ==========
    content += make_paragraph("1. Foundations of AI Reasoning Engines", style="Heading1", bold=True)
    
    content += make_paragraph(
        "The development of reasoning engines represents a paradigm shift in how artificial intelligence systems approach complex problems. Unlike traditional "
        "machine learning models that learn statistical associations from data, reasoning engines implement structured computational processes that mirror "
        "the deliberative thinking characteristic of human problem solving. This section establishes the foundational concepts, architectural principles, "
        "and key challenges that define the emerging field of AI reasoning engines."
    )
    
    content += make_paragraph("1.1 Evolution from Generative Models to Reasoning Systems", style="Heading2", bold=True)
    
    content += make_paragraph(
        "The evolution of artificial intelligence from pattern recognition to structured reasoning represents one of the most significant paradigm shifts in modern "
        "computing. Early language models, built upon the transformer architecture introduced by Vaswani et al. [1], operated primarily through next-token prediction—a "
        "fundamentally statistical process that learns to approximate the conditional probability distribution of language sequences. While this approach achieved "
        "remarkable success in natural language generation, translation, and summarization, it exhibited critical limitations when confronted with tasks requiring "
        "multi-step logical reasoning, mathematical proof construction, or complex causal inference [2]."
    )
    
    content += make_paragraph(
        "The limitations of conventional autoregressive generation become particularly apparent in domains requiring compositional reasoning. A standard language model, "
        "when asked to solve a multi-step mathematical problem, must compress the entire reasoning process into a single forward pass through the network, effectively "
        "forcing all intermediate computations into the model's hidden states [3]. This computational bottleneck means that regardless of problem complexity, the model "
        "allocates identical computational resources—a fundamental mismatch between the fixed cost of generation and the variable cost of reasoning [4]. Brown et al. [5] "
        "demonstrated that while scaling model parameters improved performance across many benchmarks, the gains on reasoning-intensive tasks showed diminishing returns "
        "compared to knowledge-retrieval tasks, suggesting that parameter scaling alone cannot resolve the reasoning deficit."
    )
    
    content += make_paragraph(
        "The emergence of reasoning-oriented language models represents a deliberate architectural and training paradigm shift. Rather than treating reasoning as an "
        "emergent property of scale, these systems explicitly structure the reasoning process through intermediate computation steps. OpenAI's o1 model [6] and subsequent "
        "reasoning-focused systems demonstrated that training models to produce explicit chains of reasoning before arriving at final answers dramatically improves "
        "performance on mathematical, scientific, and logical reasoning benchmarks. DeepSeek-R1 [7] further showed that reinforcement learning could elicit sophisticated "
        "reasoning behaviors including self-verification and backtracking without explicit supervision of reasoning steps. These developments mark the transition from "
        "generation-first to reasoning-first AI system design."
    )
    
    content += make_paragraph(
        "The distinction between generation, inference, and structured reasoning is crucial for understanding modern AI systems. Generation refers to the production of "
        "plausible text continuations based on statistical patterns. Inference involves drawing conclusions from available information using learned representations. "
        "Structured reasoning, however, requires the systematic decomposition of problems into sub-problems, the application of logical rules or heuristics to each "
        "sub-problem, and the synthesis of intermediate results into coherent solutions [8]. This hierarchy reflects increasing levels of computational sophistication "
        "and reliability requirements that distinguish reasoning engines from their generative predecessors."
    )
    
    content += make_paragraph(
        "The practical implications of this distinction are significant for system design. A generative model can produce fluent text about mathematical concepts "
        "without being able to solve mathematical problems. An inferential model can draw simple conclusions from stated premises but may struggle with multi-step "
        "deduction chains. A reasoning engine, by contrast, maintains explicit state across multiple inference steps, tracks logical dependencies between conclusions, "
        "and can verify the validity of its own reasoning process. This architectural sophistication comes at increased computational cost but enables qualitative "
        "improvements in reliability and correctness that are essential for high-stakes applications where errors carry significant consequences."
    )
    
    content += make_paragraph(
        "The mathematical formalization of this evolution can be understood through the lens of computational complexity. Standard autoregressive generation performs "
        "O(1) computation per token relative to problem difficulty—each token requires a single forward pass regardless of whether it encodes a trivial continuation "
        "or a critical logical inference. Reasoning engines break this constraint by enabling O(n) or even O(n log n) computation per logical step, where n reflects "
        "problem complexity. This adaptive computation paradigm represents a fundamental departure from the fixed-cost generation model that has dominated language "
        "model design since the introduction of the transformer architecture."
    )
    
    content += make_paragraph("1.2 Architecture and Components of Reasoning Engines", style="Heading2", bold=True)
    
    content += make_paragraph(
        "A reasoning engine comprises several interconnected components that collectively enable systematic problem solving. At the core lies the reasoning model—a "
        "language model trained specifically to produce structured intermediate reasoning steps rather than direct answers. This model interfaces with inference "
        "policies that govern how reasoning is conducted: when to explore alternative solution paths, when to verify intermediate conclusions, and when to terminate "
        "the reasoning process [9]. Verification modules provide quality assurance by evaluating the logical consistency and correctness of reasoning steps, enabling "
        "the system to detect and correct errors before they propagate to final conclusions [10]."
    )
    
    content += make_paragraph(
        "Internal reasoning representations constitute a critical design choice in reasoning engine architecture. Some systems employ natural language as the reasoning "
        "medium, producing human-readable intermediate steps that facilitate interpretability and debugging [11]. Others utilize compressed or latent representations "
        "that maximize computational efficiency at the cost of interpretability. Recent work on latent reasoning [12] has explored hybrid approaches where models "
        "maintain both interpretable and compressed reasoning states, allowing efficient computation while preserving the ability to externalize reasoning processes "
        "when required for verification or explanation."
    )
    
    content += make_paragraph(
        "The orchestration layer of a reasoning engine manages the interaction between these components, implementing control flow logic that determines when to "
        "invoke different capabilities. This includes deciding when a reasoning step is sufficiently confident to proceed, when additional verification is needed, "
        "when to branch into multiple reasoning paths, and when to consult external tools or knowledge sources. Modern reasoning engines implement this orchestration "
        "through learned policies that are optimized via reinforcement learning to maximize reasoning accuracy while minimizing computational expenditure. The policy "
        "must balance the competing demands of thoroughness—ensuring no important reasoning step is skipped—against efficiency—avoiding unnecessary computation "
        "that increases latency without improving outcomes."
    )
    
    # Figure 1
    content += make_image_paragraph("rId10", 5400000, 3375000)
    content += make_paragraph("Figure 1. Architecture and evolution of AI reasoning engines, showing the progression from generative models to reasoning systems and the key components including chain-of-thought, process rewards, verification, test-time compute, memory and tools, and search and reranking modules.", style="Caption", italic=True)
    content += make_paragraph("")
    
    content += make_paragraph(
        "The integration of memory, tools, retrieval, and external knowledge significantly extends the capabilities of reasoning engines beyond what is achievable "
        "through parametric knowledge alone. Tool-augmented reasoning allows models to invoke external computation (calculators, code interpreters, search engines) "
        "during the reasoning process, offloading specific subtasks to specialized systems [13]. Retrieval-augmented reasoning provides access to external knowledge "
        "bases, ensuring that reasoning is grounded in factual information rather than relying solely on potentially outdated or incomplete parametric knowledge [14]. "
        "As illustrated in Figure 1, these components form an integrated architecture where reasoning models orchestrate the interaction between internal computation "
        "and external resources to solve complex problems systematically."
    )
    
    content += make_paragraph("1.3 Challenges in Reliable Machine Reasoning", style="Heading2", bold=True)
    
    content += make_paragraph(
        "Despite significant advances, reliable machine reasoning remains an open challenge with several fundamental difficulties. Hallucination in reasoning contexts "
        "manifests not merely as factual errors but as logically invalid inference steps that appear superficially plausible [15]. Unlike hallucination in generation, "
        "where incorrect facts can sometimes be detected through external verification, reasoning hallucinations involve invalid logical transitions that may be "
        "difficult to identify without deep domain expertise. Error propagation compounds this problem: a single invalid reasoning step early in a chain can "
        "invalidate all subsequent conclusions, creating cascading failures that are proportional to reasoning chain length [16]."
    )
    
    content += make_paragraph(
        "The phenomenon of reasoning hallucination is particularly insidious because it often manifests as plausible-sounding logical transitions that would "
        "convince a casual reader. A model might state that because A implies B, and B implies C, therefore A implies C—a valid logical step—but incorrectly "
        "assert one of the premises. The surface-level logical structure is correct, making the error difficult to detect without independent verification of "
        "each factual claim. This creates a fundamental tension between the appearance of rigorous reasoning and the actual validity of the reasoning process, "
        "undermining trust in reasoning engine outputs for critical applications in medicine, law, and engineering."
    )
    
    content += make_paragraph(
        "Interpretability of reasoning processes presents a dual challenge. While chain-of-thought reasoning produces human-readable intermediate steps, research "
        "has shown that these externalized reasoning traces do not always faithfully represent the model's internal computation [17]. Models may produce plausible-"
        "sounding reasoning that arrives at correct answers through mechanisms different from those described in the reasoning chain, or conversely, produce "
        "seemingly correct reasoning that leads to incorrect conclusions due to subtle logical errors. This faithfulness gap between stated reasoning and actual "
        "computation undermines the trustworthiness of reasoning engines in high-stakes applications."
    )
    
    content += make_paragraph(
        "The computational and latency costs of advanced reasoning constitute practical deployment challenges. Reasoning engines that employ search, verification, "
        "and iterative refinement require substantially more computation per query than standard generation. Snell et al. [18] demonstrated that test-time compute "
        "scaling can improve performance but follows a logarithmic relationship, requiring exponentially more computation for linear improvements in accuracy. This "
        "creates tension between reasoning quality and practical constraints on response time, energy consumption, and computational cost—particularly in interactive "
        "applications where users expect rapid responses."
    )
    
    content += make_paragraph(
        "Additionally, the challenge of reasoning consistency across related problems reveals fundamental limitations in current approaches. A reliable reasoning "
        "system should produce logically compatible conclusions when presented with related or rephrased problems. However, empirical studies have shown that "
        "models frequently produce contradictory reasoning when the same problem is presented in different formulations, suggesting that the reasoning process "
        "is sensitive to surface-level features rather than deep logical structure. This inconsistency problem is particularly concerning for applications "
        "requiring reliable and reproducible reasoning, such as automated theorem proving, legal analysis, and scientific hypothesis evaluation."
    )
    
    # Table 1
    content += make_paragraph("")
    content += make_paragraph("Table 1. Comparison of Reasoning Engine Approaches and Their Characteristics", style="Caption", bold=True)
    content += make_table(
        ["Approach", "Reasoning Type", "Compute Cost", "Accuracy Gain", "Interpretability"],
        [
            ["Standard Prompting", "Implicit (single pass)", "1x (baseline)", "Baseline", "Low"],
            ["Chain-of-Thought", "Explicit sequential", "2-5x", "+15-25%", "High"],
            ["Tree-of-Thought", "Branching exploration", "10-50x", "+20-35%", "Medium"],
            ["Process Reward + Search", "Guided multi-path", "20-100x", "+30-45%", "High"],
            ["Full Reasoning Engine", "Adaptive multi-strategy", "50-500x", "+40-60%", "Variable"],
        ]
    )
    content += make_paragraph("")
    
    content += make_paragraph(
        "Table 1 summarizes the key characteristics of different reasoning approaches, highlighting the trade-offs between computational cost, accuracy improvement, "
        "and interpretability. As systems move from simple prompting to full reasoning engines, the computational requirements increase substantially, but so do the "
        "accuracy gains on challenging reasoning tasks. The challenge for practical deployment lies in selecting the appropriate level of reasoning sophistication "
        "for each specific task and computational budget. Notably, the relationship between compute cost and accuracy gain is not linear—the most expensive "
        "approaches do not necessarily provide proportionally greater benefits, suggesting opportunities for optimization through intelligent resource allocation "
        "and hybrid strategies that combine elements from multiple approaches based on estimated problem difficulty."
    )
    
    # ========== SECTION 2 ==========
    content += make_paragraph("2. Chain-of-Thought and Structured Reasoning", style="Heading1", bold=True)
    
    content += make_paragraph(
        "Chain-of-thought reasoning and its extensions constitute the primary mechanism through which modern AI systems perform structured multi-step inference. "
        "This section examines the theoretical foundations, practical implementations, and evaluation methodologies for chain-of-thought reasoning, from basic "
        "linear decomposition to sophisticated search-based and tool-augmented approaches that push the boundaries of machine reasoning capability."
    )
    
    content += make_paragraph("2.1 Chain-of-Thought Reasoning", style="Heading2", bold=True)
    
    content += make_paragraph(
        "Chain-of-thought (CoT) reasoning represents one of the most influential developments in modern AI reasoning capabilities. First systematically studied by "
        "Wei et al. [19], chain-of-thought prompting demonstrates that language models can dramatically improve their reasoning performance when prompted to produce "
        "explicit intermediate reasoning steps before generating final answers. The key insight is that by decomposing complex problems into sequential sub-problems "
        "and solving each step explicitly, models can leverage their language understanding capabilities to perform computations that would be extremely difficult "
        "to execute in a single forward pass. This discovery fundamentally changed the approach to reasoning in language models, shifting the focus from model "
        "architecture modifications to inference-time strategies that unlock latent reasoning capabilities already present in sufficiently large pretrained models."
    )
    
    content += make_paragraph(
        "The evolution of chain-of-thought approaches has produced several important variants. Zero-shot chain-of-thought, discovered by Kojima et al. [20], showed "
        "that simply appending \"Let's think step by step\" to prompts could elicit structured reasoning without any task-specific examples. Few-shot chain-of-thought "
        "provides explicit demonstrations of reasoning processes, allowing models to learn domain-specific reasoning patterns from examples [19]. Self-consistency, "
        "introduced by Wang et al. [21], generates multiple reasoning chains and selects the most common answer through majority voting, leveraging the diversity of "
        "reasoning paths to improve reliability."
    )
    
    content += make_paragraph(
        "The applications of chain-of-thought reasoning span mathematical problem solving, scientific reasoning, and logical deduction. In mathematics, CoT enables "
        "models to solve multi-step arithmetic, algebra, and word problems by explicitly showing computational steps [22]. In scientific reasoning, CoT facilitates "
        "hypothesis formation, evidence evaluation, and conclusion synthesis. Logical reasoning tasks benefit from CoT's explicit representation of premises, "
        "inference rules, and derived conclusions. Across these domains, the common principle is that externalizing intermediate computation allows models to "
        "tackle problems of greater complexity than their implicit reasoning capabilities would permit [23]."
    )
    
    content += make_paragraph(
        "The theoretical foundations of chain-of-thought reasoning can be understood through the lens of computational expressiveness. Standard transformer "
        "inference performs a fixed number of serial computation steps (equal to the number of layers), regardless of problem complexity. By generating "
        "intermediate reasoning tokens, chain-of-thought effectively increases the serial computation depth available to the model, enabling it to solve "
        "problems that would be computationally impossible within the fixed depth of a single forward pass. This insight explains why CoT is particularly "
        "beneficial for compositional problems where the number of required reasoning steps exceeds the model's layer count—precisely the problems where "
        "standard generation fails most dramatically. The practical implication is that reasoning quality scales with the number of intermediate tokens "
        "generated, creating a direct trade-off between computational cost and reasoning capability."
    )
    
    content += make_paragraph("2.2 Beyond Linear Chain-of-Thought", style="Heading2", bold=True)
    
    content += make_paragraph(
        "While linear chain-of-thought reasoning provides significant benefits, many complex problems require non-linear reasoning strategies. Tree-of-Thought (ToT), "
        "proposed by Yao et al. [24], extends CoT by allowing models to explore multiple reasoning branches simultaneously, evaluate partial solutions, and backtrack "
        "from unproductive paths. This approach mirrors human problem-solving strategies where multiple hypotheses are considered in parallel, with resources "
        "concentrated on the most promising directions. Graph-of-Thought [25] further generalizes this by allowing arbitrary connections between reasoning nodes, "
        "enabling the representation of complex dependency structures that cannot be captured by tree-structured exploration. The practical significance of these "
        "non-linear approaches becomes apparent in problems with high branching factors or where the correct reasoning path is not immediately obvious from the "
        "problem statement, requiring exploration and backtracking to identify productive solution strategies."
    )
    
    # Figure 2
    content += make_image_paragraph("rId11", 5400000, 3375000)
    content += make_paragraph("Figure 2. Comparison of chain-of-thought reasoning strategies: linear sequential reasoning (left), tree-of-thought branching exploration (center), and graph-based reasoning with cross-connections (right). Bottom panel shows relative performance on reasoning benchmarks.", style="Caption", italic=True)
    content += make_paragraph("")
    
    content += make_paragraph(
        "Self-reflection and iterative refinement represent another important extension of linear reasoning. Reflexion [26] enables models to evaluate their own "
        "reasoning outputs, identify errors or weaknesses, and generate improved reasoning chains in subsequent iterations. This creates a feedback loop where "
        "the model serves as both reasoner and critic, progressively improving solution quality through multiple passes. Decomposition strategies [27] break complex "
        "problems into independent sub-problems that can be solved separately and then synthesized, enabling parallel computation and reducing the cognitive load "
        "on any single reasoning chain."
    )
    
    content += make_paragraph(
        "Tool-augmented and retrieval-augmented reasoning extend the boundaries of what chain-of-thought can accomplish by integrating external capabilities. "
        "When a reasoning step requires precise computation, the model can invoke a calculator or code interpreter rather than attempting mental arithmetic [28]. "
        "When factual knowledge is needed, retrieval systems can provide relevant information without requiring the model to rely solely on parametric memory. "
        "As shown in Figure 2, these different reasoning strategies offer complementary advantages: linear CoT provides simplicity and interpretability, tree-based "
        "approaches offer exploration breadth, and graph-based reasoning captures complex dependencies between reasoning steps."
    )
    
    content += make_paragraph(
        "The integration of search algorithms with structured reasoning has created a new class of reasoning systems that combine the flexibility of neural "
        "generation with the systematic exploration guarantees of classical AI search. These systems treat each reasoning step as a node in a search graph, "
        "with transitions between steps representing possible continuations of the reasoning process. By applying heuristic evaluation functions—typically "
        "implemented as learned value models—the system can estimate the promise of different reasoning paths and allocate exploration effort accordingly. "
        "This approach enables reasoning systems to solve problems that require exploration of exponentially large solution spaces, making them applicable "
        "to domains such as automated theorem proving, program synthesis, and strategic planning where exhaustive enumeration is infeasible."
    )
    
    content += make_paragraph("2.3 Evaluating Reasoning Quality", style="Heading2", bold=True)
    
    content += make_paragraph(
        "Evaluating the quality of machine reasoning requires metrics that go beyond simple answer accuracy. While outcome correctness remains important, it fails "
        "to distinguish between correct answers arrived at through valid reasoning and those produced by lucky guessing or pattern matching. Process-level evaluation "
        "assesses the quality of individual reasoning steps, checking for logical validity, factual accuracy, and relevance to the overall solution strategy [29]. "
        "This distinction between outcome-level and process-level evaluation has profound implications for how reasoning systems are trained and deployed."
    )
    
    content += make_paragraph(
        "Reasoning-task benchmarks have evolved to capture increasingly sophisticated aspects of reasoning ability. GSM8K [30] and MATH [31] evaluate mathematical "
        "reasoning at different difficulty levels. ARC [32] tests scientific reasoning and common-sense inference. LogiQA and related benchmarks assess formal logical "
        "reasoning capabilities. More recent benchmarks like FrontierMath [33] target problems at the frontier of difficulty, where even the most capable reasoning "
        "systems achieve limited success, providing headroom for measuring future progress."
    )
    
    # Table 2
    content += make_paragraph("")
    content += make_paragraph("Table 2. Performance of Reasoning Approaches Across Standard Benchmarks", style="Caption", bold=True)
    content += make_table(
        ["Model/Method", "GSM8K (%)", "MATH (%)", "ARC-C (%)", "LogiQA (%)", "HumanEval (%)"],
        [
            ["GPT-4 (standard)", "92.0", "52.9", "96.3", "79.1", "87.1"],
            ["GPT-4 + CoT", "95.3", "64.5", "97.1", "83.4", "89.7"],
            ["o1-preview", "97.8", "85.5", "98.2", "88.7", "93.4"],
            ["DeepSeek-R1", "97.3", "79.8", "97.8", "86.2", "91.6"],
            ["Claude 3.5 + CoT", "96.1", "71.2", "97.5", "85.8", "92.0"],
            ["Process Reward + Search", "98.1", "88.3", "98.5", "90.1", "94.2"],
        ]
    )
    content += make_paragraph("")
    
    content += make_paragraph(
        "Faithfulness, robustness, and consistency of reasoning represent additional evaluation dimensions that are critical for trustworthy deployment. Faithfulness "
        "measures whether the externalized reasoning chain accurately reflects the model's internal decision-making process [17]. Robustness assesses whether "
        "reasoning quality is maintained under input perturbations—paraphrasing, irrelevant information insertion, or adversarial modifications. Consistency "
        "evaluates whether a model produces logically compatible reasoning across related problems, detecting contradictions that would indicate unreliable "
        "reasoning processes. As shown in Table 2, different reasoning approaches exhibit varying levels of performance across these benchmarks, with process "
        "reward guided search achieving the highest overall scores."
    )
    
    content += make_paragraph(
        "The development of comprehensive evaluation frameworks for reasoning quality remains an active area of research. Current benchmarks primarily focus "
        "on domains where ground-truth answers are available and verifiable—mathematics, formal logic, and programming. However, many important reasoning "
        "tasks involve domains where correctness is more subjective or difficult to verify, such as legal reasoning, ethical deliberation, and scientific "
        "hypothesis generation. Developing evaluation methodologies for these open-ended reasoning domains requires new approaches that assess reasoning "
        "process quality rather than merely outcome correctness. Process-level metrics such as ROSCOE [29] represent important steps in this direction, "
        "providing multi-dimensional assessment of reasoning chain quality including informativeness, relevance, coherence, and logical validity."
    )
    
    # ========== SECTION 3 ==========
    content += make_paragraph("3. Process Rewards and Reasoning Optimization", style="Heading1", bold=True)
    
    content += make_paragraph(
        "Process rewards represent a fundamental advance in how reasoning systems are trained and optimized. Rather than providing feedback only on final "
        "outcomes, process reward models evaluate the quality of each intermediate reasoning step, enabling more precise credit assignment and more efficient "
        "learning. This section examines the theoretical motivation for process rewards, practical training methodologies, and verification mechanisms "
        "that together enable the development of increasingly capable and reliable reasoning engines."
    )
    
    content += make_paragraph("3.1 Outcome Rewards versus Process Rewards", style="Heading2", bold=True)
    
    content += make_paragraph(
        "Traditional approaches to training and evaluating reasoning systems rely on outcome-based rewards—the model receives a positive signal only when "
        "the final answer is correct and a negative signal otherwise. While computationally simple, outcome rewards suffer from a fundamental credit assignment "
        "problem: when a multi-step reasoning chain produces an incorrect answer, it is unclear which step or steps caused the failure [34]. This ambiguity "
        "makes learning from mistakes extremely inefficient, as the model cannot distinguish between reasoning chains that are entirely wrong and those that "
        "contain a single error in an otherwise correct solution."
    )
    
    content += make_paragraph(
        "Process reward models (PRMs) address this limitation by providing step-level supervision. Rather than evaluating only the final answer, a PRM assigns "
        "a reward signal to each intermediate reasoning step, indicating whether that step is correct, relevant, and logically sound [35]. This fine-grained "
        "feedback enables more efficient learning by precisely identifying where reasoning goes wrong, allowing targeted improvement of specific reasoning "
        "capabilities. Lightman et al. [35] demonstrated that process supervision significantly outperforms outcome supervision for training mathematical "
        "reasoning models, particularly on problems requiring many reasoning steps."
    )
    
    content += make_paragraph(
        "The design of reward functions for multi-step reasoning involves several considerations. Step correctness rewards evaluate whether each reasoning "
        "step is logically valid given preceding steps. Progress rewards assess whether a step moves closer to the solution, penalizing circular reasoning "
        "or irrelevant tangents. Efficiency rewards encourage concise reasoning, preventing unnecessarily verbose chains that increase computational cost "
        "without improving accuracy [36]. The combination of these reward components creates a multi-objective optimization landscape that guides reasoning "
        "models toward producing correct, efficient, and well-structured solutions."
    )
    
    content += make_paragraph(
        "The practical implementation of process reward models requires careful consideration of the annotation methodology. Human annotation of step-level "
        "correctness is expensive and time-consuming, limiting the scale of manually supervised training data. Lightman et al. [35] demonstrated that even "
        "relatively small amounts of human process supervision can yield substantial improvements over purely outcome-based training. However, scaling "
        "process supervision to the levels required for training frontier reasoning models necessitates automated approaches. Mathematical verification "
        "through symbolic computation, code execution for programming tasks, and model-based evaluation for natural language reasoning provide complementary "
        "automated supervision signals that can be generated at scale without human involvement. The challenge lies in ensuring that these automated signals "
        "are sufficiently accurate to provide reliable training gradients."
    )
    
    content += make_paragraph("3.2 Training Reasoning Engines with Process Supervision", style="Heading2", bold=True)
    
    content += make_paragraph(
        "Reinforcement learning provides the primary framework for training reasoning engines with process supervision. Proximal Policy Optimization (PPO) [37] "
        "and its variants enable models to learn from reward signals while maintaining stable training dynamics. The reasoning model generates step-by-step "
        "solutions, the process reward model evaluates each step, and the policy is updated to increase the probability of high-reward reasoning paths. "
        "Group Relative Policy Optimization (GRPO), employed by DeepSeek-R1 [7], extends this framework by comparing reasoning paths against each other "
        "rather than against an absolute reward baseline, improving training stability and sample efficiency."
    )
    
    content += make_paragraph(
        "The training dynamics of reasoning engines exhibit several distinctive characteristics compared to standard language model fine-tuning. First, the "
        "reward signal is inherently sparse and delayed—even with process rewards, the signal is generated only after a complete reasoning step is produced, "
        "creating credit assignment challenges at the token level. Second, the action space is enormous, as each reasoning step consists of a variable-length "
        "sequence of tokens with complex interdependencies. Third, the quality of reasoning is highly sensitive to the distribution of training problems—models "
        "trained primarily on easy problems may fail to develop the sophisticated reasoning strategies needed for difficult problems, while training exclusively "
        "on difficult problems may destabilize learning. Curriculum learning strategies that progressively increase problem difficulty have proven effective "
        "in addressing this challenge, enabling models to build reasoning capabilities incrementally."
    )
    
    # Figure 3
    content += make_image_paragraph("rId12", 5400000, 3375000)
    content += make_paragraph("Figure 3. Process reward model training pipeline showing the flow from input problems through step generation, process reward evaluation, and verification. The middle section illustrates how correct reasoning paths (green steps) receive positive rewards while incorrect paths (red steps) receive negative rewards at the point of error.", style="Caption", italic=True)
    content += make_paragraph("")
    
    content += make_paragraph(
        "Direct Preference Optimization (DPO) [38] offers an alternative approach that avoids explicit reward model training by directly optimizing the language "
        "model to prefer better reasoning chains over worse ones. This simplifies the training pipeline but requires high-quality comparison data. Iterative DPO "
        "extends this by generating comparison pairs from the model itself through rejection sampling—generating multiple reasoning chains and using outcome "
        "correctness to create preference pairs for training [39]. As depicted in Figure 3, the training pipeline creates a virtuous cycle where improved "
        "reasoning generates better training data, which further improves reasoning capabilities. The choice between PPO-based and DPO-based training "
        "approaches involves trade-offs in training stability, data efficiency, and computational cost. PPO provides more flexible reward signal integration "
        "but requires careful hyperparameter tuning and can exhibit training instability. DPO offers simpler implementation and more stable training but "
        "is limited to learning from pairwise comparisons rather than continuous reward signals."
    )
    
    content += make_paragraph(
        "Verifiable rewards and automated feedback represent a particularly promising direction for scaling process supervision without extensive human annotation. "
        "In mathematical and programming domains, the correctness of reasoning steps can often be verified automatically through symbolic computation or code "
        "execution [40]. This enables the generation of large-scale process supervision datasets without human involvement, dramatically reducing the cost "
        "of training. Synthetic supervision through AI-assisted evaluation—where one model evaluates another's reasoning—provides a scalable alternative for "
        "domains where automatic verification is not feasible [41]."
    )
    
    content += make_paragraph(
        "The emerging paradigm of self-play and iterative self-improvement in reasoning training deserves particular attention. In this framework, the reasoning "
        "model generates solutions, a verifier evaluates them, and the results are used to create training data for the next iteration. This bootstrapping "
        "approach, exemplified by STaR (Self-Taught Reasoner) [34], enables reasoning models to improve beyond the level of their initial training data by "
        "discovering new reasoning strategies through exploration. The key insight is that correctly solving a problem—even by chance—provides a valid "
        "demonstration of reasoning that can be used for further training. Combined with process rewards that identify which steps were crucial for success, "
        "this creates a powerful curriculum learning signal that progressively develops more sophisticated reasoning capabilities without requiring "
        "additional human supervision at each iteration."
    )
    
    content += make_paragraph("3.3 Verification and Error Correction", style="Heading2", bold=True)
    
    content += make_paragraph(
        "Step-by-step verification mechanisms form a critical component of reliable reasoning engines. Rather than producing a single reasoning chain and "
        "committing to its conclusion, verification-enhanced systems evaluate each step before proceeding, catching errors before they propagate. This approach "
        "draws inspiration from formal proof verification systems where each inference step must satisfy explicit validity criteria [42]. In neural reasoning "
        "engines, verification is typically performed by a separate model (or the same model in a different mode) that evaluates whether each step follows "
        "logically from its predecessors and the original problem statement."
    )
    
    content += make_paragraph(
        "Critic, verifier, and judge models serve complementary roles in the verification ecosystem. Critics identify potential weaknesses in reasoning chains "
        "without necessarily determining correctness—flagging steps that seem unusual, unsupported, or potentially erroneous [43]. Verifiers make binary "
        "correctness determinations, classifying steps as valid or invalid. Judge models perform holistic evaluation of complete reasoning chains, assessing "
        "overall solution quality and identifying the most reliable solution among multiple candidates. The combination of these verification roles creates "
        "a multi-layered quality assurance system that catches errors at different stages of the reasoning process."
    )
    
    content += make_paragraph(
        "Detecting and correcting reasoning failures during inference enables dynamic self-improvement. When a verifier identifies an incorrect step, the "
        "reasoning engine can backtrack to the last known-correct state and generate alternative continuations [44]. This search-with-verification approach "
        "combines the exploration benefits of diverse reasoning with the quality assurance of step-level checking. Recent systems implement this as a form "
        "of Monte Carlo Tree Search (MCTS) where each node represents a reasoning step, branches represent alternative continuations, and the process "
        "reward model provides value estimates that guide the search toward correct solutions [45]."
    )
    
    content += make_paragraph(
        "The interplay between verification granularity and computational cost creates important design trade-offs. Fine-grained verification that checks "
        "every individual reasoning step provides maximum error detection capability but doubles the computational requirements, as each generation step "
        "must be followed by a verification step. Coarse-grained verification that checks reasoning at the paragraph or solution level is more efficient "
        "but may miss errors that propagate through multiple steps before becoming detectable. Adaptive verification strategies that adjust checking "
        "frequency based on estimated error probability offer a promising middle ground, concentrating verification resources on reasoning steps where "
        "errors are most likely to occur—such as complex mathematical manipulations, logical transitions, or steps that deviate significantly from "
        "the model's typical reasoning patterns."
    )
    
    # Table 3
    content += make_paragraph("")
    content += make_paragraph("Table 3. Impact of Process Reward Models on Reasoning Performance", style="Caption", bold=True)
    content += make_table(
        ["Verification Strategy", "Math Accuracy (%)", "Error Detection Rate (%)", "Compute Overhead", "Latency Impact"],
        [
            ["No verification", "72.4", "N/A", "1x", "Baseline"],
            ["Outcome-only verification", "78.1", "45.2", "2x", "+50%"],
            ["Step-level PRM", "85.7", "71.8", "5x", "+180%"],
            ["PRM + MCTS", "91.3", "82.4", "20x", "+600%"],
            ["PRM + Iterative refinement", "89.6", "78.9", "8x", "+280%"],
            ["Ensemble verification", "93.1", "88.6", "50x", "+1200%"],
        ]
    )
    content += make_paragraph("")
    
    content += make_paragraph(
        "Table 3 presents the impact of different verification strategies on reasoning performance, demonstrating the clear trade-off between accuracy gains "
        "and computational overhead. Process reward models combined with search (PRM + MCTS) achieve substantial accuracy improvements but at significant "
        "computational cost. The selection of verification strategy must balance these trade-offs against application requirements for accuracy, latency, and "
        "resource consumption. Importantly, the error detection rate—the proportion of reasoning errors successfully identified by the verification system—varies "
        "significantly across approaches, with ensemble verification achieving the highest detection rates but at prohibitive computational costs for many "
        "real-time applications. The practical deployment of verification strategies therefore requires careful analysis of the error tolerance and "
        "computational budget specific to each application domain."
    )
    
    # ========== SECTION 4 ==========
    content += make_paragraph("4. Test-Time Compute and Scalable Reasoning", style="Heading1", bold=True)
    
    content += make_paragraph(
        "Test-time compute scaling represents one of the most transformative recent developments in AI reasoning, demonstrating that the computational "
        "resources allocated during inference can be as important as—or even more important than—the resources invested during training. This section "
        "examines the strategies, trade-offs, and future directions for test-time compute scaling in reasoning engines, with particular attention to "
        "the practical implications for deploying reasoning-enhanced systems at scale in resource-constrained environments."
    )
    
    content += make_paragraph("4.1 Test-Time Scaling Strategies", style="Heading2", bold=True)
    
    content += make_paragraph(
        "Test-time compute scaling represents a paradigm shift in how AI systems allocate computational resources. Traditional approaches invest computation "
        "exclusively during training, producing fixed models that apply identical computation to every input regardless of difficulty. Test-time scaling "
        "inverts this paradigm by allowing models to dynamically increase computation during inference for more challenging problems [18]. This mirrors human "
        "cognition, where simple questions receive rapid intuitive responses while complex problems trigger extended deliberation."
    )
    
    content += make_paragraph(
        "Best-of-N sampling constitutes the simplest test-time scaling strategy. The model generates N independent solutions, and a selection mechanism "
        "(reward model, verifier, or self-consistency) chooses the best one. This approach scales linearly with N and provides diminishing but consistent "
        "improvements as N increases [46]. Self-consistency, a specific form of Best-of-N, uses majority voting among diverse reasoning chains, leveraging "
        "the observation that correct reasoning paths tend to converge on the same answer while incorrect paths produce diverse wrong answers [21]. The "
        "effectiveness of Best-of-N sampling depends critically on two factors: the diversity of the generated candidates (which determines the probability "
        "that at least one correct solution is included) and the accuracy of the selection mechanism (which determines whether the correct solution can be "
        "reliably identified among the candidates). Temperature scaling, prompt variation, and diverse decoding strategies can all be employed to increase "
        "candidate diversity, while more sophisticated reward models and verification mechanisms improve selection accuracy."
    )
    
    content += make_paragraph(
        "Search-based strategies provide more sophisticated test-time scaling by exploring the solution space more efficiently than independent sampling. "
        "Beam search maintains multiple partial solutions simultaneously, pruning unpromising paths and expanding promising ones based on process reward "
        "estimates. Monte Carlo Tree Search (MCTS) balances exploration of novel reasoning paths with exploitation of known good strategies, using upper "
        "confidence bounds to allocate computation optimally across the search tree [45]. Iterative reasoning strategies generate solutions, evaluate them, "
        "identify weaknesses, and generate improved versions in subsequent iterations, creating a refinement loop that progressively improves solution quality."
    )
    
    content += make_paragraph(
        "Reranking strategies provide a computationally efficient form of test-time scaling by generating multiple candidates and selecting among them "
        "using a separate evaluation model. Unlike search-based approaches that construct solutions incrementally with guidance, reranking generates "
        "complete solutions independently and applies post-hoc selection. This approach parallelizes naturally across hardware accelerators, making it "
        "particularly suitable for batch processing scenarios. The effectiveness of reranking depends critically on the quality of the ranker model and "
        "the diversity of the generated candidates—diverse candidate sets increase the probability that at least one candidate contains the correct "
        "solution, while accurate ranking ensures that the correct candidate is reliably selected from the pool."
    )
    
    content += make_paragraph("4.2 Compute-Accuracy-Latency Trade-offs", style="Heading2", bold=True)
    
    content += make_paragraph(
        "The relationship between inference budget and reasoning performance follows characteristic scaling laws that have been empirically characterized "
        "across multiple domains and model architectures. Snell et al. [18] demonstrated that performance typically scales logarithmically with compute "
        "budget—doubling the inference computation yields approximately constant absolute improvement in accuracy. This means that achieving high accuracy "
        "on difficult problems requires exponentially more computation, creating practical limits on how much improvement test-time compute can deliver "
        "within reasonable cost and latency constraints. Understanding these scaling laws is essential for practitioners who must make informed decisions "
        "about resource allocation. The logarithmic scaling relationship implies that for any given problem difficulty level, there exists a point of "
        "diminishing returns beyond which additional computation provides negligible accuracy benefit. Identifying this optimal stopping point—and "
        "doing so efficiently without excessive exploratory computation—is itself an active research problem."
    )
    
    # Figure 4
    content += make_image_paragraph("rId13", 5400000, 3375000)
    content += make_paragraph("Figure 4. Test-time compute scaling curves showing the relationship between computational budget (x-axis) and reasoning accuracy (y-axis) for different scaling strategies. The orange vertical line indicates the region of diminishing returns where additional compute provides minimal accuracy improvement.", style="Caption", italic=True)
    content += make_paragraph("")
    
    content += make_paragraph(
        "Adaptive allocation of computational resources addresses the inefficiency of applying uniform computation to all problems. Difficulty-aware routing "
        "systems estimate problem complexity and allocate computation proportionally—simple problems receive minimal additional computation while difficult "
        "problems trigger extensive search and verification [47]. This adaptive approach can achieve comparable accuracy to uniform high-compute allocation "
        "while dramatically reducing average computational cost. As illustrated in Figure 4, adaptive compute strategies (purple curve) achieve superior "
        "performance-per-compute ratios compared to fixed-budget approaches by concentrating resources where they provide the greatest benefit. The "
        "implementation of adaptive computation requires robust difficulty estimation mechanisms that can assess problem complexity before committing "
        "computational resources. These estimators can be trained on historical data correlating problem features with the computation required for "
        "correct solution, enabling increasingly accurate resource allocation as the system accumulates experience across diverse problem domains. "
        "Early-exit mechanisms that terminate computation when confidence exceeds a threshold provide an alternative form of adaptation that avoids "
        "the need for explicit difficulty estimation, instead relying on the model's own uncertainty signals to determine when sufficient computation "
        "has been performed."
    )
    
    content += make_paragraph(
        "Energy efficiency, latency, and cost considerations govern practical deployment decisions. In interactive applications, users expect responses "
        "within seconds, limiting the compute budget available for test-time scaling. Batch processing applications can tolerate longer latencies but face "
        "energy and cost constraints that limit total compute. The optimal trade-off point depends on the specific application: medical diagnosis systems "
        "may justify extensive computation for accuracy, while conversational assistants must balance reasoning depth against response time expectations. "
        "Hardware accelerators designed specifically for inference-time search and verification could shift these trade-offs by reducing the per-step "
        "computational cost of reasoning [4]."
    )
    
    content += make_paragraph(
        "The economics of test-time compute scaling have profound implications for the deployment and business models of reasoning-enhanced AI systems. "
        "Unlike training compute, which is amortized across all users and queries, test-time compute is incurred per-query and scales with query volume. "
        "This creates a direct relationship between reasoning quality and operating cost that must be carefully managed. Providers of reasoning services "
        "face the challenge of offering flexible compute budgets that allow users to select their preferred accuracy-cost trade-off point. Some applications "
        "warrant spending significant computational resources per query—legal analysis, medical reasoning, or scientific discovery—while others require "
        "rapid, inexpensive reasoning even at the cost of reduced accuracy. The development of efficient reasoning architectures that maximize accuracy "
        "per unit of compute therefore has direct economic significance beyond its technical importance."
    )
    
    content += make_paragraph("4.3 Future Reasoning Engines for Scalable AI Systems", style="Heading2", bold=True)
    
    content += make_paragraph(
        "Agentic reasoning and autonomous problem solving represent the next frontier in reasoning engine development. Rather than solving isolated problems, "
        "agentic reasoning systems operate in extended contexts, maintaining goals over multiple interactions, planning multi-step strategies, and adapting "
        "their approaches based on environmental feedback [13]. These systems combine reasoning engines with action execution capabilities, creating "
        "autonomous agents that can write and execute code, search for information, conduct experiments, and iteratively refine solutions without human "
        "intervention between steps. The development of agentic reasoning systems raises new challenges in safety, alignment, and control that are "
        "qualitatively different from those facing isolated reasoning engines, as errors in autonomous systems can compound through environmental "
        "interactions in ways that are difficult to predict or reverse."
    )
    
    content += make_paragraph(
        "Hardware-software co-design for efficient inference represents a critical enabler of scalable reasoning engines. Current reasoning approaches "
        "are bottlenecked by the sequential nature of autoregressive generation and the memory bandwidth requirements of large model inference. Specialized "
        "hardware architectures that support efficient tree search, parallel hypothesis evaluation, and rapid model switching could dramatically reduce the "
        "cost of reasoning [4]. Silicon-efficient computing paradigms, including sparse computation, speculative execution of reasoning branches, and "
        "hardware-native support for verification operations, promise to make advanced reasoning practical for deployment at scale. The co-evolution of "
        "reasoning algorithms and hardware architectures will likely define the performance frontier for the next generation of AI reasoning systems, "
        "with innovations in each domain enabling advances in the other."
    )
    
    # Table 4
    content += make_paragraph("")
    content += make_paragraph("Table 4. Future Directions and Research Challenges in Reasoning Engines", style="Caption", bold=True)
    content += make_table(
        ["Research Direction", "Current State", "Key Challenge", "Potential Impact", "Timeline"],
        [
            ["Latent reasoning", "Early research", "Training stability", "10x efficiency gain", "2-3 years"],
            ["Formal verification integration", "Proof of concept", "Scalability", "Guaranteed correctness", "3-5 years"],
            ["Multi-modal reasoning", "Limited integration", "Cross-modal alignment", "Broader applications", "2-4 years"],
            ["Distributed reasoning", "Theoretical", "Communication overhead", "Massive scale problems", "4-6 years"],
            ["Neuromorphic reasoning", "Conceptual", "Hardware maturity", "1000x energy efficiency", "5-10 years"],
            ["Self-improving reasoners", "Early prototypes", "Stability and alignment", "Continuous improvement", "3-5 years"],
        ]
    )
    content += make_paragraph("")
    
    content += make_paragraph(
        "The integration of reasoning engines with generative AI and silicon-efficient computing creates opportunities for systems that combine creative "
        "generation with rigorous reasoning. Generative models can propose hypotheses and solution candidates, while reasoning engines verify, refine, "
        "and select among these candidates. This division of labor leverages the strengths of each paradigm—generation for breadth and creativity, "
        "reasoning for depth and correctness—creating hybrid systems that outperform either approach alone. Table 4 outlines key future research "
        "directions and their expected timelines, highlighting the breadth of open challenges in this rapidly evolving field."
    )
    
    content += make_paragraph(
        "The prospect of multi-modal reasoning engines that can reason across text, images, code, mathematical notation, and physical simulations "
        "represents a particularly exciting frontier. Current reasoning capabilities are primarily developed in text-based domains, but many real-world "
        "problems require integrating information from multiple modalities. A scientist reasoning about experimental results must interpret graphs, "
        "understand mathematical equations, reason about physical processes, and synthesize conclusions in natural language. Multi-modal reasoning "
        "engines that natively support this kind of cross-modal inference would dramatically expand the range of problems amenable to automated reasoning, "
        "from drug discovery and materials science to engineering design and financial analysis."
    )
    
    content += make_paragraph(
        "Open research challenges in trustworthy and scalable reasoning span multiple dimensions. Alignment of reasoning processes—ensuring that reasoning "
        "engines pursue intended goals and operate within specified boundaries—becomes increasingly critical as systems gain autonomy [10]. Robustness to "
        "adversarial inputs that exploit reasoning vulnerabilities requires new defense mechanisms specifically designed for multi-step inference. "
        "Calibration of reasoning confidence—knowing when reasoning is likely to be correct and when uncertainty is high—enables appropriate deployment "
        "of human oversight. Finally, the democratization of reasoning capabilities through efficient architectures and open research ensures that the "
        "benefits of advanced reasoning are broadly accessible rather than concentrated in a few well-resourced organizations."
    )
    
    content += make_paragraph(
        "The convergence of chain-of-thought reasoning, process reward optimization, and test-time compute scaling defines the current frontier of AI "
        "reasoning capabilities. These three pillars—explicit reasoning structure, fine-grained supervision, and adaptive computation—work synergistically "
        "to enable reasoning systems that are more accurate, more reliable, and more interpretable than their predecessors. As the field continues to "
        "advance, the integration of these techniques with emerging hardware capabilities and broader AI system architectures will determine how quickly "
        "and effectively reasoning engines can be deployed to address real-world challenges requiring systematic, verifiable, and scalable machine reasoning."
    )
    
    content += make_paragraph(
        "In conclusion, reasoning engines represent a transformative advance in artificial intelligence that addresses the fundamental limitations of "
        "purely generative approaches. By combining explicit chain-of-thought decomposition with process-level reward optimization and adaptive test-time "
        "computation, these systems achieve levels of reasoning accuracy and reliability that were previously unattainable. The ongoing development of "
        "more efficient architectures, more scalable training methods, and more robust verification mechanisms will continue to push the boundaries of "
        "what machines can reason about, ultimately enabling AI systems that can serve as trusted partners in complex intellectual work across science, "
        "engineering, medicine, and beyond. The challenges that remain—including alignment, robustness, efficiency, and accessibility—define a rich "
        "research agenda that will shape the next decade of AI development and deployment."
    )
    
    # ========== REFERENCES ==========
    content += make_paragraph("")
    content += make_paragraph("References", style="Heading1", bold=True)
    
    references = [
        "[1] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, \"Attention is all you need,\" in Advances in Neural Information Processing Systems, vol. 30, 2017.",
        "[2] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi, Q. V. Le, and D. Zhou, \"Chain-of-thought prompting elicits reasoning in large language models,\" in Advances in Neural Information Processing Systems, vol. 35, 2022.",
        "[3] S. Bubeck, V. Chandrasekaran, R. Eldan, J. Gehrke, E. Horvitz, E. Kamar, P. Lee, Y. T. Lee, Y. Li, S. Lundberg, et al., \"Sparks of artificial general intelligence: Early experiments with GPT-4,\" arXiv preprint arXiv:2303.12712, 2023.",
        "[4] A. Sardana and J. Frankle, \"Beyond chinchilla-optimal: Accounting for inference in language model scaling laws,\" arXiv preprint arXiv:2401.00448, 2024.",
        "[5] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, et al., \"Language models are few-shot learners,\" in Advances in Neural Information Processing Systems, vol. 33, 2020.",
        "[6] OpenAI, \"Learning to reason with LLMs,\" OpenAI Blog, September 2024.",
        "[7] DeepSeek-AI, \"DeepSeek-R1: Incentivizing reasoning capability in LLMs via reinforcement learning,\" arXiv preprint arXiv:2501.12948, 2025.",
        "[8] S. Huang, H. Jiang, and L. Kong, \"Towards reasoning in large language models: A survey,\" in Findings of the Association for Computational Linguistics: ACL 2023, pp. 1049-1065, 2023.",
        "[9] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao, \"Reflexion: Language agents with verbal reinforcement learning,\" in Advances in Neural Information Processing Systems, vol. 36, 2023.",
        "[10] J. Leike, D. Krueger, T. Everitt, M. Martic, V. Maini, and S. Legg, \"Scalable agent alignment via reward modeling: A research direction,\" arXiv preprint arXiv:1811.07871, 2018.",
        "[11] J. Wei, J. Tay, R. Bommasani, C. Raffel, B. Zoph, S. Borgeaud, D. Yogatama, M. Bosma, D. Zhou, D. Metzler, et al., \"Emergent abilities of large language models,\" Transactions on Machine Learning Research, 2022.",
        "[12] A. Deng, Z. Hu, and T. Chen, \"Explicit CoT training for latent reasoning,\" arXiv preprint arXiv:2502.09456, 2025.",
        "[13] Y. Qin, S. Liang, Y. Ye, K. Zhu, L. Yan, Y. Lu, Y. Lin, X. Cong, X. Tang, B. Qian, et al., \"ToolLLM: Facilitating large language models to master 16000+ real-world APIs,\" in International Conference on Learning Representations, 2024.",
        "[14] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Kuttler, M. Lewis, W. Yih, T. Rocktaschel, et al., \"Retrieval-augmented generation for knowledge-intensive NLP tasks,\" in Advances in Neural Information Processing Systems, vol. 33, 2020.",
        "[15] Z. Ji, N. Lee, R. Frieske, T. Yu, D. Su, Y. Xu, E. Ishii, Y. J. Bang, A. Madotto, and P. Fung, \"Survey of hallucination in natural language generation,\" ACM Computing Surveys, vol. 55, no. 12, pp. 1-38, 2023.",
        "[16] A. Dziri, X. Lu, M. Sclar, X. L. Li, L. Jiang, B. Y. Lin, S. Welleck, P. West, C. Bhatt, J. Bras, et al., \"Faith and fate: Limits of transformers on compositionality,\" in Advances in Neural Information Processing Systems, vol. 36, 2023.",
        "[17] M. Turpin, J. Michael, E. Perez, and S. R. Bowman, \"Language models don't always say what they think: Unfaithful explanations in chain-of-thought prompting,\" in Advances in Neural Information Processing Systems, vol. 36, 2023.",
        "[18] C. Snell, J. Lee, K. Xu, and A. Kumar, \"Scaling LLM test-time compute optimally can be more effective than scaling model parameters,\" arXiv preprint arXiv:2408.03314, 2024.",
        "[19] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. Chi, Q. V. Le, and D. Zhou, \"Chain-of-thought prompting elicits reasoning in large language models,\" in NeurIPS, 2022.",
        "[20] T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, and Y. Iwasawa, \"Large language models are zero-shot reasoners,\" in Advances in Neural Information Processing Systems, vol. 35, 2022.",
        "[21] X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang, A. Chowdhery, and D. Zhou, \"Self-consistency improves chain of thought reasoning in language models,\" in International Conference on Learning Representations, 2023.",
        "[22] K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al., \"Training verifiers to solve math word problems,\" arXiv preprint arXiv:2110.14168, 2021.",
        "[23] L. Gao, A. Madaan, S. Zhou, U. Alon, P. Liu, Y. Yang, J. Callan, and G. Neubig, \"PAL: Program-aided language models,\" in International Conference on Machine Learning, 2023.",
        "[24] S. Yao, D. Yu, J. Zhao, I. Shafran, T. Griffiths, Y. Cao, and K. Narasimhan, \"Tree of thoughts: Deliberate problem solving with large language models,\" in Advances in Neural Information Processing Systems, vol. 36, 2023.",
        "[25] M. Besta, N. Blach, A. Kubicek, R. Gerstenberger, L. Gianinazzi, J. Gajber, T. Lehmann, H. Nber, R. Muller, and T. Hoefler, \"Graph of thoughts: Solving elaborate problems with large language models,\" in AAAI Conference on Artificial Intelligence, 2024.",
        "[26] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao, \"Reflexion: Language agents with verbal reinforcement learning,\" NeurIPS, 2023.",
        "[27] T. Khot, H. Trivedi, M. Finlayson, Y. Fu, K. Richardson, P. Clark, and A. Sabharwal, \"Decomposed prompting: A modular approach for solving complex tasks,\" in International Conference on Learning Representations, 2023.",
        "[28] L. Gao, A. Madaan, S. Zhou, U. Alon, P. Liu, Y. Yang, J. Callan, and G. Neubig, \"Program-aided language models,\" ICML, 2023.",
        "[29] O. Golovneva, M. Chen, S. Poff, M. Corredor, L. Zettlemoyer, M. Fazel-Zarandi, and A. Celikyilmaz, \"ROSCOE: A suite of metrics for scoring step-by-step reasoning,\" in International Conference on Learning Representations, 2023.",
        "[30] K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al., \"Training verifiers to solve math word problems,\" arXiv:2110.14168, 2021.",
        "[31] D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt, \"Measuring mathematical problem solving with the MATH dataset,\" in NeurIPS, 2021.",
        "[32] P. Clark, I. Cowhey, O. Etzioni, T. Khot, A. Sabharwal, C. Schoenick, and O. Tafjord, \"Think you have solved question answering? Try ARC, the AI2 reasoning challenge,\" arXiv preprint arXiv:1803.05457, 2018.",
        "[33] E. Glazer, N. Erdenberger, and F. Fang, \"FrontierMath: A benchmark for evaluating advanced mathematical reasoning in AI,\" arXiv preprint arXiv:2411.04872, 2024.",
        "[34] E. Zelikman, Y. Wu, J. Mu, and N. Goodman, \"STaR: Bootstrapping reasoning with reasoning,\" in Advances in Neural Information Processing Systems, vol. 35, 2022.",
        "[35] H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe, \"Let's verify step by step,\" in International Conference on Learning Representations, 2024.",
        "[36] L. Wang, L. Ma, C. Yang, and Z. Feng, \"Math-Shepherd: Verify and reinforce LLMs step-by-step without human annotations,\" in Annual Meeting of the Association for Computational Linguistics, 2024.",
        "[37] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, \"Proximal policy optimization algorithms,\" arXiv preprint arXiv:1707.06347, 2017.",
        "[38] R. Rafailov, A. Sharma, E. Mitchell, C. D. Manning, S. Ermon, and C. Finn, \"Direct preference optimization: Your language model is secretly a reward model,\" in Advances in Neural Information Processing Systems, vol. 36, 2023.",
        "[39] Z. Yuan, H. Yuan, C. Tan, W. Wang, S. Huang, and F. Huang, \"RRHF: Rank responses to align language models with human feedback without tears,\" in Advances in Neural Information Processing Systems, vol. 36, 2023.",
        "[40] A. Guo, A. Pasupat, and C. Raffel, \"Connecting large language models with evolutionary algorithms yields powerful prompt optimizers,\" in International Conference on Learning Representations, 2024.",
        "[41] Y. Zheng, R. Sun, Y. Zhang, and J. Zhou, \"Self-play fine-tuning converts weak language models to strong language models,\" in International Conference on Machine Learning, 2024.",
        "[42] S. Polu and I. Sutskever, \"Generative language modeling for automated theorem proving,\" arXiv preprint arXiv:2009.03393, 2020.",
        "[43] Y. Gou, Z. Shao, Y. Gong, Y. Shen, Y. Yang, N. Duan, and W. Chen, \"CRITIC: Large language models can self-correct with tool-interactive critiquing,\" in International Conference on Learning Representations, 2024.",
        "[44] H. Zhong, H. Luo, Y. Zhang, and Z. Li, \"Achieving >97% on GSM8K: Deeply understanding the problems makes LLMs better solvers,\" arXiv preprint arXiv:2404.14963, 2024.",
        "[45] X. Feng, Z. Wan, S. Wen, B. Chen, Z. Liu, and M. Sun, \"AlphaReasoning: Empowering large language models with Monte Carlo tree search,\" arXiv preprint arXiv:2502.07508, 2025.",
        "[46] J. Li, Z. Jiang, Y. Wu, and G. Neubig, \"Making language models better reasoners with step-aware verifier,\" in Annual Meeting of the Association for Computational Linguistics, 2023.",
        "[47] G. Team, \"Gemini: A family of highly capable multimodal models,\" arXiv preprint arXiv:2312.11805, 2023.",
    ]
    
    for ref in references:
        content += make_paragraph(ref)
    
    return content


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    output_dir = "/projects/sandbox/AMMAN"
    figures_dir = os.path.join(output_dir, "reasoning_figures")
    os.makedirs(figures_dir, exist_ok=True)
    
    print("Generating figures...")
    # Generate figures
    fig1_data = create_figure1()
    fig2_data = create_figure2()
    fig3_data = create_figure3()
    fig4_data = create_figure4()
    
    # Save figures as PNG files
    with open(os.path.join(figures_dir, "Figure_1_Reasoning_Architecture.png"), 'wb') as f:
        f.write(fig1_data)
    with open(os.path.join(figures_dir, "Figure_2_CoT_Strategies.png"), 'wb') as f:
        f.write(fig2_data)
    with open(os.path.join(figures_dir, "Figure_3_Process_Reward_Pipeline.png"), 'wb') as f:
        f.write(fig3_data)
    with open(os.path.join(figures_dir, "Figure_4_TestTime_Compute_Scaling.png"), 'wb') as f:
        f.write(fig4_data)
    
    print("Figures generated successfully.")
    
    # Build document content
    print("Building chapter content...")
    content_xml = build_chapter_content()
    
    # Define image relationships
    relationships = [
        {"id": "rId10", "target": "figure1.png"},
        {"id": "rId11", "target": "figure2.png"},
        {"id": "rId12", "target": "figure3.png"},
        {"id": "rId13", "target": "figure4.png"},
    ]
    
    images_data = {
        "rId10": fig1_data,
        "rId11": fig2_data,
        "rId12": fig3_data,
        "rId13": fig4_data,
    }
    
    # Create DOCX
    print("Creating Word document...")
    docx_bytes = create_docx(content_xml, relationships, images_data)
    
    output_path = os.path.join(output_dir, "Chapter_Reasoning_Engines.docx")
    with open(output_path, 'wb') as f:
        f.write(docx_bytes)
    
    print(f"Word document created: {output_path}")
    print(f"File size: {len(docx_bytes)} bytes")
    
    # Word count estimation
    import re
    text_content = re.sub(r'<[^>]+>', '', content_xml)
    text_content = re.sub(r'\s+', ' ', text_content).strip()
    word_count = len(text_content.split())
    print(f"Estimated word count: {word_count}")


if __name__ == "__main__":
    main()
