#!/usr/bin/env python3
"""
Build the 57-equation manuscript DOCX. Equations are native OMML objects with
NO numbers. Reads Fractional_TriHybrid_Disks_57.md; each [[EQ:n]] token (n=1..57)
is replaced by the OMML object EQ57[n-1]. Native tables + 7 embedded figures.
Stdlib only.
"""

import zipfile
import os
import re
import struct
from select57 import EQ57

MD = "/projects/sandbox/AMMAN/Fractional_TriHybrid_Disks_57.md"
OUT = "/projects/sandbox/AMMAN/Fractional_TriHybrid_Disks_57eq.docx"
FIGDIR = "/projects/sandbox/AMMAN/fractional_figures"

FIGMAP = [
    ("Figure 1", "Figure_1_velocity_alpha.png",
     "Radial velocity profile for fractional orders 1.0, 0.9, 0.7, 0.5."),
    ("Figure 2", "Figure_2_temperature_gammaT.png",
     "Temperature profile for Cattaneo relaxation 0.0, 0.3, 0.6, 0.9."),
    ("Figure 3", "Figure_3_velocity_beta.png",
     "Radial velocity profile for second-grade parameter 0.1, 0.4, 0.8, 1.2."),
    ("Figure 4", "Figure_4_temperature_shape.png",
     "Temperature profile for brick, platelet and blade nanoparticle shapes."),
    ("Figure 5", "Figure_5_concentration_Sr.png",
     "Concentration profile for Soret numbers 0.00, 0.05, 0.10, 0.15."),
    ("Figure 6", "Figure_6_temperature_Rd.png",
     "Temperature profile for radiation parameters 0.2, 0.6, 1.0, 1.5."),
    ("Figure 7", "Figure_7_Nu_alpha_shape.png",
     "Lower-disk Nusselt number versus fractional order for three shapes."),
]


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))


def png_size(path):
    with open(path, 'rb') as f:
        f.read(16)
        w, h = struct.unpack('>II', f.read(8))
    return w, h


def para(text, style='Normal', bold=False, size=22, center=False):
    text = esc(text)
    rpr = '<w:rPr>' + ('<w:b/>' if bold else '') + f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'
    ppr = ''
    jc = '<w:jc w:val="center"/>' if center else ''
    if style == 'Title':
        ppr = '<w:pPr><w:pStyle w:val="Title"/><w:jc w:val="center"/></w:pPr>'
    elif style == 'H1':
        ppr = '<w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
    elif style == 'H2':
        ppr = '<w:pPr><w:pStyle w:val="Heading2"/></w:pPr>'
    elif jc:
        ppr = f'<w:pPr>{jc}</w:pPr>'
    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r></w:p>'


def eq_para(body):
    """Centered equation with NO number."""
    return (f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="60"/></w:pPr>'
            f'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">{body}</m:oMath>'
            f'</w:p>')


def table_xml(rows):
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
            rpr = '<w:rPr>' + ('<w:b/>' if bold else '') + '<w:sz w:val="18"/></w:rPr>'
            shade = '<w:shd w:val="clear" w:color="auto" w:fill="E8E8E8"/>' if bold else ''
            out.append(f'<w:tc><w:tcPr>{shade}</w:tcPr>'
                       f'<w:p><w:r>{rpr}<w:t xml:space="preserve">{esc(cell)}</w:t></w:r></w:p></w:tc>')
        out.append('</w:tr>')
    out.append('</w:tbl>')
    out.append('<w:p/>')
    return ''.join(out)


def image_xml(rid, w, h, emu_max_w=5486400):
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
    images = []
    rid = [100]
    inserted = set()
    used_eq = set()

    i, n = 0, len(lines)
    while i < n:
        line = lines[i].rstrip()

        # standalone equation token line
        m = re.match(r'^\[\[EQ:(\d+)\]\]\s*$', line.strip())
        if m:
            k = int(m.group(1))
            body.append(eq_para(EQ57[k - 1]))
            used_eq.add(k)
            i += 1
            continue

        if line.strip().startswith('|'):
            tbl = []
            while i < n and lines[i].strip().startswith('|'):
                row = lines[i].strip().strip('|')
                if re.match(r'^[\s\-:|]+$', row):
                    i += 1
                    continue
                tbl.append([c.strip() for c in row.split('|')])
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
        elif line.startswith('**') and line.endswith('**'):
            body.append(para(line.strip('*').strip(), bold=True))
        elif line.startswith('- '):
            body.append(para('\u2022 ' + re.sub(r'\*\*([^*]+)\*\*', r'\1', line[2:]), size=22))
        else:
            clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
            clean = re.sub(r'\*([^*]+)\*', r'\1', clean)
            body.append(para(clean))

        for key, fn, cap in FIGMAP:
            if key not in inserted and key in line:
                p = os.path.join(FIGDIR, fn)
                if os.path.exists(p):
                    rid[0] += 1
                    w, h = png_size(p)
                    body.append(image_xml(rid[0], w, h))
                    body.append(para(key + '. ' + cap, bold=True, size=18, center=True))
                    images.append((rid[0], fn))
                    inserted.add(key)
        i += 1

    for key, fn, cap in FIGMAP:
        if key not in inserted and os.path.exists(os.path.join(FIGDIR, fn)):
            rid[0] += 1
            w, h = png_size(os.path.join(FIGDIR, fn))
            body.append(image_xml(rid[0], w, h))
            body.append(para(key + '. ' + cap, bold=True, size=18, center=True))
            images.append((rid[0], fn))

    write_docx(''.join(body), images)
    print("Equations embedded (no numbers):", len(used_eq), "/ 57")
    miss = [k for k in range(1, 58) if k not in used_eq]
    if miss:
        print("  MISSING:", miss)
    print("Figures:", len(images))


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
    wr = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
          '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for r, fn in images:
        wr.append(f'<Relationship Id="rId{r}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{fn}"/>')
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
        '</w:tblBorders></w:tblPr></w:style></w:styles>')
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
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
        for r, fn in images:
            with open(os.path.join(FIGDIR, fn), 'rb') as f:
                z.writestr(f'word/media/{fn}', f.read())
    print("Wrote", OUT)


if __name__ == "__main__":
    build()
