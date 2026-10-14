#!/usr/bin/env python3
"""
Minimal LaTeX -> OMML (Office Math Markup Language) converter.

Covers the constructs used in the CKD manuscript equations:
fractions, roots, sub/superscripts, n-ary operators (sum/prod/int) with
limits, accents (hat/bar/tilde/vec/dot), aligned environments, Greek
letters, operators/relations, function names, \text, \mathbf/\mathcal/
\mathbb, delimiters, spacing. Produces OMML that Microsoft Word renders
as native, editable equations.

Output is the inner content of an <m:oMath> element (caller wraps it).
"""

import re

M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

GREEK = {
    'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε',
    'varepsilon': 'ε', 'zeta': 'ζ', 'eta': 'η', 'theta': 'θ', 'vartheta': 'ϑ',
    'iota': 'ι', 'kappa': 'κ', 'lambda': 'λ', 'mu': 'μ', 'nu': 'ν', 'xi': 'ξ',
    'pi': 'π', 'varpi': 'ϖ', 'rho': 'ρ', 'varrho': 'ϱ', 'sigma': 'σ',
    'varsigma': 'ς', 'tau': 'τ', 'upsilon': 'υ', 'phi': 'φ', 'varphi': 'φ',
    'chi': 'χ', 'psi': 'ψ', 'omega': 'ω',
    'Gamma': 'Γ', 'Delta': 'Δ', 'Theta': 'Θ', 'Lambda': 'Λ', 'Xi': 'Ξ',
    'Pi': 'Π', 'Sigma': 'Σ', 'Upsilon': 'Υ', 'Phi': 'Φ', 'Psi': 'Ψ', 'Omega': 'Ω',
}

SYMBOLS = {
    'times': '×', 'cdot': '⋅', 'div': '÷', 'pm': '±', 'mp': '∓',
    'le': '≤', 'leq': '≤', 'ge': '≥', 'geq': '≥', 'neq': '≠', 'ne': '≠',
    'approx': '≈', 'equiv': '≡', 'sim': '∼', 'propto': '∝', 'infty': '∞',
    'partial': '∂', 'nabla': '∇', 'in': '∈', 'notin': '∉', 'ni': '∋',
    'subset': '⊂', 'subseteq': '⊆', 'supset': '⊃', 'supseteq': '⊇',
    'cup': '∪', 'cap': '∩', 'emptyset': '∅', 'forall': '∀', 'exists': '∃',
    'lor': '∨', 'vee': '∨', 'land': '∧', 'wedge': '∧', 'neg': '¬',
    'odot': '⊙', 'otimes': '⊗', 'oplus': '⊕', 'circ': '∘', 'bullet': '•',
    'star': '⋆', 'ast': '∗', 'cdots': '⋯', 'ldots': '…', 'dots': '…',
    'vdots': '⋮', 'ddots': '⋱', 'rightarrow': '→', 'to': '→', 'gets': '←',
    'leftarrow': '←', 'Rightarrow': '⇒', 'Leftarrow': '⇐', 'mapsto': '↦',
    'uparrow': '↑', 'downarrow': '↓', 'langle': '⟨', 'rangle': '⟩',
    'mid': '|', 'parallel': '∥', 'perp': '⊥', 'angle': '∠', 'prime': '′',
    'nabla': '∇', 'ell': 'ℓ', 'Re': 'ℜ', 'Im': 'ℑ', 'top': '⊤', 'bot': '⊥',
    'leq': '≤', 'geq': '≥', 'll': '≪', 'gg': '≫', 'subseteq': '⊆',
}

FUNCS = {'min', 'max', 'exp', 'log', 'ln', 'lg', 'sin', 'cos', 'tan', 'cot',
         'sec', 'csc', 'sinh', 'cosh', 'tanh', 'coth', 'det', 'dim', 'arg',
         'lim', 'limsup', 'liminf', 'sup', 'inf', 'gcd', 'deg', 'Pr', 'sgn',
         'mod', 'ker', 'hom', 'max', 'min'}

NARY = {'sum': ('∑', 'undOvr'), 'prod': ('∏', 'undOvr'), 'coprod': ('∐', 'undOvr'),
        'bigcup': ('⋃', 'undOvr'), 'bigcap': ('⋂', 'undOvr'),
        'bigoplus': ('⨁', 'undOvr'), 'bigotimes': ('⨂', 'undOvr'),
        'int': ('∫', 'subSup'), 'iint': ('∬', 'subSup'), 'oint': ('∮', 'subSup')}

ACCENTS = {'hat': '̂', 'widehat': '̂', 'bar': '̄', 'overline': '̄',
           'tilde': '̃', 'widetilde': '̃', 'vec': '⃗', 'dot': '̇', 'ddot': '̈'}

FONT_CMDS = {'mathbf', 'mathrm', 'mathcal', 'mathbb', 'mathsf', 'mathit',
             'boldsymbol', 'bm', 'operatorname'}

SPACING = {',', ';', '!', ':', ' ', 'quad', 'qquad', 'thinspace', 'medspace',
           'enspace', 'hspace'}


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;'))


