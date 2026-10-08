#!/usr/bin/env python3
"""
Build Fractional_TriHybrid_Disks.docx from the markdown manuscript.
Pure standard library. Renders:
  - headings, paragraphs, equations (monospace)
  - markdown pipe-tables as native Word tables
  - the 7 real PNG figures embedded at their caption anchors
"""

import zipfile
import os
import re
import struct

MD = "/projects/sandbox/AMMAN/Fractional_TriHybrid_Disks.md"
OUT = "/projects/sandbox/AMMAN/Fractional_TriHybrid_Disks.docx"
FIGDIR = "/projects/sandbox/AMMAN/fractional_figures"

# Map figure caption keyword -> png file (anchored where the Figure is discussed)
FIGMAP = [
    ("Figure 1", "Figure_1_velocity_alpha.png"),
    ("Figure 2", "Figure_2_temperature_gammaT.png"),
    ("Figure 3", "Figure_3_velocity_beta.png"),
    ("Figure 4", "Figure_4_temperature_shape.png"),
    ("Figure 5", "Figure_5_concentration_Sr.png"),
    ("Figure 6", "Figure_6_temperature_Rd.png"),
    ("Figure 7", "Figure_7_Nu_alpha_shape.png"),
]


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))


def png_size(path):
    with open(path, 'rb') as f:
        f.read(16)
        w, h = struct.unpack('>II', f.read(8))
    return w, h


def para(text, style='Normal', bold=False, size=22, mono=False, italic=False, center=False):
    text = esc(text)
    rpr = '<w:rPr>'
    if bold:
        rpr += '<w:b/>'
    if italic:
        rpr += '<w:i/>'
    if mono:
        rpr += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'
    rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'
    ppr = ''
    jc = '<w:jc w:val="center"/>' if center else ''
    if style == 'Title':
        ppr = f'<w:pPr><w:pStyle w:val="Title"/><w:jc w:val="center"/></w:pPr>'
    elif style == 'H1':
        ppr = '<w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
    elif style == 'H2':
        ppr = '<w:pPr><w:pStyle w:val="Heading2"/></w:pPr>'
    elif jc:
        ppr = f'<w:pPr>{jc}</w:pPr>'
    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r></w:p>'


def table_xml(rows):
    """rows: list of list of cell strings. First row treated as header (bold)."""
    out = ['<w:tbl>',
           '<w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="0" w:type="auto"/>',
           '<w:tblBorders>',
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '</w:tblBorders></w:tblPr>']
    for ri, row in enumerate(rows):
        out.append('<w:tr>')
        for cell in row:
            bold = (ri == 0)
            rpr = '<w:rPr>' + ('<w:b/>' if bold else '') + '<w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
            shade = '<w:shd w:val="clear" w:color="auto" w:fill="E8E8E8"/>' if bold else ''
            out.append(f'<w:tc><w:tcPr>{shade}</w:tcPr>'
                       f'<w:p><w:r>{rpr}<w:t xml:space="preserve">{esc(cell)}</w:t></w:r></w:p></w:tc>')
        out.append('</w:tr>')
    out.append('</w:tbl>')
    out.append('<w:p/>')
    return ''.join(out)


def image_xml(rid, w, h, emu_max_w=5486400):
    # scale to max width ~5.7in (5486400 EMU), preserve aspect
    emu_w = emu_max_w
    emu_h = int(emu_max_w * h / w)
    return (f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0" '
            f'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
            f'<wp:extent cx="{emu_w}" cy="{emu_h}"/>'
            f'<wp:docPr id="{rid}" name="Figure{rid}"/>'
            f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:nvPicPr><pic:cNvPr id="{rid}" name="Figure{rid}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="rId{rid}" '
            f'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
            f'<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{emu_w}" cy="{emu_h}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
            f'</a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')


