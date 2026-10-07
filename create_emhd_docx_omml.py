#!/usr/bin/env python3
"""
Create a Word (.docx) document from the revised EMHD Carreau hybrid nanofluid
manuscript, rendering every display and inline equation as a NATIVE Word
equation-editor object (OMML / Office Math Markup Language).

Standard library only (no pandoc / python-docx / latex2mathml, which cannot be
installed in this INTEGRATIONS_ONLY sandbox).

The LaTeX subset covered is exactly what the manuscript uses:
  \\frac, \\sqrt, ^{...}, _{...}, \\left[ \\right], \\left( \\right),
  \\left\\{ \\right\\}, \\underbrace{...}_{...}, \\partial, \\nabla, \\cdot,
  \\le, Greek letters, \\, \\quad \\qquad spacing, primes, and the \\tag{} label.
"""

import zipfile
import re

SRC = '/projects/sandbox/AMMAN/Manuscript_EMHD_Carreau_Hybrid_Nanofluid.md'
OUT = '/projects/sandbox/AMMAN/Manuscript_EMHD_Carreau_Hybrid_Nanofluid_Equations.docx'

M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

# ----------------------------------------------------------------------------
# Symbol table: LaTeX macro -> unicode character
# ----------------------------------------------------------------------------
SYMBOLS = {
    r'\alpha': 'α', r'\beta': 'β', r'\gamma': 'γ', r'\Gamma': 'Γ',
    r'\delta': 'δ', r'\Delta': 'Δ', r'\epsilon': 'ε', r'\varepsilon': 'ε',
    r'\zeta': 'ζ', r'\eta': 'η', r'\theta': 'θ', r'\Theta': 'Θ',
    r'\kappa': 'κ', r'\lambda': 'λ', r'\Lambda': 'Λ', r'\mu': 'μ',
    r'\nu': 'ν', r'\xi': 'ξ', r'\pi': 'π', r'\Pi': 'Π', r'\rho': 'ρ',
    r'\sigma': 'σ', r'\Sigma': 'Σ', r'\tau': 'τ', r'\phi': 'φ', r'\Phi': 'Φ',
    r'\varphi': 'φ', r'\chi': 'χ', r'\psi': 'ψ', r'\Psi': 'Ψ',
    r'\omega': 'ω', r'\Omega': 'Ω', r'\Xi': 'Ξ',
    r'\partial': '∂', r'\nabla': '∇', r'\cdot': '·', r'\times': '×',
    r'\le': '≤', r'\leq': '≤', r'\ge': '≥', r'\geq': '≥',
    r'\infty': '∞', r'\ast': '∗', r'\pm': '±', r'\to': '→',
    r'\Pr': 'Pr', r'\quad': ' ', r'\qquad': '  ', r'\,': ' ', r'\;': ' ',
    r'\!': '', r'\left': '', r'\right': '',
}


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


# ----------------------------------------------------------------------------
# Tokenizer
# ----------------------------------------------------------------------------
def tokenize(s):
    toks = []
    i = 0
    n = len(s)
    # longest macros first so \qquad matches before \quad etc.
    macros = sorted(SYMBOLS.keys(), key=len, reverse=True)
    while i < n:
        c = s[i]
        if c == '\\':
            # try macro match
            matched = None
            for mac in macros:
                if s.startswith(mac, i):
                    # ensure we don't match \rho inside \rhox etc.
                    nxt = i + len(mac)
                    if mac[-1].isalpha() and nxt < n and s[nxt].isalpha():
                        continue
                    matched = mac
                    break
            if matched:
                toks.append(('sym', SYMBOLS[matched]))
                i += len(matched)
                continue
            # control word like \frac, \sqrt, \underbrace
            m = re.match(r'\\([a-zA-Z]+)', s[i:])
            if m:
                toks.append(('cmd', m.group(1)))
                i += m.end()
                continue
            # escaped brace or symbol: \{ \} \_ etc.
            toks.append(('char', s[i + 1]))
            i += 2
            continue
        elif c == '{':
            toks.append(('{', '{')); i += 1
        elif c == '}':
            toks.append(('}', '}')); i += 1
        elif c == '^':
            toks.append(('^', '^')); i += 1
        elif c == '_':
            toks.append(('_', '_')); i += 1
        elif c == "'":
            # collect run of primes
            j = i
            while j < n and s[j] == "'":
                j += 1
            toks.append(('prime', s[i:j]))
            i = j
        elif c.isspace():
            i += 1  # ignore layout whitespace; spacing comes from macros
        else:
            toks.append(('char', c)); i += 1
    return toks


