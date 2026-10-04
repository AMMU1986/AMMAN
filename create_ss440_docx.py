#!/usr/bin/env python3
"""
Create a Word document (.docx) from the SS440 MIG welding manuscript markdown file.
Uses only the Python standard library (zipfile). Markdown tables are rendered as
native Word tables so that Table 1-3 are properly formatted.
"""

import zipfile
import re

SRC = '/projects/sandbox/AMMAN/Manuscript_SS440_MIG_Welding_Fillers.md'
OUT = '/projects/sandbox/AMMAN/Manuscript_SS440_MIG_Welding_Fillers.docx'


def escape_xml(text):
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))


def runs_from_inline(text):
    """Convert inline **bold** markers into Word runs. Returns XML of <w:r> runs."""
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    out = []
    for p in parts:
        if not p:
            continue
        if p.startswith('**') and p.endswith('**'):
            inner = escape_xml(p[2:-2])
            out.append(f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{inner}</w:t></w:r>')
        else:
            out.append(f'<w:r><w:t xml:space="preserve">{escape_xml(p)}</w:t></w:r>')
    return ''.join(out)


def para(text, style='Normal', bold=False, size=None, center=False):
    rpr = ''
    props = ''
    if bold:
        props += '<w:b/>'
    if size:
        props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    if props:
        rpr = f'<w:rPr>{props}</w:rPr>'

    ppr_bits = ''
    if style in ('Heading1', 'Heading2', 'Title'):
        ppr_bits += f'<w:pStyle w:val="{style}"/>'
    if center:
        ppr_bits += '<w:jc w:val="center"/>'
    ppr = f'<w:pPr>{ppr_bits}</w:pPr>' if ppr_bits else ''

    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r></w:p>'


def para_inline(text):
    """Paragraph that honours inline **bold** markers."""
    return f'<w:p>{runs_from_inline(text)}</w:p>'


def table_xml(rows):
    """Build a Word table from a list of rows (each a list of cell strings).
    First row is treated as a bold header."""
    ncols = max(len(r) for r in rows)
    grid = ''.join('<w:gridCol w:w="%d"/>' % (9000 // ncols) for _ in range(ncols))

    def cell(txt, header=False):
        rpr = '<w:rPr><w:b/></w:rPr>' if header else ''
        shd = '<w:shd w:val="clear" w:color="auto" w:fill="D9D9D9"/>' if header else ''
        return (
            '<w:tc>'
            f'<w:tcPr><w:tcW w:w="{9000 // ncols}" w:type="dxa"/>{shd}'
            '<w:tcBorders>'
            '<w:top w:val="single" w:sz="4" w:color="000000"/>'
            '<w:left w:val="single" w:sz="4" w:color="000000"/>'
            '<w:bottom w:val="single" w:sz="4" w:color="000000"/>'
            '<w:right w:val="single" w:sz="4" w:color="000000"/>'
            '</w:tcBorders></w:tcPr>'
            f'<w:p><w:pPr><w:spacing w:after="20"/></w:pPr>'
            f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(txt)}</w:t></w:r></w:p>'
            '</w:tc>'
        )

    body = ''
    for i, row in enumerate(rows):
        cells = row + [''] * (ncols - len(row))
        body += '<w:tr>' + ''.join(cell(c, header=(i == 0)) for c in cells) + '</w:tr>'

    tbl_pr = (
        '<w:tblPr>'
        '<w:tblW w:w="9000" w:type="dxa"/>'
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:color="000000"/>'
        '<w:left w:val="single" w:sz="4" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="4" w:color="000000"/>'
        '<w:right w:val="single" w:sz="4" w:color="000000"/>'
        '<w:insideH w:val="single" w:sz="4" w:color="000000"/>'
        '<w:insideV w:val="single" w:sz="4" w:color="000000"/>'
        '</w:tblBorders></w:tblPr>'
    )
    return f'<w:tbl>{tbl_pr}<w:tblGrid>{grid}</w:tblGrid>{body}</w:tbl><w:p/>'


def parse_table_block(lines, i):
    """Collect consecutive markdown table lines starting at index i."""
    rows = []
    while i < len(lines) and lines[i].strip().startswith('|'):
        line = lines[i].strip()
        if re.match(r'^\|[\s\-:|]+\|$', line):
            i += 1
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        rows.append(cells)
        i += 1
    return rows, i


def markdown_to_body(md):
    lines = md.split('\n')
    out = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            out.append('<w:p/>')
            i += 1
            continue

        if line.strip().startswith('|'):
            rows, i = parse_table_block(lines, i)
            if rows:
                out.append(table_xml(rows))
            continue

        if line.startswith('# ') and not line.startswith('## '):
            out.append(para(line[2:].strip(), style='Title', bold=True, size=32, center=True))
        elif line.startswith('## '):
            out.append(para(line[3:].strip(), style='Heading1', bold=True, size=28))
        elif line.startswith('### '):
            out.append(para(line[4:].strip(), style='Heading2', bold=True, size=24))
        elif line.startswith('---'):
            out.append('<w:p/>')
        else:
            out.append(para_inline(line))
        i += 1
    return '\n'.join(out)


def main():
    md = open(SRC).read()
    body_content = markdown_to_body(md)

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
</w:styles>'''

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

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', styles)

    print(f"Created {OUT}")


if __name__ == '__main__':
    main()
