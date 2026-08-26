#!/usr/bin/env python3
"""
Generate the complete chapter:
"Quality Assurance in an Age of Complexity and Continuous Change"
Book: Higher Education Beyond Boundaries: Dynamics, Change, Challenges and Opportunities

Creates:
- 4 PNG figures
- 1 Word document (.docx) with ~8300 words, 47 references, 4 tables, 4 figures
"""

import zipfile
import xml.etree.ElementTree as ET
import struct
import zlib
import io
import os
import math
import base64
from copy import deepcopy

# ============================================================
# PART 1: PNG Figure Generation (pure Python, no dependencies)
# ============================================================

def create_png(width, height, pixels):
    """Create a PNG file from raw pixel data (list of rows, each row is list of (R,G,B) tuples)."""
    def make_chunk(chunk_type, data):
        chunk = chunk_type + data
        crc = zlib.crc32(chunk) & 0xffffffff
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', crc)
    
    # PNG signature
    signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = make_chunk(b'IHDR', ihdr_data)
    
    # IDAT chunk - pixel data
    raw_data = b''
    for row in pixels:
        raw_data += b'\x00'  # filter byte
        for r, g, b in row:
            raw_data += struct.pack('BBB', r, g, b)
    
    compressed = zlib.compress(raw_data, 9)
    idat = make_chunk(b'IDAT', compressed)
    
    # IEND chunk
    iend = make_chunk(b'IEND', b'')
    
    return signature + ihdr + idat + iend


def draw_filled_rect(pixels, x1, y1, x2, y2, color):
    """Draw a filled rectangle."""
    for y in range(max(0, y1), min(len(pixels), y2)):
        for x in range(max(0, x1), min(len(pixels[0]), x2)):
            pixels[y][x] = color


def draw_text_block(pixels, x, y, text, color, scale=1):
    """Draw simplified text representation as a colored block with label indicator."""
    # Simple block representation for text labels
    for dy in range(8 * scale):
        for dx in range(len(text) * 6 * scale):
            px, py = x + dx, y + dy
            if 0 <= px < len(pixels[0]) and 0 <= py < len(pixels):
                pixels[py][px] = color


def draw_line(pixels, x1, y1, x2, y2, color, thickness=1):
    """Draw a line using Bresenham-like approach."""
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    
    while True:
        for t in range(-thickness//2, thickness//2 + 1):
            px, py = x1 + t, y1
            if 0 <= px < len(pixels[0]) and 0 <= py < len(pixels):
                pixels[py][px] = color
            px, py = x1, y1 + t
            if 0 <= px < len(pixels[0]) and 0 <= py < len(pixels):
                pixels[py][px] = color
        
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def draw_circle(pixels, cx, cy, radius, color, filled=False):
    """Draw a circle."""
    for y in range(cy - radius, cy + radius + 1):
        for x in range(cx - radius, cx + radius + 1):
            dist = math.sqrt((x - cx)**2 + (y - cy)**2)
            if filled and dist <= radius:
                if 0 <= x < len(pixels[0]) and 0 <= y < len(pixels):
                    pixels[y][x] = color
            elif not filled and abs(dist - radius) < 1.5:
                if 0 <= x < len(pixels[0]) and 0 <= y < len(pixels):
                    pixels[y][x] = color


def create_figure1():
    """Figure 1: Evolution of Quality Assurance Frameworks - Timeline/progression diagram."""
    width, height = 400, 250
    pixels = [[(245, 248, 255) for _ in range(width)] for _ in range(height)]
    
    # Title area
    draw_filled_rect(pixels, 0, 0, width, 25, (44, 62, 80))
    
    # Timeline arrow
    draw_line(pixels, 25, 125, 375, 125, (44, 62, 80), 2)
    draw_line(pixels, 370, 120, 375, 125, (44, 62, 80), 2)
    draw_line(pixels, 370, 130, 375, 125, (44, 62, 80), 2)
    
    # Era boxes
    draw_filled_rect(pixels, 40, 50, 130, 110, (231, 76, 60))
    draw_filled_rect(pixels, 140, 50, 230, 110, (41, 128, 185))
    draw_filled_rect(pixels, 240, 50, 330, 110, (39, 174, 96))
    draw_filled_rect(pixels, 310, 50, 390, 110, (142, 68, 173))
    
    # Timeline markers
    draw_circle(pixels, 85, 125, 4, (231, 76, 60), True)
    draw_circle(pixels, 185, 125, 4, (41, 128, 185), True)
    draw_circle(pixels, 285, 125, 4, (39, 174, 96), True)
    draw_circle(pixels, 350, 125, 4, (142, 68, 173), True)
    
    # Labels below
    draw_filled_rect(pixels, 40, 155, 130, 170, (231, 76, 60))
    draw_filled_rect(pixels, 140, 155, 230, 170, (41, 128, 185))
    draw_filled_rect(pixels, 240, 155, 330, 170, (39, 174, 96))
    draw_filled_rect(pixels, 310, 155, 390, 170, (142, 68, 173))
    
    # Bottom description area
    draw_filled_rect(pixels, 30, 185, 190, 240, (245, 245, 245))
    draw_filled_rect(pixels, 200, 185, 380, 240, (245, 245, 245))
    draw_filled_rect(pixels, 30, 185, 190, 188, (231, 76, 60))
    draw_filled_rect(pixels, 200, 185, 380, 188, (41, 128, 185))
    
    return create_png(width, height, pixels)


def create_figure2():
    """Figure 2: Digital Quality Assurance Ecosystem - Hub and spoke diagram."""
    width, height = 400, 300
    pixels = [[(248, 249, 250) for _ in range(width)] for _ in range(height)]
    
    # Title bar
    draw_filled_rect(pixels, 0, 0, width, 25, (52, 73, 94))
    
    # Central hub
    cx, cy = 200, 160
    draw_circle(pixels, cx, cy, 35, (41, 128, 185), True)
    draw_circle(pixels, cx, cy, 25, (133, 193, 233), True)
    
    # Spoke nodes
    nodes = [
        (80, 80, (231, 76, 60)),
        (320, 80, (39, 174, 96)),
        (80, 240, (243, 156, 18)),
        (320, 240, (142, 68, 173)),
        (200, 45, (22, 160, 133)),
        (200, 275, (211, 84, 0)),
        (50, 160, (44, 62, 80)),
        (350, 160, (192, 57, 43)),
    ]
    
    for nx, ny, color in nodes:
        draw_line(pixels, cx, cy, nx, ny, (189, 195, 199), 1)
        draw_circle(pixels, nx, ny, 20, color, True)
    
    return create_png(width, height, pixels)


def create_figure3():
    """Figure 3: Stakeholder-Centered Quality Enhancement Model - Layered circle diagram."""
    width, height = 400, 300
    pixels = [[(255, 255, 255) for _ in range(width)] for _ in range(height)]
    
    # Title bar
    draw_filled_rect(pixels, 0, 0, width, 25, (39, 55, 70))
    
    cx, cy = 200, 165
    
    # Outer layer
    draw_circle(pixels, cx, cy, 115, (214, 234, 248), True)
    draw_circle(pixels, cx, cy, 115, (41, 128, 185), False)
    
    # Second layer
    draw_circle(pixels, cx, cy, 85, (213, 245, 227), True)
    draw_circle(pixels, cx, cy, 85, (39, 174, 96), False)
    
    # Third layer
    draw_circle(pixels, cx, cy, 55, (253, 235, 208), True)
    draw_circle(pixels, cx, cy, 55, (243, 156, 18), False)
    
    # Core
    draw_circle(pixels, cx, cy, 30, (245, 183, 177), True)
    draw_circle(pixels, cx, cy, 20, (231, 76, 60), True)
    
    # Labels
    draw_filled_rect(pixels, 150, 285, 250, 298, (41, 128, 185))
    
    return create_png(width, height, pixels)


def create_figure4():
    """Figure 4: Future-Ready Quality Assurance Framework - Matrix/roadmap style."""
    width, height = 400, 300
    pixels = [[(250, 250, 255) for _ in range(width)] for _ in range(height)]
    
    # Title bar
    draw_filled_rect(pixels, 0, 0, width, 25, (44, 62, 80))
    
    # Column headers
    draw_filled_rect(pixels, 30, 35, 155, 55, (41, 128, 185))
    draw_filled_rect(pixels, 160, 35, 275, 55, (39, 174, 96))
    draw_filled_rect(pixels, 280, 35, 390, 55, (142, 68, 173))
    
    # Grid cells
    row_colors = [(231, 76, 60), (243, 156, 18), (22, 160, 133)]
    for i, color in enumerate(row_colors):
        y_start = 60 + i * 80
        # Row header
        draw_filled_rect(pixels, 5, y_start, 25, y_start + 75, color)
        # Cells
        for j, x_start in enumerate([30, 160, 280]):
            w = 125 if j < 2 else 110
            draw_filled_rect(pixels, x_start, y_start, x_start + w, y_start + 75, (min(255, color[0]+100), min(255, color[1]+100), min(255, color[2]+100)))
            draw_filled_rect(pixels, x_start, y_start, x_start + w, y_start + 3, color)
            # Content bars
            for k in range(2):
                draw_filled_rect(pixels, x_start + 5, y_start + 15 + k * 28, x_start + 5 + (k+1)*30, y_start + 28 + k * 28, color)
    
    return create_png(width, height, pixels)


# ============================================================
# PART 2: DOCX Generation (pure Python using zipfile + XML)
# ============================================================

NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
}


