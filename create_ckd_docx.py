#!/usr/bin/env python3
"""
Convert CKD_Hybrid_ML_DL_Manuscript.md to a Word .docx file.
Pure Python standard library (zipfile only) - no external dependencies.

Features:
  - Title / Heading1 / Heading2 styles
  - Inline **bold**, *italic*, `code`
  - Real Word tables with borders
  - Block ($$...$$) and inline ($...$) math rendered to readable Unicode
  - Blockquote notes
"""

import zipfile
import re

SRC = '/projects/sandbox/AMMAN/CKD_Hybrid_ML_DL_Manuscript.md'
OUT = '/projects/sandbox/AMMAN/CKD_Hybrid_ML_DL_Manuscript.docx'

# ----------------------------------------------------------------------
# Light LaTeX -> Unicode conversion so equations are human-readable in Word
# ----------------------------------------------------------------------
LATEX_MAP = [
    (r'\\times', '×'), (r'\\cdot', '·'), (r'\\le', '≤'), (r'\\ge', '≥'),
    (r'\\neq', '≠'), (r'\\approx', '≈'), (r'\\pm', '±'), (r'\\infty', '∞'),
    (r'\\sum', '∑'), (r'\\prod', '∏'), (r'\\int', '∫'), (r'\\partial', '∂'),
    (r'\\nabla', '∇'), (r'\\in', '∈'), (r'\\notin', '∉'), (r'\\forall', '∀'),
    (r'\\exists', '∃'), (r'\\lor', '∨'), (r'\\land', '∧'), (r'\\odot', '⊙'),
    (r'\\rightarrow', '→'), (r'\\to', '→'), (r'\\leftarrow', '←'), (r'\\uparrow', '↑'),
    (r'\\alpha', 'α'), (r'\\beta', 'β'), (r'\\gamma', 'γ'), (r'\\delta', 'δ'),
    (r'\\epsilon', 'ε'), (r'\\zeta', 'ζ'), (r'\\eta', 'η'), (r'\\theta', 'θ'),
    (r'\\kappa', 'κ'), (r'\\lambda', 'λ'), (r'\\mu', 'μ'), (r'\\nu', 'ν'),
    (r'\\xi', 'ξ'), (r'\\pi', 'π'), (r'\\rho', 'ρ'), (r'\\sigma', 'σ'),
    (r'\\tau', 'τ'), (r'\\phi', 'φ'), (r'\\varphi', 'φ'), (r'\\chi', 'χ'),
    (r'\\psi', 'ψ'), (r'\\omega', 'ω'), (r'\\Omega', 'Ω'), (r'\\Theta', 'Θ'),
    (r'\\Delta', 'Δ'), (r'\\Phi', 'Φ'), (r'\\Pi', 'Π'), (r'\\Sigma', 'Σ'),
    (r'\\mathbb\{1\}', '𝟙'), (r'\\min', 'min'), (r'\\max', 'max'),
    (r'\\exp', 'exp'), (r'\\log', 'log'), (r'\\tanh', 'tanh'), (r'\\arg', 'arg'),
    (r'\\sigma', 'σ'), (r'\\prime', '′'), (r'\\top', 'ᵀ'),
]

