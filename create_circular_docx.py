#!/usr/bin/env python3
"""
Build the Word .docx for the chapter
'Circular Economy and Recyclable 3D Printed Materials'.

Extends the raw-OOXML approach used elsewhere in this repo but adds support
for EMBEDDING PNG figures at '[Insert Figure N here]' placeholders.
Uses only the Python standard library (zipfile, struct, re).
"""

import zipfile
import os
import re
import struct

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(SCRIPT_DIR, 'Chapter_Circular_Economy_3D_Printing.md')
DOCX_FILE = os.path.join(SCRIPT_DIR, 'Chapter_Circular_Economy_3D_Printing.docx')
FIG_DIR = os.path.join(SCRIPT_DIR, 'circular_figures')

# Map figure number -> (filename, caption used in doc)
FIGURES = {
    1: 'Figure_1_Recycling_Degradation.png',
    2: 'Figure_2_Closed_Loop_Workflow.png',
    3: 'Figure_3_Embodied_Carbon.png',
    4: 'Figure_4_Digital_Ecosystem.png',
}

EMU_PER_PX = 9525
TARGET_WIDTH_EMU = 5486400  # 6 inches


def png_size(path):
    """Read width/height from a PNG IHDR chunk."""
    with open(path, 'rb') as f:
        header = f.read(24)
    if header[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError(f"Not a PNG: {path}")
    w, h = struct.unpack('>II', header[16:24])
    return w, h


# ─── OOXML boilerplate ───

def content_types():
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
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


def word_rels(image_rels):
    parts = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rid, target in image_rels:
        parts.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{target}"/>')
    parts.append('</Relationships>')
    return '\n'.join(parts)


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
  <w:style w:type="paragraph" w:styleId="Abstract"><w:name w:val="Abstract"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="720" w:right="720"/></w:pPr><w:rPr><w:i/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="References"><w:name w:val="References"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="FigureImg"><w:name w:val="Figure Image"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:before="200" w:after="60"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption"><w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="240"/></w:pPr><w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption"><w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="160" w:after="60"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
</w:styles>'''


def escape_xml(text):
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    return text


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
    pattern = r'(\*\*.*?\*\*|\*[^*]+?\*)'
    for part in re.split(pattern, text):
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


def make_image_paragraph(rid, w_emu, h_emu, name):
    """Inline image paragraph."""
    drawing = f'''<w:p><w:pPr><w:pStyle w:val="FigureImg"/></w:pPr><w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
<wp:extent cx="{w_emu}" cy="{h_emu}"/>
<wp:effectExtent l="0" t="0" r="0" b="0"/>
<wp:docPr id="{rid[3:]}" name="{name}"/>
<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>
<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:nvPicPr><pic:cNvPr id="{rid[3:]}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed="{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{w_emu}" cy="{h_emu}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''
    return drawing


def make_table(headers, rows):
    n_cols = len(headers)
    col_w = 9360 // n_cols
    tbl = ['<w:tbl>',
           '<w:tblPr>',
           '<w:tblW w:w="9360" w:type="dxa"/>',
           '<w:tblLayout w:type="fixed"/>',
           '<w:tblBorders>',
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '</w:tblBorders>',
           '</w:tblPr>',
           '<w:tblGrid>' + (f'<w:gridCol w:w="{col_w}"/>' * n_cols) + '</w:tblGrid>']
    # header row
    tbl.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
    for h in headers:
        tbl.append('<w:tc><w:tcPr>'
                   f'<w:tcW w:w="{col_w}" w:type="dxa"/>'
                   '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>'
                   '<w:vAlign w:val="center"/></w:tcPr>'
                   f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>{make_run(h.strip(), bold=True)}</w:p></w:tc>')
    tbl.append('</w:tr>')
    # data rows
    for row in rows:
        tbl.append('<w:tr>')
        for i in range(n_cols):
            cell = row[i].strip() if i < len(row) else ''
            tbl.append('<w:tc>'
                       f'<w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
                       f'<w:p><w:pPr><w:spacing w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>{make_run(cell)}</w:p></w:tc>')
        tbl.append('</w:tr>')
    tbl.append('</w:tbl>')
    # spacer paragraph after table
    tbl.append('<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>')
    return ''.join(tbl)


def build():
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    # Pre-compute image sizing + relationships
    image_rels = []   # (rId, target)
    image_meta = {}   # fig_num -> (rId, w_emu, h_emu)
    media_files = {}  # target -> source path
    rid_counter = 100
    for num in sorted(FIGURES):
        path = os.path.join(FIG_DIR, FIGURES[num])
        w_px, h_px = png_size(path)
        w_emu = TARGET_WIDTH_EMU
        h_emu = int(TARGET_WIDTH_EMU * h_px / w_px)
        rid = f'rId{rid_counter}'
        rid_counter += 1
        target = f'media/{FIGURES[num]}'
        image_rels.append((rid, target))
        media_files[f'word/{target}'] = path
        image_meta[num] = (rid, w_emu, h_emu)

    elements = []
    in_references = False
    in_abstract = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.strip() == '---':
            i += 1
            continue

        # Title
        if line.startswith('# ') and not line.startswith('## '):
            elements.append(make_paragraph(line[2:].strip(), 'Title'))
            i += 1
            continue

        # H1 (##)
        if line.startswith('## '):
            heading = line[3:].strip()
            in_abstract = (heading.lower() == 'abstract')
            in_references = (heading.lower() == 'references')
            elements.append(make_paragraph(heading, 'Heading1'))
            i += 1
            continue

        # H2 (###)
        if line.startswith('### '):
            elements.append(make_paragraph(line[4:].strip(), 'Heading2'))
            i += 1
            continue

        # H3 (####)
        if line.startswith('#### '):
            elements.append(make_paragraph(line[5:].strip(), 'Heading3'))
            i += 1
            continue

        # Image placeholder: [Insert Figure N here]
        m = re.match(r'\[Insert Figure (\d+) here\]', line.strip())
        if m:
            num = int(m.group(1))
            rid, w_emu, h_emu = image_meta[num]
            elements.append(make_image_paragraph(rid, w_emu, h_emu, f'Figure {num}'))
            i += 1
            continue

        # Figure caption
        if re.match(r'^Figure \d+:', line.strip()):
            elements.append(make_paragraph(line.strip(), 'FigureCaption'))
            i += 1
            continue

        # Table caption (Table N: ... without pipes)
        if re.match(r'^Table \d+:', line.strip()) and '|' not in line:
            elements.append(make_paragraph(line.strip(), 'TableCaption'))
            i += 1
            continue

        # Markdown table
        if '|' in line and i + 1 < len(lines) and re.search(r'\|?\s*-{2,}', lines[i + 1]):
            headers = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            elements.append(make_table(headers, rows))
            continue

        # Reference entry
        if in_references and re.match(r'^\[\d+\]', line.strip()):
            elements.append(make_paragraph(line.strip(), 'References'))
            i += 1
            continue

        # Abstract body
        if in_abstract:
            elements.append(make_paragraph(line.strip(), 'Abstract'))
            i += 1
            continue

        elements.append(make_paragraph(line.strip(), 'Normal'))
        i += 1

    body = '\n'.join(elements)
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{body}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    with zipfile.ZipFile(DOCX_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types())
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', word_rels(image_rels))
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
        for target, src in media_files.items():
            with open(src, 'rb') as imgf:
                zf.writestr(target, imgf.read())

    size_kb = os.path.getsize(DOCX_FILE) / 1024
    print(f"Created: {DOCX_FILE}")
    print(f"Size: {size_kb:.1f} KB")
    print(f"Embedded figures: {len(media_files)}")


if __name__ == '__main__':
    build()
