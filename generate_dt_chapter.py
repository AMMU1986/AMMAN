#!/usr/bin/env python3
"""
Generate a complete book chapter on Design Thinking and Strategic Decision-Making
as a Word document (.docx) using only Python standard library.
Includes 4 tables, 4 figures (PNG), and 47 references.
"""

import zipfile
import struct
import zlib
import io
import os
import math
import xml.etree.ElementTree as ET
from xml.dom import minidom

# ============================================================
# SECTION 1: PNG Figure Generation
# ============================================================

def create_png_rgba(width, height, pixels):
    """Create a PNG file from RGBA pixel data (list of lists of (r,g,b,a) tuples)"""
    def chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    header = b'\x89PNG\r\n\x1a\n'
    # 8-bit RGBA
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
    
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'  # filter byte (none)
        for x in range(width):
            r, g, b, a = pixels[y][x]
            raw_data += struct.pack('BBBB', r, g, b, a)
    
    idat = chunk(b'IDAT', zlib.compress(raw_data, 9))
    iend = chunk(b'IEND', b'')
    
    return header + ihdr + idat + iend


def blend_color(bg, fg, alpha):
    """Blend foreground over background with alpha (0-255)"""
    a = alpha / 255.0
    return int(bg * (1 - a) + fg * a)


def draw_filled_rect(pixels, x1, y1, x2, y2, color, width, height):
    """Draw a filled rectangle"""
    r, g, b = color
    for y in range(max(0, y1), min(height, y2)):
        for x in range(max(0, x1), min(width, x2)):
            pixels[y][x] = (r, g, b, 255)


def draw_text_block(pixels, x, y, text, color, width, height, scale=1):
    """Draw a simple text representation as a colored block with label indicator"""
    r, g, b = color
    # Draw a small indicator block
    bw = min(len(text) * 4 * scale, width - x)
    bh = 6 * scale
    for dy in range(bh):
        for dx in range(bw):
            if 0 <= y+dy < height and 0 <= x+dx < width:
                pixels[y+dy][x+dx] = (r, g, b, 255)


