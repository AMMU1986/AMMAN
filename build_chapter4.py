#!/usr/bin/env python3
"""
Build Chapter 4: Experimentation as a proper .docx file.
A .docx file is a ZIP archive with specific XML structure.
"""

import zipfile
import os
import shutil
from pathlib import Path

output_file = "/projects/sandbox/AMMAN/Chapter_4_Experimentation.docx"

# Available figures to embed
figures = [
    "/projects/sandbox/AMMAN/figures/Figure_1.png",  # rId7 - Ternary diagrams
    "/projects/sandbox/AMMAN/figures/Figure_2.png",  # rId8 - Multipass beads
    "/projects/sandbox/AMMAN/figures/Figure_3.png",  # rId9 - Thermophysical props
    "/projects/sandbox/AMMAN/figures/Figure_4.png",  # rId10 - XRD patterns
    "/projects/sandbox/AMMAN/figures/Figure_5.png",  # rId11 - FTIR spectra
]

# Verify figures exist
for f in figures:
    if os.path.exists(f):
        size = os.path.getsize(f)
        print(f"  OK: {f} ({size} bytes)")
    else:
        print(f"  MISSING: {f}")

# ===== XML Templates =====

content_types_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

# Build word/_rels/document.xml.rels with image references
doc_rels_parts = [
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
    '  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
]
for i, fig in enumerate(figures):
    rid = f"rId{i+7}"
    fname = f"media/image{i+1}.png"
    doc_rels_parts.append(f'  <Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{fname}"/>')
doc_rels_parts.append('</Relationships>')
doc_rels_xml = "\n".join(doc_rels_parts)

styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:pPr><w:spacing w:before="160" w:after="80"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr><w:tblBorders>
      <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    </w:tblBorders></w:tblPr>
  </w:style>
</w:styles>'''


def esc(text):
    """Escape XML special characters."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def para(text, bold=False, size=24, align="both", style=None):
    """Generate paragraph XML."""
    parts = []
    parts.append('<w:p><w:pPr>')
    if style:
        parts.append(f'<w:pStyle w:val="{style}"/>')
    parts.append(f'<w:jc w:val="{align}"/>')
    parts.append('</w:pPr>')
    parts.append('<w:r><w:rPr>')
    if bold:
        parts.append('<w:b/>')
    parts.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    parts.append(f'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>')
    parts.append('</w:rPr>')
    parts.append(f'<w:t xml:space="preserve">{esc(text)}</w:t>')
    parts.append('</w:r></w:p>')
    return "".join(parts)


def heading(text, level=1):
    """Generate heading."""
    return para(text, bold=True, size={1:32, 2:28, 3:26}.get(level, 24), style=f"Heading{level}")


def img(rid, cx=5400000, cy=3600000, caption=""):
    """Generate image paragraph with optional caption."""
    xml = f'''<w:p><w:pPr><w:jc w:val="center"/></w:pPr>
<w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
<wp:extent cx="{cx}" cy="{cy}"/>
<wp:docPr id="1" name="Picture"/>
<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:nvPicPr><pic:cNvPr id="0" name="img"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed="{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''
    if caption:
        xml += para(caption, bold=True, size=20, align="center")
    return xml


def table_row(cells, bold=False):
    """Create table row."""
    row = "<w:tr>"
    for c in cells:
        b = "<w:b/>" if bold else ""
        row += f'<w:tc><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr>{b}<w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t xml:space="preserve">{esc(str(c))}</w:t></w:r></w:p></w:tc>'
    row += "</w:tr>"
    return row


def table(headers, rows):
    """Create table."""
    t = '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="5000" w:type="pct"/></w:tblPr>'
    t += table_row(headers, bold=True)
    for r in rows:
        t += table_row(r)
    t += '</w:tbl>'
    return t


# ===== BUILD DOCUMENT BODY =====
body = []

# Title
body.append(heading("Chapter 4: Experimentation", 1))
body.append(para(""))

