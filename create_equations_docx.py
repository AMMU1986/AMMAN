#!/usr/bin/env python3
"""
Create a Word document (.docx) containing the List of Equations as NATIVE,
EDITABLE Microsoft Word equations (Office Math Markup Language, OMML).

Each equation is emitted as an <m:oMath> element inside the document body,
which is exactly what Word's built-in Equation Editor produces. When the
generated file is opened in Word and an equation is clicked, it is fully
editable in the equation editor (the equations are NOT images).

Uses only the Python standard library (zipfile) - no third-party packages.
"""

import zipfile

OUTPUT_PATH = '/projects/sandbox/AMMAN/Equations_List.docx'

# ------------------------------------------------------------
# OMML helper builders
# ------------------------------------------------------------
# All builders return strings of OMML (m:*) markup. Runs of ordinary math
# text use <m:r><m:t>...</m:t></m:r>.


def xml_escape(text):
    """Escape XML special characters."""
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;'))


def run(text):
    """A math run containing literal text."""
    return f'<m:r><m:t xml:space="preserve">{xml_escape(text)}</m:t></m:r>'


def run_i(text):
    """A math run explicitly rendered in italic (variables)."""
    return (f'<m:r><m:rPr><m:sty m:val="i"/></m:rPr>'
            f'<m:t xml:space="preserve">{xml_escape(text)}</m:t></m:r>')


def frac(num, den):
    """Fraction: num over den."""
    return (f'<m:f><m:num>{num}</m:num>'
            f'<m:den>{den}</m:den></m:f>')


def sub(base, sub_):
    """Subscript."""
    return (f'<m:sSub><m:e>{base}</m:e>'
            f'<m:sub>{sub_}</m:sub></m:sSub>')


def sup(base, sup_):
    """Superscript."""
    return (f'<m:sSup><m:e>{base}</m:e>'
            f'<m:sup>{sup_}</m:sup></m:sSup>')


def subsup(base, sub_, sup_):
    """Combined subscript and superscript."""
    return (f'<m:sSubSup><m:e>{base}</m:e>'
            f'<m:sub>{sub_}</m:sub><m:sup>{sup_}</m:sup></m:sSubSup>')


def rad(radicand):
    """Square root."""
    return (f'<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr>'
            f'<m:deg/><m:e>{radicand}</m:e></m:rad>')


def delim(inner, beg='(', end=')'):
    """Delimiters (brackets) around inner content."""
    return (f'<m:d><m:dPr><m:begChr m:val="{xml_escape(beg)}"/>'
            f'<m:endChr m:val="{xml_escape(end)}"/></m:dPr>'
            f'<m:e>{inner}</m:e></m:d>')


def bar(base):
    """Overbar (e.g. mean)."""
    return (f'<m:bar><m:barPr><m:pos m:val="top"/></m:barPr>'
            f'<m:e>{base}</m:e></m:bar>')


def acc(base, chr_='\u0302'):
    """Accent over a base (default: circumflex/hat)."""
    return (f'<m:acc><m:accPr><m:chr m:val="{chr_}"/></m:accPr>'
            f'<m:e>{base}</m:e></m:acc>')


def nary_sum(sub_, sup_, body):
    """N-ary summation with lower and upper limits."""
    return (f'<m:nary><m:naryPr><m:chr m:val="\u2211"/>'
            f'<m:limLoc m:val="subSup"/></m:naryPr>'
            f'<m:sub>{sub_}</m:sub><m:sup>{sup_}</m:sup>'
            f'<m:e>{body}</m:e></m:nary>')


def omath(inner):
    """Wrap content in an oMath element (an inline equation object)."""
    return f'<m:oMath>{inner}</m:oMath>'


# ------------------------------------------------------------
# Build each equation's OMML content
# ------------------------------------------------------------

