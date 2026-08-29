#!/usr/bin/env python3
"""
Build a Word .docx for the Migration, Governance and Regional Politics chapter.
Pure standard library (no python-docx). Embeds PNG figures, renders tables,
headings, references and figure captions.
"""

import zipfile
import os
import re
import struct

BASE = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(BASE, 'Chapter_Migration_Governance.md')
FIG_DIR = os.path.join(BASE, 'migration_figures')
OUT_FILE = os.path.join(BASE, 'Chapter_Migration_Governance.docx')

EMU_PER_PX = 9525  # 96 dpi
MAX_WIDTH_EMU = 5486400  # ~6 inches usable width

FIG_CAPTIONS = {
    1: "Figure 1. Analytical framework linking the structural drivers of migration, the "
       "multi-level governance layer, and political and developmental outcomes, with a "
       "feedback loop from outcomes to drivers.",
    2: "Figure 2. Principal migration corridors within and between the Middle East and "
       "Africa (schematic; arrows indicate the dominant direction of labour, forced and "
       "mixed migration flows; not to scale).",
    3: "Figure 3. Illustrative trends in remittance inflows, forced displacement, and the "
       "composition of migration flows, highlighting the coexistence of economic promise "
       "and social strain.",
    4: "Figure 4. Multi-level governance architecture and a scenario space defined by the "
       "openness of policy and the degree of cooperation, ranging from fortress region to "
       "inclusive mobility.",
}

# ─── OOXML boilerplate ───

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>'''

CORE = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
  xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Migration, Governance, and Regional Politics in the Middle East and Africa</dc:title>
  <dc:creator>Book Chapter</dc:creator>
</cp:coreProperties>'''

NUMBERING = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault><w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1"><w:name w:val="Normal"/>
    <w:pPr><w:jc w:val="both"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Abstract"><w:name w:val="Abstract"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:right="480"/></w:pPr><w:rPr><w:i/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="References"><w:name w:val="References"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="FigureImage"><w:name w:val="Figure Image"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="180" w:after="60"/><w:keepNext/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption"><w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="240"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption"><w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="60"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Keywords"><w:name w:val="Keywords"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:right="480"/><w:spacing w:after="240"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
