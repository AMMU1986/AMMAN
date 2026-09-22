#!/usr/bin/env python3
"""
Build a Word (.docx) document from the entropy-manuscript markdown, embedding
the 7 generated figures at their [[FIG:n]] markers and rendering the 6 markdown
tables as native Word tables.

Pure standard library only (zipfile + struct for PNG dimensions). No python-docx.
"""

import os
import re
import struct
import zipfile

BASE = '/projects/sandbox/AMMAN'
MD_PATH = f'{BASE}/Entropy_EMHD_Squeezing_Carreau_HNF.md'
OUT_PATH = f'{BASE}/Entropy_EMHD_Squeezing_Carreau_HNF.docx'
FIG_DIR = f'{BASE}/entropy_figures'

FIGURES = {
    '1': f'{FIG_DIR}/Figure_1_Schematic.png',
    '2': f'{FIG_DIR}/Figure_2_Velocity_Sq.png',
    '3': f'{FIG_DIR}/Figure_3_Velocity_We_M.png',
    '4': f'{FIG_DIR}/Figure_4_Temperature_Rd_Ec.png',
    '5': f'{FIG_DIR}/Figure_5_Entropy_Br_M.png',
    '6': f'{FIG_DIR}/Figure_6_Bejan_Rd_Br.png',
    '7': f'{FIG_DIR}/Figure_7_Engineering_phi.png',
}

EMU_PER_PX = 9525          # 1 px at 96 dpi
MAX_IMG_WIDTH_EMU = 5486400  # ~5.7 in usable page width


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError(f'Not a PNG: {path}')
    w, h = struct.unpack('>II', head[16:24])
    return w, h


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))


def strip_md(t):
    """Remove inline markdown emphasis / inline math markers for plain runs."""
    t = re.sub(r'\*\*([^*]+)\*\*', r'\1', t)
    t = re.sub(r'\*([^*]+)\*', r'\1', t)
    t = t.replace('$', '')
    return t


def clean_math(t):
    """Lightly de-LaTeX an equation body to a readable plain-text form."""
    t = t.strip()
    t = re.sub(r'\\tag\{([0-9]+)\}', r'', t)          # tag handled separately
    t = t.replace('\\left', '').replace('\\right', '')
    t = t.replace('\\Big', '').replace('\\bigg', '').replace('\\big', '')
    t = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'(\1)/(\2)', t)
    t = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', t)
    t = re.sub(r'\\text\{([^{}]*)\}', r'\1', t)
    t = re.sub(r'\\mathrm\{([^{}]*)\}', r'\1', t)
    t = re.sub(r'_\{([^{}]*)\}', r'_\1', t)
    t = re.sub(r'\^\{([^{}]*)\}', r'^(\1)', t)
    greek = {
        r'\\eta': 'eta', r'\\theta': 'theta', r'\\phi': 'phi', r'\\psi': 'psi',
        r'\\gamma': 'gamma', r'\\Gamma': 'Gamma', r'\\mu': 'mu', r'\\nu': 'nu',
        r'\\rho': 'rho', r'\\sigma': 'sigma', r'\\kappa': 'kappa',
        r'\\Omega': 'Omega', r'\\Lambda': 'Lambda', r'\\zeta': 'zeta',
        r'\\chi': 'chi', r'\\Xi': 'Xi', r'\\Phi': 'Phi', r'\\tau': 'tau',
        r'\\partial': 'd', r'\\infty': 'inf', r'\\times': 'x',
        r'\\int': 'INT', r'\\sum': 'SUM', r'\\to': '->', r'\\approx': '~=',
        r'\\le': '<=', r'\\ge': '>=', r'\\cdot': '.', r'\\,': ' ',
        r'\\;': ' ', r'\\!': '', r'\\quad': '   ', r'\\qquad': '     ',
        r'\\displaystyle': '', r'\\boldsymbol': '', r'\\mathbf': '',
    }
    for k, v in greek.items():
        t = re.sub(k, v, t)
    t = t.replace('{', '').replace('}', '').replace('\\', '')
    t = re.sub(r'\s+', ' ', t).strip()
    return t


