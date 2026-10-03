#!/usr/bin/env python3
"""
Build Equations_Word_Editor.docx in which every equation (1)-(27) is a LIVE,
editable Word equation object (OMML - Office Math Markup Language).

Pure Python standard library. The equations are defined directly as OMML
fragments so they open as native, fully editable equations in Microsoft Word
(click an equation -> Equation Tools ribbon appears).
"""

import os
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "Equations_Word_Editor.docx")

M = 'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"'


# ---- small OMML builders ------------------------------------------------
def r(text):
    """A math run (plain)."""
    return "<m:r><m:t>{}</m:t></m:r>".format(text)


def sub(base, s):
    return ("<m:sSub><m:sSubPr/><m:e>{}</m:e>"
            "<m:sub>{}</m:sub></m:sSub>".format(base, s))


def sup(base, s):
    return ("<m:sSup><m:sSupPr/><m:e>{}</m:e>"
            "<m:sup>{}</m:sup></m:sSup>".format(base, s))


def frac(num, den):
    return ("<m:f><m:fPr/><m:num>{}</m:num>"
            "<m:den>{}</m:den></m:f>".format(num, den))


def rad(deg, radicand):
    """Radical; deg='' for square root."""
    hide = ' <m:degHide m:val="1"/>' if deg == "" else ""
    return ("<m:rad><m:radPr>{}</m:radPr><m:deg>{}</m:deg>"
            "<m:e>{}</m:e></m:rad>".format(hide, deg, radicand))


def acc(base, ch="\u0307"):
    """Accent (over-dot by default) e.g. m-dot."""
    return ('<m:acc><m:accPr><m:chr m:val="{}"/></m:accPr>'
            "<m:e>{}</m:e></m:acc>".format(ch, base))


def nary_sum(sub_e, sup_e, body):
    """n-ary summation with lower/upper limits."""
    return ('<m:nary><m:naryPr><m:chr m:val="\u2211"/>'
            '<m:limLoc m:val="undOvr"/></m:naryPr>'
            "<m:sub>{}</m:sub><m:sup>{}</m:sup>"
            "<m:e>{}</m:e></m:nary>".format(sub_e, sup_e, body))


def mdot(idx=None):
    base = acc(r("m"))
    return sub(base, r(idx)) if idx else base


