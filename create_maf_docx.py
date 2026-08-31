#!/usr/bin/env python3
"""
Build a Word .docx for the chapter
"Machine Learning-Based Prediction of Surface Roughness in Magnetic Abrasive Finishing"
from the markdown source, embedding the 20 PNG figures and rendering the 16 tables.

Uses raw OOXML (zipfile + XML) plus DrawingML for images - no external packages.
"""

import os
import re
import struct
import zipfile

CHAPTER_DIR = '/projects/sandbox/AMMAN'
MD_FILE = os.path.join(CHAPTER_DIR, 'Chapter_ML_MAF_Surface_Roughness.md')
FIG_DIR = os.path.join(CHAPTER_DIR, 'MAF_ML_figures')
OUT_FILE = os.path.join(CHAPTER_DIR, 'Chapter_ML_MAF_Surface_Roughness.docx')

EMU_PER_PIXEL = 9525          # 1 px at 96 dpi
MAX_IMG_WIDTH_EMU = 5486400   # ~6.0 inches usable width

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
    <w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1"><w:name w:val="Normal"/><w:pPr><w:jc w:val="both"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="100"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Abstract"><w:name w:val="Abstract"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:right="480"/></w:pPr><w:rPr><w:i/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="References"><w:name w:val="References"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="FigureImg"><w:name w:val="Figure Image"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/><w:keepNext/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption"><w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="240"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption"><w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="180" w:after="60"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
