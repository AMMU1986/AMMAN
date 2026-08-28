#!/usr/bin/env python3
"""Build a .docx for the Industry 5.0 workforce chapter from markdown, with
embedded PNG figures and formatted tables. Uses raw OOXML (no python-docx)."""

import zipfile
import os
import re
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, "Chapter_AI_Workforce_Industry5.md")
OUT = os.path.join(HERE, "Chapter_AI_Workforce_Industry5.docx")

EMU_PER_PX = 9525
MAX_WIDTH_IN = 6.0
EMU_PER_IN = 914400

# ---------------- boilerplate ----------------

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''

CORE = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
  xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Artificial Intelligence for Inclusive and Sustainable Workforce Development in Industry 5.0</dc:title>
  <dc:subject>Artificial Intelligence for Sustainable Diversity, Equity, and Inclusion</dc:subject>
  <dc:creator>Chapter Author</dc:creator>
</cp:coreProperties>'''

APP = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
  <Application>Kiro</Application>
</Properties>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault><w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:sz w:val="24"/><w:szCs w:val="24"/>
    </w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr><w:spacing w:after="160" w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/><w:pPr><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="240" w:line="300" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
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
    <w:pPr><w:ind w:left="600" w:right="600"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="References">
    <w:name w:val="References"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="80"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureImg">
    <w:name w:val="Figure Image"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="160" w:after="60"/><w:keepNext/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="240"/></w:pPr>
    <w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="80"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
</w:styles>'''


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def png_size(path):
    with open(path, 'rb') as f:
        d = f.read(24)
    w, h = struct.unpack('>II', d[16:24])
    return w, h


# ---------------- run/paragraph builders ----------------

