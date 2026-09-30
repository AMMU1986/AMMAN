#!/usr/bin/env python3
"""
Build the CKD manuscript .docx from CKD_Manuscript.md with the 12 figures
embedded inline as JPG images at their [FIGURE n HERE] placeholders.

Pure standard library (zipfile). Produces a valid Office Open XML document
with:
  - Title / Heading1-3 / Normal styles (Times New Roman)
  - Real Word tables for the Markdown pipe tables
  - Inline JPG images (word/media) referenced through document.xml.rels
"""

import os
import re
import zipfile
import struct

BASE = '/projects/sandbox/AMMAN'
MD = os.path.join(BASE, 'CKD_Manuscript.md')
FIGDIR = os.path.join(BASE, 'ckd_figures')
OUT = os.path.join(BASE, 'CKD_Explainable_Ensemble_ML_Manuscript.docx')

EMU_PER_PX = 9525  # at 96 dpi
MAX_WIDTH_EMU = 5486400  # ~6.0 inches usable width (letter, 1in margins)

# Map figure number -> filename
FIG_FILES = {
    1: 'Figure_01_Framework.jpg',
    2: 'Figure_02_Distribution.jpg',
    3: 'Figure_03_MutualInfo.jpg',
    4: 'Figure_04_RFE.jpg',
    5: 'Figure_05_Correlation.jpg',
    6: 'Figure_06_SubsetComparison.jpg',
    7: 'Figure_07_IndividualModels.jpg',
    8: 'Figure_08_HPO.jpg',
    9: 'Figure_09_Ensemble.jpg',
    10: 'Figure_10_ROC_PR.jpg',
    11: 'Figure_11_SHAP.jpg',
    12: 'Figure_12_RiskStratification.jpg',
}


def jpeg_dimensions(path):
    """Return (width, height) of a baseline JPEG by scanning SOFn markers."""
    with open(path, 'rb') as f:
        data = f.read()
    i = 2  # skip SOI
    n = len(data)
    while i < n:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        # SOF0..SOF3, SOF5..SOF7, SOF9..SOF11, SOF13..SOF15 carry dimensions
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h = struct.unpack('>H', data[i + 5:i + 7])[0]
            w = struct.unpack('>H', data[i + 7:i + 9])[0]
            return w, h
        seg_len = struct.unpack('>H', data[i + 2:i + 4])[0]
        i += 2 + seg_len
    raise ValueError('No SOF marker found in ' + path)


