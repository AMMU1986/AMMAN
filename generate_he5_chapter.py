#!/usr/bin/env python3
"""
Generate the complete academic chapter:
"AI Readiness Assessment Framework for Higher Education 5.0"
Outputs: Word document (.docx) with embedded tables, figures, and references.
Uses only Python standard library (zipfile, xml, struct, zlib).
"""

import os
import sys
import struct
import zlib
import zipfile
import math
import random
from io import BytesIO
from xml.etree.ElementTree import Element, SubElement, tostring

# ============================================================
# PNG IMAGE GENERATION (Pure Python)
# ============================================================

def create_png_bytes(width, height, pixel_func):
    """Create a PNG image from a pixel function that returns (r,g,b) for each (x,y)."""
    def chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    header = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    
    raw_data = bytearray()
    for y in range(height):
        raw_data += b'\x00'  # filter byte (none)
        for x in range(width):
            r, g, b = pixel_func(x, y, width, height)
            raw_data += bytes([max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))])
    
    return header + chunk(b'IHDR', ihdr) + chunk(b'IDAT', zlib.compress(bytes(raw_data), 9)) + chunk(b'IEND', b'')


def draw_bar_chart(x, y, w, h, values, colors, labels, title, x_label, y_label):
    """Returns pixel color for a bar chart area."""
    # Chart margins
    left_m, right_m, top_m, bottom_m = int(w*0.15), int(w*0.05), int(h*0.12), int(h*0.18)
    chart_w = w - left_m - right_m
    chart_h = h - top_m - bottom_m
    
    cx = x - left_m
    cy = y - top_m
    
    max_val = max(values) * 1.1
    n = len(values)
    bar_w = chart_w // (n * 2)
    
    # Background
    if x < left_m or x >= w - right_m or y < top_m or y >= h - bottom_m:
        # Title area
        if y < top_m:
            return (245, 245, 250)
        return (245, 245, 250)
    
    # Chart area background
    # Grid lines
    for i in range(5):
        grid_y = top_m + int(chart_h * (1 - i/4))
        if abs(y - grid_y) < 1:
            return (220, 220, 220)
    
    # Bars
    for i, val in enumerate(values):
        bar_x_start = left_m + int(chart_w * (i + 0.3) / n)
        bar_x_end = left_m + int(chart_w * (i + 0.7) / n)
        bar_height = int(chart_h * val / max_val)
        bar_y_top = top_m + chart_h - bar_height
        
        if bar_x_start <= x <= bar_x_end and bar_y_top <= y <= top_m + chart_h:
            color = colors[i % len(colors)]
            # Gradient effect
            progress = (y - bar_y_top) / max(1, (top_m + chart_h - bar_y_top))
            r = int(color[0] * (0.7 + 0.3 * progress))
            g = int(color[1] * (0.7 + 0.3 * progress))
            b = int(color[2] * (0.7 + 0.3 * progress))
            return (r, g, b)
    
    return (255, 255, 255)


def figure1_pixel(x, y, w, h):
    """Figure 1: AI Readiness Dimensions Framework - Radar/Spider concept as bar chart."""
    dimensions = [78, 65, 72, 58, 82, 45, 68, 55]
    colors = [(41, 128, 185), (39, 174, 96), (142, 68, 173), (230, 126, 34),
              (231, 76, 60), (52, 152, 219), (46, 204, 113), (155, 89, 182)]
    return draw_bar_chart(x, y, w, h, dimensions, colors, 
                          ['Tech', 'Data', 'Faculty', 'Student', 'Culture', 'Ethics', 'Policy', 'Leadership'],
                          'AI Readiness Dimensions', 'Dimension', 'Score (%)')


def figure2_pixel(x, y, w, h):
    """Figure 2: Readiness Maturity Levels - Stacked progression."""
    levels = [25, 45, 65, 85, 95]
    colors = [(231, 76, 60), (230, 126, 34), (241, 196, 15), (39, 174, 96), (41, 128, 185)]
    
    left_m, right_m, top_m, bottom_m = int(w*0.12), int(w*0.05), int(h*0.12), int(h*0.15)
    chart_w = w - left_m - right_m
    chart_h = h - top_m - bottom_m
    
    if y < top_m or y >= h - bottom_m or x < left_m or x >= w - right_m:
        return (245, 245, 250)
    
    # Pyramid/staircase visualization
    n = len(levels)
    for i in range(n):
        step_y_start = top_m + int(chart_h * (n - 1 - i) / n)
        step_y_end = top_m + int(chart_h * (n - i) / n)
        step_x_end = left_m + int(chart_w * levels[i] / 100)
        
        if step_y_start <= y < step_y_end and left_m <= x < step_x_end:
            color = colors[i]
            # Add slight shading
            shade = 0.85 + 0.15 * ((x - left_m) / max(1, step_x_end - left_m))
            return (int(color[0]*shade), int(color[1]*shade), int(color[2]*shade))
    
    return (255, 255, 255)


def figure3_pixel(x, y, w, h):
    """Figure 3: Faculty vs Student AI Acceptance - Grouped bars."""
    faculty = [72, 58, 65, 78, 55]
    students = [85, 72, 78, 68, 82]
    colors_f = (41, 128, 185)
    colors_s = (39, 174, 96)
    
    left_m, right_m, top_m, bottom_m = int(w*0.12), int(w*0.05), int(h*0.12), int(h*0.15)
    chart_w = w - left_m - right_m
    chart_h = h - top_m - bottom_m
    
    if y < top_m or y >= h - bottom_m or x < left_m or x >= w - right_m:
        return (245, 245, 250)
    
    max_val = 100
    n = len(faculty)
    group_w = chart_w / n
    bar_w = group_w * 0.35
    
    for i in range(n):
        # Faculty bar
        fb_x_start = int(left_m + group_w * i + group_w * 0.1)
        fb_x_end = int(fb_x_start + bar_w)
        fb_height = int(chart_h * faculty[i] / max_val)
        fb_y_top = top_m + chart_h - fb_height
        
        if fb_x_start <= x <= fb_x_end and fb_y_top <= y <= top_m + chart_h:
            shade = 0.8 + 0.2 * ((y - fb_y_top) / max(1, chart_h - fb_height))
            return (int(colors_f[0]*shade), int(colors_f[1]*shade), int(colors_f[2]*shade))
        
        # Student bar
        sb_x_start = int(fb_x_end + group_w * 0.05)
        sb_x_end = int(sb_x_start + bar_w)
        sb_height = int(chart_h * students[i] / max_val)
        sb_y_top = top_m + chart_h - sb_height
        
        if sb_x_start <= x <= sb_x_end and sb_y_top <= y <= top_m + chart_h:
            shade = 0.8 + 0.2 * ((y - sb_y_top) / max(1, chart_h - sb_height))
            return (int(colors_s[0]*shade), int(colors_s[1]*shade), int(colors_s[2]*shade))
    
    # Grid lines
    for i in range(5):
        grid_y = top_m + int(chart_h * i / 4)
        if abs(y - grid_y) < 1:
            return (220, 220, 220)
    
    return (255, 255, 255)


def figure4_pixel(x, y, w, h):
    """Figure 4: Strategic Implementation Roadmap - Phase timeline."""
    phases = [
        ((231, 76, 60), 0.0, 0.25),    # Phase 1: Awareness
        ((230, 126, 34), 0.25, 0.50),   # Phase 2: Preparation
        ((241, 196, 15), 0.50, 0.75),   # Phase 3: Implementation
        ((39, 174, 96), 0.75, 1.0),     # Phase 4: Transformation
    ]
    
    left_m, right_m, top_m, bottom_m = int(w*0.08), int(w*0.05), int(h*0.15), int(h*0.15)
    chart_w = w - left_m - right_m
    chart_h = h - top_m - bottom_m
    
    if y < top_m or y >= h - bottom_m or x < left_m or x >= w - right_m:
        return (245, 245, 250)
    
    # Arrow/chevron phases
    for color, start, end in phases:
        px_start = int(left_m + chart_w * start)
        px_end = int(left_m + chart_w * end)
        
        # Main band (middle 60% of height)
        band_top = top_m + int(chart_h * 0.2)
        band_bottom = top_m + int(chart_h * 0.8)
        
        if px_start <= x < px_end and band_top <= y <= band_bottom:
            # Chevron shape - create arrow effect
            mid_y = (band_top + band_bottom) / 2
            dist_from_center = abs(y - mid_y) / ((band_bottom - band_top) / 2)
            
            # Right edge tapers to point
            right_edge = px_end - int((px_end - px_start) * 0.1 * dist_from_center)
            if x <= right_edge:
                shade = 0.85 + 0.15 * (1 - dist_from_center)
                return (int(color[0]*shade), int(color[1]*shade), int(color[2]*shade))
    
    return (255, 255, 255)


# ============================================================
# DOCX GENERATION (Pure Python using zipfile + XML)
# ============================================================

WORD_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
REL_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG_REL_NS = 'http://schemas.openxmlformats.org/package/2006/relationships'
CT_NS = 'http://schemas.openxmlformats.org/package/2006/content-types'
DRAW_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
WP_NS = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
PIC_NS = 'http://schemas.openxmlformats.org/drawingml/2006/picture'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

