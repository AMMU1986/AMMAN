#!/usr/bin/env python3
"""
Build a Word .docx for Chapter 4 (AI in Drug Discovery) from the markdown
source, embedding the four PNG figures inline. Pure Python standard library
(zipfile + raw OOXML), following the pattern used elsewhere in this repo.
"""

import zipfile
import os
import re
import struct

BASE = '/projects/sandbox/AMMAN'
MD_FILE = os.path.join(BASE, 'Chapter_4_AI_Drug_Discovery.md')
FIG_DIR = os.path.join(BASE, 'ch4_figures')
OUT = os.path.join(BASE, 'Chapter_4_AI_Drug_Discovery.docx')

EMU_PER_PX = 9525  # 96 dpi

# Map figure number -> (png filename, caption)
FIGURES = {
    1: ('Figure_1_Target_Identification.png',
        'Figure 1. Integrated AI workflow for target identification and validation, in which multi-omics and knowledge inputs are fused by machine learning models, ranked and assessed for tractability, and iteratively refined through experimental feedback.'),
    2: ('Figure_2_DTI_Architecture.png',
        'Figure 2. Representative dual-encoder deep learning architecture for drug-target interaction prediction, with independent drug and target encoders whose representations are fused before a prediction head estimates interaction and binding affinity.'),
    3: ('Figure_3_Generative_Design.png',
        'Figure 3. Closed-loop generative molecular design cycle integrating a generative model, a suite of property predictors, a scoring stage, and an optimisation strategy that iterate until the design objectives are satisfied.'),
    4: ('Figure_4_Drug_Repurposing.png',
        'Figure 4. Complementary computational strategies for drug repurposing, converging evidence from signature matching, network proximity, knowledge-graph link prediction, and real-world data onto candidate new indications for existing drugs.'),
}


