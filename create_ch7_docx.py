#!/usr/bin/env python3
"""
Create a Word .docx for Chapter 7 (AI in Drug Toxicology and Safety).
Converts markdown to OOXML and embeds the 4 PNG figures inline.
Uses only the Python standard library (zipfile + struct for PNG size).
"""

import zipfile
import os
import re
import struct

BASE = '/projects/sandbox/AMMAN'
MD_FILE = os.path.join(BASE, 'Chapter_7_AI_Drug_Toxicology_Safety.md')
OUT_FILE = os.path.join(BASE, 'Chapter_7_AI_Drug_Toxicology_Safety.docx')
FIG_DIR = os.path.join(BASE, 'ch7_figures')

FIGURE_MAP = {
    'Figure 7.1.': 'Figure_7_1_Multimodal_Toxicity.png',
    'Figure 7.2.': 'Figure_7_2_DDI_Mechanisms.png',
    'Figure 7.3.': 'Figure_7_3_Safety_Continuum.png',
    'Figure 7.4.': 'Figure_7_4_Pharmacovigilance.png',
}

EMU_PER_PX = 9525  # EMU per pixel at 96 dpi


def png_size(path):
    with open(path, 'rb') as f:
        data = f.read(24)
    w, h = struct.unpack('>II', data[16:24])
    return w, h


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
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/><w:keepNext/></w:pPr><w:rPr><w:b/><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/><w:keepNext/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="200" w:after="100"/><w:jc w:val="left"/><w:keepNext/></w:pPr><w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Abstract"><w:name w:val="Abstract"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="576" w:right="576"/></w:pPr><w:rPr><w:i/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="References"><w:name w:val="References"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="FigureImage"><w:name w:val="Figure Image"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption"><w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="240"/></w:pPr><w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption"><w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="180" w:after="60"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
</w:styles>'''


def escape_xml(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


def make_run(text, bold=False, italic=False):
    props = []
    if bold:
        props.append('<w:b/>')
    if italic:
        props.append('<w:i/>')
    rpr = ('<w:rPr>' + ''.join(props) + '</w:rPr>') if props else ''
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


def make_image_paragraph(rel_id, cx_emu, cy_emu, name):
    return f'''<w:p><w:pPr><w:pStyle w:val="FigureImage"/></w:pPr><w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
<wp:extent cx="{cx_emu}" cy="{cy_emu}"/>
<wp:effectExtent l="0" t="0" r="0" b="0"/>
<wp:docPr id="{rel_id[3:]}" name="{name}"/>
<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>
<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:nvPicPr><pic:cNvPr id="{rel_id[3:]}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed="{rel_id}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx_emu}" cy="{cy_emu}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''


def make_table(headers, rows):
    n_cols = len(headers)
    col_w = 9360 // n_cols
    tbl = ('<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '</w:tblBorders></w:tblPr>')
    tbl += '<w:tblGrid>' + (f'<w:gridCol w:w="{col_w}"/>' * n_cols) + '</w:tblGrid>'
    tbl += '<w:tr><w:trPr><w:tblHeader/></w:trPr>'
    for h in headers:
        tbl += ('<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>'
                f'<w:p><w:pPr><w:jc w:val="left"/><w:spacing w:after="40"/></w:pPr>{make_run(h.strip(), bold=True)}</w:p></w:tc>')
    tbl += '</w:tr>'
    for row in rows:
        tbl += '<w:tr>'
        for cell in row:
            tbl += ('<w:tc>'
                    f'<w:p><w:pPr><w:jc w:val="left"/><w:spacing w:after="40"/></w:pPr>{parse_inline(cell.strip())}</w:p></w:tc>')
        for _ in range(n_cols - len(row)):
            tbl += '<w:tc><w:p/></w:tc>'
        tbl += '</w:tr>'
    tbl += '</w:tbl><w:p/>'
    return tbl


def build():
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    elements = []
    image_rels = []
    rel_counter = 10
    in_references = False
    in_abstract = False
    i = 0

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        if line.startswith('# ') and not line.startswith('## '):
            elements.append(make_paragraph(line[2:].strip(), 'Title'))
            i += 1
            continue
        if line.startswith('## '):
            txt = line[3:].strip()
            in_references = (txt == 'References')
            in_abstract = (txt == 'Abstract')
            elements.append(make_paragraph(txt, 'Heading1'))
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
        # Table
        if '|' in line and i + 1 < len(lines) and re.search(r'\|\s*---', lines[i + 1]):
            headers = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            elements.append(make_table(headers, rows))
            continue
        # Figure caption -> image then caption
        fig_key = next((k for k in FIGURE_MAP if line.strip().startswith(k)), None)
        if fig_key:
            png_path = os.path.join(FIG_DIR, FIGURE_MAP[fig_key])
            rid = f'rId{rel_counter}'
            rel_counter += 1
            image_rels.append((rid, FIGURE_MAP[fig_key]))
            w, h = png_size(png_path)
            max_w = 5486400
            cx = w * EMU_PER_PX
            cy = h * EMU_PER_PX
            if cx > max_w:
                scale = max_w / cx
                cx = int(cx * scale)
                cy = int(cy * scale)
            elements.append(make_image_paragraph(rid, cx, cy, FIGURE_MAP[fig_key]))
            elements.append(make_paragraph(line.strip(), 'FigureCaption'))
            i += 1
            continue
        # Table caption
        if re.match(r'^Table 7\.\d+\.', line.strip()):
            elements.append(make_paragraph(line.strip(), 'TableCaption'))
            i += 1
            continue
        # References
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

    word_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rid, fname in image_rels:
        word_rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{fname}"/>')
    word_rels.append('</Relationships>')
    word_rels_xml = '\n'.join(word_rels)

    with zipfile.ZipFile(OUT_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', word_rels_xml)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
        for rid, fname in image_rels:
            with open(os.path.join(FIG_DIR, fname), 'rb') as imgf:
                zf.writestr(f'word/media/{fname}', imgf.read())

    size_kb = os.path.getsize(OUT_FILE) / 1024
    print(f"Created: {OUT_FILE}")
    print(f"Size: {size_kb:.1f} KB")
    print(f"Embedded figures: {len(image_rels)}")
    for rid, fname in image_rels:
        print(f"  {rid} -> {fname}")


if __name__ == '__main__':
    build()
