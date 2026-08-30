#!/usr/bin/env python3
"""
Create a Word .docx file for the chapter
"Smart Biomaterials and Drug-Eluting Medical Devices".

Uses the raw-OOXML approach (python-docx is unavailable in this sandbox) and
embeds the generated PNG figures inline where the "[Insert Figure N here]"
placeholders appear. Markdown pipe-tables are rendered as native Word tables.

Usage:
    python3 create_biomaterials_docx.py
"""

import zipfile
import os
import re
import struct

MD_FILE = '/projects/sandbox/AMMAN/Chapter_Smart_Biomaterials_Drug_Eluting_Devices.md'
DOCX_FILE = '/projects/sandbox/AMMAN/Chapter_Smart_Biomaterials_Drug_Eluting_Devices.docx'
FIG_DIR = '/projects/sandbox/AMMAN/biomaterials_figures'

FIGURE_FILES = {
    1: 'Figure_1_Smart_Biomaterials_Classification.png',
    2: 'Figure_2_Drug_Eluting_Implant_Architecture.png',
    3: 'Figure_3_Drug_Release_Kinetics.png',
    4: 'Figure_4_AI_Design_Workflow.png',
}

EMU_PER_INCH = 914400
TARGET_WIDTH_INCHES = 6.0

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
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="120" w:line="360" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
    <w:pPr><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Abstract">
    <w:name w:val="Abstract"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="720" w:right="720"/></w:pPr>
    <w:rPr><w:i/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="References">
    <w:name w:val="References"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="240"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureImage">
    <w:name w:val="Figure Image"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="200" w:after="0"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="Table Caption"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="60"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr>
      <w:tblBorders>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      </w:tblBorders>
    </w:tblPr>
  </w:style>