def create_docx_with_content(output_path, figure_paths):
    """Create a complete .docx file with all chapter content."""
    
    # The complete chapter text with references
    chapter_content = get_chapter_content()
    
    # Read figure files
    figure_data = []
    for fp in figure_paths:
        with open(fp, 'rb') as f:
            figure_data.append(f.read())
    
    # Create the docx as a zip file
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # [Content_Types].xml
        zf.writestr('[Content_Types].xml', get_content_types_xml())
        
        # _rels/.rels
        zf.writestr('_rels/.rels', get_rels_xml())
        
        # word/_rels/document.xml.rels
        zf.writestr('word/_rels/document.xml.rels', get_document_rels_xml(len(figure_data)))
        
        # word/styles.xml
        zf.writestr('word/styles.xml', get_styles_xml())
        
        # word/numbering.xml
        zf.writestr('word/numbering.xml', get_numbering_xml())
        
        # word/document.xml (main content)
        zf.writestr('word/document.xml', build_document_xml(chapter_content, len(figure_data)))
        
        # Add images
        for i, img_data in enumerate(figure_data):
            zf.writestr(f'word/media/image{i+1}.png', img_data)


def get_content_types_xml():
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''


def get_rels_xml():
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''


def get_document_rels_xml(num_images):
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'''
    for i in range(num_images):
        rels += f'\n  <Relationship Id="rId{i+10}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image{i+1}.png"/>'
    rels += '\n</Relationships>'
    return rels


def get_styles_xml():
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:pPr><w:spacing w:after="200" w:line="276" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="360" w:after="200"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:i/><w:sz w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Caption">
    <w:name w:val="Caption"/>
    <w:pPr><w:spacing w:after="200"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:i/><w:sz w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr>
      <w:tblBorders>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      </w:tblBorders>
    </w:tblPr>
  </w:style>
</w:styles>'''


def get_numbering_xml():
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
</w:numbering>'''


def make_paragraph(text, style=None, bold=False, italic=False):
    """Generate XML for a paragraph."""
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    p = f'<w:p xmlns:w="{ns}">'
    if style:
        p += f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
    p += '<w:r>'
    if bold or italic:
        p += '<w:rPr>'
        if bold:
            p += '<w:b/>'
        if italic:
            p += '<w:i/>'
        p += '</w:rPr>'
    # Escape XML special characters
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    p += f'<w:t xml:space="preserve">{text}</w:t></w:r></w:p>'
    return p


def make_image_paragraph(rid, width_emu=5486400, height_emu=3657600):
    """Generate XML for an inline image."""
    ns_w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    ns_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    ns_wp = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
    ns_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    ns_pic = 'http://schemas.openxmlformats.org/drawingml/2006/picture'
    
    return f'''<w:p xmlns:w="{ns_w}">
  <w:pPr><w:jc w:val="center"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline xmlns:wp="{ns_wp}" distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{width_emu}" cy="{height_emu}"/>
        <wp:docPr id="1" name="Picture"/>
        <a:graphic xmlns:a="{ns_a}">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="{ns_pic}">
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="Picture"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{rid}" xmlns:r="{ns_r}"/>
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
</w:p>'''


def make_table(headers, rows):
    """Generate XML for a table."""
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    tbl = f'<w:tbl xmlns:w="{ns}">'
    tbl += '''<w:tblPr>
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
    </w:tblPr>'''
    
    # Header row
    tbl += '<w:tr>'
    for h in headers:
        h_escaped = h.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        tbl += f'''<w:tc>
          <w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="2C3E50"/></w:tcPr>
          <w:p><w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="20"/></w:rPr>
          <w:t xml:space="preserve">{h_escaped}</w:t></w:r></w:p></w:tc>'''
    tbl += '</w:tr>'
    
    # Data rows
    for row in rows:
        tbl += '<w:tr>'
        for cell in row:
            cell_escaped = cell.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            tbl += f'''<w:tc><w:p><w:r><w:rPr><w:sz w:val="20"/></w:rPr>
              <w:t xml:space="preserve">{cell_escaped}</w:t></w:r></w:p></w:tc>'''
        tbl += '</w:tr>'
    
    tbl += '</w:tbl>'
    return tbl


def build_document_xml(content_sections, num_images):
    """Build the complete document.xml from content sections."""
    ns_w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    
    doc = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{ns_w}" 
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<w:body>'''
    
    for section in content_sections:
        doc += section
    
    doc += '</w:body></w:document>'
    return doc


