#!/usr/bin/env python3
"""
Create a downloadable Word (.docx) document for Chapter 14:
AI in Pharmacogenomics and Precision Medicine.

Renders the markdown source into OOXML, produces real Word tables,
and EMBEDS the four PNG figures as actual inline images (not just
captions). Uses only the Python standard library (zipfile + struct).
"""

import zipfile
import os
import re
import struct

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(BASE_DIR, 'Chapter_14_AI_Pharmacogenomics_Precision_Medicine.md')
DOCX_FILE = os.path.join(BASE_DIR, 'Chapter_14_AI_Pharmacogenomics_Precision_Medicine.docx')
FIG_DIR = os.path.join(BASE_DIR, 'chapter14_figures')

EMU_PER_PX = 9525  # 1 pixel = 9525 EMU at 96 DPI
MAX_IMG_WIDTH_PX = 600  # cap displayed width so images fit the page


# ─────────────────────────── PNG helpers ───────────────────────────

def png_dimensions(path):
    """Read width/height from a PNG IHDR chunk."""
    with open(path, 'rb') as f:
        header = f.read(24)
    if header[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError(f'Not a PNG file: {path}')
    w, h = struct.unpack('>II', header[16:24])
    return w, h


# ─────────────────────────── XML helpers ───────────────────────────

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
    rpr = ('<w:rPr>' + ''.join(props) + '</w:rPr>') if props else ''
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'


def parse_inline(text):
    """Parse **bold**, *italic*, and drop image markdown."""
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


def make_image_paragraph(rid, width_px, height_px, name):
    """Create a centered paragraph containing an inline image (drawing)."""
    # Scale down if wider than page area.
    if width_px > MAX_IMG_WIDTH_PX:
        scale = MAX_IMG_WIDTH_PX / width_px
        width_px = int(width_px * scale)
        height_px = int(height_px * scale)
    cx = width_px * EMU_PER_PX
    cy = height_px * EMU_PER_PX
    drawing = (
        '<w:drawing>'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{rid}" name="{escape_xml(name)}"/>'
        '<wp:cNvGraphicFramePr>'
        '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr>'
        f'<pic:cNvPr id="{rid}" name="{escape_xml(name)}"/>'
        '<pic:cNvPicPr/>'
        '</pic:nvPicPr>'
        '<pic:blipFill>'
        f'<a:blip r:embed="rId{rid}"/>'
        '<a:stretch><a:fillRect/></a:stretch>'
        '</pic:blipFill>'
        '<pic:spPr>'
        f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        '</pic:spPr>'
        '</pic:pic>'
        '</a:graphicData>'
        '</a:graphic>'
        '</wp:inline>'
        '</w:drawing>'
    )
    return f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/></w:pPr><w:r>{drawing}</w:r></w:p>'


def make_table(headers, rows):
    n_cols = len(headers)
    col_w = 9360 // n_cols
    tbl = ['<w:tbl>']
    tbl.append('<w:tblPr>')
    tbl.append('<w:tblStyle w:val="TableGrid"/>')
    tbl.append('<w:tblW w:w="9360" w:type="dxa"/>')
    tbl.append('<w:tblLayout w:type="fixed"/>')
    tbl.append('<w:tblBorders>')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        tbl.append(f'<w:{edge} w:val="single" w:sz="4" w:space="0" w:color="000000"/>')
    tbl.append('</w:tblBorders>')
    tbl.append('</w:tblPr>')
    tbl.append('<w:tblGrid>' + (f'<w:gridCol w:w="{col_w}"/>' * n_cols) + '</w:tblGrid>')

    # header row
    tbl.append('<w:tr>')
    for h in headers:
        tbl.append('<w:tc>')
        tbl.append(f'<w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>')
        tbl.append(f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="40"/></w:pPr>{make_run(h.strip(), bold=True)}</w:p>')
        tbl.append('</w:tc>')
    tbl.append('</w:tr>')

    # data rows
    for row in rows:
        tbl.append('<w:tr>')
        for i in range(n_cols):
            cell = row[i].strip() if i < len(row) else ''
            tbl.append('<w:tc>')
            tbl.append(f'<w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/></w:tcPr>')
            tbl.append(f'<w:p><w:pPr><w:spacing w:after="40"/></w:pPr>{parse_inline(cell)}</w:p>')
            tbl.append('</w:tc>')
        tbl.append('</w:tr>')
    tbl.append('</w:tbl>')
    # a trailing empty paragraph so consecutive tables/text separate cleanly
    tbl.append('<w:p/>')
    return ''.join(tbl)


# ─────────────────────────── markdown -> body ───────────────────────────

def md_to_body(md_text, images):
    """
    Convert markdown to OOXML body. `images` is a list that will be
    populated with (rel_id, filename, arcname) tuples for each embedded image.
    """
    elements = []
    lines = md_text.split('\n')
    i = 0
    in_references = False
    next_rid = 100  # image relationship ids start high to avoid clashes

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped == '---':
            i += 1
            continue

        # Image: ![alt](path)
        m = re.match(r'!\[.*?\]\((.+?)\)', stripped)
        if m:
            rel_path = m.group(1)
            fname = os.path.basename(rel_path)
            full_path = os.path.join(FIG_DIR, fname)
            if os.path.exists(full_path):
                w, h = png_dimensions(full_path)
                rid = next_rid
                next_rid += 1
                arcname = f'word/media/{fname}'
                images.append((rid, full_path, arcname))
                elements.append(make_image_paragraph(rid, w, h, fname))
            else:
                elements.append(make_paragraph(f'[Missing image: {fname}]', 'Normal'))
            i += 1
            continue

        # Title (# ) — the chapter title
        if line.startswith('# ') and not line.startswith('## '):
            elements.append(make_paragraph(line[2:].strip(), 'Title'))
            i += 1
            continue

        # Heading 1 (## )
        if line.startswith('## '):
            heading = line[3:].strip()
            if heading == 'References':
                in_references = True
            if heading == 'Abstract':
                elements.append(make_paragraph(heading, 'Heading1'))
                i += 1
                # following abstract paragraphs handled as normal
                continue
            elements.append(make_paragraph(heading, 'Heading1'))
            i += 1
            continue

        # Heading 2 (### )
        if line.startswith('### '):
            elements.append(make_paragraph(line[4:].strip(), 'Heading2'))
            i += 1
            continue

        # Heading 3 (#### )
        if line.startswith('#### '):
            elements.append(make_paragraph(line[5:].strip(), 'Heading3'))
            i += 1
            continue

        # Table (line with | followed by a separator row of ---)
        if '|' in line and i + 1 < len(lines) and re.search(r'\|?\s*-{2,}', lines[i + 1]) and '|' in lines[i + 1]:
            headers = [c.strip() for c in line.split('|') if c.strip()]
            i += 2  # skip header + separator
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].split('|') if c.strip() != ''])
                i += 1
            elements.append(make_table(headers, rows))
            continue

        # Table caption (Table N. ...)
        if re.match(r'^Table \d', stripped):
            elements.append(make_paragraph(stripped, 'Caption'))
            i += 1
            continue

        # Figure caption (Figure N. ...)
        if re.match(r'^Figure \d', stripped):
            elements.append(make_paragraph(stripped, 'Caption'))
            i += 1
            continue

        # Reference entries
        if in_references and re.match(r'^\[\d+\]', stripped):
            elements.append(make_paragraph(stripped, 'References'))
            i += 1
            continue

        # Keywords line (bold-led)
        elements.append(make_paragraph(stripped, 'Normal'))
        i += 1

    return '\n'.join(elements), images


