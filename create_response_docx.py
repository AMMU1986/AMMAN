#!/usr/bin/env python3
"""
Create a Word document (.docx) Response-to-Reviewers letter.
Uses only the Python standard library (zipfile). No external deps.
"""

import zipfile
from xml.sax.saxutils import escape

OUT = "Response_to_Reviewers.docx"


def run(text, bold=False, italic=False, size=22, color=None):
    """Return a run XML element. size is in half-points (22 = 11pt)."""
    rpr = "<w:rPr>"
    if bold:
        rpr += "<w:b/>"
    if italic:
        rpr += "<w:i/>"
    if color:
        rpr += f'<w:color w:val="{color}"/>'
    rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def para(runs, style=None, spacing_after=160, align=None):
    ppr = "<w:pPr>"
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if align:
        ppr += f'<w:jc w:val="{align}"/>'
    ppr += f'<w:spacing w:after="{spacing_after}"/></w:pPr>'
    return f"<w:p>{ppr}{''.join(runs)}</w:p>"


def heading(text, size=28):
    return para([run(text, bold=True, size=size, color="1F3864")], spacing_after=160)


def normal(text, spacing_after=160):
    return para([run(text)], spacing_after=spacing_after)


def italic_quote(text):
    return para([run(text, italic=True, color="555555")], spacing_after=120)


def bullet(text):
    ppr = ('<w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
           '<w:spacing w:after="80"/></w:pPr>')
    return f"<w:p>{ppr}{run(text)}</w:p>"


body = []

# Title block
body.append(para([run("Response to Reviewers", bold=True, size=36, color="1F3864")],
                 spacing_after=200, align="center"))
body.append(para([run("Manuscript: ", bold=True),
                  run("To study the mechanical and microstructural behavior of SA516 and 2205 "
                      "dissimilar GMAW welds fabricated by using 309L filler")], spacing_after=120))
body.append(para([run("Authors: ", bold=True),
                  run("Lochan Sharma, Amman Jakhar, Karan Mankotia")], spacing_after=120))
body.append(para([run("Corresponding Author: ", bold=True),
                  run("Lochan Sharma (lochan.e9455@cumail.in)")], spacing_after=200))

body.append(normal(
    "We sincerely thank the Editor and the Reviewer for the careful evaluation of our manuscript "
    "and for the constructive comments. The suggestions have significantly helped us improve the "
    "technical rigour, clarity, and completeness of the work. We have addressed every comment in "
    "full. Below, each comment is reproduced in italics, followed by our point-by-point response "
    "and a description of the exact changes made in the revised manuscript. All revised text and "
    "newly added figures/tables are highlighted in the revised manuscript for ease of tracking."))

# ---- Comment A ----
body.append(heading("Comment A"))
body.append(italic_quote("In Fig. 1 the dimension mentioned should be corrected."))
body.append(normal("Response: We thank the Reviewer for pointing out this inconsistency. We confirm "
                   "there was a mismatch between the dimensions stated in the text and those shown "
                   "in Figure 1. Corrections made:"))
body.append(bullet("The text stated the plate size as 100 x 90 x 12 mm, whereas Figure 1 showed each "
                   "plate as 60 mm long (60 + 60). Figure 1 has been corrected so the plate lengths "
                   "are consistent with the text, and all dimensional values were harmonised."))
body.append(bullet("Units (mm) have been added to every dimension in Figure 1, which were previously missing."))
body.append(bullet("The weld groove geometry (included V-groove angle, root gap, root face) is now "
                   "dimensioned and labelled, and the SA516 and SS2205 sides are clearly identified."))
body.append(normal("Location of change: Figure 1 (redrawn) and the Experimental Procedure section."))

# ---- Comment B ----
body.append(heading("Comment B"))
body.append(italic_quote("State why 309L filler material is chosen and its interactive effect with "
                         "the materials used."))
