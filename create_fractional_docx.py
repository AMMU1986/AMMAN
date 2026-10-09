#!/usr/bin/env python3
"""
Build a Word (.docx) version of the fractional-Stefan manuscript.

Pure Python standard library (zipfile + XML). Unlike the plain-text converter
used elsewhere in this repo, this builder:
  * renders every Markdown pipe-table as a real bordered Word table, and
  * embeds the seven generated PNG figures (centred, scaled) beneath their
    captions in the figure list.

Run AFTER generate_fractional_figures.py so the PNG files exist.
"""

import os
import re
import struct
import zipfile

BASE = '/projects/sandbox/AMMAN'
MD = os.path.join(BASE, 'Fractional_Stefan_Binary_Alloy.md')
FIG_DIR = os.path.join(BASE, 'fractional_figures')
OUT = os.path.join(BASE, 'Fractional_Stefan_Binary_Alloy.docx')

FIG_FILES = {
    1: 'Figure_1_Problem_Schematic.png',
    2: 'Figure_2_Mittag_Leffler.png',
    3: 'Figure_3_Temperature.png',
    4: 'Figure_4_Concentration.png',
    5: 'Figure_5_Interface_Kinetics.png',
    6: 'Figure_6_Lambda_Map.png',
    7: 'Figure_7_Sensitivity.png',
}

EMU_PER_INCH = 914400
MAX_WIDTH_IN = 6.0


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def strip_md(t):
    """Remove emphasis markers but keep the text readable."""
    t = re.sub(r'\*\*([^*]+)\*\*', r'\1', t)
    t = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'\1', t)
    return t


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    # IHDR width/height are big-endian uint32 at offset 16 and 20
    w, h = struct.unpack('>II', head[16:24])
    return w, h


def para(text, style=None, bold=False, size=None, italic=False, center=False):
    rpr = ''
    inner = ''
    if bold:
        inner += '<w:b/>'
    if italic:
        inner += '<w:i/>'
    if size:
        inner += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    if inner:
        rpr = f'<w:rPr>{inner}</w:rPr>'
    ppr = ''
    jc = '<w:jc w:val="center"/>' if center else ''
    if style:
        ppr = f'<w:pPr><w:pStyle w:val="{style}"/>{jc}</w:pPr>'
    elif jc:
        ppr = f'<w:pPr>{jc}</w:pPr>'
    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'


def table_xml(rows):
    """rows: list of list-of-cell-strings; first row is header."""
    grid_cols = max(len(r) for r in rows)
    borders = (
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="6" w:color="000000"/>'
        '<w:left w:val="single" w:sz="6" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="6" w:color="000000"/>'
        '<w:right w:val="single" w:sz="6" w:color="000000"/>'
        '<w:insideH w:val="single" w:sz="4" w:color="808080"/>'
        '<w:insideV w:val="single" w:sz="4" w:color="808080"/>'
        '</w:tblBorders>'
    )
    tblpr = (f'<w:tblPr><w:tblW w:w="5000" w:type="pct"/>{borders}'
             '<w:tblLook w:val="04A0"/></w:tblPr>')
    grid = '<w:tblGrid>' + ''.join('<w:gridCol/>' for _ in range(grid_cols)) + '</w:tblGrid>'
    body = ''
    for ri, row in enumerate(rows):
        header = (ri == 0)
        cells = ''
        for ci in range(grid_cols):
            cell = row[ci] if ci < len(row) else ''
            shade = '<w:shd w:val="clear" w:color="auto" w:fill="DEEBF7"/>' if header else ''
            tcpr = f'<w:tcPr>{shade}</w:tcPr>'
            rpr = '<w:rPr><w:b/><w:sz w:val="20"/></w:rPr>' if header else '<w:rPr><w:sz w:val="20"/></w:rPr>'
            cp = (f'<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>'
                  f'<w:r>{rpr}<w:t xml:space="preserve">{esc(strip_md(cell))}</w:t></w:r></w:p>')
            cells += f'<w:tc>{tcpr}{cp}</w:tc>'
        body += f'<w:tr>{cells}</w:tr>'
    return f'<w:tbl>{tblpr}{grid}{body}</w:tbl>'


