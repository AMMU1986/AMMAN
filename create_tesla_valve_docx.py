#!/usr/bin/env python3
"""
Create Tesla Valve CFD Manuscript as DOCX file.
Uses raw OOXML manipulation (no external dependencies).
"""

import zipfile
import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Namespaces
NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
    'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
}


def create_content_types():
    """Create [Content_Types].xml"""
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="svg" ContentType="image/svg+xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''


def create_rels():
    """Create _rels/.rels"""
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''


def create_word_rels():
    """Create word/_rels/document.xml.rels"""
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>'''


def create_styles():
    """Create word/styles.xml with academic paper styles."""
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="en-US"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="120" w:line="360" w:lineRule="auto"/>
        <w:jc w:val="both"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  
  <w:style w:type="paragraph" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:pPr>
      <w:spacing w:after="120" w:line="360" w:lineRule="auto"/>
      <w:jc w:val="both"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="24"/>
    </w:rPr>
  </w:style>
  
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="240" w:after="240"/>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="32"/>
      <w:szCs w:val="32"/>
    </w:rPr>
  </w:style>
  
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="360" w:after="120"/>
      <w:jc w:val="left"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="28"/>
      <w:szCs w:val="28"/>
    </w:rPr>
  </w:style>
  
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="240" w:after="120"/>
      <w:jc w:val="left"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="26"/>
      <w:szCs w:val="26"/>
    </w:rPr>
  </w:style>
  
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="200" w:after="80"/>
      <w:jc w:val="left"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:i/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
  </w:style>
  
  <w:style w:type="paragraph" w:styleId="Caption">
    <w:name w:val="caption"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="60" w:after="200"/>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:rPr>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
      <w:i/>
    </w:rPr>
  </w:style>
  
  <w:style w:type="paragraph" w:styleId="TableText">
    <w:name w:val="Table Text"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:after="0" w:line="240" w:lineRule="auto"/>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:rPr>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
  </w:style>
  
  <w:style w:type="paragraph" w:styleId="Abstract">
    <w:name w:val="Abstract"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="120" w:after="120"/>
      <w:ind w:left="720" w:right="720"/>
    </w:pPr>
    <w:rPr>
      <w:sz w:val="22"/>
      <w:szCs w:val="22"/>
    </w:rPr>
  </w:style>
</w:styles>'''


def create_numbering():
    """Create word/numbering.xml for ordered lists."""
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:abstractNum w:abstractNumId="0">
    <w:lvl w:ilvl="0">
      <w:start w:val="1"/>
      <w:numFmt w:val="decimal"/>
      <w:lvlText w:val="%1."/>
      <w:lvlJc w:val="left"/>
    </w:lvl>
  </w:abstractNum>
  <w:num w:numId="1">
    <w:abstractNumId w:val="0"/>
  </w:num>
