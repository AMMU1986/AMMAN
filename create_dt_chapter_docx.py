#!/usr/bin/env python3
"""
Create DOCX for: Design Thinking Across Core Business Functions
Uses raw zipfile/XML approach since python-docx is not available.
"""

import zipfile
import os
import struct
import zlib
from xml.etree.ElementTree import Element, SubElement, tostring

# Namespaces
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
WP_NS = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
PIC_NS = 'http://schemas.openxmlformats.org/drawingml/2006/picture'
CT_NS = 'http://schemas.openxmlformats.org/package/2006/content-types'
REL_NS = 'http://schemas.openxmlformats.org/package/2006/relationships'


def make_content_types():
    """Create [Content_Types].xml"""
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    xml += '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    xml += '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    xml += '<Default Extension="xml" ContentType="application/xml"/>'
    xml += '<Default Extension="png" ContentType="image/png"/>'
    xml += '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    xml += '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    xml += '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
    xml += '</Types>'
    return xml


def make_rels():
    """Create _rels/.rels"""
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    xml += '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    xml += '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    xml += '</Relationships>'
    return xml


def make_word_rels(image_count):
    """Create word/_rels/document.xml.rels"""
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    xml += '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    xml += '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    xml += '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
    for i in range(1, image_count + 1):
        xml += f'<Relationship Id="rIdImg{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image{i}.png"/>'
    xml += '</Relationships>'
    return xml


def make_styles():
    """Create word/styles.xml"""
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    xml += '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    
    # Normal style
    xml += '''<w:style w:type="paragraph" w:default="1" w:styleId="Normal">
        <w:name w:val="Normal"/>
        <w:pPr><w:spacing w:after="200" w:line="360" w:lineRule="auto"/></w:pPr>
        <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr>
    </w:style>'''
    
    # Title style
    xml += '''<w:style w:type="paragraph" w:styleId="Title">
        <w:name w:val="Title"/>
        <w:pPr><w:spacing w:before="0" w:after="200"/><w:jc w:val="center"/></w:pPr>
        <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="32"/></w:rPr>
    </w:style>'''
    
    # Heading1
    xml += '''<w:style w:type="paragraph" w:styleId="Heading1">
        <w:name w:val="heading 1"/>
        <w:pPr><w:spacing w:before="360" w:after="200"/></w:pPr>
        <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr>
    </w:style>'''
    
    # Heading2
    xml += '''<w:style w:type="paragraph" w:styleId="Heading2">
        <w:name w:val="heading 2"/>
        <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
        <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="26"/></w:rPr>
    </w:style>'''
    
    # Heading3
    xml += '''<w:style w:type="paragraph" w:styleId="Heading3">
        <w:name w:val="heading 3"/>
        <w:pPr><w:spacing w:before="200" w:after="100"/></w:pPr>
        <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:i/><w:sz w:val="24"/></w:rPr>
    </w:style>'''
    
    # Caption style
    xml += '''<w:style w:type="paragraph" w:styleId="Caption">
        <w:name w:val="Caption"/>
        <w:pPr><w:spacing w:before="100" w:after="200"/><w:jc w:val="center"/></w:pPr>
        <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:i/><w:sz w:val="20"/></w:rPr>
    </w:style>'''
    
    xml += '</w:styles>'
    return xml


def make_numbering():
    """Create word/numbering.xml"""
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    xml += '<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    xml += '</w:numbering>'
    return xml


def make_paragraph(text, style=None, bold=False, italic=False, font_size=None, alignment=None):
    """Create a paragraph XML string"""
    xml = '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    
    # Paragraph properties
    ppr = ''
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if alignment:
        ppr += f'<w:jc w:val="{alignment}"/>'
    if ppr:
        xml += f'<w:pPr>{ppr}</w:pPr>'
    
    # Run
    if text:
        xml += '<w:r>'
        rpr = ''
        if bold:
            rpr += '<w:b/>'
        if italic:
            rpr += '<w:i/>'
        if font_size:
            rpr += f'<w:sz w:val="{font_size}"/>'
        if rpr:
            xml += f'<w:rPr>{rpr}</w:rPr>'
        # Escape XML special chars
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        xml += f'<w:t xml:space="preserve">{text}</w:t>'
        xml += '</w:r>'
    
    xml += '</w:p>'
    return xml


def make_image_paragraph(rid, width_emu, height_emu, caption=""):
    """Create paragraph with inline image"""
    xml = '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    xml += 'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    xml += 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    xml += 'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
    xml += 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    xml += '<w:pPr><w:jc w:val="center"/></w:pPr>'
    xml += '<w:r><w:drawing>'
    xml += f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
    xml += f'<wp:extent cx="{width_emu}" cy="{height_emu}"/>'
    xml += '<wp:docPr id="1" name="Picture"/>'
    xml += '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
    xml += '<pic:pic><pic:nvPicPr><pic:cNvPr id="0" name="Picture"/><pic:cNvPicPr/></pic:nvPicPr>'
    xml += f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
    xml += f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{width_emu}" cy="{height_emu}"/></a:xfrm>'
    xml += '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
    xml += '</pic:pic></a:graphicData></a:graphic>'
    xml += '</wp:inline></w:drawing></w:r></w:p>'
    return xml