# ------------------------------------------------------------------
# XML paragraph / run builders
# ------------------------------------------------------------------
def para(text, style=None, bold=False, italic=False, size=None, align=None):
    text = esc(text)
    rpr = ''
    props = ''
    if bold:
        props += '<w:b/>'
    if italic:
        props += '<w:i/>'
    if size:
        props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    if props:
        rpr = f'<w:rPr>{props}</w:rPr>'
    ppr = ''
    inner = ''
    if style:
        inner += f'<w:pStyle w:val="{style}"/>'
    if align:
        inner += f'<w:jc w:val="{align}"/>'
    if inner:
        ppr = f'<w:pPr>{inner}</w:pPr>'
    return (f'<w:p>{ppr}<w:r>{rpr}'
            f'<w:t xml:space="preserve">{text}</w:t></w:r></w:p>')


def empty_para():
    return '<w:p/>'


def eq_para(body, tag):
    """Monospace, centred equation with right-aligned number."""
    body_x = esc(body)
    tag_x = esc(f'({tag})') if tag else ''
    rpr = '<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:i/></w:rPr>'
    tabs = ('<w:tabs><w:tab w:val="right" w:pos="9360"/></w:tabs>')
    return (f'<w:p><w:pPr>{tabs}<w:jc w:val="left"/></w:pPr>'
            f'<w:r>{rpr}<w:t xml:space="preserve">      {body_x}</w:t></w:r>'
            f'<w:r><w:tab/><w:t xml:space="preserve">{tag_x}</w:t></w:r></w:p>')


def image_para(rid, w_emu, h_emu, name):
    return (
        '<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{w_emu}" cy="{h_emu}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{rid}" name="{name}"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'noChangeAspect="1"/></wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr><pic:cNvPr id="0" name="' + name + '"/>'
        '<pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="rId{rid}"/><a:stretch><a:fillRect/>'
        '</a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/>'
        f'<a:ext cx="{w_emu}" cy="{h_emu}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'
    )


def build_table(rows):
    """rows: list of list-of-cells; first row treated as header."""
    ncol = max(len(r) for r in rows)
    grid = ''.join(f'<w:gridCol w:w="{int(9360/ncol)}"/>' for _ in range(ncol))
    xml = ['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
           '<w:tblW w:w="0" w:type="auto"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '</w:tblBorders></w:tblPr>',
           f'<w:tblGrid>{grid}</w:tblGrid>']
    for ri, row in enumerate(rows):
        cells = list(row) + [''] * (ncol - len(row))
        xml.append('<w:tr>')
        for cell in cells:
            txt = esc(strip_md(cell.strip()))
            bold = '<w:b/>' if ri == 0 else ''
            shade = ('<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>'
                     if ri == 0 else '')
            xml.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{int(9360/ncol)}" w:type="dxa"/>'
                f'{shade}</w:tcPr>'
                f'<w:p><w:pPr><w:spacing w:after="20"/></w:pPr>'
                f'<w:r><w:rPr>{bold}<w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
                f'<w:t xml:space="preserve">{txt}</w:t></w:r></w:p></w:tc>')
        xml.append('</w:tr>')
    xml.append('</w:tbl>')
    return ''.join(xml)


