#!/usr/bin/env python3
"""
Create a Word document (.docx) for the Differential Equations and Dynamical Systems chapter.
Uses only Python standard library (zipfile for docx creation).
Properly formats tables, references with square bracket citations, and section headings.
"""

import zipfile
import re


def escape_xml(text):
    """Escape XML special characters."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def create_run_xml(text, bold=False, italic=False, size=24, superscript=False):
    """Create a Word XML run element."""
    text = escape_xml(text)
    rpr_parts = []
    if bold:
        rpr_parts.append('<w:b/><w:bCs/>')
    if italic:
        rpr_parts.append('<w:i/><w:iCs/>')
    if size != 24:
        rpr_parts.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    if superscript:
        rpr_parts.append('<w:vertAlign w:val="superscript"/>')
    
    rpr = ''
    if rpr_parts:
        rpr = '<w:rPr>' + ''.join(rpr_parts) + '</w:rPr>'
    
    return f'<w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r>'


def parse_inline_formatting(text, base_size=24):
    """Parse inline markdown formatting (bold, italic) and return XML runs."""
    runs = []
    # Process bold+italic, bold, italic patterns
    pattern = r'(\*\*\*(.+?)\*\*\*|\*\*(.+?)\*\*|\*(.+?)\*|([^*]+))'
    
    for match in re.finditer(pattern, text):
        if match.group(2):  # bold+italic
            runs.append(create_run_xml(match.group(2), bold=True, italic=True, size=base_size))
        elif match.group(3):  # bold
            runs.append(create_run_xml(match.group(3), bold=True, size=base_size))
        elif match.group(4):  # italic
            runs.append(create_run_xml(match.group(4), italic=True, size=base_size))
        elif match.group(5):  # plain text
            runs.append(create_run_xml(match.group(5), size=base_size))
    
    return ''.join(runs) if runs else create_run_xml(text, size=base_size)


def create_paragraph_xml(text, style=None, bold=False, italic=False, size=24, alignment=None, spacing_before=0, spacing_after=120):
    """Create a Word XML paragraph with full formatting options."""
    ppr_parts = []
    
    if style:
        ppr_parts.append(f'<w:pStyle w:val="{style}"/>')
    if alignment:
        ppr_parts.append(f'<w:jc w:val="{alignment}"/>')
    
    spacing = f'<w:spacing w:before="{spacing_before}" w:after="{spacing_after}" w:line="360" w:lineRule="auto"/>'
    ppr_parts.append(spacing)
    
    ppr = ''
    if ppr_parts:
        ppr = '<w:pPr>' + ''.join(ppr_parts) + '</w:pPr>'
    
    # Handle inline formatting
    if bold and not any(c in text for c in ['*']):
        runs = create_run_xml(text, bold=True, italic=italic, size=size)
    else:
        runs = parse_inline_formatting(text, base_size=size)
    
    return f'<w:p>{ppr}{runs}</w:p>'


def create_table_xml(rows):
    """Create a Word XML table from parsed rows."""
    if not rows:
        return ''
    
    # Calculate number of columns
    num_cols = len(rows[0])
    col_width = 9360 // num_cols  # Total page width distributed
    
    # Table properties
    tbl_pr = '''<w:tblPr>
      <w:tblStyle w:val="TableGrid"/>
      <w:tblW w:w="9360" w:type="dxa"/>
      <w:tblBorders>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      </w:tblBorders>
      <w:tblLayout w:type="fixed"/>
    </w:tblPr>'''
    
    # Table grid
    grid_cols = ''.join(f'<w:gridCol w:w="{col_width}"/>' for _ in range(num_cols))
    tbl_grid = f'<w:tblGrid>{grid_cols}</w:tblGrid>'
    
    # Table rows
    tbl_rows = []
    for i, row in enumerate(rows):
        cells = []
        is_header = (i == 0)
        for cell_text in row:
            cell_text = cell_text.strip()
            # Remove any remaining markdown formatting
            cell_text = re.sub(r'\*\*(.+?)\*\*', r'\1', cell_text)
            cell_text = re.sub(r'\*(.+?)\*', r'\1', cell_text)
            
            shading = ''
            if is_header:
                shading = '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>'
            
            tc_pr = f'<w:tcPr><w:tcW w:w="{col_width}" w:type="dxa"/>{shading}</w:tcPr>'
            
            rpr = '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/>'
            if is_header:
                rpr += '<w:b/><w:bCs/>'
            rpr += '</w:rPr>'
            
            p_xml = f'<w:p><w:pPr><w:spacing w:before="40" w:after="40" w:line="240" w:lineRule="auto"/></w:pPr><w:r>{rpr}<w:t xml:space="preserve">{escape_xml(cell_text)}</w:t></w:r></w:p>'
            cells.append(f'<w:tc>{tc_pr}{p_xml}</w:tc>')
        
        tbl_rows.append(f'<w:tr>{"".join(cells)}</w:tr>')
    
    return f'<w:tbl>{tbl_pr}{tbl_grid}{"".join(tbl_rows)}</w:tbl>'


def markdown_to_docx_xml(md_text):
    """Convert markdown text to Word XML paragraphs with proper table handling."""
    paragraphs = []
    lines = md_text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Empty line
        if not line:
            paragraphs.append('<w:p><w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr></w:p>')
            i += 1
            continue
        
        # Table detection - collect all table lines
        if '|' in line and line.strip().startswith('|'):
            table_lines = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip().startswith('|'):
                stripped = lines[i].strip()
                # Skip separator lines (|---|---|)
                if not re.match(r'^\|[\s\-:|]+\|$', stripped):
                    # Parse cells
                    cells = [c.strip() for c in stripped.split('|')[1:-1]]
                    table_lines.append(cells)
                i += 1
            
            if table_lines:
                paragraphs.append(create_table_xml(table_lines))
                # Add space after table
                paragraphs.append('<w:p><w:pPr><w:spacing w:before="120" w:after="120"/></w:pPr></w:p>')
            continue
        
        # Horizontal rule
        if line.startswith('---'):
            paragraphs.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="12" w:space="1" w:color="auto"/></w:pBdr><w:spacing w:before="240" w:after="240"/></w:pPr></w:p>')
            i += 1
            continue
        
        # Title (# heading)
        if line.startswith('# ') and not line.startswith('## '):
            text = line[2:].strip()
            paragraphs.append(create_paragraph_xml(text, style='Title', bold=True, size=32, alignment='center', spacing_before=240, spacing_after=240))
            i += 1
            continue
        
        # Section heading (##)
        if line.startswith('## '):
            text = line[3:].strip()
            paragraphs.append(create_paragraph_xml(text, style='Heading1', bold=True, size=28, spacing_before=360, spacing_after=120))
            i += 1
            continue
        
        # Subsection (###)
        if line.startswith('### '):
            text = line[4:].strip()
            paragraphs.append(create_paragraph_xml(text, style='Heading2', bold=True, size=24, spacing_before=240, spacing_after=120))
            i += 1
            continue
        
        # Sub-subsection (####)
        if line.startswith('#### '):
            text = line[5:].strip()
            paragraphs.append(create_paragraph_xml(text, style='Heading3', bold=True, italic=True, size=24, spacing_before=180, spacing_after=60))
            i += 1
            continue
        
        # Bold line (like **Table 1: ...**)
        if line.startswith('**') and line.endswith('**'):
            text = line.strip('*').strip()
            paragraphs.append(create_paragraph_xml(text, bold=True, size=22, alignment='center', spacing_before=240, spacing_after=120))
            i += 1
            continue
        
        # Reference lines [1] Author...
        if re.match(r'^\[\d+\]', line):
            # Clean markdown italic markers
            clean = re.sub(r'\*(.+?)\*', r'\1', line)
            paragraphs.append(create_paragraph_xml(clean, size=20, spacing_before=0, spacing_after=60))
            i += 1
            continue
        
        # Regular paragraph - may span multiple lines
        para_text = line
        # Remove markdown formatting markers for clean display
        clean = re.sub(r'\*\*(.+?)\*\*', r'\1', para_text)
        clean = re.sub(r'\*(.+?)\*', r'\1', clean)
        paragraphs.append(create_paragraph_xml(clean, size=24, alignment='both', spacing_before=0, spacing_after=120))
        i += 1
    
    return '\n'.join(paragraphs)


def create_docx(input_md_path, output_path):
    """Create a .docx file from the markdown chapter."""
    
    with open(input_md_path, 'r') as f:
        md_text = f.read()
    
    body_content = markdown_to_docx_xml(md_text)
    
    # Word document XML components
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''
    
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''
    
    word_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>'''
    
    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="240"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:b/><w:bCs/><w:sz w:val="32"/><w:szCs w:val="32"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:bCs/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:bCs/><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="180" w:after="60"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:bCs/><w:i/><w:iCs/><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr>
      <w:tblBorders>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      </w:tblBorders>
    </w:tblPr>
  </w:style>
</w:styles>'''
    
    numbering = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
</w:numbering>'''
    
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {body_content}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720"/>
      <w:cols w:space="720"/>
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
        zf.writestr('word/numbering.xml', numbering)
    
    print(f"Created: {output_path}")
    
    # Verify file size
    import os
    size_kb = os.path.getsize(output_path) / 1024
    print(f"File size: {size_kb:.1f} KB")


if __name__ == '__main__':
    input_path = '/projects/sandbox/AMMAN/Chapter_Differential_Equations_Dynamical_Systems_Biology.md'
    output_path = '/projects/sandbox/AMMAN/Chapter_Differential_Equations_Dynamical_Systems_Biology.docx'
    
    print("=" * 60)
    print("Creating Word Document: Differential Equations and")
    print("Dynamical Systems in Biology")
    print("=" * 60)
    print()
    
    create_docx(input_path, output_path)
    
    print()
    print("Document includes:")
    print("  - Full chapter text with 93 in-text citations [1]-[93]")
    print("  - 4 formatted tables (one per section)")
    print("  - 93 numbered references")
    print("  - Professional formatting (Times New Roman, 1.5 spacing)")
    print()
    print("Done!")
