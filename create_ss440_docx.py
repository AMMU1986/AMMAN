#!/usr/bin/env python3
"""
Create a Word document (.docx) from the SS440 MIG welding manuscript markdown file.
Uses only the Python standard library (zipfile). Renders markdown tables as
native Word tables, headings, and justified body paragraphs.
"""

import zipfile
import re

SRC = '/projects/sandbox/AMMAN/Manuscript_SS440_MIG_Welding.md'
OUT = '/projects/sandbox/AMMAN/Manuscript_SS440_MIG_Welding.docx'


def escape_xml(text):
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))


def inline_runs(text):
    """Convert a line with optional **bold** markers into Word runs."""
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
    return ''.join(runs)


def para(text, style='Normal', bold=False, size=None):
    rpr_bits = ''
    if bold:
        rpr_bits += '<w:b/>'
    if size:
        rpr_bits += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    rpr = f'<w:rPr>{rpr_bits}</w:rPr>' if rpr_bits else ''

    ppr = ''
    if style in ('Title', 'Heading1', 'Heading2'):
        ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
    return (f'<w:p>{ppr}<w:r>{rpr}'
            f'<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r></w:p>')


def bullet(text):
    return (f'<w:p><w:pPr><w:pStyle w:val="ListBullet"/></w:pPr>'
            f'{inline_runs(text)}</w:p>')


def table_xml(rows):
    """rows: list of lists of cell strings. First row is treated as header."""
    ncols = max(len(r) for r in rows)
    grid = ''.join('<w:gridCol w:w="%d"/>' % (9360 // ncols) for _ in range(ncols))

    out = ['<w:tbl>']
    out.append('<w:tblPr>'
               '<w:tblStyle w:val="TableGrid"/>'
               '<w:tblW w:w="0" w:type="auto"/>'
               '<w:tblBorders>'
               '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '</w:tblBorders></w:tblPr>')
    out.append(f'<w:tblGrid>{grid}</w:tblGrid>')

    for ri, row in enumerate(rows):
        cells = list(row) + [''] * (ncols - len(row))
        out.append('<w:tr>')
        for cell in cells:
            is_header = (ri == 0)
            shade = '<w:shd w:val="clear" w:color="auto" w:fill="D9D9D9"/>' if is_header else ''
            rpr = '<w:rPr><w:b/><w:sz w:val="20"/></w:rPr>' if is_header else '<w:rPr><w:sz w:val="20"/></w:rPr>'
            out.append('<w:tc>'
                       f'<w:tcPr><w:tcW w:w="{9360 // ncols}" w:type="dxa"/>{shade}</w:tcPr>'
                       f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
                       f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(cell.strip())}</w:t></w:r></w:p>'
                       '</w:tc>')
        out.append('</w:tr>')
    out.append('</w:tbl>')
    out.append('<w:p/>')
    return ''.join(out)


def build_body(md):
    lines = md.split('\n')
    body = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if not line:
            body.append('<w:p/>')
            i += 1
            continue

        # Table block
        if line.lstrip().startswith('|'):
            tbl = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                row = lines[i].strip().strip('|')
                if not re.match(r'^[\s\-:|]+$', row):  # skip separator row
                    cells = [c.strip() for c in row.split('|')]
                    tbl.append(cells)
                i += 1
            if tbl:
                body.append(table_xml(tbl))
            continue

        # Headings
        if line.startswith('# '):
            body.append(para(line[2:].strip(), style='Title', bold=True, size=30))
        elif line.startswith('## '):
            body.append(para(line[3:].strip(), style='Heading1', bold=True, size=28))
        elif line.startswith('### '):
            body.append(para(line[4:].strip(), style='Heading2', bold=True, size=24))
        elif line.startswith('- '):
            body.append(bullet(line[2:].strip()))
        else:
            # bold-only line (e.g., **Table 1.** ...)
            body.append(f'<w:p>{inline_runs(line)}</w:p>')
        i += 1

    return '\n'.join(body)


def main():
    with open(SRC) as f:
        md = f.read()
    body_content = build_body(md)

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
    <w:rPr><w:b/><w:sz w:val="30"/><w:szCs w:val="30"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
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
  <w:style w:type="paragraph" w:styleId="ListBullet">
    <w:name w:val="List Bullet"/>
    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:ind w:left="420" w:hanging="220"/><w:jc w:val="both"/></w:pPr>
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

    print(f'Created {OUT}')


if __name__ == '__main__':
    main()
