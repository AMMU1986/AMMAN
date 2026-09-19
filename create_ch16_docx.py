#!/usr/bin/env python3
"""
Build the Chapter 16 Word (.docx) file from its Markdown source, formatted to
the publisher's Publication Guide:

  * Page size A5 (148 x 210 mm)
  * Margins: top 2.5 cm, bottom 1.5 cm, left 2.1 cm, right 2.1 cm,
             header 1.5 cm, footer 0 cm
  * Font: Times New Roman throughout
      - Main text: 10 pt, justified
      - Chapter title: 16 pt, centred
      - Author's name: 16 pt, centred
      - Secondary headings: 12 pt, centred, bold
      - Footnotes / captions: 9 pt
  * Figures embedded in JPEG format at their intended location, captioned
    "Fig. 16-n"; tables titled "Table 16-n".

python-docx is not available in this sandbox, so the file is assembled directly
as OOXML (a ZIP of XML parts), following the approach already used in this
repository (create_agentic_docx.py).
"""

import os
import re
import struct
import zipfile

MD_FILE = '/projects/sandbox/AMMAN/Chapter_16_Digital_Twins_Intelligent_Automation.md'
DOCX_FILE = '/projects/sandbox/AMMAN/Chapter_16_Digital_Twins_Intelligent_Automation.docx'
FIG_DIR = '/projects/sandbox/AMMAN/ch16_figures'

FIGURE_FILES = {
    1: 'Fig_16_1_DT_Architecture.jpg',
    2: 'Fig_16_2_Industry_4_to_5.jpg',
    3: 'Fig_16_3_Integration_Loop.jpg',
    4: 'Fig_16_4_Benefits.jpg',
}

EMU_PER_MM = 36000
TARGET_WIDTH_MM = 104          # fits within the ~106 mm A5 text column
TABLE_WIDTH_TWIPS = 5800       # fits within the A5 text width

# ─── OOXML parts ───

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="jpg" ContentType="image/jpeg"/>
  <Default Extension="jpeg" ContentType="image/jpeg"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

# Font sizes are in half-points (Word convention): 10pt=20, 12pt=24, 16pt=32, 9pt=18.
STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="20"/><w:szCs w:val="20"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr><w:spacing w:after="120" w:line="240" w:lineRule="auto"/></w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
    <w:pPr><w:jc w:val="both"/></w:pPr>
    <w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Author">
    <w:name w:val="Author"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr>
    <w:rPr><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:keepNext/><w:jc w:val="center"/><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:keepNext/><w:jc w:val="left"/><w:spacing w:before="160" w:after="80"/></w:pPr>
    <w:rPr><w:b/><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Abstract">
    <w:name w:val="Abstract"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="284" w:right="284"/></w:pPr>
    <w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="References">
    <w:name w:val="References"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="340" w:hanging="340"/><w:spacing w:after="60"/></w:pPr>
    <w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureImage">
    <w:name w:val="Figure Image"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:keepNext/><w:jc w:val="center"/><w:spacing w:before="160" w:after="40"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="200"/></w:pPr>
    <w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:keepNext/><w:jc w:val="left"/><w:spacing w:before="160" w:after="60"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>
  </w:style>
