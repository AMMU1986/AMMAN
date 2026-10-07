#!/usr/bin/env python3
"""
Minimal OMML (Office Math Markup Language) builder for Word .docx.

Produces <m:oMath> fragments that Word renders as native, editable equation-
editor objects. Pure standard library.

Two layers:
  1. Low-level primitives (run, sub, sup, subsup, frac, rad, nary, delim, ...)
  2. A compact text-notation parser `omml_inline(src)` that turns strings such
     as "Re = (G*D_h)/mu_nf" or "TiO2" into an <m:oMath> fragment, so inline
     symbols and chemical formulas in running text can be emitted as real
     equation objects.

Notation understood by the parser:
  _{...} or _x        subscript (single char or braced group)
  ^{...} or ^x        superscript
  (a)/(b) or a/b      fraction   (explicit parentheses recommended)
  sqrt(x)             square root
  cbrt(x)             cube root
  sum / Sum           n-ary summation (optionally sum_{i}^{n})
  Greek names         alpha beta gamma delta eta mu nu phi rho epsilon lambda
                      sigma tau theta Delta  -> unicode glyphs
  <= >= != ~ * -> etc normalised to proper math glyphs
  chemical tokens     e.g. TiO2, Al2O3, H2O -> digits become subscripts
"""

M = 'm'  # namespace prefix used in document.xml (bound to the math namespace)

GREEK = {
    'alpha': '\u03b1', 'beta': '\u03b2', 'gamma': '\u03b3', 'delta': '\u03b4',
    'Delta': '\u0394', 'epsilon': '\u03b5', 'eta': '\u03b7', 'theta': '\u03b8',
    'kappa': '\u03ba', 'lambda': '\u03bb', 'mu': '\u03bc', 'nu': '\u03bd',
    'pi': '\u03c0', 'rho': '\u03c1', 'sigma': '\u03c3', 'tau': '\u03c4',
    'phi': '\u03c6', 'psi': '\u03c8', 'omega': '\u03c9', 'Omega': '\u03a9',
    'xi': '\u03be', 'Sum': '\u2211',
}

OPS = {
    '<=': '\u2264', '>=': '\u2265', '!=': '\u2260', '~=': '\u2248',
    '->': '\u2192', '<-': '\u2190', '*': '\u00b7', '...': '\u2026',
    'inf': '\u221e', '+-': '\u00b1',
}


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


# ---------------------------------------------------------------------------
# low-level primitives
# ---------------------------------------------------------------------------
def run(text, italic=True):
    """A math run. Letters are italic by default (variable style); set
    italic=False for upright text such as function names or digits."""
    rpr = '' if italic else '<m:rPr><m:sty m:val="p"/></m:rPr>'
    return '<m:r>%s<m:t xml:space="preserve">%s</m:t></m:r>' % (rpr, esc(text))


def _wrap(inner):
    return inner if inner.startswith('<m:') else run(inner)


def sub(base, sub_):
    return ('<m:sSub><m:e>%s</m:e><m:sub>%s</m:sub></m:sSub>'
            % (_wrap(base), _wrap(sub_)))


def sup(base, sup_):
    return ('<m:sSup><m:e>%s</m:e><m:sup>%s</m:sup></m:sSup>'
            % (_wrap(base), _wrap(sup_)))


def subsup(base, sub_, sup_):
    return ('<m:sSubSup><m:e>%s</m:e><m:sub>%s</m:sub><m:sup>%s</m:sup></m:sSubSup>'
            % (_wrap(base), _wrap(sub_), _wrap(sup_)))


def frac(num, den):
    return ('<m:f><m:fPr><m:type m:val="bar"/></m:fPr>'
            '<m:num>%s</m:num><m:den>%s</m:den></m:f>'
            % (_seq(num), _seq(den)))


def rad(radicand, degree=None):
    if degree is None:
        pr = '<m:radPr><m:degHide m:val="1"/></m:radPr>'
        deg = '<m:deg/>'
    else:
        pr = '<m:radPr/>'
        deg = '<m:deg>%s</m:deg>' % _seq(degree)
    return '<m:rad>%s%s<m:e>%s</m:e></m:rad>' % (pr, deg, _seq(radicand))