# 4.1
body.append(heading("4.1. Selection of Suitable Minerals Used as Fluxes for Submerged Arc Welding", 2))
body.append(para("Controlled mineral blends that are optimized to harsh and saltwater conditions were developed into fluxes to be used in marine and offshore welding applications. The main mineral ingredients, silica (SiO\u2082), titanium dioxide (TiO\u2082), calcium fluoride (CaF\u2082), barium oxide (BaO), manganese oxide (MnO), and calcium oxide (CaO) were mixed in controlled ratios and CaO kept constant to stabilize slag chemistry. The purity of mineral powders used was 99%, and the composition of each batch was checked through X-ray fluorescence (XRF) analysis to guarantee reproducibility and quality control of the composition."))
body.append(para(""))
body.append(para("The selection of each mineral constituent was based on its specific functional role in the submerged arc welding process. Silica (A) was adjusted to 5.0 to 10.0 g, which offers fluxing activity, and slag fluidity. The titanium dioxide (B) level varied between 10.0 and 20.0 g in order to enhance the arc stability and slag detachability. Calcium fluoride was added to reduce the melting point; adding fluoride of calcium (C) 20.0 to 35.0 g was taken to create well offshore welding conditions. Barium oxide (D) was also loaded in 5.0-10.0 g to stabilize the arc effectiveness and help in the formation of slag and manganese (E) was loaded in 10.0-25.0 g, as a deoxidizer and refining the weld-metal microstructure. In each formulation shape, 8.0 g calcium oxide (F) was incorporated as a baseline basic condition and to ensure control of slag viscosity."))
body.append(para(""))
body.append(para("The mineral constituent composition ranges for flux formulation are summarized in Table 4.1. As an innovative additive, red ochre, which is an iron-edible by-product of iron-ore extraction in Rajasthan, India, was used. Being red ochre, it was dried in the oven at 110\u00b0C at a length of time of 24 h and milled to less than 45 \u00b5m before mixing. Inclusion levels were between 5.0 and 15.0 g per 100 g batch to substitute an equal fraction of silica to maintain total batch mass. With high iron levels red ochre increases electrical conductivity, arc stability and adjusts weld-metal chemistry and microstructure to better corrosion resistance."))
body.append(para(""))

# Table 4.1
body.append(para("Table 4.1: Mineral constituent composition ranges for flux formulation", bold=True, size=22, align="center"))
body.append(table(
    ["S. No", "Mineral Constituent", "Denoting Symbol", "Range (g/100g batch)"],
    [["1","SiO\u2082","A","5.0 \u2013 10.0"],["2","TiO\u2082","B","10.0 \u2013 20.0"],["3","CaF\u2082","C","20.0 \u2013 35.0"],["4","BaO","D","5.0 \u2013 10.0"],["5","MnO","E","10.0 \u2013 25.0"],["6","CaO","F","8.0 (constant)"]]
))
body.append(para(""))
body.append(para("Potassium silicate solution (5 wt%) of the batch was added as a binder, so that the mineral powders might adhere to the steel core. The powders were mixed in a turbula mixer 30 min after which they were dried in the oven at 80\u00b0C for 2 h."))
body.append(para(""))

# 4.1.1
body.append(heading("4.1.1. Design of Experimentation for Flux Formulation", 3))
body.append(para("The traditional trial-and-error method was replaced by a systematic Design of Experiments (DoE) approach to develop the 25 submerged arc welding fluxes. Mineral constituents (SiO\u2082, TiO\u2082, CaF\u2082, BaO, MnO and fixed CaO) are interdependent and an increase in one component necessarily requires a decrease in one or more other components, thus the mixture technique of Design of experiments was used. Design-Expert software (version 13, Stat-Ease Inc. Minneapolis, MN, USA) was used to design an experimental flux design matrix for SiO\u2082, TiO\u2082, CaF\u2082, BaO, MnO and fixed CaO ingredients (Table 4.2). The lower and upper bound constraints for the variables (Table 4.1) that are not possible in standard simplex-lattice or simplex-centroid designs, the D-optimal design is suitable. To minimize systematic bias, the replicates were randomly positioned in the design space."))
body.append(para(""))
body.append(para("The mixture formulation was designed according to the following mathematical constraints:"))
body.append(para("0 \u2264 \u03b1_i \u2264 x_i \u2264 \u03b2_i \u2264 100 \u2026 (Equation 4.1)", align="center"))
body.append(para("\u03a3x_i = 100 \u2026 (Equation 4.2)", align="center"))
body.append(para(""))
body.append(para("The initial letter of these expressions is x, this is the mass in grams of every mineral constituent in every batch of 100 g, while \u03b1_i and \u03b2_i serve as the lower and upper specifications of each element, which are detailed in Table 4.1. Equation (4.1) is used to make sure the amount of each single element is within a given range. The scale is able to adapt the mass variations brought by adding red ochre and binder materials."))
body.append(para(""))
body.append(para("The compositional range was analyzed based on a number of basic ternary systems as shown in Figure 4.1. The CaF\u2082 addition to the SiO\u2082-CaO-CaF\u2082 diagram (a) reduces the liquidus temperature and creates two-liquid zones, which are important in regulating the fluidity of slag. The SiO\u2082-MnO-TiO\u2082 system (b) plotted under controlled oxygen potential shows the effect of Mn and Ti in the formation and stability of silicate and titanate phases, and hence, the stability of the arc as well as the slag release. The BaO-SiO\u2082-CaF\u2082 system (c) also indicates a low-melting dual liquid phase near the SiO\u2082-CaF\u2082 interface, which means that the flux is easier to melt than the others. These ternary combinations are then further extended to a quaternary model SiO\u2082-CaF\u2082-MnO-BaO (d), whose polyhedral zone represents the scope of composition that is viable."))
body.append(para(""))