# ------------------------------------------------------------------
# Markdown -> body XML
# ------------------------------------------------------------------
def convert(md, rel_map):
    lines = md.split('\n')
    body = []
    i = 0
    n = len(lines)
    in_eq = False
    eq_buf = []

    while i < n:
        line = lines[i].rstrip('\n')

        # fenced math block ($$ ... $$)
        if line.strip() == '$$':
            if not in_eq:
                in_eq = True
                eq_buf = []
            else:
                in_eq = False
                raw = ' '.join(eq_buf)
                m = re.search(r'\\tag\{([0-9]+)\}', raw)
                tag = m.group(1) if m else ''
                body.append(eq_para(clean_math(raw), tag))
            i += 1
            continue
        if in_eq:
            eq_buf.append(line)
            i += 1
            continue

        stripped = line.strip()

        # figure marker
        fm = re.match(r'^\*\*\[\[FIG:([0-9]+)\]\]\*\*$', stripped)
        if fm:
            fid = fm.group(1)
            rid = rel_map[fid]['rid']
            we, he = rel_map[fid]['emu']
            body.append(image_para(rid, we, he, f'Figure {fid}'))
            i += 1
            continue

        # table block
        if stripped.startswith('|') and '|' in stripped[1:]:
            tbl_lines = []
            while i < n and lines[i].strip().startswith('|'):
                tbl_lines.append(lines[i].strip())
                i += 1
            rows = []
            for tl in tbl_lines:
                if re.match(r'^\|[\s\-:|]+\|?$', tl):
                    continue
                cells = [c for c in tl.strip('|').split('|')]
                rows.append(cells)
            if rows:
                body.append(build_table(rows))
                body.append(empty_para())
            continue

        # blank line
        if stripped == '':
            body.append(empty_para())
            i += 1
            continue

        # headings
        if stripped.startswith('# ') and not stripped.startswith('## '):
            body.append(para(strip_md(stripped[2:]), style='Title',
                             bold=True, size=32, align='center'))
        elif stripped.startswith('## '):
            body.append(para(strip_md(stripped[3:]), style='Heading1',
                             bold=True, size=28))
        elif stripped.startswith('### '):
            body.append(para(strip_md(stripped[4:]), style='Heading2',
                             bold=True, size=24))
        elif stripped == '---':
            body.append(empty_para())
        # figure caption (italic *Figure ...*)
        elif stripped.startswith('*Figure') and stripped.endswith('*'):
            body.append(para(strip_md(stripped), italic=True, size=20,
                             align='center'))
        # bold table caption **Table ...**
        elif stripped.startswith('**') and stripped.endswith('**'):
            body.append(para(strip_md(stripped), bold=True, size=22))
        # reference lines [n] ...
        elif re.match(r'^\[[0-9]+\]', stripped):
            body.append(para(strip_md(stripped), size=20))
        else:
            body.append(para(strip_md(stripped)))
        i += 1

    return '\n'.join(body)


# ------------------------------------------------------------------
# Assemble docx
# ------------------------------------------------------------------
def main():
    with open(MD_PATH) as f:
        md = f.read()

    # Prepare relationship + media mapping for figures
    rel_map = {}
    rid = 100
    for fid, path in FIGURES.items():
        w, h = png_size(path)
        we = w * EMU_PER_PX
        he = h * EMU_PER_PX
        if we > MAX_IMG_WIDTH_EMU:
            scale = MAX_IMG_WIDTH_EMU / we
            we = int(we * scale)
            he = int(he * scale)
        rel_map[fid] = {'rid': rid, 'emu': (we, he),
                        'media': f'media/figure{fid}.png', 'path': path}
        rid += 1

    body = convert(md, rel_map)

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '</Types>')

    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>')

    doc_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for fid, info in rel_map.items():
        doc_rels.append(
            f'<Relationship Id="rId{info["rid"]}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            f'Target="{info["media"]}"/>')
    doc_rels.append('</Relationships>')
    doc_rels = ''.join(doc_rels)

    styles = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
        '<w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
        '<w:pPr><w:spacing w:after="120" w:line="300" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
        '<w:rPr><w:b/><w:sz w:val="32"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
        '<w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
        '<w:rPr><w:b/><w:sz w:val="28"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
        '<w:pPr><w:spacing w:before="320" w:after="120"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
        '<w:rPr><w:b/><w:sz w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
        '<w:pPr><w:spacing w:before="240" w:after="100"/></w:pPr></w:style>'
        '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/>'
        '<w:tblPr><w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '</w:tblBorders></w:tblPr></w:style>'
        '</w:styles>')

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<w:body>' + body +
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
        '</w:sectPr></w:body></w:document>')

    with zipfile.ZipFile(OUT_PATH, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('_rels/.rels', rels)
        z.writestr('word/_rels/document.xml.rels', doc_rels)
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', styles)
        for fid, info in rel_map.items():
            with open(info['path'], 'rb') as im:
                z.writestr('word/' + info['media'], im.read())

    print(f"  Created {OUT_PATH}")


if __name__ == '__main__':
    main()