</w:styles>'''


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def run(text, bold=False, italic=False):
    props = ''
    if bold or italic:
        props = '<w:rPr>' + ('<w:b/>' if bold else '') + ('<w:i/>' if italic else '') + '</w:rPr>'
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (props, esc(text))


def inline(text):
    parts = re.split(r'(\*\*.*?\*\*|\*[^*]+?\*|`[^`]+?`)', text)
    out = []
    for p in parts:
        if not p:
            continue
        if p.startswith('**') and p.endswith('**'):
            out.append(run(p[2:-2], bold=True))
        elif p.startswith('*') and p.endswith('*'):
            out.append(run(p[1:-1], italic=True))
        elif p.startswith('`') and p.endswith('`'):
            out.append(run(p[1:-1]))
        else:
            out.append(run(p))
    return ''.join(out)


def para(text, style='Normal'):
    return '<w:p><w:pPr><w:pStyle w:val="%s"/></w:pPr>%s</w:p>' % (style, inline(text))


def table(headers, rows):
    n = len(headers)
    colw = 9360 // n
    b = ('<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
         '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
         '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
         '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
         '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
         '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>')
    t = ('<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
         '<w:tblBorders>%s</w:tblBorders></w:tblPr>' % b)
    t += '<w:tblGrid>' + ('<w:gridCol w:w="%d"/>' % colw) * n + '</w:tblGrid>'
    # header row
    t += '<w:tr><w:trPr><w:tblHeader/></w:trPr>'
    for h in headers:
        t += ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>'
              '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>'
              '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="20"/></w:pPr>%s</w:p></w:tc>'
              % (colw, run(h.strip(), bold=True)))
    t += '</w:tr>'
    for row in rows:
        t += '<w:tr>'
        for i in range(n):
            cell = row[i].strip() if i < len(row) else ''
            t += ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/></w:tcPr>'
                  '<w:p><w:pPr><w:spacing w:after="20"/></w:pPr>%s</w:p></w:tc>'
                  % (colw, inline(cell)))
        t += '</w:tr>'
    t += '</w:tbl><w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>'
    return t


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    # IHDR width/height are bytes 16-24
    w, h = struct.unpack('>II', head[16:24])
    return w, h


def image_para(rid, w_px, h_px, name):
    w_emu = w_px * EMU_PER_PIXEL
    h_emu = h_px * EMU_PER_PIXEL
    if w_emu > MAX_IMG_WIDTH_EMU:
        scale = MAX_IMG_WIDTH_EMU / float(w_emu)
        w_emu = int(w_emu * scale)
        h_emu = int(h_emu * scale)
    drawing = (
        '<w:r><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        '<wp:extent cx="%d" cy="%d"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        '<wp:docPr id="%d" name="%s"/>'
        '<wp:cNvGraphicFramePr>'
        '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr><pic:cNvPr id="%d" name="%s"/><pic:cNvPicPr/></pic:nvPicPr>'
        '<pic:blipFill><a:blip r:embed="%s" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
        '<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>'
        % (w_emu, h_emu, hash(name) & 0x7fffffff, esc(name),
           hash(name) & 0x7fffffff, esc(name), rid, w_emu, h_emu)
    )
    return '<w:p><w:pPr><w:pStyle w:val="FigureImg"/></w:pPr>%s</w:p>' % drawing


def build():
    with open(MD_FILE, encoding='utf-8') as f:
        lines = f.read().split('\n')

    body = []
    images = []          # (rId, media_filename, disk_path)
    rel_counter = [1]

    def next_rid():
        rid = 'rId%d' % rel_counter[0]
        rel_counter[0] += 1
        return rid

    in_refs = False
    i = 0
    fig_re = re.compile(r'^Figure\s+(\d+)\.')
    tbl_cap_re = re.compile(r'^Table\s+\d+\.')

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s == '---':
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
            body.append(para(txt, 'Heading1'))
            i += 1
            continue
        if s.startswith('### '):
            body.append(para(s[4:].strip(), 'Heading2'))
            i += 1
            continue
        if s.startswith('#### '):
            body.append(para(s[5:].strip(), 'Heading3'))
            i += 1
            continue

        # Table
        if '|' in line and i + 1 < len(lines) and re.search(r'\|?\s*-{2,}', lines[i + 1]) and '|' in lines[i + 1]:
            headers = [c.strip() for c in line.split('|') if c.strip()]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].split('|') if c.strip() != ''])
                i += 1
            body.append(table(headers, rows))
            continue

        # Figure caption -> insert image then caption
        m = fig_re.match(s)
        if m:
            num = int(m.group(1))
            fig_path = os.path.join(FIG_DIR, 'Figure_%d.png' % num)
            if os.path.exists(fig_path):
                rid = next_rid()
                media_name = 'image%d.png' % num
                images.append((rid, media_name, fig_path))
                w, h = png_size(fig_path)
                body.append(image_para(rid, w, h, 'Figure %d' % num))
            body.append(para(s, 'FigureCaption'))
            i += 1
            continue

        # Table caption
        if tbl_cap_re.match(s):
            body.append(para(s, 'TableCaption'))
            i += 1
            continue

        # Reference entry
        if in_refs and re.match(r'^\[\d+\]', s):
            body.append(para(s, 'References'))
            i += 1
            continue

        # Abstract keyword / bold-lead lines default to normal
        body.append(para(s, 'Normal'))
        i += 1

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<w:body>' + '\n'.join(body) +
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
        'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
        '</w:body></w:document>'
    )

    # document rels: styles + each image
    doc_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rid, media_name, _ in images:
        doc_rels.append('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/%s"/>'
                        % (rid, media_name))
    doc_rels.append('</Relationships>')
    doc_rels_xml = ''.join(doc_rels)

    with zipfile.ZipFile(OUT_FILE, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CONTENT_TYPES)
        z.writestr('_rels/.rels', RELS)
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', STYLES)
        z.writestr('word/_rels/document.xml.rels', doc_rels_xml)
        for _, media_name, disk_path in images:
            with open(disk_path, 'rb') as f:
                z.writestr('word/media/%s' % media_name, f.read())

    size_kb = os.path.getsize(OUT_FILE) / 1024
    print('Created %s (%.1f KB) with %d embedded figures.' % (OUT_FILE, size_kb, len(images)))


if __name__ == '__main__':
    build()
