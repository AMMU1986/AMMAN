#!/usr/bin/env python3
"""
Build a Word .docx for the chapter
"Differential Equations and Dynamical Systems in Biology"
from the custom markdown source, with embedded PNG figures, tables, and
equation displays. Stdlib only (zipfile + struct) — no python-docx needed.

Custom markdown conventions:
  # Title
  ## Heading1   ### Heading2
  $$...$$        equation display (own line)
  [FIGURE:filename|caption text]
  [TABLE:caption line
  col | col | col
  cell | cell | cell
  ...]
  [1] reference entries under the References heading
"""

import os
import re
import zipfile
import struct

BASE = '/projects/sandbox/AMMAN'
FIG_DIR = os.path.join(BASE, 'biomath_figures')
MD = os.path.join(BASE, 'Chapter_Differential_Equations_Biology.md')
OUT = os.path.join(BASE, 'Differential_Equations_Dynamical_Systems_Biology.docx')

EMU_PER_PX = 9525          # 1 px = 9525 EMU (at 96 dpi)
MAX_IMG_WIDTH_EMU = 5486400  # ~5.7 inches usable width

# ─── OOXML boilerplate ───

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
  <w:docDefaults>
    <w:rPrDefault><w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:sz w:val="24"/><w:szCs w:val="24"/>
    </w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr>
      <w:spacing w:after="140" w:line="360" w:lineRule="auto"/>
    </w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/><w:pPr><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="120" w:before="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="36"/><w:szCs w:val="36"/><w:color w:val="1F4E79"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Subtitle">
    <w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="300"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="24"/><w:color w:val="595959"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="140"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="30"/><w:szCs w:val="30"/><w:color w:val="1F4E79"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="2E75B6"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Abstract">
    <w:name w:val="Abstract"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:right="480"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Equation">
    <w:name w:val="Equation"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="120"/></w:pPr>
    <w:rPr><w:i/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="References">
    <w:name w:val="References"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="480" w:hanging="480"/><w:spacing w:after="60"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureImage">
    <w:name w:val="Figure Image"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="200" w:after="60"/><w:keepNext/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FigureCaption">
    <w:name w:val="Figure Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="240"/><w:ind w:left="360" w:right="360"/></w:pPr>
    <w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="Table Caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="200" w:after="80"/><w:jc w:val="left"/><w:keepNext/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr><w:tblBorders>
      <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    </w:tblBorders></w:tblPr>
  </w:style>
