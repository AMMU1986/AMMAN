#!/usr/bin/env python3
"""
Build a Word .docx for Chapter 20 (Future of AI-Driven Pharmacology and
Biomedical Engineering) from the markdown source, embedding the four PNG
figures. Uses raw OOXML (ZIP + XML) - no python-docx required.

Extends the approach in create_chapter_docx.py with image embedding:
 - PNG parts stored under word/media/
 - relationships added in word/_rels/document.xml.rels
 - inline <w:drawing> elements with EMU-scaled extents
"""

import zipfile
import os
import re
import struct

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
    <w:pPrDefault><w:pPr>
      <w:spacing w:after="120" w:line="360" w:lineRule="auto"/>
    </w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/><w:pPr><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
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
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="200" w:after="60"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="240"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="160" w:after="60"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
</w:styles>'''

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def escape_xml(text):
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    return text


def png_size(path):
    """Read width/height (px) from a PNG IHDR chunk."""
    with open(path, 'rb') as f:
        head = f.read(24)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('not a PNG: ' + path)
    w, h = struct.unpack('>II', head[16:24])
    return w, h


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


def make_image_paragraph(rid, img_w_px, img_h_px, docpr_id, name):
    """Inline image paragraph, scaled to a max content width."""
    EMU_PER_PX = 9525            # at 96 dpi
    MAX_W_EMU = 5486400          # ~5.7 in usable width (6.5in page - safety)
    cx = img_w_px * EMU_PER_PX
    cy = img_h_px * EMU_PER_PX
    if cx > MAX_W_EMU:
        scale = MAX_W_EMU / cx
        cx = int(cx * scale)
        cy = int(cy * scale)
    drawing = f'''<w:drawing>
  <wp:inline distT="0" distB="0" distL="0" distR="0"
      xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
    <wp:extent cx="{cx}" cy="{cy}"/>
    <wp:effectExtent l="0" t="0" r="0" b="0"/>
    <wp:docPr id="{docpr_id}" name="{escape_xml(name)}"/>
    <wp:cNvGraphicFramePr>
      <a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>
    </wp:cNvGraphicFramePr>
    <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
      <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
        <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
          <pic:nvPicPr>
            <pic:cNvPr id="{docpr_id}" name="{escape_xml(name)}"/>
            <pic:cNvPicPr/>
          </pic:nvPicPr>
          <pic:blipFill>
            <a:blip r:embed="{rid}"/>
            <a:stretch><a:fillRect/></a:stretch>
          </pic:blipFill>
          <pic:spPr>
            <a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
            <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          </pic:spPr>
        </pic:pic>
      </a:graphicData>
    </a:graphic>
  </wp:inline>
