#!/usr/bin/env python3
"""
Build a downloadable Word (.docx) file for the chapter:
"Reporting CSR and ESG Performance: Leveraging AI for Sustainability Measurement".

Pure standard library only (python-docx / PIL are NOT available in this sandbox).
Extends the raw-OOXML approach of create_chapter_docx.py to EMBED PNG figures
inline at their caption positions.
"""

import zipfile
import os
import re
import struct

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(SCRIPT_DIR, 'Chapter_CSR_ESG_AI.md')
DOCX_FILE = os.path.join(SCRIPT_DIR, 'Chapter_CSR_ESG_AI_Leveraging_AI.docx')
FIG_DIR = os.path.join(SCRIPT_DIR, 'csr_esg_figures')

EMU_PER_PX = 9525          # 96 dpi
MAX_WIDTH_EMU = 5486400    # 6 inches

# Map figure number -> png file
FIGURES = {
    1: os.path.join(FIG_DIR, 'Figure_1.png'),
    2: os.path.join(FIG_DIR, 'Figure_2.png'),
    3: os.path.join(FIG_DIR, 'Figure_3.png'),
    4: os.path.join(FIG_DIR, 'Figure_4.png'),
}


# ─── OOXML boilerplate ───

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
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Abstract">
    <w:name w:val="Abstract"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="720" w:right="720"/></w:pPr><w:rPr><w:i/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="References">
    <w:name w:val="References"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureImage">
    <w:name w:val="Figure Image"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="40"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="240"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="60"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
