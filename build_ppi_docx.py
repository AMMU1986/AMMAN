#!/usr/bin/env python3
"""
Build a Word (.docx) file from PPI_Deprescribing_Manuscript.md.

Pure standard library (zipfile/struct). Features:
  - Title / heading levels
  - Justified body paragraphs with inline bold (**...**) and italics (*...*)
  - Real Word tables (shaded header, borders) from Markdown pipe tables
  - Embedded PNG figures with captions from [[FIGURE:file|caption]] markers
"""

import os
import re
import struct
import zipfile

BASE = '/projects/sandbox/AMMAN'
MD = os.path.join(BASE, 'PPI_Deprescribing_Manuscript.md')
FIGDIR = os.path.join(BASE, 'ppi_figures')
OUT = os.path.join(BASE, 'PPI_Deprescribing_Manuscript.docx')

EMU_PER_INCH = 914400
MAX_IMG_WIDTH_IN = 6.3


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))


def png_size(path):
    with open(path, 'rb') as f:
        f.read(16)
        w, h = struct.unpack('>II', f.read(8))
    return w, h


# ---------------------------------------------------------------- inline runs
def inline_runs(text):
    """Convert **bold** / *italic* markup to a sequence of Word runs."""
    runs = []
    # tokenise on ** and *
    pattern = re.compile(r'(\*\*.+?\*\*|\*.+?\*)')
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            runs.append((text[pos:m.start()], False, False))
        tok = m.group(0)
        if tok.startswith('**'):
            runs.append((tok[2:-2], True, False))
        else:
            runs.append((tok[1:-1], False, True))
        pos = m.end()
    if pos < len(text):
        runs.append((text[pos:], False, False))
    if not runs:
        runs.append((text, False, False))
    xml = ''
    for txt, b, i in runs:
        rpr = ''
        if b or i:
            rpr = '<w:rPr>' + ('<w:b/>' if b else '') + ('<w:i/>' if i else '') + '</w:rPr>'
        xml += f'<w:r>{rpr}<w:t xml:space="preserve">{esc(txt)}</w:t></w:r>'
    return xml


def para(text, style=None, align='both', bold=False, size=None,
         spacing_after=120, keep=False):
    ppr = '<w:pPr>'
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if keep:
        ppr += '<w:keepNext/>'
    ppr += f'<w:spacing w:after="{spacing_after}" w:line="276" w:lineRule="auto"/>'
    if align:
        ppr += f'<w:jc w:val="{align}"/>'
    ppr += '</w:pPr>'
    if bold or size:
        rpr = '<w:rPr>'
        if bold:
            rpr += '<w:b/>'
        if size:
            rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        rpr += '</w:rPr>'
        run = f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'
    else:
        run = inline_runs(text)
    return f'<w:p>{ppr}{run}</w:p>'


def empty_para():
    return '<w:p/>'


# ---------------------------------------------------------------- tables
def build_table(rows):
    """rows: list of list-of-cell-strings; first row is header."""
    ncol = max(len(r) for r in rows)
    borders = ('<w:tblBorders>'
               '<w:top w:val="single" w:sz="4" w:color="666666"/>'
               '<w:left w:val="single" w:sz="4" w:color="666666"/>'
               '<w:bottom w:val="single" w:sz="4" w:color="666666"/>'
               '<w:right w:val="single" w:sz="4" w:color="666666"/>'
               '<w:insideH w:val="single" w:sz="4" w:color="999999"/>'
               '<w:insideV w:val="single" w:sz="4" w:color="999999"/>'
               '</w:tblBorders>')
    tblpr = ('<w:tblPr>'
             '<w:tblW w:w="5000" w:type="pct"/>'
             '<w:tblLayout w:type="autofit"/>'
             + borders +
             '<w:tblCellMar>'
             '<w:top w:w="40" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
             '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="80" w:type="dxa"/>'
             '</w:tblCellMar>'
             '</w:tblPr>')
    grid = '<w:tblGrid>' + ''.join('<w:gridCol/>' for _ in range(ncol)) + '</w:tblGrid>'

    body = ''
    for ri, row in enumerate(rows):
        is_header = (ri == 0)
        cells = list(row) + [''] * (ncol - len(row))
        row_xml = ''
        for cell in cells:
            shade = ('<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>'
                     if is_header else '')
            tcpr = f'<w:tcPr><w:tcW w:w="0" w:type="auto"/>{shade}<w:vAlign w:val="center"/></w:tcPr>'
            rpr = '<w:rPr><w:b/><w:sz w:val="20"/></w:rPr>' if is_header else '<w:rPr><w:sz w:val="20"/></w:rPr>'
            ptext = cell.strip()
            cell_p = (f'<w:p><w:pPr><w:spacing w:after="20"/>'
                      f'<w:jc w:val="{"center" if is_header else "left"}"/></w:pPr>'
                      f'<w:r>{rpr}<w:t xml:space="preserve">{esc(ptext)}</w:t></w:r></w:p>')
            row_xml += f'<w:tc>{tcpr}{cell_p}</w:tc>'
        hdr = '<w:trPr><w:tblHeader/></w:trPr>' if is_header else ''
        body += f'<w:tr>{hdr}{row_xml}</w:tr>'
    return f'<w:tbl>{tblpr}{grid}{body}</w:tbl>'