</w:drawing>'''
    return (f'<w:p><w:pPr><w:pStyle w:val="FigureImage"/></w:pPr>'
            f'<w:r>{drawing}</w:r></w:p>')


def make_table(headers, rows):
    n = len(headers)
    col_w = 9200 // n
    tbl = ['<w:tbl>']
    tbl.append('<w:tblPr>')
    tbl.append('<w:tblW w:w="9200" w:type="dxa"/><w:tblLayout w:type="fixed"/>')
    tbl.append('<w:tblBorders>')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        tbl.append(f'<w:{edge} w:val="single" w:sz="4" w:space="0" w:color="000000"/>')
    tbl.append('</w:tblBorders></w:tblPr>')
    tbl.append('<w:tblGrid>' + (f'<w:gridCol w:w="{col_w}"/>' * n) + '</w:tblGrid>')
    # header
    tbl.append('<w:tr>')
    for h in headers:
        tbl.append('<w:tc><w:tcPr>'
                   f'<w:tcW w:w="{col_w}" w:type="dxa"/>'
                   '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>'
                   '</w:tcPr>'
                   f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="40" w:line="240" w:lineRule="auto"/></w:pPr>'
                   f'{make_run(h.strip(), bold=True)}</w:p></w:tc>')
    tbl.append('</w:tr>')
    for row in rows:
        tbl.append('<w:tr>')
        for i in range(n):
            cell = row[i] if i < len(row) else ''
            tbl.append('<w:tc>'
                       f'<w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/></w:tcPr>'
                       f'<w:p><w:pPr><w:spacing w:after="40" w:line="240" w:lineRule="auto"/></w:pPr>'
                       f'{make_run(cell.strip())}</w:p></w:tc>')
        tbl.append('</w:tr>')
    tbl.append('</w:tbl>')
    # trailing empty paragraph so tables aren't glued to next block
    tbl.append('<w:p/>')
    return ''.join(tbl)


def md_to_body(md_text, images, base_dir):
    """images: list to append (rid, arcname, abspath); returns body xml."""
    elements = []
    lines = md_text.split('\n')
    i = 0
    in_refs = False
    img_counter = 0

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.strip() == '---':
            i += 1
            continue

        # Embedded image marker
        m = re.match(r'\[\[IMAGE:(.+?)\|(.+?)\]\]', line.strip())
        if m:
            rel_path, caption = m.group(1), m.group(2)
            img_counter += 1
            rid = f'rIdImg{img_counter}'
            arc = f'media/{os.path.basename(rel_path)}'
            abspath = os.path.join(base_dir, rel_path)
            images.append((rid, arc, abspath))
            w, h = png_size(abspath)
            elements.append(make_image_paragraph(rid, w, h, 1000 + img_counter,
                                                  os.path.basename(rel_path)))
            elements.append(make_paragraph(caption, 'FigureCaption'))
            i += 1
            continue

        if line.startswith('# ') and not line.startswith('## '):
            elements.append(make_paragraph(line[2:].strip(), 'Title'))
            i += 1
            continue
        if line.startswith('## '):
            h = line[3:].strip()
            if h == 'References':
                in_refs = True
            elements.append(make_paragraph(h, 'Heading1'))
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
        if '|' in line and i + 1 < len(lines) and re.search(r'\|\s*---', lines[i+1]):
            headers = [c.strip() for c in line.split('|') if c.strip()]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].split('|') if c.strip() != ''])
                i += 1
            elements.append(make_table(headers, rows))
            continue

        # Table caption
        if line.strip().startswith('Table 20.') and '|' not in line:
            elements.append(make_paragraph(line.strip(), 'TableCaption'))
            i += 1
            continue

        # Abstract body paragraphs (between '## Abstract' heading and next '## ')
        # handled as Normal; abstract styling optional

        if in_refs and re.match(r'^\[\d+\]', line.strip()):
            elements.append(make_paragraph(line.strip(), 'References'))
            i += 1
            continue

        elements.append(make_paragraph(line.strip(), 'Normal'))
        i += 1

    return '\n'.join(elements)


def build_word_rels(images):
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>']
    for rid, arc, _ in images:
        rels.append(f'<Relationship Id="{rid}" '
                    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                    f'Target="{arc}"/>')
    rels.append('</Relationships>')
    return '\n'.join(rels)


def create_docx(md_filepath, output_filepath):
    base_dir = os.path.dirname(os.path.abspath(md_filepath))
    with open(md_filepath, 'r', encoding='utf-8') as f:
        md = f.read()

    images = []
    body_xml = md_to_body(md, images, base_dir)

    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{W_NS}"
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

    word_rels = build_word_rels(images)

    with zipfile.ZipFile(output_filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES)
        zf.writestr('word/numbering.xml', NUMBERING)
        for rid, arc, abspath in images:
            with open(abspath, 'rb') as imf:
                zf.writestr('word/' + arc, imf.read())

    kb = os.path.getsize(output_filepath) / 1024
    print(f"Created: {output_filepath} ({kb:.1f} KB), images embedded: {len(images)}")


if __name__ == '__main__':
    d = os.path.dirname(os.path.abspath(__file__))
    md = os.path.join(d, 'Chapter_20_Future_AI_Pharmacology.md')
    out = os.path.join(d, 'Chapter_20_Future_AI_Pharmacology.docx')
    create_docx(md, out)