</w:styles>'''


def escape_xml(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


def png_size(path):
    """Read PNG width/height from IHDR (pure stdlib)."""
    with open(path, 'rb') as f:
        data = f.read(33)
    # bytes 16..24 hold width,height as big-endian uint32 after 8-byte sig + IHDR len/type
    w, h = struct.unpack('>II', data[16:24])
    return w, h


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
    for part in re.split(r'(\*\*.*?\*\*|\*[^*]+?\*)', text):
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


def make_image_paragraph(rid, cx_emu, cy_emu, name, docpr_id):
    """Inline drawing paragraph for an embedded image."""
    drawing = (
        '<w:r><w:drawing>'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        f'<wp:extent cx="{cx_emu}" cy="{cy_emu}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{docpr_id}" name="{name}"/>'
        '<wp:cNvGraphicFramePr>'
        '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr>'
        f'<pic:cNvPr id="{docpr_id}" name="{name}"/>'
        '<pic:cNvPicPr/>'
        '</pic:nvPicPr>'
        '<pic:blipFill>'
        f'<a:blip r:embed="{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
        '<a:stretch><a:fillRect/></a:stretch>'
        '</pic:blipFill>'
        '<pic:spPr>'
        '<a:xfrm><a:off x="0" y="0"/>'
        f'<a:ext cx="{cx_emu}" cy="{cy_emu}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        '</pic:spPr>'
        '</pic:pic>'
        '</a:graphicData>'
        '</a:graphic>'
        '</wp:inline>'
        '</w:drawing></w:r>'
    )
    return f'<w:p><w:pPr><w:pStyle w:val="FigureImage"/></w:pPr>{drawing}</w:p>'


def make_table(headers, rows):
    n_cols = len(headers)
    col_w = 9360 // n_cols
    tbl = ['<w:tbl>']
    tbl.append('<w:tblPr><w:tblW w:w="9360" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
               '<w:tblBorders>'
               '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '</w:tblBorders></w:tblPr>')
    tbl.append('<w:tblGrid>' + (f'<w:gridCol w:w="{col_w}"/>' * n_cols) + '</w:tblGrid>')
    # header
    tbl.append('<w:tr>')
    for h in headers:
        tbl.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>'
                   '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>'
                   '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="20"/></w:pPr>%s</w:p></w:tc>'
                   % (col_w, make_run(h.strip(), bold=True)))
    tbl.append('</w:tr>')
    # rows
    for row in rows:
        tbl.append('<w:tr>')
        for i in range(n_cols):
            cell = row[i].strip() if i < len(row) else ''
            tbl.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/></w:tcPr>'
                       '<w:p><w:pPr><w:spacing w:after="20"/></w:pPr>%s</w:p></w:tc>'
                       % (col_w, make_run(cell)))
        tbl.append('</w:tr>')
    tbl.append('</w:tbl>')
    # trailing empty paragraph (Word requires a p after a table)
    tbl.append('<w:p/>')
    return ''.join(tbl)


def build():
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    # Pre-compute image relationships / sizing
    image_rels = []          # (rId, media_path_in_zip)
    fig_rid = {}
    fig_dims = {}
    rid_counter = 3          # rId1=styles, rId2=numbering
    media = {}               # arcname -> source path
    for num in sorted(FIGURES):
        path = FIGURES[num]
        w, h = png_size(path)
        cx = w * EMU_PER_PX
        cy = h * EMU_PER_PX
        if cx > MAX_WIDTH_EMU:
            scale = MAX_WIDTH_EMU / cx
            cx = int(cx * scale)
            cy = int(cy * scale)
        rid = f'rId{rid_counter}'
        rid_counter += 1
        arc = f'media/image{num}.png'
        fig_rid[num] = rid
        fig_dims[num] = (cx, cy)
        image_rels.append((rid, arc))
        media[f'word/{arc}'] = path

    elements = []
    i = 0
    in_references = False
    in_abstract = False
    docpr_id = 100
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.strip() == '---':
            i += 1
            continue
        if line.startswith('# ') and not line.startswith('## '):
            elements.append(make_paragraph(line[2:].strip(), 'Title'))
            i += 1
            continue
        if line.startswith('## '):
            htext = line[3:].strip()
            in_abstract = (htext == 'Abstract')
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

        # Abstract body paragraph (between "## Abstract" heading and first "## Section")
        # handled as Normal below; abstract heading matched above.

        # Markdown table
        if '|' in line and i + 1 < len(lines) and re.search(r'\|\s*-', lines[i + 1]):
            headers = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            elements.append(make_table(headers, rows))
            continue

        # Figure caption -> insert IMAGE then caption
        m = re.match(r'^Figure (\d+):', line.strip())
        if m:
            num = int(m.group(1))
            if num in fig_rid:
                cx, cy = fig_dims[num]
                elements.append(make_image_paragraph(
                    fig_rid[num], cx, cy, f'Figure {num}', docpr_id))
                docpr_id += 1
            elements.append(make_paragraph(line.strip(), 'FigureCaption'))
            i += 1
            continue

        # Table caption
        if re.match(r'^Table \d+:', line.strip()):
            elements.append(make_paragraph(line.strip(), 'TableCaption'))
            i += 1
            continue

        # Reference entry
        if in_references and re.match(r'^\[\d+\]', line.strip()):
            elements.append(make_paragraph(line.strip(), 'References'))
            i += 1
            continue

        # Abstract paragraph gets the Abstract style; everything else Normal
        style = 'Abstract' if in_abstract else 'Normal'
        elements.append(make_paragraph(line.strip(), style))
        i += 1

    body_xml = '\n'.join(elements)

    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{body_xml}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    # word rels including images
    rel_lines = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
        '  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
        '  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>',
    ]
    for rid, arc in image_rels:
        rel_lines.append(
            f'  <Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{arc}"/>')
    rel_lines.append('</Relationships>')
    word_rels = '\n'.join(rel_lines)

    with zipfile.ZipFile(DOCX_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES)
        zf.writestr('word/numbering.xml', NUMBERING)
        for arcname, src in media.items():
            zf.write(src, arcname)

    size_kb = os.path.getsize(DOCX_FILE) / 1024
    print(f"Created: {DOCX_FILE}")
    print(f"Size: {size_kb:.1f} KB")
    print(f"Embedded {len(media)} figures")


if __name__ == '__main__':
    build()