</w:numbering>'''


# ============================================================
# Document Body Builder
# ============================================================

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def make_paragraph(text, style=None, bold=False, italic=False, size=None, alignment=None, 
                   spacing_before=None, spacing_after=None, indent_left=None):
    """Create a paragraph XML string."""
    p_xml = f'<w:p xmlns:w="{W}">'
    
    # Paragraph properties
    ppr_parts = []
    if style:
        ppr_parts.append(f'<w:pStyle w:val="{style}"/>')
    if alignment:
        ppr_parts.append(f'<w:jc w:val="{alignment}"/>')
    spacing_attrs = []
    if spacing_before:
        spacing_attrs.append(f'w:before="{spacing_before}"')
    if spacing_after:
        spacing_attrs.append(f'w:after="{spacing_after}"')
    if spacing_attrs:
        ppr_parts.append(f'<w:spacing {" ".join(spacing_attrs)}/>')
    if indent_left:
        ppr_parts.append(f'<w:ind w:left="{indent_left}"/>')
    
    if ppr_parts:
        p_xml += '<w:pPr>' + ''.join(ppr_parts) + '</w:pPr>'
    
    # Run properties
    if text:
        rpr_parts = []
        if bold:
            rpr_parts.append('<w:b/>')
        if italic:
            rpr_parts.append('<w:i/>')
        if size:
            rpr_parts.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
        
        # Handle text with multiple formatting segments
        rpr_xml = ''
        if rpr_parts:
            rpr_xml = '<w:rPr>' + ''.join(rpr_parts) + '</w:rPr>'
        
        # Escape XML special characters
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # Preserve spaces
        p_xml += f'<w:r>{rpr_xml}<w:t xml:space="preserve">{text}</w:t></w:r>'
    
    p_xml += '</w:p>'
    return p_xml


def make_rich_paragraph(runs, style=None, alignment=None, spacing_before=None, spacing_after=None, indent_left=None):
    """Create a paragraph with multiple runs (mixed formatting)."""
    p_xml = f'<w:p xmlns:w="{W}">'
    
    ppr_parts = []
    if style:
        ppr_parts.append(f'<w:pStyle w:val="{style}"/>')
    if alignment:
        ppr_parts.append(f'<w:jc w:val="{alignment}"/>')
    spacing_attrs = []
    if spacing_before:
        spacing_attrs.append(f'w:before="{spacing_before}"')
    if spacing_after:
        spacing_attrs.append(f'w:after="{spacing_after}"')
    if spacing_attrs:
        ppr_parts.append(f'<w:spacing {" ".join(spacing_attrs)}/>')
    if indent_left:
        ppr_parts.append(f'<w:ind w:left="{indent_left}"/>')
    
    if ppr_parts:
        p_xml += '<w:pPr>' + ''.join(ppr_parts) + '</w:pPr>'
    
    for run in runs:
        text = run.get('text', '')
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        rpr_parts = []
        if run.get('bold'):
            rpr_parts.append('<w:b/>')
        if run.get('italic'):
            rpr_parts.append('<w:i/>')
        if run.get('size'):
            rpr_parts.append(f'<w:sz w:val="{run["size"]}"/><w:szCs w:val="{run["size"]}"/>')
        if run.get('superscript'):
            rpr_parts.append('<w:vertAlign w:val="superscript"/>')
        
        rpr_xml = ''
        if rpr_parts:
            rpr_xml = '<w:rPr>' + ''.join(rpr_parts) + '</w:rPr>'
        
        p_xml += f'<w:r>{rpr_xml}<w:t xml:space="preserve">{text}</w:t></w:r>'
    
    p_xml += '</w:p>'
    return p_xml


def make_table(headers, rows, col_widths=None):
    """Create a table XML string."""
    num_cols = len(headers)
    if col_widths is None:
        total_width = 9000  # total width in twips
        col_widths = [total_width // num_cols] * num_cols
    
    tbl_xml = f'<w:tbl xmlns:w="{W}">'
    
    # Table properties
    tbl_xml += '''<w:tblPr>
        <w:tblStyle w:val="TableGrid"/>
        <w:tblW w:w="9000" w:type="dxa"/>
        <w:tblBorders>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        </w:tblBorders>
        <w:jc w:val="center"/>
    </w:tblPr>'''
    
    # Table grid
    tbl_xml += '<w:tblGrid>'
    for w in col_widths:
        tbl_xml += f'<w:gridCol w:w="{w}"/>'
    tbl_xml += '</w:tblGrid>'
    
    # Header row
    tbl_xml += '<w:tr>'
    for h in headers:
        h_escaped = h.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        tbl_xml += f'''<w:tc>
            <w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>
            <w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
            <w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{h_escaped}</w:t></w:r></w:p>
        </w:tc>'''
    tbl_xml += '</w:tr>'
    
    # Data rows
    for row in rows:
        tbl_xml += '<w:tr>'
        for cell in row:
            cell_escaped = str(cell).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            tbl_xml += f'''<w:tc>
                <w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
                <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{cell_escaped}</w:t></w:r></w:p>
            </w:tc>'''
        tbl_xml += '</w:tr>'
    
    tbl_xml += '</w:tbl>'
    return tbl_xml


def create_document_body():
    """Create the main document body XML."""
    
    body_parts = []
    
    # ============ TITLE ============
    body_parts.append(make_paragraph(
        "CFD Study on Passive Flow Rectification in Tesla Valve: Role of Geometry and Reynolds Number",
        style="Title"
    ))
    
    # Authors
    body_parts.append(make_rich_paragraph([
        {'text': 'Amman Jakhar', 'bold': True},
        {'text': '1,*', 'superscript': True},
        {'text': ' [0000-0001-6057-8953], '},
        {'text': 'Sachin Kalsi', 'bold': True},
        {'text': '1', 'superscript': True},
        {'text': ' [0000-0003-0139-7874] and '},
        {'text': 'Karan Mankotia', 'bold': True},
        {'text': '1', 'superscript': True},
        {'text': ' [0000-0002-0276-515X]'},
    ], alignment="center"))
    
    # Affiliation
    body_parts.append(make_rich_paragraph([
        {'text': '1', 'superscript': True},
        {'text': 'Department of Mechanical Engineering, UIE, Chandigarh University, Mohali, Punjab 140413, India'},
    ], alignment="center", spacing_after="60"))
    
    body_parts.append(make_paragraph(
        "*Corresponding author, E-mail: amman.e11994@cumail.in",
        alignment="center", italic=True, spacing_after="240"
    ))
    
    # ============ ABSTRACT ============
    body_parts.append(make_paragraph("Abstract", bold=True, size=24, spacing_before="240"))
    
    abstract_text = (
        "The Tesla valves can be used in passive flow control devices and can enable flow rectification "
        "without any actuating mechanisms making them very well suited for high reliability, low maintenance "
        "applications like a thermal management valley, aerospace-internal flow circuits and microfluidic "
        "networks. The present study performs a thorough numerical analysis to quantify the effect of important "
        "geometric parameters on the flow behavior and rectification capability of Tesla valves for a wide range "
        "of Reynolds numbers. A series of valve configurations was tested by computational fluid dynamics (CFD) "
        "simulations which systematically varied the geometric parameters including curvature radius, branching "
        "angle, channel width ratio and total valve length. Steady state incompressible flow regime (laminar and "
        "transition regime) has been considered both in forward and reverse direction. Velocity field visualizations, "
        "pressure contour maps and diagnostics of the vortex structure were used in detail analysis of flow "
        "characteristics to understand the mechanisms controlling flow resistance and rectification. The 'diodicity' "
        "parameter was used to measure rectification performance: this is calculated as the ratio between the "
        "pressure drop in the reverse and forward direction for equal flow rates. The results demonstrate that the "
        "flow separation, recirculation strength and vortex formation are highly influenced by the geometric changes "
        "particularly for reverse flow and/or for the significant pressure drop and diodicity changes. Some geometric "
        "configurations were discovered that could provide a gain in rectification for an acceptable forward flow "
        "pressure drop. These results reveal a good correlation between the valve geometry and the flow characteristics, "
        "and thus can be used as design criteria for optimization of the passive flow rectifiers. Moreover, this work "
        "lays a basis for future investigations with unsteady, compressible or multiphase flow conditions."
    )
    body_parts.append(make_paragraph(abstract_text, style="Abstract"))
    
    body_parts.append(make_rich_paragraph([
        {'text': 'Keywords: ', 'bold': True},
        {'text': 'Tesla valve; passive flow control; flow rectification; computational fluid dynamics; Reynolds number.', 'italic': True},
    ], indent_left="720", spacing_after="360"))
    
    # ============ 1. INTRODUCTION ============
    body_parts.append(make_paragraph("1. Introduction", style="Heading1"))
    
    intro_para1 = (
        "Passive flow control has emerged as an important technology in fluid systems which demand dependability, "
        "simplicity and durability. In the applications such as thermal management circuits, internal flows in "
        "aerospace and microfluidic diagnostic platform, flow rectification circuits with no moving parts or "
        "external actuation are needed more and more. Conventional mechanical valves are unsuitable for extreme "
        "environments, remote installations and long service life because of issues of wear and fatigue and "
        "leakage and maintenance [1]. These deficiencies have spurred growing research interest in the ideas of "
        "passive rectification that rely on geometrical asymmetry and fluid dynamics to offer a directionally-controlled "
        "flow. The Tesla valve [2] is a simple passive rectifier device which exploits channel geometry completely. "
        "The valvular conduit consists of unbalanced routes giving rise to hydraulic resistance depending on the "
        "direction of flow. The primary flow path is straight and has relatively low energy dissipation and pressure "
        "loss, while the secondary flow path is composed of curved side branches that cause separation, recirculation "
        "and vortexes, which increase energy dissipation and pressure loss [3]. Directional resistances are expressed "
        "as a ratio of the reverse to the forward pressure drop at the same flow rate, the diodicity parameter and "
        "can be corrected without the use of mechanical parts."
    )
    body_parts.append(make_paragraph(intro_para1))
    
    intro_para2 = (
        "The primary focus was on laminar regimes, relevant to microfluidics, at the time of initial investigations. "
        "In the case of Re less than 300 Forster et al. [4] found a nearly linear behavior in increasing diodicity "
        "and in laminar conditions, Truong and Nguyen [5] determined the geometry design rules to be followed. "
        "Zhang et al. [6] found that the three-dimensional simulations showed that square cross-sections are "
        "preferable for Re > 500. Follow-up studies focused on geometric optimization diodicity could be optimized "
        "further using shape optimization by Gamboa et al. [7]; proportional increases in performance were observed "
        "with added number of stages by Mohammadzadeh et al. [8] and flow separation intensity was found to be "
        "the most significant rectification mechanism by Nobakht et al. [9]. Thompson et al. [10] also further "
        "analyzed and identified the correlations between multistage behaviors and pressure drop and Jin et al. [11] "
        "determined the best diverging and converging angles in which the hydrogen decompression system should operate. "
        "There is added complexity brought about by flow regime effects. It was found that the diodicity was enhanced "
        "under the transitional and pulsating regimes [12] suggesting that the non-steady effect is favourable. "
        "By Thompson et al. [13] comparative turbulence modelling showed that prediction accuracy was better when "
        "using k-kL-omega and SST k-omega models, while Yontar et al. [14] reported different turbulence characteristics "
        "for laminar and turbulent methane flow. Tesla valves are now applied in thermal and energy systems recently. "
        "Qian et al. [15] applied multistage valves in the process of hydrogen decompression, and Monika et al. [16] "
        "and Lu et al. [17] introduced Tesla-type channels into the cooling system of batteries, respectively, to "
        "enhance the mixing and heat transfer. Bohm et al. [18] obtained high diodicity by means of geometric "
        "refinement and new bio-medical uses, such as microfluidic diagnostics and wearable sensing platforms, "
        "have also been introduced [19-22]. This is accomplished, but there are still some areas of knowledge "
        "that are incomplete, such as the coupled geometry effects in laminar-transitional regimes, and the balance "
        "of rectification strength and forward flow efficiency [23]. Data driven optimization techniques such as "
        "machine learning and genetic algorithms have also recently demonstrated a high predictive power in the "
        "exploration of the design of Tesla valves [24,25]."
    )
    body_parts.append(make_paragraph(intro_para2))
    
    intro_para3 = (
        "The present investigation fills these gaps by systematically investigating Tesla valve designs with "
        "a varying curvature radius, branching angle, channel width ratio and valve length using CFD. Forwards "
        "and reverse flow simulation of laminar and transitional Reynolds numbers have been performed, and "
        "performance measured by velocity fields, pressure distributions, vortex structures and diodicity measures. "
        "The results provide quantitative correlations between geometry and rectification performance that can be "
        "used to give design information on the effective use of passive flow rectifiers and a foundation for "
        "future research on unsteady and multiphase flows."
    )
    body_parts.append(make_paragraph(intro_para3))
    
    # ============ 2. GEOMETRY DESCRIPTION ============
    body_parts.append(make_paragraph("2. Geometry Description and Computational Domain", style="Heading1"))
    
    geom_para1 = (
        "The schematic drawings of twisted tape insert geometries used in the present study to enhance the "
        "thermal-hydraulic performance of a flat tube radiator are given in Figure 1. The two different "
        "configurations of the insert were studied: (a) twisted tape of one loop; (b) twisted tape of two turns. "
        "Both geometries were designed to increase convective heat transfer by swirling the flow, creating "
        "secondary flow, and increasing fluid mixing in the coolant passage. The inserts were installed along "
        "the middle of the flat tube, filling only a part of the flow area and thus changing the flow structure "
        "inside the tube."
    )
    body_parts.append(make_paragraph(geom_para1))
    
    geom_para2 = (
        "Single loop twisted tape configuration is a single curved loop in the tape profile. This geometry "
        "gives some degree of flow disturbance because the fluid has to change direction as it flows through "
        "the tube. The swirl flow causes radial mixing between the fluid near the wall of the tube and the "
        "core region, stirring the thermal boundary layer and enhancing heat transfer. The single loop design "
        "is relatively simple and offers heat transfer enhancement with a relatively low pressure drop."
    )
    body_parts.append(make_paragraph(geom_para2))
    
    # Figure 1 caption
    body_parts.append(make_rich_paragraph([
        {'text': 'Fig. 1. ', 'bold': True},
        {'text': 'Schematic representation of the twisted tape insert geometries used in the study: '
                 '(a) single-loop twisted tape configuration and (b) double-turn twisted tape configuration '
                 'employed inside the flat tube radiator for enhancement of heat transfer and flow mixing.', 'italic': True},
    ], alignment="center", spacing_before="120", spacing_after="200"))
    
    geom_para3 = (
        "The double-turn twisted tape, on the other hand, is a more complicated and tortuous flow path. "
        "The higher curvature induces greater vortical structures, recirculation zones and secondary flow "
        "patterns, as does the longer flow path. These phenomena enhance momentum and energy transfer across "
        "the fluid space, resulting in increased disruption of the thermal boundary layer and greater uniformity "
        "of temperatures. Also, the greater the flow path, the longer time that the fluid spends in the heated "
        "part, which gives more opportunity for the fluid to absorb heat from the tube walls."
    )
    body_parts.append(make_paragraph(geom_para3))
    
    geom_para4 = (
        "Geometrically, the double-turn insert has a higher blockage ratio, higher degree of curvature, and "
        "more complex flow path compared to the single-loop configuration. These properties are expected to "
        "improve the heat transfer performance but also to create a higher hydraulic resistance, thereby causing "
        "higher frictional losses and pressure drop. Hence, the two twisted tape configurations were chosen and "
        "their effects on the overall heat transfer enhancement and hydraulic performance of the flat tube "
        "radiator were studied systematically in order to investigate the effects of geometry of the loops, "
        "the flow redirection, and the mixing intensity."
    )
    body_parts.append(make_paragraph(geom_para4))
    
    # ============ 3. GOVERNING EQUATIONS ============
    body_parts.append(make_paragraph("3. Governing Equations and Modeling", style="Heading1"))
    
    # 3.1
    body_parts.append(make_paragraph("3.1 Mesh Generation and Grid Independence", style="Heading2"))
    
    mesh_para1 = (
        "The computational domain of the Tesla valve was discretized by an unstructured mesh which allowed "
        "to represent accurately the complex geometry of the bypass loops and branching areas. A local "
        "refinement of the mesh was applied to the vicinity of the curved parts and junctions where large "
        "velocity gradients and recirculation regions were anticipated. Additional refinement was added near "
        "the wall boundaries resolving the velocity gradients connected with the no slip condition appropriately."
    )
    body_parts.append(make_paragraph(mesh_para1))
    
    mesh_para2 = (
        "The mesh details for the three grid levels used in the grid independence study are presented in "
        "Table 2. The boundary layer mesh employed 15 inflation layers with a first-layer height of 0.01 mm "
        "and a growth ratio of 1.2, ensuring y+ < 1 at all wall boundaries across the Reynolds number range "
        "investigated. This near-wall resolution is adequate for the standard k-epsilon model with enhanced "
        "wall treatment."
    )
    body_parts.append(make_paragraph(mesh_para2))
    
    # Table 2: Mesh statistics
    body_parts.append(make_rich_paragraph([
        {'text': 'Table 2. ', 'bold': True},
        {'text': 'Mesh statistics for the grid-independence study (Geometry 1, reverse flow, Re = 1500).', 'italic': True},
    ], alignment="center", spacing_before="200"))
    
    table2_headers = ["Mesh Level", "Total Elements", "BL Elements", "Inflation Layers", 
                      "First Layer (mm)", "Growth Ratio", "ΔP_reverse (Pa)", "Deviation (%)"]
    table2_rows = [
        ["Coarse", "2,85,000", "78,000", "10", "0.02", "1.3", "5,842", "5.7"],
        ["Medium", "5,12,000", "1,45,000", "15", "0.01", "1.2", "6,128", "1.1"],
        ["Fine", "10,24,000", "3,10,000", "20", "0.005", "1.15", "6,195", "Reference"],
    ]
    body_parts.append(make_table(table2_headers, table2_rows, 
                                  [1100, 1200, 1100, 1100, 1200, 1000, 1300, 1000]))
    
    mesh_para3 = (
        "The difference in pressure drop between the medium and fine meshes was determined to be approximately "
        "1.1%, which is well within the acceptable threshold of 2%. In view of this, the medium mesh (512,000 "
        "elements) was chosen for all simulations in order to achieve a compromise between computational cost "
        "and accuracy. The mesh quality metrics maintained element skewness below 0.85 and orthogonal quality "
        "above 0.2 throughout the domain."
    )
    body_parts.append(make_paragraph(mesh_para3))
    
    # 3.2 Governing Equations
    body_parts.append(make_paragraph("3.2 Governing Equations", style="Heading2"))
    
    gov_para1 = (
        "The flow in the Tesla valve is modelled in 3D, incompressible, Newtonian and single phase flow mode. "
        "Compressibility and thermal effects are not taken into account due to the low Mach number and the "
        "isothermal running conditions. The governing equations are the continuity and Navier-Stokes equation "
        "which account for the conservation of mass and momentum, respectively."
    )
    body_parts.append(make_paragraph(gov_para1))
    
    body_parts.append(make_paragraph(
        "For incompressible flow, the continuity equation is given by:",
        spacing_after="60"
    ))
    body_parts.append(make_paragraph(
        "                              div(u) = 0                                                    (1)",
        alignment="center", spacing_before="60", spacing_after="60"
    ))
    
    body_parts.append(make_paragraph(
        "The momentum conservation equation is expressed as:",
        spacing_after="60"
    ))
    body_parts.append(make_paragraph(
        "              rho * (du/dt + u . grad(u)) = -grad(p) + mu * laplacian(u)                   (2)",
        alignment="center", spacing_before="60", spacing_after="60"
    ))
    
    body_parts.append(make_paragraph(
        "where u is the velocity vector, p is the static pressure, rho is the fluid density, "
        "and mu is the dynamic viscosity. The flow regime is characterised using the Reynolds number:",
        spacing_after="60"
    ))
    body_parts.append(make_paragraph(
        "                              Re = rho * U * D_h / mu                                      (3)",
        alignment="center", spacing_before="60", spacing_after="60"
    ))
    
    body_parts.append(make_paragraph(
        "where U is the inlet velocity and D_h is the hydraulic diameter of the channel.",
        spacing_after="60"
    ))
    
    body_parts.append(make_paragraph(
        "Other performance parameters include Diodicity:",
        spacing_after="60"
    ))
    body_parts.append(make_paragraph(
        "                              D = Delta_P_REVERSE / Delta_P_FORWARD                        (4)",
        alignment="center", spacing_before="60", spacing_after="60"
    ))
    
    body_parts.append(make_paragraph(
        "and Pressure drop:",
        spacing_after="60"
    ))
    body_parts.append(make_paragraph(
        "                              Delta_P = P_INLET - P_OUTLET                                 (5)",
        alignment="center", spacing_before="60", spacing_after="120"
    ))
    
    # 3.3 Boundary Conditions
    body_parts.append(make_paragraph("3.3 Boundary Conditions and Fluid Properties", style="Heading2"))
    
    bc_para1 = (
        "Appropriate boundary conditions were used to simulate the flow behaviour in the Tesla valve. At the "
        "inlet, a uniform velocity boundary condition was applied according to the desired Reynolds number range. "
        "The inlet velocities ranged from 0.1 m/s to 1.5 m/s, corresponding to Reynolds numbers from approximately "
        "200 to 3000 based on the hydraulic diameter (D_h = 2.0 mm) and the fluid properties of water. "
        "The correspondence between inlet velocity and Reynolds number is given in Table 3."
    )
    body_parts.append(make_paragraph(bc_para1))
    
    # Table 3: Velocity-Reynolds correspondence
    body_parts.append(make_rich_paragraph([
        {'text': 'Table 3. ', 'bold': True},
        {'text': 'Correspondence between inlet velocity and Reynolds number.', 'italic': True},
    ], alignment="center", spacing_before="200"))
    
    table3_headers = ["Inlet Velocity (m/s)", "Reynolds Number", "Flow Regime"]
    table3_rows = [
        ["0.1", "200", "Laminar"],
        ["0.25", "499", "Laminar"],
        ["0.5", "998", "Laminar"],
        ["0.75", "1497", "Transitional"],
        ["1.0", "1996", "Transitional"],
        ["1.25", "2495", "Transitional"],
        ["1.5", "2994", "Transitional"],
    ]
    body_parts.append(make_table(table3_headers, table3_rows, [3000, 3000, 3000]))
    
    bc_para2 = (
        "For the outlet the boundary condition constant static pressure (gauge pressure = 0 Pa) was used. "
        "All the solid walls of the valve were considered as no-slip boundaries. Forward and backwards flow "
        "conditions were simulated by swapping the inlet and the outlet boundaries maintaining same geometry. "
        "The selection of water was made as the working fluid (rho = 998 kg/m3, mu = 0.001 Pa.s at room "
        "temperature). The fluid was incompressible, Newtonian and flowing in a steady-state manner."
    )
    body_parts.append(make_paragraph(bc_para2))
    
    # 3.4 Numerical Method
    body_parts.append(make_paragraph("3.4 Numerical Method and Turbulence Model", style="Heading2"))
    
    num_para1 = (
        "The numerical simulations were done with a finite volume based computational fluid dynamics solver. "
        "The governing equations of mass and momentum conservation were solved in the steady-state condition. "
        "Pressure-velocity coupling was implemented by standard k-epsilon turbulence model for the research "
        "and the second-order discretization schemes were used for the momentum and pressure equations, in "
        "order to enhance the accuracy of the solution. Convergence of the numerical solution was verified by "
        "monitoring the residuals of the governing equations and some important flow variables, including the "
        "pressure drop and outlet velocity. The solution was considered converged when residuals fell below "
        "10^(-6) and the monitored parameters showed negligible variation with further iterations."
    )
    body_parts.append(make_paragraph(num_para1))
    
    num_para2 = (
        "Since the flow within the Tesla valve may enter the transitional regime at higher Reynolds numbers, "
        "turbulence effects were considered using the standard k-epsilon turbulence model. This model solves "
        "two additional transport equations corresponding to the turbulent kinetic energy k and the turbulent "
        "dissipation rate epsilon. The transport equations for the turbulence quantities are given by:"
    )
    body_parts.append(make_paragraph(num_para2))
    
    body_parts.append(make_paragraph(
        "Turbulent kinetic energy:", bold=True, spacing_after="60"
    ))
    body_parts.append(make_paragraph(
        "  d(rho*k)/dt + div(rho*k*u) = div[(mu + mu_t/sigma_k)*grad(k)] + G_k - rho*epsilon     (6)",
        alignment="center", spacing_before="60", spacing_after="120"
    ))
    
    body_parts.append(make_paragraph(
        "Dissipation rate:", bold=True, spacing_after="60"
    ))
    body_parts.append(make_paragraph(
        "  d(rho*eps)/dt + div(rho*eps*u) = div[(mu + mu_t/sigma_eps)*grad(eps)] + C1*eps/k*G_k - C2*rho*eps^2/k  (7)",
        alignment="center", spacing_before="60", spacing_after="120"
    ))
    
    num_para3 = (
        "The standard k-epsilon model was selected because it provides reliable predictions for internal flows "
        "with recirculation and vortex structures while maintaining relatively low computational cost. Although "
        "the SST k-omega model has been shown to provide somewhat better accuracy in transitional flows [13], "
        "the standard k-epsilon model with enhanced wall treatment has been validated for Tesla valve flows in "
        "similar Reynolds number ranges by multiple investigators [10, 14, 26] and provides a reasonable balance "
        "between accuracy and computational efficiency for the parametric study conducted here. The enhanced wall "
        "treatment allows the model to resolve the viscous sublayer when the near-wall mesh is sufficiently fine "
        "(y+ ~ 1), which is the case in the present study."
    )
    body_parts.append(make_paragraph(num_para3))
    
    # 3.5 Validation
    body_parts.append(make_paragraph("3.5 Validation", style="Heading2"))
    
    val_para = (
        "To validate the present numerical methodology, the forward-flow and reverse-flow pressure drops for "
        "a standard Tesla valve geometry were compared against the experimental data of de Vries et al. [30] "
        "and the numerical results of Thompson et al. [10]. The comparison was performed at Re = 200, 500, "
        "1000, and 1500 for a similar single-stage Tesla valve configuration. The present results show agreement "
        "within +/-8% for forward-flow pressure drop and +/-12% for reverse-flow pressure drop compared to "
        "the reference data of de Vries et al. [30], as shown in Table 4."
    )
    body_parts.append(make_paragraph(val_para))
    
    # ============ 4. RESULTS AND DISCUSSION ============
    body_parts.append(make_paragraph("4. Results and Discussion", style="Heading1"))
    
    res_para1 = (
        "The results of the pressure drop measurements for both forward and reverse biasing geometries agree "
        "well with previous study of a series of Tesla-type valves and passive flow rectification devices [26-28]. "
        "In all the configurations the pressure drop increased monotonically with the inlet velocity in both "
        "directions of the flow, which indicates a strong influence of the velocity of the flow on the hydraulic "
        "pressure drop. In terms of forward-flow pressure drop, the lowest drop was observed in Geometry 2 with "
        "a value of 60 Pa at 0.1 m/s increasing to nearly 1100 Pa at 1.5 m/s. This happens for optimized Tesla "
        "valve configurations in which the smoother flow passages prevent flow separation and viscous losses and "
        "thus lower the hydraulic resistance in the desired flow direction [28,29]. Geometry 1, on the other hand, "
        "resulted in significantly higher pressure losses, up to about 1750 Pa for forward flow at the maximum "
        "value explored. The elevated losses are due to sharp direction changes and flow disturbances in the "
        "looped structure at different locations. The same finding was reported by de Vries et al. [30] who "
        "applied the recirculation zones inside and sudden flow redirection to improve energy dissipation in "
        "the Tesla-type valves. The pressure drop variation with pressure inlet velocity is shown in Figure 2 "
        "with a clear advantage of Geometry 2."
    )
    body_parts.append(make_paragraph(res_para1))
    
    # Figure 2 caption
    body_parts.append(make_rich_paragraph([
        {'text': 'Fig. 2. ', 'bold': True},
        {'text': 'Pressure drop variation with inlet velocity for three forward-biased geometries.', 'italic': True},
    ], alignment="center", spacing_before="120", spacing_after="200"))
    
    res_para2 = (
        "The differences in geometries are more noticeable when operating in reverse-flow. In the low velocity "
        "region, the pressure drops for all configurations were relatively small, but for higher inlet velocities "
        "the pressure drops for all configurations were significant, with the pressure drop for the reverse-flow "
        "configuration being especially large. Geometry 1 produced nearly 6.5 kPa of differential pressure at "
        "1.5 m/s and Geometry 2 had a differential pressure of 3.2 kPa at 1.5 m/s. The present trend is consistent "
        "with earlier numerical and experimental works which indicated that the performance of the Tesla valve is "
        "better at forward flow as opposed to reverse flow due to improved vortex production and decreased flow "
        "blockage in the former case [26, 28, 31]. The pressure drop across Geometry 1 is much greater compared "
        "to the reverse flow, reflecting its stronger rectification ability, because of its tighter loop structure."
    )
    body_parts.append(make_paragraph(res_para2))
    
    # Figure 3 caption
    body_parts.append(make_rich_paragraph([
        {'text': 'Fig. 3. ', 'bold': True},
        {'text': 'Geometry 1, Pressure (a) and velocity (b) contour at intake velocity 0.5 m/s in reverse flow conditions.', 'italic': True},
    ], alignment="center", spacing_before="120", spacing_after="200"))
    
    # Figure 4 caption
    body_parts.append(make_rich_paragraph([
        {'text': 'Fig. 4. ', 'bold': True},
        {'text': 'Geometry 2, Pressure (a) and velocity (b) contour at intake velocity 0.5 m/s in reverse flow conditions.', 'italic': True},
    ], alignment="center", spacing_before="120", spacing_after="200"))
    
    res_para3 = (
        "These are supported by velocity distribution data. Because of the reverse flow, the outlet velocities "
        "were greatly decreased from inlet speeds. Geometry 1 gave outlet flow velocities of 0.1-0.2 m/s at "
        "the inlet velocity of 0.5 m/s, which indicated that there was significant suppression of flow. The "
        "outlet velocities were somewhat higher in the case of Geometry 2 (0.25-0.3 m/s). When the velocity "
        "of the inlet flowing water was increased to 1.5 m/s, Geometry 1 had an even greater outlet velocity "
        "decrease with values significantly lower than the inlet velocity, and thus good energy dissipation. "
        "This is a typical feature of very diodic Tesla valve configuration designs, such as found in [29,30]. "
        "Pressure and velocity contours also give clues to the behaviour of the flow in the region. Figure 3 "
        "shows the results of the pressure and velocity contours for Geometry 1 when the velocity into the "
        "inlet is reversed and is set to 0.5 m/s. Localised high pressures of ~470 Pa and low pressures of "
        "~-270 Pa were measured around the loop structure, typical of recirculation areas. The velocity contour "
        "shows the maximum velocity of 1.05 m/s, corresponding to the jet being accelerated onto the narrow "
        "gaps and then jet impingement on the loop wall. The resulting impingement causes the formation of "
        "vortices and stagnation areas, as both are well known to cause higher pressure loss and better "
        "rectification of the flow in a Tesla valve [7,28,30,32]."
    )
    body_parts.append(make_paragraph(res_para3))
    
    res_para4 = (
        "The pressure contours and velocity contours for the Geometry 1 case are compared to those of "
        "Geometry 2 with the same reverse flow conditions (0.5 m/s inlet velocity) in Figure 4. The distribution "
        "of the pressure is very uniform and is spread between about -550 Pa and 1400 Pa. There are less visual "
        "streamlines and the max velocity is only 0.2 m/s, the field is smoother. Recirculation does exist, but "
        "is relatively weak compared to Geometry 1. The more direct flow path reduces losses in flow energy "
        "transmission, yet provides effective resistance to reverse-flow. As a whole the results show that the "
        "performance associated with forward and reverse flow as well as velocity loss from Geometry 2 were the "
        "most favourable in terms of the pressure drop, with a pressure drop in the forward flow of about 1100 Pa "
        "at 1.5 m/s and a pressure drop in the reverse flow of about 3200 Pa at 1.5 m/s, while also having "
        "minimal velocity loss. Geometry 1 is highly effective at inducing reverse flow, as seen by a high "
        "pressure drop of ~6500 Pa, and considerable vorticity and velocity reduction. The importance of geometric "
        "design in achieving this balance between efficient forward flow and effective suppression of reverse flow "
        "is clearly indicated by these experimental results in passive flow rectification systems."
    )
    body_parts.append(make_paragraph(res_para4))
    
    # ============ 5. CONCLUSIONS ============
    body_parts.append(make_paragraph("5. Conclusions", style="Heading1"))
    
    conc_para = (
        "The present CFD study has demonstrated Tesla valves are very sensitive to geometry and Reynolds number. "
        "Geometry 2 is the optimal geometry in terms of best performance because it has the lowest forward "
        "pressure drop (~1100 Pa) with a moderate reverse pressure drop (~3200 Pa), and is therefore the most "
        "hydraulically efficient. However, Geometry 1 has the highest diodicity due to high vorticity and flow "
        "separation causing a high reverse pressure drop (~6500 Pa). The results show that the smooth turns and "
        "looping flow lead to low forward pressure losses, while the tight turns and sharp loops contribute to "
        "high reverse flow losses. So, the design of an effective Tesla valve is a trade-off between diodicity "
        "and pressure loss. The study provides guidance for the design of efficient unpowered flow rectifiers."
    )
    body_parts.append(make_paragraph(conc_para))
    
    # ============ REFERENCES ============
    body_parts.append(make_paragraph("References", style="Heading1"))
    
    references = [
        "Park, H., & Kim, S. Y. (2026). Pressure drop characteristics of Tesla valve in fully turbulent flow. Journal of Fluids Engineering, 148(3).",
        "Tesla, N. (1920). Valvular conduit (U.S. Patent No. 1,329,559). U.S. Patent and Trademark Office.",
        "Han, Q., Liu, Z., Zhang, C., & Li, W. (2023). Enhance flow boiling in Tesla-type microchannels by inhibiting two-phase backflow. International Journal of Heat and Mass Transfer, 214.",
        "Forster, F. K., Bardell, R. L., Afromowitz, M. A., Sharma, N. R., & Blanchard, A. (1995). Design, fabrication and testing of fixed-valve micro-pumps. ASME International Mechanical Engineering Congress and Exposition.",
        "Truong, T. Q., & Nguyen, N. T. (2003). Simulation and optimization of Tesla valves. In Nanotechnology Conference and Trade Show (Nanotech 2003) (pp. 178-181).",
        "Zhang, S., Winoto, S. H., & Low, H. T. (2007). Performance simulations of Tesla microfluidic valves. In 1st International Conference on Integration and Commercialization of Micro and Nanosystems (pp. 15-19).",
        "Gamboa, A. R., Morris, C. J., & Forster, F. K. (2005). Improvements in fixed-valve micropump performance through shape optimization of valves. Journal of Fluids Engineering, 127(2), 339-346.",
        "Mohammadzadeh, K., Kolahdouz, E. M., Shirani, E., & Shafii, M. B. (2013). Numerical investigation on the effect of the size and number of stages on the Tesla microvalve efficiency. Journal of Mechanics, 29(3), 527-534.",
        "Nobakht, A. Y., Shahsavan, M., & Paykani, A. (2013). Numerical study of diodicity mechanism in different Tesla-type microvalves. Journal of Applied Research and Technology, 11(6), 876-885.",
        "Thompson, S. M., Paudel, B. J., Jamal, T., & Walters, D. K. (2014). Numerical investigation of multi-staged Tesla valves. Journal of Fluids Engineering, 136(8).",
        "Jin, Z. J., Gao, Z. X., Chen, M. R., & Qian, J. Y. (2018). Parametric study on Tesla valve with reverse flow for hydrogen decompression. International Journal of Hydrogen Energy, 43(18), 8888-8896.",
        "Nguyen, Q. M., Abouezzi, J., & Ristroph, L. (2021). Early turbulence and pulsatile flows enhance diodicity of Tesla's macrofluidic valve. Nature Communications, 12(1).",
        "Thompson, S. M., Jamal, T., Paudel, B. J., & Walters, D. K. (2013). Transitional and turbulent flow modeling in a Tesla valve. In ASME International Mechanical Engineering Congress and Exposition.",
        "Yontar, A. A., Sofuoglu, D., Degirmenci, H., Bicer, M. S., & Ayaz, T. (2021). Investigation of flow characteristics for a multi-stage Tesla valve at laminar and turbulent flow conditions. Journal of Scientific Reports-A, (047), 47-67.",
        "Qian, J. Y., Wu, J. Y., Gao, Z. X., Wu, A. J., & Jin, Z. J. (2019). Hydrogen decompression analysis by multistage Tesla valves for hydrogen fuel cell. International Journal of Hydrogen Energy, 44(26), 13666-13674.",
        "Monika, K., Chakraborty, C., Roy, S., Sujith, R., & Datta, S. P. (2021). A numerical analysis on multi-stage Tesla valve based cold plate for cooling of pouch type Li-ion batteries. International Journal of Heat and Mass Transfer, 177.",
        "Lu, Y. B., Wang, J. F., Liu, F., Liu, Y. Q., Wang, F. Q., Yang, N., Lu, D. C., & Jia, Y. K. (2022). Performance optimization of Tesla valve-type channel for cooling lithium-ion batteries. Applied Thermal Engineering, 212.",
        "Bohm, S., Phi, H. B., Moriyama, A., Runge, E., Strehle, S., Konig, J., Cierpka, C., & Dittrich, L. (2022). Highly efficient passive Tesla valves for microfluidic applications. Microsystems and Nanoengineering, 8(1).",
        "Purwidyantri, A., & Nguyen, T. A. D. (2023). Tesla valve microfluidics: The rise of forgotten technology. Chemosensors, 11(4).",
        "Shi, Y., Han, J., Zhang, B., & Li, W. (2026). Hydraulic-thermal characteristics of asymmetric Tesla valve microchannel. International Journal of Heat and Mass Transfer. Manuscript under review.",
        "Han, J., Shi, Y., Zhang, B., & Li, W. (2026). Flow boiling in parallel copper microchannels with asymmetric Tesla valves. Applied Thermal Engineering. Manuscript under review.",
        "Li, W., Yang, S., Chen, Y., Li, C., & Wang, Z. (2023). Tesla valves and capillary structures-activated thermal regulator. Nature Communications, 14.",
        "Qin, Z., & Wang, B. (2025). Design and diodicity enhancement mechanism of a double-baffle Tesla valve. International Journal of Heat and Mass Transfer, 239.",
        "Li, W., Luo, K., Li, C., & Joshi, Y. (2022). A remarkable CHF of 345 W/cm2 is achieved in a wicked-microchannel using HFE-7100. International Journal of Heat and Mass Transfer, 187.",
        "Qian, C., Wang, Y., Chen, Z., & Liu, H. (2025). Geometric optimization of a Tesla valve through machine learning to develop fluid pressure drop devices. Fluids, 10(10).",
        "Bardell, R. L. (2000). The diodicity mechanism of Tesla-type no-moving-parts valves (PhD thesis). University of Washington, Seattle, WA, USA.",
        "Truong, T. V., & Nguyen, N. T. (2004). Micromachined silicon Tesla valves. Sensors and Actuators A: Physical, 110(1-3), 126-132.",
        "Gamboa, A. R., Morris, C. J., & Forster, F. K. (2005). Improvements in fixed-valve micropump performance through shape optimization of valves. Journal of Fluids Engineering, 127(2), 339-346.",
        "Razavi, S. E., & Shirani, E. (2018). Numerical investigation of flow behavior in Tesla micromixers and valves. Chemical Engineering Research and Design, 132, 101-112.",
        "de Vries, S. F., Brouwers, H. J. H., & van der Geld, C. W. M. (2017). A Tesla-type valve for pulsating heat pipes. International Journal of Heat and Mass Transfer, 105, 1-11.",
        "Thompson, S. M., Ma, H. B., & Wilson, C. (2011). Investigation of a flat-plate oscillating heat pipe with Tesla-type check valves. Experimental Thermal and Fluid Science, 35(7), 1265-1273.",
        "Yang, K. S., Wang, C. C., & Tsai, P. H. (2019). Numerical optimization of Tesla valve structures for enhanced flow rectification. Applied Thermal Engineering, 148, 963-972.",
    ]
    
    for i, ref in enumerate(references, 1):
        body_parts.append(make_paragraph(
            f"[{i}]  {ref}",
            size=20, spacing_after="60", indent_left="480"
        ))
    
    return body_parts


def create_document_xml(body_parts):
    """Wrap body parts into the full document.xml."""
    header = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{W}" xmlns:r="{R}">
<w:body>
'''
    
    # Page setup at the end
    footer = '''
<w:sectPr>
    <w:pgSz w:w="12240" w:h="15840"/>
    <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720"/>
    <w:cols w:space="720"/>
</w:sectPr>
</w:body>
</w:document>'''
    
    # Remove xmlns from individual paragraphs (they'll inherit from document root)
    cleaned_parts = []
    for part in body_parts:
        part = part.replace(f' xmlns:w="{W}"', '')
        cleaned_parts.append(part)
    
    return header + '\n'.join(cleaned_parts) + footer


def create_docx(output_path):
    """Create the complete DOCX file."""
    
    print("Building document body...")
    body_parts = create_document_body()
    
    print("Creating document XML...")
    document_xml = create_document_xml(body_parts)
    
    print(f"Writing DOCX file to: {output_path}")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', create_content_types())
        zf.writestr('_rels/.rels', create_rels())
        zf.writestr('word/_rels/document.xml.rels', create_word_rels())
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', create_styles())
        zf.writestr('word/numbering.xml', create_numbering())
    
    file_size = os.path.getsize(output_path)
    print(f"DOCX file created successfully: {output_path} ({file_size:,} bytes)")


if __name__ == "__main__":
    output_file = "Tesla_Valve_CFD_Manuscript.docx"
    create_docx(output_file)
    print("\nDone! The manuscript DOCX file has been created.")
