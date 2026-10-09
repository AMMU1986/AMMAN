#!/usr/bin/env python3
"""
Build a Word .docx for the chapter
"Techno-Economic and Sustainability Assessment of Hybrid Renewable Energy Systems".

Pure standard library (zipfile + raw OOXML). Extends the project's docx approach
with embedded PNG figures and plain-text rendering of block equations, since
matplotlib / python-docx / Pillow are not available in this sandbox.
"""

import zipfile
import os
import re
import struct

BASE = '/projects/sandbox/AMMAN'
MD_FILE = os.path.join(BASE, 'Chapter_TechnoEconomic_Sustainability_HRES.md')
DOCX_FILE = os.path.join(BASE, 'Chapter_TechnoEconomic_Sustainability_HRES.docx')

EMU_PER_PX = 9525          # 1 px (96 dpi) in EMU
MAX_WIDTH_EMU = 5486400    # ~5.72 in usable page width

# ─── OOXML boilerplate ───

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
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
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
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="240"/></w:pPr>
    <w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ImagePara">
    <w:name w:val="Image Para"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="160" w:after="60"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Equation">
    <w:name w:val="Equation"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="120"/></w:pPr>
    <w:rPr><w:i/></w:rPr>
  </w:style>
</w:styles>'''


def escape_xml(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


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


def make_table(headers, rows):
    n = len(headers)
    col_w = 9020 // n
    tbl = ('<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
           '<w:tblW w:w="9020" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '</w:tblBorders></w:tblPr>')
    tbl += '<w:tblGrid>' + (f'<w:gridCol w:w="{col_w}"/>' * n) + '</w:tblGrid>'
    # header row
    tbl += '<w:tr><w:trPr><w:tblHeader/></w:trPr>'
    for h in headers:
        tbl += ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>'
                '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>'
                '<w:vAlign w:val="center"/></w:tcPr>'
                '<w:p><w:pPr><w:spacing w:after="40" w:line="276" w:lineRule="auto"/>'
                '<w:jc w:val="center"/></w:pPr>%s</w:p></w:tc>'
                % (col_w, make_run(h.strip(), bold=True)))
    tbl += '</w:tr>'
    for row in rows:
        tbl += '<w:tr>'
        for i in range(n):
            cell = row[i].strip() if i < len(row) else ''
            tbl += ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
                    '<w:p><w:pPr><w:spacing w:after="40" w:line="276" w:lineRule="auto"/></w:pPr>'
                    '%s</w:p></w:tc>' % (col_w, make_run(cell)))
        tbl += '</w:tr>'
    tbl += '</w:tbl><w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>'
    return tbl


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('not a PNG: ' + path)
    w, h = struct.unpack('>II', head[16:24])
    return w, h


def make_image_paragraph(rid, w_px, h_px):
    w_emu = w_px * EMU_PER_PX
    h_emu = h_px * EMU_PER_PX
    if w_emu > MAX_WIDTH_EMU:
        scale = MAX_WIDTH_EMU / w_emu
        w_emu = int(w_emu * scale)
        h_emu = int(h_emu * scale)
    drawing = f'''<w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
  <wp:extent cx="{w_emu}" cy="{h_emu}"/>
  <wp:docPr id="{rid}" name="Figure{rid}"/>
  <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
    <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
      <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
        <pic:nvPicPr><pic:cNvPr id="{rid}" name="Figure{rid}"/><pic:cNvPicPr/></pic:nvPicPr>
        <pic:blipFill><a:blip r:embed="rId{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
        <pic:spPr>
          <a:xfrm><a:off x="0" y="0"/><a:ext cx="{w_emu}" cy="{h_emu}"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        </pic:spPr>
      </pic:pic>
    </a:graphicData>
  </a:graphic>
