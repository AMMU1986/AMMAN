#!/usr/bin/env python3
"""
Build the Word .docx for the chapter
"AI-Driven Research Support, Research Data Management, and Research Workflows".

Uses a raw-OOXML approach (python-docx is unavailable in this sandbox) and
embeds the generated PNG figures inline at each "[Insert Figure N here]"
placeholder, adding an italic caption beneath each figure.
"""

import zipfile
import os
import re
import struct

MD_FILE = '/projects/sandbox/AMMAN/Chapter_AI_Driven_Research_Support.md'
DOCX_FILE = '/projects/sandbox/AMMAN/Chapter_AI_Driven_Research_Support.docx'
FIG_DIR = '/projects/sandbox/AMMAN/research_figures'

FIGURE_FILES = {
    1: 'Figure_1_Research_Lifecycle.png',
    2: 'Figure_2_Adoption_Bar.png',
    3: 'Figure_3_Data_Architecture.png',
    4: 'Figure_4_Productivity_Trends.png',
}

FIGURE_CAPTIONS = {
    1: 'Figure 1. AI augmentation across the research lifecycle, showing '
       'stage-specific support underpinned by a cross-cutting layer of '
       'enabling AI capabilities.',
    2: 'Figure 2. Illustrative reported adoption of AI tools across research '
       'stages, contrasting current use with adoption planned within two years.',
    3: 'Figure 3. An AI-enabled, FAIR-aligned research data architecture, in '
       'which data is progressively acquired, curated, validated, stored, and '
       'governed.',
    4: 'Figure 4. Illustrative trends in AI-assisted research productivity '
       '(indexed to a 2019 baseline of 100) across literature discovery, '
       'analysis automation, and writing assistance.',
}

EMU_PER_INCH = 914400
TARGET_WIDTH_INCHES = 6.0

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
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
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
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="240"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureImage">
    <w:name w:val="Figure Image"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="0"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="160" w:after="60"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