# Figure 4.1
body.append(img("rId7", 5400000, 4050000, "Figure 4.1: Representation of ternary and quaternary phase relationships used in flux formulation. (a) SiO\u2082\u2013CaO\u2013CaF\u2082, (b) SiO\u2082\u2013MnO\u2013TiO\u2082, (c) BaO\u2013SiO\u2082\u2013CaF\u2082, (d) Quaternary framework"))
body.append(para(""))

# Basicity Index
body.append(para("The basicity index (BI) of 25 fluxes were calculated by using equation (4.3) given by Tulliani:"))
body.append(para("BI = (CaO + CaF\u2082 + MgO + BaO + SrO + Na\u2082O) + 0.5(MnO + Fe) / SiO\u2082 + 0.5(TiO\u2082 + Al\u2082O\u2083 + ZrO\u2082) \u2026 (Eq. 4.3)", align="center"))
body.append(para(""))
body.append(para("This index was developed with an improved description of the fluxing and deoxidizing effect of CaF\u2082 and MnO, in addition to the conventional basic oxides. The resulting values of the basicity index ranged between 2.100 and 4.622 and virtually grouped the fluxes between acidic and strongly basic as indicated in Table 4.2. CaF\u2082 and MnO rich blends, e.g. Run 2, had the highest basicity and those with high levels of SiO\u2082 and TiO\u2082 had the lowest basicity. A high level of SiO\u2082 and TiO\u2082 reduced the basicity index which generally responsible in producing liquid slags. In contrast, BaO and the constant 8% CaO increased the index, which correlates with improved desulfurization potential and better slag detachability from the weld metal."))
body.append(para(""))

# Table 4.2
body.append(para("Table 4.2: Design matrix of flux composition", bold=True, size=22, align="center"))
t2_headers = ["Run","SiO\u2082","TiO\u2082","CaF\u2082","BaO","MnO","CaO","BI"]
t2_rows = [
    ["1","10.00","18.59","21.42","9.99","25.00","8.00","2.253"],
    ["2","6.37","10.17","35.00","8.46","25.00","8.00","4.622"],
    ["3","8.15","13.98","35.00","10.00","17.86","8.00","3.201"],
    ["4","7.94","15.42","30.09","6.55","25.00","8.00","2.981"],
    ["5","8.15","13.98","35.00","10.00","17.86","8.00","3.201"],
    ["6","5.29","20.00","27.44","7.28","25.00","8.00","2.677"],
    ["7","10.00","14.37","25.63","10.00","25.00","8.00","2.816"],
    ["8","7.94","15.42","30.09","6.55","25.00","8.00","2.981"],
    ["9","7.94","15.42","30.09","6.55","25.00","8.00","2.981"],
    ["10","7.99","20.00","28.17","10.00","18.84","8.00","2.322"],
    ["11","10.00","20.00","26.73","5.00","23.27","8.00","2.100"],
    ["12","5.02","20.00","33.18","6.31","20.48","8.00","2.717"],
    ["13","5.00","14.38","30.62","10.00","25.00","8.00","3.799"],
    ["14","7.99","20.00","28.17","10.00","18.84","8.00","2.322"],
    ["15","8.79","15.54","35.00","5.35","20.32","8.00","2.823"],
    ["16","10.00","11.45","35.00","5.00","23.55","8.00","3.337"],
    ["17","10.00","19.37","31.71","9.51","14.41","8.00","2.166"],
    ["18","10.00","20.00","35.00","10.00","10.00","8.00","2.100"],
    ["19","10.00","16.88","31.33","7.89","18.90","8.00","2.461"],
    ["20","10.00","16.88","31.33","7.89","18.90","8.00","2.461"],
    ["21","10.00","10.00","30.00","10.00","25.00","8.00","3.650"],
    ["22","10.00","10.00","34.07","10.00","20.93","8.00","3.650"],
    ["23","7.97","20.00","35.00","6.01","16.02","8.00","2.326"],
    ["24","5.00","16.16","35.00","5.00","23.84","8.00","3.395"],
    ["25","5.00","20.00","35.00","9.30","15.70","8.00","2.720"],
]
body.append(table(t2_headers, t2_rows))
body.append(para(""))