</w:styles>'''


def png_dimensions(path):
    with open(path, 'rb') as f:
        header = f.read(24)
    if header[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError(f'Not a PNG file: {path}')
    width, height = struct.unpack('>II', header[16:24])
    return width, height


def escape_xml(text):
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    return text


def make_run(text, bold=False, italic=False):
    props = []
    if bold:
        props.append('<w:b/>')
    if italic:
        props.append('<w:i/>')
    rpr = ''
    if props:
        rpr = '<w:rPr>' + ''.join(props) + '</w:rPr>'
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'


def parse_inline(text):
    runs = []
    pattern = r'(\*\*.*?\*\*|\*[^*]+?\*)'
    parts = re.split(pattern, text)
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
    runs = parse_inline(text)
    return f'<w:p>{ppr}{runs}</w:p>'


def make_image_paragraph(rel_id, img_index, cx_emu, cy_emu, name):
    doc_pr_id = 1000 + img_index
    drawing = (
        '<w:r><w:drawing>'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        f'<wp:extent cx="{cx_emu}" cy="{cy_emu}"/>'
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
        f'<a:blip r:embed="{rel_id}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
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
    tbl = '<w:tbl>'
    tbl += '<w:tblPr>'
    tbl += '<w:tblStyle w:val="TableGrid"/>'
    tbl += '<w:tblW w:w="9360" w:type="dxa"/>'
    tbl += '<w:tblLayout w:type="fixed"/>'
    tbl += '<w:tblBorders>'
    tbl += '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '</w:tblBorders>'
    tbl += '</w:tblPr>'
    tbl += '<w:tblGrid>' + (f'<w:gridCol w:w="{col_w}"/>' * n_cols) + '</w:tblGrid>'

    tbl += '<w:tr><w:trPr><w:tblHeader/></w:trPr>'
    for h in headers:
        tbl += '<w:tc>'
        tbl += f'<w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/><w:vAlign w:val="center"/></w:tcPr>'
        tbl += f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="40"/></w:pPr>{make_run(h.strip(), bold=True)}</w:p>'
        tbl += '</w:tc>'
    tbl += '</w:tr>'

    for row in rows:
        tbl += '<w:tr>'
        for cell in row:
            tbl += '<w:tc>'
            tbl += f'<w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/></w:tcPr>'
            tbl += f'<w:p><w:pPr><w:jc w:val="left"/><w:spacing w:after="40"/></w:pPr>{make_run(cell.strip())}</w:p>'
            tbl += '</w:tc>'
        for _ in range(n_cols - len(row)):
            tbl += f'<w:tc><w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/></w:tcPr><w:p/></w:tc>'
        tbl += '</w:tr>'

    tbl += '</w:tbl>'
    # A trailing empty paragraph keeps tables from butting into following text.
    return tbl + '<w:p/>'


def md_to_body(md_text, image_rels):
    elements = []
    lines = md_text.split('\n')
    i = 0
    in_references = False
    in_abstract = False
    img_counter = 0

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
            heading_text = line[3:].strip()
            in_references = (heading_text == 'References')
            in_abstract = (heading_text == 'Abstract')
            elements.append(make_paragraph(heading_text, 'Heading1'))
            i += 1
            continue

        if line.startswith('### '):
            in_abstract = False
            elements.append(make_paragraph(line[4:].strip(), 'Heading2'))
            i += 1
            continue

        if line.startswith('#### '):
            elements.append(make_paragraph(line[5:].strip(), 'Heading3'))
            i += 1
            continue

        # Table detection (pipe table with separator row next)
        if '|' in line and i + 1 < len(lines) and re.match(r'^\s*\|?[\s:|-]+\|', lines[i + 1]) and '---' in lines[i + 1]:
            headers = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                row = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                rows.append(row)
                i += 1
            elements.append(make_table(headers, rows))
            continue

        # Figure placeholder -> embed actual image
        m = re.match(r'\[Insert Figure (\d+) here\]', line.strip())
        if m:
            fig_num = int(m.group(1))
            fname = FIGURE_FILES.get(fig_num)
            fpath = os.path.join(FIG_DIR, fname) if fname else None
            if fpath and os.path.exists(fpath):
                img_counter += 1
                rel_id = f'rIdImg{img_counter}'
                image_rels.append((rel_id, fname))
                px_w, px_h = png_dimensions(fpath)
                cx = int(TARGET_WIDTH_INCHES * EMU_PER_INCH)
                cy = int(cx * px_h / px_w)
                elements.append(make_image_paragraph(rel_id, img_counter, cx, cy, fname))
            else:
                elements.append(make_paragraph(line.strip(), 'FigureCaption'))
            i += 1
            continue

        # Figure caption line
        if re.match(r'^Figure \d+\.', line.strip()):
            elements.append(make_paragraph(line.strip(), 'FigureCaption'))
            i += 1
            continue

        # Table caption (**Table N.** ...)
        if line.strip().startswith('**Table '):
            elements.append(make_paragraph(line.strip(), 'TableCaption'))
            i += 1
            continue

        # References entries
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

    return '\n'.join(elements)


def build_word_rels(image_rels):
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rel_id, fname in image_rels:
        rels.append(
            f'  <Relationship Id="{rel_id}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            f'Target="media/{fname}"/>')
    rels.append('</Relationships>')
    return '\n'.join(rels)


def create_docx(md_filepath, output_filepath):
    with open(md_filepath, 'r', encoding='utf-8') as f:
        md_content = f.read()

    image_rels = []
    body_xml = md_to_body(md_content, image_rels)

    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{body_xml}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"
               w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    word_rels = build_word_rels(image_rels)

    with zipfile.ZipFile(output_filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES)
        for _, fname in image_rels:
            with open(os.path.join(FIG_DIR, fname), 'rb') as img:
                zf.writestr(f'word/media/{fname}', img.read())

    size_kb = os.path.getsize(output_filepath) / 1024
    print(f"Successfully created: {output_filepath}")
    print(f"Embedded {len(image_rels)} figure(s): "
          f"{', '.join(fn for _, fn in image_rels)}")
    print(f"File size: {size_kb:.1f} KB")


if __name__ == '__main__':
    create_docx(MD_FILE, DOCX_FILE)
