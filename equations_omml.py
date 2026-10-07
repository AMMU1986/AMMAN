#!/usr/bin/env python3
"""
The 18 governing equations expressed as explicit OMML (Office Math) trees,
plus their word-form statements. Each entry: (omath_fragment, words, number).
Rendered by build_ml_phe_docx.py as centered, numbered equation-editor objects.
"""

import omml as o
from omml import run as r, sub, sup, subsup, frac, rad, delim, nary, chem

# convenient upright helpers
def U(t):   # upright text
    return r(t, italic=False)
def V(t):   # italic variable
    return r(t, italic=True)
def op(t):  # operator glyph, upright
    return r(t, italic=False)

PLUS = op(' + ')
MINUS = op(' \u2212 ')
EQ = op(' = ')
DOT = op('\u00b7')
MIN = op(' \u2212 ')


def _phi(n):
    return sub(o.run(o.GREEK['phi']), U(str(n)))


# ---- EQ1 : effective density -------------------------------------------------
EQ1 = ''.join([
    sub(o.run(o.GREEK['rho']), U('nf')), EQ,
    delim(U('1') + MINUS + _phi(1) + MINUS + _phi(2)), DOT, sub(o.run(o.GREEK['rho']), U('bf')),
    PLUS, _phi(1), DOT, sub(o.run(o.GREEK['rho']), U('p1')),
    PLUS, _phi(2), DOT, sub(o.run(o.GREEK['rho']), U('p2')),
])

# ---- EQ2 : effective specific heat ------------------------------------------
def rhocp(sub_):
    # (rho c_p)_sub
    return sub(delim(o.run(o.GREEK['rho']) + DOT + sub(V('c'), U('p'))), U(sub_))
EQ2 = ''.join([
    rhocp('nf'), EQ,
    delim(U('1') + MINUS + _phi(1) + MINUS + _phi(2)), DOT, rhocp('bf'),
    PLUS, _phi(1), DOT, rhocp('p1'),
    PLUS, _phi(2), DOT, rhocp('p2'),
])

# ---- EQ3 : Reynolds number ---------------------------------------------------
EQ3 = ''.join([
    U('Re'), EQ, frac(V('G') + DOT + sub(V('D'), U('h')), sub(o.run(o.GREEK['mu']), U('nf'))),
])

# ---- EQ4 : Prandtl number ----------------------------------------------------
EQ4 = ''.join([
    U('Pr'), EQ, frac(sub(o.run(o.GREEK['mu']), U('nf')) + DOT + sub(V('c'), U('p,nf')),
                      sub(V('k'), U('nf'))),
])

# ---- EQ5 : heat duty ---------------------------------------------------------
EQ5 = ''.join([
    V('Q'), EQ, V('\u1e41'), DOT, sub(V('c'), U('p')),
    DOT, delim(sub(V('T'), U('in')) + MINUS + sub(V('T'), U('out'))),
])

# ---- EQ6 : overall U ---------------------------------------------------------
EQ6 = ''.join([
    V('U'), EQ, frac(V('Q'), V('A') + DOT + U('LMTD')),
])

# ---- EQ7 : LMTD --------------------------------------------------------------
EQ7 = ''.join([
    U('LMTD'), EQ,
    frac(sub(o.run('\u0394T', italic=False), U('1')) + MINUS + sub(o.run('\u0394T', italic=False), U('2')),
         U('ln') + delim(frac(sub(o.run('\u0394T', italic=False), U('1')),
                               sub(o.run('\u0394T', italic=False), U('2'))))),
])

# ---- EQ8 : resistance network ------------------------------------------------
EQ8 = ''.join([
    frac(U('1'), V('U') + DOT + V('A')), EQ,
    frac(U('1'), sub(V('h'), U('h')) + DOT + V('A')), PLUS,
    frac(sub(V('t'), U('w')), sub(V('k'), U('w')) + DOT + V('A')), PLUS,
    frac(U('1'), sub(V('h'), U('c')) + DOT + V('A')),
])

# ---- EQ9 : Nusselt -----------------------------------------------------------
EQ9 = ''.join([
    U('Nu'), EQ, frac(V('h') + DOT + sub(V('D'), U('h')), sub(V('k'), U('nf'))),
])

# ---- EQ10 : friction factor --------------------------------------------------
EQ10 = ''.join([
    V('f'), EQ, frac(o.run('\u0394P', italic=False) + DOT + sub(V('D'), U('h')) + DOT + U('2') + o.run(o.GREEK['rho']),
                     V('L') + DOT + sup(V('G'), U('2'))),
])

# ---- EQ11 : thermal performance factor --------------------------------------
EQ11 = ''.join([
    o.run(o.GREEK['eta']), EQ,
    frac(frac(sub(V('h'), U('nf')), sub(V('h'), U('w'))),
         rad(frac(sub(V('f'), U('nf')), sub(V('f'), U('w'))), degree=U('3'))),
])

# ---- EQ12 : IQR outlier rule -------------------------------------------------
EQ12 = ''.join([
    sub(V('Q'), U('1')), MINUS, U('1.5'), DOT, U('IQR'),
    op(' \u2264 '), V('x'), op(' \u2264 '),
    sub(V('Q'), U('3')), PLUS, U('1.5'), DOT, U('IQR'),
])

# ---- EQ13 : min-max normalisation -------------------------------------------
EQ13 = ''.join([
    sub(V('x'), U('norm')), EQ,
    frac(V('x') + MINUS + sub(V('x'), U('min')),
         sub(V('x'), U('max')) + MINUS + sub(V('x'), U('min'))),
])

