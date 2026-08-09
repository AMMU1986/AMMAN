#!/usr/bin/env python3
"""
Create a Word .docx file from the Design Thinking chapter markdown.
Uses raw OOXML (ZIP + XML) since python-docx is not available.
"""

import zipfile
import os
import re

# ─── OOXML boilerplate templates ───

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
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:pPr><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
</w:styles>'''


def escape_xml(text):
    """Escape special XML characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text


def make_run(text, bold=False, italic=False):
    """Create a w:r (run) element."""
    rpr = ''
    props = []
    if bold:
        props.append('<w:b/>')
    if italic:
        props.append('<w:i/>')
    if props:
        rpr = '<w:rPr>' + ''.join(props) + '</w:rPr>'
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'


def parse_inline(text):
    """Parse inline markdown (bold, italic) into runs."""
    runs = []
    # Pattern for **bold** and *italic*
    parts = re.split(r'(\*\*.*?\*\*|\*.*?\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            runs.append(make_run(part[2:-2], bold=True))
        elif part.startswith('*') and part.endswith('*') and not part.startswith('**'):
            runs.append(make_run(part[1:-1], italic=True))
        elif part:
            runs.append(make_run(part))
    return ''.join(runs)


def make_paragraph(text, style='Normal', bold=False):
    """Create a paragraph with optional style."""
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style != 'Normal' else ''
    if bold and style == 'Normal':
        runs = make_run(text, bold=True)
    else:
        runs = parse_inline(text)
    return f'<w:p>{ppr}{runs}</w:p>'


def make_table(headers, rows):
    """Create a simple table."""
    tbl = '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="0" w:type="auto"/><w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/></w:tblBorders></w:tblPr>'
    
    # Header row
    tbl += '<w:tr>'
    for h in headers:
        tbl += f'<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr><w:p><w:pPr><w:jc w:val="center"/></w:pPr>{make_run(h.strip(), bold=True)}</w:p></w:tc>'
    tbl += '</w:tr>'
    
    # Data rows
    for row in rows:
        tbl += '<w:tr>'
        for cell in row:
            tbl += f'<w:tc><w:p>{make_run(cell.strip())}</w:p></w:tc>'
        tbl += '</w:tr>'
    
    tbl += '</w:tbl>'
    return tbl


def md_to_docx_body(md_text):
    """Convert markdown to OOXML body paragraphs."""
    paragraphs = []
    lines = md_text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines
        if not line.strip():
            i += 1
            continue
        
        # Headings
        if line.startswith('# ') and not line.startswith('## '):
            paragraphs.append(make_paragraph(line[2:].strip(), 'Title'))
            i += 1
            continue
        
        if line.startswith('## '):
            paragraphs.append(make_paragraph(line[3:].strip(), 'Heading1'))
            i += 1
            continue
            
        if line.startswith('### '):
            paragraphs.append(make_paragraph(line[4:].strip(), 'Heading2'))
            i += 1
            continue
            
        if line.startswith('#### '):
            paragraphs.append(make_paragraph(line[5:].strip(), 'Heading3'))
            i += 1
            continue
        
        # Table detection
        if '|' in line and i + 1 < len(lines) and '---' in lines[i + 1]:
            # Parse table
            headers = [c.strip() for c in line.split('|') if c.strip()]
            i += 2  # skip header and separator
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                row = [c.strip() for c in lines[i].split('|') if c.strip()]
                rows.append(row)
                i += 1
            paragraphs.append(make_table(headers, rows))
            continue
        
        # Horizontal rule
        if line.strip() == '---':
            i += 1
            continue
        
        # Normal paragraph (may span multiple lines until empty line)
        para_text = line.strip()
        i += 1
        paragraphs.append(make_paragraph(para_text))
    
    return '\n'.join(paragraphs)


def create_docx(md_filepath, output_filepath):
    """Create a .docx file from markdown."""
    with open(md_filepath, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    body_xml = md_to_docx_body(md_content)
    
    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {body_xml}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''
    
    with zipfile.ZipFile(output_filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', WORD_RELS)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES)
    
    print(f"Created: {output_filepath}")
    print(f"File size: {os.path.getsize(output_filepath) / 1024:.1f} KB")


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md_file = os.path.join(script_dir, 'Chapter_Design_Thinking_Business_Functions.md')
    docx_file = os.path.join(script_dir, 'Chapter_Design_Thinking_Business_Functions.docx')
    create_docx(md_file, docx_file)
