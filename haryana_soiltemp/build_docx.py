#!/usr/bin/env python3
"""Build the Word .docx for the Haryana IoT soil-temperature paper.

Reuses the raw-OOXML helpers in create_agentic_docx.py and adds rendering of
the numbered display equations ($$ ... $$ (n)) as Unicode text with real
sub/superscript runs and a right-aligned equation number.
"""

import os
import re
import sys
import zipfile

sys.path.insert(0, '/projects/sandbox/AMMAN')
import create_agentic_docx as B

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, 'Paper_IoT_Edge_ML_Soil_Temperature_Haryana.md')
OUT = os.path.join(HERE, 'Paper_IoT_Edge_ML_Soil_Temperature_Haryana.docx')
FIG_DIR = os.path.join(HERE, 'figures')
FIGS = {1: 'Figure_1_System_Architecture.png', 2: 'Figure_2_Sensor_Node.png',
        3: 'Figure_3_Time_Series.png', 4: 'Figure_4_RMSE_Horizons.png',
        5: 'Figure_5_Scatter.png', 6: 'Figure_6_Feature_Importance.png'}

SYMBOLS = {
    'alpha': 'α', 'beta': 'β', 'delta': 'δ', 'Delta': 'Δ', 'epsilon': 'ε', 'varepsilon': 'ε',
    'eta': 'η', 'theta': 'θ', 'lambda': 'λ', 'mu': 'μ', 'nu': 'ν', 'pi': 'π', 'rho': 'ρ',
    'sigma': 'σ', 'varphi': 'φ', 'phi': 'φ', 'omega': 'ω', 'partial': '∂', 'cdot': '·',
    'times': '×', 'sim': '~', 'leftarrow': '←', 'top': 'ᵀ', 'lVert': '‖', 'rVert': '‖',
    'qquad': '    ', 'quad': '  ', ',': ' ', 'sum': '∑', 'max': 'max', 'min': 'min',
    'sin': 'sin', 'cos': 'cos', 'tan': 'tan', 'arccos': 'arccos', 'log': 'log', 'exp': 'exp',
    'arg': 'arg', 'left': '', 'right': '',
}
ACCENT = {'tilde': '\u0303', 'bar': '\u0304', 'hat': '\u0302'}


def group(s, i):
    """Return (content, next_index) for a {...} group or single token at s[i]."""
    while i < len(s) and s[i] == ' ':
        i += 1
    if i < len(s) and s[i] == '{':
        depth, j = 1, i + 1
        while depth:
            if s[j] == '{':
                depth += 1
            elif s[j] == '}':
                depth -= 1
            j += 1
        return s[i + 1:j - 1], j
    if i < len(s) and s[i] == '\\':
        m = re.match(r'\\[A-Za-z]+', s[i:])
        return m.group(0), i + len(m.group(0))
    return s[i], i + 1


def tex(s, style=''):
    """Translate a LaTeX fragment into a list of (text, style) runs."""
    out, i = [], 0
    while i < len(s):
        ch = s[i]
        if ch in '^_':
            g, i = group(s, i + 1)
            out += tex(g, 'sup' if ch == '^' else 'sub')
            continue
        if ch == '{':
            g, i = group(s, i)
            out += tex(g, style)
            continue
        if ch == '\\':
            m = re.match(r'\\([A-Za-z]+|,)', s[i:])
            name = m.group(1)
            i += len(m.group(0))
            if name in ('frac', 'tfrac'):
                a, i = group(s, i)
                b, i = group(s, i)
                simple = lambda g: re.fullmatch(r'[A-Za-z0-9]+', g.strip()) is not None
                wa = (lambda r: r) if simple(a) else (lambda r: [('(', style)] + r + [(')', style)])
                wb = (lambda r: r) if simple(b) else (lambda r: [('(', style)] + r + [(')', style)])
                out += wa(tex(a, style)) + [('/', style)] + wb(tex(b, style))
            elif name == 'sqrt':
                a, i = group(s, i)
                out += [('√(', style)] + tex(a, style) + [(')', style)]
            elif name in ('mathbf',):
                a, i = group(s, i)
                out += tex(a, 'bold' if not style else style)
            elif name in ('mathrm', 'text'):
                a, i = group(s, i)
                out += tex(a, style)
            elif name == 'mathcal':
                a, i = group(s, i)
                out.append(('ℒ' if a == 'L' else a, style))
            elif name in ACCENT:
                a, i = group(s, i)
                runs = tex(a, style)
                if runs:
                    t, st = runs[-1]
                    runs[-1] = (t + ACCENT[name], st)
                out += runs
            else:
                out.append((SYMBOLS.get(name, name), style))
            continue
        out.append((ch, style))
        i += 1
    merged = []
    for t, st in out:
        if merged and merged[-1][1] == st:
            merged[-1] = (merged[-1][0] + t, st)
        else:
            merged.append((t, st))
    return merged


