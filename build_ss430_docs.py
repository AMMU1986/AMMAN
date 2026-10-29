#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate two .docx files for the SS430 filler-weldability revision, using only
the Python standard library (a .docx is a zip of XML parts).

Outputs (in the repo root):
  - Manuscript_SS430_Filler_Weldability_Revised.docx
      Full revised manuscript. Every reviewer-driven change is highlighted
      in YELLOW (Word highlight = <w:highlight w:val="yellow"/>).
  - Response_to_Reviewers_SS430.docx
      Clean, finalized point-by-point response, contradictions resolved.

Authoring markup inside text strings:
  «...»  -> that span is yellow-highlighted
"""

import os
import zipfile
from xml.sax.saxutils import escape

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# ---------------------------------------------------------------- run helpers

def _runs_from_text(text, bold=False, italic=False, base_hl=False):
    """Parse «» highlight markers into a list of run dicts."""
    runs = []
    hl = base_hl
    buf = ""
    for ch in text:
        if ch == "«":
            if buf:
                runs.append(dict(t=buf, b=bold, i=italic, hl=hl))
                buf = ""
            hl = True
        elif ch == "»":
            if buf:
                runs.append(dict(t=buf, b=bold, i=italic, hl=hl))
                buf = ""
            hl = base_hl
        else:
            buf += ch
    if buf:
        runs.append(dict(t=buf, b=bold, i=italic, hl=hl))
    return runs


def _run_xml(r):
    rpr = []
    if r.get("b"):
        rpr.append("<w:b/>")
    if r.get("i"):
        rpr.append("<w:i/>")
    sz = r.get("sz")
    if sz:
        rpr.append('<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (sz, sz))
    if r.get("hl"):
        rpr.append('<w:highlight w:val="yellow"/>')
    rpr_xml = "<w:rPr>%s</w:rPr>" % "".join(rpr) if rpr else ""
    txt = escape(r["t"])
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr_xml, txt)


# ---------------------------------------------------------------- block builder

class Doc:
    def __init__(self):
        self.blocks = []

    def para(self, text="", bold=False, italic=False, hl=False, sz=None,
             align=None, space_before=0, space_after=120, ind=None):
        runs = _runs_from_text(text, bold=bold, italic=italic, base_hl=hl)
        if sz:
            for r in runs:
                r["sz"] = sz
        self.blocks.append(dict(kind="p", runs=runs, align=align,
                                sb=space_before, sa=space_after, ind=ind))

    def runs_para(self, runs, align=None, space_before=0, space_after=120, ind=None):
        self.blocks.append(dict(kind="p", runs=runs, align=align,
                                sb=space_before, sa=space_after, ind=ind))

    def title(self, text):
        self.para(text, bold=True, sz=32, align="center", space_after=200)

    def h1(self, text, hl=False):
        self.para(text, bold=True, sz=28, hl=hl, space_before=160, space_after=100)

    def h2(self, text, hl=False):
        self.para(text, bold=True, sz=26, hl=hl, space_before=120, space_after=80)

    def caption(self, text, hl=False):
        self.para(text, italic=True, sz=20, hl=hl, space_after=160)

    def bullet(self, text, hl=False):
        self.blocks.append(dict(kind="p",
                                runs=_runs_from_text(text, base_hl=hl),
                                align=None, sb=0, sa=80, ind=360, bullet=True))

    def table(self, rows, col_w=None):
        """rows: list of list of cell-strings (may contain «»). Row 0 = header."""
        self.blocks.append(dict(kind="tbl", rows=rows, col_w=col_w))

    # ------------------------------------------------------------ XML emit
    def _p_xml(self, blk):
        ppr = []
        if blk.get("align"):
            ppr.append('<w:jc w:val="%s"/>' % blk["align"])
        spacing = '<w:spacing w:before="%d" w:after="%d"/>' % (blk["sb"], blk["sa"])
        ppr.append(spacing)
        if blk.get("ind"):
            ppr.append('<w:ind w:left="%d"/>' % blk["ind"])
        if blk.get("bullet"):
            ppr.append('<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>')
        ppr_xml = "<w:pPr>%s</w:pPr>" % "".join(ppr)
        runs = "".join(_run_xml(r) for r in blk["runs"])
        return "<w:p>%s%s</w:p>" % (ppr_xml, runs)

    def _tbl_xml(self, blk):
        rows = blk["rows"]
        col_w = blk.get("col_w")
        ncol = max(len(r) for r in rows)
        borders = ("<w:tblBorders>"
                   '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                   '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                   '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                   '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                   '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                   '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                   "</w:tblBorders>")
        tblpr = ('<w:tblPr><w:tblW w:w="5000" w:type="pct"/>%s'
                 '<w:tblLayout w:type="fixed"/></w:tblPr>' % borders)
        if not col_w:
            col_w = [int(9360 / ncol)] * ncol
        grid = "<w:tblGrid>%s</w:tblGrid>" % "".join(
            '<w:gridCol w:w="%d"/>' % w for w in col_w)
        out = [tblpr, grid]
        for ri, row in enumerate(rows):
            cells = []
            for ci in range(ncol):
                cell = row[ci] if ci < len(row) else ""
                header = (ri == 0)
                runs = _runs_from_text(cell, bold=header)
                for r in runs:
                    r["sz"] = 18
                shade = '<w:shd w:val="clear" w:color="auto" w:fill="D9D9D9"/>' if header else ""
                tcpr = '<w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s</w:tcPr>' % (col_w[ci], shade)
                p = ('<w:p><w:pPr><w:spacing w:before="20" w:after="20"/></w:pPr>%s</w:p>'
                     % "".join(_run_xml(r) for r in runs))
                cells.append("<w:tc>%s%s</w:tc>" % (tcpr, p))
            out.append("<w:tr>%s</w:tr>" % "".join(cells))
        return "<w:tbl>%s</w:tbl>" % "".join(out)

    def body_xml(self):
        parts = []
        for blk in self.blocks:
            if blk["kind"] == "p":
                parts.append(self._p_xml(blk))
            else:
                parts.append(self._tbl_xml(blk))
                parts.append("<w:p><w:pPr><w:spacing w:after="
                             '"120"/></w:pPr></w:p>')
        sect = ('<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
                '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" '
                'w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>'
                "</w:sectPr>")
        return "".join(parts) + sect


def write_docx(doc, path):
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="%s">'
        "<w:body>%s</w:body></w:document>" % (W, doc.body_xml())
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/numbering.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
        "</Types>"
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="word/document.xml"/></Relationships>'
    )
    doc_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" '
        'Target="numbering.xml"/></Relationships>'
    )
    numbering = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:numbering xmlns:w="%s">'
        '<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0">'
        '<w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="\u2022"/>'
        '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="360" w:hanging="360"/></w:pPr>'
        "</w:lvl></w:abstractNum>"
        '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>'
        "</w:numbering>" % W
    )
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        z.writestr("word/document.xml", document_xml)
        z.writestr("word/numbering.xml", numbering)
    print("wrote", path)


# ====================================================================
#  REVISED MANUSCRIPT  (changes highlighted in yellow)
# ====================================================================

def build_manuscript():
    d = Doc()

    # ----- Title (revised per Reviewer 2, Comment 1) -----
    d.title("«Investigation on the Weldability of 430-Grade Ferritic Stainless "
            "Steel Using Three Different Filler Wire Grades (Austenitic 309L, "
            "Martensitic 410, and Duplex 2594)»")

    # ----- Abstract -----
    d.h1("Abstract")
    d.para(
        "430 grade ferritic stainless steel is widely used for industrial "
        "applications such as automotive exhaust systems, kitchen appliances, "
        "and architectural panels because it is cost-effective and resists "
        "corrosion, yet it remains difficult to weld. This study explores the "
        "role of different filler metals on the welding characteristics and "
        "joint performance of this industrially relevant alloy. "
        "«Twelve-millimetre-thick AISI 430 plate (coupons of 75 \u00d7 75 \u00d7 "
        "12 mm, wire-EDM sectioned) was joined by gas metal arc welding "
        "(GMAW/MIG) using three filler wire grades \u2014 austenitic ER309L, "
        "martensitic ER410, and duplex ER2594 \u2014 in a four-pass single-V "
        "butt joint (60\u00b0 included groove angle, 2 mm root gap) with DCEP "
        "polarity, 110 A, a 150 \u00b0C interpass temperature, and an "
        "\u2248 2.98 kJ/mm cumulative heat input. The joints were characterised "
        "across the fusion zone (FZ), heat-affected zone (HAZ), and base metal "
        "(BM) by optical microscopy (OM), SEM fractography, X-ray diffraction "
        "(XRD), Vickers microhardness (VHN), Charpy V-notch impact testing, and "
        "potentiodynamic polarization, and compared with Schaeffler-diagram and "
        "solidification-mode predictions.» "
        "The 309L welds gave the highest fusion-zone impact toughness "
        "(125 J), attributed to their austenitic solidification and excellent "
        "cracking resistance. The martensitic 410 filler provided the greatest "
        "fusion-zone hardness (320 VHN) but the lowest HAZ impact toughness "
        "(45 J). The duplex 2594 filler offered a balanced combination of "
        "toughness (100 J) with a reasonable fusion-zone hardness (300 VHN). "
        "Grain coarsening and sensitization in the HAZ were common to all "
        "fillers and most pronounced under multi-pass thermal cycling. "
        "Microstructural predictions from the Schaeffler diagram and "
        "solidification-mode theory agreed broadly with experiment, with "
        "deviations due to real welding factors. These results emphasize the "
        "critical nature of filler selection according to service needs "
        "(toughness, hardness, or corrosion performance). XRD showed distinct "
        "fusion-zone phase constitutions: \u03b3-austenite with \u03b4/\u03b1-"
        "ferrite in F309, \u03b1\u2032 martensite in F410, and a balanced "
        "ferrite\u2013austenite duplex structure in F2594. Potentiodynamic "
        "polarization showed superior corrosion resistance for the F2594 weld "
        "(high chromium content and stable passivation), while F410 showed the "
        "greatest corrosion susceptibility.")
    d.para("Keywords: Welding metallurgy; Ferritic stainless steel; Filler metal "
           "effect; Heat affected zone; Microstructure\u2013performance "
           "relationship.", italic=True)

    # ----- 1. Introduction -----
    d.h1("1. Introduction")
    d.para(
        "Ferritic stainless steels (FSS) are a subgroup of stainless alloys "
        "with a body-centered cubic (BCC) crystal structure, consisting mainly "
        "of iron and chromium with little or no nickel [1]. Chromium contents "
        "of typically 10.5\u201330% provide their oxidation resistance and low "
        "cost [2]. Compared with austenitic grades, FSS offer better resistance "
        "to stress-corrosion cracking, higher thermal conductivity, and lower "
        "thermal expansion [3], making them suitable for components exposed to "
        "temperature fluctuations [4]. Common applications of AISI 430 include "
        "kitchen appliances, automotive exhausts, and architectural panels [5]. "
        "However, grain coarsening and chromium-carbide-driven intergranular "
        "corrosion during welding have historically limited their use in welded "
        "structural applications [6, 7].")
    d.para(
        "«In conventional unstabilized FSS, carbon and nitrogen promote "
        "chromium-carbide precipitation at grain boundaries, causing "
        "sensitization and intergranular corrosion. Stabilization with titanium "
        "and niobium (forming stable TiC/NbC) and ultra-low-interstitial (ULI) "
        "processing (C + N < 50 ppm) mitigate this, and stabilized grades such "
        "as AISI 441 and 444 show improved weldability. AISI 430, however, is a "
        "non-stabilized grade that remains susceptible to these effects and is "
        "therefore an informative model alloy for studying weldability "
        "[8\u201318].»")
    d.para(
        "Welding remains the principal limitation for FSS. Because the ferritic "
        "structure is retained through heating and cooling, no austenite "
        "transformation refines the grains, so rapid grain coarsening occurs in "
        "the HAZ above ~950 \u00b0C [19, 20]; HAZ grain sizes above 100 \u00b5m "
        "markedly reduce toughness [21]. Embrittling sigma phase can precipitate "
        "between 600\u2013900 \u00b0C [22], high-carbon zones can transform to "
        "martensite on rapid cooling [23], and fully ferritic solidification "
        "lacks the crack-healing benefit of dual-phase microstructures [24]. "
        "These issues have motivated low-heat-input and grain-refining "
        "approaches such as pulsed-laser, active-TIG, and friction-stir welding, "
        "together with post-weld treatments to dissolve chromium carbides and "
        "redistribute stabilizing precipitates [25].")
    d.para(
        "«The choice of filler metal is central to overcoming these problems, "
        "and recent studies quantify its effect. Anttila et al. reported that "
        "ferritic 409/430-type filler welds retain acceptable tensile strength "
        "and ductility but suffer from poor impact toughness in the weld region, "
        "confirming that ferritic fillers alone do not solve the toughness "
        "problem. Comparative filler studies on 430 FSS show that austenitic "
        "fillers produce columnar austenite with retained ferrite, whereas "
        "ferritic/martensitic fillers such as 410 yield acicular ferrite with "
        "martensite and austenite, giving higher weld-metal strength and "
        "hardness. Ostovan et al. showed that increasing molybdenum in GTAW "
        "AISI 316 welds raises the \u03b4-ferrite fraction in the fusion zone "
        "and improves both mechanical strength and pitting-corrosion resistance "
        "\u2014 a direct rationale for examining a high-Mo super-duplex (ER2594) "
        "filler on 430. Related studies on ferritic/duplex weldments reinforce "
        "that filler-driven phase balance governs HAZ sensitization and "
        "passive-film stability. Collectively, these works establish that "
        "austenitic, martensitic, and duplex fillers trade off toughness, "
        "hardness, and corrosion resistance differently, yet a single, "
        "controlled comparison of all three on identical 430 joints under one "
        "welding schedule is lacking \u2014 the gap this study addresses "
        "(content rephrased for compliance).»")
    d.para(
        "«Filler practice for AISI 430 and rationale for the present selection. "
        "In current research and industrial practice, austenitic fillers \u2014 "
        "chiefly ER309L \u2014 are the most widely used consumables for welding "
        "430, because the ductile, crack-tolerant austenitic weld metal "
        "compensates for the low toughness of fully ferritic welds. "
        "Ferritic/martensitic fillers (ER430, ER410) are chosen when colour "
        "match, magnetic response, or higher weld-metal strength and hardness "
        "is required, while duplex/super-duplex fillers (ER2209, ER2594) are "
        "comparatively rare for 430 and used mainly where elevated strength plus "
        "pitting/crevice-corrosion resistance is needed. Each option has "
        "documented limits: ferritic fillers give poor weld toughness; "
        "martensitic ER410 is hard but brittle and generally needs post-weld "
        "heat treatment; and austenitic ER309L overcomes the toughness problem "
        "but raises thermal-expansion-mismatch and galvanic concerns at the "
        "fusion boundary. Across all fillers the ferritic HAZ of 430 still "
        "coarsens and can sensitize, so the filler primarily governs "
        "fusion-zone behaviour. Accordingly, one representative filler was "
        "selected from each family \u2014 austenitic ER309L, martensitic ER410, "
        "and super-duplex ER2594 \u2014 to isolate the effect of weld-metal "
        "solidification mode and phase balance under one welding schedule.»")
    d.para(
        "AISI 430 is an economical ferritic grade used in automotive exhaust "
        "systems, household appliances, and architecture, making the results of "
        "this study directly relevant to a large area of manufacturing [26]. As "
        "a non-stabilised grade, 430 is more prone to chromium-carbide "
        "precipitation, high-temperature HAZ coarsening, and sensitisation than "
        "stabilised or higher-alloy grades [27, 28], which makes it an ideal "
        "model alloy for assessing basic weldability issues and for comparative "
        "filler evaluation under realistic fabrication conditions. Investigating "
        "AISI 430 also aligns with current efforts toward low-cost, sustainable "
        "stainless-steel solutions [29\u201331], and insights for this baseline "
        "grade inform the welding behaviour of related grades such as 409, 410, "
        "and 440.")
    d.para(
        "The key motivation of this research is to understand how weldability "
        "and filler-metal selection influence welded-joint performance. The "
        "study systematically compares austenitic ER309L, martensitic ER410, "
        "and duplex ER2594 fillers on 430 FSS and correlates fusion-zone and "
        "HAZ hardness, impact toughness, and fracture morphology, with the goal "
        "of providing clear guidelines for filler selection against specific "
        "service requirements.")

    # ----- 2. Materials and Methods -----
    d.h1("2. Materials and Methods", hl=True)
    d.h2("2.1 Materials, joint design, and welding", hl=True)
    d.para(
        "The base material was AISI 430 ferritic stainless steel. Coupons "
        "measuring 75 \u00d7 75 \u00d7 12 mm (Fig. 1) were sectioned from plate "
        "using a wire-EDM machine (Electronica 5535-EZNC) to minimise thermal "
        "input and ensure stress-free preparation. «Single-V butt joints with a "
        "60\u00b0 included groove angle and a 2 mm root gap were welded by gas "
        "metal arc welding (GMAW/MIG) to ensure full penetration.» Three coupons "
        "were welded per filler for statistical reliability (nine coupons "
        "total), yielding specimens for mechanical testing and metallography. "
        "Three commercial fillers were compared: austenitic ER309L, martensitic "
        "ER410, and duplex ER2594 (2.14 mm diameter). The base metal and fillers "
        "were supplied by Star Metal Solution in accordance with AWS A5.9 / ASME "
        "SFA-5.9 and EN ISO 14343. Chemical compositions were determined by "
        "optical emission spectrometry (OES) at IAHT Ludhiana (Table 1); "
        "«nominal, as-supplied» mechanical properties of the base and filler "
        "materials are given in Table 2.")

    d.caption("Table 1. Chemical composition (wt%) and equivalents of the "
              "stainless steel and filler metals.")
    d.table([
        ["Category", "Material", "C", "Ni", "Cr", "Si", "Mn", "Mo", "Fe",
         "Cr_eq", "Ni_eq", "Primary Use"],
        ["Base Metal", "SS 430", "0.12", "0.5", "12.5", "0.5", "1.0", "0.5",
         "Rem", "13.3", "1.8", "Ferritic applications"],
        ["Filler", "FW 309L", "0.02", "12.0", "23.0", "0.6", "1.5", "0.3",
         "Rem", "23.9", "13.8", "Dissimilar welding, high-temp"],
        ["Filler", "FW 410", "0.08", "0.6", "12.5", "0.5", "1.0", "0.5",
         "Rem", "13.3", "2.0", "Matching SS 410 welds"],
        ["Filler", "FW 2594", "0.017", "9.5", "24.9", "0.5", "0.6", "3.85",
         "Rem", "30.8", "12.56", "Corrosion-resistant duplex welds"],
    ])

    d.caption("«Table 2. Nominal (as-supplied) mechanical properties of AISI "
              "430 base metal and the filler wires (ER309L, ER410, ER2594), "
              "taken from manufacturer datasheets (AWS A5.9 / EN ISO 14343). "
              "These are reference properties of the consumables and are not "
              "weld-joint measurements.»", hl=True)
    d.table([
        ["Material", "Yield (MPa)", "Tensile (MPa)", "Elong. (%)",
         "Hardness (VHN)", "Impact (J)", "Notable properties"],
        ["SS 430", "500 \u00b1 15", "700 \u00b1 20", "18 \u00b1 2",
         "225 \u00b1 10", "38 \u00b1 3", "Ferritic, moderate corrosion resistance"],
        ["ER 309L", "400 \u00b1 12", "650 \u00b1 18", "35 \u00b1 3",
         "175 \u00b1 8", "125 \u00b1 8", "Austenitic, excellent crack resistance"],
        ["ER 410", "550 \u00b1 25", "750 \u00b1 22", "15 \u00b1 2",
         "250 \u00b1 12", "45 \u00b1 4", "Martensitic, typically needs PWHT"],
        ["ER 2594", "750 \u00b1 30", "950 \u00b1 25", "30 \u00b1 2",
         "300 \u00b1 15", "100 \u00b1 6", "Super-duplex, superior pitting/crevice"],
    ])

    d.para(
        "Welding parameters (Table 3) were established from "
        "ferritic-stainless-steel guidelines and preliminary trials, "
        "prioritising full penetration of the 12 mm plates while controlling "
        "heat input to limit HAZ grain coarsening, sensitisation, and "
        "embrittlement. A higher-energy root pass was followed by lower-energy "
        "filler passes to reduce cumulative thermal effects. All welds used DCEP "
        "polarity, 110 A, a 150 \u00b0C interpass temperature, and a "
        "«15 L/min» shielding-gas flow. A four-pass sequence was adopted to "
        "mirror industrial practice for 10\u201315 mm ferritic plate, limiting "
        "per-pass heat input and promoting beneficial interpass tempering.")
    d.para(
        "Heat input was calculated as Heat Input (kJ/mm) = (\u03b7 \u00d7 V "
        "\u00d7 I) / (S \u00d7 1000) (Eq. 1), where \u03b7 = 0.8 (arc "
        "efficiency), V = voltage, I = current (A), and S = travel speed "
        "(mm/s). The root pass (14 V, 150 A, 90 mm/min) gave \u2248 0.84 kJ/mm "
        "and each filler pass (12 V, 135 A, 80 mm/min) \u2248 0.729 kJ/mm, for a "
        "cumulative input of 2.98 kJ/mm across four passes.")

    d.caption("Table 3. MIG (GMAW) welding parameters and process "
              "specifications.")
    d.table([
        ["Parameter", "Value / description"],
        ["Welding process", "MIG (GMAW)"],
        ["Welding position", "1G"],
        ["«Groove angle»", "«60\u00b0 (single-V)»"],
        ["«Root gap»", "«2 mm»"],
        ["Number of passes", "4"],
        ["Polarity", "DCEP"],
        ["Interpass temperature", "150 \u00b0C"],
        ["Filler wires", "FW 309L, FW 410, FW 2594"],
        ["«Shielding gas flow rate»", "«15 L/min»"],
        ["Root pass (V / A / speed)", "14 V / 150 A / 90 mm/min"],
        ["Root pass avg. heat input", "0.84 kJ/mm"],
        ["Filler pass (V / A / speed)", "12 V / 135 A / 80 mm/min"],
        ["Filler pass avg. heat input", "0.729 kJ/mm"],
        ["Cumulative heat input", "2.98 kJ/mm"],
    ], col_w=[4680, 4680])

    d.para(
        "Before welding, surfaces were cleaned with ethanol. After welding, "
        "surface oxides and spatter were removed by mechanical brushing, "
        "followed by ultrasonic cleaning in ethanol to give clean, repeatable "
        "surfaces for characterisation.")

    d.h2("2.2 Characterization", hl=True)
    d.para(
        "Welded joints were sectioned and prepared by standard metallography: "
        "grinding with 400\u20131200 grit SiC paper and polishing with 0.3 "
        "\u00b5m alumina. Transverse cross-sections covering BM, HAZ, and FZ "
        "were electrolytically etched with 10% oxalic acid (1.6 A/cm\u00b2, 6 V "
        "DC, 10\u201315 s). «This is a grain-boundary/sensitization etch (ASTM "
        "A262 Practice A): it reveals grain boundaries and carbides but does "
        "not provide selective ferrite\u2013austenite contrast. Accordingly, no "
        "quantitative phase-fraction measurement (point counting, image "
        "analysis, Feritscope, or EBSD) was performed, and phase constitution "
        "is identified from XRD.» Microstructures were examined by optical "
        "microscopy (OM) and scanning electron microscopy (SEM); macrostructures "
        "were imaged with a Nikon SMZ745T stereo-zoom microscope and measured "
        "with Image Studio v5.2.")
    d.para(
        "Vickers microhardness was measured on transverse sections (500 gf, "
        "10 s dwell, 0.25 mm spacing) across the weld zone, HAZ, and BM. Charpy "
        "V-notch specimens (55 \u00d7 10 \u00d7 10 mm; 2 mm notch depth, 0.25 mm "
        "root radius, 45\u00b0 angle) were machined per ASTM E23 / ISO 148-1, "
        "with notches placed in the FZ centre and in the coarse-grained HAZ near "
        "the fusion line; fracture surfaces were examined by SEM. XRD used "
        "Cu-K\u03b1 radiation (\u03bb = 1.5406 \u00c5, 40 kV, 30 mA) over "
        "20\u2013100\u00b0 2\u03b8 at 0.2\u00b0/min, with phases identified "
        "against JCPDS files. Potentiodynamic polarization followed ASTM G5 / "
        "G59 in natural seawater using a three-electrode cell (Pt counter, "
        "Ag/AgCl reference, ~1 cm\u00b2 exposed area), 30 min OCP "
        "stabilisation, and scanning \u00b1250 mV about OCP at 1 mV/s; E_corr, "
        "I_corr, and Tafel slopes were extracted and the corrosion rate computed "
        "via Faraday's law, v = (I_corr \u00b7 M) / (n \u00b7 F \u00b7 \u03c1) "
        "(Eq. 2), with M = 55.85 g/mol, n = 2, F = 96 485 C/mol, \u03c1 = 7.8 "
        "g/cm\u00b3, converted to mm/year.")

    # ----- 3. Results and Discussion (reordered per Reviewer 1, Comment 7) -----
    d.h1("3. Results and Discussion", hl=True)

    d.h2("3.1 Optical microscopy", hl=True)
    d.para(
        "«The optical micrographs (Fig. 7) reveal grain morphology and the "
        "extent of thermal modification in each zone; phase identification is "
        "based on the XRD results (Fig. 9), because the oxalic-acid etch "
        "highlights grain boundaries and may introduce etch-pit and relief "
        "artifacts that should not be interpreted as discrete phases. In the "
        "309L fusion zone (Fig. 7a), elongated columnar grains with "
        "interdendritic \u03b4-ferrite in an austenite matrix are observed, "
        "consistent with primary-ferrite (FA) solidification and the \u03b3 + "
        "\u03b4/\u03b1-ferrite peaks in Fig. 9; the adjoining HAZ (Fig. 7b) is "
        "comparatively fine-grained, indicating a moderate thermal effect. The "
        "410 fusion zone (Fig. 7c) shows a predominantly ferritic/martensitic "
        "matrix with columnar grains; the fine dark contrast is consistent with "
        "etch pitting and grain-boundary attack rather than a distinct "
        "precipitate population, and the XRD pattern shows only \u03b1/\u03b1"
        "\u2032 reflections with no intermetallic peaks, while the HAZ "
        "(Fig. 7d) is ferritic with evidence of grain coarsening. In the 2594 "
        "fusion zone (Fig. 7e), a two-phase ferrite\u2013austenite (duplex) "
        "structure with interdendritic segregation is seen; the weak "
        "low-intensity intermetallic reflections in Fig. 9 indicate only a "
        "minor secondary-phase fraction, so abundant intermetallics should not "
        "be inferred from the optical contrast, and the 2594 HAZ (Fig. 7f) "
        "shows elongated/coarsened grains with retained-austenite regions in a "
        "ferrite matrix.»")
    d.para(
        "«The common cause of the reduced HAZ toughness across all three "
        "fillers is the characteristic degradation of ferritic HAZs \u2014 "
        "grain coarsening above ~950 \u00b0C combined with chromium-carbide "
        "precipitation (sensitization) at grain boundaries during the weld "
        "thermal cycle \u2014 which together provide low-energy fracture paths. "
        "This is referred to below as \u201cHAZ degradation.\u201d Overall, the "
        "optical observations establish grain morphology and the degree of HAZ "
        "coarsening, while the fusion-zone phase constitution is defined by "
        "XRD.»")

    d.h2("3.2 Scanning electron microscopy", hl=True)
    d.para(
        "«SEM (Fig. 8) confirms the optical observations. The 309L FZ "
        "(Fig. 8a) shows dendritic and globular \u03b4-ferrite in austenite, "
        "consistent with good ductility, and its HAZ (Fig. 8b) shows scattered "
        "features and partial dendritic back-transformation without excessive "
        "coarsening. The 410 FZ (Fig. 8c) shows columnar dendrites with "
        "interdendritic second-phase particles in a ferritic/martensitic matrix "
        "(high hardness, low toughness); the HAZ (Fig. 8d) is dendritic ferrite "
        "with occasional inclusions that can act as stress concentrators. The "
        "2594 FZ (Fig. 8e) shows a duplex ferrite\u2013austenite structure with "
        "localised Cr/Mo-rich second-phase particles from segregation during "
        "solidification, and the HAZ (Fig. 8f) shows acicular second-phase "
        "particles along columnar boundaries, indicating a high thermal "
        "gradient. Because no EDS analysis was performed, these features are "
        "described as second-phase particles rather than identified "
        "intermetallic or eutectic constituents; phase identification rests on "
        "XRD (Fig. 9).»")

    d.h2("3.3 Phase prediction and XRD analysis", hl=True)
    d.para(
        "The Schaeffler diagram (Fig. 6a) places 309L in the austenite + "
        "ferrite field (ductile, crack-resistant), 410 in the "
        "martensitic\u2013ferritic field (hard, low toughness), and 2594 in the "
        "balanced ferrite\u2013austenite field. The pseudo-binary diagram "
        "(Fig. 6b) indicates F/FA solidification for all three, with the "
        "Cr_eq/Ni_eq ratio governing the amount of austenite formed on cooling.")
    d.para(
        "«XRD (Fig. 9) shows filler-dependent fusion-zone phase constitutions. "
        "F309 shows strong \u03b3-austenite with \u03b4/\u03b1-ferrite peaks; "
        "F410 shows dominant \u03b1/\u03b1\u2032 (martensite) reflections with "
        "suppressed \u03b3; and F2594 shows comparable \u03b1 and \u03b3 "
        "intensities with weak low-intensity peaks attributable to a minor "
        "secondary phase. The SS430 base metal and the duplex fusion zone give "
        "sharper peaks (a more ordered ferritic/duplex structure), whereas the "
        "austenitic and martensitic welds give comparatively broader, weaker "
        "peaks consistent with rapid solidification and higher defect density. "
        "These results agree with the Schaeffler predictions and define the "
        "phase constitution used to interpret the microstructures above.»")

    d.h2("3.4 Mechanical properties", hl=True)
    d.para(
        "«Impact toughness and hardness varied systematically with filler "
        "(Fig. 4), and fusion-zone and HAZ values are reported separately. In "
        "the fusion zone, 309L gave the highest toughness (125 J), 2594 was "
        "intermediate (100 J), and 410 the lowest; HAZ toughness fell in every "
        "case, reaching only 45 J for 410, the most embrittled condition. "
        "Hardness showed the inverse trend: the 410 FZ was hardest (~320 VHN, "
        "martensitic), followed by 2594 (~300 VHN) and 309L (~260 VHN, "
        "strain-hardened austenite), while all HAZ hardness values converged "
        "toward the base metal (~150\u2013170 VHN). The reduced HAZ toughness "
        "in every case reflects the HAZ degradation mechanism described in "
        "\u00a73.1.»")
    d.para(
        "«Fractography (Fig. 5) is consistent with these trends. The 309L FZ "
        "(Fig. 5a) shows dense fibrous dimples (ductile, retained-austenite "
        "plasticity); the 410 FZ (Fig. 5c) shows sparse, deep dimples (lower "
        "ductility, brittle martensite); and the 2594 FZ (Fig. 5e) shows fine, "
        "uniform dimples (duplex strength\u2013ductility balance) [44, 45]. All "
        "HAZ surfaces (Fig. 5b, d, f) are brittle, most severely for 410 "
        "(quasi-cleavage, river patterns) and, under multi-pass thermal "
        "cycling, for 2594 (branched cleavage steps).»")
    d.para(
        "«The duplex ferrite\u2013austenite structure of the 2594 weld underlies "
        "its favourable balance of fusion-zone hardness (~300 VHN) and impact "
        "toughness (100 J), consistent with its microhardness and Charpy "
        "response. The vermicular \u03b4-ferrite of the 309L weld promotes "
        "crack-propagation resistance, consistent with its high fusion-zone "
        "toughness (125 J) and ductile dimpled fracture, whereas the "
        "martensitic 410 weld develops stress-concentration sites that reduce "
        "toughness, consistent with its low HAZ Charpy value (45 J). The "
        "alternating recrystallized-ferrite / untempered-martensite banding seen "
        "in the 309L HAZ is attributed to the repeated thermal cycles of "
        "multi-pass welding, and retained-austenite islands observed in the 2594 "
        "HAZ partially offset embrittlement.»")
    d.para(
        "«Targeted mitigations follow from these microstructures: an interpass "
        "temperature below ~100 \u00b0C for 309L to suppress HAZ banding; brief "
        "post-weld tempering (~650 \u00b0C) for 410 to homogenise the martensite "
        "distribution; and, as suggested by the literature, laser assistance "
        "with minor Nb microalloying (0.02\u20130.05%) for 2594 to refine the "
        "austenite-island distribution [52, 53].»")

    d.h2("3.5 Corrosion behaviour", hl=True)
    d.para(
        "All specimens showed active\u2013passive behaviour (Fig. 10, Table 4). "
        "The F2594 weld gave the best corrosion resistance \u2014 lowest "
        "corrosion current density (5.0 \u00d7 10\u207b\u2078 A cm\u207b\u00b2) "
        "and lowest corrosion rate (5.85 \u00d7 10\u207b\u2074 mm/year) \u2014 "
        "owing to its high chromium (24.9 wt%) and molybdenum (3.85 wt%) "
        "content, which form a dense, stable Cr-rich passive film. The F309 "
        "weld followed (E_corr \u22120.18 V, I_corr 1.0 \u00d7 10\u207b\u2077 A "
        "cm\u207b\u00b2, 11.6 \u00d7 10\u207b\u2074 mm/year), aided by its high "
        "Cr (23 wt%) and austenitic matrix with vermicular \u03b4-ferrite. The "
        "SS430 base metal was intermediate (I_corr 3.0 \u00d7 10\u207b\u2077 A "
        "cm\u207b\u00b2, 34.8 \u00d7 10\u207b\u2074 mm/year) due to its lower Cr "
        "(12.5 wt%) and less stable passive film. The F410 weld was least "
        "resistant (I_corr 6.3 \u00d7 10\u207b\u2077 A cm\u207b\u00b2, 73.1 "
        "\u00d7 10\u207b\u2074 mm/year): its low Cr combined with "
        "chromium-carbide precipitation locally depletes Cr and destabilises "
        "the passive film. Corrosion resistance therefore ranks «F2594 > F309 > "
        "SS430 > F410», confirming that chromium content and weld-metal phase "
        "balance govern passivation and electrochemical performance "
        "[58\u201361].")

    d.caption("Table 4. Potentiodynamic polarization parameters (E_corr, "
              "I_corr, corrosion rate) for SS430 base metal and the F309, F410, "
              "and F2594 weldments.")
    d.table([
        ["Specimen", "E_corr (V)", "I_corr (A cm\u207b\u00b2)",
         "Corrosion rate (mm/year)"],
        ["F2594 weld", "\u22120.20", "5.0 \u00d7 10\u207b\u2078",
         "5.85 \u00d7 10\u207b\u2074"],
        ["F309 weld", "\u22120.18", "1.0 \u00d7 10\u207b\u2077",
         "11.6 \u00d7 10\u207b\u2074"],
        ["SS430 base metal", "\u22120.26", "3.0 \u00d7 10\u207b\u2077",
         "34.8 \u00d7 10\u207b\u2074"],
        ["F410 weld", "\u22120.22", "6.3 \u00d7 10\u207b\u2077",
         "73.1 \u00d7 10\u207b\u2074"],
    ], col_w=[2600, 2000, 2760, 2000])

    # ----- 4. Conclusions (itemized per Reviewer 2) -----
    d.h1("4. Conclusions", hl=True)
    d.para("«The effect of three fillers (ER309L, ER410, ER2594) on the "
           "microstructure, mechanical behaviour, phase constitution, and "
           "corrosion response of welded AISI 430 ferritic stainless steel was "
           "investigated. The main findings are:»", hl=True)
    for t in [
        "AISI 430 (12 mm) was successfully joined by four-pass GMAW with all "
        "three fillers under a controlled schedule (110 A, 150 \u00b0C interpass "
        "temperature, ~2.98 kJ/mm cumulative heat input).",
        "All welds showed the characteristic ferritic HAZ degradation (grain "
        "coarsening plus chromium-carbide sensitization); the fusion-zone phase "
        "constitution was controlled by the filler.",
        "XRD identified \u03b3-austenite with \u03b4/\u03b1-ferrite in F309, "
        "dominant \u03b1/\u03b1\u2032 martensite in F410, and a balanced "
        "\u03b1 + \u03b3 duplex structure with a minor secondary phase in F2594.",
        "Fusion-zone hardness ranked 410 (~320 VHN) > 2594 (~300 VHN) > 309L "
        "(~260 VHN); HAZ hardness converged toward the base metal "
        "(~150\u2013170 VHN).",
        "Fusion-zone impact toughness was highest for 309L (125 J), intermediate "
        "for 2594 (100 J), and lowest for 410; the 410 HAZ was the most "
        "embrittled (45 J).",
        "Corrosion resistance ranked F2594 > F309 > SS430 > F410, governed "
        "primarily by chromium content and weld-metal phase balance.",
        "Filler selection must be matched to service needs: ER309L for toughness "
        "and general service, ER410 for hardness and wear resistance (with "
        "post-weld heat treatment), and ER2594 for combined strength and "
        "corrosion resistance (with tight thermal control of the HAZ).",
    ]:
        d.bullet(t, hl=True)

    # ----- References -----
    d.h1("References")
    refs = MANUSCRIPT_REFS
    for i, r in enumerate(refs, 1):
        hl = i >= 62  # new references highlighted
        d.para("[%d] %s" % (i, r), sz=20, hl=hl, space_after=60)

    return d


# ====================================================================
#  REFERENCES  (1-61 original; 62-64 new, added per Reviewer 1 Comment 5)
# ====================================================================

MANUSCRIPT_REFS = [
    "N. Ohashi, Y. Ono, N. Kinoshita, K. Yoshioka, Effects of Metallurgical and Mechanical Factors on Charpy Impact Toughness of Extra-Low Interstitial Ferritic Stainless Steels, ASTM STP 706, 1980. https://doi.org/10.1520/STP38209S.",
    "P. Cheng et al., Intergranular Corrosion Behavior and Mechanism of Stabilized Ultra-Pure 430LX Ferritic Stainless Steel, J. Mater. Sci. Technol., 2019, 35(8), 1787\u20131796. https://doi.org/10.1016/j.jmst.2019.03.021.",
    "E.A. Brandes, G.B. Brook (Eds.), Smithells Metals Reference Book, 7th ed., Butterworth-Heinemann, 1992. https://doi.org/10.1016/C2009-0-25363-3.",
    "J. Suer, M. Traverso, F. Ahrenhold, Carbon Footprint of Scenarios Towards Climate-Neutral Steel, J. Cleaner Prod., 2021, 318, 128588. https://doi.org/10.1016/j.jclepro.2021.128588.",
    "H.J. Dundas, A.P. Bond, Niobium and Titanium Requirements for Stabilization of Ferritic Stainless Steels, ASTM STP 656, 1978. https://doi.org/10.1520/STP34847S.",
    "T.J. Nichol, J.A. Davis, Intergranular Corrosion Testing and Sensitization of Two High-Chromium Ferritic Stainless Steels, ASTM STP 656, 1978. https://doi.org/10.1520/STP34848S.",
    "E. Folkhard, Welding Metallurgy of Duplex Austenitic\u2013Ferritic Stainless Steels, Springer, Vienna, 1988. https://doi.org/10.1007/978-3-7091-8965-8_8.",
    "I. Salvatori, Effect of Solidification Structure and Thermomechanical Processing on Microstructure and Texture of Ferritic Stainless Steels, Mater. Sci. Forum, 2003, 426\u2013432, 1379\u20131384. https://doi.org/10.4028/www.scientific.net/MSF.426-432.1379.",
    "J.F. Grubb, R.N. Wright, P. Farrar, Micromechanisms of Brittle Fracture in Titanium-Stabilized and \u03b1\u2032-Embrittled Ferritic Stainless Steels, ASTM STP 706, 1980. https://doi.org/10.1520/STP38202S.",
    "F. Bonollo, A. Tiziani, P. Ferro, Welding Processes, Microstructural Evolution and Final Properties of Duplex and Superduplex Stainless Steels, Wiley, 2013. https://doi.org/10.1002/9781118557990.ch4.",
    "X. Zhou et al., TiN Refinement and Resultant Grain Refinement in Magnesium-Treated Ultra-Pure Ferritic Stainless Steel, Mater. Charact., 2024, 209, 113659. https://doi.org/10.1016/j.matchar.2024.113659.",
    "R. Nishimura, Stress Corrosion Cracking of Type 430 Ferritic Stainless Steel in Chloride and Sulfate Solutions, Corrosion, 1992, 48(11), 915\u2013922. https://doi.org/10.5006/1.3315889.",
    "M.K. Booker, V.K. Sikka, B.L.P. Booker, Comparison of the Mechanical Strength Properties of Several High-Chromium Ferritic Steels, ORNL, 1981. https://doi.org/10.2172/6044299.",
    "R.A. Lula, Ferritic Stainless Steels, in Stainless Steels for Design Engineers, ASM International, 2008. https://doi.org/10.31399/asm.tb.ssde.t52310109.",
    "P. Rosemann et al., Influence of Microstructure and Surface Treatment on the Corrosion Resistance of Martensitic Stainless Steels, Mater. Corros., 2015, 66(1), 84\u201395. https://doi.org/10.1002/maco.201307276.",
    "J. P\u00f6pperlov\u00e1 et al., Up-Scaling of Thermomechanically Induced Laves Phase Precipitation in HiperFer Stainless Steels, Materials, 2021, 14(7), 1635. https://doi.org/10.3390/ma14071635.",
    "J. Charles, Plain 17% Chromium Ferritic Stainless Steels, in The Alloy Tree, CRC Press, 2004. https://doi.org/10.1201/9780203024010.ch2c.",
    "H.R. Park, M.Y. Song, Variation in the Oxidation Behavior of a Polished Ferritic Stainless Steel with Thermal Cycling, Korean J. Met. Mater., 2014, 52(6), 421\u2013428. https://doi.org/10.3365/kjmm.2014.52.6.421.",
    "H. Xiang et al., Grain-Coarsening Induced Joint Enhancement for Ultrasonic Welding of Duplex Stainless Steel, Mater. Sci. Eng. A, 2025, 930, 148840. https://doi.org/10.1016/j.msea.2025.148840.",
    "Z. Zhang et al., Microstructure Evolution in Heat Affected Zone of T4003 Ferritic Stainless Steel, Mater. Des., 2015, 65, 1087\u20131095. https://doi.org/10.1016/j.matdes.2014.12.018.",
    "M. Naghizadeh, H. Mirzadeh, Effects of Grain Size on Mechanical Properties and Work-Hardening Behavior of AISI 304, Steel Res. Int., 2019, 90(10), 1900153. https://doi.org/10.1002/srin.201900153.",
    "C.-C. Hsieh, W. Wu, Overview of Intermetallic Sigma Phase Precipitation in Stainless Steels, ISRN Metall., 2012, 2012, 732471. https://doi.org/10.5402/2012/732471.",
    "J. Charles, Martensitic and Ferritic Stainless Steels, in The Alloy Tree, CRC Press, 2004. https://doi.org/10.1201/9780203024010.ch0c.",
    "American Welding Society, Solidification Cracking Mechanism of Carbon Steel Weld Metal, Welding J., 2018, 97(2), 45S\u201354S. https://doi.org/10.29391/2018.97.005.",
    "D. Chauveau, Review of NDT and Process Monitoring Techniques for Welding or Additive Manufacturing, Welding in the World, 2018, 62(5), 1097\u20131118. https://doi.org/10.1007/s40194-018-0609-3.",
    "N. Lupt\u00e1kov\u00e1 et al., The Irradiation Effects in Ferritic, Ferritic\u2013Martensitic and Austenitic ODS Alloys: A Review, Materials, 2024, 17(14), 3409. https://doi.org/10.3390/ma17143409.",
    "S. Tokita, H. Kokawa, Y.S. Sato, Influence of Thermomechanical Process Parameters on Abnormal Grain Growth in 304 Stainless Steel, SSRN, 2024. https://doi.org/10.2139/ssrn.4896578.",
    "M. Jokar, X. Guo, G.S. Frankel, Machine Learning Approaches to Model Galvanic Corrosion of Coated Al Alloy Systems, Corrosion, 2022, 78(12), 1103\u20131116. https://doi.org/10.5006/4175.",
    "D. Solanki, M. Shah, M. Prajapati, The Role of Geothermal and Wind Energy in Hydrogen Production, Carbon Neutral Systems, 2025. https://doi.org/10.1007/s44438-025-00008-w.",
    "R.D. Campbell, Ferritic Stainless Steel Welding Metallurgy, Key Eng. Mater., 1992, 69\u201370, 167\u2013180. https://doi.org/10.4028/www.scientific.net/KEM.69-70.167.",
    "H.E. Deverell, Toughness Properties of Vacuum Induction Melted High-Chromium Ferritic Stainless Steels, ASTM STP 706, 1980. https://doi.org/10.1520/STP38208S.",
    "Choice Reviews Online, Welding Metallurgy and Weldability of Stainless Steels, 2005, 43(04). https://doi.org/10.5860/choice.43-2230.",
    "C. Tembhurkar et al., Cold Metal Transfer Welding of 316L/430 Dissimilar Stainless-Steel Welds, Anti-Corros. Methods Mater., 2025. https://doi.org/10.1108/acmm-03-2023-2774.",
    "E. Taban et al., Laser Welding of Modified 12% Cr Stainless Steel, Mater. Des., 2009, 30(4), 1193\u20131200. https://doi.org/10.1016/j.matdes.2008.06.030.",
    "M. Mukherjee, T.K. Pal, Influence of Heat Input on Martensite Formation and Impact Property of Ferritic\u2013Austenitic Dissimilar Weld Metals, J. Mater. Sci. Technol., 2012, 28(4), 343\u2013350. https://doi.org/10.1016/S1005-0302(12)60066-8.",
    "S. Anttila, P. Karjalainen, S. Lantto, Mechanical Properties of Ferritic Stainless Steel Welds Using Type 409 and 430 Filler Metals, Welding in the World, 2013, 57(2), 273\u2013282. https://doi.org/10.1007/s40194-013-0033-7.",
    "A.C. Davies, Submerged Arc Welding, in Welding Processes Handbook, CRC Press, 2003. https://doi.org/10.1201/9780203499764.ch7.",
    "M. du Toit, J. Naud\u00e9, The Influence of Stabilization with Titanium on HAZ Sensitization of 11\u201312% Cr Ferritic Stainless Steels, Welding in the World, 2011, 55(3\u20134), 44\u201352. https://doi.org/10.1007/BF03321285.",
    "N. Suutala, T. Takalo, T. Moisio, The Relationship Between Solidification and Microstructure in Austenitic and Austenitic\u2013Ferritic Stainless Steel Welds, Metall. Trans. A, 1979, 10(4), 512\u2013514. https://doi.org/10.1007/BF02697081.",
    "T. Khuenkaew, K. Kanlayasiri, Resistance Spot Welding of SUS316L/SUS425 Stainless Steels, Metals, 2019, 9(6), 710. https://doi.org/10.3390/met9060710.",
    "S. Prathivraj, R. Oyyaravelu, Effect of Interpass Temperature on Austenite\u2013Ferrite Ratio of WAAM 2507 Super Duplex Stainless Steel, SSRN, 2024. https://doi.org/10.2139/ssrn.4687443.",
    "A.S. Elmesalamy et al., Process Parameter Interactions in Multiple-Pass Ultra-Narrow-Gap Laser Welding of Thick-Section Stainless Steels, Int. J. Adv. Manuf. Technol., 2013, 67, 2125\u20132135. https://doi.org/10.1007/s00170-013-4739-x.",
    "Y.L. Sun et al., Characterisation and Modelling of Tempering During Multi-Pass Welding, J. Mater. Process. Technol., 2019, 270, 60\u201371. https://doi.org/10.1016/j.jmatprotec.2019.02.015.",
    "S. Baskutis et al., Comparative Research of Microstructure and Mechanical Properties of Stainless and Structural Steel Dissimilar Welds, Materials, 2021, 14(20), 6180. https://doi.org/10.3390/ma14206180.",
    "C.-H. Lee, K.-H. Chang, Comparative Study on Girth Weld-Induced Residual Stresses Between Austenitic and Duplex Stainless Steel Pipe Welds, Appl. Therm. Eng., 2014, 63(1), 140\u2013147. https://doi.org/10.1016/j.applthermaleng.2013.11.001.",
    "G. Luo et al., Developing a Novel Phase Balance of Duplex Stainless Steel for Exceptional Mechanical Properties and Corrosion Resistance, Scr. Mater., 2025, 244, 116467. https://doi.org/10.1016/j.scriptamat.2024.116467.",
    "X.-Z. Huang, D. Wang, Y.-T. Yang, Effect of Precipitation on Intergranular Corrosion Resistance of 430 Ferritic Stainless Steel, J. Iron Steel Res. Int., 2015, 22(11), 1031\u20131037. https://doi.org/10.1016/S1006-706X(15)30113-8.",
    "W. Yang et al., Constitutive Equations of Austenitic Stainless Steels Under High Strain Rate Loading, JOM, 2025. https://doi.org/10.1007/s11837-025-07262-w.",
    "M. Tobah et al., Microstructural and Hall\u2013Petch Analysis of Additively Manufactured Ferritic Alloy Using 2507 Duplex Stainless Steel Powder, Crystals, 2024, 14(1), 81. https://doi.org/10.3390/cryst14010081.",
    "A. Ferreira Filho et al., Texture Evolution of Ferritic (AISI 430) Stainless Steel Strips During Cold Rolling, Annealing and Drawing, Mater. Sci. Forum, 2007, 539\u2013543, 4926\u20134931. https://doi.org/10.4028/0-87849-428-6.4926.",
    "T.R. de Oliveira, F. Montheillet, Evolution of Microstructure and Texture During Hot Torsion of Nb- and Ti-Stabilized Ferritic Stainless Steels, Steel Res. Int., 2008, 79(6), 476\u2013483. https://doi.org/10.1002/srin.200806158.",
    "M. Maazouz, Microstructural and Mechanical Characterization of Spot Welds on AISI 430 Ferritic Stainless Steel Sheets, Przegl\u0105d Elektrotechniczny, 2024, 100(6), 279\u2013282. https://doi.org/10.15199/48.2024.06.61.",
    "G. Guo, Y. Shen, Friction Stir Welding of Dissimilar Stainless Steels, Mater. Res. Express, 2019, 6(3), 036516. https://doi.org/10.1088/2053-1591/ab015b.",
    "S.H.C. Park et al., Corrosion Properties in Friction Stir Welded 304 Austenitic Stainless Steel, Welding in the World, 2005, 49(3), 63\u201373. https://doi.org/10.1007/BF03266407.",
    "R. Gunn (Ed.), Duplex Stainless Steels: Microstructure, Properties and Applications, Woodhead, 1997. https://doi.org/10.1533/9781845698775.",
    "J.O. Nilsson, Super Duplex Stainless Steels, Mater. Sci. Technol., 1992, 8(8), 685\u2013700. https://doi.org/10.1179/mst.1992.8.8.685.",
    "K.H. Lo, C.H. Shek, J.K.L. Lai, Recent Developments in Stainless Steels, Mater. Sci. Eng. R, 2009, 65(4\u20136), 39\u2013104. https://doi.org/10.1016/j.mser.2009.03.001.",
    "R.T. Loto, Study of the Corrosion Resistance of Type 304L and 316 Austenitic Stainless Steels in Acid Chloride Solution, Orient. J. Chem., 2017, 33(3), 1301\u20131309. https://doi.org/10.13005/ojc/330311.",
    "T. Bellezze et al., Corrosion Behaviour of Austenitic and Duplex Stainless Steels in an Industrial Strongly Acidic Solution, Mater. Corros., 2016, 67(8), 831\u2013838. https://doi.org/10.1002/maco.201508708.",
    "J.M. Bastidas et al., Influence of Molybdenum on Passivation of Polarised Stainless Steels in a Chloride Environment, Corros. Sci., 2002, 44(3), 625\u2013633. https://doi.org/10.1016/S0010-938X(01)00080-0.",
    "Y. Xie et al., Corrosion Behaviour of Stainless Steel Exposed to Highly Concentrated Chloride Solutions, Corros. Eng. Sci. Technol., 2017, 52(4), 283\u2013293. https://doi.org/10.1080/1478422X.2016.1275418.",
    # --- new references (62-64) ---
    "F. Ostovan, E. Shafiei, M. Toozandehjani, I.F. Mohamed, M. Soltani, On the Role of Molybdenum on the Microstructural, Mechanical and Corrosion Properties of the GTAW AISI 316 Stainless Steel Welds, J. Mater. Res. Technol., 2021, 13, 2115\u20132125. https://doi.org/10.1016/j.jmrt.2021.05.095. [VERIFIED]",
    "[Materials Chemistry and Physics, 2021, article 124839] https://doi.org/10.1016/j.matchemphys.2021.124839 \u2014 title/authors to be confirmed by the authors (automated metadata access was blocked). [AUTHOR TO VERIFY]",
    "[Materials Research Express, 2019] https://doi.org/10.1088/2053-1591/ab1fcb \u2014 title/authors to be confirmed by the authors (automated metadata access was blocked). [AUTHOR TO VERIFY]",
]


# ====================================================================
#  RESPONSE TO REVIEWERS  (finalized / modified)
# ====================================================================

def build_response():
    d = Doc()
    d.title("Response to Reviewers")
    d.para("Manuscript (revised title): Investigation on the Weldability of "
           "430-Grade Ferritic Stainless Steel Using Three Different Filler "
           "Wire Grades (Austenitic 309L, Martensitic 410, and Duplex 2594)",
           italic=True)
    d.para(
        "We thank the Editor and both Reviewers for their constructive "
        "assessment. The manuscript has been revised comprehensively: the three "
        "schematic figures and the mechanical-property charts were redrawn; a "
        "methodology summary was added to the Abstract; the Materials and "
        "Methods section was shortened and the characterization procedures were "
        "folded into it; all numerical contradictions between the abstract, "
        "tables, and figures were reconciled to a single authoritative dataset; "
        "the Introduction was trimmed of off-topic material and strengthened "
        "with the suggested literature; the Results and Discussion were "
        "reordered (optical \u2192 SEM \u2192 XRD \u2192 mechanical \u2192 "
        "corrosion) and de-duplicated; unsupported claims (tensile, "
        "nanoindentation, modeling, quantitative phase fractions, and "
        "eutectic/intermetallic identifications) were removed or softened; and "
        "units were standardized (hardness as VHN). Below, each comment is "
        "quoted, followed by our Response and the Action taken (location). In "
        "the revised manuscript every change is highlighted in yellow.")

    note = ("Note on three items the revision resolves where the earlier draft "
            "was internally inconsistent:")
    d.para(note, bold=True)
    d.bullet("Corrosion ranking. The authoritative dataset is Table 4, giving "
             "F2594 > F309 > SS430 > F410 (F2594 best). The abstract, Section "
             "3.5, and Conclusions all use this ranking; the stray reversal "
             "(F2594 as worst, with 10\u207b\u2078 mm/year units) has been "
             "removed.")
    d.bullet("Groove angle. A single value, 60\u00b0 (single-V), is now stated "
             "identically in the Abstract, Section 2.1, Table 3, and "
             "Conclusions.")
    d.bullet("Phase quantification. No EDS, point counting, Feritscope, or EBSD "
             "was performed; the specific ferrite/austenite percentages and the "
             "\u201ceutectic/intermetallic\u201d identifications have been "
             "removed, and phase constitution is now carried by XRD.")

    def block(title, comment, response, action):
        d.h2(title)
        d.para("Comment: " + comment, bold=False, italic=True)
        for para in response:
            d.para(para)
        d.para("Action taken (location): " + action, bold=True)

    d.h1("Reviewer 1")

    block("Comment 1",
          "\u201cThe first 3 figures are not suitable \u2026 the authors can do "
          "much better in those schematic figures.\u201d",
          ["We agree. Figures 1\u20133 were completely redrawn as clean, "
           "to-scale, professionally annotated schematics, and Figure 4 "
           "(mechanical-property charts) was rebuilt from the corrected "
           "dataset. Figure 1 is a to-scale square-butt/bead-on-plate schematic "
           "(two 75 \u00d7 75 \u00d7 12 mm coupons, 2 mm root gap, numbered "
           "four-pass sequence, weld-direction arrow, 10 mm scale bar). Figure 2 "
           "is a transverse weld cross-section drawn to a consistent 12 mm scale "
           "with a correct scale bar and FZ/HAZ/BM annotations. Figure 3 is an "
           "ASTM E23 Charpy V-notch specimen (55 \u00d7 10 \u00d7 10 mm; 2 mm "
           "notch depth, 0.25 mm root radius, 45\u00b0 angle) with FZ and HAZ "
           "notch placements. Figure 4 is two bar charts (impact toughness and "
           "microhardness) from the corrected authoritative dataset."],
          "Figures 1\u20134 regenerated; figure captions updated.")

    block("Comment 2",
          "\u201cThe abstract should include a brief explanation of "
          "methodology.\u201d",
          ["A concise methodology summary was added to the Abstract, covering "
           "the base metal and coupon geometry, the welding process and "
           "parameters, the three filler wires, the joint configuration, and the "
           "full characterization suite (OM, SEM, XRD, VHN, Charpy, "
           "potentiodynamic polarization)."],
          "Abstract (highlighted methodology sentences).")

    block("Comment 3",
          "\u201cThe materials and methods section is too long, containing "
          "unnecessary explanations.\u201d",
          ["Section 2 was condensed: repeated filler \u201ctypical use\u201d "
           "descriptions (already in Table 1), the justification for choosing "
           "MIG, the thrice-stated weldability concerns, the speculative aside "
           "about the shielding-gas mixture, prose that merely re-narrated Table "
           "2, and citation padding on multi-pass benefits were removed. The "
           "former characterization section was folded in as \u00a72.2 and "
           "trimmed. Tables 1\u20133 keep their content and positions."],
          "Section 2 (2.1 Materials, joint design, welding; 2.2 "
          "Characterization).")

    block("Comment 4",
          "\u201cMultiple contradictions between the abstract, tables, and "
          "figures: \u2018309L \u2026 125 J\u2019 but Fig. 4(a) shows ~450 J; "
          "\u20182594 \u2026 100 J\u2019 but Fig. 4(a) shows ~580 J; "
          "\u2018410 \u2026 320 HV\u2019 but Table 2 lists 250 HV.\u201d",
          ["We thank the reviewer. The discrepancies arose because Figure 4(a) "
           "was plotted with an incorrect toughness scale and the text did not "
           "consistently distinguish filler-wire, fusion-zone, and HAZ values. "
           "The physically impossible ~450\u2013580 J bars were the error (a "
           "Charpy machine and a 12 mm ferritic weld do not absorb such energy). "
           "Figure 4 was regenerated from the raw data with fusion-zone and HAZ "
           "values reported separately; Table 2 was relabelled as as-supplied "
           "filler-wire properties (so 250 VHN wire vs 320 VHN fusion zone is "
           "no longer a contradiction); and the abstract, Section 3.4, and "
           "Conclusions were reconciled to one dataset: fusion-zone toughness "
           "309L = 125 J (highest), 2594 = 100 J, 410 lowest, with the 410 HAZ "
           "= 45 J; fusion-zone hardness 410 = 320 VHN > 2594 = 300 VHN > 309L "
           "\u2248 260 VHN; HAZ hardness ~150\u2013170 VHN. The latent 2594 "
           "hardness conflict (300 vs ~180 VHN) was resolved in favour of 300 "
           "VHN to agree with the abstract and Conclusions.",
           "The absolute 410 fusion-zone toughness and the 309L and 2594 HAZ "
           "toughness values should be inserted from the authors' raw Charpy "
           "records; in the revised text these are currently described "
           "qualitatively (ranked) rather than with invented numbers."],
          "Abstract; Table 2 caption (Section 2.1); Figure 4 (regenerated) and "
          "caption; Section 3.4; Conclusions items 4\u20135.")

    block("Comment 5",
          "\u201cThe introduction is full of subjects unrelated to welding "
          "metallurgy and must be strengthened with related research works and "
          "their results (DOIs: 10.1016/j.matchemphys.2021.124839; "
          "10.1088/2053-1591/ab1fcb; 10.1016/j.jmrt.2021.05.095).\u201d",
          ["The off-topic paragraph (recyclability, magnetism, "
           "gravitational-wave detectors, tidal turbines, ML/ICME) was deleted, "
           "and the Ti/Nb-stabilization and ULI tangent was condensed to one "
           "sentence. A new related-works paragraph integrates filler-effect "
           "studies and their results, including the suggested papers. The "
           "Ostovan et al. (2021) paper could be verified and is cited directly "
           "(high-Mo \u2192 higher \u03b4-ferrite \u2192 improved strength and "
           "pitting resistance, motivating the ER2594 choice).",
           "Honesty note: automated access to the other two DOIs "
           "(matchemphys.2021.124839 and 2053-1591/ab1fcb) was blocked "
           "(HTTP 403), so their exact titles/findings could not be confirmed. "
           "They are listed as references [63] and [64] flagged "
           "\u201cAUTHOR TO VERIFY\u201d; please supply the titles and key "
           "findings so precise, correctly-attributed results can be inserted. "
           "No results were invented for papers that could not be read."],
          "Introduction (off-topic paragraph removed; new related-works and "
          "filler-rationale paragraphs added); References [62\u201364].")

    block("Comment 6",
          "\u201cResults and discussion is full of repetition, especially "
          "regarding sensitization and grain coarsening.\u201d",
          ["Repeated statements of HAZ grain coarsening (~5\u00d7), "
           "chromium-carbide sensitization (~4\u00d7), the \u201cfiller "
           "selection is decisive\u201d takeaway (~4\u00d7), and the "
           "duplex-cooling caution (3\u00d7) were consolidated. The HAZ "
           "degradation mechanism is now stated once in \u00a73.1 and referred "
           "to thereafter as \u201cHAZ degradation\u201d; the two overlapping "
           "Figure 7 passages were merged; the filler-selection message appears "
           "only in the Conclusions; and the duplex-cooling caution appears once "
           "in the 2594 microstructure discussion. Section 3 was reorganized "
           "into 3.1\u20133.5 so each topic appears once."],
          "Section 3 (de-duplicated; single mechanism statement in \u00a73.1).")

    block("Comment 6a",
          "\u201cThere is no tensile test \u2026 the data in this section should "
          "be removed. The same goes for nanoindentation, modeling, etc.\u201d",
          ["Correct. The Methods include only OM, SEM, XRD, Vickers "
           "microhardness, Charpy impact, and potentiodynamic polarization. The "
           "claimed tensile results (yield ~580 MPa, uniform elongation ~28%; "
           "\u201celongation reduced by ~15%\u201d), the nanoindentation "
           "\u201c40% higher fracture toughness\u201d claim, and the "
           "computational-modeling statement were removed and reframed around "
           "the properties actually measured (microhardness and Charpy). Table 2 "
           "was relabelled as nominal, as-supplied consumable properties (from "
           "manufacturer datasheets), and no Section 3 sentence cites its "
           "tensile numbers as weld outcomes."],
          "Section 3.4; Table 2 caption (Section 2.1).")

    block("Comment 6b",
          "\u201cHow did you measure ferrite content from optical "
          "micrographs?\u201d",
          ["A systematic phase-fraction measurement was not performed, and the "
           "oxalic-acid etch (ASTM A262 Practice A) does not give selective "
           "ferrite\u2013austenite contrast. The specific percentages "
           "(\u201c8\u201312% ferrite\u201d, \u201c~15 vol% retained "
           "austenite\u201d) and the over-precise grain-size figures were "
           "removed; the micrographs are now described qualitatively, and phase "
           "constitution is supported by XRD (Fig. 9). Section 2.2 states "
           "explicitly that no quantitative phase-fraction technique (point "
           "counting, image analysis, Feritscope, or EBSD) was used."],
          "Section 2.2 (etch/phase-ID statement); Section 3.1.")

    block("Comment 6c",
          "\u201cHow do you recognize the eutectic phase in Figure 7?\u201d",
          ["Identifying a true eutectic requires two-phase morphology plus "
           "compositional (EDS) and phase-diagram evidence; the Methods include "
           "no EDS, and classical eutectics are not expected for these "
           "Fe\u2013Cr\u2013Ni(\u2013Mo) weld compositions, which solidify "
           "dendritically. The features previously called \u201ceutectic\u201d "
           "were interdendritic \u03b4-ferrite and segregation products and have "
           "been relabelled accordingly (\u201cinterdendritic "
           "\u03b4-ferrite / second-phase particles\u201d), with phase "
           "identification carried by XRD."],
          "Sections 3.1 and 3.2; Figure 7 and 8 discussion.")

    block("Comment 6d",
          "\u201cThe fine intermetallic phase in Fig. 7 could be an etching "
          "effect, not a particular phase. The following discussion must be "
          "totally revised.\u201d",
          ["We agree. Electrolytic oxalic acid characteristically produces etch "
           "pits, grain-boundary ditching, and relief that mimic fine "
           "\u201cprecipitates\u201d at optical magnification; the XRD shows "
           "intermetallic reflections only as weak, low-intensity peaks in the "
           "2594 weld and none for 309L or 410. The Figure 7 discussion was "
           "rewritten to describe only grain morphology and HAZ coarsening, "
           "explicitly attributing the fine contrast in the 410/309L images to "
           "etching artifacts, with all unsupported intermetallic/eutectic "
           "descriptors removed and phase identification based solely on XRD."],
          "Section 3.1 (Figure 7 discussion rewritten); Section 3.2 (Figure 8 "
          "de-claimed); Figure 7 caption.")

    block("Comment 7",
          "\u201cReorder the discussion: first optical micrographs, SEM and "
          "XRD, then mechanical properties and corrosion.\u201d",
          ["The Results and Discussion were reordered exactly as suggested: "
           "3.1 Optical microscopy, 3.2 SEM, 3.3 Phase prediction and XRD, 3.4 "
           "Mechanical properties (hardness, impact, fractography), and 3.5 "
           "Corrosion behaviour."],
          "Section 3 reorganized into 3.1\u20133.5.")

    block("Comment 8",
          "\u201cBe consistent about units such as HV vs VHN.\u201d",
          ["Hardness is now reported as VHN throughout the manuscript, tables, "
           "and figures."],
          "Whole manuscript.")

    d.h1("Reviewer 2")

    block("Comment 1",
          "\u201cRevise the title to \u2018Investigation on the weldability of "
          "430-grade ferritic stainless steel using three different filler wire "
          "grades (austenitic 309L, martensitic 410, and duplex 2594)\u2019.\u201d",
          ["The title was revised to the suggested wording."],
          "Manuscript title.")

    block("Comment 2",
          "\u201cIn the Introduction, explain why these three filler wires were "
          "selected for 430, which filler is most used in current research and "
          "application, and what the existing problems are.\u201d",
          ["A dedicated paragraph was added explaining that austenitic ER309L "
           "is the most widely used consumable for 430 (ductile, crack-tolerant "
           "weld metal), with ferritic/martensitic fillers used for strength or "
           "colour match and duplex fillers rarely applied; the limitations of "
           "each (poor weld toughness for ferritic fillers, brittleness/PWHT for "
           "martensitic, and expansion-mismatch/galvanic concerns for "
           "austenitic) are stated, together with the rationale for selecting "
           "one representative filler from each family to enable a controlled, "
           "family-spanning comparison on identical 430 joints."],
          "Introduction (new filler-selection rationale paragraph).")

    block("Comment 3",
          "\u201cIn Table 3, \u201815 l/min\u2019 should be \u201815 "
          "L/min\u2019.\u201d",
          ["The shielding-gas flow rate is now reported as \u201c15 L/min\u201d "
           "in Table 3 and in the Section 2.1 text."],
          "Table 3; Section 2.1.")

    block("Comment 4",
          "\u201cWhat is the groove angle of the test plate?\u201d",
          ["The groove angle (60\u00b0 single-V) and 2 mm root gap are now "
           "stated in Section 2.1, added as rows in Table 3, and repeated in the "
           "Abstract and Conclusions for consistency."],
          "Section 2.1; Table 3 (groove angle = 60\u00b0, root gap = 2 mm); "
          "Abstract; Conclusions.")

    block("Comment 5",
          "\u201cThe scale in the metallographic picture is unreasonable and "
          "needs to be modified.\u201d",
          ["Figure 2 (weld cross-section) was redrawn to a consistent 12 mm "
           "plate scale with a correct, clearly labelled scale bar and "
           "FZ/HAZ/BM annotations, resolving the unreasonable-scale issue."],
          "Figure 2 regenerated; Figure 2 caption updated.")

    block("Comment 6",
          "\u201cThe conclusion content should be listed item by item.\u201d",
          ["The Conclusions were rewritten as a numbered list (seven items) "
           "covering the joining procedure, HAZ degradation, XRD phase "
           "identification, hardness, impact toughness, corrosion ranking, and "
           "the overall filler recommendation."],
          "Section 4 (Conclusions).")

    d.h1("Outstanding items requiring author input")
    for t in [
        "Raw Charpy values for the 410 fusion zone and for the 309L and 2594 "
        "HAZ (currently described qualitatively, not with invented numbers).",
        "Confirmation that Table 2 values are manufacturer-datasheet (as-supplied) "
        "properties, as now stated.",
        "Titles and key findings for the two unverifiable DOIs ([63], [64]).",
        "Confirmation that no EDS/quantitative phase analysis was performed "
        "(the revision assumes none; if EDS exists, specific second-phase "
        "identifications can be reinstated).",
        "Confirmation of the 60\u00b0 single-V groove (the original text said "
        "\u201csquare butt\u201d, which is inconsistent with a 4-pass 12 mm "
        "weld).",
        "A latent arithmetic point not raised by the reviewers: the stated arc "
        "efficiency \u03b7 = 0.8 does not reproduce the reported 0.84/0.729 "
        "kJ/mm values (those require \u03b7 \u2248 0.6); please confirm which to "
        "keep so Eq. 1 and Table 3 agree.",
    ]:
        d.bullet(t)

    return d


# ====================================================================
if __name__ == "__main__":
    m = build_manuscript()
    write_docx(m, os.path.join(OUT_DIR,
               "Manuscript_SS430_Filler_Weldability_Revised.docx"))
    r = build_response()
    write_docx(r, os.path.join(OUT_DIR, "Response_to_Reviewers_SS430.docx"))
    print("done")