</w:styles>'''


def escape_xml(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('not a PNG: ' + path)
    w, h = struct.unpack('>II', head[16:24])
    return w, h


def make_run(text, bold=False, italic=False, mono=False):
    props = []
    if mono:
        props.append('<w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>')
    if bold:
        props.append('<w:b/>')
    if italic:
        props.append('<w:i/>')
    rpr = ('<w:rPr>' + ''.join(props) + '</w:rPr>') if props else ''
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'


def parse_inline(text):
    """Handle **bold** and *italic* markdown inline."""
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


def para(text, style='Normal'):
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
    return f'<w:p>{ppr}{parse_inline(text)}</w:p>'


# ─── Equation rendering: convert LaTeX-ish $$..$$ to readable unicode math ───

GREEK = {
    'alpha': '\u03b1', 'beta': '\u03b2', 'gamma': '\u03b3', 'delta': '\u03b4',
    'sigma': '\u03c3', 'mu': '\u03bc', 'partial': '\u2202', 'ast': '*',
    'infty': '\u221e', 'ln': 'ln',
}


def _find_group(s, start):
    """Given s[start]=='{', return (content, index_after_closing_brace)."""
    depth = 0
    for j in range(start, len(s)):
        if s[j] == '{':
            depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0:
                return s[start + 1:j], j + 1
    return s[start + 1:], len(s)


def _replace_frac(s):
    """Replace \\frac{a}{b} / \\dfrac{a}{b} handling nested braces, recursively."""
    out = []
    i = 0
    while i < len(s):
        m = re.match(r'\\d?frac', s[i:])
        if m:
            k = i + m.end()
            # skip spaces
            while k < len(s) and s[k] == ' ':
                k += 1
            if k < len(s) and s[k] == '{':
                a, k2 = _find_group(s, k)
                while k2 < len(s) and s[k2] == ' ':
                    k2 += 1
                if k2 < len(s) and s[k2] == '{':
                    b, k3 = _find_group(s, k2)
                    out.append('(' + _replace_frac(a) + ')/(' + _replace_frac(b) + ')')
                    i = k3
                    continue
        out.append(s[i])
        i += 1
    return ''.join(out)


def latex_to_unicode(eq):
    s = eq
    # named text operators / symbols first
    s = s.replace('\\max', 'max').replace('\\min', 'min')
    s = s.replace('\\ldots', '\u2026').replace('\\cdots', '\u22ef')
    s = re.sub(r'\\mathbf\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\mathrm\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\text\{([^{}]*)\}', r'\1', s)
    # fractions (nested-aware)
    s = _replace_frac(s)
    # matrices / pmatrix -> keep as bracketed layout hint
    s = s.replace('\\begin{pmatrix}', '[ ').replace('\\end{pmatrix}', ' ]')
    s = s.replace('\\\\', ';  ').replace('&', ', ')
    # spacing/commands
    s = s.replace('\\qquad', '     ').replace('\\quad', '   ')
    s = s.replace('\\,', ' ').replace('\\;', ' ').replace('\\!', '')
    s = re.sub(r'\\left', '', s)
    s = re.sub(r'\\right', '', s)
    s = re.sub(r'\[[0-9]mm\]', ' ', s)
    # greek + named
    for name, ch in GREEK.items():
        s = s.replace('\\' + name, ch)
    # subscripts/superscripts
    sup = {'0': '\u2070', '1': '\u00b9', '2': '\u00b2', '3': '\u00b3',
           '4': '\u2074', '5': '\u2075', '6': '\u2076', '7': '\u2077',
           '8': '\u2078', '9': '\u2079', 't': '\u1d57', 'r': '\u02b3',
           'n': '\u207f'}
    sub = {'0': '\u2080', '1': '\u2081', '2': '\u2082', '3': '\u2083',
           '4': '\u2084', '5': '\u2085', '6': '\u2086', '7': '\u2087',
           '8': '\u2088', '9': '\u2089', 'k': '\u2096',
           'm': '\u2098', 'n': '\u2099', 'd': '\u1d48'}

    def repl_sup(m):
        body = m.group(1) if m.group(1) is not None else m.group(2)
        if len(body) > 1 and not body.isdigit():
            return '^(' + body + ')'
        return ''.join(sup.get(ch, '^' + ch) for ch in body)

    def repl_sub(m):
        body = m.group(1) if m.group(1) is not None else m.group(2)
        if len(body) > 1 and not body.isdigit():
            return '_(' + body + ')'
        return ''.join(sub.get(ch, '_' + ch) for ch in body)

    s = re.sub(r'\^\{([^{}]*)\}', repl_sup, s)
    s = re.sub(r'\^([A-Za-z0-9])', lambda m: repl_sup(m), s)
    s = re.sub(r'_\{([^{}]*)\}', repl_sub, s)
    s = re.sub(r'_([A-Za-z0-9])', lambda m: repl_sub(m), s)
    # cleanup leftover braces and backslashes
    s = s.replace('{', '').replace('}', '')
    s = s.replace('\\max', 'max').replace('\\', '')
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def make_equation(eq_latex, number):
    uni = latex_to_unicode(eq_latex)
    ppr = ('<w:pPr><w:pStyle w:val="Equation"/>'
           '<w:tabs><w:tab w:val="right" w:pos="9360"/></w:tabs></w:pPr>')
    run_eq = f'<w:r><w:rPr><w:i/><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/></w:rPr><w:t xml:space="preserve">{escape_xml(uni)}</w:t></w:r>'
    run_tab = '<w:r><w:tab/></w:r>'
    run_num = f'<w:r><w:t xml:space="preserve">({number})</w:t></w:r>'
    return f'<w:p>{ppr}{run_eq}{run_tab}{run_num}</w:p>'


def make_table(caption, headers, rows):
    n = len(headers)
    col_w = 9360 // n
    out = ['<w:tbl>']
    out.append('<w:tblPr><w:tblStyle w:val="TableGrid"/>'
               '<w:tblW w:w="9360" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
               '<w:tblBorders>'
               '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '</w:tblBorders></w:tblPr>')
    out.append('<w:tblGrid>' + f'<w:gridCol w:w="{col_w}"/>' * n + '</w:tblGrid>')
    # header
    out.append('<w:tr>')
    for h in headers:
        out.append('<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="1F4E79"/>'
                   '<w:vAlign w:val="center"/></w:tcPr>'
                   f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="40" w:line="276" w:lineRule="auto"/></w:pPr>'
                   f'<w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="20"/></w:rPr>'
                   f'<w:t xml:space="preserve">{escape_xml(h.strip())}</w:t></w:r></w:p></w:tc>')
    out.append('</w:tr>')
    for ri, row in enumerate(rows):
        shade = 'EAF1FB' if ri % 2 == 0 else 'FFFFFF'
        out.append('<w:tr>')
        for ci in range(n):
            cell = row[ci].strip() if ci < len(row) else ''
            out.append(f'<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{shade}"/></w:tcPr>'
                       f'<w:p><w:pPr><w:spacing w:after="40" w:line="276" w:lineRule="auto"/></w:pPr>'
                       f'<w:r><w:rPr><w:sz w:val="20"/></w:rPr>'
                       f'<w:t xml:space="preserve">{escape_xml(cell)}</w:t></w:r></w:p></w:tc>')
        out.append('</w:tr>')
    out.append('</w:tbl>')
    out.append('<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>')
    return para(caption, 'TableCaption') + ''.join(out)


def make_figure(rid, filename, caption, media):
    w, h = png_size(os.path.join(FIG_DIR, filename))
    ew, eh = w * EMU_PER_PX, h * EMU_PER_PX
    if ew > MAX_IMG_WIDTH_EMU:
        scale = MAX_IMG_WIDTH_EMU / ew
        ew = int(ew * scale)
        eh = int(eh * scale)
    drawing = f'''<w:p><w:pPr><w:pStyle w:val="FigureImage"/></w:pPr><w:r><w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0"
                 xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
        <wp:extent cx="{ew}" cy="{eh}"/>
        <wp:docPr id="{rid}" name="{filename}"/>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr><pic:cNvPr id="{rid}" name="{filename}"/><pic:cNvPicPr/></pic:nvPicPr>
              <pic:blipFill><a:blip r:embed="rId{rid}"
                 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>
                <a:stretch><a:fillRect/></a:stretch></pic:blipFill>
              <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{ew}" cy="{eh}"/></a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing></w:r></w:p>'''
    media.append((rid, filename))
    return drawing + para(caption, 'FigureCaption')