# ---------------------------------------------------------------- images
class ImageManager:
    def __init__(self):
        self.items = []  # (rid, media_name, path, w, h)
        self._n = 0

    def add(self, path):
        self._n += 1
        rid = f'rIdImg{self._n}'
        media = f'image{self._n}.png'
        w, h = png_size(path)
        self.items.append((rid, media, path, w, h))
        return rid, w, h


def image_paragraph(rid, px_w, px_h, docpr_id):
    # scale to max width
    width_in = min(MAX_IMG_WIDTH_IN, px_w / 96.0)
    height_in = width_in * px_h / px_w
    cx = int(width_in * EMU_PER_INCH)
    cy = int(height_in * EMU_PER_INCH)
    drawing = f'''<w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
<wp:extent cx="{cx}" cy="{cy}"/>
<wp:docPr id="{docpr_id}" name="Figure{docpr_id}"/>
<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:nvPicPr><pic:cNvPr id="{docpr_id}" name="Figure{docpr_id}"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed="{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>'''
    return f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/><w:keepNext/></w:pPr>{drawing}</w:p>'


# ---------------------------------------------------------------- parser
def parse_markdown(md, images):
    out = []
    lines = md.split('\n')
    i = 0
    docpr = 100
    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            i += 1
            continue

        # figure marker
        fm = re.match(r'\[\[FIGURE:([^|]+)\|(.+)\]\]$', line.strip())
        if fm:
            fname = fm.group(1).strip()
            caption = fm.group(2).strip()
            path = os.path.join(FIGDIR, fname)
            rid, w, h = images.add(path)
            docpr += 1
            out.append(image_paragraph(rid, w, h, docpr))
            out.append(f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="200"/></w:pPr>{inline_runs(caption)}</w:p>')
            i += 1
            continue

        # table block
        if line.strip().startswith('|'):
            tbl_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                tbl_lines.append(lines[i].strip())
                i += 1
            rows = []
            for tl in tbl_lines:
                if re.match(r'^\|[\s\-:|]+\|$', tl):
                    continue
                cells = [c.strip() for c in tl.strip('|').split('|')]
                rows.append(cells)
            if rows:
                out.append(build_table(rows))
                out.append('<w:p><w:pPr><w:spacing w:after="160"/></w:pPr></w:p>')
            continue

        # headings
        if line.startswith('# ') and not line.startswith('## '):
            out.append(para(line[2:].strip(), style='Title', align='center'))
        elif line.startswith('#### '):
            out.append(para(line[5:].strip(), style='Heading3', align='left'))
        elif line.startswith('### '):
            out.append(para(line[4:].strip(), style='Heading2', align='left'))
        elif line.startswith('## '):
            out.append(para(line[3:].strip(), style='Heading1', align='left'))
        elif line.strip() == '---':
            pass
        # numbered list
        elif re.match(r'^\d+\.\s', line):
            txt = re.sub(r'^\d+\.\s', '', line)
            num = re.match(r'^(\d+)\.', line).group(1)
            out.append(para(f'{num}. {txt}', align='both', spacing_after=60))
        # bulleted list
        elif line.startswith('- ') or line.startswith('* '):
            out.append(para('\u2022 ' + line[2:], align='both', spacing_after=60))
        else:
            out.append(para(line, align='both'))
        i += 1
    return '\n'.join(out)


# ---------------------------------------------------------------- docx assembly
STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>
<w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
<w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>
<w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
<w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>
<w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:color w:val="1F3864"/></w:rPr>
<w:pPr><w:spacing w:before="320" w:after="120"/><w:keepNext/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>
<w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="2E5496"/></w:rPr>
<w:pPr><w:spacing w:before="240" w:after="100"/><w:keepNext/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/>
<w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
<w:pPr><w:spacing w:before="160" w:after="80"/><w:keepNext/></w:pPr></w:style>
</w:styles>'''


def build_docx():
    md = open(MD).read()
    images = ImageManager()
    body = parse_markdown(md, images)

    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<w:body>
{body}
<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>
</w:body></w:document>'''

    # content types
    ct = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
          '<Default Extension="xml" ContentType="application/xml"/>',
          '<Default Extension="png" ContentType="image/png"/>',
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>',
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>',
          '</Types>']
    content_types = '\n'.join(ct)

    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '</Relationships>')

    word_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rid, media, path, w, h in images.items:
        word_rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{media}"/>')
    word_rels.append('</Relationships>')
    word_rels = '\n'.join(word_rels)

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
        for rid, media, path, w, h in images.items:
            with open(path, 'rb') as f:
                zf.writestr(f'word/media/{media}', f.read())

    print(f"Created {OUT}")
    print(f"Embedded {len(images.items)} figures")


if __name__ == '__main__':
    build_docx()