body.append(normal("Response: We agree the rationale for selecting 309L required a stronger "
                   "metallurgical justification. The relevant Introduction paragraph has been expanded "
                   "to explain both the selection criteria and the interactive (dilution) effects with "
                   "the two base metals. The added text explains that the high Cr and Ni equivalents "
                   "of 309L place the diluted weld deposit within the two-phase austenite + ferrite "
                   "region of the Schaeffler/WRC-1992 constitution diagrams, avoiding fully martensitic "
                   "or fully ferritic solidification. During welding the filler interacts with the "
                   "carbon-rich SA516 on one side and the Cr-Mo-N-rich SS2205 on the other; the "
                   "elevated Cr and Ni buffer the carbon picked up from SA516 dilution, suppressing "
                   "hard martensite in the fusion zone, while the controlled delta-ferrite content "
                   "mitigates solidification cracking without promoting excessive sigma phase. The "
                   "low-carbon 'L' grade further reduces chromium-carbide precipitation and "
                   "sensitisation. This is consistent with the observed skeletal delta ferrite with "
                   "interdendritic austenite reported in Section 3.1."))
body.append(normal("Location of change: Introduction (309L filler paragraph), cross-referenced in Section 3.1."))

# ---- Comment C ----
body.append(heading("Comment C"))
body.append(italic_quote("State any thermal model associated with it should be clearly mentioned."))
body.append(normal("Response: We agree. The original manuscript discussed cooling rate and thermal "
                   "cycling only qualitatively. An explicit thermal analysis based on the measured "
                   "welding parameters has been added:"))
body.append(bullet("Net heat input calculated from I = 180 A, V = 18 V, S = 80 mm/min (1.333 mm/s) "
                   "with arc efficiency eta = 0.8:  Q = eta x (V x I)/S = 0.8 x (18 x 180)/1.333 "
                   "= approx. 1.94 kJ/mm."))
body.append(bullet("Cooling behaviour described using the Rosenthal heat-conduction framework and the "
                   "delta-t 8/5 (800 to 500 C) cooling-time concept, which governs the phase "
                   "transformations in the two HAZs."))
body.append(bullet("The calculated heat input and cooling-rate trend are now linked explicitly to the "
                   "microhardness distribution (Table 5, Figure 5) and the fractography (Figure 4)."))
body.append(normal("Location of change: New short subsection at the end of the Experimental Procedure, "
                   "cross-referenced in Section 3.2.2 and the fractography discussion."))

# ---- Comment D ----
body.append(heading("Comment D"))
body.append(italic_quote("The author should mention the picture of the welding machine used and its "
                         "specifications."))
body.append(normal("Response: We thank the Reviewer. The manuscript named the GMAW machine but did "
                   "not include a photograph or specifications. We have added:"))
body.append(bullet("A photograph of the GMAW welding machine (Ghudani Metal Weld India, Central "
                   "Workshop, Chandigarh University) as a new figure."))
body.append(bullet("A specifications table listing model, power-source type (CC/CV), rated output "
                   "current range, open-circuit voltage, duty cycle, wire-feed-speed range, input "
                   "supply (phase/voltage), and manufacturer."))
body.append(normal("Location of change: Experimental Procedure, at the sentence naming the GMAW machine."))

# ---- Comment E ----
body.append(heading("Comment E"))
body.append(italic_quote("Diagrams of the welded specimens should be mentioned."))
body.append(normal("Response: We agree. Dimensioned drawings of the extracted test specimens have "
                   "been provided:"))
body.append(bullet("Dimensioned drawings of the Charpy impact specimen (per ASTM E23) with the V-notch "
                   "across the weld/HAZ, and the metallographic / microhardness cross-section specimen "
                   "showing the indentation traverse."))
body.append(bullet("A sectioning/extraction diagram indicating where each specimen was cut from the "
                   "welded plate and the notch location relative to the fusion zone and HAZ."))
body.append(normal("Location of change: Experimental Procedure, near Figure 2."))