def delim(inner, left='(', right=')'):
    pr = ('<m:dPr><m:begChr m:val="%s"/><m:endChr m:val="%s"/></m:dPr>'
          % (esc(left), esc(right)))
    return '<m:d>%s<m:e>%s</m:e></m:d>' % (pr, _seq(inner))


def nary(op, sub_=None, sup_=None, body=''):
    subx = '<m:sub>%s</m:sub>' % _seq(sub_) if sub_ else '<m:sub/>'
    supx = '<m:sup>%s</m:sup>' % _seq(sup_) if sup_ else '<m:sup/>'
    pr = ('<m:naryPr><m:chr m:val="%s"/><m:limLoc m:val="undOvr"/>'
          '%s%s</m:naryPr>'
          % (esc(op), '' if sub_ else '<m:subHide m:val="1"/>',
             '' if sup_ else '<m:supHide m:val="1"/>'))
    return ('<m:nary>%s%s%s<m:e>%s</m:e></m:nary>'
            % (pr, subx, supx, _seq(body)))


def _seq(x):
    """Accept a string (already OMML or plain) or list of fragments."""
    if isinstance(x, (list, tuple)):
        return ''.join(_wrap(e) for e in x)
    return _wrap(x)


def omath(inner):
    return '<m:oMath>%s</m:oMath>' % _seq(inner)


def omath_para(inner, jc='center'):
    """Display equation paragraph (centered)."""
    return ('<m:oMathPara><m:oMathParaPr><m:jc m:val="%s"/></m:oMathParaPr>'
            '<m:oMath>%s</m:oMath></m:oMathPara>' % (jc, _seq(inner)))


# ---------------------------------------------------------------------------
# chemical formula -> OMML (digits & charges as subscripts/superscripts)
# ---------------------------------------------------------------------------
def chem(formula):
    """TiO2 -> Ti O(sub2); Al2O3 -> Al2(sub) O3(sub) with element letters upright.
    Rule: a run of digits immediately after a letter becomes a subscript."""
    out = []
    i = 0
    n = len(formula)
    buf = ''
    while i < n:
        c = formula[i]
        if c.isdigit():
            # flush letter buffer as upright base, then subscript the digits
            j = i
            while j < n and formula[j].isdigit():
                j += 1
            digits = formula[i:j]
            if buf:
                base = run(buf, italic=False)
                buf = ''
            else:
                base = run('', italic=False)
            out.append(sub(base, run(digits, italic=False)))
            i = j
        else:
            buf += c
            i += 1
    if buf:
        out.append(run(buf, italic=False))
    return ''.join(out)


# ---------------------------------------------------------------------------
# compact-notation inline parser
# ---------------------------------------------------------------------------
import re as _re

# tokens that should render as upright multi-letter identifiers
UPRIGHT_IDENT = {'Re', 'Nu', 'Pr', 'LMTD', 'IQR', 'RF', 'ln', 'min', 'max',
                 'minimise', 'keep', 'if', 'RMSE', 'MAE', 'MAPE'}
CHEM_TOKENS = {'TiO2', 'Al2O3', 'H2O', 'CuO', 'SiO2', 'Fe3O4', 'ZnO',
               'MWCNT', 'Cu', 'TiO', 'Al'}


def _subify_name(name):
    """Render identifiers like D_h, k_nf, c_p, T_hi as base with subscript."""
    if '_' in name:
        base, _, s = name.partition('_')
        bchunk = _ident(base)
        schunk = run(s, italic=False) if not s.isalpha() or len(s) > 1 else run(s)
        return sub(bchunk, schunk)
    return _ident(name)


def _ident(tok):
    if tok in GREEK:
        return run(GREEK[tok], italic=True)
    if tok in CHEM_TOKENS:
        return chem(tok)
    if tok in UPRIGHT_IDENT:
        return run(tok, italic=False)
    if tok.isdigit():
        return run(tok, italic=False)
    return run(tok, italic=True)


def omml_inline(src):
    """Parse a compact math string into an <m:oMath> fragment.

    Supported: identifiers, _sub, ^sup, / fractions over explicit (),
    sqrt()/cbrt(), sum, greek, operators. Designed for the symbol-level
    expressions used in this manuscript rather than a full TeX grammar.
    """
    frags, _ = _parse_expr(src, 0)
    return omath(frags)