def build():
    with open(MD, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    body = []
    media = []          # (rId, filename)
    rid_counter = [100]  # start image rIds high to avoid clashes
    eq_num = [0]
    in_refs = False
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Title
        if stripped.startswith('# ') and not stripped.startswith('## '):
            body.append(para(stripped[2:].strip(), 'Title'))
            i += 1
            continue

        # Subtitle (italic book line right after title)
        if stripped.startswith('*') and stripped.endswith('*') and stripped.count('*') == 2 and i < 5:
            body.append(para(stripped.strip('*'), 'Subtitle'))
            i += 1
            continue

        # Heading1
        if stripped.startswith('## '):
            txt = stripped[3:].strip()
            if txt.lower() == 'references':
                in_refs = True
            body.append(para(txt, 'Heading1'))
            i += 1
            continue

        # Heading2
        if stripped.startswith('### '):
            body.append(para(stripped[4:].strip(), 'Heading2'))
            i += 1
            continue

        # Equation
        if stripped.startswith('$$') and stripped.endswith('$$') and len(stripped) > 4:
            eq_num[0] += 1
            body.append(make_equation(stripped[2:-2].strip(), eq_num[0]))
            i += 1
            continue

        # Figure
        if stripped.startswith('[FIGURE:'):
            inner = stripped[len('[FIGURE:'):].rstrip(']')
            fname, caption = inner.split('|', 1)
            rid_counter[0] += 1
            body.append(make_figure(rid_counter[0], fname.strip(), caption.strip(), media))
            i += 1
            continue

        # Table block: starts with [TABLE: and continues until a line ending with ]
        if stripped.startswith('[TABLE:'):
            block = [stripped[len('[TABLE:'):]]
            while ']' not in block[-1]:
                i += 1
                block.append(lines[i])
            block[-1] = block[-1].rstrip().rstrip(']')
            caption = block[0].strip()
            header_line = block[1]
            headers = [c.strip() for c in header_line.split('|')]
            rows = []
            for rl in block[2:]:
                if rl.strip():
                    rows.append([c.strip() for c in rl.split('|')])
            body.append(make_table(caption, headers, rows))
            i += 1
            continue

        # References entries
        if in_refs and re.match(r'^\[\d+\]', stripped):
            body.append(para(stripped, 'References'))
            i += 1
            continue

        # Keywords line / normal paragraph
        body.append(para(stripped, 'Normal'))
        i += 1

    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{''.join(body)}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"
               w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    # relationships
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rid, fname in media:
        rels.append(f'<Relationship Id="rId{rid}" '
                    f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                    f'Target="media/{fname}"/>')
    rels.append('</Relationships>')
    word_rels = '\n'.join(rels)

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CONTENT_TYPES)
        z.writestr('_rels/.rels', RELS)
        z.writestr('word/_rels/document.xml.rels', word_rels)
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', STYLES)
        for rid, fname in media:
            with open(os.path.join(FIG_DIR, fname), 'rb') as imgf:
                z.writestr(f'word/media/{fname}', imgf.read())

    print(f'Created: {OUT}')
    print(f'Size: {os.path.getsize(OUT)/1024:.1f} KB')
    print(f'Equations rendered: {eq_num[0]}   Figures embedded: {len(media)}')


if __name__ == '__main__':
    build()
