#!/usr/bin/env python3
"""
Build a .docx from Manuscript_MOO_FlatTube_HybridNanofluid.md using only the
Python standard library (zipfile). Handles:
  - Title / Heading1 (##) / Heading2 (###)
  - Inline **bold** and *italic*
  - Centered standalone bold (authors) and italic (affiliation, figure captions)
  - $$ ... $$ display equations converted to readable Unicode with real Word
    subscript/superscript runs and a right-hand equation number.
"""

import zipfile
import re

SRC = '/projects/sandbox/AMMAN/Manuscript_MOO_FlatTube_HybridNanofluid.md'
OUT = '/projects/sandbox/AMMAN/Manuscript_MOO_FlatTube_HybridNanofluid.docx'

SUB_S, SUB_E, SUP_S, SUP_E = '\x01', '\x02', '\x03', '\x04'
LB, RB, BAR = '\x05', '\x06', '\x07'  # protected literal { } |

SYMBOLS = {
    r'\rho': 'ρ', r'\varphi': 'φ', r'\phi': 'φ', r'\mu': 'μ', r'\eta': 'η',
    r'\Delta': 'Δ', r'\delta': 'δ', r'\nabla': '∇', r'\partial': '∂',
    r'\omega': 'ω', r'\sum': 'Σ', r'\cdot': '·', r'\times': '×',
    r'\leq': '≤', r'\geq': '≥', r'\le': '≤', r'\ge': '≥', r'\in': '∈',
    r'\approx': '≈', r'\pi': 'π', r'\sigma': 'σ', r'\theta': 'θ',
    r'\alpha': 'α', r'\beta': 'β', r'\gamma': 'γ', r'\lambda': 'λ', r'\tau': 'τ',
}


