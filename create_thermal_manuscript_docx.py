#!/usr/bin/env python3
"""
Create a Word document (.docx) from the thermal-modelling manuscript markdown file.

Converts Manuscript_Thermal_Modelling_ToolChip_Temperature.md into a formatted
.docx using only the Python standard library (no external dependencies).

Supports: title (#), section headings (##), subsection headings (###),
markdown tables (rendered as real Word tables), bold/italic inline markers,
and normal justified body paragraphs in Times New Roman.
"""

import zipfile
import re
import os
import struct

SRC_MD = '/projects/sandbox/AMMAN/Manuscript_Thermal_Modelling_ToolChip_Temperature.md'
OUT_DOCX = '/projects/sandbox/AMMAN/Manuscript_Thermal_Modelling_ToolChip_Temperature.docx'
FIG_DIR = '/projects/sandbox/AMMAN/thermal_figures'

# Map manuscript figure number -> PNG file in FIG_DIR
FIGURE_FILES = {
    1: 'Figure_1_Setup.png',
    2: 'Figure_2_Discretization.png',
    3: 'Figure_3_InteriorNode.png',
    4: 'Figure_4_ShearZoneTemp.png',
    5: 'Figure_5_RakeFaceTemp.png',
    6: 'Figure_6_HeatPartition.png',
    7: 'Figure_7_MWF_Temps.png',
}

EMU_PER_PX = 9525          # at 96 dpi
MAX_WIDTH_EMU = 5760720    # ~6.3 inches (fits inside 1-inch margins on Letter)

# Collected during body conversion, consumed when packaging the docx
_images = []  # list of dicts: {num, path, rid, media_name, w_emu, h_emu}


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    # IHDR width/height are big-endian uint32 at bytes 16..24
    w, h = struct.unpack('>II', head[16:24])
    return w, h


def image_paragraph(num):
    """Build an inline-image paragraph (centered) for figure `num`."""
    fname = FIGURE_FILES.get(num)
    if not fname:
        return ''
    path = os.path.join(FIG_DIR, fname)
    if not os.path.exists(path):
        return ''
    w_px, h_px = png_size(path)
    w_emu = w_px * EMU_PER_PX
    h_emu = h_px * EMU_PER_PX
    if w_emu > MAX_WIDTH_EMU:
        scale = MAX_WIDTH_EMU / w_emu
        w_emu = int(w_emu * scale)
        h_emu = int(h_emu * scale)
    idx = len(_images) + 1
    rid = f'rIdImg{idx}'
    media_name = f'image{idx}.png'
    _images.append({'path': path, 'rid': rid, 'media_name': media_name})
    docpr_id = 1000 + idx
    return (
        '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/></w:pPr>'
        '<w:r><w:drawing>'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        f'<wp:extent cx="{w_emu}" cy="{h_emu}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{docpr_id}" name="Figure{num}"/>'
        '<wp:cNvGraphicFramePr>'
        '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr>'
        f'<pic:cNvPr id="{docpr_id}" name="Figure{num}"/>'
        '<pic:cNvPicPr/>'
        '</pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rid}"/>'
        '<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr>'
        f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{w_emu}" cy="{h_emu}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        '</pic:spPr>'
        '</pic:pic>'
        '</a:graphicData></a:graphic>'
        '</wp:inline>'
        '</w:drawing></w:r></w:p>'
    )


def escape_xml(text):
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))


def strip_inline_md(text):
    """Remove markdown emphasis markers, keeping the text."""
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    return text


def para(text, style='Normal', bold=False, size=None):
    """Build a Word paragraph XML string."""
    text = escape_xml(strip_inline_md(text))

    run_props = []
    if bold:
        run_props.append('<w:b/>')
    if size is not None:
        run_props.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    rpr = f'<w:rPr>{"".join(run_props)}</w:rPr>' if run_props else ''

    style_map = {
        'Title': '<w:pPr><w:pStyle w:val="Title"/><w:jc w:val="center"/></w:pPr>',
        'Heading1': '<w:pPr><w:pStyle w:val="Heading1"/></w:pPr>',
        'Heading2': '<w:pPr><w:pStyle w:val="Heading2"/></w:pPr>',
        'Heading3': '<w:pPr><w:pStyle w:val="Heading3"/></w:pPr>',
    }
    ppr = style_map.get(style, '')
    return (f'<w:p>{ppr}<w:r>{rpr}'
            f'<w:t xml:space="preserve">{text}</w:t></w:r></w:p>')


