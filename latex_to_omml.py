#!/usr/bin/env python3
"""
Minimal LaTeX -> OMML (Office Math Markup Language) converter.

Produces Word-native, *editable* equation objects (the same markup Word writes
when you use Insert > Equation). Tailored to the LaTeX constructs used in the
entropy-EMHD-squeezing-Carreau manuscript: fractions, sub/superscripts,
radicals, \\left..\\right and \\Big.. delimiters, n-ary integrals/sums,
\\underbrace, \\begin{aligned} equation arrays, Greek letters and operators.

Pure standard library. If an equation cannot be parsed, callers should fall
back to a plain-text paragraph.
"""

import re

MATH_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
DOUBLE_BS = chr(92) * 2  # "\\"

# --- symbol tables -------------------------------------------------------
GREEK = {
    'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'Gamma': 'Γ', 'delta': 'δ',
    'Delta': 'Δ', 'epsilon': 'ϵ', 'varepsilon': 'ε', 'zeta': 'ζ', 'eta': 'η',
    'theta': 'θ', 'Theta': 'Θ', 'kappa': 'κ', 'lambda': 'λ', 'Lambda': 'Λ',
    'mu': 'μ', 'nu': 'ν', 'xi': 'ξ', 'Xi': 'Ξ', 'pi': 'π', 'Pi': 'Π',
    'rho': 'ρ', 'sigma': 'σ', 'Sigma': 'Σ', 'tau': 'τ', 'phi': 'φ',
    'varphi': 'φ', 'Phi': 'Φ', 'chi': 'χ', 'psi': 'ψ', 'Psi': 'Ψ',
    'omega': 'ω', 'Omega': 'Ω',
}
OPERATORS = {
    'times': '×', 'cdot': '⋅', 'le': '≤', 'leq': '≤', 'ge': '≥', 'geq': '≥',
    'to': '→', 'approx': '≈', 'pm': '±', 'mp': '∓', 'infty': '∞',
    'partial': '∂', 'nabla': '∇', 'ldots': '…', 'cdots': '⋯', 'neq': '≠',
    'equiv': '≡', 'propto': '∝', 'in': '∈', 'ast': '∗',
}
FUNCS = {'ln', 'log', 'sin', 'cos', 'tan', 'exp', 'max', 'min', 'lim', 'tr'}
SPACES = {',': ' ', ';': ' ', ':': ' ', '!': '', 'quad': '  ', 'qquad': '    ',
          ' ': ' '}


def _esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


# --- AST nodes -----------------------------------------------------------
class Run:
    def __init__(self, text, roman=False):
        self.text, self.roman = text, roman


class Group:
    def __init__(self, nodes):
        self.nodes = nodes


class Frac:
    def __init__(self, num, den):
        self.num, self.den = num, den


class Script:
    def __init__(self, base, sub=None, sup=None):
        self.base, self.sub, self.sup = base, sub, sup


class Rad:
    def __init__(self, radicand, deg=None):
        self.radicand, self.deg = radicand, deg


class Delim:
    def __init__(self, opn, close, content):
        self.opn, self.close, self.content = opn, close, content


class Nary:
    def __init__(self, op):
        self.op, self.sub, self.sup, self.body = op, [], [], []


class UnderBrace:
    def __init__(self, content, label):
        self.content, self.label = content, label


# --- tokenizer -----------------------------------------------------------
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
            else:
                toks.append(('cmd', s[j] if j < n else ''))
                i = j + 1
        elif c in '{}^_&':
            toks.append(('ctrl', c))
            i += 1
        elif c.isspace():
            toks.append(('space', ' '))
            i += 1
        else:
            toks.append(('char', c))
            i += 1
    return toks