</w:styles>'''


def png_dimensions(path):
    with open(path, 'rb') as f:
        header = f.read(24)
    if header[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('Not a PNG: ' + path)
    return struct.unpack('>II', header[16:24])


def escape_xml(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
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
    return (f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
            f'{parse_inline(text)}</w:p>')


def make_image_paragraph(rel_id, idx, cx, cy, name):
    doc_id = 1000 + idx
    drawing = (
        '<w:r><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{doc_id}" name="{escape_xml(name)}"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr><pic:cNvPr id="{doc_id}" name="{escape_xml(name)}"/>'
        '<pic:cNvPicPr/></pic:nvPicPr>'
        '<pic:blipFill>'
        f'<a:blip r:embed="{rel_id}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
        '<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/>'
        f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>'
    )
    return (f'<w:p><w:pPr><w:pStyle w:val="FigureImage"/></w:pPr>'
            f'{drawing}</w:p>')


def make_table(headers, rows):
    n = len(headers)
    col_w = 9360 // n
    tbl = ('<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/>'
           '<w:tblLayout w:type="fixed"/><w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '</w:tblBorders></w:tblPr>')
    tbl += '<w:tblGrid>' + f'<w:gridCol w:w="{col_w}"/>' * n + '</w:tblGrid>'
    tbl += '<w:tr>'
    for h in headers:
        tbl += ('<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="1B365D"/>'
                '<w:vAlign w:val="center"/></w:tcPr>'
                '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="40"/></w:pPr>'
                f'<w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="21"/></w:rPr>'
                f'<w:t xml:space="preserve">{escape_xml(h.strip())}</w:t></w:r></w:p></w:tc>')
    tbl += '</w:tr>'
    for ri, row in enumerate(rows):
        fill = 'EDF1F7' if ri % 2 else 'FFFFFF'
        tbl += '<w:tr>'
        for cell in row:
            tbl += (f'<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{fill}"/></w:tcPr>'
                    '<w:p><w:pPr><w:spacing w:after="40"/></w:pPr>'
                    f'<w:r><w:rPr><w:sz w:val="21"/></w:rPr>'
                    f'<w:t xml:space="preserve">{escape_xml(cell.strip())}</w:t></w:r></w:p></w:tc>')
        for _ in range(n - len(row)):
            tbl += '<w:tc><w:p/></w:tc>'
        tbl += '</w:tr>'
    tbl += '</w:tbl><w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>'
    return tbl


def md_to_body(md, image_rels):
    out = []
    lines = md.split('\n')
    i = 0
    in_refs = False
    in_abstract = False
    img_counter = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip() == '---':
            i += 1
            continue

        if line.startswith('# ') and not line.startswith('## '):
            out.append(make_paragraph(line[2:].strip(), 'Title'))
            i += 1
            continue
        if line.startswith('## '):
            h = line[3:].strip()
            in_refs = (h == 'References')
            in_abstract = (h == 'Abstract')
            out.append(make_paragraph(h, 'Heading1'))
            i += 1
            continue
        if line.startswith('### '):
            in_abstract = False
            out.append(make_paragraph(line[4:].strip(), 'Heading2'))
            i += 1
            continue
        if line.startswith('#### '):
            out.append(make_paragraph(line[5:].strip(), 'Heading3'))
            i += 1
            continue

        # markdown table
        if '|' in line and i + 1 < len(lines) and re.match(r'^\s*\|?\s*-', lines[i + 1]) and '---' in lines[i + 1]:
            headers = [c.strip() for c in line.split('|') if c.strip()]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].split('|') if c.strip()])
                i += 1
            out.append(make_table(headers, rows))
            continue

        # figure placeholder
        m = re.match(r'\[Insert Figure (\d+) here\]', line.strip())
        if m:
            fig = int(m.group(1))
            fname = FIGURE_FILES.get(fig)
            fpath = os.path.join(FIG_DIR, fname) if fname else None
            if fpath and os.path.exists(fpath):
                img_counter += 1
                rel_id = f'rIdImg{img_counter}'
                image_rels.append((rel_id, fname))
                w, h = png_dimensions(fpath)
                cx = int(TARGET_WIDTH_INCHES * EMU_PER_INCH)
                cy = int(cx * h / w)
                out.append(make_image_paragraph(rel_id, img_counter, cx, cy, fname))
                if fig in FIGURE_CAPTIONS:
                    out.append(make_paragraph(FIGURE_CAPTIONS[fig], 'FigureCaption'))
            else:
                out.append(make_paragraph(line.strip(), 'FigureCaption'))
            i += 1
            continue

        # table caption line (**Table N.** ...)
        if line.strip().startswith('**Table '):
            out.append(make_paragraph(line.strip(), 'TableCaption'))
            i += 1
            continue

        if line.strip().startswith('**Keywords:**'):
            out.append(make_paragraph(line.strip(), 'Abstract'))
            i += 1
            continue

        if in_refs and re.match(r'^\[\d+\]', line.strip()):
            out.append(make_paragraph(line.strip(), 'References'))
            i += 1
            continue

        if in_abstract:
            out.append(make_paragraph(line.strip(), 'Abstract'))
            i += 1
            continue

        out.append(make_paragraph(line.strip(), 'Normal'))
        i += 1
    return '\n'.join(out)


def build_word_rels(image_rels):
    r = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
         '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
         '  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
         '  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>']
    for rel_id, fname in image_rels:
        r.append(f'  <Relationship Id="{rel_id}" '
                 'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                 f'Target="media/{fname}"/>')
    r.append('</Relationships>')
    return '\n'.join(r)


def create_docx(md_path, out_path):
    with open(md_path, encoding='utf-8') as f:
        md = f.read()
    image_rels = []
    body = md_to_body(md, image_rels)
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{body}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"
               w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', build_word_rels(image_rels))
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
        zf.writestr('word/numbering.xml', NUMBERING)
        for _, fname in image_rels:
            with open(os.path.join(FIG_DIR, fname), 'rb') as img:
                zf.writestr(f'word/media/{fname}', img.read())
    print('Created:', out_path)
    print('Embedded figures:', ', '.join(fn for _, fn in image_rels))
    print(f'Size: {os.path.getsize(out_path)/1024:.1f} KB')


if __name__ == '__main__':
    create_docx(MD_FILE, DOCX_FILE)