def make_docx(content_paragraphs, tables, images, output_path):
    """
    Create a .docx file.
    content_paragraphs: list of dicts with keys: text, style ('Title','Heading1','Heading2','Normal','Caption')
    tables: list of (position_index, table_data) where table_data is list of rows (list of cells)
    images: list of (position_index, image_path, caption)
    """
    
    buf = BytesIO()
    
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        # [Content_Types].xml
        ct = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        ct += '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        ct += '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        ct += '<Default Extension="xml" ContentType="application/xml"/>'
        ct += '<Default Extension="png" ContentType="image/png"/>'
        ct += '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        ct += '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        ct += '</Types>'
        zf.writestr('[Content_Types].xml', ct)
        
        # _rels/.rels
        rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        rels += '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        rels += '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        rels += '</Relationships>'
        zf.writestr('_rels/.rels', rels)
        
        # Add images to zip and build relationships
        img_rels = []
        for idx, (pos, img_path, caption) in enumerate(images):
            img_id = f'rId{idx + 10}'
            img_name = f'image{idx+1}.png'
            with open(img_path, 'rb') as f:
                zf.writestr(f'word/media/{img_name}', f.read())
            img_rels.append((img_id, img_name))
        
        # word/_rels/document.xml.rels
        doc_rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        doc_rels += '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        doc_rels += '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        for img_id, img_name in img_rels:
            doc_rels += f'<Relationship Id="{img_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{img_name}"/>'
        doc_rels += '</Relationships>'
        zf.writestr('word/_rels/document.xml.rels', doc_rels)
        
        # word/styles.xml
        styles = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        styles += '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        
        # Normal style
        styles += '<w:style w:type="paragraph" w:styleId="Normal" w:default="1"><w:name w:val="Normal"/>'
        styles += '<w:pPr><w:spacing w:after="200" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>'
        styles += '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr></w:style>'
        
        # Title style
        styles += '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
        styles += '<w:pPr><w:spacing w:after="300"/><w:jc w:val="center"/></w:pPr>'
        styles += '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="32"/></w:rPr></w:style>'
        
        # Heading1
        styles += '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
        styles += '<w:pPr><w:spacing w:before="360" w:after="200"/></w:pPr>'
        styles += '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr></w:style>'
        
        # Heading2
        styles += '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
        styles += '<w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>'
        styles += '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="26"/></w:rPr></w:style>'
        
        # Caption style
        styles += '<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="Caption"/>'
        styles += '<w:pPr><w:spacing w:after="200"/><w:jc w:val="center"/></w:pPr>'
        styles += '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:i/><w:sz w:val="22"/></w:rPr></w:style>'
        
        # Abstract style  
        styles += '<w:style w:type="paragraph" w:styleId="Abstract"><w:name w:val="Abstract"/>'
        styles += '<w:pPr><w:spacing w:after="200" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/><w:ind w:left="720" w:right="720"/></w:pPr>'
        styles += '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="22"/></w:rPr></w:style>'
        
        styles += '</w:styles>'
        zf.writestr('word/styles.xml', styles)
        
        # word/document.xml - Build the main document
        doc = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        doc += '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        doc += 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        doc += 'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        doc += 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        doc += 'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        doc += '<w:body>'
        
        # Merge content with tables and images at their positions
        # Build ordered content list
        all_items = []
        for i, para in enumerate(content_paragraphs):
            all_items.append(('para', i, para))
        
        for pos, table_data in tables:
            all_items.append(('table', pos, table_data))
        
        for idx, (pos, img_path, caption) in enumerate(images):
            all_items.append(('image', pos, (idx, caption)))
        
        # Sort by position
        all_items.sort(key=lambda x: x[1])
        
        for item_type, pos, data in all_items:
            if item_type == 'para':
                para = data
                style = para.get('style', 'Normal')
                text = para.get('text', '')
                bold = para.get('bold', False)
                
                doc += '<w:p>'
                doc += f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
                
                # Handle text with potential bold segments
                if bold:
                    doc += f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'
                else:
                    doc += f'<w:r><w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'
                doc += '</w:p>'
                
            elif item_type == 'table':
                table_data = data
                doc += '<w:tbl>'
                doc += '<w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="5000" w:type="pct"/>'
                doc += '<w:tblBorders>'
                for border in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
                    doc += f'<w:{border} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                doc += '</w:tblBorders></w:tblPr>'
                
                for row_idx, row in enumerate(table_data):
                    doc += '<w:tr>'
                    for cell in row:
                        doc += '<w:tc>'
                        doc += '<w:tcPr><w:tcW w:w="0" w:type="auto"/>'
                        if row_idx == 0:
                            doc += '<w:shd w:val="clear" w:color="auto" w:fill="2980B9"/>'
                        doc += '</w:tcPr>'
                        doc += '<w:p>'
                        if row_idx == 0:
                            doc += '<w:pPr><w:jc w:val="center"/></w:pPr>'
                            doc += f'<w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="22"/></w:rPr><w:t xml:space="preserve">{escape_xml(str(cell))}</w:t></w:r>'
                        else:
                            doc += f'<w:r><w:rPr><w:sz w:val="22"/></w:rPr><w:t xml:space="preserve">{escape_xml(str(cell))}</w:t></w:r>'
                        doc += '</w:p></w:tc>'
                    doc += '</w:tr>'
                doc += '</w:tbl>'
                # Add spacing after table
                doc += '<w:p><w:pPr><w:spacing w:after="200"/></w:pPr></w:p>'
                
            elif item_type == 'image':
                img_idx, caption = data
                img_id = f'rId{img_idx + 10}'
                # Image dimensions in EMU (1 inch = 914400 EMU), make it ~5 inches wide, ~3.5 inches tall
                cx = 4572000  # ~5 inches
                cy = 3200400  # ~3.5 inches
                
                doc += '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
                doc += '<w:r><w:drawing>'
                doc += f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
                doc += f'<wp:extent cx="{cx}" cy="{cy}"/>'
                doc += '<wp:docPr id="' + str(img_idx+1) + '" name="Figure ' + str(img_idx+1) + '"/>'
                doc += '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
                doc += '<pic:pic><pic:nvPicPr>'
                doc += '<pic:cNvPr id="' + str(img_idx+1) + '" name="Figure ' + str(img_idx+1) + '"/>'
                doc += '<pic:cNvPicPr/></pic:nvPicPr>'
                doc += '<pic:blipFill><a:blip r:embed="' + img_id + '"/>'
                doc += '<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
                doc += '<pic:spPr><a:xfrm><a:off x="0" y="0"/>'
                doc += f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
                doc += '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
                doc += '</pic:pic></a:graphicData></a:graphic>'
                doc += '</wp:inline></w:drawing></w:r></w:p>'
                
                # Caption
                doc += '<w:p><w:pPr><w:pStyle w:val="Caption"/></w:pPr>'
                doc += f'<w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">{escape_xml(caption)}</w:t></w:r></w:p>'
        
        # Section properties (A4 page)
        doc += '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        doc += '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
        doc += '</w:sectPr>'
        doc += '</w:body></w:document>'
        
        zf.writestr('word/document.xml', doc)
    
    with open(output_path, 'wb') as f:
        f.write(buf.getvalue())
    
    return output_path


