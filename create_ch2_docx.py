#!/usr/bin/env python3
"""
Create a Word .docx for Chapter 2 (AI & ML in Healthcare) with EMBEDDED PNG figures.
Pure standard library: builds raw OOXML (ZIP + XML), including image parts,
relationships, and inline DrawingML so figures render inside the document.
"""

import zipfile
import os
import re
import struct

MD_FILE = '/projects/sandbox/AMMAN/Chapter_2_AI_ML_Healthcare.md'
FIG_DIR = '/projects/sandbox/AMMAN/ch2_figures'
OUT_FILE = '/projects/sandbox/AMMAN/Chapter_2_AI_ML_Healthcare.docx'
EMU_PER_PX = 9525          # English Metric Units per pixel at 96 DPI
MAX_WIDTH_EMU = 5486400    # ~6.0 inches usable width

# ─── OOXML boilerplate ───

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
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Caption">
    <w:name w:val="Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="240"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ImagePara">
    <w:name w:val="ImagePara"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="0"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCap">
    <w:name w:val="TableCap"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="180" w:after="60"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
</w:styles>'''


def escape_xml(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def png_size(path):
    """Read width/height from a PNG IHDR chunk."""
    with open(path, 'rb') as f:
        f.read(8)          # signature
        f.read(4)          # length
        f.read(4)          # 'IHDR'
        w, h = struct.unpack('>II', f.read(8))
    return w, h


def make_run(text, bold=False, italic=False):
    props = ''
    if bold or italic:
        props = '<w:rPr>' + ('<w:b/>' if bold else '') + ('<w:i/>' if italic else '') + '</w:rPr>'
    return f'<w:r>{props}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'


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
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{parse_inline(text)}</w:p>'


def make_image_paragraph(rid, w_px, h_px, name):
    """Inline DrawingML image, scaled to fit page width."""
    w_emu = w_px * EMU_PER_PX
    h_emu = h_px * EMU_PER_PX
    if w_emu > MAX_WIDTH_EMU:
        scale = MAX_WIDTH_EMU / w_emu
        w_emu = int(w_emu * scale)
        h_emu = int(h_emu * scale)
    return f'''<w:p><w:pPr><w:pStyle w:val="ImagePara"/></w:pPr><w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
<wp:extent cx="{w_emu}" cy="{h_emu}"/>
<wp:docPr id="{rid}" name="{name}"/>
<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:nvPicPr><pic:cNvPr id="{rid}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="rId{rid}"/>
<a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{w_emu}" cy="{h_emu}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''


def make_table(headers, rows):
    n = len(headers)
    col_w = 9200 // n
    tbl = ('<w:tbl><w:tblPr><w:tblW w:w="9200" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '</w:tblBorders></w:tblPr>')
    tbl += '<w:tblGrid>' + f'<w:gridCol w:w="{col_w}"/>' * n + '</w:tblGrid>'
    # header
    tbl += '<w:tr><w:trPr><w:tblHeader/></w:trPr>'
    for h in headers:
        tbl += ('<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>'
                '<w:vAlign w:val="center"/></w:tcPr>'
                f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="40" w:line="276" w:lineRule="auto"/></w:pPr>{make_run(h.strip(), bold=True)}</w:p></w:tc>')
    tbl += '</w:tr>'
    for row in rows:
        tbl += '<w:tr>'
        for i in range(n):
            cell = row[i].strip() if i < len(row) else ''
            tbl += ('<w:tc><w:tcPr><w:vAlign w:val="center"/></w:tcPr>'
                    f'<w:p><w:pPr><w:spacing w:after="40" w:line="276" w:lineRule="auto"/></w:pPr>{parse_inline(cell)}</w:p></w:tc>')
        tbl += '</w:tr>'
    tbl += '</w:tbl><w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>'
    return tbl


def build():
    with open(MD_FILE, encoding='utf-8') as f:
        lines = f.read().split('\n')

    images = []          # (rid, filename)
    body = []
    in_refs = False
    rid_counter = 100    # image rIds start high to avoid clashes
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s or s == '---':
            i += 1
            continue

        # Title
        if s.startswith('# ') and not s.startswith('## '):
            body.append(make_paragraph(s[2:].strip(), 'Title'))
            i += 1; continue
        # Headings
        if s.startswith('#### '):
            body.append(make_paragraph(s[5:].strip(), 'Heading3')); i += 1; continue
        if s.startswith('### '):
            body.append(make_paragraph(s[4:].strip(), 'Heading2')); i += 1; continue
        if s.startswith('## '):
            h = s[3:].strip()
            if h.lower() == 'references':
                in_refs = True
            body.append(make_paragraph(h, 'Heading1')); i += 1; continue

        # Abstract heading is '## Abstract' handled above; abstract body italic
        # Detect the paragraph right after Abstract heading -> style Abstract
        # (handled generically as Normal; keep simple)

        # Table
        if '|' in line and i + 1 < len(lines) and re.search(r'\|?\s*-{3,}', lines[i + 1]):
            headers = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            body.append(make_table(headers, rows))
            continue

        # Figure caption line: "Figure N. ..." -> embed image THEN caption
        m = re.match(r'^Figure (\d+)\.', s)
        if m:
            n = m.group(1)
            fig_path = os.path.join(FIG_DIR, f'Figure_{n}.png')
            if os.path.exists(fig_path):
                w, h = png_size(fig_path)
                rid = rid_counter
                rid_counter += 1
                images.append((rid, f'Figure_{n}.png'))
                body.append(make_image_paragraph(rid, w, h, f'Figure {n}'))
            body.append(make_paragraph(s, 'Caption'))
            i += 1; continue

        # Table caption line: "Table N. ..."
        if re.match(r'^Table (\d+)\.', s):
            body.append(make_paragraph(s, 'TableCap'))
            i += 1; continue

        # Reference entry
        if in_refs and re.match(r'^\[\d+\]', s):
            body.append(make_paragraph(s, 'References'))
            i += 1; continue

        # Abstract paragraph: the block right after the Abstract heading
        # We style it as Abstract if the previous emitted heading was Abstract.
        style = 'Normal'
        # look back for most recent heading text
        for prev in reversed(body):
            if 'w:pStyle w:val="Heading1"' in prev or 'w:pStyle w:val="Title"' in prev:
                if '>Abstract<' in prev:
                    style = 'Abstract'
                break
            if 'w:pStyle w:val="Normal"' in prev or 'w:pStyle w:val="Abstract"' in prev:
                # already in a text region
                if 'w:pStyle w:val="Abstract"' in prev:
                    style = 'Abstract'
                break
        body.append(make_paragraph(s, style))
        i += 1

    # Build relationships (styles + images)
    rels = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rid, fname in images:
        rels.append(f'<Relationship Id="rId{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{fname}"/>')
    word_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 + ''.join(rels) + '</Relationships>')

    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{''.join(body)}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    with zipfile.ZipFile(OUT_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', STYLES)
        for rid, fname in images:
            with open(os.path.join(FIG_DIR, fname), 'rb') as imf:
                zf.writestr(f'word/media/{fname}', imf.read())

    print(f"Created {OUT_FILE} ({os.path.getsize(OUT_FILE)/1024:.1f} KB)")
    print(f"Embedded {len(images)} images:", [f for _, f in images])


if __name__ == '__main__':
    build()