# ---- the 27 equations as OMML content ----------------------------------
def equations():
    rho = "\u03c1"      # ρ
    phi = "\u03c6"      # φ
    mu = "\u03bc"       # μ
    eps = "\u03b5"      # ε
    Delta = "\u0394"    # Δ
    approx = "\u2248"   # ≈

    E = {}

    # (1) rho_nf = phi rho_p + (1-phi) rho_w
    E[1] = (sub(r(rho), r("nf")) + r("=") + sub(r(phi + rho), r("p"))
            + r("+(1\u2212" + phi + ")") + sub(r(rho), r("w")))

    # (2) (rho cp)_nf = phi (rho cp)_p + (1-phi)(rho cp)_w
    rcp = "(" + rho + "c" + "\u209a" + ")"
    E[2] = (sub(r(rcp), r("nf")) + r("=") + r(phi) + sub(r(rcp), r("p"))
            + r("+(1\u2212" + phi + ")") + sub(r(rcp), r("w")))

    # (3) cp_nf = [phi(rho cp)_p + (1-phi)(rho cp)_w] / rho_nf
    E[3] = (sub(r("c"), r("p,nf")) + r("=")
            + frac(r(phi) + sub(r(rcp), r("p")) + r("+(1\u2212" + phi + ")")
                   + sub(r(rcp), r("w")),
                   sub(r(rho), r("nf"))))

    # (4) mu_nf = (1 + 2.5 phi) mu_w
    E[4] = (sub(r(mu), r("nf")) + r("=(1+2.5" + phi + ")") + sub(r(mu), r("w")))

    # (5) k_nf = [ (k_p + 2k_w - 2phi(k_w-k_p)) / (k_p+2k_w+phi(k_w-k_p)) ] k_w
    num5 = (sub(r("k"), r("p")) + r("+2") + sub(r("k"), r("w"))
            + r("\u22122" + phi + "(") + sub(r("k"), r("w")) + r("\u2212")
            + sub(r("k"), r("p")) + r(")"))
    den5 = (sub(r("k"), r("p")) + r("+2") + sub(r("k"), r("w"))
            + r("+" + phi + "(") + sub(r("k"), r("w")) + r("\u2212")
            + sub(r("k"), r("p")) + r(")"))
    E[5] = (sub(r("k"), r("nf")) + r("=") + frac(num5, den5)
            + sub(r("k"), r("w")))

    # (6) rho_p = x rho_Al2O3 + (1-x) rho_CuO
    E[6] = (sub(r(rho), r("p")) + r("=x") + sub(r(rho), r("Al\u2082O\u2083"))
            + r("+(1\u2212x)") + sub(r(rho), r("CuO")))

    # (7) (rho cp)_p = x (rho cp)_Al2O3 + (1-x)(rho cp)_CuO
    E[7] = (sub(r(rcp), r("p")) + r("=x") + sub(r(rcp), r("Al\u2082O\u2083"))
            + r("+(1\u2212x)") + sub(r(rcp), r("CuO")))

    # (8) k_p = x k_Al2O3 + (1-x) k_CuO
    E[8] = (sub(r("k"), r("p")) + r("=x") + sub(r("k"), r("Al\u2082O\u2083"))
            + r("+(1\u2212x)") + sub(r("k"), r("CuO")))

    # (9) U = m_dot_nf / (rho_nf A_c)
    E[9] = (r("U=") + frac(mdot("nf"),
                           sub(r(rho), r("nf")) + sub(r("A"), r("c"))))

    # (10) D_h = 4 A_c / P
    E[10] = (sub(r("D"), r("h")) + r("=") + frac(r("4") + sub(r("A"), r("c")),
                                                 r("P")))

    # (11) Re = rho_nf U D_h / mu_nf
    E[11] = (r("Re=") + frac(sub(r(rho), r("nf")) + r("U") + sub(r("D"), r("h")),
                             sub(r(mu), r("nf"))))

    # (12) Pr = mu_nf c_p,nf / k_nf
    E[12] = (r("Pr=") + frac(sub(r(mu), r("nf")) + sub(r("c"), r("p,nf")),
                             sub(r("k"), r("nf"))))

    # (13) m_dot_nf = rho_nf V_dot_nf
    E[13] = (mdot("nf") + r("=") + sub(r(rho), r("nf"))
             + sub(acc(r("V")), r("nf")))

    # (14) Q_c = m_dot_nf c_p,nf (T_in - T_out)_nf
    E[14] = (sub(r("Q"), r("c")) + r("=") + mdot("nf") + sub(r("c"), r("p,nf"))
             + sub(r("(") + sub(r("T"), r("in")) + r("\u2212")
                   + sub(r("T"), r("out")) + r(")"), r("nf")))

    # (15) Q_a = m_dot_a c_p,a (T_out - T_in)_a
    E[15] = (sub(r("Q"), r("a")) + r("=") + mdot("a") + sub(r("c"), r("p,a"))
             + sub(r("(") + sub(r("T"), r("out")) + r("\u2212")
                   + sub(r("T"), r("in")) + r(")"), r("a")))

    # (16) Q = Q_c ~= Q_a
    E[16] = (r("Q=") + sub(r("Q"), r("c")) + r(approx) + sub(r("Q"), r("a")))

    # (17) Delta T_LMTD = [(Ts-Tin)-(Ts-Tout)] / ln[(Ts-Tin)/(Ts-Tout)]
    ts_in = sub(r("T"), r("s")) + r("\u2212") + sub(r("T"), r("in,nf"))
    ts_out = sub(r("T"), r("s")) + r("\u2212") + sub(r("T"), r("out,nf"))
    E[17] = (r(Delta) + sub(r("T"), r("LMTD")) + r("=")
             + frac(r("(") + ts_in + r(")\u2212(") + ts_out + r(")"),
                    r("ln[(") + ts_in + r(")/(") + ts_out + r(")]")))

    # (18) h = Q / (A_s Delta T_LMTD)
    E[18] = (r("h=") + frac(r("Q"),
                            sub(r("A"), r("s")) + r(Delta) + sub(r("T"), r("LMTD"))))

    # (19) Nu = h D_h / k_nf
    E[19] = (r("Nu=") + frac(r("h") + sub(r("D"), r("h")),
                             sub(r("k"), r("nf"))))

    # (20) C_min = (m_dot c_p)_min
    E[20] = (sub(r("C"), r("min")) + r("=")
             + sub(r("(") + mdot() + sub(r("c"), r("p")) + r(")"), r("min")))

    # (21) Q_max = C_min (T_in,c - T_in,a)
    E[21] = (sub(r("Q"), r("max")) + r("=") + sub(r("C"), r("min"))
             + r("(") + sub(r("T"), r("in,c")) + r("\u2212")
             + sub(r("T"), r("in,a")) + r(")"))

    # (22) eps = Q / Q_max
    E[22] = (r(eps) + r("=") + frac(r("Q"), sub(r("Q"), r("max"))))

    # (23) Nu = a Re^0.5 Pr^(1/3)
    E[23] = (r("Nu=a ") + sup(r("Re"), r("0.5")) + r(" ")
             + sup(r("Pr"), r("1/3")))

    # (24) r = cov(a,p) / sqrt(cov(a,a) cov(p,p))
    E[24] = (r("r=") + frac(r("cov(a,p)"),
                            rad("", r("cov(a,a) cov(p,p)"))))

    # (25) MSE = (1/N) sum_{i=1}^{N} (a_i - p_i)^2
    body25 = sup(r("(") + sub(r("a"), r("i")) + r("\u2212")
                 + sub(r("p"), r("i")) + r(")"), r("2"))
    E[25] = (r("MSE=") + frac(r("1"), r("N"))
             + nary_sum(r("i=1"), r("N"), body25))

    # (26) RMSE = sqrt(MSE)
    E[26] = (r("RMSE=") + rad("", r("MSE")))

    # (27) MAE = (1/N) sum_{i=1}^{N} |a_i - p_i|
    body27 = (r("|") + sub(r("a"), r("i")) + r("\u2212")
              + sub(r("p"), r("i")) + r("|"))
    E[27] = (r("MAE=") + frac(r("1"), r("N"))
             + nary_sum(r("i=1"), r("N"), body27))

    return E


