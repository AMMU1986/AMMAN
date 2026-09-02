#!/usr/bin/env python3
"""
Build a Microsoft Word (.docx) file for the chapter
"Digital Twins and Intelligent Automation for Industry 5.0".

Converts the markdown source to OOXML and, unlike the earlier scripts in this
repository, EMBEDS the PNG figures inline as proper DrawingML images with the
required media parts and relationships.

Uses only the Python standard library (zipfile, struct, re).
"""

import zipfile
import os
import struct
import re

BASE = '/projects/sandbox/AMMAN'
MD_FILE = os.path.join(BASE, 'Chapter_Digital_Twins_Industry5.md')
FIG_DIR = os.path.join(BASE, 'dt_figures')
OUT_FILE = os.path.join(BASE, 'Chapter_Digital_Twins_Industry5.docx')

EMU_PER_PX = 9525          # 1 pixel at 96 dpi = 9525 EMU
MAX_WIDTH_EMU = 5486400    # ~6.0 inches, fits within 1-inch margins on Letter


# ─── styles.xml ───
STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault><w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:sz w:val="24"/><w:szCs w:val="24"/>
    </w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr>
      <w:spacing w:after="120" w:line="360" w:lineRule="auto"/>
    </w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/><w:pPr><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="240" w:after="240"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="36"/><w:szCs w:val="36"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="30"/><w:szCs w:val="30"/><w:color w:val="1F4E79"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="2E75B6"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Abstract">
    <w:name w:val="Abstract"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="720" w:right="720"/></w:pPr>
    <w:rPr><w:i/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Reference">
    <w:name w:val="Reference"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Caption">
    <w:name w:val="Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="240"/><w:keepLines/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ImagePara">
    <w:name w:val="ImagePara"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="160" w:after="0"/><w:keepNext/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="TableCaption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="180" w:after="80"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