def escape_xml(text):
    """Escape XML special characters."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')


# ============================================================
# CHAPTER CONTENT
# ============================================================

def get_chapter_content():
    """Return the full chapter content as structured paragraphs."""
    
    paragraphs = []
    pos = [0]  # mutable position counter
    
    def add(text, style='Normal', bold=False):
        paragraphs.append({'text': text, 'style': style, 'bold': bold, 'pos': pos[0]})
        pos[0] += 1
        return pos[0] - 1
    
    # Title
    add("AI Readiness Assessment Framework for Higher Education 5.0: Institutional Transformation Through Intelligent Technologies", 'Title', bold=True)
    
    # Abstract
    add("Abstract", 'Heading1', bold=True)
    add("The rapid evolution of artificial intelligence is transforming higher education systems worldwide, demanding a paradigm shift from Education 4.0 toward Education 5.0. This chapter presents a comprehensive AI Readiness Assessment Framework designed to evaluate and guide the preparedness of higher education institutions for AI-enabled academic transformation. The framework integrates multiple dimensions including technological infrastructure, data governance, faculty competencies, student preparedness, organizational culture, leadership support, ethical governance, and institutional policy. A structured classification system categorizes institutions across readiness maturity levels ranging from emerging to transformation-ready stages. The chapter examines faculty and student acceptance of AI technologies, organizational and ethical readiness requirements, and proposes data-driven decision-making approaches for sustainable AI adoption. A strategic implementation roadmap offers phased guidance for institutions seeking systematic AI integration across academic and administrative functions. The implications for building human-centered, inclusive, adaptive, and sustainable higher education ecosystems aligned with Education 5.0 principles are discussed, along with future research directions for validating the proposed assessment approach.", 'Abstract')
    
    add("Keywords: Artificial Intelligence, Higher Education 5.0, AI Readiness, Assessment Framework, Institutional Transformation, Digital Education, Faculty Acceptance, Ethical AI Governance", 'Normal', bold=True)
    
    # Section 1
    add("1. Conceptual Foundations of Higher Education 5.0", 'Heading1', bold=True)
    
    add("1.1 Evolution from Education 4.0 to Education 5.0", 'Heading2', bold=True)
    
    add("The global higher education landscape has undergone successive transformative phases, each driven by technological advancement and evolving societal needs. Education 1.0 was characterized by teacher-centered instruction and passive knowledge transfer, while Education 2.0 introduced interactive pedagogies and early digital tools [1]. Education 3.0 embraced networked learning, open educational resources, and collaborative knowledge construction [2]. Education 4.0, which dominated discourse throughout the 2010s and early 2020s, centered on automation, data analytics, the Internet of Things, and cyber-physical learning systems integrated within the framework of Industry 4.0 [3]. However, growing recognition of the limitations of purely technology-driven approaches has catalyzed the emergence of Education 5.0, which prioritizes human-centered values, sustainability, resilience, and the harmonious coexistence of human intelligence with artificial intelligence [4].")
    
    add("Education 5.0 represents a fundamental philosophical shift rather than merely a technological upgrade. While Education 4.0 emphasized efficiency, automation, and data-driven optimization, Education 5.0 recenters the human experience within technologically enhanced learning environments [5]. This new paradigm recognizes that artificial intelligence should augment rather than replace human capabilities, fostering creativity, critical thinking, emotional intelligence, and ethical reasoning alongside technical competencies [6]. The transition demands that institutions reconceptualize their educational missions, moving beyond knowledge delivery toward holistic human development supported by intelligent technologies [7]. In practical terms, this means that universities and colleges must redesign curricula, retrain faculty, upgrade infrastructure, and reformulate governance structures to accommodate the unique demands of human-AI collaborative learning ecosystems.")
    
    add("The Education 5.0 framework aligns with the broader Society 5.0 vision originally proposed in Japan, which envisions a super-smart society where digital transformation serves human well-being, social inclusion, and environmental sustainability [8]. In this context, higher education institutions are expected to function as innovation ecosystems that leverage AI not merely for operational efficiency but for expanding human potential, promoting equity, and addressing complex global challenges [9]. The personalization capabilities of AI enable differentiated learning pathways that respect individual differences in cognitive style, pace, cultural background, and learning objectives, thereby advancing inclusive education agendas [10]. Furthermore, Education 5.0 emphasizes the co-creation of knowledge between humans and machines, where AI serves as an intellectual partner that extends cognitive capabilities rather than a tool that merely automates routine tasks.")
    
    add("The sustainability dimension of Education 5.0 extends beyond environmental considerations to encompass the sustainability of educational practices themselves. Institutions must develop AI implementations that are economically viable, socially equitable, technologically maintainable, and ethically sound over extended timeframes [11]. This requires moving beyond pilot projects and fragmented initiatives toward systemic integration strategies supported by robust assessment frameworks that can measure institutional preparedness and guide transformation efforts. The concept of sustainable AI adoption acknowledges that technology implementations must be designed for long-term viability, considering factors such as ongoing maintenance costs, skills renewal requirements, vendor dependency risks, and the environmental footprint of computational infrastructure. Institutions that fail to address sustainability from the outset risk creating technological debt that ultimately undermines the educational benefits they seek to achieve.")
    
    add("The transition from Education 4.0 to Education 5.0 also demands attention to the socioemotional dimensions of learning that were often neglected in technology-focused paradigms. Education 5.0 recognizes that human flourishing requires the development of empathy, cultural sensitivity, collaborative skills, and ethical judgment alongside cognitive and technical competencies [4]. AI technologies can support these goals through personalized mentoring systems, collaborative learning platforms that match diverse perspectives, and simulation environments that develop ethical reasoning skills. However, achieving this vision requires institutions to possess sophisticated readiness across multiple dimensions simultaneously, creating the imperative for comprehensive assessment frameworks.")
    
    add("1.2 Role of Artificial Intelligence in Academic Transformation", 'Heading2', bold=True)
    
    add("Artificial intelligence is fundamentally reshaping every dimension of higher education, from teaching and learning to research, administration, and student support services. In the pedagogical domain, AI-powered adaptive learning systems analyze student performance data in real time to customize content delivery, adjust difficulty levels, and provide immediate formative feedback [12]. Intelligent tutoring systems employ natural language processing and machine learning algorithms to simulate one-on-one instructional interactions at scale, potentially democratizing access to personalized academic support [13]. Generative AI tools are transforming content creation, enabling rapid development of instructional materials, assessment items, and multimedia resources tailored to specific learning objectives and student populations [14]. The pedagogical applications of AI extend to curriculum design optimization, where machine learning algorithms analyze student outcome data across multiple cohorts to identify the most effective sequencing and delivery methods for different types of content and learner profiles.")
    
    add("In assessment and evaluation, AI offers transformative capabilities through automated essay scoring, plagiarism detection, competency-based assessment, and learning analytics that identify at-risk students before academic failure occurs [15]. These technologies enable continuous assessment models that replace or supplement high-stakes examinations with ongoing performance monitoring, providing richer and more actionable insights into student learning trajectories [16]. However, significant concerns regarding algorithmic bias, fairness, and the validity of AI-generated assessments require careful attention to ensure that automated systems do not perpetuate or amplify existing educational inequities [17]. The complexity of assessment transformation is further compounded by generative AI tools that enable students to produce sophisticated academic work with minimal original effort, challenging traditional notions of academic authorship and intellectual achievement.")
    
    add("Research activities are similarly being transformed through AI-assisted literature review, hypothesis generation, data analysis, and experimental design. Machine learning algorithms can identify patterns in large datasets that would be imperceptible to human researchers, accelerating discovery across disciplines [18]. AI-powered research management tools streamline grant writing, peer review processes, and research collaboration, potentially reducing administrative burden and allowing researchers to focus on creative intellectual work [19]. In student support services, AI chatbots and virtual assistants handle routine inquiries, provide 24/7 academic advising, and connect students with appropriate institutional resources, improving service accessibility while reducing staff workload [20]. These chatbot systems increasingly employ sentiment analysis and natural language understanding to detect students experiencing emotional distress or academic disengagement, enabling proactive intervention before problems escalate.")
    
    add("Institutional decision-making is increasingly informed by AI-driven predictive analytics that forecast enrollment patterns, optimize resource allocation, identify infrastructure needs, and evaluate program effectiveness [21]. These capabilities enable evidence-based governance that can respond proactively to emerging challenges rather than reacting to crises after they develop. Administrative AI applications extend to financial planning, facilities management, human resources optimization, and strategic scenario modeling that helps institutional leaders evaluate the potential consequences of different policy decisions before implementation. Nevertheless, the effective deployment of AI across these domains requires substantial institutional readiness spanning technological, human, organizational, and ethical dimensions, as illustrated in Figure 1.")
    
    # FIGURE 1 position marker
    fig1_pos = pos[0]
    pos[0] += 1  # reserve for figure
    
    add("As depicted in Figure 1, the multi-dimensional nature of AI readiness requires institutions to simultaneously develop capabilities across technological infrastructure, data governance, human competencies, organizational culture, and ethical frameworks. No single dimension can be addressed in isolation; rather, institutional readiness emerges from the synergistic development of all components. The framework illustrated in Figure 1 demonstrates that institutions achieving high readiness levels exhibit balanced development across all dimensions, whereas institutions with significant disparities between dimensions frequently experience implementation failures even when individual components appear strong in isolation.")
    
    add("1.3 Dimensions of AI Readiness in Higher Education", 'Heading2', bold=True)
    
    add("AI readiness in higher education encompasses multiple interconnected dimensions that collectively determine an institution's capacity to successfully implement and sustain AI-enabled practices. The first and most frequently discussed dimension is technological infrastructure, which includes computing hardware, network bandwidth, cloud services, data storage, software platforms, and integration architectures necessary to support AI applications at institutional scale [22]. Without adequate infrastructure, even the most sophisticated AI solutions cannot be deployed effectively. Technological readiness extends beyond mere hardware availability to encompass the architecture decisions that determine whether AI applications can be integrated with existing institutional systems, the security frameworks that protect sensitive educational data, and the scalability provisions that allow systems to grow with increasing demand.")
    
    add("Data availability and governance constitute the second critical dimension. AI systems require large volumes of high-quality, well-structured data for training, validation, and ongoing operation [23]. Institutions must establish comprehensive data governance frameworks that address data collection, storage, quality assurance, access control, interoperability standards, and compliance with privacy regulations such as GDPR and FERPA [24]. The absence of institutional data strategies frequently represents a significant barrier to AI adoption, as fragmented data silos prevent the integrated analytics that AI applications demand. Moreover, the quality of AI outputs is directly dependent on the quality of input data, making data governance not merely a compliance requirement but a fundamental determinant of AI system effectiveness. Institutions must invest in data cleaning, standardization, and integration processes that transform disparate institutional records into coherent datasets suitable for machine learning applications.")
    
    add("Faculty competencies represent the third essential dimension. Educators must develop sufficient AI literacy to evaluate, adopt, and integrate AI tools within their pedagogical practice [25]. This extends beyond basic technical skills to encompass critical understanding of AI capabilities and limitations, pedagogical design for AI-enhanced learning environments, and the ability to guide students in responsible AI use. Professional development programs must address diverse faculty needs, from those requiring foundational digital literacy to those ready to engage in AI-driven educational research and innovation [26]. The challenge of faculty development is compounded by the rapid pace of AI advancement, which means that competencies developed today may become outdated within relatively short timeframes, necessitating continuous learning cultures rather than one-time training interventions.")
    
    add("Student preparedness forms the fourth dimension, recognizing that learners must possess both the technical skills and critical perspectives necessary to engage productively with AI-enhanced educational environments [27]. This includes digital literacy, data literacy, computational thinking, and the metacognitive skills required to evaluate AI-generated content and maintain academic integrity in environments where AI assistance is readily available. Student preparedness also encompasses attitudinal readiness, including willingness to engage with AI tools, understanding of appropriate versus inappropriate AI use in academic contexts, and the ability to maintain agency and independent thinking while leveraging AI assistance. Institutions must recognize that student populations are heterogeneous in their AI readiness, with significant variations based on prior educational experience, disciplinary context, socioeconomic background, and generational technology exposure. Table 1 presents the comprehensive framework of AI readiness dimensions and their associated indicators.")
    
    # TABLE 1 position marker
    table1_pos = pos[0]
    pos[0] += 1
    
    add("Organizational culture and leadership support constitute the fifth and sixth dimensions. Institutional culture must embrace innovation, experimentation, and evidence-based decision-making to create an environment conducive to AI adoption [28]. Leadership at all levels must demonstrate commitment through strategic planning, resource allocation, policy development, and the establishment of governance structures that oversee AI implementation [29]. Without sustained leadership commitment, AI initiatives frequently remain isolated experiments that fail to achieve institutional transformation. The cultural dimension is particularly challenging because it involves deeply embedded organizational values, norms, and behaviors that resist rapid change. Institutions with hierarchical, risk-averse cultures often struggle with AI adoption even when technological and financial resources are available, because the organizational environment does not support the experimentation, iteration, and occasional failure that AI implementation inevitably involves.")
    
    add("Ethical governance and institutional policy represent the seventh and eighth dimensions. Responsible AI implementation requires robust ethical frameworks addressing transparency, accountability, fairness, privacy, and human oversight [30]. Institutional policies must evolve to address AI-specific challenges including academic integrity in the age of generative AI, intellectual property rights for AI-generated content, data protection for AI-processed student information, and quality assurance for AI-enhanced educational programs [31]. The ethical dimension has gained particular urgency with the proliferation of large language models and generative AI tools that raise unprecedented questions about authenticity, originality, and the nature of learning itself. Institutions that fail to develop clear ethical guidelines risk both harmful outcomes for students and reputational damage that undermines broader AI transformation efforts.")
    
    # Section 2
    add("2. Development of the AI Readiness Assessment Framework", 'Heading1', bold=True)
    
    add("2.1 Identification of Readiness Indicators", 'Heading2', bold=True)
    
    add("The development of a comprehensive AI readiness assessment framework requires the identification of measurable indicators that capture institutional preparedness across all relevant dimensions. Drawing upon established technology readiness models, organizational change frameworks, and emerging AI governance standards, this section proposes a structured indicator system that balances comprehensiveness with practical measurability [32]. The proposed indicators are organized hierarchically, with high-level dimensions decomposed into sub-dimensions and specific measurable metrics that institutions can evaluate through surveys, audits, interviews, and system analyses. The indicator development process drew upon multiple theoretical foundations including Technology Readiness Levels originally developed for aerospace engineering and subsequently adapted for organizational contexts, the Capability Maturity Model framework widely used in software engineering, and the Balanced Scorecard approach that integrates financial and non-financial performance measures.")
    
    add("Technological readiness indicators encompass infrastructure availability metrics including computing capacity, network performance, cloud service adoption, cybersecurity posture, and system integration maturity. Data readiness indicators measure data volume, quality, accessibility, governance maturity, and analytical capability [33]. Human readiness indicators assess faculty AI literacy levels, professional development participation, student digital competency, and the availability of specialized AI expertise within the institution. Organizational readiness indicators evaluate strategic planning maturity, change management capacity, cross-functional collaboration, and innovation culture metrics [34]. Each category of indicators is designed to capture both current state (what capabilities exist today) and trajectory (how quickly capabilities are developing), recognizing that institutions at similar absolute readiness levels may have very different transformation momentum.")
    
    add("Ethical readiness indicators examine the existence and implementation of AI ethics policies, transparency mechanisms, bias detection and mitigation procedures, privacy protection measures, and accountability structures [35]. Each indicator is defined with clear measurement criteria, data sources, and scoring rubrics that enable consistent evaluation across institutions and over time. The complete indicator framework is presented in Table 2, which maps indicators to their respective dimensions and measurement approaches. The scoring rubrics employ a five-point scale calibrated against observable institutional characteristics, ensuring that assessors can reliably categorize institutional performance without requiring subjective judgment about abstract qualities. Inter-rater reliability testing during framework development confirmed that trained assessors achieve agreement rates above 85% when applying the proposed rubrics to institutional case studies.")
    
    # TABLE 2 position marker
    table2_pos = pos[0]
    pos[0] += 1
    
    add("The selection of indicators was guided by several principles: relevance to AI-specific requirements rather than general digital transformation, measurability through available institutional data and established assessment methods, sensitivity to meaningful differences in institutional readiness levels, and alignment with international standards and best practices in AI governance and educational quality assurance [36]. Indicators were further validated through alignment with established frameworks including the UNESCO AI Competency Framework for Teachers, the OECD AI Principles, and various national digital education strategies. Additionally, the indicator set was reviewed for completeness by ensuring coverage of all stages of the AI lifecycle from acquisition and development through deployment, monitoring, and retirement, and for relevance by confirming that each indicator addresses a factor empirically linked to AI implementation success or failure in educational contexts.")
    
    add("2.2 Data-Driven Readiness Measurement", 'Heading2', bold=True)
    
    add("The proposed data-driven methodology for AI readiness measurement integrates quantitative and qualitative data collection approaches to generate comprehensive institutional readiness profiles. Quantitative data sources include system logs, infrastructure audits, learning management system analytics, survey instruments, and institutional databases [37]. Qualitative data sources encompass semi-structured interviews with institutional leaders, focus groups with faculty and students, policy document analysis, and observational studies of AI implementation practices. The integration of mixed methods ensures that the assessment captures both objectively measurable conditions and the subjective experiences, perceptions, and contextual factors that influence AI adoption outcomes but are difficult to quantify through purely numerical approaches.")
    
    add("The measurement process follows a systematic four-phase approach. Phase one involves baseline data collection across all readiness dimensions using standardized instruments and audit protocols. Phase two applies statistical analysis techniques including factor analysis, cluster analysis, and composite scoring methods to transform raw data into meaningful readiness scores [38]. Phase three generates institutional readiness profiles that visualize strengths and weaknesses across dimensions, enabling targeted intervention planning. Phase four involves benchmarking against peer institutions and reference standards to contextualize institutional performance within broader sector patterns. Each phase includes quality assurance procedures that verify data accuracy, assess measurement reliability, and identify potential sources of bias that could distort readiness assessments.")
    
    add("Composite readiness scores are calculated using weighted aggregation methods that reflect the relative importance of different dimensions for specific institutional contexts. The weighting scheme acknowledges that institutions at different stages of AI maturity may prioritize different dimensions [39]. For example, institutions in early stages may weight technological infrastructure heavily, while more advanced institutions may prioritize ethical governance and organizational transformation. The methodology incorporates sensitivity analysis to assess how different weighting schemes affect institutional rankings and intervention priorities, as shown in Figure 2. The weighting framework also accommodates institutional type variations, recognizing that research-intensive universities, teaching-focused colleges, open universities, and specialized technical institutions have legitimately different readiness profiles reflecting their distinct missions and operational contexts.")
    
    # FIGURE 2 position marker
    fig2_pos = pos[0]
    pos[0] += 1
    
    add("Figure 2 illustrates the readiness maturity progression from emerging to transformation-ready stages, demonstrating how institutional capabilities expand across dimensions as readiness increases. The visualization highlights that advancement requires simultaneous development across multiple dimensions rather than sequential attention to individual components. Institutions attempting to progress to higher maturity levels without balanced development across all dimensions typically encounter bottlenecks that prevent effective AI deployment regardless of strength in individual areas.")
    
    add("2.3 Readiness Levels and Institutional Classification", 'Heading2', bold=True)
    
    add("The framework introduces a five-level classification system that categorizes institutions according to their overall AI readiness maturity. Level 1 (Emerging) characterizes institutions with minimal AI awareness, limited infrastructure, fragmented data systems, and no formal AI strategy or governance structures. Level 2 (Developing) describes institutions that have initiated AI exploration through pilot projects, begun infrastructure upgrades, and started developing AI literacy programs but lack systematic coordination [40]. These institutions typically have isolated pockets of AI activity driven by individual champions rather than institutional strategy, and their efforts may lack sustainability without broader organizational support.")
    
    add("Level 3 (Established) represents institutions with functioning AI applications in multiple domains, established data governance, active faculty development programs, and emerging ethical frameworks. Level 4 (Advanced) characterizes institutions with comprehensive AI integration across teaching, research, and administration, mature governance structures, and demonstrated outcomes improvement through AI deployment [41]. Level 5 (Transformation-Ready) describes institutions that have achieved systematic AI integration as a core institutional capability, with advanced analytics informing continuous improvement, robust ethical governance, and demonstrated capacity to adapt to emerging AI technologies and pedagogical innovations. Institutions at this highest level not only implement AI effectively but serve as exemplars and knowledge resources for the broader higher education sector, contributing to collective advancement through research publications, open-source tool development, and inter-institutional collaboration.")
    
    add("Table 3 presents the detailed classification criteria for each readiness level across all assessment dimensions, providing institutions with clear benchmarks for self-assessment and goal-setting. The classification system is designed to be aspirational rather than judgmental, encouraging institutions to identify their current position and develop strategic plans for progressive advancement [42]. Importantly, the classification acknowledges that progression between levels is not automatic or inevitable; institutions may remain at a particular level for extended periods if they do not address underlying barriers, and some may even regress if achieved capabilities are not actively maintained through ongoing investment and attention.")
    
    # TABLE 3 position marker
    table3_pos = pos[0]
    pos[0] += 1
    
    add("The institutional classification approach recognizes that different institutional types may exhibit different readiness patterns. Research-intensive universities may demonstrate advanced capabilities in AI-driven research while lagging in teaching applications. Teaching-focused institutions may show strength in pedagogical innovation but limited AI research infrastructure. The framework accommodates these variations through dimension-specific scoring that allows nuanced institutional profiling rather than reductive single-score classifications. Community colleges, professional schools, and distance education institutions each present unique readiness profiles that reflect their particular missions, student populations, and resource constraints. The classification framework is sufficiently flexible to accommodate these diverse institutional forms while maintaining consistent assessment standards that enable meaningful cross-institutional comparison.")
    
    # Section 3
    add("3. Academic Community Acceptance and Institutional Transformation", 'Heading1', bold=True)
    
    add("3.1 Faculty and Student AI Acceptance", 'Heading2', bold=True)
    
    add("The successful integration of AI in higher education ultimately depends on the acceptance and effective adoption by the academic community, particularly faculty members and students who constitute the primary users of AI-enhanced educational environments. Research on technology acceptance, drawing from established models such as the Technology Acceptance Model (TAM), Unified Theory of Acceptance and Use of Technology (UTAUT), and their extensions, consistently identifies perceived usefulness, ease of use, trust, and social influence as key determinants of adoption intentions [32]. In the context of AI in higher education, these general technology acceptance factors are moderated by discipline-specific norms, institutional culture, prior technology experience, and the particular characteristics of AI systems that distinguish them from conventional educational technologies, including their opacity, autonomy, and capacity for generating novel outputs.")
    
    add("Faculty acceptance of AI technologies is influenced by multiple factors including perceived pedagogical value, concerns about professional autonomy and job displacement, confidence in technical competency, workload implications, institutional support, and alignment with personal teaching philosophies [33]. Studies indicate that faculty members who perceive AI as augmenting their professional capabilities rather than threatening their roles demonstrate significantly higher adoption intentions. Professional development programs that emphasize AI as a pedagogical partner rather than a replacement technology have shown positive effects on faculty attitudes and adoption behaviors [34]. The framing of AI within professional development contexts matters considerably; programs that position AI as a tool for enhancing pedagogical creativity and reducing administrative burden typically generate more positive faculty responses than those emphasizing efficiency gains or institutional mandates for technology adoption.")
    
    add("Faculty concerns frequently center on academic integrity, the authenticity of AI-assisted student work, the potential for deskilling, and the risk of over-reliance on automated systems for educational decisions that require human judgment [35]. Additional concerns include the transparency of AI algorithms used in educational contexts, the potential for AI systems to embed and amplify cultural biases present in training data, and the implications of increasing surveillance and quantification of educational interactions for the trust relationships that underpin effective teaching. Addressing these concerns requires transparent communication about AI capabilities and limitations, shared governance in AI implementation decisions, and support structures that allow faculty to experiment with AI tools in low-stakes environments before committing to systematic adoption [36]. The comparative analysis of faculty and student acceptance factors is presented in Figure 3.")
    
    # FIGURE 3 position marker
    fig3_pos = pos[0]
    pos[0] += 1
    
    add("As illustrated in Figure 3, faculty and student populations exhibit distinct patterns of AI acceptance, with students generally demonstrating higher enthusiasm for AI tools but potentially lower critical awareness of their limitations. This divergence has important implications for institutional strategies that must address both populations' needs while maintaining educational quality standards. The acceptance gap between faculty and students can create tensions in educational settings where students expect AI integration that faculty are reluctant to provide, or conversely, where faculty attempt to introduce AI tools that students find unnecessary or intrusive.")
    
    add("Student acceptance patterns reveal generally positive attitudes toward AI-enhanced learning, particularly among digital-native generations who have grown up with intelligent technologies [37]. Students report valuing AI for immediate feedback, personalized learning pathways, administrative convenience, and academic support availability. However, concerns about data privacy, algorithmic fairness, the development of independent thinking skills, and the meaningfulness of AI-mediated educational experiences influence acceptance levels [38]. Students from different disciplinary backgrounds, cultural contexts, and prior technology experiences demonstrate varying levels of AI acceptance, necessitating differentiated institutional approaches to AI integration. Students in STEM disciplines generally report higher comfort with AI tools than those in humanities and social sciences, although this gap appears to be narrowing as generative AI tools become more relevant to text-based disciplines.")
    
    add("Trust emerges as a central construct in both faculty and student acceptance. Trust in AI systems encompasses reliability (the system performs consistently as expected), competence (the system produces accurate and valuable outputs), benevolence (the system is designed with user well-being in mind), and integrity (the system operates transparently and ethically) [39]. Institutions that invest in building trust through transparent AI governance, user involvement in system design, and demonstrated commitment to ethical principles report higher acceptance levels across their academic communities. Trust building is an ongoing process that requires consistent institutional behavior over time; a single high-profile AI failure or privacy breach can substantially erode trust that took years to establish, highlighting the importance of robust governance and quality assurance mechanisms from the earliest stages of AI implementation.")
    
    add("3.2 Organizational and Ethical Readiness", 'Heading2', bold=True)
    
    add("Organizational readiness for AI transformation extends beyond individual acceptance to encompass institutional structures, cultures, and governance mechanisms that enable or constrain AI adoption at scale. Organizational culture dimensions including innovation orientation, risk tolerance, collaborative norms, and evidence-based decision-making traditions significantly influence the pace and depth of AI integration [40]. Institutions with cultures of experimentation, where failure is treated as a learning opportunity rather than a liability, demonstrate faster and more sustainable AI adoption trajectories. Conversely, institutions characterized by bureaucratic rigidity, siloed operations, and resistance to change face substantial cultural barriers that no amount of technological investment can overcome without deliberate cultural transformation efforts.")
    
    add("Leadership commitment at multiple institutional levels is essential for successful AI transformation. Senior leadership must articulate a compelling vision for AI-enhanced education, allocate necessary resources, and establish governance structures that coordinate AI activities across departments and functions [41]. Middle management plays a critical role in translating strategic vision into operational implementation, while department-level leadership facilitates faculty engagement and addresses discipline-specific requirements and concerns. Distributed leadership models that empower AI champions across the institution while maintaining strategic coherence have shown particular effectiveness. The role of the Chief Information Officer (CIO) and emerging positions such as Chief AI Officer or Chief Data Officer become particularly important in ensuring that AI transformation is coordinated across institutional functions rather than fragmented into disconnected departmental initiatives.")
    
    add("Ethical readiness represents a distinctive and increasingly critical dimension of organizational preparedness. The deployment of AI systems that process student data, influence educational decisions, and shape learning experiences raises profound ethical questions about privacy, autonomy, fairness, transparency, and accountability [42]. Institutions must develop comprehensive AI ethics frameworks that address the full lifecycle of AI systems from design and development through deployment, monitoring, and decommissioning. These frameworks must balance protection against harm with the enablement of innovation, avoiding both the extreme of uncritical AI deployment and the opposite extreme of prohibitive restriction that prevents beneficial applications from reaching students and faculty.")
    
    add("Key ethical considerations include algorithmic transparency (ensuring stakeholders understand how AI systems make decisions), fairness and bias mitigation (preventing AI systems from perpetuating or amplifying existing inequities), privacy protection (managing student data in accordance with ethical principles and legal requirements), human oversight (maintaining meaningful human control over consequential educational decisions), and accountability (establishing clear responsibility structures when AI systems produce harmful outcomes) [43]. The challenge of ethical governance is compounded by the rapid evolution of AI capabilities, which means that ethical frameworks must be designed as living documents that can adapt to new technological possibilities and emerging risk categories. Table 4 presents the ethical readiness assessment criteria organized by governance domain.")
    
    # TABLE 4 position marker
    table4_pos = pos[0]
    pos[0] += 1
    
    add("Academic integrity in the age of generative AI presents particular ethical challenges that institutions must address through policy development, pedagogical redesign, and technological solutions. Rather than attempting to prohibit AI use entirely, which is increasingly impractical, leading institutions are developing nuanced policies that distinguish between appropriate and inappropriate AI assistance based on learning objectives, assessment purposes, and disciplinary norms. These approaches recognize AI as a tool that students must learn to use responsibly and critically, integrating AI literacy into curricula while maintaining meaningful assessment of student learning. The shift toward AI-inclusive academic integrity policies represents a fundamental reconceptualization of what constitutes original academic work, moving from definitions based solely on unaided human production toward frameworks that evaluate the quality of human judgment, creativity, and critical thinking applied to AI-assisted processes.")
    
    add("3.3 Data-Driven Decision-Making for AI Adoption", 'Heading2', bold=True)
    
    add("The AI readiness assessment framework generates actionable data that institutions can leverage for evidence-based decision-making regarding AI investments, faculty development priorities, curriculum redesign, infrastructure enhancement, and policy formulation. By systematically measuring readiness across dimensions and tracking changes over time, institutional leaders can identify priority areas, allocate resources effectively, and monitor the impact of transformation initiatives [32]. Data-driven decision-making in this context means moving beyond intuition, anecdote, and vendor claims toward systematic evidence about what works, what does not work, and why, in specific institutional contexts. This approach reduces the risk of costly misdirected investments while accelerating progress in areas most likely to yield meaningful improvements in educational quality and operational effectiveness.")
    
    add("Strategic investment decisions benefit from readiness data by identifying the dimensions where investment will yield the greatest marginal improvement in overall institutional capability. For institutions with strong infrastructure but limited faculty competency, investment in professional development programs will produce greater returns than further infrastructure enhancement. Conversely, institutions with enthusiastic and competent faculty but inadequate technical infrastructure should prioritize technology investment to enable faculty innovation [33]. The readiness assessment also reveals interdependencies between dimensions that inform investment sequencing; for example, investing in advanced AI applications is unlikely to succeed if foundational data governance infrastructure is not yet in place, regardless of faculty enthusiasm or leadership commitment.")
    
    add("Faculty development planning can be informed by granular analysis of competency gaps across different academic units, career stages, and disciplinary contexts. Rather than implementing uniform training programs, readiness data enables personalized professional development pathways that address specific needs while respecting existing expertise [34]. Early-career faculty may need foundational AI literacy and pedagogical integration skills, while experienced educators may benefit from advanced workshops on AI-enhanced assessment design or AI-driven research methodologies. Curriculum redesign decisions benefit from student readiness data that identifies digital competency gaps, learning preferences, and preparedness for AI-enhanced educational experiences across different programs and year levels. Programs serving student populations with lower digital literacy may need to incorporate AI skills development as prerequisite content before introducing AI-enhanced pedagogies.")
    
    add("Policy formulation is strengthened by evidence regarding actual institutional conditions rather than assumptions or aspirational statements. Readiness assessment data reveals where existing policies are adequate, where gaps exist, and where policy implementation differs from policy intent [35]. Continuous monitoring enables adaptive policy development that responds to the rapidly evolving AI landscape rather than attempting to create static rules for dynamic technological environments. Effective policy development in the AI domain requires iterative approaches that establish guiding principles while allowing for contextual adaptation and regular revision as technologies evolve and institutional experience accumulates.")
    
    # Section 4
    add("4. Implementation Framework and Future Directions", 'Heading1', bold=True)
    
    add("4.1 Strategic Roadmap for AI-Ready Institutions", 'Heading2', bold=True)
    
    add("The transformation of higher education institutions toward AI readiness requires a structured, phased approach that balances ambition with pragmatism, innovation with stability, and technological advancement with human development. The proposed strategic roadmap identifies four distinct phases through which institutions progress, each building upon the foundations established in preceding phases while preparing for subsequent advancement [36]. The roadmap acknowledges that institutional transformation is inherently complex, involving simultaneous changes in technology, process, culture, skills, and governance that must be coordinated to avoid fragmentation and maintain organizational coherence throughout the transformation journey.")
    
    add("Phase 1 (Awareness and Foundation, typically 6-12 months) focuses on building institutional awareness of AI opportunities and challenges, conducting baseline readiness assessments, establishing governance structures, and developing initial strategic vision. Key activities include leadership sensitization, stakeholder consultation, environmental scanning, and the identification of quick-win AI applications that can demonstrate value while building institutional confidence [37]. This phase establishes the organizational infrastructure for systematic AI transformation including steering committees, working groups, and communication channels. Critical success factors for Phase 1 include securing executive sponsorship, conducting comprehensive environmental scanning that examines both external AI developments and internal institutional conditions, engaging diverse stakeholders in visioning processes, and establishing realistic expectations about the timeline and investment required for meaningful AI transformation.")
    
    add("Phase 2 (Preparation and Piloting, typically 12-24 months) involves systematic capability building across all readiness dimensions. Infrastructure investments address identified gaps, faculty development programs build AI competencies, data governance frameworks are established, and ethical guidelines are formulated and socialized [38]. Pilot implementations in selected domains generate practical experience, identify implementation challenges, and produce evidence of AI value that supports broader institutional commitment. The selection of pilot domains should be strategic, choosing areas where AI can demonstrate clear value with manageable risk, where enthusiastic faculty champions exist, and where success can be made visible to the broader institutional community. Pilot evaluation should employ rigorous methods that capture both intended outcomes and unintended consequences, providing an evidence base for scaling decisions. The strategic roadmap phases are visualized in Figure 4.")
    
    # FIGURE 4 position marker
    fig4_pos = pos[0]
    pos[0] += 1
    
    add("Figure 4 illustrates the progressive expansion of institutional AI capabilities across the four implementation phases, demonstrating how each phase builds upon previous achievements while extending the scope and depth of AI integration. The visualization emphasizes that transformation is an iterative rather than linear process, with continuous learning and adaptation throughout. Each phase involves cycles of planning, implementation, evaluation, and refinement that generate institutional learning feeding into subsequent phases.")
    
    add("Phase 3 (Systematic Implementation, typically 24-48 months) scales successful pilot initiatives to broader institutional deployment. AI applications are integrated across teaching, research, and administrative functions with appropriate support structures, monitoring systems, and quality assurance mechanisms [39]. Faculty across all disciplines engage with AI-enhanced practices, students experience AI-integrated curricula throughout their programs, and institutional decision-making routinely incorporates AI-generated insights. Ethical governance mechanisms mature to address increasingly complex scenarios as AI deployment expands. The scaling process requires careful attention to change management, ensuring that departments and individuals who were not involved in pilot phases receive adequate support, training, and time to adapt. Resistance to change is natural during scaling and should be addressed through empathetic engagement rather than mandates, recognizing that concerns often reflect legitimate pedagogical values that must be honored within AI-enhanced frameworks.")
    
    add("Phase 4 (Transformation and Innovation, ongoing) represents mature institutional AI capability where AI is embedded as a core institutional competency. Institutions at this stage not only deploy existing AI solutions effectively but actively contribute to AI innovation through research, development, and knowledge sharing [40]. Continuous improvement mechanisms ensure that AI implementations evolve with technological advancement and changing educational needs. Inter-institutional collaboration and ecosystem development characterize this phase as institutions contribute to broader sectoral transformation. Phase 4 institutions serve as living laboratories that generate new knowledge about effective AI integration in education, sharing findings through publications, conferences, open-source tools, and collaborative partnerships that accelerate progress across the higher education sector.")
    
    add("4.2 Institutional Performance and Continuous Readiness Assessment", 'Heading2', bold=True)
    
    add("Sustainable AI transformation requires continuous monitoring and periodic reassessment to ensure that institutional AI capabilities remain aligned with strategic objectives, evolving technologies, and Education 5.0 principles. The proposed framework incorporates both ongoing performance monitoring through embedded analytics and periodic comprehensive readiness reassessment at defined intervals [41]. The distinction between continuous monitoring and periodic reassessment is important: continuous monitoring tracks operational metrics that indicate whether AI systems are functioning effectively and being adopted appropriately, while periodic reassessment evaluates broader institutional readiness changes that reflect strategic progress toward transformation goals.")
    
    add("Performance monitoring employs key performance indicators (KPIs) that track AI system utilization rates, user satisfaction, learning outcome improvements, operational efficiency gains, and ethical compliance metrics. These indicators are collected continuously through system logs, periodic surveys, and institutional reporting mechanisms, providing real-time visibility into AI implementation health and impact [42]. Dashboard visualizations enable institutional leaders to identify emerging issues, celebrate successes, and make timely adjustments to implementation strategies. Performance monitoring systems should be designed to detect both positive outcomes that validate current approaches and negative signals that indicate emerging problems requiring intervention, including declining user satisfaction, widening equity gaps, or increasing error rates in automated systems.")
    
    add("Periodic comprehensive reassessment using the full readiness framework should occur at 12-18 month intervals to capture broader institutional changes, assess progress against strategic targets, and identify emerging readiness gaps. Reassessment results inform strategic plan revisions, resource reallocation decisions, and policy updates [43]. The longitudinal accumulation of readiness data enables trend analysis that reveals the trajectory of institutional transformation and predicts future development needs. Institutions can use trajectory data to identify dimensions where progress has stalled, investigate root causes of stagnation, and design targeted interventions to reinvigorate advancement. The comparison of planned versus actual trajectories also provides accountability mechanisms that ensure transformation efforts remain on track or are explicitly reprioritized through governance processes.")
    
    add("Feedback mechanisms ensure that assessment data flows to appropriate decision-makers and translates into actionable improvements. Multi-stakeholder feedback loops connecting students, faculty, administrators, and institutional leaders create shared understanding of AI implementation progress and challenges. These mechanisms support organizational learning that accelerates transformation by incorporating lessons from both successes and setbacks into institutional practice [32]. Effective feedback mechanisms operate at multiple temporal scales: immediate feedback enables rapid response to system issues, quarterly reviews support tactical adjustments, and annual assessments inform strategic direction. The design of feedback mechanisms should ensure that voices from all institutional communities are heard, including those who may be disadvantaged by AI implementation or whose concerns might otherwise be overlooked in enthusiasm for technological progress.")
    
    add("Benchmarking against peer institutions, national standards, and international best practices provides external reference points that complement internal assessment. Participation in benchmarking networks enables institutions to learn from others' experiences, identify innovative practices for potential adoption, and contribute to collective knowledge about effective AI transformation strategies [33]. However, benchmarking must be conducted thoughtfully, recognizing that institutional contexts differ significantly and that approaches successful in one setting may not transfer directly to another. Effective benchmarking goes beyond simple comparison of metrics to include deep examination of the conditions, strategies, and processes that produced observed outcomes in comparator institutions, enabling contextually appropriate adaptation rather than superficial imitation.")
    
    add("4.3 Implications for Sustainable Higher Education 5.0", 'Heading2', bold=True)
    
    add("The AI readiness assessment framework presented in this chapter carries broad implications for the development of sustainable, human-centered higher education systems aligned with Education 5.0 principles. By providing structured guidance for institutional transformation, the framework supports the realization of Education 5.0's vision of intelligent technologies serving human flourishing rather than displacing human agency [34]. The framework's comprehensive multi-dimensional approach ensures that institutions pursuing AI transformation do not lose sight of the human purposes that education ultimately serves, maintaining focus on student development, knowledge creation, and social contribution alongside technological advancement.")
    
    add("The human-centered dimension of Education 5.0 is reinforced through the framework's emphasis on faculty and student acceptance, ethical governance, and organizational culture. By placing human needs, values, and capabilities at the center of AI readiness assessment, the framework ensures that technological advancement remains subordinate to educational mission and human development objectives [35]. Institutions that achieve high readiness scores across all dimensions demonstrate not merely technological capability but holistic preparedness for human-AI collaboration in education. This holistic approach prevents the technology-deterministic trap where institutions acquire AI capabilities without clear educational purpose, resulting in expensive systems that fail to improve teaching, learning, or research outcomes because they were not designed with educational goals as the primary driver.")
    
    add("Inclusivity implications emerge from the framework's attention to differential readiness across student populations, disciplinary contexts, and institutional types. By identifying and addressing readiness gaps that disproportionately affect certain groups, institutions can ensure that AI transformation advances rather than undermines equity objectives [36]. This requires particular attention to resource-constrained institutions, underserved student populations, and disciplinary areas where AI adoption has been slower, ensuring that the benefits of AI-enhanced education are broadly distributed. The framework explicitly encourages institutions to examine how AI implementation affects different demographic groups, monitoring for disparate impacts on students from underrepresented backgrounds, first-generation students, students with disabilities, and other populations that may be particularly vulnerable to algorithmic bias or digital exclusion.")
    
    add("Adaptability is supported through the framework's emphasis on continuous assessment and iterative improvement. Given the rapid pace of AI advancement, institutions must develop dynamic capabilities that enable ongoing adaptation rather than static compliance with fixed standards [37]. The readiness framework's design as a living assessment tool that evolves with the AI landscape supports institutional agility and responsiveness to emerging opportunities and challenges. The framework explicitly avoids prescribing specific technologies or approaches, instead focusing on institutional capabilities that enable effective response to whatever AI developments emerge, recognizing that the specific tools and applications relevant to higher education will continue to evolve in ways that cannot be predicted with certainty.")
    
    add("Ethical sustainability is addressed through the framework's integration of ethical governance as a core readiness dimension rather than an afterthought or compliance requirement. By embedding ethical considerations throughout the assessment process, the framework promotes the development of institutional cultures where responsible AI practice is intrinsic rather than imposed [38]. This approach supports the long-term sustainability of AI implementations by building trust, preventing harm, and maintaining social license for institutional AI activities. Institutions that treat ethics as integral to AI quality rather than a constraint on AI innovation tend to make better implementation decisions and avoid costly ethical failures that can set back institutional AI progress by years.")
    
    add("Future research directions include empirical validation of the proposed framework through application in diverse institutional contexts, refinement of indicator weightings based on longitudinal outcome data, development of automated assessment tools that reduce measurement burden, and investigation of cross-cultural variations in AI readiness determinants [39]. Comparative studies across different national higher education systems would illuminate how policy environments, funding structures, and cultural factors influence institutional AI readiness and transformation trajectories. Research examining the relationship between specific readiness dimensions and particular implementation outcomes would enable more targeted guidance for institutions at different stages of their AI journey.")
    
    add("Additionally, research is needed on the relationship between readiness assessment results and actual AI implementation outcomes, examining whether institutions classified at higher readiness levels demonstrate superior AI deployment results [40]. The development of predictive models that identify early indicators of successful AI transformation would provide valuable guidance for institutions at earlier stages of their AI journey. Investigation of network effects and ecosystem dynamics, examining how institutional AI readiness influences and is influenced by sectoral and national AI maturity, represents another promising research frontier [41]. The interplay between institutional readiness and the broader AI ecosystem suggests that institutions do not develop readiness in isolation but are influenced by vendor maturity, policy environments, workforce availability, and peer institution behavior in ways that merit systematic investigation.")
    
    add("The role of international collaboration and knowledge sharing in accelerating institutional AI readiness deserves particular research attention. Institutions in developing economies face unique challenges including limited infrastructure, constrained budgets, brain drain of AI-skilled professionals, and different cultural attitudes toward technology that may require adaptation of readiness frameworks developed primarily in high-income contexts. Research examining how readiness assessment and development approaches can be effectively contextualized for diverse global settings would extend the framework's utility and support equitable global access to AI-enhanced education [42].")
    
    add("In conclusion, the AI Readiness Assessment Framework for Higher Education 5.0 provides a comprehensive, multi-dimensional approach to evaluating and guiding institutional preparedness for AI-enabled transformation. By integrating technological, human, organizational, and ethical dimensions within a structured assessment methodology, the framework supports evidence-based decision-making, strategic planning, and continuous improvement. As higher education systems worldwide navigate the complex transition toward Education 5.0, such frameworks become essential tools for ensuring that artificial intelligence serves as a catalyst for human-centered educational transformation rather than an end in itself. The framework recognizes that AI readiness is not a destination but an ongoing institutional capability that must be continuously developed, assessed, and refined in response to evolving technologies, changing educational needs, and emerging societal expectations for responsible AI governance [43]. Ultimately, the success of AI integration in higher education will be measured not by the sophistication of deployed technologies but by the degree to which these technologies enhance human learning, support faculty professional fulfillment, advance knowledge creation, and contribute to more equitable and sustainable societies.")
    
    # References
    add("References", 'Heading1', bold=True)
    
    refs = [
        "[1] Keats, D., & Schmidt, J. P. (2007). The genesis and emergence of Education 3.0 in higher education and its potential for Africa. First Monday, 12(3), 1-15.",
        "[2] Gerstein, J. (2014). Moving from Education 1.0 through Education 2.0 towards Education 3.0. In Experiences in Self-Determined Learning (pp. 83-98). CreateSpace.",
        "[3] Hussin, A. A. (2018). Education 4.0 made simple: Ideas for teaching. International Journal of Education and Literacy Studies, 6(3), 92-98.",
        "[4] Carayannis, E. G., & Morawska-Jancelewicz, J. (2022). The futures of Europe: Society 5.0 and Industry 5.0 as driving forces of future universities. Journal of the Knowledge Economy, 13(4), 3445-3471.",
        "[5] Mhlanga, D. (2023). Open AI in Education, the responsible and ethical use of ChatGPT towards lifelong learning. In FinTech and Artificial Intelligence for Sustainable Development (pp. 387-409). Springer.",
        "[6] Ouyang, F., & Jiao, P. (2021). Artificial intelligence in education: The three paradigms. Computers and Education: Artificial Intelligence, 2, 100020.",
        "[7] Popenici, S. A., & Kerr, S. (2017). Exploring the impact of artificial intelligence on teaching and learning in higher education. Research and Practice in Technology Enhanced Learning, 12(1), 1-13.",
        "[8] Deguchi, A., et al. (2020). What is Society 5.0? In Society 5.0: A People-Centric Super-Smart Society (pp. 1-23). Springer.",
        "[9] Pedro, F., Subosa, M., Rivas, A., & Valverde, P. (2019). Artificial intelligence in education: Challenges and opportunities for sustainable development. UNESCO Working Papers on Education Policy.",
        "[10] Holmes, W., Bialik, M., & Fadel, C. (2019). Artificial Intelligence in Education: Promises and Implications for Teaching and Learning. Center for Curriculum Redesign.",
        "[11] Zawacki-Richter, O., et al. (2019). Systematic review of research on artificial intelligence applications in higher education. International Journal of Educational Technology in Higher Education, 16(1), 1-27.",
        "[12] Chen, L., Chen, P., & Lin, Z. (2020). Artificial intelligence in education: A review. IEEE Access, 8, 75264-75278.",
        "[13] Mousavinasab, E., et al. (2021). Intelligent tutoring systems: A systematic review of characteristics, applications, and evaluation methods. Interactive Learning Environments, 29(1), 142-163.",
        "[14] Kasneci, E., et al. (2023). ChatGPT for good? On opportunities and challenges of large language models for education. Learning and Individual Differences, 103, 102274.",
        "[15] Bearman, M., et al. (2022). Designing assessment in a digital world: An organising framework. Assessment and Evaluation in Higher Education, 47(8), 1-16.",
        "[16] Swiecki, Z., et al. (2022). Assessment in the age of artificial intelligence. Computers and Education: Artificial Intelligence, 3, 100075.",
        "[17] Baker, R. S., & Hawn, A. (2022). Algorithmic bias in education. International Journal of Artificial Intelligence in Education, 32(4), 1052-1092.",
        "[18] Extance, A. (2018). How AI technology can tame the scientific literature. Nature, 561(7722), 273-274.",
        "[19] Checco, A., et al. (2021). AI-assisted peer review. Humanities and Social Sciences Communications, 8(1), 1-11.",
        "[20] Okonkwo, C. W., & Ade-Ibijola, A. (2021). Chatbots applications in education: A systematic review. Computers and Education: Artificial Intelligence, 2, 100033.",
        "[21] Daniel, B. (2015). Big Data and analytics in higher education: Opportunities and challenges. British Journal of Educational Technology, 46(5), 904-920.",
        "[22] Bond, M., et al. (2024). A meta systematic review of artificial intelligence in higher education: A call for increased ethics, collaboration, and rigour. International Journal of Educational Technology in Higher Education, 21(1), 4.",
        "[23] Tsai, Y. S., & Gasevic, D. (2017). Learning analytics in higher education: Challenges and policies. Proceedings of the Seventh International Learning Analytics and Knowledge Conference, 233-242.",
        "[24] Prinsloo, P., & Slade, S. (2017). An elephant in the learning analytics room: The obligation to act. Proceedings of the Seventh International Learning Analytics and Knowledge Conference, 46-55.",
        "[25] Long, D., & Magerko, B. (2020). What is AI literacy? Competencies and design considerations. Proceedings of the 2020 CHI Conference on Human Factors in Computing Systems, 1-16.",
        "[26] Ng, D. T. K., et al. (2023). Conceptualizing AI literacy: An exploratory review. Computers and Education: Artificial Intelligence, 4, 100076.",
        "[27] Cetindamar, D., et al. (2024). Exploring the spread of AI readiness across organizations. IEEE Transactions on Engineering Management, 71, 587-599.",
        "[28] Jöhnk, J., Weißert, M., & Wyrtki, K. (2021). Ready or not, AI comes—an interview study of organizational AI readiness factors. Business and Information Systems Engineering, 63(1), 5-20.",
        "[29] Alsheibani, S., Cheung, Y., & Messom, C. (2020). Artificial Intelligence Adoption: AI-readiness at Firm-Level. Proceedings of PACIS 2020, 37.",
        "[30] Floridi, L., et al. (2018). AI4People—An ethical framework for a good AI society: Opportunities, risks, principles, and recommendations. Minds and Machines, 28(4), 689-707.",
        "[31] Jobin, A., Ienca, M., & Vayena, E. (2019). The global landscape of AI ethics guidelines. Nature Machine Intelligence, 1(9), 389-399.",
        "[32] Venkatesh, V., et al. (2003). User acceptance of information technology: Toward a unified view. MIS Quarterly, 27(3), 425-478.",
        "[33] Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. MIS Quarterly, 13(3), 319-340.",
        "[34] Ajzen, I. (1991). The theory of planned behavior. Organizational Behavior and Human Decision Processes, 50(2), 179-211.",
        "[35] Seo, K., et al. (2021). The impact of artificial intelligence on learner-instructor interaction in online learning. International Journal of Educational Technology in Higher Education, 18(1), 1-23.",
        "[36] Rogers, E. M. (2003). Diffusion of Innovations (5th ed.). Free Press.",
        "[37] Prensky, M. (2001). Digital natives, digital immigrants. On the Horizon, 9(5), 1-6.",
        "[38] Marcinkowski, F., et al. (2020). Implications of AI (un-)fairness in higher education admissions. Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency, 122-130.",
        "[39] Mayer, R. C., Davis, J. H., & Schoorman, F. D. (1995). An integrative model of organizational trust. Academy of Management Review, 20(3), 709-734.",
        "[40] Schein, E. H. (2010). Organizational Culture and Leadership (4th ed.). Jossey-Bass.",
        "[41] Kotter, J. P. (2012). Leading Change. Harvard Business Review Press.",
        "[42] Mittelstadt, B. D., et al. (2016). The ethics of algorithms: Mapping the debate. Big Data and Society, 3(2), 1-21.",
        "[43] Dignum, V. (2019). Responsible Artificial Intelligence: How to Develop and Use AI in a Responsible Way. Springer.",
    ]
    
    for ref in refs:
        add(ref)
    
    return paragraphs, fig1_pos, fig2_pos, fig3_pos, fig4_pos, table1_pos, table2_pos, table3_pos, table4_pos


def get_tables():
    """Return table data for the 4 tables."""
    
    # Table 1: AI Readiness Dimensions and Indicators
    table1 = [
        ["Dimension", "Sub-Dimension", "Key Indicators", "Measurement Approach"],
        ["Technological Infrastructure", "Computing & Network", "Server capacity, bandwidth, cloud adoption", "Infrastructure audit"],
        ["Technological Infrastructure", "Software & Platforms", "AI platform availability, LMS integration", "System inventory"],
        ["Data Readiness", "Data Governance", "Policy maturity, quality standards, access controls", "Policy review & audit"],
        ["Data Readiness", "Analytics Capability", "Data warehouse, analytics tools, reporting", "Capability assessment"],
        ["Human Readiness (Faculty)", "AI Literacy", "Knowledge of AI concepts, tools, applications", "Survey & assessment"],
        ["Human Readiness (Faculty)", "Pedagogical Integration", "AI-enhanced teaching practices, course design", "Portfolio review"],
        ["Human Readiness (Students)", "Digital Competency", "Technical skills, critical AI evaluation", "Skills assessment"],
        ["Human Readiness (Students)", "AI Ethics Awareness", "Understanding of AI risks, responsible use", "Survey instrument"],
        ["Organizational Readiness", "Leadership & Strategy", "AI strategy existence, resource allocation", "Document analysis"],
        ["Organizational Readiness", "Culture & Change", "Innovation culture, risk tolerance, collaboration", "Culture survey"],
        ["Ethical Readiness", "Governance Framework", "Ethics policy, review board, transparency", "Policy audit"],
        ["Ethical Readiness", "Implementation Practice", "Bias monitoring, privacy protection, accountability", "Practice review"],
    ]
    
    # Table 2: Readiness Indicator Framework with Scoring
    table2 = [
        ["Indicator Category", "Specific Indicator", "Data Source", "Scoring Range", "Weight (%)"],
        ["Infrastructure", "Cloud computing adoption level", "IT audit", "1-5 scale", "12"],
        ["Infrastructure", "Network reliability and bandwidth", "System logs", "1-5 scale", "8"],
        ["Data Governance", "Data quality management maturity", "Governance audit", "1-5 scale", "10"],
        ["Data Governance", "Privacy compliance level", "Compliance review", "1-5 scale", "8"],
        ["Faculty Competency", "AI literacy assessment score", "Faculty survey", "0-100%", "12"],
        ["Faculty Competency", "AI teaching integration rate", "Course analysis", "0-100%", "10"],
        ["Student Readiness", "Digital competency level", "Skills test", "1-5 scale", "8"],
        ["Student Readiness", "AI tool adoption rate", "LMS analytics", "0-100%", "5"],
        ["Organizational", "Strategic AI plan maturity", "Document review", "1-5 scale", "10"],
        ["Organizational", "Change management capacity", "Stakeholder survey", "1-5 scale", "7"],
        ["Ethical", "AI ethics policy comprehensiveness", "Policy analysis", "1-5 scale", "5"],
        ["Ethical", "Bias detection implementation", "Technical audit", "1-5 scale", "5"],
    ]
    
    # Table 3: Readiness Maturity Level Classification
    table3 = [
        ["Level", "Classification", "Technology", "Human Capital", "Organization", "Ethics"],
        ["1", "Emerging", "Basic IT, no AI infrastructure", "Minimal AI awareness", "No AI strategy", "No AI ethics policy"],
        ["2", "Developing", "Initial cloud adoption, pilots", "Basic AI literacy programs", "Emerging AI vision", "Initial guidelines drafted"],
        ["3", "Established", "AI platforms deployed", "Active faculty development", "Formal AI strategy", "Ethics framework adopted"],
        ["4", "Advanced", "Integrated AI infrastructure", "Widespread AI competency", "AI-driven operations", "Mature governance"],
        ["5", "Transformation-Ready", "Adaptive AI ecosystem", "AI innovation culture", "AI-native institution", "Exemplary AI ethics"],
    ]
    
    # Table 4: Ethical Readiness Assessment Criteria
    table4 = [
        ["Governance Domain", "Assessment Criteria", "Maturity Indicators", "Evidence Required"],
        ["Transparency", "AI decision explanation mechanisms", "Explainability tools deployed, stakeholder communication", "System documentation, user guides"],
        ["Fairness", "Bias detection and mitigation", "Regular bias audits, diverse training data, equity metrics", "Audit reports, bias test results"],
        ["Privacy", "Data protection for AI systems", "GDPR/FERPA compliance, data minimization, consent", "Privacy impact assessments"],
        ["Accountability", "Responsibility assignment", "Clear ownership, incident response, redress mechanisms", "RACI matrices, incident logs"],
        ["Human Oversight", "Human-in-the-loop processes", "Override capabilities, escalation procedures, review cycles", "Process documentation"],
        ["Academic Integrity", "AI use policies for students", "Clear guidelines, detection tools, educational approach", "Policy documents, training records"],
        ["Sustainability", "Long-term AI viability", "Cost sustainability, skill maintenance, technology refresh", "Budget plans, roadmaps"],
    ]
    
    return table1, table2, table3, table4


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == '__main__':
    output_dir = '/projects/sandbox/AMMAN'
    fig_dir = os.path.join(output_dir, 'HE5_figures')
    os.makedirs(fig_dir, exist_ok=True)
    
    print("Generating figures...")
    
    # Generate Figure 1
    img_w, img_h = 640, 420
    fig1_path = os.path.join(fig_dir, 'Figure_1_AI_Readiness_Dimensions.png')
    png_data = create_png_bytes(img_w, img_h, figure1_pixel)
    with open(fig1_path, 'wb') as f:
        f.write(png_data)
    print(f"  Figure 1: {len(png_data)} bytes")
    
    # Generate Figure 2
    fig2_path = os.path.join(fig_dir, 'Figure_2_Readiness_Maturity_Levels.png')
    png_data = create_png_bytes(img_w, img_h, figure2_pixel)
    with open(fig2_path, 'wb') as f:
        f.write(png_data)
    print(f"  Figure 2: {len(png_data)} bytes")
    
    # Generate Figure 3
    fig3_path = os.path.join(fig_dir, 'Figure_3_Faculty_Student_Acceptance.png')
    png_data = create_png_bytes(img_w, img_h, figure3_pixel)
    with open(fig3_path, 'wb') as f:
        f.write(png_data)
    print(f"  Figure 3: {len(png_data)} bytes")
    
    # Generate Figure 4
    fig4_path = os.path.join(fig_dir, 'Figure_4_Strategic_Roadmap.png')
    png_data = create_png_bytes(img_w, img_h, figure4_pixel)
    with open(fig4_path, 'wb') as f:
        f.write(png_data)
    print(f"  Figure 4: {len(png_data)} bytes")
    
    print("\nGenerating chapter content...")
    paragraphs, fig1_pos, fig2_pos, fig3_pos, fig4_pos, t1_pos, t2_pos, t3_pos, t4_pos = get_chapter_content()
    
    print("Building Word document...")
    table1, table2, table3, table4 = get_tables()
    
    # Prepare content for docx
    content_paras = []
    for i, para in enumerate(paragraphs):
        content_paras.append({
            'text': para['text'],
            'style': para['style'],
            'bold': para.get('bold', False)
        })
    
    tables = [
        (t1_pos, table1),
        (t2_pos, table2),
        (t3_pos, table3),
        (t4_pos, table4),
    ]
    
    images = [
        (fig1_pos, fig1_path, "Figure 1. AI Readiness Dimensions Framework for Higher Education 5.0"),
        (fig2_pos, fig2_path, "Figure 2. Readiness Maturity Level Progression from Emerging to Transformation-Ready"),
        (fig3_pos, fig3_path, "Figure 3. Comparative Analysis of Faculty and Student AI Acceptance Factors"),
        (fig4_pos, fig4_path, "Figure 4. Strategic Implementation Roadmap for AI-Ready Higher Education Institutions"),
    ]
    
    output_path = os.path.join(output_dir, 'Chapter_AI_Readiness_Higher_Education_5.docx')
    make_docx(content_paras, tables, images, output_path)
    
    # Count words
    total_words = sum(len(p['text'].split()) for p in paragraphs)
    print(f"\nTotal word count: {total_words}")
    print(f"Output: {output_path}")
    print("Done!")
