#!/usr/bin/env python3
"""
Build Chapter_6_AI_Dielectric_Ferroelectric_Ceramics.docx from the markdown
source, embedding the four PNG figures. Pure standard library (no python-docx).
"""

import zipfile
import os
import re
import struct

SRC = '/projects/sandbox/AMMAN/Chapter_6_AI_Dielectric_Ferroelectric_Ceramics.md'
OUT = '/projects/sandbox/AMMAN/Chapter_6_AI_Dielectric_Ferroelectric_Ceramics.docx'
BASE = '/projects/sandbox/AMMAN'

EMU_PER_INCH = 914400
MAX_WIDTH_IN = 6.0  # display width for figures

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

NUMBERING = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults><w:rPrDefault><w:rPr>
    <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
    <w:sz w:val="24"/><w:szCs w:val="24"/>
  </w:rPr></w:rPrDefault>
  <w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1"><w:name w:val="Normal"/><w:pPr><w:jc w:val="both"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Abstract"><w:name w:val="Abstract"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="720" w:right="720"/></w:pPr><w:rPr><w:i/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="References"><w:name w:val="References"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/></w:pPr><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption"><w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="60" w:after="240"/></w:pPr><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="ImagePara"><w:name w:val="Image"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption"><w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="60"/></w:pPr><w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders>
    <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
  </w:tblBorders></w:tblPr></w:style>
</w:styles>'''


def escape_xml(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


def make_run(text, bold=False, italic=False):
    props = ''
    if bold:
        props += '<w:b/>'
    if italic:
        props += '<w:i/>'
    rpr = f'<w:rPr>{props}</w:rPr>' if props else ''
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'


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


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(26)
    w, h = struct.unpack('>II', head[16:24])
    return w, h


def make_image_paragraph(rid, w_px, h_px, name):
    disp_w = int(MAX_WIDTH_IN * EMU_PER_INCH)
    disp_h = int(disp_w * h_px / w_px)
    drawing = f'''<w:p><w:pPr><w:pStyle w:val="ImagePara"/></w:pPr><w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
  <wp:extent cx="{disp_w}" cy="{disp_h}"/>
  <wp:docPr id="{rid}" name="{name}"/>
  <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
    <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
      <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
        <pic:nvPicPr><pic:cNvPr id="{rid}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>
        <pic:blipFill><a:blip r:embed="rId{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
        <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{disp_w}" cy="{disp_h}"/></a:xfrm>
        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
      </pic:pic>
    </a:graphicData>
  </a:graphic>
</wp:inline></w:drawing></w:r></w:p>'''
    return drawing


def make_table(headers, rows):
    n = len(headers)
    col_w = 9360 // n
    tbl = ['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
           '<w:tblW w:w="9360" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '</w:tblBorders></w:tblPr>']
    tbl.append('<w:tblGrid>' + f'<w:gridCol w:w="{col_w}"/>' * n + '</w:tblGrid>')
    # header
    tbl.append('<w:tr>')
    for hcell in headers:
        tbl.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>'
                   '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>'
                   '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>%s</w:p></w:tc>'
                   % (col_w, make_run(hcell.strip(), bold=True)))
    tbl.append('</w:tr>')
    for row in rows:
        tbl.append('<w:tr>')
        for i in range(n):
            cell = row[i].strip() if i < len(row) else ''
            tbl.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/></w:tcPr>'
                       '<w:p><w:pPr><w:spacing w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>%s</w:p></w:tc>'
                       % (col_w, parse_inline(cell)))
        tbl.append('</w:tr>')
    tbl.append('</w:tbl>')
    # trailing empty paragraph so tables separate cleanly
    tbl.append('<w:p/>')
    return ''.join(tbl)


def build():
    with open(SRC, encoding='utf-8') as f:
        lines = f.read().split('\n')

    elements = []
    images = []  # (rid, relpath, mediafile)
    rid_counter = 100
    in_refs = False
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
        # image
        m = re.match(r'!\[(.*?)\]\((.*?)\)', s)
        if m:
            rel = m.group(2)
            abspath = os.path.join(BASE, rel)
            w, h = png_size(abspath)
            rid_counter += 1
            media_name = f'image{rid_counter}.png'
            images.append((rid_counter, abspath, media_name))
            elements.append(make_image_paragraph(rid_counter, w, h, os.path.basename(rel)))
            i += 1
            continue
        # table
        if '|' in line and i + 1 < len(lines) and re.search(r'\|\s*-', lines[i + 1]):
            headers = [c.strip() for c in line.split('|') if c.strip()]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].split('|') if c.strip() != ''])
                i += 1
            elements.append(make_table(headers, rows))
            continue
        # headings
        if s.startswith('# ') and not s.startswith('## '):
            elements.append(make_paragraph(s[2:].strip(), 'Title'))
            i += 1
            continue
        if s.startswith('## '):
            htxt = s[3:].strip()
            if htxt == 'References':
                in_refs = True
            elements.append(make_paragraph(htxt, 'Heading1'))
            i += 1
            continue
        if s.startswith('### '):
            elements.append(make_paragraph(s[4:].strip(), 'Heading2'))
            i += 1
            continue
        # figure/table captions
        if s.startswith('**Figure ') or s.startswith('**Table ') and '|' not in s:
            elements.append(make_paragraph(s, 'FigureCaption'))
            i += 1
            continue
        # abstract/keywords region: detect by heading handled above; style abstract paragraph
        if in_refs and re.match(r'^\[\d+\]', s):
            elements.append(make_paragraph(s, 'References'))
            i += 1
            continue
        elements.append(make_paragraph(s, 'Normal'))
        i += 1

    body = '\n'.join(elements)
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{body}
    <w:sectPr><w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    # relationships + content types (with image parts)
    rel_entries = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
                   '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>']
    for rid, _abspath, media in images:
        rel_entries.append(f'<Relationship Id="rId{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{media}"/>')
    word_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 + ''.join(rel_entries) + '</Relationships>')

    content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                     '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                     '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                     '<Default Extension="xml" ContentType="application/xml"/>'
                     '<Default Extension="png" ContentType="image/png"/>'
                     '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                     '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
                     '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
                     '</Types>')

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
        zf.writestr('word/numbering.xml', NUMBERING)
        for rid, abspath, media in images:
            with open(abspath, 'rb') as im:
                zf.writestr(f'word/media/{media}', im.read())

    print(f"Created {OUT} ({os.path.getsize(OUT)/1024:.1f} KB) with {len(images)} embedded figures")


if __name__ == '__main__':
    build()