def draw_line(pixels, x1, y1, x2, y2, color, width_px, height_px, thickness=1):
    """Draw a line using Bresenham's algorithm"""
    r, g, b = color
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    
    while True:
        for t in range(-thickness//2, thickness//2 + 1):
            if 0 <= y1+t < height_px and 0 <= x1 < width_px:
                pixels[y1+t][x1] = (r, g, b, 255)
            if 0 <= y1 < height_px and 0 <= x1+t < width_px:
                pixels[y1][x1+t] = (r, g, b, 255)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def draw_circle(pixels, cx, cy, radius, color, width_px, height_px, fill=True):
    """Draw a filled or outline circle"""
    r, g, b = color
    for y in range(max(0, cy-radius), min(height_px, cy+radius+1)):
        for x in range(max(0, cx-radius), min(width_px, cx+radius+1)):
            dist = math.sqrt((x-cx)**2 + (y-cy)**2)
            if fill and dist <= radius:
                pixels[y][x] = (r, g, b, 255)
            elif not fill and abs(dist - radius) < 1.5:
                pixels[y][x] = (r, g, b, 255)


def draw_arrow(pixels, x1, y1, x2, y2, color, w, h, thickness=2):
    """Draw a line with arrowhead"""
    draw_line(pixels, x1, y1, x2, y2, color, w, h, thickness)
    # Arrowhead
    angle = math.atan2(y2-y1, x2-x1)
    arrow_len = 8
    for i in range(2):
        a = angle + math.pi + (0.4 if i == 0 else -0.4)
        ax = int(x2 + arrow_len * math.cos(a))
        ay = int(y2 + arrow_len * math.sin(a))
        draw_line(pixels, x2, y2, ax, ay, color, w, h, thickness)


def generate_figure1():
    """Figure 1: Design Thinking Process Framework - showing the 5 stages"""
    W, H = 350, 200
    pixels = [[(245, 248, 252, 255) for _ in range(W)] for _ in range(H)]
    
    # Title area
    draw_filled_rect(pixels, 0, 0, W, 18, (41, 65, 122), W, H)
    draw_text_block(pixels, 80, 5, "DESIGN THINKING PROCESS", (255, 255, 255), W, H, 1)
    
    # Five stages with colors
    stages = [
        ("Empathize", (52, 152, 219)),
        ("Define", (46, 204, 113)),
        ("Ideate", (241, 196, 15)),
        ("Prototype", (230, 126, 34)),
        ("Test", (231, 76, 60))
    ]
    
    y_center = 75
    
    for i, (name, color) in enumerate(stages):
        x = 20 + i * 66
        cx, cy = x + 28, y_center
        size = 22
        for dy in range(-size, size+1):
            for dx in range(-size, size+1):
                if abs(dx) + abs(dy) <= size:
                    px, py = cx+dx, cy+dy
                    if 0 <= px < W and 0 <= py < H:
                        pixels[py][px] = (*color, 255)
        
        # Arrow to next
        if i < 4:
            draw_arrow(pixels, x + 55, y_center, x + 63, y_center, (100, 100, 100), W, H, 1)
    
    # Feedback loop
    draw_line(pixels, 325, 95, 325, 130, (150, 50, 50), W, H, 1)
    draw_line(pixels, 325, 130, 48, 130, (150, 50, 50), W, H, 1)
    draw_arrow(pixels, 48, 130, 48, 100, (150, 50, 50), W, H, 1)
    
    # Bottom section - key principles
    draw_filled_rect(pixels, 15, 150, 335, 190, (230, 236, 245), W, H)
    for i, (name, color) in enumerate(stages):
        x = 25 + i * 65
        draw_filled_rect(pixels, x, 158, x + 50, 180, color, W, H)
    
    return create_png_rgba(W, H, pixels)


def generate_figure2():
    """Figure 2: Comparative Framework - DT vs Analytical vs Systems vs Creative"""
    W, H = 350, 230
    pixels = [[(250, 252, 255, 255) for _ in range(W)] for _ in range(H)]
    
    # Title
    draw_filled_rect(pixels, 0, 0, W, 18, (44, 62, 80), W, H)
    draw_text_block(pixels, 60, 5, "COMPARATIVE APPROACHES", (255, 255, 255), W, H, 1)
    
    # Four quadrants
    quadrants = [
        (10, 25, 170, 120, "Design Thinking", (52, 152, 219)),
        (180, 25, 340, 120, "Analytical", (46, 204, 113)),
        (10, 125, 170, 220, "Systems", (155, 89, 182)),
        (180, 125, 340, 220, "Creative", (241, 196, 15)),
    ]
    
    for x1, y1, x2, y2, title, color in quadrants:
        draw_filled_rect(pixels, x1, y1, x2, y2, (255, 255, 255), W, H)
        draw_line(pixels, x1, y1, x2, y1, color, W, H, 2)
        draw_line(pixels, x1, y2, x2, y2, color, W, H, 2)
        draw_line(pixels, x1, y1, x1, y2, color, W, H, 2)
        draw_line(pixels, x2, y1, x2, y2, color, W, H, 2)
        draw_filled_rect(pixels, x1+2, y1+2, x2-2, y1+16, color, W, H)
        for j in range(3):
            fy = y1 + 22 + j * 22
            draw_filled_rect(pixels, x1+8, fy, x1+14, fy+8, color, W, H)
            draw_filled_rect(pixels, x1+18, fy+2, x1+100, fy+6, (180, 180, 180), W, H)
    
    # Center connection
    draw_circle(pixels, 175, 122, 15, (231, 76, 60), W, H, True)
    
    return create_png_rgba(W, H, pixels)


def generate_figure3():
    """Figure 3: Synthesized Strategic Decision-Making Framework"""
    W, H = 350, 280
    pixels = [[(248, 250, 252, 255) for _ in range(W)] for _ in range(H)]
    
    # Title
    draw_filled_rect(pixels, 0, 0, W, 18, (39, 60, 117), W, H)
    draw_text_block(pixels, 70, 5, "SYNTHESIZED DM MODEL", (255, 255, 255), W, H, 1)
    
    # Central flow - vertical stages
    stages = [
        (30, "Problem Identification", (52, 152, 219)),
        (65, "Empathic Research", (41, 128, 185)),
        (100, "Systemic Mapping", (155, 89, 182)),
        (135, "Creative Ideation", (241, 196, 15)),
        (170, "Analytical Evaluation", (46, 204, 113)),
        (205, "Prototyping & Testing", (230, 126, 34)),
    ]
    
    for y, label, color in stages:
        draw_filled_rect(pixels, 80, y, 270, y+28, color, W, H)
        
    # Arrows between stages
    for i in range(len(stages)-1):
        y1 = stages[i][0] + 28
        y2 = stages[i+1][0]
        draw_arrow(pixels, 175, y1+1, 175, y2-1, (80, 80, 80), W, H, 1)
    
    # Left side circles
    for i, color in enumerate([(52, 152, 219), (155, 89, 182), (46, 204, 113)]):
        y = 40 + i * 70
        draw_circle(pixels, 40, y+14, 18, color, W, H, True)
        draw_arrow(pixels, 58, y+14, 78, y+14, color, W, H, 1)
    
    # Right side circles
    for i, color in enumerate([(52, 152, 219), (241, 196, 15), (230, 126, 34)]):
        y = 40 + i * 70
        draw_arrow(pixels, 272, y+14, 290, y+14, color, W, H, 1)
        draw_circle(pixels, 310, y+14, 18, color, W, H, True)
    
    # Iteration feedback
    draw_line(pixels, 310, 250, 310, 265, (231, 76, 60), W, H, 1)
    draw_line(pixels, 310, 265, 40, 265, (231, 76, 60), W, H, 1)
    draw_arrow(pixels, 40, 265, 40, 55, (231, 76, 60), W, H, 1)
    
    return create_png_rgba(W, H, pixels)


def generate_figure4():
    """Figure 4: Future Integrated Strategic Thinking Ecosystem"""
    W, H = 350, 250
    pixels = [[(246, 249, 253, 255) for _ in range(W)] for _ in range(H)]
    
    # Title
    draw_filled_rect(pixels, 0, 0, W, 18, (36, 55, 99), W, H)
    draw_text_block(pixels, 70, 5, "FUTURE STRATEGIC ECOSYSTEM", (255, 255, 255), W, H, 1)
    
    # Central hub
    cx, cy = 175, 135
    draw_circle(pixels, cx, cy, 30, (41, 65, 122), W, H, True)
    draw_circle(pixels, cx, cy, 22, (52, 73, 140), W, H, True)
    
    # Surrounding nodes
    nodes = [
        (175, 45, (52, 152, 219)),
        (280, 75, (46, 204, 113)),
        (305, 165, (39, 174, 96)),
        (255, 220, (241, 196, 15)),
        (95, 220, (230, 126, 34)),
        (45, 165, (231, 76, 60)),
        (70, 75, (155, 89, 182)),
    ]
    
    for nx, ny, color in nodes:
        draw_circle(pixels, nx, ny, 18, color, W, H, True)
        # Connection to center
        dx = cx - nx
        dy = cy - ny
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            sx = int(nx + 18 * dx/dist)
            sy = int(ny + 18 * dy/dist)
            ex = int(cx - 30 * dx/dist)
            ey = int(cy - 30 * dy/dist)
            draw_line(pixels, sx, sy, ex, ey, (150, 150, 170), W, H, 1)
    
    # Outer ring (dashed)
    for angle in range(0, 360, 4):
        rad = math.radians(angle)
        x = int(cx + 95 * math.cos(rad))
        y = int(cy + 95 * math.sin(rad))
        if angle % 8 < 4:
            if 0 <= x < W and 0 <= y < H:
                pixels[y][x] = (150, 150, 170, 255)
    
    return create_png_rgba(W, H, pixels)


# ============================================================
# SECTION 2: DOCX Generation (using only standard library)
# ============================================================

class DocxWriter:
    """Minimal DOCX writer using Python standard library"""
    
    def __init__(self):
        self.body_xml = []
        self.rels = []
        self.images = {}  # filename -> bytes
        self.image_counter = 0
        self.rel_counter = 10  # Start after default rels
        
    def add_heading(self, text, level=1):
        style = f"Heading{level}"
        self.body_xml.append(f'''<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr><w:r><w:t>{self._escape(text)}</w:t></w:r></w:p>''')
    
    def add_paragraph(self, text, bold=False, italic=False, style=None):
        """Add a paragraph with optional formatting. Supports [bold] and [italic] markers."""
        ppr = ""
        if style:
            ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
        
        rpr = ""
        if bold:
            rpr += "<w:b/>"
        if italic:
            rpr += "<w:i/>"
        
        rpr_xml = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
        
        self.body_xml.append(f'''<w:p>{ppr}<w:r>{rpr_xml}<w:t xml:space="preserve">{self._escape(text)}</w:t></w:r></w:p>''')
    
    def add_abstract(self, text):
        """Add abstract with italic formatting"""
        self.body_xml.append(f'''<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>Abstract</w:t></w:r></w:p>''')
        self.body_xml.append(f'''<w:p><w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">{self._escape(text)}</w:t></w:r></w:p>''')
    
    def add_empty_paragraph(self):
        self.body_xml.append('<w:p/>')
    
    def add_table(self, headers, rows, caption=""):
        """Add a table with headers and rows"""
        if caption:
            self.body_xml.append(f'''<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:i/></w:rPr><w:t xml:space="preserve">{self._escape(caption)}</w:t></w:r></w:p>''')
        
        cols = len(headers)
        col_width = 9000 // cols
        
        tbl_xml = '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="9000" w:type="dxa"/><w:tblBorders>'
        for border in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
            tbl_xml += f'<w:{border} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        tbl_xml += '</w:tblBorders></w:tblPr>'
        
        # Grid
        tbl_xml += '<w:tblGrid>'
        for _ in range(cols):
            tbl_xml += f'<w:gridCol w:w="{col_width}"/>'
        tbl_xml += '</w:tblGrid>'
        
        # Header row
        tbl_xml += '<w:tr>'
        for h in headers:
            tbl_xml += f'''<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="2C3E50"/></w:tcPr><w:p><w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/></w:rPr><w:t>{self._escape(h)}</w:t></w:r></w:p></w:tc>'''
        tbl_xml += '</w:tr>'
        
        # Data rows
        for i, row in enumerate(rows):
            fill = 'ECF0F1' if i % 2 == 0 else 'FFFFFF'
            tbl_xml += '<w:tr>'
            for cell in row:
                tbl_xml += f'''<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{fill}"/></w:tcPr><w:p><w:r><w:t xml:space="preserve">{self._escape(str(cell))}</w:t></w:r></w:p></w:tc>'''
            tbl_xml += '</w:tr>'
        
        tbl_xml += '</w:tbl>'
        self.body_xml.append(tbl_xml)
        self.add_empty_paragraph()
    
    def add_image(self, image_bytes, caption="", width_emu=5000000, height_emu=3000000):
        """Add an image to the document"""
        self.image_counter += 1
        self.rel_counter += 1
        
        img_filename = f"image{self.image_counter}.png"
        rel_id = f"rId{self.rel_counter}"
        
        self.images[img_filename] = image_bytes
        self.rels.append((rel_id, img_filename))
        
        # Add image paragraph
        img_xml = f'''<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>
        <wp:inline distT="0" distB="0" distL="0" distR="0">
            <wp:extent cx="{width_emu}" cy="{height_emu}"/>
            <wp:docPr id="{self.image_counter}" name="Picture {self.image_counter}"/>
            <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
                    <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
                        <pic:nvPicPr>
                            <pic:cNvPr id="{self.image_counter}" name="{img_filename}"/>
                            <pic:cNvPicPr/>
                        </pic:nvPicPr>
                        <pic:blipFill>
                            <a:blip r:embed="{rel_id}"/>
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
        </w:drawing></w:r></w:p>'''
        
        self.body_xml.append(img_xml)
        
        # Caption
        if caption:
            self.body_xml.append(f'''<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:i/></w:rPr><w:t xml:space="preserve">{self._escape(caption)}</w:t></w:r></w:p>''')
        self.add_empty_paragraph()
    
    def add_references(self, refs):
        """Add references section"""
        self.add_heading("References", 1)
        for i, ref in enumerate(refs, 1):
            self.body_xml.append(f'''<w:p><w:pPr><w:ind w:left="360" w:hanging="360"/></w:pPr><w:r><w:t xml:space="preserve">[{i}] {self._escape(ref)}</w:t></w:r></w:p>''')
    
    def save(self, filepath):
        """Save the DOCX file"""
        with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
            # [Content_Types].xml
            content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Default Extension="png" ContentType="image/png"/>
    <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
    <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
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
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'''
            for rel_id, img_filename in self.rels:
                doc_rels += f'''
    <Relationship Id="{rel_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{img_filename}"/>'''
            doc_rels += '''
</Relationships>'''
            zf.writestr('word/_rels/document.xml.rels', doc_rels)
            
            # word/styles.xml
            styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:style w:type="paragraph" w:styleId="Normal">
        <w:name w:val="Normal"/>
        <w:rPr><w:sz w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
        <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
    </w:style>
    <w:style w:type="paragraph" w:styleId="Heading1">
        <w:name w:val="heading 1"/>
        <w:pPr><w:spacing w:before="360" w:after="120"/></w:pPr>
        <w:rPr><w:b/><w:sz w:val="32"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:color w:val="2C3E50"/></w:rPr>
    </w:style>
    <w:style w:type="paragraph" w:styleId="Heading2">
        <w:name w:val="heading 2"/>
        <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
        <w:rPr><w:b/><w:sz w:val="28"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:color w:val="34495E"/></w:rPr>
    </w:style>
    <w:style w:type="paragraph" w:styleId="Heading3">
        <w:name w:val="heading 3"/>
        <w:pPr><w:spacing w:before="200" w:after="100"/></w:pPr>
        <w:rPr><w:b/><w:sz w:val="26"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:color w:val="5D6D7E"/></w:rPr>
    </w:style>
    <w:style w:type="table" w:styleId="TableGrid">
        <w:name w:val="Table Grid"/>
        <w:tblPr><w:tblBorders>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        </w:tblBorders></w:tblPr>
    </w:style>
</w:styles>'''
            zf.writestr('word/styles.xml', styles)
            
            # word/document.xml
            body = '\n'.join(self.body_xml)
            document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<w:body>
{body}
</w:body>
</w:document>'''
            zf.writestr('word/document.xml', document)
            
            # Images
            for img_filename, img_bytes in self.images.items():
                zf.writestr(f'word/media/{img_filename}', img_bytes)
    
    def _escape(self, text):
        """Escape XML special characters"""
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')


# ============================================================
# SECTION 3: Chapter Content
# ============================================================

def build_chapter():
    doc = DocxWriter()
    
    # Title
    doc.add_heading("Design Thinking and Strategic Decision-Making: Integrating Human-Centred Innovation with Analytical, Systems, and Creative Approaches for Business Strategy", 1)
    doc.add_empty_paragraph()
    
    # Abstract (no references)
    doc.add_abstract(
        "This chapter provides a comprehensive examination of Design Thinking as a human-centred strategic approach "
        "and its integration with complementary decision-making methodologies including analytical, systems, and creative thinking. "
        "The chapter explores the foundational principles of each approach, establishes comparative frameworks for understanding their "
        "respective strengths and limitations, and develops a synthesized model for strategic decision-making in complex business environments. "
        "Drawing on established literature and contemporary business practice, the analysis demonstrates how organizations can leverage "
        "multiple cognitive and methodological frameworks to address strategic challenges with greater effectiveness. "
        "The chapter further examines practical applications across innovation management, organizational transformation, and strategic "
        "problem-solving, while identifying future directions for design-led organizations operating in increasingly complex and uncertain environments. "
        "A synthesized strategic decision-making framework is proposed that integrates empathy-driven exploration, analytical rigor, "
        "systems awareness, and creative generation into an iterative and adaptive process suitable for contemporary business challenges."
    )
    doc.add_empty_paragraph()
    
    # Keywords
    doc.add_paragraph("Keywords: Design Thinking; Strategic Decision-Making; Systems Thinking; Creative Thinking; Analytical Decision-Making; Business Strategy; Innovation Management; Human-Centred Design; Organizational Transformation", italic=True)
    doc.add_empty_paragraph()
    
    # ================================================================
    # SECTION 1
    # ================================================================
    doc.add_heading("Section 1: Foundations of Design Thinking and Strategic Decision-Making", 1)
    
    # 1.1
    doc.add_heading("1.1 Design Thinking as a Human-Centred Strategic Approach", 2)
    
    doc.add_heading("Evolution and Core Principles of Design Thinking", 3)
    doc.add_paragraph(
        "Design Thinking has evolved from its origins in industrial and product design into a widely recognized strategic methodology "
        "for addressing complex business challenges [1]. The approach draws upon the cognitive processes, creative techniques, and "
        "iterative practices traditionally employed by professional designers, translating these into a structured framework applicable "
        "across diverse organizational contexts [2]. Herbert Simon's foundational work on the sciences of the artificial first articulated "
        "the design process as a systematic approach to problem-solving that could extend beyond traditional design disciplines [3]. "
        "Subsequently, scholars at Stanford University's d.school and the design consultancy IDEO formalized Design Thinking into a "
        "pedagogical and professional methodology centred on human needs, collaborative creativity, and rapid experimentation [4]."
    )
    doc.add_paragraph(
        "The evolution of Design Thinking reflects a broader shift in management theory from purely analytical and optimization-focused "
        "approaches toward methodologies that embrace ambiguity, value qualitative insight, and prioritize stakeholder experience [5]. "
        "This transition recognizes that many strategic business challenges are not well-defined problems amenable to purely quantitative "
        "solutions but rather complex, multi-faceted situations requiring empathic understanding and creative reframing [6]. "
        "The methodology has been adopted by organizations ranging from technology companies and healthcare providers to financial "
        "institutions and government agencies, demonstrating its versatility as a strategic approach [7]."
    )
    
    doc.add_heading("Empathy, Problem Framing, Ideation, Prototyping, and Iteration", 3)
    doc.add_paragraph(
        "The Design Thinking process comprises five interconnected stages that form an iterative rather than strictly linear pathway "
        "(Figure 1). The first stage, empathy, involves deep engagement with stakeholders to understand their experiences, motivations, "
        "and unmet needs [8]. This goes beyond conventional market research by emphasizing immersive observation and genuine understanding "
        "of human behaviour in context. The define stage synthesizes empathic insights into clearly articulated problem statements that "
        "reframe challenges from the stakeholder's perspective rather than the organization's assumptions [9]."
    )
    doc.add_paragraph(
        "Ideation represents the divergent phase of the process, employing techniques such as brainstorming, mind mapping, and analogical "
        "thinking to generate a broad range of potential solutions without premature evaluation [10]. Prototyping translates selected ideas "
        "into tangible representations that can be experienced and evaluated by stakeholders, ranging from simple sketches and storyboards "
        "to functional models [11]. Testing involves presenting prototypes to users, gathering feedback, and using insights to refine "
        "solutions through further iterations. The iterative nature of the process, as illustrated in Figure 1, ensures that solutions "
        "are progressively refined through cycles of creation and validation [12]."
    )
    
    # Insert Figure 1
    fig1_bytes = generate_figure1()
    doc.add_image(fig1_bytes, "Figure 1: Design Thinking Process Framework showing the five iterative stages of Empathize, Define, Ideate, Prototype, and Test with feedback loops enabling continuous refinement.")
    
    doc.add_heading("Role of Design Thinking in Business Strategy and Innovation", 3)
    doc.add_paragraph(
        "Design Thinking's strategic value lies in its capacity to reveal latent customer needs, generate breakthrough innovations, and "
        "create organizational cultures that embrace experimentation and learning [13]. Unlike traditional strategic planning approaches "
        "that rely heavily on quantitative forecasting and competitive analysis, Design Thinking introduces a qualitative, exploratory "
        "dimension that can identify opportunities invisible to purely analytical methods [14]. Research demonstrates that organizations "
        "employing Design Thinking achieve superior innovation outcomes, improved customer satisfaction, and enhanced organizational "
        "agility compared to those relying solely on conventional strategic methodologies [15]."
    )
    doc.add_paragraph(
        "The methodology serves as a bridge between creative exploration and strategic execution, enabling organizations to move from "
        "abstract insights to implementable solutions through structured experimentation. This bridging function is particularly valuable "
        "in environments characterized by high uncertainty, rapid technological change, and evolving stakeholder expectations [16]. "
        "However, Design Thinking alone may be insufficient for addressing the full spectrum of strategic decision-making requirements, "
        "necessitating integration with complementary analytical and systemic approaches."
    )
    doc.add_paragraph(
        "Empirical research on Design Thinking's organizational impact reveals both its transformative potential and its "
        "boundary conditions. Organizations that have successfully implemented Design Thinking at scale report significant "
        "improvements in innovation speed, customer satisfaction, and employee engagement [15]. However, these outcomes are "
        "contingent upon genuine organizational commitment to the methodology's principles rather than superficial adoption "
        "of its techniques. Studies consistently show that Design Thinking produces superior outcomes when integrated into "
        "organizational strategy and culture rather than confined to isolated innovation labs or project-specific applications [16]. "
        "This finding reinforces the argument for comprehensive integration with complementary approaches that collectively "
        "address the full range of strategic decision-making requirements across different organizational contexts and "
        "challenge types. The evidence base for Design Thinking's effectiveness continues to grow, with meta-analytical "
        "studies increasingly confirming its positive impact on innovation performance, stakeholder satisfaction, and "
        "organizational learning when implemented with appropriate methodological rigour and sustained leadership support."
    )
    
    # 1.2
    doc.add_heading("1.2 Analytical Decision-Making Models", 2)
    
    doc.add_heading("Rational Choice Theory and Structured Decision-Making", 3)
    doc.add_paragraph(
        "Analytical decision-making models are grounded in rational choice theory, which posits that optimal decisions result from "
        "systematic evaluation of alternatives against clearly defined criteria [17]. These approaches assume that decision-makers can "
        "identify all relevant options, assess their consequences, and select the alternative that maximizes expected utility. Structured "
        "decision-making frameworks provide methodical procedures for decomposing complex decisions into manageable components, applying "
        "quantitative analysis, and arriving at defensible conclusions [18]."
    )
    doc.add_paragraph(
        "The historical development of rational decision-making theory traces from classical economics through operations research "
        "and management science to contemporary decision analysis. Expected utility theory, prospect theory, and behavioural economics "
        "have progressively refined our understanding of how decisions are and should be made under conditions of uncertainty [17]. "
        "These theoretical foundations inform practical methodologies including decision trees, scenario analysis, and sensitivity "
        "testing that enable organizations to systematically evaluate strategic alternatives while accounting for risk and uncertainty. "
        "The structured nature of these approaches facilitates communication among decision-makers, documentation of reasoning processes, "
        "and retrospective evaluation of decision quality independent of outcomes."
    )
    
    doc.add_heading("Multi-Criteria Decision Analysis (MCDA)", 3)
    doc.add_paragraph(
        "Multi-Criteria Decision Analysis represents one of the most sophisticated analytical approaches to strategic decision-making, "
        "enabling the systematic evaluation of alternatives against multiple, potentially conflicting objectives [19]. MCDA techniques "
        "including the Analytic Hierarchy Process (AHP), TOPSIS, and ELECTRE provide mathematical frameworks for weighting criteria, "
        "scoring alternatives, and synthesizing evaluations into ranked recommendations [20]. These methods are particularly valuable "
        "when decisions involve trade-offs between quantifiable factors such as cost, risk, and performance metrics."
    )
    doc.add_paragraph(
        "The application of MCDA in strategic contexts requires careful attention to the identification and weighting of relevant "
        "criteria, the measurement or estimation of alternative performance against each criterion, and the selection of appropriate "
        "aggregation methods [19]. Stakeholder involvement in criteria identification and weighting processes can enhance the "
        "legitimacy and acceptance of analytical outcomes, while sensitivity analysis reveals the robustness of recommendations to "
        "changes in assumptions. Contemporary applications of MCDA increasingly incorporate uncertainty through probabilistic "
        "performance assessments and robust decision-making techniques that identify alternatives performing well across multiple "
        "possible future scenarios [20]. These developments address traditional criticism of MCDA regarding its dependence on "
        "precise numerical inputs that may not be available in complex strategic contexts."
    )
    
    doc.add_heading("Cost-Benefit Analysis and Evidence-Based Evaluation", 3)
    doc.add_paragraph(
        "Cost-benefit analysis provides a fundamental framework for evaluating strategic alternatives by quantifying their expected "
        "costs and benefits in comparable terms [21]. Evidence-based management extends this principle by requiring that strategic "
        "decisions be grounded in the best available empirical evidence rather than intuition or untested assumptions [22]. These "
        "approaches bring rigor and accountability to decision-making processes, ensuring that resource allocation reflects demonstrable "
        "value creation rather than organizational politics or cognitive biases."
    )
    doc.add_paragraph(
        "The evidence-based approach challenges managers to question their assumptions, seek disconfirming evidence, and base "
        "decisions on systematic reviews of available research rather than personal experience or industry folklore [22]. In practice, "
        "this requires developing organizational capabilities for accessing, interpreting, and applying research evidence alongside "
        "contextual judgment. The integration of evidence-based evaluation with other decision-making approaches recognizes that "
        "quantitative evidence alone may be insufficient for addressing complex strategic questions but provides an essential "
        "foundation for evaluating the likely consequences of alternative courses of action. Cost-benefit analysis, when properly "
        "conducted with appropriate discount rates and comprehensive identification of costs and benefits, provides a powerful "
        "tool for comparing strategic alternatives on a common monetary scale, facilitating transparent and accountable resource "
        "allocation decisions across competing organizational priorities [21]."
    )
    
    doc.add_heading("Strengths and Limitations of Analytical Approaches", 3)
    doc.add_paragraph(
        "Analytical approaches offer significant strengths including transparency, reproducibility, and the capacity to handle "
        "quantifiable complexity systematically [23]. However, they face well-documented limitations including the assumption of "
        "rational behaviour, difficulty in capturing qualitative factors, potential for false precision, and inadequacy when addressing "
        "genuinely novel or ill-defined problems [24]. Herbert Simon's concept of bounded rationality acknowledges that decision-makers "
        "operate under cognitive constraints that limit purely rational analysis, suggesting that complementary approaches may be necessary "
        "for comprehensive strategic decision-making [3]."
    )
    
    # Table 1
    doc.add_table(
        ["Criterion", "Analytical Approaches", "Design Thinking", "Systems Thinking", "Creative Thinking"],
        [
            ["Primary Focus", "Optimization and evaluation", "Human needs and innovation", "Interconnections and wholes", "Novel idea generation"],
            ["Key Strength", "Rigor and precision", "Empathy and user insight", "Holistic understanding", "Breakthrough solutions"],
            ["Primary Limitation", "Assumes rational actors", "Scalability challenges", "Complexity of mapping", "Evaluation difficulty"],
            ["Data Type", "Quantitative metrics", "Qualitative insights", "Relational data", "Conceptual associations"],
            ["Decision Context", "Well-defined problems", "Ambiguous challenges", "Complex systems", "Open-ended exploration"],
            ["Output", "Ranked alternatives", "Validated prototypes", "System maps/models", "Diverse idea sets"],
            ["Time Horizon", "Short to medium-term", "Medium-term", "Long-term", "Variable"],
            ["Stakeholder Role", "Data providers", "Co-creators", "System participants", "Inspiration sources"],
        ],
        "Table 1: Comparative Analysis of Strategic Decision-Making Approaches"
    )
    
    # 1.3
    doc.add_heading("1.3 Systems Thinking and Creative Thinking", 2)
    
    doc.add_heading("Systems Perspective, Interrelationships, and Feedback Loops", 3)
    doc.add_paragraph(
        "Systems thinking provides a conceptual framework for understanding organizations and their environments as complex, "
        "interconnected wholes rather than collections of independent parts [25]. Originating from general systems theory and "
        "cybernetics, this approach emphasizes the importance of relationships, feedback mechanisms, and emergent properties that "
        "arise from the interaction of system components [26]. Peter Senge's influential work on learning organizations demonstrates "
        "how systems thinking enables managers to identify leverage points for intervention, understand unintended consequences of "
        "decisions, and appreciate the dynamic complexity of organizational environments [27]."
    )
    doc.add_paragraph(
        "The application of systems thinking in business strategy involves identifying the boundaries of relevant systems, "
        "mapping the key variables and their interrelationships, and understanding the feedback mechanisms that drive system "
        "behaviour over time [28]. Causal loop diagrams represent reinforcing and balancing feedback loops that create growth, "
        "stability, or oscillation in organizational systems. Stock-and-flow diagrams capture the accumulation of resources and "
        "capabilities that characterize organizational development. These tools enable strategists to develop dynamic hypotheses "
        "about organizational behaviour and to design interventions that work with rather than against systemic forces [25]. "
        "The systems perspective is particularly valuable for understanding why well-intentioned interventions sometimes "
        "produce counterintuitive outcomes and for identifying high-leverage intervention points where modest inputs can "
        "produce significant systemic improvements."
    )
    
    doc.add_heading("Emergence and Non-Linear Business Dynamics", 3)
    doc.add_paragraph(
        "A key insight from systems thinking is that complex business environments exhibit emergent properties and non-linear "
        "dynamics that cannot be predicted from analysis of individual components alone [28]. Small interventions may produce "
        "disproportionate effects, while seemingly significant changes may be absorbed by systemic resistance. This recognition "
        "challenges the assumptions underlying linear strategic planning models and highlights the need for approaches that can "
        "accommodate complexity, uncertainty, and adaptive behaviour [29]."
    )
    doc.add_paragraph(
        "In business contexts, non-linear dynamics manifest as tipping points in market adoption, cascading failures in "
        "supply chains, exponential growth in network effects, and sudden shifts in competitive landscapes [28]. Traditional "
        "linear forecasting methods are poorly suited to anticipating these phenomena, while systems thinking provides conceptual "
        "tools for understanding the conditions under which non-linear transitions become likely and for designing strategies "
        "that are robust to sudden environmental changes. The recognition of emergence challenges reductionist analytical "
        "approaches that seek to understand systems by analysing their components in isolation, reinforcing the need for "
        "holistic approaches that consider the patterns and dynamics that arise from component interactions [29]. Organizations "
        "that develop systems thinking capabilities are better positioned to anticipate disruptions, identify early warning "
        "signals of systemic change, and design adaptive strategies that maintain viability across multiple possible futures."
    )
    
    doc.add_heading("Divergent, Lateral, and Associative Thinking", 3)
    doc.add_paragraph(
        "Creative thinking encompasses a range of cognitive processes including divergent thinking, which generates multiple "
        "potential solutions to open-ended problems; lateral thinking, which approaches challenges from unconventional angles; "
        "and associative thinking, which creates novel connections between seemingly unrelated concepts [30]. These processes "
        "complement analytical approaches by expanding the solution space beyond alternatives that would emerge from systematic "
        "evaluation of known options. Edward de Bono's work on lateral thinking demonstrates how creative techniques can overcome "
        "the constraints of vertical, logical reasoning to produce genuinely novel strategic insights [31]."
    )
    
    doc.add_heading("Role of Creativity in Generating Transformative Solutions", 3)
    doc.add_paragraph(
        "Creativity plays a crucial role in generating transformative strategic solutions that transcend incremental improvement "
        "of existing approaches [32]. In business contexts characterized by disruption and rapid change, the capacity to envision "
        "fundamentally different futures and develop novel strategies for achieving them becomes a critical organizational "
        "capability. Creative thinking provides the generative capacity necessary for strategic innovation, while other "
        "methodologies provide the evaluative and implementation frameworks needed to translate creative insights into "
        "actionable strategies [33]."
    )
    
    # ================================================================
    # SECTION 2
    # ================================================================
    doc.add_heading("Section 2: Comparing Design Thinking with Complementary Approaches", 1)
    
    # 2.1
    doc.add_heading("2.1 Design Thinking versus Analytical Decision-Making", 2)
    
    doc.add_heading("Differences in Assumptions, Processes, and Outcomes", 3)
    doc.add_paragraph(
        "Design Thinking and analytical decision-making differ fundamentally in their epistemological assumptions, procedural "
        "logic, and expected outcomes (Figure 2). Analytical approaches assume that problems can be precisely defined, that "
        "relevant data can be comprehensively gathered, and that optimal solutions can be identified through systematic evaluation "
        "[17]. Design Thinking, conversely, assumes that initial problem definitions are frequently inadequate, that qualitative "
        "human insights are essential for understanding complex challenges, and that solutions emerge through iterative exploration "
        "rather than optimization [34]. These differences reflect deeper distinctions between what Roger Martin characterizes as "
        "reliability-oriented and validity-oriented approaches to management [35]."
    )
    doc.add_paragraph(
        "These fundamental differences have important practical implications for how strategic challenges are approached. "
        "Analytical methods begin with problem definition and proceed through data collection, analysis, and option evaluation "
        "in a predominantly linear sequence. Design Thinking, by contrast, begins with open-ended exploration of stakeholder "
        "experiences and iterates between problem understanding and solution development in a non-linear process [34]. "
        "The outcomes also differ characteristically: analytical approaches produce ranked lists of evaluated alternatives "
        "with associated confidence levels, while Design Thinking produces validated prototypes that embody solutions tested "
        "with real stakeholders. Neither set of outcomes is inherently superior; rather, they address different aspects of "
        "strategic decision-making that together provide a more complete basis for action than either achieves independently [35]. "
        "Understanding these complementarities enables organizations to design decision-making processes that leverage both "
        "approaches appropriately based on the specific requirements of each strategic challenge."
    )
    
    doc.add_heading("Qualitative Insight versus Quantitative Evidence", 3)
    doc.add_paragraph(
        "The tension between qualitative insight and quantitative evidence represents one of the most significant points of "
        "distinction between Design Thinking and analytical approaches. While analytical methods excel at processing quantifiable "
        "data and producing precise recommendations, Design Thinking excels at revealing the contextual, emotional, and experiential "
        "dimensions of strategic challenges that resist quantification [36]. Effective strategic decision-making frequently requires "
        "both types of knowledge, suggesting that integration rather than selection between approaches offers the greatest potential "
        "for comprehensive understanding."
    )
    doc.add_paragraph(
        "Organizations that successfully balance qualitative and quantitative approaches develop richer strategic understanding "
        "than those relying predominantly on either alone. Qualitative insights from Design Thinking can inform the selection of "
        "criteria for quantitative analysis, while quantitative evidence can validate or challenge qualitative observations [36]. "
        "This recursive relationship between qualitative exploration and quantitative validation creates a progressive deepening "
        "of strategic understanding that neither approach achieves independently. The challenge for organizations lies in "
        "developing processes and cultures that value both forms of knowledge equally, avoiding the common trap of privileging "
        "quantitative data simply because it appears more objective while neglecting the contextual richness that qualitative "
        "insights provide for interpreting quantitative findings."
    )
    
    doc.add_heading("Combining Empathy-Driven Exploration with Analytical Evaluation", 3)
    doc.add_paragraph(
        "The complementary nature of Design Thinking and analytical decision-making creates opportunities for integration that "
        "leverages the strengths of both approaches. Empathy-driven exploration can identify opportunities and generate innovative "
        "solutions that analytical methods alone would miss, while subsequent analytical evaluation can assess the feasibility, "
        "viability, and desirability of proposed solutions with greater rigor [37]. This sequential or iterative combination allows "
        "organizations to maintain both creative ambition and analytical discipline in their strategic decision-making processes, "
        "as illustrated in the comparative framework presented in Figure 2."
    )
    
    # Insert Figure 2
    fig2_bytes = generate_figure2()
    doc.add_image(fig2_bytes, "Figure 2: Comparative Framework of Four Decision-Making Approaches showing Design Thinking, Analytical Thinking, Systems Thinking, and Creative Thinking with their integration point.")
    
    # 2.2
    doc.add_heading("2.2 Design Thinking and Systems Thinking", 2)
    
    doc.add_heading("Understanding Stakeholders within Complex Organizational Systems", 3)
    doc.add_paragraph(
        "Design Thinking's focus on individual stakeholder experiences gains significant depth when complemented by systems "
        "thinking's understanding of the organizational and environmental contexts within which stakeholders operate [25]. "
        "Individual needs and behaviours are shaped by systemic factors including organizational structures, institutional "
        "incentives, cultural norms, and market dynamics. Systems thinking enables designers and strategists to appreciate how "
        "these contextual factors influence stakeholder behaviour and how proposed solutions may interact with existing systemic "
        "patterns [38]."
    )
    doc.add_paragraph(
        "The integration of Design Thinking's stakeholder focus with systems thinking's contextual analysis creates a "
        "particularly powerful approach for addressing complex organizational challenges. Where Design Thinking might focus "
        "on the experience of an individual patient in a healthcare system, systems thinking expands the view to encompass "
        "the network of relationships, institutional constraints, and resource flows that shape that experience [39]. "
        "This expanded perspective does not diminish the importance of individual experience but rather provides a richer "
        "understanding of the factors that create and sustain particular experiential patterns, enabling more effective "
        "intervention design that addresses systemic root causes rather than symptomatic manifestations. The combined "
        "approach recognizes that stakeholders are embedded within systems and that sustainable improvements in stakeholder "
        "experience require interventions that address systemic as well as individual factors."
    )
    
    doc.add_heading("Mapping Relationships, Feedback Loops, and Unintended Consequences", 3)
    doc.add_paragraph(
        "Systems mapping techniques including causal loop diagrams, stock-and-flow models, and stakeholder ecosystem maps provide "
        "tools for visualizing the complex relationships that characterize organizational environments [39]. When integrated with "
        "Design Thinking, these mapping approaches help teams anticipate unintended consequences of interventions, identify "
        "reinforcing and balancing feedback loops that may amplify or dampen the effects of innovations, and understand the "
        "broader systemic implications of solutions designed to address specific stakeholder needs [40]."
    )
    
    doc.add_heading("Using Systems Thinking to Strengthen Strategic Problem Framing", 3)
    doc.add_paragraph(
        "Systems thinking strengthens the problem framing stage of Design Thinking by expanding the boundaries of analysis "
        "beyond immediate stakeholder needs to encompass the broader systemic context [41]. This expanded framing helps avoid "
        "the trap of solving symptoms rather than root causes and enables the identification of leverage points where "
        "interventions can produce cascading positive effects throughout the system. The combination of empathic stakeholder "
        "understanding with systemic awareness creates a more comprehensive foundation for strategic problem-solving than either "
        "approach provides independently."
    )
    
    # Table 2
    doc.add_table(
        ["Integration Dimension", "Design Thinking Contribution", "Systems Thinking Contribution", "Combined Benefit"],
        [
            ["Problem Framing", "Stakeholder empathy and needs identification", "Contextual analysis and boundary setting", "Comprehensive problem understanding"],
            ["Analysis Depth", "Individual experience mapping", "Relationship and feedback mapping", "Multi-level systemic insight"],
            ["Solution Scope", "User-centred innovation", "System-level intervention design", "Solutions addressing root causes"],
            ["Risk Assessment", "User testing and validation", "Unintended consequence identification", "Robust solution evaluation"],
            ["Implementation", "Iterative prototyping", "Leverage point identification", "Strategic and targeted deployment"],
            ["Evaluation", "User satisfaction metrics", "System health indicators", "Holistic outcome measurement"],
        ],
        "Table 2: Integration of Design Thinking and Systems Thinking Contributions"
    )
    
    # 2.3
    doc.add_heading("2.3 Design Thinking and Creative Thinking", 2)
    
    doc.add_heading("Relationship Between Creativity and Design Thinking", 3)
    doc.add_paragraph(
        "Design Thinking incorporates creative thinking as a fundamental component, particularly within the ideation stage, "
        "but extends beyond pure creativity by providing a structured framework for channelling creative energy toward "
        "addressing validated human needs [42]. The relationship between the two is symbiotic: Design Thinking provides "
        "creative thinking with direction and purpose through empathic problem framing, while creative thinking provides "
        "Design Thinking with the generative capacity necessary for producing innovative solutions that transcend conventional "
        "responses to identified challenges."
    )
    
    doc.add_heading("Divergent and Convergent Thinking Processes", 3)
    doc.add_paragraph(
        "Both Design Thinking and creative problem-solving rely on alternating phases of divergent and convergent thinking. "
        "Divergent phases expand the range of possibilities by suspending judgment and encouraging quantity and variety of "
        "ideas, while convergent phases narrow options through evaluation, synthesis, and selection [30]. Design Thinking "
        "structures these alternations within a broader process framework that connects creative generation to stakeholder "
        "needs and implementation requirements, ensuring that creativity serves strategic rather than purely aesthetic purposes [43]."
    )
    
    doc.add_heading("Using Creative Techniques to Overcome Conventional Strategic Assumptions", 3)
    doc.add_paragraph(
        "Creative techniques including analogical reasoning, constraint removal, reverse brainstorming, and provocation "
        "methods offer powerful tools for challenging the conventional assumptions that often constrain strategic thinking [31]. "
        "When embedded within the Design Thinking process, these techniques help organizations move beyond incremental "
        "improvements to envision fundamentally different approaches to creating and delivering value. The combination of "
        "creative disruption with empathic validation ensures that unconventional ideas are evaluated against real human "
        "needs rather than dismissed by organizational conservatism or embraced without critical assessment [44]."
    )
    doc.add_paragraph(
        "The practical integration of creative thinking with Design Thinking's structured process creates a powerful "
        "engine for strategic innovation. Techniques such as SCAMPER (Substitute, Combine, Adapt, Modify, Put to other uses, "
        "Eliminate, Reverse), morphological analysis, and biomimicry provide systematic approaches to creative generation that "
        "can be embedded within the ideation phase of Design Thinking [32]. These techniques prevent the common problem of "
        "ideation sessions producing only incremental variations of existing solutions by providing structured provocations "
        "that push thinking beyond familiar territory. When combined with Design Thinking's empathic problem framing, these "
        "creative techniques are directed toward generating solutions that are not merely novel but also meaningfully responsive "
        "to validated stakeholder needs, creating the foundation for innovations that are both creative and purposeful [33]."
    )
    doc.add_paragraph(
        "The relationship between Design Thinking and creative thinking thus operates at multiple levels: creative thinking "
        "provides the generative engine that drives innovation within the Design Thinking process, while Design Thinking provides "
        "the structural framework that channels creative energy toward addressing genuine human needs and creates mechanisms "
        "for evaluating and refining creative outputs through iterative stakeholder engagement. Together, they form a powerful "
        "combination that produces innovations characterised by both originality and relevance, addressing the dual challenge "
        "of generating truly novel solutions while ensuring those solutions create meaningful value for intended beneficiaries [42]. "
        "This complementary relationship demonstrates that creativity, far from being incompatible with structure, often "
        "thrives within well-designed frameworks that provide both direction and freedom for creative exploration."
    )
    
    # ================================================================
    # SECTION 3
    # ================================================================
    doc.add_heading("Section 3: Integrating Approaches for Business Strategy", 1)
    
    # 3.1
    doc.add_heading("3.1 Context-Dependent Selection of Decision-Making Methods", 2)
    
    doc.add_heading("Matching Methodologies to Problem Complexity and Uncertainty", 3)
    doc.add_paragraph(
        "Effective strategic decision-making requires matching methodological approaches to the specific characteristics of "
        "the decision context, including problem complexity, uncertainty levels, time constraints, and stakeholder requirements "
        "[23]. The Cynefin framework, developed by Dave Snowden, provides a useful heuristic for categorizing decision contexts "
        "as simple, complicated, complex, or chaotic, each requiring different approaches [45]. Simple and complicated contexts "
        "may be adequately addressed by analytical methods, while complex and chaotic contexts typically benefit from the "
        "exploratory, iterative approaches characteristic of Design Thinking and creative problem-solving."
    )
    
    doc.add_heading("Organizational Culture, Stakeholder Requirements, and Resource Constraints", 3)
    doc.add_paragraph(
        "The selection of decision-making approaches must also account for organizational context factors including cultural "
        "readiness for experimentation, stakeholder tolerance for ambiguity, and available resources for extended exploration "
        "processes [14]. Organizations with strong analytical cultures may benefit from introducing Design Thinking gradually "
        "as a complement to existing methods, while organizations with limited resources may need to select approaches that "
        "provide the greatest insight within available time and budget constraints. Understanding these contextual factors "
        "enables strategic leaders to configure decision-making processes that are both methodologically appropriate and "
        "practically feasible within their organizational settings."
    )
    doc.add_paragraph(
        "Research on organizational decision-making consistently demonstrates that effective strategic processes adapt their "
        "methodology to contextual requirements rather than applying a single approach uniformly [14]. Organizations that develop "
        "meta-cognitive awareness of their decision-making processes, understanding when different approaches are most appropriate "
        "and how to transition between them, achieve superior strategic outcomes compared to those that apply familiar methods "
        "regardless of context. This adaptive capability requires investment in developing diverse methodological competencies "
        "and creating organizational structures that enable flexible configuration of decision-making processes based on real-time "
        "assessment of challenge characteristics and available resources."
    )
    
    doc.add_heading("Decision-Making in Routine, Complex, and High-Stakes Situations", 3)
    doc.add_paragraph(
        "Different decision situations call for different methodological emphases. Routine decisions benefit from established "
        "analytical frameworks that promote efficiency and consistency. Complex decisions involving multiple stakeholders, "
        "uncertain outcomes, and potential for unintended consequences benefit from the integration of Design Thinking's "
        "empathic exploration with systems thinking's contextual analysis [38]. High-stakes decisions requiring both innovation "
        "and accountability may benefit from a comprehensive approach that combines creative generation with rigorous analytical "
        "evaluation, ensuring that novel solutions are subjected to appropriate scrutiny before implementation."
    )
    
    # Table 3
    doc.add_table(
        ["Decision Context", "Primary Methodology", "Supporting Approaches", "Key Activities", "Expected Outcome"],
        [
            ["Routine/Simple", "Analytical methods", "Standard protocols", "Cost-benefit analysis, benchmarking", "Optimized efficiency"],
            ["Complicated", "MCDA/Analytical", "Expert consultation", "Multi-criteria evaluation, risk analysis", "Best-evaluated option"],
            ["Complex/Uncertain", "Design Thinking", "Systems + Creative", "Empathy research, prototyping, mapping", "Validated innovation"],
            ["High-Stakes", "Integrated framework", "All approaches", "Comprehensive exploration and evaluation", "Robust strategic choice"],
            ["Disruptive/Novel", "Creative Thinking", "Design + Systems", "Divergent ideation, scenario planning", "Breakthrough strategies"],
            ["Systemic/Wicked", "Systems Thinking", "Design + Analytical", "Causal mapping, stakeholder analysis", "Leverage interventions"],
        ],
        "Table 3: Context-Dependent Methodology Selection Framework"
    )
    
    # 3.2
    doc.add_heading("3.2 A Synthesized Strategic Decision-Making Framework", 2)
    
    doc.add_heading("Integrating Empathy and Ideation from Design Thinking", 3)
    doc.add_paragraph(
        "The synthesized framework proposed in this chapter (Figure 3) integrates the distinctive contributions of each "
        "thinking approach into a coherent strategic decision-making process. Design Thinking contributes empathic research "
        "methods for understanding stakeholder needs, structured ideation techniques for generating innovative solutions, and "
        "iterative prototyping processes for validating proposals through direct stakeholder engagement [4]. These elements "
        "ensure that strategic decisions are grounded in genuine understanding of human needs and validated through experiential "
        "testing rather than assumptions."
    )
    
    doc.add_heading("Applying Analytical Rigor through Quantitative Decision Models", 3)
    doc.add_paragraph(
        "Analytical methods contribute essential evaluative capabilities to the synthesized framework, enabling systematic "
        "assessment of strategic alternatives against defined criteria. Multi-criteria decision analysis, financial modelling, "
        "risk assessment, and evidence-based evaluation provide the quantitative rigor necessary for justifying strategic "
        "investments and ensuring accountability [19]. Within the synthesized framework, analytical methods are employed "
        "following creative generation to evaluate and select among innovative options rather than constraining the initial "
        "exploration of possibilities."
    )
    doc.add_paragraph(
        "The sequencing of analytical evaluation after creative generation is a critical design principle of the synthesized "
        "framework. Premature analytical evaluation can stifle innovation by eliminating novel ideas before they have been "
        "sufficiently developed to demonstrate their potential [20]. By protecting the creative and empathic phases from "
        "premature analytical scrutiny, the framework ensures that a diverse range of innovative options is generated before "
        "rigorous evaluation begins. This principle does not diminish the importance of analytical evaluation but rather "
        "ensures that analysis is applied to a sufficiently rich set of alternatives to produce genuinely optimal selections "
        "rather than merely confirming pre-existing organizational preferences or incrementally improving current approaches."
    )
    
    doc.add_heading("Incorporating Systems Awareness and Creative Exploration", 3)
    doc.add_paragraph(
        "Systems thinking contributes contextual awareness, stakeholder mapping, and understanding of dynamic complexity "
        "to the synthesized framework. This systemic perspective helps ensure that proposed strategies account for broader "
        "organizational and environmental factors, anticipate potential unintended consequences, and identify leverage points "
        "for maximum impact [27]. Creative thinking contributes generative techniques that expand the solution space beyond "
        "conventional alternatives, ensuring that the framework produces genuinely innovative rather than merely optimized "
        "outcomes."
    )
    
    doc.add_heading("Developing an Iterative and Adaptive Decision-Making Process", 3)
    doc.add_paragraph(
        "The synthesized framework operates as an iterative and adaptive process rather than a linear sequence, recognizing "
        "that strategic understanding develops progressively through cycles of exploration, analysis, and validation (Figure 3). "
        "Each iteration deepens understanding of the strategic challenge, expands the range of potential responses, and "
        "refines proposed solutions through evidence and stakeholder feedback [46]. This iterative structure accommodates the "
        "inherent uncertainty of complex strategic environments while maintaining sufficient analytical discipline to support "
        "confident decision-making."
    )
    
    # Insert Figure 3
    fig3_bytes = generate_figure3()
    doc.add_image(fig3_bytes, "Figure 3: Synthesized Strategic Decision-Making Model integrating Design Thinking, Systems Thinking, and Analytical Methods into an iterative six-stage process with continuous feedback loops.")
    
    # 3.3
    doc.add_heading("3.3 Practical Applications and Business Examples", 2)
    
    doc.add_heading("Innovation and New Product Development", 3)
    doc.add_paragraph(
        "The integrated framework finds natural application in innovation and new product development contexts where "
        "organizations must balance creative exploration with market validation and financial viability assessment [15]. "
        "Leading technology companies including Apple, Google, and Samsung have adopted approaches that combine empathic "
        "user research with rapid prototyping, analytical market assessment, and systems-level consideration of ecosystem "
        "effects. These organizations demonstrate that superior innovation outcomes result from the integration of multiple "
        "thinking approaches rather than reliance on any single methodology."
    )
    doc.add_paragraph(
        "The innovation process in leading organizations typically begins with ethnographic research and contextual inquiry "
        "to identify unmet needs and latent opportunities, drawing on Design Thinking's empathic methods [8]. This is followed "
        "by collaborative ideation sessions that draw on creative thinking techniques to generate diverse solution concepts. "
        "Systems thinking then examines how proposed innovations might interact with existing product ecosystems, user workflows, "
        "and market dynamics. Analytical methods including market sizing, financial modelling, and technology readiness assessment "
        "evaluate the commercial viability of promising concepts. This multi-stage, multi-methodology approach ensures that "
        "innovation efforts are simultaneously human-centred, creatively ambitious, systemically aware, and commercially viable."
    )
    doc.add_paragraph(
        "For example, the development of breakthrough products requires initial empathic research to identify latent user "
        "needs, creative ideation to envision novel solutions, systems analysis to understand ecosystem implications, and "
        "analytical evaluation to assess market potential and financial viability. This multi-methodological approach ensures "
        "that innovation is simultaneously human-centred, technically feasible, systemically viable, and financially sound [13]."
    )
    
    doc.add_heading("Business Model Transformation and Organizational Change", 3)
    doc.add_paragraph(
        "Business model transformation represents a particularly complex strategic challenge that benefits from integrated "
        "approaches. Design Thinking contributes stakeholder empathy and iterative experimentation for developing new value "
        "propositions; systems thinking provides understanding of organizational interdependencies and change dynamics; "
        "analytical methods enable financial modelling and risk assessment; and creative thinking generates novel business "
        "model configurations [35]. Organizations undertaking digital transformation, sustainability transitions, or market "
        "repositioning can leverage this integrated approach to navigate complexity while maintaining strategic coherence."
    )
    
    doc.add_heading("Strategic Problem-Solving under Uncertainty", 3)
    doc.add_paragraph(
        "Strategic environments characterized by high uncertainty, including emerging markets, technological disruption, "
        "and regulatory change, demand decision-making approaches that can accommodate ambiguity while maintaining "
        "directional clarity [45]. The integrated framework addresses this challenge by combining Design Thinking's "
        "comfort with ambiguity and iterative learning with analytical methods' capacity for structured evaluation and "
        "systems thinking's appreciation of dynamic complexity. This combination enables organizations to take strategic "
        "action in uncertain environments while maintaining the flexibility to adapt as circumstances evolve."
    )
    
    doc.add_heading("Examples Demonstrating Complementary Use of Multiple Approaches", 3)
    doc.add_paragraph(
        "Consider a healthcare organization seeking to improve patient outcomes while reducing costs. Design Thinking "
        "enables deep understanding of patient and clinician experiences; systems thinking maps the complex interactions "
        "between clinical processes, information systems, regulatory requirements, and organizational structures; "
        "analytical methods evaluate the cost-effectiveness of proposed interventions; and creative thinking generates "
        "novel approaches to care delivery that transcend incremental process improvement [7]. The integration of these "
        "approaches produces solutions that are simultaneously patient-centred, systemically aware, analytically justified, "
        "and creatively ambitious, as summarized in Table 1."
    )
    
    # ================================================================
    # SECTION 4
    # ================================================================
    doc.add_heading("Section 4: Future Directions and Implications for Design-Led Organizations", 1)
    
    # 4.1
    doc.add_heading("4.1 Addressing the Limitations of Design Thinking", 2)
    
    doc.add_heading("Scalability and Implementation Challenges", 3)
    doc.add_paragraph(
        "Despite its demonstrated value in generating innovative solutions, Design Thinking faces significant challenges "
        "when scaling from individual projects to organization-wide strategic practice [6]. The methodology's reliance on "
        "intensive qualitative research, collaborative workshops, and iterative prototyping creates resource demands that "
        "may be difficult to sustain across large organizations or extended time horizons. Addressing these scalability "
        "challenges requires developing lightweight variants of Design Thinking that maintain core principles while "
        "reducing resource requirements, as well as digital tools and platforms that can support distributed design "
        "thinking processes across organizational boundaries."
    )
    
    doc.add_heading("Integration of Quantitative Data and Evidence", 3)
    doc.add_paragraph(
        "A frequently cited limitation of Design Thinking is its relative weakness in incorporating quantitative data "
        "and evidence into decision-making processes [22]. While the methodology excels at generating qualitative insights "
        "and creative solutions, it provides limited guidance for evaluating alternatives using quantitative criteria or "
        "for integrating empirical evidence from controlled studies. The synthesized framework proposed in this chapter "
        "addresses this limitation by explicitly incorporating analytical evaluation stages that complement Design Thinking's "
        "qualitative strengths with quantitative rigor, ensuring that innovative solutions are assessed against evidence-based "
        "criteria before implementation."
    )
    
    doc.add_heading("Application in High-Risk and High-Stakes Business Environments", 3)
    doc.add_paragraph(
        "High-risk business environments including financial services, healthcare, and critical infrastructure present "
        "particular challenges for Design Thinking's experimental approach, as the consequences of prototype failures may "
        "be unacceptable [21]. In these contexts, the integration of analytical risk assessment and systems-level safety "
        "analysis with Design Thinking's exploratory methods becomes essential. Organizations operating in high-stakes "
        "environments can adapt the integrated framework by emphasizing analytical evaluation and systemic risk mapping "
        "while maintaining Design Thinking's creative and empathic elements within appropriate safety boundaries."
    )
    doc.add_paragraph(
        "The concept of bounded experimentation provides a practical framework for applying Design Thinking principles in "
        "high-risk environments. Rather than full-scale prototyping and testing, organizations can employ simulation, scenario "
        "analysis, and carefully designed pilot studies that provide experiential learning while managing downside risk [23]. "
        "Digital twins and computational modelling enable organizations to prototype and test strategic interventions in "
        "virtual environments before committing to physical implementation, combining Design Thinking's iterative experimental "
        "approach with the risk management requirements of high-stakes decision contexts. This integration demonstrates that "
        "the principles of Design Thinking can be adapted to virtually any decision context when combined with appropriate "
        "complementary methods for managing context-specific constraints and risks."
    )
    
    # Table 4
    doc.add_table(
        ["Challenge Area", "Current Limitation", "Proposed Integration Solution", "Implementation Approach"],
        [
            ["Scalability", "Resource-intensive qualitative methods", "Digital DT tools and lean variants", "Platform-supported distributed processes"],
            ["Quantitative Integration", "Weak incorporation of numerical data", "Analytical evaluation stages post-ideation", "MCDA and financial modelling checkpoints"],
            ["High-Stakes Contexts", "Risk of experimental failure", "Systems safety analysis integration", "Bounded experimentation with risk mapping"],
            ["Measurement", "Difficulty quantifying DT outcomes", "Balanced scorecard with mixed metrics", "Both qualitative and quantitative KPIs"],
            ["Cultural Resistance", "Conflicts with analytical cultures", "Gradual integration starting with pilots", "Hybrid teams combining analysts and designers"],
            ["Long-term Sustainability", "Project-based rather than ongoing", "Embedding DT in organizational routines", "Continuous improvement and learning systems"],
        ],
        "Table 4: Addressing Design Thinking Limitations through Integrated Approaches"
    )
    
    # 4.2
    doc.add_heading("4.2 Building Agile and Forward-Looking Organizations", 2)
    
    doc.add_heading("Developing Design-Led Organizational Cultures", 3)
    doc.add_paragraph(
        "Building design-led organizational cultures requires more than adopting Design Thinking as a methodology; it "
        "demands fundamental shifts in organizational values, structures, and processes that prioritize human-centred "
        "innovation, collaborative problem-solving, and continuous learning [16]. Design-led organizations cultivate "
        "psychological safety that encourages experimentation and learning from failure, cross-functional collaboration "
        "that brings diverse perspectives to strategic challenges, and customer proximity that maintains empathic "
        "connection with stakeholder needs throughout strategic decision-making processes."
    )
    doc.add_paragraph(
        "The development of design-led cultures is supported by leadership commitment to human-centred values, investment "
        "in design capabilities and infrastructure, and alignment of performance management systems with innovation and "
        "stakeholder value creation rather than purely financial metrics [15]. Organizations including IBM, Procter and "
        "Gamble, and Intuit have demonstrated how systematic investment in design capabilities can transform organizational "
        "culture and strategic performance over extended time horizons, providing models for others seeking similar "
        "transformations."
    )
    doc.add_paragraph(
        "The transformation toward design-led organizational culture is not merely an adoption of new methodologies but a "
        "fundamental reconceptualization of how organizations understand and respond to strategic challenges [16]. Design-led "
        "organizations cultivate what scholars term 'design maturity' across multiple dimensions including leadership commitment, "
        "process integration, capability development, and outcome measurement. At the highest levels of design maturity, "
        "Design Thinking principles become embedded in organizational DNA, influencing not only product and service development "
        "but also internal processes, organizational structures, and strategic decision-making at the executive level. This "
        "cultural transformation requires sustained investment over multiple years and consistent leadership commitment to "
        "human-centred values even when short-term pressures might favour more expedient analytical approaches."
    )
    
    doc.add_heading("Collaboration among Strategists, Analysts, Designers, and Managers", 3)
    doc.add_paragraph(
        "The integrated framework requires effective collaboration among professionals with diverse methodological "
        "backgrounds including strategists, data analysts, designers, and operational managers [37]. This collaboration "
        "must transcend traditional functional boundaries to create interdisciplinary teams capable of applying multiple "
        "thinking approaches to strategic challenges. Successful collaboration requires shared language, mutual respect "
        "for different forms of expertise, and structured processes that create space for both creative exploration "
        "and analytical evaluation within the same decision-making process."
    )
    doc.add_paragraph(
        "Effective interdisciplinary collaboration requires organizational structures that facilitate regular interaction "
        "between professionals with different methodological orientations, including co-located teams, cross-functional "
        "project structures, and rotation programmes that expose individuals to diverse approaches [37]. Additionally, "
        "organizations must develop shared frameworks and vocabularies that enable professionals from different backgrounds "
        "to communicate effectively about complex strategic challenges without requiring each to become expert in all "
        "methodological traditions. The T-shaped professional model, combining deep expertise in one domain with broad "
        "familiarity across others, provides a useful ideal for individual capability development, while team composition "
        "strategies ensure that collective capabilities span the full range of methodological approaches needed for "
        "integrated strategic thinking."
    )
    
    doc.add_heading("Strengthening Organizational Adaptability and Innovation Capabilities", 3)
    doc.add_paragraph(
        "Organizations that successfully integrate multiple thinking approaches develop enhanced adaptability and "
        "innovation capabilities that create sustainable competitive advantage [46]. The capacity to rapidly sense "
        "stakeholder needs through empathic research, understand systemic implications through systems analysis, "
        "generate creative alternatives through divergent thinking, and evaluate options through analytical assessment "
        "creates a comprehensive strategic capability that is difficult for competitors to replicate. This integrated "
        "capability enables organizations to respond effectively to disruption, identify emerging opportunities, and "
        "develop innovative strategies while maintaining the analytical discipline necessary for responsible resource allocation."
    )
    doc.add_paragraph(
        "The concept of dynamic capabilities, as articulated by Teece and colleagues, provides theoretical grounding for "
        "understanding how integrated strategic thinking contributes to sustainable competitive advantage [46]. Dynamic "
        "capabilities encompass an organization's ability to sense opportunities and threats, seize them through innovative "
        "strategic responses, and reconfigure organizational resources and routines to maintain competitive fitness. The "
        "integrated framework directly supports each of these capabilities: empathic research and systems mapping support "
        "sensing; creative ideation and Design Thinking prototyping support seizing; and the iterative, adaptive nature of "
        "the framework supports ongoing reconfiguration. Organizations that develop these integrated capabilities position "
        "themselves for sustained strategic advantage in dynamic environments where the ability to learn and adapt "
        "continuously is more valuable than any static competitive position."
    )
    
    # 4.3
    doc.add_heading("4.3 Future Opportunities for Integrated Strategic Thinking", 2)
    
    doc.add_heading("Emerging Trends in Hybrid Decision-Making", 3)
    doc.add_paragraph(
        "The future of strategic decision-making lies in increasingly sophisticated hybrid approaches that dynamically "
        "combine elements from multiple methodological traditions based on real-time assessment of decision context "
        "requirements [34]. Emerging trends include the development of adaptive decision-making frameworks that "
        "automatically adjust methodological emphasis based on problem characteristics, collaborative platforms that "
        "support distributed application of integrated approaches, and educational programmes that develop versatile "
        "strategic thinkers capable of fluently applying multiple methodologies (Figure 4). These trends suggest a "
        "future in which the boundaries between distinct methodological approaches become increasingly fluid, giving "
        "way to integrated strategic thinking capabilities."
    )
    doc.add_paragraph(
        "The emergence of hybrid decision-making approaches reflects growing recognition that the most effective strategic "
        "processes draw selectively from multiple methodological traditions rather than adhering rigidly to any single approach [34]. "
        "Professional education is increasingly emphasizing T-shaped competency profiles that combine deep expertise in one "
        "methodological domain with sufficient breadth across others to enable effective collaboration and contextual methodology "
        "selection. Organizations are developing internal academies and capability development programmes that build integrated "
        "strategic thinking competencies across leadership teams, ensuring that strategic decisions benefit from diverse "
        "methodological perspectives regardless of which functional area initiates the decision-making process."
    )
    
    doc.add_heading("Digital Technologies and AI-Supported Strategic Analysis", 3)
    doc.add_paragraph(
        "Artificial intelligence and digital technologies offer significant opportunities for enhancing integrated "
        "strategic thinking. Machine learning algorithms can process large volumes of qualitative stakeholder data to "
        "identify patterns and insights that complement traditional empathic research methods [47]. Natural language "
        "processing can analyse stakeholder communications to detect emerging needs and sentiments. Simulation tools "
        "can model complex system dynamics to support systems thinking. Generative AI can augment creative ideation by "
        "producing novel combinations and variations of human-generated concepts. These technological capabilities, "
        "when thoughtfully integrated with human judgment and empathy, promise to enhance the speed, scale, and "
        "sophistication of integrated strategic decision-making processes, as envisioned in Figure 4."
    )
    
    # Insert Figure 4
    fig4_bytes = generate_figure4()
    doc.add_image(fig4_bytes, "Figure 4: Future Integrated Strategic Thinking Ecosystem showing the convergence of AI and Digital Technology, Data Analytics, Sustainability, Stakeholder Value, Organizational Agility, Innovation Culture, and Systems Awareness around a Design-Led Strategy core.")
    
    doc.add_heading("Developing Resilient, Sustainable, and Stakeholder-Oriented Business Strategies", 3)
    doc.add_paragraph(
        "The integration of Design Thinking with complementary approaches provides a foundation for developing business "
        "strategies that are simultaneously resilient to disruption, environmentally and socially sustainable, and oriented "
        "toward creating value for diverse stakeholders [40]. Design Thinking's empathic focus ensures that strategies "
        "remain connected to human needs and values; systems thinking ensures that strategies account for environmental "
        "and social systemic effects; analytical methods ensure that strategies are financially viable and efficiently "
        "implemented; and creative thinking ensures that strategies transcend conventional approaches to address "
        "contemporary challenges including climate change, social inequality, and technological disruption."
    )
    doc.add_paragraph(
        "The sustainability imperative adds particular urgency to the development of integrated strategic thinking "
        "capabilities. Organizations must increasingly balance economic performance with environmental responsibility and "
        "social impact, navigating trade-offs that require both empathic understanding of diverse stakeholder perspectives "
        "and analytical evaluation of alternative courses of action [40]. Design Thinking's human-centred focus ensures "
        "that sustainability strategies remain connected to genuine human needs and aspirations rather than becoming "
        "purely technical exercises in emissions reduction or resource optimization. Systems thinking provides essential "
        "understanding of the interconnections between economic, environmental, and social systems that determine the "
        "overall impact of organizational strategies. Analytical methods enable rigorous assessment of trade-offs and "
        "measurement of progress toward sustainability goals. Creative thinking generates novel approaches to creating "
        "shared value that transcend the assumption of zero-sum trade-offs between profit and purpose."
    )
    doc.add_paragraph(
        "As organizations increasingly face pressure to create value for multiple stakeholders simultaneously including "
        "shareholders, employees, customers, communities, and the natural environment, the integrated framework offered "
        "in this chapter provides a methodological foundation for navigating these complex demands. By combining empathic "
        "understanding of diverse stakeholder perspectives with systemic awareness of interconnections and trade-offs, "
        "analytical evaluation of alternatives, and creative generation of novel value creation approaches, organizations "
        "can develop strategies that honour their obligations to multiple constituencies while maintaining competitive "
        "viability and strategic coherence in an increasingly complex world [44]."
    )
    
    # Conclusion
    doc.add_heading("Conclusion", 1)
    doc.add_paragraph(
        "This chapter has demonstrated that Design Thinking, while powerful as a human-centred approach to strategic "
        "innovation, achieves its greatest potential when integrated with complementary methodologies including analytical "
        "decision-making, systems thinking, and creative thinking. Each approach contributes distinctive capabilities: "
        "Design Thinking provides empathic understanding and iterative validation; analytical methods provide quantitative "
        "rigor and evidence-based evaluation; systems thinking provides holistic awareness and understanding of dynamic "
        "complexity; and creative thinking provides the generative capacity for breakthrough solutions. The synthesized "
        "strategic decision-making framework proposed in this chapter offers a practical model for integrating these "
        "approaches into a coherent, iterative process suitable for addressing the complex strategic challenges facing "
        "contemporary organizations."
    )
    doc.add_paragraph(
        "The framework addresses a significant gap in current strategic management literature by providing a structured "
        "approach to integrating methodologies that are typically presented as alternative or competing approaches. Rather "
        "than advocating for the superiority of any single methodology, the chapter demonstrates that each approach provides "
        "distinctive and complementary contributions that together create a more comprehensive foundation for strategic action "
        "than any achieves independently. The context-dependent selection framework (Table 3) provides practical guidance for "
        "matching methodological approaches to problem characteristics, while the synthesized model (Figure 3) demonstrates "
        "how multiple approaches can be sequenced within a coherent decision-making process."
    )
    doc.add_paragraph(
        "The implications for practice are significant. Organizations seeking to enhance their strategic decision-making "
        "capabilities should invest in developing integrated methodological competencies that combine design, analytical, "
        "systemic, and creative thinking. This requires building interdisciplinary teams, creating organizational cultures "
        "that value multiple forms of knowledge, and developing decision-making processes that create appropriate space "
        "for both exploration and evaluation. As digital technologies and artificial intelligence increasingly augment "
        "human strategic capabilities, the integrated framework provides a foundation for leveraging these technologies "
        "while maintaining the human-centred values and empathic connection that ensure strategies serve genuine human "
        "needs and create sustainable value for all stakeholders."
    )
    doc.add_paragraph(
        "Future research should focus on developing more precise contingency models for methodology selection, creating "
        "validated instruments for measuring integrated strategic thinking capabilities, and conducting longitudinal studies "
        "of organizations that have adopted integrated approaches to assess their long-term strategic performance relative "
        "to organizations employing single-methodology strategies. Additionally, the role of artificial intelligence in "
        "augmenting and potentially automating aspects of integrated strategic thinking requires careful investigation to "
        "understand both its potential benefits and its limitations in contexts requiring human empathy, creative insight, "
        "and ethical judgment. The chapter contributes to the growing body of scholarship advocating for methodological "
        "pluralism in strategic management, providing both theoretical justification and practical guidance for organizations "
        "seeking to develop more comprehensive, adaptive, and human-centred approaches to strategic decision-making in an "
        "era of unprecedented complexity and rapid change."
    )
    
    # References
    references = [
        "Brown, T. (2009). Change by Design: How Design Thinking Transforms Organizations and Inspires Innovation. Harper Business, New York.",
        "Cross, N. (2011). Design Thinking: Understanding How Designers Think and Work. Berg Publishers, Oxford.",
        "Simon, H.A. (1969). The Sciences of the Artificial. MIT Press, Cambridge, MA.",
        "Kelley, T. and Kelley, D. (2013). Creative Confidence: Unleashing the Creative Potential Within Us All. Crown Business, New York.",
        "Liedtka, J. (2018). Why Design Thinking Works. Harvard Business Review, 96(5), pp. 72-79.",
        "Kolko, J. (2015). Design Thinking Comes of Age. Harvard Business Review, 93(9), pp. 66-71.",
        "Roberts, J.P. et al. (2016). A Design Thinking Framework for Healthcare Management and Innovation. Healthcare, 4(1), pp. 11-14.",
        "Kouprie, M. and Visser, F.S. (2009). A Framework for Empathy in Design: Stepping into and out of the User's Life. Journal of Engineering Design, 20(5), pp. 437-448.",
        "Dorst, K. (2011). The Core of Design Thinking and its Application. Design Studies, 32(6), pp. 521-532.",
        "Osborn, A.F. (1953). Applied Imagination: Principles and Procedures of Creative Problem-Solving. Charles Scribner's Sons, New York.",
        "Buchenau, M. and Suri, J.F. (2000). Experience Prototyping. Proceedings of the 3rd Conference on Designing Interactive Systems, pp. 424-433.",
        "Beckman, S.L. and Barry, M. (2007). Innovation as a Learning Process: Embedding Design Thinking. California Management Review, 50(1), pp. 25-56.",
        "Verganti, R. (2009). Design-Driven Innovation: Changing the Rules of Competition by Radically Innovating What Things Mean. Harvard Business Press, Boston.",
        "Martin, R. (2009). The Design of Business: Why Design Thinking is the Next Competitive Advantage. Harvard Business Press, Boston.",
        "Elsbach, K.D. and Stigliani, I. (2018). Design Thinking and Organizational Culture: A Review and Framework for Future Research. Journal of Management, 44(6), pp. 2274-2306.",
        "Micheli, P. et al. (2019). Doing Design Thinking: Conceptual Review, Synthesis, and Research Agenda. Journal of Product Innovation Management, 36(2), pp. 124-148.",
        "Kahneman, D. (2011). Thinking, Fast and Slow. Farrar, Straus and Giroux, New York.",
        "Hammond, J.S., Keeney, R.L. and Raiffa, H. (1999). Smart Choices: A Practical Guide to Making Better Decisions. Harvard Business School Press, Boston.",
        "Belton, V. and Stewart, T. (2002). Multiple Criteria Decision Analysis: An Integrated Approach. Springer, Boston.",
        "Saaty, T.L. (1980). The Analytic Hierarchy Process: Planning, Priority Setting, Resource Allocation. McGraw-Hill, New York.",
        "Boardman, A.E. et al. (2018). Cost-Benefit Analysis: Concepts and Practice. 5th ed., Cambridge University Press.",
        "Pfeffer, J. and Sutton, R.I. (2006). Hard Facts, Dangerous Half-Truths, and Total Nonsense: Profiting from Evidence-Based Management. Harvard Business School Press, Boston.",
        "Bazerman, M.H. and Moore, D.A. (2013). Judgment in Managerial Decision Making. 8th ed., John Wiley and Sons, New York.",
        "Gigerenzer, G. and Gaissmaier, W. (2011). Heuristic Decision Making. Annual Review of Psychology, 62, pp. 451-482.",
        "Meadows, D.H. (2008). Thinking in Systems: A Primer. Chelsea Green Publishing, White River Junction, VT.",
        "von Bertalanffy, L. (1968). General System Theory: Foundations, Development, Applications. George Braziller, New York.",
        "Senge, P.M. (1990). The Fifth Discipline: The Art and Practice of the Learning Organization. Doubleday/Currency, New York.",
        "Sterman, J.D. (2000). Business Dynamics: Systems Thinking and Modeling for a Complex World. McGraw-Hill, Boston.",
        "Snowden, D.J. and Boone, M.E. (2007). A Leader's Framework for Decision Making. Harvard Business Review, 85(11), pp. 68-76.",
        "Guilford, J.P. (1967). The Nature of Human Intelligence. McGraw-Hill, New York.",
        "de Bono, E. (1985). Six Thinking Hats. Little, Brown and Company, Boston.",
        "Amabile, T.M. (1996). Creativity in Context: Update to the Social Psychology of Creativity. Westview Press, Boulder, CO.",
        "Sawyer, R.K. (2012). Explaining Creativity: The Science of Human Innovation. 2nd ed., Oxford University Press.",
        "Dorst, K. (2015). Frame Innovation: Create New Thinking by Design. MIT Press, Cambridge, MA.",
        "Martin, R. (2007). The Opposable Mind: How Successful Leaders Win Through Integrative Thinking. Harvard Business School Press, Boston.",
        "Liedtka, J. and Ogilvie, T. (2011). Designing for Growth: A Design Thinking Tool Kit for Managers. Columbia University Press, New York.",
        "Carlgren, L., Rauth, I. and Elmquist, M. (2016). Framing Design Thinking: The Concept in Idea and Enactment. Creativity and Innovation Management, 25(1), pp. 38-57.",
        "Ackoff, R.L. (1999). Ackoff's Best: His Classic Writings on Management. John Wiley and Sons, New York.",
        "Kim, D.H. (1999). Introduction to Systems Thinking. Pegasus Communications, Waltham, MA.",
        "Gharajedaghi, J. (2011). Systems Thinking: Managing Chaos and Complexity. 3rd ed., Morgan Kaufmann, Burlington, MA.",
        "Checkland, P. (1981). Systems Thinking, Systems Practice. John Wiley and Sons, Chichester.",
        "Plattner, H., Meinel, C. and Leifer, L. (2011). Design Thinking: Understand, Improve, Apply. Springer, Berlin.",
        "Tschimmel, K. (2012). Design Thinking as an Effective Toolkit for Innovation. Proceedings of the XXIII ISPIM Conference, pp. 1-20.",
        "Kimbell, L. (2011). Rethinking Design Thinking: Part I. Design and Culture, 3(3), pp. 285-306.",
        "Snowden, D.J. (2002). Complex Acts of Knowing: Paradox and Descriptive Self-Awareness. Journal of Knowledge Management, 6(2), pp. 100-111.",
        "Teece, D.J. (2018). Dynamic Capabilities as (Workable) Management Systems Theory. Journal of Management and Organization, 24(3), pp. 359-368.",
        "Davenport, T.H. (2018). The AI Advantage: How to Put the Artificial Intelligence Revolution to Work. MIT Press, Cambridge, MA.",
    ]
    
    doc.add_references(references)
    
    return doc


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    output_dir = "/projects/sandbox/AMMAN"
    output_file = os.path.join(output_dir, "Chapter_Design_Thinking_Strategic_Decision_Making.docx")
    
    print("Generating figures...")
    # Also save figures as standalone PNGs
    fig_dir = os.path.join(output_dir, "dt_chapter_figures")
    os.makedirs(fig_dir, exist_ok=True)
    
    fig1 = generate_figure1()
    fig2 = generate_figure2()
    fig3 = generate_figure3()
    fig4 = generate_figure4()
    
    with open(os.path.join(fig_dir, "Figure_1_DT_Process_Framework.png"), "wb") as f:
        f.write(fig1)
    with open(os.path.join(fig_dir, "Figure_2_Comparative_Framework.png"), "wb") as f:
        f.write(fig2)
    with open(os.path.join(fig_dir, "Figure_3_Synthesized_Model.png"), "wb") as f:
        f.write(fig3)
    with open(os.path.join(fig_dir, "Figure_4_Future_Ecosystem.png"), "wb") as f:
        f.write(fig4)
    
    print("Figures saved to:", fig_dir)
    
    print("Building chapter document...")
    doc = build_chapter()
    
    print("Saving Word document...")
    doc.save(output_file)
    
    print(f"Document saved: {output_file}")
    print(f"File size: {os.path.getsize(output_file)} bytes")