</w:styles>'''


def png_or_jpeg_dimensions(path):
    """Return (width, height) in pixels for a JPEG (or PNG) file."""
    with open(path, 'rb') as f:
        data = f.read()
    if data[:2] == b'\xff\xd8':  # JPEG: scan for SOF marker
        i = 2
        while i < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3):
                h = (data[i + 5] << 8) | data[i + 6]
                w = (data[i + 7] << 8) | data[i + 8]
                return w, h
            seg_len = (data[i + 2] << 8) | data[i + 3]
            i += 2 + seg_len
        raise ValueError('No SOF marker in JPEG: ' + path)
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        w, h = struct.unpack('>II', data[16:24])
        return w, h
    raise ValueError('Unknown image format: ' + path)


def escape_xml(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;')
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
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'


def parse_inline(text):
    """Render inline **bold** and *italic* markdown as runs."""
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


def make_caption_paragraph(text, style):
    """Caption with a bold 'Fig. 16-n.'/'Table 16-n.' label then normal text."""
    m = re.match(r'((?:Fig\.|Table) 16-\d+\.)\s*(.*)', text)
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
    if m:
        runs = make_run(m.group(1) + ' ', bold=True, sz=18) + make_run(m.group(2), sz=18)
    else:
        runs = make_run(text, sz=18)
    return f'<w:p>{ppr}{runs}</w:p>'


def make_image_paragraph(rel_id, idx, cx, cy, name):
    doc_pr = 1000 + idx
    drawing = (
        '<w:r><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{doc_pr}" name="{escape_xml(name)}"/>'
        '<wp:cNvGraphicFramePr>'
        '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr>'
        f'<pic:cNvPr id="{doc_pr}" name="{escape_xml(name)}"/><pic:cNvPicPr/>'
        '</pic:nvPicPr>'
        '<pic:blipFill>'
        f'<a:blip r:embed="{rel_id}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
        '<a:stretch><a:fillRect/></a:stretch>'
        '</pic:blipFill>'
        '<pic:spPr>'
        f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        '</pic:spPr></pic:pic>'
        '</a:graphicData></a:graphic>'
        '</wp:inline></w:drawing></w:r>'
    )
    return f'<w:p><w:pPr><w:pStyle w:val="FigureImage"/></w:pPr>{drawing}</w:p>'


def make_table(headers, rows):
    n = len(headers)
    col_w = TABLE_WIDTH_TWIPS // n
    borders = ('<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>')
    tbl = ['<w:tbl><w:tblPr>'
           f'<w:tblW w:w="{TABLE_WIDTH_TWIPS}" w:type="dxa"/>'
           '<w:jc w:val="center"/><w:tblLayout w:type="fixed"/>'
           f'<w:tblBorders>{borders}</w:tblBorders></w:tblPr>']
    tbl.append('<w:tblGrid>' + f'<w:gridCol w:w="{col_w}"/>' * n + '</w:tblGrid>')

    def cell(text, header=False):
        shd = '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>' if header else ''
        jc = 'center' if header else 'left'
        run = make_run(text.strip(), bold=header, sz=18)
        return (f'<w:tc><w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/>{shd}'
                '<w:vAlign w:val="center"/></w:tcPr>'
                f'<w:p><w:pPr><w:spacing w:after="20" w:line="240" w:lineRule="auto"/>'
                f'<w:jc w:val="{jc}"/></w:pPr>{run}</w:p></w:tc>')

    tbl.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>'
               + ''.join(cell(h, header=True) for h in headers) + '</w:tr>')
    for row in rows:
        cells = [cell(c) for c in row]
        cells += ['<w:tc><w:p/></w:tc>'] * (n - len(row))
        tbl.append('<w:tr>' + ''.join(cells) + '</w:tr>')
    tbl.append('</w:tbl><w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>')
    return ''.join(tbl)


def md_to_body(md_text, image_rels):
    elements = []
    lines = md_text.split('\n')
    i = 0
    in_refs = False
    img_count = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s or s == '---':
            i += 1
            continue

        if line.startswith('# ') and not line.startswith('## '):
            elements.append(make_paragraph(s[2:].strip(), 'Title'))
            i += 1
            continue
        if s.startswith('@AUTHORS '):
            elements.append(make_paragraph(s[len('@AUTHORS '):].strip(), 'Author'))
            i += 1
            continue
        if line.startswith('## '):
            heading = s[3:].strip()
            if heading.lower() == 'references':
                in_refs = True
            elements.append(make_paragraph(heading, 'Heading1'))
            i += 1
            continue
        if line.startswith('### '):
            elements.append(make_paragraph(s[4:].strip(), 'Heading2'))
            i += 1
            continue

        # Image placeholder
        m = re.match(r'\[\[FIG:(\d+)\]\]', s)
        if m:
            num = int(m.group(1))
            fname = FIGURE_FILES.get(num)
            fpath = os.path.join(FIG_DIR, fname) if fname else None
            if fpath and os.path.exists(fpath):
                img_count += 1
                rel_id = f'rIdImg{img_count}'
                image_rels.append((rel_id, fname))
                pw, ph = png_or_jpeg_dimensions(fpath)
                cx = TARGET_WIDTH_MM * EMU_PER_MM
                cy = int(cx * ph / pw)
                elements.append(make_image_paragraph(rel_id, img_count, cx, cy, fname))
            i += 1
            continue

        # Figure caption
        if re.match(r'Fig\. 16-\d+\.', s):
            elements.append(make_caption_paragraph(s, 'FigureCaption'))
            i += 1
            continue
        # Table caption (not a table row)
        if re.match(r'Table 16-\d+\.', s) and '|' not in s:
            elements.append(make_caption_paragraph(s, 'TableCaption'))
            i += 1
            continue

        # Pipe table
        if '|' in line and i + 1 < len(lines) and re.search(r'\|\s*-{2,}', lines[i + 1]):
            headers = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            elements.append(make_table(headers, rows))
            continue

        # Abstract / Keywords paragraph
        if s.startswith('**Keywords:**') or (elements and 'Abstract' in md_text[:0]):
            elements.append(make_paragraph(s, 'Normal'))
            i += 1
            continue

        if in_refs and re.match(r'^\[\d+\]', s):
            elements.append(make_paragraph(s, 'References'))
            i += 1
            continue

        elements.append(make_paragraph(s, 'Normal'))
        i += 1
    return '\n'.join(elements)


def build_word_rels(image_rels):
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rel_id, fname in image_rels:
        rels.append(f'  <Relationship Id="{rel_id}" '
                    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                    f'Target="media/{fname}"/>')
    rels.append('</Relationships>')
    return '\n'.join(rels)


def create_docx():
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        md = f.read()

    image_rels = []
    body = md_to_body(md, image_rels)

    # A5 page: 8391 x 11906 twips; margins per publisher guide (twips).
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{body}
    <w:sectPr>
      <w:pgSz w:w="8391" w:h="11906"/>
      <w:pgMar w:top="1417" w:right="1191" w:bottom="850" w:left="1191"
               w:header="850" w:footer="0" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    word_rels = build_word_rels(image_rels)
    with zipfile.ZipFile(DOCX_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
        for _, fname in image_rels:
            with open(os.path.join(FIG_DIR, fname), 'rb') as img:
                zf.writestr(f'word/media/{fname}', img.read())

    size_kb = os.path.getsize(DOCX_FILE) / 1024
    print(f"Created: {DOCX_FILE}")
    print(f"Embedded {len(image_rels)} JPEG figure(s): "
          f"{', '.join(fn for _, fn in image_rels)}")
    print(f"File size: {size_kb:.1f} KB")


if __name__ == '__main__':
    create_docx()