def runs_from_text(text):
    """Handle **bold** inline; everything else plain. Uses en-dash friendly."""
    out = []
    for part in re.split(r'(\*\*.*?\*\*)', text):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            out.append(f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{esc(part[2:-2])}</w:t></w:r>')
        else:
            out.append(f'<w:r><w:t xml:space="preserve">{esc(part)}</w:t></w:r>')
    return ''.join(out)


def para(text, style='Normal'):
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{runs_from_text(text)}</w:p>'


def image_para(rid, w_px, h_px, docpr_id, name):
    max_emu = int(MAX_WIDTH_IN * EMU_PER_IN)
    cx = w_px * EMU_PER_PX
    cy = h_px * EMU_PER_PX
    if cx > max_emu:
        scale = max_emu / cx
        cx = int(cx * scale)
        cy = int(cy * scale)
    drawing = f'''<w:p><w:pPr><w:pStyle w:val="FigureImg"/></w:pPr><w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
  <wp:extent cx="{cx}" cy="{cy}"/>
  <wp:effectExtent l="0" t="0" r="0" b="0"/>
  <wp:docPr id="{docpr_id}" name="{esc(name)}"/>
  <wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>
  <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
    <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
      <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
        <pic:nvPicPr>
          <pic:cNvPr id="{docpr_id}" name="{esc(name)}"/>
          <pic:cNvPicPr/>
        </pic:nvPicPr>
        <pic:blipFill>
          <a:blip r:embed="{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>
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
</w:drawing></w:r></w:p>'''
    return drawing


def build_table(headers, rows):
    n = len(headers)
    total = 9360
    col_w = total // n
    tbl = ['<w:tbl>']
    tbl.append('<w:tblPr>')
    tbl.append(f'<w:tblW w:w="{total}" w:type="dxa"/>')
    tbl.append('<w:tblLayout w:type="fixed"/>')
    tbl.append('<w:tblBorders>'
               '<w:top w:val="single" w:sz="4" w:space="0" w:color="666666"/>'
               '<w:left w:val="single" w:sz="4" w:space="0" w:color="666666"/>'
               '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="666666"/>'
               '<w:right w:val="single" w:sz="4" w:space="0" w:color="666666"/>'
               '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
               '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
               '</w:tblBorders>')
    tbl.append('</w:tblPr>')
    tbl.append('<w:tblGrid>' + (f'<w:gridCol w:w="{col_w}"/>' * n) + '</w:tblGrid>')

    # header
    tbl.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
    for h in headers:
        tbl.append('<w:tc>')
        tbl.append(f'<w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="1F4E79"/><w:vAlign w:val="center"/></w:tcPr>')
        tbl.append('<w:p><w:pPr><w:spacing w:before="40" w:after="40" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>'
                   f'<w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{esc(h)}</w:t></w:r></w:p>')
        tbl.append('</w:tc>')
    tbl.append('</w:tr>')

    for ri, row in enumerate(rows):
        shade = 'F2F6FB' if ri % 2 == 0 else 'FFFFFF'
        tbl.append('<w:tr>')
        for ci in range(n):
            cell = row[ci] if ci < len(row) else ''
            tbl.append('<w:tc>')
            tbl.append(f'<w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="{shade}"/><w:vAlign w:val="center"/></w:tcPr>')
            tbl.append('<w:p><w:pPr><w:spacing w:before="40" w:after="40" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>'
                       f'<w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{esc(cell)}</w:t></w:r></w:p>')
            tbl.append('</w:tc>')
        tbl.append('</w:tr>')
    tbl.append('</w:tbl>')
    tbl.append('<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>')
    return ''.join(tbl)


# ---------------- markdown parser ----------------

def parse():
    with open(MD, encoding='utf-8') as f:
        text = f.read()

    body = []
    images = []          # list of (rid, abspath, target)
    img_counter = 0
    docpr = 100

    lines = text.split('\n')
    i = 0
    in_refs = False
    in_abstract = False

    while i < len(lines):
        line = lines[i].rstrip('\n')
        s = line.strip()
        if not s:
            i += 1
            continue

        # figure marker
        m = re.match(r'\[\[FIGURE:(.+?)\|(.+?)\]\]', s)
        if m:
            img_counter += 1
            docpr += 1
            path = os.path.join(HERE, m.group(1))
            caption = m.group(2)
            w, h = png_size(path)
            rid = f'rIdImg{img_counter}'
            target = f'media/image{img_counter}.png'
            images.append((rid, path, target))
            body.append(image_para(rid, w, h, docpr, os.path.basename(path)))
            body.append(para(caption, 'FigureCaption'))
            i += 1
            continue

        # table marker
        m = re.match(r'\[\[TABLE:(.+)\]\]', s)
        if m:
            inner = m.group(1)
            parts = inner.split('|')
            caption = parts[0]
            headers = parts[1].split(';')
            rows = [p.split(';') for p in parts[2:]]
            body.append(para(caption, 'TableCaption'))
            body.append(build_table(headers, rows))
            i += 1
            continue

        # title
        if s.startswith('# ') and not s.startswith('## '):
            body.append(para(s[2:].strip(), 'Title'))
            i += 1
            continue

        # heading 1
        if s.startswith('## '):
            htxt = s[3:].strip()
            in_refs = (htxt == 'References')
            in_abstract = (htxt == 'Abstract')
            body.append(para(htxt, 'Heading1'))
            i += 1
            continue

        # heading 2
        if s.startswith('### '):
            in_abstract = False
            body.append(para(s[4:].strip(), 'Heading2'))
            i += 1
            continue

        # reference entry
        if in_refs and re.match(r'^\[\d+\]', s):
            body.append(para(s, 'References'))
            i += 1
            continue

        # normal / abstract / keywords
        if in_abstract:
            body.append(para(s, 'Abstract'))
        else:
            body.append(para(s, 'Normal'))
        i += 1

    return '\n'.join(body), images


def build():
    body_xml, images = parse()

    doc = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
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

    # document rels
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rid, _, target in images:
        rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{target}"/>')
    rels.append('</Relationships>')
    word_rels = '\n'.join(rels)

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CONTENT_TYPES)
        z.writestr('_rels/.rels', RELS)
        z.writestr('docProps/core.xml', CORE)
        z.writestr('docProps/app.xml', APP)
        z.writestr('word/_rels/document.xml.rels', word_rels)
        z.writestr('word/document.xml', doc)
        z.writestr('word/styles.xml', STYLES)
        for _, abspath, target in images:
            with open(abspath, 'rb') as f:
                z.writestr('word/' + target, f.read())

    print("Wrote", OUT, f"({os.path.getsize(OUT)/1024:.1f} KB), images embedded: {len(images)}")


if __name__ == '__main__':
    build()
