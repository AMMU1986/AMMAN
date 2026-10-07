#!/usr/bin/env python3
"""
Create a Word document (.docx) from the revised EMHD Carreau hybrid nanofluid
manuscript markdown file.

Uses only the Python standard library (zipfile for the OOXML package). Unlike the
earlier chapter scripts, this converter renders real Word tables and handles
inline bold, headings, image placeholders and horizontal rules.
"""

import zipfile
import re

SRC = '/projects/sandbox/AMMAN/Manuscript_EMHD_Carreau_Hybrid_Nanofluid.md'
OUT = '/projects/sandbox/AMMAN/Manuscript_EMHD_Carreau_Hybrid_Nanofluid.docx'


def escape_xml(text):
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))


def runs_from_inline(text):
    """Convert a line with **bold** markers into a sequence of Word runs."""
    # Normalise a few unicode/markdown artefacts
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    runs = []
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            inner = escape_xml(part[2:-2])
            runs.append(f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{inner}</w:t></w:r>')
        else:
            runs.append(f'<w:r><w:t xml:space="preserve">{escape_xml(part)}</w:t></w:r>')
    return ''.join(runs) if runs else '<w:r><w:t xml:space="preserve"></w:t></w:r>'


def para(text, style=None):
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ''
    return f'<w:p>{ppr}{runs_from_inline(text)}</w:p>'


def empty_para():
    return '<w:p/>'


def table_xml(rows):
    """rows: list of list[str]. First row treated as header (bold, shaded)."""
    ncol = max(len(r) for r in rows)
    grid = ''.join('<w:gridCol w:w="%d"/>' % (9000 // ncol) for _ in range(ncol))

    def cell(text, header=False):
        shade = '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>' if header else ''
        tcpr = (f'<w:tcPr><w:tcBorders>'
                f'<w:top w:val="single" w:sz="4" w:color="000000"/>'
                f'<w:bottom w:val="single" w:sz="4" w:color="000000"/>'
                f'<w:left w:val="single" w:sz="4" w:color="000000"/>'
                f'<w:right w:val="single" w:sz="4" w:color="000000"/>'
                f'</w:tcBorders>{shade}</w:tcPr>')
        rpr = '<w:rPr><w:b/></w:rPr>' if header else ''
        return (f'<w:tc>{tcpr}<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>'
                f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r></w:p></w:tc>')

    body = ''
    for i, row in enumerate(rows):
        cells = row + [''] * (ncol - len(row))
        body += '<w:tr>' + ''.join(cell(c, header=(i == 0)) for c in cells) + '</w:tr>'

    return (f'<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
            f'<w:tblW w:w="0" w:type="auto"/>'
            f'<w:tblBorders>'
            f'<w:top w:val="single" w:sz="4" w:color="000000"/>'
            f'<w:bottom w:val="single" w:sz="4" w:color="000000"/>'
            f'<w:left w:val="single" w:sz="4" w:color="000000"/>'
            f'<w:right w:val="single" w:sz="4" w:color="000000"/>'
            f'<w:insideH w:val="single" w:sz="4" w:color="000000"/>'
            f'<w:insideV w:val="single" w:sz="4" w:color="000000"/>'
            f'</w:tblBorders></w:tblPr>'
            f'<w:tblGrid>{grid}</w:tblGrid>{body}</w:tbl>')


def split_table_row(line):
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    return cells


def is_separator(line):
    return bool(re.match(r'^\|[\s\-:|]+\|?$', line.strip()))


def convert(md):
    out = []
    lines = md.split('\n')
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip()

        # Blank line
        if not line:
            out.append(empty_para())
            i += 1
            continue

        # Table block
        if line.strip().startswith('|'):
            block = []
            while i < n and lines[i].strip().startswith('|'):
                if not is_separator(lines[i]):
                    block.append(split_table_row(lines[i]))
                i += 1
            if block:
                out.append(table_xml(block))
            continue

        # Horizontal rule
        if re.match(r'^-{3,}$', line.strip()):
            i += 1
            continue

        # Image -> caption placeholder paragraph
        m = re.match(r'^!\[.*?\]\((.*?)\)\s*$', line.strip())
        if m:
            out.append(para(f'[Figure placeholder: {m.group(1)}]'))
            i += 1
            continue

        # Headings
        if line.startswith('### '):
            out.append(para(line[4:].strip(), style='Heading2'))
        elif line.startswith('## '):
            out.append(para(line[3:].strip(), style='Heading1'))
        elif line.startswith('# '):
            out.append(para(line[2:].strip(), style='Title'))
        else:
            out.append(para(line))
        i += 1

    return '\n'.join(out)


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
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr><w:tblBorders>
      <w:top w:val="single" w:sz="4" w:color="000000"/>
      <w:left w:val="single" w:sz="4" w:color="000000"/>
      <w:bottom w:val="single" w:sz="4" w:color="000000"/>
      <w:right w:val="single" w:sz="4" w:color="000000"/>
      <w:insideH w:val="single" w:sz="4" w:color="000000"/>
      <w:insideV w:val="single" w:sz="4" w:color="000000"/>
    </w:tblBorders></w:tblPr>
  </w:style>
</w:styles>'''


def main():
    with open(SRC, 'r', encoding='utf-8') as f:
        md = f.read()

    body = convert(md)

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<w:body>'
        f'{body}'
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
        '</w:body></w:document>'
    )

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', WORD_RELS)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)

    print(f'Created {OUT}')


if __name__ == '__main__':
    main()