# ----------------------------------------------------------------------------
# Parser -> list of OMML element strings
# ----------------------------------------------------------------------------
PRIME_MAP = {1: '′', 2: '″', 3: '‴', 4: '⁗'}


def run(text):
    return f'<m:r><m:t xml:space="preserve">{esc(text)}</m:t></m:r>'


def parse(toks):
    """Return (omml_string, next_index). Parses until EOF or matching brace."""
    pos = [0]
    out = _parse_seq(toks, pos, stop_on_brace=False)
    return out


def _read_group(toks, pos):
    """Read a {...} group or a single atom; return its omml string."""
    if pos[0] >= len(toks):
        return ''
    kind, val = toks[pos[0]]
    if kind == '{':
        pos[0] += 1
        inner = _parse_seq(toks, pos, stop_on_brace=True)
        if pos[0] < len(toks) and toks[pos[0]][0] == '}':
            pos[0] += 1
        return inner
    # single atom
    return _parse_atom(toks, pos)


def _parse_atom(toks, pos):
    kind, val = toks[pos[0]]
    if kind == 'cmd':
        pos[0] += 1
        if val == 'frac':
            num = _read_group(toks, pos)
            den = _read_group(toks, pos)
            return (f'<m:f><m:fPr><m:type m:val="bar"/></m:fPr>'
                    f'<m:num>{num}</m:num><m:den>{den}</m:den></m:f>')
        if val == 'sqrt':
            rad = _read_group(toks, pos)
            return f'<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e>{rad}</m:e></m:rad>'
        if val == 'underbrace':
            base = _read_group(toks, pos)
            sub = ''
            if pos[0] < len(toks) and toks[pos[0]][0] == '_':
                pos[0] += 1
                sub = _read_group(toks, pos)
            # bottom brace accent + limit underneath
            inner = (f'<m:groupChr><m:groupChrPr><m:chr m:val="&#9183;"/>'
                     f'<m:pos m:val="bot"/><m:vertJc m:val="top"/></m:groupChrPr>'
                     f'<m:e>{base}</m:e></m:groupChr>')
            return (f'<m:limLow><m:e>{inner}</m:e><m:lim>{sub}</m:lim></m:limLow>')
        if val in ('mathrm', 'text', 'mathbf', 'operatorname'):
            return _read_group(toks, pos)
        # unknown command -> literal
        return run('\\' + val)
    return _read_group_single(toks, pos)


def _read_group_single(toks, pos):
    kind, val = toks[pos[0]]
    if kind == '{':
        return _read_group(toks, pos)
    pos[0] += 1
    if kind in ('char',):
        return run(val)
    if kind == 'sym':
        return run(val)
    if kind == 'prime':
        return run(''.join(PRIME_MAP.get(len(val), "'" * len(val)) for _ in [0]))
    return run(val)