def build_equations():
    """Return a list of (section, [(number, omml_inner), ...]) groups."""

    # convenience aliases
    rho = '\u03c1'      # ρ
    phi = '\u03c6'      # φ
    mu = '\u03bc'       # μ
    eta = '\u03b7'      # η
    delta = '\u0394'    # Δ
    partial = '\u2202'  # ∂
    mdot = '\u1e41'     # ṁ (m with dot above)
    le = '\u2264'       # ≤
    isin = '\u2208'     # ∈
    minus = '\u2212'    # −
    cdot = '\u22c5'     # ⋅
    times = '\u00d7'    # ×

    groups = []

    # ---- Section 3.2 ----
    eqs_32 = []

    # (1) rho_hnf = (1-phi) rho_bf + phi1 rho_p1 + phi2 rho_p2
    e1 = (sub(run_i(rho), run('hnf')) + run('=') +
          delim(run('1') + run(minus) + run_i(phi)) + sub(run_i(rho), run('bf')) +
          run('+') + sub(run_i(phi), run('1')) + sub(run_i(rho), run('p1')) +
          run('+') + sub(run_i(phi), run('2')) + sub(run_i(rho), run('p2')))
    eqs_32.append((1, e1))

    # (2) (rho c_p)_hnf = (1-phi)(rho c_p)_bf + phi1 (rho c_p)_p1 + phi2 (rho c_p)_p2
    rho_cp = run_i(rho) + sub(run_i('c'), run('p'))
    e2 = (sub(delim(rho_cp), run('hnf')) + run('=') +
          delim(run('1') + run(minus) + run_i(phi)) + sub(delim(rho_cp), run('bf')) +
          run('+') + sub(run_i(phi), run('1')) + sub(delim(rho_cp), run('p1')) +
          run('+') + sub(run_i(phi), run('2')) + sub(delim(rho_cp), run('p2')))
    eqs_32.append((2, e2))

    # (3) phi = phi1 + phi2
    e3 = (run_i(phi) + run('=') + sub(run_i(phi), run('1')) +
          run('+') + sub(run_i(phi), run('2')))
    eqs_32.append((3, e3))

    # (4) k_hnf = k_bf * [ (k_np + 2 k_bf - 2 phi (k_bf - k_np)) /
    #                      (k_np + 2 k_bf + phi (k_bf - k_np)) ]
    k_np = sub(run_i('k'), run('np'))
    k_bf = sub(run_i('k'), run('bf'))
    num4 = (k_np + run('+') + run('2') + k_bf + run(minus) + run('2') +
            run_i(phi) + delim(k_bf + run(minus) + k_np))
    den4 = (k_np + run('+') + run('2') + k_bf + run('+') +
            run_i(phi) + delim(k_bf + run(minus) + k_np))
    e4 = (sub(run_i('k'), run('hnf')) + run('=') + k_bf + run(cdot) +
          delim(frac(num4, den4), '[', ']'))
    eqs_32.append((4, e4))

    # (5) mu_hnf = mu_bf / ( 1 - 34.87 (d_p/d_bf)^(-0.3) phi^1.03 )
    dp_dbf = frac(sub(run_i('d'), run('p')), sub(run_i('d'), run('bf')))
    den5 = (run('1') + run(minus) + run('34.87') +
            sup(delim(dp_dbf), run(minus + '0.3')) +
            sup(run_i(phi), run('1.03')))
    e5 = (sub(run_i(mu), run('hnf')) + run('=') +
          frac(sub(run_i(mu), run('bf')), den5))
    eqs_32.append((5, e5))

    groups.append(('3.2 Hybrid nanofluid thermophysical properties', eqs_32))

    # ---- Section 3.4 Governing equations (CFD) ----
    eqs_34 = []

    # (6) d(rho u_i)/dx_i = 0
    e6 = (frac(run(partial) + delim(run_i(rho) + sub(run_i('u'), run_i('i'))),
               run(partial) + sub(run_i('x'), run_i('i'))) +
          run('=') + run('0'))
    eqs_34.append((6, e6))

    # (7) d(rho u_i u_j)/dx_j = -dp/dx_i + d/dx_j[(mu+mu_t)(du_i/dx_j + du_j/dx_i)]
    ui = sub(run_i('u'), run_i('i'))
    uj = sub(run_i('u'), run_i('j'))
    xi = sub(run_i('x'), run_i('i'))
    xj = sub(run_i('x'), run_i('j'))
    mu_t = sub(run_i(mu), run_i('t'))
    inner7 = (frac(run(partial) + ui, run(partial) + xj) + run('+') +
              frac(run(partial) + uj, run(partial) + xi))
    e7 = (frac(run(partial) + delim(run_i(rho) + ui + uj), run(partial) + xj) +
          run('=') + run(minus) + frac(run(partial) + run_i('p'), run(partial) + xi) +
          run('+') +
          frac(run(partial), run(partial) + xj) +
          delim(delim(run_i(mu) + run('+') + mu_t) + delim(inner7), '[', ']'))
    eqs_34.append((7, e7))

    # (8) d(rho c_p u_j T)/dx_j = d/dx_j[(k + c_p mu_t / Pr_t) dT/dx_j]
    cp = sub(run_i('c'), run('p'))
    Pr_t = sub(run('Pr'), run_i('t'))
    inner8 = (run_i('k') + run('+') + frac(cp + mu_t, Pr_t))
    e8 = (frac(run(partial) + delim(run_i(rho) + cp + uj + run_i('T')),
               run(partial) + xj) +
          run('=') +
          frac(run(partial), run(partial) + xj) +
          delim(delim(inner8) + frac(run(partial) + run_i('T'), run(partial) + xj),
                '[', ']'))
    eqs_34.append((8, e8))

    groups.append(('3.4 Governing equations (CFD)', eqs_34))

    # ---- Section 3.5 Data reduction ----
    eqs_35 = []

    # (9) Q_elec = V I
    e9 = (sub(run_i('Q'), run('elec')) + run('=') +
          run_i('V') + run_i('I'))
    eqs_35.append((9, e9))

    # (10) Q_fluid = mdot c_p (T_out - T_in)
    e10 = (sub(run_i('Q'), run('fluid')) + run('=') +
           run_i(mdot) + cp +
           delim(sub(run_i('T'), run('out')) + run(minus) + sub(run_i('T'), run('in'))))
    eqs_35.append((10, e10))

    # (11) h = Q / (A_s dT_lm)
    e11 = (run_i('h') + run('=') +
           frac(run_i('Q'), sub(run_i('A'), run('s')) + run_i(delta) + sub(run_i('T'), run('lm'))))
    eqs_35.append((11, e11))

    # (12) Nu = h D_h / k
    Dh = sub(run_i('D'), run('h'))
    e12 = (run('Nu') + run('=') + frac(run_i('h') + Dh, run_i('k')))
    eqs_35.append((12, e12))

    # (13) Re = rho u D_h / mu
    e13 = (run('Re') + run('=') + frac(run_i(rho) + run_i('u') + Dh, run_i(mu)))
    eqs_35.append((13, e13))

    # (14) f = 2 dP D_h / (rho u^2 L_h)
    e14 = (run_i('f') + run('=') +
           frac(run('2') + run_i(delta) + run_i('P') + Dh,
                run_i(rho) + sup(run_i('u'), run('2')) + sub(run_i('L'), run('h'))))
    eqs_35.append((14, e14))

    # (15) D_h = 2 W H / (W + H)
    e15 = (Dh + run('=') +
           frac(run('2') + run_i('W') + run_i('H'), run_i('W') + run('+') + run_i('H')))
    eqs_35.append((15, e15))

    # (16) P_pump = dP * Vdot / eta_p
    Vdot = acc(run_i('V'), '\u0307')  # V with dot above
    e16 = (sub(run_i('P'), run('pump')) + run('=') +
           frac(run_i(delta) + run_i('P') + run(cdot) + Vdot,
                sub(run_i(eta), run('p'))))
    eqs_35.append((16, e16))

    # (17) eta = (Nu/Nu_0) / (f/f_0)^(1/3)
    Nu0 = sub(run('Nu'), run('0'))
    f0 = sub(run_i('f'), run('0'))
    e17 = (run_i(eta) + run('=') +
           frac(frac(run('Nu'), Nu0),
                sup(delim(frac(run_i('f'), f0)), frac(run('1'), run('3')))))
    eqs_35.append((17, e17))

    groups.append(('3.5 Data reduction', eqs_35))

    # ---- Section 3.6 Machine-learning metrics ----
    eqs_36 = []

    yi = sub(run_i('y'), run_i('i'))
    yhat = sub(acc(run_i('y')), run_i('i'))
    ybar = bar(run_i('y'))
    sum_lower = run_i('i') + run('=') + run('1')
    sum_upper = run_i('n')

    # (18) R^2 = 1 - [ sum (y_i - yhat_i)^2 ] / [ sum (y_i - ybar)^2 ]
    num18 = nary_sum(sum_lower, sum_upper, sup(delim(yi + run(minus) + yhat), run('2')))
    den18 = nary_sum(sum_lower, sum_upper, sup(delim(yi + run(minus) + ybar), run('2')))
    e18 = (sup(run_i('R'), run('2')) + run('=') + run('1') + run(minus) +
           frac(num18, den18))
    eqs_36.append((18, e18))

    # (19) RMSE = sqrt( (1/n) sum (y_i - yhat_i)^2 )
    body19 = (frac(run('1'), run_i('n')) +
              nary_sum(sum_lower, sum_upper, sup(delim(yi + run(minus) + yhat), run('2'))))
    e19 = (run('RMSE') + run('=') + rad(body19))
    eqs_36.append((19, e19))

    # (20) MAPE = (100/n) sum | (y_i - yhat_i)/y_i |
    absbar = delim(frac(yi + run(minus) + yhat, yi), '|', '|')
    e20 = (run('MAPE') + run('=') + frac(run('100'), run_i('n')) +
           nary_sum(sum_lower, sum_upper, absbar))
    eqs_36.append((20, e20))

    groups.append(('3.6 Machine-learning metrics', eqs_36))

    # ---- Section 3.7 Multi-objective optimization ----
    eqs_37 = []

    # (21) min over x  F(x) = [f1(x), f2(x)] = [-Nu(x), P_pump(x)]
    minx = sub(run('min'), run_i('x'))
    Fx = run_i('F') + delim(run_i('x'))
    f1x = sub(run_i('f'), run('1')) + delim(run_i('x'))
    f2x = sub(run_i('f'), run('2')) + delim(run_i('x'))
    Nux = run('Nu') + delim(run_i('x'))
    Ppumpx = sub(run_i('P'), run('pump')) + delim(run_i('x'))
    e21 = (minx + run('\u2003') + Fx + run('=') +
           delim(f1x + run(',') + run('\u2002') + f2x, '[', ']') + run('=') +
           delim(run(minus) + Nux + run(',') + run('\u2002') + Ppumpx, '[', ']'))
    eqs_37.append((21, e21))

    # (22) constraints
    ar = (run('2') + run(' ' + le + ' ') + run('AR') + run(' ' + le + ' ') + run('8'))
    dh_c = (run('2 mm') + run(' ' + le + ' ') + Dh + run(' ' + le + ' ') + run('4 mm'))
    phi_c = (run('0') + run(' ' + le + ' ') + run_i(phi) + run(' ' + le + ' ') + run('1%'))
    mr_c = (run('MR') + run(' ' + isin + ' ') +
            delim(run('25:75') + run(',') + run(' 50:50') + run(',') + run(' 75:25'),
                  '{', '}'))
    re_c = (run('3000') + run(' ' + le + ' ') + run('Re') + run(' ' + le + ' ') + run('20000'))
    e22 = ar + run(',\u2002') + dh_c + run(',\u2002') + phi_c + run(',\u2002') + mr_c + run(',\u2002') + re_c
    eqs_37.append((22, e22))

    groups.append(('3.7 Multi-objective optimization', eqs_37))

    return groups