# 4.1.2
body.append(heading("4.1.2. Selection of SAW Process Parameters", 3))
body.append(para("For the multipass bead-on-plate experimentation, the welding parameters were carefully selected based on pre-trial tests. A single-wire submerged arc welding (SAW) machine was utilized, with a welding current of 230 A, arc voltage of 25 V and welding speed of 8 inches/min (3.39 mm/s). The choice of these parameters were based on the pre-trial tests to determine bead profile consistency, slag detachability and no surface defect like undercut or over reinforcement."))
body.append(para(""))
body.append(para("The heat input was calculated with the help of the standard formula:"))
body.append(para("Heat Input (HI) = (V \u00d7 I \u00d7 60 / S) \u00d7 \u03b7 \u2026 (Equation 4.4)", align="center"))
body.append(para("Where V is the welding voltage, I is the welding current, S is the welding speed, and \u03b7 is the arc efficiency, \u03b7 = 0.75. Heat input value of about 1.02 kJ/mm was obtained, which is within the recommended range of 0.8-2.5 kJ/mm in X70 pipeline steel welding."))
body.append(para(""))
body.append(para("EA2TiB filler wire with 2.4 mm diameter was utilized. Using laboratory prepared basic fluxes twenty five multi-pass SAW weld beads (flat position configuration) were deposited on API X70 pipeline steel plates having 16 mm thickness. No edge preparation was done for bead on plate experimentation. The weld passes were deposited as a multipass bead to each flux composition and in each case, five passes were deposited over the bead. The interpass temperature was rigorously kept at 120\u00b0C to 150\u00b0C."))
body.append(para(""))

# Table 4.3
body.append(para("Table 4.3: Chemical composition of base metal and filler wire", bold=True, size=22, align="center"))
body.append(table(
    ["Material","C","Si","Mn","P","S","Mo","Ni","Cr","Fe"],
    [["BM (X70)","0.058","0.331","1.590","0.006","0.002","0.003","0.219","0.007","98.1"],
     ["FW (EA2TiB)","0.03","0.078","0.781","0.020","0.005","0.317","0.090","0.042","98.8"]]
))
body.append(para(""))

# 4.2
body.append(heading("4.2. SAW Flux Preparation", 2))
body.append(para("The preparation of agglomerated fluxes followed a systematic and reproducible procedure. The preparation of the agglomerated fluxes was performed in the laboratory and each milled separately to a particle size less than 45 \u00b5m (passing through a 325-mesh sieve). This is done to develop a homogenous flux mixture, to ensure consistent melting during submerged arc welding. This particle size was selected due to its maximum contact surface area of individual flux constituent, uniform distribution of binder and its ideal agglomeration thus eliminating segregation of high-density oxide like BaO and MnO throughout its handling and welding process."))
body.append(para(""))
body.append(para("Following the weighing of the mineral components based on the design matrix as illustrated in Table 4.2, the powders were then combined in a turbula mixer in 30 minutes to get a homogeneous mixture. The inorganic binder was a potassium silicate solution at 5 wt. % of the total batch mass (K\u2082SiO\u2083). The binder was diluted in distilled water at 1:3 ratio to lower the viscosity and was then gradually poured to the powdered mixture, continually stirred to homogenize the whole flux mixture. After uniformly homogenizing the flux mixture, a 1.0 mm sieve was used to make the wet mixture into green agglomerates and then dried in an oven at 100\u00b0C during 2 hours to dry out the agglomerates and remove the absorbed moisture before cracking."))
body.append(para(""))
body.append(para("The agglomerates were then dried and then crushed and sieved to reach a final particle size distribution of 0.5 mm to 1.4 mm (ASTM 14-35 mesh). The sieved fluxes were placed in sealed jars at 120\u00b0C overnight before welding to remove all remaining hydroxyl groups. Thus reducing the chances of the multipass welded SAW beads cracking, as a result of hydrogen."))
body.append(para(""))

