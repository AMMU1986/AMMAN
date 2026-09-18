#!/usr/bin/env python3
"""
build_docx.py - Assemble the fully formatted Word (.docx) manuscript for
Chapter 5, "Human-in-the-Loop and Explainable AI in Mission Control Systems".

python-docx is unavailable in this sandbox, so the document is written as raw
Office Open XML packed into a .docx (ZIP). The four JPEG figures are embedded
inline where their [[FIGURE 5.x]] placeholders occur.

Formatting: Times New Roman, 12 pt, 1.5 line spacing, numeric [n] citations,
chapter-scoped section / figure / table / equation numbering (5.x).
"""

import os
import re
import struct
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(HERE, 'chapter.md')
OUT_FILE = os.path.join(HERE, '..',
                        'Chapter_5_HITL_XAI_Mission_Control.docx')
FIG_DIR = os.path.join(HERE, '..', 'hitl_figures')

FIGURE_FILES = {
    '5.1': 'Figure_5_1_Autonomy_Spectrum.jpg',
    '5.2': 'Figure_5_2_Reference_Architecture.jpg',
    '5.3': 'Figure_5_3_Explanation_Taxonomy.jpg',
    '5.4': 'Figure_5_4_Depth_vs_Performance.jpg',
}

EMU_PER_INCH = 914400
TARGET_WIDTH_INCHES = 6.0

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="jpeg" ContentType="image/jpeg"/>
  <Default Extension="jpg" ContentType="image/jpeg"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

# 1.5 spacing => line=360 (240*1.5); TNR 12pt => sz 24 half-points.
STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault><w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:sz w:val="24"/><w:szCs w:val="24"/>
    </w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr>
      <w:spacing w:after="160" w:line="360" w:lineRule="auto"/>
    </w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/><w:pPr><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ChapterNum">
    <w:name w:val="ChapterNum"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="60"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:color w:val="404040"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="240"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="AuthorLine">
    <w:name w:val="AuthorLine"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="40"/></w:pPr>
    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:keepNext/><w:spacing w:before="320" w:after="120"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:keepNext/><w:spacing w:before="240" w:after="100"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:i/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="AbstractBody">
    <w:name w:val="AbstractBody"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="360" w:right="360"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Equation">
    <w:name w:val="Equation"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="80"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="References">
    <w:name w:val="References"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="80"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureImage">
    <w:name w:val="FigureImage"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="160" w:after="40"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Caption">
    <w:name w:val="Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="200"/><w:ind w:left="360" w:right="360"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="TableCaption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:keepNext/><w:spacing w:before="200" w:after="80"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCell">
    <w:name w:val="TableCell"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:after="20" w:line="276" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
