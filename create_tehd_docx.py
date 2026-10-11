#!/usr/bin/env python3
"""
Convert Research_Article_TEHD_Journal_Bearing.md into a Word (.docx) document
with NATIVE Word equation objects (OMML) and all seven embedded figures.

Pure standard library (zipfile) + the local latex2omml converter.
"""

import os
import re
import zipfile
from latex2omml import latex_to_omml

SRC = '/projects/sandbox/AMMAN/Research_Article_TEHD_Journal_Bearing.md'
OUT = '/projects/sandbox/AMMAN/Research_Article_TEHD_Journal_Bearing.docx'
FIGDIR = '/projects/sandbox/AMMAN/tehd_figures'

USABLE = 9360          # twips (6.5 in)
IMG_W_EMU = 5486400    # 6.0 in display width

# figure number -> file
FIGS = {
    1: 'Fig1_schematic.png',
    2: 'Fig2_pressure_validation.png',
    3: 'Fig3_peakpressure_validation.png',
    4: 'Fig4_pressure_index.png',
    5: 'Fig5_temperature_index.png',
    6: 'Fig6_load_index.png',
    7: 'Fig7_film_eccentricity.png',
}


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def png_size(path):
    with open(path, 'rb') as f:
        b = f.read(24)
    return int.from_bytes(b[16:20], 'big'), int.from_bytes(b[20:24], 'big')


def omath(latex):
    return f'<m:oMath>{latex_to_omml(latex)}</m:oMath>'


def runs_from_inline(text, bold=False):
    """Build runs for a line: **bold** -> bold runs, $math$ -> native OMML."""
    tokens = re.split(r'(\*\*[^*]+\*\*|\$[^$]+\$)', text)
    out = []
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith('**') and tok.endswith('**'):
            out.append(f'<w:r><w:rPr><w:b/></w:rPr>'
                       f'<w:t xml:space="preserve">{esc(tok[2:-2])}</w:t></w:r>')
        elif tok.startswith('$') and tok.endswith('$'):
            out.append(omath(tok[1:-1]))
        else:
            rpr = '<w:rPr><w:b/></w:rPr>' if bold else ''
            out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{esc(tok)}</w:t></w:r>')
    return ''.join(out) or '<w:r><w:t></w:t></w:r>'


def para(text, style=None, align=None):
    ppr = '<w:pPr>'
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if align:
        ppr += f'<w:jc w:val="{align}"/>'
    ppr += '</w:pPr>'
    return f'<w:p>{ppr}{runs_from_inline(text)}</w:p>'


def heading(text, lvl):
    style = {1: 'Heading1', 2: 'Heading2', 3: 'Heading3'}[lvl]
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{runs_from_inline(text)}</w:p>'


def equation_para(latex, number):
    tabs = (f'<w:pPr><w:tabs><w:tab w:val="center" w:pos="4680"/>'
            f'<w:tab w:val="right" w:pos="{USABLE}"/></w:tabs></w:pPr>')
    lead = '<w:r><w:tab/></w:r>'
    num = f'<w:r><w:tab/><w:t xml:space="preserve">({number})</w:t></w:r>' if number else ''
    return f'<w:p>{tabs}{lead}{omath(latex)}{num}</w:p>'