def make_table(headers, rows):
    """Create a simple table XML"""
    xml = '<w:tbl xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    # Table properties
    xml += '<w:tblPr>'
    xml += '<w:tblStyle w:val="TableGrid"/>'
    xml += '<w:tblW w:w="5000" w:type="pct"/>'
    xml += '<w:tblBorders>'
    xml += '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '</w:tblBorders>'
    xml += '</w:tblPr>'
    
    # Header row
    xml += '<w:tr>'
    for h in headers:
        h_escaped = h.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        xml += '<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="2C3E50"/></w:tcPr>'
        xml += '<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>'
        xml += f'<w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="20"/></w:rPr>'
        xml += f'<w:t xml:space="preserve">{h_escaped}</w:t></w:r></w:p></w:tc>'
    xml += '</w:tr>'
    
    # Data rows
    for row in rows:
        xml += '<w:tr>'
        for cell in row:
            cell_escaped = cell.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            xml += '<w:tc><w:p><w:pPr><w:spacing w:after="0"/></w:pPr>'
            xml += f'<w:r><w:rPr><w:sz w:val="20"/></w:rPr>'
            xml += f'<w:t xml:space="preserve">{cell_escaped}</w:t></w:r></w:p></w:tc>'
        xml += '</w:tr>'
    
    xml += '</w:tbl>'
    return xml


def build_document():
    """Build the complete document.xml content"""
    
    # Start document
    doc = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    doc += '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    doc += 'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    doc += 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    doc += 'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
    doc += 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    doc += '<w:body>'
    
    # Read the markdown file and convert to docx XML
    with open('Chapter_Design_Thinking_Business_Functions.md', 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    i = 0
    figure_count = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            i += 1
            continue
        
        # Title (# )
        if line.startswith('# ') and not line.startswith('## '):
            text = line[2:].strip()
            doc += make_paragraph(text, style="Title", bold=True)
            i += 1
            continue
        
        # Heading 1 (## )
        if line.startswith('## ') and not line.startswith('### '):
            text = line[3:].strip()
            doc += make_paragraph(text, style="Heading1", bold=True)
            i += 1
            continue
        
        # Heading 2 (### )
        if line.startswith('### '):
            text = line[4:].strip()
            doc += make_paragraph(text, style="Heading2", bold=True)
            i += 1
            continue
        
        # Horizontal rule
        if line == '---':
            i += 1
            continue
        
        # Bold text markers
        if line.startswith('**') and line.endswith('**'):
            text = line.strip('*').strip()
            doc += make_paragraph(text, bold=True)
            i += 1
            continue
        
        # Figure placeholders
        if '[Insert Figure' in line:
            figure_count += 1
            # Image: 15cm wide = 5715000 EMU, height proportional (assume 600/1200 ratio)
            w_emu = 5715000
            h_emu = 2857500  # approximately half width for 1200x600 images
            if figure_count >= 3:
                h_emu = 3333750  # 1200x700 images
            doc += make_image_paragraph(f"rIdImg{figure_count}", w_emu, h_emu)
            i += 1
            continue
        
        # Figure caption (italic)
        if line.startswith('*Figure') and line.endswith('*'):
            text = line.strip('*').strip()
            doc += make_paragraph(text, style="Caption", italic=True)
            i += 1
            continue
        
        # Table detection
        if line.startswith('|') and i + 1 < len(lines) and lines[i+1].strip().startswith('|---'):
            # Parse table
            headers = [h.strip() for h in line.split('|')[1:-1]]
            i += 2  # skip header and separator
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                row = [c.strip() for c in lines[i].strip().split('|')[1:-1]]
                rows.append(row)
                i += 1
            doc += make_table(headers, rows)
            continue
        
        # Regular paragraph (may contain inline formatting)
        if line.startswith('*') and not line.startswith('**'):
            # Italic paragraph (caption or keyword)
            text = line.strip('*').strip()
            doc += make_paragraph(text, italic=True)
        elif line.startswith('**') and '**' in line[2:]:
            # Bold start - like "**Keywords:**..."
            text = line.replace('**', '')
            doc += make_paragraph(text, bold=True)
        else:
            # Clean up any remaining markdown
            text = line.replace('**', '').replace('*', '')
            doc += make_paragraph(text)
        
        i += 1
    
    # Close document
    doc += '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
    doc += '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
    doc += '</w:sectPr></w:body></w:document>'
    
    return doc


def create_docx():
    """Create the complete DOCX file"""
    output_file = 'Chapter_Design_Thinking_Business_Functions.docx'
    
    # Image files
    images = [
        'dt_figures/Figure_1_Design_Thinking_Process.png',
        'dt_figures/Figure_2_Customer_Experience_Framework.png',
        'dt_figures/Figure_3_Business_Model_Innovation.png',
        'dt_figures/Figure_4_Organizational_Readiness.png',
    ]
    
    # Build all parts
    content_types = make_content_types()
    rels = make_rels()
    word_rels = make_word_rels(len(images))
    styles = make_styles()
    numbering = make_numbering()
    document = build_document()
    
    # Create DOCX (ZIP file)
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', styles)
        zf.writestr('word/numbering.xml', numbering)
        
        # Add images
        for i, img_path in enumerate(images, 1):
            if os.path.exists(img_path):
                zf.write(img_path, f'word/media/image{i}.png')
            else:
                print(f"Warning: {img_path} not found!")
    
    print(f"DOCX created: {output_file}")
    print(f"File size: {os.path.getsize(output_file)} bytes")


if __name__ == '__main__':
    create_docx()