# --- parser --------------------------------------------------------------
class Parser:
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def nxt(self):
        tok = self.t[self.i]
        self.i += 1
        return tok

    def parse_seq(self, until_brace):
        nodes = []
        while True:
            typ, val = self.peek()
            if typ is None:
                break
            if typ == 'ctrl' and val == '}':
                if until_brace:
                    break
                self.nxt()
                continue
            if typ == 'space':
                self.nxt()
                continue
            if typ == 'ctrl' and val in ('^', '_'):
                base = nodes.pop() if nodes else Run('')
                nodes.append(self.parse_scripts(base))
                continue
            if typ == 'ctrl' and val == '&':
                self.nxt()
                continue
            if typ == 'cmd' and val == 'right':
                break  # handled by delimiter parser
            atom = self.parse_atom()
            if atom is None:
                continue
            # n-ary operators consume the remainder of the sequence as body
            if isinstance(atom, Nary):
                rest = self.parse_seq(until_brace)
                atom.body = rest
                nodes.append(atom)
                break
            nodes.append(atom)
        return nodes

    def parse_scripts(self, base):
        sub = sup = None
        while True:
            typ, val = self.peek()
            if typ == 'ctrl' and val in ('^', '_'):
                self.nxt()
                arg = self.parse_script_arg()
                if val == '_':
                    sub = arg
                else:
                    sup = arg
            else:
                break
        return Script(base, sub, sup)

    def parse_script_arg(self):
        typ, val = self.peek()
        if typ == 'ctrl' and val == '{':
            self.nxt()
            seq = self.parse_seq(True)
            if self.peek()[1] == '}':
                self.nxt()
            return Group(seq)
        return self.parse_atom()

    def read_delim(self):
        typ, val = self.nxt()
        if typ == 'cmd':
            m = {'{': '{', '}': '}', '|': '|', '.': '', 'langle': '⟨',
                 'rangle': '⟩', 'lvert': '|', 'rvert': '|', 'Vert': '‖'}
            return m.get(val, '')
        if typ == 'char':
            return '' if val == '.' else val
        return ''

    def parse_atom(self):
        typ, val = self.nxt()
        if typ == 'ctrl' and val == '{':
            seq = self.parse_seq(True)
            if self.peek()[1] == '}':
                self.nxt()
            return Group(seq)
        if typ == 'char':
            ch = '′' if val == "'" else val
            return Run(ch)
        if typ == 'space':
            return Run(' ')
        if typ == 'cmd':
            return self.dispatch(val)
        return Run('')

    def dispatch(self, name):
        if name == 'frac' or name == 'dfrac' or name == 'tfrac':
            num = self.req_group()
            den = self.req_group()
            return Frac(num, den)
        if name == 'sqrt':
            rad = self.req_group()
            return Rad(rad)
        if name in ('left',):
            opn = self.read_delim()
            inner = self.parse_seq(False)
            close = ''
            if self.peek() == ('cmd', 'right'):
                self.nxt()
                close = self.read_delim()
            return Delim(opn, close, Group(inner))
        if name == 'underbrace':
            content = self.req_group()
            label = None
            if self.peek() == ('ctrl', '_'):
                self.nxt()
                label = self.parse_script_arg()
            return UnderBrace(content, label)
        if name in ('int', 'iint', 'oint'):
            nn = Nary('∫')
            self._nary_limits(nn)
            return nn
        if name == 'sum':
            nn = Nary('∑')
            self._nary_limits(nn)
            return nn
        if name == 'prod':
            nn = Nary('∏')
            self._nary_limits(nn)
            return nn
        if name in ('mathrm', 'text', 'operatorname', 'mathbf', 'mathit',
                    'mathsf', 'boldsymbol', 'mathcal', 'mathbb', 'mathscr'):
            g = self.req_group()
            return Group([Run(_flatten_text(g), roman=(name in (
                'mathrm', 'text', 'operatorname', 'mathsf')))])
        if name == 'displaystyle' or name == 'limits' or name == 'nolimits':
            return Run('')
        if name in GREEK:
            return Run(GREEK[name])
        if name in OPERATORS:
            return Run(OPERATORS[name])
        if name in FUNCS:
            return Run(name, roman=True)
        if name in SPACES:
            return Run(SPACES[name])
        if name == DOUBLE_BS[0] or name == '':
            return Run(' ')
        # unknown command: emit its name so nothing is silently lost
        return Run(name, roman=True)

    def _nary_limits(self, nn):
        while True:
            typ, val = self.peek()
            if typ == 'ctrl' and val in ('^', '_'):
                self.nxt()
                arg = self.parse_script_arg()
                if val == '_':
                    nn.sub = [arg]
                else:
                    nn.sup = [arg]
            else:
                break

    def req_group(self):
        typ, val = self.peek()
        if typ == 'ctrl' and val == '{':
            self.nxt()
            seq = self.parse_seq(True)
            if self.peek()[1] == '}':
                self.nxt()
            return seq
        return [self.parse_atom()]