def math_para(omml_body, tag):
    """A centered paragraph containing a display equation + a right (n) label."""
    return (
        '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
        '<m:oMathPara><m:oMath>' + omml_body + '</m:oMath></m:oMathPara>'
        '<w:r><w:rPr><w:sz w:val="22"/></w:rPr>'
        '<w:t xml:space="preserve">     (' + str(tag) + ')</w:t></w:r>'
        '</w:p>'
    )


def heading(text, size=28):
    return ('<w:p><w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>'
            '<w:r><w:rPr><w:b/><w:sz w:val="{}"/></w:rPr>'
            '<w:t xml:space="preserve">{}</w:t></w:r></w:p>'.format(size, text))


def body_text(text, bold=False, italic=False):
    rpr = ""
    if bold or italic:
        rpr = "<w:rPr>{}{}</w:rPr>".format("<w:b/>" if bold else "",
                                           "<w:i/>" if italic else "")
    return ('<w:p><w:r>{}<w:t xml:space="preserve">{}</w:t></w:r></w:p>'
            .format(rpr, text))


def build():
    E = equations()
    body = []
    body.append(heading("Equations (1)\u2013(27) \u2014 Live Word Equation Objects", 32))
    body.append(body_text(
        "Each equation below is a native, editable Microsoft Word equation "
        "(OMML). Click any equation to edit it with the Equation Tools ribbon, "
        "or copy-paste it directly into the manuscript.", italic=True))

    body.append(heading("Section 2.4 \u2014 Governing and property equations"))
    labels = {
        1: "Nanofluid density", 2: "Nanofluid heat capacity",
        3: "Nanofluid specific heat", 4: "Nanofluid viscosity (Einstein)",
        5: "Nanofluid thermal conductivity (Maxwell)",
        6: "Hybrid equivalent particle density",
        7: "Hybrid equivalent particle heat capacity",
        8: "Hybrid equivalent particle conductivity",
        9: "Coolant mean velocity", 10: "Hydraulic diameter",
        11: "Reynolds number", 12: "Prandtl number",
        13: "Coolant mass flow rate", 14: "Heat rejected (coolant side)",
        15: "Heat gained (air side)", 16: "Energy balance",
        17: "Log-mean temperature difference",
        18: "Coolant-side convective coefficient", 19: "Nusselt number",
        20: "Minimum heat-capacity rate", 21: "Maximum possible heat transfer",
        22: "Radiator effectiveness", 23: "Power-law Nusselt correlation",
        24: "Pearson correlation coefficient", 25: "Mean square error",
        26: "Root mean square error", 27: "Mean absolute error",
    }
    for n in range(1, 24):
        body.append(body_text("Eq. ({}) \u2014 {}".format(n, labels[n]), bold=True))
        body.append(math_para(E[n], n))

    body.append(heading("Section 3.5 \u2014 Machine-learning performance metrics"))
    for n in range(24, 28):
        body.append(body_text("Eq. ({}) \u2014 {}".format(n, labels[n]), bold=True))
        body.append(math_para(E[n], n))

    content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                     '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                     '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                     '<Default Extension="xml" ContentType="application/xml"/>'
                     '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                     '</Types>')
    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
                 '</Relationships>')

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        + M + '>'
        '<w:body>' + "".join(body) +
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
        '</w:sectPr></w:body></w:document>'
    )

    with zipfile.ZipFile(OUT_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("word/document.xml", document)

    print("Created {}".format(OUT_PATH))


if __name__ == "__main__":
    build()
