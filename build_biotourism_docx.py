#!/usr/bin/env python3
"""
Build a downloadable Word .docx for the chapter
"Bio-Integrated Urban Tourism: Green Infrastructure".

Uses raw OOXML (ZIP + XML) because python-docx is unavailable in this
sandbox. Embeds real PNG figures via word/media + relationships + DrawingML,
renders markdown tables, styled headings, and a hanging-indent reference list.
"""

import os
import re
import struct
import zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(BASE, "Chapter_Bio_Integrated_Urban_Tourism.md")
FIGDIR = os.path.join(BASE, "biotourism_figures")
OUT = os.path.join(BASE, "Chapter_Bio_Integrated_Urban_Tourism.docx")

EMU_PER_PX = 9525          # at 96 dpi
MAX_IMG_WIDTH_EMU = 5486400  # ~5.72 in printable width (6.5in - margins allowance)

# ─── boilerplate ───
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
  <w:docDefaults><w:rPrDefault><w:rPr>
    <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
    <w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1"><w:name w:val="Normal"/><w:pPr><w:jc w:val="both"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr><w:rPr><w:b/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/><w:keepNext/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/><w:keepNext/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Abstract"><w:name w:val="Abstract"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="600" w:right="600"/></w:pPr><w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="References"><w:name w:val="References"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="240"/></w:pPr><w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="ImageP"><w:name w:val="ImageP"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="180" w:after="20"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption"><w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="180" w:after="60"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
</w:styles>'''


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def make_run(text, bold=False, italic=False):
    props = ''
    if bold or italic:
        props = '<w:rPr>' + ('<w:b/>' if bold else '') + ('<w:i/>' if italic else '') + '</w:rPr>'
    return f'<w:r>{props}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'


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


def para(text, style='Normal'):
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{parse_inline(text)}</w:p>'


def image_para(rid, w_px, h_px, name):
    w_emu = w_px * EMU_PER_PX
    h_emu = h_px * EMU_PER_PX
    if w_emu > MAX_IMG_WIDTH_EMU:
        scale = MAX_IMG_WIDTH_EMU / w_emu
        w_emu = int(w_emu * scale)
        h_emu = int(h_emu * scale)
    return f'''<w:p><w:pPr><w:pStyle w:val="ImageP"/></w:pPr><w:r><w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0"
        xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
        <wp:extent cx="{w_emu}" cy="{h_emu}"/>
        <wp:docPr id="{rid[3:]}" name="{esc(name)}"/>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr><pic:cNvPr id="{rid[3:]}" name="{esc(name)}"/><pic:cNvPicPr/></pic:nvPicPr>
              <pic:blipFill>
                <a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="{rid}"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{w_emu}" cy="{h_emu}"/></a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline></w:drawing></w:r></w:p>'''


def make_table(headers, rows):
    n = len(headers)
    col_w = 9360 // n
    tbl = ['<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '</w:tblBorders></w:tblPr>']
    tbl.append('<w:tblGrid>' + f'<w:gridCol w:w="{col_w}"/>' * n + '</w:tblGrid>')
    tbl.append('<w:tr>')
    for h in headers:
        tbl.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="C8E0C8"/></w:tcPr>'
                   '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="20" w:line="276" w:lineRule="auto"/></w:pPr>%s</w:p></w:tc>'
                   % (col_w, make_run(h.strip(), bold=True)))
    tbl.append('</w:tr>')
    for row in rows:
        tbl.append('<w:tr>')
        for i in range(n):
            cell = row[i].strip() if i < len(row) else ''
            tbl.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/></w:tcPr>'
                       '<w:p><w:pPr><w:spacing w:after="20" w:line="276" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>%s</w:p></w:tc>'
                       % (col_w, make_run(cell)))
        tbl.append('</w:tr>')
    tbl.append('</w:tbl><w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>')
    return ''.join(tbl)


def build():
    md = open(MD, encoding="utf-8").read()
    lines = md.split('\n')

    images = []          # (rid, filename, w, h)
    body = []
    in_refs = False
    i = 0
    img_counter = 0

    while i < len(lines):
        line = lines[i].rstrip('\n')
        s = line.strip()
        if not s:
            i += 1
            continue

        # image tag
        m = re.match(r'\[\[IMG:(.+?)\]\]', s)
        if m:
            fn = m.group(1)
            img_counter += 1
            rid = f'rId{100 + img_counter}'
            w, h = png_size(os.path.join(FIGDIR, fn))
            images.append((rid, fn, w, h))
            body.append(image_para(rid, w, h, fn))
            i += 1
            continue

        if s.startswith('# ') and not s.startswith('## '):
            body.append(para(s[2:].strip(), 'Title'))
            i += 1
            continue
        if s.startswith('## '):
            txt = s[3:].strip()
            if txt.lower() == 'references':
                in_refs = True
            if txt.lower() == 'abstract':
                body.append(para(txt, 'Heading1'))
                i += 1
                # following paragraphs until next ## -> Abstract style
                while i < len(lines) and not lines[i].strip().startswith('## '):
                    p = lines[i].strip()
                    if p:
                        body.append(para(p, 'Abstract'))
                    i += 1
                continue
            body.append(para(txt, 'Heading1'))
            i += 1
            continue
        if s.startswith('### '):
            body.append(para(s[4:].strip(), 'Heading2'))
            i += 1
            continue

        # table
        if s.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:-]+\|', lines[i + 1].strip()):
            headers = [c.strip() for c in s.strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            body.append(make_table(headers, rows))
            continue

        # captions
        if re.match(r'^(Figure|Table)\s+\d+\.', s):
            style = 'TableCaption' if s.startswith('Table') else 'Caption'
            body.append(para(s, style))
            i += 1
            continue

        # reference entry
        if in_refs and re.match(r'^\[\d+\]', s):
            body.append(para(s, 'References'))
            i += 1
            continue

        body.append(para(s, 'Normal'))
        i += 1

    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{''.join(body)}
    <w:sectPr><w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    # relationships
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rid, fn, w, h in images:
        rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{fn}"/>')
    rels.append('</Relationships>')

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CONTENT_TYPES)
        z.writestr('_rels/.rels', RELS)
        z.writestr('word/_rels/document.xml.rels', '\n'.join(rels))
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', STYLES)
        for rid, fn, w, h in images:
            with open(os.path.join(FIGDIR, fn), 'rb') as f:
                z.writestr(f'word/media/{fn}', f.read())

    print("Created:", OUT)
    print("Size: %.1f KB" % (os.path.getsize(OUT) / 1024))
    print("Embedded images:", len(images))
    for rid, fn, w, h in images:
        print("  -", fn, f"({w}x{h})")


if __name__ == '__main__':
    build()
