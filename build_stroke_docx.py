#!/usr/bin/env python3
"""
Build a Word .docx for the manuscript
"Sex Differences in Early Functional Outcomes After Acute Stroke"
from the markdown source, embedding the four generated figures and
rendering the three tables as native Word tables.

Pure standard library (zipfile/zlib/struct); no python-docx required.
"""

import os
import re
import struct
import zipfile

BASE = '/projects/sandbox/AMMAN'
MD = os.path.join(BASE, 'Sex_Differences_Early_Functional_Outcomes_Stroke.md')
OUT = os.path.join(BASE, 'Sex_Differences_Early_Functional_Outcomes_Stroke.docx')
FIGDIR = os.path.join(BASE, 'stroke_figures')

FIGURES = {
    1: 'Figure_1_Framework.png',
    2: 'Figure_2_GoodOutcome.png',
    3: 'Figure_3_Forest.png',
    4: 'Figure_4_Treatment.png',
}

EMU_PER_IN = 914400
DISP_WIDTH_IN = 6.0


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(26)
    w, h = struct.unpack('>II', head[16:24])
    return w, h


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;'))


def runs_from_inline(text):
    """Parse **bold** and *italic* into a list of (text, bold, italic)."""
    tokens = []
    i = 0
    bold = italic = False
    buf = ''

    def flush():
        nonlocal buf
        if buf:
            tokens.append((buf, bold, italic))
            buf = ''

    while i < len(text):
        if text.startswith('**', i):
            flush()
            bold = not bold
            i += 2
        elif text[i] == '*':
            flush()
            italic = not italic
            i += 1
        else:
            buf += text[i]
            i += 1
    flush()
    return tokens


def run_xml(text, bold=False, italic=False, size=22, color=None):
    rpr = '<w:rPr>'
    rpr += '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>'
    if bold:
        rpr += '<w:b/>'
    if italic:
        rpr += '<w:i/>'
    if color:
        rpr += '<w:color w:val="%s"/>' % color
    rpr += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size)
    rpr += '</w:rPr>'
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, esc(text))


def para(text, style=None, size=22, jc='both', space_after=140, bold=False):
    ppr = '<w:pPr>'
    if style:
        ppr += '<w:pStyle w:val="%s"/>' % style
    ppr += '<w:spacing w:after="%d" w:line="276" w:lineRule="auto"/>' % space_after
    ppr += '<w:jc w:val="%s"/>' % jc
    ppr += '</w:pPr>'
    runs = ''.join(run_xml(t, bold=(b or bold), italic=i, size=size)
                   for (t, b, i) in runs_from_inline(text))
    if not runs:
        runs = run_xml('', size=size)
    return '<w:p>%s%s</w:p>' % (ppr, runs)


def heading(text, level):
    sizes = {1: 30, 2: 26, 3: 23}
    colors = {1: '1F3B66', 2: '2E69B2', 3: '24959A'}
    ppr = ('<w:pPr><w:spacing w:before="%d" w:after="120"/><w:keepNext/></w:pPr>'
           % (300 if level == 1 else 200))
    r = ('<w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/>'
         '<w:color w:val="%s"/><w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr>'
         '<w:t xml:space="preserve">%s</w:t></w:r>'
         % (colors[level], sizes[level], sizes[level], esc(text)))
    return '<w:p>%s%s</w:p>' % (ppr, r)


def title_block(text):
    ppr = '<w:pPr><w:spacing w:after="120"/><w:jc w:val="center"/></w:pPr>'
    r = ('<w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/>'
         '<w:color w:val="1F3B66"/><w:sz w:val="40"/><w:szCs w:val="40"/></w:rPr>'
         '<w:t xml:space="preserve">%s</w:t></w:r>' % esc(text))
    return '<w:p>%s%s</w:p>' % (ppr, r)


def table_xml(rows):
    """rows: list of list of cell strings; first row is header."""
    n = len(rows[0])
    total = 9360
    cw = total // n
    grid = ''.join('<w:gridCol w:w="%d"/>' % cw for _ in range(n))

    def cell(text, header=False):
        shade = '<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % ('1F3B66' if header else 'FFFFFF')
        tcpr = ('<w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s'
                '<w:tcMar><w:top w:w="40" w:type="dxa"/><w:bottom w:w="40" w:type="dxa"/>'
                '<w:left w:w="70" w:type="dxa"/><w:right w:w="70" w:type="dxa"/></w:tcMar>'
                '<w:vAlign w:val="center"/></w:tcPr>' % (cw, shade))
        runs = ''.join(run_xml(t, bold=(header or b), italic=i, size=18,
                               color=('FFFFFF' if header else None))
                       for (t, b, i) in runs_from_inline(text))
        if not runs:
            runs = run_xml('', size=18)
        p = ('<w:p><w:pPr><w:spacing w:after="20" w:line="240" w:lineRule="auto"/>'
             '<w:jc w:val="left"/></w:pPr>%s</w:p>' % runs)
        return '<w:tc>%s%s</w:tc>' % (tcpr, p)

    borders = ('<w:tblBorders>'
               '<w:top w:val="single" w:sz="4" w:color="9AA6B4"/>'
               '<w:left w:val="single" w:sz="4" w:color="9AA6B4"/>'
               '<w:bottom w:val="single" w:sz="4" w:color="9AA6B4"/>'
               '<w:right w:val="single" w:sz="4" w:color="9AA6B4"/>'
               '<w:insideH w:val="single" w:sz="4" w:color="C8D0DA"/>'
               '<w:insideV w:val="single" w:sz="4" w:color="C8D0DA"/>'
               '</w:tblBorders>')
    tblpr = ('<w:tblPr><w:tblW w:w="%d" w:type="dxa"/>%s'
             '<w:tblLook w:val="04A0"/></w:tblPr>' % (total, borders))
    body = ''
    for ri, row in enumerate(rows):
        is_h = (ri == 0)
        trpr = '<w:trPr>%s</w:trPr>' % ('<w:tblHeader/>' if is_h else '')
        body += '<w:tr>%s%s</w:tr>' % (trpr, ''.join(cell(c, is_h) for c in row))
    return ('<w:tbl>%s<w:tblGrid>%s</w:tblGrid>%s</w:tbl>'
            '<w:p><w:pPr><w:spacing w:after="80"/></w:pPr></w:p>' % (tblpr, grid, body))


