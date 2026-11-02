#!/usr/bin/env python3
"""
Create the Word .docx for the manuscript
"Fixed-time stability of Cohen-Grossberg BAM neural networks with delayed
destabilizing impulses".

Reuses the raw-OOXML helpers of create_agentic_docx.py (python-docx is not
available in this sandbox) and adds:
  * embedding of figures written as  ![Figure N](path)  in the markdown,
  * conversion of LaTeX math ($...$ inline, $$...\\tag{n}$$ display) into
    readable Cambria Math runs with real superscripts/subscripts,
  * right-aligned equation numbers.

Usage:
    python3 create_fxts_docx.py
"""

import os
import re
import zipfile

import create_agentic_docx as base

HERE = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(HERE, 'Manuscript_FXTS_CGBAMNN_Delayed_Impulses.md')
DOCX_FILE = os.path.join(HERE, 'Manuscript_FXTS_CGBAMNN_Delayed_Impulses.docx')

# ---------------------------------------------------------------------------
# LaTeX -> run list
# ---------------------------------------------------------------------------

SYM = {
    'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ϵ',
    'varepsilon': 'ε', 'zeta': 'ζ', 'eta': 'η', 'theta': 'θ', 'kappa': 'κ',
    'lambda': 'λ', 'mu': 'μ', 'nu': 'ν', 'xi': 'ξ', 'rho': 'ρ',
    'varrho': 'ϱ', 'sigma': 'σ', 'tau': 'τ', 'phi': 'φ', 'chi': 'χ',
    'psi': 'ψ', 'omega': 'ω', 'Theta': 'Θ', 'Phi': 'Φ', 'Psi': 'Ψ',
    'Delta': 'Δ', 'ell': 'ℓ', 'le': '≤', 'leq': '≤', 'ge': '≥', 'geq': '≥',
    'ne': '≠', 'to': '→', 'infty': '∞', 'cdot': '·', 'times': '×',
    'sum': '∑', 'int': '∫', 'bigcup': '⋃', 'cap': '∩', 'subset': '⊂',
    'in': '∈', 'notin': '∉', 'square': '□', 'star': '⋆', 'ldots': '…',
    'dots': '…', 'cdots': '⋯', 'lceil': '⌈', 'rfloor': '⌋', 'ast': '∗',
    'ln': 'ln', 'max': 'max', 'min': 'min', 'sin': 'sin', 'tanh': 'tanh',
    'qquad': '\u2003\u2003', 'quad': '\u2003', ',': '\u2009', ';': '\u2005',
    '!': '', 'bmod': ' mod ', 'mid': '|', '{': '{', '}': '}', '|': '‖',
    'prime': '′',
}
ACCENT = {'tilde': '\u0303', 'hat': '\u0302', 'check': '\u030c',
          'bar': '\u0304', 'dot': '\u0307'}
BB = {'R': 'ℝ', 'N': 'ℕ'}
CAL = {'H': 'ℋ', 'N': '𝒩', 'S': '𝒮'}
DROP = {'left', 'right', 'Big', 'big', 'Bigg', 'bigg', 'displaystyle'}


def tokenize(s):
    toks, i = [], 0
    while i < len(s):
        ch = s[i]
        if ch == '\\':
            if i + 1 < len(s) and s[i + 1] == '\\':
                toks.append('\\\\'); i += 2; continue
            m = re.match(r'\\([A-Za-z]+)', s[i:])
            if m:
                toks.append('\\' + m.group(1)); i += len(m.group(0)); continue
            toks.append('\\' + s[i + 1]); i += 2; continue
        if ch.isspace():
            i += 1; continue
        toks.append(ch); i += 1
    return toks