def _parse_seq(toks, pos, stop_on_brace):
    """Parse a sequence, handling scripts (^ _) that bind to the previous atom."""
    elems = []
    while pos[0] < len(toks):
        kind, val = toks[pos[0]]
        if kind == '}' and stop_on_brace:
            break
        if kind in ('^', '_'):
            # script binds to previous element
            base = elems.pop() if elems else run('')
            sup = None
            sub = None
            if kind == '^':
                pos[0] += 1
                sup = _read_group(toks, pos)
                if pos[0] < len(toks) and toks[pos[0]][0] == '_':
                    pos[0] += 1
                    sub = _read_group(toks, pos)
            else:
                pos[0] += 1
                sub = _read_group(toks, pos)
                if pos[0] < len(toks) and toks[pos[0]][0] == '^':
                    pos[0] += 1
                    sup = _read_group(toks, pos)
            elems.append(_script(base, sup, sub))
            continue
        if kind == 'prime':
            pos[0] += 1
            p = PRIME_MAP.get(len(val), "'" * len(val))
            base = elems.pop() if elems else run('')
            elems.append(_script(base, run(p), None))
            continue
        elems.append(_parse_atom(toks, pos))
    return ''.join(elems)


def _script(base, sup, sub):
    if sup is not None and sub is not None:
        return (f'<m:sSubSup><m:e>{base}</m:e>'
                f'<m:sub>{sub}</m:sub><m:sup>{sup}</m:sup></m:sSubSup>')
    if sup is not None:
        return f'<m:sSup><m:e>{base}</m:e><m:sup>{sup}</m:sup></m:sSup>'
    if sub is not None:
        return f'<m:sSub><m:e>{base}</m:e><m:sub>{sub}</m:sub></m:sSub>'
    return base


def latex_to_omml(latex, display=True, tag=None):
    # strip \tag{..}
    latex = re.sub(r'\\tag\{[^}]*\}', '', latex)
    # normalise \left\{ \right\}
    latex = latex.replace(r'\left\{', '{LBRACE}').replace(r'\right\}', '{RBRACE}')
    # keep delimiters as literal chars: convert \left[ -> [ etc. handled by SYMBOLS(\left->'')
    body = parse(tokenize(latex))
    body = body.replace('{LBRACE}', run('{')).replace('{RBRACE}', run('}'))
    tag_run = ''
    if tag:
        tag_run = f'<m:r><m:t xml:space="preserve">     ({tag})</m:t></m:r>'
    omath = f'<m:oMath>{body}{tag_run}</m:oMath>'
    if display:
        jc = '<m:jc m:val="center"/>' if not tag else '<m:jc m:val="center"/>'
        return (f'<w:p><m:oMathPara><m:oMathParaPr>{jc}</m:oMathParaPr>'
                f'{omath}</m:oMathPara></w:p>')
    return omath


# ----------------------------------------------------------------------------
# Inline math: replace $...$ fragments inside a text line with OMML runs.
# For robustness we also convert a handful of unicode-only inline expressions
# as plain text (they are already unicode in the source).
# ----------------------------------------------------------------------------
def render_inline(text):
    """Return list of (is_math, payload) segments for a paragraph line."""
    segs = []
    for i, part in enumerate(re.split(r'(\$[^$]+\$)', text)):
        if not part:
            continue
        if part.startswith('$') and part.endswith('$') and len(part) > 2:
            segs.append(('math', latex_to_omml(part[1:-1], display=False)))
        else:
            segs.append(('text', part))
    return segs


def runs_from_inline(text):
    out = []
    for kind, payload in render_inline(text):
        if kind == 'math':
            out.append(payload)
        else:
            for p in re.split(r'(\*\*[^*]+\*\*)', payload):
                if not p:
                    continue
                if p.startswith('**') and p.endswith('**'):
                    out.append(f'<w:r><w:rPr><w:b/></w:rPr>'
                               f'<w:t xml:space="preserve">{esc(p[2:-2])}</w:t></w:r>')
                else:
                    out.append(f'<w:r><w:t xml:space="preserve">{esc(p)}</w:t></w:r>')
    return ''.join(out) if out else '<w:r><w:t xml:space="preserve"></w:t></w:r>'


def para(text, style=None):
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ''
    return f'<w:p>{ppr}{runs_from_inline(text)}</w:p>'