def drawing_xml(rid, w_emu, h_emu, name, docpr_id):
    return ('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="60"/></w:pPr>'
            '<w:r><w:drawing>'
            '<wp:inline distT="0" distB="0" distL="0" distR="0">'
            '<wp:extent cx="%d" cy="%d"/>'
            '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
            '<wp:docPr id="%d" name="%s"/>'
            '<wp:cNvGraphicFramePr><a:graphicFrameLocks '
            'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
            '</wp:cNvGraphicFramePr>'
            '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:nvPicPr><pic:cNvPr id="%d" name="%s"/><pic:cNvPicPr/></pic:nvPicPr>'
            '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            '</pic:pic></a:graphicData></a:graphic>'
            '</wp:inline></w:drawing></w:r></w:p>'
            % (w_emu, h_emu, docpr_id, name, docpr_id, name, rid, w_emu, h_emu))


def parse_markdown(md):
    """Yield structured blocks: ('title'|'h1'|'h2'|'para'|'bpara'|'table'|'fig', payload)."""
    lines = md.split('\n')
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.startswith('# ') and not line.startswith('## '):
            blocks.append(('title', line[2:].strip()))
        elif line.startswith('## '):
            blocks.append(('h1', line[3:].strip()))
        elif line.startswith('### '):
            blocks.append(('h2', line[4:].strip()))
        elif line.startswith('---'):
            pass
        elif line.lstrip().startswith('|'):
            # gather table
            tbl = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                tbl.append(lines[i].strip())
                i += 1
            rows = []
            for r in tbl:
                if re.match(r'^\|[\s\-:|]+\|$', r):
                    continue
                cells = [c.strip() for c in r.strip('|').split('|')]
                rows.append(cells)
            if rows:
                blocks.append(('table', rows))
            continue
        else:
            # figure legend?
            m = re.match(r'^\*\*Figure (\d+)\.\*\*', line)
            if m:
                blocks.append(('fig', int(m.group(1))))
            # bold-only line
            if line.startswith('**') and line.rstrip().endswith('**') and line.count('**') == 2:
                blocks.append(('bpara', line.strip().strip('*').strip()))
            else:
                blocks.append(('para', line.strip()))
        i += 1
    return blocks


def build():
    md = open(MD).read()
    blocks = parse_markdown(md)

    rels = ['<Relationship Id="rId1" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
            'Target="styles.xml"/>']
    media = {}       # filename -> arcname
    fig_rid = {}     # fsignum -> rid
    rid_counter = 2
    docpr_counter = 1

    for n, fname in FIGURES.items():
        arwithin = 'media/%s' % fname
        rid = 'rId%d' % rid_counter
        rid_counter += 1
        rels.append('<Relationship Id="%s" '
                    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                    'Target="%s"/>' % (rid, arwithin))
        media[os.path.join(FIGDIR, fname)] = 'word/' + arwithin
        fig_rid[n] = rid

    body = []
    for kind, payload in blocks:
        if kind == 'title':
            body.append(title_block(payload))
        elif kind == 'h1':
            body.append(heading(payload, 1))
        elif kind == 'h2':
            body.append(heading(payload, 2))
        elif kind == 'table':
            body.append(table_xml(payload))
        elif kind == 'bpara':
            body.append(para(payload, bold=True, jc='left', space_after=80))
        elif kind == 'fig':
            n = payload
            w, h = png_size(os.path.join(FIGDIR, FIGURES[n]))
            w_emu = int(DISP_WIDTH_IN * EMU_PER_IN)
            h_emu = int(w_emu * h / w)
            body.append(drawing_xml(fig_rid[n], w_emu, h_emu, FIGURES[n], docpr_counter))
            docpr_counter += 1
            # legend caption follows as its own para (rendered smaller/italic-ish)
        elif kind == 'para':
            # figure legends get smaller styling
            if re.match(r'^\*\*Figure \d+\.\*\*', payload):
                body.append(para(payload, size=19, jc='left', space_after=160))
            else:
                body.append(para(payload))

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<w:body>' + ''.join(body) +
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
        '</w:body></w:document>'
    )

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Override PartName="/word/document.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '</Types>'
    )

    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="word/document.xml"/></Relationships>'
    )

    word_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + ''.join(rels) + '</Relationships>'
    )

    styles = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
        '<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>'
        '</w:style></w:styles>'
    )

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('_rels/.rels', root_rels)
        z.writestr('word/_rels/document.xml.rels', word_rels)
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', styles)
        for src, arc in media.items():
            with open(src, 'rb') as f:
                z.writestr(arc, f.read())

    print("Wrote", OUT)


if __name__ == '__main__':
    build()