class Parser:
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def take(self):
        tok = self.peek(); self.i += 1; return tok

    def group(self, va):
        """Parse one argument (braced group or single token)."""
        if self.peek() == '{':
            self.take()
            out = self.seq(va, stop='}')
            self.take()
            return out
        return self.atom(va)

    def raw_group(self):
        if self.peek() == '{':
            self.take(); depth, buf = 1, []
            while depth:
                tok = self.take()
                if tok == '{': depth += 1
                elif tok == '}': depth -= 1
                if depth: buf.append(tok)
            return buf
        return [self.take()]

    def seq(self, va, stop=None):
        out = []
        while self.peek() is not None and self.peek() != stop:
            if stop is None and self.peek() == '}':
                self.take(); continue
            out.extend(self.atom(va))
        return out

    def atom(self, va):
        tok = self.take()
        if tok is None:
            return []
        if tok == '{':
            out = self.seq(va, stop='}'); self.take(); return out
        if tok in ('^', '_'):
            nva = 'superscript' if tok == '^' else 'subscript'
            return self.group(va or nva)
        if tok == '&':
            return [('\u2003', va)]
        if tok == '\\\\':
            return [('\n', None)]
        if tok.startswith('\\'):
            name = tok[1:]
            if name in DROP:
                return []
            if name == 'frac':
                num = self.group(va); den = self.group(va)
                return wrap(num) + [('/', va)] + wrap(den)
            if name in ACCENT:
                inner = self.group(va)
                if inner:
                    txt, v = inner[-1]
                    inner[-1] = (txt + ACCENT[name], v)
                return inner
            if name == 'mathbb':
                g = ''.join(self.raw_group()); return [(BB.get(g, g), va)]
            if name == 'mathcal':
                g = ''.join(self.raw_group()); return [(CAL.get(g, g), va)]
            if name in ('operatorname', 'text', 'mathrm', 'mathbf'):
                g = self.raw_group()
                return [(' '.join(g) if name == 'text' else ''.join(g), va)]
            if name == 'begin':
                env = ''.join(self.raw_group())
                body = []
                while not (self.peek() == '\\end'):
                    body.append(self.take())
                self.take(); self.raw_group()
                inner = Parser(body).seq(va)
                if env == 'cases':
                    return [('{ ', va), ('\n', None)] + inner
                if env == 'pmatrix':
                    flat = [(t if t != '\n' else '; ', v) for t, v in inner]
                    return [('[', va)] + flat + [(']', va)]
                return inner
            if name in SYM:
                return [(SYM[name], va)]
            return [(name, va)]
        return [(tok, va)]


def wrap(runs):
    text = ''.join(t for t, _ in runs)
    if len(text) <= 1 or re.fullmatch(r'[A-Za-z0-9.]+', text):
        return runs
    va = runs[0][1] if runs else None
    return [('(', va)] + runs + [(')', va)]


def latex_runs(src):
    runs = Parser(tokenize(src)).seq(None)
    merged = []
    for t, v in runs:
        if merged and merged[-1][1] == v and t != '\n' and merged[-1][0] != '\n':
            merged[-1] = (merged[-1][0] + t, v)
        else:
            merged.append((t, v))
    return merged


def math_xml(src):
    out = []
    for t, v in latex_runs(src):
        if t == '\n':
            out.append('<w:r><w:br/></w:r>'); continue
        rpr = ('<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"'
               ' w:cs="Cambria Math"/>')
        if v:
            rpr += f'<w:vertAlign w:val="{v}"/>'
        rpr += '</w:rPr>'
        out.append(f'<w:r>{rpr}<w:t xml:space="preserve">'
                   f'{base.escape_xml(t)}</w:t></w:r>')
    return ''.join(out)


# ---------------------------------------------------------------------------
# Inline text with math, bold, italic, code
# ---------------------------------------------------------------------------

def inline_xml(text):
    parts = re.split(r'(\$[^$]+\$|`[^`]+`)', text)
    out = []
    for part in parts:
        if not part:
            continue
        if part.startswith('$') and part.endswith('$'):
            out.append(math_xml(part[1:-1]))
        elif part.startswith('`'):
            out.append('<w:r><w:rPr><w:rFonts w:ascii="Consolas" '
                       'w:hAnsi="Consolas"/></w:rPr><w:t xml:space="preserve">'
                       f'{base.escape_xml(part[1:-1])}</w:t></w:r>')
        else:
            out.append(base.parse_inline(part))
    return ''.join(out)


def paragraph(text, style='Normal'):
    return (f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
            f'{inline_xml(text)}</w:p>')


def display_eq(src):
    m = re.search(r'\\tag\{(\d+)\}', src)
    num = m.group(1) if m else None
    src = re.sub(r'\\tag\{\d+\}', '', src)
    tab = ('<w:tabs><w:tab w:val="center" w:pos="4680"/>'
           '<w:tab w:val="right" w:pos="9360"/></w:tabs>')
    xml = (f'<w:p><w:pPr>{tab}<w:spacing w:before="120" w:after="120"/>'
           '<w:jc w:val="left"/></w:pPr><w:r><w:tab/></w:r>' + math_xml(src))
    if num:
        xml += f'<w:r><w:tab/><w:t>({num})</w:t></w:r>'
    return xml + '</w:p>'