SUP = str.maketrans('0123456789+-=()n', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ')
SUB = str.maketrans('0123456789+-=()aeioxhklmnpst', '₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑᵢₒₓₕₖₗₘₙₚₛₜ')


def _supersub(s):
    # ^{...} and _{...}
    def rep_sup(m):
        inner = m.group(1)
        try:
            return inner.translate(SUP)
        except Exception:
            return '^(' + inner + ')'
    def rep_sub(m):
        inner = m.group(1)
        return inner.translate(SUB) if all(c in '0123456789+-=()aeioxhklmnpst' for c in inner) else '_' + inner
    s = re.sub(r'\^\{([^{}]*)\}', rep_sup, s)
    s = re.sub(r'_\{([^{}]*)\}', rep_sub, s)
    s = re.sub(r'\^([A-Za-z0-9])', lambda m: m.group(1).translate(SUP), s)
    s = re.sub(r'_([A-Za-z0-9])', lambda m: m.group(1).translate(SUB), s)
    return s


def latex_to_unicode(s):
    s = s.replace('\\\\', ' ; ')
    s = re.sub(r'\\(?:frac|dfrac)\{([^{}]*)\}\{([^{}]*)\}', r'(\1)/(\2)', s)
    s = re.sub(r'\\(?:text|mathrm|mathbf|mathcal|operatorname|boldsymbol)\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\(?:left|right|big|Big|,|;|!|quad|qquad)', ' ', s)
    s = re.sub(r'\\min\\!?', 'min', s)
    for pat, rep in LATEX_MAP:
        s = re.sub(pat, rep, s)
    s = _supersub(s)
    s = s.replace('{', '').replace('}', '')
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def escape_xml(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


import os
EMU_PER_PX = 9525          # at 96 DPI
MAX_WIDTH_EMU = 5486400    # 6.0 inches content width

# collected images: list of dicts {rid, target, abspath, w_emu, h_emu, cap}
MEDIA = []


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(26)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        return (800, 600)
    import struct as _s
    w, h = _s.unpack('>II', head[16:24])
    return (w, h)


def image_block(path, caption):
    """Return docx XML for a centered inline image + caption, registering media."""
    abspath = path if os.path.isabs(path) else os.path.join(
        '/projects/sandbox/AMMAN', path)
    if not os.path.exists(abspath):
        return para(f'[missing image: {path}]', jc='center')
    w_px, h_px = png_size(abspath)
    w_emu = w_px * EMU_PER_PX
    h_emu = h_px * EMU_PER_PX
    if w_emu > MAX_WIDTH_EMU:
        scale = MAX_WIDTH_EMU / w_emu
        w_emu = int(w_emu * scale)
        h_emu = int(h_emu * scale)
    idx = len(MEDIA) + 1
    rid = f'rIdImg{idx}'
    target = f'media/image{idx}.png'
    MEDIA.append({'rid': rid, 'target': target, 'abspath': abspath})
    docpr_id = 1000 + idx
    drawing = (
        '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="40"/></w:pPr>'
        '<w:r><w:drawing>'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        f'<wp:extent cx="{w_emu}" cy="{h_emu}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{docpr_id}" name="Figure{idx}"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr>'
        f'<pic:cNvPr id="{docpr_id}" name="Figure{idx}"/>'
        '<pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rid}" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
        '<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/>'
        f'<a:ext cx="{w_emu}" cy="{h_emu}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline>'
        '</w:drawing></w:r></w:p>'
    )
    cap = ''
    if caption:
        runs = ''.join(run_xml(t, b, i, m, 18)
                       for (t, b, i, m) in inline_runs(caption))
        cap = (f'<w:p><w:pPr><w:jc w:val="center"/>'
               '<w:spacing w:after="160"/></w:pPr>'
               f'{runs}</w:p>')
    return drawing + cap


# ----------------------------------------------------------------------
# Inline run parsing: **bold**, *italic*, `code`, $math$
# ----------------------------------------------------------------------
def inline_runs(text):
    """Return list of (text, bold, italic, mono) runs."""
    runs = []
    i = 0
    n = len(text)
    while i < n:
        if text.startswith('**', i):
            j = text.find('**', i + 2)
            if j != -1:
                runs.append((text[i+2:j], True, False, False)); i = j + 2; continue
        if text[i] == '`':
            j = text.find('`', i + 1)
            if j != -1:
                runs.append((text[i+1:j], False, False, True)); i = j + 1; continue
        if text[i] == '$':
            j = text.find('$', i + 1)
            if j != -1:
                runs.append((latex_to_unicode(text[i+1:j]), False, True, False)); i = j + 1; continue
        if text[i] == '*':
            j = text.find('*', i + 1)
            if j != -1 and j > i + 1:
                runs.append((text[i+1:j], False, True, False)); i = j + 1; continue
        # plain char: accumulate until next marker
        m = re.search(r'(\*\*|`|\$|\*)', text[i:])
        if m:
            runs.append((text[i:i+m.start()], False, False, False)); i += m.start()
        else:
            runs.append((text[i:], False, False, False)); i = n
    return [r for r in runs if r[0] != '']


def run_xml(text, bold=False, italic=False, mono=False, size=None):
    text = escape_xml(text)
    props = []
    if bold: props.append('<w:b/>')
    if italic: props.append('<w:i/>')
    if mono: props.append('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>')
    if size: props.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    rpr = f'<w:rPr>{"".join(props)}</w:rPr>' if props else ''
    return f'<w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r>'


def para(text='', style='Normal', jc=None, size=None):
    ppr_items = []
    if style != 'Normal':
        ppr_items.append(f'<w:pStyle w:val="{style}"/>')
    if jc:
        ppr_items.append(f'<w:jc w:val="{jc}"/>')
    ppr = f'<w:pPr>{"".join(ppr_items)}</w:pPr>' if ppr_items else ''
    if text == '':
        return f'<w:p>{ppr}</w:p>'
    runs = ''.join(run_xml(t, b, i, m, size) for (t, b, i, m) in inline_runs(text))
    return f'<w:p>{ppr}{runs}</w:p>'


def mono_para(text, jc='center', size=20):
    return (f'<w:p><w:pPr><w:jc w:val="{jc}"/></w:pPr>'
            f'{run_xml(text, mono=True, size=size)}</w:p>')


def bullet_para(text, size=None):
    runs = ''.join(run_xml(t, b, i, m, size) for (t, b, i, m) in inline_runs(text))
    return ('<w:p><w:pPr><w:ind w:left="360" w:hanging="360"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">•  </w:t></w:r>{runs}</w:p>')


# ----------------------------------------------------------------------
# Table building
# ----------------------------------------------------------------------
def build_table(rows):
    """rows = list of list of cell strings; first row is header."""
    borders = ('<w:tblBorders>'
               + ''.join(f'<w:{b} w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
                         for b in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
               + '</w:tblBorders>')
    tblpr = (f'<w:tblPr><w:tblW w:w="5000" w:type="pct"/>{borders}'
             '<w:tblLayout w:type="autofit"/></w:tblPr>')
    xml = [f'<w:tbl>{tblpr}']
    for ri, row in enumerate(rows):
        xml.append('<w:tr>')
        for cell in row:
            shade = '<w:shd w:val="clear" w:fill="D9E2F3"/>' if ri == 0 else ''
            runs = ''.join(run_xml(t, (b or ri == 0), i, m, 18)
                           for (t, b, i, m) in inline_runs(cell))
            if not runs:
                runs = run_xml('', size=18)
            xml.append(f'<w:tc><w:tcPr><w:tcW w:w="0" w:type="auto"/>{shade}</w:tcPr>'
                       f'<w:p>{runs}</w:p></w:tc>')
        xml.append('</w:tr>')
    xml.append('</w:tbl><w:p/>')
    return ''.join(xml)


def split_table_row(line):
    line = line.strip()
    if line.startswith('|'): line = line[1:]
    if line.endswith('|'): line = line[:-1]
    return [c.strip() for c in line.split('|')]


# ----------------------------------------------------------------------
# Main markdown walk
# ----------------------------------------------------------------------
def convert(md):
    out = []
    lines = md.split('\n')
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip()

        # Image:  ![caption](path)
        img = re.match(r'^!\[(.*?)\]\((.*?)\)\s*$', line.strip())
        if img:
            caption, path = img.group(1), img.group(2)
            out.append(image_block(path, caption))
            i += 1
            continue

        # Block equation $$ ... $$
        if line.strip().startswith('$$'):
            buf = []
            content = line.strip()[2:]
            if content.endswith('$$') and len(content) > 2:
                buf.append(content[:-2])
                i += 1
            else:
                if content: buf.append(content)
                i += 1
                while i < n and not lines[i].strip().endswith('$$'):
                    buf.append(lines[i]); i += 1
                if i < n:
                    tail = lines[i].strip()[:-2]
                    if tail: buf.append(tail)
                    i += 1
            raw = ' '.join(x.strip() for x in buf if x.strip())
            # split aligned eqns on \\ -> separate lines
            for piece in latex_to_unicode(raw).split(' ; '):
                if piece.strip():
                    out.append(mono_para(piece.strip()))
            out.append(para(''))
            continue

        # Table
        if line.strip().startswith('|') and i + 1 < n and re.match(r'^\s*\|[\s:\-|]+\|\s*$', lines[i+1]):
            header = split_table_row(line)
            i += 2  # skip separator
            rows = [header]
            while i < n and lines[i].strip().startswith('|'):
                rows.append(split_table_row(lines[i])); i += 1
            out.append(build_table(rows))
            continue

        # Blank
        if not line.strip():
            out.append(para('')); i += 1; continue

        # Horizontal rule
        if re.match(r'^-{3,}$', line.strip()):
            out.append(para('')); i += 1; continue

        # Headings
        if line.startswith('### '):
            out.append(para(line[4:].strip(), style='Heading2')); i += 1; continue
        if line.startswith('## '):
            out.append(para(line[3:].strip(), style='Heading1')); i += 1; continue
        if line.startswith('# '):
            out.append(para(line[2:].strip(), style='Title', jc='center')); i += 1; continue

        # Blockquote
        if line.lstrip().startswith('>'):
            txt = line.lstrip()[1:].strip()
            txt = txt.replace('*', '')
            out.append(para(txt, jc='left', size=18)); i += 1; continue

        # Numbered / bullet list
        m = re.match(r'^\s*(\d+)\.\s+(.*)$', line)
        if m:
            out.append(bullet_para(f'{m.group(1)}. {m.group(2)}')); i += 1; continue
        if re.match(r'^\s*[-*]\s+', line):
            out.append(bullet_para(re.sub(r'^\s*[-*]\s+', '', line))); i += 1; continue

        # Normal paragraph
        out.append(para(line)); i += 1

    return '\n'.join(out)


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
    <w:rPr><w:b/><w:sz w:val="27"/><w:szCs w:val="27"/><w:color w:val="1F3864"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="320" w:after="120"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:rPr><w:b/><w:i/><w:sz w:val="23"/><w:szCs w:val="23"/><w:color w:val="2E5496"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="200" w:after="80"/></w:pPr>
  </w:style>
</w:styles>'''

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

WORD_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''


def main():
    with open(SRC, 'r', encoding='utf-8') as f:
        md = f.read()
    body = convert(md)
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                f'<w:body>{body}'
                '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
                '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
                '</w:body></w:document>')
    # Build word relationships (styles + each embedded image)
    rel_items = ['<Relationship Id="rId1" '
                 'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
                 'Target="styles.xml"/>']
    for m in MEDIA:
        rel_items.append(
            f'<Relationship Id="{m["rid"]}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            f'Target="{m["target"]}"/>')
    word_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 + ''.join(rel_items) + '</Relationships>')

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
        for m in MEDIA:
            with open(m['abspath'], 'rb') as f:
                zf.writestr('word/' + m['target'], f.read())
    print('Created', OUT, 'with', len(MEDIA), 'embedded image(s)')


if __name__ == '__main__':
    main()