</w:styles>'''

NUMBERING = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'


def png_size(path):
    with open(path, 'rb') as f:
        f.read(16)
        w, h = struct.unpack('>II', f.read(8))
    return w, h


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
    """Handle **bold** and *italic* inline markdown -> runs."""
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
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{parse_inline(text)}</w:p>'


def make_table(headers, rows):
    n = len(headers)
    col_w = 9360 // n
    xml = ['<w:tbl>']
    xml.append('<w:tblPr>'
               '<w:tblW w:w="9360" w:type="dxa"/>'
               '<w:tblLayout w:type="fixed"/>'
               '<w:tblBorders>'
               '<w:top w:val="single" w:sz="4" w:space="0" w:color="404040"/>'
               '<w:left w:val="single" w:sz="4" w:space="0" w:color="404040"/>'
               '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="404040"/>'
               '<w:right w:val="single" w:sz="4" w:space="0" w:color="404040"/>'
               '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="404040"/>'
               '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="404040"/>'
               '</w:tblBorders></w:tblPr>')
    xml.append('<w:tblGrid>' + f'<w:gridCol w:w="{col_w}"/>' * n + '</w:tblGrid>')
    # header row
    xml.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
    for h in headers:
        xml.append('<w:tc><w:tcPr>'
                   f'<w:tcW w:w="{col_w}" w:type="dxa"/>'
                   '<w:shd w:val="clear" w:color="auto" w:fill="1F4E79"/>'
                   '<w:vAlign w:val="center"/></w:tcPr>'
                   '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>'
                   f'<w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="21"/></w:rPr>'
                   f'<w:t xml:space="preserve">{escape_xml(h.strip())}</w:t></w:r></w:p></w:tc>')
    xml.append('</w:tr>')
    # data rows
    for ri, row in enumerate(rows):
        shade = 'F2F6FB' if ri % 2 == 0 else 'FFFFFF'
        xml.append('<w:tr>')
        for ci in range(n):
            cell = row[ci].strip() if ci < len(row) else ''
            xml.append('<w:tc><w:tcPr>'
                       f'<w:tcW w:w="{col_w}" w:type="dxa"/>'
                       f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>'
                       '<w:vAlign w:val="center"/></w:tcPr>'
                       '<w:p><w:pPr><w:spacing w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>'
                       f'<w:r><w:rPr><w:sz w:val="21"/></w:rPr>'
                       f'<w:t xml:space="preserve">{escape_xml(cell)}</w:t></w:r></w:p></w:tc>')
        xml.append('</w:tr>')
    xml.append('</w:tbl>')
    # spacer paragraph after table
    xml.append('<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>')
    return ''.join(xml)


def make_image_paragraph(rid, w_px, h_px, doc_pr_id, name):
    """Inline DrawingML image paragraph, scaled to fit page width."""
    w_emu = w_px * EMU_PER_PX
    h_emu = h_px * EMU_PER_PX
    if w_emu > MAX_WIDTH_EMU:
        scale = MAX_WIDTH_EMU / w_emu
        w_emu = int(w_emu * scale)
        h_emu = int(h_emu * scale)
    drawing = (
        '<w:r><w:drawing>'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
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
        f'<a:blip r:embed="{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
        '<a:stretch><a:fillRect/></a:stretch>'
        '</pic:blipFill>'
        '<pic:spPr>'
        f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{w_emu}" cy="{h_emu}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        '</pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic>'
        '</wp:inline></w:drawing></w:r>')
    return f'<w:p><w:pPr><w:pStyle w:val="ImagePara"/></w:pPr>{drawing}</w:p>'


def build():
    with open(MD_FILE, encoding='utf-8') as f:
        lines = f.read().split('\n')

    body = []
    images = []           # list of (rel_id, filename, media_name)
    rel_counter = 100     # relationship ids for images
    docpr_counter = 1
    in_refs = False
    in_abstract = False
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

        # Figure image marker: [[FIGURE:file|caption]]
        m = re.match(r'^\[\[FIGURE:([^|]+)\|(.+)\]\]$', stripped)
        if m:
            fname, caption = m.group(1), m.group(2)
            fpath = os.path.join(FIG_DIR, fname)
            w, h = png_size(fpath)
            rid = f'rIdImg{rel_counter}'
            media_name = f'media/image{docpr_counter}.png'
            images.append((rid, fpath, media_name))
            body.append(make_image_paragraph(rid, w, h, docpr_counter, fname))
            body.append(make_paragraph(caption, 'Caption'))
            rel_counter += 1
            docpr_counter += 1
            i += 1
            continue

        # Title
        if stripped.startswith('# ') and not stripped.startswith('## '):
            body.append(make_paragraph(stripped[2:], 'Title'))
            i += 1
            continue
        # H1
        if stripped.startswith('## '):
            heading = stripped[3:].strip()
            if heading.lower() == 'references':
                in_refs = True
                in_abstract = False
            elif heading.lower() == 'abstract':
                in_abstract = True
                in_refs = False
            else:
                in_abstract = False
            body.append(make_paragraph(heading, 'Heading1'))
            i += 1
            continue
        # H2
        if stripped.startswith('### '):
            body.append(make_paragraph(stripped[4:].strip(), 'Heading2'))
            i += 1
            continue
        # H3
        if stripped.startswith('#### '):
            body.append(make_paragraph(stripped[5:].strip(), 'Heading3'))
            i += 1
            continue

        # Table
        if '|' in line and i + 1 < len(lines) and re.search(r'\|\s*-', lines[i + 1]):
            headers = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2  # skip header + separator
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            body.append(make_table(headers, rows))
            continue

        # Table caption (**Table N.** ...)
        if stripped.startswith('**Table '):
            body.append(make_paragraph(stripped, 'TableCaption'))
            i += 1
            continue

        # Reference entry
        if in_refs and re.match(r'^\[\d+\]', stripped):
            body.append(make_paragraph(stripped, 'Reference'))
            i += 1
            continue

        # Abstract body paragraph -> italic indented block
        if in_abstract:
            body.append(make_paragraph(stripped, 'Abstract'))
            i += 1
            continue

        # Normal paragraph
        body.append(make_paragraph(stripped, 'Normal'))
        i += 1

    body_xml = '\n'.join(body)

    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<w:body>'
        f'{body_xml}'
        '<w:sectPr>'
        '<w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
        'w:header="720" w:footer="720" w:gutter="0"/>'
        '</w:sectPr>'
        '</w:body></w:document>')

    # Relationships (styles, numbering, + one per image)
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>']
    for rid, _, media_name in images:
        rels.append(f'<Relationship Id="{rid}" '
                    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                    f'Target="{media_name}"/>')
    rels.append('</Relationships>')
    word_rels = ''.join(rels)

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
        '</Types>')

    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>')

    with zipfile.ZipFile(OUT_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', root_rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES)
        zf.writestr('word/numbering.xml', NUMBERING)
        for _, fpath, media_name in images:
            with open(fpath, 'rb') as img:
                zf.writestr('word/' + media_name, img.read())

    size_kb = os.path.getsize(OUT_FILE) / 1024
    print(f"Created {OUT_FILE}")
    print(f"  Size: {size_kb:.1f} KB")
    print(f"  Embedded figures: {len(images)}")


if __name__ == '__main__':
    build()
