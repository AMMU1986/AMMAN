#!/usr/bin/env python3
"""
Generate DOCX file for the Accreditation chapter without python-docx.
Uses zipfile and XML directly since DOCX is a ZIP of XML files.
"""
import zipfile
import os
import re
from xml.sax.saxutils import escape

def create_docx(md_path, output_path):
    """Create a DOCX file from the markdown chapter."""
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse markdown into structured elements
    elements = parse_markdown(content)
    
    # Build the document XML
    body_xml = build_body_xml(elements)
    
    # Create the DOCX package
    write_docx_package(output_path, body_xml)
    print(f"Successfully created: {output_path}")


def parse_markdown(text):
    """Parse markdown text into a list of elements."""
    elements = []
    lines = text.split('\n')
    i = 0
    in_table = False
    table_rows = []
    
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines
        if not line.strip():
            if in_table and table_rows:
                elements.append(('table', table_rows))
                table_rows = []
                in_table = False
            i += 1
            continue
        
        # Headings
        if line.startswith('# ') and not line.startswith('## '):
            elements.append(('heading1', line[2:].strip()))
            i += 1
            continue
        elif line.startswith('## '):
            elements.append(('heading2', line[3:].strip()))
            i += 1
            continue
        elif line.startswith('### '):
            elements.append(('heading3', line[4:].strip()))
            i += 1
            continue
        
        # Horizontal rule
        if line.strip() == '---':
            i += 1
            continue
        
        # Table detection
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_rows = []
            # Skip separator rows
            if re.match(r'^\|[\s\-|]+\|$', line.strip()):
                i += 1
                continue
            cells = [c.strip() for c in line.strip().split('|')[1:-1]]
            table_rows.append(cells)
            i += 1
            continue
        else:
            if in_table and table_rows:
                elements.append(('table', table_rows))
                table_rows = []
                in_table = False
        
        # Figure description (italic block)
        if line.strip().startswith('*[Figure') or line.strip().startswith('*['):
            elements.append(('italic', line.strip().strip('*')))
            i += 1
            continue
        
        # Bold paragraph (like figure captions)
        if line.strip().startswith('**Figure'):
            elements.append(('bold_para', clean_markdown(line.strip())))
            i += 1
            continue
        
        # Bold paragraph for keywords, table titles, etc.
        if line.strip().startswith('**') and line.strip().endswith('**'):
            elements.append(('bold_para', line.strip().strip('*')))
            i += 1
            continue
        
        # Regular paragraph - collect consecutive lines
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith('#') \
              and not lines[i].startswith('|') and not lines[i].strip() == '---' \
              and not lines[i].strip().startswith('**Figure') \
              and not lines[i].strip().startswith('*['):
            para_lines.append(lines[i])
            i += 1
        
        para_text = ' '.join(para_lines)
        elements.append(('paragraph', para_text))
    
    # Final table if pending
    if in_table and table_rows:
        elements.append(('table', table_rows))
    
    return elements


def clean_markdown(text):
    """Remove markdown formatting markers."""
    # Remove bold markers
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    # Remove italic markers
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    return text


def build_body_xml(elements):
    """Build the w:body XML content from parsed elements."""
    body_parts = []
    
    for elem_type, content in elements:
        if elem_type == 'heading1':
            body_parts.append(make_heading(content, 1))
        elif elem_type == 'heading2':
            body_parts.append(make_heading(content, 2))
        elif elem_type == 'heading3':
            body_parts.append(make_heading(content, 3))
        elif elem_type == 'bold_para':
            body_parts.append(make_bold_paragraph(content))
        elif elem_type == 'italic':
            body_parts.append(make_italic_paragraph(content))
        elif elem_type == 'paragraph':
            body_parts.append(make_paragraph(content))
        elif elem_type == 'table':
            body_parts.append(make_table(content))
    
    return '\n'.join(body_parts)


def make_heading(text, level):
    """Create heading XML."""
    text = clean_markdown(text)
    sizes = {1: '32', 2: '28', 3: '24'}
    size = sizes.get(level, '24')
    return f'''<w:p>
  <w:pPr><w:pStyle w:val="Heading{level}"/></w:pPr>
  <w:r><w:rPr><w:b/><w:sz w:val="{size}"/></w:rPr><w:t>{escape(text)}</w:t></w:r>
</w:p>'''


def make_paragraph(text):
    """Create paragraph XML with inline formatting."""
    text = clean_markdown(text)
    return f'''<w:p>
  <w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r>
</w:p>'''


def make_bold_paragraph(text):
    """Create bold paragraph XML."""
    return f'''<w:p>
  <w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r>
</w:p>'''


def make_italic_paragraph(text):
    """Create italic paragraph XML."""
    return f'''<w:p>
  <w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r>
</w:p>'''


def make_table(rows):
    """Create table XML."""
    if not rows:
        return ''
    
    num_cols = len(rows[0]) if rows else 0
    col_width = 9000 // max(num_cols, 1)
    
    tbl_xml = '<w:tbl>\n<w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="9000" w:type="dxa"/><w:tblBorders>'
    tbl_xml += '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl_xml += '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl_xml += '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl_xml += '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl_xml += '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl_xml += '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl_xml += '</w:tblBorders></w:tblPr>\n'
    
    # Grid columns
    tbl_xml += '<w:tblGrid>'
    for _ in range(num_cols):
        tbl_xml += f'<w:gridCol w:w="{col_width}"/>'
    tbl_xml += '</w:tblGrid>\n'
    
    for row_idx, row in enumerate(rows):
        tbl_xml += '<w:tr>'
        for cell in row:
            cell_text = escape(clean_markdown(cell))
            if row_idx == 0:
                # Header row - bold
                tbl_xml += f'<w:tc><w:p><w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{cell_text}</w:t></w:r></w:p></w:tc>'
            else:
                tbl_xml += f'<w:tc><w:p><w:r><w:t xml:space="preserve">{cell_text}</w:t></w:r></w:p></w:tc>'
        tbl_xml += '</w:tr>\n'
    
    tbl_xml += '</w:tbl>'
    return tbl_xml


def write_docx_package(output_path, body_xml):
    """Write the complete DOCX ZIP package."""
    
    # [Content_Types].xml
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''
    
    # _rels/.rels
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''
    
    # word/_rels/document.xml.rels
    doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''
    
    # word/styles.xml
    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="200" w:line="276" w:lineRule="auto"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="480" w:after="240"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="360" w:after="200"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
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
    
    # word/document.xml
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{body_xml}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>'''
    
    # Write the ZIP/DOCX file
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', doc_rels)
        zf.writestr('word/styles.xml', styles)
        zf.writestr('word/document.xml', document)


if __name__ == '__main__':
    md_file = '/projects/sandbox/AMMAN/Chapter_Accreditation_Accountability_Learning_Renewal.md'
    docx_file = '/projects/sandbox/AMMAN/Chapter_Accreditation_Accountability_Learning_Renewal.docx'
    create_docx(md_file, docx_file)