def table_cell(text, bold=False):
    text = escape_xml(strip_inline_md(text))
    rpr = '<w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>' if bold \
        else '<w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
    return ('<w:tc><w:tcPr><w:tcBorders>'
            '<w:top w:val="single" w:sz="4" w:color="808080"/>'
            '<w:left w:val="single" w:sz="4" w:color="808080"/>'
            '<w:bottom w:val="single" w:sz="4" w:color="808080"/>'
            '<w:right w:val="single" w:sz="4" w:color="808080"/>'
            '</w:tcBorders></w:tcPr>'
            f'<w:p><w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r></w:p></w:tc>')


def build_table(rows):
    """rows: list of lists of cell strings. First row treated as header."""
    out = ['<w:tbl><w:tblPr>'
           '<w:tblStyle w:val="TableGrid"/>'
           '<w:tblW w:w="0" w:type="auto"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:color="808080"/>'
           '<w:left w:val="single" w:sz="4" w:color="808080"/>'
           '<w:bottom w:val="single" w:sz="4" w:color="808080"/>'
           '<w:right w:val="single" w:sz="4" w:color="808080"/>'
           '<w:insideH w:val="single" w:sz="4" w:color="808080"/>'
           '<w:insideV w:val="single" w:sz="4" w:color="808080"/>'
           '</w:tblBorders></w:tblPr>']
    for i, row in enumerate(rows):
        out.append('<w:tr>')
        for cell in row:
            out.append(table_cell(cell, bold=(i == 0)))
        out.append('</w:tr>')
    out.append('</w:tbl>')
    out.append('<w:p/>')  # spacer after table
    return ''.join(out)


def parse_table_line(line):
    parts = [p.strip() for p in line.strip().strip('|').split('|')]
    return parts


def markdown_to_body(md_text):
    paragraphs = []
    lines = md_text.split('\n')
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip()

        # Table block
        if line.strip().startswith('|') and '|' in line.strip()[1:]:
            table_rows = []
            while i < n and lines[i].strip().startswith('|'):
                l = lines[i].strip()
                if re.match(r'^\|[\s\-:|]+\|?$', l):  # separator row
                    i += 1
                    continue
                table_rows.append(parse_table_line(l))
                i += 1
            if table_rows:
                paragraphs.append(build_table(table_rows))
            continue

        if not line:
            paragraphs.append('<w:p/>')
            i += 1
            continue

        # Figure placeholder, e.g. "**[Figure 4 near here.]**" or "[Figure 4 near here.]"
        fig_match = re.search(r'\[figure\s+(\d+)\s+near here', line, re.IGNORECASE)
        if fig_match:
            num = int(fig_match.group(1))
            img_xml = image_paragraph(num)
            if img_xml:
                paragraphs.append(img_xml)
            else:
                paragraphs.append(para(line.strip().strip('*').strip(), bold=True))
            i += 1
            continue

        if line.startswith('# ') and not line.startswith('## '):
            paragraphs.append(para(line[2:].strip(), style='Title', bold=True, size=32))
        elif line.startswith('## '):
            paragraphs.append(para(line[3:].strip(), style='Heading1', bold=True, size=28))
        elif line.startswith('### '):
            paragraphs.append(para(line[4:].strip(), style='Heading2', bold=True, size=24))
        elif line.startswith('#### '):
            paragraphs.append(para(line[5:].strip(), style='Heading3', bold=True, size=22))
        elif line.startswith('---'):
            paragraphs.append('<w:p/>')
        elif line.strip().startswith('**') and line.strip().endswith('**') and line.count('**') == 2:
            paragraphs.append(para(line.strip().strip('*').strip(), bold=True))
        elif line.strip().startswith(('- ', '* ')):
            paragraphs.append(para('\u2022  ' + line.strip()[2:], size=24))
        elif re.match(r'^\d+\.\s', line.strip()):
            paragraphs.append(para(line.strip(), size=24))
        else:
            paragraphs.append(para(line))
        i += 1

    return '\n'.join(paragraphs)


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


def build_word_rels():
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for img in _images:
        rels.append(
            f'<Relationship Id="{img["rid"]}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            f'Target="media/{img["media_name"]}"/>')
    rels.append('</Relationships>')
    return ''.join(rels)

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="360" w:after="120"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:rPr><w:b/><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="120" w:after="60"/></w:pPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
  </w:style>
</w:styles>'''


def create_docx():
    with open(SRC_MD, 'r', encoding='utf-8') as f:
        md_text = f.read()

    body = markdown_to_body(md_text)

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<w:body>'
        f'{body}'
        '<w:sectPr>'
        '<w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
        '</w:sectPr>'
        '</w:body></w:document>'
    )

    with zipfile.ZipFile(OUT_DOCX, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', build_word_rels())
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
        for img in _images:
            with open(img['path'], 'rb') as f:
                zf.writestr(f'word/media/{img["media_name"]}', f.read())

    print(f'Created {OUT_DOCX} with {len(_images)} embedded figures')


if __name__ == '__main__':
    create_docx()
