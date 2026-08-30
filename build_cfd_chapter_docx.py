#!/usr/bin/env python3
"""
Build the Word .docx for Chapter 12: Computational Fluid Dynamics and AI in
Drug Delivery. Renders markdown to OOXML with:
  - Title / Heading1-3 / Abstract / References / captions styles
  - Bordered tables with shaded header rows
  - Embedded PNG figures (DrawingML) placed after their first in-text citation
  - Figure captions

Pure standard library (no python-docx / no matplotlib needed).
"""

import zipfile
import os
import re
import struct

BASE = '/projects/sandbox/AMMAN'
MD_FILE = os.path.join(BASE, 'Chapter_CFD_AI_Drug_Delivery.md')
OUT_FILE = os.path.join(BASE, 'Chapter_CFD_AI_Drug_Delivery.docx')
FIG_DIR = os.path.join(BASE, 'cfd_figures')

# Map figure number -> (filename, caption). Image inserted after first citation.
FIGURES = {
    1: ('Figure_1_Airway_Deposition.png',
        'Figure 1. Representative airway model showing the dominant particle '
        'deposition mechanisms (impaction, sedimentation, and diffusion) and '
        'the predicted regional deposition profile across the respiratory tract.'),
    2: ('Figure_2_WSS_Nanoparticle.png',
        'Figure 2. Wall shear stress distribution in a bifurcating artery and '
        'the corresponding near-wall nanoparticle accumulation and margination '
        'toward the vessel wall.'),
    3: ('Figure_3_Surrogate_Workflow.png',
        'Figure 3. Typical CFD-machine learning surrogate workflow, comprising '
        'an offline training phase and near-instant online inference, with the '
        'accompanying reduction in computational time.'),
    4: ('Figure_4_Digital_Twin.png',
        'Figure 4. Architecture of a closed-loop CFD-AI digital twin for '
        'personalized drug delivery, showing the flow of information from '
        'patient data through model assimilation to a dosing recommendation.'),
}

EMU_PER_PIXEL = 9525  # 1 pixel at 96 dpi