# ----------------------------------------------------------------------------
# Tables
# ----------------------------------------------------------------------------
def split_row(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def is_sep(line):
    return bool(re.match(r'^\|[\s\-:|]+\|?$', line.strip()))


def table_xml(rows):
    ncol = max(len(r) for r in rows)
    grid = ''.join('<w:gridCol w:w="%d"/>' % (9000 // ncol) for _ in range(ncol))

    def cell(txt, header=False):
        shade = '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>' if header else ''
        rpr = '<w:rPr><w:b/></w:rPr>' if header else ''
        return (f'<w:tc><w:tcPr>{shade}</w:tcPr>'
                f'<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>'
                f'<w:r>{rpr}<w:t xml:space="preserve">{esc(txt)}</w:t></w:r></w:p></w:tc>')

    body = ''
    for i, row in enumerate(rows):
        cells = row + [''] * (ncol - len(row))
        body += '<w:tr>' + ''.join(cell(c, i == 0) for c in cells) + '</w:tr>'
    return (f'<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
            f'<w:tblW w:w="0" w:type="auto"/></w:tblPr>'
            f'<w:tblGrid>{grid}</w:tblGrid>{body}</w:tbl>')


# ----------------------------------------------------------------------------
# Markdown -> body XML
# ----------------------------------------------------------------------------
def convert(md):
    out = []
    lines = md.split('\n')
    i, n = 0, len(lines)
    while i < n:
        line = lines[i].rstrip()

        # Display equation block  $$ ... \tag{k} ... $$
        if line.strip() == '$$':
            j = i + 1
            buf = []
            while j < n and lines[j].strip() != '$$':
                buf.append(lines[j])
                j += 1
            latex = '\n'.join(buf)
            tagm = re.search(r'\\tag\{([^}]*)\}', latex)
            tag = tagm.group(1) if tagm else None
            out.append(latex_to_omml(latex, display=True, tag=tag))
            i = j + 1
            continue

        if not line:
            out.append('<w:p/>'); i += 1; continue

        if line.strip().startswith('|'):
            block = []
            while i < n and lines[i].strip().startswith('|'):
                if not is_sep(lines[i]):
                    block.append(split_row(lines[i]))
                i += 1
            if block:
                out.append(table_xml(block))
            continue

        if re.match(r'^-{3,}$', line.strip()):
            i += 1; continue

        mimg = re.match(r'^!\[.*?\]\((.*?)\)\s*$', line.strip())
        if mimg:
            out.append(para(f'[Figure placeholder: {mimg.group(1)}]'))
            i += 1; continue

        if line.startswith('### '):
            out.append(para(line[4:].strip(), 'Heading2'))
        elif line.startswith('## '):
            out.append(para(line[3:].strip(), 'Heading1'))
        elif line.startswith('# '):
            out.append(para(line[2:].strip(), 'Title'))
        else:
            out.append(para(line))
        i += 1
    return '\n'.join(out)


# ----------------------------------------------------------------------------
# OOXML package parts
# ----------------------------------------------------------------------------
CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
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
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr><w:tblBorders>
      <w:top w:val="single" w:sz="4" w:color="000000"/>
      <w:left w:val="single" w:sz="4" w:color="000000"/>
      <w:bottom w:val="single" w:sz="4" w:color="000000"/>
      <w:right w:val="single" w:sz="4" w:color="000000"/>
      <w:insideH w:val="single" w:sz="4" w:color="000000"/>
      <w:insideV w:val="single" w:sz="4" w:color="000000"/>
    </w:tblBorders></w:tblPr>
  </w:style>
</w:styles>'''


def main():
    with open(SRC, 'r', encoding='utf-8') as f:
        md = f.read()
    body = convert(md)

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<w:body>{body}'
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
        '</w:body></w:document>'
    )

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', WORD_RELS)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
    print(f'Created {OUT}')


if __name__ == '__main__':
    main()
