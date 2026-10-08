#!/usr/bin/env python3
"""
Minimal OMML (Office Math Markup Language) builder.
Produces <m:oMath> ... </m:oMath> fragments that Word renders as native,
editable Equation-Editor objects. Stdlib only.

Helper constructors cover: runs (text), Greek/symbols, superscripts (ssup),
subscripts (ssub), sub-superscripts (ssubsup), fractions (frac), radicals (rad),
n-ary integrals (nary), delimiters/brackets (delim), accents, and grouping.
"""

M = "m"  # namespace prefix used in document.xml (bound to the math namespace)


def _r(text, sty=None):
    """A math run. sty: 'p' plain (upright), 'i' italic, 'bi' bold-italic, None=default."""
    text = (text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
    rpr = ''
    if sty == 'p':
        rpr = '<m:rPr><m:sty m:val="p"/></m:rPr>'
    elif sty == 'bi':
        rpr = '<m:rPr><m:sty m:val="bi"/></m:rPr>'
    elif sty == 'b':
        rpr = '<m:rPr><m:sty m:val="b"/></m:rPr>'
    # default (no rPr) renders italic in Word, standard for variables
    return f'<m:r>{rpr}<m:t xml:space="preserve">{text}</m:t></m:r>'


def run(text, sty=None):
    return _r(text, sty)


def txt(text):
    """Upright multi-letter text (e.g. function names, 'exp')."""
    return _r(text, 'p')


def frac(num, den):
    return f'<m:f><m:num>{num}</m:num><m:den>{den}</m:den></m:f>'


def sup(base, exp):
    return f'<m:sSup><m:e>{base}</m:e><m:sup>{exp}</m:sup></m:sSup>'


def sub(base, s):
    return f'<m:sSub><m:e>{base}</m:e><m:sub>{s}</m:sub></m:sSub>'


def subsup(base, s, e):
    return (f'<m:sSubSup><m:e>{base}</m:e><m:sub>{s}</m:sub>'
            f'<m:sup>{e}</m:sup></m:sSubSup>')


def rad(radicand, degree=None):
    if degree is None:
        return (f'<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr>'
                f'<m:deg/><m:e>{radicand}</m:e></m:rad>')
    return f'<m:rad><m:deg>{degree}</m:deg><m:e>{radicand}</m:e></m:rad>'


def delim(inner, left='(', right=')'):
    return (f'<m:d><m:dPr><m:begChr m:val="{left}"/><m:endChr m:val="{right}"/>'
            f'</m:dPr><m:e>{inner}</m:e></m:d>')


def nary(op, lo, hi, body, limloc='subSup'):
    """n-ary operator (integral/sum). op like '&#8747;' integral, '&#8721;' sum."""
    return (f'<m:nary><m:naryPr><m:chr m:val="{op}"/><m:limLoc m:val="{limloc}"/>'
            f'<m:subHide m:val="0"/><m:supHide m:val="0"/></m:naryPr>'
            f'<m:sub>{lo}</m:sub><m:sup>{hi}</m:sup><m:e>{body}</m:e></m:nary>')


def nary_nolim(op, body):
    return (f'<m:nary><m:naryPr><m:chr m:val="{op}"/><m:limLoc m:val="subSup"/>'
            f'<m:subHide m:val="1"/><m:supHide m:val="1"/></m:naryPr>'
            f'<m:sub/><m:sup/><m:e>{body}</m:e></m:nary>')


def func(name, arg):
    """A function application like lim, exp with a lower script handled separately."""
    return (f'<m:func><m:fName>{name}</m:fName><m:e>{arg}</m:e></m:func>')


def lim_lower(name, under):
    """lim with underscript (m:limLow)."""
    return f'<m:limLow><m:e>{name}</m:e><m:lim>{under}</m:lim></m:limLow>'


def group(*parts):
    return ''.join(parts)


def omath(inner):
    """Wrap an equation body as a display oMath paragraph element."""
    return f'<m:oMathPara><m:oMath>{inner}</m:oMath></m:oMathPara>'


# ---- Greek letters and common symbols as entity strings ----
G = {
    'alpha': '&#945;', 'beta': '&#946;', 'gamma': '&#947;', 'Gamma': '&#915;',
    'delta': '&#948;', 'Delta': '&#916;', 'eta': '&#951;', 'theta': '&#952;',
    'Theta': '&#920;', 'kappa': '&#954;', 'lambda': '&#955;', 'Lambda': '&#923;',
    'mu': '&#956;', 'nu': '&#957;', 'rho': '&#961;', 'sigma': '&#963;',
    'Sigma': '&#931;', 'tau': '&#964;', 'phi': '&#966;', 'Phi': '&#934;',
    'chi': '&#967;', 'pi': '&#960;', 'infty': '&#8734;', 'partial': '&#8706;',
    'nabla': '&#8711;', 'cdot': '&#8901;', 'times': '&#215;', 'approx': '&#8776;',
    'leq': '&#8804;', 'geq': '&#8805;', 'to': '&#8594;', 'star': '&#8727;',
    'integral': '&#8747;', 'sum': '&#8721;', 'minus': '&#8722;', 'prime': '&#8242;',
}