# ---- Comment F ----
body.append(heading("Comment F"))
body.append(italic_quote("By drawing a schematic diagram, fusion zone, HAZ zone, base plate as well "
                         "as weld bead geometry should be mentioned."))
body.append(normal("Response: We agree. A labelled schematic clarifying the weld zones has been added:"))
body.append(bullet("A schematic cross-section of the weld joint labelling the base plates (SA516 and "
                   "SS2205), the fusion zone (FZ), HAZ-1 (SA516 side) and HAZ-2 (SS2205 side), the "
                   "fusion boundaries, and the weld bead geometry (bead width, reinforcement height, "
                   "penetration depth)."))
body.append(bullet("The microhardness indentation traverse is overlaid so the 'distance from the left "
                   "side' axis in Figure 5 can be mapped spatially to each weld zone."))
body.append(normal("Location of change: New figure at the start of Section 3.1, referenced in Section 3.2.2."))

# ---- Comment G ----
body.append(heading("Comment G"))
body.append(italic_quote("Literature review in the introduction part i.e. ref. 4 should be written "
                         "elaborately."))
body.append(normal("Response: We thank the Reviewer. On review we found that reference [4] (Saini and "
                   "Singh, on recycling of steel slag as a flux for submerged arc welding) did not "
                   "appropriately support the statement on SA516 and its ASTM pressure-vessel "
                   "specification. Corrections/additions made:"))
body.append(bullet("Reference [4] has been replaced with an appropriate source directly supporting "
                   "SA516 Gr. 70 / ASME SA-516 pressure-vessel steel specifications and weldability."))
body.append(bullet("The Introduction has been expanded with a more elaborate SA516 Gr. 70 literature "
                   "review covering weldability, HAZ behaviour, notch toughness and pressure-vessel/"
                   "boiler applications, drawing on relevant prior studies (including existing "
                   "references on SA516 SAW welds and through-thickness residual stresses)."))
body.append(normal("Location of change: Introduction, at the SA516 statement and surrounding review."))

# ---- Additional corrections ----
body.append(heading("Additional corrections made by the authors (self-identified during revision)"))
body.append(bullet("Conclusion vs. Table 5: the Conclusion stated the highest microhardness (372 HV) "
                   "occurred at HAZ-1, whereas the Abstract and Table 5 attribute 372 HV to HAZ-2 "
                   "(SS2205 side). The Conclusion has been corrected."))
body.append(bullet("'HAZ along X70 side' in the Experimental Procedure has been corrected to the SA516 "
                   "side; X70 was not used in this study."))
body.append(bullet("Fractography labelling (Figure 4c): text stated 'this region is from the HAZ-1' "
                   "while describing HAZ-2; corrected."))
body.append(bullet("Filler wire diameter '08 mm' corrected to the intended 0.8 mm, consistent with "
                   "GMAW practice."))

body.append(normal("We believe these revisions have substantially strengthened the manuscript and "
                   "fully address the Reviewer's comments. We thank the Editor and Reviewer again for "
                   "their valuable time and guidance.", spacing_after=200))
body.append(para([run("Sincerely,", size=22)], spacing_after=40))
body.append(para([run("On behalf of all authors,", size=22)], spacing_after=40))
body.append(para([run("Lochan Sharma (Corresponding Author)", bold=True, size=22)], spacing_after=40))

document_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:body>' + ''.join(body) +
    '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
    'w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>'
    '</w:body></w:document>'
)

content_types = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
    '</Types>'
)

rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '</Relationships>'
)

doc_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
    '</Relationships>'
)

numbering = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="1"/>'
    '<w:numFmt w:val="bullet"/><w:lvlText w:val="&#8226;"/><w:lvlJc w:val="left"/>'
    '<w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>'
    '<w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/></w:rPr></w:lvl></w:abstractNum>'
    '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>'
    '</w:numbering>'
)

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document_xml)
    z.writestr("word/_rels/document.xml.rels", doc_rels)
    z.writestr("word/numbering.xml", numbering)

print(f"Created {OUT}")