# Figure 4.2
body.append(img("rId8", 5400000, 4050000, "Figure 4.2: Twenty five multi-pass SAW beads deposited on API X70 pipeline steel plate"))
body.append(para(""))

# 4.3
body.append(heading("4.3. Characterization of Physicochemical and Thermophysical Properties of SAW Fluxes", 2))
body.append(para("The comprehensive characterization of all 25 flux formulations involved the measurement of density, thermal properties (thermal conductivity, thermal diffusivity, and specific heat capacity), phase analysis through X-ray diffraction (XRD), and structural analysis through Fourier Transform Infrared (FTIR) spectroscopy."))
body.append(para(""))

# 4.3.1
body.append(heading("4.3.1. Measurement of Density of Fluxes", 3))
body.append(para("The density measurements were made using tapped-density methodology, in which the flux powders have been placed into known cylindrical flasks (10 mL) in a known set of tapping, which ensures the uniformity of the particle distribution, and finally weighed using precise analytical balances. Density calculation followed Equation (4.5):"))
body.append(para("\u03c1 = Mass / Volume \u2026 (Equation 4.5)", align="center"))
body.append(para(""))
body.append(para("The entire thermophysical characterization of the 25 different submerged arc welding flux formulations showed a density of 1.40 to 1.54 g/cm\u00b3 (Figure 4.3a), which shows good correlation with the literature values of such multicomponent flux systems. Formulations enriched in high-density oxides such as BaO (\u03c1 = 5.72 g/cm\u00b3) and MnO (\u03c1 = 5.03 g/cm\u00b3) exhibited maximum density values (Flux 14\u2013Flux 16 and Flux 23\u2013Flux 25), consistent with theoretical predictions based on rule-of-mixtures calculations. Conversely, silica-dominated (SiO\u2082, \u03c1 = 2.65 g/cm\u00b3) and fluorspar-rich (CaF\u2082, \u03c1 = 3.18 g/cm\u00b3) compositions displayed lower bulk densities (Flux 1\u2013Flux 6). The mean density of 1.48 \u00b1 0.04 g/cm\u00b3 is an optimal one. The coefficient of variation of 2.7% points towards low porosity and high manufacturing reproducibility."))
body.append(para(""))

# 4.3.2
body.append(heading("4.3.2. Thermal Properties (Thermal Conductivity, Thermal Diffusivity and Specific Heat) Measurement", 3))
body.append(para("Specific heat capacity, thermal diffusivity, and thermal conductivity measurements were made using the Hot Disk Transient Plane Source (TPS-2500S) which is the international standard method (ISO 22007-2) of simultaneous determination of thermal properties. The TPS technique utilizes a nickel sensor that is enclosed in two thin insulating coatings to act both as a specialized heat source and resistance thermometer. Compared to traditional methods, the TPS method is more accurate with the measurement uncertainties usually less than both \u00b13% and \u00b15% of thermal conductivity and thermal diffusivity respectively."))
body.append(para(""))
body.append(para("The outcome of the thermal conductivity (Figure 4.3b) showed that the range was 0.34 to 0.52 W/m\u00b7K. High concentrations of metallic oxides (MnO, BaO, and TiO\u2082) enhanced thermal conductivity by up to 53% over silicate-based formulations due to improved phonon transport. The effective thermal conductivity follows: k_eff = \u03a3\u03c6_i\u00b7k_i (Equation 4.6)."))
body.append(para(""))
body.append(para("Specific heat capacity ranged from 0.902 to 1.192 MJ/m\u00b3\u00b7K (Figure 4.3c). Flux 25 had the highest value of 1.28 MJ/m\u00b3\u00b7K correlating with high CaF\u2082 and MnO content. Thermal diffusivity ranged from 0.202 to 0.351 mm\u00b2/s (Figure 4.3d), calculated using \u03b1 = k/\u03c1C_p (Equation 4.7). Flux 3 and Flux 22 had lowest values (0.202-0.215 mm\u00b2/s) while Flux 8 and Flux 20 exhibited highest values (0.335-0.351 mm\u00b2/s)."))
body.append(para(""))