def _flatten_text(nodes):
    out = []
    for nd in nodes:
        if isinstance(nd, Run):
            out.append(nd.text)
        elif isinstance(nd, Group):
            out.append(_flatten_text(nd.nodes))
        elif isinstance(nd, Script):
            out.append(_flatten_text([nd.base]))
    return ''.join(out)


# --- emitter -------------------------------------------------------------
def emit(node):
    if isinstance(node, Run):
        if node.text == '':
            return ''
        rpr = '<m:rPr><m:sty m:val="p"/></m:rPr>' if node.roman else ''
        return f'<m:r>{rpr}<m:t xml:space="preserve">{_esc(node.text)}</m:t></m:r>'
    if isinstance(node, Group):
        return emit_seq(node.nodes)
    if isinstance(node, Frac):
        return ('<m:f><m:fPr><m:type m:val="bar"/></m:fPr>'
                f'<m:num>{emit_seq(node.num)}</m:num>'
                f'<m:den>{emit_seq(node.den)}</m:den></m:f>')
    if isinstance(node, Script):
        base = emit(node.base) or '<m:r><m:t></m:t></m:r>'
        if node.sub is not None and node.sup is not None:
            return (f'<m:sSubSup><m:e>{base}</m:e>'
                    f'<m:sub>{emit(node.sub)}</m:sub>'
                    f'<m:sup>{emit(node.sup)}</m:sup></m:sSubSup>')
        if node.sub is not None:
            return (f'<m:sSub><m:e>{base}</m:e>'
                    f'<m:sub>{emit(node.sub)}</m:sub></m:sSub>')
        return (f'<m:sSup><m:e>{base}</m:e>'
                f'<m:sup>{emit(node.sup)}</m:sup></m:sSup>')
    if isinstance(node, Rad):
        if node.deg is None:
            return ('<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr>'
                    f'<m:deg/><m:e>{emit_seq(node.radicand)}</m:e></m:rad>')
        return (f'<m:rad><m:deg>{emit_seq(node.deg)}</m:deg>'
                f'<m:e>{emit_seq(node.radicand)}</m:e></m:rad>')
    if isinstance(node, Delim):
        beg = _esc(node.opn)
        end = _esc(node.close)
        return ('<m:d><m:dPr>'
                f'<m:begChr m:val="{beg}"/><m:endChr m:val="{end}"/>'
                '<m:grow m:val="1"/></m:dPr>'
                f'<m:e>{emit(node.content)}</m:e></m:d>')
    if isinstance(node, Nary):
        chr_attr = f'<m:chr m:val="{node.op}"/>' if node.op != '∫' else ''
        sub_hide = '' if node.sub else '<m:subHide m:val="1"/>'
        sup_hide = '' if node.sup else '<m:supHide m:val="1"/>'
        return ('<m:nary><m:naryPr>' + chr_attr +
                '<m:limLoc m:val="subSup"/>' + sub_hide + sup_hide +
                '</m:naryPr>'
                f'<m:sub>{emit_seq(node.sub)}</m:sub>'
                f'<m:sup>{emit_seq(node.sup)}</m:sup>'
                f'<m:e>{emit_seq(node.body)}</m:e></m:nary>')
    if isinstance(node, UnderBrace):
        inner = emit_seq(node.content)
        grp = ('<m:groupChr><m:groupChrPr><m:chr m:val="⏟"/>'
               '<m:pos m:val="bot"/><m:vertJc m:val="top"/></m:groupChrPr>'
               f'<m:e>{inner}</m:e></m:groupChr>')
        lab = emit(node.label) if node.label is not None else ''
        return ('<m:limLow><m:limLowPr/>'
                f'<m:e>{grp}</m:e><m:lim>{lab}</m:lim></m:limLow>')
    return ''


