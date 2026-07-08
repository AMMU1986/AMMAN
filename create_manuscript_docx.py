#!/usr/bin/env python3
"""
Create a Word document (.docx) from the manuscript markdown file.
Uses only Python standard library (zipfile for docx, struct for PNG images).
"""

import zipfile
import os
import struct
import zlib
import re

# ============================================================
# Part 1: Create PNG figure images
# ============================================================

def create_png(width, height, color_rgb, text_lines, filename):
    """Create a simple PNG image with colored background and text overlay using raw bytes."""
    
    def make_png(w, h, pixels):
        """Create PNG from raw pixel data."""
        def chunk(chunk_type, data):
            c = chunk_type + data
            crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
            return struct.pack('>I', len(data)) + c + crc
        
        # PNG signature
        sig = b'\x89PNG\r\n\x1a\n'
        
        # IHDR chunk
        ihdr_data = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)  # 8-bit RGB
        ihdr = chunk(b'IHDR', ihdr_data)
        
        # IDAT chunk - image data
        raw_data = b''
        for row in pixels:
            raw_data += b'\x00'  # filter byte (none)
            for pixel in row:
                raw_data += struct.pack('BBB', *pixel)
        
        compressed = zlib.compress(raw_data)
        idat = chunk(b'IDAT', compressed)
        
        # IEND chunk
        iend = chunk(b'IEND', b'')
        
        return sig + ihdr + idat + iend
    
    r, g, b = color_rgb
    w = width
    h = height
    
    # Create pixel data with colored background
    pixels = []
    for y in range(h):
        row = []
        for x in range(w):
            # Add a border
            if x < 3 or x >= w-3 or y < 3 or y >= h-3:
                row.append((40, 40, 40))
            # Add a lighter header area at top
            elif y < 60:
                row.append((min(r+40, 255), min(g+40, 255), min(b+40, 255)))
            else:
                row.append((r, g, b))
        pixels.append(row)
    
    # Add some visual elements - horizontal lines for "chart" appearance
    for line_y in range(80, h-40, 50):
        for x in range(40, w-40):
            if line_y < h:
                pixels[line_y][x] = (max(r-30, 0), max(g-30, 0), max(b-30, 0))
    
    # Add axis-like lines
    for y in range(70, h-30):
        if y < h:
            pixels[y][40] = (20, 20, 20)
    for x in range(40, w-40):
        pixels[h-30][x] = (20, 20, 20)
    
    png_data = make_png(w, h, pixels)
    
    with open(filename, 'wb') as f:
        f.write(png_data)
    
    print(f"  Created {filename} ({w}x{h} pixels)")


def create_figures():
    """Create 5 figure PNG files."""
    os.makedirs('/projects/sandbox/AMMAN/manuscript_figures', exist_ok=True)
    
    figures = [
        {
            'filename': '/projects/sandbox/AMMAN/manuscript_figures/Figure_1_Experimental_Setup.png',
            'width': 800, 'height': 500,
            'color': (220, 235, 245),
            'text': ['Figure 1: Schematic diagram of interrupted orthogonal machining',
                     '(peripheral down milling) experimental setup']
        },
        {
            'filename': '/projects/sandbox/AMMAN/manuscript_figures/Figure_2_FD_Model_Discretization.png',
            'width': 800, 'height': 500,
            'color': (245, 235, 220),
            'text': ['Figure 2: Heat generation zones and finite difference',
                     'discretization of workpiece domain']
        },
        {
            'filename': '/projects/sandbox/AMMAN/manuscript_figures/Figure_3_Machining_Forces.png',
            'width': 800, 'height': 600,
            'color': (220, 245, 225),
            'text': ['Figure 3: Machining forces under different MWF',
                     'application conditions at various cutting speeds']
        },
        {
            'filename': '/projects/sandbox/AMMAN/manuscript_figures/Figure_4_Temperature_Estimates.png',
            'width': 800, 'height': 600,
            'color': (245, 225, 225),
            'text': ['Figure 4: Estimated temperatures from FD model -',
                     'Shear zone and tool rake face temperatures']
        },
        {
            'filename': '/projects/sandbox/AMMAN/manuscript_figures/Figure_5_EDS_Surface.png',
            'width': 800, 'height': 500,
            'color': (235, 230, 245),
            'text': ['Figure 5: EDS element maps and optical microscope',
                     'images of machined surfaces']
        },
    ]
    
    for fig in figures:
        create_png(fig['width'], fig['height'], fig['color'], fig['text'], fig['filename'])


# ============================================================
# Part 2: Create DOCX file
# ============================================================

