#!/usr/bin/env python3
"""
Create a Word .docx file from the AI for Electric Vehicles chapter markdown.
Uses raw XML generation since python-docx is not available in this environment.
"""

import zipfile
import os
import re


def escape_xml(text):
    """Escape special XML characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text


def make_run(text, bold=False, italic=False):
    """Create a single run element."""
    rpr = ''
    if bold or italic:
        parts = []
        if bold:
            parts.append('<w:b/>')
        if italic:
            parts.append('<w:i/>')
        rpr = '<w:rPr>' + ''.join(parts) + '</w:rPr>'
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'


def parse_inline(text):
    """Parse bold (**) markers in text and return runs."""
    runs = ''
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            inner = part[2:-2]
            runs += make_run(inner, bold=True)
        else:
            if part:
                runs += make_run(part)
    return runs


def make_paragraph(text, style=None, bold=False, italic=False, alignment=None):
    """Create a Word XML paragraph."""
    ppr_parts = []
    if style:
        ppr_parts.append(f'<w:pStyle w:val="{style}"/>')
    if alignment:
        ppr_parts.append(f'<w:jc w:val="{alignment}"/>')
    
    ppr = ''
    if ppr_parts:
        ppr = '<w:pPr>' + ''.join(ppr_parts) + '</w:pPr>'
    
    if bold or italic:
        runs = make_run(text, bold=bold, italic=italic)
    else:
        runs = parse_inline(text)
    
    return f'<w:p>{ppr}{runs}</w:p>'


def make_table(headers, rows):
    """Create a Word XML table."""
    num_cols = len(headers)
    col_width = 9360 // num_cols  # distribute across page width
    
    tbl_grid = '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{col_width}"/>' for _ in range(num_cols)) + '</w:tblGrid>'
    
    table_xml = '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="9360" w:type="dxa"/>'
    table_xml += '<w:tblBorders>'
    table_xml += '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    table_xml += '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    table_xml += '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    table_xml += '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    table_xml += '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    table_xml += '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    table_xml += '</w:tblBorders>'
    table_xml += '</w:tblPr>'
    table_xml += tbl_grid

    # Header row
    table_xml += '<w:tr>'
    for h in headers:
        cell_text = escape_xml(h.strip())
        table_xml += f'<w:tc><w:tcPr><w:tcW w:w="{col_width}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>'
        table_xml += f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{cell_text}</w:t></w:r></w:p></w:tc>'
    table_xml += '</w:tr>'

    # Data rows
    for row in rows:
        table_xml += '<w:tr>'
        for idx, cell in enumerate(row):
            cell_text = escape_xml(cell.strip())
            table_xml += f'<w:tc><w:tcPr><w:tcW w:w="{col_width}" w:type="dxa"/></w:tcPr>'
            table_xml += f'<w:p><w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{cell_text}</w:t></w:r></w:p></w:tc>'
        table_xml += '</w:tr>'

    table_xml += '</w:tbl>'
    return table_xml


# Read the markdown file
with open('/projects/sandbox/AMMAN/Chapter_AI_Electric_Vehicles_Charging_Infrastructure.md', 'r') as f:
    md_content = f.read()

# Parse markdown and convert to document XML
body_content = ''
lines = md_content.split('\n')
i = 0
in_table = False
table_headers = []
table_rows = []

while i < len(lines):
    line = lines[i]

    # Handle table start
    if line.startswith('|') and not in_table:
        in_table = True
        table_headers = [c for c in line.split('|')[1:-1]]
        i += 1
        # Skip separator line
        if i < len(lines) and re.match(r'\|[\s\-|]+\|', lines[i]):
            i += 1
        table_rows = []
        continue
    elif in_table and line.startswith('|'):
        table_rows.append([c for c in line.split('|')[1:-1]])
        i += 1
        continue
    elif in_table and not line.startswith('|'):
        body_content += make_table(table_headers, table_rows)
        body_content += '<w:p/>'
        in_table = False
        table_headers = []
        table_rows = []
        # Don't increment, process current line

    # Title
    if line.startswith('# ') and not line.startswith('## '):
        title_text = line[2:].strip()
        body_content += make_paragraph(title_text, style='Title', bold=True, alignment='center')
    # Heading 1
    elif line.startswith('## '):
        body_content += make_paragraph(line[3:].strip(), style='Heading1', bold=True)
    # Heading 2
    elif line.startswith('### '):
        body_content += make_paragraph(line[4:].strip(), style='Heading2', bold=True)
    # Heading 3
    elif line.startswith('#### '):
        body_content += make_paragraph(line[5:].strip(), style='Heading3', bold=True)
    # Empty line
    elif line.strip() == '':
        body_content += '<w:p/>'
    # Figure caption (bold italic)
    elif line.startswith('**Figure'):
        caption = line.strip('*').strip()
        body_content += make_paragraph(caption, bold=True, italic=True, alignment='center')
    # Table caption (bold)
    elif line.startswith('**Table'):
        caption = line.strip('*').strip()
        body_content += make_paragraph(caption, bold=True, alignment='center')
    # Keywords line
    elif line.startswith('**Keywords:'):
        body_content += make_paragraph(line)
    # Normal paragraph
    else:
        body_content += make_paragraph(line)

    i += 1

# Handle any remaining table
if in_table:
    body_content += make_table(table_headers, table_rows)

# Document XML
document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
            xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
            xmlns:o="urn:schemas-microsoft-com:office:office"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
            xmlns:v="urn:schemas-microsoft-com:vml"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:w10="urn:schemas-microsoft-com:office:word"
            xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
            xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
            xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
            xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
            xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
            mc:Ignorable="w14 wp14">
<w:body>
{body_content}
<w:sectPr>
<w:pgSz w:w="12240" w:h="15840"/>
<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
<w:cols w:space="720"/>
</w:sectPr>
</w:body>
</w:document>'''

# Styles XML
styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults>
<w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault>
</w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal">
<w:name w:val="Normal"/>
<w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
</w:style>
<w:style w:type="paragraph" w:styleId="Title">
<w:name w:val="Title"/>
<w:pPr><w:jc w:val="center"/><w:spacing w:before="240" w:after="360"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
</w:style>
<w:style w:type="paragraph" w:styleId="Heading1">
<w:name w:val="heading 1"/>
<w:pPr><w:spacing w:before="360" w:after="120"/><w:keepNext/></w:pPr>
<w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
</w:style>
<w:style w:type="paragraph" w:styleId="Heading2">
<w:name w:val="heading 2"/>
<w:pPr><w:spacing w:before="240" w:after="120"/><w:keepNext/></w:pPr>
<w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
</w:style>
<w:style w:type="paragraph" w:styleId="Heading3">
<w:name w:val="heading 3"/>
<w:pPr><w:spacing w:before="200" w:after="80"/><w:keepNext/></w:pPr>
<w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
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

# Content Types
content_types_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

# Relationships
rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

word_rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

# Create the .docx file
output_path = '/projects/sandbox/AMMAN/Chapter_AI_Electric_Vehicles_Charging_Infrastructure.docx'
with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('[Content_Types].xml', content_types_xml)
    zf.writestr('_rels/.rels', rels_xml)
    zf.writestr('word/document.xml', document_xml)
    zf.writestr('word/styles.xml', styles_xml)
    zf.writestr('word/_rels/document.xml.rels', word_rels_xml)

file_size = os.path.getsize(output_path)
print(f"Word document created successfully: {output_path}")
print(f"File size: {file_size / 1024:.1f} KB")