def _parse_group(s, i):
    """parse a parenthesised group starting at s[i]=='('; return (frag,new_i)."""
    assert s[i] == '('
    depth = 0
    start = i
    while i < len(s):
        if s[i] == '(':
            depth += 1
        elif s[i] == ')':
            depth -= 1
            if depth == 0:
                inner = s[start + 1:i]
                frag, _ = _parse_expr(inner, 0)
                return frag, i + 1
        i += 1
    frag, _ = _parse_expr(s[start + 1:], 0)
    return frag, len(s)


def _atom(s, i):
    """parse one atom (identifier/number/group/func) with optional _ ^."""
    n = len(s)
    while i < n and s[i] == ' ':
        i += 1
    if i >= n:
        return '', i
    # function / sqrt / cbrt
    for fn in ('sqrt', 'cbrt'):
        if s.startswith(fn, i) and i + len(fn) < n and s[i + len(fn)] == '(':
            grp, j = _parse_group(s, i + len(fn))
            base = rad(grp, degree=(run('3', italic=False) if fn == 'cbrt' else None))
            return _attach_scripts(s, j, base)
    # group
    if s[i] == '(':
        grp, j = _parse_group(s, i)
        base = delim(grp)
        return _attach_scripts(s, j, base)
    # identifier or number (incl. chemical tokens and dotted names)
    m = _re.match(r'[A-Za-z]+[A-Za-z0-9]*|\d+(?:\.\d+)?', s[i:])
    if not m:
        # operator / punctuation char
        ch = s[i]
        glyph = {'=': '=', '+': '+', '-': '\u2212', ',': ',', '|': '|'}.get(ch, ch)
        return run(glyph, italic=False), i + 1
    tok = m.group(0)
    j = i + len(tok)
    # chemical token: whole token to chem()
    if tok in CHEM_TOKENS:
        base = chem(tok)
    else:
        base = _ident(tok)
    return _attach_scripts(s, j, base)


def _attach_scripts(s, i, base):
    n = len(s)
    sub_ = None
    sup_ = None
    while i < n and s[i] in '_^':
        kind = s[i]
        i += 1
        if i < n and s[i] == '{':
            depth = 0
            start = i
            while i < n:
                if s[i] == '{':
                    depth += 1
                elif s[i] == '}':
                    depth -= 1
                    if depth == 0:
                        break
                i += 1
            inner = s[start + 1:i]
            i += 1
            frag, _ = _parse_expr(inner, 0)
        else:
            m = _re.match(r'[A-Za-z0-9]+', s[i:])
            if m:
                tok = m.group(0)
                i += len(tok)
                frag = run(tok, italic=(tok.isalpha() and len(tok) == 1))
            else:
                frag = run(s[i], italic=False)
                i += 1
        if kind == '_':
            sub_ = frag
        else:
            sup_ = frag
    if sub_ is not None and sup_ is not None:
        return subsup(base, sub_, sup_), i
    if sub_ is not None:
        return sub(base, sub_), i
    if sup_ is not None:
        return sup(base, sup_), i
    return base, i


def _parse_expr(s, i):
    """parse a sequence of atoms with simple a/b fraction handling."""
    n = len(s)
    frags = []
    while i < n:
        while i < n and s[i] == ' ':
            i += 1
        if i >= n:
            break
        # multi-char operators
        matched = False
        for op in ('<=', '>=', '!=', '~=', '->', '<-', '...', '+-'):
            if s.startswith(op, i):
                frags.append(run(OPS[op], italic=False))
                i += len(op)
                matched = True
                break
        if matched:
            continue
        if s[i] == '*':
            frags.append(run(OPS['*'], italic=False))
            i += 1
            continue
        if s[i] == '/':
            # fraction: previous atom is numerator, next atom is denominator
            i += 1
            num = frags.pop() if frags else run('')
            den, i = _atom(s, i)
            frags.append(frac(num, den))
            continue
        atom, i = _atom(s, i)
        if atom == '':
            break
        frags.append(atom)
    return ''.join(_wrap(f) for f in frags), i