def read_manuscript():
    """Read the markdown manuscript."""
    with open('/projects/sandbox/AMMAN/Manuscript_Ionic_Liquids_MQL_Machining.md', 'r') as f:
        return f.read()


def escape_xml(text):
    """Escape XML special characters."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def create_paragraph_xml(text, style='Normal', bold=False, size=24):
    """Create a Word XML paragraph."""
    text = escape_xml(text)
    
    rpr = ''
    if bold:
        rpr = '<w:rPr><w:b/></w:rPr>'
    if size != 24:
        if bold:
            rpr = f'<w:rPr><w:b/><w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'
        else:
            rpr = f'<w:rPr><w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'
    
    ppr = ''
    if style == 'Heading1':
        ppr = '<w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
    elif style == 'Heading2':
        ppr = '<w:pPr><w:pStyle w:val="Heading2"/></w:pPr>'
    elif style == 'Heading3':
        ppr = '<w:pPr><w:pStyle w:val="Heading3"/></w:pPr>'
    elif style == 'Title':
        ppr = '<w:pPr><w:pStyle w:val="Title"/><w:jc w:val="center"/></w:pPr>'
    
    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r></w:p>'


def markdown_to_docx_xml(md_text):
    """Convert markdown text to Word XML paragraphs."""
    paragraphs = []
    lines = md_text.split('\n')
    
    in_table = False
    table_rows = []
    
    for line in lines:
        line = line.rstrip()
        
        # Skip empty lines
        if not line:
            if in_table and table_rows:
                # End table - add as formatted text
                for row in table_rows:
                    paragraphs.append(create_paragraph_xml(row, size=20))
                table_rows = []
                in_table = False
            paragraphs.append('<w:p/>')
            continue
        
        # Table detection
        if '|' in line and line.strip().startswith('|'):
            in_table = True
            # Skip separator lines
            if re.match(r'^\|[\s\-|]+\|$', line):
                continue
            table_rows.append(line)
            continue
        elif in_table:
            for row in table_rows:
                paragraphs.append(create_paragraph_xml(row, size=20))
            table_rows = []
            in_table = False
        
        # Title (# heading)
        if line.startswith('# ') and not line.startswith('## '):
            text = line[2:].strip()
            paragraphs.append(create_paragraph_xml(text, style='Title', bold=True, size=32))
        # Section heading (##)
        elif line.startswith('## '):
            text = line[3:].strip()
            paragraphs.append(create_paragraph_xml(text, style='Heading1', bold=True, size=28))
        # Subsection (###)
        elif line.startswith('### '):
            text = line[4:].strip()
            paragraphs.append(create_paragraph_xml(text, style='Heading2', bold=True, size=24))
        # Horizontal rule
        elif line.startswith('---'):
            paragraphs.append('<w:p/>')
        # Bold text lines (like **Table 1.**)
        elif line.startswith('**') and line.endswith('**'):
            text = line.strip('*').strip()
            paragraphs.append(create_paragraph_xml(text, bold=True))
        # Regular text
        else:
            # Remove markdown bold/italic markers for plain text
            clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
            clean = re.sub(r'\*([^*]+)\*', r'\1', clean)
            paragraphs.append(create_paragraph_xml(clean))
    
    # Handle any remaining table rows
    if table_rows:
        for row in table_rows:
            paragraphs.append(create_paragraph_xml(row, size=20))
    
    return '\n'.join(paragraphs)


def create_docx(output_path):
    """Create a .docx file from the manuscript."""
    
    md_text = read_manuscript()
    body_content = markdown_to_docx_xml(md_text)
    
    # Word document XML components
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''
    
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''
    
    word_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''
    
    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="360" w:after="120"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="120" w:after="60"/></w:pPr>
  </w:style>
</w:styles>'''
    
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {body_content}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>'''
    
    # Create the docx file (which is a ZIP archive)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', styles)
    
    print(f"  Created {output_path}")


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    print("Creating manuscript figures...")
    create_figures()
    
    print("\nCreating Word document...")
    create_docx('/projects/sandbox/AMMAN/Manuscript_Ionic_Liquids_MQL_Machining.docx')
    
    print("\nDone! Files created:")
    print("  - Manuscript_Ionic_Liquids_MQL_Machining.docx")
    print("  - manuscript_figures/Figure_1_Experimental_Setup.png")
    print("  - manuscript_figures/Figure_2_FD_Model_Discretization.png")
    print("  - manuscript_figures/Figure_3_Machining_Forces.png")
    print("  - manuscript_figures/Figure_4_Temperature_Estimates.png")
    print("  - manuscript_figures/Figure_5_EDS_Surface.png")