</w:styles>'''


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def make_run(text, bold=False, italic=False, sz=None):
    props = []
    if bold:
        props.append('<w:b/>')
    if italic:
        props.append('<w:i/>')
    if sz:
        props.append(f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
    rpr = ('<w:rPr>' + ''.join(props) + '</w:rPr>') if props else ''
    return f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'


def parse_inline(text):
    runs = []
    parts = re.split(r'(\*\*.*?\*\*|\*[^*]+?\*)', text)
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


def para(text, style='Normal'):
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{parse_inline(text)}</w:p>'


def make_table(headers, rows):
    n = len(headers)
    col_w = 9360 // n
    tbl = ('<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '</w:tblBorders></w:tblPr>')
    tbl += '<w:tblGrid>' + (f'<w:gridCol w:w="{col_w}"/>' * n) + '</w:tblGrid>'
    # header
    tbl += '<w:tr><w:trPr><w:tblHeader/></w:trPr>'
    for h in headers:
        tbl += ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>'
                '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>'
                '<w:vAlign w:val="center"/></w:tcPr>'
                '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>%s</w:p></w:tc>'
                % (col_w, make_run(h.strip(), bold=True, sz=20)))
    tbl += '</w:tr>'
    for row in rows:
        tbl += '<w:tr>'
        for i in range(n):
            cell = row[i].strip() if i < len(row) else ''
            tbl += ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
                    '<w:p><w:pPr><w:spacing w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>%s</w:p></w:tc>'
                    % (col_w, make_run(cell, sz=20)))
        tbl += '</w:tr>'
    tbl += '</w:tbl><w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>'
    return tbl


def png_size(path):
    with open(path, 'rb') as f:
        f.read(16)
        w, h = struct.unpack('>II', f.read(8))
    return w, h


def make_image(rid, path, docpr_id):
    w, h = png_size(path)
    width_emu = w * EMU_PER_PX
    height_emu = h * EMU_PER_PX
    if width_emu > MAX_WIDTH_EMU:
        scale = MAX_WIDTH_EMU / width_emu
        width_emu = int(width_emu * scale)
        height_emu = int(height_emu * scale)
    return (
        '<w:p><w:pPr><w:pStyle w:val="FigureImage"/></w:pPr><w:r><w:drawing>'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        f'<wp:extent cx="{width_emu}" cy="{height_emu}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{docpr_id}" name="Figure{docpr_id}"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr>'
        f'<pic:cNvPr id="{docpr_id}" name="Figure{docpr_id}.png"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rid}" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
        '<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/>'
        f'<a:ext cx="{width_emu}" cy="{height_emu}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'
    )


def build_body(md, image_rels):
    """image_rels: dict fig_num -> rId. Returns body xml."""
    elements = []
    lines = md.split('\n')
    i = 0
    in_refs = False
    docpr = 100
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue

        # figure marker
        m = re.match(r'\[\[FIGURE:(\d+)\]\]', s)
        if m:
            n = int(m.group(1))
            elements.append(make_image(image_rels[n], os.path.join(FIG_DIR, f'Figure_{n}.png'), docpr))
            docpr += 1
            elements.append(para(FIG_CAPTIONS[n], 'FigureCaption'))
            i += 1
            continue

        if s == '---':
            i += 1
            continue
        if s.startswith('# ') and not s.startswith('## '):
            elements.append(para(s[2:].strip(), 'Title'))
            i += 1
            continue
        if s.startswith('## '):
            h = s[3:].strip()
            if h == 'References':
                in_refs = True
            elements.append(para(h, 'Heading1'))
            i += 1
            continue
        if s.startswith('### '):
            elements.append(para(s[4:].strip(), 'Heading2'))
            i += 1
            continue
        if s.startswith('#### '):
            elements.append(para(s[5:].strip(), 'Heading3'))
            i += 1
            continue
        # table
        if '|' in line and i + 1 < len(lines) and re.match(r'^\s*\|?\s*-', lines[i+1]) and '---' in lines[i+1]:
            headers = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            elements.append(make_table(headers, rows))
            continue
        # abstract paragraph (right after ## Abstract heading, italic)
        if s.startswith('**Keywords:**'):
            elements.append(para(s, 'Keywords'))
            i += 1
            continue
        if s.startswith('**Table '):
            elements.append(para(s, 'TableCaption'))
            i += 1
            continue
        if in_refs and re.match(r'^\[\d+\]', s):
            elements.append(para(s, 'References'))
            i += 1
            continue
        # Detect abstract body: heading 'Abstract' style handled by preceding; use italic Abstract for the abstract paragraph
        elements.append(para(s, 'Normal'))
        i += 1
    return '\n'.join(elements)


def main():
    with open(MD_FILE, encoding='utf-8') as f:
        md = f.read()

    # Mark the abstract paragraph as Abstract style: find text between '## Abstract' and '**Keywords'
    # We'll do a light transform: replace the abstract body paragraph handling by style.
    # Simpler: post-process by tagging. Detect the single long paragraph after '## Abstract'.
    image_rels = {1: 'rId10', 2: 'rId11', 3: 'rId12', 4: 'rId13'}

    body = build_body(md, image_rels)

    # Convert the abstract paragraph (first Normal para after Abstract heading) to Abstract style.
    # Find '## Abstract' heading element then the following Normal paragraph.
    body = re.sub(
        r'(<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r>(?:<w:rPr>[^<]*</w:rPr>)?<w:t xml:space="preserve">Abstract</w:t></w:r></w:p>\s*)<w:p><w:pPr><w:pStyle w:val="Normal"/>',
        r'\1<w:p><w:pPr><w:pStyle w:val="Abstract"/>',
        body, count=1)

    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
                'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
                'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
                'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
                '<w:body>' + body +
                '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
                '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
                'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>')

    # relationships including images
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
            '<Relationship Id="rId10" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/Figure_1.png"/>'
            '<Relationship Id="rId11" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/Figure_2.png"/>'
            '<Relationship Id="rId12" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/Figure_3.png"/>'
            '<Relationship Id="rId13" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/Figure_4.png"/>'
            '</Relationships>')

    with zipfile.ZipFile(OUT_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('docProps/core.xml', CORE)
        zf.writestr('word/_rels/document.xml.rels', rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
        zf.writestr('word/numbering.xml', NUMBERING)
        for n in range(1, 5):
            with open(os.path.join(FIG_DIR, f'Figure_{n}.png'), 'rb') as im:
                zf.writestr(f'word/media/Figure_{n}.png', im.read())

    print('Created', OUT_FILE, '(%.1f KB)' % (os.path.getsize(OUT_FILE)/1024))


if __name__ == '__main__':
    main()