def escape_xml(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


def inline_runs(text):
    """Convert **bold** segments to runs; return XML for the runs inside a <w:p>."""
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    runs = []
    for p in parts:
        if not p:
            continue
        if p.startswith('**') and p.endswith('**'):
            inner = escape_xml(p[2:-2])
            runs.append(f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{inner}</w:t></w:r>')
        else:
            runs.append(f'<w:r><w:t xml:space="preserve">{escape_xml(p)}</w:t></w:r>')
    return ''.join(runs) if runs else '<w:r><w:t xml:space="preserve"></w:t></w:r>'


def para(text, style=None):
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ''
    return f'<w:p>{ppr}{inline_runs(text)}</w:p>'


def empty_para():
    return '<w:p/>'


def image_paragraph(rid, w_px, h_px, doc_pr_id, name):
    """Inline image, scaled to fit page width, centered."""
    w_emu = w_px * EMU_PER_PX
    h_emu = h_px * EMU_PER_PX
    if w_emu > MAX_WIDTH_EMU:
        scale = MAX_WIDTH_EMU / w_emu
        w_emu = int(w_emu * scale)
        h_emu = int(h_emu * scale)
    return (
        '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="120"/></w:pPr>'
        '<w:r><w:drawing>'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{w_emu}" cy="{h_emu}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{doc_pr_id}" name="{escape_xml(name)}"/>'
        '<wp:cNvGraphicFramePr>'
        '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr>'
        f'<pic:cNvPr id="{doc_pr_id}" name="{escape_xml(name)}"/>'
        '<pic:cNvPicPr/>'
        '</pic:nvPicPr>'
        '<pic:blipFill>'
        f'<a:blip r:embed="{rid}"/>'
        '<a:stretch><a:fillRect/></a:stretch>'
        '</pic:blipFill>'
        '<pic:spPr>'
        f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{w_emu}" cy="{h_emu}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        '</pic:spPr>'
        '</pic:pic>'
        '</a:graphicData>'
        '</a:graphic>'
        '</wp:inline>'
        '</w:drawing></w:r></w:p>'
    )


def build_table(rows):
    """rows: list of list of cell strings; first row is header."""
    n_cols = max(len(r) for r in rows)
    # grid
    col_w = int(9360 / n_cols)  # twips within ~6.5in content
    grid = '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{col_w}"/>' for _ in range(n_cols)) + '</w:tblGrid>'
    tbl_pr = (
        '<w:tblPr>'
        '<w:tblStyle w:val="TableGrid"/>'
        '<w:tblW w:w="0" w:type="auto"/>'
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '</w:tblBorders>'
        '</w:tblPr>'
    )
    xml = ['<w:tbl>', tbl_pr, grid]
    for ri, row in enumerate(rows):
        cells = list(row) + [''] * (n_cols - len(row))
        xml.append('<w:tr>')
        for cell in cells:
            header = (ri == 0)
            shading = '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>' if header else ''
            # bold header text and any **..** inside
            txt = cell.strip()
            bold_all = header
            # build runs
            parts = re.split(r'(\*\*[^*]+\*\*)', txt)
            runs = []
            for p in parts:
                if not p:
                    continue
                b = bold_all or (p.startswith('**') and p.endswith('**'))
                inner = escape_xml(p[2:-2] if (p.startswith('**') and p.endswith('**')) else p)
                rpr = '<w:rPr>' + ('<w:b/>' if b else '') + '<w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
                runs.append(f'<w:r>{rpr}<w:t xml:space="preserve">{inner}</w:t></w:r>')
            if not runs:
                runs.append('<w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve"></w:t></w:r>')
            cell_pr = f'<w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/>{shading}</w:tcPr>'
            xml.append(f'<w:tc>{cell_pr}<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>{"".join(runs)}</w:p></w:tc>')
        xml.append('</w:tr>')
    xml.append('</w:tbl>')
    # add empty paragraph after a table (Word requirement to separate)
    xml.append(empty_para())
    return ''.join(xml)


def is_table_sep(line):
    return re.match(r'^\|[\s:\-|]+\|\s*$', line.strip()) is not None


def parse_row(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return [c.strip() for c in s.split('|')]


def convert():
    with open(MD, 'r') as f:
        lines = f.read().split('\n')

    body = []
    media = {}       # rid -> (arcname, filepath, ext)
    rels_extra = []  # relationship XML entries
    rid_counter = [10]  # start image rIds high to avoid clashing with styles rId1
    docpr_counter = [1]

    def add_image(fig_no):
        fname = FIG_FILES[fig_no]
        fpath = os.path.join(FIGDIR, fname)
        w, h = jpeg_dimensions(fpath)
        rid = f'rId{rid_counter[0]}'
        rid_counter[0] += 1
        arc = f'media/{fname}'
        media[rid] = (arc, fpath)
        rels_extra.append(
            f'<Relationship Id="{rid}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            f'Target="{arc}"/>'
        )
        docpr = docpr_counter[0]
        docpr_counter[0] += 1
        return image_paragraph(rid, w, h, docpr, fname)

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip()

        # Figure placeholder
        m = re.match(r'\*\*\[FIGURE (\d+) HERE\]\*\*', line.strip())
        if m:
            body.append(add_image(int(m.group(1))))
            i += 1
            continue

        # Table block
        if line.strip().startswith('|'):
            tbl_lines = []
            while i < n and lines[i].strip().startswith('|'):
                tbl_lines.append(lines[i])
                i += 1
            rows = [parse_row(l) for l in tbl_lines if not is_table_sep(l)]
            if rows:
                body.append(build_table(rows))
            continue

        if not line.strip():
            body.append(empty_para())
            i += 1
            continue

        # Horizontal rule
        if line.strip() == '---':
            body.append(empty_para())
            i += 1
            continue

        # Headings
        if line.startswith('#### '):
            body.append(para(line[5:].strip(), 'Heading3'))
        elif line.startswith('### '):
            body.append(para(line[4:].strip(), 'Heading3'))
        elif line.startswith('## '):
            body.append(para(line[3:].strip(), 'Heading1'))
        elif line.startswith('# '):
            body.append(para(line[2:].strip(), 'Title'))
        else:
            body.append(para(line.strip()))
        i += 1

    body_xml = '\n'.join(body)

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="jpg" ContentType="image/jpeg"/>'
        '<Default Extension="jpeg" ContentType="image/jpeg"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '</Types>'
    )

    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>'
    )

    doc_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        + ''.join(rels_extra) +
        '</Relationships>'
    )

    styles = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>'
        '<w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr>'
        '<w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:color w:val="1F4E79"/></w:rPr>'
        '<w:pPr><w:spacing w:before="320" w:after="120"/><w:keepNext/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="25"/><w:szCs w:val="25"/><w:color w:val="2E75B6"/></w:rPr>'
        '<w:pPr><w:spacing w:before="240" w:after="100"/><w:keepNext/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:i/><w:sz w:val="23"/><w:szCs w:val="23"/><w:color w:val="2E75B6"/></w:rPr>'
        '<w:pPr><w:spacing w:before="160" w:after="80"/><w:keepNext/></w:pPr></w:style>'
        '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/>'
        '<w:tblPr><w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '</w:tblBorders></w:tblPr></w:style>'
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
        '<w:body>'
        + body_xml +
        '<w:sectPr>'
        '<w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>'
        '</w:sectPr>'
        '</w:body></w:document>'
    )

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', root_rels)
        zf.writestr('word/_rels/document.xml.rels', doc_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', styles)
        for rid, (arc, fpath) in media.items():
            with open(fpath, 'rb') as imf:
                zf.writestr('word/' + arc, imf.read())

    print(f'Created {OUT}')
    print(f'  embedded images: {len(media)}')
    sz = os.path.getsize(OUT)
    print(f'  size: {sz/1024:.1f} KB')


if __name__ == '__main__':
    convert()
