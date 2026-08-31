#!/usr/bin/env python3
"""
Create a Word .docx file for Chapter 5 (Results and Discussion).

Uses raw OOXML (ZIP + XML) because python-docx / pandoc are not available in this
sandbox. This extends the converter used for the other chapters
(create_chapter_docx.py) to additionally handle:
    * fenced code blocks (``` ... ```) -> monospaced equation/reaction paragraphs
    * level-4 headings (##### )
    * bullet list items (- )
    * APA-style reference paragraphs (Author, Year) with a hanging indent
"""

import zipfile
import os
import re

# ─── OOXML boilerplate ───

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

NUMBERING = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="120" w:line="360" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
    <w:pPr><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading4">
    <w:name w:val="heading 4"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="160" w:after="80"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="References">
    <w:name w:val="References"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="240"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="Table Caption"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="120" w:after="60"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Equation">
    <w:name w:val="Equation"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="60" w:after="60"/><w:jc w:val="left"/><w:ind w:left="360"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ListBullet">
    <w:name w:val="List Bullet"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="720" w:hanging="360"/><w:spacing w:after="60"/><w:jc w:val="left"/></w:pPr>
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


def escape_xml(text):
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    return text


def make_run(text, bold=False, italic=False):
    props = []
    if bold:
        props.append('<w:b/>')
    if italic:
        props.append('<w:i/>')
    rpr = ('<w:rPr>' + ''.join(props) + '</w:rPr>') if props else ''
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'


