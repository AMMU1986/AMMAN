#!/usr/bin/env python3
"""
Generate Nomenclature.docx using only the Python standard library.

A .docx is a ZIP archive of Open Office XML parts. We build the minimal set of
parts required for a valid Word document: content-types, package rels,
document rels, and the main document body (headings, paragraphs, and tables).

No third-party packages required (works offline).
"""

import zipfile
from xml.sax.saxutils import escape

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


# ----------------------------------------------------------------------------
# Data: (symbol, description, unit).  Unit column omitted where not applicable.
# ----------------------------------------------------------------------------

general_symbols = [
    ("a_P", "Coefficient of the central computational point in the discretized equation", "\u2013"),
    ("a_nb", "Coefficients of neighbouring nodes", "\u2013"),
    ("b", "Source term in the discretized equation", "\u2013"),
    ("C_p", "Specific heat capacity at constant pressure", "J kg\u207b\u00b9 K\u207b\u00b9"),
    ("d", "Displacement vector (residual-based correction)", "\u2013"),
    ("\u2016d\u2016", "Euclidean (2-)norm of the displacement vector", "\u2013"),
    ("D", "Fluid domain / gap width (conjugate ratio Dk_f/Lk_w)", "m"),
    ("e_n", "Error in tuning index at iteration n", "\u2013"),
    ("g", "Gravitational acceleration", "m s\u207b\u00b2"),
    ("Gr", "Grashof number", "\u2013"),
    ("k", "Thermal conductivity", "W m\u207b\u00b9 K\u207b\u00b9"),
    ("L", "Solid wall thickness (conjugate ratio Dk_f/Lk_w)", "m"),
    ("Nu", "Nusselt number", "\u2013"),
    ("P", "Pressure", "Pa"),
    ("Pe", "P\u00e9clet number", "\u2013"),
    ("Ra", "Rayleigh number", "\u2013"),
    ("Re", "Reynolds number", "\u2013"),
    ("T", "Temperature", "K"),
    ("T_c", "Cold-wall temperature", "K"),
    ("T_h", "Hot-wall temperature", "K"),
    ("u", "Velocity component in x-direction", "m s\u207b\u00b9"),
    ("U", "Lid (top-wall) velocity", "m s\u207b\u00b9"),
    ("v", "Velocity component in y-direction", "m s\u207b\u00b9"),
    ("x, y", "Cartesian coordinates", "m"),
]

greek_symbols = [
    ("\u03b1", "Under-relaxation factor (0 < \u03b1 \u2264 1)", "\u2013"),
    ("\u03b1\u2080", "Initial relaxation factor", "\u2013"),
    ("\u0394\u03b1", "Change in relaxation factor (ANFIS output)", "\u2013"),
    ("\u03b2", "Thermal expansion coefficient", "K\u207b\u00b9"),
    ("\u03b3_n", "Tuning index at iteration n", "\u2013"),
    ("\u0394e_n", "Change in error at iteration n", "\u2013"),
    ("\u03bc", "Dynamic viscosity", "Pa s"),
    ("\u03c1", "Density", "kg m\u207b\u00b3"),
    ("\u03d5", "Nanoparticle volume fraction", "\u2013"),
    ("\u03c6_P", "Generic transported variable at point P", "\u2013"),
    ("\u03c6_nb", "Generic transported variable at neighbouring nodes", "\u2013"),
]

subscripts = [
    ("c", "Cold (wall)"),
    ("f", "Base fluid"),
    ("h", "Hot (wall)"),
    ("n", "Current iteration"),
    ("n\u22121", "Previous iteration"),
    ("n+1", "Next iteration"),
    ("nb", "Neighbouring node"),
    ("nf", "Nanofluid (effective property)"),
    ("P", "Central computational point"),
    ("s", "Solid nanoparticle"),
]

superscripts = [
    ("*", "Updated (under-relaxed) value of a variable"),
    ("2", "Second-order (used in second derivatives, e.g. \u2202\u00b2u/\u2202x\u00b2)"),
]

acronyms = [
    ("ANFIS", "Adaptive-Network-Based Fuzzy Inference System"),
    ("CFD", "Computational Fluid Dynamics"),
    ("CHT", "Conjugate Heat Transfer"),
    ("CPU", "Central Processing Unit"),
    ("SIMPLER", "Semi-Implicit Method for Pressure-Linked Equations Revised"),
    ("SOR", "Successive Over-Relaxation"),
]


# ----------------------------------------------------------------------------
# XML builders
# ----------------------------------------------------------------------------