# ─── OOXML templates ───

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1"><w:name w:val="Normal"/><w:pPr><w:jc w:val="both"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr><w:rPr><w:b/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="200" w:after="100"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Abstract"><w:name w:val="Abstract"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="576" w:right="576"/></w:pPr><w:rPr><w:i/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="References"><w:name w:val="References"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="FigureImage"><w:name w:val="Figure Image"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption"><w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="240"/></w:pPr><w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption"><w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="120" w:after="60"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
</w:styles>'''


def escape_xml(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


def make_run(text, bold=False, italic=False):
    props = ''
    if bold:
        props += '<w:b/>'
    if italic:
        props += '<w:i/>'
    rpr = f'<w:rPr>{props}</w:rPr>' if props else ''
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
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
    return f'<w:p>{ppr}{parse_inline(text)}</w:p>'


def make_table(headers, rows):
    n_cols = len(headers)
    col_w = 9200 // n_cols
    tbl = ('<w:tbl><w:tblPr><w:tblW w:w="9200" w:type="dxa"/>'
           '<w:tblLayout w:type="fixed"/><w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '</w:tblBorders></w:tblPr>')
    tbl += '<w:tblGrid>' + (f'<w:gridCol w:w="{col_w}"/>' * n_cols) + '</w:tblGrid>'
    # header
    tbl += '<w:tr><w:trPr><w:tblHeader/></w:trPr>'
    for h in headers:
        tbl += ('<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>'
                '<w:vAlign w:val="center"/></w:tcPr>'
                f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>'
                f'<w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{escape_xml(h.strip())}</w:t></w:r></w:p></w:tc>')
    tbl += '</w:tr>'
    # data
    for row in rows:
        tbl += '<w:tr>'
        for i in range(n_cols):
            cell = row[i].strip() if i < len(row) else ''
            tbl += ('<w:tc><w:tcPr><w:vAlign w:val="center"/></w:tcPr>'
                    f'<w:p><w:pPr><w:spacing w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>'
                    f'<w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{escape_xml(cell)}</w:t></w:r></w:p></w:tc>')
        tbl += '</w:tr>'
    tbl += '</w:tbl><w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>'
    return tbl


def png_dimensions(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('not a PNG: ' + path)
    w, h = struct.unpack('>II', head[16:24])
    return w, h


def make_image_paragraphs(fig_num, rel_id, width_px, height_px):
    """Image paragraph (scaled to fit page width) + caption paragraph."""
    max_w_px = 600  # fit within ~6.25in text width
    if width_px > max_w_px:
        scale = max_w_px / width_px
        width_px = int(width_px * scale)
        height_px = int(height_px * scale)
    cx = width_px * EMU_PER_PIXEL
    cy = height_px * EMU_PER_PIXEL
    name = f'Figure{fig_num}'
    drawing = (
        f'<w:p><w:pPr><w:pStyle w:val="FigureImage"/></w:pPr><w:r><w:drawing>'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0" '
        f'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        f'<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{fig_num}" name="{name}"/>'
        f'<wp:cNvGraphicFramePr><a:graphicFrameLocks '
        f'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        f'</wp:cNvGraphicFramePr>'
        f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr><pic:cNvPr id="{fig_num}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rel_id}" '
        f'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
        f'<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        f'</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'
    )
    caption = make_paragraph(FIGURES[fig_num][1], 'FigureCaption')
    return drawing + caption


def build():
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    # Figure relationships: rId2.. for images (rId1 = styles)
    fig_rel = {}  # fig_num -> rId
    rid = 2
    for n in sorted(FIGURES):
        fig_rel[n] = f'rId{rid}'
        rid += 1

    fig_inserted = set()
    elements = []
    in_references = False
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue
        if stripped == '---':
            i += 1
            continue

        # Title
        if line.startswith('# ') and not line.startswith('## '):
            elements.append(make_paragraph(line[2:].strip(), 'Title'))
            i += 1
            continue
        # Heading 1
        if line.startswith('## '):
            htext = line[3:].strip()
            if htext == 'References':
                in_references = True
            elements.append(make_paragraph(htext, 'Heading1'))
            i += 1
            continue
        if line.startswith('### '):
            elements.append(make_paragraph(line[4:].strip(), 'Heading2'))
            i += 1
            continue
        if line.startswith('#### '):
            elements.append(make_paragraph(line[5:].strip(), 'Heading3'))
            i += 1
            continue

        # Table caption (**Table N. ...**)
        if stripped.startswith('**Table') and stripped.endswith('**'):
            elements.append(make_paragraph(stripped.strip('*').strip(), 'TableCaption'))
            i += 1
            continue

        # Table
        if '|' in line and i + 1 < len(lines) and re.match(r'^\s*\|[\s\-:|]+\|\s*$', lines[i + 1]):
            headers = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            elements.append(make_table(headers, rows))
            continue

        # Reference entry
        if in_references and re.match(r'^\[\d+\]', stripped):
            elements.append(make_paragraph(stripped, 'References'))
            i += 1
            continue

        # Abstract paragraph (paragraph following the Abstract heading, before 12.1)
        # Determine style: italic abstract block
        # We track abstract by checking previous heading.
        style = 'Normal'
        elements.append(make_paragraph(stripped, style))

        # After adding a normal paragraph, check for first figure citation to insert image
        for n in sorted(FIGURES):
            if n not in fig_inserted and re.search(rf'\bFigure {n}\b', stripped):
                fname = FIGURES[n][0]
                w, h = png_dimensions(os.path.join(FIG_DIR, fname))
                elements.append(make_image_paragraphs(n, fig_rel[n], w, h))
                fig_inserted.add(n)
        i += 1

    # Mark abstract paragraphs as italic: find Abstract heading and style following paras
    # (simple post-process: convert the single abstract paragraph)
    body = '\n'.join(elements)
    # Style abstract: the paragraph(s) between Abstract heading and first Heading1 "12.1"
    body = style_abstract(body)

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<w:body>{body}'
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
        'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>'
    )

    # Build word/_rels/document.xml.rels
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>')
    for n in sorted(FIGURES):
        rels += (f'<Relationship Id="{fig_rel[n]}" '
                 f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                 f'Target="media/{FIGURES[n][0]}"/>')
    rels += '</Relationships>'

    with zipfile.ZipFile(OUT_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
        for n in sorted(FIGURES):
            with open(os.path.join(FIG_DIR, FIGURES[n][0]), 'rb') as imgf:
                zf.writestr(f'word/media/{FIGURES[n][0]}', imgf.read())

    if fig_inserted != set(FIGURES):
        print("  WARNING: not all figures inserted:", set(FIGURES) - fig_inserted)
    size_kb = os.path.getsize(OUT_FILE) / 1024
    print(f"Created {OUT_FILE} ({size_kb:.1f} KB)")
    print(f"Figures embedded: {sorted(fig_inserted)}")


def style_abstract(body):
    """Convert the abstract paragraph (between Abstract heading and 12.1 heading)
    from Normal to Abstract style."""
    # Find the Abstract heading paragraph
    abs_head = '<w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t xml:space="preserve">Abstract</w:t>'
    idx = body.find('Abstract</w:t>')
    if idx == -1:
        return body
    # Find start of next paragraph after the heading, up to the 12.1 heading
    start = body.find('</w:p>', idx)
    end = body.find('12.1 Fundamentals', idx)
    if start == -1 or end == -1:
        return body
    segment = body[start:end]
    styled = segment.replace('<w:pStyle w:val="Normal"/>', '<w:pStyle w:val="Abstract"/>')
    return body[:start] + styled + body[end:]


if __name__ == '__main__':
    build()