def build():
    md = open(MD).read()
    lines = md.split('\n')

    body = []
    images = []   # (rid, filename)
    rid_counter = [100]
    inserted_figs = set()

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip()

        # table block
        if line.strip().startswith('|'):
            tbl = []
            while i < n and lines[i].strip().startswith('|'):
                row = lines[i].strip().strip('|')
                if re.match(r'^[\s\-:|]+$', row):
                    i += 1
                    continue
                cells = [c.strip() for c in row.split('|')]
                tbl.append(cells)
                i += 1
            body.append(table_xml(tbl))
            continue

        if not line:
            body.append('<w:p/>')
            i += 1
            continue

        if line.startswith('# ') and not line.startswith('## '):
            body.append(para(line[2:].strip(), style='Title', bold=True, size=30))
        elif line.startswith('## '):
            body.append(para(line[3:].strip(), style='H1', bold=True, size=26))
        elif line.startswith('### '):
            body.append(para(line[4:].strip(), style='H2', bold=True, size=23))
        elif re.match(r'^\(\d+\)', line):
            # equation line -> monospace
            body.append(para(line, mono=True, size=20))
        elif line.startswith('**') and line.endswith('**'):
            body.append(para(line.strip('*').strip(), bold=True))
        elif line.startswith('- '):
            body.append(para('\u2022 ' + re.sub(r'\*\*([^*]+)\*\*', r'\1', line[2:]), size=22))
        else:
            clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
            clean = re.sub(r'\*([^*]+)\*', r'\1', clean)
            body.append(para(clean))

        # after writing a paragraph, check whether to anchor a figure:
        # insert each figure right after the first paragraph that references it
        for key, fn in FIGMAP:
            if key not in inserted_figs and key in line and 'Figure' in line:
                # only in discussion sentences, not the caption of another
                path = os.path.join(FIGDIR, fn)
                if os.path.exists(path):
                    rid_counter[0] += 1
                    rid = rid_counter[0]
                    w, h = png_size(path)
                    body.append(image_xml(rid, w, h))
                    body.append(para(key + '. ' + figure_caption(key), bold=True, size=18, center=True))
                    images.append((rid, fn))
                    inserted_figs.add(key)
        i += 1

    # any figures not yet anchored -> append at end
    for key, fn in FIGMAP:
        if key not in inserted_figs:
            path = os.path.join(FIGDIR, fn)
            if os.path.exists(path):
                rid_counter[0] += 1
                rid = rid_counter[0]
                w, h = png_size(path)
                body.append(image_xml(rid, w, h))
                body.append(para(key + '. ' + figure_caption(key), bold=True, size=18, center=True))
                images.append((rid, fn))

    write_docx(''.join(body), images)


def figure_caption(key):
    caps = {
        "Figure 1": "Radial velocity profile for fractional orders alpha = 1.0, 0.9, 0.7, 0.5.",
        "Figure 2": "Temperature profile for Cattaneo relaxation gammaT = 0.0, 0.3, 0.6, 0.9.",
        "Figure 3": "Radial velocity profile for second-grade parameter beta = 0.1, 0.4, 0.8, 1.2.",
        "Figure 4": "Temperature profile for brick, platelet and blade nanoparticle shapes.",
        "Figure 5": "Concentration profile for Soret numbers Sr = 0.00, 0.05, 0.10, 0.15.",
        "Figure 6": "Temperature profile for radiation parameters Rd = 0.2, 0.6, 1.0, 1.5.",
        "Figure 7": "Lower-disk Nusselt number versus fractional order for three shapes.",
    }
    return caps.get(key, "")


def write_docx(body_xml, images):
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
    # document rels: styles + each image
    wr = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
          '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rid, fn in images:
        wr.append(f'<Relationship Id="rId{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{fn}"/>')
    wr.append('</Relationships>')
    word_rels = ''.join(wr)

    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
        '<w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
        '<w:pPr><w:spacing w:after="120" w:line="300" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
        '<w:rPr><w:b/><w:sz w:val="30"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
        '<w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
        '<w:rPr><w:b/><w:sz w:val="26"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
        '<w:pPr><w:spacing w:before="300" w:after="120"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
        '<w:rPr><w:b/><w:i/><w:sz w:val="23"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
        '<w:pPr><w:spacing w:before="200" w:after="100"/></w:pPr></w:style>'
        '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/>'
        '<w:tblPr><w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '</w:tblBorders></w:tblPr></w:style>'
        '</w:styles>')

    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<w:body>' + body_xml +
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
        '</w:body></w:document>')

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('_rels/.rels', rels)
        z.writestr('word/_rels/document.xml.rels', word_rels)
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', styles)
        for rid, fn in images:
            with open(os.path.join(FIGDIR, fn), 'rb') as f:
                z.writestr(f'word/media/{fn}', f.read())
    print("Wrote", OUT, "with", len(images), "embedded figures")


if __name__ == "__main__":
    build()