# ---- EQ14 : BR-ANN objective -------------------------------------------------
EQ14 = ''.join([
    V('F') + delim(V('w')), EQ,
    o.run(o.GREEK['beta']), DOT,
    nary('\u2211', sub_=V('i'), body=sup(sub(V('e'), U('i')), U('2'))),
    PLUS, o.run(o.GREEK['alpha']), DOT,
    nary('\u2211', sub_=V('j'), body=sup(sub(V('w'), U('j')), U('2'))),
])

# ---- EQ15 : random forest average -------------------------------------------
EQ15 = ''.join([
    sub(o.run('\u0177', italic=True), U('RF')), EQ,
    frac(U('1'), V('B')), DOT,
    nary('\u2211', sub_=(V('b') + op('=') + U('1')), sup_=V('B'),
         body=sub(V('T'), U('b')) + delim(V('x'))),
])

# ---- EQ16 : gradient boosting update ----------------------------------------
EQ16 = ''.join([
    sub(V('F'), U('m')) + delim(V('x')), EQ,
    sub(V('F'), o.run('m\u22121', italic=False)) + delim(V('x')), PLUS,
    o.run(o.GREEK['nu']), DOT, sub(V('h'), U('m')) + delim(V('x')),
])

# ---- EQ17 : SVR objective ----------------------------------------------------
EQ17 = ''.join([
    U('min'), op('  '),
    frac(U('1'), U('2')), sup(delim(V('w'), '\u2016', '\u2016'), U('2')),
    PLUS, V('C'), DOT,
    nary('\u2211', sub_=V('i'),
         body=delim(sub(o.run(o.GREEK['xi']), U('i')) + PLUS + sup(sub(o.run(o.GREEK['xi']), U('i')), U('*')))),
])

# ---- EQ18 : coefficient of determination ------------------------------------
EQ18 = ''.join([
    sup(V('R'), U('2')), EQ, U('1'), MINUS,
    frac(nary('\u2211', sub_=V('i'),
              body=sup(delim(sub(V('y'), U('i')) + MINUS + sub(o.run('\u0177', italic=True), U('i'))), U('2'))),
         nary('\u2211', sub_=V('i'),
              body=sup(delim(sub(V('y'), U('i')) + MINUS + o.run('\u0233', italic=True)), U('2')))),
])


EQUATIONS = {
    'EQ1': (EQ1, 'mixture density equals base-fluid volume fraction times base-fluid density, '
                 'plus each particle volume fraction times its solid density', 1),
    'EQ2': (EQ2, 'the product of mixture density and specific heat equals the volume-weighted sum of '
                 'the density-specific-heat products of base fluid and particles', 2),
    'EQ3': (EQ3, 'Reynolds number equals channel mass flux times hydraulic diameter divided by dynamic viscosity', 3),
    'EQ4': (EQ4, 'Prandtl number equals dynamic viscosity times specific heat divided by thermal conductivity', 4),
    'EQ5': (EQ5, 'heat duty equals mass flow rate times specific heat times the inlet-to-outlet temperature difference', 5),
    'EQ6': (EQ6, 'overall heat-transfer coefficient equals heat duty divided by the product of area and '
                 'log-mean temperature difference', 6),
    'EQ7': (EQ7, 'log-mean temperature difference equals the difference of the terminal temperature differences '
                 'divided by the natural logarithm of their ratio', 7),
    'EQ8': (EQ8, 'overall thermal resistance equals the hot-side convective resistance plus the plate-wall '
                 'conduction resistance plus the cold-side convective resistance', 8),
    'EQ9': (EQ9, 'Nusselt number equals the convective coefficient times hydraulic diameter divided by '
                 'nanofluid thermal conductivity', 9),
    'EQ10': (EQ10, 'Darcy friction factor equals pressure drop times hydraulic diameter times twice the density, '
                   'divided by channel length times the square of the mass flux', 10),
    'EQ11': (EQ11, 'thermal performance factor equals the convective-coefficient ratio divided by the cube root '
                   'of the friction-factor ratio', 11),
    'EQ12': (EQ12, 'an observation is retained only if it lies within 1.5 interquartile ranges of the first and '
                   'third quartiles', 12),
    'EQ13': (EQ13, 'the normalised feature equals the raw value minus its minimum divided by the span between '
                   'its maximum and minimum', 13),
    'EQ14': (EQ14, 'the Bayesian-regularised objective equals a weighted sum of squared errors plus a weighted '
                   'sum of squared network weights', 14),
    'EQ15': (EQ15, 'the random-forest prediction equals the arithmetic mean of the outputs of the B bootstrap trees', 15),
    'EQ16': (EQ16, 'each boosting stage adds a shrunk tree fitted to the negative gradient of a '
                   'complexity-penalised loss', 16),
    'EQ17': (EQ17, 'support-vector regression minimises model complexity plus a penalty on deviations that '
                   'exceed the epsilon-insensitive tube', 17),
    'EQ18': (EQ18, 'the coefficient of determination equals one minus the residual sum of squares divided by '
                   'the total sum of squares', 18),
}


if __name__ == '__main__':
    import xml.dom.minidom as X
    NS = '<root xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">%s</root>'
    for k in sorted(EQUATIONS, key=lambda x: EQUATIONS[x][2]):
        frag = EQUATIONS[k][0]
        X.parseString(NS % o.omath(frag))
        print('OK', k)
    print('all 18 equations well-formed')
