#!/usr/bin/env python3
"""
Build the Word .docx for the chapter
"Agricultural Data Management: Big Data Analytics, Cloud Computing, and Edge Intelligence".

Extends the raw-OOXML approach used elsewhere in this repo (no python-docx needed)
to also embed PNG figures. Figures are referenced in the markdown with markers of
the form [[IMAGE:filename.png]] followed by a caption line beginning "Figure N.".
"""

import zipfile
import os
import re
import struct

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(SCRIPT_DIR, 'Chapter_Agricultural_Data_Management.md')
FIG_DIR = os.path.join(SCRIPT_DIR, 'agri_figures')
OUT_FILE = os.path.join(SCRIPT_DIR, 'Agricultural_Data_Management_Chapter.docx')

EMU_PER_PX = 9525          # 1 pixel (at 96 dpi) in English Metric Units
MAX_WIDTH_EMU = 5486400    # ~6 inches usable page width

# ─── OOXML templates ───

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
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="200" w:after="60"/></w:pPr>
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


def make_table(headers, rows):
    n_cols = len(headers)
    col_w = 9000 // n_cols
    tbl = ('<w:tbl><w:tblPr><w:tblW w:w="9000" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '</w:tblBorders></w:tblPr>')
    tbl += '<w:tblGrid>' + (f'<w:gridCol w:w="{col_w}"/>' * n_cols) + '</w:tblGrid>'
    # header
    tbl += '<w:tr>'
    for h in headers:
        tbl += ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>'
                '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>'
                '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="40"/></w:pPr>%s</w:p></w:tc>'
                % (col_w, make_run(h.strip(), bold=True)))
    tbl += '</w:tr>'
    # data
    for row in rows:
        tbl += '<w:tr>'
        for i in range(n_cols):
            cell = row[i].strip() if i < len(row) else ''
            tbl += ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/></w:tcPr>'
                    '<w:p><w:pPr><w:spacing w:after="40"/><w:jc w:val="left"/></w:pPr>%s</w:p></w:tc>'
                    % (col_w, make_run(cell)))
        tbl += '</w:tr>'
    tbl += '</w:tbl>'
    # empty paragraph after table for spacing
    tbl += '<w:p/>'
    return tbl


def png_size(path):
    """Read PNG width/height from the IHDR chunk."""
    with open(path, 'rb') as f:
        f.read(8)                 # signature
        f.read(4)                 # length
        f.read(4)                 # 'IHDR'
        w, h = struct.unpack('>II', f.read(8))
    return w, h


def make_image_paragraph(rid, width_px, height_px, name, docpr_id):
    """Build a centered inline image paragraph."""
    cx = width_px * EMU_PER_PX
    cy = height_px * EMU_PER_PX
    if cx > MAX_WIDTH_EMU:
        scale = MAX_WIDTH_EMU / cx
        cx = int(cx * scale)
        cy = int(cy * scale)
    drawing = f'''<w:r><w:drawing>
  <wp:inline distT="0" distB="0" distL="0" distR="0"
    xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
    <wp:extent cx="{cx}" cy="{cy}"/>
    <wp:docPr id="{docpr_id}" name="{name}"/>
    <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
      <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
        <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
          <pic:nvPicPr>
            <pic:cNvPr id="{docpr_id}" name="{name}"/>
            <pic:cNvPicPr/>
          </pic:nvPicPr>
          <pic:blipFill>
            <a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="{rid}"/>
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
</w:drawing></w:r>'''
    return f'<w:p><w:pPr><w:pStyle w:val="FigureImage"/></w:pPr>{drawing}</w:p>'


def build():
    with open(MD_FILE, encoding='utf-8') as f:
        lines = f.read().split('\n')

    elements = []
    images = []            # list of (filename, rid)
    img_counter = 0
    in_refs = False
    in_abstract = False
    i = 0

    while i < len(lines):
        line = lines[i]
        s = line.strip()

        if not s:
            i += 1
            continue
        if s == '---':
            i += 1
            continue

        # Image marker
        m = re.match(r'\[\[IMAGE:(.+?)\]\]', s)
        if m:
            fname = m.group(1)
            img_counter += 1
            rid = f'rIdImg{img_counter}'
            images.append((fname, rid))
            w, h = png_size(os.path.join(FIG_DIR, fname))
            elements.append(make_image_paragraph(rid, w, h, fname, 100 + img_counter))
            i += 1
            continue

        # Title
        if line.startswith('# ') and not line.startswith('## '):
            elements.append(make_paragraph(line[2:].strip(), 'Title'))
            i += 1
            continue
        # Heading 1
        if line.startswith('## '):
            txt = line[3:].strip()
            if txt == 'References':
                in_refs = True
            in_abstract = (txt == 'Abstract')
            elements.append(make_paragraph(txt, 'Heading1'))
            i += 1
            continue
        # Heading 2 / 3
        if line.startswith('### '):
            in_abstract = False
            elements.append(make_paragraph(line[4:].strip(), 'Heading2'))
            i += 1
            continue
        if line.startswith('#### '):
            elements.append(make_paragraph(line[5:].strip(), 'Heading3'))
            i += 1
            continue

        # Table
        if '|' in line and i + 1 < len(lines) and re.search(r'\|?\s*-{2,}', lines[i + 1]) and '|' in lines[i + 1]:
            headers = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            elements.append(make_table(headers, rows))
            continue

        # Table caption
        if s.startswith('Table ') and s[6:7].isdigit() and '|' not in s:
            elements.append(make_paragraph(s, 'TableCaption'))
            i += 1
            continue
        # Figure caption
        if s.startswith('Figure ') and s[7:8].isdigit():
            elements.append(make_paragraph(s, 'FigureCaption'))
            i += 1
            continue
        # Reference entries
        if in_refs and re.match(r'^\[\d+\]', s):
            elements.append(make_paragraph(s, 'References'))
            i += 1
            continue
        # Abstract body
        if in_abstract:
            elements.append(make_paragraph(s, 'Abstract'))
            i += 1
            continue
        # Note
        if s.startswith('**Note:**'):
            elements.append(make_paragraph(s, 'Normal'))
            i += 1
            continue
        # Normal
        elements.append(make_paragraph(s, 'Normal'))
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

    # word/_rels/document.xml.rels including image relationships
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>']
    for idx, (fname, rid) in enumerate(images, start=1):
        rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image{idx}.png"/>')
    rels.append('</Relationships>')
    word_rels = '\n'.join(rels)

    with zipfile.ZipFile(OUT_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES)
        zf.writestr('word/numbering.xml', NUMBERING)
        for idx, (fname, rid) in enumerate(images, start=1):
            with open(os.path.join(FIG_DIR, fname), 'rb') as imgf:
                zf.writestr(f'word/media/image{idx}.png', imgf.read())

    size_kb = os.path.getsize(OUT_FILE) / 1024
    print(f"Created: {OUT_FILE}")
    print(f"Size: {size_kb:.1f} KB")
    print(f"Embedded images: {len(images)}")
    for fname, rid in images:
        print(f"  - {fname}")


if __name__ == '__main__':
    build()