</w:styles>'''


def jpeg_dimensions(path):
    """Read (width, height) in pixels from a JPEG's SOF marker."""
    with open(path, 'rb') as f:
        data = f.read()
    if data[:2] != b'\xff\xd8':
        raise ValueError('Not a JPEG: %s' % path)
    i = 2
    n = len(data)
    while i < n:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        i += 2
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            continue
        if i + 2 > n:
            break
        seg_len = struct.unpack('>H', data[i:i + 2])[0]
        # SOF0..SOF15 except DHT(C4), JPG(C8), DAC(CC)
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h = struct.unpack('>H', data[i + 3:i + 5])[0]
            w = struct.unpack('>H', data[i + 5:i + 7])[0]
            return w, h
        i += seg_len
    raise ValueError('No SOF marker found in %s' % path)


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def run(text, bold=False, italic=False, sup=False):
    props = []
    if bold:
        props.append('<w:b/>')
    if italic:
        props.append('<w:i/>')
    if sup:
        props.append('<w:vertAlign w:val="superscript"/>')
    rpr = '<w:rPr>' + ''.join(props) + '</w:rPr>' if props else ''
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, esc(text))


def parse_inline(text):
    """Handle **bold**, *italic*, and ^superscript (single token or ^{...})."""
    out = []
    # first split on bold/italic
    pattern = r'(\*\*.*?\*\*|\*[^*]+?\*)'
    for part in re.split(pattern, text):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            out.append(_with_sup(part[2:-2], bold=True))
        elif part.startswith('*') and part.endswith('*'):
            out.append(_with_sup(part[1:-1], italic=True))
        else:
            out.append(_with_sup(part))
    return ''.join(out)


def _with_sup(text, bold=False, italic=False):
    """Split text on ^markers, rendering the marker as superscript.
    Supports ^1, ^1,* style: superscript runs until a space."""
    out = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == '^':
            j = i + 1
            # superscript token: letters/digits/comma/asterisk, stop at space
            while j < len(text) and text[j] not in ' \t':
                j += 1
            token = text[i + 1:j]
            if token:
                out.append(run(token, bold=bold, italic=italic, sup=True))
            i = j
        else:
            j = text.find('^', i)
            if j == -1:
                j = len(text)
            out.append(run(text[i:j], bold=bold, italic=italic))
            i = j
    return ''.join(out)


def para(text, style='Normal'):
    ppr = '<w:pPr><w:pStyle w:val="%s"/></w:pPr>' % style
    return '<w:p>%s%s</w:p>' % (ppr, parse_inline(text))


def image_para(rel_id, idx, cx, cy, name):
    did = 2000 + idx
    drawing = (
        '<w:r><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        '<wp:extent cx="%d" cy="%d"/>' % (cx, cy) +
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        '<wp:docPr id="%d" name="%s"/>' % (did, esc(name)) +
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'noChangeAspect="1"/></wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr><pic:cNvPr id="%d" name="%s"/>' % (did, esc(name)) +
        '<pic:cNvPicPr/></pic:nvPicPr>'
        '<pic:blipFill><a:blip r:embed="%s" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>' % rel_id +
        '<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/>'
        '<a:ext cx="%d" cy="%d"/></a:xfrm>' % (cx, cy) +
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline>'
        '</w:drawing></w:r>'
    )
    return '<w:p><w:pPr><w:pStyle w:val="FigureImage"/></w:pPr>%s</w:p>' % drawing


def make_table(headers, rows):
    ncol = len(headers)
    total = 9360
    colw = total // ncol
    borders = (
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '</w:tblBorders>')
    t = ('<w:tbl><w:tblPr><w:tblW w:w="%d" w:type="dxa"/>'
         '<w:tblLayout w:type="fixed"/>%s</w:tblPr>' % (total, borders))
    t += '<w:tblGrid>' + ('<w:gridCol w:w="%d"/>' % colw) * ncol + '</w:tblGrid>'
    # header row
    t += '<w:tr><w:trPr><w:tblHeader/></w:trPr>'
    for h in headers:
        t += ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>'
              '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>'
              '<w:vAlign w:val="center"/></w:tcPr>'
              '<w:p><w:pPr><w:pStyle w:val="TableCell"/><w:jc w:val="center"/></w:pPr>%s</w:p></w:tc>'
              % (colw, run(h, bold=True)))
    t += '</w:tr>'
    for r in rows:
        t += '<w:tr>'
        for c in range(ncol):
            cell = r[c] if c < len(r) else ''
            t += ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/></w:tcPr>'
                  '<w:p><w:pPr><w:pStyle w:val="TableCell"/></w:pPr>%s</w:p></w:tc>'
                  % (colw, parse_inline(cell)))
        t += '</w:tr>'
    t += '</w:tbl>'
    # spacer paragraph so tables don't collide with following text
    t += '<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>'
    return t


def build_body(md, image_rels):
    lines = md.split('\n')
    els = []
    i = 0
    n = len(lines)
    title_count = 0
    in_refs = False
    in_authors = False
    in_abstract = False
    img_idx = 0

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # figure placeholder
        m = re.match(r'\[\[FIGURE (\d+\.\d+)\]\]', stripped)
        if m:
            key = m.group(1)
            fname = FIGURE_FILES.get(key)
            fpath = os.path.join(FIG_DIR, fname) if fname else None
            if fpath and os.path.exists(fpath):
                img_idx += 1
                rel = 'rIdImg%d' % img_idx
                image_rels.append((rel, fname))
                pw, ph = jpeg_dimensions(fpath)
                cx = int(TARGET_WIDTH_INCHES * EMU_PER_INCH)
                cy = int(cx * ph / pw)
                els.append(image_para(rel, img_idx, cx, cy, fname))
            i += 1
            continue

        # headings
        if stripped.startswith('#### '):
            els.append(para(stripped[5:].strip(), 'Heading2'))
            i += 1
            continue
        if stripped.startswith('### '):
            els.append(para(stripped[4:].strip(), 'Heading2'))
            i += 1
            continue
        if stripped.startswith('## '):
            htext = stripped[3:].strip()
            if htext.lower() == 'references':
                in_refs = True
            in_abstract = (htext.lower() == 'abstract')
            in_authors = False
            els.append(para(htext, 'Heading1'))
            i += 1
            continue
        if stripped.startswith('# '):
            htext = stripped[2:].strip()
            title_count += 1
            if title_count == 1:
                els.append(para(htext, 'ChapterNum'))
            else:
                els.append(para(htext, 'Title'))
                in_authors = True  # author block follows the title
            i += 1
            continue

        # table: header line with pipes followed by --- separator
        if '|' in line and i + 1 < n and re.match(r'^\s*\|?[\s:\-|]+\|?\s*$', lines[i + 1]) and '-' in lines[i + 1]:
            headers = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < n and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            els.append(make_table(headers, rows))
            continue

        # captions
        if re.match(r'^Figure \d+\.\d+\.', stripped):
            els.append(para(stripped, 'Caption'))
            i += 1
            continue
        if re.match(r'^Table \d+\.\d+\.', stripped):
            els.append(para(stripped, 'TableCaption'))
            i += 1
            continue

        # equations
        if re.match(r'^\(\d+\.\d+\)', stripped):
            els.append(para(stripped, 'Equation'))
            i += 1
            continue

        # references
        if in_refs and re.match(r'^\[\d+\]', stripped):
            els.append(para(stripped, 'References'))
            i += 1
            continue

        # abstract body / keywords
        if stripped.startswith('**Keywords:**'):
            els.append(para(stripped, 'AbstractBody'))
            in_abstract = False
            i += 1
            continue

        # author block lines (between title and first '## ')
        if in_authors:
            els.append(para(stripped, 'AuthorLine'))
            i += 1
            continue

        if in_abstract:
            els.append(para(stripped, 'AbstractBody'))
            i += 1
            continue

        els.append(para(stripped, 'Normal'))
        i += 1

    return '\n'.join(els)


def build_word_rels(image_rels):
    out = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
           '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
           '  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rel, fname in image_rels:
        out.append('  <Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/%s"/>' % (rel, fname))
    out.append('</Relationships>')
    return '\n'.join(out)


def main():
    with open(MD_FILE, encoding='utf-8') as f:
        md = f.read()
    # detect abstract region to style its paragraphs
    md = _mark_abstract(md)

    image_rels = []
    body = build_body(md, image_rels)

    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                '<w:body>%s'
                '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
                '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
                'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
                '</w:body></w:document>' % body)

    word_rels = build_word_rels(image_rels)

    with zipfile.ZipFile(OUT_FILE, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CONTENT_TYPES)
        z.writestr('_rels/.rels', RELS)
        z.writestr('word/_rels/document.xml.rels', word_rels)
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', STYLES)
        for _, fname in image_rels:
            with open(os.path.join(FIG_DIR, fname), 'rb') as img:
                z.writestr('word/media/%s' % fname, img.read())

    size_kb = os.path.getsize(OUT_FILE) / 1024
    print('Created:', os.path.abspath(OUT_FILE))
    print('Embedded %d figure(s): %s' % (len(image_rels),
          ', '.join(fn for _, fn in image_rels)))
    print('Size: %.1f KB' % size_kb)


def _mark_abstract(md):
    """Style paragraphs under '## Abstract' (before Keywords) as AbstractBody
    by converting them; done by wrapping with a sentinel the parser understands.
    Simpler approach: replace the abstract paragraph with an AbstractBody tag via
    a marker recognised in build_body. Here we just prefix a zero-width marker."""
    return md  # abstract paragraph handled as Normal; keywords already styled


if __name__ == '__main__':
    main()