def run(text, bold=False, italic=False):
    props = ""
    if bold or italic:
        props = "<w:rPr>" + ("<w:b/>" if bold else "") + ("<w:i/>" if italic else "") + "</w:rPr>"
    return f'<w:r>{props}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def para(text="", bold=False, italic=False, size=None, style=None):
    ppr = ""
    inner = ""
    if style == "title":
        inner = '<w:jc w:val="center"/><w:spacing w:after="200"/>'
    if size or bold or italic:
        rpr = "<w:rPr>"
        if bold:
            rpr += "<w:b/>"
        if italic:
            rpr += "<w:i/>"
        if size:
            rpr += f'<w:sz w:val="{size*2}"/>'
        rpr += "</w:rPr>"
    else:
        rpr = ""
    if inner:
        ppr = f"<w:pPr>{inner}</w:pPr>"
    if text == "":
        return f"<w:p>{ppr}</w:p>"
    run_props = ""
    if bold or italic or size:
        run_props = "<w:rPr>"
        if bold:
            run_props += "<w:b/>"
        if italic:
            run_props += "<w:i/>"
        if size:
            run_props += f'<w:sz w:val="{size*2}"/>'
        run_props += "</w:rPr>"
    return (f"<w:p>{ppr}<w:r>{run_props}"
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')


def heading(text, level=1):
    size = {1: 15, 2: 13}.get(level, 12)
    return para(text, bold=True, size=size)


def cell(text, bold=False, width=None):
    wprops = ""
    if width:
        wprops = f'<w:tcW w:w="{width}" w:type="dxa"/>'
    tcpr = f"<w:tcPr>{wprops}</w:tcPr>" if wprops else ""
    run_props = "<w:rPr><w:b/></w:rPr>" if bold else ""
    return (f"<w:tc>{tcpr}<w:p><w:r>{run_props}"
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p></w:tc>')


def table(header, rows, widths):
    borders = (
        "<w:tblBorders>"
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        "</w:tblBorders>"
    )
    tblpr = f'<w:tblPr><w:tblW w:w="0" w:type="auto"/>{borders}</w:tblPr>'
    grid = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{w}"/>' for w in widths) + "</w:tblGrid>"
    hdr = "<w:tr>" + "".join(cell(h, bold=True, width=w) for h, w in zip(header, widths)) + "</w:tr>"
    body = ""
    for r in rows:
        body += "<w:tr>" + "".join(cell(c, width=w) for c, w in zip(r, widths)) + "</w:tr>"
    return f"<w:tbl>{tblpr}{grid}{hdr}{body}</w:tbl>"


# ----------------------------------------------------------------------------
# Assemble document
# ----------------------------------------------------------------------------

def build_document_xml():
    body = []
    body.append(para("Nomenclature", bold=True, size=18, style="title"))
    body.append(para(
        "Manuscript: From Pure Fluids to Nanofluids: Extending ANFIS-Based "
        "Convergence Control to Dispersed Phase Heat Transfer",
        italic=True, size=10))
    body.append(para(""))

    body.append(heading("General Symbols (Roman)", 2))
    body.append(table(["Symbol", "Description", "Unit"], general_symbols, [1500, 6500, 1800]))
    body.append(para(""))

    body.append(heading("Greek Symbols", 2))
    body.append(table(["Symbol", "Description", "Unit"], greek_symbols, [1500, 6500, 1800]))
    body.append(para(""))

    body.append(heading("Subscripts", 2))
    body.append(table(["Subscript", "Description"], subscripts, [1800, 8000]))
    body.append(para(""))

    body.append(heading("Superscripts", 2))
    body.append(table(["Superscript", "Description"], superscripts, [1800, 8000]))
    body.append(para(""))

    body.append(heading("Abbreviations / Acronyms", 2))
    body.append(table(["Acronym", "Definition"], acronyms, [1800, 8000]))
    body.append(para(""))

    body.append(heading("Notes", 2))
    body.append(para(
        "1. The symbol \u03c6 (phi) is recommended for the generic transported "
        "variable, while \u03d5 (or \u03c6\u1d65) is recommended for the "
        "nanoparticle volume fraction, to avoid overloading a single glyph "
        "across Eqs. (5)\u2013(11)."))
    body.append(para(
        "2. The conjugate conduction\u2013convection ratio appears as both "
        "Dk_f/Lk_w (Sec. 2.5) and Lk_w/Dk_f (Sec. 3.3); recommend using one "
        "consistent form throughout."))

    doc = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:document xmlns:w="{W}"><w:body>'
        + "".join(body)
        + '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
        'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
        "</w:body></w:document>"
    )
    return doc


CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    "</Types>"
)

RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
    'Target="word/document.xml"/>'
    "</Relationships>"
)


def main(out_path="Nomenclature.docx"):
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/document.xml", build_document_xml())
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
