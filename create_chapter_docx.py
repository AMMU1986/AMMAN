#!/usr/bin/env python3
"""
Create a Word (.docx) document for the Agricultural Tourism chapter
using only Python standard library (zipfile + XML).
"""
import zipfile
import os
import re

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "Chapter_Agricultural_Tourism_Regenerative_Farming.docx")

# Read the markdown source
MD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "Chapter_Agricultural_Tourism_Regenerative_Farming.md")

def escape_xml(text):
    """Escape XML special characters."""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    return text

def make_paragraph(text, style="Normal", bold=False, italic=False, font_size=24):
    """Create a Word XML paragraph. font_size is in half-points (24 = 12pt)."""
    rpr = ""
    if bold:
        rpr += "<w:b/>"
    if italic:
        rpr += "<w:i/>"
    if font_size != 24:
        rpr += f'<w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/>'
    if rpr:
        rpr = f"<w:rPr>{rpr}</w:rPr>"

    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>'

    # Handle bold fragments within text (e.g. **text**)
    escaped = escape_xml(text)

    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{escaped}</w:t></w:r></w:p>'

def make_heading(text, level=1):
    """Create a heading paragraph."""
    style = f"Heading{level}"
    sizes = {1: 36, 2: 32, 3: 28, 4: 26}
    fs = sizes.get(level, 24)
    return make_paragraph(text, style=style, bold=True, font_size=fs)

def make_table_row(cells, is_header=False):
    """Create a table row."""
    row_xml = "<w:tr>"
    if is_header:
        row_xml += "<w:trPr><w:tblHeader/></w:trPr>"
    for cell in cells:
        bold_tag = "<w:b/>" if is_header else ""
        rpr = f"<w:rPr>{bold_tag}<w:sz w:val='20'/><w:szCs w:val='20'/></w:rPr>" if bold_tag else "<w:rPr><w:sz w:val='20'/><w:szCs w:val='20'/></w:rPr>"
        cell_text = escape_xml(cell.strip())
        row_xml += f'''<w:tc>
          <w:tcPr><w:tcW w:w="0" w:type="auto"/></w:tcPr>
          <w:p><w:pPr><w:pStyle w:val="Normal"/></w:pPr>
          <w:r>{rpr}<w:t xml:space="preserve">{cell_text}</w:t></w:r></w:p>
        </w:tc>'''
    row_xml += "</w:tr>"
    return row_xml

def make_table(rows):
    """Create a table from list of rows (first row = header)."""
    if not rows:
        return ""
    ncols = len(rows[0])
    col_width = 9000 // ncols
    grid = "".join(f'<w:gridCol w:w="{col_width}"/>' for _ in range(ncols))

    table_xml = f'''<w:tbl>
      <w:tblPr>
        <w:tblStyle w:val="TableGrid"/>
        <w:tblW w:w="9000" w:type="dxa"/>
        <w:tblBorders>
          <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        </w:tblBorders>
        <w:tblLayout w:type="autofit"/>
      </w:tblPr>
      <w:tblGrid>{grid}</w:tblGrid>'''

    for i, row in enumerate(rows):
        table_xml += make_table_row(row, is_header=(i == 0))
    table_xml += "</w:tbl>"
    return table_xml

def parse_markdown_to_docx_body(md_text):
    """Parse markdown and convert to Word XML body content."""
    body_content = []
    lines = md_text.split('\n')
    i = 0
    in_table = False
    table_rows = []

    while i < len(lines):
        line = lines[i]

        # Skip image links (we reference them as text)
        if line.startswith('!['):
            # Extract caption from next lines if present
            i += 1
            continue

        # Horizontal rules
        if line.strip() == '---':
            body_content.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="1" w:color="auto"/></w:pBdr></w:pPr></w:p>')
            i += 1
            continue

        # Table detection
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_rows = []
            # Parse cells
            cells = [c.strip() for c in line.split('|')[1:-1]]
            # Skip separator rows (e.g., |:---|:---|)
            if cells and all(re.match(r'^[-:]+$', c) for c in cells):
                i += 1
                continue
            if cells:
                table_rows.append(cells)
            i += 1
            continue
        elif in_table:
            # End of table
            in_table = False
            if table_rows:
                body_content.append(make_table(table_rows))
                body_content.append(make_paragraph("", font_size=20))  # spacing
            table_rows = []

        # Headings
        if line.startswith('# '):
            text = line[2:].strip()
            body_content.append(make_heading(text, 1))
            i += 1
            continue
        elif line.startswith('## '):
            text = line[3:].strip()
            body_content.append(make_heading(text, 2))
            i += 1
            continue
        elif line.startswith('### '):
            text = line[4:].strip()
            body_content.append(make_heading(text, 3))
            i += 1
            continue
        elif line.startswith('#### '):
            text = line[5:].strip()
            body_content.append(make_heading(text, 4))
            i += 1
            continue

        # Bold/Keywords line
        if line.startswith('**Keywords:'):
            clean = line.replace('**', '')
            body_content.append(make_paragraph(clean, italic=True, font_size=22))
            i += 1
            continue

        # List items
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            text = line.strip()[2:]
            # Clean markdown formatting
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
            body_content.append(make_paragraph(f"  \u2022 {text}", font_size=22))
            i += 1
            continue

        # Numbered list
        num_match = re.match(r'^(\d+)\.\s+', line.strip())
        if num_match:
            text = line.strip()[len(num_match.group(0)):]
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
            body_content.append(make_paragraph(f"  {num_match.group(1)}. {text}", font_size=22))
            i += 1
            continue

        # Empty line
        if line.strip() == '':
            body_content.append(make_paragraph("", font_size=10))
            i += 1
            continue

        # Regular paragraph
        text = line.strip()
        # Clean markdown bold/italic
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        if text:
            body_content.append(make_paragraph(text, font_size=22))

        i += 1

    # Flush remaining table
    if in_table and table_rows:
        body_content.append(make_table(table_rows))

    return '\n'.join(body_content)

def create_docx(body_xml, output_path):
    """Create a complete .docx file."""

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
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
    <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="360" w:after="200"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="36"/><w:szCs w:val="36"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="280" w:after="160"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading4">
    <w:name w:val="heading 4"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:i/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
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

    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
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

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', styles)

    print(f"Word document created: {output_path}")
    print(f"File size: {os.path.getsize(output_path):,} bytes")

if __name__ == "__main__":
    print("Reading markdown source...")
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        md_text = f.read()

    print("Converting to Word XML...")
    body_xml = parse_markdown_to_docx_body(md_text)

    print("Creating .docx file...")
    create_docx(body_xml, OUTPUT_PATH)
    print("Done!")
