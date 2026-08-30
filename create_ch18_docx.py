#!/usr/bin/env python3
"""
Create a Word .docx for Chapter 18 (AI Applications in Disease-Specific
Pharmacology) from the markdown source, with embedded PNG figures.

Uses raw OOXML (ZIP + XML) since python-docx is not available in this sandbox.
Extends the base builder (create_chapter_docx.py) with image embedding:
  - '![Figure_N]' anchor lines become inline w:drawing elements
  - PNGs are added as word/media/imageN.png with relationships and content type
"""

import zipfile
import os
import re
import struct

FIG_DIR = '/projects/sandbox/AMMAN/ch18_figures'

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
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
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
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureImage">
    <w:name w:val="Figure Image"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="240"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="Table Caption"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="120" w:after="60"/></w:pPr>
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


def png_size(path):
    """Read PNG width/height (px) from the IHDR chunk."""
    with open(path, 'rb') as f:
        head = f.read(24)
    w, h = struct.unpack('>II', head[16:24])
    return w, h


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
    rpr = '<w:rPr>' + ''.join(props) + '</w:rPr>' if props else ''
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
    return f'<w:p>{ppr}{parse_inline(text)}</w:p>'


def make_image_paragraph(rid, emu_w, emu_h, docpr_id, name):
    """Inline image (w:drawing) centered in its own paragraph."""
    drawing = (
        '<w:r><w:drawing>'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        f'<wp:extent cx="{emu_w}" cy="{emu_h}"/>'
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
        f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{emu_w}" cy="{emu_h}"/></a:xfrm>'
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
    tbl = '<w:tbl>'
    tbl += '<w:tblPr><w:tblStyle w:val="TableGrid"/>'
    tbl += '<w:tblW w:w="9360" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
    tbl += '<w:tblBorders>'
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        tbl += f'<w:{edge} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '</w:tblBorders></w:tblPr>'
    col_w = 9360 // n_cols
    tbl += '<w:tblGrid>' + (f'<w:gridCol w:w="{col_w}"/>' * n_cols) + '</w:tblGrid>'
    # header
    tbl += '<w:tr><w:trPr><w:tblHeader/></w:trPr>'
    for h in headers:
        tbl += '<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/><w:vAlign w:val="center"/></w:tcPr>'
        tbl += f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="20"/></w:pPr>{make_run(h.strip(), bold=True)}</w:p></w:tc>'
    tbl += '</w:tr>'
    for row in rows:
        tbl += '<w:tr>'
        for cell in row:
            tbl += '<w:tc><w:tcPr><w:vAlign w:val="center"/></w:tcPr>'
            tbl += f'<w:p><w:pPr><w:jc w:val="left"/><w:spacing w:after="20"/></w:pPr>{make_run(cell.strip())}</w:p></w:tc>'
        for _ in range(n_cols - len(row)):
            tbl += '<w:tc><w:p/></w:tc>'
        tbl += '</w:tr>'
    tbl += '</w:tbl>'
    # spacer paragraph after table
    tbl += '<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>'
    return tbl


def md_to_body(md_text, images):
    """Convert markdown to OOXML body. `images` collects (rid, filename)."""
    elements = []
    lines = md_text.split('\n')
    i = 0
    in_references = False
    docpr = 1

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        stripped = line.strip()

        if stripped == '---':
            i += 1
            continue

        # Image anchor: ![Figure_N]
        m_img = re.match(r'^!\[(Figure_\d+)\]$', stripped)
        if m_img:
            fig_name = m_img.group(1)
            fig_path = os.path.join(FIG_DIR, fig_name + '.png')
            rid = f'rIdImg{docpr}'
            images.append((rid, fig_name + '.png', fig_path))
            px_w, px_h = png_size(fig_path)
            # display width ~6.2 inches; EMU = inches * 914400
            disp_w_in = 6.2
            emu_w = int(disp_w_in * 914400)
            emu_h = int(emu_w * px_h / px_w)
            elements.append(make_image_paragraph(rid, emu_w, emu_h, docpr, fig_name))
            docpr += 1
            i += 1
            continue

        if line.startswith('# ') and not line.startswith('## '):
            elements.append(make_paragraph(stripped[2:].strip(), 'Title'))
            i += 1
            continue

        if line.startswith('## '):
            htext = stripped[3:].strip()
            if htext == 'References':
                in_references = True
            elements.append(make_paragraph(htext, 'Heading1'))
            i += 1
            continue

        if line.startswith('### '):
            elements.append(make_paragraph(stripped[4:].strip(), 'Heading2'))
            i += 1
            continue

        if line.startswith('#### '):
            elements.append(make_paragraph(stripped[5:].strip(), 'Heading3'))
            i += 1
            continue

        # Table
        if '|' in line and i + 1 < len(lines) and re.search(r'\|?\s*-{2,}', lines[i + 1]):
            headers = [c.strip() for c in line.split('|') if c.strip()]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                row = [c.strip() for c in lines[i].split('|') if c.strip()]
                rows.append(row)
                i += 1
            elements.append(make_table(headers, rows))
            continue

        # Figure caption line: "Figure N. ..."
        if re.match(r'^Figure \d+\.', stripped):
            elements.append(make_paragraph(stripped, 'FigureCaption'))
            i += 1
            continue

        # Table caption line: "Table N. ..." (not a table row)
        if re.match(r'^Table \d+\.', stripped) and '|' not in stripped:
            elements.append(make_paragraph(stripped, 'TableCaption'))
            i += 1
            continue

        # Abstract body paragraph (italic block) — style the abstract text
        # Reference entries
        if in_references and re.match(r'^\[\d+\]', stripped):
            elements.append(make_paragraph(stripped, 'References'))
            i += 1
            continue

        elements.append(make_paragraph(stripped, 'Normal'))
        i += 1

    return '\n'.join(elements)


def create_docx(md_filepath, output_filepath):
    with open(md_filepath, 'r', encoding='utf-8') as f:
        md_content = f.read()

    images = []
    body_xml = md_to_body(md_content, images)

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

    # Build document relationships (styles, numbering, images)
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>']
    for rid, fname, _ in images:
        rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{fname}"/>')
    rels.append('</Relationships>')
    word_rels = '\n'.join(rels)

    with zipfile.ZipFile(output_filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES)
        zf.writestr('word/numbering.xml', NUMBERING)
        for _, fname, fpath in images:
            with open(fpath, 'rb') as imgf:
                zf.writestr(f'word/media/{fname}', imgf.read())

    size_kb = os.path.getsize(output_filepath) / 1024
    print(f"Successfully created: {output_filepath}")
    print(f"File size: {size_kb:.1f} KB")
    print(f"Embedded images: {len(images)}")


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md_file = os.path.join(script_dir, 'Chapter_18_AI_Disease_Pharmacology.md')
    docx_file = os.path.join(script_dir, 'Chapter_18_AI_Disease_Pharmacology.docx')
    create_docx(md_file, docx_file)