def image_xml(rel_id, pid, px_w, px_h):
    disp_w_in = min(MAX_WIDTH_IN, px_w / 96.0)
    scale = disp_w_in / (px_w / 96.0)
    cx = int(px_w / 96.0 * EMU_PER_INCH * scale)
    cy = int(px_h / 96.0 * EMU_PER_INCH * scale)
    return (
        '<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        f'<wp:docPr id="{pid}" name="Figure{pid}"/>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr><pic:cNvPr id="{pid}" name="Figure{pid}"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rel_id}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/>'
        f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline>'
        '</w:drawing></w:r></w:p>'
    )


def build():
    with open(MD, 'r') as f:
        lines = f.read().split('\n')

    body = []
    images = []        # (rel_id, media_name, path)
    rel_counter = [1]  # rId1 reserved for styles

    def next_rid():
        rel_counter[0] += 1
        return f'rId{rel_counter[0]}'

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip()

        # Markdown table block
        if line.startswith('|'):
            tbl = []
            while i < n and lines[i].rstrip().startswith('|'):
                raw = lines[i].rstrip()
                if not re.match(r'^\|[\s:\-\|]+\|$', raw):
                    cells = [c.strip() for c in raw.strip('|').split('|')]
                    tbl.append(cells)
                i += 1
            body.append(table_xml(tbl))
            body.append('<w:p/>')
            continue

        if not line:
            i += 1
            continue

        # Figure list bullet -> embed image then caption
        m = re.match(r'^- \*\*Figure (\d+)\.\*\*\s*(.*)$', line)
        if m:
            num = int(m.group(1))
            cap = 'Figure %d. %s' % (num, strip_md(m.group(2)))
            fpath = os.path.join(FIG_DIR, FIG_FILES.get(num, ''))
            if os.path.exists(fpath):
                rid = next_rid()
                media = 'image%d.png' % num
                images.append((rid, media, fpath))
                w, h = png_size(fpath)
                body.append(image_xml(rid, num + 100, w, h))
            body.append(para(cap, bold=True, size=20, center=True))
            body.append('<w:p/>')
            i += 1
            continue

        if line.startswith('# ') and not line.startswith('## '):
            body.append(para(line[2:].strip(), style='Title', bold=True, size=32, center=True))
        elif line.startswith('## '):
            body.append(para(line[3:].strip(), style='Heading1', bold=True, size=28))
        elif line.startswith('### '):
            body.append(para(line[4:].strip(), style='Heading2', bold=True, size=24))
        elif line.startswith('---'):
            body.append('<w:p/>')
        elif line.startswith('> '):
            body.append(para(strip_md(line[2:]), size=22, italic=True))
        elif line.startswith('**') and line.rstrip().endswith('**') and line.count('**') == 2:
            body.append(para(strip_md(line), bold=True))
        elif line.startswith('*') and line.endswith('*') and not line.startswith('**'):
            body.append(para(strip_md(line), italic=True, size=20))
        elif re.match(r'^\d+\.\s', line) or line.startswith('[') or line.startswith('- '):
            body.append(para(strip_md(line)))
        else:
            body.append(para(strip_md(line)))
        i += 1

    body_xml = '\n'.join(body)

    # ---- package parts -------------------------------------------------
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '</Types>'
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>'
    )
    doc_rel_items = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rid, media, _ in images:
        doc_rel_items.append(
            f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{media}"/>')
    word_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + ''.join(doc_rel_items) + '</Relationships>'
    )
    styles = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>'
        '<w:pPr><w:spacing w:after="120" w:line="312" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="32"/></w:rPr>'
        '<w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr>'
        '<w:pPr><w:spacing w:before="320" w:after="120"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="24"/></w:rPr>'
        '<w:pPr><w:spacing w:before="240" w:after="80"/></w:pPr></w:style>'
        '</w:styles>'
    )
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<w:body>' + body_xml +
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
        '</w:body></w:document>'
    )

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('_rels/.rels', rels)
        z.writestr('word/_rels/document.xml.rels', word_rels)
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', styles)
        for _, media, path in images:
            with open(path, 'rb') as f:
                z.writestr('word/media/' + media, f.read())

    print('Created %s' % OUT)
    print('  embedded %d figures' % len(images))


if __name__ == '__main__':
    build()