def emit_seq(nodes):
    return ''.join(emit(n) for n in nodes)


# --- preprocessing -------------------------------------------------------
def _preprocess(s):
    # Convert \Big[ \bigg( etc. into \left / \right delimiters.
    sizers = r'(?:Bigg|bigg|Big|big|Bigl|Bigr|bigl|bigr|Biggl|Biggr)'
    s = re.sub(r'\\' + sizers + r'\s*([\[\(\{])', r'\\left\1', s)
    s = re.sub(r'\\' + sizers + r'\s*([\]\)\}])', r'\\right\1', s)
    s = re.sub(r'\\' + sizers + r'\s*\\\{', r'\\left\\{', s)
    s = re.sub(r'\\' + sizers + r'\s*\\\}', r'\\right\\}', s)
    return s


def _parse(latex):
    toks = tokenize(_preprocess(latex))
    return Parser(toks).parse_seq(False)


# --- public API ----------------------------------------------------------
def latex_to_omath(latex):
    """Return an <m:oMath> ... </m:oMath> string for a single LaTeX equation."""
    latex = latex.strip()
    latex = re.sub(r'\\tag\{[0-9]+\}', '', latex)

    m = re.search(r'\\begin\{aligned\}(.*)\\end\{aligned\}', latex, re.S)
    if m:
        inner = m.group(1)
        rows = inner.split(DOUBLE_BS)
        cells = []
        for r in rows:
            r = r.replace('&', '').strip()
            if not r:
                continue
            cells.append(f'<m:e>{emit_seq(_parse(r))}</m:e>')
        body = f'<m:eqArr>{"".join(cells)}</m:eqArr>'
    else:
        body = emit_seq(_parse(latex))
    return f'<m:oMath>{body}</m:oMath>'


def equation_paragraph(latex, tag=None):
    """Full <w:p> with an inline editable equation and a right-aligned number."""
    omath = latex_to_omath(latex)
    num = f'({tag})' if tag else ''
    tabs = '<w:tabs><w:tab w:val="right" w:pos="9350"/></w:tabs>'
    numrun = (f'<w:r><w:tab/><w:t xml:space="preserve">{_esc(num)}</w:t></w:r>'
              if num else '')
    return (f'<w:p><w:pPr>{tabs}'
            '<w:spacing w:before="80" w:after="80"/></w:pPr>'
            f'{omath}{numrun}</w:p>')


if __name__ == '__main__':
    tests = [
        r'\mu(\dot{\gamma}) = \mu_0\left[1 + (\Gamma\dot{\gamma})^2\right]^{\frac{n-1}{2}}. \tag{6}',
        r'N_{s,\text{avg}} = \int_0^1 N_s(\eta)\,\mathrm{d}\eta. \tag{70}',
        r'\eta = \frac{y}{h(t)}, \qquad \psi = \left[\frac{a\nu_f}{1-\gamma t}\right]^{1/2}x\,f(\eta). \tag{22}',
    ]
    for t in tests:
        print(equation_paragraph(t, re.search(r'\\tag\{([0-9]+)\}', t).group(1)))
        print('---')
