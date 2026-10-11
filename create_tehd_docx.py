#!/usr/bin/env python3
"""
Convert Research_Article_TEHD_Journal_Bearing.md into a Word (.docx) document.

Pure Python standard library (zipfile only) - no python-docx required.
Produces:
  - real Word tables (with borders, bold header row)
  - embedded figures (the two validation PNGs)
  - readable equations (LaTeX converted to Unicode, numbered, centred)
  - heading / bold inline formatting
"""

import os
import re
import zipfile

SRC = '/projects/sandbox/AMMAN/Research_Article_TEHD_Journal_Bearing.md'
OUT = '/projects/sandbox/AMMAN/Research_Article_TEHD_Journal_Bearing.docx'
FIG_DIR = '/projects/sandbox/AMMAN/tehd_figures'
FIG1 = os.path.join(FIG_DIR, 'Fig1_pressure_validation.png')
FIG2 = os.path.join(FIG_DIR, 'Fig2_maxpressure_validation.png')

USABLE_TWIPS = 9360  # page width 12240 - margins 2*1440

# ----------------------------------------------------------------------------
# LaTeX -> Unicode (readable, lossless-enough for a Word draft)
# ----------------------------------------------------------------------------
GREEK = {
    r'\alpha': 'α', r'\beta': 'β', r'\gamma': 'γ', r'\delta': 'δ', r'\Delta': 'Δ',
    r'\varepsilon': 'ε', r'\epsilon': 'ε', r'\theta': 'θ', r'\Theta': 'Θ',
    r'\lambda': 'λ', r'\Lambda': 'Λ', r'\mu': 'μ', r'\nu': 'ν', r'\pi': 'π',
    r'\rho': 'ρ', r'\sigma': 'σ', r'\tau': 'τ', r'\phi': 'φ', r'\Phi': 'Φ',
    r'\omega': 'ω', r'\Omega': 'Ω', r'\eta': 'η',
}
OPS = {
    r'\partial': '∂', r'\nabla': '∇', r'\int': '∫', r'\infty': '∞',
    r'\ge': '≥', r'\geq': '≥', r'\le': '≤', r'\leq': '≤', r'\neq': '≠',
    r'\to': '→', r'\approx': '≈', r'\times': '×', r'\cdot': '·',
    r'\pm': '±', r'\sqrt': '√', r'\ln': 'ln', r'\exp': 'exp',
    r'\sin': 'sin', r'\cos': 'cos', r'\arctan': 'arctan', r'\begin{cases}': '',
    r'\end{cases}': '', r'\mathbf': '', r'\text': '', r'\left': '', r'\right': '',
    r'\quad': '   ', r'\qquad': '    ', r'\;': ' ', r'\,': ' ', r'\!': '',
    r'\big': '', r'\Big': '', r'\bigg': '', r'\Bigg': '',
}
SUP = str.maketrans('0123456789+-=()n', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ')
SUB = str.maketrans('0123456789+-=()aeioxcmrztbhsj',
                    '₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑᵢₒₓ꜀ₘᵣ_ₜᵦₕₛⱼ')


def _conv_fracs(s):
    # replace \frac{A}{B} -> (A)/(B), repeatedly for simple (non-nested) cases
    pat = re.compile(r'\\d?frac\{([^{}]*)\}\{([^{}]*)\}')
    prev = None
    while prev != s:
        prev = s
        s = pat.sub(r'(\1)/(\2)', s)
    return s


def _conv_scripts(s):
    # superscripts: ^{...} and ^x
    def sup_group(m):
        inner = m.group(1)
        try:
            return inner.translate(SUP)
        except Exception:
            return '^(' + inner + ')'
    s = re.sub(r'\^\{([^{}]*)\}', sup_group, s)
    s = re.sub(r'\^(\w)', lambda m: m.group(1).translate(SUP), s)

    def sub_group(m):
        inner = m.group(1)
        out = []
        for ch in inner:
            out.append(ch.translate(SUB) if ch.translate(SUB) != ch else '_' + ch)
        # if any char could not be subscripted cleanly, fall back
        if all(c.translate(SUB) != c or not c.isalnum() for c in inner):
            return inner.translate(SUB)
        return '_(' + inner + ')'
    s = re.sub(r'_\{([^{}]*)\}', sub_group, s)
    s = re.sub(r'_(\w)', lambda m: ('_' + m.group(1)), s)
    return s


def latex_to_text(s):
    s = s.replace(r'\\', ' | ')  # line breaks within an equation
    s = _conv_fracs(s)
    for k, v in GREEK.items():
        s = s.replace(k, v)
    for k, v in OPS.items():
        s = s.replace(k, v)
    s = _conv_scripts(s)
    s = s.replace('{', '').replace('}', '')
    s = re.sub(r'\\[a-zA-Z]+', '', s)   # drop any remaining commands
    s = s.replace('\\', '')
    s = re.sub(r'[ \t]+', ' ', s).strip()
    return s


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


# ----------------------------------------------------------------------------
# Inline run builder (handles **bold** and $inline math$)
# ----------------------------------------------------------------------------
def runs_from_inline(text):
    # Split on bold and inline-math tokens, preserving them
    tokens = re.split(r'(\*\*[^*]+\*\*|\$[^$]+\$)', text)
    xml = []
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith('**') and tok.endswith('**'):
            inner = esc(tok[2:-2])
            xml.append(f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{inner}</w:t></w:r>')
        elif tok.startswith('$') and tok.endswith('$'):
            inner = esc(latex_to_text(tok[1:-1]))
            xml.append(f'<w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">{inner}</w:t></w:r>')
        else:
            xml.append(f'<w:r><w:t xml:space="preserve">{esc(tok)}</w:t></w:r>')
    return ''.join(xml) or '<w:r><w:t></w:t></w:r>'


def para(text, style=None, align=None):
    ppr = '<w:pPr>'
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if align:
        ppr += f'<w:jc w:val="{align}"/>'
    ppr += '</w:pPr>'
    return f'<w:p>{ppr}{runs_from_inline(text)}</w:p>'


def heading(text, lvl):
    style = {1: 'Heading1', 2: 'Heading2', 3: 'Heading3'}[lvl]
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{runs_from_inline(text)}</w:p>'


def equation_para(latex, number):
    txt = esc(latex_to_text(latex))
    num = f'({number})' if number else ''
    # tab-separated: equation centred-ish, number right
    tabs = ('<w:pPr><w:tabs><w:tab w:val="center" w:pos="4680"/>'
            f'<w:tab w:val="right" w:pos="{USABLE_TWIPS}"/></w:tabs></w:pPr>')
    body = (f'<w:r><w:tab/><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">{txt}</w:t></w:r>'
            f'<w:r><w:tab/><w:t xml:space="preserve">{num}</w:t></w:r>')
    return f'<w:p>{tabs}{body}</w:p>'


def table_xml(rows):
    ncols = max(len(r) for r in rows)
    colw = USABLE_TWIPS // ncols
    grid = '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{colw}"/>' for _ in range(ncols)) + '</w:tblGrid>'
    borders = ('<w:tblBorders>'
               + ''.join(f'<w:{b} w:val="single" w:sz="4" w:space="0" w:color="444444"/>'
                         for b in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV'])
               + '</w:tblBorders>')
    tblpr = (f'<w:tblPr><w:tblW w:w="{USABLE_TWIPS}" w:type="dxa"/>{borders}'
             '<w:tblLook w:val="04A0"/></w:tblPr>')
    out = [f'<w:tbl>{tblpr}{grid}']
    for i, row in enumerate(rows):
        cells = []
        row = row + [''] * (ncols - len(row))
        for cell in row:
            shade = '<w:shd w:val="clear" w:fill="D9E2F3"/>' if i == 0 else ''
            rpr_b = '<w:b/>' if i == 0 else ''
            inner = runs_from_inline(cell)
            # force bold in header by wrapping; simplest: re-emit with bold rPr if header
            if i == 0:
                inner = (f'<w:r><w:rPr><w:b/></w:rPr>'
                         f'<w:t xml:space="preserve">{esc(strip_md(cell))}</w:t></w:r>')
            cells.append(f'<w:tc><w:tcPr><w:tcW w:w="{colw}" w:type="dxa"/>{shade}</w:tcPr>'
                         f'<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>{inner}</w:p></w:tc>')
        out.append('<w:tr>' + ''.join(cells) + '</w:tr>')
    out.append('</w:tbl><w:p/>')
    return ''.join(out)


def strip_md(t):
    t = re.sub(r'\*\*([^*]+)\*\*', r'\1', t)
    t = re.sub(r'\$([^$]+)\$', lambda m: latex_to_text(m.group(1)), t)
    return t


def image_para(rid, w_emu, h_emu, pid):
    return (f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
            f'<wp:extent cx="{w_emu}" cy="{h_emu}"/>'
            f'<wp:docPr id="{pid}" name="Picture{pid}"/>'
            f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:nvPicPr><pic:cNvPr id="{pid}" name="Picture{pid}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{w_emu}" cy="{h_emu}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            f'</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')


# ----------------------------------------------------------------------------
# Markdown parser -> body xml
# ----------------------------------------------------------------------------
def build_body(md):
    lines = md.split('\n')
    body = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip()

        # equation block
        if line.strip() == '$$':
            j = i + 1
            buf = []
            while j < n and lines[j].strip() != '$$':
                buf.append(lines[j])
                j += 1
            blob = ' '.join(x.strip() for x in buf)
            mnum = re.search(r'\\tag\{(\d+)\}', blob)
            number = mnum.group(1) if mnum else ''
            blob = re.sub(r'\\tag\{\d+\}', '', blob)
            body.append(equation_para(blob, number))
            i = j + 1
            continue

        # table block
        if line.startswith('|'):
            rows = []
            while i < n and lines[i].rstrip().startswith('|'):
                raw = lines[i].rstrip()
                if re.match(r'^\|[\s:\-|]+\|?\s*$', raw):
                    i += 1
                    continue
                cells = [c.strip() for c in raw.strip().strip('|').split('|')]
                rows.append(cells)
                i += 1
            if rows:
                body.append(table_xml(rows))
            continue

        if not line.strip():
            body.append('<w:p/>')
            i += 1
            continue

        if line.startswith('# ') and not line.startswith('## '):
            body.append(para(line[2:].strip(), style='Title', align='center'))
        elif line.startswith('## '):
            body.append(heading(line[3:].strip(), 1))
        elif line.startswith('### '):
            body.append(heading(line[4:].strip(), 2))
        elif line.startswith('#### '):
            body.append(heading(line[5:].strip(), 3))
        elif line.startswith('---'):
            body.append('<w:p/>')
        else:
            body.append(para(line))
            # Insert figures right after their caption line
            if line.startswith('**Figure 1.**'):
                body.append(image_para('rIdImg1', 5486400, 3657600, 101))
            elif line.startswith('**Figure 2.**'):
                body.append(image_para('rIdImg2', 5486400, 3657600, 102))
        i += 1

    return '\n'.join(body)


STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:rPr><w:b/><w:sz w:val="30"/><w:szCs w:val="30"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="300" w:after="120"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:rPr><w:b/><w:sz w:val="23"/><w:szCs w:val="23"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="220" w:after="100"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:rPr><w:b/><w:i/><w:sz w:val="22"/><w:szCs w:val="22"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="120" w:after="60"/></w:pPr>
  </w:style>
</w:styles>'''


def build_docx():
    with open(SRC, 'r') as f:
        md = f.read()
    body = build_body(md)

    content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '</Types>')

    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>')

    word_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        '<Relationship Id="rIdImg1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/>'
        '<Relationship Id="rIdImg2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image2.png"/>'
        '</Relationships>')

    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<w:body>{body}'
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
        '</w:body></w:document>')

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
        with open(FIG1, 'rb') as im:
            zf.writestr('word/media/image1.png', im.read())
        with open(FIG2, 'rb') as im:
            zf.writestr('word/media/image2.png', im.read())
    print(f'Created {OUT} ({os.path.getsize(OUT)/1024:.1f} KB)')


if __name__ == '__main__':
    build_docx()