def table_xml(headers, rows):
    n = len(headers)
    col_w = 9360 // n
    borders = ''.join(
        f'<w:{e} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
    tbl = ('<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
           '<w:tblW w:w="9360" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
           f'<w:tblBorders>{borders}</w:tblBorders></w:tblPr>'
           '<w:tblGrid>' + f'<w:gridCol w:w="{col_w}"/>' * n + '</w:tblGrid>')

    def cell(txt, head=False):
        shade = ('<w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>'
                 '</w:tcPr>') if head else ''
        body = inline_xml(f'**{txt}**' if head else txt)
        return (f'<w:tc>{shade}<w:p><w:pPr><w:spacing w:after="20" '
                f'w:line="240" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>'
                f'{body}</w:p></w:tc>')
    tbl += '<w:tr>' + ''.join(cell(h, True) for h in headers) + '</w:tr>'
    for r in rows:
        r = r + [''] * (n - len(r))
        tbl += '<w:tr>' + ''.join(cell(c) for c in r[:n]) + '</w:tr>'
    return tbl + '</w:tbl>'


def split_row(line):
    cells = line.strip().strip('|').split('|')
    return [c.strip() for c in cells]


def md_to_body(md, image_rels):
    el, lines, i, refs, img = [], md.split('\n'), 0, False, 0
    while i < len(lines):
        line = lines[i]
        st = line.strip()
        if not st or st == '---':
            i += 1; continue
        if st.startswith('$$'):
            buf = st
            while not (buf.endswith('$$') and len(buf) > 2):
                i += 1; buf += ' ' + lines[i].strip()
            el.append(display_eq(buf[2:-2])); i += 1; continue
        if line.startswith('# '):
            el.append(paragraph(line[2:].strip(), 'Title')); i += 1; continue
        if line.startswith('## '):
            h = line[3:].strip(); refs = h == 'References'
            el.append(paragraph(h, 'Heading1')); i += 1; continue
        if line.startswith('### '):
            el.append(paragraph(line[4:].strip(), 'Heading2')); i += 1; continue
        if st.startswith('|') and i + 1 < len(lines) and \
                re.match(r'^\|[-| ]+\|$', lines[i + 1].strip()):
            headers = split_row(st); i += 2; rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append(split_row(lines[i])); i += 1
            el.append(table_xml(headers, rows)); continue
        m = re.match(r'!\[[^\]]*\]\(([^)]+)\)', st)
        if m:
            path = os.path.join(HERE, m.group(1))
            img += 1
            rel = f'rIdImg{img}'
            fname = os.path.basename(path)
            image_rels.append((rel, fname, path))
            w, h = base.png_dimensions(path)
            cx = int(6.3 * base.EMU_PER_INCH); cy = int(cx * h / w)
            el.append(base.make_image_paragraph(rel, img, cx, cy, fname))
            i += 1; continue
        if re.match(r'^Figure \d+\.', st):
            el.append(paragraph(st, 'FigureCaption')); i += 1; continue
        if re.match(r'^Table \d+\.', st):
            el.append(paragraph(st, 'TableCaption')); i += 1; continue
        if refs and re.match(r'^\[\d+\]', st):
            el.append(paragraph(st, 'References')); i += 1; continue
        if re.match(r'^\d+\. ', st):
            el.append(paragraph(st, 'Normal')); i += 1; continue
        el.append(paragraph(st, 'Normal')); i += 1
    return '\n'.join(el)


def main():
    md = open(MD_FILE, encoding='utf-8').read()
    image_rels = []
    body = md_to_body(md, image_rels)
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/'
           'wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats'
           '.org/officeDocument/2006/relationships"><w:body>' + body +
           '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" '
           'w:right="1440" w:bottom="1440" w:left="1440" w:header="720" '
           'w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>')
    rels = base.build_word_rels([(r, f) for r, f, _ in image_rels])
    with zipfile.ZipFile(DOCX_FILE, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', base.CONTENT_TYPES)
        z.writestr('_rels/.rels', base.RELS)
        z.writestr('word/_rels/document.xml.rels', rels)
        z.writestr('word/document.xml', doc)
        z.writestr('word/styles.xml', base.STYLES)
        z.writestr('word/numbering.xml', base.NUMBERING)
        for _, fname, path in image_rels:
            z.write(path, f'word/media/{fname}')
    print(f'Created {DOCX_FILE} with {len(image_rels)} figures, '
          f'{os.path.getsize(DOCX_FILE) / 1024:.1f} KB')


if __name__ == '__main__':
    main()
