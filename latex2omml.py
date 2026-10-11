#!/usr/bin/env python3
"""
Minimal LaTeX -> OMML (Office Math Markup Language) converter.

Produces the *inner* OMML for a math zone (to be wrapped in <m:oMath>...).
Covers the LaTeX subset used by the TEHD article: \frac \dfrac \sqrt, super/
subscripts, \left \right and \big-family delimiters, Greek letters, operators,
\bar accents, \mathrm \text \mathbf \boldsymbol, \begin{cases}, functions, and
spacing commands. Unknown commands are skipped gracefully.

Pure standard library. Run directly to self-test against the article equations.
"""

import re

M = 'm:'  # namespace prefix (declared on the document root)

GREEK = {
    'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'Delta': 'Δ',
    'varepsilon': 'ε', 'epsilon': 'ε', 'theta': 'θ', 'Theta': 'Θ',
    'lambda': 'λ', 'Lambda': 'Λ', 'mu': 'μ', 'nu': 'ν', 'pi': 'π', 'Pi': 'Π',
    'rho': 'ρ', 'sigma': 'σ', 'Sigma': 'Σ', 'tau': 'τ', 'phi': 'φ', 'Phi': 'Φ',
    'omega': 'ω', 'Omega': 'Ω', 'eta': 'η', 'kappa': 'κ', 'xi': 'ξ',
}
SYM = {
    'partial': '∂', 'nabla': '∇', 'infty': '∞', 'times': '×', 'cdot': '·',
    'pm': '±', 'mp': '∓', 'ge': '≥', 'geq': '≥', 'le': '≤', 'leq': '≤',
    'neq': '≠', 'approx': '≈', 'equiv': '≡', 'propto': '∝', 'to': '→',
    'leftarrow': '←', 'rightarrow': '→', 'll': '≪', 'gg': '≫', 'in': '∈',
    'int': '∫', 'iint': '∬', 'iiint': '∭', 'oint': '∮', 'sum': '∑', 'prod': '∏',
    'c‌dot': '·',
}
FUNCS = {'sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'exp', 'ln', 'log',
         'arctan', 'arcsin', 'arccos', 'max', 'min', 'lim', 'sinh', 'cosh', 'tanh'}
SPACES = {'quad': '  ', 'qquad': '    ', ',': ' ', ';': ' ', ':': ' ', '!': '',
          ' ': ' '}
DELIM = {'(': '(', ')': ')', '[': '[', ']': ']', '|': '|', '.': '',
         '{': '{', '}': '}', 'lbrace': '{', 'rbrace': '}', 'langle': '⟨',
         'rangle': '⟩', 'vert': '|', 'Vert': '‖'}


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def run(text, sty=None):
    if text == '':
        return ''
    rpr = ''
    if sty:
        rpr = f'<{M}rPr><{M}sty {M}val="{sty}"/></{M}rPr>'
    return f'<{M}r>{rpr}<{M}t xml:space="preserve">{esc(text)}</{M}t></{M}r>'


def ele(tag, inner):
    return f'<{M}{tag}>{inner}</{M}{tag}>'


def tokenize(s):
    toks, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == '\\':
            j = i + 1
            if j < n and s[j].isalpha():
                k = j
                while k < n and s[k].isalpha():
                    k += 1
                toks.append(('cmd', s[j:k]))
                i = k
            elif j < n:
                toks.append(('cmd', s[j]))  # \{ \} \, \; \! \\ \| etc.
                i = j + 1
            else:
                i = j
        elif c == '{':
            toks.append(('lb', '{')); i += 1
        elif c == '}':
            toks.append(('rb', '}')); i += 1
        elif c == '^':
            toks.append(('sup', '^')); i += 1
        elif c == '_':
            toks.append(('sub', '_')); i += 1
        elif c == '&':
            toks.append(('amp', '&')); i += 1
        elif c in ' \t\n':
            i += 1
        else:
            toks.append(('chr', c)); i += 1
    return toks