</wp:inline></w:drawing></w:r>'''
    return f'<w:p><w:pPr><w:pStyle w:val="ImagePara"/></w:pPr>{drawing}</w:p>'


def latex_to_text(eq):
    """Readable plain-text rendering of the two block equations used in the chapter."""
    if 'NPC' in eq:
        return ('NPC = \u03a3 (t = 0 \u2192 N) [ (C_cap,t + C_rep,t + C_O&M,t '
                '+ C_fuel,t \u2212 S_t) / (1 + r)^t ]')
    if 'LCOE' in eq:
        return ('LCOE = [ \u03a3 (t = 0 \u2192 N) (C_cap,t + C_O&M,t + C_rep,t + C_fuel,t) / (1 + r)^t ] '
                '\u00f7 [ \u03a3 (t = 1 \u2192 N) E_t / (1 + r)^t ]')
    # generic fallback: strip latex markup
    s = eq.strip().strip('$')
    s = s.replace('\\sum', '\u03a3').replace('\\dfrac', '').replace('\\frac', '')
    s = re.sub(r'[\\{}]', '', s)
    return s


def is_caption(line, kind):
    # Real captions carry a period inside the bold span, e.g. "**Figure 1.**";
    # in-text references are "**Figure 1**" (no period) and must NOT match.
    return bool(re.match(r'^\*\*' + kind + r'\s*\d+\.\*\*', line.strip()))


def build_body(md, images):
    """Convert markdown to OOXML body; `images` collects (rid, abspath)."""
    out = []
    lines = md.split('\n')
    i = 0
    in_refs = False
    rid_counter = [1]  # rId1 reserved for styles; start images at rId2 later

    def next_image_rid():
        rid_counter[0] += 1
        return rid_counter[0] + 1  # keep clear of styles(rId1)/numbering(rId2)

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s or s == '---':
            i += 1
            continue

        # Block equation ($$ ... $$ on one line)
        if s.startswith('$$') and s.endswith('$$') and len(s) > 4:
            out.append(make_paragraph(latex_to_text(s), 'Equation'))
            i += 1
            continue

        # Image: ![alt](path)
        m = re.match(r'^!\[.*?\]\((.+?)\)$', s)
        if m:
            rel = m.group(1)
            abspath = os.path.join(BASE, rel)
            if os.path.exists(abspath):
                w_px, h_px = png_size(abspath)
                rid = next_image_rid()
                images.append((rid, abspath))
                out.append(make_image_paragraph(rid, w_px, h_px))
            i += 1
            continue

        # Headings
        if s.startswith('# ') and not s.startswith('## '):
            out.append(make_paragraph(s[2:].strip(), 'Title'))
            i += 1
            continue
        if s.startswith('## '):
            txt = s[3:].strip()
            if txt == 'References':
                in_refs = True
            out.append(make_paragraph(txt, 'Heading1'))
            i += 1
            continue
        if s.startswith('### '):
            out.append(make_paragraph(s[4:].strip(), 'Heading2'))
            i += 1
            continue

        # Table
        if '|' in line and i + 1 < len(lines) and re.search(r'\|?\s*-{3,}', lines[i + 1]):
            headers = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            out.append(make_table(headers, rows))
            continue

        # Captions
        if is_caption(s, 'Figure'):
            out.append(make_paragraph(s, 'FigureCaption'))
            i += 1
            continue
        if is_caption(s, 'Table'):
            out.append(make_paragraph(s, 'TableCaption'))
            i += 1
            continue

        # Abstract / keywords block
        if s.startswith('**Keywords:**'):
            out.append(make_paragraph(s, 'Abstract'))
            i += 1
            continue

        # Reference entries
        if in_refs and re.match(r'^\[\d+\]', s):
            out.append(make_paragraph(s, 'References'))
            i += 1
            continue

        out.append(make_paragraph(s, 'Normal'))
        i += 1

    return '\n'.join(out)


def build():
    with open(MD_FILE, encoding='utf-8') as f:
        md = f.read()

    images = []
    body = build_body(md, images)

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

    # Relationships: styles + numbering + one per image
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>']
    for idx, (rid, _) in enumerate(images, start=1):
        rels.append(f'<Relationship Id="rId{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image{idx}.png"/>')
    rels.append('</Relationships>')
    word_rels = '\n'.join(rels)

    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''

    with zipfile.ZipFile(DOCX_FILE, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('_rels/.rels', RELS)
        z.writestr('word/_rels/document.xml.rels', word_rels)
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', STYLES)
        z.writestr('word/numbering.xml', NUMBERING)
        for idx, (_, abspath) in enumerate(images, start=1):
            with open(abspath, 'rb') as img:
                z.writestr(f'word/media/image{idx}.png', img.read())

    print(f"Created {DOCX_FILE}")
    print(f"  size: {os.path.getsize(DOCX_FILE)/1024:.1f} KB")
    print(f"  embedded figures: {len(images)}")


if __name__ == '__main__':
    build()