def eq_paragraph(latex, num):
    runs = ''
    for t, st in tex(latex):
        rpr = '<w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>'
        if st == 'sub':
            rpr += '<w:vertAlign w:val="subscript"/>'
        elif st == 'sup':
            rpr += '<w:vertAlign w:val="superscript"/>'
        elif st == 'bold':
            rpr += '<w:b/>'
        runs += f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{B.escape_xml(t)}</w:t></w:r>'
    return ('<w:p><w:pPr><w:tabs><w:tab w:val="center" w:pos="4680"/>'
            '<w:tab w:val="right" w:pos="9360"/></w:tabs><w:spacing w:before="120" w:after="120"/>'
            '<w:jc w:val="left"/></w:pPr><w:r><w:tab/></w:r>' + runs +
            f'<w:r><w:tab/><w:t>({num})</w:t></w:r></w:p>')


def body_xml(md, image_rels):
    """Split markdown around display equations, delegating other text to B.md_to_body."""
    parts, buf = [], []
    for line in md.split('\n'):
        m = re.match(r'^\$\$ (.*) \$\$ \((\d+)\)$', line.strip())
        if m:
            parts.append(('md', '\n'.join(buf)))
            parts.append(('eq', m.groups()))
            buf = []
        else:
            buf.append(line)
    parts.append(('md', '\n'.join(buf)))
    xml = []
    for kind, val in parts:
        if kind == 'eq':
            xml.append(eq_paragraph(*val))
        else:
            # md_to_body numbers images from 1 in every call; renumber them globally
            k = len(image_rels)
            chunk = B.md_to_body(val, image_rels)
            for i in range(len(image_rels) - k, 0, -1):
                g = k + i
                chunk = chunk.replace(f'"rIdImg{i}"', f'"rIdFig{g}"')
                chunk = chunk.replace(f'id="{1000 + i}"', f'id="{2000 + g}"')
                image_rels[g - 1] = (f'rIdFig{g}', image_rels[g - 1][1])
            xml.append(chunk)
    return '\n'.join(xml)


def main():
    B.FIG_DIR, B.FIGURE_FILES = FIG_DIR, FIGS
    md = open(MD, encoding='utf-8').read()
    image_rels = []
    body = body_xml(md, image_rels)
    doc = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{body}
    <w:sectPr><w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', B.CONTENT_TYPES)
        zf.writestr('_rels/.rels', B.RELS)
        zf.writestr('word/_rels/document.xml.rels', B.build_word_rels(image_rels))
        zf.writestr('word/document.xml', doc)
        zf.writestr('word/styles.xml', B.STYLES)
        zf.writestr('word/numbering.xml', B.NUMBERING)
        for _, fname in image_rels:
            zf.write(os.path.join(FIG_DIR, fname), f'word/media/{fname}')
    print('wrote', OUT, len(image_rels), 'figures')


if __name__ == '__main__':
    main()