UNI_SUB = {c: d for c, d in zip('0123456789+-=()', '₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎')}
UNI_SUB.update({c: d for c, d in zip('aehiklmnoprstuvx', 'ₐₑₕᵢₖₗₘₙₒₚᵣₛₜᵤᵥₓ')})
UNI_SUP = {c: d for c, d in zip('0123456789+-=()', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾')}
UNI_SUP.update({'n': 'ⁿ', 'i': 'ⁱ', 'T': 'ᵀ'})


def find_group(s, i):
    """s[i] == '{'; return (content, index_after_matching_close)."""
    assert s[i] == '{'
    depth = 0
    for j in range(i, len(s)):
        if s[j] == '{':
            depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
    return s[i + 1:], len(s)


def process_commands(s):
    """Resolve \\frac, \\sqrt, \\hat, \\bar, \\overline, \\text, \\mathbf, etc."""
    out = ''
    i = 0
    while i < len(s):
        if s[i] == '\\':
            m = re.match(r'\\(frac|tfrac|dfrac|sqrt|hat|bar|overline|dot|text|mathbf|mathcal|mathrm)', s[i:])
            if m:
                cmd = m.group(1)
                j = i + len(m.group(0))
                if j < len(s) and s[j] == '{':
                    a, j = find_group(s, j)
                    a = process_commands(a)
                    if cmd in ('frac', 'tfrac', 'dfrac'):
                        if j < len(s) and s[j] == '{':
                            b, j = find_group(s, j)
                            b = process_commands(b)
                            out += '(' + a + ')/(' + b + ')'
                        else:
                            out += a
                    elif cmd == 'sqrt':
                        out += '√(' + a + ')'
                    elif cmd == 'hat':
                        out += (a[0] + '\u0302' + a[1:]) if a else a
                    elif cmd in ('bar', 'overline'):
                        out += (a[0] + '\u0305' + a[1:]) if a else a
                    elif cmd == 'dot':
                        out += (a[0] + '\u0307' + a[1:]) if a else a
                    else:  # text / mathbf / mathcal / mathrm
                        out += a
                    i = j
                    continue
        out += s[i]
        i += 1
    return out


def to_unicode_scripts(s):
    """Resolve nested _x / ^x inside an already-script group to Unicode chars."""
    out = ''
    i = 0
    while i < len(s):
        c = s[i]
        if c in ('_', '^'):
            table = UNI_SUB if c == '_' else UNI_SUP
            if i + 1 < len(s) and s[i + 1] == '{':
                content, j = find_group(s, i + 1)
            elif i + 1 < len(s):
                content, j = s[i + 1], i + 2
            else:
                content, j = '', i + 1
            out += ''.join(table.get(ch, ch) for ch in content)
            i = j
            continue
        out += c
        i += 1
    return out


def mark_scripts(s):
    out = ''
    i = 0
    while i < len(s):
        c = s[i]
        if c in ('_', '^'):
            start, end = (SUB_S, SUB_E) if c == '_' else (SUP_S, SUP_E)
            if i + 1 < len(s) and s[i + 1] == '{':
                content, j = find_group(s, i + 1)
                out += start + to_unicode_scripts(content) + end
                i = j
                continue
            elif i + 1 < len(s):
                out += start + s[i + 1] + end
                i += 2
                continue
        out += c
        i += 1
    return out


def convert_latex(eq):
    m = re.search(r'\\tag\{([^}]*)\}', eq)
    number = m.group(1) if m else ''
    eq = re.sub(r'\\tag\{[^}]*\}', '', eq).strip()
    eq = eq.replace(r'\{', LB).replace(r'\}', RB).replace(r'\|', BAR)
    eq = process_commands(eq)
    eq = eq.replace(r'\left', '').replace(r'\right', '')
    for k, v in SYMBOLS.items():
        eq = eq.replace(k, v)
    eq = re.sub(r'\\quad', '  ', eq)
    eq = re.sub(r'\\[,;:! ]', ' ', eq)
    eq = re.sub(r'\\%', '%', eq)
    eq = mark_scripts(eq)
    eq = eq.replace('{', '').replace('}', '')
    eq = eq.replace(LB, '{').replace(RB, '}').replace(BAR, '|')
    eq = re.sub(r'[ ]{2,}', ' ', eq)
    return eq, number


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def run_xml(text, bold=False, italic=False, vert=None):
    props = ''
    if bold:
        props += '<w:b/>'
    if italic:
        props += '<w:i/>'
    if vert:
        props += f'<w:vertAlign w:val="{vert}"/>'
    rpr = f'<w:rPr>{props}</w:rPr>' if props else ''
    return f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'


def inline_runs(text, bold=False, italic=False):
    """Parse **bold** and *italic* into runs."""
    runs = []
    i = 0
    while i < len(text):
        if text.startswith('**', i):
            j = text.find('**', i + 2)
            if j != -1:
                runs.extend(inline_runs(text[i + 2:j], bold=True, italic=italic))
                i = j + 2
                continue
        if text[i] == '*':
            j = text.find('*', i + 1)
            if j != -1:
                runs.extend(inline_runs(text[i + 1:j], bold=bold, italic=True))
                i = j + 1
                continue
        # accumulate a plain chunk up to next marker
        nxt = len(text)
        for mark in ('**', '*'):
            k = text.find(mark, i)
            if k != -1:
                nxt = min(nxt, k)
        chunk = text[i:nxt] if nxt > i else text[i]
        runs.append(run_xml(chunk, bold=bold, italic=italic))
        i += len(chunk)
    return runs


def equation_runs(eq_text):
    runs = []
    buf = ''
    vert = None

    def flush():
        nonlocal buf
        if buf:
            runs.append(run_xml(buf, vert=vert))
            buf = ''
    for ch in eq_text:
        if ch == SUB_S:
            flush(); vert = 'subscript'
        elif ch == SUB_E:
            flush(); vert = None
        elif ch == SUP_S:
            flush(); vert = 'superscript'
        elif ch == SUP_E:
            flush(); vert = None
        else:
            buf += ch
    flush()
    return runs


def para(runs_xml, style=None, jc=None):
    ppr = '<w:pPr>'
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if jc:
        ppr += f'<w:jc w:val="{jc}"/>'
    ppr += '</w:pPr>'
    return f'<w:p>{ppr}{"".join(runs_xml)}</w:p>'


def build_body(md):
    paras = []
    for raw in md.split('\n'):
        line = raw.rstrip()
        if not line or line.startswith('---'):
            continue
        if line.startswith('# ') and not line.startswith('## '):
            paras.append(para(inline_runs(line[2:].strip()), style='Title', jc='center'))
        elif line.startswith('### '):
            paras.append(para(inline_runs(line[4:].strip()), style='Heading2'))
        elif line.startswith('## '):
            paras.append(para(inline_runs(line[3:].strip()), style='Heading1'))
        elif line.startswith('$$') and line.endswith('$$'):
            eq_text, number = convert_latex(line[2:-2])
            runs = equation_runs(eq_text)
            if number:
                runs.append(run_xml('\t(' + number + ')'))
            paras.append(para(runs, jc='center'))
        else:
            stripped = line.strip()
            # standalone bold (authors) -> centered bold
            if stripped.startswith('**') and stripped.endswith('**') and stripped.count('**') == 2:
                paras.append(para(inline_runs(stripped), jc='center'))
            # standalone italic (affiliation, figure captions) -> centered italic
            elif stripped.startswith('*') and stripped.endswith('*') and not stripped.startswith('**') and stripped.count('*') == 2:
                paras.append(para(inline_runs(stripped), jc='center'))
            else:
                paras.append(para(inline_runs(line)))
    return '\n'.join(paras)


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
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
    <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
    <w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/></w:pPr>
  </w:style>
</w:styles>'''


def main():
    with open(SRC, 'r', encoding='utf-8') as f:
        md = f.read()
    body = build_body(md)
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {body}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>'''
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', WORD_RELS)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', STYLES)
    print('Created', OUT)


if __name__ == '__main__':
    main()