def get_chapter_content():
    """Return all document content as a list of XML paragraph strings."""
    sections = []
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    
    # Helper functions for cleaner code
    def p(text, style=None, bold=False, italic=False):
        sections.append(make_paragraph(text, style, bold, italic))
    
    def h1(text):
        p(text, 'Heading1', bold=True)
    
    def h2(text):
        p(text, 'Heading2', bold=True)
    
    def h3(text):
        p(text, 'Heading3', bold=True, italic=True)
    
    def img(num):
        rid = f'rId{num + 9}'
        sections.append(make_image_paragraph(rid))
    
    def caption(text):
        p(text, 'Caption', italic=True)
    
    def table(headers, rows, caption_text):
        p(caption_text, 'Caption', bold=True)
        sections.append(make_table(headers, rows))
        p('')  # spacing
    
    # ============================================================
    # CHAPTER TITLE
    # ============================================================
    h1('Quality Assurance in an Age of Complexity and Continuous Change')
    p('Book: Higher Education Beyond Boundaries: Dynamics, Change, Challenges and Opportunities', italic=True)
    p('')
    
    # ABSTRACT
    h2('Abstract')
    p('Quality assurance in higher education has undergone a fundamental transformation in response to globalization, digital disruption, and evolving stakeholder expectations. This chapter examines how quality assurance frameworks have adapted to an increasingly complex and rapidly changing higher education landscape. Drawing on contemporary scholarship and institutional practice, the analysis explores the shift from compliance-oriented to enhancement-led approaches, the challenges posed by digital and transnational education, and the emergence of adaptive, technology-enabled quality systems. The chapter presents a stakeholder-centered model for quality enhancement, emphasizing student experience, evidence-based decision-making, and continuous improvement cultures. Future directions are considered, including agile and AI-supported quality assurance, global harmonization of standards, and a proposed framework for sustainable, future-ready quality management. Through critical synthesis of current research and international best practice, this chapter offers both conceptual and practical guidance for institutions navigating quality assurance beyond traditional boundaries.')
    p('')
    p('Keywords: quality assurance, higher education, continuous improvement, digital transformation, transnational education, stakeholder engagement, accreditation, adaptive quality systems, learning analytics, future-ready frameworks')
    p('')
    p('Abbreviations: QA - Quality Assurance; IQA - Internal Quality Assurance; EQA - External Quality Assurance; ESG - European Standards and Guidelines; TNE - Transnational Education; AI - Artificial Intelligence; INQAAHE - International Network for Quality Assurance Agencies in Higher Education; KPIs - Key Performance Indicators')
    p('')
    
    # ============================================================
    # 1. FOUNDATIONS OF QUALITY ASSURANCE
    # ============================================================
    h1('1. Foundations of Quality Assurance in a Changing Higher Education Landscape')
    
    p('The foundations of quality assurance in higher education rest upon a rich intellectual and institutional history that has shaped current practices and continues to inform emerging approaches. Understanding these foundations is essential for appreciating both the achievements and limitations of existing quality frameworks, and for charting productive directions for future development. This section examines the evolution of quality concepts, the complexity and disruption characterizing the contemporary landscape, and the principles and mechanisms of current quality assurance frameworks.')
    
    h2('1.1 Evolution and Changing Meaning of Quality in Higher Education')
    
    p('The concept of quality in higher education has evolved significantly over the past half-century, reflecting shifts in institutional missions, societal expectations, and the broader political economy of knowledge production [1]. Historically, quality was defined primarily in terms of academic reputation, faculty credentials, and resource inputs. Universities operated as autonomous institutions, largely self-regulating and accountable mainly to their scholarly communities [2]. Quality assurance, to the extent it existed, was embedded in collegial governance structures, peer review, and the maintenance of academic standards through disciplinary traditions.')
    
    p('The expansion of higher education systems from the 1960s onward brought new demands for accountability and public assurance of educational standards [3]. Massification meant that higher education was no longer the preserve of a small elite; governments, employers, and the wider public increasingly expected evidence that institutions were delivering value for the substantial public and private investment in education [4]. This shift gave rise to formal quality assurance mechanisms, including accreditation bodies, national quality agencies, and standardized frameworks for institutional and program review [5].')
    
    p('Traditional approaches to academic quality assurance were predominantly compliance-oriented, focused on ensuring institutions met minimum standards for facilities, staffing, curricula, and governance [6]. These approaches reflected a regulatory mindset: quality was assessed against predetermined criteria, and the primary purpose of quality assurance was to certify that institutions were fit for purpose. While effective in establishing baseline standards, compliance-based models were often criticized for being bureaucratic, backward-looking, and insufficiently attentive to the dynamic and complex nature of educational quality [7].')
    
    p('From the late 1990s, a discernible shift occurred from compliance-oriented to enhancement-oriented quality assurance. Enhancement-led approaches foreground continuous improvement, innovation, and the active engagement of institutions in reflecting on and improving their educational provision [8]. Rather than merely checking conformity with standards, enhancement-oriented quality assurance encourages institutions to identify strengths and areas for development, to experiment with new pedagogies and curricula, and to cultivate a culture of quality that permeates all levels of the institution [9]. This shift is reflected in the evolution of quality assurance frameworks globally, from the European Standards and Guidelines (ESG) to the approaches adopted by agencies in Australasia, North America, and beyond [10].')
    
    p('Emerging expectations from students, employers, governments, and society at large have further reshaped the meaning of quality [11]. Students increasingly act as informed consumers, seeking programs that offer employability, flexibility, and personalized learning experiences. Employers demand graduates with transversal competencies, digital literacy, and the capacity for lifelong learning. Governments and funding bodies require evidence of impact, efficiency, and equity. Society more broadly expects higher education to address grand challenges, promote social mobility, and contribute to sustainable development [12]. These diverse and sometimes competing expectations render quality a multidimensional, contested, and evolving concept, requiring quality assurance systems that are themselves adaptive and responsive to change.')
    
    p('The tension between these different conceptions of quality presents a fundamental challenge for quality assurance practitioners and policymakers. A view of quality as excellence implies selective admission and high academic standards, while quality as fitness for purpose emphasizes alignment between institutional provision and stakeholder needs [1]. Quality as transformation foregrounds the developmental impact of education on students, while quality as value for money introduces economic efficiency considerations [2]. Contemporary quality assurance must navigate these competing conceptions, developing frameworks that are sufficiently multidimensional to address the full range of stakeholder expectations while remaining coherent and practicable in implementation [6].')
    
    p('Furthermore, the increasing marketization of higher education has introduced competitive dynamics that both support and complicate quality assurance [4]. Competition among institutions for students, research funding, and international rankings has incentivized quality improvement in some areas while potentially distorting institutional priorities in others. The proliferation of university rankings and league tables, while providing useful comparative information, has been criticized for promoting a narrow, metrics-driven conception of quality that may not adequately capture the breadth and depth of educational value [23]. Quality assurance systems must therefore resist the temptation to reduce quality to easily quantifiable indicators, while still providing meaningful and comparable information to diverse stakeholders [27].')
    
    # Table 1
    table(
        ['Era', 'Dominant Paradigm', 'Focus', 'Key Mechanisms', 'Limitations'],
        [
            ['1960s-1980s', 'Collegial/Self-Regulation', 'Academic reputation, inputs', 'Peer review, institutional autonomy', 'Limited external accountability'],
            ['1980s-2000s', 'Compliance/Accountability', 'Minimum standards, fitness for purpose', 'Accreditation, external review, audit', 'Bureaucratic, backward-looking'],
            ['2000s-2010s', 'Standards-Based', 'Benchmarking, outcomes', 'National frameworks, ESG, KPIs', 'Prescriptive, limited flexibility'],
            ['2010s-2020s', 'Enhancement-Led', 'Continuous improvement, innovation', 'Self-evaluation, peer learning, engagement', 'Resource-intensive, uneven uptake'],
            ['2020s-Present', 'Adaptive/Technology-Enabled', 'Agility, resilience, inclusivity', 'AI, analytics, risk-based QA', 'Emerging, not yet fully validated'],
        ],
        'Table 1. Evolution of Quality Assurance Paradigms in Higher Education [1][5][8][10]'
    )
    
    h2('1.2 Complexity and Disruption in Higher Education')
    
    p('The contemporary higher education landscape is characterized by unprecedented complexity and disruption. Globalization has expanded the reach of higher education beyond national borders, creating new opportunities and challenges for quality assurance [13]. International student mobility, transnational education partnerships, branch campuses, and cross-border online provision all pose questions about how quality can be assured when education transcends geographic, regulatory, and cultural boundaries [14]. The proliferation of providers, including private universities, online platforms, and corporate training organizations, has further complicated the quality landscape, blurring the lines between formal and informal learning and raising questions about credential recognition and equivalence [15].')
    
    p('Digital transformation represents a further source of disruption. The rapid expansion of online, blended, and hybrid learning, accelerated by the COVID-19 pandemic, has challenged established assumptions about how quality is defined, assured, and improved [16]. Emerging educational technologies, including artificial intelligence (AI), learning analytics, adaptive learning systems, and virtual reality, promise to transform teaching, learning, and assessment but also raise new questions about data quality, algorithmic transparency, privacy, and equity [17]. Quality assurance frameworks designed for campus-based, face-to-face provision may be inadequate for the complexities of technology-enabled education, necessitating new models and approaches [18].')
    
    p('Changing institutional structures and stakeholder relationships add further layers of complexity. The rise of multi-campus universities, university networks, public-private partnerships, and collaborative degree programs means that quality assurance must navigate diverse governance structures, regulatory environments, and quality cultures [19]. The growing importance of lifelong learning, micro-credentials, and flexible learning pathways challenges traditional program-level quality assurance, requiring frameworks that can accommodate diverse modes, durations, and purposes of learning [20].')
    
    p('The pace of change itself constitutes a challenge for quality assurance. Traditional quality assurance cycles, typically operating on five-to-seven-year review periods, may be too slow to keep pace with rapidly evolving educational technologies, labor market demands, and student expectations [18]. The emergence of agile and responsive quality management approaches reflects a recognition that quality assurance must be capable of operating at multiple temporal scales, combining periodic comprehensive reviews with ongoing real-time monitoring and rapid-cycle improvement [42]. This temporal dimension of quality assurance has become particularly salient in the context of the COVID-19 pandemic, which demonstrated that educational institutions must be capable of adapting their provision, and their quality systems, with unprecedented speed [43].')
    
    p('The interconnection between these various sources of complexity and disruption creates what may be termed a complex adaptive system, in which changes in one dimension ripple through and affect others [45]. Globalization interacts with digitalization to enable new forms of transnational online provision. Changing student demographics interact with technological innovation to create demand for personalized, flexible, and technology-enhanced learning. Evolving labor market needs interact with government policy to reshape expectations of graduate outcomes and institutional accountability. Quality assurance systems must be capable of operating effectively within this complex, dynamic, and interconnected environment, requiring approaches that are systemic, adaptive, and responsive to emergent properties and feedback effects [19].')
    
    # Figure 1
    img(1)
    caption('Figure 1. Evolution of Quality Assurance Frameworks in Higher Education: From Compliance to Adaptive Models [5][10][18]')
    p('')
    
    h2('1.3 Contemporary Quality Assurance Frameworks and Principles')
    
    p('Modern quality assurance in higher education is structured around a set of widely recognized principles and mechanisms. Internal quality assurance (IQA) refers to the processes and systems institutions use to monitor, evaluate, and improve their educational provision. These include curriculum design and review, student feedback mechanisms, teaching evaluation, learning outcomes assessment, and strategic planning for quality enhancement [21]. External quality assurance (EQA) encompasses the activities of national and international agencies that evaluate institutions or programs against established standards, typically through accreditation, audit, or assessment [22].')
    
    p('Accreditation remains the most visible form of external quality assurance in many jurisdictions. It serves both a gatekeeping function, certifying that institutions meet threshold standards, and a developmental function, encouraging continuous improvement [23]. Benchmarking, both domestic and international, enables institutions to compare their performance against peers and identify areas for development [24]. Assessment of learning outcomes has become a central focus of quality assurance, reflecting the shift from input-based to outcome-based models of quality [25].')
    
    p('Transparency, accountability, and evidence-based quality management are core principles of contemporary frameworks. The European Standards and Guidelines (ESG), for example, emphasize the importance of clear and publicly available information about institutions and programs, robust evidence bases for quality judgments, and mechanisms for stakeholder engagement [10]. Similarly, frameworks in Australasia, North America, and Asia-Pacific stress the importance of data-driven decision-making, stakeholder participation, and a commitment to continuous improvement [26].')
    
    p('A critical challenge for contemporary quality assurance is balancing standardization with flexibility. While common standards and frameworks provide a basis for comparability and trust, excessive standardization can stifle innovation and fail to account for the diversity of institutional missions, student populations, and educational contexts [27]. The most effective quality assurance systems are those that combine clear principles and standards with sufficient flexibility to accommodate diversity, encourage innovation, and respond to emerging challenges [28].')
    
    p('The relationship between internal and external quality assurance is a further dimension of contemporary frameworks. Effective quality assurance systems achieve a productive alignment between institutions own quality processes and the requirements of external agencies, avoiding duplication while ensuring that external evaluation adds value to institutional efforts [22]. This alignment is supported by meta-evaluation, in which external agencies assess the effectiveness of institutions internal quality systems rather than duplicating detailed program-level review. Such approaches can reduce the administrative burden of quality assurance while maintaining public confidence in educational standards [26]. The principle of subsidiarity, allocating quality responsibilities to the most appropriate level, is increasingly recognized as fundamental to efficient and effective quality governance [5].')
    
    p('The evolution of quality assurance frameworks also reflects broader shifts in governance philosophy, from command-and-control regulation to more collaborative and trust-based approaches [8]. Contemporary frameworks increasingly emphasize institutional responsibility for quality, with external agencies playing a facilitative and assurance role rather than a directive one. This shift requires high levels of institutional maturity, capacity, and commitment to quality, as well as robust mechanisms for public accountability and stakeholder protection [21]. The challenge for quality assurance systems is to foster institutional ownership and innovation while maintaining sufficient external oversight to protect students and the public interest [9].')
    
    # ============================================================
    # 2. QUALITY ASSURANCE UNDER CONDITIONS OF CONTINUOUS CHANGE
    # ============================================================
    h1('2. Quality Assurance Under Conditions of Continuous Change')
    
    p('Continuous change has become the defining condition of contemporary higher education, requiring quality assurance systems that are capable of maintaining standards and supporting improvement in the face of persistent uncertainty and disruption. This section examines how quality assurance operates in the context of digital transformation, flexible and transnational education, and the broader challenges of risk, resilience, and adaptive management.')
    
    h2('2.1 Managing Quality in Digital and Technology-Enabled Education')
    
    p('The digital revolution has fundamentally altered the delivery, assessment, and quality assurance of higher education. Online, blended, and hybrid learning modalities now constitute a significant proportion of educational provision globally, requiring quality assurance frameworks that address the unique challenges of technology-mediated education [16]. Quality assurance of online learning encompasses multiple dimensions: course design and instructional quality, learner engagement and interaction, assessment integrity, technological infrastructure and reliability, and the adequacy of student support services [29].')
    
    p('Artificial intelligence is emerging as both a tool and a subject of quality assurance. AI-powered learning analytics enable institutions to monitor student engagement, predict at-risk learners, and personalize learning pathways in real time [30]. These capabilities offer significant potential for quality enhancement, enabling earlier intervention, more responsive curricula, and richer evidence bases for quality judgments. However, the deployment of AI in education also raises important quality concerns, including algorithmic bias, the transparency of decision-making processes, and the potential for surveillance and loss of learner autonomy [17].')
    
    p('Digital assessment presents particular challenges for quality assurance. The shift to online and remote assessment during the COVID-19 pandemic exposed vulnerabilities in assessment integrity and raised questions about the equivalence of online and in-person assessment [31]. Proctoring technologies, e-portfolios, and competency-based assessments offer potential solutions but require careful quality assurance to ensure fairness, accessibility, and validity [32]. Data quality is a further concern: the proliferation of educational data demands robust frameworks for data governance, quality, and ethical use [33].')
    
    p('Cybersecurity, privacy, and technological reliability are increasingly recognized as dimensions of educational quality. Institutions must ensure that digital learning environments are secure, that student data is protected, and that technology failures do not disproportionately affect vulnerable learners [34]. Quality assurance frameworks must therefore extend beyond traditional academic concerns to encompass the technological and ethical dimensions of digital education, as illustrated in Figure 2.')
    
    p('The quality assurance of technology-enabled education also requires attention to the digital divide and questions of equitable access. Not all students have equal access to reliable internet connectivity, appropriate devices, or suitable study environments for online learning [16]. Quality assurance frameworks must therefore consider the accessibility and inclusivity of digital provision, ensuring that technology-enabled education does not inadvertently exacerbate existing inequalities. This includes attention to universal design principles, the availability of alternative formats and modes of engagement, and the provision of technical and pedagogical support for students and staff [29]. The comprehensive nature of the digital quality assurance ecosystem is depicted in Figure 2, showing how these components interconnect and depend upon one another.')
    
    p('Moreover, the rapid evolution of generative artificial intelligence tools presents novel challenges for academic integrity and assessment design. The emergence of large language models capable of producing sophisticated written content has forced institutions to reconsider traditional assessment methods and develop new approaches to evaluating authentic student learning [31]. Quality assurance frameworks must evolve to address these challenges, incorporating guidelines for the ethical use of AI tools in teaching and assessment, developing new forms of authentic assessment that demonstrate genuine competence, and ensuring that assessment practices remain valid and fair in an AI-augmented educational environment [32].')
    
    # Figure 2
    img(2)
    caption('Figure 2. Digital Quality Assurance Ecosystem: Interconnected Components for Technology-Enabled Higher Education [17][30][34]')
    p('')
    
    # Table 2
    table(
        ['Component', 'Quality Dimension', 'Key Indicators', 'Challenges'],
        [
            ['Online Course Design', 'Instructional quality, accessibility', 'Student satisfaction, completion rates', 'Diverse learner needs, rapid tech change'],
            ['AI and Learning Analytics', 'Predictive accuracy, ethical use', 'Early alert effectiveness, bias audits', 'Algorithmic transparency, data privacy'],
            ['Digital Assessment', 'Integrity, validity, fairness', 'Authentication rates, grade distributions', 'Remote proctoring concerns, accessibility'],
            ['Cybersecurity', 'Data protection, reliability', 'Incident rates, recovery times', 'Evolving threats, resource constraints'],
            ['Student Support Systems', 'Responsiveness, inclusivity', 'Response times, satisfaction scores', 'Scalability, digital divide'],
        ],
        'Table 2. Key Components of Quality Assurance in Digital and Technology-Enabled Education [16][29][33]'
    )
    
    h2('2.2 Quality Assurance for Flexible and Transnational Education')
    
    p('The proliferation of flexible learning pathways, including micro-credentials, stackable qualifications, and lifelong learning programs, presents both opportunities and challenges for quality assurance [35]. Micro-credentials, in particular, have grown rapidly as a response to employer demand for targeted, verifiable competencies and learner demand for flexible, accessible upskilling opportunities. However, the diversity of micro-credential providers, formats, and recognition frameworks creates significant challenges for quality assurance, including questions of comparability, portability, and consumer protection [36].')
    
    p('Cross-border and transnational higher education (TNE) has expanded significantly in recent decades, driven by institutional internationalization strategies, government policies, and learner demand [14]. TNE takes many forms, including branch campuses, franchise arrangements, joint programs, and online cross-border provision. Ensuring consistent quality across different regulatory, cultural, and operational contexts is a central challenge, requiring robust partnership agreements, shared quality standards, and effective mechanisms for monitoring and review [37].')
    
    p('Maintaining consistent quality across campuses, platforms, and partner institutions demands a systematic approach to quality assurance that is both flexible and rigorous [38]. This includes clear articulation of expected learning outcomes, alignment of curricula and assessment across delivery modes, coordinated quality monitoring, and shared professional development for teaching staff. International frameworks, such as the UNESCO/OECD Guidelines for Quality Provision in Cross-Border Higher Education and the INQAAHE Guidelines of Good Practice, provide a basis for harmonizing quality standards across borders [39].')
    
    p('The recognition of prior learning and the integration of non-formal and informal learning into formal qualifications further complicate the quality landscape. Quality assurance systems must accommodate learners who bring diverse experiences and credentials, ensuring that recognition processes are fair, transparent, and robust [40]. This requires quality frameworks that are capable of evaluating competence regardless of how or where it was acquired, a significant departure from traditional input- and process-based quality assurance models.')
    
    p('The quality assurance of collaborative and joint programs between institutions in different countries presents particular governance challenges. When multiple institutions share responsibility for a program, questions arise about which quality standards apply, which agency has jurisdiction, and how quality responsibilities are distributed among partners [37]. Effective quality assurance of collaborative provision requires clear agreements about roles and responsibilities, shared quality criteria, coordinated monitoring mechanisms, and transparent communication with students about the nature and governance of their program [38]. The development of joint program accreditation, in which a single quality evaluation covers provision delivered across multiple national systems, represents an innovative response to these challenges, though significant practical and regulatory barriers remain [39].')
    
    p('The growth of education technology companies and platform providers as significant actors in higher education raises additional quality considerations. When institutions rely on third-party platforms for learning management, assessment, credentialing, or student support, the quality of educational provision becomes dependent on commercial actors whose priorities may not fully align with educational values [35]. Quality assurance frameworks must address the governance of these relationships, ensuring that technology partnerships support rather than compromise educational quality, and that institutions retain meaningful oversight of the learning experience regardless of the technological infrastructure through which it is delivered [36].')
    
    h2('2.3 Risk, Resilience, and Adaptive Quality Management')
    
    p('The increasing pace and unpredictability of change in higher education demand quality assurance systems that are not merely reactive but actively anticipate and manage risk [41]. Risk-based approaches to quality assurance identify and prioritize areas of greatest vulnerability, enabling institutions and agencies to focus resources where they are most needed and to intervene proactively rather than retrospectively [42]. This shift from periodic, comprehensive review to risk-informed, targeted quality management reflects broader trends in organizational governance and risk management.')
    
    p('The COVID-19 pandemic starkly illustrated the importance of institutional resilience and adaptive quality management. Institutions that had invested in flexible delivery, robust digital infrastructure, and agile quality systems were better able to maintain educational quality during the disruption [43]. Crisis preparedness, including scenario planning, business continuity frameworks, and rapid quality feedback mechanisms, is now recognized as an essential dimension of quality assurance, not merely a response to exceptional circumstances [44].')
    
    p('Adaptive quality systems are those capable of responding to new challenges and opportunities without sacrificing rigor or coherence. Key features of adaptive quality systems include real-time data feedback, devolved decision-making, rapid iteration of processes, and a tolerance for experimentation and innovation [45]. Such systems require a cultural shift within institutions, moving from a compliance mindset to one that embraces learning, agility, and resilience as core values. The development of adaptive quality cultures is both a leadership challenge and an organizational learning imperative, requiring sustained investment in capacity-building, professional development, and shared governance.')
    
    p('The concept of organizational resilience, drawn from ecological and systems thinking, provides a valuable framework for understanding adaptive quality management [45]. Resilient organizations are not simply those that can withstand shocks, but those that can adapt, transform, and emerge stronger from disruption. Applied to quality assurance, this implies systems that are designed for learning and adaptation rather than mere compliance, that incorporate redundancy and diversity as sources of strength, and that maintain core quality commitments while flexibly adapting processes and mechanisms to changing circumstances [44]. The development of institutional resilience as a quality attribute requires attention to governance structures, communication systems, resource flexibility, and the cultivation of adaptive capacity at all organizational levels [43].')
    
    p('Risk registers, scenario planning exercises, and continuity protocols have become standard components of institutional quality infrastructure in the post-pandemic era. These tools enable institutions to identify potential threats to educational quality, assess their likelihood and impact, and develop contingency responses that can be activated rapidly when needed [41]. The integration of risk management with quality assurance represents a significant evolution in quality thinking, recognizing that quality is not merely a matter of achieving standards under normal conditions but of maintaining standards and supporting improvement under conditions of uncertainty and change [42]. This integration is essential for institutions operating in an environment characterized by geopolitical instability, technological disruption, demographic shifts, and evolving regulatory landscapes.')
    
    # ============================================================
    # 3. STAKEHOLDER-CENTERED AND EVIDENCE-BASED QUALITY ENHANCEMENT
    # ============================================================
    h1('3. Stakeholder-Centered and Evidence-Based Quality Enhancement')
    
    p('The shift toward stakeholder-centered and evidence-based quality enhancement represents one of the most significant developments in quality assurance philosophy and practice. This section examines how student-centered approaches, data-driven monitoring, and continuous improvement cultures are reshaping quality assurance from a periodic evaluation exercise into an ongoing, embedded, and participatory process of educational improvement.')
    
    h2('3.1 Student-Centered Approaches to Quality')
    
    p('The student is increasingly recognized as the central stakeholder in quality assurance, reflecting the broader shift toward learner-centered education [11]. Student-centered quality assurance places the student experience, engagement, and learning outcomes at the heart of quality processes. This entails not only measuring student satisfaction and academic achievement but also actively involving students in the design, implementation, and evaluation of quality assurance mechanisms [46].')
    
    p('Student engagement in quality assurance takes multiple forms, including participation in governance structures, membership of review panels, co-design of curricula and assessment, and contribution to quality enhancement initiatives. Research consistently demonstrates that meaningful student engagement leads to more relevant, responsive, and effective quality processes [12]. However, ensuring inclusive and representative student participation remains a challenge, particularly for diverse and dispersed student populations in online and transnational contexts.')
    
    p('Equity, inclusion, and accessibility are fundamental dimensions of quality in contemporary higher education. Quality assurance frameworks must address the needs of all learners, including those from underrepresented and marginalized groups, students with disabilities, mature learners, and those studying in non-traditional modes [46]. This requires quality indicators and processes that are sensitive to diversity, that promote equitable outcomes, and that actively identify and address barriers to participation and achievement. As shown in Figure 3, the stakeholder-centered model positions student experience at the core, surrounded by layers of institutional process, governance, and external environment.')
    
    p('The concept of students as partners in quality assurance represents a more advanced form of engagement than traditional student feedback mechanisms [46]. Partnership approaches involve students as active collaborators in curriculum design, pedagogical innovation, quality review, and institutional governance, recognizing that students bring unique perspectives, expertise, and creativity to quality processes. Research on students-as-partners initiatives demonstrates positive outcomes for both students and institutions, including enhanced learning experiences, more innovative curricula, and stronger quality cultures [12]. However, implementing genuine partnership requires attention to power dynamics, adequate resourcing, inclusive representation, and institutional commitment to shared governance.')
    
    p('The measurement of student learning outcomes has become a central concern of quality assurance, driven by stakeholder demands for evidence of educational effectiveness and graduate competence [25]. However, the assessment of complex learning outcomes, including critical thinking, creativity, ethical reasoning, and intercultural competence, presents significant methodological challenges. Quality assurance frameworks must support institutions in developing valid and reliable approaches to outcomes assessment while avoiding reductive approaches that measure only easily quantifiable outcomes at the expense of more nuanced and transformative dimensions of learning [11]. The integration of direct and indirect evidence of learning, including portfolio-based assessment, capstone projects, employer feedback, and longitudinal graduate studies, offers a more comprehensive approach to outcomes-based quality assurance [21].')
    
    # Figure 3
    img(3)
    caption('Figure 3. Stakeholder-Centered Quality Enhancement Model: Concentric Layers of Quality Influence and Feedback [11][12][46]')
    p('')
    
    h2('3.2 Data-Driven Quality Monitoring and Decision-Making')
    
    p('Evidence-based quality assurance depends on robust institutional data systems and the capacity to translate data into actionable insights [30]. Institutional data encompasses a wide range of information, including student enrollment and progression data, learning analytics, graduate outcomes, teaching evaluations, research metrics, and resource utilization. The integration and analysis of these data sources enables institutions to monitor quality in real time, identify emerging issues, and make informed decisions about resource allocation and strategic priorities [33].')
    
    p('Learning analytics, the measurement, collection, analysis, and reporting of data about learners and their contexts, has emerged as a powerful tool for quality monitoring and enhancement [30]. Analytics platforms can identify patterns of engagement, predict student success or risk of withdrawal, and evaluate the effectiveness of pedagogical interventions. When used ethically and transparently, learning analytics can support personalized learning, early intervention, and evidence-based curriculum development [47].')
    
    p('Dashboards, predictive analytics, and early-warning mechanisms represent the practical application of data-driven quality monitoring. Institutional dashboards aggregate and visualize key quality indicators, enabling leaders and quality professionals to track performance trends and identify anomalies [33]. Predictive analytics use historical and real-time data to forecast future outcomes, such as student retention or program viability. Early-warning systems alert staff to students at risk of disengagement or failure, enabling timely support interventions. Together, these tools form an integrated quality intelligence infrastructure that supports both operational management and strategic planning.')
    
    p('The ethical dimensions of data-driven quality assurance require careful attention. The collection and analysis of student data raises important questions about consent, privacy, transparency, and the potential for surveillance [34]. Students must be informed about what data is collected, how it is used, and what safeguards are in place to protect their privacy and autonomy. Algorithmic decision-making in quality processes must be subject to scrutiny for bias, fairness, and accuracy, with mechanisms for human oversight and appeal [17]. The development of ethical frameworks for learning analytics in quality assurance is an active area of research and policy development, with several international bodies publishing guidelines and principles for responsible data use in educational contexts [47].')
    
    p('The challenge of data integration across institutional systems remains significant. Many institutions operate multiple data systems that are not fully interoperable, creating silos of information that limit the potential for comprehensive quality analysis [33]. Investment in data infrastructure, including common data standards, integrated platforms, and analytical capabilities, is essential for realizing the full potential of evidence-based quality assurance. Furthermore, the capacity of staff to interpret and act on data-driven insights requires ongoing professional development in data literacy, analytical thinking, and evidence-informed decision-making [30]. Without this human capacity, even the most sophisticated data systems will fail to deliver meaningful quality improvement.')
    
    # Table 3
    table(
        ['Data Source', 'Application in QA', 'Tools/Technologies', 'Ethical Considerations'],
        [
            ['Student enrollment/progression', 'Retention monitoring, cohort analysis', 'Student information systems, BI tools', 'Data accuracy, consent'],
            ['Learning analytics', 'Engagement tracking, at-risk identification', 'LMS analytics, predictive models', 'Algorithmic fairness, transparency'],
            ['Graduate outcomes', 'Employability, satisfaction', 'Surveys, labor market data', 'Response bias, longitudinal tracking'],
            ['Teaching evaluations', 'Pedagogical quality, faculty development', 'Survey platforms, sentiment analysis', 'Anonymity, representativeness'],
            ['Resource utilization', 'Efficiency, value-for-money', 'Financial systems, space analytics', 'Contextual interpretation'],
        ],
        'Table 3. Data Sources and Their Application in Quality Assurance [30][33][47]'
    )
    
    h2('3.3 Building a Culture of Continuous Quality Improvement')
    
    p('Sustainable quality enhancement requires more than effective processes and systems; it demands a pervasive institutional culture of continuous improvement [9]. A culture of quality is one in which all members of the institution, from senior leaders to front-line staff and students, are engaged in reflecting on and improving educational provision. Such cultures are characterized by shared values of excellence, openness to feedback, willingness to learn from mistakes, and a commitment to evidence-based practice [8].')
    
    p('Leadership and governance are critical enablers of quality cultures. Effective quality leadership involves not only setting expectations and allocating resources but also modeling reflective practice, promoting dialogue, and empowering staff and students to contribute to quality processes [21]. Distributed leadership, in which quality responsibilities are shared across all levels of the institution, is associated with more resilient and responsive quality cultures [28].')
    
    p('Faculty and staff engagement is essential for the success of quality enhancement initiatives. Quality processes that are perceived as externally imposed or bureaucratic are unlikely to gain genuine buy-in from academic and professional staff [7]. Effective engagement strategies include involving staff in the design and implementation of quality processes, providing professional development opportunities, recognizing and rewarding contributions to quality, and creating spaces for collegial reflection and peer learning [9].')
    
    p('Feedback loops and reflective practice are the mechanisms through which quality cultures sustain themselves. Effective feedback loops connect data collection and analysis to action and review, ensuring that evidence informs improvement and that the impact of changes is monitored [26]. Reflective practice, at both individual and organizational levels, enables institutions to learn from experience, adapt to changing circumstances, and build institutional memory. Organizational learning theory provides a valuable framework for understanding how institutions develop and sustain quality cultures, emphasizing the importance of shared mental models, systems thinking, and a commitment to dialogue and inquiry [45].')
    
    p('The relationship between quality assurance and academic freedom represents a persistent tension in quality cultures. Academic staff may perceive quality processes as intrusive, bureaucratic, or threatening to their professional autonomy [7]. Effective quality cultures resolve this tension by framing quality enhancement as a professional responsibility rather than an external imposition, by ensuring that quality processes respect disciplinary expertise and academic judgment, and by demonstrating that quality assurance supports rather than constrains pedagogical innovation and intellectual freedom [28]. This requires leadership that is sensitive to academic values, processes that are designed with academic input, and a discourse of quality that emphasizes professional learning and development rather than surveillance and control [9].')
    
    p('The sustainability of quality cultures depends on the institutional capacity to maintain momentum and commitment over time. Quality improvement fatigue, in which staff become disengaged from quality processes due to their frequency, complexity, or perceived lack of impact, is a recognized challenge [7]. Sustainable quality cultures address this through meaningful engagement, visible impact, recognition and reward, and the integration of quality processes into routine professional practice rather than treating them as separate, additional activities. The most effective institutions are those in which quality thinking becomes embedded in everyday academic and administrative work, rather than being confined to periodic review cycles or specialist quality units [8][26].')
    
    # ============================================================
    # 4. FUTURE DIRECTIONS
    # ============================================================
    h1('4. Future Directions for Quality Assurance Beyond Boundaries')
    
    p('The future of quality assurance in higher education lies beyond the traditional boundaries that have defined the field: boundaries of geography, technology, institutional form, and regulatory jurisdiction. This section explores innovative models for future quality assurance, the imperative of global collaboration and harmonization, and a proposed framework for sustainable quality that integrates adaptability, innovation, inclusivity, and resilience as core organizing principles for quality assurance in an era of unprecedented change and opportunity.')
    
    h2('4.1 Innovative Models for Future Quality Assurance')
    
    p('The future of quality assurance in higher education will be shaped by the convergence of technological innovation, changing educational models, and evolving societal expectations [18]. Agile quality assurance, drawing on principles from software development and organizational management, emphasizes iterative cycles of planning, action, and review, enabling institutions to respond rapidly to feedback and changing circumstances [42]. Risk-based approaches, already adopted by several national quality agencies, direct quality assurance attention to areas of greatest risk and potential impact, reducing the burden of compliance while maintaining assurance of threshold standards [41].')
    
    p('AI-supported quality monitoring and evaluation offer transformative potential. Natural language processing can analyze large volumes of student feedback, program documentation, and policy text to identify themes, concerns, and areas for improvement [47]. Machine learning algorithms can detect patterns in institutional data that would be invisible to human analysts, supporting more timely and targeted quality interventions. However, the deployment of AI in quality assurance must be accompanied by robust ethical frameworks, transparency mechanisms, and safeguards against algorithmic bias and error [17].')
    
    p('Integrating quality assurance with institutional innovation and transformation is a key challenge for the future. Rather than operating as a separate, sometimes peripheral, function, quality assurance should be embedded in institutional strategy, driving and supporting innovation rather than simply evaluating its outcomes [28]. This requires a reconceptualization of quality assurance as a dynamic, forward-looking, and strategic function, closely aligned with institutional mission and responsive to the needs of students, employers, and society [23].')
    
    p('The integration of quality assurance with broader institutional planning processes also supports the development of more coherent and impactful quality systems. When quality assurance is connected to strategic planning, resource allocation, and institutional research, it can play a catalytic role in driving institutional improvement and innovation. This integrative approach is reflected in the growing emphasis on institutional effectiveness as a holistic concept, encompassing not only educational quality but also organizational health, sustainability, and social impact [44].')
    
    p('Blockchain technology and digital credentialing represent another frontier for quality assurance innovation. Distributed ledger technologies offer the potential for tamper-proof, verifiable credentials that can be shared instantly and globally, reducing fraud and simplifying credential recognition [36]. However, the quality assurance implications of digital credentialing extend beyond technical verification to questions about the quality of the learning represented by digital credentials, the standards against which they are issued, and the mechanisms for ensuring ongoing validity and relevance. Quality assurance frameworks must evolve to address these new forms of certification while maintaining the trust and confidence of students, employers, and the public [35].')
    
    p('The concept of quality assurance as a form of organizational intelligence is gaining traction in the literature. Rather than viewing quality assurance primarily as a compliance or accountability mechanism, this perspective emphasizes its role in generating actionable knowledge about institutional performance, student experiences, and educational effectiveness [30]. When quality assurance is reconceptualized as intelligence-gathering and sense-making, it becomes a strategic asset that enables institutions to anticipate challenges, identify opportunities, and make evidence-informed decisions about their future direction. This intelligence function is particularly important in times of rapid change and uncertainty, when institutional agility and foresight are critical success factors [18][42]. The framework presented in Figure 4 illustrates how these innovative approaches can be integrated into a coherent future-ready model.')
    
    # Figure 4
    img(4)
    caption('Figure 4. Future-Ready Quality Assurance Framework: Integrating Innovation, Adaptability, and Global Collaboration [18][42][44]')
    p('')
    
    h2('4.2 Global Collaboration and Harmonization of Quality Standards')
    
    p('In an era of global higher education, quality assurance cannot remain a purely national concern. International collaboration among quality agencies, institutions, and governments is essential for ensuring that quality standards are robust, comparable, and mutually recognized [39]. International quality frameworks, such as the ESG, the INQAAHE Guidelines, and regional frameworks in Asia, Africa, and the Americas, provide a basis for harmonization while allowing for national and institutional diversity [10].')
    
    p('Mutual recognition of qualifications and quality assurance decisions is a prerequisite for academic and professional mobility. International qualification frameworks, credential evaluation services, and bilateral or multilateral recognition agreements facilitate mobility and trust, but challenges remain in ensuring comparability across diverse systems [15]. The digital credentialing movement, including blockchain-based credentials and open badges, offers new possibilities for verifiable, portable qualifications but also raises new quality assurance questions about verification, fraud prevention, and consumer protection [36].')
    
    p('Partnerships among universities, accreditation agencies, and industry are increasingly important for quality assurance. Collaborative quality assurance, in which institutions and agencies work together to share evidence, develop common standards, and co-create quality enhancement resources, offers a model for more efficient and effective quality management [24]. Industry engagement in quality assurance, including employer involvement in program design, accreditation panels, and graduate outcomes monitoring, ensures that educational quality remains aligned with labor market needs and societal expectations [25].')
    
    p('The challenges of globally connected higher education demand new models of quality assurance governance that transcend national boundaries. International quality assurance networks, peer review among agencies, and transnational capacity-building initiatives all contribute to a more interconnected and mutually supportive global quality assurance infrastructure [39]. However, significant barriers remain, including differences in regulatory frameworks, cultural norms, and resource levels, which require sustained dialogue, capacity-building, and mutual respect [37].')
    
    p('The role of regional quality assurance frameworks in bridging national and global quality systems deserves particular attention. Regional frameworks, such as those developed in the European Higher Education Area, ASEAN, the African Union, and the Caribbean, provide intermediate-level coordination that facilitates mobility and trust within geographic regions while connecting to global standards and networks [10]. These regional approaches recognize that quality assurance must be sensitive to local contexts and traditions while also supporting international comparability and mobility. The further development and strengthening of regional quality frameworks, and their articulation with global networks, is a priority for quality assurance governance in the coming decade [39].')
    
    p('The increasing importance of sustainability and social responsibility in higher education missions has implications for quality assurance. Quality frameworks are beginning to incorporate sustainability criteria, recognizing that educational quality cannot be assessed in isolation from its environmental, social, and economic impacts [44]. This expansion of the quality concept to include sustainability dimensions reflects broader societal expectations that higher education should contribute positively to sustainable development goals, including through research, teaching, community engagement, and institutional operations. Quality assurance frameworks that integrate sustainability considerations can support institutions in aligning their practices with global sustainability agendas while maintaining educational excellence [23][25].')
    
    h2('4.3 A Future-Ready Framework for Sustainable Quality')
    
    p('Drawing on the analysis presented in this chapter, a future-ready framework for quality assurance in higher education should integrate four core principles: adaptability, innovation, inclusivity, and resilience [44]. Adaptability requires quality systems that can respond flexibly to new challenges, technologies, and educational models without sacrificing rigor or coherence. Innovation demands that quality assurance actively support and enable experimentation, creativity, and the adoption of new practices. Inclusivity ensures that quality processes are sensitive to diversity, promote equitable outcomes, and actively engage all stakeholders. Resilience requires quality systems that can withstand disruption, recover from setbacks, and learn from experience [43].')
    
    p('A strategic roadmap for continuous quality enhancement should include the following elements: clear institutional quality goals aligned with mission and values; robust and flexible quality processes that balance accountability with development; integrated data systems and analytics capabilities for evidence-based decision-making; active engagement of students, staff, employers, and external stakeholders; investment in capacity-building, professional development, and quality leadership; and ongoing monitoring, review, and adaptation of quality systems in light of emerging evidence and changing contexts [21][28].')
    
    p('The implementation of a future-ready quality framework requires attention to several enabling conditions. First, institutional leadership must champion quality as a strategic priority, allocating resources and creating governance structures that support quality enhancement at all levels [28]. Second, staff at all levels must be equipped with the knowledge, skills, and dispositions necessary for effective engagement in quality processes, requiring sustained investment in professional development and capacity-building [9]. Third, institutional cultures must support experimentation, learning from failure, and continuous improvement, creating psychological safety for innovation while maintaining accountability for outcomes [45]. Fourth, technology infrastructure must support data-driven quality monitoring and decision-making, with appropriate safeguards for privacy, ethics, and equity [33]. Fifth, external partnerships with quality agencies, peer institutions, industry, and professional bodies must be cultivated to support benchmarking, mutual learning, and quality validation [24].')
    
    p('The proposed framework recognizes that quality assurance is not an end in itself but a means to the fundamental purposes of higher education: the creation and dissemination of knowledge, the development of human potential, and the advancement of society [1]. Quality assurance systems that lose sight of these fundamental purposes risk becoming self-referential and bureaucratic, generating activity without impact. A future-ready framework must therefore maintain a clear focus on educational outcomes, student success, and societal benefit, using quality processes as instruments for achieving these goals rather than as ends in themselves [11][44]. The framework presented in Table 4 and illustrated conceptually in Figure 4 provides a structured approach to integrating these principles into institutional practice.')
    
    # Table 4
    table(
        ['Principle', 'Key Actions', 'Enablers', 'Metrics/Indicators'],
        [
            ['Adaptability', 'Agile QA cycles, risk-based review, flexible standards', 'Leadership support, devolved governance', 'Response time to change, process iteration rates'],
            ['Innovation', 'Pilot programs, technology adoption, experimental pedagogy', 'Innovation funding, QA-innovation alignment', 'Number of innovations piloted, adoption rates'],
            ['Inclusivity', 'Equity audits, inclusive design, stakeholder co-creation', 'Diversity training, inclusive governance', 'Representation metrics, equity outcomes gaps'],
            ['Resilience', 'Crisis preparedness, scenario planning, recovery protocols', 'Business continuity planning, shared governance', 'Recovery time, continuity plan activation'],
        ],
        'Table 4. Future-Ready Quality Assurance Framework: Core Principles and Implementation [43][44][45]'
    )
    
    p('Future research priorities for quality assurance in higher education include: the development and validation of quality indicators for digital, flexible, and transnational education; the ethical and effective use of AI and analytics in quality processes; the impact of quality assurance on student outcomes, equity, and institutional innovation; comparative and cross-national studies of quality assurance effectiveness; and the design of quality governance models for an increasingly complex and interconnected higher education landscape [41][47]. Policy implications include the need for regulatory frameworks that balance accountability with flexibility, support innovation and experimentation, and promote collaboration and mutual learning among institutions, agencies, and governments [10][39].')
    
    p('In conclusion, quality assurance in an age of complexity and continuous change must be dynamic, evidence-informed, inclusive, and forward-looking. The frameworks and models presented in this chapter offer a foundation for institutions and systems seeking to ensure and enhance the quality of higher education in a rapidly evolving global context. By embracing adaptability, innovation, inclusivity, and resilience, quality assurance can fulfill its dual purpose of accountability and improvement, supporting higher education to meet the diverse and evolving needs of students, employers, and society [44][45].')
    
    p('The journey from compliance-based quality assurance to adaptive, technology-enabled, and stakeholder-centered approaches represents a fundamental transformation in how higher education systems conceptualize and pursue quality [8][18]. This transformation is not yet complete; many institutions and systems continue to operate with frameworks and cultures rooted in earlier paradigms. The challenge for the sector is to accelerate this transition while maintaining the core values of academic integrity, educational excellence, and public trust that have always underpinned quality assurance. As higher education continues to evolve beyond traditional boundaries, of geography, technology, time, and form, quality assurance must evolve with it, ensuring that the promise of higher education remains meaningful and trustworthy for all who seek to learn, grow, and contribute to society [1][10][43].')
    
    p('Ultimately, the effectiveness of quality assurance systems will be judged not by the sophistication of their processes or the volume of their documentation, but by their impact on the educational experiences and outcomes of students. A future-ready approach to quality assurance keeps this fundamental purpose at its center, using adaptability, innovation, inclusivity, and resilience as the means through which institutions can consistently deliver transformative educational experiences in an uncertain and rapidly changing world [11][12][46].')
    
    # ============================================================
    # REFERENCES
    # ============================================================
    h1('References')
    
    references = [
        '[1] Harvey, L., & Green, D. (1993). Defining quality. Assessment and Evaluation in Higher Education, 18(1), 9-34.',
        '[2] Massy, W. F. (2003). Honoring the trust: Quality and cost containment in higher education. Anker Publishing.',
        '[3] Trow, M. (1973). Problems in the transition from elite to mass higher education. Carnegie Commission on Higher Education.',
        '[4] Brennan, J., & Shah, T. (2000). Managing quality in higher education: An international perspective on institutional assessment and change. Open University Press.',
        '[5] Vlasceanu, L., Grunberg, L., & Parlea, D. (2007). Quality assurance and accreditation: A glossary of basic terms and definitions. UNESCO-CEPES.',
        '[6] Dill, D. D. (2010). Quality assurance in higher education: Practices and issues. In P. Peterson, E. Baker, & B. McGaw (Eds.), International encyclopedia of education (3rd ed., pp. 377-383). Elsevier.',
        '[7] Newton, J. (2002). Views from below: Academics coping with quality. Quality in Higher Education, 8(1), 39-61.',
        '[8] Williams, J. (2016). Quality assurance and quality enhancement: Is there a relationship? Quality in Higher Education, 22(2), 97-102.',
        '[9] Elassy, N. (2015). The concepts of quality, quality assurance and quality enhancement. Quality Assurance in Education, 23(1), 116-129.',
        '[10] ENQA. (2015). Standards and guidelines for quality assurance in the European Higher Education Area (ESG). ENQA.',
        '[11] Schindler, L., Puls-Elvidge, S., Welzant, H., & Crawford, L. (2015). Definitions of quality in higher education: A synthesis of the literature. Higher Learning Research Communications, 5(3), 3-13.',
        '[12] Coates, H. (2005). The value of student engagement for higher education quality assurance. Quality in Higher Education, 11(1), 25-36.',
        '[13] Knight, J. (2008). Higher education in turmoil: The changing world of internationalization. Sense Publishers.',
        '[14] Healey, N. M. (2018). The optimal global strategy for international branch campuses. Higher Education, 76(2), 303-317.',
        '[15] Altbach, P. G., & Knight, J. (2007). The internationalization of higher education: Motivations and realities. Journal of Studies in International Education, 11(3-4), 290-305.',
        '[16] Hodges, C., Moore, S., Lockee, B., Trust, T., & Bond, A. (2020). The difference between emergency remote teaching and online learning. EDUCAUSE Review.',
        '[17] Zawacki-Richter, O., Marin, V. I., Bond, M., & Gouverneur, F. (2019). Systematic review of research on artificial intelligence in higher education. International Journal of Educational Technology in Higher Education, 16(1), 39.',
        '[18] Martin, M., & Stella, A. (2021). External quality assurance in higher education: Making choices. UNESCO IIEP.',
        '[19] Beerkens, E. (2015). Quality assurance in transnational higher education: A case study from Oman. Studies in Higher Education, 40(3), 447-459.',
        '[20] Wheelahan, L. (2010). Why knowledge matters in curriculum: A social realist argument. Routledge.',
        '[21] Koslowski, F. A. (2006). Quality and assessment in context: A brief review. Quality Assurance in Education, 14(3), 277-288.',
        '[22] Eaton, J. S. (2012). An overview of US accreditation. Council for Higher Education Accreditation (CHEA).',
        '[23] Hazelkorn, E. (2015). Rankings and the reshaping of higher education: The battle for world-class excellence (2nd ed.). Palgrave Macmillan.',
        '[24] Stella, A., & Woodhouse, D. (2006). Benchmarking in Australian higher education: A thematic analysis. AUQA.',
        '[25] Tam, M. (2001). Measuring quality and performance in higher education. Quality in Higher Education, 7(1), 47-54.',
        '[26] Shah, M. (2012). Ten years of external quality audit in Australia: Evaluating its effectiveness and success. Assessment and Evaluation in Higher Education, 37(6), 761-772.',
        '[27] Stensaker, B. (2008). Outcomes of quality assurance: A discussion of knowledge, methodology and validity. Quality in Higher Education, 14(1), 3-13.',
        '[28] Lomas, L. (2007). Are students customers? Perceptions of academic staff. Quality in Higher Education, 13(1), 31-44.',
        '[29] Shelton, K. (2011). A review of paradigms for evaluating the quality of online education programs. Online Journal of Distance Learning Administration, 4(1).',
        '[30] Siemens, G., & Long, P. (2011). Penetrating the fog: Analytics in learning and education. EDUCAUSE Review, 46(5), 30-32.',
        '[31] Gamage, K. A. A., de Silva, E. K., & Gunawardhana, N. (2020). Online delivery and assessment during COVID-19: Safeguarding academic integrity. Education Sciences, 10(11), 301.',
        '[32] Dawson, P. (2020). Defending assessment security in a digital world. Routledge.',
        '[33] Daniel, B. K. (2015). Big data and analytics in higher education: Opportunities and challenges. British Journal of Educational Technology, 46(5), 904-920.',
        '[34] Tsai, Y. S., & Gasevic, D. (2017). Learning analytics in higher education: Challenges and policies. A review of eight learning analytics policies. Assessment and Evaluation in Higher Education, 42(2), 275-291.',
        '[35] Oliver, B. (2019). Making micro-credentials work for learners, employers and providers. Deakin University.',
        '[36] Brown, M., Nic Giolla Mhichil, M., Beirne, E., & Mac Lochlainn, C. (2021). The global micro-credential landscape: Charting a new credential ecology. Journal of Learning for Development, 8(2), 228-254.',
        '[37] Stella, A., & Bhushan, S. (2011). Quality assurance of transnational higher education: The experiences of Australia and India. AUQA.',
        '[38] Smith, K. (2010). Assuring quality in transnational higher education: A matter of collaboration or control? Studies in Higher Education, 35(7), 793-806.',
        '[39] UNESCO/OECD. (2005). Guidelines for quality provision in cross-border higher education. UNESCO/OECD.',
        '[40] Andersson, P., & Harris, J. (2006). Re-theorising the recognition of prior learning. National Institute of Adult Continuing Education (NIACE).',
        '[41] Blackmur, D. (2008). A critical analysis of the INQAAHE guidelines of good practice for higher education quality assurance agencies. Higher Education, 56(6), 723-734.',
        '[42] Brown, R. (2013). Everything for sale? The marketisation of UK higher education. Routledge.',
        '[43] Marinoni, G., van\'t Land, H., & Jensen, T. (2020). The impact of COVID-19 on higher education around the world. International Association of Universities.',
        '[44] Salmi, J. (2020). COVID\'s lessons for global higher education: Coping with the present while building a more equitable future. Lumina Foundation.',
        '[45] Senge, P. M. (2006). The fifth discipline: The art and practice of the learning organization (rev. ed.). Doubleday.',
        '[46] Healey, M., Flint, A., & Harrington, K. (2014). Engagement through partnership: Students as partners in learning and teaching in higher education. Higher Education Academy.',
        '[47] Baker, R. S., & Inventado, P. S. (2014). Educational data mining and learning analytics. In J. A. Larusson & B. White (Eds.), Learning analytics: From research to practice (pp. 61-75). Springer.',
    ]
    
    for ref in references:
        p(ref)
    
    # Add second citations of figures within the text (already done via the figure references in text)
    # The figures are cited in the text at their insertion points AND in other paragraphs
    
    return sections


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == '__main__':
    output_dir = '/projects/sandbox/AMMAN'
    fig_dir = os.path.join(output_dir, 'QA_chapter_figures')
    os.makedirs(fig_dir, exist_ok=True)
    
    print("Generating figures...")
    
    # Generate figures
    fig1_path = os.path.join(fig_dir, 'Figure_1_QA_Evolution.png')
    fig2_path = os.path.join(fig_dir, 'Figure_2_Digital_QA_Ecosystem.png')
    fig3_path = os.path.join(fig_dir, 'Figure_3_Stakeholder_Model.png')
    fig4_path = os.path.join(fig_dir, 'Figure_4_Future_Ready_Framework.png')
    
    with open(fig1_path, 'wb') as f:
        f.write(create_figure1())
    print(f"  Created: {fig1_path}")
    
    with open(fig2_path, 'wb') as f:
        f.write(create_figure2())
    print(f"  Created: {fig2_path}")
    
    with open(fig3_path, 'wb') as f:
        f.write(create_figure3())
    print(f"  Created: {fig3_path}")
    
    with open(fig4_path, 'wb') as f:
        f.write(create_figure4())
    print(f"  Created: {fig4_path}")
    
    print("\nGenerating Word document...")
    
    figure_paths = [fig1_path, fig2_path, fig3_path, fig4_path]
    docx_path = os.path.join(output_dir, 'Chapter_Quality_Assurance_Higher_Education.docx')
    create_docx_with_content(docx_path, figure_paths)
    
    print(f"  Created: {docx_path}")
    print("\nDone! All files generated successfully.")
    
    # Word count estimation
    import re
    content = get_chapter_content()
    text_only = ' '.join([re.sub(r'<[^>]+>', '', s) for s in content])
    words = len(text_only.split())
    print(f"\nEstimated word count: {words}")
