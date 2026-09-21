#!/usr/bin/env python3
"""
Create a Word document (.docx) from the thermal-modelling manuscript markdown file.

Converts Manuscript_Thermal_Modelling_ToolChip_Temperature.md into a formatted
.docx using only the Python standard library (no external dependencies).

Supports: title (#), section headings (##), subsection headings (###),
markdown tables (rendered as real Word tables), bold/italic inline markers,
and normal justified body paragraphs in Times New Roman.
"""

import zipfile
import re

SRC_MD = '/projects/sandbox/AMMAN/Manuscript_Thermal_Modelling_ToolChip_Temperature.md'
OUT_DOCX = '/projects/sandbox/AMMAN/Manuscript_Thermal_Modelling_ToolChip_Temperature.docx'


def escape_xml(text):
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))


def strip_inline_md(text):
    """Remove markdown emphasis markers, keeping the text."""
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    return text


def para(text, style='Normal', bold=False, size=None):
    """Build a Word paragraph XML string."""
    text = escape_xml(strip_inline_md(text))

    run_props = []
    if bold:
        run_props.append('<w:b/>')
    if size is not None:
        run_props.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    rpr = f'<w:rPr>{"".join(run_props)}</w:rPr>' if run_props else ''

    style_map = {
        'Title': '<w:pPr><w:pStyle w:val="Title"/><w:jc w:val="center"/></w:pPr>',
        'Heading1': '<w:pPr><w:pStyle w:val="Heading1"/></w:pPr>',
        'Heading2': '<w:pPr><w:pStyle w:val="Heading2"/></w:pPr>',
        'Heading3': '<w:pPr><w:pStyle w:val="Heading3"/></w:pPr>',
    }
    ppr = style_map.get(style, '')
    return (f'<w:p>{ppr}<w:r>{rpr}'
            f'<w:t xml:space="preserve">{text}</w:t></w:r></w:p>')


def table_cell(text, bold=False):
    text = escape_xml(strip_inline_md(text))
    rpr = '<w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>' if bold \
        else '<w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
    return ('<w:tc><w:tcPr><w:tcBorders>'
            '<w:top w:val="single" w:sz="4" w:color="808080"/>'
            '<w:left w:val="single" w:sz="4" w:color="808080"/>'
            '<w:bottom w:val="single" w:sz="4" w:color="808080"/>'
            '<w:right w:val="single" w:sz="4" w:color="808080"/>'
            '</w:tcBorders></w:tcPr>'
            f'<w:p><w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r></w:p></w:tc>')


def build_table(rows):
    """rows: list of lists of cell strings. First row treated as header."""
    out = ['<w:tbl><w:tblPr>'
           '<w:tblStyle w:val="TableGrid"/>'
           '<w:tblW w:w="0" w:type="auto"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:color="808080"/>'
           '<w:left w:val="single" w:sz="4" w:color="808080"/>'
           '<w:bottom w:val="single" w:sz="4" w:color="808080"/>'
           '<w:right w:val="single" w:sz="4" w:color="808080"/>'
           '<w:insideH w:val="single" w:sz="4" w:color="808080"/>'
           '<w:insideV w:val="single" w:sz="4" w:color="808080"/>'
           '</w:tblBorders></w:tblPr>']
    for i, row in enumerate(rows):
        out.append('<w:tr>')
        for cell in row:
            out.append(table_cell(cell, bold=(i == 0)))
        out.append('</w:tr>')
    out.append('</w:tbl>')
    out.append('<w:p/>')  # spacer after table
    return ''.join(out)


def parse_table_line(line):
    parts = [p.strip() for p in line.strip().strip('|').split('|')]
    return parts


def markdown_to_body(md_text):
    paragraphs = []
    lines = md_text.split('\n')
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip()

        # Table block
        if line.strip().startswith('|') and '|' in line.strip()[1:]:
            table_rows = []
            while i < n and lines[i].strip().startswith('|'):
                l = lines[i].strip()
                if re.match(r'^\|[\s\-:|]+\|?$', l):  # separator row
                    i += 1
                    continue
                table_rows.append(parse_table_line(l))
                i += 1
            if table_rows:
                paragraphs.append(build_table(table_rows))
            continue

        if not line:
            paragraphs.append('<w:p/>')
            i += 1
            continue

        if line.startswith('# ') and not line.startswith('## '):
            paragraphs.append(para(line[2:].strip(), style='Title', bold=True, size=32))
        elif line.startswith('## '):
            paragraphs.append(para(line[3:].strip(), style='Heading1', bold=True, size=28))
        elif line.startswith('### '):
            paragraphs.append(para(line[4:].strip(), style='Heading2', bold=True, size=24))
        elif line.startswith('#### '):
            paragraphs.append(para(line[5:].strip(), style='Heading3', bold=True, size=22))
        elif line.startswith('---'):
            paragraphs.append('<w:p/>')
        elif line.strip().startswith('**') and line.strip().endswith('**') and line.count('**') == 2:
            paragraphs.append(para(line.strip().strip('*').strip(), bold=True))
        elif line.strip().startswith(('- ', '* ')):
            paragraphs.append(para('\u2022  ' + line.strip()[2:], size=24))
        elif re.match(r'^\d+\.\s', line.strip()):
            paragraphs.append(para(line.strip(), size=24))
        else:
            paragraphs.append(para(line))
        i += 1

    return '\n'.join(paragraphs)


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
    <w:rPr><w:b/><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="120" w:after="60"/></w:pPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
  </w:style>
</w:styles>'''


def create_docx():
    with open(SRC_MD, 'r', encoding='utf-8') as f:
        md_text = f.read()

    body = markdown_to_body(md_text)

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<w:body>'
        f'{body}'
        '<w:sectPr>'
        '<w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
        '</w:sectPr>'
        '</w:body></w:document>'
    )

    with zipfile.ZipFile(OUT_DOCX, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', WORD_RELS)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)

    print(f'Created {OUT_DOCX}')


if __name__ == '__main__':
    create_docx()