# ------------------------------------------------------------
# WordprocessingML paragraph builders
# ------------------------------------------------------------

def heading_paragraph(text, level='Heading1'):
    text = xml_escape(text)
    return (f'<w:p><w:pPr><w:pStyle w:val="{level}"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{text}</w:t></w:r></w:p>')


def title_paragraph(text):
    text = xml_escape(text)
    return (f'<w:p><w:pPr><w:pStyle w:val="Title"/><w:jc w:val="center"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{text}</w:t></w:r></w:p>')


def equation_paragraph(number, omml_inner):
    """A paragraph holding a centered native equation with a right-aligned
    equation number, using a tab-stop layout common in journal papers."""
    equation = omath(omml_inner)
    # Tab stops: centre tab in the middle, right tab at the margin so the
    # equation sits centred and the number sits at the right edge.
    ppr = ('<w:pPr>'
           '<w:tabs>'
           '<w:tab w:val="center" w:pos="4680"/>'
           '<w:tab w:val="right" w:pos="9360"/>'
           '</w:tabs>'
           '</w:pPr>')
    return (f'<w:p>{ppr}'
            f'<w:r><w:tab/></w:r>'
            f'{equation}'
            f'<w:r><w:tab/><w:t xml:space="preserve">({number})</w:t></w:r>'
            f'</w:p>')


def empty_paragraph():
    return '<w:p/>'


# ------------------------------------------------------------
# Package assembly
# ------------------------------------------------------------

def build_body():
    parts = [title_paragraph('List of Equations')]
    groups = build_equations()
    for section, eqs in groups:
        parts.append(heading_paragraph(section, 'Heading1'))
        for number, inner in eqs:
            parts.append(equation_paragraph(number, inner))
            parts.append(empty_paragraph())
    return '\n'.join(parts)


def create_docx(output_path):
    body_content = build_body()

    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

    word_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr>
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
</w:styles>'''

    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {body_content}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', styles)

    print(f"  Created {output_path}")


if __name__ == '__main__':
    print("Creating Word document with native (editable) equations...")
    create_docx(OUTPUT_PATH)
    print("\nDone! File created:")
    print(f"  - {OUTPUT_PATH}")