def escape_xml(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    w, h = struct.unpack('>II', head[16:24])
    return w, h


def make_run(text, bold=False, italic=False):
    props = []
    if bold:
        props.append('<w:b/>')
    if italic:
        props.append('<w:i/>')
    rpr = '<w:rPr>' + ''.join(props) + '</w:rPr>' if props else ''
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'


def parse_inline(text):
    runs = []
    pattern = r'(\*\*.*?\*\*|\*[^*]+?\*)'
    for part in re.split(pattern, text):
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
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
    return f'<w:p>{ppr}{parse_inline(text)}</w:p>'


def make_image_paragraph(rid, w_px, h_px, name):
    # Scale to fit a max width of 600 px (page content width) preserving aspect
    max_w = 600
    if w_px > max_w:
        h_px = int(h_px * max_w / w_px)
        w_px = max_w
    cx = w_px * EMU_PER_PX
    cy = h_px * EMU_PER_PX
    drawing = f'''<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="200" w:after="60"/></w:pPr><w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
<wp:extent cx="{cx}" cy="{cy}"/>
<wp:docPr id="1" name="{name}"/>
<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:nvPicPr><pic:cNvPr id="0" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''
    return drawing


def make_table(headers, rows):
    n = len(headers)
    col_w = 9200 // n
    tbl = ['<w:tbl>',
           '<w:tblPr><w:tblStyle w:val="TableGrid"/>',
           '<w:tblW w:w="9200" w:type="dxa"/><w:tblLayout w:type="fixed"/>',
           '<w:tblBorders>',
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
           '</w:tblBorders></w:tblPr>']
    tbl.append('<w:tblGrid>' + f'<w:gridCol w:w="{col_w}"/>' * n + '</w:tblGrid>')
    # header row
    tbl.append('<w:tr>')
    for hdr in headers:
        tbl.append('<w:tc><w:tcPr>'
                   f'<w:tcW w:w="{col_w}" w:type="dxa"/>'
                   '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>'
                   f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="40"/></w:pPr>{make_run(hdr.strip(), bold=True)}</w:p></w:tc>')
    tbl.append('</w:tr>')
    for row in rows:
        tbl.append('<w:tr>')
        for i in range(n):
            cell = row[i].strip() if i < len(row) else ''
            tbl.append('<w:tc>'
                       f'<w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/></w:tcPr>'
                       f'<w:p><w:pPr><w:spacing w:after="40"/></w:pPr>{parse_inline(cell)}</w:p></w:tc>')
        tbl.append('</w:tr>')
    tbl.append('</w:tbl>')
    tbl.append('<w:p/>')  # spacer after table
    return ''.join(tbl)


def build_body(md_text, image_rels):
    """image_rels: dict fig_num -> rId"""
    elements = []
    lines = md_text.split('\n')
    i = 0
    in_references = False
    in_abstract = False
    figures_inserted = set()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue
        if stripped == '---':
            i += 1
            continue

        # Title
        if line.startswith('# ') and not line.startswith('## '):
            elements.append(make_paragraph(line[2:].strip(), 'Title'))
            i += 1
            continue

        # Heading 1
        if line.startswith('## '):
            htext = line[3:].strip()
            in_references = (htext == 'References')
            in_abstract = (htext == 'Abstract')
            elements.append(make_paragraph(htext, 'Heading1'))
            i += 1
            continue
        if line.startswith('### '):
            in_abstract = False
            elements.append(make_paragraph(line[4:].strip(), 'Heading2'))
            i += 1
            continue
        if line.startswith('#### '):
            elements.append(make_paragraph(line[5:].strip(), 'Heading3'))
            i += 1
            continue

        # Table
        if '|' in line and i + 1 < len(lines) and re.match(r'^\s*\|?[\s:\-|]+\|?\s*$', lines[i+1]) and '---' in lines[i+1]:
            headers = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            elements.append(make_table(headers, rows))
            continue

        # Table caption line (**Table N.** ...)
        m_tbl = re.match(r'^\*\*Table (\d+)\.\*\*\s*(.*)$', stripped)
        if m_tbl:
            elements.append(make_paragraph(stripped, 'TableCaption'))
            i += 1
            continue

        # Abstract body -> Abstract style
        if in_abstract:
            elements.append(make_paragraph(stripped, 'Abstract'))
            i += 1
            continue

        # References
        if in_references and re.match(r'^\[\d+\]', stripped):
            elements.append(make_paragraph(stripped, 'References'))
            i += 1
            continue

        # Normal paragraph: emit it, then if it references a figure not yet
        # inserted, place the image + caption right after (after 2nd mention
        # to keep flow near the discussion — but simplest: after first mention).
        elements.append(make_paragraph(stripped, 'Normal'))

        for fig_num in sorted(FIGURES.keys()):
            if fig_num in figures_inserted:
                continue
            if re.search(r'\*\*Figure %d\*\*' % fig_num, stripped) or re.search(r'\bFigure %d\b' % fig_num, stripped):
                fname, caption = FIGURES[fig_num]
                w, h = png_size(os.path.join(FIG_DIR, fname))
                rid = image_rels[fig_num]
                elements.append(make_image_paragraph(rid, w, h, fname))
                elements.append(make_paragraph(caption, 'FigureCaption'))
                figures_inserted.add(fig_num)
                break
        i += 1

    return '\n'.join(elements), figures_inserted


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
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Abstract"><w:name w:val="Abstract"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="720" w:right="720"/></w:pPr><w:rPr><w:i/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="References"><w:name w:val="References"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption"><w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="240"/></w:pPr><w:rPr><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption"><w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="120" w:after="60"/><w:jc w:val="left"/></w:pPr><w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
  <w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders>
    <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/></w:tblBorders></w:tblPr></w:style>
</w:styles>'''


def main():
    with open(MD_FILE, encoding='utf-8') as f:
        md = f.read()

    # Assign relationship IDs: rId1 styles, then rId2.. images
    image_rels = {}
    rid_counter = 2
    for fig_num in sorted(FIGURES.keys()):
        image_rels[fig_num] = f'rId{rid_counter}'
        rid_counter += 1

    body, inserted = build_body(md, image_rels)

    # document rels
    rel_entries = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for fig_num in sorted(FIGURES.keys()):
        fname = FIGURES[fig_num][0]
        rel_entries.append(f'<Relationship Id="{image_rels[fig_num]}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{fname}"/>')
    word_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 + ''.join(rel_entries) + '</Relationships>')

    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{body}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
        for fig_num in sorted(FIGURES.keys()):
            fname = FIGURES[fig_num][0]
            with open(os.path.join(FIG_DIR, fname), 'rb') as imgf:
                zf.writestr(f'word/media/{fname}', imgf.read())

    print(f"Created {OUT} ({os.path.getsize(OUT)/1024:.1f} KB)")
    print(f"Figures embedded: {sorted(inserted)}")


if __name__ == '__main__':
    main()