# Figure 4.3
body.append(img("rId9", 5400000, 4050000, "Figure 4.3: Variation of thermophysical properties with flux number: (a) density, (b) thermal conductivity, (c) specific heat, (d) thermal diffusivity"))
body.append(para(""))

# 4.3.3
body.append(heading("4.3.3. Phase Analysis of Fluxes", 3))
body.append(para("X-Ray diffraction of four typical flux mixtures has shown clearance of crystalline phase assemblage (Figure 4.4). Flux 2 (35% CaF\u2082, 25% MnO) exhibits strong fluorite reflections at 2\u03b8 = 28.3\u00b0, 32.2\u00b0, and 47.0\u00b0, corresponding to (111), (200) and (220) planes. High intensity and small FWHM indicates high crystallinity. Flux 20 with lower CaF\u2082 (31.3%) shows lower fluorite peaks and new MnO peaks at 30.1\u00b0 and 50.5\u00b0. Flux 12 displays intermediate assemblage with fluorite and rutile peaks at 27.4\u00b0, 36.1\u00b0, and 54.4\u00b0."))
body.append(para(""))
body.append(para("Higher crystallinity in fluorite (Flux 2, 16) resulted in lower thermal diffusivity (0.215\u20130.245 mm\u00b2/s) compared to MnO-rich Flux 20 (0.335 mm\u00b2/s), consistent with phonon scattering. Higher basicity fluxes (Flux 2, 13) showed sharper peaks while lower basicity fluxes (Flux 11, 18) had broader peaks reflecting higher amorphous content."))
body.append(para(""))

# Figure 4.4
body.append(img("rId10", 5400000, 5400000, "Figure 4.4: XRD patterns for (a) Flux 2, (b) Flux 12, (c) Flux 16, (d) Flux 20"))
body.append(para(""))

# 4.3.4
body.append(heading("4.3.4. Structural Analysis of Fluxes", 3))
body.append(para("FTIR spectra for eight flux samples are shown in Figure 4.5. The most striking feature is a wide, strong signal in the 1070\u20131120 cm\u207b\u00b9 range, characteristic of asymmetric Si-O-Si stretching. A systematic shift towards lower wavenumbers in set B (Flux 14, 19, 21, 25) compared to set A (Flux 1, 6, 7, 11) indicates increased network depolymerization. The average peak position shifted from 1105 cm\u207b\u00b9 (set A) to 1085 cm\u207b\u00b9 (set B)."))
body.append(para(""))
body.append(para("The I\u2089\u2085\u2080/I\u2081\u2081\u2080\u2080 ratio ranged from 0.15\u20130.25 in set A and 0.30\u20130.45 in set B, correlating with specific heat capacities of 1.05\u20131.19 MJ/m\u00b3\u00b7K (set B) vs 0.90\u20130.98 MJ/m\u00b3\u00b7K (set A). O-H stretching bands centered around 3400 cm\u207b\u00b9 indicate moisture/hydroxyl content. TiO\u2082 adds lattice-vibration bands at 400\u2013800 cm\u207b\u00b9, while MnO contributes modes in 700\u2013400 cm\u207b\u00b9 domain."))
body.append(para(""))

# Figure 4.5
body.append(img("rId11", 5400000, 4500000, "Figure 4.5: FTIR spectra of (A) Flux 1, 6, 7, 11 and (B) Flux 14, 19, 21, 25 showing transmittance vs wavenumber (4000-500 cm\u207b\u00b9)"))
body.append(para(""))

body.append(para("The comprehensive characterization presented in this chapter establishes the fundamental physicochemical and thermophysical properties of the 25 formulated fluxes, providing the scientific foundation for understanding the structure-property-performance relationships that govern their behavior during the submerged arc welding process."))

# ===== ASSEMBLE DOCUMENT XML =====
body_xml = "\n".join(body)

document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
  <w:body>
    {body_xml}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>'''

# ===== CREATE DOCX (ZIP) FILE =====
with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('[Content_Types].xml', content_types_xml)
    zf.writestr('_rels/.rels', rels_xml)
    zf.writestr('word/_rels/document.xml.rels', doc_rels_xml)
    zf.writestr('word/document.xml', document_xml)
    zf.writestr('word/styles.xml', styles_xml)
    
    # Add images
    for i, fig_path in enumerate(figures):
        if os.path.exists(fig_path):
            zf.write(fig_path, f'word/media/image{i+1}.png')

print(f"\nDocument created: {output_file}")
print(f"File size: {os.path.getsize(output_file)} bytes")