def image_para(rid, w_emu, h_emu, pid):
    return (f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
            f'<wp:extent cx="{w_emu}" cy="{h_emu}"/>'
            f'<wp:docPr id="{pid}" name="Picture{pid}"/>'
            f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:nvPicPr><pic:cNvPr id="{pid}" name="Picture{pid}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{w_emu}" cy="{h_emu}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            f'</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')


def table_xml(rows):
    ncols = max(len(r) for r in rows)
    colw = USABLE // ncols
    grid = '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{colw}"/>' for _ in range(ncols)) + '</w:tblGrid>'
    borders = ('<w:tblBorders>' + ''.join(
        f'<w:{b} w:val="single" w:sz="4" w:space="0" w:color="444444"/>'
        for b in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']) + '</w:tblBorders>')
    tblpr = (f'<w:tblPr><w:tblW w:w="{USABLE}" w:type="dxa"/>{borders}'
             '<w:tblLook w:val="04A0"/></w:tblPr>')
    out = [f'<w:tbl>{tblpr}{grid}']
    for i, row in enumerate(rows):
        row = row + [''] * (ncols - len(row))
        cells = []
        for cell in row:
            shade = '<w:shd w:val="clear" w:fill="D9E2F3"/>' if i == 0 else ''
            inner = runs_from_inline(cell, bold=(i == 0))
            cells.append(f'<w:tc><w:tcPr><w:tcW w:w="{colw}" w:type="dxa"/>{shade}</w:tcPr>'
                         f'<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>{inner}</w:p></w:tc>')
        out.append('<w:tr>' + ''.join(cells) + '</w:tr>')
    out.append('</w:tbl><w:p/>')
    return ''.join(out)


def build_body(md):
    lines = md.split('\n')
    body, i, n = [], 0, len(md.split('\n'))
    while i < n:
        line = lines[i].rstrip()

        if line.strip() == '$$':
            j, buf = i + 1, []
            while j < n and lines[j].strip() != '$$':
                buf.append(lines[j]); j += 1
            blob = ' '.join(x.strip() for x in buf)
            mnum = re.search(r'\\tag\{(\d+)\}', blob)
            number = mnum.group(1) if mnum else ''
            blob = re.sub(r'\\tag\{\d+\}', '', blob)
            body.append(equation_para(blob, number))
            i = j + 1
            continue

        if line.startswith('|'):
            rows = []
            while i < n and lines[i].rstrip().startswith('|'):
                raw = lines[i].rstrip()
                if re.match(r'^\|[\s:\-|]+\|?\s*$', raw):
                    i += 1; continue
                rows.append([c.strip() for c in raw.strip().strip('|').split('|')])
                i += 1
            if rows:
                body.append(table_xml(rows))
            continue

        if not line.strip():
            body.append('<w:p/>'); i += 1; continue

        if line.startswith('# ') and not line.startswith('## '):
            body.append(para(line[2:].strip(), style='Title', align='center'))
        elif line.startswith('## '):
            body.append(heading(line[3:].strip(), 1))
        elif line.startswith('### '):
            body.append(heading(line[4:].strip(), 2))
        elif line.startswith('#### '):
            body.append(heading(line[5:].strip(), 3))
        elif line.startswith('---'):
            body.append('<w:p/>')
        else:
            body.append(para(line))
            mfig = re.match(r'^\*\*Figure (\d)\.\*\*', line)
            if mfig:
                fnum = int(mfig.group(1))
                if fnum in FIGS:
                    w, h = png_size(os.path.join(FIGDIR, FIGS[fnum]))
                    body.append(image_para(f'rIdImg{fnum}', IMG_W_EMU,
                                           int(IMG_W_EMU * h / w), 100 + fnum))
        i += 1
    return '\n'.join(body)


STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:rPr><w:b/><w:sz w:val="30"/><w:szCs w:val="30"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="300" w:after="120"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:rPr><w:b/><w:sz w:val="23"/><w:szCs w:val="23"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="220" w:after="100"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:rPr><w:b/><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="120" w:after="60"/></w:pPr>
  </w:style>
</w:styles>'''


def build_docx():
    with open(SRC) as f:
        md = f.read()
    body = build_body(md)

    content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '</Types>')

    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>')

    img_rels = ''.join(
        f'<Relationship Id="rIdImg{k}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image{k}.png"/>'
        for k in FIGS)
    word_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        + img_rels + '</Relationships>')

    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<w:body>{body}'
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
        '</w:body></w:document>')

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
        for k, fn in FIGS.items():
            with open(os.path.join(FIGDIR, fn), 'rb') as im:
                zf.writestr(f'word/media/image{k}.png', im.read())
    print(f'Created {OUT} ({os.path.getsize(OUT)/1024:.1f} KB)')


if __name__ == '__main__':
    build_docx()