def mr(text, upright=False):
    if text == '':
        return ''
    rpr = '<m:rPr><m:sty m:val="p"/></m:rPr>' if upright else ''
    return f'<m:r>{rpr}<m:t xml:space="preserve">{esc(text)}</m:t></m:r>'


# -------------------------------------------------------------- tokenizer
def tokenize(s):
    toks = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c == '\\':
            if i + 1 < n and s[i + 1] == '\\':
                toks.append(('rowbreak',)); i += 2; continue
            j = i + 1
            if j < n and s[j].isalpha():
                k = j
                while k < n and s[k].isalpha():
                    k += 1
                toks.append(('cmd', s[j:k])); i = k; continue
            else:
                toks.append(('cmd', s[j] if j < n else '')); i = j + 1; continue
        if c in '{}^_&':
            toks.append((c,)); i += 1; continue
        toks.append(('char', c)); i += 1
    return toks


class TS:
    def __init__(self, toks):
        self.t = toks
        self.i = 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def next(self):
        t = self.peek()
        if t is not None:
            self.i += 1
        return t


# -------------------------------------------------------------- parser
def read_group_raw(ts):
    out = ''
    if ts.peek() and ts.peek()[0] == '{':
        ts.next()
        depth = 1
        while ts.peek() is not None:
            t = ts.next()
            if t[0] == '{':
                depth += 1; out += '{'
            elif t[0] == '}':
                depth -= 1
                if depth == 0:
                    break
                out += '}'
            elif t[0] == 'char':
                out += t[1]
            elif t[0] == 'cmd':
                out += '\\' + t[1]
            elif t[0] in ('^', '_', '&'):
                out += t[0]
    return out


def parse_group_or_atom(ts):
    p = ts.peek()
    if p and p[0] == '{':
        ts.next()
        inner = parse_seq(ts, closing=True)
        return inner
    return parse_atom(ts)


def make_script(base, sub, sup):
    b = f'<m:e>{base}</m:e>'
    if sub is not None and sup is not None:
        return f'<m:sSubSup>{b}<m:sub>{sub}</m:sub><m:sup>{sup}</m:sup></m:sSubSup>'
    if sub is not None:
        return f'<m:sSub>{b}<m:sub>{sub}</m:sub></m:sSub>'
    return f'<m:sSup>{b}<m:sup>{sup}</m:sup></m:sSup>'


def nary(chop, limloc, sub, sup):
    subhide = '0' if sub is not None else '1'
    suphide = '0' if sup is not None else '1'
    subx = f'<m:sub>{sub}</m:sub>' if sub is not None else '<m:sub/>'
    supx = f'<m:sup>{sup}</m:sup>' if sup is not None else '<m:sup/>'
    pr = (f'<m:naryPr><m:chr m:val="{chop}"/><m:limLoc m:val="{limloc}"/>'
          f'<m:subHide m:val="{subhide}"/><m:supHide m:val="{suphide}"/></m:naryPr>')
    return f'<m:nary>{pr}{subx}{supx}<m:e/></m:nary>'


def parse_atom(ts):
    t = ts.next()
    if t is None:
        return ''
    k = t[0]
    if k == '{':
        inner = parse_seq(ts, closing=True)
        return inner
    if k == 'char':
        ch = t[1]
        if ch == ' ':
            return ''
        return mr(ch)
    if k == 'cmd':
        name = t[1]
        if name in ('frac', 'dfrac', 'tfrac'):
            num = parse_group_or_atom(ts)
            den = parse_group_or_atom(ts)
            return (f'<m:f><m:fPr><m:type m:val="bar"/></m:fPr>'
                    f'<m:num>{num}</m:num><m:den>{den}</m:den></m:f>')
        if name == 'sqrt':
            deg = None
            if ts.peek() and ts.peek()[0] == 'char' and ts.peek()[1] == '[':
                ts.next()
                buf = ''
                while ts.peek() and not (ts.peek()[0] == 'char' and ts.peek()[1] == ']'):
                    tt = ts.next()
                    buf += tt[1] if tt[0] == 'char' else ''
                if ts.peek():
                    ts.next()
                deg = mr(buf)
            rad = parse_group_or_atom(ts)
            if deg:
                return f'<m:rad><m:deg>{deg}</m:deg><m:e>{rad}</m:e></m:rad>'
            return ('<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr>'
                    f'<m:deg/><m:e>{rad}</m:e></m:rad>')
        if name in NARY:
            chop, limloc = NARY[name]
            sub = sup = None
            while ts.peek() and ts.peek()[0] in ('_', '^'):
                op = ts.next()[0]
                scr = parse_group_or_atom(ts)
                if op == '_':
                    sub = scr
                else:
                    sup = scr
            return nary(chop, limloc, sub, sup)
        if name in ACCENTS:
            base = parse_group_or_atom(ts)
            return (f'<m:acc><m:accPr><m:chr m:val="{ACCENTS[name]}"/></m:accPr>'
                    f'<m:e>{base}</m:e></m:acc>')
        if name == 'mathbb':
            g = read_group_raw(ts)
            return mr('𝟙' if g.strip() == '1' else g)
        if name in ('text', 'mathrm', 'operatorname', 'textrm', 'textnormal'):
            g = read_group_raw(ts)
            return mr(g, upright=True)
        if name in FONT_CMDS:
            return parse_group_or_atom(ts)
        if name in FUNCS:
            return mr(name, upright=True)
        if name == 'left':
            d = ts.next()
            ch = _delim(d)
            return mr(ch) if ch not in ('.', '') else ''
        if name == 'right':
            d = ts.next()
            ch = _delim(d)
            return mr(ch) if ch not in ('.', '') else ''
        if name == 'begin':
            return parse_env(ts)
        if name == 'end':
            read_group_raw(ts)
            return ''
        if name in GREEK:
            return mr(GREEK[name])
        if name in SYMBOLS:
            return mr(SYMBOLS[name])
        if name in SPACING:
            return ''
        if name in ('{', '}', '|', '%', '#', '$', '&', '_'):
            return mr(name)
        if name == 'lbrace':
            return mr('{')
        if name == 'rbrace':
            return mr('}')
        # unknown command: emit letters as-is
        return mr(name)
    if k in ('^', '_'):
        # stray script with empty base
        scr = parse_group_or_atom(ts)
        if k == '_':
            return make_script('', scr, None)
        return make_script('', None, scr)
    return ''