# ─────────────────────────── package parts ───────────────────────────

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults><w:rPrDefault><w:rPr>
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
  <w:style w:type="paragraph" w:styleId="Caption">
    <w:name w:val="Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="200"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="References">
    <w:name w:val="References"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr><w:tblBorders>
      <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    </w:tblBorders></w:tblPr>
  </w:style>
</w:styles>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''


def build_content_types():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Default Extension="png" ContentType="image/png"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
            '</Types>')


def build_word_rels(images):
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rid, _full, arcname in images:
        target = arcname.replace('word/', '')
        rels.append(f'<Relationship Id="rId{rid}" '
                    f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                    f'Target="{target}"/>')
    rels.append('</Relationships>')
    return ''.join(rels)


def create_docx():
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        md_content = f.read()

    images = []
    body_xml, images = md_to_body(md_content, images)

    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<w:body>'
        f'{body_xml}'
        '<w:sectPr>'
        '<w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
        'w:header="720" w:footer="720" w:gutter="0"/>'
        '</w:sectPr>'
        '</w:body>'
        '</w:document>'
    )

    with zipfile.ZipFile(DOCX_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', build_content_types())
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', build_word_rels(images))
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES)
        for _rid, full_path, arcname in images:
            with open(full_path, 'rb') as img:
                zf.writestr(arcname, img.read())

    size_kb = os.path.getsize(DOCX_FILE) / 1024
    print(f"Created: {DOCX_FILE}")
    print(f"Embedded {len(images)} image(s).")
    print(f"File size: {size_kb:.1f} KB")


if __name__ == '__main__':
    create_docx()