class Parser:
    def __init__(self, toks):
        self.t = toks
        self.i = 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def next(self):
        tok = self.peek(); self.i += 1
        return tok

    # parse a sequence until stop(token) true or end
    def sequence(self, stop):
        out = []
        while self.i < len(self.t):
            if stop(self.peek()):
                break
            out.append(self.atom_scripts())
        return ''.join(out)

    def group_or_atom(self):
        """Read one braced group or a single atom (no scripts)."""
        if self.peek()[0] == 'lb':
            self.next()
            inner = self.sequence(lambda tk: tk[0] == 'rb')
            if self.peek()[0] == 'rb':
                self.next()
            return inner
        return self.atom()

    def raw_group(self):
        """Read a braced group as a plain string (env names)."""
        s = ''
        if self.peek()[0] == 'lb':
            self.next()
            while self.i < len(self.t) and self.peek()[0] != 'rb':
                ty, v = self.next()
                s += v
            if self.peek()[0] == 'rb':
                self.next()
        return s

    def atom_scripts(self):
        base = self.atom()
        sub = sup = None
        # allow sub then sup, or sup then sub
        for _ in range(2):
            ty = self.peek()[0]
            if ty == 'sub' and sub is None:
                self.next(); sub = self.group_or_atom()
            elif ty == 'sup' and sup is None:
                self.next(); sup = self.group_or_atom()
            else:
                break
        if sub is not None and sup is not None:
            return ele('sSubSup', ele('e', base) + ele('sub', sub) + ele('sup', sup))
        if sub is not None:
            return ele('sSub', ele('e', base) + ele('sub', sub))
        if sup is not None:
            return ele('sSup', ele('e', base) + ele('sup', sup))
        return base

    def delim(self, tok):
        ty, v = tok
        if ty == 'cmd':
            return DELIM.get(v, '')
        if ty == 'chr':
            return DELIM.get(v, v)
        return ''

    def atom(self):
        ty, v = self.next()
        if ty == 'lb':
            inner = self.sequence(lambda tk: tk[0] == 'rb')
            if self.peek()[0] == 'rb':
                self.next()
            return inner
        if ty == 'chr':
            return run(v)
        if ty == 'amp':
            return run('  ')
        if ty == 'sup' or ty == 'sub':
            return ''  # stray
        if ty == 'cmd':
            return self.command(v)
        return ''

    def command(self, name):
        # spacing
        if name in SPACES:
            return run(SPACES[name]) if SPACES[name] else ''
        if name == '\\':  # line break
            return run('  ')
        # fractions
        if name in ('frac', 'dfrac', 'tfrac'):
            num = self.group_or_atom()
            den = self.group_or_atom()
            return ele('f', ele('num', num) + ele('den', den))
        # radical
        if name == 'sqrt':
            deg = ''
            if self.peek() == ('chr', '['):
                # optional [n]
                self.next()
                buf = ''
                while self.i < len(self.t) and self.peek() != ('chr', ']'):
                    buf += self.next()[1]
                if self.peek() == ('chr', ']'):
                    self.next()
                deg = run(buf)
            e = self.group_or_atom()
            if deg:
                return ele('rad', ele('deg', deg) + ele('e', e))
            return ele('rad', f'<{M}radPr><{M}degHide {M}val="1"/></{M}radPr>'
                       + ele('deg', '') + ele('e', e))
        # accents
        if name == 'bar':
            e = self.group_or_atom()
            return ele('acc', f'<{M}accPr><{M}chr {M}val="\u0304"/></{M}accPr>'
                       + ele('e', e))
        if name in ('hat', 'tilde', 'vec', 'dot', 'ddot'):
            ch = {'hat': '\u0302', 'tilde': '\u0303', 'vec': '\u20d7',
                  'dot': '\u0307', 'ddot': '\u0308'}[name]
            e = self.group_or_atom()
            return ele('acc', f'<{M}accPr><{M}chr {M}val="{ch}"/></{M}accPr>'
                       + ele('e', e))
        # upright / bold text wrappers
        if name in ('mathrm', 'text', 'textrm', 'mathsf', 'operatorname'):
            return self.styled(self.group_or_atom(), 'p')
        if name in ('mathbf', 'boldsymbol', 'bm'):
            return self.styled(self.group_or_atom(), 'b')
        if name in ('mathit',):
            return self.group_or_atom()
        # delimiters
        if name == 'left':
            beg = self.delim(self.next())
            inner = self.sequence(lambda tk: tk == ('cmd', 'right'))
            if self.peek() == ('cmd', 'right'):
                self.next()
                end = self.delim(self.next())
            else:
                end = ''
            dpr = (f'<{M}dPr><{M}begChr {M}val="{beg}"/>'
                   f'<{M}endChr {M}val="{end}"/></{M}dPr>')
            return ele('d', dpr + ele('e', inner))
        if name.startswith('big') or name.startswith('Big'):
            return ''  # size hint; following delimiter becomes a normal char
        # environments
        if name == 'begin':
            env = self.raw_group()
            return self.environment(env)
        if name == 'end':
            self.raw_group()
            return ''
        # greek / symbols / functions
        if name in GREEK:
            return run(GREEK[name])
        if name in SYM:
            return run(SYM[name])
        if name in FUNCS:
            return run(name, sty='p')
        # unknown -> skip
        return ''

    def styled(self, inner, sty):
        # wrap plain-text content; if it is a single run, restyle; else prepend style
        m = re.match(r'^<%sr>(?:<%srPr>.*?</%srPr>)?<%st xml:space="preserve">(.*?)</%st></%sr>$'
                     % (M, M, M, M, M, M), inner, re.S)
        if m:
            return run(m.group(1), sty=sty)
        return inner  # structured content: leave as-is

    def environment(self, env):
        # collect tokens until matching \end{...}
        depth = 1
        buf = []
        while self.i < len(self.t):
            tok = self.peek()
            if tok == ('cmd', 'begin'):
                depth += 1; buf.append(self.next()); buf.append(('_rawgrp', self.raw_group()))
                continue
            if tok == ('cmd', 'end'):
                self.next(); self.raw_group(); depth -= 1
                if depth == 0:
                    break
                continue
            buf.append(self.next())
        # split into rows on '\\'
        rows, cur = [], []
        for tok in buf:
            if tok == ('cmd', '\\'):
                rows.append(cur); cur = []
            else:
                cur.append(tok)
        rows.append(cur)
        row_xml = []
        for row in rows:
            # split cells on &
            cells, cell = [], []
            for tok in row:
                if tok[0] == 'amp':
                    cells.append(cell); cell = []
                else:
                    cell.append(tok)
            cells.append(cell)
            parts = []
            for ci, cell in enumerate(cells):
                sub = Parser(cell)
                parts.append(sub.sequence(lambda tk: False))
                if ci < len(cells) - 1:
                    parts.append(run('   '))
            row_xml.append(ele('e', ''.join(parts)))
        eqarr = ele('eqArr', ''.join(row_xml))
        if env in ('cases',):
            dpr = (f'<{M}dPr><{M}begChr {M}val="{{"/>'
                   f'<{M}endChr {M}val=""/></{M}dPr>')
            return ele('d', dpr + ele('e', eqarr))
        if env in ('matrix', 'array', 'aligned', 'bmatrix', 'pmatrix'):
            return eqarr
        return eqarr


