#!/usr/bin/env python3
"""
Create a Word (.docx) document for Chapter 1 from the markdown source.
Uses only Python standard library (zipfile, xml) - no external dependencies.
DOCX is a ZIP archive containing XML files (Office Open XML format).
"""

import zipfile
import os
import re
from xml.sax.saxutils import escape

INPUT_MD = "/projects/sandbox/AMMAN/Chapter_1_Introduction_to_Rehabilitation_Robots.md"
OUTPUT_DOCX = "/projects/sandbox/AMMAN/Chapter_1_Introduction_to_Rehabilitation_Robots.docx"

# Read the markdown file
with open(INPUT_MD, "r", encoding="utf-8") as f:
    md_content = f.read()

# ============================================================
# DOCX XML Templates
# ============================================================

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

WORD_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:pPr><w:spacing w:after="200" w:line="276" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="480" w:after="240"/><w:keepNext/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:b/><w:sz w:val="36"/><w:color w:val="1A1A2E"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="200"/><w:keepNext/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:b/><w:sz w:val="32"/><w:color w:val="2C3E50"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="280" w:after="160"/><w:keepNext/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:b/><w:sz w:val="28"/><w:color w:val="34495E"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading4">
    <w:name w:val="heading 4"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:keepNext/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:b/><w:i/><w:sz w:val="24"/><w:color w:val="4A4A6A"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="Table Caption"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="120" w:after="240"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Reference">
    <w:name w:val="Reference"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:after="120"/><w:ind w:left="480" w:hanging="480"/></w:pPr>
    <w:rPr><w:sz w:val="20"/></w:rPr>
  </w:style>
</w:styles>'''


def make_run(text, bold=False, italic=False):
    """Create a run element with optional formatting."""
    rpr = ""
    if bold or italic:
        rpr = "<w:rPr>"
        if bold:
            rpr += "<w:b/>"
        if italic:
            rpr += "<w:i/>"
        rpr += "</w:rPr>"
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def process_inline(text):
    """Process inline markdown formatting (bold, italic) into runs."""
    runs = []
    # Process **bold** and *italic*
    parts = re.split(r'(\*\*.*?\*\*|\*.*?\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            runs.append(make_run(part[2:-2], bold=True))
        elif part.startswith('*') and part.endswith('*'):
            runs.append(make_run(part[1:-1], italic=True))
        elif part:
            runs.append(make_run(part))
    return ''.join(runs)


def make_paragraph(text, style="Normal"):
    """Create a paragraph element."""
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style != "Normal" else ""
    runs = process_inline(text)
    return f'<w:p>{ppr}{runs}</w:p>'


def make_table_row(cells, is_header=False):
    """Create a table row."""
    row = '<w:tr>'
    for cell in cells:
        cell_text = cell.strip()
        rpr = "<w:rPr><w:b/></w:rPr>" if is_header else ""
        row += f'''<w:tc>
          <w:tcPr><w:tcBorders>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          </w:tcBorders></w:tcPr>
          <w:p><w:pPr><w:spacing w:after="60"/></w:pPr>
            <w:r>{rpr}<w:t xml:space="preserve">{escape(cell_text)}</w:t></w:r>
          </w:p>
        </w:tc>'''
    row += '</w:tr>'
    return row


def make_table(rows_data):
    """Create a table from parsed row data."""
    if len(rows_data) < 2:
        return ""
    
    num_cols = len(rows_data[0])
    # Calculate approximate column widths (total page width ~9360 twips)
    col_width = 9360 // num_cols
    
    tbl = '<w:tbl><w:tblPr>'
    tbl += '<w:tblStyle w:val="TableGrid"/>'
    tbl += '<w:tblW w:w="9360" w:type="dxa"/>'
    tbl += '<w:tblBorders>'
    tbl += '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '</w:tblBorders>'
    tbl += '</w:tblPr>'
    
    # Grid
    tbl += '<w:tblGrid>'
    for _ in range(num_cols):
        tbl += f'<w:gridCol w:w="{col_width}"/>'
    tbl += '</w:tblGrid>'
    
    # Header row
    tbl += make_table_row(rows_data[0], is_header=True)
    
    # Data rows (skip separator row if present)
    for row in rows_data[1:]:
        # Skip separator rows (containing only dashes)
        if all(re.match(r'^[-:\s]+$', cell) for cell in row):
            continue
        tbl += make_table_row(row, is_header=False)
    
    tbl += '</w:tbl>'
    return tbl


def convert_md_to_docx_body(md_text):
    """Convert markdown text to DOCX body XML."""
    body_elements = []
    lines = md_text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines
        if not line.strip():
            i += 1
            continue
        
        # Skip horizontal rules
        if line.strip() == '---':
            i += 1
            continue
        
        # Skip image lines (we reference them in captions instead)
        if line.strip().startswith('!['):
            i += 1
            continue
        
        # Headings
        if line.startswith('# '):
            body_elements.append(make_paragraph(line[2:].strip(), "Heading1"))
            i += 1
            continue
        elif line.startswith('## '):
            body_elements.append(make_paragraph(line[3:].strip(), "Heading2"))
            i += 1
            continue
        elif line.startswith('### '):
            body_elements.append(make_paragraph(line[4:].strip(), "Heading3"))
            i += 1
            continue
        elif line.startswith('#### '):
            body_elements.append(make_paragraph(line[5:].strip(), "Heading4"))
            i += 1
            continue
        
        # Table detection
        if '|' in line and line.strip().startswith('|'):
            table_rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().split('|')[1:-1]]
                table_rows.append(cells)
                i += 1
            if table_rows:
                body_elements.append(make_table(table_rows))
            continue
        
        # Figure/Table caption lines (bold starts)
        if line.strip().startswith('**Figure') or line.strip().startswith('**Table'):
            body_elements.append(make_paragraph(line.strip(), "FigureCaption"))
            i += 1
            continue
        
        # Reference entries
        if re.match(r'^\[\d+\]', line.strip()):
            body_elements.append(make_paragraph(line.strip(), "Reference"))
            i += 1
            continue
        
        # Regular paragraphs
        body_elements.append(make_paragraph(line.strip()))
        i += 1
    
    return '\n'.join(body_elements)


# Convert markdown to body XML
print("Converting markdown to DOCX XML...")
body_xml = convert_md_to_docx_body(md_content)

# Create the document.xml
DOCUMENT_XML = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {body_xml}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720"/>
    </w:sectPr>
  </w:body>
</w:document>'''

# Create the DOCX file (ZIP archive)
print("Creating DOCX file...")
with zipfile.ZipFile(OUTPUT_DOCX, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('[Content_Types].xml', CONTENT_TYPES)
    zf.writestr('_rels/.rels', RELS)
    zf.writestr('word/_rels/document.xml.rels', WORD_RELS)
    zf.writestr('word/document.xml', DOCUMENT_XML)
    zf.writestr('word/styles.xml', STYLES)

file_size = os.path.getsize(OUTPUT_DOCX) / 1024
print(f"\nDOCX file created successfully!")
print(f"Output: {OUTPUT_DOCX}")
print(f"File size: {file_size:.1f} KB")
