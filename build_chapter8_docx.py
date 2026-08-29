#!/usr/bin/env python3
"""
Build the Chapter 8 .docx with embedded PNG figures, inline tables and references.
Pure standard library (no python-docx). Extends the OOXML approach used in
create_chapter_docx.py by adding image (drawing) support.
"""

import zipfile
import os
import re
import struct

SRC_MD = '/projects/sandbox/AMMAN/Chapter_8_Sustainable_Manufacturing_Industry5.md'
FIG_DIR = '/projects/sandbox/AMMAN/chapter8_figures'
OUT_DOCX = '/projects/sandbox/AMMAN/Chapter_8_Sustainable_Manufacturing_Industry5.docx'

EMU_PER_PX = 9525          # 1 px = 9525 EMU at 96 dpi
MAX_WIDTH_EMU = 5486400    # ~6.0 inches printable width

# ─── boilerplate ───
CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

NUMBERING = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault><w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:sz w:val="24"/><w:szCs w:val="24"/>
    </w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/><w:pPr><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Abstract">
    <w:name w:val="Abstract"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:right="480"/></w:pPr><w:rPr><w:i/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="References">
    <w:name w:val="References"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureImage">
    <w:name w:val="Figure Image"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="180" w:after="60"/><w:keepNext/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="240"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="180" w:after="60"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
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


def escape_xml(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def make_run(text, bold=False, italic=False):
    props = []
    if bold:
        props.append('<w:b/>')
    if italic:
        props.append('<w:i/>')
    rpr = '<w:rPr>' + ''.join(props) + '</w:rPr>' if props else ''
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'


def parse_inline(text):
    runs = []
    parts = re.split(r'(\*\*.*?\*\*|\*[^*]+?\*)', text)
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
    return (f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
            f'{parse_inline(text)}</w:p>')


def png_size(path):
    with open(path, 'rb') as f:
        f.read(16)
        w, h = struct.unpack('>II', f.read(8))
    return w, h


def make_image_paragraph(rid, w_px, h_px, name):
    cx = w_px * EMU_PER_PX
    cy = h_px * EMU_PER_PX
    if cx > MAX_WIDTH_EMU:
        scale = MAX_WIDTH_EMU / cx
        cx = int(cx * scale)
        cy = int(cy * scale)
    drawing = f'''<w:p><w:pPr><w:pStyle w:val="FigureImage"/></w:pPr><w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
<wp:extent cx="{cx}" cy="{cy}"/>
<wp:effectExtent l="0" t="0" r="0" b="0"/>
<wp:docPr id="{rid}" name="{name}"/>
<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>
<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:nvPicPr><pic:cNvPr id="{rid}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed="rId{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''
    return drawing


def make_table(headers, rows):
    n_cols = len(headers)
    col_w = 9360 // n_cols
    tbl = '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
    tbl += '<w:tblW w:w="9360" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
    tbl += '<w:tblBorders>'
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        tbl += f'<w:{edge} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '</w:tblBorders></w:tblPr>'
    tbl += '<w:tblGrid>' + f'<w:gridCol w:w="{col_w}"/>' * n_cols + '</w:tblGrid>'
    # header row
    tbl += '<w:tr><w:trPr><w:tblHeader/></w:trPr>'
    for h in headers:
        tbl += ('<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>'
                '<w:vAlign w:val="center"/></w:tcPr>'
                '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="40" w:line="240" w:lineRule="auto"/></w:pPr>'
                f'{make_run(h.strip(), bold=True)}</w:p></w:tc>')
    tbl += '</w:tr>'
    for row in rows:
        tbl += '<w:tr>'
        for cell in row:
            tbl += ('<w:tc><w:p><w:pPr><w:spacing w:after="40" w:line="240" w:lineRule="auto"/></w:pPr>'
                    f'{make_run(cell.strip())}</w:p></w:tc>')
        for _ in range(n_cols - len(row)):
            tbl += '<w:tc><w:p/></w:tc>'
        tbl += '</w:tr>'
    tbl += '</w:tbl>'
    # spacer paragraph after table
    tbl += '<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>'
    return tbl


def md_to_body(md_text, fig_rids):
    elements = []
    lines = md_text.split('\n')
    i = 0
    in_refs = False
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        s = line.strip()
        if s == '---':
            i += 1
            continue
        # figure marker
        m = re.match(r'\[\[FIGURE:(\d+)\]\]', s)
        if m:
            n = int(m.group(1))
            rid = fig_rids[n]
            elements.append(make_image_paragraph(rid['rid'], rid['w'], rid['h'], f'Figure {n}'))
            i += 1
            continue
        # title
        if line.startswith('# ') and not line.startswith('## '):
            elements.append(make_paragraph(s[2:].strip(), 'Title'))
            i += 1
            continue
        if line.startswith('## '):
            head = s[3:].strip()
            if head == 'References':
                in_refs = True
            elements.append(make_paragraph(head, 'Heading1'))
            i += 1
            continue
        if line.startswith('### '):
            elements.append(make_paragraph(s[4:].strip(), 'Heading2'))
            i += 1
            continue
        if line.startswith('#### '):
            elements.append(make_paragraph(s[5:].strip(), 'Heading3'))
            i += 1
            continue
        # table
        if '|' in line and i + 1 < len(lines) and re.search(r'\|\s*---', lines[i + 1]):
            headers = [c.strip() for c in line.split('|') if c.strip()]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].split('|') if c.strip()])
                i += 1
            elements.append(make_table(headers, rows))
            continue
        # figure caption (starts with "Figure N:")
        if re.match(r'^Figure \d+:', s):
            elements.append(make_paragraph(s, 'FigureCaption'))
            i += 1
            continue
        # table caption (starts with "Table N.")
        if re.match(r'^Table \d+\.', s):
            elements.append(make_paragraph(s, 'TableCaption'))
            i += 1
            continue
        # reference entry
        if in_refs and re.match(r'^\[\d+\]', s):
            elements.append(make_paragraph(s, 'References'))
            i += 1
            continue
        elements.append(make_paragraph(s, 'Normal'))
        i += 1
    return '\n'.join(elements)


def build():
    with open(SRC_MD, encoding='utf-8') as f:
        md = f.read()

    # assign relationship ids to figures 1..4 (rId10+)
    fig_rids = {}
    base = 10
    for n in range(1, 5):
        path = os.path.join(FIG_DIR, f'Figure_{n}.png')
        w, h = png_size(path)
        fig_rids[n] = {'rid': base + n, 'w': w, 'h': h, 'path': path}

    body = md_to_body(md, fig_rids)

    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
  <w:body>
{body}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    # document relationships (styles, numbering, images)
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>']
    for n in range(1, 5):
        rid = fig_rids[n]['rid']
        rels.append(f'<Relationship Id="rId{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/Figure_{n}.png"/>')
    rels.append('</Relationships>')
    word_rels = '\n'.join(rels)

    with zipfile.ZipFile(OUT_DOCX, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES)
        zf.writestr('word/numbering.xml', NUMBERING)
        for n in range(1, 5):
            with open(fig_rids[n]['path'], 'rb') as img:
                zf.writestr(f'word/media/Figure_{n}.png', img.read())

    size_kb = os.path.getsize(OUT_DOCX) / 1024
    print(f"Created: {OUT_DOCX}")
    print(f"Size: {size_kb:.1f} KB")


if __name__ == '__main__':
    build()