def latex_to_omml(latex):
    """Return inner OMML for the given LaTeX math string."""
    toks = tokenize(latex)
    p = Parser(toks)
    return p.sequence(lambda tk: False)


# ----------------------------------------------------------------- self-test
if __name__ == '__main__':
    import xml.dom.minidom as minidom

    SRC = '/projects/sandbox/AMMAN/Research_Article_TEHD_Journal_Bearing.md'
    with open(SRC) as f:
        md = f.read()

    # display equations
    disp = []
    lines = md.split('\n')
    i = 0
    while i < len(lines):
        if lines[i].strip() == '$$':
            j = i + 1; buf = []
            while j < len(lines) and lines[j].strip() != '$$':
                buf.append(lines[j]); j += 1
            blob = ' '.join(x.strip() for x in buf)
            blob = re.sub(r'\\tag\{\d+\}', '', blob)
            disp.append(blob)
            i = j + 1
        else:
            i += 1
    inline = re.findall(r'(?<!\$)\$([^$]+)\$', md)

    root_open = ('<root xmlns:m="http://schemas.openxmlformats.org/'
                 'officeDocument/2006/math">')
    ok = bad = 0
    for kind, items in (('display', disp), ('inline', inline)):
        for e in items:
            try:
                omml = latex_to_omml(e)
                minidom.parseString(root_open + omml + '</root>')
                ok += 1
            except Exception as ex:
                bad += 1
                print(f'  [FAIL {kind}] {e[:60]!r}: {ex}')
    print(f'display={len(disp)} inline={len(inline)}  parsed OK={ok} FAIL={bad}')
