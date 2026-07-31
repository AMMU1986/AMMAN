"""
Create a Word .docx file from scratch using only Python's built-in zipfile module.
A .docx file is an Open XML Format zip archive containing XML documents.
"""
import zipfile
import os
import re

# Read the markdown source
with open('/projects/sandbox/chapter_accreditation.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# ============================================================
# XML Templates for .docx
# ============================================================

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

WORD_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="200" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="0" w:after="300"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="36"/><w:szCs w:val="36"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="200"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:i/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="120" w:after="240"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableHeader">
    <w:name w:val="Table Header"/>
    <w:basedOn w:val="Normal"/>
    <w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCell">
    <w:name w:val="Table Cell"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Abstract">
    <w:name w:val="Abstract"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="120" w:after="120"/><w:ind w:left="720" w:right="720"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
</w:styles>'''

NUMBERING = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
</w:numbering>'''


def escape_xml(text):
    """Escape XML special characters."""
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
    # Process bold+italic (***text***), bold (**text**), italic (*text*)
    pattern = r'(\*\*\*(.+?)\*\*\*|\*\*(.+?)\*\*|\*(.+?)\*)'
    last_end = 0
    for m in re.finditer(pattern, text):
        # Add plain text before match
        if m.start() > last_end:
            plain = text[last_end:m.start()]
            if plain:
                runs.append(make_run(plain))
        if m.group(2):  # bold+italic
            runs.append(make_run(m.group(2), bold=True, italic=True))
        elif m.group(3):  # bold
            runs.append(make_run(m.group(3), bold=True))
        elif m.group(4):  # italic
            runs.append(make_run(m.group(4), italic=True))
        last_end = m.end()
    # Remaining text
    if last_end < len(text):
        remaining = text[last_end:]
        if remaining:
            runs.append(make_run(remaining))
    if not runs:
        runs.append(make_run(text))
    return ''.join(runs)


def make_paragraph(text, style='Normal'):
    """Create a paragraph with a given style."""
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
    runs = parse_inline(text)
    return f'<w:p>{ppr}{runs}</w:p>'


def make_table(headers, rows):
    """Create a table in Word XML."""
    # Table properties
    tbl_pr = '''<w:tblPr>
      <w:tblStyle w:val="TableGrid"/>
      <w:tblW w:w="9500" w:type="dxa"/>
      <w:tblBorders>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      </w:tblBorders>
      <w:tblLook w:val="04A0"/>
    </w:tblPr>'''

    # Calculate column width
    num_cols = len(headers)
    col_width = 9500 // num_cols

    # Grid
    grid = '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{col_width}"/>' for _ in headers) + '</w:tblGrid>'

    # Header row
    header_cells = ''
    for h in headers:
        header_cells += f'''<w:tc>
          <w:tcPr><w:tcW w:w="{col_width}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>
          <w:p><w:pPr><w:pStyle w:val="TableCell"/></w:pPr><w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{escape_xml(h)}</w:t></w:r></w:p>
        </w:tc>'''
    header_row = f'<w:tr>{header_cells}</w:tr>'

    # Data rows
    data_rows = ''
    for row in rows:
        cells = ''
        for cell in row:
            cells += f'''<w:tc>
              <w:tcPr><w:tcW w:w="{col_width}" w:type="dxa"/></w:tcPr>
              <w:p><w:pPr><w:pStyle w:val="TableCell"/></w:pPr><w:r><w:t xml:space="preserve">{escape_xml(cell)}</w:t></w:r></w:p>
            </w:tc>'''
        data_rows += f'<w:tr>{cells}</w:tr>'

    return f'<w:tbl>{tbl_pr}{grid}{header_row}{data_rows}</w:tbl>'


def parse_table_from_md(lines):
    """Parse a markdown table into headers and rows."""
    headers = [cell.strip() for cell in lines[0].split('|')[1:-1]]
    # Skip separator line (lines[1])
    rows = []
    for line in lines[2:]:
        row = [cell.strip() for cell in line.split('|')[1:-1]]
        rows.append(row)
    return headers, rows


def convert_md_to_paragraphs(md_text):
    """Convert markdown text to list of Word XML paragraph elements."""
    paragraphs = []
    lines = md_text.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line.strip():
            i += 1
            continue

        # Title (# )
        if line.startswith('# '):
            paragraphs.append(make_paragraph(line[2:].strip(), 'Title'))
            i += 1
            continue

        # Heading 1 (## )
        if line.startswith('## '):
            paragraphs.append(make_paragraph(line[3:].strip(), 'Heading1'))
            i += 1
            continue

        # Heading 2 (### )
        if line.startswith('### '):
            paragraphs.append(make_paragraph(line[4:].strip(), 'Heading2'))
            i += 1
            continue

        # Heading 3 (#### )
        if line.startswith('#### '):
            paragraphs.append(make_paragraph(line[5:].strip(), 'Heading3'))
            i += 1
            continue

        # Table detection
        if '|' in line and i + 1 < len(lines) and re.match(r'\s*\|[\s\-:|]+\|', lines[i + 1]):
            table_lines = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                table_lines.append(lines[i])
                i += 1
            headers, rows = parse_table_from_md(table_lines)
            paragraphs.append(make_table(headers, rows))
            # Add spacing after table
            paragraphs.append('<w:p><w:pPr><w:pStyle w:val="Normal"/></w:pPr></w:p>')
            continue

        # Figure caption (starts with **Figure)
        if line.strip().startswith('**Figure'):
            # Clean markdown bold markers
            clean = line.strip().replace('**', '')
            paragraphs.append(make_paragraph(clean, 'FigureCaption'))
            i += 1
            continue

        # Figure description in brackets
        if line.strip().startswith('[Figure'):
            # This is a figure description - render as italic caption
            clean = line.strip()
            paragraphs.append(make_paragraph(clean, 'FigureCaption'))
            i += 1
            continue

        # Bold paragraph header (like **Keywords:**)
        if line.strip().startswith('**') and '**' in line.strip()[2:]:
            clean = line.strip().replace('**', '')
            paragraphs.append(make_paragraph(clean, 'Normal'))
            i += 1
            continue

        # Normal paragraph
        paragraphs.append(make_paragraph(line.strip(), 'Normal'))
        i += 1

    return paragraphs


# ============================================================
# Build document
# ============================================================

paragraphs = convert_md_to_paragraphs(md_content)

# Assemble document.xml
doc_body = ''.join(paragraphs)

DOCUMENT = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {doc_body}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720"/>
    </w:sectPr>
  </w:body>
</w:document>'''

# ============================================================
# Write .docx zip file
# ============================================================

output_path = '/projects/sandbox/Accreditation_Chapter.docx'

with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('[Content_Types].xml', CONTENT_TYPES)
    zf.writestr('_rels/.rels', RELS)
    zf.writestr('word/_rels/document.xml.rels', WORD_RELS)
    zf.writestr('word/document.xml', DOCUMENT)
    zf.writestr('word/styles.xml', STYLES)
    zf.writestr('word/numbering.xml', NUMBERING)

print(f"Word file created: {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")
