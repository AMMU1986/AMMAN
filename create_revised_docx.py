#!/usr/bin/env python3
"""
Create a Word document (.docx) from the revised Tesla valve CFD manuscript.
Text between == markers is highlighted in yellow to indicate revisions.
"""

import zipfile
import re
import os


def escape_xml(text):
    """Escape XML special characters."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def parse_markdown_to_paragraphs(md_text):
    """Parse markdown text into structured paragraphs with formatting info."""
    paragraphs = []
    lines = md_text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()
        
        # Skip horizontal rules
        if stripped == '---':
            i += 1
            continue
        
        # Empty line
        if not stripped:
            paragraphs.append({'type': 'empty', 'text': ''})
            i += 1
            continue
        
        # Title (# heading)
        if stripped.startswith('# ') and not stripped.startswith('## '):
            text = stripped[2:].strip()
            paragraphs.append({'type': 'title', 'text': text})
            i += 1
            continue
        
        # Section heading (##)
        if stripped.startswith('## '):
            text = stripped[3:].strip()
            paragraphs.append({'type': 'heading1', 'text': text})
            i += 1
            continue
        
        # Subsection (###)
        if stripped.startswith('### '):
            text = stripped[4:].strip()
            paragraphs.append({'type': 'heading2', 'text': text})
            i += 1
            continue
        
        # Table detection
        if '|' in stripped and stripped.strip().startswith('|'):
            # Collect all table rows
            table_rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip().startswith('|'):
                row = lines[i].strip()
                # Skip separator lines (|---|---|)
                if not re.match(r'^\|[\s\-:|]+\|$', row):
                    table_rows.append(row)
                i += 1
            paragraphs.append({'type': 'table', 'rows': table_rows})
            continue
        
        # Regular paragraph (may span multiple lines)
        para_text = stripped
        i += 1
        # Collect continuation lines (not empty, not heading, not table, not rule)
        while i < len(lines):
            next_line = lines[i].rstrip()
            if (not next_line or next_line.startswith('#') or next_line == '---' or 
                (next_line.strip().startswith('|') and '|' in next_line)):
                break
            para_text += ' ' + next_line
            i += 1
        
        paragraphs.append({'type': 'paragraph', 'text': para_text})
    
    return paragraphs


def text_to_runs(text):
    """Convert text with == highlighting and ** bold markers to runs with formatting."""
    runs = []
    
    # First, process the text to identify highlighted and bold sections
    # We'll parse character by character with state tracking
    # Simplified approach: use regex to split into segments
    
    # Pattern to find ==...== (highlighted) sections
    # Within those, there may be **...** (bold) markers
    
    segments = re.split(r'(==)', text)
    
    in_highlight = False
    current_segments = []
    
    for seg in segments:
        if seg == '==':
            in_highlight = not in_highlight
            continue
        if seg:
            current_segments.append({'text': seg, 'highlight': in_highlight})
    
    # Now process bold within each segment
    for segment in current_segments:
        # Split by ** for bold
        parts = re.split(r'(\*\*)', segment['text'])
        in_bold = False
        for part in parts:
            if part == '**':
                in_bold = not in_bold
                continue
            if part:
                # Clean up any remaining markdown (subscript, superscript)
                # Remove <sub>, </sub>, <sup>, </sup> tags for plain text
                clean = re.sub(r'</?su[bp]>', '', part)
                runs.append({
                    'text': clean,
                    'highlight': segment['highlight'],
                    'bold': in_bold
                })
    
    return runs


def runs_to_xml(runs):
    """Convert runs to Word XML."""
    xml_parts = []
    for run in runs:
        if not run['text']:
            continue
        
        rpr_parts = []
        if run.get('bold'):
            rpr_parts.append('<w:b/><w:bCs/>')
        if run.get('highlight'):
            rpr_parts.append('<w:highlight w:val="yellow"/>')
        
        rpr = ''
        if rpr_parts:
            rpr = '<w:rPr>' + ''.join(rpr_parts) + '</w:rPr>'
        
        escaped_text = escape_xml(run['text'])
        xml_parts.append(f'<w:r>{rpr}<w:t xml:space="preserve">{escaped_text}</w:t></w:r>')
    
    return ''.join(xml_parts)


def paragraph_to_xml(para):
    """Convert a paragraph dict to Word XML."""
    if para['type'] == 'empty':
        return '<w:p><w:pPr><w:spacing w:after="0"/></w:pPr></w:p>'
    
    if para['type'] == 'title':
        runs = text_to_runs(para['text'])
        runs_xml = runs_to_xml(runs)
        return f'''<w:p>
  <w:pPr><w:pStyle w:val="Title"/><w:jc w:val="center"/></w:pPr>
  {runs_xml}
</w:p>'''
    
    if para['type'] == 'heading1':
        runs = text_to_runs(para['text'])
        runs_xml = runs_to_xml(runs)
        return f'''<w:p>
  <w:pPr><w:pStyle w:val="Heading1"/></w:pPr>
  {runs_xml}
</w:p>'''
    
    if para['type'] == 'heading2':
        runs = text_to_runs(para['text'])
        runs_xml = runs_to_xml(runs)
        return f'''<w:p>
  <w:pPr><w:pStyle w:val="Heading2"/></w:pPr>
  {runs_xml}
</w:p>'''
    
    if para['type'] == 'table':
        # Create a Word table
        rows_xml = []
        for row_text in para['rows']:
            # Parse table row cells
            cells = [c.strip() for c in row_text.split('|')[1:-1]]
            cells_xml = []
            for cell in cells:
                runs = text_to_runs(cell)
                runs_xml = runs_to_xml(runs)
                cells_xml.append(f'''<w:tc>
  <w:tcPr><w:tcW w:w="0" w:type="auto"/><w:tcBorders>
    <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
  </w:tcBorders></w:tcPr>
  <w:p><w:pPr><w:spacing w:after="0"/><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:pPr>{runs_xml}</w:p>
</w:tc>''')
            rows_xml.append(f'<w:tr>{"".join(cells_xml)}</w:tr>')
        
        table_xml = f'''<w:tbl>
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
    <w:tblLook w:val="04A0"/>
  </w:tblPr>
  {"".join(rows_xml)}
</w:tbl>'''
        return table_xml
    
    if para['type'] == 'paragraph':
        runs = text_to_runs(para['text'])
        runs_xml = runs_to_xml(runs)
        return f'''<w:p>
  <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
  {runs_xml}
</w:p>'''
    
    return ''


def create_docx(md_file, output_path):
    """Create a .docx file from the revised manuscript markdown."""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # Parse markdown into paragraphs
    paragraphs = parse_markdown_to_paragraphs(md_text)
    
    # Convert to XML
    body_parts = []
    for para in paragraphs:
        xml = paragraph_to_xml(para)
        if xml:
            body_parts.append(xml)
    
    body_content = '\n'.join(body_parts)
    
    # Word document XML components
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
</Types>'''
    
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''
    
    word_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>'''
    
    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:rPr><w:b/><w:bCs/><w:sz w:val="32"/><w:szCs w:val="32"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:rPr><w:b/><w:bCs/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="360" w:after="120"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:rPr><w:b/><w:bCs/><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
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
    
    settings = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:defaultTabStop w:val="720"/>
  <w:characterSpacingControl w:val="doNotCompress"/>
  <w:compat>
    <w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>
  </w:compat>
</w:settings>'''
    
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
        zf.writestr('word/settings.xml', settings)
    
    print(f"Created: {output_path}")
    # Get file size
    size = os.path.getsize(output_path)
    print(f"File size: {size:,} bytes ({size/1024:.1f} KB)")


if __name__ == '__main__':
    md_file = '/projects/sandbox/AMMAN/Revised_Tesla_Valve_CFD_Manuscript.md'
    output_file = '/projects/sandbox/AMMAN/Revised_Tesla_Valve_CFD_Manuscript.docx'
    
    print("=" * 60)
    print("GENERATING REVISED MANUSCRIPT DOCX")
    print("With yellow highlighting for all revisions")
    print("=" * 60)
    print()
    
    create_docx(md_file, output_file)
    
    print()
    print("Done! The revised manuscript has been created with:")
    print("  - Yellow highlighting on all revised/added text")
    print("  - Proper tables for data presentation")
    print("  - Times New Roman font, 12pt, 1.5 line spacing")
    print("  - Justified text alignment")
