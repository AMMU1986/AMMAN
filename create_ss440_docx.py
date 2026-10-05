#!/usr/bin/env python3
"""
Create a Word document (.docx) from the corrected SS440 MIG welding manuscript.

Renders markdown headings, paragraphs and GitHub-style pipe tables into a valid
.docx using only the Python standard library (zipfile). Tables are emitted as
native Word tables (w:tbl) with borders and a shaded header row.
"""

import zipfile
import re

MD_PATH = '/projects/sandbox/AMMAN/Manuscript_SS440_MIG_Welding_Fillers.md'
OUT_PATH = '/projects/sandbox/AMMAN/Manuscript_SS440_MIG_Welding_Fillers.docx'


def escape_xml(text):
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))


def runs_from_inline(text):
    """Convert inline **bold** markers into a sequence of Word runs."""
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


def para(text, style=None, bold=False, size=None, align=None):
    ppr_bits = []
    if style:
        ppr_bits.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        ppr_bits.append(f'<w:jc w:val="{align}"/>')
    ppr = f'<w:pPr>{"".join(ppr_bits)}</w:pPr>' if ppr_bits else ''

    rpr_bits = []
    if bold:
        rpr_bits.append('<w:b/>')
    if size:
        rpr_bits.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    rpr = f'<w:rPr>{"".join(rpr_bits)}</w:rPr>' if rpr_bits else ''

    return (f'<w:p>{ppr}<w:r>{rpr}'
            f'<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r></w:p>')


def para_inline(text, style=None):
    """Paragraph that honours inline **bold** markers."""
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ''
    return f'<w:p>{ppr}{runs_from_inline(text)}</w:p>'


def split_row(line):
    cells = line.strip().strip('|').split('|')
    return [c.strip() for c in cells]


def cell_xml(text, header=False, width=None):
    shade = '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>' if header else ''
    w = f'<w:tcW w:w="{width}" w:type="dxa"/>' if width else ''
    tcpr = f'<w:tcPr>{w}{shade}<w:vAlign w:val="center"/></w:tcPr>'
    rpr = '<w:rPr><w:b/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>' if header \
          else '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
    ppr = '<w:pPr><w:spacing w:after="20" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr>'
    return (f'<w:tc>{tcpr}<w:p>{ppr}<w:r>{rpr}'
            f'<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r></w:p></w:tc>')


def table_xml(rows):
    borders = (
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '</w:tblBorders>'
    )
    tblpr = (f'<w:tblPr><w:tblStyle w:val="TableGrid"/>'
             f'<w:tblW w:w="5000" w:type="pct"/>{borders}'
             f'<w:tblLook w:val="04A0"/></w:tblPr>')

    ncols = len(rows[0])
    col_w = int(9360 / ncols)
    grid = '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{col_w}"/>' for _ in range(ncols)) + '</w:tblGrid>'

    body = ''
    for i, row in enumerate(rows):
        header = (i == 0)
        trpr = '<w:trPr><w:tblHeader/></w:trPr>' if header else ''
        cells = ''.join(cell_xml(c, header=header, width=col_w) for c in row)
        body += f'<w:tr>{trpr}{cells}</w:tr>'

    return f'<w:tbl>{tblpr}{grid}{body}</w:tbl>'


def build_body(md_text):
    out = []
    lines = md_text.split('\n')
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i].rstrip()

        # Blank line
        if not line.strip():
            out.append('<w:p/>')
            i += 1
            continue

        # Table block
        if line.strip().startswith('|'):
            tbl_lines = []
            while i < n and lines[i].strip().startswith('|'):
                tbl_lines.append(lines[i])
                i += 1
            rows = []
            for tl in tbl_lines:
                if re.match(r'^\s*\|[\s\-:|]+\|\s*$', tl):
                    continue  # separator row
                rows.append(split_row(tl))
            if rows:
                out.append(table_xml(rows))
            out.append('<w:p/>')
            continue

        # Headings
        if line.startswith('# ') and not line.startswith('## '):
            out.append(para(line[2:].strip(), style='Title', bold=True, size=30))
        elif line.startswith('## '):
            out.append(para(line[3:].strip(), style='Heading1', bold=True, size=28))
        elif line.startswith('### '):
            out.append(para(line[4:].strip(), style='Heading2', bold=True, size=24))
        elif line.startswith('**') and line.endswith('**') and line.count('**') == 2:
            out.append(para(line.strip('*').strip(), bold=True))
        else:
            out.append(para_inline(line))
        i += 1

    return '\n'.join(out)


def create_docx():
    with open(MD_PATH, 'r') as f:
        md_text = f.read()
    body = build_body(md_text)

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
    {body}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    with zipfile.ZipFile(OUT_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', styles)

    print(f"Created {OUT_PATH}")


if __name__ == '__main__':
    create_docx()
