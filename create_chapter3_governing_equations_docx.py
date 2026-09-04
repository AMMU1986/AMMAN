#!/usr/bin/env python3
"""
Create a Word .docx file for Chapter 3: Governing Equations and Modelling.

Water-based Al2O3-TiO2-CuO ternary hybrid nanofluid (THNF) flat-tube
heat-exchanger study.

Uses raw OOXML (ZIP + XML) since python-docx is not available in this sandbox,
mirroring the conventions of build_chapter4.py / create_chapter_docx.py.

Equations are rendered legibly using Unicode subscripts/superscripts and Greek
letters, with equation numbers kept in parentheses as in the existing chapter
scripts.
"""

import zipfile
import os

output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Chapter_3_Governing_Equations_and_Modelling.docx",
)

# ===== XML Templates =====
content_types_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

doc_rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
    <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="240" w:after="240"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="36"/><w:szCs w:val="36"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
</w:styles>'''


def esc(text):
    """Escape special XML characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def para(text, bold=False, italic=False, size=24, align="both", style=None):
    """A simple single-run paragraph."""
    parts = ['<w:p><w:pPr>']
    if style:
        parts.append(f'<w:pStyle w:val="{style}"/>')
    parts.append(f'<w:jc w:val="{align}"/>')
    parts.append('</w:pPr><w:r><w:rPr>')
    if bold:
        parts.append('<w:b/>')
    if italic:
        parts.append('<w:i/>')
    parts.append(
        f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
    )
    parts.append(f'</w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')
    return "".join(parts)


def heading(text, level=1):
    return para(text, bold=True, size={1: 32, 2: 28}.get(level, 24),
                style=f"Heading{level}", align="left")


def equation(number, expr, size=24):
    """
    Render an equation paragraph: the mathematical expression in italic on the
    left, and the equation number in parentheses right-aligned via a tab stop.
    """
    # Right-aligned tab stop near the page margin so equation numbers line up.
    ppr = (
        '<w:pPr>'
        '<w:tabs><w:tab w:val="right" w:pos="9360"/></w:tabs>'
        '<w:spacing w:before="60" w:after="60"/>'
        '<w:jc w:val="left"/>'
        '</w:pPr>'
    )
    expr_run = (
        '<w:r><w:rPr><w:i/>'
        f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
        f'</w:rPr><w:t xml:space="preserve">{esc(expr)}</w:t></w:r>'
    )
    tab_run = '<w:r><w:tab/></w:r>'
    num_run = (
        '<w:r><w:rPr>'
        f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
        f'</w:rPr><w:t xml:space="preserve">({number})</w:t></w:r>'
    )
    return f'<w:p>{ppr}{expr_run}{tab_run}{num_run}</w:p>'


# ===== Unicode helpers for legible maths =====
# Greek letters
phi = "\u03c6"        # φ
rho = "\u03c1"        # ρ
mu = "\u03bc"         # μ
eta = "\u03b7"        # η
DELTA = "\u0394"      # Δ  (delta P as pressure drop)
SIGMA = "\u03a3"      # Σ
# Subscripts
sub = {
    "0": "\u2080", "1": "\u2081", "2": "\u2082", "3": "\u2083",
    "c": "\u1d04", "h": "\u2095", "w": "\u1d21", "m": "\u2098",
    "b": "\u1d47", "s": "\u209b", "p": "\u209a", "i": "\u1d62",
    "j": "\u2c7c", "k": "\u2096", "n": "\u2099", "N": "\u2099",
}
# Superscripts
sup = {
    "2": "\u00b2", "-1": "\u207b\u00b9", "-2": "\u207b\u00b2",
    "T": "\u1d40", "1/3": "\u00b9\u141f\u00b3",
}

# Convenience Unicode composites used across equations
DP = DELTA + "P"                 # ΔP  (pressure drop)
Sgen = "S" + "\u1d67\u2091\u2099"  # S_gen (approx via small caps subscripts) -> fallback below

# The subscript Unicode set is incomplete for multi-letter subscripts such as
# "gen", "gen,T", "Al2O3", "THNF", "bf", "in", "out". For readability and to
# avoid missing glyphs, multi-letter subscripts are written with an underscore
# notation (e.g. S_gen, T_in), which is unambiguous and journal-friendly.

# ===== DOCUMENT BODY =====
body = []

# Title
body.append(para("3. Governing Equations and Modelling", style="Title", align="center"))

# Intro
body.append(para(
    "The thermal-hydraulic behaviour of the water-based Al\u2082O\u2083-TiO\u2082-CuO "
    "ternary hybrid nanofluid (THNF) flowing through the rectangular flat-tube "
    "heat exchanger was evaluated using the conservation of mass and energy, "
    "together with standard dimensionless heat-transfer and flow-resistance "
    "parameters. The experimental configuration consisted of an aluminium "
    "flat-tube channel of length L = 800 mm, width W = 40 mm, and height "
    "H = 3 mm, giving a hydraulic diameter of approximately 5.58 mm. A uniform "
    "heat flux of q\u2033 = 5000 W m\u207b\u00b2 was imposed on the test section."
))

# ---- 3.1 ----
body.append(heading("3.1 Thermophysical and Flow Model", 2))
body.append(para(
    "The total nanoparticle volume fraction of the ternary hybrid nanofluid is "
    "defined as the ratio of the combined nanoparticle volume to the total "
    "suspension volume:"
))
body.append(equation(
    "1",
    f"{phi} = (V_Al\u2082O\u2083 + V_TiO\u2082 + V_CuO) / "
    f"(V_Al\u2082O\u2083 + V_TiO\u2082 + V_CuO + V_bf)"
))
body.append(para(
    "where V_Al\u2082O\u2083, V_TiO\u2082, and V_CuO are the volumes of the three "
    "nanoparticles and V_bf is the volume of the base fluid. The present "
    "investigation considers total nanoparticle concentrations between 0.05 "
    "and 0.20 vol.%."
))
body.append(para("The flow cross-sectional area of the rectangular flat tube is given by:"))
body.append(equation("2", "A_c = W H"))
body.append(para("and the corresponding wetted perimeter is:"))
body.append(equation("3", "P_w = 2(W + H)"))
body.append(para("The hydraulic diameter follows directly as:"))
body.append(equation("4", "D_h = 4 A_c / P_w"))
body.append(para("which, for a rectangular cross-section, reduces to:"))
body.append(equation("5", "D_h = 2 W H / (W + H)"))
body.append(para(
    "For the present geometry this yields D_h \u2248 5.58 mm and an aspect ratio "
    "of W/H \u2248 13.3."
))
body.append(para("The mean velocity of the working fluid is obtained from the measured mass flow rate as:"))
body.append(equation("6", f"u_m = m\u0307 / ({rho} A_c)"))
body.append(para(
    f"where m\u0307 is the mass flow rate and {rho} is the density of the THNF."
))
body.append(para("The Reynolds number, which characterises the flow regime, is defined as:"))
body.append(equation("7", f"Re = {rho} u_m D_h / {mu}"))
body.append(para(
    f"where {mu} is the dynamic viscosity of the THNF. All experiments were "
    "conducted under turbulent-flow conditions in the range Re = 4000-16000."
))
body.append(para(
    "The bulk mean temperature of the fluid is approximated by the arithmetic "
    "mean of the inlet and outlet temperatures:"
))
body.append(equation("8", "T_b = (T_in + T_out) / 2"))
body.append(para(
    "where T_in and T_out are the measured inlet and outlet temperatures, "
    "respectively. The temperature-dependent thermophysical properties were "
    "evaluated over the experimental range of 30-60 \u00b0C."
))

# ---- 3.2 ----
body.append(heading("3.2 Energy Balance and Heat-Transfer Model", 2))
body.append(para(
    "Under steady-state conditions, the heat transferred to the THNF is "
    "determined from the measured mass flow rate and temperature rise:"
))
body.append(equation("9", "Q\u0307 = m\u0307 C_p (T_out - T_in)"))
body.append(para("where C_p is the specific heat capacity of the THNF."))
body.append(para(
    "For the constant heat-flux boundary condition, the applied heat flux "
    "relates to the heat-transfer rate through:"
))
body.append(equation("10", "q\u2033 = Q\u0307 / A_s"))
body.append(para(
    "where A_s is the effective heat-transfer surface area, and the "
    "experimental heat flux was maintained at 5000 W m\u207b\u00b2. For the "
    "rectangular flat-tube test section, this area is expressed as:"
))
body.append(equation("11", "A_s = 2(W + H) L"))
body.append(para("The average convective heat-transfer coefficient is then calculated from:"))
body.append(equation("12", "h = Q\u0307 / [A_s (T_w - T_b)]"))
body.append(para(
    "where T_w is the mean wall temperature and T_b is the bulk fluid "
    "temperature. The corresponding Nusselt number is:"
))
body.append(equation("13", "Nu = h D_h / k"))
body.append(para("where k is the thermal conductivity of the THNF."))
body.append(para(
    "The percentage enhancement in heat-transfer coefficient relative to the "
    "base fluid is evaluated as:"
))
body.append(equation("14", "%Enh_h = [(h_THNF - h_bf) / h_bf] \u00d7 100"))
body.append(para("and, similarly, the Nusselt-number enhancement is:"))
body.append(equation("15", "%Enh_Nu = [(Nu_THNF - Nu_bf) / Nu_bf] \u00d7 100"))
body.append(para(
    "The experimental results show that the highest THNF concentration and "
    "Reynolds number produced improvements of approximately 13.6 % in Nusselt "
    "number and 25.5 % in heat-transfer coefficient relative to deionised water."
))

# ---- 3.3 ----
body.append(heading("3.3 Pressure Drop and Friction Factor Model", 2))
body.append(para(
    "The hydraulic resistance of the flat-tube channel was quantified from the "
    "pressure drop measured across the test section. The Darcy friction factor "
    "is calculated as:"
))
body.append(equation("16", f"f = 2 {DP} D_h / ({rho} u_m\u00b2 L)"))
body.append(para(
    f"where {DP} is the pressure drop between the inlet and outlet pressure "
    "taps and L is the test-section length; the differential pressure was "
    "recorded using the facility's pressure transducer."
))
body.append(para("The percentage increase in friction factor caused by nanoparticle addition is determined from:"))
body.append(equation("17", "%Penalty_f = [(f_THNF - f_bf) / f_bf] \u00d7 100"))
body.append(para(
    "The results indicate that increasing nanoparticle concentration raises the "
    f"friction factor, with a maximum penalty of approximately 20-21 % at "
    f"{phi} = 0.20 %."
))
body.append(para("The pumping power required to overcome the pressure loss is expressed as:"))
body.append(equation("18", f"P_p = m\u0307 {DP} / {rho}"))
body.append(para(
    "The thermal benefit of the THNF must therefore be assessed simultaneously "
    "with its associated hydraulic penalty."
))

# ---- 3.4 ----
body.append(heading("3.4 Thermal-Hydraulic Performance", 2))
body.append(para(
    "To evaluate the combined influence of heat-transfer enhancement and "
    "frictional losses, the thermal-hydraulic performance factor is defined as:"
))
body.append(equation("19", f"{eta} = (Nu_THNF / Nu_bf) / (f_THNF / f_bf)^(1/3)"))
body.append(para(
    "where the subscripts THNF and bf denote the ternary hybrid nanofluid and "
    f"the base fluid, respectively. A value of {eta} > 1 indicates that the "
    "improvement in heat transfer outweighs the additional hydraulic "
    "resistance. The present study reports a performance factor greater than "
    "unity throughout the investigated operating range, reaching a maximum of "
    "approximately 1.25."
))

# ---- 3.5 ----
body.append(heading("3.5 Entropy Generation Model", 2))
body.append(para(
    "A second-law analysis was employed to quantify the thermodynamic "
    "irreversibility arising from heat transfer and fluid friction. The total "
    "entropy generation rate is expressed as the sum of thermal and frictional "
    "contributions:"
))
body.append(equation("20", "S_gen = S_gen,T + S_gen,F"))
body.append(para(
    "where S_gen,T and S_gen,F denote the thermal and frictional "
    "entropy-generation rates, respectively."
))
body.append(para(
    "The thermal entropy-generation rate associated with finite-temperature "
    "heat transfer is calculated as:"
))
body.append(equation("21", "S_gen,T = Q\u0307\u00b2 / (h A_s T_b\u00b2)"))
body.append(para("while the frictional entropy-generation rate resulting from pressure losses is given by:"))
body.append(equation("22", f"S_gen,F = m\u0307 {DP} / ({rho} T_b)"))
body.append(para("Combining these contributions gives the total entropy-generation rate:"))
body.append(equation("23", f"S_gen = Q\u0307\u00b2 / (h A_s T_b\u00b2) + m\u0307 {DP} / ({rho} T_b)"))
body.append(para(
    "This formulation allows the competing effects of improved heat transfer "
    "and increased viscous resistance to be quantified within a common "
    "second-law framework - a consideration that is particularly relevant to "
    "the present THNF, in which increasing nanoparticle concentration improves "
    "thermal performance while simultaneously increasing frictional losses."
))
body.append(para(
    "The Bejan number is subsequently defined as the ratio of thermal entropy "
    "generation to total entropy generation:"
))
body.append(equation("24", "Be = S_gen,T / (S_gen,T + S_gen,F)"))
body.append(para(
    "A high Bejan number indicates dominance of thermal irreversibility, "
    "whereas a low value indicates that frictional irreversibility prevails. "
    "The experimental results reveal a transition from thermal- to "
    "friction-dominated irreversibility as the Reynolds number increases."
))

# ---- 3.6 ----
body.append(heading("3.6 Thermophysical Property Enhancement", 2))
body.append(para("The thermal-conductivity enhancement relative to the base fluid is calculated using:"))
body.append(equation("25", "%Enh_k = [(k_THNF - k_bf) / k_bf] \u00d7 100"))
body.append(para("and the relative viscosity increase is expressed as:"))
body.append(equation("26", f"%Inc_{mu} = [({mu}_THNF - {mu}_bf) / {mu}_bf] \u00d7 100"))
body.append(para(
    "These parameters are particularly important because thermal conductivity "
    "directly influences the convective heat-transfer coefficient, whereas "
    "viscosity governs the Reynolds number, pressure drop, friction factor, "
    "and frictional entropy generation. The THNF thermal conductivity increases "
    "with both temperature and nanoparticle concentration, while the viscosity "
    "penalty diminishes at elevated temperatures."
))

# ---- 3.7 ----
body.append(heading("3.7 Artificial Neural Network Modelling", 2))
body.append(para(
    "In addition to the experimental data-reduction model, a feedforward "
    "artificial neural network (ANN) was developed to predict the principal "
    "thermal-hydraulic parameters. The network architecture comprises four "
    "input neurons, two hidden layers containing 10 and 8 neurons, "
    "respectively, and three output neurons (a 4-10-8-3 configuration). The "
    "four inputs are Reynolds number, nanoparticle volume fraction, inlet "
    "temperature, and mass flow rate, while the outputs are Nusselt number, "
    "friction factor, and heat-transfer coefficient."
))
body.append(para("The input vector is defined as:"))
body.append(equation("27", f"X = [Re  {phi}  T_in  m\u0307]\u1d40"))
body.append(para("and the output vector as:"))
body.append(equation("28", "Y = [Nu  f  h]\u1d40"))
body.append(para(
    "Prior to training, the input and output variables are normalised to "
    "improve numerical stability. A general min-max normalisation is expressed "
    "as:"
))
body.append(equation("29", "X_N = (X - X_min) / (X_max - X_min)"))
body.append(para("For neuron j in a hidden layer, the weighted input is:"))
body.append(equation("30", f"z_j = {SIGMA}\u1d62\u208c\u2081\u207f w_ij x_i + b_j"))
body.append(para("where w_ij is the connection weight and b_j is the neuron bias. The nonlinear activation is represented by the hyperbolic tangent function:"))
body.append(equation("31", "a_j = tanh(z_j)"))
body.append(para("which may equivalently be written as:"))
body.append(equation("32", "a_j = 2 / [1 + exp(-2 z_j)] - 1"))
body.append(para("The output layer then provides the predicted thermal-hydraulic parameters according to:"))
body.append(equation("33", f"\u0176_k = {SIGMA}\u2c7c\u208c\u2081\u207f w_jk a_j + b_k"))
body.append(para(
    "where \u0176_k represents the ANN prediction of Nu, f, or h. The overall "
    "ANN mapping can therefore be represented compactly as:"
))
body.append(equation("34", "\u0176 = W\u2083 f\u2082 [ W\u2082 f\u2081 ( W\u2081 X + b\u2081 ) + b\u2082 ] + b\u2083"))
body.append(para(
    "where W\u2081, W\u2082, and W\u2083 are the weight matrices and b\u2081, b\u2082, "
    "and b\u2083 are the corresponding bias vectors. The network was trained "
    "using the Levenberg-Marquardt backpropagation algorithm."
))

# ---- 3.8 ----
body.append(heading("3.8 ANN Performance Evaluation", 2))
body.append(para("The prediction error was assessed using several statistical metrics. The mean squared error is defined as:"))
body.append(equation("35", "MSE = (1/N) \u03a3\u1d62\u208c\u2081\u1d3a (y_i - \u0177_i)\u00b2"))
body.append(para("the root mean square error as:"))
body.append(equation("36", "RMSE = \u221a[ (1/N) \u03a3\u1d62\u208c\u2081\u1d3a (y_i - \u0177_i)\u00b2 ]"))
body.append(para("and the coefficient of determination as:"))
body.append(equation("37", "R\u00b2 = 1 - [ \u03a3\u1d62\u208c\u2081\u1d3a (y_i - \u0177_i)\u00b2 ] / [ \u03a3\u1d62\u208c\u2081\u1d3a (y_i - \u0233)\u00b2 ]"))
body.append(para(
    "where y_i, \u0177_i, and \u0233 denote the experimental value, the "
    "ANN-predicted value, and the mean experimental value, respectively. The "
    "mean absolute percentage error is determined from:"
))
body.append(equation("38", "MAPE = (100/N) \u03a3\u1d62\u208c\u2081\u1d3a | (y_i - \u0177_i) / y_i |"))
body.append(para(
    "The developed ANN demonstrated high predictive accuracy, with R\u00b2 values "
    "exceeding approximately 0.987 and MAPE values below 1.2 % for the "
    "principal predicted parameters."
))

# ---- 3.9 ----
body.append(heading("3.9 Modelling and Optimisation Framework", 2))
body.append(para(
    "The complete modelling framework therefore integrates experimental "
    "thermophysical characterisation, energy-balance calculations, "
    "dimensionless heat-transfer analysis, pressure-drop analysis, "
    "entropy-generation minimisation, and ANN-based prediction. The governing "
    "relationships in Eqs. (1)-(26) generate the experimentally derived "
    "thermal-hydraulic and thermodynamic response variables, while Eqs. "
    "(27)-(38) define the ANN-based surrogate model. Conceptually, the "
    "framework can be represented as the mapping:"
))
body.append(equation(
    "39",
    f"{{Re, {phi}, T_in, m\u0307}} \u2192 {{Nu, f, h}} \u2192 "
    f"{{{eta}, S_gen, Be}}"
))
body.append(para(
    "This integrated approach enables the competing effects of nanoparticle "
    "concentration and flow rate to be evaluated simultaneously. In particular, "
    "the analysis identifies Reynolds number as the most influential ANN input, "
    "followed by nanoparticle volume fraction, inlet temperature, and mass flow "
    "rate."
))

# ---- Closing note ----
body.append(para(""))
body.append(para(
    "Note for journal submission: Eqs. (21)-(24) should be verified against the "
    "exact entropy-generation formulation and temperature reference used in "
    "your experimental calculations before final submission, since "
    "entropy-generation expressions can differ depending on whether local or "
    "mean temperatures and hydraulic-volume definitions are adopted. The "
    "uploaded manuscript supports the thermal/frictional decomposition and "
    "Bejan analysis but does not provide the full original derivation of these "
    "equations.",
    italic=True,
))


def create_docx():
    body_xml = "\n".join(body)
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">\n'
        '  <w:body>\n'
        f'{body_xml}\n'
        '    <w:sectPr>\n'
        '      <w:pgSz w:w="12240" w:h="15840"/>\n'
        '      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
        'w:header="720" w:footer="720" w:gutter="0"/>\n'
        '    </w:sectPr>\n'
        '  </w:body>\n'
        '</w:document>'
    )

    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml)
        zf.writestr("_rels/.rels", rels_xml)
        zf.writestr("word/_rels/document.xml.rels", doc_rels_xml)
        zf.writestr("word/document.xml", document_xml)
        zf.writestr("word/styles.xml", styles_xml)

    size_kb = os.path.getsize(output_file) / 1024
    print(f"Successfully created: {output_file}")
    print(f"File size: {size_kb:.1f} KB")


if __name__ == "__main__":
    create_docx()