def _delim(d):
    if d is None:
        return ''
    if d[0] == 'char':
        return d[1]
    if d[0] == 'cmd':
        return {'{': '{', '}': '}', 'lbrace': '{', 'rbrace': '}',
                'langle': '⟨', 'rangle': '⟩', 'vert': '|', '|': '‖',
                'lceil': '⌈', 'rceil': '⌉', 'lfloor': '⌊', 'rfloor': '⌋',
                '.': '.'}.get(d[1], '')
    return ''


def parse_env(ts):
    env = read_group_raw(ts)
    rows = [[]]
    depth = 0
    while ts.peek() is not None:
        p = ts.peek()
        if p[0] == 'cmd' and p[1] == 'begin':
            # nested env: collect raw into current row (rare); treat generically
            rows[-1].append(ts.next())
            continue
        if p[0] == 'cmd' and p[1] == 'end':
            ts.next()
            read_group_raw(ts)
            break
        if p[0] == 'rowbreak' and depth == 0:
            ts.next(); rows.append([]); continue
        rows[-1].append(ts.next())
    es = []
    for r in rows:
        cells = [t for t in r if t[0] != '&']
        cell = parse_seq(TS(cells), closing=False)
        if cell.strip():
            es.append(f'<m:e>{cell}</m:e>')
    if not es:
        return ''
    if env in ('aligned', 'align', 'align*', 'gather', 'gathered', 'cases',
               'array', 'matrix', 'bmatrix', 'pmatrix', 'split', 'eqnarray'):
        pr = '<m:eqArrPr><m:baseJc m:val="center"/></m:eqArrPr>'
        return f'<m:eqArr>{pr}{"".join(es)}</m:eqArr>'
    return ''.join(e[5:-6] for e in es)  # strip <m:e></m:e> if unknown env


def parse_seq(ts, closing):
    out = []
    while True:
        p = ts.peek()
        if p is None:
            break
        if closing and p[0] == '}':
            ts.next()
            break
        if p[0] == 'rowbreak' or p[0] == '&':
            ts.next()
            continue
        if p[0] == 'cmd' and p[1] == 'end':
            break
        atom = parse_atom(ts)
        sub = sup = None
        while ts.peek() and ts.peek()[0] in ('_', '^'):
            op = ts.next()[0]
            scr = parse_group_or_atom(ts)
            if op == '_':
                sub = scr
            else:
                sup = scr
        if sub is not None or sup is not None:
            atom = make_script(atom, sub, sup)
        out.append(atom)
    return ''.join(out)


def latex_to_omml_inner(latex):
    """Convert a LaTeX math string to the inner OMML (no <m:oMath> wrapper)."""
    s = latex.strip()
    s = re.sub(r'\\tag\{[^{}]*\}', '', s)
    s = s.strip().strip('$').strip()
    ts = TS(tokenize(s))
    return parse_seq(ts, closing=False)


def omath(latex):
    inner = latex_to_omml_inner(latex)
    return (f'<m:oMath xmlns:m="{M}">{inner}</m:oMath>')


if __name__ == '__main__':
    tests = [
        r'\tilde{x}_{j} = \frac{x_{j}-\mu_{j}^{\text{train}}}{\sigma_{j}^{\text{train}}}',
        r'\text{BS}(h) = \frac{1}{N}\sum_{i=1}^{N}\big(\hat{p}_h^{\text{cal},(i)}-y_{i,h}\big)^2',
        r'S_h = \prod_{l=1}^{h}\big(1-\lambda_l\big)',
    ]
    for t in tests:
        print(omath(t)[:300], '\n')