def parse_inline(text):
    """Parse inline markdown (**bold** and *italic*) into runs."""
    runs = []
    pattern = r'(\*\*.*?\*\*|\*[^*]+?\*)'
    parts = re.split(pattern, text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            runs.append(make_run(part[2:-2], bold=True))
        elif part.startswith('*') and part.endswith('*'):
            runs.append(make_run(part[1:-1], italic=True))
        else:
            runs.append(make_run(part))
    return ''.join(runs)


def make_paragraph(text, style='Normal'):
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
    runs = parse_inline(text)
    return f'<w:p>{ppr}{runs}</w:p>'


def make_equation_block(code_lines):
    """Render a fenced code block as one monospaced paragraph with line breaks."""
    inner = []
    for j, ln in enumerate(code_lines):
        if j > 0:
            inner.append('<w:br/>')
        inner.append(f'<w:t xml:space="preserve">{escape_xml(ln)}</w:t>')
    ppr = '<w:pPr><w:pStyle w:val="Equation"/></w:pPr>'
    run = ('<w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>'
           '<w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>' + ''.join(inner) + '</w:r>')
    return f'<w:p>{ppr}{run}</w:p>'


def make_table(headers, rows):
    tbl = '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
    tbl += '<w:tblW w:w="9360" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
    tbl += '<w:tblBorders>'
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        tbl += f'<w:{edge} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '</w:tblBorders></w:tblPr>'

    n_cols = len(headers)
    col_w = 9360 // n_cols
    tbl += '<w:tblGrid>' + (f'<w:gridCol w:w="{col_w}"/>' * n_cols) + '</w:tblGrid>'

    # header
    tbl += '<w:tr>'
    for h in headers:
        tbl += '<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>'
        tbl += f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr>{make_run(h.strip(), bold=True)}</w:p></w:tc>'
    tbl += '</w:tr>'

    # data
    for row in rows:
        tbl += '<w:tr>'
        for cell in row:
            tbl += '<w:tc>'
            tbl += f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="40"/></w:pPr>{make_run(cell.strip())}</w:p>'
            tbl += '</w:tc>'
        for _ in range(n_cols - len(row)):
            tbl += '<w:tc><w:p/></w:tc>'
        tbl += '</w:tr>'

    tbl += '</w:tbl>'
    # spacer paragraph after table
    tbl += '<w:p/>'
    return tbl


def md_to_body(md_text):
    elements = []
    lines = md_text.split('\n')
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        if line.strip() == '---':
            i += 1
            continue

        # Fenced code block (equations / reactions)
        if line.strip().startswith('```'):
            i += 1
            code_lines = []
            while i < n and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            # strip trailing blank lines within the block
            while code_lines and not code_lines[-1].strip():
                code_lines.pop()
            elements.append(make_equation_block(code_lines))
            continue

        # Title (# )
        if line.startswith('# ') and not line.startswith('## '):
            elements.append(make_paragraph(line[2:].strip(), 'Title'))
            i += 1
            continue

        # Heading 1 (## )
        if line.startswith('## ') and not line.startswith('### '):
            elements.append(make_paragraph(line[3:].strip(), 'Heading1'))
            i += 1
            continue

        # Heading 2 (### )
        if line.startswith('### ') and not line.startswith('#### '):
            elements.append(make_paragraph(line[4:].strip(), 'Heading2'))
            i += 1
            continue

        # Heading 3 (#### )
        if line.startswith('#### ') and not line.startswith('##### '):
            elements.append(make_paragraph(line[5:].strip(), 'Heading3'))
            i += 1
            continue

        # Heading 4 (##### )
        if line.startswith('##### '):
            elements.append(make_paragraph(line[6:].strip(), 'Heading4'))
            i += 1
            continue

        # Table (header row followed by |---| separator)
        if '|' in line and i + 1 < n and re.search(r'\|?\s*:?-{2,}', lines[i + 1]) and '|' in lines[i + 1]:
            headers = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2  # skip header + separator
            rows = []
            while i < n and '|' in lines[i] and lines[i].strip():
                row = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                rows.append(row)
                i += 1
            elements.append(make_table(headers, rows))
            continue

        # Bold table caption (**Table ...**)
        if line.strip().startswith('**Table'):
            elements.append(make_paragraph(line.strip().strip('*'), 'TableCaption'))
            i += 1
            continue

        # Italic figure caption (*Figure ...* or *Fig. ...*)
        stripped = line.strip()
        if stripped.startswith('*') and stripped.endswith('*') and \
                re.match(r'\*(Figure|Fig\.)', stripped):
            elements.append(make_paragraph(stripped.strip('*'), 'FigureCaption'))
            i += 1
            continue

        # Italic note (*Note.* ...)
        if stripped.startswith('*Note.'):
            elements.append(make_paragraph(stripped.strip('*'), 'FigureCaption'))
            i += 1
            continue

        # Bullet list item
        if stripped.startswith('- '):
            elements.append(make_paragraph('\u2022  ' + stripped[2:].strip(), 'ListBullet'))
            i += 1
            continue

        # Numbered reference entry: "[12] Surname, X. ... (Year)."
        if re.match(r'^\[\d+\]\s', stripped):
            elements.append(make_paragraph(stripped, 'References'))
            i += 1
            continue

        # APA reference entry: "Surname, X. ... (Year)."  -> hanging indent
        if re.match(r'^[A-ZÀ-Þ][A-Za-zÀ-ÿ.\-\']+,\s', stripped) and re.search(r'\((?:19|20)\d{2}[a-z]?\)', stripped):
            elements.append(make_paragraph(stripped, 'References'))
            i += 1
            continue

        # Normal paragraph
        elements.append(make_paragraph(stripped, 'Normal'))
        i += 1

    return '\n'.join(elements)


def create_docx(md_filepath, output_filepath):
    with open(md_filepath, 'r', encoding='utf-8') as f:
        md_content = f.read()

    body_xml = md_to_body(md_content)

    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{body_xml}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"
               w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    with zipfile.ZipFile(output_filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', WORD_RELS)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES)
        zf.writestr('word/numbering.xml', NUMBERING)

    size_kb = os.path.getsize(output_filepath) / 1024
    print(f"Successfully created: {output_filepath}")
    print(f"File size: {size_kb:.1f} KB")


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md_file = os.path.join(script_dir, 'Chapter_5_Results_and_Discussion.md')
    docx_file = os.path.join(script_dir, 'Chapter_5_Results_and_Discussion.docx')
    create_docx(md_file, docx_file)
